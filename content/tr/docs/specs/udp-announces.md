---
title: "UDP BitTorrent Duyuruları"
description: "I2P'de UDP tabanlı BitTorrent tracker announce (duyuru isteği) için protokol spesifikasyonu"
slug: "udp-bittorrent-announces"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Genel Bakış

Bu belirtim, I2P'de UDP BitTorrent duyuruları için protokolü belgeler. I2P'de BitTorrent'in genel belirtimi için [I2P üzerinde BitTorrent belgelendirmesi](/docs/applications/bittorrent/) sayfasına bakın. Bu belirtimin geliştirilmesine ilişkin arka plan ve ek bilgiler için [Öneri 160](/proposals/160-udp-trackers/) sayfasına bakın.

Bu protokol 24 Haziran 2025’te resmen onaylandı ve I2P 2.10.0 (API 0.9.67) sürümünde uygulandı; bu sürüm 8 Eylül 2025’te yayınlandı. UDP izleyici desteği, birden fazla üretim ortamı izleyicisi ve tam i2psnark istemci desteğiyle şu anda I2P ağında çalışır durumdadır.

## Tasarım

Bu belirtim, [I2P Datagram Specification](/docs/api/datagrams/) içinde tanımlandığı gibi, yanıtlanabilir datagram2, yanıtlanabilir datagram3 ve ham datagramları kullanır. Datagram2 ve Datagram3, [Proposal 163](/proposals/163-datagram2/) içinde tanımlanan yanıtlanabilir datagramların varyantlarıdır. Datagram2, yeniden oynatma saldırılarına karşı direnç ve çevrimdışı imza desteği ekler. Datagram3, eski datagram biçiminden daha küçüktür, ancak kimlik doğrulaması yoktur.

### BEP 15 (BitTorrent Geliştirme Önerisi 15)

Referans için, [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) belgesinde tanımlanan mesaj akışı şu şekildedir:

```
Client                        Tracker
  Connect Req. ------------->
    <-------------- Connect Resp.
  Announce Req. ------------->
    <-------------- Announce Resp.
  Announce Req. ------------->
    <-------------- Announce Resp.
```
IP adresi sahteciliğini önlemek için bağlantı kurma aşaması gereklidir. Tracker, istemcinin sonraki duyuru isteklerinde kullanacağı bir bağlantı kimliği döndürür. Bu bağlantı kimliği, varsayılan olarak istemci tarafında bir dakika içinde, tracker tarafında ise iki dakika içinde geçerliliğini yitirir.

I2P, mevcut UDP yetenekli istemci kod tabanlarında benimsenmeyi kolaylaştırmak, verimlilik ve aşağıda tartışılan güvenlik nedenleri için BEP 15 (BitTorrent Geliştirme Önerisi 15) ile aynı mesaj akışını kullanır:

```
Client                        Tracker
  Connect Req. ------------->       (Repliable Datagram2)
    <-------------- Connect Resp.   (Raw)
  Announce Req. ------------->      (Repliable Datagram3)
    <-------------- Announce Resp.  (Raw)
  Announce Req. ------------->      (Repliable Datagram3)
    <-------------- Announce Resp.  (Raw)
           ...
```
Bu, streaming (TCP) duyurularına kıyasla potansiyel olarak büyük bir bant genişliği tasarrufu sağlar. Datagram2, bir streaming SYN ile yaklaşık aynı boyutta olsa da, ham yanıt, streaming SYN ACK’ten çok daha küçüktür. Sonraki istekler Datagram3 kullanır ve sonraki yanıtlar hamdır.

Tracker (izleyici sunucu)ın bağlantı kimliklerini announce hedeflerine veya hash’e eşleyen büyük bir eşleme tablosu tutmasına gerek kalmaması için announce istekleri Datagram3 biçimindedir. Bunun yerine, tracker, gönderen hash’inden, mevcut zaman damgasından (belirli bir aralığa dayalı) ve gizli bir değerden kriptografik olarak bağlantı kimlikleri üretebilir. Bir announce isteği alındığında, tracker bağlantı kimliğini doğrular ve ardından gönderim hedefi olarak Datagram3 gönderen hash’ini kullanır.

### Bağlantı Ömrü

