---
title: "Streaming Protocol"
description: "TCP-like transport used by most I2P applications"
slug: "streaming"
aliases:
  - "/de/streaming"
  - "/de/streaming/"
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

Die standardmäßige maximale Übertragung- und Empfangsfenstergröße in der Java-Implementierung beträgt 128 Pakete. Implementierungen, die eine maximale Übertragungsfenstergröße höher als 128 setzen, müssen die folgenden Probleme berücksichtigen:

- One-phase connection setup using **SYN**, **ACK**, and **FIN** flags that can be bundled with payload data to reduce round-trips.
- **Sliding-window congestion control**, with slow start and congestion avoidance tuned for I2P’s high-latency environment.
- Packet compression (default 4KB compressed segments) balancing retransmission cost and fragmentation latency.
- Fully **authenticated, encrypted**, and **reliable** channel abstraction between I2P destinations.

Die empfohlene minimale Puffergröße für Empfänger-Implementierungen beträgt 128 Pakete oder 232 KB (ungefähr 128 * 1812). Aufgrund der I2P-Netzwerk-Latenz, Paketverlusten und der daraus resultierenden Staukontrolle wird ein Puffer dieser Größe selten gefüllt. Ein Überlauf tritt jedoch viel wahrscheinlicher bei hochbandbreitigen "local loopback"-Verbindungen (gleicher router) oder bei lokalen Tests auf.

Um Überlaufsituationen schnell anzuzeigen und reibungslos davon zu erholen, gibt es einen einfachen Mechanismus für Rückstau im Streaming-Protokoll. Wenn ein Paket mit einem optionalen Verzögerungsfeld mit einem Wert von 60001 oder höher empfangen wird, zeigt dies "Choking" oder ein Empfangsfenster von Null an. Ein Paket mit einem optionalen Verzögerungsfeld mit einem Wert von 60000 oder weniger zeigt "Unchoking" an. Pakete ohne ein optionales Verzögerungsfeld beeinflussen den Choke/Unchoke-Zustand nicht.

Nach dem Drosseln sollten keine weiteren Pakete mit Daten gesendet werden, bis der Sender wieder entdrosselt wird, außer gelegentlichen "Probe"-Datenpaketen zum Ausgleich möglicher verlorener Entdrosselungspakete. Der gedrosselte Endpunkt sollte einen "Persistenz-Timer" starten, um das Probing zu steuern, wie bei TCP. Der entdrosselnde Endpunkt sollte mehrere Pakete mit diesem gesetzten Feld senden oder sie regelmäßig weiter senden, bis wieder Datenpakete empfangen werden. Die maximale Wartezeit für die Entdrosselung ist implementierungsabhängig. Die Senderfenstergröße und Staukontrollstrategie nach der Entdrosselung ist implementierungsabhängig.

### Congestion Control

Die streaming lib verwendet standardmäßige slow-start (exponentielles Fensterwachstum) und congestion avoidance (lineares Fensterwachstum) Phasen, mit exponentiellem Backoff. Windowing und Bestätigungen verwenden Paketanzahl, nicht Byte-Anzahl.

### Latency Considerations

Jedes Paket, einschließlich eines mit gesetztem SYNCHRONIZE-Flag, kann auch das CLOSE-Flag gesetzt haben. Die Verbindung wird nicht geschlossen, bis der Peer mit dem CLOSE-Flag antwortet. CLOSE-Pakete können ebenfalls Daten enthalten.

### Ping / Pong {#ping}

Es gibt keine Ping-Funktion auf der I2CP-Ebene (entspricht ICMP Echo) oder in Datagrammen. Diese Funktion wird im Streaming bereitgestellt. Pings und Pongs dürfen nicht mit einem Standard-Streaming-Paket kombiniert werden; wenn die ECHO-Option gesetzt ist, werden die meisten anderen Flags, Optionen, ackThrough, sequenceNum, NACKs usw. ignoriert.

Ein Ping-Paket muss die Flags ECHO, SIGNATURE_INCLUDED und FROM_INCLUDED gesetzt haben. Die sendStreamId muss größer als null sein, und die receiveStreamId wird ignoriert. Die sendStreamId kann einer bestehenden Verbindung entsprechen oder auch nicht.

