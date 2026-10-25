---
title: "Streaming Protocol"
description: "TCP-like transport used by most I2P applications"
slug: "streaming"
aliases:
  - "/zh/streaming"
  - "/zh/streaming/"
lastUpdated: "2026-01"
accurateFor: "0.9.68"
---

## 概述 {#overview}

streaming库在技术上属于"应用"层的一部分，因为它不是核心router功能。但在实际应用中，它为几乎所有现有的I2P应用程序提供了重要功能，通过在I2P上提供类似TCP的流，并允许现有应用程序轻松移植到I2P。用于客户端通信的另一个端到端传输库是[datagram库](/docs/specs/datagrams)。

流传输库是基于核心 [I2CP API](/docs/specs/i2cp) 之上的一层，它允许在不可靠、无序且未认证的消息层上实现可靠、有序且经过认证的消息流。就像 TCP 与 IP 的关系一样，这种流传输功能有一系列可用的权衡和优化选项，但与其将该功能嵌入到基础 I2P 代码中，不如将其分离到独立的库中，这样既可以保持类 TCP 复杂性的分离，也允许实现替代的优化实现。

考虑到消息的相对高成本，streaming library 的消息调度和传递协议已经过优化，允许传递的单个消息包含尽可能多的可用信息。例如，通过 streaming library 代理的小型 HTTP 事务可以在单次往返中完成 - 第一个消息捆绑了 SYN、FIN 和小型 HTTP 请求负载，而回复则捆绑了 SYN、FIN、ACK 和 HTTP 响应负载。虽然必须传输额外的 ACK 来告知 HTTP 服务器已收到 SYN/FIN/ACK，但本地 HTTP 代理通常可以立即向浏览器传递完整响应。

流媒体库与TCP的抽象非常相似，具有滑动窗口、拥塞控制算法（包括慢启动和拥塞避免）以及常规数据包行为（ACK、SYN、FIN、RST、rto计算等）。

流媒体库是一个针对 I2P 网络操作优化的强大库。它具有单阶段设置，并包含完整的窗口化实现。

## API {#api}

