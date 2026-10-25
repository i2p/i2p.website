---
title: "Streaming Protocol"
description: "TCP-like transport used by most I2P applications"
slug: "streaming"
aliases:
  - "/ar/streaming"
  - "/ar/streaming/"
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

الحد الأقصى الافتراضي لحجم نافذة الإرسال والاستقبال في تطبيق Java هو 128 حزمة. التطبيقات التي تحدد حداً أقصى لحجم نافذة الإرسال أعلى من 128 يجب أن تأخذ في الاعتبار المسائل التالية:

- One-phase connection setup using **SYN**, **ACK**, and **FIN** flags that can be bundled with payload data to reduce round-trips.
- **Sliding-window congestion control**, with slow start and congestion avoidance tuned for I2P’s high-latency environment.
- Packet compression (default 4KB compressed segments) balancing retransmission cost and fragmentation latency.
- Fully **authenticated, encrypted**, and **reliable** channel abstraction between I2P destinations.

الحد الأدنى الموصى به لحجم المخزن المؤقت لتطبيقات المستقبِل هو 128 حزمة أو 232 كيلوبايت (تقريباً 128 * 1812). بسبب زمن الاستجابة في شبكة I2P وفقدان الحزم والتحكم في الازدحام الناتج عن ذلك، نادراً ما يتم ملء مخزن مؤقت بهذا الحجم. ومع ذلك، فإن الفيض أكثر احتمالاً للحدوث في اتصالات "local loopback" عالية النطاق الترددي (نفس الـ router) أو في الاختبار المحلي.

للإشارة السريعة والتعافي السلس من حالات الفيض، توجد آلية بسيطة للدفع العكسي في بروتوكول التدفق. إذا تم استقبال حزمة بحقل تأخير اختياري بقيمة 60001 أو أعلى، فهذا يشير إلى "الخنق" أو نافذة استقبال بقيمة صفر. الحزمة التي تحتوي على حقل تأخير اختياري بقيمة 60000 أو أقل تشير إلى "إلغاء الخنق". الحزم التي لا تحتوي على حقل تأخير اختياري لا تؤثر على حالة الخنق/إلغاء الخنق.

بعد التعرض للاختناق، يجب عدم إرسال المزيد من الحزم التي تحتوي على بيانات حتى يتم إلغاء اختناق المرسل، باستثناء حزم البيانات "الاستطلاعية" العرضية للتعويض عن حزم إلغاء الاختناق المحتملة المفقودة. يجب على النقطة النهائية المختنقة بدء "مؤقت الثبات" للتحكم في الاستطلاع، كما هو الحال في TCP. يجب على النقطة النهائية التي تلغي الاختناق إرسال عدة حزم مع تعيين هذا الحقل، أو الاستمرار في إرسالها بشكل دوري حتى يتم استقبال حزم البيانات مرة أخرى. الحد الأقصى لوقت انتظار إلغاء الاختناق يعتمد على التنفيذ. حجم نافذة المرسل واستراتيجية التحكم في الازدحام بعد إلغاء الاختناق يعتمد على التنفيذ.

### Congestion Control

تستخدم مكتبة الـ streaming الطرق المعيارية للبدء البطيء (النمو الأسي للنافذة) ومراحل تجنب الازدحام (النمو الخطي للنافذة)، مع التراجع الأسي. تستخدم النوافذ والإقرارات عدد الحزم، وليس عدد البايتات.

### Latency Considerations

أي حزمة، بما في ذلك التي تحتوي على علم SYNCHRONIZE، قد تحتوي أيضًا على علم CLOSE. لا يتم إغلاق الاتصال حتى يستجيب النظير بعلم CLOSE. قد تحتوي حزم CLOSE على بيانات أيضًا.

### Ping / Pong {#ping}

لا توجد وظيفة ping في طبقة I2CP (مكافئة لـ ICMP echo) أو في datagrams. هذه الوظيفة متوفرة في streaming. لا يمكن دمج Pings و pongs مع حزمة streaming قياسية؛ إذا تم تعيين خيار ECHO، فإن معظم الأعلام والخيارات الأخرى و ackThrough و sequenceNum و NACKs وما إلى ذلك يتم تجاهلها.

