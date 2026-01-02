---
title: "SSU2 Spesifikasyonu"
description: "Güvenli Yarı Güvenilir UDP Taşıma Protokolü Sürüm 2"
slug: "ssu2"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## 1. Genel Bakış

SSU2, I2P içinde güvenli, yarı güvenilir router’lar arası iletişim için kullanılan UDP tabanlı bir taşıma katmanı protokolüdür. Genel amaçlı bir taşıma protokolü değildir; bunun yerine **I2NP mesaj alışverişi** için özelleştirilmiştir.

### Temel Özellikler

- Noise XK pattern (Noise protokolünde kullanılan bir anahtar değişimi şablonu) ile kimlik doğrulamalı anahtar değişimi
- Derin Paket İnceleme (DPI) direncine yönelik şifrelenmiş üstbilgiler
- Aktarıcılar ve hole punching (delik açma tekniği) kullanarak NAT geçişi
- Bağlantı taşınması ve adres doğrulaması
- İsteğe bağlı yol doğrulaması
- İleri gizlilik ve yeniden oynatma koruması

### Eski Sürüm ve Uyumluluk

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Implementation</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">SSU2 Default</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">SSU1 Removed</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">i2pd</td><td style="border:1px solid var(--color-border); padding:0.6rem;">2.44.0</td><td style="border:1px solid var(--color-border); padding:0.6rem;">2.44.0</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Java I2P</td><td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.56</td><td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.61</td></tr>
  </tbody>
</table>
SSU1 artık genel I2P ağı genelinde kullanımda değil.

---

## 2. Kriptografi

SSU2, I2P'ye özgü uzantılarla birlikte **Noise_XK_25519_ChaChaPoly_SHA256** kullanır.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Function</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Algorithm</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Diffie-Hellman</td><td style="border:1px solid var(--color-border); padding:0.6rem;">X25519 (RFC 7748)</td><td style="border:1px solid var(--color-border); padding:0.6rem;">32-byte keys</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Cipher</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20/Poly1305 (RFC 7539)</td><td style="border:1px solid var(--color-border); padding:0.6rem;">AEAD encryption</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Hash</td><td style="border:1px solid var(--color-border); padding:0.6rem;">SHA-256</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Used for key derivation and message integrity</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">KDF</td><td style="border:1px solid var(--color-border); padding:0.6rem;">HKDF-SHA256 (RFC 5869)</td><td style="border:1px solid var(--color-border); padding:0.6rem;">For session and header keys</td></tr>
  </tbody>
</table>
Başlıklar ve yükler, `mixHash()` aracılığıyla kriptografik olarak birbirine bağlanır.   Uygulama verimliliği için tüm kriptografik ilkeller NTCP2 ve ECIES (Eliptik Eğri Entegre Şifreleme Şeması) ile ortaktır.

---

## 3. Mesajlara Genel Bakış

### 3.1 UDP Datagram Kuralları

- Her UDP datagramı **tam olarak bir SSU2 message** taşır.  
- Session Confirmed iletileri birden fazla datagram arasında parçalanabilir.

**Minimum boyut:** 40 bayt   **Maksimum boyut:** 1472 bayt (IPv4) / 1452 bayt (IPv6)

### 3.2 Mesaj Türleri

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Message</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Header</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Session Request</td><td style="border:1px solid var(--color-border); padding:0.6rem;">32B</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Handshake initiation</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">1</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Session Created</td><td style="border:1px solid var(--color-border); padding:0.6rem;">32B</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Handshake response</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">2</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Session Confirmed</td><td style="border:1px solid var(--color-border); padding:0.6rem;">16B</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Final handshake, may be fragmented</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">6</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Data</td><td style="border:1px solid var(--color-border); padding:0.6rem;">16B</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypted I2NP message blocks</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Peer Test</td><td style="border:1px solid var(--color-border); padding:0.6rem;">32B</td><td style="border:1px solid var(--color-border); padding:0.6rem;">NAT reachability testing</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">9</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Retry</td><td style="border:1px solid var(--color-border); padding:0.6rem;">32B</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Token or rejection notice</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">10</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Token Request</td><td style="border:1px solid var(--color-border); padding:0.6rem;">32B</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Request for validation token</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">11</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Hole Punch</td><td style="border:1px solid var(--color-border); padding:0.6rem;">32B</td><td style="border:1px solid var(--color-border); padding:0.6rem;">NAT traversal signaling</td></tr>
  </tbody>
</table>
---

## 4. Oturum Kurulumu

### 4.1 Standart Akış (Geçerli Belirteç)