流媒体库API为Java应用程序提供了标准的套接字范式。底层的[I2CP](/docs/specs/i2cp) API完全被隐藏，除了应用程序可以通过流媒体库传递[I2CP参数](/docs/specs/i2cp#options)给I2CP解释。

streaming lib 的标准接口是应用程序使用 I2PSocketManagerFactory 来创建 I2PSocketManager。然后应用程序向 socket 管理器请求一个 I2PSession，这将通过 [I2CP](/docs/specs/i2cp) 建立与 router 的连接。然后应用程序可以通过 I2PSocket 建立连接或通过 I2PServerSocket 接收连接。

关于良好的使用示例，请参见 i2psnark 代码。

### 选项和默认值 {#options}

下面列出了选项和当前的默认值。选项区分大小写，可以为整个 router、特定客户端或基于每个连接的单独套接字设置。许多值都针对典型 I2P 条件下的 HTTP 性能进行了调优。强烈建议其他应用程序（如点对点服务）根据需要进行修改，通过设置选项并通过调用 I2PSocketManagerFactory.createManager(_i2cpHost, _i2cpPort, opts) 传递这些选项。时间值以毫秒为单位。

请注意，更高层的API，如 [SAM](/docs/api/samv3)、[BOB](/docs/legacy/bob) 和 [I2PTunnel](/docs/api/i2ptunnel)，可能会用它们自己的默认值覆盖这些默认设置。另外请注意，许多选项仅适用于监听传入连接的服务器。

从 0.9.1 版本开始，大部分（但不是全部）选项都可以在活跃的套接字管理器或会话上进行更改。详情请参见 javadocs。

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
## 协议规范 {#spec}

[查看流库规范页面。](/docs/specs/streaming)

## 实现细节 {#implementation}

### 设置 {#setup}

发起方发送一个设置了 SYNCHRONIZE 标志的数据包。此数据包也可能包含初始数据。对等方回复一个设置了 SYNCHRONIZE 标志的数据包。此数据包也可能包含初始响应数据。

发起方可以在收到SYNCHRONIZE响应之前发送额外的数据包，最多可达初始窗口大小。这些数据包的发送Stream ID字段也将设置为0。接收方必须短时间缓冲在未知流上收到的数据包，因为它们可能会乱序到达，在SYNCHRONIZE数据包之前到达。

### MTU 选择和协商 {#mtu}

最大消息大小（也称为 MTU / MRU）会协商为两个对等节点支持的较小值。由于 tunnel 消息会填充到 1KB，糟糕的 MTU 选择会导致大量开销。MTU 通过选项 i2p.streaming.maxMessageSize 指定。当前默认的 1730 MTU 值被选择为恰好适合两个 1K I2NP tunnel 消息，包括典型情况下的开销。

注意：这是仅有效载荷的最大大小，不包括头部。

注意：对于ECIES连接，由于开销较小，推荐的MTU为1812。无论使用什么密钥类型，所有连接的默认MTU仍为1730。客户端必须使用发送和接收MTU中的最小值，这是通常的做法。参见提案155。

连接中的第一条消息包含由流式传输层添加的 387 字节（典型值）Destination，通常还有 898 字节（典型值）LeaseSet 和 Session 密钥，这些都由 router 打包在 Garlic 消息中。（如果之前已经建立了 ElGamal Session，则不会打包 LeaseSet 和 Session 密钥）。因此，将完整的 HTTP 请求装入单个 1KB I2NP 消息的目标并不总是能够实现。然而，MTU 的选择，以及在 tunnel gateway 处理器中仔细实现分片和批处理策略，是影响网络带宽、延迟、可靠性和效率的重要因素，特别是对于长连接而言。

### 数据完整性 {#integrity}

数据完整性通过在[I2CP层](/docs/specs/i2cp#format)中实现的gzip CRC-32校验和来保证。流协议中没有校验和字段。

### 数据包封装 {#encapsulation}

每个数据包都作为单独的消息（或作为[Garlic Message](/docs/overview/garlic-routing)中的单独丁香）通过I2P发送。消息封装在底层的[I2CP](/docs/specs/i2cp)、[I2NP](/docs/specs/i2np)和[tunnel message](/docs/specs/tunnel-message)层中实现。流协议中没有数据包分隔符机制或载荷长度字段。

### 可选延迟 {#delay}

数据包可能包含一个可选的延迟字段，指定接收方在确认数据包之前应等待的请求延迟时间（以毫秒为单位）。有效值为0到60000（包含）。值为0表示请求立即确认。这仅为建议性质，接收方应稍作延迟，以便可以用单个确认来确认多个数据包。某些实现可能在此字段中包含一个建议值（测量的RTT / 2）。对于非零的可选延迟值，接收方应将发送确认前的最大延迟限制在最多几秒钟。大于60000的可选延迟值表示阻塞，见下文。

### 传输/接收窗口和阻塞 {#windows}

TCP 报头包含以字节为单位的接收窗口；然而，流协议并不提供以字节或数据包为单位交换最大接收窗口大小的方式。只有一个简单的阻塞/非阻塞指示来表明接收缓冲区已满。每个端点必须维护自己对远端接收窗口的估计，无论是以字节还是数据包为单位。请注意，如果客户端应用程序清空缓冲区的速度较慢，接收缓冲区可能在任何窗口大小下都会溢出。

Java 实现中的默认最大发送和接收窗口大小为 128 个数据包。将最大发送窗口大小设置为高于 128 的实现必须考虑以下问题：

- 由于接收缓冲区溢出，来自 Java router 的 CHOKE 响应更有可能发生。
- 必须实现远端接收器缓冲区大小估算以减少重复溢出（见上文）
- 必须正确处理 CHOKE（见下文）
- 超过 256 的最大窗口大小更容易出错，因为 nack 计数选项字段长度为一个字节，将最大 NACK 数量限制为 255。本规范不涉及如何处理超过 255 个 NACK 的情况。不推荐使用超过 256 的最大窗口大小。

接收器实现的推荐最小缓冲区大小为128个数据包或232 KB（大约128 * 1812）。由于I2P网络延迟、数据包丢失以及由此产生的拥塞控制，这种大小的缓冲区很少被填满。然而，在高带宽的"本地回环"（同一router）连接或本地测试中，溢出更有可能发生。

为了快速指示并平稳地从溢出条件中恢复，流协议中有一个简单的推回机制。如果收到一个可选延迟字段值为60001或更高的数据包，这表示"阻塞"或接收窗口为零。可选延迟字段值为60000或更低的数据包表示"解除阻塞"。没有可选延迟字段的数据包不会影响阻塞/解除阻塞状态。

被阻塞后，在发送端解除阻塞之前，不应再发送包含数据的数据包，但偶尔发送"探测"数据包以补偿可能丢失的解除阻塞数据包除外。被阻塞的端点应启动"持续定时器"来控制探测，如同TCP中一样。解除阻塞的端点应发送多个设置了此字段的数据包，或继续定期发送这些数据包，直到再次收到数据包。等待解除阻塞的最大时间取决于具体实现。解除阻塞后的发送端窗口大小和拥塞控制策略取决于具体实现。

### 拥塞控制 {#congestion}

流媒体库使用标准的慢启动（指数窗口增长）和拥塞避免（线性窗口增长）阶段，并采用指数退避。窗口管理和确认使用数据包计数，而非字节计数。

### 关闭 {#close}

任何数据包，包括设置了 SYNCHRONIZE 标志的数据包，也可能同时发送 CLOSE 标志。连接不会关闭，直到对等方响应 CLOSE 标志。CLOSE 数据包也可能包含数据。

### Ping / Pong {#ping}

在 I2CP 层（相当于 ICMP echo）或数据报中没有 ping 功能。此功能在流式传输中提供。Ping 和 pong 不能与标准流式传输数据包结合使用；如果设置了 ECHO 选项，那么大多数其他标志、选项、ackThrough、sequenceNum、NACK 等都将被忽略。

ping 包必须设置 ECHO、SIGNATURE_INCLUDED 和 FROM_INCLUDED 标志。sendStreamId 必须大于零，receiveStreamId 会被忽略。sendStreamId 可能对应也可能不对应现有连接。

pong 数据包必须设置 ECHO 标志。sendStreamId 必须为零，receiveStreamId 是来自 ping 的 sendStreamId。在 0.9.18 版本之前，pong 数据包不包含 ping 中包含的任何载荷。

从 0.9.18 版本开始，ping 和 pong 可能包含有效载荷。ping 中的有效载荷最多 32 字节，会在 pong 中返回。

可以通过配置 i2p.streaming.answerPings=false 来配置流以禁用发送 pong 响应。

### 0-RTT 问题 {#0rtt}

如上所述，与TCP不同，streaming允许通过在SYN数据包中捆绑数据来实现0-RTT数据传输。这是首选的实现方式。此外，streaming允许在SYN之后、收到SYN-ACK之前发送额外的数据包（最多达到初始窗口大小）。这些数据包将具有非零序列号，不会设置SYN标志，并且sendStreamID为零。

接收方应该设计以处理握手过程中的乱序或丢包情况，包括数据包在SYN之前到达的情况。推荐的实现方式是对未知ID的非SYN包进行队列缓存而不是丢弃，并在收到SYN后从队列中取出这些包。

在反向方向上，情况类似。连接接收方（Bob）应该延迟发送 SYN-ACK（ACK DELAY），并等待短时间以接收来自应用程序的数据。在收到来自应用程序的数据后，将其（最多到最大数据包大小）放入 SYN-ACK 数据包中并发送。额外的数据包（最多到初始窗口大小）也可以发送，无需等待 SYN-ACK 的 ACK。

发起方应该缓存在收到 SYN-ACK 之前接收到的任何数据包，就像握手完成后处理乱序数据包一样。

### 测试流媒体库 {#testing}

对于测试新的或修改过的流媒体库的开发者，Java I2P 提供了一个简单的本地测试工具，用于对真实网络条件进行可重现的测试，包括延迟、丢包和延迟抖动。它是一个小型存根，仅实现了用于本地连接的 I2CP 服务器。

开发人员应该使用各种典型参数进行测试，包括从10毫秒到至少15秒的延迟，以及0到10%的数据包丢失率。添加抖动可以轻松测试乱序处理。

这也是通过手动暂停两个应用程序中的一个来测试缓冲区溢出（CHOKE/UNCHOKE）的良好设置。

从 i2p.i2p 源代码包：

- `ant buildTest`
- `java -cp build/routertest.jar net.i2p.router.client.LocalClientManager -?` (查看选项帮助)
- `java -cp build/routertest.jar net.i2p.router.client.LocalClientManager [options]` (运行)

### i2p.streaming.profile 注释 {#profile}

此选项支持两个值：1=bulk 和 2=interactive。该选项为流传输库和/或 router 提供关于预期流量模式的提示。

"Bulk" 意味着优化高带宽，可能以延迟为代价。这是默认设置。"Interactive" 意味着优化低延迟，可能以带宽或效率为代价。优化策略（如果有的话）取决于具体实现，可能包括流协议之外的更改。

在 API 版本 0.9.63 之前，Java I2P 对除了 1（bulk）以外的任何值都会返回错误，tunnel 将无法启动。从 API 0.9.64 开始，Java I2P 忽略该值。在 API 版本 0.9.63 之前，i2pd 忽略此选项；从 API 0.9.64 开始，i2pd 实现了此功能。

虽然流协议包含一个标志字段来将配置文件设置传递给另一端，但在任何已知的 router 中都没有实现此功能。

### 控制块共享 {#sharing}

streaming lib 支持"TCP"控制块共享。这会在连接到同一远程对等节点的连接之间共享三个重要的 streaming lib 参数（窗口大小、往返时间、往返时间方差）。这用于连接打开/关闭时的"时间性"共享，而不是连接期间的"集合"共享（参见 [RFC 2140](http://www.ietf.org/rfc/rfc2140.txt)）。每个 ConnectionManager（即每个本地 Destination）都有单独的共享，这样就不会向同一 router 上的其他 Destination 泄露信息。给定对等节点的共享数据会在几分钟后过期。以下控制块共享参数可以按 router 设置：

- RTT_DAMPENING = 0.75
- RTTDEV_DAMPENING = 0.75
- WINDOW_DAMPENING = 0.75

### 其他参数 {#other}

以下参数是推荐的默认值。默认值可能因实现而异：

- MIN_RESEND_DELAY = 100 ms (最小 RTO)
- MAX_RESEND_DELAY = 45 sec (最大 RTO)
- MIN_WINDOW_SIZE = 1
- MAX_WINDOW_SIZE = 128
- TREND_COUNT = 3
- MIN_MESSAGE_SIZE = 512 (最小 MTU)
- INBOUND_BUFFER_SIZE = maxMessageSize * (maxWindowSize + 2)
- INITIAL_TIMEOUT (仅在 RTT 采样之前有效) = 9 sec
- "alpha" (根据 RFC 6298 的 RTT 衰减因子) = 0.125
- "beta" (根据 RFC 6298 的 RTTDEV 衰减因子) = 0.25
- "K" (根据 RFC 6298 的 RTDEV 倍数) = 4
- PASSIVE_FLUSH_DELAY = 175 ms
- 最大 RTT 估计值: 60 sec

### 历史 {#history}

streaming库是为I2P有机发展而来的 - 首先mihi实现了"mini streaming library"作为I2PTunnel的一部分，它被限制为1个消息的窗口大小（需要在发送下一个消息之前收到ACK），然后它被重构为通用的streaming接口（镜像TCP套接字），并部署了完整的streaming实现，采用滑动窗口协议和优化来考虑高带宽x延迟乘积。单个流可以调整最大数据包大小和其他选项。默认消息大小被选择为恰好适合两个1K I2NP tunnel消息，这是在重传丢失消息的带宽成本与多个消息的延迟和开销之间的合理权衡。

## 未来工作 {#future}

流媒体库的行为对应用层性能有着深远的影响，因此是进一步分析的重要领域。

- 可能需要对流媒体库参数进行额外调优。
- 另一个研究领域是流媒体库与 NTCP 和 SSU 传输层的交互。详情请参见 [NTCP 讨论页面](/docs/historical/ntcp-discussion)。
- 路由算法与流媒体库的交互强烈影响性能。特别是，将消息随机分发到池中的多个 tunnel 会导致高度的无序传送，从而导致窗口大小比正常情况下更小。router 目前通过一组一致的 tunnel 路由单个来源/目标对的消息，直到 tunnel 过期或传送失败。应该审查 router 的故障和 tunnel 选择算法以寻求可能的改进。
- 第一个 SYN 数据包中的数据可能超过接收方的 MTU。
- DELAY_REQUESTED 字段可以得到更多使用。
- 短期流上的重复初始 SYNCHRONIZE 数据包可能无法被识别和移除。
- 不要在重传中发送 MTU。
- 除非出站窗口已满，否则数据会被发送。（即无 Nagle 或 TCP_NODELAY）这应该有一个配置选项。
- zzz 已在流媒体库中添加调试代码，以 wireshark 兼容（pcap）格式记录数据包；使用此功能进一步分析性能。该格式可能需要增强以将更多流媒体库参数映射到 TCP 字段。
- 有提议用标准 TCP（或者可能是空层加原始套接字）替换流媒体库。这可能与流媒体库不兼容，但比较两者的性能会很有价值。
