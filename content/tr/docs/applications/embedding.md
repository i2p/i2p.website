---
title: "I2P'yi Uygulamanıza Gömme"
description: "Uygulamanızla birlikte bir I2P router'ı sorumlu bir şekilde paketlemek için güncellenmiş pratik rehber"
slug: "embedding"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

I2P'yi uygulamanızla birlikte paketlemek, kullanıcıları dahil etmenin güçlü bir yoludur—ancak yalnızca router sorumlu bir şekilde yapılandırılmışsa.

## 1. Router Ekipleriyle Koordine Olun

- Paketlemeden önce **Java I2P** ve **i2pd** geliştiricileriyle iletişime geçin. Varsayılan ayarlarınızı gözden geçirebilir ve uyumluluk endişelerini vurgulayabilirler.
- Yığınınıza (stack) uygun router uygulamasını seçin:
  - **Java/Scala** → Java I2P
  - **C/C++** → i2pd
  - **Diğer diller** → bir router paketleyin ve [SAM v3](/docs/api/samv3/) veya [I2CP](/docs/specs/i2cp/) kullanarak entegre edin
- Router ikili dosyaları ve bağımlılıkları (Java runtime, ICU, vb.) için yeniden dağıtım koşullarını doğrulayın.

## 2. Önerilen Yapılandırma Varsayılanları

"Tükettiğinden fazlasını katkıda bulun" hedefini benimse. Modern varsayılan ayarlar, ağ sağlığı ve kararlılığına öncelik verir.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Setting</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended Default (2025)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Bandwidth share</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">80% for participating tunnels </td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel quantities</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2pd: 3 inbound / 3 outbound; Java I2P: 2 inbound / 2 outbound. </td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature &amp; encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Use Ed25519 (<code>SIGNATURE_TYPE=7</code>) and advertise ECIES-X25519 + ElGamal (<code>i2cp.leaseSetEncType=4,0</code>).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Client protocols</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Use SAM v3 or I2CP.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">API listeners</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Bind SAM/I2CP to <code>127.0.0.1</code> only. Disable if not needed.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UI toggles</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Expose bandwidth controls, logs, and an opt-in checkbox for participating tunnels.</td>
    </tr>
  </tbody>
</table>
### Katılımcı Tüneller Temel Öneme Sahip

Katılımcı tünelleri **devre dışı bırakmayın**.

1. Relay yapmayan router'lar kendileri daha kötü performans gösterir.
2. Ağ, gönüllü kapasite paylaşımına bağlıdır.
3. Örtü trafiği (relay edilen trafik) anonimliği artırır.

**Resmi minimumlar:** - Paylaşılan bant genişliği: ≥ 12 KB/s   - Floodfill otomatik katılım: ≥ 128 KB/s   - Önerilen: 2 gelen / 2 giden tünel (Java I2P varsayılanı)

## 3. Kalıcılık ve Yeniden Tohumlama

Kalıcı durum dizinleri (`netDb/`, profiller, sertifikalar) çalıştırmalar arasında korunmalıdır.

Kalıcılık olmadan, kullanıcılarınız her başlangıçta yeniden tohumlama (reseed) tetikleyecek—bu da performansı düşürür ve yeniden tohumlama sunucularındaki yükü artırır.

Kalıcılık mümkün değilse (örn. konteynerler veya geçici kurulumlar):

1. Yükleyiciye **1.000–2.000 router bilgisi** ekleyin.  
2. Halka açık sunucuların yükünü azaltmak için bir veya daha fazla özel reseed sunucusu çalıştırın.

Yapılandırma değişkenleri: - Temel dizin: `i2p.dir.base` - Yapılandırma dizini: `i2p.dir.config` - Yeniden ekim için `certificates/` dizinini dahil edin.

## 4. Güvenlik ve Maruziyet

