---
title: "Görünmez Çoklu Barındırma"
number: "140"
author: "str4d"
created: "2017-05-22"
lastupdated: "2017-07-04"
status: "Aç"
thread: "http://zzz.i2p/topics/2335"
toc: true
---

## Genel Bakış

Bu öneri, bir I2P istemcisi, hizmeti veya harici dengeleyici sürecinin tek bir [Destination](http://localhost:63465/docs/specs/common-structures/#destination)'ı şeffaf bir şekilde barındıran birden fazla router'ı yönetmesini sağlayan bir protokol için tasarımı özetlemektedir.

Bu öneri şu anda somut bir uygulama belirtmiyor. [I2CP](/docs/specs/i2cp/) için bir uzantı olarak veya yeni bir protokol olarak uygulanabilir.

## Motivasyon

Multihoming, aynı Destination'ı barındırmak için birden fazla router'ın kullanıldığı durumdur. I2P ile multihoming yapmanın mevcut yolu, aynı Destination'ı her router üzerinde bağımsız olarak çalıştırmaktır; herhangi bir zamanda istemciler tarafından kullanılan router, LeaseSet yayınlayan son router'dır.

Bu bir hack ve muhtemelen büyük ölçekli web siteleri için çalışmayacaktır. Diyelim ki her biri 16 tunnel'a sahip 100 multihoming router'ımız var. Bu, her 10 dakikada 1600 LeaseSet yayını veya neredeyse saniyede 3 tane demektir. floodfill'ler bunalmış olurdu ve kısıtlamalar devreye girerdi. Bu, arama trafiğinden bahsetmeden önceki durum.

Öneri 123 bu sorunu 100 gerçek LeaseSet hash'ini listeleyen bir meta-LeaseSet ile çözüyor. Arama iki aşamalı bir süreç haline geliyor: önce meta-LeaseSet'i arama, sonra da adlandırılmış LeaseSet'lerden birini arama. Bu, arama trafiği sorununa iyi bir çözüm, ancak kendi başına önemli bir gizlilik sızıntısı yaratıyor: Yayınlanan meta-LeaseSet'i izleyerek hangi multihoming router'ların çevrimiçi olduğunu belirlemek mümkün, çünkü her gerçek LeaseSet tek bir router'a karşılık geliyor.

Bir I2P istemcisinin veya servisinin tek bir Destination'ı birden fazla router arasında dağıtabilmesi için bir yönteme ihtiyacımız var, bu şekilde tek bir router kullanmaktan ayırt edilemez olmalı (LeaseSet'in kendisi açısından).

## Tasarım

### Definitions

    User
        The person or organisation wanting to multihome their Destination(s). A
        single Destination is considered here without loss of generality (WLOG).

    Client
        The application or service running behind the Destination. It may be a
        client-side, server-side, or peer-to-peer application; we refer to it as
        a client in the sense that it connects to the I2P routers.

        The client consists of three parts, which may all be in the same process
        or may be split across processes or machines (in a multi-client setup):

        Balancer
            The part of the client that manages peer selection and tunnel
            building. There is a single balancer at any one time, and it
            communicates with all I2P routers. There may be failover balancers.

        Frontend
            The part of the client that can be operated in parallel. Each
            frontend communicates with a single I2P router.

        Backend
            The part of the client that is shared between all frontends. It has
            no direct communication with any I2P router.

    Router
        An I2P router run by the user that sits at the boundary between the I2P
        network and the user's network (akin to an edge device in corporate
        networks). It builds tunnels under the command of a balancer, and routes
        packets for a client or frontend.

### High-level overview

Aşağıdaki istenen konfigürasyonu hayal edin:

- Tek Destination'a sahip bir istemci uygulaması.
- Her biri üç gelen tunnel'ı yöneten dört router.
- Tüm on iki tunnel tek bir LeaseSet'te yayınlanmalıdır.

### Single-client

```
                -{ [Tunnel 1]===\
                 |-{ [Tunnel 2]====[Router 1]-----
                 |-{ [Tunnel 3]===/               \
                 |                                 \
                 |-{ [Tunnel 4]===\                 \
  [Destination]  |-{ [Tunnel 5]====[Router 2]-----   \
    \            |-{ [Tunnel 6]===/               \   \
     [LeaseSet]--|                               [Client]
                 |-{ [Tunnel 7]===\               /   /
                 |-{ [Tunnel 8]====[Router 3]-----   /
                 |-{ [Tunnel 9]===/                 /
                 |                                 /
                 |-{ [Tunnel 10]==\               /
                 |-{ [Tunnel 11]===[Router 4]-----
                  -{ [Tunnel 12]==/
```
### Tanımlar

