---
title: "I2P üzerinden Bittorrent"
description: "I2P üzerindeki BitTorrent istemcileri ve tracker'ları için protokol spesifikasyonları"
slug: "bittorrent"
lastUpdated: "2026-08"
accurateFor: "0.9.70"
---

I2P üzerinde birkaç bittorrent istemcisi ve tracker bulunmaktadır. I2P adresleme sistemi IP ve port yerine Destination kullandığından, tracker ve istemci yazılımlarında I2P üzerinde çalışabilmek için küçük değişiklikler gereklidir. Bu değişiklikler aşağıda belirtilmiştir. Eski I2P istemcileri ve tracker'ları ile uyumluluk yönergelerine dikkatli bir şekilde uyun.

Bu sayfa, tüm istemciler ve tracker'lar için ortak olan protokol ayrıntılarını belirtir. Belirli istemciler ve tracker'lar diğer benzersiz özellikler veya protokoller uygulayabilir.

İstemci ve tracker yazılımlarının I2P'ye ek portlarını memnuniyetle karşılıyoruz.

---

## Geliştiriciler için Genel Rehberlik

Java olmayan çoğu bittorrent istemcisi I2P'ye [SAMv3](/docs/api/samv3/) üzerinden bağlanacaktır. SAM oturumları (veya I2P içinde tunnel havuzları veya tunnel setleri) uzun ömürlü olacak şekilde tasarlanmıştır. Çoğu bittorrent istemcisi yalnızca bir oturuma ihtiyaç duyacaktır; bu oturum başlangıçta oluşturulur ve çıkışta kapatılır. I2P, devrelerin hızla oluşturulup atılabileceği Tor'dan farklıdır. Uygulamanızı birden fazla veya iki eşzamanlı oturum kullanacak şekilde ya da bunları hızla oluşturup atacak şekilde tasarlamadan önce dikkatli düşünün ve I2P geliştiricilerine danışın. Bittorrent istemcileri her bağlantı için benzersiz bir oturum oluşturmamalıdır. İstemcinizi duyurular ve istemci bağlantıları için aynı oturumu kullanacak şekilde tasarlayın.

Ayrıca, istemci ayarlarınızın (ve kullanıcılara router ayarları hakkında verdiğiniz rehberlik veya router paketliyorsanız router varsayılan ayarlarının) kullanıcılarınızın ağdan tükettiklerinden daha fazla kaynak katkıda bulunmalarını sağlayacağından emin olun. I2P eşler arası bir ağdır ve popüler bir uygulama ağı kalıcı tıkanıklığa sürüklerse ağ hayatta kalamaz.

I2P outproxy üzerinden clearnet'e bittorrent desteği sağlamayın çünkü muhtemelen engellenecektir. Rehberlik için outproxy operatörleriyle görüşün.

Java I2P ve i2pd router uygulamaları bağımsızdır ve davranış, özellik desteği ve varsayılan ayımlarda küçük farklılıklar bulunmaktadır. Lütfen uygulamanızı her iki router'ın da en son sürümü ile test edin.

i2pd SAM varsayılan olarak etkindir; Java I2P SAM ise değildir. Kullanıcılarınıza Java I2P'de SAM'ı nasıl etkinleştirecekleri konusunda talimatlar sağlayın (router konsolunda /configclients üzerinden), ve/veya ilk bağlantı başarısız olursa kullanıcıya iyi bir hata mesajı sunun, örneğin "I2P'nin çalıştığından ve SAM arayüzünün etkinleştirildiğinden emin olun".

Java I2P ve i2pd router'larının tunnel miktarları için farklı varsayılan değerleri vardır. Java varsayılanı 2, i2pd varsayılanı ise 5'tir. Düşük-orta bant genişliği ve düşük-orta bağlantı sayıları için 3 yeterlidir. Java I2P ve i2pd router'larıyla tutarlı performans elde etmek için lütfen SESSION CREATE mesajında tunnel miktarını belirtin.

I2P birden fazla imza ve şifreleme türünü destekler. Uyumluluk için I2P, eski ve verimsiz türleri varsayılan olarak kullanır, bu nedenle tüm istemciler daha yeni türleri belirtmelidir.

