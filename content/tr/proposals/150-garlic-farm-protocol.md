---
title: "Sarımsak Çiftliği Protokolü"
number: "150"
author: "zzz"
created: "2019-05-02"
lastupdated: "2019-05-20"
status: "Açık"
thread: "http://zzz.i2p/topics/2234"
---

## Genel Bakış

Bu, JRaft'a dayalı Sarımsak Çiftliği kablo protokolü için spesifikasyondur, TCP üzerinden uygulama için "exts" kodu ve "dmprinter" örnek uygulaması [JRAFT]_. JRaft, Raft protokolünün bir uygulamasıdır [RAFT]_.

Belgelenmiş bir kablo protokolü olan bir uygulama bulamadık. Ancak, JRaft uygulaması, kodun incelenebileceği ve ardından protokolün belgelenebileceği kadar basittir. Bu öneri bu çabanın sonucudur.

Bu, Meta LeaseSet içindeki girdilerin yayınlanmasında yönlendiricilerin eşgüdümü için arka plan olacak. Teklif 123'e bakın.

## Hedefler

- Küçük kod boyutu
- Mevcut uygulama tabanlı
- Seri hale getirilmiş Java nesneleri veya herhangi bir Java'ya özgü özellikler veya kodlama yok
- Herhangi bir bootstrapping bu protokolün kapsamı dışındadır. En az bir diğer sunucunun sabit kodlanmış veya bu protokolün dışında yapılandırılmış olduğu varsayılır.
- Band dışı ve I2P kullanım durumlarını destekleyin.

## Tasarım

Raft protokolü somut bir protokol değildir; yalnızca bir durum makinesi tanımlar. Bu nedenle, JRaft'ın somut protokolünü belgeleriz ve protokolümüzü buna dayandırırız. Bir kimlik doğrulama el sıkışmasının eklenmesi dışında JRaft protokolünde hiçbir değişiklik yoktur.

Raft bir günlük yayınlamakla görevli bir Lider seçer. Bu günlük, Raft Yapılandırma verilerini ve Uygulama verilerini içerir. Uygulama verileri her Sunucunun Yönlendiricisinin durumunu ve Meta LS2 kümesi için Hedefi içerir. Sunucular, Meta LS2'nin yayınlayıcısını ve içeriğini belirlemek için ortak bir algoritma kullanır. Meta LS2'nin yayıncısı mutlaka Raft Lideri değildir.

## Teknik Şartname

Kablo protokolü SSL soketler veya SSL olmayan I2P soketleri üzerinden çalışır. I2P soketleri HTTP Proxy üzerinden yönlendirilir. Temiz ağ SSL olmayan soketlere destek yoktur.

### El Sıkışma ve Kimlik Doğrulama

JRaft tarafından tanımlanmamıştır.

Hedefler:

- Kullanıcı/parola kimlik doğrulama yöntemi
- Sürüm tanımlayıcısı
- Küme tanımlayıcısı
- Genişletilebilir
- I2P soketleri için kullanıldığında proxying kolaylığı
- Sunucuyu gereksiz yere bir Sarımsak Çiftliği sunucusu olarak ifşa etmeyin
- Tam bir web sunucusu uygulamasının gerekli olmadığı basit protokol
- Yaygın standartlarla uyumlu, böylece istenirse standart kütüphaneler kullanılabilir

Bir WebSocket benzeri el sıkışması [WEBSOCKET]_ ve HTTP Özeti kimlik doğrulaması [RFC-2617]_ kullanacağız. RFC 2617 Temel kimlik doğrulaması desteklenmemektedir. HTTP proxy üzerinden yönlendirilirken, [RFC-2616]_'da belirtildiği gibi proxy ile iletişim kurun.

Kimlik Bilgileri
````````````````

Kullanıcı adları ve parolalar küme başına mı yoksa sunucu başına mı olduğuna uygulamaya bağlıdır.

HTTP İsteği 1
``````````````

Başlatan taraf aşağıdaki gibi gönderir.

Tüm satırlar HTTP tarafından gerekli görüldüğü gibi CRLF ile sonlandırılır.

.. raw:: html

  {% highlight %}