يجب أن تحتوي حزمة ping على العلامات ECHO و SIGNATURE_INCLUDED و FROM_INCLUDED. يجب أن يكون sendStreamId أكبر من الصفر، ويتم تجاهل receiveStreamId. قد يتطابق sendStreamId مع اتصال موجود أو قد لا يتطابق.

يجب أن تحتوي حزمة pong على علامة ECHO مُعيَّنة. يجب أن يكون sendStreamId صفراً، وreceiveStreamId هو sendStreamId من ping. قبل الإصدار 0.9.18، حزمة pong لا تتضمن أي بيانات مُحمَّلة كانت موجودة في ping.

اعتباراً من الإصدار 0.9.18، قد تحتوي pings و pongs على حمولة بيانات. الحمولة في ping، بحد أقصى 32 بايت، يتم إرجاعها في pong.

يمكن تكوين Streaming لتعطيل إرسال pongs مع التكوين i2p.streaming.answerPings=false.

### مشاكل 0-RTT {#0rtt}

كما ذُكر أعلاه، على عكس TCP، يسمح streaming بتسليم البيانات بـ 0-RTT من خلال تجميع البيانات في حزمة SYN. هذا هو التنفيذ المفضل. أيضاً، يسمح streaming بإرسال حزم بيانات إضافية (حتى حجم النافذة الأولي) بعد SYN، قبل استلام SYN-ACK. هذه الحزم ستحمل رقم تسلسل غير صفري، ولن تحتوي على علامة SYN، وستحمل sendStreamID بقيمة صفر.

يجب على المستقبلات أن تصمم للتعامل مع الحزم غير المرتبة أو المفقودة أثناء المصافحة، بما في ذلك وصول حزم البيانات قبل SYN. التنفيذ المفضل هو وضع حزم غير-SYN للمعرف غير المعروف في طابور انتظار بدلاً من إسقاطها، واسترجاعها من الطابور بعد استلام SYN.

في الاتجاه العكسي، الأمور متشابهة. يجب على مستقبل الاتصال (Bob) تأخير إرسال SYN-ACK (ACK DELAY) والانتظار لفترة قصيرة للحصول على البيانات من التطبيق. عند استقبال البيانات من التطبيق، ضعها (حتى الحد الأقصى لحجم الحزمة) في حزمة SYN-ACK وأرسلها. قد يتم أيضاً إرسال حزم بيانات إضافية، حتى حجم النافذة الأولي، دون انتظار ACK للـ SYN-ACK.

يجب على المُرسِل الأصلي تخزين أي حزم بيانات مستلمة قبل SYN-ACK مؤقتاً، بنفس طريقة التعامل مع الحزم غير المرتبة بعد اكتمال المصافحة.

### اختبار مكتبات التدفق {#testing}

للمطورين الذين يختبرون مكتبات البث الجديدة أو المُحدثة، يوفر Java I2P أداة اختبار محلية بسيطة لاختبار قابل للتكرار لظروف الشبكة الحقيقية، بما في ذلك زمن الاستجابة وفقدان الحزم وتذبذب التأخير. إنها عبارة عن stub صغير يطبق فقط خادم I2CP للاتصالات المحلية.

يجب على المطورين إجراء الاختبارات مع مجموعة واسعة من المعاملات النموذجية، بما في ذلك زمن الاستجابة من 10 مللي ثانية إلى 15 ثانية على الأقل، وفقدان الحزم من 0 إلى 10%. إضافة التذبذب يجعل من السهل اختبار التعامل مع الحزم غير المرتبة.

هذا أيضاً إعداد جيد لاختبار تجاوز المخزن المؤقت (CHOKE/UNCHOKE) عن طريق تعليق إحدى التطبيقين يدوياً.

من حزمة المصدر i2p.i2p:

- `I2PSocketManagerFactory` negotiates or reuses a router session via I2CP.  
- If no key is provided, a new destination is automatically generated.  
- Developers can pass I2CP options (e.g., tunnel lengths, encryption types, or connection settings) through the `options` map.  
- `I2PSocket` and `I2PServerSocket` mirror standard Java `Socket` interfaces, making migration straightforward.

### ملاحظات i2p.streaming.profile {#profile}

يدعم هذا الخيار قيمتين؛ 1=bulk و 2=interactive. يوفر الخيار تلميحاً لمكتبة التدفق و/أو router حول نمط حركة البيانات المتوقع.

