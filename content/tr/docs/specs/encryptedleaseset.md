---
title: "Şifrelenmiş LeaseSet"
description: "Özel Destinations (I2P hedefleri) için erişim denetimli LeaseSet biçimi"
slug: "encryptedleaseset"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Genel Bakış

Bu belge, şifreli LeaseSet2 (LS2) için körleme, şifreleme ve şifre çözmeyi tanımlar. Şifreli LeaseSet'ler, I2P ağ veritabanında gizli servis bilgilerinin erişim denetimli olarak yayımlanmasına olanak tanır.

**Temel Özellikler:** - İleriye dönük gizlilik için günlük anahtar rotasyonu - İki kademeli istemci yetkilendirmesi (DH tabanlı ve PSK tabanlı) - AES donanımı olmayan cihazlarda performans için ChaCha20 şifrelemesi - Anahtar körleme ile Red25519 imzaları - Gizliliği koruyan istemci üyeliği

**İlgili Dokümantasyon:** - [Ortak Yapılar Spesifikasyonu](/docs/specs/common-structures/) - Şifrelenmiş LeaseSet yapısı - [Öneri 123: Yeni netDB Girdileri](/proposals/123-new-netdb-entries/) - Şifrelenmiş LeaseSet'ler hakkında arka plan bilgisi - [Ağ Veritabanı Dokümantasyonu](/docs/specs/common-structures/) - NetDB kullanımı

---

## Sürüm Geçmişi ve Uygulama Durumu

### Protokol Geliştirme Zaman Çizelgesi

**Sürüm Numaralandırma Hakkında Önemli Not:**   I2P iki ayrı sürüm numaralandırma şeması kullanır: - **API/Router Sürümü:** 0.9.x serisi (teknik özelliklerde kullanılır) - **Ürün Yayın Sürümü:** 2.x.x serisi (genel kullanıma sunulan sürümler için kullanılır)

Teknik özellikler API sürümlerine (örn. 0.9.41) atıfta bulunurken, son kullanıcılar ürün sürümlerini (örn. 2.10.0) görür.

### Uygulama Kilometre Taşları

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Release Date</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Features</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.38</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">January 2019</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Floodfill support for standard LS2, offline keys</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.39</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">March 2019</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Full encrypted LS2 support, Red25519 (sig type&nbsp;11)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.40</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">May 2019</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Per-client authorization, encrypted LS2 with offline keys, B32 support</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.41</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">June 2019</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Protocol finalized as stable</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>2.10.0</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">September 2025</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Latest Java implementation (API version 0.9.61)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>i2pd 2.58.0</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">September 2025</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Full C++ implementation compatibility</td></tr>
  </tbody>
</table>
### Mevcut Durum

- ✅ **Protokol Durumu:** Haziran 2019'dan bu yana kararlı ve değişmedi
- ✅ **Java I2P:** 0.9.40+ sürümlerinde eksiksiz olarak uygulanmıştır
- ✅ **i2pd (C++):** 2.58.0+ sürümlerinde eksiksiz olarak uygulanmıştır
- ✅ **Birlikte Çalışabilirlik:** Uygulamalar arasında tamdır
- ✅ **Ağ Dağıtımı:** 6+ yıllık operasyonel deneyimle üretim kullanımına hazır

---

## Kriptografik Tanımlar

### Notasyon ve Sözleşimler

- `||` birleştirmeyi ifade eder
- `mod L` Ed25519 mertebesine göre modüler indirgemeyi ifade eder
- Aksi belirtilmedikçe tüm bayt dizileri ağ bayt sıralamasındadır (big-endian, en anlamlı bayt önce)
- Little-endian değerler açıkça belirtilir (en az anlamlı bayt önce)

### CSRNG(n)

**Kriptografik olarak güvenli rastgele sayı üreteci**

Anahtar materyali üretimine uygun, kriptografik olarak güvenli rastgele veriden `n` bayt üretir.

**Güvenlik Gereksinimleri:** - Kriptografik olarak güvenli olmalı (anahtar üretimi için uygun) - Ağda bitişik bayt dizileri açığa çıktığında güvenli olmalı - Gerçekleştirimler, potansiyel olarak güvenilmez kaynaklardan gelen çıktıyı karmalamalıdır

