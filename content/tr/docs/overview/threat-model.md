---
title: "I2P'nin Tehdit Modeli"
description: "I2P'nin tasarımında değerlendirilen saldırı türlerinin analizi ve mevcut koruma önlemleri"
slug: "threat-model"
aliases:
  - "/tr/how_threatmodel"
  - "/tr/how_threatmodel/"
lastUpdated: "2010-11"
accurateFor: "0.8.1"
---

## "Anonim" ile Neyi Kastediyoruz?

Anonimlik seviyeniz "birinin öğrenmesini istemediğiniz bilgileri bulmasının ne kadar zor olduğu" şeklinde tanımlanabilir — kim olduğunuz, nerede bulunduğunuz, kiminle iletişim kurduğunuz, hatta ne zaman iletişim kurduğunuz. "Mükemmel" anonimlik burada faydalı bir kavram değildir — yazılım sizi bilgisayar kullanmayan veya İnternet'te olmayan insanlardan ayırt edilemez hale getirmeyecektir. Bunun yerine, kimler olursa olsunlar gerçek ihtiyaçlarını karşılayacak yeterli anonimlik sağlamak için çalışıyoruz — sadece web sitelerine göz atanlardan, veri alışverişi yapanlara, güçlü organizasyonlar veya devletler tarafından keşfedilmekten korkanlara kadar.

I2P'nin sizin özel ihtiyaçlarınız için yeterli anonimlik sağlayıp sağlamadığı sorusu zor bir sorudur, ancak bu sayfa I2P'nin çeşitli saldırılar altında nasıl çalıştığını inceleyerek bu soruyu yanıtlamanızda size yardımcı olacaktır, böylece ihtiyaçlarınızı karşılayıp karşılamadığına karar verebilirsiniz.

Aşağıda açıklanan tehditlere karşı I2P'nin direncine yönelik daha fazla araştırma ve analizleri memnuniyetle karşılıyoruz. Mevcut literatürün (büyük bir kısmı Tor odaklı) daha fazla incelenmesi ve I2P odaklı özgün çalışmalara ihtiyaç vardır.

---

## Ağ Topolojisi Özeti

I2P, birçok [diğer](/docs/overview/comparison/) sistemin fikirlerini temel alır, ancak ilgili literatürü incelerken akılda tutulması gereken birkaç önemli nokta vardır:

- **I2P ücretsiz bir route mixnet'tir** — mesaj oluşturucu, mesajların gönderileceği yolu açıkça tanımlar (outbound tunnel), ve mesaj alıcısı da mesajların alınacağı yolu açıkça tanımlar (inbound tunnel).
- **I2P'nin resmi giriş ve çıkış noktaları yoktur** — tüm eşler karışıma tam olarak katılır ve ağ katmanında giriş veya çıkış proxy'leri bulunmaz (ancak uygulama katmanında birkaç proxy mevcuttur).
- **I2P tamamen dağıtıktır** — merkezi kontroller veya otoriteler yoktur. Bazı router'ları mix kaskadları işletecek şekilde değiştirmek (tunnel'lar inşa etmek ve tunnel uç noktasında yönlendirmeyi kontrol etmek için gerekli anahtarları vermek) veya dizin tabanlı profilleme ve seçim yapmak mümkündür, bunların hepsi ağın geri kalanıyla uyumluluğu bozmadan yapılabilir, ancak tabii ki bunu yapmak gerekli değildir (ve hatta kişinin anonimliğine zarar verebilir).

Mesajı alan belirli hop veya tunnel gateway'ine özgü olan, varlığı sadece o noktada bilinen önemsiz olmayan gecikmeler ve toplu işleme stratejileri uygulamak için belgelenmiş planlarımız bulunmaktadır. Bu, çoğunlukla düşük gecikme süreli bir mixnet'in daha yüksek gecikme süreli iletişim (örn. e-posta) için gizleme trafiği sağlamasına olanak tanır. Ancak anlamlı koruma sağlamak için önemli gecikmelerin gerekli olduğunun ve bu tür gecikmelerin uygulanmasının büyük bir zorluk olacağının farkındayız. Bu gecikme özelliklerini gerçekten uygulayıp uygulamayacağımız şu anda net değildir.

Teorik olarak, mesaj yolu boyunca bulunan router'lar mesajı bir sonraki eşe iletmeden önce keyfi sayıda atlama ekleyebilir, ancak mevcut uygulama bunu yapmaz.

---

## Tehdit Modeli

