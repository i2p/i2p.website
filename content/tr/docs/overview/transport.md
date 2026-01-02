---
title: "Taşıma Katmanı"
description: "I2P'nin taşıma katmanını anlamak - NTCP2 ve SSU2 dahil olmak üzere routers arasında nokta-nokta iletişim yöntemleri"
slug: "transport"
lastUpdated: "2025-03"
accurateFor: "2.10.0"
---

---

## 1. Genel Bakış

I2P'de bir **taşıma**, routers arasında doğrudan, noktadan noktaya iletişim yöntemidir. Bu mekanizmalar, router kimliğini doğrularken gizlilik ve bütünlüğü güvence altına alır.

Her bir aktarım, kimlik doğrulama, akış kontrolü, onaylar ve yeniden iletim yetenekleri içeren bağlantı modellerini kullanarak çalışır.

---

## 2. Mevcut Taşıma Protokolleri

I2P şu anda iki birincil taşıma protokolünü destekler:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Transport</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NTCP2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TCP</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise-based TCP transport with modern encryption (as of 0.9.36)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UDP</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Secure Semireliable UDP with modern encryption (as of 0.9.56)</td>
    </tr>
  </tbody>
</table>
### 2.1 Eski Taşıma Protokolleri (Kullanımdan Kaldırılmış)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Transport</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NTCP</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TCP</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Replaced by NTCP2; removed in 0.9.62</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UDP</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Replaced by SSU2; removed in 0.9.62</td>
    </tr>
  </tbody>
</table>
---

## 3. Taşıma Hizmetleri

Taşıma alt sistemi aşağıdaki hizmetleri sunar:

### 3.1 Mesaj Teslimi

- Güvenilir [I2NP](/docs/specs/i2np/) mesaj teslimi (taşıma protokolleri I2NP mesajlaşmasını münhasıran ele alır)
- Sıraya uygun teslimat evrensel olarak **GARANTİ EDİLMEZ**
- Öncelik temelli mesaj kuyruklama

### 3.2 Bağlantı Yönetimi

- Bağlantı kurulumu ve kapatılması
- Eşik değerlerinin uygulanmasıyla bağlantı sınırı yönetimi
- Her eş için durum takibi
- Otomatik ve manuel eş yasaklılar listesi uygulanması

### 3.3 Ağ Yapılandırması

