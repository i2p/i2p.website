---
title: "Streaming Protocol"
description: "TCP-like transport used by most I2P applications"
slug: "streaming"
aliases:
  - "/hi/streaming"
  - "/hi/streaming/"
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

Java implementation में default maximum transmit और receive window size 128 packets है। 128 से अधिक maximum transmit window size सेट करने वाले implementations को निम्नलिखित मुद्दों पर विचार करना चाहिए:

- One-phase connection setup using **SYN**, **ACK**, and **FIN** flags that can be bundled with payload data to reduce round-trips.
- **Sliding-window congestion control**, with slow start and congestion avoidance tuned for I2P’s high-latency environment.
- Packet compression (default 4KB compressed segments) balancing retransmission cost and fragmentation latency.
- Fully **authenticated, encrypted**, and **reliable** channel abstraction between I2P destinations.

receiver implementations के लिए अनुशंसित न्यूनतम buffer size 128 packets या 232 KB (लगभग 128 * 1812) है। I2P network latency, packet drops, और परिणामी congestion control के कारण, इस आकार का buffer शायद ही कभी भरता है। हालांकि, overflow होने की संभावना high-bandwidth "local loopback" (same-router) connections या local testing में बहुत अधिक होती है।

overflow स्थितियों को तुरंत संकेतित करने और सुचारू रूप से रिकवर करने के लिए, streaming protocol में pushback के लिए एक सरल तंत्र है। यदि कोई packet 60001 या उससे अधिक value के optional delay field के साथ प्राप्त होता है, तो यह "choking" या शून्य receive window को दर्शाता है। 60000 या उससे कम value के optional delay field वाला packet "unchoking" को दर्शाता है। बिना optional delay field वाले packets choke/unchoke state को प्रभावित नहीं करते।

choked होने के बाद, transmitter के unchoked होने तक डेटा के साथ कोई और packets नहीं भेजे जाने चाहिए, सिवाय कभी-कभार "probe" डेटा packets के जो संभावित खोए गए unchoke packets की भरपाई के लिए भेजे जाते हैं। choked endpoint को probing को नियंत्रित करने के लिए TCP की तरह एक "persist timer" शुरू करना चाहिए। unchoking endpoint को इस field के सेट के साथ कई packets भेजने चाहिए, या जब तक डेटा packets दोबारा प्राप्त नहीं होते तब तक उन्हें नियमित रूप से भेजते रहना चाहिए। unchoking के लिए अधिकतम प्रतीक्षा समय implementation-dependent है। unchoked होने के बाद transmitter window size और congestion control strategy implementation-dependent है।

### Congestion Control

स्ट्रीमिंग lib मानक slow-start (exponential window growth) और congestion avoidance (linear window growth) phases का उपयोग करती है, exponential backoff के साथ। Windowing और acknowledgments packet count का उपयोग करते हैं, byte count का नहीं।

### Latency Considerations

कोई भी packet, जिसमें SYNCHRONIZE flag सेट वाला भी शामिल है, उसमें CLOSE flag भी भेजा जा सकता है। connection तब तक बंद नहीं होता जब तक peer CLOSE flag के साथ जवाब नहीं देता। CLOSE packets में data भी हो सकता है।

### Ping / Pong {#ping}

I2CP layer (ICMP echo के समकक्ष) या datagrams में कोई ping function नहीं है। यह function streaming में प्रदान की जाती है। Pings और pongs को standard streaming packet के साथ जोड़ा नहीं जा सकता; यदि ECHO option सेट है, तो अधिकांश अन्य flags, options, ackThrough, sequenceNum, NACKs, आदि को ignore किया जाता है।

एक ping packet में ECHO, SIGNATURE_INCLUDED, और FROM_INCLUDED flags सेट होने चाहिए। sendStreamId शून्य से अधिक होना चाहिए, और receiveStreamId को अनदेखा किया जाता है। sendStreamId किसी मौजूदा connection से मेल खाता हो या न हो।

एक pong packet में ECHO flag सेट होना चाहिए। sendStreamId शून्य होना चाहिए, और receiveStreamId ping से sendStreamId है। रिलीज़ 0.9.18 से पहले, pong packet में ping में शामिल कोई भी payload शामिल नहीं होता है।

