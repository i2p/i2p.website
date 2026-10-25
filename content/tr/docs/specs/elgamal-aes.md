---
title: "ElGamal/AES + SessionTag Şifrelemesi"
description: "ElGamal, AES, SHA-256 ve tek kullanımlık oturum etiketlerini birleştiren eski uçtan uca şifreleme"
slug: "elgamal-aes"
aliases:
  - "/tr/how_elgamalaes"
  - "/tr/how_elgamalaes/"
lastUpdated: "2020-04"
accurateFor: "0.9.46"
---

## Genel Bakış

ElGamal/AES+SessionTags uçtan uca şifreleme için kullanılır.

Güvenilmez, sırasız, mesaj tabanlı bir sistem olan I2P, garlic mesajlarına veri gizliliği ve bütünlüğü sağlamak için asimetrik ve simetrik şifreleme algoritmalarının basit bir kombinasyonunu kullanır. Bütün olarak, bu kombinasyon ElGamal/AES+SessionTags olarak adlandırılır, ancak bu 2048bit ElGamal, AES256, SHA256 ve 32 byte nonce kullanımını tanımlamak için aşırı ayrıntılı bir yoldur.

Bir router başka bir router'a ilk kez garlic mesajı şifrelemek istediğinde, AES256 oturum anahtarı için anahtar materyalini ElGamal ile şifreler ve bu şifrelenmiş ElGamal bloğundan sonra AES256/CBC şifrelenmiş yükü ekler. Şifrelenmiş yüke ek olarak, AES şifrelenmiş bölüm yük uzunluğunu, şifrelenmemiş yükün SHA256 hash'ini ve bir dizi "session tag" - rastgele 32 baytlık nonce'ları içerir. Gönderici bir sonraki sefer başka bir router'a garlic mesajı şifrelemek istediğinde, ElGamal ile yeni bir oturum anahtarı şifrelemek yerine, daha önce teslim edilmiş session tag'lerden birini seçer ve o session tag ile kullanılan oturum anahtarını kullanarak yükü eskisi gibi AES şifreler, session tag'in kendisini başa ekleyerek. Bir router garlic şifrelenmiş mesaj aldığında, mevcut bir session tag ile eşleşip eşleşmediğini görmek için ilk 32 baytı kontrol eder - eşleşirse, mesajı basitçe AES ile deşifreler, ancak eşleşmezse, ilk bloğu ElGamal ile deşifreler.

Her oturum etiketi yalnızca bir kez kullanılabilir, böylece dahili saldırganların farklı mesajları gereksiz yere aynı router'lar arasında geçen mesajlar olarak ilişkilendirmesi önlenir. ElGamal/AES+SessionTag şifreli mesajın göndereni, etiketleri ne zaman ve kaç tane teslim edeceğini seçer ve alıcıyı bir dizi mesajı karşılamak için yeterli etiketle önceden stoklar. Garlic mesajları, küçük bir ek mesajı clove (karanfil) olarak paketleyerek ("delivery status message" - teslimat durumu mesajı) başarılı etiket teslimatını tespit edebilir - garlic mesaj hedeflenen alıcıya ulaştığında ve başarılı bir şekilde şifreçözüldüğünde, bu küçük teslimat durumu mesajı açığa çıkan clove'lardan biridir ve alıcıya bu clove'u (tabii ki bir inbound tunnel aracılığıyla) orijinal gönderene geri göndermesi için talimatlar içerir. Orijinal gönderen bu teslimat durumu mesajını aldığında, garlic mesajda paketlenen oturum etiketlerinin başarılı bir şekilde teslim edildiğini bilir.

Session tag'lerin kendilerinin kısa bir yaşam süresi vardır, bu sürenin ardından kullanılmazlarsa atılırlar. Ayrıca, her anahtar için saklanan miktar sınırlıdır ve anahtarların sayısı da sınırlıdır - çok fazla anahtar gelirse, yeni veya eski mesajlar düşürülebilir. Gönderen, session tag'leri kullanan mesajların iletilip iletilmediğini takip eder ve yeterli iletişim yoksa, daha önce düzgün şekilde iletildiği varsayılan mesajları düşürebilir ve tam maliyetli ElGamal şifrelemeye geri dönebilir. Bir session, tüm tag'leri tükenene veya süresi dolana kadar var olmaya devam edecektir.

Oturumlar tek yönlüdür. Etiketler Alice'ten Bob'a teslim edilir ve Alice daha sonra bu etiketleri, Bob'a gönderdiği sonraki mesajlarda teker teker kullanır.

Oturumlar Destination'lar arasında, router'lar arasında veya bir router ile Destination arasında kurulabilir. Her router ve Destination, Session Key'leri ve Session Tag'lerini takip etmek için kendi Session Key Manager'ını tutar. Ayrı Session Key Manager'lar, düşmanların birden fazla Destination'ı birbirleriyle veya bir router ile ilişkilendirmesini engeller.

## Mesaj Alımı

Alınan her mesaj iki olası durumdan birine sahiptir:

