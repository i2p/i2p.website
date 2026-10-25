---
title: "Streaming Protocol"
description: "TCP-like transport used by most I2P applications"
slug: "streaming"
aliases:
  - "/vi/streaming"
  - "/vi/streaming/"
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

Kích thước cửa sổ truyền và nhận tối đa mặc định trong triển khai Java là 128 gói tin. Các triển khai đặt kích thước cửa sổ truyền tối đa cao hơn 128 phải xem xét các vấn đề sau:

- One-phase connection setup using **SYN**, **ACK**, and **FIN** flags that can be bundled with payload data to reduce round-trips.
- **Sliding-window congestion control**, with slow start and congestion avoidance tuned for I2P’s high-latency environment.
- Packet compression (default 4KB compressed segments) balancing retransmission cost and fragmentation latency.
- Fully **authenticated, encrypted**, and **reliable** channel abstraction between I2P destinations.

Kích thước buffer tối thiểu được khuyến nghị cho các triển khai receiver là 128 packets hoặc 232 KB (khoảng 128 * 1812). Do độ trễ mạng I2P, packet drops, và kiểm soát tắc nghẽn kết quả, buffer có kích thước này hiếm khi bị đầy. Tuy nhiên, tràn buffer có khả năng xảy ra cao hơn nhiều trên các kết nối "local loopback" băng thông cao (cùng router) hoặc trong kiểm thử cục bộ.

Để nhanh chóng báo hiệu và phục hồi mượt mà từ các tình trạng tràn bộ đệm, có một cơ chế đơn giản để đẩy ngược trong giao thức streaming. Nếu một gói tin được nhận với trường delay tùy chọn có giá trị 60001 hoặc cao hơn, điều đó cho biết trạng thái "choking" hoặc cửa sổ nhận bằng không. Một gói tin với trường delay tùy chọn có giá trị 60000 hoặc thấp hơn cho biết trạng thái "unchoking". Các gói tin không có trường delay tùy chọn sẽ không ảnh hưởng đến trạng thái choke/unchoke.

Sau khi bị choke, không nên gửi thêm gói tin nào có dữ liệu cho đến khi transmitter được unchoke, ngoại trừ các gói tin dữ liệu "thăm dò" thỉnh thoảng để bù đắp cho các gói tin unchoke có thể bị mất. Endpoint bị choke nên bắt đầu một "persist timer" để kiểm soát việc thăm dò, như trong TCP. Endpoint thực hiện unchoke nên gửi một số gói tin với trường này được thiết lập, hoặc tiếp tục gửi chúng định kỳ cho đến khi nhận được gói tin dữ liệu trở lại. Thời gian tối đa để chờ unchoke phụ thuộc vào implementation. Kích thước cửa sổ transmitter và chiến lược kiểm soát tắc nghẽn sau khi được unchoke phụ thuộc vào implementation.

### Congestion Control

Thư viện streaming sử dụng các giai đoạn slow-start chuẩn (tăng trưởng cửa sổ theo cấp số nhân) và tránh tắc nghẽn (tăng trưởng cửa sổ tuyến tính), với exponential backoff. Windowing và acknowledgments sử dụng số lượng gói tin, không phải số byte.

### Latency Considerations

Bất kỳ gói tin nào, bao gồm cả gói tin có cờ SYNCHRONIZE được đặt, cũng có thể được gửi kèm với cờ CLOSE. Kết nối sẽ không được đóng cho đến khi peer phản hồi với cờ CLOSE. Các gói tin CLOSE cũng có thể chứa dữ liệu.

### Ping / Pong {#ping}

Không có chức năng ping tại lớp I2CP (tương đương với ICMP echo) hoặc trong datagram. Chức năng này được cung cấp trong streaming. Ping và pong không thể kết hợp với gói streaming tiêu chuẩn; nếu tùy chọn ECHO được thiết lập, thì hầu hết các cờ, tùy chọn, ackThrough, sequenceNum, NACK khác, v.v. sẽ bị bỏ qua.

Gói ping phải có các cờ ECHO, SIGNATURE_INCLUDED, và FROM_INCLUDED được thiết lập. sendStreamId phải lớn hơn không, và receiveStreamId sẽ được bỏ qua. sendStreamId có thể hoặc không tương ứng với một kết nối đang tồn tại.

