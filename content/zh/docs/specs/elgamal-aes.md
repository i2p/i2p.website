---
title: "ElGamal/AES + SessionTag 加密"
description: "结合 ElGamal、AES、SHA-256 和一次性会话标签的传统端到端加密"
slug: "elgamal-aes"
aliases:
  - "/zh/how_elgamalaes"
  - "/zh/how_elgamalaes/"
lastUpdated: "2020-04"
accurateFor: "0.9.46"
---

## 概述

ElGamal/AES+SessionTags 用于端到端加密。

作为一个不可靠、无序、基于消息的系统，I2P 使用非对称和对称加密算法的简单组合来为 garlic 消息提供数据机密性和完整性。总体而言，这种组合被称为 ElGamal/AES+SessionTags，但这是一种过于冗长的方式来描述 2048 位 ElGamal、AES256、SHA256 和 32 字节随机数的使用。

当一个router首次想要向另一个router加密garlic消息时，它们使用ElGamal加密AES256会话密钥的密钥材料，并在该加密的ElGamal块之后追加AES256/CBC加密的载荷。除了加密的载荷外，AES加密部分还包含载荷长度、未加密载荷的SHA256哈希值，以及多个"session tags"——随机的32字节随机数。下次发送方想要向另一个router加密garlic消息时，它们不再使用ElGamal加密新的会话密钥，而是简单地选择一个之前传递的session tag，并像之前一样使用AES加密载荷，使用与该session tag一起使用的会话密钥，并在前面加上session tag本身。当一个router接收到garlic加密消息时，它们检查前32个字节以查看是否匹配可用的session tag——如果匹配，它们简单地进行AES解密，但如果不匹配，它们则对第一个块进行ElGamal解密。

每个会话标签只能使用一次，以防止内部对手不必要地将不同消息关联为来自相同的router之间的通信。ElGamal/AES+SessionTag加密消息的发送方选择何时以及传递多少标签，为接收方预先储备足够的标签来覆盖一系列消息。Garlic消息可以通过将一个小的附加消息作为瓣（"传递状态消息"）捆绑来检测成功的标签传递 - 当garlic消息到达预期接收方并成功解密时，这个小的传递状态消息是暴露的瓣之一，并包含指令让接收方将该瓣发送回原始发送方（当然是通过入站tunnel）。当原始发送方收到这个传递状态消息时，他们知道捆绑在garlic消息中的会话标签已成功传递。

Session tags 本身具有较短的生命周期，如果未使用将被丢弃。此外，每个密钥存储的数量是有限的，密钥本身的数量也是如此——如果到达的消息过多，可能会丢弃新消息或旧消息。发送方会跟踪使用 session tags 的消息是否正确传达，如果通信不充分，它可能会丢弃之前假设已正确传递的消息，回退到完整的昂贵 ElGamal 加密。会话将持续存在，直到其所有 tags 耗尽或过期。

会话是单向的。标签从 Alice 传递给 Bob，然后 Alice 在后续发送给 Bob 的消息中逐个使用这些标签。

会话可以在目标节点之间、router之间，或者router与目标节点之间建立。每个router和目标节点都维护自己的会话密钥管理器来跟踪会话密钥和会话标签。独立的会话密钥管理器可以防止对手将多个目标节点彼此关联或与router关联。

## 消息接收

每个接收到的消息都有以下两种可能的情况之一：

1. 它是现有会话的一部分，包含会话标签和AES加密块
2. 它用于新会话，包含ElGamal和AES加密块

当 router 收到消息时，它首先假设消息来自现有会话，并尝试查找 Session Tag 并使用 AES 解密后续数据。如果失败，它将假设这是新会话的消息，并尝试使用 ElGamal 进行解密。

## 新会话消息规范 {#new}

一个新会话 ElGamal 消息包含两个部分，一个加密的 ElGamal 块和一个加密的 AES 块。

加密消息包含：

```
   +----+----+----+----+----+----+----+----+
   |                                       |
   +                                       +
   |       ElGamal Encrypted Block         |
   ~                                       ~
   |                                       |
   +         +----+----+----+----+----+----+
   |         |                             |
   +----+----+                             +
   |                                       |
   +                                       +
   |         AES Encrypted Block           |
   ~                                       ~
   |                                       |
   +         +----+----+----+----+----+----+
   |         +
   +----+----+
```
### ElGamal 块

加密的 ElGamal 块长度始终为 514 字节。

未加密的 ElGamal 数据长度为 222 字节，包含：

