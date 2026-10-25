---
title: "Streaming Protocol"
description: "TCP-like transport used by most I2P applications"
slug: "streaming"
aliases:
  - "/tr/streaming"
  - "/tr/streaming/"
lastUpdated: "2026-01"
accurateFor: "0.9.68"
---

## Overview

The **I2P Streaming Library** provides reliable, in-order, authenticated transport over I2P’s message layer, similar to **TCP over IP**.   It sits above the [I2CP protocol](/docs/specs/i2cp/) and is used by nearly all interactive I2P applications, including HTTP proxies, IRC, BitTorrent, and email.

This design enables small HTTP requests and responses to complete in a single round-trip.   A SYN packet may carry the request payload, while the responder’s SYN/ACK/FIN may contain the full response body.

---

The Java streaming API mirrors standard Java socket programming:

Full Javadocs are available from the I2P router console or [here](/docs/specs/streaming/).

## API Basics

---

You can pass configuration properties when creating a socket manager via:

Newer features since version 0.9.4 include reject log suppression, DSA list support (0.9.21), and mandatory protocol enforcement (0.9.36).   Routers since 2.10.0 include post-quantum hybrid encryption (ML-KEM + X25519) at the transport layer.

### Core Characteristics

---

Each stream is identified by a **Stream ID**. Packets carry control flags similar to TCP: `SYNCHRONIZE`, `ACK`, `FIN`, and `RESET`.   Packets may contain both data and control flags simultaneously, improving efficiency for short-lived connections.