```
                -{ [Tunnel 1]===\
                 |-{ [Tunnel 2]====[Router 1]---------[Frontend 1]
                 |-{ [Tunnel 3]===/          \                    \
                 |                            \                    \
                 |-{ [Tunnel 4]===\            \                    \
  [Destination]  |-{ [Tunnel 5]====[Router 2]---\-----[Frontend 2]   \
    \            |-{ [Tunnel 6]===/          \   \                \   \
     [LeaseSet]--|                         [Balancer]            [Backend]
                 |-{ [Tunnel 7]===\          /   /                /   /
                 |-{ [Tunnel 8]====[Router 3]---/-----[Frontend 3]   /
                 |-{ [Tunnel 9]===/            /                    /
                 |                            /                    /
                 |-{ [Tunnel 10]==\          /                    /
                 |-{ [Tunnel 11]===[Router 4]---------[Frontend 4]
                  -{ [Tunnel 12]==/
```
### Üst düzey genel bakış

- Bir Destination yükle veya oluştur.

- Her router ile Destination'a bağlı bir oturum açın.

- Düzenli olarak (yaklaşık her on dakikada bir, ancak tunnel canlılığına bağlı olarak az ya da çok):

- Her router'dan hızlı katmanı elde edin.

- Her router'dan/router'a tünel oluşturmak için peer'ların üst kümesini kullanın.

    - By default, tunnels to/from a particular router will use peers from
      that router's fast tier, but this is not enforced by the protocol.

- Tüm aktif router'lardan aktif gelen tunnel'ların setini topla ve bir LeaseSet oluştur.

- LeaseSet'i router'lardan bir veya birkaçı aracılığıyla yayınla.

### Tek istemci

Bu konfigürasyonu oluşturmak ve yönetmek için, client'ın şu anda [I2CP](/docs/specs/i2cp/) tarafından sağlanandan daha fazla yeni işlevselliğe ihtiyacı vardır:

- Bir router'a, onlar için LeaseSet oluşturmadan tüneller inşa etmesini söyler.
- Gelen havuzundaki mevcut tünellerin listesini alır.

Ek olarak, aşağıdaki işlevsellik, istemcinin tunnel'larını nasıl yönettiği konusunda önemli esneklik sağlayacaktır:

- Bir router'ın hızlı katmanının içeriğini al.
- Bir router'a verilen eş listesini kullanarak gelen veya giden tunnel oluşturmasını söyle.

### Çoklu istemci

```
         Client                           Router

                    --------------------->  Create Session
   Session Status  <---------------------
                    --------------------->  Get Fast Tier
        Peer List  <---------------------
                    --------------------->  Create Tunnel
    Tunnel Status  <---------------------
                    --------------------->  Get Tunnel Pool
      Tunnel List  <---------------------
                    --------------------->  Publish LeaseSet
                    --------------------->  Send Packet
      Send Status  <---------------------
  Packet Received  <---------------------
```
### Genel istemci süreci

**Oturum Oluştur** - Belirtilen Destination için bir oturum oluştur.

**Oturum Durumu** - Oturumun kurulduğunun onayı ve istemcinin artık tunnel'ları oluşturmaya başlayabileceği.

**Get Fast Tier** - Router'ın şu anda tunnel'lar oluşturmayı düşüneceği eşlerin listesini talep et.

**Peer Listesi** - Router tarafından bilinen peer'ların listesi.

**Tunnel Oluştur** - Router'ın belirtilen eşler üzerinden yeni bir tunnel oluşturmasını talep eder.

**Tunnel Durumu** - Belirli bir tunnel oluşturma işleminin sonucu, mevcut olduğunda.

**Tunnel Pool Al** - Hedef için gelen veya giden havuzdaki mevcut tunnelların listesini talep et.

**Tunnel Listesi** - İstenen havuz için tunnel'ların listesi.

**LeaseSet Yayınla** - Router'ın sağlanan LeaseSet'i Destination için giden tunnel'lardan biri aracılığıyla yayınlamasını talep eder. Yanıt durumu gerekmez; router LeaseSet'in yayınlandığından emin olana kadar yeniden denemeye devam etmelidir.

**Paket Gönder** - İstemciden giden bir paket. İsteğe bağlı olarak, paketin gönderilmesi gereken (gönderilmesi gerekir mi?) bir giden tunnel belirtir.

