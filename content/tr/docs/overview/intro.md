---
title: "I2P: Anonim İletişim için Ölçeklenebilir Bir Çerçeve"
description: "I2P mimarisi ve işleyişine giriş"
slug: "intro"
aliases:
  - "/tr/intro"
  - "/tr/intro/"
  - "/tr/how_intro"
  - "/tr/how_intro/"
lastUpdated: "2025-01"
accurateFor: "0.9.65"
---

NOT: Bu belge orijinal olarak 2003 yılında jrandom tarafından yazılmıştır. Güncel tutmaya çalışsak da, bazı bilgiler eski veya eksik olabilir. Taşıma ve kriptografi bölümleri 2025-01 itibariyle günceldir.

## Giriş

I2P, ölçeklenebilir, kendi kendini organize eden, dayanıklı paket anahtarlamalı anonim bir ağ katmanıdır ve üzerinde anonimlik veya güvenlik odaklı herhangi bir sayıda farklı uygulama çalışabilir. Bu uygulamaların her biri, serbest yönlü mixnet'in (karışım ağı) uygun implementasyonu konusunda endişelenmeden kendi anonimlik, gecikme ve verim dengelerini kurabilir ve böylece aktivitelerini I2P üzerinde halihazırda çalışan daha büyük kullanıcı anonimlik kümesiyle harmanlayabilir.

Halihazırda mevcut uygulamalar, tipik İnternet etkinliklerinin tam yelpazesini sağlar — **anonim** web tarama, web barındırma, sohbet, dosya paylaşımı, e-posta, blog yazma ve içerik sendikasyonu ile geliştirme aşamasında olan diğer birçok uygulama.

