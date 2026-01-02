---
title: "ECIES-X25519-AEAD-Ratchet (kademeli anahtar yenileme mekanizması) Şifreleme Şartnamesi"
description: "I2P için Eliptik Eğri Bütünleşik Şifreleme Şeması (X25519 + AEAD)"
slug: "ecies"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
toc: true
---

## Genel Bakış

### Amaç

ECIES-X25519-AEAD-Ratchet, I2P'nin modern uçtan uca şifreleme protokolüdür ve eski ElGamal/AES+SessionTags sisteminin yerini alır. İleriye dönük gizlilik, kimlik doğrulamalı şifreleme ve performans ile güvenlikte önemli iyileştirmeler sağlar.

### ElGamal/AES+SessionTags'e Göre Başlıca İyileştirmeler

- **Daha Küçük Anahtarlar**: 32 baytlık anahtarlar, 256 baytlık ElGamal açık anahtarlarına karşı (%87,5 azalma)
- **İleri Gizlilik**: DH ratcheting (DH ratchet mekanizması) aracılığıyla sağlanır (eski protokolde mevcut değildir)
- **Modern Kriptografi**: X25519 DH, ChaCha20-Poly1305 AEAD, SHA-256
- **Kimlik Doğrulamalı Şifreleme**: AEAD yapısı aracılığıyla yerleşik kimlik doğrulaması
- **Çift Yönlü Protokol**: Eşleştirilmiş gelen/giden oturumlar, tek yönlü eski protokole karşı
- **Verimli Etiketler**: 8 baytlık oturum etiketleri, 32 baytlık etiketlere karşı (%75 azalma)
- **Trafik Gizleme**: Elligator2 kodlaması, el sıkışmalarını rastgele veriden ayırt edilemez hale getirir

### Dağıtım Durumu

- **İlk Sürüm**: Sürüm 0.9.46 (25 Mayıs 2020)
- **Ağ Dağıtımı**: 2020 itibarıyla tamamlandı
- **Güncel Durum**: Olgun, yaygın olarak konuşlandırılmış (5+ yıldır üretimde)
- **Router Desteği**: Sürüm 0.9.46 veya üzeri gereklidir
- **Floodfill Gereksinimleri**: Şifreli sorgular için neredeyse %100 benimsenme

### Gerçekleştirme Durumu

**Tamamen Uygulandı:** - Bağlama içeren New Session (NS) mesajları - New Session Reply (NSR) mesajları - Existing Session (ES) mesajları - DH ratchet (kademeli anahtar yenileme) mekanizması - Session tag ve simetrik anahtar ratchet'ları - DateTime, NextKey, ACK, ACK Request, Garlic Clove ve Padding blokları

**Uygulanmadı (sürüm 0.9.50 itibarıyla):** - MessageNumbers bloğu (tip 6) - Options bloğu (tip 5) - Termination bloğu (tip 4) - Protokol katmanı otomatik yanıtları - Sıfır statik anahtar modu - Multicast oturumları

**Not**: 1.5.0'dan 2.10.0'a (2021-2025) kadar olan sürümlerin uygulama durumu, bazı özellikler eklenmiş olabileceğinden doğrulama gerektirir.

---

## Protokolün Temelleri

### Noise Protokol Çerçevesi

