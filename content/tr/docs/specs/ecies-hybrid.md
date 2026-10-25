---
title: "PQ Hybrid ECIES-X25519-AEAD-Ratchet"
description: "ML-KEM kullanan ECIES şifreleme protokolünün kuantum sonrası hibrit varyantı"
slug: "ecies-hybrid"
category: "Protokoller"
lastUpdated: "2026-04"
accurateFor: "0.9.69"
---

## Not

Çeşitli router uygulamalarında geliştirme, test ve dağıtım süreci devam ediyor. Durum için bu uygulamaların belgelerini kontrol edin.

## Genel Bakış

Bu, ECIES-X25519-AEAD-Ratchet protokolünün [ECIES](/docs/specs/ecies/) PQ Hybrid varyantıdır. Onaylanacak genel PQ önerisi [Prop169](/proposals/169-pq-crypto/)'un ilk aşamasıdır. Genel hedefler, tehdit modelleri, analiz, alternatifler ve ek bilgiler için bu öneriye bakın.

Bu spesifikasyon yalnızca standart [ECIES](/docs/specs/ecies/) ile olan farklılıkları içerir ve o spesifikasyon ile birlikte okunmalıdır.

## Tasarım

CRYSTALS-Kyber'a dayalı ancak onunla UYUMLU OLMAYAN NIST FIPS 203 standardını destekliyoruz [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

Hybrid handshake'ler [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) belirtiminde tanımlandığı gibidir.

### Anahtar Değişimi

Ratchet için hibrit bir anahtar değişimi tanımlıyoruz. PQ KEM yalnızca geçici anahtarlar sağlar ve Noise IK gibi statik anahtar el sıkışmalarını doğrudan desteklemez.

[FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)'te belirtildiği gibi üç ML-KEM varyantını tanımlıyoruz, toplam 3 yeni şifreleme türü için. Hibrit türler yalnızca X25519 ile kombinasyon halinde tanımlanmıştır.

Yeni şifreleme türleri şunlardır:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Code</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
</tr>
</table>
Ek yük önemli olacaktır. Tipik mesaj 1 ve 2 boyutları (IK için) şu anda yaklaşık 100 bayt civarındadır (herhangi bir ek yük öncesi). Bu, algoritmaya bağlı olarak 8x ile 15x arasında artacaktır.

### Yeni Kripto Gerekli

