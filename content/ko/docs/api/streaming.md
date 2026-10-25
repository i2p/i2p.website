---
title: "Streaming Protocol"
description: "TCP-like transport used by most I2P applications"
slug: "streaming"
aliases:
  - "/ko/streaming"
  - "/ko/streaming/"
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

Java 구현에서 기본 최대 송신 및 수신 윈도우 크기는 128개 패킷입니다. 최대 송신 윈도우 크기를 128보다 높게 설정하는 구현체는 다음 문제들을 고려해야 합니다:

- One-phase connection setup using **SYN**, **ACK**, and **FIN** flags that can be bundled with payload data to reduce round-trips.
- **Sliding-window congestion control**, with slow start and congestion avoidance tuned for I2P’s high-latency environment.
- Packet compression (default 4KB compressed segments) balancing retransmission cost and fragmentation latency.
- Fully **authenticated, encrypted**, and **reliable** channel abstraction between I2P destinations.

수신자 구현을 위한 권장 최소 버퍼 크기는 128개 패킷 또는 232 KB (대략 128 * 1812)입니다. I2P 네트워크 지연 시간, 패킷 손실 및 그로 인한 혼잡 제어 때문에 이 크기의 버퍼가 가득 차는 경우는 드뭅니다. 그러나 고대역폭 "로컬 루프백" (동일 router) 연결이나 로컬 테스트에서는 오버플로우가 발생할 가능성이 훨씬 높습니다.

오버플로우 상황을 빠르게 표시하고 원활하게 복구하기 위해, 스트리밍 프로토콜에는 pushback을 위한 간단한 메커니즘이 있습니다. 60001 이상의 값을 가진 선택적 지연 필드가 있는 패킷이 수신되면, 이는 "choking" 또는 수신 윈도우가 0임을 나타냅니다. 60000 이하의 값을 가진 선택적 지연 필드가 있는 패킷은 "unchoking"을 나타냅니다. 선택적 지연 필드가 없는 패킷은 choke/unchoke 상태에 영향을 주지 않습니다.

choke된 후에는 전송자가 unchoke될 때까지 데이터가 포함된 패킷을 더 이상 전송해서는 안 되며, 가능한 손실된 unchoke 패킷을 보상하기 위한 가끔의 "probe" 데이터 패킷만 예외입니다. choke된 엔드포인트는 TCP에서처럼 프로빙을 제어하기 위해 "persist timer"를 시작해야 합니다. unchoking 엔드포인트는 이 필드가 설정된 패킷을 여러 개 전송하거나, 데이터 패킷이 다시 수신될 때까지 주기적으로 계속 전송해야 합니다. unchoking을 기다리는 최대 시간은 구현에 따라 다릅니다. unchoke된 후의 전송자 윈도우 크기와 혼잡 제어 전략은 구현에 따라 다릅니다.

### Congestion Control

스트리밍 라이브러리는 표준 slow-start (지수적 윈도우 증가)와 혼잡 회피 (선형 윈도우 증가) 단계를 지수적 백오프와 함께 사용합니다. 윈도잉과 승인 확인은 바이트 수가 아닌 패킷 수를 사용합니다.

### Latency Considerations

SYNCHRONIZE 플래그가 설정된 패킷을 포함하여 모든 패킷은 CLOSE 플래그도 함께 보낼 수 있습니다. 연결은 피어가 CLOSE 플래그로 응답할 때까지 닫히지 않습니다. CLOSE 패킷도 데이터를 포함할 수 있습니다.

### Ping / Pong {#ping}

I2CP 계층(ICMP echo와 동등한)이나 데이터그램에는 ping 기능이 없습니다. 이 기능은 스트리밍에서 제공됩니다. ping과 pong은 표준 스트리밍 패킷과 결합될 수 없습니다. ECHO 옵션이 설정되면 대부분의 다른 플래그, 옵션, ackThrough, sequenceNum, NACK 등은 무시됩니다.

ping 패킷은 ECHO, SIGNATURE_INCLUDED, FROM_INCLUDED 플래그가 설정되어 있어야 합니다. sendStreamId는 0보다 커야 하며, receiveStreamId는 무시됩니다. sendStreamId는 기존 연결과 일치할 수도 있고 일치하지 않을 수도 있습니다.

