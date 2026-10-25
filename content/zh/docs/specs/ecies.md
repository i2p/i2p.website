---
title: "ECIES-X25519-AEAD-Ratchet"
description: "I2P端到端加密的椭圆曲线集成加密方案"
slug: "ecies"
aliases:
  - "/zh/docs/specs/ecies-x25519-aead-ratchet"
  - "/zh/docs/specs/ecies-x25519-aead-ratchet/"
category: "协议"
lastUpdated: "2025-06"
accurateFor: "0.9.67"
---

## 注意

网络部署完成。可能会有小幅修订。请参阅 [Prop144](/proposals/144-ecies-x25519/) 查看原始提案，包括背景讨论和附加信息。

截至 0.9.66 版本，以下功能尚未实现：

- MessageNumbers、Options 和 Termination 块
- 协议层响应
- 零静态密钥
- 多播

关于此协议的 MLKEM PQ Hybrid 版本，请参阅 [ECIES-HYBRID](/docs/specs/ecies-hybrid/)。

## 概述

这是用于替代 ElGamal/AES+SessionTags [ElG-AES](/docs/specs/elgamal-aes/) 的新端到端加密协议。

它依赖于以下先前的工作：

- 通用结构规范 [Common](/docs/specs/common-structures/)
- [I2NP](/docs/specs/i2np/) 规范包括 LS2
- ElGamal/AES+Session Tags [Elg-AES](/docs/specs/elgamal-aes/)
- <http://zzz.i2p/topics/1768> 新非对称加密概述
- 底层加密概述 [CRYPTO-ELG](/docs/specs/cryptography/#elgamal)
- ECIES <http://zzz.i2p/topics/2418>
- [NTCP2](/docs/specs/ntcp2/) [Prop111](/proposals/111-ntcp2/)
- 123 新 netDb 条目
- 142 新加密模板
- [Noise](https://noiseprotocol.org/noise.html) 协议
- [Signal](https://signal.org/docs/specifications/doubleratchet/) 双棘轮算法

它支持端到端、destination 到 destination 通信的新加密方式。

该设计使用 Noise 握手和数据阶段，结合了 Signal 的双重棘轮机制。

本规范中对 Signal 和 Noise 的所有引用仅供背景信息参考。理解或实现本规范不需要了解 Signal 和 Noise 协议。

此规范从版本 0.9.46 开始支持。

## 规范

该设计使用 Noise 握手和数据阶段，并融合了 Signal 的双棘轮机制。

### 密码学设计概述

协议需要重新设计的部分有五个：

- 1\) 新的和现有的会话容器格式将被新格式替换。
- 2\) ElGamal（256字节公钥，128字节私钥）将被ECIES-X25519（32字节公钥和私钥）替换
- 3\) AES将被AEAD_ChaCha20_Poly1305（以下简称ChaChaPoly）替换
- 4\) SessionTags将被棘轮机制替换，本质上是一个密码学同步PRNG。
- 5\) 在ElGamal/AES+SessionTags规范中定义的AES载荷，将被类似于NTCP2中的块格式替换。

以下五个变更各自都有对应的章节。

### 加密类型

加密类型（在LS2中使用）是4。这表示一个小端序32字节X25519公钥，以及此处指定的端到端协议。

加密类型 0 是 ElGamal。加密类型 1-3 保留用于 ECIES-ECDH-AES-SessionTag，参见提案 145 [Prop145](/proposals/145-ecies-ecdh-aes/)。

### Noise 协议框架

该协议基于 Noise Protocol Framework [NOISE](https://noiseprotocol.org/noise.html)（修订版 34，2018-07-11）提供要求。Noise 具有与 Station-To-Station 协议 [STS](https://en.wikipedia.org/wiki/Station-to-Station_protocol) 类似的特性，后者是 [SSU](/docs/transport/ssu/) 协议的基础。在 Noise 术语中，Alice 是发起方，Bob 是响应方。

该规范基于 Noise 协议 Noise_IK_25519_ChaChaPoly_SHA256。（初始密钥派生函数的实际标识符是 "Noise_IKelg2_25519_ChaChaPoly_SHA256"，用于表示 I2P 扩展 - 请参见下面的 KDF 1 部分）此 Noise 协议使用以下原语：

- 交互式握手模式：IK Alice 立即将她的静态密钥传输给 Bob (I) Alice 已经知道 Bob 的静态密钥 (K)
- 单向握手模式：N Alice 不将她的静态密钥传输给 Bob (N)
- DH 函数：X25519 使用 32 字节密钥长度的 X25519 DH，如 [RFC-7748](https://tools.ietf.org/html/rfc7748) 中所规定。
- 密码函数：ChaChaPoly AEAD_CHACHA20_POLY1305，如 [RFC-7539](https://tools.ietf.org/html/rfc7539) 第 2.8 节所规定。12 字节随机数，前 4 字节设为零。与 [NTCP2](/docs/specs/ntcp2/) 中的相同。
- 哈希函数：SHA256 标准 32 字节哈希，在 I2P 中已被广泛使用。

#### 框架的补充内容

本规范定义了对 Noise_IK_25519_ChaChaPoly_SHA256 的以下增强。这些增强通常遵循 [NOISE](https://noiseprotocol.org/noise.html) 第 13 节中的指导原则。

1) 明文临时密钥使用以下方式编码

    [Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf).
2) 回复以明文标签为前缀。3) 载荷格式定义适用于消息1、消息2和数据阶段。

    Of course, this is not defined in Noise.

所有消息都包含一个 [I2NP](/docs/specs/i2np/) Garlic Message 头部。数据阶段使用类似于但不兼容 Noise 数据阶段的加密。

### 握手模式

握手使用 [Noise](https://noiseprotocol.org/noise.html) 握手模式。

使用以下字母映射：

- e = 一次性临时密钥
- s = 静态密钥
- p = 消息载荷

一次性和非绑定会话类似于 Noise N 模式。

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
#### 安全特性

使用 Noise 术语，建立和数据序列如下：（载荷安全属性来自 [Noise](https://noiseprotocol.org/noise.html)）

```
IK(s, rs):           Authentication   Confidentiality
  <- s
  ...
  -> e, es, s, ss           1                2
  <- e, ee, se              2                4
  ->                        2                5
  <-                        2                5
```
#### 与 XK 的区别

IK 握手与 [NTCP2](/docs/specs/ntcp2/) 和 [SSU2](/docs/specs/ssu2/) 中使用的 XK 握手有几个不同之处。

- 总共四次DH操作，相比XK的三次
- 第一条消息中的发送方认证：载荷被认证为属于发送方公钥的所有者，尽管密钥可能已被泄露（认证1）。XK需要另一轮往返才能完成Alice的认证。
- 第二条消息后的完全前向保密性（机密性5）。Bob可以在第二条消息后立即发送具有完全前向保密性的载荷。XK需要另一轮往返才能实现完全前向保密性。

总结来说，IK 允许 Bob 向 Alice 进行 1-RTT 响应载荷传输并具有完全前向保密性，但是请求载荷不具有前向保密性。

### 会话

ElGamal/AES+SessionTag协议是单向的。在这一层，接收方不知道消息来自哪里。出站和入站会话没有关联。确认是通过带外方式使用DeliveryStatusMessage（封装在GarlicMessage中）在瓣片中进行的。

在本规范中，我们定义了两种创建双向协议的机制——"配对"和"绑定"。这些机制提供了更高的效率和安全性。

#### 会话上下文

与 ElGamal/AES+SessionTags 一样，所有入站和出站会话都必须在给定的上下文中，要么是 router 的上下文，要么是特定本地目标的上下文。在 Java I2P 中，这个上下文称为会话密钥管理器。

会话不得在上下文之间共享，因为这会允许各种本地目标之间，或本地目标与 router 之间的关联分析。

当给定目标同时支持 ElGamal/AES+SessionTags 和本规范时，两种类型的会话可以共享一个上下文。请参见下面第 1c) 节。

#### 配对入站和出站会话

当在发起方（Alice）创建出站会话时，会创建一个新的入站会话并与出站会话配对，除非不需要回复（例如原始数据报）。

新的入站会话总是与新的出站会话配对，除非不需要回复（例如原始数据报）。

如果请求回复并绑定到远端目标或router，那么新的出站会话将绑定到该目标或router，并替换任何先前到该目标或router的出站会话。

配对入站和出站会话提供了一个双向协议，具有轮换DH密钥的能力。

#### 绑定会话和目标

到给定目的地或router只有一个出站会话。可能有多个来自给定目的地或router的当前入站会话。通常，当创建新的入站会话并在该会话上接收到流量时（这相当于ACK确认），任何其他会话都会被标记为相对较快地过期，大约在一分钟左右。会检查之前发送的消息（PN）值，如果在之前的入站会话中没有未接收的消息（在窗口大小范围内），则可能立即删除之前的会话。

当发起方（Alice）创建出站会话时，它会绑定到远端目的地（Bob），任何配对的入站会话也将绑定到远端目的地。随着会话的棘轮更新，它们将继续绑定到远端目的地。

当在接收方（Bob）创建入站会话时，可以根据Alice的选择绑定到远端Destination（Alice）。如果Alice在新会话消息中包含绑定信息（她的静态密钥），该会话将绑定到该destination，并且将创建出站会话并绑定到相同的Destination。随着会话的棘轮推进，它们继续绑定到远端Destination。

#### 绑定和配对的好处

对于常见的流式传输情况，我们期望 Alice 和 Bob 按以下方式使用该协议：

- Alice 将她的新出站会话与新入站会话配对，两者都绑定到远端目标（Bob）。
- Alice 在发送给 Bob 的新会话消息中包含绑定信息和签名，以及回复请求。
- Bob 将他的新入站会话与新出站会话配对，两者都绑定到远端目标（Alice）。
- Bob 在配对会话中向 Alice 发送回复（确认），并使用新的 DH 密钥进行棘轮。
- Alice 使用 Bob 的新密钥棘轮到新的出站会话，与现有入站会话配对。

通过将入站会话绑定到远端目标地址，并将入站会话与绑定到同一目标地址的出站会话配对，我们获得了两个主要好处：

1) Bob对Alice的初始回复使用临时-临时DH

2\) 在 Alice 收到 Bob 的回复并进行棘轮操作后，Alice 发送给 Bob 的所有后续消息都使用临时-临时 DH。

