---
title: "Tunnel 创建规范 (ECIES-X25519)"
description: "使用 ECIES-X25519 加密原语的 Tunnel Build 消息加密，以实现前向保密。"
slug: "tunnel-creation-ecies"
aliases:
  - "/zh/docs/specs/tunnel-creation-ecies-spec"
  - "/zh/docs/specs/tunnel-creation-ecies-spec/"
category: "协议"
lastUpdated: "2025-06"
accurateFor: "0.9.66"
---

## 概述

本文档规定了使用[ECIES-X25519](/docs/specs/ecies/)引入的加密原语进行Tunnel Build消息加密。这是将router从ElGamal转换为ECIES-X25519密钥的整体提案[Prop156](/proposals/156/)的一部分。

有两个版本规范。第一个使用现有的构建消息和构建记录大小，以兼容 ElGamal router。此规范在 0.9.48 版本中实现，现已弃用。第二个使用两个新的构建消息和更小的构建记录大小，只能与 ECIES router 一起使用。此规范在 0.9.51 版本中实现。

为了将网络从 ElGamal + AES256 过渡到 ECIES + ChaCha20，需要使用混合 ElGamal 和 ECIES router 的 tunnel。提供了处理混合 tunnel hop 的规范。不会对 ElGamal hop 的格式、处理或加密进行任何更改。此格式保持 tunnel 构建记录的相同大小，这是兼容性所必需的。

ElGamal tunnel 创建者将为每跳生成临时的 X25519 密钥对，并遵循此规范来创建包含 ECIES 跳的 tunnel。

本文档规定了 ECIES-X25519 tunnel 构建。有关 ECIES router 所需的所有更改概述，请参见提案 156 [Prop156](/proposals/156/)。有关长记录规范开发的其他背景信息，请参见提案 152 [Prop152](/proposals/152/)。有关短记录规范开发的其他背景信息，请参见提案 157 [Prop157](/proposals/157/)。

### 密码学原语

实现此规范所需的基本组件包括：

