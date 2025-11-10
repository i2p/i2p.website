```markdown
---
title: "ECIES-X25519-AEAD-Ratchet"
number: "144"
author: "zzz, chisana, orignal"
created: "2018-11-22"
lastupdated: "2025-03-05"
status: "Closed"
thread: "http://zzz.i2p/topics/2639"
target: "0.9.46"
implementedin: "0.9.46"
---

## 注意
网络部署和测试正在进行中。
可能会有小幅修订。
请参阅 [SPEC]_ 了解官方规范。

截至 0.9.46，以下功能尚未实现：

- MessageNumbers, Options, 和 Termination 块
- 协议层响应
- 零静态密钥
- 多播

## 概述

这是一个关于自 I2P 开始以来第一个新的端到端加密类型的提案，它旨在取代 ElGamal/AES+SessionTags [Elg-AES]_。

该提案依赖于以下先前的工作：

- 通用结构规范 [Common]_
- 包括 LS2 的 [I2NP]_ 规范
- ElGamal/AES+Session Tags [Elg-AES]_
- http://zzz.i2p/topics/1768 新的非对称加密概述
- 底层加密概述 [CRYPTO-ELG]_
- ECIES http://zzz.i2p/topics/2418
- [NTCP2]_ [Prop111]_
- 123 新 netDB 条目
- 142 新加密模板
- [Noise]_ 协议
- [Signal]_ 双密码算法

目标是支持新的加密，用于端到端、目的地到目的地的通信。

设计将采用 Noise 握手和数据阶段结合 Signal 的双密码算法。

本提案中对 Signal 和 Noise 的所有引用仅用于背景信息。
了解或实现此提案不需要 Signal 和 Noise 协议的知识。

### 当前 ElGamal 的用途

回顾一下，以下数据结构中可能会找到 256 字节的 ElGamal 公钥。
参考通用结构规范。

- 在路由器身份中
  这是路由器的加密密钥。

- 在目的地中
  目的地的公钥曾用于旧的 i2cp 到 i2cp 的加密，该加密在 0.6 版本中被禁用，目前未被使用，除用于 LeaseSet 加密的 IV（不推荐使用）。
  使用的是 LeaseSet 中的公钥。

- 在 LeaseSet 中
  这是目的地的加密密钥。

- 在 LS2 中
  这是目的地的加密密钥。

### 密钥证书中的 EncTypes

回顾一下，当我们添加对签名类型的支持时，我们还添加了对加密类型的支持。
在目的地和路由器身份中的加密类型字段始终为零。
是否更改尚待决定。
参考通用结构规范 [Common]_。

### 非对称加密的用途

回顾一下，我们使用 ElGamal 用于：

1) 隧道生成消息（密钥在 RouterIdentity 中）
   此提案未涵盖如何替换。
   请参阅提案 152 [Prop152]_。

2) 路由器到路由器的 netdb 和其他 I2NP 消息加密（密钥在 RouterIdentity 中）
   取决于本提案。
   需要一个关于 1) 的提案，或者将密钥放入 RI 选项中。

3) 客户端端到端的 ElGamal+AES/SessionTag（密钥在 LeaseSet 中，目的地密钥未使用）
   本提案中已经涵盖了替换。

4) 对于 NTCP1 和 SSU 的临时 DH
   本提案不涵盖如何替换。
   请参阅 NTCP2 提案 111。
   当前没有针对 SSU2 的提案。

### 目标

- 向后兼容
- 需要并建立在 LS2（提案 123）的基础上
- 利用为 NTCP2（提案 111）添加的新加密或原语
- 无需支持新的加密或原语
- 保持加密和签名的解耦；支持所有当前和未来版本
- 启用目的地的新加密
- 为路由器启用新加密，但仅适用于大蒜消息 - 隧道构建将是一个单独的提案
- 不破坏依赖于 32 字节二进制目的地哈希的任何东西，例如 bittorrent
- 通过临时静态 DH 维护 0-RTT 消息传递
- 不需要在此协议层缓存/排队消息；继续支持不等待响应的无限制消息传递
- 在 1 RTT 后升级到临时临时 DH
- 维持乱序消息的处理
- 保持 256 位的安全性
- 添加前向保密
- 添加身份验证（AEAD）
- 比 ElGamal 更具 CPU 效率
- 不依赖 Java jbigi 提高 DH 效率
- 将 DH 操作最小化
- 比 ElGamal 更具带宽效率（514 字节的 ElGamal 块）
- 如果需要，支持在同一个隧道上同时使用新旧加密
- 接收者能够有效地区分从同一隧道下来的是新的还是旧的加密
- 其他人无法区别新的、旧的或未来的加密
- 消除新旧会话长度分类（支持填充）
- 不需要新的 I2NP 消息
- 用 AEAD 替换 AES 负载中的 SHA-256 校验和
- 支持发送和接收会话的绑定，以便可以在协议内进行确认，而不仅仅是带外。
  这还将立即允许回复具有前向保密性。
- 启用某些消息的端到端加密（例如 RouterInfo 存储），我们目前由于 CPU 负担过重而没有这样做。
- 不改变 I2NP Garlic Message 或 Garlic Message Delivery Instructions 格式。
- 消除 Garlic Clove Set 和 Clove 格式中未使用或冗余的字段。

消除会话标签的几个问题，包括：

- 在第一次回复之前无法使用 AES
- 如果假设标签传递则不可靠而且可能停顿
- 特别是在首次传递时带宽效率低
- 存储标签的巨大空间效率低
- 传递标签的巨大带宽开销
- 高度复杂，难以实现
- 难以为各种用例进行调整（流媒体与数据报，服务器与客户端，高带宽与低带宽）
- 由于标签传递导致的内存耗尽漏洞

### 非目标 / 不在范围之内

- LS2 格式更改（提案 123 完成）
- 新的 DHT 旋转算法或共享的随机生成
- 建筑隧道的新加密。
  请参阅提案 152 [Prop152]_。
- 隧道层加密的新加密。
  请参阅提案 153 [Prop153]_。
- I2NP DLM / DSM / DSRM 消息的加密、传输和接收方法。
  不改变。
- 不支持 LS1 到 LS2 或 ElGamal/AES 到此提案的通信。
  本提案是一个双向协议。
  目的地可以通过发布两个使用相同隧道的 leaseset 来处理向后兼容，或者将两种加密类型都放入 LS2 中。
- 威胁模型变化
- 实施细节在此不讨论，由各项目自行决定。
- （乐观地）添加扩展或钩子以支持多播

### 理由

ElGamal/AES+SessionTag 大约是我们唯一的端到端协议，大约 15 年来几乎没有对协议进行修改。
现在，已经有更快的密码学原语。
我们需要加强协议的安全性。
我们还开发了启发式策略和解决方法，以最小化协议的内存和带宽开销，但这些策略脆弱，难以调整，使协议更容易出错，导致会话丢失。

在大约相同的时间段内，ElGamal/AES+SessionTag 规范和相关文档已经描述了传递会话标签是多么昂贵，并建议用“同步 PRNG”替换会话标签传递。
同步 PRNG 确定性地在两端生成相同的标签，来源于一个共同的种子。
同步 PRNG 也可以称为“棘轮”。
该提案（最终）指定了该棘轮机制，并消除了标签传递。

通过使用一个棘轮（一个同步 PRNG）来生成会话标签，我们消除了在新会话消息和后续消息中发送会话标签的开销。对于一个典型的标签集的 32 个标签来说，这就是 1KB。
这也消除了发送方存储会话标签的需求，从而将存储要求减半。

需要一个完整的双向握手，类似于 Noise IK 模式来避免密钥泄漏模拟攻击（KCI）攻击。
请参阅[NOISE]_中的 Noise “Payload Security Properties” 表。
有关 KCI 的更多信息，请参阅论文 https://www.usenix.org/system/files/conference/woot15/woot15-paper-hlauschek.pdf

### 威胁模型

威胁模型与 NTCP2（提案 111）稍有不同。
中间人节点是 OBEP 和 IBGW，并假设通过与洪泛节点合作，可以全面看到当前或历史的全球 NetDB。

目标是防止中间人将流量分类为新消息和现有会话消息，或者将流量分类为新加密与旧加密。

## 详细建议

本提案定义了一种新的端到端协议，用于取代 ElGamal/AES+SessionTags。
设计将采用 Noise 握手和数据阶段结合 Signal 的双密码算法。

### 加密设计概要

协议有五个部分需要重新设计：

- 1) 新的会话和现有会话容器格式被新的格式替换。
- 2) ElGamal（256 字节公钥，128 字节私钥）被替换为 ECIES-X25519（32 字节公钥和私钥）
- 3) AES 被替换为 AEAD_ChaCha20_Poly1305（简称 ChaChaPoly）
- 4) 会话标签将被棘轮所取代，实质上这是一种加密、同步的 PRNG。
- 5) 如在 ElGamal/AES+SessionTags 规范中定义的 AES 负载，替换为类似于 NTCP2 中的块格式。

下面的每个更改都有自己的章节。

### I2P 的新密码原语
现有的 I2P 路由器实现将需要实现以下不需要的标准密码原语，以用于当前的 I2P 协议：

- ECIES（但这实质上是 X25519）
- Elligator2

尚未实施 [NTCP2]_([Prop111]_) 的现有 I2P 路由器实现也将需要实现：

- X25519 密钥生成和 DH
- AEAD_ChaCha20_Poly1305（简称 ChaChaPoly）
- HKDF

### 加密类型

加密类型（用于 LS2 中）是 4。
这表示一个小端 32 字节的 X25519 公钥，以及此处指定的端到端协议。

加密类型 0 是 ElGamal。
加密类型 1-3 保留用于 ECIES-ECDH-AES-SessionTag，请参阅提案 145 [Prop145]_。

### Noise 协议框架

该提案提供基于 Noise 协议框架的需求
[NOISE]_（Revision 34, 2018-07-11）。
Noise 的特性类似于站对站协议
[STS]_，它是 [SSU]_ 协议的基础。 在 Noise 中，Alice
是发起者，Bob 是响应者。

该提案基于 Noise 协议 Noise_IK_25519_ChaChaPoly_SHA256。
（实际的初始密钥派生函数的标识符
是 "Noise_IKelg2_25519_ChaChaPoly_SHA256"
表示 I2P 扩展 - 参见下文的 KDF 1 节）
此 Noise 协议使用以下原语：

- 交互式握手模式：IK
  Alice 立即将其静态密钥传输给 Bob（I）
  Alice 已经知道 Bob 的静态密钥（K）

- 单向握手模式：N
  Alice 不将其静态密钥传输给 Bob（N）

- DH 函数：X25519
  X25519 DH，密钥长度为 32 字节，规范见 [RFC-7748]_。

- 密码函数：ChaChaPoly
  AEAD_CHACHA20_POLY1305，规范见 [RFC-7539]_ 第 2.8 节。
  12 字节的 nonce，前 4 个字节设置为零。
  与 [NTCP2]_ 中相同。

- 哈希函数：SHA256
  标准 32 字节哈希，在 I2P 中已经广泛使用。

对框架的补充
```````````````````````````

