---
title: "İsimlendirme Tartışması"
description: "I2P'nin isimlendirme modeli hakkındaki tarihsel tartışma ve küresel DNS tarzı şemaların neden reddedildiği"
slug: "naming"
aliases:
  - "/tr/docs/legacy/naming"
  - "/tr/docs/legacy/naming/"
  - "/tr/naming_discussion"
  - "/tr/naming_discussion/"
lastUpdated: "2025-02"
accurateFor: "historical"
---

NOT: Aşağıdaki, I2P adlandırma sisteminin arkasındaki nedenler, yaygın argümanlar ve olası alternatiflerin tartışmasıdır. Güncel dokümantasyon için [adlandırma sayfasına](/docs/naming) bakın.

## Reddedilen Alternatifler

I2P içinde adlandırma, olasılıkların spektrumu boyunca savunucularla birlikte en başından beri sıkça tartışılan bir konu olmuştur. Ancak, I2P'nin güvenli iletişim ve merkezi olmayan işletim için doğasında bulunan talebi göz önüne alındığında, geleneksel DNS tarzı adlandırma sistemi açıkça dışarıda kalır, "çoğunluk kuralları" oylama sistemleri de öyle.

I2P, DNS benzeri hizmetlerin kullanımını teşvik etmez çünkü bir sitenin ele geçirilmesiyle verilen zarar muazzam olabilir - ve güvensiz destinationlar hiçbir değere sahip değildir. DNSsec'in kendisi hala kayıt şirketlerine ve sertifika otoritelerine geri dönerken, I2P ile bir destination'a gönderilen istekler ele geçirilemez veya yanıt taklit edilemez çünkü bunlar destination'ın açık anahtarlarıyla şifrelenir ve bir destination'ın kendisi sadece bir çift açık anahtar ve bir sertifikadır. Öte yandan DNS tarzı sistemler, arama yolundaki ad sunucularından herhangi birinin basit hizmet engelleme ve taklit saldırıları düzenlemesine izin verir. Yanıtları merkezi bir sertifika otoritesi tarafından imzalandığını doğrulayan bir sertifika eklemek, düşman ad sunucusu sorunlarının çoğunu ele alacaktır ancak yeniden oynatma saldırılarının yanı sıra düşman sertifika otoritesi saldırılarına da açık bırakacaktır.

Oylama tarzı isimlendirme de tehlikelidir, özellikle anonim sistemlerde Sybil saldırılarının etkinliği göz önüne alındığında - saldırgan keyfi olarak yüksek sayıda eş oluşturabilir ve belirli bir ismi ele geçirmek için her biriyle "oy" kullanabilir. Kimliği ücretsiz olmaktan çıkarmak için proof-of-work yöntemleri kullanılabilir, ancak ağ büyüdükçe çevrimiçi oylama yürütmek için herkesle iletişim kurmak için gereken yük uygulanamaz hale gelir, ya da tam ağ sorgulanmazsa farklı yanıt kümeleri erişilebilir olabilir.

Ancak Internet'te olduğu gibi, I2P de bir isimlendirme sisteminin tasarımını ve işleyişini (IP benzeri) iletişim katmanının dışında tutuyor. Paketlenmiş isimlendirme kütüphanesi, [alternatif isimlendirme sistemlerinin](#alternatives) bağlanabileceği basit bir servis sağlayıcı arayüzü içerir ve son kullanıcıların tercih ettikleri isimlendirme ödünleşimlerini yönlendirmelerine olanak tanır.

## Tartışma

