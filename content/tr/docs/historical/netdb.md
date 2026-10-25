---
title: "Ağ Veritabanı Tartışması"
description: "netDb için floodfill, Kademlia deneyleri ve gelecekteki ayarlamalar hakkında tarihsel notlar"
slug: "netdb"
aliases:
  - "/tr/docs/legacy/netdb"
  - "/tr/docs/legacy/netdb/"
  - "/tr/netdb_discussion"
  - "/tr/netdb_discussion/"
lastUpdated: "2008-03"
accurateFor: "0.7"
---

NOT: Aşağıdakiler netDb implementasyonunun tarihçesi hakkında bir tartışmadır ve güncel bilgi değildir. Mevcut dokümantasyon için [ana netDb sayfasına](/docs/overview/network-database) bakınız.

## Geçmiş {#status}

netDb, "floodfill" adı verilen basit bir teknikle dağıtılır. Uzun zaman önce, netDb ayrıca yedek algoritma olarak Kademlia DHT kullanıyordu. Ancak, uygulamamızda iyi çalışmadı ve 0.6.1.20 sürümünde tamamen devre dışı bırakıldı.

*(jrandom'ın eski Syndie'deki 26 Kasım 2005 tarihli gönderisinden uyarlanmıştır)*

Floodfill netDb gerçekten sadece basit ve belki geçici bir önlemdir, mümkün olan en basit algoritmayı kullanır - veriyi floodfill netDb'deki bir eşe gönder, 10 saniye bekle, netDb'den rastgele bir eş seç ve onlardan gönderilecek girdiyi iste, doğru ekleme / dağıtımını doğrula. Doğrulama eşi yanıt vermezse veya girdiyi yoksa, gönderen işlemi tekrarlar. Floodfill netDb'deki eş, floodfill netDb'de olmayan bir eşten netDb store aldığında, bunu floodfill netDb'deki tüm eşlere gönderir.

Bir noktada, Kademlia arama/depolama işlevselliği hala yerindeydi. Eşler, floodfill eşlerini netDb'ye katılmayan herhangi bir eşten her zaman her anahtara daha 'yakın' olarak kabul ediyordu. Floodfill eşleri herhangi bir nedenle başarısız olursa Kademlia netDb'ye geri dönüyorduk. Ancak, Kademlia daha sonra tamamen devre dışı bırakıldı (aşağıya bakın).

Daha yakın zamanda, Kademlia 2009 sonlarında kısmen yeniden tanıtıldı ve her floodfill router'ın saklaması gereken netdb boyutunu sınırlamanın bir yolu olarak kullanıldı.

### Floodfill Algoritmasının Tanıtımı

Floodfill, 0.6.0.4 sürümünde tanıtıldı ve Kademlia yedek algoritma olarak korundu.

*(jrandom'ın eski Syndie'deki yazılarından uyarlanmıştır, 26 Kasım 2005)*

Sık sık söylediğim gibi, belirli bir teknolojiye özellikle bağlı değilim - benim için önemli olan sonuç alacak şeydir. Son birkaç yıldır çeşitli netDb fikirler üzerinde çalışırken, son birkaç haftada karşılaştığımız sorunlar bunlardan bazılarını gündeme getirdi. Canlı ağda, netDb redundans faktörü 4 peer'e ayarlandığında (yani 4 peer'in aldığını doğrulayana kadar bir girdiyi yeni peer'lere göndermeye devam ettiğimiz anlamına gelir) ve peer başına timeout o peer'in ortalama yanıt süresinin 4 katına ayarlandığında, 4 peer'in store'u ACK'lamadan önce **hâlâ** ortalama 40-60 peer'e gönderim yapıyoruz. Bu da çıkması gereken mesaj sayısının 36-56 katı mesaj gönderildiği anlamına geliyor, her biri tunnel kullanarak ve böylece 2-4 bağlantıyı geçiyor. Dahası, bu değer büyük ölçüde çarpık, çünkü 'başarısız' store işleminde (60 saniye mesaj gönderdikten sonra 4'ten az kişinin mesajı ACK'ladığı anlamına gelir) gönderim yapılan ortalama peer sayısı 130-160 peer aralığındaydı.

