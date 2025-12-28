---
title: "ECIES-X25519-AEAD-Ratchet"
number: "144"
author: "zzz, chisana, orignal"
created: "2018-11-22"
lastupdated: "2025-03-05"
status: "已关闭"
thread: "http://zzz.i2p/topics/2639"
target: "0.9.46"
implementedin: "0.9.46"
toc: true
---

## 注意

网络部署和测试正在进行中。可能会有小幅修订。请参阅[规范](/docs/specs/ecies/)获取官方规格说明。

截至 0.9.46 版本，以下功能尚未实现：

- MessageNumbers、Options 和 Termination 块
- 协议层响应
- 零静态密钥
- 多播

## 概述

这是自 I2P 诞生以来第一个新的端到端加密类型提案，用于替换 ElGamal/AES+SessionTags [Elg-AES](/docs/legacy/elgamal-aes/)。

它依赖于以下先前的工作：

- 通用结构规范 [Common Structures](/docs/specs/common-structures/)
- [I2NP](/docs/specs/i2np/) 规范包含 LS2
- ElGamal/AES+Session Tags [Elg-AES](/docs/legacy/elgamal-aes/)
- [http://zzz.i2p/topics/1768](http://zzz.i2p/topics/1768) 新的非对称加密概述
- 底层加密概述 [CRYPTO-ELG](/docs/specs/cryptography/)
- ECIES [http://zzz.i2p/topics/2418](http://zzz.i2p/topics/2418)
- [NTCP2](/docs/specs/ntcp2/) [提案 111](/proposals/111-ntcp-2/)
- 123 新的 netDB 条目
- 142 新加密模板
- [Noise](https://noiseprotocol.org/noise.html) 协议
- [Signal](https://signal.org/docs/) 双棘轮算法

目标是支持端到端、目标到目标通信的新加密技术。

该设计将使用 Noise 握手和数据阶段，结合 Signal 的双重棘轮机制。

本提案中对 Signal 和 Noise 的所有引用仅用于背景信息。理解或实现本提案不需要了解 Signal 和 Noise 协议的相关知识。

### Current ElGamal Uses

作为回顾，ElGamal 256字节公钥可以在以下数据结构中找到。请参考通用结构规范。

- 在路由器身份中
  这是路由器的加密密钥。

- 在目标地址中
  目标地址的公钥曾用于旧的 i2cp-to-i2cp 加密，
  该功能在 0.6 版本中被禁用，目前除了用作
  LeaseSet 加密的 IV（已弃用）外，暂未使用。
  改为使用 LeaseSet 中的公钥。

- 在 LeaseSet 中
  这是目标的加密密钥。

- 在 LS2 中
  这是目标地址的加密密钥。

### EncTypes in Key Certs

作为回顾，当我们添加对签名类型的支持时，我们也添加了对加密类型的支持。加密类型字段始终为零，无论是在目标地址还是 RouterIdentities 中都是如此。是否要改变这一点仍有待确定。请参考通用结构规范 [Common Structures](/docs/specs/common-structures/)。

### 当前 ElGamal 用途

作为回顾，我们使用 ElGamal 用于：

1) Tunnel Build 消息（密钥在 RouterIdentity 中）    本提案未涵盖替换方案。    参见提案 152 [Proposal 152](/proposals/152-ecies-tunnels)。

2) Router-to-router 加密 netdb 和其他 I2NP 消息（密钥在 RouterIdentity 中）    依赖于此提案。    需要为 1) 制定提案，或将密钥放在 RI 选项中。

3) 客户端端到端 ElGamal+AES/SessionTag (密钥在 LeaseSet 中，Destination 密钥未使用)    替换方案在本提案中有涵盖。

4) NTCP1 和 SSU 的临时 DH    替换方案不在此提案中涵盖。    参见提案 111 关于 NTCP2。    目前没有关于 SSU2 的提案。

### 密钥证书中的 EncTypes

- 向后兼容
- 需要并基于 LS2 (提案 123)
- 利用为 NTCP2 添加的新加密或原语 (提案 111)
- 不需要新的加密或原语来支持
- 维持加密和签名的解耦；支持所有当前和未来版本
- 为目标启用新加密
- 为 router 启用新加密，但仅用于 garlic 消息 - tunnel 构建将是
  单独的提案
- 不破坏任何依赖 32 字节二进制目标哈希的功能，例如 bittorrent
- 使用临时-静态 DH 维持 0-RTT 消息传递
- 在此协议层不要求缓冲/排队消息；
  继续支持双向无限消息传递而无需等待响应
- 在 1 RTT 后升级到临时-临时 DH
- 维持乱序消息的处理
- 维持 256 位安全性
- 添加前向保密性
- 添加身份验证 (AEAD)
- 比 ElGamal 的 CPU 效率高得多
- 不依赖 Java jbigi 来提高 DH 效率
- 最小化 DH 操作
- 比 ElGamal 的带宽效率高得多 (514 字节 ElGamal 块)
- 如有需要，在同一 tunnel 上支持新旧加密
- 接收方能够有效地区分来自同一
  tunnel 的新旧加密
- 其他人无法区分新旧或未来的加密
- 消除新与现有会话长度分类 (支持填充)
- 不需要新的 I2NP 消息
- 用 AEAD 替换 AES 负载中的 SHA-256 校验和
- 支持传输和接收会话的绑定，以便
  确认可以在协议内进行，而不是仅在带外进行。
  这也将允许回复立即具有前向保密性。
- 启用我们目前由于 CPU 开销而未进行的某些消息 (RouterInfo 存储)
  的端到端加密。
- 不改变 I2NP Garlic Message
  或 Garlic Message 传递指令格式。
- 消除 Garlic Clove Set 和 Clove 格式中未使用或冗余的字段。

消除 session tags 的几个问题，包括：

- 在第一次回复之前无法使用 AES
- 如果假设标签传递成功会导致不可靠性和停滞
- 带宽效率低下，特别是在首次传递时
- 存储标签的空间效率极低
- 传递标签的带宽开销巨大
- 高度复杂，难以实现
- 难以针对各种用例进行调优
  （流式传输与数据报、服务器与客户端、高带宽与低带宽）
- 由于标签传递导致的内存耗尽漏洞

### 非对称加密用途

- LS2 格式更改（提案 123 已完成）
- 新的 DHT 轮换算法或共享随机生成
- 隧道构建的新加密。
  参见提案 152 [Proposal 152](/proposals/152-ecies-tunnels)。
- 隧道层加密的新加密。
  参见提案 153 [Proposal 153](/proposals/153-chacha20-layer-encryption)。
- I2NP DLM / DSM / DSRM 消息的加密、传输和接收方法。
  不更改。
- 不支持 LS1 到 LS2 或 ElGamal/AES 到本提案的通信。
  本提案是双向协议。
  目标可以通过使用相同隧道发布两个 leaseSet，或在 LS2 中放置两种加密类型来处理向后兼容性。
- 威胁模型更改
- 实现细节在此不讨论，留给各个项目。
- （乐观）添加扩展或钩子以支持组播

### 目标

ElGamal/AES+SessionTag 协议作为我们唯一的端到端协议已经使用了大约 15 年，基本上没有对协议进行任何修改。现在有了更快的密码学原语。我们需要增强协议的安全性。我们还开发了启发式策略和变通方法来最小化协议的内存和带宽开销，但这些策略很脆弱，难以调整，并且使协议更容易出现故障，导致会话中断。

在大约相同的时间段内，ElGamal/AES+SessionTag 规范和相关文档已经描述了传输 session tag 的带宽成本有多高，并提议用"同步 PRNG"来替代 session tag 传输。同步 PRNG 基于共同种子，在两端确定性地生成相同的标签。同步 PRNG 也可以称为"棘轮"。这个提案（最终）指定了该棘轮机制，并消除了标签传输。

通过使用棘轮机制（同步的伪随机数生成器）来生成会话标签，我们消除了在新会话消息和后续需要时发送会话标签的开销。对于典型的32个标签的标签集，这相当于1KB的数据。这也消除了发送方对会话标签的存储需求，从而将存储要求减半。

需要一个完整的双向握手，类似于 Noise IK 模式，以避免密钥泄露冒充攻击（KCI）。请参阅 [NOISE](https://noiseprotocol.org/noise.html) 中的 Noise "Payload Security Properties" 表格。有关 KCI 的更多信息，请参阅论文 https://www.usenix.org/system/files/conference/woot15/woot15-paper-hlauschek.pdf

### 非目标 / 超出范围

威胁模型与 NTCP2（提案 111）有所不同。中间人攻击节点是 OBEP 和 IBGW，假设它们通过与 floodfill 节点串通，能够完全查看当前或历史的全球 NetDB。

目标是防止这些中间人攻击者将流量分类为新的和现有会话消息，或者分类为新加密与旧加密。

## Detailed Proposal

该提案定义了一个新的端到端协议来替代 ElGamal/AES+SessionTags。该设计将使用 Noise 握手和包含 Signal 双棘轮机制的数据阶段。

### 理由说明

协议需要重新设计的部分共有五个：

- 1) 新的和现有的会话容器格式
  将被新格式替换。
- 2) ElGamal（256字节公钥，128字节私钥）将被
  ECIES-X25519（32字节公钥和私钥）替换
- 3) AES将被
  AEAD_ChaCha20_Poly1305（以下简称为ChaChaPoly）替换
- 4) SessionTags将被棘轮机制替换，
  这本质上是一个加密的、同步的伪随机数生成器。
- 5) 在ElGamal/AES+SessionTags规范中定义的AES载荷
  将被类似于NTCP2中的块格式替换。

以下五个变更分别在各自的章节中介绍。

### 威胁模型

现有的 I2P router 实现需要为以下标准密码学原语提供实现，这些原语在当前的 I2P 协议中并非必需：

- ECIES（但这本质上是 X25519）
- Elligator2

尚未实现 [NTCP2](/docs/specs/ntcp2/) ([提案 111](/proposals/111-ntcp-2/)) 的现有 I2P router 实现还需要实现：

- X25519 密钥生成和 DH
- AEAD_ChaCha20_Poly1305（以下简称 ChaChaPoly）
- HKDF

### Crypto Type

加密类型（在 LS2 中使用）是 4。这表示一个小端序 32 字节 X25519 公钥，以及此处指定的端到端协议。

加密类型 0 是 ElGamal。加密类型 1-3 保留用于 ECIES-ECDH-AES-SessionTag，参见提案 145 [Proposal 145](/proposals/145-ecies)。

### 密码学设计概述

