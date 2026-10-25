---
title: "İsimlendirme ve Adres Defteri"
description: "I2P'nin insan tarafından okunabilir ana bilgisayar adlarını hedeflere nasıl eşlediği"
slug: "naming"
aliases:
  - "/tr/docs/specs/naming"
  - "/tr/docs/specs/naming/"
  - "/tr/docs/naming"
  - "/tr/docs/naming/"
lastUpdated: "2025-01"
accurateFor: "0.9.65"
---

## Genel Bakış

I2P, yerel ad-hedef eşlemesi üzerinde çalışmak üzere tasarlanmış genel bir adlandırma kütüphanesi ve temel uygulama ile birlikte gelir, ayrıca [adres defteri](#address-book) adlı bir eklenti uygulaması da içerir. I2P ayrıca Tor'un .onion adreslerine benzer [Base32 ana makine adlarını](#base32-names) da destekler.

Adres defteri, güven ağı (web-of-trust) tabanlı güvenli, dağıtık ve insan tarafından okunabilir bir adlandırma sistemidir. Sadece yerel benzersizlik zorunluluğu getirerek, tüm insan tarafından okunabilir isimlerin global olarak benzersiz olması gereksiniminden yalnızca vazgeçer. I2P'deki tüm mesajlar kriptografik olarak hedeflerine göre adreslenirken, farklı kişiler "Alice" için farklı hedeflere işaret eden yerel adres defteri girişlerine sahip olabilir. İnsanlar hâlâ güven ağlarında belirtilen eşlerin yayınlanmış adres defterlerini içe aktararak, üçüncü taraf aracılığıyla sağlanan girişleri ekleyerek veya (bazı kişiler ilk gelen ilk hizmet alan kayıt sistemi kullanarak bir dizi yayınlanmış adres defteri düzenlediklerinde) bu adres defterlerini isim sunucuları olarak ele alıp geleneksel DNS'yi taklit etmeyi seçerek yeni isimler keşfedebilir.

NOT: I2P adlandırma sisteminin arkasındaki mantık, ona karşı yaygın argümanlar ve olası alternatifler için [adlandırma tartışması](/docs/legacy/naming/) sayfasına bakın.

---

## İsimlendirme Sistemi Bileşenleri

I2P'de merkezi bir adlandırma otoritesi yoktur. Tüm ana bilgisayar adları yereldir.

İsimlendirme sistemi oldukça basittir ve çoğu router dışındaki uygulamalarda gerçekleştirilir, ancak I2P dağıtımı ile birlikte paketlenir. Bileşenler şunlardır:

1. Aramalar yapan ve ayrıca [Base32 ana makine adlarını](#base32-names) işleyen yerel [adlandırma servisi](#naming-services).
2. Router'dan arama talep eden ve başarısız aramalar için kullanıcıyı uzak jump servislerine yönlendiren [HTTP proxy](#http-proxy).
3. Kullanıcıların yerel hosts.txt dosyalarına ana makine eklemelerine olanak sağlayan HTTP [host-add formları](#host-add-services).
4. Kendi aramalarını yapan ve yönlendirme sağlayan HTTP [jump servisleri](#jump-services).
5. HTTP aracılığıyla alınan dış ana makine listelerini yerel liste ile birleştiren [adres defteri](#address-book) uygulaması.
6. Adres defteri yapılandırması ve yerel ana makine listelerinin görüntülenmesi için basit bir web arayüzü olan [SusiDNS](#susidns) uygulaması.

---

## İsimlendirme Servisleri

I2P'deki tüm hedefler 516-bayt (veya daha uzun) anahtarlardır. (Daha kesin olmak gerekirse, bu 256-baytlık bir genel anahtar artı 128-baytlık bir imzalama anahtarı artı 3-veya-daha-fazla baytlık bir sertifikadan oluşur ve Base64 gösteriminde 516 veya daha fazla bayttır. Null olmayan [Sertifikalar](/docs/legacy/naming/#certificates) şu anda imza türü belirtimi için kullanılmaktadır. Bu nedenle, yakın zamanda oluşturulan hedeflerdeki sertifikalar 3 bayttan fazladır.

Bir uygulama (i2ptunnel veya HTTP proxy) bir hedefi ad ile erişmek istediğinde, router o adı çözümlemek için çok basit bir yerel arama yapar.

### Hosts.txt İsimlendirme Servisi

hosts.txt Adlandırma Servisi, metin dosyaları üzerinde basit bir doğrusal arama yapar. Bu adlandırma servisi, 0.8.8 sürümüne kadar varsayılandı ve bu sürümde Blockfile Adlandırma Servisi ile değiştirildi. hosts.txt formatı, dosya binlerce girişe ulaştıktan sonra çok yavaş hale gelmişti.

Ana makine adlarını aramak ve bunları 516-bayt destination key'e dönüştürmek için üç yerel dosyada sırayla doğrusal arama yapar. Her dosya basit bir [yapılandırma dosyası formatında](/docs/specs/configuration/) olup, hostname=base64 şeklinde satır başına bir tane içerir. Dosyalar şunlardır:

1. privatehosts.txt
2. userhosts.txt
3. hosts.txt

### Blockfile İsimlendirme Servisi

Blockfile Adlandırma Servisi, hostsdb.blockfile adlı tek bir veritabanı dosyasında birden fazla "adres defteri" saklar. Bu Adlandırma Servisi, 0.8.8 sürümünden beri varsayılan olarak kullanılmaktadır.

Blockfile, basitçe birden fazla sıralanmış haritanın (anahtar-değer çiftleri) disk üzerinde depolanması olup, atlama listeleri olarak uygulanır. Blockfile formatı [Blockfile sayfasında](/docs/specs/blockfile/) belirtilmiştir. Kompakt bir formatta hızlı Destination arama sağlar. Blockfile ek yükü önemli olsa da, hedefler hosts.txt formatındaki gibi Base 64 yerine binary olarak depolanır. Ayrıca blockfile, gelişmiş adres defteri özelliklerini uygulamak için her giriş için keyfi metadata depolama yeteneği (ekleme tarihi, kaynak ve yorumlar gibi) sağlar. Blockfile depolama gereksinimi hosts.txt formatına göre mütevazı bir artış olup, blockfile arama sürelerinde yaklaşık 10 kat azalma sağlar.

Oluşturulduğunda, adlandırma servisi hosts.txt Adlandırma Servisi tarafından kullanılan üç dosyadan girişleri içe aktarır. Blok dosyası, privatehosts.txt, userhosts.txt ve hosts.txt adlı sıralı olarak aranacak üç harita tutarak önceki uygulamayı taklit eder. Ayrıca hızlı ters arama yapmak için bir ters arama haritası da tutar.

### Diğer Adlandırma Servisi Olanakları

Arama büyük/küçük harf duyarsızdır. İlk eşleşme kullanılır ve çakışmalar tespit edilmez. Aramalarda isimlendirme kurallarının zorlanması yoktur. Aramalar birkaç dakika önbelleğe alınır. Base 32 çözümlemesi [aşağıda açıklanmıştır](#base32-names). Naming Service API'sinin tam açıklaması için [Naming Service Javadocs](http://idk.i2p/javadoc-i2p/net/i2p/client/naming/package-summary.html) bölümüne bakın. Bu API, 0.8.7 sürümünde ekleme ve çıkarma işlemleri, hostname ile birlikte rastgele özelliklerin saklanması ve diğer özellikler sağlamak için önemli ölçüde genişletilmiştir.

### Alternatif ve Deneysel Adlandırma Hizmetleri

Adlandırma servisi `i2p.naming.impl=class` yapılandırma özelliği ile belirtilir. Başka uygulamalar da mümkündür. Örneğin, router içinde ağ üzerinden gerçek zamanlı aramalar (DNS benzeri) için deneysel bir tesis bulunmaktadır. Daha fazla bilgi için [tartışma sayfasındaki alternatiflere](/docs/legacy/naming/#alternatives) bakın.

HTTP proxy, '.i2p' ile biten tüm ana bilgisayar adları için router üzerinden arama yapar. Aksi takdirde, isteği yapılandırılmış bir HTTP outproxy'ye iletir. Bu nedenle, pratikte tüm HTTP (I2P Site) ana bilgisayar adları '.i2p' sözde-Üst Düzey Alanı ile bitmelidir.

Router hostname'i çözümleyemezse, HTTP proxy kullanıcıya birkaç "jump" servisinin bağlantılarını içeren bir hata sayfası döndürür. Ayrıntılar için aşağıya bakın.

---

## .i2p.alt Etki Alanı

Daha önce [RFC 6761](https://www.rfc-editor.org/rfc/rfc6761.html)'de belirtilen prosedürleri takip ederek [.i2p TLD'sini rezerve etmek için başvuruda bulunduk](https://datatracker.ietf.org/doc/draft-grothoff-iesg-special-use-p2p-names/). Ancak bu başvuru ve diğer tüm başvurular reddedildi ve RFC 6761 bir "hata" olarak ilan edildi.

GNUnet ekibi ve diğerleri tarafından yıllar süren çalışmalardan sonra, .alt domain'i 2023 sonu itibariyle [RFC 9476](https://www.rfc-editor.org/rfc/rfc9476.html) ile özel kullanım TLD'si olarak ayrıldı. IANA tarafından onaylanmış resmi kayıt kuruluşları bulunmamasına rağmen, .i2p.alt domain'ini başlıca gayri resmi kayıt kuruluşu [GANA](https://gana.gnunet.org/dot-alt/dot_alt.html) ile kaydettirdik. Bu, başkalarının domain'i kullanmasını engellemez, ancak bu durumu caydırmaya yardımcı olacaktır.

.alt domain'inin bir avantajı, teoride DNS çözümleyicilerinin RFC 9476'ya uyum sağlamak için güncellendiğinde .alt isteklerini iletmeyecek olmalarıdır ve bu da DNS sızıntılarını önleyecektir. .i2p.alt hostname'leriyle uyumluluk için, I2P yazılımları ve servisleri bu hostname'leri .alt TLD'sini çıkararak işleyecek şekilde güncellenmelidir. Bu güncellemeler 2024'ün ilk yarısında planlanmıştır.

Şu anda, .i2p.alt'ı I2P hostname'lerinin görüntülenmesi ve değişimi için tercih edilen biçim haline getirmek için herhangi bir plan bulunmamaktadır. Bu, daha fazla araştırma ve tartışma gerektiren bir konudur.

---

## Adres Defteri

### Gelen Abonelikler ve Birleştirme

Adres defteri uygulaması periyodik olarak diğer kullanıcıların hosts.txt dosyalarını alır ve birkaç kontrol sonrasında bunları yerel hosts.txt ile birleştirir. İsimlendirme çakışmaları ilk gelen ilk hizmet alır esasına göre çözülür.

Başka bir kullanıcının hosts.txt dosyasına abone olmak, onlara belirli bir miktar güven vermeyi içerir. Örneğin, yeni bir site için kendi anahtarlarını hızlıca girerek ve ardından yeni host/anahtar girdisini size iletmeden önce yeni bir siteyi 'ele geçirmelerini' istemezsiniz.

Bu nedenle, varsayılan olarak yapılandırılan tek abonelik `http://i2p-projekt.i2p/hosts.txt (http://udhdrtrcetjm5sxzskjyr5ztpeszydbh4dpl3pl4utgqqw2v4jna.b32.i2p/hosts.txt)` olup, I2P sürümünde bulunan hosts.txt dosyasının bir kopyasını içerir. Kullanıcılar yerel adres defteri uygulamalarında ek abonelikleri (subscriptions.txt veya [SusiDNS](#susidns) aracılığıyla) yapılandırmalıdır.

Diğer bazı genel adres defteri abonelik bağlantıları:

- http://i2host.i2p/cgi-bin/i2hostetag
- http://stats.i2p/cgi-bin/newhosts.txt

Bu hizmetlerin operatörleri, host'ları listelemek için çeşitli politikalara sahip olabilir. Bu listede yer almak onay anlamına gelmez.

### Adlandırma Kuralları

I2P içinde host adları konusunda teknik sınırlamalar bulunmasa da, adres defteri aboneliklerden içe aktarılan host adları üzerinde çeşitli kısıtlamalar uygular. Bunu temel tipografik mantık ve tarayıcı uyumluluğu ile güvenlik için yapar. Kurallar temelde RFC2396 Bölüm 3.2.2'dekilerle aynıdır. Bu kuralları ihlal eden host adları diğer router'lara yayılmayabilir.

Adlandırma Kuralları:

- İsimler içe aktarımda küçük harfe dönüştürülür.
- İsimler küçük harfe dönüştürüldükten sonra mevcut userhosts.txt ve hosts.txt dosyalarındaki (ancak privatehosts.txt değil) mevcut isimlerle çakışma açısından kontrol edilir.
- Küçük harfe dönüştürüldükten sonra yalnızca [a-z] [0-9] '.' ve '-' karakterlerini içermelidir.
- '.' veya '-' ile başlamamalıdır.
- '.i2p' ile bitmelidir.
- '.i2p' dahil olmak üzere maksimum 67 karakter.
- '..' içermemelidir.
- '.-' veya '-.' içermemelidir (0.6.1.33 sürümünden itibaren).
- IDN için 'xn--' hariç '--' içermemelidir.
- Base32 hostname'leri (*.b32.i2p) base 32 kullanımı için ayrılmıştır ve bu nedenle içe aktarılmasına izin verilmez.
- Proje kullanımı için ayrılmış belirli hostname'lere izin verilmez (proxy.i2p, router.i2p, console.i2p, mail.i2p, *.proxy.i2p, *.router.i2p, *.console.i2p, *.mail.i2p ve diğerleri)
- 'www.' ile başlayan hostname'ler önerilmez ve bazı kayıt servisleri tarafından reddedilir. Bazı adres defteri uygulamaları, aramalardan 'www.' öneklerini otomatik olarak çıkarır. Bu nedenle 'www.example.i2p' kaydetmek gereksizdir ve 'www.example.i2p' ile 'example.i2p' için farklı hedefler kaydetmek, bazı kullanıcılar için 'www.example.i2p'yi erişilemez hale getirir.
- Anahtarlar base64 geçerliliği açısından kontrol edilir.
- Anahtarlar hosts.txt'deki (ancak privatehosts.txt değil) mevcut anahtarlarla çakışma açısından kontrol edilir.
- Minimum anahtar uzunluğu 516 byte.
- Maksimum anahtar uzunluğu 616 byte (100 byte'a kadar sertifikaları hesaba katmak için).

Abonelik yoluyla alınan ve tüm kontrolleri geçen herhangi bir isim, yerel adlandırma servisi aracılığıyla eklenir.

Host adındaki '.' sembollerinin hiçbir önemi olmadığını ve herhangi bir gerçek adlandırma veya güven hiyerarşisini belirtmediğini unutmayın. Eğer 'host.i2p' adı zaten mevcutsa, herhangi birinin hosts.txt dosyasına 'a.host.i2p' adını eklemesini engelleyecek hiçbir şey yoktur ve bu ad diğerlerinin adres defteri tarafından içe aktarılabilir. Alt alan adlarını domain 'sahipleri' olmayanlara reddetme yöntemleri (sertifikalar?) ve bu yöntemlerin arzu edilirliği ve uygulanabilirliği, gelecekteki tartışmalar için konulardır.

Uluslararası Alan Adları (IDN) i2p'de de çalışır (punycode 'xn--' formatını kullanarak). Firefox'un konum çubuğunda IDN .i2p alan adlarının doğru şekilde görüntülenmesi için about:config'de 'network.IDN.whitelist.i2p (boolean) = true' ekleyin.

Adres defteri uygulaması privatehosts.txt dosyasını hiç kullanmadığından, pratikte bu dosya hosts.txt içinde zaten bulunan siteler için özel takma adlar veya "evcil hayvan isimleri" yerleştirmek için uygun olan tek yerdir.

### Gelişmiş Abonelik Beslemesi Formatı

0.9.26 sürümünden itibaren, abonelik siteleri ve istemciler imzalar dahil olmak üzere metadata içeren gelişmiş bir hosts.txt besleme protokolünü destekleyebilir. Bu format, standart hosts.txt hostname=base64destination formatı ile geriye dönük uyumludur. Ayrıntılar için [spesifikasyona](/docs/specs/subscription/) bakın.

### Giden Abonelikler

Address Book, birleştirilmiş hosts.txt dosyasını başkalarının abonelikleri için erişebileceği bir konuma (geleneksel olarak yerel I2P Site'ın ana dizinindeki hosts.txt) yayınlayacaktır. Bu adım isteğe bağlıdır ve varsayılan olarak devre dışıdır.

### Barındırma ve HTTP Taşıma Sorunları

Adres defteri uygulaması, eepget ile birlikte, aboneliğin web sunucusu tarafından döndürülen Etag ve/veya Last-Modified bilgilerini kaydeder. Bu, bir sonraki getirme işleminde hiçbir şey değişmemişse web sunucusunun '304 Not Modified' döndürmesi sayesinde gereken bant genişliğini büyük ölçüde azaltır.

Ancak değişiklik olmuşsa hosts.txt dosyasının tamamı indirilir. Bu konu hakkındaki tartışma için aşağıya bakın.

Statik bir hosts.txt veya eşdeğer bir CGI uygulaması sunan sunucuların Content-Length başlığı ve Etag veya Last-Modified başlığından birini göndermesi şiddetle önerilir. Ayrıca sunucunun uygun olduğunda '304 Not Modified' yanıtı göndermesini sağlayın. Bu, ağ bant genişliğini önemli ölçüde azaltacak ve bozulma olasılığını düşürecektir.

---

## Host Ekleme Servisleri

Bir host ekleme servisi, hostname ve Base64 anahtarını parametre olarak alan ve bunları yerel hosts.txt dosyasına ekleyen basit bir CGI uygulamasıdır. Eğer diğer router'lar o hosts.txt dosyasına abone olursa, yeni hostname/anahtar çifti ağ boyunca yayılacaktır.

Host ekleme hizmetlerinin, en azından yukarıda listelenen adres defteri uygulaması tarafından uygulanan kısıtlamaları uygulaması önerilir. Host ekleme hizmetleri, host adları ve anahtarlar üzerinde ek kısıtlamalar uygulayabilir, örneğin:

- 'Alt alan' sayısında sınırlama.
- Çeşitli yöntemlerle 'alt alanlar' için yetkilendirme.
- Hashcash veya imzalı sertifikalar.
- Host adları ve/veya içeriğin editöryal incelemesi.
- Hostların içeriğe göre kategorizasyonu.
- Belirli host adlarının rezervasyonu veya reddedilmesi.
- Belirli bir zaman diliminde kayıt edilen ad sayısında kısıtlamalar.
- Kayıt ve yayınlama arasında gecikmeler.
- Doğrulama için hostun çalışır durumda olması gerekliliği.
- Son kullanma tarihi ve/veya iptal.
- IDN sahtekarlık reddi.

---

## Jump Hizmetleri

Bir jump servisi, hostname'i parametre olarak alan ve sonuna `?i2paddresshelper=key` dizesi eklenerek uygun URL'ye 301 yönlendirmesi döndüren basit bir CGI uygulamasıdır. HTTP proxy eklenen dizeyi yorumlayacak ve bu anahtarı gerçek hedef olarak kullanacaktır. Ayrıca, proxy bu anahtarı önbelleğe alacağı için yeniden başlatılana kadar address helper gerekli olmayacaktır.

Abonelikler gibi, bir atlama servisinin kullanılmasının da belirli bir güven gerektirdiğini unutmayın, çünkü bir atlama servisi kötü niyetli olarak bir kullanıcıyı yanlış bir hedefe yönlendirebilir.

En iyi hizmeti sağlamak için, bir jump servisi yerel host listesinin güncel olması amacıyla birkaç hosts.txt sağlayıcısına abone olmalıdır.

---

## SusiDNS

SusiDNS basitçe adres defteri aboneliklerini yapılandırmak ve dört adres defteri dosyasına erişmek için bir web arayüzü ön ucudur. Asıl işin tamamı 'address book' uygulaması tarafından yapılır.

Şu anda SusiDNS içinde adres defteri isimlendirme kurallarının çok az uygulanması var, bu nedenle bir kullanıcı yerel olarak adres defteri abonelik kuralları tarafından reddedilecek olan host adlarını girebilir.

---

## Base32 İsimleri

I2P, Tor'un .onion adreslerine benzer Base32 host adlarını destekler. Base32 adresleri, tam 516 karakterlik Base64 Destination'lardan veya addresshelper'lardan çok daha kısa ve kullanımı kolaydır. Örnek: `ukeu3k5oycgaauneqgtnvselmt4yemvoilkln7jpvamvfx7dnkdq.b32.i2p`

Tor'da adres 16 karakter (80 bit) veya SHA-1 hash'inin yarısıdır. I2P tam SHA-256 hash'ini temsil etmek için 52 karakter (256 bit) kullanır. Format {52 karakter}.b32.i2p şeklindedir. Tor'un gizli servisleri için {52 karakter}.onion formatına dönüştürme [önerisi](https://blog.torproject.org/blog/tor-weekly-news-%E2%80%94-december-4th-2013) bulunmaktadır. Base32, tam Destination'ı almak için leaseSet'i aramak üzere I2CP üzerinden router'ı sorgulayan isimlendirme servisinde uygulanmaktadır. Base32 aramaları yalnızca Destination aktif olduğunda ve bir leaseSet yayınladığında başarılı olacaktır. Çözümleme bir network database araması gerektirebileceğinden, yerel adres defteri aramasından önemli ölçüde daha uzun sürebilir.

Base32 adresleri, hostname'lerin veya tam hedeflerin kullanıldığı çoğu yerde kullanılabilir, ancak isim hemen çözümlenmezse başarısız olabilecekleri bazı istisnalar vardır. Örneğin I2PTunnel, isim bir hedefe çözümlenmezse başarısız olacaktır.

---

## Genişletilmiş Base32 İsimleri

Genişletilmiş base 32 adları, şifrelenmiş lease set'leri desteklemek için 0.9.40 sürümünde tanıtıldı. Şifrelenmiş leaseset'ler için adresler, geleneksel base 32 adreslerinin 52 karakteri (32 bayt) ile karşılaştırıldığında, ".b32.i2p" dahil olmak üzere 56 veya daha fazla kodlanmış karakter (35 veya daha fazla çözümlenmiş bayt) ile tanımlanır. Ek bilgi için 123 ve 149 numaralı önerilere bakınız.

Standart Base 32 ("b32") adresleri hedefin hash değerini içerir. Bu, şifreli ls2 (öneri 123) için çalışmayacaktır.

Encrypted LS2 (öneri 123) için geleneksel bir base 32 adresi kullanamazsınız, çünkü bu sadece hedefin hash'ini içerir. Blinded olmayan public key'i sağlamaz. İstemciler leaseset'i almak ve şifrelemek için hedefin public key'ini, sig type'ını, blinded sig type'ını ve isteğe bağlı bir secret veya private key'i bilmek zorundadır. Bu nedenle, tek başına bir base 32 adresi yetersizdir. İstemci ya tam hedefi (public key içeren) ya da public key'in kendisini bilmelidir. İstemci address book'ta tam hedefe sahipse ve address book hash'e göre ters arama destekliyorsa, public key alınabilir.

Bu yüzden hash yerine public key'i base32 adresine koyan yeni bir formata ihtiyacımız var. Bu format aynı zamanda public key'in signature türünü ve blinding şemasının signature türünü de içermelidir.

Bu bölüm, bu adresler için yeni bir b32 formatını belgelemektedir. Tartışmalar sırasında bu yeni formatı "b33" adresi olarak adlandırmış olsak da, gerçek yeni format olağan ".b32.i2p" son ekini korumaktadır.

### Oluşturma ve kodlama

{56+ karakter}.b32.i2p (binary olarak 35+ karakter) şeklinde bir hostname oluşturun. Önce base 32 ile kodlanacak binary veriyi oluşturun:

```
flag (1 byte)
  bit 0: 0 for one-byte sigtypes, 1 for two-byte sigtypes
  bit 1: 0 for no secret, 1 if secret is required
  bit 2: 0 for no per-client auth,
         1 if client private key is required
  bits 7-3: Unused, set to 0

public key sigtype (1 or 2 bytes as indicated in flags)
  If 1 byte, the upper byte is assumed zero

blinded key sigtype (1 or 2 bytes as indicated in flags)
  If 1 byte, the upper byte is assumed zero

public key
  Number of bytes as implied by sigtype
```
Son işleme ve sağlama toplamı:

```
Construct the binary data as above.
Treat checksum as little-endian.
Calculate checksum = CRC-32(data[3:end])
data[0] ^= (byte) checksum
data[1] ^= (byte) (checksum >> 8)
data[2] ^= (byte) (checksum >> 16)

hostname = Base32.encode(data) || ".b32.i2p"
```
b32'nin sonundaki kullanılmayan bitler 0 olmalıdır. Standart 56 karakterlik (35 bayt) adres için kullanılmayan bit bulunmaz.

### Kod Çözme ve Doğrulama

```
Strip the ".b32.i2p" from the hostname
data = Base32.decode(hostname)
Calculate checksum = CRC-32(data[3:end])
Treat checksum as little-endian.
flags = data[0] ^ (byte) checksum
if 1 byte sigtypes:
  pubkey sigtype = data[1] ^ (byte) (checksum >> 8)
  blinded sigtype = data[2] ^ (byte) (checksum >> 16)
else (2 byte sigtypes) :
  pubkey sigtype = data[1] ^ ((byte) (checksum >> 8)) || data[2] ^ ((byte) (checksum >> 16))
  blinded sigtype = data[3] || data[4]
parse the remainder based on the flags to get the public key
```
### Gizli ve Özel Anahtar Bitleri

Secret ve private key bitleri, client'lara, proxy'lere veya diğer istemci tarafı kodlara leaseset'i deşifre etmek için secret ve/veya private key'in gerekli olacağını belirtmek için kullanılır. Belirli uygulamalar kullanıcıdan gerekli veriyi sağlamasını isteyebilir veya gerekli veri eksikse bağlantı girişimlerini reddedebilir.

### Notlar

- İlk 3 byte'ı hash ile XORlamak sınırlı bir checksum yeteneği sağlar ve başlangıçtaki tüm base32 karakterlerinin rastgele olmasını garanti eder. Yalnızca birkaç flag ve sigtype kombinasyonu geçerlidir, bu nedenle herhangi bir yazım hatası geçersiz bir kombinasyon oluşturacak ve reddedilecektir.
- Olağan durumda (1 byte sigtype'lar, secret yok, istemci başına auth yok), hostname {56 karakter}.b32.i2p olacak ve 35 byte'a decode olacaktır, Tor ile aynı.
- Tor 2-byte checksum'ında 1/64K false negative oranı vardır. 3 byte ile, birkaç göz ardı edilen byte çıkarıldığında, bizimki milyonda bire yaklaşıyor çünkü çoğu flag/sigtype kombinasyonu geçersiz.
- Adler-32 küçük girdiler için ve küçük değişiklikleri tespit etmek için kötü bir seçimdir. Bunun yerine CRC-32 kullanıyoruz. CRC-32 hızlıdır ve yaygın olarak mevcuttur.
- Bu spesifikasyonun kapsamı dışında olsa da, router'lar ve/veya istemciler public key'den destination'a ve tam tersine olan eşleştirmeyi hatırlamalı ve (muhtemelen kalıcı olarak) cache'lemelidir.
- Eski ve yeni türleri uzunluğa göre ayırt edin. Eski b32 adresleri her zaman {52 karakter}.b32.i2p'dir. Yenileri {56+ karakter}.b32.i2p'dir.
- Tor tartışma thread'i [burada](https://lists.torproject.org/pipermail/tor-dev/2017-January/011816.html)
- 2-byte sigtype'ların hiç gerçekleşmesini beklemeyin, daha ancak 13'e kadar çıktık. Şimdi implement etmeye gerek yok.
- Yeni format, b32 gibi jump link'lerde kullanılabilir (ve jump server'lar tarafından sunulabilir) istenirse.
- 32 byte'tan uzun herhangi bir secret, private key veya public key, DNS maksimum label uzunluğu olan 63 karakteri aşacaktır. Tarayıcılar muhtemelen umursamaz.
- Geriye dönük uyumluluk sorunu yok. Uzun b32 adresleri eski yazılımlarda 32-byte hash'lere dönüştürülmeye çalışıldığında başarısız olacaktır.
