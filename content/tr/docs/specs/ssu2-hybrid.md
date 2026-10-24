---
title: "PQ Hibrit SSU2"
description: "ML-KEM kullanan SSU2 taşıma protokolünün kuantum sonrası hibrit varyantı"
slug: "ssu2-hybrid"
lastupdated: "2026-10"
category: "Aktarımlar"
accurateFor: "0.9.71"
---

### Durum

Beta Q2 2026, sürüm Q3 2026

## Genel Bakış

Bu, Teklif 169'da tasarlanan SSU2 aktarım protokolünün hibrit kuantum sonrası varyantıdır. Ek arka plan bilgisi için söz konusu teklife bakınız.

PQ Hybrid SSU2 yalnızca standart SSU2 ile aynı adres ve port üzerinde tanımlanır. Farklı bir portta veya standart SSU2 desteği olmadan çalıştırılmasına izin verilmez; standart SSU2'nin kullanımdan kaldırılacağı birkaç yıl boyunca da bu durum değişmeyecektir.

Bu belirtim, yalnızca standart SSU2'nin PQ Hybrid desteği için gerektirdiği değişiklikleri belgelemektedir. Temel uygulama ayrıntıları için SSU2 belirtimine bakınız.

## Tasarım

CRYSTALS-Kyber ve CRYSTALS-Dilithium'a (3.1, 3 ve daha eski sürümler) dayanan ancak bunlarla UYUMLU OLMAYAN NIST FIPS 203 ve 204 standartlarını [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) destekliyoruz.

### Anahtar Değişimi

PQ KEM yalnızca geçici (ephemeral) anahtarlar sağlar ve Noise XK ile IK gibi statik anahtar el sıkışmalarını (handshake) doğrudan desteklemez. Şifreleme türleri, PQ Hybrid Ratchet'te kullanılanlarla aynıdır ve [/docs/specs/common-structures/](/docs/specs/common-structures/) adresindeki ortak yapılar belgesinde tanımlanmıştır; [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)'te olduğu gibi, Hybrid türleri yalnızca X25519 ile birlikte tanımlanmaktadır.

Şifreleme türleri şunlardır:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">SSU2 Version</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
</tr>
</table>
### Geçerli Kombinasyonlar

Yeni şifreleme türleri RouterAddresses içinde belirtilir. Anahtar sertifikasındaki şifreleme türü 4. tür olmaya devam edecektir.

## Teknik Özellikler

### El Sıkışma Desenleri