"Bulk" يعني التحسين من أجل عرض نطاق ترددي عالي، ربما على حساب زمن الاستجابة. هذا هو الإعداد الافتراضي. "Interactive" يعني التحسين من أجل زمن استجابة منخفض، ربما على حساب عرض النطاق الترددي أو الكفاءة. استراتيجيات التحسين، إن وجدت، تعتمد على التنفيذ، وقد تشمل تغييرات خارج بروتوكول البث المتدفق.

حتى إصدار API 0.9.63، كان Java I2P يُرجع خطأ لأي قيمة غير 1 (bulk) وكان tunnel يفشل في البدء. اعتباراً من API 0.9.64، Java I2P يتجاهل القيمة. حتى إصدار API 0.9.63، كان i2pd يتجاهل هذا الخيار؛ تم تنفيذه في i2pd اعتباراً من API 0.9.64.

بينما يتضمن بروتوكول التدفق حقل علامة لتمرير إعداد الملف الشخصي إلى الطرف الآخر، إلا أن هذا غير مطبق في أي router معروف.

### مشاركة Control Block {#sharing}

تدعم مكتبة streaming مشاركة "TCP" Control Block. هذا يشارك ثلاثة معاملات مهمة في مكتبة streaming (حجم النافذة، وقت الرحلة الدائرية، تباين وقت الرحلة الدائرية) عبر الاتصالات إلى نفس النظير البعيد. يُستخدم هذا للمشاركة "الزمنية" في وقت فتح/إغلاق الاتصال، وليس المشاركة "الجماعية" أثناء الاتصال (انظر [RFC 2140](http://www.ietf.org/rfc/rfc2140.txt)). هناك مشاركة منفصلة لكل ConnectionManager (أي لكل Destination محلي) بحيث لا يحدث تسرب معلومات إلى Destinations أخرى على نفس router. تنتهي صلاحية بيانات المشاركة لنظير معين بعد بضع دقائق. يمكن تعيين معاملات Control Block Sharing التالية لكل router:

1. **SYN sent** — initiator includes optional data.  
2. **SYN/ACK response** — responder includes optional data.  
3. **ACK finalization** — establishes reliability and session state.  
4. **FIN/RESET** — used for orderly closure or abrupt termination.

### المعاملات الأخرى {#other}

المعاملات التالية هي القيم الافتراضية الموصى بها. قد تختلف القيم الافتراضية حسب التنفيذ:

- The streaming layer continuously adapts to network latency and throughput via RTT-based feedback.  
- Applications perform best when routers are contributing peers (participating tunnels enabled).  
- TCP-like congestion control mechanisms prevent overloading slow peers and help balance bandwidth use across tunnels.

### التاريخ {#history}

نمت مكتبة streaming بشكل طبيعي لـ I2P - أولاً قام mihi بتطوير "mini streaming library" كجزء من I2PTunnel، والتي كانت محدودة بحجم نافذة من رسالة واحدة (تتطلب ACK قبل إرسال التالية)، ثم تم إعادة هيكلتها إلى واجهة streaming عامة (تحاكي TCP sockets) وتم نشر تطبيق streaming الكامل مع بروتوكول نافذة متحركة وتحسينات لأخذ ناتج النطاق الترددي العالي × التأخير بعين الاعتبار. قد تقوم التدفقات الفردية بتعديل الحد الأقصى لحجم الحزمة والخيارات الأخرى. حجم الرسالة الافتراضي محدد ليناسب بدقة رسالتين من I2NP tunnel بحجم 1K، وهو مقايضة معقولة بين تكاليف النطاق الترددي لإعادة إرسال الرسائل المفقودة، وزمن الاستجابة والحمولة الإضافية للرسائل المتعددة.

## Interoperability and Best Practices

سلوك مكتبة streaming له تأثير عميق على الأداء على مستوى التطبيق، وبالتالي، فهو مجال مهم لمزيد من التحليل.

- Always test against both **Java I2P** and **i2pd** to ensure full compatibility.  
- Although the protocol is standardized, minor implementation differences may exist.  
- Handle older routers gracefully—many peers still run pre-2.0 versions.  
- Monitor connection stats using `I2PSocket.getOptions()` and `getSession()` to read RTT and retransmission metrics.