SAM kullanılırken, imza türü DEST GENERATE ve SESSION CREATE (geçici için) komutlarında belirtilir. Tüm istemciler SIGNATURE_TYPE=7 (Ed25519) ayarlamalıdır.

Şifreleme türü SAM SESSION CREATE komutunda veya i2cp seçeneklerinde belirtilir. Birden fazla şifreleme türüne izin verilir. Bazı tracker'lar ECIES-X25519'u destekler, bazıları ElGamal'i destekler ve bazıları her ikisini de destekler. İstemciler her ikisine de bağlanabilmek için i2cp.leaseSetEncType=4,0 (ECIES-X25519 ve ElGamal için) ayarını yapmalıdır.

DHT desteği, aynı oturum üzerinden TCP ve UDP için SAMv3.3 PRIMARY ve SUBSESSIONS gerektirir. Bu, istemci Java ile yazılmadığı sürece istemci tarafında önemli geliştirme çabası gerektirecektir. i2pd şu anda SAMv3.3'ü desteklememektedir. libtorrent şu anda SAMv3.3'ü desteklememektedir.

DHT desteği olmadan, magnet linklerinin çalışması için bilinen açık tracker'ların yapılandırılabilir listesine otomatik olarak duyuru yapmak isteyebilirsiniz. Şu anda aktif olan açık tracker'lar hakkında bilgi için I2P kullanıcılarına danışın ve varsayılanlarınızı güncel tutun. i2p_pex uzantısını desteklemek de DHT desteğinin eksikliğini gidermeye yardımcı olacaktır.

