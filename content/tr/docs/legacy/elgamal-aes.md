---
title: "ElGamal/AES + SessionTag (oturum etiketi) Şifreleme"
description: "ElGamal, AES, SHA-256 ve tek kullanımlık oturum etiketlerini birleştiren eski tip uçtan uca şifreleme"
slug: "elgamal-aes"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "needs-review"
---

> **Durum:** Bu belge, eski ElGamal/AES+SessionTag (oturum etiketi) şifreleme protokolünü açıklar. Modern I2P sürümleri (2.10.0+) [ECIES-X25519-AEAD-Ratchet](/docs/specs/ecies/) kullandığından, bu protokol yalnızca geriye dönük uyumluluk için desteklenmeye devam etmektedir. ElGamal protokolü kullanımdan kaldırılmıştır ve yalnızca tarihsel ve birlikte çalışabilirlik amaçlarıyla muhafaza edilmektedir.

## Genel Bakış

ElGamal/AES+SessionTag, I2P'nin garlic messages (garlic mesajları) için özgün uçtan uca şifreleme mekanizmasını sağlıyordu. Şunları birleştiriyordu:

- **ElGamal (2048-bit)** — anahtar değişimi için
- **AES-256/CBC** — yük verisinin şifrelenmesi için
- **SHA-256** — özetleme ve IV türetimi için
- **Session Tags (32 bayt)** — tek kullanımlık mesaj tanımlayıcıları için

Protokol, kalıcı bağlantıları sürdürmeye gerek kalmadan routers ve destinations (I2P adresleri) arasında güvenli iletişim kurulmasına olanak tanıyordu. Her oturum, simetrik bir AES anahtarı oluşturmak için asimetrik bir ElGamal değişimi kullanıyordu; ardından o oturuma referans veren hafif "tagged" mesajlar geliyordu.

## Protokol İşleyişi

### Oturum Kurulumu (Yeni Oturum)

Yeni bir oturum, iki bölüm içeren bir mesajla başladı:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Section</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>ElGamal-encrypted block</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">514 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">222 bytes of plaintext encrypted using the recipient's ElGamal public key</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Establishes the AES session key and IV seed</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>AES-encrypted block</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Variable (≥128 bytes typical)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Payload data, integrity hash, and session tags</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Carries the actual message and new tags</td>
    </tr>
  </tbody>
</table>
ElGamal bloğunun içindeki açık metin şunlardan oluşuyordu:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Session Key</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 key for the session</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Pre-IV</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Material for deriving the AES initialization vector (<code>IV = first 16 bytes of SHA-256(Pre-IV)</code>)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Random Padding</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">158 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Filler to reach required ElGamal plaintext length</td>
    </tr>
  </tbody>
</table>
### Mevcut Oturum Mesajları

Bir oturum kurulduğunda, gönderici, önbelleğe alınmış oturum etiketlerini kullanarak **existing-session** mesajları gönderebilirdi:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Session Tag</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Single-use identifier tied to the existing session key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-Encrypted Block</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Variable</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypted payload and metadata using the established AES key</td>
    </tr>
  </tbody>
</table>
Router'lar iletilen etiketleri yaklaşık **15 dakika** boyunca önbelleğe alırdı; bu sürenin ardından kullanılmayan etiketlerin süresi dolardı. Her etiket, korelasyon saldırılarını önlemek için tam olarak **bir mesaj** için geçerliydi.

### AES ile Şifrelenmiş Blok Biçimi

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tag Count</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Number (0–200) of new session tags included</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Session Tags</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32 × N bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Newly generated single-use tags</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Payload Size</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Length of the payload in bytes</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Payload Hash</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SHA-256 digest of the payload</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Flag</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1 byte</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>0x00</code> normal, <code>0x01</code> = new session key follows (unused)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">New Session Key</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32 bytes (optional)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Replacement AES key (rarely used)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Payload</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Variable</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypted message data</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Padding</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Variable (16-byte aligned)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Random padding to block boundary</td>
    </tr>
  </tbody>
</table>
Router'lar, yeni oturumlar için Pre-IV'den (ön IV), mevcut oturumlar içinse session tag'den (oturum etiketi) türetilen oturum anahtarı ve IV'yi (başlatma vektörü) kullanarak şifresini çözer. Şifre çözüldükten sonra, düz metin yükünün SHA-256 karmasını yeniden hesaplayarak bütünlüğü doğrularlar.