该提案定义了以下增强 Noise_IK_25519_ChaChaPoly_SHA256。 这些通常遵循
[NOISE]_ 第 13 节中的指南。

1) 用 [Elligator2]_ 编码的明文临时密钥。

2) 回复以明文标签作为前缀。

3) 消息 1、2 和数据阶段定义的有效负载格式。
   当然，这在 Noise 中没有定义。

所有消息都包括一个 [I2NP]_ 大蒜消息头。
数据阶段使用类似但与 Noise 数据阶段不兼容的加密。

### 握手模式

握手使用 [Noise]_ 握手模式。

使用以下字母映射：

- e = 一次性临时密钥
- s = 静态密钥
- p = 消息有效载荷

一次性和不绑定的会话类似于 Noise N 模式。

.. raw:: html

  {% highlight lang='dataspec' %}
<- s
  ...
  e es p ->

{% endhighlight %}


绑定会话类似于 Noise IK 模式。

.. raw:: html

  {% highlight lang='dataspec' %}
<- s
  ...
  e es s ss p ->
  <- tag e ee se
  <- p
  p ->

{% endhighlight %}

### 会话

当前的 ElGamal/AES+SessionTag 协议是单向的。
在这一层，接收方不知道消息来自哪里。
出站和入站会话没有关联。
确认是使用在 clove 中包裹在大蒜消息中的 DeliveryStatusMessage 带外（out-of-band）的。

单向协议中存在相当大的低效。
所有回复也必须使用一个昂贵的 '新会话' 消息。
这导致更高的带宽、CPU 和内存使用。

单向协议中也存在安全弱点。
所有会话都基于临时静态 DH。
没有返回路径，Bob 无法将其静态密钥“棘轮”到临时密钥。
不知道消息来自何处，也无法使用
接收到的临时密钥用于出站消息，
因此初始回复也使用临时静态 DH。