Bu çılgınca, özellikle üzerinde sadece belki 250 peer'ı olan bir ağ için.

En basit cevap "tabii ki jrandom, bu bozuk. düzelt şunu" demek olurdu, ama bu sorunun özüne tam olarak değmiyor. Devam eden başka bir çabayla uyumlu olarak, muhtemelen kısıtlı rotalar nedeniyle önemli sayıda ağ sorununuz var - bazı diğer eş düğümlerle konuşamayan eş düğümler, genellikle NAT veya güvenlik duvarı sorunları nedeniyle. Diyelim ki, belirli bir netDb girişine en yakın K eş düğüm, netDb store mesajının onlara ulaşabildiği ama başka bir eş düğümün netDb lookup mesajının ulaşamadığı şekilde 'kısıtlı rota' arkasındaysa, o giriş esasen ulaşılamaz olurdu. Bu çizgileri biraz daha takip ederek ve bazı kısıtlı rotaların düşmanca niyetle oluşturulacağı gerçeğini göz önünde bulundurarak, uzun vadeli bir netDb çözümünü daha yakından incelemek zorunda kalacağımız açık.

Birkaç alternatif var, ancak özellikle bahsetmeye değer iki tanesi bulunuyor. İlki, tam ağın bir alt kümesini kullanarak netDb'yi bir Kademlia DHT olarak çalıştırmak, burada tüm bu eşler harici olarak erişilebilir durumda. NetDb'ye katılmayan eşler hala bu eşleri sorgular ancak istenmeyen netDb store veya lookup mesajları almazlar. NetDb'ye katılım hem kendi kendini seçen hem de kullanıcı tarafından elemeli olacak - router'lar routerInfo'larında katılmak isteyip istemediklerini belirten bir bayrak yayınlayıp yayınlamama konusunda seçim yaparken, her router hangi eşleri netDb'nin bir parçası olarak görmek istediğini seçer (bu bayrağı yayınlayan ancak hiçbir zaman yararlı veri vermeyen eşler göz ardı edilir, böylece netDb'den esasen elenmiş olurlar).

Başka bir alternatif ise geçmişten gelen DTSTTCPW (Mümkün Olan En Basit Şeyi Yap) zihniyetine dönüş - bir floodfill netDb, ancak yukarıdaki alternatif gibi, tam ağın sadece bir alt kümesini kullanarak. Bir kullanıcı floodfill netDb'ye bir giriş yayınlamak istediğinde, bunu katılımcı router'lardan birine gönderiyor, bir ACK bekliyor ve ardından 30 saniye sonra, düzgün dağıtıldığını doğrulamak için floodfill netDb'deki başka rastgele bir katılımcıyı sorgulıyor. Eğer dağıtıldıysa harika, eğer dağıtılmadıysa süreci tekrarlıyor. Bir floodfill router netDb store aldığında, hemen ACK gönderiyor ve netDb store'u bilinen tüm netDb eşlerine sıraya alıyor. Bir floodfill router netDb lookup aldığında, veriye sahipse onunla yanıtlıyor, ancak sahip değilse floodfill netDb'deki örneğin 20 diğer eşin hash'leriyle yanıtlıyor.

Ağ ekonomisi perspektifinden bakıldığında, floodfill netDb orijinal yayın netDb'sine oldukça benzerdir, ancak bir girdi yayınlamanın maliyeti yayıncı tarafından değil, çoğunlukla netDb'deki eşler tarafından karşılanır. Bunu biraz daha detaylandırıp netDb'yi kara kutu gibi ele aldığımızda, netDb'nin gerektirdiği toplam bant genişliğinin şu şekilde olduğunu görebiliriz:

```
recvKBps = N * (L + 1) * (1 + F) * (1 + R) * S / T
```
burada:

```
N = number of routers in the entire network
L = average number of client destinations on each router
    (+1 for the routerInfo)
F = tunnel failure percentage
R = tunnel rebuild period, as a fraction of the tunnel lifetime
S = average netDb entry size
T = tunnel lifetime
```
Birkaç değer girerek:

```
recvKBps = 1000 * (5 + 1) * (1 + 0.05) * (1 + 0.2) * 2KB / 10m
         = 25.2KBps
```
Bu da N ile doğrusal olarak ölçeklenir (100.000 eş durumunda, netDb toplam 2,5MBps'lik netDb depolama mesajlarını işleyebilmelidir, ya da 300 eş durumunda 7,6KBps).

floodfill netDb'de her netDb katılımcısı istemci tarafından üretilen netDb depolamalarının yalnızca küçük bir kısmını doğrudan alırken, sonunda tüm girişleri alacaklardır, bu nedenle tüm bağlantılarının tam recvKBps'yi işleyebilir olması gerekir. Buna karşılık, diğer eşleri senkronize tutmak için hepsinin `(recvKBps/sizeof(netDb)) * (sizeof(netDb)-1)` göndermesi gerekecektir.

Bir floodfill netDb, netDb işlemleri için tunnel yönlendirme veya hangi girdileri 'güvenli bir şekilde' yanıtlayabileceği konusunda özel bir seçim gerektirmez, çünkü temel varsayım hepsinin her şeyi depoladığıdır. Ayrıca, gereken netDb disk kullanımı ile ilgili olarak, modern herhangi bir makine için hala oldukça önemsizdir ve her 1000 peer için yaklaşık 11MB gerektirir `(N * (L + 1) * S)`.

Kademlia netDb bu sayıları azaltacak, ideal olarak bunları K çarpı M değerlerine getirecek; burada K = yedekleme faktörü ve M = netDb'deki router sayısı (örn. 5/100, 100.000 router'da 126KBps recvKBps ve 536MB veriyor). Ancak Kademlia netDb'nin dezavantajı, düşmanca bir ortamda güvenli işletimin artan karmaşıklığıdır.

Şu anda düşündüğüm şey, mevcut canlı ağımızda basitçe bir floodfill netDb implementasyonu ve dağıtımı yapmak, bunu kullanmak isteyen eş düğümlerin üye olarak işaretlenmiş diğer eş düğümleri seçip geleneksel Kademlia netDb eş düğümleri yerine onları sorgulamalarına izin vermek. Bu aşamada bant genişliği ve disk gereksinimleri yeterince önemsiz (7.6KBps ve 3MB disk alanı) ve bu netDb'yi tamamen hata ayıklama planından çıkaracak - ele alınması gereken kalan sorunlar netDb ile ilgisiz bir şeyden kaynaklanacak.

Floodfill netDb'nin bir parçası olduklarını söyleyen bayrağı yayınlamak için eşler nasıl seçilir? Başlangıçta, bu gelişmiş bir yapılandırma seçeneği olarak manuel olarak yapılabilir (router dış erişilebilirliğini doğrulayamıyorsa yok sayılır). Çok fazla eş bu bayrağı ayarlarsa, netDb katılımcıları hangilerini çıkaracaklarını nasıl seçer? Yine, başlangıçta bu gelişmiş bir yapılandırma seçeneği olarak manuel olarak yapılabilir (erişilemeyen eşler çıkarıldıktan sonra). NetDb bölünmesinden nasıl kaçınırız? Router'ların K rastgele netDb eşini sorgulayarak netDb'nin flood fill'i düzgün bir şekilde yaptığını doğrulamasıyla. NetDb'ye katılmayan router'lar tunnel açacak yeni router'ları nasıl keşfeder? Bu belki de netDb router'ının netDb'deki eşlerle değil, netDb dışındaki rastgele eşlerle yanıt vereceği özel bir netDb sorgusu göndererek yapılabilir.

I2P'nin netDb'si geleneksel yük taşıyan DHT'lerden çok farklıdır - yalnızca ağ meta verilerini taşır, gerçek yük verilerini taşımaz, bu nedenle floodfill algoritması kullanan bir netDb bile keyfi miktarda I2P Site/IRC/bt/mail/syndie/vb. verilerini sürdürebilir. I2P büyüdükçe bu yükü biraz daha dağıtmak için bazı optimizasyonlar bile yapabiliriz (belki de netDb katılımcıları arasında neyi paylaşmaları gerektiğini görmek için bloom filtrelerini geçirmek), ancak şimdilik çok daha basit bir çözümle idare edebileceğimiz görünüyor.

Derinlemesine incelemeye değer bir gerçek var - tüm leaseSet'lerin netDb'de yayınlanması gerekmez! Aslında çoğunun yayınlanmasına gerek yoktur - sadece istenmeyen mesajlar alacak hedefler (yani sunucular) için gereklidir. Bunun nedeni, bir hedeften diğerine gönderilen garlic wrapped mesajların zaten gönderenin leaseSet'ini paketlemesidir, böylece bu iki hedef arasındaki sonraki gönderme/alma işlemleri (kısa bir süre içinde) herhangi bir netDb etkinliği olmadan çalışır.

Bu denklemlere geri döndüğümüzde, L değerini 5'ten 0.1 gibi bir değere değiştirebiliriz (her 50 hedeften sadece 1'inin sunucu olduğunu varsayarak). Önceki denklemler ayrıca istemcilerden gelen sorguları yanıtlamak için gereken ağ yükünü de geçiştirdi, ancak bu oldukça değişken olsa da (kullanıcı etkinliğine bağlı olarak), yayınlama sıklığıyla karşılaştırıldığında çok önemsiz olması da oldukça muhtemeldir.

