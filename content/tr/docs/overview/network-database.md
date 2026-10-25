---
title: "Ağ Veritabanı"
description: "I2P'nin dağıtık ağ veritabanını (netDb) anlama - router iletişim bilgileri ve hedef aramaları için özelleştirilmiş bir DHT"
slug: "network-database"
aliases:
  - "/tr/how_networkdatabase"
  - "/tr/how_networkdatabase/"
lastUpdated: "2025-03"
accurateFor: "0.9.65"
---

## Genel Bakış

I2P'nin netDb'si, yalnızca iki tür veri içeren özelleşmiş bir dağıtılmış veritabanıdır - router iletişim bilgileri (**RouterInfos**) ve hedef iletişim bilgileri (**LeaseSets**). Her veri parçası uygun taraf tarafından imzalanır ve onu kullanan veya depolayan herkes tarafından doğrulanır. Ayrıca, veriler içinde canlılık bilgileri bulunur, bu da alakasız girişlerin atılmasına, yeni girişlerin eskilerin yerini almasına ve belirli saldırı sınıflarına karşı korunmaya olanak tanır.

netDb, tüm router'ların bir alt kümesi olan "floodfill router'lar"ın dağıtılmış veritabanını sürdürdüğü "floodfill" adı verilen basit bir teknikle dağıtılır.

---

## RouterInfo

Bir I2P router başka bir router ile iletişim kurmak istediğinde, bazı önemli veri parçalarını bilmesi gerekir - bunların tümü router tarafından paketlenir ve "RouterInfo" adı verilen bir yapıya imzalanır, bu yapı router'ın kimliğinin SHA256'sı anahtar olarak kullanılarak dağıtılır. Yapının kendisi şunları içerir:

- Router'ın kimliği (bir şifreleme anahtarı, bir imzalama anahtarı ve bir sertifika)
- Ulaşılabileceği iletişim adresleri
- Bunun ne zaman yayınlandığı
- Bir dizi rastgele metin seçeneği
- Yukarıdakilerin imzası, kimliğin imzalama anahtarı tarafından oluşturulmuş

### Beklenen Seçenekler

Aşağıdaki metin seçenekleri kesinlikle gerekli olmamakla birlikte, mevcut olmaları beklenmektedir:

- **caps** (Yetenek bayrakları - floodfill katılımını, yaklaşık bant genişliğini ve algılanan erişilebilirliği belirtmek için kullanılır)
  - **D**: Orta tıkanıklık (0.9.58 sürümünden itibaren)
  - **E**: Yüksek tıkanıklık (0.9.58 sürümünden itibaren)
  - **f**: Floodfill
  - **G**: Tüm tunnel'ları reddediyor (0.9.58 sürümünden itibaren)
  - **H**: Gizli
  - **K**: 12 KBps'nin altında paylaşılan bant genişliği
  - **L**: 12 - 48 KBps paylaşılan bant genişliği (varsayılan)
  - **M**: 48 - 64 KBps paylaşılan bant genişliği
  - **N**: 64 - 128 KBps paylaşılan bant genişliği
  - **O**: 128 - 256 KBps paylaşılan bant genişliği
  - **P**: 256 - 2000 KBps paylaşılan bant genişliği (0.9.20 sürümünden itibaren, aşağıdaki nota bakın)
  - **R**: Erişilebilir
  - **U**: Erişilemeز
  - **X**: 2000 KBps'nin üzerinde paylaşılan bant genişliği (0.9.20 sürümünden itibaren, aşağıdaki nota bakın)

"Paylaşılan bant genişliği" == (paylaşım %) * min(gelen bw, giden bw)

Eski router'larla uyumluluk için, bir router birden fazla bant genişliği harfi yayınlayabilir, örneğin "PO".

Not: P ve X bant genişliği sınıfları arasındaki sınır 2000 veya 2048 KBps olabilir, uygulayıcının tercihine bağlıdır.