GET /GarlicFarm/CLUSTER/VERSION/websocket HTTP/1.1
  Host: (ip):(port)
  Cache-Control: no-cache
  Connection: close
  (diğer başlıklar yok sayılır)
  (boş satır)

  CLUSTER kümenin adıdır (varsayılan "farm")
  VERSION ise Sarımsak Çiftliği sürümüdür (şimdi "1")

{% endhighlight %}


HTTP Yanıtı 1
```````````````

Eğer yol doğru değilse, alıcı [RFC-2616]_'da belirtildiği gibi standart bir "HTTP/1.1 404 Not Found" yanıtı gönderir.

Eğer yol doğruysa, alıcı [RFC-2617]_'da belirtildiği gibi standart bir "HTTP/1.1 401 Unauthorized" yanıtı gönderir ve WWW-Authenticate HTTP özeti kimlik doğrulama başlığını içerir.

Her iki taraf da daha sonra soketi kapatır.


HTTP İsteği 2
``````````````

Başlatan taraf aşağıdaki gibi gönderir,
[RFC-2617]_ ve [WEBSOCKET]_ gibi.

Tüm satırlar HTTP tarafından gerekli görüldüğü gibi CRLF ile sonlandırılır.

.. raw:: html

  {% highlight %}

GET /GarlicFarm/CLUSTER/VERSION/websocket HTTP/1.1
  Host: (ip):(port)
  Cache-Control: no-cache
  Connection: keep-alive, Upgrade
  Upgrade: websocket
  (Daha proxyli ise Sec-Websocket-* başlıkları)
  Authorization: (RFC 2617'de olduğu gibi HTTP özeti yetkilendirme başlığı)
  (diğer başlıklar yok sayılır)
  (boş satır)

  CLUSTER kümenin adıdır (varsayılan "farm")
  VERSION ise Sarımsak Çiftliği sürümüdür (şimdi "1")

{% endhighlight %}

HTTP Yanıtı 2
```````````````

Eğer kimlik doğrulama doğru değilse, alıcı [RFC-2617]_'da belirtildiği gibi başka bir standart "HTTP/1.1 401 Unauthorized" yanıtı gönderir.

Eğer kimlik doğrulama doğruysa, alıcı [WEBSOCKET]_'da olduğu gibi aşağıdaki yanıtı gönderir.

Tüm satırlar HTTP tarafından gerekli görüldüğü gibi CRLF ile sonlandırılır.

.. raw:: html

  {% highlight %}

HTTP/1.1 101 Switching Protocols
  Connection: Upgrade
  Upgrade: websocket
  (Sec-Websocket-* başlıkları)
  (diğer başlıklar yok sayılır)
  (boş satır)

{% endhighlight %}

Bu alındıktan sonra, soket açık kalır. Aşağıda tanımlandığı gibi Raft protokolü aynı sokette başlar.

