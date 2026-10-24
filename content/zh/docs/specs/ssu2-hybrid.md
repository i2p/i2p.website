---
title: "PQ 混合 SSU2"
description: "使用 ML-KEM 的 SSU2 传输协议后量子混合变体"
slug: "ssu2-hybrid"
lastupdated: "2026-10"
category: "传输层"
accurateFor: "0.9.71"
---

### 状态

Beta 版本预计 2026 年第二季度，正式发布预计 2026 年第三季度

## 概述

这是 SSU2 传输协议的混合后量子变体，如提案 169 中所设计。有关更多背景信息，请参阅该提案。

PQ Hybrid SSU2 仅在与标准 SSU2 相同的地址和端口上定义。不允许在不同端口上运行，或在不支持标准 SSU2 的情况下运行，在标准 SSU2 被弃用之前的数年内，此限制将持续有效。

本规范仅记录在标准 SSU2 基础上支持 PQ Hybrid（后量子混合）所需的变更。基线实现细节请参阅 SSU2 规范。

## 设计

我们支持 NIST FIPS 203 和 204 标准 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)，这些标准基于 CRYSTALS-Kyber 和 CRYSTALS-Dilithium（3.1、3 及更早版本），但与其**不兼容**。

### 密钥交换

PQ KEM 仅提供临时密钥，不直接支持静态密钥握手，例如 Noise XK 和 IK。所使用的加密类型与 PQ Hybrid Ratchet 中的相同，并在公共结构文档 [/docs/specs/common-structures/](/docs/specs/common-structures/) 中定义。与 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) 一致，混合类型仅与 X25519 组合定义。

加密类型包括：

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">SSU2 Version</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
</tr>
</table>
### 合法组合

新的加密类型在 RouterAddresses 中标识。密钥证书中的加密类型将继续为类型 4。

## 规范

### 握手模式

握手过程使用 [Noise Protocol](https://noiseprotocol.org/noise.html) 握手模式。

使用以下字母映射：

- e = 一次性临时密钥
- s = 静态密钥
- p = 消息载荷
- e1 = 一次性临时 PQ 密钥，由 Alice 发送给 Bob
- ekem1 = KEM 密文，由 Bob 发送给 Alice

以下对 XK 和 IK 进行的混合前向保密（hfs）修改，依照 [Noise HFS 规范](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) 第 5 节的规定：

```
XK:                       XKhfs:
  <- s                      <- s
  ...                       ...
  -> e, es, p               -> e, es, e1, p
  <- e, ee, p               <- e, ee, ekem1, p
  -> s, se                  -> s, se
  <- p                      <- p
  p ->                      p ->


  e1 and ekem1 are encrypted. See pattern definitions below.
  NOTE: e1 and ekem1 are different sizes (unlike X25519)
```
e1 模式的定义如下，详见 [Noise HFS 规范](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) 第 4 节：

```
For Alice:
  (encap_key, decap_key) = PQ_KEYGEN()

  // EncryptAndHash(encap_key)
  ciphertext = ENCRYPT(k, n, encap_key, ad)
  n++
  MixHash(ciphertext)

  For Bob:

  // DecryptAndHash(ciphertext)
  encap_key = DECRYPT(k, n, ciphertext, ad)
  n++
  MixHash(ciphertext)
```
ekem1 模式的定义如下，具体规范参见 [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) 第 4 节：

```
For Bob:

  (kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

  // EncryptAndHash(kem_ciphertext)
  ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)
  MixHash(ciphertext)

  // MixKey
  MixKey(kem_shared_key)


  For Alice:

  // DecryptAndHash(ciphertext)
  kem_ciphertext = DECRYPT(k, n, ciphertext, ad)
  MixHash(ciphertext)

  // MixKey
  kem_shared_key = DECAPS(kem_ciphertext, decap_key)
  MixKey(kem_shared_key)
```
### Noise 握手密钥派生函数（KDF）

#### 概述

混合握手在 [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) 中定义。从 Alice 发送给 Bob 的第一条消息，在消息载荷之前包含 e1（封装密钥）。该密钥被视为附加的静态密钥；对其调用 EncryptAndHash()（作为 Alice 方）或 DecryptAndHash()（作为 Bob 方）。然后按常规方式处理消息载荷。

从 Bob 发送给 Alice 的第二条消息，在消息载荷之前包含密文 ekem1。该密文被视为额外的静态密钥：由 Bob 调用 EncryptAndHash()，或由 Alice 调用 DecryptAndHash()。然后计算 kem_shared_key，并调用 MixKey(kem_shared_key)。之后按常规方式处理消息载荷。

#### 已定义的 ML-KEM 操作

我们定义以下函数，对应于 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) 中所定义的密码学构建块。

