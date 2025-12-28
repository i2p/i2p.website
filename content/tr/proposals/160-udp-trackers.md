---
title: "UDP İzleyiciler"
number: "160"
author: "zzz"
created: "2022-01-03"
lastupdated: "2025-06-25"
status: "Kapalı"
thread: "http://zzz.i2p/topics/1634"
target: "0.9.67"
toc: true
---

## Durum

2025-06-24 tarihinde incelemede onaylandı. Spesifikasyon [UDP spesifikasyonu](/docs/specs/udp-bittorrent-announces/) adresindedir. zzzot 0.20.0-beta2'de uygulandı. API 0.9.67 itibariyle i2psnark'ta uygulandı. Durum için diğer uygulamaların belgelerini kontrol edin.

## Genel Bakış

Bu öneri I2P'de UDP tracker'larının uygulanması içindir.

### Change History

I2P'de UDP tracker'lar için ön bir öneri, Mayıs 2014'te [bittorrent spec sayfamızda](/docs/applications/bittorrent/) yayınlanmıştı; bu, resmi öneri sürecimizden önceydi ve hiçbir zaman uygulanmadı. Bu öneri 2022'nin başlarında oluşturuldu ve 2014 versiyonunu basitleştiriyor.

Bu öneri yanıtlanabilir datagramlara dayandığından, 2023 yılının başlarında [Datagram2 önerisi](/proposals/163-datagram2/) üzerinde çalışmaya başladığımızda askıya alındı. Bu öneri Nisan 2025'te onaylandı.

Bu önerinin 2023 versiyonu "uyumluluk" ve "hızlı" olmak üzere iki mod belirtiyordu. Daha ayrıntılı analiz, hızlı modun güvensiz olacağını ve ayrıca çok sayıda torrent'e sahip istemciler için verimsiz olacağını ortaya çıkardı. Ayrıca, BiglyBT uyumluluk modunu tercih ettiğini belirtti. Bu mod, standart [BEP 15](http://www.bittorrent.org/beps/bep_0015.html)'i destekleyen herhangi bir tracker veya istemci için uygulanması daha kolay olacaktır.

Uyumluluk modu, istemci tarafında sıfırdan uygulamak için daha karmaşık olsa da, 2023 yılında başlattığımız ön hazırlık kodumuz mevcut.

Bu nedenle, buradaki mevcut sürüm hızlı modu kaldırmak ve "uyumluluk" terimini çıkarmak için daha da basitleştirilmiştir. Mevcut sürüm yeni Datagram2 formatına geçer ve UDP duyuru uzantı protokolü [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) referansları ekler.

Ayrıca, bu protokolün verimlilik kazanımlarını genişletmek için bağlantı yanıtına bir bağlantı ID yaşam süresi alanı eklenir.

## Motivation

Kullanıcı tabanı genel olarak ve özellikle BitTorrent kullanıcılarının sayısı artmaya devam ettikçe, tracker'ların bunalmayacağı şekilde tracker'ları ve announce'ları daha verimli hale getirmemiz gerekiyor.

Bittorrent, 2008 yılında BEP 15 [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) ile UDP tracker'ları önerdi ve şu anda clearnet üzerindeki tracker'ların büyük çoğunluğu yalnızca UDP kullanıyor.

Datagram'lar ile streaming protokolü arasındaki bant genişliği tasarrufunu hesaplamak zordur. Yanıtlanabilir bir istek, bir streaming SYN ile yaklaşık aynı boyuttadır, ancak HTTP GET'in 600 baytlık devasa URL parametre dizesi olduğu için payload yaklaşık 500 bayt daha küçüktür. Ham yanıt, streaming SYN ACK'den çok daha küçüktür ve tracker'ın giden trafiği için önemli bir azalma sağlar.

Ayrıca, datagramlar streaming bağlantısına göre çok daha az bellek içi durum gerektirdiğinden, implementasyona özel bellek azalmaları da olmalıdır.

