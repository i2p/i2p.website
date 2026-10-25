---
title: "I2CP 概述"
description: "I2P客户端协议（I2CP）概述——会话管理、选项、有效载荷格式和多路复用。"
slug: "i2cp-overview"
aliases:
  - "/zh/docs/protocol/i2cp"
  - "/zh/docs/protocol/i2cp/"
category: "协议"
lastUpdated: "2025-04"
accurateFor: "0.9.66"
---

## 概述

I2P客户端协议（I2CP）在路由器与任何希望在网络上传输通信的客户端之间实现了明确的职责分离。它通过单个TCP套接字发送和接收消息，实现安全且异步的消息传递。使用I2CP时，客户端应用程序会告知路由器其身份（即其“目标”）、所需的匿名性、可靠性与延迟之间的权衡，以及消息的发送位置。相应地，路由器通过I2CP通知客户端是否有消息到达，并请求授权以使用某些隧道。

该协议本身使用 Java 实现，以提供客户端 SDK。此 SDK 通过 i2p.jar 包提供，实现了 I2CP 的客户端部分。客户端永远不应需要访问包含路由器本身及 I2CP 路由器端的 router.jar 包。非 Java 客户端还需要实现[流式传输库](/docs/api/streaming/)以支持类 TCP 的连接。

应用程序可以通过使用[简单匿名消息（SAM）](/docs/api/samv3/)协议来利用基础的 I2CP 以及[流式传输](/docs/api/streaming/)和[数据报](/docs/specs/datagrams/)库，该协议不要求客户端处理任何类型的加密。此外，客户端也可以通过多种代理访问网络——HTTP、CONNECT 以及 SOCKS 4/4a/5。或者，Java 客户端可以直接使用 ministreaming.jar 和 streaming.jar 中的这些库。因此，无论是 Java 还是非 Java 应用程序都有多种选择。