pong 패킷은 ECHO 플래그가 설정되어 있어야 합니다. sendStreamId는 0이어야 하며, receiveStreamId는 ping의 sendStreamId입니다. 릴리스 0.9.18 이전에는 pong 패킷에 ping에 포함된 페이로드가 포함되지 않습니다.

릴리스 0.9.18부터 ping과 pong은 페이로드를 포함할 수 있습니다. ping의 페이로드는 최대 32바이트까지 가능하며, pong에서 반환됩니다.

Streaming은 `i2p.streaming.answerPings=false` 설정을 통해 pong 전송을 비활성화하도록 구성할 수 있습니다.

### 0-RTT 문제점 {#0rtt}

위에서 언급한 바와 같이, TCP와 달리 streaming은 SYN 패킷에 데이터를 번들링하여 0-RTT 데이터 전송을 허용합니다. 이것이 선호되는 구현 방식입니다. 또한, streaming은 SYN 이후에 SYN-ACK를 받기 전에 추가 데이터 패킷들(초기 윈도우 크기까지)을 전송할 수 있도록 허용합니다. 이러한 패킷들은 0이 아닌 시퀀스 번호를 가지고, SYN 플래그가 설정되지 않으며, sendStreamID가 0입니다.

수신자는 핸드셰이크 중에 순서가 바뀌거나 손실된 패킷을 처리할 수 있도록 설계해야 하며, 여기에는 SYN보다 먼저 데이터 패킷이 도착하는 경우도 포함됩니다. 권장하는 구현 방법은 알려지지 않은 ID에 대한 non-SYN 패킷을 드롭하지 말고 큐에 저장한 후, SYN이 수신된 후 큐에서 검색하는 것입니다.

역방향에서도 상황은 비슷합니다. 연결 수신자(Bob)는 SYN-ACK 전송을 지연시키고(ACK DELAY) 애플리케이션으로부터의 데이터를 짧은 시간 동안 기다려야 합니다. 애플리케이션으로부터 데이터를 받으면, 해당 데이터를(최대 패킷 크기까지) SYN-ACK 패킷에 넣어서 전송합니다. 초기 윈도우 크기까지의 추가 데이터 패킷들도 SYN-ACK의 ACK를 기다리지 않고 전송될 수 있습니다.

발신자는 SYN-ACK를 받기 전에 수신된 모든 데이터 패킷을 버퍼링해야 하며, 이는 핸드셰이크 완료 후의 순서 이탈 처리와 동일합니다.

### 스트리밍 라이브러리 테스트 {#testing}

새로운 또는 변경된 스트리밍 라이브러리를 테스트하는 개발자를 위해, Java I2P는 지연시간, 패킷 손실, 지연 지터를 포함한 실제 네트워크 환경의 재현 가능한 테스트를 위한 간단한 로컬 테스트 유틸리티를 제공합니다. 이는 로컬 연결을 위한 I2CP 서버만을 구현하는 작은 스텁입니다.

개발자들은 10ms에서 최소 15초까지의 지연 시간과 0에서 10%까지의 패킷 손실을 포함한 다양한 일반적인 매개변수로 테스트해야 합니다. 지터를 추가하면 순서가 바뀐 패킷 처리를 쉽게 테스트할 수 있습니다.

이것은 두 애플리케이션 중 하나를 수동으로 중단시켜 버퍼 오버플로우(CHOKE/UNCHOKE)를 테스트하기에도 좋은 설정입니다.

i2p.i2p 소스 패키지에서:

- `I2PSocketManagerFactory` negotiates or reuses a router session via I2CP.  
- If no key is provided, a new destination is automatically generated.  
- Developers can pass I2CP options (e.g., tunnel lengths, encryption types, or connection settings) through the `options` map.  
- `I2PSocket` and `I2PServerSocket` mirror standard Java `Socket` interfaces, making migration straightforward.

### i2p.streaming.profile 참고사항 {#profile}

이 옵션은 두 가지 값을 지원합니다. 1=bulk, 2=interactive입니다. 이 옵션은 예상되는 트래픽 패턴에 대한 힌트를 streaming library 및/또는 router에 제공합니다.