(encap_key, decap_key) = PQ_KEYGEN()

    Alice creates the encapsulation and decapsulation keys
    The encapsulation key is sent in message 1.
    encap_key and decap_key sizes vary based on ML-KEM variant.

(ciphertext, kem_shared_key) = ENCAPS(encap_key)

    Bob calculates the ciphertext and shared key,
    using the ciphertext received in message 1.
    The ciphertext is sent in message 2.
    ciphertext size varies based on ML-KEM variant.
    The kem_shared_key is always 32 bytes.

kem_shared_key = DECAPS(ciphertext, decap_key)

    Alice calculates the shared key,
    using the ciphertext received in message 2.
    The kem_shared_key is always 32 bytes.

请注意，encap_key 和密文均在 Noise 握手消息 1 和 2 的 ChaCha/Poly 块中加密。它们将作为握手过程的一部分被解密。

kem_shared_key 通过 MixHash() 混入链接密钥（chaining key）。详情见下文。

#### Alice 消息 1 的密钥派生函数（KDF）

在 'es' 消息模式之后、载荷之前，添加：

```
This is the "e1" message pattern:
  (encap_key, decap_key) = PQ_KEYGEN()

  // EncryptAndHash(encap_key)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, encap_key, ad)
  n++

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)


  End of "e1" message pattern.

  NOTE: For the next section (payload for XK or static key for IK),
  the keydata and chain key remain the same,
  and n now equals 1 (instead of 0 for non-hybrid).
```
#### 消息1的Bob密钥派生函数（KDF）

在 'es' 消息模式之后、载荷之前，添加：

```
This is the "e1" message pattern:

  // DecryptAndHash(encap_key_section)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  encap_key = DECRYPT(k, n, encap_key_section, ad)
  n++

  // MixHash(encap_key_section)
  h = SHA256(h || encap_key_section)

  End of "e1" message pattern.

  NOTE: For the next section (payload for XK or static key for IK),
  the keydata and chain key remain the same,
  and n now equals 1 (instead of 0 for non-hybrid).
```
#### 消息 2 的 Bob KDF

对于 XK：在 'ee' 消息模式之后、载荷之前，添加：

```
This is the "ekem1" message pattern:

  (kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

  // EncryptAndHash(kem_ciphertext)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)

  // MixKey(kem_shared_key)
  keydata = HKDF(chainKey, kem_shared_key, "", 64)
  chainKey = keydata[0:31]

  End of "ekem1" message pattern.

  // AEAD parameters for payload section
  ... as in standard SSU2 ...
  k = keydata[32:63]
  ...

```
#### Alice 消息 2 的密钥派生函数（KDF）

在 'ee' 消息模式之后，添加：

```
This is the "ekem1" message pattern:

  // DecryptAndHash(kem_ciphertext_section)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  kem_ciphertext = DECRYPT(k, n, kem_ciphertext_section, ad)

  // MixHash(kem_ciphertext_section)
  h = SHA256(h || kem_ciphertext_section)

  // MixKey(kem_shared_key)
  kem_shared_key = DECAPS(kem_ciphertext, decap_key)
  keydata = HKDF(chainKey, kem_shared_key, "", 64)
  chainKey = keydata[0:31]

  End of "ekem1" message pattern.

  // AEAD parameters for payload section
  ... as in standard SSU2 ...
  k = keydata[32:63]
  ...

```
#### 消息3的密钥派生函数（KDF）

unchanged

#### split() 的密钥派生函数（KDF）

unchanged

### 握手详情

#### Noise 标识符

- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"

请注意，MLKEM-1024 **不**支持用于 SSU2，因为其密钥过大，无法容纳在标准的 1500 字节数据报中。

#### 长头部

长头部为 32 字节。它在会话创建之前使用，用于 Token Request、SessionRequest、SessionCreated 和 Retry 消息。它也用于会话外的 Peer Test 和 Hole Punch 消息。

在以下消息中，将长头部中的 ver（版本）字段设置为 3 或 4，以指示 MLKEM-512 或 MLKEM-768。

- (0) 会话请求
- (1) 会话已创建
- (9) 重试
- (10) 令牌请求
- (11) 打洞