Một gói pong phải có cờ ECHO được thiết lập. sendStreamId phải bằng không, và receiveStreamId là sendStreamId từ ping. Trước phiên bản 0.9.18, gói pong không bao gồm bất kỳ payload nào có trong ping.

Từ phiên bản phát hành 0.9.18, các ping và pong có thể chứa payload. Payload trong ping, tối đa 32 byte, sẽ được trả về trong pong.

Streaming có thể được cấu hình để vô hiệu hóa việc gửi pong bằng cách thiết lập i2p.streaming.answerPings=false.

### Các Vấn Đề 0-RTT {#0rtt}

Như đã lưu ý ở trên, không giống như TCP, streaming cho phép truyền dữ liệu 0-RTT bằng cách gộp dữ liệu vào gói SYN. Đây là cách triển khai được ưu tiên. NGOÀI RA, streaming cho phép các gói dữ liệu bổ sung (tối đa bằng kích thước cửa sổ ban đầu) được gửi sau SYN, trước khi nhận được SYN-ACK. Những gói này sẽ có số thứ tự khác không, sẽ không có cờ SYN được đặt, và sẽ có sendStreamID bằng không.

Các bên nhận nên thiết kế để xử lý các gói tin bị lộn xộn thứ tự hoặc bị mất trong quá trình handshake, bao gồm việc các gói tin dữ liệu đến trước gói SYN. Cách triển khai được khuyên dùng là xếp hàng đợi, không loại bỏ, các gói tin không phải SYN cho một ID không xác định, và lấy chúng từ hàng đợi sau khi nhận được gói SYN.

Theo chiều ngược lại, mọi thứ cũng tương tự. Người nhận kết nối (Bob) nên trì hoãn việc gửi SYN-ACK (ACK DELAY) và đợi một khoảng thời gian ngắn để nhận dữ liệu từ ứng dụng. Khi nhận được dữ liệu từ ứng dụng, đặt nó (tối đa là kích thước gói tin tối đa) vào gói tin SYN-ACK và gửi đi. Các gói tin dữ liệu bổ sung, tối đa đến kích thước cửa sổ ban đầu, cũng có thể được gửi mà không cần đợi ACK của SYN-ACK.

Bên khởi tạo nên đệm các gói dữ liệu nhận được trước SYN-ACK, tương tự như việc xử lý không theo thứ tự sau khi quá trình bắt tay hoàn tất.

### Kiểm thử Thư viện Streaming {#testing}

Đối với các nhà phát triển đang thử nghiệm các thư viện streaming mới hoặc đã thay đổi, Java I2P cung cấp một tiện ích thử nghiệm cục bộ đơn giản để thử nghiệm có thể tái tạo các điều kiện mạng thực tế, bao gồm độ trễ, mất gói tin và jitter độ trễ. Đây là một stub nhỏ chỉ triển khai một máy chủ I2CP cho các kết nối cục bộ.

Các nhà phát triển nên kiểm thử với một phạm vi rộng các tham số điển hình, bao gồm độ trễ từ 10ms đến ít nhất 15s, và tỷ lệ mất gói từ 0 đến 10%. Thêm jitter giúp dễ dàng kiểm thử việc xử lý các gói tin không theo thứ tự.

Đây cũng là một thiết lập tốt để kiểm tra tràn bộ đệm (CHOKE/UNCHOKE) bằng cách tạm dừng thủ công một trong hai ứng dụng.

Từ gói mã nguồn i2p.i2p:

- `I2PSocketManagerFactory` negotiates or reuses a router session via I2CP.  
- If no key is provided, a new destination is automatically generated.  
- Developers can pass I2CP options (e.g., tunnel lengths, encryption types, or connection settings) through the `options` map.  
- `I2PSocket` and `I2PServerSocket` mirror standard Java `Socket` interfaces, making migration straightforward.

### Ghi chú về i2p.streaming.profile {#profile}

Tùy chọn này hỗ trợ hai giá trị; 1=bulk và 2=interactive. Tùy chọn này cung cấp gợi ý cho thư viện streaming và/hoặc router về mẫu lưu lượng dự kiến.

