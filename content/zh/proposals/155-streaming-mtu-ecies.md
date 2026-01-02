---
title: "ECIES 目标的流式 MTU"
number: "155"
author: "zzz"
created: "2020-05-06"
lastupdated: "2020-05-30"
status: "已关闭"
thread: "http://zzz.i2p/topics/2886"
target: "0.9.47"
implementedin: "0.9.47"
toc: true
---

## 注意
网络部署和测试正在进行中。
可能会有小幅修改。


## 概览


### 摘要

ECIES 将现有会话（ES）消息的开销减少了约 90 个字节。
因此，我们可以将 ECIES 连接的 MTU 增加约 90 个字节。
参见 the [ECIES specification](/docs/specs/ecies/#overhead), [Streaming specification](/docs/specs/streaming/#flags-and-option-data-fields), and [Streaming API documentation](/docs/api/streaming/)。

如果不增加 MTU，在许多情况下，开销的节省并没有真正“节省”，因为消息将被填充到使用两个完整的隧道消息。

本提案不需要更改任何规范。
该提案仅作为建议发布，以便促进讨论和达成对推荐值及实现细节的共识。


### 目标

- 增加协商的 MTU
- 最大化 1 KB 隧道消息的使用
- 不更改流式协议


## 设计

使用现有的 MAX_PACKET_SIZE_INCLUDED 选项和 MTU 协商。
流式传输继续使用发送和接收的 MTU 中的最小值。
默认情况下，无论使用什么密钥，所有连接仍为 1730。

鼓励在所有 SYN 数据包中包含 MAX_PACKET_SIZE_INCLUDED 选项，双向传输，尽管这不是强制性的。

如果目标仅为 ECIES，使用更高的值（无论是 Alice 还是 Bob）。
如果目标是双密钥，行为可能有所不同：

如果双密钥客户端位于路由器之外（在外部应用程序中），它可能不知道在远程使用的密钥类型，并且 Alice 可能会在 SYN 中请求更高的值，而 SYN 中的最大数据量仍为 1730。

如果双密钥客户端位于路由器内，正在使用的密钥信息可能已知也可能未知。
租约集合可能尚未获取，或者内部 API 接口可能无法轻松地向客户端提供该信息。
如果信息可用，Alice 可以使用更高的值；否则，Alice 必须在协商之前使用标准值 1730。

作为 Bob 的双密钥客户端可以发回更高的值，即使没有从 Alice 接收到值或接收到的值为 1730；然而，在流式传输中没有上行协商的规定，因此 MTU 应保持在 1730。

正如 the [Streaming API documentation](/docs/api/streaming/) 中所指出的，从 Alice 到 Bob 发送的 SYN 数据包中的数据可能会超出 Bob 的 MTU。这是流式协议中的一个弱点。
因此，双密钥客户端必须在发送的 SYN 数据包中将数据限制为 1730 字节，同时发送更高的 MTU 选项。
一旦从 Bob 收到更高的 MTU，Alice 可以增加实际发送的最大有效负载。


### 分析

如 the [ECIES specification](/docs/specs/ecies/#overhead) 中所述，现有会话消息的 ElGamal 开销为 151 字节，而 Ratchet 开销为 69 字节。因此，我们可以将棘轮连接的 MTU 从 1730 增加 (151 - 69) = 82 字节至 1812。

## 规范

在 the [Streaming API documentation](/docs/api/streaming/) 的 MTU 选择和协商部分添加以下更改和澄清。
无需更改 the [Streaming specification](/docs/specs/streaming/)。

选项 i2p.streaming.maxMessageSize 的默认值对于所有连接保持 1730，无论使用何种密钥。
客户机必须使用发送和接收的 MTU 中的最小值。

有四个相关的 MTU 常量和变量：

- DEFAULT_MTU：1730，未更改，适用于所有连接
- i2cp.streaming.maxMessageSize：默认 1730 或 1812，可以通过配置更改
- ALICE_SYN_MAX_DATA：Alice 在 SYN 数据包中可以包含的最大数据
- negotiated_mtu：Alice 和 Bob 的 MTU 中的最小值，作为 Bob 到 Alice SYN ACK 中的最大数据尺寸，以及双向传输中所有后续数据包中使用的数据最大尺寸 

我们需要考虑五种情况：

### 1) 仅 Alice ElGamal
无变更，所有数据包使用 1730 MTU。

- ALICE_SYN_MAX_DATA = 1730
- i2cp.streaming.maxMessageSize 默认：1730
- Alice 可在 SYN 中发送 MAX_PACKET_SIZE_INCLUDED，不要求除非 != 1730

### 2) 仅 Alice ECIES
所有数据包使用 1812 MTU。

- ALICE_SYN_MAX_DATA = 1812
- i2cp.streaming.maxMessageSize 默认：1812
- Alice 必须在 SYN 中发送 MAX_PACKET_SIZE_INCLUDED

### 3) Alice 双密钥且知道 Bob 是 ElGamal
所有数据包使用 1730 MTU。

- ALICE_SYN_MAX_DATA = 1730
- i2cp.streaming.maxMessageSize 默认：1812
- Alice 可在 SYN 中发送 MAX_PACKET_SIZE_INCLUDED，不要求除非 != 1730

### 4) Alice 双密钥且知道 Bob 是 ECIES
所有数据包使用 1812 MTU。

- ALICE_SYN_MAX_DATA = 1812
- i2cp.streaming.maxMessageSize 默认：1812
- Alice 必须在 SYN 中发送 MAX_PACKET_SIZE_INCLUDED

### 5) Alice 双密钥且未知 Bob 密钥
在 SYN 数据包中发送 1812 作为 MAX_PACKET_SIZE_INCLUDED，但限制 SYN 数据包中的数据为 1730。

- ALICE_SYN_MAX_DATA = 1730
- i2cp.streaming.maxMessageSize 默认：1812
- Alice 必须在 SYN 中发送 MAX_PACKET_SIZE_INCLUDED

### 对于所有情况

Alice 和 Bob 计算 negotiated_mtu，Alice 和 Bob 的 MTU 中的最小值，作为 Bob 到 Alice SYN ACK 中的最大数据尺寸，以及双向传输中所有后续数据包中使用的数据最大尺寸。

## 依据

参见 the [Java I2P source code](https://github.com/i2p/i2p.i2p/blob/master/apps/streaming/java/src/net/i2p/client/streaming/impl/ConnectionOptions.java#L220) 了解当前值为何为 1730。
参见 the [ECIES specification](/docs/specs/ecies/#overhead) 了解为什么 ECIES 的开销比 ElGamal 少 82 个字节。

## 实现说明

如果流式传输正在创建最佳大小的消息，那么非常重要的是 ECIES-Ratchet 层不会超出该大小进行填充。

适应两个隧道消息的最佳大蒜消息大小，包括 16 字节的大蒜消息 I2NP 头，4 字节的蒜头消息长度，8 字节的 ES 标签和 16 字节的 MAC，为 1956 字节。

在 ECIES 中推荐的填充算法如下：

- 如果大蒜消息的总长度为 1954-1956 字节，则不添加填充块（没有空间）
- 如果大蒜消息的总长度为 1938-1953 字节，则添加填充块以精确填充到 1956 字节。
- 否则，按惯例填充，例如随机填充 0-15 字节。

类似策略可用于单隧道消息大小（964）和三隧道消息大小（2952），尽管这些大小在实践中应该很少见。

## 问题

1812 值为初步值，需要确认并可能调整。

## 迁移

无向后兼容性问题。
这是一个现有的选项，MTU 协商已经是规格的一部分。

旧的 ECIES 目标将支持 1730。
任何接收更高值的客户端将以 1730 响应，对方将按惯例向下协商。

