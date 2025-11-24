---
title: "UDP İzleyicileri"
number: "160"
author: "zzz"
created: "2022-01-03"
lastupdated: "2025-06-25"
status: "Kapandı"
thread: "http://zzz.i2p/topics/1634"
target: "0.9.67"
---

## Durum

2025-06-24'te gözden geçirildi ve onaylandı.
Spesifikasyon [UDP]'de bulunmaktadır.
Zzzot 0.20.0-beta2'de uygulandı.
API 0.9.67 itibarıyla i2psnark'ta uygulandı.
Durum için diğer uygulamaların belgelerinin kontrol edilmesi gerekmektedir.

## Genel Bakış

Bu teklif, I2P'de UDP izleyicilerinin uygulanması içindir.

### Değişiklik Geçmişi

Mayıs 2014'te I2P'de UDP izleyicilerine ilişkin ön bir teklif bittorrent spesifikasyon sayfamıza [/en/docs/applications/bittorrent/](/en/docs/applications/bittorrent/)
yüklendi; bu, resmi teklif sürecimizden öncesine aitti ve hiçbir zaman uygulanmadı.
Bu teklif 2022'nin başlarında oluşturuldu ve 2014 versiyonunu basitleştiriyor.

Bu teklif, yanıt verilebilir datagramlara dayandığı için 2023 başlarında Datagram2 teklifi [/en/proposals/163-datagram2/](/en/proposals/163-datagram2/) üzerinde
çalışmaya başladığımızda askıya alındı.
Bu teklif Nisan 2025'te onaylandı.

2023 versiyonu bu teklifi, "uyumluluk" ve "hızlı" olmak üzere iki mod olarak belirtiyordu.
Daha fazla analiz, hızlı modun güvensiz olacağını ve çok sayıda torrente sahip
olan istemciler için verimsiz olacağını ortaya çıkardı.
Ayrıca, BiglyBT uyumluluk modunu tercih ettiğini belirtti.
Bu mod, standart [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) destekleyen herhangi bir izleyici veya istemci için daha kolay uygulanır.

Uyumluluk modu, istemciden sıfırdan uygulamak için daha karmaşık olmasına rağmen,
2023'te başlamış olan ön kodumuz bulunmaktadır.

Bu nedenle, buradaki mevcut versiyon daha da sadeleştirildi ve hızlı
mod kaldırıldı, "uyumluluk" terimi de kaldırıldı. Mevcut versiyon yeni Datagram2
formatına geçiyor ve UDP duyuru uzantı protokolüne [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) referanslar ekliyor.

Ayrıca, protokolün verimlilik kazançlarını artırmak için bağlantı ID'si ömrü alanı
bağlantı yanıtına eklenmiştir.

## Gerekçe

Kullanıcı tabanı genel olarak ve özellikle bittorrent kullanıcılarının sayısı artmaya devam ettikçe,
izleyicilerin ve duyuruların daha verimli hale getirilmesi gerekmektedir aksi halde izleyiciler
ağır yük altına girerler.

Bittorrent, 2008'de BEP 15'te [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) UDP izleyicilerini önerdi ve şu anda açık internetteki
izleyicilerin büyük çoğunluğu yalnızca UDP'dir.

Datagramların ve akış protokolünün bant genişliği tasarrufunu hesaplamak zordur.
Yanıt verilebilir bir istek, bir akış SYN'si ile aynı boyuttadır, ancak yük
yaklaşık 500 bayt daha küçüktür çünkü HTTP GET devasa bir 600 bayt
URL parametre dizesine sahiptir.
Ham yanıt, çıkış yapan trafikte önemli bir azaltma sağlayarak
bir akış SYN ACK'den çok daha küçüktür.

Ek olarak, uygulamaya özel bellek azaltımları olmalıdır, çünkü
datagramlar, bir akış bağlantısından çok daha az bellek içi duruma ihtiyaç duyar.

[Prop169]'ta öngörülen Kuantum Sonrası şifreleme ve imzalar,
şifrelenmiş ve imzalı yapılar, hedefler dahil, önemli ölçüde artıracaktır.
leasing setleri, akış SYN ve SYN ACK. Bu
fazlalığı, PQ kriptografisi I2P'de benimsenmeden önce mümkün olduğunca
azaltmak önemlidir.