**Gönderim Durumu** - İstemciyi bir paketin gönderilmesinin başarılı veya başarısız olduğu konusunda bilgilendirir.

**Paket Alındı** - İstemci için gelen bir paket. İsteğe bağlı olarak paketin alındığı gelen tunnel'ı belirtir(?)

## Security implications

Router'ların perspektifinden bakıldığında, bu tasarım işlevsel olarak mevcut durumla eşdeğerdir. Router hala tüm tunnel'ları inşa eder, kendi peer profillerini tutar ve router ile istemci operasyonları arasında ayrımı zorlar. Varsayılan yapılandırmada tamamen aynıdır, çünkü o router için tunnel'lar kendi hızlı katmanından inşa edilir.

netDB perspektifinden bakıldığında, bu protokol aracılığıyla oluşturulan tek bir LeaseSet, mevcut işlevsellikten yararlandığı için mevcut durumla aynıdır. Ancak, 16 Lease'e yaklaşan daha büyük LeaseSet'ler için, bir gözlemcinin LeaseSet'in çok konumlu (multihomed) olduğunu belirlemesi mümkün olabilir:

- Hızlı katmanın mevcut maksimum boyutu 75 eştir. Inbound Gateway
  (IBGW, bir Lease'de yayınlanan düğüm) katmanın bir kesiminden seçilir
  (hash ile tunnel pool başına rastgele bölümlendirilir, sayıya göre değil):

      1 hop
          The whole fast tier

      2 hops
          Half of the fast tier
          (the default until mid-2014)

      3+ hops
          A quarter of the fast tier
          (3 being the current default)

Bu, ortalama olarak IBGW'lerin 20-30 eşten oluşan bir kümeden olacağı anlamına gelir.

- Tek bağlantılı bir kurulumda, tam 16-tünelli bir LeaseSet, (diyelim) 20 peer'e kadar olan bir setten rastgele seçilen 16 IBGW'ye sahip olacaktır.

- Varsayılan yapılandırmayı kullanan 4 router'lı multihomed kurulumda, tam bir 16-tunnel LeaseSet, en fazla 80 peer'dan oluşan bir setten rastgele seçilmiş 16 IBGW'ye sahip olacaktır, ancak router'lar arasında ortak peer'ların bir kısmının bulunması muhtemeldir.

Bu nedenle varsayılan yapılandırma ile, istatistiksel analiz yoluyla bir LeaseSet'in bu protokol tarafından üretildiğini anlamanın mümkün olabileceği söylenebilir. Ayrıca kaç router olduğunu da anlamak mümkün olabilir, ancak hızlı katmanlardaki değişimin bu analizin etkinliğini azaltacağı da söylenebilir.

İstemci hangi eşleri seçeceği konusunda tam kontrole sahip olduğundan, bu bilgi sızıntısı azaltılmış bir eş kümesinden IBGW'ler seçilerek azaltılabilir veya ortadan kaldırılabilir.

## Compatibility

Bu tasarım, LeaseSet formatında hiçbir değişiklik olmadığı için ağ ile tamamen geriye dönük uyumludur. Tüm router'ların yeni protokolden haberdar olması gerekir, ancak hepsi aynı varlık tarafından kontrol edileceği için bu bir endişe kaynağı değildir.

## Performance and scalability notes

Bu öneriye göre LeaseSet başına 16 Lease üst sınırı değiştirilmemiştir. Bundan daha fazla tünele ihtiyaç duyan Destination'lar için iki olası ağ modifikasyonu bulunmaktadır:

- LeaseSet'lerin boyut üst sınırını artırın. Bu uygulaması en basit olan yöntem olacaktır (yine de yaygın olarak kullanılabilmesi için kapsamlı ağ desteği gerektirecek olsa da), ancak daha büyük paket boyutları nedeniyle daha yavaş aramalar ile sonuçlanabilir. Maksimum uygulanabilir LeaseSet boyutu, alttaki aktarım katmanlarının MTU'su tarafından tanımlanır ve bu nedenle yaklaşık 16kB civarındadır.

- Tiered LeaseSet'ler için Proposal 123'ü uygulayın. Bu önerinin kombinasyonunda,
  alt-LeaseSet'ler için Destination'lar birden fazla router'a yayılabilir,
  etkin bir şekilde clearnet servisler için birden fazla IP adresi gibi davranır.

## Acknowledgements

Bu öneriye yol açan tartışma için psi'ye teşekkürler.
