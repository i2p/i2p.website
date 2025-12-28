---
title: "ECIES-X25519-AEAD-Ratchet 混合加密"
description: "采用 ML-KEM（基于格的密钥封装机制）的 ECIES 加密协议的后量子混合变体"
slug: "ecies-hybrid"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## 实现状态

**当前部署:** - **i2pd (C++ 实现)**: 已在版本 2.58.0 (2025 年 9 月) 中完整实现，并支持 ML-KEM-512、ML-KEM-768 和 ML-KEM-1024。当可用 OpenSSL 3.5.0 或更高版本时，默认启用后量子端到端加密。 - **Java I2P**: 截至版本 0.9.67 / 2.10.0 (2025 年 9 月) 尚未实现。规范已获批准，计划在未来版本中实现。

本规范描述了已获批准的功能，这些功能目前已在 i2pd 部署，并计划在 Java I2P 实现中采用。

## 概述

这是 ECIES-X25519-AEAD-Ratchet 协议 [ECIES](/docs/specs/ecies/) 的后量子混合变体。它是有待批准的提案 169 [Prop169](/proposals/169-pq-crypto/) 的第一阶段。有关总体目标、威胁模型、分析、替代方案及更多信息，请参阅该提案。

提案 169 状态：**开放** (混合 ECIES（椭圆曲线集成加密方案）实现的第一阶段已获批准).

本规范仅包含相对于标准 [ECIES](/docs/specs/ecies/)（椭圆曲线集成加密方案）的差异，必须与该规范一并阅读。

## 设计