在 I2P 0.6 版本发布时，客户端到路由器的端到端加密（即在 I2CP 连接上加密数据）已被禁用，仅保留由路由器实现的 ElGamal/AES 端到端加密。目前客户端库仍需实现的唯一加密功能是用于 [LeaseSets](/docs/specs/i2cp/#msg_CreateLeaseSet) 和 [Session Configurations](/docs/specs/i2cp/#struct_SessionConfig) 的 DSA 公私钥签名，以及这些密钥的管理。

在标准的 I2P 安装中，外部 Java 客户端通过 I2CP 使用端口 7654 与本地路由器通信。默认情况下，路由器绑定到地址 127.0.0.1。要绑定到 0.0.0.0，请设置路由器高级配置选项 `i2cp.tcp.bindAllInterfaces=true` 并重启路由器。与路由器位于同一 JVM 中的客户端通过内部 JVM 接口直接将消息传递给路由器。

某些路由器和客户端实现还可能支持通过 SSL 的外部连接，可通过配置 `i2cp.SSL=true` 选项启用。尽管 SSL 并非默认设置，但强烈建议对任何可能暴露在公共互联网上的流量启用 SSL。除非启用了 SSL，否则授权用户名/密码（如有）、[目标地址](/docs/specs/common-structures/#type_PrivateKey) 的 [私钥](/docs/specs/common-structures/#type_PrivateKey) 和 [签名私钥](/docs/specs/common-structures/#type_SigningPrivateKey) 都将以明文形式传输。某些路由器和客户端实现还可能支持通过域套接字（domain sockets）的外部连接。

## I2CP 协议规范

请参阅 [I2CP 规范页面](/docs/specs/i2cp/) 以获取完整的协议规范。

## I2CP 初始化 {#initialization}

当客户端连接到路由器时，首先发送一个协议版本字节（0x2A）。然后发送一个[获取日期消息](/docs/specs/i2cp/#msg_GetDate)，并等待路由器返回的[设置日期消息](/docs/specs/i2cp/#msg_SetDate)响应。接着，客户端发送一个包含会话配置的[创建会话消息](/docs/specs/i2cp/#msg_CreateSession)。之后，客户端等待路由器发来的[请求LeaseSet消息](/docs/specs/i2cp/#msg_RequestLeaseSet)，该消息表明入站隧道已建立，客户端随后以包含已签名LeaseSet的CreateLeaseSetMessage进行响应。此后，客户端即可与其他I2P目标发起或接收连接。

## I2CP 选项 {#options}

### 路由器端选项

以下选项传统上通过包含在 [CreateSession 消息](/docs/specs/i2cp/#msg_CreateSession) 或 [ReconfigureSession 消息](/docs/specs/i2cp/#msg_ReconfigureSession) 中的 [SessionConfig](/docs/specs/i2cp/#struct_SessionConfig) 传递给路由器。

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;" colspan="6">Router-side Options</th>
</tr>
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Option</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">As Of Release</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Recommended Arguments</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Allowable Range</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Default</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Description</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">clientMessageTimeout</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">8*1000 - 120*1000</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">60*1000</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The timeout (ms) for all sent messages. Unused. See the protocol specification for per-message settings.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">crypto.lowTagThreshold</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1-128</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">30</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Minimum number of ElGamal/AES Session Tags before we send more. Recommended: approximately tagsToSend * 2/3</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">crypto.ratchet.inboundTags</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.47</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1-?</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">160</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Inbound tag window for ECIES-X25519-AEAD-Ratchet. Local inbound tagset size. See proposal 144.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">crypto.ratchet.outboundTags</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.47</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1-?</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">160</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Outbound tag window for ECIES-X25519-AEAD-Ratchet. Advisory to send to the far-end in the options block. See proposal 144.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">crypto.tagsToSend</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1-128</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">40</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Number of ElGamal/AES Session Tags to send at a time. For clients with relatively low bandwidth per-client-pair (IRC, some UDP apps), this may be set lower.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">explicitPeers</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">null</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Comma-separated list of Base 64 Hashes of peers to build tunnels through; for debugging only</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.dontPublishLeaseSet</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true, false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Should generally be set to true for clients and false for servers</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.fastReceive</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true, false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">If true, the router just sends the MessagePayload instead of sending a MessageStatus and awaiting a ReceiveMessageBegin.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetAuthType</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0-2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The type of authentication for encrypted LS2. 0 for no per-client authentication (the default); 1 for DH per-client authentication; 2 for PSK per-client authentication. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetEncType</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4,0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0-65535,...</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The encryption type to be used, as of 0.9.38. Interpreted client-side, but also passed to the router in the SessionConfig, to declare intent and check support. As of 0.9.39, may be comma-separated values for multiple types. See PublicKey in common structures spec for values. See proposals 123, 144, and 145.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetOfflineExpiration</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The expiration of the offline signature, 4 bytes, seconds since the epoch. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetOfflineSignature</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The base 64 of the offline signature. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetPrivKey</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">A base 64 X25519 private key for the router to use to decrypt the encrypted LS2 locally, only if per-client authentication is enabled. Optionally preceded by the key type and ':'. Only "ECIES_X25519:" is supported, which is the default. See proposal 123. Do not confuse with i2cp.leaseSetPrivateKey which is for the leaseset encryption keys.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetSecret</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.39</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">""</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Base 64 encoded UTF-8 secret used to blind the leaseset address. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetTransientPublicKey</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">[type:]b64 The base 64 of the transient private key, prefixed by an optional sig type number or name, default DSA_SHA1. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetType</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1,3,5,7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1-255</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The type of leaseset to be sent in the CreateLeaseSet2 Message. Interpreted client-side, but also passed to the router in the SessionConfig, to declare intent and check support. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.messageReliability</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">BestEffort, None</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">BestEffort</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Guaranteed is disabled; None implemented in 0.8.1; the streaming lib default is None as of 0.8.1, the client side default is None as of 0.9.4</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.password</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">string</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;" rowspan="2">For authorization, if required by the router. If the client is running in the same JVM as a router, this option is not required. Warning - username and password are sent in the clear to the router, unless using SSL (i2cp.SSL=true). Authorization is only recommended when using SSL.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.username</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">string</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">inbound.allowZeroHop</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true, false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">If incoming zero hop tunnel is allowed</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">outbound.allowZeroHop</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true, false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">If outgoing zero hop tunnel is allowed</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">inbound.backupQuantity</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">number from 0 to 3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">No limit</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Number of redundant fail-over for tunnels in</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">outbound.backupQuantity</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">number from 0 to 3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">No limit</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Number of redundant fail-over for tunnels out</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">inbound.IPRestriction</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">number from 0 to 4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 to 4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Number of IP bytes to match to determine if two routers should not be in the same tunnel. 0 to disable.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">outbound.IPRestriction</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">number from 0 to 4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 to 4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Number of IP bytes to match to determine if two routers should not be in the same tunnel. 0 to disable.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">inbound.length</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">number from 0 to 3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 to 7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Length of tunnels in</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">outbound.length</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">number from 0 to 3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 to 7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Length of tunnels out</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">inbound.lengthVariance</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">number from -1 to 2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">-7 to 7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Random amount to add or subtract to the length of tunnels in. A positive number x means add a random amount from 0 to x inclusive. A negative number -x means add a random amount from -x to x inclusive. The router will limit the total length of the tunnel to 0 to 7 inclusive. The default variance was 1 prior to release 0.7.6.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">outbound.lengthVariance</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">number from -1 to 2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">-7 to 7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Random amount to add or subtract to the length of tunnels out. A positive number x means add a random amount from 0 to x inclusive. A negative number -x means add a random amount from -x to x inclusive. The router will limit the total length of the tunnel to 0 to 7 inclusive. The default variance was 1 prior to release 0.7.6.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">inbound.nickname</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">string</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Name of tunnel - generally used in routerconsole, which will use the first few characters of the Base64 hash of the destination by default.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">outbound.nickname</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">string</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Name of tunnel - generally ignored unless inbound.nickname is unset.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">outbound.priority</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">number from -25 to 25</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">-25 to 25</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Priority adjustment for outbound messages. Higher is higher priority.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">inbound.quantity</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">number from 1 to 3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 to 16</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Number of tunnels in. Limit was increased from 6 to 16 in release 0.9; however, numbers higher than 6 are incompatible with older releases.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">outbound.quantity</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">number from 1 to 3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">No limit</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Number of tunnels out</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">inbound.randomKey</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.17</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Base 64 encoding of 32 random bytes</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;" rowspan="2">Used for consistent peer ordering across restarts.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">outbound.randomKey</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.17</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Base 64 encoding of 32 random bytes</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">inbound.*</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Any other options prefixed with "inbound." are stored in the "unknown options" properties of the inbound tunnel pool's settings.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">outbound.*</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Any other options prefixed with "outbound." are stored in the "unknown options" properties of the outbound tunnel pool's settings.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">shouldBundleReplyInfo</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true, false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Set to false to disable ever bundling a reply LeaseSet. For clients that do not publish their LeaseSet, this option must be true for any reply to be possible. "true" is also recommended for multihomed servers with long connection times.

Setting to "false" may save significant outbound bandwidth, especially if the client is configured with a large number of inbound tunnels (Leases). If replies are still required, this may shift the bandwidth burden to the far-end client and the floodfill. There are several cases where "false" may be appropriate:

- Unidirectional communication, no reply required
- LeaseSet is published and higher reply latency is acceptable
- LeaseSet is published, client is a "server", all connections are inbound so the connecting far-end destination obviously has the leaseset already. Connections are either short, or it is acceptable for latency on a long-lived connection to temporarily increase while the other end re-fetches the LeaseSet after expiration. HTTP servers may fit these requirements.</td>
</tr>
</table>
注意：较大的数量、长度或方差设置可能会导致显著的性能或可靠性问题。

注意：自 0.7.7 版本起，选项名称和值必须使用 UTF-8 编码。这主要对昵称等字段有用。在此版本之前，包含多字节字符的选项会被损坏。由于选项以 [映射（Mapping）](/docs/specs/common-structures/#type_Mapping) 形式编码，所有选项名称和值的最大长度限制为 255 字节（而非字符）。

### 客户端选项

以下选项将在客户端侧进行解释，如果通过 I2PClient.createSession() 调用传递给 I2PSession，则会被解析。流式传输库还应将这些选项传递给 I2CP。其他实现可能具有不同的默认值。

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;" colspan="6">Client-side Options</th>
</tr>
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Option</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">As Of Release</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Recommended Arguments</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Allowable Range</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Default</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Description</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.closeIdleTime</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1800000</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">300000 minimum</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">(ms) Idle time required (default 30 minutes)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.closeOnIdle</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true, false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Close I2P session when idle</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.encryptLeaseSet</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true, false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Encrypt the lease</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.fastReceive</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true, false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">If true, the router just sends the MessagePayload instead of sending a MessageStatus and awaiting a ReceiveMessageBegin.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.gzip</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.6.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true, false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Gzip outbound data</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetAuthType</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0-2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The type of authentication for encrypted LS2. 0 for no per-client authentication (the default); 1 for DH per-client authentication; 2 for PSK per-client authentication. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetBlindedType</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.39</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0-65535</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">See prop. 123</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The sig type of the blinded key for encrypted LS2. Default depends on the destination sig type. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetClient.dh.nnn</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">b64name:b64pubkey</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The base 64 of the client name (ignored, UI use only), followed by a ':', followed by the base 64 of the public key to use for DH per-client auth. nnn starts with 0. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetClient.psk.nnn</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">b64name:b64privkey</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The base 64 of the client name (ignored, UI use only), followed by a ':', followed by the base 64 of the private key to use for PSK per-client auth. nnn starts with 0. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetEncType</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0-65535,...</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The encryption type to be used, as of 0.9.38. Interpreted client-side, but also passed to the router in the SessionConfig, to declare intent and check support. As of 0.9.39, may be comma-separated values for multiple types. See also i2cp.leaseSetPrivateKey. See PublicKey in common structures spec for values. See proposals 123, 144, and 145.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetKey</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">For encrypted leasesets. Base 64 SessionKey (44 characters)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetOption.nnn</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">srvKey=srvValue</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">A service record to be placed in the LeaseSet2 options. Example: "_smtp._tcp=1 86400 0 0 25 ...b32.i2p". nnn starts with 0. See proposal 167.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetPrivateKey</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.18</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Base 64 private keys for encryption. Optionally preceded by the encryption type name or number and ':'. For LS1, only one key is supported, and only "0:" or "ELGAMAL_2048:" is supported, which is the default. As of 0.9.39, for LS2, multiple keys may be comma-separated, and each key must be a different encryption type. I2CP will generate the public key from the private key. Use for persistent leaseset keys across restarts. See proposals 123, 144, and 145. See also i2cp.leaseSetEncType. Do not confuse with i2cp.leaseSetPrivKey which is for encrypted LS2.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetSecret</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.39</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">""</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Base 64 encoded UTF-8 secret used to blind the leaseset address. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetSigningPrivateKey</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.18</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Base 64 private key for signatures. Optionally preceded by the key type and ':'. DSA_SHA1 is the default. Key type must match the signature type in the destination. I2CP will generate the public key from the private key. Use for persistent leaseset keys across restarts.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetType</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1,3,5,7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1-255</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The type of leaseset to be sent in the CreateLeaseSet2 Message. Interpreted client-side, but also passed to the router in the SessionConfig, to declare intent and check support. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.messageReliability</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">BestEffort, None</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">None</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Guaranteed is disabled; None implemented in 0.8.1; None is the default as of 0.9.4</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.reduceIdleTime</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1200000</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">300000 minimum</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">(ms) Idle time required (default 20 minutes, minimum 5 minutes)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.reduceOnIdle</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true, false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Reduce tunnel quantity when idle</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.reduceQuantity</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 to 5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Tunnel quantity when reduced (applies to both inbound and outbound)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.SSL</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true, false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Connect to the router using SSL. If the client is running in the same JVM as a router, this option is ignored, and the client connects to that router internally.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.tcp.host</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">127.0.0.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Router hostname. If the client is running in the same JVM as a router, this option is ignored, and the client connects to that router internally.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.tcp.port</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1-65535</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7654</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Router I2CP port. If the client is running in the same JVM as a router, this option is ignored, and the client connects to that router internally.</td>
</tr>
</table>
注意：所有参数（包括数字）均为字符串。布尔值 true/false 为不区分大小写的字符串，任何不区分大小写不等于 "true" 的值都将被解释为 false。所有选项名称均区分大小写。

## I2CP 载荷数据格式与多路复用 {#format}

I2CP 处理的端到端消息（即客户端在 [SendMessageMessage](/docs/specs/i2cp/#msg_SendMessage) 中发送的数据，以及在 [MessagePayloadMessage](/docs/specs/i2cp/#msg_MessagePayload) 中接收的数据）使用标准的 10 字节 gzip 头进行压缩，该头以 0x1F 0x8B 0x08 开始，符合 [RFC 1952](http://www.ietf.org/rfc/rfc1952.txt) 的规定。从 0.7.1 版本开始，I2P 利用了 gzip 头中原本被忽略的部分来包含协议、源端口（from-port）和目标端口（to-port）信息，从而支持在同一目标地址上实现流式传输和数据报传输，并允许多通道环境下使用数据报进行查询/响应操作的可靠运行。

gzip 功能无法完全关闭，但设置 `i2cp.gzip=false` 会将 gzip 压缩力度设为 0，可能节省少量 CPU 资源。实现方可以根据内容可压缩性的评估，按每个套接字或每条消息为单位选择不同的 gzip 压缩力度。由于 API 0.9.57（提案 161）中实现了对目标填充数据的可压缩性优化，即使有效载荷本身不可压缩，也建议对双向流式 SYN 数据包以及可回复的数据报进行压缩。对于压缩力度为 0 的情况，实现方可以编写一个简单的 gzip/gunzip 函数，相比通用 gzip 库能显著提升效率。

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Bytes</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Content</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0-2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Gzip header 0x1F 0x8B 0x08</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Gzip flags</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4-5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">I2P Source port (Gzip mtime)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">6-7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">I2P Destination port (Gzip mtime)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Gzip xflags (set to 2 to be indistinguishable from the Java implementation)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">9</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">I2P Protocol (6 = Streaming, 17 = Datagram, 18 = Raw Datagrams) (Gzip OS)</td>
</tr>
</table>
注意：I2P 协议号 224-254 保留用于实验性协议。I2P 协议号 255 保留用于未来扩展。

数据完整性通过 [RFC 1952](http://www.ietf.org/rfc/rfc1952.txt) 规定的标准 gzip CRC-32 进行验证。

## 与标准IP的重要区别 {#ip-differences}

I2CP 端口用于 I2P 套接字和数据报。它们与本地套接字或端口无关。由于在 0.7.1 版本之前 I2P 不支持端口和协议号，为了向后兼容，I2P 中的端口和协议号与标准 IP 中的有所区别：

- 端口 0 是有效的，具有特殊含义。
- 端口 1-1023 并无特殊或特权含义。
- 服务器默认在端口 0 上监听，表示“所有端口”。
- 客户端默认发送到端口 0，表示“任意端口”。
- 客户端默认从端口 0 发送，表示“未指定”。
- 服务器可以在端口 0 上运行一个服务，同时在更高端口上运行其他服务。如果是这样，端口 0 的服务是默认服务；如果传入的套接字或数据报端口不匹配其他服务，则将连接到该默认服务。
- 大多数 I2P 目的地仅运行一个服务，因此你可以使用默认设置，忽略 I2CP 端口配置。
- 协议号 0 是有效的，表示“任意协议”。但不推荐使用，且可能无法正常工作。流式传输要求协议号设置为 6。
- 流式套接字通过内部连接 ID 进行跟踪。因此，不需要 dest:port:dest:port:protocol 这个五元组保持唯一。例如，两个目的地之间可以存在多个具有相同端口的套接字。客户端在发起出站连接时，无需选择“空闲端口”。

## 未来工作 {#future}

- 当前的授权机制可以修改为使用哈希密码。
- 创建租赁集（Create Lease Set）消息中包含了签名私钥，但这是不必要的。密钥撤销功能尚未实现。该字段应替换为随机数据或直接移除。
- 某些改进可能会使用之前已定义但未实现的消息。