对于本提案，我们定义了两种方法来创建一个双向协议——“配对”和“绑定”。
这些机制提供了提高的效率和安全性。

会话上下文
``````````````

与 ElGamal/AES+SessionTags 一样，所有入站和出站会话
必须在给定的上下文中，或者是路由器的上下文或特定本地目的地的上下文。
在 Java I2P 中，此上下文称为会话密钥管理器。

会话不得在上下文之间共享，因为这会
允许各个本地目的地或本地目的地和路由器之间的关联。

当支持 ElGamal/AES+SessionTags 和本提案的给定目的地时，可以在一个上下文中共享这两种类型的会话。
请参阅下面的第 1c) 节。

配对入站和出站会话
````````````````````````````````````

当在源地（Alice）创建出站会话时，
除非没有期望的回复（例如原始数据报）否则，总是创建一个新的入站会话并将其与出站会话配对。

当在接收器（Bob）创建入站会话时，
通常新入站会话会与一个新的出站会话配对，除非没有请求的回复（例如原始数据报）。

如果请求了一个回复并绑定到远程目的地或路由器，
那个新的出站会话被绑定到那个目的地或路由器，并取代了到那个目的地或路由器的任何先前的出站会话。

入站和出站会话的配对提供了一个双向协议，
使得能够对 DH 密钥进行棘轮。

绑定会话和目的地
``````````````````````````````````

到一个给定目的地或路由器只能有一个出站会话。
来自某一给定目的地或路由器的当前入站会话可能有几个。
通常，当一个新的入站会话被创建时，并接收到该会话上的流量（也就是确认），任何其他会话将被标记
以相对较快的速度过期，在大约一分钟左右。
检查先前发送的消息（PN）值，如果先前入站会话中没有未收到的消息（在窗口大小内），
可以立即删除先前的会话。

当在发起者（Alice）创建出站会话时，
它被绑定到远程目的地（Bob），
任何配对的入站会话也将被绑定到远程目的地。
当会话棘轮时，它们继续绑定到远程目的地。

当在接收器（Bob）创建入站会话时，
他可以选择绑定到远程目的地。
如果 Alice 在新会话消息中包含绑定信息（她的静态密钥），
会话将绑定到该目的地，
并且将创建一个出站会话并绑定到相同的目的地。
当会话棘轮时，它们继续绑定到远程目的地。

绑定和配对的好处
````````````````````````````````

对于常见的流媒体情况，我们期望 Alice 和 Bob 使用协议如下：

- Alice 配对她的新出站会话到一个新的入站会话，均绑定到远程目的地（Bob）。
- Alice 在发送到 Bob 的新会话消息中包括绑定信息和签名。
- Bob 配对他的新入站会话到一个新的出站会话，均绑定到远程目的地（Alice）。
- Bob 以一个棘轮到一个新的 DH 密钥回复（确认） Alice。
- Alice 使用 Bob 的新密钥棘轮到一个新的出站会话，配对到现有入站会话。

通过将一个入站会话绑定到远程目的地，并将入站会话
配对到绑定到相同目的地的出站会话，我们实现了两个主要好处：

1) Bob 到 Alice 的初始回复使用临时临时 DH

2) 在 Alice 接收到 Bob 的回复并进行棘轮后，Alice 到 Bob 的所有后续消息
使用临时临时 DH。

消息确认
````````````

在 ElGamal/AES+SessionTags 中，当 LeaseSet 作为一个大蒜块一起传送时，
或标签被传递，发送路由器请求一个确认。
这是一个包含 DeliveryStatus 消息的单独的大蒜块。
为了增加安全性，DeliveryStatus 消息被包裹在一个大蒜消息中。
从协议的角度来看，此机制是带外的。

在新协议中，由于入站和出站会话是配对的，
我们可以在带内进行确认。不需要单独的块。

一个显式确认简单地是一个没有 I2NP 块的现有会话消息。
然而，在大多数情况下，可以避免显式确认，因为有逆向流量。
实现可能需要等待短时间（可能百毫秒）
再发送显式确认，以给予流媒体或应用层时间进行响应。

实现还需要将任何 ACK 的发送推迟到
I2NP 块被处理完后，因为大蒜消息可能包含一个带有
一组租约的 Database Store Message。
一个最近的租约集将是路由 ACK 所需的，
而远程目的地（包含在租约集中）将是验证绑定静态密钥所需的。

会话超时
``````````

出站会话应该总是先于入站会话超时。
当一个出站会话到期，以及创建新的一个时，将创建一个配对入站
会话。本来有一个旧的入站会话，
它将被允许过期。

### 多播

待定

### 定义
我们定义了以下与使用的密码构建块相对应的函数。

ZEROLEN
    零长度字节数组

CSRNG(n)
    来自加密安全随机数生成器的 n 字节输出。

H(p, d)
    采用个性化字符串 p 和数据 d 的 SHA-256 哈希函数，并
    产生长度为 32 字节的输出。
    如在 [NOISE]_ 中定义。
    || 表示附加。

    使用 SHA-256，如下所示：

        H(p, d) := SHA-256(p || d)

MixHash(d)
    接受前一个哈希 h 和新数据 d 的 SHA-256 哈希函数，
    生成一个长度为 32 字节的输出。
    || 表示附加。

    使用 SHA-256，如下所示：

        MixHash(d) := h = SHA-256(h || d)

STREAM
    如在 [RFC-7539]_ 中指定的 ChaCha20/Poly1305 AEAD。
    S_KEY_LEN = 32 和 S_IV_LEN = 12。

    ENCRYPT(k, n, plaintext, ad)
        使用加密密钥 k 和 nonce n （对于密钥 k 必须唯一）加密明文。
        关联数据 ad 是可选的。
        返回一个大小为明文 + 16 字节的 HMAC 的密文。

        如果密钥是秘密的，整个密文必须与随机数据不可区分。

    DECRYPT(k, n, ciphertext, ad)
        使用加密密钥 k 和 nonce n 解密密文。
        关联数据 ad 是可选的。
        返回明文。