## Tasarım

Bu öneri [DATAGRAMS]'de tanımlandığı gibi yanıt verilebilir datagram2, yanıt verilebilir datagram3
ve ham datagramları kullanır.
Datagram2 ve Datagram3, Öneri 163'te [/en/proposals/163-datagram2/](/en/proposals/163-datagram2/) tanımlanan yeni yanıt verilebilir datagram
türevleridir.
Datagram2, tekrar saldırısına direnç ve çevrimdışı imza desteği ekler.
Datagram3, eski datagram formatından daha küçüktür ancak kimlik doğrulama içermez.

### BEP 15

Referans olması için, [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) tarafından tanımlanan mesaj akışı şu şekildedir:

```
İstemci                         İzleyici
    Bağlantı İst. ------------->
      <-------------- Bağlantı Yanıtı
    Duyuru İst. ------------->
      <-------------- Duyuru Yanıtı
    Duyuru İst. ------------->
      <-------------- Duyuru Yanıtı
```

Bağlantı aşaması IP adresi sahteciliğini önlemek için gereklidir.
İzleyici, istemcinin sonraki duyurularında kullanacağı bir bağlantı ID'si döner.
Bu bağlantı ID'si, istemcide bir dakikada, izleyicide iki dakikada sona erer.

I2P, mevcut UDP yetenekli istemci kod tabanlarında benimsenmesi kolay olması için
BEP 15 ile aynı mesaj akışını, verimlilik için ve aşağıda tartışılan güvenlik nedenleriyle kullanacaktır:

```
İstemci                         İzleyici
    Bağlantı İst. ------------->       (Yanıt Verilebilir Datagram2)
      <-------------- Bağlantı Yanıtı   (Ham)
    Duyuru İst. ------------->      (Yanıt Verilebilir Datagram3)
      <-------------- Duyuru Yanıtı  (Ham)
    Duyuru İst. ------------->      (Yanıt Verilebilir Datagram3)
      <-------------- Duyuru Yanıtı  (Ham)
             ...
```

Bu, potansiyel olarak
akışlı (TCP) duyurulara karşı büyük bant genişliği tasarrufu sağlar.
Datagram2, bir akış SYN'si ile yaklaşık aynı boyutta olsa da
ham yanıt, akış SYN ACK'den çok daha küçüktür. 
Sonraki isteklere Datagram3 kullanılır ve sonraki yanıtlar hamdır. 

Duyuru istekleri Datagram3, böylece izleyici
bağlantı ID'lerinden duyuru hedefini veya karmaşayı duyurmak zorunda kalmaz.
Bunun yerine, izleyici, bağlantı ID'lerini, gönderici hash'inden,
mevcut zaman damgasından (belirli bir aralığa dayanarak)
ve gizli bir değerden kriptografik olarak oluşturabilir.
Bir duyuru isteği alındığında, izleyici
bağlantı ID'sini doğrular ve ardından
Datagram3 gönderici hash'ini gönderme hedefi olarak kullanır.

### İzleyici/İstemci desteği

Entegre bir uygulama için (örneğin, i2psnark ve ZzzOT Java eklentisi gibi bir süreçte yönlendirici ve istemci),
veya I2CP tabanlı bir uygulama için (örneğin BiglyBT),
akış ve datagram trafiğini ayrı olarak uygulamak ve yönlendirmek kolay olmalıdır.
ZzzOT ve i2psnark'ın bu teklifi uygulayan ilk izleyici ve istemci olması bekleniyor.

Entegre olmayan izleyiciler ve istemciler aşağıda tartışılmıştır.

İzleyiciler
``````````

Bilinen dört I2P izleyici uygulaması vardır:

- zzzot, opentracker.dg2.i2p ve birkaç başkasında çalışan entegre bir Java yönlendirici eklentisi
- tracker2.postman.i2p, muhtemelen bir Java yönlendiricinin ve HTTP Sunucusu tünelinin arkasında çalışıyor
- UDP desteği yorumlanan eski C opentracker, zzz tarafından dönüştürüldü
- r4sas tarafından dönüştürülen yeni C opentracker, opentracker.r4sas.i2p ve muhtemelen
  başkalarında çalışıyor, muhtemelen bir i2pd yönlendirici ve HTTP Sunucusu tünelinin arkasında çalışıyor