[/proposals/169-pq-crypto/](/proposals/169-pq-crypto/) adresinde öngörüldüğü şekliyle Post-Quantum şifreleme ve imzalar, destinasyonlar, leaseSet'ler, streaming SYN ve SYN ACK dahil olmak üzere şifrelenmiş ve imzalanmış yapıların yükünü önemli ölçüde artıracaktır. PQ kripto I2P'de benimsenmeye başlamadan önce mümkün olan yerlerde bu yükü minimize etmek önemlidir.

## Motivasyon

Bu öneri, [/docs/api/datagrams/](/docs/api/datagrams/) bölümünde tanımlandığı şekliyle repliable datagram2, repliable datagram3 ve raw datagramları kullanır. Datagram2 ve Datagram3, Öneri 163 [/proposals/163-datagram2/](/proposals/163-datagram2/) içinde tanımlanan repliable datagramların yeni varyantlarıdır. Datagram2, tekrar saldırısına karşı koruma ve çevrimdışı imza desteği ekler. Datagram3, eski datagram formatından daha küçüktür ancak kimlik doğrulaması içermez.

### BEP 15

Referans için, [BEP 15](http://www.bittorrent.org/beps/bep_0015.html)'te tanımlanan mesaj akışı şu şekildedir:

```
Client                        Tracker
    Connect Req. ------------->
      <-------------- Connect Resp.
    Announce Req. ------------->
      <-------------- Announce Resp.
    Announce Req. ------------->
      <-------------- Announce Resp.
```
Bağlantı aşaması IP adresi sahtekarlığını önlemek için gereklidir. Tracker, istemcinin sonraki duyurularda kullandığı bir bağlantı kimliği döndürür. Bu bağlantı kimliği varsayılan olarak istemcide bir dakika, tracker'da ise iki dakika içinde sona erer.

I2P, mevcut UDP özellikli istemci kod tabanlarında benimsenmesi kolaylığı, verimlilik ve aşağıda tartışılan güvenlik nedenleri için BEP 15 ile aynı mesaj akışını kullanacaktır:

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
Bu durum, streaming (TCP) duyurularına kıyasla potansiyel olarak büyük bir bant genişliği tasarrufu sağlar. Datagram2, streaming SYN ile yaklaşık aynı boyutta olsa da, ham yanıt streaming SYN ACK'den çok daha küçüktür. Sonraki istekler Datagram3 kullanır ve sonraki yanıtlar ham formatındadır.

Announce istekleri Datagram3 türündedir, böylece tracker'ın bağlantı ID'lerini announce hedefine veya hash'e eşleyen büyük bir tablo tutması gerekmez. Bunun yerine, tracker bağlantı ID'lerini gönderen hash'inden, mevcut zaman damgasından (belirli bir aralığa dayalı) ve gizli bir değerden kriptografik olarak oluşturabilir. Bir announce isteği alındığında, tracker bağlantı ID'sini doğrular ve ardından Datagram3 gönderen hash'ini gönderim hedefi olarak kullanır.

### Değişiklik Geçmişi

Entegre bir uygulama (tek süreçte router ve istemci, örneğin i2psnark ve ZzzOT Java eklentisi) veya I2CP tabanlı bir uygulama (örneğin BiglyBT) için, streaming ve datagram trafiğini ayrı ayrı uygulayıp yönlendirmek basit olmalıdır. ZzzOT ve i2psnark'ın bu öneriyi uygulayan ilk tracker ve istemci olması beklenmektedir.

Entegre olmayan tracker'lar ve istemciler aşağıda ele alınmaktadır.

#### Trackers

Bilinen dört I2P tracker uygulaması vardır:

- zzzot, entegre bir Java router eklentisi, opentracker.dg2.i2p ve diğer birkaç yerde çalışıyor
- tracker2.postman.i2p, muhtemelen bir Java router ve HTTP Server tunnel arkasında çalışıyor
- zzz tarafından port edilmiş eski C opentracker, UDP desteği yorumlanmış durumda
- r4sas tarafından port edilmiş yeni C opentracker, opentracker.r4sas.i2p ve muhtemelen diğer yerlerde çalışıyor,
  muhtemelen bir i2pd router ve HTTP Server tunnel arkasında çalışıyor

Şu anda duyuru isteklerini almak için HTTP sunucu tüneli kullanan harici bir tracker uygulaması için, uygulama oldukça zor olabilir. Datagramları yerel HTTP istek/yanıtlarına çevirmek için özelleştirilmiş bir tünel geliştirilebilir. Ya da hem HTTP isteklerini hem de datagramları işleyen ve datagramları harici sürece ileten özelleştirilmiş bir tünel tasarlanabilir. Bu tasarım kararları büyük ölçüde belirli router ve tracker uygulamalarına bağlı olacak ve bu teklifin kapsamı dışında kalmaktadır.

#### Clients

qbittorrent ve diğer libtorrent tabanlı istemciler gibi harici SAM tabanlı torrent istemcileri, i2pd tarafından desteklenmeyen [SAM v3.3](/docs/api/samv3/) gerektirir. Bu aynı zamanda DHT desteği için de gereklidir ve o kadar karmaşıktır ki bilinen hiçbir SAM torrent istemcisi bunu uygulamamıştır. Bu önerinin SAM tabanlı uygulamalarının yakın zamanda beklenmemektedir.

### Connection Lifetime

[BEP 15](http://www.bittorrent.org/beps/bep_0015.html), bağlantı kimliğinin istemcide bir dakikada, tracker'da ise iki dakikada sona ereceğini belirtir. Bu yapılandırılabilir değildir. Bu durum, istemciler tüm duyuruları bir dakikalık pencere içinde toplu olarak yapmadıkça, potansiyel verimlilik kazançlarını sınırlar. i2psnark şu anda duyuruları toplu olarak yapmaz; trafik patlamalarını önlemek için bunları dağıtır. Güçlü kullanıcıların aynı anda binlerce torrent çalıştırdığı bildirilmektedir ve bu kadar çok duyuruyu bir dakika içinde patlatmak gerçekçi değildir.

Burada, bağlantı yanıtını isteğe bağlı bir bağlantı yaşam süresi alanı ekleyecek şekilde genişletmeyi öneriyoruz. Eğer mevcut değilse varsayılan değer bir dakikadır. Aksi takdirde, saniye cinsinden belirtilen yaşam süresi istemci tarafından kullanılacak ve tracker bağlantı ID'sini bir dakika daha koruyacaktır.

### Compatibility with BEP 15

Bu tasarım, mevcut istemciler ve izleyicilerde gerekli değişiklikleri sınırlamak için [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) ile mümkün olduğunca uyumluluğu korur.

Gereken tek değişiklik, announce yanıtındaki peer bilgisinin formatıdır. Connect yanıtına lifetime alanının eklenmesi gerekli değildir ancak yukarıda açıklandığı gibi verimlilik için şiddetle önerilir.

### BEP 15

Bir UDP announce protokolünün önemli bir hedefi, adres sahtekarlığını önlemektir. İstemci gerçekten var olmalı ve gerçek bir leaseset paketlemelidir. Connect Response'u almak için gelen tunnel'lara sahip olmalıdır. Bu tunnel'lar sıfır-hop olabilir ve anında oluşturulabilir, ancak bu yaratıcıyı ifşa ederdi. Bu protokol bu hedefe ulaşır.

### Tracker/Client desteği

- Bu öneri blinded destinationları desteklemez,
  ancak bunu destekleyecek şekilde genişletilebilir. Aşağıya bakın.

## Tasarım

### Protocols and Ports

Repliable Datagram2, I2CP protokol 19'u kullanır; repliable Datagram3, I2CP protokol 20'yi kullanır; ham datagramlar I2CP protokol 18'i kullanır. İstekler Datagram2 veya Datagram3 olabilir. Yanıtlar her zaman hamdır. I2CP protokol 17'yi kullanan eski repliable datagram ("Datagram1") formatı istekler veya yanıtlar için KULLANILMAMALIDIR; bunlar istek/yanıt portlarında alınırsa atılmalıdır. Datagram1 protokol 17'nin hala DHT protokolü için kullanıldığını unutmayın.

İstekler, duyuru URL'sinden I2CP "to port" kullanır; aşağıya bakınız. İstek "from port"u istemci tarafından seçilir, ancak sıfır olmayan ve DHT tarafından kullanılanlardan farklı bir port olmalıdır, böylece yanıtlar kolayca sınıflandırılabilir. Tracker'lar yanlış portta alınan istekleri reddetmelidir.

Yanıtlar istekteki I2CP "to port" değerini kullanır. İsteğin "from port" değeri, istekteki "to port" değeridir.

### Announce URL

Announce URL formatı [BEP 15](http://www.bittorrent.org/beps/bep_0015.html)'te belirtilmemiştir, ancak clearnet'te olduğu gibi, UDP announce URL'leri "udp://host:port/path" biçimindedir. Path kısmı göz ardı edilir ve boş olabilir, ancak clearnet'te tipik olarak "/announce" şeklindedir. :port kısmı her zaman mevcut olmalıdır, ancak ":port" kısmı atlanırsa, clearnet'te yaygın port olduğu için varsayılan I2CP portu olan 6969'u kullanın. Ayrıca eklenmiş &a=b&c=d cgi parametreleri de olabilir, bunlar işlenebilir ve announce isteğinde sağlanabilir, bkz. [BEP 41](http://www.bittorrent.org/beps/bep_0041.html). Parametre veya path yoksa, [BEP 41](http://www.bittorrent.org/beps/bep_0041.html)'de ima edildiği gibi sondaki / de atlanabilir.

### Bağlantı Yaşam Süresi

Tüm değerler network byte sırası (big endian) ile gönderilir. Paketlerin tam olarak belirli bir boyutta olmasını beklemeyin. Gelecekteki uzantılar paketlerin boyutunu artırabilir.

#### Connect Request

İstemciden tracker'a. 16 byte. Yanıtlanabilir Datagram2 olmalıdır. [BEP 15](http://www.bittorrent.org/beps/bep_0015.html)'teki ile aynı. Değişiklik yok.

```
Offset  Size            Name            Value
  0       64-bit integer  protocol_id     0x41727101980 // magic constant
  8       32-bit integer  action          0 // connect
  12      32-bit integer  transaction_id
```
#### Connect Response

Tracker'dan istemciye. 16 veya 18 bayt. Ham olmalıdır. Aşağıda belirtilen durumlar dışında [BEP 15](http://www.bittorrent.org/beps/bep_0015.html)'teki ile aynıdır.

```
Offset  Size            Name            Value
  0       32-bit integer  action          0 // connect
  4       32-bit integer  transaction_id
  8       64-bit integer  connection_id
  16      16-bit integer  lifetime        optional  // Change from BEP 15
```
Yanıt, istek "from port"u olarak alınan I2CP "to port"una gönderilmelidir.

lifetime alanı isteğe bağlıdır ve connection_id istemci yaşam süresini saniye cinsinden belirtir. Varsayılan değer 60'tır ve belirtildiğinde minimum değer 60'tır. Maksimum değer 65535 veya yaklaşık 18 saattir. Tracker, connection_id'yi istemci yaşam süresinden 60 saniye daha fazla süreyle korumalıdır.

#### Announce Request

İstemciden tracker'a. En az 98 bayt. Yanıtlanabilir Datagram3 olmalıdır. Aşağıda belirtilen durumlar dışında [BEP 15](http://www.bittorrent.org/beps/bep_0015.html)'teki ile aynı.

connection_id, connect yanıtında alındığı şekliyledir.

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
  84      32-bit integer  IP address      0     // default
  88      32-bit integer  key
  92      32-bit integer  num_want        -1    // default
  96      16-bit integer  port
  98      varies          options     optional  // As specified in BEP 41
```
[BEP 15](http://www.bittorrent.org/beps/bep_0015.html)'ten yapılan değişiklikler:

- key göz ardı edilir
- port muhtemelen göz ardı edilir
- Seçenekler bölümü, varsa, [BEP 41](http://www.bittorrent.org/beps/bep_0041.html)'de tanımlandığı gibidir

Yanıt, istek "from port"u olarak alınan I2CP "to port"una gönderilmek ZORUNDADIR. Announce isteğindeki portu kullanmayın.

#### Announce Response

Tracker'dan istemciye. En az 20 bayt. Ham olmalıdır. Aşağıda belirtildiği haller dışında [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) ile aynıdır.

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
[BEP 15](http://www.bittorrent.org/beps/bep_0015.html)'ten yapılan değişiklikler:

- 6-byte IPv4+port veya 18-byte IPv6+port yerine, SHA-256 binary peer hash'leriyle
  32-byte'lık "compact responses" katları döndürürüz.
  TCP compact responses'larda olduğu gibi, bir port dahil etmiyoruz.

Yanıt, istek "from port"u olarak alınan I2CP "to port"una GÖNDERİLMELİDİR. Duyuru isteğindeki portu kullanmayın.

I2P datagramları yaklaşık 64 KB'lık çok büyük bir maksimum boyuta sahiptir; ancak güvenilir teslimat için 4 KB'dan büyük datagramlardan kaçınılmalıdır. Bant genişliği verimliliği için, tracker'lar muhtemelen maksimum peer sayısını yaklaşık 50 ile sınırlamalıdır, bu da çeşitli katmanlardaki overhead öncesinde yaklaşık 1600 baytlık bir pakete karşılık gelir ve parçalanma sonrasında iki-tunnel-message payload sınırı içinde olmalıdır.

BEP 15'te olduğu gibi, takip edilecek peer adreslerinin sayısını belirten bir sayım bulunmamaktadır (BEP 15 için IP/port, burada ise hash'ler). BEP 15'te öngörülmemişken, peer bilgisinin tamamlandığını ve bazı ek verilerin izlediğini belirtmek için tamamı sıfırlardan oluşan bir peer-sonu işaretleyicisi tanımlanabilir.

Gelecekte genişletme mümkün olması için, istemciler 32-byte'lık tüm sıfırlardan oluşan hash'i ve ardından gelen herhangi bir veriyi görmezden gelmelidir. Tracker'lar tüm sıfırlardan oluşan hash'ten gelen duyuruları reddetmelidir, ancak bu hash zaten Java router'ları tarafından yasaklanmıştır.

#### Scrape

[BEP 15](http://www.bittorrent.org/beps/bep_0015.html)'ten scrape isteği/yanıtı bu öneri tarafından gerekli değildir, ancak istenirse uygulanabilir, herhangi bir değişiklik gerekmez. İstemci önce bir bağlantı ID'si almalıdır. Scrape isteği her zaman yanıtlanabilir Datagram3'tür. Scrape yanıtı her zaman raw'dır.

#### İzleyiciler

Tracker'dan client'a. Minimum 8 bayt (mesaj boşsa). Ham olmalı. [BEP 15](http://www.bittorrent.org/beps/bep_0015.html)'teki ile aynı. Değişiklik yok.

```
Offset  Size            Name            Value
  0       32-bit integer  action          3 // error
  4       32-bit integer  transaction_id
  8       string          message
```
## Extensions

Extension bitleri veya bir versiyon alanı dahil edilmemiştir. İstemciler ve tracker'lar paketlerin belirli bir boyutta olduğunu varsaymamalıdır. Bu şekilde, uyumluluğu bozmadan ek alanlar eklenebilir. Gerekli olması durumunda [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) içinde tanımlanan extension formatı önerilir.

Bağlantı yanıtı, isteğe bağlı bir bağlantı ID ömrü eklemek için değiştirildi.

Blinded destination desteği gerekiyorsa, announce isteğinin sonuna blinded 35-byte adresini ekleyebilir veya [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) formatını kullanarak yanıtlarda blinded hash'leri talep edebiliriz (parametreler TBD). Blinded 35-byte peer adreslerinin kümesi, tamamen sıfırlardan oluşan 32-byte hash'ten sonra announce yanıtının sonuna eklenebilir.

## Implementation guidelines

Entegre olmayan, I2CP olmayan istemciler ve tracker'lar için zorlukların tartışılması için yukarıdaki tasarım bölümüne bakın.

### BEP 15 ile Uyumluluk

Belirli bir tracker hostname'i için, bir istemci UDP'yi HTTP URL'lerinden önce tercih etmeli ve her ikisine birden announce yapmamalıdır.

Mevcut BEP 15 desteğine sahip istemciler yalnızca küçük değişiklikler gerektirir.

Bir istemci DHT veya diğer datagram protokollerini destekliyorsa, muhtemelen yanıtların o porta geri gelmesi ve DHT mesajları ile karışmaması için istek "kaynak port" olarak farklı bir port seçmelidir. İstemci yanıt olarak yalnızca ham datagramlar alır. Tracker'lar hiçbir zaman istemciye yanıtlanabilir datagram2 göndermez.

Varsayılan opentracker listesine sahip istemciler, bilinen opentracker'ların UDP desteklediği bilindiğinde UDP URL'lerini eklemek için listeyi güncellemelidir.

İstemciler isteklerin yeniden iletimini uygulayabilir veya uygulamayabilir. Yeniden iletimler, eğer uygulanırsa, en az 15 saniyelik bir başlangıç zaman aşımı kullanmalı ve her yeniden iletim için zaman aşımını ikiye katlamalıdır (üstel geri çekilme).

İstemciler bir hata yanıtı aldıktan sonra geri çekilmelidir.

### Güvenlik Analizi

Mevcut BEP 15 desteğine sahip tracker'lar yalnızca küçük değişiklikler gerektirecektir. Bu öneri, 2014 önerisinden farklı olarak, tracker'ın aynı port üzerinde yanıtlanabilir datagram2 ve datagram3 alımını desteklemesi gerektiği açısından ayrılır.

Tracker kaynak gereksinimlerini en aza indirmek için, bu protokol tracker'ın daha sonraki doğrulama için istemci hash'lerinin bağlantı ID'lerine eşlemelerini saklamasına yönelik herhangi bir gerekliliği ortadan kaldıracak şekilde tasarlanmıştır. Bu mümkündür çünkü duyuru istek paketi yanıtlanabilir bir Datagram3 paketidir, dolayısıyla gönderenin hash'ini içerir.

Önerilen bir uygulama şöyledir:

- Mevcut epoch'u bağlantı yaşam süresi çözünürlüğü ile mevcut zaman olarak tanımlayın,
  ``epoch = now / lifetime``.
- 8 bayt çıktı üreten ``H(secret, clienthash, epoch)`` kriptografik hash fonksiyonunu tanımlayın.
- Tüm bağlantılar için kullanılan rastgele sabit secret değerini oluşturun.
- Bağlantı yanıtları için ``connection_id = H(secret,  clienthash, epoch)`` oluşturun
- Duyuru istekleri için, alınan bağlantı ID'sini mevcut epoch'ta şu şekilde doğrulayarak geçerli kılın
  ``connection_id == H(secret, clienthash, epoch) || connection_id == H(secret, clienthash, epoch - 1)``

## Migration

Mevcut istemciler UDP announce URL'lerini desteklemez ve bunları yok sayar.

Mevcut tracker'lar yanıtlanabilir veya ham datagram'ların alınmasını desteklemez, bunlar düşürülecektir.

Bu öneri tamamen isteğe bağlıdır. Ne istemciler ne de tracker'lar bunu herhangi bir zamanda uygulamak zorunda değildirler.

## Rollout

İlk uygulamaların ZzzOT ve i2psnark'ta olması beklenmektedir. Bu öneri için test etme ve doğrulama amacıyla kullanılacaklardır.

Diğer uygulamalar, test ve doğrulama tamamlandıktan sonra istenildiği şekilde takip edecektir.