[BEP 15](http://www.bittorrent.org/beps/bep_0015.html), bağlantı kimliğinin istemcide bir dakika içinde, tracker (izleyici sunucu) tarafında ise iki dakika içinde süresinin dolduğunu belirtir. Bu yapılandırılabilir değildir. Bu durum, istemciler tüm announce'ları (duyuru isteği) bir dakikalık bir zaman dilimi içinde toplu halde göndermedikçe olası verimlilik kazanımlarını sınırlar. i2psnark şu anda announce'ları toplu göndermiyor; trafik patlamalarını önlemek için bunları zamana yayar. İleri düzey kullanıcıların aynı anda binlerce torrent çalıştırdığı bildiriliyor ve bu kadar çok announce'ı bir dakikaya sığdırmak gerçekçi değildir.

Burada, bağlantı yanıtını isteğe bağlı bir bağlantı ömrü alanı ekleyecek şekilde genişletmeyi öneriyoruz. Alan yoksa varsayılan bir dakikadır. Aksi halde, istemci saniye cinsinden belirtilen ömrü kullanacak ve izleyici bağlantı kimliğini buna ek olarak bir dakika daha muhafaza edecektir.

### BEP 15 (BitTorrent Geliştirme Önerisi 15) ile uyumluluk

Bu tasarım, mevcut istemciler ve izleyicilerde gereken değişiklikleri sınırlamak için mümkün olduğunca [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) ile uyumluluğu korur.

Zorunlu tek değişiklik, announce yanıtındaki peer info biçimidir. Connect yanıtına lifetime alanının eklenmesi zorunlu değildir ancak yukarıda açıklandığı gibi verimlilik açısından şiddetle önerilir.

### Güvenlik Analizi

Bir UDP duyuru protokolünün önemli bir amacı, adres sahteciliğini önlemektir. İstemci gerçekten var olmalı ve gerçek bir leaseSet'i eklemelidir. Connect Response'u alabilmek için gelen tunnel'lere sahip olmalıdır. Bu tunnel'ler zero-hop (sıfır atlamalı) olabilir ve anında kurulabilirler, ancak bu durum oluşturucuyu açığa çıkarır. Bu protokol bu amaca ulaşır.

### Sorunlar

Bu protokol körleştirilmiş hedefleri desteklemez, ancak bunu destekleyecek şekilde genişletilebilir. Aşağıya bakın.

## Teknik Şartname

### Protokoller ve Bağlantı Noktaları

Yanıtlanabilir Datagram2, I2CP protokolü 19’u kullanır; yanıtlanabilir Datagram3, I2CP protokolü 20’yi kullanır; ham datagramlar I2CP protokolü 18’i kullanır. İstekler Datagram2 veya Datagram3 olabilir. Yanıtlar her zaman hamdır. I2CP protokolü 17’yi kullanan eski yanıtlanabilir datagram ("Datagram1") biçimi istekler veya yanıtlar için KESİNLİKLE kullanılmamalıdır; istek/yanıt portlarında alınırsa bunlar düşürülmelidir. Datagram1’in 17 numaralı protokolünün DHT protokolü için hâlâ kullanıldığını unutmayın.

İsteklerde, announce URL’sinden alınan I2CP "to port" değeri kullanılır; aşağıya bakın. İstek için "from port" istemci tarafından seçilir, ancak sıfır olmamalı ve yanıtların kolayca sınıflandırılabilmesi için DHT (Dağıtık Hash Tablosu) tarafından kullanılanlardan farklı bir port olmalıdır. Tracker’lar yanlış porttan gelen istekleri reddetmelidir.

Yanıtlar, istekteki I2CP "to port" değerini kullanır. Yanıtın "from port" değeri, istekteki "to port" değeridir.

### Duyuru URL'si

[BEP 15](http://www.bittorrent.org/beps/bep_0015.html)’te announce URL biçimi belirtilmemiştir, ancak açık internette olduğu gibi, UDP announce URL’leri "udp://host:port/path" biçimindedir. Yol (path) yok sayılır ve boş olabilir, ancak açık internette genellikle "/announce" olur. ":port" kısmı her zaman bulunmalıdır; ancak ":port" kısmı atlanmışsa, açık internette yaygın olarak kullanılan port olduğu için varsayılan I2CP portu olarak 6969’u kullanın. Ayrıca sonuna &a=b&c=d gibi CGI parametreleri eklenmiş olabilir; bunlar işlenip duyuru isteğinde sunulabilir, bkz. [BEP 41](http://www.bittorrent.org/beps/bep_0041.html). Parametreler veya yol yoksa, [BEP 41](http://www.bittorrent.org/beps/bep_0041.html)’de ima edildiği gibi, sondaki / da atlanabilir.

### Datagram Biçimleri

Tüm değerler ağ bayt sırası (big endian; en anlamlı bayt önce) ile gönderilir. Paketlerin tam olarak belirli bir boyutta olmasını beklemeyin. Gelecekteki genişletmeler paketlerin boyutunu artırabilir.

#### Bağlantı İsteği

İstemciden trackere (izleyici). 16 bayt. Yanıtlanabilir bir Datagram2 olmalıdır. [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) ile aynıdır. Değişiklik yok.

```
Offset  Size            Name            Value
0       64-bit integer  protocol_id     0x41727101980 // magic constant
8       32-bit integer  action          0 // connect
12      32-bit integer  transaction_id
```
#### Bağlantı Yanıtı

İstemciye tracker (izleyici sunucu) tarafından. 16 ya da 18 bayt. Ham olmalıdır. Aşağıda belirtilenler dışında [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) ile aynıdır.

```
Offset  Size            Name            Value
0       32-bit integer  action          0 // connect
4       32-bit integer  transaction_id
8       64-bit integer  connection_id
16      16-bit integer  lifetime        optional  // Change from BEP 15
```
Yanıt, istek "from port" olarak alınan I2CP "to port"a gönderilmelidir.

lifetime alanı isteğe bağlıdır ve connection_id için istemci ömrünü saniye cinsinden belirtir. Varsayılan 60’tır ve belirtilmişse asgari değer 60’tır. Azami değer 65535’tir (yaklaşık 18 saat). Tracker (izleyici sunucusu), connection_id değerini istemci ömründen 60 saniye daha uzun süre korumalıdır.

#### Duyuru İsteği

İstemciden izleyiciye. En az 98 bayt. Yanıtlanabilir Datagram3 (Datagram sürüm 3) olmalıdır. Aşağıda belirtilenler dışında [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) ile aynıdır.

connection_id, connect yanıtında alındığı gibidir.

```
Offset  Size            Name            Value
0       64-bit integer  connection_id
8       32-bit integer  action          1     // announce
12      32-bit integer  transaction_id
16      20-byte string  info_hash
36      20-byte string  peer_id
56      64-bit integer  downloaded
64      64-bit integer  left
72      64-bit integer  uploaded
80      32-bit integer  event           0     // 0: none; 1: completed; 2: started; 3: stopped
84      32-bit integer  IP address      0     // default, unused in I2P
88      32-bit integer  key
92      32-bit integer  num_want        -1    // default
96      16-bit integer  port                  // must be same as I2CP from port
98      varies          options     optional  // As specified in BEP 41
```
[BEP 15](http://www.bittorrent.org/beps/bep_0015.html)'e göre değişiklikler:

- anahtar yok sayılır
- IP adresi kullanılmaz
- bağlantı noktası muhtemelen yok sayılır ama I2CP from port ile aynı olmalıdır
- Seçenekler bölümü, varsa, [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) belgesinde tanımlandığı gibidir

Yanıt, istek sırasında "from port" olarak alınan I2CP "to port" alanına gönderilmelidir. Duyuru isteğindeki portu kullanmayın.

#### Duyuru Yanıtı

Tracker'dan istemciye. En az 20 bayt. Ham olmalıdır. Aşağıda belirtilenler dışında [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) ile aynıdır.

```
Offset  Size            Name            Value
0           32-bit integer  action          1 // announce
4           32-bit integer  transaction_id
8           32-bit integer  interval
12          32-bit integer  leechers
16          32-bit integer  seeders
20   32 * n 32-byte hash    binary hashes     // Change from BEP 15
...                                           // Change from BEP 15
```
[BEP 15](http://www.bittorrent.org/beps/bep_0015.html)'e göre değişiklikler:

- 6 baytlık IPv4+bağlantı noktası veya 18 baytlık IPv6+bağlantı noktası yerine, SHA-256 ikili eş karmalarını içeren, her biri 32 bayt olan "compact responses" (kompakt yanıtlar) öğelerinin katları halinde döndürürüz. TCP compact responses ile olduğu gibi, bir bağlantı noktası eklemeyiz.

Yanıt, istekte "from port" olarak bildirilen değeri I2CP "to port" olarak kullanarak gönderilmek zorundadır. Duyuru isteğindeki bağlantı noktasını kullanmayın.

I2P datagramlar yaklaşık 64 KB’lık çok büyük bir azami boyuta sahiptir; ancak, güvenilir iletim için 4 KB’den büyük datagramlardan kaçınılmalıdır. Bant kullanımında verimlilik için, tracker’lar (torrent izleme sunucuları) azami eş sayısını muhtemelen yaklaşık 50 ile sınırlandırmalıdır; bu, çeşitli katmanlardaki ek yükten önce yaklaşık 1600 baytlık bir pakete karşılık gelir ve parçalandıktan sonra iki tunnel iletisi yük sınırının içinde kalmalıdır.

BEP 15’te olduğu gibi, takip edecek eş adreslerinin (BEP 15 için IP/port, burada ise hash’ler) sayısı dahil edilmemiştir. BEP 15’te düşünülmemiş olsa da, eş bilgileri tamamlandığını ve ardından bazı uzantı verilerinin geleceğini belirtmek için tamamı sıfırlardan oluşan bir end-of-peers marker (eşler-sonu işaretleyici) tanımlanabilir.

Gelecekte bu genişletme mümkün olabilsin diye, istemciler 32 baytlık, tamamen sıfırlardan oluşan bir hash’i ve onu izleyen tüm verileri göz ardı etmelidir. Tracker’lar, tamamen sıfırlardan oluşan bir hash’ten gelen announce’ları reddetmelidir; gerçi bu hash halihazırda Java router’lar tarafından yasaklanmıştır.

#### Kazıma

[BEP 15](http://www.bittorrent.org/beps/bep_0015.html)'te tanımlanan scrape (tracker/izleyici durumu sorgusu) isteği/yanıtı bu belirtim tarafından zorunlu değildir; ancak istenirse herhangi bir değişiklik gerektirmeden uygulanabilir. İstemci önce bir bağlantı kimliği edinmelidir. Scrape isteği her zaman yanıtlanabilir Datagram3'tür. Scrape yanıtı her zaman hamdır.

#### Hata Yanıtı

İzleyiciden istemciye. En az 8 bayt (mesaj boşsa). Ham olmalıdır. [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) ile aynıdır. Değişiklik yok.

```
Offset  Size            Name            Value
0       32-bit integer  action          3 // error
4       32-bit integer  transaction_id
8       string          message
```
## Uzantılar

Uzantı bitleri veya bir sürüm alanı dahil edilmez. İstemciler ve tracker'lar (izleyiciler), paketlerin belirli bir boyutta olduğunu varsaymamalıdır. Bu sayede, uyumluluğu bozmadan ilave alanlar eklenebilir. Gerekirse, [BEP 41](http://www.bittorrent.org/beps/bep_0041.html)'de tanımlanan uzantılar biçimi önerilir.

Bağlanma yanıtı, isteğe bağlı bir bağlantı kimliği yaşam süresi eklemek için değiştirildi.

Körleştirilmiş hedef desteği gerekiyorsa, körleştirilmiş 35 baytlık adresi announce isteğinin sonuna ekleyebiliriz ya da [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) biçimini kullanarak (parametreler belirlenecek) yanıtlarda körleştirilmiş hash'ler talep edebiliriz. Tümü sıfırlardan oluşan 32 baytlık bir hash'in ardından, körleştirilmiş 35 baytlık eş (peer) adreslerinin kümesi announce yanıtının sonuna eklenebilir.

## Uygulama Yönergeleri

Entegre olmayan ve I2CP kullanmayan istemci ve tracker'ların (izleyici sunucuları) karşılaştığı zorlukların tartışıldığı yukarıdaki tasarım bölümüne bakın.

### İstemciler

Belirli bir izleyici ana makine adı için, istemci HTTP URL’lerine kıyasla UDP’yi tercih etmeli ve ikisine birden duyuru yapmamalıdır.

Mevcut BEP 15 desteğine sahip istemciler yalnızca küçük değişiklikler gerektirmelidir.

Bir istemci DHT veya diğer datagram protokollerini destekliyorsa, yanıtların o porta dönmesi ve DHT iletileriyle karışmaması için, isteğin "from port" değeri olarak muhtemelen farklı bir port seçmelidir. İstemci, yanıt olarak yalnızca ham datagramlar alır. Tracker'lar istemciye asla yanıtlanabilir bir datagram2 göndermez.

Varsayılan opentracker (herkese açık tracker) listesine sahip istemciler, bilinen opentracker'ların UDP'yi desteklediği doğrulandıktan sonra, listeyi UDP URL'leri ekleyecek şekilde güncellemelidir.

İstemciler, isteklerin yeniden iletimini uygulayabilir veya uygulamayabilir. Yeniden iletimler, uygulanırsa, en az 15 saniyelik bir başlangıç zaman aşımı kullanmalı ve her yeniden iletimde zaman aşımını ikiye katlamalıdır (exponential backoff (üstel geri çekilme)).

İstemciler bir hata yanıtı aldıktan sonra back off (yeniden denemeleri geciktirerek istek hızını azaltma) uygulamalıdır.

### İzleyiciler

Mevcut BEP 15 desteğine sahip tracker'ların (izleyici) yalnızca küçük değişiklikler gerektirmesi beklenir. Bu spesifikasyon, 2014 tarihli öneriden şu açıdan farklıdır: tracker aynı bağlantı noktasında repliable datagram2 ve datagram3 alımını desteklemelidir.

Tracker (izleyici) kaynak gereksinimlerini en aza indirmek için, bu protokol, tracker’ın daha sonra doğrulama amacıyla istemci karmalarının bağlantı kimlikleriyle eşlemelerini depolamasını gerektiren herhangi bir zorunluluğu ortadan kaldıracak şekilde tasarlanmıştır. Bu, announce (duyuru) istek paketinin yanıtlanabilir bir Datagram3 paketi olması sayesinde mümkündür; bu nedenle gönderenin karmasını içerir.

Önerilen bir gerçekleme şöyledir:

- Mevcut epoku, bağlantı ömrü çözünürlüğüyle ölçülen mevcut zaman olarak tanımlayın, `epoch = now / lifetime`.
- 8 bayt çıktısı üreten bir kriptografik özet (hash) fonksiyonunu `H(secret, clienthash, epoch)` olarak tanımlayın.
- Tüm bağlantılarda kullanılacak rastgele sabit gizli değeri üretin.
- Bağlantı yanıtlarında `connection_id = H(secret, clienthash, epoch)` üretin
- Announce isteklerinde, alınan bağlantı kimliğini mevcut epokta doğrulamak için `connection_id == H(secret, clienthash, epoch) || connection_id == H(secret, clienthash, epoch - 1)` ifadesini doğrulayın

## Dağıtım Durumu

Bu protokol 24 Haziran 2025 tarihinde onaylandı ve Eylül 2025 itibarıyla I2P ağında tamamen faaliyette.

### Mevcut Gerçeklemeler

**i2psnark**: 8 Eylül 2025'te yayımlanan I2P sürüm 2.10.0'da (API 0.9.67) tam UDP tracker (izleyici sunucusu) desteği yer almaktadır. Bu sürümden itibaren tüm I2P kurulumları varsayılan olarak UDP tracker özelliğini içerir.

**zzzot tracker**: Sürüm 0.20.0-beta2 ve üzeri UDP duyurularını destekler. Ekim 2025 itibarıyla, aşağıdaki production tracker'lar çalışır durumdadır: - opentracker.dg2.i2p - opentracker.simp.i2p - opentracker.skank.i2p

### İstemci Uyumluluk Notları

**SAM v3.3 sınırlamaları**: SAM (Simple Anonymous Messaging) kullanan harici BitTorrent istemcileri, Datagram2/3 için SAM v3.3 desteği gerektirir. Bu, Java I2P'de mevcutken i2pd (C++ I2P uygulaması) tarafından şu anda desteklenmemektedir; bu da qBittorrent gibi libtorrent tabanlı istemcilerde benimsenmesini sınırlayabilir.

**I2CP istemcileri**: I2CP'yi doğrudan kullanan istemciler (örneğin BiglyBT), SAM sınırlamaları olmadan UDP tracker desteğini uygulayabilir.

## Kaynaklar

- **[BEP15]**: [BitTorrent UDP Tracker Protokolü](http://www.bittorrent.org/beps/bep_0015.html)
- **[BEP41]**: [UDP Tracker Protokolü Uzantıları](http://www.bittorrent.org/beps/bep_0041.html)
- **[DATAGRAMS]**: [I2P Datagramları Şartnamesi](/docs/api/datagrams/)
- **[Prop160]**: [UDP Tracker'lar için Öneri](/proposals/160-udp-trackers/)
- **[Prop163]**: [Datagram2 Önerisi](/proposals/163-datagram2/)
- **[SPEC]**: [I2P üzerinden BitTorrent](/docs/applications/bittorrent/)