在以下消息中，像往常一样将长头部中的 ver（版本）字段设置为 2，即使支持 MLKEM-512 或 MLKEM-768 也是如此。如果对端支持，实现也可以将该值设置为 3 或 4，但这并非必须。实现应接受 2-4 之间的任意值。

- (7) 对等测试（会话外消息 5-7）

讨论：并非所有消息类型都严格要求将 version 字段设置为 3 或 4，但这样做有助于在不支持后量子连接时更早地检测到失败。Token Request 和 Retry（类型 9 和 10）应使用版本 3/4 以保持一致性。Hole Punch 消息（类型 11）可能不需要此处理，但为了统一性，我们将遵循相同的模式。Peer Test 消息（类型 7）处于会话外，不表明发起会话的意图。

- 中继请求
- 中继响应
- 中继介绍
- 节点测试

头部加密之前：

在头部加密之前：

```

  +----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+

  Destination Connection ID :: 8 bytes, unsigned big endian integer

  Packet Number :: 4 bytes, unsigned big endian integer

  type :: The message type = 0, 1, 7, 9, 10, or 11

  ver :: The protocol version = 2, 3, or 4 for non-PQ, MLKEM512, MLKEM768

  id :: 1 byte, the network ID (currently 2, except for test networks)

  flag :: 1 byte, unused, set to 0 for future compatibility

  Source Connection ID :: 8 bytes, unsigned big endian integer

  Token :: 8 bytes, unsigned big endian integer

```
#### 短报头

unchanged

#### SessionRequest（类型 0）

变更说明：当前的 SSU2 在 ChaCha 段中仅包含块数据。引入 ML-KEM 后，ChaCha 段中还将包含加密后的后量子（PQ）公钥。

用于防欺骗的 KDF 变更：为解决提案 165 [Prop165]_ 中提出的问题，但采用不同的解决方案，我们对 Session Request 的 KDF 进行了修改。此变更仅适用于 PQ 会话，非 PQ 会话的 KDF 保持不变。

```

// End of KDF for initial chain key (unchanged)
  // Bob static key
  // MixHash(bpk)
  h = SHA256(h || bpk);

  // Start of KDF for session request
  // NEW for PQ only
  // bhash = Bob router hash (32 bytes)
  // MixHash(bhash)
  h = SHA256(h || bhash);

  // Rest of KDF for session request, unchanged, as in SSU2 spec
  // MixHash(header)
  h = SHA256(h || header)

  ...

```
原始内容：

```
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 0-15, ChaCha20     |
  +  encrypted with Bob intro key         +
  |    See Header Encryption KDF          |
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 16-31, ChaCha20    |
  +  encrypted with Bob intro key n=0     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +       X, ChaCha20 encrypted           +
  |       with Bob intro key n=0          |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (MLKEM)     |
  +          (length varies)              +
  |  k defined in KDF for Session Request |
  +  n = 0                                +
  |  see KDF for associated data          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (payload)   |
  +          (length varies)              +
  |  k defined in KDF for Session Request |
  +  n = 1                                +
  |  see KDF for associated data          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
未加密数据（未显示 Poly1305 认证标签）：

```
  +----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                   X                   |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM encap_key            |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     Noise payload (block data)        |
  +          (length varies)              +
  |     see below for allowed blocks      |
  +----+----+----+----+----+----+----+----+
```
数据包大小（不包含 IP 开销）：

| 类型 | 类型代码 | X 长度 | 消息 1 长度 | 消息 1 加密长度 | 消息 1 解密长度 | PQ 密钥长度 | 载荷长度 |
|------|-----------|-------|-----------|---------------|---------------|------------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 896+pl | 832+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1280+pl | 1216+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | n/a | 过大 | | | | |
注意：类型代码仅供内部使用。Router 将保持类型 4，相关支持信息将在 router 地址中标注。

MLKEM768_X25519 的最小 MTU：IPv4 为 1318，IPv6 为 1338。详见下文。

变更：当前的 SSU2 仅在单个 ChaCha 段中包含有效载荷。使用 ML-KEM 后，将在有效载荷之前新增一个 ChaCha 段，用于包含加密的后量子密文。

#### SessionCreated（类型 1）

变更：当前的 SSU2 仅在单个 ChaCha 段中包含有效载荷。使用 ML-KEM 后，将在有效载荷之前新增一个 ChaCha 段，其中包含加密的后量子（PQ）密文。

原始内容：

```
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 0-15, ChaCha20     |
  +  encrypted with Bob intro key and     +
  | derived key, see Header Encryption KDF|
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 16-31, ChaCha20    |
  +  encrypted with derived key n=0       +
  |  See Header Encryption KDF            |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +       Y, ChaCha20 encrypted           +
  |       with derived key n=0            |
  +              (32 bytes)               +
  |       See Header Encryption KDF       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 data (MLKEM)               |
  +   Encrypted and authenticated data    +
  |  length varies                        |
  +  k defined in KDF for Session Created +
  |  (before mixKey)                      |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 data (payload)             |
  +   Encrypted and authenticated data    +
  |  length varies                        |
  +  k defined in KDF for Session Created +
  |  (after mixKey)                       |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