Her halükarda, hala sihir yok, ancak gereken bant genişliği/disk alanında yaklaşık 1/5 oranında güzel bir azalma var (muhtemelen daha sonra daha fazla olacak, routerInfo dağıtımının doğrudan eş kurulumunun bir parçası olarak mı yoksa sadece netDb aracılığıyla mı gittiğine bağlı olarak).

### Kademlia Algoritmasının Devre Dışı Bırakılması

Kademlia, 0.6.1.20 sürümünde tamamen devre dışı bırakıldı.

*(jrandom ile 11/07 tarihli IRC konuşmasından uyarlanmıştır)*

Kademlia, temel seviyenin sunamayacağı minimum bir hizmet seviyesi gerektiriyordu (bant genişliği, cpu), katmanlar eklendikten sonra bile (saf kad bu konuda saçma). Kademlia çalışmazdı. Güzel bir fikirdi, ancak düşmanca ve değişken bir ortam için uygun değildi.

### Mevcut Durum

NetDb, I2P ağında çok özel bir rol oynar ve algoritmalar bizim ihtiyaçlarımıza göre ayarlanmıştır. Bu aynı zamanda henüz karşılaşmadığımız ihtiyaçları ele alacak şekilde ayarlanmadığı anlamına da gelir. I2P şu anda oldukça küçüktür (birkaç yüz router). 3-5 floodfill router'ın ağdaki 10.000 düğümü idare edebileceğine dair bazı hesaplamalar yapılmıştı. NetDb uygulaması şu anda ihtiyaçlarımızı fazlasıyla karşılamaktadır, ancak ağ büyüdükçe muhtemelen daha fazla ayarlama ve hata düzeltme yapılacaktır.

