---
title: "ECIES-X25519-AEAD-Ratchet Hibrit Şifreleme"
description: "ML-KEM (modül-örgü tabanlı anahtar kapsülleme mekanizması) kullanan ECIES şifreleme protokolünün kuantum sonrası hibrit varyantı"
slug: "ecies-hybrid"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Gerçekleştirim Durumu

**Güncel Dağıtım:** - **i2pd (C++ implementasyonu)**: ML-KEM-512, ML-KEM-768 ve ML-KEM-1024 desteğiyle 2.58.0 sürümünde (Eylül 2025) tamamen uygulanmıştır. OpenSSL 3.5.0 veya daha yenisi mevcut olduğunda post-kuantum uçtan uca şifreleme varsayılan olarak etkinleştirilir. - **Java I2P**: 0.9.67 / 2.10.0 sürümleri itibarıyla (Eylül 2025) henüz uygulanmamıştır. Spesifikasyon onaylanmış olup, uygulama gelecekteki sürümler için planlanmaktadır.

Bu belirtim, i2pd'de hâlihazırda devreye alınmış ve Java I2P gerçekleştirimleri için planlanan onaylı işlevselliği tanımlar.

## Genel Bakış

Bu, ECIES-X25519-AEAD-Ratchet protokolünün [ECIES](/docs/specs/ecies/) kuantum sonrası hibrit varyantıdır. Onaylanması beklenen Öneri 169’un [Prop169](/proposals/169-pq-crypto/) ilk aşamasını temsil eder. Genel hedefler, tehdit modelleri, analiz, alternatifler ve ek bilgiler için söz konusu öneriye bakın.

Öneri 169 durumu: **Açık** (hibrit ECIES uygulamasının ilk aşaması onaylandı).

Bu spesifikasyon, standart [ECIES](/docs/specs/ecies/)'ten yalnızca farkları içerir ve söz konusu spesifikasyonla birlikte okunmalıdır.

## Tasarım


Hibrit el sıkışmaları, klasik X25519 Diffie-Hellman’ı kuantum sonrası ML-KEM anahtar kapsülleme mekanizmalarıyla birleştirir. Bu yaklaşım, PQNoise araştırmasında belgelenen hibrit ileri gizlilik kavramlarına ve TLS 1.3, IKEv2 ve WireGuard’daki benzer uygulamalara dayanır.

### Anahtar Değişimi

Ratchet (anahtar yenileme mekanizması) için hibrit bir anahtar değişimi tanımlıyoruz. Post-quantum KEM (anahtar kapsülleme mekanizması) yalnızca geçici anahtarlar sağlar ve Noise IK gibi statik anahtarlı el sıkışmalarını doğrudan desteklemez.