Uygulamanızın yalnızca ihtiyacı olan kaynakları kullanmasını sağlama konusunda geliştiricilere daha fazla rehberlik için lütfen [SAMv3 spesifikasyonuna](/docs/api/samv3/) ve [I2P'yi uygulamanızla paketleme kılavuzumuza](/docs/applications/embedding/) bakın. Daha fazla yardım için I2P veya i2pd geliştiricilerine başvurun.

---

## Duyurular

İstemciler genellikle eski tracker'larla uyumluluk için duyuruda sahte bir port=6881 parametresi içerir. Tracker'lar port parametresini görmezden gelebilir ve bunu zorunlu kılmamalıdır.

ip parametresi, I2P Base 64 alfabesi [A-Z][a-z][0-9]-~ kullanarak istemcinin [Destination](/docs/specs/common-structures/#struct_Destination)'ının base 64'üdür. [Destination](/docs/specs/common-structures/#struct_Destination)'lar 387+ bayttır, dolayısıyla Base 64 516+ bayttır. İstemciler genellikle eski tracker'larla uyumluluk için Base 64 Destination'a ".i2p" ekler. Tracker'lar eklenmiş bir ".i2p" gerektirmemelidir.

Diğer parametreler standart bittorrent'teki ile aynıdır.

İstemciler için mevcut Destination'lar 387 veya daha fazla bayttır (Base 64 kodlamasında 516 veya daha fazla). Şimdilik varsayılacak makul maksimum 475 bayttır. Tracker, kompakt yanıtlar sunmak için Base64'ü çözmesi gerektiğinden (aşağıya bakın), tracker muhtemelen duyuru yapıldığında Base64'ü çözmeli ve hatalı Base64'ü reddetmelidir.

Varsayılan yanıt türü kompakt olmayan türdür. İstemciler compact=1 parametresiyle kompakt yanıt talep edebilir. Bir tracker talep edildiğinde kompakt yanıt döndürebilir, ancak bunu yapmak zorunda değildir. Not: Tüm popüler tracker'lar artık kompakt yanıtları destekler ve en az bir tanesi announce'da compact=1 gerektirir. Tüm istemciler kompakt yanıtları talep etmeli ve desteklemelidir.

Yeni I2P istemcisi geliştiricilerinin, 4444 portundaki HTTP istemci proxy'si yerine kendi tunnel'ları üzerinden duyuru yapmaları şiddetle önerilir. Bu hem daha verimlidir hem de tracker tarafından hedef zorlamasına izin verir (aşağıya bakınız).

UDP duyuruları spesifikasyonu 2025-06'da tamamlandı. Çeşitli I2P istemcileri ve tracker'larda destek 2025'in ilerleyen dönemlerinde kullanıma sunulacak. Ek bilgi için aşağıya bakın.

---

## Kompakt Olmayan Tracker Yanıtları

Not: Kullanımdan kaldırılmıştır. Popüler tüm tracker'lar artık kompakt yanıtları desteklemektedir ve en az bir tanesi announce'ta compact=1 gerektirmektedir. Tüm istemciler kompakt yanıtları talep etmeli ve desteklemelidir.

Kompakt olmayan yanıt, I2P "ip"si ile standart bittorrent'teki gibidir. Bu, muhtemelen ".i2p" son eki olan uzun bir base64 kodlu "DNS dizesi"dir.

Tracker'lar genellikle eski istemcilerle uyumluluk için sahte bir port anahtarı içerir veya duyurudan (announce) gelen portu kullanır. İstemciler port parametresini görmezden gelmelidir ve bunu gerektirmemelidir.

ip anahtarının değeri, yukarıda açıklandığı gibi istemcinin [Destination](/docs/specs/common-structures/#struct_Destination)'ının base 64 kodlamasıdır. Tracker'lar genellikle eski istemcilerle uyumluluk için, announce ip'sinde ".i2p" yoksa Base 64 Destination'a ".i2p" ekler. İstemciler yanıtlarda eklenmiş ".i2p" gerektirmemelidir.

Diğer yanıt anahtarları ve değerleri standart bittorrent'teki ile aynıdır.

---

## Kompakt Tracker Yanıtları

Kompakt yanıtta, "peers" sözlük anahtarının değeri, uzunluğu 32 baytın katı olan tek bir bayt dizisidir. Bu dize, eşlerin ikili [Destinations](/docs/specs/common-structures/#struct_Destination) yapılarının birleştirilmiş [32-baytlık SHA-256 Hash'lerini](/docs/specs/common-structures/#type_Hash) içerir. Bu hash, destination zorlaması (aşağıya bakın) kullanılmadığı sürece tracker tarafından hesaplanmalıdır; destination zorlaması kullanıldığında X-I2P-DestHash veya X-I2P-DestB32 HTTP başlıklarında teslim edilen hash ikili forma dönüştürülüp saklanabilir. Peers anahtarı mevcut olmayabilir veya peers değeri sıfır uzunlukta olabilir.

Kompakt yanıt desteği hem istemciler hem de tracker'lar için isteğe bağlı olsa da, nominal yanıt boyutunu %90'dan fazla azalttığı için şiddetle tavsiye edilir.

---

## Hedef Zorlama

Bazı I2P bittorrent istemcileri (hepsi değil) kendi tunnel'ları üzerinden duyuru yapar. Tracker'lar spoofing'i önlemek için bunu zorunlu kılmayı seçebilir ve I2PTunnel HTTP Server tunnel'ı tarafından eklenen HTTP başlıkları kullanarak istemcinin [Destination](/docs/specs/common-structures/#struct_Destination)'ını doğrulayabilir. Bu başlıklar X-I2P-DestHash, X-I2P-DestB64 ve X-I2P-DestB32'dir ve bunlar aynı bilginin farklı formatlarıdır. Bu başlıklar istemci tarafından taklit edilemez. Destination'ları zorunlu kılan bir tracker'ın ip duyuru parametresini hiç gerektirmesi gerekmez.

Birçok istemci duyurular için kendi tunnel'ı yerine HTTP proxy kullandığından, hedef zorlama bu istemcilerin kullanımını engelleyecektir, ta ki bu istemciler kendi tunnel'ları üzerinden duyuru yapacak şekilde dönüştürülene kadar.

Ne yazık ki, ağ büyüdükçe kötü niyetli davranışların miktarı da artacaktır, bu nedenle sonunda tüm tracker'ların destination'ları zorunlu kılacağını bekliyoruz. Hem tracker hem de istemci geliştiricileri bunu öngörmelidir.

---

## Host Adlarını Duyur

Torrent dosyalarındaki duyuru URL ana bilgisayar adları genellikle [I2P adlandırma standartlarını](/docs/overview/naming/) takip eder. Adres defterlerinden gelen ana bilgisayar adları ve ".b32.i2p" Base 32 ana bilgisayar adlarına ek olarak, tam Base 64 Destination (".i2p" eklenmiş veya eklenmemiş) desteklenmelidir. Açık olmayan tracker'lar kendi ana bilgisayar adlarını bu formatların herhangi birinde tanıyabilmelidir.

Anonimliği korumak için, istemciler genellikle torrent dosyalarındaki I2P olmayan duyuru URL'lerini görmezden gelmelidir.

---

## İstemci Bağlantıları

İstemciden istemciye bağlantılar TCP üzerinden standart protokol kullanır. Şu anda uTP iletişimini destekleyen bilinen I2P istemcisi yoktur.

I2P, yukarıda açıklandığı gibi adresler için 387+ baytlık [Destinations](/docs/specs/common-structures/#struct_Destination) kullanır.

İstemci yalnızca hedefin hash'ine sahipse (kompakt yanıt veya PEX'ten gelen gibi), bunu Base 32 ile kodlayarak, ".b32.i2p" ekleyerek ve Adlandırma Servisini sorgulayarak bir arama gerçekleştirmelidir; servis mevcut ise tam Destination'ı döndürecektir.

İstemci, kompakt olmayan bir yanıtta aldığı bir eşin tam Destination bilgisine sahipse, bunu bağlantı kurulumunda doğrudan kullanmalıdır. Bir Destination'ı arama için tekrar Base 32 hash'ine dönüştürmeyin, bu oldukça verimsizdir.

---

## Çapraz Ağ Koruması

Anonimliği korumak için, I2P bittorrent istemcileri genellikle I2P olmayan duyuruları veya eş bağlantılarını desteklemez. I2P HTTP outproxy'leri genellikle duyuruları engeller. Bittorrent trafiğini destekleyen bilinen SOCKS outproxy'leri yoktur.

HTTP inproxy üzerinden I2P olmayan istemcilerin kullanımını önlemek için, I2P tracker'ları genellikle X-Forwarded-For HTTP başlığı içeren erişimleri veya duyuruları engeller. Tracker'lar IPv4 veya IPv6 IP'li standart ağ duyurularını reddetmeli ve bunları yanıtlarda sunmamalıdır.

---

## PEX

I2P PEX, ut_pex'e dayanmaktadır. ut_pex'in resmi bir spesifikasyonu mevcut görünmediğinden, yardım için libtorrent kaynak kodunu incelemek gerekli olabilir. Bu, [uzantı el sıkışması](http://www.bittorrent.org/beps/bep_0010.html)'nda "i2p_pex" olarak tanımlanan bir uzantı mesajıdır. En fazla 3 anahtar içeren bencode edilmiş bir sözlük içerir: "added", "added.f" ve "dropped". added ve dropped değerleri her biri tek bir bayt dizisidir ve uzunluğu 32 baytın katıdır. Bu bayt dizeleri, eşlerin ikili [Destinations](/docs/specs/common-structures/#struct_Destination) değerlerinin birleştirilmiş SHA-256 Hash'leridir. Bu, yukarıda belirtilen i2p kompakt yanıt formatındaki peers sözlük değeri ile aynı formattır. added.f değeri, eğer mevcutsa, ut_pex'teki ile aynıdır.

---

## DHT

DHT desteği, 0.9.2 sürümünden itibaren i2psnark istemcisine dahil edilmiştir. [BEP 5](http://www.bittorrent.org/beps/bep_0005.html)'ten ön farklılıklar aşağıda açıklanmıştır ve değişikliğe tabidir. DHT destekleyen bir istemci geliştirmek istiyorsanız I2P geliştiricileriyle iletişime geçin.

Standart DHT'den farklı olarak, I2P DHT seçenekler el sıkışmasında veya PORT mesajında bir bit kullanmaz. [Uzantı el sıkışmasında](http://www.bittorrent.org/beps/bep_0010.html) "i2p_dht" olarak tanımlanan bir uzantı mesajıyla duyurulur. İkisi de tamsayı olan "port" ve "rport" olmak üzere iki anahtarlı bencoded bir sözlük içerir.

Kompakt düğüm bilgisinde listelenen UDP (datagram) portu, yanıtlanabilir (imzalanmış) datagramları almak için kullanılır. Bu, duyurular dışındaki sorgular için kullanılır. Buna "sorgu portu" diyoruz. Bu, uzantı mesajındaki "port" değeridir. Sorgular [I2CP](/docs/specs/i2cp/) protokol numarası 17'yi kullanır.

Bu UDP portuna ek olarak, sorgu portu + 1'e eşit ikinci bir datagram portu kullanırız. Bu port, yanıtlar, hatalar ve duyurular için imzasız (ham) datagramları almak için kullanılır. Bu port, yanıtların sorguda gönderilen token'ları içermesi ve imzalanmasına gerek olmaması nedeniyle artan verimlilik sağlar. Buna "yanıt portu" diyoruz. Bu, uzantı mesajından gelen "rport" değeridir. Sorgu portu + 1 olmalıdır. Yanıtlar ve duyurular [I2CP](/docs/specs/i2cp/) protokol numarası 18'i kullanır.

Kompakt peer bilgisi, 4 bayt IP + 2 bayt port yerine 32 bayttır (32 bayt SHA256 Hash). Peer portu yoktur. Bir yanıtta, "values" anahtarı her biri tek bir kompakt peer bilgisi içeren string listesidir.

Kompakt düğüm bilgisi, 20 bayt Node ID + 4 bayt IP + 2 bayt port yerine 54 bayttır (20 bayt Node ID + 32 bayt SHA256 Hash + 2 bayt port). Bir yanıtta, "nodes" anahtarı birleştirilmiş kompakt düğüm bilgisini içeren tek bir bayt dizisidir.

Güvenli düğüm kimliği gereksinimi: Çeşitli DHT saldırılarını zorlaştırmak için, Düğüm Kimliği'nin ilk 4 baytı hedef Hash'in ilk 4 baytı ile eşleşmeli ve Düğüm Kimliği'nin sonraki iki baytı, hedef hash'in sonraki iki baytının port ile özel VEYA işlemine tabi tutulmuş hali ile eşleşmelidir.

Bir torrent dosyasında, trackersız torrent sözlüğünün "nodes" anahtarı henüz belirlenmemiştir (TBD). Bu, bir host string'i ve port integer'ı içeren listelerin listesi yerine 32 byte'lık binary string'lerin (SHA256 Hash'leri) bir listesi olabilir. Alternatifler: Birleştirilmiş hash'ler içeren tek bir byte string'i veya yalnızca string'lerin bir listesi.

---

## Datagram (UDP) İzleyiciler

I2P'de UDP duyurularının spesifikasyonu 2025-06'da tamamlandı. Çeşitli I2P istemcileri ve tracker'larda destek 2025'in ilerleyen dönemlerinde kullanıma sunulacak. [BEP 15](http://www.bittorrent.org/beps/bep_0015.html)'ten farkları [UDP duyuru spesifikasyonunda](/docs/specs/udp-announces/) belgelenmiştir. Spesifikasyon ayrıca [yeni Datagram 2/3 formatları](/docs/specs/datagrams/) için destek gerektirir.

---

## Ek Bilgiler

İzin verilen hızlı seti hesaplamak için ön bir belirtim [Teklif 172](/proposals/172-bep6-allowed-fast) adresindedir

---

## Ek Bilgi

- I2P bittorrent standartları genellikle [zzz.i2p](http://zzz.i2p/) üzerinde tartışılır.
- Mevcut tracker yazılımı yeteneklerinin bir tablosu [orada da mevcuttur](http://zzz.i2p/files/trackers.html).
- [I2P bittorrent SSS](http://forum.i2p/viewtopic.php?t=2068)
- [I2P üzerinde DHT tartışması](http://zzz.i2p/topics/812)