- ML-KEM (eski adıyla CRYSTALS-Kyber) [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
- SHA3-128 (eski adıyla Keccak-256) [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf) Yalnızca SHAKE128 için kullanılır
- SHA3-256 (eski adıyla Keccak-512) [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
- SHAKE128 ve SHAKE256 (SHA3-128 ve SHA3-256'nın XOF uzantıları)
  [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)

SHA3-256, SHAKE128 ve SHAKE256 için test vektörleri [NIST-VECTORS](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values) adresinde bulunmaktadır.

Java bouncycastle kütüphanesinin yukarıdakilerin tümünü desteklediğini unutmayın. C++ kütüphane desteği OpenSSL 3.5'te mevcuttur [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

## Spesifikasyon

### Ortak Yapılar

Anahtar uzunlukları ve tanımlayıcılar için ortak yapılar spesifikasyonuna bakın [COMMON](/docs/specs/common-structures/).

### Handshake Kalıpları

El sıkışmalar [Noise](https://noiseprotocol.org/noise.html) el sıkışma desenlerini kullanır.

Aşağıdaki harf eşlemesi kullanılır:

- e = tek kullanımlık geçici anahtar
- s = statik anahtar
- p = mesaj yükü
- e1 = tek kullanımlık geçici PQ anahtarı, Alice'den Bob'a gönderilir
- ekem1 = KEM şifreli metni, Bob'dan Alice'e gönderilir

Hibrit ileri güvenlik (hfs) için XK ve IK'ya yapılan aşağıdaki değişiklikler [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) bölüm 5'te belirtildiği gibidir:

```
IK:                         IKhfs:
<- s                        <- s
...                         ...
-> e, es, s, ss, p          -> e, es, e1, s, ss, p
<- tag, e, ee, se, p        <- tag, e, ee, ekem1, se, p
<- p                        <- p
p ->                        p ->

e1 and ekem1 are encrypted. See pattern definitions below.
NOTE: e1 and ekem1 are different sizes (unlike X25519)
```
e1 deseni, [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) bölüm 4'te belirtildiği gibi aşağıdaki şekilde tanımlanır:

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
ekem1 deseni, [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) bölüm 4'te belirtildiği şekilde aşağıdaki gibi tanımlanır:

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
### Tanımlı ML-KEM Operasyonları

[FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)'te tanımlandığı şekilde kullanılan kriptografik yapı taşlarına karşılık gelen aşağıdaki fonksiyonları tanımlıyoruz.

**(encap_key, decap_key) = PQ_KEYGEN()**

Alice, kapsülleme ve kapsül açma anahtarlarını oluşturur. Kapsülleme anahtarı NS mesajında gönderilir. encap_key ve decap_key boyutları ML-KEM varyantına göre değişir.

**(ciphertext, kem_shared_key) = ENCAPS(encap_key)**

Bob, NS mesajında aldığı ciphertext kullanarak ciphertext ve paylaşılan anahtarı hesaplar. Ciphertext, NSR mesajında gönderilir. ciphertext boyutu ML-KEM varyantına göre değişir. kem_shared_key her zaman 32 bayttır.

**kem_shared_key = DECAPS(ciphertext, decap_key)**

Alice, NSR mesajında aldığı şifrelenmiş metin kullanarak paylaşılan anahtarı hesaplar. kem_shared_key her zaman 32 bayttır.

Hem encap_key hem de ciphertext'in, Noise handshake mesajları 1 ve 2'deki ChaCha/Poly blokları içinde şifrelendiğini unutmayın. Bunlar handshake süreci kapsamında şifresi çözülecektir.

kem_shared_key, MixHash() ile chaining key'e karıştırılır. Ayrıntılar için aşağıya bakın.

### Noise Handshake KDF

#### Genel Bakış

Hibrit el sıkışma [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) belgesinde tanımlanmıştır. Alice'den Bob'a gönderilen ilk mesaj, mesaj yükünden önce e1 kapsülleme anahtarını içerir. Bu ek bir statik anahtar olarak ele alınır; (Alice olarak) EncryptAndHash() veya (Bob olarak) DecryptAndHash() çağırın. Ardından mesaj yükünü her zamanki gibi işleyin.

İkinci mesaj, Bob'dan Alice'e, mesaj yükünden önce ekem1 olan şifreli metni içerir. Bu ek bir statik anahtar olarak değerlendirilir; (Bob olarak) EncryptAndHash() veya (Alice olarak) DecryptAndHash() çağırın. Sonra, kem_shared_key'i hesaplayın ve MixKey(kem_shared_key) çağırın. Ardından mesaj yükünü her zamanki gibi işleyin.

#### Noise tanımlayıcıları

Bunlar Noise başlatma dizeleridir:

- "Noise_IKhfselg2_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM1024_ChaChaPoly_SHA256"

#### NS Mesajı için Alice KDF

'es' mesaj deseninden sonra ve 's' mesaj deseninden önce, şunu ekleyin:

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

NOTE: For the next section (static key for IK),
the keydata and chain key remain the same, and n now equals 1
(instead of 0 for non-hybrid).
```
#### NS Mesajı için Bob KDF

'es' mesaj deseninden sonra ve 's' mesaj deseninden önce şunu ekleyin:

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

NOTE: For the next section (static key for IK),
the keydata and chain key remain the same, and n now equals 1
(instead of 0 for non-hybrid).
```
#### NSR Mesajı için Bob KDF

'ee' mesaj deseninden sonra ve 'se' mesaj deseninden önce şunu ekleyin:

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
```
#### NSR Mesajı için Alice KDF

'ee' mesaj deseninden sonra ve 'ss' mesaj deseninden önce şunu ekleyin:

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
```
#### split() için KDF

değişmemiş

### Mesaj Formatı

#### NS Formatı

Değişiklikler: Mevcut ratchet, statik anahtarı ilk ChaCha bölümünde ve yükü ikinci bölümde içeriyordu. ML-KEM ile artık üç bölüm bulunuyor. İlk bölüm şifrelenmiş PQ genel anahtarını içeriyor. İkinci bölüm statik anahtarı içeriyor. Üçüncü bölüm yükü içeriyor.

Şifrelenmiş format:

```
+----+----+----+----+----+----+----+----+
|                                       |
+         New Session Ephemeral         +
|            Public Key                 |
+            32 bytes                   +
|      Encoded with Elligator2          |
+----+----+----+----+----+----+----+----+
|                                       |
+         ML-KEM encap_key              +
|       ChaCha20 encrypted data         |
+   (see table below for length)        +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+      (MAC) for encap_key Section      +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
|                                       |
+         X25519 Static Key             +
|       ChaCha20 encrypted data         |
+            32 bytes                   +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+     (MAC) for Static Key Section      +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
|                                       |
+          Payload Section              +
|       ChaCha20 encrypted data         |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+      (MAC) for Payload Section        +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
```
Şifresi çözülmüş format:

```
Payload Part 1:

+----+----+----+----+----+----+----+----+
|                                       |
+         ML-KEM encap_key              +
|                                       |
+   (see table below for length)        +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

Payload Part 2:

+----+----+----+----+----+----+----+----+
|                                       |
+         X25519 Static Key             +
|            (32 bytes)                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

Payload Part 3:

+----+----+----+----+----+----+----+----+
|                                       |
+          Payload Section              +
|                                       |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
Boyutlar:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">X len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NS len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NS Enc len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NS Dec len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">PQ key len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">pl len</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">96+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">64+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">--</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">912+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">880+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">800+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">800</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1296+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1360+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1184+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1184</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1680+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1648+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1568+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1568</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
</table>
Payload'ın bir DateTime bloğu içermesi gerektiğini, bu nedenle minimum payload boyutunun 7 olduğunu unutmayın. Minimum NS boyutları buna göre hesaplanabilir.

#### NSR Formatı

Değişiklikler: Mevcut ratchet, ilk ChaCha bölümü için boş bir payload ve ikinci bölümde payload içerir. ML-KEM ile artık üç bölüm bulunmaktadır. İlk bölüm şifrelenmiş PQ ciphertext içerir. İkinci bölümde boş bir payload bulunur. Üçüncü bölüm payload içerir.

Şifrelenmiş format:

```
+----+----+----+----+----+----+----+----+
|       Session Tag 8 bytes             |
+----+----+----+----+----+----+----+----+
|                                       |
+       Ephemeral Public Key            +
|            32 bytes                   |
+      Encoded with Elligator2          +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+         ML-KEM ciphertext             +
|       ChaCha20 encrypted data         |
+   (see table below for length)        +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+     (MAC) for ciphertext Section      +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+   (MAC) for key Section (no data)     +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
|                                       |
+          Payload Section              +
|       ChaCha20 encrypted data         |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+      (MAC) for Payload Section        +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
```
Şifresi çözülmüş format:

```
Payload Part 1:

+----+----+----+----+----+----+----+----+
|                                       |
+         ML-KEM ciphertext             +
|                                       |
+   (see table below for length)        +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

Payload Part 2:

empty

Payload Part 3:

+----+----+----+----+----+----+----+----+
|                                       |
+          Payload Section              +
|                                       |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
Boyutlar:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Y len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NSR len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NSR Enc len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NSR Dec len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">PQ CT len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">opt len</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">72+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">--</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">856+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">816+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">768+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">768</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1176+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1136+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1088+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1088</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1656+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1616+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1568+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1568</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
</table>
NSR'nin normalde sıfır olmayan bir yük taşıyacağını, ancak ratchet spesifikasyonunun [ECIES](/docs/specs/ecies/) bunu gerektirmediğini, dolayısıyla minimum yük boyutunun 0 olduğunu unutmayın. Minimum NSR boyutları buna göre hesaplanabilir.

## Ek Yük Analizi

### Anahtar Değişimi

Boyut artışı (bayt):

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Pubkey (NS)</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Ciphertext (NSR)</th>
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
Hız:

[CLOUDFLARE](https://blog.cloudflare.com/pq-2024/) tarafından bildirilen hızlar:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Relative speed</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">X25519 DH/keygen</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">baseline</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2.25x faster</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1.5x faster</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1x (same)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">XK</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4x DH (keygen + 3 DH)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4x DH + 2x PQ (keygen + enc/dec) = 4.9x DH = 22% slower</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4x DH + 2x PQ (keygen + enc/dec) = 5.3x DH = 32% slower</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4x DH + 2x PQ (keygen + enc/dec) = 6x DH = 50% slower</td>
</tr>
</table>
## Güvenlik Analizi

NIST güvenlik kategorileri [NIST-PQ-END](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf) slayt 10'da özetlenmiştir. Ön kriterler: Hibrit protokoller için minimum NIST güvenlik kategorimiz 2, yalnızca PQ protokolleri için 3 olmalıdır.

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

Bunların hepsi hibrit protokollerdir. Muhtemelen MLKEM768'i tercih etmek gerekiyor; MLKEM512 yeterince güvenli değil.

NIST güvenlik kategorileri [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf):

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
## Tür Tercihleri

Güvenlik kategorisi ve anahtar uzunluğuna dayalı olarak, ilk destek için önerilen tür şudur:

MLKEM768_X25519 (tip 6)

## Uygulama Notları

### Kütüphane Desteği

Bouncycastle, BoringSSL ve WolfSSL kütüphaneleri artık MLKEM destekliyor. OpenSSL desteği 8 Nisan 2025 tarihli 3.5 sürümünde gelecek [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

### Paylaşılan Tunnel'lar

Aynı tunnel'lar üzerinde birden fazla protokolün otomatik sınıflandırılması/algılanması, mesaj 1'in (Yeni Oturum Mesajı) uzunluk kontrolüne dayalı olarak mümkün olmalıdır. Örnek olarak MLKEM512_X25519 kullanıldığında, mesaj 1 uzunluğu mevcut ratchet protokolünden 816 bayt daha büyüktür ve minimum mesaj 1 boyutu (sadece DateTime payload'u dahil) 919 bayttır. Mevcut ratchet ile mesaj 1 boyutlarının çoğu 816 bayttan küçük payload'a sahiptir, bu nedenle hibrit olmayan ratchet olarak sınıflandırılabilirler. Büyük mesajlar muhtemelen nadir olan POST'lardır.

Bu nedenle önerilen strateji şudur:

- Mesaj 1, 919 bayttan küçükse, mevcut ratchet protokolüdür.
- Mesaj 1, 919 bayt veya daha büyükse, muhtemelen MLKEM512_X25519'dur. Önce MLKEM512_X25519'u deneyin ve başarısız olursa, mevcut ratchet protokolünü deneyin.

Bu, aynı hedefte standart ratchet ve hibrit ratchet'i verimli bir şekilde desteklememizi sağlamalıdır, tıpkı daha önce aynı hedefte ElGamal ve ratchet'i desteklediğimiz gibi. Bu nedenle, aynı hedef için çift protokol desteği sunamadığımız duruma kıyasla MLKEM hibrit protokolüne çok daha hızlı geçiş yapabiliriz, çünkü mevcut hedeflere MLKEM desteği ekleyebiliriz.

Gerekli desteklenen kombinasyonlar şunlardır:

- X25519 + MLKEM512
- X25519 + MLKEM768
- X25519 + MLKEM1024

Aşağıdaki kombinasyonlar karmaşık olabilir ve desteklenmesi ZORUNLU DEĞİLDİR, ancak uygulamaya bağlı olarak desteklenebilir:

- Birden fazla MLKEM
- ElG + bir veya daha fazla MLKEM
- X25519 + bir veya daha fazla MLKEM
- ElG + X25519 + bir veya daha fazla MLKEM

Aynı hedefte birden fazla MLKEM algoritmasını (örneğin, MLKEM512_X25519 ve MLKEM_768_X25519) desteklemek zorunlu değildir. Sadece birini seçin. Uygulama-bağımlı.

Aynı hedefte üç algoritmayı (örneğin X25519, MLKEM512_X25519 ve MLKEM769_X25519) desteklemek zorunlu değildir. Sınıflandırma ve yeniden deneme stratejisi çok karmaşık olabilir. Yapılandırma ve yapılandırma arayüzü çok karmaşık olabilir. Uygulamaya bağlıdır.

Aynı hedefte ElGamal ve hibrit algoritmalarını desteklemek gerekli değildir. ElGamal artık kullanılmıyor ve sadece ElGamal + hibrit (X25519 olmadan) pek mantıklı değil. Ayrıca, ElGamal ve Hibrit Yeni Oturum Mesajları büyük olduğundan, sınıflandırma stratejileri genellikle her iki şifre çözme işlemini de denemek zorunda kalır ve bu verimsiz olur. Uygulama-bağımlıdır.

İstemciler, aynı tünellerde X25519 ve hibrit protokoller için aynı veya farklı X25519 statik anahtarları kullanabilir, implementasyona bağlıdır.

### İleri Gizlilik

ECIES spesifikasyonu, New Session Message payload'ında Garlic Messages'a izin verir, bu da başlangıç streaming paketinin (genellikle bir HTTP GET) istemcinin leaseset'i ile birlikte 0-RTT teslimatına olanak sağlar. Ancak, New Session Message payload'ı forward secrecy'ye sahip değildir. Bu öneri ratchet için gelişmiş forward secrecy'yi vurguladığı için, implementasyonlar streaming payload'ını veya tam streaming mesajını ilk Existing Session Message'a kadar erteleyebilir veya ertelemelidir. Bu, 0-RTT teslimatının pahasına olacaktır. Stratejiler ayrıca trafik türüne veya tunnel türüne, ya da örneğin GET vs. POST'a bağlı olabilir. Implementasyona bağlıdır.

### Yeni Oturum Boyutu

MLKEM, yukarıda açıklandığı gibi New Session Message boyutunu dramatik olarak artıracaktır. Bu, 1024 baytlık tunnel mesajlarına bölünmeleri gereken tunnel'lar aracılığıyla New Session Message teslimatının güvenilirliğini önemli ölçüde azaltabilir. Teslimat başarısı, fragment sayısının üsseli ile orantılıdır. Uygulamalar, 0-RTT teslimatı pahasına mesaj boyutunu sınırlamak için çeşitli stratejiler kullanabilir. Uygulama-bağımlıdır.

## Referanslar

- [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/)
- [COMMON](/docs/specs/common-structures/)
- [ECIES](/docs/specs/ecies/)
- [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
- [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
- [FORUM](http://zzz.i2p/topics/3294)
- [NIST-PQ-END](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf)
- [NIST-VECTORS](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values)
- [Noise](https://noiseprotocol.org/noise.html)
- [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf)
- [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)
- [PQ-WIREGUARD](https://eprint.iacr.org/2020/379.pdf)
- [Prop169](/proposals/169-pq-crypto/)
