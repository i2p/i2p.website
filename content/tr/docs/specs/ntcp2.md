---
title: "NTCP2 Transport"
description: "Router'dan router'a bağlantılar için Noise tabanlı TCP taşıma protokolü"
slug: "ntcp2"
category: "Taşımalar"
lastUpdated: "2026-07"
accurateFor: "0.9.70"
---

## Genel Bakış

NTCP2, [NTCP](/docs/transport/ntcp)'nin çeşitli otomatik tanımlama ve saldırı türlerine karşı direncini artıran kimlik doğrulamalı anahtar anlaşma protokolüdür.

NTCP2 esneklik ve NTCP ile birlikte çalışabilirlik için tasarlanmıştır. NTCP ile aynı port üzerinde desteklenebilir, farklı bir port kullanabilir veya hiç eşzamanlı NTCP desteği olmadan çalışabilir. Detaylar için aşağıdaki Yayınlanan Router Bilgisi bölümüne bakınız.

Diğer I2P taşıma protokolleri gibi, NTCP2 de yalnızca I2NP mesajlarının noktadan noktaya (router'dan router'a) taşınması için tanımlanmıştır. Genel amaçlı bir veri kanalı değildir.

NTCP2, sürüm 0.9.36 itibariyle desteklenmektedir. Orijinal öneri, arka plan tartışması ve ek bilgiler dahil olmak üzere [Prop111](/proposals/111-ntcp-2)'e bakınız.

## Noise Protokol Çerçevesi

NTCP2, Noise Protocol Framework [NOISE](https://noiseprotocol.org/noise.html) (Revizyon 33, 2017-10-04) kullanır. Noise, [SSU](/docs/transport/ssu) protokolünün temelini oluşturan Station-To-Station protokolü [STS](#references) ile benzer özelliklere sahiptir. Noise terminolojisinde Alice başlatıcı, Bob ise yanıtlayıcıdır.

NTCP2, Noise_XK_25519_ChaChaPoly_SHA256 Noise protokolüne dayanmaktadır. (İlk anahtar türetme fonksiyonu için gerçek tanımlayıcı, I2P uzantılarını belirtmek için "Noise_XKaesobfse+hs2+hs3_25519_ChaChaPoly_SHA256"dır - aşağıdaki KDF 1 bölümüne bakınız) Bu Noise protokolü aşağıdaki temel öğeleri kullanır:

- Handshake Pattern: XK Alice anahtarını Bob'a iletir (X) Alice Bob'un statik anahtarını zaten bilir (K)
- DH Fonksiyonu: X25519 [RFC-7748](https://tools.ietf.org/html/rfc7748)'de belirtildiği gibi 32 bayt anahtar uzunluğuna sahip X25519 DH.
- Şifre Fonksiyonu: ChaChaPoly [RFC-7539](https://tools.ietf.org/html/rfc7539) bölüm 2.8'de belirtildiği gibi AEAD_CHACHA20_POLY1305. İlk 4 baytı sıfıra ayarlanmış 12 bayt nonce.
- Hash Fonksiyonu: SHA256 I2P'de zaten yaygın olarak kullanılan standart 32-bayt hash.

## Çerçeveye Eklentiler

NTCP2, Noise_XK_25519_ChaChaPoly_SHA256'ya aşağıdaki geliştirmeleri tanımlar. Bunlar genellikle [NOISE](https://noiseprotocol.org/noise.html) bölüm 13'teki yönergeleri takip eder.

1) Açık metin geçici anahtarlar bilinen bir anahtar ve IV kullanılarak AES şifreleme ile gizlenir. 2) Mesaj 1 ve 2'ye rastgele açık metin dolgu eklenir. Açık metin dolgu, handshake hash (MixHash) hesaplamasına dahil edilir. Mesaj 2 ve mesaj 3 bölüm 1 için aşağıdaki KDF bölümlerine bakın. Mesaj 3 ve veri aşaması mesajlarına rastgele AEAD dolgusu eklenir. 3) TCP üzerinde Noise için gerekli olduğu gibi ve obfs4'te olduğu gibi iki baytlık bir çerçeve uzunluğu alanı eklenir. Bu sadece veri aşaması mesajlarında kullanılır. Mesaj 1 ve 2 AEAD çerçeveleri sabit uzunluktadır. Mesaj 3 bölüm 1 AEAD çerçevesi sabit uzunluktadır. Mesaj 3 bölüm 2 AEAD çerçeve uzunluğu mesaj 1'de belirtilir. 4) İki baytlık çerçeve uzunluğu alanı obfs4'te olduğu gibi SipHash-2-4 ile gizlenir. 5) Mesaj 1,2,3 ve veri aşaması için payload formatı tanımlanır. Tabii ki bunlar framework'te tanımlanmaz.

## Mesajlar

Tüm NTCP2 mesajları 65537 bayt veya daha kısa uzunluktadır. Mesaj formatı, çerçeveleme ve ayırt edilemezlik için değişiklikler yapılmış Noise mesajlarına dayanmaktadır. Standart Noise kütüphanelerini kullanan uygulamaların, alınan mesajları Noise mesaj formatına/formatından ön işleme tabi tutması gerekebilir. Tüm şifrelenmiş alanlar AEAD şifreli metinleridir.

Kurulum sırası şu şekildedir:

```
Alice                           Bob

SessionRequest ------------------->
<------------------- SessionCreated
SessionConfirmed ----------------->
```
Noise terminolojisini kullanarak, kurulum ve veri dizisi şu şekildedir: (Payload Güvenlik Özellikleri [Noise](https://noiseprotocol.org/noise.html)'den )

```
XK(s, rs):           Authentication   Confidentiality
  <- s
  ...
  -> e, es                  0                2
  <- e, ee                  2                1
  -> s, se                  2                5
  <-                        2                5
```
Bir oturum kurulduktan sonra, Alice ve Bob Data mesajları alışverişi yapabilir.

Tüm mesaj türleri (SessionRequest, SessionCreated, SessionConfirmed, Data ve TimeSync) bu bölümde belirtilmiştir.

Bazı gösterimler:

    - RH_A = Router Hash for Alice (32 bytes)
    - RH_B = Router Hash for Bob (32 bytes)

### Kimlik Doğrulamalı Şifreleme

Üç ayrı kimlik doğrulamalı şifreleme örneği (CipherStates) vardır. Biri handshake aşamasında, ikisi ise (gönderme ve alma) veri aşamasında kullanılır. Her birinin KDF'den gelen kendi anahtarı vardır.

Şifrelenmiş/kimlik doğrulanmış veriler şu şekilde temsil edilecektir:

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|   Encrypted and authenticated data    |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
```
#### ChaCha20/Poly1305

Şifrelenmiş ve doğrulanmış veri formatı.

Şifreleme/şifre çözme fonksiyonlarına girdiler:

```
k :: 32 byte cipher key, as generated from KDF

nonce :: Counter-based nonce, 12 bytes.
         Starts at 0 and incremented for each message.
         First four bytes are always zero.
         Last eight bytes are the counter, little-endian encoded.
         Maximum value is 2**64 - 2.
         Connection must be dropped and restarted after
         it reaches that value.
         The value 2**64 - 1 must never be sent.

ad :: In handshake phase:
      Associated data, 32 bytes.
      The SHA256 hash of all preceding data.
      In data phase:
      Zero bytes

data :: Plaintext data, 0 or more bytes
```
Şifreleme fonksiyonunun çıktısı, şifre çözme fonksiyonunun girdisi:

```
+----+----+----+----+----+----+----+----+
|Obfs Len |                             |
+----+----+                             +
|       ChaCha20 encrypted data         |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+              (MAC)                    +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Obfs Len :: Length of (encrypted data + MAC) to follow, 16 - 65535
            Obfuscation using SipHash (see below)
            Not used in message 1 or 2, or message 3 part 1, where the length is fixed
            Not used in message 3 part 1, as the length is specified in message 1

encrypted data :: Same size as plaintext data, 0 - 65519 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
ChaCha20 için, burada açıklanan [RFC-7539](https://tools.ietf.org/html/rfc7539)'a karşılık gelir ve TLS [RFC-7905](https://tools.ietf.org/html/rfc7905)'te de benzer şekilde kullanılır.

#### Notlar

- ChaCha20 bir akım şifresi olduğundan, düz metinlerin doldurulması gerekmez. Ek anahtar akışı baytları atılır.
- Şifre için anahtar (256 bit) SHA256 KDF aracılığıyla üzerinde anlaşılır. Her mesaj için KDF'nin ayrıntıları aşağıdaki ayrı bölümlerdedir.
- 1, 2 ve 3. mesajın ilk kısmı için ChaChaPoly çerçeveleri bilinen boyuttadır. 3. mesajın ikinci kısmından başlayarak çerçeveler değişken boyuttadır. 3. mesaj kısım 1 boyutu 1. mesajda belirtilir. Veri aşamasından başlayarak, çerçevelerin önüne obfs4'teki gibi SipHash ile gizlenmiş iki baytlık uzunluk eklenir.
- Doldurma, 1 ve 2. mesajlar için doğrulanmış veri çerçevesinin dışındadır. Doldurma bir sonraki mesaj için KDF'de kullanılır, böylece kurcalama tespit edilir. 3. mesajdan başlayarak doldurma doğrulanmış veri çerçevesinin içindedir.

#### AEAD Hata İşleme

- Mesaj 1, 2 ve mesaj 3'ün 1. ve 2. kısımlarında, AEAD mesaj boyutu önceden bilinir. Bir AEAD kimlik doğrulama hatasında, alıcı daha fazla mesaj işlemeyi durdurmalı ve yanıt vermeden bağlantıyı kapatmalıdır. Bu anormal bir kapatma (TCP RST) olmalıdır.
- Yoklama direnci için, mesaj 1'de bir AEAD hatasından sonra, Bob rastgele bir zaman aşımı (aralık TBD) ayarlamalı ve ardından socket'i kapatmadan önce rastgele sayıda bayt (aralık TBD) okumalıdır. Bob, tekrarlanan hatalar yaşayan IP'lerin kara listesini tutmalıdır.
- Veri aşamasında, AEAD mesaj boyutu SipHash ile "şifrelenir" (gizlenir). Bir şifre çözme oracle'ı oluşturmaktan kaçınmak için dikkat edilmelidir. Bir veri aşaması AEAD kimlik doğrulama hatasında, alıcı rastgele bir zaman aşımı (aralık TBD) ayarlamalı ve ardından rastgele sayıda bayt (aralık TBD) okumalıdır. Okuma işleminden sonra veya okuma zaman aşımında, alıcı "AEAD hatası" neden kodunu içeren bir sonlandırma bloğu ile yük göndermelidir ve bağlantıyı kapatmalıdır.
- Veri aşamasında geçersiz bir uzunluk alanı değeri için de aynı hata eylemini gerçekleştirin.

### Anahtar Türetme Fonksiyonu (KDF) (handshake mesajı 1 için)

KDF, DH sonucundan bir handshake aşaması şifre anahtarı k üretir ve [RFC-2104](https://tools.ietf.org/html/rfc2104)'te tanımlandığı şekilde HMAC-SHA256(key, data) kullanır. Bunlar InitializeSymmetric(), MixHash(), ve MixKey() fonksiyonlarıdır ve tam olarak Noise spesifikasyonunda tanımlandığı gibidir.

```
This is the "e" message pattern:

// Define protocol_name.
Set protocol_name = "Noise_XKaesobfse+hs2+hs3_25519_ChaChaPoly_SHA256"
 (48 bytes, US-ASCII encoded, no NULL termination).

// Define Hash h = 32 bytes
h = SHA256(protocol_name);

Define ck = 32 byte chaining key. Copy the h data to ck.
Set ck = h

Define rs = Bob's 32-byte static key as published in the RouterInfo

// MixHash(null prologue)
h = SHA256(h);

// up until here, can all be precalculated by Alice for all outgoing connections

// Alice must validate that Bob's static key is a valid point on the curve here.

// Bob static key
// MixHash(rs)
// || below means append
h = SHA256(h || rs);

// up until here, can all be precalculated by Bob for all incoming connections

This is the "e" message pattern:

Alice generates her ephemeral DH key pair e.

// Alice ephemeral key X
// MixHash(e.pubkey)
// || below means append
h = SHA256(h || e.pubkey);

// h is used as the associated data for the AEAD in message 1
// Retain the Hash h for the message 2 KDF


End of "e" message pattern.

This is the "es" message pattern:

// DH(e, rs) == DH(s, re)
Define input_key_material = 32 byte DH result of Alice's ephemeral key and Bob's static key
Set input_key_material = X25519 DH result

// MixKey(DH())

Define temp_key = 32 bytes
Define HMAC-SHA256(key, data) as in [RFC-2104]_
// Generate a temp key from the chaining key and DH result
// ck is the chaining key, defined above
temp_key = HMAC-SHA256(ck, input_key_material)
// overwrite the DH result in memory, no longer needed
input_key_material = (all zeros)

// Output 1
// Set a new chaining key from the temp key
// byte() below means a single byte
ck =       HMAC-SHA256(temp_key, byte(0x01)).

// Output 2
// Generate the cipher key k
Define k = 32 bytes
// || below means append
// byte() below means a single byte
k =        HMAC-SHA256(temp_key, ck || byte(0x02)).
// overwrite the temp_key in memory, no longer needed
temp_key = (all zeros)

// retain the chaining key ck for message 2 KDF


End of "es" message pattern.
```
### 1) SessionRequest

Alice, Bob'a gönderir.

Noise içeriği: Alice'in geçici anahtarı X Noise yükü: 16 bayt seçenek bloğu Noise olmayan yük: Rastgele dolgu

(Payload Security Properties [Noise](https://noiseprotocol.org/noise.html)'dan)

```
XK(s, rs):           Authentication   Confidentiality
  -> e, es                  0                2

  Authentication: None (0).
  This payload may have been sent by any party, including an active attacker.

  Confidentiality: 2.
  Encryption to a known recipient, forward secrecy for sender compromise
  only, vulnerable to replay.  This payload is encrypted based only on DHs
  involving the recipient's static key pair.  If the recipient's static
  private key is compromised, even at a later date, this payload can be
  decrypted.  This message can also be replayed, since there's no ephemeral
  contribution from the recipient.

  "e": Alice generates a new ephemeral key pair and stores it in the e
       variable, writes the ephemeral public key as cleartext into the
       message buffer, and hashes the public key along with the old h to
       derive a new h.

  "es": A DH is performed between the Alice's ephemeral key pair and the
        Bob's static key pair.  The result is hashed along with the old ck to
        derive a new ck and k, and n is set to zero.
```
X değeri, gerekli DPI karşı önlemleri olan payload ayırt edilemezliği ve benzersizliği sağlamak için şifrelenir. Bunu başarmak için elligator2 gibi daha karmaşık ve yavaş alternatiflerin yerine AES şifreleme kullanırız. Bob'un router genel anahtarına asimetrik şifreleme çok yavaş olacaktır. AES şifreleme, Bob'un router hash'ini anahtar olarak ve network database'de yayınlanan Bob'un IV'sını kullanır.

AES şifreleme yalnızca DPI direnci içindir. Bob'un router hash'ini ve network veritabanında yayınlanan IV'yi bilen herhangi bir taraf, bu mesajdaki X değerini şifreleyebilir.

Dolgu Alice tarafından şifrelenmez. Zamanlama saldırılarını engellemek için Bob'un dolguyu şifrelemesi gerekebilir.

Ham içerikler:

```
+----+----+----+----+----+----+----+----+
|                                       |
+        obfuscated with RH_B           +
|       AES-CBC-256 encrypted X         |
+             (32 bytes)                +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|   ChaChaPoly encrypted data           |
+             (16 bytes)                +
|   k defined in KDF for message 1      |
+   n = 0                               +
|   see KDF for associated data         |
+----+----+----+----+----+----+----+----+
|                                       |
+        Poly1305 MAC (16 bytes)        +
|                                       |
+----+----+----+----+----+----+----+----+
|     unencrypted authenticated         |
~         padding (optional)            ~
|     length defined in options block   |
+----+----+----+----+----+----+----+----+

X :: 32 bytes, AES-256-CBC encrypted X25519 ephemeral key, little endian
        key: RH_B
        iv: As published in Bobs network database entry

padding :: Random data, 0 or more bytes.
           Total message length must be 65535 bytes or less.
           Total message length must be 287 bytes or less if
           Bob is publishing his address as NTCP
           (see Version Detection section below).
           Alice and Bob will use the padding data in the KDF for message 2.
           It is authenticated so that any tampering will cause the
           next message to fail.
```
Şifrelenmemiş veri (Poly1305 kimlik doğrulama etiketi gösterilmemiş):

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|                   X                   |
+              (32 bytes)               +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|               options                 |
+              (16 bytes)               +
|                                       |
+----+----+----+----+----+----+----+----+
|     unencrypted authenticated         |
+         padding (optional)            +
|     length defined in options block   |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

X :: 32 bytes, X25519 ephemeral key, little endian

options :: options block, 16 bytes, see below

padding :: Random data, 0 or more bytes.
           Total message length must be 65535 bytes or less.
           Total message length must be 287 bytes or less if
           Bob is publishing his address as "NTCP"
           (see Version Detection section below)
           Alice and Bob will use the padding data in the KDF for message 2.
           It is authenticated so that any tampering will cause the
           next message to fail.
```
Seçenekler bloğu: Not: Tüm alanlar big-endian formatındadır.

```
+----+----+----+----+----+----+----+----+
| id | ver|  padLen | m3p2len | Rsvd(0) |
+----+----+----+----+----+----+----+----+
|        tsA        |   Reserved (0)    |
+----+----+----+----+----+----+----+----+

id :: 1 byte, the network ID (currently 2, except for test networks)
      As of 0.9.42. See proposal 147.

ver :: 1 byte, protocol version (currently 2)

padLen :: 2 bytes, length of the padding, 0 or more
          See below for max guidelines. Random size from 0 to 64 bytes minimum is recommended.
          (Distribution is implementation-dependent)

m3p2Len :: 2 bytes, length of the the second AEAD frame in SessionConfirmed
           (message 3 part 2) See notes below

Rsvd :: 2 bytes, set to 0 for compatibility with future options

tsA :: 4 bytes, Unix timestamp, unsigned seconds.
       Wraps around in 2106

Reserved :: 4 bytes, set to 0 for compatibility with future options
```
#### Notlar

- Yayınlanan adres "NTCP" olduğunda, Bob aynı port üzerinde hem NTCP hem de NTCP2'yi destekler. Uyumluluk için, "NTCP" olarak yayınlanan bir adrese bağlantı başlatırken Alice bu mesajın boyutunu, padding dahil olmak üzere 287 bayt veya daha az ile sınırlandırmalıdır. Bu, Bob tarafından otomatik protokol tanımlamasını kolaylaştırır. "NTCP2" olarak yayınlandığında boyut kısıtlaması yoktur. Aşağıdaki Yayınlanan Adresler ve Sürüm Algılama bölümlerine bakın.

- İlk AES bloğundaki benzersiz X değeri, şifreli metnin her oturum için farklı olmasını sağlar.

- Bob, zaman damgası değeri mevcut zamandan çok fazla farklı olan bağlantıları reddetmelidir. Maksimum delta zamanını "D" olarak adlandırın. Bob, replay saldırılarını önlemek için daha önce kullanılmış handshake değerlerinin yerel bir önbelleğini tutmalı ve tekrarları reddetmelidir. Önbellekteki değerler en az 2*D ömre sahip olmalıdır. Önbellek değerleri implementasyona bağımlıdır, ancak 32-byte'lık X değeri (veya şifrelenmiş eşdeğeri) kullanılabilir.

- Diffie-Hellman geçici anahtarları kriptografik saldırıları önlemek için asla yeniden kullanılmamalıdır ve yeniden kullanım tekrar saldırısı olarak reddedilecektir.

- "KE" ve "auth" seçenekleri uyumlu olmalıdır, yani paylaşılan gizli anahtar K uygun boyutta olmalıdır. Daha fazla "auth" seçeneği eklenirse, bu "KE" bayrağının anlamını dolaylı olarak farklı bir KDF veya farklı bir kesme boyutu kullanacak şekilde değiştirebilir.

- Bob, Alice'in geçici anahtarının burada eğri üzerinde geçerli bir nokta olduğunu doğrulamalıdır.

- Padding makul bir miktarla sınırlandırılmalıdır. Bob aşırı padding içeren bağlantıları reddedebilir. Bob padding seçeneklerini mesaj 2'de belirtecektir. Min/max kılavuzları henüz belirlenmedi. Minimum 0 ila 31 bayt arası rastgele boyut? (Dağılım implementasyona bağlıdır) Java implementasyonları şu anda padding'i maksimum 256 baytla sınırlandırıyor.

- AEAD, DH, zaman damgası, görünür tekrar oynatma veya anahtar doğrulama hatası dahil olmak üzere herhangi bir hata durumunda, Bob daha fazla mesaj işlemeyi durdurmalı ve yanıt vermeden bağlantıyı kapatmalıdır. Bu anormal bir kapatma (TCP RST) olmalıdır. Sondajlama direnci için, bir AEAD hatasından sonra Bob rastgele bir zaman aşımı (aralık TBD) ayarlamalı ve ardından soketi kapatmadan önce rastgele sayıda bayt (aralık TBD) okumalıdır.

- Bob, şifre çözme işlemini denemeden önce geçerli bir anahtar için hızlı bir MSB kontrolü yapabilir (X[31] & 0x80 == 0). Yüksek bit ayarlanmışsa, AEAD hatalarında olduğu gibi araştırma direnci uygulayın.

- DoS Azaltımı: DH nispeten pahalı bir işlemdir. Önceki NTCP protokolünde olduğu gibi, router'lar CPU veya bağlantı tükenmesini önlemek için gerekli tüm önlemleri almalıdır. Maksimum aktif bağlantılar ve devam eden maksimum bağlantı kurulumları için sınırlar koyun. Okuma zaman aşımlarını uygulayın (hem okuma başına hem de "slowloris" için toplam). Aynı kaynaktan tekrarlanan veya eşzamanlı bağlantıları sınırlayın. Tekrar tekrar başarısız olan kaynaklar için kara listeler tutun. AEAD hatasına yanıt vermeyin.

- Hızlı sürüm algılama ve el sıkışmayı kolaylaştırmak için, uygulamalar Alice'in ilk mesajın tüm içeriğini dolgu dahil olmak üzere tamponlamasını ve ardından bir kerede boşaltmasını sağlamalıdır. Bu, verilerin tek bir TCP paketinde bulunma olasılığını artırır (işletim sistemi veya ara kutular tarafından bölümlenmediği sürece) ve Bob tarafından bir kerede alınmasını sağlar. Ek olarak, uygulamalar Bob'un ikinci mesajın tüm içeriğini dolgu dahil olmak üzere tamponlamasını ve ardından bir kerede boşaltmasını sağlamalıdır. ve Bob'un üçüncü mesajın tüm içeriğini bir kerede tamponlamasını ve boşaltmasını sağlamalıdır. Bu aynı zamanda verimlilik ve rastgele dolgunun etkinliğini sağlamak içindir.

- "ver" alanı: NTCP2'yi gösteren, payload spesifikasyonları da dahil olmak üzere genel Noise protokolü, uzantılar ve NTCP protokolü. Bu alan gelecekteki değişiklikler için desteği belirtmek amacıyla kullanılabilir.

- Mesaj 3 bölüm 2 uzunluğu: Bu, SessionConfirmed mesajında gönderilecek olan Alice'in Router Info'sunu ve isteğe bağlı padding'i içeren ikinci AEAD çerçevesinin boyutudur (16-bayt MAC dahil). Router'lar periyodik olarak Router Info'larını yeniden oluşturup yeniden yayınladıkları için, mevcut Router Info'nun boyutu mesaj 3 gönderilmeden önce değişebilir. Uygulamalar iki stratejiden birini seçmelidir:

a\) mesaj 3'te gönderilecek mevcut Router Info'yu kaydet, böylece boyut bilinir ve isteğe bağlı olarak padding için yer ekle;

b\) Router Info boyutunda olası artışa izin verecek kadar belirtilen boyutu artırın ve mesaj 3 gerçekten gönderildiğinde her zaman dolgu ekleyin. Her iki durumda da, mesaj 1'de yer alan "m3p2len" uzunluğu, mesaj 3'te gönderildiğinde o çerçevenin boyutuyla tam olarak aynı olmalıdır.

- Bob, mesaj 1'i doğruladıktan ve padding'i okuduktan sonra herhangi bir gelen veri kalırsa bağlantıyı başarısız kılmalıdır. Alice'ten ekstra veri olmamalıdır, çünkü Bob henüz mesaj 2 ile yanıt vermemiştir.

- Ağ kimliği alanı, çapraz ağ bağlantılarını hızla tanımlamak için kullanılır. Bu alan sıfır değilse ve Bob'un ağ kimliğiyle eşleşmiyorsa, Bob bağlantıyı kesip gelecekteki bağlantıları engellemeli. Test ağlarından gelen herhangi bir bağlantı farklı bir kimliğe sahip olacak ve testi geçemeyecek. 0.9.42 sürümü itibariyle. Daha fazla bilgi için 147 numaralı öneriye bakın.

- API 0.9.68'e kadar (sürüm 2.11.0), Java I2P, PQ olmayan bağlantılar için maksimum 256 bayt dolgu uyguladı, ancak bu daha önce belgelenmemişti.
  API 0.9.69 itibariyle (sürüm 2.12.0), Java I2P, PQ olmayan bağlantılar için MLKEM-512 ile aynı maksimum dolguyu uygular. Maksimum dolgu 880 bayttır.

### Anahtar Türetme Fonksiyonu (KDF) (handshake mesaj 2 ve mesaj 3 bölüm 1 için)

```
// take h saved from message 1 KDF
// MixHash(ciphertext)
h = SHA256(h || 32 byte encrypted payload from message 1)

// MixHash(padding)
// Only if padding length is nonzero
h = SHA256(h || random padding from message 1)

This is the "e" message pattern:

Bob generates his ephemeral DH key pair e.

// h is from KDF for handshake message 1
// Bob ephemeral key Y
// MixHash(e.pubkey)
// || below means append
h = SHA256(h || e.pubkey);

// h is used as the associated data for the AEAD in message 2
// Retain the Hash h for the message 3 KDF

End of "e" message pattern.

This is the "ee" message pattern:

// DH(e, re)
Define input_key_material = 32 byte DH result of Alice's ephemeral key and Bob's ephemeral key
Set input_key_material = X25519 DH result
// overwrite Alice's ephemeral key in memory, no longer needed
// Alice:
e(public and private) = (all zeros)
// Bob:
re = (all zeros)

// MixKey(DH())

Define temp_key = 32 bytes
Define HMAC-SHA256(key, data) as in [RFC-2104]_
// Generate a temp key from the chaining key and DH result
// ck is the chaining key, from the KDF for handshake message 1
temp_key = HMAC-SHA256(ck, input_key_material)
// overwrite the DH result in memory, no longer needed
input_key_material = (all zeros)

// Output 1
// Set a new chaining key from the temp key
// byte() below means a single byte
ck =       HMAC-SHA256(temp_key, byte(0x01)).

// Output 2
// Generate the cipher key k
Define k = 32 bytes
// || below means append
// byte() below means a single byte
k =        HMAC-SHA256(temp_key, ck || byte(0x02)).
// overwrite the temp_key in memory, no longer needed
temp_key = (all zeros)

// retain the chaining key ck for message 3 KDF

End of "ee" message pattern.
```
### 2) SessionCreated

Bob, Alice'e gönderir.

Noise içeriği: Bob'un geçici anahtarı Y Noise yükü: 16 bayt seçenek bloğu Noise-dışı yük: Rastgele dolgu

(Payload Güvenlik Özellikleri [Noise](https://noiseprotocol.org/noise.html)'dan)

```
XK(s, rs):           Authentication   Confidentiality
  <- e, ee                  2                1

  Authentication: 2.
  Sender authentication resistant to key-compromise impersonation (KCI).
  The sender authentication is based on an ephemeral-static DH ("es" or "se")
  between the sender's static key pair and the recipient's ephemeral key pair.
  Assuming the corresponding private keys are secure, this authentication cannot be forged.

  Confidentiality: 1.
  Encryption to an ephemeral recipient.
  This payload has forward secrecy, since encryption involves an ephemeral-ephemeral DH ("ee").
  However, the sender has not authenticated the recipient,
  so this payload might be sent to any party, including an active attacker.


  "e": Bob generates a new ephemeral key pair and stores it in the e variable,
  writes the ephemeral public key as cleartext into the message buffer,
  and hashes the public key along with the old h to derive a new h.

  "ee": A DH is performed between the Bob's ephemeral key pair and the Alice's ephemeral key pair.
  The result is hashed along with the old ck to derive a new ck and k, and n is set to zero.
```
Y değeri, gerekli DPI karşı önlemleri olan yük ayırt edilemezliği ve benzersizliği sağlamak için şifrelenir. Bunu başarmak için elligator2 gibi daha karmaşık ve yavaş alternatiflere kıyasla AES şifrelemesi kullanırız. Alice'in router genel anahtarına asimetrik şifreleme çok yavaş olurdu. AES şifrelemesi, anahtar olarak Bob'un router hash'ini ve mesaj 1'den gelen AES durumunu (network database'de yayınlanan Bob'un IV'siyle başlatılmıştı) kullanır.

AES şifrelemesi yalnızca DPI direnci içindir. Bob'un router hash'ini ve IV'sini (bunlar ağ veritabanında yayınlanır) bilen ve mesaj 1'in ilk 32 baytını yakalayan herhangi bir taraf, bu mesajdaki Y değerini şifreleyebilir.

Ham içerikler:

```
+----+----+----+----+----+----+----+----+
|                                       |
+        obfuscated with RH_B           +
|       AES-CBC-256 encrypted Y         |
+              (32 bytes)               +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|   ChaChaPoly encrypted data (options) |
+   16 bytes                            +
|   k defined in KDF for message 2      |
+   n = 0; see KDF for associated data  +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+        Poly1305 MAC (16 bytes)        +
|                                       |
+----+----+----+----+----+----+----+----+
|     unencrypted authenticated         |
+         padding (optional)            +
|     length defined in options block   |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

Y :: 32 bytes, AES-256-CBC encrypted X25519 ephemeral key, little endian
        key: RH_B
        iv: Using AES state from message 1
```
Şifrelenmemiş veri (Poly1305 kimlik doğrulama etiketi gösterilmemiş):

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|                  Y                    |
+              (32 bytes)               +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|               options                 |
+              (16 bytes)               +
|                                       |
+----+----+----+----+----+----+----+----+
|     unencrypted authenticated         |
+         padding (optional)            +
|     length defined in options block   |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

Y :: 32 bytes, X25519 ephemeral key, little endian

options :: options block, 16 bytes, see below

padding :: Random data, 0 or more bytes.
           Total message length must be 65535 bytes or less.
           Alice and Bob will use the padding data in the KDF for message 3 part 1.
           It is authenticated so that any tampering will cause the
           next message to fail.
```
#### Notlar

- Alice, Bob'un geçici anahtarının burada eğri üzerinde geçerli bir nokta olduğunu doğrulamalıdır.
- Dolgu makul bir miktarla sınırlandırılmalıdır. Alice aşırı dolguya sahip bağlantıları reddedebilir. Alice, dolgu seçeneklerini mesaj 3'te belirtecektir. Min/maks yönergeleri henüz belirlenmedi. 0 ila 31 bayt arasında minimum rastgele boyut? (Dağılım uygulamaya bağlıdır)
- AEAD, DH, zaman damgası, görünür tekrar saldırı veya anahtar doğrulama hatası dahil herhangi bir hatada, Alice daha fazla mesaj işlemeyi durdurmalı ve yanıt vermeden bağlantıyı kapatmalıdır. Bu anormal bir kapatma (TCP RST) olmalıdır.
- Hızlı el sıkışmayı kolaylaştırmak için, uygulamalar Bob'un dolgu dahil ilk mesajın tüm içeriğini arabelleğe aldığından ve ardından bir kerede boşalttığından emin olmalıdır. Bu, verilerin tek bir TCP paketinde yer alma olasılığını artırır (OS veya middlebox'lar tarafından segmentlenmediği sürece) ve Alice tarafından bir kerede alınmasını sağlar. Bu aynı zamanda verimlilik için ve rastgele dolgunun etkinliğini sağlamak içindir.
- Alice, mesaj 2'yi doğruladıktan ve dolguyu okuduktan sonra gelen herhangi bir veri kalırsa bağlantıyı başarısız kılmalıdır. Bob'tan ekstra veri olmamalıdır, çünkü Alice henüz mesaj 3 ile yanıt vermemiştir.

Seçenekler bloğu: Not: Tüm alanlar big-endian formatındadır.

```
+----+----+----+----+----+----+----+----+
| Rsvd(0) | padLen  |   Reserved (0)    |
+----+----+----+----+----+----+----+----+
|        tsB        |   Reserved (0)    |
+----+----+----+----+----+----+----+----+

Reserved :: 10 bytes total, set to 0 for compatibility with future options

padLen :: 2 bytes, big endian, length of the padding, 0 or more
          See below for max guidelines. Random size from 0 to 64 bytes minimum is recommended.
          (Distribution is implementation-dependent)

tsB :: 4 bytes, big endian, Unix timestamp, unsigned seconds.
       Wraps around in 2106
```
#### Notlar

- Alice, zaman damgası değeri mevcut zamandan çok uzak olan bağlantıları reddetmelidir. Maksimum delta zamanını "D" olarak adlandırın. Alice, tekrar saldırılarını önlemek için daha önce kullanılmış handshake değerlerinin yerel bir önbelleğini tutmalı ve duplikatları reddetmelidir. Önbellekteki değerlerin yaşam süresi en az 2*D olmalıdır. Önbellek değerleri uygulamaya bağlıdır, ancak 32-byte Y değeri (veya şifrelenmiş eşdeğeri) kullanılabilir.

- API 0.9.68'e kadar (sürüm 2.11.0), Java I2P PQ olmayan bağlantılar için maksimum 256 bayt padding uyguladı, ancak bu daha önce belgelenmemişti.
  API 0.9.69 itibariyle (sürüm 2.12.0), Java I2P PQ olmayan bağlantılar için MLKEM-512 ile aynı maksimum padding'i uygular. Maksimum padding 848 bayttır.

#### Sorunlar

- Minimum/maksimum dolgu seçenekleri buraya dahil edilsin mi?

### Handshake mesajı 3 bölüm 1 için şifreleme, mesaj 2 KDF kullanarak)

```
// take h saved from message 2 KDF
// MixHash(ciphertext)
h = SHA256(h || 24 byte encrypted payload from message 2)

// MixHash(padding)
// Only if padding length is nonzero
h = SHA256(h || random padding from message 2)
// h is used as the associated data for the AEAD in message 3 part 1, below

This is the "s" message pattern:

Define s = Alice's static public key, 32 bytes

// EncryptAndHash(s.publickey)
// EncryptWithAd(h, s.publickey)
// AEAD_ChaCha20_Poly1305(key, nonce, associatedData, data)
// k is from handshake message 1
// n is 1
ciphertext = AEAD_ChaCha20_Poly1305(k, n++, h, s.publickey)
// MixHash(ciphertext)
// || below means append
h = SHA256(h || ciphertext);

// h is used as the associated data for the AEAD in message 3 part 2

End of "s" message pattern.
```
### Anahtar Türetme Fonksiyonu (KDF) (handshake mesajı 3 bölüm 2 için)

```
This is the "se" message pattern:

// DH(s, re) == DH(e, rs)
Define input_key_material = 32 byte DH result of Alice's static key and Bob's ephemeral key
Set input_key_material = X25519 DH result
// overwrite Bob's ephemeral key in memory, no longer needed
// Alice:
re = (all zeros)
// Bob:
e(public and private) = (all zeros)

// MixKey(DH())

Define temp_key = 32 bytes
Define HMAC-SHA256(key, data) as in [RFC-2104]_
// Generate a temp key from the chaining key and DH result
// ck is the chaining key, from the KDF for handshake message 1
temp_key = HMAC-SHA256(ck, input_key_material)
// overwrite the DH result in memory, no longer needed
input_key_material = (all zeros)

// Output 1
// Set a new chaining key from the temp key
// byte() below means a single byte
ck =       HMAC-SHA256(temp_key, byte(0x01)).

// Output 2
// Generate the cipher key k
Define k = 32 bytes
// || below means append
// byte() below means a single byte
k =        HMAC-SHA256(temp_key, ck || byte(0x02)).

// h from message 3 part 1 is used as the associated data for the AEAD in message 3 part 2

// EncryptAndHash(payload)
// EncryptWithAd(h, payload)
// AEAD_ChaCha20_Poly1305(key, nonce, associatedData, data)
// n is 0
ciphertext = AEAD_ChaCha20_Poly1305(k, n++, h, payload)
// MixHash(ciphertext)
// || below means append
h = SHA256(h || ciphertext);

// retain the chaining key ck for the data phase KDF
// retain the hash h for the data phase Additional Symmetric Key (SipHash) KDF

End of "se" message pattern.

// overwrite the temp_key in memory, no longer needed
temp_key = (all zeros)
```
### 3) SessionConfirmed

Alice, Bob'a gönderir.

Noise içeriği: Alice'in statik anahtarı Noise yükü: Alice'in RouterInfo'su ve rastgele dolgu Non-noise yükü: yok

(Payload Security Properties [Noise](https://noiseprotocol.org/noise.html) kaynaklı)

```
XK(s, rs):           Authentication   Confidentiality
  -> s, se                  2                5

  Authentication: 2.
  Sender authentication resistant to key-compromise impersonation (KCI).  The
  sender authentication is based on an ephemeral-static DH ("es" or "se")
  between the sender's static key pair and the recipient's ephemeral key
  pair.  Assuming the corresponding private keys are secure, this
  authentication cannot be forged.

  Confidentiality: 5.
  Encryption to a known recipient, strong forward secrecy.  This payload is
  encrypted based on an ephemeral-ephemeral DH as well as an ephemeral-static
  DH with the recipient's static key pair.  Assuming the ephemeral private
  keys are secure, and the recipient is not being actively impersonated by an
  attacker that has stolen its static private key, this payload cannot be
  decrypted.

  "s": Alice writes her static public key from the s variable into the
  message buffer, encrypting it, and hashes the output along with the old h
  to derive a new h.

  "se": A DH is performed between the Alice's static key pair and the Bob's
  ephemeral key pair.  The result is hashed along with the old ck to derive a
  new ck and k, and n is set to zero.
```
Bu iki ChaChaPoly frame içerir. İlki Alice'in şifrelenmiş statik public key'idir. İkincisi Noise payload'udur: Alice'in şifrelenmiş RouterInfo'su, isteğe bağlı seçenekler ve isteğe bağlı dolgu. Aralarında MixKey() fonksiyonu çağrıldığı için farklı anahtarlar kullanırlar.

Ham içerik:

```
+----+----+----+----+----+----+----+----+
|                                       |
+   ChaCha20 encrypted data (32 bytes)  +
|   Alice static key S                  |
+     k defined in KDF for message 2    +
|   n = 1 see KDF for associated data   |
+----+----+----+----+----+----+----+----+
|                                       |
+        Poly1305 MAC (16 bytes)        +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+   ChaCha20 encrypted data             +
|     Length specified in message 1     |
+     (including 16 byte MAC to follow) +
|                                       |
+       Alice RouterInfo                +
|       using block format 2            |
+       Alice Options (optional)        +
|       using block format 1            |
+       Arbitrary padding               +
|       using block format 254          |
+                                       +
| k defined in KDF for message 3 part 2 |
+     n = 0                             +
|     see KDF for associated data       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+        Poly1305 MAC (16 bytes)        +
|                                       |
+----+----+----+----+----+----+----+----+

S :: 32 bytes, ChaChaPoly encrypted Alice's X25519 static key, little endian
     inside 48 byte ChaChaPoly frame
```
Şifrelenmemiş veri (Poly1305 kimlik doğrulama etiketleri gösterilmemiş):

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|              S                        |
+       Alice static key                +
|          (32 bytes)                   |
+                                       +
|                                       |
+                                       +
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|                                       |
+                                       +
|       Alice RouterInfo block          |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+       Optional Options block          +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+       Optional Padding block          +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

S :: 32 bytes, Alice's X25519 static key, little endian
```
#### Notlar

- Bob, olağan Router Info doğrulamasını gerçekleştirmeli. İmza türünün desteklendiğinden emin olun, imzayı doğrulayın, zaman damgasının sınırlar içinde olduğunu doğrulayın ve gerekli diğer kontrolleri yapın.

- Bob, ilk çerçevede alınan Alice'in statik anahtarının Router Info'daki statik anahtarla eşleştiğini doğrulamalıdır. Bob önce Router Info'da eşleşen sürüm (v) seçeneğine sahip bir NTCP veya NTCP2 Router Address aramalıdır. Aşağıdaki Yayınlanmış Router Info ve Yayınlanmamış Router Info bölümlerine bakın.

- Bob'un netdb'sinde Alice'in RouterInfo'sunun eski bir sürümü varsa, router info'daki statik anahtarın her ikisinde de aynı olduğunu doğrulayın (eğer mevcutsa) ve eski sürüm XXX'den daha eski değilse (aşağıdaki anahtar rotasyon zamanına bakın)

- Bob, Alice'in statik anahtarının burada eğri üzerinde geçerli bir nokta olduğunu doğrulamalıdır.

- Dolgu parametrelerini belirtmek için seçenekler dahil edilmelidir.

- AEAD, RI, DH, zaman damgası veya anahtar doğrulama hatası dahil herhangi bir hata durumunda, Bob daha fazla mesaj işlemeyi durdurmalı ve yanıt vermeden bağlantıyı kapatmalıdır. Bu anormal bir kapatma (TCP RST) olmalıdır.

- Hızlı el sıkışmayı kolaylaştırmak için, uygulamalar Alice'in üçüncü mesajın tüm içeriğini (her iki AEAD frame'ini de dahil olmak üzere) arabelleğe almasını ve ardından bir kerede temizlemesini sağlamalıdır. Bu, verilerin tek bir TCP paketinde bulunma olasılığını artırır (işletim sistemi veya middlebox'lar tarafından bölümlenmedikçe) ve Bob tarafından aynı anda alınmasını sağlar. Bu aynı zamanda verimlilik için ve rastgele padding'in etkinliğini sağlamak içindir.

- Mesaj 3 bölüm 2 çerçeve uzunluğu: Bu çerçevenin uzunluğu (MAC dahil) Alice tarafından mesaj 1'de gönderilir. Dolgu için yeterli alan bırakmayla ilgili önemli notlar için o mesaja bakın.

- Mesaj 3 bölüm 2 çerçeve içeriği: Bu çerçevenin formatı, çerçevenin uzunluğunun mesaj 1'de Alice tarafından gönderilmesi dışında veri fazı çerçevelerinin formatıyla aynıdır. Veri fazı çerçeve formatı için aşağıya bakınız. Çerçeve aşağıdaki sırada 1 ila 3 blok içermelidir:

1)  Alice'in Router Info bloğu (gerekli)   2)  Seçenekler bloğu (isteğe bağlı)

3\) Dolgu bloğu (isteğe bağlı) Bu çerçeve hiçbir zaman başka bir blok türü içermemelidir.

- Alice, mesaj 3'ün sonuna bir veri aşaması çerçevesi (isteğe bağlı olarak padding içeren) ekleyip her ikisini birden gönderirse, mesaj 3 bölüm 2 padding'i gerekli değildir, çünkü bir gözlemciye tek bir büyük bayt akışı gibi görünecektir. Alice genellikle (ama her zaman değil) Bob'a gönderecek bir I2NP mesajı olduğundan (bu yüzden ona bağlandı), bu uygulama hem verimlilik hem de rastgele padding'in etkinliğini sağlamak için önerilir.

- Mesaj 3 AEAD çerçevelerinin (1. ve 2. parçalar) teorik maksimum toplam uzunluğu 65535 bayttır; 1. parça 48 bayt olduğundan 2. parçanın maksimum çerçeve uzunluğu 65487'dir; MAC hariç 2. parçanın maksimum düz metin uzunluğu 65471'dir.
  UYARI: Bazı uygulamalar çok daha küçük uzunluklar zorunlu kılar. Java I2P şu anda toplam uzunluğu 4096 bayta sınırlar. Aşırı dolgu ekleme.

### Anahtar Türetme Fonksiyonu (KDF) (veri aşaması için)

Veri aşaması sıfır uzunluklu ilişkili veri girişi kullanır.

KDF, chaining key ck'dan iki şifre anahtarı k_ab ve k_ba üretir, [RFC-2104](https://tools.ietf.org/html/rfc2104)'te tanımlandığı gibi HMAC-SHA256(key, data) kullanarak. Bu, Noise spesifikasyonunda tanımlandığı gibi Split() fonksiyonudur.

```
ck = from handshake phase

// k_ab, k_ba = HKDF(ck, zerolen)
// ask_master = HKDF(ck, zerolen, info="ask")

// zerolen is a zero-length byte array
temp_key = HMAC-SHA256(ck, zerolen)
// overwrite the chaining key in memory, no longer needed
ck = (all zeros)

// Output 1
// cipher key, for Alice transmits to Bob (Noise doesn't make clear which is which, but Java code does)
k_ab =   HMAC-SHA256(temp_key, byte(0x01)).

// Output 2
// cipher key, for Bob transmits to Alice (Noise doesn't make clear which is which, but Java code does)
k_ba =   HMAC-SHA256(temp_key, k_ab || byte(0x02)).


KDF for SipHash for length field:
Generate an Additional Symmetric Key (ask) for SipHash
SipHash uses two 8-byte keys (big endian) and 8 byte IV for first data.

// "ask" is 3 bytes, US-ASCII, no null termination
ask_master = HMAC-SHA256(temp_key, "ask" || byte(0x01))
// sip_master = HKDF(ask_master, h || "siphash")
// "siphash" is 7 bytes, US-ASCII, no null termination
// overwrite previous temp_key in memory
// h is from KDF for message 3 part 2
temp_key = HMAC-SHA256(ask_master, h || "siphash")
// overwrite ask_master in memory, no longer needed
ask_master = (all zeros)
sip_master = HMAC-SHA256(temp_key, byte(0x01))

Alice to Bob SipHash k1, k2, IV:
// sipkeys_ab, sipkeys_ba = HKDF(sip_master, zerolen)
// overwrite previous temp_key in memory
temp_key = HMAC-SHA256(sip_master, zerolen)
// overwrite sip_master in memory, no longer needed
sip_master = (all zeros)

sipkeys_ab = HMAC-SHA256(temp_key, byte(0x01)).
sipk1_ab = sipkeys_ab[0:7], little endian
sipk2_ab = sipkeys_ab[8:15], little endian
sipiv_ab = sipkeys_ab[16:23]

Bob to Alice SipHash k1, k2, IV:

sipkeys_ba = HMAC-SHA256(temp_key, sipkeys_ab || byte(0x02)).
sipk1_ba = sipkeys_ba[0:7], little endian
sipk2_ba = sipkeys_ba[8:15], little endian
sipiv_ba = sipkeys_ba[16:23]

// overwrite the temp_key in memory, no longer needed
temp_key = (all zeros)
```
### 4) Veri Aşaması

Noise yükü: Aşağıda tanımlandığı gibi, rastgele dolgu dahil Noise olmayan yük: yok

Mesaj 3'ün 2. bölümünden başlayarak, tüm mesajlar önüne eklenmiş iki baytlık gizlenmiş uzunluğa sahip kimlik doğrulamalı ve şifrelenmiş ChaChaPoly "çerçevesi" içindedir. Tüm dolgu çerçeve içindedir. Çerçeve içinde sıfır veya daha fazla "blok" içeren standart bir format bulunur. Her blok bir baytlık tip ve iki baytlık uzunluğa sahiptir. Tipler tarih/saat, I2NP mesajı, seçenekler, sonlandırma ve dolguyu içerir.

Not: Bob, veri aşamasında Alice'e gönderdiği ilk mesaj olarak RouterInfo'sunu gönderebilir, ancak bunu yapmak zorunda değildir.

(Payload Güvenlik Özellikleri [Noise](https://noiseprotocol.org/noise.html)'dan)

```
XK(s, rs):           Authentication   Confidentiality
  <-                        2                5
  ->                        2                5

  Authentication: 2.
  Sender authentication resistant to key-compromise impersonation (KCI).
  The sender authentication is based on an ephemeral-static DH ("es" or "se")
  between the sender's static key pair and the recipient's ephemeral key pair.
  Assuming the corresponding private keys are secure, this authentication cannot be forged.

  Confidentiality: 5.
  Encryption to a known recipient, strong forward secrecy.
  This payload is encrypted based on an ephemeral-ephemeral DH as well as
  an ephemeral-static DH with the recipient's static key pair.
  Assuming the ephemeral private keys are secure, and the recipient is not being actively impersonated
  by an attacker that has stolen its static private key, this payload cannot be decrypted.
```
#### Notlar

- Verimlilik için ve uzunluk alanının tanımlanmasını en aza indirmek için, uygulamalar gönderenin veri mesajlarının tüm içeriğini uzunluk alanı ve AEAD çerçevesi dahil olmak üzere tampon belleğe aldığından ve ardından bir kerede boşalttığından emin olmalıdır. Bu, verinin tek bir TCP paketinde bulunma olasılığını artırır (işletim sistemi veya middlebox'lar tarafından bölümlenmedikçe) ve karşı tarafça bir kerede alınmasını sağlar. Bu aynı zamanda verimlilik içindir ve rastgele dolgunun etkinliğini sağlamak içindir.
- Router, AEAD hatasında oturumu sonlandırmayı seçebilir veya iletişim kurmaya devam etmeye çalışabilir. Devam ederse, router tekrarlanan hatalardan sonra sonlandırmalıdır.

#### SipHash gizlenmiş uzunluk

Referans: [SipHash](https://www.131002.net/siphash/)

Her iki taraf da handshake'i tamamladıktan sonra, ChaChaPoly "frame"lerinde şifrelenen ve doğrulanan payload'ları aktarırlar.

Her frame, big endian formatında iki baytlık bir uzunluk ile öncelenir. Bu uzunluk, MAC dahil olmak üzere takip edecek şifrelenmiş frame baytlarının sayısını belirtir. Stream'de tanımlanabilir uzunluk alanlarının iletilmesini önlemek için, frame uzunluğu, veri fazı KDF'sinden başlatıldığı şekliyle SipHash'ten türetilen bir mask ile XOR'lanarak gizlenir. İki yönün KDF'den benzersiz SipHash anahtarları ve IV'lere sahip olduğunu unutmayın.

```
    sipk1, sipk2 = The SipHash keys from the KDF.  (two 8-byte long integers)
    IV[0] = sipiv = The SipHash IV from the KDF. (8 bytes)
    length is big endian.
    For each frame:
      IV[n] = SipHash-2-4(sipk1, sipk2, IV[n-1])
      Mask[n] = First 2 bytes of IV[n]
      obfuscatedLength = length ^ Mask[n]

    The first length output will be XORed with with IV[1].
```
Alıcı, özdeş SipHash anahtarlarına ve IV'ye sahiptir. Uzunluğun çözümü, uzunluğu gizlemek için kullanılan maskeyi türeterek ve frame'in uzunluğunu elde etmek için kısaltılmış özet ile XOR işlemi yaparak gerçekleştirilir. Frame uzunluğu, MAC dahil olmak üzere şifrelenmiş frame'in toplam uzunluğudur.

#### Notlar

- Unsigned long integer döndüren bir SipHash kütüphane fonksiyonu kullanırsanız, en az anlamlı iki byte'ı Mask olarak kullanın. Long integer'ı little endian olarak sonraki IV'ye dönüştürün.

#### Ham içerik

```
+----+----+----+----+----+----+----+----+
|obf size |                             |
+----+----+                             +
|                                       |
+   ChaChaPoly frame                    +
|   Encrypted and authenticated         |
+   key is k_ab for Alice to Bob        +
|   key is k_ba for Bob to Alice        |
+   as defined in KDF for data phase    +
|   n starts at 0 and increments        |
+   for each frame in that direction    +
|   no associated data                  |
+   16 bytes minimum                    +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

obf size :: 2 bytes length obfuscated with SipHash
            when de-obfuscated: 16 - 65535

Minimum size including length field is 18 bytes.
Maximum size including length field is 65537 bytes.
Obfuscated length is 2 bytes.
Maximum ChaChaPoly frame is 65535 bytes.
```
#### Notlar

- Alıcının MAC'i kontrol etmek için tüm çerçeveyi alması gerektiğinden, gönderenin çerçeve boyutunu maksimuma çıkarmak yerine çerçeveleri birkaç KB ile sınırlandırması önerilir. Bu, alıcıdaki gecikmeyi en aza indirecektir.

#### Şifrelenmemiş veri

Şifrelenmiş çerçevede sıfır veya daha fazla blok bulunur. Her blok bir baytlık tanımlayıcı, iki baytlık uzunluk ve sıfır veya daha fazla veri baytı içerir.

Genişletilebilirlik için, alıcılar bilinmeyen tanımlayıcılara sahip blokları görmezden gelmeli ve bunları dolgu olarak ele almalıdır.

Şifreli veri maksimum 65535 bayt olup, 16 baytlık kimlik doğrulama başlığı dahildir, dolayısıyla maksimum şifrelenmemiş veri 65519 bayttır.

(Poly1305 auth etiketi gösterilmemiş):

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
       0 for datetime
       1 for options
       2 for RouterInfo
       3 for I2NP message
       4 for termination
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

Handshake mesajı 3 bölüm 2'de sıralama şöyle olmalıdır: RouterInfo, ardından varsa Options, ardından varsa Padding. Başka hiçbir bloğa izin verilmez.

Veri fazında sıra belirtilmemiştir, ancak aşağıdaki gereksinimler hariçtir: Dolgu (Padding) mevcut ise son blok olmalıdır. Sonlandırma (Termination) mevcut ise Dolgu hariç son blok olmalıdır.

Tek bir çerçevede birden fazla I2NP bloğu bulunabilir. Tek bir çerçevede birden fazla Padding bloğuna izin verilmez. Diğer blok türlerinin tek bir çerçevede birden fazla bloğu bulunması muhtemelen olmayacaktır, ancak yasaklanmamıştır.

#### TarihSaat

Zaman senkronizasyonu için özel durum:

```
+----+----+----+----+----+----+----+
| 0  |    4    |     timestamp     |
+----+----+----+----+----+----+----+

blk :: 0
size :: 2 bytes, big endian, value = 4
timestamp :: Unix timestamp, unsigned seconds.
             Wraps around in 2106
```
NOT: Uygulamalar ağdaki saat sapmasını önlemek için en yakın saniyeye yuvarlamalıdır.

#### Seçenekler

Güncellenmiş seçenekleri geçir. Seçenekler şunları içerir: Minimum ve maksimum dolgu.

Seçenekler bloğu değişken uzunlukta olacaktır.

```
+----+----+----+----+----+----+----+----+
| 1  |  size   |tmin|tmax|rmin|rmax|tdmy|
+----+----+----+----+----+----+----+----+
|tdmy|  rdmy   |  tdelay |  rdelay |    |
~----+----+----+----+----+----+----+    ~
|              more_options             |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 1
size :: 2 bytes, big endian, size of options to follow, 12 bytes minimum

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

Padding distribution specified as additional parameters?
Random delay specified as additional parameters?

more_options :: Format TBD
```
#### Seçenekler Sorunları

- Seçenekler formatı henüz belirlenmedi.
- Seçenek müzakeresi henüz belirlenmedi.

#### RouterInfo

Alice'in RouterInfo'sunu Bob'a ilet. Handshake mesajı 3 bölüm 2'de kullanılır. Alice'in RouterInfo'sunu Bob'a veya Bob'unkini Alice'e ilet. Veri aşamasında isteğe bağlı olarak kullanılır.

```
+----+----+----+----+----+----+----+----+
| 2  |  size   |flg |    RouterInfo     |
+----+----+----+----+                   +
| (Alice RI in handshake msg 3 part 2)  |
~ (Alice, Bob, or third-party           ~
|  RI in data phase)                    |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 2
size :: 2 bytes, big endian, size of flag + router info to follow
flg :: 1 byte flags
       bit order: 76543210
       bit 0: 0 for local store, 1 for flood request
       bits 7-1: Unused, set to 0 for future compatibility
routerinfo :: Alice's or Bob's RouterInfo
```
#### Notlar

- Veri aşamasında kullanıldığında, alıcı (Alice veya Bob) bunun başlangıçta gönderilen (Alice için) veya gönderildiği (Bob için) Router Hash ile aynı olduğunu doğrulamalıdır. Ardından, bunu yerel bir I2NP DatabaseStore Mesajı olarak ele alın. İmzayı doğrulayın, daha güncel zaman damgasını doğrulayın ve yerel netdb'de saklayın. Bayrak bit 0'ı 1 ise ve alıcı taraf floodfill ise, bunu sıfır olmayan yanıt token'ına sahip bir DatabaseStore Mesajı olarak ele alın ve en yakın floodfill'lere taşırın.
- Router Info gzip ile sıkıştırılmaz (DatabaseStore Mesajında olduğunun aksine, orada sıkıştırılır)
- RouterInfo'da yayınlanmış RouterAddress'ler olmadıkça taşıma talep edilmemelidir. Alıcı router, RouterInfo'da yayınlanmış RouterAddress'ler olmadıkça RouterInfo'yu taşımamalıdır.
- Uygulayıcılar, bir blok okunurken hatalı biçimlendirilmiş veya kötü niyetli verilerin okumaların bir sonraki bloğa taşmasına neden olmayacağından emin olmalıdır.
- Bu protokol RouterInfo'nun alındığına, saklandığına veya taşındığına dair bir onay sağlamaz (ne el sıkışma ne de veri aşamasında). Onay isteniyorsa ve alıcı floodfill ise, gönderen bunun yerine yanıt token'ı olan standart bir I2NP DatabaseStoreMessage göndermelidir.

#### Sorunlar

- Ayrıca veri fazında, I2NP DatabaseStoreMessage yerine de kullanılabilir. Örneğin, Bob bunu veri fazını başlatmak için kullanabilir.
- Bunun, floodfill'ler tarafından taşkın yapma gibi DatabaseStoreMessage'lar için genel bir değiştirici olarak, başlatan dışındaki router'lar için RI içermesine izin var mı?

#### I2NP Mesajı

Değiştirilmiş başlığa sahip tek bir I2NP mesajı. I2NP mesajları bloklar arasında veya ChaChaPoly çerçeveleri arasında parçalanmayabilir.

Bu, standart NTCP I2NP başlığından ilk 9 baytı kullanır ve başlığın son 7 baytını şu şekilde kaldırır: sona erme süresini 8 bayttan 4 bayta kısaltır (milisaniye yerine saniye, SSU ile aynı), 2 baytlık uzunluğu kaldırır (blok boyutu - 9 kullanır) ve tek baytlık SHA256 sağlama toplamını kaldırır.

```
+----+----+----+----+----+----+----+----+
| 3  |  size   |type|    msg id         |
+----+----+----+----+----+----+----+----+
|   short exp       |     message       |
+----+----+----+----+                   +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 3
size :: 2 bytes, big endian, size of type + msg id + exp + message to follow
        I2NP message body size is (size - 9).
type :: 1 byte, I2NP msg type, see I2NP spec
msg id :: 4 bytes, big endian, I2NP message ID
short exp :: 4 bytes, big endian, I2NP message expiration, Unix timestamp, unsigned seconds.
             Wraps around in 2106
message :: I2NP message body
```
#### Notlar

- Uygulayıcılar, bir blok okurken hatalı biçimlendirilmiş veya kötü niyetli verilerin okumaların bir sonraki bloğa taşmasına neden olmayacağını sağlamalıdır.

#### Sonlandırma

Noise açık bir sonlandırma mesajı önerir. Orijinal NTCP'de böyle bir mesaj yoktur. Bağlantıyı kes. Bu, çerçevedeki son dolgu olmayan blok olmalıdır.

```
+----+----+----+----+----+----+----+----+
| 4  |  size   |    valid data frames   |
+----+----+----+----+----+----+----+----+
    received   | rsn|     addl data     |
+----+----+----+----+                   +
~               .   .   .               ~
+----+----+----+----+----+----+----+----+

blk :: 4
size :: 2 bytes, big endian, value = 9 or more
valid data frames received :: The number of valid AEAD data phase frames received
                              (current receive nonce value)
                              0 if error occurs in handshake phase
                              8 bytes, big endian
rsn :: reason, 1 byte:
       0: normal close or unspecified
       1: termination received
       2: idle timeout
       3: router shutdown
       4: data phase AEAD failure
       5: incompatible options
       6: incompatible signature type
       7: clock skew
       8: padding violation
       9: AEAD framing error
       10: payload format error
       11: message 1 error
       12: message 2 error
       13: message 3 error
       14: intra-frame read timeout
       15: RI signature verification fail
       16: s parameter missing, invalid, or mismatched in RouterInfo
       17: banned
addl data :: optional, 0 or more bytes, for future expansion, debugging,
             or reason text.
             Format unspecified and may vary based on reason code.
```
#### Notlar

Tüm nedenler gerçekte kullanılmayabilir, implementasyona bağlıdır. Handshake hataları genellikle TCP RST ile kapatma sonucuna yol açar. Yukarıdaki handshake mesaj bölümlerindeki notlara bakın. Listelenen ek nedenler tutarlılık, loglama, hata ayıklama veya politika değişiklikleri içindir.

#### Doldurma

Bu, AEAD çerçeveleri içindeki dolgu için kullanılır. 1. ve 2. mesajlar için dolgular AEAD çerçevelerinin dışındadır. 3. mesaj ve veri aşaması için tüm dolgular AEAD çerçevelerinin içindedir.

AEAD içindeki padding kabaca müzakere edilen parametrelere uymalıdır. Bob istediği tx/rx min/max parametrelerini mesaj 2'de gönderdi. Alice istediği tx/rx min/max parametrelerini mesaj 3'te gönderdi. Güncellenmiş seçenekler veri fazı sırasında gönderilebilir. Yukarıdaki seçenekler blok bilgilerine bakın.

Varsa, bu çerçevedeki son blok olmalıdır.

```
+----+----+----+----+----+----+----+----+
|254 |  size   |      padding           |
+----+----+----+                        +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 254
size :: 2 bytes, big endian, size of padding to follow
padding :: random data
```
#### Notlar

- Boyut = 0'a izin verilir.
- Dolgu stratejileri henüz belirlenmedi.
- Minimum dolgu henüz belirlenmedi.
- Yalnızca dolgu içeren çerçevelere izin verilir.
- Dolgu varsayılanları henüz belirlenmedi.
- Dolgu parametresi müzakeresi için seçenekler bloğuna bakın
- Min/max dolgu parametreleri için seçenekler bloğuna bakın
- Noise mesajları 64KB ile sınırlar. Daha fazla dolguya ihtiyaç duyulursa, birden fazla çerçeve gönderin.
- Müzakere edilen dolgu ihlali durumunda router tepkisi uygulamaya bağlıdır.

#### Diğer blok türleri

Uygulamalar, ileri uyumluluk için bilinmeyen blok türlerini göz ardı etmelidir, ancak mesaj 3 bölüm 2'de bilinmeyen bloklara izin verilmez.

#### Gelecekteki çalışmalar

- Dolgu uzunluğu ya mesaj bazında kararlaştırılmalı ve uzunluk dağılımı tahminleri yapılmalı, ya da rastgele gecikmeler eklenmelidir. Bu karşı önlemler DPI'ye (Derin Paket İnceleme) karşı direnç sağlamak için dahil edilmelidir, çünkü mesaj boyutları aksi takdirde taşıma protokolü tarafından I2P trafiğinin taşındığını ortaya çıkarır. Kesin dolgu şeması gelecek çalışmaların bir alanıdır.

### 5) Sonlandırma

Bağlantılar normal veya anormal TCP soket kapanması yoluyla sonlandırılabilir, ya da Noise'un önerdiği gibi açık bir sonlandırma mesajı ile sonlandırılabilir. Açık sonlandırma mesajı yukarıdaki veri aşamasında tanımlanmıştır.

Herhangi bir normal veya anormal sonlandırma durumunda, router'lar bellekteki tüm geçici verileri sıfırlamalıdır; bu veriler arasında handshake geçici anahtarları, simetrik kripto anahtarları ve ilgili bilgiler bulunur.

## Yayınlanan Router Bilgisi

### Yetenekler

0.9.50 sürümünden itibaren, NTCP2 adreslerinde SSU'ya benzer şekilde "caps" seçeneği desteklenmektedir. "caps" seçeneğinde bir veya daha fazla yetenek yayınlanabilir. Yetenekler herhangi bir sırada olabilir, ancak uygulamalar arası tutarlılık için "46" sırası önerilir. Tanımlanmış iki yetenek vardır:

4: Giden IPv4 yeteneğini belirtir. Host alanında bir IP yayınlanmışsa, bu yetenek gerekli değildir. Router gizliyse veya NTCP2 yalnızca giden bağlantılarda kullanılıyorsa, '4' ve '6' tek bir adreste birleştirilebilir.

6: Giden IPv6 yeteneğini belirtir. Host alanında bir IP yayınlanmışsa, bu yetenek gerekli değildir. Router gizliyse veya NTCP2 yalnızca giden bağlantı için kullanılıyorsa, '4' ve '6' tek bir adreste birleştirilebilir.

### Yayınlanan Adresler

Yayınlanan RouterAddress (RouterInfo'nun bir parçası) "NTCP" veya "NTCP2" protokol tanımlayıcısına sahip olacaktır.

RouterAddress, mevcut NTCP protokolünde olduğu gibi "host" ve "port" seçeneklerini içermelidir.

RouterAddress, NTCP2 desteğini belirtmek için üç seçenek içermelidir:

- s=(Base64 anahtar) Bu RouterAddress için mevcut Noise statik genel anahtar (s). Standart I2P Base 64 alfabesi kullanılarak Base 64 kodlanmıştır. İkili formatta 32 bayt, Base 64 kodlu olarak 44 bayt, little-endian X25519 genel anahtarı.
- i=(Base64 IV) Bu RouterAddress için mesaj 1'deki X değerini şifrelemek için mevcut IV. Standart I2P Base 64 alfabesi kullanılarak Base 64 kodlanmıştır. İkili formatta 16 bayt, Base 64 kodlu olarak 24 bayt, big-endian.
- v=2 Mevcut sürüm (2). "NTCP" olarak yayınlandığında, sürüm 1 için ek destek ima edilir. Gelecek sürümler için destek virgülle ayrılmış değerlerle olacaktır, örn. v=2,3 Uygulama, virgül varsa birden fazla sürüm dahil olmak üzere uyumluluğu doğrulamalıdır. Virgülle ayrılmış sürümler sayısal sırada olmalıdır.

Alice, NTCP2 protokolünü kullanarak bağlanmadan önce üç seçeneğin de mevcut ve geçerli olduğunu doğrulamalıdır.

"s", "i" ve "v" seçenekleri ile "NTCP" olarak yayınlandığında, router hem NTCP hem de NTCP2 protokolleri için o host ve port üzerinde gelen bağlantıları kabul etmeli ve protokol sürümünü otomatik olarak algılamalıdır.

"s", "i" ve "v" seçenekleriyle "NTCP2" olarak yayınlandığında, router o host ve port üzerinde yalnızca NTCP2 protokolü için gelen bağlantıları kabul eder.

Bir router hem NTCP1 hem de NTCP2 bağlantılarını destekliyorsa ancak gelen bağlantılar için otomatik sürüm algılaması uygulamıyorsa, hem "NTCP" hem de "NTCP2" adreslerini tanıtmalı ve NTCP2 seçeneklerini yalnızca "NTCP2" adresine dahil etmelidir. Router, NTCP2'nin tercih edilmesi için "NTCP2" adresinde "NTCP" adresinden daha düşük bir maliyet değeri (daha yüksek öncelik) ayarlamalıdır.

Aynı RouterInfo içinde birden fazla NTCP2 RouterAddress yayınlanırsa (hem "NTCP" hem de "NTCP2" olarak, ek IP adresleri veya portlar için), aynı portu belirten tüm adresler özdeş NTCP2 seçenekleri ve değerleri içermelidir. Özellikle, tümü aynı statik anahtar ve iv içermelidir.

### Yayınlanmamış NTCP2 Adresi

Eğer Alice gelen bağlantılar için NTCP2 adresini ("NTCP" veya "NTCP2" olarak) yayınlamazsa, Bob'un mesaj 3 bölüm 2'de Alice'in RouterInfo'sunu aldıktan sonra anahtarı doğrulayabilmesi için yalnızca statik anahtarını ve NTCP2 sürümünü içeren bir "NTCP2" router adresi yayınlamalıdır.

- s=(Base64 anahtarı) Yayınlanan adresler için yukarıda tanımlandığı gibi.
- v=2 Yayınlanan adresler için yukarıda tanımlandığı gibi.

Bu router adresi "i", "host" veya "port" seçeneklerini içermeyecektir, çünkü giden NTCP2 bağlantıları için bunlar gerekli değildir. Bu adres için yayınlanan maliyet kesinlikle önemli değildir, çünkü yalnızca gelen bağlantılar içindir; ancak maliyetin diğer adreslerden daha yüksek (daha düşük öncelik) olarak ayarlanması diğer router'lar için faydalı olabilir. Önerilen değer 14'tür.

Alice ayrıca mevcut yayınlanmış "NTCP" adresine basitçe "s" ve "v" seçeneklerini ekleyebilir.

### Genel Anahtar ve IV Döndürme

RouterInfo'ların önbelleğe alınması nedeniyle, router'lar statik public key'i veya IV'yi router çalışır durumdayken değiştirmemelidir, ister yayınlanmış bir adreste olsun ister olmasın. Router'lar bu key ve IV'yi hemen yeniden başlatma sonrasında yeniden kullanım için kalıcı olarak saklamalıdır, böylece gelen bağlantılar çalışmaya devam eder ve yeniden başlatma süreleri açığa çıkmaz. Router'lar son kapanma zamanını kalıcı olarak saklamalı veya başka bir şekilde belirlemelidir, böylece önceki kesinti süresi başlangıçta hesaplanabilir.

Yeniden başlatma zamanlarının açığa çıkarılması endişeleri nedeniyle, router daha önce bir süre (en az birkaç saat) kapalı kalmışsa, router başlangıçta bu anahtarı veya IV'yi döndürebilir.

Router'ın yayınlanmış NTCP2 RouterAddress'leri varsa (NTCP veya NTCP2 olarak), rotasyon öncesi minimum kesinti süresi çok daha uzun olmalıdır, örneğin bir ay, yerel IP adresi değişmediği veya router "rekey" yapmadığı sürece.

Eğer router herhangi bir yayınlanmış SSU RouterAddress'e sahipse, ancak NTCP2'ye (NTCP veya NTCP2 olarak) sahip değilse, rotasyon öncesindeki minimum kesinti süresi daha uzun olmalıdır, örneğin bir gün, yerel IP adresi değişmedikçe veya router "yeniden anahtarlama" yapmadıkça. Bu, yayınlanan SSU adresinin introducer'lara sahip olduğu durumlarda bile geçerlidir.

Eğer router herhangi bir yayınlanmış RouterAddress'e (NTCP, NTCP2 veya SSU) sahip değilse, router "rekey" yapmadığı sürece IP adresi değişse bile rotasyondan önceki minimum kesinti süresi iki saat kadar kısa olabilir.

Eğer router farklı bir Router Hash'e "rekey" yaparsa, aynı zamanda yeni bir noise anahtarı ve IV de oluşturmalıdır.

Uygulamalar, statik genel anahtar veya IV değiştirilmesinin, eski bir RouterInfo önbelleğe almış olan routerlardan gelen NTCP2 bağlantılarını engelleyeceğinin farkında olmalıdır. RouterInfo yayınlama, tunnel eş seçimi (hem OBGW hem de IB en yakın hop dahil), sıfır-hop tunnel seçimi, transport seçimi ve diğer uygulama stratejileri bunu dikkate almalıdır.

IV rotasyonu, anahtar rotasyonu ile aynı kurallara tabidir, ancak IV'ler yalnızca yayınlanan RouterAddress'lerde bulunur, dolayısıyla gizli veya güvenlik duvarı arkasındaki router'lar için IV yoktur. Herhangi bir şey değişirse (sürüm, anahtar, seçenekler?) IV'nin de değişmesi önerilir.

Not: Yeniden anahtar üretimi öncesindeki minimum kesinti süresi, ağ sağlığını sağlamak ve orta düzeyde bir süre çevrimdışı kalan bir router'ın yeniden tohum almasını önlemek için değiştirilebilir.

## Sürüm Algılama

"NTCP" olarak yayınlandığında, router gelen bağlantılar için protokol sürümünü otomatik olarak tespit etmelidir.

Bu algılama uygulamaya bağlıdır, ancak burada bazı genel rehberlik bulunmaktadır.

Gelen bir NTCP bağlantısının sürümünü tespit etmek için Bob şu şekilde ilerler:

- En az 64 bayt bekle (minimum NTCP2 mesaj 1 boyutu)

- Eğer alınan ilk veri 288 veya daha fazla bayt ise, gelen bağlantı sürüm 1'dir.

- Eğer 288 bayttan azsa, ya

> - Daha fazla veri için kısa bir süre bekleyin (yaygın NTCP2 benimseniminden önce iyi bir strateji) toplam alınan 288 ise, bu NTCP 1.   >   > - Sürüm 2 olarak kod çözmenin ilk aşamalarını deneyin, başarısız olursa, daha fazla veri için kısa bir süre bekleyin (yaygın NTCP2 benimseniminden sonra iyi bir strateji)   >   >   > - SessionRequest paketinin ilk 32 baytını (X anahtarı) RH_B anahtarıyla AES-256 kullanarak şifreleyin.   >   > - Eğri üzerinde geçerli bir nokta doğrulayın. Başarısız olursa, NTCP 1 için daha fazla veri için kısa bir süre bekleyin   >   > - AEAD çerçevesini doğrulayın. Başarısız olursa, NTCP 1 için daha fazla veri için kısa bir süre bekleyin

NTCP 1 üzerinde aktif TCP segmentasyon saldırıları tespit edersek değişiklikler veya ek stratejiler önerebileceğimizi unutmayın.

Hızlı versiyon tespiti ve handshake işlemini kolaylaştırmak için, uygulamalar Alice'in ilk mesajın tüm içeriğini (padding dahil) önce tamponlayıp sonra bir seferde temizlemesini sağlamalıdır. Bu, verilerin tek bir TCP paketinde yer alma olasılığını artırır (işletim sistemi veya middlebox'lar tarafından bölünmedikçe) ve Bob tarafından aynı anda alınmasını sağlar. Bu aynı zamanda verimlilik için ve rastgele padding'in etkinliğini garanti altına almak içindir. Bu kural hem NTCP hem de NTCP2 handshake'leri için geçerlidir.

## Varyantlar, Yedekler ve Genel Sorunlar

- Alice ve Bob'un ikisi de NTCP2'yi destekliyorsa, Alice NTCP2 ile bağlanmalıdır.
- Alice herhangi bir nedenle NTCP2 kullanarak Bob'a bağlanamayı başaramazsa, bağlantı başarısız olur. Alice NTCP 1 kullanarak yeniden deneyemez.

## Saat Sapması Yönergeleri

Peer zaman damgaları ilk iki handshake mesajında, Session Request ve Session Created'da yer alır. İki peer arasında +/- 60 saniyeden büyük bir saat kayması genellikle öldürücüdür. Bob yerel saatinin kötü olduğunu düşünürse, hesaplanan kayma veya bazı harici kaynakları kullanarak saatini ayarlayabilir. Aksi takdirde, Bob maksimum kayma aşılsa bile bağlantıyı basitçe kapatmak yerine Session Created ile yanıtlamalıdır. Bu, Alice'in Bob'un zaman damgasını alıp kaymayı hesaplamasına ve gerekirse harekete geçmesine olanak tanır. Bob bu noktada Alice'in router kimliğine sahip değildir, ancak kaynakları korumak için Bob'un Alice'in IP'sinden gelen bağlantıları belirli bir süre boyunca veya aşırı kayma ile tekrarlanan bağlantı girişimlerinden sonra engellemesi arzu edilebilir.

Alice, hesaplanan saat kaymasını RTT'nin yarısını çıkararak ayarlamalıdır. Alice yerel saatinin kötü olduğunu düşünüyorsa, hesaplanan kaymayı veya harici bir kaynağı kullanarak saatini ayarlayabilir. Alice, Bob'un saatinin kötü olduğunu düşünüyorsa, Bob'u belirli bir süre yasaklayabilir. Her iki durumda da Alice bağlantıyı kapatmalıdır.

Eğer Alice Session Confirmed ile yanıtlarsa (muhtemelen çarpıklık 60s sınırına çok yakın olduğu için ve Alice ile Bob hesaplamaları RTT nedeniyle tam olarak aynı olmadığı için), Bob hesaplanan saat çarpıklığını RTT'nin yarısını çıkararak ayarlamalıdır. Ayarlanmış saat çarpıklığı maksimum değeri aşarsa, Bob bu durumda saat çarpıklığı neden kodu içeren bir Disconnect mesajı ile yanıtlamalı ve bağlantıyı kapatmalıdır. Bu noktada, Bob Alice'in router kimliğine sahiptir ve Alice'i belirli bir süre için yasaklayabilir.

## Referanslar

- [Ortak Yapılar](/docs/specs/common-structures)
- [I2NP](/docs/specs/i2np)
- [Network Database](/docs/overview/network-database)
- [NOISE - Noise Protocol Framework](https://noiseprotocol.org/noise.html)
- [NTCP](/docs/transport/ntcp)
- [Prop104](/proposals/104-tls-transport)
- [Prop109](/proposals/109-pt-transport)
- [Prop111](/proposals/111-ntcp-2)
- [RFC-2104 - HMAC](https://tools.ietf.org/html/rfc2104)
- [RFC-3526 - DH Groups](https://tools.ietf.org/html/rfc3526)
- [RFC-6151](https://tools.ietf.org/html/rfc6151)
- [RFC-7539 - ChaCha20-Poly1305](https://tools.ietf.org/html/rfc7539)
- [RFC-7748 - X25519](https://tools.ietf.org/html/rfc7748)
- [RFC-7905](https://tools.ietf.org/html/rfc7905)
- [SipHash](https://www.131002.net/siphash/)
- [SSU](/docs/transport/ssu)
- **[STS]** Diffie, W.; van Oorschot P. C.; Wiener M. J., Kimlik Doğrulama ve Doğrulanmış Anahtar Değişimleri