- Web tarayıcısı: proxy kullanımını destekleyen herhangi bir mevcut tarayıcı kullanarak.
- Sohbet: IRC ve diğer protokoller
- Dosya paylaşımı: [I2PSnark](#i2psnark) ve diğer uygulamalar
- E-posta: [susimail](#i2pmail--susimail) ve diğer uygulamalar
- Blog: herhangi bir yerel web sunucusu veya mevcut eklentiler kullanarak

[Freenet](#freenet) veya [GNUnet](https://www.gnunet.org/en/) gibi içerik dağıtım ağlarında barındırılan web sitelerinin aksine, I2P üzerinde barındırılan hizmetler tamamen etkileşimlidir — geleneksel web tarzı arama motorları, bülten panoları, yorum yapabileceğiniz bloglar, veritabanı tabanlı siteler ve Freenet gibi statik sistemleri yerel olarak kurmanıza gerek kalmadan sorgulayabileceğiniz köprüler bulunmaktadır.

Tüm bu anonimlik destekli uygulamalarla birlikte, I2P mesaj odaklı ara yazılım rolünü üstlenir — uygulamalar bazı verileri kriptografik bir tanımlayıcıya (bir "destination") göndermek istediklerini belirtir ve I2P bunun güvenli ve anonim şekilde ulaştırılmasından sorumludur. I2P aynı zamanda I2P'nin anonim best-effort mesajlarının güvenilir, sıralı akışlar halinde aktarılmasına olanak tanıyan basit bir [streaming](#streaming-library) kütüphanesi sunar ve ağın yüksek bant genişliği gecikme çarpımına uyarlanmış TCP tabanlı tıkanıklık kontrol algoritmasını şeffaf şekilde sunar. Mevcut uygulamaları ağa bağlamak için birkaç basit SOCKS proxy mevcut olsa da, değerleri sınırlı kalmıştır çünkü neredeyse her uygulama rutin olarak anonim bağlamda hassas olan bilgileri açığa çıkarır. Güvenli olan tek yol, uygulamanın düzgün çalışmasını sağlamak için tam olarak denetlemektir ve buna yardımcı olmak için ağdan en iyi şekilde yararlanmak üzere kullanılabilecek çeşitli dillerde bir dizi API sağlıyoruz.

I2P akademik, ticari veya hükümet destekli bir araştırma projesi değildir; bunun yerine ihtiyaç duyan kişilere yeterli düzeyde anonimlik sağlamak için gerekli her şeyi yapmayı hedefleyen bir mühendislik çabasıdır. 2003 yılının başından beri bir tam zamanlı geliştirici ve dünya çapından özel bir yarı zamanlı katkı sağlayıcı grubu ile aktif geliştirme halindedir. I2P üzerinde yapılan tüm çalışmalar açık kaynaklıdır ve [web sitesinde](/) ücretsiz olarak mevcuttur. Kodun büyük bir kısmı doğrudan kamu alanına yayınlanmış olup, yalnızca birkaç kriptografik rutin BSD tarzı lisanslar altında kullanılmaktadır. I2P üzerinde çalışan kişiler, istemci uygulamalarını hangi lisans altında yayınlayacaklarını kontrol etmezler ve GPL lisanslı birkaç uygulama mevcuttur ([I2PTunnel](#i2ptunnel), [susimail](#i2pmail--susimail), [I2PSnark](#i2psnark), I2P-Bote, I2Phex ve diğerleri). I2P finansmanı tamamen bağışlardan gelmekte olup, şu anda hiçbir yargı yetkisinde vergi avantajı almamaktadır, çünkü geliştiricilerin birçoğu kendileri anonimdir.

---

## İşlem

### Genel Bakış

I2P'nin işleyişini anlamak için birkaç temel kavramı anlamak gereklidir. İlk olarak, I2P ağa katılan yazılım (bir "router") ile bireysel uygulamalarla ilişkili anonim uç noktalar ("destinations") arasında katı bir ayrım yapar. Birinin I2P çalıştırdığı genellikle bir sır değildir. Gizlenen şey, kullanıcının ne yaptığına dair bilgiler (eğer bir şey yapıyorsa) ve belirli bir destination'ın hangi router'a bağlı olduğu bilgisidir. Son kullanıcılar genellikle router'larında birkaç yerel destination'a sahip olacaktır — örneğin, biri IRC sunucularına proxy görevi görmek için, diğeri kullanıcının anonim web sunucusunu ("I2P Site") desteklemek için, bir diğeri I2Phex örneği için, başka bir tanesi torrent'ler için, vb.

Anlaşılması gereken bir diğer kritik kavram da "tunnel"dır. Tunnel, açıkça seçilmiş router listesi üzerinden geçen yönlendirilmiş bir yoldur. Katmanlı şifreleme kullanılır, böylece router'ların her biri yalnızca tek bir katmanın şifresini çözebilir. Şifresi çözülen bilgi, bir sonraki router'ın IP'sini ve iletilecek şifrelenmiş bilgiyi içerir. Her tunnel'ın bir başlangıç noktası (ilk router, "gateway" olarak da bilinir) ve bir bitiş noktası vardır. Mesajlar yalnızca tek yönde gönderilebilir. Mesajları geri göndermek için başka bir tunnel gereklidir.

![Gelen ve giden tunnel şeması](/images/tunnels.svg) *Şekil 1: İki tür tunnel vardır: gelen ve giden.*

İki tür tunnel bulunur: **"outbound" tunnel'lar** mesajları tunnel yaratıcısından uzağa gönderirken, **"inbound" tunnel'lar** mesajları tunnel yaratıcısına getirir. Bu iki tunnel'ın birleşimi kullanıcıların birbirlerine mesaj göndermesine olanak tanır. Gönderen ("Alice" yukarıdaki resimde) bir outbound tunnel kurarken, alıcı ("Bob" yukarıdaki resimde) bir inbound tunnel oluşturur. Bir inbound tunnel'ın gateway'i herhangi bir başka kullanıcıdan mesaj alabilir ve bunları endpoint'e ("Bob") kadar iletir. Outbound tunnel'ın endpoint'i mesajı inbound tunnel'ın gateway'ine iletmesi gerekir. Bunu yapmak için, gönderen ("Alice") şifreli mesajına talimatlar ekler. Outbound tunnel'ın endpoint'i mesajın şifresini çözdüğünde, mesajı doğru inbound gateway'ine ("Bob"'a giden gateway) yönlendirme talimatlarına sahip olacaktır.

Anlaşılması gereken üçüncü kritik kavram I2P'nin **"network database"** (veya "netDb") — ağ meta verilerini paylaşmak için kullanılan bir algoritma çiftidir. Taşınan iki meta veri türü **"routerInfo"** ve **"leaseSets"** — routerInfo, router'lara belirli bir router ile iletişim kurmak için gerekli verileri verir (public key'leri, transport adresleri, vb.), leaseSets ise router'lara belirli bir hedefle iletişim kurmak için gerekli bilgileri verir. Bir leaseSet bir dizi "lease" içerir. Bu lease'lerin her biri, belirli bir hedefe ulaşmaya izin veren bir tunnel gateway belirtir. Bir lease'de bulunan tam bilgiler:

- Belirli bir hedefe ulaşmayı sağlayan tunnel için gelen ağ geçidi.
- Tunnel'ın sona ereceği zaman.
- Mesajları şifreleyebilmek için genel anahtar çifti (tunnel üzerinden göndermek ve hedefe ulaşmak için).

Router'lar kendi routerInfo bilgilerini doğrudan netDb'ye gönderirken, leaseSet'ler giden tunnel'lar aracılığıyla gönderilir (leaseSet'lerin anonim olarak gönderilmesi gerekir, böylece bir router ile onun leaseSet'leri arasında bağlantı kurulması önlenir).

Ağda başarılı bağlantılar kurmak için yukarıdaki kavramları birleştirebiliriz.

Kendi gelen ve giden tunnel'larını kurmak için Alice, routerInfo toplamak amacıyla netDb'de arama yapar. Bu şekilde, tunnel'larında hop olarak kullanabileceği eş listelerini toplar. Daha sonra ilk hop'a bir yapı mesajı gönderebilir, bir tunnel'ın yapımını talep edebilir ve o router'dan yapım mesajını tunnel yapılana kadar ileriye iletmesini isteyebilir.

![Diğer router'lar hakkında bilgi talep et](/images/netdb_get_routerinfo_1.svg)

![Router bilgilerini kullanarak tunnel oluşturma](/images/netdb_get_routerinfo_2.svg) *Şekil 2: Router bilgileri tunnel oluşturmak için kullanılır.*

Alice, Bob'a bir mesaj göndermek istediğinde, önce netDb'de Bob'un leaseSet'ini bulmak için arama yapar ve böylece Bob'un mevcut gelen tunnel gateway'lerini elde eder. Daha sonra kendi giden tunnel'larından birini seçer ve mesajı, giden tunnel'ın bitiş noktasına mesajı Bob'un gelen tunnel gateway'lerinden birine iletmesi talimatıyla birlikte gönderir. Giden tunnel bitiş noktası bu talimatları aldığında, mesajı talep edildiği gibi iletir ve Bob'un gelen tunnel gateway'i mesajı aldığında, tunnel boyunca Bob'un router'ına iletilir. Alice, Bob'un mesajı yanıtlayabilmesini istiyorsa, kendi hedefini mesajın bir parçası olarak açıkça iletmesi gerekir. Bu, [streaming](#streaming-library) kütüphanesinde yapıldığı gibi üst düzey bir katman tanıtarak gerçekleştirilebilir. Alice ayrıca en güncel LeaseSet'ini mesajla birlikte paketleyerek yanıt süresini kısaltabilir, böylece Bob yanıt vermek istediğinde bunun için netDb araması yapmasına gerek kalmaz, ancak bu isteğe bağlıdır.

![LeaseSet'ler kullanarak tünelleri bağlama](/images/netdb_get_leaseset.svg) *Şekil 3: LeaseSet'ler giden ve gelen tünelleri bağlamak için kullanılır.*

Tunnel'ların kendileri ağ içindeki eşlere yetkisiz ifşayı önlemek için katmanlı şifrelemeye sahip olsa da (transport katmanının kendisi de ağ dışındaki eşlere yetkisiz ifşayı önlemek için yaptığı gibi), mesajı outbound tunnel uç noktasından ve inbound tunnel ağ geçidinden gizlemek için ek bir uçtan uca şifreleme katmanı eklemek gereklidir. Bu "[garlic encryption](#garlic-messages)", Alice'in router'ının birden fazla mesajı tek bir "garlic mesajı" içinde paketlemesine izin verir ve belirli bir public key ile şifrelenir, böylece ara eşler ne garlic içinde kaç mesaj olduğunu, ne bu mesajların ne dediğini, ne de bu bireysel clove'ların nereye gideceğini belirleyemez. Alice ve Bob arasındaki tipik uçtan uca iletişim için, garlic Bob'un leaseSet'inde yayınlanan public key ile şifrelenir ve bu sayede mesaj Bob'un kendi router'ına public key vermeden şifrelenmesine olanak tanır.

Akılda tutulması gereken bir diğer önemli gerçek ise I2P'nin tamamen mesaj tabanlı olması ve yol boyunca bazı mesajların kaybolabileceğidir. I2P kullanan uygulamalar mesaj odaklı arayüzleri kullanabilir ve kendi tıkanıklık kontrolü ile güvenilirlik ihtiyaçlarını karşılayabilir, ancak çoğu için I2P'yi akış tabanlı bir ağ olarak görmeyi sağlayan mevcut [streaming](#streaming-library) kütüphanesini yeniden kullanmak en iyi seçenek olacaktır.

---

### Tunnel'lar

Hem gelen hem de giden tunnel'lar benzer ilkeler üzerinde çalışır. Tunnel gateway'i bir dizi tunnel mesajını biriktirir ve sonunda bunları tunnel teslimatı için bir şeye ön işler. Ardından, gateway bu ön işlenmiş veriyi şifreler ve ilk durağa iletir. Bu eş ve sonraki tunnel katılımcıları, bir sonraki eşe iletmeden önce bunun kopya olmadığını doğruladıktan sonra bir şifreleme katmanı ekler. Sonunda, mesaj uç noktaya ulaşır ve burada mesajlar tekrar ayrılır ve istendiği gibi iletilir. Fark, tunnel'ın yaratıcısının ne yaptığında ortaya çıkar — gelen tunnel'lar için yaratıcı uç nokta olup tüm eklenen katmanları basitçe şifrelerken, giden tunnel'lar için yaratıcı gateway olup tüm katmanları önceden şifreler, böylece tüm hop başına şifreleme katmanları eklendikten sonra mesaj tunnel uç noktasında açık olarak ulaşır.

Mesajları iletmek için seçilen belirli eşlerin (peer) yanı sıra bunların özel sıralaması, I2P'nin hem anonimlik hem de performans özelliklerini anlamak için önemlidir. Network database (netDb) (aşağıda) sorgulanacak eşleri seçmek ve girişleri depolamak için kendi kriterlerine sahip olsa da, tunnel yaratıcıları ağdaki herhangi bir eşi herhangi bir sırada (ve hatta tek bir tunnel'da herhangi bir sayıda) kullanabilir. Mükemmel gecikme ve kapasite verileri küresel olarak bilinse, seçim ve sıralama istemcinin tehdit modeliyle birlikte özel ihtiyaçları tarafından yönlendirilirdi. Ne yazık ki, gecikme ve kapasite verilerini anonim olarak toplamak önemsiz değildir ve bu bilgiyi sağlaması için güvenilmeyen eşlere bağımlı olmak ciddi anonimlik sonuçları doğurur.

Anonimlik perspektifinden bakıldığında, en basit teknik tüm ağdan rastgele peer'ları seçmek, bunları rastgele sıralamak ve bu peer'ları o sırada sonsuza kadar kullanmak olacaktır. Performans perspektifinden bakıldığında ise, en basit teknik gerekli yedek kapasiteye sahip en hızlı peer'ları seçmek, şeffaf arıza durumu geçişini sağlamak için yükü farklı peer'lar arasında yaymak ve kapasite bilgileri değiştiğinde tunnel'ı yeniden inşa etmek olacaktır. İlki hem kırılgan hem de verimsiz olsa da, ikincisi erişilemeyen bilgi gerektirir ve yetersiz anonimlik sunar. I2P bunun yerine peer'ları profillerine göre düzenlemek için anonimlik bilincine sahip ölçüm koduyla birleştirilmiş bir dizi peer seçim stratejisi sunmaya çalışmaktadır.

Temel olarak, I2P sürekli olarak etkileşimde bulunduğu eşlerle ilgili profil oluşturur ve bunları dolaylı davranışlarını ölçerek yapar — örneğin, bir eş bir netDb sorgulamasına 1.3 saniyede yanıt verdiğinde, bu gidiş-dönüş gecikmesi hem istek ve yanıtın geçtiği iki tunnel (gelen ve giden) üzerinden dahil olan tüm routerların profillerine hem de sorgulanan eşin profiline kaydedilir. Aktarım katmanı gecikmesi veya tıkanıklık gibi doğrudan ölçümler profilin bir parçası olarak kullanılmaz, çünkü bunlar manipüle edilebilir ve ölçüm yapan router ile ilişkilendirilerek onları basit saldırılara maruz bırakabilir. Bu profilleri toplarken, her birinin performansını özetlemek için bir dizi hesaplama yapılır — gecikmesi, yoğun aktiviteyi işleme kapasitesi, şu anda aşırı yüklenip yüklenmediği ve ağa ne kadar iyi entegre olduğu görünüyor. Bu hesaplamalar daha sonra aktif eşler için karşılaştırılarak routerları dört katmana organize eder — hızlı ve yüksek kapasiteli, yüksek kapasiteli, başarısız olmayan ve başarısız olan. Bu katmanların eşikleri dinamik olarak belirlenir ve şu anda oldukça basit algoritmalar kullanılsa da, alternatifler mevcuttur.

Bu profil verilerini kullanarak, en basit makul eş seçim stratejisi üst katmandaki eşleri (hızlı ve yüksek kapasiteli) rastgele seçmektir ve bu şu anda istemci tunnel'ları için kullanılmaktadır. Keşif tunnel'ları (netDb ve tunnel yönetimi için kullanılan) "başarısız olmayan" katmandan rastgele eş seçer (bu katman 'daha iyi' katlardaki router'ları da içerir), bu sayede eşin router'ları daha geniş bir alanda örneklemesine olanak tanır ve peer seçimini rastgele [tepe tırmanışı](https://en.wikipedia.org/wiki/Hill_climbing) ile optimize eder. Ancak bu stratejiler tek başlarına, predecessor ve netDb toplama saldırıları yoluyla router'ın üst katmanındaki eşler hakkında bilgi sızdırır. Bunun karşılığında, yükü eşit şekilde dengelemese de belirli düşman sınıflarının gerçekleştirdiği saldırıları ele alacak çeşitli alternatifler mevcuttur.

Rastgele bir anahtar seçip eşleri (peers) bu anahtardan XOR mesafelerine göre sıralayarak, predecessor ve harvesting saldırılarında sızan bilgi, eşlerin başarısızlık oranına ve katmanın churn'üne göre azaltılır. NetDb harvesting saldırılarıyla başa çıkmanın başka bir basit stratejisi, gelen tunnel gateway(ler)ini sabit tutup tunnel'larda daha ilerde bulunan eşleri rastgele seçmektir. İstemcinin iletişim kurduğu düşmanlar için predecessor saldırılarıyla başa çıkmak amacıyla, giden tunnel uç noktaları da sabit kalacaktır. En çok maruz kalan noktada hangi eşin sabitleneceğinin seçimi elbette süre sınırına sahip olmalıdır, çünkü tüm eşler sonunda başarısız olur, bu nedenle ya reaktif olarak ayarlanabilir ya da diğer router'ların ölçülmüş ortalama arıza süresini taklit etmek için proaktif olarak önlenebilir. Bu iki strateji de birleştirilebilir, sabit bir maruz eş kullanılarak ve tunnel'ların kendisinde XOR tabanlı sıralama yapılarak. Daha katı bir strateji, potansiyel bir tunnel'ın tam eşlerini ve sıralamasını sabitleyecek, sadece hepsi her seferinde aynı şekilde katılmayı kabul ederse bireysel eşleri kullanacaktır. Bu, her eşin predecessor ve successor'ının her zaman aynı olması bakımından XOR tabanlı sıralamadan farklıdır, XOR ise sadece sıralarının değişmemesini sağlar.

Daha önce belirtildiği gibi, I2P şu anda (0.8 sürümü) XOR tabanlı sıralama ile yukarıdaki katmanlı rastgele stratejiyi içermektedir. Tunnel işletimi, yönetimi ve eş seçimi ile ilgili mekaniklerin daha ayrıntılı tartışması [tunnel spec](/docs/specs/tunnel-implementation/) adresinde bulunabilir.

---

### Network Database (netDb)

Daha önce belirtildiği gibi, I2P'nin netDb'si ağın meta verilerini paylaşmak için çalışır. Bu, [ağ veritabanı](/docs/specs/common-structures/) sayfasında ayrıntılı olarak açıklanmıştır, ancak aşağıda temel bir açıklama mevcuttur.

Tüm I2P router'ları yerel bir netDb içerir, ancak tüm router'lar DHT'ye katılmaz veya leaseSet aramalarına yanıt vermez. DHT'ye katılan ve leaseSet aramalarına yanıt veren router'lara 'floodfill' denir. Router'lar manuel olarak floodfill olarak yapılandırılabilir veya yeterli kapasiteye sahip olup güvenilir çalışma için diğer kriterleri karşıladıklarında otomatik olarak floodfill haline gelebilir.

Diğer I2P router'ları verilerini saklayacak ve basit 'store' ve 'lookup' sorguları göndererek floodfill'lerden veri arayacaklardır. Bir floodfill router 'store' sorgusu alırsa, [Kademlia algoritması](http://en.wikipedia.org/wiki/Kademlia) kullanarak bilgiyi diğer floodfill router'lara yayacaktır. 'Lookup' sorguları şu anda önemli bir güvenlik sorununu önlemek için farklı çalışmaktadır. Bir lookup yapıldığında, floodfill router lookup'ı diğer eşlere iletmeyecek, bunun yerine her zaman kendisi cevap verecektir (eğer istenen veriye sahipse).

Ağ veritabanında iki tür bilgi saklanır.

- Bir **RouterInfo**, belirli bir I2P router hakkında bilgileri ve ona nasıl ulaşılacağını saklar
- Bir **LeaseSet**, belirli bir hedef hakkında bilgileri saklar (örneğin I2P web sitesi, e-posta sunucusu...)

Tüm bu bilgiler yayınlayan taraf tarafından imzalanır ve bilgiyi kullanan veya saklayan herhangi bir I2P router tarafından doğrulanır. Ayrıca, veri eski girişlerin saklanmasını ve olası saldırıları önlemek için zamanlama bilgisi içerir. Bu nedenle I2P, doğru zamanı korumak için gerekli kodu paketler, zaman zaman bazı SNTP sunucularını sorgular (varsayılan olarak [pool.ntp.org](http://www.pool.ntp.org/) round robin) ve taşıma katmanında router'lar arasındaki zaman farkını tespit eder.

Bazı ek açıklamalar da önemlidir.

- **Yayımlanmamış ve şifrelenmiş leaseSet'ler:**
  Kişi sadece belirli kişilerin bir hedefe ulaşabilmesini isteyebilir. Bu, hedefi netDb'de yayımlamayarak mümkündür. Ancak hedefi başka yollarla iletmeniz gerekecektir. Bu, 'şifrelenmiş leaseSet'ler tarafından desteklenir. Bu leaseSet'ler yalnızca şifre çözme anahtarına erişimi olan kişiler tarafından çözülebilir.

- **Bootstrapping:**
  netDb'nin bootstrapping işlemi oldukça basittir. Bir router, erişilebilir bir eşten tek bir routerInfo almayı başardığında, ağdaki diğer routerlara referanslar için o routeri sorgulayabilir. Şu anda, bir dizi kullanıcı bu bilgiyi erişilebilir hale getirmek için routerInfo dosyalarını bir web sitesine gönderir. I2P, routerInfo dosyalarını toplamak ve bootstrap yapmak için otomatik olarak bu web sitelerinden birine bağlanır. I2P bu bootstrap sürecini "reseeding" olarak adlandırır.

- **Lookup ölçeklenebilirliği:**
  I2P ağında lookup'lar iteratif'tir, rekürsif değildir. Bir floodfill'den lookup başarısız olursa, lookup bir sonraki en yakın floodfill'e tekrarlanır. Floodfill, veri için başka bir floodfill'e rekürsif olarak sormaz. Iteratif lookup'lar büyük DHT ağlarına ölçeklenebilir.

---

### Taşıma Protokolleri

Router'lar arasındaki iletişim, harici saldırganlara karşı gizlilik ve bütünlük sağlarken, iletişim kurulan router'ın belirli bir mesajı alması gereken router olduğunu doğrulamalıdır. Router'ların diğer router'larla nasıl iletişim kurduğunun ayrıntıları kritik değildir — bu temel gereksinimleri sağlamak için farklı zamanlarda üç ayrı protokol kullanılmıştır.

I2P şu anda TCP üzerinden [NTCP2](/docs/specs/ntcp2/) ve UDP üzerinden [SSU2](/docs/specs/ssu2/) olmak üzere iki transport protokolünü desteklemektedir. Bunlar protokollerin önceki sürümleri olan [NTCP](/docs/legacy/ssu/) ve [SSU](/docs/legacy/ssu/)'yu değiştirmiştir ve bu eski sürümler artık kullanımdan kaldırılmıştır. Her iki protokol de hem IPv4 hem de IPv6'yı destekler. Hem TCP hem de UDP transport'larını destekleyerek, I2P kısıtlayıcı sansür rejimlerinde trafiği engellemek için tasarlanmış olanlar da dahil olmak üzere çoğu güvenlik duvarını etkili bir şekilde aşabilir. NTCP2 ve SSU2, modern şifreleme standartlarını kullanmak, trafik tanımlama direncini artırmak, verimlilik ve güvenliği artırmak ve NAT traversal'ı daha sağlam hale getirmek için tasarlanmıştır. Router'lar desteklenen her transport ve IP adresini ağ veritabanında yayınlar. Genel IPv4 ve IPv6 ağlarına erişimi olan router'lar genellikle NTCP2/SSU2'nin IPv4/IPv6 ile her kombinasyonu için birer tane olmak üzere dört adres yayınlar.

[SSU2](/docs/specs/ssu2/) SSU'nun hedeflerini destekler ve genişletir. SSU2'nin Wireguard ve QUIC gibi diğer modern UDP tabanlı protokollerle birçok benzerliği vardır. UDP üzerinden ağ mesajlarının güvenilir taşınmasına ek olarak, SSU2 eşler arası, işbirlikçi IP adresi tespiti, güvenlik duvarı tespiti ve NAT geçişi için özel olanaklar sağlar. [SSU özelliğinde](/docs/legacy/ssu/) açıklandığı gibi:

> Bu protokolün amacı, üçüncü taraflarca kolayca ayırt edilebilir olan minimum miktarda veriyi açığa çıkarırken, güvenli, kimlik doğrulamalı, yarı güvenilir ve sırasız mesaj teslimatı sağlamaktır. Yüksek dereceli iletişimi desteklemeli ve aynı zamanda TCP-dostu sıkışıklık kontrolü içermeli ve PMTU tespitini de içerebilir. Ev kullanıcıları için yeterli hızlarda toplu veriyi verimli bir şekilde taşıyabilme yeteneğine sahip olmalıdır. Ek olarak, çoğu NAT veya güvenlik duvarı gibi ağ engellerini ele alma tekniklerini desteklemelidir.

[NTCP2](/docs/specs/ntcp2/), NTCP'nin hedeflerini destekler ve genişletir. Modern şifreleme standartlarını kullanarak TCP üzerinden ağ mesajlarının verimli ve tamamen şifrelenmiş aktarımını ve trafik tanımlamaya karşı direnç sağlar.

I2P aynı anda birden fazla transport'u destekler. Giden bağlantı için belirli bir transport "teklifler" ile seçilir. Her transport bağlantı için teklif verir ve bu tekliflerin göreceli değeri önceliği belirler. Transport'lar, eşe (peer) zaten kurulmuş bir bağlantı olup olmamasına bağlı olarak farklı tekliflerle yanıt verebilir.

Bid (öncelik) değerleri implementasyona bağlıdır ve trafik koşulları, bağlantı sayıları ve diğer faktörlere göre değişebilir. Router'lar ayrıca gelen bağlantılar için transport tercihlerini network veritabanında her transport ve adres için transport "maliyetleri" olarak yayınlar.

---

### Kriptografi

I2P, şifreleme, kimlik doğrulama ve doğrulama için çeşitli protokol katmanlarında kriptografi kullanır. Başlıca protokol katmanları şunlardır: taşımalar, tunnel yapı mesajları, tunnel katmanı şifrelemesi, ağ veritabanı mesajları ve uçtan uca (garlic) mesajları. I2P'nin orijinal tasarımı, o zamanlar güvenli kabul edilen küçük bir kriptografik ilkel kümesi kullanıyordu. Bunlar arasında ElGamal asimetrik şifrelemesi, DSA-SHA1 imzaları, AES256/CBC simetrik şifreleme ve SHA-256 hash'leri bulunuyordu. Mevcut bilgi işlem gücü arttıkça ve kriptografik araştırmalar yıllar boyunca önemli ölçüde geliştikçe, I2P ilkellerini ve protokollerini yükseltmesi gerekiyordu. Bu nedenle, "şifreleme türleri" ve "imza türleri" konseptini ekledik ve protokollerimizi bu tanımlayıcıları içerecek ve desteği belirtecek şekilde genişlettik. Bu, geriye dönük uyumluluğu bozmadan veya ağ güncellemeleri için bir "bayrak günü" gerektirmeden, modern kriptografi için ağ desteğini periyodik olarak güncellememize ve genişletmemize, ayrıca ağı yeni ilkeller için gelecek güvenceli hale getirmemize olanak tanır. Bazı imza ve şifreleme türleri ayrıca deneysel kullanım için ayrılmıştır.

Çoğu protokol katmanında kullanılan mevcut ilkeller X25519 anahtar değişimi, EdDSA imzaları, ChaCha20/Poly1305 kimliği doğrulanmış simetrik şifreleme ve SHA-256 özet değerleridir. AES256 hala tunnel katmanı şifreleme için kullanılmaktadır. Bu modern protokoller ağ iletişiminin büyük çoğunluğu için kullanılır. ElGamal, ECDSA ve DSA-SHA1 dahil eski ilkeller, eski router'larla iletişim kurulurken geriye dönük uyumluluk için çoğu implementasyon tarafından desteklenmeye devam etmektedir. Bazı eski protokoller kullanımdan kaldırılmış ve/veya tamamen kaldırılmıştır. Yakın gelecekte sağlam güvenlik standartlarımızı korumak için kuantum sonrası (PQ) veya hibrit-PQ şifreleme ve imzalara geçiş konusunda araştırma yapmaya başlayacağız.

Bu kriptografik temel unsurlar, I2P'nin çeşitli düşmanlara karşı katmanlı savunmalarını sağlamak için bir araya getirilir. En alt düzeyde, router'lar arası iletişim, aktarım katmanı güvenliği tarafından korunur. Aktarım katmanları üzerinden geçen [Tunnel](#tunnels) mesajları kendi katmanlı şifrelemelerine sahiptir. Çeşitli diğer mesajlar, aynı zamanda şifrelenmiş olan "garlic mesajları" içinde iletilir.

#### Garlic Messages

Garlic mesajları, "soğan" katmanlı şifrelemenin bir uzantısıdır ve tek bir mesajın içeriğinin birden fazla "karanfil" içermesine olanak tanır — kendi teslimat talimatları ile birlikte tam olarak oluşturulmuş mesajlar. Mesajlar, aksi takdirde bilgiye erişimi olmaması gereken bir peer üzerinden düz metin olarak geçecekleri durumlarda garlic mesajına sarılır — örneğin, bir router başka bir router'dan bir tunnel'da yer almasını istediğinde, isteği bir garlic içine sarar, bu garlic'i alıcı router'ın public key'i ile şifreler ve bir tunnel üzerinden iletir. Başka bir örnek, bir client'ın bir destinasyon'a mesaj göndermek istediği durumdur — gönderenin router'ı o veri mesajını (diğer bazı mesajlarla birlikte) bir garlic içine sarar, bu garlic'i alıcının leaseSet'inde yayınlanmış public key ile şifreler ve uygun tunnel'lar üzerinden iletir.

Şifreleme katmanının içindeki her karanfilin yanına eklenen "talimatlar", karanfilin yerel olarak, uzak bir router'a veya uzak bir router üzerindeki uzak bir tunnel'a iletilmesini talep etme yeteneğini içerir. Bu talimatlarda, bir eşin teslimatın belirli bir zamana veya koşulun karşılanmasına kadar geciktirilmesini talep etmesine olanak tanıyan alanlar bulunur, ancak [önemsiz olmayan gecikmeler](#variable-latency) devreye alınana kadar bu talepler yerine getirilmeyecektir. Garlic mesajlarını tunnel oluşturmadan herhangi bir sayıda hop üzerinden açıkça yönlendirmek veya hatta tunnel mesajlarını garlic mesajlarına sararak tunnel'daki bir sonraki hop'a teslim etmeden önce birkaç hop ileride yönlendirmek mümkündür, ancak bu teknikler mevcut uygulamada şu anda kullanılmamaktadır.

#### Oturum Etiketleri

Güvenilmez, sırasız, mesaj tabanlı bir sistem olan I2P, garlic mesajlarına veri gizliliği ve bütünlüğü sağlamak için asimetrik ve simetrik şifreleme algoritmalarının basit bir kombinasyonunu kullanır. Orijinal kombinasyon ElGamal/AES+SessionTags olarak adlandırılıyordu, ancak bu 2048bit ElGamal, AES256, SHA256 ve 32 baytlık nonce'ların basit kullanımını tanımlamak için aşırı ayrıntılı bir yoldur. Bu protokol hala desteklenirken, ağın çoğu yeni bir protokol olan ECIES-X25519-AEAD-Ratchet'e geçmiştir. Bu protokol X25519, ChaCha20/Poly1305 ve 32 baytlık nonce'ları oluşturmak için senkronize bir PRNG'yi birleştirir. Her iki protokol de aşağıda kısaca açıklanacaktır.

#### ElGamal/AES+SessionTags

Bir router başka bir router'a garlic mesajı şifrelemek istediğinde ilk kez, bir AES256 oturum anahtarı için anahtar materyalini ElGamal ile şifreler ve bu şifrelenmiş ElGamal bloğundan sonra AES256/CBC şifrelenmiş yükü ekler. Şifrelenmiş yükün yanı sıra, AES şifrelenmiş bölüm yük uzunluğunu, şifrelenmemiş yükün SHA256 hash'ini ve bir dizi "session tag" — rastgele 32 baytlık nonce'ları içerir. Gönderici bir sonraki sefer başka bir router'a garlic mesajı şifrelemek istediğinde, yeni bir oturum anahtarını ElGamal ile şifrelemek yerine, daha önce teslim edilmiş session tag'lerden birini seçer ve yükü daha önceki gibi AES ile şifreler, o session tag ile kullanılan oturum anahtarını kullanarak ve session tag'in kendisini öne ekleyerek. Bir router garlic şifrelenmiş mesaj aldığında, ilk 32 baytı kontrol ederek mevcut bir session tag ile eşleşip eşleşmediğini görür — eşleşiyorsa, mesajı basitçe AES ile çözer, ancak eşleşmiyorsa, ilk bloğu ElGamal ile çözer.

Her oturum etiketi yalnızca bir kez kullanılabilir, böylece dahili saldırganların farklı mesajları aynı router'lar arasında geçiyor diye gereksiz yere ilişkilendirmesi önlenir. ElGamal/AES+SessionTag şifreli mesaj gönderen taraf, etiketleri ne zaman ve kaç tane teslim edeceğini seçer ve alıcıyı bir dizi mesajı karşılayacak yeterli etiketle önceden stoklar. Garlic mesajları, küçük bir ek mesajı karanfil olarak paketleyerek (bir "teslim durumu mesajı") başarılı etiket teslimini tespit edebilir — garlic mesajı hedeflenen alıcıya ulaştığında ve başarıyla şifresi çözüldüğünde, bu küçük teslim durumu mesajı ortaya çıkan karanfillerden biridir ve alıcıya bu karanfili orijinal gönderene geri göndermesi için talimatlar içerir (tabii ki bir inbound tunnel aracılığıyla). Orijinal gönderen bu teslim durumu mesajını aldığında, garlic mesajında paketlenen oturum etiketlerinin başarıyla teslim edildiğini bilir.

Session tag'lerin kendileri çok kısa bir yaşam süresine sahiptir ve kullanılmazlarsa bu süre sonunda atılırlar. Ayrıca, her anahtar için depolanan miktar sınırlıdır, anahtarların sayısı da öyle - çok fazla gelirse, yeni veya eski mesajlar düşürülebilir. Gönderici, session tag'leri kullanan mesajların iletilip iletilmediğini takip eder ve yeterli iletişim yoksa, daha önce düzgün şekilde iletildiği varsayılan mesajları düşürebilir ve pahalı tam ElGamal şifrelemesine geri dönebilir.

#### ECIES-X25519-AEAD-Ratchet

ElGamal/AES+SessionTags birçok açıdan önemli ek yük gerektiriyordu. ElGamal oldukça yavaş olduğu için CPU kullanımı yüksekti. Büyük sayıda session tag'in önceden teslim edilmesi gerektiği ve ElGamal public key'lerin çok büyük olması nedeniyle bant genişliği aşırıydı. Büyük miktarlarda session tag saklama gereksinimi nedeniyle bellek kullanımı yüksekti. Güvenilirlik, kayıp session tag teslimatı nedeniyle engellenmişti.

ECIES-X25519-AEAD-Ratchet bu sorunları çözmek için tasarlandı. Anahtar değişimi için X25519 kullanılır. Doğrulanmış simetrik şifreleme için ChaCha20/Poly1305 kullanılır. Şifreleme anahtarları "çift ratchet" yapılır veya periyodik olarak döndürülür. Oturum etiketleri 32 bayttan 8 bayta düşürülür ve PRNG ile üretilir. Protokol, Signal ve WhatsApp'ta kullanılan signal protokolüyle birçok benzerlik gösterir. Bu protokol CPU, RAM ve bant genişliğinde önemli ölçüde daha düşük ek yük sağlar.

Oturum etiketleri, oturum etiketleri ve oturum anahtarları oluşturmak için oturumun her iki ucunda çalışan deterministik senkronize bir PRNG'den üretilir. PRNG, SHA-256 HMAC kullanan bir HKDF'dir ve X25519 DH sonucundan beslenmiştir. Oturum etiketleri hiçbir zaman önceden iletilmez; sadece mesajla birlikte dahil edilirler. Alıcı, oturum etiketi ile indekslenmiş sınırlı sayıda oturum anahtarı saklar. Gönderen herhangi bir oturum etiketi veya anahtarı saklamak zorunda değildir çünkü bunlar önceden gönderilmez; talep üzerine oluşturulabilirler. Bu PRNG'yi gönderen ve alıcı arasında yaklaşık olarak senkronize tutarak (alıcı sonraki örneğin 50 etiketin bir penceresini önceden hesaplar), periyodik olarak büyük sayıda etiketi paketleme ek yükü ortadan kaldırılır.

---

## Gelecek

I2P protokolleri cep telefonları dahil çoğu platformda verimlidir ve çoğu tehdit modeli için güvenlidir. Ancak, güçlü devlet destekli düşmanlarla karşılaşanların ihtiyaçlarını karşılamak ve sürekli gelişen kriptografik ilerlemeler ile sürekli artan bilgi işlem gücü tehditlerini karşılamak için daha fazla iyileştirme gerektiren birkaç alan vardır. İki olası özellik, kısıtlı rotalar ve değişken gecikme süresi, 2003 yılında jrandom tarafından önerilmişti. Bu özellikleri artık uygulamayı planlamasak da, aşağıda açıklanmıştır.

### Kısıtlı Rota İşlemi

I2P, işlevsel bir paket anahtarlı ağın üzerinde çalışacak şekilde tasarlanmış bir kaplama ağıdır ve anonimlik ile güvenlik sunmak için uçtan uca ilkesini kullanır. İnternet artık uçtan uca ilkesini tam anlamıyla benimsememekle birlikte (NAT kullanımı nedeniyle), I2P ağın önemli bir bölümünün erişilebilir olmasını gerektirir — kenar kısımlarda kısıtlı rotalar kullanarak çalışan bir dizi peer olabilir, ancak I2P çoğu peer'ın erişilemez olduğu dejeneratif durum için uygun bir yönlendirme algoritması içermez. Bununla birlikte, böyle bir algoritma kullanan bir ağın üzerinde çalışabilir.

Hangi eşlerin doğrudan erişilebilir olduğuna dair sınırlamaların bulunduğu kısıtlı rota işletimi, kısıtlı rotaların nasıl ele alındığına bağlı olarak birkaç farklı işlevsel ve anonimlik etkisine sahiptir. En temel düzeyde, kısıtlı rotalar bir eşin gelen bağlantılara izin vermeyen bir NAT veya güvenlik duvarının arkasında olması durumunda ortaya çıkar. Bu büyük ölçüde dağıtık delik açma işlemini taşıma katmanına entegre ederek ele alınmış, çoğu NAT ve güvenlik duvarının arkasındaki kişilerin herhangi bir yapılandırma olmaksızın istenmeyen bağlantılar alabilmesini sağlamıştır. Ancak bu, eşin IP adresinin ağ içindeki router'lara maruz kalmasını sınırlamaz, çünkü onlar basitçe yayınlanan introducer aracılığıyla eşle tanıştırılabilir.

Kısıtlı rotaların işlevsel yönetiminin ötesinde, kişinin IP adresinin maruziyetini sınırlamak için kullanılabilecek iki düzeyde kısıtlı işlem vardır — iletişim için router'a özgü tunnellar kullanmak ve 'istemci router'ları sunmak. İlki için, router'lar ya yeni bir tunnel havuzu oluşturabilir ya da keşif havuzlarını yeniden kullanabilir, bunların bazılarının gelen geçitlerini ulaşım adreslerinin yerine routerInfo'larının bir parçası olarak yayınlayabilir. Bir peer onlarla iletişime geçmek istediğinde, netDb'de bu tunnel geçitlerini görür ve ilgili mesajı yayınlanan tunnellardan biri aracılığıyla onlara gönderir. Kısıtlı rotanın arkasındaki peer yanıt vermek isterse, bunu ya doğrudan (IP'sini peer'e maruz bırakmaya istekliyse) ya da giden tunnelları aracılığıyla dolaylı olarak yapabilir. Peer'in doğrudan bağlantıları olan router'lar ona ulaşmak istediğinde (örneğin tunnel mesajlarını iletmek için), doğrudan bağlantılarını yayınlanan tunnel geçidi üzerinde önceliklendirir. 'İstemci router'ları kavramı, hiçbir router adresi yayınlamayarak kısıtlı rotayı genişletir. Böyle bir router'ın routerInfo'sunu netDb'de yayınlamasına bile gerek yoktur, sadece iletişime geçtiği peer'lere kendi imzaladığı routerInfo'yu sağlar (router'ın açık anahtarlarını geçirmek için gereklidir).

Kısıtlı rotalar arkasındaki kullanıcılar için ödünleşimler vardır, çünkü muhtemelen diğer kişilerin tunnel'larına daha az sıklıkta katılırlar ve bağlı oldukları router'lar normalde açığa çıkmayacak trafik desenlerini çıkarabilir. Öte yandan, bu maruz kalmanın maliyeti bir IP'nin kullanılabilir hale getirilmesinin maliyetinden azsa, bu değerli olabilir. Bu, tabii ki, kısıtlı rota arkasındaki router'ın iletişim kurduğu eşlerin düşman olmadığını varsayar — ya ağ bağlantı kurmak için düşman bir eş kullanma olasılığının yeterince küçük olacak kadar büyüktür, ya da güvenilir (ve belki de geçici) eşler kullanılır.

Kısıtlı rotalar karmaşıktır ve genel amaç büyük ölçüde terk edilmiştir. Birkaç ilgili iyileştirme, bunlara olan ihtiyacı büyük ölçüde azaltmıştır. Artık güvenlik duvarı portlarını otomatik olarak açmak için UPnP desteği sunuyoruz. Hem IPv4 hem de IPv6 destekliyoruz. SSU2, adres tespiti, güvenlik duvarı durumu belirleme ve işbirlikçi NAT delik delme özelliklerini iyileştirdi. SSU2, NTCP2 ve adres uyumluluğu kontrolleri, tunnel oluşturulmadan önce tunnel atlamalarının bağlanabilmesini sağlar. GeoIP ve ülke tanımlama, kısıtlayıcı güvenlik duvarlarına sahip ülkelerdeki eşlerden kaçınmamızı sağlar. Bu güvenlik duvarlarının arkasındaki "gizli" router'lar için destek geliştirildi. Bazı uygulamalar ayrıca Yggdrasil gibi overlay ağlardaki eşlere bağlantıları da destekler.

### Değişken Gecikme

I2P'nin ilk çabalarının büyük kısmı düşük gecikme iletişimi üzerine odaklanmış olsa da, başından beri değişken gecikme hizmetleri göz önünde bulundurularak tasarlanmıştır. En temel düzeyde, I2P üzerinde çalışan uygulamalar orta ve yüksek gecikmeli iletişimin anonimliğini sunabilir ve aynı zamanda trafik desenlerini düşük gecikmeli trafik ile karıştırabilir. Dahili olarak ise, I2P garlic encryption aracılığıyla kendi orta ve yüksek gecikmeli iletişimini sunabilir — mesajın belirli bir gecikmeden sonra, belirli bir zamanda, belirli sayıda mesaj geçtikten sonra veya başka bir karıştırma stratejisi ile gönderilmesi gerektiğini belirterek. Katmanlı şifreleme ile, yalnızca clove'un gecikme talebini açığa çıkardığı router mesajın yüksek gecikme gerektirdiğini bilir ve bu da trafiğin düşük gecikmeli trafik ile daha da karışmasına olanak tanır. İletim ön koşulu karşılandığında, clove'u tutan router (ki bu muhtemelen bir garlic mesajı olacaktır) onu talep edildiği gibi iletir — bir router'a, bir tunnel'a veya büyük ihtimalle uzak bir istemci hedefine.

Değişken gecikme süresi hizmetlerinin hedefi, bunu desteklemek için sakla-ve-ilet mekanizmaları için önemli kaynaklar gerektirir. Bu mekanizmalar i2p-bote gibi çeşitli mesajlaşma uygulamalarında desteklenebilir ve desteklenmektedir. Ağ seviyesinde, Freenet gibi alternatif ağlar bu hizmetleri sağlar. I2P router seviyesinde bu hedefi takip etmemeye karar verdik.

---

## Benzer Sistemler

I2P'nin mimarisi, mesaj odaklı ara katman yazılımı kavramları, DHT'lerin topolojisi, serbest rota mixnet'lerinin anonimliği ve kriptografisi ile paket anahtarlamalı ağların uyum kabiliyeti üzerine inşa edilmiştir. Değer, yeni kavramlar veya algoritmalardan değil, mevcut sistemlerin ve makalelerin araştırma sonuçlarını dikkatli bir mühendislikle birleştirmekten gelir. Hem teknik hem de işlevsel karşılaştırmalar için gözden geçirilmeye değer birkaç benzer çaba olsa da, burada özellikle ikisi öne çıkarılmıştır — Tor ve Freenet.

Ayrıca [Ağ Karşılaştırmaları Sayfası](/docs/overview/comparison/)'na bakın. Bu açıklamaların jrandom tarafından 2003 yılında yazıldığını ve şu anda doğru olmayabileceğini unutmayın.

### Tor

*[website](https://www.torproject.org/)*

İlk bakışta, Tor ve I2P birçok işlevsel ve anonimlik ile ilgili benzerliğe sahiptir. I2P'nin gelişimi Tor üzerindeki erken dönem çalışmalardan haberdar olmadan başlamış olsa da, orijinal onion routing ve ZKS çalışmalarının birçok dersi I2P'nin tasarımına entegre edilmiştir. Dizin sunucuları ile esasen güvenilir, merkezi bir sistem inşa etmek yerine, I2P her peer'ın diğer router'ları profilleme sorumluluğunu alarak mevcut kaynakları en iyi şekilde nasıl kullanacağını belirlediği kendi kendini organize eden bir ağ veritabanına sahiptir. Diğer önemli bir fark ise hem I2P hem de Tor katmanlı ve sıralı yollar (tunnel'lar ve circuit'ler/stream'ler) kullanmasına rağmen, I2P temelde paket anahtarlamalı bir ağ iken, Tor temelde devre anahtarlamalı bir ağdır, bu da I2P'nin tıkanıklık veya diğer ağ arızalarını şeffaf bir şekilde aşmasına, yedekli yollar çalıştırmasına ve verileri mevcut kaynaklar arasında yük dengelemesi yapmasına olanak tanır. Tor entegre outproxy keşfi ve seçimi sunarak kullanışlı outproxy işlevselliği sunarken, I2P bu tür uygulama katmanı kararlarını I2P üzerinde çalışan uygulamalara bırakır — aslında I2P, TCP benzeri streaming kütüphanesini bile uygulama katmanına dışsallaştırmış, geliştiricilerin farklı stratejilerle deneyim yapmalarına, alan spesifik bilgilerini kullanarak daha iyi performans sunmalarına olanak tanımıştır.

Anonimlik perspektifinden bakıldığında, temel ağlar karşılaştırıldığında çok benzerlik vardır. Ancak, birkaç temel fark bulunmaktadır. Dahili bir düşman veya çoğu harici düşmanla başa çıkarken, I2P'nin simplex tunnel'ları, akışların kendilerine bakılarak Tor'un duplex devrelerinin açığa çıkaracağından yarı kadar trafik verisi açığa çıkarır — bir HTTP istek ve yanıtı Tor'da aynı yolu izlerken, I2P'de istek oluşturan paketler bir veya daha fazla outbound tunnel üzerinden çıkar ve yanıtı oluşturan paketler bir veya daha fazla farklı inbound tunnel üzerinden geri gelir. I2P'nin peer seçimi ve sıralama stratejileri predecessor saldırılarını yeterince ele alırken, bidirectional tunnel'lara geçiş gerekli olursa, aynı router'lar boyunca bir inbound ve outbound tunnel inşa edebiliriz.

Tor'un teleskopik tunnel oluşturma yöntemini kullanmasında başka bir anonimlik sorunu ortaya çıkmaktadır, çünkü bir circuit'teki hücrelerin bir düşmanın node'undan geçerken basit paket sayımı ve zamanlama ölçümleri, düşmanın circuit içindeki konumu hakkında istatistiksel bilgi açığa çıkarır. I2P'nin tek yönlü tunnel oluşturması tek bir mesajla gerçekleştirilir böylece bu veri açığa çıkarılmaz. Bir tunnel içindeki konumu korumak önemlidir, çünkü aksi takdirde bir düşman güçlü predecessor, intersection ve trafik doğrulama saldırılarını gerçekleştirebilir.

Genel olarak, Tor ve I2P odaklandıkları alanlarda birbirlerini tamamlar — Tor yüksek hızlı anonim İnternet outproxy hizmeti sunmaya odaklanırken, I2P kendi başına merkezi olmayan dayanıklı bir ağ sunmaya odaklanır. Teorik olarak, her ikisi de her iki amaca ulaşmak için kullanılabilir, ancak sınırlı geliştirme kaynakları göz önüne alındığında, her ikisinin de güçlü ve zayıf yanları vardır. I2P geliştiricileri, Tor'u I2P'nin tasarımından yararlanacak şekilde değiştirmek için gerekli adımları düşünmüşlerdir, ancak kaynak kıtlığı altında Tor'un uygulanabilirliğine ilişkin endişeler, I2P'nin paket anahtarlama mimarisinin kıt kaynakları daha etkili bir şekilde kullanabileceğini öne sürmektedir.

### Freenet

*[website](http://www.freenetproject.org/)*

Freenet, I2P'nin tasarımının ilk aşamalarında büyük rol oynadı — ağ içinde tamamen bulunan canlı bir takma kimlikli topluluğun uygulanabilirliğine kanıt sağlayarak, outproxy'lerde bulunan tehlikelerin önlenebileceğini gösterdi. I2P'nin ilk tohumu, Freenet için bir değiştirme iletişim katmanı olarak başladı ve ölçeklenebilir, anonim ve güvenli noktadan noktaya iletişimin karmaşıklığını sansüre dayanıklı dağıtılmış veri deposunun karmaşıklığından ayırmaya çalıştı. Ancak zamanla, Freenet'in algoritmalarında bulunan bazı anonimlik ve ölçeklenebilirlik sorunları, I2P'nin odağının Freenet'in bir bileşeni olmaktan ziyade genel bir anonim iletişim katmanı sağlama konusunda kalması gerektiğini açık hale getirdi. Yıllar boyunca, Freenet geliştiricileri eski tasarımdaki zayıflıkları görmüş ve önemli anonimlik sunmak için bir "premix" katmanına ihtiyaç duyacaklarını öne sürmelerini sağlamıştır. Başka bir deyişle, Freenet'in I2P veya Tor gibi bir mixnet üzerinde çalışması gerekir; "istemci düğümler" mixnet aracılığıyla "sunucu düğümlere" veri talep eder ve yayınlar, sunucu düğümler de Freenet'in buluşsal dağıtılmış veri depolama algoritmalarına göre veriyi alır ve depolar.

Freenet'in işlevselliği I2P'nin işlevselliğini çok iyi tamamlar, çünkü Freenet doğal olarak orta ve yüksek gecikme sistemlerini işletmek için gerekli araçların çoğunu sağlarken, I2P doğal olarak yeterli anonimlik sunmak için uygun düşük gecikme mix ağını sağlar. Mixnet'i sansüre dirençli dağıtık veri deposundan ayırma mantığı hâlâ mühendislik, anonimlik, güvenlik ve kaynak tahsis perspektifinden açık görünüyor, bu nedenle umuyoruz ki Freenet ekibi bu yönde çabalarını sürdürür, eğer I2P veya Tor gibi mevcut mixnet'leri basitçe yeniden kullanmıyorsa (veya gerektiğinde geliştirmeye yardım etmiyorsa).

---

## Ek A: Uygulama Katmanı

I2P'nin kendisi gerçekten çok fazla bir şey yapmaz — sadece uzak hedeflere mesajlar gönderir ve yerel hedefleri hedefleyen mesajları alır — ilginç işlerin çoğu onun üzerindeki katmanlarda gerçekleşir. Kendi başına I2P, anonim ve güvenli bir IP katmanı olarak görülebilir ve paketlenmiş [streaming library](#streaming-library) de bunun üzerinde anonim ve güvenli bir TCP katmanının uygulaması olarak değerlendirilebilir. Bunun ötesinde, [I2PTunnel](#i2ptunnel) I2P ağına girmek veya çıkmak için genel bir TCP proxy sistemi sunar ve çeşitli ağ uygulamaları son kullanıcılar için ek işlevsellik sağlar.

### Akış Kütüphanesi

I2P streaming kütüphanesi, genel bir streaming arayüzü (TCP soketlerini yansıtan) olarak görülebilir ve implementasyon, I2P üzerindeki yüksek gecikmeyi hesaba katmak için çeşitli optimizasyonlarla birlikte bir [sliding window protocol](http://en.wikipedia.org/wiki/Sliding_Window_Protocol) destekler. Bireysel streamler maksimum paket boyutunu ve diğer seçenekleri ayarlayabilir, ancak 4KB sıkıştırılmış varsayılan değeri, kayıp mesajları yeniden iletmenin bant genişliği maliyetleri ile çoklu mesajların gecikmesi arasında makul bir denge gibi görünmektedir.

Ayrıca, sonraki mesajların nispeten yüksek maliyeti göz önünde bulundurularak, streaming kütüphanesinin mesajları planlama ve iletme protokolü, aktarılan bireysel mesajların mevcut olan tüm bilgiyi içermesine izin verecek şekilde optimize edilmiştir. Örneğin, streaming kütüphanesi üzerinden proxy edilen küçük bir HTTP işlemi tek bir gidiş-dönüşte tamamlanabilir — ilk mesaj bir SYN, FIN ve küçük yükü (tipik bir HTTP isteği sığar) birleştirir ve yanıt SYN, FIN, ACK ve küçük yükü (birçok HTTP yanıtı sığar) birleştirir. SYN/FIN/ACK'nin alındığını bildirmek için ek bir ACK iletilmesi gerekse de, yerel HTTP proxy tam yanıtı tarayıcıya anında iletebilir.

Bununla birlikte, genel olarak streaming kütüphanesi, kayan pencereleri, tıkanıklık kontrol algoritmaları (hem yavaş başlangıç hem de tıkanıklık kaçınması) ve genel paket davranışı (ACK, SYN, FIN, RST, vb.) ile TCP'nin bir soyutlamasına çok benzemektedir.

### Adlandırma Kütüphanesi ve Adres Defteri

*Daha fazla bilgi için [İsimlendirme ve Adres Defteri](/docs/overview/naming/) sayfasına bakın.*

*Geliştiren: mihi, Ragnarok*

I2P içindeki isimlendirme, olasılıkların tüm yelpazesinde savunucuları olan ve en başından beri sıkça tartışılan bir konu olmuştur. Ancak, I2P'nin güvenli iletişim ve merkezi olmayan işlem için doğasında bulunan talebi göz önüne alındığında, geleneksel DNS-tarzı isimlendirme sistemi açıkça uygun değildir, "çoğunluk kuralları" oylama sistemleri de öyle. Bunun yerine, I2P yerel bir isimden hedefe eşleme üzerinde çalışacak şekilde tasarlanmış genel bir isimlendirme kütüphanesi ve temel bir uygulama ile birlikte gelir, ayrıca "Address Book" adı verilen isteğe bağlı bir eklenti uygulaması da bulunur. Address book, güven ağı güdümlü, güvenli, dağıtık ve insanların okuyabileceği bir isimlendirme sistemidir; yalnızca tüm insan tarafından okunabilir isimlerin küresel olarak benzersiz olması çağrısını feda ederek sadece yerel benzersizliği zorunlu kılar. I2P'deki tüm mesajlar kriptografik olarak hedefleri tarafından adreslenirken, farklı insanlar farklı hedeflere atıfta bulunan "Alice" için yerel address book girişlerine sahip olabilirler. İnsanlar hâlâ güven ağlarında belirtilen emsallerin yayınlanmış address book'larını içe aktararak, üçüncü bir taraf aracılığıyla sağlanan girişleri ekleyerek veya (bazı insanlar ilk gelen ilk hizmet alır kayıt sistemi kullanarak bir dizi yayınlanmış address book organize ederse) bu address book'ları isim sunucuları olarak ele almayı seçerek geleneksel DNS'yi taklit ederek yeni isimleri keşfedebilirler.

I2P, DNS benzeri hizmetlerin kullanımını teşvik etmez, çünkü bir sitenin ele geçirilmesiyle verilen zarar çok büyük olabilir — ve güvensiz hedeflerin hiçbir değeri yoktur. DNSsec'in kendisi hala kayıt şirketlerine ve sertifika otoritelerine geri dönerken, I2P ile bir hedefe gönderilen istekler ele geçirilemez veya yanıt sahteleştirilemez, çünkü bunlar hedefin public key'leriyle şifrelenir ve bir hedefin kendisi sadece bir çift public key ve bir sertifikadan ibarettir. DNS tarzı sistemler ise arama yolundaki isim sunucularından herhangi birinin basit hizmet reddi ve sahteleştirme saldırıları düzenlemesine izin verir. Bazı merkezi sertifika otoritesi tarafından imzalandığı şekilde yanıtları doğrulayan bir sertifika eklemek, düşmanca isim sunucusu sorunlarının çoğunu çözebilir ancak tekrar saldırılarının yanı sıra düşmanca sertifika otoritesi saldırılarına da açık bırakır.

Oylama tarzı isimlendirme de tehlikelidir, özellikle anonim sistemlerde Sybil saldırılarının etkinliği göz önüne alındığında — saldırgan basitçe keyfi olarak yüksek sayıda peer oluşturabilir ve belirli bir ismi ele geçirmek için her biriyle "oy" verebilir. Kimliği ücretsiz olmaktan çıkarmak için proof-of-work yöntemleri kullanılabilir, ancak ağ büyüdükçe çevrimiçi oylama yapmak için herkesle iletişim kurmanın gerektirdiği yük uygulanamaz hale gelir veya tam ağ sorgulanmazsa farklı cevap kümeleriyle karşılaşılabilir.

Ancak İnternet'te olduğu gibi, I2P de bir adlandırma sisteminin tasarımını ve işleyişini (IP benzeri) iletişim katmanının dışında tutuyor. Paketlenmiş adlandırma kütüphanesi, alternatif adlandırma sistemlerinin takılabileceği basit bir servis sağlayıcı arabirimi içerir ve son kullanıcıların hangi tür adlandırma ödünleşimlerini tercih ettiklerini belirlemelerine olanak tanır.

### I2PTunnel

*Geliştirici: mihi*

I2PTunnel muhtemelen I2P'nin en popüler ve çok yönlü istemci uygulamasıdır ve I2P ağına hem giriş hem de çıkış yönünde genel proxy işlevselliği sağlar. I2PTunnel dört ayrı proxy uygulaması olarak görülebilir — gelen TCP bağlantılarını alan ve bunları belirli bir I2P destination'a ileten bir "client", HTTP proxy gibi davranan ve istekleri uygun I2P destination'a ileten (gerekirse naming service'i sorgulayarak) bir "httpclient" (diğer adıyla "eepproxy"), bir destination üzerinde gelen I2P streaming bağlantılarını alan ve bunları belirli bir TCP host+port'a ileten bir "server", ve HTTP istek ve yanıtlarını ayrıştırarak daha güvenli çalışmaya olanak tanıyan "server"ı genişleten bir "httpserver". Ek olarak bir "socksclient" uygulaması da vardır, ancak daha önce belirtilen nedenlerle kullanımı önerilmez.

I2P'nin kendisi bir outproxy ağı değildir — veriyi karışım ağına sokup çıkaran mix net'te bulunan anonimlik ve güvenlik kaygıları, I2P'nin tasarımını dış kaynaklara ihtiyaç duymadan kullanıcının gereksinimlerini karşılayabilen anonim bir ağ sağlamaya odaklanmış tutmuştur. Ancak, I2PTunnel "httpclient" uygulaması outproxy için bir kanca sunar — talep edilen hostname ".i2p" ile bitmiyorsa, kullanıcı tarafından sağlanan outproxy setinden rastgele bir hedef seçer ve isteği onlara iletir. Bu hedefler basitçe açıkça outproxy çalıştırmayı seçmiş gönüllüler tarafından işletilen I2PTunnel "server" örnekleridir — varsayılan olarak kimse outproxy değildir ve outproxy çalıştırmak otomatik olarak diğer insanlara sizin üzerinizden proxy yapmasını söylemez. Outproxy'lerin doğal zayıflıkları olsa da, I2P kullanımı için basit bir kavram kanıtı sunarlar ve bazı kullanıcılar için yeterli olabilecek bir tehdit modeli altında bazı işlevsellik sağlarlar.

I2PTunnel kullanımdaki uygulamaların çoğunu etkinleştirir. Bir web sunucusuna işaret eden "httpserver", herkesin kendi anonim web sitesini (veya "I2P Sitesi") çalıştırmasını sağlar — bu amaç için I2P ile birlikte bir web sunucusu paketlenir, ancak herhangi bir web sunucusu kullanılabilir. Herkes anonim olarak barındırılan IRC sunucularından birine işaret eden bir "client" çalıştırabilir; bu sunucuların her biri yerel IRCd'lerine işaret eden bir "server" çalıştırır ve IRCd'ler arasında kendi "client" tunnel'ları üzerinden iletişim kurar. Son kullanıcılar ayrıca [I2Pmail'in](#i2pmail--susimail) POP3 ve SMTP hedeflerine işaret eden "client" tunnel'larına sahiptir (bunlar da basitçe POP3 ve SMTP sunucularına işaret eden "server" örnekleridir), ayrıca I2P'nin CVS sunucusuna işaret eden "client" tunnel'ları da vardır ve bu da anonim geliştirmeye olanak tanır. Zaman zaman insanlar NNTP sunucusuna işaret eden "server" örneklerine erişmek için "client" proxy'leri bile çalıştırmışlardır.

### I2PSnark

*I2PSnark geliştiricileri: jrandom ve diğerleri, [mjw](http://www.klomp.org/mark/)'nin [Snark](http://www.klomp.org/snark/) istemcisinden porte edilmiştir*

I2P kurulumu ile birlikte gelen I2PSnark, çok torrent özellikli basit bir anonim BitTorrent istemcisi sunar ve tüm işlevselliği sade bir HTML web arayüzü üzerinden gösterir.

### I2Pmail / Susimail

*Geliştirenler: postman, susi23, mastiejaner*

I2Pmail bir uygulamadan ziyade bir hizmettir — postman, mastiejaner ile geliştirilen bir dizi bileşene erişen I2PTunnel örnekleri aracılığıyla POP3 ve SMTP hizmeti ile hem dahili hem de harici e-posta sunar ve insanların tercih ettikleri mail istemcilerini kullanarak takma ad altında mail gönderip almalarını sağlar. Ancak, çoğu mail istemci önemli ölçüde tanımlayıcı bilgi açığa çıkardığı için, I2P özellikle I2P'nin anonimlik ihtiyaçları göz önünde bulundurularak geliştirilmiş olan susi23'ün web tabanlı susimail istemcisini paketler. I2Pmail/mail.i2p hizmeti, hashcash destekli kotalarla şeffaf virüs filtreleme ve hizmet reddi koruması sunar. Ayrıca, her kullanıcı mail.i2p outproxy'leri üzerinden teslimat öncesi kendi toplu işlem stratejisini kontrol edebilir - bu proxy'ler mail.i2p SMTP ve POP3 sunucularından ayrıdır — hem outproxy'ler hem de inproxy'ler mail.i2p SMTP ve POP3 sunucularıyla I2P'nin kendisi üzerinden iletişim kurar, bu nedenle bu anonim olmayan konumların ele geçirilmesi kullanıcının mail hesaplarına veya aktivite desenlerine erişim sağlamaz.
