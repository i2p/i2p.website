---
title: "Düşük düzey kriptografi"
description: "I2P genelinde kullanılan simetrik, asimetrik ve imza kriptografik primitiflerinin özeti"
slug: "cryptography"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "needs-review"
---

> **Durum:** Bu sayfa eski “Low-level Cryptography Specification” belgesinin özetini sunar. Modern I2P sürümleri (2.10.0, Ekim 2025) yeni kriptografik ilkelere geçişi tamamladı. Uygulama ayrıntıları için [ECIES](/docs/specs/ecies/), [Encrypted LeaseSets](/docs/specs/encryptedleaseset/), [NTCP2](/docs/specs/ntcp2/), [Red25519](/docs/specs/red25519-signature-scheme/), [SSU2](/docs/specs/ssu2/) ve [Tunnel Creation (ECIES)](/docs/specs/implementation/) gibi uzmanlaşmış teknik belgelere başvurun.

## Evrim Anlık Görüntüsü

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Functional Area</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Legacy Primitive</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Current / Planned Primitive</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Migration Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Transport key exchange</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Diffie–Hellman over 2048-bit prime (NTCP / SSU)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519 (NTCP2 / SSU2)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Completed (NTCP2 and SSU2 fully deployed)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">End-to-end encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ElGamal/AES+SessionTags</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECIES-X25519-AEAD-Ratchet</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Completed (2.4.0+)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Symmetric cipher</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256/CBC + HMAC-MD5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20/Poly1305 (AEAD)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Active (tunnel layer remains AES-256)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default signatures</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DSA-SHA1 (1024-bit)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA/RedDSA on Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fully migrated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Experimental / future</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Hybrid post-quantum encryption (opt-in)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">In testing (2.10.0)</td>
    </tr>
  </tbody>
  
</table>
## Asimetrik Şifreleme

### X25519 (eliptik eğri Diffie-Hellman anahtar değişimi algoritması)

- NTCP2, ECIES-X25519-AEAD-Ratchet, SSU2 ve X25519 tabanlı tunnel oluşturma için kullanılır.  
- Noise protokol çerçevesi aracılığıyla kompakt anahtarlar, sabit zamanlı işlemler ve ileri gizlilik sağlar.  
- 32 baytlık anahtarlar ve verimli anahtar değişimiyle 128 bit güvenlik sunar.

### ElGamal (Eski)

- Eski router'larla geriye dönük uyumluluk için korunmuştur.  
- 2048 bitlik Oakley Group 14 asal sayısı (RFC 3526) üzerinde, üreteç 2 ile çalışır.  
- AES oturum anahtarlarını ve IV'leri 514 baytlık şifreli metinler içinde şifreler.  
- Kimliği doğrulanmış şifreleme ve ileri gizlilik yoktur; tüm modern uç noktalar ECIES'e geçmiştir.

## Simetrik Şifreleme

### ChaCha20/Poly1305 (ChaCha20 akış şifreleyicisi ve Poly1305 mesaj kimlik doğrulama koduna (MAC) dayalı doğrulanmış şifreleme (AEAD) şeması)

- NTCP2, SSU2 ve ECIES (Eliptik Eğri Entegre Şifreleme Şeması) genelinde varsayılan kimlik doğrulamalı şifreleme yapıtaşıdır.  
- AES donanım desteği olmadan AEAD (İlişkili Verili Kimlik Doğrulamalı Şifreleme) güvenliği ve yüksek performans sağlar.  
- RFC 7539’a göre uygulanmıştır (256‑bit anahtar, 96‑bit tek seferlik sayı, 128‑bit etiket).

### AES‑256/CBC (Eski)

- Hâlâ tunnel katmanı şifrelemesi için kullanılır; blok şifre yapısı I2P’nin katmanlı şifreleme modeline uygundur.  
- PKCS#5 padding ve her atlama için IV dönüşümleri kullanır.  
- Uzun vadeli bir inceleme için planlanmış olsa da kriptografik olarak sağlamlığını koruyor.

## İmzalar

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Signature Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage Notes</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DSA‑SHA1 (1024‑bit)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Original default; still accepted for legacy Destinations.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA‑SHA256/384/512</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Used during 2014–2015 transition.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA‑SHA512‑Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default for Router and Destination identities (since 0.9.15).</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RedDSA‑SHA512‑Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Used for encrypted LeaseSet signatures (0.9.39+).</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Specialized</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA‑SHA512‑4096</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For out‑of‑band signing (su3 updates, reseeds, plugins).</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Application‑layer</td>
    </tr>
  </tbody>