## Oturum Etiketi Yönetimi

- Etiketler **tek yönlüdür**: Alice → Bob etiketleri, Bob → Alice için yeniden kullanılamaz.
- Etiketler yaklaşık **15 dakika** sonra sona erer.
- Router'lar, etiketleri, anahtarları ve sona erme zamanlarını izlemek için hedef başına oturum anahtarı yöneticileri bulundurur.
- Uygulamalar, [I2CP seçenekleri](/docs/specs/i2cp/) aracılığıyla etiket davranışını denetleyebilir:
  - **`i2cp.tagThreshold`** — yenileme yapılmadan önce önbellekte tutulması gereken minimum etiket sayısı
  - **`i2cp.tagCount`** — mesaj başına yeni etiket sayısı

Bu mekanizma, mesajlar arasındaki ilişkilendirilemezliği korurken, yüksek maliyetli ElGamal el sıkışmalarını en aza indirdi.

## Yapılandırma ve Verimlilik

Session tags (oturum etiketleri), I2P'nin yüksek gecikmeli ve sırasız aktarımı genelinde verimliliği artırmak için getirildi. Tipik bir yapılandırma **mesaj başına 40 etiket** sağlardı ve yaklaşık 1.2 KB ek yük eklerdi. Uygulamalar, beklenen trafiğe göre teslim davranışını ayarlayabilirdi:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Use Case</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended Tags</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Short-lived requests (HTTP, datagrams)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0 – 5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Low overhead, may trigger ElGamal fallback</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Persistent streams or bulk transfer</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">20 – 50</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Higher bandwidth use, avoids session re-establishment</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Long-term services</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">50+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ensures steady tag supply despite loss or delay</td>
    </tr>
  </tbody>
</table>
Routers periyodik olarak süresi dolmuş etiketleri temizler ve kullanılmayan oturum durumunu budar; böylece bellek kullanımını azaltır ve etiket taşması saldırılarını hafifletir.

## Sınırlamalar

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Category</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Limitation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Performance</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">514-byte ElGamal block adds heavy overhead for new sessions; session tags consume 32 bytes each.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Security</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No forward secrecy – compromise of ElGamal private key exposes past sessions.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Integrity</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-CBC requires manual hash verification; no AEAD.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Quantum Resistance</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Vulnerable to Shor's algorithm – will not survive quantum attacks.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Complexity</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Requires stateful tag management and careful timeout tuning.</td>
    </tr>
  </tbody>
</table>
Bu eksiklikler, [ECIES-X25519-AEAD-Ratchet](/docs/specs/ecies/) protokolünün tasarımını doğrudan motive etti; bu protokol mükemmel ileri gizlilik, kimlik doğrulamalı şifreleme ve verimli anahtar değişimi sağlar.

## Kullanımdan Kaldırma ve Geçiş Durumu

- **Tanıtıldı:** Erken I2P sürümleri (0.6 öncesi)
- **Kullanımdan kaldırıldı:** ECIES-X25519'in tanıtılmasıyla (X25519 tabanlı ECIES anahtar değişimi) (0.9.46 → 0.9.48)
- **Kaldırıldı:** 2.4.0 itibarıyla (Aralık 2023) artık varsayılan değil
- **Destekleniyor:** Yalnızca geriye dönük uyumluluk

Modern router'lar ve hedefler artık **şifreleme türü 4 (ECIES-X25519)**'ü, **tür 0 (ElGamal/AES)** yerine duyuruyor. Eski protokol, güncel olmayan eşlerle birlikte çalışabilirlik için tanınmaya devam ediyor, ancak yeni dağıtımlarda kullanılmamalıdır.

## Tarihsel Bağlam

ElGamal/AES+SessionTag, I2P'nin erken kriptografik mimarisinin temelini oluşturuyordu. Hibrit tasarımı, tek kullanımlık oturum etiketleri ve tek yönlü oturumlar gibi yenilikleri getirdi; bunlar sonraki protokolleri şekillendirdi. Bu fikirlerin birçoğu, deterministic ratchets (belirlenimli anahtar yenileme “ratchet” mekanizmaları) ve hybrid post-quantum key exchanges (klasik ve kuantum sonrası şemaları birleştiren hibrit anahtar değişimleri) gibi modern yapılara evrildi.