**Kaynaklar:** - [PRNG Güvenlik Hususları](http://projectbullrun.org/dual-ec/ext-rand.html) - [Tor Geliştirici Tartışması](https://lists.torproject.org/pipermail/tor-dev/2015-November/009954.html)

### H(p, d)

**Kişiselleştirmeli SHA-256 Karma**

Domain-separated (etki alanı ayrımlı) özet fonksiyonu, şunları alır:
- `p`: Kişiselleştirme dizesi (etki alanı ayrımı sağlar)
- `d`: Özetlenecek veri

**Uygulama:**

```
H(p, d) := SHA-256(p || d)
```
**Kullanım:** SHA-256'nin farklı protokol kullanımları arasında çakışma saldırılarını önlemek için kriptografik alan ayrımı sağlar.

### Akış: ChaCha20

**Akış şifresi: RFC 7539 Bölüm 2.4'te belirtildiği gibi ChaCha20**

**Parametreler:** - `S_KEY_LEN = 32` (256 bitlik anahtar) - `S_IV_LEN = 12` (96 bitlik tek kullanımlık sayı) - Başlangıç sayacı: `1` (RFC 7539 0 veya 1'e izin verir; AEAD bağlamlarında 1 önerilir)

**ENCRYPT(k, iv, plaintext)**

Açık metni şunları kullanarak şifreler: - `k`: 32 baytlık şifreleme anahtarı - `iv`: 12 baytlık nonce (tek kullanımlık sayı; HER anahtar için benzersiz OLMALIDIR) - Açık metinle aynı boyutta şifreli metin döndürür

**Güvenlik Özelliği:** Anahtar gizliyse, tüm şifreli metin rastgele veriden ayırt edilemez olmalıdır.

**Şifre Çöz(k, iv, ciphertext)**

Şifreli metni şunları kullanarak çözer: - `k`: 32 baytlık şifreleme anahtarı - `iv`: 12 baytlık nonce (tek kullanımlık değer) - Açık metni döndürür

**Tasarım Gerekçesi:** ChaCha20 (akış şifreleme algoritması), AES'e (Gelişmiş Şifreleme Standardı) göre tercih edildi çünkü: - Donanım hızlandırması olmayan cihazlarda AES'ten 2.5-3 kat daha hızlı - Sabit zamanlı bir uygulamayı gerçekleştirmek daha kolay - AES-NI (AES için donanım hızlandırma talimatları) mevcut olduğunda karşılaştırılabilir güvenlik ve hız

**Referanslar:** - [RFC 7539](https://datatracker.ietf.org/doc/html/rfc7539) - IETF Protokolleri için ChaCha20 ve Poly1305

### İmza: Red25519 (imza türü)

**İmza Şeması: Red25519 (SigType 11) Anahtar Körleme ile**

Red25519, Ed25519 eğrisi üzerinde Ed25519 imzalarına dayanır; özetleme için SHA-512 kullanır ve ZCash RedDSA'da belirtildiği şekilde key blinding (körleme) desteği sağlar.

**İşlevler:**

#### DERIVE_PUBLIC(privkey)

Verilen özel anahtara karşılık gelen genel anahtarı döndürür. - Standart Ed25519 taban noktasıyla skaler çarpımı kullanır

#### SIGN(privkey, m)

Mesaj `m` üzerinden, `privkey` özel anahtarı kullanılarak oluşturulmuş bir imza döndürür.

**Red25519 imzalama işleminin Ed25519'e göre farkları:** 1. **Rastgele Nonce (tek seferlik değer):** 80 bayt ek rastgele veri kullanır

   ```
   T = CSRNG(80)  // 80 random bytes
   r = H*(T || publickey || message)
   ```
Bu, aynı mesaj ve anahtar için bile her Red25519 (bir eliptik eğri imza şeması) imzasını benzersiz kılar.

2. **Özel Anahtar Üretimi:** Red25519 özel anahtarları rastgele sayılardan üretilir ve `mod L` alınarak indirgenir; Ed25519'un bit-clamping (bit kısma) yaklaşımı kullanılmaz.

#### VERIFY(pubkey, m, sig)

İmza `sig`'i açık anahtar `pubkey` ve mesaj `m` ile doğrular. - İmza geçerliyse `true`, aksi halde `false` döndürür - Doğrulama Ed25519 ile aynıdır

**Anahtar Körleme İşlemleri:**

#### GENERATE_ALPHA(data, secret)

Anahtar körleştirme için alpha üretir. - `data`: Genellikle imzalama açık anahtarını ve imza türlerini içerir - `secret`: İsteğe bağlı ek giz (kullanılmıyorsa sıfır uzunluklu) - Sonuç, Ed25519 özel anahtarlarıyla aynı dağılıma sahiptir (mod L indirgemesinden sonra)

#### BLIND_PRIVKEY(privkey, alpha)

Gizli `alpha` kullanarak özel bir anahtarı körleştirir. - Uygulama: `blinded_privkey = (privkey + alpha) mod L` - Alan üzerinde skaler aritmetik kullanır

#### BLIND_PUBKEY(pubkey, alpha)

Bir genel anahtarı gizli `alpha` kullanarak körler. - Uygulama: `blinded_pubkey = pubkey + DERIVE_PUBLIC(alpha)` - Eğri üzerinde grup elemanı (nokta) toplamını kullanır

**Kritik Özellik:**

```
BLIND_PUBKEY(pubkey, alpha) == DERIVE_PUBLIC(BLIND_PRIVKEY(privkey, alpha))
```
**Güvenlik Hususları:**

ZCash Protokol Şartnamesi Bölüm 5.4.6.1'den: Güvenlik açısından, alpha'nın körleştirilmemiş özel anahtarlarla aynı dağılıma sahip olması gerekir. Bu, "yeniden rastgeleleştirilmiş bir açık anahtar ile o anahtar altında üretilmiş imza(ların) birleşiminin, yeniden rastgeleleştirildiği anahtarı ortaya çıkarmamasını" sağlar.

**Desteklenen İmza Türleri:** - **Tür 7 (Ed25519):** Mevcut destinasyonlar için desteklenir (geri uyumluluk) - **Tür 11 (Red25519):** Şifreleme kullanan yeni destinasyonlar için önerilir - **Blinded keys (körleştirilmiş anahtarlar):** Her zaman Tür 11 (Red25519) kullanın

**Referanslar:** - [ZCash Protokol Spesifikasyonu](https://zips.z.cash/protocol/protocol.pdf) - Bölüm 5.4.6 RedDSA - [I2P Red25519 Spesifikasyonu](/docs/specs/red25519-signature-scheme/)

### DH (Diffie-Hellman): X25519

**Eliptik Eğri Diffie-Hellman: X25519**

Curve25519 tabanlı bir açık anahtar anlaşması sistemi.

**Parametreler:** - Özel anahtarlar: 32 bayt - Açık anahtarlar: 32 bayt - Paylaşılan sır çıktısı: 32 bayt

**İşlevler:**

#### GENERATE_PRIVATE()

CSRNG (kriptografik olarak güvenli rastgele sayı üreteci) kullanarak yeni bir 32 baytlık özel anahtar oluşturur.

#### DERIVE_PUBLIC(privkey)

Verilen özel anahtardan 32 baytlık genel anahtarı türetir. - Curve25519 üzerinde skaler çarpma kullanır

#### DH(privkey, pubkey)

Diffie-Hellman anahtar değişimini gerçekleştirir. - `privkey`: Yerel 32 baytlık özel anahtar - `pubkey`: Uzak 32 baytlık açık anahtar - Döndürür: 32 baytlık paylaşılan sır

**Güvenlik Özellikleri:** - Curve25519 üzerinde Hesaplamalı Diffie-Hellman varsayımı - Geçici anahtarlar kullanıldığında ileri gizlilik - Zamanlama saldırılarını önlemek için sabit zamanlı gerçekleştirim gereklidir

**Kaynaklar:** - [RFC 7748](https://datatracker.ietf.org/doc/html/rfc7748) - Güvenlik için Eliptik Eğriler

### HKDF (HMAC tabanlı anahtar türetme fonksiyonu)

**HMAC tabanlı Anahtar Türetme Fonksiyonu**

Girdi anahtar malzemesinden anahtar malzemesini ayıklar ve genişletir.

**Parametreler:** - `salt`: en fazla 32 bayt (genellikle SHA-256 için 32 bayt) - `ikm`: girdi anahtar materyali (herhangi bir uzunlukta olabilir, iyi entropiye sahip olmalı) - `info`: bağlama özgü bilgi (domain separation — alan ayrımı) - `n`: çıktının bayt cinsinden uzunluğu

**Uygulama:**

RFC 5869'da belirtildiği şekilde HKDF'yi şu ayarlarla kullanır: - **Hash Fonksiyonu:** SHA-256 - **HMAC:** RFC 2104'te belirtildiği şekilde - **Salt Uzunluğu:** En fazla 32 bayt (SHA-256 için HashLen)

**Kullanım Deseni:**

```
keys = HKDF(salt, ikm, info, n)
```
**Etki Alanı Ayrımı:** `info` parametresi, protokolde HKDF'nin (HMAC tabanlı Anahtar Türetme Fonksiyonu) farklı kullanımları arasında kriptografik etki alanı ayrımı sağlar.

**Doğrulanmış Bilgi Değerleri:** - `"ELS2_L1K"` - Katman 1 (dış) şifreleme - `"ELS2_L2K"` - Katman 2 (iç) şifreleme - `"ELS2_XCA"` - DH istemci yetkilendirmesi - `"ELS2PSKA"` - PSK istemci yetkilendirmesi - `"i2pblinding1"` - Alfa oluşturma

**Referanslar:** - [RFC 5869](https://datatracker.ietf.org/doc/html/rfc5869) - HKDF Şartnamesi (HMAC tabanlı çıkarma ve genişletme anahtar türetme işlevi) - [RFC 2104](https://datatracker.ietf.org/doc/html/rfc2104) - HMAC Şartnamesi (karma tabanlı mesaj doğrulama kodu)

---

## Biçim Spesifikasyonu

Şifrelenmiş LS2 (ikinci nesil LeaseSet formatı) üç iç içe geçmiş katmandan oluşur:

1. **Katman 0 (Dış):** Depolama ve geri alma için düz metin bilgileri
2. **Katman 1 (Orta):** İstemci kimlik doğrulama verileri (şifrelenmiş)
3. **Katman 2 (İç):** Asıl LeaseSet2 verileri (şifrelenmiş)

**Genel Yapı:**

```
Layer 0 data + Enc(layer 1 data + Enc(layer 2 data)) + Signature
```
**Önemli:** Şifreli LS2, körlenmiş anahtarlar kullanır. Destination (Hedef) başlıkta yer almaz. DHT (Dağıtık karma tablosu) depolama konumu `SHA-256(sig type || blinded public key)` olup her gün yenilenir.

### Katman 0 (Dış) - Açık metin

Katman 0 standart LS2 başlığını KULLANMAZ. Blinded keys (körleştirilmiş anahtarlar) için optimize edilmiş özel bir biçime sahiptir.

**Yapı:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Type</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Not in header, from DatabaseStore message field</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded Public Key Sig Type</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, always <code>0x000b</code> (Red25519 type 11)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded Public Key</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Red25519 blinded public key</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Published Timestamp</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, seconds since epoch (rolls over in 2106)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Expires</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, offset from published in seconds (max 65,535 &asymp; 18.2 hours)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Flags</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Bit flags (see below)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">[Optional] Transient Key Data</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Present if flag bit&nbsp;0 is set</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">lenOuterCiphertext</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, length of outer ciphertext</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">outerCiphertext</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">lenOuterCiphertext</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted Layer&nbsp;1 data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Red25519 signature over all preceding data</td></tr>
  </tbody>
</table>
**Bayraklar Alanı (2 bayt, bitler 15-0):** - **Bit 0:** Çevrimdışı anahtar göstergesi   - `0` = Çevrimdışı anahtar yok   - `1` = Çevrimdışı anahtarlar mevcut (geçici anahtar verisi ardından gelir) - **Bitler 1-15:** Ayrılmış, gelecekteki uyumluluk için 0 olmalıdır

**Geçici Anahtar Verileri (bayrak biti 0 = 1 ise mevcut):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Expires Timestamp</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, seconds since epoch</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Transient Sig Type</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, signature type</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Transient Signing Public Key</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Length implied by signature type</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signed by blinded public key; covers expires timestamp, transient sig type, and transient public key</td></tr>
  </tbody>
</table>
**İmza Doğrulama:** - **Çevrimdışı anahtarlar olmadan:** Körlenmiş açık anahtarla doğrulayın - **Çevrimdışı anahtarlarla:** Geçici açık anahtarla doğrulayın

İmza, Type'tan outerCiphertext'e kadar (dahil) tüm verileri kapsar.

### Katman 1 (Orta) - İstemci Yetkilendirme

**Şifre çözme:** Bkz. [Katman 1 Şifreleme](#layer-1-encryption) bölümü.

**Yapı:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Flags</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Authorization flags (see below)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">[Optional] Auth Data</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Present based on flags</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">innerCiphertext</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted Layer&nbsp;2 data (remainder)</td></tr>
  </tbody>
</table>
**Bayraklar Alanı (1 bayt, bitler 7-0):** - **Bit 0:** Yetkilendirme modu   - `0` = İstemci başına yetkilendirme yok (herkes)   - `1` = İstemci başına yetkilendirme (kimlik doğrulama bölümü ardından gelir) - **Bitler 3-1:** Kimlik doğrulama şeması (yalnızca bit 0 = 1 ise)   - `000` = DH istemci kimlik doğrulaması   - `001` = PSK istemci kimlik doğrulaması   - Diğerleri ayrılmış - **Bitler 7-4:** Kullanılmıyor, 0 olmalıdır

**DH İstemci Yetkilendirme Verileri (bayraklar = 0x01, bitler 3-1 = 000):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ephemeralPublicKey</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Server's ephemeral X25519 public key</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">clients</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, number of client entries</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">authClient[]</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">40 bytes each</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Array of client authorization entries</td></tr>
  </tbody>
</table>
**authClient Girdisi (40 bayt):** - `clientID_i`: 8 bayt - `clientCookie_i`: 32 bayt (şifrelenmiş authCookie)

**PSK İstemci Yetkilendirme Verileri (bayraklar = 0x03, 3-1 bitleri = 001):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">authSalt</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Salt for PSK key derivation</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">clients</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, number of client entries</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">authClient[]</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">40 bytes each</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Array of client authorization entries</td></tr>
  </tbody>
</table>
**authClient Girdisi (40 bayt):** - `clientID_i`: 8 bayt - `clientCookie_i`: 32 bayt (şifrelenmiş authCookie)

### Katman 2 (İç) - LeaseSet Verileri

**Şifre çözme:** Bkz. [Katman 2 Şifreleme](#layer-2-encryption) bölümü.

**Yapı:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Type</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>3</code> (LS2) or <code>7</code> (Meta LS2)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Complete LeaseSet2 or MetaLeaseSet2</td></tr>
  </tbody>
</table>
İç katman, aşağıdakileri içeren tam LeaseSet2 yapısını barındırır: - LS2 başlığı - Lease (kiralama kaydı) bilgisi - LS2 imzası

**Doğrulama Gereksinimleri:** Şifre çözme işleminden sonra, gerçeklemeler şunları doğrulamalıdır: 1. İç zaman damgasının dışta yayımlanan zaman damgasıyla eşleştiğini 2. İç sona erme zamanının dış sona erme zamanıyla eşleştiğini 3. LS2 imzasının geçerli olduğunu 4. Lease (kiralama kaydı) verisinin iyi biçimlendirilmiş olduğunu

**Referanslar:** - [Ortak Yapılar Spesifikasyonu](/docs/specs/common-structures/) - LeaseSet2 biçim ayrıntıları

---

## Körleme Anahtarı Türetimi

### Genel Bakış

I2P, Ed25519 ve ZCash RedDSA tabanlı bir additive key blinding (toplamsal anahtar körleme) şeması kullanır. İleri gizlilik için körlenmiş anahtarlar günlük olarak (UTC gece yarısında) yenilenir.

**Tasarım Gerekçesi:**

I2P, Tor'un rend-spec-v3.txt dosyasındaki Ek A.2 yaklaşımını KULLANMAMAYI açıkça seçti. Spesifikasyona göre:

> "Benzer tasarım amaçlarına sahip olan Tor'un rend-spec-v3.txt belgesindeki Ek A.2'yi kullanmıyoruz; çünkü oradaki körlenmiş açık anahtarlar asal mertebeli altgrubun dışında olabilir ve bunun güvenlik sonuçları bilinmemektedir."

I2P'nin additive blinding (toplamsal körleme) yöntemi, körlenmiş anahtarların Ed25519 eğrisinin asal dereceli alt grubunda kalmasını garanti eder.

### Matematiksel Tanımlar

**Ed25519 Parametreleri:** - `B`: Ed25519 taban noktası (üreteç) = `2^255 - 19` - `L`: Ed25519 mertebesi = `2^252 + 27742317777372353535851937790883648493`

**Temel Değişkenler:** - `A`: Körleştirilmemiş 32 baytlık imzalama açık anahtarı (Destination (I2P adresi) içinde) - `a`: Körleştirilmemiş 32 baytlık imzalama özel anahtarı - `A'`: Körleştirilmiş 32 baytlık imzalama açık anahtarı (şifrelenmiş LeaseSet içinde kullanılır) - `a'`: Körleştirilmiş 32 baytlık imzalama özel anahtarı - `alpha`: 32 baytlık körleştirme faktörü (gizli)

**Yardımcı İşlevler:**

#### LEOS2IP(x)

"Küçük endian oktet dizisini tamsayıya dönüştürme"

little-endian (küçük uç önde bayt sıralaması) biçimindeki bir bayt dizisini tamsayı gösterimine dönüştürür.

#### H*(x)

"Özetleme ve İndirgeme"

```
H*(x) = (LEOS2IP(SHA512(x))) mod L
```
Ed25519 anahtar üretimindeki işlemin aynısı.

### Alfa Kuşağı

**Günlük Rotasyon:** Her gün UTC gece yarısında (00:00:00 UTC) yeni bir alpha (alfa parametresi) ve blinded keys (körleştirilmiş anahtarlar) oluşturulması ZORUNLUDUR.

**GENERATE_ALPHA(destination, date, secret) Algoritması:**

```python
# Input parameters
A = destination's signing public key (32 bytes)
stA = signature type of A (2 bytes, big endian)
     # 0x0007 for Ed25519 or 0x000b for Red25519
stA' = signature type of blinded key A' (2 bytes, big endian) 
     # Always 0x000b (Red25519)
datestring = "YYYYMMDD" (8 bytes ASCII from current UTC date)
secret = optional UTF-8 encoded string (zero-length if not used)

# Computation
keydata = A || stA || stA'  # 36 bytes total
seed = HKDF(
    salt=H("I2PGenerateAlpha", keydata),
    ikm=datestring || secret,
    info="i2pblinding1",
    n=64
)

# Treat seed as 64-byte little-endian integer and reduce
alpha = seed mod L
```
**Doğrulanan Parametreler:** - Salt kişiselleştirmesi: `"I2PGenerateAlpha"` - HKDF bilgisi: `"i2pblinding1"` - Çıktı: indirgeme öncesi 64 bayt - Alpha dağılımı: `mod L` sonrasında Ed25519 özel anahtarlarıyla özdeş dağılımda

### Özel Anahtar Körleştirme

**BLIND_PRIVKEY(a, alpha) Algoritması:**

Şifrelenmiş LeaseSet'i yayımlayan hedef sahibi için:

```python
# For Ed25519 private key (type 7)
if sigtype == 7:
    seed = destination's signing private key (32 bytes)
    a = left_half(SHA512(seed))  # 32 bytes
    a = clamp(a)  # Ed25519 clamping
    
# For Red25519 private key (type 11)
elif sigtype == 11:
    a = destination's signing private key (32 bytes)
    # No clamping for Red25519

# Additive blinding using scalar arithmetic
blinded_privkey = a' = (a + alpha) mod L

# Derive blinded public key
blinded_pubkey = A' = DERIVE_PUBLIC(a')
```
**Kritik:** `mod L` indirgemesi, özel ve açık anahtarlar arasındaki doğru cebirsel ilişkiyi sürdürmek için hayati önemdedir.

### Açık Anahtar Körleme

**BLIND_PUBKEY(A, alpha) Algoritması:**

Şifrelenmiş LeaseSet'i alan ve doğrulayan istemciler için:

```python
alpha = GENERATE_ALPHA(destination, date, secret)
A = destination's signing public key (32 bytes)

# Additive blinding using group elements (curve points)
blinded_pubkey = A' = A + DERIVE_PUBLIC(alpha)
```
**Matematiksel Eşdeğerlik:**

Her iki yöntem de aynı sonuçları verir:

```
BLIND_PUBKEY(A, alpha) == DERIVE_PUBLIC(BLIND_PRIVKEY(a, alpha))
```
Bunun nedeni:

```
A' = A + [alpha]B
   = [a]B + [alpha]B
   = [a + alpha]B  (group operation)
   = DERIVE_PUBLIC(a + alpha mod L)
```
### Körleştirilmiş Anahtarlarla İmzalama

**Körleştirilmemiş LeaseSet İmzalama:**

Körlemesi kaldırılmış LeaseSet (doğrulanmış istemcilere doğrudan gönderilen) şu şekilde imzalanır: - Standart Ed25519 (tip 7) veya Red25519 (tip 11) imzası - Körlemesi kaldırılmış imzalama özel anahtarı - Körlemesi kaldırılmış açık anahtarla doğrulanır

**Çevrimdışı Anahtarlarla:** - körleştirilmemiş geçici özel anahtar ile imzalanır - körleştirilmemiş geçici açık anahtar ile doğrulanır - Her ikisi de tür 7 veya 11 olmalıdır

**Şifreli LeaseSet İmzalama:**

Şifrelenmiş LeaseSet'in dış kısmı, körleştirilmiş anahtarlarla birlikte Red25519 imzalarını kullanır.

**Red25519 İmza Algoritması:**

```python
# Generate per-signature random nonce
T = CSRNG(80)  # 80 random bytes

# Calculate r (differs from Ed25519)
r = H*(T || blinded_pubkey || message)

# Rest is same as Ed25519
R = [r]B
S = (r + H(R || A' || message) * a') mod L
signature = R || S  # 64 bytes total
```
**Ed25519'dan Temel Farklar:** 1. 80 bayt rastgele veri `T` kullanır (özel anahtarın karması değil) 2. Genel anahtar değerini doğrudan kullanır (özel anahtarın karması değil) 3. Aynı mesaj ve anahtar için bile her imza benzersizdir

**Doğrulama:**

Ed25519 ile aynı:

```python
# Parse signature
R = signature[0:32]
S = signature[32:64]

# Verify equation: [S]B = R + [H(R || A' || message)]A'
return [S]B == R + [H(R || A' || message)]A'
```
### Güvenlik Hususları

**Alfa Dağıtımı:**

Güvenlik açısından, alpha körleştirilmemiş özel anahtarlarla özdeş dağılıma sahip olmalıdır. Ed25519 (tip 7)’yi Red25519 (tip 11)’ye körleştirirken, dağılımlar biraz farklılık gösterir.

**Öneri:** ZCash gereksinimlerini karşılamak için hem körleştirilmemiş hem de körleştirilmiş anahtarlar için Red25519 (type 11) kullanın: "yeniden rastgeleleştirilmiş bir açık anahtar ile o anahtar altında oluşturulan imza(lar)ın birleşimi, yeniden rastgeleleştirildiği anahtarı açığa çıkarmaz."

**Tip 7 Desteği:** Mevcut destinations (I2P adresleri) ile geriye dönük uyumluluk için Ed25519 desteklenir, ancak yeni şifreli destinations için tip 11 önerilir.

**Günlük Rotasyonun Faydaları:** - İleri gizlilik: Bugünkü körleştirilmiş anahtarın ele geçirilmesi, dünkünü ortaya çıkarmaz - İlişkilendirilemezlik: Günlük rotasyon, DHT üzerinden uzun vadeli takibi engeller - Anahtar ayrımı: Farklı zaman dilimleri için farklı anahtarlar

**Kaynaklar:** - [ZCash Protokol Spesifikasyonu](https://zips.z.cash/protocol/protocol.pdf) - Bölüm 5.4.6.1 - [Tor Anahtar Körleme Tartışması](https://lists.torproject.org/pipermail/tor-dev/2013-December/005943.html) - [Tor Bilet #8106](https://trac.torproject.org/projects/tor/ticket/8106)

---

## Şifreleme ve İşleme

### Subcredential (alt kimlik bilgisi) türetimi

Şifrelemeden önce, şifrelenmiş katmanları Destination'ın (I2P hedef adresi) imzalama genel anahtarı bilgisine bağlamak için bir kimlik bilgisi ve bir alt kimlik bilgisi türetiriz.

**Amaç:** Yalnızca Destination'ın (I2P'de bir hizmetin kimliği) imzalama için açık anahtarını bilenlerin şifrelenmiş LeaseSet'in şifresini çözebilmesini sağlamak. Tam Destination gerekli değildir.

#### Kimlik Bilgisi Hesaplaması

```python
A = destination's signing public key (32 bytes)
stA = signature type of A (2 bytes big endian)
     # 0x0007 for Ed25519 or 0x000b for Red25519
stA' = signature type of blinded key A' (2 bytes big endian)
     # Always 0x000b (Red25519)

keydata = A || stA || stA'  # 36 bytes

credential = H("credential", keydata)  # 32 bytes
```
**Alan Ayrımı:** Kişiselleştirme dizesi `"credential"` bu karmanın herhangi bir DHT arama anahtarıyla veya protokolün diğer kullanımlarıyla çakışmamasını garanti eder.

#### Subcredential (alt kimlik bilgisi) Hesaplaması

```python
blindedPublicKey = A' (32 bytes, from blinding process)

subcredential = H("subcredential", credential || blindedPublicKey)  # 32 bytes
```
**Amaç:** subcredential (alt kimlik bilgisi), şifrelenmiş LeaseSet'i şunlara bağlar: 1. Belirli Destination (credential aracılığıyla) 2. Belirli körleştirilmiş anahtar (blindedPublicKey aracılığıyla) 3. Belirli gün (blindedPublicKey'nin günlük rotasyonu aracılığıyla)

Bu, yeniden oynatma saldırılarını ve cross-day linking (günler arası ilişkilendirme) durumunu önler.

### Katman 1 Şifrelemesi

**Bağlam:** Katman 1, istemci yetkilendirme verilerini içerir ve subcredential (alt kimlik bilgisi) temel alınarak türetilen bir anahtarla şifrelenir.

#### Şifreleme Algoritması

```python
# Prepare input
outerInput = subcredential || publishedTimestamp
# publishedTimestamp: 4 bytes from Layer 0

# Generate random salt
outerSalt = CSRNG(32)  # 32 bytes

# Derive encryption key and IV
keys = HKDF(
    salt=outerSalt,
    ikm=outerInput,
    info="ELS2_L1K",  # Domain separation
    n=44  # 32 bytes key + 12 bytes IV
)

outerKey = keys[0:31]    # 32 bytes (indices 0-31 inclusive)
outerIV = keys[32:43]    # 12 bytes (indices 32-43 inclusive)

# Encrypt and prepend salt
outerPlaintext = [Layer 1 data]
outerCiphertext = outerSalt || ENCRYPT(outerKey, outerIV, outerPlaintext)
```
**Çıktı:** `outerCiphertext` `32 + len(outerPlaintext)` bayt uzunluğundadır.

**Güvenlik Özellikleri:** - Salt (tuz), aynı subcredential (alt kimlik bilgisi) olsa bile benzersiz anahtar/IV çiftlerini garanti eder - Bağlam dizesi `"ELS2_L1K"` alan ayrımı sağlar - ChaCha20 anlamsal güvenlik sağlar (şifreli metnin rastgele olandan ayırt edilememesi)

#### Şifre Çözme Algoritması

```python
# Parse salt from ciphertext
outerSalt = outerCiphertext[0:31]  # First 32 bytes

# Derive decryption key and IV (same process as encryption)
outerInput = subcredential || publishedTimestamp
keys = HKDF(
    salt=outerSalt,
    ikm=outerInput,
    info="ELS2_L1K",
    n=44
)

outerKey = keys[0:31]    # 32 bytes
outerIV = keys[32:43]    # 12 bytes

# Decrypt (skip salt bytes)
outerPlaintext = DECRYPT(outerKey, outerIV, outerCiphertext[32:end])
```
**Doğrulama:** Şifre çözme işleminden sonra, Katman 2'ye geçmeden önce Katman 1 yapısının düzgün biçimlendirilmiş olduğunu doğrulayın.

### Katman 2 Şifreleme

**Bağlam:** Katman 2, gerçek LeaseSet2 verisini içerir ve per-client auth (istemci başına kimlik doğrulama) etkinleştirildiyse authCookie'den, etkin değilse boş dizgeden türetilen bir anahtarla şifrelenir.

#### Şifreleme Algoritması

```python
# Determine authCookie based on authorization mode
if per_client_auth_enabled:
    authCookie = [32-byte cookie from client authorization process]
else:
    authCookie = b''  # Zero-length byte array

# Prepare input
innerInput = authCookie || subcredential || publishedTimestamp

# Generate random salt
innerSalt = CSRNG(32)  # 32 bytes

# Derive encryption key and IV
keys = HKDF(
    salt=innerSalt,
    ikm=innerInput,
    info="ELS2_L2K",  # Domain separation
    n=44  # 32 bytes key + 12 bytes IV
)

innerKey = keys[0:31]    # 32 bytes
innerIV = keys[32:43]    # 12 bytes

# Encrypt and prepend salt
innerPlaintext = [Layer 2 data: LS2 type byte + LeaseSet2 data]
innerCiphertext = innerSalt || ENCRYPT(innerKey, innerIV, innerPlaintext)
```
**Çıktı:** `innerCiphertext` `32 + len(innerPlaintext)` bayttır.

**Anahtar Bağlama:** - İstemci kimlik doğrulaması yoksa: Yalnızca subcredential (alt kimlik bilgisi) ve zaman damgasına bağlanır - İstemci kimlik doğrulaması etkinse: Ayrıca authCookie'ye bağlanır (her yetkilendirilmiş istemci için farklıdır)

#### Şifre Çözme Algoritması

```python
# Determine authCookie (same as encryption)
if per_client_auth_enabled:
    authCookie = [32-byte cookie from client authorization process]
else:
    authCookie = b''  # Zero-length byte array

# Parse salt from ciphertext
innerSalt = innerCiphertext[0:31]  # First 32 bytes

# Derive decryption key and IV
innerInput = authCookie || subcredential || publishedTimestamp
keys = HKDF(
    salt=innerSalt,
    ikm=innerInput,
    info="ELS2_L2K",
    n=44
)

innerKey = keys[0:31]    # 32 bytes
innerIV = keys[32:43]    # 12 bytes

# Decrypt (skip salt bytes)
innerPlaintext = DECRYPT(innerKey, innerIV, innerCiphertext[32:end])
```
**Doğrulama:** Şifresi çözüldükten sonra: 1. LS2 tip baytının geçerli olduğunu doğrula (3 veya 7) 2. LeaseSet2 yapısını ayrıştır 3. İç zaman damgasının dıştaki yayımlanan zaman damgasıyla eşleştiğini doğrula 4. İç sona erme zamanının dıştaki sona erme zamanıyla eşleştiğini doğrula 5. LeaseSet2 imzasını doğrula

### Şifreleme Katmanı Özeti

```
┌─────────────────────────────────────────────────┐
│ Layer 0 (Plaintext)                             │
│ - Blinded public key                            │
│ - Timestamps                                    │
│ - Signature                                     │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │ Layer 1 (Encrypted with subcredential)  │   │
│  │ - Authorization flags                   │   │
│  │ - Client auth data (if enabled)         │   │
│  │                                          │   │
│  │  ┌────────────────────────────────┐     │   │
│  │  │ Layer 2 (Encrypted with        │     │   │
│  │  │          authCookie + subcred) │     │   │
│  │  │ - LeaseSet2 type               │     │   │
│  │  │ - LeaseSet2 data               │     │   │
│  │  │ - Leases                       │     │   │
│  │  │ - LS2 signature                │     │   │
│  │  └────────────────────────────────┘     │   │
│  └─────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```
**Şifre Çözme Akışı:** 1. Körlenmiş açık anahtar kullanarak Katman 0 imzasını doğrulayın 2. subcredential (alt kimlik bilgisi) kullanarak Katman 1'in şifresini çözün 3. authCookie elde etmek için (varsa) yetkilendirme verisini işleyin 4. authCookie ve subcredential kullanarak Katman 2'nin şifresini çözün 5. LeaseSet2'yi doğrulayın ve ayrıştırın

---

## İstemci Başına Yetkilendirme

### Genel Bakış

İstemci bazlı yetkilendirme etkinleştirildiğinde, sunucu yetkilendirilmiş istemcilerin bir listesini tutar. Her istemcinin, güvenli bir bant dışı yolla iletilmesi gereken anahtar materyali vardır.

**İki Yetkilendirme Mekanizması:** 1. **DH (Diffie-Hellman) İstemci Yetkilendirmesi:** Daha güvenlidir, X25519 anahtar anlaşmasını kullanır 2. **PSK (Önceden Paylaşılan Anahtar) Yetkilendirmesi:** Daha basittir, simetrik anahtarlar kullanır

**Ortak Güvenlik Özellikleri:** - İstemci üyeliği gizliliği: Gözlemciler istemci sayısını görür ancak belirli istemcileri tanımlayamaz - Anonim istemci ekleme/kaldırma: Belirli istemcilerin ne zaman eklendiği veya kaldırıldığı izlenemez - 8 baytlık istemci tanımlayıcısı çakışma olasılığı: ~ 18 kentilyonda 1 (ihmal edilebilir)

### DH İstemci Yetkilendirmesi

**Genel Bakış:** Her istemci bir X25519 anahtar çifti oluşturur ve açık anahtarını güvenli bir bant dışı kanal üzerinden sunucuya gönderir. Sunucu, her istemci için benzersiz bir authCookie'yi şifrelemek için ephemeral DH (geçici Diffie-Hellman) kullanır.

#### İstemci Anahtar Üretimi

```python
# Client generates keypair
csk_i = GENERATE_PRIVATE()  # 32-byte X25519 private key
cpk_i = DERIVE_PUBLIC(csk_i)  # 32-byte X25519 public key

# Client sends cpk_i to server via secure out-of-band channel
# Client KEEPS csk_i secret (never transmitted)
```
**Güvenlik Avantajı:** İstemcinin özel anahtarı cihazını asla terk etmez. Bant dışı iletimi ele geçiren bir saldırgan, X25519 DH'yi (Diffie-Hellman anahtar değişimi) kırmadan gelecekteki şifrelenmiş LeaseSets'i deşifre edemez.

#### Sunucu Tarafı İşleme

```python
# Server generates new auth cookie and ephemeral keypair
authCookie = CSRNG(32)  # 32-byte cookie

esk = GENERATE_PRIVATE()  # 32-byte ephemeral private key
epk = DERIVE_PUBLIC(esk)  # 32-byte ephemeral public key

# For each authorized client i
for cpk_i in authorized_clients:
    # Perform DH key agreement
    sharedSecret = DH(esk, cpk_i)  # 32 bytes
    
    # Derive client-specific encryption key
    authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
    okm = HKDF(
        salt=epk,  # Ephemeral public key as salt
        ikm=authInput,
        info="ELS2_XCA",  # Domain separation
        n=52  # 32 key + 12 IV + 8 ID
    )
    
    # Extract components
    clientKey_i = okm[0:31]    # 32 bytes
    clientIV_i = okm[32:43]    # 12 bytes
    clientID_i = okm[44:51]    # 8 bytes
    
    # Encrypt authCookie for this client
    clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
    
    # Store [clientID_i, clientCookie_i] entry in Layer 1
```
**Katman 1 Veri Yapısı:**

```
ephemeralPublicKey (32 bytes)
clients (2 bytes) = N
[clientID_1 (8 bytes) || clientCookie_1 (32 bytes)]
[clientID_2 (8 bytes) || clientCookie_2 (32 bytes)]
...
[clientID_N (8 bytes) || clientCookie_N (32 bytes)]
```
**Sunucu Önerileri:** - Yayınlanan her şifreli LeaseSet için yeni bir geçici anahtar çifti oluşturun - Pozisyona dayalı izlemeyi önlemek için istemci sırasını rastgeleleştirin - Gerçek istemci sayısını gizlemek için sahte girdiler eklemeyi düşünün

#### İstemci İşleme

```python
# Client has: csk_i (their private key), destination, date, secret
# Client receives: encrypted LeaseSet with epk in Layer 1

# Perform DH key agreement with server's ephemeral public key
sharedSecret = DH(csk_i, epk)  # 32 bytes

# Derive expected client identifier and decryption key
cpk_i = DERIVE_PUBLIC(csk_i)  # Client's own public key
authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp

okm = HKDF(
    salt=epk,
    ikm=authInput,
    info="ELS2_XCA",
    n=52
)

clientKey_i = okm[0:31]    # 32 bytes
clientIV_i = okm[32:43]    # 12 bytes
clientID_i = okm[44:51]    # 8 bytes

# Search Layer 1 authorization data for clientID_i
for (clientID, clientCookie) in layer1_auth_entries:
    if clientID == clientID_i:
        # Found matching entry, decrypt authCookie
        authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie)
        # Use authCookie to decrypt Layer 2
        break
else:
    # No matching entry - client not authorized or revoked
    raise AuthorizationError("Client not authorized")
```
**İstemci Hata Yönetimi:** - `clientID_i` bulunamadıysa: İstemcinin yetkisi iptal edilmiştir ya da hiç yetkilendirilmemiştir - Şifre çözme başarısız olursa: Bozulmuş veri ya da yanlış anahtarlar (son derece nadir) - İstemciler, iptali tespit etmek için periyodik olarak yeniden almalılar

### PSK (önceden paylaşılan anahtar) İstemci Yetkilendirmesi

**Genel Bakış:** Her istemcinin önceden paylaşılan 32 baytlık simetrik bir anahtarı vardır. Sunucu, her istemcinin PSK'sini (önceden paylaşılan anahtar) kullanarak aynı authCookie'yi şifreler.

#### Anahtar Üretimi

```python
# Option 1: Client generates key
psk_i = CSRNG(32)  # 32-byte pre-shared key
# Client sends psk_i to server via secure out-of-band channel

# Option 2: Server generates key
psk_i = CSRNG(32)  # 32-byte pre-shared key
# Server sends psk_i to one or more clients via secure out-of-band channel
```
**Güvenlik Notu:** İstenirse aynı PSK (önceden paylaşılan anahtar) birden fazla istemci arasında paylaşılabilir (bir "grup" yetkilendirmesi oluşturur).

#### Sunucu İşleme

```python
# Server generates new auth cookie and salt
authCookie = CSRNG(32)  # 32-byte cookie
authSalt = CSRNG(32)     # 32-byte salt

# For each authorized client i
for psk_i in authorized_clients:
    # Derive client-specific encryption key
    authInput = psk_i || subcredential || publishedTimestamp
    
    okm = HKDF(
        salt=authSalt,
        ikm=authInput,
        info="ELS2PSKA",  # Domain separation
        n=52  # 32 key + 12 IV + 8 ID
    )
    
    # Extract components
    clientKey_i = okm[0:31]    # 32 bytes
    clientIV_i = okm[32:43]    # 12 bytes
    clientID_i = okm[44:51]    # 8 bytes
    
    # Encrypt authCookie for this client
    clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
    
    # Store [clientID_i, clientCookie_i] entry in Layer 1
```
**Katman 1 Veri Yapısı:**

```
authSalt (32 bytes)
clients (2 bytes) = N
[clientID_1 (8 bytes) || clientCookie_1 (32 bytes)]
[clientID_2 (8 bytes) || clientCookie_2 (32 bytes)]
...
[clientID_N (8 bytes) || clientCookie_N (32 bytes)]
```
#### İstemci İşleme

```python
# Client has: psk_i (their pre-shared key), destination, date, secret
# Client receives: encrypted LeaseSet with authSalt in Layer 1

# Derive expected client identifier and decryption key
authInput = psk_i || subcredential || publishedTimestamp

okm = HKDF(
    salt=authSalt,
    ikm=authInput,
    info="ELS2PSKA",
    n=52
)

clientKey_i = okm[0:31]    # 32 bytes
clientIV_i = okm[32:43]    # 12 bytes
clientID_i = okm[44:51]    # 8 bytes

# Search Layer 1 authorization data for clientID_i
for (clientID, clientCookie) in layer1_auth_entries:
    if clientID == clientID_i:
        # Found matching entry, decrypt authCookie
        authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie)
        # Use authCookie to decrypt Layer 2
        break
else:
    # No matching entry - client not authorized or revoked
    raise AuthorizationError("Client not authorized")
```
### Karşılaştırma ve Öneriler

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">DH Authorization</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">PSK Authorization</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Key Exchange</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Asymmetric (X25519)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Symmetric (shared secret)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Security</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Higher (forward secrecy)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Lower (depends on PSK secrecy)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Client Privacy</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Private key never transmitted</td><td style="border:1px solid var(--color-border); padding:0.5rem;">PSK must be transmitted securely</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Performance</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">N+1 DH operations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">No DH operations</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Key Sharing</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">One key per client</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Can share key among multiple clients</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Revocation Detection</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Adversary cannot tell when revoked</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Adversary can track revocation if PSK intercepted</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Use Case</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">High security requirements</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Performance-critical or group access</td></tr>
  </tbody>
</table>
**Öneri:** - **DH yetkilendirmesini kullanın** ileriye dönük gizliliğin önemli olduğu yüksek güvenlikli uygulamalar için - **PSK yetkilendirmesini kullanın** performansın kritik olduğu durumlarda veya istemci gruplarını yönetirken - **PSK'leri asla yeniden kullanmayın** farklı hizmetler veya zaman dilimleri arasında - **Her zaman güvenli kanallar kullanın** anahtar dağıtımı için (örn., Signal, OTR, PGP)

### Güvenlik Hususları

**İstemci Üyeliğinin Gizliliği:**

Her iki mekanizma da istemci üyeliği için gizliliği şu yollarla sağlar: 1. **Şifrelenmiş istemci tanımlayıcıları:** HKDF çıktısından türetilen 8 baytlık clientID 2. **Ayırt edilemeyen tanımlama bilgileri:** Tüm 32 baytlık clientCookie değerleri rastgele görünür 3. **İstemciye özgü meta veri yok:** Hangi girdinin hangi istemciye ait olduğunu belirlemenin bir yolu yok

Bir gözlemci şunları görebilir: - Yetkili istemci sayısı (`clients` alanından) - Zaman içinde istemci sayısındaki değişiklikler

Bir gözlemci ŞUNLARI GÖREMEZ: - Hangi belirli istemcilerin yetkilendirildiği - Belirli istemcilerin ne zaman eklendiği veya kaldırıldığı (sayı aynı kalıyorsa) - İstemciyi tanımlayıcı herhangi bir bilgi

**Rastgeleleştirme Önerileri:**

Sunucular, şifrelenmiş bir LeaseSet oluşturduklarında her seferinde istemci sırasını rastgeleleştirmelidir:

```python
import random

# Before serializing
auth_entries = [(clientID_i, clientCookie_i) for each client]
random.shuffle(auth_entries)
# Now serialize in randomized order
```
**Faydalar:** - İstemcilerin listedeki konumlarını öğrenmelerini önler - Konum değişikliklerine dayalı çıkarım saldırılarını önler - İstemcilerin eklenmesi/iptal edilmesini ayırt edilemez hale getirir

**İstemci Sayısını Gizleme:**

Sunucular rastgele dummy girdiler (sahte girdiler) ekleyebilir:

```python
# Add dummy entries
num_dummies = random.randint(0, max_dummies)
for _ in range(num_dummies):
    dummy_id = CSRNG(8)
    dummy_cookie = CSRNG(32)
    auth_entries.append((dummy_id, dummy_cookie))

# Randomize all entries (real + dummy)
random.shuffle(auth_entries)
```
**Maliyet:** Doldurma girdileri, şifrelenmiş LeaseSet boyutunu artırır (her biri 40 bayt).

**AuthCookie Rotasyonu:**

Sunucular yeni bir authCookie oluşturmalıdır: - Şifrelenmiş bir LeaseSet yayımlandığında her seferinde (genellikle birkaç saatte bir) - Bir istemcinin yetkisini iptal ettikten hemen sonra - Hiçbir istemci değişikliği olmasa bile düzenli bir programa göre (örn. günlük)

**Faydalar:** - authCookie kompromize olursa maruz kalmayı sınırlar - Yetkisi iptal edilen istemcilerin erişimi hızla kaybetmesini sağlar - Katman 2 için ileri gizlilik sağlar

---

## Şifrelenmiş LeaseSets (I2P'de bir hedefin gelen tunnel uçlarını ve anahtarlarını içeren kayıtlar) için Base32 Adresleme

### Genel Bakış

Geleneksel I2P base32 adresleri yalnızca Destination (I2P hedef adresi) hash'ini içerir (32 bayt → 52 karakter). Bu, şifrelenmiş LeaseSets için yetersizdir çünkü:

1. İstemcilerin, körleştirilmiş açık anahtarı türetebilmesi için **körleştirilmemiş açık anahtar** gereklidir
2. İstemcilerin, doğru anahtar türetimi için **imza türleri** (körleştirilmemiş ve körleştirilmiş) gereklidir
3. Yalnızca hash (özet) bu bilgiyi sağlamaz

**Çözüm:** Açık anahtar ve imza türlerini içeren yeni bir base32 biçimi.

### Adres Biçimi Spesifikasyonu

**Çözümlenmiş Yapı (35 bayt):**

```
┌─────────────────────────────────────────────────────┐
│ Byte 0   │ Byte 1  │ Byte 2  │ Bytes 3-34          │
│ Flags    │ Unblind │ Blinded │ Public Key          │
│ (XOR)    │ SigType │ SigType │ (32 bytes)          │
│          │ (XOR)   │ (XOR)   │                     │
└─────────────────────────────────────────────────────┘
```
**İlk 3 Bayt (Checksum ile XOR):**

İlk 3 bayt, bir CRC-32 sağlama toplamının bölümleriyle XOR'lanmış üstveri içerir:

```python
# Data structure before XOR
flags = 0x00           # 1 byte (reserved for future use)
unblinded_sigtype = 0x07 or 0x0b  # 1 byte (7 or 11)
blinded_sigtype = 0x0b  # 1 byte (always 11)

# Compute CRC-32 checksum of public key
checksum = crc32(pubkey)  # 4-byte CRC-32 of bytes 3-34

# XOR first 3 bytes with parts of checksum
data[0] = flags XOR (checksum >> 24) & 0xFF
data[1] = unblinded_sigtype XOR (checksum >> 16) & 0xFF  
data[2] = blinded_sigtype XOR (checksum >> 8) & 0xFF

# Bytes 3-34 contain the unmodified 32-byte public key
data[3:34] = pubkey
```
**Sağlama Toplamı Özellikleri:** - Standart CRC-32 polinomunu kullanır - Yanlış negatif oranı: ~16 milyonda 1 - Adres yazım hataları için hata tespiti sağlar - Kimlik doğrulama için kullanılamaz (kriptografik olarak güvenli değildir)

**Kodlanmış Biçim:**

```
Base32Encode(35 bytes) || ".b32.i2p"
```
**Özellikler:** - Toplam karakter sayısı: 56 (35 bayt × 8 bit ÷ karakter başına 5 bit) - Sonek: ".b32.i2p" (geleneksel base32 ile aynı) - Toplam uzunluk: 56 + 8 = 64 karakter (null sonlandırıcı hariç)

**Base32 Kodlaması:** - Alfabe: `abcdefghijklmnopqrstuvwxyz234567` (RFC 4648 standardı) - Sondaki kullanılmayan 5 bit MUTLAKA 0 olmalıdır - Büyük/küçük harfe duyarsızdır (gelenek gereği küçük harf)

### Adres Oluşturma

```python
import struct
from zlib import crc32
import base64

def generate_encrypted_b32_address(pubkey, unblinded_sigtype, blinded_sigtype):
    """
    Generate base32 address for encrypted LeaseSet.
    
    Args:
        pubkey: 32-byte public key (bytes)
        unblinded_sigtype: Unblinded signature type (7 or 11)
        blinded_sigtype: Blinded signature type (always 11)
    
    Returns:
        String address ending in .b32.i2p
    """
    # Verify inputs
    assert len(pubkey) == 32, "Public key must be 32 bytes"
    assert unblinded_sigtype in [7, 11], "Unblinded sigtype must be 7 or 11"
    assert blinded_sigtype == 11, "Blinded sigtype must be 11"
    
    # Compute CRC-32 of public key
    checksum = crc32(pubkey) & 0xFFFFFFFF  # Ensure 32-bit unsigned
    
    # Prepare metadata bytes
    flags = 0x00
    
    # XOR metadata with checksum parts
    byte0 = flags ^ ((checksum >> 24) & 0xFF)
    byte1 = unblinded_sigtype ^ ((checksum >> 16) & 0xFF)
    byte2 = blinded_sigtype ^ ((checksum >> 8) & 0xFF)
    
    # Construct 35-byte data
    data = bytes([byte0, byte1, byte2]) + pubkey
    
    # Base32 encode (standard alphabet)
    # Python's base64 module uses uppercase by default
    b32 = base64.b32encode(data).decode('ascii').lower().rstrip('=')
    
    # Construct full address
    address = b32 + ".b32.i2p"
    
    return address
```
### Adres Ayrıştırma

```python
import struct
from zlib import crc32
import base64

def parse_encrypted_b32_address(address):
    """
    Parse base32 address for encrypted LeaseSet.
    
    Args:
        address: String address ending in .b32.i2p
    
    Returns:
        Tuple of (pubkey, unblinded_sigtype, blinded_sigtype)
    
    Raises:
        ValueError: If address is invalid or checksum fails
    """
    # Remove suffix
    if not address.endswith('.b32.i2p'):
        raise ValueError("Invalid address suffix")
    
    b32 = address[:-8]  # Remove ".b32.i2p"
    
    # Verify length (56 characters for 35 bytes)
    if len(b32) != 56:
        raise ValueError(f"Invalid length: {len(b32)} (expected 56)")
    
    # Base32 decode
    # Add padding if needed
    padding_needed = (8 - (len(b32) % 8)) % 8
    b32_padded = b32.upper() + '=' * padding_needed
    
    try:
        data = base64.b32decode(b32_padded)
    except Exception as e:
        raise ValueError(f"Invalid base32 encoding: {e}")
    
    # Verify decoded length
    if len(data) != 35:
        raise ValueError(f"Invalid decoded length: {len(data)} (expected 35)")
    
    # Extract public key
    pubkey = data[3:35]
    
    # Compute CRC-32 for verification
    checksum = crc32(pubkey) & 0xFFFFFFFF
    
    # Un-XOR metadata bytes
    flags = data[0] ^ ((checksum >> 24) & 0xFF)
    unblinded_sigtype = data[1] ^ ((checksum >> 16) & 0xFF)
    blinded_sigtype = data[2] ^ ((checksum >> 8) & 0xFF)
    
    # Verify expected values
    if flags != 0x00:
        raise ValueError(f"Invalid flags: {flags:#x} (expected 0x00)")
    
    if unblinded_sigtype not in [7, 11]:
        raise ValueError(f"Invalid unblinded sigtype: {unblinded_sigtype} (expected 7 or 11)")
    
    if blinded_sigtype != 11:
        raise ValueError(f"Invalid blinded sigtype: {blinded_sigtype} (expected 11)")
    
    return pubkey, unblinded_sigtype, blinded_sigtype
```
### Geleneksel Base32 ile Karşılaştırma

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Traditional B32</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Encrypted LS2 B32</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Content</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-256 hash of Destination</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Public key + signature types</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Decoded Size</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">35 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Encoded Length</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">52 characters</td><td style="border:1px solid var(--color-border); padding:0.5rem;">56 characters</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Suffix</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">.b32.i2p</td><td style="border:1px solid var(--color-border); padding:0.5rem;">.b32.i2p</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Total Length</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">60 chars</td><td style="border:1px solid var(--color-border); padding:0.5rem;">64 chars</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Checksum</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">None</td><td style="border:1px solid var(--color-border); padding:0.5rem;">CRC-32 (XOR'd into first 3 bytes)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Use Case</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Regular destinations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted LeaseSet destinations</td></tr>
  </tbody>
</table>
### Kullanım Kısıtlamaları

**BitTorrent Uyumsuzluğu:**

Şifreli LS2 adresleri BitTorrent'in compact announce yanıtlarıyla KULLANILAMAZ:

```
Compact announce reply format:
┌────────────────────────────┐
│ 32-byte destination hash   │  ← Only hash, no signature types
│ 2-byte port                │
└────────────────────────────┘
```
**Sorun:** Kompakt biçim yalnızca özeti (32 bayt) içerir; imza türleri veya açık anahtar bilgisi için yer yoktur.

**Çözüm:** Tam announce yanıtlarını veya tam adresleri destekleyen HTTP tabanlı tracker'ları kullanın.

### Adres Defteri Entegrasyonu

Bir istemcinin adres defterinde tam bir Destination (I2P hedef kimliği) varsa:

1. Tam Destination'ı (I2P hedef adresi; açık anahtarı içerir) kaydet
2. Hash ile tersine aramayı destekle
3. Şifreli LS2 ile karşılaşıldığında, açık anahtarı adres defterinden al
4. Tam Destination zaten biliniyorsa yeni base32 biçimine gerek yok

**Şifreli LS2 (LeaseSet2)'yi destekleyen adres defteri formatları:** - hosts.txt içinde tam destination dizeleri - destination sütunu olan SQLite veritabanları - tam destination verisi içeren JSON/XML formatları

### Uygulama Örnekleri

**Örnek 1: Adres Oluştur**

```python
# Ed25519 destination example
pubkey = bytes.fromhex('a' * 64)  # 32-byte public key
unblinded_type = 7   # Ed25519
blinded_type = 11    # Red25519 (always)

address = generate_encrypted_b32_address(pubkey, unblinded_type, blinded_type)
print(f"Address: {address}")
# Output: 56 base32 characters + .b32.i2p
```
**Örnek 2: Ayrıştır ve Doğrula**

```python
address = "abc...xyz.b32.i2p"  # 56 chars + suffix

try:
    pubkey, unblinded, blinded = parse_encrypted_b32_address(address)
    print(f"Public Key: {pubkey.hex()}")
    print(f"Unblinded SigType: {unblinded}")
    print(f"Blinded SigType: {blinded}")
except ValueError as e:
    print(f"Invalid address: {e}")
```
**Örnek 3: Destination (hedef) üzerinden dönüştürme**

```python
def destination_to_encrypted_b32(destination):
    """
    Convert full Destination to encrypted LS2 base32 address.
    
    Args:
        destination: I2P Destination object
    
    Returns:
        Base32 address string
    """
    # Extract public key and signature type from destination
    pubkey = destination.signing_public_key  # 32 bytes
    sigtype = destination.sig_type  # 7 or 11
    
    # Blinded type is always 11 (Red25519)
    blinded_type = 11
    
    # Generate address
    return generate_encrypted_b32_address(pubkey, sigtype, blinded_type)
```
### Güvenlik Hususları

**Gizlilik:** - Base32 adresi açık anahtarı ortaya çıkarır - Bu, kasıtlıdır ve protokol için gereklidir - Özel anahtarı KESİNLİKLE ifşa etmez veya güvenliği tehlikeye atmaz - Açık anahtarlar tasarım gereği herkese açık bilgidir

**Çakışma Direnci:** - CRC-32 yalnızca 32 bit çakışma direnci sağlar - Kriptografik olarak güvenli değildir (yalnızca hata tespiti için kullanın) - Kimlik doğrulama için sağlama toplamına güvenmeyin - Tam hedef doğrulaması hâlâ gereklidir

**Adres Doğrulama:** - Kullanımdan önce her zaman sağlama toplamını doğrulayın - Geçersiz imza türlerine sahip adresleri reddedin - Açık anahtarın eliptik eğri üzerinde olduğunu doğrulayın (uygulamaya özgü)

**Referanslar:** - [Teklif 149: Şifrelenmiş LS2 için B32](/proposals/149-b32-encrypted-ls2/) - [B32 Adresleme Spesifikasyonu](/docs/specs/b32-for-encrypted-leasesets/) - [I2P Adlandırma Spesifikasyonu](/docs/overview/naming/)

---

## Çevrimdışı Anahtar Desteği

### Genel Bakış

Çevrimdışı anahtarlar, ana imzalama anahtarının çevrimdışı (soğuk depoda) kalmasını sağlarken, günlük işlemler için geçici bir imzalama anahtarının kullanılmasına olanak tanır. Bu, yüksek güvenlikli hizmetler için kritiktir.

**Şifreli LS2'ye Özgü Gereksinimler:** - Geçici anahtarlar çevrimdışı olarak üretilmelidir - Körleştirilmiş özel anahtarlar önceden üretilmelidir (günde bir adet) - Hem geçici hem de körleştirilmiş anahtarlar toplu halde teslim edilmelidir - Henüz standartlaştırılmış bir dosya biçimi tanımlanmadı (spesifikasyonda TODO)

### Çevrimdışı Anahtar Yapısı

**Katman 0 Geçici Anahtar Verisi (0 numaralı bayrak biti 1 ise):**

```
┌───────────────────────────────────────────────────┐
│ Expires Timestamp       │ 4 bytes (seconds)       │
│ Transient Sig Type      │ 2 bytes (big endian)    │
│ Transient Signing Pubkey│ Variable (sigtype len)  │
│ Signature (by blinded)  │ 64 bytes (Red25519)     │
└───────────────────────────────────────────────────┘
```
**İmza Kapsamı:** Çevrimdışı anahtar bloğundaki imza şunları kapsar: - Sona erme zaman damgası (4 bayt) - Geçici imza türü (2 bayt)   - Geçici imzalama açık anahtarı (değişken)

Bu imza, **körleştirilmiş açık anahtar** kullanılarak doğrulanır ve bu da körleştirilmiş özel anahtara sahip tarafın bu geçici anahtarı yetkilendirdiğini kanıtlar.

### Anahtar Üretim Süreci

**Çevrimdışı anahtarlarla şifreli LeaseSet için:**

1. **Geçici anahtar çiftleri oluştur** (çevrimdışı, soğuk depolamada):
   ```python
   # For each day in future
   for date in future_dates:
       # Generate daily transient keypair
       transient_privkey = generate_red25519_privkey()  # Type 11
       transient_pubkey = derive_public(transient_privkey)

       # Store for later delivery
       keys[date] = (transient_privkey, transient_pubkey)
   ```

2. **Generate daily blinded keypairs** (offline, in cold storage):
   ```python
# Her gün için    for date in future_dates:

       # Derive alpha for this date
       datestring = date.strftime("%Y%m%d")  # "YYYYMMDD"
       alpha = GENERATE_ALPHA(destination, datestring, secret)
       
       # Blind the signing private key
       a = destination_signing_privkey  # Type 7 or 11
       blinded_privkey = BLIND_PRIVKEY(a, alpha)  # Result is type 11
       blinded_pubkey = DERIVE_PUBLIC(blinded_privkey)
       
       # Store for later delivery
       blinded_keys[date] = (blinded_privkey, blinded_pubkey)
   ```

3. **Sign transient keys with blinded keys** (offline):
   ```python
for date in future_dates:

       transient_pubkey = keys[date][1]
       blinded_privkey = blinded_keys[date][0]
       
       # Create signature data
       expires = int((date + timedelta(days=1)).timestamp())
       sig_data = struct.pack('>I', expires)  # 4 bytes
       sig_data += struct.pack('>H', 11)     # Transient type (Red25519)
       sig_data += transient_pubkey          # 32 bytes
       
       # Sign with blinded private key
       signature = RED25519_SIGN(blinded_privkey, sig_data)
       
       # Package for delivery
       offline_sig_blocks[date] = {
           'expires': expires,
           'transient_type': 11,
           'transient_pubkey': transient_pubkey,
           'signature': signature
       }
   ```

4. **Package for delivery to router:**
   ```python
# Her tarih için    delivery_package[date] = {

       'transient_privkey': keys[date][0],
       'transient_pubkey': keys[date][1],
       'blinded_privkey': blinded_keys[date][0],
       'blinded_pubkey': blinded_keys[date][1],
       'offline_sig_block': offline_sig_blocks[date]
}

   ```

### Router Usage

**Daily Key Loading:**

```python
# UTC'de gece yarısı (veya yayımlamadan önce)

date = datetime.utcnow().date()

# Bugün için anahtarları yükle

today_keys = load_delivery_package(date)

transient_privkey = today_keys['transient_privkey'] transient_pubkey = today_keys['transient_pubkey'] blinded_privkey = today_keys['blinded_privkey'] blinded_pubkey = today_keys['blinded_pubkey'] offline_sig_block = today_keys['offline_sig_block']

# Bugünkü şifreli LeaseSet (I2P'de bir hedefin gelen tunnel bilgilerini içeren kayıt) için bu anahtarları kullanın

```

**Publishing Process:**

```python
# 1. İç LeaseSet2 (LeaseSet'in 2. sürümü) oluşturun

inner_ls2 = create_leaseset2(

    destinations, leases, expires, 
    signing_key=transient_privkey  # Use transient key
)

# 2. Katman 2'yi Şifrele

layer2_ciphertext = encrypt_layer2(inner_ls2, authCookie, subcredential, timestamp)

# 3. Yetkilendirme verileriyle Katman 1'i oluşturun

layer1_plaintext = create_layer1(authorization_data, layer2_ciphertext)

# 4. Katman 1'i Şifrele

layer1_ciphertext = encrypt_layer1(layer1_plaintext, subcredential, timestamp)

# 5. Katman 0'ı çevrimdışı imza bloğuyla oluşturun

layer0 = create_layer0(

    blinded_pubkey,
    timestamp,
    expires,
    flags=0x0001,  # Bit 0 set (offline keys present)
    offline_sig_block=offline_sig_block,
    layer1_ciphertext=layer1_ciphertext
)

# 6. Katman 0'ı geçici özel anahtarla imzala

signature = RED25519_SIGN(transient_privkey, layer0)

# 7. İmzayı ekle ve yayımla

encrypted_leaseset = layer0 + signature publish_to_netdb(encrypted_leaseset)

```

### Security Considerations

**Tracking via Offline Signature Block:**

The offline signature block is in plaintext (Layer 0). An adversary scraping floodfills could:
- Track the same encrypted LeaseSet across multiple days
- Correlate encrypted LeaseSets even though blinded keys change daily

**Mitigation:** Generate new transient keys daily (in addition to blinded keys):

```python
# Her gün HEM yeni transient (geçici) anahtarlar HEM DE yeni blinded (körlenmiş) anahtarlar oluşturun

for date in future_dates:

    # New transient keypair for this day
    transient_privkey = generate_red25519_privkey()
    transient_pubkey = derive_public(transient_privkey)
    
    # New blinded keypair for this day
    alpha = GENERATE_ALPHA(destination, datestring, secret)
    blinded_privkey = BLIND_PRIVKEY(signing_privkey, alpha)
    blinded_pubkey = DERIVE_PUBLIC(blinded_privkey)
    
    # Sign new transient key with new blinded key
    sig = RED25519_SIGN(blinded_privkey, transient_pubkey || metadata)
    
    # Now offline sig block changes daily
```

**Benefits:**
- Prevents tracking across days via offline signature block
- Provides same security as encrypted LS2 without offline keys
- Each day appears completely independent

**Cost:**
- More keys to generate and store
- More complex key management

### File Format (TODO)

**Current Status:** No standardized file format defined for batch key delivery.

**Requirements for Future Format:**

1. **Must support multiple dates:**
   - Batch delivery of 30+ days worth of keys
   - Clear date association for each key set

2. **Must include all necessary data:**
   - Transient private key
   - Transient public key
   - Blinded private key
   - Blinded public key
   - Pre-computed offline signature block
   - Expiration timestamps

3. **Should be tamper-evident:**
   - Checksums or signatures over entire file
   - Integrity verification before loading

4. **Should be encrypted:**
   - Keys are sensitive material
   - Encrypt file with router's key or passphrase

**Proposed Format Example (JSON, encrypted):**

```json
{   "version": 1,   "destination_hash": "base64...",   "keys": [

    {
      "date": "2025-10-15",
      "transient": {
        "type": 11,
        "privkey": "base64...",
        "pubkey": "base64..."
      },
      "blinded": {
        "privkey": "base64...",
        "pubkey": "base64..."
      },
      "offline_sig_block": {
        "expires": 1729123200,
        "signature": "base64..."
      }
    }
],   "signature": "base64..."  // Signature over entire structure }

```

### I2CP Protocol Enhancement (TODO)

**Current Status:** No I2CP protocol enhancement defined for offline keys with encrypted LeaseSet.

**Requirements:**

1. **Key delivery mechanism:**
   - Upload batch of keys from client to router
   - Acknowledgment of successful key loading

2. **Key expiration notification:**
   - Router notifies client when keys running low
   - Client can generate and upload new batch

3. **Key revocation:**
   - Emergency revocation of future keys if compromise suspected

**Proposed I2CP Messages:**

```
UPLOAD_OFFLINE_KEYS   - Şifrelenmiş anahtar materyali paketi   - Kapsanan tarih aralığı

OFFLINE_KEY_STATUS   - Kalan gün sayısı   - Bir sonraki anahtarın sona erme tarihi

REVOKE_OFFLINE_KEYS     - Geçersiz kılınacak tarih aralığı   - Yerine konacak yeni anahtarlar (isteğe bağlı)

```

### Implementation Status

**Java I2P:**
- ✅ Offline keys for standard LS2: Fully supported (since 0.9.38)
- ⚠️ Offline keys for encrypted LS2: Implemented (since 0.9.40)
- ❌ File format: Not standardized
- ❌ I2CP protocol: Not enhanced

**i2pd (C++):**
- ✅ Offline keys for standard LS2: Fully supported
- ✅ Offline keys for encrypted LS2: Fully supported (since 2.58.0)
- ❌ File format: Not standardized
- ❌ I2CP protocol: Not enhanced

**References:**
- [Offline Signatures Proposal](/proposals/123-new-netdb-entries/)
- [I2CP Specification](/docs/specs/i2cp/)

---

## Security Considerations

### Cryptographic Security

**Algorithm Selection:**

All cryptographic primitives are based on well-studied algorithms:
- **ChaCha20:** Modern stream cipher, constant-time, no timing attacks
- **SHA-256:** NIST-approved hash, 128-bit security level
- **HKDF:** RFC 5869 standard, proven security bounds
- **Ed25519/Red25519:** Curve25519-based, ~128-bit security level
- **X25519:** Diffie-Hellman over Curve25519, ~128-bit security level

**Key Sizes:**
- All symmetric keys: 256 bits (32 bytes)
- All public/private keys: 256 bits (32 bytes)
- All nonces/IVs: 96 bits (12 bytes)
- All signatures: 512 bits (64 bytes)

These sizes provide adequate security margins against current and near-future attacks.

### Forward Secrecy

**Daily Key Rotation:**

Encrypted LeaseSets rotate keys daily (UTC midnight):
- New blinded public/private key pair
- New storage location in DHT
- New encryption keys for both layers

**Benefits:**
- Compromising today's blinded key doesn't reveal yesterday's
- Limits exposure window to 24 hours
- Prevents long-term tracking via DHT

**Enhanced with Ephemeral Keys:**

DH client authorization uses ephemeral keys:
- Server generates new ephemeral DH keypair for each publication
- Compromising ephemeral key only affects that publication
- True forward secrecy even if long-term keys compromised

### Privacy Properties

**Destination Blinding:**

The blinded public key:
- Is unlinkable to the original destination (without knowing the secret)
- Changes daily, preventing long-term correlation
- Cannot be reversed to find the original public key

**Client Membership Privacy:**

Per-client authorization provides:
- **Anonymity:** No way to identify which clients are authorized
- **Untraceability:** Cannot track when specific clients added/revoked
- **Size obfuscation:** Can add dummy entries to hide true count

**DHT Privacy:**

Storage location rotates daily:
```
location = SHA-256(sig_type || blinded_public_key)

```

This prevents:
- Correlation across days via DHT lookups
- Long-term monitoring of service availability
- Traffic analysis of DHT queries

### Threat Model

**Adversary Capabilities:**

1. **Network Adversary:**
   - Can monitor all DHT traffic
   - Can observe encrypted LeaseSet publications
   - Cannot decrypt without proper keys

2. **Floodfill Adversary:**
   - Can store and analyze all encrypted LeaseSets
   - Can track publication patterns over time
   - Cannot decrypt Layer 1 or Layer 2
   - Can see client count (but not identities)

3. **Authorized Client Adversary:**
   - Can decrypt specific encrypted LeaseSets
   - Can access inner LeaseSet2 data
   - Cannot determine other clients' identities
   - Cannot decrypt past LeaseSets (with ephemeral keys)

**Out of Scope:**

- Malicious router implementations
- Compromised router host systems
- Side-channel attacks (timing, power analysis)
- Physical access to keys
- Social engineering attacks

### Attack Scenarios

**1. Offline Keys Tracking Attack:**

**Attack:** Adversary tracks encrypted LeaseSets via unchanging offline signature block.

**Mitigation:** Generate new transient keys daily (in addition to blinded keys).

**Status:** Documented recommendation, implementation-specific.

**2. Client Position Inference Attack:**

**Attack:** If client order is static, clients can infer their position and detect when other clients added/removed.

**Mitigation:** Randomize client order in authorization list for each publication.

**Status:** Documented recommendation in specification.

**3. Client Count Analysis Attack:**

**Attack:** Adversary monitors client count changes over time to infer service popularity or client churn.

**Mitigation:** Add random dummy entries to authorization list.

**Status:** Optional feature, deployment-specific trade-off (size vs. privacy).

**4. PSK Interception Attack:**

**Attack:** Adversary intercepts PSK during out-of-band exchange and can decrypt all future encrypted LeaseSets.

**Mitigation:** Use DH client authorization instead, or ensure secure key exchange (Signal, OTR, PGP).

**Status:** Known limitation of PSK approach, documented in specification.

**5. Timing Correlation Attack:**

**Attack:** Adversary correlates publication times across days to link encrypted LeaseSets.

**Mitigation:** Randomize publication times, use delayed publishing.

**Status:** Implementation-specific, not addressed in core specification.

**6. Long-term Secret Compromise:**

**Attack:** Adversary compromises the blinding secret and can compute all past and future blinded keys.

**Mitigation:** 
- Use optional secret parameter (not empty)
- Rotate secret periodically
- Use different secrets for different services

**Status:** Secret parameter is optional; using it is highly recommended.

### Operational Security

**Key Management:**

1. **Signing Private Key:**
   - Store offline in cold storage
   - Use only for generating blinded keys (batch process)
   - Never expose to online router

2. **Blinded Private Keys:**
   - Generate offline, deliver in batches
   - Rotate daily automatically
   - Delete after use (forward secrecy)

3. **Transient Private Keys (with offline keys):**
   - Generate offline, deliver in batches
   - Can be longer-lived (days/weeks)
   - Rotate regularly for enhanced privacy

4. **Client Authorization Keys:**
   - DH: Client private keys never leave client device
   - PSK: Use unique keys per client, secure exchange
   - Revoke immediately upon client removal

**Secret Management:**

The optional secret parameter in `GENERATE_ALPHA`:
- SHOULD be used for high-security services
- MUST be transmitted securely to authorized clients
- SHOULD be rotated periodically (e.g., monthly)
- CAN be different for different client groups

**Monitoring and Auditing:**

1. **Publication Monitoring:**
   - Verify encrypted LeaseSets published successfully
   - Monitor floodfill acceptance rates
   - Alert on publication failures

2. **Client Access Monitoring:**
   - Log client authorization attempts (without identifying clients)
   - Monitor for unusual patterns
   - Detect potential attacks early

3. **Key Rotation Auditing:**
   - Verify daily key rotation occurs
   - Check blinded key changes daily
   - Ensure old keys are deleted

### Implementation Security

**Constant-Time Operations:**

Implementations MUST use constant-time operations for:
- All scalar arithmetic (mod L operations)
- Private key comparisons
- Signature verification
- DH key agreement

**Memory Security:**

- Zero sensitive key material after use
- Use secure memory allocation for keys
- Prevent keys from being paged to disk
- Clear stack variables containing key material

**Random Number Generation:**

- Use cryptographically secure RNG (CSRNG)
- Properly seed RNG from OS entropy source
- Do not use predictable RNGs for key material
- Verify RNG output quality periodically

**Input Validation:**

- Validate all public keys are on the curve
- Check all signature types are supported
- Verify all lengths before parsing
- Reject malformed encrypted LeaseSets early

**Error Handling:**

- Do not leak information via error messages
- Use constant-time comparison for authentication
- Do not expose timing differences in decryption
- Log security-relevant events properly

### Recommendations

**For Service Operators:**

1. ✅ **Use Red25519 (type 11)** for new destinations
2. ✅ **Use DH client authorization** for high-security services
3. ✅ **Generate new transient keys daily** when using offline keys
4. ✅ **Use the optional secret parameter** in GENERATE_ALPHA
5. ✅ **Randomize client order** in authorization lists
6. ✅ **Monitor publication success** and investigate failures
7. ⚠️ **Consider dummy entries** to hide client count (size trade-off)

**For Client Implementers:**

1. ✅ **Validate blinded public keys** are on prime-order subgroup
2. ✅ **Verify all signatures** before trusting data
3. ✅ **Use constant-time operations** for cryptographic primitives
4. ✅ **Zero key material** immediately after use
5. ✅ **Implement proper error handling** without information leaks
6. ✅ **Support both Ed25519 and Red25519** destination types

**For Network Operators:**

1. ✅ **Accept encrypted LeaseSets** in floodfill routers
2. ✅ **Enforce reasonable size limits** to prevent abuse
3. ✅ **Monitor for anomalous patterns** (extremely large, frequent updates)
4. ⚠️ **Consider rate limiting** encrypted LeaseSet publications

---

## Implementation Notes

### Java I2P Implementation

**Repository:** https://github.com/i2p/i2p.i2p

**Key Classes:**
- `net.i2p.data.LeaseSet2` - LeaseSet2 structure
- `net.i2p.data.EncryptedLeaseSet` - Encrypted LS2 implementation
- `net.i2p.crypto.eddsa.EdDSAEngine` - Ed25519/Red25519 signatures
- `net.i2p.crypto.HKDF` - HKDF implementation
- `net.i2p.crypto.ChaCha20` - ChaCha20 cipher

**Configuration:**

Enable encrypted LeaseSet in `clients.config`:
```properties
# Şifreli LeaseSet'i etkinleştir

i2cp.encryptLeaseSet=true

# İsteğe bağlı: İstemci yetkilendirmesini etkinleştirin

i2cp.enableAccessList=true

# İsteğe bağlı: DH (Diffie-Hellman anahtar değişimi) yetkilendirmesini kullanın (varsayılan PSK'dir; pre-shared key - önceden paylaşılan anahtar).

i2cp.accessListType=0

# İsteğe bağlı: Körleme sırrı (şiddetle önerilir)

i2cp.blindingSecret=gizlinizi-buraya-yazın

```

**API Usage Example:**

```java
// Şifrelenmiş bir LeaseSet oluştur EncryptedLeaseSet els = new EncryptedLeaseSet();

// Hedefi ayarla els.setDestination(destination);

// Her istemci için yetkilendirmeyi etkinleştir els.setAuthorizationEnabled(true); els.setAuthType(EncryptedLeaseSet.AUTH_DH);

// Yetkili istemcileri ekle (DH açık anahtarları) for (byte[] clientPubKey : authorizedClients) {

    els.addClient(clientPubKey);
}

// Körleme parametrelerini ayarla els.setBlindingSecret("your-secret");

// İmzala ve yayımla els.sign(signingPrivateKey); netDb.publish(els);

```

### i2pd (C++) Implementation

**Repository:** https://github.com/PurpleI2P/i2pd

**Key Files:**
- `libi2pd/LeaseSet.h/cpp` - LeaseSet implementations
- `libi2pd/Crypto.h/cpp` - Cryptographic primitives
- `libi2pd/Ed25519.h/cpp` - Ed25519/Red25519 signatures
- `libi2pd/ChaCha20.h/cpp` - ChaCha20 cipher

**Configuration:**

Enable in tunnel configuration (`tunnels.conf`):
```ini
[my-hidden-service] type = http host = 127.0.0.1 port = 8080 keys = my-service-keys.dat

# Şifreli LeaseSet'i etkinleştir

encryptleaseset = true

# İsteğe bağlı: İstemci kimlik doğrulama türü (0=DH, 1=PSK)

authtype = 0

# İsteğe bağlı: Körleme sırrı

secret = sırrınız-buraya

# İsteğe bağlı: Yetkilendirilmiş istemciler (her satıra bir, base64 ile kodlanmış açık anahtarlar)

client.1 = base64-ile-kodlanmış-istemci-açık-anahtarı-1 client.2 = base64-ile-kodlanmış-istemci-açık-anahtarı-2

```

**API Usage Example:**

```cpp
// Şifrelenmiş LeaseSet oluştur auto encryptedLS = std::make_shared<i2p::data::EncryptedLeaseSet>(

    destination,
    blindingSecret
);

// İstemci başına yetkilendirmeyi etkinleştir encryptedLS->SetAuthType(i2p::data::AUTH_TYPE_DH);

// Yetkilendirilmiş istemcileri ekle for (const auto& clientPubKey : authorizedClients) {

    encryptedLS->AddClient(clientPubKey);
}

// İmzala ve yayınla encryptedLS->Sign(signingPrivKey); netdb.Publish(encryptedLS);

```

### Testing and Debugging

**Test Vectors:**

Generate test vectors for implementation verification:

```python
# Test vektörü 1: Anahtar körleme

destination_pubkey = bytes.fromhex('a' * 64) sigtype = 7 blinded_sigtype = 11 date = "20251015" secret = ""

alpha = generate_alpha(destination_pubkey, sigtype, blinded_sigtype, date, secret) print(f"Alpha: {alpha.hex()}")

# Beklenen: (referans uygulamayla karşılaştırarak doğrulayın)

```

**Unit Tests:**

Key areas to test:
1. HKDF derivation with various inputs
2. ChaCha20 encryption/decryption
3. Red25519 signature generation and verification
4. Key blinding (private and public)
5. Layer 1/2 encryption/decryption
6. Client authorization (DH and PSK)
7. Base32 address generation and parsing

**Integration Tests:**

1. Publish encrypted LeaseSet to test network
2. Retrieve and decrypt from client
3. Verify daily key rotation
4. Test client authorization (add/remove clients)
5. Test offline keys (if supported)

**Common Implementation Errors:**

1. **Incorrect mod L reduction:** Must use proper modular arithmetic
2. **Endianness errors:** Most fields are big-endian, but some crypto uses little-endian
3. **Off-by-one in array slicing:** Verify indices are inclusive/exclusive as needed
4. **Missing constant-time comparisons:** Use constant-time for all sensitive comparisons
5. **Not zeroing key material:** Always zero keys after use

### Performance Considerations

**Computational Costs:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Cost</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Key blinding (server)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 scalar mult</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per publication</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Key blinding (client)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 point add + 1 scalar mult</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per retrieval</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Layer 1 encryption</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 HKDF + 1 ChaCha20</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Fast</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Layer 2 encryption</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 HKDF + 1 ChaCha20</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Fast</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DH client auth (server)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">N+1 X25519 ops</td><td style="border:1px solid var(--color-border); padding:0.5rem;">N = number of clients</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DH client auth (client)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 X25519 op</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per retrieval</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">PSK client auth</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0 DH ops</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Only HKDF + ChaCha20</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature (Red25519)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 signature op</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Similar cost to Ed25519</td></tr>
  </tbody>
</table>

**Size Overhead:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Component</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Frequency</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded public key</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Layer 1 encryption overhead</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes (salt)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Layer 2 encryption overhead</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes (salt)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DH auth per client</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per client per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DH ephemeral pubkey</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet (if DH auth)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">PSK auth per client</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per client per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">PSK salt</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet (if PSK auth)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature</td><td style="border:1px solid var(--color-border); padding:0.5rem;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline sig block</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈100 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet (if offline keys)</td></tr>
  </tbody>
</table>

**Typical Sizes:**

- **No client auth:** ~200 bytes overhead
- **With 10 DH clients:** ~600 bytes overhead
- **With 100 DH clients:** ~4200 bytes overhead

**Optimization Tips:**

1. **Batch key generation:** Generate blinded keys for multiple days in advance
2. **Cache subcredentials:** Compute once per day, reuse for all publications
3. **Reuse ephemeral keys:** Can reuse ephemeral DH key for short period (minutes)
4. **Parallel client encryption:** Encrypt client cookies in parallel
5. **Fast path for no auth:** Skip authorization layer entirely when disabled

### Compatibility

**Backward Compatibility:**

- Ed25519 (type 7) destinations supported for unblinded keys
- Red25519 (type 11) required for blinded keys
- Traditional LeaseSets still fully supported
- Encrypted LeaseSets do not break existing network

**Forward Compatibility:**

- Reserved flag bits for future features
- Extensible authorization scheme (3 bits allow 8 types)
- Version field in various structures

**Interoperability:**

- Java I2P and i2pd fully interoperable since:
  - Java I2P 0.9.40 (May 2019)
  - i2pd 2.58.0 (September 2025)
- Encrypted LeaseSets work across implementations
- Client authorization works across implementations

---

## References

### IETF RFCs

- **[RFC 2104](https://datatracker.ietf.org/doc/html/rfc2104)** - HMAC: Keyed-Hashing for Message Authentication (February 1997)
- **[RFC 5869](https://datatracker.ietf.org/doc/html/rfc5869)** - HMAC-based Extract-and-Expand Key Derivation Function (HKDF) (May 2010)
- **[RFC 7539](https://datatracker.ietf.org/doc/html/rfc7539)** - ChaCha20 and Poly1305 for IETF Protocols (May 2015)
- **[RFC 7748](https://datatracker.ietf.org/doc/html/rfc7748)** - Elliptic Curves for Security (January 2016)

### I2P Specifications

- **[Common Structures Specification](/docs/specs/common-structures/)** - LeaseSet2 and EncryptedLeaseSet structures
- **[Proposal 123: New netDB Entries](/proposals/123-new-netdb-entries/)** - Background and design of LeaseSet2
- **[Proposal 146: Red25519](/proposals/146-red25519/)** - Red25519 signature scheme specification
- **[Proposal 149: B32 for Encrypted LS2](/proposals/149-b32-encrypted-ls2/)** - Base32 addressing for encrypted LeaseSets
- **[Red25519 Specification](/docs/specs/red25519-signature-scheme/)** - Detailed Red25519 implementation
- **[B32 Addressing Specification](/docs/specs/b32-for-encrypted-leasesets/)** - Base32 address format
- **[Network Database Documentation](/docs/specs/common-structures/)** - NetDB usage and operations
- **[I2CP Specification](/docs/specs/i2cp/)** - I2P Client Protocol

### Cryptographic References

- **[Ed25519 Paper](http://cr.yp.to/papers.html#ed25519)** - "High-speed high-security signatures" by Bernstein et al.
- **[ZCash Protocol Specification](https://zips.z.cash/protocol/protocol.pdf)** - Section 5.4.6: RedDSA signature scheme
- **[Tor Rendezvous Specification v3](https://spec.torproject.org/rend-spec)** - Tor's onion service specification (for comparison)

### Security References

- **[Key Blinding Security Discussion](https://lists.torproject.org/pipermail/tor-dev/2013-December/005943.html)** - Tor Project mailing list discussion
- **[Tor Ticket #8106](https://trac.torproject.org/projects/tor/ticket/8106)** - Key blinding implementation discussion
- **[PRNG Security](http://projectbullrun.org/dual-ec/ext-rand.html)** - Random number generator security considerations
- **[Tor PRNG Discussion](https://lists.torproject.org/pipermail/tor-dev/2015-November/009954.html)** - Discussion of PRNG usage in Tor

### Implementation References

- **[Java I2P Repository](https://github.com/i2p/i2p.i2p)** - Official Java implementation
- **[i2pd Repository](https://github.com/PurpleI2P/i2pd)** - C++ implementation
- **[I2P Website](/)** - Official I2P project website
- **[I2P Specifications](/docs/specs/)** - Complete specification index

### Version History

- **[I2P Release Notes](/en/blog)** - Official release announcements
- **[Java I2P Releases](https://github.com/i2p/i2p.i2p/releases)** - GitHub release history
- **[i2pd Releases](https://github.com/PurpleI2P/i2pd/releases)** - GitHub release history

---

## Appendix A: Cryptographic Constants

### Ed25519 / Red25519 Constants

```python
# Ed25519 baz noktası (üreteç)

B = 2**255 - 19

# Ed25519 mertebesi (skaler alan boyutu)

L = 2**252 + 27742317777372353535851937790883648493

# İmza türü değerleri

SIGTYPE_ED25519 = 7    # 0x0007 SIGTYPE_RED25519 = 11  # 0x000b

# Anahtar uzunlukları

PRIVKEY_SIZE = 32  # bayt PUBKEY_SIZE = 32   # bayt SIGNATURE_SIZE = 64  # bayt

```

### ChaCha20 Constants

```python
# ChaCha20 parametreleri

CHACHA20_KEY_SIZE = 32   # bayt (256 bit) CHACHA20_NONCE_SIZE = 12  # bayt (96 bit) CHACHA20_INITIAL_COUNTER = 1  # RFC 7539, 0 veya 1'e izin verir

```

### HKDF Constants

```python
# HKDF (HMAC tabanlı Anahtar Türetme Fonksiyonu) parametreleri

HKDF_HASH = "SHA-256" HKDF_SALT_MAX = 32  # bayt (HashLen)

# HKDF info dizeleri (alan ayrımı)

HKDF_INFO_ALPHA = b"i2pblinding1" HKDF_INFO_LAYER1 = b"ELS2_L1K" HKDF_INFO_LAYER2 = b"ELS2_L2K" HKDF_INFO_DH_AUTH = b"ELS2_XCA" HKDF_INFO_PSK_AUTH = b"ELS2PSKA"

```

### Hash Personalization Strings

```python
# SHA-256 kişiselleştirme dizeleri

HASH_PERS_ALPHA = b"I2PGenerateAlpha" HASH_PERS_RED25519 = b"I2P_Red25519H(x)" HASH_PERS_CREDENTIAL = b"credential" HASH_PERS_SUBCREDENTIAL = b"subcredential"

```

### Structure Sizes

```python
# Katman 0 (dış) boyutları

BLINDED_SIGTYPE_SIZE = 2   # bayt BLINDED_PUBKEY_SIZE = 32   # bayt (Red25519 için) PUBLISHED_TS_SIZE = 4      # bayt EXPIRES_SIZE = 2           # bayt FLAGS_SIZE = 2             # bayt LEN_OUTER_CIPHER_SIZE = 2  # bayt SIGNATURE_SIZE = 64        # bayt (Red25519)

# Çevrimdışı anahtar blok boyutları

OFFLINE_EXPIRES_SIZE = 4   # bytes OFFLINE_SIGTYPE_SIZE = 2   # bytes OFFLINE_SIGNATURE_SIZE = 64  # bytes

# Katman 1 (orta) boyutları

AUTH_FLAGS_SIZE = 1        # bayt EPHEMERAL_PUBKEY_SIZE = 32  # bayt (DH kimlik doğrulaması) AUTH_SALT_SIZE = 32        # bayt (PSK kimlik doğrulaması) NUM_CLIENTS_SIZE = 2       # bayt CLIENT_ID_SIZE = 8         # bayt CLIENT_COOKIE_SIZE = 32    # bayt AUTH_CLIENT_ENTRY_SIZE = 40  # bayt (CLIENT_ID + CLIENT_COOKIE)

# Şifreleme ek yükü

SALT_SIZE = 32  # bayt (her bir şifrelenmiş katmanın başına eklenir)

# Base32 adresi

B32_ENCRYPTED_DECODED_SIZE = 35  # bayt B32_ENCRYPTED_ENCODED_LEN = 56   # karakter B32_SUFFIX = ".b32.i2p"

```

---

## Appendix B: Test Vectors

### Test Vector 1: Alpha Generation

**Input:**
```python
# Hedef açık anahtarı (Ed25519)

A = bytes.fromhex('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa') stA = 0x0007  # Ed25519 stA_prime = 0x000b  # Red25519 date = "20251015" secret = ""  # secret boş

```

**Computation:**
```python
keydata = A || bytes([0x00, 0x07]) || bytes([0x00, 0x0b])

# keydata = 36 bayt

salt = SHA256(b"I2PGenerateAlpha" + keydata) ikm = b"20251015" info = b"i2pblinding1"

seed = HKDF(salt, ikm, info, 64) alpha = LEOS2IP(seed) mod L

```

**Expected Output:**
```
(Referans implementasyonla karşılaştırarak doğrulayın) alpha = [64 baytlık onaltılık değer]

```

### Test Vector 2: ChaCha20 Encryption

**Input:**
```python
key = bytes([i for i in range(32)])  # 0x00..0x1f nonce = bytes([i for i in range(12)])  # 0x00..0x0b plaintext = b"Hello, I2P!"

```

**Computation:**
```python
ciphertext = ChaCha20_Encrypt(key, nonce, plaintext, counter=1)

```

**Expected Output:**
```
ciphertext = [RFC 7539 test vektörlerine göre doğrulayın]

```

### Test Vector 3: HKDF

**Input:**
```python
salt = bytes(32)  # Tamamı sıfır ikm = b"test input keying material" info = b"ELS2_L1K" n = 44

```

**Computation:**
```python
keys = HKDF(salt, ikm, info, n)

```

**Expected Output:**
```
keys = [44 baytlık onaltılık değer]

```

### Test Vector 4: Base32 Address

**Input:**
```python
pubkey = bytes.fromhex('bbbb' + 'bb' * 30)  # 32 bayt unblinded_sigtype = 11  # Red25519 blinded_sigtype = 11    # Red25519

```

**Computation:**
```python
address = generate_encrypted_b32_address(pubkey, unblinded_sigtype, blinded_sigtype)

```

**Expected Output:**
```
address = [56 base32 karakter].b32.i2p

# Sağlama toplamının doğru şekilde doğrulandığını teyit edin

```

---

## Appendix C: Glossary

**Alpha (α):** The secret blinding factor used to blind public and private keys. Generated from the destination, date, and optional secret.

**AuthCookie:** A 32-byte random value encrypted for each authorized client, used as input to Layer 2 encryption.

**B (Base Point):** The generator point for the Ed25519 elliptic curve.

**Blinded Key:** A public or private key that has been transformed using the alpha blinding factor. Blinded keys cannot be linked to the original keys without knowing alpha.

**ChaCha20:** A stream cipher providing fast, secure encryption without requiring AES hardware support.

**ClientID:** An 8-byte identifier derived from HKDF output, used to identify authorization entries for clients.

**ClientCookie:** A 32-byte encrypted value containing the authCookie for a specific client.

**Credential:** A 32-byte value derived from the destination's public key and signature types, binding encryption to knowledge of the destination.

**CSRNG:** Cryptographically Secure Random Number Generator. Must provide unpredictable output suitable for key generation.

**DH (Diffie-Hellman):** A cryptographic protocol for securely establishing shared secrets. I2P uses X25519.

**Ed25519:** An elliptic curve signature scheme providing fast signatures with 128-bit security level.

**Ephemeral Key:** A short-lived cryptographic key, typically used once and then discarded.

**Floodfill:** I2P routers that store and serve network database entries, including encrypted LeaseSets.

**HKDF:** HMAC-based Key Derivation Function, used to derive multiple cryptographic keys from a single source.

**L (Order):** The order of the Ed25519 scalar field (approximately 2^252).

**Layer 0 (Outer):** The plaintext portion of an encrypted LeaseSet, containing blinded key and metadata.

**Layer 1 (Middle):** The first encrypted layer, containing client authorization data.

**Layer 2 (Inner):** The innermost encrypted layer, containing the actual LeaseSet2 data.

**LeaseSet2 (LS2):** Second version of I2P's network database entry format, introducing encrypted variants.

**NetDB:** The I2P network database, a distributed hash table storing router and destination information.

**Offline Keys:** A feature allowing the main signing key to remain in cold storage while a transient key handles daily operations.

**PSK (Pre-Shared Key):** A symmetric key shared in advance between two parties, used for PSK client authorization.

**Red25519:** An Ed25519-based signature scheme with key blinding support, based on ZCash RedDSA.

**Salt:** Random data used as input to key derivation functions to ensure unique outputs.

**SigType:** A numeric identifier for signature algorithms (e.g., 7 = Ed25519, 11 = Red25519).

**Subcredential:** A 32-byte value derived from the credential and blinded public key, binding encryption to a specific encrypted LeaseSet.

**Transient Key:** A temporary signing key used with offline keys, with a limited validity period.

**X25519:** An elliptic curve Diffie-Hellman protocol over Curve25519, providing key agreement.

---

## Document Information

**Status:** This document represents the current stable encrypted LeaseSet specification as implemented in I2P since June 2019. The protocol is mature and widely deployed.

**Contributing:** For corrections or improvements to this documentation, please submit issues or pull requests to the I2P specifications repository.

**Support:** For questions about implementing encrypted LeaseSets:
- I2P Forum: https://i2pforum.net/
- IRC: #i2p-dev on OFTC
- Matrix: #i2p-dev:matrix.org

**Acknowledgments:** This specification builds on work by the I2P development team, ZCash cryptography research, and Tor Project's key blinding research.