"Bulk"는 지연 시간을 희생하더라도 높은 대역폭을 위해 최적화한다는 의미입니다. 이것이 기본값입니다. "Interactive"는 대역폭이나 효율성을 희생하더라도 낮은 지연 시간을 위해 최적화한다는 의미입니다. 최적화 전략이 있다면 구현에 따라 달라지며, 스트리밍 프로토콜 외부의 변경사항을 포함할 수 있습니다.

API 버전 0.9.63까지 Java I2P는 1(bulk) 이외의 값에 대해 오류를 반환하고 tunnel이 시작되지 않았습니다. API 0.9.64부터 Java I2P는 이 값을 무시합니다. API 버전 0.9.63까지 i2pd는 이 옵션을 무시했지만, API 0.9.64부터 i2pd에서 구현되었습니다.

streaming 프로토콜에는 프로필 설정을 상대방에게 전달하기 위한 플래그 필드가 포함되어 있지만, 이는 알려진 어떤 router에서도 구현되지 않았습니다.

### Control Block 공유 {#sharing}

streaming lib는 "TCP" Control Block 공유를 지원합니다. 이는 동일한 원격 피어에 대한 연결 간에 세 가지 중요한 streaming lib 매개변수(윈도우 크기, 왕복 시간, 왕복 시간 편차)를 공유합니다. 이는 연결 중의 "앙상블" 공유가 아닌 연결 열기/닫기 시점의 "시간적" 공유에 사용됩니다([RFC 2140](http://www.ietf.org/rfc/rfc2140.txt) 참조). 동일한 router의 다른 Destination에 정보가 누출되지 않도록 ConnectionManager당(즉, 로컬 Destination당) 별도의 공유가 있습니다. 주어진 피어의 공유 데이터는 몇 분 후에 만료됩니다. 다음 Control Block Sharing 매개변수는 router당 설정할 수 있습니다:

1. **SYN sent** — initiator includes optional data.  
2. **SYN/ACK response** — responder includes optional data.  
3. **ACK finalization** — establishes reliability and session state.  
4. **FIN/RESET** — used for orderly closure or abrupt termination.

### 기타 매개변수 {#other}

다음 매개변수들은 권장 기본값입니다. 기본값은 구현에 따라 다를 수 있습니다:

- The streaming layer continuously adapts to network latency and throughput via RTT-based feedback.  
- Applications perform best when routers are contributing peers (participating tunnels enabled).  
- TCP-like congestion control mechanisms prevent overloading slow peers and help balance bandwidth use across tunnels.

### 역사 {#history}

streaming 라이브러리는 I2P를 위해 유기적으로 성장해왔습니다. 처음에 mihi가 I2PTunnel의 일부로 "mini streaming library"를 구현했는데, 이는 윈도우 크기가 1개 메시지로 제한되어 있었습니다(다음 메시지를 보내기 전에 ACK가 필요했음). 이후 이것이 일반적인 streaming 인터페이스(TCP 소켓을 미러링)로 리팩토링되었고, 슬라이딩 윈도우 프로토콜과 높은 대역폭 x 지연 곱을 고려한 최적화가 적용된 완전한 streaming 구현이 배포되었습니다. 개별 stream은 최대 패킷 크기 및 기타 옵션을 조정할 수 있습니다. 기본 메시지 크기는 정확히 두 개의 1K I2NP tunnel 메시지에 맞도록 선택되며, 손실된 메시지 재전송의 대역폭 비용과 여러 메시지의 지연 시간 및 오버헤드 사이의 합리적인 절충안입니다.

## Interoperability and Best Practices

스트리밍 라이브러리의 동작은 애플리케이션 수준의 성능에 큰 영향을 미치므로, 추가 분석이 필요한 중요한 영역입니다.

- Always test against both **Java I2P** and **i2pd** to ensure full compatibility.  
- Although the protocol is standardized, minor implementation differences may exist.  
- Handle older routers gracefully—many peers still run pre-2.0 versions.  
- Monitor connection stats using `I2PSocket.getOptions()` and `getSession()` to read RTT and retransmission metrics.
