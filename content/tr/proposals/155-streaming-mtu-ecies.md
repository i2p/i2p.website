---
title: "ECIES Hedefleri için Akış MTU'su"
number: "155"
author: "zzz"
created: "2020-05-06"
lastupdated: "2020-05-30"
status: "Kapalı"
thread: "http://zzz.i2p/topics/2886"
target: "0.9.47"
implementedin: "0.9.47"
toc: true
---

## Not
Ağ dağılımı ve test süreçleri devam ediyor.
Küçük revizyonlar yapılabilir.


## Genel Bakış


### Özet

ECIES, mevcut oturum (ES) mesaj yükünü yaklaşık 90 bayt azaltır.
Bu nedenle, ECIES bağlantıları için MTU'yu yaklaşık 90 bayt artırabiliriz.
Bakınız the [ECIES specification](/docs/specs/ecies/#overhead), [Streaming specification](/docs/specs/streaming/#flags-and-option-data-fields), and [Streaming API documentation](/docs/api/streaming/).

MTU'yu artırmadan, birçok durumda yük kazanımları gerçekten 'kazanılmış' olmaz,
çünkü mesajlar yine de iki tam tünel mesajı kullanacak şekilde doldurulacaktır.

Bu öneri, herhangi bir spesifikasyon değişikliği gerektirmez.
Öneri olarak yalnızca, önerilen değerin ve uygulama detaylarının tartışılması ve fikir birliğinin sağlanması amacıyla buradadır.


### Amaçlar

- Müzakere edilen MTU'yu artırmak
- 1 KB tünel mesajlarının kullanımını maksimize etmek
- Akış protokolünü değiştirmemek


## Tasarım

Mevcut MAX_PACKET_SIZE_INCLUDED seçeneği ve MTU müzakeresini kullanın.
Akış, gönderilen ve alınan MTU'nun minimumunu kullanmaya devam eder.
Varsayılan, hangi anahtarların kullanıldığına bakılmaksızın tüm bağlantılar için 1730 olarak kalır.

Uygulamalar, her iki yönde de tüm SYN paketlerinde MAX_PACKET_SIZE_INCLUDED seçeneğini dahil etmeye teşvik edilir,
ancak bu bir zorunluluk değildir.

Eğer bir hedef yalnızca ECIES ise, daha yüksek değeri kullanın (Alice veya Bob olarak).
Eğer bir hedef çifte anahtar ise, davranış değişebilir:

Eğer çift anahtar istemci router dışında ise (dış bir uygulamada),
uzak uçta hangi anahtarın kullanıldığını "bilmemesi" mümkün olabilir ve Alice SYN'de
daha yüksek bir değer isteyebilir, fakat SYN'deki maksimum veri 1730 olarak kalır.

Eğer çift anahtar istemci router içinde ise,
hangi anahtarın kullanıldığı bilgisi müşteriye bilinebilir veya bilinmeyebilir.
Lease set henüz alınmamış olabilir veya dahili API arabirimleri
bu bilgiyi müşteriye kolayca sağlayamayabilir.
Bilgi mevcutsa, Alice daha yüksek değeri kullanabilir;
aksi takdirde, Alice müzakere edilene kadar standart 1730 değerini kullanmalıdır.

Bob olarak bir çift anahtar istemci, Alice'den alınan hiçbir değer veya 1730 değeri
olmasa bile yanıt olarak daha yüksek bir değer gönderebilir;
ancak, akışta yukarı doğru müzakere için bir düzenleme yoktur,
bu nedenle MTU 1730 olarak kalmalıdır.


the [Streaming API documentation](/docs/api/streaming/)'da belirtildiği gibi, Alice'den Bob'a gönderilen SYN paketlerindeki veri,
Bob'un MTU'sunu aşabilir.
Bu, akış protokolündeki bir zayıflıktır.
Bu nedenle, çift anahtar istemciler gönderilen SYN paketlerindeki veriyi
1730 bayt ile sınırlamalıdır, ancak daha yüksek bir MTU seçeneği göndermelidir.
Bob'dan daha yüksek MTU alındıktan sonra, Alice gönderilen gerçek maksimum
yükü artırabilir.


### Analiz

the [ECIES specification](/docs/specs/ecies/#overhead) 'de açıklandığı üzere, mevcut oturum mesajları için ElGamal yükü
151 bayt, ve Ratchet yükü 69 bayttır.
Bu nedenle, ratchet bağlantıları için MTU'yu (151 - 69) = 82 bayt artırabiliriz,
1730'dan 1812'ye.


## Spesifikasyon

the [Streaming API documentation](/docs/api/streaming/) 'teki MTU Seçimi ve Müzakere bölümüne aşağıdaki değişiklikler ve açıklamalar eklenmiştir.
the [Streaming specification](/docs/specs/streaming/) 'e herhangi bir değişiklik yapılmamıştır.


i2p.streaming.maxMessageSize seçeneğinin varsayılan değeri, hangi anahtarların kullanıldığına bakılmaksızın tüm bağlantılar için 1730 olarak kalır.
Müşteriler, her zamanki gibi, gönderilen ve alınan MTU'nun minimumunu kullanmalıdır.

Dört ilgili MTU sabiti ve değişkeni vardır:

- DEFAULT_MTU: 1730, değişmemiş, tüm bağlantılar için
- i2cp.streaming.maxMessageSize: varsayılan 1730 veya 1812, yapılandırma ile değiştirilebilir
- ALICE_SYN_MAX_DATA: Alice'in bir SYN paketinde dahil edebileceği maksimum veri
- negotiated_mtu: Bob'dan Alice'e SYN ACK'deki ve her iki yönde gönderilen tüm sonraki paketlerde kullanılacak maksimum veri boyutu olarak Alice ve Bob'un MTU'sunun minimumu


Dikkate alınması gereken beş durum vardır:


### 1) Yalnızca Alice ElGamal
Değişiklik yok, tüm paketlerde 1730 MTU.

- ALICE_SYN_MAX_DATA = 1730
- i2cp.streaming.maxMessageSize varsayılan: 1730
- Alice, SYN'de MAX_PACKET_SIZE_INCLUDED gönderebilir, aksi belirtilmediği sürece gerek yoktur


### 2) Yalnızca Alice ECIES
Tüm paketlerde 1812 MTU.

- ALICE_SYN_MAX_DATA = 1812
- i2cp.streaming.maxMessageSize varsayılan: 1812
- Alice SYN'de MAX_PACKET_SIZE_INCLUDED göndermelidir


### 3) Çifte Anahtar Alice ve Bob'un ElGamal olduğunu biliyor
Tüm paketlerde 1730 MTU.

- ALICE_SYN_MAX_DATA = 1730
- i2cp.streaming.maxMessageSize varsayılan: 1812
- Alice, SYN'de MAX_PACKET_SIZE_INCLUDED gönderebilir, aksi belirtilmediği sürece gerek yoktur


### 4) Çifte Anahtar Alice ve Bob'un ECIES olduğunu biliyor
Tüm paketlerde 1812 MTU.

- ALICE_SYN_MAX_DATA = 1812
- i2cp.streaming.maxMessageSize varsayılan: 1812
- Alice SYN'de MAX_PACKET_SIZE_INCLUDED göndermelidir


### 5) Çifte Anahtar Alice ve Bob anahtarı bilinmiyor
1812'yi SYN paketi içinde MAX_PACKET_SIZE_INCLUDED olarak gönderin ancak SYN paket verisini 1730 ile sınırlayın.

- ALICE_SYN_MAX_DATA = 1730
- i2cp.streaming.maxMessageSize varsayılan: 1812
- Alice SYN'de MAX_PACKET_SIZE_INCLUDED göndermelidir


### Tüm Durumlar için

Alice ve Bob, Bob'dan Alice'e SYN ACK'deki ve her iki yönde gönderilen tüm sonraki paketlerde kullanılacak maksimum veri boyutu olarak Alice ve Bob'un MTU'sunun minimumunu hesaplarlar.
            


## Gerekçe

Mevcut değerin neden 1730 olduğunu görmek için the [Java I2P source code](https://github.com/i2p/i2p.i2p/blob/master/apps/streaming/java/src/net/i2p/client/streaming/impl/ConnectionOptions.java#L220) 'a bakın.
ECIES yükünün neden ElGamal'dan 82 bayt daha az olduğunu görmek için the [ECIES specification](/docs/specs/ecies/#overhead) 'e bakın.


## Uygulama Notları

Eğer akış, optimal boyutta mesajlar oluşturuyorsa, ECIES-Ratchet katmanının bu boyutun ötesinde dolgu yapmaması çok önemlidir.

İki tünel mesajına sığacak optimal Garlic Mesaj boyutu,
16 baytlık Garlic Mesaj I2NP başlığı, 4 baytlık Garlic Mesaj Uzunluğu,
8 baytlık ES etiketi ve 16 baytlık MAC dahil olmak üzere 1956 bayttır.

ECIES'deki önerilen dolgu algoritması şu şekildedir:

- Eğer Garlic Mesajının toplam uzunluğu 1954-1956 bayt olacaksa,
  dolgu bloğu eklemeyin (yer yok)
- Eğer Garlic Mesajının toplam uzunluğu 1938-1953 bayt olacaksa,
  tam olarak 1956 bayta ulaşmak için dolgu bloğu ekleyin.
- Aksi takdirde, genellikle 0-15 bayt arasında rastgele bir miktarla doldurun.

Benzer stratejiler, pratikte nadir olacak olan optimal bir tünel mesajı boyutu (964) ve üç tünel mesajı boyutu (2952) için kullanılabilir.


## Sorunlar

1812 değeri ön araştırmadir. Doğrulanması ve olası ayarlamalar gerekebilir.


## Geçiş

Geriye dönük uyumluluk sorunları yok.
Bu, mevcut bir seçenek ve MTU müzakeresi zaten spesifikasyonun bir parçası.

Daha eski ECIES hedefleri 1730'u destekleyecektir.
Daha yüksek bir değer alan herhangi bir müşteri 1730 ile yanıt verecek ve uzak uç tarafından
her zamanki gibi aşağı doğru müzakere edilecektir.


