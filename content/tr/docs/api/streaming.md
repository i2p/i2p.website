---
title: "Akış Protokolü"
description: "Çoğu I2P uygulaması tarafından kullanılan TCP benzeri taşıma protokolü"
slug: "streaming"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Genel Bakış

**I2P Streaming Library** (Akış Kütüphanesi), I2P'nin mesaj katmanı üzerinde güvenilir, sıralı ve kimliği doğrulanmış iletim sağlar; **IP üzerinden TCP**'ye benzer şekilde çalışır. [I2CP protokolü](/docs/specs/i2cp/)'nün üstünde yer alır ve HTTP proxy'leri, IRC, BitTorrent ve e-posta dahil olmak üzere neredeyse tüm etkileşimli I2P uygulamaları tarafından kullanılır.

### Temel Özellikler

- Gidiş-dönüş sayısını azaltmak için yük verisiyle birlikte paketlenebilen **SYN**, **ACK** ve **FIN** bayraklarını kullanan tek fazlı bağlantı kurulumu.
- I2P'nin yüksek gecikmeli ortamına uyarlanmış yavaş başlangıç ve tıkanıklık önleme ile **kayan pencere tıkanıklık kontrolü**.
- Yeniden iletim maliyeti ve parçalanma gecikmesi arasında denge kuran paket sıkıştırma (varsayılan 4KB sıkıştırılmış segmentler).
- I2P destinasyonları arasında tamamen **kimliği doğrulanmış, şifrelenmiş** ve **güvenilir** kanal soyutlaması.

Bu tasarım, küçük HTTP isteklerinin ve yanıtlarının tek bir gidiş-dönüş içinde tamamlanmasını sağlar. Bir SYN paketi istek yükünü taşıyabilirken, yanıtlayanın SYN/ACK/FIN paketi tam yanıt gövdesini içerebilir.

---

## API Temelleri

Java streaming API'si standart Java soket programlamayı yansıtır:

```java
I2PSocketManager mgr = I2PSocketManagerFactory.createManager(host, port, options);
I2PSocket socket       = mgr.connect(destination);
I2PServerSocket server = mgr.getServerSocket();
```
- `I2PSocketManagerFactory`, I2CP üzerinden bir router oturumunu müzakere eder veya yeniden kullanır.
- Eğer bir anahtar sağlanmazsa, yeni bir destination otomatik olarak oluşturulur.
- Geliştiriciler, I2CP seçeneklerini (örn. tunnel uzunlukları, şifreleme türleri veya bağlantı ayarları) `options` haritası aracılığıyla iletebilirler.
- `I2PSocket` ve `I2PServerSocket`, standart Java `Socket` arayüzlerini yansıtarak geçişi kolaylaştırır.

Tam Javadocs belgeleri I2P router konsolundan veya [buradan](/docs/specs/streaming/) erişilebilir.

---

## Yapılandırma ve Ayarlama

Bir socket manager oluştururken yapılandırma özelliklerini şu şekilde iletebilirsiniz:

```java
I2PSocketManagerFactory.createManager(host, port, properties);
```
### Anahtar Seçenekleri

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Default</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.maxWindowSize</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Maximum send window (bytes)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128 KB</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.initialRTO</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Initial retransmission timeout</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">9s</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.inactivityTimeout</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Timeout before connection close</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">90s</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.enforceProtocol</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Enforce protocol ID (prevents confusion)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">true</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.congestionAlgorithm</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Congestion control method</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default (AIMD TCP-like)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.disableRejectLogging</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Disable logging rejected packets</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">false</td>
    </tr>
  </tbody>
</table>
### İş Yüküne Göre Davranış

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Workload</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended Settings</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>HTTP-like</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default parameters are ideal.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Bulk Transfer</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Increase window size to 256 KB or 512 KB; lengthen timeouts.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Real-time Streaming</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Lower tunnel length to 1-2 hops; adjust RTO downwards.</td>
    </tr>
  </tbody>
</table>
Sürüm 0.9.4'ten bu yana eklenen yeni özellikler arasında reddetme günlüğü bastırma, DSA liste desteği (0.9.21) ve zorunlu protokol uygulaması (0.9.36) bulunmaktadır. 2.10.0 sürümünden itibaren router'lar, aktarım katmanında kuantum sonrası hibrit şifreleme (ML-KEM + X25519) içermektedir.

---

## Protokol Detayları

Her akış bir **Stream ID** (Akış Kimliği) ile tanımlanır. Paketler TCP'ye benzer kontrol bayrakları taşır: `SYNCHRONIZE`, `ACK`, `FIN` ve `RESET`. Paketler aynı anda hem veri hem de kontrol bayrakları içerebilir, bu da kısa ömürlü bağlantılar için verimliliği artırır.

### Bağlantı Yaşam Döngüsü

1. **SYN gönderildi** — başlatıcı isteğe bağlı veri içerir.  
2. **SYN/ACK yanıtı** — yanıtlayıcı isteğe bağlı veri içerir.  
3. **ACK sonlandırması** — güvenilirlik ve oturum durumunu oluşturur.  
4. **FIN/RESET** — düzenli kapanış veya ani sonlandırma için kullanılır.