Ein Pong-Paket muss das ECHO-Flag gesetzt haben. Die sendStreamId muss null sein, und die receiveStreamId ist die sendStreamId aus dem Ping. Vor Release 0.9.18 enthält das Pong-Paket keine Nutzdaten, die im Ping enthalten waren.

Ab Version 0.9.18 können Pings und Pongs eine Nutzlast enthalten. Die Nutzlast im Ping, bis zu maximal 32 Bytes, wird im Pong zurückgegeben.

Streaming kann so konfiguriert werden, dass das Senden von Pongs mit der Konfiguration i2p.streaming.answerPings=false deaktiviert wird.

### 0-RTT Probleme {#0rtt}

Wie oben erwähnt, ermöglicht Streaming im Gegensatz zu TCP die 0-RTT-Zustellung von Daten, indem Daten im SYN-Paket gebündelt werden. Dies ist die bevorzugte Implementierung. AUSSERDEM erlaubt Streaming zusätzliche Datenpakete (bis zur anfänglichen Fenstergröße), die nach dem SYN gesendet werden, bevor das SYN-ACK empfangen wird. Diese Pakete haben eine von Null verschiedene Sequenznummer, haben das SYN-Flag nicht gesetzt und haben eine sendStreamID von Null.

Empfänger sollten für ungeordnete oder verlorene Pakete während des Handshakes ausgelegt sein, einschließlich des Ankommens von Datenpaketen vor dem SYN. Die bevorzugte Implementierung ist es, Nicht-SYN-Pakete für eine unbekannte ID in eine Warteschlange einzureihen, anstatt sie zu verwerfen, und sie nach dem Empfang des SYN aus der Warteschlange abzurufen.

In umgekehrter Richtung sind die Abläufe ähnlich. Der Verbindungsempfänger (Bob) sollte das Senden des SYN-ACK verzögern (ACK DELAY) und kurz auf Daten von der Anwendung warten. Beim Erhalt von Daten von der Anwendung sollten diese (bis zur maximalen Paketgröße) in das SYN-ACK-Paket eingefügt und gesendet werden. Zusätzliche Datenpakete, bis zur anfänglichen Fenstergröße, können ebenfalls gesendet werden, ohne auf eine ACK-Bestätigung des SYN-ACK zu warten.

Der Ursprungssender sollte alle Datenpakete puffern, die vor dem SYN-ACK empfangen werden, genauso wie bei der Behandlung von Paketen außerhalb der Reihenfolge nach Abschluss des Handshakes.

### Testen von Streaming-Bibliotheken {#testing}

Für Entwickler, die neue oder geänderte Streaming-Bibliotheken testen, bietet Java I2P ein einfaches lokales Test-Hilfsprogramm für reproduzierbare Tests realer Netzwerkbedingungen, einschließlich Latenz, Paketverlust und Delay-Jitter. Es ist ein kleiner Stub, der nur einen I2CP-Server für lokale Verbindungen implementiert.

Entwickler sollten mit einer breiten Palette typischer Parameter testen, einschließlich Latenz von 10ms bis mindestens 15s und Paketverlust von 0 bis 10%. Das Hinzufügen von Jitter erleichtert das Testen der Behandlung von Paketen außer der Reihenfolge.

Dies ist auch eine gute Konfiguration, um Pufferüberläufe (CHOKE/UNCHOKE) zu testen, indem man eine der beiden Anwendungen manuell pausiert.

Aus dem i2p.i2p Quellcode-Paket:

- `I2PSocketManagerFactory` negotiates or reuses a router session via I2CP.  
- If no key is provided, a new destination is automatically generated.  
- Developers can pass I2CP options (e.g., tunnel lengths, encryption types, or connection settings) through the `options` map.  
- `I2PSocket` and `I2PServerSocket` mirror standard Java `Socket` interfaces, making migration straightforward.

### i2p.streaming.profile Hinweise {#profile}

Diese Option unterstützt zwei Werte; 1=bulk und 2=interactive. Die Option gibt der Streaming-Bibliothek und/oder dem router einen Hinweis auf das erwartete Verkehrsmuster.