ECIES-X25519-AEAD-Ratchet, [Noise Protocol Framework](https://noiseprotocol.org/) (Noise Protokol Çatısı) (Revision 34, 2018-07-11) temelinde, özellikle I2P'ye özgü uzantılarla **IK** (Etkileşimli, uzaktaki statik anahtarı bilinen) el sıkışma desenini kullanır.

### Noise Protokol Tanımlayıcısı

```
Noise_IKelg2+hs2_25519_ChaChaPoly_SHA256
```
**Tanımlayıcı Bileşenler:** - `Noise` - Temel çerçeve - `IK` - Bilinen uzak statik anahtarla etkileşimli el sıkışma deseni - `elg2` - Geçici anahtarlar için Elligator2 kodlaması (I2P extension) - `+hs2` - Etiketi karışıma katmak için ikinci iletiden önce çağrılan MixHash (I2P extension) - `25519` - X25519 Diffie-Hellman işlevi - `ChaChaPoly` - ChaCha20-Poly1305 AEAD şifreleme algoritması - `SHA256` - SHA-256 özet işlevi

### Noise El Sıkışma Örüntüsü

**IK Desen Notasyonu:**

```
<- s                    (Bob's static key known to Alice)
...
-> e, es, s, ss         (Alice sends ephemeral, DH es, static key, DH ss)
<- e, ee, se            (Bob sends ephemeral, DH ee, DH se)
```
**Kısaltmaların Anlamları:** - `e` - Geçici anahtar iletimi - `s` - Statik anahtar iletimi - `es` - Alice'in geçici anahtarı ile Bob'un statik anahtarı arasındaki DH (Diffie-Hellman) - `ss` - Alice'in statik anahtarı ile Bob'un statik anahtarı arasındaki DH - `ee` - Alice'in geçici anahtarı ile Bob'un geçici anahtarı arasındaki DH - `se` - Bob'un statik anahtarı ile Alice'in geçici anahtarı arasındaki DH

### Noise Güvenlik Özellikleri

Noise terminolojisini kullanarak, IK pattern (IK kalıbı) şunları sağlar:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Message</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Authentication Level</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Confidentiality Level</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Message&nbsp;1 (NS)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;1 (sender auth, KCI vulnerable)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;2 (weak forward secrecy)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Message&nbsp;2 (NSR)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;2 (mutual auth)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;4 (weak forward secrecy)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Transport (ES)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;2 (mutual auth)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;5 (strong forward secrecy)</td>
    </tr>
  </tbody>
</table>
**Kimlik Doğrulama Düzeyleri:** - **Düzey 1**: Yükün, gönderenin statik anahtarının sahibine ait olduğu doğrulanır, ancak Key Compromise Impersonation (KCI) (anahtar ele geçirilmesiyle kimliğe bürünme) saldırılarına karşı savunmasızdır - **Düzey 2**: NSR sonrasında KCI saldırılarına karşı dayanıklı

**Gizlilik Seviyeleri:** - **Seviye 2**: Göndericinin statik anahtarı daha sonra ele geçirilirse ileri gizlilik - **Seviye 4**: Göndericinin geçici anahtarı daha sonra ele geçirilirse ileri gizlilik - **Seviye 5**: Her iki geçici anahtar da silindikten sonra tam ileri gizlilik

### IK (Noise protokolünde el sıkışma kalıbı) ile XK (Noise protokolünde el sıkışma kalıbı) Arasındaki Farklar

IK pattern (IK deseni), NTCP2 ve SSU2'de kullanılan XK pattern (XK deseni) ile farklılık gösterir:

1. **Dört DH İşlemi**: IK, 4 DH işlemi (es, ss, ee, se) kullanır; XK için sayı 3'tür
2. **Anında Kimlik Doğrulama**: Alice’nin kimliği ilk mesajda doğrulanır (Kimlik Doğrulama Düzeyi 1)
3. **Daha Hızlı İleri Gizlilik**: Tam ileri gizlilik (Düzey 5), ikinci mesajdan sonra (1-RTT) sağlanır
4. **Ödün**: İlk mesajın yükü ileri gizliliğe sahip değildir (XK'de tüm yükler ileri gizliliğe sahiptir)

**Özet**: IK (Noise IK deseni), Bob'un yanıtının 1-RTT (tek gidiş-dönüş süresi) içinde tam ileri gizlilikle iletilmesini mümkün kılar; bunun bedeli olarak, ilk isteğin ileri gizlilik sağlamamasıdır.

### Signal Double Ratchet (çift mandallı anahtar yenileme mekanizması) Kavramları

ECIES, [Signal Double Ratchet Algorithm](https://signal.org/docs/specifications/doubleratchet/) kavramlarını benimser:

- **DH Mandalı**: Yeni DH anahtarlarını periyodik olarak değiş tokuş ederek ileri gizlilik sağlar
- **Simetrik Anahtar Mandalı**: Her mesaj için yeni oturum anahtarları türetir
- **Oturum Etiketi Mandalı**: Tek kullanımlık oturum etiketlerini deterministik olarak üretir

**Signal'dan Temel Farklar:** - **Daha Seyrek Ratcheting**: (ratchet/mandal mekanizması) I2P yalnızca gerektiğinde ratchet uygular (etiket tükenmesine yaklaşıldığında veya politikaya göre) - **Başlık Şifrelemesi Yerine Oturum Etiketleri**: Şifrelenmiş başlıklar yerine deterministik etiketler kullanır - **Açık ACK'ler**: (onay) Yalnızca ters trafiğe güvenmek yerine bant içi ACK bloklarını kullanır - **Ayrı Etiket ve Anahtar Ratchet'leri**: Alıcı için daha verimlidir (anahtar hesaplamasını erteleyebilir)

### Noise (kriptografik protokol çerçevesi) için I2P Uzantıları


---

## Kriptografik İlkel Yapılar

### X25519 Diffie-Hellman

**Belirtim**: [RFC 7748](https://tools.ietf.org/html/rfc7748)

**Anahtar Özellikleri:** - **Özel Anahtar Boyutu**: 32 bayt - **Açık Anahtar Boyutu**: 32 bayt - **Paylaşılan Sır Boyutu**: 32 bayt - **Endianness (bayt sıralaması)**: Little-endian - **Eğri**: Curve25519

**İşlemler:**

### X25519 GENERATE_PRIVATE()

Rastgele 32 baytlık bir özel anahtar oluşturur:

```
privkey = CSRNG(32)
```
### X25519 DERIVE_PUBLIC(privkey)

İlgili açık anahtarı türetir:

```
pubkey = curve25519_scalarmult_base(privkey)
```
32 baytlık little-endian (küçük uçlu bayt sıralaması) açık anahtarı döndürür.

### X25519 DH(privkey, pubkey)

Diffie-Hellman anahtar değişimini gerçekleştirir:

```
sharedSecret = curve25519_scalarmult(privkey, pubkey)
```
32 bayt uzunluğunda bir paylaşılan sır döndürür.

**Güvenlik Notu**: Uygulayıcılar, paylaşılan sırrın tamamının sıfırlardan oluşmadığını doğrulamalıdır (zayıf anahtar). Bu gerçekleşirse reddedin ve el sıkışmayı sonlandırın.

### ChaCha20-Poly1305 AEAD (İlişkili Verili Kimlik Doğrulamalı Şifreleme)

**Belirtim**: [RFC 7539](https://tools.ietf.org/html/rfc7539) bölüm 2.8

**Parametreler:** - **Anahtar Boyutu**: 32 bayt (256 bit) - **Nonce Boyutu** (tek kullanımlık sayı): 12 bayt (96 bit) - **MAC Boyutu**: 16 bayt (128 bit) - **Blok Boyutu**: 64 bayt (dahili)

**Nonce (tek seferlik sayı) Biçimi:**

```
Byte 0-3:   0x00 0x00 0x00 0x00  (always zero)
Byte 4-11:  Little-endian counter (message number N)
```
**AEAD (İlişkili Verili Kimlik Doğrulamalı Şifreleme) Kurgusu:**

AEAD (kimlik doğrulamalı şifreleme ve ilişkili veriler), ChaCha20 akış şifreleyicisini Poly1305 MAC (mesaj doğrulama kodu) ile birleştirir:

1. Anahtar ve nonce (tek-kullanımlık sayı) kullanarak ChaCha20 anahtar akışını üretin
2. Açık metni anahtar akışıyla XOR işlemi uygulayarak şifreleyin
3. Poly1305 MAC (ileti kimlik doğrulama kodu) değerini (ilişkili veri || şifreli metin) üzerinde hesaplayın
4. Şifreli metne 16 baytlık MAC ekleyin

### ChaCha20-Poly1305 ENCRYPT(k, n, plaintext, ad)

Düz metni kimlik doğrulamalı olarak şifreler:

```python
# Inputs
k = 32-byte cipher key
n = 12-byte nonce (first 4 bytes zero, last 8 bytes = message number)
plaintext = data to encrypt (0 to 65519 bytes)
ad = associated data (optional, used in MAC calculation)

# Output
ciphertext = chacha20_encrypt(k, n, plaintext)
mac = poly1305(ad || ciphertext, poly1305_key_gen(k, n))
return ciphertext || mac  # Total length = len(plaintext) + 16
```
**Özellikler:** - Şifreli metin, açık metinle aynı uzunluktadır (akış şifresi) - Çıktı plaintext_length + 16 bayttır (MAC dahildir) - Anahtar gizliyse, tüm çıktı rastgele veriden ayırt edilemez - MAC hem ilişkili veriyi hem de şifreli metni doğrular

### ChaCha20-Poly1305 ŞİFRE ÇÖZ(k, n, ciphertext, ad)

Şifresini çözer ve kimlik doğrulamasını doğrular:

```python
# Split ciphertext and MAC
ct_without_mac = ciphertext[0:-16]
received_mac = ciphertext[-16:]

# Verify MAC
expected_mac = poly1305(ad || ct_without_mac, poly1305_key_gen(k, n))
if not constant_time_compare(received_mac, expected_mac):
    raise AuthenticationError("MAC verification failed")

# Decrypt
plaintext = chacha20_decrypt(k, n, ct_without_mac)
return plaintext
```
**Kritik Güvenlik Gereksinimleri:** - Nonces (tek seferlik değer) aynı anahtarla gönderilen her mesaj için MUTLAKA benzersiz olmalıdır - Nonces KESİNLİKLE yeniden kullanılmamalıdır (yeniden kullanılırsa felaket niteliğinde bir başarısızlık) - MAC doğrulaması zamanlama saldırılarını önlemek için sabit zamanlı karşılaştırma MUTLAKA kullanmalıdır - Başarısız MAC doğrulaması, mesajın tamamen reddedilmesiyle MUTLAKA sonuçlanmalıdır (kısmi şifre çözme yok)

### SHA-256 Özet Fonksiyonu

**Belirtim**: NIST FIPS 180-4

**Özellikler:** - **Çıktı Boyutu**: 32 bayt (256 bit) - **Blok Boyutu**: 64 bayt (512 bit) - **Güvenlik Seviyesi**: 128 bit (çakışma direnci)

**İşlemler:**

### SHA-256 H(p, d)

Kişiselleştirme dizesiyle SHA-256 özeti:

```
H(p, d) := SHA256(p || d)
```
Burada `||` birleştirmeyi ifade eder, `p` kişiselleştirme dizesidir, `d` veridir.

### SHA-256 MixHash(d)

Çalışan karma değerini yeni verilerle günceller:

```
h = SHA256(h || d)
```
Noise el sıkışması boyunca transkript karmasını sürdürmek için kullanılır.

### HKDF Anahtar Türetimi

**Spesifikasyon**: [RFC 5869](https://tools.ietf.org/html/rfc5869)

**Açıklama**: HMAC tabanlı, SHA-256 kullanan anahtar türetme fonksiyonu

**Parametreler:** - **Karma Fonksiyonu**: HMAC-SHA256 - **Tuz Uzunluğu**: En fazla 32 bayt (SHA-256 çıktı boyutu) - **Çıktı Uzunluğu**: Değişken (en fazla 255 * 32 bayt)

**HKDF Fonksiyonu:**

```python
def HKDF(salt, ikm, info, length):
    """
    Args:
        salt: Salt value (32 bytes max for SHA-256)
        ikm: Input key material (any length)
        info: Context-specific info string
        length: Desired output length in bytes
    
    Returns:
        output: Derived key material (length bytes)
    """
    # Extract phase
    prk = HMAC-SHA256(salt, ikm)
    
    # Expand phase
    n = ceil(length / 32)
    t = b''
    okm = b''
    for i in range(1, n + 1):
        t = HMAC-SHA256(prk, t || info || byte(i))
        okm = okm || t
    
    return okm[0:length]
```
**Yaygın Kullanım Kalıpları:**

```python
# Generate two keys (64 bytes total)
keydata = HKDF(chainKey, sharedSecret, "KDFDHRatchetStep", 64)
nextRootKey = keydata[0:31]
chainKey = keydata[32:63]

# Generate session tag (8 bytes)
tagdata = HKDF(chainKey, CONSTANT, "SessionTagKeyGen", 64)
nextChainKey = tagdata[0:31]
sessionTag = tagdata[32:39]

# Generate symmetric key (32 bytes)
keydata = HKDF(chainKey, ZEROLEN, "SymmetricRatchet", 64)
nextChainKey = keydata[0:31]
sessionKey = keydata[32:63]
```
**ECIES'de Kullanılan Bilgi Dizeleri:** - `"KDFDHRatchetStep"` - DH ratchet (kademeli anahtar yenileme mekanizması) için anahtar türetimi - `"TagAndKeyGenKeys"` - Etiket ve anahtar zinciri anahtarlarının başlatılması - `"STInitialization"` - Oturum etiketi ratchet başlatılması - `"SessionTagKeyGen"` - Oturum etiketi üretimi - `"SymmetricRatchet"` - Simetrik anahtar üretimi - `"XDHRatchetTagSet"` - DH ratchet etiket kümesi anahtarı - `"SessionReplyTags"` - NSR etiket kümesi üretimi - `"AttachPayloadKDF"` - NSR payload (yük) anahtar türetimi

### Elligator2 Kodlaması

**Amaç**: X25519 açık anahtarlarını, 32 baytlık eş-dağılımlı rastgele bayt dizilerinden ayırt edilemez olacak şekilde kodlamak.

**Spesifikasyon**: [Elligator2 Makalesi](https://elligator.cr.yp.to/elligator-20130828.pdf)

**Sorun**: Standart X25519 açık anahtarları tanınabilir bir yapıya sahiptir. Bir gözlemci, içerik şifrelenmiş olsa bile, bu anahtarları tespit ederek el sıkışma mesajlarını belirleyebilir.

**Çözüm**: Elligator2, geçerli X25519 açık anahtarlarının yaklaşık %50'si ile rastgele görünümlü 254 bitlik bit dizileri arasında bijektif bir eşleme sağlar.

**Elligator2 (kriptografik bir eşleme tekniği) ile Anahtar Üretimi:**

### Elligator2 GENERATE_PRIVATE_ELG2()

Elligator2 (gizleme amaçlı bir kodlama yöntemi) ile kodlanabilir bir genel anahtara karşılık gelen bir özel anahtar üretir:

```python
while True:
    privkey = CSRNG(32)
    pubkey = DERIVE_PUBLIC(privkey)
    
    # Test if public key is Elligator2-encodable
    try:
        encoded = ENCODE_ELG2(pubkey)
        # Success - this key pair is suitable
        return privkey
    except NotEncodableError:
        # Try again with new random key
        continue
```
**Önemli**: Rastgele oluşturulan özel anahtarların yaklaşık %50'si kodlanamayan açık anahtarlar üretir. Bunlar atılmalı ve yeniden oluşturma denenmelidir.

**Performans Optimizasyonu**: El sıkışma sırasında gecikmeleri önlemek için uygun anahtar çiftlerinden oluşan bir havuzu koruyacak şekilde anahtarları arka plan iş parçacığında önceden oluşturun.

### Elligator2 (elliptik eğri nokta kodlama yöntemi) ENCODE_ELG2(pubkey)

Bir açık anahtarı rastgele görünümlü 32 bayta kodlar:

```python
def ENCODE_ELG2(pubkey):
    """
    Encodes X25519 public key using Elligator2.
    
    Args:
        pubkey: 32-byte X25519 public key (little-endian)
    
    Returns:
        encoded: 32-byte encoded key indistinguishable from random
    
    Raises:
        NotEncodableError: If pubkey cannot be encoded
    """
    # Perform Elligator2 representative calculation
    # Returns 254-bit value (31.75 bytes)
    encodedKey = elligator2_encode(pubkey)
    
    # Add 2 random bits to MSB to make full 32 bytes
    randomByte = CSRNG(1)
    encodedKey[31] |= (randomByte & 0xc0)
    
    return encodedKey
```
**Kodlama Ayrıntıları:** - Elligator2 254 bit üretir (tam 256 değil) - 31. baytın en anlamlı 2 biti rastgele dolgudur - Sonuç 32 baytlık uzayda uniform dağılımlıdır - Geçerli X25519 açık anahtarlarının yaklaşık %50'sini başarıyla kodlar

### Elligator2 DECODE_ELG2(encodedKey)

Orijinal açık anahtara geri çözülür:

```python
def DECODE_ELG2(encodedKey):
    """
    Decodes Elligator2-encoded key back to X25519 public key.
    
    Args:
        encodedKey: 32-byte encoded key
    
    Returns:
        pubkey: 32-byte X25519 public key (little-endian)
    """
    # Mask out 2 random padding bits from MSB
    encodedKey[31] &= 0x3f
    
    # Perform Elligator2 representative inversion
    pubkey = elligator2_decode(encodedKey)
    
    return pubkey
```
**Güvenlik Özellikleri:** - Kodlanmış anahtarlar, hesaplama bakımından rastgele baytlardan ayırt edilemez - Hiçbir istatistiksel test, Elligator2 ile kodlanmış anahtarları güvenilir biçimde tespit edemez - Kod çözme deterministiktir (aynı kodlanmış anahtar her zaman aynı açık anahtarı üretir) - Kodlama, kodlanabilir altkümedeki anahtarların ~50%'si için bijektiftir

**Uygulama Notları:** - El sıkışma sırasında yeniden kodlamayı önlemek için kodlanmış anahtarları oluşturma aşamasında saklayın - Elligator2 (eliptik eğri anahtarlarını rastgele görünümlü baytlara eşleyen bir gizleme tekniği) üretiminden çıkan uygun olmayan anahtarlar, NTCP2 için kullanılabilir (Elligator2 gerektirmez) - Arka planda anahtar oluşturma, performans için kritik önemdedir - Ortalama oluşturma süresi, %50 reddedilme oranı nedeniyle iki katına çıkar

---

## Mesaj Biçimleri

### Genel Bakış

ECIES (Eliptik Eğri Tümleşik Şifreleme Şeması) üç mesaj türü tanımlar:

1. **New Session (NS)**: Alice'den Bob'a gönderilen ilk el sıkışma mesajı
2. **New Session Reply (NSR)**: Bob'un Alice'e el sıkışma yanıtı
3. **Existing Session (ES)**: Her iki yönde de bundan sonraki tüm mesajlar

Tüm mesajlar, ek şifreleme katmanlarıyla birlikte I2NP Garlic Message (I2NP 'Garlic Message' mesaj biçimi) içinde kapsüllenir.

### I2NP Garlic Mesaj Kapsayıcısı (garlic: I2P'de kullanılan, birden fazla mesajı demetleme tekniği)

Tüm ECIES (Eliptik Eğri Tabanlı Entegre Şifreleme Şeması) mesajları, standart I2NP Garlic Message başlıklarıyla kapsüllenir:

```
+----+----+----+----+----+----+----+----+
|type|      msg_id       |  expiration   |
+----+----+----+----+----+----+----+----+
                         |  size   |chks|
+----+----+----+----+----+----+----+----+
|      length       |                   |
+----+----+----+----+                   +
|          encrypted data               |
~                                       ~
```
**Alanlar:** - `type`: 0x26 (Garlic Message - I2P'de özel bir mesaj türü) - `msg_id`: 4 baytlık I2NP mesaj kimliği - `expiration`: 8 baytlık Unix zaman damgası (milisaniye cinsinden) - `size`: 2 baytlık yük boyutu - `chks`: 1 baytlık sağlama toplamı - `length`: 4 baytlık şifrelenmiş veri uzunluğu - `encrypted data`: ECIES ile şifrelenmiş yük

**Amaç**: I2NP katmanında mesaj tanımlama ve yönlendirme sağlar. `length` alanı, alıcıların toplam şifrelenmiş yük boyutunu bilmelerine olanak tanır.

### Yeni Oturum (NS) Mesajı

New Session mesajı, Alice'ten Bob'a yeni bir oturum başlatır. Üç varyantı vardır:

1. **Bağlama ile** (1b): Çift yönlü iletişim için Alice'in statik anahtarını içerir
2. **Bağlama olmadan** (1c): Tek yönlü iletişim için statik anahtarı kullanmaz
3. **Tek Seferlik** (1d): Oturum kurulumu olmadan tek mesaj kipi

### Bağlama içeren NS Mesajı (Tip 1b)

**Kullanım durumu**: Akış, yanıtlanabilir datagramlar, yanıt gerektiren herhangi bir protokol

**Toplam Uzunluk**: 96 + payload_length bayt

**Biçim**:

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
+         Static Key Section            +
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
~          Variable length              ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
```
**Alan Ayrıntıları:**

**Geçici Açık Anahtar** (32 bayt, açık metin): - Alice'in tek kullanımlık X25519 açık anahtarı - Elligator2 ile kodlanmıştır (rastgele veriden ayırt edilemez) - Her NS mesajı için yeni üretilir (asla yeniden kullanılmaz) - Little-endian format (en düşük anlamlı bayt önce)

**Statik Anahtar Bölümü** (32 bayt şifreli, MAC ile 48 bayt): - Alice'in X25519 statik açık anahtarını (32 bayt) içerir - ChaCha20 ile şifrelenir - Poly1305 MAC (16 bayt) ile doğrulanır - Bob tarafından oturumu Alice'in hedefine bağlamak için kullanılır

**Payload Bölümü** (değişken uzunlukta şifrelenmiş, +16 bayt MAC): - Garlic Clove (garlic şifrelemesindeki alt-mesaj) öğelerini ve diğer blokları içerir - İlk blok olarak DateTime bloğunu içermelidir - Genellikle uygulama verisi içeren Garlic Clove bloklarını içerir - Anında ratchet (anahtar yenilemesi) için NextKey bloğunu içerebilir - ChaCha20 ile şifrelenir - Poly1305 MAC (16 bayt) ile doğrulanır

**Güvenlik Özellikleri:** - Geçici anahtar ileri gizlilik bileşeni sağlar - Statik anahtar, Alice'i kimlik doğrular (hedefe bağlayarak) - Her iki bölüm de alan ayrımı için ayrı MAC'lere sahiptir - Tüm el sıkışması 2 DH (Diffie-Hellman) işlemi gerçekleştirir (es, ss)

### Bağlama olmadan NS mesajı (Tür 1c)

**Kullanım Senaryosu**: Yanıtın beklenmediği veya istenmediği ham datagramlar

**Toplam Uzunluk**: 96 + payload_length bayt

**Biçim**:

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
|           All zeros                   |
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
~          Variable length              ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
```
**Temel Fark**: Bayraklar Bölümü, statik anahtar yerine 32 bayt sıfır içerir.

**Algılama**: Bob, 32 baytlık bölümü şifresini çözerek ve tüm baytların sıfır olup olmadığını kontrol ederek mesaj türünü belirler: - Tümü sıfır → Bağlı olmayan oturum (type 1c) - Sıfır olmayan → Statik anahtarlı bağlı oturum (type 1b)

**Özellikler:** - Statik anahtar olmaması, Alice'in hedefiyle kriptografik bir bağ kurulmadığı anlamına gelir - Bob yanıt gönderemez (bilinen bir hedef yok) - Yalnızca 1 DH (Diffie-Hellman) işlemi gerçekleştirir - Noise "N" örüntüsünü "IK" yerine izler - Yanıtların hiç gerekmediği durumlarda daha verimlidir

**Flags Section** (gelecekte kullanım için ayrılmış): Şu anda tamamı sıfır. Gelecek sürümlerde özellik müzakeresi için kullanılabilir.

### NS Tek Seferlik Mesaj (Tür 1d)

**Kullanım Senaryosu**: Oturum veya yanıt beklenmeyen tek bir anonim mesaj

**Toplam Uzunluk**: 96 + payload_length bayt

**Biçim**: Bağlama olmadan NS ile aynıdır (tip 1c)

**Ayrım**:  - Tip 1c aynı oturumda birden fazla mesaj gönderebilir (ES mesajları ardından gelir) - Tip 1d oturum kurulumu olmadan tam olarak bir mesaj gönderir - Uygulamada, gerçekleştirimler başlangıçta bunları aynı şekilde ele alabilir

**Özellikler:** - Maksimum anonimlik (sabit anahtar yok, oturum yok) - Hiçbir taraf oturum durumunu tutmaz - Noise "N" desenini izler - Tek DH işlemi

### Yeni Oturum Yanıtı (NSR) Mesajı

Bob, Alice'in NS mesajına yanıt olarak bir veya daha fazla NSR mesajı gönderir. NSR, Noise IK el sıkışmasını (Noise protokolünün IK kalıbı) tamamlar ve iki yönlü bir oturum kurar.

**Toplam Uzunluk**: 72 + payload_length bayt

**Biçim**:

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
+  (MAC) for Key Section (empty)        +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~          Variable length              ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
```
**Alan Ayrıntıları:**

**Oturum Etiketi** (8 bayt, açık metin): - NSR etiket kümesinden üretilir (bkz. KDF bölümleri) - Bu yanıtı Alice'in NS mesajıyla ilişkilendirir - Alice'in bu NSR'nin hangi NS'ye yanıt verdiğini belirlemesini sağlar - Tek seferlik kullanım (asla yeniden kullanılmaz)

**Geçici Açık Anahtar** (32 bayt, açık metin): - Bob'un tek kullanımlık X25519 açık anahtarı - Elligator2 ile kodlanmış - Her NSR mesajı için yeni üretilir - Gönderilen her NSR için farklı olmalıdır

**Key Section MAC** (16 bayt): - Boş veriyi (ZEROLEN) kimlik doğrular - Noise IK protokolünün bir parçası (se pattern) - İlişkili veri olarak transkript karmasını kullanır - NSR'nin NS'ye bağlanması için kritiktir

**Yük Bölümü** (değişken uzunlukta): - Garlic cloves (garlic mesajındaki tekil alt-iletiler) ve bloklar içerir - Genellikle uygulama katmanı yanıtlarını içerir - Boş olabilir (ACK-only NSR) - Maksimum boyut: 65519 bayt (65535 - 16 bayt MAC)

**Birden Çok NSR Mesajı:**

Bob, bir NS'ye (istek mesajı) yanıt olarak birden fazla NSR (yanıt mesajı) gönderebilir: - Her NSR benzersiz bir geçici anahtara sahiptir - Her NSR benzersiz bir oturum etiketine sahiptir - Alice, el sıkışma işlemini tamamlamak için aldığı ilk NSR'yi kullanır - Diğer NSR'ler yedeklilik içindir (paket kaybı durumunda)

**Kritik Zamanlama:** - Alice, ES mesajları göndermeden önce bir NSR almalıdır - Bob, ES mesajları göndermeden önce bir ES mesajı almalıdır - NSR, split() işlemi aracılığıyla çift yönlü oturum anahtarları kurar

**Güvenlik Özellikleri:** - Noise IK el sıkışmasını tamamlar - 2 ek DH işlemi gerçekleştirir (ee, se) - NS+NSR genelinde toplam 4 DH işlemi - Karşılıklı kimlik doğrulamayı sağlar (Seviye 2) - NSR yükü için zayıf ileri gizlilik (Seviye 4) sağlar

### Mevcut Oturum (ES) Mesajı

NS/NSR el sıkışmasından sonra tüm mesajlar Existing Session (mevcut oturum) formatını kullanır. ES mesajları hem Alice hem de Bob tarafından çift yönlü olarak kullanılır.

**Toplam Uzunluk**: 8 + payload_length + 16 bayt (en az 24 bayt)

**Biçim**:

```
+----+----+----+----+----+----+----+----+
|       Session Tag   8 bytes           |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~          Variable length              ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+              (MAC)                    +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
```
**Alan Ayrıntıları:**

**Oturum Etiketi** (8 bayt, açık metin): - Mevcut giden tagset (etiket kümesi) temel alınarak üretilir - Oturumu ve mesaj numarasını tanımlar - Alıcı, oturum anahtarını ve nonce (tek seferlik değer) bulmak için etiketi arar - Tek seferlik kullanım (her etiket tam olarak bir kez kullanılır) - Biçim: HKDF çıktısının ilk 8 baytı

**Yük Bölümü** (değişken uzunlukta): - Garlic cloves (garlic encryption bağlamında 'clove' olarak adlandırılan alt mesajlar) ve bloklar içerir - Gerekli blok yoktur (boş olabilir) - Yaygın bloklar: Garlic Clove, NextKey, ACK, ACK Request, Padding - Maksimum boyut: 65519 bayt (65535 - 16 bayt MAC)

**MAC** (16 bayt): - Poly1305 kimlik doğrulama etiketi - Tüm yük üzerinde hesaplanır - İlişkili veri: 8 baytlık oturum etiketi - Doğrulaması başarılı olmalıdır; aksi halde ileti reddedilir

**Etiket Sorgulama Süreci:**

1. Alıcı 8 baytlık etiketi çıkarır
2. Geçerli tüm gelen etiket kümelerinde etiketi arar
3. İlişkili oturum anahtarını ve mesaj numarası N'yi alır
4. Nonce (tek kullanımlık sayı) oluşturur: `[0x00, 0x00, 0x00, 0x00, N (8 bytes little-endian)]`
5. Etiketi ilişkili veri olarak kullanarak AEAD (İlişkili verili kimlik doğrulamalı şifreleme) ile yükün şifresini çözer
6. Etiketi etiket kümesinden kaldırır (tek kullanımlık)
7. Çözülmüş blokları işler

**Oturum Etiketi Bulunamadı:**

Etiket herhangi bir tagset (etiket kümesi) içinde bulunamazsa: - NS mesajı olabilir → NS şifre çözmeyi dene - NSR mesajı olabilir → NSR şifre çözmeyi dene - Sıra dışı bir ES olabilir → tagset güncellemesi için kısa süre bekle - Yeniden oynatma saldırısı olabilir → reddet - Bozuk veri olabilir → reddet

**Boş Yük:**

ES mesajları boş yükler (0 bayt) içerebilir: - ACK Request alındığında açık bir ACK işlevi görür - Uygulama verisi olmadan protokol katmanı yanıtı sağlar - Yine de bir session tag (oturum etiketi) tüketir - Üst katmanın hemen gönderecek verisi olmadığında kullanışlıdır

**Güvenlik Özellikleri:** - NSR alındıktan sonra tam ileri gizlilik (Seviye 5) - AEAD (ek verilerle kimlik doğrulamalı şifreleme) aracılığıyla kimliği doğrulanmış şifreleme - Etiket, ek ilişkili veri olarak işlev görür - Ratchet (anahtar ilerletme mekanizması) gerekli hale gelmeden önce etiket kümesi başına en fazla 65535 ileti

---

## Anahtar Türetme Fonksiyonları

Bu bölüm, ECIES'te kullanılan tüm KDF işlemlerini (anahtar türetme fonksiyonu) belgeler ve tam kriptografik türetimleri gösterir.

### Notasyon ve Sabitler

**Sabitler:** - `ZEROLEN` - Sıfır uzunlukta bayt dizisi (boş dize) - `||` - Birleştirme işleci

**Değişkenler:** - `h` - Transkriptin kümülatif özeti (32 bayt) - `chainKey` - HKDF için zincirleme anahtarı (32 bayt) - `k` - Simetrik şifreleme anahtarı (32 bayt) - `n` - Nonce (tek-kullanımlık sayı) / mesaj numarası

**Anahtarlar:** - `ask` / `apk` - Alice'in statik özel/açık anahtarı - `aesk` / `aepk` - Alice'in geçici özel/açık anahtarı - `bsk` / `bpk` - Bob'un statik özel/açık anahtarı - `besk` / `bepk` - Bob'un geçici özel/açık anahtarı

### NS Mesajı KDF'leri (anahtar türetme fonksiyonları)

### KDF 1: Başlangıç Zincir Anahtarı

Protokol ilklendirmesinde bir kez yapılır (önceden hesaplanabilir):

```python
# Protocol name (40 bytes, ASCII, no null termination)
protocol_name = "Noise_IKelg2+hs2_25519_ChaChaPoly_SHA256"

# Initialize hash
h = SHA256(protocol_name)

# Initialize chaining key
chainKey = h

# MixHash with empty prologue
h = SHA256(h)

# State: chainKey and h initialized
# Can be precalculated for all outbound sessions
```
**Sonuç:** - `chainKey` = Tüm sonraki KDF'ler (anahtar türetme fonksiyonları) için başlangıç zincirleme anahtarı - `h` = Başlangıç özet transkripti

### KDF 2: Bob'un Statik Anahtar Karıştırması

Bob bunu bir kez yapar (tüm gelen oturumlar için önceden hesaplanabilir):

```python
# Bob's static keys (published in LeaseSet)
bsk = GENERATE_PRIVATE()
bpk = DERIVE_PUBLIC(bsk)

# Mix Bob's public key into hash
h = SHA256(h || bpk)

# State: h updated with Bob's identity
# Can be precalculated by Bob for all inbound sessions
```
### KDF 3: Alice'nin Geçici Anahtar Üretimi

Alice her NS message (NS mesajı) için yeni anahtarlar oluşturur:

```python
# Generate ephemeral key pair suitable for Elligator2
aesk = GENERATE_PRIVATE_ELG2()
aepk = DERIVE_PUBLIC(aesk)

# Mix ephemeral public key into hash
h = SHA256(h || aepk)

# Elligator2 encode for transmission
elg2_aepk = ENCODE_ELG2(aepk)

# State: h updated with Alice's ephemeral key
# Send elg2_aepk as first 32 bytes of NS message
```
### KDF 4: NS Statik Anahtar Bölümü (es DH)

Alice'in statik anahtarını şifrelemek için anahtarlar türetir:

```python
# Perform first DH (ephemeral-static)
sharedSecret = DH(aesk, bpk)  # Alice computes
# Equivalent: sharedSecret = DH(bsk, aepk)  # Bob computes

# Derive cipher key from shared secret
keydata = HKDF(chainKey, sharedSecret, "", 64)
chainKey = keydata[0:31]
k = keydata[32:63]

# AEAD encryption parameters
nonce = 0
associated_data = h  # Current hash transcript

# Encrypt static key section
if binding_requested:
    plaintext = apk  # Alice's static public key (32 bytes)
else:
    plaintext = bytes(32)  # All zeros for unbound

ciphertext = ENCRYPT(k, nonce, plaintext, associated_data)
# ciphertext = 32 bytes encrypted + 16 bytes MAC = 48 bytes

# Mix ciphertext into hash
h = SHA256(h || ciphertext)

# State: Static key section encrypted, h updated
# Send ciphertext (48 bytes) as next part of NS message
```
### KDF (Anahtar Türetme Fonksiyonu) 5: NS Payload Bölümü (ss DH, yalnızca bağlama amaçlı)

Bağlı oturumlarda, yükü şifrelemek için ikinci DH'yi (Diffie-Hellman anahtar değişimi) gerçekleştirin:

```python
if binding_requested:
    # Alice's static keys
    ask = GENERATE_PRIVATE()  # Alice's long-term key
    apk = DERIVE_PUBLIC(ask)
    
    # Perform second DH (static-static)
    sharedSecret = DH(ask, bpk)  # Alice computes
    # Equivalent: sharedSecret = DH(bsk, apk)  # Bob computes
    
    # Derive cipher key
    keydata = HKDF(chainKey, sharedSecret, "", 64)
    chainKey = keydata[0:31]
    k = keydata[32:63]
    
    nonce = 0
    associated_data = h
else:
    # Unbound: reuse keys from static key section
    # chainKey and k unchanged
    nonce = 1  # Increment nonce (reusing same key)
    associated_data = h

# Encrypt payload
payload = build_payload()  # DateTime + Garlic Cloves + etc.
ciphertext = ENCRYPT(k, nonce, payload, associated_data)

# Mix ciphertext into hash
h = SHA256(h || ciphertext)

# State: Payload encrypted, h contains complete NS transcript
# Save chainKey and h for NSR processing
# Send ciphertext as final part of NS message
```
**Önemli Notlar:**

1. **Bound (bağlı) vs Unbound (bağsız)**: 
   - Bound 2 DH işlemi gerçekleştirir (es + ss)
   - Unbound 1 DH işlemi gerçekleştirir (yalnızca es)
   - Unbound, yeni bir anahtar türetmek yerine nonce (tek kullanımlık sayı) değerini artırır

2. **Anahtar Yeniden Kullanım Güvenliği**:
   - Farklı nonce'lar (0 ve 1), anahtarın/nonce'un yeniden kullanılmasını önler
   - Farklı ilişkili veriler (h farklı) alan ayrımı sağlar

3. **Hash Transkripti**:
   - `h` artık şunları içerir: protocol_name, empty prologue (önsöz), bpk, aepk, static_key_ciphertext, payload_ciphertext
   - Bu transkript, NS mesajının tüm parçalarını birbirine bağlar

### NSR Reply Tagset KDF (yanıt etiket kümesi için anahtar türetme fonksiyonu)

Bob, NSR (bir mesaj türü) mesajları için etiketler oluşturur:

```python
# Chain key from NS payload section
# chainKey = final chainKey from NS KDF

# Generate tagset key
tagsetKey = HKDF(chainKey, ZEROLEN, "SessionReplyTags", 32)

# Initialize NSR tagset (see DH_INITIALIZE below)
tagset_nsr = DH_INITIALIZE(chainKey, tagsetKey)

# Get tag for this NSR
tagsetEntry = tagset_nsr.GET_NEXT_ENTRY()
tag = tagsetEntry.SESSION_TAG  # 8 bytes

# State: tag available for NSR message
# Send tag as first 8 bytes of NSR
```
### NSR Mesajı KDF'leri (anahtar türetme fonksiyonları)

### KDF 6: NSR Geçici Anahtar Üretimi

Bob, her NSR için yeni bir geçici anahtar üretir:

```python
# Mix tag into hash (I2P extension to Noise)
h = SHA256(h || tag)

# Generate ephemeral key pair
besk = GENERATE_PRIVATE_ELG2()
bepk = DERIVE_PUBLIC(besk)

# Mix ephemeral public key into hash
h = SHA256(h || bepk)

# Elligator2 encode for transmission
elg2_bepk = ENCODE_ELG2(bepk)

# State: h updated with tag and Bob's ephemeral key
# Send elg2_bepk as bytes 9-40 of NSR message
```
### KDF 7: NSR Anahtar Bölümü (ee ve se DH)

NSR anahtar bölümü için anahtarlar türetir:

```python
# Perform third DH (ephemeral-ephemeral)
sharedSecret_ee = DH(aesk, bepk)  # Alice computes
# Equivalent: sharedSecret_ee = DH(besk, aepk)  # Bob computes

# Mix ee into chain
keydata = HKDF(chainKey, sharedSecret_ee, "", 32)
chainKey = keydata[0:31]

# Perform fourth DH (static-ephemeral)
sharedSecret_se = DH(ask, bepk)  # Alice computes
# Equivalent: sharedSecret_se = DH(besk, apk)  # Bob computes

# Derive cipher key from se
keydata = HKDF(chainKey, sharedSecret_se, "", 64)
chainKey = keydata[0:31]
k = keydata[32:63]

# AEAD encryption of empty data (key section has no payload)
nonce = 0
associated_data = h
ciphertext = ENCRYPT(k, nonce, ZEROLEN, associated_data)
# ciphertext = 16 bytes (MAC only, no plaintext)

# Mix ciphertext into hash
h = SHA256(h || ciphertext)

# State: Key section encrypted, chainKey contains all 4 DH results
# Send ciphertext (16 bytes MAC) as bytes 41-56 of NSR
```
**Kritik**: Bu, Noise IK el sıkışmasını tamamlar. `chainKey` artık 4 DH işleminin tümünden (es, ss, ee, se) gelen katkıları içerir.

### KDF 8: NSR Yük Bölümü

NSR yükü şifrelemesi için anahtarlar türetir:

```python
# Split chainKey into bidirectional keys
keydata = HKDF(chainKey, ZEROLEN, "", 64)
k_ab = keydata[0:31]   # Alice → Bob key
k_ba = keydata[32:63]  # Bob → Alice key

# Initialize ES tagsets for both directions
tagset_ab = DH_INITIALIZE(chainKey, k_ab)  # Alice → Bob
tagset_ba = DH_INITIALIZE(chainKey, k_ba)  # Bob → Alice

# Derive NSR payload key (Bob → Alice)
k_nsr = HKDF(k_ba, ZEROLEN, "AttachPayloadKDF", 32)

# Encrypt NSR payload
nonce = 0
associated_data = h  # Binds payload to entire NSR
payload = build_payload()  # Usually application reply
ciphertext = ENCRYPT(k_nsr, nonce, payload, associated_data)

# State: Bidirectional ES sessions established
# tagset_ab and tagset_ba ready for ES messages
# Send ciphertext as bytes 57+ of NSR message
```
**Önemli Notlar:**

1. **Bölme İşlemi**: 
   - Her yön için bağımsız anahtarlar oluşturur
   - Alice→Bob ve Bob→Alice yönleri arasında anahtarın yeniden kullanılmasını önler

2. **NSR Yük Bağlama**:
   - Yükü el sıkışmaya bağlamak için ilişkili veri olarak `h` kullanır
   - Ayrı bir KDF (anahtar türetme fonksiyonu) ("AttachPayloadKDF") alan ayrımı sağlar

3. **ES (ES adlı mesaj) Hazırlığı**:
   - NSR (NSR adlı mesaj) sonrasında, her iki taraf da ES mesajları gönderebilir
   - Alice, ES göndermeden önce NSR almalıdır
   - Bob, ES göndermeden önce ES almalıdır

### ES Mesaj KDF'leri (anahtar türetme fonksiyonları)

ES iletileri, tagsets (etiket kümeleri) içindeki önceden oluşturulmuş oturum anahtarlarını kullanır:

```python
# Sender gets next tag and key
tagsetEntry = outbound_tagset.GET_NEXT_ENTRY()
tag = tagsetEntry.SESSION_TAG     # 8 bytes
k = tagsetEntry.SESSION_KEY       # 32 bytes
N = tagsetEntry.INDEX             # Message number

# Construct nonce (12 bytes)
nonce = [0x00, 0x00, 0x00, 0x00] + little_endian_8_bytes(N)

# AEAD encryption
associated_data = tag  # Tag is associated data
payload = build_payload()
ciphertext = ENCRYPT(k, nonce, payload, associated_data)

# Send: tag || ciphertext (8 + len(ciphertext) bytes)
```
**Alıcı Süreci:**

```python
# Extract tag
tag = message[0:8]

# Look up tag in inbound tagsets
tagsetEntry = inbound_tagset.GET_SESSION_KEY(tag)
if tagsetEntry is None:
    # Not an ES message, try NS/NSR decryption
    return try_handshake_decryption(message)

k = tagsetEntry.SESSION_KEY
N = tagsetEntry.INDEX

# Construct nonce
nonce = [0x00, 0x00, 0x00, 0x00] + little_endian_8_bytes(N)

# AEAD decryption
associated_data = tag
ciphertext = message[8:]
try:
    payload = DECRYPT(k, nonce, ciphertext, associated_data)
except AuthenticationError:
    # MAC verification failed, reject message
    return reject_message()

# Process payload blocks
process_payload(payload)

# Remove tag from tagset (one-time use)
inbound_tagset.remove(tag)
```
### DH_INITIALIZE Fonksiyonu

Tek bir yön için bir tagset (etiket kümesi) oluşturur:

```python
def DH_INITIALIZE(rootKey, k):
    """
    Initializes a tagset with session tag and symmetric key ratchets.
    
    Args:
        rootKey: Chain key from previous DH ratchet (32 bytes)
        k: Key material from split() or DH ratchet (32 bytes)
    
    Returns:
        tagset: Initialized tagset object
    """
    # Derive next root key and chain key
    keydata = HKDF(rootKey, k, "KDFDHRatchetStep", 64)
    nextRootKey = keydata[0:31]
    chainKey_tagset = keydata[32:63]
    
    # Derive separate chain keys for tags and keys
    keydata = HKDF(chainKey_tagset, ZEROLEN, "TagAndKeyGenKeys", 64)
    sessTag_ck = keydata[0:31]   # Session tag chain key
    symmKey_ck = keydata[32:63]  # Symmetric key chain key
    
    # Create tagset object
    tagset = Tagset()
    tagset.nextRootKey = nextRootKey
    tagset.sessTag_chainKey = sessTag_ck
    tagset.symmKey_chainKey = symmKey_ck
    tagset.lastIndex = -1
    
    return tagset
```
**Kullanım Bağlamları:**

1. **NSR Etiket Kümesi**: `DH_INITIALIZE(chainKey_from_NS, tagsetKey_NSR)`
2. **ES Etiket Kümeleri**: `DH_INITIALIZE(chainKey_from_NSR, k_ab or k_ba)`
3. **Ratcheted (kademeli) Etiket Kümeleri**: `DH_INITIALIZE(nextRootKey_from_previous, tagsetKey_from_DH)`

---

## Ratchet Mekanizmaları (tek yönlü anahtar yenileme mekanizmaları)

ECIES, ileri gizlilik ve verimli oturum yönetimi sağlamak için üç eşzamanlı ratchet (anahtar yenileme mekanizması) kullanır.

### Ratchet (mandal mekanizması) Genel Bakış

**Üç Ratchet (ilerlemeli anahtar yenileme mekanizması) Türleri:**

1. **DH Ratchet** (tek yönlü anahtar yenileme mekanizması): Yeni kök anahtarlar üretmek için Diffie-Hellman anahtar değişimleri gerçekleştirir
2. **Session Tag Ratchet**: Tek kullanımlık oturum etiketlerini belirlenimli olarak türetir
3. **Symmetric Key Ratchet**: Mesaj şifrelemesi için oturum anahtarlarını türetir

**İlişki:**

```
DH Ratchet (periodic)
    ↓
Creates new tagset
    ↓
Session Tag Ratchet (per message) ← synchronized → Symmetric Key Ratchet (per message)
    ↓                                                      ↓
Session Tags (8 bytes each)                      Session Keys (32 bytes each)
```
**Temel Özellikler:**

- **Gönderici**: Etiketleri ve anahtarları talep üzerine üretir (depolama gerekmez)
- **Alıcı**: İleri bakış penceresi için etiketleri önceden üretir (depolama gerekir)
- **Senkronizasyon**: Etiket indeksi, anahtar indeksini belirler (N_tag = N_key)
- **İleri Gizlilik**: Periyodik DH ratchet (Diffie-Hellman temelli artımlı anahtar yenileme mekanizması) ile sağlanır
- **Verimlilik**: Alıcı, etiket alınana kadar anahtar hesaplamasını erteleyebilir

### DH Ratchet (Diffie-Hellman temelli kademeli anahtar yenileme mekanizması)

DH ratchet (Diffie-Hellman tabanlı kademeli anahtar yenileme mekanizması), periyodik olarak yeni geçici anahtarlar değiş tokuş ederek ileri gizlilik sağlar.

### DH Ratchet (Diffie-Hellman anahtar yenileme mekanizması) Frekansı

**Gerekli Ratchet (adım adım anahtar yenileme mekanizması) Koşulları:** - Etiket kümesi tükenmeye yaklaşıyor (azami etiket değeri 65535'tir) - Uygulamaya özgü politikalar:   - Mesaj sayısı eşiği (örn. her 4096 mesajda bir)   - Zaman eşiği (örn. her 10 dakikada bir)   - Veri hacmi eşiği (örn. her 100 MB'de bir)

**Önerilen İlk Ratchet (kademeli anahtar yenileme mekanizması)**: Sınıra ulaşmamak için etiket numarası 4096 civarında

**Maksimum Değerler:** - **Maksimum tag set (etiket kümesi) kimliği**: 65535 - **Maksimum anahtar kimliği**: 32767 - **Tag set başına maksimum ileti**: 65535 - **Oturum başına teorik maksimum veri**: ~6.9 TB (64K tag sets × 64K ileti × 1730 bayt ortalama)

### DH Ratchet (DH "ratchet" mekanizması) Etiket ve Anahtar Kimlikleri

**İlk Etiket Kümesi** (el sıkışması sonrası): - Etiket kümesi kimliği: 0 - Henüz hiçbir NextKey bloğu gönderilmedi - Hiçbir anahtar kimliği atanmadı

**İlk Ratchet (kademeli anahtar yenileme mekanizması) Sonrası**: - Etiket kümesi kimliği: 1 = (1 + Alice'in anahtar kimliği + Bob'un anahtar kimliği) = (1 + 0 + 0) - Alice, anahtar kimliği 0 olan NextKey (sonraki anahtar) gönderir - Bob, anahtar kimliği 0 olan NextKey ile yanıtlar

**Sonraki Etiket Kümeleri**: - Etiket kümesi kimliği = 1 + gönderenin anahtar kimliği + alıcının anahtar kimliği - Örnek: Etiket kümesi 5 = (1 + sender_key_2 + receiver_key_2)

**Etiket Kümesi İlerleme Tablosu:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Tag Set ID</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Sender Key ID</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Receiver Key ID</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">n/a</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">n/a</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Initial tag set (post-NSR)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">First ratchet (both generate new keys)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Sender generates new key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Receiver generates new key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Sender generates new key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Receiver generates new key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">...</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">...</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">...</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Pattern repeats</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">65534</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32767 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32766</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Second-to-last tag set</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">65535</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32767</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32767 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Final tag set</td>
    </tr>
  </tbody>
</table>
\* = Yeni anahtar bu ratchet (kademeli anahtar yenileme mekanizması) sırasında üretildi

**Anahtar Kimliği Kuralları:** - Kimlikler 0'dan başlayarak ardışık olarak verilir - Kimlikler yalnızca yeni bir anahtar oluşturulduğunda artar - Maksimum anahtar kimliği 32767'dir (15 bit) - Anahtar kimliği 32767'den sonra yeni oturum gereklidir

### DH Ratchet (kademeli anahtar yenileme mekanizması) Mesaj Akışı

**Roller:** - **Tag Sender** (Etiket Gönderici): giden etiket kümesine sahiptir, iletiler gönderir - **Tag Receiver** (Etiket Alıcı): gelen etiket kümesine sahiptir, iletiler alır

**Kalıp:** Etiket göndericisi, etiket kümesi neredeyse tükendiğinde ratchet (aşamalı anahtar yenileme mekanizması) başlatır.

**Mesaj Akış Diyagramı:**

```
Tag Sender                         Tag Receiver

       ... using tag set #0 ...

(Tag set #0 approaching exhaustion)
(Generate new key #0)

NextKey forward, request reverse, with key #0  -------->
(Repeat until NextKey ACK received)
                                   (Generate new key #0)
                                   (Perform DH: sender_key_0 × receiver_key_0)
                                   (Create inbound tag set #1)

        <---------------           NextKey reverse, with key #0
                                   (Repeat until tag from tag set #1 received)

(Receive NextKey with key #0)
(Perform DH: sender_key_0 × receiver_key_0)
(Create outbound tag set #1)


       ... using tag set #1 ...


(Tag set #1 approaching exhaustion)
(Generate new key #1)

NextKey forward, with key #1        -------->
(Repeat until NextKey ACK received)
                                   (Reuse existing key #0)
                                   (Perform DH: sender_key_1 × receiver_key_0)
                                   (Create inbound tag set #2)

        <--------------            NextKey reverse, id 0 (ACK)
                                   (Repeat until tag from tag set #2 received)

(Receive NextKey with id 0)
(Perform DH: sender_key_1 × receiver_key_0)
(Create outbound tag set #2)


       ... using tag set #2 ...


(Tag set #2 approaching exhaustion)
(Reuse existing key #1)

NextKey forward, request reverse, id 1  -------->
(Repeat until NextKey received)
                                   (Generate new key #1)
                                   (Perform DH: sender_key_1 × receiver_key_1)
                                   (Create inbound tag set #3)

        <--------------            NextKey reverse, with key #1

(Receive NextKey with key #1)
(Perform DH: sender_key_1 × receiver_key_1)
(Create outbound tag set #3)


       ... using tag set #3 ...

       (Pattern repeats: even-numbered tag sets
        use forward key, odd-numbered use reverse key)
```
**Ratchet (mandal mekanizması) örüntüleri:**

**Çift Numaralı Etiket Kümeleri Oluşturma** (2, 4, 6, ...): 1. Gönderen yeni bir anahtar üretir 2. Gönderen yeni anahtar içeren NextKey bloğunu gönderir 3. Alıcı, eski anahtar kimliğiyle NextKey bloğunu gönderir (ACK) 4. Her ikisi de (yeni gönderen anahtarı × eski alıcı anahtarı) ile DH (Diffie-Hellman anahtar değişimi) gerçekleştirir

**Tek Sayılı Etiket Kümeleri Oluşturma** (3, 5, 7, ...): 1. Gönderici ters yöndeki anahtarı talep eder (istek bayrağı ile NextKey gönderir) 2. Alıcı yeni bir anahtar üretir 3. Alıcı yeni anahtarla NextKey bloğunu gönderir 4. Her ikisi de (eski gönderici anahtarı × yeni alıcı anahtarı) ile DH (Diffie-Hellman anahtar değişimi) gerçekleştirir

### NextKey (bir sonraki anahtar) Blok Biçimi

Ayrıntılı NextKey (sonraki anahtar) blok belirtimi için Payload Format bölümüne bakın.

**Temel Öğeler:** - **Bayrak baytı**:   - Bit 0: Anahtar mevcut (1) veya yalnızca kimlik (0)   - Bit 1: Reverse key (ters anahtar) (1) veya forward key (ileri anahtar) (0)   - Bit 2: reverse key talep et (1) veya talep yok (0) - **Anahtar Kimliği**: 2 bayt, big-endian (0-32767) - **Açık Anahtar**: 32 bayt X25519 (eğer bit 0 = 1 ise)

**Örnek NextKey Blocks (bir sonraki anahtar blokları):**

```python
# Sender initiates ratchet with new key (key ID 0, tag set 1)
NextKey(flags=0x01, key_id=0, pubkey=sender_key_0)

# Receiver replies with new key (key ID 0, tag set 1)
NextKey(flags=0x03, key_id=0, pubkey=receiver_key_0)

# Sender ratchets again with new key (key ID 1, tag set 2)
NextKey(flags=0x01, key_id=1, pubkey=sender_key_1)

# Receiver ACKs with old key ID (tag set 2)
NextKey(flags=0x02, key_id=0)

# Sender requests reverse key (tag set 3)
NextKey(flags=0x04, key_id=1)

# Receiver sends new reverse key (key ID 1, tag set 3)
NextKey(flags=0x03, key_id=1, pubkey=receiver_key_1)
```
### DH Ratchet KDF (Anahtar Türetme Fonksiyonu)

Yeni anahtarlar değiş tokuş edildiğinde:

```python
# Tag sender generates or reuses key
if generating_new:
    sender_sk = GENERATE_PRIVATE()
    sender_pk = DERIVE_PUBLIC(sender_sk)
else:
    # Reuse existing key pair
    sender_pk = existing_sender_pk

# Tag receiver generates or reuses key
if generating_new:
    receiver_sk = GENERATE_PRIVATE()
    receiver_pk = DERIVE_PUBLIC(receiver_sk)
else:
    # Reuse existing key pair
    receiver_pk = existing_receiver_pk

# Both parties perform DH
sharedSecret = DH(sender_sk, receiver_pk)

# Derive tagset key
tagsetKey = HKDF(sharedSecret, ZEROLEN, "XDHRatchetTagSet", 32)

# Get next root key from previous tagset
rootKey = previous_tagset.nextRootKey

# Initialize new tagset
new_tagset = DH_INITIALIZE(rootKey, tagsetKey)

# Tag sender: outbound tagset
# Tag receiver: inbound tagset
```
**Kritik Zamanlama:**

**Etiket Gönderici:** - Yeni giden etiket kümesini hemen oluşturur - Yeni etiketleri hemen kullanmaya başlar - Eski giden etiket kümesini siler

**Etiket Alıcısı:** - Yeni bir gelen etiket kümesi oluşturur - Tolerans süresi (3 dakika) boyunca eski gelen etiket kümesini muhafaza eder - Tolerans süresi boyunca hem eski hem de yeni etiket kümelerinden etiketleri kabul eder - Tolerans süresinden sonra eski gelen etiket kümesini siler

### DH Ratchet (kademeli Diffie-Hellman anahtar yenileme mekanizması) Durum Yönetimi

**Gönderici Durumu:** - Mevcut giden etiket kümesi - Etiket kümesi kimliği ve anahtar kimlikleri - Sonraki kök anahtar (bir sonraki ratchet (anahtar ilerletme mekanizması) için) - Mevcut etiket kümesindeki ileti sayısı

**Alıcı durumu:** - Güncel gelen etiket kümesi(leri) (geçiş süresinde 2 olabilir) - Boşluk tespiti için önceki ileti numaraları (PN) - Önceden üretilmiş etiketler için ileriye bakış penceresi - Sonraki kök anahtar (bir sonraki ratchet (kademeli anahtar yenileme mekanizması) için)

**Durum Geçiş Kuralları:**

1. **İlk Ratchet (kademeli anahtar yenileme) Öncesi**:
   - Etiket kümesi 0 kullanılıyor (NSR'den)
   - Hiçbir anahtar kimliği atanmadı

2. **Ratchet (kademeli anahtar yenileme mekanizması) Başlatma**:
   - Yeni anahtar üret (eğer gönderici bu turda üretiyorsa)
   - ES mesajında NextKey bloğunu gönder
   - Yeni bir giden etiket kümesi oluşturmadan önce NextKey yanıtını bekle

3. **Ratchet (anahtar sürgüsü) İsteğinin Alınması**:
   - Yeni bir anahtar üret (bu turda alıcı üretiyorsa)
   - Alınan anahtarla DH (Diffie-Hellman) gerçekleştir
   - Yeni bir gelen etiket kümesi oluştur
   - NextKey yanıtı gönder
   - Eski gelen etiket kümesini bir müsaade süresi boyunca koru

4. **Ratchet'in Tamamlanması (anahtar yenileme mekanizması)**:
   - NextKey yanıtını alın
   - DH (Diffie-Hellman anahtar değişimi) gerçekleştirin
   - Yeni giden etiket kümesi oluşturun
   - Yeni etiketleri kullanmaya başlayın

### Session Tag Ratchet (oturum etiketi için kademeli güncelleme mekanizması)

Session tag ratchet (kademeli kriptografik mekanizma), tek kullanımlık 8 baytlık oturum etiketlerini deterministik olarak üretir.

### Oturum Etiketi Ratchet'in (kademeli anahtar yenileme mekanizması) Amacı

- Açık etiket iletiminin yerini alır (ElGamal 32 baytlık etiketler gönderirdi)
- Alıcının ileri bakış penceresi için etiketleri önceden üretmesini sağlar
- Gönderici talep üzerine üretir (depolama gerekmez)
- Simetrik anahtar ratchet (adım adım anahtar yenileme mekanizması) ile indeks aracılığıyla senkronize olur

### Oturum Etiketi Ratchet (mandallama mekanizması) Formülü

**Başlatma:**

```python
# From DH_INITIALIZE
sessTag_ck = initial_chain_key  # 32 bytes

# Initialize session tag ratchet
keydata = HKDF(sessTag_ck, ZEROLEN, "STInitialization", 64)
sessTag_chainKey = keydata[0:31]    # First chain key
SESSTAG_CONSTANT = keydata[32:63]   # Constant for all tags in this tagset
```
**Etiket Üretimi (N etiketi için):**

```python
# Generate tag N
keydata = HKDF(sessTag_chainKey_(N-1), SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
sessTag_chainKey_N = keydata[0:31]  # Chain key for next tag
tag_N = keydata[32:39]              # Session tag (8 bytes)

# Chain continues for each tag
# tag_0, tag_1, tag_2, ..., tag_65535
```
**Tam Sekans:**

```python
# Tag 0
keydata_0 = HKDF(sessTag_chainKey, SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
sessTag_chainKey_0 = keydata_0[0:31]
tag_0 = keydata_0[32:39]

# Tag 1
keydata_1 = HKDF(sessTag_chainKey_0, SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
sessTag_chainKey_1 = keydata_1[0:31]
tag_1 = keydata_1[32:39]

# Tag N
keydata_N = HKDF(sessTag_chainKey_(N-1), SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
sessTag_chainKey_N = keydata_N[0:31]
tag_N = keydata_N[32:39]
```
### Session Tag Ratchet (oturum etiketi ratchet mekanizması) Gönderici Gerçeklemesi

```python
class OutboundTagset:
    def __init__(self, sessTag_ck):
        # Initialize
        keydata = HKDF(sessTag_ck, ZEROLEN, "STInitialization", 64)
        self.chainKey = keydata[0:31]
        self.constant = keydata[32:63]
        self.index = -1
    
    def get_next_tag(self):
        # Increment index
        self.index += 1
        
        if self.index > 65535:
            raise TagsetExhausted("Ratchet required")
        
        # Generate tag
        keydata = HKDF(self.chainKey, self.constant, "SessionTagKeyGen", 64)
        self.chainKey = keydata[0:31]
        tag = keydata[32:39]
        
        return (tag, self.index)
```
**Gönderici Süreci:** 1. Her mesaj için `get_next_tag()` çağrısını yap 2. Dönen etiketi ES mesajında kullan 3. Olası ACK (onay) takibi için indeks N'yi sakla 4. Etiket depolaması gerekmez (istek üzerine oluşturulur)

### Session Tag Ratchet (oturum etiketi için kademeli anahtar yenileme mekanizması) Alıcı Tarafı Uygulaması

```python
class InboundTagset:
    def __init__(self, sessTag_ck, look_ahead=32):
        # Initialize
        keydata = HKDF(sessTag_ck, ZEROLEN, "STInitialization", 64)
        self.chainKey = keydata[0:31]
        self.constant = keydata[32:63]
        self.index = -1
        self.look_ahead = look_ahead
        self.tags = {}  # Dictionary: tag -> index
        
        # Pre-generate initial tags
        self.extend(look_ahead)
    
    def extend(self, count):
        """Generate 'count' more tags"""
        for _ in range(count):
            self.index += 1
            
            if self.index > 65535:
                return  # Cannot exceed maximum
            
            # Generate tag
            keydata = HKDF(self.chainKey, self.constant, "SessionTagKeyGen", 64)
            self.chainKey = keydata[0:31]
            tag = keydata[32:39]
            
            # Store tag
            self.tags[tag] = self.index
    
    def lookup_tag(self, tag):
        """Look up tag and return index"""
        if tag in self.tags:
            index = self.tags[tag]
            # Remove tag (one-time use)
            del self.tags[tag]
            return index
        return None
    
    def check_and_extend(self):
        """Extend if tag count is low"""
        current_count = len(self.tags)
        if current_count < self.look_ahead // 2:
            # Extend to restore window
            self.extend(self.look_ahead - current_count)
```
**Alıcı Süreci:** 1. İleriye bakış penceresi için etiketleri önceden oluştur (örn., 32 etiket) 2. Etiketleri bir hash tablosunda veya sözlükte sakla 3. Mesaj geldiğinde, N indeksini almak için etiketi ara 4. Etiketi depodan kaldır (tek kullanımlık) 5. Etiket sayısı eşik değerin altına düşerse pencereyi genişlet

### Oturum Etiketi İleriye Bakma Stratejisi

**Amaç**: Bellek kullanımını sıralama dışı mesaj işleme ile dengelemek

**Önerilen Look-Ahead (ileriye bakma) Boyutları:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Tagset Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Initial Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Maximum Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR tagset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Short-lived</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ES tagset 0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">24</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">160</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Initial ES tagset</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ES tagset 1+</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">160</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">160</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Ratcheted tagsets</td>
    </tr>
  </tbody>
</table>
**Uyarlanabilir İleriye Bakma:**

```python
# Dynamic look-ahead based on highest tag received
look_ahead = min(tsmax, tsmin + N // 4)

# Example:
# tsmin = 24, tsmax = 160
# N = 0:   look_ahead = min(160, 24 + 0/4) = 24
# N = 100: look_ahead = min(160, 24 + 100/4) = 49
# N = 500: look_ahead = min(160, 24 + 500/4) = 149
# N = 544: look_ahead = min(160, 24 + 544/4) = 160
```
**Geriden Kırp:**

```python
# Trim tags far behind highest received
trim_behind = look_ahead // 2

# If highest received tag is N=100, trim tags below N=50
```
**Bellek Hesaplama:**

```python
# Per tag: 8 bytes (tag) + 2 bytes (index) + overhead ≈ 16 bytes
# Look-ahead of 160 tags ≈ 2.5 KB per inbound tagset

# With multiple sessions:
# 100 inbound sessions × 2.5 KB = 250 KB total
```
### Session Tag'lerin (Oturum Etiketleri) Sıra Dışı İşlenmesi

**Senaryo**: Mesajlar sırayla gelmiyor

```
Expected: tag_5, tag_6, tag_7, tag_8
Received: tag_5, tag_7, tag_6, tag_8
```
**Alıcı Davranışı:**

1. tag_5'i al:
   - Ara: 5. indekste bulundu
   - İletiyi işle
   - tag_5'i kaldır
   - Alınan en yüksek: 5

2. tag_7 (sırasız) alındığında:
   - Ara: indeks 7'de bulundu
   - Mesajı işle
   - tag_7'yi kaldır
   - Alınan en yüksek: 7
   - Not: tag_6 hâlâ depoda (henüz alınmadı)

3. tag_6 alındı (gecikmeli):
   - Sorgula: indeks 6'da bulundu
   - Mesajı işle
   - tag_6 öğesini kaldır
   - En yüksek alınan: 7 (değişmedi)

4. tag_8'i al:
   - Ara: indeks 8'de bulundu
   - Mesajı işle
   - tag_8'i kaldır
   - Alınan en yüksek: 8

**Pencere Bakımı:** - Alınan en yüksek indeksi takip et - Eksik indekslerin (boşluklar) listesini tut - Pencereyi en yüksek indekse göre genişlet - İsteğe bağlı: Zaman aşımından sonra eski boşlukları kaldır

### Simetrik Anahtar Mandalı

symmetric key ratchet (simetrik anahtarların kademeli yenileme mekanizması), oturum etiketleriyle eşzamanlı 32 baytlık şifreleme anahtarları üretir.

### Symmetric Key Ratchet (simetrik anahtar mandal mekanizması) Amacı

- Her mesaj için benzersiz bir şifreleme anahtarı sağlar
- session tag ratchet (oturum etiketi kademeli güncelleme mekanizması) ile eşzamanlıdır (aynı indeks)
- Gönderici talep üzerine oluşturabilir
- Alıcı, etiket alınana kadar oluşturmayı erteleyebilir

### Symmetric Key Ratchet (simetrik anahtar mandalı) formülü

**Başlatma:**

```python
# From DH_INITIALIZE
symmKey_ck = initial_chain_key  # 32 bytes

# No additional initialization needed
# Unlike session tag ratchet, no constant is derived
```
**Anahtar Oluşturma (anahtar N için):**

```python
# Generate key N
SYMMKEY_CONSTANT = ZEROLEN  # Empty string
keydata = HKDF(symmKey_chainKey_(N-1), SYMMKEY_CONSTANT, "SymmetricRatchet", 64)
symmKey_chainKey_N = keydata[0:31]  # Chain key for next key
key_N = keydata[32:63]              # Session key (32 bytes)
```
**Aşamaların Tamamı:**

```python
# Key 0
keydata_0 = HKDF(symmKey_ck, ZEROLEN, "SymmetricRatchet", 64)
symmKey_chainKey_0 = keydata_0[0:31]
key_0 = keydata_0[32:63]

# Key 1
keydata_1 = HKDF(symmKey_chainKey_0, ZEROLEN, "SymmetricRatchet", 64)
symmKey_chainKey_1 = keydata_1[0:31]
key_1 = keydata_1[32:63]

# Key N
keydata_N = HKDF(symmKey_chainKey_(N-1), ZEROLEN, "SymmetricRatchet", 64)
symmKey_chainKey_N = keydata_N[0:31]
key_N = keydata_N[32:63]
```
### Symmetric Key Ratchet (mandal mekanizması) Gönderici Gerçeklemesi

```python
class OutboundKeyRatchet:
    def __init__(self, symmKey_ck):
        self.chainKey = symmKey_ck
        self.index = -1
    
    def get_key(self, index):
        """Generate key for specific index"""
        # Fast-forward to desired index if needed
        while self.index < index:
            self.index += 1
            keydata = HKDF(self.chainKey, ZEROLEN, "SymmetricRatchet", 64)
            self.chainKey = keydata[0:31]
            if self.index == index:
                return keydata[32:63]
        
        # Should not reach here if called correctly
        raise ValueError("Key already generated")
```
**Gönderici Süreci:** 1. Sonraki etiketi ve onun N indisini al 2. N indisi için anahtar üret 3. Anahtarı kullanarak mesajı şifrele 4. Anahtar depolaması gerekmez

### Symmetric Key Ratchet (simetrik anahtar yenileme mekanizması) Alıcı Tarafı Gerçeklemesi

**Strateji 1: Ertelenmiş Oluşturma (Önerilen)**

```python
class InboundKeyRatchet:
    def __init__(self, symmKey_ck):
        self.chainKey = symmKey_ck
        self.index = -1
        self.cache = {}  # Optional: cache recently used keys
    
    def get_key(self, index):
        """Generate key for specific index"""
        # Check cache first (optional optimization)
        if index in self.cache:
            key = self.cache[index]
            del self.cache[index]
            return key
        
        # Fast-forward to desired index
        while self.index < index:
            self.index += 1
            keydata = HKDF(self.chainKey, ZEROLEN, "SymmetricRatchet", 64)
            self.chainKey = keydata[0:31]
            
            if self.index == index:
                return keydata[32:63]
        
        raise ValueError("Index already passed")
```
**Ertelenmiş Üretim Süreci:** 1. Etiketli ES mesajını al 2. N indeksini elde etmek için etiketi sorgula 3. 0'dan N'ye kadar anahtarları üret (henüz üretilmediyse) 4. Mesajı çözmek için N anahtarını kullan 5. Zincir anahtarı artık N indeksinde konumlandı

**Avantajlar:** - Minimal bellek kullanımı - Anahtarlar yalnızca gerektiğinde üretilir - Basit gerçekleştirim

**Dezavantajlar:** - İlk kullanımda 0'dan N'e kadar tüm anahtarları üretmelidir - Önbellekleme olmadan sıra dışı mesajları işleyemez

**Strateji 2: Etiket Penceresi ile Önceden Oluşturma (Alternatif)**

```python
class InboundKeyRatchet:
    def __init__(self, symmKey_ck):
        self.chainKey = symmKey_ck
        self.index = -1
        self.keys = {}  # Dictionary: index -> key
    
    def extend(self, count):
        """Pre-generate 'count' more keys"""
        for _ in range(count):
            self.index += 1
            keydata = HKDF(self.chainKey, ZEROLEN, "SymmetricRatchet", 64)
            self.chainKey = keydata[0:31]
            key = keydata[32:63]
            self.keys[self.index] = key
    
    def get_key(self, index):
        """Retrieve pre-generated key"""
        if index in self.keys:
            key = self.keys[index]
            del self.keys[index]
            return key
        return None
```
**Önceden Oluşturma Süreci:** 1. Etiket penceresiyle eşleşen anahtarları önceden oluştur (örn., 32 anahtar) 2. Anahtarları mesaj numarasına göre indekslenmiş olarak sakla 3. Etiket alındığında ilgili anahtarı bul 4. Etiketler kullanıldıkça pencereyi genişlet

**Avantajlar:** - Sıralama dışı mesajları doğal olarak işler - Hızlı anahtar elde etme (oluşturma gecikmesi yok)

**Dezavantajlar:** - Daha yüksek bellek kullanımı (anahtar başına 32 bayt, etiket başına 8 bayta karşı) - Anahtarlar etiketlerle senkronize tutulmalıdır

**Bellek Karşılaştırması:**

```python
# Look-ahead of 160:
# Tags only:  160 × 16 bytes = 2.5 KB
# Tags+Keys:  160 × (16 + 32) bytes = 7.5 KB
# 
# For 100 sessions:
# Tags only:  250 KB
# Tags+Keys:  750 KB
```
### Oturum Etiketleri ile Simetrik Ratchet (simetrik anahtar yenileme mekanizması) Senkronizasyonu

**Kritik Gereksinim**: Oturum etiketi indeksi, simetrik anahtar indeksine eşit olmak zorundadır

```python
# Sender
tag, index = outbound_tagset.get_next_tag()
key = outbound_keyratchet.get_key(index)  # Same index
nonce = construct_nonce(index)
ciphertext = ENCRYPT(key, nonce, payload, tag)

# Receiver
index = inbound_tagset.lookup_tag(tag)
key = inbound_keyratchet.get_key(index)  # Same index
nonce = construct_nonce(index)
plaintext = DECRYPT(key, nonce, ciphertext, tag)
```
**Hata Türleri:**

Senkronizasyon bozulursa: - Şifre çözme için yanlış anahtar kullanıldı - MAC doğrulaması başarısız olur - İleti reddedildi

**Önleme:** - Etiket ve anahtar için her zaman aynı indeksi kullanın - Her iki ratchet'te (anahtar ilerletme mekanizması) de indeksleri asla atlamayın - Sırası bozulmuş mesajları dikkatle ele alın

### Symmetric Ratchet (kademeli anahtar yenileme mekanizması) için Nonce (tek-kullanımlık sayı) Oluşturma

Tek kullanımlık sayı, mesaj numarasından türetilir:

```python
def construct_nonce(index):
    """
    Construct 12-byte nonce for ChaCha20-Poly1305
    
    Args:
        index: Message number (0-65535)
    
    Returns:
        nonce: 12-byte nonce
    """
    # First 4 bytes are always zero
    nonce = bytearray(12)
    nonce[0:4] = b'\x00\x00\x00\x00'
    
    # Last 8 bytes are little-endian message number
    nonce[4:12] = index.to_bytes(8, byteorder='little')
    
    return bytes(nonce)
```
**Örnekler:**

```python
index = 0:     nonce = 0x00000000 0000000000000000
index = 1:     nonce = 0x00000000 0100000000000000
index = 255:   nonce = 0x00000000 FF00000000000000
index = 256:   nonce = 0x00000000 0001000000000000
index = 65535: nonce = 0x00000000 FFFF000000000000
```
**Önemli Özellikler:** - Nonce (tek kullanımlık sayı) değerleri bir etiket kümesindeki her mesaj için benzersizdir - Nonceler asla tekrar etmez (tek kullanımlık etiketler bunu sağlar) - 8 baytlık sayaç 2^64 mesaja izin verir (biz yalnızca 2^16 kullanıyoruz) - Nonce biçimi RFC 7539'un sayaç tabanlı yapısıyla uyumludur

---

## Oturum Yönetimi

### Oturum Bağlamı

Tüm gelen ve giden oturumlar belirli bir bağlama ait olmalıdır:

1. **Router Bağlamı**: router'ın kendisi için oturumlar
2. **Hedef Bağlamı**: belirli bir yerel hedef (istemci uygulaması) için oturumlar

**Kritik Kural**: Korelasyon saldırılarını önlemek için oturumlar bağlamlar arasında KESİNLİKLE paylaşılmamalıdır.

**Uygulama:**

```python
class SessionKeyManager:
    """Context for managing sessions (router or destination)"""
    def __init__(self, context_id):
        self.context_id = context_id
        self.inbound_sessions = {}   # far_end_dest -> [sessions]
        self.outbound_sessions = {}  # far_end_dest -> session
        self.static_keypair = generate_keypair()  # Context's identity
    
    def get_outbound_session(self, destination):
        """Get or create outbound session to destination"""
        if destination not in self.outbound_sessions:
            self.outbound_sessions[destination] = create_outbound_session(destination)
        return self.outbound_sessions[destination]
    
    def add_inbound_session(self, session, destination=None):
        """Add inbound session, optionally bound to destination"""
        if destination:
            if destination not in self.inbound_sessions:
                self.inbound_sessions[destination] = []
            self.inbound_sessions[destination].append(session)
        else:
            # Unbound session
            self.inbound_sessions[None].append(session)
```
**Java I2P Gerçeklemesi:**

Java I2P'de, `SessionKeyManager` sınıfı şu işlevleri sağlar: - router başına bir `SessionKeyManager` - yerel hedef başına bir `SessionKeyManager` - her bağlamda ECIES ve ElGamal oturumlarının ayrı yönetimi

### Oturum Bağlama

**Binding** (bağlama), bir oturumu belirli bir karşı uçtaki hedefle ilişkilendirir.

### Bağlı Oturumlar

**Özellikler:** - NS mesajına gönderenin statik anahtarı dahil edilir - Alıcı, gönderenin hedefini belirleyebilir - Çift yönlü iletişimi sağlar - Her hedef için tek bir giden oturum - Birden çok gelen oturum olabilir (geçişler sırasında)

**Kullanım Durumları:** - Akış bağlantıları (TCP benzeri) - Yanıtlanabilir datagramlar - İstek/yanıt gerektiren herhangi bir protokol

**Bağlama Süreci:**

```python
# Alice creates bound outbound session
outbound_session = OutboundSession(
    destination=bob_destination,
    static_key=alice_static_key,
    bound=True
)

# Alice sends NS with static key
ns_message = build_ns_message(
    ephemeral_key=alice_ephemeral_key,
    static_key=alice_static_key,  # Included for binding
    payload=data
)

# Bob receives NS
bob_receives_ns(ns_message)
# Bob extracts Alice's static key
alice_static_key = decrypt_static_key_section(ns_message)

# Bob looks up Alice's destination (from bundled LeaseSet)
alice_destination = lookup_destination_by_static_key(alice_static_key)

# Bob creates bound inbound session
inbound_session = InboundSession(
    destination=alice_destination,
    bound=True
)

# Bob pairs with outbound session
outbound_session = OutboundSession(
    destination=alice_destination,
    bound=True
)
```
**Faydalar:** 1. **Ephemeral-Ephemeral DH**: (geçici-geçici Diffie-Hellman) Yanıt ee DH kullanır (tam ileri gizlilik) 2. **Oturum Sürekliliği**: Ratchets (kademeli anahtar yenileme mekanizmaları) aynı hedefe bağın korunmasını sağlar 3. **Güvenlik**: Oturum ele geçirmeyi önler (statik anahtarla kimliği doğrulanır) 4. **Verimlilik**: Her hedef için tek bir oturum (yinelenme yok)

### Bağlı Olmayan Oturumlar

**Özellikler:** - NS message (NS iletisi) içinde statik anahtar yok (flags bölümü tamamen sıfırdır) - Alıcı gönderenin kimliğini belirleyemez - Yalnızca tek yönlü iletişim - Aynı hedefe birden çok oturuma izin verilir

**Kullanım Senaryoları:** - Ham datagramlar (fire-and-forget - gönder-ve-unut) - Anonim yayınlama - Yayın tarzı mesajlaşma

**Özellikler:** - Daha anonim (gönderici tanımlaması yok) - Daha verimli (el sıkışmada 1 DH (Diffie-Hellman anahtar değişimi) ile 2 DH) - Yanıt mümkün değil (alıcı nereye yanıt vereceğini bilmiyor) - Oturum ratcheting (adımlı anahtar yenileme) yok (tek seferlik ya da sınırlı kullanım)

### Oturum Eşleştirme

**Eşleştirme**, çift yönlü iletişim için gelen bir oturumu giden bir oturumla bağlar.

### Eşleştirilmiş Oturumlar Oluşturma

**Alice'in Bakış Açısı (başlatıcı):**

```python
# Create outbound session to Bob
outbound_session = create_outbound_session(bob_destination)

# Create paired inbound session
inbound_session = create_inbound_session(
    paired_with=outbound_session,
    bound_to=bob_destination
)

# Link them
outbound_session.paired_inbound = inbound_session
inbound_session.paired_outbound = outbound_session

# Send NS message
send_ns_message(outbound_session, payload)
```
**Bob'un Bakış Açısı (yanıtlayan):**

```python
# Receive NS message
ns_message = receive_ns_message()

# Create inbound session
inbound_session = create_inbound_session_from_ns(ns_message)

# If NS contains static key (bound):
if ns_message.has_static_key():
    alice_destination = extract_destination(ns_message)
    inbound_session.bind_to(alice_destination)
    
    # Create paired outbound session
    outbound_session = create_outbound_session(alice_destination)
    
    # Link them
    outbound_session.paired_inbound = inbound_session
    inbound_session.paired_outbound = outbound_session

# Send NSR
send_nsr_message(inbound_session, outbound_session, payload)
```
### Oturum Eşleştirmenin Avantajları

1. **Bant içi ACK'ler**: Ayrı bir clove (garlic mesajı içindeki alt iletisi) olmadan iletileri onaylayabilir
2. **Verimli ratchet (sürekli anahtar güncelleme mekanizması)**: Her iki yön birlikte ve eşgüdümlü olarak ilerler
3. **Akış denetimi**: Eşleştirilmiş oturumlar arasında back-pressure (aşırı yükü kaynağa geri ileterek baskılama) uygulanabilir
4. **Durum tutarlılığı**: Senkronize durumu sürdürmek daha kolaydır

### Oturum Eşleştirme Kuralları

- Giden oturum eşleşmemiş olabilir (bağlı olmayan NS)
- Bağlı NS için gelen oturum eşleştirilmiş olmalıdır
- Eşleştirme oturum oluşturma sırasında gerçekleşir, sonrasında değil
- Eşleştirilmiş oturumlar aynı hedefe bağlıdır
- Ratchet'lar (ardışık anahtar yenileme mekanizması) bağımsız olarak gerçekleşir ancak koordine edilir

### Oturum Yaşam Döngüsü

### Oturum Yaşam Döngüsü: Oluşturma Aşaması

**Giden Oturum Oluşturma (Alice):**

```python
def create_outbound_session(destination, bound=True):
    session = OutboundSession()
    session.destination = destination
    session.bound = bound
    session.state = SessionState.NEW
    session.created_time = now()
    
    # Generate keys for NS message
    session.ephemeral_keypair = generate_elg2_keypair()
    if bound:
        session.static_key = context.static_keypair.public_key
    
    # Will be populated after NSR received
    session.outbound_tagset = None
    session.inbound_tagset = None
    
    return session
```
**Gelen Oturum Oluşturma (Bob):**

```python
def create_inbound_session_from_ns(ns_message):
    session = InboundSession()
    session.state = SessionState.ESTABLISHED
    session.created_time = now()
    
    # Extract from NS
    session.remote_ephemeral_key = ns_message.ephemeral_key
    session.remote_static_key = ns_message.static_key
    
    if session.remote_static_key:
        session.bound = True
        session.destination = lookup_destination(session.remote_static_key)
    else:
        session.bound = False
        session.destination = None
    
    # Generate keys for NSR
    session.ephemeral_keypair = generate_elg2_keypair()
    
    # Create tagsets from KDF
    session.inbound_tagset = create_tagset_from_nsr()
    session.outbound_tagset = create_tagset_from_nsr()
    
    return session
```
### Oturum Yaşam Döngüsü: Aktif Aşama

**Durum Geçişleri:**

```
NEW (outbound only)
  ↓
  NS sent
  ↓
PENDING_REPLY (outbound only)
  ↓
  NSR received
  ↓
ESTABLISHED
  ↓
  ES messages exchanged
  ↓
ESTABLISHED (ongoing)
  ↓
  (optional) RATCHETING
  ↓
ESTABLISHED
```
**Aktif Oturum Bakımı:**

```python
def maintain_active_session(session):
    # Update last activity time
    session.last_activity = now()
    
    # Check for ratchet needed
    if session.outbound_tagset.needs_ratchet():
        initiate_ratchet(session)
    
    # Check for incoming ratchet
    if received_nextkey_block():
        process_ratchet(session)
    
    # Trim old tags from inbound tagset
    session.inbound_tagset.expire_old_tags()
    
    # Check session health
    if session.idle_time() > SESSION_TIMEOUT:
        mark_session_idle(session)
```
### Oturum Yaşam Döngüsü: Sona Erme Aşaması

**Oturum Zaman Aşımı Değerleri:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Session Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Sender Timeout</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Receiver Timeout</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR tagset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">N/A</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Short-lived</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ES tagset 0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Initial</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ES tagset 1+</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Ratcheted</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Old tagset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">N/A</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">After ratchet</td>
    </tr>
  </tbody>
</table>
**Sona Erme Mantığı:**

```python
def check_session_expiration():
    for session in active_sessions:
        # Outbound session expiration (sender)
        if session.is_outbound():
            if session.idle_time() > 8 * 60:  # 8 minutes
                expire_outbound_session(session)
        
        # Inbound session expiration (receiver)
        else:
            if session.idle_time() > 10 * 60:  # 10 minutes
                expire_inbound_session(session)
    
    # Old tagsets (after ratchet)
    for tagset in old_tagsets:
        if tagset.age() > 3 * 60:  # 3 minutes
            delete_tagset(tagset)
```
**Kritik Kural**: Desenkronizasyonu önlemek için giden oturumların süresi, gelen oturumlardan önce MUTLAKA dolmalıdır.

**Düzenli Sonlandırma:**

```python
def terminate_session(session, reason=0):
    # Send Termination block (if implemented)
    send_termination_block(session, reason)
    
    # Mark session for deletion
    session.state = SessionState.TERMINATED
    
    # Keep session briefly for final messages
    schedule_deletion(session, delay=30)  # 30 seconds
    
    # Notify paired session
    if session.paired_session:
        session.paired_session.mark_remote_terminated()
```
### Birden çok NS mesajı

**Senaryo**: Alice'in NS iletisi kaybolur ya da NSR yanıtı kaybolur.

**Alice'in Davranışı:**

```python
class OutboundSession:
    def __init__(self):
        self.ns_messages_sent = []
        self.ns_timer = None
        self.max_ns_attempts = 5
    
    def send_ns_message(self, payload):
        # Generate new ephemeral key for each NS
        ephemeral_key = generate_elg2_keypair()
        
        ns_message = build_ns_message(
            ephemeral_key=ephemeral_key,
            static_key=self.static_key,
            payload=payload
        )
        
        # Store state for this NS
        ns_state = {
            'ephemeral_key': ephemeral_key,
            'chainkey': compute_chainkey(ns_message),
            'hash': compute_hash(ns_message),
            'tagset': derive_nsr_tagset(ns_message),
            'sent_time': now()
        }
        self.ns_messages_sent.append(ns_state)
        
        # Send message
        send_message(ns_message)
        
        # Set timer for retry
        if not self.ns_timer:
            self.ns_timer = set_timer(1.0, self.on_ns_timeout)
    
    def on_ns_timeout(self):
        if len(self.ns_messages_sent) >= self.max_ns_attempts:
            # Give up
            fail_session("No NSR received after {self.max_ns_attempts} attempts")
            return
        
        # Retry with new NS message
        send_ns_message(self.payload)
    
    def on_nsr_received(self, nsr_message):
        # Cancel timer
        cancel_timer(self.ns_timer)
        
        # Find which NS this NSR responds to
        tag = nsr_message.tag
        for ns_state in self.ns_messages_sent:
            if tag in ns_state['tagset']:
                # This NSR corresponds to this NS
                self.active_ns_state = ns_state
                break
        
        # Process NSR and complete handshake
        complete_handshake(nsr_message, self.active_ns_state)
        
        # Discard other NS states
        self.ns_messages_sent = []
```
**Önemli Özellikler:**

1. **Benzersiz Geçici Anahtarlar**: Her NS farklı bir geçici anahtar kullanır
2. **Bağımsız El Sıkışmaları**: Her NS ayrı bir el sıkışma durumu oluşturur
3. **NSR Korelasyonu**: NSR etiketi, hangi NS'ye yanıt verdiğini belirler
4. **Durum Temizliği**: Kullanılmayan NS durumları, başarılı bir NSR'den sonra atılır

**Saldırıların Önlenmesi:**

Kaynak tükenmesini önlemek için:

```python
# Limit NS sending rate
max_ns_rate = 5 per 10 seconds per destination

# Limit total NS attempts
max_ns_attempts = 5

# Limit total pending NS states
max_pending_ns = 10 per context
```
### Birden fazla NSR mesajı

**Senaryo**: Bob birden fazla NSR gönderir (örn. yanıt verileri birden çok mesaja bölünmüştür).

**Bob'un Davranışı:**

```python
class InboundSession:
    def send_nsr_replies(self, payload_chunks):
        # One NS received, multiple NSRs to send
        for chunk in payload_chunks:
            # Generate new ephemeral key for each NSR
            ephemeral_key = generate_elg2_keypair()
            
            # Get next tag from NSR tagset
            tag = self.nsr_tagset.get_next_tag()
            
            nsr_message = build_nsr_message(
                tag=tag,
                ephemeral_key=ephemeral_key,
                payload=chunk
            )
            
            send_message(nsr_message)
        
        # Wait for ES message from Alice
        self.state = SessionState.AWAITING_ES
```
**Alice'nin Davranışı:**

```python
class OutboundSession:
    def on_nsr_received(self, nsr_message):
        if self.state == SessionState.PENDING_REPLY:
            # First NSR received
            complete_handshake(nsr_message)
            self.state = SessionState.ESTABLISHED
            
            # Create ES sessions
            self.es_outbound_tagset = derive_es_outbound_tagset()
            self.es_inbound_tagset = derive_es_inbound_tagset()
            
            # Send ES message (ACK)
            send_es_message(empty_payload)
        
        elif self.state == SessionState.ESTABLISHED:
            # Additional NSR received
            # Decrypt and process payload
            payload = decrypt_nsr_payload(nsr_message)
            process_payload(payload)
            
            # These NSRs are from other NS attempts, ignore handshake
```
**Bob'un Temizliği:**

```python
class InboundSession:
    def on_es_received(self, es_message):
        # First ES received from Alice
        # This confirms which NSR Alice used
        
        # Clean up other handshake states
        for other_ns_state in self.pending_ns_states:
            if other_ns_state != self.active_ns_state:
                delete_ns_state(other_ns_state)
        
        # Delete unused NSR tagsets
        for tagset in self.nsr_tagsets:
            if tagset != self.active_nsr_tagset:
                delete_tagset(tagset)
        
        self.state = SessionState.ESTABLISHED
```
**Önemli Özellikler:**

1. **Birden Fazla NSR'ye İzin Verilir**: Bob, NS başına birden fazla NSR gönderebilir
2. **Farklı Geçici Anahtarlar**: Her NSR benzersiz bir geçici anahtar kullanmalıdır
3. **Aynı NSR Tagset (etiket kümesi)**: Bir NS için tüm NSR'lar aynı tagset kullanır
4. **İlk ES Kazanır**: Alice'in ilk ES'si hangi NSR'nin başarılı olduğunu belirler
5. **ES Sonrası Temizlik**: ES alındıktan sonra Bob kullanılmayan durumları atar

### Oturum Durum Makinesi

**Tam Durum Diyagramı:**

```
                    Outbound Session                    Inbound Session

                         NEW
                          |
                     send NS
                          |
                   PENDING_REPLY -------------------- receive NS ---> ESTABLISHED
                          |                                                |
                   receive NSR                                        send NSR
                          |                                                |
                    ESTABLISHED <---------- receive ES ------------- AWAITING_ES
                          |                     |                          |
                    ┌─────┴─────┐               |                    receive ES
                    |           |               |                          |
              send ES      receive ES           |                    ESTABLISHED
                    |           |               |                          |
                    └─────┬─────┘               |                ┌─────────┴─────────┐
                          |                     |                |                   |
                          |                     |          send ES              receive ES
                          |                     |                |                   |
                          |                     |                └─────────┬─────────┘
                          |                     |                          |
                          └─────────────────────┴──────────────────────────┘
                                              ACTIVE
                                                |
                                         idle timeout
                                                |
                                             EXPIRED
```
**Durum Açıklamaları:**

- **NEW**: Giden oturum oluşturuldu, henüz NS gönderilmedi
- **PENDING_REPLY**: NS gönderildi, NSR bekleniyor
- **AWAITING_ES**: NSR gönderildi, Alice'ten ilk ES bekleniyor
- **ESTABLISHED**: El sıkışma tamamlandı, ES gönderip/alabilir
- **ACTIVE**: ES mesajlarını etkin biçimde değiş tokuş ediyor
- **RATCHETING**: DH ratchet (Diffie-Hellman mandalı) sürüyor (ACTIVE alt kümesi)
- **EXPIRED**: Oturum zaman aşımına uğradı, silinmeyi bekliyor
- **TERMINATED**: Oturum açıkça sonlandırıldı

---

## Yük Biçimi

Tüm ECIES (Eliptik Eğri Entegre Şifreleme Şeması) iletilerinin (NS, NSR, ES) yük bölümü, NTCP2'ye benzer blok tabanlı bir biçim kullanır.

### Blok Yapısı

**Genel Biçim:**

```
+----+----+----+----+----+----+----+----+
|blk |  size   |       data             |
+----+----+----+                        +
|                                       |
~               ...                     ~
|                                       |
+----+----+----+----+----+----+----+----+
|blk |  size   |       data             |
+----+----+----+                        +
|                                       |
~               ...                     ~
|                                       |
+----+----+----+----+----+----+----+----+
```
**Alanlar:**

- `blk`: 1 bayt - Blok tür numarası
- `size`: 2 bayt - Veri alanının big-endian (büyük anlamlı bayt sıralaması) boyutu (0-65516)
- `data`: Değişken uzunluk - Bloğa özgü veri

**Kısıtlamalar:**

- Maksimum ChaChaPoly çerçevesi: 65535 bayt
- Poly1305 MAC: 16 bayt
- Maksimum toplam blok boyutu: 65519 bayt (65535 - 16)
- Maksimum tek blok: 65519 bayt (3 baytlık başlık dahil)
- Maksimum tek blok verisi: 65516 bayt

### Blok Türleri

**Tanımlı Blok Türleri:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DateTime</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">7 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Required in NS</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1-3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Future use</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Termination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">9+ bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unimplemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Session termination</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Options</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">21+ bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unimplemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Session options</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">MessageNumbers</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">5 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unimplemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">PN value</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NextKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">3 or 35 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DH ratchet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ACK</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">4+ bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Message acknowledgment</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">9</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ACK Request</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">3 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Request ACK</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Future use</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Garlic Clove</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Variable</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Application data</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12-223</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Future use</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">224-253</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Variable</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Testing features</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">254</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Padding</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Variable</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Traffic shaping</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">255</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Future extension</td>
    </tr>
  </tbody>
</table>
**Bilinmeyen Blokların İşlenmesi:**

Gerçekleştirimler, tür numaraları bilinmeyen blokları yok saymak ve bunları dolgu olarak değerlendirmek zorundadır. Bu, ileriye dönük uyumluluğu sağlar.

### Blok Sıralama Kuralları

### NS Mesaj Sıralaması

**Zorunlu:** - DateTime bloğu MUTLAKA en başta olmalıdır

**İzin verilenler:** - Garlic Clove (garlic encryption içinde tekil mesaj parçası) (type 11) - Seçenekler (type 5) - uygulanmışsa - Dolgu (type 254)

**Yasak:** - NextKey (sonraki anahtar), ACK (alındı onayı), ACK Request (alındı onayı isteği), Termination (sonlandırma), MessageNumbers (ileti numaraları)

**Örnek Geçerli NS Yükü:**

```
DateTime (0) | Garlic Clove (11) | Garlic Clove (11) | Padding (254)
```
### NSR Mesaj Sıralaması

**Gerekli:** - Yok (yük boş olabilir)

**İzin verilenler:** - Garlic Clove (Garlic Message içindeki alt birim) (tip 11) - Options (tip 5) - eğer uygulanmışsa - Padding (tip 254)

**Yasak:** - DateTime, NextKey, ACK, ACK Request, Termination, MessageNumbers

**Geçerli NSR Yükü Örneği:**

```
Garlic Clove (11) | Garlic Clove (11) | Padding (254)
```
veya

```
(empty - ACK only)
```
### ES Mesaj Sıralaması

**Gerekli:** - Yok (payload (yük) boş olabilir)

**İzin verilen (herhangi bir sırada):** - Garlic Clove (garlic mesajındaki alt birim) (type 11) - NextKey (Sonraki Anahtar) (type 7) - ACK (type 8) - ACK Request (ACK İsteği) (type 9) - Termination (Sonlandırma) (type 4) - uygulanmışsa - MessageNumbers (Mesaj Numaraları) (type 6) - uygulanmışsa - Options (Seçenekler) (type 5) - uygulanmışsa - Padding (Dolgu) (type 254)

**Özel Kurallar:** - Sonlandırma bloğu (Padding hariç) en sonda OLMALIDIR - Padding (doldurma) bloğu en sonda OLMALIDIR - Birden fazla Garlic Cloves (garlic mesajındaki alt mesaj birimleri) kullanılabilir - En fazla 2 NextKey (bir sonraki anahtar bilgisi) bloğuna izin verilir (ileri ve geri) - Birden fazla Padding bloğuna İZİN VERİLMEZ

**Geçerli ES Yüklerine Örnekler:**

```
Garlic Clove (11) | ACK (8) | Padding (254)
```
```
NextKey (7) | Garlic Clove (11) | Garlic Clove (11)
```
```
NextKey (7) forward | NextKey (7) reverse | Garlic Clove (11)
```
```
ACK Request (9) | Garlic Clove (11) | Termination (4) | Padding (254)
```
### Tarih-Saat Bloğu (Tür 0)

**Amaç**: Yeniden oynatma (replay) saldırılarını önleme ve saat kayması (clock skew) doğrulaması için zaman damgası

**Boyut**: 7 bayt (3 bayt başlık + 4 bayt veri)

**Biçim:**

```
+----+----+----+----+----+----+----+
| 0  |    4    |     timestamp     |
+----+----+----+----+----+----+----+
```
**Alanlar:**

- `blk`: 0
- `size`: 4 (big-endian - yüksek anlamlı bayt önce)
- `timestamp`: 4 bayt - saniye cinsinden Unix zaman damgası (işaretsiz, big-endian)

**Zaman Damgası Biçimi:**

```python
timestamp = int(time.time())  # Seconds since 1970-01-01 00:00:00 UTC
# Wraps around in year 2106 (4-byte unsigned maximum)
```
**Doğrulama Kuralları:**

```python
MAX_CLOCK_SKEW_PAST = 5 * 60      # 5 minutes
MAX_CLOCK_SKEW_FUTURE = 2 * 60    # 2 minutes

def validate_datetime(timestamp):
    now = int(time.time())
    age = now - timestamp
    
    if age < -MAX_CLOCK_SKEW_FUTURE:
        return False  # Too far in future
    
    if age > MAX_CLOCK_SKEW_PAST:
        return False  # Too old
    
    return True
```
**Replay Saldırılarını Önleme:**

```python
class ReplayFilter:
    def __init__(self, duration=5*60):
        self.duration = duration  # 5 minutes
        self.seen_messages = BloomFilter(size=100000, false_positive_rate=0.001)
        self.cleanup_timer = RepeatTimer(60, self.cleanup)
    
    def check_replay(self, ephemeral_key, timestamp):
        # Check timestamp validity
        if not validate_datetime(timestamp):
            return False
        
        # Check if ephemeral key seen recently
        if ephemeral_key in self.seen_messages:
            return False  # Replay attack
        
        # Add to seen messages
        self.seen_messages.add(ephemeral_key)
        return True
    
    def cleanup(self):
        # Expire old entries (Bloom filter automatically ages out)
        pass
```
**Uygulama Notları:**

1. **NS Mesajları**: DateTime MUTLAKA ilk blok olmalıdır
2. **NSR/ES Mesajları**: DateTime genellikle dahil edilmez
3. **Yeniden Oynatma Penceresi**: 5 dakika önerilen asgari süredir
4. **Bloom Filtresi**: Verimli yeniden oynatma tespiti için önerilir
5. **Saat Kayması**: Geçmişte 5 dakikaya, gelecekte 2 dakikaya izin verin

### Garlic Clove Block (Sarımsak Dişi Bloğu) (Type 11)

**Amaç**: İletilmek üzere I2NP mesajlarını kapsüller

**Biçim:**

```
+----+----+----+----+----+----+----+----+
| 11 |  size   |                        |
+----+----+----+                        +
|      Delivery Instructions            |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|type|  Message_ID       | Expiration  |
+----+----+----+----+----+----+----+----+
     |      I2NP Message body           |
+----+                                  +
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
```
**Alanlar:**

- `blk`: 11
- `size`: clove (garlic encryption içindeki alt-ileti) toplam boyutu (değişken)
- `Delivery Instructions`: I2NP spesifikasyonunda belirtildiği gibi
- `type`: I2NP mesaj türü (1 bayt)
- `Message_ID`: I2NP mesaj kimliği (4 bayt)
- `Expiration`: Saniye cinsinden Unix zaman damgası (4 bayt)
- `I2NP Message body`: Değişken uzunluklu mesaj verisi

**Teslimat Talimatı Biçimleri:**

**Yerel Teslimat** (1 bayt):

```
+----+
|0x00|
+----+
```
**Hedefe Teslim** (33 bayt):

```
+----+----+----+----+----+----+----+----+
|0x01|                                  |
+----+        Destination Hash         +
|              32 bytes                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
**Router Teslimi** (33 bayt):

```
+----+----+----+----+----+----+----+----+
|0x02|                                  |
+----+         Router Hash              +
|              32 bytes                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
**Tunnel Teslimi** (37 bayt):

```
+----+----+----+----+----+----+----+----+
|0x03|         Tunnel ID                |
+----+----+----+----+----+              +
|           Router Hash                 |
+              32 bytes                 +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
**I2NP Mesaj Başlığı** (toplam 9 bayt):

```
+----+----+----+----+----+----+----+----+
|type|      msg_id       |  expiration   |
+----+----+----+----+----+----+----+----+
     |                                   |
```
- `type`: I2NP mesaj türü (Database Store, Database Lookup, Data, vb.)
- `msg_id`: 4 baytlık mesaj kimliği
- `expiration`: 4 baytlık Unix zaman damgası (saniye)

**ElGamal Clove Formatı'ndan Önemli Farklar:**

1. **Sertifika Yok**: Sertifika alanı dahil edilmedi (ElGamal'de kullanılmıyor)
2. **Clove ID Yok**: Clove (garlic mesajı içindeki alt mesaj) ID'si dahil edilmedi (her zaman 0'dı)
3. **Clove Zaman Aşımı Yok**: Bunun yerine I2NP mesaj zaman aşımı kullanılır
4. **Kompakt Başlık**: 9 baytlık I2NP başlığı vs daha büyük ElGamal biçimi
5. **Her Clove Ayrı Bir Bloktur**: CloveSet yapısı yok

**Birden Çok Clove (garlic mesajı içindeki alt-mesaj birimi):**

```python
# Multiple Garlic Cloves in one message
payload = [
    build_datetime_block(),
    build_garlic_clove(i2np_message_1),
    build_garlic_clove(i2np_message_2),
    build_garlic_clove(i2np_message_3),
    build_padding_block()
]
```
**Cloves (garlic mesajındaki alt mesajlar) içindeki yaygın I2NP mesaj türleri:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseStore</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Publishing LeaseSet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseLookup</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Requesting LeaseSet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DeliveryStatus</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ACK (legacy, avoid in ECIES)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Streaming data</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">21</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Garlic</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Nested garlic messages</td>
    </tr>
  </tbody>
</table>
**Clove Processing (Clove'un işlenmesi):**

```python
def process_garlic_clove(clove_data):
    # Parse delivery instructions
    delivery_type = clove_data[0]
    
    if delivery_type == 0x00:
        # Local delivery
        offset = 1
    elif delivery_type == 0x01:
        # Destination delivery
        dest_hash = clove_data[1:33]
        offset = 33
    elif delivery_type == 0x02:
        # Router delivery
        router_hash = clove_data[1:33]
        offset = 33
    elif delivery_type == 0x03:
        # Tunnel delivery
        tunnel_id = struct.unpack('>I', clove_data[1:5])[0]
        router_hash = clove_data[5:37]
        offset = 37
    
    # Parse I2NP header
    i2np_type = clove_data[offset]
    msg_id = struct.unpack('>I', clove_data[offset+1:offset+5])[0]
    expiration = struct.unpack('>I', clove_data[offset+5:offset+9])[0]
    
    # Extract I2NP body
    i2np_body = clove_data[offset+9:]
    
    # Process message
    process_i2np_message(i2np_type, msg_id, expiration, i2np_body)
```
### NextKey Block (sonraki anahtar bloğu) (Tip 7)

**Amaç**: DH ratchet (ardışık anahtar yenileme mekanizması) anahtar değişimi

**Biçim (Anahtar Mevcut - 38 bayt):**

```
+----+----+----+----+----+----+----+----+
| 7  |   35    |flag|  key ID |         |
+----+----+----+----+----+----+         +
|                                       |
+     Next DH Ratchet Public Key        +
|              32 bytes                 |
+                                       +
|                                       |
+                             +----+----+
|                             |
+----+----+----+----+----+----+
```
**Biçim (Yalnızca Anahtar Kimliği - 6 bayt):**

```
+----+----+----+----+----+----+
| 7  |    3    |flag|  key ID |
+----+----+----+----+----+----+
```
**Alanlar:**

- `blk`: 7
- `size`: 3 (yalnızca ID) veya 35 (anahtarla)
- `flag`: 1 bayt - Bayrak bitleri
- `key ID`: 2 bayt - Big-endian anahtar tanımlayıcısı (0-32767)
- `Public Key`: 32 bayt - X25519 ortak anahtar (little-endian), eğer bayrak bit 0 = 1 ise

**Bayrak Bitleri:**

```
Bit 7 6 5 4 3 2 1 0
    | | | | | | | |
    | | | | | | | +-- Bit 0: Key present (1) or ID only (0)
    | | | | | | +---- Bit 1: Reverse key (1) or forward key (0)
    | | | | | +------ Bit 2: Request reverse key (1) or no request (0)
    | | | | |
    +-+-+-+-+-------- Bits 3-7: Reserved (set to 0)
```
**Bayrak Örnekleri:**

```python
# Forward key present
flags = 0x01  # Binary: 00000001

# Reverse key present
flags = 0x03  # Binary: 00000011

# Forward key ID only (ACK)
flags = 0x00  # Binary: 00000000

# Reverse key ID only (ACK)
flags = 0x02  # Binary: 00000010

# Forward key ID with reverse request
flags = 0x04  # Binary: 00000100
```
**Anahtar Kimliği Kuralları:**

- ID'ler ardışık: 0, 1, 2, ..., 32767
- ID yalnızca yeni bir anahtar üretildiğinde artar
- Bir sonraki ratchet (anahtar ilerletme mekanizması) gerçekleşene kadar birden çok mesaj için aynı ID kullanılır
- En yüksek ID 32767'dir (sonrasında yeni bir oturum başlatılmalıdır)

**Kullanım Örnekleri:**

```python
# Initiating ratchet (sender generates new key)
nextkey = NextKeyBlock(
    flags=0x01,           # Key present, forward
    key_id=0,
    public_key=sender_new_pk
)

# Replying to ratchet (receiver generates new key)
nextkey = NextKeyBlock(
    flags=0x03,           # Key present, reverse
    key_id=0,
    public_key=receiver_new_pk
)

# Acknowledging ratchet (no new key from sender)
nextkey = NextKeyBlock(
    flags=0x02,           # ID only, reverse
    key_id=0
)

# Requesting reverse ratchet
nextkey = NextKeyBlock(
    flags=0x04,           # Request reverse, forward ID
    key_id=1
)
```
**İşleme Mantığı:**

```python
def process_nextkey_block(block):
    flags = block.flags
    key_id = block.key_id
    
    key_present = (flags & 0x01) != 0
    is_reverse = (flags & 0x02) != 0
    request_reverse = (flags & 0x04) != 0
    
    if key_present:
        public_key = block.public_key
        
        if is_reverse:
            # Reverse key received
            perform_dh_ratchet(receiver_key=public_key, key_id=key_id)
            # Sender should ACK with own key ID
        else:
            # Forward key received
            perform_dh_ratchet(sender_key=public_key, key_id=key_id)
            # Receiver should reply with reverse key
            send_reverse_key(generate_new_key())
    
    else:
        # Key ID only (ACK)
        if is_reverse:
            # Reverse key ACK
            confirm_reverse_ratchet(key_id)
        else:
            # Forward key ACK
            confirm_forward_ratchet(key_id)
    
    if request_reverse:
        # Sender requests receiver to generate new key
        send_reverse_key(generate_new_key())
```
**Birden Çok NextKey Bloğu:**

Her iki yön eşzamanlı olarak ratcheting (kademeli anahtar yenileme mekanizması) yapıyorsa, tek bir ES mesajı en fazla 2 NextKey bloğu içerebilir:

```python
# Both directions ratcheting
payload = [
    NextKeyBlock(flags=0x01, key_id=2, public_key=forward_key),  # Forward
    NextKeyBlock(flags=0x03, key_id=1, public_key=reverse_key),  # Reverse
    build_garlic_clove(data)
]
```
### ACK Bloğu (Tip 8)

**Amaç**: Alınan mesajları bant içi olarak onaylamak

**Biçim (Tekli ACK (onay) - 7 bayt):**

```
+----+----+----+----+----+----+----+
| 8  |    4    |tagsetid |   N     |
+----+----+----+----+----+----+----+
```
**Biçim (Birden Çok ACK):**

```
+----+----+----+----+----+----+----+----+
| 8  |  size   |tagsetid |   N     |    |
+----+----+----+----+----+----+----+    +
|            more ACKs                  |
~               ...                     ~
|                                       |
+----+----+----+----+----+----+----+----+
```
**Alanlar:**

- `blk`: 8
- `size`: 4 * ACK sayısı (en az 4)
- Her ACK için:
  - `tagsetid`: 2 bayt - Big-endian (en anlamlı bayt önce) etiket kümesi kimliği (0-65535)
  - `N`: 2 bayt - Big-endian mesaj numarası (0-65535)

**Tag Set ID (etiket kümesi kimliği) Belirlenmesi:**

```python
# Tag set 0 (initial, after NSR)
tagset_id = 0

# After first ratchet (tag set 1)
# Both Alice and Bob sent key ID 0
tagset_id = 1 + 0 + 0 = 1

# After second ratchet (tag set 2)
# Alice sent key ID 1, Bob still using key ID 0
tagset_id = 1 + 1 + 0 = 2

# After third ratchet (tag set 3)
# Alice still using key ID 1, Bob sent key ID 1
tagset_id = 1 + 1 + 1 = 3
```
**Tek ACK Örneği:**

```python
# ACK message from tag set 5, message number 127
ack_block = ACKBlock(
    tagset_id=5,
    message_number=127
)

# Wire format (7 bytes):
# 08 00 04 00 05 00 7F
# |  |  |  |  |  |  |
# |  |  |  |  |  |  +-- N (127)
# |  |  |  |  +--------- N high byte
# |  |  |  +------------ tagset_id (5)
# |  |  +--------------- tagset_id high byte
# |  +------------------ size (4)
# +--------------------- type (8)
```
**Birden Çok ACK Örneği:**

```python
# ACK three messages
ack_block = ACKBlock([
    (tagset_id=3, N=42),
    (tagset_id=3, N=43),
    (tagset_id=4, N=0)
])

# Wire format (15 bytes):
# 08 00 0C 00 03 00 2A 00 03 00 2B 00 04 00 00
#                (ts=3, N=42) (ts=3, N=43) (ts=4, N=0)
```
**İşleme:**

```python
def process_ack_block(block):
    num_acks = block.size // 4
    
    for i in range(num_acks):
        offset = i * 4
        tagset_id = struct.unpack('>H', block.data[offset:offset+2])[0]
        message_num = struct.unpack('>H', block.data[offset+2:offset+4])[0]
        
        # Mark message as acknowledged
        mark_acked(tagset_id, message_num)
        
        # May trigger retransmission timeout cancellation
        cancel_retransmit_timer(tagset_id, message_num)
```
**ACK'ler Ne Zaman Gönderilmeli:**

1. **Açık ACK İsteği**: ACK İsteği bloğuna her zaman yanıt verin
2. **LeaseSet Teslimi**: Gönderen, iletiye LeaseSet eklediğinde
3. **Oturum Kurulumu**: NS/NSR'yi ACK edebilir (NS/NSR: New Session/New Session Reply - Yeni Oturum/Yeni Oturum Yanıtı; protokol her ne kadar ES (Existing Session - Mevcut Oturum) üzerinden örtük ACK'i tercih etse de)
4. **Ratchet Onayı**: NextKey (bir sonraki anahtar) alımını ACK edebilir (ratchet: kriptografik anahtar ilerletme mekanizması)
5. **Uygulama Katmanı**: Üst katman protokolünün gerektirdiği şekilde (ör. Streaming (I2P akış katmanı))

**ACK Zamanlaması:**

```python
class ACKManager:
    def __init__(self):
        self.pending_acks = []
        self.ack_timer = None
    
    def request_ack(self, tagset_id, message_num):
        self.pending_acks.append((tagset_id, message_num))
        
        if not self.ack_timer:
            # Delay ACK briefly to allow higher layer to respond
            self.ack_timer = set_timer(0.1, self.send_acks)  # 100ms
    
    def send_acks(self):
        if self.pending_acks and not has_outbound_data():
            # No higher layer data, send explicit ACK
            send_es_message(build_ack_block(self.pending_acks))
        
        # Otherwise, ACK will piggyback on next ES message
        self.pending_acks = []
        self.ack_timer = None
```
### ACK İstek Bloğu (Tip 9)

**Amaç**: Mevcut mesaj için bant içi alındı onayı talep etmek

**Biçim:**

```
+----+----+----+----+
| 9  |    1    |flg |
+----+----+----+----+
```
**Alanlar:**

- `blk`: 9
- `size`: 1
- `flg`: 1 bayt - Bayraklar (tüm bitler şu anda kullanılmamaktadır, 0'a ayarlanmıştır)

**Kullanım:**

```python
# Request ACK for this message
payload = [
    build_ack_request_block(),
    build_garlic_clove(important_data)
]
```
**Alıcı Yanıtı:**

ACK isteği alındığında:

1. **Anlık Veriyle**: ACK bloğunu anlık yanıta dahil edin
2. **Anlık Veri Olmadan**: Bir zamanlayıcı başlatın (ör. 100ms) ve zamanlayıcı süresi dolarsa ACK ile boş bir ES gönderin
3. **Tag Set ID (etiket kümesi kimliği)**: Geçerli gelen tagset kimliğini kullanın
4. **Mesaj Numarası**: Alınan session tag (oturum etiketi) ile ilişkili mesaj numarasını kullanın

**İşleme:**

```python
def process_ack_request(message):
    # Extract message identification
    tagset_id = message.tagset_id
    message_num = message.message_num
    
    # Schedule ACK
    schedule_ack(tagset_id, message_num)
    
    # If no data to send immediately, start timer
    if not has_pending_data():
        set_timer(0.1, lambda: send_ack_only(tagset_id, message_num))
```
**ACK İsteği ne zaman kullanılır:**

1. **Kritik Mesajlar**: Alındı onayı verilmesi gereken mesajlar
2. **LeaseSet Teslimi**: Bir LeaseSet'i paket içine dahil ederken
3. **Session Ratchet (oturum ratchet mekanizması)**: NextKey block (bir sonraki anahtar bloğu) gönderdikten sonra
4. **İletimin Sonu**: Gönderenin artık gönderecek verisi kalmadığında ancak onay istediğinde

**Ne Zaman Kullanılmamalı:**

1. **Akış Protokolü**: Akış katmanı ACK'leri (alındı onayı) işler
2. **Yüksek Frekanslı Mesajlar**: Her mesaj için ACK isteğinden kaçının (ek yük)
3. **Önemsiz Datagramlar**: Ham datagramlar genellikle ACK'lere gerek duymaz

### Sonlandırma Bloğu (Tür 4)

**Durum**: UYGULANMADI

**Amaç**: Oturumu sorunsuz bir şekilde sonlandırmak

**Biçim:**

```
+----+----+----+----+----+----+----+----+
| 4  |  size   | rsn|     addl data     |
+----+----+----+----+                   +
~               ...                     ~
+----+----+----+----+----+----+----+----+
```
**Alanlar:**

- `blk`: 4
- `size`: 1 veya daha fazla bayt
- `rsn`: 1 bayt - Sebep kodu
- `addl data`: İsteğe bağlı ek veri (biçim nedene bağlıdır)

**Gerekçe Kodları:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Meaning</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Additional Data</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Normal close / unspecified</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">None</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Termination received</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">None</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Idle timeout</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">None (implementation-specific)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Resource exhaustion</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">None (implementation-specific)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4+</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implementation-specific</td>
    </tr>
  </tbody>
</table>
**Kullanım (uygulandığında):**

```python
# Normal session close
termination = TerminationBlock(
    reason=0,
    additional_data=b''
)

# Session termination due to received termination
termination = TerminationBlock(
    reason=1,
    additional_data=b''
)
```
**Kurallar:**

- Padding (doldurma) dışında son blok olmak ZORUNLUDUR
- Varsa Termination (sonlandırma) sonrasında Padding gelmesi ZORUNLUDUR
- NS veya NSR iletilerinde izin verilmez
- Yalnızca ES iletilerinde izin verilir

### Seçenekler Bloğu (Tür 5)

**Durum**: UYGULANMADI

**Amaç**: Oturum parametrelerinin müzakere edilmesi

**Biçim:**

```
+----+----+----+----+----+----+----+----+
| 5  |  size   |ver |flg |STL |STimeout |
+----+----+----+----+----+----+----+----+
|  SOTW   |  RITW   |tmin|tmax|rmin|rmax|
+----+----+----+----+----+----+----+----+
|  tdmy   |  rdmy   |  tdelay |  rdelay |
+----+----+----+----+----+----+----+----+
|              more_options             |
~               ...                     ~
|                                       |
+----+----+----+----+----+----+----+----+
```
**Alanlar:**

- `blk`: 5
- `size`: 21 veya daha fazla bayt
- `ver`: 1 bayt - Protokol sürümü (0 olmalı)
- `flg`: 1 bayt - Bayraklar (şu anda tüm bitler kullanılmıyor)
- `STL`: 1 bayt - Oturum etiketi uzunluğu (8 olmalı)
- `STimeout`: 2 bayt - Oturum boşta kalma zaman aşımı (saniye cinsinden, big-endian)
- `SOTW`: 2 bayt - Gönderen Giden Etiket Penceresi (big-endian)
- `RITW`: 2 bayt - Alıcı Gelen Etiket Penceresi (big-endian)
- `tmin`, `tmax`, `rmin`, `rmax`: Her biri 1 bayt - Dolgu parametreleri (4.4 sabit noktalı)
- `tdmy`: 2 bayt - Göndermeye istekli olunan en yüksek dummy traffic (sahte trafik) (bytes/sec, big-endian)
- `rdmy`: 2 bayt - İstenen dummy traffic (bytes/sec, big-endian)
- `tdelay`: 2 bayt - Eklemeye istekli olunan en yüksek mesaj içi gecikme (msec, big-endian)
- `rdelay`: 2 bayt - İstenen mesaj içi gecikme (msec, big-endian)
- `more_options`: Değişken uzunluklu - Gelecekteki genişletmeler

**Dolgu Parametreleri (4.4 Sabit Noktalı):**

```python
def encode_padding_ratio(ratio):
    """
    Encode padding ratio as 4.4 fixed-point
    
    ratio: 0.0 to 15.9375
    returns: 0x00 to 0xFF
    """
    return int(ratio * 16)

def decode_padding_ratio(encoded):
    """
    Decode 4.4 fixed-point to ratio
    
    encoded: 0x00 to 0xFF
    returns: 0.0 to 15.9375
    """
    return encoded / 16.0

# Examples:
# 0x00 = 0.0 (no padding)
# 0x01 = 0.0625 (6.25% padding)
# 0x10 = 1.0 (100% padding - double traffic)
# 0x80 = 8.0 (800% padding - 9x traffic)
# 0xFF = 15.9375 (1593.75% padding)
```
**Tag Window Negotiation (Etiket Penceresi Müzakeresi):**

```python
# SOTW: Sender's recommendation for receiver's inbound window
# RITW: Sender's declaration of own inbound window

# Receiver calculates actual inbound window:
inbound_window = calculate_window(
    sender_suggestion=SOTW,
    own_constraints=MAX_INBOUND_TAGS,
    own_resources=available_memory()
)

# Sender uses:
# - RITW to know how far ahead receiver will accept
# - Own SOTW to hint optimal window size
```
**Varsayılan Değerler (Seçenekler müzakere edilmediğinde):**

```python
DEFAULT_OPTIONS = {
    'version': 0,
    'session_tag_length': 8,
    'session_timeout': 600,  # 10 minutes
    'sender_outbound_tag_window': 160,
    'receiver_inbound_tag_window': 160,
    'tmin': 0x00,  # No minimum padding
    'tmax': 0x10,  # Up to 100% padding
    'rmin': 0x00,  # No minimum requested
    'rmax': 0x10,  # Up to 100% requested
    'tdmy': 0,     # No dummy traffic
    'rdmy': 0,     # No dummy traffic requested
    'tdelay': 0,   # No delay
    'rdelay': 0    # No delay requested
}
```
### Mesaj Numaraları Bloğu (Tür 6)

**Durum**: UYGULANMADI

**Amaç**: Önceki etiket kümesinde gönderilen son mesajı belirtir (boşluk algılamayı etkinleştirir)

**Biçim:**

```
+----+----+----+----+----+
| 6  |    2    |  PN    |
+----+----+----+----+----+
```
**Alanlar:**

- `blk`: 6
- `size`: 2
- `PN`: 2 bayt - Önceki etiket kümesinin son ileti numarası (big-endian (yüksek anlamlı bayt önce), 0-65535)

**PN (Previous Number - Önceki Numara) Tanımı:**

PN, önceki etiket kümesinde gönderilen son etiketin indeksidir.

**Kullanım (uygulandığında):**

```python
# After ratcheting to new tag set
# Old tag set: sent messages 0-4095
# New tag set: sending first message

payload = [
    MessageNumbersBlock(PN=4095),
    build_garlic_clove(data)
]
```
**Alıcı Faydaları:**

```python
def process_message_numbers(pn_value):
    # Receiver can now:
    
    # 1. Determine if any messages were skipped
    highest_received_in_old_tagset = 4090
    if pn_value > highest_received_in_old_tagset:
        missing_count = pn_value - highest_received_in_old_tagset
        # 5 messages were never received
    
    # 2. Delete tags higher than PN from old tagset
    for tag_index in range(pn_value + 1, MAX_TAG_INDEX):
        delete_tag(old_tagset, tag_index)
    
    # 3. Expire tags ≤ PN after grace period (e.g., 2 minutes)
    schedule_deletion(old_tagset, delay=120)
```
**Kurallar:**

- 0 numaralı etiket kümesinde kesinlikle gönderilmemelidir (önceki etiket kümesi yok)
- Yalnızca ES messages (ES iletileri) içinde gönderilir
- Yalnızca yeni etiket kümesinin ilk ileti(ler)inde gönderilir
- PN değeri, gönderenin bakış açısına göredir (gönderenin gönderdiği son etiket)

**Signal ile ilişkisi:**

Signal Double Ratchet'te, PN mesaj başlığındadır. ECIES'te ise şifreli yük içinde bulunur ve isteğe bağlıdır.

### Dolgu Bloğu (Tür 254)

**Amaç**: Trafik analizine karşı direnç ve mesaj boyutunun gizlenmesi

**Biçim:**

```
+----+----+----+----+----+----+----+----+
|254 |  size   |      padding           |
+----+----+----+                        +
|                                       |
~               ...                     ~
|                                       |
+----+----+----+----+----+----+----+----+
```
**Alanlar:**

- `blk`: 254
- `size`: 0-65516 bayt (big-endian; yüksek anlamlı bayt önde)
- `padding`: Rastgele veya sıfır veri

**Kurallar:**

- Mesajdaki son blok olmalıdır
- Birden fazla dolgu bloğuna izin verilmez
- Sıfır uzunlukta olabilir (yalnızca 3 baytlık başlık)
- Dolgu verisi sıfır değerli baytlar veya rastgele baytlar olabilir

**Varsayılan Doldurma:**

```python
DEFAULT_PADDING_MIN = 0
DEFAULT_PADDING_MAX = 15

def generate_default_padding():
    size = random.randint(DEFAULT_PADDING_MIN, DEFAULT_PADDING_MAX)
    data = random.bytes(size)  # or zeros
    return PaddingBlock(size, data)
```
**Trafik Analizi Direncine Yönelik Stratejiler:**

**Strateji 1: Rastgele Boyut (Varsayılan)**

```python
# Add 0-15 bytes random padding to each message
padding_size = random.randint(0, 15)
padding_block = PaddingBlock(padding_size, random.bytes(padding_size))
```
**Strateji 2: En Yakın Katına Yuvarlama**

```python
# Round total message size to next multiple of 64
target_size = ((message_size + 63) // 64) * 64
padding_size = target_size - message_size - 3  # -3 for block header
padding_block = PaddingBlock(padding_size, random.bytes(padding_size))
```
**Strateji 3: Sabit Mesaj Boyutları**

```python
# Always send 1KB messages
TARGET_MESSAGE_SIZE = 1024
padding_size = TARGET_MESSAGE_SIZE - message_size - 3
padding_block = PaddingBlock(padding_size, random.bytes(padding_size))
```
**Strateji 4: Müzakere Edilen Dolgu (Seçenekler bloğu)**

```python
# Calculate padding based on negotiated parameters
# tmin, tmax from Options block
min_padding = int(payload_size * tmin_ratio)
max_padding = int(payload_size * tmax_ratio)
padding_size = random.randint(min_padding, max_padding)
padding_block = PaddingBlock(padding_size, random.bytes(padding_size))
```
**Yalnızca Dolgudan Oluşan Mesajlar:**

Mesajlar tamamen dolgudan oluşabilir (uygulama verisi içermez):

```python
# Dummy traffic message
payload = [
    PaddingBlock(random.randint(100, 500), random.bytes(...))
]
```
**Uygulama Notları:**

1. **Tamamen Sıfır Dolgu**: Kabul edilebilir (ChaCha20 tarafından şifrelenecektir)
2. **Rastgele Dolgu**: Şifrelemeden sonra ek bir güvenlik sağlamaz ancak daha fazla entropi kullanır
3. **Performans**: Rastgele dolgu üretimi hesaplama açısından maliyetli olabilir; sıfır kullanmayı değerlendirin
4. **Bellek**: Büyük dolgu blokları bant genişliğini tüketir; maksimum boyut konusunda dikkatli olun

---

## Uygulama Kılavuzu

### Önkoşullar

**Kriptografik Kütüphaneler:**

- **X25519**: libsodium, NaCl veya Bouncy Castle
- **ChaCha20-Poly1305**: libsodium, OpenSSL 1.1.0+ veya Bouncy Castle
- **SHA-256**: OpenSSL, Bouncy Castle veya yerleşik dil desteği
- **Elligator2**: Sınırlı kütüphane desteği; özel gerçekleştirim gerektirebilir

**Elligator2 (eliptik eğri noktalarını rastgele görünümlü veriye eşleyen teknik) Uygulaması:**

Elligator2 yaygın olarak uygulanmıyor. Seçenekler:

1. **OBFS4**: Tor'un obfs4 pluggable transport (takılabilir taşıma) özelliği Elligator2 gerçekleştirmesini içerir
2. **Özel Gerçekleme**: [Elligator2 makalesi](https://elligator.cr.yp.to/elligator-20130828.pdf) temel alınarak
3. **kleshni/Elligator**: GitHub'da referans uygulaması

**Java I2P Notu:** Java I2P, özel Elligator2 (bir kriptografik gizleme tekniği) eklemeleriyle net.i2p.crypto.eddsa kütüphanesini kullanır.

### Önerilen Uygulama Sırası

**Aşama 1: Temel Kriptografi** 1. X25519 DH (Diffie-Hellman) anahtar üretimi ve değişimi 2. ChaCha20-Poly1305 AEAD (İlişkili Verili Kimlik Doğrulamalı Şifreleme) şifreleme/şifre çözme 3. SHA-256 karmalama ve MixHash (durum karmasını güncelleme işlemi) 4. HKDF (HMAC tabanlı anahtar türetme fonksiyonu) ile anahtar türetme 5. Elligator2 (eliptik eğri noktalarını rastgele görünüme eşleyen kodlama) kodlama/kod çözme (başlangıçta test vektörleri kullanılabilir)

**Aşama 2: Mesaj Biçimleri** 1. NS message (bağlı olmayan) - en basit biçim 2. NS message (bağlı) - statik anahtar ekler 3. NSR message 4. ES message 5. Blok ayrıştırma ve oluşturma

**Aşama 3: Oturum Yönetimi** 1. Oturum oluşturma ve depolama 2. Etiket kümesi yönetimi (gönderen ve alıcı) 3. Oturum etiketi ratchet (kademeli yenileme mekanizması) 4. Simetrik anahtar ratchet 5. Etiket arama ve pencere yönetimi

**Aşama 4: DH Ratcheting (Diffie-Hellman kademeli mekanizması)** 1. NextKey blokunun işlenmesi 2. DH ratchet KDF (Anahtar Türetme Fonksiyonu) 3. Ratchet sonrasında etiket kümesi oluşturma 4. Birden çok etiket kümesinin yönetimi

**Aşama 5: Protokol Mantığı** 1. NS/NSR/ES durum makinesi 2. Tekrar saldırısı önleme (DateTime, Bloom filtresi) 3. Yeniden iletim mantığı (çoklu NS/NSR) 4. ACK işleme

**Aşama 6: Entegrasyon** 1. I2NP Garlic Clove (garlic encryption içindeki 'diş' öğesi) işleme 2. LeaseSet paketleme 3. Akış protokolü entegrasyonu 4. Datagram protokolü entegrasyonu

### Gönderici Gerçeklemesi

**Giden Oturum Yaşam Döngüsü:**

```python
class OutboundSession:
    def __init__(self, destination, bound=True):
        self.destination = destination
        self.bound = bound
        self.state = SessionState.NEW
        
        # Keys for NS message
        self.ephemeral_keypair = generate_elg2_keypair()
        if bound:
            self.static_key = context.static_keypair
        
        # Will be populated after NSR
        self.outbound_tagset = None
        self.outbound_keyratchet = None
        self.inbound_tagset = None
        self.inbound_keyratchet = None
        
        # Timing
        self.created_time = now()
        self.last_activity = now()
        
        # Retransmission
        self.ns_attempts = []
        self.ns_timer = None
    
    def send_initial_message(self, payload):
        """Send NS message"""
        # Build NS message
        ns_message = self.build_ns_message(payload)
        
        # Send
        send_to_network(self.destination, ns_message)
        
        # Track for retransmission
        self.ns_attempts.append({
            'message': ns_message,
            'time': now(),
            'ephemeral_key': self.ephemeral_keypair,
            'kdf_state': self.save_kdf_state()
        })
        
        # Start timer
        self.ns_timer = set_timer(1.0, self.on_ns_timeout)
        self.state = SessionState.PENDING_REPLY
    
    def build_ns_message(self, payload):
        """Construct NS message"""
        # KDF initialization
        chainKey, h = self.initialize_kdf()
        
        # Ephemeral key section
        elg2_ephemeral = ENCODE_ELG2(self.ephemeral_keypair.public_key)
        h = SHA256(h || self.destination.static_key)
        h = SHA256(h || self.ephemeral_keypair.public_key)
        
        # es DH
        es_shared = DH(self.ephemeral_keypair.private_key, 
                       self.destination.static_key)
        keydata = HKDF(chainKey, es_shared, "", 64)
        chainKey = keydata[0:31]
        k_static = keydata[32:63]
        
        # Encrypt static key section
        if self.bound:
            static_section = self.static_key.public_key
        else:
            static_section = bytes(32)
        
        static_ciphertext = ENCRYPT(k_static, 0, static_section, h)
        h = SHA256(h || static_ciphertext)
        
        # ss DH (if bound)
        if self.bound:
            ss_shared = DH(self.static_key.private_key, 
                          self.destination.static_key)
            keydata = HKDF(chainKey, ss_shared, "", 64)
            chainKey = keydata[0:31]
            k_payload = keydata[32:63]
            nonce = 0
        else:
            k_payload = k_static
            nonce = 1
        
        # Build payload blocks
        payload_data = self.build_ns_payload(payload)
        
        # Encrypt payload
        payload_ciphertext = ENCRYPT(k_payload, nonce, payload_data, h)
        h = SHA256(h || payload_ciphertext)
        
        # Save KDF state for NSR processing
        self.ns_chainkey = chainKey
        self.ns_hash = h
        
        # Assemble message
        return elg2_ephemeral + static_ciphertext + payload_ciphertext
    
    def build_ns_payload(self, application_data):
        """Build NS payload blocks"""
        blocks = []
        
        # DateTime block (required, first)
        blocks.append(build_datetime_block())
        
        # Garlic Clove(s) with application data
        blocks.append(build_garlic_clove(application_data))
        
        # Optionally bundle LeaseSet
        if should_send_leaseset():
            blocks.append(build_garlic_clove(build_leaseset_store()))
        
        # Padding
        blocks.append(build_padding_block(random.randint(0, 15)))
        
        return encode_blocks(blocks)
    
    def on_nsr_received(self, nsr_message):
        """Process NSR and establish ES session"""
        # Cancel retransmission timer
        cancel_timer(self.ns_timer)
        
        # Parse NSR
        tag = nsr_message[0:8]
        elg2_bob_ephemeral = nsr_message[8:40]
        key_section_mac = nsr_message[40:56]
        payload_ciphertext = nsr_message[56:]
        
        # Find corresponding NS attempt
        ns_state = self.find_ns_by_tag(tag)
        if not ns_state:
            raise ValueError("NSR tag doesn't match any NS")
        
        # Restore KDF state
        chainKey = ns_state['chainkey']
        h = ns_state['hash']
        
        # Decode Bob's ephemeral key
        bob_ephemeral = DECODE_ELG2(elg2_bob_ephemeral)
        
        # Mix tag and Bob's ephemeral into hash
        h = SHA256(h || tag)
        h = SHA256(h || bob_ephemeral)
        
        # ee DH
        ee_shared = DH(self.ephemeral_keypair.private_key, bob_ephemeral)
        keydata = HKDF(chainKey, ee_shared, "", 32)
        chainKey = keydata[0:31]
        
        # se DH
        se_shared = DH(self.static_key.private_key, bob_ephemeral)
        keydata = HKDF(chainKey, se_shared, "", 64)
        chainKey = keydata[0:31]
        k_key_section = keydata[32:63]
        
        # Verify key section MAC
        try:
            DECRYPT(k_key_section, 0, key_section_mac, h)
        except AuthenticationError:
            raise ValueError("NSR key section MAC verification failed")
        
        h = SHA256(h || key_section_mac)
        
        # Split for bidirectional ES
        keydata = HKDF(chainKey, ZEROLEN, "", 64)
        k_ab = keydata[0:31]  # Alice → Bob
        k_ba = keydata[32:63]  # Bob → Alice
        
        # Initialize ES tagsets
        self.outbound_tagset = DH_INITIALIZE(chainKey, k_ab)
        self.inbound_tagset = DH_INITIALIZE(chainKey, k_ba)
        
        # Decrypt NSR payload
        k_nsr = HKDF(k_ba, ZEROLEN, "AttachPayloadKDF", 32)
        try:
            payload = DECRYPT(k_nsr, 0, payload_ciphertext, h)
        except AuthenticationError:
            raise ValueError("NSR payload MAC verification failed")
        
        # Process NSR payload blocks
        self.process_payload_blocks(payload)
        
        # Session established
        self.state = SessionState.ESTABLISHED
        self.last_activity = now()
        
        # Send ES message (implicit ACK)
        self.send_es_ack()
    
    def send_es_message(self, payload):
        """Send ES message"""
        if self.state != SessionState.ESTABLISHED:
            raise ValueError("Session not established")
        
        # Get next tag and key
        tag, index = self.outbound_tagset.get_next_tag()
        key = self.outbound_keyratchet.get_key(index)
        
        # Construct nonce
        nonce = construct_nonce(index)
        
        # Build payload blocks
        payload_data = self.build_es_payload(payload)
        
        # AEAD encryption
        ciphertext = ENCRYPT(key, nonce, payload_data, tag)
        
        # Assemble message
        es_message = tag + ciphertext
        
        # Send
        send_to_network(self.destination, es_message)
        
        # Update activity
        self.last_activity = now()
        
        # Check if ratchet needed
        if self.outbound_tagset.should_ratchet():
            self.initiate_ratchet()
```
### Alıcı Gerçeklemesi

**Gelen Oturumun Yaşam Döngüsü:**

```python
class InboundSession:
    def __init__(self):
        self.state = None
        self.bound = False
        self.destination = None
        
        # Keys
        self.remote_ephemeral_key = None
        self.remote_static_key = None
        self.ephemeral_keypair = None
        
        # Tagsets
        self.inbound_tagset = None
        self.outbound_tagset = None
        
        # Timing
        self.created_time = None
        self.last_activity = None
        
        # Paired session
        self.paired_outbound = None
    
    @staticmethod
    def try_decrypt_ns(message):
        """Attempt to decrypt as NS message"""
        # Parse NS structure
        elg2_ephemeral = message[0:32]
        static_ciphertext = message[32:80]  # 32 + 16
        payload_ciphertext = message[80:]
        
        # Decode ephemeral key
        try:
            alice_ephemeral = DECODE_ELG2(elg2_ephemeral)
        except:
            return None  # Not a valid Elligator2 encoding
        
        # Check replay
        if is_replay(alice_ephemeral):
            return None
        
        # KDF initialization
        chainKey, h = initialize_kdf()
        
        # Mix keys
        h = SHA256(h || context.static_keypair.public_key)
        h = SHA256(h || alice_ephemeral)
        
        # es DH
        es_shared = DH(context.static_keypair.private_key, alice_ephemeral)
        keydata = HKDF(chainKey, es_shared, "", 64)
        chainKey = keydata[0:31]
        k_static = keydata[32:63]
        
        # Decrypt static key section
        try:
            static_data = DECRYPT(k_static, 0, static_ciphertext, h)
        except AuthenticationError:
            return None  # Not a valid NS message
        
        h = SHA256(h || static_ciphertext)
        
        # Check if bound or unbound
        if static_data == bytes(32):
            # Unbound
            alice_static_key = None
            k_payload = k_static
            nonce = 1
        else:
            # Bound - perform ss DH
            alice_static_key = static_data
            ss_shared = DH(context.static_keypair.private_key, alice_static_key)
            keydata = HKDF(chainKey, ss_shared, "", 64)
            chainKey = keydata[0:31]
            k_payload = keydata[32:63]
            nonce = 0
        
        # Decrypt payload
        try:
            payload = DECRYPT(k_payload, nonce, payload_ciphertext, h)
        except AuthenticationError:
            return None
        
        h = SHA256(h || payload_ciphertext)
        
        # Create session
        session = InboundSession()
        session.state = SessionState.ESTABLISHED
        session.created_time = now()
        session.last_activity = now()
        session.remote_ephemeral_key = alice_ephemeral
        session.remote_static_key = alice_static_key
        session.bound = (alice_static_key is not None)
        session.ns_chainkey = chainKey
        session.ns_hash = h
        
        # Extract destination if bound
        if session.bound:
            session.destination = extract_destination_from_payload(payload)
        
        # Process payload
        session.process_payload_blocks(payload)
        
        return session
    
    def send_nsr_reply(self, reply_payload):
        """Send NSR message"""
        # Generate NSR tagset
        tagsetKey = HKDF(self.ns_chainkey, ZEROLEN, "SessionReplyTags", 32)
        nsr_tagset = DH_INITIALIZE(self.ns_chainkey, tagsetKey)
        
        # Get tag
        tag, _ = nsr_tagset.get_next_tag()
        
        # Mix tag into hash
        h = SHA256(self.ns_hash || tag)
        
        # Generate ephemeral key
        self.ephemeral_keypair = generate_elg2_keypair()
        bob_ephemeral = self.ephemeral_keypair.public_key
        elg2_bob_ephemeral = ENCODE_ELG2(bob_ephemeral)
        
        # Mix ephemeral key
        h = SHA256(h || bob_ephemeral)
        
        chainKey = self.ns_chainkey
        
        # ee DH
        ee_shared = DH(self.ephemeral_keypair.private_key, 
                      self.remote_ephemeral_key)
        keydata = HKDF(chainKey, ee_shared, "", 32)
        chainKey = keydata[0:31]
        
        # se DH
        se_shared = DH(context.static_keypair.private_key, 
                      self.remote_ephemeral_key)
        keydata = HKDF(chainKey, se_shared, "", 64)
        chainKey = keydata[0:31]
        k_key_section = keydata[32:63]
        
        # Encrypt key section (empty)
        key_section_ciphertext = ENCRYPT(k_key_section, 0, ZEROLEN, h)
        h = SHA256(h || key_section_ciphertext)
        
        # Split for bidirectional ES
        keydata = HKDF(chainKey, ZEROLEN, "", 64)
        k_ab = keydata[0:31]  # Alice → Bob
        k_ba = keydata[32:63]  # Bob → Alice
        
        # Initialize ES tagsets
        self.inbound_tagset = DH_INITIALIZE(chainKey, k_ab)
        self.outbound_tagset = DH_INITIALIZE(chainKey, k_ba)
        
        # Build reply payload
        payload_data = build_payload_blocks(reply_payload)
        
        # Encrypt payload
        k_nsr = HKDF(k_ba, ZEROLEN, "AttachPayloadKDF", 32)
        payload_ciphertext = ENCRYPT(k_nsr, 0, payload_data, h)
        
        # Assemble NSR
        nsr_message = tag + elg2_bob_ephemeral + key_section_ciphertext + payload_ciphertext
        
        # Send
        send_to_network(self.destination, nsr_message)
        
        # Wait for ES
        self.state = SessionState.AWAITING_ES
        self.last_activity = now()
    
    def on_es_received(self, es_message):
        """Process first ES message"""
        if self.state == SessionState.AWAITING_ES:
            # First ES received, confirms session
            self.state = SessionState.ESTABLISHED
        
        # Process ES message
        self.process_es_message(es_message)
    
    def process_es_message(self, es_message):
        """Decrypt and process ES message"""
        # Extract tag
        tag = es_message[0:8]
        ciphertext = es_message[8:]
        
        # Look up tag
        index = self.inbound_tagset.lookup_tag(tag)
        if index is None:
            raise ValueError("Tag not found")
        
        # Get key
        key = self.inbound_keyratchet.get_key(index)
        
        # Construct nonce
        nonce = construct_nonce(index)
        
        # Decrypt
        try:
            payload = DECRYPT(key, nonce, ciphertext, tag)
        except AuthenticationError:
            raise ValueError("ES MAC verification failed")
        
        # Process blocks
        self.process_payload_blocks(payload)
        
        # Update activity
        self.last_activity = now()
```
### Mesaj Sınıflandırması

**Mesaj Türlerini Ayırt Etme:**

```python
def classify_message(message):
    """Determine message type"""
    
    # Minimum lengths
    if len(message) < 24:
        return None  # Too short
    
    # Check for session tag (8 bytes)
    tag = message[0:8]
    
    # Try ES decryption first (most common)
    session = lookup_session_by_tag(tag)
    if session:
        return ('ES', session)
    
    # Try NSR decryption (tag + Elligator2 key)
    if len(message) >= 72:
        # Check if bytes 8-40 are valid Elligator2
        try:
            nsr_ephemeral = DECODE_ELG2(message[8:40])
            nsr_session = find_pending_nsr_by_tag(tag)
            if nsr_session:
                return ('NSR', nsr_session)
        except:
            pass
    
    # Try NS decryption (starts with Elligator2 key)
    if len(message) >= 96:
        try:
            ns_ephemeral = DECODE_ELG2(message[0:32])
            ns_session = InboundSession.try_decrypt_ns(message)
            if ns_session:
                return ('NS', ns_session)
        except:
            pass
    
    # Check ElGamal/AES (for dual-key compatibility)
    if len(message) >= 514:
        if (len(message) - 2) % 16 == 0:
            # Might be ElGamal NS
            return ('ELGAMAL_NS', None)
        elif len(message) % 16 == 0:
            # Might be ElGamal ES
            return ('ELGAMAL_ES', None)
    
    return None  # Unknown message type
```
### Oturum Yönetimi En İyi Uygulamaları

**Oturum Depolama:**

```python
class SessionKeyManager:
    def __init__(self):
        # Outbound sessions (one per destination)
        self.outbound_sessions = {}  # destination -> OutboundSession
        
        # Inbound sessions (multiple per destination during transition)
        self.inbound_sessions = []  # [InboundSession]
        
        # Session tag lookup (fast path for ES messages)
        self.tag_to_session = {}  # tag -> InboundSession
        
        # Limits
        self.max_inbound_sessions = 1000
        self.max_tags_per_session = 160
    
    def get_outbound_session(self, destination):
        """Get or create outbound session"""
        if destination not in self.outbound_sessions:
            session = OutboundSession(destination)
            self.outbound_sessions[destination] = session
        return self.outbound_sessions[destination]
    
    def add_inbound_session(self, session):
        """Add new inbound session"""
        # Check limits
        if len(self.inbound_sessions) >= self.max_inbound_sessions:
            self.expire_oldest_session()
        
        self.inbound_sessions.append(session)
        
        # Add tags to lookup table
        self.register_session_tags(session)
    
    def register_session_tags(self, session):
        """Register session's tags in lookup table"""
        for tag in session.inbound_tagset.get_all_tags():
            self.tag_to_session[tag] = session
    
    def lookup_tag(self, tag):
        """Fast tag lookup"""
        return self.tag_to_session.get(tag)
    
    def expire_sessions(self):
        """Periodic session expiration"""
        now_time = now()
        
        # Expire outbound sessions
        for dest, session in list(self.outbound_sessions.items()):
            if session.idle_time(now_time) > 8 * 60:
                del self.outbound_sessions[dest]
        
        # Expire inbound sessions
        expired = []
        for session in self.inbound_sessions:
            if session.idle_time(now_time) > 10 * 60:
                expired.append(session)
        
        for session in expired:
            self.remove_inbound_session(session)
    
    def remove_inbound_session(self, session):
        """Remove inbound session and clean up tags"""
        self.inbound_sessions.remove(session)
        
        # Remove tags from lookup
        for tag in session.inbound_tagset.get_all_tags():
            if tag in self.tag_to_session:
                del self.tag_to_session[tag]
```
**Bellek Yönetimi:**

```python
class TagMemoryManager:
    def __init__(self, max_memory_kb=10240):  # 10 MB default
        self.max_memory = max_memory_kb * 1024
        self.current_memory = 0
        self.max_tags_per_session = 160
        self.min_tags_per_session = 32
    
    def calculate_tag_memory(self, session):
        """Calculate memory used by session tags"""
        tag_count = len(session.inbound_tagset.tags)
        # Each tag: 8 bytes (tag) + 2 bytes (index) + 32 bytes (key, optional)
        # + overhead
        bytes_per_tag = 16 if session.defer_keys else 48
        return tag_count * bytes_per_tag
    
    def check_pressure(self):
        """Check if under memory pressure"""
        return self.current_memory > (self.max_memory * 0.9)
    
    def handle_pressure(self):
        """Reduce memory usage when under pressure"""
        if not self.check_pressure():
            return
        
        # Strategy 1: Reduce look-ahead windows
        for session in all_sessions:
            if session.look_ahead > self.min_tags_per_session:
                session.reduce_look_ahead(self.min_tags_per_session)
        
        # Strategy 2: Trim old tags aggressively
        for session in all_sessions:
            session.inbound_tagset.trim_behind(aggressive=True)
        
        # Strategy 3: Refuse new ratchets
        for session in all_sessions:
            if session.outbound_tagset.should_ratchet():
                session.defer_ratchet = True
        
        # Strategy 4: Expire idle sessions early
        expire_idle_sessions(threshold=5*60)  # 5 min instead of 10
```
### Test Stratejileri

**Birim Testleri:**

```python
def test_x25519_dh():
    """Test X25519 key exchange"""
    alice_sk = GENERATE_PRIVATE()
    alice_pk = DERIVE_PUBLIC(alice_sk)
    
    bob_sk = GENERATE_PRIVATE()
    bob_pk = DERIVE_PUBLIC(bob_sk)
    
    # Both sides compute same shared secret
    alice_shared = DH(alice_sk, bob_pk)
    bob_shared = DH(bob_sk, alice_pk)
    
    assert alice_shared == bob_shared

def test_elligator2_encode_decode():
    """Test Elligator2 roundtrip"""
    sk = GENERATE_PRIVATE_ELG2()
    pk = DERIVE_PUBLIC(sk)
    
    encoded = ENCODE_ELG2(pk)
    decoded = DECODE_ELG2(encoded)
    
    assert decoded == pk

def test_chacha_poly_encrypt_decrypt():
    """Test ChaCha20-Poly1305 AEAD"""
    key = CSRNG(32)
    nonce = construct_nonce(42)
    plaintext = b"Hello, I2P!"
    ad = b"associated_data"
    
    ciphertext = ENCRYPT(key, nonce, plaintext, ad)
    decrypted = DECRYPT(key, nonce, ciphertext, ad)
    
    assert decrypted == plaintext

def test_session_tag_ratchet():
    """Test session tag generation"""
    sessTag_ck = CSRNG(32)
    tagset = SessionTagRatchet(sessTag_ck)
    
    # Generate 100 tags
    tags = [tagset.get_next_tag() for _ in range(100)]
    
    # All tags should be unique
    assert len(set(tags)) == 100
    
    # Each tag should be 8 bytes
    for tag in tags:
        assert len(tag) == 8
```
**Entegrasyon Testleri:**

```python
def test_ns_nsr_handshake():
    """Test NS/NSR handshake"""
    # Alice creates outbound session
    alice_session = OutboundSession(bob_destination, bound=True)
    
    # Alice sends NS
    ns_message = alice_session.build_ns_message(b"Hello Bob")
    
    # Bob receives NS
    bob_session = InboundSession.try_decrypt_ns(ns_message)
    assert bob_session is not None
    assert bob_session.bound == True
    
    # Bob sends NSR
    nsr_message = bob_session.build_nsr_message(b"Hello Alice")
    
    # Alice receives NSR
    alice_session.on_nsr_received(nsr_message)
    assert alice_session.state == SessionState.ESTABLISHED
    
    # Both should have matching ES tagsets
    # (Cannot directly compare, but can test by sending ES messages)

def test_es_bidirectional():
    """Test ES messages in both directions"""
    # (After NS/NSR handshake)
    
    # Alice sends ES to Bob
    es_alice_to_bob = alice_session.send_es_message(b"Data from Alice")
    
    # Bob receives ES
    bob_session.process_es_message(es_alice_to_bob)
    
    # Bob sends ES to Alice
    es_bob_to_alice = bob_session.send_es_message(b"Data from Bob")
    
    # Alice receives ES
    alice_session.process_es_message(es_bob_to_alice)

def test_dh_ratchet():
    """Test DH ratchet"""
    # (After established session)
    
    # Alice initiates ratchet
    alice_session.initiate_ratchet()
    nextkey_alice = build_nextkey_block(
        flags=0x01,
        key_id=0,
        public_key=alice_new_key
    )
    
    # Send to Bob
    bob_session.process_nextkey_block(nextkey_alice)
    
    # Bob replies
    nextkey_bob = build_nextkey_block(
        flags=0x03,
        key_id=0,
        public_key=bob_new_key
    )
    
    # Send to Alice
    alice_session.process_nextkey_block(nextkey_bob)
    
    # Both should now be using new tagsets
    assert alice_session.outbound_tagset.id == 1
    assert bob_session.inbound_tagset.id == 1
```
**Test Vektörleri:**

Spesifikasyonda yer alan test vektörlerini uygulayın:

1. **Noise IK el sıkışması**: Standart Noise test vektörlerini kullanın
2. **HKDF**: RFC 5869 test vektörlerini kullanın
3. **ChaCha20-Poly1305**: RFC 7539 test vektörlerini kullanın
4. **Elligator2**: Elligator2 makalesinden veya OBFS4'ten test vektörlerini kullanın

**Birlikte Çalışabilirlik Testleri:**

1. **Java I2P**: Java I2P referans uygulamasına karşı test edin
2. **i2pd**: C++ i2pd uygulamasına karşı test edin
3. **Paket Yakalamaları**: Mesaj biçimlerini doğrulamak için Wireshark dissector (varsa) kullanın
4. **Uygulamalar Arası**: Uygulamalar arasında gönderme/alma yapabilen bir test düzeneği oluşturun

### Performansla İlgili Hususlar

**Anahtar Üretimi:**

Elligator2 (kriptografik eşleme yöntemi) anahtar üretimi hesaplama açısından pahalıdır (%50 reddedilme oranı):

```python
class KeyPool:
    """Pre-generate keys in background thread"""
    def __init__(self, pool_size=10):
        self.pool = Queue(maxsize=pool_size)
        self.generator_thread = Thread(target=self.generate_keys, daemon=True)
        self.generator_thread.start()
    
    def generate_keys(self):
        while True:
            if not self.pool.full():
                keypair = generate_elg2_keypair()
                # Also compute encoded form
                encoded = ENCODE_ELG2(keypair.public_key)
                self.pool.put((keypair, encoded))
            else:
                sleep(0.1)
    
    def get_keypair(self):
        try:
            return self.pool.get(timeout=1.0)
        except Empty:
            # Pool exhausted, generate inline
            return generate_elg2_keypair()
```
**Etiket Sorgulaması:**

O(1) etiket araması için hash tabloları kullanın:

```python
class FastTagLookup:
    def __init__(self):
        self.tag_to_session = {}  # Python dict is hash table
    
    def add_tag(self, tag, session, index):
        # 8-byte tag as bytes is hashable
        self.tag_to_session[tag] = (session, index)
    
    def lookup_tag(self, tag):
        return self.tag_to_session.get(tag)
```
**Bellek Optimizasyonu:**

Simetrik anahtar üretimini ertele:

```python
class DeferredKeyRatchet:
    """Only generate keys when needed"""
    def __init__(self, symmKey_ck):
        self.chainKey = symmKey_ck
        self.index = -1
        self.cache = LRUCache(maxsize=32)  # Cache recent keys
    
    def get_key(self, index):
        # Check cache first
        if index in self.cache:
            return self.cache[index]
        
        # Generate keys up to index
        while self.index < index:
            self.index += 1
            keydata = HKDF(self.chainKey, ZEROLEN, "SymmetricRatchet", 64)
            self.chainKey = keydata[0:31]
            
            if self.index == index:
                key = keydata[32:63]
                self.cache[index] = key
                return key
```
**Toplu İşleme:**

Birden çok mesajı toplu olarak işleyin:

```python
def process_message_batch(messages):
    """Process multiple messages efficiently"""
    results = []
    
    # Group by type
    ns_messages = []
    nsr_messages = []
    es_messages = []
    
    for msg in messages:
        msg_type = classify_message(msg)
        if msg_type[0] == 'NS':
            ns_messages.append(msg)
        elif msg_type[0] == 'NSR':
            nsr_messages.append(msg)
        elif msg_type[0] == 'ES':
            es_messages.append(msg)
    
    # Process in batches
    # ES messages are most common, process first
    for msg in es_messages:
        results.append(process_es_message(msg))
    
    for msg in nsr_messages:
        results.append(process_nsr_message(msg))
    
    for msg in ns_messages:
        results.append(process_ns_message(msg))
    
    return results
```
---

## Güvenlik Hususları

### Tehdit Modeli

**Saldırganın Yetenekleri:**

1. **Pasif Gözlemci**: Tüm ağ trafiğini gözlemleyebilir
2. **Aktif Saldırgan**: İletileri enjekte edebilir, değiştirebilir, düşürebilir, yeniden oynatabilir
3. **Kompromize Düğüm**: Bir router'ı veya bir hedefi kompromize edebilir
4. **Trafik Analizi**: Trafik kalıpları üzerinde istatistiksel analiz yapabilir

**Güvenlik Hedefleri:**

1. **Gizlilik**: Mesaj içerikleri gözlemciden gizlenir
2. **Kimlik Doğrulama**: Göndericinin kimliği doğrulanır (bağlı oturumlar için)
3. **İleri Gizlilik**: Anahtarlar ele geçirilse bile geçmiş mesajlar gizli kalır
4. **Yeniden Oynatmayı Önleme**: Eski mesajlar yeniden oynatılamaz
5. **Trafik Gizleme**: El sıkışmaları rastgele veriden ayırt edilemez

### Kriptografik Varsayımlar

**Zorluk Varsayımları:**

1. **X25519 CDH**: Curve25519 üzerinde Hesaplamalı Diffie-Hellman (CDH) probleminin çözümü hesaplamalı olarak zordur
2. **ChaCha20 PRF**: ChaCha20 bir psödo-rastgele fonksiyondur
3. **Poly1305 MAC**: Poly1305, seçilmiş mesaj saldırısı altında taklit edilemezlik sağlar
4. **SHA-256 CR**: SHA-256 çakışmaya dayanıklıdır
5. **HKDF Security**: HKDF, anahtarları eş dağılımlı olacak şekilde çıkarır ve genişletir

**Güvenlik Düzeyleri:**

- **X25519**: ~128-bit güvenlik düzeyi (eğrinin mertebesi 2^252)
- **ChaCha20**: 256-bit anahtarlar, 256-bit güvenlik düzeyi
- **Poly1305**: 128-bit güvenlik düzeyi (çakışma olasılığı)
- **SHA-256**: 128-bit çakışma direnci, 256-bit ön-imaj direnci

### Anahtar Yönetimi

**Anahtar Oluşturma:**

```python
# CRITICAL: Use cryptographically secure RNG
def CSRNG(length):
    # GOOD: os.urandom, secrets.token_bytes (Python)
    # GOOD: /dev/urandom (Linux)
    # GOOD: BCryptGenRandom (Windows)
    # BAD: random.random(), Math.random() (NOT cryptographically secure)
    return os.urandom(length)

# CRITICAL: Validate keys
def validate_x25519_key(pubkey):
    # Check for weak keys (all zeros, small order points)
    if pubkey == bytes(32):
        raise WeakKeyError("All-zero public key")
    
    # Perform DH to check for weak shared secrets
    test_shared = DH(test_private_key, pubkey)
    if test_shared == bytes(32):
        raise WeakKeyError("Results in zero shared secret")
```
**Anahtar Depolama:**

```python
# CRITICAL: Protect private keys
class SecureKeyStorage:
    def __init__(self):
        # Store in memory with protection
        self.keys = {}
        
        # Option 1: Memory locking (prevent swapping to disk)
        # mlock(self.keys)
        
        # Option 2: Encrypted storage
        # self.encryption_key = derive_from_password()
    
    def store_key(self, key_id, private_key):
        # Option: Encrypt before storage
        # encrypted = encrypt(private_key, self.encryption_key)
        # self.keys[key_id] = encrypted
        self.keys[key_id] = private_key
    
    def delete_key(self, key_id):
        # Securely wipe memory
        if key_id in self.keys:
            key = self.keys[key_id]
            # Overwrite with zeros before deletion
            for i in range(len(key)):
                key[i] = 0
            del self.keys[key_id]
```
**Anahtar Döndürme:**

```python
# CRITICAL: Rotate keys regularly
class KeyRotationPolicy:
    def __init__(self):
        self.max_messages_per_tagset = 4096  # Ratchet before 65535
        self.max_tagset_age = 10 * 60       # 10 minutes
        self.max_session_age = 60 * 60      # 1 hour
    
    def should_ratchet(self, tagset):
        return (tagset.messages_sent >= self.max_messages_per_tagset or
                tagset.age() >= self.max_tagset_age)
    
    def should_replace_session(self, session):
        return session.age() >= self.max_session_age
```
### Saldırı Azaltma Önlemleri

### Yeniden Oynatma Saldırılarına Karşı Önlemler

**DateTime (tarih-saat) Doğrulaması:**

```python
MAX_CLOCK_SKEW_PAST = 5 * 60
MAX_CLOCK_SKEW_FUTURE = 2 * 60

def validate_datetime(timestamp):
    now = int(time.time())
    age = now - timestamp
    
    if age < -MAX_CLOCK_SKEW_FUTURE:
        raise ReplayError("Timestamp too far in future")
    
    if age > MAX_CLOCK_SKEW_PAST:
        raise ReplayError("Timestamp too old")
    
    return True
```
**NS Mesajları için Bloom Filtresi:**

```python
class ReplayFilter:
    def __init__(self, capacity=100000, error_rate=0.001, duration=5*60):
        self.bloom = BloomFilter(capacity=capacity, error_rate=error_rate)
        self.duration = duration
        self.entries = []  # (timestamp, ephemeral_key)
    
    def check_replay(self, ephemeral_key, timestamp):
        # Validate timestamp
        if not validate_datetime(timestamp):
            return False
        
        # Check Bloom filter
        if ephemeral_key in self.bloom:
            # Potential replay (or false positive)
            # Check exact match in entries
            for ts, key in self.entries:
                if key == ephemeral_key:
                    return False  # Definite replay
        
        # Add to filter
        self.bloom.add(ephemeral_key)
        self.entries.append((timestamp, ephemeral_key))
        
        # Expire old entries
        self.expire_old_entries()
        
        return True
    
    def expire_old_entries(self):
        now = int(time.time())
        self.entries = [(ts, key) for ts, key in self.entries
                       if now - ts < self.duration]
```
**Session Tag (oturum etiketi) Tek Seferlik Kullanım:**

```python
def process_session_tag(tag):
    # Look up tag
    entry = tagset.lookup_tag(tag)
    if entry is None:
        raise ValueError("Invalid session tag")
    
    # CRITICAL: Remove tag immediately (one-time use)
    tagset.remove_tag(tag)
    
    # Use associated key
    return entry.key, entry.index
```
### Key Compromise Impersonation (KCI) (anahtar ele geçirilmesi kaynaklı kimlik taklidi) için Önlemler

**Sorun**: NS mesaj kimlik doğrulaması KCI'ye (Key Compromise Impersonation - anahtar ele geçirilmesiyle kimlik taklidi) karşı savunmasızdır (Kimlik Doğrulama Düzeyi 1)

**Azaltma**:

1. Mümkün olan en kısa sürede NSR (Authentication Level 2 - Kimlik Doğrulama Seviyesi 2) durumuna geçin
2. Güvenlik açısından kritik işlemler için NS payload (yük)'a güvenmeyin
3. Geri döndürülemez işlemleri gerçekleştirmeden önce NSR onayını bekleyin

```python
def process_ns_message(ns_message):
    # NS authenticated at Level 1 (KCI vulnerable)
    # Do NOT perform security-critical operations yet
    
    # Extract sender's static key
    sender_key = ns_message.static_key
    
    # Mark session as pending Level 2 authentication
    session.auth_level = 1
    session.sender_key = sender_key
    
    # Send NSR
    send_nsr_reply(session)

def process_first_es_message(es_message):
    # Now we have Level 2 authentication (KCI resistant)
    session.auth_level = 2
    
    # Safe to perform security-critical operations
    process_security_critical_operation(es_message)
```
### Hizmet Reddi (DoS) Azaltma Önlemleri

**NS Flood Koruması:**

```python
class NSFloodProtection:
    def __init__(self):
        self.ns_count = defaultdict(int)  # source -> count
        self.ns_timestamps = defaultdict(list)  # source -> [timestamps]
        
        self.max_ns_per_source = 5
        self.rate_window = 10  # seconds
        self.max_concurrent_ns = 100
    
    def check_ns_allowed(self, source):
        # Global limit
        total_pending = sum(self.ns_count.values())
        if total_pending >= self.max_concurrent_ns:
            return False
        
        # Per-source rate limit
        now = time.time()
        timestamps = self.ns_timestamps[source]
        
        # Remove old timestamps
        timestamps = [ts for ts in timestamps if now - ts < self.rate_window]
        self.ns_timestamps[source] = timestamps
        
        # Check rate
        if len(timestamps) >= self.max_ns_per_source:
            return False
        
        # Allow NS
        timestamps.append(now)
        self.ns_count[source] += 1
        return True
    
    def on_session_established(self, source):
        # Decrease pending count
        if self.ns_count[source] > 0:
            self.ns_count[source] -= 1
```
**Etiket Depolama Sınırları:**

```python
class TagStorageLimit:
    def __init__(self, max_tags=1000000):
        self.max_tags = max_tags
        self.current_tags = 0
    
    def can_create_session(self, look_ahead):
        if self.current_tags + look_ahead > self.max_tags:
            return False
        return True
    
    def add_tags(self, count):
        self.current_tags += count
    
    def remove_tags(self, count):
        self.current_tags -= count
```
**Uyarlanabilir Kaynak Yönetimi:**

```python
class AdaptiveResourceManager:
    def __init__(self):
        self.load_level = 0  # 0 = low, 1 = medium, 2 = high, 3 = critical
    
    def adjust_parameters(self):
        if self.load_level == 0:
            # Normal operation
            return {
                'max_look_ahead': 160,
                'max_sessions': 1000,
                'session_timeout': 10 * 60
            }
        
        elif self.load_level == 1:
            # Moderate load
            return {
                'max_look_ahead': 80,
                'max_sessions': 800,
                'session_timeout': 8 * 60
            }
        
        elif self.load_level == 2:
            # High load
            return {
                'max_look_ahead': 32,
                'max_sessions': 500,
                'session_timeout': 5 * 60
            }
        
        else:  # load_level == 3
            # Critical load
            return {
                'max_look_ahead': 16,
                'max_sessions': 200,
                'session_timeout': 3 * 60
            }
```
### Trafik Analizi Direnci

**Elligator2 (eliptik eğri noktalarını rastgele veri gibi gösteren bir teknik) Kodlaması:**

El sıkışma mesajlarının rastgele veriden ayırt edilemez olmasını sağlar:

```python
# NS and NSR start with Elligator2-encoded ephemeral keys
# Observer cannot distinguish from random 32-byte string
```
**Dolgu Stratejileri:**

```python
# Resist message size fingerprinting
def add_padding(payload, strategy='random'):
    if strategy == 'random':
        # Random padding 0-15 bytes
        size = random.randint(0, 15)
    
    elif strategy == 'round':
        # Round to next 64-byte boundary
        target = ((len(payload) + 63) // 64) * 64
        size = target - len(payload) - 3  # -3 for block header
    
    elif strategy == 'fixed':
        # Always 1KB messages
        size = 1024 - len(payload) - 3
    
    return build_padding_block(size)
```
**Zamanlama Saldırıları:**

```python
# CRITICAL: Use constant-time operations
def constant_time_compare(a, b):
    """Constant-time byte string comparison"""
    if len(a) != len(b):
        return False
    
    result = 0
    for x, y in zip(a, b):
        result |= x ^ y
    
    return result == 0

# CRITICAL: Constant-time MAC verification
def verify_mac(computed_mac, received_mac):
    if not constant_time_compare(computed_mac, received_mac):
        # Always take same time regardless of where comparison fails
        raise AuthenticationError("MAC verification failed")
```
### Uygulama Tuzakları

**Yaygın Hatalar:**

1. **Nonce (tek kullanımlık sayı) Yeniden Kullanımı**: (key, nonce) çiftlerini ASLA yeniden kullanmayın
   ```python
   # BAD: Reusing nonce with same key
   ciphertext1 = ENCRYPT(key, nonce, plaintext1, ad1)
   ciphertext2 = ENCRYPT(key, nonce, plaintext2, ad2)  # CATASTROPHIC

# İYİ: Her mesaj için benzersiz nonce (tek kullanımlık sayı)    ciphertext1 = ENCRYPT(key, nonce1, plaintext1, ad1)    ciphertext2 = ENCRYPT(key, nonce2, plaintext2, ad2)

   ```

2. **Ephemeral Key Reuse**: Generate fresh ephemeral key for each NS/NSR
   ```python
# KÖTÜ: Geçici anahtarın yeniden kullanımı    ephemeral_key = generate_elg2_keypair()    send_ns_message(ephemeral_key)    send_ns_message(ephemeral_key)  # KÖTÜ

# İYİ: Her mesaj için yeni bir anahtar    send_ns_message(generate_elg2_keypair())    send_ns_message(generate_elg2_keypair())

   ```

3. **Weak RNG**: Use cryptographically secure random number generator
   ```python
# KÖTÜ: Kriptografik olmayan rastgele sayı üreteci (RNG)    import random    key = bytes([random.randint(0, 255) for _ in range(32)])  # GÜVENSİZ

# DOĞRU: Kriptografik olarak güvenli rastgele sayı üreteci    import os    key = os.urandom(32)

   ```

4. **Timing Attacks**: Use constant-time comparisons
   ```python
# KÖTÜ: Erken çıkışlı karşılaştırma    if computed_mac == received_mac:  # Zamanlama sızıntısı

       pass
   
# İYİ: Sabit zamanlı karşılaştırma    if constant_time_compare(computed_mac, received_mac):

       pass
   ```

5. **Incomplete MAC Verification**: Always verify before using data
   ```python
# YANLIŞ: Doğrulamadan önce şifre çözme    plaintext = chacha20_decrypt(key, nonce, ciphertext)    mac_ok = verify_mac(mac, plaintext)  # ÇOK GEÇ    if not mac_ok:

       return error
   
# DOĞRU: AEAD (ek verili kimlik doğrulamalı şifreleme) şifre çözmeden önce doğrular    try:

       plaintext = DECRYPT(key, nonce, ciphertext, ad)  # Verifies MAC first
except AuthenticationError:

       return error
   ```

6. **Key Deletion**: Securely wipe keys from memory
   ```python
# KÖTÜ: Basit silme    del private_key  # Hâlâ bellekte

# İYİ: Silmeden önce üzerine yazın    for i in range(len(private_key)):

       private_key[i] = 0
del private_key

   ```

### Security Audits

**Recommended Audits:**

1. **Cryptographic Review**: Expert review of KDF chains and DH operations
2. **Implementation Audit**: Code review for timing attacks, key management, RNG usage
3. **Protocol Analysis**: Formal verification of handshake security properties
4. **Side-Channel Analysis**: Timing, power, and cache attacks
5. **Fuzzing**: Random input testing for parser robustness

**Test Cases:**

```python
# Güvenlik açısından kritik test vakaları

def test_nonce_uniqueness():

    """Ensure nonces are never reused"""
    nonces = set()
    for i in range(10000):
        nonce = construct_nonce(i)
        assert nonce not in nonces
        nonces.add(nonce)

def test_key_isolation():

    """Ensure sessions don't share keys"""
    session1 = create_session(destination1)
    session2 = create_session(destination2)
    
    assert session1.key != session2.key

def test_replay_prevention():

    """Ensure replay attacks are detected"""
    ns_message = create_ns_message()
    
    # First delivery succeeds
    assert process_ns_message(ns_message) == True
    
    # Replay fails
    assert process_ns_message(ns_message) == False

def test_mac_verification():

    """Ensure MAC verification is enforced"""
    key = CSRNG(32)
    nonce = construct_nonce(0)
    plaintext = b"test"
    ad = b"test_ad"
    
    ciphertext = ENCRYPT(key, nonce, plaintext, ad)
    
    # Correct MAC verifies
    assert DECRYPT(key, nonce, ciphertext, ad) == plaintext
    
    # Corrupted MAC fails
    corrupted = ciphertext[:-1] + bytes([ciphertext[-1] ^ 0xFF])
    with pytest.raises(AuthenticationError):
        DECRYPT(key, nonce, corrupted, ad)
```

---

## Configuration and Deployment

### I2CP Configuration

**Enable ECIES Encryption:**

```properties
# Yalnızca ECIES (Eliptik Eğri Entegre Şifreleme Şeması) (yeni kurulumlar için önerilir)

i2cp.leaseSetEncType=4

# Çift anahtarlı (uyumluluk için ECIES + ElGamal)

i2cp.leaseSetEncType=4,0

# Yalnızca ElGamal (eski, önerilmez)

i2cp.leaseSetEncType=0

```

**LeaseSet Type:**

```properties
# Standart LS2 (en yaygın)

i2cp.leaseSetType=3

# Şifreli LS2 (blinded destinations - körleştirilmiş hedefler)

i2cp.leaseSetType=5

# Meta LS2 (birden fazla hedef)

i2cp.leaseSetType=7

```

**Additional Options:**

```properties
# ECIES (Eliptik Eğri Entegre Şifreleme Şeması) için statik anahtar (isteğe bağlı, belirtilmezse otomatik olarak oluşturulur)

# Base64 ile kodlanmış 32 baytlık X25519 (elliptik eğri Diffie-Hellman anahtar değişimi) açık anahtar

i2cp.leaseSetPrivateKey=<base64-encoded-key>

# İmza türü (LeaseSet için)

i2cp.leaseSetSigningPrivateKey=<base64-encoded-key> i2cp.leaseSetSigningType=7  # Ed25519

```

### Java I2P Configuration

**router.config:**

```properties
# Router'dan router'a ECIES (Eliptik Eğri Entegre Şifreleme Şeması)

i2p.router.useECIES=true

```

**Build Properties:**

```java
// For I2CP clients (Java) Properties props = new Properties(); props.setProperty("i2cp.leaseSetEncType", "4"); props.setProperty("i2cp.leaseSetType", "3");

I2PSession session = i2pClient.createSession(props);

```

### i2pd Configuration

**i2pd.conf:**

```ini
[sınırlar]

# ECIES (Eliptik Eğri Entegre Şifreleme Şeması) oturumlarının bellek sınırı

ecies.memory = 128M

[ecies]

# ECIES'i etkinleştir (Eliptik Eğri Entegre Şifreleme Şeması)

enabled = true

# Yalnızca ECIES (Eliptik Eğri Bütünleşik Şifreleme Düzeni) veya çift anahtarlı

compatibility = true  # true = çift anahtarlı, false = yalnızca ECIES

```

**Tunnels Configuration:**

```ini
[my-service] type = http host = 127.0.0.1 port = 8080 keys = my-service-keys.dat

# Yalnızca ECIES (Eliptik Eğri Tümleşik Şifreleme Şeması)

ecies = true

```

### Compatibility Matrix

**Router Version Support:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">ECIES Support</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">LS2 Support</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Dual-Key</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">&lt; 0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">❌ No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">❌ No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">N/A</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy only</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.38-0.9.45</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">❌ No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">N/A</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LS2 only</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.46-0.9.50</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Initial ECIES</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.5.0+</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.0.0+</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
  </tbody>
</table>

**Destination Compatibility:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Destination Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Can Connect To</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-only</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-only, Dual-key</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Requires 0.9.46+ routers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Dual-key</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Maximum compatibility</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal-only</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal-only, Dual-key</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy</td>
    </tr>
  </tbody>
</table>

**FloodFill Requirements:**

- **ECIES-only destinations**: Require majority of floodfills on 0.9.46+ for encrypted lookups
- **Dual-key destinations**: Work with any floodfill version
- **Current status**: Near 100% floodfill adoption as of 2025

### Migration Guide

**Migrating from ElGamal to ECIES:**

**Step 1: Enable Dual-Key Mode**

```properties
# ElGamal'i koruyarak ECIES'i ekleyin

i2cp.leaseSetEncType=4,0

```

**Step 2: Monitor Connections**

```bash
# Bağlantı türlerini kontrol edin

i2prouter.exe status

# veya

http://127.0.0.1:7657/peers

```

**Step 3: Switch to ECIES-Only (after testing)**

```properties
# ElGamal'ı kaldır

i2cp.leaseSetEncType=4

```

**Step 4: Restart Application**

```bash
# I2P router'ı veya uygulamayı yeniden başlatın

systemctl restart i2p

# veya

i2prouter.exe restart

```

**Rollback Plan:**

```properties
# Sorunlar olursa yalnızca ElGamal'a geri dönün

i2cp.leaseSetEncType=0

```

### Performance Tuning

**Session Limits:**

```properties
# Maksimum gelen oturum sayısı

i2p.router.maxInboundSessions=1000

# En fazla giden oturum sayısı

i2p.router.maxOutboundSessions=1000

# Oturum zaman aşımı (saniye)

i2p.router.sessionTimeout=600

```

**Memory Limits:**

```properties
# Etiket depolama sınırı (KB)

i2p.ecies.maxTagMemory=10240  # 10 MB

# İleri bakış penceresi

i2p.ecies.tagLookAhead=160 i2p.ecies.tagLookAheadMin=32

```

**Ratchet Policy:**

```properties
# ratchet (anahtar yenileme mekanizması) öncesi mesajlar

i2p.ecies.ratchetThreshold=4096

# Ratchet (kademeli anahtar yenileme mekanizması) başlamadan önceki süre (saniye)

i2p.ecies.ratchetTimeout=600  # 10 dakika

```

### Monitoring and Debugging

**Logging:**

```properties
# ECIES (Eliptik Eğri Entegre Şifreleme Şeması) hata ayıklama günlüğünü etkinleştir

logger.i2p.router.transport.ecies=DEBUG

```

**Metrics:**

Monitor these metrics:

1. **NS Success Rate**: Percentage of NS messages receiving NSR
2. **Session Establishment Time**: Time from NS to first ES
3. **Tag Storage Usage**: Current memory usage for tags
4. **Ratchet Frequency**: How often sessions ratchet
5. **Session Lifetime**: Average session duration

**Common Issues:**

1. **NS Timeout**: No NSR received
   - Check destination is online
   - Check floodfill availability
   - Verify LeaseSet published correctly

2. **High Memory Usage**: Too many tags stored
   - Reduce look-ahead window
   - Decrease session timeout
   - Implement aggressive expiration

3. **Frequent Ratchets**: Sessions ratcheting too often
   - Increase ratchet threshold
   - Check for retransmissions

4. **Session Failures**: ES messages failing to decrypt
   - Verify tag synchronization
   - Check for replay attacks
   - Validate nonce construction

---

## References

### Specifications

1. **ECIES Proposal**: [Proposal 144](/proposals/144-ecies-x25519-aead-ratchet/)
2. **I2NP**: [I2NP Specification](/docs/specs/i2np/)
3. **Common Structures**: [Common Structures Specification](/docs/specs/common-structures/)
4. **NTCP2**: [NTCP2 Specification](/docs/specs/ntcp2/)
5. **SSU2**: [SSU2 Specification](/docs/specs/ssu2/)
6. **I2CP**: [I2CP Specification](/docs/specs/i2cp/)
7. **ElGamal/AES+SessionTags**: [ElGamal/AES Specification](/docs/legacy/elgamal-aes/)

### Cryptographic Standards

1. **Noise Protocol Framework**: [Noise Specification](https://noiseprotocol.org/noise.html) (Revision 34, 2018-07-11)
2. **Signal Double Ratchet**: [Signal Specification](https://signal.org/docs/specifications/doubleratchet/)
3. **RFC 7748**: [Elliptic Curves for Security (X25519)](https://tools.ietf.org/html/rfc7748)
4. **RFC 7539**: [ChaCha20 and Poly1305 for IETF Protocols](https://tools.ietf.org/html/rfc7539)
5. **RFC 5869**: [HKDF (HMAC-based Key Derivation Function)](https://tools.ietf.org/html/rfc5869)
6. **RFC 2104**: [HMAC: Keyed-Hashing for Message Authentication](https://tools.ietf.org/html/rfc2104)
7. **Elligator2**: [Elligator Paper](https://elligator.cr.yp.to/elligator-20130828.pdf)

### Implementation Resources

1. **Java I2P**: [i2p.i2p Repository](https://github.com/i2p/i2p.i2p)
2. **i2pd (C++)**: [i2pd Repository](https://github.com/PurpleI2P/i2pd)
3. **OBFS4 (Elligator2)**: [obfs4proxy Repository](https://gitlab.com/yawning/obfs4)

### Additional Information

1. **I2P Website**: [/](/)
2. **I2P Forum**: [https://i2pforum.net](https://i2pforum.net)
3. **I2P Wiki**: [https://wiki.i2p-projekt.de](https://wiki.i2p-projekt.de)

---

## Appendix A: KDF Summary

**All KDF Operations in ECIES:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Input</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Info String</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Output</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NS Initial ChainKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">protocol_name</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">(none - SHA256)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">h, chainKey</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NS Static Key Section</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, es_shared</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">""</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, k</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NS Payload Section (bound)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, ss_shared</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">""</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, k</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR Tagset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"SessionReplyTags"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">tagsetKey</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR ee DH</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, ee_shared</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">""</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR se DH</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, se_shared</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">""</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, k</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR Split</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">""</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">k_ab, k_ba</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR Payload</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">k_ba</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"AttachPayloadKDF"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">k_nsr</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DH Initialize</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">rootKey, k</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"KDFDHRatchetStep"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">nextRootKey, chainKey</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Tag and Key Chain Keys</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"TagAndKeyGenKeys"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">sessTag_ck, symmKey_ck</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Session Tag Init</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">sessTag_ck</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"STInitialization"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, CONSTANT</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Session Tag Gen</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, CONSTANT</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"SessionTagKeyGen"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, tag</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Symmetric Key Gen</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"SymmetricRatchet"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DH Ratchet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">sharedSecret</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"XDHRatchetTagSet"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">tagsetKey</td>
    </tr>
  </tbody>
</table>

---

## Appendix B: Message Size Calculator

**Calculate message sizes for capacity planning:**

```python
def calculate_ns_size(payload_size, bound=True):

    """Calculate New Session message size"""
    ephemeral_key = 32
    static_section = 32 + 16  # encrypted + MAC
    payload_encrypted = payload_size + 16  # + MAC
    
    return ephemeral_key + static_section + payload_encrypted

def calculate_nsr_size(payload_size):

    """Calculate New Session Reply message size"""
    tag = 8
    ephemeral_key = 32
    key_section_mac = 16
    payload_encrypted = payload_size + 16  # + MAC
    
    return tag + ephemeral_key + key_section_mac + payload_encrypted

def calculate_es_size(payload_size):

    """Calculate Existing Session message size"""
    tag = 8
    payload_encrypted = payload_size + 16  # + MAC
    
    return tag + payload_encrypted

# Örnekler

print("NS (bound, 1KB yük):", calculate_ns_size(1024, bound=True), "bayt")

# Çıktı: 1120 bayt

print("NSR (1KB veri yükü):", calculate_nsr_size(1024), "bayt")

# Çıktı: 1096 bayt

print("ES (1KB veri yükü):", calculate_es_size(1024), "bayt")

# Çıktı: 1048 bayt

```

---

## Appendix C: Glossary

**AEAD**: Authenticated Encryption with Associated Data - encryption mode that provides both confidentiality and authenticity

**Authentication Level**: Noise protocol security property indicating strength of sender identity verification

**Binding**: Association of a session with a specific far-end destination

**ChaCha20**: Stream cipher designed by Daniel J. Bernstein

**ChainKey**: Cryptographic key used in HKDF chains to derive subsequent keys

**Confidentiality Level**: Noise protocol security property indicating strength of forward secrecy

**DH**: Diffie-Hellman key agreement protocol

**Elligator2**: Encoding technique to make elliptic curve points indistinguishable from random

**Ephemeral Key**: Short-lived key used only for a single handshake

**ES**: Existing Session message (used after handshake completion)

**Forward Secrecy**: Property ensuring past communications remain secure if keys are compromised

**Garlic Clove**: I2NP message container for end-to-end delivery

**HKDF**: HMAC-based Key Derivation Function

**IK Pattern**: Noise handshake pattern where initiator sends static key immediately

**KCI**: Key Compromise Impersonation attack

**KDF**: Key Derivation Function - cryptographic function for generating keys from other keys

**LeaseSet**: I2P structure containing a destination's public keys and tunnel information

**LS2**: LeaseSet version 2 with encryption type support

**MAC**: Message Authentication Code - cryptographic checksum proving authenticity

**MixHash**: Noise protocol function for maintaining running hash transcript

**NS**: New Session message (initiates new session)

**NSR**: New Session Reply message (response to NS)

**Nonce**: Number used once - ensures unique encryption even with same key

**Pairing**: Linking an inbound session with an outbound session for bidirectional communication

**Poly1305**: Message authentication code designed by Daniel J. Bernstein

**Ratchet**: Cryptographic mechanism for deriving sequential keys

**Session Tag**: 8-byte one-time identifier for existing session messages

**Static Key**: Long-term key associated with a destination's identity

**Tag Set**: Collection of session tags derived from a common root

**X25519**: Elliptic curve Diffie-Hellman key agreement using Curve25519

---