- **netId** = 2 (Temel ağ uyumluluğu - Bir router farklı netId'ye sahip bir eş ile iletişim kurmayı reddeder)
- **router.version** (Daha yeni özellikler ve mesajlarla uyumluluğu belirlemek için kullanılır)

R/U yetenekleri hakkında notlar: Bir router genellikle R veya U yeteneğini yayınlamalıdır, erişilebilirlik durumu şu anda bilinmiyorsa hariç. R, router'ın en az bir transport adresinde doğrudan erişilebilir olduğu anlamına gelir (tanıtıcı gerekli değil, güvenlik duvarı arkasında değil). U, router'ın HİÇBİR transport adresinde doğrudan erişilebilir OLMADIĞI anlamına gelir.

Kullanımdan kaldırılan seçenekler: - ~~coreVersion~~ (Hiç kullanılmadı, 0.9.24 sürümünde kaldırıldı) - ~~stat_uptime~~ = 90m (0.7.9 sürümünden beri kullanılmıyor, 0.9.24 sürümünde kaldırıldı)

Bu değerler diğer router'lar tarafından temel kararlar için kullanılır. Bu router'a bağlanmalı mıyız? Bu router üzerinden bir tunnel yönlendirmeye çalışmalı mıyız? Özellikle bant genişliği yetenek bayrağı, yalnızca router'ın tunnel yönlendirmesi için minimum eşiği karşılayıp karşılamadığını belirlemek için kullanılır. Minimum eşiğin üzerinde, ilan edilen bant genişliği router'da kullanıcı arayüzünde gösterim ve hata ayıklama ve ağ analizi dışında hiçbir yerde kullanılmaz veya güvenilmez.

Geçerli NetID numaraları:

| Kullanım | NetID Numarası |
|-------|--------------|
| Ayrılmış | 0 |
| Ayrılmış | 1 |
| Mevcut Ağ (varsayılan) | 2 |
| Ayrılmış Gelecek Ağları | 3 - 15 |
| Çatallanmalar ve Test Ağları | 16 - 254 |
| Ayrılmış | 255 |
### Ek Seçenekler

Ek metin seçenekleri, router'ın sağlığı hakkında az sayıda istatistik içerir ve bu istatistikler ağ performans analizi ve hata ayıklama için [stats.i2p](http://stats.i2p/) gibi siteler tarafından toplanır. Bu istatistikler, tunnel oluşturma başarı oranları gibi geliştiriciler için kritik olan verileri sağlarken, aynı zamanda bu verilerin açıklanmasından kaynaklanabilecek yan etkilerle bu tür verilere duyulan ihtiyacı dengeleyecek şekilde seçilmiştir. Mevcut istatistikler şunlarla sınırlıdır:

- Keşif tunnel'ı oluşturma başarı, reddetme ve zaman aşımı oranları
- 1 saatlik ortalama katılımcı tunnel sayısı

Bunlar isteğe bağlıdır, ancak dahil edilirse ağ genelindeki performans analizine yardımcı olur. API 0.9.58 sürümü itibarıyla, bu istatistikler aşağıdaki gibi basitleştirilmiş ve standartlaştırılmıştır:

- Seçenek anahtarları stat_(statisim).(statperiod) şeklindedir
- Seçenek değerleri ';' ile ayrılır
- Olay sayıları veya normalleştirilmiş yüzdeler için istatistikler 4. değeri kullanır; ilk üç değer kullanılmaz ancak mevcut olmalıdır
- Ortalama değerler için istatistikler 1. değeri kullanır ve ';' ayırıcısı gerekmez
- İstatistik analizinde tüm router'ların eşit ağırlıklandırılması ve ek anonimlik için, router'lar bu istatistikleri yalnızca bir saat veya daha fazla çalışma süresi sonrasında ve RI yayınlandığı her 16 defada bir kez dahil etmelidir.

Örnek:

```
stat_tunnel.buildExploratoryExpire.60m = 0;0;0;53.14
stat_tunnel.buildExploratoryReject.60m = 0;0;0;15.51
stat_tunnel.buildExploratorySuccess.60m = 0;0;0;31.35
stat_tunnel.participatingTunnels.60m = 289.20
```
Floodfill router'lar, ağ veritabanlarındaki giriş sayısı hakkında ek veriler yayınlayabilir. Bunlar isteğe bağlıdır, ancak dahil edildiklerinde ağ genelindeki performans analizine yardımcı olurlar.

Aşağıdaki iki seçenek, floodfill router'ların yayınladığı her RI'da bulunmalıdır:

- **netdb.knownLeaseSets**
- **netdb.knownRouters**

Örnek:

```
netdb.knownLeaseSets = 158
netdb.knownRouters = 11374
```
Yayınlanan veriler router'ın kullanıcı arayüzünde görülebilir, ancak diğer hiçbir router tarafından kullanılmaz veya güvenilmez.

### Aile Seçenekleri

0.9.24 sürümünden itibaren, router'lar aynı varlık tarafından işletilen bir "aile"nin parçası olduklarını beyan edebilirler. Aynı ailedeki birden fazla router tek bir tunnel'da kullanılmayacaktır.

Aile seçenekleri şunlardır:

- **family** (Aile adı)
- **family.key** Ailenin [Signing Public Key](/docs/specs/common-structures/#type_SigningPublicKey) imza türü kodu (ASCII rakamlarında) ':' ile birleştirilmiş ve base 64 formatında Signing Public Key ile birleştirilmiş
- **family.sig** ((UTF-8 formatında aile adı) ile (32 byte router hash) birleştirilmiş) imzasının base 64 formatı

### RouterInfo Son Kullanma Tarihi

RouterInfo'ların belirli bir son kullanma zamanı yoktur. Her router, RouterInfo aramalarının sıklığı ile bellek veya disk kullanımı arasında denge kurarak kendi yerel politikasını sürdürme özgürlüğüne sahiptir. Mevcut uygulamada, aşağıdaki genel politikalar bulunmaktadır:

- İlk çalışma saatinde hiçbir süre dolumu yoktur, çünkü kalıcı olarak saklanan veriler eski olabilir.
- 25 veya daha az RouterInfo varsa hiçbir süre dolumu yoktur.
- Yerel RouterInfo sayısı arttıkça, makul sayıda RouterInfo tutmaya çalışmak için süre dolumu zamanı kısalır. 120'den az router ile süre dolumu zamanı 72 saattir, 300 router ile süre dolumu zamanı yaklaşık 30 saattir.
- [SSU](/docs/legacy/ssu/) introducer içeren RouterInfo'lar yaklaşık bir saatte sona erer, çünkü introducer listesi yaklaşık o sürede sona erer.
- Floodfill'ler tüm yerel RouterInfo'lar için kısa süre dolumu zamanı (1 saat) kullanır, çünkü geçerli RouterInfo'lar kendilerine sık sık yeniden yayınlanacaktır.

### RouterInfo Kalıcı Depolama

RouterInfo'lar periyodik olarak diske yazılır böylece yeniden başlatma sonrasında kullanılabilir olurlar.

Uzun süre sona erme sürelerine sahip Meta LeaseSet'lerin kalıcı olarak saklanması arzu edilebilir. Bu uygulama bağımlıdır.

### Ayrıca Bakınız

- [RouterInfo spesifikasyonu](/docs/specs/common-structures/#struct_RouterInfo)
- [RouterInfo Javadoc](http://idk.i2p/javadoc-i2p/net/i2p/data/router/RouterInfo.html)

---

## LeaseSet

netDb'de dağıtılan ikinci veri parçası bir "LeaseSet"tir - belirli bir istemci hedefi için **tunnel giriş noktaları grupunu (leases)** belgeler. Bu leases'lerin her biri aşağıdaki bilgileri belirtir:

- Tunnel gateway router (kimliğini belirterek)
- Mesajların gönderileceği o router üzerindeki tunnel ID'si (4 baytlık bir sayı)
- Bu tunnel'ın ne zaman sona ereceği.

LeaseSet'in kendisi netDb'de destination'ın SHA256'sından türetilen anahtar altında saklanır. Sürüm 0.9.38 itibariyle Encrypted LeaseSet'ler (LS2) için bir istisna vardır. DHT anahtarı için tip byte'ı (3) ve ardından gelen blinded public key'in SHA256'sı kullanılır ve sonra her zamanki gibi döndürülür. Aşağıdaki Kademlia Closeness Metric bölümüne bakın.

Bu lease'lere ek olarak, LeaseSet şunları içerir:

- Hedefin kendisi (bir şifreleme anahtarı, bir imzalama anahtarı ve bir sertifika)
- Ek şifreleme genel anahtarı: garlic mesajlarının uçtan uca şifrelenmesi için kullanılır
- Ek imzalama genel anahtarı: LeaseSet iptal etme için amaçlanmıştır, ancak şu anda kullanılmamaktadır.
- Hedefin LeaseSet'i yayınladığından emin olmak için tüm LeaseSet verilerinin imzası.

- [Lease spesifikasyonu](/docs/specs/common-structures/#struct_Lease)
- [LeaseSet spesifikasyonu](/docs/specs/common-structures/#struct_LeaseSet)
- [Lease Javadoc](http://idk.i2p/javadoc-i2p/net/i2p/data/Lease.html)
- [LeaseSet Javadoc](http://idk.i2p/javadoc-i2p/net/i2p/data/LeaseSet.html)

0.9.38 sürümü itibariyle, üç yeni leaseSet türü tanımlanmıştır; LeaseSet2, MetaLeaseSet ve EncryptedLeaseSet. Aşağıya bakınız.

### Yayımlanmamış LeaseSet'ler

Yalnızca giden bağlantılar için kullanılan bir hedefin LeaseSet'i *yayımlanmamış*tır. Hiçbir zaman bir floodfill router'a yayımlanmak üzere gönderilmez. Web tarama ve IRC istemcileri gibi "İstemci" tünelleri yayımlanmamıştır. Sunucular, [I2NP depolama mesajları](#leaseset-storage-to-peers) sayesinde bu yayımlanmamış hedeflere hala mesaj gönderebilecektir.

### İptal Edilmiş LeaseSet'ler

Bir LeaseSet, sıfır lease içeren yeni bir LeaseSet yayınlanarak *iptal edilebilir*. İptaller, LeaseSet içindeki ek imzalama anahtarı tarafından imzalanmalıdır. İptaller tam olarak uygulanmamıştır ve pratik bir kullanımları olup olmadığı belirsizdir. Bu, söz konusu imzalama anahtarının planlanmış tek kullanımıdır, dolayısıyla şu anda kullanılmamaktadır.

### LeaseSet2 (LS2)

0.9.38 sürümünden itibaren, floodfill'ler yeni bir LeaseSet2 yapısını desteklemektedir. Bu yapı eski LeaseSet yapısına çok benzer ve aynı amaca hizmet eder. Yeni yapı, yeni şifreleme türlerini, çoklu şifreleme türlerini, seçenekleri, çevrimdışı imzalama anahtarlarını ve diğer özellikleri desteklemek için gereken esnekliği sağlar. Ayrıntılar için 123 numaralı öneriyi inceleyin.

### Meta LeaseSet (LS2)

0.9.38 sürümünden itibaren, floodfill'ler yeni bir Meta LeaseSet yapısını destekler. Bu yapı DHT'de ağaç benzeri bir yapı sağlayarak diğer LeaseSet'lere referans verir. Meta LeaseSet'leri kullanarak, bir site büyük çoklu ev sahibi hizmetler uygulayabilir; burada ortak bir hizmet sağlamak için birkaç farklı Destination kullanılır. Bir Meta LeaseSet'teki girişler Destination'lar veya diğer Meta LeaseSet'ler olabilir ve 18,2 saate kadar uzun süre geçerliliğe sahip olabilir. Bu özelliği kullanarak, ortak bir hizmet sunan yüzlerce veya binlerce Destination çalıştırabilmek mümkün olmalıdır. Ayrıntılar için 123 numaralı öneriye bakın.

### Şifrelenmiş LeaseSets (LS1)

Bu bölüm, sabit bir simetrik anahtar kullanarak LeaseSet'leri şifrelemenin eski, güvensiz yöntemini açıklar. Encrypted LeaseSet'lerin LS2 sürümü için aşağıya bakın.

*Şifrelenmiş* bir LeaseSet içinde, tüm Lease'ler ayrı bir anahtarla şifrelenir. Lease'ler yalnızca anahtara sahip olanlar tarafından çözülebilir ve dolayısıyla hedef yalnızca anahtara sahip olanlar tarafından iletişim kurulabilir. LeaseSet'in şifrelendiğine dair hiçbir bayrak veya doğrudan gösterge yoktur. Şifrelenmiş LeaseSet'ler yaygın olarak kullanılmaz ve şifrelenmiş LeaseSet'lerin kullanıcı arayüzü ve uygulamasının iyileştirilebilip iyileştirilemeyeceğinin araştırılması gelecekteki çalışmalar için bir konudur.

### Şifrelenmiş LeaseSets (LS2)

0.9.38 sürümü itibariyle, floodfill'ler yeni bir EncryptedLeaseSet yapısını desteklemektedir. Destination gizlidir ve floodfill'e yalnızca körleştirilmiş bir genel anahtar ve son kullanma tarihi görünür. Yalnızca tam Destination'a sahip olanlar yapıyı şifreleyebilir. Yapı, Destination'ın hash'ine değil, körleştirilmiş genel anahtarın hash'ine dayalı bir DHT konumunda depolanır. Ayrıntılar için 123 numaralı öneriyi inceleyin.

### LeaseSet Sona Erme Süresi

Normal leaseSet'ler için son kullanma tarihi, kira sürelerinin en geç sona erme zamanıdır. Yeni leaseSet2 veri yapıları için son kullanma tarihi başlıkta belirtilir. LeaseSet2 için son kullanma tarihi, kira sürelerinin en geç sona erme tarihiyle eşleşmelidir. EncryptedLeaseSet ve MetaLeaseSet için son kullanma tarihi değişebilir ve maksimum son kullanma süresi uygulanabilir, bu henüz belirlenmemiştir.

### LeaseSet Kalıcı Depolama

LeaseSet verilerinin kalıcı olarak depolanması gerekli değildir, çünkü çok hızlı bir şekilde sona ererler. Ancak, uzun sona erme süreleri olan EncryptedLeaseSet ve MetaLeaseSet verilerinin kalıcı olarak depolanması tavsiye edilebilir.

### Şifreleme Anahtarı Seçimi (LS2)

LeaseSet2 birden fazla şifreleme anahtarı içerebilir. Anahtarlar sunucu tercihine göre sıralanır, en çok tercih edilen ilk sıradadır. Varsayılan istemci davranışı, desteklenen şifreleme türüne sahip ilk anahtarı seçmektir. İstemciler, şifreleme desteği, göreli performans ve diğer faktörlere dayalı olarak başka seçim algoritmaları kullanabilir.

---

## Önyükleme

netDb merkezi olmayan bir yapıdadır, ancak entegrasyon sürecinin sizi bağlayabilmesi için en az bir eş referansına ihtiyacınız vardır. Bu, router'ınızı aktif bir eşin RouterInfo'su ile "yeniden tohumlaması" yoluyla gerçekleştirilir - özellikle, onların `routerInfo-$hash.dat` dosyasını alarak `netDb/` dizininizde saklamak suretiyle. Bu dosyaları size herhangi biri sağlayabilir - hatta kendi netDb dizininizi açığa çıkararak siz de başkalarına sağlayabilirsiniz. Süreci basitleştirmek için gönüllüler netDb dizinlerini (veya bir alt kümesini) normal (i2p olmayan) ağda yayınlar ve bu dizinlerin URL'leri I2P'de sabit kodlanmıştır. Router ilk kez başladığında, rastgele seçilen bu URL'lerden birinden otomatik olarak veri getirir.

---

## Floodfill

Floodfill netDb basit bir dağıtık depolama mekanizmasıdır. Depolama algoritması basittir: veriyi kendisini floodfill router olarak tanıtan en yakın eşe gönder. Floodfill netDb'deki eş, floodfill netDb'de olmayan bir eşten netDb store aldığında, bunu floodfill netDb-eşlerinin bir alt kümesine gönderir. Seçilen eşler, belirli bir anahtara ([XOR-metriği](#kademlia-closeness-metric)'ne göre) en yakın olanlardır.

Floodfill netDb'nin bir parçası olan kişilerin belirlenmesi önemsizdir - bu, her router'ın yayınlanan routerInfo'sunda bir yetenek olarak gösterilir.

Floodfill'ler merkezi bir otoriteye sahip değildir ve bir "konsensüs" oluşturmazlar - sadece basit bir DHT katmanı uygularlar.

### Floodfill Router Katılımı

Tor'dan farklı olarak, dizin sunucularının sabit kodlu ve güvenilir olduğu ve bilinen varlıklar tarafından işletildiği durumun aksine, I2P floodfill eş kümesinin üyeleri güvenilir olmak zorunda değildir ve zaman içinde değişir.

netDb'nin güvenilirliğini artırmak ve netDb trafiğinin router üzerindeki etkisini en aza indirmek için, floodfill yalnızca yüksek bant genişliği limitleriyle yapılandırılmış router'larda otomatik olarak etkinleştirilir. Yüksek bant genişliği limitli router'lar (varsayılan değer çok daha düşük olduğundan manuel olarak yapılandırılması gerekir) düşük gecikmeli bağlantılarda olduğu varsayılır ve 7/24 erişilebilir olma olasılıkları daha yüksektir. Bir floodfill router için mevcut minimum paylaşım bant genişliği 128 KByte/sn'dir.

Ayrıca, floodfill işlemi otomatik olarak etkinleştirilmeden önce router'ın sağlık için birkaç ek testi geçmesi gerekir (giden mesaj kuyruğu süresi, iş gecikmesi, vb.).

Mevcut otomatik katılım kuralları ile ağdaki router'ların yaklaşık %6'sı floodfill router'larıdır.

Bazı eşler manuel olarak floodfill olacak şekilde yapılandırılırken, diğerleri floodfill eş sayısı bir eşik değerinin altına düştüğünde otomatik olarak gönüllü olan yüksek bant genişlikli router'lardır. Bu, floodfill'lerin çoğunun veya tamamının bir saldırıya kaybedilmesinden kaynaklanan uzun vadeli ağ hasarını önler. Buna karşılık, çok fazla floodfill mevcut olduğunda bu eşler kendilerini floodfill olmaktan çıkarırlar.

### Floodfill Router Rolleri

Bir floodfill router'ının floodfill olmayan router'larınkine ek olan tek servisleri netDb store'larını kabul etmek ve netDb sorgularına yanıt vermektir. Genellikle yüksek bant genişliğine sahip oldukları için, çok sayıda tunnel'da yer alma (yani başkaları için "relay" olma) olasılıkları daha yüksektir, ancak bu doğrudan dağıtık veritabanı servisleriyle ilgili değildir.

---

## Kademlia Yakınlık Metriği

netDb, yakınlığı belirlemek için basit bir Kademlia-tarzı XOR metriği kullanır. Bir Kademlia anahtarı oluşturmak için RouterIdentity veya Destination'ın SHA256 hash'i hesaplanır. Bir istisna, 0.9.38 sürümünden itibaren Encrypted LeaseSet'ler (LS2) içindir. DHT anahtarı için tür byte'ı (3) ve ardından blinded public key'in SHA256'sı kullanılır ve sonra her zamanki gibi döndürülür.

Bu algoritmanın bir modifikasyonu [Sybil saldırıları](#sybil-attack-partial-keyspace) maliyetini artırmak için yapılır. Aranan veya saklanan anahtarın SHA256 hash'i yerine, 32-byte ikili arama anahtarının UTC tarihi ile birleştirilmiş hali olan 8-byte ASCII string yyyyAAgg formatında temsil edilen SHA256 hash'i alınır, yani SHA256(anahtar + yyyyAAgg). Bu "routing key" olarak adlandırılır ve her gün gece yarısı UTC'de değişir. Bu şekilde sadece arama anahtarı modifiye edilir, floodfill router hash'leri değil. DHT'nin günlük dönüşümü bazen "keyspace rotation" olarak adlandırılır, ancak kesin anlamda bir rotasyon değildir.

Routing anahtarları hiçbir I2NP mesajında ağ üzerinden gönderilmez, yalnızca mesafe belirlenmesi için yerel olarak kullanılır.

---

## Network Database Segmentasyonu - Alt Veritabanları

Geleneksel olarak Kademlia-tarzı DHT'ler, DHT'deki herhangi bir düğümde saklanan bilgilerin bağlantısızlığını korumakla ilgilenmez. Örneğin, bir bilgi parçası DHT'deki bir düğüme saklanabilir, ardından o düğümden koşulsuz olarak geri istenebilir. I2P içinde ve netDb kullanılırken durum böyle değildir, DHT'de saklanan bilgiler yalnızca bunu yapmanın "güvenli" olduğu belirli bilinen koşullar altında paylaşılabilir. Bu, kötü niyetli bir aktörün client tunnel'a bir store göndererek, sonra da client tunnel'ın şüpheli "Host"undan doğrudan geri isteyerek bir client tunnel'ı bir router ile ilişkilendirmeye çalışabileceği bir saldırı sınıfını önlemek içindir.

### Bölümleme Yapısı

I2P router'ları, birkaç koşul karşılandığı takdirde bu saldırı sınıfına karşı etkili savunmalar uygulayabilir. Bir netDb implementasyonu, bir veritabanı girişinin bir client tunnel üzerinden mi yoksa doğrudan mı alındığını takip edebilmelidir. Eğer client tunnel üzerinden alındıysa, client'ın yerel hedefini kullanarak hangi client tunnel üzerinden alındığını da takip etmelidir. Eğer giriş birden fazla client tunnel üzerinden alındıysa, netDb girişin gözlemlendiği tüm hedefleri takip etmelidir. Ayrıca bir girişin bir arama yanıtı olarak mı yoksa bir depolama olarak mı alındığını da takip etmelidir.

Hem Java hem de C++ implementasyonlarında, bu durum önce doğrudan aramalar ve floodfill işlemleri için tek bir "Ana" netDb kullanılarak gerçekleştirilir. Bu ana netDb, router bağlamında bulunur. Daha sonra, her istemciye kendi netDb sürümü verilir; bu, istemci tünellerine gönderilen veritabanı girişlerini yakalamak ve istemci tünellerinden gönderilen aramalara yanıt vermek için kullanılır. Bunlara "İstemci Ağ Veritabanları" veya "Alt Veritabanları" diyoruz ve bunlar istemci bağlamında bulunur. İstemci tarafından işletilen netDb yalnızca istemcinin yaşam süresi boyunca var olur ve sadece istemcinin tünelleriyle iletişim kurulan girişleri içerir. Bu, istemci tünellerine gönderilen girişlerin doğrudan router'a gönderilen girişlerle çakışmasını imkansız hale getirir.

Ayrıca, her netDb'nin bir veritabanı girişinin neden alındığını hatırlaması gerekir - hedeflerimizden birine gönderildiği için mi, yoksa bir arama işleminin parçası olarak tarafımızca talep edildiği için mi. Eğer bir veritabanı girişi store işlemi olarak alındıysa, yani başka bir router tarafından bize gönderildiyse, o zaman netDb başka bir router anahtarı aradığında bu giriş için isteklere yanıt vermelidir. Ancak, eğer bir sorguya yanıt olarak alındıysa, o zaman netDb girişin daha önce aynı hedefe store edilmiş olması durumunda yalnızca giriş için bir sorguya yanıt vermelidir. Bir client asla ana netDb'den bir giriş ile sorgulara yanıt vermemelidir, yalnızca kendi client ağ veritabanından yanıt vermelidir.

Bu stratejiler alınmalı ve birlikte kullanılmalıdır, böylece her ikisi de uygulanır. Birlikte kullanıldığında, netDb'yi "Bölümlendirir" ve saldırılara karşı güvenli hale getirir.

---

## Depolama, Doğrulama ve Arama Mekanizmaları

### RouterInfo Eşlere Depolama

Yerel RouterInfo içeren [I2NP](/docs/specs/i2np/) DatabaseStoreMessages, bir [NTCP](/docs/specs/ntcp2/) veya [SSU](/docs/specs/ssu2/) transport bağlantısının başlatılmasının bir parçası olarak eşler ile değiş tokuş edilir.

### Eşlere LeaseSet Depolama

Yerel LeaseSet içeren [I2NP](/docs/specs/i2np/) DatabaseStoreMessages, ilgili Destination'dan gelen normal trafik ile birlikte garlic encryption mesajı içinde paketlenerek eşler (peers) ile periyodik olarak değiştirilir. Bu, herhangi bir LeaseSet arama gereksinimi olmadan veya iletişim kuran Destination'ların LeaseSet yayınlamış olma zorunluluğu olmadan, ilk yanıtın ve sonraki yanıtların uygun bir Lease'e gönderilmesine olanak tanır.

### Floodfill Seçimi

DatabaseStoreMessage, saklanan RouterInfo veya LeaseSet için mevcut routing anahtarına en yakın olan floodfill'e gönderilmelidir. Şu anda, en yakın floodfill yerel veritabanında yapılan bir arama ile bulunmaktadır. O floodfill gerçekten en yakın olmasa bile, onu diğer birden fazla floodfill'e göndererek "daha yakına" yayacaktır. Bu, yüksek derecede hata toleransı sağlar.

Geleneksel Kademlia'da, bir eş DHT'ye bir öğeyi en yakın hedefe eklemeden önce "en yakını bul" araması yapardı. Doğrulama işlemi mevcut olmaları durumunda daha yakın floodfill'leri keşfetme eğiliminde olacağından, bir router düzenli olarak yayınladığı RouterInfo ve LeaseSet'ler için DHT "mahallesi" bilgisini hızla geliştirecektir. I2NP bir "en yakını bul" mesajı tanımlamasa da, gerekli hale gelirse, bir router DatabaseSearchReplyMessage'larda daha yakın eşler alınmayana kadar en az anlamlı biti çevrilmiş bir anahtar (yani key ^ 0x01) için basitçe yinelemeli bir arama yapabilir. Bu, daha uzak bir eşin netdb öğesine sahip olması durumunda bile gerçek en yakın eşin bulunmasını sağlar.

### RouterInfo'nun Floodfill'lere Depolanması

Bir router kendi RouterInfo'sunu doğrudan bir floodfill router'a bağlanarak ve ona sıfır olmayan bir Reply Token ile bir [I2NP](/docs/specs/i2np/) DatabaseStoreMessage göndererek yayınlar. Bu mesaj uçtan uca garlic encryption ile şifrelenmez, çünkü bu doğrudan bir bağlantıdır, dolayısıyla arada router yoktur (ve zaten bu veriyi gizlemeye gerek yoktur). Floodfill router, Message ID'si Reply Token'ın değerine ayarlanmış bir [I2NP](/docs/specs/i2np/) DeliveryStatusMessage ile yanıt verir.

Bazı durumlarda, bir router RouterInfo DatabaseStoreMessage'ını keşif tüneli üzerinden de gönderebilir; örneğin, bağlantı sınırları, bağlantı uyumsuzluğu veya gerçek IP'yi floodfill'den gizleme isteği nedeniyle. Floodfill, aşırı yüklenme zamanlarında veya diğer kriterlere dayanarak böyle bir depolama işlemini kabul etmeyebilir; RouterInfo'nun doğrudan olmayan şekilde depolanmasının yasal olup olmadığını açıkça belirlemek, daha fazla araştırma gerektiren bir konudur.

### LeaseSet'lerin Floodfill'lere Depolanması

LeaseSet'lerin depolanması RouterInfo'lara göre çok daha hassastır, çünkü bir router LeaseSet'in kendisiyle ilişkilendirilememesini sağlamaya dikkat etmelidir.

Bir router, yerel bir LeaseSet'i o Destination için bir giden istemci tüneli üzerinden sıfır olmayan bir Reply Token ile bir [I2NP](/docs/specs/i2np/) DatabaseStoreMessage göndererek yayınlar. Mesaj, tünelin giden uç noktasından mesajı gizlemek için Destination'ın Session Key Manager'ı kullanılarak uçtan uca garlic encryption ile şifrelenir. floodfill router, Message ID'si Reply Token değerine ayarlanmış bir [I2NP](/docs/specs/i2np/) DeliveryStatusMessage ile yanıt verir. Bu mesaj, istemcinin gelen tünellerinden birine geri gönderilir.

### Flooding

Herhangi bir router gibi, bir floodfill de LeaseSet veya RouterInfo'yu yerel olarak depolamadan önce doğrulamak için çeşitli kriterler kullanır. Bu kriterler uyarlanabilir olabilir ve mevcut yük, netDb boyutu ve diğer faktörler dahil olmak üzere mevcut koşullara bağımlı olabilir. Tüm doğrulama işlemleri flooding yapılmadan önce tamamlanmalıdır.

Bir floodfill router, yerel NetDb'sinde daha önce sakladığından daha yeni olan geçerli bir RouterInfo veya LeaseSet içeren bir DatabaseStoreMessage aldıktan sonra, bunu "flooda" eder. Bir NetDb girişini flood etmek için, NetDb girişinin routing key'ine en yakın olan birkaç (şu anda 3) floodfill router'ı arar. (Routing key, RouterIdentity veya Destination'ın SHA256 Hash'i ile tarih (yyyyMMdd) eklenerek oluşturulur.) Key'e en yakın olanlara flood ederek, kendisine en yakın olanlara değil, floodfill depolamanın doğru yere ulaşmasını sağlar, saklayan router routing key için DHT "komşuluğu" hakkında iyi bilgiye sahip olmasa bile.

Floodfill daha sonra bu eşlerin her birine doğrudan bağlanır ve sıfır Reply Token içeren bir [I2NP](/docs/specs/i2np/) DatabaseStoreMessage gönderir. Bu doğrudan bir bağlantı olduğu için mesaj uçtan uca garlic encryption ile şifrelenmez, çünkü araya giren router'lar yoktur (ve bu veriyi gizlemeye gerek de yoktur). Diğer router'lar Reply Token sıfır olduğu için yanıt vermez veya tekrar flood etmez.

Floodfill'ler tunnel'lar üzerinden flood yapmamalıdır; DatabaseStoreMessage doğrudan bağlantı üzerinden gönderilmelidir.

Floodfill'ler asla süresi dolmuş bir LeaseSet veya bir saatten daha uzun süre önce yayınlanmış bir RouterInfo flood etmemelidir.

### RouterInfo ve LeaseSet Arama

[I2NP](/docs/specs/i2np/) DatabaseLookupMessage, bir floodfill router'dan netDb girişi talep etmek için kullanılır. Aramalar, router'ın giden keşif tunnel'larından biri üzerinden gönderilir. Yanıtların, router'ın gelen keşif tunnel'larından biri üzerinden döndürülmesi belirtilir.

Sorgular genellikle istenen anahtara en yakın olan iki "iyi" (bağlantı başarısız olmayan) floodfill router'a paralel olarak gönderilir.

Anahtar floodfill router tarafından yerel olarak bulunursa, bir [I2NP](/docs/specs/i2np/) DatabaseStoreMessage ile yanıt verir. Anahtar floodfill router tarafından yerel olarak bulunamazsa, anahtara yakın diğer floodfill router'ların listesini içeren bir [I2NP](/docs/specs/i2np/) DatabaseSearchReplyMessage ile yanıt verir.

LeaseSet aramaları sürüm 0.9.5'ten itibaren uçtan uca garlic encryption ile şifrelenir. RouterInfo aramaları şifrelenmez ve bu nedenle istemci tunnel'ının giden uç noktası (OBEP) tarafından gözetlenmeye karşı savunmasızdır. Bu durum ElGamal şifrelemenin maliyetli olmasından kaynaklanır. RouterInfo arama şifrelemesi gelecekteki bir sürümde etkinleştirilebilir.

Sürüm 0.9.7 itibariyle, bir leaseSet aramasına verilen yanıtlar (bir DatabaseStoreMessage veya bir DatabaseSearchReplyMessage), aramaya oturum anahtarı ve etiket dahil edilerek şifrelenecektir. Bu, yanıtı yanıt tünelinin gelen ağ geçidinden (IBGW) gizler. RouterInfo aramalarına verilen yanıtlar, arama şifrelemesini etkinleştirirsek şifrelenecektir.

(Referans: [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf) Aşağıdaki italik terimler için Bölüm 2.2-2.3)

Ağın nispeten küçük boyutu ve flooding redundancy nedeniyle, aramalar genellikle O(log n) yerine O(1)'dir. Bir router, anahtara ilk denemede cevabı alacak kadar yakın bir floodfill router'ı bilme olasılığı yüksektir. 0.8.9 öncesi sürümlerde, router'lar iki arama redundancy kullanıyordu (yani, farklı peer'lara paralel olarak iki arama gerçekleştiriliyordu) ve aramalar için ne *recursive* ne de *iterative* routing uygulanmıştı. Sorgular *sorgu başarısızlığı şansını azaltmak* için *aynı anda birden fazla rota üzerinden* gönderiliyordu.

0.8.9 sürümünden itibaren, *yinelemeli arama*lar arama fazlalığı olmaksızın uygulanmaktadır. Bu, tüm floodfill eşleri bilinmediğinde çok daha iyi çalışacak daha verimli ve güvenilir bir arama yöntemidir ve ağ büyümesi için ciddi bir kısıtlamayı ortadan kaldırır. Ağ büyüdükçe ve her router yalnızca floodfill eşlerinin küçük bir alt kümesini tanıdıkça, aramalar O(log n) olacaktır. Eş, anahtara daha yakın referanslar döndürmese bile, ek sağlamlık için ve kötü niyetli bir floodfill'in anahtar alanının bir kısmını kara deliğe çevirmesini önlemek için arama bir sonraki en yakın eş ile devam eder. Aramalar, toplam arama zaman aşımına ulaşılana veya maksimum eş sayısı sorgulanana kadar devam eder.

*Node ID'ler* *doğrulanabilir* çünkü router hash'ini hem node ID hem de Kademlia anahtarı olarak doğrudan kullanırız. Arama anahtarına daha yakın olmayan yanlış yanıtlar genellikle göz ardı edilir. Ağın mevcut boyutu göz önüne alındığında, bir router *hedef ID alanının komşuluğu hakkında ayrıntılı bilgiye* sahiptir.

### RouterInfo Depolama Doğrulaması

Not: RouterInfo doğrulaması, [Practical Attacks Against the I2P Network](http://wwwcip.informatik.uni-erlangen.de/~spjsschl/i2p.pdf) makalesinde açıklanan saldırıyı önlemek amacıyla 0.9.7.1 sürümünden itibaren devre dışı bırakılmıştır. Doğrulamanın güvenli bir şekilde yapılabilecek şekilde yeniden tasarlanabilip tasarlanamayacağı belirsizdir.

Bir depolamanın başarılı olduğunu doğrulamak için, router basitçe yaklaşık 10 saniye bekler, sonra anahtara yakın başka bir floodfill router'a (ancak depolamanın gönderildiği router değil) bir arama gönderir. Aramalar router'ın giden keşif tunnel'larından biri üzerinden gönderilir. Aramalar, giden uç nokta (OBEP) tarafından gizlice dinlemeyi önlemek için uçtan uca garlic encryption ile şifrelenir.

### LeaseSet Depolama Doğrulaması

Bir depolamanın başarılı olduğunu doğrulamak için, bir router basitçe yaklaşık 10 saniye bekler, ardından anahtara yakın başka bir floodfill router'a (ancak depolamanın gönderildiği router'a değil) bir arama gönderir. Aramalar, doğrulanmakta olan LeaseSet'in hedefi için giden istemci tunnel'larından birinden gönderilir. Giden tunnel'ın OBEP'i tarafından gözetlemeyi önlemek için, aramalar uçtan uca garlic encryption ile şifrelenir. Yanıtların istemcinin gelen tunnel'larından biri üzerinden dönmesi belirtilir.

0.9.7 sürümünden itibaren, hem RouterInfo hem de LeaseSet aramaları için gelen yanıtlar (bir DatabaseStoreMessage veya bir DatabaseSearchReplyMessage) şifrelenecektir, böylece yanıt reply tunnel'ının gelen ağ geçidinden (IBGW) gizlenecektir.

### Keşif

*Exploration*, bir router'ın yeni router'lar hakkında bilgi edinmeye çalıştığı özel bir netDb arama biçimidir. Bunu, bir floodfill router'ına rastgele bir anahtarı arayan bir [I2NP](/docs/specs/i2np/) DatabaseLookup Mesajı göndererek yapar. Bu arama başarısız olacağından, floodfill normalde anahtara yakın floodfill router'larının hash'lerini içeren bir [I2NP](/docs/specs/i2np/) DatabaseSearchReplyMessage ile yanıt verir. Bu yararlı olmaz, çünkü istekte bulunan router muhtemelen bu floodfill'leri zaten bilmektedir ve tüm floodfill router'larını DatabaseLookup Mesajının "dahil etme" alanına eklemek pratik olmaz. Bir exploration sorgusu için, istekte bulunan router DatabaseLookup Mesajında özel bir bayrak ayarlar. floodfill daha sonra yalnızca istenen anahtara yakın olan floodfill olmayan router'larla yanıt verir.

### Arama Yanıtları Üzerine Notlar

Arama isteğine verilen yanıt ya bir Database Store Message (başarı durumunda) ya da bir Database Search Reply Message (başarısızlık durumunda) olur. DSRM, yanıtın kaynağını belirtmek için bir 'from' router hash alanı içerir; DSM içermez. DSRM 'from' alanı doğrulanmamıştır ve sahte veya geçersiz olabilir. Başka yanıt etiketleri yoktur. Bu nedenle, paralel olarak birden fazla istek yapılırken, çeşitli floodfill router'ların performansını izlemek zordur.

---

## MultiHoming

Hedefler, aynı özel ve genel anahtarları kullanarak (geleneksel olarak eepPriv.dat dosyalarında saklanır) aynı anda birden fazla router üzerinde barındırılabilir. Her iki örnek de imzalanmış leaseSet'lerini periyodik olarak floodfill eşlerine yayınladığından, veritabanı araması talep eden bir eşe en son yayınlanan leaseSet döndürülür. LeaseSet'ler (en fazla) 10 dakikalık bir yaşam süresine sahip olduğundan, belirli bir örnek çökerse, kesinti en fazla 10 dakika sürer ve genellikle bundan çok daha kısadır. Çoklu barındırma işlevi doğrulanmış olup ağdaki birkaç hizmet tarafından kullanılmaktadır.

0.9.38 sürümü itibariyle, floodfill'ler yeni bir Meta LeaseSet yapısını desteklemektedir. Bu yapı, DHT'de diğer LeaseSet'lere referans vermek için ağaç benzeri bir yapı sağlar. Meta LeaseSet'leri kullanarak, bir site ortak bir hizmeti sağlamak için birkaç farklı Destination'ın kullanıldığı büyük çoklu bağlantılı hizmetler uygulayabilir. Bir Meta LeaseSet'teki girişler Destination'lar veya diğer Meta LeaseSet'ler olabilir ve 18.2 saate kadar uzun süre geçerliliğe sahip olabilirler. Bu özelliği kullanarak, ortak bir hizmeti barındıran yüzlerce veya binlerce Destination çalıştırmanın mümkün olması gerekir. Detaylar için 123 numaralı öneriye bakınız.

---

## Tehdit Analizi

Ayrıca [tehdit modeli sayfasında](/docs/overview/threat-model/#floodfill) da ele alınmıştır.

Düşmanca davranan bir kullanıcı, bir veya daha fazla floodfill router oluşturarak ve bunları kötü, yavaş veya hiç yanıt vermeyecek şekilde yapılandırarak ağa zarar vermeye çalışabilir. Aşağıda bazı senaryolar tartışılmaktadır.

### Büyüme Yoluyla Genel Azaltma

Şu anda ağda yaklaşık 1700 floodfill router bulunmaktadır. Aşağıdaki saldırıların çoğu, ağ boyutu ve floodfill router sayısı arttıkça daha zor hale gelecek veya daha az etkiye sahip olacaktır.

### Yedeklilik Yoluyla Genel Risk Azaltma

Flooding yoluyla, tüm netdb girişleri anahtara en yakın 3 floodfill router üzerinde saklanır.

### Sahtekarlıklar

Tüm netDb girdileri oluşturucuları tarafından imzalanır, bu nedenle hiçbir router sahte bir RouterInfo veya LeaseSet oluşturamaz.

### Yavaş veya Yanıt Vermeyen

Her router, her floodfill router için [peer profili](/docs/overview/peer-selection/) içinde genişletilmiş bir istatistik seti tutar ve bu peer için çeşitli kalite metriklerini kapsar. Bu set şunları içerir:

- Ortalama yanıt süresi
- İstenen veriyle yanıtlanan sorguların yüzdesi
- Başarıyla doğrulanan depolamaların yüzdesi
- Son başarılı depolama
- Son başarılı arama
- Son yanıt

Bir router hangi floodfill router'ın bir anahtara en yakın olduğunu belirlemesi gerektiğinde, hangi floodfill router'ların "iyi" olduğunu belirlemek için bu metrikleri kullanır. "İyiliği" belirlemek için kullanılan yöntemler ve eşikler nispeten yenidir ve daha fazla analiz ve iyileştirmeye tabidir. Tamamen yanıt vermeyen bir router hızlıca tespit edilip kaçınılacak olsa da, yalnızca bazen kötü niyetli olan router'larla başa çıkmak çok daha zor olabilir.

### Sybil Saldırısı (Tam Anahtar Alanı)

Bir saldırgan, keyspace boyunca dağılmış çok sayıda floodfill router oluşturarak bir [Sybil saldırısı](https://www.freehaven.net/anonbib/cache/sybil.pdf) gerçekleştirebilir.

(İlgili bir örnekte, bir araştırmacı yakın zamanda [çok sayıda Tor relay'i](http://blog.torproject.org/blog/june-2010-progress-report) oluşturdu.) Başarılı olursa, bu tüm ağa karşı etkili bir DOS saldırısı olabilir.

Eğer floodfill'ler yukarıda açıklanan eş profil metrikleri kullanılarak "kötü" olarak işaretlenecek kadar kötü davranmıyorlarsa, bu durumla başa çıkmak zor bir senaryodur. Tor'un yanıtı röle durumunda çok daha çevik olabilir, çünkü şüpheli röleler konsensüsten manuel olarak kaldırılabilir. I2P ağı için bazı olası yanıtlar aşağıda listelenmiştir, ancak hiçbiri tamamen tatmin edici değildir:

- Kötü router hash'leri veya IP'lerin bir listesini derleyin ve listeyi çeşitli yollarla duyurun (konsol haberleri, web sitesi, forum, vb.); kullanıcıların listeyi manuel olarak indirip yerel "kara listelerine" eklemeleri gerekir.
- Ağdaki herkesten floodfill'i manuel olarak etkinleştirmesini isteyin (Sybil'e daha fazla Sybil ile karşı koyun)
- Sabit kodlanmış "kötü" listeyi içeren yeni bir yazılım sürümü yayınlayın
- "Kötü" eşleri otomatik olarak tanımlamaya çalışarak eş profili metriklerini ve eşiklerini iyileştiren yeni bir yazılım sürümü yayınlayın.
- Tek bir IP bloğunda çok fazla floodfill varsa onları diskalifiye eden yazılım ekleyin
- Tek bir birey veya grup tarafından kontrol edilen otomatik abonelik tabanlı kara liste uygulayın. Bu, Tor "konsensüs" modelinin bir bölümünü etkili bir şekilde uygulayacaktır. Ne yazık ki bu aynı zamanda tek bir birey veya gruba ağda herhangi bir router veya IP'nin katılımını engelleme veya hatta tüm ağı tamamen kapatma veya yok etme gücü verecektir.

Bu saldırı, ağ boyutu büyüdükçe daha zor hale gelir.

### Sybil Saldırısı (Kısmi Anahtar Uzayı)

Bir saldırgan, keyspace içinde yakın bir şekilde kümelenmiş az sayıda (8-15) floodfill router oluşturarak ve bu routerlara ait RouterInfo'ları geniş çapta dağıtarak bir [Sybil saldırısı](https://www.freehaven.net/anonbib/cache/sybil.pdf) düzenleyebilir. Ardından, o keyspace içindeki bir anahtar için yapılan tüm aramalar ve depolamalar saldırganın routerlarından birine yönlendirilir. Başarılı olursa, bu örneğin belirli bir I2P Sitesine karşı etkili bir DOS saldırısı olabilir.

Anahtar alanı, anahtarın kriptografik (SHA256) Hash'i ile indekslendiği için, bir saldırgan anahtara yeterince yakın olan yeterli sayıda router hash'i elde edene kadar tekrar tekrar router hash'leri oluşturmak için kaba kuvvet yöntemi kullanmak zorundadır. Ağ boyutuna bağlı olan bunun için gereken hesaplama gücü miktarı bilinmemektedir.

Bu saldırıya karşı kısmi bir savunma olarak, Kademlia "yakınlığını" belirlemek için kullanılan algoritma zaman içinde değişir. Yakınlığı belirlemek için anahtarın Hash'ini (yani H(k)) kullanmak yerine, anahtarın mevcut tarih dizgisiyle eklenmiş halinin Hash'ini kullanırız, yani H(k + YYYYMMDD). "Routing key generator" adı verilen bir fonksiyon bunu yapar ve orijinal anahtarı bir "routing key"e dönüştürür. Başka bir deyişle, tüm netDb anahtar uzayı her gün UTC gece yarısında "döner". Herhangi bir kısmi-anahtar-uzayı saldırısının her gün yeniden üretilmesi gerekir, çünkü döndürme sonrasında saldıran router'lar artık hedef anahtara veya birbirlerine yakın olmazlar.

Bu saldırı, ağ boyutu büyüdükçe daha zor hale gelir. Ancak, son araştırmalar keyspace rotasyonunun özellikle etkili olmadığını göstermektedir. Bir saldırgan önceden çok sayıda router hash'ini önceden hesaplayabilir ve rotasyondan sonra yarım saat içinde keyspace'in bir bölümünü "tutulmaya" almak için sadece birkaç router yeterlidir.

Günlük anahtar alanı rotasyonunun bir sonucu, dağıtılmış ağ veritabanının rotasyondan sonra birkaç dakika boyunca güvenilmez hale gelebilmesidir -- yeni "en yakın" router henüz bir depolama almadığı için arama işlemleri başarısız olacaktır. Sorunun kapsamı ve azaltma yöntemleri (örneğin gece yarısında netDb "devir teslim" işlemleri) daha fazla çalışma konusudur.

### Bootstrap Saldırıları

Bir saldırgan, bir reseed web sitesini ele geçirerek veya geliştiricileri kendi reseed web sitesini router'daki sabit kodlanmış listeye eklemeye kandırarak, yeni router'ları izole edilmiş veya çoğunluğu kontrol ettiği bir ağa başlatmaya çalışabilir.

Birkaç savunma mümkündür ve bunların çoğu planlanmıştır:

- Reseeding için HTTPS'ten HTTP'ye geri dönüşe izin verme. Bir MITM saldırganı HTTPS'i engelleyip ardından HTTP'ye yanıt verebilir.
- Reseed verilerini kurulum programına dahil etme

Uygulanan savunma yöntemleri:

- Reseed görevini tek bir site kullanmak yerine birkaç reseed sitesinden RouterInfo alt kümesi getirmek için değiştirme
- Reseed web sitelerini periyodik olarak yoklayan ve verilerin eskimediğini veya ağın diğer görünümleriyle tutarsız olmadığını doğrulayan ağ-dışı reseed izleme servisi oluşturma
- 0.9.14 sürümünden itibaren, reseed verileri imzalı zip dosyasına paketlenmekte ve indirildiğinde imza doğrulanmaktadır. Ayrıntılar için [su3 spesifikasyonuna](/docs/specs/updates/#su3) bakın.

### Sorgu Yakalama

Ayrıca [arama](#routerinfo-and-leaseset-lookup) bölümüne bakınız (Referans: [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf) aşağıdaki italik terimler için Bölüm 2.2-2.3)

Bootstrap saldırısına benzer şekilde, floodfill router kullanan bir saldırgan, kontrol ettiği routerların referanslarını döndürerek eşleri kendi kontrolündeki router alt kümesine "yönlendirme" girişiminde bulunabilir.

Bu keşif yoluyla çalışması pek olası değildir, çünkü keşif düşük frekanslı bir görevdir. Router'lar eş referanslarının çoğunluğunu normal tunnel oluşturma etkinliği yoluyla elde eder. Keşif sonuçları genellikle birkaç router hash'i ile sınırlıdır ve her keşif sorgusu rastgele bir floodfill router'a yönlendirilir.

0.8.9 sürümünden itibaren, *iteratif aramalar* uygulanmaktadır. Bir arama için [I2NP](/docs/specs/i2np/) DatabaseSearchReplyMessage yanıtında döndürülen floodfill router referansları, arama anahtarına daha yakın (veya bir sonraki en yakın) iseler takip edilir. İsteyen router, referansların anahtara daha yakın olduğuna güvenmez (yani bunlar *doğrulanabilir şekilde doğrudur*). Arama ayrıca daha yakın anahtar bulunamadığında durmaz, zaman aşımı veya maksimum sorgu sayısına ulaşılana kadar bir sonraki en yakın düğümü sorgulayarak devam eder. Bu, kötü niyetli bir floodfill'in anahtar alanının bir bölümünü kara deliğe çevirmesini önler. Ayrıca, günlük anahtar alanı rotasyonu, bir saldırganın istenen anahtar alanı bölgesi içinde bir router bilgisini yeniden oluşturmasını gerektirir. Bu tasarım, [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf) makalesinde açıklanan sorgu yakalama saldırısının çok daha zor olmasını sağlar.

### DHT Tabanlı Relay Seçimi

(Referans: [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf) Bölüm 3)

Bu, floodfill ile pek ilgisi yoktur, ancak tunnel'lar için eş seçiminin güvenlik açıklarının tartışıldığı [eş seçimi sayfasına](/docs/overview/peer-selection/) bakın.

### Bilgi Sızıntıları

(Referans: [In Search of an Anonymous and Secure Lookup](https://www.freehaven.net/anonbib/cache/ccs10-lookup.pdf) Bölüm 3)

Bu makale, Torsk ve NISAN tarafından kullanılan "Finger Table" DHT aramalarındaki zayıflıkları ele almaktadır. İlk bakışta, bunların I2P için geçerli olmadığı görülmektedir. İlk olarak, Torsk ve NISAN tarafından DHT kullanımı I2P'dekinden önemli ölçüde farklıdır. İkinci olarak, I2P'nin network database aramaları yalnızca [peer selection](/docs/overview/peer-selection/) ve [tunnel building](/docs/overview/tunnel-routing/) süreçleriyle gevşek bir şekilde ilişkilidir; tunnel'lar için yalnızca önceden bilinen peer'lar kullanılır. Ayrıca, peer selection DHT anahtar-yakınlığı kavramıyla hiçbir ilgisi yoktur.

Bunların bir kısmı aslında I2P ağı çok daha büyüdüğünde daha ilginç hale gelebilir. Şu anda, her router ağın büyük bir kısmını biliyor, bu nedenle network database'de belirli bir Router Info aramak o router'ın gelecekte bir tunnel'da kullanılacağına dair güçlü bir gösterge değil. Belki de ağ 100 kat daha büyük olduğunda, arama daha ilişkili olabilir. Tabii ki, daha büyük bir ağ Sybil saldırısını da o kadar zorlaştırır.

Ancak, I2P'de DHT bilgi sızıntısının genel sorunu daha fazla araştırma gerektirir. floodfill router'lar sorguları gözlemleyebilecek ve bilgi toplayabilecek konumdadır. Kesinlikle, *f* = 0.2 seviyesinde (makalede belirtildiği gibi %20 kötü niyetli düğüm) tanımladığımız Sybil tehditlerin ([burada](/docs/overview/threat-model/#sybil), [burada](#sybil-attack-full-keyspace) ve [burada](#sybil-attack-partial-keyspace)) birçoğunun çeşitli nedenlerle sorunlu hale gelmesini bekliyoruz.

---

## Geçmiş

[netdb tartışma sayfasına taşındı](/docs/legacy/netdb/).

---

## Gelecek Çalışmalar

Ek netDb sorguları ve yanıtlarının uçtan uca şifrelenmesi.

Arama yanıtlarını izlemek için daha iyi yöntemler.
