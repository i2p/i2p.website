---
title: "SSU2 传输"
date: 2022-10-11
author: "zzz"
description: "SSU2 传输"
categories: ["development"]
---

## 概述

自 2005 年以来，I2P 一直使用一种抗审查的 UDP 传输协议“SSU”。在过去的 17 年里，我们几乎没有收到（如果有的话）关于 SSU 被封锁的报告。然而，以当今在安全性、抗封锁能力和性能方面的标准来看，我们还能做得更好。好得多。

因此，我们与[i2pd 项目](https://i2pd.xyz/)合作，创建并实现了 "SSU2"，这是一种按最高的安全与抗封锁标准设计的现代 UDP 协议。该协议将取代 SSU。

我们将业界标准的加密与基于 UDP 的 WireGuard 和 QUIC 协议的最佳特性相结合，并融合了我们基于 TCP 的协议“NTCP2”的抗审查特性。SSU2 可能是有史以来设计出的最安全的传输协议之一。

Java I2P 和 i2pd 团队正在完成 SSU2 传输，我们将在下一个版本中为所有 router 启用它。这将完成我们长达十年的计划，即对可追溯至 2003 年的 Java I2P 最初实现中的全部密码学机制进行升级。SSU2 将取代 SSU，而 SSU 是我们唯一仍在使用 ElGamal 加密的部分。

- Signature types and ECDSA signatures (0.9.8, 2013)
- Ed25519 signatures and leasesets (0.9.15, 2014)
- Ed25519 routers (0.9.22, 2015)
- Destination encryption types and X25519 leasesets (0.9.46, 2020)
- Router encryption types and X25519 routers (0.9.49, 2021)

在完成向 SSU2 的过渡之后，我们将已经把我们所有经过认证和加密的协议迁移到标准的 [Noise Protocol](https://noiseprotocol.org/) 握手：

- NTCP2 (0.9.36, 2018)
- ECIES-X25519-Ratchet end-to-end protocol (0.9.46, 2020)
- ECIES-X25519 tunnel build messages (1.5.0, 2021)
- SSU2 (2.0.0, 2022)

所有 I2P Noise 协议都使用以下标准密码学算法：

- [X25519](https://en.wikipedia.org/wiki/Curve25519)
- [ChaCha20/Poly1305 AEAD](https://www.rfc-editor.org/rfc/rfc8439.html)
- [SHA-256](https://en.wikipedia.org/wiki/SHA-2)

## 目标

- Upgrade the asymmetric cryptography to the much faster X25519
- Use standard symmetric authenticated encryption ChaCha20/Poly1305
- Improve the obfuscation and blocking resistance features of SSU
- Improve the resistance to spoofed addresses by adapting strategies from QUIC
- Improved handshake CPU efficiency
- Improved bandwidth efficiency via smaller handshakes and acknowledgements
- Improve the security of the peer test and relay features of SSU
- Improve the handling of peer IP and port changes by adapting the "connection migration" feature of QUIC
- Move away from heuristic code for packet handling to documented, algorithmic processing
- Support a gradual network transition from SSU to SSU2
- Easy extensibility using the block concept from NTCP2

## 设计

I2P 使用多层加密来保护流量免受攻击者的威胁。最底层是传输协议层，用于两个 router 之间的点对点链路。我们目前有两种传输协议：NTCP2（于 2018 年引入的现代 TCP 协议）和 SSU（于 2005 年开发的 UDP 协议）。

SSU2 与先前的 I2P 传输协议一样，并非用于数据的通用管道。它的主要任务是将 I2P 的底层 I2NP 消息从一个 router 安全地传递到下一个 router。这些点到点连接中的每一个都构成 I2P tunnel 中的一跳。更高层的 I2P 协议在这些点到点连接之上运行，以在 I2P 的各个目的地之间端到端传递 garlic 消息。

设计 UDP 传输会带来在 TCP 协议中不存在的独特且复杂的挑战。UDP 协议必须处理由地址欺骗引发的安全问题，并且必须实现其自身的拥塞控制。此外，所有消息都必须分片以适应网络路径的最大传输单元（MTU），并由接收方重新组装。

我们首先大量借鉴了我们此前在 NTCP2、SSU 和流式协议方面的经验。随后，我们仔细审查并大量借鉴了两个新近开发的 UDP 协议：

- QUIC ([RFC 9000](https://www.rfc-editor.org/rfc/rfc9000.html), [RFC 9001](https://www.rfc-editor.org/rfc/rfc9001.html), [RFC 9002](https://www.rfc-editor.org/rfc/rfc9002.html))
- [WireGuard](https://www.wireguard.com/protocol/)

对抗性的路径内攻击者（例如国家级防火墙）对协议进行分类与封锁，并不是那些协议威胁模型中的明确组成部分。然而，这在 I2P 的威胁模型中是一个重要部分，因为我们的使命是为全球处于风险中的用户提供匿名且抗审查的通信系统。因此，我们的大量设计工作涉及将从 NTCP2 和 SSU 中汲取的经验与 QUIC 和 WireGuard 所支持的特性与安全性相结合。

## 性能

I2P 网络是由多种多样的 routers（路由器）构成的复杂混合体。全球范围内有两种主要实现，运行在从高性能数据中心计算机到树莓派和 Android 手机等各种硬件上。Routers 同时使用 TCP 和 UDP 传输协议。尽管 SSU2 的改进幅度很大，我们并不预计用户能够明显感知到这些变化，无论是在本地还是在端到端传输速度方面。

以下是 SSU2 相对于 SSU 的预计改进的一些亮点：

- 40% reduction in total handshake packet size
- 50% or more reduction in handshake CPU
- 90% or more reduction in ACK overhead
- 50% reduction in packet fragmentation
- 10% reduction in data phase overhead

## 过渡计划

I2P 致力于保持向后兼容性，这既是为了确保网络稳定性，也为了让较旧的 routers 继续发挥作用并保持安全。然而，这也有其限度，因为兼容性会增加代码复杂性和维护需求。

Java I2P 和 i2pd 项目都将在它们的下一个版本（分别为 2.0.0 和 2.44.0，计划于 2022 年 11 月下旬发布）中默认启用 SSU2。然而，它们在禁用 SSU 的计划上有所不同。I2pd 将立即禁用 SSU，因为与其 SSU 实现相比，SSU2 带来了巨大的改进。Java I2P 计划在 2023 年年中禁用 SSU，以支持渐进式过渡，并给较旧的 routers 留出升级时间。

## 摘要


I2P 的创始人不得不为密码学算法和协议做出若干选择。其中有些选择优于另一些，但二十年过去，如今大多数已显露老态。当然，我们早已预见到这一点，并且在过去十年一直在规划并实施密码学升级。

SSU2 是我们漫长升级路径中最后开发、也是最复杂的协议。UDP 的一系列假设以及威胁模型都极具挑战。我们先设计并部署了另外三种 Noise 协议的变体，并从中积累了经验，对安全性与协议设计问题有了更深入的理解。

预计在计划于2022年11月下旬发布的 i2pd 和 Java I2P 版本中启用 SSU2。如果更新顺利，没人会注意到任何不同。尽管性能收益显著，但对大多数人而言可能难以衡量。

一如既往，我们建议在新版本可用时进行更新。维护安全并帮助网络的最佳方式是运行最新版本。