#### 消息确认

在 ElGamal/AES+SessionTags 中，当 LeaseSet 作为 garlic clove 打包时，或者传送标签时，发送方 router 会请求 ACK 确认。这是一个包含 DeliveryStatus 消息的独立 garlic clove。为了额外的安全性，DeliveryStatus 消息被包装在 Garlic 消息中。从协议的角度来看，这种机制是带外的。

在新协议中，由于入站和出站会话是配对的，我们可以进行带内ACK。不需要单独的clove。

显式 ACK 就是一个没有 I2NP 块的现有会话消息。但是，在大多数情况下可以避免显式 ACK，因为存在反向流量。对于实现来说，可能希望在发送显式 ACK 之前等待短时间（可能一百毫秒），以给流传输层或应用层时间来响应。

实现还需要推迟任何 ACK 发送，直到 I2NP 块处理完成后，因为 Garlic Message 可能包含带有 leaseSet 的 Database Store Message。需要最新的 leaseSet 来路由 ACK，而远端目标（包含在 leaseSet 中）对于验证绑定静态密钥是必需的。

#### 会话超时

出站会话应该总是在入站会话之前过期。一旦出站会话过期并创建了新的会话，也会创建一个新的配对入站会话。如果存在旧的入站会话，它将被允许过期。

### 组播

待定

### 定义

我们定义以下对应于所使用的密码学构建块的函数。

ZEROLEN

零长度字节数组

CSRNG(n)

来自加密安全随机数生成器的 n 字节输出

    generator.

H(p, d)