Ayrıca bkz. [Names: Decentralized, Secure, Human-Meaningful: Choose Two](https://zooko.com/distnames.html).

### jrandom'dan yorumlar

(eski Syndie'deki bir gönderiden uyarlanmıştır, 26 Kasım 2005)

S: Bazı host'lar tek bir adres üzerinde anlaşamıyorsa ve bazı adresler çalışıyor, diğerleri çalışmıyorsa ne yapmalı? Bir ismin doğru kaynağı kimdir?

C: Yapamazsınız. Bu aslında I2P'deki isimler ile DNS'in nasıl çalıştığı arasındaki kritik bir farktır - I2P'deki isimler insan tarafından okunabilir, güvenli ancak **global olarak benzersiz değildir**. Bu tasarım gereği böyledir ve güvenlik ihtiyacımızın doğal bir parçasıdır.

Eğer bir şekilde sizi bir isimle ilişkili hedefi değiştirmeye ikna edebilseydim, siteyi başarılı bir şekilde "ele geçirmiş" olurdum ve hiçbir koşulda bu kabul edilebilir değildir. Bunun yerine yaptığımız şey isimleri **yerel olarak benzersiz** hale getirmektir: bunlar bir siteyi çağırmak için *sizin* kullandığınız şeylerdir, tıpkı tarayıcınızın yer imlerine veya IM istemcinizin arkadaş listesine bir şeyler eklediğinizde onları istediğiniz gibi çağırabilmeniz gibi. Sizin "Patron" dediğiniz kişi başka birinin "Sally" dediği kişi olabilir.

İsimler asla güvenli bir şekilde insan tarafından okunabilir ve küresel olarak benzersiz olmayacaktır.

### zzz tarafından yorumlar

Aşağıdaki zzz'den gelen metin, I2P'nin isimlendirme sistemi hakkındaki yaygın şikayetlerin bir incelemesidir.

- **Verimsizlik:** Tüm hosts.txt dosyası indirilir (eğer değiştiyse, çünkü eepget etag ve last-modified başlıklarını kullanır). Şu anda yaklaşık 800 host için yaklaşık 400K boyutunda.

Doğru, ancak bu I2P bağlamında çok fazla trafik değil, zaten I2P'nin kendisi son derece verimsiz (floodfill veritabanları, büyük şifreleme ek yükü ve dolgu, garlic routing, vb.). Eğer birinden her 12 saatte bir hosts.txt dosyası indirirseniz, ortalama olarak yaklaşık 10 bayt/saniye eder.

I2P'de genellikle olduğu gibi, burada da anonimlik ve verimlilik arasında temel bir ödünleşim vardır. Bazıları etag ve last-modified başlıklarını kullanmanın tehlikeli olduğunu söyler çünkü verileri en son ne zaman talep ettiğinizi açığa çıkarır. Diğerleri ise yalnızca belirli anahtarları talep etmeyi önermiştir (jump servislerinin yaptığına benzer, ancak daha otomatik bir şekilde), muhtemelen anonimlikte daha fazla kayıp pahasına.

Olası iyileştirmeler address book'un (adres defterinin) değiştirilmesi veya tamamlanması (i2host.i2p'ye bakın), ya da http://example.i2p/hosts.txt yerine http://example.i2p/cgi-bin/recenthosts.cgi'ye abone olmak gibi basit bir şey olabilir. Varsayımsal bir recenthosts.cgi'nin örneğin son 24 saatteki tüm host'ları dağıttığını düşünürsek, bu mevcut last-modified ve etag ile hosts.txt'den hem daha verimli hem de daha anonim olabilir.

Örnek bir uygulama stats.i2p adresinde http://stats.i2p/cgi-bin/newhosts.txt konumunda bulunmaktadır. Bu betik, zaman damgası içeren bir Etag döndürür. If-None-Match etag ile bir istek geldiğinde, betik YALNIZCA o zaman damgasından sonraki yeni host'ları döndürür, eğer hiçbiri yoksa 304 Not Modified yanıtı verir. Bu şekilde betik, abonenin bilmediği host'ları adres defteri ile uyumlu bir şekilde verimli olarak döndürür.

Bu nedenle verimsizlik büyük bir sorun değildir ve köklü değişiklik yapmadan durumu iyileştirmenin birkaç yolu vardır.

- **Ölçeklenebilir Değil:** 400K hosts.txt (doğrusal arama ile) şu anda o kadar büyük değil ve muhtemelen sorun olmadan 10 kat veya 100 kat büyüyebilir.

Ağ trafiği açısından yukarıdaki açıklamaya bakın. Ancak bir anahtar için ağ üzerinden yavaş gerçek zamanlı sorgu yapmayacaksanız, tüm anahtar setini yerel olarak saklamanız gerekir ve bu anahtar başına yaklaşık 500 byte maliyetle gelir.

- **Yapılandırma ve "güven" gerektirir:** Hazır adres defteri yalnızca nadiren güncellenen http://www.i2p2.i2p/hosts.txt adresine abone olduğundan, yeni kullanıcılar için kötü bir deneyim yaratır.

Bu çok kasıtlı bir durumdur. jrandom, kullanıcının bir hosts.txt sağlayıcısına "güvenmesini" istiyor ve sevdiği bir deyişle "güven bir boolean değildir". Yapılandırma adımı, kullanıcıları anonim bir ağda güven konularını düşünmeye zorlamaya çalışır.

Başka bir örnek olarak, HTTP Proxy'deki "I2P Site Unknown" hata sayfası bazı atlama servislerini listeler, ancak herhangi birini özel olarak "tavsiye etmez" ve hangisini seçeceği (veya seçmeyeceği) kullanıcıya bağlıdır. jrandom'ın söyleyeceği gibi, listelenen sağlayıcılara onları listeleyecek kadar güveniriz ancak otomatik olarak onlardan anahtarı almaya yetecek kadar güvenmeyiz.

Bunun ne kadar başarılı olduğundan emin değilim. Ancak isimlendirme sistemi için bir tür güven hiyerarşisi olmalı. Herkesi eşit şekilde ele almak, ele geçirme riskini artırabilir.

- **DNS değildir**

Ne yazık ki I2P üzerinden gerçek zamanlı aramalar web taramayı önemli ölçüde yavaşlatacaktır.

Ayrıca, DNS sınırlı önbellekleme ve yaşam süresi ile aramalar üzerine kuruludur, I2P anahtarları ise kalıcıdır.

Tabii ki çalıştırabiliriz ama neden? Uygun bir seçenek değil.

- **Güvenilir değil:** Adres defteri abonelikleri için belirli sunuculara bağımlıdır.

Evet, yapılandırdığınız birkaç sunucuya bağlıdır. I2P içinde sunucular ve hizmetler gelir ve gider. Diğer herhangi bir merkezi sistem (örneğin DNS kök sunucuları) de aynı sorunu yaşar. Tamamen merkezi olmayan bir sistem (herkesin yetkili olduğu) "herkes bir kök DNS sunucusudur" çözümü uygulayarak veya hosts.txt dosyanızdaki herkesi adres defterinize ekleyen bir betik gibi daha da basit bir şeyle mümkündür.

Ancak, tamamen yetkili çözümleri savunan insanlar genellikle çakışma ve ele geçirme sorunlarını tam olarak düşünmemişlerdir.

- **Garip, gerçek zamanlı değil:** hosts.txt sağlayıcıları, anahtar ekleme web formu sağlayıcıları, jump servis sağlayıcıları, I2P Site durum raporlayıcıları gibi bir yama işidir. Jump sunucuları ve abonelikler baş belasıdır, DNS gibi çalışması gerekir.

Güvenilirlik ve güven bölümlerine bakın.

Özetle, mevcut sistem korkunç derecede bozuk, verimsiz veya ölçeklenemeyen bir durumda değil ve "sadece DNS kullanın" önerileri iyi düşünülmüş değil.

## Alternatifler

I2P kaynak kodu birkaç takılabilir isimlendirme sistemi içerir ve isimlendirme sistemleriyle deneyim yapılabilmesi için yapılandırma seçeneklerini destekler.

- **Meta** - sırayla iki veya daha fazla başka adlandırma sistemini çağırır. Varsayılan olarak, önce PetName sonra HostsTxt'yi çağırır.
- **PetName** - petnames.txt dosyasında arama yapar. Bu dosya formatı hosts.txt ile aynı DEĞİLDİR.
- **HostsTxt** - aşağıdaki dosyalarda sırayla arama yapar:
  1. privatehosts.txt
  2. userhosts.txt
  3. hosts.txt
- **AddressDB** - Her host, addressDb/ dizininde ayrı bir dosyada listelenir.
- **Eepget** - harici bir sunucudan HTTP arama isteği yapar - Meta ile HostsTxt aramasından sonra yığınlanmalıdır. Bu, atlama sistemini genişletebilir veya değiştirebilir. Bellek içi önbellekleme içerir.
- **Exec** - arama için harici bir program çağırır, java'dan bağımsız olarak arama şemalarında ek deneyimlere izin verir. HostsTxt'den sonra veya tek adlandırma sistemi olarak kullanılabilir. Bellek içi önbellekleme içerir.
- **Dummy** - Base64 adları için yedek olarak kullanılır, aksi takdirde başarısız olur.

Mevcut adlandırma sistemi, gelişmiş yapılandırma seçeneği `i2p.naming.impl` ile değiştirilebilir (yeniden başlatma gereklidir). Ayrıntılar için `core/java/src/net/i2p/client/naming` klasörüne bakın.

Herhangi bir yeni sistem HostsTxt ile yığılmalı veya yerel depolama ve/veya adres defteri abonelik işlevlerini uygulamalıdır, çünkü adres defteri yalnızca hosts.txt dosyalarını ve formatını bilir.

## Sertifikalar

I2P hedefleri bir sertifika içerir, ancak şu anda bu sertifika her zaman null'dır. Null sertifika ile base64 hedefler her zaman "AAAA" ile biten 516 bayt uzunluğundadır ve bu durum adres defteri birleştirme mekanizmasında ve muhtemelen diğer yerlerde kontrol edilir. Ayrıca, bir sertifika oluşturmak veya onu bir hedefe eklemek için kullanılabilir bir yöntem yoktur. Bu nedenle sertifikaları uygulamak için bunların güncellenmesi gerekecektir.

Sertifikaların olası kullanımlarından biri [proof of work](/get-involved/todo#hashcash) içindir.

Bir diğeri, "alt alanların" (tırnak içinde çünkü gerçekte böyle bir şey yok, I2P düz bir isimlendirme sistemi kullanır) 2. seviye alanın anahtarları tarafından imzalanmasıdır.

Herhangi bir sertifika uygulamasıyla birlikte sertifikaları doğrulama yöntemi de gelmelidir. Muhtemelen bu adres defteri birleştirme kodunda gerçekleşir. Birden fazla sertifika türü veya birden fazla sertifika için bir yöntem var mı?

Yanıtları merkezi bir sertifika otoritesi tarafından imzalandığı şeklinde doğrulayan bir sertifika eklemek, düşmanca nameserver sorunlarının çoğunu çözerdi ancak replay saldırıları ve düşmanca sertifika otoritesi saldırılarına açık bırakırdı.
