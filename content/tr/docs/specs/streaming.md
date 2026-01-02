---
title: "Akış Protokolü"
description: "Çoğu I2P uygulaması tarafından kullanılan, TCP benzeri güvenilir bir taşıma protokolü"
slug: "streaming"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## Genel Bakış

I2P Streaming Library (I2P Akış Kütüphanesi), I2P'nin güvenilir olmayan mesaj katmanının üzerinde — IP üzerinde TCP'ye benzer şekilde — güvenilir, sıralı ve kimliği doğrulanmış veri iletimi sağlar. Web gezintisi, IRC, e-posta ve dosya paylaşımı gibi etkileşimli I2P uygulamalarının neredeyse tamamı tarafından kullanılır.

I2P’nin yüksek gecikmeli anonim tunnel’ları üzerinden güvenilir iletim, tıkanıklık denetimi, yeniden iletim ve akış kontrolü sağlar. Her akış, hedefler arasında uçtan uca tamamen şifrelenir.

---

## Temel Tasarım İlkeleri

Akış kitaplığı, **tek aşamalı bir bağlantı kurulumu** uygular; burada SYN, ACK ve FIN bayrakları aynı mesajda veri yükleri taşıyabilir. Bu, yüksek gecikmeli ortamlarda gidiş-dönüşleri en aza indirir — küçük bir HTTP işlemi tek bir gidiş-dönüşte tamamlanabilir.

Tıkanıklık kontrolü ve yeniden iletim, TCP örnek alınarak modellenmiş, ancak I2P'nin ortamına uyarlanmıştır. Pencere boyutları bayt tabanlı değil, mesaj tabanlıdır ve tunnel gecikmesi ile ek yüke göre ayarlanmıştır. Protokol, TCP'nin AIMD algoritmasına benzer şekilde yavaş başlangıç, tıkanıklık önleme ve üstel geri çekilme destekler.

---

## Mimari

Akış kitaplığı, uygulamalar ile I2CP arayüzü arasında çalışır.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Layer</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Responsibility</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Application</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Standard I2PSocket and I2PServerSocket usage</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Streaming Library</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connection setup, sequencing, retransmission, and flow control</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2CP</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel creation, routing, and message handling</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2NP / Router Layer</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Transport through tunnels</td>
    </tr>
  </tbody>
</table>
Çoğu kullanıcı ona I2PSocketManager, I2PTunnel ya da SAMv3 aracılığıyla erişir. Kütüphane, destination (hedef) yönetimi, tunnel kullanımı ve yeniden iletimleri şeffaf bir şekilde ele alır.

---

## Paket Formatı

```
+-----------------------------------------------+
| Send Stream ID (4B) | Receive Stream ID (4B) |
+-----------------------------------------------+
| Sequence Number (4B) | Ack Through (4B)      |
+-----------------------------------------------+
| NACK Count (1B) | optional NACK list (4B each)
+-----------------------------------------------+
| Flags (1B) | Option Size (1B) | Options ...   |
+-----------------------------------------------+
| Payload ...                                  |
```
### Başlık Ayrıntıları

- **Akış Kimlikleri**: Yerel ve uzak akışları benzersiz şekilde tanımlayan 32-bit değerler.
- **Sıra Numarası**: SYN için 0'dan başlar, mesaj başına artar.
- **Ack Through**: (kümülatif onay) N değerine kadar olan tüm mesajları, NACK (olumsuz onay) listesindekiler hariç, onaylar.
- **Bayraklar**: Durumu ve davranışı kontrol eden bit maskesi.
- **Seçenekler**: RTT, MTU ve protokol görüşmesi için değişken uzunluklu liste.

### Anahtar Bayrakları

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Flag</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SYN</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connection initiation</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ACK</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Acknowledge received packets</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">FIN</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Graceful close</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RST</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reset connection</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">FROM_INCLUDED</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Sender’s destination included</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SIGNATURE_INCLUDED</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Message signed by sender</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECHO / ECHO_REPLY</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ping/Pong keepalive</td>
    </tr>
  </tbody>
</table>
---

## Akış Kontrolü ve Güvenilirlik

Streaming, TCP'nin bayt tabanlı yaklaşımının aksine, **mesaj tabanlı pencereleme** kullanır. Aktarım halindeki onaylanmamış paketlere izin verilen sayı, mevcut pencere boyutuna eşittir (varsayılan 128).

### Mekanizmalar

- **Tıkanıklık kontrolü:** Yavaş başlangıç ve AIMD (Toplamsal Artış, Çarpımsal Azalış) tabanlı kaçınma.  
- **Choke/Unchoke:** Arabellek doluluğuna dayalı akış kontrolü sinyallemesi.  
- **Yeniden iletim:** RFC 6298 tabanlı RTO (yeniden iletim zaman aşımı) hesaplaması ve üstel geri çekilme.  
- **Yinelenenleri filtreleme:** Potansiyel olarak yeniden sıralanmış iletiler üzerinde güvenilirliği sağlar.