"Bulk" bedeutet die Optimierung für hohe Bandbreite, möglicherweise auf Kosten der Latenz. Dies ist die Standardeinstellung. "Interactive" bedeutet die Optimierung für niedrige Latenz, möglicherweise auf Kosten der Bandbreite oder Effizienz. Optimierungsstrategien, falls vorhanden, sind implementierungsabhängig und können Änderungen außerhalb des Streaming-Protokolls beinhalten.

Bis zur API-Version 0.9.63 gab Java I2P einen Fehler für jeden anderen Wert als 1 (bulk) zurück und der tunnel konnte nicht gestartet werden. Ab API 0.9.64 ignoriert Java I2P den Wert. Bis zur API-Version 0.9.63 ignorierte i2pd diese Option; sie ist in i2pd ab API 0.9.64 implementiert.

Obwohl das Streaming-Protokoll ein Flag-Feld enthält, um die Profil-Einstellung an das andere Ende zu übertragen, ist dies in keinem bekannten router implementiert.

### Control Block Sharing {#sharing}

Die Streaming-Bibliothek unterstützt "TCP" Control Block Sharing. Dabei werden drei wichtige Parameter der Streaming-Bibliothek (Fenstergröße, Round-Trip-Zeit, Round-Trip-Zeit-Varianz) zwischen Verbindungen zum gleichen entfernten Peer geteilt. Dies wird für "temporäres" Sharing beim Öffnen/Schließen von Verbindungen verwendet, nicht für "Ensemble"-Sharing während einer Verbindung (Siehe [RFC 2140](http://www.ietf.org/rfc/rfc2140.txt)). Es gibt eine separate Freigabe pro ConnectionManager (d.h. pro lokale Destination), damit keine Informationen an andere Destinations auf demselben router weitergegeben werden. Die Freigabedaten für einen bestimmten Peer laufen nach wenigen Minuten ab. Die folgenden Control Block Sharing Parameter können pro router eingestellt werden:

1. **SYN sent** — initiator includes optional data.  
2. **SYN/ACK response** — responder includes optional data.  
3. **ACK finalization** — establishes reliability and session state.  
4. **FIN/RESET** — used for orderly closure or abrupt termination.

### Weitere Parameter {#other}

Die folgenden Parameter sind empfohlene Standardwerte. Standardwerte können variieren, abhängig von der Implementierung:

- The streaming layer continuously adapts to network latency and throughput via RTT-based feedback.  
- Applications perform best when routers are contributing peers (participating tunnels enabled).  
- TCP-like congestion control mechanisms prevent overloading slow peers and help balance bandwidth use across tunnels.

### Geschichte {#history}

Die streaming library ist organisch für I2P gewachsen - zuerst implementierte mihi die "Mini-Streaming-Bibliothek" als Teil von I2PTunnel, die auf eine Fenstergröße von 1 Nachricht beschränkt war (erforderte eine ACK vor dem Senden der nächsten), und dann wurde sie zu einer generischen Streaming-Schnittstelle refaktoriert (nach dem Vorbild von TCP-Sockets) und die vollständige Streaming-Implementierung wurde mit einem Sliding-Window-Protokoll und Optimierungen bereitgestellt, um das hohe Bandbreite × Verzögerungs-Produkt zu berücksichtigen. Einzelne Streams können die maximale Paketgröße und andere Optionen anpassen. Die Standard-Nachrichtengröße ist so gewählt, dass sie genau in zwei 1K I2NP tunnel messages passt und stellt einen vernünftigen Kompromiss zwischen den Bandbreitenkosten der Neuübertragung verlorener Nachrichten und der Latenz und dem Overhead mehrerer Nachrichten dar.

## Interoperability and Best Practices

Das Verhalten der Streaming-Bibliothek hat einen tiefgreifenden Einfluss auf die Anwendungsebenen-Performance und ist daher ein wichtiger Bereich für weitere Analysen.

- Always test against both **Java I2P** and **i2pd** to ensure full compatibility.  
- Although the protocol is standardized, minor implementation differences may exist.  
- Handle older routers gracefully—many peers still run pre-2.0 versions.  
- Monitor connection stats using `I2PSocket.getOptions()` and `getSession()` to read RTT and retransmission metrics.
