---
title: "SOCKS Proxy"
description: "I2P'nin SOCKS tünelini güvenli şekilde kullanmak (2.10.0 için güncellenmiştir)"
slug: "socks"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

> **Dikkat:** SOCKS tüneli, uygulama yüklerini temizlemeden iletir. Birçok protokol IP'leri, ana bilgisayar adlarını veya diğer tanımlayıcıları sızdırır. SOCKS'u yalnızca anonimlik açısından denetlediğiniz yazılımlarla kullanın.

---

## 1. Genel Bakış

I2P, bir **I2PTunnel istemcisi** aracılığıyla giden bağlantılar için **SOCKS 4, 4a ve 5** proxy desteği sağlar. Standart uygulamaların I2P hedeflerine ulaşmasını sağlar ancak **clearnet'e erişemez**. **SOCKS outproxy yoktur** ve tüm trafik I2P ağı içinde kalır.

### Uygulama Özeti

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Parameter</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Java I2P</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">i2pd</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default Port</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">User-defined</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>127.0.0.1:4447</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported SOCKS Versions</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4, 4a, 5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4, 4a, 5</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UDP Mode</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stubbed (non-functional)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stubbed (non-functional)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Persistent Keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Since 0.9.9</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Shared Client Tunnels</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outproxy Support</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">❌ None</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">❌ None</td>
    </tr>
  </tbody>
</table>
**Desteklenen adres türleri:** - `.i2p` host adları (adres defteri girdileri) - Base32 hash'leri (`.b32.i2p`) - Base64 veya clearnet desteği yok

---

## 2. Güvenlik Riskleri ve Kısıtlamalar

### Uygulama Katmanı Sızıntısı

SOCKS, uygulama katmanının altında çalışır ve protokolleri temizleyemez. Birçok istemci (örneğin, tarayıcılar, IRC, e-posta) IP adresinizi, ana bilgisayar adınızı veya sistem ayrıntılarınızı ifşa eden meta veriler içerir.

Yaygın sızıntılar şunları içerir: - E-posta başlıklarında veya IRC CTCP yanıtlarında IP'ler   - Protokol yüklerinde gerçek isimler/kullanıcı adları   - İşletim sistemi parmak izleri içeren user-agent dizileri   - Harici DNS sorguları   - WebRTC ve tarayıcı telemetrisi

**I2P bu sızıntıları engelleyemez**—bunlar tünel katmanının üstünde gerçekleşir. SOCKS'u yalnızca anonimlik için tasarlanmış **denetlenmiş istemciler** için kullanın.

### Paylaşılan Tünel Kimliği

Birden fazla uygulama bir SOCKS tüneli paylaşıyorsa, aynı I2P hedef kimliğini paylaşırlar. Bu, farklı hizmetler arasında ilişkilendirme veya parmak izi oluşturma olanağı sağlar.

**Azaltma:** Her uygulama için **paylaşılmayan tunnel'lar** kullanın ve yeniden başlatmalar arasında tutarlı kriptografik kimlikleri korumak için **kalıcı anahtarları** etkinleştirin.

### UDP Modu Geçici Olarak Kapatıldı

SOCKS5'te UDP desteği uygulanmamıştır. Protokol UDP yeteneğini duyurur, ancak çağrılar göz ardı edilir. Yalnızca TCP kullanan istemciler kullanın.

### Tasarım Gereği Outproxy Yok

Tor'dan farklı olarak, I2P SOCKS tabanlı clearnet outproxy'leri **sunmaz**. Harici IP adreslerine ulaşma girişimleri başarısız olur veya kimliği açığa çıkarır. Outproxy gerekiyorsa HTTP veya HTTPS proxy'leri kullanın.

---

## 3. Tarihsel Bağlam

Geliştiriciler uzun zamandır anonim kullanım için SOCKS'u önermiyor. Dahili geliştirici tartışmalarından ve 2004'teki [Toplantı 81](/tr/blog/2004/03/16/i2p-dev-meeting-march-16-2004/) ve [Toplantı 82](/tr/blog/2004/03/23/i2p-dev-meeting-march-23-2004/)'den:

> "Rastgele trafiği yönlendirmek güvenli değildir ve anonimlik yazılımı geliştiricileri olarak son kullanıcılarımızın güvenliğini her şeyden önce düşünmemiz gerekir."

SOCKS desteği uyumluluk için dahil edilmiştir ancak üretim ortamları için önerilmez. Hemen hemen her internet uygulaması, anonim yönlendirme için uygun olmayan hassas meta verileri sızdırır.

---

## 4. Yapılandırma

### Java I2P

