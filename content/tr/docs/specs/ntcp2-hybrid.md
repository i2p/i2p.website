---
title: "PQ Hibrit NTCP2"
description: "ML-KEM kullanan NTCP2 taşıma protokolünün kuantum sonrası hibrit varyantı"
slug: "ntcp2-hybrid"
lastupdated: "2026-10"
category: "Ulaşım Yöntemleri"
accurateFor: "0.9.71"
---

### Durum

Beta Q1 2026, yayın Q2 2026

## Genel Bakış

Bu, Proposal 169'da tasarlanan NTCP2 taşıma protokolünün kuantum sonrası hibrit varyantıdır. Ek bilgi için o teklife bakınız.

PQ Hibrit NTCP2, yalnızca standart NTCP2 ile aynı adres ve port üzerinde tanımlıdır. Farklı bir port üzerinde veya standart NTCP2 desteğinin olmadığı durumlarda çalışma izin verilmez ve standart NTCP2 kullanım dışı bırakılana kadar birkaç yıl boyunca bu şekilde kalacaktır.

Bu belge, standart NTCP2'yi PQ Hibrit'i destekleyecek şekilde güncellemek için gereken değişiklikleri dokumente eder. Temel uygulama ayrıntıları için NTCP2 belgesine bakın.

## Tasarım

CRYSTALS-Kyber ve CRYSTALS-Dilithium (3.1, 3 ve daha eski sürümler) temeline dayanan ancak bunlarla UYUMLU OLMAYAN [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) ve [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) standartlarını destekliyoruz.

### Anahtar Değişimi

PQ KEM yalnızca geçici anahtarlar sağlar ve Noise XK ve IK gibi statik anahtarlı el sıkışmalarını doğrudan desteklemez. Şifreleme türleri, PQ Hibrit Ratchet'te kullanılanlarla aynıdır ve ortak yapılar belgesinde [/docs/specs/common-structures/](/docs/specs/common-structures/), [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) gibi tanımlanmıştır. Hibrit türler yalnızca X25519 ile birlikte tanımlanmıştır.

Şifreleme türleri şunlardır:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NTCP2 Version</th>
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
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
</tr>
</table>
### Geçerli Kombinasyonlar

Yeni şifreleme türleri RouterAddresses'te belirtilir. Anahtar sertifikasındaki şifreleme türü 4 türü olarak kalır.

## Teknik Özellikler

### El Sıkışma Desenleri