Because I2P tunnels introduce latency and message reordering, the library buffers packets from unknown or early-arriving streams.   Buffered messages are stored until synchronization completes, ensuring complete, in-order delivery.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Default</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2cp.accessList</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">null</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Comma- or space-separated list of Base64 peer Hashes used for either access list or blacklist. As of release 0.7.13.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2cp.destination.sigType</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DSA_SHA1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">The name or number of the signature type for a transient destination. As of release 0.9.12.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2cp.enableAccessList</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">false</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Use the access list as a whitelist for incoming connections. As of release 0.7.13.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2cp.enableBlackList</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">false</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Use the access list as a blacklist for incoming connections. As of release 0.7.13.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.answerPings</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">true</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Whether to respond to incoming pings</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.blacklist</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">null</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Comma- or space-separated list of Base64 peer Hashes to be blacklisted for incoming connections to ALL destinations in the context. This option must be set in the context properties, NOT in the createManager() options argument. Note that setting this in the router context will not affect clients outside the router in a separate JVM and context. As of release 0.9.3.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.bufferSize</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64K</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">How much transmit data (in bytes) will be accepted that hasn't been written out yet.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.congestionAvoidanceGrowthRateFactor</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">When we're in congestion avoidance, we grow the window size at the rate of <code>1/(windowSize*factor)</code>. In standard TCP, window sizes are in bytes, while in I2P, window sizes are in messages. A higher number means slower growth.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.connectDelay</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">-1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">How long to wait after instantiating a new con before actually attempting to connect. If this is &lt;= 0, connect immediately with no initial data. If greater than 0, wait until the output stream is flushed, the buffer fills, or that many milliseconds pass, and include any initial data with the SYN.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.connectTimeout</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5*60*1000</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">How long to block on connect, in milliseconds. Negative means indefinitely. Default is 5 minutes.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.disableRejectLogging</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">false</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Whether to disable warnings in the logs when an incoming connection is rejected due to connection limits. As of release 0.9.4.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.dsalist</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">null</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Comma- or space-separated list of Base64 peer Hashes or host names to be contacted using an alternate DSA destination. Only applies if multisession is enabled and the primary session is non-DSA (generally for shared clients only). This option must be set in the context properties, NOT in the createManager() options argument. Note that setting this in the router context will not affect clients outside the router in a separate JVM and context. As of release 0.9.21.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.enforceProtocol</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">true</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Whether to listen only for the streaming protocol. Setting to true will prohibit communication with Destinations earlier than release 0.7.1 (released March 2009). Set to true if running multiple protocols on this Destination. As of release 0.9.1. Default true as of release 0.9.36.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.inactivityAction</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2 (send)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">(0=noop, 1=disconnect) What to do on an inactivity timeout - do nothing, disconnect, or send a duplicate ack.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.inactivityTimeout</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">90*1000</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Idle time before sending a keepalive</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.initialAckDelay</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">750</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Delay before sending an ack</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.initialResendDelay</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1000</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">The initial value of the resend delay field in the packet header, times 1000. Not fully implemented; see below.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.initialRTO</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">9000</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Initial timeout (if no <a href="#sharing">sharing data</a> available). As of release 0.9.8.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.initialRTT</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">8000</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Initial round trip time estimate (if no <a href="#sharing">sharing data</a> available). Disabled as of release 0.9.8; uses actual RTT.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.initialWindowSize</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">(if no <a href="#sharing">sharing data</a> available) In standard TCP, window sizes are in bytes, while in I2P, window sizes are in messages.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.limitAction</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reset</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">What action to take when an incoming connection exceeds limits. Valid values are: reset (reset the connection); drop (drop the connection); or http (send a hardcoded HTTP 429 response). Any other value is a custom response to be sent. backslash-r and backslash-n will be replaced with CR and LF. As of release 0.9.34.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.maxConcurrentStreams</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">-1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">(0 or negative value means unlimited) This is a total limit for incoming and outgoing combined.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.maxConnsPerMinute</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Incoming connection limit (per peer; 0 means disabled). As of release 0.7.14.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.maxConnsPerHour</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">(per peer; 0 means disabled). As of release 0.7.14.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.maxConnsPerDay</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">(per peer; 0 means disabled). As of release 0.7.14.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.maxMessageSize</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1730</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">The maximum size of the payload, i.e. the MTU in bytes.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.maxResends</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">8</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Maximum number of retransmissions before failure.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.maxTotalConnsPerMinute</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Incoming connection limit (all peers; 0 means disabled). As of release 0.7.14.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.maxTotalConnsPerHour</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">(all peers; 0 means disabled) Use with caution as exceeding this will disable a server for a long time. As of release 0.7.14.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.maxTotalConnsPerDay</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">(all peers; 0 means disabled) Use with caution as exceeding this will disable a server for a long time. As of release 0.7.14.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.maxWindowSize</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.profile</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1 (bulk)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1=bulk; 2=interactive; see important notes <a href="#profile">below</a>.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.readTimeout</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">-1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">How long to block on read, in milliseconds. Negative means indefinitely.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.slowStartGrowthRateFactor</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">When we're in slow start, we grow the window size at the rate of 1/(factor). In standard TCP, window sizes are in bytes, while in I2P, window sizes are in messages. A higher number means slower growth.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.tcbcache.rttDampening</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.75</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ref: RFC 2140. Floating point value. May be set only via context properties, not connection options. As of release 0.9.8.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.tcbcache.rttdevDampening</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.75</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ref: RFC 2140. Floating point value. May be set only via context properties, not connection options. As of release 0.9.8.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.tcbcache.wdwDampening</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.75</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ref: RFC 2140. Floating point value. May be set only via context properties, not connection options. As of release 0.9.8.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.streaming.writeTimeout</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">-1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">How long to block on write/flush, in milliseconds. Negative means indefinitely.</td>
    </tr>
  </tbody>
</table>
## Configuration and Tuning

The option `i2p.streaming.enforceProtocol=true` (default since 0.9.36) ensures connections use the correct I2CP protocol number, preventing conflicts between multiple subsystems sharing one destination.

## Protocol Details

### Key Options

---

The streaming protocol coexists with the **Datagram API**, giving developers the choice between connection-oriented and connectionless transports.

### Behavior by Workload

Applications can reuse existing tunnels by running as **shared clients**, allowing multiple services to share the same destination.   While this reduces overhead, it increases cross-service correlation risk—use with care.

Because I2P adds several hundred milliseconds of base latency, applications should minimize round-trips.   Bundle data with connection setup where possible (e.g., HTTP requests in SYN).   Avoid designs relying on many small sequential exchanges.

---

Performance depends heavily on tunnel configuration:   - **Short tunnels (1–2 hops)** → lower latency, reduced anonymity.   - **Long tunnels (3+ hops)** → higher anonymity, increased RTT.

### Connection Lifecycle

---

### Fragmentation and Reordering

---