我们使用 NIST FIPS 203 标准 [FIPS203](https://csrc.nist.gov/pubs/fips/203/final)，该标准以 CRYSTALS-Kyber 为基础，但与其不兼容（版本 3.1、3 以及更早版本）。

混合握手将经典的 X25519 Diffie-Hellman 与后量子 ML-KEM 密钥封装机制（NIST 后量子密钥封装标准，原名 Kyber）相结合。这种方法基于 PQNoise（关于混合前向保密的研究）中记录的混合前向保密概念，以及在 TLS 1.3、IKEv2 和 WireGuard 中的类似实现。

### 密钥交换

我们为 Ratchet（棘轮机制）定义了一种混合密钥交换。后量子 KEM（密钥封装机制）仅提供临时密钥，并不直接支持诸如 Noise IK 之类的静态密钥握手。

我们按照 [FIPS203](https://csrc.nist.gov/pubs/fips/203/final) 的规定定义三种 ML-KEM（基于模块格的密钥封装机制）变体，共计新增 3 种加密类型。混合类型仅在与 X25519（椭圆曲线 Diffie–Hellman 密钥交换算法的一种实现）组合时定义。

新的加密类型为：

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Security Level</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">ML-KEM Variant</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NIST Category 1 (AES-128 equivalent)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ML-KEM-512</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NIST Category 3 (AES-192 equivalent)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ML-KEM-768 (Recommended)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NIST Category 5 (AES-256 equivalent)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ML-KEM-1024</td>
    </tr>
  </tbody>
</table>
**注意：** MLKEM768_X25519（Type 6）是推荐的默认变体，在合理开销下提供强大的后量子安全性。

与仅使用 X25519 的加密相比，额外开销相当可观。针对 IK 模式，消息 1 和 2 的典型大小目前约为 96-103 字节（不含额外负载）。根据消息类型不同，这一数值在 MLKEM512 情况下将增加约 9-12 倍，在 MLKEM768 情况下增加约 13-16 倍，在 MLKEM1024 情况下增加约 17-23 倍。

### 需要新的加密技术

- **ML-KEM**（原名 CRYSTALS-Kyber）[FIPS203](https://csrc.nist.gov/pubs/fips/203/final) - 基于模格的密钥封装机制标准
- **SHA3-256**（原名 Keccak-512）[FIPS202](https://csrc.nist.gov/pubs/fips/202/final) - SHA-3 标准的一部分
- **SHAKE128 和 SHAKE256**（SHA3 的 XOF（可扩展输出函数）扩展）[FIPS202](https://csrc.nist.gov/pubs/fips/202/final) - 可扩展输出函数

SHA3-256、SHAKE128 和 SHAKE256 的测试向量可在 [NIST 加密算法验证计划](https://csrc.nist.gov/Projects/cryptographic-algorithm-validation-program) 中获取。

**库支持:** - Java: Bouncycastle 库 1.79 及以上版本支持所有 ML-KEM（模块格密钥封装机制）变体以及 SHA3/SHAKE 函数 - C++: OpenSSL 3.5 及以上版本包含对 ML-KEM 的完整支持（于 2025 年 4 月发布） - Go: 有多种库可用于 ML-KEM 和 SHA3 的实现

## 规范

### 通用结构

有关密钥长度和标识符，请参阅[通用结构规范](/docs/specs/common-structures/)。

### 握手模式

握手使用 [Noise Protocol Framework](https://noiseprotocol.org/noise.html)（Noise 协议框架）的握手模式，并结合针对 I2P 的特定改动，以实现混合式后量子安全性。

使用以下字母映射：

- **e** = 一次性临时密钥（X25519）
- **s** = 静态密钥
- **p** = 消息负载
- **e1** = 一次性临时 PQ（后量子）密钥，从 Alice 发送给 Bob（I2P 特定的令牌）
- **ekem1** = KEM（密钥封装机制）密文，从 Bob 发送给 Alice（I2P 特定的令牌）

**重要说明：** 模式名称 "IKhfs" 和 "IKhfselg2" 以及标记 "e1" 和 "ekem1" 是 I2P 特定的适配，未记录于官方 Noise 协议框架规范中。这些表示为将 ML-KEM（模块格密钥封装机制）集成到 Noise IK 模式而做的自定义定义。尽管混合的 X25519 + ML-KEM 方案在后量子密码学研究和其他协议中广为认可，但此处使用的特定命名法是 I2P 特有的。

将以下修改应用于 IK，以实现混合前向保密：

```
Standard IK:              I2P IKhfs (Hybrid):
<- s                      <- s
...                       ...
-> e, es, s, ss, p        -> e, es, e1, s, ss, p
<- e, ee, se, p           <- e, ee, ekem1, se, p
<- p                      <- p
p ->                      p ->

Note: e1 and ekem1 are encrypted within ChaCha20-Poly1305 AEAD blocks.
Note: e1 (ML-KEM public key) and ekem1 (ML-KEM ciphertext) have different sizes.
```
**e1** 模式定义如下：

```
For Alice (sender):
(encap_key, decap_key) = PQ_KEYGEN()

// EncryptAndHash(encap_key)
ciphertext = ENCRYPT(k, n, encap_key, ad)
n++
MixHash(ciphertext)

For Bob (receiver):
// DecryptAndHash(ciphertext)
encap_key = DECRYPT(k, n, ciphertext, ad)
n++
MixHash(ciphertext)
```
**ekem1** 模式定义如下：

```
For Bob (receiver of encap_key):
(kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

// EncryptAndHash(kem_ciphertext)
ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)
MixHash(ciphertext)

// MixKey
MixKey(kem_shared_key)

For Alice (sender of encap_key):
// DecryptAndHash(ciphertext)
kem_ciphertext = DECRYPT(k, n, ciphertext, ad)
MixHash(ciphertext)

// MixKey
kem_shared_key = DECAPS(kem_ciphertext, decap_key)
MixKey(kem_shared_key)
```
### 定义的 ML-KEM（基于模块格的密钥封装机制）操作

我们定义以下函数，它们对应于 [FIPS203](https://csrc.nist.gov/pubs/fips/203/final) 所规定的密码学构建模块。

**(encap_key, decap_key) = PQ_KEYGEN()** : Alice 生成封装密钥和解封装密钥。封装密钥在 NS 消息中发送。密钥大小：   - ML-KEM-512: encap_key = 800 字节, decap_key = 1632 字节   - ML-KEM-768: encap_key = 1184 字节, decap_key = 2400 字节   - ML-KEM-1024: encap_key = 1568 字节, decap_key = 3168 字节

**(ciphertext, kem_shared_key) = ENCAPS(encap_key)** : Bob 使用在 NS 消息中收到的封装密钥计算密文和共享密钥。密文在 NSR 消息中发送。密文大小:   - ML-KEM-512: 768 字节   - ML-KEM-768: 1088 字节   - ML-KEM-1024: 1568 字节

kem_shared_key 在所有三种变体中始终为 **32 字节**。

**kem_shared_key = DECAPS(ciphertext, decap_key)** : Alice 使用在 NSR 消息中收到的密文计算共享密钥。kem_shared_key 始终为 **32 字节**。

**重要：** encap_key 和 ciphertext 都在 Noise（加密握手协议框架）的握手消息 1 和 2 中的 ChaCha20-Poly1305 块内被加密。它们会作为握手过程的一部分被解密。

使用 MixKey() 将 kem_shared_key 混入链密钥。详见下文。

### Noise 握手的密钥派生函数

#### 概述

混合握手将经典的 X25519 ECDH（椭圆曲线 Diffie-Hellman）与后量子 ML-KEM（密钥封装机制）相结合。第一条消息（从 Alice 发往 Bob）在消息载荷之前包含 e1（ML-KEM 封装密钥）。将其视为额外的密钥材料；对其调用 EncryptAndHash()（作为 Alice）或 DecryptAndHash()（作为 Bob）。然后按常规处理消息载荷。

第二条消息（从 Bob 发往 Alice）在消息负载之前包含 ekem1（ML-KEM 密文）。将其视为额外的密钥材料；对其调用 EncryptAndHash()（作为 Bob）或 DecryptAndHash()（作为 Alice）。随后计算 kem_shared_key，并调用 MixKey(kem_shared_key)。然后照常处理消息负载。

#### Noise 标识符

这些是 Noise（加密握手协议框架）初始化字符串（I2P 专用）：

- `Noise_IKhfselg2_25519+MLKEM512_ChaChaPoly_SHA256`
- `Noise_IKhfselg2_25519+MLKEM768_ChaChaPoly_SHA256`
- `Noise_IKhfselg2_25519+MLKEM1024_ChaChaPoly_SHA256`

#### 用于 NS 消息的 Alice 端 KDF（密钥派生函数）

在 'es' 消息模式之后、's' 消息模式之前，添加：

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
#### Bob 端 NS 消息的密钥派生函数

在 'es' 消息模式之后，并在 's' 消息模式之前，添加：

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
#### 用于 NSR 消息的 Bob 侧 KDF（密钥派生函数）

在 'ee' 消息模式之后、'se' 消息模式之前，添加：

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
```
#### 用于 NSR 消息的 Alice KDF（密钥派生函数）

在 'ee' 消息模式之后且在 'ss' 消息模式之前，添加：

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
```
#### 用于 split() 的密钥派生函数

split() 函数保持与标准 ECIES（椭圆曲线集成加密方案）规范一致，未作改动。握手完成后：

```
keydata = HKDF(chainKey, ZEROLEN, "", 64)
k_ab = keydata[0:31]
k_ba = keydata[32:63]
```
这些是用于持续通信的双向会话密钥。

### 消息格式

#### NS (New Session，新会话) 格式

**Changes:** 当前的棘轮在第一个 ChaCha20-Poly1305 部分中包含静态密钥，在第二个部分中包含有效载荷。随着 ML-KEM 的引入，现在有三个部分。第一部分包含加密的 ML-KEM 公钥（encap_key）。第二部分包含静态密钥。第三部分包含有效载荷。

**消息大小：**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">X25519 len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NS len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NS Enc len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NS Dec len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">PQ key len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">pl len</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">96+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">--</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">912+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">880+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">800+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">800</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1296+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1264+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1184+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1184</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1680+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1648+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1568+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1568</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
  </tbody>
</table>
**注意：** 负载必须包含一个 DateTime 块（日期时间块）（最少 7 字节：1 字节类型、2 字节大小、4 字节时间戳）。因此，可以相应地计算出 NS 的最小大小。由此，X25519 的可用最小 NS 大小为 103 字节，而混合变体范围为 919 到 1687 字节。

对于三个 ML-KEM 变体，大小分别增加 816、1200 和 1584 字节，这些增加量由 ML-KEM 公钥以及用于认证加密的 16 字节 Poly1305 消息认证码（MAC）共同构成。

#### NSR（New Session Reply，新会话应答）格式

**变更：** 当前的 ratchet（密钥棘轮）在第一个 ChaCha20-Poly1305 部分的负载为空，负载位于第二个部分。引入 ML-KEM 后，现在有三个部分。第一部分包含加密的 ML-KEM 密文。第二部分的负载为空。第三部分包含负载。

**消息大小：**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">X25519 len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NSR len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NSR Enc len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NSR Dec len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">PQ ct len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">pl len</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">72+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">40+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">--</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">856+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">824+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">784+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">768</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1176+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1144+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1104+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1088</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1656+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1624+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1584+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1568</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
  </tbody>
</table>
对于三种 ML-KEM（基于模格的密钥封装机制）变体，大小分别增加 784、1104 和 1584 字节；这些增量由 ML-KEM 密文以及用于认证加密的 16 字节 Poly1305 消息认证码（MAC）共同构成。

## 开销分析

### 密钥交换

与仅使用 X25519 相比，混合加密的开销相当可观：

- **MLKEM512_X25519**: 握手消息大小约增加 9-12 倍 (NS: 9.5 倍, NSR: 11.9 倍)
- **MLKEM768_X25519**: 握手消息大小约增加 13-16 倍 (NS: 13.5 倍, NSR: 16.3 倍)
- **MLKEM1024_X25519**: 握手消息大小约增加 17-23 倍 (NS: 17.5 倍, NSR: 23 倍)

为获得后量子安全带来的额外收益，这种开销是可以接受的。由于基础消息大小不同，各消息类型的倍率也会有所不同（NS 最小为 96 字节，NSR 最小为 72 字节）。

### 带宽注意事项

对于典型的会话建立且负载最小的场景： - 仅 X25519：总计 ~200 字节（NS + NSR） - MLKEM512_X25519：总计 ~1,800 字节（增长 9 倍） - MLKEM768_X25519：总计 ~2,500 字节（增长 12.5 倍） - MLKEM1024_X25519：总计 ~3,400 字节（增长 17 倍）

在会话建立之后，后续的消息加密使用与仅使用 X25519 的会话相同的数据传输格式，因此不会给后续消息带来额外开销。

## 安全分析

### 握手

混合握手同时提供经典（X25519）与后量子（ML-KEM）的安全性。攻击者必须破解**两者**：经典的ECDH（椭圆曲线Diffie-Hellman）和后量子的KEM（密钥封装机制），才能危及会话密钥。

这提供： - **当前安全性**：X25519 ECDH 可抵御传统攻击者（128 位安全级别） - **未来安全性**：ML-KEM（模块格密钥封装机制）可抵御量子攻击者（因参数集而异） - **混合安全性**：要危及会话，必须同时攻破二者（安全级别 = 两者中的最大值）

### 安全级别

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Variant</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NIST Category</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Classical Security</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">PQ Security</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Hybrid Security</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Category 1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit (X25519)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-128 equivalent</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Category 3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit (X25519)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-192 equivalent</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Category 5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit (X25519)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 equivalent</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit</td>
    </tr>
  </tbody>
</table>
**注意：** 混合安全级别受两种组成部分中较弱者所限制。在所有情况下，X25519（基于 Curve25519 的椭圆曲线 Diffie-Hellman 密钥交换算法）提供 128 位经典安全性。若出现具备密码学相关能力的量子计算机，安全级别将取决于所选择的 ML-KEM（基于模格的密钥封装机制，NIST 标准 Kyber）参数集。

### 前向保密

这种混合方案保持了前向保密性。会话密钥由临时的 X25519 和临时的 ML-KEM（模块格密钥封装机制，后量子密钥封装算法）密钥交换共同导出。只要在握手后销毁 X25519 或 ML-KEM 的临时私钥，即使长期静态密钥被泄露，过去的会话也无法被解密。

在第二个消息（NSR）发送后，IK 模式即可提供完全的前向保密（Noise Confidentiality level 5，Noise 协议的机密性等级 5）。

## 类型首选项

实现应支持多种混合类型，并协商选择双方共同支持的最强变体。偏好顺序应为：

1. **MLKEM768_X25519** (后量子密钥封装机制（KEM）与 X25519 的混合密钥交换套件) (Type 6) - 推荐的默认选项，安全性与性能的最佳平衡
2. **MLKEM1024_X25519** (Type 7) - 适用于敏感应用的最高安全性
3. **MLKEM512_X25519** (Type 5) - 面向资源受限场景的基础级后量子安全
4. **X25519** (Type 4) - 仅经典算法，用于兼容性的回退选项

**理由:** 推荐将 MLKEM768_X25519 作为默认选项，因为它提供 NIST 第3类安全性（等效于 AES-192），在对抗量子计算机方面被认为足够，同时还能保持合理的消息大小。MLKEM1024_X25519 提供更高的安全性，但开销会显著增加。

## 实现说明

### 库支持

- **Java**：Bouncycastle 库 1.79 版（2024 年 8 月）及更高版本支持所有所需的 ML-KEM（模块格密钥封装机制）变体和 SHA3/SHAKE 函数。为符合 FIPS 203，请使用 `org.bouncycastle.pqc.crypto.mlkem.MLKEMEngine`。
- **C++**：OpenSSL 3.5（2025 年 4 月）及之后的版本通过 EVP_KEM 接口包含对 ML-KEM 的支持。该版本为长期支持（LTS）版本，维护至 2030 年 4 月。
- **Go**：有多种第三方库可用于 ML-KEM 和 SHA3，其中包括 Cloudflare 的 CIRCL 库。

### 迁移策略

实现应：1. 在过渡期内同时支持 X25519-only 和混合 ML-KEM（模块格密钥封装机制）变体 2. 当双方对等节点都支持时优先选择混合变体 3. 为向后兼容保留回退到 X25519-only 4. 在选择默认变体时考虑网络带宽约束

### 共享 Tunnels

消息大小的增加可能会影响共享 tunnel 的使用。实现应考虑： - 在可能的情况下将握手批量处理，以摊平开销 - 对混合会话使用更短的到期时间，以减少已存储的状态 - 监控带宽使用情况并相应调整参数 - 对会话建立流量实施拥塞控制

### 新会话大小注意事项

由于握手消息更大，各实现可能需要： - 增加用于会话协商的缓冲区大小（建议至少 4KB） - 为较慢的连接调整超时值（考虑到消息大小约为原来的 ~3–17 倍） - 考虑对 NS/NSR 消息中的有效载荷数据进行压缩 - 如果传输层需要，实现分片处理

### 测试与验证

实现应验证: - 正确的 ML-KEM（密钥封装机制）密钥生成、封装与解封装 - 将 kem_shared_key 正确集成到 Noise KDF（密钥派生函数）中 - 消息大小的计算与规范相一致 - 与其他 I2P router 实现的互操作性 - 当 ML-KEM 不可用时的回退行为

用于 ML-KEM（模块格密钥封装机制）操作的测试向量可在 NIST [加密算法验证计划](https://csrc.nist.gov/Projects/cryptographic-algorithm-validation-program) 中获得。

## 版本兼容性

**I2P 版本编号：** I2P 采用两套并行的版本号： - **Router 发行版本**: 2.x.x 格式（例如，2.10.0 于 2025 年 9 月发布） - **API/协议版本**: 0.9.x 格式（例如，0.9.67 对应于 router 2.10.0）

本规范参考协议版本 0.9.67，对应于 router 发布版本 2.10.0 及更高版本。

**兼容性矩阵：**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Implementation</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">ML-KEM Support</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2pd</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.58.0+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Full (512/768/1024)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deployed September 2025</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Java I2P</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67 / 2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Not yet</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Planned for future release</td>
    </tr>
  </tbody>
</table>
## 参考资料

- **[ECIES]**: [ECIES-X25519-AEAD-Ratchet 规范](/docs/specs/ecies/)
- **[Prop169]**: [提案 169：后量子密码学](/proposals/169-pq-crypto/)
- **[FIPS203]**: [NIST FIPS 203 - ML-KEM 标准](https://csrc.nist.gov/pubs/fips/203/final)
- **[FIPS202]**: [NIST FIPS 202 - SHA-3 标准](https://csrc.nist.gov/pubs/fips/202/final)
- **[Noise]**: [Noise 协议框架](https://noiseprotocol.org/noise.html)
- **[COMMON]**: [通用结构规范](/docs/specs/common-structures/)
- **[RFC7539]**: [RFC 7539 - ChaCha20 与 Poly1305](https://www.rfc-editor.org/rfc/rfc7539)
- **[RFC5869]**: [RFC 5869 - HKDF](https://www.rfc-editor.org/rfc/rfc5869)
- **[OpenSSL]**: [OpenSSL 3.5 ML-KEM 文档](https://docs.openssl.org/3.5/man7/EVP_KEM-ML-KEM/)
- **[Bouncycastle]**: [Bouncycastle Java 加密库](https://www.bouncycastle.org/)

---
