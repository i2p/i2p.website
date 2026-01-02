---
title: "NTCP2 Taşıma"
description: "router'lar arası bağlantılar için Noise (Noise protokol çerçevesi) tabanlı TCP taşıma protokolü"
slug: "ntcp2"
lastUpdated: "2025-10"
accurateFor: "0.9.66"
type: docs
---

## Genel Bakış

NTCP2, eski NTCP taşıma protokolünün yerini, trafik parmak izi tespitine dirençli, uzunluk alanlarını şifreleyen ve modern şifre takımlarını destekleyen Noise tabanlı bir el sıkışmasıyla alır. Router'lar, I2P ağındaki iki zorunlu taşıma protokolü olarak NTCP2'yi SSU2 ile birlikte çalıştırabilir. NTCP (sürüm 1) 0.9.40'da (Mayıs 2019) kullanımı önerilmez hale getirildi ve 0.9.50'de (Mayıs 2021) tamamen kaldırıldı.

## Noise Protokol Çerçevesi

NTCP2, I2P'ye özgü uzantılarla birlikte Noise Protocol Framework (Noise Protokol Çatısı) [Revizyon 33, 2017-10-04](https://noiseprotocol.org/noise.html) kullanır:

- **Desen**: `Noise_XK_25519_ChaChaPoly_SHA256`
- **Genişletilmiş Tanımlayıcı**: `Noise_XKaesobfse+hs2+hs3_25519_ChaChaPoly_SHA256` (KDF (Anahtar Türetme Fonksiyonu) başlatma için)
- **DH İşlevi**: X25519 (RFC 7748) - 32 baytlık anahtarlar, little-endian kodlama
- **Şifreleme**: AEAD_CHACHA20_POLY1305 (RFC 7539/RFC 8439)
  - 12 baytlık nonce (tek seferlik değer): ilk 4 bayt sıfır, son 8 bayt sayaç (little-endian)
  - Maksimum nonce değeri: 2^64 - 2 (bağlantı 2^64 - 1'e ulaşmadan önce sonlandırılmalıdır)
- **Özet Fonksiyonu**: SHA-256 (32 bayt çıktı)
- **MAC (Mesaj Doğrulama Kodu)**: Poly1305 (16 bayt kimlik doğrulama etiketi)

### I2P'ye Özgü Uzantılar

1. **AES ile Gizleme**: Bob'un router karması ve yayımlanmış IV (başlatma vektörü) kullanılarak AES-256-CBC ile şifrelenen geçici anahtarlar
2. **Rastgele Dolgu**: Mesaj 1-2'de açık metin dolgusu (kimliği doğrulanmış), mesaj 3 ve sonrasında AEAD (authenticated encryption with associated data - ilişkili verilerle kimlik doğrulamalı şifreleme) dolgusu (şifrelenmiş)
3. **SipHash-2-4 ile Uzunluk Gizleme**: İki baytlık çerçeve uzunlukları SipHash çıktısı ile XOR'lanır
4. **Çerçeve Yapısı**: Veri aşaması için başında uzunluk alanı bulunan çerçeveler (TCP akış uyumluluğu)
5. **Blok Tabanlı Yükler**: Tür tanımlı bloklarla yapılandırılmış veri biçimi

## El Sıkışma Akışı

```
Alice (Initiator)             Bob (Responder)
SessionRequest  ──────────────────────►
                ◄────────────────────── SessionCreated
SessionConfirmed ──────────────────────►
```
### Üç Mesajlı El Sıkışma

1. **SessionRequest** - Alice'in gizlileştirilmiş geçici anahtarı, seçenekler, dolgu ipuçları
2. **SessionCreated** - Bob'un gizlileştirilmiş geçici anahtarı, şifrelenmiş seçenekler, dolgu
3. **SessionConfirmed** - Alice'in şifrelenmiş statik anahtarı ve RouterInfo (iki AEAD çerçevesi)

### Noise Mesaj Kalıpları

```
XK(s, rs):           Authentication   Confidentiality
  <- s               (Bob's static key known in advance)
  -> e, es                  0                2
  <- e, ee                  2                1
  -> s, se                  2                5
  <-                        2                5
```
**Kimlik Doğrulama Seviyeleri:** - 0: Kimlik doğrulama yok (herhangi bir taraf göndermiş olabilir) - 2: Gönderici kimlik doğrulaması, anahtar ele geçirilmesine dayalı kimliğe bürünmeye (KCI) karşı dayanıklıdır

**Gizlilik Düzeyleri:** - 1: Geçici alıcı (ileri gizlilik, alıcı kimlik doğrulaması yok) - 2: Bilinen alıcı, yalnızca gönderenin ele geçirilmesi durumunda ileri gizlilik - 5: Güçlü ileri gizlilik (geçici-geçici + geçici-statik DH)

## Mesaj Spesifikasyonları

### Anahtar Gösterimi

- `RH_A` = Alice için Router Hash (32 bayt, SHA-256)
- `RH_B` = Bob için Router Hash (32 bayt, SHA-256)
- `||` = bitiştirme operatörü
- `byte(n)` = değeri n olan tek bayt
- Aksi belirtilmedikçe tüm çok baytlı tamsayılar **big-endian** (büyük-sonlu) düzenindedir
- X25519 anahtarları **little-endian** (küçük-sonlu) (32 bayt)

### Kimliği Doğrulanmış Şifreleme (ChaCha20-Poly1305)

**Şifreleme İşlevi:**

```
AEAD_ChaCha20_Poly1305(key, nonce, associatedData, plaintext)
  → (ciphertext || MAC)
```
**Parametreler:** - `key`: KDF (Anahtar Türetme Fonksiyonu) çıktısı 32 baytlık şifreleme anahtarı - `nonce`: 12 bayt (4 sıfır bayt + 8 baytlık sayaç, little-endian (küçük uca dayalı bayt sıralaması)) - `associatedData`: el sıkışma aşamasında 32 baytlık özet; veri aşamasında sıfır uzunlukta - `plaintext`: Şifrelenecek veri (0+ bayt)

**Çıktı:** - Şifreli metin: Düz metinle aynı uzunlukta - MAC: 16 bayt (Poly1305 kimlik doğrulama etiketi)

**Nonce (tek kullanımlık sayı) Yönetimi:** - Her bir şifreleme örneği için sayaç 0'dan başlar - O yöndeki her AEAD (kimliği doğrulanmış ek verili şifreleme) işlemi için artırılır - Veri aşamasında Alice→Bob ve Bob→Alice için ayrı sayaçlar vardır - Sayaç 2^64 - 1 değerine ulaşmadan önce bağlantı sonlandırılmalıdır

## Mesaj 1: SessionRequest (oturum isteği)

Alice, Bob ile bir bağlantı başlatır.

**Noise İşlemleri**: `e, es` (geçici anahtar oluşturma ve değişimi)

### Ham Biçim

```
+----+----+----+----+----+----+----+----+
|                                       |
+    AES-256-CBC Encrypted X (32B)      +
|    Key: RH_B, IV: Bob's published IV  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+    ChaChaPoly Frame (48 bytes)        +
|    Plaintext: 32B (X + options)       |
+    k from KDF-1, n=0, ad=h            +
|                                       |
+----+----+----+----+----+----+----+----+
|    Cleartext Padding (optional)       |
+    Length specified in options         +
|    0 to 65535 - 80 bytes              |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
**Boyut Kısıtları:** - Minimum: 80 bayt (32 AES + 48 AEAD) - Maksimum: toplam 65535 bayt - **Özel durum**: "NTCP" adreslerine bağlanırken en fazla 287 bayt (sürüm algılama)

### Şifresi Çözülmüş İçerik

```
+----+----+----+----+----+----+----+----+
|                                       |
+    X (Alice ephemeral public key)     +
|    32 bytes, X25519, little-endian    |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|           Options Block               |
+             (16 bytes)                +
|                                       |
+----+----+----+----+----+----+----+----+
|    Cleartext Padding (optional)       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
### Seçenekler Bloğu (16 bayt, big-endian (yüksek anlamlı bayt önce))

```
+----+----+----+----+----+----+----+----+
| id | ver|  padLen | m3p2len | Rsvd(0) |
+----+----+----+----+----+----+----+----+
|        tsA        |   Reserved (0)    |
+----+----+----+----+----+----+----+----+

id      : 1 byte  - Network ID (2 for mainnet, 16-254 for testnets)
ver     : 1 byte  - Protocol version (currently 2)
padLen  : 2 bytes - Padding length in this message (0-65455)
m3p2len : 2 bytes - Length of SessionConfirmed part 2 frame
Rsvd    : 2 bytes - Reserved, set to 0
tsA     : 4 bytes - Unix timestamp (seconds since epoch)
Reserved: 4 bytes - Reserved, set to 0
```
**Kritik Alanlar:** - **Ağ Kimliği** (0.9.42'den beri): Ağlar arası bağlantıların hızlı reddedilmesi - **m3p2len**: 3. iletinin 2. bölümünün tam boyutu (gönderildiğinde eşleşmelidir)

### Anahtar Türetme Fonksiyonu (KDF-1)

**Başlatma Protokolü:**

```
protocol_name = "Noise_XKaesobfse+hs2+hs3_25519_ChaChaPoly_SHA256"
h = SHA256(protocol_name)
ck = h  // Chaining key initialized to hash
```
**MixHash İşlemleri:**

```
h = SHA256(h)                    // Null prologue
h = SHA256(h || rs)              // Bob's static key (known)
h = SHA256(h || e.pubkey)        // Alice's ephemeral key X
// h is now the associated data for message 1 AEAD
```
**MixKey İşlemi (es deseni):**

```
dh_result = X25519(Alice.ephemeral_private, Bob.static_public)
temp_key = HMAC-SHA256(ck, dh_result)
ck = HMAC-SHA256(temp_key, byte(0x01))
k = HMAC-SHA256(temp_key, ck || byte(0x02))
// k is the cipher key for message 1
// ck is retained for message 2 KDF
```
### Gerçekleştirim Notları

1. **AES Obfuscation (gizleme)**: Yalnızca DPI (Derin Paket İnceleme) direnci için kullanılır; Bob'un router hash'i ve IV'si olan herkes X'in şifresini çözebilir
2. **Replay Prevention**: Bob, X değerlerini (veya şifrelenmiş eşdeğerlerini) en az 2*D saniye boyunca önbelleğe almalıdır (D = maksimum saat sapması)
3. **Timestamp Validation**: Bob, |tsA - current_time| > D olan bağlantıları reddetmelidir (genellikle D = 60 saniye)
4. **Curve Validation**: Bob, X'in geçerli bir X25519 noktası olduğunu doğrulamalıdır
5. **Fast Rejection**: Bob, şifre çözmeden önce X[31] & 0x80 == 0 olup olmadığını kontrol edebilir (geçerli X25519 anahtarlarında MSB (en anlamlı bit) sıfırdır)
6. **Error Handling**: Herhangi bir başarısızlıkta, Bob rastgele bir zaman aşımı ve rastgele bayt okumasının ardından TCP RST ile kapatır
7. **Buffering**: Alice, verimlilik için tüm mesajı (padding (doldurma) dahil) tek seferde boşaltmalıdır

## Mesaj 2: SessionCreated (oturum oluşturuldu)

Bob, Alice'e yanıt verir.

**Noise İşlemleri**: `e, ee` (geçici-geçici DH)

### Ham Biçim

```
+----+----+----+----+----+----+----+----+
|                                       |
+    AES-256-CBC Encrypted Y (32B)      +
|    Key: RH_B, IV: AES state from msg1 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+    ChaChaPoly Frame (48 bytes)        +
|    Plaintext: 32B (Y + options)       |
+    k from KDF-2, n=0, ad=h            +
|                                       |
+----+----+----+----+----+----+----+----+
|    Cleartext Padding (optional)       |
+    Length specified in options         +
|    0 to 65535 - 80 bytes              |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
### Şifresi Çözülmüş İçerik

```
+----+----+----+----+----+----+----+----+
|                                       |
+    Y (Bob ephemeral public key)       +
|    32 bytes, X25519, little-endian    |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|           Options Block               |
+             (16 bytes)                +
|                                       |
+----+----+----+----+----+----+----+----+
|    Cleartext Padding (optional)       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
### Seçenekler Bloğu (16 bayt, big-endian (büyük uçlu bayt sıralaması))

```
+----+----+----+----+----+----+----+----+
| Rsvd(0) | padLen  |   Reserved (0)    |
+----+----+----+----+----+----+----+----+
|        tsB        |   Reserved (0)    |
+----+----+----+----+----+----+----+----+

Rsvd    : 2 bytes - Reserved, set to 0
padLen  : 2 bytes - Padding length in this message
Reserved: 10 bytes - Reserved, set to 0
tsB     : 4 bytes - Unix timestamp (seconds since epoch)
```
### Anahtar Türetme Fonksiyonu (KDF-2)

**MixHash İşlemleri:**

```
h = SHA256(h || encrypted_payload_msg1)  // 32-byte ciphertext
if (msg1_padding_length > 0):
    h = SHA256(h || padding_from_msg1)
h = SHA256(h || e.pubkey)                // Bob's ephemeral key Y
// h is now the associated data for message 2 AEAD
```
**MixKey İşlemi (ee deseni):**

```
dh_result = X25519(Bob.ephemeral_private, Alice.ephemeral_public)
temp_key = HMAC-SHA256(ck, dh_result)
ck = HMAC-SHA256(temp_key, byte(0x01))
k = HMAC-SHA256(temp_key, ck || byte(0x02))
// k is the cipher key for message 2
// ck is retained for message 3 KDF
```
**Bellek Temizliği:**

```
// Overwrite ephemeral keys after ee DH
Alice.ephemeral_public = zeros(32)
Alice.ephemeral_private = zeros(32)  // Bob side
Bob.received_ephemeral = zeros(32)    // Bob side
```
### Uygulama Notları

1. **AES Zincirleme**: Y şifrelemesi, 1. mesajdan (sıfırlanmadan) AES-CBC durumunu kullanır
2. **Replay Saldırılarını Önleme**: Alice en az 2*D saniye boyunca Y değerlerini önbelleğe almalıdır
3. **Zaman Damgası Doğrulaması**: Alice, |tsB - current_time| > D ise reddetmelidir
4. **Eğri Doğrulaması**: Alice, Y'nin geçerli bir X25519 noktası olduğunu doğrulamalıdır
5. **Hata İşleme**: Herhangi bir hata durumunda Alice, bağlantıyı TCP RST ile kapatır
6. **Tamponlama**: Bob, tüm mesajı tek seferde tampondan boşaltmalıdır

## Mesaj 3: SessionConfirmed

Alice oturumu onaylar ve RouterInfo (router bilgi kaydı) gönderir.

**Noise İşlemleri**: `s, se` (statik anahtarın açıklanması ve statik-geçici DH)

### İki Parçalı Yapı

Mesaj 3 **iki ayrı AEAD (ilişkili verili kimlik doğrulamalı şifreleme) çerçeveden** oluşur:

1. **Bölüm 1**: Alice'in şifrelenmiş statik anahtarını içeren sabit 48 baytlık çerçeve
2. **Bölüm 2**: RouterInfo (router bilgisi), seçenekler ve dolgu içeren değişken uzunluklu çerçeve

### Ham Biçim

```
+----+----+----+----+----+----+----+----+
|    ChaChaPoly Frame 1 (48 bytes)      |
+    Plaintext: Alice static key (32B)  +
|    k from KDF-2, n=1, ad=h            |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+    ChaChaPoly Frame 2 (variable)      +
|    Length specified in msg1.m3p2len   |
+    k from KDF-3, n=0, ad=h            +
|    Plaintext: RouterInfo + padding    |
+                                       +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
**Boyut Kısıtlamaları:** - Bölüm 1: Tam olarak 48 bayt (32 açık metin + 16 MAC) - Bölüm 2: Uzunluk, mesaj 1'deki m3p2len alanında belirtilir - Toplam azami: 65535 bayt (bölüm 1 azami 48, dolayısıyla bölüm 2 azami 65487)

### Şifresi Çözülmüş İçerik

**Bölüm 1:**

```
+----+----+----+----+----+----+----+----+
|                                       |
+    S (Alice static public key)        +
|    32 bytes, X25519, little-endian    |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
**Bölüm 2:**

```
+----+----+----+----+----+----+----+----+
|    Block: RouterInfo (required)       |
+    Type=2, contains Alice's RI         +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
|    Block: Options (optional)          |
+    Type=1, padding parameters          +
|                                       |
+----+----+----+----+----+----+----+----+
|    Block: Padding (optional)          |
+    Type=254, random data               +
|    MUST be last block if present      |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
### Anahtar Türetme Fonksiyonu (KDF-3)

**Bölüm 1 (s deseni):**

```
h = SHA256(h || encrypted_payload_msg2)  // 32-byte ciphertext
if (msg2_padding_length > 0):
    h = SHA256(h || padding_from_msg2)

// Encrypt static key with message 2 cipher key
ciphertext = AEAD_ChaCha20_Poly1305(k_msg2, n=1, h, Alice.static_public)
h = SHA256(h || ciphertext)  // 48 bytes (32 + 16)
// h is now the associated data for message 3 part 2
```
**Bölüm 2 (se pattern):**

```
dh_result = X25519(Alice.static_private, Bob.ephemeral_public)
temp_key = HMAC-SHA256(ck, dh_result)
ck = HMAC-SHA256(temp_key, byte(0x01))
k = HMAC-SHA256(temp_key, ck || byte(0x02))
// k is the cipher key for message 3 part 2
// ck is retained for data phase KDF

ciphertext = AEAD_ChaCha20_Poly1305(k, n=0, h, payload)
h = SHA256(h || ciphertext)
// h is retained for SipHash KDF
```
**Bellek Temizleme:**

```
// Overwrite Bob's ephemeral key after se DH
Alice.received_ephemeral = zeros(32)  // Alice side
Bob.ephemeral_public = zeros(32)       // Bob side
Bob.ephemeral_private = zeros(32)      // Bob side
```
### Uygulama Notları

1. **RouterInfo Doğrulaması**: Bob, imzayı, zaman damgasını ve anahtar tutarlılığını doğrulamalıdır
2. **Anahtar Eşleşmesi**: Bob, 1. bölümdeki Alice'in statik anahtarının RouterInfo'daki anahtarla eşleştiğini doğrulamalıdır
3. **Statik Anahtarın Konumu**: NTCP veya NTCP2 RouterAddress içinde eşleşen "s" parametresine bakın
4. **Blok Sırası**: RouterInfo ilk, Options ikinci (varsa), Padding en son (varsa) olmalıdır
5. **Uzunluk Planlaması**: Alice, mesaj 1'deki m3p2len'in 2. bölümün uzunluğuyla tam olarak eşleştiğinden emin olmalıdır
6. **Arabelleğe Alma**: Alice, her iki bölümü tek bir TCP gönderimi olarak birlikte flush (tamponu boşaltmak) etmelidir
7. **İsteğe Bağlı Zincirleme**: Alice, verimlilik için hemen bir data phase frame (veri aşaması çerçevesi) ekleyebilir

## Veri Aşaması

El sıkışması tamamlandıktan sonra, tüm iletiler gizlenmiş uzunluk alanlarına sahip, değişken uzunluklu AEAD (İlişkili verili kimlik doğrulamalı şifreleme) çerçeveleri kullanır.

### Anahtar Türetme Fonksiyonu (Veri Aşaması)

**Split İşlevi (Noise):**

```
// Generate transmit and receive keys
zerolen = ""  // Zero-length byte array
temp_key = HMAC-SHA256(ck, zerolen)

// Alice transmits to Bob
k_ab = HMAC-SHA256(temp_key, byte(0x01))

// Bob transmits to Alice  
k_ba = HMAC-SHA256(temp_key, k_ab || byte(0x02))

// Cleanup
ck = zeros(32)
temp_key = zeros(32)
```
**SipHash Anahtar Türetimi:**

```
// Generate additional symmetric key for SipHash
ask_master = HMAC-SHA256(temp_key, "ask" || byte(0x01))

// "siphash" is 7 bytes US-ASCII
temp_key2 = HMAC-SHA256(ask_master, h || "siphash")
sip_master = HMAC-SHA256(temp_key2, byte(0x01))

// Alice to Bob SipHash keys
temp_key3 = HMAC-SHA256(sip_master, zerolen)
sipkeys_ab = HMAC-SHA256(temp_key3, byte(0x01))
sipk1_ab = sipkeys_ab[0:7]   // 8 bytes, little-endian
sipk2_ab = sipkeys_ab[8:15]  // 8 bytes, little-endian
sipiv_ab = sipkeys_ab[16:23] // 8 bytes, IV

// Bob to Alice SipHash keys
sipkeys_ba = HMAC-SHA256(temp_key3, sipkeys_ab || byte(0x02))
sipk1_ba = sipkeys_ba[0:7]   // 8 bytes, little-endian
sipk2_ba = sipkeys_ba[8:15]  // 8 bytes, little-endian
sipiv_ba = sipkeys_ba[16:23] // 8 bytes, IV
```
### Çerçeve Yapısı

```
+----+----+----+----+----+----+----+----+
|Obfs Len |                             |
+----+----+    ChaChaPoly Frame         +
|    Encrypted Block Data               |
+    k_ab (Alice→Bob) or k_ba (Bob→Alice)|
|    Nonce starts at 0, increments      |
+    No associated data (empty string)  +
|                                       |
~           .   .   .                   ~
|                                       |
+----+----+----+----+----+----+----+----+
|    Poly1305 MAC (16 bytes)            |
+----+----+----+----+----+----+----+----+
```
**Çerçeve Kısıtlamaları:** - Minimum: 18 bayt (2 gizlenmiş uzunluk + 0 düz metin + 16 MAC) - Maksimum: 65537 bayt (2 gizlenmiş uzunluk + 65535 çerçeve) - Önerilen: çerçeve başına birkaç KB (alıcı gecikmesini en aza indirmek için)

### SipHash ile Uzunluk Gizleme

**Amaç**: DPI'nin çerçeve sınırlarını tespit etmesini önlemek

**Algoritma:**

```
// Initialization (per direction)
IV[0] = sipiv  // From KDF

// For each frame:
IV[n] = SipHash-2-4(sipk1, sipk2, IV[n-1])
Mask[n] = IV[n][0:1]  // First 2 bytes of IV
ObfuscatedLength = ActualLength XOR Mask[n]

// Send 2-byte ObfuscatedLength, then ActualLength bytes
```
**Kod çözme:**

```
// Receiver maintains identical IV chain
IV[n] = SipHash-2-4(sipk1, sipk2, IV[n-1])
Mask[n] = IV[n][0:1]
ActualLength = ObfuscatedLength XOR Mask[n]
// Read ActualLength bytes (includes 16-byte MAC)
```
**Notlar:** - Her yön için ayrı IV (başlatma vektörü) zincirleri (Alice→Bob ve Bob→Alice) - SipHash uint64 döndürürse, maske olarak en düşük anlamlı 2 baytı kullanın - uint64 değerini bir sonraki IV'ye little-endian (küçük endian) baytlar olarak dönüştürün

### Blok Biçimi

Her çerçeve sıfır veya daha fazla blok içerir:

```
+----+----+----+----+----+----+----+----+
|Type| Length  |       Data              |
+----+----+----+                        +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type  : 1 byte  - Block type identifier
Length: 2 bytes - Big-endian, data size (0-65516)
Data  : Variable length payload
```
**Boyut Sınırları:** - Maksimum çerçeve: 65535 bayt (MAC dahil) - Maksimum blok alanı: 65519 bayt (çerçeve - 16 baytlık MAC) - Maksimum tek blok: 65519 bayt (3 baytlık başlık + 65516 veri)

### Blok Türleri

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DateTime</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Time synchronization (4-byte timestamp)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Options</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Padding parameters, dummy traffic</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo delivery/flooding</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2NP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2NP message with shortened header</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Termination</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Explicit connection close</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">224-253</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental features</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">254</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Padding</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Random padding (must be last)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">255</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Future extensions</td></tr>
  </tbody>
</table>
**Blok Sıralama Kuralları:** - **Mesaj 3 bölüm 2**: RouterInfo, Options (isteğe bağlı), Padding (isteğe bağlı) - Başka tür YOK - **Veri aşaması**: Şunlar dışında herhangi bir sırayla:   - Padding varsa MUTLAKA son blok olmalıdır   - Termination varsa MUTLAKA (Padding hariç) son blok olmalıdır - Çerçeve başına birden fazla I2NP bloğuna izin verilir - Çerçeve başına birden fazla Padding bloğuna İZİN VERİLMEZ

### Blok Türü 0: DateTime

Saat sapması tespiti için zaman senkronizasyonu.

```
+----+----+----+----+----+----+----+
| 0  |    4    |     timestamp     |
+----+----+----+----+----+----+----+

Type     : 0
Length   : 4 (big-endian)
Timestamp: 4 bytes, Unix seconds (big-endian)
```
**Uygulama**: Saat ofsetinin birikmesini önlemek için en yakın saniyeye yuvarlayın.

### Blok Türü 1: Seçenekler

Dolgu ve trafik şekillendirme parametreleri.

```
+----+----+----+----+----+----+----+----+
| 1  |  size   |tmin|tmax|rmin|rmax|tdmy|
+----+----+----+----+----+----+----+----+
|tdmy|  rdmy   |  tdelay |  rdelay |    |
+----+----+----+----+----+----+----+    +
|         more_options (TBD)            |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type  : 1
Length: 12+ bytes (big-endian)
```
**Dolgu Oranları** (4.4 sabit noktalı sayı, değer/16.0): - `tmin`: İletimde minimum dolgu oranı (0.0 - 15.9375) - `tmax`: İletimde maksimum dolgu oranı (0.0 - 15.9375) - `rmin`: Alımda minimum dolgu oranı (0.0 - 15.9375) - `rmax`: Alımda maksimum dolgu oranı (0.0 - 15.9375)

**Örnekler:** - 0x00 = 0% dolgu - 0x01 = 6.25% dolgu - 0x10 = 100% dolgu (1:1 oranı) - 0x80 = 800% dolgu (8:1 oranı)

**Sahte Trafik:** - `tdmy`: Göndermeye istekli olunan azami değer (2 bayt, bayt/sn ortalaması) - `rdmy`: Alınması talep edilen miktar (2 bayt, bayt/sn ortalaması)

**Gecikme Ekleme:** - `tdelay`: Eklemeye razı olunan en yüksek değer (2 bayt, milisaniye cinsinden ortalama) - `rdelay`: Talep edilen gecikme (2 bayt, milisaniye cinsinden ortalama)

**Kılavuzlar:** - Min değerler istenen trafik analizi direncini gösterir - Max değerler bant genişliği kısıtlarını gösterir - Gönderici alıcının maksimumuna uymalıdır - Gönderici kısıtlar dahilinde alıcının minimumuna uyabilir - Herhangi bir yaptırım mekanizması yoktur; uygulamalar farklılık gösterebilir

### Blok Türü 2: RouterInfo (router bilgisi)

netDb'nin doldurulması ve yayılması için RouterInfo iletimi.

```
+----+----+----+----+----+----+----+----+
| 2  |  size   |flg |    RouterInfo     |
+----+----+----+----+                   +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type : 2
Length: Flag (1 byte) + RouterInfo size
Flag : Bit 0 = flood request (1) or local store (0)
       Bits 1-7 = Reserved, set to 0
```
**Kullanım:**

**Mesaj 3 Bölüm 2'de** (el sıkışması): - Alice RouterInfo'yu (Router bilgisi) Bob'a gönderir - Flood bit (ağa yayma biti) genellikle 0 (yerel depolama) - RouterInfo gzip ile sıkıştırılmamıştır

**Veri Aşamasında:** - Taraflardan herhangi biri güncellenmiş RouterInfo'sunu gönderebilir - Flood bit = 1: floodfill dağıtımını iste (alıcı floodfill ise) - Flood bit = 0: Yalnızca yerel netdb depolaması

**Doğrulama Gereksinimleri:** 1. İmza türünün desteklendiğini doğrulayın 2. RouterInfo (yöneltici bilgi kaydı) imzasını doğrulayın 3. Zaman damgasının kabul edilebilir sınırlar içinde olduğunu doğrulayın 4. El sıkışması için: Statik anahtarın NTCP2 adresinin "s" parametresiyle eşleştiğini doğrulayın 5. Veri aşaması için: router hash'in oturum eşiyle eşleştiğini doğrulayın 6. Yalnızca yayımlanmış adresleri olan RouterInfo'ları dağıt

**Notlar:** - ACK mekanizması yok (gerektiğinde yanıt belirteci ile I2NP DatabaseStore kullanın) - Üçüncü taraf RouterInfos içerebilir (floodfill kullanımı) - gzip ile sıkıştırılmamıştır (I2NP DatabaseStore'un aksine)

### Blok Türü 3: I2NP Mesajı

Kısaltılmış 9 baytlık başlığa sahip I2NP mesajı.

```
+----+----+----+----+----+----+----+----+
| 3  |  size   |type|    msg_id         |
+----+----+----+----+----+----+----+----+
|   expiration  |     I2NP payload      |
+----+----+----+                        +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type      : 3
Length    : 9 + payload_size (big-endian)
Type      : 1 byte, I2NP message type
Msg_ID    : 4 bytes, big-endian, I2NP message ID
Expiration: 4 bytes, big-endian, Unix timestamp (seconds)
Payload   : I2NP message body (length = size - 9)
```
**NTCP1'e göre farklar:** - Bitiş zamanı: 4 bayt (saniye) vs 8 bayt (milisaniye) - Uzunluk: Çıkarıldı (blok uzunluğundan türetilebilir) - Sağlama toplamı: Çıkarıldı (AEAD (ilişkili verilerle kimlik doğrulamalı şifreleme) bütünlük sağlar) - Başlık: 9 bayt vs 16 bayt (%44 azalma)

**Parçalama:** - I2NP mesajları bloklar arasında kesinlikle parçalanmamalıdır - I2NP mesajları çerçeveler arasında kesinlikle parçalanmamalıdır - Çerçeve başına birden fazla I2NP bloğuna izin verilir

### Blok Tipi 4: Sonlandırma

Gerekçe koduyla bağlantıyı açıkça kapatma.

```
+----+----+----+----+----+----+----+----+
| 4  |  size   |  valid_frames_recv    |
+----+----+----+----+----+----+----+----+
| (continued) |rsn |   additional_data   |
+----+----+----+----+                   +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type            : 4
Length          : 9+ bytes (big-endian)
Valid_Frames_Recv: 8 bytes, big-endian (receive nonce value)
                  0 if error in handshake phase
Reason          : 1 byte (see table below)
Additional_Data : Optional (format unspecified, for debugging)
```
**Neden Kodları:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Reason</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Phase</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Normal close / unspecified</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Termination received</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Idle timeout</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Router shutdown</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data phase AEAD failure</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Incompatible options</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Incompatible signature type</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Clock skew</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Padding violation</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">9</td><td style="border:1px solid var(--color-border); padding:0.5rem;">AEAD framing error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Payload format error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Message 1 error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Message 2 error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">13</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Message 3 error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">14</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Intra-frame read timeout</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo signature verification fail</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">16</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Static key parameter mismatch</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">17</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Banned</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td></tr>
  </tbody>
</table>
**Kurallar:** - Sonlandırma MUTLAKA çerçevede dolgu olmayan son blok olmalıdır - Çerçeve başına en fazla bir sonlandırma bloğu - Gönderen gönderdikten sonra bağlantıyı kapatmalıdır - Alıcı aldıktan sonra bağlantıyı kapatmalıdır

**Hata İşleme:** - El sıkışma hataları: Genellikle TCP RST ile kapatılır (sonlandırma bloğu yok) - Veri aşaması AEAD hataları: Rastgele zaman aşımı + rastgele okuma, ardından sonlandırma gönder - Güvenlik prosedürleri için "AEAD Error Handling" bölümüne bakın

### Blok Türü 254: Dolgu

Trafik analizine karşı dayanıklılık için rastgele dolgu.

```
+----+----+----+----+----+----+----+----+
|254 |  size   |     random_data       |
+----+----+----+                        +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type: 254
Length: 0-65516 bytes (big-endian)
Data: Cryptographically random bytes
```
**Kurallar:** - Varsa, padding (dolgu) çerçevede son blok MUTLAKA olmalıdır - Sıfır uzunluklu padding'e izin verilir - Her çerçevede yalnızca bir padding bloğuna izin verilir - Yalnızca padding içeren çerçevelere izin verilir - Options bloğunda müzakere edilen parametrelere uyulmalıdır

**İletiler 1-2'de Dolgu:** - AEAD (ilişkili verilerle kimlik doğrulamalı şifreleme) çerçevesinin dışında (açık metin) - Sonraki iletinin hash zincirine dahil edilir (kimliği doğrulanmış) - Sonraki iletide AEAD başarısız olduğunda kurcalama saptanır

**Mesaj 3+ ve Veri Aşamasında Dolgu:** - AEAD (kimliği doğrulamalı ve ilişkili verili şifreleme) çerçevesinin içinde (şifrelenmiş ve kimlik doğrulaması yapılmış) - Trafik şekillendirme ve boyut gizleme için kullanılır

## AEAD (ek verili kimliği doğrulanmış şifreleme) Hata İşleme

**Kritik Güvenlik Gereksinimleri:**

### El Sıkışma Aşaması (Mesajlar 1-3)

**Bilinen Mesaj Boyutu:** - Mesaj boyutları önceden belirlenir veya önceden belirtilir - AEAD (ilişkili verili doğrulanmış şifreleme) kimlik doğrulama hatası şüpheye yer bırakmaz

**Bob'un Mesaj 1 başarısızlığına yanıtı:** 1. Rastgele bir zaman aşımı ayarla (aralık uygulamaya bağlıdır, 100-500ms önerilir) 2. Rastgele sayıda bayt oku (aralık uygulamaya bağlıdır, 1KB-64KB önerilir) 3. Bağlantıyı TCP RST ile kapat (yanıt yok) 4. Kaynak IP'yi geçici olarak kara listeye al 5. Uzun vadeli yasaklamalar için tekrarlanan hataları izle

**Alice'in Mesaj 2 Hatasına Yanıtı:** 1. Bağlantıyı hemen TCP RST ile kapat 2. Bob'a yanıt verme

**Bob'un Mesaj 3 Hatasına Yanıtı:** 1. Bağlantıyı TCP RST ile hemen kapat 2. Alice'e yanıt verme

### Veri Aşaması

**Gizlenmiş Mesaj Boyutu:** - Uzunluk alanı SipHash (anahtarlı karma fonksiyonu) ile gizlenmiştir - Geçersiz uzunluk ya da AEAD (ek verilerle kimliği doğrulanmış şifreleme) hatası şunlara işaret edebilir:   - Saldırgan yoklaması   - Ağ bozulması   - Senkronu bozulmuş SipHash IV   - Kötücül eş

**AEAD (İlişkili Verili Kimlik Doğrulamalı Şifreleme) veya Uzunluk Hatasına Yanıt:** 1. Rastgele bir zaman aşımı ayarla (100-500ms önerilir) 2. Rastgele miktarda bayt oku (1KB-64KB önerilir) 3. Neden kodu 4 (AEAD başarısızlığı) veya 9 (çerçeveleme hatası) ile bir sonlandırma bloğu gönder 4. Bağlantıyı kapat

**Decryption Oracle'ın (saldırganın hata geri bildirimlerinden yararlanarak şifre çözmeye dair bilgi çıkarabildiği sorgulanabilir bileşen) Önlenmesi:** - Rastgele bir zaman aşımı gerçekleşmeden önce eşe hata türünü asla açıklamayın - AEAD kontrolünden önce uzunluk doğrulamasını asla atlamayın - Geçersiz uzunluğu AEAD hatasıyla aynı şekilde ele alın - Her iki hata için de aynı hata işleme yolunu kullanın

**Uygulama ile ilgili değerlendirmeler:** - Bazı gerçekleştirmeler, AEAD (Authenticated Encryption with Associated Data — ilişkili verili kimlik doğrulamalı şifreleme) hataları seyrek görülüyorsa çalışmaya devam edebilir - Hatalar tekrarlandığında sonlandırın (önerilen eşik: saatte 3-5 hata) - Hata kurtarma ile güvenlik arasında denge kurun

## Yayınlanan RouterInfo (router bilgisi)

### Router Adres Biçimi

NTCP2 desteği, belirli seçeneklere sahip yayımlanmış RouterAddress girdileri aracılığıyla duyurulur.

**Taşıma Stili:** - `"NTCP2"` - Bu bağlantı noktasında yalnızca NTCP2 - `"NTCP"` - Bu bağlantı noktasında hem NTCP hem NTCP2 (otomatik algılama)   - **Not**: 0.9.50'de (Mayıs 2021) NTCP (v1) desteği kaldırıldı   - "NTCP" stili artık kullanımdan kaldırıldı; "NTCP2" kullanın

### Gerekli Seçenekler

**Tüm Yayımlanmış NTCP2 Adresleri:**

1. **`host`** - IP adresi (IPv4 ya da IPv6) veya ana makine adı
   - Biçim: Standart IP gösterimi veya alan adı
   - Yalnızca giden ya da gizli router'lar için atlanabilir

2. **`port`** - TCP bağlantı noktası numarası
   - Biçim: Tamsayı, 1-65535
   - Yalnızca giden veya gizli routers için atlanabilir

3. **`s`** - Statik açık anahtar (X25519)
   - Biçim: Base64 ile kodlanmış, 44 karakter
   - Kodlama: I2P Base64 alfabesi
   - Kaynak: 32 bayt X25519 açık anahtar, little-endian (düşük anlamlı bayt önce)

4. **`i`** - AES için İlklendirme Vektörü
   - Biçim: Base64 ile kodlanmış, 24 karakter
   - Kodlama: I2P Base64 alfabesi
   - Kaynak: 16 baytlık IV, big-endian

5. **`v`** - Protokol sürümü
   - Biçim: Tamsayı veya virgülle ayrılmış tamsayılar
   - Geçerli: `"2"`
   - Gelecekte: `"2,3"` (sayısal sırada olmalıdır)

**İsteğe Bağlı Seçenekler:**

6. **`caps`** - Yetenekler (0.9.50'den beri)
   - Biçim: Yetenek karakterlerinden oluşan bir dize
   - Değerler:
     - `"4"` - IPv4 giden bağlantı yeteneği
     - `"6"` - IPv6 giden bağlantı yeteneği
     - `"46"` - Hem IPv4 hem de IPv6 (önerilen sıralama)
   - `host` yayımlanmışsa gerekmez
   - Gizli/güvenlik duvarı arkasındaki routers için kullanışlıdır

7. **`cost`** - Adres önceliği
   - Biçim: Tamsayı, 0-255
   - Daha düşük değerler = daha yüksek öncelik
   - Önerilen: normal adresler için 5-10
   - Önerilen: yayımlanmamış adresler için 14

### Örnek RouterAddress Girdileri

**Yayınlanan IPv4 Adresi:**

```
<Address cost="5">
  <transport_style>NTCP2</transport_style>
  <options>
    <host>192.0.2.1</host>
    <port>8887</port>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <i>MDEyMzQ1Njc4OUFCQ0RFRg==</i>
    <v>2</v>
  </options>
</Address>
```
**Gizli Router (Yalnızca Giden):**

```
<Address cost="14">
  <transport_style>NTCP2</transport_style>
  <options>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <v>2</v>
    <caps>4</caps>
  </options>
</Address>
```
**Çift Yığınlı Router:**

```
<!-- IPv4 Address -->
<Address cost="5">
  <transport_style>NTCP2</transport_style>
  <options>
    <host>192.0.2.1</host>
    <port>8887</port>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <i>MDEyMzQ1Njc4OUFCQ0RFRg==</i>
    <v>2</v>
  </options>
</Address>

<!-- IPv6 Address (same keys, same port) -->
<Address cost="5">
  <transport_style>NTCP2</transport_style>
  <options>
    <host>2001:db8::1</host>
    <port>8887</port>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <i>MDEyMzQ1Njc4OUFCQ0RFRg==</i>
    <v>2</v>
  </options>
</Address>
```
**Önemli Kurallar:** - **aynı bağlantı noktası**na sahip birden çok NTCP2 adresi, MUTLAKA **özdeş** `s`, `i` ve `v` değerleri kullanmalıdır - Farklı bağlantı noktaları farklı anahtarlar kullanabilir - Çift yığın (dual-stack) routers ayrı IPv4 ve IPv6 adresleri yayımlamalıdır

### Yayınlanmamış NTCP2 Adresi

**Yalnızca Giden Router'lar İçin:**

Bir router, gelen NTCP2 bağlantılarını kabul etmiyorsa ancak giden bağlantılar başlatıyorsa, yine de aşağıdakileri içeren bir RouterAddress (yöneltici adresi) yayımlaması ZORUNDADIR:

```xml
<Address cost="14">
  <transport_style>NTCP2</transport_style>
  <options>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <v>2</v>
  </options>
</Address>
```
**Amaç:** - El sıkışma sırasında Bob'un Alice'in statik anahtarını doğrulamasına olanak tanır - Mesaj 3, bölüm 2 RouterInfo doğrulaması için gereklidir - `i`, `host` veya `port` gerekmez (yalnızca giden)

**Alternatif:** - Yayımlanmış mevcut "NTCP" veya SSU adresine `s` ve `v` ekleyin

### Açık Anahtar ve IV Rotasyonu

**Kritik Güvenlik Politikası:**

**Genel Kurallar:** 1. **router çalışırken asla rotasyon yapmayın** 2. **Anahtar ve IV (başlatma vektörü) değerlerini kalıcı olarak saklayın** yeniden başlatmalar arasında 3. **Önceki kapalı kalma süresini izleyin** rotasyon uygunluğunu belirlemek için

**Rotasyondan önceki minimum kesinti süresi:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Router Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Min Downtime</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Reason</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Published NTCP2 address</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>1 month</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Many routers cache RouterInfo</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Published SSU only (no NTCP2)</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>1 day</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Moderate caching</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">No published addresses (hidden)</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>2 hours</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimal impact</td></tr>
  </tbody>
</table>
**Ek Tetikleyiciler:** - Yerel IP adresi değişikliği: Kesinti süresinden bağımsız olarak yenilenebilir - Router "rekey" (yeni Router Hash): Yeni anahtarlar oluşturur

**Gerekçe:** - Anahtar değişiklikleri üzerinden yeniden başlatma zamanlarının açığa çıkmasını önler - Önbelleğe alınmış RouterInfos öğelerinin süresinin doğal olarak dolmasına izin verir - Ağ kararlılığını korur - Başarısız bağlantı girişimlerini azaltır

**Uygulama:** 1. Anahtarı, IV (başlatma vektörü) ve son kapatma zaman damgasını kalıcı olarak saklayın 2. Başlangıçta downtime = current_time - last_shutdown değerini hesaplayın 3. downtime, router türü için minimumun üzerindeyse, anahtar ve IV için rotasyon yapılabilir 4. IP değiştiyse veya yeniden anahtarlama varsa, rotasyon yapılabilir 5. Aksi halde, önceki anahtarı ve IV'yi yeniden kullanın

**IV Rotasyonu:** - Anahtar rotasyonuyla aynı kurallara tabidir - Yalnızca yayımlanmış adreslerde bulunur (gizli routers değil) - Anahtar her değiştiğinde IV'nin değiştirilmesi önerilir

## Sürüm Tespiti

**Bağlam:** `transportStyle="NTCP"` (eski) iken, Bob aynı portta hem NTCP v1 hem de v2’yi destekler ve protokol sürümünü otomatik olarak algılamalıdır.

**Tespit Algoritması:**

```
1. Wait for at least 64 bytes (minimum NTCP2 message 1 size)

2. If received ≥ 288 bytes:
   → Connection is NTCP version 1 (NTCP1 message 1 is 288 bytes)

3. If received < 288 bytes:
   
   Option A (conservative, pre-NTCP2 majority):
   a. Wait additional short time (e.g., 100-500ms)
   b. If total received ≥ 288 bytes → NTCP1
   c. Otherwise → Attempt NTCP2 decode
   
   Option B (aggressive, post-NTCP2 majority):
   a. Attempt NTCP2 decode immediately:
      - Decrypt first 32 bytes (X key) with AES-256-CBC
      - Verify valid X25519 point (X[31] & 0x80 == 0)
      - Verify AEAD frame
   b. If decode succeeds → NTCP2
   c. If decode fails → Wait for more data or NTCP1
```
**Hızlı MSB (en yüksek anlamlı bit) Kontrolü:** - AES şifre çözmeden önce doğrulayın: `encrypted_X[31] & 0x80 == 0` - Geçerli X25519 anahtarlarında yüksek bit temizdir - Başarısızlık büyük olasılıkla NTCP1'i (veya bir saldırıyı) gösterir - Başarısızlık durumunda yoklama direnci (rastgele zaman aşımı + okuma) uygulayın

**Uygulama Gereksinimleri:**

1. **Alice’in Sorumluluğu:**
   - "NTCP" adresine bağlanırken, 1. mesajı en fazla 287 baytla sınırla
   - Tüm 1. mesajı tamponla ve tek seferde boşalt
   - Tek bir TCP paketiyle iletilme olasılığını artırır

2. **Bob'un Sorumlulukları:**
   - Sürümü tespit etmeden önce alınan veriyi arabelleğe al
   - Uygun zaman aşımı yönetimini uygula
   - Hızlı sürüm tespiti için TCP_NODELAY kullan
   - Sürüm tespit edildikten sonra 2. mesajın tamamını arabelleğe al ve tek seferde boşalt

**Güvenlik Hususları:** - Segmentasyon saldırıları: Bob, TCP segmentasyonuna karşı dayanıklı olmalıdır - Yoklama saldırıları: Başarısızlıklarda rastgele gecikmeler ve bayt okumaları uygulayın - DoS (Hizmet Reddi) önleme: Eşzamanlı bekleyen bağlantıları sınırlandırın - Okuma zaman aşımları: Hem her okuma için hem de toplam ("slowloris" koruması)

## Saat Sapması Yönergeleri

**Zaman Damgası Alanları:** - Mesaj 1: `tsA` (Alice'in zaman damgası) - Mesaj 2: `tsB` (Bob'un zaman damgası) - Mesaj 3+: İsteğe bağlı DateTime (tarih-saat) blokları

**Maksimum Sapma (D):** - Tipik: **±60 saniye** - Uygulama bazında yapılandırılabilir - Sapma > D genellikle ölümcül kabul edilir

### Bob'un Ele Alması (Mesaj 1)

```
1. Receive tsA from Alice
2. skew = tsA - current_time
3. If |skew| > D:
   a. Still send message 2 (allows Alice to calculate skew)
   b. Include tsB in message 2
   c. Do NOT initiate handshake completion
   d. Optionally: Temporary ban Alice's IP
   e. After message 2 sent, close connection

4. If |skew| ≤ D:
   a. Continue handshake normally
```
**Gerekçe:** Zaman sapması olsa bile 2. mesajın gönderilmesi, Alice'in sistem saatiyle ilgili sorunları teşhis etmesine olanak tanır.

### Alice'in İşlemesi (Mesaj 2)

```
1. Receive tsB from Bob
2. RTT = (current_time_now - tsA_sent)
3. adjusted_skew = (tsB - current_time_now) - (RTT / 2)
4. If |adjusted_skew| > D:
   a. Close connection immediately
   b. If local clock suspect: Adjust clock or use external time source
   c. If Bob's clock suspect: Temporary ban Bob
   d. Log for operator review
5. If |adjusted_skew| ≤ D:
   a. Continue handshake normally
   b. Optionally: Track skew for time synchronization
```
**RTT Düzeltmesi:** - Hesaplanan sapmadan RTT (gidiş-dönüş süresi) değerinin yarısını çıkarın - Ağ yayılım gecikmesini dikkate alır - Daha doğru sapma tahmini

### Bob'un İşlemesi (Mesaj 3)

```
1. If message 3 received (unlikely if skew exceeded in message 1)
2. Recalculate skew = tsA_received - current_time
3. If |adjusted_skew| > D:
   a. Send termination block (reason code 7: clock skew)
   b. Close connection
   c. Ban Alice for period (e.g., 1-24 hours)
```
### Zaman Senkronizasyonu

**DateTime Blokları (Veri Aşaması):** - Periyodik olarak DateTime bloğu gönder (tip 0) - Alıcı saat ayarlaması için kullanabilir - Zaman damgasını en yakın saniyeye yuvarla (yanlılığı önlemek için)

**Harici Zaman Kaynakları:** - NTP (Ağ Zaman Protokolü) - Sistem saati eşzamanlaması - I2P ağının konsensüs zamanı

**Saat Ayarlama Stratejileri:** - Yerel saat yanlışsa: Sistem saatini ayarla veya offset (kaydırma) kullan - Eşlerin saatleri sürekli yanlışsa: Eşte sorun olduğunu işaretle - Ağ sağlığını izlemek için skew (sapma) istatistiklerini izle

## Güvenlik Özellikleri

### İleri Gizlilik

**Şunlarla Gerçekleştirilir:** - Geçici Diffie-Hellman anahtar değişimi (X25519) - Üç DH işlemi: es, ee, se (Noise XK pattern) (Noise XK deseni) - El sıkışması tamamlandıktan sonra geçici anahtarlar imha edilir

**Gizlilik İlerlemesi:** - Mesaj 1: Seviye 2 (gönderen kompromize olduğunda forward secrecy (ileriye dönük gizlilik)) - Mesaj 2: Seviye 1 (geçici alıcı) - Mesaj 3+: Seviye 5 (güçlü forward secrecy)

**Mükemmel İleri Gizlilik (Perfect Forward Secrecy):** - Uzun vadeli statik anahtarların ele geçirilmesi geçmiş oturum anahtarlarını AÇIĞA ÇIKARMAZ - Her oturum benzersiz geçici anahtarlar kullanır - Geçici özel anahtarlar asla yeniden kullanılmaz - Anahtar anlaşmasından sonra bellek temizliği

**Sınırlamalar:** - Mesaj 1, Bob'un statik anahtarı ele geçirilirse savunmasızdır (ancak Alice'in kompromize olması durumunda ileri gizlilik sağlar) - Mesaj 1 için yeniden oynatma saldırıları mümkündür (zaman damgası ve yeniden oynatma önbelleği ile azaltılır)

### Kimlik Doğrulama

**Karşılıklı Kimlik Doğrulama:** - Alice'in kimliği, 3. mesajdaki statik anahtar ile doğrulanır - Bob'un kimliği, statik özel anahtara sahip olmasıyla doğrulanır (başarılı el sıkışmadan örtük olarak)

**Anahtar Ele Geçirme Yoluyla Kimliğe Bürünme (KCI) Direnci:** - Kimlik doğrulama düzeyi 2 (KCI'ye dayanıklı) - Saldırgan, Alice'in statik özel anahtarına sahip olsa bile (Alice'in geçici anahtarı olmadan) Alice'in kimliğine bürünemez - Saldırgan, Bob'un statik özel anahtarına sahip olsa bile (Bob'un geçici anahtarı olmadan) Bob'un kimliğine bürünemez

**Statik Anahtar Doğrulaması:** - Alice, Bob'un statik anahtarını önceden bilir (RouterInfo'dan) - Bob, 3. mesajda Alice'in statik anahtarının RouterInfo ile eşleştiğini doğrular - Ortadaki adam saldırılarını önler

### Trafik Analizine Karşı Direnç

**DPI (Derin Paket İncelemesi) Karşı Önlemleri:** 1. **AES Gizleme:** Geçici anahtarlar şifrelenir, rastgele görünür 2. **SipHash Uzunluk Gizleme:** Çerçeve uzunlukları açık metin değildir 3. **Rastgele Dolgu:** Değişken mesaj boyutları, sabit kalıplar yok 4. **Şifreli Çerçeveler:** Tüm yük ChaCha20 ile şifrelenir

**Replay Saldırılarının Önlenmesi:** - Zaman damgası doğrulaması (±60 saniye) - Geçici anahtarlar için yeniden oynatma önbelleği (geçerlilik süresi 2*D) - Nonce (tek kullanımlık sayı) artışları, oturum içinde paketlerin yeniden oynatılmasını engeller

**Yoklamaya Karşı Direnç:** - AEAD (Authenticated Encryption with Associated Data - ilişkili verili doğrulamalı şifreleme) hatalarında rastgele zaman aşımı süreleri - Bağlantı kapatılmadan önce rastgele bayt okunması - El sıkışma başarısızlıklarında yanıt verilmez - Tekrarlanan başarısızlıklarda IP kara listeleme

**Dolgu Yönergeleri:** - Mesajlar 1-2: Açık metin dolgusu (kimliği doğrulanmış) - Mesaj 3+: AEAD çerçeveleri içinde şifrelenmiş dolgu - Müzakere edilen dolgu parametreleri (Seçenekler bloğu) - Yalnızca dolgu çerçevelerine izin verilir

### Hizmet Reddi Saldırılarının Azaltılması

**Bağlantı Sınırları:** - Maksimum etkin bağlantı sayısı (gerçeklemeye bağlı) - Maksimum bekleyen el sıkışması sayısı (örn., 100-1000) - IP başına bağlantı sınırları (örn., eşzamanlı 3-10)

**Kaynak Koruması:** - DH (Diffie-Hellman) işlemleri oran sınırlandırılmış (hesaplama açısından maliyetli) - Soket başına ve toplam okuma zaman aşımları - "Slowloris" koruması (toplam süre sınırları) - Kötüye kullanıma karşı IP kara listeleme

**Hızlı Reddetme:** - Ağ kimliği uyuşmazlığı → anında kapatma - Geçersiz X25519 noktası (eliptik eğri Diffie–Hellman anahtar değişimi) → şifre çözmeden önce hızlı MSB kontrolü - Zaman damgası sınırların dışında → hesaplama yapmadan kapatma - AEAD (Authenticated Encryption with Associated Data, ilişkili verili kimlik doğrulamalı şifreleme) hatası → yanıt yok, rastgele gecikme

**Yoklamaya karşı direnç:** - Rastgele zaman aşımı: 100-500ms (uygulamaya bağlı) - Rastgele okuma: 1KB-64KB (uygulamaya bağlı) - Saldırgana hata bilgisi verilmez - TCP RST ile kapat (FIN el sıkışması yok)

### Kriptografik Güvenlik

**Algoritmalar:** - **X25519**: 128-bit güvenlik, eliptik eğri DH (Curve25519) - **ChaCha20**: 256-bit anahtarlı akış şifresi - **Poly1305**: bilgi kuramsal olarak güvenli MAC (İleti Kimlik Doğrulama Kodu) - **SHA-256**: 128-bit çarpışma direnci, 256-bit öngörüntü direnci - **HMAC-SHA256**: anahtar türetimi için PRF (yalancı rastgele fonksiyon)

**Anahtar Boyutları:** - Statik anahtarlar: 32 bayt (256 bit) - Geçici anahtarlar: 32 bayt (256 bit) - Şifreleme anahtarları: 32 bayt (256 bit) - MAC (İleti Kimlik Doğrulama Kodu): 16 bayt (128 bit)

**Bilinen Sorunlar:** - ChaCha20 nonce (tek seferlik sayı) yeniden kullanımı felaketlidir (sayaç artırımıyla önlenir) - X25519 küçük alt grup sorunlarına sahiptir (eğri doğrulamasıyla hafifletilir) - SHA-256 teorik olarak length extension (uzunluk genişletme saldırısı) karşı savunmasızdır (HMAC'te istismar edilemez)

**Bilinen Güvenlik Açığı Yok (Ekim 2025 itibarıyla):** - Noise Protocol Framework kapsamlı olarak incelendi - ChaCha20-Poly1305 TLS 1.3'te kullanıma alındı - X25519 modern protokollerde standart - Tasarıma karşı pratik saldırı yok

## Kaynaklar

### Ana Spesifikasyonlar

- **[NTCP2 Spesifikasyonu](/docs/specs/ntcp2/)** - Resmi I2P spesifikasyonu
- **[Öneri 111](/proposals/111-ntcp-2/)** - Gerekçeleriyle birlikte özgün tasarım belgesi
- **[Noise Protocol Framework](https://noiseprotocol.org/noise.html)** - Revizyon 33 (2017-10-04)

### Kriptografik Standartlar

- **[RFC 7748](https://www.rfc-editor.org/rfc/rfc7748)** - Güvenlik için Eliptik Eğriler (X25519)
- **[RFC 7539](https://www.rfc-editor.org/rfc/rfc7539)** - IETF Protokolleri için ChaCha20 ve Poly1305
- **[RFC 8439](https://www.rfc-editor.org/rfc/rfc8439)** - ChaCha20-Poly1305 (RFC 7539'un yerini alır)
- **[RFC 2104](https://www.rfc-editor.org/rfc/rfc2104)** - HMAC: Mesaj kimlik doğrulaması için anahtarlı özetleme
- **[SipHash](https://www.131002.net/siphash/)** - Özet (hash) fonksiyonu uygulamaları için SipHash-2-4

### İlgili I2P Spesifikasyonları

- **[I2NP Belirtimi](/docs/specs/i2np/)** - I2P Ağ Protokolü mesaj biçimi
- **[Ortak Yapılar](/docs/specs/common-structures/)** - RouterInfo, RouterAddress biçimleri
- **[SSU Taşıma](/docs/legacy/ssu/)** - UDP taşıma (orijinal, şimdi SSU2)
- **[Öneri 147](/proposals/147-transport-network-id-check/)** - Taşıma Ağı Kimliği Denetimi (0.9.42)

### Uygulama Referansları

- **[I2P Java](https://github.com/i2p/i2p.i2p)** - Referans implementasyonu (Java)
- **[i2pd](https://github.com/PurpleI2P/i2pd)** - C++ implementasyonu
- **[I2P Sürüm Notları](/blog/)** - Sürüm geçmişi ve güncellemeler

### Tarihsel Bağlam

- **[İstasyondan İstasyona Protokolü (STS)](https://en.wikipedia.org/wiki/Station-to-Station_protocol)** - Noise çerçevesi için ilham kaynağı
- **[obfs4](https://gitlab.com/yawning/obfs4)** - Takılabilir aktarım (SipHash tabanlı uzunluk gizleme için emsal)

## Uygulama Yönergeleri

### Zorunlu Gereksinimler

**Uyumluluk için:**

1. **Tam El Sıkışmasını Uygulayın:**
   - Doğru KDF (anahtar türetme fonksiyonu) zincirleriyle her üç mesajı da destekleyin
   - Tüm AEAD (ilişkili verili doğrulamalı şifreleme) etiketlerini doğrulayın
   - X25519 (eliptik eğri anahtar değişimi) noktalarının geçerli olduğunu doğrulayın

2. **Veri Aşamasını Uygulayın:**
   - SipHash uzunluk gizleme (her iki yönde)
   - Tüm blok türleri: 0 (Tarih/Saat), 1 (Seçenekler), 2 (RouterInfo), 3 (I2NP), 4 (Sonlandırma), 254 (Dolgu)
   - Doğru nonce (tek seferlik sayı) yönetimi (ayrı sayaçlar)

3. **Güvenlik Özellikleri:**
   - Yeniden yürütmenin önlenmesi (geçici anahtarları 2*D boyunca önbelleğe alma)
   - Zaman damgası doğrulaması (varsayılan ±60 saniye)
   - 1-2 numaralı iletilerde rastgele dolgu
   - Rastgele zaman aşımı süreleriyle AEAD hata işleme

4. **RouterInfo Yayınlama:**
   - Statik anahtarı ("s"), IV'yi ("i") ve sürümü ("v") yayınla
   - Anahtarları ilkeye göre döndür
   - Gizli router'lar için yetenekler alanını ("caps") destekle

5. **Ağ Uyumluluğu:**
   - Ağ kimliği alanını destekleyin (şu anda ana ağ için 2)
   - Mevcut Java ve i2pd gerçeklemeleriyle birlikte çalışın
   - Hem IPv4 hem de IPv6'yı destekleyin

### Önerilen Uygulamalar

**Performans Optimizasyonu:**

1. **Arabelleğe Alma Stratejisi:**
   - Tüm mesajları tek seferde gönder (mesaj 1, 2, 3)
   - El sıkışma mesajları için TCP_NODELAY (Nagle algoritmasını devre dışı bırakma seçeneği) kullan
   - Birden çok veri bloğunu tek bir çerçevede arabelleğe al
   - Çerçeve boyutunu birkaç KB'ye sınırla (alıcı gecikmesini en aza indir)

2. **Bağlantı Yönetimi:**
   - Mümkün olduğunda bağlantıları yeniden kullanın
   - Bağlantı havuzu uygulayın
   - Bağlantı sağlığını izleyin (DateTime blokları)

3. **Bellek Yönetimi:**
   - Kullanımdan sonra hassas veriyi sıfırla (geçici anahtarlar, DH sonuçları)
   - Eşzamanlı el sıkışmalarını sınırla (DoS önleme; Hizmet Reddi)
   - Sık tahsisler için bellek havuzları kullan

**Güvenlik Sıkılaştırma:**

1. **Sondalama Direnci:**
   - Rastgele zaman aşımı süreleri: 100-500ms
   - Rastgele bayt okumaları: 1KB-64KB
   - Tekrarlanan başarısızlıklar için IP kara listeleme
   - Eşlere hata ayrıntıları sağlanmaz

2. **Kaynak Sınırları:**
   - IP başına maksimum bağlantı: 3-10
   - Maksimum bekleyen el sıkışması: 100-1000
   - Okuma zaman aşımları: işlem başına 30-60 saniye
   - Toplam bağlantı zaman aşımı: el sıkışma için 5 dakika

3. **Anahtar Yönetimi:**
   - Statik anahtar ve IV (başlatma vektörü)'nin kalıcı olarak saklanması
   - Güvenli rastgele sayı üretimi (kriptografik RNG - rastgele sayı üreteci)
   - Anahtar rotasyonu politikalarına kesinlikle uyun
   - Geçici anahtarları asla yeniden kullanmayın

**İzleme ve Tanılama:**

1. **Metrikler:**
   - El sıkışma başarı/başarısızlık oranları
   - AEAD (İlişkili Verilerle Kimliği Doğrulanmış Şifreleme) hata oranları
   - Saat sapması dağılımı
   - Bağlantı süresi istatistikleri

2. **Günlükleme:**
   - El sıkışması başarısızlıklarını neden kodlarıyla günlüğe kaydedin
   - Saat sapması olaylarını günlüğe kaydedin
   - Yasaklanmış IP'leri günlüğe kaydedin
   - Hassas anahtar malzemesini asla günlüğe kaydetmeyin

3. **Testler:**
   - KDF zincirleri için birim testleri
   - Diğer gerçekleştirimlerle entegrasyon testleri
   - Paket işleme için Fuzzing (rastgele ve bozulmuş girdilerle test)
   - DoS dayanıklılığı için yük testleri

### Sık Yapılan Hatalar

**Kaçınılması Gereken Kritik Hatalar:**

1. **Nonce (tek-kullanımlık sayı) Yeniden Kullanımı:**
   - Oturum ortasında nonce sayacını asla sıfırlamayın
   - Her yön için ayrı sayaçlar kullanın
   - 2^64 - 1 değerine ulaşmadan önce sonlandırın

2. **Anahtar Döndürme:**
   - router çalışırken anahtarları asla döndürmeyin
   - Geçici anahtarları oturumlar arasında asla yeniden kullanmayın
   - Asgari kesinti süresi kurallarına uyun

3. **Zaman Damgası İşleme:**
   - Süresi geçmiş zaman damgalarını asla kabul etmeyin
   - Sapmayı hesaplarken her zaman RTT (gidiş-dönüş süresi) için düzeltme uygulayın
   - DateTime zaman damgalarını saniye hassasiyetine yuvarlayın

4. **AEAD (ek verili kimlik doğrulamalı şifreleme) Hataları:**
   - Hata türünü saldırgana asla açıklamayın
   - Kapatmadan önce her zaman rastgele bir zaman aşımı süresi kullanın
   - Geçersiz uzunluğu AEAD başarısızlığıyla aynı şekilde ele alın

5. **Dolgu:**
   - Uzlaşılan sınırların dışında asla dolgu göndermeyin
   - Dolgu bloğunu her zaman en sona yerleştirin
   - Her çerçevede birden fazla dolgu bloğu kullanmayın

6. **RouterInfo:**
   - Her zaman statik anahtarın RouterInfo ile eşleştiğini doğrulayın
   - Yayınlanmış adresleri olmayan RouterInfo'ları asla flood etmeyin (ağa yaymayın)
   - Her zaman imzaları doğrulayın

### Test Metodolojisi

**Birim Testleri:**

1. **Kriptografik Primitifler:**
   - X25519, ChaCha20, Poly1305, SHA-256 için test vektörleri
   - HMAC-SHA256 test vektörleri
   - SipHash-2-4 test vektörleri

2. **KDF Zincirleri:**
   - Üç iletinin tamamı için bilinen cevap testleri
   - Zincirleme anahtar yayılımını doğrulayın
   - SipHash IV üretimini test edin

3. **Mesaj Ayrıştırma:**
   - Geçerli mesajın kod çözümü
   - Geçersiz mesajın reddedilmesi
   - Sınır durumları (boş, azami boyut)

**Entegrasyon Testleri:**

1. **El sıkışma:**
   - Başarılı üç mesajlık alışveriş
   - Saat sapmasına göre reddetme
   - Yeniden oynatma saldırısı tespiti
   - Geçersiz anahtarların reddedilmesi

2. **Veri Aşaması:**
   - I2NP (I2P Ağ Protokolü) mesaj aktarımı
   - RouterInfo (yönlendirici bilgisi) değişimi
   - Doldurma yönetimi
   - Sonlandırma mesajları

3. **Birlikte Çalışabilirlik:**
   - Java I2P'ye karşı test yapın
   - i2pd'ye karşı test yapın
   - IPv4 ve IPv6'yı test edin
   - Yayınlanmış ve gizli routers üzerinde test yapın

**Güvenlik Testleri:**

1. **Negatif Testler:**
   - Geçersiz AEAD etiketleri
   - Yeniden oynatılmış mesajlar
   - Saat kayması saldırıları
   - Hatalı biçimlendirilmiş çerçeveler

2. **DoS (Hizmet Reddi) Testleri:**
   - Bağlantı taşması
   - Slowloris saldırıları
   - CPU tükenmesi (aşırı DH (Diffie-Hellman anahtar değişimi))
   - Bellek tükenmesi

3. **Fuzzing (rastgele girdilerle hata bulma testi):**
   - Rastgele el sıkışma mesajları
   - Rastgele veri aşaması çerçeveleri
   - Rastgele blok türleri ve boyutları
   - Geçersiz kriptografik değerler

### NTCP'den geçiş

**Eski NTCP desteği için (artık kaldırıldı):**

NTCP (sürüm 1), I2P 0.9.50'de (Mayıs 2021) kaldırıldı. Mevcut tüm uygulamalar NTCP2'yi desteklemelidir. Tarihsel notlar:

1. **Geçiş Dönemi (2018-2021):**
   - 0.9.36: NTCP2 tanıtıldı (varsayılan olarak devre dışı)
   - 0.9.37: NTCP2 varsayılan olarak etkinleştirildi
   - 0.9.40: NTCP kullanımı önerilmiyor (deprecated)
   - 0.9.50: NTCP kaldırıldı

2. **Sürüm Tespiti:**
   - "NTCP" transportStyle (taşıma stili) her iki sürümün de desteklendiğini belirtir
   - "NTCP2" transportStyle yalnızca NTCP2'nin desteklendiğini belirtir
   - Mesaj boyutuna göre otomatik algılama (287 vs 288 bayt)

3. **Güncel Durum:**
   - Tüm router'lar NTCP2'yi desteklemelidir
   - "NTCP" transportStyle kullanımdan kaldırılmıştır
   - Yalnızca "NTCP2" transportStyle kullanın

## Ek A: Noise XK Deseni

**Standart Noise XK Pattern (Noise protokol ailesindeki XK el sıkışma örüntüsü):**

```
XK(s, rs):
  <- s
  ...
  -> e, es
  <- e, ee
  -> s, se
```
**Yorumlama:**

- `<-` : Yanıtlayıcıdan (Bob) başlatıcıya (Alice) giden mesaj
- `->` : Başlatıcıdan (Alice) yanıtlayıcıya (Bob) giden mesaj
- `s` : Statik anahtar (uzun süreli kimlik anahtarı)
- `rs` : Uzak statik anahtar (eşin statik anahtarı, önceden bilinir)
- `e` : Geçici anahtar (oturuma özgü, talep üzerine üretilir)
- `es` : Geçici-Statik DH (Alice geçici × Bob statik)
- `ee` : Geçici-Geçici DH (Alice geçici × Bob geçici)
- `se` : Statik-Geçici DH (Alice statik × Bob geçici)

**Anahtar Anlaşması Sırası:**

1. **Ön-mesaj:** Alice, Bob'un statik açık anahtarını biliyor (RouterInfo'dan)
2. **Mesaj 1:** Alice geçici anahtarı gönderir, es DH işlemini gerçekleştirir
3. **Mesaj 2:** Bob geçici anahtarı gönderir, ee DH işlemini gerçekleştirir
4. **Mesaj 3:** Alice statik anahtarını açıklar, se DH işlemini gerçekleştirir

**Güvenlik Özellikleri:**

- Alice kimliği doğrulandı: Evet (3. mesajla)
- Bob kimliği doğrulandı: Evet (statik özel anahtara sahip olmasıyla)
- İleri gizlilik: Evet (geçici anahtarlar imha edildi)
- KCI resistance (Key Compromise Impersonation - anahtar ele geçirilmesi saldırısına karşı direnç): Evet (kimlik doğrulama seviyesi 2)

## Ek B: Base64 Kodlama

**I2P Base64 Alfabesi:**

```
ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-~
```
**Standart Base64'dan farklar:** - 62-63 numaralı karakterler: `-~`, `+/` yerine - Dolgu: Aynı (`=`) veya bağlama bağlı olarak atlanabilir

**NTCP2 kullanımında:** - Statik anahtar ("s"): 32 bayt → 44 karakter (dolgu yok) - IV ("i"): 16 bayt → 24 karakter (dolgu yok)

**Kodlama Örneği:**

```python
# 32-byte static key (hex): 
# f4489e1bb0597b39ca6cbf5ad9f5f1f09043e02d96cb9aa6a63742b3462429aa

# I2P Base64 encoded:
# 9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=
```
## Ek C: Paket Yakalama Analizi

**NTCP2 trafiğinin tanımlanması:**

1. **TCP El Sıkışması:**
   - Standart TCP SYN, SYN-ACK, ACK
   - Hedef port genellikle 8887 veya benzeri

2. **Mesaj 1 (SessionRequest):**
   - Alice'ten gelen ilk uygulama verisi
   - 80-65535 bayt (genellikle birkaç yüz)
   - Rastgele görünür (AES ile şifrelenmiş geçici anahtar)
   - "NTCP" adresine bağlanılıyorsa en fazla 287 bayt

3. **Mesaj 2 (SessionCreated - oturum oluşturuldu):**
   - Bob'dan gelen yanıt
   - 80-65535 bayt (tipik olarak birkaç yüz)
   - Ayrıca rastgele görünür

4. **Mesaj 3 (SessionConfirmed):**
   - Alice'den
   - 48 bayt + değişken (RouterInfo boyutu + dolgu)
   - Genellikle 1-4 KB

5. **Veri Aşaması:**
   - Değişken uzunluklu çerçeveler
   - Uzunluk alanı gizlenmiş (rastgele görünür)
   - Şifrelenmiş yük
   - Dolgu, boyutu öngörülemez kılar

**DPI Atlatma:** - Düz metin üstbilgileri yok - Sabit kalıplar yok - Uzunluk alanları gizlenmiş - Rastgele dolgu boyut tabanlı sezgisel yöntemleri bozar

**NTCP ile karşılaştırma:** - NTCP'nin 1. mesajı her zaman 288 bayttır (tespit edilebilir) - NTCP2'nin 1. mesajının boyutu değişir (tespit edilemez) - NTCP tanınabilir örüntülere sahipti - NTCP2, DPI'ye (Derin Paket İncelemesi) direnmek üzere tasarlandı

## Ek D: Sürüm Geçmişi

**Önemli Dönüm Noktaları:**

- **0.9.36** (23 Ağustos 2018): NTCP2 tanıtıldı, varsayılan olarak devre dışı
- **0.9.37** (4 Ekim 2018): NTCP2 varsayılan olarak etkin
- **0.9.40** (20 Mayıs 2019): NTCP kullanımdan kaldırıldı
- **0.9.42** (27 Ağustos 2019): Ağ Kimliği alanı eklendi (Öneri 147)
- **0.9.50** (17 Mayıs 2021): NTCP kaldırıldı, yetenekler için destek eklendi
- **2.10.0** (9 Eylül 2025): En son kararlı sürüm

**Protokol Kararlılığı:** - 0.9.50'den beri geriye dönük uyumluluğu bozan değişiklik yok - Sondalama direncine yönelik devam eden iyileştirmeler - Performans ve güvenilirliğe odaklanma - Kuantum sonrası kriptografi geliştirme aşamasında (varsayılan olarak etkin değil)

**Güncel Taşıma Durumu:** - NTCP2: Zorunlu TCP taşıma - SSU2: Zorunlu UDP taşıma - NTCP (v1): Kaldırıldı - SSU (v1): Kaldırıldı
