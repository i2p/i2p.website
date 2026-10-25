---
title: "数据报"
description: "I2CP 之上的认证、可回复和原始消息格式"
slug: "datagrams"
aliases:
  - "/zh/datagrams"
  - "/zh/datagrams/"
lastUpdated: "2025-04"
accurateFor: "0.9.66"
---

## 数据报概述 {#overview}

数据报基于基础的 [I2CP](/docs/specs/i2cp) 构建，以标准格式提供经过身份验证且可回复的消息。这让应用程序能够可靠地从数据报中读取"发送方"地址，并确认该地址确实发送了该消息。这对某些应用程序是必要的，因为基础的 I2P 消息是完全原始的——它没有"发送方"地址（不像 IP 数据包）。此外，消息和发送方通过对载荷进行签名来进行身份验证。

数据报，如[流库数据包](/docs/api/streaming)，是应用层构造。这些协议独立于底层[传输](/docs/overview/transport)；协议由router转换为I2NP消息，任一协议都可以通过任一传输方式承载。

## 应用程序指南 {#application}

用Java编写的应用程序可以使用数据报API，而其他语言编写的应用程序可以使用[SAM](/docs/api/samv3)的数据报支持。在i2ptunnel中的[SOCKS代理](/docs/api/socks)、'streamr'隧道类型和udpTunnel类中也有有限的支持。

### 数据报长度 {#length}

应用程序设计者应该仔细考虑可回复与不可回复数据报之间的权衡。此外，由于tunnel会将数据报分片为1KB的tunnel消息，数据报大小会影响可靠性。消息片段越多，其中某个片段被中间跳点丢弃的可能性就越大。不建议使用大于几KB的消息。超过约10KB时，传送成功的概率会急剧下降。

[查看数据报规范页面。](/docs/specs/datagrams)

还要注意的是，较低层添加的各种开销，特别是 garlic messages，会对间歇性消息造成很大负担，比如基于 Kademlia-over-UDP 的应用所使用的消息。当前的实现是针对使用流媒体库的频繁流量进行调优的。

### I2CP 协议号和端口 {#protocol}

已签名（可回复）数据报的标准I2CP协议号是PROTO_DATAGRAM (17)。应用程序可以选择是否在I2CP头部设置协议。默认值取决于具体实现。必须设置此协议号以便对在同一目的地接收的数据报和流量进行解复用。

由于数据报不是面向连接的，应用程序可能需要端口号来将数据报与特定对等节点或通信会话关联，就像传统的UDP over IP一样。应用程序可以在I2CP (gzip)头部中添加"from"和"to"端口，如[I2CP页面](/docs/specs/i2cp#format)中所述。

在数据报API中没有方法来指定它是不可回复的（原始）还是可回复的。应用程序应该设计为期望适当的类型。应用程序应该使用I2CP协议号或端口来指示数据报类型。I2CP协议号PROTO_DATAGRAM（签名的，也称为Datagram1）、PROTO_DATAGRAM_RAW、PROTO_DATAGRAM2和PROTO_DATAGRAM3在I2PSession API中为此目的而定义。客户端/服务器数据报应用程序中的一个常见设计模式是，对包含随机数的请求使用签名数据报，对回复使用原始数据报，返回请求中的随机数。

**默认值：**

- PROTO_DATAGRAM = 17
- PROTO_DATAGRAM_RAW = 18
- PROTO_DATAGRAM2 = 19
- PROTO_DATAGRAM3 = 20

### 数据完整性 {#integrity}

数据完整性通过[I2CP 层](/docs/specs/i2cp#format)中实现的 gzip CRC-32 校验和来保证。经过认证的数据报（Datagram1 和 Datagram2）也确保完整性。数据报协议中没有校验和字段。

### 数据包封装 {#encapsulation}

每个数据报都通过I2P作为单个消息发送（或作为[Garlic Message](/docs/overview/garlic-routing)中的单独clove）。消息封装在底层的[I2CP](/docs/specs/i2cp)、[I2NP](/docs/specs/i2np)和[tunnel message](/docs/specs/tunnel-message)层中实现。数据报协议中没有数据包分隔符机制或长度字段。

## 规范 {#spec}

[查看数据报规范页面。](/docs/specs/datagrams)