Duyuru isteklerini almak için şu anda bir HTTP sunucusu tüneli kullanan
dış bir izleyicide uygulama oldukça zor olabilir.
Datagramları yerel HTTP istek/yanıtlarına dönüştürmek için özel bir tünel geliştirilebilir.
Ya da hem HTTP isteklerini hem de datagramları işleyen ve
datagramları dış sürece iletecek özel bir tünel tasarlanabilir.
Bu tasarım kararı, büyük ölçüde belirli yönlendirici ve izleyici uygulamalarına
bağlı olacak ve bu teklifin kapsamı dışındadır.

İstemciler
`````````
qbittorrent gibi dış SAM tabanlı torrent istemcileri ve diğer libtorrent tabanlı istemciler
i2pd tarafından desteklenmeyen SAM v3.3 [/en/docs/api/samv3/](/en/docs/api/samv3/) gerektirecektir.
Bu ayrıca DHT desteği için gereklidir ve bilinen hiçbir
SAM torrent istemcisi bunu uygulamamıştır.
Bu teklifin herhangi bir SAM tabanlı uygulamasının yakın zamanda beklenmemesi gerekir.

### Bağlantı Ömrü

[BEP 15](http://www.bittorrent.org/beps/bep_0015.html) bağlantı ID'sinin istemcide bir dakika, izleyicide iki dakika içinde sona erdiğini belirtir.
Bu yapılandırılamaz.
Bu olası verimlilik kazanımlarını sınırlar, aksi takdirde 
istemciler bir dakikalık bir pencere içinde tüm duyuruları yapmak için duyuruları toplardı.
i2psnark şu anda duyuruları toplamaz; trafiği patlamalardan kaçınmak için yayar.
Güç kullanıcılarının aynı anda binlerce torrent çalıştırıldığı bildirilmektedir
ve bu kadar çok duyurunun bir dakika içinde patlaması gerçekçi değildir.

Burada, yanıtı genişletip bir bağlantı ömrü alanı eklemeyi öneriyoruz.
Varlığı yoksa, varsayılan bir dakikadır. Aksi takdirde belirtilen
ömür, saniyeler cinsinden, istemci tarafından kullanılacaktır ve izleyici
bağlantı ID'sini istemci ömrünün bir dakikasının ötesine saklayacaktır.

### BEP 15 ile Uyumluluk

Bu tasarım mevcut istemcilerde ve izleyicilerde
gereken değişiklikleri sınırlamak için [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) ile
mümkün olduğunca uyumluluğu korur.

Tek gerektiren değişiklik, yanıt duyuru içindeki eş bilgisi formatıdır.
Verimlilik için yanıt ömrü karekökünün eklenmesi önerilir yukarıda açıklandığı gibi.

### Güvenlik Analizi

Bir UDP duyuru protokolünün önemli bir hedefi, adres sahteciliğini önlemektir.
İstemci gerçek bir leasing setini toplamalı ve gerçek bir kiracı
olmalıdır.
Bu tünellerin hiçbir sıfır atlamalı olması gerekmez ve anında inşa edilebilir,
ama bu yaratıcıyı ortaya çıkarır.
Bu protokol bu hedefi gerçekleştirir.

### Sorunlar

- Bu teklif körlenen hedefleri desteklemez,
  ancak bunu yapmak için genişletilebilir. Aşağıya bakın.

## Spesifikasyon

### Protokoller ve Portlar

Yanıt Verilebilir Datagram2 I2CP protokol 19'u kullanır; 
yanıt Verilebilir Datagram3 I2CP protokol 20'yi kullanır; 
ham datagramlar I2CP protokol 18'i kullanır.
İstekler Datagram2 veya Datagram3 olabilir. Yanıtlar her zaman hamdır.
Daha önce kullanılan yanıt Verilebilir datagram ("Datagram1") formatı I2CP protokol 17'yi kullanarak 
istekler veya yanıtlar için KULLANILMAMALIDIR; eğer yanıt/istek portları üzerinden alınırsa bunlar düşürülmelidir.
Datagram1 protokol 17'nin hala DHT protokolü için kullanıldığını unutmayın.

İstekler, duyuru URL'sinden I2CP "to port" kullanır; aşağıya bakın.
İstek "from port" istemci tarafından seçilir, ama sıfır olmamalı
ve DHT'nin kullandığı portlardan farklı olmalıdır, böylece yanıtlar kolayca sınıflandırılabilir.
Yanlış port üzerinden alınan istekleri izleyiciler reddetmelidir.

Yanıtlar, duyurudan alınan istekteki I2CP "to port"u kullanır.
İstek "from port" istekteki "to port"tur.

### Duyuru URL

Duyuru URL formatı [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) içinde tanımlanmamıştır,
ama açık internette olduğu gibi, UDP duyuru URL'leri "udp://host:port/path" şeklindedir.
Yol dikkate alınmaz ve boş olabilir, ancak tipik olarak açık internette "/announce" dür.
:port bölümü daima bulunmalıdır, ama
:port kısmı eksikse, I2CP portu 6969 olarak varsayılan şekilde düşünülmelidir.
Bu, açık internetteki yaygın bir porttur.
Ayrıca cgi parametreleri &a=b&c=d eklenebilir,
bu parametreler işlenebilir ve duyuru isteğinde sağlanabilir, bkz. [BEP 41](http://www.bittorrent.org/beps/bep_0041.html).
Eğer parametre veya yol yoksa, son /, belirtildiği gibi [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) atlanabilir.

### Datagram Formatları

Tüm değerler ağ bayt düzeninde (big endian) gönderilir.
Paketlerin belirli bir boyutta olduğunu beklemeyin.
Gelecekte eklentiler paketlerin boyutunu artırabilir.

Bağlantı İsteği
```````````````