I2P tasarımı 2003 yılında, [Onion Routing](http://www.onion-router.net), [Freenet](http://freenetproject.org/) ve [Tor](https://www.torproject.org/)'un ortaya çıkmasından kısa bir süre sonra başladı. Tasarımımız o dönemde yayınlanan araştırmalardan önemli ölçüde faydalanmaktadır. I2P birkaç onion routing tekniği kullandığından, Tor'a olan önemli akademik ilgiden faydalanmaya devam ediyoruz.

[Anonimlik literatüründe](http://freehaven.net/anonbib/topic.html) (büyük ölçüde [Traffic Analysis: Protocols, Attacks, Design Issues and Open Problems](http://citeseer.ist.psu.edu/454354.html)) ortaya konan saldırılar ve analizlerden yola çıkarak, aşağıda çok çeşitli saldırılar ile I2P'nin birçok savunma mekanizması kısaca açıklanmaktadır. Bu listeyi, yeni saldırılar tespit edildikçe güncellemekteyiz.

I2P'ye özgü olabilecek bazı saldırılar da dahil edilmiştir. Bu saldırıların hepsine iyi yanıtlarımız bulunmamakla birlikte, araştırmalarımızı sürdürmeye ve savunmalarımızı iyileştirmeye devam ediyoruz.

Ayrıca, mevcut ağın küçük boyutu nedeniyle bu saldırıların çoğu olması gerekenden çok daha kolaydır. Ele alınması gereken bazı sınırlamalardan haberdar olmamıza rağmen, I2P yüz binlerce hatta milyonlarca katılımcıyı destekleyecek şekilde tasarlanmıştır. Söz yaymaya ve ağı büyütmeye devam ettikçe, bu saldırılar çok daha zor hale gelecektir.

[Ağ karşılaştırmaları](/docs/overview/comparison/) ve ["garlic" terminolojisi](/docs/overview/garlic-routing/) sayfaları da incelemeniz için faydalı olabilir.

### Kaba Kuvvet Saldırıları

Küresel pasif veya aktif bir saldırgan tarafından tüm düğümler arasında geçen tüm mesajları izleyerek ve hangi mesajın hangi yolu takip ettiğini ilişkilendirmeye çalışarak bir kaba kuvvet saldırısı gerçekleştirilebilir. I2P'ye karşı bu saldırıyı gerçekleştirmek önemsiz olmayacaktır, çünkü ağdaki tüm eşler sıklıkla mesaj göndermekte (hem uçtan uca hem de ağ bakım mesajları) ve ayrıca uçtan uca bir mesaj yolu boyunca boyut ve veri değiştirmektedir. Ek olarak, harici saldırgan mesajlara erişime sahip değildir, çünkü router'lar arası iletişim hem şifrelenmiş hem de akış halindedir (iki adet 1024 baytlık mesajı bir adet 2048 baytlık mesajdan ayırt edilemez hale getirir).

Ancak, güçlü bir saldırgan eğilimleri tespit etmek için kaba kuvvet kullanabilir — eğer bir I2P hedefine 5GB gönderebilir ve herkesin ağ bağlantısını izleyebilirlerse, 5GB veri almayan tüm eşleri eleyebilirler. Bu saldırıyı yenmek için teknikler mevcut, ancak aşırı derecede pahalı olabilir (bkz: [Tarzan](http://citeseer.ist.psu.edu/freedman02tarzan.html)'ın taklitçileri veya sabit hızlı trafik). Çoğu kullanıcı bu saldırıdan endişe duymaz, çünkü bunu gerçekleştirmenin maliyeti aşırıdır (ve genellikle yasadışı faaliyetler gerektirir). Ancak saldırı hala mümkündür, örneğin büyük bir ISS'deki veya Internet değişim noktasındaki bir gözlemci tarafından. Buna karşı savunmak isteyenler, düşük bant genişliği sınırları belirleme ve I2P Siteleri için yayınlanmamış veya şifrelenmiş leaseSet'ler kullanma gibi uygun karşı önlemler almak isteyeceklerdir. Önemsiz olmayan gecikmeler ve kısıtlı rotalar gibi diğer karşı önlemler şu anda uygulanmamıştır.

Tek bir router veya router grubu ağın tüm trafiğini yönlendirmeye çalışmasına karşı kısmi bir savunma olarak, router'lar tek bir eş üzerinden kaç tunnel'ın yönlendirilebileceğine dair sınırlar içerir. Ağ büyüdükçe, bu sınırlar daha fazla ayarlama yapılabilir. Eş derecelendirme, seçme ve kaçınma için diğer mekanizmalar eş seçimi sayfasında tartışılmaktadır.

### Zamanlama Saldırıları

I2P'nin mesajları tek yönlüdür ve mutlaka bir yanıt gönderileceği anlamına gelmez. Ancak, I2P üzerindeki uygulamaların mesaj sıklıkları içinde büyük olasılıkla tanınabilir kalıpları olacaktır — örneğin, bir HTTP isteği, HTTP yanıtını içeren büyük bir yanıt mesajları dizisiyle birlikte küçük bir mesaj olacaktır. Bu verileri ve ağ topolojisinin geniş bir görünümünü kullanarak, bir saldırgan bazı bağlantıları mesajı iletmek için çok yavaş olduğu gerekçesiyle eleyebilir.

Bu tür saldırı güçlüdür, ancak I2P'ye uygulanabilirliği açık değildir, çünkü kuyrukta bekleme, mesaj işleme ve kısıtlama nedeniyle mesaj gecikmelerindeki değişkenlik genellikle bir mesajın tek bir bağlantı boyunca geçiş süresini karşılar veya aşar — saldırgan mesaj alınır alınmaz bir yanıtın gönderileceğini bildiğinde bile. Bununla birlikte, oldukça otomatik yanıtları açığa çıkaracak bazı senaryolar vardır — streaming kütüphanesi (SYN+ACK ile) ve garantili teslimatın mesaj modu (DataMessage+DeliveryStatusMessage ile) bunu yapar.

Protokol temizleme veya daha yüksek gecikme süresi olmadan, küresel aktif saldırganlar önemli bilgiler elde edebilir. Bu nedenle, bu saldırılardan endişe duyan kişiler gecikme süresini artırabilir (önemsiz olmayan gecikme veya toplu işlem stratejileri kullanarak), protokol temizleme dahil edebilir veya diğer gelişmiş tunnel yönlendirme tekniklerini kullanabilir, ancak bunlar I2P'de uygulanmamıştır.

Kaynaklar: [Low-Resource Routing Attacks Against Anonymous Systems](http://www.cs.colorado.edu/department/publications/reports/docs/CU-CS-1025-07.pdf)

### Kesişim Saldırıları

Düşük gecikme sistemlerine karşı kesişim saldırıları son derece güçlüdür — hedefle periyodik olarak iletişim kurun ve ağda hangi eşlerin bulunduğunu takip edin. Zaman içinde, düğüm değişimi gerçekleştikçe saldırgan, bir mesaj başarıyla iletildiğinde çevrimiçi olan eş kümelerini basitçe kesiştirerek hedef hakkında önemli bilgiler elde edecektir. Bu saldırının maliyeti ağ büyüdükçe önemlidir, ancak bazı senaryolarda uygulanabilir olabilir.

Özetle, bir saldırgan aynı anda tunnel'ınızın her iki ucunda da bulunuyorsa, başarılı olabilir. I2P'nin düşük gecikme süreli iletişim için bu duruma karşı tam bir savunması yoktur. Bu, düşük gecikme süreli onion routing'in doğasında var olan bir zayıflıktır. Tor da [benzer bir sorumluluk reddi beyanı](https://trac.torproject.org/projects/tor/wiki/TheOnionRouter/TorFAQ#Whatattacksremainagainstonionrouting) sunmaktadır.

I2P'de uygulanan kısmi savunmalar:

- Peer'ların [katı sıralaması](/docs/specs/tunnel-implementation/#ordering)
- Yavaş değişen küçük bir gruptan peer profilleme ve seçimi
- Tek bir peer üzerinden yönlendirilen tunnel sayısında sınırlamalar
- Aynı /16 IP aralığından peer'ların tek bir tunnel'ın üyesi olmasının engellenmesi
- I2P Siteleri veya diğer barındırılan hizmetler için, birden fazla router'da eşzamanlı barındırma veya multihoming desteği

Toplamda bile, bu savunmalar tam bir çözüm değildir. Ayrıca, güvenlik açığımızı önemli ölçüde artırabilecek bazı tasarım seçimleri yaptık:

- Düşük bant genişlikli "guard node'lar" kullanmıyoruz
- Birkaç tunnel'dan oluşan tunnel havuzları kullanıyoruz ve trafik tunnel'dan tunnel'a geçebilir.
- Tunnel'lar uzun ömürlü değildir; her 10 dakikada yeni tunnel'lar oluşturulur.
- Tunnel uzunlukları yapılandırılabilir. Tam koruma için 3-hop tunnel'lar önerilse de, birkaç uygulama ve servis varsayılan olarak 2-hop tunnel'lar kullanır.

Gelecekte, önemli gecikmeleri karşılayabilen eşler için bu mümkün olabilir (önemsiz olmayan gecikmeler ve toplu işleme stratejileri başına). Ayrıca, bu yalnızca diğer insanların bildiği destinasyonlar için geçerlidir — destinasyonu yalnızca güvenilir eşler tarafından bilinen özel bir grup endişelenmek zorunda değildir, çünkü bir saldırgan saldırı düzenlemek için onları "ping"leyemez.

Referans: [One Cell Enough](http://blog.torproject.org/blog/one-cell-enough)

### Hizmet Reddi Saldırıları

I2P'ye karşı kullanılabilir çok sayıda hizmet reddi saldırısı bulunmaktadır ve her birinin farklı maliyetleri ve sonuçları vardır:

**Açgözlü kullanıcı saldırısı:** Bu, insanların katkıda bulunmaya istekli olduklarından önemli ölçüde daha fazla kaynak tüketmeye çalışmasıdır. Buna karşı savunma şudur:

- Çoğu kullanıcının ağa kaynak sağlaması için varsayılanları ayarlayın. I2P'de kullanıcılar varsayılan olarak trafiği yönlendirir. [Diğer ağlardan](/docs/overview/comparison/) keskin bir ayrımla, I2P kullanıcılarının %95'inden fazlası başkaları için trafiği aktarır.
- Kullanıcıların ağa katkılarını (paylaşım yüzdesini) artırabilmeleri için kolay yapılandırma seçenekleri sağlayın. Kullanıcıların ne katkıda bulunduklarını görebilmeleri için "paylaşım oranı" gibi anlaşılması kolay metrikleri görüntüleyin.
- Blog'lar, forumlar, IRC ve diğer iletişim araçlarıyla güçlü bir topluluk sürdürün.

**Açlık saldırısı:** Düşmanca bir kullanıcı, ağda aynı varlığın kontrolü altında olduğu belirlenmemiş önemli sayıda peer oluşturarak ağa zarar vermeye çalışabilir (Sybil'de olduğu gibi). Bu düğümler daha sonra ağa herhangi bir kaynak sağlamamaya karar vererek, mevcut peer'ların daha büyük bir network database'de arama yapmasına veya gerekenden daha fazla tunnel talep etmesine neden olur. Alternatif olarak, düğümler seçili trafiği periyodik olarak düşürerek veya belirli peer'lara bağlantıları reddederek aralıklı hizmet sağlayabilir. Bu davranış, yoğun yük altındaki veya arızalı bir düğümün davranışından ayırt edilemeyebilir. I2P bu sorunları peer'lar üzerinde profiller tutarak, düşük performans gösterenleri belirlemeye çalışarak ve bunları basitçe göz ardı ederek veya nadiren kullanarak ele alır. Sorunlu peer'ları tanıma ve bunlardan kaçınma yeteneğimizi önemli ölçüde geliştirdik; ancak bu alanda hala önemli çabalar gereklidir.

**Flooding saldırısı:** Düşmanca bir kullanıcı ağa, bir peer'a, bir hedefe veya bir tunnel'a flooding saldırısı yapmaya çalışabilir. Ağ ve peer flooding'i mümkündür ve I2P standart IP katmanı flooding'ini önlemek için hiçbir şey yapmaz. Hedefin çeşitli inbound tunnel gateway'lerine çok sayıda mesaj göndererek bir hedefe mesaj flooding'i yapmak mümkündür, ancak hedef bunu hem mesajın içeriğinden hem de tunnel testlerinin başarısız olmasından anlayacaktır. Aynı durum sadece tek bir tunnel'a flooding yapmak için de geçerlidir. I2P'nin ağ flooding saldırısına karşı hiçbir savunması yoktur. Hedef ve tunnel flooding saldırısı için, hedef hangi tunnel'ların yanıt vermediğini belirler ve yenilerini oluşturur. İstemci daha büyük yükü kaldırmak istiyorsa, daha fazla tunnel eklemek için yeni kod da yazılabilir. Öte yandan, yük istemcinin başa çıkabileceğinden fazlaysa, tunnel'lara aktarmaları gereken mesaj veya bayt sayısını kısmaları talimatını verebilirler (gelişmiş tunnel operasyonu uygulandığında).

**CPU yük saldırısı:** Şu anda insanların uzaktan bir peer'in kriptografik açıdan pahalı bir işlem gerçekleştirmesini talep etmesine yönelik bazı yöntemler bulunmaktadır ve düşmanca bir saldırgan, CPU'yu aşırı yüklemek amacıyla bu peer'i çok sayıda bu tür istekle doldurmak için bu yöntemleri kullanabilir. Hem iyi mühendislik uygulamaları kullanmak hem de potansiyel olarak bu pahalı isteklere önemsiz olmayan sertifikalar (örneğin HashCash) eklenmesini gerektirmek bu sorunu hafifletmelidir, ancak saldırganın implementasyondaki çeşitli hataları istismar etmesi için alan olabilir.

**Floodfill DOS saldırısı:** Düşmanca davranan bir kullanıcı floodfill router olarak ağa zarar vermeye çalışabilir. Güvenilmez, aralıklı veya kötü niyetli floodfill router'lara karşı mevcut savunmalar yetersizdir. Bir floodfill router sorgulamalara kötü veya hiç yanıt vermeyebilir ve ayrıca floodfill'ler arası iletişimi engelleyebilir. Bazı savunma mekanizmaları ve eş profilleme uygulanmış olsa da, yapılacak çok şey vardır. Daha fazla bilgi için [network database sayfasına](/docs/specs/common-structures/) bakınız.

### Etiketleme Saldırıları

Etiketleme saldırıları — bir mesajı yol boyunca daha sonra tanımlanabilecek şekilde değiştirme — I2P'de kendi başlarına imkansızdır, çünkü tunnellardan geçen mesajlar imzalanır. Ancak, bir saldırgan hem inbound tunnel gateway'i hem de o tunnel'da daha ilerde bir katılımcı ise, işbirliği yaparak aynı tunnel'da bulunduklarını tespit edebilirler (ve benzersiz hop id'leri ve diğer güncellemelerin eklenmesinden önce, aynı tunnel içindeki işbirlikçi peer'lar bu gerçeği hiçbir çaba harcamadan fark edebilirdi). Ancak outbound tunnel'daki bir saldırgan ile inbound tunnel'ın herhangi bir bölümü işbirliği yapamaz, çünkü tunnel şifreleme inbound ve outbound tunnellar için veriyi ayrı ayrı doldurur ve değiştirir. Harici saldırganlar hiçbir şey yapamaz, çünkü bağlantılar şifrelidir ve mesajlar imzalanmıştır.

### Bölümleme Saldırıları

Bölümleme saldırıları — bir ağdaki eşleri (teknik olarak veya analitik olarak) ayırmanın yollarını bulma — güçlü bir düşmanla uğraşırken akılda tutulması gereken önemli konulardır, çünkü ağın büyüklüğü anonimliğinizi belirlemede kilit rol oynar. Eşler arasındaki bağlantıları keserek parçalanmış ağlar oluşturmak yoluyla yapılan teknik bölümleme, I2P'nin yerleşik network database'i tarafından ele alınır; bu veritabanı çeşitli eşler hakkında istatistikler tutarak, diğer parçalanmış bölümlere mevcut bağlantıların ağı iyileştirmek amacıyla kullanılabilmesini sağlar. Ancak, saldırgan kontrolü altında olmayan eşlere olan tüm bağlantıları kopararak hedefi esasen yalıtırsa, hiçbir network database iyileştirmesi bunu düzeltemez. Bu noktada, router'ın yapabileceği tek şey, daha önce güvenilir olan önemli sayıda eşin erişilemez hale geldiğini fark etmek ve istemciyi geçici olarak bağlantısının kesildiği konusunda uyarmaktır (bu tespit kodu şu anda henüz uygulanmamıştır).

Ağı analitik olarak router'lar ve hedeflerin nasıl davrandığına bakarak farklılıklar arayıp bunlara göre gruplandırarak bölümleme de çok güçlü bir saldırıdır. Örneğin, ağ veritabanını [toplayan](#harvesting-attacks) bir saldırgan, belirli bir hedefin LeaseSet'inde 5 gelen tunnel'ı varken diğerlerinin sadece 2 veya 3'ü olduğunu bilebilir, bu da düşmanın istemcileri seçilen tunnel sayısına göre potansiyel olarak bölümlemesine olanak tanır. Önemsiz olmayan gecikmeler ve toplu işleme stratejileriyle uğraşırken başka bir bölümleme mümkündür, çünkü tunnel gateway'leri ve sıfır olmayan gecikmelere sahip belirli hop'lar muhtemelen öne çıkacaktır. Ancak, bu veriler yalnızca o belirli hop'lara maruz kalır, bu nedenle bu konuda etkili bir şekilde bölümleme yapmak için saldırganın ağın önemli bir bölümünü kontrol etmesi gerekir (ve yine de bu sadece olasılıksal bir bölümleme olacaktır, çünkü diğer hangi tunnel'ların veya mesajların bu gecikmelere sahip olduğunu bilemezler).

Ayrıca [network database sayfasında](/docs/specs/common-structures/) tartışılmıştır (bootstrap saldırısı).

### Öncül Saldırıları

Predecessor saldırısı, hedefin tunnel'larına katılarak ve bir önceki veya bir sonraki hop'u takip ederek (sırasıyla outbound veya inbound tunnel'lar için) hangi eşlerin hedefe 'yakın' olduğunu görmeye çalışan pasif bir istatistik toplama yöntemidir. Zamanla, mükemmel rastgele bir eş örneklemi ve rastgele sıralama kullanarak, bir saldırgan hangi eşin istatistiksel olarak diğerlerinden daha 'yakın' göründüğünü tespit edebilir ve bu eş de hedefin bulunduğu yer olacaktır.

I2P bunu dört şekilde önler: birincisi, tunnel'lara katılmak için seçilen eşler ağ genelinde rastgele örneklenmez — bunlar eşleri katmanlara ayıran eş seçim algoritmasından türetilir. İkincisi, bir tunnel'daki eşlerin [sıkı sıralaması](/docs/specs/tunnel-implementation/#ordering) ile, bir eşin daha sık görünmesi onların kaynak olduğu anlamına gelmez. Üçüncüsü, permütasyonlu tunnel uzunluğu ile (varsayılan olarak etkin değil) 0 atlama tunnel'ları bile makul inkar edilebilirlik sağlayabilir çünkü gateway'in ara sıra değişimi normal tunnel'lar gibi görünür. Dördüncüsü, kısıtlı rotalar ile (uygulanmamış), yalnızca hedefe kısıtlı bağlantısı olan eş hedefle iletişim kurarken, saldırganlar sadece o gateway ile karşılaşır.

Mevcut tunnel yapım yöntemi, özellikle öncül saldırısına karşı mücadele etmek için tasarlanmıştır. Ayrıca bkz. [kesişim saldırısı](#intersection-attacks).

Referanslar: [Wright et al. 2008](http://forensics.umass.edu/pubs/wright.tissec.2008.pdf), bu [2004 öncül saldırı makalesinin](http://forensics.umass.edu/pubs/wright-tissec.pdf) güncellenmiş halidir.

### Hasat Saldırıları

"Harvesting" (veri toplama), I2P çalıştıran kullanıcıların bir listesini derleme anlamına gelir. Basitçe bir peer çalıştırarak, hangi kullanıcılara bağlandığını görerek ve bulabileceği diğer peer'lara yapılan referansları toplayarak yasal saldırılar için ve diğer saldırılara yardımcı olmak için kullanılabilir.

I2P'nin kendisi bu saldırıya karşı etkili savunmalarla tasarlanmamıştır, çünkü tam da bu bilgiyi içeren dağıtık ağ veritabanı bulunmaktadır. Aşağıdaki faktörler saldırıyı pratikte biraz daha zorlaştırır:

- Ağ büyümesi, ağın belirli bir oranını elde etmeyi daha zor hale getirecektir
- Floodfill router'ları DOS koruması olarak sorgu sınırları uygular
- Bir router'ın bilgilerini netDb'ye yayınlamasını engelleyen (ancak aynı zamanda veri aktarmasını da engelleyen) "gizli mod" şu anda yaygın olarak kullanılmamakta ancak kullanılabilir.

Gelecekteki uygulamalarda, temel ve kapsamlı kısıtlı rotalar bu saldırının gücünü azaltacaktır, çünkü "gizli" eşler iletişim adreslerini network database'de yayınlamazlar — sadece ulaşılabilecekleri tunnel'ları (aynı zamanda public key'leri vb.) yayınlarlar.

Gelecekte, router'lar GeoIP kullanarak kendilerinin I2P düğümü olarak tanımlanmasının riskli olacağı belirli bir ülkede bulunup bulunmadıklarını tespit edebilirler. Bu durumda, router otomatik olarak gizli modu etkinleştirebilir veya diğer kısıtlı yönlendirme yöntemlerini uygulayabilir.

### Trafik Analizi Yoluyla Kimlik Belirleme

Bir router'a giren ve çıkan trafiği inceleyerek, kötü niyetli bir İSS veya devlet düzeyindeki güvenlik duvarı bir bilgisayarın I2P çalıştırdığını tespit edebilir. [Yukarıda](#harvesting-attacks) tartışıldığı gibi, I2P özellikle bir bilgisayarın I2P çalıştırdığını gizlemek için tasarlanmamıştır. Ancak, transport katmanı ve protokollerin tasarımında alınan birkaç tasarım kararı I2P trafiğini tespit etmeyi bir ölçüde zorlaştırmaktadır:

- Rastgele port seçimi
- Tüm trafiğin Noktadan-Noktaya Şifrelenmesi
- Protokol baytları veya diğer şifrelenmemiş sabit alanlar olmadan DH anahtar değişimi
- Hem TCP hem UDP taşıyıcılarının eşzamanlı kullanımı. UDP, bazı Derin Paket İnceleme (DPI) ekipmanları için takip etmesi çok daha zor olabilir.

Yakın gelecekte, I2P transport protokollerinin daha fazla gizlenmesi yoluyla trafik analizi sorunlarını doğrudan ele almayı planlıyoruz, muhtemelen şunları içerecek:

- Bağlantı kurulum sırasında özellikle rastgele uzunluklarda transport katmanında padding
- Paket boyutu dağılım imzalarının incelenmesi ve gerektiğinde ek padding
- SSL veya diğer yaygın protokolleri taklit eden ek transport yöntemlerinin geliştirilmesi
- Yüksek katmanlardaki padding stratejilerinin transport katmanındaki paket boyutlarını nasıl etkilediğinin gözden geçirilmesi
- Çeşitli devlet düzeyindeki güvenlik duvarlarının Tor'u engellemek için uyguladığı yöntemlerin incelenmesi
- DPI ve gizleme uzmanlarıyla doğrudan çalışma

Referans: [Breaking and Improving Protocol Obfuscation](http://www.iis.se/docs/hjelmvik_breaking.pdf)

### Sybil Saldırıları

Sybil, düşmanın keyfi olarak büyük sayıda işbirlikçi node oluşturduğu ve artan sayıları diğer saldırıları gerçekleştirmek için kullandığı bir saldırı kategorisini tanımlar. Örneğin, bir saldırgan eşlerin rastgele seçildiği bir ağda bulunuyorsa ve bu eşlerden biri olma şansının %80 olmasını istiyorsa, ağdaki node sayısının beş katı kadar node oluşturur ve zarı atar. Kimlik ücretsiz olduğunda, Sybil güçlü bir düşman için çok etkili bir teknik olabilir. Bunu ele almanın temel tekniği, kimliği 'ücretsiz olmayan' hale getirmektir — [Tarzan](http://www.pdos.lcs.mit.edu/tarzan/) (diğerleri arasında) IP adreslerinin sınırlı olduğu gerçeğini kullanırken, IIP yeni bir kimlik oluşturmak için 'ücretlendirme' yapmak üzere [HashCash](http://www.hashcash.org/) kullanmıştır. Şu anda Sybil'i ele almak için herhangi bir özel teknik uygulamamış olmakla birlikte, router ve destination veri yapılarında gerektiğinde uygun değerde bir HashCash sertifikası (veya kıtlığı kanıtlayan başka bir sertifika) içerebilecek yer tutucu sertifikalar bulundurmaktayız.

Çeşitli yerlerde HashCash Sertifikaları gerektirmenin iki büyük sorunu vardır:

- Geriye dönük uyumluluğu koruma
- Klasik HashCash problemi — üst düzey makinelerde anlamlı iş kanıtları olan HashCash değerlerini seçerken, aynı zamanda mobil cihazlar gibi düşük performanslı makinelerde de uygulanabilir olmasını sağlama.

Belirli bir IP aralığındaki router sayısına yönelik çeşitli sınırlamalar, birden fazla IP bloğuna makine yerleştirme yeteneği olmayan saldırganlara karşı güvenlik açığını kısıtlar. Ancak bu, güçlü bir düşmana karşı anlamlı bir savunma değildir.

Daha fazla Sybil tartışması için [ağ veritabanı sayfasına](/docs/specs/common-structures/) bakın.

### Buddy Tükenme Saldırıları

(Referans: [In Search of an Anonymous and Secure Lookup](http://www.eecs.berkeley.edu/~pmittal/publications/nisan-torsk-ccs10.pdf) Bölüm 5.2)

Bir router, işbirlikçi bir eşe hariç tunnel oluşturma isteklerini kabul etmeyi veya iletmeyi reddederek, bir tunnel'ın tamamen kendi işbirlikçi router'ları setinden oluşturulmasını sağlayabilir. Çok sayıda işbirlikçi router varsa, yani bir [Sybil saldırısı](#sybil-attacks) durumunda, başarı şansları artar. Bu durum, eşlerin performansını izlemek için kullandığımız eş profilleme yöntemleriyle kısmen azaltılmaktadır. Ancak, makalede belirtildiği gibi router sayısı *f* = 0.2 veya %20 kötü niyetli düğüme yaklaştıkça bu güçlü bir saldırıdır. Kötü niyetli router'lar ayrıca hedef router'a bağlantıları sürdürebilir ve hedef tarafından yönetilen profilleri manipüle etme ve çekici görünme girişiminde bu bağlantılar üzerinden trafik için mükemmel iletim bant genişliği sağlayabilir. Daha fazla araştırma ve savunma önlemleri gerekli olabilir.

### Kriptografik Saldırılar

Uzun anahtarlarla güçlü şifreleme kullanıyoruz ve I2P'de kullanılan endüstri standardı şifreleme ilkellerinin güvenliğini varsayıyoruz. Güvenlik özellikleri arasında yol boyunca değiştirilmiş mesajların anında tespiti, size gönderilmemiş mesajları şifresini çözme imkansızlığı ve ortadaki adam saldırılarına karşı savunma yer almaktadır. 2003'te seçilen anahtar boyutları o zamanlar oldukça muhafazakardı ve hala [diğer anonimlik ağlarında](https://torproject.org/) kullanılanlardan daha uzundur. Mevcut anahtar uzunluklarının bizim en büyük zayıflığımız olduğunu düşünmüyoruz, özellikle geleneksel, devlet düzeyinde olmayan rakipler için; hatalar ve ağın küçük boyutu çok daha endişe vericidir. Tabii ki, tüm şifreleme algoritmaları sonunda daha hızlı işlemciler, şifreleme araştırmaları ve gökkuşağı tabloları, video oyun donanımı kümeleri gibi yöntemlerdeki ilerlemeler nedeniyle eskimiş hale gelir. Ne yazık ki, I2P geriye uyumluluk sağlarken anahtarları uzatmak veya paylaşılan gizli değerleri değiştirmek için kolay mekanizmalarla tasarlanmamıştır.

Daha uzun anahtarları destekleyecek şekilde çeşitli veri yapılarının ve protokollerin yükseltilmesi er ya da geç ele alınmak zorunda kalacak ve bu, [diğerleri](https://torproject.org/) için olduğu gibi büyük bir girişim olacaktır. Umarız dikkatli planlama sayesinde aksaksızlığı en aza indirebilir ve gelecekteki geçişleri kolaylaştıracak mekanizmalar uygulayabiliriz.

Gelecekte, birkaç I2P protokolü ve veri yapısı, mesajları rastgele boyutlara güvenli bir şekilde doldurmayı destekleyecek, böylece mesajlar sabit boyutta yapılabilir veya garlic mesajlar rastgele değiştirilerek bazı clove'ların gerçekte olduğundan daha fazla alt-clove içeriyormuş gibi görünmesi sağlanabilir. Ancak şu anda garlic, tunnel ve uçtan uca mesajlar basit rastgele doldurma içermektedir.

### Floodfill Anonimlik Saldırıları

[Yukarıda](#denial-of-service-attacks) açıklanan floodfill DOS saldırılarına ek olarak, floodfill router'ları netDb'deki rolleri ve bu katılımcılarla yüksek frekanslı iletişim nedeniyle ağ katılımcıları hakkında bilgi edinmek için benzersiz bir konumdadır. Bu durum, floodfill router'ların toplam keyspace'in yalnızca bir bölümünü yönetmesi ve [ağ veritabanı sayfasında](/docs/specs/common-structures/) açıklandığı gibi keyspace'in günlük olarak döngüye girmesi nedeniyle bir dereceye kadar hafifletilmiştir. Router'ların floodfill'lerle iletişim kurma mekanizmaları dikkatli bir şekilde tasarlanmıştır. Ancak, bu tehditler daha fazla incelenmelidir. Spesifik potansiyel tehditler ve karşılık gelen savunma yöntemleri gelecekteki araştırmalar için bir konudur.

### Diğer Ağ Veritabanı Saldırıları

Düşmanca niyetli bir kullanıcı, bir veya daha fazla floodfill router oluşturup bunları kötü, yavaş veya hiç yanıt vermeyecek şekilde tasarlayarak ağa zarar vermeye çalışabilir. Çeşitli senaryolar [network database sayfasında](/docs/specs/common-structures/) tartışılmaktadır.

### Merkezi Kaynak Saldırıları

Saldırıya uğrayabilecek veya saldırı vektörü olarak kullanılabilecek birkaç merkezi veya sınırlı kaynak bulunmaktadır (bazıları I2P içinde, bazıları değil). Kasım 2007'de jrandom'un yokluğu ve ardından Ocak 2008'de i2p.net barındırma hizmetinin kaybı, I2P ağının geliştirilmesi ve işletilmesinde çok sayıda merkezi kaynağı ortaya çıkardı ve bunların çoğu artık dağıtılmış durumdadır. Dışarıdan erişilebilir kaynaklara yapılan saldırılar esas olarak yeni kullanıcıların bizi bulma yeteneğini etkiler, ağın kendisinin işleyişini değil.

- Web sitesi yansılanmıştır ve harici kamu erişimi için DNS round-robin kullanır.
- Router'lar artık [birden fazla harici reseed konumunu](/docs/overview/faq/#reseed) desteklemektedir, ancak daha fazla reseed sunucusuna ihtiyaç duyulabilir ve güvenilmez veya kötü niyetli reseed sunucularının ele alınması geliştirilmeli olabilir.
- Router'lar artık birden fazla güncelleme dosyası konumunu destekler. Kötü niyetli bir güncelleme sunucusu büyük bir dosya besleyebilir; boyutu sınırlamak gerekir.
- Router'lar artık birden fazla varsayılan güvenilir güncelleme imzalayıcısını destekler.
- Router'lar artık birden fazla güvenilmez floodfill eşini daha iyi ele alır. Kötü niyetli floodfill'ler daha fazla çalışma gerektirir.
- Kod artık dağıtık bir kaynak kontrol sisteminde saklanmaktadır.
- Router'lar tek bir haber sunucusuna güvenir, ancak farklı bir sunucuyu işaret eden sabit kodlanmış bir yedek URL vardır. Kötü niyetli bir haber sunucusu büyük bir dosya besleyebilir; boyutu sınırlamak gerekir.
- Adres defteri abonelik sağlayıcıları, host-ekleme hizmetleri ve jump hizmetleri dahil olmak üzere [isimlendirme sistemi hizmetleri](/docs/overview/naming/) kötü niyetli olabilir. Abonelikler için önemli korumalar 0.6.1.31 sürümünde uygulandı ve sonraki sürümlerde ek geliştirmeler yapıldı. Ancak, tüm isimlendirme hizmetleri bir ölçüde güven gerektirir; ayrıntılar için [isimlendirme sayfasına](/docs/overview/naming/) bakın.
- i2p2.de için DNS hizmetine bağımlı kalmaya devam ediyoruz; bunu kaybetmek yeni kullanıcıları çekme yeteneğimizde önemli bir aksamaya neden olur ve i2p.net'in kaybının yaptığı gibi ağı küçültür (kısa-orta vadede).

### Geliştirme Saldırıları

Bu saldırılar doğrudan ağa yönelik değildir, bunun yerine yazılım geliştirmesine katkıda bulunan herkese yasal engeller çıkararak ya da geliştiricileri yazılımı sabote etmeye zorlayacak her türlü yöntemi kullanarak geliştirme ekibini hedef alır. Geleneksel teknik önlemler bu saldırıları engelleyemez ve eğer birisi bir geliştiricinin yaşamını veya geçim kaynağını tehdit ederse (hatta sadece hapishane tehdidi ile birlikte bir mahkeme emri ve susturma emri çıkarsa bile), büyük bir sorunumuz olur.

Ancak, bu saldırılara karşı korunmaya yardımcı olan iki teknik vardır:

- Ağın tüm bileşenleri inceleme, doğrulama, değiştirme ve geliştirmeyi mümkün kılmak için açık kaynak olmalıdır. Bir geliştirici ele geçirilirse, bu fark edildiğinde topluluk açıklama talep etmeli ve o geliştiricinin çalışmalarını kabul etmeyi bırakmalıdır. Dağıtık kaynak kontrol sistemimize yapılan tüm check-inler kriptografik olarak imzalanır ve sürüm paketleyicileri değişiklikleri daha önce onaylanmış olanlarla kısıtlamak için bir güven listesi sistemi kullanır.
- Ağın kendisi üzerinde geliştirme, geliştiricilerin anonim kalmasına izin verirken geliştirme sürecini güvenli hale getirir. Tüm I2P geliştirmesi I2P üzerinden gerçekleşebilir — dağıtık kaynak kontrol sistemi, IRC sohbeti, halka açık web sunucuları, tartışma forumları (forum.i2p) ve yazılım dağıtım siteleri kullanarak, hepsi I2P içinde mevcuttur.

Ayrıca herhangi bir savunma gerekli olması durumunda hukuki danışmanlık sunan çeşitli kuruluşlarla da ilişkilerimizi sürdürüyoruz.

### Uygulama Saldırıları (Hatalar)

Ne kadar çabalasak da, çoğu karmaşık uygulama tasarım veya uygulama hatalarını içerir ve I2P de bunun bir istisnası değildir. I2P üzerinde çalışan iletişimin anonimliğini veya güvenliğini beklenmedik şekillerde saldırmak için istismar edilebilecek hatalar olabilir. Kullanılan tasarım veya protokollere karşı saldırılara karşı dayanabilmeye yardımcı olmak için tüm tasarımları ve belgeleri yayınlıyoruz ve çok sayıda gözün sistemi geliştireceği umuduyla inceleme ve eleştiri istiyoruz. Belirsizlik yoluyla güvenlik anlayışına inanmıyoruz.

Ayrıca kod da aynı şekilde ele alınmakta olup, yazılım sisteminin ihtiyaçlarını karşılamayan (değişiklik kolaylığı dahil) bir şeyi yeniden çalışma veya atma konusunda çok az isteksizlik gösterilmektedir. Ağın ve yazılım bileşenlerinin tasarım ve uygulama dokümantasyonu güvenliğin temel bir parçasıdır, çünkü bunlar olmadan geliştiricilerin yazılımı eksiklikleri ve hataları tespit edecek kadar öğrenmek için zaman harcama konusunda istekli olmaları pek olası değildir.

Yazılımımızda özellikle bellek yetersizliği hataları (OOM'lar) yoluyla hizmet reddi saldırıları, router konsolundaki siteler arası betik çalıştırma (XSS) sorunları ve çeşitli protokoller aracılığıyla standart olmayan girdilere karşı diğer güvenlik açıkları ile ilgili hatalar bulunma olasılığı yüksektir.

I2P hâlâ küçük bir geliştirici topluluğuna sahip küçük bir ağdır ve akademik veya araştırma gruplarından neredeyse hiç ilgi görmemektedir. Bu nedenle [diğer anonimlik ağlarının](https://torproject.org/) almış olabileceği analizden yoksunuz. İnsanları [dahil olmaya](/get-involved/) ve yardım etmeye davet etmeye devam ediyoruz.

---

## Diğer Savunmalar

### Engelleme Listeleri

Bir dereceye kadar, I2P, bir engelleme listesinde bulunan IP adreslerinde çalışan peer'ları (eş düğümler) önleyecek şekilde geliştirilebilir. Standart formatlarda yaygın olarak kullanılabilen birkaç engelleme listesi mevcuttur ve bunlar anti-P2P organizasyonları, potansiyel devlet düzeyindeki hasımları ve diğerlerini listeler.

Aktif eş düğümlerin gerçekten gerçek engelleme listesinde görünmesi ölçüsünde, sadece bir alt küme eş düğüm tarafından engelleme ağı bölümleme eğilimi gösterir, erişilebilirlik sorunlarını kötüleştirir ve genel güvenilirliği azaltır. Bu nedenle belirli bir engelleme listesi üzerinde anlaşmak ve bunu varsayılan olarak etkinleştirmek isteyebiliriz.

Engelleme listeleri, kötü niyetliliğe karşı savunma dizisinin yalnızca bir parçasıdır (belki de küçük bir parçası). Büyük ölçüde profilleme sistemi, netDb'de herhangi bir şeye güvenmemiz gerekmeyecek şekilde router davranışını ölçmede iyi bir iş çıkarıyor. Ancak yapılabilecek daha fazla şey var. Yukarıdaki listedeki alanların her biri için kötülüğü tespit etmede yapabileceğimiz iyileştirmeler bulunuyor.

Eğer bir engelleme listesi otomatik güncellemelerle merkezi bir konumda barındırılıyorsa, ağ [merkezi kaynak saldırısına](#central-resource-attacks) karşı savunmasız hale gelir. Bir listeye otomatik abonelik, liste sağlayıcısına I2P ağını tamamen kapatma gücü verir.

Şu anda, yazılımımızla birlikte yalnızca geçmiş DOS kaynaklarının IP'lerini listeleyen varsayılan bir engelleme listesi dağıtılmaktadır. Otomatik güncelleme mekanizması bulunmamaktadır. Belirli bir IP aralığı I2P ağına karşı ciddi saldırılar gerçekleştirirse, insanlardan engelleme listelerini forum, blog vb. gibi bant dışı mekanizmalar aracılığıyla manuel olarak güncellemelerini istemek zorunda kalırız.
