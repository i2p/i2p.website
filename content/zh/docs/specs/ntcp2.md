---
title: "NTCP2 传输协议"
description: "基于 Noise 的 TCP 传输协议用于 router 到 router 链接"
slug: "ntcp2"
category: "传输层"
lastUpdated: "2026-07"
accurateFor: "0.9.70"
---

## 概述

NTCP2 是一种经过身份验证的密钥协商协议，提高了 [NTCP](/docs/transport/ntcp) 对各种形式的自动识别和攻击的抵抗能力。

NTCP2 的设计具有灵活性，可以与 NTCP 共存。它可以在与 NTCP 相同的端口上支持，或者在不同的端口上，或者完全不同时支持 NTCP。详情请参见下面的已发布 router 信息部分。

与其他 I2P 传输协议一样，NTCP2 仅用于点对点（router 到 router）传输 I2NP 消息。它不是通用的数据管道。

NTCP2 从 0.9.36 版本开始支持。请参阅 [Prop111](/proposals/111-ntcp-2) 查看原始提案，包括背景讨论和其他信息。

## Noise 协议框架

NTCP2使用Noise协议框架[NOISE](https://noiseprotocol.org/noise.html)（修订版33，2017-10-04）。Noise具有与Station-To-Station协议[STS](#references)类似的属性，后者是[SSU](/docs/transport/ssu)协议的基础。在Noise术语中，Alice是发起方，Bob是响应方。

NTCP2 基于 Noise 协议 Noise_XK_25519_ChaChaPoly_SHA256。（初始密钥派生函数的实际标识符是 "Noise_XKaesobfse+hs2+hs3_25519_ChaChaPoly_SHA256" 以表示 I2P 扩展 - 请参见下面的 KDF 1 部分）此 Noise 协议使用以下原语：

- 握手模式：XK Alice 将她的密钥传输给 Bob (X) Alice 已经知道 Bob 的静态密钥 (K)
- DH 函数：X25519 按照 [RFC-7748](https://tools.ietf.org/html/rfc7748) 规范，使用密钥长度为 32 字节的 X25519 DH。
- 加密函数：ChaChaPoly 按照 [RFC-7539](https://tools.ietf.org/html/rfc7539) 第 2.8 节规范的 AEAD_CHACHA20_POLY1305。12 字节随机数，前 4 字节设为零。
- 哈希函数：SHA256 标准 32 字节哈希，已在 I2P 中广泛使用。

## 框架的扩展

NTCP2 定义了对 Noise_XK_25519_ChaChaPoly_SHA256 的以下增强。这些增强通常遵循 [NOISE](https://noiseprotocol.org/noise.html) 第 13 节中的指导原则。

1) 明文临时密钥使用已知密钥和 IV 进行 AES 加密混淆。2) 在消息 1 和 2 中添加随机明文填充。明文填充包含在握手哈希 (MixHash) 计算中。请参阅下面消息 2 和消息 3 第 1 部分的 KDF 章节。在消息 3 和数据阶段消息中添加随机 AEAD 填充。3) 添加两字节帧长度字段，这是 Noise over TCP 所要求的，与 obfs4 中的做法相同。这仅用于数据阶段消息。消息 1 和 2 的 AEAD 帧长度固定。消息 3 第 1 部分 AEAD 帧长度固定。消息 3 第 2 部分 AEAD 帧长度在消息 1 中指定。4) 两字节帧长度字段使用 SipHash-2-4 进行混淆，与 obfs4 中的做法相同。5) 为消息 1、2、3 和数据阶段定义了负载格式。当然，这些在框架中并未定义。

## 消息

所有 NTCP2 消息的长度都小于或等于 65537 字节。消息格式基于 Noise 消息，并针对帧结构和不可区分性进行了修改。使用标准 Noise 库的实现可能需要对接收到的消息进行预处理，以转换为 Noise 消息格式。所有加密字段都是 AEAD 密文。

建立序列如下：