Önbellekleme
```````````

Kimlik bilgilerinin en az bir saat boyunca önbelleğe alınması gerekir, böylece
ilerleyen bağlantılar doğrudan yukarıdaki
"HTTP İsteği 2"e atlanabilir.

### Mesaj Türleri

İki tür mesaj vardır: istekler ve yanıtlar.
İstekler, Günlük Girdileri içerebilir ve değişken boyutludur;
yanıtlar, Günlük Girdileri içermez ve sabit boyutludur.

Mesaj tipleri 1-4, Raft tarafından tanımlanan standart RPC mesajlarıdır.
Bu, çekirdek Raft protokolüdür.

Mesaj tipleri 5-15, JRaft tarafından tanımlanan, istemcileri, dinamik sunucu değişikliklerini ve
verimli günlük senkronizasyonunu desteklemek için genişletilmiş RPC mesajlarıdır.

Mesaj tipleri 16-17, Raft bölüm 7'de tanımlanan Günlük Sıkıştırma RPC mesajlarıdır.

========================  ======  ===========  =================   =====================================
Mesaj                     Numarası  Gönderen      Gönderilen Taraf       Notlar
========================  ======  ===========  =================   =====================================
RequestVoteRequest           1    Aday         Takipçi              Standart Raft RPC; Günlük girdileri içermemelidir
RequestVoteResponse          2    Takipçi      Aday                 Standart Raft RPC
AppendEntriesRequest         3    Lider        Takipçi              Standart Raft RPC
AppendEntriesResponse        4    Takipçi      Lider / İstemci      Standart Raft RPC
ClientRequest                5    İstemci      Lider / Takipçi      Yanıt AppendEntriesResponse'dir; Sadece Uygulama günlük girdilerini içermelidir
AddServerRequest             6    İstemci      Lider                Yalnızca tek bir ClusterServer günlük girdisi içermelidir
AddServerResponse            7    Lider        İstemci              Lider ayrıca JoinClusterRequest gönderir
RemoveServerRequest          8    Takipçi      Lider                Yalnızca tek bir ClusterServer günlük girdisi içermelidir
RemoveServerResponse         9    Lider        Takipçi
SyncLogRequest              10    Lider        Takipçi              Uygulamaya sadece bir LogPack günlük girdisi içermelidir
SyncLogResponse             11    Takipçi      Lider
JoinClusterRequest          12    Lider        Yeni Sunucu          Katılma daveti; yalnızca bir Yapılandırma günlük girdisi içermelidir
JoinClusterResponse         13    Yeni Sunucu  Lider
LeaveClusterRequest         14    Lider        Takipçi              Ayrılma komutu
LeaveClusterResponse        15    Takipçi      Lider
InstallSnapshotRequest      16    Lider        Takipçi              Raft Bölümü 7; Sadece bir SnapshotSyncRequest günlük girdisi içermelidir
InstallSnapshotResponse     17    Takipçi      Lider                Raft Bölümü 7
========================  ======  ===========  =================   =====================================

### Kurulum

HTTP el sıkışmasının ardından, kurulum sırası şu şekildedir:

.. raw:: html

  {% highlight %}

Yeni Sunucu Alice              Rastgele Takipçi Bob

  İstemci İsteği   ------->
          <---------   AppendEntries Yanıtı

  Bob lider olduğunu söylerse, aşağıdaki şekilde devam edin.
  Aksi takdirde, Alice Bob'dan bağlantıyı kesmelidir ve lider ile bağlantı kurmalıdır.


  Yeni Sunucu Alice              Lider Charlie

  İstemci İsteği   ------->
          <---------   AppendEntries Yanıtı
  AddServer İsteği   ------->
          <---------   AddServer Yanıtı
          <---------   JoinCluster İsteği
  JoinCluster Yanıtı  ------->
          <---------   SyncLog İsteği
                       VEYA InstallSnapshot İsteği
  SyncLog Yanıtı  ------->
  VEYA InstallSnapshot Yanıtı

{% endhighlight %}

Bağlantıyı Kesme Sırası:

.. raw:: html

  {% highlight %}

Takipçi Alice              Lider Charlie

  RemoveServer İsteği   ------->
          <---------   RemoveServer Yanıtı
          <---------   LeaveCluster İsteği
  LeaveCluster Yanıtı  ------->

{% endhighlight %}

Seçim Sırası:

.. raw:: html

  {% highlight %}

Aday Alice               Takipçi Bob

  RequestVote İsteği   ------->
          <---------   RequestVote Yanıtı

  Alice seçim kazandıysa:

  Lider Alice                Takipçi Bob

  AppendEntries İsteği   ------->
  (kalp atışı)
          <---------   AppendEntries Yanıtı

{% endhighlight %}


### Tanımlar

- Kaynak: Mesajın kökenini tanımlar
- Hedef: Mesajın alıcısını tanımlar
- Dönemler: Raft'a bakın. 0 ile başlatılır, monoton artar
- İndeksler: Raft'a bakın. 0 ile başlatılır, monoton artar

### İstekler

İstekler bir başlık ve sıfır veya daha fazla günlük girdisi içerir. İstekler sabit boyutlu bir başlık ve değişken boyutlu isteğe bağlı Günlük Girdileri içerir.

İstek Başlığı
`````````````

İstek başlığı 45 bayttır, aşağıdaki gibi. Tüm değerler işaretsiz big-endian'dir.

.. raw:: html

  {% highlight lang='dataspec' %}