### Protocol Enforcement

The **I2P Streaming Library** is the backbone of all reliable communication within I2P.   It ensures in-order, authenticated, encrypted message delivery and provides a near drop-in replacement for TCP in anonymous environments.

### Shared Clients

To achieve optimal performance: - Minimize round-trips with SYN+payload bundling.   - Tune window and timeout parameters for your workload.   - Favor shorter tunnels for latency-sensitive applications.   - Use congestion-friendly designs to avoid overloading peers.

Java uygulamasında varsayılan maksimum iletim ve alma penceresi boyutu 128 pakettir. Maksimum iletim penceresi boyutunu 128'den yüksek olarak ayarlayan uygulamalar aşağıdaki konuları göz önünde bulundurmalıdır:

- One-phase connection setup using **SYN**, **ACK**, and **FIN** flags that can be bundled with payload data to reduce round-trips.
- **Sliding-window congestion control**, with slow start and congestion avoidance tuned for I2P’s high-latency environment.
- Packet compression (default 4KB compressed segments) balancing retransmission cost and fragmentation latency.
- Fully **authenticated, encrypted**, and **reliable** channel abstraction between I2P destinations.

Alıcı uygulamaları için önerilen minimum arabellek boyutu 128 paket veya 232 KB'dır (yaklaşık 128 * 1812). I2P ağ gecikmesi, paket kayıpları ve bunun sonucunda oluşan tıkanıklık kontrolü nedeniyle, bu boyuttaki bir arabellek nadiren dolar. Ancak taşma, yüksek bant genişlikli "yerel geri döngü" (aynı router) bağlantılarında veya yerel testlerde çok daha olası bir durumdur.

Taşma durumlarını hızlıca belirtmek ve sorunsuzca kurtarmak için, akış protokolünde basit bir geri itme mekanizması bulunmaktadır. 60001 veya daha yüksek değerli isteğe bağlı gecikme alanı ile bir paket alınırsa, bu "boğma" veya sıfır alma penceresi anlamına gelir. 60000 veya daha düşük değerli isteğe bağlı gecikme alanına sahip bir paket "boğmayı kaldırma" anlamına gelir. İsteğe bağlı gecikme alanı olmayan paketler boğma/boğmayı kaldırma durumunu etkilemez.

Choke edildikten sonra, muhtemel kayıp unchoke paketlerini telafi etmek için ara sıra gönderilen "probe" veri paketleri dışında, transmitter unchoke edilene kadar veri içeren başka paket gönderilmemelidir. Choke edilmiş endpoint, TCP'deki gibi probing'i kontrol etmek için bir "persist timer" başlatmalıdır. Unchoking endpoint bu alanı ayarlanmış olarak birkaç paket göndermeli veya veri paketleri tekrar alınana kadar bunları periyodik olarak göndermeye devam etmelidir. Unchoking için beklenecek maksimum süre implementasyona bağlıdır. Unchoke edildikten sonra transmitter pencere boyutu ve congestion control stratejisi implementasyona bağlıdır.

### Congestion Control

Streaming kütüphanesi standart yavaş başlama (üssel pencere büyütme) ve tıkanıklık önleme (doğrusal pencere büyütme) fazlarını üssel geri çekilme ile kullanır. Pencereleme ve onaylamalar bayt sayısı değil, paket sayısı kullanır.

### Latency Considerations

SYNCHRONIZE bayrağı ayarlanmış olanlar dahil herhangi bir paket, CLOSE bayrağını da gönderebilir. Bağlantı, eş CLOSE bayrağıyla yanıt verene kadar kapatılmaz. CLOSE paketleri de veri içerebilir.

### Ping / Pong {#ping}

