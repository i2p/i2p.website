---
title: "ECIES Tunnels"
aliases:
  - "/zh/proposals/152-ecies-config"
  - "/zh/proposals/152-ecies-config/"
  - "/zh/proposals/152"
  - "/zh/proposals/152/"
number: "152"
author: "chisana, zzz, orignal"
created: "2019-07-04"
lastupdated: "2025-03-05"
status: "Closed"
thread: "http://zzz.i2p/topics/2737"
target: "0.9.48"
implementedin: "0.9.48"
toc: true
---

## 注意

网络部署和测试正在进行中。   可能进行小幅修订。   参见 [SPEC](/docs/specs/tunnel-implementation/) 获取官方规范。

## 概述

本文档提议对隧道构建消息的加密方式进行修改，   使用 [ECIES-X25519](/docs/specs/ecies/) 引入的密码原语。   这是整体提案 [Proposal 156](/proposals/156-ecies-routers) 的一部分，   旨在将路由器从 ElGamal 迁移至 ECIES-X25519 密钥。

为实现网络从 ElGamal + AES256 到 ECIES + ChaCha20 的过渡，   需要支持包含混合 ElGamal 和 ECIES 路由器的隧道。   本文档提供了处理混合隧道跳点的规范。   ElGamal 跳点的格式、处理和加密方式不会做任何更改。

使用 ElGamal 的隧道创建者需要为每个跳点生成临时的 X25519 密钥对，   并遵循本规范创建包含 ECIES 跳点的隧道。

本提案指定了实现 ECIES-X25519 隧道构建所需的变化。   如需了解 ECIES 路由器所需的所有变更概览，请参见提案 156 [Proposal 156](/proposals/156-ecies-routers)。

本提案保持了隧道构建记录的大小不变，   以确保兼容性。更小的构建记录和消息将在后续实现——参见 [Proposal 157](/proposals/157-new-tbm)。

### 密码原语

不引入新的密码原语。实现本提案所需的密码原语包括：