Mesaj tipi:      1 bayt
  Kaynak:          Kimlik, 4 bayt tamsayı
  Hedef:           Kimlik, 4 bayt tamsayı
  Dönem:           Mevcut dönem (notlara bakın), 8 bayt tamsayı
  Son Günlük Dönemi:  8 bayt tamsayı
  Son Günlük İndeksi:  8 bayt tamsayı
  Onaylı İndeks:   8 bayt tamsayı
  Günlük girdileri boyutu:  Toplam bayt cinsinden boyut, 4 bayt tamsayı
  Günlük girdileri:       aşağıda belirtildiği gibi, belirtilen toplam uzunluk

{% endhighlight %}


#### Notlar

RequestVote İsteğinde, Dönem adayın dönemidir. Diğerlerinde, liderin mevcut dönemidir.

AppendEntries İsteğinde, günlük girdileri boyutu sıfır olduğunda, bu mesaj bir kalp atışı (canlı tutma) mesajıdır.

Günlük Girdileri
``````````````

Günlük sıfır veya daha fazla günlük girdisi içerir. Her günlük girdisi aşağıdaki gibidir. Tüm değerler işaretsiz big-endian'dir.

.. raw:: html

  {% highlight lang='dataspec' %}

Dönem:           8 bayt tamsayı
  Değer türü:     1 bayt
  Girdi boyutu:   Bayt olarak, 4 bayt tamsayı
  Girdi:          belirlenen uzunlukta

{% endhighlight %}

Günlük İçeriği
````````````

Tüm değerler işaretsiz big-endian'dir.

========================  ======
Günlük Değer Türü           Sayı
========================  ======
Uygulama                    1
Yapılandırma                2
Küme Sunucusu               3
Günlük Paketi               4
Anlık Görüntü Eşitleme İsteği 5
========================  ======

#### Uygulama

