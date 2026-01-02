---
title: "通用结构"
description: "I2P 规范中通用的共享数据类型与序列化格式"
slug: "common-structures"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## 概述

本文档规定了适用于所有 I2P 协议的基础数据结构，包括 [I2NP](/docs/specs/i2np/)、[I2CP](/docs/specs/i2cp/)、[SSU2](/docs/specs/ssu2/)、[NTCP2](/docs/specs/ntcp2/) 等。这些通用结构确保不同 I2P 实现与协议层之间的互操作性。

### 自 0.9.58 以来的关键变更

- 在 Router 标识中弃用 ElGamal 和 DSA-SHA1（使用 X25519 + EdDSA）
- 后量子 ML-KEM（密钥封装机制）支持处于测试版阶段（自 2.10.0 起需用户主动启用）
- 服务记录选项已标准化（[提案 167](/proposals/167-service-records/)，在 0.9.66 中实现）
- 可压缩填充规范已最终确定（[提案 161](/zh/proposals/161-ri-dest-padding/)，在 0.9.57 中实现）

---

## 通用类型规范

### 整数

**描述：** 表示一个以网络字节序（大端序）编码的非负整数。

**内容：** 长度为 1 到 8 个字节，表示一个无符号整数。

**用法：** I2P 协议各处的字段长度、计数、类型标识符和数值。

---

### 日期

**描述:** 时间戳，表示自 Unix 纪元（1970 年 1 月 1 日 00:00:00 GMT）以来的毫秒数。

**内容：** 8 字节整数（无符号长整型）

**特殊值：** - `0` = 未定义或空日期 - 最大值: `0xFFFFFFFFFFFFFFFF` (年份 584,942,417,355)

**实现注意事项:** - 始终使用 UTC/GMT 时区 - 需要毫秒级精度 - 用于租约过期、RouterInfo 发布以及时间戳验证

---

### 字符串

**描述：** 带有长度前缀的 UTF-8 编码字符串。

**格式:**

```
+----+----+----+----+----+----+
|len | UTF-8 encoded data...   |
+----+----+----+----+----+----+

len :: Integer (1 byte)
       Value: 0-255 (string length in bytes, NOT characters)

data :: UTF-8 encoded bytes
        Length: 0-255 bytes
```
**约束条件：** - 最大长度：255 字节（不是字符 - 多字节 UTF-8 序列按多个字节计算） - 长度可以为零（空字符串） - 不包含空字符终止符（null terminator） - 字符串不是以空字符结尾

**重要：** UTF-8 编码序列每个字符可以使用多个字节。一个包含 100 个字符的字符串，如果使用多字节字符，可能会超过 255 字节的限制。

---

## 密码学密钥结构

### 公钥

**描述：** 用于非对称加密的公钥。密钥类型和长度取决于上下文，或在密钥证书中指定。

**默认类型：** ElGamal (自 0.9.58 起在 Router 身份中已弃用)

**支持的类型：**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destinations only (unused field)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated for RIs</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">132</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Recommended</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">800</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1184</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1568</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512_CT</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">768</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768_CT</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1088</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024_CT</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1568</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
  </tbody>
</table>
**实现要求:**