रिलीज़ 0.9.18 के अनुसार, pings और pongs में एक payload हो सकता है। ping में payload, अधिकतम 32 bytes तक, pong में वापस किया जाता है।

Streaming को कॉन्फ़िगरेशन i2p.streaming.answerPings=false के साथ pongs भेजना अक्षम करने के लिए कॉन्फ़िगर किया जा सकता है।

### 0-RTT मुद्दे {#0rtt}

जैसा कि ऊपर बताया गया है, TCP के विपरीत, streaming SYN packet में data को bundle करके 0-RTT data delivery की अनुमति देता है। यह preferred implementation है। इसके अतिरिक्त, streaming अतिरिक्त data packets (initial window size तक) को SYN के बाद भेजने की अनुमति देता है, SYN-ACK प्राप्त होने से पहले। इन packets का sequence number nonzero होगा, SYN flag set नहीं होगा, और sendStreamID zero होगा।

रिसीवर्स को handshake के दौरान out-of-order या dropped packets के लिए डिज़ाइन करना चाहिए, जिसमें SYN से पहले data packets का आना भी शामिल है। पसंदीदा implementation यह है कि अज्ञात ID के लिए non-SYN packets को drop न करें बल्कि queue में रखें, और SYN प्राप्त होने के बाद उन्हें queue से retrieve करें।

विपरीत दिशा में, चीजें समान हैं। कनेक्शन प्राप्तकर्ता (Bob) को SYN-ACK (ACK DELAY) भेजने में देरी करनी चाहिए और एप्लिकेशन से डेटा के लिए थोड़ा समय इंतजार करना चाहिए। एप्लिकेशन से डेटा प्राप्त करने पर, इसे (अधिकतम पैकेट साइज़ तक) SYN-ACK पैकेट में डालें और भेजें। अतिरिक्त डेटा पैकेट, प्रारंभिक विंडो साइज़ तक, SYN-ACK के ACK की प्रतीक्षा किए बिना भी भेजे जा सकते हैं।

प्रवर्तक को SYN-ACK से पहले प्राप्त किसी भी डेटा पैकेट को बफर करना चाहिए, जैसा कि handshake पूर्ण होने के बाद out-of-order handling के समान होता है।

### स्ट्रीमिंग लाइब्रेरीज़ का परीक्षण {#testing}

नए या बदले गए streaming libraries का परीक्षण करने वाले developers के लिए, Java I2P एक सरल स्थानीय परीक्षण उपयोगिता प्रदान करता है जो वास्तविक नेटवर्क स्थितियों के प्रजनन योग्य परीक्षण के लिए है, जिसमें latency, packet loss, और delay jitter शामिल हैं। यह एक छोटा stub है जो केवल स्थानीय connections के लिए I2CP server को implement करता है।

डेवलपर्स को विस्तृत श्रृंखला के सामान्य पैरामीटर के साथ परीक्षण करना चाहिए, जिसमें 10ms से कम से कम 15s तक की latency और 0 से 10% तक की packet loss शामिल है। Jitter जोड़ना out-of-order handling का परीक्षण करना आसान बनाता है।

यह buffer overflow (CHOKE/UNCHOKE) को test करने के लिए भी एक अच्छा setup है, दो applications में से किसी एक को manually suspend करके।

i2p.i2p स्रोत पैकेज से:

- `I2PSocketManagerFactory` negotiates or reuses a router session via I2CP.  
- If no key is provided, a new destination is automatically generated.  
- Developers can pass I2CP options (e.g., tunnel lengths, encryption types, or connection settings) through the `options` map.  
- `I2PSocket` and `I2PServerSocket` mirror standard Java `Socket` interfaces, making migration straightforward.

### i2p.streaming.profile नोट्स {#profile}

यह विकल्प दो मान समर्थित करता है; 1=bulk और 2=interactive। यह विकल्प streaming library और/या router को अपेक्षित ट्रैफिक पैटर्न के बारे में संकेत प्रदान करता है।

"Bulk" का मतलब है उच्च bandwidth के लिए अनुकूलन करना, संभावित रूप से latency की कीमत पर। यह default है। "Interactive" का मतलब है कम latency के लिए अनुकूलन करना, संभावित रूप से bandwidth या दक्षता की कीमत पर। अनुकूलन रणनीतियां, यदि कोई हैं, तो implementation-dependent हैं, और इसमें streaming protocol के बाहर के बदलाव भी शामिल हो सकते हैं।