### Parçalama ve Yeniden Sıralama

I2P tünelleri gecikme ve mesaj yeniden sıralamasına neden olduğundan, kütüphane bilinmeyen veya erken gelen akışlardan paketleri tamponlar. Tamponlanmış mesajlar senkronizasyon tamamlanana kadar saklanır ve böylece eksiksiz, sıralı teslimat sağlanır.

### Protokol Uygulaması

`i2p.streaming.enforceProtocol=true` seçeneği (0.9.36 sürümünden beri varsayılan) bağlantıların doğru I2CP protokol numarasını kullanmasını sağlar ve tek bir hedefi paylaşan birden fazla alt sistem arasındaki çakışmaları önler.

---

## Birlikte Çalışabilirlik ve En İyi Uygulamalar

Akış protokolü **Datagram API** ile birlikte çalışır ve geliştiricilere bağlantı yönelimli ve bağlantısız aktarım yöntemleri arasında seçim yapma imkanı sunar.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Use Case</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended Transport</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reliable, ordered data (HTTP, IRC, FTP)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Streaming</strong></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connectionless or lossy data (DNS, telemetry)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Datagram</strong></td>
    </tr>
  </tbody>
</table>
### Paylaşımlı İstemciler

Uygulamalar, **paylaşımlı istemciler** olarak çalışarak mevcut tunnel'ları yeniden kullanabilir, bu sayede birden fazla hizmetin aynı hedefi paylaşmasına olanak tanır. Bu yöntem yükü azaltırken, hizmetler arası ilişkilendirme riskini artırır—dikkatli kullanın.

### Tıkanıklık Kontrolü

- Streaming katmanı, RTT tabanlı geri bildirim yoluyla ağ gecikmesine ve verimi sürekli olarak uyarlar.
- Uygulamalar, yönlendiriciler katkıda bulunan eşler olduğunda (katılımcı tüneller etkinleştirildiğinde) en iyi performansı gösterir.
- TCP benzeri tıkanıklık kontrol mekanizmaları, yavaş eşlerin aşırı yüklenmesini önler ve tüneller arasında bant genişliği kullanımını dengelemeye yardımcı olur.

### Gecikme Süreleri Hakkında Dikkat Edilmesi Gerekenler

I2P birkaç yüz milisaniyelik temel gecikme eklediğinden, uygulamalar gidiş-dönüş sayısını en aza indirmelidir. Mümkün olduğunda verileri bağlantı kurulumu ile birleştirin (örneğin, SYN içinde HTTP istekleri). Birçok küçük sıralı veri alışverişine dayanan tasarımlardan kaçının.

---

## Test ve Uyumluluk

- Tam uyumluluğu sağlamak için her zaman hem **Java I2P** hem de **i2pd**'ye karşı test edin.
- Protokol standardize edilmiş olsa da küçük uygulama farklılıkları bulunabilir.
- Eski router'ları nazikçe ele alın—birçok eş hala 2.0 öncesi sürümleri çalıştırıyor.
- RTT ve yeniden iletim metriklerini okumak için `I2PSocket.getOptions()` ve `getSession()` kullanarak bağlantı istatistiklerini izleyin.

Performans, tünel yapılandırmasına büyük ölçüde bağlıdır:   - **Kısa tunneller (1–2 hop)** → düşük gecikme, azaltılmış anonimlik.   - **Uzun tunneller (3+ hop)** → yüksek anonimlik, artmış RTT.

---

## Temel İyileştirmeler (2.0.0–2.10.0)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Introduced</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Persistent ACK Bundling</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.0.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Optimized round-trip reduction for HTTP workloads.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Adaptive Window Scaling</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.3.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Improved large file transfer stability.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Thread Pooling and Socket Reuse</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.5.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reduced per-connection overhead.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Protocol Enforcement Default</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.36</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ensures correct stream usage.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Hybrid ML-KEM Ratchet</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Adds post-quantum hybrid encryption layer.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>i2pd Streaming API Compatibility Fixes</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.9.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Full parity with Java I2P library behavior.</td>
    </tr>
  </tbody>
</table>
---

## Özet

**I2P Streaming Library**, I2P içindeki tüm güvenilir iletişimin omurgasıdır. Sıralı, kimliği doğrulanmış, şifrelenmiş mesaj teslimatını sağlar ve anonim ortamlarda TCP için neredeyse hazır bir alternatif sunar.

Optimum performans elde etmek için: - SYN+payload paketlemesi ile gidiş-dönüş sayısını minimize edin.   - Pencere ve zaman aşımı parametrelerini iş yükünüze göre ayarlayın.   - Gecikmeye duyarlı uygulamalar için daha kısa tunnel'ları tercih edin.   - Eşleri (peer) aşırı yüklemekten kaçınmak için tıkanıklık dostu tasarımlar kullanın.