- AES-256-CBC 如 [密码学](/docs/specs/cryptography/) 中所述
- STREAM ChaCha20 函数：ENCRYPT(k, iv, plaintext) 和 DECRYPT(k, iv, ciphertext) - 如 [EncryptedLeaseSet](/docs/specs/encryptedleaseset/) 和 [RFC-7539](https://tools.ietf.org/html/rfc7539) 中所述
- STREAM ChaCha20/Poly1305 函数：ENCRYPT(k, n, plaintext, ad) 和 DECRYPT(k, n, ciphertext, ad) - 如 [NTCP2](/docs/specs/ntcp2/)、[ECIES-X25519](/docs/specs/ecies/) 和 [RFC-7539](https://tools.ietf.org/html/rfc7539) 中所述
- X25519 DH 函数 - 如 [NTCP2](/docs/specs/ntcp2/) 和 [ECIES-X25519](/docs/specs/ecies/) 中所述
- HKDF(salt, ikm, info, n) - 如 [NTCP2](/docs/specs/ntcp2/) 和 [ECIES-X25519](/docs/specs/ecies/) 中所述

在其他地方定义的其他 Noise 函数：

- MixHash(d) - 如在 [NTCP2](/docs/specs/ntcp2/) 和 [ECIES-X25519](/docs/specs/ecies/) 中所述
- MixKey(d) - 如在 [NTCP2](/docs/specs/ntcp2/) 和 [ECIES-X25519](/docs/specs/ecies/) 中所述

## 设计

### Noise 协议框架

本规范基于 Noise Protocol Framework [NOISE](https://noiseprotocol.org/noise.html)（修订版 34，2018-07-11）提供要求。在 Noise 术语中，Alice 是发起者，Bob 是响应者。

它基于 Noise 协议 Noise_N_25519_ChaChaPoly_SHA256。该 Noise 协议使用以下基元：

- 单向握手模式：N - Alice 不向 Bob 传输她的静态密钥 (N)
- DH 函数：X25519 - 如 [RFC-7748](https://tools.ietf.org/html/rfc7748) 中指定的密钥长度为 32 字节的 X25519 DH
- 加密函数：ChaChaPoly - 如 [RFC-7539](https://tools.ietf.org/html/rfc7539) 第 2.8 节中指定的 AEAD_CHACHA20_POLY1305。12 字节随机数，前 4 字节设为零。与 [NTCP2](/docs/specs/ntcp2/) 中的相同
- 哈希函数：SHA256 - 标准 32 字节哈希，已在 I2P 中广泛使用

### 握手模式

握手使用[Noise](https://noiseprotocol.org/noise.html)握手模式。

使用以下字母映射：

- e = 一次性临时密钥
- s = 静态密钥
- p = 消息载荷

构建请求与 Noise N 模式相同。这也与 [NTCP2](/docs/specs/ntcp2/) 中使用的 XK 模式的第一条消息（会话请求）相同。

```
<- s
  ...
  e es p ->
```
### 请求加密

构建请求记录由tunnel创建者创建，并对各个跳点进行非对称加密。请求记录的非对称加密目前使用[密码学](/docs/specs/cryptography/)中定义的ElGamal，并包含SHA-256校验和。此设计不具备前向保密性。

ECIES 设计使用单向 Noise 模式 "N"，采用 ECIES-X25519 临时-静态 DH，配合 HKDF 和 ChaCha20/Poly1305 AEAD，以实现前向保密性、完整性和身份验证。Alice 是 tunnel 构建请求者。tunnel 中的每一跳都是一个 Bob。

### 回复加密

构建回复记录由跳数创建者创建并对称加密给创建者。ElGamal回复记录的对称加密使用AES，并带有预置的SHA-256校验和。这种设计不具备前向保密性。

ECIES 回复使用 ChaCha20/Poly1305 AEAD 来保证完整性和认证。

## 长记录规范

注意：已弃用，已过时。请使用下面指定的短记录格式。

### 构建请求记录

加密的 BuildRequestRecords 在 ElGamal 和 ECIES 中都是 528 字节，以保持兼容性。

#### 请求记录未加密

这是ECIES-X25519 router的tunnel BuildRequestRecord规范。变更摘要：

- 移除未使用的 32 字节 router 哈希
- 将请求时间从小时改为分钟
- 为未来可变 tunnel 时间添加过期字段
- 为标志添加更多空间
- 为额外构建选项添加映射
- AES-256 回复密钥和 IV 不用于跃点自己的回复记录
- 未加密记录更长，因为加密开销更少

请求记录不包含任何 ChaCha 回复密钥。这些密钥是从 KDF 派生的。请参见下文。

所有字段都是大端序。

未加密大小：464 字节

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-3</td><td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel ID to receive messages as, nonzero</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">4-7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next tunnel ID, nonzero</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">8-39</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next router identity hash</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">40-71</td><td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 tunnel layer key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">72-103</td><td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 tunnel IV key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">104-135</td><td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 reply key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">136-151</td><td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 reply IV</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">152</td><td style="border:1px solid var(--color-border); padding:0.6rem;">flags</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">153-155</td><td style="border:1px solid var(--color-border); padding:0.6rem;">more flags, unused, set to 0 for compatibility</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">156-159</td><td style="border:1px solid var(--color-border); padding:0.6rem;">request time (in minutes since the epoch, rounded down)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">160-163</td><td style="border:1px solid var(--color-border); padding:0.6rem;">request expiration (in seconds since creation)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">164-167</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next message ID</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">168-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel build options (Mapping)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">other data as implied by flags or options</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-463</td><td style="border:1px solid var(--color-border); padding:0.6rem;">random padding</td></tr>
</tbody>
</table>
flags 字段与 [Tunnel-Creation](/docs/specs/tunnel-creation/) 中定义的相同，包含以下内容：

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bit</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;" colspan="2"><em>Bit order: 76543210 (bit 7 is MSB)</em></td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">if set, allow messages from anyone</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">6</td><td style="border:1px solid var(--color-border); padding:0.6rem;">if set, allow messages to anyone, and send the reply to the specified next hop in a Tunnel Build Reply Message</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">5-0</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Undefined, must set to 0 for compatibility with future options</td></tr>
</tbody>
</table>
位 7 表示该跳将是入站网关 (IBGW)。位 6 表示该跳将是出站端点 (OBEP)。如果两个位都未设置，该跳将是中间参与者。两个位不能同时设置。

请求过期时间用于未来可变的 tunnel 持续时间。目前唯一支持的值是 600（10分钟）。

tunnel 构建选项是一个映射结构，定义见[通用结构](/docs/specs/common-structures/)。目前定义的唯一选项是带宽参数，从 API 0.9.65 开始，详情见下文。如果映射结构为空，则为两个字节 0x00 0x00。映射的最大大小（包括长度字段）为 296 字节，映射长度字段的最大值为 294。

#### 请求记录已加密

除了临时公钥采用小端序外，所有字段都采用大端序。

加密大小：528 字节

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-15</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Hop's truncated identity hash</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">16-47</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Sender's ephemeral X25519 public key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">48-511</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20 encrypted BuildRequestRecord</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">512-527</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Poly1305 MAC</td></tr>
</tbody>
</table>
### 构建回复记录

加密的 BuildReplyRecord 对于 ElGamal 和 ECIES 都是 528 字节，以保持兼容性。

#### 回复记录未加密

这是 ECIES-X25519 router 的 tunnel BuildReplyRecord 规范。变更摘要：

- 为构建回复选项添加映射
- 未加密记录更长，因为加密开销更少

ECIES 回复使用 ChaCha20/Poly1305 加密。

所有字段均为大端序。

未加密大小：512 字节

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel Build Reply Options (Mapping)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">other data as implied by options</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-510</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Random padding</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">511</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Reply byte</td></tr>
</tbody>
</table>
tunnel build reply 选项是一个 Mapping 结构，如 [Common](/docs/specs/common-structures/) 中定义。目前唯一定义的选项是带宽参数，自 API 0.9.65 起，详见下文。如果 Mapping 结构为空，则为两字节 0x00 0x00。Mapping（包括长度字段）的最大大小为 511 字节，Mapping 长度字段的最大值为 509。

回复字节是以下值之一，如 [Tunnel-Creation](/docs/specs/tunnel-creation/) 中定义的，以避免指纹识别：

- 0x00 (接受)
- 30 (TUNNEL_REJECT_BANDWIDTH)

#### 回复记录已加密

加密大小：528 字节

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-511</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20 encrypted BuildReplyRecord</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">512-527</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Poly1305 MAC</td></tr>
</tbody>
</table>
完全过渡到 ECIES 记录后，范围填充规则与请求记录相同。

### 记录的对称加密

混合隧道是被允许的，也是从 ElGamal 过渡到 ECIES 所必需的。在过渡期间，越来越多的 router 将使用 ECIES 密钥。

对称加密预处理将以相同方式运行：

- "encryption"：
  - 密码在解密模式下运行
  - 请求记录在预处理中被预先解密（隐藏加密的请求记录）
- "decryption"：
  - 密码在加密模式下运行
  - 请求记录被参与跳数加密（显示下一个明文请求记录）
- ChaCha20 没有"模式"，因此它只是运行三次：
  - 一次在预处理中
  - 一次由跳数处理
  - 一次在最终回复处理中

当使用混合 tunnel 时，tunnel 创建者需要基于当前和前一跳的加密类型来确定 BuildRequestRecord 的对称加密。

每个跳跃节点将使用自己的加密类型来加密 BuildReplyRecords，以及 VariableTunnelBuildMessage (VTBM) 中的其他记录。

在回复路径上，端点（发送者）需要使用每一跳的回复密钥来撤销[多重加密](https://en.wikipedia.org/wiki/Multiple_encryption)。

作为一个澄清的例子，让我们看看一个被 ElGamal 包围的带有 ECIES 的出站 tunnel：

- 发送方 (OBGW) -> ElGamal (H1) -> ECIES (H2) -> ElGamal (H3)

所有BuildRequestRecord都处于加密状态（使用ElGamal或ECIES）。

当使用AES256/CBC密码时，仍然用于每个记录，不会跨多个记录进行链接。

同样，ChaCha20 将用于加密每个记录，而不是在整个 VTBM 中进行流式传输。

请求记录由发送方（OBGW）进行预处理：

- H3的记录使用以下方式"加密"：
  - H2的回复密钥（ChaCha20）
  - H1的回复密钥（AES256/CBC）
- H2的记录使用以下方式"加密"：
  - H1的回复密钥（AES256/CBC）
- H1的记录在发送时不使用对称加密

只有 H2 检查回复加密标志，并看到其后跟着 AES256/CBC。

经过每个跳点处理后，记录处于"解密"状态：

- H3 的记录使用以下方式"解密"：
  - H3 的回复密钥 (AES256/CBC)
- H2 的记录使用以下方式"解密"：
  - H3 的回复密钥 (AES256/CBC)
  - H2 的回复密钥 (ChaCha20-Poly1305)
- H1 的记录使用以下方式"解密"：
  - H3 的回复密钥 (AES256/CBC)
  - H2 的回复密钥 (ChaCha20)
  - H1 的回复密钥 (AES256/CBC)

tunnel 创建者，也称为入站端点（IBEP），对回复进行后处理：

- H3的记录使用以下方式"加密"：
  - H3的回复密钥 (AES256/CBC)
- H2的记录使用以下方式"加密"：
  - H3的回复密钥 (AES256/CBC)
  - H2的回复密钥 (ChaCha20-Poly1305)
- H1的记录使用以下方式"加密"：
  - H3的回复密钥 (AES256/CBC)
  - H2的回复密钥 (ChaCha20)
  - H1的回复密钥 (AES256/CBC)

### 请求记录键

这些密钥明确包含在 ElGamal BuildRequestRecords 中。对于 ECIES BuildRequestRecords，包含了 tunnel 密钥和 AES 回复密钥，但 ChaCha 回复密钥是从 DH 交换中派生的。有关 router 静态 ECIES 密钥的详细信息，请参见 [Prop156](/proposals/156/)。

以下是如何推导先前在请求记录中传输的密钥的描述。

#### 初始 ck 和 h 的 KDF

这是标准的 [NOISE](https://noiseprotocol.org/noise.html)，用于模式"N"的标准协议名称。

```
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
#### 请求记录的密钥派生函数

ElGamal tunnel 创建者为 tunnel 中的每个 ECIES 跳点生成临时 X25519 密钥对，并使用上述方案加密其 BuildRequestRecord。ElGamal tunnel 创建者将使用本规范之前的方案来加密到 ElGamal 跳点。

ECIES tunnel 创建者需要使用 [Tunnel-Creation](/docs/specs/tunnel-creation/) 中定义的方案对每个 ElGamal 跳跃点的公钥进行加密。ECIES tunnel 创建者将使用上述方案对 ECIES 跳跃点进行加密。

这意味着tunnel跳点只能看到来自相同加密类型的加密记录。

对于 ElGamal 和 ECIES tunnel 创建者，它们将为每一跳生成唯一的临时 X25519 密钥对，用于加密到 ECIES 跳点。

**重要提示**：临时密钥在每个 ECIES hop 和每个构建记录中必须是唯一的。如果未能使用唯一密钥，将为串通的 hop 提供攻击向量，使它们能够确认自己处于同一个 tunnel 中。

```
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
`replyKey`、`layerKey` 和 `layerIV` 仍然必须包含在 ElGamal 记录内，并且可以随机生成。

### 回复记录加密

回复记录使用 ChaCha20/Poly1305 加密。

```
// AEAD parameters
k = chainkey from build request
n = 0
plaintext = 512 byte build reply record
ad = h from build request

ciphertext = ENCRYPT(k, n, plaintext, ad)
```
## 短记录规范

本规范使用两个新的I2NP tunnel构建消息，Short Tunnel Build Message（类型25）和Outbound Tunnel Build Reply Message（类型26）。

tunnel 创建者和所创建 tunnel 中的所有跳点都必须支持 ECIES-X25519，并且至少为 0.9.51 版本。回复 tunnel（用于出站构建）或出站 tunnel（用于入站构建）中的跳点没有任何要求。

加密的请求和回复记录将为218字节，相比之下所有其他构建消息为528字节。

明文请求记录将为154字节，相比之下ElGamal记录为222字节，而上述定义的ECIES记录为464字节。

明文响应记录将为202字节，相比之下ElGamal记录为496字节，而上述定义的ECIES记录为512字节。

回复加密将对该跳的自身记录使用 ChaCha20/Poly1305，对构建消息中的其他记录使用 ChaCha20（不是 ChaCha20/Poly1305）。

通过使用 HKDF 创建层密钥和回复密钥，请求记录将变得更小，因此它们不会明确包含在请求中。

### 消息流

```
STBM: Short tunnel build message (type 25)
OTBRM: Outbound tunnel build reply message (type 26)

Outbound Build A-B-C
Reply through existing inbound D-E-F


                New Tunnel
         STBM      STBM      STBM
Creator ------> A ------> B ------> C ---\
                                   OBEP   \
                                          | Garlic wrapped (optional)
                                          | OTBRM
                                          | (TUNNEL delivery)
                                          | from OBEP to
                                          | creator
              Existing Tunnel             /
Creator <-------F---------E-------- D <--/
                                   IBGW



Inbound Build D-E-F
Sent through existing outbound A-B-C


              Existing Tunnel
Creator ------> A ------> B ------> C ---\
                                  OBEP    \
                                          | Garlic wrapped (optional)
                                          | STBM
                                          | (ROUTER delivery)
                                          | from creator
                New Tunnel                | to IBGW
          STBM      STBM      STBM        /
Creator <------ F <------ E <------ D <--/
                                   IBGW
```
#### 注释

消息的garlic encryption封装能够对OBEP（入站构建）或IBGW（出站构建）隐藏消息内容。这是推荐的但不是必需的。如果OBEP和IBGW是同一个router，则没有必要这样做。

### 简短构建请求记录

简短加密的 BuildRequestRecords 长度为 218 字节。

#### 短请求记录未加密

长记录变更摘要：

- 将未加密长度从 464 字节更改为 154 字节
- 将加密长度从 528 字节更改为 218 字节
- 移除层密钥和回复密钥及 IV，它们将从 KDF 生成

请求记录不包含任何 ChaCha 应答密钥。这些密钥是从 KDF 派生的。请参见下文。

所有字段均采用大端序。

未加密大小：154 字节。

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-3</td><td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel ID to receive messages as, nonzero</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">4-7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next tunnel ID, nonzero</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">8-39</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next router identity hash</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">40</td><td style="border:1px solid var(--color-border); padding:0.6rem;">flags</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">41-42</td><td style="border:1px solid var(--color-border); padding:0.6rem;">more flags, unused, set to 0 for compatibility</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">43</td><td style="border:1px solid var(--color-border); padding:0.6rem;">layer encryption type</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">44-47</td><td style="border:1px solid var(--color-border); padding:0.6rem;">request time (in minutes since the epoch, rounded down)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">48-51</td><td style="border:1px solid var(--color-border); padding:0.6rem;">request expiration (in seconds since creation)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">52-55</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next message ID</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">56-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel build options (Mapping)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">other data as implied by flags or options</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-153</td><td style="border:1px solid var(--color-border); padding:0.6rem;">random padding (see below)</td></tr>
</tbody>
</table>
flags 字段与 [Tunnel-Creation](/docs/specs/tunnel-creation/) 中定义的相同，包含以下内容：

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bit</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;" colspan="2"><em>Bit order: 76543210 (bit 7 is MSB)</em></td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">if set, allow messages from anyone</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">6</td><td style="border:1px solid var(--color-border); padding:0.6rem;">if set, allow messages to anyone, and send the reply to the specified next hop in a Tunnel Build Reply Message</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">5-0</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Undefined, must set to 0 for compatibility with future options</td></tr>
</tbody>
</table>
位7表示该跳点将成为入站网关（IBGW）。位6表示该跳点将成为出站端点（OBEP）。如果两个位都未设置，该跳点将成为中间参与者。两个位不能同时设置。

层加密类型：0 表示 AES（如当前 tunnel 中使用的）；1 表示未来使用（ChaCha？）

请求过期时间用于将来可变的 tunnel 持续时间。目前，唯一支持的值是 600（10 分钟）。

创建者临时公钥是一个ECIES密钥，采用大端字节序。它用于IBGW层和回复密钥及IV的KDF。这只包含在Inbound Tunnel Build消息的明文记录中。这是必需的，因为在构建记录的这一层没有DH交换。

tunnel 构建选项是一个映射结构，如[通用结构](/docs/specs/common-structures/)中定义的那样。目前定义的唯一选项是带宽参数，从 API 0.9.65 开始，详细信息见下文。如果映射结构为空，这是两个字节 0x00 0x00。映射的最大大小（包括长度字段）是 98 字节，映射长度字段的最大值是 96。

#### 短请求记录加密

除了临时公钥是小端字节序外，所有字段都是大端字节序。

加密大小：218 字节

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-15</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Hop's truncated identity hash</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">16-47</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Sender's ephemeral X25519 public key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">48-201</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20 encrypted ShortBuildRequestRecord</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">202-217</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Poly1305 MAC</td></tr>
</tbody>
</table>
### 短构建回复记录

短加密的 BuildReplyRecords 为 218 字节。

#### 短回复记录未加密

长记录变更摘要：

- 将未加密长度从512字节更改为202字节
- 将加密长度从528字节更改为218字节

ECIES 回复使用 ChaCha20/Poly1305 加密。

所有字段都是大端序。

未加密大小：202 字节。

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel Build Reply Options (Mapping)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">other data as implied by options</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-200</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Random padding (see below)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">201</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Reply byte</td></tr>
</tbody>
</table>
tunnel 构建回复选项是一个在[通用结构](/docs/specs/common-structures/)中定义的映射结构。目前定义的唯一选项是带宽参数，从 API 0.9.65 开始，详情见下文。如果映射结构为空，则为两个字节 0x00 0x00。映射的最大大小（包括长度字段）为 201 字节，映射长度字段的最大值为 199。

回复字节是在 [Tunnel-Creation](/docs/specs/tunnel-creation/) 中定义的以下值之一，以避免指纹识别：

- 0x00 (接受)
- 30 (TUNNEL_REJECT_BANDWIDTH)

未来可能会定义额外的回复值来表示对不支持选项的拒绝。

#### 短回复记录加密

加密大小：218 字节

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-201</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20 encrypted ShortBuildReplyRecord</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">202-217</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Poly1305 MAC</td></tr>
</tbody>
</table>
### 密钥派生函数

我们使用隧道构建记录加密/解密后 Noise 状态中的链式密钥 (ck) 来派生以下密钥：回复密钥、AES 层密钥、AES IV 密钥以及用于 OBEP 的 garlic 回复密钥/标签。

Reply keys：注意 KDF 对于 OBEP 和非 OBEP 跃点略有不同。与长记录不同，我们不能使用 ck 的左半部分作为 reply key，因为它不是最后一个并且稍后会被使用。reply key 用于使用 AEAD/ChaCha20/Poly1305 加密该记录的回复，并使用 ChaCha20 回复其他记录。两者使用相同的密钥。nonce 是消息中记录的位置，从 0 开始。详细信息见下文。

```
keydata = HKDF(ck, ZEROLEN, "SMTunnelReplyKey", 64)
replyKey = keydata[32:63]
ck = keydata[0:31]

AES Layer key:
keydata = HKDF(ck, ZEROLEN, "SMTunnelLayerKey", 64)
layerKey = keydata[32:63]

IV key for non-OBEP record:
ivKey = keydata[0:31]
because it's last

IV key for OBEP record:
ck = keydata[0:31]
keydata = HKDF(ck, ZEROLEN, "TunnelLayerIVKey", 64)
ivKey = keydata[32:63]
ck = keydata[0:31]

OBEP garlic reply key/tag:
keydata = HKDF(ck, ZEROLEN, "RGarlicKeyAndTag", 64)
garlicReplyKey = keydata[32:63]
garlicReplyTag = keydata[0:7]
```
注意：OBEP 处 IV 密钥的 KDF 与其他跳点不同，即使回复没有使用 garlic encryption 也是如此。

#### 记录加密

hop 自身的回复记录使用 ChaCha20/Poly1305 加密。这与上面的长记录规范相同，除了 'n' 是记录编号 0-7，而不是始终为 0。参见 [RFC-7539](https://tools.ietf.org/html/rfc7539)。

```
// AEAD parameters
k = replyKey from KDF above
n = record number 0-7
plaintext = 202 byte build reply record
ad = h from build request

ciphertext = ENCRYPT(k, n, plaintext, ad)
```
其他记录在每个跳点都会使用 ChaCha20（不是 ChaCha20/Poly1305）进行迭代和对称加密。这与上述长记录规范不同，长记录使用 AES 且不使用记录编号。

记录编号被放置在IV的第4字节，因为ChaCha20使用12字节的IV，其中第4-11字节是小端序的nonce。参见[RFC-7539](https://tools.ietf.org/html/rfc7539)。

```
// Parameters
k = replyKey from KDF above
n = record number 0-7
iv = 12 bytes, all zeros except iv[4] = n
plaintext = 218 byte encrypted record

ciphertext = ENCRYPT(k, iv, plaintext)
```
#### Garlic Encryption

对消息进行 garlic 包装可以向 OBEP（对于入站构建）或 IBGW（对于出站构建）隐藏消息内容。这是推荐的做法但不是必需的。如果 OBEP 和 IBGW 是同一个 router，则没有必要进行包装。

入站短隧道构建消息的 garlic encryption，由创建者执行，加密到 ECIES IBGW，使用 Noise 'N' 加密，如 [ECIES-ROUTERS](/docs/specs/ecies-routers/) 中定义。

由 OBEP 对出站 tunnel 构建回复消息进行 garlic encryption，加密给创建者，使用现有会话消息，采用上述 KDF 中的 32 字节 garlic 回复密钥和 8 字节 garlic 回复标签。格式按照 [I2NP](/docs/specs/i2np/)、[ECIES-ROUTERS](/docs/specs/ecies-routers/) 和 [ECIES-X25519](/docs/specs/ecies/) 中对数据库查询回复的规定执行。

#### 层加密

本规范在构建请求记录中包含了一个层加密类型字段。目前唯一支持的层加密类型是0，即AES。除了层密钥和IV密钥是从上述KDF派生而不是包含在构建请求记录中之外，这与之前的规范没有变化。

添加新的层加密类型，例如 ChaCha20，是一个需要额外研究的话题，目前不是本规范的一部分。

## 实现说明

- 旧版 router 不会检查跳跃的加密类型，会发送 ElGamal 加密的记录。一些最新的 router 存在 bug，会发送各种格式错误的记录。实现者应该在可能的情况下在 DH 操作之前检测并拒绝这些记录，以减少 CPU 使用量。

### 构建记录

构建记录顺序必须随机化，这样中间跳跃节点就不会知道它们在 tunnel 中的位置。

推荐的最少构建记录数量为4个。如果构建记录数量多于跳数，必须添加"虚假"记录，包含随机或实现特定的数据。对于入站tunnel构建，必须始终为发起router添加一个"虚假"记录，包含正确的16字节哈希前缀和真实的X25519临时密钥，否则最近的跳点将知道下一跳是发起者。

"伪造"记录的其余部分可能是随机数据，或者可能以任何格式加密，供发起者向自身发送关于构建的数据，也许是为了减少待处理构建的存储需求。

入站tunnel的发起者必须使用某种方法来验证其"虚假"记录未被前一跳修改，因为这也可能被用于去匿名化。发起者可以存储并验证记录的校验和，或在记录中包含校验和，或使用AEAD加密/解密功能，具体取决于实现。如果16字节哈希前缀或其他构建记录内容被修改，router必须丢弃该tunnel。

出站 tunnel 的虚假记录，以及入站 tunnel 的额外虚假记录，没有这些要求，可以是完全随机的数据，因为它们永远不会对任何跳点可见。发起者可能仍然希望验证它们没有被修改。

## Tunnel 带宽参数

### 概述

随着我们在过去几年中通过新协议、加密类型和拥塞控制改进提高了网络性能，视频流等更快速的应用正在变得可行。这些应用需要在其客户端tunnel的每一跳中都具备高带宽。

然而，参与的 router 在收到隧道构建消息时，并不知道该 tunnel 将使用多少带宽。它们只能根据所有参与 tunnel 当前使用的总带宽以及参与 tunnel 的总带宽限制来决定接受或拒绝 tunnel。

请求的 router 也无法获得每个跳点可用带宽的信息。

此外，router目前无法限制tunnel上的入站流量。这在服务过载或遭受DDoS攻击时会非常有用。

tunnel 建立请求和回复消息中的 tunnel 带宽参数增加了对这些功能的支持。更多背景信息请参见 [Prop168](/proposals/168/)。这些参数从 API 0.9.65 开始定义，但不同实现的支持情况可能有所差异。它们同时支持长短两种 ECIES 构建记录。

### 构建请求选项

以下三个选项可以在记录的隧道构建选项映射字段中设置：请求的 router 可以包含任意、全部或不包含任何选项。

- m := 此tunnel所需的最小带宽（KBps正整数，以字符串形式表示）
- r := 此tunnel请求的带宽（KBps正整数，以字符串形式表示）
- l := 此tunnel的带宽限制；仅发送给IBGW（KBps正整数，以字符串形式表示）

约束条件：m <= r <= l

如果指定了"m"参数，而参与的 router 无法提供至少这么多的带宽，则应该拒绝该 tunnel。

请求选项会发送给相应加密构建请求记录中的每个参与者，对其他参与者不可见。

### 构建回复选项

当响应为 ACCEPTED 时，可以在记录的 tunnel 构建回复选项映射字段中设置以下选项：

- b := 此 tunnel 可用带宽（以字符串形式表示的 KBps 正整数）

约束条件：b >= m

如果在构建请求中指定了"m"或"r"，参与的 router 应该包含此项。如果指定了"m"值，该值应至少等于"m"值，但如果指定了"r"值，可以小于或大于"r"值。

参与的router应该尝试为tunnel预留并提供至少这么多带宽，但这并不能保证。Router无法预测10分钟后的情况，而且参与流量的优先级低于router自己的流量和tunnel。

如有必要，router 也可能会过度分配可用带宽，这可能是可取的，因为 tunnel 中的其他跳点可能会拒绝它。

基于这些原因，参与 router 的回复应被视为尽力而为的承诺，而非保证。

回复选项会在相应的加密构建回复记录中发送给请求的 router，其他参与者无法看到这些选项。

### 实现说明

带宽参数是在参与的 router 在 tunnel 层看到的，即每秒固定大小的 1 KB tunnel 消息数量。传输层（NTCP2 或 SSU2）开销不包括在内。

此带宽可能远高于或远低于客户端看到的带宽。Tunnel 消息包含大量开销，包括来自更高层的开销，如 ratchet 和流传输。间歇性的小消息（如流传输确认）将扩展为每个 1 KB。不过，I2CP 层的 gzip 压缩可能会大幅减少带宽使用。

在请求 router 的最简单实现是使用池中当前 tunnel 的平均、最小和/或最大带宽来计算请求中要填入的值。更复杂的算法是可能的，具体由实现者决定。

目前没有定义 I2CP 或 SAM 选项供客户端告知 router 所需的带宽，此处也不提议新的选项。如有必要，可能会在以后定义相关选项。

实现可以使用可用带宽或任何其他数据、算法、本地策略或本地配置来计算在构建响应中返回的带宽值。

## 参考资料

- [通用结构](/docs/specs/common-structures/)
- [密码学](/docs/specs/cryptography/)
- [ECIES-ROUTERS](/docs/specs/ecies-routers/)
- [ECIES-X25519](/docs/specs/ecies/)
- [EncryptedLeaseSet](/docs/specs/encryptedleaseset/)
- [I2NP](/docs/specs/i2np/)
- [多重加密](https://en.wikipedia.org/wiki/Multiple_encryption)
- [NOISE](https://noiseprotocol.org/noise.html)
- [NTCP2](/docs/specs/ntcp2/)
- [提案119](/proposals/119/)
- [提案143](/proposals/143/)
- [提案152](/proposals/152/)
- [提案153](/proposals/153/)
- [提案156](/proposals/156/)
- [提案157](/proposals/157/)
- [提案168](/proposals/168/)
- [RFC-7539](https://tools.ietf.org/html/rfc7539)
- [RFC-7748](https://tools.ietf.org/html/rfc7748)
- [Tunnel创建](/docs/specs/tunnel-creation/)