- Her taşıma için birden çok router adresi (IPv4 ve IPv6 desteği v0.9.8'den beri)
- UPnP ile güvenlik duvarında bağlantı noktası açma
- NAT/güvenlik duvarı geçiş desteği
- Birden çok yöntemle yerel IP tespiti

### 3.4 Güvenlik

- Noktadan noktaya iletişim için şifreleme
- IP adreslerinin yerel kurallara göre doğrulanması
- Saat uzlaşısının belirlenmesi (yedek olarak NTP)

### 3.5 Bant Genişliği Yönetimi

- Gelen ve giden bant genişliği sınırları
- Giden iletiler için en uygun taşıma protokolü seçimi

---

## 4. Taşıma Adresleri

Alt sistem, router iletişim noktaları listesini sürdürür:

- Taşıma yöntemi (NTCP2, SSU2)
- IP adresi
- Port numarası
- İsteğe bağlı parametreler

Her taşıma yöntemi için birden fazla adres mümkündür.

### 4.1 Yaygın Adres Yapılandırmaları

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Configuration</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Hidden</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Routers with no published addresses</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Firewalled</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Routers publishing SSU2 addresses with "introducer" peer lists for NAT traversal</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Unrestricted</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Routers advertising both NTCP2 and SSU2 addresses on IPv4 and/or IPv6</td>
    </tr>
  </tbody>
</table>
---

## 5. Taşıma Seçimi

Sistem, üst katman protokollerinden bağımsız olarak [I2NP mesajları](/docs/specs/i2np/) için taşıma protokollerini seçer. Seçim, her taşıma protokolünün teklif sunduğu ve en düşük teklifin kazandığı bir **teklif verme sistemi** kullanır.

### 5.1 Teklif Belirleme Faktörleri

- Taşıma tercih ayarları
- Mevcut eş bağlantıları
- Mevcut ile eşik bağlantı sayıları
- Son bağlantı denemeleri geçmişi
- Mesaj boyutu kısıtları
- Eş RouterInfo (router bilgisi) taşıma yetenekleri
- Bağlantı doğrudanlığı (doğrudan veya introducer (aracılık eden düğüm) bağımlı)
- Eşin ilan ettiği taşıma tercihleri

Genellikle, iki router aynı anda tek bir transport (taşıma) bağlantısını sürdürür; ancak eşzamanlı çoklu transport bağlantıları da mümkündür.

---

## 6. NTCP2

**NTCP2** (Yeni Taşıma Protokolü 2), I2P için TCP tabanlı modern bir taşıma protokolüdür ve 0.9.36 sürümünde tanıtılmıştır.

### 6.1 Temel Özellikler

- **Noise Protocol Framework**'e (gürültü protokol çerçevesi) dayalı (Noise_XK pattern)
- Anahtar değişimi için **X25519** kullanır
- Kimliği doğrulanmış şifreleme için **ChaCha20/Poly1305** kullanır
- Karma için **BLAKE2s** kullanır
- DPI'ye (Deep Packet Inspection - derin paket inceleme) karşı dayanım için protokol gizleme
- Trafik analizi direnci için isteğe bağlı dolgu

### 6.2 Bağlantı Kurulumu

1. **Oturum İsteği** (Alice → Bob): Geçici X25519 anahtarı + şifreli yük
2. **Oturum Oluşturuldu** (Bob → Alice): Geçici anahtar + şifreli onay
3. **Oturum Onaylandı** (Alice → Bob): RouterInfo ile son el sıkışması

Bunu izleyen tüm veriler, el sıkışmadan türetilen oturum anahtarlarıyla şifrelenir.

Tüm ayrıntılar için [NTCP2 Şartnamesi](/docs/specs/ntcp2/) belgesine bakın.

---

## 7. SSU2

**SSU2** (Secure Semireliable UDP 2), I2P için modern UDP tabanlı taşıma protokolüdür ve 0.9.56 sürümünde tanıtılmıştır.

### 7.1 Temel Özellikler

- **Noise Protocol Framework** (gürültü protokol çerçevesi) (Noise_XK deseni) üzerine kuruludur
- Anahtar değişimi için **X25519** kullanır
- Kimliği doğrulanmış şifreleme için **ChaCha20/Poly1305** kullanır
- Seçmeli onaylarla yarı güvenilir veri teslimi
- Delik açma ve aktarma/tanıştırma yoluyla NAT geçişi
- Bağlantı taşınması desteği
- Yol MTU keşfi

### 7.2 SSU (Eski) ile karşılaştırıldığında avantajlar

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">SSU (Legacy)</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">SSU2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ElGamal + AES</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519 + ChaCha20/Poly1305</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Header encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Partial</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Full (ChaCha20)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connection ID</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fixed</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypted, rotatable</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NAT traversal</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Basic introduction</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Enhanced hole punching + relay</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Obfuscation</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Minimal</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Improved (variable padding)</td>
    </tr>
  </tbody>
</table>
Tüm ayrıntılar için [SSU2 Specification](/docs/specs/ssu2/) belgesine bakın.

---

## 8. NAT Geçişi

Her iki taşıma yöntemi de, güvenlik duvarı arkasındaki router'ların ağa katılabilmesi için NAT geçişini destekler.

### 8.1 SSU2'ye Giriş

Bir router doğrudan gelen bağlantıları kabul edemediğinde:

1. Router, **introducer** (tanıştırıcı) adreslerini kendi RouterInfo'sunda yayımlar
2. Bağlanan eş, introducer'a bir tanıştırma isteği gönderir
3. Introducer, bağlantı bilgilerini güvenlik duvarı arkasındaki router'a iletir
4. Güvenlik duvarı arkasındaki router, giden bağlantıyı başlatır (hole punch - delik delme)
5. Doğrudan iletişim kurulur

### 8.2 NTCP2 ve Güvenlik Duvarları

NTCP2, gelen TCP bağlantısı gerektirir. NAT arkasındaki router'lar şunları yapabilir:

- Portları otomatik olarak açmak için UPnP kullanın
- Port yönlendirmesini manuel olarak yapılandırın
- Gelen bağlantılar için SSU2'ye güvenirken gidenler için NTCP2 kullanın

---

## 9. Protokol Gizleme

Her iki modern taşıma protokolü de obfuscation (trafik gizleme) özellikleri barındırır:

- **Rastgele dolgu** el sıkışma iletilerinde
- **Şifrelenmiş başlıklar** protokol imzalarını ifşa etmez
- **Değişken uzunluklu iletiler** trafik analizine direnmek için
- **Sabit kalıplar yok** bağlantı kurulumu sırasında

> **Not**: Taşıma katmanı gizleme, I2P'nin tunnel mimarisinin sağladığı anonimliğin yerine geçmez; onu tamamlar.

---

## 10. Gelecekteki Geliştirmeler

Planlanan araştırmalar ve iyileştirmeler şunları içerir:

- **Pluggable transports (takılabilir taşıma protokolleri)** – Tor ile uyumlu gizleme eklentileri
- **QUIC-based transport** – QUIC protokolünün faydalarının incelenmesi
- **Connection limit optimization** – En uygun eş bağlantı sınırlarına yönelik araştırma
- **Enhanced padding strategies** – Trafik analizine karşı direncin artırılması

---

## 11. Referanslar

- [NTCP2 Spesifikasyonu](/docs/specs/ntcp2/) – Noise tabanlı TCP taşıma
- [SSU2 Spesifikasyonu](/docs/specs/ssu2/) – Güvenli, yarı güvenilir UDP 2
- [I2NP Spesifikasyonu](/docs/specs/i2np/) – I2P Ağ Protokolü mesajları
- [Ortak Yapılar](/docs/specs/common-structures/) – RouterInfo ve adres yapıları
- [Tarihsel NTCP Tartışması](/docs/ntcp/) – Eski taşıma geliştirme geçmişi
- [Eski SSU Dokümantasyonu](/docs/legacy/ssu/) – Orijinal SSU spesifikasyonu (kullanımdan kaldırıldı)
