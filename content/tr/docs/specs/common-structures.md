---
title: "Ortak Yapılar"
description: "I2P spesifikasyonları genelinde kullanılan ortak veri türleri ve serileştirme biçimleri"
slug: "common-structures"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Genel Bakış

Bu belge, [I2NP](/docs/specs/i2np/), [I2CP](/docs/specs/i2cp/), [SSU2](/docs/specs/ssu2/), [NTCP2](/docs/specs/ntcp2/) ve diğerleri de dahil olmak üzere tüm I2P protokolleri genelinde kullanılan temel veri yapılarını belirtir. Bu ortak yapılar, farklı I2P uygulamaları ve protokol katmanları arasında birlikte çalışabilirliği sağlar.

### 0.9.58'den Bu Yana Önemli Değişiklikler

- Router Kimlikleri için ElGamal ve DSA-SHA1 kullanımdan kaldırıldı (X25519 + EdDSA kullanın)
- Kuantum-sonrası ML-KEM desteği beta testinde (2.10.0 itibarıyla isteğe bağlı)
- Service record seçenekleri standartlaştırıldı ([Proposal 167](/proposals/167-service-records/), 0.9.66'da uygulandı)
- Sıkıştırılabilir dolgu spesifikasyonları kesinleştirildi ([Proposal 161](/tr/proposals/161-ri-dest-padding/), 0.9.57'de uygulandı)

---

## Ortak Tür Belirtimleri

### Tamsayı

**Açıklama:** Ağ bayt sırası (big-endian; en anlamlı bayt önce) ile temsil edilen negatif olmayan bir tamsayıyı ifade eder.

**İçerik:** İşaretsiz bir tamsayıyı temsil eden 1 ile 8 bayt.

**Kullanım:** I2P protokollerinin genelinde alan uzunlukları, öğe sayıları, tür tanımlayıcıları ve sayısal değerler.

---

### Tarih

**Açıklama:** Unix zaman başlangıcından (1 Ocak 1970 00:00:00 GMT) bu yana geçen süreyi milisaniye cinsinden ifade eden zaman damgası.

**İçerik:** 8 baytlık tamsayı (unsigned long)

**Özel Değerler:** - `0` = Tanımsız veya null tarih - Maksimum değer: `0xFFFFFFFFFFFFFFFF` (yıl 584,942,417,355)

**Uygulama Notları:** - Her zaman UTC/GMT saat dilimi kullanılmalı - Milisaniye düzeyinde hassasiyet gerekir - lease süresinin dolması, RouterInfo yayını ve zaman damgası doğrulaması için kullanılır

---

### Dize

**Açıklama:** UTF-8 ile kodlanmış, uzunluk önekli dize.

**Biçim:**

```
+----+----+----+----+----+----+
|len | UTF-8 encoded data...   |
+----+----+----+----+----+----+

len :: Integer (1 byte)
       Value: 0-255 (string length in bytes, NOT characters)

data :: UTF-8 encoded bytes
        Length: 0-255 bytes
```
**Kısıtlamalar:** - Maksimum uzunluk: 255 bayt (karakter değil - çok baytlı UTF-8 dizileri birden fazla bayt olarak sayılır) - Uzunluk sıfır olabilir (boş dize) - Null sonlandırıcı DAHİL DEĞİL - Dize null ile sonlandırılmış DEĞİLDİR

**Önemli:** UTF-8 dizileri karakter başına birden çok bayt kullanabilir. 100 karakterlik bir dize, çok baytlı karakterler kullanıyorsa 255 baytlık sınırı aşabilir.

---

## Kriptografik Anahtar Yapıları

### PublicKey

**Açıklama:** Asimetrik şifreleme için açık anahtar. Anahtar türü ve uzunluğu bağlama bağlıdır veya bir Key Certificate (Anahtar Sertifikası) içinde belirtilir.

**Varsayılan Tür:** ElGamal (0.9.58 itibarıyla Router Identities için kullanımdan kaldırıldı)

**Desteklenen Türler:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destinations only (unused field)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated for RIs</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">132</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Recommended</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">800</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1184</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1568</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512_CT</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">768</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768_CT</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1088</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024_CT</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1568</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
  </tbody>
</table>
**Uygulama Gereksinimleri:**

1. **X25519 (Tip 4) - Mevcut Standart:**
   - ECIES-X25519-AEAD-Ratchet şifrelemesi için kullanılır
   - 0.9.48'den beri Router Kimlikleri için zorunludur
   - Little-endian (küçük uca öncelikli) kodlama (diğer türlerin aksine)
   - Bkz. [ECIES](/docs/specs/ecies/) ve [ECIES-ROUTERS](/docs/specs/ecies/#routers)

2. **ElGamal (Type 0) - Eski:**
   - 0.9.58 itibarıyla Router kimlikleri için kullanımdan kaldırıldı
   - Destinasyonlar için hala geçerli (alan 0.6/2005'ten beri kullanılmıyor)
   - [ElGamal spesifikasyonu](/docs/specs/cryptography/)'nda tanımlanan sabit asal sayıları kullanır
   - Geriye dönük uyumluluk için destek korunmaktadır

3. **MLKEM (Kuantum Sonrası) - Beta:**
   - Hibrit yaklaşım, ML-KEM'i X25519 ile birleştirir
   - 2.10.0'da varsayılan olarak etkin değildir
   - Hidden Service Manager (Gizli Servis Yöneticisi) üzerinden manuel etkinleştirme gerektirir
   - Bkz. [ECIES-HYBRID](/docs/specs/ecies/#hybrid) ve [Öneri 169](/proposals/169-pq-crypto/)
   - Tip kodları ve teknik özellikler değişikliğe tabidir

**JavaDoc:** [PublicKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/PublicKey.html)

---

### Özel anahtar

**Description:** Asimetrik şifre çözme için özel anahtar; PublicKey türlerine karşılık gelir.

**Depolama:** Tür ve uzunluk bağlamdan çıkarılır ya da veri yapıları/anahtar dosyalarında ayrı olarak saklanır.

**Desteklenen Türler:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destinations only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated for RIs</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">48</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">66</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Recommended</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1632</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2400</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3168</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
  </tbody>
</table>
**Güvenlik Notları:** - Özel anahtarlar MUTLAKA kriptografik olarak güvenli rastgele sayı üreteçleri kullanılarak üretilmelidir - X25519 özel anahtarları, RFC 7748'te tanımlandığı şekilde scalar clamping (skaler kısma) kullanır - Anahtar materyali artık gerekmediğinde bellekten güvenli bir şekilde MUTLAKA silinmelidir

**JavaDoc:** [PrivateKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/PrivateKey.html)

---

### Oturum Anahtarı

**Açıklama:** I2P'nin tunnel ve garlic encryption (garlic şifreleme tekniği) kapsamında AES-256 ile şifreleme ve şifre çözme için simetrik anahtar.

**İçerik:** 32 bayt (256 bit)

**Kullanım:** - Tunnel katmanı şifrelemesi (AES-256/CBC IV ile) - Garlic mesaj şifrelemesi - Uçtan uca oturum şifrelemesi

**Oluşturma:** Kriptografik olarak güvenli bir rastgele sayı üreteci kullanılmalıdır.

**JavaDoc:** [SessionKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SessionKey.html)

---

### SigningPublicKey

**Açıklama:** İmza doğrulaması için açık anahtar. Tür ve uzunluk, Destination (I2P varış adresi) Anahtar Sertifikası'nda belirtilir ya da bağlamdan çıkarılır.

**Varsayılan Tür:** DSA_SHA1 (0.9.58 itibarıyla kullanımdan kaldırılmıştır)

**Desteklenen Türler:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA_SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">128</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA256_P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Older Destinations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA384_P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA512_P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">132</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA256_2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA384_3072</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA512_4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Recommended for SU3</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Recommended</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519ph</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.25</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RedDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted leasesets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specialized</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved (GOST)</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">9</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Proposal 134</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved (GOST)</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">128</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Proposal 134</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved (MLDSA)</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12-20</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Proposal 169</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">65280-65534</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Testing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Never production</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">65535</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Future expansion</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td></tr>
  </tbody>
</table>
**Uygulama Gereksinimleri:**

1. **EdDSA_SHA512_Ed25519 (Tür 7) - Güncel Standart:**
   - 2015'in sonlarından beri tüm yeni Router Kimlikleri ve Hedefler için varsayılan
   - SHA-512 karmasıyla Ed25519 eğrisini kullanır
   - 32 baytlık açık anahtarlar, 64 baytlık imzalar
   - Little-endian (küçük-uçlu) kodlama (diğer çoğu türün aksine)
   - Yüksek performans ve güvenlik

2. **RedDSA_SHA512_Ed25519 (Type 11) - Özel amaçlı:**
   - Yalnızca şifrelenmiş leasesets ve blinding (körleme) için kullanılır
   - Asla Router Identities veya standart Destinations için kullanılmaz
   - EdDSA'ya göre temel farklar:
     - Özel anahtarlar modüler indirgeme ile elde edilir (clamping değil)
     - İmzalar 80 bayt rastgele veri içerir
     - Açık anahtarları doğrudan kullanır (özel anahtarların özetleri değil)
   - Bkz. [Red25519 spesifikasyonu](//docs/specs/red25519-signature-scheme/

3. **DSA_SHA1 (Type 0) - Eski:**
   - 0.9.58 itibarıyla Router Kimlikleri için kullanımdan kaldırıldı
   - Yeni Destinations (hedefler) için önerilmez
   - SHA-1 ile 1024-bit DSA (bilinen zayıflıklar)
   - Destek yalnızca uyumluluk amacıyla sürdürülmektedir

4. **Çok bileşenli anahtarlar:**
   - İki bileşenden oluştuğunda (örneğin ECDSA noktaları X,Y)
   - Her bir bileşen, başa sıfırlar eklenerek length/2 olacak şekilde doldurulur
   - Örnek: 64 baytlık ECDSA anahtarı = 32 bayt X + 32 bayt Y

**JavaDoc:** [SigningPublicKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SigningPublicKey.html)

---

### SigningPrivateKey

**Açıklama:** İmzaları oluşturmak için kullanılan ve SigningPublicKey (imza doğrulaması için kullanılan açık anahtar) türlerine karşılık gelen özel anahtar.

**Depolama:** Tür ve uzunluk oluşturma anında belirtilir.

**Desteklenen Türler:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA_SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA256_P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Older Destinations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA384_P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">48</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA512_P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">66</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA256_2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA384_3072</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">768</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA512_4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1024</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Recommended for SU3</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Recommended</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519ph</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.25</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RedDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted leasesets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specialized</td></tr>
  </tbody>
</table>
**Güvenlik Gereksinimleri:** - Kriptografik olarak güvenli bir rastgele kaynak kullanarak oluşturun - Uygun erişim kontrolleriyle koruyun - İş bittikten sonra bellekten güvenli bir şekilde silin - EdDSA için: 32 baytlık tohum SHA-512 ile özetlenir, ilk 32 bayt skaler hâline getirilir (clamped — bitleri standart maskeyle ayarlanmış) - RedDSA için: Farklı anahtar üretimi (clamping yerine modüler indirgeme)

**JavaDoc:** [SigningPrivateKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SigningPrivateKey.html)

---

### İmza

**Açıklama:** Veri üzerinde, SigningPrivateKey türüne karşılık gelen imzalama algoritması kullanılarak oluşturulan kriptografik imza.

**Tür ve Uzunluk:** İmzalamada kullanılan anahtar türünden çıkarılır.

**Desteklenen Türler:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA_SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">40</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA256_P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Older Destinations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA384_P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA512_P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">132</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA256_2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA384_3072</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA512_4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current for SU3</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Recommended</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519ph</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.25</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RedDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted leasesets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specialized</td></tr>
  </tbody>
</table>
**Biçim Notları:** - Çok öğeli imzalar (ör. ECDSA R,S değerleri) her bir öğe length/2'ye ulaşacak şekilde baştaki sıfırlarla doldurulur - EdDSA ve RedDSA little-endian kodlaması kullanır - Diğer tüm türler big-endian kodlaması kullanır

**Doğrulama:** - İlgili SigningPublicKey kullanın - Anahtar türü için imza algoritması spesifikasyonlarına uyun - İmza uzunluğunun anahtar türü için beklenen uzunlukla eşleştiğini kontrol edin

**JavaDoc:** [Signature](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Signature.html)

---

### Özet

**Açıklama:** Verinin SHA-256 karması, I2P genelinde bütünlük doğrulaması ve tanımlama için kullanılır.

**İçerik:** 32 bayt (256 bit)

**Kullanım:** - Router Kimliği karma değerleri (ağ veritabanı anahtarları) - Hedef karma değerleri (ağ veritabanı anahtarları) - Leases (leaseSet içindeki ögeler) içinde Tunnel ağ geçidinin tanımlanması - Veri bütünlüğünün doğrulanması - Tunnel ID'nin oluşturulması

**Algoritma:** SHA-256, FIPS 180-4'te tanımlandığı şekilde

**JavaDoc:** [Hash](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Hash.html)

---

### Oturum Etiketi

**Açıklama:** Oturum tanımlama ve etiket tabanlı şifreleme için kullanılan rastgele sayı.

**Önemli:** Oturum etiketi boyutu şifreleme türüne göre değişir: - **ElGamal/AES+SessionTag:** 32 bayt (eski) - **ECIES-X25519:** 8 bayt (mevcut standart)

**Mevcut Standart (ECIES - Eliptik Eğri Entegre Şifreleme Şeması):**

```
Contents: 8 bytes
Usage: Ratchet-based encryption for Destinations and Routers
```
Ayrıntılı spesifikasyonlar için [ECIES](/docs/specs/ecies/) ve [ECIES-ROUTERS](/docs/specs/ecies/#routers) belgelerine bakın.

**Eski (ElGamal/AES):**

```
Contents: 32 bytes
Usage: Deprecated encryption scheme
```
**Üretim:** Kriptografik olarak güvenli bir rastgele sayı üretecinin kullanılması zorunludur.

**JavaDoc:** [SessionTag](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SessionTag.html)

---

### TunnelId

**Açıklama:** Bir router'ın bir tunnel içindeki konumuna ilişkin benzersiz tanımlayıcı. Bir tunnel içindeki her atlama kendi TunnelId'sine (tünel kimliği) sahiptir.

**Biçim:**

```
Contents: 4-byte Integer (unsigned 32-bit)
Range: Generally > 0 (zero reserved for special cases)
```
**Kullanım:** - Her router'da gelen/giden tunnel bağlantılarını belirler - Tunnel zincirindeki her hop (ağ atlaması) için farklı bir TunnelId kullanılır - Geçit tunnel'lerini belirlemek için Lease yapılarında (I2P'de kiralama kayıtları) kullanılır

**Özel Değerler:** - `0` = Özel protokol amaçları için ayrılmıştır (normal çalışmada kullanmaktan kaçının) - TunnelIds (tunnel kimlikleri) her bir router için yerel olarak geçerlidir

**JavaDoc:** [TunnelId](http://docs.i2p-projekt.de/javadoc/net/i2p/data/TunnelId.html)

---

## Sertifika Özellikleri

### Sertifika

**Açıklama:** I2P genelinde kullanılan alındılar, iş ispatı (proof-of-work) veya kriptografik üstveri için kapsayıcı.

**Biçim:**

```
+----+----+----+----+----+----+-//
|type| length  | payload
+----+----+----+----+----+----+-//

type :: Integer (1 byte)
        Values: 0-5 (see types below)

length :: Integer (2 bytes, big-endian)
          Size of payload in bytes

payload :: data
           length -> $length bytes
```
**Toplam Boyut:** minimum 3 bayt (NULL certificate - boş sertifika), maksimum 65538 bayt

### Sertifika Türleri

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Payload Length</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Total Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">NULL</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Default/empty certificate</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">HASHCASH</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused (was for proof-of-work)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">HIDDEN</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused (hidden routers don't advertise)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SIGNED</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 or 72</td><td style="border:1px solid var(--color-border); padding:0.5rem;">43 or 75</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused (DSA signature ± destination hash)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MULTIPLE</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused (multiple certificates)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">KEY</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4+</td><td style="border:1px solid var(--color-border); padding:0.5rem;">7+</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Current</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specifies key types (see below)</td></tr>
  </tbody>
</table>
### Anahtar Sertifikası (Tip 5)

**Giriş:** Sürüm 0.9.12 (Aralık 2013)

**Purpose:** Varsayılan olmayan anahtar türlerini belirtir ve standart 384 baytlık KeysAndCert yapısının dışında kalan fazla anahtar verisini depolar.

**Yük Yapısı:**

```
+----+----+----+----+----+----+----+----+-//
|SPKtype|CPKtype| Excess SPK data     |
+----+----+----+----+----+----+----+----+-//
              | Excess CPK data...    |
+----+----+----+----+----+----+----+----+

SPKtype :: Signing Public Key Type (2 bytes)
           See SigningPublicKey table above

CPKtype :: Crypto Public Key Type (2 bytes)
           See PublicKey table above

Excess SPK data :: Signing key bytes beyond 128 bytes
                   Length: 0 to 65531 bytes

Excess CPK data :: Crypto key bytes beyond 256 bytes
                   Length: 0 to remaining space
```
**Kritik Gerçekleştirim Notları:**

1. **Anahtar Türü Sırası:**
   - **UYARI:** İmzalama anahtar türü, Kripto anahtar türünden ÖNCE gelir
   - Bu sezgilere aykırıdır ancak uyumluluk için korunmaktadır
   - Sıra: SPKtype, CPKtype (CPKtype, SPKtype değil)

2. **KeysAndCert içinde Anahtar Verisi Düzeni:**
   ```
   [Crypto Public Key (partial/complete)]
   [Padding (if total key lengths < 384)]
   [Signing Public Key (partial/complete)]
   [Certificate Header (3 bytes)]
   [Key Certificate (4+ bytes)]
   [Excess Signing Key Data]
   [Excess Crypto Key Data]
   ```

3. **Fazla Anahtar Verisini Hesaplama:**
   - Eğer Crypto Key > 256 bayt ise: Excess = (Crypto Length - 256)
   - Eğer Signing Key > 128 bayt ise: Excess = (Signing Length - 128)
   - Padding = max(0, 384 - Crypto Length - Signing Length)

**Örnekler (ElGamal Kripto Anahtarı):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Signing Key Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Total SPK Length</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Padding</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Excess in Cert</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Total Structure Size</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA_SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">128</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 7 = 394</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 7 = 394</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 7 = 394</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">132</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 11 = 398</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">128</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 135 = 522</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">384</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 391 = 778</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 7 = 394</td></tr>
  </tbody>
</table>
**Router Kimliği Gereksinimleri:** - 0.9.15 sürümüne kadar NULL sertifikası kullanıldı - 0.9.16 sürümünden beri varsayılan olmayan anahtar türleri için Anahtar Sertifikası gerekli - 0.9.48 sürümünden beri X25519 şifreleme anahtarları destekleniyor

**Destination (uç nokta kimliği) gereksinimleri:** - NULL sertifika VEYA Key Certificate (anahtar sertifikası) (gerektiğinde) - Varsayılan olmayan imzalama anahtarı türleri için 0.9.12'den beri Key Certificate gereklidir - Kripto açık anahtar alanı 0.6'dan (2005) beri kullanılmıyor, ancak yine de mevcut olmalıdır

**Önemli Uyarılar:**

1. **NULL ve KEY Sertifikası:**
   - ElGamal+DSA_SHA1'ı belirten (0,0) türlerine sahip bir KEY sertifikasına izin verilir ancak önerilmez
   - ElGamal+DSA_SHA1 için her zaman NULL sertifikasını kullanın (kanonik gösterim)
   - (0,0) olan KEY sertifikası 4 bayt daha uzundur ve uyumluluk sorunlarına yol açabilir
   - Bazı gerçekleştirimler (0,0) KEY sertifikalarını doğru şekilde işleyemeyebilir

2. **Fazladan Veri Doğrulaması:**
   - Uygulamalar, sertifika uzunluğunun anahtar türleri için beklenen uzunlukla eşleştiğini doğrulamak ZORUNDADIR
   - Anahtar türlerine karşılık gelmeyen fazladan veri içeren sertifikaları reddedin
   - Geçerli sertifika yapısından sonra yer alan çöp veriyi yasaklayın

**JavaDoc:** [Sertifika](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Certificate.html)

---

### Eşleme

**Açıklama:** Yapılandırma ve meta veriler için kullanılan anahtar-değer özellik koleksiyonu.

**Biçim:**

```
+----+----+----+----+----+----+----+----+
|  size   | key_string (len + data)| =  |
+----+----+----+----+----+----+----+----+
| val_string (len + data)     | ;  | ...
+----+----+----+----+----+----+----+

size :: Integer (2 bytes, big-endian)
        Total number of bytes that follow (not including size field)
        Range: 0 to 65535

key_string :: String
              Format: 1-byte length + UTF-8 data
              Length: 0-255 bytes

= :: Single byte (0x3D, '=' character)

val_string :: String
              Format: 1-byte length + UTF-8 data
              Length: 0-255 bytes

; :: Single byte (0x3B, ';' character)

[Repeat key_string = val_string ; for additional entries]
```
**Boyut Sınırları:** - Anahtar uzunluğu: 0-255 bayt (+ uzunluk için 1 bayt) - Değer uzunluğu: 0-255 bayt (+ uzunluk için 1 bayt) - Toplam eşleme boyutu: 0-65535 bayt (+ boyut alanı için 2 bayt) - Maksimum yapı boyutu: 65537 bayt

**Kritik Sıralama Gereksinimi:**

Eşlemeler **imzalı yapılar** içinde (RouterInfo, RouterAddress, Destination (hedef) özellikleri, I2CP SessionConfig) bulunduğunda, girdiler imzanın değişmezliğini sağlamak için anahtarlarına göre MUTLAKA sıralanmalıdır:

1. **Sıralama Yöntemi:** Unicode kod noktası değerlerini kullanarak leksikografik sıralama (Java String.compareTo() ile eşdeğer)
2. **Büyük/Küçük Harf Duyarlılığı:** Anahtarlar ve değerler genellikle büyük/küçük harfe duyarlıdır (uygulamaya bağlı)
3. **Yinelenen Anahtarlar:** İmzalı yapılarda İZİN VERİLMEZ (imza doğrulama hatasına yol açar)
4. **Karakter Kodlaması:** UTF-8 bayt düzeyinde karşılaştırma

**Sıralama Neden Önemlidir:** - İmzalar bayt gösterimi üzerinden hesaplanır - Farklı anahtar sıraları farklı imzalar üretir - İmzalanmamış eşlemeler sıralama gerektirmez ancak aynı kurala uymalıdır

**Uygulama Notları:**

1. **Kodlama Fazlalığı:**
   - Hem `=` ve `;` ayraçları hem de dize uzunluğu baytları mevcut
   - Bu verimsizdir, ancak uyumluluk için korunmaktadır
   - Uzunluk baytları esas alınır; ayraçlar gerekli olsa da fazladır

2. **Karakter Desteği:**
   - Belgelerde yazılanlara rağmen, `=` ve `;` dizgiler içinde DESTEKLENİR (bunu uzunluk baytları halleder)
   - UTF-8 kodlaması tüm Unicode'u destekler
   - **Uyarı:** I2CP UTF-8 kullanır, ancak I2NP tarihsel olarak UTF-8'i doğru şekilde işleyemiyordu
   - Azami uyumluluk için mümkün olduğunda I2NP eşlemeleri için ASCII kullanın

3. **Özel Bağlamlar:**
   - **RouterInfo/RouterAddress:** Sıralı olmalıdır, yinelenen olmamalıdır
   - **I2CP SessionConfig:** Sıralı olmalıdır, yinelenen olmamalıdır  
   - **Uygulama eşlemeleri:** Sıralama önerilir ancak her zaman zorunlu değildir

**Örnek (RouterInfo seçenekleri):**

```
Mapping size: 45 bytes
Sorted entries:
  caps=L       (capabilities)
  netId=2      (network ID)
  router.version=0.9.67
```
**JavaDoc:** [DataHelper](http://docs.i2p-projekt.de/javadoc/net/i2p/data/DataHelper.html)

---

## Ortak Yapı Belirtimi

### Anahtarlar ve Sertifikalar

**Açıklama:** Şifreleme anahtarı, imzalama anahtarı ve sertifikayı birleştiren temel yapıdır. Hem RouterIdentity (Yönlendirici Kimliği) hem de Destination (Hedef) olarak kullanılır.

**Yapı:**

```
+----+----+----+----+----+----+----+----+
| public_key                            |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| padding (optional)                    |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signing_key                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| certificate                           |
+----+----+----+-//

public_key :: PublicKey (partial or full)
              Default: 256 bytes (ElGamal)
              Other sizes: As specified in Key Certificate

padding :: Random data
           Length: 0 bytes or as needed
           CONSTRAINT: public_key + padding + signing_key = 384 bytes

signing_key :: SigningPublicKey (partial or full)
               Default: 128 bytes (DSA_SHA1)
               Other sizes: As specified in Key Certificate

certificate :: Certificate
               Minimum: 3 bytes (NULL certificate)
               Common: 7 bytes (Key Certificate with default keys)

TOTAL LENGTH: 387+ bytes (never assume exactly 387!)
```
**Anahtar Hizalaması:** - **Kriptografik Açık Anahtar:** Başta hizalı (bayt 0) - **Dolgu:** Ortada (gerekirse) - **İmzalama Açık Anahtarı:** Sonda hizalı (bayt 256 ile bayt 383 arası) - **Sertifika:** Bayt 384'te başlar

**Boyut Hesaplaması:**

```
Total size = 384 + 3 + key_certificate_length

For NULL certificate (ElGamal + DSA_SHA1):
  Total = 384 + 3 = 387 bytes

For Key Certificate (EdDSA + X25519):
  Total = 384 + 3 + 4 = 391 bytes

For larger keys (e.g., RSA_4096):
  Total = 384 + 3 + 4 + excess_key_data_length
```
### Dolgu Üretimi Yönergeleri ([Öneri 161](/tr/proposals/161-ri-dest-padding/))

**Uygulama Sürümü:** 0.9.57 (Ocak 2023, sürüm 2.1.0)

**Arka plan:** - ElGamal+DSA olmayan anahtarlar için, 384 baytlık sabit yapıda dolgu bulunur - Destinations (I2P adresleri) için, 256 baytlık açık anahtar alanı 0.6'dan (2005) beri kullanılmıyor - Dolgu, güvenliği korurken sıkıştırılabilir olacak şekilde üretilmelidir

**Gereksinimler:**

1. **Asgari Rastgele Veri:**
   - En az 32 bayt kriptografik olarak güvenli rastgele veri kullanın
   - Bu, güvenlik için yeterli entropi sağlar

2. **Sıkıştırma Stratejisi:**
   - 32 baytı dolgu/açık anahtar alanı boyunca tekrarlayın
   - I2NP Database Store, Streaming SYN, SSU2 handshake gibi protokoller sıkıştırma kullanır
   - Güvenliği zedelemeden önemli bant genişliği tasarrufu

3. **Örnekler:**

**Router Kimliği (X25519 + EdDSA):**

```
Structure:
- 32 bytes X25519 public key
- 320 bytes padding (10 copies of 32-byte random data)
- 32 bytes EdDSA public key
- 7 bytes Key Certificate

Compression savings: ~288 bytes when compressed
```
**Hedef (ElGamal-unused + EdDSA):**

```
Structure:
- 256 bytes unused ElGamal field (11 copies of 32-byte random data, truncated to 256)
- 96 bytes padding (3 copies of 32-byte random data)
- 32 bytes EdDSA public key  
- 7 bytes Key Certificate

Compression savings: ~320 bytes when compressed
```
4. **Bu Neden Çalışır:**
   - Tam yapının SHA-256 hash (özet) değeri yine de tüm entropiyi içerir
   - Ağ veritabanının DHT dağıtımı yalnızca hash’e bağlıdır
   - İmzalama anahtarı (32 bayt EdDSA/X25519) 256 bit entropi sağlar
   - Tekrar eden rastgele verinin ilave 32 baytı = toplam 512 bit entropi
   - Kriptografik güç için fazlasıyla yeterli

5. **Uygulama Notları:**
   - 387+ baytlık yapının tamamını saklamalı ve iletmelidir
   - SHA-256 özeti, sıkıştırılmamış yapının tamamı üzerinden hesaplanır
   - Sıkıştırma, protokol katmanında uygulanır (I2NP, Streaming, SSU2)
   - 0.6 (2005) sürümünden bu yana tüm sürümlerle geriye dönük uyumludur

**JavaDoc:** [KeysAndCert](http://docs.i2p-projekt.de/javadoc/net/i2p/data/KeysAndCert.html)

---

### RouterIdentity (router kimliği)

**Açıklama:** I2P ağındaki bir router'ı benzersiz şekilde tanımlar. Yapısı KeysAndCert ile aynıdır.

**Biçim:** Yukarıdaki KeysAndCert yapısına bakın

**Güncel Gereksinimler (0.9.58 itibarıyla):**

1. **Zorunlu Anahtar Türleri:**
   - **Şifreleme:** X25519 (tip 4, 32 bayt)
   - **İmzalama:** EdDSA_SHA512_Ed25519 (tip 7, 32 bayt)
   - **Sertifika:** Key Certificate (tip 5)

2. **Kullanımdan Kaldırılan Anahtar Türleri:**
   - ElGamal (tip 0) 0.9.58 itibarıyla Router Kimlikleri için kullanımdan kaldırılmıştır
   - DSA_SHA1 (tip 0) 0.9.58 itibarıyla Router Kimlikleri için kullanımdan kaldırılmıştır
   - Bunlar yeni router'lar için KULLANILMAMALIDIR

3. **Tipik Boyut:**
   - X25519 + EdDSA, Anahtar Sertifikası ile = 391 bayt
   - 32 bayt X25519 açık anahtarı
   - 320 bayt dolgu ([Proposal 161](/tr/proposals/161-ri-dest-padding/)'e göre sıkıştırılabilir)
   - 32 bayt EdDSA açık anahtarı
   - 7 bayt sertifika (3 baytlık başlık + 4 baytlık anahtar türleri)

**Tarihsel Gelişim:** - 0.9.16 öncesi: Her zaman NULL sertifikası (ElGamal + DSA_SHA1) - 0.9.16-0.9.47: Anahtar Sertifikası desteği eklendi - 0.9.48+: X25519 şifreleme anahtarları desteklendi - 0.9.58+: ElGamal ve DSA_SHA1 kullanımdan kaldırıldı

**Ağ Veritabanı Anahtarı:** - RouterInfo, tam RouterIdentity'nin SHA-256 özeti ile anahtarlanır - Özet, 391+ baytlık tam yapı üzerinde (doldurma dahil) hesaplanır

**Ayrıca bakınız:** - Dolgu (padding) oluşturma yönergeleri ([Öneri 161](/tr/proposals/161-ri-dest-padding/)) - Yukarıdaki Anahtar Sertifikası belirtimi

**JavaDoc:** [RouterIdentity](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterIdentity.html)

---

### Hedef

**Açıklama:** Güvenli mesaj teslimi için uç nokta tanımlayıcısı. Yapısal olarak KeysAndCert (anahtarlar ve sertifikadan oluşan yapı) ile aynıdır, ancak kullanım semantiği farklıdır.

**Biçim:** Bkz. yukarıdaki KeysAndCert yapısı

**RouterIdentity'den kritik fark:** - **Açık anahtar alanı KULLANILMIYOR ve rastgele veri içerebilir** - Bu alan 0.6 sürümünden (2005) beri kullanılmıyor - Aslen eski I2CP-to-I2CP şifrelemesi için kullanılıyordu (devre dışı) - Şu anda yalnızca kullanımdan kaldırılmış LeaseSet şifrelemesi için IV (ilklendirme vektörü) olarak kullanılır

**Güncel Öneriler:**

1. **İmza Anahtarı:**
   - **Önerilen:** EdDSA_SHA512_Ed25519 (tür 7, 32 bayt)
   - Alternatif: Eski sürümlerle uyumluluk için ECDSA türleri
   - Kaçının: DSA_SHA1 (kullanımdan kaldırıldı, önerilmez)

2. **Şifreleme Anahtarı:**
   - Alan kullanılmıyor ancak mevcut olmalıdır
   - **Önerilir:** [Proposal 161](/tr/proposals/161-ri-dest-padding/) uyarınca rastgele verilerle doldurun (sıkıştırılabilir)
   - Boyut: Her zaman 256 bayt (ElGamal yuvası, ElGamal için kullanılmasa da)

3. **Sertifika:**
   - ElGamal + DSA_SHA1 için NULL sertifika (yalnızca eski)
   - Diğer tüm imzalama anahtarı türleri için Anahtar Sertifikası

**Tipik Modern Hedef:**

```
Structure:
- 256 bytes unused field (random data, compressible)
- 96 bytes padding (random data, compressible)
- 32 bytes EdDSA signing public key
- 7 bytes Key Certificate

Total: 391 bytes
Compression savings: ~320 bytes
```
**Gerçek Şifreleme Anahtarı:** - Destination (I2P hedef adresi) için şifreleme anahtarı **LeaseSet** içindedir, Destination'da değil - LeaseSet geçerli şifreleme genel anahtar(lar)ını içerir - Şifreleme anahtarının işlenmesi için LeaseSet2 spesifikasyonuna bakın

**Ağ Veritabanı Anahtarı:** - LeaseSet, tam Destination (hedef) değerinin SHA-256 karmasıyla anahtarlanır - Karma, 387+ baytlık yapının tamamı üzerinden hesaplanır

**JavaDoc:** [Destination](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Destination.html)

---

## Ağ Veritabanı Yapıları

### Lease (kiralama kaydı)

**Açıklama:** Belirli bir tunnel’i, bir Destination (Hedef) için mesaj almaya yetkilendirir. Orijinal LeaseSet formatının (tip 1) bir parçasıdır.

**Biçim:**

```
+----+----+----+----+----+----+----+----+
| tunnel_gw                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|     tunnel_id     |      end_date
+----+----+----+----+----+----+----+----+
                    |
+----+----+----+----+

tunnel_gw :: Hash (32 bytes)
             SHA-256 hash of the gateway RouterIdentity

tunnel_id :: TunnelId (4 bytes)
             Tunnel identifier at the gateway router

end_date :: Date (8 bytes)
            Expiration timestamp in milliseconds since epoch
```
**Toplam Boyut:** 44 bayt

**Kullanım:** - Yalnızca orijinal LeaseSet'te kullanılır (tip 1, kullanımdan kaldırılmış) - LeaseSet2 ve sonraki varyantlar için bunun yerine Lease2 kullanın

**JavaDoc:** [Lease](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Lease.html)

---

### LeaseSet (Tür 1)

**Açıklama:** Orijinal LeaseSet biçimi. Bir Destination (hedef kimlik) için yetkilendirilmiş tunnel'lar ve anahtarlar içerir. ağ veritabanında saklanır. **Durum: Kullanımdan kaldırıldı** (yerine LeaseSet2 kullanın).

**Yapı:**

```
+----+----+----+----+----+----+----+----+
| destination                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| encryption_key                        |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signing_key                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| num| Lease 0                          |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Lease 1                               |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Lease ($num-1)                        |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

destination :: Destination
               Length: 387+ bytes

encryption_key :: PublicKey (256 bytes, ElGamal)
                  Used for end-to-end ElGamal/AES+SessionTag encryption
                  Generated anew at each router startup (not persistent)

signing_key :: SigningPublicKey (128+ bytes)
               Same type as Destination signing key
               Used for LeaseSet revocation (unimplemented)
               Generated anew at each router startup (not persistent)

num :: Integer (1 byte)
       Number of Leases to follow
       Range: 0-16

leases :: Array of Lease structures
          Length: $num × 44 bytes
          Each Lease is 44 bytes

signature :: Signature (40+ bytes)
             Length determined by Destination signing key type
             Signed by Destination's SigningPrivateKey
```
**Veritabanı Depolaması:** - **Veritabanı Türü:** 1 - **Anahtar:** Hedefin SHA-256 karması - **Değer:** Tam LeaseSet yapısı

**Önemli Notlar:**

1. **Destination (I2P’de uç nokta adres nesnesi) Genel Anahtarı Kullanılmıyor:**
   - Destination içindeki şifreleme genel anahtarı alanı kullanılmıyor
   - LeaseSet içindeki şifreleme anahtarı gerçek şifreleme anahtarıdır

2. **Geçici Anahtarlar:**
   - `encryption_key` geçicidir (router başlatıldığında yeniden oluşturulur)
   - `signing_key` geçicidir (router başlatıldığında yeniden oluşturulur)
   - Her iki anahtar da yeniden başlatmalar arasında kalıcı değildir

3. **İptal (Uygulanmadı):**
   - `signing_key`, LeaseSet iptali için tasarlanmıştı
   - İptal mekanizması hiçbir zaman uygulanmadı
   - Sıfır-lease (kiralama girdisi)’li LeaseSet iptal için tasarlanmıştı ancak kullanılmıyor

4. **Sürümlendirme/Zaman damgası:**
   - LeaseSet'te açık bir `published` zaman damgası alanı yoktur
   - Sürüm, tüm lease'lerin (lease: I2P'de inbound tunnel referans kaydı) en erken sona erme zamanıdır
   - Yeni LeaseSet'in kabul edilmesi için lease sona erme zamanı daha erken olmalıdır

5. **Lease Sona Erme Bilgisinin Yayımlanması:**
   - 0.9.7 öncesi: Tüm leases (I2P’de yönlendirme için kullanılan lease girdileri) aynı sona erme zamanı (en erkeni) ile yayımlanırdı
   - 0.9.7+: Gerçek bireysel lease sona erme zamanları yayımlanır
   - Bu bir uygulama ayrıntısıdır, belirtimin parçası değildir

6. **Sıfır Leases:**
   - Sıfır Leases içeren LeaseSet teknik olarak izinlidir
   - İptal için tasarlandı (uygulanmamış)
   - Pratikte kullanılmıyor
   - LeaseSet2 varyantları en az bir Lease (I2P'de bir inbound tunnel kaydı) gerektirir

**Kullanımdan kaldırma:** LeaseSet tür 1 kullanımdan kaldırılmıştır. Yeni uygulamalar, şu özellikleri sağlayan **LeaseSet2 (tür 3)** kullanmalıdır: - Yayımlanma zaman damgası alanı (daha iyi sürümleme) - Birden fazla şifreleme anahtarı desteği - Çevrimdışı imza yeteneği - 4 baytlık lease (kiralama girdisi) sona erme süreleri (8 bayta kıyasla) - Daha esnek seçenekler

**JavaDoc:** [LeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/LeaseSet.html)

---

## LeaseSet Varyantları

### Lease2 (Lease nesnesinin ikinci sürümü)

**Açıklama:** 4 baytlık sona erme zamanı içeren geliştirilmiş lease (kiralama kaydı) biçimi. LeaseSet2 (type 3) ve MetaLeaseSet (type 7) içinde kullanılır.

**Giriş:** Sürüm 0.9.38 (bkz. [Öneri 123](/proposals/123-new-netdb-entries/))

**Biçim:**

```
+----+----+----+----+----+----+----+----+
| tunnel_gw                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|     tunnel_id     |      end_date     |
+----+----+----+----+----+----+----+----+

tunnel_gw :: Hash (32 bytes)
             SHA-256 hash of gateway RouterIdentity

tunnel_id :: TunnelId (4 bytes)
             Tunnel identifier at gateway

end_date :: 4-byte timestamp (seconds since epoch)
            Rolls over in year 2106
```
**Toplam Boyut:** 40 bayt (orijinal Lease'ten 4 bayt daha küçük)

**Orijinal Lease (I2P'de bir tunnel kiralama kaydı) ile Karşılaştırma:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1pxsolid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Lease (Type&nbsp;1)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Lease2 (Type&nbsp;3+)</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Size</td><td style="border:1px solid var(--color-border); padding:0.5rem;">44 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Expiration Size</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes (ms)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes (seconds)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Precision</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Millisecond</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Second</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Rollover</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Year&nbsp;292,277,026,596</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Year&nbsp;2106</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Used In</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet (deprecated)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2, MetaLeaseSet</td></tr>
  </tbody>
</table>
**JavaDoc:** [Lease2](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Lease2.html)

---

### Çevrimdışı İmza

**Açıklama:** Hedefin özel imzalama anahtarına çevrimiçi erişim olmadan LeaseSet yayınlanmasına olanak tanıyan, önceden imzalanmış geçici anahtarlar için isteğe bağlı bir yapı.

**Giriş:** Version 0.9.38 (bkz. [Öneri 123](/proposals/123-new-netdb-entries/))

**Biçim:**

```
+----+----+----+----+----+----+----+----+
|     expires       | sigtype |         |
+----+----+----+----+----+----+         +
|       transient_public_key            |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|           signature                   |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

expires :: 4-byte timestamp (seconds since epoch)
           Expiration of transient key validity
           Rolls over in year 2106

sigtype :: 2-byte signature type
           Type of transient_public_key (see SigningPublicKey types)

transient_public_key :: SigningPublicKey
                        Length determined by sigtype
                        Temporary signing key for LeaseSet

signature :: Signature
             Length determined by Destination's signing key type
             Signature of (expires || sigtype || transient_public_key)
             Signed by Destination's permanent SigningPrivateKey
```
**Amaç:** - Çevrimdışı LeaseSet oluşturulmasını sağlar - Destination (I2P'de uç kimliği) ana anahtarını çevrimiçi ifşadan korur - Geçici anahtar, çevrimdışı imza olmadan yeni bir LeaseSet yayımlanarak iptal edilebilir

**Kullanım Senaryoları:**

1. **Yüksek Güvenlikli Hedefler:**
   - Ana imzalama anahtarı çevrimdışı olarak saklanır (HSM, soğuk depolama)
   - Geçici anahtarlar sınırlı süreler için çevrimdışı olarak oluşturulur
   - Ele geçirilmiş bir geçici anahtar, ana imzalama anahtarını açığa çıkarmaz

2. **Şifreli LeaseSet (I2P'de bir hizmetin iletişim uç noktalarını ve anahtarlarını içeren kayıt) Yayınlama:**
   - EncryptedLeaseSet, çevrimdışı imza içerebilir
   - Körlenmiş açık anahtar + çevrimdışı imza ek güvenlik sağlar

**Güvenlik Hususları:**

1. **Sona Erme Yönetimi:**
   - Makul bir sona erme süresi belirleyin (günler ila haftalar, yıllar değil)
   - Sona ermeden önce yeni geçici anahtarlar oluşturun
   - Daha kısa sona erme süresi = daha iyi güvenlik, daha fazla bakım

2. **Anahtar Üretimi:**
   - Geçici anahtarları güvenli bir ortamda çevrimdışı oluşturun
   - Çevrimdışı olarak ana anahtarla imzalayın
   - Yalnızca imzalanmış geçici anahtarı + imzayı çevrimiçi router'a aktarın

3. **İptal:**
   - Örtük iptal için çevrimdışı imza olmadan yeni bir LeaseSet yayımlayın
   - Ya da farklı bir geçici anahtarla yeni bir LeaseSet yayımlayın

**İmza Doğrulama:**

```
Data to sign: expires (4 bytes) || sigtype (2 bytes) || transient_public_key

Verification:
1. Extract Destination from LeaseSet
2. Get Destination's SigningPublicKey
3. Verify signature over (expires || sigtype || transient_public_key)
4. Check that current time < expires
5. If valid, use transient_public_key to verify LeaseSet signature
```
**Uygulama Notları:** - Toplam boyut, imza türü ve Destination (I2P hedef kimliği) imzalama anahtarı türüne bağlı olarak değişir - Minimum boyut: 4 + 2 + 32 (EdDSA anahtarı) + 64 (EdDSA imzası) = 102 bayt - Maksimum pratik boyut: ~600 bayt (RSA-4096 geçici anahtarı + RSA-4096 imzası)

**Şunlarla uyumlu:** - LeaseSet2 (I2P'de bir adresin erişim kaydı; tip 3) - EncryptedLeaseSet (tip 5) - MetaLeaseSet (tip 7)

**Ayrıca bkz.:** Ayrıntılı çevrimdışı imza protokolü için [Öneri 123](/proposals/123-new-netdb-entries/).

---

### LeaseSet2Header

**Açıklama:** LeaseSet2 (tip 3) ve MetaLeaseSet (tip 7) için ortak başlık yapısı.

**Giriş:** Sürüm 0.9.38 (bkz. [Öneri 123](/proposals/123-new-netdb-entries/))

**Biçim:**

```
+----+----+----+----+----+----+----+----+
| destination                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|     published     | expires |  flags  |
+----+----+----+----+----+----+----+----+
| offline_signature (optional)          |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

destination :: Destination
               Length: 387+ bytes

published :: 4-byte timestamp (seconds since epoch)
             Publication time of this LeaseSet
             Rolls over in year 2106

expires :: 2-byte offset (seconds)
           Offset from published timestamp
           Maximum: 65535 seconds (18.2 hours)

flags :: 2 bytes (bit flags)
         See flag definitions below

offline_signature :: OfflineSignature (optional)
                     Present only if flags bit 0 is set
                     Variable length
```
**Minimum Toplam Boyut:** 395 bayt (çevrimdışı imza hariç)

**Bayrak Tanımları (bit sırası: 15 14 ... 3 2 1 0):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Bit</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline Keys</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0 = No offline keys, 1 = Offline signature present</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unpublished</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0 = Standard published, 1 = Unpublished (client-side only)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0 = Standard, 1 = Will be blinded when published</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3-15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Must be 0 for compatibility</td></tr>
  </tbody>
</table>
**Bayrak Ayrıntıları:**

**Bit 0 - Çevrimdışı Anahtarlar:** - `0`: Çevrimdışı imza yok, LeaseSet imzasını doğrulamak için Destination'ın imzalama anahtarını kullanın - `1`: OfflineSignature yapısı flags alanından sonra gelir

**Bit 1 - Yayınlanmamış:** - `0`: Standart yayınlanmış LeaseSet (hedefin tunnel kiralarını içeren kayıt), floodfill'lere yayılmalıdır - `1`: Yayınlanmamış LeaseSet (yalnızca istemci tarafında)   - Floodfill'lere yayılmamalı, yayınlanmamalı veya sorgulara yanıt olarak gönderilmemelidir   - Süresi dolmuşsa, yerine yenisini bulmak için netdb sorgulanmamalıdır (bit 2 de ayarlıysa hariç)   - Yerel tunnel'lar veya test için kullanılır


**Sona Erme Sınırları:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">LeaseSet Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Maximum Expires Value</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Maximum Actual Time</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2 (type 3)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈660 seconds</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈11 minutes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MetaLeaseSet (type 7)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">65,535 seconds</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈18.2 hours</td></tr>
  </tbody>
</table>
**Yayınlanma Zaman Damgası Gereksinimleri:**

LeaseSet (tip 1) bir published alanına sahip değildi; sürümleme için en erken lease (kiralama) sona erme zamanını aramayı gerektiriyordu. LeaseSet2, 1 saniyelik çözünürlükle açıkça belirtilmiş bir `published` zaman damgası ekler.

**Kritik Uygulama Notu:** - Routers, Destination başına LeaseSet yayın hızını **saniyede birden çok daha yavaş** olacak şekilde sınırlamak zorundadır - Daha hızlı yayınlanıyorsa, her yeni LeaseSet'in `published` zamanının en az 1 saniye daha sonra olduğundan emin olun - Floodfills, `published` zamanı mevcut sürümden daha yeni değilse LeaseSet'i reddedecektir - Önerilen asgari aralık: yayınlar arasında 10-60 saniye

**Hesaplama Örnekleri:**

**LeaseSet2 (en fazla 11 dakika):**

```
published = 1704067200 (2024-01-01 00:00:00 UTC)
expires = 660 (seconds)
Actual expiration = 1704067200 + 660 = 1704067860 (2024-01-01 00:11:00 UTC)
```
**MetaLeaseSet (en fazla 18,2 saat):**

```
published = 1704067200 (2024-01-01 00:00:00 UTC)
expires = 65535 (seconds)
Actual expiration = 1704067200 + 65535 = 1704132735 (2024-01-01 18:12:15 UTC)
```
**Sürümleme:** - `published` zaman damgası daha büyükse LeaseSet "daha yeni" kabul edilir - Floodfills yalnızca en yeni sürümü depolar ve yayar - En eski Lease (kiralama kaydı) önceki LeaseSet'in en eski Lease'i ile eşleştiğinde dikkat edin

---

### LeaseSet2 (Tür 3)

**Açıklama:** Birden çok şifreleme anahtarı, çevrimdışı imzalar ve hizmet kayıtlarını destekleyen modern LeaseSet biçimi. I2P gizli hizmetleri için güncel standarttır.

**Giriş:** Sürüm 0.9.38 (bkz. [Öneri 123](/proposals/123-new-netdb-entries/))

**Yapı:**

```
+----+----+----+----+----+----+----+----+
|         ls2_header                    |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|          options                      |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|numk| keytype0| keylen0 |              |
+----+----+----+----+----+              +
|          encryption_key_0             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| keytypen| keylenn |                   |
+----+----+----+----+                   +
|          encryption_key_n             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| num| Lease2 0                         |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Lease2($num-1)                        |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

ls2header :: LeaseSet2Header
             Length: 395+ bytes (varies with offline signature)

options :: Mapping
           Key-value pairs for service records and metadata
           Length: 2+ bytes (size field + data)

numk :: Integer (1 byte)
        Number of encryption keys
        Range: 1 to (implementation-defined maximum, typically 8)

keytype :: 2-byte encryption type
           See PublicKey type table

keylen :: 2-byte key length
          Must match keytype specification

encryption_key :: PublicKey
                  Length: keylen bytes
                  Type: keytype

[Repeat keytype/keylen/encryption_key for each key]

num :: Integer (1 byte)
       Number of Lease2s
       Range: 1-16 (at least one required)

leases :: Array of Lease2 structures
          Length: $num × 40 bytes

signature :: Signature
             Length determined by signing key type
             Signed over entire structure including database type prefix
```
**Veritabanı Depolaması:** - **Veritabanı Türü:** 3 - **Anahtar:** Destination (I2P'de hedef kimlik) öğesinin SHA-256 karması - **Değer:** Tam LeaseSet2 yapısı

**İmza Hesaplaması:**

```
Data to sign: database_type (1 byte, value=3) || complete LeaseSet2 data

Verification:
1. Prepend database type byte (0x03) to LeaseSet2 data
2. If offline signature present:
   - Verify offline signature against Destination key
   - Verify LeaseSet2 signature against transient key
3. Else:
   - Verify LeaseSet2 signature against Destination key
```
### Şifreleme Anahtarı Tercih Sırası

**Yayımlanmış (Sunucu) LeaseSet için:** - Anahtarlar sunucunun tercih sırasına göre listelenir (en çok tercih edilen en başta) - Birden fazla türü destekleyen istemciler sunucu tercihine UYMALIDIR - Listeden desteklenen ilk türü seçin - Genel olarak, numarası daha yüksek (daha yeni) anahtar türleri daha güvenli/verimlidir - Önerilen sıra: Anahtarları tür koduna göre ters sırada listeleyin (en yenisi en başta)

**Örnek Sunucu Tercihi:**

```
numk = 2
Key 0: X25519 (type 4, 32 bytes)         [Most preferred]
Key 1: ElGamal (type 0, 256 bytes)       [Legacy compatibility]
```
**Yayınlanmamış (İstemci) LeaseSet için:** - Anahtar sırası pratikte önemli değildir (istemcilere bağlantı denemeleri nadirdir) - Tutarlılık için aynı kurala uyun

**İstemci Anahtarı Seçimi:** - Sunucu tercihini esas al (desteklenen ilk türü seç) - Ya da uygulama tarafından tanımlanan tercihi kullan - Ya da her iki tarafın yeteneklerine dayanarak ortak bir tercih belirle

### Seçenek Eşlemesi

**Gereksinimler:** - Seçenekler anahtara göre MUTLAKA sıralanmalıdır (leksikografik, UTF-8 bayt sırası) - Sıralama, imzanın değişmezliğini sağlar - Yinelenen anahtarlara İZİN VERİLMEZ

**Standart Format ([Öneri 167](/proposals/167-service-records/)):**

API 0.9.66 (Haziran 2025, 2.9.0 sürümü) itibarıyla, service record (hizmet kaydı) seçenekleri standart bir biçime uyar. Tam spesifikasyon için [Proposal 167](/proposals/167-service-records/) belgesine bakın.

**Servis Kaydı Seçenek Biçimi:**

```
Key: _service._proto
Value: record_type ttl [priority weight] port target [appoptions]

service :: Symbolic name of service (lowercase, [a-z0-9-])
           Examples: smtp, http, irc, mumble
           Use standard identifiers from IANA Service Name Registry
           or Linux /etc/services when available

proto :: Transport protocol (lowercase, [a-z0-9-])
         "tcp" = streaming protocol
         "udp" = repliable datagrams
         Protocol indicators for raw datagrams may be defined later

record_type :: "0" (self-reference) or "1" (SRV record)

ttl :: Time to live in seconds (positive integer)
       Recommended minimum: 86400 (one day)
       Prevents frequent re-queries

For record_type = 0 (self-reference):
  port :: I2CP port number (non-negative integer)
  appoptions :: Optional application-specific data (no spaces or commas)

For record_type = 1 (SRV record):
  priority :: Lower value = more preferred (non-negative integer)
  weight :: Relative weight for same priority, higher = more likely (non-negative)
  port :: I2CP port number (non-negative integer)
  target :: Hostname or b32 of destination (lowercase)
            Format: "example.i2p" or "aaaaa...aaaa.b32.i2p"
            Recommend b32 unless hostname is "well known"
  appoptions :: Optional application-specific data (no spaces or commas)
```
**Örnek Hizmet Kayıtları:**

**1. Kendi Kendine Referans Veren SMTP Sunucusu:**

```
Destination: aaaa...aaaa.b32.i2p (this LeaseSet)
Option: "_smtp._tcp" = "0 999999 25"

Meaning: This destination provides SMTP service on I2CP port 25
```
**2. Tek Harici SMTP Sunucusu:**

```
Destination: aaaa...aaaa.b32.i2p (this LeaseSet)
Option: "_smtp._tcp" = "1 86400 0 0 25 bbbb...bbbb.b32.i2p"

Meaning: SMTP service provided by bbbb...bbbb on port 25
         TTL = 1 day, single server (priority=0, weight=0)
```
**3. Birden Fazla SMTP Sunucusu (Yük Dengeleme):**

```
Destination: aaaa...aaaa.b32.i2p (this LeaseSet)
Option: "_smtp._tcp" = "1 86400 0 0 25 bbbb...bbbb.b32.i2p,1 86400 1 0 25 cccc...cccc.b32.i2p"

Meaning: Two SMTP servers
         bbbb...bbbb (priority=0, preferred)
         cccc...cccc (priority=1, backup)
```
**4. Uygulama Seçenekleri ile HTTP Hizmeti:**

```
Option: "_http._tcp" = "0 86400 80 tls=1.3;cert=ed25519"

Meaning: HTTP on port 80 with TLS 1.3 and EdDSA certificates
```
**TTL (yaşam süresi) Önerileri:** - En az: 86400 saniye (1 gün) - Daha uzun TTL, netdb sorgu yükünü azaltır - Sorgu azaltımı ile hizmet güncellemelerinin yayılımı arasında denge - Kararlı hizmetler için: 604800 (7 gün) veya daha uzun

**Uygulama Notları:**

1. **Şifreleme Anahtarları (0.9.44 itibarıyla):**
   - ElGamal (tip 0, 256 bayt): Eski sürümlerle uyumluluk
   - X25519 (tip 4, 32 bayt): Güncel standart
   - MLKEM varyantları: Kuantum sonrası (beta, henüz kesinleşmedi)

2. **Anahtar Uzunluğu Doğrulaması:**
   - Floodfill düğümleri ve istemciler bilinmeyen anahtar türlerini ayrıştırabilmek zorundadır
   - Bilinmeyen anahtarları atlamak için keylen alanını kullanın
   - Anahtar türü bilinmiyorsa ayrıştırma başarısız olmamalıdır

3. **Yayınlanan Zaman Damgası:**
   - Hız sınırlamasıyla ilgili LeaseSet2Header notlarına bakın
   - Yayınlar arasında en az 1 saniyelik artış gereklidir
   - Önerilen: Yayınlar arasında 10-60 saniye

4. **Şifreleme Türü Geçişi:**
   - Birden çok anahtar, kademeli geçişi destekler
   - Geçiş döneminde hem eski hem de yeni anahtarları listeleyin
   - Yeterli bir istemci yükseltme süresi geçtikten sonra eski anahtarı kaldırın

**JavaDoc:** [LeaseSet2](http://docs.i2p-projekt.de/javadoc/net/i2p/data/LeaseSet2.html)

---

### MetaLease

**Açıklama:** MetaLeaseSet (özel bir leaseSet türü) için, tunnels yerine diğer LeaseSets'e başvurabilen bir Lease yapısı. Yük dengeleme ve yedeklilik için kullanılır.

**Giriş:** Sürüm 0.9.38, 0.9.40’ta çalışması planlanıyor (bkz. [Öneri 123](/proposals/123-new-netdb-entries/))

**Biçim:**

```
+----+----+----+----+----+----+----+----+
| tunnel_gw                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|    flags     |cost|      end_date     |
+----+----+----+----+----+----+----+----+

tunnel_gw :: Hash (32 bytes)
             SHA-256 hash of:
             - Gateway RouterIdentity (for type 1), OR
             - Another MetaLeaseSet destination (for type 3/5/7)

flags :: 3 bytes
         Bit order: 23 22 ... 3 2 1 0
         Bits 3-0: Entry type (see table below)
         Bits 23-4: Reserved (must be 0)

cost :: 1 byte (0-255)
        Lower value = higher priority
        Used for load balancing

end_date :: 4-byte timestamp (seconds since epoch)
            Expiration time
            Rolls over in year 2106
```
**Toplam Boyut:** 40 bayt

**Girdi Türü (bayrak bitleri 3-0):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Unknown</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unknown/invalid entry</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Points to LeaseSet (type 1, deprecated)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Points to LeaseSet2 (type 3)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Points to EncryptedLeaseSet (type 5)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MetaLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align-center?">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Points to another MetaLeaseSet (type 7)</td></tr>
  </tbody>
</table>
**Kullanım Senaryoları:**

1. **Yük Dengeleme:**
   - Birden çok MetaLease (tekil kiralama girdisi) girdisi içeren MetaLeaseSet (I2P'de üst düzey LeaseSet türü)
   - Her bir girdi farklı bir LeaseSet2'ye işaret eder
   - İstemciler cost alanına göre seçim yapar

2. **Yedeklilik:**
   - Yedek leaseSet'lere (I2P’de bir hedefin kullanılabilir giriş tünellerini tanımlayan veri kümesi) işaret eden birden çok kayıt
   - Birincil leaseSet kullanılamadığında geri dönüş

3. **Hizmet Geçişi:**
   - MetaLeaseSet (LeaseSet'leri meta düzeyde tanımlayan yapı) yeni LeaseSet'e işaret eder
   - Destinations (I2P'de hedef kimlik/adresler) arasında sorunsuz geçişe olanak tanır

**Maliyet Alanı Kullanımı:** - Daha düşük maliyet = daha yüksek öncelik - Maliyet 0 = en yüksek öncelik - Maliyet 255 = en düşük öncelik - İstemciler daha düşük maliyetli kayıtları tercih etmelidir - Eş maliyetli kayıtlar rastgele olarak yük dengelenebilir

**Lease2 ile karşılaştırma:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Lease2</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">MetaLease</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Size</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Tunnel ID</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Replaced by flags (3 bytes) + cost (1 byte)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Points To</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specific tunnel</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet or MetaLeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Usage</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Direct tunnel reference</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Indirection/load balancing</td></tr>
  </tbody>
</table>
**JavaDoc:** [MetaLease](http://docs.i2p-projekt.de/javadoc/net/i2p/data/MetaLease.html)

---

### MetaLeaseSet (leaseSet'ler için meta küme, Tür 7)

**Açıklama:** Diğer LeaseSet'lere dolaylı yönlendirme sağlayan MetaLease (bir giriş türü) girdileri içeren bir LeaseSet varyantı. Yük dengeleme, yedeklilik ve hizmet geçişi için kullanılır.

**Giriş:** 0.9.38'de tanımlandı, 0.9.40'ta çalışır hâle gelmesi planlandı (bkz. [Öneri 123](/proposals/123-new-netdb-entries/))

**Durum:** Spesifikasyon tamamlandı. Üretim ortamına dağıtım durumu, mevcut I2P sürümleriyle doğrulanmalıdır.

**Yapı:**

```
+----+----+----+----+----+----+----+----+
|         ls2_header                    |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|          options                      |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| num| MetaLease 0                      |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| MetaLease($num-1)                     |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|numr|                                  |
+----+                                  +
|          revocation_0                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|          revocation_n                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

ls2header :: LeaseSet2Header
             Length: 395+ bytes

options :: Mapping
           Length: 2+ bytes (size + data)
           MUST be sorted by key

num :: Integer (1 byte)
       Number of MetaLease entries
       Range: 1 to (implementation-defined, recommend 1-16)

metaleases :: Array of MetaLease structures
              Length: $num × 40 bytes

numr :: Integer (1 byte)
        Number of revocation hashes
        Range: 0 to (implementation-defined, recommend 0-16)

revocations :: Array of Hash structures
               Length: $numr × 32 bytes
               SHA-256 hashes of revoked LeaseSet Destinations
```
**Veritabanı Depolaması:** - **Veritabanı Türü:** 7 - **Anahtar:** Destination (I2P hedef kimliği) değerinin SHA-256 özeti - **Değer:** Tam MetaLeaseSet yapısı

**İmzanın Hesaplanması:**

```
Data to sign: database_type (1 byte, value=7) || complete MetaLeaseSet data

Verification:
1. Prepend database type byte (0x07) to MetaLeaseSet data
2. If offline signature present in header:
   - Verify offline signature against Destination key
   - Verify MetaLeaseSet signature against transient key
3. Else:
   - Verify MetaLeaseSet signature against Destination key
```
**Kullanım Senaryoları:**

**1. Yük Dengeleme:**

```
MetaLeaseSet for primary.i2p:
  MetaLease 0: cost=0, points to server1.i2p LeaseSet2
  MetaLease 1: cost=0, points to server2.i2p LeaseSet2
  MetaLease 2: cost=0, points to server3.i2p LeaseSet2

Clients randomly select among equal-cost entries
```
**2. Failover (hata durumunda devretme):**

```
MetaLeaseSet for service.i2p:
  MetaLease 0: cost=0, points to primary.i2p LeaseSet2
  MetaLease 1: cost=100, points to backup.i2p LeaseSet2

Clients prefer cost=0 (primary), fall back to cost=100 (backup)
```
**3. Hizmet Geçişi:**

```
MetaLeaseSet for old-domain.i2p:
  MetaLease 0: cost=0, points to new-domain.i2p LeaseSet2

Transparently redirects clients from old to new destination
```
**4. Çok Katmanlı Mimari:**

```
MetaLeaseSet for service.i2p:
  MetaLease 0: cost=0, points to region1-meta.i2p (another MetaLeaseSet)
  MetaLease 1: cost=0, points to region2-meta.i2p (another MetaLeaseSet)

Each region MetaLeaseSet points to regional servers
Allows hierarchical load balancing
```
**İptal Listesi:**

Geri çekme listesi, MetaLeaseSet (özel bir LeaseSet türü)'in daha önce yayımlanmış LeaseSet'leri açıkça geri çekmesine olanak tanır:

- **Amaç:** Belirli Destination (I2P hedefi) öğelerini artık geçersiz olarak işaretlemek
- **İçerik:** İptal edilmiş Destination yapılarına ait SHA-256 özetleri
- **Kullanım:** İstemciler, Destination özet değeri iptal listesinde yer alan LeaseSet'leri KULLANMAMALIDIR
- **Tipik Değer:** Çoğu kurulumda Boş (numr=0)

**İptal Örneği:**

```
Service migrates from dest-v1.i2p to dest-v2.i2p:
  MetaLease 0: points to dest-v2.i2p
  Revocations: [hash(dest-v1.i2p)]

Clients will use v2 and ignore v1 even if cached
```
**Sona Erme Yönetimi:**

MetaLeaseSet, expires=65535 saniye (~18,2 saat) azami değeriyle LeaseSet2Header kullanır:

- LeaseSet2'den çok daha uzun (en fazla ~11 dakika)
- Nispeten statik dolaylı adresleme için uygundur
- Başvurulan LeaseSet'lerin geçerlilik süresi daha kısa olabilir
- İstemciler, hem MetaLeaseSet'in hem de başvurulan LeaseSet'lerin geçerlilik sürelerini kontrol etmelidir

**Seçenek Eşlemesi:**

- LeaseSet2 options ile aynı formatı kullanın
- Hizmet kayıtlarını içerebilir ([Öneri 167](/proposals/167-service-records/))
- Anahtara göre sıralanmış OLMALIDIR
- Hizmet kayıtları genellikle indirection structure (dolaylama yapısı) yerine nihai hizmeti tanımlar

**İstemci Gerçekleme Notları:**

1. **Çözümleme Süreci:**
   ```
   1. Query netdb for MetaLeaseSet using SHA-256(Destination)
   2. Parse MetaLeaseSet, extract MetaLease entries
   3. Sort entries by cost (lower = better)
   4. For each entry in cost order:
      a. Extract LeaseSet hash from tunnel_gw field
      b. Determine entry type from flags
      c. Query netdb for referenced LeaseSet (may be another MetaLeaseSet)
      d. Check revocation list
      e. Check expiration
      f. If valid, use the LeaseSet; else try next entry
   ```

2. **Önbellekleme:**
   - Hem MetaLeaseSet (diğer LeaseSet'lere referans veren üst düzey kayıt) hem de referans verilen LeaseSet'leri önbelleğe al
   - Her iki düzeyin süresinin dolup dolmadığını kontrol et
   - Güncellenmiş MetaLeaseSet'in yayınlanmasını izle

3. **Failover (yedek devreye alma):**
   - Tercih edilen kayıt başarısız olursa, bir sonraki en düşük maliyetli olanı deneyin
   - Başarısız olan kayıtları geçici olarak kullanılamaz olarak işaretlemeyi düşünün
   - İyileşme için periyodik olarak yeniden kontrol edin

**Uygulama Durumu:**

[Öneri 123](/proposals/123-new-netdb-entries/), bazı bölümlerin "geliştirme aşamasında" kaldığını belirtir. Uygulayıcılar şunları yapmalıdır: - Hedef I2P sürümünde üretime uygunluğunu doğrulayın - Dağıtımdan önce MetaLeaseSet desteğini test edin - Daha yeni I2P sürümlerinde güncellenmiş spesifikasyonları kontrol edin

**JavaDoc:** [MetaLeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/MetaLeaseSet.html)

---

### EncryptedLeaseSet (Tip 5)

**Açıklama:** Geliştirilmiş gizlilik için şifrelenmiş ve körleştirilmiş LeaseSet. Yalnızca körleştirilmiş açık anahtar ve üstveri görünür; gerçek lease kayıtları (I2P'de tünel kiralama kayıtları) ve şifreleme anahtarları şifrelenmiştir.

**Giriş:** 0.9.38'de tanımlandı, 0.9.39'da çalışır durumda (bkz. [Öneri 123](/proposals/123-new-netdb-entries/))

**Yapı:**

```
+----+----+----+----+----+----+----+----+
| sigtype |                             |
+----+----+                             +
|        blinded_public_key             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|     published     | expires |  flags  |
+----+----+----+----+----+----+----+----+
| offline_signature (optional)          |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|  len    |                             |
+----+----+                             +
|         encrypted_data                |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

sigtype :: 2-byte signature type
           Type of blinded_public_key
           MUST be RedDSA_SHA512_Ed25519 (type 11)

blinded_public_key :: SigningPublicKey (32 bytes for RedDSA)
                      Blinded version of Destination signing key
                      Used to verify signature on EncryptedLeaseSet

published :: 4-byte timestamp (seconds since epoch)
             Publication time
             Rolls over in year 2106

expires :: 2-byte offset (seconds)
           Offset from published
           Maximum: 65535 seconds (18.2 hours)
           Practical maximum for LeaseSet data: ~660 seconds (~11 min)

flags :: 2 bytes
         Bit 0: Offline signature present (0=no, 1=yes)
         Bit 1: Unpublished (0=published, 1=client-side only)
         Bits 15-2: Reserved (must be 0)

offline_signature :: OfflineSignature (optional)
                     Present only if flags bit 0 = 1
                     Variable length

len :: 2-byte integer
       Length of encrypted_data
       Range: 1 to 65535

encrypted_data :: Encrypted payload
                  Length: len bytes
                  Contains encrypted LeaseSet2 or MetaLeaseSet

signature :: Signature (64 bytes for RedDSA)
             Length determined by sigtype
             Signed by blinded_public_key or transient key
```
**Veritabanı Depolaması:** - **Veritabanı Türü:** 5 - **Anahtar:** **körleştirilmiş Destination**'ın (I2P'deki 'Destination', yani hedef tanımlayıcı) (orijinal Destination değil) SHA-256 karması - **Değer:** Tam EncryptedLeaseSet (şifreli LeaseSet) yapısı

**LeaseSet2 (I2P'de bir hedefin bağlantı/erişim bilgilerini içeren kayıt biçiminin 2. sürümü) ile karşılaştırıldığında kritik farklar:**

1. **LeaseSet2Header yapısını KULLANMAZ** (benzer alanlar vardır ancak düzeni farklıdır)
2. **Körleştirilmiş açık anahtar** tam Destination (I2P'de hedef kimliği) yerine
3. **Şifrelenmiş yük** açık metin lease'ler ve anahtarlar yerine
4. **Veritabanı anahtarı, körleştirilmiş Destination'ın karmasıdır**, orijinal Destination değil

**İmza Hesaplaması:**

```
Data to sign: database_type (1 byte, value=5) || complete EncryptedLeaseSet data

Verification:
1. Prepend database type byte (0x05) to EncryptedLeaseSet data
2. If offline signature present (flags bit 0 = 1):
   - Verify offline signature against blinded public key
   - Verify EncryptedLeaseSet signature against transient key
3. Else:
   - Verify EncryptedLeaseSet signature against blinded public key
```
**İmza Türü Gereksinimi:**

**RedDSA_SHA512_Ed25519 (tip 11) MUTLAKA kullanılmalıdır:** - 32 baytlık körleştirilmiş açık anahtarlar - 64 baytlık imzalar - Körleştirme güvenlik özellikleri için gereklidir - Bkz. [Red25519 spesifikasyonu](//docs/specs/red25519-signature-scheme/

**EdDSA'dan Temel Farklar:** - Özel anahtarlar modüler indirgeme ile üretilir (clamping [anahtar bitlerinin sabit bir kalıba göre ayarlanması] değil) - İmzalar 80 bayt rastgele veri içerir - Açık anahtarları doğrudan kullanır (özetler değil) - Güvenli körleme işlemini mümkün kılar

**Körleme ve Şifreleme:**

Tam ayrıntılar için [EncryptedLeaseSet spesifikasyonu](/docs/specs/encryptedleaseset/) bölümüne bakın:

**1. Anahtar Körleme:**

```
Blinding process (daily rotation):
  secret = HKDF(original_signing_private_key, date_string, "i2pblinding1")
  alpha = SHA-256(secret) mod L (where L is Ed25519 group order)
  blinded_private_key = alpha * original_private_key
  blinded_public_key = alpha * original_public_key
```
**2. Veritabanı Konumu:**

```
Client publishes to:
  Key = SHA-256(blinded_destination)
  
Where blinded_destination uses:
  - Blinded public key (signing key)
  - Same unused public key field (random)
  - Same certificate structure
```
**3. Şifreleme Katmanları (Üç Katmanlı):**

**Katman 1 - Kimlik Doğrulama Katmanı (İstemci Erişimi):** - Şifreleme: ChaCha20 akış şifreleme algoritması - Anahtar türetimi: Her istemciye özel sırlarla HKDF - Kimliği doğrulanmış istemciler dış katmanın şifresini çözebilir

**Katman 2 - Şifreleme Katmanı:** - Şifreleme: ChaCha20 - Anahtar: İstemci ile sunucu arasındaki DH (Diffie-Hellman anahtar değişimi) üzerinden türetilir - Asıl LeaseSet2 veya MetaLeaseSet içerir

**Katman 3 - İç LeaseSet:** - Eksiksiz LeaseSet2 veya MetaLeaseSet - Tüm tunnels, şifreleme anahtarları ve seçenekleri içerir - Yalnızca başarıyla şifre çözüldükten sonra erişilebilir

**Şifreleme Anahtarı Türetimi:**

```
Client has: ephemeral_client_private_key
Server has: ephemeral_server_public_key (in encrypted_data)

Shared secret = X25519(client_private, server_public)
Encryption key = HKDF(shared_secret, context_info, "i2pblinding2")
```
**Keşif Süreci:**

**Yetkili istemciler için:**

```
1. Client knows original Destination
2. Client computes current blinded Destination (based on current date)
3. Client computes database key: SHA-256(blinded_destination)
4. Client queries netdb for EncryptedLeaseSet using blinded key
5. Client decrypts layer 1 using authorization credentials
6. Client decrypts layer 2 using DH shared secret
7. Client extracts inner LeaseSet2/MetaLeaseSet
8. Client uses tunnels from inner LeaseSet for communication
```
**Yetkisiz istemciler için:** - EncryptedLeaseSet'i bulsalar bile şifresini çözemezler - Körleştirilmiş sürümden orijinal Destination'ı belirleyemezler - Farklı körleştirme dönemleri boyunca EncryptedLeaseSet'leri ilişkilendiremezler (günlük rotasyon)

**Sona Erme Zamanları:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Content Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Maximum Expires</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet (outer)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">65,535 sec (≈18.2 hr)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Full 2-byte expires field</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Inner LeaseSet2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈660 sec (≈11 min)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Actual lease data practical maximum</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Inner MetaLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">65,535 sec (≈18.2 hr)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Indirection can be longer-lived</td></tr>
  </tbody>
</table>
**Yayınlanma Zaman Damgası:**

LeaseSet2Header ile aynı gereksinimler: - Yayınlar arasında en az 1 saniye artış olmalıdır - Floodfills, mevcut sürümden daha yeni değilse reddeder - Önerilen: yayınlar arasında 10-60 saniye

**Şifreli LeaseSets ile Çevrimdışı İmzalar:**

Çevrimdışı imzalar kullanılırken özel hususlar:
- Körleştirilmiş açık anahtar günlük olarak yenilenir
- Çevrimdışı imza, yeni körleştirilmiş anahtarla günlük olarak yeniden oluşturulmalıdır
- VEYA çevrimdışı imzayı dıştaki EncryptedLeaseSet yerine içteki LeaseSet üzerinde kullanın
- Bkz. [Proposal 123](/proposals/123-new-netdb-entries/) notları

**Uygulama Notları:**

1. **İstemci Yetkilendirmesi:**
   - Birden fazla istemci farklı anahtarlarla yetkilendirilebilir
   - Her yetkilendirilmiş istemci benzersiz şifre çözme kimlik bilgilerine sahiptir
   - Yetkilendirme anahtarları değiştirilerek istemcinin yetkisi geri alınabilir

2. **Günlük Anahtar Rotasyonu:**
   - Körleştirilmiş anahtarlar her gün UTC'de gece yarısında değişir
   - İstemciler körleştirilmiş Destination (hedef) değerini günlük olarak yeniden hesaplamalıdır
   - Eski EncryptedLeaseSet'ler rotasyondan sonra keşfedilemez hale gelir

3. **Gizlilik Özellikleri:**
   - Floodfills orijinal Destination (I2P hedef kimliği) tespit edemez
   - Yetkisiz istemciler hizmete erişemez
   - Farklı blinding periods (körleştirme dönemleri) ilişkilendirilemez
   - Sona erme süreleri dışında şifresiz üstveri yoktur

4. **Performans:**
   - İstemciler günlük körleştirme hesaplamasını yapmalıdır
   - Üç katmanlı şifreleme ek hesaplama yükü getirir
   - Şifre çözülmüş iç LeaseSet'i önbelleğe almayı düşünün

**Güvenlik Hususları:**

1. **Yetkilendirme Anahtarı Yönetimi:**
   - İstemci yetkilendirme kimlik bilgilerini güvenli bir şekilde dağıtın
   - İnce taneli geri alma için her istemciye benzersiz kimlik bilgileri kullanın
   - Yetkilendirme anahtarlarını periyodik olarak döndürün

2. **Saat Eşzamanlaması:**
   - Günlük körleme, eşzamanlı UTC tarihlerine bağlıdır
   - Saat sapması, sorgu başarısızlıklarına neden olabilir
   - Tolerans için önceki/ertesi günün körlemesini desteklemeyi düşünün

3. **Metaveri Sızıntısı:**
   - Published ve expires alanları açık metindir
   - Örüntü analizi servisin özelliklerini ortaya çıkarabilir
   - Endişeleniyorsanız yayımlama aralıklarını rastgeleleştirin

**JavaDoc:** [EncryptedLeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/EncryptedLeaseSet.html)

---

## Router Yapıları

### RouterAddress (router adresi)

**Açıklama:** Belirli bir taşıma protokolü üzerinden bir router için bağlantı bilgilerini tanımlar.

**Biçim:**

```
+----+----+----+----+----+----+----+----+
|cost|           expiration
+----+----+----+----+----+----+----+----+
     |        transport_style           |
+----+----+----+----+-//-+----+----+----+
|                                       |
+                                       +
|               options                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

cost :: Integer (1 byte)
        Relative cost, 0=free, 255=expensive
        Typical values:
          5-6: SSU2
          10-11: NTCP2

expiration :: Date (8 bytes)
              MUST BE ALL ZEROS (see critical note below)

transport_style :: String (1-256 bytes)
                   Transport protocol name
                   Current values: "SSU2", "NTCP2"
                   Legacy: "SSU", "NTCP" (removed)

options :: Mapping
           Transport-specific configuration
           Common options: "host", "port"
           Transport-specific options vary
```
**KRİTİK - Sona Erme Alanı:**

⚠️ **expiration alanı MUTLAKA tamamı sıfır (8 sıfır bayt) olarak ayarlanmalıdır.**

- **Gerekçe:** Sürüm 0.9.3'ten beri, Expiration alanının sıfırdan farklı olması imza doğrulama hatasına neden oluyor
- **Geçmiş:** Expiration alanı başlangıçta kullanılmıyordu, her zaman null idi
- **Güncel Durum:** Alan 0.9.12 itibarıyla yeniden tanındı, ancak ağ yükseltmesinin beklenmesi gerekiyor
- **Uygulama:** Her zaman 0x0000000000000000 olarak ayarlayın

Herhangi bir sıfırdan farklı sona erme değeri, RouterInfo (I2P router'ına ait bilgi kaydı) imzasının doğrulamada başarısız olmasına neden olur.

### Taşıma Protokolleri

**Güncel Protokoller (2.10.0 itibarıyla):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Introduced</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Removed</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>SSU2</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.54 (May 2022)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Default since 0.9.56</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>NTCP2</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.36 (Aug 2018)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.50 (May 2021)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Use NTCP2</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2.4.0 (Dec 2023)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Use SSU2</td></tr>
  </tbody>
</table>
**Taşıma Stili Değerleri:** - `SSU2`: Güncel UDP tabanlı taşıma - `NTCP2`: Güncel TCP tabanlı taşıma - `NTCP`: Eski, kaldırıldı (kullanmayın) - `SSU`: Eski, kaldırıldı (kullanmayın)

### Genel Seçenekler

Tüm taşıma protokolleri genellikle şunları içerir:

```
"host" = IPv4 or IPv6 address or hostname
"port" = Port number (1-65535)
```
### SSU2'ye Özel Seçenekler

Tüm ayrıntılar için bkz: [SSU2 spesifikasyonu](/docs/specs/ssu2/) (I2P'nin UDP tabanlı taşıma protokolünün 2. sürümü).

**Gerekli Seçenekler:**

```
"host" = IP address (IPv4 or IPv6)
"port" = UDP port number
"s" = Static X25519 public key (Base64, 44 characters = 32 bytes)
"i" = Introduction key X25519 (Base64, 44 characters = 32 bytes)
"v" = "2" (protocol version)
```
**İsteğe Bağlı Seçenekler:**

```
"caps" = Capability string (e.g., "B" for bandwidth tier)
"ihost0", "ihost1", ... = Introducer IP addresses
"iport0", "iport1", ... = Introducer ports  
"ikey0", "ikey1", ... = Introducer static keys (Base64, 44 chars)
"itag0", "itag1", ... = Introducer relay tags
"iexp0", "iexp1", ... = Introducer expiration timestamps
"mtu" = Maximum transmission unit (default 1500, min 1280)
"mtu6" = IPv6 MTU (if different from IPv4)
```
**SSU2 RouterAddress (yöneltici adresi) Örneği:**

```
cost: 5
expiration: 0x0000000000000000
transport_style: "SSU2"
options:
  host=198.51.100.42
  port=12345
  s=SGVsbG8gV29ybGQhIFRoaXMgaXMgYSBzYW1wbGUga2V5IQ==
  i=QW5vdGhlciBTYW1wbGUgS2V5IGZvciBJbnRyb2R1Y3Rpb24=
  v=2
  caps=BC
  mtu=1472
```
### NTCP2'ye Özgü Seçenekler

Tam ayrıntılar için [NTCP2 spesifikasyonuna](/docs/specs/ntcp2/) bakın.

**Zorunlu Seçenekler:**

```
"host" = IP address (IPv4 or IPv6)
"port" = TCP port number
"s" = Static X25519 public key (Base64, 44 characters = 32 bytes)
"i" = Initialization vector (Base64, 24 characters = 16 bytes)
"v" = "2" (protocol version)
```
**İsteğe Bağlı Seçenekler (0.9.50'den beri):**

```
"caps" = Capability string
```
**Örnek NTCP2 RouterAddress:**

```
cost: 10
expiration: 0x0000000000000000
transport_style: "NTCP2"
options:
  host=198.51.100.42
  port=23456
  s=SGVsbG8gV29ybGQhIFRoaXMgaXMgYSBzYW1wbGUga2V5IQ==
  i=U2FtcGxlIElWIGhlcmU=
  v=2
```
### Uygulama Notları

1. **Maliyet Değerleri:**
   - UDP (SSU2) verimliliği nedeniyle genellikle daha düşük maliyetlidir (5-6)
   - TCP (NTCP2) ek yük nedeniyle genellikle daha yüksek maliyetlidir (10-11)
   - Daha düşük maliyet = tercih edilen taşıma

2. **Birden Fazla Adres:**
   - Router'lar birden fazla RouterAddress (router adresi) girdisi yayımlayabilir
   - Farklı taşıma protokolleri (SSU2 ve NTCP2)
   - Farklı IP sürümleri (IPv4 ve IPv6)
   - İstemciler maliyete ve yeteneklere göre seçer

3. **Ana makine adı (hostname) vs IP:**
   - Performans açısından IP adresleri tercih edilir
   - Ana makine adları desteklenir ancak DNS çözümleme ek yükü getirir
   - Yayımlanan RouterInfo'lar için IP kullanmayı düşünün

4. **Base64 Kodlama:**
   - Tüm anahtarlar ve ikili veriler Base64 olarak kodlanır
   - Standart Base64 (RFC 4648)
   - Dolgu veya standart dışı karakter yok

**JavaDoc:** [RouterAddress](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterAddress.html)

---

### RouterInfo

**Açıklama:** netDb'de (I2P ağ veritabanı) saklanan bir router hakkında yayımlanmış eksiksiz bilgi. Kimlik, adresler ve yetenekler içerir.

**Biçim:**

```
+----+----+----+----+----+----+----+----+
| router_ident                          |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| published                             |
+----+----+----+----+----+----+----+----+
|size| RouterAddress 0                  |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| RouterAddress 1                       |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| RouterAddress ($size-1)               |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+-//-+----+----+----+
|psiz| options                          |
+----+----+----+----+-//-+----+----+----+
| signature                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

router_ident :: RouterIdentity
                Length: 387+ bytes (typically 391 for X25519+EdDSA)

published :: Date (8 bytes)
             Publication timestamp (milliseconds since epoch)

size :: Integer (1 byte)
        Number of RouterAddress entries
        Range: 0-255

addresses :: Array of RouterAddress
             Variable length
             Each RouterAddress has variable size

peer_size :: Integer (1 byte)
             Number of peer hashes (ALWAYS 0)
             Historical, unused feature

options :: Mapping
           Router capabilities and metadata
           MUST be sorted by key

signature :: Signature
             Length determined by router_ident signing key type
             Typically 64 bytes (EdDSA)
             Signed by router_ident's SigningPrivateKey
```
**Veritabanı Depolaması:** - **Veritabanı Türü:** 0 - **Anahtar:** RouterIdentity'nin SHA-256 karması - **Değer:** Tam RouterInfo yapısı

**Yayımlanma Zaman Damgası:** - 8 baytlık Tarih (epoch'tan beri milisaniye cinsinden) - RouterInfo sürümlendirmesi için kullanılır - Routers periyodik olarak yeni RouterInfo yayımlar - Floodfills, yayımlanma zaman damgasına göre en yeni sürümü tutar

**Adres Sıralaması:** - **Tarihsel:** Çok eski routers, adreslerin verilerinin SHA-256 karmasına göre sıralanmasını gerektirirdi - **Güncel:** Sıralama GEREKLİ DEĞİL, uyumluluk için uygulamaya değer değil - Adresler herhangi bir sırada olabilir

**Eş Sayısı Alanı (Tarihsel):** - **Her zaman 0** modern I2P'de - Kısıtlı rotalar için tasarlanmıştı (uygulanmadı) - Uygulansaydı, ardından o sayıda Router Hashes (router için benzersiz özetler) gelirdi - Bazı eski uygulamalar sıralanmış bir eş listesi gerektirmiş olabilir

**Seçenek Eşlemesi:**

Seçenekler anahtara göre sıralanmak zorundadır. Standart seçenekler şunları içerir:

**Yetenek Seçenekleri:**

```
"caps" = Capability string
         Common values:
           f = Floodfill (network database)
           L or M or N or O = Bandwidth tier (L=lowest, O=highest)
           R = Reachable
           U = Unreachable/firewalled
           Example: "fLRU" = Floodfill, Low bandwidth, Reachable, Unreachable
```
**Ağ Seçenekleri:**

```
"netId" = Network ID (default "2" for main I2P network)
          Different values for test networks

"router.version" = I2P version string
                   Example: "0.9.67" or "2.10.0"
```
**İstatistiksel Seçenekler:**

```
"stat_uptime" = Uptime in milliseconds
"coreVersion" = Core I2P version
"router.version" = Full router version string
```
Standart seçeneklerin tam listesi için [Ağ Veritabanı RouterInfo (yöneltici bilgisi) dokümantasyonu](/docs/specs/common-structures/#routerInfo) bölümüne bakın.

**İmza Hesaplama:**

```
Data to sign: Complete RouterInfo structure from router_ident through options

Verification:
1. Extract RouterIdentity from RouterInfo
2. Get SigningPublicKey from RouterIdentity (type determines algorithm)
3. Verify signature over all data preceding signature field
4. Signature must match signing key type and length
```
**Tipik Modern RouterInfo:**

```
RouterIdentity: 391 bytes (X25519+EdDSA with Key Certificate)
Published: 8 bytes
Size: 1 byte (typically 1-4 addresses)
RouterAddress × N: Variable (typically 200-500 bytes each)
Peer Size: 1 byte (value=0)
Options: Variable (typically 50-200 bytes)
Signature: 64 bytes (EdDSA)

Total: ~1000-2500 bytes typical
```
**Uygulama Notları:**

1. **Birden Fazla Adres:**
   - Router'lar genellikle 1-4 adres yayınlar
   - IPv4 ve IPv6 varyantları
   - SSU2 ve/veya NTCP2 taşıma protokolleri
   - Her adres bağımsızdır

2. **Sürümleme:**
   - Daha yeni RouterInfo (router bilgi kaydı), daha geç `published` zaman damgasına sahiptir
   - Routers, her ~2 saatte bir veya adresler değiştiğinde yeniden yayınlar
   - Floodfills yalnızca en yeni sürümü depolar ve yayar

3. **Doğrulama:**
   - RouterInfo'yu kabul etmeden önce imzayı doğrulayın
   - Her RouterAddress'te expiration alanının tamamen sıfırlardan oluştuğunu kontrol edin
   - Seçenekler eşlemesinin anahtara göre sıralı olduğunu doğrulayın
   - Sertifika ve anahtar türlerinin bilinen/desteklenen türler olduğunu kontrol edin

4. **Ağ Veritabanı:**
   - Floodfills, Hash(RouterIdentity) ile indekslenen RouterInfo'yu saklar
   - Son yayından sonra ~2 gün boyunca saklanır
   - Routers, diğer router'ları keşfetmek için floodfills'i sorgular

**JavaDoc:** [RouterInfo](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterInfo.html)

---

## Uygulama Notları

### Bayt Sırası (Endianness - baytların bellekte veya iletimde diziliş sırası)

**Varsayılan: Big-Endian (Ağ bayt sırası)**

I2P yapılarının çoğu big-endian (büyük uçlu) bayt sırasını kullanır: - Tüm tamsayı türleri (1-8 bayt) - Tarih tipindeki zaman damgaları - TunnelId - Dize uzunluğu ön eki - Sertifika türleri ve uzunlukları - Anahtar türü kodları - Eşleme boyutu alanları

**İstisna: Little-Endian (küçük uçlu bayt sıralaması)**

Aşağıdaki anahtar türleri **little-endian** (en az anlamlı bayt önce) kodlamasını kullanır: - **X25519** şifreleme anahtarları (tip 4) - **EdDSA_SHA512_Ed25519** imzalama anahtarları (tip 7) - **EdDSA_SHA512_Ed25519ph** imzalama anahtarları (tip 8) - **RedDSA_SHA512_Ed25519** imzalama anahtarları (tip 11)

**Uygulama:**

```java
// Big-endian (most structures)
int value = ((bytes[0] & 0xFF) << 24) | 
            ((bytes[1] & 0xFF) << 16) |
            ((bytes[2] & 0xFF) << 8) | 
            (bytes[3] & 0xFF);

// Little-endian (X25519, EdDSA, RedDSA)
int value = (bytes[0] & 0xFF) | 
            ((bytes[1] & 0xFF) << 8) |
            ((bytes[2] & 0xFF) << 16) | 
            ((bytes[3] & 0xFF) << 24);
```
### Yapı Sürümleme

**Asla Sabit Boyutlar Varsaymayın:**

Birçok yapı değişken uzunluğa sahiptir: - RouterIdentity: 387+ bayt (her zaman 387 değil) - Destination: 387+ bayt (her zaman 387 değil) - LeaseSet2: Önemli ölçüde değişir - Certificate: 3+ bayt

**Her Zaman Boyut Alanlarını Okuyun:** - Sertifika uzunluğu 1-2. baytlarda - Mapping (eşleme) boyutu başlangıçta - KeysAndCert her zaman 384 + 3 + certificate_length olarak hesaplanır

**Fazladan Veriyi Denetleyin:** - Geçerli yapıların ardından gelen sondaki gereksiz veriyi engelleyin - Sertifika uzunluklarının anahtar türleriyle eşleştiğini doğrulayın - Sabit boyutlu türler için beklenen uzunlukların birebir olmasını zorunlu kılın

### Güncel Öneriler (Ekim 2025)

**Yeni Router Kimlikleri İçin:**

```
Encryption: X25519 (type 4, 32 bytes)
Signing: EdDSA_SHA512_Ed25519 (type 7, 32 bytes)
Certificate: Key Certificate (type 5)
Total Size: 391 bytes
Padding: Compressible per [Proposal 161](/tr/proposals/161-ri-dest-padding/)
```
**Yeni Destination (I2P'de adres/kimlik) nesneleri için:**

```
Unused Public Key Field: 256 bytes random (compressible)
Signing: EdDSA_SHA512_Ed25519 (type 7, 32 bytes)
Certificate: Key Certificate (type 5)
Total Size: 391 bytes
Padding: Compressible per [Proposal 161](/tr/proposals/161-ri-dest-padding/)
```
**Yeni LeaseSets için:**

```
Type: LeaseSet2 (type 3)
Encryption Keys: X25519 (type 4, 32 bytes)
Leases: At least 1, typically 3-5
Options: Include service records per [Proposal 167](/proposals/167-service-records/)
Signature: EdDSA (64 bytes)
```
**Şifrelenmiş Hizmetler için:**

```
Type: EncryptedLeaseSet (type 5)
Blinding: RedDSA_SHA512_Ed25519 (type 11)
Inner LeaseSet: LeaseSet2 (type 3)
Rotation: Daily blinding key rotation
Authorization: Per-client encryption keys
```
### Kullanımdan Kaldırılmış Özellikler - Kullanmayın

**Kullanımdan Kaldırılmış Şifreleme:** - Router Kimlikleri için ElGamal (type 0) (0.9.58'de kullanımdan kaldırıldı) - ElGamal/AES+SessionTag (oturum etiketi) şifrelemesi (ECIES-X25519 kullanın)

**Kullanımdan Kaldırılan İmzalama:** - DSA_SHA1 (tip 0) Router Kimlikleri için (0.9.58'de kullanımdan kaldırıldı) - ECDSA varyantları (tip 1-3) yeni gerçeklemeler için - RSA varyantları (tip 4-6) SU3 dosyaları hariç

**Kullanımdan Kaldırılmış Ağ Biçimleri:** - LeaseSet tip 1 (LeaseSet2 kullanın) - Lease (44 bayt, Lease2 kullanın) - Orijinal Lease sona erme biçimi

**Kullanımdan Kaldırılmış Taşıma Protokolleri:** - NTCP (0.9.50'de kaldırıldı) - SSU (2.4.0'da kaldırıldı)

**Kullanımdan Kaldırılmış Sertifikalar:** - HASHCASH (tip 1) - HIDDEN (tip 2) - SIGNED (tip 3) - MULTIPLE (tip 4)

### Güvenlik Hususları

**Anahtar Üretimi:** - Daima kriptografik olarak güvenli rastgele sayı üreteçleri kullanın - Anahtarları farklı bağlamlar arasında asla yeniden kullanmayın - Özel anahtarları uygun erişim denetimleriyle koruyun - İşiniz bittiğinde anahtar materyalini bellekten güvenli bir şekilde silin

**İmza Doğrulama:** - Verilere güvenmeden önce her zaman imzaları doğrulayın - İmza uzunluğunun anahtar türüyle eşleştiğini kontrol edin - İmzalanmış verilerin beklenen alanları içerdiğini doğrulayın - Sıralı eşlemeler için, imzalamadan/doğrulamadan önce sıralama düzenini doğrulayın

**Zaman Damgası Doğrulama:** - Yayınlanan zamanların makul olduğunu kontrol edin (çok uzak bir gelecekte olmamalı) - Lease (kiralama girdisi) sona erme zamanlarının geçmiş olmadığını doğrulayın - Saat kayması toleransını göz önünde bulundurun (tipik olarak ±30 saniye)

**Ağ Veritabanı:** - Depolamadan önce tüm yapıları doğrulayın - DoS saldırılarını önlemek için boyut sınırlarını uygulayın - Sorgular ve yayımlar için oran sınırlaması uygulayın - Veritabanı anahtarlarının yapı özetleriyle (hash) eşleştiğini doğrulayın

### Uyumluluk Notları

**Geriye Dönük Uyumluluk:** - ElGamal ve DSA_SHA1 hâlâ eski router'lar için destekleniyor - Kullanımdan kaldırılmış anahtar türleri işlevsel kalır ancak kullanımı önerilmez - Sıkıştırılabilir padding (doldurma) ([Proposal 161](/tr/proposals/161-ri-dest-padding/)) 0.6'ya kadar geriye dönük uyumludur

**İleriye Dönük Uyumluluk:** - Bilinmeyen anahtar türleri, uzunluk alanları kullanılarak ayrıştırılabilir - Bilinmeyen sertifika türleri, uzunluk kullanılarak atlanabilir - Bilinmeyen imza türleri, sorunsuz şekilde ele alınmalıdır - Uygulayıcılar, bilinmeyen isteğe bağlı özellikler karşısında başarısız olmamalıdır

**Geçiş Stratejileri:** - Geçiş sırasında hem eski hem de yeni anahtar türlerini destekleyin - LeaseSet2 birden fazla şifreleme anahtarını listeleyebilir - Çevrimdışı imzalar güvenli anahtar döndürmeyi mümkün kılar - MetaLeaseSet şeffaf hizmet geçişini sağlar

### Test ve Doğrulama

**Yapı Doğrulaması:** - Tüm uzunluk alanlarının beklenen aralıklar içinde olduğunu doğrulayın - Değişken uzunluklu yapıların doğru şekilde ayrıştırıldığını kontrol edin - İmzaların başarıyla doğrulandığını doğrulayın - Hem en küçük hem de en büyük boyutlu yapılarla test edin

**Uç Durumlar:** - Sıfır uzunluklu dizeler - Boş eşlemeler - Asgari ve azami lease (kiralama kaydı) sayıları - Sıfır uzunluklu yük içeren sertifika - Çok büyük yapılar (azami boyutlara yakın)

**Birlikte çalışabilirlik:** - Resmi Java I2P gerçekleştirmesine karşı test edin - i2pd ile uyumluluğu doğrulayın - Çeşitli netDb (ağ veritabanı) içerikleriyle test edin - Doğruluğu bilinen test vektörlerine göre doğrulayın

---

## Kaynakça

### Spesifikasyonlar

- [I2NP Protokolü](/docs/specs/i2np/)
- [I2CP Protokolü](/docs/specs/i2cp/)
- [SSU2 Taşıma](/docs/specs/ssu2/)
- [NTCP2 Taşıma](/docs/specs/ntcp2/)
- [Tunnel Protokolü](/docs/specs/implementation/)
- [Datagram Protokolü](/docs/api/datagrams/)

### Kriptografi

- [Kriptografiye Genel Bakış](/docs/specs/cryptography/)
- [ElGamal/AES Şifreleme](/docs/legacy/elgamal-aes/)
- [ECIES-X25519 Şifreleme](/docs/specs/ecies/)
- [Routers için ECIES](/docs/specs/ecies/#routers)
- [ECIES Hibrit (Post-Kuantum)](/docs/specs/ecies/#hybrid)
- [Red25519 İmzaları](/docs/specs/red25519-signature-scheme/)
- [Şifrelenmiş LeaseSet (hedefin tünel giriş noktaları ve sürelerini içeren kayıt)](/docs/specs/encryptedleaseset/)

### Öneriler

- [Öneri 123: Yeni netDB Kayıtları](/proposals/123-new-netdb-entries/)
- [Öneri 134: GOST İmza Türleri](/proposals/134-gost/)
- [Öneri 136: Deneysel İmza Türleri](/proposals/136-experimental-sigtypes/)
- [Öneri 145: ECIES-P256](/proposals/145-ecies/)
- [Öneri 156: ECIES Routers](/proposals/156-ecies-routers/)
- [Öneri 161: Dolgu Üretimi](/tr/proposals/161-ri-dest-padding/)
- [Öneri 167: Hizmet Kayıtları](/proposals/167-service-records/)
- [Öneri 169: Kuantum Sonrası Kriptografi](/proposals/169-pq-crypto/)
- [Tüm Öneriler Dizini](/proposals/)

### Ağ Veritabanı

- [Ağ Veritabanına Genel Bakış](/docs/specs/common-structures/)
- [RouterInfo Standart Seçenekleri](/docs/specs/common-structures/#routerInfo)

### JavaDoc API Referansı

- [Çekirdek Veri Paketi](http://docs.i2p-projekt.de/javadoc/net/i2p/data/)
- [PublicKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/PublicKey.html)
- [PrivateKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/PrivateKey.html)
- [SessionKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SessionKey.html)
- [SigningPublicKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SigningPublicKey.html)
- [SigningPrivateKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SigningPrivateKey.html)
- [Signature](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Signature.html)
- [Hash](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Hash.html)
- [SessionTag](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SessionTag.html)
- [TunnelId](http://docs.i2p-projekt.de/javadoc/net/i2p/data/TunnelId.html)
- [Certificate](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Certificate.html)
- [DataHelper](http://docs.i2p-projekt.de/javadoc/net/i2p/data/DataHelper.html)
- [KeysAndCert](http://docs.i2p-projekt.de/javadoc/net/i2p/data/KeysAndCert.html)
- [RouterIdentity](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterIdentity.html)
- [Destination](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Destination.html)
- [Lease](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Lease.html)
- [LeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/LeaseSet.html)
- [Lease2](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Lease2.html)
- [LeaseSet2](http://docs.i2p-projekt.de/javadoc/net/i2p/data/LeaseSet2.html)
- [MetaLease](http://docs.i2p-projekt.de/javadoc/net/i2p/data/MetaLease.html)
- [MetaLeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/MetaLeaseSet.html)
- [EncryptedLeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/EncryptedLeaseSet.html)
- [RouterAddress](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterAddress.html)
- [RouterInfo](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterInfo.html)

### Harici Standartlar

- **RFC 7748 (X25519):** Güvenlik için Eliptik Eğriler
- **RFC 7539 (ChaCha20):** IETF Protokolleri için ChaCha20 ve Poly1305
- **RFC 4648 (Base64):** Base16, Base32 ve Base64 Veri Kodlamaları
- **FIPS 180-4 (SHA-256):** Güvenli Özet Standardı
- **FIPS 204 (ML-DSA):** Modül-Kafes Tabanlı Dijital İmza Standardı
- [IANA Hizmet Kaydı](http://www.dns-sd.org/ServiceTypes.html)

### Topluluk Kaynakları

- [I2P Web Sitesi](/)
- [I2P Forumu](https://i2pforum.net)
- [I2P GitLab](https://i2pgit.org/I2P_Developers/i2p.i2p)
- [I2P GitHub Aynası](https://github.com/i2p/i2p.i2p)
- [Teknik Dokümantasyon Dizini](/docs/)

### Sürüm Bilgileri

- [I2P 2.10.0 Sürümü](/tr/blog/2025/09/08/i2p-2.10.0-release/)
- [Sürüm Geçmişi](https://github.com/i2p/i2p.i2p/blob/master/history.txt)
- [Değişiklik Günlüğü](https://github.com/i2p/i2p.i2p/blob/master/debian/changelog)

---

## Ek: Hızlı Başvuru Tabloları

### Anahtar Türü Hızlı Başvuru

**Güncel Standart (tüm yeni uygulamalar için önerilir):** - **Şifreleme:** X25519 (tip 4, 32 bayt, little-endian (küçük endian)) - **İmzalama:** EdDSA_SHA512_Ed25519 (tip 7, 32 bayt, little-endian)

**Eski (Destekleniyor ancak artık önerilmiyor):** - **Şifreleme:** ElGamal (tip 0, 256 bayt, big-endian (en yüksek anlamlı bayt önce)) - **İmzalama:** DSA_SHA1 (tip 0, 20 baytlık özel / 128 baytlık açık, big-endian)

**Özelleştirilmiş:** - **İmzalama (Şifrelenmiş LeaseSet):** RedDSA_SHA512_Ed25519 (tip 11, 32 bayt, little-endian (küçük uçlu bayt sıralaması))

**Post-Kuantum (Beta, henüz kesinleşmedi):** - **Hibrit Şifreleme:** MLKEM_X25519 varyantları (tipler 5-7) - **Saf PQ Şifreleme:** MLKEM varyantları (henüz atanmış tip kodları yok)

### Yapı Boyutları Hızlı Başvuru

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Structure</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Minimum Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Typical Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Maximum Size</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Integer</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Date</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">String</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">256 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SessionKey</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Hash</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelId</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Certificate</td><td style="border:1px solid var(--color-border); padding:0.5rem;">3 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">7 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">65,538 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">KeysAndCert</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">391 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterIdentity</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">391 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Destination</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">391 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Lease</td><td style="border:1px solid var(--color-border); padding:0.5rem;">44 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">44 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">44 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Lease2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1200 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈2000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈500 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈800 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈2000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈600 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈3000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterAddress</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈150 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈300 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈600 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1500 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈3000+ bytes</td></tr>
  </tbody>
</table>
### Veritabanı Türleri için Hızlı Başvuru

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Structure</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Stored under Hash(RouterIdentity)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Use LeaseSet2 instead</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Stored under Hash(Destination)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Stored under Hash(Blinded Destination)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">MetaLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Defined</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Verify production status</td></tr>
  </tbody>
</table>
### Taşıma Protokolü Hızlı Başvuru

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Port Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">UDP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.54</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Default since 0.9.56</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TCP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.36</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">UDP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1pxsolid var(--color-border); padding:0.5rem;">Removed in 2.4.0</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TCP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed in 0.9.50</td></tr>
  </tbody>
</table>
### Sürüm Kilometre Taşları Hızlı Başvuru

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">API</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Date</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Changes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.6.x</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2005</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destination encryption disabled</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Dec 2013</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Key Certificates introduced</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Sep 2015</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA support added</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.16</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.16</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Nov 2015</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Router Key Certificates</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.36</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.36</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Aug 2018</td><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP2 introduced</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Nov 2018</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2, X25519 for Destinations</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Dec 2018</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet working</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.48</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.48</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Jul 2020</td><td style="border:1px solid var(--color-border); padding:0.5rem;">X25519 for Router Identities</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.50</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.50</td><td style="border:1px solid var(--color-border); padding:0.5rem;">May 2021</td><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP removed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.54</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.54</td><td style="border:1px solid var(--color-border); padding:0.5rem;">May 2022</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 testing</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.57</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.57</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Jan 2023</td><td style="border:1px solid var(--color-border); padding:0.5rem;">[Proposal 161](/tr/proposals/161-ri-dest-padding/) padding (release 2.1.0)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.58</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.58</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mar 2023</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal/DSA deprecated for RIs (2.2.0)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.66</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.66</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Jun 2025</td><td style="border:1px solid var(--color-border); padding:0.5rem;">[Proposal 167](/proposals/167-service-records/) service records (2.9.0)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Sep 2025</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ML-KEM beta support (2.10.0)</td></tr>
  </tbody>
</table>
---
