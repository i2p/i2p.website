---
title: "Görünmez Multihoming"
number: "140"
author: "str4d"
created: "2017-05-22"
lastupdated: "2017-07-04"
status: "Açık"
thread: "http://zzz.i2p/topics/2335"
---

## Genel Bakış

Bu öneri, bir I2P istemcisi, hizmeti veya harici dengeleme sürecinin, tek bir [Destination](http://localhost:63465/en/docs/specs/common-structures/#destination) üzerinde birden fazla yönlendiricinin şeffaf bir şekilde yönetilmesini sağlayan bir protokol tasarımını özetlemektedir.

Öneri şu anda somut bir uygulama belirtmemektedir. [I2CP](/en/docs/specs/i2cp/) için bir uzantı ya da yeni bir protokol olarak uygulanabilir.


## Motivasyon

Multihoming, aynı Destination'ı barındırmak için birden fazla yönlendiricinin kullanıldığı durumdur. Şu anki I2P ile multihoming yapma yöntemi, her yönlendiricide bağımsız olarak aynı Destination'ı çalıştırmaktır; herhangi bir zamanda istemciler tarafından kullanılan yönlendirici, en son [LeaseSet](http://localhost:63465/en/docs/specs/common-structures/#leaseset) yayınlayandır.

Bu yöntem bir hack olup, büyük ölçekli web siteleri için uygun değildir. Örneğin, her biri 16 tünel olan 100 multihoming yönlendiricimiz olduğunu varsayalım. Bu, her 10 dakikada bir 1600 LeaseSet yayını, yani saniyede neredeyse 3 yayın anlamına gelir. Yoğunluğun fazla olması anaforları boğar ve sınırlamalar devreye girer. Bahsetmediğimiz arama trafiğinden bile önce.

[Proposal 123](/en/proposals/123-new-netdb-entries/), 100 gerçek LeaseSet hash'ini listeleyen bir meta-LeaseSet ile bu sorunu çözer. Bir arama iki aşamalı bir işlem haline gelir: önce meta-LeaseSet, ardından adlandırılan LeaseSet’lerden biri aranır. Bu, arama trafiği sorununa iyi bir çözüm ancak kendiliğinden önemli bir gizlilik açığı oluşturur: Yayınlanan meta-LeaseSet'i izleyerek hangi multihoming yönlendiricilerin çevrimiçi olduğunu belirlemek mümkündür, çünkü her gerçek LeaseSet tek bir yönlendiriciye karşılık gelir.

Bir I2P istemcisi ya da hizmeti için, bir Destination'ı birden fazla yönlendiriciye yayma yollarına ihtiyacımız var, LeaseSet'in perspektifinden tek bir yönlendirici kullanmaya ayırtedilemeyecek bir şekilde.


## Tasarım

### Tanımlar

    Kullanıcı
        Destination'larını multihome yapmak isteyen kişi veya kuruluş. Tek bir
        Destination burada genellik kaybetmeden (WLOG) ele alınmıştır.

    İstemci
        Destination'ın arkasında çalışan uygulama veya hizmet. İstemci tarafta,
        sunucu tarafında veya eşten-eşe bir uygulama olabilir; I2P yönlendiricilere
        bağlanması anlamında bir istemci olarak adlandırılır.

        İstemci üç bölümden oluşur ve hepsi aynı süreç içinde olabilir veya
        (çoklu istemci kurulumunda) süreçler veya makineler arasında bölünebilir:

        Dengeleyici
            İstemcinin eş seçimi ve tünel oluşturma işlemlerini yöneten parça.
            Herhangi bir zamanda tek bir dengeleyici vardır ve tüm I2P yönlendiricilerle iletişim kurar.
            Yedek dengeleyiciler olabilir.

        Ön Uç
            Paralel çalıştırılabilen istemci parçası. Her ön uç tek bir I2P yönlendirici ile iletişim kurar.

        Arka Uç
            Tüm ön uçlar arasında paylaşılan istemci parçası. Herhangi bir I2P
            yönlendirici ile doğrudan iletişimi yoktur.

    Yönlendirici
        Kullanıcı tarafından çalıştırılan ve I2P ağı ile kullanıcının ağı arasındaki sınırda duran
        bir I2P yönlendirici (kurumsal ağlardaki uç cihazlara benzer).
        Bir dengeleyicinin komutuyla tünel oluşturur ve bir istemci veya
        ön uç için paketleri yönlendirir.

### Yüksek seviye genel bakış

Aşağıdaki istenen konfigürasyonu hayal edin:

- Tek bir Destination'a sahip bir istemci uygulaması.
- Her biri üç gelen tünel yöneten dört yönlendirici.
- Tüm on iki tünel tek bir LeaseSet içinde yayımlanmalıdır.

Tek istemci

```
                -{ [Tünel 1]===\
                 |-{ [Tünel 2]====[Yönlendirici 1]-----
                 |-{ [Tünel 3]===/               \
                 |                                 \
                 |-{ [Tünel 4]===\                 \
  [Destination]  |-{ [Tünel 5]====[Yönlendirici 2]-----   \
    \            |-{ [Tünel 6]===/               \   \
     [LeaseSet]--|                               [İstemci]
                 |-{ [Tünel 7]===\               /   /
                 |-{ [Tünel 8]====[Yönlendirici 3]-----   /
                 |-{ [Tünel 9]===/                 /
                 |                                 /
                 |-{ [Tünel 10]==\               /
                 |-{ [Tünel 11]===[Yönlendirici 4]-----
                  -{ [Tünel 12]==/

Çoklu istemci

```
                -{ [Tünel 1]===\
                 |-{ [Tünel 2]====[Yönlendirici 1]---------[Ön uç 1]
                 |-{ [Tünel 3]===/          \                    \
                 |                            \                    \
                 |-{ [Tünel 4]===\            \                    \
  [Destination]  |-{ [Tünel 5]====[Yönlendirici 2]---\-----[Ön uç 2]   \
    \            |-{ [Tünel 6]===/          \   \                \   \
     [LeaseSet]--|                         [Dengeleyici]            [Arka uç]
                 |-{ [Tünel 7]===\          /   /                /   /
                 |-{ [Tünel 8]====[Yönlendirici 3]---/-----[Ön uç 3]   /
                 |-{ [Tünel 9]===/            /                    /
                 |                            /                    /
                 |-{ [Tünel 10]==\          /                    /
                 |-{ [Tünel 11]===[Yönlendirici 4]---------[Ön uç 4]
                  -{ [Tünel 12]==/

### Genel istemci süreci
- Bir Destination yükleyin veya oluşturun.

- Her yönlendiriciyle, Destination'a bağlı bir oturum açın.

- Periyodik olarak (her on dakikada bir civarında, ancak tünel canlılığına bağlı olarak daha fazla veya daha az):

  - Her yönlendiriciden hızlı katmanı alın.

  - Her yönlendiriciye giden/gelen tünelleri oluşturmak için eşlerin üst kümesini kullanın.

    - Varsayılan olarak, belirli bir yönlendiriciye gidip gelen tüneller, o yönlendiricinin hızlı katmanındaki
      eşleri kullanacaktır, ancak bu protokol tarafından zorunlu değildir.

  - Tüm aktif yönlendiricilerden aktif gelen tünellerin setini toplayın ve bir
    LeaseSet oluşturun.

  - LeaseSet'i bir veya daha çok yönlendirici aracılığıyla yayımlayın.

### I2CP'ye farklar
Bu konfigürasyonu oluşturmak ve yönetmek için, istemcinin [I2CP](/en/docs/specs/i2cp/) tarafından şu anda sağlanandan daha fazla yeni işlevselliğe ihtiyacı vardır:

- Bir LeaseSet oluşturmadan, bir yönlendiriciye tüneller inşa etmesini söylemek.
- Gelen havuzdaki mevcut tünellerin bir listesini almak.

Ayrıca, istemcinin tünellerini yönetirken önemli bir esneklik sağlayacak olan şu işlevsellik:

- Bir yönlendiricinin hızlı katmanının içeriğini almak.
- Belirtilen bir eş listesini kullanarak bir gelen veya giden tünel inşa etmesi için bir yönlendiriciye emir vermek.

### Protokol taslağı

```
         İstemci                           Yönlendirici

                    --------------------->  Oturum Oluştur
   Oturum Durumu  <---------------------
                    --------------------->  Hızlı Katmanı Al
        Eş Listesi  <---------------------
                    --------------------->  Tünel Oluştur
    Tünel Durumu  <---------------------
                    --------------------->  Tünel Havuzunu Al
      Tünel Listesi  <---------------------
                    --------------------->  LeaseSet Yayınla
                    --------------------->  Paket Gönder
      Gönderme Durumu  <---------------------
  Paket Alındı  <---------------------

### Mesajlar
    Oturum Oluştur
        Verilen Destination için bir oturum oluşturun.

    Oturum Durumu
        Oturumun kurulduğuna ve istemcinin artık tüneller oluşturmaya
        başlayabileceğine dair onay.

    Hızlı Katmanı Al
        Yönlendiricinin şu anda tünel oluşturmayı düşüneceği
        eşlerin bir listesini isteyin.

    Eş Listesi
        Yönlendirici tarafından bilinen bir eşler listesi.

    Tünel Oluştur
        Yönlendiriciden, belirtilen eşler aracılığıyla yeni bir tünel
        oluşturmasını isteyin.

    Tünel Durumu
        Belirli bir tünel inşasının sonucu, kullanılabilir olduğunda.

    Tünel Havuzunu Al
        Destination'ın gelen veya giden havuzundaki mevcut tünellerin
        bir listesini isteyin.

    Tünel Listesi
        İstenen havuz için tünellerin listesi.

    LeaseSet Yayınla
        Yönlendiricinin, sağlanan LeaseSet'i Destination için bir giden
        tünel aracılığıyla yayımlamasını isteyin. Yanıttan status bildirimi
        gerekmez; yönlendirici LeaseSet'in yayımlandığına tatmin olana
        kadar yeniden denemeye devam etmelidir.

    Paket Gönder
        İstemciden gelen bir çıkış paketi. Paketin gönderileceği
        giden tüneli isteğe bağlı olarak belirtir (belirtmeli?).

    Gönderme Durumu
        Bir paketin gönderilmesinin başarı veya başarısızlığını
        istemciye bildirir.

    Paket Alındı
        İstemci için bir gelen paket. Paketin alındığı
        gelen tüneli isteğe bağlı olarak belirtir(?)


## Güvenlik etkileri

Yönlendiricilerin perspektifinden, bu tasarım işlevsel olarak mevcut duruma
eşdeğerdir. Yönlendirici hala tüm tünelleri oluşturur, kendi eş profillerini
korur ve yönlendirici ile istemci işlemleri arasında ayrımı uygular. Varsayılan
konfigürasyon tamamen aynıdır, çünkü bu yönlendirici için tüneller kendi hızlı
katmanından yapılmıştır.

netDB açısından, bu protokol aracılığıyla oluşturulan tek bir LeaseSet, mevcut
durumla aynıdır çünkü önceden var olan işlevselliği kullanır. Bununla birlikte,
16 Lease'e yaklaşan daha büyük LeaseSet'ler için, bir gözlemcinin LeaseSet'in
multihome yapıldığını belirlemesi mümkün olabilir:

- Hızlı katmanın mevcut maksimum büyüklüğü 75 eştir. İnbound Gateway
  (IBGW, Lease içinde yayımlanan düğüm), katmanın bir kısmından
  (sayım değil, hash'e göre rastgele ayrılmış tünel havuzuna göre):

      1 hop
          Tüm hızlı katman

      2 hop
          Hızlı katmanın yarısı
          (2014 ortalarına kadar varsayılan)

      3+ hop
          Hızlı katmanın dörtte biri
          (şu anki varsayılan olan 3)

  Yani, ortalama olarak IBGWs 20-30 eşlik bir setten olacaktır.

- Tekil homed kurulumda, tam 16 tünelli LeaseSet'in bir setten rastgele seçilmiş
  16 IBGW'si olacaktır, en fazla (diyelim ki) 20 eş.

- Varsayılan konfigürasyon kullanılarak dört yönlendirici multihomed bir kurulumda,
  tam 16 tünelli LeaseSet rastgele seçilmiş 16 IBGW'si en fazla 80 eş
  içeren bir setteng olacaktır, ancak yönlendiriciler arasında muhtemelen
  ortak eşler olacaktır.

Dolayısıyla varsayılan konfigürasyonda, LeaseSet'in bu protokol tarafından
üretildiğini anlamak için istatistiksel analizle tespit edilmesi mümkün olabilir.
Kaç adet yönlendirici olduğunu anlamak da mümkün olabilir, ancak hızlı
katmanlarının değişiklik etkisi bu analizin etkinliğini azaltacaktır.

İstemci seçmelerinde tam kontrole sahip olduğundan, bu bilgi sızıntısı,
IBGWs'yi bir eşler setinden seçerek azaltılabilir veya ortadan kaldırılabilir.


## Uyumluluk

Bu tasarım ağ ile tamamen geriye dönük uyumludur, çünkü [LeaseSet](http://localhost:63465/en/docs/specs/common-structures/#leaseset) formatında
herhangi bir değişiklik yoktur. Tüm yönlendiricilerin yeni protokolden haberdar
olması gerekecektir, ancak bunlar aynı kuruluş tarafından kontrol edildiğinden bu
bir endişe değildir.


## Performans ve ölçeklenebilirlik notları

LeaseSet başına 16 [Lease]'in üst sınırı bu öneriyle değişmeden kalmaktadır. Daha fazla
tünele ihtiyaç duyan Destinations için iki olası ağ değişikliği vardır:

- LeaseSet boyutunun üst limitini artırmak. Bu, uygulanması en kolay olanıdır
  (ancak, yaygın olarak kullanılabilmesi için yaygın ağ desteği gerektirir),
  ancak daha büyük paket boyutları nedeniyle daha yavaş aramalara yol açabilir.
  MTU'su tarafından tanımlanan maksimum uygulanabilir LeaseSet boyutu taşımaların
  ve dolayısıyla yaklaşık 16kB olur.

- [Proposal 123](/en/proposals/123-new-netdb-entries/) uygulaması ile katmanlı LeaseSet'ler. Bu öneriyle
  birlikte, alt-LeaseSet'lere olan Destinations, birden fazla yönlendiriciye
  yayılabilir ve bu da, temiz ağ hizmeti için birden fazla IP adresi gibi
  davranır.


## Teşekkürler

Bu öneriye yol açan tartışmadan dolayı psi'ye teşekkür ederiz.