```
Alice                        Bob
SessionRequest  ─────────────>
<──────────────  SessionCreated
SessionConfirmed ────────────>
```
### 4.2 Belirteç Edinimi

```
Alice                        Bob
TokenRequest  ───────────────>
<──────────────  Retry (Token)
SessionRequest  ─────────────>
<──────────────  SessionCreated
SessionConfirmed ────────────>
```
### 4.3 Geçersiz Belirteç

```
Alice                        Bob
SessionRequest ─────────────>
<──────────────  Retry (Termination)
```
---

## 5. Başlık Yapıları

### 5.1 Uzun Başlık (32 bayt)

Oturum kurulmadan önce kullanılır (SessionRequest, Created, Retry, PeerTest, TokenRequest, HolePunch).

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Destination Connection ID</td><td style="border:1px solid var(--color-border); padding:0.6rem;">8</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Random unique ID</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Packet Number</td><td style="border:1px solid var(--color-border); padding:0.6rem;">4</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Random (ignored during handshake)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Type</td><td style="border:1px solid var(--color-border); padding:0.6rem;">1</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Message type</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Version</td><td style="border:1px solid var(--color-border); padding:0.6rem;">1</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Always 2</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">NetID</td><td style="border:1px solid var(--color-border); padding:0.6rem;">1</td><td style="border:1px solid var(--color-border); padding:0.6rem;">2 = main I2P network</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Flags</td><td style="border:1px solid var(--color-border); padding:0.6rem;">1</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved (0)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Source Connection ID</td><td style="border:1px solid var(--color-border); padding:0.6rem;">8</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Random ID distinct from destination</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Token</td><td style="border:1px solid var(--color-border); padding:0.6rem;">8</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Token for address validation</td></tr>
  </tbody>
</table>
### 5.2 Kısa Başlık (16 bayt)

Kurulmuş oturumlar sırasında kullanılır (SessionConfirmed, Data).

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Destination Connection ID</td><td style="border:1px solid var(--color-border); padding:0.6rem;">8</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Stable throughout session</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Packet Number</td><td style="border:1px solid var(--color-border); padding:0.6rem;">4</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Incrementing per message</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Type</td><td style="border:1px solid var(--color-border); padding:0.6rem;">1</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Message type (2 or 6)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Flags</td><td style="border:1px solid var(--color-border); padding:0.6rem;">3</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ACK/fragment flags</td></tr>
  </tbody>
</table>
---

## 6. Şifreleme

### 6.1 AEAD (kimlik doğrulamalı şifreleme ve ilişkili veri)

Tüm veri yükleri **ChaCha20/Poly1305 AEAD** (kimliği doğrulanmış ilişkili verilerle şifreleme) ile şifrelenir:

```
ciphertext = ChaCha20_Poly1305_Encrypt(key, nonce, plaintext, associated_data)
```
- Nonce (tek seferlik sayı): 12 bayt (4 sıfır + 8 sayaç)
- Tag (doğrulama etiketi): 16 bayt
- Associated Data (ilişkili veri): bütünlük bağlaması için başlık içerir

### 6.2 Başlık Koruması

Başlıklar, oturum başlığı anahtarlarından türetilen ChaCha20 anahtar akışı kullanılarak maskelenir. Bu, tüm Connection ID'lerin ve paket alanlarının rastgele görünmesini sağlayarak DPI (Derin Paket İncelemesi) direnci sağlar.

### 6.3 Anahtar Türetimi

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Phase</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Input</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Output</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Initial</td><td style="border:1px solid var(--color-border); padding:0.6rem;">introKey + salt</td><td style="border:1px solid var(--color-border); padding:0.6rem;">handshake header key</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Handshake</td><td style="border:1px solid var(--color-border); padding:0.6rem;">DH(X25519)</td><td style="border:1px solid var(--color-border); padding:0.6rem;">chainKey + AEAD key</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Data phase</td><td style="border:1px solid var(--color-border); padding:0.6rem;">chainKey</td><td style="border:1px solid var(--color-border); padding:0.6rem;">TX/RX keys</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Key rotation</td><td style="border:1px solid var(--color-border); padding:0.6rem;">oldKey</td><td style="border:1px solid var(--color-border); padding:0.6rem;">newKey</td></tr>
  </tbody>
</table>
---

## 7. Güvenlik ve Yeniden Oynatma Saldırılarının Önlenmesi

- Belirteçler IP başına olup ~60 saniye içinde süresi dolar.  
- Yeniden oynatma saldırıları, oturum başına Bloom filtreleri aracılığıyla engellenir.  
- Yinelenen geçici anahtarlar reddedilir.  
- Başlıklar ve yükler kriptografik olarak birbirine bağlanır.