```
   +----+----+----+----+----+----+----+----+
   |                                       |
   +                                       +
   |           Session Key                 |
   +                                       +
   |                                       |
   +                                       +
   |                                       |
   +----+----+----+----+----+----+----+----+
   |                                       |
   +                                       +
   |              Pre-IV                   |
   +                                       +
   |                                       |
   +                                       +
   |                                       |
   +----+----+----+----+----+----+----+----+
   +                                       +
   |                                       |
   +                                       +
   |       158 bytes random padding        |
   ~                                       ~
   |                                       |
   +                             +----+----+
   |                             |
   +----+----+----+----+----+----+
```
32字节的[Session Key](/docs/specs/common-structures#type_SessionKey)是会话的标识符。32字节的Pre-IV将用于生成后续AES块的IV；IV是Pre-IV的SHA-256哈希值的前16个字节。

222字节的载荷使用[ElGamal加密](/docs/specs/cryptography#elgamal)，加密后的数据块长度为514字节。

### AES块 {#aes}

AES块中的未加密数据包含以下内容：

```
   +----+----+----+----+----+----+----+----+
   |tag count|                             |
   +----+----+                             +
   |                                       |
   +                                       +
   |          Session Tags                 |
   ~                                       ~
   |                                       |
   +                                       +
   |                                       |
   +         +----+----+----+----+----+----+
   |         |    payload size   |         |
   +----+----+----+----+----+----+         +
   |                                       |
   +                                       +
   |          Payload Hash                 |
   +                                       +
   |                                       |
   +                             +----+----+
   |                             |flag|    |
   +----+----+----+----+----+----+----+    +
   |                                       |
   +                                       +
   |          New Session Key (opt.)       |
   +                                       +
   |                                       |
   +                                  +----+
   |                                  |    |
   +----+----+----+----+----+----+----+    +
   |                                       |
   +                                       +
   |           Payload                     |
   ~                                       ~
   |                                       |
   +                        +----//---+----+
   |                        |              |
   +----+----+----//---+----+              +
   |          Padding to 16 bytes          |
   +----+----+----+----+----+----+----+----+
```
#### 定义

```
tag count:
    2-byte Integer, 0-200

Session Tags:
    That many 32-byte SessionTags

payload size:
    4-byte Integer

Payload Hash:
    The 32-byte SHA256 Hash of the payload

flag:
    A one-byte value. Normally == 0. If == 0x01, a Session Key follows

New Session Key:
    A 32-byte SessionKey,
    to replace the old key, and is only present if preceding flag is 0x01

Payload:
    the data

Padding:
    Random data to a multiple of 16 bytes for the total length.
    May contain more than the minimum required padding.
```
最小长度：48 字节

然后使用来自 ElGamal 部分的会话密钥和 IV（从 pre-IV 计算得出）对数据进行 [AES 加密](/docs/specs/cryptography)。加密的 AES 块长度是可变的，但始终是 16 字节的倍数。

#### 注意事项

- 实际的最大载荷长度和最大块长度小于64 KB；详见[I2NP 概述](/docs/protocol/i2np)。
- New Session Key目前未使用，永远不会出现。

## 现有会话消息规范 {#existing}

成功传送的会话标签会被记住一段短暂的时间（目前为15分钟），直到它们被使用或丢弃。标签通过将其打包在现有会话消息中来使用，该消息仅包含一个AES加密块，且前面没有ElGamal块。

现有的会话消息如下：

```
   +----+----+----+----+----+----+----+----+
   |                                       |
   +                                       +
   |            Session Tag                |
   +                                       +
   |                                       |
   +                                       +
   |                                       |
   +----+----+----+----+----+----+----+----+
   |                                       |
   +                                       +
   |         AES Encrypted Block           |
   ~                                       ~
   |                                       |
   +                                       +
   |                                       |
   +----+----+----+----+----+----+----+----+
```
#### 定义

```
Session Tag:
    A 32-byte SessionTag
    previously delivered in an AES block

AES Encrypted Block:
    As specified above.
```
会话标签也用作预初始化向量。初始化向量是会话标签SHA-256哈希值的前16个字节。

要解码来自现有会话的消息，router 会查找 Session Tag 以找到关联的 Session Key。如果找到了 Session Tag，则使用关联的 Session Key 解密 AES 块。如果未找到标签，则假定该消息是 [New Session Message](#new)。

## Session Tag 配置选项 {#config}

从 0.9.2 版本开始，客户端可以配置要发送的默认 Session Tags 数量和当前会话的低标签阈值。对于短暂的流连接或数据报，这些选项可用于显著减少带宽使用。详情请参见 [I2CP options specification](/docs/protocol/i2cp#options)。会话设置也可以在每条消息的基础上进行覆盖。详情请参见 [I2CP Send Message Expires specification](/docs/specs/i2cp#msg_SendMessageExpires)。

## 未来工作 {#future}

**注意：** ElGamal/AES+SessionTags 正在被 ECIES-X25519-AEAD-Ratchet（提案 144）替代。下面提到的问题和想法已经被纳入新协议的设计中。以下条目将不会在 ElGamal/AES+SessionTags 中得到解决。

有许多可能的区域可以调整会话密钥管理器的算法；其中一些可能与流库行为相互作用，或对整体性能产生重大影响。

- 交付的标签数量可能取决于消息大小，需要考虑在tunnel消息层最终填充到1KB的情况。

- 客户端可以向router发送会话生命周期的估计值，作为所需标签数量的建议。

- 提供的标签太少会导致 router 回退到昂贵的 ElGamal 加密。

- router 可以假定 Session Tags 已送达，或在使用它们之前等待确认；每种策略都有权衡。

- 对于非常简短的消息，ElGamal 块中预 IV 和填充字段的几乎全部 222 字节都可以用于整个消息，而无需建立会话。

- 评估填充策略；目前我们填充到最少128字节。
  对小消息添加一些标签会比填充更好。

- 如果 Session Tag 系统是双向的，也许效率会更高，
  这样在"正向"路径中传递的标签可以在"反向"路径中使用，
  从而避免在初始响应中使用 ElGamal。
  router 目前在向自身发送 tunnel 测试消息时就使用了一些类似的技巧。

- 从会话标签改为
  [同步PRNG](/docs/overview/performance#future#prng)。

- 这些想法中的一些可能需要新的 I2NP 消息类型，或者
  在 [传递指令](/docs/specs/tunnel-message#struct_TunnelMessageDeliveryInstructions) 中设置标志，
  或者在会话密钥字段的前几个字节中设置魔术数字，
  并接受随机会话密钥匹配魔术数字的小风险。