### Hesaplamaların Güncellenmesi 03-2008

Mevcut sayılar:

```
recvKBps = N * (L + 1) * (1 + F) * (1 + R) * S / T
```
burada:

```
N = number of routers in the entire network
L = average number of client destinations on each router
    (+1 for the routerInfo)
F = tunnel failure percentage
R = tunnel rebuild period, as a fraction of the tunnel lifetime
S = average netDb entry size
T = tunnel lifetime
```
Varsayımlardaki değişiklikler:

- L şimdi yaklaşık .5, yukarıdaki .1'e kıyasla, i2psnark ve diğer uygulamaların popülerliği nedeniyle.
- F yaklaşık .33, ancak tunnel test etmedeki hatalar 0.6.1.33'te düzeltildi, bu yüzden çok daha iyi olacak.
- netDb yaklaşık 2/3 5K routerInfo ve 1/3 2K leaseSet olduğu için, S = 4K.
  RouterInfo boyutu 0.6.1.32 ve 0.6.1.33'te gereksiz istatistikleri kaldırdığımız için küçülüyor.
- R = tunnel inşa periyodu: 0.2 çok düşüktü - belki 0.7'ydi -
  ancak 0.6.1.32'deki inşa algoritması iyileştirmeleri ağ yükseltildikçe bunu yaklaşık 0.2'ye indirmeli.
  Şu anda ağın yarısı .30 veya daha eski sürümlerde olduğu için 0.5 diyelim.