本提案基于 Noise 协议框架 [NOISE](https://noiseprotocol.org/noise.html)（修订版 34，2018-07-11）提供要求。Noise 具有与 Station-To-Station 协议 [STS](https://en.wikipedia.org/wiki/Station-to-Station_protocol) 相似的特性，后者是 [SSU](/docs/legacy/ssu/) 协议的基础。在 Noise 术语中，Alice 是发起方，Bob 是响应方。

该提案基于 Noise 协议 Noise_IK_25519_ChaChaPoly_SHA256。（初始密钥派生函数的实际标识符是 "Noise_IKelg2_25519_ChaChaPoly_SHA256"，以表示 I2P 扩展 - 参见下面的 KDF 1 部分）此 Noise 协议使用以下基元：

- Interactive Handshake Pattern: IK
  Alice 立即向 Bob 传输她的静态密钥 (I)
  Alice 已经知道 Bob 的静态密钥 (K)

- One-Way Handshake Pattern: N
  Alice 不向 Bob 传输她的静态密钥 (N)

- DH Function: X25519
  X25519 DH，密钥长度为32字节，如[RFC-7748](https://tools.ietf.org/html/rfc7748)中所规定。

- Cipher Function: ChaChaPoly
  AEAD_CHACHA20_POLY1305，如 [RFC-7539](https://tools.ietf.org/html/rfc7539) 第 2.8 节所规定。
  12 字节随机数，前 4 个字节设为零。
  与 [NTCP2](/docs/specs/ntcp2/) 中的相同。

- Hash Function: SHA256
  标准32字节哈希，已在I2P中广泛使用。

### I2P 的新密码学基元

此提案定义了对 Noise_IK_25519_ChaChaPoly_SHA256 的以下增强。这些增强通常遵循 [NOISE](https://noiseprotocol.org/noise.html) 第 13 节中的指导原则。

1) 明文临时密钥使用 [Elligator2](https://elligator.cr.yp.to/) 进行编码。

2) 回复以明文标签作为前缀。

3) 负载格式为消息 1、消息 2 和数据阶段定义。当然，这在 Noise 中没有定义。

所有消息都包含一个 [I2NP](/docs/specs/i2np/) Garlic Message 头部。数据阶段使用与 Noise 数据阶段相似但不兼容的加密方式。

### 加密类型

握手使用 [Noise](https://noiseprotocol.org/noise.html) 握手模式。

使用以下字母映射：

- e = 一次性临时密钥
- s = 静态密钥
- p = 消息载荷

一次性会话和无绑定会话类似于 Noise N 模式。

```

<- s
  ...
  e es p ->

```
绑定会话类似于 Noise IK 模式。

```

<- s
  ...
  e es s ss p ->
  <- tag e ee se
  <- p
  p ->

```
### Noise Protocol Framework

当前的 ElGamal/AES+SessionTag 协议是单向的。在此层，接收方不知道消息来自何处。出站和入站会话没有关联。确认是通过在 clove 中使用 DeliveryStatusMessage（包装在 GarlicMessage 中）进行带外处理的。

单向协议存在大量低效问题。任何回复也必须使用昂贵的"新会话"消息。这会导致更高的带宽、CPU和内存使用量。

单向协议也存在安全弱点。所有会话都基于临时-静态DH。没有返回路径，Bob无法将其静态密钥"棘轮"到临时密钥。在不知道消息来源的情况下，无法将接收到的临时密钥用于出站消息，因此初始回复也使用临时-静态DH。

对于此提案，我们定义了两种创建双向协议的机制 - "配对"和"绑定"。这些机制提供了更高的效率和安全性。

### 框架新增功能

与 ElGamal/AES+SessionTags 一样，所有入站和出站会话都必须在给定的上下文中，要么是 router 的上下文，要么是特定本地目标的上下文。在 Java I2P 中，这个上下文称为 Session Key Manager。

会话不得在上下文之间共享，因为这会允许各种本地目标之间，或本地目标与router之间产生关联。

当给定目的地同时支持 ElGamal/AES+SessionTags 和此提议时，两种类型的会话可能共享一个上下文。请参见下面的第 1c) 节。

### 握手模式

当发起方（Alice）创建出站会话时，会创建一个新的入站会话并与出站会话配对，除非不需要回复（例如原始数据报）。

新的入站会话总是与新的出站会话配对，除非不需要回复（例如原始数据报）。

如果请求回复并绑定到远端目标或router，那么新的出站会话将绑定到该目标或router，并替换之前到该目标或router的任何出站会话。

配对入站和出站会话提供了一个具有 DH 密钥棘轮功能的双向协议。

### 会话

对于给定的目标或router，只有一个出站会话。可能存在来自给定目标或router的多个当前入站会话。通常，当创建新的入站会话并在该会话上接收到流量（作为ACK）时，任何其他会话都将被标记为相对快速地过期，大约在一分钟左右。会检查先前发送的消息（PN）值，如果在先前的入站会话中没有未接收的消息（在窗口大小范围内），则先前的会话可能会立即被删除。

当发起方（Alice）创建出站会话时，它会绑定到远端目标（Bob），任何配对的入站会话也将绑定到远端目标。随着会话的推进，它们将继续绑定到远端目标。

当在接收方（Bob）创建入站会话时，该会话可以绑定到远端 Destination（Alice），这取决于 Alice 的选择。如果 Alice 在新会话消息中包含绑定信息（她的静态密钥），该会话将绑定到该 destination，并且将创建一个出站会话绑定到同一个 Destination。随着会话的棘轮化，它们将继续绑定到远端 Destination。

### 会话上下文

对于常见的流式传输情况，我们期望 Alice 和 Bob 按如下方式使用协议：

- Alice 将她的新出站会话与新入站会话配对，两者都绑定到远端目标（Bob）。
- Alice 在发送给 Bob 的 New Session 消息中包含绑定信息和签名，以及回复请求。
- Bob 将他的新入站会话与新出站会话配对，两者都绑定到远端目标（Alice）。
- Bob 在配对会话中向 Alice 发送回复（确认），并棘轮到新的 DH 密钥。
- Alice 使用 Bob 的新密钥棘轮到新的出站会话，与现有入站会话配对。

通过将入站会话绑定到远端目标地址(Destination)，并将入站会话与绑定到相同目标地址的出站会话配对，我们可以获得两个主要优势：

1) Bob 对 Alice 的初始回复使用临时-临时 DH

2) 在 Alice 收到 Bob 的回复并进行 ratchet 操作后，Alice 发送给 Bob 的所有后续消息都使用临时-临时 DH。

### 配对入站和出站会话

在ElGamal/AES+SessionTags中，当LeaseSet作为garlic clove打包，或者标签被传递时，发送router请求一个ACK。这是一个单独的garlic clove，包含一个DeliveryStatus消息。为了额外的安全性，DeliveryStatus消息被包装在一个Garlic消息中。从协议的角度来看，这种机制是带外的。

在新协议中，由于入站和出站会话是配对的，我们可以在带内进行ACK。不需要单独的clove。

显式 ACK 简单来说就是一个不包含 I2NP 块的现有会话消息。然而，在大多数情况下，可以避免显式 ACK，因为存在反向流量。对于实现来说，可能需要等待一小段时间（也许一百毫秒）再发送显式 ACK，以便给流传输层或应用层时间来响应。

实现还需要推迟发送任何ACK，直到I2NP块被处理完毕，因为Garlic Message可能包含带有lease set的Database Store Message。需要最新的lease set来路由ACK，并且需要远端目标（包含在lease set中）来验证绑定静态密钥。

### 绑定会话和目标

出站会话应该总是比入站会话先过期。一旦出站会话过期并创建了新的会话，相应的新配对入站会话也会被创建。如果存在旧的入站会话，它将被允许过期。

### 绑定和配对的优势

待定

### 消息确认

我们定义了与所使用的密码学构建块相对应的以下函数。

ZEROLEN

    zero-length byte array

CSRNG(n)

    n-byte output from a cryptographically-secure random number generator.