Uygulama içeriği, basitlik ve genişletilebilirlik için UTF-8 kodlamalı [JSON](https://www.json.org/) formatındadır. Aşağıdaki Uygulama Katmanı bölümüne bakın.

#### Yapılandırma

Bu, liderin yeni bir küme yapılandırmasını seri hale getirmesi ve eşlere çoğaltması için kullanılır. Sıfır veya daha fazla ClusterServer yapılandırması içerir.

.. raw:: html

  {% highlight lang='dataspec' %}

Günlük İndeksi:  8 bayt tamsayı
  Son Günlük İndeksi:  8 bayt tamsayı
  Her sunucu için ClusterServer Verileri:
    Kimlik:                4 bayt tamsayı
    Uç nokta veri boyutu:  Bayt olarak, 4 bayt tamsayı
    Uç nokta verisi:       "tcp://localhost:9001" şeklinde ASCII dizesi, belirtilen uzunlukta

{% endhighlight %}

#### Küme Sunucusu

Bir kümedeki bir sunucu için yapılandırma bilgileri. Bu yalnızca bir AddServerRequest veya RemoveServerRequest mesajında dahil edilir.

AddServerRequest Mesajında kullanıldığında:

.. raw:: html

  {% highlight lang='dataspec' %}

Kimlik:                4 bayt tamsayı
  Uç nokta veri boyutu:  Bayt olarak, 4 bayt tamsayı
  Uç nokta verisi:       "tcp://localhost:9001" şeklinde ASCII dizesi, belirtilen uzunlukta

{% endhighlight %}

RemoveServerRequest Mesajında kullanıldığında:

.. raw:: html

  {% highlight lang='dataspec' %}

Kimlik:                4 bayt tamsayı

{% endhighlight %}

#### Günlük Paketi

Bu yalnızca bir SyncLogRequest mesajında dahil edilir.

Aşağıdaki veriler sıkıştırılmış (gzipped) olarak iletilir:

.. raw:: html

  {% highlight lang='dataspec' %}

İndeks veri boyutu: Bayt olarak, 4 bayt tamsayı
  Günlük veri boyutu: Bayt olarak, 4 bayt tamsayı
  İndeks verisi:     Her indeks için 8 bayt, belirtilen uzunlukta
  Günlük veri:       belirtilen uzunlukta

{% endhighlight %}

#### Anlık Görüntü Eşitleme İsteği

Bu yalnızca bir InstallSnapshotRequest mesajında dahil edilir.

.. raw:: html

  {% highlight lang='dataspec' %}

Son Günlük İndeksi:  8 bayt tamsayı
  Son Günlük Dönemi:   8 bayt tamsayı
  Yapılandırma veri boyutu: Bayt olarak, 4 bayt tamsayı
  Yapılandırma verisi:     belirtilen uzunlukta
  Ofset:          Verinin veritabanındaki ofseti, bayt olarak, 8 bayt tamsayı
  Veri boyutu:        Bayt olarak, 4 bayt tamsayı
  Veri:            belirtilen uzunlukta
  Tamamlandı Mı:         eğer tamamlandıysa 1, değilse 0 (1 bayt)

{% endhighlight %}

### Yanıtlar

Tüm yanıtlar 26 bayttır, aşağıdaki gibi. Tüm değerler işaretsiz big-endian'dir.

.. raw:: html

  {% highlight lang='dataspec' %}

Mesaj tipi:   1 bayt
  Kaynak:         Kimlik, 4 bayt tamsayı
  Hedef:          Genellikle gerçek hedef kimliği (notlara bakın), 4 bayt tamsayı
  Dönem:          Mevcut dönem, 8 bayt tamsayı
  Sonraki İndeks: Liderin son günlük indeksi + 1'ye başlanır, 8 bayt tamsayı
  Kabul Edildi Mi: Eğer kabul edildiyse 1, değilse 0 (notları inceleyin), 1 bayt

{% endhighlight %}

Notlar
`````

Hedef Kimliği genellikle bu mesajın gerçek hedefidir. Ancak, AppendEntriesResponse, AddServerResponse ve RemoveServerResponse için, mevcut liderin kimliğidir.

RequestVoteResponse'ta, Kabul Edildi Mi 1 ise aday için bir oy (istek sahibi), ve 0 ise oy yoktur.

## Uygulama Katmanı

Her Sunucu, bir İstemci İsteği içinde periyodik olarak Uygulama verilerini güncel olarak gönderir. Uygulama verileri her Sunucunun Router'ının durumunu ve Meta LS2 kümesi için Hedefi içerir. Sunucular, Meta LS2'nin yayıncısını ve içeriğini belirlemek için ortak bir algoritma kullanırlar. Günlükteki "en iyi" son duruma sahip sunucu Meta LS2 yayıncısıdır. Meta LS2'nin yayıncısı mutlaka Raft Lideri değildir.

### Uygulama Veri İçeriği

Uygulama içeriği, basitlik ve genişletilebilirlik için UTF-8 kodlamalı [JSON](https://www.json.org/) formatındadır. Tam spesifikasyon TBD (Henüz Belirlenmedi). Amaç, Meta LS2'yi yayınlamak için "en iyi" yönlendiriciyi belirlemek üzere bir algoritma yazmak için yeterli veriyi sağlamak ve yayıncının Meta LS2'deki Hedefleri ağırlıklandırması için yeterli bilgiye sahip olmasını sağlamaktır. Veriler hem yönlendirici hem de Hedef istatistiklerini içerecektir.

Veriler, diğer sunucuların sağlığı ve Meta LS'nin alınma kabiliyeti hakkında uzaktan algılama verileri içerebilir. Bu veriler ilk sürümde desteklenmeyecektir.

Veriler, bir yönetici istemcisi tarafından yayınlanan yapılandırma bilgilerini içerebilir. Bu veriler ilk sürümde desteklenmeyecektir.

"Eşleme: değer" belirtilmişse, bu JSON eşleme anahtarını ve değerini belirtir. Aksi takdirde, belirleme TBD.

Küme verileri (en üst düzey):

- küme: Küme ismi
- tarih: Bu verilerin tarihi (uzun, epoch'tan itibaren milisaniye cinsinden)
- kimlik: Raft Kimliği (tamsayı)

Yapılandırma verileri (config):

- Herhangi bir yapılandırma parametreleri

MetaLS yayınlama durumu (meta):

- hedef: metals hedefi, base64
- sonYayınlananLS: mevcutsa, son yayımlanan metals'in base64 kodlaması
- sonYayınlanmaZamanı: milisaniye olarak veya hiç olmazsa 0
- yayınlamaYapılandırması: Yayıncı yapılandırma durumu kapalı/açık/otomatik
- yayınlıyor: metals yayıncı durumu boolean doğru/yanlış

Yönlendirici verileri (router):

- sonYayınlananRI: mevcutsa, son yayımlanan yönlendirici bilgisinin base64 kodlaması
- çalışma süresi: Milisaniye cinsinden çalışma süresi
- İş gecikmesi
- Keşif tünelleri
- Katılımcı tüneller
- Yapılandırılmış bant genişliği
- Mevcut bant genişliği

Hedefler (destinasyonlar):
Liste

Hedef verileri:

- hedef: hedef, base64
- çalışma süresi: Milisaniye cinsinden çalışma süresi
- Yapılandırılmış tüneller
- Mevcut tüneller
- Yapılandırılmış bant genişliği
- Mevcut bant genişliği
- Yapılandırılmış bağlantılar
- Mevcut bağlantılar
- Kara liste verileri

Uzak yönlendirici algılama verileri:

- Görülen Son RI sürümü
- LS Alma zamanı
- Bağlantı testi verileri
- En yakın floodfills profil verileri
  dünkü, bugünkü ve yarınki zaman aralıkları için

Uzak hedef algılama verileri:

- Görülen Son LS sürümü
- LS Alma zamanı
- Bağlantı testi verileri
- En yakın floodfills profil verileri
  dünkü, bugünkü ve yarınki zaman aralıkları için

Meta LS algılama verileri:

- Görülen son sürüm
- Alma zamanı
- En yakın floodfills profil verileri
  dünkü, bugünkü ve yarınki zaman aralıkları için

## Yönetim Arayüzü

TBD, muhtemelen ayrı bir teklif.
İlk sürüm için gerekli değildir.

Bir yönetim arayüzünün gereksinimleri:

- Birden fazla ana hedefi destekleme, yani birden fazla sanal küme (çiftlik)
- Paylaşılan küme durumunun kapsamlı görünümünü sağlama - üyeler tarafından yayınlanan tüm istatistikler, mevcut lider kim vb.
- Kümedeki bir katılımcıyı veya lideri zorla çıkarma yeteneği
- MetaLS'yi zorla yayınlama yeteneği (mevcut düğüm yayıncı ise)
- Exclude karmaşıklarını metaLS'den çıkarma yeteneği (mevcut düğüm yayıncı ise)
- Toplu dağıtımlar için yapılandırma içe/dışa aktarma işlevselliği

## Yönlendirici Arayüzü

TBD, muhtemelen ayrı bir teklif.
i2pcontrol ilk sürüm için gerekli değildir ve detaylı değişiklikler ayrı bir teklifte bulunacaktır.

Sarımsak Çiftliği için yönlendirici API gereksinimleri (JVM içi Java veya i2pcontrol)

- getLocalRouterStatus()
- getLocalLeafHash(Hash masterHash)
- getLocalLeafStatus(Hash leaf)
- getRemoteMeasuredStatus(Hash masterOrLeaf) // muhtemelen MVP'de yok
- publishMetaLS(Hash masterHash, List<MetaLease> contents) // veya imzalı MetaLeaseSet? Kim imzalıyor?
- stopPublishingMetaLS(Hash masterHash)
- kimlik doğrulama TBD?

## Gerekçe

Atomix çok büyük ve protokolü I2P üzerinden yönlendirme özelleştirmesine izin vermiyor. Ayrıca, kablo formatı belgelenmemiştir ve Java serileştirmesine bağlıdır.

## Notlar

## Sorunlar

- Bir müşterinin bilinmeyen bir lidere nasıl ulaşabileceği ve onunla bağlantı kurabileceği bir yol yok.
  Bir Takipçi'nin AppendEntries Yanıtında Konfigürasyonu bir Günlük Girdisi olarak göndermesi için bir değişiklik küçük olurdu.

## Geçiş

Geriye dönük uyumluluk sorunları yoktur.

## Referanslar

.. [JRAFT]
    https://github.com/datatechnology/jraft

.. [JSON]
    https://json.org/

.. [RAFT]
    https://ramcloud.stanford.edu/wiki/download/attachments/11370504/raft.pdf

.. [RFC-2616]
    https://tools.ietf.org/html/rfc2616

.. [RFC-2617]
    https://tools.ietf.org/html/rfc2617

.. [WEBSOCKET]
    https://en.wikipedia.org/wiki/WebSocket