```
recvKBps = 700 * (0.5 + 1) * (1 + 0.33) * (1 + 0.5) * 4KB / 10m
         ~= 28KBps
```
Bu sadece depoları hesaba katıyor - peki sorgular ne olacak?

### Kademlia Algoritmasının Dönüşü?

*(2 Ocak 2007 I2P toplantısından uyarlanmıştır)*

Kademlia netDb düzgün çalışmıyordu. Kalıcı olarak mı öldü yoksa geri gelecek mi? Eğer geri gelirse, Kademlia netDb'deki eşler ağdaki router'ların çok sınırlı bir alt kümesi olacaktır (temelde genişletilmiş sayıda floodfill eş, eğer/ne zaman floodfill eşleri yükü kaldıramaz hale gelirse). Ancak floodfill eşleri yükü kaldırabildiği sürece (ve yükü kaldırabilecek başka eşler eklenemediği sürece), bu gereksizdir.

### Floodfill'in Geleceği

*(jrandom ile 11/07 tarihli IRC konuşmasından uyarlanmıştır)*

İşte bir öneri: Kapasite sınıfı O otomatik olarak floodfill olsun. Hmm. Emin olmadığımız sürece, tüm O sınıfı router'lara karşı süslü bir DDoS yöntemi ile sonuçlanabiliriz. Durum tam da şu: yeterli erişilebilirlik sağlarken floodfill sayısını mümkün olduğunca az tutmak istiyoruz. netDb istekleri başarısız olduğunda/olursa, floodfill eş sayısını artırmamız gerekir, ancak şu an netDb fetch problemi olduğunun farkında değilim. Kayıtlarıma göre 33 "O" sınıfı eş var. 33, floodfill için /çok/ fazla.