"Bulk" có nghĩa là tối ưu hóa cho băng thông cao, có thể phải đánh đổi độ trễ. Đây là mặc định. "Interactive" có nghĩa là tối ưu hóa cho độ trễ thấp, có thể phải đánh đổi băng thông hoặc hiệu suất. Các chiến lược tối ưu hóa, nếu có, phụ thuộc vào cách triển khai và có thể bao gồm các thay đổi bên ngoài giao thức streaming.

Qua phiên bản API 0.9.63, Java I2P sẽ trả về lỗi cho bất kỳ giá trị nào khác ngoài 1 (bulk) và tunnel sẽ không khởi động được. Từ API 0.9.64 trở đi, Java I2P bỏ qua giá trị này. Qua phiên bản API 0.9.63, i2pd đã bỏ qua tùy chọn này; nó được triển khai trong i2pd từ API 0.9.64.

Mặc dù giao thức streaming bao gồm một trường flag để truyền cài đặt profile đến đầu kia, điều này không được triển khai trong bất kỳ router nào đã biết.

### Chia sẻ Control Block {#sharing}

Thư viện streaming hỗ trợ chia sẻ "TCP" Control Block. Điều này chia sẻ ba tham số quan trọng của thư viện streaming (kích thước cửa sổ, thời gian khứ hồi, phương sai thời gian khứ hồi) giữa các kết nối tới cùng một peer từ xa. Tính năng này được sử dụng cho chia sẻ "tạm thời" tại thời điểm mở/đóng kết nối, không phải chia sẻ "tập hợp" trong suốt một kết nối (Xem [RFC 2140](http://www.ietf.org/rfc/rfc2140.txt)). Có một chia sẻ riêng biệt cho mỗi ConnectionManager (tức là mỗi Destination cục bộ) để không có rò rỉ thông tin sang các Destination khác trên cùng một router. Dữ liệu chia sẻ cho một peer nhất định sẽ hết hạn sau vài phút. Các tham số Control Block Sharing sau đây có thể được thiết lập cho mỗi router:

1. **SYN sent** — initiator includes optional data.  
2. **SYN/ACK response** — responder includes optional data.  
3. **ACK finalization** — establishes reliability and session state.  
4. **FIN/RESET** — used for orderly closure or abrupt termination.

### Các Tham Số Khác {#other}

Các tham số sau đây là giá trị mặc định được khuyến nghị. Giá trị mặc định có thể khác nhau, tùy thuộc vào cách triển khai:

- The streaming layer continuously adapts to network latency and throughput via RTT-based feedback.  
- Applications perform best when routers are contributing peers (participating tunnels enabled).  
- TCP-like congestion control mechanisms prevent overloading slow peers and help balance bandwidth use across tunnels.

### Lịch sử {#history}

Thư viện streaming đã phát triển một cách tự nhiên cho I2P - đầu tiên mihi đã triển khai "mini streaming library" như một phần của I2PTunnel, được giới hạn ở kích thước cửa sổ là 1 message (yêu cầu ACK trước khi gửi message tiếp theo), sau đó nó được tái cấu trúc thành một giao diện streaming tổng quát (phản ánh TCP sockets) và triển khai streaming đầy đủ được triển khai với giao thức sliding window và các tối ưu hóa để tính đến sản phẩm băng thông cao x độ trễ. Các stream riêng lẻ có thể điều chỉnh kích thước packet tối đa và các tùy chọn khác. Kích thước message mặc định được chọn để phù hợp chính xác với hai tunnel message I2NP 1K, và là một sự cân bằng hợp lý giữa chi phí băng thông của việc truyền lại các message bị mất và độ trễ cùng overhead của nhiều message.

## Interoperability and Best Practices

Hành vi của thư viện streaming có tác động sâu sắc đến hiệu suất ở cấp độ ứng dụng, và do đó, đây là một lĩnh vực quan trọng cần được phân tích thêm.

- Always test against both **Java I2P** and **i2pd** to ensure full compatibility.  
- Although the protocol is standardized, minor implementation differences may exist.  
- Handle older routers gracefully—many peers still run pre-2.0 versions.  
- Monitor connection stats using `I2PSocket.getOptions()` and `getSession()` to read RTT and retransmission metrics.
