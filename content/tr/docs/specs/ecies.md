---
title: "ECIES-X25519-AEAD-Ratchet"
description: "I2P uçtan uca şifreleme için Eliptik Eğri Entegre Şifreleme Şeması"
slug: "ecies"
aliases:
  - "/tr/docs/specs/ecies-x25519-aead-ratchet"
  - "/tr/docs/specs/ecies-x25519-aead-ratchet/"
category: "Protokoller"
lastUpdated: "2025-06"
accurateFor: "0.9.67"
---

## Not

Ağ dağıtımı tamamlandı. Küçük revizyonlara tabidir. Arka plan tartışması ve ek bilgiler dahil olmak üzere orijinal teklif için [Prop144](/proposals/144-ecies-x25519/) bölümüne bakın.

Aşağıdaki özellikler 0.9.66 sürümü itibarıyla henüz uygulanmamıştır:

- MessageNumbers, Options ve Termination blokları
- Protokol katmanı yanıtları
- Sıfır statik anahtar
- Multicast

Bu protokolün MLKEM PQ Hybrid sürümü için, [ECIES-HYBRID](/docs/specs/ecies-hybrid/) bölümüne bakın.

## Genel Bakış

Bu, ElGamal/AES+SessionTags [ElG-AES](/docs/specs/elgamal-aes/) protokolünün yerini alacak yeni uçtan uca şifreleme protokolüdür.

Aşağıdaki şekilde önceki çalışmalara dayanmaktadır:

- Ortak yapılar spesifikasyonu [Common](/docs/specs/common-structures/)
- LS2 dahil [I2NP](/docs/specs/i2np/) spesifikasyonu
- ElGamal/AES+Session Tags [Elg-AES](/docs/specs/elgamal-aes/)
- <http://zzz.i2p/topics/1768> yeni asimetrik kripto genel bakış
- Düşük seviye kripto genel bakış [CRYPTO-ELG](/docs/specs/cryptography/#elgamal)
- ECIES <http://zzz.i2p/topics/2418>
- [NTCP2](/docs/specs/ntcp2/) [Prop111](/proposals/111-ntcp2/)
- 123 Yeni netDb Girdileri
- 142 Yeni Kripto Şablonu
- [Noise](https://noiseprotocol.org/noise.html) protokolü
- [Signal](https://signal.org/docs/specifications/doubleratchet/) double ratchet algoritması

Uçtan uca, hedeften hedefe iletişim için yeni şifrelemeyi destekler.

Tasarım, Signal'in çift ratchet'ini içeren bir Noise handshake ve veri aşaması kullanır.

Bu spesifikasyondaki Signal ve Noise'a yapılan tüm referanslar yalnızca arka plan bilgisi içindir. Bu spesifikasyonu anlamak veya uygulamak için Signal ve Noise protokollerinin bilinmesi gerekmez.

Bu spesifikasyon 0.9.46 sürümünden itibaren desteklenmektedir.

## Spesifikasyon

Tasarım, Signal'in çift mandal (double ratchet) sistemini içeren bir Noise el sıkışması ve veri aşaması kullanır.

### Kriptografik Tasarım Özeti

Protokolün yeniden tasarlanması gereken beş bölümü vardır:

- 1\) Yeni ve Mevcut Session container formatları yeni formatlarla
  değiştirilir.
- 2\) ElGamal (256 bayt public key, 128 bayt private key) 
  ECIES-X25519 (32 bayt public ve private key) ile değiştirilir
- 3\) AES, AEAD_ChaCha20_Poly1305 (aşağıda ChaChaPoly olarak
  kısaltılmıştır) ile değiştirilir
- 4\) SessionTag'ler, temelde kriptografik, senkronize bir PRNG olan
  ratchet'larla değiştirilecektir.
- 5\) ElGamal/AES+SessionTags spesifikasyonunda tanımlanan AES payload,
  NTCP2'dekine benzer bir blok formatıyla değiştirilir.

Beş değişikliğin her birinin aşağıda kendi bölümü bulunmaktadır.

### Kripto Türü