Yani floodfill, o havuzdaki peer sayısı kesin olarak sınırlandırıldığında en iyi şekilde çalışır mı? Ve floodfill havuzunun boyutu, ağın kendisi kademeli olarak büyüse bile fazla büyümemeli mi? 3-5 floodfill peer'ı 10K router'ı kaldırabilir hatırladığım kadarıyla (eski syndie'de detayları açıklayan bir sürü sayı paylaşmıştım). Bu, özellikle opt-in olan node'lar diğerlerinden gelen verilere güvenemiyorsa, otomatik opt-in ile doldurmak zor bir gereklilik gibi görünüyor. örneğin "bakalım ilk 5'in içinde miyim" ve sadece kendileri hakkındaki verilere güvenebiliyorlar (örneğin "kesinlikle O sınıfıyım, 150 KB/s taşıyorum ve 123 gündür aktifim"). Ve ilk 5 de düşmanca. Temel olarak, tor directory server'ları ile aynı - güvenilir insanlar (yani geliştiriciler) tarafından seçiliyor. Evet, şu anda opt-in ile sömürülebilir, ama bu tespit etmek ve başa çıkmak açısından önemsiz olurdu. Sonunda, Kademlia'dan daha kullanışlı bir şeye ihtiyacımız olabilir ve sadece makul derecede yetenekli peer'ların bu şemaya katılmasını sağlayabiliriz. N sınıfı ve üstü, bir saldırganın hizmet reddine neden olma riskini bastıracak kadar büyük bir miktar olmalı, umarım. Ama o zaman floodfill'den farklı olması gerekir, devasa trafik yaratmayacak anlamda. Büyük miktar mı? DHT tabanlı netDb için? DHT tabanlı olması şart değil.

### Floodfill TODO Listesi {#todo}

NOT: Aşağıdaki bilgiler güncel değildir. Mevcut durum ve gelecekteki çalışmaların listesi için [ana netDb sayfasına](/docs/overview/network-database) bakınız.

Ağ 13 Mart 2008'de birkaç saat boyunca sadece bir floodfill'e düştü (yaklaşık 18:00 - 20:00 UTC) ve bu büyük sorunlara neden oldu.

0.6.1.33 sürümünde uygulanan iki değişiklik, floodfill eş kaldırma veya değişim döngüsünün neden olduğu kesintileri azaltmalıdır:

1. Her seferinde arama için kullanılan floodfill eşlerini rastgeleleştir.
   Bu, sonunda başarısız olanları geçmenizi sağlayacaktır.
   Bu değişiklik aynı zamanda bazen ff arama kodunu çıldırtan kötü bir hatayı da düzeltti.
2. Çalışır durumdaki floodfill eşlerini tercih et.
   Kod artık mümkünse kara listeye alınmış, başarısız olan veya yarım saattir
   haber alınmayan eşlerden kaçınıyor.

Bir fayda, bir I2P Site'a daha hızlı ilk bağlantıdır (yani önce leaseset'i almanız gerektiğinde). Arama zaman aşımı 10s'dir, dolayısıyla baştan çevrimdışı olan bir peer'a sormakla başlamazsanız, 10s tasarruf edebilirsiniz.

Bu değişikliklerde anonimlik açısından *bazı* sonuçlar *olabilir*. Örneğin, floodfill **store** kodunda, kara listeye alınmış eşlerin (shitlisted peers) kaçınılmadığına dair yorumlar bulunuyor, çünkü bir eş "kötü" olabilir ve sonra ne olduğunu görebilir. Aramalar, depolamalardan çok daha az savunmasızdır - çok daha az sıklıkta gerçekleşir ve daha az bilgi verir. Yani belki de bu konuda endişelenmemiz gerekmediğini düşünüyoruz? Ancak değişiklikleri ayarlamak istersek, "çevrimdışı" olarak listelenen veya kara listeye alınmış bir eşe göndermeyi kolayca yapabiliriz, sadece gönderdiğimiz 2 eşin parçası olarak saymayız (gerçekten bir yanıt beklemediğimiz için).

Bir floodfill eşinin seçildiği birkaç yer vardır - bu düzeltme yalnızca birini ele alır - normal bir eşin [aynı anda 2] kimden arama yaptığı. Daha iyi floodfill seçiminin uygulanması gereken diğer yerler:

1. Normal bir peer'ın hangi peer'a sakladığı [aynı anda 1 tane]
   (rastgele - niteleme eklenmesi gerekiyor, çünkü zaman aşımları uzun)
2. Normal bir peer'ın bir saklama işlemini doğrulamak için hangi peer'a arama yaptığı [aynı anda 1 tane]
   (rastgele - niteleme eklenmesi gerekiyor, çünkü zaman aşımları uzun)