Routers, AEAD kimlik doğrulamasından geçemeyen veya geçersiz sürüm ya da NetID içeren herhangi bir paketi atmalıdır.

---

## 8. Paket Numaralandırma ve Oturum Ömrü

Her yön kendi 32-bit sayacını tutar.   - 0'dan başlar, paket başına artar.   - Devir yapmamalıdır; 2³²'ye ulaşmadan oturumu yeniden anahtarlayın veya sonlandırın.

Bağlantı kimlikleri, oturumun tamamı boyunca, geçiş sırasında da sabit kalır.

---

## 9. Veri Aşaması

- Tür = 6 (Veri)
- Kısa başlık (16 bayt)
- Yük, bir veya daha fazla şifreli blok içerir:
  - ACK/NACK listeleri
  - I2NP ileti parçaları
  - Dolgu (0–31 bayt rastgele)
  - Sonlandırma blokları (isteğe bağlı)

Seçici yeniden iletim ve sırasız teslim desteklenir. Güvenilirlik “yarı güvenilir” düzeyinde kalır — kayıp paketler, yeniden deneme sınırlarına ulaşıldıktan sonra sessizce düşürülebilir.

---

## 10. Aktarıcı ve NAT Geçişi

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Message</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Peer Test</td><td style="border:1px solid var(--color-border); padding:0.6rem;">7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Determines inbound reachability</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Retry</td><td style="border:1px solid var(--color-border); padding:0.6rem;">9</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Issues new token or rejection</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Token Request</td><td style="border:1px solid var(--color-border); padding:0.6rem;">10</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Requests new address token</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Hole Punch</td><td style="border:1px solid var(--color-border); padding:0.6rem;">11</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Coordinates NAT hole punching</td></tr>
  </tbody>
</table>
Aktarıcı router'lar, kısıtlayıcı NAT'lerin arkasındaki eşlere bu kontrol iletilerini kullanarak yardımcı olur.

---

## 11. Oturumun Sonlandırılması

Taraflardan herhangi biri, bir Data message (veri iletisi) içinde bir **Termination block** (sonlandırma bloğu) kullanarak oturumu kapatabilir. Alındıktan hemen sonra kaynaklar serbest bırakılmalıdır. Onaydan sonra tekrarlanan sonlandırma paketleri yok sayılabilir.

---

## 12. Uygulama Yönergeleri

Routers **MUST**: - version = 2 ve NetID = 2 değerlerini doğrulayın.   - 40 bayttan küçük paketleri veya geçersiz AEAD'i atın.   - 120 saniyelik yeniden oynatma önbelleğini zorunlu kılın.   - Yeniden kullanılan belirteçleri veya geçici anahtarları reddedin.

Routers **YAPMALIDIR**: - 0–31 bayt dolguyu rastgeleleştirin.   - Uyarlamalı yeniden iletim kullanın (RFC 6298).   - Taşımadan önce her eş için yol doğrulamasını uygulayın.

---

## 13. Güvenlik Özeti

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Property</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Achieved By</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Forward secrecy</td><td style="border:1px solid var(--color-border); padding:0.6rem;">X25519 ephemeral keys</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Replay protection</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Tokens + Bloom filter</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Authenticated encryption</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20/Poly1305</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">KCI resistance</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Noise XK pattern</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">DPI resistance</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypted headers</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">NAT traversal</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Relay + Hole Punch</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Migration</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Static connection IDs</td></tr>
  </tbody>
</table>
---

## 14. Referanslar

- [Öneri 159 – SSU2](/proposals/159-ssu2/)
- [Noise Protokolü Çerçevesi](https://noiseprotocol.org/noise.html)
- [RFC 9000 – QUIC Taşıma](https://datatracker.ietf.org/doc/html/rfc9000)
- [RFC 9001 – QUIC için TLS](https://datatracker.ietf.org/doc/html/rfc9001)
- [RFC 7539 – ChaCha20/Poly1305 AEAD (İlişkili Veri ile Kimlik Doğrulamalı Şifreleme)](https://datatracker.ietf.org/doc/html/rfc7539)
- [RFC 7748 – X25519 ECDH (Eliptik Eğri Diffie–Hellman)](https://datatracker.ietf.org/doc/html/rfc7748)
- [RFC 5869 – HKDF-SHA256 (HMAC tabanlı Ayıkla ve Genişlet Anahtar Türetme Fonksiyonu)](https://datatracker.ietf.org/doc/html/rfc5869)