API संस्करण 0.9.63 तक, Java I2P 1 (bulk) के अलावा किसी भी मान के लिए एक त्रुटि वापस करता था और tunnel शुरू होने में विफल हो जाता था। API 0.9.64 से, Java I2P इस मान को नज़रअंदाज़ करता है। API संस्करण 0.9.63 तक, i2pd इस विकल्प को नज़रअंदाज़ करता था; यह API 0.9.64 से i2pd में लागू किया गया है।

जबकि streaming protocol में प्रोफाइल सेटिंग को दूसरे छोर तक पहुंचाने के लिए एक flag field शामिल है, यह किसी भी ज्ञात router में implement नहीं किया गया है।

### Control Block Sharing {#sharing}

streaming lib "TCP" Control Block sharing का समर्थन करती है। यह तीन महत्वपूर्ण streaming lib पैरामीटर (window size, round trip time, round trip time variance) को समान remote peer के connections में साझा करती है। इसका उपयोग connection open/close समय पर "temporal" sharing के लिए किया जाता है, connection के दौरान "ensemble" sharing के लिए नहीं ([RFC 2140](http://www.ietf.org/rfc/rfc2140.txt) देखें)। प्रत्येक ConnectionManager (यानी प्रत्येक local Destination) के लिए एक अलग share है ताकि समान router पर अन्य Destinations में कोई जानकारी लीक न हो। किसी दिए गए peer के लिए share data कुछ मिनटों बाद expire हो जाता है। निम्नलिखित Control Block Sharing parameters प्रत्येक router के लिए सेट किए जा सकते हैं:

1. **SYN sent** — initiator includes optional data.  
2. **SYN/ACK response** — responder includes optional data.  
3. **ACK finalization** — establishes reliability and session state.  
4. **FIN/RESET** — used for orderly closure or abrupt termination.

### अन्य पैरामीटर {#other}

निम्नलिखित पैरामीटर अनुशंसित डिफ़ॉल्ट हैं। डिफ़ॉल्ट अलग हो सकते हैं, कार्यान्वयन पर निर्भर:

- The streaming layer continuously adapts to network latency and throughput via RTT-based feedback.  
- Applications perform best when routers are contributing peers (participating tunnels enabled).  
- TCP-like congestion control mechanisms prevent overloading slow peers and help balance bandwidth use across tunnels.

### इतिहास {#history}

streaming library I2P के लिए प्राकृतिक रूप से विकसित हुई है - पहले mihi ने I2PTunnel के हिस्से के रूप में "mini streaming library" को लागू किया, जो 1 message के window size तक सीमित थी (अगला भेजने से पहले ACK की आवश्यकता), और फिर इसे एक सामान्य streaming interface (TCP sockets को दर्शाते हुए) में पुनर्गठित किया गया और पूर्ण streaming implementation को sliding window protocol और उच्च bandwidth x delay product को ध्यान में रखते हुए अनुकूलन के साथ तैनात किया गया। व्यक्तिगत streams अधिकतम packet size और अन्य विकल्पों को समायोजित कर सकती हैं। डिफ़ॉल्ट message size को दो 1K I2NP tunnel messages में सटीक रूप से फिट करने के लिए चुना गया है, और यह खोए हुए messages को फिर से भेजने की bandwidth लागत, और कई messages की latency और overhead के बीच एक उचित समझौता है।

## Interoperability and Best Practices

स्ट्रीमिंग लाइब्रेरी का व्यवहार एप्लिकेशन-स्तरीय प्रदर्शन पर गहरा प्रभाव डालता है, और इसीलिए यह आगे के विश्लेषण के लिए एक महत्वपूर्ण क्षेत्र है।

- Always test against both **Java I2P** and **i2pd** to ensure full compatibility.  
- Although the protocol is standardized, minor implementation differences may exist.  
- Handle older routers gracefully—many peers still run pre-2.0 versions.  
- Monitor connection stats using `I2PSocket.getOptions()` and `getSession()` to read RTT and retransmission metrics.