1. **X25519 (类型 4) - 当前标准:**
   - 用于 ECIES-X25519-AEAD-Ratchet 加密
   - 自 0.9.48 起对 Router 标识为强制要求
   - 小端序编码 (与其他类型不同)
   - 参见 [ECIES](/docs/specs/ecies/) 和 [ECIES-ROUTERS](/docs/specs/ecies/#routers)

2. **ElGamal (Type 0) - 遗留:**
   - 自 0.9.58 起，已弃用于 Router 身份
   - 对 Destination（目标）仍然有效（该字段自 0.6/2005 起未使用）
   - 使用 [ElGamal 规范](/docs/specs/cryptography/) 中定义的固定素数
   - 为向后兼容而保留支持

3. **MLKEM（后量子） - 测试版：**
   - 混合方案将 ML-KEM 与 X25519 结合
   - 在 2.10.0 中默认未启用
   - 需要通过 Hidden Service Manager（隐藏服务管理器）手动启用
   - 参见 [ECIES-HYBRID](/docs/specs/ecies/#hybrid) 和 [Proposal 169](/proposals/169-pq-crypto/)
   - 类型代码和规范可能会变更

**JavaDoc：** [PublicKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/PublicKey.html)

---

### 私钥

**Description:** 用于非对称解密、与 PublicKey 类型相对应的私钥。

**存储：** 类型和长度由上下文推断，或单独保存在数据结构/密钥文件中。

**支持的类型：**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destinations only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated for RIs</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">48</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">66</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Recommended</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1632</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2400</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3168</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
  </tbody>
</table>
**安全注意事项：** - 私钥必须使用密码学安全的随机数生成器生成 - X25519 私钥按 RFC 7748 的定义采用标量夹紧（scalar clamping） - 在不再需要时，必须从内存中安全地擦除密钥材料

**JavaDoc：** [PrivateKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/PrivateKey.html)

---

### 会话密钥

**说明：** 用于 I2P 的 tunnel 与 garlic encryption 中进行 AES-256 加密与解密的对称密钥。

**内容：** 32 字节（256 位）

**用途：** - tunnel 层加密 (AES-256/CBC with IV) - garlic 消息加密 - 端到端会话加密

**生成:** 必须使用密码学安全的随机数生成器。

**JavaDoc：** [SessionKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SessionKey.html)

---

### SigningPublicKey

**描述:** 用于验证签名的公钥。类型和长度由 Destination（I2P 目标标识）的密钥证书指定，或由上下文推断。

**默认类型：** DSA_SHA1 (自 0.9.58 起已弃用)

**支持的类型：**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA_SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">128</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA256_P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Older Destinations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA384_P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA512_P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">132</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA256_2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA384_3072</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA512_4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Recommended for SU3</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Recommended</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519ph</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.25</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RedDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted leasesets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specialized</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved (GOST)</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">9</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Proposal 134</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved (GOST)</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">128</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Proposal 134</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved (MLDSA)</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12-20</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Proposal 169</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">65280-65534</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Testing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Never production</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">65535</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Future expansion</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td></tr>
  </tbody>
</table>
**实现要求:**

1. **EdDSA_SHA512_Ed25519 (Type 7) - 当前标准：**
   - 自 2015 年末以来，默认用于所有新的 router 身份和 Destination（目的地）
   - 使用 Ed25519 曲线与 SHA-512 哈希
   - 32 字节公钥，64 字节签名
   - 小端序编码（与大多数其他类型不同）
   - 高性能与高安全性

2. **RedDSA_SHA512_Ed25519 (Type 11) - 专用:**
   - 仅用于加密的 leaseSet 和盲化
   - 绝不用于 Router 身份标识或标准目标
   - 与 EdDSA 的关键差异：
     - 私钥采用模约减（而非钳位）
     - 签名包含 80 字节的随机数据
     - 直接使用公钥（而非私钥的哈希）
   - 参见 [Red25519 规范](//docs/specs/red25519-signature-scheme/

3. **DSA_SHA1 (Type 0) - 遗留：**
   - 自 0.9.58 起，对 Router 身份标识已弃用
   - 不建议用于新的 Destinations（目标）
   - 1024 位 DSA 与 SHA-1（已知弱点）
   - 仅为兼容性而保留支持

4. **多元素密钥：**
   - 由两个元素组成时（例如，ECDSA 点 X、Y）
   - 每个元素在前面用零填充至 length/2 的长度
   - 示例：64 字节的 ECDSA 密钥 = 32 字节的 X + 32 字节的 Y

**JavaDoc：** [SigningPublicKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SigningPublicKey.html)

---

### SigningPrivateKey

**说明：** 用于创建签名的私钥，对应于 SigningPublicKey 类型。

**存储：** 类型和长度在创建时指定。

**支持的类型：**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA_SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA256_P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Older Destinations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA384_P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">48</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA512_P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">66</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA256_2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA384_3072</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">768</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA512_4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1024</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Recommended for SU3</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Recommended</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519ph</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.25</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RedDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted leasesets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specialized</td></tr>
  </tbody>
</table>
**安全要求：** - 使用密码学安全的随机数源生成 - 使用适当的访问控制进行保护 - 完成后从内存中安全擦除 - 对于 EdDSA：将 32 字节种子经 SHA-512 哈希，取前 32 字节作为标量（经 clamping 位约束处理） - 对于 RedDSA：密钥生成方式不同（使用模约简而非 clamping）

**JavaDoc：** [SigningPrivateKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SigningPrivateKey.html)（签名私钥）

---

### 签名

**说明:** 对数据的密码学签名，使用与 SigningPrivateKey 类型相对应的签名算法。

**类型和长度：** 根据用于签名的密钥类型推断。

**支持的类型:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA_SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">40</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA256_P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Older Destinations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA384_P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA512_P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">132</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA256_2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA384_3072</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA512_4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current for SU3</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Recommended</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519ph</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.25</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RedDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted leasesets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specialized</td></tr>
  </tbody>
</table>
**格式说明：** - 多元素签名（例如 ECDSA 的 R、S 值）使用前导零将每个元素填充到 length/2 的长度 - EdDSA 和 RedDSA 使用小端序编码 - 其他所有类型使用大端序编码

**验证:** - 使用相应的 SigningPublicKey - 遵循该密钥类型的签名算法规范 - 检查签名长度是否与该密钥类型的预期长度匹配

**JavaDoc：** [Signature](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Signature.html)

---

### 哈希

**描述：** 对数据的 SHA-256 哈希，在 I2P 中广泛用于完整性校验和标识。

**内容：** 32 字节 (256 位)

**用途：** - Router Identity 哈希（网络数据库键） - Destination 哈希（网络数据库键） - 在 Leases 中的 Tunnel 网关标识 - 数据完整性验证 - Tunnel ID 生成

**算法：** 根据 FIPS 180-4 定义的 SHA-256

**JavaDoc:** [哈希](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Hash.html)

---

### 会话标签

**描述:** 用于会话标识和基于标签的加密的随机数。

**重要:** Session Tag（会话标签）的大小会因加密类型而异: - **ElGamal/AES+SessionTag:** 32 字节（遗留） - **ECIES-X25519:** 8 字节（当前标准）

**当前标准（ECIES，椭圆曲线集成加密方案）：**

```
Contents: 8 bytes
Usage: Ratchet-based encryption for Destinations and Routers
```
有关详细规范，请参见 [ECIES](/docs/specs/ecies/) 和 [ECIES-ROUTERS](/docs/specs/ecies/#routers)。

**旧版（ElGamal/AES）：**

```
Contents: 32 bytes
Usage: Deprecated encryption scheme
```
**生成：** 必须使用密码学安全的随机数生成器。

**JavaDoc：** [SessionTag](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SessionTag.html)

---

### TunnelId

**描述：**用于标识 router 在 tunnel 中位置的唯一标识符。一个 tunnel 中的每一跳都有其自己的 TunnelId。

**格式:**

```
Contents: 4-byte Integer (unsigned 32-bit)
Range: Generally > 0 (zero reserved for special cases)
```
**用途：** - 在每个 router 识别入站/出站 tunnel 连接 - 在 tunnel 链的每一跳使用不同的 TunnelId - 用于 Lease（租约）结构中以标识网关 tunnel

**特殊值：** - `0` = 保留用于协议的特殊用途（在正常运行中应避免使用） - TunnelIds 对每个 router 仅具有本地意义

**JavaDoc 文档:** [TunnelId](http://docs.i2p-projekt.de/javadoc/net/i2p/data/TunnelId.html)

---

## 证书规范

### 证书

**描述：** 在整个 I2P 中使用的收据、工作量证明或密码学元数据的容器。

**格式：**

```
+----+----+----+----+----+----+-//
|type| length  | payload
+----+----+----+----+----+----+-//

type :: Integer (1 byte)
        Values: 0-5 (see types below)

length :: Integer (2 bytes, big-endian)
          Size of payload in bytes

payload :: data
           length -> $length bytes
```
**总大小：** 最少 3 字节 (NULL certificate，空证书), 最多 65538 字节

### 证书类型

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Payload Length</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Total Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">NULL</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Default/empty certificate</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">HASHCASH</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused (was for proof-of-work)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">HIDDEN</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused (hidden routers don't advertise)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SIGNED</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 or 72</td><td style="border:1px solid var(--color-border); padding:0.5rem;">43 or 75</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused (DSA signature ± destination hash)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MULTIPLE</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused (multiple certificates)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">KEY</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4+</td><td style="border:1px solid var(--color-border); padding:0.5rem;">7+</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Current</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specifies key types (see below)</td></tr>
  </tbody>
</table>
### 密钥证书（类型5）

**简介:** 版本 0.9.12 (2013年12月)

**目的：** 指定非默认的密钥类型，并在标准 384 字节的 KeysAndCert 结构之外存储额外的密钥数据。

**有效载荷结构：**

```
+----+----+----+----+----+----+----+----+-//
|SPKtype|CPKtype| Excess SPK data     |
+----+----+----+----+----+----+----+----+-//
              | Excess CPK data...    |
+----+----+----+----+----+----+----+----+

SPKtype :: Signing Public Key Type (2 bytes)
           See SigningPublicKey table above

CPKtype :: Crypto Public Key Type (2 bytes)
           See PublicKey table above

Excess SPK data :: Signing key bytes beyond 128 bytes
                   Length: 0 to 65531 bytes

Excess CPK data :: Crypto key bytes beyond 256 bytes
                   Length: 0 to remaining space
```
**关键实现注意事项：**

1. **密钥类型顺序：**
   - **警告：**签名密钥类型在加密密钥类型之前
   - 这看起来反直觉，但为兼容性而保留
   - 顺序：SPKtype, CPKtype（不是 CPKtype, SPKtype）

2. **KeysAndCert（密钥与证书结构）中的密钥数据布局：**
   ```
   [Crypto Public Key (partial/complete)]
   [Padding (if total key lengths < 384)]
   [Signing Public Key (partial/complete)]
   [Certificate Header (3 bytes)]
   [Key Certificate (4+ bytes)]
   [Excess Signing Key Data]
   [Excess Crypto Key Data]
   ```

3. **计算超出部分的密钥数据:**
   - 如果 Crypto Key > 256 字节: Excess = (Crypto Length - 256)
   - 如果 Signing Key > 128 字节: Excess = (Signing Length - 128)
   - Padding = max(0, 384 - Crypto Length - Signing Length)

**示例（ElGamal 加密密钥）：**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Signing Key Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Total SPK Length</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Padding</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Excess in Cert</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Total Structure Size</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA_SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">128</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 7 = 394</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 7 = 394</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 7 = 394</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">132</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 11 = 398</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">128</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 135 = 522</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">384</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 391 = 778</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 7 = 394</td></tr>
  </tbody>
</table>
**Router 身份要求：** - 使用 NULL 证书直到 0.9.15 版本 - 自 0.9.16 起，非默认密钥类型需要密钥证书 - 自 0.9.48 起，支持 X25519 加密密钥

**Destination（目的地标识）要求：** - 按需使用 NULL 证书或密钥证书 - 自 0.9.12 起，非默认的签名密钥类型需要密钥证书 - 自 0.6（2005）起，加密公钥字段不再使用，但仍必须存在

**重要警告：**

1. **NULL 与 KEY 证书：**
   - 带有类型 (0,0) 并指定 ElGamal+DSA_SHA1 的 KEY 证书是允许的，但不建议使用
   - 对于 ElGamal+DSA_SHA1，应始终使用 NULL 证书（规范表示）
   - 带有 (0,0) 的 KEY 证书会多出 4 字节，并可能引发兼容性问题
   - 某些实现可能无法正确处理带有 (0,0) 的 KEY 证书

2. **多余数据验证:**
   - 实现必须验证证书长度与对应密钥类型的预期长度相匹配
   - 拒绝包含与密钥类型不对应的多余数据的证书
   - 禁止在有效证书结构之后出现尾随垃圾数据

**JavaDoc：** [证书](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Certificate.html)

---

### 映射

**描述：** 用于配置和元数据的键值对属性集合。

**格式:**

```
+----+----+----+----+----+----+----+----+
|  size   | key_string (len + data)| =  |
+----+----+----+----+----+----+----+----+
| val_string (len + data)     | ;  | ...
+----+----+----+----+----+----+----+

size :: Integer (2 bytes, big-endian)
        Total number of bytes that follow (not including size field)
        Range: 0 to 65535

key_string :: String
              Format: 1-byte length + UTF-8 data
              Length: 0-255 bytes

= :: Single byte (0x3D, '=' character)

val_string :: String
              Format: 1-byte length + UTF-8 data
              Length: 0-255 bytes

; :: Single byte (0x3B, ';' character)

[Repeat key_string = val_string ; for additional entries]
```
**大小限制：** - 键长度：0-255 字节 (+ 1 个长度字节) - 值长度：0-255 字节 (+ 1 个长度字节) - 映射总大小：0-65535 字节 (+ 2 个大小字段字节) - 最大结构大小：65537 字节

**关键排序要求：**

当映射出现在**签名结构**（RouterInfo、RouterAddress、Destination 属性、I2CP SessionConfig）中时，为确保签名不变性，条目必须按键排序：

1. **排序方法:** 使用 Unicode 码点值的字典序排序（等同于 Java String.compareTo()）
2. **大小写敏感性:** 键和值通常区分大小写（取决于应用程序）
3. **重复键:** 在已签名的结构中不允许（会导致签名验证失败）
4. **字符编码:** UTF-8 字节级比较

**为什么排序很重要:** - 签名是基于字节表示来计算的 - 不同的键顺序会产生不同的签名 - 未签名的映射不要求排序，但应遵循相同的约定

**实现说明：**

1. **编码冗余:**
   - 同时存在 `=` 和 `;` 分隔符以及字符串长度字节
   - 这虽然低效，但为兼容性而保留
   - 以长度字节为准；分隔符是必需的，但属于冗余

2. **字符支持：**
   - 尽管文档中另有说明，字符串内的 `=` 和 `;` 确实受到支持（由长度字节处理）
   - UTF-8 编码支持完整的 Unicode
   - **警告：**I2CP 使用 UTF-8，但 I2NP 在历史上并未正确处理 UTF-8
   - 为获得最大兼容性，在可能情况下对 I2NP 映射使用 ASCII

3. **特殊上下文：**
   - **RouterInfo/RouterAddress：** 必须排序，不得重复
   - **I2CP SessionConfig：** 必须排序，不得重复  
   - **应用映射：** 建议排序，但并非总是必须

**示例（RouterInfo（路由器信息）选项）：**

```
Mapping size: 45 bytes
Sorted entries:
  caps=L       (capabilities)
  netId=2      (network ID)
  router.version=0.9.67
```
**JavaDoc：** [DataHelper](http://docs.i2p-projekt.de/javadoc/net/i2p/data/DataHelper.html)

---

## 通用结构规范

### 密钥与证书

**Description:** 组合了加密密钥、签名密钥和证书的基础结构。可同时用作 RouterIdentity（路由标识）和 Destination（目的地）。

**结构：**

```
+----+----+----+----+----+----+----+----+
| public_key                            |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| padding (optional)                    |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signing_key                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| certificate                           |
+----+----+----+-//

public_key :: PublicKey (partial or full)
              Default: 256 bytes (ElGamal)
              Other sizes: As specified in Key Certificate

padding :: Random data
           Length: 0 bytes or as needed
           CONSTRAINT: public_key + padding + signing_key = 384 bytes

signing_key :: SigningPublicKey (partial or full)
               Default: 128 bytes (DSA_SHA1)
               Other sizes: As specified in Key Certificate

certificate :: Certificate
               Minimum: 3 bytes (NULL certificate)
               Common: 7 bytes (Key Certificate with default keys)

TOTAL LENGTH: 387+ bytes (never assume exactly 387!)
```
**密钥对齐:** - **加密公钥:** 从开头对齐（字节 0） - **填充:** 位于中间（如有需要） - **签名公钥:** 对齐到末尾（字节 256 到字节 383） - **证书:** 从字节 384 开始

**大小计算：**

```
Total size = 384 + 3 + key_certificate_length

For NULL certificate (ElGamal + DSA_SHA1):
  Total = 384 + 3 = 387 bytes

For Key Certificate (EdDSA + X25519):
  Total = 384 + 3 + 4 = 391 bytes

For larger keys (e.g., RSA_4096):
  Total = 384 + 3 + 4 + excess_key_data_length
```
### 填充生成指南 ([Proposal 161](/zh/proposals/161-ri-dest-padding/))

**实现版本：** 0.9.57（2023年1月，发行版 2.1.0）

**背景：** - 对于非 ElGamal+DSA 密钥，填充存在于 384 字节的固定结构中 - 对于 Destination（I2P 目的地标识），自 0.6（2005 年）以来 256 字节的公钥字段一直未使用 - 填充应以便于压缩且仍然安全的方式生成

**要求:**

1. **随机数据的最低要求：**
   - 使用至少 32 字节的密码学安全随机数据
   - 这可为安全性提供足够的熵

2. **压缩策略：**
   - 在整个填充/公钥字段内重复这 32 字节
   - 诸如 I2NP Database Store、Streaming SYN（I2P Streaming 子系统中的 SYN 握手消息）、SSU2 handshake 等协议会使用压缩
   - 在不牺牲安全性的前提下可显著节省带宽

3. **示例：**

**Router 标识 (X25519 + EdDSA):**

```
Structure:
- 32 bytes X25519 public key
- 320 bytes padding (10 copies of 32-byte random data)
- 32 bytes EdDSA public key
- 7 bytes Key Certificate

Compression savings: ~288 bytes when compressed
```
**目的地 (ElGamal-unused + EdDSA):**

```
Structure:
- 256 bytes unused ElGamal field (11 copies of 32-byte random data, truncated to 256)
- 96 bytes padding (3 copies of 32-byte random data)
- 32 bytes EdDSA public key  
- 7 bytes Key Certificate

Compression savings: ~320 bytes when compressed
```
4. **为什么这可行：**
   - 完整结构的 SHA-256 哈希仍然包含全部熵
   - 网络数据库 DHT 的分布仅依赖该哈希
   - 签名密钥（32 bytes 的 EdDSA/X25519）提供 256 比特熵
   - 额外 32 字节的重复随机数据 = 总熵 512 比特
   - 对密码学强度而言绰绰有余

5. **实现说明:**
   - 必须存储并传输完整的 387+ 字节结构
   - 针对完整的未压缩结构计算 SHA-256 哈希
   - 在协议层应用压缩 (I2NP, Streaming, SSU2)
   - 与自 0.6 (2005) 起的所有版本向后兼容

**JavaDoc：** [KeysAndCert](http://docs.i2p-projekt.de/javadoc/net/i2p/data/KeysAndCert.html)

---

### RouterIdentity（Router 身份标识）

**说明：** 在 I2P 网络中唯一标识一个 router。其结构与 KeysAndCert（密钥与证书）相同。

**格式:** 请参阅上文的 KeysAndCert 结构

**当前要求（截至 0.9.58）：**

1. **强制的密钥类型：**
   - **加密：** X25519 (类型 4，32 字节)
   - **签名：** EdDSA_SHA512_Ed25519 (类型 7，32 字节)
   - **证书：** 密钥证书 (类型 5)

2. **已弃用的密钥类型：**
   - 自 0.9.58 起，ElGamal（类型 0）用于 Router 身份时已弃用
   - 自 0.9.58 起，DSA_SHA1（类型 0）用于 Router 身份时已弃用
   - 这些切勿用于新的 router

3. **典型大小：**
   - 带密钥证书的 X25519（基于 Curve25519 的密钥交换算法） + EdDSA（椭圆曲线数字签名算法的一种） = 391 字节
   - 32 字节 X25519 公钥
   - 320 字节填充（可按 [Proposal 161](/zh/proposals/161-ri-dest-padding/) 压缩）
   - 32 字节 EdDSA 公钥
   - 7 字节证书（3 字节头部 + 4 字节密钥类型）

**历史演进:** - 0.9.16 之前: 始终为 NULL 证书（ElGamal + DSA_SHA1） - 0.9.16-0.9.47: 新增 Key Certificate（密钥证书）支持 - 0.9.48+: 支持 X25519 加密密钥 - 0.9.58+: 弃用 ElGamal 和 DSA_SHA1

**网络数据库键：** - RouterInfo（路由器信息对象）以完整的 RouterIdentity（路由器身份）的 SHA-256 哈希作为键 - 哈希在完整的 391+ 字节结构上计算（包括填充）

**另见：** - 填充生成指南 ([提案 161](/zh/proposals/161-ri-dest-padding/)) - 上文的密钥证书规范

**JavaDoc 文档:** [RouterIdentity](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterIdentity.html)

---

### 目的地

**描述：** 用于安全消息传递的端点标识符。在结构上与 KeysAndCert 相同，但其使用语义不同。

**格式：** 参见上面的 KeysAndCert 结构

**与 RouterIdentity（路由标识）之间的关键区别：** - **公钥字段未使用，且可能包含随机数据** - 自 0.6 版（2005 年）起该字段一直未被使用 - 最初用于旧的 I2CP-to-I2CP 加密（已禁用） - 目前仅在已弃用的 LeaseSet（租约集）加密中作为 IV（初始化向量）使用

**当前建议：**

1. **签名密钥：**
   - **推荐：** EdDSA_SHA512_Ed25519（类型 7，32 字节）
   - 可选：用于与旧版本兼容的 ECDSA 类型
   - 避免：DSA_SHA1（已弃用，不建议使用）

2. **加密密钥：**
   - 该字段未被使用，但必须存在
   - **建议：** 根据[提案 161](/zh/proposals/161-ri-dest-padding/)填充随机数据（可压缩）
   - 大小：始终为 256 字节（ElGamal 槽位，尽管并未用于 ElGamal）

3. **证书：**
   - 用于 ElGamal + DSA_SHA1 的 NULL certificate（NULL 证书）（仅限旧版）
   - 适用于所有其他签名密钥类型的 Key Certificate（密钥证书）

**典型的现代目的地：**

```
Structure:
- 256 bytes unused field (random data, compressible)
- 96 bytes padding (random data, compressible)
- 32 bytes EdDSA signing public key
- 7 bytes Key Certificate

Total: 391 bytes
Compression savings: ~320 bytes
```
**实际用于加密的密钥：**
- Destination（目标标识）的加密密钥位于 **LeaseSet** 中，而不在 Destination 内
- LeaseSet 包含当前的加密公钥（可能为多个）
- 有关加密密钥处理，请参阅 LeaseSet2 规范

**网络数据库键：** - LeaseSet 以完整的 Destination（I2P 目标标识）的 SHA-256 哈希为键 - 哈希基于完整的 387+ 字节结构计算

**JavaDoc：** [Destination（目标地址）](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Destination.html)

---

## 网络数据库结构

### 租约

**描述：** 授权特定的 tunnel 接收发往某个 Destination（目标地址）的消息。是最初的 LeaseSet 格式（type 1）的一部分。

**格式：**

```
+----+----+----+----+----+----+----+----+
| tunnel_gw                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|     tunnel_id     |      end_date
+----+----+----+----+----+----+----+----+
                    |
+----+----+----+----+

tunnel_gw :: Hash (32 bytes)
             SHA-256 hash of the gateway RouterIdentity

tunnel_id :: TunnelId (4 bytes)
             Tunnel identifier at the gateway router

end_date :: Date (8 bytes)
            Expiration timestamp in milliseconds since epoch
```
**总大小：** 44 字节

**用法：** - 仅用于原始 LeaseSet（I2P 中的租约集合）（类型 1，已弃用） - 对于 LeaseSet2 及后续变体，请改用 Lease2

**JavaDoc：** [Lease（租约）](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Lease.html)

---

### LeaseSet (类型 1)

**描述：** 原始的 LeaseSet 格式。包含某个 Destination（I2P 目的地）的授权 tunnels 和密钥。存储在网络数据库中。**状态：已弃用**（请改用 LeaseSet2）。

**结构:**

```
+----+----+----+----+----+----+----+----+
| destination                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| encryption_key                        |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signing_key                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| num| Lease 0                          |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Lease 1                               |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Lease ($num-1)                        |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

destination :: Destination
               Length: 387+ bytes

encryption_key :: PublicKey (256 bytes, ElGamal)
                  Used for end-to-end ElGamal/AES+SessionTag encryption
                  Generated anew at each router startup (not persistent)

signing_key :: SigningPublicKey (128+ bytes)
               Same type as Destination signing key
               Used for LeaseSet revocation (unimplemented)
               Generated anew at each router startup (not persistent)

num :: Integer (1 byte)
       Number of Leases to follow
       Range: 0-16

leases :: Array of Lease structures
          Length: $num × 44 bytes
          Each Lease is 44 bytes

signature :: Signature (40+ bytes)
             Length determined by Destination signing key type
             Signed by Destination's SigningPrivateKey
```
**数据库存储:** - **数据库类型:** 1 - **键:** Destination（目标标识）的 SHA-256 哈希 - **值:** 完整的 LeaseSet 结构

**重要说明：**

1. **Destination（目标地址）公钥未使用：**
   - Destination 中的加密公钥字段未被使用
   - LeaseSet 中的加密密钥才是实际的加密密钥

2. **临时密钥:**
   - `encryption_key` 是临时的 (在 router 启动时重新生成)
   - `signing_key` 是临时的 (在 router 启动时重新生成)
   - 两个密钥在重启之间都不会持久保存

3. **撤销（未实现）：**
   - `signing_key` 原本用于撤销 LeaseSet
   - 撤销机制从未实现
   - Zero-lease（零租约） LeaseSet 原本用于撤销，但未被使用

4. **版本控制/时间戳:**
   - LeaseSet 没有显式的 `published` 时间戳字段
   - 版本是所有 lease（租约）中最早的到期时间
   - 新的 LeaseSet 必须具有更早的 lease 到期时间才会被接受

5. **Lease（租约）到期信息发布:**
   - Pre-0.9.7: 所有已发布的 lease 采用相同的到期时间（取最早）
   - 0.9.7+: 发布各个 lease 的实际到期时间
   - 这是实现细节，不属于规范的一部分

6. **零个 Lease:**
   - 在技术上允许具有零个 Lease（租约）的 LeaseSet（租约集合）
   - 用于撤销（尚未实现）
   - 在实践中未使用
   - LeaseSet2 变体至少需要一个 Lease

**弃用：** LeaseSet 类型 1 已被弃用。新的实现应当使用 **LeaseSet2 (类型 3)**，它提供： - 发布时间戳字段（更好的版本控制） - 支持多个加密密钥 - 离线签名能力 - 4 字节的租约到期时间（相对于 8 字节） - 更灵活的选项

**JavaDoc：** [LeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/LeaseSet.html)

---

## LeaseSet 变体

### Lease2

**描述：** 采用 4 字节过期时间的改进租约格式。用于 LeaseSet2（类型 3）和 MetaLeaseSet（类型 7）。

**简介：** 版本 0.9.38 (参见 [提案 123](/proposals/123-new-netdb-entries/))

**格式：**

```
+----+----+----+----+----+----+----+----+
| tunnel_gw                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|     tunnel_id     |      end_date     |
+----+----+----+----+----+----+----+----+

tunnel_gw :: Hash (32 bytes)
             SHA-256 hash of gateway RouterIdentity

tunnel_id :: TunnelId (4 bytes)
             Tunnel identifier at gateway

end_date :: 4-byte timestamp (seconds since epoch)
            Rolls over in year 2106
```
**总大小：** 40 字节 (比原始的 Lease 小 4 字节)

**与原始租约的比较：**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1pxsolid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Lease (Type&nbsp;1)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Lease2 (Type&nbsp;3+)</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Size</td><td style="border:1px solid var(--color-border); padding:0.5rem;">44 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Expiration Size</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes (ms)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes (seconds)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Precision</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Millisecond</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Second</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Rollover</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Year&nbsp;292,277,026,596</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Year&nbsp;2106</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Used In</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet (deprecated)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2, MetaLeaseSet</td></tr>
  </tbody>
</table>
**JavaDoc 文档：** [Lease2](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Lease2.html)

---

### 离线签名

**说明：** 一种可选结构，用于预先签名的临时密钥，使得在无需在线访问 Destination（I2P 的目标标识）的私有签名密钥的情况下也可发布 LeaseSet。

**简介:** 版本 0.9.38 (参见 [提案 123](/proposals/123-new-netdb-entries/))

**格式：**

```
+----+----+----+----+----+----+----+----+
|     expires       | sigtype |         |
+----+----+----+----+----+----+         +
|       transient_public_key            |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|           signature                   |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

expires :: 4-byte timestamp (seconds since epoch)
           Expiration of transient key validity
           Rolls over in year 2106

sigtype :: 2-byte signature type
           Type of transient_public_key (see SigningPublicKey types)

transient_public_key :: SigningPublicKey
                        Length determined by sigtype
                        Temporary signing key for LeaseSet

signature :: Signature
             Length determined by Destination's signing key type
             Signature of (expires || sigtype || transient_public_key)
             Signed by Destination's permanent SigningPrivateKey
```
**目的：** - 支持离线生成 LeaseSet - 保护 Destination（I2P 的地址标识）主密钥免于在线暴露 - 可通过发布不带离线签名的新 LeaseSet 来撤销临时密钥

**使用场景:**

1. **高安全性目标地址：**
   - 主签名密钥离线存储（硬件安全模块 HSM、冷存储）
   - 临时密钥离线生成，仅在限定时间段内使用
   - 即使临时密钥被攻破也不会泄露主密钥

2. **加密的 LeaseSet 发布：**
   - EncryptedLeaseSet 可以包含离线签名
   - 盲化公钥（blinded public key）+ 离线签名可提供额外的安全性

**安全注意事项：**

1. **有效期管理:**
   - 设置合理的有效期 (以天到数周为宜，而不是数年)
   - 在到期前生成新的临时密钥
   - 更短的有效期 = 更高的安全性，但需要更多维护

2. **密钥生成:**
   - 在安全环境中离线生成临时密钥
   - 使用主密钥离线签名
   - 仅将已签名的临时密钥 + 签名传输到在线 router

3. **撤销：**
   - 发布新的 LeaseSet，且不带离线签名，以隐式撤销
   - 或者发布使用不同临时密钥的新 LeaseSet

**签名验证：**

```
Data to sign: expires (4 bytes) || sigtype (2 bytes) || transient_public_key

Verification:
1. Extract Destination from LeaseSet
2. Get Destination's SigningPublicKey
3. Verify signature over (expires || sigtype || transient_public_key)
4. Check that current time < expires
5. If valid, use transient_public_key to verify LeaseSet signature
```
**实现说明：** - 总大小取决于 sigtype 和 Destination（I2P 目标标识）的签名密钥类型 - 最小大小：4 + 2 + 32 (EdDSA 密钥) + 64 (EdDSA 签名) = 102 字节 - 最大实用大小：~600 字节 (RSA-4096 临时密钥 + RSA-4096 签名)

**兼容性：** - LeaseSet2 (类型 3) - EncryptedLeaseSet (类型 5) - MetaLeaseSet (类型 7)

**另请参阅：** [提案 123](/proposals/123-new-netdb-entries/)，了解离线签名协议的详细说明。

---

### LeaseSet2Header（LeaseSet2 头部）

**说明：** 通用头部结构，适用于 LeaseSet2（类型 3）和 MetaLeaseSet（类型 7）。

**简介：** 版本 0.9.38（参见 [提案 123](/proposals/123-new-netdb-entries/)）

**格式：**

```
+----+----+----+----+----+----+----+----+
| destination                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|     published     | expires |  flags  |
+----+----+----+----+----+----+----+----+
| offline_signature (optional)          |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

destination :: Destination
               Length: 387+ bytes

published :: 4-byte timestamp (seconds since epoch)
             Publication time of this LeaseSet
             Rolls over in year 2106

expires :: 2-byte offset (seconds)
           Offset from published timestamp
           Maximum: 65535 seconds (18.2 hours)

flags :: 2 bytes (bit flags)
         See flag definitions below

offline_signature :: OfflineSignature (optional)
                     Present only if flags bit 0 is set
                     Variable length
```
**最小总大小：** 395 字节（不含离线签名）

**标志位定义 (位顺序: 15 14 ... 3 2 1 0):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Bit</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline Keys</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0 = No offline keys, 1 = Offline signature present</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unpublished</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0 = Standard published, 1 = Unpublished (client-side only)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0 = Standard, 1 = Will be blinded when published</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3-15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Must be 0 for compatibility</td></tr>
  </tbody>
</table>
**标志详细信息:**

**位 0 - 离线密钥:** - `0`: 无离线签名，使用 Destination（目的地）的签名密钥验证 LeaseSet 签名 - `1`: OfflineSignature 结构紧随 flags 字段之后

**第 1 位 - 未发布：** - `0`: 标准的已发布 LeaseSet，应当被洪泛到 floodfills - `1`: 未发布的 LeaseSet（仅限客户端）   - 不应被洪泛、不应发布，也不应在响应查询时发送   - 如果过期，不要向 netdb 查询替代项（除非第 2 位也被设置）   - 用于本地 tunnels 或测试

**位 2 - 盲化 (自 0.9.42 起):** - `0`: 标准 LeaseSet - `1`: 此未加密的 LeaseSet 在发布时将被盲化并加密   - 发布的版本将为 EncryptedLeaseSet（加密的 LeaseSet） (type 5)   - 如果过期，请在 netdb 中查询**盲化位置**以进行替换   - 还必须将位 1 设为 1（未发布 + 盲化）   - 用于加密的隐藏服务

**过期限制：**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">LeaseSet Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Maximum Expires Value</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Maximum Actual Time</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2 (type 3)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈660 seconds</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈11 minutes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MetaLeaseSet (type 7)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">65,535 seconds</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈18.2 hours</td></tr>
  </tbody>
</table>
**发布时间戳要求：**

LeaseSet（租约集合）（类型 1）没有 published 字段，因此在进行版本化时需要搜索最早的租约到期时间。LeaseSet2 增加了显式的 `published` 时间戳，精度为 1 秒。

**关键实现注意事项：** - Routers 必须将 LeaseSet 的发布速率限制为每个 Destination（I2P 目的地）**远低于每秒一次** - 如果发布更快，确保每个新的 LeaseSet 的 `published` 时间至少晚 1 秒 - 如果 `published` 时间不比当前版本更新，Floodfills 将拒绝该 LeaseSet - 建议的最小间隔：两次发布之间为 10-60 秒

**计算示例：**

**LeaseSet2 (最长 11 分钟):**

```
published = 1704067200 (2024-01-01 00:00:00 UTC)
expires = 660 (seconds)
Actual expiration = 1704067200 + 660 = 1704067860 (2024-01-01 00:11:00 UTC)
```
**MetaLeaseSet (最长 18.2 小时):**

```
published = 1704067200 (2024-01-01 00:00:00 UTC)
expires = 65535 (seconds)
Actual expiration = 1704067200 + 65535 = 1704132735 (2024-01-01 18:12:15 UTC)
```
**版本管理：** - 如果 `published` 时间戳更大，则将该 LeaseSet（租约集合）视为“更新的” - Floodfills 仅存储并对最新版本进行泛洪 - 当最旧的 Lease（租约）与先前 LeaseSet 的最旧 Lease 相匹配时需注意

---

### LeaseSet2 (类型 3)

**说明：** 现代的 LeaseSet 格式，支持多个加密密钥、离线签名和服务记录。是 I2P 隐藏服务的现行标准。

**简介：** 版本 0.9.38（参见 [提案 123](/proposals/123-new-netdb-entries/)）

**结构：**

```
+----+----+----+----+----+----+----+----+
|         ls2_header                    |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|          options                      |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|numk| keytype0| keylen0 |              |
+----+----+----+----+----+              +
|          encryption_key_0             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| keytypen| keylenn |                   |
+----+----+----+----+                   +
|          encryption_key_n             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| num| Lease2 0                         |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Lease2($num-1)                        |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

ls2header :: LeaseSet2Header
             Length: 395+ bytes (varies with offline signature)

options :: Mapping
           Key-value pairs for service records and metadata
           Length: 2+ bytes (size field + data)

numk :: Integer (1 byte)
        Number of encryption keys
        Range: 1 to (implementation-defined maximum, typically 8)

keytype :: 2-byte encryption type
           See PublicKey type table

keylen :: 2-byte key length
          Must match keytype specification

encryption_key :: PublicKey
                  Length: keylen bytes
                  Type: keytype

[Repeat keytype/keylen/encryption_key for each key]

num :: Integer (1 byte)
       Number of Lease2s
       Range: 1-16 (at least one required)

leases :: Array of Lease2 structures
          Length: $num × 40 bytes

signature :: Signature
             Length determined by signing key type
             Signed over entire structure including database type prefix
```
**数据库存储:** - **数据库类型:** 3 - **键:** Destination（目标标识）的 SHA-256 哈希值 - **值:** 完整的 LeaseSet2 结构

**签名计算：**

```
Data to sign: database_type (1 byte, value=3) || complete LeaseSet2 data

Verification:
1. Prepend database type byte (0x03) to LeaseSet2 data
2. If offline signature present:
   - Verify offline signature against Destination key
   - Verify LeaseSet2 signature against transient key
3. Else:
   - Verify LeaseSet2 signature against Destination key
```
### 加密密钥偏好顺序

**针对已发布 (服务器端) LeaseSet (租约集):** - 按服务器偏好顺序列出密钥 (最优先的在前) - 支持多种类型的客户端应当遵循服务器的偏好 - 从列表中选择第一个受支持的类型 - 一般而言, 编号更高 (较新) 的密钥类型更安全/更高效 - 建议的顺序: 按类型代码的逆序列出密钥 (最新的在前)

**示例服务器首选项：**

```
numk = 2
Key 0: X25519 (type 4, 32 bytes)         [Most preferred]
Key 1: ElGamal (type 0, 256 bytes)       [Legacy compatibility]
```
**对于未发布（客户端）LeaseSet：** - 密钥顺序基本无关紧要（很少会向客户端发起连接） - 为保持一致性，遵循相同的约定

**客户端密钥选择：** - 遵循服务器偏好（选择第一个受支持的类型） - 或使用由实现定义的偏好 - 或基于双方的能力确定综合偏好

### 选项映射

**要求：** - 选项必须按键排序（字典序，UTF-8 字节顺序） - 排序确保签名不变 - 不允许重复键

**标准格式（[提案 167](/proposals/167-service-records/)）：**

自 API 0.9.66（2025 年 6 月，发行版 2.9.0）起，服务记录选项采用标准化格式。完整规范参见[提案 167](/proposals/167-service-records/)。

**服务记录选项格式：**

```
Key: _service._proto
Value: record_type ttl [priority weight] port target [appoptions]

service :: Symbolic name of service (lowercase, [a-z0-9-])
           Examples: smtp, http, irc, mumble
           Use standard identifiers from IANA Service Name Registry
           or Linux /etc/services when available

proto :: Transport protocol (lowercase, [a-z0-9-])
         "tcp" = streaming protocol
         "udp" = repliable datagrams
         Protocol indicators for raw datagrams may be defined later

record_type :: "0" (self-reference) or "1" (SRV record)

ttl :: Time to live in seconds (positive integer)
       Recommended minimum: 86400 (one day)
       Prevents frequent re-queries

For record_type = 0 (self-reference):
  port :: I2CP port number (non-negative integer)
  appoptions :: Optional application-specific data (no spaces or commas)

For record_type = 1 (SRV record):
  priority :: Lower value = more preferred (non-negative integer)
  weight :: Relative weight for same priority, higher = more likely (non-negative)
  port :: I2CP port number (non-negative integer)
  target :: Hostname or b32 of destination (lowercase)
            Format: "example.i2p" or "aaaaa...aaaa.b32.i2p"
            Recommend b32 unless hostname is "well known"
  appoptions :: Optional application-specific data (no spaces or commas)
```
**示例服务记录：**

**1. 自引用型 SMTP 服务器：**

```
Destination: aaaa...aaaa.b32.i2p (this LeaseSet)
Option: "_smtp._tcp" = "0 999999 25"

Meaning: This destination provides SMTP service on I2CP port 25
```
**2. 单一外部 SMTP 服务器：**

```
Destination: aaaa...aaaa.b32.i2p (this LeaseSet)
Option: "_smtp._tcp" = "1 86400 0 0 25 bbbb...bbbb.b32.i2p"

Meaning: SMTP service provided by bbbb...bbbb on port 25
         TTL = 1 day, single server (priority=0, weight=0)
```
**3. 多个 SMTP 服务器（负载均衡）：**

```
Destination: aaaa...aaaa.b32.i2p (this LeaseSet)
Option: "_smtp._tcp" = "1 86400 0 0 25 bbbb...bbbb.b32.i2p,1 86400 1 0 25 cccc...cccc.b32.i2p"

Meaning: Two SMTP servers
         bbbb...bbbb (priority=0, preferred)
         cccc...cccc (priority=1, backup)
```
**4. 带有应用选项的 HTTP 服务：**

```
Option: "_http._tcp" = "0 86400 80 tls=1.3;cert=ed25519"

Meaning: HTTP on port 80 with TLS 1.3 and EdDSA certificates
```
**TTL 建议:** - 最小值: 86400 秒 (1 天) - 更长的 TTL 可降低 netdb 查询负载 - 在查询减少与服务更新传播之间取得平衡 - 对于稳定的服务: 604800 (7 天) 或更长

**实现说明：**

1. **加密密钥（截至 0.9.44）：**
   - ElGamal（类型 0，256 字节）：向后兼容
   - X25519（类型 4，32 字节）：当前标准
   - MLKEM（基于模格的密钥封装机制）变体：后量子（测试版，未最终定稿）

2. **密钥长度验证:**
   - floodfill 与客户端必须能够解析未知的密钥类型
   - 使用 keylen 字段跳过未知密钥
   - 不要因密钥类型未知而导致解析失败

3. **发布时间戳：**
   - 参见 LeaseSet2Header（LeaseSet v2 头部）关于速率限制的说明
   - 两次发布之间的最小间隔为 1 秒
   - 建议：两次发布之间间隔 10-60 秒

4. **加密类型迁移:**
   - 通过多密钥支持实现渐进式迁移
   - 在过渡期同时列出旧密钥和新密钥
   - 在给予客户端足够的升级周期后移除旧密钥

**JavaDoc：** [LeaseSet2](http://docs.i2p-projekt.de/javadoc/net/i2p/data/LeaseSet2.html)

---

### MetaLease（元租约）

**说明：** 用于 MetaLeaseSet（元 LeaseSet）的 Lease（租约）结构，可引用其他 LeaseSets，而非引用 tunnels。用于负载均衡和冗余。

**简介：** 版本 0.9.38，计划在 0.9.40 中投入使用（参见 [Proposal 123](/proposals/123-new-netdb-entries/)）

**格式：**

```
+----+----+----+----+----+----+----+----+
| tunnel_gw                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|    flags     |cost|      end_date     |
+----+----+----+----+----+----+----+----+

tunnel_gw :: Hash (32 bytes)
             SHA-256 hash of:
             - Gateway RouterIdentity (for type 1), OR
             - Another MetaLeaseSet destination (for type 3/5/7)

flags :: 3 bytes
         Bit order: 23 22 ... 3 2 1 0
         Bits 3-0: Entry type (see table below)
         Bits 23-4: Reserved (must be 0)

cost :: 1 byte (0-255)
        Lower value = higher priority
        Used for load balancing

end_date :: 4-byte timestamp (seconds since epoch)
            Expiration time
            Rolls over in year 2106
```
**总大小：** 40 字节

**条目类型（标志位 3-0）：**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Unknown</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unknown/invalid entry</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Points to LeaseSet (type 1, deprecated)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Points to LeaseSet2 (type 3)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Points to EncryptedLeaseSet (type 5)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MetaLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align-center?">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Points to another MetaLeaseSet (type 7)</td></tr>
  </tbody>
</table>
**使用场景：**

1. **负载均衡：**
   - MetaLeaseSet（元租约集）包含多个 MetaLease（元租约）条目
   - 每个条目都指向不同的 LeaseSet2
   - 客户端根据 cost 字段进行选择

2. **冗余：**
   - 多个条目指向备用 LeaseSets
   - 如果主 LeaseSet 不可用则回退

3. **服务迁移:**
   - MetaLeaseSet（元 LeaseSet）指向新的 LeaseSet
   - 允许在不同的 Destinations（I2P 目的地）之间平滑过渡

**成本字段用法：** - 成本越低 = 优先级越高 - 成本为 0 = 最高优先级 - 成本为 255 = 最低优先级 - 客户端应当（SHOULD）优先选择较低成本的条目 - 成本相同的条目可以随机进行负载均衡

**与 Lease2 的比较：**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Lease2</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">MetaLease</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Size</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Tunnel ID</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Replaced by flags (3 bytes) + cost (1 byte)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Points To</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specific tunnel</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet or MetaLeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Usage</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Direct tunnel reference</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Indirection/load balancing</td></tr>
  </tbody>
</table>
**JavaDoc:** [MetaLease](http://docs.i2p-projekt.de/javadoc/net/i2p/data/MetaLease.html)

---

### MetaLeaseSet (元租约集) (类型 7)

**描述：** 包含 MetaLease（元租约）条目的 LeaseSet 变体，提供对其他 LeaseSets 的间接引用。用于负载均衡、冗余和服务迁移。

**简介：** 在 0.9.38 中定义，计划在 0.9.40 中投入使用 (参见 [提案 123](/proposals/123-new-netdb-entries/))

**状态:** 规范已完成。应使用当前 I2P 发行版验证生产部署状态。

**结构：**

```
+----+----+----+----+----+----+----+----+
|         ls2_header                    |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|          options                      |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| num| MetaLease 0                      |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| MetaLease($num-1)                     |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|numr|                                  |
+----+                                  +
|          revocation_0                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|          revocation_n                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

ls2header :: LeaseSet2Header
             Length: 395+ bytes

options :: Mapping
           Length: 2+ bytes (size + data)
           MUST be sorted by key

num :: Integer (1 byte)
       Number of MetaLease entries
       Range: 1 to (implementation-defined, recommend 1-16)

metaleases :: Array of MetaLease structures
              Length: $num × 40 bytes

numr :: Integer (1 byte)
        Number of revocation hashes
        Range: 0 to (implementation-defined, recommend 0-16)

revocations :: Array of Hash structures
               Length: $numr × 32 bytes
               SHA-256 hashes of revoked LeaseSet Destinations
```
**数据库存储：** - **数据库类型：** 7 - **键：** Destination（I2P 的目标地址）的 SHA-256 哈希 - **值：** 完整的 MetaLeaseSet（I2P 中的 leaseSet 元集合）结构

**签名计算：**

```
Data to sign: database_type (1 byte, value=7) || complete MetaLeaseSet data

Verification:
1. Prepend database type byte (0x07) to MetaLeaseSet data
2. If offline signature present in header:
   - Verify offline signature against Destination key
   - Verify MetaLeaseSet signature against transient key
3. Else:
   - Verify MetaLeaseSet signature against Destination key
```
**使用场景：**

**1. 负载均衡:**

```
MetaLeaseSet for primary.i2p:
  MetaLease 0: cost=0, points to server1.i2p LeaseSet2
  MetaLease 1: cost=0, points to server2.i2p LeaseSet2
  MetaLease 2: cost=0, points to server3.i2p LeaseSet2

Clients randomly select among equal-cost entries
```
**2. 故障切换:**

```
MetaLeaseSet for service.i2p:
  MetaLease 0: cost=0, points to primary.i2p LeaseSet2
  MetaLease 1: cost=100, points to backup.i2p LeaseSet2

Clients prefer cost=0 (primary), fall back to cost=100 (backup)
```
**3. 服务迁移：**

```
MetaLeaseSet for old-domain.i2p:
  MetaLease 0: cost=0, points to new-domain.i2p LeaseSet2

Transparently redirects clients from old to new destination
```
**4. 多层架构：**

```
MetaLeaseSet for service.i2p:
  MetaLease 0: cost=0, points to region1-meta.i2p (another MetaLeaseSet)
  MetaLease 1: cost=0, points to region2-meta.i2p (another MetaLeaseSet)

Each region MetaLeaseSet points to regional servers
Allows hierarchical load balancing
```
**撤销列表：**

撤销列表允许 MetaLeaseSet 明确撤销先前发布的 LeaseSets：

- **用途:** 将特定的 Destination（I2P 的地址标识）标记为不再有效
- **内容:** 已吊销的 Destination 结构的 SHA-256 哈希
- **用法:** 客户端不得使用其 Destination 哈希出现在吊销列表中的 LeaseSets
- **典型值:** 在大多数部署中为空（numr=0）

**撤销示例:**

```
Service migrates from dest-v1.i2p to dest-v2.i2p:
  MetaLease 0: points to dest-v2.i2p
  Revocations: [hash(dest-v1.i2p)]

Clients will use v2 and ignore v1 even if cached
```
**过期处理：**

MetaLeaseSet（元 LeaseSet）使用 LeaseSet2Header（LeaseSet2 的头部），其 expires 最大为 65535 秒（约 18.2 小时）：

- 比 LeaseSet2 长得多（最长约 11 分钟）
- 适用于相对静态的间接引用
- 被引用的 LeaseSets 可以有更短的到期时间
- 客户端必须同时检查 MetaLeaseSet 和被引用的 LeaseSets 的到期时间

**选项映射:**

- 使用与 LeaseSet2 选项相同的格式
- 可以包含服务记录（[提案 167](/proposals/167-service-records/)）
- 必须按键排序
- 服务记录通常描述最终的目标服务，而不是间接结构

**客户端实现注意事项：**

1. **解析流程：**
   ```
   1. Query netdb for MetaLeaseSet using SHA-256(Destination)
   2. Parse MetaLeaseSet, extract MetaLease entries
   3. Sort entries by cost (lower = better)
   4. For each entry in cost order:
      a. Extract LeaseSet hash from tunnel_gw field
      b. Determine entry type from flags
      c. Query netdb for referenced LeaseSet (may be another MetaLeaseSet)
      d. Check revocation list
      e. Check expiration
      f. If valid, use the LeaseSet; else try next entry
   ```

2. **缓存：**
   - 同时缓存 MetaLeaseSet（元租约集合）和其引用的 LeaseSets
   - 检查这两个层级的过期时间
   - 监控是否有更新的 MetaLeaseSet 发布

3. **故障切换:**
   - 如果首选条目失败，尝试成本次低的下一个条目
   - 考虑将失败的条目标记为暂时不可用
   - 定期重新检查以确认是否已恢复

**实现状态:**

[提案 123](/proposals/123-new-netdb-entries/) 指出部分内容仍处于“开发中”。实现者应当： - 在目标 I2P 版本中验证生产就绪性 - 在部署前测试对 MetaLeaseSet（I2P 中用于聚合多个 leaseSet 的元集合）的支持 - 在较新的 I2P 版本中检查是否有更新的规范

**JavaDoc:** [MetaLeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/MetaLeaseSet.html)（MetaLeaseSet：用于聚合多个 leaseSet 的元数据集合）

---

### EncryptedLeaseSet（加密的 LeaseSet，类型 5）

**描述：** 加密且盲化的 LeaseSet，用于增强隐私。仅盲化的公钥和元数据可见；实际的租约和加密密钥均被加密。

**简介：** 在 0.9.38 中定义，自 0.9.39 起可用（参见 [提案 123](/proposals/123-new-netdb-entries/)）

**结构：**

```
+----+----+----+----+----+----+----+----+
| sigtype |                             |
+----+----+                             +
|        blinded_public_key             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|     published     | expires |  flags  |
+----+----+----+----+----+----+----+----+
| offline_signature (optional)          |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|  len    |                             |
+----+----+                             +
|         encrypted_data                |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

sigtype :: 2-byte signature type
           Type of blinded_public_key
           MUST be RedDSA_SHA512_Ed25519 (type 11)

blinded_public_key :: SigningPublicKey (32 bytes for RedDSA)
                      Blinded version of Destination signing key
                      Used to verify signature on EncryptedLeaseSet

published :: 4-byte timestamp (seconds since epoch)
             Publication time
             Rolls over in year 2106

expires :: 2-byte offset (seconds)
           Offset from published
           Maximum: 65535 seconds (18.2 hours)
           Practical maximum for LeaseSet data: ~660 seconds (~11 min)

flags :: 2 bytes
         Bit 0: Offline signature present (0=no, 1=yes)
         Bit 1: Unpublished (0=published, 1=client-side only)
         Bits 15-2: Reserved (must be 0)

offline_signature :: OfflineSignature (optional)
                     Present only if flags bit 0 = 1
                     Variable length

len :: 2-byte integer
       Length of encrypted_data
       Range: 1 to 65535

encrypted_data :: Encrypted payload
                  Length: len bytes
                  Contains encrypted LeaseSet2 or MetaLeaseSet

signature :: Signature (64 bytes for RedDSA)
             Length determined by sigtype
             Signed by blinded_public_key or transient key
```
**数据库存储:** - **数据库类型:** 5 - **键:** 对 **blinded Destination** (经盲化的 Destination) 的 SHA-256 哈希 (非原始的 Destination) - **值:** 完整的 EncryptedLeaseSet (加密的 leaseSet) 结构

**与 LeaseSet2 的关键差异：**

1. **不使用 LeaseSet2Header 结构**（字段相似，但布局不同）
2. **盲化的公钥**，而不是完整的 Destination（目标标识）
3. **加密的有效载荷**，而非明文的租约和密钥
4. **数据库键为盲化 Destination 的哈希**，而不是原始的 Destination

**签名计算：**

```
Data to sign: database_type (1 byte, value=5) || complete EncryptedLeaseSet data

Verification:
1. Prepend database type byte (0x05) to EncryptedLeaseSet data
2. If offline signature present (flags bit 0 = 1):
   - Verify offline signature against blinded public key
   - Verify EncryptedLeaseSet signature against transient key
3. Else:
   - Verify EncryptedLeaseSet signature against blinded public key
```
**签名类型要求：**

**必须使用 RedDSA_SHA512_Ed25519 (类型 11)：** - 32 字节的盲化公钥 - 64 字节的签名 - 为实现盲化的安全属性所必需 - 参见 [Red25519 规范](//docs/specs/red25519-signature-scheme/

**与 EdDSA 的关键差异：** - 通过模约简（modular reduction）得到私钥（而非 clamping（位约束）） - 签名包含 80 字节的随机数据 - 直接使用公钥（而非哈希） - 支持安全的盲化操作

**盲化与加密:**

完整详情请参见 [EncryptedLeaseSet 规范](/docs/specs/encryptedleaseset/)：

**1. 密钥盲化：**

```
Blinding process (daily rotation):
  secret = HKDF(original_signing_private_key, date_string, "i2pblinding1")
  alpha = SHA-256(secret) mod L (where L is Ed25519 group order)
  blinded_private_key = alpha * original_private_key
  blinded_public_key = alpha * original_public_key
```
**2. 数据库位置：**

```
Client publishes to:
  Key = SHA-256(blinded_destination)
  
Where blinded_destination uses:
  - Blinded public key (signing key)
  - Same unused public key field (random)
  - Same certificate structure
```
**3. 加密层（三层）：**

**第 1 层 - 认证层（客户端访问）：** - 加密：ChaCha20 流密码 - 密钥派生：HKDF（使用每个客户端的机密） - 已认证的客户端可以解密外层

**第2层 - 加密层:** - 加密算法：ChaCha20 - 密钥：由客户端与服务器之间的 DH（Diffie-Hellman 密钥交换）导出 - 包含实际的 LeaseSet2 或 MetaLeaseSet

**第 3 层 - 内部 LeaseSet:** - 完整的 LeaseSet2 或 MetaLeaseSet - 包含所有 tunnels、加密密钥、选项 - 仅在成功解密后可访问

**加密密钥派生:**

```
Client has: ephemeral_client_private_key
Server has: ephemeral_server_public_key (in encrypted_data)

Shared secret = X25519(client_private, server_public)
Encryption key = HKDF(shared_secret, context_info, "i2pblinding2")
```
**发现过程：**

**适用于已授权的客户端：**

```
1. Client knows original Destination
2. Client computes current blinded Destination (based on current date)
3. Client computes database key: SHA-256(blinded_destination)
4. Client queries netdb for EncryptedLeaseSet using blinded key
5. Client decrypts layer 1 using authorization credentials
6. Client decrypts layer 2 using DH shared secret
7. Client extracts inner LeaseSet2/MetaLeaseSet
8. Client uses tunnels from inner LeaseSet for communication
```
**对于未授权的客户端：** - 即使找到 EncryptedLeaseSet（加密的 leaseSet），也无法解密 - 无法从盲化版本确定原始 Destination（目标地址） - 无法在不同的盲化周期（每日轮换）之间关联 EncryptedLeaseSets

**过期时间：**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Content Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Maximum Expires</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet (outer)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">65,535 sec (≈18.2 hr)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Full 2-byte expires field</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Inner LeaseSet2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈660 sec (≈11 min)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Actual lease data practical maximum</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Inner MetaLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">65,535 sec (≈18.2 hr)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Indirection can be longer-lived</td></tr>
  </tbody>
</table>
**发布时间：**

与 LeaseSet2Header 的要求相同：
- 每次发布之间必须至少增加 1 秒
- 如果不比当前版本新，Floodfills 将拒绝
- 建议：每次发布之间间隔 10-60 秒

**使用加密 LeaseSets 的离线签名：**

使用离线签名时的特别注意事项： - 盲化公钥每日轮换 - 离线签名必须每日使用新的盲化密钥重新生成 - 或者将离线签名用于内部 LeaseSet，而不是外层 EncryptedLeaseSet（加密的 LeaseSet） - 参见 [Proposal 123](/proposals/123-new-netdb-entries/) 的说明

**实现说明：**

1. **客户端授权:**
   - 可为多个客户端使用不同的密钥进行授权
   - 每个获授权的客户端都拥有唯一的解密凭据
   - 通过更改授权密钥撤销客户端的授权

2. **每日密钥轮换：**
   - 盲化密钥在 UTC 午夜轮换
   - 客户端必须每天重新计算盲化 Destination（目标标识）
   - 旧的 EncryptedLeaseSets 在轮换后将无法被发现

3. **隐私属性:**
   - Floodfills（floodfill 路由）无法确定原始 Destination（目的地标识）
   - 未授权的客户端无法访问该服务
   - 不同的 blinding periods（盲化周期）之间无法关联
   - 除了到期时间之外没有明文元数据

4. **性能：**
   - 客户端必须执行每日盲化计算
   - 三层加密会增加计算开销
   - 考虑缓存已解密的内部 LeaseSet（租约集）

**安全注意事项：**

1. **授权密钥管理:**
   - 安全分发客户端授权凭据
   - 为每个客户端使用唯一凭据，以实现细粒度撤销
   - 定期轮换授权密钥

2. **时钟同步:**
   - 每日 blinding（盲化）依赖于同步的 UTC 日期
   - 时钟偏移可能导致查询失败
   - 考虑为容差支持前一天/后一天的 blinding

3. **元数据泄露：**
   - Published 和 expires 字段是明文
   - 模式分析可能会揭示服务特征
   - 如果担心，可将发布间隔随机化

**JavaDoc：** [EncryptedLeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/EncryptedLeaseSet.html)

---

## Router 结构

### RouterAddress（router 地址）

**描述：** 定义通过特定传输协议与 router 建立连接所需的信息。

**格式:**

```
+----+----+----+----+----+----+----+----+
|cost|           expiration
+----+----+----+----+----+----+----+----+
     |        transport_style           |
+----+----+----+----+-//-+----+----+----+
|                                       |
+                                       +
|               options                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

cost :: Integer (1 byte)
        Relative cost, 0=free, 255=expensive
        Typical values:
          5-6: SSU2
          10-11: NTCP2

expiration :: Date (8 bytes)
              MUST BE ALL ZEROS (see critical note below)

transport_style :: String (1-256 bytes)
                   Transport protocol name
                   Current values: "SSU2", "NTCP2"
                   Legacy: "SSU", "NTCP" (removed)

options :: Mapping
           Transport-specific configuration
           Common options: "host", "port"
           Transport-specific options vary
```
**严重 - Expiration 字段:**

⚠️ **过期字段必须设置为全零（8个零字节）。**

- **原因：** 自 0.9.3 版本起，非零的到期时间会导致签名验证失败
- **历史：** 到期时间字段最初未被使用，始终为 null
- **当前状态：** 自 0.9.12 起该字段再次被识别，但必须等待网络升级
- **实现：** 始终设置为 0x0000000000000000

任何非零的过期值都会导致 RouterInfo（I2P router 的信息记录）签名验证失败。

### 传输协议

**当前协议（截至 2.10.0）：**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Introduced</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Removed</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>SSU2</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.54 (May 2022)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Default since 0.9.56</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>NTCP2</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.36 (Aug 2018)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.50 (May 2021)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Use NTCP2</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2.4.0 (Dec 2023)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Use SSU2</td></tr>
  </tbody>
</table>
**传输样式取值:** - `"SSU2"`: 当前基于 UDP 的传输方式 - `"NTCP2"`: 当前基于 TCP 的传输方式 - `"NTCP"`: 遗留，已移除（请勿使用） - `"SSU"`: 遗留，已移除（请勿使用）

### 通用选项

所有传输方式通常包括：

```
"host" = IPv4 or IPv6 address or hostname
"port" = Port number (1-65535)
```
### SSU2 特定选项

完整细节请参见 [SSU2 规范](/docs/specs/ssu2/)。

**必需选项：**

```
"host" = IP address (IPv4 or IPv6)
"port" = UDP port number
"s" = Static X25519 public key (Base64, 44 characters = 32 bytes)
"i" = Introduction key X25519 (Base64, 44 characters = 32 bytes)
"v" = "2" (protocol version)
```
**可选选项:**

```
"caps" = Capability string (e.g., "B" for bandwidth tier)
"ihost0", "ihost1", ... = Introducer IP addresses
"iport0", "iport1", ... = Introducer ports  
"ikey0", "ikey1", ... = Introducer static keys (Base64, 44 chars)
"itag0", "itag1", ... = Introducer relay tags
"iexp0", "iexp1", ... = Introducer expiration timestamps
"mtu" = Maximum transmission unit (default 1500, min 1280)
"mtu6" = IPv6 MTU (if different from IPv4)
```
**示例 SSU2 RouterAddress（路由地址）：**

```
cost: 5
expiration: 0x0000000000000000
transport_style: "SSU2"
options:
  host=198.51.100.42
  port=12345
  s=SGVsbG8gV29ybGQhIFRoaXMgaXMgYSBzYW1wbGUga2V5IQ==
  i=QW5vdGhlciBTYW1wbGUgS2V5IGZvciBJbnRyb2R1Y3Rpb24=
  v=2
  caps=BC
  mtu=1472
```
### NTCP2 特定选项

完整说明请参见 [NTCP2 规范](/docs/specs/ntcp2/)。

**必需选项:**

```
"host" = IP address (IPv4 or IPv6)
"port" = TCP port number
"s" = Static X25519 public key (Base64, 44 characters = 32 bytes)
"i" = Initialization vector (Base64, 24 characters = 16 bytes)
"v" = "2" (protocol version)
```
**可选选项（自 0.9.50 起）：**

```
"caps" = Capability string
```
**NTCP2 RouterAddress 示例:**

```
cost: 10
expiration: 0x0000000000000000
transport_style: "NTCP2"
options:
  host=198.51.100.42
  port=23456
  s=SGVsbG8gV29ybGQhIFRoaXMgaXMgYSBzYW1wbGUga2V5IQ==
  i=U2FtcGxlIElWIGhlcmU=
  v=2
```
### 实现说明

1. **成本值：**
   - UDP (SSU2) 由于效率更高，通常成本更低（5-6）
   - TCP (NTCP2) 由于开销更大，通常成本更高（10-11）
   - 成本越低 = 更优先的传输方式

2. **多个地址：**
   - Routers 可能会发布多个 RouterAddress（路由地址条目）
   - 不同的传输协议（SSU2 和 NTCP2）
   - 不同的 IP 版本（IPv4 和 IPv6）
   - 客户端会根据开销和能力进行选择

3. **主机名 vs IP:**
   - 出于性能考虑，优先使用 IP 地址
   - 支持主机名，但会增加 DNS 解析开销
   - 可考虑在已发布的 RouterInfos（I2P 路由信息条目）中使用 IP

4. **Base64 编码：**
   - 所有密钥和二进制数据均以 Base64 编码
   - 标准 Base64（RFC 4648）
   - 无填充或非标准字符

**JavaDoc：** [RouterAddress](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterAddress.html)

---

### RouterInfo（路由器信息）

**描述:** 关于 router 的完整已发布信息，存储在网络数据库中。包含身份标识、地址和能力。

**格式：**

```
+----+----+----+----+----+----+----+----+
| router_ident                          |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| published                             |
+----+----+----+----+----+----+----+----+
|size| RouterAddress 0                  |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| RouterAddress 1                       |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| RouterAddress ($size-1)               |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+-//-+----+----+----+
|psiz| options                          |
+----+----+----+----+-//-+----+----+----+
| signature                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

router_ident :: RouterIdentity
                Length: 387+ bytes (typically 391 for X25519+EdDSA)

published :: Date (8 bytes)
             Publication timestamp (milliseconds since epoch)

size :: Integer (1 byte)
        Number of RouterAddress entries
        Range: 0-255

addresses :: Array of RouterAddress
             Variable length
             Each RouterAddress has variable size

peer_size :: Integer (1 byte)
             Number of peer hashes (ALWAYS 0)
             Historical, unused feature

options :: Mapping
           Router capabilities and metadata
           MUST be sorted by key

signature :: Signature
             Length determined by router_ident signing key type
             Typically 64 bytes (EdDSA)
             Signed by router_ident's SigningPrivateKey
```
**数据库存储：** - **数据库类型：** 0 - **键：** RouterIdentity（I2P router 的身份标识）的 SHA-256 哈希 - **值：** 完整的 RouterInfo 结构（I2P router 的信息结构）

**发布时间戳:** - 8 字节日期（自 Unix 纪元以来的毫秒数） - 用于 RouterInfo（路由信息）的版本管理 - Routers（路由器）会周期性地发布新的 RouterInfo - Floodfills（floodfill 路由器）会根据发布时间戳保留最新版本

**地址排序:** - **历史:** 非常早期的 routers 要求按其数据的 SHA-256 哈希对地址进行排序 - **当前:** 不需要排序，为了兼容性而实现并不值得 - 地址可以按任意顺序

**对等体数量字段（历史）：** - **始终为 0** 在现代 I2P 中 - 原本用于受限路由（未实现） - 若实现，其后将跟随相应数量的 Router 哈希 - 某些旧实现可能要求已排序的对等体列表

**选项映射：**

选项必须按键名排序。标准选项包括：

**能力选项：**

```
"caps" = Capability string
         Common values:
           f = Floodfill (network database)
           L or M or N or O = Bandwidth tier (L=lowest, O=highest)
           R = Reachable
           U = Unreachable/firewalled
           Example: "fLRU" = Floodfill, Low bandwidth, Reachable, Unreachable
```
**网络选项：**

```
"netId" = Network ID (default "2" for main I2P network)
          Different values for test networks

"router.version" = I2P version string
                   Example: "0.9.67" or "2.10.0"
```
**统计选项：**

```
"stat_uptime" = Uptime in milliseconds
"coreVersion" = Core I2P version
"router.version" = Full router version string
```
有关标准选项的完整列表，请参阅[网络数据库 RouterInfo（路由器信息）文档](/docs/specs/common-structures/#routerInfo)。

**签名计算:**

```
Data to sign: Complete RouterInfo structure from router_ident through options

Verification:
1. Extract RouterIdentity from RouterInfo
2. Get SigningPublicKey from RouterIdentity (type determines algorithm)
3. Verify signature over all data preceding signature field
4. Signature must match signing key type and length
```
**典型的现代 RouterInfo（I2P router 信息记录）:**

```
RouterIdentity: 391 bytes (X25519+EdDSA with Key Certificate)
Published: 8 bytes
Size: 1 byte (typically 1-4 addresses)
RouterAddress × N: Variable (typically 200-500 bytes each)
Peer Size: 1 byte (value=0)
Options: Variable (typically 50-200 bytes)
Signature: 64 bytes (EdDSA)

Total: ~1000-2500 bytes typical
```
**实现说明:**

1. **多个地址:**
   - Routers 通常发布 1-4 个地址
   - IPv4 和 IPv6 变体
   - SSU2 和/或 NTCP2 传输协议
   - 每个地址相互独立

2. **版本控制：**
   - 较新的 RouterInfo（路由器信息）具有更晚的 `published` 时间戳
   - Routers（路由器）约每 2 小时或在地址更改时重新发布
   - Floodfills（泛洪节点）只存储并泛洪最新版本

3. **验证：**
   - 在接受 RouterInfo（路由信息记录）之前验证签名
   - 检查每个 RouterAddress（路由地址记录）中的过期字段是否全为零
   - 验证选项映射是否按键名排序
   - 检查证书和密钥类型是否为已知/受支持

4. **网络数据库（netDb）：**
   - Floodfills 以 Hash(RouterIdentity) 为索引存储 RouterInfo
   - 在上次发布后保留约 2 天
   - Routers 查询 floodfills 以发现其他 routers

**JavaDoc：** [RouterInfo](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterInfo.html)

---

## 实现说明

### 字节序（Endianness）

**默认：大端序（网络字节序）**

大多数 I2P 结构使用大端字节序: - 所有整数类型（1-8 字节） - 日期时间戳 - TunnelId（隧道 ID） - 字符串长度前缀 - 证书类型和长度 - 密钥类型代码 - 映射大小字段

**例外：小端序**

以下密钥类型使用**小端序**编码： - **X25519** 加密密钥 (类型 4) - **EdDSA_SHA512_Ed25519** 签名密钥 (类型 7) - **EdDSA_SHA512_Ed25519ph** 签名密钥 (类型 8) - **RedDSA_SHA512_Ed25519** 签名密钥 (类型 11)

**实现：**

```java
// Big-endian (most structures)
int value = ((bytes[0] & 0xFF) << 24) | 
            ((bytes[1] & 0xFF) << 16) |
            ((bytes[2] & 0xFF) << 8) | 
            (bytes[3] & 0xFF);

// Little-endian (X25519, EdDSA, RedDSA)
int value = (bytes[0] & 0xFF) | 
            ((bytes[1] & 0xFF) << 8) |
            ((bytes[2] & 0xFF) << 16) | 
            ((bytes[3] & 0xFF) << 24);
```
### 结构版本控制

**切勿假设固定大小：**

许多结构具有可变长度: - RouterIdentity（路由器身份）: 387+ 字节（并非总是 387） - Destination（目的地标识）: 387+ 字节（并非总是 387） - LeaseSet2（租约集2）: 变化幅度很大 - Certificate（证书）: 3+ 字节

**始终读取大小字段：** - 证书长度位于第 1-2 字节 - 映射大小位于开头 - KeysAndCert 始终按 384 + 3 + certificate_length 计算

**检查是否有多余数据:** - 禁止在有效结构之后出现尾随垃圾数据 - 验证证书长度与密钥类型匹配 - 对固定大小类型强制执行精确的预期长度

### 当前建议（2025年10月）

**针对新的 Router 身份：**

```
Encryption: X25519 (type 4, 32 bytes)
Signing: EdDSA_SHA512_Ed25519 (type 7, 32 bytes)
Certificate: Key Certificate (type 5)
Total Size: 391 bytes
Padding: Compressible per [Proposal 161](/zh/proposals/161-ri-dest-padding/)
```
**对于新的 Destination（目标标识）：**

```
Unused Public Key Field: 256 bytes random (compressible)
Signing: EdDSA_SHA512_Ed25519 (type 7, 32 bytes)
Certificate: Key Certificate (type 5)
Total Size: 391 bytes
Padding: Compressible per [Proposal 161](/zh/proposals/161-ri-dest-padding/)
```
**针对新的 LeaseSets：**

```
Type: LeaseSet2 (type 3)
Encryption Keys: X25519 (type 4, 32 bytes)
Leases: At least 1, typically 3-5
Options: Include service records per [Proposal 167](/proposals/167-service-records/)
Signature: EdDSA (64 bytes)
```
**适用于加密服务：**

```
Type: EncryptedLeaseSet (type 5)
Blinding: RedDSA_SHA512_Ed25519 (type 11)
Inner LeaseSet: LeaseSet2 (type 3)
Rotation: Daily blinding key rotation
Authorization: Per-client encryption keys
```
### 已弃用功能 - 请勿使用

**已弃用的加密:** - ElGamal (type 0) 用于 Router 身份（自 0.9.58 起弃用） - ElGamal/AES+SessionTag（会话标签）加密（使用 ECIES-X25519）

**已弃用的签名：** - 用于 Router 身份的 DSA_SHA1（类型 0）（自 0.9.58 起弃用） - ECDSA 变体（类型 1-3），不用于新的实现 - RSA 变体（类型 4-6），SU3 文件除外

**已弃用的网络格式:** - LeaseSet 类型 1 (使用 LeaseSet2) - Lease (44 字节, 使用 Lease2) - 原始 Lease 到期时间格式

**已弃用的传输协议：** - NTCP (已在 0.9.50 中移除) - SSU (已在 2.4.0 中移除)

**已弃用的证书：** - HASHCASH (type 1)（使用 Hashcash 机制的证书类型） - HIDDEN (type 2)（隐藏证书类型） - SIGNED (type 3)（签名证书类型） - MULTIPLE (type 4)（多重证书类型）

### 安全注意事项

**密钥生成：** - 始终使用密码学安全的随机数生成器 - 切勿在不同上下文中复用密钥 - 通过适当的访问控制保护私钥 - 完成后从内存中安全擦除密钥材料

**签名验证：** - 在信任数据之前务必验证签名 - 检查签名长度与密钥类型匹配 - 验证已签名的数据包含预期字段 - 对于已排序的映射，在签名/验证前先验证排序顺序

**时间戳验证：** - 检查发布时间是否合理（不是过远的未来时间） - 验证租约未过期 - 考虑时钟偏差容差（典型值为 ±30 秒）

**网络数据库：** - 在存储之前验证所有结构 - 强制执行大小限制以防止 DoS - 对查询和发布实施速率限制 - 验证数据库键与结构哈希匹配

### 兼容性说明

**向后兼容性：** - ElGamal 和 DSA_SHA1 仍支持旧版 routers - 已弃用的密钥类型仍可用，但不建议使用 - 可压缩填充（[Proposal 161](/zh/proposals/161-ri-dest-padding/)）与 0.6 版本向后兼容

**前向兼容性:** - 未知的密钥类型可以使用长度字段进行解析 - 未知的证书类型可以通过长度跳过 - 未知的签名类型应当被稳妥地处理 - 实现不应因未知的可选特性而失败

**迁移策略:** - 在过渡期间同时支持新旧密钥类型 - LeaseSet2（LeaseSet 的第二版）可以列出多个加密密钥 - 离线签名实现安全的密钥轮换 - MetaLeaseSet（用于透明服务迁移的元 LeaseSet）实现透明的服务迁移

### 测试与验证

**结构验证：** - 验证所有长度字段都在预期范围内 - 检查可变长度结构能被正确解析 - 验证签名能够成功通过校验 - 使用最小和最大尺寸的结构进行测试

**边界情况:** - 零长度字符串 - 空映射 - 最小和最大租约数 - 有效载荷为零长度的证书 - 非常大的结构（接近最大大小）

**互操作性：** - 对照官方 Java I2P 实现进行测试 - 验证与 i2pd 的兼容性 - 使用各种网络数据库（netDb）内容进行测试 - 对照已知正确的测试向量进行验证

---

## 参考资料

### 规范

- [I2NP 协议](/docs/specs/i2np/)
- [I2CP 协议](/docs/specs/i2cp/)
- [SSU2 传输](/docs/specs/ssu2/)
- [NTCP2 传输](/docs/specs/ntcp2/)
- [Tunnel 协议](/docs/specs/implementation/)
- [数据报协议](/docs/api/datagrams/)

### 密码学

- [密码学概览](/docs/specs/cryptography/)
- [ElGamal/AES 加密](/docs/legacy/elgamal-aes/)
- [ECIES-X25519 加密](/docs/specs/ecies/)
- [面向 Routers 的 ECIES](/docs/specs/ecies/#routers)
- [ECIES 混合（后量子）](/docs/specs/ecies/#hybrid)
- [Red25519 签名](/docs/specs/red25519-signature-scheme/)
- [加密的 LeaseSet](/docs/specs/encryptedleaseset/)

### 提案

- [提案 123：新的 netDB 条目](/proposals/123-new-netdb-entries/)
- [提案 134：GOST 签名类型](/proposals/134-gost/)
- [提案 136：实验性签名类型](/proposals/136-experimental-sigtypes/)
- [提案 145：ECIES-P256](/proposals/145-ecies/)
- [提案 156：ECIES Routers](/proposals/156-ecies-routers/)
- [提案 161：填充生成](/zh/proposals/161-ri-dest-padding/)
- [提案 167：服务记录](/proposals/167-service-records/)
- [提案 169：后量子密码学](/proposals/169-pq-crypto/)
- [全部提案索引](/proposals/)

### 网络数据库

- [netDb 概览](/docs/specs/common-structures/)
- [RouterInfo 标准选项](/docs/specs/common-structures/#routerInfo)

### JavaDoc API 参考


### 外部标准

- **RFC 7748 (X25519):** 用于安全的椭圆曲线
- **RFC 7539 (ChaCha20):** 用于 IETF 协议的 ChaCha20 和 Poly1305
- **RFC 4648 (Base64):** Base16、Base32 和 Base64 数据编码
- **FIPS 180-4 (SHA-256):** 安全散列标准
- **FIPS 204 (ML-DSA):** 基于模格的数字签名标准
- [IANA 服务注册表](http://www.dns-sd.org/ServiceTypes.html)

### 社区资源

- [I2P 网站](/)
- [I2P 论坛](https://i2pforum.net)
- [I2P GitLab](https://i2pgit.org/I2P_Developers/i2p.i2p)
- [I2P GitHub 镜像](https://github.com/i2p/i2p.i2p)
- [技术文档索引](/docs/)

### 发布信息

- [I2P 2.10.0 发布](/zh/blog/2025/09/08/i2p-2.10.0-release/)
- [发布历史](https://github.com/i2p/i2p.i2p/blob/master/history.txt)
- [更新日志](https://github.com/i2p/i2p.i2p/blob/master/debian/changelog)

---

## 附录：快速参考表

### 密钥类型快速参考

**当前标准（建议所有新的实现采用）：** - **加密：** X25519 (类型 4, 32 字节, 小端序) - **签名：** EdDSA_SHA512_Ed25519 (类型 7, 32 字节, 小端序)

**旧版（受支持但已弃用）：** - **加密：** ElGamal (类型 0，256 字节，大端序) - **签名：** DSA_SHA1 (类型 0，20 字节私钥 / 128 字节公钥，大端序)

**专用:** - **签名（加密的 LeaseSet）:** RedDSA_SHA512_Ed25519 (类型 11, 32 字节, 小端序)

**后量子（测试版，尚未最终确定）：** - **混合加密：** MLKEM_X25519 变体（类型 5-7） - **纯后量子加密：** MLKEM（模块格密钥封装机制，Kyber）变体（尚未分配类型代码）

### 结构大小速查表

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Structure</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Minimum Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Typical Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Maximum Size</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Integer</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Date</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">String</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">256 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SessionKey</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Hash</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelId</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Certificate</td><td style="border:1px solid var(--color-border); padding:0.5rem;">3 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">7 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">65,538 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">KeysAndCert</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">391 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterIdentity</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">391 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Destination</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">391 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Lease</td><td style="border:1px solid var(--color-border); padding:0.5rem;">44 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">44 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">44 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Lease2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1200 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈2000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈500 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈800 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈2000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈600 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈3000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterAddress</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈150 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈300 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈600 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1500 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈3000+ bytes</td></tr>
  </tbody>
</table>
### 数据库类型速查表

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Structure</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Stored under Hash(RouterIdentity)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Use LeaseSet2 instead</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Stored under Hash(Destination)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Stored under Hash(Blinded Destination)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">MetaLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Defined</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Verify production status</td></tr>
  </tbody>
</table>
### 传输协议快速参考

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Port Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">UDP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.54</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Default since 0.9.56</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TCP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.36</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">UDP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1pxsolid var(--color-border); padding:0.5rem;">Removed in 2.4.0</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TCP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed in 0.9.50</td></tr>
  </tbody>
</table>
### 版本里程碑快速参考

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">API</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Date</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Changes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.6.x</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2005</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destination encryption disabled</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Dec 2013</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Key Certificates introduced</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Sep 2015</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA support added</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.16</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.16</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Nov 2015</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Router Key Certificates</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.36</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.36</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Aug 2018</td><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP2 introduced</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Nov 2018</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2, X25519 for Destinations</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Dec 2018</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet working</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.48</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.48</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Jul 2020</td><td style="border:1px solid var(--color-border); padding:0.5rem;">X25519 for Router Identities</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.50</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.50</td><td style="border:1px solid var(--color-border); padding:0.5rem;">May 2021</td><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP removed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.54</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.54</td><td style="border:1px solid var(--color-border); padding:0.5rem;">May 2022</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 testing</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.57</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.57</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Jan 2023</td><td style="border:1px solid var(--color-border); padding:0.5rem;">[Proposal 161](/zh/proposals/161-ri-dest-padding/) padding (release 2.1.0)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.58</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.58</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mar 2023</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal/DSA deprecated for RIs (2.2.0)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.66</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.66</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Jun 2025</td><td style="border:1px solid var(--color-border); padding:0.5rem;">[Proposal 167](/proposals/167-service-records/) service records (2.9.0)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Sep 2025</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ML-KEM beta support (2.10.0)</td></tr>
  </tbody>
</table>
---