DH
    X25519 公钥协商系统。32 字节的私钥，32 字节的公钥，生成32 字节的输出。
    它有以下函数：

    GENERATE_PRIVATE()
        生成一个新的私钥。

    DERIVE_PUBLIC(privkey)
        返回与给定私钥对应的公钥。

    GENERATE_PRIVATE_ELG2()
        生成一个可编码为 Elligator2 的公钥的新私钥。
        需要丢弃不合适的随机生成的私钥中的一半。

    ENCODE_ELG2(pubkey)
        返回与给定公钥（反向映射）对应的 Elligator2 编码的公钥。
        编码的密钥是小端。
        编码的密钥必须是 256 位的，与随机数据不可区分。
        请参阅下面 Elligator2 部分的规格。

    DECODE_ELG2(pubkey)
        返回与给定 Elligator2 编码的公钥对应的公钥。
        请参阅下面 Elligator2 部分的规格。

    DH(privkey, pubkey)
        使用给定的私钥和公钥生成一个共享的秘密。

HKDF(salt, ikm, info, n)
    一个密码密钥派生函数，接收一些输入密钥材料 ikm（应具有良好的熵，但不要求是均匀随机字符串），一个长度为 32 字节的 salt 和一个上下文特定的 'info' 值，生成一个 n 字节的输出，适用于用作密钥材料。

    使用 HKDF 如 [RFC-5869]_ 中指定的，使用 HMAC 哈希函数 SHA-256
    如 [RFC-2104]_ 中指定的。这意味着 SALT_LEN 最大为 32 字节。

MixKey(d)
    使用 HKDF() 和一个先前的 chainKey 和新的数据 d，并
    设置新的 chainKey 和 k。
    如在 [NOISE]_ 中定义。

    使用 HKDF，如下所示：

        MixKey(d) := output = HKDF(chainKey, d, "", 64)
                     chainKey = output[0:31]
                     k = output[32:63]

### 1) 消息格式

当前消息格式回顾
````````````````````````

如 [I2NP]_ 中指定的 Garlic Message 如下。
作为一个设计目标，无法区分中间跳的旧加密消息和新加密消息，
此格式不能更改，即使长度字段是多余的。
使用完整的 16 字节标头显示格式，尽管
实际标头可能根据使用的传输具有不同的格式。

解密后数据包含一系列大蒜块和其他
数据，也称为 Clove Set。

有关详细信息和完整规范，请参阅 [I2NP]_。

.. raw:: html

  {% highlight lang='dataspec' %}
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

{% endhighlight %}

加密数据格式回顾
`````````````````````````
当前消息格式，已使用超过 15 年，
是 ElGamal/AES+SessionTags。
在 ElGamal/AES+SessionTags 中，有两种消息格式：

1) 新会话：
- 514 字节的 ElGamal 块
- AES 块（最小 128 字节，16 的倍数）

2) 现有会话：
- 32 字节的会话标签
- AES 块（最小 128 字节，16 的倍数）

最小填充到 128 是在 Java I2P 中实现但在接收端不强制执行。

这些消息封装在一个 I2NP 大蒜消息中，包含
一个长度字段，因此已知长度。

请注意，未定义填充为非 mod-16 长度，
因此新会话始终是（mod 16 == 2），
而现有会话始终是（mod 16 == 0）。
我们需要修复这个问题。

接收器首先尝试将前 32 字节作为会话标签进行查找。
如果找到，他会解密 AES 块。
如果没有找到，并且数据至少为（514+16）长，他会尝试解密 ElGamal 块，
如果成功，则解密 AES 块。

新会话标签和与 Signal 的比较
````````````````````````````````````````

在 Signal Double Ratchet 中，头部包含：

- DH: 当前的棘轮公钥
- PN: 以前的链消息长度
- N: 消息编号

Signal 的“发送链”大致相当于我们的标签集。
通过使用会话标签，我们可以消除大部分内容。

在新会话中，我们只将公钥放入未加密的头部中。

在现有会话中，我们使用会话标签作为头部。
会话标签与当前棘轮公钥和消息编号相关联。

在新旧会话中，PN 和 N 位于加密的正文中。

在 Signal 中，事情不断地在进行棘轮。一个新的 DH 公钥需要
接收者来进行棘轮并发送一个新的公钥回去，这也充当
接收到的公钥的确认。
这对我们来说将是太多的 DH 操作。
因此，我们将接收到的密钥的确认和传输新的公钥分开。
任何使用会话标签的消息都从新的 DH 公钥生成，构成一个 ACK。
我们只有在希望更换密钥时才传输新的公钥。

在进行 DH 操作之前，消息的最大数量为 65535。

传递会话密钥时，我们从中派生“标签集”，而不是必须传递会话标签。
一个标签集最多可以有 65536 个标签。
但是，接收器应该实现一个“预视”策略，而不是一次生成所有可能的标签。
最多只生成最后接收到的好标签数量的 N 个标签。
N 最多可能为 128，但 32 或更少可能是更好的选择。

### 1a) 新会话格式

新会话一次性公钥（32 字节）
加密数据和 MAC（剩余字节）

新会话消息可以包含发送者的静态公钥。
如果包含了静态密钥，则反向会话绑定到该密钥。
如果期望有回复，即用于流式数据和可回复的数据报，则应包含静态密钥。
对于原始数据报不应包含。

新会话消息类似于单向 Noise [NOISE]_ 模式
“N”（如果不发送静态密钥），
或双向模式“IK”（如果发送静态密钥）。

### 1b) 新会话格式（带绑定）

长度为 96 + 负载长度。
加密格式：

.. raw:: html

  {% highlight lang='dataspec' %}
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

{% endhighlight %}

新会话临时密钥
`````````````````````````

临时密钥为 32 字节，用 Elligator2 编码。
该密钥从不重复使用；每条消息生成新密钥，包括重传。

静态密钥
``````````

解密时，Alice 的 X25519 静态密钥，32 字节。

有效负载
`````````

加密长度是数据的其余部分。
解密后的长度比加密长度少 16。
负载必须包含一个 DateTime 块并且通常包含一个或多个大蒜块。
请参阅下面的有效负载部分以了解格式和其他要求。

### 1c) 新会话格式（不带绑定）

如果不需要回复，则不发送静态密钥。

长度为 96 + 负载长度。
加密格式：

.. raw:: html

  {% highlight lang='dataspec' %}
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

{% endhighlight %}

新会话临时密钥
`````````````````````````

Alice 的临时密钥。
临时密钥为 32 字节，用 Elligator2 编码，小端。
该密钥从不重复使用；每条消息生成新密钥，包括重传。

标志部分解密数据
````````````````````````````

标志部分没有内容。
始终为 32 字节，因为它必须是与绑定会话的静态密钥相同的长度。
Bob 通过测试 32 个字节是否全为零来确定它是静态密钥还是标志部分。

TODO 这里是否需要任何标志？