</table>
## Hash ve Anahtar Türetimi

- **SHA‑256:** DHT (Dağıtık Karma Tablosu) anahtarları, HKDF ve eski imzalar için kullanılır.  
- **SHA‑512:** EdDSA/RedDSA tarafından ve Noise HKDF türetimlerinde kullanılır.  
- **HKDF‑SHA256:** ECIES, NTCP2 ve SSU2 içinde oturum anahtarlarını türetir.  
- Günlük olarak dönen SHA‑256 türetimleri, netDb içindeki RouterInfo (yönlendirici bilgisi) ve LeaseSet depolama konumlarını güvence altına alır.

## Taşıma Katmanı Özeti

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Transport</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Key Exchange</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Encryption</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Authentication</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NTCP2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20/Poly1305</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AEAD</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default TCP transport</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SSU2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20/Poly1305</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AEAD</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default UDP transport</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SSU (Legacy)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DH‑2048</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES‑256/CBC + HMAC‑MD5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Legacy</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Removed (2.4.0)</td>
    </tr>
  </tbody>
</table>
Her iki taşıma, Noise_XK el sıkışma desenini kullanarak bağlantı düzeyinde ileri gizlilik (forward secrecy) ve yeniden oynatma koruması sağlar.

## Tunnel Katmanı Şifrelemesi

- Her atlama düzeyindeki katmanlı şifreleme için AES‑256/CBC kullanılmaya devam ediyor.  
- Giden ağ geçitleri yinelemeli AES deşifre işlemi yapar; her atlama, kendi katman anahtarı ve IV (Initialization Vector - başlatma vektörü) anahtarını kullanarak yeniden şifreler.  
- Çift IV şifreleme, korelasyon ve doğrulama saldırılarını hafifletir.  
- AEAD (Authenticated Encryption with Associated Data - ilişkili verilerle kimliği doğrulanmış şifreleme) kullanımına geçiş inceleniyor, ancak şu anda planlanmıyor.

## Kuantum Sonrası Kriptografi

- I2P 2.10.0, **deneysel hibrit post‑kuantum şifreleme**yi tanıtıyor.  
- Test amacıyla Hidden Service Manager (Gizli Servis Yöneticisi) üzerinden elle etkinleştirilir.  
- X25519’u kuantuma dayanıklı bir KEM ile birleştirir (hibrit mod).
- Varsayılan değildir; araştırma ve performans değerlendirmesi için tasarlanmıştır.

## Genişletilebilirlik Çerçevesi

- Şifreleme ve imza *tür tanımlayıcıları* birden fazla kriptografik ilkelin paralel olarak desteklenmesine olanak tanır.  
- Mevcut eşleştirmeler şunları içerir:  
  - **Şifreleme türleri:** 0 = ElGamal/AES+SessionTags, 4 = ECIES‑X25519‑AEAD‑Ratchet.  
  - **İmza türleri:** 0 = DSA‑SHA1, 7 = EdDSA‑SHA512‑Ed25519, 11 = RedDSA‑SHA512‑Ed25519.  
- Bu çerçeve, ağ bölünmeleri olmadan post‑quantum (kuantum sonrası) şemalar dahil gelecekteki yükseltmeleri mümkün kılar.

## Kriptografik Bileşim

- **Taşıma katmanı:** X25519 + ChaCha20/Poly1305 (Noise çerçevesi).  
- **Tunnel katmanı:** Anonimlik için AES‑256/CBC katmanlı şifreleme.  
- **Uçtan uca:** Gizlilik ve ileri gizlilik için ECIES‑X25519‑AEAD‑Ratchet.  
- **Veritabanı katmanı:** Kimlik doğrulaması için EdDSA/RedDSA imzaları.

Bu katmanlar derinlemesine savunma sağlar: bir katman kompromize edilse bile, diğerleri gizliliği ve ilişkilendirilemezliği korur.

## Özet

I2P 2.10.0 sürümünün kriptografik yığını şunlara odaklanır:

- **Curve25519 (X25519)** anahtar değişimi için  
- **ChaCha20/Poly1305** simetrik şifreleme için  
- **EdDSA / RedDSA** dijital imzalar için  
- **SHA‑256 / SHA‑512** özetleme ve türetme için  
- **Deneysel kuantum‑sonrası hibrit modlar** geleceğe dönük uyumluluk için

Eski ElGamal, AES‑CBC ve DSA, geriye dönük uyumluluk için korunmaktadır, ancak artık etkin taşıma protokollerinde veya şifreleme yollarında kullanılmamaktadır.