İstemciden izleyiciye.
16 bayt. Yanıt Verilebilir Datagram2 olmalı. [BEP 15](http://www.bittorrent.org/beps/bep_0015.html)'teki ile aynı. Hiçbir değişiklik yoktur.

```
Offset  Boyut            İsim            Değer
  0       64-bit integer  protocol_id     0x41727101980 // sihirli sabit
  8       32-bit integer  action          0 // bağlantı
  12      32-bit integer  transaction_id
```


Bağlantı Yanıtı
``````````````

İzleyiciden istemciye.
16 veya 18 bayt. Ham olmalı. [BEP 15](http://www.bittorrent.org/beps/bep_0015.html)'teki ile aynı, aşağıda belirtilen farklar hariç.

```
Offset  Boyut            İsim            Değer
  0       32-bit integer  action          0 // bağlantı
  4       32-bit integer  transaction_id
  8       64-bit integer  connection_id
  16      16-bit integer  lifetime        optional  // BEP 15'ten Değişiklik
```

Yanıt, istek "from port" olarak alınan I2CP "to port"una gönderilmelidir.

Ömür alanı isteğe bağlıdır ve saniyeler cinsinden connection_id istemci ömrünü belirtir.
Varsayılan 60'tır ve belirtilirse minimum 60'tır.
Maksimum 65535'tür veya yaklaşık 18 saattir.
İzleyici, istemci ömründen 60 saniye daha fazla connection_id'yi korumalıdır.

Duyuru İsteği
````````````

İstemciden izleyiciye.
En az 98 bayt. Yanıt Verilebilir Datagram3 olmalı. [BEP 15](http://www.bittorrent.org/beps/bep_0015.html)'teki ile aynı, aşağıda belirtilen farklar hariç.

Bağlantı_ID, bağlantı yanıtında alındığı gibidir.

```
Offset  Boyut            İsim            Değer
  0       64-bit integer  connection_id
  8       32-bit integer  action          1     // duyuru
  12      32-bit integer  transaction_id
  16      20-byte string  info_hash
  36      20-byte string  peer_id
  56      64-bit integer  downloaded
  64      64-bit integer  left
  72      64-bit integer  uploaded
  80      32-bit integer  event           0     // 0: yok; 1: tamamlandı; 2: başlatıldı; 3: durduruldu
  84      32-bit integer  IP address      0     // varsayılan
  88      32-bit integer  key
  92      32-bit integer  num_want        -1    // varsayılan
  96      16-bit integer  port
  98      değişken         options     optional  // BEP 41'de belirtildiği gibi
```

[BEP 15](http://www.bittorrent.org/beps/bep_0015.html) değiştirilmiş kullanımları:

- Anahtar yok sayılır
- Port muhtemelen yok sayılır
- Opsiyonel bölümü, varsa, [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) 'de zaten tanımlandığı gibi
The response MUST be sent to the I2CP "to port" that was received as the request "from port".
Yanıt, istek "from port" olarak belirtilen I2CP "to port"una gönderilmelidir.
Duyuru isteğindeki port kullanılmamalıdır.

Duyuru Yanıtı
```````````

İzleyiciden istemciye.
En az 20 bayt. Ham olmalı. [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) 'teki ile aynı, aşağıda belirtilen farklar hariç.

```
Offset  Boyut            İsim            Değer
  0           32-bit integer  action          1 // duyuru
  4           32-bit integer  transaction_id
  8           32-bit integer  interval
  12          32-bit integer  leechers
  16          32-bit integer  seeders
  20   32 * n 32-byte hash    binary hashes     // BEP 15'ten Değişiklik
  ...                                           // BEP 15'ten Değişiklik
```

[BEP15]'ten Değişiklikler:

- 6 baytlık IPv4+port veya 18 baytlık IPv6+port yerine,
  32 baytlık "kompakt yanıtlar" orijinal peer hash'leri döndürüyoruz.
  TCP kompakt yanıtları gibi, bir port dahil etmiyoruz.

Yanıt, istek "from port" olarak alınan I2CP "to port"una gönderilmelidir.
Duyuru isteğindeki port kullanılmamalıdır.

I2P datagramlarının yaklaşık 64 KB'lık çok büyük maksimum boyutu vardır;
ancak, güvenilir teslimat için, 4 KB'den büyük datagramlardan kaçınılmalıdır.
Bant genişliği verimliliği için, izleyiciler maksimum eşleri
yaklaşık 50 ile sınırlamalıdır, ki bu yaklaşık 1600 baytlık bir pakete
işaret eder, çeşitli katmanlarda üst yapıdan önce ve bir iki tünel-mesaj
yük limitine sığacak şekilde parçalanmış olarak gönderilebilir.

BEP 15'te belirtildiği gibi, takiben gelen peer adresleri
(IP/port açısından BEP 15, burada hash'ler) yapılacak bir bilgi olarak takip edenlerden değildir. 
Sonuç değerlendirmesi için 
tamamlayıcı veri aynı boyutta
daha fazla gönderilecektir.

### Eklentiler

Eklenti biti veya bir versiyon alanı dahil edilmemiştir.
İstemci ve izleyiciler, paketlerin belirli bir boyutta olduğuna dair
varsayımda bulunmamalıdır. Bu şekilde, ek alanlar eklenebilir ve
uyumluluk bozulmaz. Eğer bir ek alan gerekli ise, [BEP41]'de tanımlandığı gibi ek formatı önerilir.

Duyuru yanıtına ömrü eklenmiştir.

Eğer körlenmiş hedef desteği gerekiyorsa, ya duyuru isteğinin
sonuna 35 baytlık körlenmiş adres ekliyoruz ya da
yanıtlarda körlenmiş hash'leri talep ediyoruz,
[BEP41] formatını kullanarak (parametreler belirlenmemiştir).
Verilen körlenmiş 35 baytlık peer adresleri
duyuru yanıtının sonuna eklenebilir, tüm sıfırlı 32 baytlık bir hash'in
ardından.

## Uygulama Kılavuzları

Entegre olmayan, I2CP olmayan müşteriler ve izleyiciler açısından
karşılaşılan zorluklar hakkında yukarıdaki tasarım kısmında bir
tartışma vardır.

### Müşteriler

Belirli bir izleyici ana bilgisayar adına göre, bir istemci
UDP'yi HTTP URL'lerine tercih etmelidir 
ve hem UDP hem de HTTP'ye duyuru Duyurmamalıdır.

BEP 15 desteği olan istemciler yalnızca küçük modifikasyonlar
gerektirecektir.

Eğer bir istemci DHT veya diğer datagram protokollerini destekliyorsa, 
istek "from port" olarak belirli bir farkı seçmeli
ve yanıtların bu porta dönmesini ve
DHT mesajları ile karışmamasını sağlamalıdır.
İstemci yalnızca cevapsız ham datagramları
yanıtlar olarak alacak.
İzleyiciler istemciye hiçbir zaman bir
yanıt verilebilir datagram2 göndermeyecek.

Opentrackerlerle ilgili varsayılan bir listeye sahip olan
istemciler, opentrackerların
UDP'yi desteklediği bilindikten sonra
UDP URL'lerini de ekleyerek listeyi güncellemelidir.

İstemciler isteği yeniden gönderimini
uygulayıp uygulamamakta özgürdür.
Yeniden gönderimler,
uygulanıyorsa, en azından ilk zaman aşımı 15 saniye olarak
belirlenmeli ve her yeniden gönderim için
bekleme süresi iki katına çıkarılmalıdır
(üstel geri çekilme).

Hata yanıtı aldıktan sonra istemciler geri adım atmalıdır.

### İzleyiciler

BEP 15 desteği olan izleyiciler yalnızca küçük 
modifikasyonlar gerektirecektir.
Bu öneri, izleyicinin
aynı port üzerinden yanıt verilebilir datagram2 ve
datagram3 alımını desteklemesi gerektiği
yönünden 2014 teklifinden farklıdır.

İzleyici kaynak gereksinimlerini minimize
etmek için, bu protokol, izleyicinin
ileri doğrulama için istemci hash'lerinin bağlantı 
ID'lerine olan eşleşmelerini depolamasını gerektiren 
herhangi bir gereksinimi ortadan
kaldırmak için tasarlanmıştır.
Bu mümkündür çünkü duyuru istek paketi 
yanıt Verilebilir bir 
Datagram3 paketi olduğundan, gönderici 
hash'ini içerir.

Önerilen bir uygulama:

- Geçerli epoch'u bağlantı ömrü çözünürlüğü ile
  geçerli zaman olarak tanımlayın, ``epoch = şimdi / ömür``.
- 8 baytlık bir çıktı üreten, kriptografik bir hash
  fonksiyonu ``H(secret, clienthash, epoch)`` tanımlayın.
- Tüm bağlantılar için kullanılan rastgele sabit
  secret'ı üretin.
- Bağlantı yanıtları için, ``connection_id = H(secret, clienthash, epoch)``'ü
  oluşturun
- Duyuru talepleri için, alınan bağlantı ID'sini
  şu doğrulamalar ile geçerli epoch'da doğrulayın
  ``connection_id == H(secret, clienthash, epoch) || connection_id == H(secret, clienthash, epoch - 1)``

## Göç

Mevcut istemciler UDP duyuru URL'lerini desteklemez ve onları yok sayar.

Mevcut izleyiciler yanıt verilebilir veya ham
datagramların alınmasını desteklemez, düşürülecektir.

Bu öneri tamamen isteğe bağlıdır. Ne müşteriler ne de izleyiciler herhangi
bir zamanda uygulama yapmaya gereklidir.

## Yayılma

İlk uygulamaların ZzzOT ve i2psnark'ta olması bekleniyor.
Bu tester ve bu önerinin doğrulanması için kullanılacaktır.

Diğer uygulamalar, istek üzerine, testlerin ve doğrulamanın tamamlanmasından sonra olacaktır.

## Referanslar

.. [BEP15]
    http://www.bittorrent.org/beps/bep_0015.html

.. [BEP41]
    http://www.bittorrent.org/beps/bep_0041.html

.. [DATAGRAMS]
    {{ spec_url('datagrams') }}

.. [Prop163]
    {{ proposal_url('163') }}

.. [Prop169]
    {{ proposal_url('169') }}

.. [SAMv3]
    {{ site_url('docs/api/samv3') }}

.. [SPEC]
    {{ site_url('docs/applications/bittorrent', True) }}

.. [UDP]
    {{ spec_url('udp-announces') }}