1. Mevcut bir oturumun parçasıdır ve bir Session Tag ile AES şifrelenmiş blok içerir
2. Yeni bir oturum içindir ve hem ElGamal hem de AES şifrelenmiş blokları içerir

Bir router bir mesaj aldığında, önce bunun mevcut bir oturumdan geldiğini varsayar ve Session Tag'i aramaya çalışır, ardından takip eden veriyi AES kullanarak şifrelemesini çözmeye çalışır. Bu başarısız olursa, bunun yeni bir oturum için olduğunu varsayar ve ElGamal kullanarak şifrelemesini çözmeye çalışır.

## New Session Message Specification {#new}

Yeni Oturum ElGamal Mesajı iki bölüm içerir: şifreli bir ElGamal bloğu ve şifreli bir AES bloğu.

Şifrelenmiş mesaj şunları içerir:

```
   +----+----+----+----+----+----+----+----+
   |                                       |
   +                                       +
   |       ElGamal Encrypted Block         |
   ~                                       ~
   |                                       |
   +         +----+----+----+----+----+----+
   |         |                             |
   +----+----+                             +
   |                                       |
   +                                       +
   |         AES Encrypted Block           |
   ~                                       ~
   |                                       |
   +         +----+----+----+----+----+----+
   |         +
   +----+----+
```
### ElGamal Blok

Şifrelenmiş ElGamal Bloğu her zaman 514 bayt uzunluğundadır.

Şifrelenmemiş ElGamal verisi 222 bayt uzunluğundadır ve şunları içerir:

```
   +----+----+----+----+----+----+----+----+
   |                                       |
   +                                       +
   |           Session Key                 |
   +                                       +
   |                                       |
   +                                       +
   |                                       |
   +----+----+----+----+----+----+----+----+
   |                                       |
   +                                       +
   |              Pre-IV                   |
   +                                       +
   |                                       |
   +                                       +
   |                                       |
   +----+----+----+----+----+----+----+----+
   +                                       +
   |                                       |
   +                                       +
   |       158 bytes random padding        |
   ~                                       ~
   |                                       |
   +                             +----+----+
   |                             |
   +----+----+----+----+----+----+
```
32-byte [Session Key](/docs/specs/common-structures#type_SessionKey) oturum için tanımlayıcıdır. 32-byte Pre-IV, takip eden AES bloğu için IV oluşturmak amacıyla kullanılacaktır; IV, Pre-IV'nin SHA-256 Hash'inin ilk 16 byte'ıdır.

222 baytlık yük [ElGamal kullanılarak](/docs/specs/cryptography#elgamal) şifrelenir ve şifrelenmiş blok 514 bayt uzunluğundadır.

### AES Bloğu {#aes}

AES bloğundaki şifrelenmemiş veri şunları içerir:

```
   +----+----+----+----+----+----+----+----+
   |tag count|                             |
   +----+----+                             +
   |                                       |
   +                                       +
   |          Session Tags                 |
   ~                                       ~
   |                                       |
   +                                       +
   |                                       |
   +         +----+----+----+----+----+----+
   |         |    payload size   |         |
   +----+----+----+----+----+----+         +
   |                                       |
   +                                       +
   |          Payload Hash                 |
   +                                       +
   |                                       |
   +                             +----+----+
   |                             |flag|    |
   +----+----+----+----+----+----+----+    +
   |                                       |
   +                                       +
   |          New Session Key (opt.)       |
   +                                       +
   |                                       |
   +                                  +----+
   |                                  |    |
   +----+----+----+----+----+----+----+    +
   |                                       |
   +                                       +
   |           Payload                     |
   ~                                       ~
   |                                       |
   +                        +----//---+----+
   |                        |              |
   +----+----+----//---+----+              +
   |          Padding to 16 bytes          |
   +----+----+----+----+----+----+----+----+
```
#### Tanım

```
tag count:
    2-byte Integer, 0-200

Session Tags:
    That many 32-byte SessionTags

payload size:
    4-byte Integer

Payload Hash:
    The 32-byte SHA256 Hash of the payload

flag:
    A one-byte value. Normally == 0. If == 0x01, a Session Key follows

New Session Key:
    A 32-byte SessionKey,
    to replace the old key, and is only present if preceding flag is 0x01

Payload:
    the data

Padding:
    Random data to a multiple of 16 bytes for the total length.
    May contain more than the minimum required padding.
```
Minimum uzunluk: 48 bayt

Veriler daha sonra ElGamal bölümünden gelen oturum anahtarı ve IV (pre-IV'den hesaplanan) kullanılarak [AES Şifrelenir](/docs/specs/cryptography). Şifrelenmiş AES Blok uzunluğu değişkendir ancak her zaman 16 baytın katıdır.

#### Notlar

- Gerçek maksimum payload uzunluğu ve maksimum blok uzunluğu 64 KB'den azdır; [I2NP Genel Bakış](/docs/protocol/i2np) bölümüne bakın.
- New Session Key şu anda kullanılmıyor ve hiçbir zaman mevcut değil.

## Mevcut Oturum Mesajı Spesifikasyonu {#existing}

Başarıyla teslim edilen session tag'ler, kullanılana veya atılana kadar kısa bir süre (şu anda 15 dakika) boyunca hatırlanır. Bir tag, yalnızca AES şifrelenmiş blok içeren ve önünde ElGamal blok bulunmayan bir Existing Session Message içinde paketlenerek kullanılır.

Mevcut oturum mesajı şu şekildedir:

```
   +----+----+----+----+----+----+----+----+
   |                                       |
   +                                       +
   |            Session Tag                |
   +                                       +
   |                                       |
   +                                       +
   |                                       |
   +----+----+----+----+----+----+----+----+
   |                                       |
   +                                       +
   |         AES Encrypted Block           |
   ~                                       ~
   |                                       |
   +                                       +
   |                                       |
   +----+----+----+----+----+----+----+----+
```
#### Tanım

```
Session Tag:
    A 32-byte SessionTag
    previously delivered in an AES block

AES Encrypted Block:
    As specified above.
```
Session etiketi aynı zamanda pre-IV olarak da görev yapar. IV, sessionTag'in SHA-256 Hash'inin ilk 16 byte'ıdır.

Mevcut bir oturumdan gelen bir mesajı çözmek için, router Session Tag'i arayarak ilişkili Session Key'i bulur. Session Tag bulunursa, AES bloğu ilişkili Session Key kullanılarak çözülür. Eğer tag bulunamazsa, mesajın [Yeni Oturum Mesajı](#new) olduğu varsayılır.

## Oturum Etiketi Yapılandırma Seçenekleri {#config}

0.9.2 sürümünden itibaren, istemci varsayılan Session Tag sayısını ve mevcut oturum için düşük tag eşiğini yapılandırabilir. Kısa streaming bağlantıları veya datagramlar için, bu seçenekler bant genişliğini önemli ölçüde azaltmak için kullanılabilir. Ayrıntılar için [I2CP seçenekleri spesifikasyonuna](/docs/protocol/i2cp#options) bakın. Oturum ayarları ayrıca mesaj bazında geçersiz kılınabilir. Ayrıntılar için [I2CP Send Message Expires spesifikasyonuna](/docs/specs/i2cp#msg_SendMessageExpires) bakın.

## Gelecek Çalışmalar {#future}

**Not:** ElGamal/AES+SessionTags, ECIES-X25519-AEAD-Ratchet (Öneri 144) ile değiştiriliyor. Aşağıda referans gösterilen sorunlar ve fikirler yeni protokolün tasarımına dahil edilmiştir. Aşağıdaki maddeler ElGamal/AES+SessionTags'te ele alınmayacaktır.

Session Key Manager'ın algoritmalarını ayarlayabileceğiniz birçok alan vardır; bazıları streaming kütüphanesinin davranışıyla etkileşime girebilir veya genel performans üzerinde önemli etkisi olabilir.

- Teslim edilen etiket sayısı, tunnel mesaj katmanında 1KB'ye nihai dolguyu göz önünde bulundurarak mesaj boyutuna bağlı olabilir.

- İstemciler, gerekli etiket sayısı hakkında tavsiye niteliğinde olmak üzere router'a oturum yaşam süresine ilişkin bir tahmin gönderebilir.

- Çok az etiket teslim edilmesi, router'ın pahalı ElGamal şifrelemesine geri dönmesine neden olur.

- Router, Session Tag'lerin teslim edildiğini varsayabilir veya bunları kullanmadan önce onay bekleyebilir;
  her strateji için değiş tokuşlar vardır.

- Çok kısa mesajlar için, bir oturum kurmak yerine, ElGamal bloğundaki pre-IV ve padding alanlarının neredeyse tamamı olan 222 bayt tüm mesaj için kullanılabilir.

- Doldurma stratejisini değerlendir; şu anda minimum 128 bayt'a kadar dolduruyoruz.
  Küçük mesajları doldurmak yerine birkaç etiket eklemek daha iyi olurdu.

- Session Tag sisteminin çift yönlü olması durumunda işler daha verimli olabilir,
  böylece 'ileri' yolda teslim edilen tag'ler 'geri' yolda kullanılabilir,
  böylece ilk yanıtta ElGamal'dan kaçınılabilir.
  Router şu anda kendisine tunnel test mesajları gönderirken
  bunun gibi bazı hileler yapıyor.

- Session Tags'den 
  [senkronize bir PRNG](/docs/overview/performance#future#prng)'ye geçiş.

- Bu fikirlerin birkaçı yeni bir I2NP mesaj türü gerektirebilir veya
  [Teslimat Talimatları](/docs/specs/tunnel-message#struct_TunnelMessageDeliveryInstructions)'nda
  bir bayrak ayarlayabilir ya da Session Key alanının ilk birkaç baytında
  sihirli bir sayı belirleyip rastgele Session Key'in sihirli sayıyla eşleşme riskini kabul edebilir.