El sıkışmalar [Noise Protocol](https://noiseprotocol.org/noise.html) el sıkışma desenlerini kullanır.

Aşağıdaki harf eşlemesi kullanılır:

- e = tek kullanımlık geçici anahtar
- s = sabit anahtar
- p = mesaj yükü
- e1 = Alice'den Bob'a gönderilen tek kullanımlık geçici PQ anahtarı
- ekem1 = Bob'dan Alice'e gönderilen KEM şifreli metni

Hibrit ileri gizlilik (hfs) için XK ve IK'ya aşağıdaki değişiklikler [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) belgesinin 5. bölümünde belirtildiği gibidir:

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
e1 deseninin tanımı, [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) belgesinin 4. bölümünde belirtildiği gibi aşağıdaki gibidir:

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
ekem1 deseninin tanımı, [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) bölüm 4'te belirtildiği gibi aşağıdaki gibidir:

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
### Gürültü El Sıkışma KDF

#### Genel Bakış

Hibrit el sıkışma, [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) içinde tanımlanmıştır. Alice'den Bob'a giden ilk mesaj, mesaj yükünden önce e1, yani kapsülleme anahtarını içerir. Bu, ek bir statik anahtar olarak kabul edilir; onunla birlikte EncryptAndHash() fonksiyonunu (Alice olarak) veya DecryptAndHash() fonksiyonunu (Bob olarak) çağırın. Ardından mesaj yükü normal şekilde işlenir.

İkinci mesaj, Bob'dan Alice'e, mesaj yükünden önce ekem1 şifreli metnini içerir. Bu, ek bir sabit anahtar olarak kabul edilir; bununla birlikte EncryptAndHash() (Bob olarak) veya DecryptAndHash() (Alice olarak) çağrısı yapılır. Ardından, kem_shared_key hesaplanır ve MixKey(kem_shared_key) çağrılır. Bundan sonra mesaj yükü normal şekilde işlenir.

#### Tanımlanmış ML-KEM İşlemleri

[FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) belgesinde tanımlandığı gibi kullanılan kriptografik yapı taşlarına karşılık gelen aşağıdaki fonksiyonları tanımlarız.

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

kem_shared_key = DECAPS(sifreli_metin, decap_anahtari)

    Alice calculates the shared key,
    using the ciphertext received in message 2.
    The kem_shared_key is always 32 bytes.

encap_key ve şifreli metnin her ikisinin de Gürültü el sıkışma mesajları 1 ve 2'deki ChaCha/Poly bloklarının içinde şifrelendiğini unutmayın. Bu değerler, el sıkışma sürecinin bir parçası olarak çözülecektir.

kem_shared_key, MixHash() ile zincirleme anahtarına karıştırılır. Ayrıntılar için aşağıya bakın.

#### İleti 1 için Alice KDF

'Es' mesaj deseninden sonra ve yükten önce şunu ekleyin:

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

'Es' mesaj deseninden sonra ve yükten önce şunu ekleyin:

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

XK için: 'ee' mesaj deseninden sonra ve yükten önce şunu ekleyin:

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
#### İleti 2 için Alice KDF

'ee' mesaj deseninden sonra şunu ekleyin:

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
#### İleti 3 için KDF (sadece XK)

unchanged

#### split() için KDF

unchanged

### El sıkışma Ayrıntıları

#### Gürültü tanımlayıcıları

- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM1024_ChaChaPoly_SHA256"

#### 1) Oturum İsteği

Değişiklikler: Mevcut NTCP2 yalnızca tek bir ChaCha bölümündeki seçenekleri içerir. ML-KEM ile, seçeneklerden önce şifrelenmiş PQ genel anahtarını içeren yeni bir ChaCha bölümü eklenecek.

Aynı yönlendirici adresi ve bağlantı noktasında PQ ve PQ olmayan NTCP2'nin desteklenebilmesi için, bunun bir PQ bağlantısı olduğunu belirtmek üzere X değerinin (X25519 geçici ortak anahtarı) en anlamlı bitini kullanıyoruz. Bu bit, PQ olmayan bağlantılarda her zaman sıfırlanır.

Alice için, mesaj Noise tarafından şifrelendikten sonra ancak X'in AES şifrelemesi uygulanmadan önce, X[31] |= 0x7f ayarlayın.

Bob için, X'in AES ile şifresi çözüldükten sonra X[31] & 0x80 değerini test edin. Eğer bit ayarlanmışsa, X[31] &= 0x7f ile temizleyin ve bir PQ bağlantısı olarak Noise ile şifresini çözün. Eğer bit temizse, normalde olduğu gibi bir PQ olmayan bağlantı olarak Noise ile şifresini çözün.

Farklı bir yönlendirici adresi ve bağlantı noktasında reklam verilen PQ NTCP2 için bu gerekli değildir.

Ek bilgi için aşağıda Yayımlanan Adresler bölümünü görün.

Ham içerikler:

```
  +----+----+----+----+----+----+----+----+
  |        MS bit set to 1 and then       |
  +        obfuscated with RH_B           +
  |       AES-CBC-256 encrypted X         |
  +             (32 bytes)                +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaChaPoly encrypted data (MLKEM)   |
  +      (see table below for length)     +
  |   k defined in KDF for message 1      |
  +   n = 0                               +
  |   see KDF for associated data         |
  ~                                       ~
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (options)   |
  +         16 bytes                      +
  |   k defined in KDF for message 1      |
  +   n = 1                               +
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

  Same as current specification except add a second ChaChaPoly frame
```
Şifrelenmemiş veri (Poly1305 kimlik doğrulama etiketi gösterilmedi):

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
  |           ML-KEM encap_key            |
  +      (see table below for length)     +
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
```
Not: Mesaj 1 seçenekler bloğundaki sürüm alanı, PQ bağlantıları için bile 2 olarak ayarlanmalıdır.

Boyutlar:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">X len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Msg 1 len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Msg 1 Enc len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Msg 1 Dec len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">PQ key len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">opt len</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">64+pad</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">--</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">880+pad</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">848</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">816</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">800</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1264+pad</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1232</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1200</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1184</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1648+pad</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1616</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1584</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1568</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
</tr>
</table>
Not: Tür kodları yalnızca iç kullanım içindir. Yönlendiriciler tür 4 olarak kalacak ve destek yönlendirici adreslerinde belirtilecektir.

#### 2) OturumOluşturuldu

Değişiklikler: Mevcut NTCP2 yalnızca tek bir ChaCha bölümündeki seçenekleri içerir. ML-KEM ile, şifreli Kuantum Sonrası şifreli metnini içeren seçeneklerden önce yeni bir ChaCha bölümü eklenecek.

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
  |   ChaCha20 encrypted data (MLKEM)     |
  -      (see table below for length)     -
  +   k defined in KDF for message 2      +
  |  (before mixKey)                      |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 encrypted data (options)   |
  -           16 bytes                    -
  +   k defined in KDF for message 2      +
  |  (after mixKey)                       |
  +  n = 0; see KDF for associated data   +
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

  Same as current specification except add a second ChaChaPoly frame
```
Şifrelenmemiş veri (Poly1305 kimlik doğrulama etiketi gösterilmedi):

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
  |           ML-KEM Ciphertext           |
  +      (see table below for length)     +
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
```
Boyutlar:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Y len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Msg 2 len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Msg 2 Enc len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Msg 2 Dec len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">PQ CT len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">opt len</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">64+pad</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">--</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">848+pad</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">816</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">784</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">768</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1168+pad</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1136</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1104</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1088</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1648+pad</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1616</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1584</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1568</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
</tr>
</table>
Not: Tür kodları yalnızca iç kullanım içindir. Yönlendiriciler tür 4 olarak kalacak ve destek yönlendirici adreslerinde belirtilecektir.

#### 3) OturumOnaylandı

Değişmedi

#### Anahtar Türetme Fonksiyonu (KDF) (veri aşaması için)

Değişmedi

#### Yayınlanan Adresler

Tüm durumlarda, NTCP2 taşıma adını olduğu gibi kullanın.

PQ olmayan, güvenlik duvarına sahip olmayan ile aynı adres/bağlantı noktasını kullanın. Sadece bir PQ çeşidi desteklenir. Yönlendirici adresinde, v=2'yi (normal şekilde) ve MLKEM 512/768/1024'ü belirtmek için yeni parametre pq=[3|4|5]'i yayınlayın. Alice, bu bağlantının hibrit bir bağlantı olduğunu belirtmek için oturum isteğinde geçici anahtarın MSB'sini (key[31] & 0x80) ayarlar. Yukarıya bakın. Eski yönlendiriciler pq parametresini yoksayar ve normal şekilde pq'suz bağlanır.

Farklı adres/bağlantı noktası, PQ olmayan ya da yalnızca PQ ve duvar arkası olmayan yapılar desteklenmez. PQ olmayan NTCP2 devre dışı bırakılana kadar, bu özellik birkaç yıl boyunca uygulanmayacaktır. PQ olmayan devre dışı bırakıldığında, birden fazla PQ çeşidi desteklenebilir ancak adres başına yalnızca biri olabilir. Desteklendiğinde, yönlendirici adresinde MLKEM 512/768/1024'ü belirtmek için v=[3|4|5] yayımlanmalıdır. Alice, geçici anahtarın MSB'sini ayarlamaz. Eski yönlendiriciler v parametresini kontrol eder ve bu adresi desteklenmiyor olarak atlar.

Güvenlik duvarına alınmış adresler (yayınlanan IP yok): Yönlendirici adresinde, v=2'yi yayınlayın (normal şekilde). pq parametresi yayınlamaya gerek yok.

Alice, Bob'un yayınladığı PQ varyantını kullanarak PQ Bob'a bağlanabilir; Alice, yönlendirici bilgisinde PQ desteğini ilan etmiş olsun ya da etmemiş olsun ve aynı varyantı ilan etmiş olsun ya da etmemiş olsun fark etmez.

#### Maksimum Dolgu

Geçerli spesifikasyonda, 1. ve 2. mesajların "makul" miktarda dolgu içermesi tanımlanmıştır ve önerilen aralık 0-31 bayt olarak belirtilmiştir, maksimum değer belirtilmemiştir.

API 0.9.68'e kadar (sürüm 2.11.0), Java I2P PQ olmayan bağlantılar için maksimum 256 bayt doldurma uyguladı, ancak bu daha önce belgelenmemişti. API 0.9.69'dan itibaren (sürüm 2.12.0), Java I2P PQ olmayan bağlantılar için MLKEM-512 ile aynı maksimum doldurmayı uygular. Aşağıdaki tabloya bakın.

PQ bağlantıları için maksimum doldurma, tanımlanan mesaj boyutu kadar olacak, yani maksimum doldurma mesaj boyutunu iki katına çıkartacaktır, şu şekilde:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Message Max Padding</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">non-PQ (thru 0.9.68)</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">non-PQ (as of 0.9.69)</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">MLKEM-512</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">MLKEM-768</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">MLKEM-1024</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Session Request</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">256</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">880</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">880</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1264</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1648</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Session Created</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">256</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">848</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">848</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1168</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1648</td>
</tr>
</table>
## Ek Yük Analizi

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
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+1584</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+1584</td>
</tr>
</table>
## Güvenlik Analizi

NIST güvenlik kategorileri, [NIST sunumu](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf) 10. sayfasında özetlenmiştir. Ön kriterler: Hibrit protokoller için minimum NIST güvenlik kategorimiz 2, sadece KPK için ise 3 olmalıdır.

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
### Tokalaşmalar

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
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
</tr>
</table>
## Uygulama Notları

### Kütüphane Desteği

Bouncycastle, BoringSSL ve WolfSSL kütüphaneleri artık MLKEM ve MLDSA'yı destekliyor. OpenSSL desteği 8 Nisan 2025'te yapılacakları 3.5 sürümüyle gelecek [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

### Gelen Trafik Tanımlama

Geçici anahtarın en anlamlı bitini (key[31] & 0x80), bunun hibrit bir bağlantı olduğunu belirtmek için oturum isteğinde ayarlarız. Bu, standart NTCP ve hibrit NTCP'yi aynı portta çalıştırabilmemizi sağlar. Gelen bağlantılar için yalnızca bir hibrit varyant desteklenir ve bu, yönlendirici adresinde duyurulur. Örneğin, pq=3 veya pq=4.

#### Şifreleme

Alice olarak, PQ bağlantısı için şifrelemeden önce X[31] |= 0x80 ayarlayın. Bu, X'i geçersiz bir X25519 açık anahtarı yapar. Şifrelemeden sonra AES-CBC bunu rastgele hale getirecektir. X'in en anlamlı biti (MSB), şifrelemeden sonra rastgele olacaktır.

Bob olarak, şifre çözmeden sonra (X[31] & 0x80) != 0 olup olmadığını test edin. Eğer öyleyse, bu bir PQ bağlantısıdır.

NTCP2-PQ için gerekli minimum yönlendirici sürümü henüz belirlenmedi (TBD).

Not: Tür kodları yalnızca iç kullanım içindir. Yönlendiriciler tür 4 olarak kalacak ve destek yönlendirici adreslerinde belirtilecektir.

## Yönlendirici Uyumluluğu

### Taşıma Adları

Tüm durumlarda, NTCP2 taşıma adını her zamanki gibi kullanın. Eski yönlendiriciler pq parametresini yoksayar ve her zamanki gibi standart NTCP2 ile bağlanır.

## Referanslar

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