未加密数据（未显示 Poly1305 认证标签）：

```
  +----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                  Y                    |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM Ciphertext           |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     Noise payload (block data)        |
  +          (length varies)              +
  |      see below for allowed blocks     |
  +----+----+----+----+----+----+----+----+
```
数据包大小（不包含 IP 开销）：

| Type | Type Code | Y len | Msg 2 len | Msg 2 Enc len | Msg 2 Dec len | PQ CT len | pl len |
|------|-----------|-------|-----------|---------------|---------------|-----------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 864+pl | 800+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1184+pl | 1120+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | 不适用 | 过大 | | | | |
注意：类型代码仅供内部使用。Router 将保持类型 4，相关支持信息将在 router 地址中标注。

MLKEM768_X25519 的最小 MTU：IPv4 为 1318，IPv6 为 1338。详见下文。

最大尺寸：Alice 尚未获取 Bob 的 RouterInfo，因此不知道他公布的 MTU。对于此消息，按以下方式使用临时 MTU。对于 MLKEM512_X25519，将 1280 或收到的 SessionRequest 大小中的较大值作为 MTU；对于 MLKEM768_X25519，将（IPv4 为 1318 或 IPv6 为 1338）或收到的 SessionRequest 大小中的较大值作为 MTU。由于 MLKEM 密文比 MLKEM 公钥更短，SessionCreated 的开销小于 SessionRequest 的开销。这使得即使 SessionRequest 中几乎没有填充，SessionCreated 仍可采用一定范围的填充大小。

#### SessionConfirmed（类型 2）

unchanged

#### 数据阶段的密钥派生函数（KDF）

unchanged

#### 中继与对等测试

以下数据块包含版本字段。这些字段将保持版本 2（以兼容不支持后量子密码学的 Bob 端），不会为后量子密码学升级至版本 3/4。

