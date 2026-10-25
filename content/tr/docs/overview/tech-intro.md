---
title: "I2P: Teknik Giriş"
description: "I2P mimarisi ve işleyişine teknik giriş"
slug: "tech-intro"
aliases:
  - "/tr/techintro"
  - "/tr/techintro/"
lastUpdated: "2025-01"
accurateFor: "0.9.65"
---

NOT: Bu belge orijinal olarak 2003 yılında jrandom tarafından yazılmıştır. Güncel tutmaya çalışsak da, bazı bilgiler eskimiş veya eksik olabilir. Taşıma ve kriptografi bölümleri 2025-01 itibariyle günceldir.

## Giriş

I2P, ölçeklenebilir, kendi kendini organize eden, dayanıklı paket anahtarlamalı anonim bir ağ katmanıdır ve bu katman üzerinde anonimlik veya güvenlik odaklı herhangi bir sayıda farklı uygulama çalışabilir. Bu uygulamaların her biri, özgür rota mixnet'inin doğru uygulanması konusunda endişelenmeden kendi anonimlik, gecikme ve verim dengelerini kurabilir ve böylece faaliyetlerini I2P üzerinde zaten çalışan daha geniş kullanıcı anonimlik kümesiyle harmanlamalarına olanak tanır.

Halihazırda mevcut uygulamalar, tipik İnternet etkinliklerinin tüm yelpazesini sağlamaktadır — **anonim** web gezintisi, web barındırma, sohbet, dosya paylaşımı, e-posta, blog yazımı ve içerik dağıtımı ile birlikte geliştirilmekte olan diğer çeşitli uygulamalar.