[FIPS203](https://csrc.nist.gov/pubs/fips/203/final)'te belirtildiği üzere üç ML-KEM varyantını tanımlıyoruz; böylece toplamda 3 yeni şifreleme türü elde ediliyor. Hibrit türler yalnızca X25519 ile birlikte tanımlanır.

Yeni şifreleme türleri şunlardır:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Security Level</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">ML-KEM Variant</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NIST Category 1 (AES-128 equivalent)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ML-KEM-512</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NIST Category 3 (AES-192 equivalent)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ML-KEM-768 (Recommended)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NIST Category 5 (AES-256 equivalent)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ML-KEM-1024</td>
    </tr>
  </tbody>
</table>
**Not:** MLKEM768_X25519 (Type 6), makul düzeyde ek yükle güçlü kuantum sonrası güvenlik sağlayan önerilen varsayılan varyanttır.

Yalnızca X25519 kullanan şifrelemeyle karşılaştırıldığında ek yük önemli ölçüde fazladır. IK pattern (Noise el sıkışma deseni) için tipik 1 ve 2 numaralı ileti boyutları (ek yükten önce) şu anda yaklaşık 96-103 bayttır. Bu değer, ileti türüne bağlı olarak MLKEM512 için yaklaşık 9-12 kat, MLKEM768 için 13-16 kat ve MLKEM1024 için 17-23 kat artacaktır.

### Yeni Şifreleme Gerekli

- **ML-KEM** (eski adıyla CRYSTALS-Kyber) [FIPS203](https://csrc.nist.gov/pubs/fips/203/final) - Modül-örgü tabanlı Anahtar Kapsülleme Mekanizması Standardı
- **SHA3-256** (eski adıyla Keccak-512) [FIPS202](https://csrc.nist.gov/pubs/fips/202/final) - SHA-3 Standardının parçası
- **SHAKE128 and SHAKE256** (SHA3 için XOF uzantıları) [FIPS202](https://csrc.nist.gov/pubs/fips/202/final) - Genişletilebilir Çıktı Fonksiyonları

SHA3-256, SHAKE128 ve SHAKE256 için test vektörleri [NIST Kriptografik Algoritma Doğrulama Programı](https://csrc.nist.gov/Projects/cryptographic-algorithm-validation-program) adresinde mevcuttur.

**Kütüphane Desteği:** - Java: Bouncycastle kütüphanesi sürüm 1.79 ve sonrası tüm ML-KEM (modül-kafes tabanlı anahtar kapsülleme mekanizması) varyantlarını ve SHA3/SHAKE işlevlerini destekler - C++: OpenSSL 3.5 ve sonrası tam ML-KEM desteği içerir (Nisan 2025'te yayımlandı) - Go: ML-KEM ve SHA3 gerçek­lemesi için birden çok kütüphane mevcut

## Şartname

### Ortak Yapılar

Anahtar uzunlukları ve tanımlayıcılar hakkında bilgi için [Common Structures Specification](/docs/specs/common-structures/) belgesine bakın.

### El Sıkışma Desenleri

El sıkışmaları, hibrit kuantum sonrası güvenlik için I2P'ye özgü uyarlamalarla [Noise Protocol Framework (Noise Protokol Çerçevesi)](https://noiseprotocol.org/noise.html) el sıkışma kalıplarını kullanır.

Aşağıdaki harf eşlemesi kullanılır:

- **e** = tek kullanımlık geçici anahtar (X25519)
- **s** = statik anahtar
- **p** = mesaj yükü
- **e1** = tek kullanımlık geçici PQ (post-quantum - kuantum-sonrası) anahtar, Alice'ten Bob'a gönderilen (I2P'ye özgü belirteç)
- **ekem1** = KEM (Key Encapsulation Mechanism - Anahtar Kapsülleme Mekanizması) şifreli metni, Bob'dan Alice'e gönderilen (I2P'ye özgü belirteç)

**Önemli Not:** "IKhfs" ve "IKhfselg2" desen adları ile "e1" ve "ekem1" belirteçleri, resmi Noise Protocol Framework spesifikasyonunda belgelenmeyen, I2P’ye özgü uyarlamalardır. Bunlar, ML-KEM’i Noise IK desenine entegre etmek için özel tanımları temsil eder. Hibrit X25519 + ML-KEM yaklaşımı post-kuantum kriptografi araştırmalarında ve diğer protokollerde yaygın olarak kabul görse de, burada kullanılan özgül adlandırma I2P’ye özgüdür.

Hibrit ileri gizlilik için IK'ye yönelik aşağıdaki değişiklikler uygulanır:

```
Standard IK:              I2P IKhfs (Hybrid):
<- s                      <- s
...                       ...
-> e, es, s, ss, p        -> e, es, e1, s, ss, p
<- e, ee, se, p           <- e, ee, ekem1, se, p
<- p                      <- p
p ->                      p ->

Note: e1 and ekem1 are encrypted within ChaCha20-Poly1305 AEAD blocks.
Note: e1 (ML-KEM public key) and ekem1 (ML-KEM ciphertext) have different sizes.
```
**e1** deseni aşağıdaki gibi tanımlanır:

```
For Alice (sender):
(encap_key, decap_key) = PQ_KEYGEN()

// EncryptAndHash(encap_key)
ciphertext = ENCRYPT(k, n, encap_key, ad)
n++
MixHash(ciphertext)

For Bob (receiver):
// DecryptAndHash(ciphertext)
encap_key = DECRYPT(k, n, ciphertext, ad)
n++
MixHash(ciphertext)
```
**ekem1** örüntüsü aşağıdaki gibi tanımlanır:

```
For Bob (receiver of encap_key):
(kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

// EncryptAndHash(kem_ciphertext)
ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)
MixHash(ciphertext)

// MixKey
MixKey(kem_shared_key)

For Alice (sender of encap_key):
// DecryptAndHash(ciphertext)
kem_ciphertext = DECRYPT(k, n, ciphertext, ad)
MixHash(ciphertext)

// MixKey
kem_shared_key = DECAPS(kem_ciphertext, decap_key)
MixKey(kem_shared_key)
```
### Tanımlanmış ML-KEM (Modüler Kafes Tabanlı Anahtar Kapsülleme Mekanizması) İşlemleri

[FIPS203](https://csrc.nist.gov/pubs/fips/203/final)'te belirtildiği gibi kriptografik yapı taşlarına karşılık gelen aşağıdaki fonksiyonları tanımlıyoruz.

**(encap_key, decap_key) = PQ_KEYGEN()** : Alice kapsülleme ve dekapsülleme anahtarlarını oluşturur. Kapsülleme anahtarı NS mesajında gönderilir. Anahtar boyutları:   - ML-KEM-512: encap_key = 800 bayt, decap_key = 1632 bayt   - ML-KEM-768: encap_key = 1184 bayt, decap_key = 2400 bayt   - ML-KEM-1024: encap_key = 1568 bayt, decap_key = 3168 bayt

**(ciphertext, kem_shared_key) = ENCAPS(encap_key)** : Bob, NS mesajında alınan enkapsülasyon anahtarını kullanarak şifreli metni ve paylaşılan anahtarı hesaplar. Şifreli metin NSR mesajında gönderilir. Şifreli metin boyutları:   - ML-KEM-512: 768 bayt   - ML-KEM-768: 1088 bayt   - ML-KEM-1024: 1568 bayt

kem_shared_key, üç varyantın tamamında her zaman **32 bayt**'tır.

**kem_shared_key = DECAPS(ciphertext, decap_key)** : Alice, NSR mesajında aldığı şifreli metni kullanarak paylaşılan anahtarı hesaplar. kem_shared_key her zaman **32 bayt** uzunluğundadır.

**Önemli:** encap_key ve ciphertext, Noise (kriptografik el sıkışma protokolü) el sıkışması mesajları 1 ve 2'deki ChaCha20-Poly1305 blokları içinde şifrelenir. El sıkışma sürecinin bir parçası olarak bunların şifresi çözülecektir.

kem_shared_key, MixKey() ile zincirleme anahtarına karıştırılır. Ayrıntılar için aşağıya bakın.

### Noise Handshake KDF (anahtar türetme fonksiyonu)

#### Genel Bakış

Hibrit el sıkışması, klasik X25519 ECDH ile post-kuantum ML-KEM (Key Encapsulation Mechanism — anahtar kapsülleme mekanizması) birleştirir. Alice’ten Bob’a giden ilk mesaj, mesaj yükünden önce e1’i (ML-KEM kapsülleme anahtarı) içerir. Bu, ek anahtar malzemesi olarak değerlendirilir; bunun üzerinde (Alice olarak) EncryptAndHash() ya da (Bob olarak) DecryptAndHash() çağırın. Ardından mesaj yükünü her zamanki gibi işleyin.

Bob'dan Alice'e giden ikinci mesaj, mesaj yükünden önce ekem1'i (the ML-KEM ciphertext) (ML-KEM ile üretilmiş şifreli veri) içerir. Bu, ek anahtar malzemesi olarak değerlendirilir; ekem1 üzerinde EncryptAndHash() (Bob olarak) ya da DecryptAndHash() (Alice olarak) çağırın. Ardından kem_shared_key'i hesaplayın ve MixKey(kem_shared_key) çağırın. Sonra mesaj yükünü her zamanki gibi işleyin.

#### Noise Tanımlayıcıları

Bunlar, Noise (Noise protokol çerçevesi) başlatma dizeleridir (I2P'ye özgü):

- `Noise_IKhfselg2_25519+MLKEM512_ChaChaPoly_SHA256`
- `Noise_IKhfselg2_25519+MLKEM768_ChaChaPoly_SHA256`
- `Noise_IKhfselg2_25519+MLKEM1024_ChaChaPoly_SHA256`

#### NS Mesajı için Alice KDF (Anahtar Türetme Fonksiyonu)

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

NOTE: For the next section (payload for XK or static key for IK),
the keydata and chain key remain the same,
and n now equals 1 (instead of 0 for non-hybrid).
```
#### NS Mesajı için Bob KDF (anahtar türetme fonksiyonu)

'es' mesaj kalıbından sonra ve 's' mesaj kalıbından önce şunu ekleyin:

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
#### NSR Mesajı için Bob tarafındaki KDF

'ee' mesaj kalıbından sonra ve 'se' mesaj kalıbından önce, şunu ekleyin:

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
#### NSR Mesajı için Alice KDF'si

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

split() fonksiyonu, standart ECIES spesifikasyonundaki haliyle aynen kullanılır. El sıkışma (handshake) tamamlandıktan sonra:

```
keydata = HKDF(chainKey, ZEROLEN, "", 64)
k_ab = keydata[0:31]
k_ba = keydata[32:63]
```
Bunlar, devam eden iletişim için çift yönlü oturum anahtarlarıdır.

### Mesaj Biçimi

#### NS (Yeni Oturum) Biçimi

**Değişiklikler:** Mevcut ratchet (kademeli anahtar yenileme mekanizması) ilk ChaCha20-Poly1305 bölümünde statik anahtarı ve ikinci bölümde yükü içerir. ML-KEM ile artık üç bölüm vardır. Birinci bölüm, şifrelenmiş ML-KEM açık anahtarını (encap_key) içerir. İkinci bölüm statik anahtarı içerir. Üçüncü bölüm yükü içerir.

**Mesaj Boyutları:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">X25519 len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NS len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NS Enc len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NS Dec len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">PQ key len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">pl len</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">96+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">--</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">912+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">880+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">800+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">800</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1296+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1264+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1184+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1184</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1680+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1648+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1568+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1568</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
  </tbody>
</table>
**Not:** Yük, bir DateTime bloğu içermelidir (en az 7 bayt: 1 baytlık tür, 2 baytlık boyut, 4 baytlık zaman damgası). Minimum NS boyutları buna göre hesaplanabilir. Bu nedenle, pratikte minimum NS boyutu X25519 için 103 bayttır ve hibrit varyantlarda 919 ile 1687 bayt arasında değişir.

Üç ML-KEM (modül kafes tabanlı anahtar kapsülleme mekanizması) varyantı için 816, 1200 ve 1584 baytlık boyut artışları, ML-KEM açık anahtarının ve kimlik doğrulamalı şifreleme için 16 baytlık bir Poly1305 MAC'in dahil edilmesinden kaynaklanır.

#### NSR (New Session Reply - Yeni Oturum Yanıtı) Formatı

**Değişiklikler:** Mevcut ratchet (anahtar yenileme mekanizması), ilk ChaCha20-Poly1305 bölümünde veri yükünü boş bırakır ve veri yükü ikinci bölümde yer alır. ML-KEM ile artık üç bölüm vardır. Birinci bölüm, ML-KEM şifreli metnini içerir. İkinci bölümün veri yükü boştur. Üçüncü bölüm veri yükünü içerir.

**Mesaj Boyutları:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">X25519 len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NSR len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NSR Enc len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NSR Dec len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">PQ ct len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">pl len</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">72+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">40+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">--</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">856+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">824+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">784+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">768</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1176+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1144+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1104+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1088</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1656+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1624+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1584+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1568</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
  </tbody>
</table>
Üç ML-KEM varyantı için 784, 1104 ve 1584 baytlık boyut artışları, ML-KEM şifreli metni ile kimlik doğrulamalı şifreleme için 16 baytlık Poly1305 MAC'in toplamından kaynaklanır.

## Ek Yük Analizi

### Anahtar Değişimi

Hibrit şifrelemenin ek yükü, yalnızca X25519’a kıyasla oldukça fazladır:

- **MLKEM512_X25519**: El sıkışma mesajı boyutunda yaklaşık 9-12 kat artış (NS: 9.5 kat, NSR: 11.9 kat)
- **MLKEM768_X25519**: El sıkışma mesajı boyutunda yaklaşık 13-16 kat artış (NS: 13.5 kat, NSR: 16.3 kat)
- **MLKEM1024_X25519**: El sıkışma mesajı boyutunda yaklaşık 17-23 kat artış (NS: 17.5 kat, NSR: 23 kat)

Bu ek yük, kuantum sonrası güvenliğin sağladığı ek avantajlar karşılığında kabul edilebilir. Çarpanlar, temel mesaj boyutları farklı olduğundan mesaj türüne göre değişir (NS en az 96 bayt, NSR en az 72 bayt).

### Bant Genişliğiyle İlgili Hususlar

Minimal yüklerle tipik bir oturum kurulumu için: - Yalnızca X25519 (anahtar değişim algoritması): toplam ~200 bayt (NS + NSR) - MLKEM512_X25519 (MLKEM: kuantuma dayanıklı anahtar kapsülleme; X25519 ile hibrit): toplam ~1,800 bayt (9x artış) - MLKEM768_X25519: toplam ~2,500 bayt (12.5x artış) - MLKEM1024_X25519: toplam ~3,400 bayt (17x artış)

Oturum kurulumu tamamlandıktan sonra, devam eden mesaj şifrelemesi, yalnızca X25519 kullanan oturumlarla aynı veri aktarım biçimini kullanır; bu nedenle sonraki mesajlar için ek yük yoktur.

## Güvenlik Analizi

### El sıkışmaları

Hibrit el sıkışması, hem klasik (X25519) hem de kuantum sonrası (ML-KEM) güvenlik sağlar. Bir saldırganın oturum anahtarlarını kompromize edebilmesi için **her ikisini de** kırması gerekir: klasik ECDH'yi ve kuantum sonrası KEM'i.

Bu şunları sağlar: - **Mevcut güvenlik**: X25519 ECDH (eliptik eğri Diffie–Hellman anahtar değişimi) klasik saldırganlara karşı güvenlik sağlar (128-bit güvenlik seviyesi) - **Geleceğe yönelik güvenlik**: ML-KEM (kuantum sonrası anahtar kapsülleme mekanizması) kuantum saldırganlara karşı güvenlik sağlar (parametre setine göre değişir) - **Hibrit güvenlik**: Oturumu ele geçirmek için her ikisinin de kırılması gerekir (güvenlik seviyesi = iki bileşenden en büyüğü)

### Güvenlik Düzeyleri

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Variant</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NIST Category</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Classical Security</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">PQ Security</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Hybrid Security</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Category 1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit (X25519)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-128 equivalent</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Category 3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit (X25519)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-192 equivalent</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Category 5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit (X25519)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 equivalent</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit</td>
    </tr>
  </tbody>
</table>
**Not:** Hibrit güvenlik seviyesi, iki bileşenden daha zayıf olanıyla sınırlıdır. Tüm durumlarda X25519, 128 bit klasik güvenlik sağlar. Kriptografik açıdan ilgili bir kuantum bilgisayar kullanılabilir hâle gelirse, güvenlik seviyesi seçilen ML-KEM parametre kümesine bağlı olacaktır.

### İleri Gizlilik

Hibrit yaklaşım, ileri gizlilik özelliklerini korur. Oturum anahtarları, hem geçici X25519 hem de geçici ML-KEM anahtar değişimlerinden türetilir. El sıkışmadan sonra X25519 veya ML-KEM geçici özel anahtarlarından herhangi biri imha edilirse, uzun vadeli statik anahtarlar ele geçirilmiş olsa bile geçmiş oturumların şifresi çözülemez.

IK pattern (IK deseni), ikinci mesaj (NSR) gönderildikten sonra tam ileri gizlilik (Noise Confidentiality level 5) sağlar.

## Tür Tercihleri

Gerçeklemeler birden fazla hibrit türünü desteklemeli ve karşılıklı desteklenen en güçlü varyant üzerinde anlaşmalıdır. Tercih sırası şöyle olmalıdır:

1. **MLKEM768_X25519** (Type 6) - Önerilen varsayılan, güvenlik ve performans arasında en iyi denge
2. **MLKEM1024_X25519** (Type 7) - Hassas uygulamalar için en yüksek güvenlik
3. **MLKEM512_X25519** (Type 5) - Kaynak kısıtlı senaryolar için temel kuantum sonrası güvenlik
4. **X25519** (Type 4) - Yalnızca klasik, uyumluluk için geri dönüş seçeneği

**Gerekçe:** MLKEM768_X25519, varsayılan olarak önerilir çünkü NIST Kategori 3 güvenliği (AES-192 eşdeğeri) sağlar; bu, kuantum bilgisayarlara karşı yeterli koruma olarak kabul edilirken makul mesaj boyutlarını da korur. MLKEM1024_X25519 daha yüksek güvenlik sağlar ancak önemli ölçüde artan ek yüke yol açar.

## Uygulama Notları

### Kütüphane Desteği

- **Java**: Bouncycastle kitaplığı sürüm 1.79 (Ağustos 2024) ve sonraki sürümler, gerekli tüm ML-KEM (post-kuantum anahtar kapsülleme mekanizması) varyantlarını ve SHA3/SHAKE işlevlerini destekler. FIPS 203 uyumluluğu için `org.bouncycastle.pqc.crypto.mlkem.MLKEMEngine` kullanın.
- **C++**: OpenSSL 3.5 (Nisan 2025) ve sonrası, EVP_KEM arayüzü üzerinden ML-KEM desteğini içerir. Bu, Nisan 2030'a kadar bakımda olan bir Uzun Süreli Destek (LTS) sürümüdür.
- **Go**: ML-KEM ve SHA3 için, Cloudflare'ın CIRCL kitaplığı da dahil olmak üzere çeşitli üçüncü taraf kitaplıklar mevcuttur.

### Geçiş Stratejisi

Gerçekleştirimler şunları yapmalıdır: 1. Geçiş döneminde yalnızca X25519 ve hibrit ML-KEM varyantlarının her ikisini de desteklemek 2. Her iki eş de desteklediğinde hibrit varyantları tercih etmek 3. Geriye dönük uyumluluk için yalnızca X25519’a fallback (otomatik yedek yönteme geçiş) olanağını sürdürmek 4. Varsayılan varyantı seçerken ağ bant genişliği kısıtlamalarını dikkate almak

### Paylaşılan Tunnels

Artan mesaj boyutları paylaşılan tunnel kullanımını etkileyebilir. Uygulamalar şunları dikkate almalıdır: - Mümkün olduğunda ek yükü dağıtmak için el sıkışmalarını toplu biçimde gerçekleştirmek - Saklanan durumu azaltmak için hibrit oturumlar için daha kısa geçerlilik süreleri kullanmak - Bant genişliği kullanımını izlemek ve parametreleri buna göre ayarlamak - Oturum kurulum trafiği için tıkanıklık kontrolü uygulamak

### Yeni Oturum Boyutu ile İlgili Hususlar

Daha büyük el sıkışma mesajları nedeniyle, gerçekleştirimlerin şunları yapması gerekebilir: - Oturum müzakeresi için arabellek boyutlarını artırmak (en az 4KB önerilir) - Daha yavaş bağlantılar için zaman aşımı değerlerini ayarlamak (~3-17x daha büyük mesajları hesaba katın) - NS/NSR mesajlarındaki yük verisi için sıkıştırmayı değerlendirmek - Taşıma katmanı gerektiriyorsa parçalama desteğini uygulamak

### Test ve Doğrulama

Gerçeklemeler şunları doğrulamalıdır: - Doğru ML-KEM anahtar üretimi, enkapsülleme ve dekapsülleme - kem_shared_key değerinin Noise KDF (Noise anahtar türetme fonksiyonu) içine doğru şekilde entegre edilmesi - İleti boyutu hesaplamalarının spesifikasyona uygun olması - Diğer I2P router gerçeklemeleriyle birlikte çalışabilirlik - ML-KEM mevcut olmadığında geri dönüş (fallback) davranışı

ML-KEM işlemleri için test vektörleri NIST [Cryptographic Algorithm Validation Program](https://csrc.nist.gov/Projects/cryptographic-algorithm-validation-program) programında mevcuttur.

## Sürüm Uyumluluğu

**I2P Sürüm Numaralandırması:** I2P iki paralel sürüm numarası kullanır: - **Router yayın sürümü**: 2.x.x biçimi (örn., 2.10.0 Eylül 2025'te yayımlandı) - **API/protokol sürümü**: 0.9.x biçimi (örn., 0.9.67 router 2.10.0'a karşılık gelir)

Bu belirtim, router sürümü 2.10.0 ve sonrasına karşılık gelen 0.9.67 protokol sürümüne atıfta bulunur.

**Uyumluluk Matrisi:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Implementation</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">ML-KEM Support</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2pd</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.58.0+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Full (512/768/1024)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deployed September 2025</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Java I2P</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67 / 2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Not yet</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Planned for future release</td>
    </tr>
  </tbody>
</table>
## Referanslar

- **[ECIES]**: [ECIES-X25519-AEAD-Ratchet Teknik Şartnamesi](/docs/specs/ecies/)
- **[Prop169]**: [Öneri 169: Kuantum Sonrası Kriptografi](/proposals/169-pq-crypto/)
- **[FIPS203]**: [NIST FIPS 203 - ML-KEM Standardı](https://csrc.nist.gov/pubs/fips/203/final)
- **[FIPS202]**: [NIST FIPS 202 - SHA-3 Standardı](https://csrc.nist.gov/pubs/fips/202/final)
- **[Noise]**: [Noise Protokol Çerçevesi](https://noiseprotocol.org/noise.html)
- **[COMMON]**: [Ortak Yapılar Teknik Şartnamesi](/docs/specs/common-structures/)
- **[RFC7539]**: [RFC 7539 - ChaCha20 ve Poly1305](https://www.rfc-editor.org/rfc/rfc7539)
- **[RFC5869]**: [RFC 5869 - HKDF](https://www.rfc-editor.org/rfc/rfc5869)
- **[OpenSSL]**: [OpenSSL 3.5 ML-KEM Dokümantasyonu](https://docs.openssl.org/3.5/man7/EVP_KEM-ML-KEM/)
- **[Bouncycastle]**: [Bouncycastle Java Kriptografi Kütüphanesi](https://www.bouncycastle.org/)

---