```
Alice                           Bob

SessionRequest ------------------->
<------------------- SessionCreated
SessionConfirmed ----------------->
```
使用 Noise 术语，建立连接和数据序列如下：（载荷安全属性来自 [Noise](https://noiseprotocol.org/noise.html)）

```
XK(s, rs):           Authentication   Confidentiality
  <- s
  ...
  -> e, es                  0                2
  <- e, ee                  2                1
  -> s, se                  2                5
  <-                        2                5
```
一旦建立了会话，Alice 和 Bob 就可以交换数据消息。

本节规定了所有消息类型（SessionRequest、SessionCreated、SessionConfirmed、Data 和 TimeSync）。

一些注释：

    - RH_A = Router Hash for Alice (32 bytes)
    - RH_B = Router Hash for Bob (32 bytes)

### 认证加密

有三个独立的认证加密实例 (CipherStates)。一个在握手阶段使用，两个（发送和接收）在数据阶段使用。每个都有来自 KDF 的自己的密钥。

加密/认证数据将表示为

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|   Encrypted and authenticated data    |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
```
#### ChaCha20/Poly1305

加密和认证的数据格式。

加密/解密函数的输入：

```
k :: 32 byte cipher key, as generated from KDF

nonce :: Counter-based nonce, 12 bytes.
         Starts at 0 and incremented for each message.
         First four bytes are always zero.
         Last eight bytes are the counter, little-endian encoded.
         Maximum value is 2**64 - 2.
         Connection must be dropped and restarted after
         it reaches that value.
         The value 2**64 - 1 must never be sent.

ad :: In handshake phase:
      Associated data, 32 bytes.
      The SHA256 hash of all preceding data.
      In data phase:
      Zero bytes

data :: Plaintext data, 0 or more bytes
```
加密函数的输出，解密函数的输入：

```
+----+----+----+----+----+----+----+----+
|Obfs Len |                             |
+----+----+                             +
|       ChaCha20 encrypted data         |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+              (MAC)                    +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Obfs Len :: Length of (encrypted data + MAC) to follow, 16 - 65535
            Obfuscation using SipHash (see below)
            Not used in message 1 or 2, or message 3 part 1, where the length is fixed
            Not used in message 3 part 1, as the length is specified in message 1

encrypted data :: Same size as plaintext data, 0 - 65519 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
对于 ChaCha20，这里描述的内容对应于 [RFC-7539](https://tools.ietf.org/html/rfc7539)，这也在 TLS [RFC-7905](https://tools.ietf.org/html/rfc7905) 中有类似使用。

#### 注意事项

- 由于ChaCha20是流密码，明文无需填充。多余的密钥流字节会被丢弃。
- 密码的密钥（256位）通过SHA256 KDF协商确定。每个消息的KDF详细信息在下面的单独章节中说明。
- 消息1、消息2和消息3第一部分的ChaChaPoly帧具有已知大小。从消息3第二部分开始，帧的大小是可变的。消息3第一部分的大小在消息1中指定。从数据阶段开始，帧前会添加一个使用SipHash混淆的两字节长度字段，就像obfs4中一样。
- 对于消息1和2，填充在认证数据帧之外。填充用于下一个消息的KDF中，因此篡改会被检测到。从消息3开始，填充在认证数据帧内部。

#### AEAD 错误处理

- 在消息1、消息2以及消息3的第1部分和第2部分中，AEAD消息大小是预先已知的。在AEAD认证失败时，接收方必须停止进一步的消息处理并关闭连接而不响应。这应该是异常关闭（TCP RST）。
- 为了抵御探测，在消息1中，在AEAD失败后，Bob应该设置一个随机超时时间（范围待定），然后在关闭套接字之前读取随机数量的字节（范围待定）。Bob应该维护一个重复失败IP的黑名单。
- 在数据阶段，AEAD消息大小使用SipHash进行"加密"（混淆）。必须小心避免创建解密预言机。在数据阶段AEAD认证失败时，接收方应该设置一个随机超时时间（范围待定），然后读取随机数量的字节（范围待定）。读取完成后，或在读取超时时，接收方应该发送包含终止块的载荷，该终止块包含"AEAD失败"原因代码，并关闭连接。
- 对于数据阶段中无效长度字段值，采取相同的错误处理措施。

### 密钥派生函数 (KDF)（用于握手消息1）

KDF 从 DH 结果生成握手阶段密码密钥 k，使用 [RFC-2104](https://tools.ietf.org/html/rfc2104) 中定义的 HMAC-SHA256(key, data)。这些是 InitializeSymmetric()、MixHash() 和 MixKey() 函数，与 Noise 规范中定义的完全相同。

```
This is the "e" message pattern:

// Define protocol_name.
Set protocol_name = "Noise_XKaesobfse+hs2+hs3_25519_ChaChaPoly_SHA256"
 (48 bytes, US-ASCII encoded, no NULL termination).

// Define Hash h = 32 bytes
h = SHA256(protocol_name);

Define ck = 32 byte chaining key. Copy the h data to ck.
Set ck = h

Define rs = Bob's 32-byte static key as published in the RouterInfo

// MixHash(null prologue)
h = SHA256(h);

// up until here, can all be precalculated by Alice for all outgoing connections

// Alice must validate that Bob's static key is a valid point on the curve here.

// Bob static key
// MixHash(rs)
// || below means append
h = SHA256(h || rs);

// up until here, can all be precalculated by Bob for all incoming connections

This is the "e" message pattern:

Alice generates her ephemeral DH key pair e.

// Alice ephemeral key X
// MixHash(e.pubkey)
// || below means append
h = SHA256(h || e.pubkey);

// h is used as the associated data for the AEAD in message 1
// Retain the Hash h for the message 2 KDF


End of "e" message pattern.

This is the "es" message pattern:

// DH(e, rs) == DH(s, re)
Define input_key_material = 32 byte DH result of Alice's ephemeral key and Bob's static key
Set input_key_material = X25519 DH result

// MixKey(DH())

Define temp_key = 32 bytes
Define HMAC-SHA256(key, data) as in [RFC-2104]_
// Generate a temp key from the chaining key and DH result
// ck is the chaining key, defined above
temp_key = HMAC-SHA256(ck, input_key_material)
// overwrite the DH result in memory, no longer needed
input_key_material = (all zeros)

// Output 1
// Set a new chaining key from the temp key
// byte() below means a single byte
ck =       HMAC-SHA256(temp_key, byte(0x01)).

// Output 2
// Generate the cipher key k
Define k = 32 bytes
// || below means append
// byte() below means a single byte
k =        HMAC-SHA256(temp_key, ck || byte(0x02)).
// overwrite the temp_key in memory, no longer needed
temp_key = (all zeros)

// retain the chaining key ck for message 2 KDF


End of "es" message pattern.
```
### 1) SessionRequest

Alice 发送给 Bob。

Noise 内容：Alice 的临时密钥 X Noise 载荷：16 字节选项块 非 Noise 载荷：随机填充

(来自 [Noise](https://noiseprotocol.org/noise.html) 的载荷安全属性)

```
XK(s, rs):           Authentication   Confidentiality
  -> e, es                  0                2

  Authentication: None (0).
  This payload may have been sent by any party, including an active attacker.

  Confidentiality: 2.
  Encryption to a known recipient, forward secrecy for sender compromise
  only, vulnerable to replay.  This payload is encrypted based only on DHs
  involving the recipient's static key pair.  If the recipient's static
  private key is compromised, even at a later date, this payload can be
  decrypted.  This message can also be replayed, since there's no ephemeral
  contribution from the recipient.

  "e": Alice generates a new ephemeral key pair and stores it in the e
       variable, writes the ephemeral public key as cleartext into the
       message buffer, and hashes the public key along with the old h to
       derive a new h.

  "es": A DH is performed between the Alice's ephemeral key pair and the
        Bob's static key pair.  The result is hashed along with the old ck to
        derive a new ck and k, and n is set to zero.
```
X 值经过加密以确保载荷的不可区分性和唯一性，这些是必要的深度包检测（DPI）对抗措施。我们使用 AES 加密来实现这一点，而不是使用更复杂和更慢的替代方案如 elligator2。使用 Bob 的 router 公钥进行非对称加密会过于缓慢。AES 加密使用 Bob 的 router hash 作为密钥，并使用 Bob 在 netDb 中发布的 IV。

AES 加密仅用于抵抗 DPI（深度包检测）。任何知道 Bob 的 router 哈希值和 IV（这些都发布在网络数据库中）的一方都可以解密此消息中的 X 值。

填充数据不会被 Alice 加密。Bob 可能需要解密填充数据，以防止时序攻击。

原始内容：

```
+----+----+----+----+----+----+----+----+
|                                       |
+        obfuscated with RH_B           +
|       AES-CBC-256 encrypted X         |
+             (32 bytes)                +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|   ChaChaPoly encrypted data           |
+             (16 bytes)                +
|   k defined in KDF for message 1      |
+   n = 0                               +
|   see KDF for associated data         |
+----+----+----+----+----+----+----+----+
|                                       |
+        Poly1305 MAC (16 bytes)        +
|                                       |
+----+----+----+----+----+----+----+----+
|     unencrypted authenticated         |
~         padding (optional)            ~
|     length defined in options block   |
+----+----+----+----+----+----+----+----+

X :: 32 bytes, AES-256-CBC encrypted X25519 ephemeral key, little endian
        key: RH_B
        iv: As published in Bobs network database entry

padding :: Random data, 0 or more bytes.
           Total message length must be 65535 bytes or less.
           Total message length must be 287 bytes or less if
           Bob is publishing his address as NTCP
           (see Version Detection section below).
           Alice and Bob will use the padding data in the KDF for message 2.
           It is authenticated so that any tampering will cause the
           next message to fail.
```
未加密数据（未显示 Poly1305 认证标签）：

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|                   X                   |
+              (32 bytes)               +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|               options                 |
+              (16 bytes)               +
|                                       |
+----+----+----+----+----+----+----+----+
|     unencrypted authenticated         |
+         padding (optional)            +
|     length defined in options block   |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

X :: 32 bytes, X25519 ephemeral key, little endian

options :: options block, 16 bytes, see below

padding :: Random data, 0 or more bytes.
           Total message length must be 65535 bytes or less.
           Total message length must be 287 bytes or less if
           Bob is publishing his address as "NTCP"
           (see Version Detection section below)
           Alice and Bob will use the padding data in the KDF for message 2.
           It is authenticated so that any tampering will cause the
           next message to fail.
```
选项块：注意：所有字段都是大端字节序。

```
+----+----+----+----+----+----+----+----+
| id | ver|  padLen | m3p2len | Rsvd(0) |
+----+----+----+----+----+----+----+----+
|        tsA        |   Reserved (0)    |
+----+----+----+----+----+----+----+----+

id :: 1 byte, the network ID (currently 2, except for test networks)
      As of 0.9.42. See proposal 147.

ver :: 1 byte, protocol version (currently 2)

padLen :: 2 bytes, length of the padding, 0 or more
          See below for max guidelines. Random size from 0 to 64 bytes minimum is recommended.
          (Distribution is implementation-dependent)

m3p2Len :: 2 bytes, length of the the second AEAD frame in SessionConfirmed
           (message 3 part 2) See notes below

Rsvd :: 2 bytes, set to 0 for compatibility with future options

tsA :: 4 bytes, Unix timestamp, unsigned seconds.
       Wraps around in 2106

Reserved :: 4 bytes, set to 0 for compatibility with future options
```
#### 注意事项

- 当发布的地址是"NTCP"时，Bob在同一端口上同时支持NTCP和NTCP2。为了兼容性，当Alice向发布为"NTCP"的地址发起连接时，必须将此消息的最大大小（包括填充）限制在287字节或更少。这便于Bob进行自动协议识别。当发布为"NTCP2"时，没有大小限制。请参见下面的发布地址和版本检测部分。

- 初始AES块中的唯一X值确保每个会话的密文都不相同。

- Bob必须拒绝时间戳值与当前时间相差过大的连接。将最大时间差称为"D"。Bob必须维护一个本地缓存，存储之前使用过的握手值并拒绝重复值，以防止重放攻击。缓存中的值必须具有至少2*D的生命周期。缓存值的实现依赖于具体实现，但可以使用32字节的X值（或其加密等价物）。

- Diffie-Hellman 临时密钥绝不能重复使用，以防止密码学攻击，重复使用将被拒绝并视为重放攻击。

- "KE" 和 "auth" 选项必须兼容，即共享密钥 K 必须具有适当的大小。如果添加了更多的 "auth" 选项，这可能会隐式地改变 "KE" 标志的含义，以使用不同的 KDF 或不同的截断大小。

- Bob 必须在此处验证 Alice 的临时密钥是曲线上的有效点。

- 填充应限制在合理范围内。Bob 可能会拒绝填充过多的连接。Bob 将在消息 2 中指定其填充选项。最小/最大指导原则待定。最小从 0 到 31 字节的随机大小？（分布依赖于实现）Java 实现目前将填充限制为最大 256 字节。

- 在任何错误情况下，包括AEAD、DH、时间戳、明显重放攻击或密钥验证失败，Bob必须停止进一步的消息处理并关闭连接而不响应。这应该是异常关闭（TCP RST）。为了抵抗探测，在AEAD失败后，Bob应该设置一个随机超时（范围待定），然后读取随机数量的字节（范围待定），之后再关闭套接字。

- Bob 可以在尝试解密之前对有效密钥进行快速 MSB 检查 (X[31] & 0x80 == 0)。如果高位被设置，则实现与 AEAD 失败相同的探测抵抗机制。

- DoS 缓解：DH 是一个相对昂贵的操作。与之前的 NTCP 协议一样，router 应采取所有必要措施防止 CPU 或连接耗尽。对最大活跃连接数和正在进行的最大连接建立数设置限制。强制执行读取超时（包括单次读取和"slowloris"攻击的总超时）。限制来自同一源的重复或同时连接。为反复失败的源维护黑名单。不要响应 AEAD 失败。

- 为了便于快速版本检测和握手，实现必须确保 Alice 缓冲然后一次性刷新第一条消息的全部内容，包括填充数据。这增加了数据包含在单个 TCP 数据包中的可能性（除非被操作系统或中间设备分段），并且 Bob 能够一次性接收所有数据。此外，实现必须确保 Bob 缓冲然后一次性刷新第二条消息的全部内容，包括填充数据，并且 Bob 缓冲然后一次性刷新第三条消息的全部内容。这也是为了提高效率并确保随机填充的有效性。

- "ver"字段：整体Noise协议、扩展和NTCP协议（包括载荷规范），表示NTCP2。此字段可用于指示对未来变更的支持。

- 消息3第2部分长度：这是包含Alice的Router Info和可选填充的第二个AEAD帧的大小（包括16字节MAC），将在SessionConfirmed消息中发送。由于router会定期重新生成和重新发布其Router Info，当前Router Info的大小可能在消息3发送前发生变化。实现必须选择以下两种策略之一：

a\) 保存要在消息3中发送的当前 Router Info，这样就知道了大小，并可选择性地添加填充空间；

b\) 增加指定的大小以允许 Router Info 大小可能的增长，并在实际发送消息 3 时始终添加填充。无论哪种情况，消息 1 中包含的 "m3p2len" 长度必须与消息 3 中发送该帧时的大小完全一致。

- 如果在验证消息1并读取填充数据后仍有任何传入数据，Bob必须使连接失败。不应该有来自Alice的额外数据，因为Bob还没有用消息2进行响应。

- 网络ID字段用于快速识别跨网络连接。如果此字段非零且与Bob的网络ID不匹配，Bob应断开连接并阻止未来的连接。来自测试网络的任何连接都应具有不同的ID，并且测试会失败。自0.9.42版本起。更多信息请参阅提案147。

- 在 API 0.9.68 (release 2.11.0) 之前，Java I2P 为非PQ连接实现了最大256字节的填充，但这之前没有被记录在文档中。
  自 API 0.9.69 (release 2.12.0) 起，Java I2P 对非PQ连接实现了与 MLKEM-512 相同的最大填充。最大填充为880字节。

### 密钥派生函数 (KDF) (用于握手消息 2 和消息 3 第 1 部分)

```
// take h saved from message 1 KDF
// MixHash(ciphertext)
h = SHA256(h || 32 byte encrypted payload from message 1)

// MixHash(padding)
// Only if padding length is nonzero
h = SHA256(h || random padding from message 1)

This is the "e" message pattern:

Bob generates his ephemeral DH key pair e.

// h is from KDF for handshake message 1
// Bob ephemeral key Y
// MixHash(e.pubkey)
// || below means append
h = SHA256(h || e.pubkey);

// h is used as the associated data for the AEAD in message 2
// Retain the Hash h for the message 3 KDF

End of "e" message pattern.

This is the "ee" message pattern:

// DH(e, re)
Define input_key_material = 32 byte DH result of Alice's ephemeral key and Bob's ephemeral key
Set input_key_material = X25519 DH result
// overwrite Alice's ephemeral key in memory, no longer needed
// Alice:
e(public and private) = (all zeros)
// Bob:
re = (all zeros)

// MixKey(DH())

Define temp_key = 32 bytes
Define HMAC-SHA256(key, data) as in [RFC-2104]_
// Generate a temp key from the chaining key and DH result
// ck is the chaining key, from the KDF for handshake message 1
temp_key = HMAC-SHA256(ck, input_key_material)
// overwrite the DH result in memory, no longer needed
input_key_material = (all zeros)

// Output 1
// Set a new chaining key from the temp key
// byte() below means a single byte
ck =       HMAC-SHA256(temp_key, byte(0x01)).

// Output 2
// Generate the cipher key k
Define k = 32 bytes
// || below means append
// byte() below means a single byte
k =        HMAC-SHA256(temp_key, ck || byte(0x02)).
// overwrite the temp_key in memory, no longer needed
temp_key = (all zeros)

// retain the chaining key ck for message 3 KDF

End of "ee" message pattern.
```
### 2) SessionCreated

Bob 发送给 Alice。

Noise 内容：Bob 的临时密钥 Y Noise 载荷：16 字节选项块 非 Noise 载荷：随机填充

（来自 [Noise](https://noiseprotocol.org/noise.html) 的载荷安全属性）

```
XK(s, rs):           Authentication   Confidentiality
  <- e, ee                  2                1

  Authentication: 2.
  Sender authentication resistant to key-compromise impersonation (KCI).
  The sender authentication is based on an ephemeral-static DH ("es" or "se")
  between the sender's static key pair and the recipient's ephemeral key pair.
  Assuming the corresponding private keys are secure, this authentication cannot be forged.

  Confidentiality: 1.
  Encryption to an ephemeral recipient.
  This payload has forward secrecy, since encryption involves an ephemeral-ephemeral DH ("ee").
  However, the sender has not authenticated the recipient,
  so this payload might be sent to any party, including an active attacker.


  "e": Bob generates a new ephemeral key pair and stores it in the e variable,
  writes the ephemeral public key as cleartext into the message buffer,
  and hashes the public key along with the old h to derive a new h.

  "ee": A DH is performed between the Bob's ephemeral key pair and the Alice's ephemeral key pair.
  The result is hashed along with the old ck to derive a new ck and k, and n is set to zero.
```
Y 值被加密以确保载荷的不可区分性和唯一性，这是必要的 DPI 对抗措施。我们使用 AES 加密来实现这一点，而不是使用更复杂和更慢的替代方案，如 elligator2。使用 Alice 的 router 公钥进行非对称加密将会过于缓慢。AES 加密使用 Bob 的 router hash 作为密钥，以及来自消息 1 的 AES 状态（该状态使用 Bob 发布在 netDb 中的 IV 进行初始化）。

AES加密仅用于抵抗DPI（深度包检测）。任何知道Bob的router哈希值和IV（这些都发布在网络数据库中）并捕获到消息1前32字节的一方，都可以解密此消息中的Y值。

原始内容：

```
+----+----+----+----+----+----+----+----+
|                                       |
+        obfuscated with RH_B           +
|       AES-CBC-256 encrypted Y         |
+              (32 bytes)               +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|   ChaChaPoly encrypted data (options) |
+   16 bytes                            +
|   k defined in KDF for message 2      |
+   n = 0; see KDF for associated data  +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+        Poly1305 MAC (16 bytes)        +
|                                       |
+----+----+----+----+----+----+----+----+
|     unencrypted authenticated         |
+         padding (optional)            +
|     length defined in options block   |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

Y :: 32 bytes, AES-256-CBC encrypted X25519 ephemeral key, little endian
        key: RH_B
        iv: Using AES state from message 1
```
未加密数据（未显示 Poly1305 认证标签）：

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|                  Y                    |
+              (32 bytes)               +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|               options                 |
+              (16 bytes)               +
|                                       |
+----+----+----+----+----+----+----+----+
|     unencrypted authenticated         |
+         padding (optional)            +
|     length defined in options block   |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

Y :: 32 bytes, X25519 ephemeral key, little endian

options :: options block, 16 bytes, see below

padding :: Random data, 0 or more bytes.
           Total message length must be 65535 bytes or less.
           Alice and Bob will use the padding data in the KDF for message 3 part 1.
           It is authenticated so that any tampering will cause the
           next message to fail.
```
#### 注释

- Alice 必须在此验证 Bob 的临时密钥是曲线上的有效点。
- 填充应限制在合理的范围内。Alice 可能会拒绝填充过多的连接。Alice 将在消息 3 中指定她的填充选项。最小/最大准则待定。最少从 0 到 31 字节的随机大小？（分布取决于实现）
- 遇到任何错误，包括 AEAD、DH、时间戳、明显的重放攻击或密钥验证失败，Alice 必须停止进一步的消息处理并关闭连接而不响应。这应该是异常关闭（TCP RST）。
- 为了促进快速握手，实现必须确保 Bob 缓冲然后一次性刷新第一条消息的全部内容，包括填充。这增加了数据被包含在单个 TCP 数据包中的可能性（除非被操作系统或中间设备分段），并被 Alice 一次性接收。这也是为了效率和确保随机填充的有效性。
- 如果在验证消息 2 和读取填充后还有任何传入数据，Alice 必须使连接失败。不应该有来自 Bob 的额外数据，因为 Alice 尚未用消息 3 响应。

选项块：注意：所有字段均为大端字节序。

```
+----+----+----+----+----+----+----+----+
| Rsvd(0) | padLen  |   Reserved (0)    |
+----+----+----+----+----+----+----+----+
|        tsB        |   Reserved (0)    |
+----+----+----+----+----+----+----+----+

Reserved :: 10 bytes total, set to 0 for compatibility with future options

padLen :: 2 bytes, big endian, length of the padding, 0 or more
          See below for max guidelines. Random size from 0 to 64 bytes minimum is recommended.
          (Distribution is implementation-dependent)

tsB :: 4 bytes, big endian, Unix timestamp, unsigned seconds.
       Wraps around in 2106
```
#### 注意事项

- Alice 必须拒绝时间戳值与当前时间相差过大的连接。将最大时间差称为"D"。Alice 必须维护一个本地缓存，存储之前使用过的握手值并拒绝重复值，以防止重放攻击。缓存中的值必须至少保持 2*D 的生存期。缓存值的具体实现取决于实现方式，不过可以使用 32 字节的 Y 值（或其加密等价物）。

- 在 API 0.9.68（发布版本 2.11.0）之前，Java I2P 为非 PQ 连接实现了最大 256 字节的填充，但此前未被文档化。
  从 API 0.9.69（发布版本 2.12.0）开始，Java I2P 为非 PQ 连接实现与 MLKEM-512 相同的最大填充。最大填充为 848 字节。

#### 问题

- 在这里包含最小/最大填充选项？

### 使用消息2 KDF对握手消息3第1部分进行加密

```
// take h saved from message 2 KDF
// MixHash(ciphertext)
h = SHA256(h || 24 byte encrypted payload from message 2)

// MixHash(padding)
// Only if padding length is nonzero
h = SHA256(h || random padding from message 2)
// h is used as the associated data for the AEAD in message 3 part 1, below

This is the "s" message pattern:

Define s = Alice's static public key, 32 bytes

// EncryptAndHash(s.publickey)
// EncryptWithAd(h, s.publickey)
// AEAD_ChaCha20_Poly1305(key, nonce, associatedData, data)
// k is from handshake message 1
// n is 1
ciphertext = AEAD_ChaCha20_Poly1305(k, n++, h, s.publickey)
// MixHash(ciphertext)
// || below means append
h = SHA256(h || ciphertext);

// h is used as the associated data for the AEAD in message 3 part 2

End of "s" message pattern.
```
### 密钥派生函数 (KDF)（用于握手消息 3 第 2 部分）

```
This is the "se" message pattern:

// DH(s, re) == DH(e, rs)
Define input_key_material = 32 byte DH result of Alice's static key and Bob's ephemeral key
Set input_key_material = X25519 DH result
// overwrite Bob's ephemeral key in memory, no longer needed
// Alice:
re = (all zeros)
// Bob:
e(public and private) = (all zeros)

// MixKey(DH())

Define temp_key = 32 bytes
Define HMAC-SHA256(key, data) as in [RFC-2104]_
// Generate a temp key from the chaining key and DH result
// ck is the chaining key, from the KDF for handshake message 1
temp_key = HMAC-SHA256(ck, input_key_material)
// overwrite the DH result in memory, no longer needed
input_key_material = (all zeros)

// Output 1
// Set a new chaining key from the temp key
// byte() below means a single byte
ck =       HMAC-SHA256(temp_key, byte(0x01)).

// Output 2
// Generate the cipher key k
Define k = 32 bytes
// || below means append
// byte() below means a single byte
k =        HMAC-SHA256(temp_key, ck || byte(0x02)).

// h from message 3 part 1 is used as the associated data for the AEAD in message 3 part 2

// EncryptAndHash(payload)
// EncryptWithAd(h, payload)
// AEAD_ChaCha20_Poly1305(key, nonce, associatedData, data)
// n is 0
ciphertext = AEAD_ChaCha20_Poly1305(k, n++, h, payload)
// MixHash(ciphertext)
// || below means append
h = SHA256(h || ciphertext);

// retain the chaining key ck for the data phase KDF
// retain the hash h for the data phase Additional Symmetric Key (SipHash) KDF

End of "se" message pattern.

// overwrite the temp_key in memory, no longer needed
temp_key = (all zeros)
```
### 3) SessionConfirmed

Alice 发送给 Bob。

Noise 内容：Alice 的静态密钥 Noise 载荷：Alice 的 RouterInfo 和随机填充 非 Noise 载荷：无

(来自 [Noise](https://noiseprotocol.org/noise.html) 的载荷安全属性)

```
XK(s, rs):           Authentication   Confidentiality
  -> s, se                  2                5

  Authentication: 2.
  Sender authentication resistant to key-compromise impersonation (KCI).  The
  sender authentication is based on an ephemeral-static DH ("es" or "se")
  between the sender's static key pair and the recipient's ephemeral key
  pair.  Assuming the corresponding private keys are secure, this
  authentication cannot be forged.

  Confidentiality: 5.
  Encryption to a known recipient, strong forward secrecy.  This payload is
  encrypted based on an ephemeral-ephemeral DH as well as an ephemeral-static
  DH with the recipient's static key pair.  Assuming the ephemeral private
  keys are secure, and the recipient is not being actively impersonated by an
  attacker that has stolen its static private key, this payload cannot be
  decrypted.

  "s": Alice writes her static public key from the s variable into the
  message buffer, encrypting it, and hashes the output along with the old h
  to derive a new h.

  "se": A DH is performed between the Alice's static key pair and the Bob's
  ephemeral key pair.  The result is hashed along with the old ck to derive a
  new ck and k, and n is set to zero.
```
这包含两个 ChaChaPoly 帧。第一个是 Alice 加密的静态公钥。第二个是 Noise 载荷：Alice 加密的 RouterInfo、可选选项和可选填充。它们使用不同的密钥，因为在两者之间调用了 MixKey() 函数。

原始内容：

```
+----+----+----+----+----+----+----+----+
|                                       |
+   ChaCha20 encrypted data (32 bytes)  +
|   Alice static key S                  |
+     k defined in KDF for message 2    +
|   n = 1 see KDF for associated data   |
+----+----+----+----+----+----+----+----+
|                                       |
+        Poly1305 MAC (16 bytes)        +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+   ChaCha20 encrypted data             +
|     Length specified in message 1     |
+     (including 16 byte MAC to follow) +
|                                       |
+       Alice RouterInfo                +
|       using block format 2            |
+       Alice Options (optional)        +
|       using block format 1            |
+       Arbitrary padding               +
|       using block format 254          |
+                                       +
| k defined in KDF for message 3 part 2 |
+     n = 0                             +
|     see KDF for associated data       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+        Poly1305 MAC (16 bytes)        +
|                                       |
+----+----+----+----+----+----+----+----+

S :: 32 bytes, ChaChaPoly encrypted Alice's X25519 static key, little endian
     inside 48 byte ChaChaPoly frame
```
未加密数据（未显示 Poly1305 认证标签）：

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|              S                        |
+       Alice static key                +
|          (32 bytes)                   |
+                                       +
|                                       |
+                                       +
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|                                       |
+                                       +
|       Alice RouterInfo block          |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+       Optional Options block          +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+       Optional Padding block          +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

S :: 32 bytes, Alice's X25519 static key, little endian
```
#### 注释

- Bob必须执行常规的Router Info验证。确保签名类型受支持，验证签名，验证时间戳在范围内，以及任何其他必要的检查。

- Bob 必须验证在第一帧中收到的 Alice 的静态密钥与 Router Info 中的静态密钥匹配。Bob 必须首先在 Router Info 中搜索具有匹配版本 (v) 选项的 NTCP 或 NTCP2 Router Address。请参见下面的已发布 Router Info 和未发布 Router Info 章节。

- 如果 Bob 在他的 netDb 中有 Alice 的 RouterInfo 的较旧版本，验证 router info 中的静态密钥在两个版本中是否相同（如果存在），以及较旧版本是否少于 XXX 时间（参见下面的密钥轮换时间）

- Bob 必须在此验证 Alice 的静态密钥是曲线上的有效点。

- 应该包含选项，以指定填充参数。

- 在任何错误情况下，包括 AEAD、RI、DH、时间戳或密钥验证失败，Bob 必须停止进一步的消息处理并关闭连接而不响应。这应该是异常关闭（TCP RST）。

- 为了促进快速握手，实现必须确保 Alice 缓冲然后一次性刷新第三条消息的全部内容，包括两个 AEAD 帧。这增加了数据被包含在单个 TCP 数据包中的可能性（除非被操作系统或中间件分段），并且被 Bob 一次性接收。这也是为了提高效率并确保随机填充的有效性。

- 消息 3 第 2 部分帧长度：此帧的长度（包括 MAC）由 Alice 在消息 1 中发送。请参阅该消息，了解关于为填充预留足够空间的重要说明。

- 消息3第2部分帧内容：此帧的格式与数据阶段帧的格式相同，除了帧长度由Alice在消息1中发送。数据阶段帧格式见下文。该帧必须按以下顺序包含1到3个块：

1)  Alice 的 Router Info 块（必需）   2)  选项块（可选）

3\) 填充块（可选）此帧绝不能包含任何其他块类型。

- 如果 Alice 在消息 3 的末尾附加一个数据阶段帧（可选择包含填充）并同时发送两者，则不需要消息 3 第 2 部分填充，因为对观察者来说这将显示为一个大的字节流。由于 Alice 通常（但不总是）会有 I2NP 消息要发送给 Bob（这就是她连接到他的原因），为了效率和确保随机填充的有效性，这是推荐的实现方式。

- 消息3 AEAD帧（部分1和部分2）的理论最大总长度为65535字节；部分1为48字节，因此部分2的最大帧长度为65487字节；部分2的最大明文长度（不含MAC）为65471字节。
  警告：某些实现强制使用小得多的长度。Java I2P目前将总长度限制为4096字节。请勿添加过多填充。

### 密钥派生函数 (KDF) (用于数据阶段)

数据阶段使用零长度关联数据输入。

KDF 从链式密钥 ck 生成两个密码密钥 k_ab 和 k_ba，使用 [RFC-2104](https://tools.ietf.org/html/rfc2104) 中定义的 HMAC-SHA256(key, data)。这是 Split() 函数，与 Noise 规范中的定义完全一致。

```
ck = from handshake phase

// k_ab, k_ba = HKDF(ck, zerolen)
// ask_master = HKDF(ck, zerolen, info="ask")

// zerolen is a zero-length byte array
temp_key = HMAC-SHA256(ck, zerolen)
// overwrite the chaining key in memory, no longer needed
ck = (all zeros)

// Output 1
// cipher key, for Alice transmits to Bob (Noise doesn't make clear which is which, but Java code does)
k_ab =   HMAC-SHA256(temp_key, byte(0x01)).

// Output 2
// cipher key, for Bob transmits to Alice (Noise doesn't make clear which is which, but Java code does)
k_ba =   HMAC-SHA256(temp_key, k_ab || byte(0x02)).


KDF for SipHash for length field:
Generate an Additional Symmetric Key (ask) for SipHash
SipHash uses two 8-byte keys (big endian) and 8 byte IV for first data.

// "ask" is 3 bytes, US-ASCII, no null termination
ask_master = HMAC-SHA256(temp_key, "ask" || byte(0x01))
// sip_master = HKDF(ask_master, h || "siphash")
// "siphash" is 7 bytes, US-ASCII, no null termination
// overwrite previous temp_key in memory
// h is from KDF for message 3 part 2
temp_key = HMAC-SHA256(ask_master, h || "siphash")
// overwrite ask_master in memory, no longer needed
ask_master = (all zeros)
sip_master = HMAC-SHA256(temp_key, byte(0x01))

Alice to Bob SipHash k1, k2, IV:
// sipkeys_ab, sipkeys_ba = HKDF(sip_master, zerolen)
// overwrite previous temp_key in memory
temp_key = HMAC-SHA256(sip_master, zerolen)
// overwrite sip_master in memory, no longer needed
sip_master = (all zeros)

sipkeys_ab = HMAC-SHA256(temp_key, byte(0x01)).
sipk1_ab = sipkeys_ab[0:7], little endian
sipk2_ab = sipkeys_ab[8:15], little endian
sipiv_ab = sipkeys_ab[16:23]

Bob to Alice SipHash k1, k2, IV:

sipkeys_ba = HMAC-SHA256(temp_key, sipkeys_ab || byte(0x02)).
sipk1_ba = sipkeys_ba[0:7], little endian
sipk2_ba = sipkeys_ba[8:15], little endian
sipiv_ba = sipkeys_ba[16:23]

// overwrite the temp_key in memory, no longer needed
temp_key = (all zeros)
```
### 4) 数据阶段

Noise payload：如下所定义，包括随机填充 Non-noise payload：无

从消息3的第2部分开始，所有消息都在一个经过认证和加密的ChaChaPoly"帧"内，前面附加了两字节的混淆长度。所有填充都在帧内部。帧内部是标准格式，包含零个或多个"块"。每个块都有一个单字节类型和两字节长度。类型包括日期/时间、I2NP消息、选项、终止和填充。

注意：Bob 可以（但不是必须）在数据阶段向 Alice 发送的第一条消息中包含他的 RouterInfo。

（有效载荷安全属性来自 [Noise](https://noiseprotocol.org/noise.html) ）

```
XK(s, rs):           Authentication   Confidentiality
  <-                        2                5
  ->                        2                5

  Authentication: 2.
  Sender authentication resistant to key-compromise impersonation (KCI).
  The sender authentication is based on an ephemeral-static DH ("es" or "se")
  between the sender's static key pair and the recipient's ephemeral key pair.
  Assuming the corresponding private keys are secure, this authentication cannot be forged.

  Confidentiality: 5.
  Encryption to a known recipient, strong forward secrecy.
  This payload is encrypted based on an ephemeral-ephemeral DH as well as
  an ephemeral-static DH with the recipient's static key pair.
  Assuming the ephemeral private keys are secure, and the recipient is not being actively impersonated
  by an attacker that has stolen its static private key, this payload cannot be decrypted.
```
#### 注释

- 为了提高效率并最大限度地减少长度字段的识别，实现必须确保发送方缓冲然后一次性刷新数据消息的全部内容，包括长度字段和AEAD帧。这增加了数据包含在单个TCP数据包中的可能性（除非被操作系统或中间设备分段），并且能够被对方一次性接收。这也是为了提高效率并确保随机填充的有效性。
- router可以选择在AEAD错误时终止会话，或者可以继续尝试通信。如果继续，router应该在重复错误后终止连接。

#### SipHash 混淆长度

参考资料：[SipHash](https://www.131002.net/siphash/)

一旦双方完成握手，它们就会传输负载，这些负载随后在ChaChaPoly"帧"中进行加密和身份验证。

每个帧前面都有一个两字节长度字段，采用大端序。这个长度指定了后续加密帧字节的数量，包括MAC。为了避免在流中传输可识别的长度字段，帧长度通过与从数据阶段KDF初始化的SipHash派生的掩码进行异或运算来进行混淆。请注意，两个方向具有来自KDF的唯一SipHash密钥和IV。

```
    sipk1, sipk2 = The SipHash keys from the KDF.  (two 8-byte long integers)
    IV[0] = sipiv = The SipHash IV from the KDF. (8 bytes)
    length is big endian.
    For each frame:
      IV[n] = SipHash-2-4(sipk1, sipk2, IV[n-1])
      Mask[n] = First 2 bytes of IV[n]
      obfuscatedLength = length ^ Mask[n]

    The first length output will be XORed with with IV[1].
```
接收方拥有相同的SipHash密钥和IV。解码长度是通过推导用于混淆长度的掩码，并将截断的摘要进行异或运算来获得帧的长度。帧长度是包括MAC在内的加密帧的总长度。

#### 注释

- 如果您使用返回无符号长整数的 SipHash 库函数，请使用最低有效两个字节作为 Mask。将长整数转换为小端序作为下一个 IV。

#### 原始内容

```
+----+----+----+----+----+----+----+----+
|obf size |                             |
+----+----+                             +
|                                       |
+   ChaChaPoly frame                    +
|   Encrypted and authenticated         |
+   key is k_ab for Alice to Bob        +
|   key is k_ba for Bob to Alice        |
+   as defined in KDF for data phase    +
|   n starts at 0 and increments        |
+   for each frame in that direction    +
|   no associated data                  |
+   16 bytes minimum                    +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

obf size :: 2 bytes length obfuscated with SipHash
            when de-obfuscated: 16 - 65535

Minimum size including length field is 18 bytes.
Maximum size including length field is 65537 bytes.
Obfuscated length is 2 bytes.
Maximum ChaChaPoly frame is 65535 bytes.
```
#### 注释

- 由于接收方必须获得完整的帧才能检查MAC，建议发送方将帧限制在几KB而不是最大化帧大小。这将最小化接收方的延迟。

#### 未加密数据

加密帧中包含零个或多个块。每个块包含一个单字节标识符、一个双字节长度和零个或多个数据字节。

为了扩展性，接收方必须忽略具有未知标识符的块，并将它们视为填充。

加密数据最大为 65535 字节，包括 16 字节的身份验证头，因此最大未加密数据为 65519 字节。

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
       0 for datetime
       1 for options
       2 for RouterInfo
       3 for I2NP message
       4 for termination
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

在握手消息 3 第 2 部分中，顺序必须是：RouterInfo，如果存在则跟随 Options，如果存在则跟随 Padding。不允许其他块。

在数据阶段，顺序未指定，除了以下要求：如果存在填充，则必须是最后一个块。如果存在终止，则必须是除填充之外的最后一个块。

一个帧中可能包含多个 I2NP 块。不允许在一个帧中包含多个 Padding 块。其他块类型可能不会在一个帧中包含多个块，但这并不被禁止。

#### 日期时间

时间同步的特殊情况：

```
+----+----+----+----+----+----+----+
| 0  |    4    |     timestamp     |
+----+----+----+----+----+----+----+

blk :: 0
size :: 2 bytes, big endian, value = 4
timestamp :: Unix timestamp, unsigned seconds.
             Wraps around in 2106
```
注意：实现必须四舍五入到最近的秒数，以防止网络中的时钟偏差。

#### 选项

传递更新的选项。选项包括：最小和最大填充。

选项块将是可变长度的。

```
+----+----+----+----+----+----+----+----+
| 1  |  size   |tmin|tmax|rmin|rmax|tdmy|
+----+----+----+----+----+----+----+----+
|tdmy|  rdmy   |  tdelay |  rdelay |    |
~----+----+----+----+----+----+----+    ~
|              more_options             |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 1
size :: 2 bytes, big endian, size of options to follow, 12 bytes minimum

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

Padding distribution specified as additional parameters?
Random delay specified as additional parameters?

more_options :: Format TBD
```
#### 选项问题

- 选项格式待定。
- 选项协商待定。

#### RouterInfo

将 Alice 的 RouterInfo 传递给 Bob。在握手消息 3 第 2 部分中使用。将 Alice 的 RouterInfo 传递给 Bob，或将 Bob 的传递给 Alice。在数据阶段可选使用。

```
+----+----+----+----+----+----+----+----+
| 2  |  size   |flg |    RouterInfo     |
+----+----+----+----+                   +
| (Alice RI in handshake msg 3 part 2)  |
~ (Alice, Bob, or third-party           ~
|  RI in data phase)                    |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 2
size :: 2 bytes, big endian, size of flag + router info to follow
flg :: 1 byte flags
       bit order: 76543210
       bit 0: 0 for local store, 1 for flood request
       bits 7-1: Unused, set to 0 for future compatibility
routerinfo :: Alice's or Bob's RouterInfo
```
#### 注意事项

- 当在数据阶段使用时，接收方（Alice或Bob）应验证这是与最初发送（对于Alice）或发送给（对于Bob）的相同的Router Hash。然后，将其视为本地I2NP DatabaseStore消息。验证签名，验证更新的时间戳，并存储在本地netDb中。如果标志位0为1，且接收方是floodfill，则将其视为带有非零回复令牌的DatabaseStore消息，并将其泛洪到最近的floodfill。
- Router Info不会用gzip压缩（与DatabaseStore消息中的情况不同，在那里它是压缩的）
- 除非RouterInfo中有已发布的RouterAddresses，否则不得请求泛洪。除非RouterInfo中有已发布的RouterAddresses，否则接收路由器不得泛洪RouterInfo。
- 实现者必须确保在读取块时，格式错误或恶意数据不会导致读取溢出到下一个块。
- 此协议不提供RouterInfo已被接收、存储或泛洪的确认（无论是在握手阶段还是数据阶段）。如果需要确认，且接收方是floodfill，发送方应改为发送带有回复令牌的标准I2NP DatabaseStoreMessage。

#### 问题

- 也可以在数据阶段使用，而不是使用 I2NP DatabaseStoreMessage。例如，Bob 可以使用它来启动数据阶段。
- 是否允许此消息包含除发起者之外的其他路由器的 RI，作为 DatabaseStoreMessages 的通用替代，例如用于 floodfill 的泛洪？

#### I2NP 消息

一个带有修改过的头部的单个 I2NP 消息。I2NP 消息不能跨块或跨 ChaChaPoly 帧进行分片。

这使用标准 NTCP I2NP 头部的前 9 个字节，并移除头部的最后 7 个字节，具体如下：将过期时间从 8 字节缩短为 4 字节（使用秒而不是毫秒，与 SSU 相同），移除 2 字节长度字段（使用块大小 - 9），并移除单字节 SHA256 校验和。

```
+----+----+----+----+----+----+----+----+
| 3  |  size   |type|    msg id         |
+----+----+----+----+----+----+----+----+
|   short exp       |     message       |
+----+----+----+----+                   +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 3
size :: 2 bytes, big endian, size of type + msg id + exp + message to follow
        I2NP message body size is (size - 9).
type :: 1 byte, I2NP msg type, see I2NP spec
msg id :: 4 bytes, big endian, I2NP message ID
short exp :: 4 bytes, big endian, I2NP message expiration, Unix timestamp, unsigned seconds.
             Wraps around in 2106
message :: I2NP message body
```
#### 注释

- 实现者必须确保在读取块时，格式错误或恶意数据不会导致读取越界到下一个块中。

#### 终止

Noise 建议使用显式终止消息。原始的 NTCP 没有这样的消息。断开连接。这必须是帧中最后一个非填充块。

```
+----+----+----+----+----+----+----+----+
| 4  |  size   |    valid data frames   |
+----+----+----+----+----+----+----+----+
    received   | rsn|     addl data     |
+----+----+----+----+                   +
~               .   .   .               ~
+----+----+----+----+----+----+----+----+

blk :: 4
size :: 2 bytes, big endian, value = 9 or more
valid data frames received :: The number of valid AEAD data phase frames received
                              (current receive nonce value)
                              0 if error occurs in handshake phase
                              8 bytes, big endian
rsn :: reason, 1 byte:
       0: normal close or unspecified
       1: termination received
       2: idle timeout
       3: router shutdown
       4: data phase AEAD failure
       5: incompatible options
       6: incompatible signature type
       7: clock skew
       8: padding violation
       9: AEAD framing error
       10: payload format error
       11: message 1 error
       12: message 2 error
       13: message 3 error
       14: intra-frame read timeout
       15: RI signature verification fail
       16: s parameter missing, invalid, or mismatched in RouterInfo
       17: banned
addl data :: optional, 0 or more bytes, for future expansion, debugging,
             or reason text.
             Format unspecified and may vary based on reason code.
```
#### 注释

并非所有原因都可能被实际使用，这取决于具体实现。握手失败通常会导致使用 TCP RST 关闭连接。请参阅上述握手消息部分的说明。列出的其他原因是为了保持一致性、日志记录、调试或应对策略变更。

#### 填充

这是用于AEAD帧内部的填充。消息1和消息2的填充在AEAD帧外部。消息3和数据阶段的所有填充都在AEAD帧内部。

AEAD 内的填充应大致遵循协商的参数。Bob 在消息 2 中发送了他请求的发送/接收最小/最大参数。Alice 在消息 3 中发送了她请求的发送/接收最小/最大参数。在数据阶段可能会发送更新的选项。请参见上面的选项块信息。

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
size :: 2 bytes, big endian, size of padding to follow
padding :: random data
```
#### 注意事项

- 允许大小 = 0。
- 填充策略待定。
- 最小填充待定。
- 允许仅包含填充的帧。
- 填充默认值待定。
- 参见选项块中的填充参数协商
- 参见选项块中的最小/最大填充参数
- Noise 协议将消息限制为 64KB。如果需要更多填充，请发送多个帧。
- router 对违反协商填充的响应取决于具体实现。

#### 其他区块类型

实现应该忽略未知的块类型以保持向前兼容性，但在消息3第2部分中除外，该部分不允许未知块。

#### 未来工作

- 填充长度可以基于每条消息决定并估算长度分布，或者应该添加随机延迟。这些对策需要包含在内以抵御DPI，因为消息大小会泄露传输协议正在承载I2P流量。确切的填充方案是未来工作的一个领域。

### 5) 终止

连接可能通过正常或异常的TCP套接字关闭来终止，或者如Noise建议的那样，通过显式终止消息来终止。显式终止消息在上面的数据阶段中定义。

在任何正常或异常终止时，router 应该清零所有内存中的临时数据，包括握手临时密钥、对称加密密钥和相关信息。

## 已发布的 Router 信息

### 功能特性

从 0.9.50 版本开始，NTCP2 地址支持"caps"选项，类似于 SSU。可以在"caps"选项中发布一个或多个能力。能力可以按任意顺序排列，但建议使用"46"顺序，以保持各实现间的一致性。定义了两种能力：

4: 表示出站 IPv4 能力。如果在 host 字段中发布了 IP 地址，则不需要此能力。如果 router 是隐藏的，或者 NTCP2 仅用于出站，'4' 和 '6' 可以在单个地址中组合使用。

6: 表示出站IPv6能力。如果在host字段中发布了IP地址，则不需要此能力。如果router是隐藏的，或者NTCP2仅支持出站，'4'和'6'可以在单个地址中组合使用。

### 已发布地址

已发布的 RouterAddress（RouterInfo 的一部分）将具有 "NTCP" 或 "NTCP2" 的协议标识符。

RouterAddress 必须包含 "host" 和 "port" 选项，就像当前的 NTCP 协议一样。

RouterAddress 必须包含三个选项来表示 NTCP2 支持：

- s=(Base64 密钥) 此 RouterAddress 的当前 Noise 静态公钥 (s)。使用标准 I2P Base 64 字母表进行 Base 64 编码。二进制 32 字节，Base 64 编码后 44 字节，小端序 X25519 公钥。
- i=(Base64 IV) 此 RouterAddress 用于在消息 1 中加密 X 值的当前 IV。使用标准 I2P Base 64 字母表进行 Base 64 编码。二进制 16 字节，Base 64 编码后 24 字节，大端序。
- v=2 当前版本 (2)。当发布为"NTCP"时，暗示额外支持版本 1。未来版本的支持将使用逗号分隔的值，例如 v=2,3。实现应验证兼容性，如果存在逗号则包括多个版本。逗号分隔的版本必须按数字顺序排列。

Alice 必须验证所有三个选项都存在且有效，然后才能使用 NTCP2 协议进行连接。

当以"NTCP"发布并带有"s"、"i"和"v"选项时，router必须在该主机和端口上接受NTCP和NTCP2协议的传入连接，并自动检测协议版本。

当发布为带有 "s"、"i" 和 "v" 选项的 "NTCP2" 时，router 仅接受该主机和端口上 NTCP2 协议的传入连接。

如果一个 router 同时支持 NTCP1 和 NTCP2 连接，但没有实现入站连接的自动版本检测，它必须同时广播 "NTCP" 和 "NTCP2" 地址，并且只在 "NTCP2" 地址中包含 NTCP2 选项。router 应该在 "NTCP2" 地址中设置更低的成本值（更高的优先级），而不是在 "NTCP" 地址中，这样 NTCP2 就会被优先选择。

如果在同一个 RouterInfo 中发布了多个 NTCP2 RouterAddress（无论是 "NTCP" 还是 "NTCP2"）（用于额外的 IP 地址或端口），所有指定相同端口的地址必须包含相同的 NTCP2 选项和值。特别是，所有地址都必须包含相同的静态密钥和 iv。

### 未发布的 NTCP2 地址

如果Alice没有发布她的NTCP2地址（作为"NTCP"或"NTCP2"）用于接收连接，她必须发布一个只包含她的静态密钥和NTCP2版本的"NTCP2" router地址，这样Bob在消息3第2部分接收到Alice的RouterInfo后可以验证该密钥。

- s=(Base64 key) 如上所述，用于已发布地址。
- v=2 如上所述，用于已发布地址。

此 router 地址不会包含 "i"、"host" 或 "port" 选项，因为出站 NTCP2 连接不需要这些选项。此地址的已发布成本并不严格重要，因为它仅用于入站连接；不过，如果成本设置得比其他地址更高（优先级更低），可能对其他 router 有帮助。建议值为 14。

Alice 也可以简单地在现有已发布的 "NTCP" 地址中添加 "s" 和 "v" 选项。

### 公钥和IV轮换

由于对RouterInfo的缓存，router在运行时不得轮换静态公钥或IV，无论是否在已发布的地址中。Router必须持久化存储此密钥和IV以便在立即重启后重复使用，这样传入连接将继续工作，且重启时间不会暴露。Router必须持久化存储或以其他方式确定上次关闭时间，以便在启动时可以计算出之前的停机时间。

考虑到暴露重启时间的担忧，如果router之前已经离线一段时间（至少几个小时），router可能会在启动时轮换这个密钥或初始化向量。

如果router具有任何已发布的NTCP2 RouterAddresses（作为NTCP或NTCP2），则轮换前的最小停机时间应该更长，例如一个月，除非本地IP地址已更改或router进行"重新生成密钥"操作。

如果 router 有任何已发布的 SSU RouterAddresses，但没有 NTCP2（作为 NTCP 或 NTCP2），那么轮换前的最小停机时间应该更长，例如一天，除非本地 IP 地址已更改或 router "重新生成密钥"。即使已发布的 SSU 地址有引荐者，这也适用。

如果 router 没有任何已发布的 RouterAddresses（NTCP、NTCP2 或 SSU），轮换前的最短停机时间可能只有两小时，即使 IP 地址发生变化，除非 router 进行"重新生成密钥"操作。

如果 router 重新生成密钥到不同的 Router Hash，它也应该生成新的 noise 密钥和 IV。

实现必须意识到，更改静态公钥或IV将阻止来自缓存了旧RouterInfo的router的传入NTCP2连接。RouterInfo发布、tunnel对等节点选择（包括OBGW和IB最近跳）、零跳tunnel选择、传输选择和其他实现策略都必须考虑到这一点。

IV轮换遵循与密钥轮换相同的规则，除了IV只存在于已发布的RouterAddresses中，因此隐藏或防火墙后的router没有IV。如果有任何变化（版本、密钥、选项？），建议IV也应该相应改变。

注意：重新生成密钥前的最小停机时间可能会被修改，以确保网络健康，并防止因中等时长停机的 router 进行重新播种。

## 版本检测

当发布为"NTCP"时，router必须自动检测传入连接的协议版本。

这种检测是依赖于实现的，但这里提供一些通用指导。

为了检测传入 NTCP 连接的版本，Bob 按以下步骤进行：

- 等待至少 64 字节（NTCP2 消息 1 的最小大小）

- 如果初始接收到的数据是288字节或更多，则传入连接是版本1。

- 如果小于 288 字节，则

> - 等待短时间以获取更多数据（在NTCP2广泛采用之前的好策略），如果总共收到至少288字节，则为NTCP 1。   >   > - 尝试将前几个阶段解码为版本2，如果失败，等待短时间以获取更多数据（NTCP2广泛采用后的好策略）   >   >   > - 使用AES-256和密钥RH_B解密SessionRequest数据包的前32字节（X密钥）。   >   > - 验证曲线上的有效点。如果失败，为NTCP 1等待短时间以获取更多数据   >   > - 验证AEAD帧。如果失败，为NTCP 1等待短时间以获取更多数据

请注意，如果我们检测到对 NTCP 1 的主动 TCP 分段攻击，可能会建议进行更改或采用其他策略。

为了便于快速版本检测和握手，实现必须确保 Alice 缓冲然后一次性刷新第一条消息的全部内容，包括填充数据。这增加了数据包含在单个 TCP 数据包中的可能性（除非被操作系统或中间设备分段），并且 Bob 能够一次性接收到所有数据。这也是为了提高效率并确保随机填充的有效性。这适用于 NTCP 和 NTCP2 握手。

## 变体、后备方案和一般问题

- 如果 Alice 和 Bob 都支持 NTCP2，Alice 应该使用 NTCP2 连接。
- 如果 Alice 因任何原因无法使用 NTCP2 连接到 Bob，连接失败。Alice 不得使用 NTCP 1 重试。

## 时钟偏差指南

对等节点时间戳包含在前两个握手消息中：Session Request 和 Session Created。两个对等节点之间超过 +/- 60 秒的时钟偏差通常是致命的。如果 Bob 认为他的本地时钟有问题，他可以使用计算出的偏差或某些外部源来调整他的时钟。否则，即使超过了最大偏差，Bob 也应该回复 Session Created，而不是简单地关闭连接。这允许 Alice 获取 Bob 的时间戳并计算偏差，必要时采取行动。此时 Bob 还没有 Alice 的 router 身份，但为了节约资源，Bob 可能希望在一段时间内禁止来自 Alice IP 的传入连接，或者在多次连接尝试都出现过度偏差后进行禁止。

Alice应该通过减去一半的RTT来调整计算出的时钟偏差。如果Alice认为她的本地时钟有问题，她可以使用计算出的偏差或某些外部源来调整她的时钟。如果Alice认为Bob的时钟有问题，她可以在一段时间内封禁Bob。无论哪种情况，Alice都应该关闭连接。

如果Alice确实回复了Session Confirmed消息（可能是因为时钟偏差非常接近60秒的限制，并且由于RTT的原因，Alice和Bob的计算结果并不完全相同），Bob应该通过减去RTT的一半来调整计算出的时钟偏差。如果调整后的时钟偏差超过了最大值，Bob应该回复一个包含时钟偏差原因码的Disconnect消息，并关闭连接。此时，Bob已经获得了Alice的router身份，并可能在一段时间内禁止Alice。

## 参考文献

- [通用结构](/docs/specs/common-structures)
- [I2NP](/docs/specs/i2np)
- [网络数据库](/docs/overview/network-database)
- [NOISE - Noise 协议框架](https://noiseprotocol.org/noise.html)
- [NTCP](/docs/transport/ntcp)
- [Prop104](/proposals/104-tls-transport)
- [Prop109](/proposals/109-pt-transport)
- [Prop111](/proposals/111-ntcp-2)
- [RFC-2104 - HMAC](https://tools.ietf.org/html/rfc2104)
- [RFC-3526 - DH 组](https://tools.ietf.org/html/rfc3526)
- [RFC-6151](https://tools.ietf.org/html/rfc6151)
- [RFC-7539 - ChaCha20-Poly1305](https://tools.ietf.org/html/rfc7539)
- [RFC-7748 - X25519](https://tools.ietf.org/html/rfc7748)
- [RFC-7905](https://tools.ietf.org/html/rfc7905)
- [SipHash](https://www.131002.net/siphash/)
- [SSU](/docs/transport/ssu)
- **[STS]** Diffie, W.; van Oorschot P. C.; Wiener M. J., 认证与认证密钥交换