Crypto türü (LS2'de kullanılan) 4'tür. Bu, little-endian 32-byte X25519 public key ve burada belirtilen uçtan-uca protokolü gösterir.

Crypto türü 0 ElGamal'dır. Crypto türleri 1-3 ECIES-ECDH-AES-SessionTag için ayrılmıştır, bkz. öneri 145 [Prop145](/proposals/145-ecies-ecdh-aes/).

### Noise Protocol Framework

Bu protokol, Noise Protocol Framework [NOISE](https://noiseprotocol.org/noise.html) (Revizyon 34, 2018-07-11) tabanlı gereksinimleri sağlar. Noise, [SSU](/docs/transport/ssu/) protokolünün temelini oluşturan Station-To-Station protokolü [STS](https://en.wikipedia.org/wiki/Station-to-Station_protocol) ile benzer özelliklere sahiptir. Noise terminolojisinde Alice başlatıcı, Bob ise yanıtlayıcıdır.

Bu spesifikasyon Noise_IK_25519_ChaChaPoly_SHA256 Noise protokolüne dayanmaktadır. (İlk anahtar türetme fonksiyonu için gerçek tanımlayıcı, I2P uzantılarını belirtmek için "Noise_IKelg2_25519_ChaChaPoly_SHA256"dir - aşağıdaki KDF 1 bölümüne bakın) Bu Noise protokolü aşağıdaki ilkelleri kullanır:

- Interactive Handshake Pattern: IK Alice, statik anahtarını hemen Bob'a iletir (I) Alice zaten Bob'un statik anahtarını bilir (K)
- One-Way Handshake Pattern: N Alice, statik anahtarını Bob'a iletmez (N)
- DH Function: X25519 [RFC-7748](https://tools.ietf.org/html/rfc7748)'de belirtildiği gibi 32 bayt anahtar uzunluğuna sahip X25519 DH.
- Cipher Function: ChaChaPoly [RFC-7539](https://tools.ietf.org/html/rfc7539) bölüm 2.8'de belirtildiği gibi AEAD_CHACHA20_POLY1305. İlk 4 baytı sıfıra ayarlanmış 12 baytlık nonce. [NTCP2](/docs/specs/ntcp2/)'dekiyle aynı.
- Hash Function: SHA256 Standart 32 bayt hash, I2P'de zaten yaygın olarak kullanılmakta.

#### Framework'e Eklemeler

Bu belirtim, Noise_IK_25519_ChaChaPoly_SHA256'ya aşağıdaki geliştirmeleri tanımlar. Bunlar genellikle [NOISE](https://noiseprotocol.org/noise.html) bölüm 13'teki yönergeleri takip eder.

1)  Açık metin geçici anahtarlar şununla kodlanır

    [Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf).
2) Yanıt, düz metin etiketi ile öneklenir. 3) Payload formatı 1, 2 numaralı mesajlar ve veri aşaması için tanımlanır.

    Of course, this is not defined in Noise.

Tüm mesajlar bir [I2NP](/docs/specs/i2np/) Garlic Message başlığı içerir. Veri aşaması, Noise veri aşamasına benzer ancak onunla uyumlu olmayan şifreleme kullanır.

### Handshake Kalıpları

Handshake'ler [Noise](https://noiseprotocol.org/noise.html) handshake kalıplarını kullanır.

Aşağıdaki harf eşleme kullanılır:

- e = tek kullanımlık geçici anahtar
- s = statik anahtar
- p = mesaj yükü

Tek kullanımlık ve Unbound oturumlar Noise N desenine benzer.

```
<- s
...
e es p ->
```
Bağlı oturumlar Noise IK desenine benzer.

```
<- s
...
e es s ss p ->
<- tag e ee se
<- p
p ->
```
#### Güvenlik Özellikleri

Noise terminolojisini kullanarak, kurulum ve veri dizisi şu şekildedir: (Payload Güvenlik Özellikleri [Noise](https://noiseprotocol.org/noise.html)'dan )

```
IK(s, rs):           Authentication   Confidentiality
  <- s
  ...
  -> e, es, s, ss           1                2
  <- e, ee, se              2                4
  ->                        2                5
  <-                        2                5
```
#### XK'den Farkları

IK el sıkışmaları, [NTCP2](/docs/specs/ntcp2/) ve [SSU2](/docs/specs/ssu2/)'de kullanılan XK el sıkışmalarından birkaç farklılığa sahiptir.

- XK için üç yerine toplam dört DH işlemi
- İlk mesajda gönderen kimlik doğrulaması: Yük, gönderenin genel anahtarının sahibine ait olarak doğrulanır, ancak anahtar ele geçirilmiş olabilir (Kimlik Doğrulama 1) XK, Alice'in doğrulanması için başka bir gidiş-dönüş gerektirir.
- İkinci mesajdan sonra tam ileri gizlilik (Gizlilik 5). Bob, ikinci mesajdan hemen sonra tam ileri gizlilikle bir yük gönderebilir. XK, tam ileri gizlilik için başka bir gidiş-dönüş gerektirir.

Özetle, IK, Bob'dan Alice'e yanıt yükünün tam ileri gizlilik ile 1-RTT teslimatına izin verir, ancak istek yükü ileri gizlilik sağlamaz.

### Oturumlar

ElGamal/AES+SessionTag protokolü tek yönlüdür. Bu katmanda, alıcı bir mesajın nereden geldiğini bilmez. Giden ve gelen oturumlar ilişkilendirilmez. Onaylamalar, clove içindeki bir DeliveryStatusMessage (GarlicMessage içine sarılmış) kullanılarak bant dışında yapılır.

Bu spesifikasyon için, çift yönlü protokol oluşturmak amacıyla iki mekanizma tanımlıyoruz - "eşleştirme" ve "bağlama". Bu mekanizmalar artan verimlilik ve güvenlik sağlar.

#### Oturum Bağlamı

ElGamal/AES+SessionTags'te olduğu gibi, tüm gelen ve giden oturumlar belirli bir bağlamda olmalıdır; ya router'ın bağlamında ya da belirli bir yerel hedefin bağlamında. Java I2P'de bu bağlam Session Key Manager olarak adlandırılır.

Oturumlar bağlamlar arasında paylaşılmamalıdır, çünkü bu çeşitli yerel destinasyonlar arasında veya yerel bir destinasyon ile router arasında korelasyona olanak tanır.

Belirli bir hedef hem ElGamal/AES+SessionTags'i hem de bu spesifikasyonu desteklediğinde, her iki oturum türü de bir bağlamı paylaşabilir. Aşağıdaki 1c) bölümüne bakınız.

#### Gelen ve Giden Oturumları Eşleştirme

Başlatıcıda (Alice) bir giden oturum oluşturulduğunda, hiçbir yanıt beklenmediği durumlar dışında (örneğin ham datagramlar), yeni bir gelen oturum oluşturulur ve giden oturumla eşleştirilir.

Yeni bir gelen oturum, yanıt istenmediği durumlar haricinde (örn. ham datagramlar) her zaman yeni bir giden oturum ile eşleştirilir.

Eğer bir yanıt talep ediliyorsa ve uzak uç hedefine veya router'a bağlıysa, bu yeni giden oturum o hedefe veya router'a bağlanır ve o hedefe veya router'a giden önceki giden oturumu değiştirir.

Gelen ve giden oturumları eşleştirmek, DH anahtarlarını ratchet etme yeteneğine sahip çift yönlü bir protokol sağlar.

#### Oturumları ve Hedefleri Bağlama

Belirli bir hedefe veya router'a yalnızca bir giden oturum vardır. Belirli bir hedeften veya router'dan birkaç mevcut gelen oturum olabilir. Genellikle, yeni bir gelen oturum oluşturulduğunda ve o oturum üzerinde trafik alındığında (bu bir ACK işlevi görür), diğerleri bir dakika kadar içinde nispeten hızlı bir şekilde sona erecek şekilde işaretlenir. Önceki gönderilen mesajlar (PN) değeri kontrol edilir ve önceki gelen oturumda alınmamış mesaj yoksa (pencere boyutu içinde), önceki oturum hemen silinebilir.

Başlatıcıda (Alice) bir giden oturum oluşturulduğunda, uzak uç Destination'a (Bob) bağlanır ve eşleştirilmiş herhangi bir gelen oturum da uzak uç Destination'a bağlanır. Oturumlar ratchet işlemi yaparken, uzak uç Destination'a bağlı olmaya devam ederler.

Alıcıda (Bob) bir gelen oturum oluşturulduğunda, Alice'in seçeneğine bağlı olarak uzak uç Destination'a (Alice) bağlanabilir. Alice, Yeni Oturum mesajında bağlama bilgilerini (statik anahtarını) dahil ederse, oturum o destination'a bağlanacak ve aynı Destination'a bağlı bir giden oturum oluşturulacaktır. Oturumlar ratchet işlemi yaparken, uzak uç Destination'a bağlı olmaya devam ederler.

#### Bağlama ve Eşleştirmenin Faydaları

Yaygın, streaming durumu için Alice ve Bob'un protokolü şu şekilde kullanmasını bekliyoruz:

- Alice, yeni giden oturumunu yeni bir gelen oturum ile eşleştirir, her ikisi de uzak uç hedefine (Bob) bağlıdır.
- Alice, Bob'a gönderilen New Session mesajına bağlama bilgilerini ve imzayı, ayrıca bir yanıt isteğini dahil eder.
- Bob, yeni gelen oturumunu yeni bir giden oturum ile eşleştirir, her ikisi de uzak uç hedefine (Alice) bağlıdır.
- Bob, eşleştirilmiş oturumda Alice'e yeni bir DH anahtarına ratchet ile birlikte bir yanıt (ack) gönderir.
- Alice, Bob'un yeni anahtarı ile yeni bir giden oturuma ratchet yapar, mevcut gelen oturum ile eşleştirilmiş olarak.

Bir gelen oturumu uzak uç Destination'a bağlayarak ve gelen oturumu aynı Destination'a bağlı bir giden oturumla eşleştirerek, iki önemli fayda elde ederiz:

1)  Bob'tan Alice'e gelen ilk yanıt ephemeral-ephemeral DH kullanır

2\) Alice, Bob'un yanıtını aldıktan ve ratchet işlemini gerçekleştirdikten sonra, Alice'tan Bob'a gönderilen tüm sonraki mesajlar ephemeral-ephemeral DH kullanır.

#### Mesaj ACK'ları

ElGamal/AES+SessionTags'da, bir LeaseSet garlic clove olarak paketlendiğinde veya tag'ler teslim edildiğinde, gönderen router bir ACK talep eder. Bu, bir DeliveryStatus Mesajı içeren ayrı bir garlic clove'dur. Ek güvenlik için, DeliveryStatus Mesajı bir Garlic Mesajına sarılır. Bu mekanizma, protokol açısından bant dışıdır.

Yeni protokolde, gelen ve giden oturumlar eşleştirildiği için, ACK'ları bant içinde tutabiliriz. Ayrı bir clove gerekli değildir.

Açık bir ACK, basitçe I2NP bloğu olmayan bir Mevcut Oturum mesajıdır. Ancak çoğu durumda, ters trafik olduğu için açık bir ACK'dan kaçınılabilir. Uygulamaların, streaming veya uygulama katmanına yanıt verme zamanı tanımak için açık bir ACK göndermeden önce kısa bir süre (belki de yüz ms) beklemesi arzu edilebilir.

Uygulamalar ayrıca ACK gönderimini I2NP bloğu işlenene kadar ertelemek zorunda kalacak, çünkü Garlic Message bir lease set içeren Database Store Message içerebilir. ACK'yi yönlendirmek için güncel bir lease set gerekli olacak ve bağlayıcı statik anahtarı doğrulamak için uzak uç hedef (lease set içinde bulunan) gerekli olacak.

#### Oturum Zaman Aşımları

Giden oturumlar her zaman gelen oturumlardan önce sona ermelidir. Giden bir oturum sona erdiğinde ve yeni bir tane oluşturulduğunda, yeni bir eşleştirilmiş gelen oturum da oluşturulacaktır. Eğer eski bir gelen oturum varsa, bunun sona ermesine izin verilecektir.

### Multicast

TBD

### Tanımlar

Kullanılan kriptografik yapı taşlarına karşılık gelen aşağıdaki fonksiyonları tanımlıyoruz.

ZEROLEN

sıfır uzunluklu bayt dizisi

CSRNG(n)

kriptografik olarak güvenli rastgele sayı üreticisinden n-bayt çıktı

    generator.

H(p, d)

Bir kişiselleştirme dizesi p ve veri alan SHA-256 hash fonksiyonu

    d, and produces an output of length 32 bytes. As defined in
    [NOISE](https://noiseprotocol.org/noise.html). || below means append.

    Use SHA-256 as follows:

        H(p, d) := SHA-256(p || d)

MixHash(d)

Önceki hash h ve yeni veri d'yi alan SHA-256 hash fonksiyonu,

    and produces an output of length 32 bytes. || below means append.

    Use SHA-256 as follows:

        MixHash(d) := h = SHA-256(h || d)

STREAM

ChaCha20/Poly1305 AEAD, belirtildiği şekilde

    [RFC-7539](https://tools.ietf.org/html/rfc7539). S_KEY_LEN = 32 and S_IV_LEN =
    12.

    ENCRYPT(k, n, plaintext, ad)

    :   Encrypts plaintext using the cipher key k, and nonce n which
        MUST be unique for the key k. Associated data ad is optional.
        Returns a ciphertext that is the size of the plaintext + 16
        bytes for the HMAC.

        The entire ciphertext must be indistinguishable from random if
        the key is secret.

    DECRYPT(k, n, ciphertext, ad)

    :   Decrypts ciphertext using the cipher key k, and nonce n.
        Associated data ad is optional. Returns the plaintext.

DH

X25519 genel anahtar anlaşma sistemi. 32 baytlık özel anahtarlar, genel

    keys of 32 bytes, produces outputs of 32 bytes. It has the following
    functions:

    GENERATE_PRIVATE()

    :   Generates a new private key.

    DERIVE_PUBLIC(privkey)

    :   Returns the public key corresponding to the given private key.

    GENERATE_PRIVATE_ELG2()

    :   Generates a new private key that maps to a public key suitable
        for Elligator2 encoding. Note that half of the
        randomly-generated private keys will not be suitable and must be
        discarded.

    ENCODE_ELG2(pubkey)

    :   Returns the Elligator2-encoded public key corresponding to the
        given public key (inverse mapping). Encoded keys are little
        endian. Encoded key must be 256 bits indistinguishable from
        random data. See Elligator2 section below for specification.

    DECODE_ELG2(pubkey)

    :   Returns the public key corresponding to the given
        Elligator2-encoded public key. See Elligator2 section below for
        specification.

    DH(privkey, pubkey)

    :   Generates a shared secret from the given private and public
        keys.

HKDF(salt, ikm, info, n)

Bazı girdi anahtarını alan kriptografik anahtar türetme fonksiyonu

    material ikm (which should have good entropy but is not required to
    be a uniformly random string), a salt of length 32 bytes, and a
    context-specific 'info' value, and produces an output of n bytes
    suitable for use as key material.

    Use HKDF as specified in [RFC-5869](https://tools.ietf.org/html/rfc5869), using
    the HMAC hash function SHA-256 as specified in
    [RFC-2104](https://tools.ietf.org/html/rfc2104). This means that SALT_LEN is 32
    bytes max.

MixKey(d)

Önceki chainKey ve yeni veri d ile HKDF() kullanın ve yeni

    chainKey and k. As defined in [NOISE](https://noiseprotocol.org/noise.html).

    Use HKDF as follows:

        MixKey(d) := output = HKDF(chainKey, d, "", 64)
                     chainKey = output[0:31]
                     k = output[32:63]

### 1) Mesaj formatı

#### Mevcut Mesaj Formatının İncelemesi

[I2NP](/docs/specs/i2np/) spesifikasyonunda belirtilen Garlic Message aşağıdaki gibidir. Tasarım amacı ara aktarımların yeni ve eski şifrelemeyi ayırt edememesi olduğundan, uzunluk alanı gereksiz olsa bile bu format değiştirilemez. Format tam 16-baytlık başlık ile gösterilmektedir, ancak gerçek başlık kullanılan taşımaya bağlı olarak farklı formatta olabilir.

Şifrelendiği zaman veri, bir dizi Garlic Clove ve ek veri içerir, bunlar Clove Set olarak da bilinir.

Ayrıntılar ve tam spesifikasyon için [I2NP](/docs/specs/i2np/) bölümüne bakın.

```
+----+----+----+----+----+----+----+----+
|type|      msg_id       |  expiration
+----+----+----+----+----+----+----+----+
                         |  size   |chks|
+----+----+----+----+----+----+----+----+
|      length       |                   |
+----+----+----+----+                   +
|          encrypted data               |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
```
#### Şifreli Veri Formatı İncelemesi

ElGamal/AES+SessionTags'de iki mesaj formatı vardır:

1\) Yeni oturum: - 514 bayt ElGamal bloğu - AES bloğu (minimum 128 bayt, 16'nın katı)

2\) Mevcut oturum: - 32 bayt Oturum Etiketi - AES bloğu (minimum 128 bayt, 16'nın katı)

Bu mesajlar, uzunluk alanı içeren bir I2NP garlic mesajında kapsüllenir, böylece uzunluk bilinir.

Alıcı önce ilk 32 byte'ı Session Tag olarak aramaya çalışır. Bulunursa, AES bloğunu çözer. Bulunmazsa ve veri en az (514+16) uzunluğundaysa, ElGamal bloğunu çözmeye çalışır ve başarılı olursa AES bloğunu çözer.

#### Yeni Oturum Etiketleri ve Signal ile Karşılaştırma

Signal Double Ratchet'te, başlık şunları içerir:

- DH: Mevcut ratchet genel anahtarı
- PN: Önceki zincir mesaj uzunluğu
- N: Mesaj Numarası

Signal'in "gönderme zincirleri" kabaca bizim etiket kümelerimize eşdeğerdir. Bir oturum etiketi kullanarak bunun çoğunu ortadan kaldırabiliriz.

New Session'da, şifrelenmemiş başlığa yalnızca public key'i koyuyoruz.

Mevcut Oturumda, başlık için bir oturum etiketi kullanırız. Oturum etiketi, mevcut ratchet genel anahtarı ve mesaj numarası ile ilişkilendirilir.

Hem yeni hem de Mevcut Oturum'da, PN ve N şifreli gövdede bulunur.

Signal'de işler sürekli olarak ratcheting yapıyor. Yeni bir DH public key, alıcının ratchet yapmasını ve geri yeni bir public key göndermesini gerektirir, bu aynı zamanda alınan public key için ack görevi görür. Bu bizim için çok fazla DH işlemi olurdu. Bu yüzden alınan key'in ack'ını ve yeni public key'in iletimini ayırıyoruz. Yeni DH public key'den üretilen session tag kullanan herhangi bir mesaj bir ACK oluşturur. Sadece rekey yapmak istediğimizde yeni bir public key iletiyoruz.

DH'nin ratchet yapması gereken maksimum mesaj sayısı 65535'tir.

Bir oturum anahtarı teslim ederken, oturum etiketlerini de teslim etmek zorunda kalmak yerine "Etiket Kümesi"ni ondan türetiriz. Bir Etiket Kümesi 65536 etikete kadar olabilir. Ancak alıcılar, tüm olası etiketleri aynı anda oluşturmak yerine "öngörü" stratejisi uygulamalıdır. Yalnızca alınan son geçerli etiketten sonra en fazla N etiket oluşturun. N en fazla 128 olabilir, ancak 32 veya daha az daha iyi bir seçim olabilir.

### 1a) Yeni oturum formatı

Yeni Oturum Tek Kullanımlık Genel anahtar (32 byte) Şifrelenmiş veri ve MAC (kalan byte'lar)

New Session mesajı gönderenin statik açık anahtarını içerebilir veya içermeyebilir. Eğer dahil edilmişse, ters oturum bu anahtara bağlanır. Yanıt bekleniyorsa, yani streaming ve yanıtlanabilir datagramlar için statik anahtar dahil edilmelidir. Ham datagramlar için dahil edilmemelidir.

New Session mesajı, tek yönlü Noise [NOISE](https://noiseprotocol.org/noise.html) kalıbı "N" (statik anahtar gönderilmezse) veya iki yönlü kalıp "IK" (statik anahtar gönderilirse) ile benzerdir.

### 1b) Yeni oturum formatı (bağlama ile)

Uzunluk 96 + yük uzunluğudur. Şifreli format:

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|   New Session Ephemeral Public Key    |
+             32 bytes                  +
|     Encoded with Elligator2           |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+         Static Key                    +
|       ChaCha20 encrypted data         |
+            32 bytes                   +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+    (MAC) for Static Key Section       +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Public Key :: 32 bytes, little endian, Elligator2, cleartext

Static Key encrypted data :: 32 bytes

Payload Section encrypted data :: remaining data minus 16 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
#### Yeni Oturum Geçici Anahtarı

Ephemeral key 32 bayttır ve Elligator2 ile kodlanır. Bu anahtar asla yeniden kullanılmaz; yeniden iletimler dahil olmak üzere her mesajla birlikte yeni bir anahtar oluşturulur.

#### Statik Anahtar

Şifresi çözüldüğünde, Alice'in X25519 statik anahtarı, 32 bayt.

#### Yük

Şifrelenmiş uzunluk, verinin geri kalanıdır. Şifresi çözülmüş uzunluk, şifrelenmiş uzunluktan 16 daha azdır. Payload bir DateTime bloğu içermeli ve genellikle bir veya daha fazla Garlic Clove bloğu içerir. Format ve ek gereksinimler için aşağıdaki payload bölümüne bakın.

### 1c) Yeni oturum formatı (bağlama olmadan)

Eğer yanıt gerekli değilse, statik anahtar gönderilmez.

Uzunluk 96 + yük uzunluğudur. Şifrelenmiş format:

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|   New Session Ephemeral Public Key    |
+             32 bytes                  +
|     Encoded with Elligator2           |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+           Flags Section               +
|       ChaCha20 encrypted data         |
+            32 bytes                   +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for above section       +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Public Key :: 32 bytes, little endian, Elligator2, cleartext

Flags Section encrypted data :: 32 bytes

Payload Section encrypted data :: remaining data minus 16 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
#### Yeni Oturum Geçici Anahtarı

Alice'in geçici anahtarı. Geçici anahtar 32 bayttır, Elligator2 ile kodlanmış, küçük endian. Bu anahtar asla yeniden kullanılmaz; yeniden gönderimler dahil olmak üzere her mesajla birlikte yeni bir anahtar oluşturulur.

#### Bayraklar Bölümü Şifresi Çözülmüş veri

Flags bölümü hiçbir şey içermez. Her zaman 32 byte'tır, çünkü bağlama ile New Session mesajları için statik anahtar ile aynı uzunlukta olmalıdır. Bob, 32 byte'ın hepsinin sıfır olup olmadığını test ederek bunun statik anahtar mı yoksa flags bölümü mü olduğunu belirler.

TODO burada herhangi bir bayrak gerekli mi?

#### Yük

Şifrelenmiş uzunluk, verinin geri kalanıdır. Şifresi çözülmüş uzunluk, şifrelenmiş uzunluktan 16 eksiktir. Yük bir DateTime bloğu içermeli ve genellikle bir veya daha fazla Garlic Clove bloğu içerecektir. Format ve ek gereksinimler için aşağıdaki yük bölümüne bakın.

### 1d) Tek seferlik format (bağlama veya oturum yok)

Sadece tek bir mesajın gönderilmesi bekleniyorsa, oturum kurulumu veya statik anahtar gerekli değildir.

Uzunluk 96 + payload uzunluğudur. Şifreli format:

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|       Ephemeral Public Key            |
+             32 bytes                  +
|     Encoded with Elligator2           |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+           Flags Section               +
|       ChaCha20 encrypted data         |
+            32 bytes                   +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for above section       +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Public Key :: 32 bytes, little endian, Elligator2, cleartext

Flags Section encrypted data :: 32 bytes

Payload Section encrypted data :: remaining data minus 16 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
#### Yeni Oturum Tek Kullanımlık Anahtarı

Tek kullanımlık anahtar 32 bayttır, Elligator2 ile kodlanmış, little endian formatında. Bu anahtar asla yeniden kullanılmaz; yeniden iletimler de dahil olmak üzere her mesajla birlikte yeni bir anahtar oluşturulur.

#### Bayraklar Bölümü Şifresi Çözülmüş veri

Flags bölümü hiçbir şey içermez. Her zaman 32 bayttır, çünkü bağlama ile New Session mesajları için statik anahtar ile aynı uzunlukta olmalıdır. Bob, 32 baytın hepsinin sıfır olup olmadığını test ederek bunun bir statik anahtar mı yoksa bir flags bölümü mü olduğunu belirler.

TODO burada herhangi bir bayrak gerekli mi?

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|                                       |
+             All zeros                 +
|              32 bytes                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

zeros:: All zeros, 32 bytes.
```
#### Yük Verisi

Şifreli uzunluk, verinin kalan kısmıdır. Şifresi çözülen uzunluk, şifreli uzunluktan 16 eksiktir. Yük bir DateTime bloğu içermeli ve genellikle bir veya daha fazla Garlic Clove bloğu içerir. Format ve ek gereksinimler için aşağıdaki yük bölümüne bakın.

### 1f) Yeni Oturum Mesajı için KDF'ler

#### Başlangıç ChainKey için KDF

Bu, değiştirilmiş bir protokol adına sahip IK için standart [NOISE](https://noiseprotocol.org/noise.html)'dur. Hem IK kalıbı (bağlı oturumlar) hem de N kalıbı (bağlanmamış oturumlar) için aynı başlatıcıyı kullandığımızı unutmayın.

Protokol adı iki nedenden dolayı değiştirilmiştir. İlk olarak, geçici anahtarların Elligator2 ile kodlandığını belirtmek için, ikinci olarak ise ikinci mesajdan önce tag değerini karıştırmak için MixHash() fonksiyonunun çağrıldığını belirtmek için.

```
This is the "e" message pattern:

// Define protocol_name.
Set protocol_name = "Noise_IKelg2+hs2_25519_ChaChaPoly_SHA256"
 (40 bytes, US-ASCII encoded, no NULL termination).

// Define Hash h = 32 bytes
h = SHA256(protocol_name);

Define ck = 32 byte chaining key. Copy the h data to ck.
Set chainKey = h

// MixHash(null prologue)
h = SHA256(h);

// up until here, can all be precalculated by Alice for all outgoing connections
```
#### Bayraklar/Statik Anahtar Bölümü Şifrelenmiş İçerikleri için KDF

```
This is the "e" message pattern:

// Bob's X25519 static keys
// bpk is published in leaseset
bsk = GENERATE_PRIVATE()
bpk = DERIVE_PUBLIC(bsk)

// Bob static public key
// MixHash(bpk)
// || below means append
h = SHA256(h || bpk);

// up until here, can all be precalculated by Bob for all incoming connections

// Alice's X25519 ephemeral keys
aesk = GENERATE_PRIVATE_ELG2()
aepk = DERIVE_PUBLIC(aesk)

// Alice ephemeral public key
// MixHash(aepk)
// || below means append
h = SHA256(h || aepk);

// h is used as the associated data for the AEAD in the New Session Message
// Retain the Hash h for the New Session Reply KDF
// eapk is sent in cleartext in the
// beginning of the New Session message
elg2_aepk = ENCODE_ELG2(aepk)
// As decoded by Bob
aepk = DECODE_ELG2(elg2_aepk)

End of "e" message pattern.

This is the "es" message pattern:

// Noise es
sharedSecret = DH(aesk, bpk) = DH(bsk, aepk)

// MixKey(DH())
//[chainKey, k] = MixKey(sharedSecret)
// ChaChaPoly parameters to encrypt/decrypt
keydata = HKDF(chainKey, sharedSecret, "", 64)
chainKey = keydata[0:31]

// AEAD parameters
k = keydata[32:63]
n = 0
ad = h
ciphertext = ENCRYPT(k, n, flags/static key section, ad)

End of "es" message pattern.

This is the "s" message pattern:

// MixHash(ciphertext)
// Save for Payload section KDF
h = SHA256(h || ciphertext)

// Alice's X25519 static keys
ask = GENERATE_PRIVATE()
apk = DERIVE_PUBLIC(ask)

End of "s" message pattern.
```
#### Payload Bölümü için KDF (Alice statik anahtarı ile)

```
This is the "ss" message pattern:

// Noise ss
sharedSecret = DH(ask, bpk) = DH(bsk, apk)

// MixKey(DH())
//[chainKey, k] = MixKey(sharedSecret)
// ChaChaPoly parameters to encrypt/decrypt
// chainKey from Static Key Section
Set sharedSecret = X25519 DH result
keydata = HKDF(chainKey, sharedSecret, "", 64)
chainKey = keydata[0:31]

// AEAD parameters
k = keydata[32:63]
n = 0
ad = h
ciphertext = ENCRYPT(k, n, payload, ad)

End of "ss" message pattern.

// MixHash(ciphertext)
// Save for New Session Reply KDF
h = SHA256(h || ciphertext)
```
#### Payload Bölümü için KDF (Alice statik anahtarı olmadan)

Bunun bir Noise "N" deseni olduğunu, ancak bağlı oturumlar için kullandığımız aynı "IK" başlatıcısını kullandığımızı unutmayın.

Yeni Oturum mesajları, statik anahtar şifresi çözülüp incelenene ve tamamının sıfır içerip içermediği belirlenenene kadar Alice'in statik anahtarını içerip içermediği tespit edilemez. Bu nedenle, alıcı tüm Yeni Oturum mesajları için "IK" durum makinesini kullanmalıdır. Eğer statik anahtar tamamen sıfırlardan oluşuyorsa, "ss" mesaj deseni atlanmalıdır.

```
chainKey = from Flags/Static key section
k = from Flags/Static key section
n = 1
ad = h from Flags/Static key section
ciphertext = ENCRYPT(k, n, payload, ad)
```
### 1g) Yeni Oturum Yanıt formatı

Tek bir New Session mesajına yanıt olarak bir veya daha fazla New Session Reply gönderilebilir. Her yanıt, oturum için bir TagSet'ten oluşturulan bir etiketle başlar.

New Session Reply iki bölümden oluşur. İlk bölüm, önüne etiket eklenmiş Noise IK el sıkışmasının tamamlanmasıdır. İlk bölümün uzunluğu 56 bayttır. İkinci bölüm veri fazı yükü (payload) dir. İkinci bölümün uzunluğu 16 + payload uzunluğudur.

Toplam uzunluk 72 + payload uzunluğu. Şifreli format:

```
+----+----+----+----+----+----+----+----+
|       Session Tag   8 bytes           |
+----+----+----+----+----+----+----+----+
|                                       |
+        Ephemeral Public Key           +
|                                       |
+            32 bytes                   +
|     Encoded with Elligator2           |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+  (MAC) for Key Section (no data)      +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Tag :: 8 bytes, cleartext

Public Key :: 32 bytes, little endian, Elligator2, cleartext

MAC :: Poly1305 message authentication code, 16 bytes
       Note: The ChaCha20 plaintext data is empty (ZEROLEN)

Payload Section encrypted data :: remaining data minus 16 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
#### Oturum Etiketi

Etiket, aşağıdaki DH Initialization KDF'de başlatıldığı şekliyle Session Tags KDF'de oluşturulur. Bu, yanıtı oturumla ilişkilendirir. DH Initialization'dan gelen Session Key kullanılmaz.

#### Yeni Oturum Yanıtı Geçici Anahtarı

Bob'un geçici anahtarı. Geçici anahtar 32 bayttır, Elligator2 ile kodlanmış, little endian formatındadır. Bu anahtar asla yeniden kullanılmaz; yeniden iletimler dahil olmak üzere her mesajda yeni bir anahtar üretilir.

#### Yük

Şifrelenmiş uzunluk, verinin geri kalanıdır. Şifresi çözülmüş uzunluk, şifrelenmiş uzunluktan 16 eksiktir. Yük genellikle bir veya daha fazla Garlic Clove bloğu içerir. Format ve ek gereksinimler için aşağıdaki yük bölümüne bakın.

#### Reply TagSet için KDF

TagSet'ten bir veya daha fazla etiket oluşturulur, bu TagSet aşağıdaki KDF kullanılarak başlatılır ve New Session mesajından gelen chainKey kullanılır.

```
// Generate tagset

tagsetKey = HKDF(chainKey, ZEROLEN, "SessionReplyTags", 32)
    tagset_nsr = DH_INITIALIZE(chainKey, tagsetKey)

```
#### Yanıt Anahtarı Bölümü Şifrelenmiş İçerikleri için KDF

```
// Keys from the New Session message
// Alice's X25519 keys
// apk and aepk are sent in original New Session message
// ask = Alice private static key
// apk = Alice public static key
// aesk = Alice ephemeral private key
// aepk = Alice ephemeral public key
// Bob's X25519 static keys
// bsk = Bob private static key
// bpk = Bob public static key

// Generate the tag
tagsetEntry = tagset_nsr.GET_NEXT_ENTRY()
tag = tagsetEntry.SESSION_TAG

// MixHash(tag)
h = SHA256(h || tag)

This is the "e" message pattern:

// Bob's X25519 ephemeral keys
besk = GENERATE_PRIVATE_ELG2()
bepk = DERIVE_PUBLIC(besk)

// Bob's ephemeral public key
// MixHash(bepk)
// || below means append
h = SHA256(h || bepk);

// elg2_bepk is sent in cleartext in the
// beginning of the New Session message
elg2_bepk = ENCODE_ELG2(bepk)
// As decoded by Bob
bepk = DECODE_ELG2(elg2_bepk)

End of "e" message pattern.

This is the "ee" message pattern:

// MixKey(DH())
//[chainKey, k] = MixKey(sharedSecret)
// ChaChaPoly parameters to encrypt/decrypt
// chainKey from original New Session Payload Section
sharedSecret = DH(aesk, bepk) = DH(besk, aepk)
keydata = HKDF(chainKey, sharedSecret, "", 32)
chainKey = keydata[0:31]

End of "ee" message pattern.

This is the "se" message pattern:

// MixKey(DH())
//[chainKey, k] = MixKey(sharedSecret)
sharedSecret = DH(ask, bepk) = DH(besk, apk)
keydata = HKDF(chainKey, sharedSecret, "", 64)
chainKey = keydata[0:31]

// AEAD parameters
k = keydata[32:63]
n = 0
ad = h
ciphertext = ENCRYPT(k, n, ZEROLEN, ad)

End of "se" message pattern.

// MixHash(ciphertext)
h = SHA256(h || ciphertext)

chainKey is used in the ratchet below.
```
#### Payload Bölümü Şifreli İçerikleri için KDF

Bu, bölünme sonrası ilk Mevcut Oturum mesajı gibidir, ancak ayrı bir etiket yoktur. Ayrıca, yükü NSR mesajına bağlamak için yukarıdaki hash'i kullanırız.

```
This is the "ss" message pattern:

// Noise ss
sharedSecret = DH(ask, bpk) = DH(bsk, apk)

// MixKey(DH())
//[chainKey, k] = MixKey(sharedSecret)
// ChaChaPoly parameters to encrypt/decrypt
// chainKey from Static Key Section
Set sharedSecret = X25519 DH result
keydata = HKDF(chainKey, sharedSecret, "", 64)
chainKey = keydata[0:31]

// AEAD parameters
k = keydata[32:63]
n = 0
ad = h
ciphertext = ENCRYPT(k, n, payload, ad)

End of "ss" message pattern.

// MixHash(ciphertext)
// Save for New Session Reply KDF
h = SHA256(h || ciphertext)
```
### Notlar

Yanıtın boyutuna bağlı olarak, her biri benzersiz geçici anahtarlara sahip birden fazla NSR mesajı yanıt olarak gönderilebilir.

Alice ve Bob'un her NS ve NSR mesajı için yeni geçici anahtarlar kullanması gereklidir.

Alice, Mevcut Oturum (ES) mesajları göndermeden önce Bob'un NSR mesajlarından birini almalıdır ve Bob da ES mesajları göndermeden önce Alice'ten bir ES mesajı almalıdır.

Bob'un NSR Payload Section'ından gelen `chainKey` ve `k`, başlangıç ES DH Ratchet'ları için girdi olarak kullanılır (her iki yön için, DH Ratchet KDF'ye bakın).

Bob, Alice'den aldığı ES mesajları için yalnızca Mevcut Oturumları korumalıdır. Oluşturulan diğer tüm gelen ve giden oturumlar (birden fazla NSR için) belirli bir oturum için Alice'in ilk ES mesajını aldıktan hemen sonra yok edilmelidir.

### 1h) Mevcut oturum formatı

Oturum etiketi (8 bayt) Şifrelenmiş veri ve MAC (aşağıdaki bölüm 3'e bakın)

#### Format

Şifrelenmiş:

```
+----+----+----+----+----+----+----+----+
|       Session Tag                     |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+              (MAC)                    +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Session Tag :: 8 bytes, cleartext

Payload Section encrypted data :: remaining data minus 16 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
#### Yük Verisi

Şifrelenmiş uzunluk, verinin geri kalan kısmıdır. Şifresi çözülmüş uzunluk, şifrelenmiş uzunluktan 16 eksiktir. Format ve gereksinimler için aşağıdaki payload bölümüne bakınız.

#### KDF

```
See AEAD section below.

// AEAD parameters for Existing Session payload
k = The 32-byte session key associated with this session tag
n = The message number N in the current chain, as retrieved from the associated Session Tag.
ad = The session tag, 8 bytes
ciphertext = ENCRYPT(k, n, payload, ad)
```
### 2) ECIES-X25519

Format: 32-byte genel ve özel anahtarlar, little-endian.

### 2a) Elligator2

Standart Noise el sıkışmalarında, her yöndeki ilk el sıkışma mesajları açık metin olarak iletilen geçici anahtarlarla başlar. Geçerli X25519 anahtarları rastgele verilerden ayırt edilebildiği için, ortadaki adam bu mesajları rastgele oturum etiketleriyle başlayan Mevcut Oturum mesajlarından ayırt edebilir. [NTCP2](/docs/specs/ntcp2/) ([Prop111](/proposals/111-ntcp2/)) protokolünde, anahtarı gizlemek için bant dışı statik anahtar kullanarak düşük maliyetli bir XOR fonksiyonu kullandık. Ancak buradaki tehdit modeli farklıdır; herhangi bir MitM'in trafiğin hedefini doğrulamak için herhangi bir yöntem kullanmasına veya ilk el sıkışma mesajlarını Mevcut Oturum mesajlarından ayırt etmesine izin vermek istemiyoruz.

Bu nedenle, New Session ve New Session Reply mesajlarındaki geçici anahtarları uniform rastgele dizelerden ayırt edilemez hale getirmek için [Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf) kullanılır.

#### Format

32-baytlık genel ve özel anahtarlar. Kodlanmış anahtarlar little endian formatındadır.

[Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf) içinde tanımlandığı gibi, kodlanmış anahtarlar 254 rastgele bitten ayırt edilemez. 256 rastgele bit (32 bayt) gerektiriyoruz. Bu nedenle, kodlama ve kod çözme aşağıdaki gibi tanımlanır:

Kodlama:

```
ENCODE_ELG2() Definition

// Encode as defined in Elligator2 specification
encodedKey = encode(pubkey)
// OR in 2 random bits to MSB
randomByte = CSRNG(1)
encodedKey[31] |= (randomByte & 0xc0)
```
Kod Çözme:

```
DECODE_ELG2() Definition

// Mask out 2 random bits from MSB
encodedKey[31] &= 0x3f
// Decode as defined in Elligator2 specification
pubkey = decode(encodedKey)
```
#### Notlar

Elligator2, ortalama anahtar üretim süresini iki katına çıkarır, çünkü özel anahtarların yarısı Elligator2 ile kodlama için uygun olmayan genel anahtarlara yol açar. Ayrıca, üretici uygun bir anahtar çifti bulana kadar yeniden denemeye devam etmek zorunda olduğu için anahtar üretim süresi üstel dağılımlı olarak sınırsızdır.

Bu ek yük, uygun anahtarların bir havuzunu tutmak için anahtar üretimini önceden ayrı bir iş parçacığında yaparak yönetilebilir.

Oluşturucu, uygunluğu belirlemek için ENCODE_ELG2() fonksiyonunu yapar. Bu nedenle, oluşturucu ENCODE_ELG2() sonucunu saklamalıdır böylece tekrar hesaplanması gerekmez.

Ek olarak, uygun olmayan anahtarlar Elligator2'nin kullanılmadığı [NTCP2](/docs/specs/ntcp2/) için kullanılan anahtar havuzuna eklenebilir. Bunu yapmanın güvenlik sorunları henüz belirlenmemiştir.

### 3) AEAD (ChaChaPoly)

ChaCha20 ve Poly1305 kullanarak AEAD, [NTCP2](/docs/specs/ntcp2/) ile aynı. Bu [RFC-7539](https://tools.ietf.org/html/rfc7539)'a karşılık gelir ve TLS [RFC-7905](https://tools.ietf.org/html/rfc7905)'te de benzer şekilde kullanılır.

#### Yeni Oturum ve Yeni Oturum Yanıtı Girdileri

Yeni Oturum mesajındaki bir AEAD bloğu için şifreleme/şifre çözme fonksiyonlarının girdileri:

```
k :: 32 byte cipher key
     See New Session and New Session Reply KDFs above.

n :: Counter-based nonce, 12 bytes.
     n = 0

ad :: Associated data, 32 bytes.
      The SHA256 hash of the preceding data, as output from mixHash()

data :: Plaintext data, 0 or more bytes
```
#### Mevcut Oturum Girdileri

Mevcut Oturum mesajındaki bir AEAD bloğu için şifreleme/şifre çözme fonksiyonlarına girdiler:

```
k :: 32 byte session key
     As looked up from the accompanying session tag.

n :: Counter-based nonce, 12 bytes.
     Starts at 0 and incremented for each message when transmitting.
     For the receiver, the value
     as looked up from the accompanying session tag.
     First four bytes are always zero.
     Last eight bytes are the message number (n), little-endian encoded.
     Maximum value is 65535.
     Session must be ratcheted when N reaches that value.
     Higher values must never be used.

ad :: Associated data
      The session tag

data :: Plaintext data, 0 or more bytes
```
#### Şifrelenmiş Format

Şifreleme fonksiyonunun çıktısı, şifre çözme fonksiyonunun girdisi:

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|       ChaCha20 encrypted data         |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+              (MAC)                    +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

encrypted data :: Same size as plaintext data, 0 - 65519 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
#### Notlar

- ChaCha20 bir akış şifresi olduğundan, düz metinlerin doldurulmasına gerek yoktur.
  Ek anahtar akışı baytları atılır.
- Şifre için anahtar (256 bit) SHA256 KDF aracılığıyla üzerinde anlaşılır. Her mesaj için KDF'nin ayrıntıları aşağıdaki ayrı bölümlerde yer almaktadır.
- ChaChaPoly çerçeveleri I2NP veri mesajında kapsüllendiği için bilinen boyuttadır.
- Tüm mesajlar için dolgu, kimlik doğrulaması yapılan veri çerçevesinin içindedir.

#### AEAD Hata İşleme

AEAD doğrulamasını geçemeyen tüm alınan veriler atılmalıdır. Hiçbir yanıt döndürülmez.

### 4) Ratchets

Hala önceki gibi session tag'leri kullanıyoruz, ancak bunları üretmek için ratchet'ları kullanıyoruz. Session tag'lerin hiç uygulamadığımız bir rekey seçeneği de vardı. Yani çift ratchet gibi ama ikincisini hiç yapmadık.

Burada Signal'in Double Ratchet'ına benzer bir şey tanımlıyoruz. Oturum etiketleri, alıcı ve gönderici taraflarında deterministik ve özdeş olarak üretilir.

Simetrik anahtar/etiket cırcırı kullanarak, gönderen tarafında session etiketlerini depolamak için bellek kullanımını ortadan kaldırıyoruz. Ayrıca etiket kümelerini göndermenin bant genişliği tüketimini de ortadan kaldırıyoruz. Alıcı tarafındaki kullanım hala önemli, ancak session etiketini 32 bayttan 8 bayta küçülteceğimiz için bunu daha da azaltabiliriz.

Signal'da belirtilen (ve isteğe bağlı) başlık şifrelemesini kullanmıyoruz, bunun yerine oturum etiketleri kullanıyoruz.

Bir DH ratchet kullanarak, ElGamal/AES+SessionTags'de hiç uygulanmamış olan ileri gizlilik sağlarız.

Not: Yeni Oturum tek kullanımlık genel anahtarı ratchet'in bir parçası değildir, tek işlevi Alice'in ilk DH ratchet anahtarını şifrelemektir.

#### Mesaj Numaraları

Double Ratchet, kayıp veya sıra dışı mesajları her mesaj başlığına bir etiket dahil ederek ele alır. Alıcı etiketin indeksini arar, bu mesaj numarası N'dir. Mesaj bir PN değeri içeren Message Number bloğu içeriyorsa, alıcı önceki etiket setinde o değerden daha yüksek olan etiketleri silebilir, aynı zamanda atlanan mesajların daha sonra gelmesi durumuna karşı önceki etiket setindeki atlanan etiketleri saklayabilir.

#### Örnek Uygulama

Bu ratchet'ları uygulamak için aşağıdaki veri yapılarını ve fonksiyonları tanımlıyoruz.

TAGSET_ENTRY

Bir TAGSET içindeki tek bir girdi.

    INDEX

    :   An integer index, starting with 0

    SESSION_TAG

    :   An identifier to go out on the wire, 8 bytes

    SESSION_KEY

    :   A symmetric key, never goes on the wire, 32 bytes

TAGSET

TAGSET_ENTRIES koleksiyonu.

    CREATE(key, n)

    :   Generate a new TAGSET using initial cryptographic key material
        of 32 bytes. The associated session identifier is provided. The
        initial number of of tags to create is specified; this is
        generally 0 or 1 for an outgoing session. LAST_INDEX = -1
        EXTEND(n) is called.

    EXTEND(n)

    :   Generate n more TAGSET_ENTRIES by calling EXTEND() n times.

    EXTEND()

    :   Generate one more TAGSET_ENTRY, unless the maximum number
        SESSION_TAGS have already been generated. If LAST_INDEX is
        greater than or equal to 65535, return. ++ LAST_INDEX Create a
        new TAGSET_ENTRY with the LAST_INDEX value and the calculated
        SESSION_TAG. Calls RATCHET_TAG() and (optionally) RATCHET_KEY().
        For inbound sessions, the calculation of the SESSION_KEY may be
        deferred and calculated in GET_SESSION_KEY(). Calls EXPIRE()

    EXPIRE()

    :   Remove tags and keys that are too old, or if the TAGSET size
        exceeds some limit.

    RATCHET_TAG()

    :   Calculates the next SESSION_TAG based on the last SESSION_TAG.

    RATCHET_KEY()

    :   Calculates the next SESSION_KEY based on the last SESSION_KEY.

    SESSION

    :   The associated session.

    CREATION_TIME

    :   When the TAGSET was created.

    LAST_INDEX

    :   The last TAGSET_ENTRY INDEX generated by EXTEND().

    GET_NEXT_ENTRY()

    :   Used for outgoing sessions only. EXTEND(1) is called if there
        are no remaining TAGSET_ENTRIES. If EXTEND(1) did nothing, the
        max of 65535 TAGSETS have been used, and return an error.
        Returns the next unused TAGSET_ENTRY.

    GET_SESSION_KEY(sessionTag)

    :   Used for incoming sessions only. Returns the TAGSET_ENTRY
        containing the sessionTag. If found, the TAGSET_ENTRY is
        removed. If the SESSION_KEY calculation was deferred, it is
        calculated now. If there are few TAGSET_ENTRIES remaining,
        EXTEND(n) is called.

#### 4a) DH Ratchet

Ratchet yapar ancak Signal'in yaptığı kadar hızlı değil. Alınan anahtarın onaylanmasını yeni anahtar üretiminden ayırırız. Tipik kullanımda, Alice ve Bob her biri Yeni Oturumda hemen ratchet yapar (iki kez), ancak tekrar ratchet yapmaz.

Bir ratchet'ın tek yön için olduğunu ve o yön için bir Yeni Oturum etiketi / mesaj anahtarı ratchet zinciri oluşturduğunu unutmayın. Her iki yön için anahtarlar oluşturmak için iki kez ratchet yapmanız gerekir.

Her yeni anahtar oluşturup gönderdiğinizde ratchet yaparsınız. Her yeni anahtar aldığınızda ratchet yaparsınız.

Alice bağlanmamış giden oturum oluştururken bir kez ratchet yapar, gelen oturum oluşturmaz (bağlanmamış yanıtlanamaz demektir).

Bob, bağlı olmayan bir gelen oturum oluştururken bir kez ratchet yapar ve karşılık gelen bir giden oturum oluşturmaz (bağlı olmayan yanıtlanamaz).

Alice, Bob'un New Session Reply (NSR) mesajlarından birini alana kadar Bob'a New Session (NS) mesajları göndermeye devam eder. Daha sonra NSR'nin Payload Section KDF sonuçlarını oturum ratchet'ları için girdi olarak kullanır (DH Ratchet KDF'ye bakın) ve Existing Session (ES) mesajları göndermeye başlar.

Alınan her NS mesajı için, Bob yeni bir gelen oturum oluşturur ve yanıt Payload Section'ının KDF sonuçlarını yeni gelen ve giden ES DH Ratchet için girdi olarak kullanır.

Her gerekli yanıt için, Bob Alice'e yanıtı payload içinde bulunan bir NSR mesajı gönderir. Bob'un her NSR için yeni ephemeral anahtarlar kullanması gereklidir.

Bob, karşılık gelen giden oturumda ES mesajları oluşturup göndermeden önce, gelen oturumlardan birinde Alice'den bir ES mesajı almalıdır.

Alice, Bob'tan bir NSR mesajı almak için bir zamanlayıcı kullanmalıdır. Zamanlayıcı süresi dolarsa, oturum kaldırılmalıdır.

KCI ve/veya kaynak tüketimi saldırısından kaçınmak için (saldırgan Bob'un NSR yanıtlarını düşürerek Alice'in NS mesajları göndermeye devam etmesini sağlar), Alice zamanlayıcı süresi dolması nedeniyle belirli sayıda yeniden denemeden sonra Bob'a Yeni Oturum başlatmaktan kaçınmalıdır.

Alice ve Bob, alınan her NextKey bloğu için bir DH ratchet yapar.

Alice ve Bob, her DH ratchet sonrasında yeni etiket kümeleri ve iki simetrik anahtar ratchet'i oluşturur. Belirli bir yöndeki her yeni ES mesajı için, Alice ve Bob oturum etiketi ve simetrik anahtar ratchet'lerini ilerletir.

İlk el sıkışmadan sonra DH ratchet'ların sıklığı implementasyona bağlıdır. Protokol bir ratchet gerekli olmadan önce 65535 mesaj sınırı koysa da, daha sık ratcheting (mesaj sayısına, geçen zamana veya her ikisine dayalı olarak) ek güvenlik sağlayabilir.

Bağlı oturumlarda son handshake KDF'den sonra, Bob ve Alice gelen ve giden oturumlar için bağımsız simetrik ve etiket zinciri anahtarları oluşturmak için ortaya çıkan CipherState üzerinde Noise Split() fonksiyonunu çalıştırmalıdır.

##### ANAHTAR VE ETİKET SETİ KİMLİKLERİ

Anahtar ve etiket kümesi kimlik numaraları, anahtarları ve etiket kümelerini tanımlamak için kullanılır. Anahtar kimlikleri, NextKey bloklarında gönderilen veya kullanılan anahtarı tanımlamak için kullanılır. Etiket kümesi kimlikleri, ACK bloklarında (mesaj numarası ile birlikte) onaylanan mesajı tanımlamak için kullanılır. Hem anahtar hem de etiket kümesi kimlikleri tek yön için etiket kümelerine uygulanır. Anahtar ve etiket kümesi kimlik numaraları sıralı olmalıdır.

Bir oturumda her yönde kullanılan ilk etiket setlerinde, etiket seti ID'si 0'dır. NextKey blokları gönderilmemiştir, bu nedenle anahtar ID'leri yoktur.

Bir DH ratchet başlatmak için, gönderici 0 anahtar ID'sine sahip yeni bir NextKey bloğu iletir. Alıcı 0 anahtar ID'sine sahip yeni bir NextKey bloğu ile yanıtlar. Gönderici daha sonra 1 etiket kümesi ID'si ile yeni bir etiket kümesi kullanmaya başlar.

Sonraki etiket setleri benzer şekilde oluşturulur. NextKey değişimlerinden sonra kullanılan tüm etiket setleri için, etiket seti numarası (1 + Alice'in anahtar ID'si + Bob'un anahtar ID'si)'dir.

Anahtar ve etiket kümesi ID'leri 0'dan başlar ve sıralı olarak artar. Maksimum etiket kümesi ID'si 65535'tir. Maksimum anahtar ID'si 32767'dir. Bir etiket kümesi neredeyse tükendiğinde, etiket kümesi göndereni bir NextKey değişimi başlatmalıdır. 65535 etiket kümesi neredeyse tükendiğinde, etiket kümesi göndereni bir Yeni Oturum mesajı göndererek yeni bir oturum başlatmalıdır.

1730'luk streaming maksimum mesaj boyutu ile ve yeniden iletim olmadığı varsayımıyla, tek bir etiket seti kullanarak teorik maksimum veri transferi 1730 * 65536 ~= 108 MB'dır. Gerçek maksimum değer yeniden iletimler nedeniyle daha düşük olacaktır.

Mevcut 65536 etiket setinin tamamı kullanıldığında, oturum atılıp değiştirilmeden önce teorik maksimum veri aktarımı 64K * 108 MB ~= 6.9 TB'dir.

##### DH RATCHET MESAJ AKIŞI

Bir etiket seti için bir sonraki anahtar değişimi, o etiketlerin göndereni (giden etiket setinin sahibi) tarafından başlatılmalıdır. Alıcı (gelen etiket setinin sahibi) yanıt verecektir. Uygulama katmanındaki tipik bir HTTP GET trafiği için, Bob daha fazla mesaj gönderecek ve anahtar değişimini başlatarak ilk ratchet'i yapacaktır; aşağıdaki diyagram bunu göstermektedir. Alice ratchet yaptığında, aynı şey tersine gerçekleşir.

NS/NSR el sıkışmasından sonra kullanılan ilk etiket seti, etiket seti 0'dır. Etiket seti 0 neredeyse tükendiğinde, etiket seti 1'i oluşturmak için her iki yönde de yeni anahtarlar değiştirilmelidir. Bundan sonra, yeni bir anahtar yalnızca tek yönde gönderilir.

Tag set 2'yi oluşturmak için, tag gönderici yeni bir anahtar gönderir ve tag alıcı onaylamak için eski anahtarının ID'sini gönderir. Her iki taraf da DH yapar.

Tag set 3'ü oluşturmak için, tag göndereni eski anahtarının ID'sini gönderir ve tag alıcısından yeni bir anahtar talep eder. Her iki taraf da bir DH yapar.

Sonraki tag setleri, tag set 2 ve 3 için olduğu gibi oluşturulur. Tag set numarası (1 + gönderen anahtar kimliği + alıcı anahtar kimliği)'dir.

```
Tag Sender                    Tag Receiver

                 ... use tag set #0 ...


(Tagset #0 almost empty)
(generate new key #0)

Next Key, forward, request reverse, with key #0  -------->
(repeat until next key received)

                            (generate new key #0, do DH, create IB Tagset #1)

        <-------------      Next Key, reverse, with key #0
                            (repeat until tag received on new tagset)

(do DH, create OB Tagset #1)


                 ... use tag set #1 ...


(Tagset #1 almost empty)
(generate new key #1)

Next Key, forward, with key #1        -------->
(repeat until next key received)

                            (reuse key #0, do DH, create IB Tagset #2)

        <--------------     Next Key, reverse, id 0
                            (repeat until tag received on new tagset)

(do DH, create OB Tagset #2)


                 ... use tag set #2 ...


(Tagset #2 almost empty)
(reuse key #1)

Next Key, forward, request reverse, id 1  -------->
(repeat until next key received)

                            (generate new key #1, do DH, create IB Tagset #3)

        <--------------     Next Key, reverse, with key #1

(do DH, create OB Tagset #3)
(reuse key #1, do DH, create IB Tagset #3)



                 ... use tag set #3 ...



     After tag set 3, repeat the above
     patterns as shown for tag sets 2 and 3.

     To create a new even-numbered tag set, the sender sends a new key
     to the receiver. The receiver sends his old key ID
     back as an acknowledgement.

     To create a new odd-numbered tag set, the sender sends a reverse request
     to the receiver. The receiver sends a new reverse key to the sender.
```
Giden tagset için DH ratchet tamamlandıktan ve yeni bir giden tagset oluşturulduktan sonra, hemen kullanılmalı ve eski giden tagset silinebilir.

Bir gelen tagset için DH ratchet tamamlandıktan ve yeni bir gelen tagset oluşturulduktan sonra, alıcı her iki tagset'teki tag'leri dinlemeli ve eski tagset'i kısa bir süre sonra, yaklaşık 3 dakika sonra silmelidir.

Etiket kümesi ve anahtar kimliği ilerlemesinin özeti aşağıdaki tabloda verilmiştir. * yeni bir anahtarın oluşturulduğunu gösterir.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">New Tag Set ID</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Sender key ID</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Rcvr key ID</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">n/a</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">n/a</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 *</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 *</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 *</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 *</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2 *</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2 *</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">...</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">...</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">...</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">65534</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32767 *</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32766</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">65535</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32767</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32767 *</td>
</tr>
</table>
Anahtar ve etiket seti kimlik numaraları sıralı olmalıdır.

##### DH BAŞLATMA KDF

Bu, tek yön için DH_INITIALIZE(rootKey, k) tanımıdır. Bir etiket kümesi ve gerekirse sonraki bir DH ratchet için kullanılacak "sonraki kök anahtar" oluşturur.

DH başlatmayı üç yerde kullanırız. İlk olarak, Yeni Oturum Yanıtları için bir etiket seti oluşturmak üzere kullanırız. İkinci olarak, Mevcut Oturum mesajlarında kullanmak için her yön için birer tane olmak üzere iki etiket seti oluşturmak için kullanırız. Son olarak, ek Mevcut Oturum mesajları için tek yönde yeni bir etiket seti oluşturmak üzere DH Ratchet'ten sonra kullanırız.

```
Inputs:
1) rootKey = chainKey from Payload Section
2) k from the New Session KDF or split()

// KDF_RK(rk, dh_out)
keydata = HKDF(rootKey, k, "KDFDHRatchetStep", 64)

// Output 1: The next Root Key (KDF input for the next DH ratchet)
nextRootKey = keydata[0:31]
// Output 2: The chain key to initialize the new
// session tag and symmetric key ratchets
// for the tag set
ck = keydata[32:63]

// session tag and symmetric key chain keys
keydata = HKDF(ck, ZEROLEN, "TagAndKeyGenKeys", 64)
sessTag_ck = keydata[0:31]
symmKey_ck = keydata[32:63]
```
##### DH RATCHET KDF

Bu, bir tagset tükenmeden önce, NextKey bloklarında yeni DH anahtarları değiştirildikten sonra kullanılır.

```
// Tag sender generates new X25519 ephemeral keys
// and sends rapk to tag receiver in a NextKey block
rask = GENERATE_PRIVATE()
rapk = DERIVE_PUBLIC(rask)

// Tag receiver generates new X25519 ephemeral keys
// and sends rbpk to Tag sender in a NextKey block
rbsk = GENERATE_PRIVATE()
rbpk = DERIVE_PUBLIC(rbsk)

sharedSecret = DH(rask, rbpk) = DH(rbsk, rapk)
tagsetKey = HKDF(sharedSecret, ZEROLEN, "XDHRatchetTagSet", 32)
rootKey = nextRootKey // from previous tagset in this direction
newTagSet = DH_INITIALIZE(rootKey, tagsetKey)
```
#### 4b) Oturum Etiketi Ratchet

Signal'de olduğu gibi her mesaj için ratchet'ler. Oturum etiketi ratchet'i simetrik anahtar ratchet'i ile senkronize edilir, ancak alıcı anahtar ratchet'i bellek tasarrufu için "geride kalabilir".

Transmitter, iletilen her mesaj için bir kez ratchet yapar. Ek etiketlerin saklanmasına gerek yoktur. Transmitter ayrıca mevcut zincirdeki mesajın mesaj numarası olan 'N' için bir sayaç tutmalıdır. 'N' değeri gönderilen mesaja dahil edilir. Mesaj Numarası blok tanımına bakın.

Alıcı, maksimum pencere boyutu kadar ileri ratchet yapmalı ve etiketleri oturumla ilişkili bir "etiket seti"nde saklamalıdır. Alındıktan sonra, saklanan etiket atılabilir ve önceki alınmamış etiketler yoksa, pencere ilerletilebilir. Alıcı, her oturum etiketiyle ilişkili 'N' değerini tutmalı ve gönderilen mesajdaki sayının bu değerle eşleştiğini kontrol etmelidir. Mesaj Numarası blok tanımına bakın.

##### KDF

Bu RATCHET_TAG() tanımıdır.

```
Inputs:
1) Session Tag Chain key sessTag_ck
   First time: output from DH ratchet
   Subsequent times: output from previous session tag ratchet

Generated:
2) input_key_material = SESSTAG_CONSTANT
   Must be unique for this tag set (generated from chain key),
   so that the sequence isn't predictable, since session tags
   go out on the wire in plaintext.

Outputs:
1) N (the current session tag number)
2) the session tag (and symmetric key, probably)
3) the next Session Tag Chain Key (KDF input for the next session tag ratchet)

Initialization:
keydata = HKDF(sessTag_ck, ZEROLEN, "STInitialization", 64)
// Output 1: Next chain key
sessTag_chainKey = keydata[0:31]
// Output 2: The constant
SESSTAG_CONSTANT = keydata[32:63]

// KDF_ST(ck, constant)
keydata_0 = HKDF(sessTag_chainkey, SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
// Output 1: Next chain key
sessTag_chainKey_0 = keydata_0[0:31]
// Output 2: The session tag
// or more if tag is longer than 8 bytes
tag_0 = keydata_0[32:39]

// repeat as necessary to get to tag_n
keydata_n = HKDF(sessTag_chainKey_(n-1), SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
// Output 1: Next chain key
sessTag_chainKey_n = keydata_n[0:31]
// Output 2: The session tag
// or more if tag is longer than 8 bytes
tag_n = keydata_n[32:39]
```
#### 4c) Simetrik Anahtar Ratchet

Signal'de olduğu gibi her mesaj için ratchet'ler. Her simetrik anahtar ilişkili bir mesaj numarası ve oturum etiketine sahiptir. Oturum anahtarı ratchet'i simetrik etiket ratchet'i ile senkronize edilir, ancak alıcı anahtar ratchet'i bellek tasarrufu için "geride kalabilir".

Verici, gönderilen her mesaj için bir kez ratchet yapar. Ek anahtarların saklanması gerekmez.

Alıcı bir session tag aldığında, simetrik anahtar ratchet'ını ilişkili anahtara kadar ilerletmemişse, ilişkili anahtara "yetişmek" zorundadır. Alıcı muhtemelen henüz alınmamış olan önceki tag'ler için anahtarları önbelleğe alacaktır. Alındıktan sonra, saklanan anahtar atılabilir ve eğer önceki alınmamış tag'ler yoksa, pencere ilerletilebilir.

Verimlilik için, session tag ve simetrik anahtar ratchet'ları ayrıdır, böylece session tag ratchet'ı simetrik anahtar ratchet'ından önde çalışabilir. Bu aynı zamanda ek güvenlik sağlar, çünkü session tag'ları hat üzerinden gönderilir.

##### KDF

Bu RATCHET_KEY() fonksiyonunun tanımıdır.

```
Inputs:
1) Symmetric Key Chain key symmKey_ck
   First time: output from DH ratchet
   Subsequent times: output from previous symmetric key ratchet

Generated:
2) input_key_material = SYMMKEY_CONSTANT = ZEROLEN
   No need for uniqueness. Symmetric keys never go out on the wire.
   TODO: Set a constant anyway?

Outputs:
1) N (the current session key number)
2) the session key
3) the next Symmetric Key Chain Key (KDF input for the next symmetric key ratchet)

// KDF_CK(ck, constant)
SYMMKEY_CONSTANT = ZEROLEN
// Output 1: Next chain key
keydata_0 = HKDF(symmKey_ck, SYMMKEY_CONSTANT, "SymmetricRatchet", 64)
symmKey_chainKey_0 = keydata_0[0:31]
// Output 2: The symmetric key
k_0 = keydata_0[32:63]

// repeat as necessary to get to k[n]
keydata_n = HKDF(symmKey_chainKey_(n-1), SYMMKEY_CONSTANT, "SymmetricRatchet", 64)
// Output 1: Next chain key
symmKey_chainKey_n = keydata_n[0:31]
// Output 2: The symmetric key
k_n = keydata_n[32:63]
```
### 5) Yük

Bu, ElGamal/AES+SessionTags spesifikasyonunda tanımlanan AES bölüm formatını değiştirir.

Bu, [NTCP2](/docs/specs/ntcp2/) spesifikasyonunda tanımlanan aynı blok formatını kullanır. Bireysel blok türleri farklı şekilde tanımlanır.

Uygulayıcıların kod paylaşımını teşvik etmenin ayrıştırma sorunlarına yol açabileceği endişeleri bulunmaktadır. Uygulayıcılar kod paylaşımının faydalarını ve risklerini dikkatli bir şekilde değerlendirmeli ve iki bağlam için sıralama ve geçerli blok kurallarının farklı olduğundan emin olmalıdır.

#### Payload Bölümü Şifresi çözülmüş veri

Şifrelenmiş uzunluk, verinin kalan kısmıdır. Şifresi çözülmüş uzunluk, şifrelenmiş uzunluktan 16 eksiktir. Tüm blok türleri desteklenir. Tipik içerikler aşağıdaki blokları içerir:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Payload Block Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type Number</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Block Length</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">DateTime</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Termination (TBD)</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">9 typ.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Options (TBD)</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">21+</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Message Number (TBD)</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">TBD</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Next Key</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3 or 35</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">ACK</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4 typ.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">ACK Request</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">9</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Garlic Clove</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">varies</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Padding</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">254</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">varies</td>
</tr>
</table>
#### Şifrelenmemiş veri

Şifrelenmiş çerçevede sıfır veya daha fazla blok bulunur. Her blok bir baytlık tanımlayıcı, iki baytlık uzunluk ve sıfır veya daha fazla bayt veri içerir.

Genişletilebilirlik için, alıcılar bilinmeyen tip numaralarına sahip blokları ZORUNLU olarak görmezden gelmeli ve bunları dolgu olarak değerlendirmelidir.

Şifrelenmiş veri maksimum 65535 bayttır ve 16-baytlık kimlik doğrulama başlığını içerir, bu nedenle maksimum şifrelenmemiş veri 65519 bayttır.

(Poly1305 doğrulama etiketi gösterilmedi):

```
+----+----+----+----+----+----+----+----+
|blk |  size   |       data             |
+----+----+----+                        +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
|blk |  size   |       data             |
+----+----+----+                        +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
~               .   .   .               ~

blk :: 1 byte
       0 datetime
       1-3 reserved
       4 termination
       5 options
       6 previous message number
       7 next session key
       8 ack
       9 ack request
       10 reserved
       11 Garlic Clove
       224-253 reserved for experimental features
       254 for padding
       255 reserved for future extension
size :: 2 bytes, big endian, size of data to follow, 0 - 65516
data :: the data

Maximum ChaChaPoly frame is 65535 bytes.
Poly1305 tag is 16 bytes
Maximum total block size is 65519 bytes
Maximum single block size is 65519 bytes
Block type is 1 byte
Block length is 2 bytes
Maximum single block data size is 65516 bytes.
```
#### Blok Sıralama Kuralları

New Session mesajında, DateTime bloğu gereklidir ve ilk blok olmalıdır.

Diğer izin verilen bloklar:

- Garlic Clove (tip 11)
- Seçenekler (tip 5)
- Dolgu (tip 254)

New Session Reply mesajında hiçbir blok gerekli değildir.

Diğer izin verilen bloklar:

- Garlic Clove (tip 11)
- Seçenekler (tip 5)
- Dolgu (tip 254)

Başka hiçbir bloka izin verilmez. Dolgu (padding) varsa, son blok olmalıdır.

Mevcut Oturum mesajında, aşağıdaki gereksinimler dışında hiçbir blok gerekli değildir ve sıra belirtilmemiştir:

Termination, eğer mevcutsa, Padding dışında son blok olmalıdır. Padding, eğer mevcutsa, son blok olmalıdır.

Tek bir çerçevede birden fazla Garlic Clove bloğu olabilir. Tek bir çerçevede en fazla iki Next Key bloğu olabilir. Tek bir çerçevede birden fazla Padding bloğuna izin verilmez. Diğer blok türlerinin muhtemelen tek bir çerçevede birden fazla bloğu olmayacaktır, ancak bu yasaklanmamıştır.

#### TarihSaat

Bir son kullanma tarihi. Tekrar saldırılarının önlenmesine yardımcı olur. Bob, bu zaman damgasını kullanarak mesajın güncel olduğunu doğrulamalıdır. Zaman geçerliyse, Bob tekrar saldırılarını önlemek için bir Bloom filtresi veya başka bir mekanizma uygulamalıdır. Bob ayrıca, şifre çözme işleminden önce son dönemdeki yinelenen NS mesajlarını tespit etmek ve atmak için yinelenen geçici anahtar (Elligator2 çözümlemesi öncesi veya sonrası) kontrolü yapabilir. Genellikle yalnızca New Session mesajlarında bulunur.

```
+----+----+----+----+----+----+----+
| 0  |    4    |     timestamp     |
+----+----+----+----+----+----+----+

blk :: 0
size :: 2 bytes, big endian, value = 4
timestamp :: Unix timestamp, unsigned seconds.
             Wraps around in 2106
```
#### Garlic Clove

[I2NP](/docs/specs/i2np/)'de belirtildiği gibi tek bir çözülmüş Garlic Clove, kullanılmayan veya gereksiz alanları kaldırmak için yapılan değişikliklerle birlikte. Uyarı: Bu format ElGamal/AES formatından önemli ölçüde farklıdır. Her clove ayrı bir payload bloğudur. Garlic Clove'lar bloklar arasında veya ChaChaPoly çerçeveleri arasında parçalanamaz.

```
+----+----+----+----+----+----+----+----+
| 11 |  size   |                        |
+----+----+----+                        +
|      Delivery Instructions            |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|type|  Message_ID       | Expiration   
+----+----+----+----+----+----+----+----+
     |      I2NP Message body           |
+----+                                  +
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

size :: size of all data to follow

Delivery Instructions :: As specified in
       the Garlic Clove section of [I2NP]_.
       Length varies but is typically 1, 33, or 37 bytes

type :: I2NP message type

Message_ID :: 4 byte `Integer` I2NP message ID

Expiration :: 4 bytes, seconds since the epoch
```
Notlar:

- Uygulayıcılar, bir blok okunurken hatalı biçimlendirilmiş veya kötü niyetli verilerin bir sonraki bloğa taşan okumalar yapmamasını sağlamalıdır.
- [I2NP](/docs/specs/i2np/) içinde belirtilen Clove Set formatı kullanılmaz. Her clove kendi bloğunda bulunur.
- I2NP mesaj başlığı 9 byte olup, [NTCP2](/docs/specs/ntcp2/) içinde kullanılanla aynı formata sahiptir.
- [I2NP](/docs/specs/i2np/) içindeki Garlic Message tanımından Certificate, Message ID ve Expiration dahil edilmez.
- [I2NP](/docs/specs/i2np/) içindeki Garlic Clove tanımından Certificate, Clove ID ve Expiration dahil edilmez.

#### Sonlandırma

Uygulanması isteğe bağlıdır. Oturumu sonlandır. Bu, çerçevedeki son dolgu olmayan blok olmalıdır. Bu oturumda daha fazla mesaj gönderilmeyecektir.

NS veya NSR'de izin verilmez. Yalnızca Mevcut Oturum mesajlarında dahil edilir.

```
+----+----+----+----+----+----+----+----+
| 4  |  size   | rsn|     addl data     |
+----+----+----+----+                   +
~               .   .   .               ~
+----+----+----+----+----+----+----+----+

blk :: 4
size :: 2 bytes, big endian, value = 1 or more
rsn :: reason, 1 byte:
       0: normal close or unspecified
       1: termination received
       others: optional, impementation-specific
addl data :: optional, 0 or more bytes, for future expansion, debugging,
             or reason text.
             Format unspecified and may vary based on reason code.
```
#### Seçenekler

UYGULANMAMIŞ, daha fazla çalışma için. Güncellenmiş seçenekleri geçir. Seçenekler oturum için çeşitli parametreler içerir. Daha fazla bilgi için aşağıdaki Session Tag Length Analysis bölümüne bakın.

Seçenekler bloğu değişken uzunlukta olabilir, çünkü more_options mevcut olabilir.

```
+----+----+----+----+----+----+----+----+
| 5  |  size   |ver |flg |STL |STimeout |
+----+----+----+----+----+----+----+----+
|  SOTW   |  RITW   |tmin|tmax|rmin|rmax|
+----+----+----+----+----+----+----+----+
|  tdmy   |  rdmy   |  tdelay |  rdelay |
+----+----+----+----+----+----+----+----+
|              more_options             |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 5
size :: 2 bytes, big endian, size of options to follow, 21 bytes minimum
ver :: Protocol version, must be 0
flg :: 1 byte flags
       bits 7-0: Unused, set to 0 for future compatibility
STL :: Session tag length (must be 8), other values unimplemented
STimeout :: Session idle timeout (seconds), big endian
SOTW :: Sender Outbound Tag Window, 2 bytes big endian
RITW :: Receiver Inbound Tag Window 2 bytes big endian

tmin, tmax, rmin, rmax :: requested padding limits
    tmin and rmin are for desired resistance to traffic analysis.
    tmax and rmax are for bandwidth limits.
    tmin and tmax are the transmit limits for the router sending this options block.
    rmin and rmax are the receive limits for the router sending this options block.
    Each is a 4.4 fixed-point float representing 0 to 15.9375
    (or think of it as an unsigned 8-bit integer divided by 16.0).
    This is the ratio of padding to data. Examples:
    Value of 0x00 means no padding
    Value of 0x01 means add 6 percent padding
    Value of 0x10 means add 100 percent padding
    Value of 0x80 means add 800 percent (8x) padding
    Alice and Bob will negotiate the minimum and maximum in each direction.
    These are guidelines, there is no enforcement.
    Sender should honor receiver's maximum.
    Sender may or may not honor receiver's minimum, within bandwidth constraints.

tdmy: Max dummy traffic willing to send, 2 bytes big endian, bytes/sec average
rdmy: Requested dummy traffic, 2 bytes big endian, bytes/sec average
tdelay: Max intra-message delay willing to insert, 2 bytes big endian, msec average
rdelay: Requested intra-message delay, 2 bytes big endian, msec average

more_options :: Format undefined, for future use
```
SOTW, gönderenin alıcıya yönelik gelen etiket penceresi (maksimum öngörü) önerisidir. RITW ise gönderenin kullanmayı planladığı gelen etiket penceresi (maksimum öngörü) beyanıdır. Her taraf daha sonra öngörüyü minimum, maksimum veya başka bir hesaplamaya dayalı olarak ayarlar veya düzenler.

Notlar:

- Varsayılan olmayan oturum etiketi uzunluğu desteğinin asla gerekli olmayacağı umulmaktadır.
- Etiket penceresi Signal belgelerinde MAX_SKIP'tir.

Sorunlar:

- Seçenek müzakeresi henüz belirlenmemiş.
- Varsayılanlar henüz belirlenmemiş.
- Doldurma ve gecikme seçenekleri NTCP2'den kopyalanmış, ancak bu seçenekler orada tam olarak uygulanmamış veya incelenmemiş.

#### Mesaj Numaraları

Uygulama isteğe bağlıdır. Önceki etiket kümesindeki uzunluk (gönderilen mesaj sayısı) (PN). Alıcı, önceki etiket kümesinden PN'den yüksek etiketleri hemen silebilir. Alıcı, önceki etiket kümesinden PN'den küçük veya eşit etiketleri kısa bir süre sonra (örn. 2 dakika) geçersiz kılabilir.

```
+----+----+----+----+----+
| 6  |  size   |  PN    |
+----+----+----+----+----+

blk :: 6
size :: 2
PN :: 2 bytes big endian. The index of the last tag sent in the previous tag set.
```
Notlar:

- Maksimum PN 65535'tir.
- PN tanımı Signal tanımına eşittir, eksi bir.
  Bu Signal'in yaptığına benzer, ancak Signal'de PN ve N başlıkta yer alır. Burada ise şifrelenmiş mesaj gövdesinde bulunurlar.
- Bu bloğu tag set 0'da göndermeyin, çünkü önceki bir tag set yoktu.

#### Sonraki DH Ratchet Genel Anahtarı

Bir sonraki DH ratchet anahtarı payload içindedir ve isteğe bağlıdır. Her seferinde ratchet yapmıyoruz. (Bu, signal'den farklıdır; signal'de header içindedir ve her seferinde gönderilir)

İlk ratchet için, Key ID = 0.

NS veya NSR'de izin verilmez. Yalnızca Mevcut Oturum mesajlarında dahil edilir.

```
+----+----+----+----+----+----+----+----+
| 7  |  size   |flag|  key ID |         |
+----+----+----+----+----+----+         +
|                                       |
+                                       +
|     Next DH Ratchet Public Key        |
+                                       +
|                                       |
+                             +----+----+
|                             |
+----+----+----+----+----+----+

blk :: 7
size :: 3 or 35
flag :: 1 byte flags
        bit order: 76543210
        bit 0: 1 for key present, 0 for no key present
        bit 1: 1 for reverse key, 0 for forward key
        bit 2: 1 to request reverse key, 0 for no request
               only set if bit 1 is 0
        bits 7-2: Unused, set to 0 for future compatibility
key ID :: The key ID of this key. 2 bytes, big endian
          0 - 32767
Public Key :: The next X25519 public key, 32 bytes, little endian
              Only if bit 0 is 1
```
Notlar:

- Key ID, o etiket seti için kullanılan yerel anahtar için artan bir sayaçtır, 0'dan başlar.
- ID, anahtar değişmedikçe değişmemelidir.
- Kesinlikle gerekli olmayabilir, ancak hata ayıklama için yararlıdır.
  Signal bir key ID kullanmaz.
- Maksimum Key ID 32767'dir.
- Her iki yöndeki etiket setlerinin aynı anda ratcheting yaptığı nadir durumlarda, bir çerçeve iki Next Key bloğu içerecektir; biri forward key için, diğeri reverse key için.
- Key ve tag set ID numaraları ardışık olmalıdır.
- Ayrıntılar için yukarıdaki DH Ratchet bölümüne bakın.

#### Onay

Bu yalnızca bir ack istek bloğu alındığında gönderilir. Birden fazla mesajı onaylamak için birden fazla ack mevcut olabilir.

NS veya NSR'de izin verilmez. Yalnızca Mevcut Oturum mesajlarında bulunur.

```
+----+----+----+----+----+----+----+----+
| 8  |  size   |tagsetid |   N     |    |
+----+----+----+----+----+----+----+    +
|             more acks                 |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 8
size :: 4 * number of acks to follow, minimum 1 ack
for each ack:
tagsetid :: 2 bytes, big endian, from the message being acked
N :: 2 bytes, big endian, from the message being acked
```
Notlar:

- Tag seti ID'si ve N, onaylanan mesajı benzersiz şekilde tanımlar.
- Her yönde bir oturum için kullanılan ilk tag setlerinde, tag seti ID'si 0'dır.
- Hiçbir NextKey bloğu gönderilmemiştir, bu nedenle anahtar ID'leri yoktur.
- NextKey alışverişlerinden sonra kullanılan tüm tag setler için, tag seti numarası (1 + Alice'in anahtar ID'si + Bob'un anahtar ID'si)'dir.

#### Ack İsteği

In-band onay talep et. Garlic Clove içindeki out-of-band DeliveryStatus Mesajını değiştirmek için.

Açık bir onay istenirse, mevcut tagset ID'si ve mesaj numarası (N) bir onay bloğunda döndürülür.

NS veya NSR'de izin verilmez. Yalnızca Mevcut Oturum mesajlarında dahil edilir.

```
+----+----+----+----+
|  9 |  size   |flg |
+----+----+----+----+

blk :: 9
size :: 1
flg :: 1 byte flags
       bits 7-0: Unused, set to 0 for future compatibility
```
#### Doldurma

Tüm dolgu (padding) AEAD çerçeveleri içindedir. TODO AEAD içindeki dolgu kabaca müzakere edilen parametrelere uymalıdır. TODO Alice talep ettiği tx/rx min/max parametrelerini NS mesajında gönderdi. TODO Bob talep ettiği tx/rx min/max parametrelerini NSR mesajında gönderdi. Güncellenmiş seçenekler veri aşamasında gönderilebilir. Yukarıdaki seçenekler bloğu bilgisine bakın.

Eğer mevcutsa, bu çerçevedeki son blok olmalıdır.

```
+----+----+----+----+----+----+----+----+
|254 |  size   |      padding           |
+----+----+----+                        +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 254
size :: 2 bytes, big endian, 0-65516
padding :: zeros or random data
```
Notlar:

- Tamamen sıfır dolgulama uygun, çünkü şifrelenecek.
- Dolgu stratejileri henüz belirlenmedi.
- Sadece dolgu içeren çerçeveler izin veriliyor.
- Varsayılan dolgu 0-15 bayt.
- Dolgu parametresi müzakeresi için seçenekler bloğuna bakın
- Min/max dolgu parametreleri için seçenekler bloğuna bakın
- Router'ın müzakere edilmiş dolgu ihlali durumundaki tepkisi
  uygulamaya bağlıdır.

#### Diğer blok türleri

Uygulamalar, ileriye dönük uyumluluk için bilinmeyen blok türlerini görmezden gelmelidir.

#### Gelecekteki çalışmalar

- Padding uzunluğu ya mesaj bazında karar verilmeli ve uzunluk dağılımının tahminleri yapılmalı, ya da rastgele gecikmeler eklenmelidir. Bu karşı önlemler DPI'ye (Deep Packet Inspection - Derin Paket İnceleme) karşı direnç sağlamak için dahil edilmelidir, çünkü mesaj boyutları aksi takdirde I2P trafiğinin taşıma protokolü tarafından taşındığını açığa çıkaracaktır. Kesin padding şeması gelecekte yapılacak çalışmaların bir alanıdır, Ek A konuyla ilgili daha fazla bilgi sağlamaktadır.

## Tipik Kullanım Desenleri

### HTTP GET

Bu en tipik kullanım durumudur ve HTTP olmayan çoğu akış kullanım durumu da bu kullanım durumuyla aynı olacaktır. Küçük bir başlangıç mesajı gönderilir, bir yanıt gelir ve her iki yönde de ek mesajlar gönderilir.

Bir HTTP GET genellikle tek bir I2NP mesajına sığar. Alice tek bir yeni Session mesajı ile küçük bir istek gönderir ve bir yanıt leaseSet'i paketler. Alice yeni anahtara anında ratchet içerir. Hedefle bağlamak için imza içerir. Onay istenmez.

Bob hemen ratchet yapar.

Alice derhal ratchet yapar.

Bu oturumlarla devam eder.

```
Alice                           Bob

  New Session (1b)     ------------------->
  with ephemeral key 1
  with static key for binding
  with next key
  with bundled HTTP GET
  with bundled LS
  without bundled Delivery Status Message

  any retransmissions, same as above

  following messages may arrive in any order:

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 1
                      with bundled HTTP reply part 1

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 2
                      with bundled HTTP reply part 2

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 3
                      with bundled HTTP reply part 3

  After reception of any of these messages,
  Alice switches to use Existing Session messages,
  creates a new inbound + outbound session pair,
  and ratchets.


  Existing Session     ------------------->
  with bundled streaming ack


  Existing Session     ------------------->
  with bundled streaming ack


  After reception of any of these messages,
  Bob switches to use Existing Session messages.


  <--------------     Existing Session
                      with bundled HTTP reply part 4


  Existing Session     ------------------->
  with bundled streaming ack

  <--------------     Existing Session
                      with bundled HTTP reply part 5
```
### HTTP POST

Alice'in üç seçeneği var:

1)  HTTP GET'te olduğu gibi yalnızca ilk mesajı gönder (pencere boyutu = 1). Değil

    recommended.
2)  Streaming penceresine kadar gönder, ancak aynı Elligator2-encoded kullanarak

    cleartext public key. All messages contain same next public key
    (ratchet). This will be visible to OBGW/IBEP because they all start
    with the same cleartext. Things proceed as in 1). Not recommended.
3)  Önerilen uygulama. Streaming penceresi kadar gönder, ancak bir

    different Elligator2-encoded cleartext public key (session) for
    each. All messages contain same next public key (ratchet). This will
    not be visible to OBGW/IBEP because they all start with different
    cleartext. Bob must recognize that they all contain the same next
    public key, and respond to all with the same ratchet. Alice uses
    that next public key and continues.

Seçenek 3 mesaj akışı:

```
Alice                           Bob

  New Session (1b)     ------------------->
  with ephemeral key 1
  with static key for binding
  with bundled HTTP POST part 1
  with bundled LS
  without bundled Delivery Status Message


  New Session (1b)     ------------------->
  with ephemeral key 2
  with static key for binding
  with bundled HTTP POST part 2
  with bundled LS
  without bundled Delivery Status Message


  New Session (1b)     ------------------->
  with ephemeral key 3
  with static key for binding
  with bundled HTTP POST part 3
  with bundled LS
  without bundled Delivery Status Message


  following messages can arrive in any order:

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 1
                      with bundled streaming ack

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 2
                      with bundled streaming ack

  After reception of any of these messages,
  Alice switches to use Existing Session messages,
  creates a new inbound + outbound session pair,
  and ratchets.


  following messages can arrive in any order:


  Existing Session     ------------------->
  with bundled HTTP POST part 4

  Existing Session     ------------------->
  with next key
  with bundled HTTP POST part 5


  After reception of any of these messages,
  Bob switches to use Existing Session messages.


  <--------------     Existing Session
                      with bundled streaming ack

  After reception of any of this message,
  Alice switches to use Existing Session messages,
  and Alice ratchets.


  Existing Session     ------------------->
  with next key
  with bundled HTTP POST part 4

  after reception of this message, Bob ratchets

  Existing Session     ------------------->
  with next key
  with bundled HTTP POST part 5

  <--------------     Existing Session
                      with bundled streaming ack
```
### Yanıtlanabilir Datagram

Tek bir yanıt beklenen tek bir mesaj. Ek mesajlar veya yanıtlar gönderilebilir.

HTTP GET'e benzer, ancak oturum etiketi pencere boyutu ve yaşam süresi için daha küçük seçeneklerle. Belki de ratchet talep etmeyin.

```
Alice                           Bob

  New Session (1b)     ------------------->
  with static key for binding
  with next key
  with bundled repliable datagram
  with bundled LS
  without bundled Delivery Status Message


  <--------------     New Session Reply (1g)
                      with Bob ephemeral key
                      with bundled reply part 1

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key
                      with bundled reply part 2

  After reception of either message,
  Alice switches to use Existing Session messages,
  and ratchets.

  If the Existing Session message arrives first,
  Alice ratchets on the existing inbound and outbound
  sessions.

  When the New Session Reply arrives, Alice
  sets the existing inbound session to expire,
  creates a new inbound and outbound session,
  and sends Existing Session messages on
  the new outbound session.

  Alice keeps the expiring inbound session
  around for a while to process the Existing Session
  message sent to Alice.
  If all expected original Existing Session message replies
  have been processed, Alice can expire the original
  inbound session immediately.

  if there are any other messages:

  Existing Session     ------------------->
  with bundled message

  Existing Session     ------------------->
  with bundled streaming ack

  <--------------     Existing Session
                      with bundled message
```
### Çoklu Ham Veri Paketleri

Yanıt beklenmeden birden fazla anonim mesaj.

Bu senaryoda Alice bir oturum talep eder, ancak bağlama yapmadan. Yeni oturum mesajı gönderilir. Yanıt LS paketi dahil edilmez. Bir yanıt DSM paketi dahil edilir (bu, paketlenmiş DSM gerektiren tek kullanım durumudur). Sonraki anahtar dahil edilmez. Yanıt veya ratchet talep edilmez. Ratchet gönderilmez. Seçenekler oturum etiketleri penceresini sıfıra ayarlar.

```
Alice                           Bob

  New Session (1c)     ------------------->
  with bundled message
  without bundled LS
  with bundled Delivery Status Message 1

  New Session (1c)     ------------------->
  with bundled message
  without bundled LS
  with bundled Delivery Status Message 2

  New Session (1c)     ------------------->
  with bundled message
  without bundled LS
  with bundled Delivery Status Message 3
 
  following messages can arrive in any order:

  <--------------     Delivery Status Message 1

  <--------------     Delivery Status Message 2

  <--------------     Delivery Status Message 3

  After reception of any of these messages,
  Alice switches to use Existing Session messages.

  Existing Session     ------------------->

  Existing Session     ------------------->

  Existing Session     ------------------->
```
### Tekil Ham Datagram

Yanıt beklenmeden gönderilen tek bir anonim mesaj.

Tek seferlik mesaj gönderildi. Yanıt LS veya DSM paketlenmedi. Sonraki anahtar dahil edilmedi. Yanıt veya ratchet talep edilmedi. Ratchet gönderilmedi. Seçenekler oturum etiketleri penceresini sıfıra ayarladı.

```
Alice                           Bob

  One-Time Message (1d)   ------------------->
  with bundled message
  without bundled LS
  without bundled Delivery Status Message
```
### Uzun Süreli Oturumlar

Uzun süreli oturumlar, o andan itibaren ileri gizliliği korumak için herhangi bir zamanda ratchet yapabilir veya ratchet talep edebilir. Oturumlar, oturum başına gönderilen mesaj sınırına (65535) yaklaştıkça ratchet yapmak zorundadır.

## Uygulama Hususları

### Savunma

Mevcut ElGamal/AES+SessionTag protokolünde olduğu gibi, uygulamalar oturum etiketi depolamasını sınırlamalı ve bellek tüketme saldırılarına karşı korunmalıdır.

Önerilen bazı stratejiler şunlardır:

- Depolanan session tag sayısında katı sınır
- Bellek baskısı altındayken boştaki gelen oturumların agresif süre dolumu
- Tek bir uzak uç hedefe bağlı gelen oturum sayısında sınırlama
- Bellek baskısı altındayken session tag penceresinin uyarlanabilir azaltılması ve eski kullanılmayan tag'lerin silinmesi
- Bellek baskısı altındaysa istendiğinde ratchet işlemini reddetme

### Parametreler

Önerilen parametreler ve zaman aşımları:

- NSR tagset boyutu: 12 tsmin ve tsmax
- ES tagset 0 boyutu: tsmin 24, tsmax 160
- ES tagset (1+) boyutu: 160 tsmin ve tsmax
- NSR tagset zaman aşımı: alıcı için 3 dakika
- ES tagset zaman aşımı: gönderici için 8 dakika, alıcı için 10 dakika
- Önceki ES tagset'i kaldır: 3 dakika sonra
- Tag N için tagset önceden bakma: min(tsmax, tsmin + N/4)
- Tag N'nin arkasındaki tagset kırpma: min(tsmax, tsmin + N/4) / 2
- Sonraki anahtarı gönderme tag'i: 4096
- Tagset yaşam süresi sonrası sonraki anahtarı gönder: TBD
- Oturumu değiştir eğer NS alındıysa: 3 dakika sonra
- Maksimum saat sapması: -5 dakika ile +2 dakika
- NS tekrar filtreleme süresi: 5 dakika
- Dolgu boyutu: 0-15 bayt (diğer stratejiler TBD)

### Sınıflandırma

Gelen mesajları sınıflandırmak için aşağıdaki öneriler sunulmaktadır.

#### Yalnızca X25519

Yalnızca bu protokolle kullanılan bir tunnel üzerinde, şu anda ElGamal/AES+SessionTags ile yapıldığı gibi kimlik doğrulama yapın:

İlk olarak, başlangıç verisini bir session tag (oturum etiketi) olarak ele alın ve session tag'i arayın. Bulunursa, o session tag ile ilişkili saklanan veriyi kullanarak şifreleyin.

Bulunamazsa, başlangıç verisini DH public key ve nonce olarak ele alın. Bir DH işlemi ve belirtilen KDF gerçekleştirin, ve kalan veriyi şifre çözmeye çalışın.

#### X25519 ElGamal/AES+SessionTags ile Paylaşımlı

Hem bu protokolü hem de ElGamal/AES+SessionTags'i destekleyen bir tunnel'da, gelen mesajları şu şekilde sınıflandırın:

ElGamal/AES+SessionTags spesifikasyonundaki bir kusur nedeniyle, AES bloğu rastgele mod-16 olmayan bir uzunluğa doldurulmaz. Bu nedenle, Mevcut Oturum mesajlarının uzunluğu mod 16 her zaman 0'dır ve Yeni Oturum mesajlarının uzunluğu mod 16 her zaman 2'dir (çünkü ElGamal bloğu 514 bayt uzunluğundadır).

Uzunluk mod 16 değeri 0 veya 2 değilse, başlangıç verisini bir oturum etiketi olarak ele alın ve oturum etiketini arayın. Bulunursa, o oturum etiketiyle ilişkili saklanan veriyi kullanarak şifre çözme işlemi gerçekleştirin.

Bulunamazsa ve uzunluk mod 16'sı 0 veya 2 değilse, başlangıç verisini bir DH public key ve nonce olarak ele alın. Bir DH işlemi ve belirtilen KDF gerçekleştirin ve kalan veriyi şifrelemesini çözmeye çalışın. (göreli trafik karışımına ve X25519 ile ElGamal DH işlemlerinin göreli maliyetlerine dayanarak, bu adım bunun yerine en son yapılabilir)

Aksi takdirde, uzunluk mod 16 değeri 0 ise, başlangıç verilerini bir ElGamal/AES oturum etiketi olarak ele alın ve oturum etiketini arayın. Bulunursa, o oturum etiketiyle ilişkili saklanan verileri kullanarak şifreleyin.

Bulunamadığında ve veri en az 642 (514 + 128) bayt uzunluğundaysa ve uzunluk mod 16 değeri 2 ise, başlangıç verisini ElGamal bloğu olarak ele alın. Kalan veriyi şifresini çözmeye çalışın.

ElGamal/AES+SessionTag spesifikasyonunun mod-16 olmayan padding'e izin verecek şekilde güncellenmesi durumunda, işlerin farklı şekilde yapılması gerekecektir.

### Yeniden İletimler ve Durum Geçişleri

Ratchet katmanı yeniden iletim yapmaz ve iki istisna dışında, iletimler için zamanlayıcı kullanmaz. Zamanlayıcılar ayrıca tagset zaman aşımı için gereklidir.

İletim zamanlayıcıları yalnızca NSR göndermek ve alınan bir ES'de ACK isteği bulunduğunda ES ile yanıtlamak için kullanılır. Önerilen zaman aşımı süresi bir saniyedir. Hemen hemen tüm durumlarda, üst katman (datagram veya streaming) yanıt verecek, bir NSR veya ES'yi zorlayacak ve zamanlayıcı iptal edilebilecektir. Zamanlayıcı tetiklenirse, NSR veya ES ile boş bir payload gönderin.

#### Ratchet Katmanı Yanıtları

İlk uygulamalar üst katmanlarda çift yönlü trafiğe dayanmaktadır. Yani, uygulamalar karşı yönde trafiğin yakında iletileceğini varsayar ve bu durum ECIES katmanında gerekli herhangi bir yanıtı zorlar.

Ancak, belirli trafik tek yönlü veya çok düşük bant genişliğinde olabilir, bu durumda zamanında yanıt oluşturacak daha yüksek katman trafiği bulunmayabilir.

NS ve NSR mesajlarının alınması bir yanıt gerektirir; ACK Request ve Next Key bloklarının alınması da bir yanıt gerektirir.

Uygulamalar, yanıt gerektiren bu mesajlardan biri alındığında bir zamanlayıcı başlatmalı ve kısa bir süre içinde (örneğin 1 saniye) ters yönlü trafik gönderilmezse ECIES katmanında "boş" (Garlic Clove bloğu olmayan) bir yanıt oluşturmalıdır.

NS ve NSR mesajlarına yanıtlar için daha da kısa bir zaman aşımı uygulamak, trafiği mümkün olan en kısa sürede verimli ES mesajlarına kaydırmak için uygun olabilir.

#### NSR için NS Bağlama

Ratchet katmanında, Bob olarak, Alice yalnızca statik anahtar ile bilinir. NS mesajı doğrulanmıştır ([Noise](https://noiseprotocol.org/noise.html) IK gönderen doğrulaması 1). Ancak, ratchet katmanının Alice'e herhangi bir şey gönderebilmesi için bu yeterli değildir, çünkü ağ yönlendirmesi tam bir Destination gerektirir.

NSR gönderilebilmeden önce, Alice'in tam Destination'ı ya ratchet katmanı ya da daha üst katman yanıtlanabilir protokolü tarafından keşfedilmelidir; bu yanıtlanabilir [Datagrams](/docs/specs/datagrams/) veya [Streaming](/docs/specs/streaming/) olabilir. O Destination için Leaseset bulunduktan sonra, bu Leaseset NS'de bulunanla aynı statik anahtarı içerecektir.

Genellikle, üst katman yanıt verecek ve Alice'in Destination Hash'i ile Alice'in LeaseSet'inin network database aramasını zorlayacaktır. Bu LeaseSet neredeyse her zaman yerel olarak bulunacaktır, çünkü NS bir Garlic Clove bloğu içeriyordu ve bu blok Alice'in LeaseSet'ini içeren bir Database Store mesajı barındırıyordu.

Bob'un ratchet katmanı NSR göndermeye hazır olması ve bekleyen oturumu Alice'in Destination'ına bağlaması için, Bob NS payload'ını işlerken Destination'ı "yakalamalıdır". NS'teki statik anahtarla eşleşen bir anahtara sahip Leaseset içeren bir Database Store mesajı bulunursa, bekleyen oturum artık o Destination'a bağlanır ve Bob yanıt zamanlayıcısı sona ererse NSR'yi nereye göndereceğini bilir. Bu önerilen uygulamadır.

Alternatif bir tasarım, statik anahtarın bir Destination ile eşlendiği bir önbellek veya veritabanı tutmaktır. Bu yaklaşımın güvenliği ve pratikliği daha fazla çalışma gerektiren bir konudur.

Ne bu spesifikasyon ne de diğerleri her NS'nin Alice'in Leaseset'ini içermesini kesin olarak gerektirmez. Ancak pratikte içermelidir. Önerilen ES tagset gönderen zaman aşımı (8 dakika), maksimum Leaseset zaman aşımından (10 dakika) daha kısadır, bu nedenle önceki oturumun süresi dolmuş, Alice'in Bob'un hala geçerli Leaseset'ine sahip olduğunu düşünüp yeni NS ile yeni bir Leaseset göndermediği küçük bir zaman penceresi olabilir. Bu, daha fazla çalışma gerektiren bir konudur.

#### Çoklu NS Mesajları

Eğer üst katman (datagram veya streaming) daha fazla veri göndermeden önce NSR yanıtı alınmazsa, muhtemelen yeniden iletim olarak, Alice yeni bir geçici anahtar kullanarak yeni bir NS oluşturmalıdır. Önceki herhangi bir NS'den gelen geçici anahtarı yeniden kullanmayın. Alice, gönderilen herhangi bir NSR'ye yanıt olarak NSR mesajlarını almak için ek handshake durumunu ve türetilmiş alma tagset'ini korumalıdır.

Uygulamalar, gönderilen NS mesajlarının toplam sayısını veya NS mesajı gönderme hızını, üst katman mesajlarını gönderilmeden önce kuyruğa alarak veya düşürerek sınırlayabilir.

Belirli durumlarda, yüksek yük altında veya belirli saldırı senaryolarında, Bob'un kaynak tüketme saldırısından kaçınmak için şifre çözmeye çalışmadan NS mesajlarını sıraya alması, düşürmesi veya sınırlaması uygun olabilir.

Alınan her NS için Bob bir NSR giden tagset oluşturur, bir NSR gönderir, bir split() yapar ve gelen ve giden ES tagsetlerini oluşturur. Ancak Bob, ilgili gelen tagset üzerinde ilk ES mesajı alınana kadar herhangi bir ES mesajı göndermez. Bundan sonra Bob, alınan diğer NS'ler veya gönderilen NSR'ler için tüm handshake durumlarını ve tagsetleri atabilir veya kısa sürede sona ermelerine izin verebilir. ES mesajları için NSR tagsetlerini kullanmayın.

Bob'un NSR'den hemen sonra, Alice'tan ilk ES'i almadan önce bile spekülatif olarak ES mesajları göndermeyi seçip seçemeyeceği daha ileri araştırma gerektiren bir konudur. Belirli senaryolar ve trafik desenlerinde bu, önemli ölçüde bant genişliği ve CPU tasarrufu sağlayabilir. Bu strateji, trafik desenleri, ilk oturumun tagset'inde alınan ES'lerin yüzdesi veya diğer veriler gibi buluşsal yöntemlere dayalı olabilir.

#### Çoklu NSR Mesajları

Her alınan NS mesajı için, bir ES mesajı alınana kadar, Bob ya üst katman trafiği gönderilmesi ya da NSR gönderim zamanlayıcısının süresi dolması nedeniyle yeni bir NSR ile yanıt vermelidir.

Her NSR, gelen NS'ye karşılık gelen el sıkışma durumunu ve etiket setini kullanır. Bob, bir ES mesajı alınana kadar, alınan tüm NS mesajları için el sıkışma durumu ve etiket setini korumalıdır.

Uygulamalar, gönderilen NSR mesajlarının toplam sayısını veya NSR mesajı gönderme hızını, üst katman mesajlarını gönderilmeden önce kuyruğa alarak veya bırakarak sınırlayabilir. Bunlar, gelen NS mesajları veya ek üst katman giden trafik nedeniyle oluştuğunda sınırlanabilir.

Belirli durumlarda, yüksek yük altında veya belirli saldırı senaryolarında, Alice'in kaynak tükenme saldırısından kaçınmak için NSR mesajlarını deşifreye çalışmadan kuyruğa alması, düşürmesi veya sınırlaması uygun olabilir. Bu sınırlar tüm oturumlar genelinde toplam, oturum başına veya her ikisi birden olabilir.

Alice bir NSR aldığında, Alice ES oturum anahtarlarını türetmek için bir split() yapar. Alice bir zamanlayıcı ayarlamalı ve üst katman herhangi bir trafik göndermezse, genellikle bir saniye içinde boş bir ES mesajı göndermelidir.

Diğer gelen NSR etiket setleri yakında kaldırılabilir veya sürelerinin dolmasına izin verilebilir, ancak Alice alınan diğer NSR mesajlarını şifrelemek için bunları kısa bir süre saklamalıdır.

### Yeniden Oynatma Önleme

Bob, dahil edilen DateTime yakın zamanlı ise NS yeniden oynatma saldırılarını önlemek için bir Bloom filtresi veya başka bir mekanizma uygulamalı ve DateTime'ın çok eski olduğu NS mesajlarını reddetmelidir. Bob ayrıca şifre çözme işleminden önce yakın zamandaki yinelenen NS mesajlarını tespit etmek ve düşürmek için yinelenen geçici anahtar (Elligator2 kod çözme öncesi veya sonrası) için daha önceki bir yeniden oynatma tespit kontrolü kullanabilir.

NSR ve ES mesajları, session tag tek kullanımlık olduğu için doğal olarak tekrar oynatma korumasına sahiptir.

Garlic mesajları ayrıca router, I2NP mesaj kimliğine dayalı router genelinde Bloom filtresi uygularsa tekrar oynatma korumasına sahiptir.

## İlgili Değişiklikler

ECIES Hedeflerinden Veritabanı Aramaları: [Prop154](/proposals/154-ratchet/)'e bakın, şimdi 0.9.46 sürümü için [I2NP](/docs/specs/i2np/)'ye dahil edilmiştir.

Bu spesifikasyon, leaseSet ile birlikte X25519 genel anahtarını yayınlamak için LS2 desteği gerektirir. [I2NP](/docs/specs/i2np/) içindeki LS2 spesifikasyonlarında herhangi bir değişiklik gerekmez. Tüm destek, 0.9.38'de uygulanmış olan [Prop123](/proposals/123-new-netdb-entries/) içinde tasarlanmış, spesifiye edilmiş ve uygulanmıştır.

Bu spesifikasyon, etkinleştirilmesi için I2CP seçeneklerinde bir özelliğin ayarlanmasını gerektirir. Tüm destek, 0.9.38 sürümünde uygulanan [Prop123](/proposals/123-new-netdb-entries/) içinde tasarlanmış, belirtilmiş ve uygulanmıştır.

ECIES'i etkinleştirmek için gereken seçenek, I2CP, BOB, SAM veya i2ptunnel için tek bir I2CP özelliğidir.

Tipik değerler yalnızca ECIES için i2cp.leaseSetEncType=4 veya ECIES ve ElGamal ikili anahtarları için i2cp.leaseSetEncType=4,0'dır.

## Uyumluluk

Çift anahtar ile LS2'yi destekleyen herhangi bir router (0.9.38 veya daha yüksek) çift anahtarlı destinasyonlara bağlantıyı desteklemelidir.

Yalnızca ECIES hedefleri, şifrelenmiş arama yanıtları almak için floodfill'lerin çoğunluğunun 0.9.46 sürümüne güncellenmesini gerektirir. Bkz. [Prop154](/proposals/154-ratchet/).

ECIES-only hedefleri yalnızca ECIES-only olan veya dual-key olan diğer hedeflerle bağlantı kurabilir.

## Referanslar

- [Common](/docs/specs/common-structures/)
- [CRYPTO-ELG](/docs/specs/cryptography/#elgamal)
- [Datagrams](/docs/specs/datagrams/)
- [ECIES-HYBRID](/docs/specs/ecies-hybrid/)
- [ElG-AES](/docs/specs/elgamal-aes/)
- [Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf) - Ayrıca [Elligator makalesi](https://www.imperialviolet.org/2013/12/25/elligator.html) ve OBFS4 koduna bakın
- [GARLICSPEC](/docs/overview/garlic-routing/)
- [I2CP](/docs/specs/i2cp/)
- [I2NP](/docs/specs/i2np/)
- [NOISE](https://noiseprotocol.org/noise.html)
- [NTCP2](/docs/specs/ntcp2/)
- [Prop111](/proposals/111-ntcp2/)
- [Prop123](/proposals/123-new-netdb-entries/)
- [Prop142](/proposals/142-ecies-template/)
- [Prop144](/proposals/144-ecies-x25519/)
- [Prop145](/proposals/145-ecies-ecdh-aes/)
- [Prop152](/proposals/152-ecies-config/)
- [Prop153](/proposals/153-chacha20-layer/)
- [Prop154](/proposals/154-ratchet/)
- [RFC-2104](https://tools.ietf.org/html/rfc2104)
- [RFC-4880-S5.1](https://tools.ietf.org/html/rfc4880#section-5.1)
- [RFC-5869](https://tools.ietf.org/html/rfc5869)
- [RFC-7539](https://tools.ietf.org/html/rfc7539)
- [RFC-7748](https://tools.ietf.org/html/rfc7748)
- [RFC-7905](https://tools.ietf.org/html/rfc7905)
- [Signal](https://signal.org/docs/specifications/doubleratchet/)
- [SSU](/docs/transport/ssu/)
- [SSU2](/docs/specs/ssu2/)
- [STS](https://en.wikipedia.org/wiki/Station-to-Station_protocol) - Diffie, W.; van Oorschot P. C.; Wiener M. J., Kimlik Doğrulama ve Kimlik Doğrulamalı Anahtar Değişimi
- [Streaming](/docs/specs/streaming/)