有效负载
`````````

加密长度是数据的其余部分。
解密后的长度比加密长度少 16。
负载必须包含一个 DateTime 块并且通常包含一个或多个大蒜块。
请参阅下面的有效负载部分以了解格式和其他要求。

### 1d) 一次性格式（无绑定或会话）

如果预计只发送一条消息，则无需会话设置或静态密钥。

长度为 96 + 负载长度。
加密格式：

.. raw:: html

  {% highlight lang='dataspec' %}
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

{% endhighlight %}

新会话一次性密钥
`````````````````````````

一次性密钥为 32 字节，用 Elligator2 编码，小端。
该密钥从不重复使用；每条消息生成新密钥，包括重传。

标志部分解密数据
````````````````````````````

标志部分没有内容。
始终为 32 字节，因为它必须是与绑定会话的静态密钥相同的长度。
Bob 通过测试 32 个字节是否全为零来确定它是静态密钥还是标志部分。

TODO 这里是否需要任何标志？

.. raw:: html

  {% highlight lang='dataspec' %}
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

{% endhighlight %}

有效负载
`````````

加密长度是数据的其余部分。
解密后的长度比加密长度少 16。
负载必须包含一个 DateTime 块并且通常包含一个或多个大蒜块。
请参阅下面的有效负载部分以了解格式和其他要求。

### 1f) 新会话消息的 KDF

初始 ChainKey 的 KDF
````````````````````````

这是标准 [NOISE]_ 的 IK，带有一个修改的协议名称。
请注意，我们对绑定会话（绑定会话）的 IK 模式和不绑定的会话（unbound 会话）的模式使用相同的初始化器。

协议名称被修改的原因有两个。
首先，表明临时密钥用 Elligator2 编码，
其次，说明在第二个消息之前调用 MixHash() 来混合标签值。

.. raw:: html

  {% highlight lang='text' %}
这是 "e" 消息模式：

  // 定义 protocol_name。
  设置 protocol_name = "Noise_IKelg2+hs2_25519_ChaChaPoly_SHA256"
   (40 字节，US-ASCII 编码，没有 NULL 终止)。

  // 定义哈希 h = 32 字节
  h = SHA256(protocol_name);

  定义 ck = 32 字节链接密钥。将 h 数据复制到 ck。
  设置 chainKey = h

  // MixHash(null prologue)
  h = SHA256(h);

  // 到此为止，Alice 为所有传出连接预先计算

{% endhighlight %}

用于标志/静态键部分加密内容的 KDF
```````````````````````````````````````````````````

.. raw:: html

  {% highlight lang='text' %}
这是 "e" 消息模式：

  // Bob 的 X25519 静态密钥
  // bpk 在 leaseset 中发布
  bsk = GENERATE_PRIVATE()
  bpk = DERIVE_PUBLIC(bsk)

  // Bob 的静态公钥
  // MixHash(bpk)
  // || 表示附加
  h = SHA256(h || bpk);

  // 到此为止，Bob 为所有传入连接预先计算

  // Alice 的 X25519 临时密钥
  aesk = GENERATE_PRIVATE_ELG2()
  aepk = DERIVE_PUBLIC(aesk)

  // Alice 临时公钥
  // MixHash(aepk)
  // || 表示附加
  h = SHA256(h || aepk);

  // h 用作新会话消息中 AEAD 的关联数据
  // 保留用于新会话回复 KDF 的哈希 h
  // eapk 在新会话消息的开头以明文形式发送
  elg2_aepk = ENCODE_ELG2(aepk)
  // Bob 解码时
  aepk = DECODE_ELG2(elg2_aepk)

  "e" 消息模式结束。

  这是 "es" 消息模式：

  // Noise es
  sharedSecret = DH(aesk, bpk) = DH(bsk, aepk)

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // ChaChaPoly 参数以加密/解密
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  chainKey = keydata[0:31]

  // AEAD 参数
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, flags/static key section, ad)

  "es" 消息模式结束。

  这是 "s" 消息模式：

  // MixHash(ciphertext)
  // 用于负载部分 KDF 的保存
  h = SHA256(h || ciphertext)

  // Alice 的 X25519 静态密钥
  ask = GENERATE_PRIVATE()
  apk = DERIVE_PUBLIC(ask)

  "s" 消息模式结束。

{% endhighlight %}

左旋消息负载部分的 KDF
`````````````````````````````````````````````````````

.. raw:: html

  {% highlight lang='text' %}
这是 "ss" 消息模式：

  // Noise ss
  sharedSecret = DH(ask, bpk) = DH(bsk, apk)

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // ChaChaPoly 参数以加密/解密
  // 来自静态密钥部分的 chainKey
  Set sharedSecret = X25519 DH 结果
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  chainKey = keydata[0:31]

  // AEAD 参数
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, payload, ad)

  "ss" 消息模式结束。

  // MixHash(ciphertext)
  // 用于新会话回复 KDF 的保存
  h = SHA256(h || ciphertext)

{% endhighlight %}

左旋消息负载部分的 KDF（无 Alice 静态密钥）
```````````````````````````````````````````````````````

请注意，这是一个 Noise "N" 模式，但我们与绑定会话使用与绑定会话相同的 "IK" 初始化器

在解密 Alice 的静态密钥并检查是否包含全零之前，无法识别包含 Alice 静态密钥的新的大蒜消息。
因此，接收方必须使用挂起的 "IK" 状态机为所有
新的大蒜消息密钥。
如果静态密钥为全零，则必须跳过 "ss" 消息模式。

.. raw:: html

  {% highlight lang='text' %}
chainKey = 来自标记/静态密钥部分
  k = from 标记/静态密钥部分
  n = 1
  ad = h from 标记/静态密钥部分
  ciphertext = ENCRYPT(k, n, payload, ad)

{% endhighlight %}

### 1g) 新会话回复格式

一个或多个新会话回复可能对单个新会话消息进行响应。
每个回复都由一个标签前置，该标签是为会话生成的 TagSet。

新会话回复分为两部分。
第一部分是 Noise IK 握手的完成并带有前置标签。
第一部分的长度为 56 字节。
第二部分是数据阶段负载。
第二部分的长度为 16 + 负载长度。

总长度为 72 + 负载长度。
加密格式：

.. raw:: html

  {% highlight lang='dataspec' %}
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

{% endhighlight %}

会话标签
```````````
该标签在以下
DH 初始化 KDF 中。 这关联回复到会话。
DH 初始化的会话密钥未使用。

新会话回复临时密钥
````````````````````````````````

Bob 的临时密钥。
临时密钥为 32 字节，用 Elligator2 编码，小端。
该密钥从未重复使用；每条消息生成新密钥，包括重传。

有效负载
`````````
加密长度是数据的其余部分。
解密后的长度比加密长度少 16。
有效负载通常包含一个或多个大蒜块。
请参阅下面的有效负载部分以了解格式和其他要求。