接受个性化字符串 p 和数据的 SHA-256 哈希函数

    d, and produces an output of length 32 bytes. As defined in
    [NOISE](https://noiseprotocol.org/noise.html). || below means append.

    Use SHA-256 as follows:

        H(p, d) := SHA-256(p || d)

MixHash(d)

SHA-256 哈希函数接受先前的哈希值 h 和新数据 d，

    and produces an output of length 32 bytes. || below means append.

    Use SHA-256 as follows:

        MixHash(d) := h = SHA-256(h || d)

STREAM

ChaCha20/Poly1305 AEAD 如规范中所述

    [RFC-7539](https://tools.ietf.org/html/rfc7539). S_KEY_LEN = 32 and S_IV_LEN =
    12.

    ENCRYPT(k, n, plaintext, ad)

    :   Encrypts plaintext using the cipher key k, and nonce n which
        MUST be unique for the key k. Associated data ad is optional.
        Returns a ciphertext that is the size of the plaintext + 16
        bytes for the HMAC.

        The entire ciphertext must be indistinguishable from random if
        the key is secret.

    DECRYPT(k, n, ciphertext, ad)

    :   Decrypts ciphertext using the cipher key k, and nonce n.
        Associated data ad is optional. Returns the plaintext.

DH

X25519 公钥协商系统。32 字节的私钥，公钥

    keys of 32 bytes, produces outputs of 32 bytes. It has the following
    functions:

    GENERATE_PRIVATE()

    :   Generates a new private key.

    DERIVE_PUBLIC(privkey)

    :   Returns the public key corresponding to the given private key.

    GENERATE_PRIVATE_ELG2()

    :   Generates a new private key that maps to a public key suitable
        for Elligator2 encoding. Note that half of the
        randomly-generated private keys will not be suitable and must be
        discarded.

    ENCODE_ELG2(pubkey)

    :   Returns the Elligator2-encoded public key corresponding to the
        given public key (inverse mapping). Encoded keys are little
        endian. Encoded key must be 256 bits indistinguishable from
        random data. See Elligator2 section below for specification.

    DECODE_ELG2(pubkey)

    :   Returns the public key corresponding to the given
        Elligator2-encoded public key. See Elligator2 section below for
        specification.

    DH(privkey, pubkey)

    :   Generates a shared secret from the given private and public
        keys.

HKDF(salt, ikm, info, n)

一个密码学密钥派生函数，接受一些输入密钥

    material ikm (which should have good entropy but is not required to
    be a uniformly random string), a salt of length 32 bytes, and a
    context-specific 'info' value, and produces an output of n bytes
    suitable for use as key material.

    Use HKDF as specified in [RFC-5869](https://tools.ietf.org/html/rfc5869), using
    the HMAC hash function SHA-256 as specified in
    [RFC-2104](https://tools.ietf.org/html/rfc2104). This means that SALT_LEN is 32
    bytes max.

MixKey(d)

使用 HKDF() 函数处理之前的 chainKey 和新数据 d，并设置新的

    chainKey and k. As defined in [NOISE](https://noiseprotocol.org/noise.html).

    Use HKDF as follows:

        MixKey(d) := output = HKDF(chainKey, d, "", 64)
                     chainKey = output[0:31]
                     k = output[32:63]

### 1) 消息格式

#### 当前消息格式审查

如[I2NP](/docs/specs/i2np/)中所指定的Garlic Message格式如下。由于设计目标是中间跳跃节点无法区分新旧加密方式，因此该格式不能更改，即使长度字段是冗余的。此格式显示了完整的16字节头部，尽管实际头部可能采用不同格式，具体取决于所使用的传输方式。

解密后，数据包含一系列 Garlic Cloves 和附加数据，也称为 Clove Set。

详见 [I2NP](/docs/specs/i2np/) 了解详情和完整规范。

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
#### 加密数据格式审查

在 ElGamal/AES+SessionTags 中，有两种消息格式：

1\) 新会话： - 514字节ElGamal块 - AES块（最少128字节，16的倍数）

2\) 现有会话： - 32 字节会话标签 - AES 块（最少 128 字节，16 的倍数）

这些消息被封装在一个 I2NP garlic message 中，该消息包含一个长度字段，因此长度是已知的。

接收方首先尝试将前32字节作为Session Tag进行查找。如果找到，则解密AES块。如果未找到，且数据长度至少为(514+16)字节，则尝试解密ElGamal块，如果成功，再解密AES块。

#### 新会话标签及与Signal的比较

在 Signal Double Ratchet 中，消息头包含：

- DH: 当前棘轮公钥
- PN: 前一链消息长度
- N: 消息编号

Signal 的"发送链"大致相当于我们的标签集。通过使用会话标签，我们可以消除其中的大部分内容。

在新会话中，我们只在未加密的头部放置公钥。

在现有会话中，我们使用会话标签作为头部。会话标签与当前棘轮公钥和消息编号相关联。

在新会话和现有会话中，PN 和 N 都在加密体内。

在Signal中，密钥不断地进行棘轮更新。新的DH公钥要求接收方进行棘轮操作并发送新的公钥作为回应，这同时也作为对接收到的公钥的确认。对我们来说，这会产生过多的DH运算。因此我们将接收到的密钥的确认和新公钥的传输分离开来。任何使用从新DH公钥生成的session tag的消息都构成确认。我们仅在希望重新生成密钥时才传输新的公钥。

DH必须进行棘轮操作之前的最大消息数量是65535。

在交付会话密钥时，我们从中推导出"标签集"，而不必同时交付会话标签。一个标签集最多可包含65536个标签。但是，接收者应该实施"预先生成"策略，而不是一次性生成所有可能的标签。最多只生成超过最后一个有效接收标签N个标签。N最多可能是128，但32或更少可能是更好的选择。

### 1a) 新会话格式

新会话一次性公钥（32字节）加密数据和MAC（剩余字节）

New Session 消息可能包含也可能不包含发送方的静态公钥。如果包含，反向会话将绑定到该密钥。如果期望收到回复，即用于流传输和可回复数据报，则应包含静态密钥。对于原始数据报则不应包含。

New Session 消息类似于单向 Noise [NOISE](https://noiseprotocol.org/noise.html) 模式 "N"（如果不发送静态密钥），或双向模式 "IK"（如果发送静态密钥）。

### 1b) 新会话格式（带绑定）

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
#### 新会话临时密钥

临时密钥为32字节，使用Elligator2编码。此密钥从不重复使用；每条消息都会生成新密钥，包括重传消息。

#### 静态密钥

解密后，Alice 的 X25519 静态密钥，32 字节。

#### 负载

加密长度是数据的剩余部分。解密长度比加密长度少16字节。载荷必须包含一个DateTime块，通常还会包含一个或多个Garlic Clove块。格式和其他要求请参见下面的载荷部分。

### 1c) 新会话格式（无绑定）

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
#### 新会话临时密钥

Alice的临时密钥。临时密钥为32字节，使用Elligator2编码，小端序。此密钥从不重复使用；每条消息都会生成新密钥，包括重传消息。

#### 标志段解密数据

标志位部分不包含任何内容。它总是32字节，因为它必须与用于绑定的新会话消息中的静态密钥长度相同。Bob通过测试这32个字节是否全为零来确定它是静态密钥还是标志位部分。

TODO 这里需要任何标志吗？

#### 载荷

加密长度是数据的剩余部分。解密长度比加密长度少16字节。载荷必须包含一个DateTime块，通常还会包含一个或多个Garlic Clove块。有关格式和附加要求，请参见下面的载荷部分。

### 1d) 一次性格式（无绑定或会话）

如果只需要发送单条消息，则不需要会话设置或静态密钥。

长度为 96 + 载荷长度。加密格式：

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
#### 新会话一次性密钥

一次性密钥为32字节，使用Elligator2编码，小端序。此密钥永不重复使用；每条消息都会生成新密钥，包括重传消息。

#### 标志部分解密数据

Flags 部分不包含任何内容。它始终是 32 字节，因为它必须与带绑定的新会话消息中的静态密钥长度相同。Bob 通过测试这 32 字节是否全为零来判断它是静态密钥还是 flags 部分。

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
#### 载荷

加密长度是数据的剩余部分。解密长度比加密长度少16字节。载荷必须包含一个DateTime块，通常还会包含一个或多个Garlic Clove块。格式和附加要求请参见下面的载荷部分。

### 1f) 新会话消息的密钥派生函数 (KDFs)

#### 初始 ChainKey 的 KDF

这是用于 IK 的标准 [NOISE](https://noiseprotocol.org/noise.html)，但使用了修改过的协议名称。注意我们对 IK 模式（绑定会话）和 N 模式（非绑定会话）使用相同的初始化器。

协议名称被修改有两个原因。首先，表明临时密钥使用 Elligator2 编码，其次，表明在第二条消息之前调用 MixHash() 来混合标签值。

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
#### 标志/静态密钥段加密内容的密钥派生函数

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
#### 载荷部分的密钥派生函数（使用 Alice 静态密钥）

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
#### 负载部分的密钥派生函数（不含 Alice 静态密钥）

请注意，这是一个 Noise "N" 模式，但我们使用与绑定会话相同的 "IK" 初始化器。

New Session消息在静态密钥被解密并检查是否包含全零之前，无法确定是否包含Alice的静态密钥。因此，接收方必须对所有New Session消息使用"IK"状态机。如果静态密钥全为零，则必须跳过"ss"消息模式。

```
chainKey = from Flags/Static key section
k = from Flags/Static key section
n = 1
ad = h from Flags/Static key section
ciphertext = ENCRYPT(k, n, payload, ad)
```
### 1g) 新会话回复格式

可能会发送一个或多个New Session Replies来响应单个New Session消息。每个回复都会以一个标签作为前缀，该标签是从会话的TagSet中生成的。

新会话回复分为两部分。第一部分是完成 Noise IK 握手，前面带有一个标签。第一部分的长度是 56 字节。第二部分是数据阶段载荷。第二部分的长度是 16 + 载荷长度。

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
#### 会话标签

该标签在会话标签 KDF 中生成，如下面的 DH 初始化 KDF 中初始化的那样。这将回复与会话关联起来。不使用来自 DH 初始化的会话密钥。

#### 新会话回复临时密钥

Bob的临时密钥。临时密钥为32字节，使用Elligator2编码，小端序。此密钥永不重用；每条消息都会生成新密钥，包括重传消息。

#### 载荷

加密长度是数据的剩余部分。解密长度比加密长度少16字节。载荷通常包含一个或多个Garlic Clove块。格式和其他要求请参见下面的载荷部分。

#### Reply TagSet 的密钥派生函数

从 TagSet 中创建一个或多个标签，TagSet 使用下面的 KDF 进行初始化，使用来自 New Session 消息的 chainKey。

```
// Generate tagset

tagsetKey = HKDF(chainKey, ZEROLEN, "SessionReplyTags", 32)
    tagset_nsr = DH_INITIALIZE(chainKey, tagsetKey)

```
#### 回复密钥段加密内容的密钥派生函数

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
#### 载荷段加密内容的密钥派生函数

这类似于分割后的第一个现有会话消息，但没有单独的标签。此外，我们使用上面的哈希值将有效负载绑定到 NSR 消息。

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
### 注释

可能会发送多个 NSR 消息作为回复，每个消息都带有唯一的临时密钥，具体取决于响应的大小。

Alice 和 Bob 需要为每个 NS 和 NSR 消息使用新的临时密钥。

Alice必须在发送现有会话(ES)消息之前接收到Bob的NSR消息之一，而Bob必须在发送ES消息之前接收到Alice的ES消息。

来自Bob的NSR载荷部分的`chainKey`和`k`被用作初始ES DH Ratchets的输入（双向，参见DH Ratchet KDF）。

Bob 必须只为从 Alice 收到的 ES 消息保留现有会话。任何其他创建的入站和出站会话（用于多个 NSR）都应在收到 Alice 针对给定会话的第一个 ES 消息后立即销毁。

### 1h) 现有会话格式

会话标签（8字节）加密数据和MAC（见下面第3节）

#### 格式

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
#### 载荷

加密长度是数据的剩余部分。解密长度比加密长度少16字节。格式和要求请参见下面的载荷部分。

#### KDF

```
See AEAD section below.

// AEAD parameters for Existing Session payload
k = The 32-byte session key associated with this session tag
n = The message number N in the current chain, as retrieved from the associated Session Tag.
ad = The session tag, 8 bytes
ciphertext = ENCRYPT(k, n, payload, ad)
```
### 2) ECIES-X25519

格式：32字节公钥和私钥，小端序。

### 2a) Elligator2

在标准的 Noise 握手中，每个方向的初始握手消息都以明文传输的临时密钥开始。由于有效的 X25519 密钥可以与随机数据区分开来，中间人可能会将这些消息与以随机会话标签开始的现有会话消息区分开来。在 [NTCP2](/docs/specs/ntcp2/) ([Prop111](/proposals/111-ntcp2/)) 中，我们使用了一个低开销的 XOR 函数，利用带外静态密钥来混淆密钥。然而，这里的威胁模型不同；我们不希望允许任何中间人使用任何手段来确认流量的目的地，或者将初始握手消息与现有会话消息区分开来。

因此，使用 [Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf) 来转换 New Session 和 New Session Reply 消息中的临时密钥，使它们与均匀随机字符串无法区分。

#### 格式

32字节公钥和私钥。编码的密钥采用小端序。

如 [Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf) 中所定义，编码的密钥与 254 个随机位无法区分。我们需要 256 个随机位（32 字节）。因此，编码和解码定义如下：

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
#### 注释

Elligator2使平均密钥生成时间增加一倍，因为有一半的私钥会产生不适合用Elligator2编码的公钥。此外，密钥生成时间是无界的，呈指数分布，因为生成器必须不断重试直到找到合适的密钥对。

这种开销可以通过在单独的线程中提前生成密钥来管理，以维护一个合适密钥的池。

生成器执行 ENCODE_ELG2() 函数来确定适用性。因此，生成器应该存储 ENCODE_ELG2() 的结果，这样就不必再次计算。

此外，不适合的密钥可能会被添加到用于 [NTCP2](/docs/specs/ntcp2/) 的密钥池中，在那里不使用 Elligator2。这样做的安全问题待定。

### 3) AEAD (ChaChaPoly)

使用 ChaCha20 和 Poly1305 的 AEAD，与 [NTCP2](/docs/specs/ntcp2/) 中相同。这对应于 [RFC-7539](https://tools.ietf.org/html/rfc7539)，在 TLS [RFC-7905](https://tools.ietf.org/html/rfc7905) 中也有类似使用。

#### 新会话和新会话回复输入

New Session 消息中 AEAD 块的加密/解密函数输入：

```
k :: 32 byte cipher key
     See New Session and New Session Reply KDFs above.

n :: Counter-based nonce, 12 bytes.
     n = 0

ad :: Associated data, 32 bytes.
      The SHA256 hash of the preceding data, as output from mixHash()

data :: Plaintext data, 0 or more bytes
```
#### 现有会话输入

现有会话消息中 AEAD 块加密/解密函数的输入：

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
#### 加密格式

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
#### 注释

- 由于ChaCha20是流密码，明文无需填充。
  多余的密钥流字节会被丢弃。
- 密码的密钥（256位）通过SHA256 KDF协商确定。每种消息的KDF详细信息在下面的单独章节中说明。
- ChaChaPoly帧具有已知大小，因为它们封装在I2NP数据消息中。
- 对于所有消息，填充都在经过认证的数据帧内部。

#### AEAD 错误处理

所有未通过AEAD验证的接收数据都必须被丢弃。不返回任何响应。

### 4) 棘轮机制

我们仍然像以前一样使用会话标签，但我们使用棘轮来生成它们。会话标签也有一个我们从未实现的重新密钥选项。所以这就像一个双棘轮，但我们从未做过第二个。

在这里我们定义了类似于 Signal 的 Double Ratchet 的机制。会话标签在接收方和发送方都是确定性地、相同地生成的。

通过使用对称密钥/标签棘轮机制，我们消除了发送方存储会话标签的内存使用。我们还消除了发送标签集的带宽消耗。接收方的使用量仍然很大，但我们可以进一步减少它，因为我们将会话标签从32字节缩减到8字节。

我们不使用 Signal 中规定的（可选）头部加密，而是使用会话标签。

通过使用 DH ratchet，我们实现了前向保密性，这在 ElGamal/AES+SessionTags 中从未实现过。

注意：新会话一次性公钥不是 ratchet 的一部分，其唯一功能是加密 Alice 的初始 DH ratchet 密钥。

#### 消息编号

Double Ratchet 通过在每个消息头中包含一个标签来处理丢失或乱序的消息。接收方查找标签的索引，这就是消息编号 N。如果消息包含一个带有 PN 值的消息编号块，接收方可以删除前一个标签集合中高于该值的任何标签，同时保留前一个标签集合中被跳过的标签，以防被跳过的消息稍后到达。

#### 示例实现

我们定义以下数据结构和函数来实现这些棘轮机制。

TAGSET_ENTRY

TAGSET 中的单个条目。

    INDEX

    :   An integer index, starting with 0

    SESSION_TAG

    :   An identifier to go out on the wire, 8 bytes

    SESSION_KEY

    :   A symmetric key, never goes on the wire, 32 bytes

TAGSET

TAGSET_ENTRIES 的集合。

    CREATE(key, n)

    :   Generate a new TAGSET using initial cryptographic key material
        of 32 bytes. The associated session identifier is provided. The
        initial number of of tags to create is specified; this is
        generally 0 or 1 for an outgoing session. LAST_INDEX = -1
        EXTEND(n) is called.

    EXTEND(n)

    :   Generate n more TAGSET_ENTRIES by calling EXTEND() n times.

    EXTEND()

    :   Generate one more TAGSET_ENTRY, unless the maximum number
        SESSION_TAGS have already been generated. If LAST_INDEX is
        greater than or equal to 65535, return. ++ LAST_INDEX Create a
        new TAGSET_ENTRY with the LAST_INDEX value and the calculated
        SESSION_TAG. Calls RATCHET_TAG() and (optionally) RATCHET_KEY().
        For inbound sessions, the calculation of the SESSION_KEY may be
        deferred and calculated in GET_SESSION_KEY(). Calls EXPIRE()

    EXPIRE()

    :   Remove tags and keys that are too old, or if the TAGSET size
        exceeds some limit.

    RATCHET_TAG()

    :   Calculates the next SESSION_TAG based on the last SESSION_TAG.

    RATCHET_KEY()

    :   Calculates the next SESSION_KEY based on the last SESSION_KEY.

    SESSION

    :   The associated session.

    CREATION_TIME

    :   When the TAGSET was created.

    LAST_INDEX

    :   The last TAGSET_ENTRY INDEX generated by EXTEND().

    GET_NEXT_ENTRY()

    :   Used for outgoing sessions only. EXTEND(1) is called if there
        are no remaining TAGSET_ENTRIES. If EXTEND(1) did nothing, the
        max of 65535 TAGSETS have been used, and return an error.
        Returns the next unused TAGSET_ENTRY.

    GET_SESSION_KEY(sessionTag)

    :   Used for incoming sessions only. Returns the TAGSET_ENTRY
        containing the sessionTag. If found, the TAGSET_ENTRY is
        removed. If the SESSION_KEY calculation was deferred, it is
        calculated now. If there are few TAGSET_ENTRIES remaining,
        EXTEND(n) is called.

#### 4a) DH Ratchet

棘轮机制，但速度远不如 Signal。我们将接收密钥的确认与生成新密钥分开处理。在典型使用中，Alice 和 Bob 在新会话中会立即各自棘轮（两次），但之后不会再次棘轮。

请注意，一个棘轮是针对单一方向的，它为该方向生成一个新的会话标签/消息密钥棘轮链。要为两个方向生成密钥，您必须进行两次棘轮操作。

每次生成并发送新密钥时，您都会进行棘轮操作。每次接收新密钥时，您也会进行棘轮操作。

Alice 在创建未绑定出站会话时进行一次 ratchet 操作，她不会创建入站会话（未绑定是不可回复的）。

Bob在创建未绑定入站会话时进行一次棘轮操作，并且不创建相应的出站会话（未绑定是不可回复的）。

Alice 继续向 Bob 发送 New Session (NS) 消息，直到收到 Bob 的 New Session Reply (NSR) 消息之一。然后她使用 NSR 的 Payload Section KDF 结果作为会话棘轮的输入（参见 DH Ratchet KDF），并开始发送 Existing Session (ES) 消息。

对于收到的每个 NS 消息，Bob 创建一个新的入站会话，使用回复载荷段的 KDF 结果作为新的入站和出站 ES DH Ratchet 的输入。

对于每个需要的回复，Bob向Alice发送一个NSR消息，回复内容在载荷中。要求Bob为每个NSR使用新的临时密钥。

Bob必须在其中一个入站会话上收到来自Alice的ES消息，然后才能在对应的出站会话上创建并发送ES消息。

Alice应该使用计时器来接收来自Bob的NSR消息。如果计时器过期，会话应该被移除。

为了避免KCI和/或资源耗尽攻击（攻击者丢弃Bob的NSR回复以让Alice持续发送NS消息），Alice应该在由于定时器超时而重试一定次数后，避免向Bob启动新会话。

Alice 和 Bob 在收到每个 NextKey 块时都会执行一次 DH 棘轮操作。

Alice 和 Bob 在每次 DH ratchet 后都会生成新的标签集 ratchets 和两个对称密钥 ratchets。对于给定方向上的每条新 ES 消息，Alice 和 Bob 都会推进会话标签和对称密钥 ratchets。

初始握手后 DH ratchet 的频率取决于具体实现。虽然协议规定在需要进行 ratchet 之前最多可以传输 65535 条消息，但更频繁的 ratchet（基于消息数量、经过时间或两者）可能会提供额外的安全性。

在绑定会话的最终握手KDF之后，Bob和Alice必须对生成的CipherState运行Noise Split()函数，以便为入站和出站会话创建独立的对称密钥和标签链密钥。

##### 密钥和标签集 ID

密钥和标签集ID号用于标识密钥和标签集。密钥ID在NextKey块中用于标识发送或使用的密钥。标签集ID在ACK块中与消息号一起使用，用于标识被确认的消息。密钥和标签集ID都适用于单一方向的标签集。密钥和标签集ID号必须是连续的。

在每个方向的会话中使用的第一个标签集中，标签集 ID 为 0。由于没有发送 NextKey 块，所以没有密钥 ID。

要开始一个 DH ratchet，发送方传输一个密钥 ID 为 0 的新 NextKey 块。接收方用一个密钥 ID 为 0 的新 NextKey 块进行回复。然后发送方开始使用标签集 ID 为 1 的新标签集。

后续的标签集以类似方式生成。对于在 NextKey 交换后使用的所有标签集，标签集编号为 (1 + Alice 的密钥 ID + Bob 的密钥 ID)。

密钥和标签集ID从0开始并依次递增。最大标签集ID为65535。最大密钥ID为32767。当标签集即将耗尽时，标签集发送方必须启动NextKey交换。当标签集65535即将耗尽时，标签集发送方必须通过发送New Session消息来启动新会话。

在流式传输最大消息大小为1730字节的情况下，假设没有重传，使用单个标签集的理论最大数据传输量为1730 * 65536 ~= 108 MB。由于重传的存在，实际最大值会更低。

在会话必须被丢弃和替换之前，使用所有65536个可用标签集的理论最大数据传输量为64K * 108 MB ~= 6.9 TB。

##### DH RATCHET 消息流

标签集的下一次密钥交换必须由这些标签的发送方（出站标签集的所有者）发起。接收方（入站标签集的所有者）将进行响应。对于应用层的典型 HTTP GET 流量，Bob 将发送更多消息并通过发起密钥交换来首先进行棘轮；下图显示了这一点。当 Alice 进行棘轮时，同样的过程会反向发生。

在 NS/NSR 握手后使用的第一个标签集是标签集 0。当标签集 0 几乎耗尽时，必须在两个方向上交换新密钥以创建标签集 1。之后，新密钥只在一个方向上发送。

为了创建标签集2，标签发送方发送一个新密钥，标签接收方发送其旧密钥的ID作为确认。双方都执行DH交换。

要创建标签集3，标签发送方发送其旧密钥的ID并向标签接收方请求一个新密钥。双方执行DH交换。

后续标签集的生成方式与标签集 2 和 3 相同。标签集编号为 (1 + 发送方密钥 ID + 接收方密钥 ID)。

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
在出站标签集完成 DH ratchet 后，创建新的出站标签集时，应立即使用该标签集，并可删除旧的出站标签集。

当入站标签集的 DH ratchet 完成后，创建新的入站标签集时，接收方应同时监听两个标签集中的标签，并在短时间内（约 3 分钟后）删除旧的标签集。

标签集和密钥ID进展的摘要如下表所示。* 表示生成了新密钥。

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">New Tag Set ID</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Sender key ID</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Rcvr key ID</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">n/a</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">n/a</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 *</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 *</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 *</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 *</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2 *</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2 *</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">...</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">...</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">...</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">65534</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32767 *</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32766</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">65535</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32767</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32767 *</td>
</tr>
</table>
密钥和标签集ID号必须是连续的。

##### DH 初始化 KDF

这是单个方向上 DH_INITIALIZE(rootKey, k) 的定义。它创建一个标签集，以及一个"下一个根密钥"，用于在必要时进行后续的 DH 棘轮操作。

我们在三个地方使用 DH 初始化。首先，我们用它为新会话回复生成标签集。其次，我们用它生成两个标签集，每个方向一个，用于现有会话消息。最后，我们在 DH Ratchet 之后使用它在单个方向生成新的标签集，用于额外的现有会话消息。

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
##### DH RATCHET KDF

这在 NextKey 块中交换新的 DH 密钥之后、在标签集耗尽之前使用。

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
#### 4b) 会话标签棘轮

每条消息都使用棘轮机制，如同 Signal 中一样。会话标签棘轮与对称密钥棘轮同步，但接收方密钥棘轮可能会"滞后"以节省内存。

发送方对于每个传输的消息都会进行一次ratchet操作。不需要存储额外的标签。发送方还必须保持一个计数器来记录'N'，即当前链中消息的消息编号。'N'值包含在发送的消息中。请参见消息编号块定义。

接收方必须按照最大窗口大小向前推进棘轮，并将标签存储在与会话关联的"标签集"中。一旦接收到，存储的标签可以被丢弃，如果没有之前未接收的标签，窗口可以向前推进。接收方应该保持与每个会话标签关联的'N'值，并检查发送消息中的数字是否与此值匹配。请参见消息编号块定义。

##### KDF

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
#### 4c) 对称密钥棘轮

每条消息都使用棘轮机制，如同Signal中一样。每个对称密钥都有一个关联的消息编号和会话标签。会话密钥棘轮与对称标签棘轮是同步的，但接收方密钥棘轮可能会"滞后"以节省内存。

发送方棘轮为每个传输的消息递进一次。无需存储额外的密钥。

当接收方获得一个会话标签时，如果它还没有将对称密钥棘轮推进到相关联的密钥，它必须"追赶"到相关联的密钥。接收方可能会为任何尚未接收的先前标签缓存密钥。一旦接收到，存储的密钥可以被丢弃，如果没有先前未接收的标签，窗口可以向前推进。

为了提高效率，session tag（会话标签）和对称密钥棘轮是分离的，这样session tag棘轮可以领先于对称密钥棘轮运行。这也提供了一些额外的安全性，因为session tag会在网络上传输。

##### KDF

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
### 5) 载荷

这取代了在 ElGamal/AES+SessionTags 规范中定义的 AES 部分格式。

这使用了与 [NTCP2](/docs/specs/ntcp2/) 规范中定义的相同块格式。各个块类型的定义有所不同。

有人担心鼓励实现者共享代码可能导致解析问题。实现者应该仔细考虑共享代码的好处和风险，并确保两种上下文中的排序和有效块规则是不同的。

#### 负载部分解密数据

加密长度是数据的剩余部分。解密长度比加密长度少16字节。支持所有块类型。典型内容包括以下块：

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Payload Block Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type Number</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Block Length</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">DateTime</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Termination (TBD)</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">9 typ.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Options (TBD)</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">21+</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Message Number (TBD)</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">TBD</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Next Key</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3 or 35</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">ACK</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4 typ.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">ACK Request</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">9</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Garlic Clove</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">varies</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Padding</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">254</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">varies</td>
</tr>
</table>
#### 未加密数据

加密帧中包含零个或多个块。每个块包含一个单字节标识符、一个双字节长度和零个或多个字节的数据。

为了扩展性，接收方必须忽略具有未知类型编号的块，并将其视为填充。

加密数据最大为 65535 字节，包括一个 16 字节的认证头，因此未加密数据的最大长度为 65519 字节。

(Poly1305 认证标签未显示)：

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
#### 区块排序规则

在 New Session 消息中，DateTime 块是必需的，并且必须是第一个块。

其他允许的块：

- Garlic Clove (类型 11)
- Options (类型 5)
- Padding (类型 254)

在 New Session Reply 消息中，不需要任何块。

其他允许的区块：

- Garlic Clove (type 11)
- 选项 (type 5)
- 填充 (type 254)

不允许其他块。如果存在填充，它必须是最后一个块。

在现有会话消息中，不需要任何块，顺序也未指定，除了以下要求：

如果存在终止块，它必须是除填充块之外的最后一个块。如果存在填充块，它必须是最后一个块。

在单个帧中可能存在多个 Garlic Clove 块。在单个帧中最多可以有两个 Next Key 块。在单个帧中不允许存在多个 Padding 块。其他块类型在单个帧中可能不会有多个块，但这并不被禁止。

#### 日期时间

过期时间。有助于防止重放攻击。Bob必须使用此时间戳验证消息是否为最近的消息。如果时间有效，Bob必须实现布隆过滤器或其他机制来防止重放攻击。Bob也可以使用更早的重放检测检查来检测重复的临时密钥（Elligator2解码之前或之后），以在解密前检测并丢弃最近重复的NS消息。通常仅包含在New Session消息中。

```
+----+----+----+----+----+----+----+
| 0  |    4    |     timestamp     |
+----+----+----+----+----+----+----+

blk :: 0
size :: 2 bytes, big endian, value = 4
timestamp :: Unix timestamp, unsigned seconds.
             Wraps around in 2106
```
#### Garlic Clove

根据 [I2NP](/docs/specs/i2np/) 规范指定的单个解密的 Garlic Clove，经过修改以移除未使用或冗余的字段。警告：此格式与 ElGamal/AES 的格式有显著差异。每个 clove 都是一个独立的载荷块。Garlic Clove 不能跨块分片或跨 ChaChaPoly 帧分片。

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
       the Garlic Clove section of [I2NP]_.
       Length varies but is typically 1, 33, or 37 bytes

type :: I2NP message type

Message_ID :: 4 byte `Integer` I2NP message ID

Expiration :: 4 bytes, seconds since the epoch
```
注意事项：

- 实现者必须确保在读取块时，格式错误或恶意数据不会导致读取溢出到下一个块。
- 不使用 [I2NP](/docs/specs/i2np/) 中指定的 Clove Set 格式。每个 clove 都包含在自己的块中。
- I2NP 消息头为 9 字节，格式与 [NTCP2](/docs/specs/ntcp2/) 中使用的格式相同。
- 不包含 [I2NP](/docs/specs/i2np/) 中 Garlic Message 定义的 Certificate、Message ID 和 Expiration。
- 不包含 [I2NP](/docs/specs/i2np/) 中 Garlic Clove 定义的 Certificate、Clove ID 和 Expiration。

#### 终止

实现是可选的。丢弃会话。这必须是帧中最后一个非填充块。此会话中将不再发送更多消息。

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
#### 选项

未实现，有待进一步研究。传递更新的选项。选项包括会话的各种参数。更多信息请参见下面的会话标签长度分析部分。

选项块的长度可能是可变的，因为可能存在 more_options。

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
SOTW 是发送方向接收方推荐的接收方入站标签窗口（最大预读取）。RITW 是发送方声明的他计划使用的入站标签窗口（最大预读取）。然后每一方根据某个最小值或最大值或其他计算来设置或调整预读取。

注意事项：

- 希望永远不需要支持非默认的会话标签长度。
- 标签窗口在Signal文档中是MAX_SKIP。

问题：

- 选项协商待定。
- 默认值待定。
- 填充和延迟选项从 NTCP2 复制而来，但这些选项在那里尚未完全实现或研究。

#### 消息编号

实现是可选的。前一个标签集中的长度（发送的消息数量）（PN）。接收方可以立即删除前一个标签集中高于PN的标签。接收方可以在短时间后（例如2分钟）使前一个标签集中小于或等于PN的标签过期。

```
+----+----+----+----+----+
| 6  |  size   |  PN    |
+----+----+----+----+----+

blk :: 6
size :: 2
PN :: 2 bytes big endian. The index of the last tag sent in the previous tag set.
```
注意事项：

- 最大 PN 值为 65535。
- PN 的定义等于 Signal 的定义减一。
  这与 Signal 的做法类似，但在 Signal 中，PN 和 N 在头部。而在这里，它们在加密的消息体中。
- 不要在标签集 0 中发送此块，因为没有之前的标签集。

#### 下一个 DH Ratchet 公钥

下一个 DH ratchet 密钥在载荷中，它是可选的。我们不会每次都进行 ratchet。（这与 signal 不同，在 signal 中它位于头部，并且每次都会发送）

对于第一个棘轮，密钥 ID = 0。

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
- 除非密钥发生变化，否则 ID 不得更改。
- 虽然可能不是严格必需的，但它对调试很有用。
  Signal 不使用 key ID。
- 最大 Key ID 是 32767。
- 在极少数情况下，如果两个方向的标签集同时进行棘轮操作，
  一个帧将包含两个 Next Key 块，一个用于前向密钥，一个用于反向密钥。
- 密钥和标签集 ID 号码必须是顺序的。
- 详细信息请参阅上面的 DH Ratchet 部分。

#### 确认

这仅在收到确认请求块时发送。可能存在多个确认来确认多个消息。

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

- tag set ID 和 N 唯一标识正在被确认的消息。
- 在会话每个方向使用的第一个 tag set 中，tag set ID 为 0。
- 没有发送 NextKey 块，因此没有 key ID。
- 对于 NextKey 交换后使用的所有 tag set，tag set 编号为 (1 + Alice 的 key ID + Bob 的 key ID)。

#### 确认请求

请求带内确认。用于替换 Garlic Clove 中的带外 DeliveryStatus 消息。

如果请求显式确认，当前标签集 ID 和消息编号 (N) 将在确认块中返回。

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
#### 填充

所有填充都在 AEAD 帧内。待办事项：AEAD 内的填充应大致遵守协商的参数。待办事项：Alice 在 NS 消息中发送了她请求的 tx/rx 最小/最大参数。待办事项：Bob 在 NSR 消息中发送了他请求的 tx/rx 最小/最大参数。在数据阶段可能会发送更新的选项。请参阅上面的选项块信息。

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
注释：

- 全零填充是可以的，因为它会被加密。
- 填充策略待定。
- 允许仅填充帧。
- 填充默认为 0-15 字节。
- 参见选项块中的填充参数协商
- 参见选项块中的最小/最大填充参数
- router 对违反协商填充的响应取决于具体实现。

#### 其他区块类型

为了保持前向兼容性，实现应该忽略未知的区块类型。

#### 未来工作

- 填充长度要么基于每条消息决定并估算长度分布，要么应该添加随机延迟。这些对抗措施用于抵御 DPI，因为消息大小会暴露传输协议正在承载 I2P 流量。具体的填充方案是未来工作的一个领域，附录 A 提供了有关该主题的更多信息。

## 典型使用模式

### HTTP GET

这是最典型的使用场景，大多数非HTTP流式使用场景也与此场景相同。发送一个小的初始消息，然后接收回复，随后在两个方向上发送额外的消息。

HTTP GET 请求通常能够容纳在单个 I2NP 消息中。Alice 发送一个小型请求，包含单个新的 Session 消息，并捆绑一个回复 leaseset。Alice 包含立即棘轮到新密钥。包含签名以绑定到目标地址。不请求确认。

Bob 立即进行棘轮操作。

Alice 立即执行棘轮操作。

继续进行这些会话。

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
### HTTP POST

Alice 有三个选项：

1) 仅发送第一条消息（窗口大小 = 1），如 HTTP GET。不

    recommended.
2) 发送至流窗口，但使用相同的 Elligator2 编码

    cleartext public key. All messages contain same next public key
    (ratchet). This will be visible to OBGW/IBEP because they all start
    with the same cleartext. Things proceed as in 1). Not recommended.
3) 推荐实现。发送至流式窗口，但使用一个

    different Elligator2-encoded cleartext public key (session) for
    each. All messages contain same next public key (ratchet). This will
    not be visible to OBGW/IBEP because they all start with different
    cleartext. Bob must recognize that they all contain the same next
    public key, and respond to all with the same ratchet. Alice uses
    that next public key and continues.

选项3消息流程：

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
### 可回复数据报

单个消息，预期有单个回复。可能发送额外的消息或回复。

类似于 HTTP GET，但会话标签窗口大小和生命周期的选项较少。也许不需要请求棘轮。

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
### 多个原始数据报

多个匿名消息，无需回复。

在这种情况下，Alice 请求一个会话，但没有绑定。发送新的会话消息。没有打包回复 LS。打包了一个回复 DSM（这是唯一需要打包 DSM 的用例）。不包含下一个密钥。不请求回复或 ratchet。不发送 ratchet。选项将会话标签窗口设置为零。

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
### 单个原始数据报

一条匿名消息，不需要回复。

发送一次性消息。不捆绑回复 LS 或 DSM。不包含下一个密钥。不请求回复或 ratchet。不发送 ratchet。选项将会话标签窗口设置为零。

```
Alice                           Bob

  One-Time Message (1d)   ------------------->
  with bundled message
  without bundled LS
  without bundled Delivery Status Message
```
### 长期会话

长期存在的会话可以在任何时候进行棘轮操作，或请求棘轮操作，以从该时间点开始维护前向保密性。当会话接近每个会话发送消息的限制（65535条）时，必须进行棘轮操作。

## 实现注意事项

### 防御

与现有的 ElGamal/AES+SessionTag 协议一样，实现必须限制会话标签存储并防范内存耗尽攻击。

一些推荐的策略包括：

- 对存储的会话标签数量设置硬性限制
- 在内存压力下积极过期闲置的入站会话
- 限制绑定到单个远端目标的入站会话数量
- 在内存压力下自适应减少会话标签窗口并删除旧的未使用标签
- 在内存压力下，当被请求时拒绝执行棘轮操作

### 参数

推荐的参数和超时设置：

- NSR tagset 大小：12 tsmin 和 tsmax
- ES tagset 0 大小：tsmin 24，tsmax 160
- ES tagset (1+) 大小：160 tsmin 和 tsmax
- NSR tagset 超时：接收方 3 分钟
- ES tagset 超时：发送方 8 分钟，接收方 10 分钟
- 移除先前 ES tagset 在：3 分钟后
- Tagset 前瞻标签 N：min(tsmax, tsmin + N/4)
- Tagset 后退修剪标签 N：min(tsmax, tsmin + N/4) / 2
- 在标签处发送下一个密钥：4096
- 在 tagset 生命周期后发送下一个密钥：待定
- 如果在以下时间后收到 NS 则替换会话：3 分钟
- 最大时钟偏移：-5 分钟到 +2 分钟
- NS 重放过滤器持续时间：5 分钟
- 填充大小：0-15 字节（其他策略待定）

### 分类

以下是对传入消息进行分类的建议。

#### 仅限 X25519

在仅使用此协议的 tunnel 上，按照当前 ElGamal/AES+SessionTags 的方式进行身份识别：

首先，将初始数据视为会话标签，并查找该会话标签。如果找到，则使用与该会话标签关联的存储数据进行解密。

如果未找到，将初始数据视为 DH 公钥和随机数。执行 DH 操作和指定的 KDF，并尝试解密剩余数据。

#### X25519 共享与 ElGamal/AES+SessionTags

在支持此协议和ElGamal/AES+SessionTags的tunnel上，按如下方式对传入消息进行分类：

由于ElGamal/AES+SessionTags规范中的一个缺陷，AES块没有填充到随机的非16倍数长度。因此，现有会话消息的长度模16总是0，而新会话消息的长度模16总是2（因为ElGamal块长度为514字节）。

如果长度模16不等于0或2，则将初始数据视为会话标签，并查找该会话标签。如果找到，使用与该会话标签关联的存储数据进行解密。

如果未找到，且长度模16不等于0或2，则将初始数据视为DH公钥和随机数。执行DH操作和指定的KDF，并尝试解密剩余数据。（基于相对流量组合和X25519与ElGamal DH操作的相对成本，此步骤可能最后执行）

否则，如果长度对16取模为0，则将初始数据视为ElGamal/AES会话标签，并查找该会话标签。如果找到，则使用与该会话标签关联的存储数据进行解密。

如果未找到，且数据至少为 642（514 + 128）字节长，并且长度模 16 等于 2，则将初始数据视为 ElGamal 块。尝试解密剩余数据。

请注意，如果 ElGamal/AES+SessionTag 规范更新为允许非模16填充，则需要采用不同的处理方式。

### 重传和状态转换

ratchet 层不进行重传，除了两个例外情况外，不使用计时器进行传输。计时器也是 tagset 超时所必需的。

传输计时器仅用于发送 NSR 和在收到包含 ACK 请求的 ES 时进行回复。推荐的超时时间为一秒。在几乎所有情况下，上层协议（数据报或流式传输）会进行回复，强制发送 NSR 或 ES，计时器可能会被取消。如果计时器确实触发，则发送带有 NSR 或 ES 的空载荷。

#### Ratchet 层响应

初始实现依赖于更高层的双向流量。也就是说，这些实现假设反向流量很快就会传输，这将强制在ECIES层进行任何必要的响应。

然而，某些流量可能是单向的或带宽极低，因此没有更高层的流量来产生及时的响应。

接收 NS 和 NSR 消息需要响应；接收 ACK Request 和 Next Key 块也需要响应。

实现应该在收到需要响应的这些消息之一时启动计时器，如果在短时间内（例如1秒）没有发送反向流量，则在ECIES层生成"空"（没有Garlic Clove块）响应。

对于 NS 和 NSR 消息的响应，采用更短的超时时间可能也是合适的，以便尽快将流量转移到高效的 ES 消息上。

#### NSR 的 NS 绑定

在棘轮层，作为Bob，Alice仅通过静态密钥被识别。NS消息经过身份验证（[Noise](https://noiseprotocol.org/noise.html) IK发送方身份验证1）。然而，这对于棘轮层能够向Alice发送任何内容是不够的，因为网络路由需要一个完整的Destination。

在可以发送NSR之前，Alice的完整目标地址必须通过棘轮层或更高层的可应答协议来发现，可以是可应答的[数据报](/docs/specs/datagrams/)或[流](/docs/specs/streaming/)。在找到该目标地址的LeaseSet后，该LeaseSet将包含与NS中相同的静态密钥。

通常，上层协议会响应，通过 Alice 的 Destination Hash 强制进行 Alice 的 Leaseset 的网络数据库查找。该 Leaseset 几乎总能在本地找到，因为 NS 包含了一个 Garlic Clove 块，其中包含了一个 Database Store 消息，该消息包含了 Alice 的 Leaseset。

为了让 Bob 准备好发送 ratchet-layer NSR，并将待处理的会话绑定到 Alice 的 Destination，Bob 应该在处理 NS 负载时"捕获"Destination。如果找到包含 Leaseset 的 Database Store 消息，且其密钥与 NS 中的静态密钥匹配，则待处理的会话现在绑定到该 Destination，Bob 知道在响应计时器过期时向何处发送任何 NSR。这是推荐的实现方式。

另一种设计是维护一个缓存或数据库，将静态密钥映射到目标地址。这种方法的安全性和实用性是进一步研究的主题。

本规范和其他规范都没有严格要求每个 NS 都包含 Alice 的 Leaseset。但是，在实践中，它应该包含。推荐的 ES 标签集发送方超时时间（8 分钟）比最大 Leaseset 超时时间（10 分钟）要短，因此可能存在一个小的时间窗口，在这个窗口内，前一个会话已经过期，Alice 认为 Bob 仍然拥有她的有效 Leaseset，因此不会随新的 NS 发送新的 Leaseset。这是一个需要进一步研究的话题。

#### 多个 NS 消息

如果在上层（数据报或流）发送更多数据（可能是重传）之前没有收到 NSR 响应，Alice 必须使用新的临时密钥组成新的 NS。不要重复使用之前任何 NS 中的临时密钥。Alice 必须维护额外的握手状态和派生的接收标签集，以便接收对任何已发送 NSR 的回复 NSR 消息。

实现可以限制发送的NS消息总数，或者限制NS消息的发送速率，方法是在发送前对高层消息进行排队或丢弃。

在某些情况下，当负载较高时，或在某些攻击场景下，Bob 可能适合对表面上的 NS 消息进行排队、丢弃或限制，而不尝试解密，以避免资源耗尽攻击。

对于每个收到的 NS，Bob 生成一个 NSR outbound tagset，发送一个 NSR，执行 split() 操作，并生成 inbound 和 outbound ES tagsets。然而，Bob 在接收到相应 inbound tagset 上的第一个 ES 消息之前，不会发送任何 ES 消息。之后，Bob 可以丢弃所有其他已接收 NS 或已发送 NSR 的握手状态和 tagsets，或让它们很快过期。不要将 NSR tagsets 用于 ES 消息。

这是一个需要进一步研究的话题，即 Bob 是否可以选择在 NSR 之后立即投机性地发送 ES 消息，甚至在收到 Alice 的第一个 ES 之前。在某些场景和流量模式下，这可能节省大量带宽和 CPU 资源。这种策略可能基于启发式方法，如流量模式、在第一个会话标签集上收到的 ES 百分比或其他数据。

#### 多个 NSR 消息

对于收到的每个 NS 消息，在收到 ES 消息之前，Bob 必须回复一个新的 NSR，这可能是由于发送了更高层的流量，或者是 NSR 发送定时器过期。

每个NSR使用与传入NS对应的握手状态和标签集。Bob必须维护所有接收到的NS消息的握手状态和标签集，直到收到ES消息为止。

实现可以限制发送的NSR消息总数，或限制NSR消息发送速率，可以通过在发送前对高层消息进行排队或丢弃来实现。这些限制可以在由传入的NS消息引起时应用，也可以在有额外的高层出站流量时应用。

在某些情况下，当负载很高时，或在某些攻击场景下，Alice 可能会适当地对 NSR 消息进行队列、丢弃或限制而不尝试解密，以避免资源耗尽攻击。这些限制可能是跨所有会话的总限制、每个会话的限制，或者两者兼而有之。

一旦 Alice 收到 NSR，Alice 执行 split() 来派生 ES 会话密钥。Alice 应该设置一个计时器，如果上层没有发送任何流量，通常在一秒钟内发送一个空的 ES 消息。

其他入站NSR标签集可能很快被移除或允许过期，但Alice应该保留它们一小段时间，以解密任何其他接收到的NSR消息。

### 重放攻击防护

Bob必须实现布隆过滤器或其他机制来防止NS重放攻击（如果包含的DateTime是最近的），并拒绝DateTime过旧的NS消息。Bob也可以使用更早的重放检测检查来检查重复的临时密钥（在Elligator2解码前或后），以便在解密前检测并丢弃最近的重复NS消息。

NSR 和 ES 消息具有固有的重放防护，因为会话标签是一次性使用的。

如果router实现基于I2NP消息ID的路由器级布隆过滤器，garlic消息还具有重放攻击防护功能。

## 相关更改

来自 ECIES 目标的数据库查找：参见 [Prop154](/proposals/154-ratchet/)，现已纳入 [I2NP](/docs/specs/i2np/) 用于 0.9.46 版本发布。

此规范要求 LS2 支持以便在 leaseset 中发布 X25519 公钥。不需要对 [I2NP](/docs/specs/i2np/) 中的 LS2 规范进行任何更改。所有支持都是在 [Prop123](/proposals/123-new-netdb-entries/) 中设计、规范和实现的，已在 0.9.38 版本中实现。

此规范要求在 I2CP 选项中设置一个属性来启用。所有支持都已在 [Prop123](/proposals/123-new-netdb-entries/) 中设计、规定和实现，该提案在 0.9.38 版本中实现。

启用 ECIES 所需的选项是 I2CP、BOB、SAM 或 i2ptunnel 的单个 I2CP 属性。

典型值为 i2cp.leaseSetEncType=4 表示仅使用 ECIES，或 i2cp.leaseSetEncType=4,0 表示 ECIES 和 ElGamal 双密钥。

## 兼容性

任何支持带有双密钥的 LS2 的 router（0.9.38 或更高版本）都应该支持连接到带有双密钥的目标地址。

仅ECIES目标需要大多数floodfill更新到0.9.46版本才能获得加密的查找回复。请参阅[Prop154](/proposals/154-ratchet/)。

仅支持 ECIES 的目标地址只能与其他仅支持 ECIES 或双密钥的目标地址连接。

## 参考资料

- [Common](/docs/specs/common-structures/)
- [CRYPTO-ELG](/docs/specs/cryptography/#elgamal)
- [Datagrams](/docs/specs/datagrams/)
- [ECIES-HYBRID](/docs/specs/ecies-hybrid/)
- [ElG-AES](/docs/specs/elgamal-aes/)
- [Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf) - 另见 [Elligator article](https://www.imperialviolet.org/2013/12/25/elligator.html) 和 OBFS4 代码
- [GARLICSPEC](/docs/overview/garlic-routing/)
- [I2CP](/docs/specs/i2cp/)
- [I2NP](/docs/specs/i2np/)
- [NOISE](https://noiseprotocol.org/noise.html)
- [NTCP2](/docs/specs/ntcp2/)
- [Prop111](/proposals/111-ntcp2/)
- [Prop123](/proposals/123-new-netdb-entries/)
- [Prop142](/proposals/142-ecies-template/)
- [Prop144](/proposals/144-ecies-x25519/)
- [Prop145](/proposals/145-ecies-ecdh-aes/)
- [Prop152](/proposals/152-ecies-config/)
- [Prop153](/proposals/153-chacha20-layer/)
- [Prop154](/proposals/154-ratchet/)
- [RFC-2104](https://tools.ietf.org/html/rfc2104)
- [RFC-4880-S5.1](https://tools.ietf.org/html/rfc4880#section-5.1)
- [RFC-5869](https://tools.ietf.org/html/rfc5869)
- [RFC-7539](https://tools.ietf.org/html/rfc7539)
- [RFC-7748](https://tools.ietf.org/html/rfc7748)
- [RFC-7905](https://tools.ietf.org/html/rfc7905)
- [Signal](https://signal.org/docs/specifications/doubleratchet/)
- [SSU](/docs/transport/ssu/)
- [SSU2](/docs/specs/ssu2/)
- [STS](https://en.wikipedia.org/wiki/Station-to-Station_protocol) - Diffie, W.; van Oorschot P. C.; Wiener M. J., Authentication and Authenticated Key Exchanges
- [Streaming](/docs/specs/streaming/)