Tipik yapılandırma değerleri:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Parameter</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Default</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>maxWindowSize</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Max unacknowledged messages</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>maxMessageSize</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1730</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Maximum payload bytes per message</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>initialRTO</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">9000 ms</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Initial retransmission timeout</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>inactivityTimeout</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">90000 ms</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Idle connection timeout</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>connectTimeout</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">300000 ms</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connection establishment timeout</td>
    </tr>
  </tbody>
</table>
---

## Bağlantı Kurulumu

1. **Başlatıcı** bir SYN gönderir (isteğe bağlı olarak payload (yük) ve FROM_INCLUDED ile).  
2. **Yanıtlayıcı** SYN+ACK ile yanıt verir (payload içerebilir).  
3. **Başlatıcı** kurulumu teyit eden son ACK'i gönderir.

İsteğe bağlı başlangıç yükleri, tam el sıkışma tamamlanmadan önce veri iletimine izin verir.

---

## Gerçekleme Ayrıntıları

### Yeniden İletim ve Zaman Aşımı

Yeniden iletim algoritması **RFC 6298**'e uyar.   - **Başlangıç RTO'su:** 9s   - **Minimum RTO:** 100ms   - **Maksimum RTO:** 45s   - **Alfa:** 0.125   - **Beta:** 0.25

### Kontrol Bloğu Paylaşımı

Aynı eşe yapılan sonraki bağlantılar, daha hızlı artış için önceki RTT (gidiş-dönüş süresi) ve pencere verilerini yeniden kullanarak “soğuk başlangıç” gecikmesinden kaçınır. Kontrol bloklarının süresi birkaç dakika içinde dolar.

### MTU ve Parçalama

- Varsayılan MTU: **1730 bayt** (iki I2NP mesajına sığar).  
- ECIES (Elliptic Curve Integrated Encryption Scheme - Eliptik Eğri Entegre Şifreleme Şeması) hedefleri: **1812 bayt** (azaltılmış ek yük).  
- Minimum desteklenen MTU: 512 bayt.

Faydalı yük boyutu, 22 baytlık asgari akış başlığını içermez.

---

## Sürüm Geçmişi

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Router Version</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.7.1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Protocol numbers defined in I2CP</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.11</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Variable-length signatures</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA signature support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ed25519 signature support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.18</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ping/Pong payloads</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.20</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">FROM_INCLUDED not required in RESET</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.36</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Protocol enforcement enabled by default</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.39</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">OFFLINE_SIGNATURE support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.58</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Bob’s hash added to NACK field in SYN</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Post-Quantum hybrid encryption (experimental)</td>
    </tr>
  </tbody>
</table>
---

## Uygulama Düzeyinde Kullanım

### Java Örneği

```java
Properties props = new Properties();
props.setProperty("i2p.streaming.maxWindowSize", "512");
I2PSocketManager mgr = I2PSocketManagerFactory.createManager(props);

I2PSocket socket = mgr.connect(destination);
InputStream in = socket.getInputStream();
OutputStream out = socket.getOutputStream();
```
### SAMv3 ve i2pd Desteği

- **SAMv3**: Java dışı istemciler için STREAM ve DATAGRAM kipleri sağlar.  
- **i2pd**: Yapılandırma dosyası seçenekleri aracılığıyla aynı akış parametrelerini sunar (örn. `i2p.streaming.maxWindowSize`, `profile`, vb.)

---

## Akış ve Datagramlar Arasında Seçim

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Use Case</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended Transport</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Reason</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HTTP, IRC, Email</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Streaming</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Requires reliability</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DNS</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Repliable Datagram</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Single request/response</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Telemetry, Logging</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Raw Datagram</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Best-effort acceptable</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P2P DHT</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Datagram</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">High connection churn</td>
    </tr>
  </tbody>
</table>
---

## Güvenlik ve Post-Kuantum Gelecek

Akış oturumları I2CP katmanında uçtan uca şifrelenir.   Post-kuantum hibrit şifreleme (ML-KEM + X25519) 2.10.0 sürümünde deneysel olarak desteklenir ancak varsayılan olarak devre dışıdır.

---

## Kaynaklar

- [Streaming API Genel Bakış](/docs/specs/streaming/)  
- [Streaming Protokolü Belirtimi](/docs/specs/streaming/)  
- [I2CP Belirtimi](/docs/specs/i2cp/)  
- [Öneri 144: Streaming MTU Hesaplamaları](/proposals/144-ecies-x25519-aead-ratchet/)  
- [I2P 2.10.0 Sürüm Notları](/tr/blog/2025/09/08/i2p-2.10.0-release/)