用于回复 TagSet 的 KDF
```````````````````````

根据下面的 KDF，使用从新会话消息派生的 DH 根密钥初始化的 tag set。

.. raw:: html

  {% highlight lang='text' %}
// 生成标签集
  tagsetKey = HKDF(chainKey, ZEROLEN, "SessionReplyTags", 32)
  tagset_nsr = DH_INITIALIZE(chainKey, tagsetKey)

{% endhighlight %}

用于回复密钥部分加密内容的 KDF
````````````````````````````````````````````

.. raw:: html

  {% highlight lang='text' %}
// 钥匙来自新会话消息
  // Alice 的 X25519 密钥
  // apk 和 aepk 在原始新会话消息中发送
  // ask = Alice 私有静态密钥
  // apk = Alice 公有静态密钥
  // aesk = Alice 临时私有密钥
  // aepk = Alice 临时公有密钥
  // Bob 的 X25519 静态密钥
  // bsk = Bob 私有静态密钥
  // bpk = Bob 公有静态密钥

  // 生成标签
  tagsetEntry = tagset_nsr.GET_NEXT_ENTRY()
  tag = tagsetEntry.SESSION_TAG

  // MixHash(tag)
  h = SHA256(h || tag)

  这是 “e” 消息模式：

  // Bob 的 X25519 临时密钥
  besk = GENERATE_PRIVATE_ELG2()
  bepk = DERIVE_PUBLIC(besk)

  // Bob 的临时公钥
  // MixHash(bepk)
  // || 表示附加
  h = SHA256(h || bepk);

  // elg2_bepk 在
  // 新会话消息的开头以明文形式发送
  elg2_bepk = ENCODE_ELG2(bepk)
  // Bob 解码时
  bepk = DECODE_ELG2(elg2_bepk)

  “e” 消息模式结束。

  这是 “ee” 消息模式：

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // ChaChaPoly 参数以加密/解密
  // 来自原始新会话负载部分的 chainKey
  sharedSecret = DH(aesk, bepk) = DH(besk, aepk)
  keydata = HKDF(chainKey, sharedSecret, "", 32)
  chainKey = keydata[0:31]

  “ee” 消息模式结束。

  这是 “se” 消息模式：

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  sharedSecret = DH(ask, bepk) = DH(besk, apk)
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  chainKey = keydata[0:31]

  // AEAD 参数
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, ZEROLEN, ad)

  “se” 消息模式结束。

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)

  chainKey 用于下面的棘轮。

{% endhighlight %}

负载部分加密内容的 KDF
``````````````````````````````````````````

这就像第一个现有会话消息，在拆分后，但没有单独的标签。
此外，我们使用上面的散列将
有效载荷绑定到 NSR 消息。

.. raw:: html

  {% highlight lang='text' %}
// split()
  keydata = HKDF(chainKey, ZEROLEN, "", 64)
  k_ab = keydata[0:31]
  k_ba = keydata[32:63]
  tagset_ab = DH_INITIALIZE(chainKey, k_ab)
  tagset_ba = DH_INITIALIZE(chainKey, k_ba)

  // 新会话回复负载的 AEAD 参数
  k = HKDF(k_ba, ZEROLEN, "AttachPayloadKDF", 32)
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, payload, ad)
{% endhighlight %}

### 备注

多个 NSR 消息可能会被发送以作为回复，每一个都有独特的临时密钥，取决于回复的大小。

Alice 和 Bob 被要求为每个 NS 和 NSR 消息使用新的临时密钥。

Alice 必须接收 Bob 的一个 NSR 消息，然后再发送现有会话（ES）消息，
Bob 必须接收来自 Alice 的 ES 消息，然后再在与会话绑定的出站渠道上发送 ES 消息。

``chainKey`` 和在 Bob 的 NSR 负载部分的 ``k`` 是用作初始 ES DH 棘轮的输入（参见 DH 棘轮 KDF）。

Bob 只需保留从 Alice 接收的 ES 消息的现有会话。
对于多个 NSR 创建的任何其他入站和出站会话，应在收到 Alice 的第一个 ES 消息后立即销毁。

### 1h) 现有会话格式

会话标签（8 字节）
加密数据和 MAC（见下面的第 3 节）

格式
``````

加密：

.. raw:: html

  {% highlight lang='dataspec' %}
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

{% endhighlight %}

有效负载
```````
加密长度是数据的余量。
解密后的长度比加密长度少 16。
请参阅下面的有效负载部分以了解格式和要求。