I2CP katmanında (ICMP echo'ya eşdeğer) veya datagramlarda ping fonksiyonu bulunmaz. Bu fonksiyon streaming'de sağlanır. Ping'ler ve pong'lar standart bir streaming paketi ile birleştirilemez; ECHO seçeneği ayarlanırsa, diğer çoğu bayrak, seçenek, ackThrough, sequenceNum, NACK'ler vb. göz ardı edilir.

Bir ping paketi ECHO, SIGNATURE_INCLUDED ve FROM_INCLUDED bayraklarının ayarlanmış olması gerekir. sendStreamId sıfırdan büyük olmalıdır ve receiveStreamId göz ardı edilir. sendStreamId mevcut bir bağlantıya karşılık gelebilir veya gelmeyebilir.

Bir pong paketi ECHO bayrağının ayarlanmış olması gerekir. sendStreamId sıfır olmalıdır ve receiveStreamId ping'den gelen sendStreamId'dir. 0.9.18 sürümünden önce, pong paketi ping'de bulunan herhangi bir payload içermez.

0.9.18 sürümünden itibaren, ping ve pong mesajları bir yük içerebilir. Ping içindeki yük, maksimum 32 bayt olmak üzere, pong içinde geri döndürülür.

Streaming, i2p.streaming.answerPings=false yapılandırması ile pong gönderimini devre dışı bırakacak şekilde yapılandırılabilir.

### 0-RTT Sorunları {#0rtt}

Yukarıda belirtildiği gibi, TCP'den farklı olarak, streaming veriyi SYN paketine dahil ederek 0-RTT veri iletimi sağlar. Bu tercih edilen uygulamadır. AYRICA, streaming SYN-ACK alınmadan önce SYN'den sonra ek veri paketlerinin (başlangıç pencere boyutuna kadar) gönderilmesine izin verir. Bu paketler sıfır olmayan bir sıra numarasına sahip olacak, SYN bayrağı ayarlanmayacak ve sıfır sendStreamID'ye sahip olacaktır.

Alıcılar, handshake sırasında sıra dışı veya düşen paketler için tasarım yapmalıdır; bu, SYN'den önce veri paketlerinin gelmesi durumunu da içerir. Tercih edilen uygulama, bilinmeyen bir ID için SYN olmayan paketleri bırakmak yerine kuyruğa almak ve SYN alındıktan sonra bunları kuyruktan geri almaktır.

Ters yönde de durum benzerdir. Bağlantı alıcısı (Bob) SYN-ACK göndermeyi geciktirmeli (ACK DELAY) ve uygulamadan gelen veri için kısa bir süre beklemelidir. Uygulamadan veri aldığında, bunu (maksimum paket boyutuna kadar) SYN-ACK paketine koymalı ve göndermelidir. İlk pencere boyutuna kadar ek veri paketleri de SYN-ACK'nin ACK'sını beklemeden gönderilebilir.

Başlatıcı, SYN-ACK'den önce alınan tüm veri paketlerini tamponlamalıdır, bu da el sıkışma tamamlandıktan sonraki sıra dışı işleme ile aynıdır.

### Streaming Kütüphanelerini Test Etme {#testing}

Yeni veya değiştirilmiş streaming kütüphanelerini test eden geliştiriciler için Java I2P, gecikme, paket kaybı ve gecikme jitter'ı dahil gerçek ağ koşullarının tekrarlanabilir testleri için basit bir yerel test yardımcı programı sağlar. Bu, yalnızca yerel bağlantılar için I2CP sunucusu uygulayan küçük bir saplama programıdır.

Geliştiriciler, 10ms'den en az 15s'ye kadar gecikme ve %0 ile %10 arasında paket kaybı dahil olmak üzere geniş bir tipik parametre yelpazesi ile test etmelidir. Jitter eklemek, sıra dışı işleme testini kolaylaştırır.

Bu aynı zamanda iki uygulamadan birini manuel olarak askıya alarak buffer overflow (CHOKE/UNCHOKE) test etmek için iyi bir kurulum.

i2p.i2p kaynak paketinden:

- `I2PSocketManagerFactory` negotiates or reuses a router session via I2CP.  
- If no key is provided, a new destination is automatically generated.  
- Developers can pass I2CP options (e.g., tunnel lengths, encryption types, or connection settings) through the `options` map.  
- `I2PSocket` and `I2PServerSocket` mirror standard Java `Socket` interfaces, making migration straightforward.

### i2p.streaming.profile Notları {#profile}

Bu seçenek iki değeri destekler; 1=toplu ve 2=etkileşimli. Bu seçenek, streaming kütüphanesi ve/veya router'a beklenen trafik desenine dair bir ipucu sağlar.

"Bulk" yüksek bant genişliği için optimize etmeyi, muhtemelen gecikme pahasına yapmayı ifade eder. Bu varsayılan ayardır. "Interactive" düşük gecikme için optimize etmeyi, muhtemelen bant genişliği veya verimlilik pahasına yapmayı ifade eder. Optimizasyon stratejileri, varsa, uygulamaya bağlıdır ve akış protokolü dışındaki değişiklikleri de içerebilir.

API sürüm 0.9.63'e kadar, Java I2P 1 (toplu) dışındaki herhangi bir değer için hata döndürür ve tunnel başlatılamazdı. API 0.9.64 itibariyle, Java I2P bu değeri görmezden gelir. API sürüm 0.9.63'e kadar, i2pd bu seçeneği görmezden gelirdi; API 0.9.64 itibariyle i2pd'de uygulanmıştır.

Streaming protokolü profil ayarını diğer uca iletmek için bir bayrak alanı içerse de, bu özellik bilinen hiçbir router'da uygulanmamıştır.

### Kontrol Bloğu Paylaşımı {#sharing}

Streaming kütüphanesi "TCP" Kontrol Bloğu paylaşımını destekler. Bu, aynı uzak eşe (peer) yapılan bağlantılar arasında üç önemli streaming kütüphanesi parametresini (pencere boyutu, gidiş-dönüş süresi, gidiş-dönüş süresi varyansı) paylaşır. Bu, bağlantı sırasında "ensemble" paylaşım değil, bağlantı açma/kapama zamanında "temporal" paylaşım için kullanılır ([RFC 2140](http://www.ietf.org/rfc/rfc2140.txt)'a bakınız). Aynı router üzerindeki diğer Destination'lara bilgi sızıntısı olmaması için ConnectionManager başına (yani yerel Destination başına) ayrı bir paylaşım vardır. Belirli bir eş için paylaşım verisi birkaç dakika sonra sona erer. Aşağıdaki Kontrol Bloğu Paylaşım parametreleri router başına ayarlanabilir:

1. **SYN sent** — initiator includes optional data.  
2. **SYN/ACK response** — responder includes optional data.  
3. **ACK finalization** — establishes reliability and session state.  
4. **FIN/RESET** — used for orderly closure or abrupt termination.

### Diğer Parametreler {#other}

Aşağıdaki parametreler önerilen varsayılan değerlerdir. Varsayılan değerler uygulamaya bağlı olarak değişebilir:

- The streaming layer continuously adapts to network latency and throughput via RTT-based feedback.  
- Applications perform best when routers are contributing peers (participating tunnels enabled).  
- TCP-like congestion control mechanisms prevent overloading slow peers and help balance bandwidth use across tunnels.

### Geçmiş {#history}

Streaming kütüphanesi I2P için organik olarak büyüdü - önce mihi, I2PTunnel'ın bir parçası olarak "mini streaming kütüphanesini" uyguladı, bu da 1 mesajlık pencere boyutuyla sınırlıydı (bir sonrakini göndermeden önce ACK gerektiriyordu), daha sonra genel bir streaming arayüzüne (TCP soketlerini yansıtan) yeniden yapılandırıldı ve tam streaming uygulaması, kayan pencere protokolü ve yüksek bant genişliği x gecikme ürününü hesaba katacak optimizasyonlarla dağıtıldı. Bireysel akışlar maksimum paket boyutunu ve diğer seçenekleri ayarlayabilir. Varsayılan mesaj boyutu, tam olarak iki adet 1K I2NP tunnel mesajına sığacak şekilde seçilmiştir ve kayıp mesajları yeniden iletmenin bant genişliği maliyetleri ile birden fazla mesajın gecikme süresi ve ek yükü arasında makul bir dengeyi temsil eder.

## Interoperability and Best Practices

Streaming kütüphanesinin davranışı, uygulama seviyesindeki performans üzerinde derin bir etkiye sahiptir ve bu nedenle daha fazla analiz için önemli bir alandır.

- Always test against both **Java I2P** and **i2pd** to ensure full compatibility.  
- Although the protocol is standardized, minor implementation differences may exist.  
- Handle older routers gracefully—many peers still run pre-2.0 versions.  
- Monitor connection stats using `I2PSocket.getOptions()` and `getSession()` to read RTT and retransmission metrics.