- Router konsolunu (`127.0.0.1:7657`) yalnızca yerel olarak tutun.
- Arayüzü harici olarak açıyorsanız HTTPS kullanın.
- Gerekli değilse harici SAM/I2CP'yi devre dışı bırakın.
- Dahil edilen eklentileri gözden geçirin—yalnızca uygulamanızın desteklediği eklentileri ekleyin.
- Uzaktan konsol erişimi için her zaman kimlik doğrulama ekleyin.

**2.5.0'dan bu yana tanıtılan güvenlik özellikleri:** - Uygulamalar arası netDb izolasyonu (2.4.0+)   - DoS azaltma ve Tor engelleme listeleri (2.5.1)   - NTCP2 yoklama direnci (2.9.0)   - Floodfill router seçim iyileştirmeleri (2.6.0+)

## 5. Desteklenen API'ler (2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">API</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SAM v3 (3.3)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Active</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Recommended bridge for non-Java apps.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2CP</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Active</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stable protocol core, used internally by Java I2P.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2PControl</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Active</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">JSON-RPC API; plugin maintained.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>BOB</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">⚠️ Deprecated</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Removed from Java I2P since 1.7.0; use SAM v3 instead.</td>
    </tr>
  </tbody>
</table>
Tüm resmi belgeler `/docs/api/` altında bulunur — eski `/spec/samv3/` yolu **mevcut değildir**.

## 6. Ağ ve Portlar

Tipik varsayılan portlar: - 4444 – HTTP Proxy   - 4445 – HTTPS Proxy   - 7654 – I2CP   - 7656 – SAM Bridge   - 7657 – Router Console   - 7658 – Yerel I2P sitesi   - 6668 – IRC Proxy   - 9000–31000 – Rastgele router portu (UDP/TCP gelen)

Router'lar ilk çalıştırmada rastgele bir gelen bağlantı noktası seçer. Yönlendirme performansı artırır, ancak UPnP bunu otomatik olarak halledebilir.

## 7. Modern Değişiklikler (2024–2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Change</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Details</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU1 Transport</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Removed</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SSU2 is now the exclusive UDP transport.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2P-over-Tor</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Blocked</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Since 2.6.0 (July 2024).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Datagram2/3</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Added</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Authenticated, repliable datagram formats (2.9.0).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>LeaseSet service records</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Added</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Enables service discovery (Proposal 167).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Tunnel build parameters</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Improved</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Adaptive congestion handling (2.9.0+).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Post-quantum crypto</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Introduced (beta)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ML-KEM hybrid ratchet, opt-in from 2.10.0.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Java 17 requirement</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Announced</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Becomes mandatory in 2.11.0 (early 2026).</td>
    </tr>
  </tbody>
</table>
## 8. Kullanıcı Deneyimi ve Test

- I2P'nin ne yaptığını ve bant genişliğinin neden paylaşıldığını açıkla.
- Router tanılamaları sağla (bant genişliği, tunnel'lar, reseed durumu).
- Paketleri Windows, macOS ve Linux'ta test et (düşük RAM dahil).
- Hem **Java I2P** hem de **i2pd** eşleri ile birlikte çalışabilirliği doğrula.
- Ağ kesintilerinden ve düzgün olmayan çıkışlardan kurtarmayı test et.

## 9. Topluluk Kaynakları

- Forum: [i2pforum.net](https://i2pforum.net) veya I2P içinde `http://i2pforum.i2p`.  
- Kod: [i2pgit.org/I2P_Developers/i2p.i2p](https://i2pgit.org/I2P_Developers/i2p.i2p).  
- IRC (Irc2P ağı): `#i2p-dev`, `#i2pd`.  
  - `#i2papps` doğrulanmamış; mevcut olmayabilir.  
  - Kanalınızın hangi ağda (Irc2P vs ilita.i2p) barındırıldığını belirtin.

Sorumlu bir şekilde gömme, kullanıcı deneyimi, performans ve ağa katkı arasında denge kurmak anlamına gelir. Bu varsayılanları kullanın, router geliştiricileriyle senkronize kalın ve yayınlamadan önce gerçek dünya yükü altında test edin.