KDF
```

.. raw:: html

  {% highlight lang='text' %}
参见下面的 AEAD 部分。

  // 现有会话负载的 AEAD 参数
  k = 与此会话标签相关联的 32 字节会话密钥
  n = 当前链中的消息数 N，作为从关联的会话标签中检索。
  ad = 会话标签，8 字节
  ciphertext = ENCRYPT(k, n, payload, ad)
{% endhighlight %}

### 2) ECIES-X25519

格式：32 字节公钥和私钥，little-endian。

理由：用于 [NTCP2]_。

### 2a) Elligator2

在标准 Noise 握手中，每个方向的初始握手消息以
以明文传输的临时密钥开始。
由于有效的 X25519 密钥可以与随机区分，Man-in-the-middle 可以将这些消息与现有会话消息区分开来，这些现有会话消息以随机会话标签开始。
在 [NTCP2]_ ([Prop111]_) 中，我们使用了一种低开销的 XOR 函数，该函数使用带外的静态密钥来混淆
密钥。然而，此处的威胁模型有所不同；我们不希望允许任何 MitM 使用任何方式来确认流量的目的地，或者
从现有会话消息中区分初始握手消息。

因此，使用 [Elligator2]_ 将新会话和新会话回复消息中的临时密钥
转换为与均匀随机字符串不可区分的形式。

格式
``````

32 字节公钥和私钥。
编码的密钥是小端。

如 [Elligator2]_ 中定义的，编码的密钥与 254 位随机数不可区分。
我们需要 256 位的随机数（32 字节）。因此，编码和解码定义如下：

编码：

.. raw:: html

  {% highlight lang='text' %}
ENCODE_ELG2() 定义

  // 编码如 Elligator2 规范中定义
  encodedKey = encode(pubkey)
  // 在 MSB 中 OR 上 2 个随机位
  randomByte = CSRNG(1)
  encodedKey[31] |= (randomByte & 0xc0)
{% endhighlight %}

解码：

.. raw:: html

  {% highlight lang='text' %}
DECODE_ELG2() 定义

  // 从 MSB 中屏蔽掉 2 个随机位
  encodedKey[31] &= 0x3f
  // 解码为 Elligator2 规范中定义
  pubkey = decode(encodedKey)
{% endhighlight %}

理由
````````````

需要防止 OBEP 和 IBGW 对流量进行分类。

备注
``````

Elligator2 使平均密钥生成时间翻倍，原因是生成的一半私钥导致的公钥不适用于用 Elligator2 编码。
另外，密钥生成时间是无界的，具有指数分布，因为发生器必须不断重试，直到找到一个合适的密钥对。

可以在不同的线程中提前进行密钥生成以管理这种开销，以便保留一组合适的密钥。

生成器执行 ENCODE_ELG2() 函数以确定适用性。
因此，生成器应存储 ENCODE_ELG2() 的结果，以便不必再次计算。

此外，适用的密钥可能会被添加到用于 [NTCP2]_ 的密钥池中，不使用 Elligator2 的情况下。
这样做的安全性问题还有待确定。

### 3) AEAD (ChaChaPoly)

使用 ChaCha20 和 Poly1305 的 AEAD，与 [NTCP2]_ 相同。
这对应于 [RFC-7539]_，亦如
在 TLS [RFC-7905]_ 中类似使用。

新会话和新会话回复输入
````````````````````````

用于加密/解密函数
在新会话消息中的 AEAD 块：

.. raw:: html

  {% highlight lang='dataspec' %}
k :: 32 字节密码密钥
       参见上面的新会话和新会话回复 KDF。

  n :: 基于计数器的 nonce，12 字节。
       n = 0

  ad :: 关联的数据，32 字节。
        作为 mixHash() 的输出的 SHA256 哈希

  数据 :: 明文数据，0 个字节或更多字节

{% endhighlight %}

现有会话输入
`````````````

用于加密/解密函数
在现有会话消息中的 AEAD 块：

.. raw:: html

  {% highlight lang='dataspec' %}
k :: 32 字节会话密钥
       作为伴随会话标签查找。

  n :: 基于计数器的 nonce，12 字节。
       为发射者，每次消息递增。
       对于接收方，该值
       作为伴随会话标签查找。
       前四个字节始终为零。
       最后八个字节为消息编号（n），小端编码。
       最大值为 65535。
       会话必须在 N 达到该值时进行棘轮。
       不得使用更高的值。

  ad :: 关联数据
        会话标签

  数据 :: 明文数据，0 个字节或更多字节

{% endhighlight %}

加密格式
``````````

加密函数的输出，解密函数的输入：

.. raw:: html

  {% highlight lang='dataspec' %}
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

  encrypted data :: 和明文数据大小相同，0 - 65519 字节

  MAC :: Poly1305 消息验证码，16 字节

{% endhighlight %}