El sıkışmalar (handshake), [Noise Protocol](https://noiseprotocol.org/noise.html) el sıkışma kalıplarını kullanır.

Aşağıdaki harf eşleştirmesi kullanılmaktadır:

- e = tek kullanımlık geçici anahtar
- s = statik anahtar
- p = mesaj yükü
- e1 = tek kullanımlık geçici PQ anahtarı, Alice'ten Bob'a gönderilir
- ekem1 = KEM şifreli metni, Bob'dan Alice'e gönderilir

XK ve IK için hibrit ileri gizlilik (hfs) kapsamındaki aşağıdaki değişiklikler, [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) belgesinin 5. bölümünde belirtildiği şekildedir:

```
XK:                       XKhfs:
  <- s                      <- s
  ...                       ...
  -> e, es, p               -> e, es, e1, p
  <- e, ee, p               <- e, ee, ekem1, p
  -> s, se                  -> s, se
  <- p                      <- p
  p ->                      p ->


  e1 and ekem1 are encrypted. See pattern definitions below.
  NOTE: e1 and ekem1 are different sizes (unlike X25519)
```
e1 deseni, [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) bölüm 4'te belirtildiği üzere aşağıdaki gibi tanımlanmaktadır:

```
For Alice:
  (encap_key, decap_key) = PQ_KEYGEN()

  // EncryptAndHash(encap_key)
  ciphertext = ENCRYPT(k, n, encap_key, ad)
  n++
  MixHash(ciphertext)

  For Bob:

  // DecryptAndHash(ciphertext)
  encap_key = DECRYPT(k, n, ciphertext, ad)
  n++
  MixHash(ciphertext)
```
ekem1 deseni, [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) bölüm 4'te belirtildiği üzere aşağıdaki şekilde tanımlanmaktadır:

```
For Bob:

  (kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

  // EncryptAndHash(kem_ciphertext)
  ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)
  MixHash(ciphertext)

  // MixKey
  MixKey(kem_shared_key)


  For Alice:

  // DecryptAndHash(ciphertext)
  kem_ciphertext = DECRYPT(k, n, ciphertext, ad)
  MixHash(ciphertext)

  // MixKey
  kem_shared_key = DECAPS(kem_ciphertext, decap_key)
  MixKey(kem_shared_key)
```
### Noise El Sıkışma KDF (Anahtar Türetme Fonksiyonu)

#### Genel Bakış

Hibrit el sıkışması (handshake), [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) belgesinde tanımlanmıştır. Alice'ten Bob'a gönderilen ilk mesaj, mesaj yükünden önce kapsülleme anahtarı olan e1'i içerir. Bu, ek bir statik anahtar olarak ele alınır; üzerinde EncryptAndHash() (Alice olarak) veya DecryptAndHash() (Bob olarak) çağrılır. Ardından mesaj yükü her zamanki gibi işlenir.

Bob'dan Alice'e gönderilen ikinci mesaj, mesaj yükünden önce ekem1 şifreli metnini içerir. Bu, ek bir statik anahtar olarak işlenir; bunun üzerinde (Bob olarak) EncryptAndHash() ya da (Alice olarak) DecryptAndHash() çağrılır. Ardından kem_shared_key hesaplanır ve MixKey(kem_shared_key) çağrılır. Sonrasında mesaj yükü normal şekilde işlenir.

#### Tanımlanmış ML-KEM İşlemleri

[FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)'te tanımlandığı şekilde kullanılan kriptografik yapı taşlarına karşılık gelen aşağıdaki fonksiyonları tanımlıyoruz.

(encap_key, decap_key) = PQ_KEYGEN()

    Alice creates the encapsulation and decapsulation keys
    The encapsulation key is sent in message 1.
    encap_key and decap_key sizes vary based on ML-KEM variant.

(ciphertext, kem_shared_key) = ENCAPS(encap_key)

    Bob calculates the ciphertext and shared key,
    using the ciphertext received in message 1.
    The ciphertext is sent in message 2.
    ciphertext size varies based on ML-KEM variant.
    The kem_shared_key is always 32 bytes.

kem_shared_key = DECAPS(ciphertext, decap_key)

    Alice calculates the shared key,
    using the ciphertext received in message 2.
    The kem_shared_key is always 32 bytes.

Hem encap_key hem de ciphertext'in, Noise el sıkışma mesajları 1 ve 2'deki ChaCha/Poly blokları içinde şifrelendiğini unutmayın. Bunlar, el sıkışma sürecinin bir parçası olarak çözümlenecektir.

kem_shared_key, MixHash() ile zincirleme anahtara karıştırılır. Ayrıntılar için aşağıya bakın.

#### Mesaj 1 için Alice KDF

'es' mesaj deseni sonrasında ve yük (payload) öncesinde şunları ekleyin:

```
This is the "e1" message pattern:
  (encap_key, decap_key) = PQ_KEYGEN()

  // EncryptAndHash(encap_key)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, encap_key, ad)
  n++

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)


  End of "e1" message pattern.

  NOTE: For the next section (payload for XK or static key for IK),
  the keydata and chain key remain the same,
  and n now equals 1 (instead of 0 for non-hybrid).
```
#### Mesaj 1 için Bob KDF

'es' mesaj deseni sonrasında ve yük (payload) öncesinde şunları ekleyin:

```
This is the "e1" message pattern:

  // DecryptAndHash(encap_key_section)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  encap_key = DECRYPT(k, n, encap_key_section, ad)
  n++

  // MixHash(encap_key_section)
  h = SHA256(h || encap_key_section)

  End of "e1" message pattern.

  NOTE: For the next section (payload for XK or static key for IK),
  the keydata and chain key remain the same,
  and n now equals 1 (instead of 0 for non-hybrid).
```
#### Mesaj 2 için Bob KDF

XK için: 'ee' mesaj deseni sonrasında ve yük (payload) öncesinde şunu ekleyin:

```
This is the "ekem1" message pattern:

  (kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

  // EncryptAndHash(kem_ciphertext)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)

  // MixKey(kem_shared_key)
  keydata = HKDF(chainKey, kem_shared_key, "", 64)
  chainKey = keydata[0:31]

  End of "ekem1" message pattern.

  // AEAD parameters for payload section
  ... as in standard SSU2 ...
  k = keydata[32:63]
  ...

```
#### Mesaj 2 için Alice KDF

'ee' mesaj deseninden sonra ekleyin:

```
This is the "ekem1" message pattern:

  // DecryptAndHash(kem_ciphertext_section)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  kem_ciphertext = DECRYPT(k, n, kem_ciphertext_section, ad)

  // MixHash(kem_ciphertext_section)
  h = SHA256(h || kem_ciphertext_section)

  // MixKey(kem_shared_key)
  kem_shared_key = DECAPS(kem_ciphertext, decap_key)
  keydata = HKDF(chainKey, kem_shared_key, "", 64)
  chainKey = keydata[0:31]

  End of "ekem1" message pattern.

  // AEAD parameters for payload section
  ... as in standard SSU2 ...
  k = keydata[32:63]
  ...

```
#### Mesaj 3 için KDF

unchanged

#### split() için KDF

unchanged

### El Sıkışma Ayrıntıları

#### Noise tanımlayıcıları

- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"

MLKEM-1024'ün SSU2 için DESTEKLENMEDIĞINI unutmayın; zira anahtarlar standart 1500 baytlık bir datagram içine sığamayacak kadar büyüktür.

#### Uzun Başlık

Uzun başlık 32 bayttır. Bir oturum oluşturulmadan önce, Token Request, SessionRequest, SessionCreated ve Retry için kullanılır. Ayrıca oturum dışı Peer Test ve Hole Punch mesajları için de kullanılır.

Aşağıdaki mesajlarda, MLKEM-512 veya MLKEM-768'i belirtmek için uzun başlıktaki ver (sürüm) alanını 3 veya 4 olarak ayarlayın.

- (0) Oturum İsteği
- (1) Oturum Oluşturuldu
- (9) Yeniden Deneme
- (10) Token İsteği
- (11) Delik Açma

Aşağıdaki mesajlarda, MLKEM-512 veya MLKEM-768 desteklense bile, uzun başlıktaki ver (version/sürüm) alanını her zamanki gibi 2 olarak ayarlayın. Uygulamalar, karşı taraf destekliyorsa değeri 3 veya 4 olarak da ayarlayabilir; ancak bu zorunlu değildir. Uygulamalar 2-4 arasındaki herhangi bir değeri kabul etmelidir.

- (7) Eş Testi (oturum dışı mesajlar 5-7)

Tartışma: Sürüm alanını 3 veya 4 olarak ayarlamak tüm mesaj türleri için kesinlikle gerekli olmayabilir; ancak bunu yapmak, desteklenmeyen post-kuantum bağlantıları için erken hata tespitine yardımcı olur. Token Request ve Retry mesajları (tür 9 ve 10), tutarlılık açısından 3/4 sürümlerine sahip olmalıdır. Hole Punch mesajları (tür 11) bu işlemi gerektirmeyebilir, ancak tekdüzelik için aynı kalıbı izleyeceğiz. Peer Test mesajları (tür 7) oturum dışıdır ve bir oturum başlatma niyetini göstermez.

- Relay İsteği
- Relay Yanıtı
- Relay Girişi
- Peer Testi

Başlık şifrelemesinden önce:

Başlık şifrelemesinden önce:

```

  +----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+

  Destination Connection ID :: 8 bytes, unsigned big endian integer

  Packet Number :: 4 bytes, unsigned big endian integer

  type :: The message type = 0, 1, 7, 9, 10, or 11

  ver :: The protocol version = 2, 3, or 4 for non-PQ, MLKEM512, MLKEM768

  id :: 1 byte, the network ID (currently 2, except for test networks)

  flag :: 1 byte, unused, set to 0 for future compatibility

  Source Connection ID :: 8 bytes, unsigned big endian integer

  Token :: 8 bytes, unsigned big endian integer

```
#### Kısa Başlık

unchanged

#### SessionRequest (Tür 0)

Değişiklikler: Mevcut SSU2, ChaCha bölümünde yalnızca blok verilerini içermektedir. ML-KEM ile ChaCha bölümü, şifrelenmiş PQ (post-kuantum) genel anahtarını da içerecektir.

Sahte Kimlik Koruması için KDF Değişikliği: Proposal 165 [Prop165]_'te dile getirilen sorunları farklı bir çözümle ele almak amacıyla, Session Request için KDF'yi değiştiriyoruz. Bu yalnızca PQ (post-kuantum) oturumları için geçerlidir. PQ olmayan oturumlar için KDF değişmeden kalmaktadır.

```

// End of KDF for initial chain key (unchanged)
  // Bob static key
  // MixHash(bpk)
  h = SHA256(h || bpk);

  // Start of KDF for session request
  // NEW for PQ only
  // bhash = Bob router hash (32 bytes)
  // MixHash(bhash)
  h = SHA256(h || bhash);

  // Rest of KDF for session request, unchanged, as in SSU2 spec
  // MixHash(header)
  h = SHA256(h || header)

  ...

```
Ham içerikler:

```
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 0-15, ChaCha20     |
  +  encrypted with Bob intro key         +
  |    See Header Encryption KDF          |
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 16-31, ChaCha20    |
  +  encrypted with Bob intro key n=0     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +       X, ChaCha20 encrypted           +
  |       with Bob intro key n=0          |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (MLKEM)     |
  +          (length varies)              +
  |  k defined in KDF for Session Request |
  +  n = 0                                +
  |  see KDF for associated data          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (payload)   |
  +          (length varies)              +
  |  k defined in KDF for Session Request |
  +  n = 1                                +
  |  see KDF for associated data          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
Şifrelenmemiş veri (Poly1305 kimlik doğrulama etiketi gösterilmemiştir):

```
  +----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                   X                   |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM encap_key            |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     Noise payload (block data)        |
  +          (length varies)              +
  |     see below for allowed blocks      |
  +----+----+----+----+----+----+----+----+
```
IP ek yükü dahil edilmeden boyutlar:

| Tür | Tür Kodu | X uzunluğu | Mesaj 1 uzunluğu | Mesaj 1 Şifreli uzunluğu | Mesaj 1 Çözülmüş uzunluğu | PQ anahtar uzunluğu | pl uzunluğu |
|------|-----------|-------|-----------|---------------|---------------|------------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 896+pl | 832+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1280+pl | 1216+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | n/a | çok büyük | | | | |
Not: Tür kodları yalnızca dahili kullanım içindir. Router'lar 4. tür olarak kalacak ve destek, router adreslerinde belirtilecektir.

MLKEM768_X25519 için minimum MTU: IPv4 için 1318 ve IPv6 için 1338. Aşağıya bakınız.

Değişiklikler: Mevcut SSU2 yalnızca tek bir ChaCha bölümünde yükü içerir. ML-KEM ile, yükten önce gelen ve şifrelenmiş KF şifre metnini içeren yeni bir ChaCha bölümü eklenecek.

#### SessionCreated (Tür 1)

Değişiklikler: Geçerli SSU2 yalnızca tek bir ChaCha bölümünde yük içerir. ML-KEM ile, yükten önce gelen ve şifrelenmiş KJ şifreli metnini içeren yeni bir ChaCha bölümü eklenecek.

Ham içerikler:

```
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 0-15, ChaCha20     |
  +  encrypted with Bob intro key and     +
  | derived key, see Header Encryption KDF|
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 16-31, ChaCha20    |
  +  encrypted with derived key n=0       +
  |  See Header Encryption KDF            |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +       Y, ChaCha20 encrypted           +
  |       with derived key n=0            |
  +              (32 bytes)               +
  |       See Header Encryption KDF       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 data (MLKEM)               |
  +   Encrypted and authenticated data    +
  |  length varies                        |
  +  k defined in KDF for Session Created +
  |  (before mixKey)                      |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 data (payload)             |
  +   Encrypted and authenticated data    +
  |  length varies                        |
  +  k defined in KDF for Session Created +
  |  (after mixKey)                       |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
Şifrelenmemiş veri (Poly1305 kimlik doğrulama etiketi gösterilmemiştir):

```
  +----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                  Y                    |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM Ciphertext           |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     Noise payload (block data)        |
  +          (length varies)              +
  |      see below for allowed blocks     |
  +----+----+----+----+----+----+----+----+
```
IP ek yükü dahil edilmeden boyutlar:

| Tür | Tür Kodu | Y uz | Msg 2 uz | Msg 2 Enc uz | Msg 2 Dec uz | PQ CT uz | pl uz |
|------|-----------|-------|-----------|---------------|---------------|-----------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 864+pl | 800+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1184+pl | 1120+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | n/a | çok büyük | | | | |
Not: Tür kodları yalnızca dahili kullanım içindir. Router'lar 4. tür olarak kalacak ve destek, router adreslerinde belirtilecektir.

MLKEM768_X25519 için minimum MTU: IPv4 için 1318 ve IPv6 için 1338. Aşağıya bakınız.

Maksimum boyut: Alice henüz Bob'ın RouterInfo'suna sahip değil ve yayınlanan MTU'sunu bilmiyor. Bu mesaj için aşağıdaki şekilde geçici bir MTU kullanın. MLKEM512_X25519 için, MTU olarak 1280 veya alınan SessionRequest boyutunun en büyüğünü kullanın. MLKEM768_X25519 için, MTU olarak (IPv4 için 1318 veya IPv6 için 1338) veya alınan SessionRequest boyutunun en büyüğünü kullanın. MLKEM şifre metni, MLKEM genel anahtarından daha küçük olduğu için SessionCreated yükü, SessionRequest yükünden daha küçüktür. Bu, SessionRequest'te çok az veya hiç doldurma olmasa bile, SessionCreated içinde çeşitli doldurma boyutları aralığına izin verir.

#### SessionConfirmed (Tip 2)

unchanged

#### Veri aşaması için KDF (Anahtar Türetme Fonksiyonu)

unchanged

#### Relay ve Eş Testi

Aşağıdaki bloklar sürüm alanları içermektedir. Bu alanlar, (PQ desteklemeyen Bob ile uyumluluk sağlamak amacıyla) sürüm 2 olarak kalacak ve PQ için sürüm 3/4'e geçmeyecektir.

* [CABFORUM](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/)
* [Choosing-Hash](https://kerkour.com/fast-secure-hash-function-sha256-sha512-sha3-blake3)
* [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/)
* [COMMON](/docs/specs/common-structures/)
* [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/)
* [ECIES](/docs/specs/ecies/)
* [FORUM](http://zzz.i2p/topics/3294)
* [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
* [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
* [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)
* [FIPS205](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.205.pdf)
* [MLDSA-OIDS](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/)
* [NIST-PQ](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards)
* [NIST-PQ-UPDATE](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf)
* [NIST-PQ-END](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf)
* [NIST-VECTORS](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values)
* [Noise](https://noiseprotocol.org/noise.html)
* [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf)
* [NSA-PQ](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF)
* [NTCP2](/docs/specs/ntcp2/)
* [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)
* [Prop165](/docs/proposals/165/)
* [PQ-WIREGUARD](https://eprint.iacr.org/2020/379.pdf)
* [RFC-2104](https://tools.ietf.org/html/rfc2104)
* [Rosenpass](https://rosenpass.eu/)
* [Rosenpass-Whitepaper](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf)
* [SSH-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-sshm-mlkem-hybrid-kex/)
* [SSU2](/docs/specs/ssu2/)
* [TLS-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-tls-hybrid-design/)

#### Yayınlanan Adresler

Her durumda, SSU2 transport adını her zamanki gibi kullanın. MLKEM-1024 desteklenmemektedir.

PQ olmayan, firewall arkasında olmayan ile aynı adres/port kullanılır. PQ varyantlarından biri veya her ikisi desteklenir. Router adresinde, MLKEM 512/768/her ikisini belirtmek için v=2 (her zamanki gibi) ve yeni pq=[3|4|3,4|4,3] parametresi yayımlanır. Aşağıda belirtilen minimum MTU değerinin altında MTU'ya sahip router'lar, "4" içeren bir "pq" parametresi yayımlamamalıdır. MLKEM-768 tercihini belirtmek için 4,3, MLKEM-512 tercihini belirtmek için 3,4 yayımlanır. Gerçek sürüm başlatıcıya bağlıdır ve tercih dikkate alınmayabilir. Aşağıda belirtilen minimum MTU değerinin altında MTU'ya sahip router'lar MLKEM768 kullanarak bağlanmamalıdır. Eski router'lar pq parametresini görmezden gelecek ve her zamanki gibi PQ olmayan şekilde bağlanacaktır.

PQ olmayan ile farklı adres/port veya yalnızca PQ, güvenlik duvarı olmayan desteklenmemektedir. Bu, PQ olmayan SSU2 devre dışı bırakılana kadar, yani birkaç yıl sonrasına kadar uygulanmayacaktır. PQ olmayan devre dışı bırakıldığında, bir veya her iki PQ varyantı desteklenir. Router adresinde, MLKEM 512/768/her ikisini belirtmek için v=[3|4|3,4|4,3] yayımlayın. Eski router'lar v parametresini kontrol edecek ve bu adresi desteklenmiyor olarak atlayacaktır.

Güvenlik duvarı arkasındaki adresler (IP yayınlanmaz): Router adresinde, v=2 yayınlanır (her zamanki gibi). pq parametresi, relay (aktarma) desteği sağlamak için güvenlik duvarı arkasındaki adreslerde MUTLAKA yayınlanmalıdır.

Alice, kendi router info'sunda PQ desteği ilan edip etmediğinden veya aynı varyantı ilan edip etmediğinden bağımsız olarak, Bob'un yayımladığı PQ varyantını kullanarak PQ destekli bir Bob'a bağlanabilir.

#### MTU

MLKEM768 kullanırken MTU sınırını aşmamaya dikkat edin. MLKEM768_X25519 için minimum MTU, IPv4'te 1318 ve IPv6'da 1338'dir (en az 10 baytlık bir DateTime ve Padding ya da RelayTagRequest bloğundan oluşan minimum yük varsayımıyla). SSU2 için genel minimum MTU 1280 olduğundan, tüm eşler MLKEM768 kullanamayabilir. Gerçek MTU, minimum değerin altındaysa —yerel olarak veya eş tarafından duyurulan değer için— MLKEM768'i yayımlamayın veya kullanmayın. 1. ya da 2. mesajın yerel veya uzak MTU'yu aşmasına yol açacak şekilde dolgu boyutu eklememesine özen gösterin.

## Genel Yük Analizi

### Anahtar Değişimi

Boyut artışı (bayt):

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Pubkey (Msg 1)</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Ciphertext (Msg 2)</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+816</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+784</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+1200</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+1104</td>
</tr>
</table>
## Güvenlik Analizi

NIST güvenlik kategorileri, [NIST sunumunun](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf) 10. slaytında özetlenmektedir. Ön kriterler: Hibrit protokoller için minimum NIST güvenlik kategorimiz 2, yalnızca PQ (Post-Quantum / kuantum sonrası şifreleme) kullanan protokoller için ise 3 olmalıdır.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Category</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">As Secure As</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES128</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">SHA256</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES192</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">SHA384</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES256</td>
</tr>
</table>
### El Sıkışmaları

Bunların hepsi hibrit protokollerdir. Uygulamalar MLKEM768'i tercih etmelidir; MLKEM512 yeterince güvenli değildir.

NIST güvenlik kategorileri [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf):

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Algorithm</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Security Category</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
</tr>
</table>
## Uygulama Notları

### Kütüphane Desteği

Bouncycastle, BoringSSL ve WolfSSL kütüphaneleri artık MLKEM ve MLDSA'yı desteklemektedir. OpenSSL desteği ise 8 Nisan 2025'te yayımlanacak olan 3.5 sürümünde yer alacaktır [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

### Gelen Trafik Tanımlama

Bunun hibrit bir bağlantı olduğunu belirtmek için oturum isteğindeki geçici anahtarın MSB'sini (key[31] & 0x80) ayarlarız. Bu, aynı port üzerinde hem standart NTCP hem de hibrit NTCP çalıştırmamıza olanak tanır. Gelen bağlantılar için yalnızca bir hibrit varyant desteklenir ve bu varyant router adresinde duyurulur. Örneğin, pq=3 veya pq=4.

## Router Uyumluluğu

### Taşıma Adları

Alice olarak, bir PQ bağlantısı için, gizleme işleminden önce X[31] |= 0x80 olarak ayarlayın. Bu, X'i geçersiz bir X25519 açık anahtarı haline getirir. Gizleme işleminden sonra AES-CBC onu rastgele hale getirecektir. Gizleme işleminin ardından X'in MSB'si (en yüksek değerli bit) rastgele olacaktır.

## Referanslar

* [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/)
* [COMMON](/docs/specs/common-structures/)
* [ECIES](/docs/specs/ecies/)
* [FORUM](http://zzz.i2p/topics/3294)
* [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
* [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
* [NIST-PQ](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards)
* [NIST-PQ-UPDATE](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf)
* [NIST-PQ-END](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf)
* [NIST-VECTORS](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values)
* [Noise](https://noiseprotocol.org/noise.html)
* [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf)
* [NSA-PQ](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF)
* [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)
* [Prop165](/docs/proposals/165/)
* [PQ-WIREGUARD](https://eprint.iacr.org/2020/379.pdf)
* [RFC-2104](https://tools.ietf.org/html/rfc2104)
* [Rosenpass](https://rosenpass.eu/)
* [Rosenpass-Whitepaper](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf)
* [SSH-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-sshm-mlkem-hybrid-kex/)
* [SSU2](/docs/specs/ssu2/)
* [TLS-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-tls-hybrid-design/)