3. Bir floodfill peer'ın başarısız bir aramaya yanıt olarak gönderdiği peer'lar (aramaya en yakın 3 tanesi)
4. Bir floodfill peer'ın flood yaptığı peer'lar (diğer tüm floodfill peer'lar)
5. NTCP her 6 saatlik "fısıltı"da gönderilen floodfill peer'ların listesi
   (diğer floodfill iyileştirmeleri nedeniyle bu artık gerekli olmayabilir)

Yapılabilecek ve yapılması gereken daha pek çok şey var:

- Bir floodfill eşinin entegrasyonunu daha iyi değerlendirmek için "dbHistory" istatistiklerini kullan
- Yanıt vermeyen floodfill eşlere anında tepki vermek için "dbHistory" istatistiklerini kullan
- Yeniden denemelerde daha akıllı ol - yeniden denemeler üst katman tarafından işlenir, FloodOnlySearchJob'da değil, böylece başka bir rastgele sıralama yapar ve az önce denediğimiz ff eşlerini kasıtlı olarak atlama yerine tekrar dener.
- Entegrasyon istatistiklerini daha fazla iyileştir
- netDb'de sadece floodfill göstergesi yerine entegrasyon istatistiklerini gerçekten kullan
- Gecikme istatistikleri de kullanılsın mı?
- Başarısız floodfill eşlerini tanımada daha fazla iyileştirme

Son tamamlanan:

- [Release 0.6.3'te]
  Ağ analizine dayalı olarak, sınıf O eşlerin belirli bir yüzdesi için
  floodfill'e otomatik katılımı uygula.
- [Release 0.6.3'te]
  floodfill trafiğini azaltmak için netDb giriş boyutunu küçültmeye devam et -
  artık ağı izlemek için gerekli minimum istatistik sayısındayız.
- [Release 0.6.3'te]
  Hariç tutulacak floodfill eşlerin manuel listesi
  (router kimliğine göre [engelleme listeleri](/docs/overview/threat-model#blocklist))
- [Release 0.6.3'te]
  Depolar için daha iyi floodfill eş seçimi:
  netDb'si eski olan, yakın zamanda başarısız depo işlemi olan
  veya kalıcı olarak kara listeye alınmış eşlerden kaçın.
- [Release 0.6.4'te]
  floodfill eşlere doğrudan bağlantı sayısını azaltmak için,
  RouterInfo depoları için zaten bağlı olan floodfill eşleri tercih et.
- [Release 0.6.5'te]
  Artık floodfill olmayan eşler, sorgu yapan router'ın
  artık floodfill olmadığını bilmesi için
  bir sorguya yanıt olarak routerInfo'larını gönderirler.
- [Release 0.6.5'te]
  Otomatik olarak floodfill olma gereksinimlerinin daha fazla ayarlanması
- [Release 0.6.5'te]
  Hızlı floodfill'leri kayırmaya hazırlık olarak yanıt süresi profillemeyi düzelt
- [Release 0.6.5'te]
  Engelleme listesi oluşturmayı iyileştir
- [Release 0.7'de]
  netDb keşfini düzelt
- [Release 0.7'de]
  Engelleme listesi oluşturmayı varsayılan olarak aç, bilinen sorun çıkaranları engelle
- [Son sürümlerde birkaç iyileştirme, devam eden bir çaba]
  Yüksek bant genişliği ve floodfill router'lar üzerindeki kaynak taleplerini azalt

Bu uzun bir liste ama birçok eşin floodfill anahtarını açıp kapatmasından veya floodfill router gibi davranmasından kaynaklanan DOS saldırılarına dayanıklı bir ağa sahip olmak için bu kadar çalışma gerekecek. İki tane ff router'ımız olduğunda ve ikisi de 7/24 çalıştığında bunların hiçbiri sorun değildi. Yine, jrandom'ın yokluğu bize geliştirilmesi gereken yerleri gösterdi.

Bu çabaya yardımcı olmak için, floodfill eşler için ek profil verileri artık (0.6.1.33 sürümünden itibaren) router konsolundaki "Profiller" sayfasında görüntülenmektedir. Bunu floodfill eşlerini derecelendirmek için hangi verilerin uygun olduğunu analiz etmek amacıyla kullanacağız.

Ağ şu anda oldukça dayanıklı durumda, ancak floodfill eşlerinin performansını ve güvenilirliğini ölçme ve bunlara tepki verme algoritmalarımızı geliştirmeye devam edeceğiz. Şu anda kötü niyetli floodfill'lerin veya bir floodfill DDOS'unun potansiyel tehditlerine karşı tam olarak sağlamlaştırılmış olmamamıza rağmen, altyapının çoğu yerinde ve gerektiğinde hızlıca tepki verebilecek iyi bir konumdayız.