备注
`````
- 由于 ChaCha20 是一种流加密，因此不需要对明文进行填充。
  额外的密钥流字节将被丢弃。

- 密码的密钥（256 位）通过 SHA256 KDF 协商。
  每条消息的 KDF 细节在以下单独部分中。

- ChaChaPoly 框架已知大小，因为它们被封装在 I2NP 数据消息中。

- 对于所有消息，
  填充在验证数据框内。

AEAD 错误处理
``````````````

所有接收到的数据一旦 AEAD 验证失败就必须被丢弃。
不会返回响应。

理由
``````````````

在 [NTCP2]_ 中使用。

### 4) 棘轮

我们仍然使用会话标签，像先前一样，但是我们使用棘轮生成它们。
会话标签也有我们从未实现的替换选项。
因此它像一个双棘轮，但我们从未做过第二个。

在此我们定义了类似 Signal 的双棘轮的内容。
会话标签在发送方和接收方以决定方式生成，且相同。

通过使用对称键/标签棘轮，我们消除了存储发送方会话标签的内存使用。
我们还消除了发送标签集的带宽消耗。
接收方的使用仍然显著，但我们可以进一步减少
我们将会话标签从 32 字节缩小到 8 字节。

我们没有使用 Signal 中指定（并且可选的）标头加密，
而是使用会话标签。

通过使用 DH 棘轮，我们实现了前向保密，这在 ElGamal/AES+SessionTags 中从未实施过。

注意：新会话的一次性公钥不是棘轮的一部分，其唯一功能
是加密 Alice 的初始 DH 棘轮密钥。

消息编号
````````````````

双棘轮通过在每个消息头中包含一个标签来处理丢失或乱序的消息。接收者查找标签的索引，这是消息编号 N。
如果消息包含消息编号块（Message Number block）中的 PN 值，
接收方可以立即删除以前标签中高于该值的标签，
而保留标签中以前标签集内的 skipped 标签
以防轻微问题不太多。

示例实现
````````````````````````````

我们定义以下数据结构和函数以实现这些棘轮。

TAGSET_ENTRY
    TAGSET 中的单个条目。

    INDEX
        整数索引，从 0 开始

    SESSION_TAG
        将作为标识符传出，在网络上传输，8 字节

    SESSION_KEY
        一个对称密钥，从不在网络上传输，32 字节

TAGSET
    TAGSET_ENTRY的集合。

    CREATE(key, n)
        使用初始加密密钥生成一个新的 TAGSET。
        与会话的标识符一起提供。
        初始化创建数量为 0 或 1 的标签集；这通常是一个
        传出会话。
        LAST_INDEX = -1
        调用 EXTEND(n)。

    EXTEND(n)
        调用 EXTEND() n 次生成更多的 TAGSET_ENTRY。

    EXTEND()
        生成另外一个 TAGSET_ENTRY，除非已经生成了最大数量 SESSION_TAGS。
        如果 LAST_INDEX 大于等于 65535，返回。
        ++ LAST_INDEX
        使用 LAST_INDEX 值创建一个新的 TAGSET_ENTRY 和计算的 SESSION_TAG。
        调用 RATCHET_TAG() 和（可选）RATCHET_KEY()。
        对于入站会话，会将 SESSION_KEY 的计算推迟，并在 GET_SESSION_KEY() 中计算。
        调用 EXPIRE()

    EXPIRE()
        移除太旧的，或如果 TAGSET 大小超过某个限制的标签和密钥。

    RATCHET_TAG()
        根据最后一个 SESSION_TAG 计算下一个 SESSION_TAG。

    RATCHET_KEY()
        根据最后一个 SESSION_KEY 计算下一个 SESSION_KEY。

    SESSION
        关联的会话。

    CREATION_TIME
        TAGSET 被创建的时间。

    LAST_INDEX
        由 EXTEND() 生成的最后一个 TAGSET_ENTRY。

    GET_NEXT_ENTRY()
        仅用于传出会话。
        如果没有剩余的 TAGSET_ENTRY，将调用 EXTEND(1)。
        如果 EXTEND(1) 没有做任何事情，则最大为 65535 的 TAGSETS 已被使用，
        并返回一个错误。
        返回下一个未使用的 TAGSET_ENTRY。

    GET_SESSION_KEY(sessionTag)
        仅用于接收会话。
        返回包含 sessionTag 的 TAGSET_ENTRY。
        如果找到，TAGSET_ENTRY 被移除。
        如果 SESSION_KEY 计算被推迟，则现在计算它。
        如果剩余的 TAGSET_ENTRY 很少，调用 EXTEND(n)。

4a) DH 棘轮
``````````````

棘轮但不如 Signal 那样快。
我们将接收到的密钥的确认与传输新的密钥分开。
在典型用法中，Alice 和 Bob 在一个新会话中会立即棘轮（两次），但不会再棘轮。

注意，一个棘轮用于单一方向，并生成一个用于该方向的新会话标记/消息密钥棘轮链。
要生成两个方向的密钥，必须运行两次棘轮。

您每次生成并发送新密钥时都必须棘轮。
每次接收到新密钥时都必须棘轮。

Alice 每次创建不绑定出站会话时会棘轮，她不创建入站会话
（不绑定是不相关的）。

Bob 每次创建不绑定入站会话时会棘轮，并且不创建对应的出站会话
（不绑定是不相关的）。

Alice 开始发送新的会话（NS）消息给 Bob，直到收到 Bob 的一个新的会话回复（NSR）消息。
然后她使用 NSR 有效负载部分的 KDF 结果作为会话棘轮的输入（见 DH 棘轮 KDF），并开始发送现有会话（ES）消息。

对于每个收到的 NS 消息，Bob 创建一个新的入站会话，使用回复负载部分的 KDF 结果作为新的入站和出站 ES DH 棘轮的输入。

对于每个必要的回复，Bob 发送给 Alice 一个 NSR 消息，回复包含在负载部分。
Bob 必须在每个 NSR 生成新的临时密钥。

Bob 必须接收到 Alice 在其中一个入站会话中发送的 ES 消息，然后才创建并发送在关联的出站渠道的 ES 消息。

Alice 应该为从 Bob 接收 NSR 消息设置超时。如果计时到期，会话应被移除。

为了避免发生 KCI 和/或资源耗尽攻击，攻击者会掉落 Bob 的 NSR 回复以保持 Alice 发送新的会话消息，
Alice 应避免在某一数量的重试后由于计时到期而开始新会话。

Alice 和 Bob 每收到一个 NextKey 块就做一个 DH 棘轮。

Alice 和 Bob 每次 DH 棘轮后都会生成新的标签集和两个对称密钥棘轮。每个
在给定方向上发送新的 ES 消息，Alice 和 Bob 都会推进会话标签和对称的密钥棘轮。

在初次握手后，DH 棘轮的频率依赖于实现。
虽然协议限制为 65535 消息，但棘轮是必须的，
更频繁的棘轮（基于消息计数，经过的时间，或两者都）
可能提供额外的安全性。

在绑定会话的最后握手 KDF 后，Bob 和 Alice 必须对
使用生成 CipherState 的 Noise Split() 函数，在绑定的会话进行独立的对称和标签链密钥的生成。

#### 密钥和标签集 ID

密钥和标签集 ID 用于标识使用的标签集。
密钥 ID 用于 NextKey 块中标识发送或使用的密钥。
标签集 ID 用于在 ACK 块中标识确认消息。
- 用于一个方向的标签集。

在每个方向用于会话的第一个标签集中，标签集 ID 为 0。
由于没有发送 NextKey 块，所以没有密钥 ID。

要开始一个 DH 棘轮，发送方发送一个带有密钥 ID 为 0 的 NextKey 块。
接收方使用密钥 ID 为 0 的 NextKey 块进行回复。
然后发件方开始使用具有标签集 ID 为 1 的新标签集。

后续标签集类似地产生。
对于所有在 NextKey 交换后用的标签集，标签集数量是（1 + Alice 的的密钥 ID + Bob 的的密钥 ID）。

密钥和标签集 ID 从 0 开始并按顺序增加。
最大标签集 ID 为 65535。
最大密钥 ID 为 32767。
当接近耗尽时，标签集发送方必须启动一个 NextKey 交换。
当接近耗尽时，标签集 65535 几乎耗尽时，标签集发送方必须通过发送一个新的会话
启动一个新会话消息。

对于假定的最大消息大小为 1730，并且假设没有重传，
使用单个标签集的理论最大数据传输量为 1730 * 65536 ~= 108 MB。
因为重传，实际最大值将更低。

可能会话可用的所有 65536 个标签集，之前的时候最大数据传输，
是 64K * 108 MB ~= 6.9 TB。

#### DH 棘轮消息流

标签集的下一个密钥交换必须由发件方
发送（那些标签的发件方）。
接收方（入站标签集的所有者）将会响应。
对于应用在应用层上的构造的 HTTP GET 请求，Bob 将会发送更很多消息，并将第一个
通过启动密钥交换，下面的图显示了这一点。
当 Alice 棘轮时，同样的事情发生在反方向。

在 NS/NSR 握手后使用的第一个标签集是标签集 0。
当标签集 0 接近耗尽时，必须交换新密钥，以便两个方向都能创建标签集 1。
在那之后，一个新的密钥只会在一个方向上被发送。

为了创建标签集 2，标签发送方发送新密钥，标签接收方发送他的旧密钥作为确认。
双方都会进行 DH。

为了创建标签集 3，标签发送方发送他的旧密钥的 ID，并请求标签接收方的新的密钥。
双方都会进行 DH。

后续的标签集按照标签集 2 和 3 的顺序生成。
标签集数是（1+发送方密钥 id+接收方密钥 id）。

.. raw:: html

  {% highlight %}
标签发件方                    标签接收方

                   ... 使用标签集 #0 ...


  (标签集 #0 几乎耗尽)
  (生成新密钥 #0)

  下一密钥，正向，请求反向，带有密钥 #0  -------->
  (重复直到接收到下一个密钥