H(p, d)

    SHA-256 hash function that takes a personalization string p and data d, and
    produces an output of length 32 bytes.
    As defined in [NOISE](https://noiseprotocol.org/noise.html).
    || below means append.

    Use SHA-256 as follows::

        H(p, d) := SHA-256(p || d)

MixHash(d)

    SHA-256 hash function that takes a previous hash h and new data d,
    and produces an output of length 32 bytes.
    || below means append.

    Use SHA-256 as follows::

        MixHash(d) := h = SHA-256(h || d)

STREAM

    The ChaCha20/Poly1305 AEAD as specified in [RFC-7539](https://tools.ietf.org/html/rfc7539).
    S_KEY_LEN = 32 and S_IV_LEN = 12.

    ENCRYPT(k, n, plaintext, ad)
        Encrypts plaintext using the cipher key k, and nonce n which MUST be unique for
        the key k.
        Associated data ad is optional.
        Returns a ciphertext that is the size of the plaintext + 16 bytes for the HMAC.

        The entire ciphertext must be indistinguishable from random if the key is secret.

    DECRYPT(k, n, ciphertext, ad)
        Decrypts ciphertext using the cipher key k, and nonce n.
        Associated data ad is optional.
        Returns the plaintext.

DH

    X25519 public key agreement system. Private keys of 32 bytes, public keys of 32
    bytes, produces outputs of 32 bytes. It has the following
    functions:

    GENERATE_PRIVATE()
        Generates a new private key.

    DERIVE_PUBLIC(privkey)
        Returns the public key corresponding to the given private key.

    GENERATE_PRIVATE_ELG2()
        Generates a new private key that maps to a public key suitable for Elligator2 encoding.
        Note that half of the randomly-generated private keys will not be suitable and must be discarded.

    ENCODE_ELG2(pubkey)
        Returns the Elligator2-encoded public key corresponding to the given public key (inverse mapping).
        Encoded keys are little endian.
        Encoded key must be 256 bits indistinguishable from random data.
        See Elligator2 section below for specification.

    DECODE_ELG2(pubkey)
        Returns the public key corresponding to the given Elligator2-encoded public key.
        See Elligator2 section below for specification.

    DH(privkey, pubkey)
        Generates a shared secret from the given private and public keys.

HKDF(salt, ikm, info, n)

    A cryptographic key derivation function which takes some input key material ikm (which
    should have good entropy but is not required to be a uniformly random string), a salt
    of length 32 bytes, and a context-specific 'info' value, and produces an output
    of n bytes suitable for use as key material.

    Use HKDF as specified in [RFC-5869](https://tools.ietf.org/html/rfc5869), using the HMAC hash function SHA-256
    as specified in [RFC-2104](https://tools.ietf.org/html/rfc2104). This means that SALT_LEN is 32 bytes max.

MixKey(d)

    Use HKDF() with a previous chainKey and new data d, and
    sets the new chainKey and k.
    As defined in [NOISE](https://noiseprotocol.org/noise.html).

    Use HKDF as follows::

        MixKey(d) := output = HKDF(chainKey, d, "", 64)
                     chainKey = output[0:31]
                     k = output[32:63]


### 会话超时

### 组播

[I2NP](/docs/specs/i2np/) 中规定的 Garlic Message 如下所示。由于设计目标是中间跳点无法区分新旧加密，因此这种格式不能更改，即使长度字段是冗余的。该格式显示了完整的 16 字节头部，尽管实际的头部可能采用不同的格式，具体取决于所使用的传输方式。

解密后，数据包含一系列 Garlic Cloves 和附加数据，也称为 Clove Set。

详见 [I2NP](/docs/specs/i2np/) 了解详细信息和完整规范。

```

+----+----+----+----+----+----+----+----+
  |type|      msg_id       |  expiration
  +----+----+----+----+----+----+----+----+
                           |  size   |chks|
  +----+----+----+----+----+----+----+----+
  |      length       |                   |
  +----+----+----+----+                   +
  |          encrypted data               |
  ~                                       ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

```
### 定义

目前使用了超过15年的消息格式是ElGamal/AES+SessionTags。在ElGamal/AES+SessionTags中，有两种消息格式：

1) 新会话：- 514 字节 ElGamal 块 - AES 块（最少 128 字节，16 的倍数）

2) 现有会话：- 32字节Session Tag - AES块（最少128字节，16的倍数）

最小填充到 128 字节是在 Java I2P 中实现的，但在接收时不会强制执行。

这些消息被封装在一个 I2NP garlic 消息中，该消息包含一个长度字段，因此长度是已知的。

注意，没有定义对非模16长度的填充，因此新会话总是（mod 16 == 2），而现有会话总是（mod 16 == 0）。我们需要修复这个问题。

接收方首先尝试查找前32字节作为Session Tag。如果找到，他解密AES块。如果未找到，且数据长度至少为(514+16)，他尝试解密ElGamal块，如果成功，则解密AES块。

### 1) 消息格式

在 Signal Double Ratchet 中，报头包含：

- DH: 当前棘轮公钥
- PN: 前一链消息长度
- N: 消息编号

Signal 的"发送链"大致相当于我们的标签集。通过使用会话标签，我们可以消除其中的大部分。

在新会话中，我们仅将公钥放在未加密的头部中。

在现有会话中，我们为头部使用会话标签。会话标签与当前的 ratchet 公钥和消息编号相关联。

在新会话和现有会话中，PN 和 N 都位于加密主体中。

在 Signal 中，事情在不断地棘轮化。新的 DH 公钥要求接收方进行棘轮操作并发送新的公钥回去，这也作为对接收到的公钥的确认。这对我们来说会有太多的 DH 操作。所以我们将接收到的密钥的确认和新公钥的传输分开。任何使用从新 DH 公钥生成的会话标签的消息都构成一个 ACK。我们只有在希望重新密钥时才传输新的公钥。

在 DH 必须进行棘轮操作之前的最大消息数量是 65535。

在传递会话密钥时，我们从中派生"Tag Set"，而不必同时传递会话标签。一个Tag Set最多可以包含65536个标签。但是，接收方应该实现"预读"策略，而不是一次生成所有可能的标签。最多只生成超过最后一个有效接收标签的N个标签。N的值最多可能是128，但32甚至更少可能是更好的选择。

### 当前消息格式审查

新会话一次性公钥（32字节）加密数据和MAC（剩余字节）

New Session 消息可能包含也可能不包含发送方的静态公钥。如果包含，反向会话将绑定到该密钥。如果期望收到回复，即对于流传输和可回复数据报，应该包含静态密钥。对于原始数据报则不应包含。

New Session 消息类似于单向 Noise [NOISE](https://noiseprotocol.org/noise.html) 模式 "N"（如果不发送静态密钥），或双向模式 "IK"（如果发送静态密钥）。

### 加密数据格式审查

长度为 96 + 载荷长度。加密格式：

```

+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   New Session Ephemeral Public Key    |
  +             32 bytes                  +
  |     Encoded with Elligator2           |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +         Static Key                    +
  |       ChaCha20 encrypted data         |
  +            32 bytes                   +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +    (MAC) for Static Key Section       +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |       ChaCha20 encrypted data         |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) for Payload Section     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  Public Key :: 32 bytes, little endian, Elligator2, cleartext

  Static Key encrypted data :: 32 bytes

  Payload Section encrypted data :: remaining data minus 16 bytes

  MAC :: Poly1305 message authentication code, 16 bytes

```
### 新会话标签与Signal的比较

临时密钥为 32 字节，使用 Elligator2 编码。此密钥不会被重复使用；每条消息都会生成新密钥，包括重传消息。

### 1a) 新会话格式

解密后，Alice的X25519静态密钥，32字节。

### 1b) 新会话格式（带绑定）

加密长度是数据的剩余部分。解密长度比加密长度少16字节。有效载荷必须包含一个DateTime块，通常还会包含一个或多个Garlic Clove块。格式和其他要求请参见下面的有效载荷部分。

### 新会话临时密钥

如果不需要回复，则不发送静态密钥。

长度为 96 + 载荷长度。加密格式：

```

+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   New Session Ephemeral Public Key    |
  +             32 bytes                  +
  |     Encoded with Elligator2           |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +           Flags Section               +
  |       ChaCha20 encrypted data         |
  +            32 bytes                   +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) for above section       +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |       ChaCha20 encrypted data         |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) for Payload Section     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  Public Key :: 32 bytes, little endian, Elligator2, cleartext

  Flags Section encrypted data :: 32 bytes

  Payload Section encrypted data :: remaining data minus 16 bytes

  MAC :: Poly1305 message authentication code, 16 bytes

```
### 静态密钥

Alice的临时密钥。临时密钥为32字节，使用Elligator2编码，小端序。此密钥永不重复使用；每条消息都会生成新密钥，包括重传消息。

### 负载

Flags 部分不包含任何内容。它总是 32 字节，因为它必须与带绑定的新会话消息中的静态密钥长度相同。Bob 通过测试这 32 字节是否全为零来判断它是静态密钥还是 flags 部分。

TODO 这里需要任何标志吗？

### 1c) 新会话格式（无绑定）

加密长度是数据的剩余部分。解密长度比加密长度少16字节。有效载荷必须包含一个DateTime块，通常还会包含一个或多个Garlic Clove块。格式和其他要求请参见下面的有效载荷部分。

### 新会话临时密钥

如果预期只发送单条消息，则不需要会话设置或静态密钥。

长度为 96 + 负载长度。加密格式：

```

+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |       Ephemeral Public Key            |
  +             32 bytes                  +
  |     Encoded with Elligator2           |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +           Flags Section               +
  |       ChaCha20 encrypted data         |
  +            32 bytes                   +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) for above section       +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |       ChaCha20 encrypted data         |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) for Payload Section     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  Public Key :: 32 bytes, little endian, Elligator2, cleartext

  Flags Section encrypted data :: 32 bytes

  Payload Section encrypted data :: remaining data minus 16 bytes

  MAC :: Poly1305 message authentication code, 16 bytes

```
### Flags Section 解密数据

一次性密钥为 32 字节，使用 Elligator2 编码，小端序。此密钥永不重复使用；每条消息都会生成新密钥，包括重传消息。

### 有效载荷

Flags 部分不包含任何内容。它始终为 32 字节，因为它必须与用于绑定的新会话消息的静态密钥长度相同。Bob 通过测试这 32 字节是否全为零来确定它是静态密钥还是 flags 部分。

TODO 这里需要任何标志吗？

```

+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                                       |
  +             All zeros                 +
  |              32 bytes                 |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+

  zeros:: All zeros, 32 bytes.

```
### 1d) 一次性格式（无绑定或会话）

加密长度是数据的剩余部分。解密长度比加密长度少 16。载荷必须包含一个 DateTime 块，通常还会包含一个或多个 Garlic Clove 块。格式和附加要求请参见下面的载荷部分。

### 新会话一次性密钥

### Flags Section 解密数据

这是用于 IK 的标准 [NOISE](https://noiseprotocol.org/noise.html)，使用修改后的协议名称。注意我们对 IK 模式（绑定会话）和 N 模式（非绑定会话）使用相同的初始化器。

协议名称被修改有两个原因。首先，表示临时密钥使用 Elligator2 编码，其次，表示在第二个消息之前调用 MixHash() 来混合标签值。

```

This is the "e" message pattern:

  // Define protocol_name.
  Set protocol_name = "Noise_IKelg2+hs2_25519_ChaChaPoly_SHA256"
   (40 bytes, US-ASCII encoded, no NULL termination).

  // Define Hash h = 32 bytes
  h = SHA256(protocol_name);

  Define ck = 32 byte chaining key. Copy the h data to ck.
  Set chainKey = h

  // MixHash(null prologue)
  h = SHA256(h);

  // up until here, can all be precalculated by Alice for all outgoing connections

```
### 载荷

```

This is the "e" message pattern:

  // Bob's X25519 static keys
  // bpk is published in leaseset
  bsk = GENERATE_PRIVATE()
  bpk = DERIVE_PUBLIC(bsk)

  // Bob static public key
  // MixHash(bpk)
  // || below means append
  h = SHA256(h || bpk);

  // up until here, can all be precalculated by Bob for all incoming connections

  // Alice's X25519 ephemeral keys
  aesk = GENERATE_PRIVATE_ELG2()
  aepk = DERIVE_PUBLIC(aesk)

  // Alice ephemeral public key
  // MixHash(aepk)
  // || below means append
  h = SHA256(h || aepk);

  // h is used as the associated data for the AEAD in the New Session Message
  // Retain the Hash h for the New Session Reply KDF
  // eapk is sent in cleartext in the
  // beginning of the New Session message
  elg2_aepk = ENCODE_ELG2(aepk)
  // As decoded by Bob
  aepk = DECODE_ELG2(elg2_aepk)

  End of "e" message pattern.

  This is the "es" message pattern:

  // Noise es
  sharedSecret = DH(aesk, bpk) = DH(bsk, aepk)

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // ChaChaPoly parameters to encrypt/decrypt
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  chainKey = keydata[0:31]

  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, flags/static key section, ad)

  End of "es" message pattern.

  This is the "s" message pattern:

  // MixHash(ciphertext)
  // Save for Payload section KDF
  h = SHA256(h || ciphertext)

  // Alice's X25519 static keys
  ask = GENERATE_PRIVATE()
  apk = DERIVE_PUBLIC(ask)

  End of "s" message pattern.


```
### 1f) 新会话消息的 KDF

```

This is the "ss" message pattern:

  // Noise ss
  sharedSecret = DH(ask, bpk) = DH(bsk, apk)

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // ChaChaPoly parameters to encrypt/decrypt
  // chainKey from Static Key Section
  Set sharedSecret = X25519 DH result
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  chainKey = keydata[0:31]

  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, payload, ad)

  End of "ss" message pattern.

  // MixHash(ciphertext)
  // Save for New Session Reply KDF
  h = SHA256(h || ciphertext)

```
### 初始 ChainKey 的 KDF

注意这是一个 Noise "N" 模式，但我们使用与绑定会话相同的 "IK" 初始化器。

新会话消息无法在静态密钥被解密和检查以确定其是否包含全零之前被识别为包含或不包含 Alice 的静态密钥。因此，接收方必须对所有新会话消息使用"IK"状态机。如果静态密钥全为零，则必须跳过"ss"消息模式。

```

chainKey = from Flags/Static key section
  k = from Flags/Static key section
  n = 1
  ad = h from Flags/Static key section
  ciphertext = ENCRYPT(k, n, payload, ad)

```
### 用于标志/静态密钥部分加密内容的 KDF

可以发送一个或多个新会话回复来响应单个新会话消息。每个回复都以一个标签作为前缀，该标签从会话的TagSet中生成。

新会话回复分为两个部分。第一部分是带有前置标签的 Noise IK 握手的完成。第一部分的长度为 56 字节。第二部分是数据阶段载荷。第二部分的长度为 16 + 载荷长度。

总长度为 72 + 载荷长度。加密格式：

```

+----+----+----+----+----+----+----+----+
  |       Session Tag   8 bytes           |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Ephemeral Public Key           +
  |                                       |
  +            32 bytes                   +
  |     Encoded with Elligator2           |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +  (MAC) for Key Section (no data)      +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |       ChaCha20 encrypted data         |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) for Payload Section     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  Tag :: 8 bytes, cleartext

  Public Key :: 32 bytes, little endian, Elligator2, cleartext

  MAC :: Poly1305 message authentication code, 16 bytes
         Note: The ChaCha20 plaintext data is empty (ZEROLEN)

  Payload Section encrypted data :: remaining data minus 16 bytes

  MAC :: Poly1305 message authentication code, 16 bytes

```
### 负载段的KDF（使用Alice静态密钥）

该标签在会话标签 KDF 中生成，如下面的 DH 初始化 KDF 中初始化的那样。这将回复与会话相关联。来自 DH 初始化的会话密钥不被使用。

### 负载部分的 KDF（不含 Alice 静态密钥）

Bob的临时密钥。临时密钥为32字节，使用Elligator2编码，小端序。此密钥永不重复使用；每条消息都会生成新密钥，包括重传消息。

### 1g) 新会话回复格式

加密长度是数据的剩余部分。解密长度比加密长度少16字节。载荷通常包含一个或多个Garlic Clove块。格式和其他要求请参见下方的载荷部分。

### Session Tag

从TagSet中创建一个或多个标签，TagSet使用下面的KDF进行初始化，使用来自New Session消息的chainKey。

```

// Generate tagset
  tagsetKey = HKDF(chainKey, ZEROLEN, "SessionReplyTags", 32)
  tagset_nsr = DH_INITIALIZE(chainKey, tagsetKey)

```
### 新会话回复临时密钥

```

// Keys from the New Session message
  // Alice's X25519 keys
  // apk and aepk are sent in original New Session message
  // ask = Alice private static key
  // apk = Alice public static key
  // aesk = Alice ephemeral private key
  // aepk = Alice ephemeral public key
  // Bob's X25519 static keys
  // bsk = Bob private static key
  // bpk = Bob public static key

  // Generate the tag
  tagsetEntry = tagset_nsr.GET_NEXT_ENTRY()
  tag = tagsetEntry.SESSION_TAG

  // MixHash(tag)
  h = SHA256(h || tag)

  This is the "e" message pattern:

  // Bob's X25519 ephemeral keys
  besk = GENERATE_PRIVATE_ELG2()
  bepk = DERIVE_PUBLIC(besk)

  // Bob's ephemeral public key
  // MixHash(bepk)
  // || below means append
  h = SHA256(h || bepk);

  // elg2_bepk is sent in cleartext in the
  // beginning of the New Session message
  elg2_bepk = ENCODE_ELG2(bepk)
  // As decoded by Bob
  bepk = DECODE_ELG2(elg2_bepk)

  End of "e" message pattern.

  This is the "ee" message pattern:

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // ChaChaPoly parameters to encrypt/decrypt
  // chainKey from original New Session Payload Section
  sharedSecret = DH(aesk, bepk) = DH(besk, aepk)
  keydata = HKDF(chainKey, sharedSecret, "", 32)
  chainKey = keydata[0:31]

  End of "ee" message pattern.

  This is the "se" message pattern:

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  sharedSecret = DH(ask, bepk) = DH(besk, apk)
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  chainKey = keydata[0:31]

  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, ZEROLEN, ad)

  End of "se" message pattern.

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)

  chainKey is used in the ratchet below.

```
### 载荷

这类似于分离后的第一个现有会话消息，但没有单独的标签。此外，我们使用上述哈希将负载绑定到 NSR 消息。

```

// split()
  keydata = HKDF(chainKey, ZEROLEN, "", 64)
  k_ab = keydata[0:31]
  k_ba = keydata[32:63]
  tagset_ab = DH_INITIALIZE(chainKey, k_ab)
  tagset_ba = DH_INITIALIZE(chainKey, k_ba)

  // AEAD parameters for New Session Reply payload
  k = HKDF(k_ba, ZEROLEN, "AttachPayloadKDF", 32)
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, payload, ad)
```
### Reply TagSet的KDF

可能会发送多个NSR消息作为回复，每个消息都带有唯一的临时密钥，这取决于响应的大小。

Alice 和 Bob 需要为每个 NS 和 NSR 消息使用新的临时密钥。

Alice 必须在发送现有会话（ES）消息之前接收到 Bob 的一条 NSR 消息，而 Bob 必须在发送 ES 消息之前接收到来自 Alice 的一条 ES 消息。

Bob's NSR Payload Section 中的 ``chainKey`` 和 ``k`` 被用作初始 ES DH Ratchets 的输入（双向，参见 DH Ratchet KDF）。

Bob必须仅保留从Alice接收到的ES消息的现有会话。任何其他创建的入站和出站会话（用于多个NSR）应在收到Alice针对给定会话的第一个ES消息后立即销毁。

### 回复密钥段加密内容的 KDF

Session tag（8 字节）加密数据和 MAC（见下面第 3 节）

### KDF for Payload Section Encrypted Contents（载荷部分加密内容的密钥派生函数）

加密的：

```

+----+----+----+----+----+----+----+----+
  |       Session Tag                     |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |       ChaCha20 encrypted data         |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +              (MAC)                    +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  Session Tag :: 8 bytes, cleartext

  Payload Section encrypted data :: remaining data minus 16 bytes

  MAC :: Poly1305 message authentication code, 16 bytes

```
### 注意事项

加密长度是数据的剩余部分。解密长度比加密长度少 16。有关格式和要求，请参见下面的负载部分。

KDF

```
See AEAD section below.

  // AEAD parameters for Existing Session payload
  k = The 32-byte session key associated with this session tag
  n = The message number N in the current chain, as retrieved from the associated Session Tag.
  ad = The session tag, 8 bytes
  ciphertext = ENCRYPT(k, n, payload, ad)
```
### 1h) 现有会话格式

格式：32字节公钥和私钥，小端序。

理由：用于 [NTCP2](/docs/specs/ntcp2/)。

### 格式

在标准 Noise 握手中，每个方向的初始握手消息都以明文传输的临时密钥开始。由于有效的 X25519 密钥可以与随机数据区分开来，中间人可能会将这些消息与以随机会话标签开始的现有会话消息区分开来。在 [NTCP2](/docs/specs/ntcp2/) ([提案 111](/proposals/111-ntcp-2/)) 中，我们使用了一个低开销的 XOR 函数，利用带外静态密钥来混淆密钥。然而，这里的威胁模型有所不同；我们不希望允许任何中间人使用任何手段来确认流量的目的地，或者将初始握手消息与现有会话消息区分开来。

因此，使用 [Elligator2](https://elligator.cr.yp.to/) 来转换 New Session 和 New Session Reply 消息中的临时密钥，使它们与均匀随机字符串无法区分。

### 载荷

32字节的公钥和私钥。编码的密钥采用小端序。

如[Elligator2](https://elligator.cr.yp.to/)中所定义，编码的密钥与254个随机比特无法区分。我们需要256个随机比特（32字节）。因此，编码和解码定义如下：

编码：

```

ENCODE_ELG2() Definition

  // Encode as defined in Elligator2 specification
  encodedKey = encode(pubkey)
  // OR in 2 random bits to MSB
  randomByte = CSRNG(1)
  encodedKey[31] |= (randomByte & 0xc0)
```
解码：

```

DECODE_ELG2() Definition

  // Mask out 2 random bits from MSB
  encodedKey[31] &= 0x3f
  // Decode as defined in Elligator2 specification
  pubkey = decode(encodedKey)
```
### 2) ECIES-X25519

需要防止 OBEP 和 IBGW 对流量进行分类。

### 2a) Elligator2

Elligator2 使密钥生成时间平均增加一倍，因为一半的私钥会产生不适合用 Elligator2 编码的公钥。同时，密钥生成时间是无界的且呈指数分布，因为生成器必须持续重试直到找到合适的密钥对。

这种开销可以通过在单独的线程中提前生成密钥来管理，以保持合适密钥的池。

生成器执行 ENCODE_ELG2() 函数来确定适用性。因此，生成器应该存储 ENCODE_ELG2() 的结果，这样就不必再次计算。

此外，不合适的密钥可能会被添加到用于 [NTCP2](/docs/specs/ntcp2/) 的密钥池中，其中不使用 Elligator2。这样做的安全问题待定。

### 格式

使用 ChaCha20 和 Poly1305 的 AEAD，与 [NTCP2](/docs/specs/ntcp2/) 中相同。这对应于 [RFC-7539](https://tools.ietf.org/html/rfc7539)，在 TLS [RFC-7905](https://tools.ietf.org/html/rfc7905) 中也有类似使用。

### 论证

新会话消息中 AEAD 块的加密/解密函数输入：

```

k :: 32 byte cipher key
       See New Session and New Session Reply KDFs above.

  n :: Counter-based nonce, 12 bytes.
       n = 0

  ad :: Associated data, 32 bytes.
        The SHA256 hash of the preceding data, as output from mixHash()

  data :: Plaintext data, 0 or more bytes

```
### 注意事项

现有会话消息中 AEAD 块的加密/解密函数输入：

```

k :: 32 byte session key
       As looked up from the accompanying session tag.

  n :: Counter-based nonce, 12 bytes.
       Starts at 0 and incremented for each message when transmitting.
       For the receiver, the value
       as looked up from the accompanying session tag.
       First four bytes are always zero.
       Last eight bytes are the message number (n), little-endian encoded.
       Maximum value is 65535.
       Session must be ratcheted when N reaches that value.
       Higher values must never be used.

  ad :: Associated data
        The session tag

  data :: Plaintext data, 0 or more bytes

```
### 3) AEAD (ChaChaPoly)

加密函数的输出，解密函数的输入：

```

+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |       ChaCha20 encrypted data         |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +              (MAC)                    +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  encrypted data :: Same size as plaintext data, 0 - 65519 bytes

  MAC :: Poly1305 message authentication code, 16 bytes

```
### 新会话和新会话回复输入

- 由于 ChaCha20 是流密码，明文无需填充。
  多余的密钥流字节将被丢弃。

- 密码的密钥（256位）通过SHA256 KDF协商确定。
  每个消息的KDF详细信息在下面的单独章节中说明。

- ChaChaPoly 帧具有已知大小，因为它们被封装在 I2NP 数据消息中。

- 对于所有消息，
  填充位于已认证的
  数据帧内部。

### 现有会话输入

所有未通过 AEAD 验证的接收数据必须被丢弃。不返回任何响应。

### 加密格式

在 [NTCP2](/docs/specs/ntcp2/) 中使用。

### 说明

我们仍然像以前一样使用 session tags，但我们使用 ratchets 来生成它们。Session tags 也有一个我们从未实现的重新密钥选项。所以这就像一个双 ratchet，但我们从未做第二个。

这里我们定义了类似于 Signal 的 Double Ratchet 的机制。会话标签在接收方和发送方都以确定性和相同的方式生成。

通过使用对称密钥/标签棘轮机制，我们消除了发送方存储会话标签的内存使用。我们还消除了发送标签集的带宽消耗。接收方的使用量仍然很大，但我们可以进一步减少它，因为我们将把会话标签从32字节缩小到8字节。

我们不使用 Signal 中指定的（可选的）报头加密，而是使用会话标签。

通过使用 DH ratchet，我们实现了前向安全性，这在 ElGamal/AES+SessionTags 中从未实现过。

注意：New Session 一次性公钥不是 ratchet 的一部分，它的唯一功能是加密 Alice 的初始 DH ratchet 密钥。

### AEAD 错误处理

Double Ratchet通过在每个消息头中包含一个标签来处理丢失或乱序的消息。接收方查找标签的索引，这就是消息编号N。如果消息包含带有PN值的消息编号块，接收方可以删除前一个标签集中高于该值的任何标签，同时保留前一个标签集中被跳过的标签，以防跳过的消息稍后到达。

### 理由

我们定义以下数据结构和函数来实现这些棘轮机制。

TAGSET_ENTRY

    A single entry in a TAGSET.

    INDEX
        An integer index, starting with 0

    SESSION_TAG
        An identifier to go out on the wire, 8 bytes

    SESSION_KEY
        A symmetric key, never goes on the wire, 32 bytes

TAGSET

    A collection of TAGSET_ENTRIES.

    CREATE(key, n)
        Generate a new TAGSET using initial cryptographic key material of 32 bytes.
        The associated session identifier is provided.
        The initial number of of tags to create is specified; this is generally 0 or 1
        for an outgoing session.
        LAST_INDEX = -1
        EXTEND(n) is called.

    EXTEND(n)
        Generate n more TAGSET_ENTRIES by calling EXTEND() n times.

    EXTEND()
        Generate one more TAGSET_ENTRY, unless the maximum number SESSION_TAGS have
        already been generated.
        If LAST_INDEX is greater than or equal to 65535, return.
        ++ LAST_INDEX
        Create a new TAGSET_ENTRY with the LAST_INDEX value and the calculated SESSION_TAG.
        Calls RATCHET_TAG() and (optionally) RATCHET_KEY().
        For inbound sessions, the calculation of the SESSION_KEY may
        be deferred and calculated in GET_SESSION_KEY().
        Calls EXPIRE()

    EXPIRE()
        Remove tags and keys that are too old, or if the TAGSET size exceeds some limit.

    RATCHET_TAG()
        Calculates the next SESSION_TAG based on the last SESSION_TAG.

    RATCHET_KEY()
        Calculates the next SESSION_KEY based on the last SESSION_KEY.

    SESSION
        The associated session.

    CREATION_TIME
        When the TAGSET was created.

    LAST_INDEX
        The last TAGSET_ENTRY INDEX generated by EXTEND().

    GET_NEXT_ENTRY()
        Used for outgoing sessions only.
        EXTEND(1) is called if there are no remaining TAGSET_ENTRIES.
        If EXTEND(1) did nothing, the max of 65535 TAGSETS have been used,
        and return an error.
        Returns the next unused TAGSET_ENTRY.

    GET_SESSION_KEY(sessionTag)
        Used for incoming sessions only.
        Returns the TAGSET_ENTRY containing the sessionTag.
        If found, the TAGSET_ENTRY is removed.
        If the SESSION_KEY calculation was deferred, it is calculated now.
        If there are few TAGSET_ENTRIES remaining, EXTEND(n) is called.


### 4) 棘轮机制

棘轮机制，但速度远不如 Signal。我们将接收密钥的确认与生成新密钥分开处理。在典型使用中，Alice 和 Bob 在新会话中会立即各自棘轮（两次），但之后不会再次棘轮。

注意，ratchet 是单向的，为该方向生成新的会话标签/消息密钥 ratchet 链。要为两个方向生成密钥，您必须执行两次 ratchet。

每次生成并发送新密钥时，你都会执行 ratchet 操作。每次接收到新密钥时，你也会执行 ratchet 操作。

Alice在创建未绑定的出站会话时会执行一次ratchet操作，她不会创建入站会话（未绑定是不可回复的）。

Bob 在创建未绑定入站会话时执行一次棘轮操作，并且不创建相应的出站会话（未绑定是不可回复的）。

Alice继续向Bob发送New Session (NS)消息，直到收到Bob的New Session Reply (NSR)消息之一。然后她将NSR的载荷部分KDF结果作为会话棘轮的输入（参见DH Ratchet KDF），并开始发送Existing Session (ES)消息。

对于收到的每个 NS 消息，Bob 创建一个新的入站会话，使用回复载荷部分的 KDF 结果作为新入站和出站 ES DH Ratchet 的输入。

对于所需的每个回复，Bob 向 Alice 发送一个包含回复内容的 NSR 消息。要求 Bob 为每个 NSR 使用新的临时密钥。

Bob 必须在相应的出站会话上创建和发送 ES 消息之前，先在其中一个入站会话上收到来自 Alice 的 ES 消息。

Alice 应该使用计时器来接收来自 Bob 的 NSR 消息。如果计时器超时，应该移除该会话。

为了避免 KCI 和/或资源耗尽攻击（攻击者丢弃 Bob 的 NSR 回复以保持 Alice 发送 NS 消息），Alice 应该在由于计时器过期导致重试达到一定次数后，避免向 Bob 启动新会话。

Alice和Bob在收到每个NextKey块时都会执行DH棘轮。

Alice 和 Bob 在每次 DH ratchet 之后都会生成新的标签集 ratchets 和两个对称密钥 ratchets。对于给定方向上的每个新的 ES 消息，Alice 和 Bob 会推进会话标签和对称密钥 ratchets。

初始握手后 DH ratchets 的频率取决于具体实现。虽然协议规定在需要进行 ratchet 之前最多可以发送 65535 条消息，但更频繁的 ratcheting（基于消息数量、经过时间或两者）可能提供额外的安全性。

在绑定会话的最终握手 KDF 之后，Bob 和 Alice 必须在生成的 CipherState 上运行 Noise Split() 函数，为入站和出站会话创建独立的对称密钥和标签链密钥。

#### KEY AND TAG SET IDS

密钥和标签集ID号用于识别密钥和标签集。密钥ID在NextKey块中用于识别发送或使用的密钥。标签集ID（与消息编号一起）在ACK块中用于识别被确认的消息。密钥和标签集ID都适用于单一方向的标签集。密钥和标签集ID号必须是连续的。

在每个方向的会话中使用的第一个标签集中，标签集 ID 为 0。尚未发送 NextKey 块，因此没有密钥 ID。

要开始 DH ratchet，发送方传输一个密钥 ID 为 0 的新 NextKey 块。接收方回复一个密钥 ID 为 0 的新 NextKey 块。然后发送方开始使用标签集 ID 为 1 的新标签集。

后续的标签集以类似的方式生成。对于在NextKey交换之后使用的所有标签集，标签集编号为（1 + Alice的密钥ID + Bob的密钥ID）。

密钥和标签集ID从0开始，依次递增。标签集ID的最大值是65535。密钥ID的最大值是32767。当标签集几乎耗尽时，标签集发送方必须发起NextKey交换。当标签集65535几乎耗尽时，标签集发送方必须通过发送New Session消息来发起新会话。

在流式传输最大消息大小为1730的情况下，假设没有重传，使用单个标签集的理论最大数据传输量为1730 * 65536 ~= 108 MB。由于重传的存在，实际最大值会更低。

在会话必须被丢弃和替换之前，使用所有65536个可用标签集的理论最大数据传输量为64K * 108 MB ~= 6.9 TB。

#### DH RATCHET MESSAGE FLOW

标签集的下一次密钥交换必须由这些标签的发送方（出站标签集的所有者）发起。接收方（入站标签集的所有者）将响应。对于应用层的典型HTTP GET流量，Bob将发送更多消息并通过发起密钥交换来首先进行棘轮操作；下图显示了这一点。当Alice进行棘轮操作时，同样的过程会反向发生。

NS/NSR握手后使用的第一个标签集是标签集0。当标签集0几乎耗尽时，必须在两个方向上交换新密钥以创建标签集1。之后，新密钥只在一个方向上发送。

为了创建标签集2，标签发送方发送一个新密钥，标签接收方发送其旧密钥的ID作为确认。双方都执行DH。

要创建标签集3，标签发送方发送其旧密钥的ID并从标签接收方请求新密钥。双方都执行DH。

后续的标签集生成方式与标签集 2 和 3 相同。标签集编号为 (1 + 发送方密钥 ID + 接收方密钥 ID)。

```

Tag Sender                    Tag Receiver

                   ... use tag set #0 ...


  (Tagset #0 almost empty)
  (generate new key #0)

  Next Key, forward, request reverse, with key #0  -------->
  (repeat until next key received)

                              (generate new key #0, do DH, create IB Tagset #1)

          <-------------      Next Key, reverse, with key #0
                              (repeat until tag received on new tagset)

  (do DH, create OB Tagset #1)


                   ... use tag set #1 ...


  (Tagset #1 almost empty)
  (generate new key #1)

  Next Key, forward, with key #1        -------->
  (repeat until next key received)

                              (reuse key #0, do DH, create IB Tagset #2)

          <--------------     Next Key, reverse, id 0
                              (repeat until tag received on new tagset)

  (do DH, create OB Tagset #2)


                   ... use tag set #2 ...


  (Tagset #2 almost empty)
  (reuse key #1)

  Next Key, forward, request reverse, id 1  -------->
  (repeat until next key received)

                              (generate new key #1, do DH, create IB Tagset #3)

          <--------------     Next Key, reverse, with key #1

  (do DH, create OB Tagset #3)
  (reuse key #1, do DH, create IB Tagset #3)


                   ... use tag set #3 ...


       After tag set 3, repeat the above
       patterns as shown for tag sets 2 and 3.

       To create a new even-numbered tag set, the sender sends a new key
       to the receiver. The receiver sends his old key ID
       back as an acknowledgement.

       To create a new odd-numbered tag set, the sender sends a reverse request
       to the receiver. The receiver sends a new reverse key to the sender.

```
当出站标签集的DH ratchet完成后，创建新的出站标签集时，应立即使用新标签集，旧的出站标签集可以被删除。

当入站tagset的DH棘轮完成后，创建新的入站tagset时，接收方应该监听两个tagset中的标签，并在短时间后（约3分钟）删除旧的tagset。

标签集和密钥 ID 进展的摘要见下表。* 表示生成了新密钥。

| New Tag Set ID | Sender key ID | Rcvr key ID |
|----------------|---------------|-------------|
| 0              | n/a           | n/a         |
| 1              | 0 *           | 0 *         |
| 2              | 1 *           | 0           |
| 3              | 1             | 1 *         |
| 4              | 2 *           | 1           |
| 5              | 2             | 2 *         |
| ...            | ...           | ...         |
| 65534          | 32767 *       | 32766       |
| 65535          | 32767         | 32767 *     |
密钥和标签集ID号码必须是连续的。

#### DH INITIALIZATION KDF

这是单方向 DH_INITIALIZE(rootKey, k) 的定义。它创建一个标签集，以及一个"下一个根密钥"，在必要时用于后续的 DH 棘轮。

我们在三个地方使用DH初始化。首先，我们用它为New Session Replies生成标签集。其次，我们用它生成两个标签集，每个方向一个，用于Existing Session消息。最后，我们在DH Ratchet之后使用它，为额外的Existing Session消息在单个方向生成新的标签集。

```

Inputs:
  1) rootKey = chainKey from Payload Section
  2) k from the New Session KDF or split()

  // KDF_RK(rk, dh_out)
  keydata = HKDF(rootKey, k, "KDFDHRatchetStep", 64)

  // Output 1: The next Root Key (KDF input for the next DH ratchet)
  nextRootKey = keydata[0:31]
  // Output 2: The chain key to initialize the new
  // session tag and symmetric key ratchets
  // for the tag set
  ck = keydata[32:63]

  // session tag and symmetric key chain keys
  keydata = HKDF(ck, ZEROLEN, "TagAndKeyGenKeys", 64)
  sessTag_ck = keydata[0:31]
  symmKey_ck = keydata[32:63]

```
#### DH RATCHET KDF

这在 NextKey 块中交换新的 DH 密钥后使用，在标签集耗尽之前。

```


// Tag sender generates new X25519 ephemeral keys
  // and sends rapk to tag receiver in a NextKey block
  rask = GENERATE_PRIVATE()
  rapk = DERIVE_PUBLIC(rask)
  
  // Tag receiver generates new X25519 ephemeral keys
  // and sends rbpk to Tag sender in a NextKey block
  rbsk = GENERATE_PRIVATE()
  rbpk = DERIVE_PUBLIC(rbsk)

  sharedSecret = DH(rask, rbpk) = DH(rbsk, rapk)
  tagsetKey = HKDF(sharedSecret, ZEROLEN, "XDHRatchetTagSet", 32)
  rootKey = nextRootKey // from previous tagset in this direction
  newTagSet = DH_INITIALIZE(rootKey, tagsetKey)

```
### 消息编号

每条消息都有棘轮机制，如同 Signal 中一样。会话标签棘轮与对称密钥棘轮同步，但接收方密钥棘轮可能"滞后"以节省内存。

发送方对每个传输的消息进行一次棘轮操作。无需存储额外的标签。发送方还必须保持一个计数器来记录 'N'，即当前链中消息的消息编号。'N' 值包含在发送的消息中。请参见消息编号块定义。

接收方必须按最大窗口大小向前棘轮并将标签存储在与会话关联的"标签集"中。一旦接收到，存储的标签可能会被丢弃，如果没有之前未接收的标签，窗口可能会前进。接收方应该保持与每个会话标签关联的'N'值，并检查发送消息中的数字是否与此值匹配。请参阅消息编号块定义。

#### KDF

这是 RATCHET_TAG() 的定义。

```

Inputs:
  1) Session Tag Chain key sessTag_ck
     First time: output from DH ratchet
     Subsequent times: output from previous session tag ratchet

  Generated:
  2) input_key_material = SESSTAG_CONSTANT
     Must be unique for this tag set (generated from chain key),
     so that the sequence isn't predictable, since session tags
     go out on the wire in plaintext.

  Outputs:
  1) N (the current session tag number)
  2) the session tag (and symmetric key, probably)
  3) the next Session Tag Chain Key (KDF input for the next session tag ratchet)

  Initialization:
  keydata = HKDF(sessTag_ck, ZEROLEN, "STInitialization", 64)
  // Output 1: Next chain key
  sessTag_chainKey = keydata[0:31]
  // Output 2: The constant
  SESSTAG_CONSTANT = keydata[32:63]

  // KDF_ST(ck, constant)
  keydata_0 = HKDF(sessTag_chainkey, SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
  // Output 1: Next chain key
  sessTag_chainKey_0 = keydata_0[0:31]
  // Output 2: The session tag
  // or more if tag is longer than 8 bytes
  tag_0 = keydata_0[32:39]

  // repeat as necessary to get to tag_n
  keydata_n = HKDF(sessTag_chainKey_(n-1), SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
  // Output 1: Next chain key
  sessTag_chainKey_n = keydata_n[0:31]
  // Output 2: The session tag
  // or more if tag is longer than 8 bytes
  tag_n = keydata_n[32:39]

```
### 示例实现

每条消息都使用棘轮机制，如同 Signal 中的实现。每个对称密钥都有一个关联的消息号码和会话标签。会话密钥棘轮与对称标签棘轮同步，但接收方密钥棘轮可能会"滞后"以节省内存。

发送方每发送一条消息就进行一次棘轮操作。无需存储额外的密钥。

当接收方获得session tag时，如果它尚未将对称密钥ratchet提前到关联密钥，它必须"追赶"到关联密钥。接收方可能会缓存尚未接收到的任何先前tag的密钥。一旦接收到，存储的密钥可能会被丢弃，如果没有先前未接收的tag，窗口可能会向前推进。

为了提高效率，会话标签和对称密钥棘轮是分离的，这样会话标签棘轮可以领先于对称密钥棘轮运行。这也提供了一些额外的安全性，因为会话标签会在网络上传输。

#### KDF

这是 RATCHET_KEY() 的定义。

```

Inputs:
  1) Symmetric Key Chain key symmKey_ck
     First time: output from DH ratchet
     Subsequent times: output from previous symmetric key ratchet

  Generated:
  2) input_key_material = SYMMKEY_CONSTANT = ZEROLEN
     No need for uniqueness. Symmetric keys never go out on the wire.
     TODO: Set a constant anyway?

  Outputs:
  1) N (the current session key number)
  2) the session key
  3) the next Symmetric Key Chain Key (KDF input for the next symmetric key ratchet)

  // KDF_CK(ck, constant)
  SYMMKEY_CONSTANT = ZEROLEN
  // Output 1: Next chain key
  keydata_0 = HKDF(symmKey_ck, SYMMKEY_CONSTANT, "SymmetricRatchet", 64)
  symmKey_chainKey_0 = keydata_0[0:31]
  // Output 2: The symmetric key
  k_0 = keydata_0[32:63]

  // repeat as necessary to get to k[n]
  keydata_n = HKDF(symmKey_chainKey_(n-1), SYMMKEY_CONSTANT, "SymmetricRatchet", 64)
  // Output 1: Next chain key
  symmKey_chainKey_n = keydata_n[0:31]
  // Output 2: The symmetric key
  k_n = keydata_n[32:63]


```
### 4a) DH Ratchet（DH 棘轮）

这替代了 ElGamal/AES+SessionTags 规范中定义的 AES 部分格式。

这使用与 [NTCP2](/docs/specs/ntcp2/) 规范中定义的相同块格式。各个块类型的定义有所不同。

有人担心鼓励实现者共享代码可能导致解析问题。实现者应该仔细考虑共享代码的利弊，并确保两种上下文的排序和有效区块规则是不同的。

### Payload Section Decrypted data

加密长度是数据的剩余部分。解密长度比加密长度少16字节。支持所有块类型。典型内容包括以下块：

| Payload Block Type | Type Number | Block Length |
|--------------------|-------------|--------------|
| DateTime           | 0           | 7            |
| Termination (TBD)  | 4           | 9 typ.       |
| Options (TBD)      | 5           | 21+          |
| Message Number (TBD) | 6           | TBD          |
| Next Key           | 7           | 3 or 35      |
| ACK                | 8           | 4 typ.       |
| ACK Request        | 9           | 3            |
| Garlic Clove       | 11          | varies       |
| Padding            | 254         | varies       |
### Unencrypted data

加密帧中包含零个或多个块。每个块包含一个单字节标识符、一个双字节长度和零个或多个数据字节。

为了可扩展性，接收方必须忽略具有未知类型编号的块，并将它们视为填充。

加密数据最大为 65535 字节，包括 16 字节的身份验证头，因此未加密数据的最大长度为 65519 字节。

（未显示 Poly1305 认证标签）：

```

+----+----+----+----+----+----+----+----+
  |blk |  size   |       data             |
  +----+----+----+                        +
  |                                       |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |blk |  size   |       data             |
  +----+----+----+                        +
  |                                       |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  ~               .   .   .               ~

  blk :: 1 byte
         0 datetime
         1-3 reserved
         4 termination
         5 options
         6 previous message number
         7 next session key
         8 ack
         9 ack request
         10 reserved
         11 Garlic Clove
         224-253 reserved for experimental features
         254 for padding
         255 reserved for future extension
  size :: 2 bytes, big endian, size of data to follow, 0 - 65516
  data :: the data

  Maximum ChaChaPoly frame is 65535 bytes.
  Poly1305 tag is 16 bytes
  Maximum total block size is 65519 bytes
  Maximum single block size is 65519 bytes
  Block type is 1 byte
  Block length is 2 bytes
  Maximum single block data size is 65516 bytes.

```
### Block Ordering Rules

在新会话消息中，DateTime 块是必需的，并且必须是第一个块。

其他允许的区块：

- Garlic Clove (类型 11)
- Options (类型 5)
- Padding (类型 254)

在新会话回复消息中，不需要任何块。

其他允许的块：

- Garlic Clove (类型 11)
- Options (类型 5)
- Padding (类型 254)

不允许其他块。填充（如果存在）必须是最后一个块。

在现有会话消息中，不需要任何块，且顺序不做规定，除了以下要求：

终止块（如果存在）必须是除填充块之外的最后一个块。填充块（如果存在）必须是最后一个块。

单个帧中可能包含多个 Garlic Clove 块。单个帧中最多可以包含两个 Next Key 块。单个帧中不允许包含多个 Padding 块。其他块类型在单个帧中可能不会有多个块，但这并不被禁止。

### DateTime

一个过期时间。有助于防止重放。Bob必须使用此时间戳验证消息是否为最新的。如果时间有效，Bob必须实现布隆过滤器或其他机制来防止重放攻击。通常仅包含在New Session消息中。

```

+----+----+----+----+----+----+----+
  | 0  |    4    |     timestamp     |
  +----+----+----+----+----+----+----+

  blk :: 0
  size :: 2 bytes, big endian, value = 4
  timestamp :: Unix timestamp, unsigned seconds.
               Wraps around in 2106

```
### 4b) Session Tag Ratchet（会话标签棘轮）

单个解密的 Garlic Clove，如 [I2NP](/docs/specs/i2np/) 中所规定，但删除了未使用或冗余的字段。警告：此格式与 ElGamal/AES 格式显著不同。每个 clove 都是一个单独的载荷块。Garlic Clove 不能跨块或跨 ChaChaPoly 帧进行分片。

```

+----+----+----+----+----+----+----+----+
  | 11 |  size   |                        |
  +----+----+----+                        +
  |      Delivery Instructions            |
  ~                                       ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |type|  Message_ID       | Expiration   
  +----+----+----+----+----+----+----+----+
       |      I2NP Message body           |
  +----+                                  +
  ~                                       ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  size :: size of all data to follow

  Delivery Instructions :: As specified in
         the Garlic Clove section of [I2NP](/docs/specs/i2np/).
         Length varies but is typically 1, 33, or 37 bytes

  type :: I2NP message type

  Message_ID :: 4 byte `Integer` I2NP message ID

  Expiration :: 4 bytes, seconds since the epoch

```
注意事项：

- 实现者必须确保在读取块时，
  格式错误或恶意数据不会导致读取操作
  越界到下一个块中。

- [I2NP](/docs/specs/i2np/) 中指定的 Clove Set 格式未被使用。
  每个 clove 都包含在自己的块中。

- I2NP 消息头为 9 字节，格式与 [NTCP2](/docs/specs/ntcp2/) 中使用的格式相同。

- 来自 [I2NP](/docs/specs/i2np/) 中 Garlic Message 定义的 Certificate、Message ID 和 Expiration 不包括在内。

- Certificate、Clove ID 和 Expiration 来自 [I2NP](/docs/specs/i2np/) 中的
  Garlic Clove 定义，但不包含在内。

理由：

- 这些证书从未被使用过。
- 独立的消息 ID 和 clove ID 从未被使用过。
- 独立的过期时间从未被使用过。
- 与旧的 Clove Set 和 Clove 格式相比，总体节省空间约为：1 个 clove 节省 35 字节，2 个 clove 节省 54 字节，3 个 clove 节省 73 字节。
- 该区块格式具有可扩展性，任何新字段都可以作为新的区块类型添加。

### Termination

实现是可选的。丢弃 session。这必须是帧中最后一个非填充块。在此 session 中将不再发送更多消息。

不允许在 NS 或 NSR 中使用。仅包含在现有会话消息中。

```

+----+----+----+----+----+----+----+----+
  | 4  |  size   | rsn|     addl data     |
  +----+----+----+----+                   +
  ~               .   .   .               ~
  +----+----+----+----+----+----+----+----+

  blk :: 4
  size :: 2 bytes, big endian, value = 1 or more
  rsn :: reason, 1 byte:
         0: normal close or unspecified
         1: termination received
         others: optional, impementation-specific
  addl data :: optional, 0 or more bytes, for future expansion, debugging,
               or reason text.
               Format unspecified and may vary based on reason code.

```
### 4c) 对称密钥棘轮

未实现，有待进一步研究。传递更新的选项。选项包括会话的各种参数。更多信息请参见下面的会话标签长度分析部分。

options 块的长度可能是可变的，因为可能存在 more_options。

```

+----+----+----+----+----+----+----+----+
  | 5  |  size   |ver |flg |STL |STimeout |
  +----+----+----+----+----+----+----+----+
  |  SOTW   |  RITW   |tmin|tmax|rmin|rmax|
  +----+----+----+----+----+----+----+----+
  |  tdmy   |  rdmy   |  tdelay |  rdelay |
  +----+----+----+----+----+----+----+----+
  |              more_options             |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  blk :: 5
  size :: 2 bytes, big endian, size of options to follow, 21 bytes minimum
  ver :: Protocol version, must be 0
  flg :: 1 byte flags
         bits 7-0: Unused, set to 0 for future compatibility
  STL :: Session tag length (must be 8), other values unimplemented
  STimeout :: Session idle timeout (seconds), big endian
  SOTW :: Sender Outbound Tag Window, 2 bytes big endian
  RITW :: Receiver Inbound Tag Window 2 bytes big endian

  tmin, tmax, rmin, rmax :: requested padding limits
      tmin and rmin are for desired resistance to traffic analysis.
      tmax and rmax are for bandwidth limits.
      tmin and tmax are the transmit limits for the router sending this options block.
      rmin and rmax are the receive limits for the router sending this options block.
      Each is a 4.4 fixed-point float representing 0 to 15.9375
      (or think of it as an unsigned 8-bit integer divided by 16.0).
      This is the ratio of padding to data. Examples:
      Value of 0x00 means no padding
      Value of 0x01 means add 6 percent padding
      Value of 0x10 means add 100 percent padding
      Value of 0x80 means add 800 percent (8x) padding
      Alice and Bob will negotiate the minimum and maximum in each direction.
      These are guidelines, there is no enforcement.
      Sender should honor receiver's maximum.
      Sender may or may not honor receiver's minimum, within bandwidth constraints.

  tdmy: Max dummy traffic willing to send, 2 bytes big endian, bytes/sec average
  rdmy: Requested dummy traffic, 2 bytes big endian, bytes/sec average
  tdelay: Max intra-message delay willing to insert, 2 bytes big endian, msec average
  rdelay: Requested intra-message delay, 2 bytes big endian, msec average

  more_options :: Format undefined, for future use

```
SOTW 是发送方向接收方推荐的接收方入站标签窗口（最大前瞻值）。RITW 是发送方声明的入站标签窗口（最大前瞻值），即他计划使用的值。然后双方基于某些最小值、最大值或其他计算来设置或调整前瞻值。

注意事项：

- 希望永远不需要支持非默认会话标签长度。
- 标签窗口是 Signal 文档中的 MAX_SKIP。

问题：

- 选项协商待定。
- 默认值待定。
- 填充和延迟选项从 NTCP2 复制而来，
  但这些选项在那里尚未完全实现或研究。

### Message Numbers

实现是可选的。前一个标签集中的长度（发送的消息数量）(PN)。接收方可以立即删除前一个标签集中高于 PN 的标签。接收方可以在短时间内（例如 2 分钟）使前一个标签集中小于或等于 PN 的标签过期。

```

+----+----+----+----+----+
  | 6  |  size   |  PN    |
 +----+----+----+----+----+

  blk :: 6
  size :: 2
  PN :: 2 bytes big endian. The index of the last tag sent in the previous tag set.

```
注意事项：

- 最大 PN 为 65535。
- PN 的定义等于 Signal 的定义减一。
  这与 Signal 的做法类似，但在 Signal 中，PN 和 N 在头部。
  在这里，它们在加密的消息体中。
- 不要在标签集 0 中发送此块，因为没有前一个标签集。

### 5) 负载

下一个 DH ratchet 密钥在负载中，它是可选的。我们不会每次都进行 ratchet。（这与 signal 不同，在 signal 中它位于头部，并且每次都会发送）

对于第一个棘轮，Key ID = 0。

不允许在 NS 或 NSR 中使用。仅包含在现有会话消息中。

```

+----+----+----+----+----+----+----+----+
  | 7  |  size   |flag|  key ID |         |
  +----+----+----+----+----+----+         +
  |                                       |
  +                                       +
  |     Next DH Ratchet Public Key        |
  +                                       +
  |                                       |
  +                             +----+----+
  |                             |
  +----+----+----+----+----+----+

  blk :: 7
  size :: 3 or 35
  flag :: 1 byte flags
          bit order: 76543210
          bit 0: 1 for key present, 0 for no key present
          bit 1: 1 for reverse key, 0 for forward key
          bit 2: 1 to request reverse key, 0 for no request
                 only set if bit 1 is 0
          bits 7-2: Unused, set to 0 for future compatibility
  key ID :: The key ID of this key. 2 bytes, big endian
            0 - 32767
  Public Key :: The next X25519 public key, 32 bytes, little endian
                Only if bit 0 is 1


```
注意事项：

- Key ID 是用于该标签集的本地密钥的递增计数器，从 0 开始。
- 除非密钥更改，否则 ID 不得更改。
- 虽然可能不是严格必需的，但它对调试很有用。
  Signal 不使用 key ID。
- 最大 Key ID 为 32767。
- 在双向标签集同时进行棘轮操作的罕见情况下，一个帧将包含两个 Next Key 块，一个用于前向密钥，一个用于反向密钥。
- 密钥和标签集 ID 号必须是连续的。
- 详情请参见上面的 DH Ratchet 部分。

### Payload Section 已解密数据

这仅在收到 ack 请求块时发送。可能存在多个 ack 来确认多条消息。

在 NS 或 NSR 中不允许。仅包含在现有会话消息中。

```
+----+----+----+----+----+----+----+----+
  | 8  |  size   |tagsetid |   N     |    |
  +----+----+----+----+----+----+----+    +
  |             more acks                 |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  blk :: 8
  size :: 4 * number of acks to follow, minimum 1 ack
  for each ack:
  tagsetid :: 2 bytes, big endian, from the message being acked
  N :: 2 bytes, big endian, from the message being acked


```
注意事项：

- 标签集 ID 和 N 唯一标识被确认的消息。
- 在每个方向的会话中使用的第一个标签集中，标签集 ID 为 0。
- 没有发送 NextKey 块，因此没有密钥 ID。
- 对于 NextKey 交换后使用的所有标签集，标签集编号为 (1 + Alice 的密钥 ID + Bob 的密钥 ID)。

### 未加密数据

请求带内确认。用于替换 Garlic Clove 中的带外 DeliveryStatus 消息。

如果请求显式确认，则当前 tagset ID 和消息编号 (N) 会在 ack 块中返回。

不允许在 NS 或 NSR 中使用。仅包含在现有会话消息中。

```

+----+----+----+----+
  |  9 |  size   |flg |
  +----+----+----+----+

  blk :: 9
  size :: 1
  flg :: 1 byte flags
         bits 7-0: Unused, set to 0 for future compatibility

```
### 区块排序规则

所有填充都在AEAD帧内。TODO AEAD内的填充应大致遵循协商的参数。TODO Alice在NS消息中发送了她请求的tx/rx最小/最大参数。TODO Bob在NSR消息中发送了他请求的tx/rx最小/最大参数。更新的选项可能在数据阶段发送。请参阅上面的选项块信息。

如果存在，这必须是帧中的最后一个块。

```

+----+----+----+----+----+----+----+----+
  |254 |  size   |      padding           |
  +----+----+----+                        +
  |                                       |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  blk :: 254
  size :: 2 bytes, big endian, 0-65516
  padding :: zeros or random data

```
注意事项：

- 全零填充是可以的，因为它会被加密。
- 填充策略待定。
- 允许仅填充帧。
- 填充默认为0-15字节。
- 参见选项块中的填充参数协商
- 参见选项块中的最小/最大填充参数
- Router对违反协商填充的响应取决于具体实现。

### 日期时间

实现应忽略未知的块类型以保持向前兼容性。

### Garlic Clove（大蒜瓣）

- 填充长度应该根据每条消息的具体情况和长度分布的估计来决定，或者应该添加随机延迟。这些对策旨在抵抗 DPI，因为消息大小会暴露传输协议正在承载 I2P 流量。确切的填充方案是未来工作的一个领域，附录 A 提供了有关该主题的更多信息。

## Typical Usage Patterns

### 终止

这是最典型的用例，大多数非HTTP流式传输用例也与此用例相同。发送一个小的初始消息，然后收到回复，接着在两个方向上发送额外的消息。

HTTP GET 通常可以放入单个 I2NP 消息中。Alice 发送一个小请求，包含单个新的 Session 消息，捆绑一个回复 leaseset。Alice 包含立即 ratchet 到新密钥。包含签名以绑定到目标。不请求确认。

Bob 立即进行棘轮操作。

Alice 立即进行棘轮操作。

继续使用这些会话。

```

Alice                           Bob

  New Session (1b)     ------------------->
  with ephemeral key 1
  with static key for binding
  with next key
  with bundled HTTP GET
  with bundled LS
  without bundled Delivery Status Message

  any retransmissions, same as above

  following messages may arrive in any order:

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 1
                      with bundled HTTP reply part 1

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 2
                      with bundled HTTP reply part 2

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 3
                      with bundled HTTP reply part 3

  After reception of any of these messages,
  Alice switches to use Existing Session messages,
  creates a new inbound + outbound session pair,
  and ratchets.


  Existing Session     ------------------->
  with bundled streaming ack


  Existing Session     ------------------->
  with bundled streaming ack


  After reception of any of these messages,
  Bob switches to use Existing Session messages.


  <--------------     Existing Session
                      with bundled HTTP reply part 4


  Existing Session     ------------------->
  with bundled streaming ack

  <--------------     Existing Session
                      with bundled HTTP reply part 5

```
### 选项

Alice有三个选项：

1) 仅发送第一条消息（窗口大小 = 1），如 HTTP GET 中所示。不推荐使用。

2) 发送至流窗口，但使用相同的 Elligator2 编码明文公钥。所有消息包含相同的下一个公钥（棘轮）。这对 OBGW/IBEP 是可见的，因为它们都以相同的明文开始。处理过程与 1) 中相同。不推荐使用。

3) 推荐的实现方式。发送到流窗口上限，但每个消息使用不同的 Elligator2 编码明文公钥（会话）。所有消息都包含相同的下一个公钥（ratchet）。这对 OBGW/IBEP 来说是不可见的，因为它们都以不同的明文开始。Bob 必须识别出它们都包含相同的下一个公钥，并用相同的 ratchet 响应所有消息。Alice 使用那个下一个公钥并继续。

选项 3 消息流：

```

Alice                           Bob

  New Session (1b)     ------------------->
  with ephemeral key 1
  with static key for binding
  with bundled HTTP POST part 1
  with bundled LS
  without bundled Delivery Status Message


  New Session (1b)     ------------------->
  with ephemeral key 2
  with static key for binding
  with bundled HTTP POST part 2
  with bundled LS
  without bundled Delivery Status Message


  New Session (1b)     ------------------->
  with ephemeral key 3
  with static key for binding
  with bundled HTTP POST part 3
  with bundled LS
  without bundled Delivery Status Message


  following messages can arrive in any order:

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 1
                      with bundled streaming ack

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 2
                      with bundled streaming ack

  After reception of any of these messages,
  Alice switches to use Existing Session messages,
  creates a new inbound + outbound session pair,
  and ratchets.


  following messages can arrive in any order:


  Existing Session     ------------------->
  with bundled HTTP POST part 4

  Existing Session     ------------------->
  with next key
  with bundled HTTP POST part 5


  After reception of any of these messages,
  Bob switches to use Existing Session messages.


  <--------------     Existing Session
                      with bundled streaming ack

  After reception of any of this message,
  Alice switches to use Existing Session messages,
  and Alice ratchets.


  Existing Session     ------------------->
  with next key
  with bundled HTTP POST part 4

  after reception of this message, Bob ratchets

  Existing Session     ------------------->
  with next key
  with bundled HTTP POST part 5

  <--------------     Existing Session
                      with bundled streaming ack

```
### 消息编号

单个消息，期望单个回复。可能会发送其他消息或回复。

类似于 HTTP GET，但会话标签窗口大小和生命周期的选项更少。可能不请求 ratchet。

```

Alice                           Bob

  New Session (1b)     ------------------->
  with static key for binding
  with next key
  with bundled repliable datagram
  with bundled LS
  without bundled Delivery Status Message


  <--------------     New Session Reply (1g)
                      with Bob ephemeral key
                      with bundled reply part 1

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key
                      with bundled reply part 2

  After reception of either message,
  Alice switches to use Existing Session messages,
  and ratchets.

  If the Existing Session message arrives first,
  Alice ratchets on the existing inbound and outbound
  sessions.

  When the New Session Reply arrives, Alice
  sets the existing inbound session to expire,
  creates a new inbound and outbound session,
  and sends Existing Session messages on
  the new outbound session.

  Alice keeps the expiring inbound session
  around for a while to process the Existing Session
  message sent to Alice.
  If all expected original Existing Session message replies
  have been processed, Alice can expire the original
  inbound session immediately.

  if there are any other messages:

  Existing Session     ------------------->
  with bundled message

  Existing Session     ------------------->
  with bundled streaming ack

  <--------------     Existing Session
                      with bundled message

```
### 下一个 DH Ratchet 公钥

多个匿名消息，不期待回复。

在这种情况下，Alice 请求一个会话，但不进行绑定。发送新会话消息。没有捆绑回复 LS。捆绑了一个回复 DSM（这是唯一需要捆绑 DSM 的用例）。不包含下一个密钥。不请求回复或 ratchet。不发送 ratchet。选项将会话标签窗口设置为零。

```

Alice                           Bob

  New Session (1c)     ------------------->
  with bundled message
  without bundled LS
  with bundled Delivery Status Message 1

  New Session (1c)     ------------------->
  with bundled message
  without bundled LS
  with bundled Delivery Status Message 2

  New Session (1c)     ------------------->
  with bundled message
  without bundled LS
  with bundled Delivery Status Message 3
 
  following messages can arrive in any order:

  <--------------     Delivery Status Message 1

  <--------------     Delivery Status Message 2

  <--------------     Delivery Status Message 3

  After reception of any of these messages,
  Alice switches to use Existing Session messages.

  Existing Session     ------------------->

  Existing Session     ------------------->

  Existing Session     ------------------->

```
### 确认

一条匿名消息，无需回复。

发送一次性消息。不绑定回复 LS 或 DSM。不包含下一个密钥。不请求回复或 ratchet。不发送 ratchet。选项将会话标签窗口设置为零。

```

Alice                           Bob

  One-Time Message (1d)   ------------------->
  with bundled message
  without bundled LS
  without bundled Delivery Status Message

```
### 确认请求

长期会话可能会在任何时候进行棘轮操作或请求棘轮操作，以从该时间点开始保持前向保密性。当会话接近每个会话发送消息的限制（65535）时，必须进行棘轮操作。

## Implementation Considerations

### 填充

与现有的 ElGamal/AES+SessionTag 协议一样，实现必须限制 session tag 存储并防范内存耗尽攻击。

一些推荐的策略包括：

- 存储的会话标签数量硬限制
- 内存压力下积极过期空闲入站会话
- 绑定到单个远端目标的入站会话数量限制
- 内存压力下自适应减少会话标签窗口并删除旧的未使用标签
- 内存压力下拒绝按请求进行棘轮操作

### 其他区块类型

推荐参数和超时设置：

- NSR tagset 大小：12 tsmin 和 tsmax
- ES tagset 0 大小：tsmin 24，tsmax 160
- ES tagset (1+) 大小：160 tsmin 和 tsmax
- NSR tagset 超时：接收方 3 分钟
- ES tagset 超时：发送方 8 分钟，接收方 10 分钟
- 删除先前 ES tagset 后：3 分钟
- Tagset 向前查找标签 N：min(tsmax, tsmin + N/4)
- Tagset 向后修剪标签 N：min(tsmax, tsmin + N/4) / 2
- 在标签处发送下一个密钥：TBD
- Tagset 生命周期后发送下一个密钥：TBD
- 如果在以下时间后收到 NS 则替换会话：3 分钟
- 最大时钟偏差：-5 分钟到 +2 分钟
- NS 重放过滤器持续时间：5 分钟
- 填充大小：0-15 字节（其他策略 TBD）

### 未来工作

以下是对传入消息进行分类的建议。

### X25519 Only

在仅使用此协议的 tunnel 上，按照当前 ElGamal/AES+SessionTags 的方式进行身份识别：

首先，将初始数据视为会话标签，并查找该会话标签。如果找到，则使用与该会话标签关联的存储数据进行解密。

如果未找到，将初始数据视为 DH 公钥和 nonce。执行 DH 操作和指定的 KDF，然后尝试解密剩余数据。

### HTTP GET

在支持此协议和 ElGamal/AES+SessionTags 的隧道上，按以下方式对传入消息进行分类：

由于ElGamal/AES+SessionTags规范中的一个缺陷，AES块没有填充到随机的非16倍数长度。因此，现有会话消息的长度模16总是0，新会话消息的长度模16总是2（因为ElGamal块长度为514字节）。

如果长度模16不等于0或2，则将初始数据视为session tag，并查找该session tag。如果找到，则使用与该session tag关联的存储数据进行解密。

如果未找到，且长度模16不等于0或2，则将初始数据视为DH公钥和随机数。执行DH操作和指定的KDF，并尝试解密剩余数据。（基于相对流量组合和X25519与ElGamal DH操作的相对成本，此步骤可能会最后执行）

否则，如果长度模16等于0，将初始数据视为ElGamal/AES会话标签，并查找该会话标签。如果找到，使用与该会话标签关联的存储数据进行解密。

如果未找到，且数据至少为 642（514 + 128）字节长，并且长度对 16 取模等于 2，则将初始数据视为 ElGamal 块。尝试解密剩余数据。

请注意，如果 ElGamal/AES+SessionTag 规范更新为允许非模16填充，则需要采用不同的处理方式。

### HTTP POST

初始实现依赖于高层的双向流量。也就是说，实现假设相反方向的流量很快就会被传输，这将强制在 ECIES 层产生任何必需的响应。

但是，某些流量可能是单向的或带宽非常低，因此没有更高层的流量来产生及时的响应。

接收 NS 和 NSR 消息需要响应；接收 ACK Request 和 Next Key 块也需要响应。

一个复杂的实现可能会在收到这些需要响应的消息之一时启动计时器，如果在短时间内（例如1秒）没有发送反向流量，则在ECIES层生成"空"（没有Garlic Clove块）响应。

对于 NS 和 NSR 消息的响应，使用更短的超时时间可能也是合适的，以便尽快将流量转移到高效的 ES 消息上。

## Analysis

### 可回复数据报

每个方向前两条消息的消息开销如下。这假设在 ACK 之前每个方向只有一条消息，或者任何额外的消息都作为现有会话消息进行推测性发送。如果没有对已传递会话标签的推测性确认，旧协议的开销会高得多。

分析新协议时不假设填充。不假设捆绑的 leaseSet。

### 多个原始数据报

新会话消息，每个方向相同：

```

ElGamal block:
  514 bytes

  AES block:
  - 2 byte tag count
  - 1024 bytes of tags (32 typical)
  - 4 byte payload size
  - 32 byte hash of payload
  - 1 byte flags
  - 1 byte clove count
  - 33 byte Garlic deliv. inst.
  - 16 byte I2NP header
  - 15 byte clove cert, id, exp.
  - 15 byte msg cert, id, exp.
  - 0 byte padding assuming 1936 byte message
  1143 total

  Total:
  1657 bytes
```
现有会话消息，每个方向相同：

```

AES block:
  - 32 byte session tag
  - 2 byte tag count
  - 4 byte payload size
  - 32 byte hash of payload
  - 1 byte flags
  - 1 byte clove count
  - 33 byte Garlic deliv. inst.
  - 16 byte I2NP header
  - 15 byte msg cert, id, exp.
  - 15 byte clove cert, id, exp.
  - 0 byte padding assuming 1936 byte message
  151 total
```
```
Four message total (two each direction)
  3616 bytes overhead
```
### 单个原始数据报

Alice-to-Bob 新会话消息：

```

- 32 byte ephemeral public key
  - 32 byte static public key
  - 16 byte Poly1305 MAC
  - 7 byte DateTime block
  - 3 byte Garlic block overhead
  - 9 byte I2NP header
  - 33 byte Garlic deliv. inst.
  - 16 byte Poly1305 MAC

  Total:
  148 bytes overhead
```
Bob-to-Alice 新会话回复消息：

```

- 8 byte session tag
  - 32 byte ephemeral public key
  - 16 byte Poly1305 MAC
  - 3 byte Garlic block overhead
  - 9 byte I2NP header
  - 33 byte Garlic deliv. inst.
  - 16 byte Poly1305 MAC

  Total:
  117 bytes overhead
```
现有会话消息，每个方向相同：

```

- 8 byte session tag
  - 3 byte Garlic block overhead
  - 9 byte I2NP header
  - 33 byte Garlic deliv. inst.
  - 16 byte Poly1305 MAC

  Total:
  69 bytes
```
### 长期会话

总共四条消息（每个方向两条）：

```

372 bytes
  90% (approx. 10x) reduction compared to ElGamal/AES+SessionTags
```
仅握手：

```

ElGamal: 1657 + 1657 = 3314 bytes
  Ratchet: 148 _ 117 = 265 bytes
  92% (approx. 12x) reduction compared to ElGamal/AES+SessionTags
```
长期总计（忽略握手）：

```
ElGamal: 151 + 32 byte tag sent previously = 183 bytes
  Ratchet: 69 bytes
  64% (approx. 3x) reduction compared to ElGamal/AES+SessionTags
```
### CPU

TODO 在提案稳定后更新此部分。

每一方交换 New Session 和 New Session Reply 消息都需要以下加密操作：

- HMAC-SHA256: 每个HKDF 3次，总计待定
- ChaChaPoly: 各2次
- X25519密钥生成: Alice 2次，Bob 1次
- X25519 DH: 各3次
- 签名验证: 1次 (Bob)

Alice 为每个绑定会话计算至少 5 个 ECDH，向 Bob 发送的每个 NS 消息需要 2 个，Bob 的每个 NSR 消息需要 3 个。

Bob 也会为每个绑定会话计算 6 个 ECDH，其中 3 个用于 Alice 的每条 NS 消息，3 个用于他自己的每条 NSR 消息。

每一方在处理每个现有会话消息时都需要执行以下加密操作：

- HKDF：2
- ChaChaPoly：1

### 防御

当前会话标签长度为 32 字节。我们尚未找到该长度的任何依据，但我们正在继续研究档案。上述提案将新标签长度定义为 8 字节。证明 8 字节标签合理性的分析如下：

session tag ratchet 被假定生成随机、均匀分布的标签。对于特定的 session tag 长度没有加密学上的原因。session tag ratchet 与对称密钥 ratchet 同步，但生成独立的输出。两个 ratchet 的输出可能具有不同的长度。

因此，唯一需要关注的是会话标签冲突。假设实现不会尝试通过两个会话同时解密来处理冲突；实现将简单地将标签与之前的会话或新会话关联，任何在另一个会话上收到的带有该标签的消息在解密失败后都将被丢弃。

目标是选择一个足够大的会话标签长度以最小化碰撞风险，同时又足够小以最小化内存使用。

这假设实现会限制会话标签存储以防止内存耗尽攻击。这也将大大降低攻击者能够创建冲突的可能性。请参阅下面的实现考虑事项部分。

对于最坏情况，假设一个繁忙的服务器每秒有64个新的入站会话。假设15分钟的入站会话标签生存期（与现在相同，可能应该减少）。假设入站会话标签窗口为32。64 * 15 * 60 * 32 = 1,843,200 个标签。当前Java I2P最大入站标签数为750,000，据我们所知从未达到过这个数值。

百万分之一 (1e-6) 的 session tag 碰撞目标可能就足够了。由于网络拥塞导致消息在传输过程中丢失的概率远高于此。

参考：https://en.wikipedia.org/wiki/Birthday_paradox 概率表部分。

使用 32 字节 session tags（256 位），session tag 空间为 1.2e77。碰撞概率为 1e-18 时需要 4.8e29 个条目。碰撞概率为 1e-6 时需要 4.8e35 个条目。180 万个 32 字节的 tags 总共约为 59 MB。

使用16字节会话标签（128位），会话标签空间为3.4e38。碰撞概率为1e-18时需要2.6e10个条目。碰撞概率为1e-6时需要2.6e16个条目。180万个16字节标签总计约30 MB。

使用8字节session tags（64位），session tag空间为1.8e19。碰撞概率为1e-18时需要6.1个条目。碰撞概率为1e-6时需要6.1e6（6,100,000）个条目。180万个8字节的tags总计约15 MB。

610万个活跃标签是我们最坏情况下估计的180万个标签的3倍以上。因此碰撞的概率将小于百万分之一。我们因此得出结论，8字节的session tags是足够的。这导致存储空间减少4倍，加上因为传输标签不被存储而减少的2倍。所以与ElGamal/AES+SessionTags相比，我们的session tag内存使用量将减少8倍。

为了在这些假设错误时保持灵活性，我们将在选项中包含一个会话标签长度字段，以便可以在每个会话的基础上覆盖默认长度。除非绝对必要，否则我们不打算实现动态标签长度协商。

实现应该至少能够识别会话标签冲突，优雅地处理这些冲突，并记录或计算冲突次数。虽然仍然极不可能发生，但它们比 ElGamal/AES+SessionTags 的情况更有可能发生，并且确实可能会发生。

### 参数

使用两倍的每秒会话数（128）和两倍的标签窗口（64），我们有4倍的标签数（740万）。百万分之一碰撞概率的最大值是610万个标签。12字节（甚至10字节）标签将增加巨大的安全边际。

然而，百万分之一的碰撞概率是一个好的目标吗？比在传输过程中被丢弃的概率大得多并没有太大用处。Java 的 DecayingBloomFilter 的误报目标大约是万分之一，但即使是千分之一也不是什么严重问题。通过将目标降低到万分之一，8 字节标签就有了充足的余量。

### 分类

发送方实时生成标签和密钥，因此无需存储。与 ElGamal/AES 相比，这将整体存储需求减半。ECIES 标签为 8 字节，而 ElGamal/AES 为 32 字节。这将整体存储需求再减少 4 倍。接收方不存储每个标签的会话密钥，除了"间隙"部分，在合理的丢失率下这些间隙是最小的。

标签过期时间减少33%会带来另外33%的节省，假设会话时间较短。

因此，相比 ElGamal/AES 的总空间节省系数为 10.7，即 92%。

## Related Changes

### X25519 专用

来自 ECIES 目标的数据库查询：参见 [Proposal 154](/proposals/154-ecies-lookups)，现已纳入 [I2NP](/docs/specs/i2np/) 用于 0.9.46 版本。

此提案需要 LS2 支持来与 leaseset 一起发布 X25519 公钥。不需要对 [I2NP](/docs/specs/i2np/) 中的 LS2 规范进行任何更改。所有支持都在 [Proposal 123](/proposals/123-new-netdb-entries) 中设计、规范和实现，该提案在 0.9.38 版本中实现。

### X25519 共享与 ElGamal/AES+SessionTags

无。此提案需要 LS2 支持，以及在 I2CP 选项中设置一个属性来启用。不需要对 [I2CP](/docs/specs/i2cp/) 规范进行任何更改。所有支持都在 [Proposal 123](/proposals/123-new-netdb-entries) 中设计、规范和实现，该提案在 0.9.38 版本中实现。

启用 ECIES 所需的选项是一个单独的 I2CP 属性，适用于 I2CP、BOB、SAM 或 i2ptunnel。

典型值为 i2cp.leaseSetEncType=4（仅 ECIES），或 i2cp.leaseSetEncType=4,0（ECIES 和 ElGamal 双密钥）。

### 协议层响应

本节内容复制自 [Proposal 123](/proposals/123-new-netdb-entries)。

SessionConfig 映射中的选项：

```
  i2cp.leaseSetEncType=nnn[,nnn]  The encryption types to be used.
                                  0: ElGamal
                                  1-3: See proposal 145
                                  4: This proposal.
```
### Create Leaseset2 Message

该提案需要 LS2，从版本 0.9.38 开始支持。[I2CP](/docs/specs/i2cp/) 规范无需任何更改。所有支持都在 [Proposal 123](/proposals/123-new-netdb-entries) 中设计、规定和实现，该提案在 0.9.38 中实现。

### 开销

任何支持双密钥 LS2 的 router（0.9.38 或更高版本）都应该支持连接到具有双密钥的目标节点。

仅支持 ECIES 的目标地址将需要大多数 floodfill 节点升级到 0.9.46 版本才能获得加密的查找回复。请参阅[提案 154](/proposals/154-ecies-lookups)。

仅支持 ECIES 的目标只能与其他仅支持 ECIES 或双密钥的目标连接。