* [CABFORUM](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/)
* [Choosing-Hash](https://kerkour.com/fast-secure-hash-function-sha256-sha512-sha3-blake3)
* [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/)
* [COMMON](/docs/specs/common-structures/)
* [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/)
* [ECIES](/docs/specs/ecies/)
* [FORUM](http://zzz.i2p/topics/3294)
* [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
* [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
* [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)
* [FIPS205](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.205.pdf)
* [MLDSA-OIDS](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/)
* [NIST-PQ](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards)
* [NIST-PQ-UPDATE](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf)
* [NIST-PQ-END](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf)
* [NIST-VECTORS](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values)
* [Noise](https://noiseprotocol.org/noise.html)
* [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf)
* [NSA-PQ](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF)
* [NTCP2](/docs/specs/ntcp2/)
* [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)
* [Prop165](/docs/proposals/165/)
* [PQ-WIREGUARD](https://eprint.iacr.org/2020/379.pdf)
* [RFC-2104](https://tools.ietf.org/html/rfc2104)
* [Rosenpass](https://rosenpass.eu/)
* [Rosenpass-Whitepaper](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf)
* [SSH-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-sshm-mlkem-hybrid-kex/)
* [SSU2](/docs/specs/ssu2/)
* [TLS-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-tls-hybrid-design/)

#### 已发布地址

在所有情况下，请照常使用 SSU2 传输名称。不支持 MLKEM-1024。

使用与非后量子密码（PQ）、非防火墙情况下相同的地址/端口。支持一种或两种后量子变体。在 router 地址中，照常发布 v=2，并发布新参数 pq=[3|4|3,4|4,3]，以指示支持 MLKEM-512/768/两者皆支持。MTU 低于下述最小值的 router 不得发布包含"4"的"pq"参数。发布 4,3 表示优先使用 MLKEM-768，发布 3,4 表示优先使用 MLKEM-512。实际使用的版本由发起方决定，偏好设置不一定会被采纳。MTU 低于下述最小值的 router 不得使用 MLKEM-768 进行连接。旧版 router 将忽略 pq 参数，并照常以非后量子方式进行连接。

不支持与非后量子密码学（non-PQ）不同的地址/端口，或仅后量子密码学（PQ-only）、非防火墙配置。在非后量子 SSU2 被禁用之前（距今还有数年），此功能不会被实现。当非后量子密码学被禁用后，将支持一种或两种后量子密码学变体。在 router 地址中，通过发布 `v=[3|4|3,4|4,3]` 来标识 MLKEM 512/768/两者兼支持。较旧的 router 将检查 `v` 参数，并跳过此地址，视其为不受支持。

防火墙地址（未发布 IP）：在 router 地址中，照常发布 v=2。防火墙地址中必须发布 pq 参数，以支持中继功能。

无论 Alice 是否在其 router info 中公告支持 PQ，或者是否公告相同的变体，她都可以使用 Bob 发布的 PQ 变体连接到支持 PQ 的 Bob。

#### MTU

使用 MLKEM768 时请注意不要超过 MTU 限制。MLKEM768_X25519 的最小 MTU 要求为：IPv4 下 1318 字节，IPv6 下 1338 字节（假设最小有效载荷为 10 字节，包含一个 DateTime 块和一个 Padding 或 RelayTagRequest 块）。SSU2 总体的最小 MTU 为 1280，因此并非所有对等节点都能使用 MLKEM768。如果实际 MTU（无论是本地还是对等节点所通告的）低于上述最小值，则不应发布或使用 MLKEM768。同时需注意，不要因填充（padding）过大而导致消息 1 或消息 2 超出本地或远端的 MTU 限制。

## 开销分析

### 密钥交换

大小增加（字节）：

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Pubkey (Msg 1)</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Ciphertext (Msg 2)</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+816</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+784</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+1200</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+1104</td>
</tr>
</table>
## 安全性分析

NIST 安全类别在 [NIST 演示文稿](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf) 第 10 页中有所概述。初步标准：对于混合协议，我们的最低 NIST 安全类别应为 2；对于纯后量子密码（PQ-only）协议，则应为 3。

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Category</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">As Secure As</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES128</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">SHA256</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES192</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">SHA384</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES256</td>
</tr>
</table>
### 握手

这些都是混合协议。实现应优先选择 MLKEM768；MLKEM512 的安全性不足。

NIST 安全类别 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)：

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Algorithm</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Security Category</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
</tr>
</table>
## 实现说明

### 库支持

Bouncycastle、BoringSSL 和 WolfSSL 库现已支持 MLKEM 和 MLDSA。OpenSSL 的支持将在其 2025 年 4 月 8 日发布的 3.5 版本中提供 [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)。

### 入站流量识别

我们在会话请求中设置临时密钥的最高位（key[31] & 0x80），以表明这是一个混合连接。这使我们能够在同一端口上同时运行标准 NTCP 和混合 NTCP。入站仅支持一种混合变体，并在 router 地址中进行广播。例如，pq=3 或 pq=4。

## 路由器兼容性

### 传输层名称

作为 Alice 方，在建立 PQ 连接时，于混淆处理前，设置 X[31] |= 0x80。这将使 X 成为一个无效的 X25519 公钥。经过混淆处理后，AES-CBC 将对其进行随机化。混淆后，X 的最高有效位将呈随机状态。

## 参考资料

* [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/)
* [COMMON](/docs/specs/common-structures/)
* [ECIES](/docs/specs/ecies/)
* [FORUM](http://zzz.i2p/topics/3294)
* [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
* [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
* [NIST-PQ](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards)
* [NIST-PQ-UPDATE](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf)
* [NIST-PQ-END](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf)
* [NIST-VECTORS](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values)
* [Noise](https://noiseprotocol.org/noise.html)
* [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf)
* [NSA-PQ](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF)
* [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)
* [Prop165](/docs/proposals/165/)
* [PQ-WIREGUARD](https://eprint.iacr.org/2020/379.pdf)
* [RFC-2104](https://tools.ietf.org/html/rfc2104)
* [Rosenpass](https://rosenpass.eu/)
* [Rosenpass-Whitepaper](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf)
* [SSH-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-sshm-mlkem-hybrid-kex/)
* [SSU2](/docs/specs/ssu2/)
* [TLS-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-tls-hybrid-design/)