- Web tarayıcısı kullanımı: proxy kullanımını destekleyen herhangi bir mevcut tarayıcı kullanarak.
- Sohbet: IRC ve diğer protokoller
- Dosya paylaşımı: [I2PSnark](#i2psnark) ve diğer uygulamalar
- E-posta: [susimail](#i2pmail--susimail) ve diğer uygulamalar
- Blog: herhangi bir yerel web sunucusu veya mevcut eklentiler kullanarak

[Freenet](#freenet) veya [GNUnet](https://www.gnunet.org/en/) gibi içerik dağıtım ağlarında barındırılan web sitelerinin aksine, I2P üzerinde barındırılan hizmetler tamamen etkileşimlidir — geleneksel web tarzı arama motorları, bülten panoları, yorum yapabileceğiniz bloglar, veritabanı destekli siteler ve Freenet gibi statik sistemleri yerel olarak yüklemeden sorgulayabileceğiniz köprüler bulunmaktadır.

Tüm bu anonimlik etkinleştirilmiş uygulamalarla birlikte, I2P mesaj odaklı ara katman yazılımının rolünü üstlenir — uygulamalar bir kriptografik tanımlayıcıya (bir "destination") veri göndermek istediklerini söyler ve I2P bunun güvenli ve anonim bir şekilde ulaştırılmasını sağlar. I2P ayrıca I2P'nin anonim en iyi çaba mesajlarının güvenilir, sıralı akışlar olarak aktarılmasına izin vermek için basit bir [streaming](#streaming-library) kütüphanesi de içerir ve ağın yüksek bant genişliği gecikme çarpımı için ayarlanmış TCP tabanlı bir tıkanıklık kontrolü algoritmasını şeffaf bir şekilde sunar. Mevcut uygulamaları ağa bağlamak için birkaç basit SOCKS proxy mevcut olsa da, bunların değeri sınırlı kalmıştır çünkü neredeyse her uygulama rutin olarak anonim bağlamda hassas bilgi olan şeyleri açığa çıkarır. Gidilecek tek güvenli yol, bir uygulamayı uygun çalışmasını sağlamak için tam olarak denetlemektir ve buna yardımcı olmak için ağdan en iyi şekilde yararlanmak amacıyla kullanılabilecek çeşitli dillerde bir dizi API sağlarız.

I2P bir araştırma projesi değildir — akademik, ticari veya devlet destekli — bunun yerine ihtiyacı olanlara yeterli düzeyde anonimlik sağlamak için gerekli olan her şeyi yapmayı amaçlayan bir mühendislik çabasıdır. 2003'ün başlarından beri bir tam zamanlı geliştirici ve dünyanın her yerinden özel bir yarı zamanlı katkıda bulunanlar grubu ile aktif geliştirilmektedir. I2P üzerinde yapılan tüm çalışmalar açık kaynak kodludur ve [web sitesinde](/) ücretsiz olarak mevcuttur; kodun çoğunluğu doğrudan kamu alanına yayımlanmış olmasına rağmen, BSD tarzı lisanslar altında birkaç kriptografik rutinden yararlanılmaktadır. I2P üzerinde çalışan kişiler, insanların hangi lisans altında istemci uygulamaları yayımladığını kontrol etmezler ve mevcut birkaç GPL lisanslı uygulama bulunmaktadır ([I2PTunnel](#i2ptunnel), [susimail](#i2pmail--susimail), [I2PSnark](#i2psnark), I2P-Bote, I2Phex ve diğerleri). I2P için finansman tamamen bağışlardan gelmektedir ve şu anda herhangi bir yargı bölgesinde vergi muafiyeti almamaktadır, çünkü geliştiricilerin çoğu kendileri anonimdir.

---

## İşlem

### Genel Bakış

I2P'nin işleyişini anlamak için birkaç temel kavramı anlamak gereklidir. İlk olarak, I2P ağa katılan yazılım (bir "router") ile bireysel uygulamalarla ilişkili anonim uç noktalar ("destinations") arasında katı bir ayrım yapar. Birinin I2P çalıştırıyor olması genellikle bir sır değildir. Gizlenen şey, kullanıcının ne yaptığına dair bilgiler (eğer bir şey yapıyorsa) ve belirli bir destination'ın hangi router'a bağlı olduğudur. Son kullanıcılar genellikle router'larında birkaç yerel destination'a sahip olacaklardır — örneğin, biri IRC sunucularına proxy yapan, diğeri kullanıcının anonim web sunucusunu ("I2P Site") destekleyen, bir diğeri I2Phex örneği için, bir diğeri torrent'lar için, vb.

Anlaşılması gereken bir diğer kritik kavram da "tunnel"dır. Bir tunnel, açıkça seçilmiş bir router listesi boyunca yönlendirilmiş bir yoldur. Katmanlı şifreleme kullanılır, böylece router'ların her biri yalnızca tek bir katmanın şifresini çözebilir. Şifresi çözülmüş bilgi, iletilecek şifrelenmiş bilgiyle birlikte bir sonraki router'ın IP'sini içerir. Her tunnel'ın bir başlangıç noktası ("gateway" olarak da bilinen ilk router) ve bir bitiş noktası vardır. Mesajlar yalnızca tek yönde gönderilebilir. Mesajları geri göndermek için başka bir tunnel gereklidir.

![Gelen ve giden tunnel şeması](/images/tunnels.svg) *Şekil 1: İki tür tunnel vardır: gelen ve giden.*

İki tür tunnel mevcuttur: **"outbound" tunnel**lar mesajları tunnel yaratıcısından uzağa gönderirken, **"inbound" tunnel**lar mesajları tunnel yaratıcısına getirir. Bu iki tunnel'ı birleştirmek kullanıcıların birbirlerine mesaj göndermesine olanak tanır. Gönderici (yukarıdaki resimde "Alice") bir outbound tunnel kurarken, alıcı (yukarıdaki resimde "Bob") bir inbound tunnel oluşturur. Bir inbound tunnel'ın gateway'i herhangi bir kullanıcıdan mesaj alabilir ve bunları endpoint'e ("Bob") kadar iletir. Outbound tunnel'ın endpoint'i mesajı inbound tunnel'ın gateway'ine göndermek zorundadır. Bunu yapmak için gönderici ("Alice") şifrelenmiş mesajına talimatlar ekler. Outbound tunnel'ın endpoint'i mesajı çözdüğünde, mesajı doğru inbound gateway'e ("Bob"a giden gateway) iletme talimatlarına sahip olacaktır.

Anlaşılması gereken üçüncü kritik kavram, I2P'nin **"network database"** (veya "netDb") sistemidir — ağ meta verilerini paylaşmak için kullanılan bir algoritma çifti. Taşınan iki tür meta veri **"routerInfo"** ve **"leaseSets"** şeklindedir — routerInfo, router'lara belirli bir router ile iletişim kurmak için gerekli verileri (genel anahtarları, aktarım adresleri vb.) verirken, leaseSet router'lara belirli bir hedefe ulaşmak için gerekli bilgileri verir. Bir leaseSet, bir dizi "lease" içerir. Bu lease'lerin her biri, belirli bir hedefe ulaşmayı sağlayan bir tünel geçidi belirtir. Bir lease'de bulunan tam bilgiler:

- Belirli bir hedefe ulaşmayı sağlayan bir tunnel için gelen ağ geçidi.
- Bir tunnel'ın sona erdiği zaman.
- Mesajları şifreleyebilmek için genel anahtar çifti (tunnel üzerinden göndermek ve hedefe ulaşmak için).

Router'lar kendileri routerInfo'larını doğrudan netDb'ye gönderirken, leaseSet'ler outbound tunnel'lar aracılığıyla gönderilir (leaseSet'lerin anonim olarak gönderilmesi gerekir, böylece bir router'ın leaseSet'leriyle ilişkilendirilmesi önlenir).

Yukarıdaki kavramları birleştirerek ağda başarılı bağlantılar kurabiliriz.

Kendi gelen ve giden tunnel'larını oluşturmak için Alice, routerInfo toplamak amacıyla netDb'de arama yapar. Bu şekilde tunnel'larında atlama noktası (hop) olarak kullanabileceği eş listelerini toplar. Daha sonra ilk atlama noktasına bir yapı mesajı gönderebilir, tunnel'ın inşasını talep edebilir ve o router'dan tunnel inşa edilene kadar yapı mesajını ileriye göndermesini isteyebilir.

![Diğer router'lar hakkında bilgi talep et](/images/netdb_get_routerinfo_1.svg)

![Router bilgileri kullanarak tünel oluşturma](/images/netdb_get_routerinfo_2.svg) *Şekil 2: Router bilgileri tunnel oluşturmak için kullanılır.*

Alice, Bob'a bir mesaj göndermek istediğinde, önce Bob'un leaseSet'ini bulmak için netDb'de bir arama yapar ve böylece onun mevcut gelen tunnel geçitlerini öğrenir. Daha sonra kendi giden tunnel'larından birini seçer ve mesajı, giden tunnel'ın uç noktasına Bob'un gelen tunnel geçitlerinden birine iletmesi talimatıyla birlikte o tunnel'dan gönderir. Giden tunnel uç noktası bu talimatları aldığında, mesajı talep edildiği gibi iletir ve Bob'un gelen tunnel geçidi mesajı aldığında, bu mesaj tunnel boyunca Bob'un router'ına iletilir. Alice, Bob'un mesajı yanıtlayabilmesini istiyorsa, kendi hedefini açıkça mesajın kendisinin bir parçası olarak iletmesi gerekir. Bu, [streaming](#streaming-library) kütüphanesinde yapıldığı gibi daha üst seviyeli bir katman eklenerek gerçekleştirilebilir. Alice ayrıca, Bob'un yanıt vermek istediğinde netDb araması yapmasına gerek kalmaması için en güncel LeaseSet'ini mesajla birlikte paketleyerek yanıt süresini kısaltabilir, ancak bu isteğe bağlıdır.

![LeaseSet'leri kullanarak tünelleri bağlama](/images/netdb_get_leaseset.svg) *Şekil 3: LeaseSet'ler giden ve gelen tünelleri bağlamak için kullanılır.*

Tunnel'ların kendileri ağ içindeki eşlere yetkisiz açıklamayı önlemek için katmanlı şifrelemeye sahip olsa da (aktarım katmanının kendisi de ağ dışındaki eşlere yetkisiz açıklamayı önlemek için yaptığı gibi), mesajı giden tunnel uç noktasından ve gelen tunnel ağ geçidinden gizlemek için ek bir uçtan uca şifreleme katmanı eklemek gereklidir. Bu "[garlic encryption](#garlic-messages)" Alice'in router'ının birden fazla mesajı tek bir "garlic message" içinde paketlemesine izin verir, belirli bir genel anahtarla şifrelenir böylece aracı eşler ne garlic içinde kaç mesaj olduğunu, ne bu mesajların ne dediğini, ne de bu bireysel karanfillerin nereye gönderildiğini belirleyemez. Alice ve Bob arasındaki tipik uçtan uca iletişim için, garlic Bob'un leaseSet'inde yayınlanan genel anahtarla şifrelenir, bu da Bob'un kendi router'ının genel anahtarını vermeden mesajın şifrelenmesine izin verir.

Akılda tutulması gereken bir diğer önemli gerçek ise I2P'nin tamamen mesaj tabanlı olduğu ve bazı mesajların yol boyunca kaybolabileceğidir. I2P kullanan uygulamalar mesaj odaklı arayüzleri kullanabilir ve kendi tıkanıklık kontrolü ve güvenilirlik ihtiyaçlarını karşılayabilir, ancak çoğu için sağlanan [streaming](#streaming-library) kütüphanesini yeniden kullanarak I2P'yi akış tabanlı bir ağ olarak görmeleri en iyi seçenektir.

---

### Tunnel'lar

Hem gelen hem de giden tunnel'lar benzer prensipler üzerinde çalışır. Tunnel gateway'i bir dizi tunnel mesajını biriktirir ve sonunda bunları tunnel teslimi için ön işleme tabi tutar. Ardından, gateway bu ön işlenmiş veriyi şifreler ve ilk hop'a iletir. Bu peer ve sonraki tunnel katılımcıları, bir sonraki peer'a iletmeden önce bunun bir kopya olmadığını doğruladıktan sonra bir şifreleme katmanı ekler. Sonunda, mesaj endpoint'e ulaşır, burada mesajlar tekrar ayrılır ve istendiği şekilde iletilir. Fark, tunnel'ın yaratıcısının ne yaptığında ortaya çıkar — gelen tunnel'lar için yaratıcı endpoint'tir ve eklenen tüm katmanları basitçe çözer, giden tunnel'lar için ise yaratıcı gateway'dir ve tüm katmanları önceden çözer, böylece hop başına şifrelemenin tüm katmanları eklendikten sonra mesaj tunnel endpoint'ine açık metin olarak ulaşır.

Mesajları iletmek için belirli eşlerin seçimi ve bunların özel sıralaması, hem I2P'nin anonimlik hem de performans özelliklerini anlamak için önemlidir. Network database (netDb) (aşağıda) sorgulanacak eşleri seçmek ve girişleri depolamak için kendi kriterlerine sahip olsa da, tunnel yaratıcıları ağdaki herhangi bir eşi herhangi bir sırada (ve hatta tek bir tunnel'da herhangi bir sayıda) kullanabilirler. Mükemmel gecikme ve kapasite verisi küresel olarak bilinse, seçim ve sıralama istemcinin tehdit modeliyle birlikte onun özel ihtiyaçları tarafından yönlendirilirdi. Ne yazık ki, gecikme ve kapasite verisini anonim olarak toplamak önemsiz değildir ve bu bilgiyi sağlamak için güvenilmeyen eşlere bağımlı olmanın kendi ciddi anonimlik sonuçları vardır.

Anonimlik açısından, en basit teknik tüm ağdan rastgele peer'ları seçmek, onları rastgele sıralamak ve bu peer'ları sonsuza kadar bu sırada kullanmak olurdu. Performans açısından ise, en basit teknik gerekli yedek kapasiteye sahip en hızlı peer'ları seçmek, şeffaf failover'ı ele almak için yükü farklı peer'lara yaymak ve kapasite bilgisi değiştiğinde tunnel'ı yeniden inşa etmek olurdu. İlki hem kırılgan hem de verimsizken, ikincisi erişilemeyen bilgi gerektirir ve yetersiz anonimlik sunar. I2P bunun yerine, peer'ları profillerine göre organize etmek için anonimlik farkında ölçüm kodu ile birlikte bir dizi peer seçim stratejisi sunmaya çalışmaktadır.

Temel olarak, I2P etkileşimde bulunduğu eşlerle sürekli olarak profilleme yapar ve bunları dolaylı davranışlarını ölçerek gerçekleştirir — örneğin, bir eş netDb sorgulamasına 1.3 saniyede yanıt verdiğinde, bu gidiş-dönüş gecikme süresi, isteğin ve yanıtın geçtiği iki tunnel (gelen ve giden) ile ilgili tüm router'ların profillerinde ve ayrıca sorgulanan eşin profilinde kaydedilir. Ulaştırma katmanı gecikmesi veya tıkanıklık gibi doğrudan ölçümler profilin bir parçası olarak kullanılmaz, çünkü bunlar manipüle edilebilir ve ölçüm yapan router ile ilişkilendirilebilir, bu da onları önemsiz saldırılara maruz bırakır. Bu profiller toplanırken, her birinin performansını özetlemek için bir dizi hesaplama yapılır — gecikme süresi, çok fazla etkinliği işleme kapasitesi, şu anda aşırı yüklenip yüklenmediği ve ağa ne kadar iyi entegre olduğu görünüyor. Bu hesaplamalar daha sonra aktif eşler için karşılaştırılır ve router'lar dört seviyede organize edilir — hızlı ve yüksek kapasiteli, yüksek kapasiteli, başarısız olmayan ve başarısız olan. Bu seviyelerin eşikleri dinamik olarak belirlenir ve şu anda oldukça basit algoritmalar kullanılsa da alternatifler mevcuttur.

Bu profil verilerini kullanarak, en basit mantıklı eş seçim stratejisi üst katmandaki eşleri (hızlı ve yüksek kapasiteli) rastgele seçmektir ve bu strateji şu anda istemci tünelleri için uygulanmaktadır. Keşif tünelleri (netDb ve tünel yönetimi için kullanılan) eşleri "başarısız olmayan" katmandan rastgele seçer (bu katman 'daha iyi' katlardaki router'ları da içerir), böylece eşin router'ları daha geniş bir şekilde örneklemesine olanak tanır ve aslında rastgeleleştirilmiş [tepe tırmanışı](https://en.wikipedia.org/wiki/Hill_climbing) yoluyla eş seçimini optimize eder. Ancak bu stratejiler tek başına, öncül ve netDb hasat saldırıları yoluyla router'ın üst katmanındaki eşler hakkında bilgi sızdırmaktadır. Buna karşılık, yükü eşit şekilde dengelemese de, belirli düşman sınıfları tarafından gerçekleştirilen saldırılara karşı korunma sağlayan çeşitli alternatifler mevcuttur.

Rastgele bir anahtar seçerek ve eşleri bu anahtardan XOR mesafelerine göre sıralayarak, sızdırılan bilgi, eşlerin hata oranı ve katmanın değişim hızına göre predecessor ve harvesting saldırılarında azaltılır. netDb harvesting saldırılarıyla başa çıkmak için başka bir basit strateji, gelen tunnel geçitlerini sabit tutup tunnel içindeki daha ilerideki eşleri rastgele hale getirmektir. İstemcinin temas kurduğu düşmanlar için predecessor saldırılarıyla başa çıkmak amacıyla, giden tunnel uç noktaları da sabit kalacaktır. En açık noktada hangi eşin sabitleneceğinin seçimi elbette süre bakımından bir sınıra sahip olmalıdır, çünkü tüm eşler sonunda başarısız olur, bu nedenle reaktif olarak ayarlanabilir veya diğer router'ların ölçülmüş ortalama arıza süresini taklit etmek için proaktif olarak önlenebilir. Bu iki strateji birleştirilebilir, sabit bir açık eş ve tunnel'ların kendisi içinde XOR tabanlı sıralama kullanılabilir. Daha katı bir strateji, potansiyel bir tunnel'ın tam eşlerini ve sıralamasını sabitleyecek, yalnızca tümü her seferinde aynı şekilde katılmayı kabul ederse bireysel eşleri kullanacaktır. Bu, XOR tabanlı sıralamadan farklıdır çünkü her eşin predecessor ve successor'ı her zaman aynıdır, XOR ise yalnızca sıralarının değişmediğinden emin olur.

Daha önce belirtildiği gibi, I2P şu anda (sürüm 0.8) XOR tabanlı sıralama ile yukarıdaki katmanlı rastgele stratejiyi içermektedir. Tunnel işletimi, yönetimi ve eş seçimi ile ilgili mekaniklerin daha ayrıntılı bir tartışması [tunnel spesifikasyonunda](/docs/specs/tunnel-implementation/) bulunabilir.

---

### Ağ Veritabanı (netDb)

Daha önce belirtildiği gibi, I2P'nin netDb'si ağın meta verilerini paylaşmak için çalışır. Bu, [ağ veritabanı](/docs/specs/common-structures/) sayfasında detaylandırılmıştır, ancak temel bir açıklama aşağıda mevcuttur.

Tüm I2P router'ları yerel bir netDb içerir, ancak tüm router'lar DHT'ye katılmaz veya leaseset aramalarına yanıt vermez. DHT'ye katılan ve leaseset aramalarına yanıt veren bu router'lara 'floodfill' denir. Router'lar manuel olarak floodfill olarak yapılandırılabilir veya yeterli kapasiteye sahiplerse ve güvenilir çalışma için diğer kriterleri karşılıyorlarsa otomatik olarak floodfill olabilirler.

Diğer I2P router'lar verilerini saklayacak ve basit 'store' (depolama) ve 'lookup' (arama) sorguları göndererek floodfill'lerden veri arayacaklar. Bir floodfill router 'store' sorgusu alırsa, [Kademlia algoritmasını](http://en.wikipedia.org/wiki/Kademlia) kullanarak bilgiyi diğer floodfill router'lara yayacaktır. 'Lookup' sorguları şu anda önemli bir güvenlik sorunundan kaçınmak için farklı şekilde çalışır. Bir arama yapıldığında, floodfill router aramayı diğer eşlere iletmeyecek, bunun yerine her zaman kendisi cevap verecektir (eğer istenen veriye sahipse).

Ağ veritabanında iki tür bilgi saklanır.

- Bir **RouterInfo**, belirli bir I2P router hakkında bilgi ve ona nasıl ulaşılacağını saklar
- Bir **LeaseSet**, belirli bir hedef hakkında bilgi saklar (örn. I2P web sitesi, e-posta sunucusu...)

Tüm bu bilgiler yayınlayan taraf tarafından imzalanır ve bilgiyi kullanan veya depolayan herhangi bir I2P router tarafından doğrulanır. Ayrıca, veriler zamanlama bilgilerini içerir, böylece eski girişlerin depolanması ve olası saldırılar önlenir. Bu aynı zamanda I2P'nin doğru zamanı korumak için gerekli kodu paketlemesinin, zaman zaman bazı SNTP sunucularını sorgulama ([pool.ntp.org](http://www.pool.ntp.org/) varsayılan olarak round robin) ve transport katmanında router'lar arasındaki zaman farkını tespit etme nedenlerinden biridir.

Bazı ek açıklamalar da önemlidir.

- **Yayınlanmamış ve şifrelenmiş leaseSet'ler:**
  Bir kişi sadece belirli kişilerin bir hedefe ulaşabilmesini isteyebilir. Bu, hedefi netDb'de yayınlamayarak mümkündür. Ancak hedefi başka yollarla iletmeniz gerekecektir. Bu, 'şifrelenmiş leaseSet'ler tarafından desteklenir. Bu leaseSet'ler sadece şifre çözme anahtarına erişimi olan kişiler tarafından çözülebilir.

- **Bootstrapping:**
  netDb'yi başlatma oldukça basittir. Bir router, ulaşılabilir bir eş'in tek bir routerInfo'sunu almayı başardığında, o router'ı ağdaki diğer router'lara referanslar için sorgulayabilir. Şu anda, bir dizi kullanıcı bu bilgiyi kullanılabilir hale getirmek için routerInfo dosyalarını bir web sitesine gönderir. I2P otomatik olarak routerInfo dosyalarını toplamak ve başlatmak için bu web sitelerinden birine bağlanır. I2P bu bootstrap sürecini "reseeding" olarak adlandırır.

- **Arama ölçeklenebilirliği:**
  I2P ağındaki aramalar yinelemeli (iterative) olup, özyinelemeli (recursive) değildir. Bir floodfill'den yapılan arama başarısız olursa, arama bir sonraki en yakın floodfill'e tekrarlanır. floodfill, veri için başka bir floodfill'e özyinelemeli olarak sormaz. Yinelemeli aramalar büyük DHT ağları için ölçeklenebilirdir.

---

### Taşıma Protokolleri

Router'lar arasındaki iletişim, harici saldırganlara karşı gizlilik ve bütünlük sağlarken, iletişim kurulan router'ın belirli bir mesajı alması gereken router olduğunu doğrulamalıdır. Router'ların diğer router'larla nasıl iletişim kurduğunun detayları kritik değildir — bu temel gereksinimleri sağlamak için farklı zamanlarda üç ayrı protokol kullanılmıştır.

I2P şu anda TCP üzerinde [NTCP2](/docs/specs/ntcp2/) ve UDP üzerinde [SSU2](/docs/specs/ssu2/) olmak üzere iki transport protokolünü desteklemektedir. Bunlar, artık kullanımdan kaldırılmış olan önceki protokol sürümleri [NTCP](/docs/legacy/ssu/) ve [SSU](/docs/legacy/ssu/)'nun yerini almıştır. Her iki protokol de hem IPv4 hem de IPv6'yı destekler. Hem TCP hem de UDP transportlarını destekleyerek, I2P kısıtlayıcı sansür rejimlerinde trafiği engellemek amacıyla kurulan güvenlik duvarları da dahil olmak üzere çoğu güvenlik duvarını etkili bir şekilde aşabilir. NTCP2 ve SSU2, modern şifreleme standartlarını kullanmak, trafik tanımlama direncini artırmak, verimlilik ve güvenliği artırmak ve NAT geçişini daha sağlam hale getirmek için tasarlanmıştır. Router'lar desteklenen her bir transport ve IP adresini network database'de yayınlar. Halka açık IPv4 ve IPv6 ağlarına erişimi olan router'lar genellikle NTCP2/SSU2'nin IPv4/IPv6 ile her kombinasyonu için birer tane olmak üzere dört adres yayınlar.

[SSU2](/docs/specs/ssu2/) SSU'nun hedeflerini destekler ve genişletir. SSU2'nin Wireguard ve QUIC gibi diğer modern UDP tabanlı protokollerle birçok benzerliği vardır. UDP üzerinden ağ mesajlarının güvenilir taşınmasına ek olarak, SSU2 eşler arası, işbirlikçi IP adresi tespiti, güvenlik duvarı tespiti ve NAT geçişi için özel kolaylıklar sağlar. [SSU spesifikasyonunda](/docs/legacy/ssu/) açıklandığı gibi:

> Bu protokolün amacı, üçüncü taraflarca kolayca ayırt edilebilir minimum miktarda veri açığa çıkararak güvenli, kimlik doğrulamalı, yarı güvenilir ve sırasız mesaj teslimi sağlamaktır. Yüksek dereceli iletişimi desteklemeli ve ayrıca TCP dostu sıkışıklık kontrolü içermeli ve PMTU algılaması içerebilir. Ev kullanıcıları için yeterli hızlarda toplu veri aktarımını verimli bir şekilde gerçekleştirebilmelidir. Ek olarak, çoğu NAT veya güvenlik duvarı gibi ağ engellerini aşmak için teknikleri desteklemelidir.

[NTCP2](/docs/specs/ntcp2/), NTCP'nin hedeflerini destekler ve genişletir. Modern şifreleme standartlarını kullanarak TCP üzerinden ağ mesajlarının verimli ve tamamen şifreli taşınmasını ve trafik tanımlamasına karşı direnç sağlar.

I2P aynı anda birden fazla transport protokolünü destekler. Giden bağlantı için belirli bir transport "teklifler" ile seçilir. Her transport bağlantı için teklif verir ve bu tekliflerin göreceli değeri önceliği belirler. Transport protokolleri, eş noktaya (peer) zaten kurulmuş bir bağlantı olup olmadığına bağlı olarak farklı teklifler verebilir.

Bid (öncelik) değerleri uygulamaya bağlıdır ve trafik koşulları, bağlantı sayıları ve diğer faktörlere göre değişebilir. Router'lar ayrıca gelen bağlantılar için taşıma tercihlerini network database'de her taşıma ve adres için taşıma "maliyetleri" olarak yayınlar.

---

### Kriptografi

I2P, şifreleme, kimlik doğrulama ve doğrulama için birkaç protokol katmanında kriptografi kullanır. Ana protokol katmanları şunlardır: aktarım protokolleri, tunnel oluşturma mesajları, tunnel katmanı şifrelemesi, network database mesajları ve uçtan uca (garlic) mesajları. I2P'nin orijinal tasarımı, o dönemde güvenli kabul edilen küçük bir kriptografik temel öğeler kümesi kullanıyordu. Bunlar arasında ElGamal asimetrik şifrelemesi, DSA-SHA1 imzaları, AES256/CBC simetrik şifrelemesi ve SHA-256 hash'leri bulunuyordu. Kullanılabilir işlem gücü arttıkça ve kriptografik araştırmalar yıllar içinde önemli ölçüde geliştikçe, I2P'nin temel öğelerini ve protokollerini yükseltmesi gerekiyordu. Bu nedenle, "şifreleme türleri" ve "imza türleri" kavramını ekledik ve protokollerimizi bu tanımlayıcıları içerecek şekilde genişlettik ve desteği belirtmek için kullandık. Bu, geriye dönük uyumluluğu bozmadan veya ağ güncellemeleri için "bayrak günü" gerektirmeden, modern kriptografi için ağ desteğini periyodik olarak güncellememize ve genişletmememize ve ağı yeni temel öğeler için geleceğe hazır hale getirmemize olanak tanır. Bazı imza ve şifreleme türleri aynı zamanda deneysel kullanım için ayrılmıştır.

Çoğu protokol katmanında kullanılan mevcut temel yapı taşları X25519 anahtar değişimi, EdDSA imzaları, ChaCha20/Poly1305 kimlik doğrulamalı simetrik şifreleme ve SHA-256 hash'leridir. AES256 hala tunnel katman şifrelemesi için kullanılmaktadır. Bu modern protokoller ağ iletişiminin büyük çoğunluğu için kullanılır. ElGamal, ECDSA ve DSA-SHA1 dahil olmak üzere eski temel yapı taşları, eski router'larla iletişim kurarken geriye dönük uyumluluk için çoğu implementasyon tarafından desteklenmeye devam etmektedir. Bazı eski protokoller kullanımdan kaldırılmış ve/veya tamamen kaldırılmıştır. Yakın gelecekte, sağlam güvenlik standartlarımızı korumak için kuantum sonrası (PQ) veya hibrit-PQ şifreleme ve imzalara geçiş konusunda araştırmalara başlayacağız.

Bu kriptografik temel yapı taşları, I2P'nin çeşitli düşmanlara karşı katmanlı savunmalarını sağlamak için bir araya getirilmiştir. En alt seviyede, router'lar arası iletişim aktarım katmanı güvenliği ile korunmaktadır. Aktarım katmanları üzerinden geçen [tunnel](#tunnels) mesajları kendi katmanlı şifrelemeye sahiptir. Diğer çeşitli mesajlar da şifrelenmiş olan "garlic message" mesajları içinde iletilmektedir.

#### Garlic Mesajları

Garlic mesajları, "soğan" katmanlı şifrelemenin bir uzantısıdır ve tek bir mesajın içeriğinin birden fazla "karanfil" içermesine olanak tanır — kendi teslimat talimatlarıyla birlikte tam olarak oluşturulmuş mesajlar. Mesajlar, aksi takdirde bilgiye erişimi olmaması gereken bir peer üzerinden açık metin olarak geçecekleri durumlarda garlic mesajına sarılır — örneğin, bir router başka bir router'dan bir tunnel'a katılmasını istediğinde, isteği bir garlic içine sarar, bu garlic'i alıcı router'ın public key'i ile şifreler ve bir tunnel üzerinden iletir. Başka bir örnek ise bir istemcinin bir hedefe mesaj göndermek istediği durumdur — gönderen tarafın router'ı bu veri mesajını (diğer bazı mesajlarla birlikte) bir garlic içine sarar, bu garlic'i alıcının leaseSet'inde yayınlanan public key ile şifreler ve uygun tunnel'lar üzerinden iletir.

Şifreleme katmanındaki her clove'a eklenen "talimatlar", clove'un yerel olarak, uzak bir router'a veya uzak bir router'daki uzak bir tunnel'a iletilmesini talep etme yeteneğini içerir. Bu talimatlarda, bir eşin teslimatın belirli bir zaman veya koşul karşılanana kadar ertelenmesini talep etmesine olanak tanıyan alanlar bulunur, ancak [önemsiz olmayan gecikmeler](#variable-latency) devreye alınana kadar bu istekler yerine getirilmeyecektir. Garlic mesajlarını tunnel oluşturmadan istediğiniz sayıda hop boyunca açıkça yönlendirmek, hatta tunnel mesajlarını garlic mesajlarına sararak tunnel'daki bir sonraki hop'a teslim etmeden önce birkaç hop ileri göndererek yeniden yönlendirmek mümkündür, ancak bu teknikler mevcut implementasyonda şu anda kullanılmamaktadır.

#### Oturum Etiketleri

Güvenilmez, düzensiz, mesaj tabanlı bir sistem olarak I2P, garlic mesajlarına veri gizliliği ve bütünlüğü sağlamak için asimetrik ve simetrik şifreleme algoritmalarının basit bir kombinasyonunu kullanır. Orijinal kombinasyon ElGamal/AES+SessionTags olarak adlandırılıyordu, ancak bu 2048bit ElGamal, AES256, SHA256 ve 32 bayt nonce'ların basit kullanımını tanımlamak için aşırı ayrıntılı bir yoldur. Bu protokol hala desteklense de, ağın çoğu yeni bir protokol olan ECIES-X25519-AEAD-Ratchet'a geçmiştir. Bu protokol X25519, ChaCha20/Poly1305 ve 32 bayt nonce'ları üretmek için senkronize edilmiş bir PRNG'yi birleştirir. Her iki protokol de aşağıda kısaca açıklanacaktır.

#### ElGamal/AES+SessionTags

Bir router başka bir router'a garlic mesajı şifrelemek istediği ilk seferde, AES256 oturum anahtarı için anahtar materyalini ElGamal ile şifreler ve AES256/CBC şifrelenmiş yükü bu şifrelenmiş ElGamal bloğundan sonra ekler. Şifrelenmiş yükün yanı sıra, AES şifrelenmiş bölüm yük uzunluğunu, şifrelenmemiş yükün SHA256 hash'ini ve bir dizi "oturum etiketi" — rastgele 32 byte nonce'ları içerir. Gönderen bir sonraki sefer başka bir router'a garlic mesajı şifrelemek istediğinde, yeni bir oturum anahtarını ElGamal ile şifrelemek yerine daha önce teslim edilen oturum etiketlerinden birini seçer ve yükü daha önceki gibi AES ile şifreler, o oturum etiketi ile kullanılan oturum anahtarını kullanarak ve oturum etiketinin kendisini başa ekleyerek. Bir router garlic şifrelenmiş mesaj aldığında, mevcut bir oturum etiketiyle eşleşip eşleşmediğini görmek için ilk 32 byte'ı kontrol eder — eşleşirse, mesajı basitçe AES ile çözer, ancak eşleşmezse, ilk bloğu ElGamal ile çözer.

Her session tag'i yalnızca bir kez kullanılabilir, böylece dahili düşmanların farklı mesajları aynı router'lar arasında olduğu şeklinde gereksiz yere ilişkilendirmesi önlenir. ElGamal/AES+SessionTag şifrelenmiş mesaj gönderen, etiketleri ne zaman ve kaç tane teslim edeceğini seçer, alıcıyı bir dizi mesajı karşılayacak kadar etiketle önceden stoklar. Garlic mesajlar, küçük bir ek mesajı clove olarak paketleyerek (bir "teslimat durumu mesajı") başarılı etiket teslimatını tespit edebilir — garlic mesaj hedeflenen alıcıya ulaştığında ve başarıyla şifrelendiğinde, bu küçük teslimat durumu mesajı ortaya çıkan clove'lardan biridir ve alıcıya clove'u orijinal gönderene geri göndermesi talimatını verir (tabii ki bir inbound tunnel üzerinden). Orijinal gönderen bu teslimat durumu mesajını aldığında, garlic mesajda paketlenen session tag'lerin başarıyla teslim edildiğini bilir.

Session tag'lerinin kendileri çok kısa bir yaşam süresine sahiptir ve kullanılmazlarsa bu süre sonunda atılırlar. Ayrıca, her anahtar için saklanan miktar sınırlıdır, anahtarların sayısı da öyle - çok fazla gelirse, yeni veya eski mesajlar düşürülebilir. Gönderici, session tag'leri kullanan mesajların ulaşıp ulaşmadığını takip eder ve yeterli iletişim yoksa, daha önce düzgün bir şekilde teslim edildiği varsayılan mesajları düşürebilir ve tam maliyetli ElGamal şifrelemeye geri dönebilir.

#### ECIES-X25519-AEAD-Ratchet

ElGamal/AES+SessionTags birçok açıdan önemli ek yük gerektiriyordu. CPU kullanımı yüksekti çünkü ElGamal oldukça yavaştır. Bant genişliği aşırıydı çünkü büyük miktarda session tag'in önceden teslim edilmesi gerekiyordu ve ElGamal genel anahtarları çok büyüktür. Bellek kullanımı, büyük miktarda session tag saklama gereksinimi nedeniyle yüksekti. Güvenilirlik, kayıp session tag teslimatı nedeniyle zarar görüyordu.

ECIES-X25519-AEAD-Ratchet bu sorunları ele almak için tasarlandı. X25519 anahtar değişimi için kullanılır. ChaCha20/Poly1305 doğrulanmış simetrik şifreleme için kullanılır. Şifreleme anahtarları "çift ratchet" yani periyodik olarak döndürülür. Oturum etiketleri 32 bayttan 8 bayta düşürüldü ve bir PRNG ile üretiliyor. Protokol, Signal ve WhatsApp'ta kullanılan signal protokolü ile birçok benzerliğe sahiptir. Bu protokol CPU, RAM ve bant genişliğinde önemli ölçüde daha düşük yük sağlar.

Session etiketleri, session etiketleri ve session anahtarları üretmek için oturumun her iki ucunda çalışan deterministik senkronize bir PRNG'den üretilir. PRNG, SHA-256 HMAC kullanan bir HKDF'dir ve X25519 DH sonucundan beslenir. Session etiketleri hiçbir zaman önceden iletilmez; yalnızca mesajla birlikte dahil edilirler. Alıcı, session etiketi ile indekslenen sınırlı sayıda session anahtarı saklar. Gönderen, önceden gönderilmedikleri için herhangi bir session etiketi veya anahtarı saklamak zorunda değildir; talep üzerine üretilebilirler. Bu PRNG'yi gönderen ve alıcı arasında kabaca senkronize tutarak (alıcı, örneğin sonraki 50 etiketin bir penceresini önceden hesaplar), büyük sayıda etiketi periyodik olarak paketlemenin ek yükü ortadan kaldırılır.

---

## Gelecek

I2P protokolleri cep telefonları da dahil olmak üzere çoğu platformda verimlidir ve çoğu tehdit modeli için güvenlidir. Ancak, güçlü devlet destekli düşmanlarla karşı karşıya kalanların ihtiyaçlarını karşılamak ve sürekli gelişen kriptografik ilerlemeler ile sürekli artan bilgi işlem gücü tehditlerini karşılamak için daha fazla iyileştirme gerektiren birkaç alan vardır. İki olası özellik, kısıtlı rotalar ve değişken gecikme, 2003 yılında jrandom tarafından önerildi. Artık bu özellikleri uygulama planımız olmasa da, aşağıda açıklanmaktadır.

### Kısıtlı Rota İşlemi

I2P, işlevsel bir paket anahtarlamalı ağ üzerinde çalışacak şekilde tasarlanmış bir kaplama ağıdır ve anonimlik ile güvenlik sunmak için uçtan uca prensibi kullanır. İnternet artık uçtan uca prensibini tam olarak benimsemese de (NAT kullanımı nedeniyle), I2P ağın önemli bir bölümünün erişilebilir olmasını gerektirir — kenar bölgelerde kısıtlı rotalar kullanarak çalışan bir dizi eş (peer) olabilir, ancak I2P çoğu eşin erişilemez olduğu dejeneratif durum için uygun bir yönlendirme algoritması içermez. Ancak böyle bir algoritma kullanan bir ağ üzerinde çalışabilir.

Hangi eşlerin doğrudan erişilebilir olduğuna dair sınırlamaların bulunduğu kısıtlı rota işletimi, kısıtlı rotaların nasıl ele alındığına bağlı olarak çeşitli farklı işlevsel ve anonimlik etkilerine sahiptir. En temel düzeyde, kısıtlı rotalar bir eşin gelen bağlantılara izin vermeyen bir NAT veya güvenlik duvarının arkasında bulunduğu durumlarda ortaya çıkar. Bu, dağıtılmış delik delme tekniğinin aktarım katmanına entegre edilmesiyle büyük ölçüde çözülmüş ve çoğu NAT ve güvenlik duvarının arkasındaki kişilerin herhangi bir yapılandırma olmadan istenmeyen bağlantıları alabilmesini sağlamıştır. Ancak bu, eşin IP adresinin ağ içindeki routerlara maruz kalmasını sınırlamaz, çünkü yayınlanan introducer aracılığıyla eşle tanıştırılabilirler.

Kısıtlı rotaların işlevsel ele alınmasının ötesinde, kişinin IP adresinin maruziyetini sınırlamak için kullanılabilecek iki seviye kısıtlı işlem bulunmaktadır — iletişim için router-özgü tunneller kullanmak ve 'client routerlar' sunmak. İlki için, routerlar ya yeni bir tunnel havuzu oluşturabilir ya da mevcut keşif havuzlarını yeniden kullanabilir, transport adreslerinin yerine routerInfo'larının bir parçası olarak bazılarının gelen gateway'lerini yayınlayabilirler. Bir peer onlarla iletişim kurmak istediğinde, netDb'de bu tunnel gateway'lerini görür ve ilgili mesajı basitçe yayınlanan tunnellardan biri aracılığıyla gönderir. Kısıtlı rota arkasındaki peer yanıtlamak isterse, bunu ya doğrudan (IP'sini peer'a ifşa etmeye istekliyse) ya da dolaylı olarak giden tunnelleri aracılığıyla yapabilir. Peer'in doğrudan bağlantıları olan routerlar ona ulaşmak istediğinde (örneğin tunnel mesajlarını iletmek için), doğrudan bağlantılarını yayınlanan tunnel gateway'ine göre öncelikli hale getirirler. 'Client routerlar' kavramı, herhangi bir router adresi yayınlamayarak kısıtlı rotayı basitçe genişletir. Böyle bir router, routerInfo'sını netDb'de yayınlamaya bile gerek duymaz, sadece iletişim kurduğu peer'lara kendi imzalı routerInfo'sını sağlar (router'ın public keylerini geçirmek için gerekli).

Kısıtlı rotalar arkasındaki kullanıcılar için ödünleşimler vardır, çünkü muhtemelen diğer insanların tunnel'larına daha az sıklıkla katılırlar ve bağlı oldukları router'lar normalde açığa çıkmayacak trafik desenlerini çıkarabilir. Öte yandan, bu maruziyetin maliyeti bir IP adresinin kullanılabilir hale getirilmesinin maliyetinden düşükse, buna değer olabilir. Bu elbette, kısıtlı rota arkasındaki router'ın iletişim kurduğu eşlerin düşmanca olmadığını varsayar — ya ağ bağlantı kurmak için düşmanca bir eş kullanma olasılığının yeterince küçük olacağı kadar büyüktür, ya da bunun yerine güvenilir (ve belki geçici) eşler kullanılır.

Kısıtlı rotalar karmaşıktır ve genel hedef büyük ölçüde terk edilmiştir. Birkaç ilgili iyileştirme bunlara olan ihtiyacı büyük ölçüde azaltmıştır. Artık güvenlik duvarı portlarını otomatik olarak açmak için UPnP destekliyoruz. Hem IPv4 hem de IPv6 destekliyoruz. SSU2 adres tespiti, güvenlik duvarı durumu belirleme ve işbirlikli NAT delik delme özelliklerini iyileştirdi. SSU2, NTCP2 ve adres uyumluluk kontrolleri, tunnel oluşturulmadan önce tunnel hoplarının bağlanabilmesini sağlar. GeoIP ve ülke tanımlama, kısıtlayıcı güvenlik duvarları olan ülkelerdeki eşlerden kaçınmamızı sağlar. Bu güvenlik duvarlarının arkasındaki "gizli" routerlar için destek iyileştirildi. Bazı implementasyonlar ayrıca Yggdrasil gibi overlay ağlardaki eşlere bağlantıları destekler.

### Değişken Gecikme

I2P'nin ilk çabalarının büyük kısmı düşük gecikmeli iletişime odaklanmış olsa da, sistem başından itibaren değişken gecikme süreli hizmetleri göz önünde bulundurarak tasarlanmıştı. En temel düzeyde, I2P üzerinde çalışan uygulamalar orta ve yüksek gecikmeli iletişimin anonimliğini sunabilirken aynı zamanda trafik desenlerini düşük gecikmeli trafikle harmanlamaya devam edebilir. Dahili olarak ise I2P, garlic encryption aracılığıyla kendi orta ve yüksek gecikmeli iletişimini sunabilir — mesajın belirli bir gecikme sonrasında, belirli bir zamanda, belirli sayıda mesaj geçtikten sonra veya başka bir karıştırma stratejisi ile gönderilmesi gerektiğini belirterek. Katmanlı şifreleme ile yalnızca gecikme talebini açığa çıkaran clove'u alan router, mesajın yüksek gecikme gerektirdiğini bilir ve bu da trafiğin düşük gecikmeli trafikle daha da karışmasını sağlar. İletim ön koşulu karşılandığında, clove'u tutan router (ki bu muhtemelen kendisi bir garlic mesajı olacaktır) onu talep edildiği gibi basitçe iletir — bir router'a, bir tunnel'a veya büyük olasılıkla uzak bir istemci hedefine.

Değişken gecikme hizmetlerinin hedefi, bunu desteklemek için store-and-forward (sakla ve ilet) mekanizmaları için önemli kaynaklar gerektirir. Bu mekanizmalar i2p-bote gibi çeşitli mesajlaşma uygulamalarında desteklenebilir ve desteklenmektedir. Ağ seviyesinde, Freenet gibi alternatif ağlar bu hizmetleri sağlar. I2P router seviyesinde bu hedefi takip etmemeye karar verdik.

---

## Benzer Sistemler

I2P'nin mimarisi mesaj odaklı middleware kavramları, DHT'lerin topolojisi, serbest rota mixnet'lerin anonimlik ve kriptografisi ve paket anahtarlamalı ağların uyarlanabilirliği üzerine kurulmuştur. Değer yeni kavramlar veya algoritmalardan değil, mevcut sistemlerin ve makalelerin araştırma sonuçlarını birleştiren dikkatli mühendislikten gelir. Hem teknik hem de işlevsel karşılaştırmalar için incelenmeye değer birkaç benzer çaba olsa da, burada özellikle ikisi öne çıkarılmaktadır — Tor ve Freenet.

Ayrıca [Ağ Karşılaştırmaları Sayfası](/docs/overview/comparison/)'na bakın. Bu açıklamaların 2003 yılında jrandom tarafından yazıldığını ve şu anda doğru olmayabileceğini unutmayın.

### Tor

*[website](https://www.torproject.org/)*

İlk bakışta, Tor ve I2P birçok işlevsel ve anonimlik ile ilgili benzerliğe sahiptir. I2P'nin gelişimi Tor üzerindeki erken dönem çabalarından haberdar olmamızdan önce başlamış olsa da, orijinal onion routing ve ZKS çabalarının birçok dersi I2P'nin tasarımına entegre edilmiştir. Directory server'ları olan esasen güvenilir, merkezi bir sistem inşa etmek yerine, I2P her peer'in mevcut kaynakları en iyi şekilde nasıl kullanacağını belirlemek için diğer router'ları profilleme sorumluluğunu üstlendiği, kendi kendini organize eden bir network database'ine sahiptir. Bir diğer önemli fark ise hem I2P hem de Tor katmanlı ve sıralı yollar (tunnel'lar ve circuit'lar/stream'ler) kullanırken, I2P temelde paket anahtarlı bir ağ iken, Tor temelde devre anahtarlı bir ağdır ve bu I2P'nin şeffaf bir şekilde tıkanıklık veya diğer ağ arızalarını aşmasına, yedek yolları çalıştırmasına ve verileri mevcut kaynaklar arasında yük dengelemesi yapmasına olanak tanır. Tor entegre outproxy keşfi ve seçimi sunarak yararlı outproxy işlevselliği sunarken, I2P bu tür uygulama katmanı kararlarını I2P üzerinde çalışan uygulamalara bırakır — aslında I2P, TCP benzeri streaming kütüphanesinin kendisini bile uygulama katmanına dışsallaştırmış ve geliştiricilerin farklı stratejilerle deneyim yapmalarına, daha iyi performans sunmak için kendi alan özel bilgilerini kullanmalarına olanak tanımıştır.

Anonimlik perspektifinden bakıldığında, temel ağlar karşılaştırıldığında çok fazla benzerlik vardır. Ancak, birkaç temel fark bulunmaktadır. Dahili bir düşman veya çoğu harici düşmanla uğraşırken, I2P'nin simplex tunnel'ları, akışlara bakılarak Tor'un duplex devreleriyle ortaya çıkacak trafik verisinin yarısı kadar trafik verisi açığa çıkarır — bir HTTP isteği ve yanıtı Tor'da aynı yolu izlerken, I2P'de isteği oluşturan paketler bir veya daha fazla outbound tunnel üzerinden gider ve yanıtı oluşturan paketler bir veya daha fazla farklı inbound tunnel üzerinden geri gelir. I2P'nin peer seçimi ve sıralama stratejileri predecessor saldırılarını yeterince ele alması gerekirken, çift yönlü tunnel'lara geçiş gerekli olursa, basitçe aynı router'lar boyunca bir inbound ve outbound tunnel oluşturabiliriz.

Tor'un teleskopik tunnel oluşturma kullanımında başka bir anonimlik sorunu ortaya çıkar, çünkü bir devre içindeki hücreler düşmanın düğümünden geçerken basit paket sayma ve zamanlama ölçümleri, düşmanın devre içindeki konumu hakkında istatistiksel bilgi açığa çıkarır. I2P'nin tek mesajla tek yönlü tunnel oluşturması bu verinin açığa çıkmamasını sağlar. Tunnel içindeki konumu korumak önemlidir, çünkü aksi takdirde düşman bir dizi güçlü öncül, kesişim ve trafik doğrulama saldırısı düzenleyebilir.

Genel olarak, Tor ve I2P odaklandıkları konularda birbirlerini tamamlar — Tor yüksek hızda anonim İnternet outproxy hizmeti sunmaya odaklanırken, I2P kendi içinde merkezi olmayan dayanıklı bir ağ sunmaya odaklanır. Teoride, her ikisi de her iki amacı gerçekleştirmek için kullanılabilir, ancak sınırlı geliştirme kaynakları göz önüne alındığında, her ikisinin de güçlü ve zayıf yanları vardır. I2P geliştiricileri, Tor'u I2P'nin tasarımından faydalanacak şekilde değiştirmek için gerekli adımları değerlendirmişlerdir, ancak Tor'un kaynak kıtlığı altındaki yaşayabilirliği konusundaki endişeler, I2P'nin paket anahtarlama mimarisinin kıt kaynakları daha etkili bir şekilde kullanabileceğini öne sürmektedir.

### Freenet

*[web sitesi](http://www.freenetproject.org/)*

Freenet, I2P'nin tasarımının ilk aşamalarında büyük rol oynadı — ağ içinde tamamen yer alan canlı bir sözde isimli topluluğun uygulanabilirliğini kanıtlayarak, outproxy'lerde bulunan tehlikelerin önlenebileceğini gösterdi. I2P'nin ilk tohumları, ölçeklenebilir, anonim ve güvenli noktadan noktaya iletişimin karmaşıklıklarını, sansüre dirençli dağıtık veri depolama karmaşıklıklarından ayırmaya çalışan Freenet için bir yedek iletişim katmanı olarak başladı. Ancak zamanla, Freenet'in algoritmalarında bulunan bazı anonimlik ve ölçeklenebilirlik sorunları, I2P'nin odağının Freenet'in bir bileşeni olarak değil, genel bir anonim iletişim katmanı sağlama konusunda kalması gerektiğini açık hale getirdi. Yıllar boyunca, Freenet geliştiricileri eski tasarımdaki zayıflıkları görmeye başladı ve önemli anonimlik sunmak için bir "premix" katmanına ihtiyaç duyacaklarını öne sürmelerine neden oldu. Başka bir deyişle, Freenet'in I2P veya Tor gibi bir mixnet üzerinde çalışması gerekiyor; "istemci düğümleri" mixnet üzerinden "sunucu düğümlerine" veri talep edip yayınlıyor, sonra bu düğümler Freenet'in buluşsal dağıtık veri depolama algoritmalarına göre verileri getirip depoluyorlar.

Freenet'in işlevselliği I2P'nin işlevselliğini çok iyi tamamlar, çünkü Freenet doğal olarak orta ve yüksek gecikme süreli sistemleri işletmek için birçok araç sağlarken, I2P doğal olarak yeterli anonimlik sunmak için uygun olan düşük gecikme süreli mix network'ü sağlar. Mixnet'i sansüre dirençli dağıtık veri deposundan ayırma mantığı hâlâ mühendislik, anonimlik, güvenlik ve kaynak tahsisi perspektifinden açık görünüyor, bu nedenle umarım Freenet ekibi bu yönde çabalar gösterir, eğer I2P veya Tor gibi mevcut mixnet'leri basitçe yeniden kullanmıyorsa (veya gerektiğinde geliştirmeye yardım etmiyorsa).

---

## Ek A: Uygulama Katmanı

I2P'nin kendisi pek fazla şey yapmaz — sadece uzak hedeflere mesajlar gönderir ve yerel hedefleri hedefleyen mesajları alır — ilginç işlerin çoğu onun üzerindeki katmanlarda gerçekleşir. Tek başına I2P, anonim ve güvenli bir IP katmanı olarak görülebilir ve paketlenen [streaming library](#streaming-library) onun üzerinde anonim ve güvenli bir TCP katmanı uygulaması olarak görülebilir. Bunun ötesinde, [I2PTunnel](#i2ptunnel) I2P ağına girip çıkmak için genel bir TCP proxy sistemi sunar ve çeşitli ağ uygulamaları son kullanıcılar için daha fazla işlevsellik sağlar.

### Streaming Kütüphanesi

I2P streaming kütüphanesi genel bir streaming arayüzü (TCP soketlerini yansıtan) olarak görülebilir ve uygulama, I2P üzerindeki yüksek gecikmeyi hesaba katmak için çeşitli optimizasyonlarla birlikte [sliding window protokolünü](http://en.wikipedia.org/wiki/Sliding_Window_Protocol) destekler. Bireysel streamler maksimum paket boyutunu ve diğer seçenekleri ayarlayabilir, ancak varsayılan 4KB sıkıştırılmış boyut, kayıp mesajları yeniden iletmenin bant genişliği maliyetleri ile çoklu mesajların gecikmesi arasında makul bir denge gibi görünmektedir.

Ayrıca, sonraki mesajların nispeten yüksek maliyeti göz önüne alındığında, streaming kütüphanesinin mesajları planlama ve teslim etme protokolü, geçirilen bireysel mesajların mevcut olan tüm bilgiyi içermesine izin verecek şekilde optimize edilmiştir. Örneğin, streaming kütüphanesi aracılığıyla proxy edilen küçük bir HTTP işlemi tek bir round trip'te tamamlanabilir — ilk mesaj bir SYN, FIN ve küçük payload'u (genellikle bir HTTP isteği sığar) birleştirir ve yanıt SYN, FIN, ACK ve küçük payload'u (birçok HTTP yanıtı sığar) birleştirir. SYN/FIN/ACK'nin alındığını söylemek için ek bir ACK iletilmesi gerekse de, yerel HTTP proxy tam yanıtı tarayıcıya hemen teslim edebilir.

Genel olarak, streaming kütüphanesi kayan pencereleri, tıkanıklık kontrol algoritmaları (hem yavaş başlatma hem de tıkanıklık önleme) ve genel paket davranışları (ACK, SYN, FIN, RST, vb.) ile TCP'nin bir soyutlamasına oldukça benzemektedir.

### Adlandırma Kütüphanesi ve Adres Defteri

*Daha fazla bilgi için [İsimlendirme ve Adres Defteri](/docs/overview/naming/) sayfasına bakın.*

*Geliştiriciler: mihi, Ragnarok*

I2P içindeki adlandırma, olasılıklar spektrumundaki savunucularla birlikte en başından beri sıkça tartışılan bir konu olmuştur. Ancak, I2P'nin güvenli iletişim ve merkezi olmayan işleyiş için doğasında var olan talebi göz önüne alındığında, geleneksel DNS tarzı adlandırma sistemi açıkça dışarıda kalmaktadır, "çoğunluk kuralları" oylama sistemleri de öyle. Bunun yerine, I2P yerel ad-hedef eşlemesinden çalışacak şekilde tasarlanmış genel bir adlandırma kütüphanesi ve temel bir uygulama ile birlikte, ayrıca "Adres Defteri" adlı isteğe bağlı bir eklenti uygulaması ile birlikte gelmektedir. Adres defteri, güven ağı odaklı güvenli, dağıtık ve insan tarafından okunabilir bir adlandırma sistemidir, sadece tüm insan tarafından okunabilir adların küresel olarak benzersiz olma çağrısını feda ederek yalnızca yerel benzersizlik gerektirmektedir. I2P'deki tüm mesajlar hedeflerine göre kriptografik olarak adreslenmiş olsa da, farklı insanlar farklı hedeflere atıfta bulunan "Alice" için yerel adres defteri girdilerine sahip olabilirler. İnsanlar yine de güven ağlarında belirtilen emsallerin yayınlanmış adres defterlerini içe aktararak, üçüncü bir taraf aracılığıyla sağlanan girişleri ekleyerek veya (bazı insanlar ilk gelen ilk hizmet alan kayıt sistemi kullanarak bir dizi yayınlanmış adres defteri düzenlerse) bu adres defterlerini ad sunucuları olarak ele almayı seçerek geleneksel DNS'yi taklit ederek yeni adlar keşfedebilirler.

I2P, DNS benzeri hizmetlerin kullanımını teşvik etmez, çünkü bir sitenin ele geçirilmesi durumunda verilen zarar muazzam olabilir — ve güvensiz hedeflerin hiçbir değeri yoktur. DNSsec'in kendisi hâlâ kayıt şirketlerine ve sertifika otoritelerine dayanır, oysa I2P ile bir hedefe gönderilen istekler ele geçirilemez veya yanıt sahteleştirilemez, çünkü bunlar hedefin public key'lerine şifrelenir ve bir hedefin kendisi sadece bir çift public key ve bir sertifikadan oluşur. Diğer yandan DNS tarzı sistemler, arama yolundaki isim sunucularından herhangi birinin basit hizmet reddi ve sahteciliği saldırıları düzenlemesine izin verir. Yanıtları merkezi bir sertifika otoritesi tarafından imzalandığı şekilde doğrulayan bir sertifika eklemek, düşmanca isim sunucusu sorunlarının çoğunu çözebilir ancak tekrar saldırılarının yanı sıra düşmanca sertifika otoritesi saldırılarına da açık bırakır.

Oylama tarzı isimlendirme de tehlikelidir, özellikle anonim sistemlerde Sybil saldırılarının etkinliği göz önüne alındığında — saldırgan basitçe keyfi olarak yüksek sayıda peer oluşturabilir ve belirli bir ismi ele geçirmek için her biriyle "oy kullanabilir". Kimliği ücretsiz olmaktan çıkarmak için proof-of-work (çalışma kanıtı) yöntemleri kullanılabilir, ancak ağ büyüdükçe çevrimiçi oylama yürütmek için herkesle iletişim kurmanın gerektirdiği yük makul değildir, ya da tam ağ sorgulanmazsa farklı cevap setlerine ulaşılabilir.

Ancak İnternet'te olduğu gibi, I2P de bir isimlendirme sisteminin tasarımını ve işleyişini (IP benzeri) iletişim katmanının dışında tutuyor. Paketlenmiş isimlendirme kütüphanesi, alternatif isimlendirme sistemlerinin bağlanabileceği basit bir servis sağlayıcı arayüzü içeriyor ve böylece son kullanıcıların hangi tür isimlendirme ödünleşimlerini tercih ettiklerini belirlemelerine olanak tanıyor.

### I2PTunnel

*Geliştiren: mihi*

I2PTunnel muhtemelen I2P'nin en popüler ve çok yönlü istemci uygulamasıdır ve I2P ağına hem giriş hem de çıkış yönünde genel proxy işlevi sağlar. I2PTunnel dört ayrı proxy uygulaması olarak görülebilir — gelen TCP bağlantılarını alan ve bunları belirli bir I2P destination'a ileten bir "client", HTTP proxy gibi davranan ve istekleri uygun I2P destination'a ileten (gerekirse naming service'i sorgulayarak) bir "httpclient" (aka "eepproxy"), bir destination üzerinde gelen I2P streaming bağlantılarını alan ve bunları belirli bir TCP host+port'a ileten bir "server", ve HTTP istek ve yanıtlarını ayrıştırarak daha güvenli işlem sağlayan "server"ı genişleten bir "httpserver". Ek bir "socksclient" uygulaması da vardır, ancak daha önce belirtilen nedenlerle kullanımı önerilmez.

I2P'nin kendisi bir outproxy ağı değildir — verileri karışım ağına girip çıkaran bir mix net'in doğasında bulunan anonimlik ve güvenlik endişeleri, I2P'nin tasarımını dış kaynaklara ihtiyaç duymadan kullanıcının ihtiyaçlarını karşılayabilen anonim bir ağ sağlamaya odaklanmış durumda tutmuştur. Ancak, I2PTunnel "httpclient" uygulaması outproxy için bir kanca sunar — istenen hostname ".i2p" ile bitmiyorsa, kullanıcının sağladığı outproxy setinden rastgele bir hedef seçer ve isteği onlara yönlendirir. Bu hedefler, açık bir şekilde outproxy çalıştırmayı seçen gönüllüler tarafından çalıştırılan basit I2PTunnel "server" örnekleridir — hiç kimse varsayılan olarak outproxy değildir ve outproxy çalıştırmak otomatik olarak diğer insanlara sizin üzerinizden proxy yapmasını söylemez. Outproxy'lerin doğal zayıflıkları olsa da, I2P kullanımı için basit bir kavram kanıtı sunar ve bazı kullanıcılar için yeterli olabilecek bir tehdit modeli altında bazı işlevsellik sağlar.

I2PTunnel kullanımdaki uygulamaların çoğunu etkinleştirir. Bir web sunucusuna işaret eden bir "httpserver", herkesin kendi anonim web sitesini (veya "I2P Site") çalıştırmasına olanak tanır — bu amaç için I2P ile birlikte bir web sunucusu paketlenmiştir, ancak herhangi bir web sunucusu kullanılabilir. Herkes anonim olarak barındırılan IRC sunucularından birine işaret eden bir "client" çalıştırabilir; bunların her biri yerel IRCd'lerine işaret eden bir "server" çalıştırır ve IRCd'ler arasında kendi "client" tunnel'ları üzerinden iletişim kurar. Son kullanıcıların ayrıca [I2Pmail'in](#i2pmail--susimail) POP3 ve SMTP hedeflerine işaret eden "client" tunnel'ları vardır (bunlar da basitçe POP3 ve SMTP sunucularına işaret eden "server" örnekleridir), ayrıca I2P'nin CVS sunucusuna işaret eden "client" tunnel'ları da vardır ve bu anonim geliştirmeye olanak tanır. Zaman zaman insanlar bir NNTP sunucusuna işaret eden "server" örneklerine erişmek için "client" proxy'leri bile çalıştırmışlardır.

### I2PSnark

*I2PSnark geliştiricileri: jrandom ve diğerleri, [mjw](http://www.klomp.org/mark/)'nin [Snark](http://www.klomp.org/snark/) istemcisinden uyarlanmıştır*

I2P kurulumunda dahil olan I2PSnark, çoklu torrent yetenekleri ile basit bir anonim BitTorrent istemcisi sunar ve tüm işlevselliği düz HTML web arayüzü üzerinden kullanıma sunar.

### I2Pmail / Susimail

*Geliştiren: postman, susi23, mastiejaner*

I2Pmail bir uygulamadan çok bir hizmettir — postman, mastiejaner ile geliştirilen bir dizi bileşene erişen I2PTunnel örnekleri aracılığıyla POP3 ve SMTP hizmeti ile hem dahili hem de harici e-posta sunar, böylece insanlar tercih ettikleri posta istemcilerini kullanarak takma ad altında posta gönderip alabilirler. Ancak çoğu posta istemcisi önemli miktarda tanımlayıcı bilgi açığa çıkardığından, I2P özellikle I2P'nin anonimlik ihtiyaçları göz önünde bulundurularak oluşturulan susi23'ün web tabanlı susimail istemcisini paketler. I2Pmail/mail.i2p hizmeti, hashcash destekli kotalarla hizmet reddi önlemesinin yanı sıra şeffaf virüs filtreleme sunar. Ayrıca, her kullanıcı mail.i2p outproxy'leri aracılığıyla teslimattan önce toplama stratejilerini kontrol edebilir; bu outproxy'ler mail.i2p SMTP ve POP3 sunucularından ayrıdır — hem outproxy'ler hem de inproxy'ler mail.i2p SMTP ve POP3 sunucularıyla I2P'nin kendisi aracılığıyla iletişim kurar, bu nedenle bu anonim olmayan konumların ele geçirilmesi kullanıcının posta hesaplarına veya aktivite kalıplarına erişim sağlamaz.