1. [I2PTunnel Manager](http://127.0.0.1:7657/i2ptunnel)'ı açın  
2. **"SOCKS 4/4a/5"** tipinde yeni bir istemci tunnel'ı oluşturun  
3. Seçenekleri yapılandırın:  
   - Yerel port (herhangi bir uygun port)  
   - Paylaşımlı istemci: uygulama başına ayrı kimlik için *devre dışı bırakın*  
   - Kalıcı anahtar: anahtar korelasyonunu azaltmak için *etkinleştirin*  
4. Tunnel'ı başlatın

### i2pd

i2pd varsayılan olarak `127.0.0.1:4447` adresinde etkinleştirilmiş SOCKS5 desteği içerir. `i2pd.conf` dosyasındaki `[SOCKSProxy]` bölümü altındaki yapılandırma, port, host ve tunnel parametrelerini ayarlamanıza olanak tanır.

---

## 5. Geliştirme Zaman Çizelgesi

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Change</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Date</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.7.1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Initial SOCKS 4/4a/5 support</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2010</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.9</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Added persistent keying</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2013</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1.7.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">BOB API deprecated and removed</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2022</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P-over-Tor blocked to improve network health</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2024</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Post-quantum hybrid encryption introduced</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2025</td>
    </tr>
  </tbody>
</table>
SOCKS modülünün kendisi 2013'ten bu yana büyük bir protokol güncellemesi görmedi, ancak çevresindeki tunnel yığını performans ve kriptografik iyileştirmeler aldı.

---

## 6. Önerilen Alternatifler

Herhangi bir **üretim**, **halka açık** veya **güvenlik açısından kritik** uygulama için, SOCKS yerine resmi I2P API'lerinden birini kullanın:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">API</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended For</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SAM v3 (3.3)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Simple Anonymous Messaging API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Cross-language apps needing socket-like I/O</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Streaming Library</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TCP-like sockets for Java</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Native Java integrations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2CP</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Low-level router communication</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Custom protocols, router-level integration</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>BOB</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated (removed 2022)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Legacy only; migrate to SAM</td>
    </tr>
  </tbody>
</table>
Bu API'ler uygun hedef izolasyonu, kriptografik kimlik kontrolü ve daha iyi yönlendirme performansı sağlar.

---

## 7. OnionCat / GarliCat

OnionCat, GarliCat modu (`fd60:db4d:ddb5::/48` IPv6 aralığı) aracılığıyla I2P'yi destekler. Hala çalışır durumda ancak 2019'dan beri sınırlı geliştirme ile.

**Kullanım uyarıları:** - SusiDNS'de manuel `.oc.b32.i2p` yapılandırması gerektirir   - Statik IPv6 ataması gerektirir   - I2P projesi tarafından resmi olarak desteklenmemektedir

Yalnızca gelişmiş VPN-over-I2P kurulumları için önerilir.

---

## 8. En İyi Uygulamalar

SOCKS kullanmanız gerekiyorsa: 1. Her uygulama için ayrı tunnel oluşturun.   2. Paylaşımlı istemci modunu devre dışı bırakın.   3. Kalıcı anahtarları etkinleştirin.   4. SOCKS5 DNS çözümlemesini zorunlu kılın.   5. Protokol davranışını sızıntılara karşı denetleyin.   6. Clearnet bağlantılarından kaçının.   7. Ağ trafiğini sızıntılara karşı izleyin.

---

## 9. Teknik Özet

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Parameter</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Supported SOCKS Versions</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4, 4a, 5</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Transport</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TCP only</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>UDP Support</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stubbed (non-functional)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Clearnet Access</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Not supported</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Default Ports</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Java I2P: user-set; i2pd: <code>127.0.0.1:4447</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Persistent Keying</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported since 0.9.9</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Shared Tunnels</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported (discouraged)</td>
    </tr>
  </tbody>
</table>
---

## 10. Sonuç

I2P'deki SOCKS proxy, mevcut TCP uygulamalarıyla temel uyumluluk sağlar ancak **güçlü anonimlik garantileri için tasarlanmamıştır**. Yalnızca kontrollü, denetlenmiş test ortamları için kullanılmalıdır.

> Ciddi dağıtımlar için **SAM v3** veya **Streaming API**'ye geçiş yapın. Bu API'ler uygulama kimliklerini izole eder, modern kriptografi kullanır ve sürekli geliştirme alır.

---

### Ek Kaynaklar

- [Resmi SOCKS Belgeleri](/docs/api/socks/)  
- [SAMv3 Spesifikasyonu](/docs/api/samv3/)  
- [Streaming Kütüphanesi Belgeleri](/docs/specs/streaming/)  
- [I2PTunnel Referansı](/docs/specs/implementation/)  
- [I2P Geliştirici Belgeleri](https://i2pgit.org/I2P_Developers/i2p.i2p)  
- [Topluluk Forumu](https://i2pforum.net)