- AES-256-CBC，见 [Cryptography](/docs/specs/cryptography/)
- STREAM ChaCha20/Poly1305 函数：  
  ENCRYPT(k, n, plaintext, ad) 和 DECRYPT(k, n, ciphertext, ad) —— 见 [NTCP2](/docs/specs/ntcp2/) [ECIES-X25519](/docs/specs/ecies/) 和 [RFC-7539](https://tools.ietf.org/html/rfc7539)
- X25519 DH 函数 —— 见 [NTCP2](/docs/specs/ntcp2/) 和 [ECIES-X25519](/docs/specs/ecies/)
- HKDF(salt, ikm, info, n) —— 见 [NTCP2](/docs/specs/ntcp2/) 和 [ECIES-X25519](/docs/specs/ecies/)

其他在别处定义的 Noise 函数：

- MixHash(d) —— 见 [NTCP2](/docs/specs/ntcp2/) 和 [ECIES-X25519](/docs/specs/ecies/)
- MixKey(d) —— 见 [NTCP2](/docs/specs/ntcp2/) 和 [ECIES-X25519](/docs/specs/ecies/)

### 目标

- 提高密码操作速度
- 使用 ECIES 原语替换 ElGamal + AES256/CBC，用于 Tunnel BuildRequestRecords 和 BuildReplyRecords
- 加密后的 BuildRequestRecords 和 BuildReplyRecords 大小不变（528 字节），以确保兼容性
- 不引入新的 I2NP 消息
- 保持加密构建记录的大小以确保兼容性
- 为隧道构建消息添加前向保密性
- 添加认证加密
- 检测构建请求记录的跳点重排序
- 提高时间戳分辨率，以便减少 Bloom 过滤器的大小
- 添加隧道过期字段，以支持可变隧道生命周期（仅限全 ECIES 隧道）
- 添加可扩展的选项字段以支持未来功能
- 复用现有密码原语
- 在保持兼容性的同时尽可能提升隧道构建消息的安全性
- 支持混合 ElGamal/ECIES 对等体的隧道
- 增强对构建消息“标记”攻击的防御能力
- 跳点在处理构建消息时无需提前知道下一跳的加密类型，  
  因为此时可能尚未获取下一跳的 RI
- 最大限度保持与当前网络的兼容性
- 不改变 ElGamal 路由器的隧道 AES 请求/回复加密
- 不改变隧道 AES “层” 加密，相关内容见 [Proposal 153](/proposals/153-chacha20-layer-encryption)
- 继续支持 8 条记录的 TBM/TBRM 和可变大小的 VTBM/VTBRM
- 不要求全网“旗帜日”式升级

### 非目标

- 重新设计隧道构建消息，要求“旗帜日”式升级
- 缩小隧道构建消息（需要全 ECIES 跳点和新提案）
- 使用 [Proposal 143](/proposals/143-build-message-options) 中定义的隧道构建选项，仅小消息需要
- 双向隧道 —— 参见 [Proposal 119](/proposals/119-bidirectional-tunnels)
- 更小的隧道构建消息 —— 参见 [Proposal 157](/proposals/157-new-tbm)

## 威胁模型

### 设计目标

- 任何跳点都无法确定隧道的发起者。

- 中间跳点必须无法确定隧道的方向或其在隧道中的位置。

- 任何跳点都无法读取其他请求或回复记录的内容，  
  除了下一跳的截断路由器哈希和临时密钥。

- 出站构建的回复隧道成员无法读取任何回复记录。

- 入站构建的出站隧道成员无法读取任何请求记录，  
  但 OBEP 可以看到下一跳的截断路由器哈希和临时密钥（IBGW）

### 标记攻击

隧道构建设计的主要目标之一是使共谋路由器 X 和 Y 更难确认它们处于同一隧道中。   如果路由器 X 在第 m 跳，路由器 Y 在第 m+1 跳，它们显然会知道；   但如果路由器 X 在第 m 跳，而路由器 Y 在第 m+n 跳（n>1），这应困难得多。

标记攻击是指中间跳点 X 以某种方式修改隧道构建消息，   使得路由器 Y 在收到消息时能够检测到该修改。   目标是使任何被修改的消息在到达路由器 Y 之前被 X 和 Y 之间的某个路由器丢弃。   对于未被丢弃而到达路由器 Y 的修改，隧道创建者应在回复中检测到损坏并丢弃该隧道。

可能的攻击方式：

- 修改一条构建记录
- 替换一条构建记录
- 添加或删除一条构建记录
- 重新排序构建记录

TODO: 当前设计是否能防止所有这些攻击？

## 设计

### Noise 协议框架

本提案基于 Noise 协议框架 [NOISE](https://noiseprotocol.org/noise.html)（修订版 34，2018-07-11）提出要求。   在 Noise 术语中，Alice 是发起方，Bob 是响应方。

本提案基于 Noise 协议 Noise_N_25519_ChaChaPoly_SHA256。   该 Noise 协议使用以下原语：

- 单向握手模式：N  
  Alice 不向 Bob 发送其静态密钥（N）

- DH 函数：X25519  
  X25519 DH，密钥长度为 32 字节，如 [RFC-7748](https://tools.ietf.org/html/rfc7748) 所定义。

- 加密函数：ChaChaPoly  
  AEAD_CHACHA20_POLY1305，如 [RFC-7539](https://tools.ietf.org/html/rfc7539) 第 2.8 节所定义。  
  使用 12 字节 nonce，前 4 字节设为零。  
  与 [NTCP2](/docs/specs/ntcp2/) 中的相同。

- 哈希函数：SHA256  
  标准 32 字节哈希，I2P 中已广泛使用。

#### 对框架的补充

无。

### 握手模式

握手使用 [Noise](https://noiseprotocol.org/noise.html) 握手模式。

使用以下字母映射：

- e = 一次性临时密钥
- s = 静态密钥
- p = 消息载荷

构建请求与 Noise N 模式相同。   这也与 [NTCP2](/docs/specs/ntcp2/) 中 XK 模式的第一条消息（会话请求）相同。

```text
<- s
  ...
  e es p ->
```
### 请求加密

构建请求记录由隧道创建者生成，并使用非对称加密发送给各个跳点。   当前的请求记录非对称加密使用 ElGamal，定义见 [Cryptography](/docs/specs/cryptography/)，   并包含 SHA-256 校验和。该设计不具备前向保密性。

新设计将使用单向 Noise 模式“N”，结合 ECIES-X25519 临时-静态 DH、HKDF 和   ChaCha20/Poly1305 AEAD，以实现前向保密、完整性和认证。   Alice 是隧道构建请求方。隧道中的每个跳点都是 Bob。

（载荷安全属性）

```text
N:                      Authentication   Confidentiality
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
### 回复加密

构建回复记录由跳点创建者生成，并使用对称加密发送回创建者。   当前的回复记录对称加密使用 AES，并前置 SHA-256 校验和。   该设计不具备前向保密性。

新设计将使用 ChaCha20/Poly1305 AEAD 实现完整性与认证。

### 理由

请求中的临时公钥无需使用 AES 或 Elligator2 混淆。   只有前一跳能看到它，而前一跳已知下一跳是 ECIES。

回复记录无需使用另一个 DH 进行完整的非对称加密。

## 规范

### 构建请求记录

加密的 BuildRequestRecords 对 ElGamal 和 ECIES 均为 528 字节，以确保兼容性。

#### 请求记录未加密（ElGamal）

作为参考，这是来自 [I2NP](/docs/specs/i2np/) 的 ElGamal 路由器当前隧道 BuildRequestRecord 规范。   未加密数据在加密前会前置一个非零字节和数据的 SHA-256 哈希，   定义见 [Cryptography](/docs/specs/cryptography/)。

所有字段均为大端序。

未加密大小：222 字节

```text
bytes     0-3: tunnel ID to receive messages as, nonzero
  bytes    4-35: local router identity hash
  bytes   36-39: next tunnel ID, nonzero
  bytes   40-71: next router identity hash
  bytes  72-103: AES-256 tunnel layer key
  bytes 104-135: AES-256 tunnel IV key
  bytes 136-167: AES-256 reply key
  bytes 168-183: AES-256 reply IV
  byte      184: flags
  bytes 185-188: request time (in hours since the epoch, rounded down)
  bytes 189-192: next message ID
  bytes 193-221: uninterpreted / random padding
```
#### 请求记录已加密（ElGamal）

作为参考，这是来自 [I2NP](/docs/specs/i2np/) 的 ElGamal 路由器当前隧道 BuildRequestRecord 规范。

加密大小：528 字节

```text
bytes    0-15: Hop's truncated identity hash
  bytes  16-528: ElGamal encrypted BuildRequestRecord
```
#### 请求记录未加密（ECIES）

这是为 ECIES-X25519 路由器提议的隧道 BuildRequestRecord 规范。   变更摘要：

- 移除未使用的 32 字节路由器哈希
- 将请求时间从小时改为分钟
- 添加过期字段以支持未来可变隧道时间
- 增加标志位空间
- 添加映射以支持额外构建选项
- 跳点自身的回复记录不使用 AES-256 回复密钥
- 未加密记录更长，因为加密开销更小

请求记录不包含任何 ChaCha 回复密钥。   这些密钥由 KDF 派生。见下文。

所有字段均为大端序。

未加密大小：464 字节

```text
bytes     0-3: tunnel ID to receive messages as, nonzero
  bytes     4-7: next tunnel ID, nonzero
  bytes    8-39: next router identity hash
  bytes   40-71: AES-256 tunnel layer key
  bytes  72-103: AES-256 tunnel IV key
  bytes 104-135: AES-256 reply key
  bytes 136-151: AES-256 reply IV
  byte      152: flags
  bytes 153-155: more flags, unused, set to 0 for compatibility
  bytes 156-159: request time (in minutes since the epoch, rounded down)
  bytes 160-163: request expiration (in seconds since creation)
  bytes 164-167: next message ID
  bytes   168-x: tunnel build options (Mapping)
  bytes     x-x: other data as implied by flags or options
  bytes   x-463: random padding
```
标志位字段定义见 [Tunnel Creation](/docs/specs/tunnel-implementation/)，包含以下内容：

```text
Bit order: 76543210 (bit 7 is MSB)
bit 7: if set, allow messages from anyone
bit 6: if set, allow messages to anyone, and send the reply to the
       specified next hop in a Tunnel Build Reply Message
bits 5-0: Undefined, must set to 0 for compatibility with future options
```
位顺序：76543210（位 7 为最高位）   位 7：若设置，则允许任何人发送消息   位 6：若设置，则允许向任何人发送消息，并将回复发送到

位 5-0：未定义，为兼容未来选项必须设为 0

位 7 表示该跳点将作为入站网关（IBGW）。位 6   表示该跳点将作为出站端点（OBEP）。若两者均未设置，   该跳点为中间参与者。两者不能同时设置。

#### 请求记录已加密（ECIES）

请求过期时间用于未来可变隧道持续时间。   目前唯一支持的值是 600（10 分钟）。

隧道构建选项是 [Common Structures](/docs/specs/common-structures/) 中定义的映射结构。   供将来使用。目前未定义任何选项。   若映射结构为空，则为两个字节 0x00 0x00。   映射的最大大小（包括长度字段）为 296 字节，   映射长度字段的最大值为 294。

```text
bytes    0-15: Hop's truncated identity hash
  bytes   16-47: Sender's ephemeral X25519 public key
  bytes  48-511: ChaCha20 encrypted BuildRequestRecord
  bytes 512-527: Poly1305 MAC
```
### 构建回复记录

除临时公钥为小端序外，所有字段均为大端序。

#### 回复记录未加密（ElGamal）

加密大小：528 字节

加密的 BuildReplyRecords 对 ElGamal 和 ECIES 均为 528 字节，以确保兼容性。

ElGamal 回复使用 AES 加密。

```text
bytes   0-31: SHA-256 Hash of bytes 32-527
  bytes 32-526: random data
  byte     527: reply

  total length: 528
```
#### 回复记录未加密（ECIES）

所有字段均为大端序。

- 添加构建回复选项的映射
- 未加密记录更长，因为加密开销更小

未加密大小：528 字节

这是为 ECIES-X25519 路由器提议的隧道 BuildReplyRecord 规范。   变更摘要：

ECIES 回复使用 ChaCha20/Poly1305 加密。

```text
bytes    0-x: Tunnel Build Reply Options (Mapping)
  bytes    x-x: other data as implied by options
  bytes  x-510: Random padding
  byte     511: Reply byte
```
所有字段均为大端序。

未加密大小：512 字节

- 0x00（接受）
- 30（TUNNEL_REJECT_BANDWIDTH）

#### 回复记录已加密（ECIES）

隧道构建回复选项是 [Common Structures](/docs/specs/common-structures/) 中定义的映射结构。   供将来使用。目前未定义任何选项。   若映射结构为空，则为两个字节 0x00 0x00。   映射的最大大小（包括长度字段）为 511 字节，   映射长度字段的最大值为 509。

```text
bytes   0-511: ChaCha20 encrypted BuildReplyRecord
  bytes 512-527: Poly1305 MAC
```
回复字节为以下值之一，   定义见 [Tunnel Creation](/docs/specs/tunnel-implementation/)，以避免指纹识别：

### 记录的对称加密

加密大小：528 字节

在完全过渡到 ECIES 记录后，填充规则与请求记录相同。

- “加密”：

  - 密码运行在解密模式
  - 在预处理中预先解密请求记录（隐藏加密的请求记录）

- “解密”：

  - 密码运行在加密模式
  - 跳点通过加密揭示下一个明文请求记录

- ChaCha20 没有“模式”，因此只需运行三次：

  - 预处理时一次
  - 跳点处理时一次
  - 最终回复处理时一次

允许并需要混合隧道，以实现从 ElGamal 到 ECIES 的过渡。   在过渡期间，越来越多的路由器将使用 ECIES 密钥。

对称密码预处理将以相同方式运行：

当使用混合隧道时，隧道创建者需要根据当前和前一跳的加密类型   来决定 BuildRequestRecord 的对称加密方式。

每个跳点将使用自己的加密类型来加密 BuildReplyRecords，   以及 VariableTunnelBuildMessage (VTBM) 中的其他记录。

- 发送方（OBGW） -> ElGamal（H1） -> ECIES（H2） -> ElGamal（H3）

在回复路径上，端点（发送方）需要使用每个跳点的回复密钥   撤销 [Multiple Encryption](https://en.wikipedia.org/wiki/Multiple_encryption)。

作为澄清示例，考虑一个被 ElGamal 包围的 ECIES 出站隧道：

所有 BuildRequestRecords 均处于加密状态（使用 ElGamal 或 ECIES）。

使用 AES256/CBC 时，仍对每条记录单独使用，不跨多条记录链接。

- H3 的记录使用以下方式“加密”：

  - H2 的回复密钥（ChaCha20）
  - H1 的回复密钥（AES256/CBC）

- H2 的记录使用以下方式“加密”：

  - H1 的回复密钥（AES256/CBC）

- H1 的记录无需对称加密直接发出

同样，ChaCha20 将用于加密每条记录，而不是在整个 VTBM 上流式加密。

请求记录由发送方（OBGW）预处理：

- H3 的记录使用以下方式“解密”：

  - H3 的回复密钥（AES256/CBC）

- H2 的记录使用以下方式“解密”：

  - H3 的回复密钥（AES256/CBC）
  - H2 的回复密钥（ChaCha20-Poly1305）

- H1 的记录使用以下方式“解密”：

  - H3 的回复密钥（AES256/CBC）
  - H2 的回复密钥（ChaCha20）
  - H1 的回复密钥（AES256/CBC）

只有 H2 检查回复加密标志，并看到其后跟 AES256/CBC。

- H3 的记录使用以下方式“加密”：

  - H3 的回复密钥（AES256/CBC）

- H2 的记录使用以下方式“加密”：

  - H3 的回复密钥（AES256/CBC）
  - H2 的回复密钥（ChaCha20-Poly1305）

- H1 的记录使用以下方式“加密”：

  - H3 的回复密钥（AES256/CBC）
  - H2 的回复密钥（ChaCha20）
  - H1 的回复密钥（AES256/CBC）

### 请求记录密钥（ECIES）

每个跳点处理后，记录处于“解密”状态：

隧道创建者（即入站端点 IBEP）对回复进行后处理：

#### KDF 用于初始 ck 和 h

这些密钥在 ElGamal BuildRequestRecords 中显式包含。   对于 ECIES BuildRequestRecords，隧道密钥和 AES 回复密钥包含在内，   但 ChaCha 回复密钥由 DH 交换派生。   有关路由器静态 ECIES 密钥的详细信息，参见 [Proposal 156](/proposals/156-ecies-routers)。

```text
This is the "e" message pattern:

  // Define protocol_name.
  Set protocol_name = "Noise_N_25519_ChaChaPoly_SHA256"
  (31 bytes, US-ASCII encoded, no NULL termination).

  // Define Hash h = 32 bytes
  // Pad to 32 bytes. Do NOT hash it, because it is not more than 32 bytes.
  h = protocol_name || 0

  Define ck = 32 byte chaining key. Copy the h data to ck.
  Set chainKey = h

  // MixHash(null prologue)
  h = SHA256(h);

  // up until here, can all be precalculated by all routers.
```
#### KDF 用于请求记录

以下是派生先前在请求记录中传输的密钥的方法描述。

这是标准 [NOISE](https://noiseprotocol.org/noise.html) 对模式“N”使用标准协议名称。

ElGamal 隧道创建者为隧道中的每个 ECIES 跳点生成一个临时 X25519 密钥对，   并使用上述方案加密其 BuildRequestRecord。   ElGamal 隧道创建者将使用本规范之前的方案加密到 ElGamal 跳点。

ECIES 隧道创建者需要使用 [Tunnel Creation](/docs/specs/tunnel-implementation/) 中定义的方案   加密到每个 ElGamal 跳点的公钥。ECIES 隧道创建者将使用上述方案加密到 ECIES 跳点。

这意味着跳点只会看到与其自身加密类型相同的加密记录。

```text
// Each hop's X25519 static keypair (hesk, hepk) from the Router Identity
  hesk = GENERATE_PRIVATE()
  hepk = DERIVE_PUBLIC(hesk)

  // MixHash(hepk)
  // || below means append
  h = SHA256(h || hepk);

  // up until here, can all be precalculated by each router
  // for all incoming build requests

  // Sender generates an X25519 ephemeral keypair per ECIES hop in the VTBM (sesk, sepk)
  sesk = GENERATE_PRIVATE()
  sepk = DERIVE_PUBLIC(sesk)

  // MixHash(sepk)
  h = SHA256(h || sepk);

  End of "e" message pattern.

  This is the "es" message pattern:

  // Noise es
  // Sender performs an X25519 DH with Hop's static public key.
  // Each Hop, finds the record w/ their truncated identity hash,
  // and extracts the Sender's ephemeral key preceding the encrypted record.
  sharedSecret = DH(sesk, hepk) = DH(hesk, sepk)

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // ChaChaPoly parameters to encrypt/decrypt
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  // Save for Reply Record KDF
  chainKey = keydata[0:31]

  // AEAD parameters
  k = keydata[32:63]
  n = 0
  plaintext = 464 byte build request record
  ad = h
  ciphertext = ENCRYPT(k, n, plaintext, ad)

  End of "es" message pattern.

  // MixHash(ciphertext)
  // Save for Reply Record KDF
  h = SHA256(h || ciphertext)
```
对于 ElGamal 和 ECIES 隧道创建者，它们将为每个 ECIES 跳点生成唯一的临时 X25519 密钥对，   用于加密到 ECIES 跳点。

### 请求记录加密（ElGamal）

**重要**：   临时密钥必须在每个 ECIES 跳点和每个构建记录中唯一。   若未使用唯一密钥，共谋跳点可能确认它们处于同一隧道中，从而打开攻击向量。

### 回复记录加密（ECIES）

``replyKey``、``layerKey`` 和 ``layerIV`` 仍必须包含在 ElGamal 记录中，   可随机生成。

```text
// AEAD parameters
  k = chainkey from build request
  n = 0
  plaintext = 512 byte build reply record
  ad = h from build request

  ciphertext = ENCRYPT(k, n, plaintext, ad)
```
### 回复记录加密（ElGamal）

定义见 [Tunnel Creation](/docs/specs/tunnel-implementation/)。   ElGamal 跳点的加密方式无变更。

### 安全分析

回复记录使用 ChaCha20/Poly1305 加密。

定义见 [Tunnel Creation](/docs/specs/tunnel-implementation/)。   ElGamal 跳点的加密方式无变更。

ElGamal 无法为隧道构建消息提供前向保密性。

AES256/CBC 略好，仅理论上可能受到已知明文 `biclique` 攻击的削弱。

对 AES256/CBC 唯一已知的实际攻击是填充预言攻击，当攻击者已知 IV 时可能发生。

攻击者需要破解下一跳的 ElGamal 加密才能获取 AES256/CBC 密钥信息（回复密钥和 IV）。

ElGamal 比 ECIES 显著更消耗 CPU，可能导致资源耗尽。

## 理由

ECIES 结合每构建请求记录或 VariableTunnelBuildMessage 使用新临时密钥，提供前向保密性。

## 实现说明

* 较旧的路由器不检查跳点的加密类型，会发送 ElGamal 加密的记录。  
  一些较新的路由器存在缺陷，会发送各种格式错误的记录。  
  实现者应尽可能在 DH 操作前检测并拒绝这些记录，以减少 CPU 使用。

## 问题

## 迁移

ChaCha20Poly1305 提供 AEAD 加密，允许接收方在尝试解密前验证消息完整性。

## 参考文献

* [Common](/docs/specs/common-structures/)
* [Cryptography](/docs/specs/cryptography/)
* [ECIES-X25519](/docs/specs/ecies/)
* [I2NP](/docs/specs/i2np/)
* [NOISE](https://noiseprotocol.org/noise.html)
* [NTCP2](/docs/specs/ntcp2/)
* [Prop119](/proposals/119-bidirectional-tunnels/)
* [Prop143](/proposals/143-build-message-options/)
* [Prop153](/proposals/153-chacha20-layer-encryption/)
* [Prop156](/proposals/156-ecies-routers/)
* [Prop157](/proposals/157-new-tbm/)
* [SPEC](/docs/specs/tunnel-implementation/#tunnel-creation-ecies)
* [Tunnel-Creation](/docs/specs/tunnel-implementation/#tunnel-creation-ecies)
* [Multiple-Encryption](https://en.wikipedia.org/wiki/Multiple_encryption)
* [RFC-7539](https://tools.ietf.org/html/rfc7539)
* [RFC-7748](https://tools.ietf.org/html/rfc7748)
