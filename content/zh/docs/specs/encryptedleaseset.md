---
title: "加密的 LeaseSet"
description: "受访问控制的 LeaseSet 格式，用于私有 Destination（目标标识）"
slug: "encryptedleaseset"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## 概述

本文档规定了对加密的 LeaseSet2（LS2）的盲化、加密和解密。加密的 LeaseSets 用于在 I2P 网络数据库（netDb）中以受访问控制的方式发布隐藏服务信息。

**关键特性:** - 每日密钥轮换，以实现前向保密 - 两级客户端授权（基于 DH 和基于 PSK） - 在没有 AES 硬件的设备上使用 ChaCha20 加密以提升性能 - 带密钥盲化的 Red25519 签名 - 隐私保护的客户端成员资格

**相关文档：** - [通用结构规范](/docs/specs/common-structures/) - 加密的 LeaseSet（租约集）结构 - [提案 123：新的 netDB（网络数据库）条目](/proposals/123-new-netdb-entries/) - 加密 LeaseSet 的背景 - [网络数据库文档](/docs/specs/common-structures/) - NetDB 用法

---

## 版本历史与实现状态

### 协议开发时间线

**关于版本编号的重要说明：**   I2P 使用两套独立的版本编号方案：
- **API/Router 版本：** 0.9.x 系列（用于技术规范）
- **产品发布版本：** 2.x.x 系列（用于公开发布）

技术规范会引用 API 版本（例如 0.9.41），而终端用户看到的是产品版本（例如 2.10.0）。

### 实现里程碑

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Release Date</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Features</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.38</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">January 2019</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Floodfill support for standard LS2, offline keys</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.39</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">March 2019</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Full encrypted LS2 support, Red25519 (sig type&nbsp;11)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.40</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">May 2019</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Per-client authorization, encrypted LS2 with offline keys, B32 support</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.41</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">June 2019</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Protocol finalized as stable</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>2.10.0</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">September 2025</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Latest Java implementation (API version 0.9.61)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>i2pd 2.58.0</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">September 2025</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Full C++ implementation compatibility</td></tr>
  </tbody>
</table>
### 当前状态

- ✅ **协议状态:** 自2019年6月以来保持稳定且未变更
- ✅ **Java I2P:** 在 0.9.40+ 版本中已完整实现
- ✅ **i2pd (C++):** 在 2.58.0+ 版本中已完整实现
- ✅ **互操作性:** 各实现之间完全互通
- ✅ **网络部署:** 已达生产就绪，拥有6年以上的运行经验

---

## 密码学定义

### 记法与约定

- `||` 表示连接（拼接）
- `mod L` 表示按 Ed25519 的阶进行模约简
- 除非另有说明，所有字节数组均采用网络字节序（大端）
- 小端序的数值会被明确标注

### CSRNG(n)（密码学安全随机数生成器）

**密码学安全的随机数生成器**

生成 `n` 字节的密码学安全随机数据，适用于密钥材料生成。

**安全要求：** - 必须在密码学上安全（适用于密钥生成） - 当相邻的字节序列暴露在网络上时也必须是安全的 - 实现应当对来自可能不可信来源的输出进行哈希处理

**参考资料：** - [PRNG 安全考量](http://projectbullrun.org/dual-ec/ext-rand.html) - [Tor 开发者讨论](https://lists.torproject.org/pipermail/tor-dev/2015-November/009954.html)

### H(p, d)

**带个性化的 SHA-256 哈希**

域分离哈希函数，接收： - `p`: 个性化字符串（提供域分离） - `d`: 待哈希的数据

**实现：**

```
H(p, d) := SHA-256(p || d)
```
**用途：** 提供密码学域分离，以防止在不同协议对 SHA-256 的使用之间发生碰撞攻击。

### 流加密: ChaCha20

**流密码：ChaCha20，如 RFC 7539 第 2.4 节所述**

**参数：** - `S_KEY_LEN = 32` (256 位密钥) - `S_IV_LEN = 12` (96 位 nonce（随机数）) - 初始计数器：`1` (RFC 7539 允许为 0 或 1; 在 AEAD 场景中推荐使用 1)

**加密(k, iv, plaintext)**

使用以下参数加密明文： - `k`: 32 字节加密密钥 - `iv`: 12 字节随机数（nonce）（对于每个密钥必须唯一） - 返回的密文与明文大小相同

**安全性质:** 若密钥保密，整个密文必须与随机数据不可区分。

**DECRYPT(k, iv, ciphertext)**

使用以下参数解密密文： - `k`: 32 字节的加密密钥 - `iv`: 12 字节的 nonce（一次性随机数） - 返回明文

**设计理由：** 之所以选择 ChaCha20 而非 AES，原因在于： - 在没有硬件加速的设备上，比 AES 快 2.5-3 倍 - 更容易实现常数时间（constant-time） - 在可用 AES-NI（AES 指令集扩展）时，安全性和速度相当

**参考资料：** - [RFC 7539](https://datatracker.ietf.org/doc/html/rfc7539) - 用于 IETF 协议的 ChaCha20 和 Poly1305

### 签名算法: Red25519

**签名方案：Red25519（基于 Ed25519 的变体，SigType 11），并使用密钥盲化**

Red25519 基于 Ed25519 曲线上的 Ed25519 签名，使用 SHA-512 进行哈希，并按 ZCash RedDSA（ZCash 的 RedDSA 签名方案）的规范支持密钥盲化。

**功能：**

#### DERIVE_PUBLIC(privkey)

返回与给定私钥对应的公钥。 - 使用标准的 Ed25519 基点上的标量乘法

#### SIGN(privkey, m)

返回由私钥 `privkey` 对消息 `m` 的签名。

**Red25519 与 Ed25519 的签名差异:** 1. **Random Nonce（一次性随机数）:** 使用 80 字节的额外随机数据

   ```
   T = CSRNG(80)  // 80 random bytes
   r = H*(T || publickey || message)
   ```
这使得每个 Red25519（随机化签名算法）签名都是唯一的，即使消息和密钥相同也不例外。

2. **私钥生成：** Red25519 私钥由随机数生成，并在 `mod L` 下约简，而不是使用 Ed25519 的 bit-clamping（位钳制）方法。

#### VERIFY(pubkey, m, sig)

验证签名`sig`是否与公钥`pubkey`和消息`m`匹配。 - 如果签名有效则返回`true`，否则返回`false` - 验证过程与 Ed25519 完全相同

**密钥盲化操作：**

#### GENERATE_ALPHA(data, secret)

生成用于密钥盲化的 α。 - `data`: 通常包含签名公钥和签名类型 - `secret`: 可选的附加秘密（未使用时长度为零） - 结果与 Ed25519 私钥的分布一致（经过 mod L 约简后）

#### BLIND_PRIVKEY(privkey, alpha)

使用秘密值 `alpha` 对私钥进行盲化。 - 实现：`blinded_privkey = (privkey + alpha) mod L` - 在该域上使用标量运算

#### BLIND_PUBKEY(pubkey, alpha)

使用秘密 `alpha` 对公钥进行盲化。 - 实现: `blinded_pubkey = pubkey + DERIVE_PUBLIC(alpha)` - 使用曲线上的群元素（点）加法

**关键属性:**

```
BLIND_PUBKEY(pubkey, alpha) == DERIVE_PUBLIC(BLIND_PRIVKEY(privkey, alpha))
```
**安全注意事项：**

引自 ZCash 协议规范第 5.4.6.1 节：出于安全性考虑，alpha 必须与去盲后的私钥同分布。这确保“重新随机化的公钥与在该密钥下生成的签名的组合不会泄露它是从哪个密钥重新随机化得到的。”

**支持的签名类型:** - **类型 7 (Ed25519):** 支持用于现有目的地（向后兼容） - **类型 11 (Red25519):** 建议用于使用加密的新目的地 - **Blinded keys（盲化密钥）:** 始终使用类型 11 (Red25519)

**参考资料：** - [ZCash 协议规范](https://zips.z.cash/protocol/protocol.pdf) - 第 5.4.6 节 RedDSA - [I2P Red25519 规范](/docs/specs/red25519-signature-scheme/)

### DH（Diffie-Hellman）: X25519

**椭圆曲线迪菲-赫尔曼：X25519**

基于 Curve25519 的公钥密钥协商系统

**参数：** - 私钥：32 字节 - 公钥：32 字节 - 共享密钥输出：32 字节

**功能：**

#### GENERATE_PRIVATE()

使用 CSRNG（密码学安全随机数生成器）生成一个新的 32 字节私钥。

#### DERIVE_PUBLIC(privkey)

从给定的私钥导出 32 字节的公钥。 - 使用 Curve25519（椭圆曲线）上的标量乘法

#### DH(privkey, pubkey)

执行 Diffie-Hellman 密钥协商。 - `privkey`: 本地 32 字节私钥 - `pubkey`: 远端 32 字节公钥 - 返回: 32 字节共享密钥

**安全属性：** - 在 Curve25519 上的计算型 Diffie-Hellman (CDH) 假设 - 使用临时密钥时具备前向保密性 - 需要常数时间实现以防止时间侧信道攻击

**参考文献：** - [RFC 7748](https://datatracker.ietf.org/doc/html/rfc7748) - 用于安全的椭圆曲线

### HKDF（基于 HMAC 的提取与扩展密钥派生函数）

**基于 HMAC 的密钥派生函数**

从输入的密钥材料中提取并扩展密钥材料。

**参数:** - `salt`: 最多 32 字节（对于 SHA-256 通常为 32 字节） - `ikm`: 输入密钥材料（任意长度，应具有足够的熵） - `info`: 上下文相关的信息（域分离） - `n`: 输出长度（字节数）

**实现：**

使用 RFC 5869 规定的 HKDF（基于 HMAC 的密钥派生函数），其参数为:
- **哈希函数:** SHA-256
- **HMAC:** 如 RFC 2104 所述
- **盐长度:** 最多 32 字节（针对 SHA-256 的 HashLen）

**使用模式：**

```
keys = HKDF(salt, ikm, info, n)
```
**域分离：** `info` 参数为协议中 HKDF 的不同用法之间提供加密域分离。

**已验证信息值:** - `"ELS2_L1K"` - 第 1 层（外层）加密 - `"ELS2_L2K"` - 第 2 层（内层）加密 - `"ELS2_XCA"` - DH 客户端授权 - `"ELS2PSKA"` - PSK 客户端授权 - `"i2pblinding1"` - Alpha 生成

**参考资料：** - [RFC 5869](https://datatracker.ietf.org/doc/html/rfc5869) - HKDF 规范 - [RFC 2104](https://datatracker.ietf.org/doc/html/rfc2104) - HMAC 规范

---

## 格式规范

加密的 LS2（第二代 leaseSet）由三个嵌套层组成：

1. **第0层（外层）：** 用于存储和检索的明文信息
2. **第1层（中层）：** 客户端认证数据（已加密）
3. **第2层（内层）：** 实际的 LeaseSet2（LeaseSet 的第二版）数据（已加密）

**整体结构：**

```
Layer 0 data + Enc(layer 1 data + Enc(layer 2 data)) + Signature
```
**重要：** 加密的 LS2 使用盲化密钥。Destination（目的地标识）不在首部中。DHT 的存储位置为 `SHA-256(sig type || blinded public key)`，每天轮换。

### 第0层 (外层) - 明文

第0层不使用标准的 LS2 头部。它使用一种专为盲化密钥优化的自定义格式。

**结构：**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Type</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Not in header, from DatabaseStore message field</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded Public Key Sig Type</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, always <code>0x000b</code> (Red25519 type 11)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded Public Key</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Red25519 blinded public key</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Published Timestamp</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, seconds since epoch (rolls over in 2106)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Expires</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, offset from published in seconds (max 65,535 &asymp; 18.2 hours)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Flags</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Bit flags (see below)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">[Optional] Transient Key Data</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Present if flag bit&nbsp;0 is set</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">lenOuterCiphertext</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, length of outer ciphertext</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">outerCiphertext</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">lenOuterCiphertext</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted Layer&nbsp;1 data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Red25519 signature over all preceding data</td></tr>
  </tbody>
</table>
**标志字段（2 字节，位 15-0）：** - **位 0：** 离线密钥指示符   - `0` = 无离线密钥   - `1` = 存在离线密钥（随后附带临时密钥数据） - **位 1-15：** 保留，必须为 0 以保证将来兼容性

**临时密钥数据（当标志位 bit 0 = 1 时存在）：**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Expires Timestamp</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, seconds since epoch</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Transient Sig Type</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, signature type</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Transient Signing Public Key</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Length implied by signature type</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signed by blinded public key; covers expires timestamp, transient sig type, and transient public key</td></tr>
  </tbody>
</table>
**签名验证：** - **无离线密钥：** 使用盲化公钥进行验证 - **有离线密钥：** 使用临时公钥进行验证

签名覆盖从 Type 到 outerCiphertext 的所有数据（包含两者）。

### 第1层（中间） - 客户端授权

**解密：** 参见[第 1 层加密](#layer-1-encryption)一节。

**结构：**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Flags</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Authorization flags (see below)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">[Optional] Auth Data</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Present based on flags</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">innerCiphertext</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted Layer&nbsp;2 data (remainder)</td></tr>
  </tbody>
</table>
**标志字段（1 字节，位 7-0）：** - **位 0：** 授权模式   - `0` = 无按客户端授权（所有人）   - `1` = 按客户端授权（随后为授权部分） - **位 3-1：** 认证方案（仅当位 0 = 1 时）   - `000` = DH 客户端认证   - `001` = PSK 客户端认证   - 其他保留 - **位 7-4：** 未使用，必须为 0

**DH 客户端授权数据 (标志 = 0x01, 位 3-1 = 000):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ephemeralPublicKey</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Server's ephemeral X25519 public key</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">clients</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, number of client entries</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">authClient[]</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">40 bytes each</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Array of client authorization entries</td></tr>
  </tbody>
</table>
**authClient 条目 (40 字节):** - `clientID_i`: 8 字节 - `clientCookie_i`: 32 字节 (加密的 authCookie)

**PSK（预共享密钥）客户端授权数据（flags = 0x03，bits 3-1 = 001）：**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">authSalt</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Salt for PSK key derivation</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">clients</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, number of client entries</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">authClient[]</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">40 bytes each</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Array of client authorization entries</td></tr>
  </tbody>
</table>
**authClient 条目 (40 字节):** - `clientID_i`: 8 字节 - `clientCookie_i`: 32 字节 (加密的 authCookie (身份验证 Cookie))

### 第2层（内部） - LeaseSet 数据

**解密：** 参见[第 2 层加密](#layer-2-encryption)一节。

**结构：**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Type</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>3</code> (LS2) or <code>7</code> (Meta LS2)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Complete LeaseSet2 or MetaLeaseSet2</td></tr>
  </tbody>
</table>
内层包含完整的 LeaseSet2 结构，包括： - LS2 头部 - 租约信息 - LS2 签名

**验证要求：** 解密后，实现必须验证：1. 内部时间戳与外部发布的时间戳相匹配 2. 内部过期时间与外部过期时间相匹配 3. LS2 签名有效 4. 租约数据格式正确

**参考资料：** - [通用结构规范](/docs/specs/common-structures/) - LeaseSet2（LeaseSet 的第二版）格式详细说明

---

## 盲化密钥派生

### 概述

I2P 使用基于 Ed25519 和 ZCash RedDSA 的 additive key blinding scheme（加法型密钥盲化方案）。为实现前向保密，盲化密钥每天（UTC 午夜）轮换。

**设计依据：**

I2P 明确选择不采用 Tor 的 rend-spec-v3.txt 附录 A.2 中的方案。根据该规范：

> "我们不使用 Tor 的 rend-spec-v3.txt 的附录 A.2（其设计目标相似），因为其盲化的公钥可能不在素数阶子群上，其安全影响未知。"

I2P 的加法盲化保证盲化后的密钥仍位于 Ed25519 曲线的素数阶子群上。

### 数学定义

**Ed25519 参数：** - `B`: Ed25519 基点（生成元） = `2^255 - 19` - `L`: Ed25519 阶 = `2^252 + 27742317777372353535851937790883648493`

**关键变量:** - `A`: 未盲化的 32 字节签名公钥（位于 Destination（I2P 目标标识）中） - `a`: 未盲化的 32 字节签名私钥 - `A'`: 已盲化的 32 字节签名公钥（用于加密的 LeaseSet） - `a'`: 已盲化的 32 字节签名私钥 - `alpha`: 32 字节盲化因子（秘密）

**辅助函数：**

#### LEOS2IP(x)

"将小端序八位字节串转换为整数"

将小端序字节数组转换为整数表示。

#### H*(x)

"哈希与归约"

```
H*(x) = (LEOS2IP(SHA512(x))) mod L
```
与 Ed25519 密钥生成中的操作相同。

### Alpha 生成

**每日轮换：** 必须每天在 UTC 午夜（00:00:00 UTC）生成新的 alpha（参数名）和盲化密钥。

**GENERATE_ALPHA(destination, date, secret) 算法：**

```python
# Input parameters
A = destination's signing public key (32 bytes)
stA = signature type of A (2 bytes, big endian)
     # 0x0007 for Ed25519 or 0x000b for Red25519
stA' = signature type of blinded key A' (2 bytes, big endian) 
     # Always 0x000b (Red25519)
datestring = "YYYYMMDD" (8 bytes ASCII from current UTC date)
secret = optional UTF-8 encoded string (zero-length if not used)

# Computation
keydata = A || stA || stA'  # 36 bytes total
seed = HKDF(
    salt=H("I2PGenerateAlpha", keydata),
    ikm=datestring || secret,
    info="i2pblinding1",
    n=64
)

# Treat seed as 64-byte little-endian integer and reduce
alpha = seed mod L
```
**已验证的参数：** - 盐值个性化：`"I2PGenerateAlpha"` - HKDF 信息：`"i2pblinding1"` - 输出：约简前为 64 字节 - Alpha 的分布：在 `mod L` 之后与 Ed25519 私钥的分布相同

### 私钥盲化

**BLIND_PRIVKEY(a, alpha) 算法：**

对于发布加密的 LeaseSet 的目的地（Destination）所有者：

```python
# For Ed25519 private key (type 7)
if sigtype == 7:
    seed = destination's signing private key (32 bytes)
    a = left_half(SHA512(seed))  # 32 bytes
    a = clamp(a)  # Ed25519 clamping
    
# For Red25519 private key (type 11)
elif sigtype == 11:
    a = destination's signing private key (32 bytes)
    # No clamping for Red25519

# Additive blinding using scalar arithmetic
blinded_privkey = a' = (a + alpha) mod L

# Derive blinded public key
blinded_pubkey = A' = DERIVE_PUBLIC(a')
```
**关键：** `mod L` 约化对于保持私钥与公钥之间正确的代数关系至关重要。

### 公钥盲化

**BLIND_PUBKEY(A, alpha) 算法:**

对于检索并验证加密 LeaseSet 的客户端：

```python
alpha = GENERATE_ALPHA(destination, date, secret)
A = destination's signing public key (32 bytes)

# Additive blinding using group elements (curve points)
blinded_pubkey = A' = A + DERIVE_PUBLIC(alpha)
```
**数学等价性：**

这两种方法产生完全相同的结果：

```
BLIND_PUBKEY(A, alpha) == DERIVE_PUBLIC(BLIND_PRIVKEY(a, alpha))
```
这是因为：

```
A' = A + [alpha]B
   = [a]B + [alpha]B
   = [a + alpha]B  (group operation)
   = DERIVE_PUBLIC(a + alpha mod L)
```
### 使用盲化密钥签名

**未盲化 LeaseSet 签名:**

unblinded（未盲化）的 LeaseSet（直接发送给已认证的客户端）使用以下方式签名： - 标准 Ed25519（类型 7）或 Red25519（类型 11）签名 - unblinded 签名私钥 - 使用 unblinded 公钥进行验证

**使用离线密钥：** - 由去盲的临时私钥签名 - 使用去盲的临时公钥验证 - 二者都必须为类型 7 或 11

**加密的 LeaseSet（租约集）签名：**

加密的 LeaseSet 的外层部分使用带盲化密钥的 Red25519（可重随机化的 Ed25519）签名。

**Red25519 签名算法：**

```python
# Generate per-signature random nonce
T = CSRNG(80)  # 80 random bytes

# Calculate r (differs from Ed25519)
r = H*(T || blinded_pubkey || message)

# Rest is same as Ed25519
R = [r]B
S = (r + H(R || A' || message) * a') mod L
signature = R || S  # 64 bytes total
```
**与 Ed25519 的关键差异：** 1. 使用 80 字节的随机数据 `T` (而非私钥的哈希) 2. 直接使用公钥值 (而非私钥的哈希) 3. 即使针对相同的消息和密钥，每个签名也都是唯一的

**验证：**

与 Ed25519（椭圆曲线数字签名算法）相同：

```python
# Parse signature
R = signature[0:32]
S = signature[32:64]

# Verify equation: [S]B = R + [H(R || A' || message)]A'
return [S]B == R + [H(R || A' || message)]A'
```
### 安全注意事项

**Alpha 发行版：**

为了安全起见，alpha 必须与未盲化的私钥同分布。当将 Ed25519（类型 7）盲化为 Red25519（与 Ed25519 相关的一种密钥格式）（类型 11）时，这些分布会略有不同。

**建议：**对未盲化和盲化密钥都使用 Red25519（type 11），以满足 ZCash 的要求：“将一个再随机化（re-randomized）的公钥与在该密钥下的签名组合在一起，不会泄露其再随机化来源的密钥。”

**类型 7 支持：** 为与现有 Destination（目标地址）保持向后兼容，支持 Ed25519，但对于新的加密 Destination，推荐使用类型 11。

**每日轮换的优势：** - 前向保密性：即使今日的盲化密钥被攻破，也不会泄露昨日的盲化密钥 - 不可关联性：每日轮换可防止通过 DHT（分布式哈希表）进行的长期跟踪 - 密钥分离：不同时间段使用不同的密钥

**参考资料：** - [ZCash 协议规范](https://zips.z.cash/protocol/protocol.pdf) - 第 5.4.6.1 节 - [Tor 密钥盲化讨论](https://lists.torproject.org/pipermail/tor-dev/2013-December/005943.html) - [Tor 工单 #8106](https://trac.torproject.org/projects/tor/ticket/8106)

---

## 加密与处理

### Subcredential（子凭据）派生

在加密之前，我们派生出一个凭据和一个子凭据，以将加密层与持有 Destination（目的地标识）的签名公钥这一事实绑定。

**目标：** 确保只有知道 Destination（I2P 目的地标识）的签名公钥的人才能解密加密的 LeaseSet。不需要完整的 Destination。

#### 凭证计算

```python
A = destination's signing public key (32 bytes)
stA = signature type of A (2 bytes big endian)
     # 0x0007 for Ed25519 or 0x000b for Red25519
stA' = signature type of blinded key A' (2 bytes big endian)
     # Always 0x000b (Red25519)

keydata = A || stA || stA'  # 36 bytes

credential = H("credential", keydata)  # 32 bytes
```
**域分离:** 个性化字符串 `"credential"` 可确保此哈希不会与任何 DHT 查找键或协议中的其他用法发生碰撞。

#### Subcredential（子凭据）计算

```python
blindedPublicKey = A' (32 bytes, from blinding process)

subcredential = H("subcredential", credential || blindedPublicKey)  # 32 bytes
```
**目的:** subcredential（子凭据）将加密的 LeaseSet 绑定到: 1. 特定的 Destination（目标标识）（通过 credential） 2. 特定的盲化密钥（通过 blindedPublicKey） 3. 特定的日期（通过对 blindedPublicKey 的每日轮换）

这可以防止重放攻击和跨日关联。

### 第一层加密

**上下文：** 第1层包含客户端授权数据，并使用由 subcredential（子凭据）派生的密钥进行加密。

#### 加密算法

```python
# Prepare input
outerInput = subcredential || publishedTimestamp
# publishedTimestamp: 4 bytes from Layer 0

# Generate random salt
outerSalt = CSRNG(32)  # 32 bytes

# Derive encryption key and IV
keys = HKDF(
    salt=outerSalt,
    ikm=outerInput,
    info="ELS2_L1K",  # Domain separation
    n=44  # 32 bytes key + 12 bytes IV
)

outerKey = keys[0:31]    # 32 bytes (indices 0-31 inclusive)
outerIV = keys[32:43]    # 12 bytes (indices 32-43 inclusive)

# Encrypt and prepend salt
outerPlaintext = [Layer 1 data]
outerCiphertext = outerSalt || ENCRYPT(outerKey, outerIV, outerPlaintext)
```
**输出：** `outerCiphertext` 为 `32 + len(outerPlaintext)` 字节。

**安全属性:** - 盐值确保即使使用相同的子凭据也能得到唯一的密钥/IV 对 - 上下文字符串 `"ELS2_L1K"` 提供域分离 - ChaCha20 提供语义安全（密文与随机数不可区分）

#### 解密算法

```python
# Parse salt from ciphertext
outerSalt = outerCiphertext[0:31]  # First 32 bytes

# Derive decryption key and IV (same process as encryption)
outerInput = subcredential || publishedTimestamp
keys = HKDF(
    salt=outerSalt,
    ikm=outerInput,
    info="ELS2_L1K",
    n=44
)

outerKey = keys[0:31]    # 32 bytes
outerIV = keys[32:43]    # 12 bytes

# Decrypt (skip salt bytes)
outerPlaintext = DECRYPT(outerKey, outerIV, outerCiphertext[32:end])
```
**验证：** 解密后，先验证第 1 层结构是否正确，再继续处理第 2 层。

### 二层加密

**上下文：** 第2层包含实际的 LeaseSet2 数据，并使用从 authCookie（如果启用了按客户端认证）或空字符串（如果未启用）派生的密钥进行加密。

#### 加密算法

```python
# Determine authCookie based on authorization mode
if per_client_auth_enabled:
    authCookie = [32-byte cookie from client authorization process]
else:
    authCookie = b''  # Zero-length byte array

# Prepare input
innerInput = authCookie || subcredential || publishedTimestamp

# Generate random salt
innerSalt = CSRNG(32)  # 32 bytes

# Derive encryption key and IV
keys = HKDF(
    salt=innerSalt,
    ikm=innerInput,
    info="ELS2_L2K",  # Domain separation
    n=44  # 32 bytes key + 12 bytes IV
)

innerKey = keys[0:31]    # 32 bytes
innerIV = keys[32:43]    # 12 bytes

# Encrypt and prepend salt
innerPlaintext = [Layer 2 data: LS2 type byte + LeaseSet2 data]
innerCiphertext = innerSalt || ENCRYPT(innerKey, innerIV, innerPlaintext)
```
**输出:** `innerCiphertext` 为 `32 + len(innerPlaintext)` 字节。

**密钥绑定:** - 如果未启用客户端认证: 仅绑定到子凭据和时间戳 - 如果启用了客户端认证: 另外绑定到 authCookie (对每个已授权客户端都不同)

#### 解密算法

```python
# Determine authCookie (same as encryption)
if per_client_auth_enabled:
    authCookie = [32-byte cookie from client authorization process]
else:
    authCookie = b''  # Zero-length byte array

# Parse salt from ciphertext
innerSalt = innerCiphertext[0:31]  # First 32 bytes

# Derive decryption key and IV
innerInput = authCookie || subcredential || publishedTimestamp
keys = HKDF(
    salt=innerSalt,
    ikm=innerInput,
    info="ELS2_L2K",
    n=44
)

innerKey = keys[0:31]    # 32 bytes
innerIV = keys[32:43]    # 12 bytes

# Decrypt (skip salt bytes)
innerPlaintext = DECRYPT(innerKey, innerIV, innerCiphertext[32:end])
```
**验证：** 解密后: 1. 验证 LS2（LeaseSet2，I2P 中 LeaseSet 的第二版）类型字节是否有效 (3 或 7) 2. 解析 LeaseSet2 结构 3. 验证内部时间戳与外部发布的时间戳一致 4. 验证内部过期时间与外部过期时间一致 5. 验证 LeaseSet2 签名

### 加密层概述

```
┌─────────────────────────────────────────────────┐
│ Layer 0 (Plaintext)                             │
│ - Blinded public key                            │
│ - Timestamps                                    │
│ - Signature                                     │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │ Layer 1 (Encrypted with subcredential)  │   │
│  │ - Authorization flags                   │   │
│  │ - Client auth data (if enabled)         │   │
│  │                                          │   │
│  │  ┌────────────────────────────────┐     │   │
│  │  │ Layer 2 (Encrypted with        │     │   │
│  │  │          authCookie + subcred) │     │   │
│  │  │ - LeaseSet2 type               │     │   │
│  │  │ - LeaseSet2 data               │     │   │
│  │  │ - Leases                       │     │   │
│  │  │ - LS2 signature                │     │   │
│  │  └────────────────────────────────┘     │   │
│  └─────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```
**解密流程：** 1. 使用盲化公钥验证第0层签名 2. 使用 subcredential（子凭据）解密第1层 3. 处理授权数据（如存在）以获取 authCookie（授权Cookie） 4. 使用 authCookie 和 subcredential 解密第2层 5. 验证并解析 LeaseSet2

---

## 按客户端授权

### 概述

启用逐客户端授权时，服务器会维护一个已授权客户端的列表。每个客户端都拥有必须通过带外方式安全传输的密钥材料。

**两种授权机制：** 1. **DH（Diffie-Hellman，迪菲-赫尔曼）客户端授权：** 更安全，使用 X25519 密钥协商 2. **PSK（Pre-Shared Key，预共享密钥）授权：** 更简单，使用对称密钥

**常见安全属性：** - 客户端成员隐私：观察者可以看到客户端数量，但无法识别具体的客户端 - 匿名的客户端添加/撤销：无法追踪特定客户端何时被添加或移除 - 8 字节客户端标识符的碰撞概率：~1/（18×10^18）（可忽略不计）

### DH（Diffie-Hellman 密钥交换）客户端授权

**概述:** 每个客户端生成一个 X25519（椭圆曲线密钥交换算法）密钥对，并通过安全的带外通道将其公钥发送到服务器。服务器使用临时 DH（Diffie-Hellman）为每个客户端加密一个唯一的 authCookie。

#### 客户端密钥生成

```python
# Client generates keypair
csk_i = GENERATE_PRIVATE()  # 32-byte X25519 private key
cpk_i = DERIVE_PUBLIC(csk_i)  # 32-byte X25519 public key

# Client sends cpk_i to server via secure out-of-band channel
# Client KEEPS csk_i secret (never transmitted)
```
**安全优势：** 客户端的私钥永不离开其设备。即使攻击者截获带外传输，在不攻破 X25519 DH 的情况下，也无法解密未来的加密 LeaseSets。

#### 服务器端处理

```python
# Server generates new auth cookie and ephemeral keypair
authCookie = CSRNG(32)  # 32-byte cookie

esk = GENERATE_PRIVATE()  # 32-byte ephemeral private key
epk = DERIVE_PUBLIC(esk)  # 32-byte ephemeral public key

# For each authorized client i
for cpk_i in authorized_clients:
    # Perform DH key agreement
    sharedSecret = DH(esk, cpk_i)  # 32 bytes
    
    # Derive client-specific encryption key
    authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
    okm = HKDF(
        salt=epk,  # Ephemeral public key as salt
        ikm=authInput,
        info="ELS2_XCA",  # Domain separation
        n=52  # 32 key + 12 IV + 8 ID
    )
    
    # Extract components
    clientKey_i = okm[0:31]    # 32 bytes
    clientIV_i = okm[32:43]    # 12 bytes
    clientID_i = okm[44:51]    # 8 bytes
    
    # Encrypt authCookie for this client
    clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
    
    # Store [clientID_i, clientCookie_i] entry in Layer 1
```
**第 1 层数据结构：**

```
ephemeralPublicKey (32 bytes)
clients (2 bytes) = N
[clientID_1 (8 bytes) || clientCookie_1 (32 bytes)]
[clientID_2 (8 bytes) || clientCookie_2 (32 bytes)]
...
[clientID_N (8 bytes) || clientCookie_N (32 bytes)]
```
**服务器端建议：** - 为每个已发布的加密 LeaseSet（租约集）生成新的临时密钥对 - 随机化客户端顺序，以防止基于位置的跟踪 - 考虑添加填充条目以隐藏真实的客户端数量

#### 客户端处理

```python
# Client has: csk_i (their private key), destination, date, secret
# Client receives: encrypted LeaseSet with epk in Layer 1

# Perform DH key agreement with server's ephemeral public key
sharedSecret = DH(csk_i, epk)  # 32 bytes

# Derive expected client identifier and decryption key
cpk_i = DERIVE_PUBLIC(csk_i)  # Client's own public key
authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp

okm = HKDF(
    salt=epk,
    ikm=authInput,
    info="ELS2_XCA",
    n=52
)

clientKey_i = okm[0:31]    # 32 bytes
clientIV_i = okm[32:43]    # 12 bytes
clientID_i = okm[44:51]    # 8 bytes

# Search Layer 1 authorization data for clientID_i
for (clientID, clientCookie) in layer1_auth_entries:
    if clientID == clientID_i:
        # Found matching entry, decrypt authCookie
        authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie)
        # Use authCookie to decrypt Layer 2
        break
else:
    # No matching entry - client not authorized or revoked
    raise AuthorizationError("Client not authorized")
```
**客户端错误处理：** - 如果未找到`clientID_i`：客户端已被撤销或从未被授权 - 如果解密失败：数据损坏或密钥错误（极其罕见） - 客户端应定期重新获取以检测是否被撤销

### PSK（预共享密钥）客户端授权

**概述：** 每个客户端都有一个预共享的32字节对称密钥。服务器使用每个客户端的PSK（预共享密钥）对相同的authCookie进行加密。

#### 密钥生成

```python
# Option 1: Client generates key
psk_i = CSRNG(32)  # 32-byte pre-shared key
# Client sends psk_i to server via secure out-of-band channel

# Option 2: Server generates key
psk_i = CSRNG(32)  # 32-byte pre-shared key
# Server sends psk_i to one or more clients via secure out-of-band channel
```
**安全说明：** 如果需要，同一个 PSK（预共享密钥）可以在多个客户端之间共享（会创建“组”授权）。

#### 服务器端处理

```python
# Server generates new auth cookie and salt
authCookie = CSRNG(32)  # 32-byte cookie
authSalt = CSRNG(32)     # 32-byte salt

# For each authorized client i
for psk_i in authorized_clients:
    # Derive client-specific encryption key
    authInput = psk_i || subcredential || publishedTimestamp
    
    okm = HKDF(
        salt=authSalt,
        ikm=authInput,
        info="ELS2PSKA",  # Domain separation
        n=52  # 32 key + 12 IV + 8 ID
    )
    
    # Extract components
    clientKey_i = okm[0:31]    # 32 bytes
    clientIV_i = okm[32:43]    # 12 bytes
    clientID_i = okm[44:51]    # 8 bytes
    
    # Encrypt authCookie for this client
    clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
    
    # Store [clientID_i, clientCookie_i] entry in Layer 1
```
**第1层数据结构:**

```
authSalt (32 bytes)
clients (2 bytes) = N
[clientID_1 (8 bytes) || clientCookie_1 (32 bytes)]
[clientID_2 (8 bytes) || clientCookie_2 (32 bytes)]
...
[clientID_N (8 bytes) || clientCookie_N (32 bytes)]
```
#### 客户端处理

```python
# Client has: psk_i (their pre-shared key), destination, date, secret
# Client receives: encrypted LeaseSet with authSalt in Layer 1

# Derive expected client identifier and decryption key
authInput = psk_i || subcredential || publishedTimestamp

okm = HKDF(
    salt=authSalt,
    ikm=authInput,
    info="ELS2PSKA",
    n=52
)

clientKey_i = okm[0:31]    # 32 bytes
clientIV_i = okm[32:43]    # 12 bytes
clientID_i = okm[44:51]    # 8 bytes

# Search Layer 1 authorization data for clientID_i
for (clientID, clientCookie) in layer1_auth_entries:
    if clientID == clientID_i:
        # Found matching entry, decrypt authCookie
        authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie)
        # Use authCookie to decrypt Layer 2
        break
else:
    # No matching entry - client not authorized or revoked
    raise AuthorizationError("Client not authorized")
```
### 比较与建议

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">DH Authorization</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">PSK Authorization</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Key Exchange</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Asymmetric (X25519)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Symmetric (shared secret)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Security</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Higher (forward secrecy)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Lower (depends on PSK secrecy)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Client Privacy</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Private key never transmitted</td><td style="border:1px solid var(--color-border); padding:0.5rem;">PSK must be transmitted securely</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Performance</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">N+1 DH operations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">No DH operations</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Key Sharing</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">One key per client</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Can share key among multiple clients</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Revocation Detection</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Adversary cannot tell when revoked</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Adversary can track revocation if PSK intercepted</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Use Case</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">High security requirements</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Performance-critical or group access</td></tr>
  </tbody>
</table>
**建议：** - **使用 DH 授权** 适用于前向保密性重要的高安全性应用 - **使用 PSK 授权** 当性能至关重要或需要管理客户端分组时 - **切勿重复使用 PSK** 在不同服务或不同时期 - **始终使用安全信道** 进行密钥分发（例如 Signal、OTR、PGP）

### 安全注意事项

**客户端成员身份隐私:**

这两种机制通过以下方式为客户端成员身份提供隐私：
1. **加密的客户端标识符：** 8 字节的 clientID，源自 HKDF（基于 HMAC 的密钥派生函数）输出
2. **不可区分的 Cookie：** 所有 32 字节的 clientCookie 值看起来都是随机的
3. **没有特定于客户端的元数据：** 无法识别哪个条目属于哪个客户端

观察者可以看到：
- 授权客户端的数量（来自 `clients` 字段）
- 客户端数量随时间的变化

观察者无法看到： - 哪些具体客户端已被授权 - 具体客户端何时被添加或移除（如果数量保持不变） - 任何可用于识别客户端的信息

**随机化建议：**

服务器应当在每次生成加密的 LeaseSet 时随机化客户端顺序：

```python
import random

# Before serializing
auth_entries = [(clientID_i, clientCookie_i) for each client]
random.shuffle(auth_entries)
# Now serialize in randomized order
```
**优点：** - 防止客户端获知其在列表中的位置 - 防止基于位置变化的推断攻击 - 使客户端的新增/撤销不可区分

**隐藏客户端数量:**

服务器可以插入随机的伪条目：

```python
# Add dummy entries
num_dummies = random.randint(0, max_dummies)
for _ in range(num_dummies):
    dummy_id = CSRNG(8)
    dummy_cookie = CSRNG(32)
    auth_entries.append((dummy_id, dummy_cookie))

# Randomize all entries (real + dummy)
random.shuffle(auth_entries)
```
**成本：** 填充条目会增加加密的 LeaseSet 大小（每个 40 字节）。

**AuthCookie 轮换：**

服务器应当生成一个新的 authCookie（认证 Cookie）： - 每次发布加密的 LeaseSet 时（通常每隔数小时） - 在撤销某个客户端之后立即 - 按照固定计划（例如，每日），即使没有客户端发生变更

**优势:** - 在 authCookie 遭到泄露时，限制暴露 - 确保被撤销授权的客户端能快速失去访问权限 - 为第二层提供前向保密性

---

## 用于加密 LeaseSets 的 Base32 寻址

### 概述

传统的 I2P base32 地址仅包含 Destination（目的地标识）的哈希（32 字节 → 52 个字符）。这对于加密的 LeaseSets 来说是不足的，因为：

1. 客户端需要 **未盲化公钥** 才能派生出盲化公钥
2. 客户端需要 **签名类型**（unblinded 和 blinded，分别为未盲化与盲化），以便正确进行密钥派生
3. 仅凭哈希无法提供这些信息

**解决方案：** 包含公钥和签名类型的新 base32 格式。

### 地址格式规范

**解码后的结构（35 字节）：**

```
┌─────────────────────────────────────────────────────┐
│ Byte 0   │ Byte 1  │ Byte 2  │ Bytes 3-34          │
│ Flags    │ Unblind │ Blinded │ Public Key          │
│ (XOR)    │ SigType │ SigType │ (32 bytes)          │
│          │ (XOR)   │ (XOR)   │                     │
└─────────────────────────────────────────────────────┘
```
**前3个字节（与校验和进行异或）：**

前 3 个字节包含与 CRC-32 校验和的部分按位异或后的元数据：

```python
# Data structure before XOR
flags = 0x00           # 1 byte (reserved for future use)
unblinded_sigtype = 0x07 or 0x0b  # 1 byte (7 or 11)
blinded_sigtype = 0x0b  # 1 byte (always 11)

# Compute CRC-32 checksum of public key
checksum = crc32(pubkey)  # 4-byte CRC-32 of bytes 3-34

# XOR first 3 bytes with parts of checksum
data[0] = flags XOR (checksum >> 24) & 0xFF
data[1] = unblinded_sigtype XOR (checksum >> 16) & 0xFF  
data[2] = blinded_sigtype XOR (checksum >> 8) & 0xFF

# Bytes 3-34 contain the unmodified 32-byte public key
data[3:34] = pubkey
```
**校验和属性:** - 使用标准 CRC-32 多项式 - 假阴性率：约为 1600 万分之一 - 可检测地址拼写错误 - 不能用作认证（不具备密码学安全性）

**编码格式：**

```
Base32Encode(35 bytes) || ".b32.i2p"
```
**特性：** - 总字符数：56 (35 字节 × 8 位 ÷ 每字符 5 位) - 后缀: ".b32.i2p" (与传统 base32 相同) - 总长度：56 + 8 = 64 字符 (不包含空字符终止符)

**Base32 编码：** - 字母表: `abcdefghijklmnopqrstuvwxyz234567` (遵循 RFC 4648 标准) - 末尾未使用的 5 个位必须为 0 - 不区分大小写 (按惯例使用小写)

### 地址生成

```python
import struct
from zlib import crc32
import base64

def generate_encrypted_b32_address(pubkey, unblinded_sigtype, blinded_sigtype):
    """
    Generate base32 address for encrypted LeaseSet.
    
    Args:
        pubkey: 32-byte public key (bytes)
        unblinded_sigtype: Unblinded signature type (7 or 11)
        blinded_sigtype: Blinded signature type (always 11)
    
    Returns:
        String address ending in .b32.i2p
    """
    # Verify inputs
    assert len(pubkey) == 32, "Public key must be 32 bytes"
    assert unblinded_sigtype in [7, 11], "Unblinded sigtype must be 7 or 11"
    assert blinded_sigtype == 11, "Blinded sigtype must be 11"
    
    # Compute CRC-32 of public key
    checksum = crc32(pubkey) & 0xFFFFFFFF  # Ensure 32-bit unsigned
    
    # Prepare metadata bytes
    flags = 0x00
    
    # XOR metadata with checksum parts
    byte0 = flags ^ ((checksum >> 24) & 0xFF)
    byte1 = unblinded_sigtype ^ ((checksum >> 16) & 0xFF)
    byte2 = blinded_sigtype ^ ((checksum >> 8) & 0xFF)
    
    # Construct 35-byte data
    data = bytes([byte0, byte1, byte2]) + pubkey
    
    # Base32 encode (standard alphabet)
    # Python's base64 module uses uppercase by default
    b32 = base64.b32encode(data).decode('ascii').lower().rstrip('=')
    
    # Construct full address
    address = b32 + ".b32.i2p"
    
    return address
```
### 地址解析

```python
import struct
from zlib import crc32
import base64

def parse_encrypted_b32_address(address):
    """
    Parse base32 address for encrypted LeaseSet.
    
    Args:
        address: String address ending in .b32.i2p
    
    Returns:
        Tuple of (pubkey, unblinded_sigtype, blinded_sigtype)
    
    Raises:
        ValueError: If address is invalid or checksum fails
    """
    # Remove suffix
    if not address.endswith('.b32.i2p'):
        raise ValueError("Invalid address suffix")
    
    b32 = address[:-8]  # Remove ".b32.i2p"
    
    # Verify length (56 characters for 35 bytes)
    if len(b32) != 56:
        raise ValueError(f"Invalid length: {len(b32)} (expected 56)")
    
    # Base32 decode
    # Add padding if needed
    padding_needed = (8 - (len(b32) % 8)) % 8
    b32_padded = b32.upper() + '=' * padding_needed
    
    try:
        data = base64.b32decode(b32_padded)
    except Exception as e:
        raise ValueError(f"Invalid base32 encoding: {e}")
    
    # Verify decoded length
    if len(data) != 35:
        raise ValueError(f"Invalid decoded length: {len(data)} (expected 35)")
    
    # Extract public key
    pubkey = data[3:35]
    
    # Compute CRC-32 for verification
    checksum = crc32(pubkey) & 0xFFFFFFFF
    
    # Un-XOR metadata bytes
    flags = data[0] ^ ((checksum >> 24) & 0xFF)
    unblinded_sigtype = data[1] ^ ((checksum >> 16) & 0xFF)
    blinded_sigtype = data[2] ^ ((checksum >> 8) & 0xFF)
    
    # Verify expected values
    if flags != 0x00:
        raise ValueError(f"Invalid flags: {flags:#x} (expected 0x00)")
    
    if unblinded_sigtype not in [7, 11]:
        raise ValueError(f"Invalid unblinded sigtype: {unblinded_sigtype} (expected 7 or 11)")
    
    if blinded_sigtype != 11:
        raise ValueError(f"Invalid blinded sigtype: {blinded_sigtype} (expected 11)")
    
    return pubkey, unblinded_sigtype, blinded_sigtype
```
### 与传统 Base32 的比较

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Traditional B32</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Encrypted LS2 B32</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Content</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-256 hash of Destination</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Public key + signature types</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Decoded Size</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">35 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Encoded Length</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">52 characters</td><td style="border:1px solid var(--color-border); padding:0.5rem;">56 characters</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Suffix</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">.b32.i2p</td><td style="border:1px solid var(--color-border); padding:0.5rem;">.b32.i2p</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Total Length</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">60 chars</td><td style="border:1px solid var(--color-border); padding:0.5rem;">64 chars</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Checksum</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">None</td><td style="border:1px solid var(--color-border); padding:0.5rem;">CRC-32 (XOR'd into first 3 bytes)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Use Case</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Regular destinations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted LeaseSet destinations</td></tr>
  </tbody>
</table>
### 使用限制

**BitTorrent 不兼容性:**

加密的 LS2 地址不能用于 BitTorrent 的紧凑型 announce 响应：

```
Compact announce reply format:
┌────────────────────────────┐
│ 32-byte destination hash   │  ← Only hash, no signature types
│ 2-byte port                │
└────────────────────────────┘
```
**问题：**紧凑格式仅包含哈希（32 字节），没有为签名类型或公钥信息预留空间。

**解决方案：** 使用完整的 announce 响应，或使用支持完整地址的基于 HTTP 的 tracker。

### 地址簿集成

如果客户端在地址簿中包含完整的 Destination（I2P 目标标识）:

1. 存储完整的 Destination（I2P 的目标标识；包含公钥）
2. 支持通过哈希反向查找
3. 当遇到加密的 LS2（LeaseSet v2）时，从地址簿获取公钥
4. 如果已知完整的 Destination，则无需新的 base32 格式

**支持加密的 LS2（LeaseSet2，第二代 leaseSet）的地址簿格式：** - hosts.txt，包含完整的 destination 字符串 - SQLite 数据库，包含 destination 列 - JSON/XML 格式，包含完整的 destination 数据

### 实现示例

**示例 1：生成地址**

```python
# Ed25519 destination example
pubkey = bytes.fromhex('a' * 64)  # 32-byte public key
unblinded_type = 7   # Ed25519
blinded_type = 11    # Red25519 (always)

address = generate_encrypted_b32_address(pubkey, unblinded_type, blinded_type)
print(f"Address: {address}")
# Output: 56 base32 characters + .b32.i2p
```
**示例 2: 解析与验证**

```python
address = "abc...xyz.b32.i2p"  # 56 chars + suffix

try:
    pubkey, unblinded, blinded = parse_encrypted_b32_address(address)
    print(f"Public Key: {pubkey.hex()}")
    print(f"Unblinded SigType: {unblinded}")
    print(f"Blinded SigType: {blinded}")
except ValueError as e:
    print(f"Invalid address: {e}")
```
**示例 3：从 Destination（I2P 目的地标识）转换**

```python
def destination_to_encrypted_b32(destination):
    """
    Convert full Destination to encrypted LS2 base32 address.
    
    Args:
        destination: I2P Destination object
    
    Returns:
        Base32 address string
    """
    # Extract public key and signature type from destination
    pubkey = destination.signing_public_key  # 32 bytes
    sigtype = destination.sig_type  # 7 or 11
    
    # Blinded type is always 11 (Red25519)
    blinded_type = 11
    
    # Generate address
    return generate_encrypted_b32_address(pubkey, sigtype, blinded_type)
```
### 安全注意事项

**隐私：** - Base32 地址会暴露公钥 - 这是有意为之且是该协议的要求 - 不会泄露私钥，也不会危及安全性 - 公钥按设计就是公开信息

**抗碰撞性：** - CRC-32 仅提供 32 位的抗碰撞性 - 不具备密码学安全性（仅用于错误检测） - 切勿依赖校验和用于认证 - 仍然需要进行完整的目标验证

**地址验证：** - 在使用前务必验证校验和 - 拒绝具有无效签名类型的地址 - 验证公钥位于曲线上（取决于具体实现）

**参考资料：** - [提案 149：用于加密 LS2（LeaseSet 第2版）的 B32](/proposals/149-b32-encrypted-ls2/) - [B32 寻址规范](/docs/specs/b32-for-encrypted-leasesets/) - [I2P 命名规范](/docs/overview/naming/)

---

## 离线密钥支持

### 概述

离线密钥允许主签名密钥保持离线（冷存储），同时使用临时签名密钥处理日常操作。这对于高安全性的服务至关重要。

**加密的 LS2（LeaseSet v2）特定要求：** - 临时密钥必须离线生成 - 盲化私钥必须预先生成（每天一个） - 临时密钥和盲化密钥均按批次交付 - 尚未定义标准化的文件格式（规范中待补充）

### 离线密钥结构

**第 0 层临时密钥数据 (当标志位第 0 位为 1 时)：**

```
┌───────────────────────────────────────────────────┐
│ Expires Timestamp       │ 4 bytes (seconds)       │
│ Transient Sig Type      │ 2 bytes (big endian)    │
│ Transient Signing Pubkey│ Variable (sigtype len)  │
│ Signature (by blinded)  │ 64 bytes (Red25519)     │
└───────────────────────────────────────────────────┘
```
**签名覆盖范围：** 离线密钥块中的签名覆盖： - 到期时间戳(4 字节) - 临时签名类型(2 字节)   - 临时签名公钥(可变长度)

该签名使用**盲化公钥**进行验证，证明持有盲化私钥的实体已授权此临时密钥。

### 密钥生成过程

**对于使用离线密钥的加密 LeaseSet：**

1. **生成临时密钥对**（离线，在冷存储中）:
   ```python
   # For each day in future
   for date in future_dates:
       # Generate daily transient keypair
       transient_privkey = generate_red25519_privkey()  # Type 11
       transient_pubkey = derive_public(transient_privkey)

       # Store for later delivery
       keys[date] = (transient_privkey, transient_pubkey)
   ```

2. **Generate daily blinded keypairs** (offline, in cold storage):
   ```python
# 遍历每一天    for date in future_dates:

       # Derive alpha for this date
       datestring = date.strftime("%Y%m%d")  # "YYYYMMDD"
       alpha = GENERATE_ALPHA(destination, datestring, secret)
       
       # Blind the signing private key
       a = destination_signing_privkey  # Type 7 or 11
       blinded_privkey = BLIND_PRIVKEY(a, alpha)  # Result is type 11
       blinded_pubkey = DERIVE_PUBLIC(blinded_privkey)
       
       # Store for later delivery
       blinded_keys[date] = (blinded_privkey, blinded_pubkey)
   ```

3. **Sign transient keys with blinded keys** (offline):
   ```python
for date in future_dates:

       transient_pubkey = keys[date][1]
       blinded_privkey = blinded_keys[date][0]
       
       # Create signature data
       expires = int((date + timedelta(days=1)).timestamp())
       sig_data = struct.pack('>I', expires)  # 4 bytes
       sig_data += struct.pack('>H', 11)     # Transient type (Red25519)
       sig_data += transient_pubkey          # 32 bytes
       
       # Sign with blinded private key
       signature = RED25519_SIGN(blinded_privkey, sig_data)
       
       # Package for delivery
       offline_sig_blocks[date] = {
           'expires': expires,
           'transient_type': 11,
           'transient_pubkey': transient_pubkey,
           'signature': signature
       }
   ```

4. **Package for delivery to router:**
   ```python
# 针对每个日期    delivery_package[date] = {

       'transient_privkey': keys[date][0],
       'transient_pubkey': keys[date][1],
       'blinded_privkey': blinded_keys[date][0],
       'blinded_pubkey': blinded_keys[date][1],
       'offline_sig_block': offline_sig_blocks[date]
}

   ```

### Router Usage

**Daily Key Loading:**

```python
# 在 UTC 午夜（或在发布之前）

date = datetime.utcnow().date()

# 加载今天的密钥

today_keys = load_delivery_package(date)

transient_privkey = today_keys['transient_privkey'] transient_pubkey = today_keys['transient_pubkey'] blinded_privkey = today_keys['blinded_privkey'] blinded_pubkey = today_keys['blinded_pubkey'] offline_sig_block = today_keys['offline_sig_block']

# 将这些密钥用于今天的加密 LeaseSet

```

**Publishing Process:**

```python
# 1. 创建内部 LeaseSet2（I2P 中用于发布目的地接入信息的数据结构）

inner_ls2 = create_leaseset2(

    destinations, leases, expires, 
    signing_key=transient_privkey  # Use transient key
)

# 2. 加密第 2 层

layer2_ciphertext = encrypt_layer2(inner_ls2, authCookie, subcredential, timestamp)

# 3. 创建带有授权数据的第 1 层

layer1_plaintext = create_layer1(authorization_data, layer2_ciphertext)

# 4. 加密第 1 层

layer1_ciphertext = encrypt_layer1(layer1_plaintext, subcredential, timestamp)

# 5. 创建包含离线签名块的 Layer 0（第0层）

layer0 = create_layer0(

    blinded_pubkey,
    timestamp,
    expires,
    flags=0x0001,  # Bit 0 set (offline keys present)
    offline_sig_block=offline_sig_block,
    layer1_ciphertext=layer1_ciphertext
）

# 6. 使用临时私钥对第0层签名

signature = RED25519_SIGN(transient_privkey, layer0)

# 7. 附加签名并发布

encrypted_leaseset = layer0 + signature publish_to_netdb(encrypted_leaseset)

```

### Security Considerations

**Tracking via Offline Signature Block:**

The offline signature block is in plaintext (Layer 0). An adversary scraping floodfills could:
- Track the same encrypted LeaseSet across multiple days
- Correlate encrypted LeaseSets even though blinded keys change daily

**Mitigation:** Generate new transient keys daily (in addition to blinded keys):

```python
# 每天同时生成新的临时密钥和新的盲化密钥

for date in future_dates:

    # New transient keypair for this day
    transient_privkey = generate_red25519_privkey()
    transient_pubkey = derive_public(transient_privkey)
    
    # New blinded keypair for this day
    alpha = GENERATE_ALPHA(destination, datestring, secret)
    blinded_privkey = BLIND_PRIVKEY(signing_privkey, alpha)
    blinded_pubkey = DERIVE_PUBLIC(blinded_privkey)
    
    # Sign new transient key with new blinded key
    sig = RED25519_SIGN(blinded_privkey, transient_pubkey || metadata)
    
    # Now offline sig block changes daily
```

**Benefits:**
- Prevents tracking across days via offline signature block
- Provides same security as encrypted LS2 without offline keys
- Each day appears completely independent

**Cost:**
- More keys to generate and store
- More complex key management

### File Format (TODO)

**Current Status:** No standardized file format defined for batch key delivery.

**Requirements for Future Format:**

1. **Must support multiple dates:**
   - Batch delivery of 30+ days worth of keys
   - Clear date association for each key set

2. **Must include all necessary data:**
   - Transient private key
   - Transient public key
   - Blinded private key
   - Blinded public key
   - Pre-computed offline signature block
   - Expiration timestamps

3. **Should be tamper-evident:**
   - Checksums or signatures over entire file
   - Integrity verification before loading

4. **Should be encrypted:**
   - Keys are sensitive material
   - Encrypt file with router's key or passphrase

**Proposed Format Example (JSON, encrypted):**

```json
{   "version": 1,   "destination_hash": "base64...",   "keys": [

    {
      "date": "2025-10-15",
      "transient": {
        "type": 11,
        "privkey": "base64...",
        "pubkey": "base64..."
      },
      "blinded": {
        "privkey": "base64...",
        "pubkey": "base64..."
      },
      "offline_sig_block": {
        "expires": 1729123200,
        "signature": "base64..."
      }
    }
],   "signature": "base64..."  // Signature over entire structure }

```

### I2CP Protocol Enhancement (TODO)

**Current Status:** No I2CP protocol enhancement defined for offline keys with encrypted LeaseSet.

**Requirements:**

1. **Key delivery mechanism:**
   - Upload batch of keys from client to router
   - Acknowledgment of successful key loading

2. **Key expiration notification:**
   - Router notifies client when keys running low
   - Client can generate and upload new batch

3. **Key revocation:**
   - Emergency revocation of future keys if compromise suspected

**Proposed I2CP Messages:**

```
UPLOAD_OFFLINE_KEYS   - 一批加密的密钥材料   - 涵盖的日期范围

OFFLINE_KEY_STATUS   - 剩余天数   - 下一个密钥到期日期

REVOKE_OFFLINE_KEYS     - 要吊销的日期范围   - 用于替换的新密钥 (可选)

```

### Implementation Status

**Java I2P:**
- ✅ Offline keys for standard LS2: Fully supported (since 0.9.38)
- ⚠️ Offline keys for encrypted LS2: Implemented (since 0.9.40)
- ❌ File format: Not standardized
- ❌ I2CP protocol: Not enhanced

**i2pd (C++):**
- ✅ Offline keys for standard LS2: Fully supported
- ✅ Offline keys for encrypted LS2: Fully supported (since 2.58.0)
- ❌ File format: Not standardized
- ❌ I2CP protocol: Not enhanced

**References:**
- [Offline Signatures Proposal](/proposals/123-new-netdb-entries/)
- [I2CP Specification](/docs/specs/i2cp/)

---

## Security Considerations

### Cryptographic Security

**Algorithm Selection:**

All cryptographic primitives are based on well-studied algorithms:
- **ChaCha20:** Modern stream cipher, constant-time, no timing attacks
- **SHA-256:** NIST-approved hash, 128-bit security level
- **HKDF:** RFC 5869 standard, proven security bounds
- **Ed25519/Red25519:** Curve25519-based, ~128-bit security level
- **X25519:** Diffie-Hellman over Curve25519, ~128-bit security level

**Key Sizes:**
- All symmetric keys: 256 bits (32 bytes)
- All public/private keys: 256 bits (32 bytes)
- All nonces/IVs: 96 bits (12 bytes)
- All signatures: 512 bits (64 bytes)

These sizes provide adequate security margins against current and near-future attacks.

### Forward Secrecy

**Daily Key Rotation:**

Encrypted LeaseSets rotate keys daily (UTC midnight):
- New blinded public/private key pair
- New storage location in DHT
- New encryption keys for both layers

**Benefits:**
- Compromising today's blinded key doesn't reveal yesterday's
- Limits exposure window to 24 hours
- Prevents long-term tracking via DHT

**Enhanced with Ephemeral Keys:**

DH client authorization uses ephemeral keys:
- Server generates new ephemeral DH keypair for each publication
- Compromising ephemeral key only affects that publication
- True forward secrecy even if long-term keys compromised

### Privacy Properties

**Destination Blinding:**

The blinded public key:
- Is unlinkable to the original destination (without knowing the secret)
- Changes daily, preventing long-term correlation
- Cannot be reversed to find the original public key

**Client Membership Privacy:**

Per-client authorization provides:
- **Anonymity:** No way to identify which clients are authorized
- **Untraceability:** Cannot track when specific clients added/revoked
- **Size obfuscation:** Can add dummy entries to hide true count

**DHT Privacy:**

Storage location rotates daily:
```
location = SHA-256(sig_type || blinded_public_key)

```

This prevents:
- Correlation across days via DHT lookups
- Long-term monitoring of service availability
- Traffic analysis of DHT queries

### Threat Model

**Adversary Capabilities:**

1. **Network Adversary:**
   - Can monitor all DHT traffic
   - Can observe encrypted LeaseSet publications
   - Cannot decrypt without proper keys

2. **Floodfill Adversary:**
   - Can store and analyze all encrypted LeaseSets
   - Can track publication patterns over time
   - Cannot decrypt Layer 1 or Layer 2
   - Can see client count (but not identities)

3. **Authorized Client Adversary:**
   - Can decrypt specific encrypted LeaseSets
   - Can access inner LeaseSet2 data
   - Cannot determine other clients' identities
   - Cannot decrypt past LeaseSets (with ephemeral keys)

**Out of Scope:**

- Malicious router implementations
- Compromised router host systems
- Side-channel attacks (timing, power analysis)
- Physical access to keys
- Social engineering attacks

### Attack Scenarios

**1. Offline Keys Tracking Attack:**

**Attack:** Adversary tracks encrypted LeaseSets via unchanging offline signature block.

**Mitigation:** Generate new transient keys daily (in addition to blinded keys).

**Status:** Documented recommendation, implementation-specific.

**2. Client Position Inference Attack:**

**Attack:** If client order is static, clients can infer their position and detect when other clients added/removed.

**Mitigation:** Randomize client order in authorization list for each publication.

**Status:** Documented recommendation in specification.

**3. Client Count Analysis Attack:**

**Attack:** Adversary monitors client count changes over time to infer service popularity or client churn.

**Mitigation:** Add random dummy entries to authorization list.

**Status:** Optional feature, deployment-specific trade-off (size vs. privacy).

**4. PSK Interception Attack:**

**Attack:** Adversary intercepts PSK during out-of-band exchange and can decrypt all future encrypted LeaseSets.

**Mitigation:** Use DH client authorization instead, or ensure secure key exchange (Signal, OTR, PGP).

**Status:** Known limitation of PSK approach, documented in specification.

**5. Timing Correlation Attack:**

**Attack:** Adversary correlates publication times across days to link encrypted LeaseSets.

**Mitigation:** Randomize publication times, use delayed publishing.

**Status:** Implementation-specific, not addressed in core specification.

**6. Long-term Secret Compromise:**

**Attack:** Adversary compromises the blinding secret and can compute all past and future blinded keys.

**Mitigation:** 
- Use optional secret parameter (not empty)
- Rotate secret periodically
- Use different secrets for different services

**Status:** Secret parameter is optional; using it is highly recommended.

### Operational Security

**Key Management:**

1. **Signing Private Key:**
   - Store offline in cold storage
   - Use only for generating blinded keys (batch process)
   - Never expose to online router

2. **Blinded Private Keys:**
   - Generate offline, deliver in batches
   - Rotate daily automatically
   - Delete after use (forward secrecy)

3. **Transient Private Keys (with offline keys):**
   - Generate offline, deliver in batches
   - Can be longer-lived (days/weeks)
   - Rotate regularly for enhanced privacy

4. **Client Authorization Keys:**
   - DH: Client private keys never leave client device
   - PSK: Use unique keys per client, secure exchange
   - Revoke immediately upon client removal

**Secret Management:**

The optional secret parameter in `GENERATE_ALPHA`:
- SHOULD be used for high-security services
- MUST be transmitted securely to authorized clients
- SHOULD be rotated periodically (e.g., monthly)
- CAN be different for different client groups

**Monitoring and Auditing:**

1. **Publication Monitoring:**
   - Verify encrypted LeaseSets published successfully
   - Monitor floodfill acceptance rates
   - Alert on publication failures

2. **Client Access Monitoring:**
   - Log client authorization attempts (without identifying clients)
   - Monitor for unusual patterns
   - Detect potential attacks early

3. **Key Rotation Auditing:**
   - Verify daily key rotation occurs
   - Check blinded key changes daily
   - Ensure old keys are deleted

### Implementation Security

**Constant-Time Operations:**

Implementations MUST use constant-time operations for:
- All scalar arithmetic (mod L operations)
- Private key comparisons
- Signature verification
- DH key agreement

**Memory Security:**

- Zero sensitive key material after use
- Use secure memory allocation for keys
- Prevent keys from being paged to disk
- Clear stack variables containing key material

**Random Number Generation:**

- Use cryptographically secure RNG (CSRNG)
- Properly seed RNG from OS entropy source
- Do not use predictable RNGs for key material
- Verify RNG output quality periodically

**Input Validation:**

- Validate all public keys are on the curve
- Check all signature types are supported
- Verify all lengths before parsing
- Reject malformed encrypted LeaseSets early

**Error Handling:**

- Do not leak information via error messages
- Use constant-time comparison for authentication
- Do not expose timing differences in decryption
- Log security-relevant events properly

### Recommendations

**For Service Operators:**

1. ✅ **Use Red25519 (type 11)** for new destinations
2. ✅ **Use DH client authorization** for high-security services
3. ✅ **Generate new transient keys daily** when using offline keys
4. ✅ **Use the optional secret parameter** in GENERATE_ALPHA
5. ✅ **Randomize client order** in authorization lists
6. ✅ **Monitor publication success** and investigate failures
7. ⚠️ **Consider dummy entries** to hide client count (size trade-off)

**For Client Implementers:**

1. ✅ **Validate blinded public keys** are on prime-order subgroup
2. ✅ **Verify all signatures** before trusting data
3. ✅ **Use constant-time operations** for cryptographic primitives
4. ✅ **Zero key material** immediately after use
5. ✅ **Implement proper error handling** without information leaks
6. ✅ **Support both Ed25519 and Red25519** destination types

**For Network Operators:**

1. ✅ **Accept encrypted LeaseSets** in floodfill routers
2. ✅ **Enforce reasonable size limits** to prevent abuse
3. ✅ **Monitor for anomalous patterns** (extremely large, frequent updates)
4. ⚠️ **Consider rate limiting** encrypted LeaseSet publications

---

## Implementation Notes

### Java I2P Implementation

**Repository:** https://github.com/i2p/i2p.i2p

**Key Classes:**
- `net.i2p.data.LeaseSet2` - LeaseSet2 structure
- `net.i2p.data.EncryptedLeaseSet` - Encrypted LS2 implementation
- `net.i2p.crypto.eddsa.EdDSAEngine` - Ed25519/Red25519 signatures
- `net.i2p.crypto.HKDF` - HKDF implementation
- `net.i2p.crypto.ChaCha20` - ChaCha20 cipher

**Configuration:**

Enable encrypted LeaseSet in `clients.config`:
```properties
# 启用加密的 LeaseSet

i2cp.encryptLeaseSet=true

# 可选：启用客户端授权

i2cp.enableAccessList=true

# 可选：使用 DH（Diffie-Hellman）授权（默认为 PSK（预共享密钥））

i2cp.accessListType=0

# 可选：盲化密钥（强烈推荐）

i2cp.blindingSecret=your-secret-here

```

**API Usage Example:**

```java
// 创建加密的 LeaseSet EncryptedLeaseSet els = new EncryptedLeaseSet();

// 设置目标 els.setDestination(destination);

// 启用按客户端授权 els.setAuthorizationEnabled(true); els.setAuthType(EncryptedLeaseSet.AUTH_DH);

// 添加已授权客户端（DH（Diffie-Hellman）公钥） for (byte[] clientPubKey : authorizedClients) {

    els.addClient(clientPubKey);
}

// 设置盲化参数 els.setBlindingSecret("your-secret");

// 签名并发布 els.sign(signingPrivateKey); netDb.publish(els);

```

### i2pd (C++) Implementation

**Repository:** https://github.com/PurpleI2P/i2pd

**Key Files:**
- `libi2pd/LeaseSet.h/cpp` - LeaseSet implementations
- `libi2pd/Crypto.h/cpp` - Cryptographic primitives
- `libi2pd/Ed25519.h/cpp` - Ed25519/Red25519 signatures
- `libi2pd/ChaCha20.h/cpp` - ChaCha20 cipher

**Configuration:**

Enable in tunnel configuration (`tunnels.conf`):
```ini
[my-hidden-service] type = http host = 127.0.0.1 port = 8080 keys = my-service-keys.dat

# 启用加密的 LeaseSet（租约集合）

encryptleaseset = true

# 可选：客户端授权类型 (0=DH, 1=PSK)

authtype = 0

# 可选：盲化秘密

secret = your-secret-here

# 可选：已授权的客户端（每行一个，公钥为 base64 编码）

client.1 = base64-编码的-客户端-公钥-1 client.2 = base64-编码的-客户端-公钥-2

```

**API Usage Example:**

```cpp
// 创建加密的 LeaseSet auto encryptedLS = std::make_shared<i2p::data::EncryptedLeaseSet>(

    destination,
    blindingSecret
);

// 启用按客户端授权 encryptedLS->SetAuthType(i2p::data::AUTH_TYPE_DH);

// 添加已授权客户端 for (const auto& clientPubKey : authorizedClients) {

    encryptedLS->AddClient(clientPubKey);
}

// 签名并发布 encryptedLS->Sign(signingPrivKey); netdb.Publish(encryptedLS);

```

### Testing and Debugging

**Test Vectors:**

Generate test vectors for implementation verification:

```python
# 测试向量 1：密钥盲化

destination_pubkey = bytes.fromhex('a' * 64) sigtype = 7 blinded_sigtype = 11 date = "20251015" secret = ""

alpha = generate_alpha(destination_pubkey, sigtype, blinded_sigtype, date, secret) print(f"Alpha: {alpha.hex()}")

# 预期: (对照参考实现进行验证)

```

**Unit Tests:**

Key areas to test:
1. HKDF derivation with various inputs
2. ChaCha20 encryption/decryption
3. Red25519 signature generation and verification
4. Key blinding (private and public)
5. Layer 1/2 encryption/decryption
6. Client authorization (DH and PSK)
7. Base32 address generation and parsing

**Integration Tests:**

1. Publish encrypted LeaseSet to test network
2. Retrieve and decrypt from client
3. Verify daily key rotation
4. Test client authorization (add/remove clients)
5. Test offline keys (if supported)

**Common Implementation Errors:**

1. **Incorrect mod L reduction:** Must use proper modular arithmetic
2. **Endianness errors:** Most fields are big-endian, but some crypto uses little-endian
3. **Off-by-one in array slicing:** Verify indices are inclusive/exclusive as needed
4. **Missing constant-time comparisons:** Use constant-time for all sensitive comparisons
5. **Not zeroing key material:** Always zero keys after use

### Performance Considerations

**Computational Costs:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Cost</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Key blinding (server)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 scalar mult</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per publication</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Key blinding (client)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 point add + 1 scalar mult</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per retrieval</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Layer 1 encryption</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 HKDF + 1 ChaCha20</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Fast</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Layer 2 encryption</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 HKDF + 1 ChaCha20</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Fast</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DH client auth (server)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">N+1 X25519 ops</td><td style="border:1px solid var(--color-border); padding:0.5rem;">N = number of clients</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DH client auth (client)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 X25519 op</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per retrieval</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">PSK client auth</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0 DH ops</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Only HKDF + ChaCha20</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature (Red25519)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 signature op</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Similar cost to Ed25519</td></tr>
  </tbody>
</table>

**Size Overhead:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Component</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Frequency</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded public key</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Layer 1 encryption overhead</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes (salt)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Layer 2 encryption overhead</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes (salt)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DH auth per client</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per client per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DH ephemeral pubkey</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet (if DH auth)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">PSK auth per client</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per client per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">PSK salt</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet (if PSK auth)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature</td><td style="border:1px solid var(--color-border); padding:0.5rem;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline sig block</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈100 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet (if offline keys)</td></tr>
  </tbody>
</table>

**Typical Sizes:**

- **No client auth:** ~200 bytes overhead
- **With 10 DH clients:** ~600 bytes overhead
- **With 100 DH clients:** ~4200 bytes overhead

**Optimization Tips:**

1. **Batch key generation:** Generate blinded keys for multiple days in advance
2. **Cache subcredentials:** Compute once per day, reuse for all publications
3. **Reuse ephemeral keys:** Can reuse ephemeral DH key for short period (minutes)
4. **Parallel client encryption:** Encrypt client cookies in parallel
5. **Fast path for no auth:** Skip authorization layer entirely when disabled

### Compatibility

**Backward Compatibility:**

- Ed25519 (type 7) destinations supported for unblinded keys
- Red25519 (type 11) required for blinded keys
- Traditional LeaseSets still fully supported
- Encrypted LeaseSets do not break existing network

**Forward Compatibility:**

- Reserved flag bits for future features
- Extensible authorization scheme (3 bits allow 8 types)
- Version field in various structures

**Interoperability:**

- Java I2P and i2pd fully interoperable since:
  - Java I2P 0.9.40 (May 2019)
  - i2pd 2.58.0 (September 2025)
- Encrypted LeaseSets work across implementations
- Client authorization works across implementations

---

## References

### IETF RFCs

- **[RFC 2104](https://datatracker.ietf.org/doc/html/rfc2104)** - HMAC: Keyed-Hashing for Message Authentication (February 1997)
- **[RFC 5869](https://datatracker.ietf.org/doc/html/rfc5869)** - HMAC-based Extract-and-Expand Key Derivation Function (HKDF) (May 2010)
- **[RFC 7539](https://datatracker.ietf.org/doc/html/rfc7539)** - ChaCha20 and Poly1305 for IETF Protocols (May 2015)
- **[RFC 7748](https://datatracker.ietf.org/doc/html/rfc7748)** - Elliptic Curves for Security (January 2016)

### I2P Specifications

- **[Common Structures Specification](/docs/specs/common-structures/)** - LeaseSet2 and EncryptedLeaseSet structures
- **[Proposal 123: New netDB Entries](/proposals/123-new-netdb-entries/)** - Background and design of LeaseSet2
- **[Proposal 146: Red25519](/proposals/146-red25519/)** - Red25519 signature scheme specification
- **[Proposal 149: B32 for Encrypted LS2](/proposals/149-b32-encrypted-ls2/)** - Base32 addressing for encrypted LeaseSets
- **[Red25519 Specification](/docs/specs/red25519-signature-scheme/)** - Detailed Red25519 implementation
- **[B32 Addressing Specification](/docs/specs/b32-for-encrypted-leasesets/)** - Base32 address format
- **[Network Database Documentation](/docs/specs/common-structures/)** - NetDB usage and operations
- **[I2CP Specification](/docs/specs/i2cp/)** - I2P Client Protocol

### Cryptographic References

- **[Ed25519 Paper](http://cr.yp.to/papers.html#ed25519)** - "High-speed high-security signatures" by Bernstein et al.
- **[ZCash Protocol Specification](https://zips.z.cash/protocol/protocol.pdf)** - Section 5.4.6: RedDSA signature scheme
- **[Tor Rendezvous Specification v3](https://spec.torproject.org/rend-spec)** - Tor's onion service specification (for comparison)

### Security References

- **[Key Blinding Security Discussion](https://lists.torproject.org/pipermail/tor-dev/2013-December/005943.html)** - Tor Project mailing list discussion
- **[Tor Ticket #8106](https://trac.torproject.org/projects/tor/ticket/8106)** - Key blinding implementation discussion
- **[PRNG Security](http://projectbullrun.org/dual-ec/ext-rand.html)** - Random number generator security considerations
- **[Tor PRNG Discussion](https://lists.torproject.org/pipermail/tor-dev/2015-November/009954.html)** - Discussion of PRNG usage in Tor

### Implementation References

- **[Java I2P Repository](https://github.com/i2p/i2p.i2p)** - Official Java implementation
- **[i2pd Repository](https://github.com/PurpleI2P/i2pd)** - C++ implementation
- **[I2P Website](/)** - Official I2P project website
- **[I2P Specifications](/docs/specs/)** - Complete specification index

### Version History

- **[I2P Release Notes](/en/blog)** - Official release announcements
- **[Java I2P Releases](https://github.com/i2p/i2p.i2p/releases)** - GitHub release history
- **[i2pd Releases](https://github.com/PurpleI2P/i2pd/releases)** - GitHub release history

---

## Appendix A: Cryptographic Constants

### Ed25519 / Red25519 Constants

```python
# Ed25519（椭圆曲线数字签名算法）基点（生成元）

B = 2**255 - 19

# Ed25519 群阶（标量域大小）

L = 2**252 + 27742317777372353535851937790883648493

# 签名类型值

SIGTYPE_ED25519 = 7    # 0x0007 SIGTYPE_RED25519 = 11  # 0x000b

# 密钥长度

PRIVKEY_SIZE = 32  # bytes PUBKEY_SIZE = 32   # bytes SIGNATURE_SIZE = 64  # bytes

```

### ChaCha20 Constants

```python
# ChaCha20 参数

CHACHA20_KEY_SIZE = 32   # 字节（256 位） CHACHA20_NONCE_SIZE = 12  # 字节（96 位） CHACHA20_INITIAL_COUNTER = 1  # RFC 7539 允许 0 或 1

```

### HKDF Constants

```python
# HKDF 参数

HKDF_HASH = "SHA-256" HKDF_SALT_MAX = 32  # 字节（HashLen）

# HKDF 的 info 字符串（域分离）

HKDF_INFO_ALPHA = b"i2pblinding1" HKDF_INFO_LAYER1 = b"ELS2_L1K" HKDF_INFO_LAYER2 = b"ELS2_L2K" HKDF_INFO_DH_AUTH = b"ELS2_XCA" HKDF_INFO_PSK_AUTH = b"ELS2PSKA"

```

### Hash Personalization Strings

```python
# SHA-256 个性化字符串

HASH_PERS_ALPHA = b"I2PGenerateAlpha" HASH_PERS_RED25519 = b"I2P_Red25519H(x)" HASH_PERS_CREDENTIAL = b"credential" HASH_PERS_SUBCREDENTIAL = b"subcredential"

```

### Structure Sizes

```python
# 第0层（外层）大小

BLINDED_SIGTYPE_SIZE = 2   # 字节 BLINDED_PUBKEY_SIZE = 32   # 字节（用于 Red25519） PUBLISHED_TS_SIZE = 4      # 字节 EXPIRES_SIZE = 2           # 字节 FLAGS_SIZE = 2             # 字节 LEN_OUTER_CIPHER_SIZE = 2  # 字节 SIGNATURE_SIZE = 64        # 字节（Red25519）

# 离线密钥块大小

OFFLINE_EXPIRES_SIZE = 4   # 字节 OFFLINE_SIGTYPE_SIZE = 2   # 字节 OFFLINE_SIGNATURE_SIZE = 64  # 字节

# 第 1 层 (中间) 大小

AUTH_FLAGS_SIZE = 1        # 字节 EPHEMERAL_PUBKEY_SIZE = 32  # 字节 (DH 认证) AUTH_SALT_SIZE = 32        # 字节 (PSK 认证) NUM_CLIENTS_SIZE = 2       # 字节 CLIENT_ID_SIZE = 8         # 字节 CLIENT_COOKIE_SIZE = 32    # 字节 AUTH_CLIENT_ENTRY_SIZE = 40  # 字节 (CLIENT_ID + CLIENT_COOKIE)

# 加密开销

SALT_SIZE = 32  # 字节（前置于每个加密层之前）

# Base32 地址

B32_ENCRYPTED_DECODED_SIZE = 35  # 字节 B32_ENCRYPTED_ENCODED_LEN = 56   # 字符 B32_SUFFIX = ".b32.i2p"

```

---

## Appendix B: Test Vectors

### Test Vector 1: Alpha Generation

**Input:**
```python
# 目的地公钥（Ed25519）

A = bytes.fromhex('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa') stA = 0x0007  # Ed25519 stA_prime = 0x000b  # Red25519 date = "20251015" secret = ""  # 空的秘密

```

**Computation:**
```python
keydata = A || bytes([0x00, 0x07]) || bytes([0x00, 0x0b])

# keydata = 36 字节

salt = SHA256(b"I2PGenerateAlpha" + keydata) ikm = b"20251015" info = b"i2pblinding1"

seed = HKDF(salt, ikm, info, 64) alpha = LEOS2IP(seed) mod L

```

**Expected Output:**
```
(与参考实现比对) alpha = [64 字节十六进制值]

```

### Test Vector 2: ChaCha20 Encryption

**Input:**
```python
key = bytes([i for i in range(32)])  # 0x00..0x1f nonce = bytes([i for i in range(12)])  # 0x00..0x0b plaintext = b"Hello, I2P!"

```

**Computation:**
```python
ciphertext = ChaCha20_Encrypt(key, nonce, plaintext, counter=1)

```

**Expected Output:**
```
ciphertext = [与 RFC 7539 测试向量比对验证]

```

### Test Vector 3: HKDF

**Input:**
```python
salt = bytes(32)  # 全零 ikm = b"test input keying material" info = b"ELS2_L1K" n = 44

```

**Computation:**
```python
keys = HKDF(salt, ikm, info, n)

```

**Expected Output:**
```
keys = [44字节的十六进制值]

```

### Test Vector 4: Base32 Address

**Input:**
```python
pubkey = bytes.fromhex('bbbb' + 'bb' * 30)  # 32 字节 unblinded_sigtype = 11  # Red25519 blinded_sigtype = 11    # Red25519

```

**Computation:**
```python
address = generate_encrypted_b32_address(pubkey, unblinded_sigtype, blinded_sigtype)

```

**Expected Output:**
```
address = [56 个 base32 字符].b32.i2p

# 确认校验和验证能正确通过

```

---

## Appendix C: Glossary

**Alpha (α):** The secret blinding factor used to blind public and private keys. Generated from the destination, date, and optional secret.

**AuthCookie:** A 32-byte random value encrypted for each authorized client, used as input to Layer 2 encryption.

**B (Base Point):** The generator point for the Ed25519 elliptic curve.

**Blinded Key:** A public or private key that has been transformed using the alpha blinding factor. Blinded keys cannot be linked to the original keys without knowing alpha.

**ChaCha20:** A stream cipher providing fast, secure encryption without requiring AES hardware support.

**ClientID:** An 8-byte identifier derived from HKDF output, used to identify authorization entries for clients.

**ClientCookie:** A 32-byte encrypted value containing the authCookie for a specific client.

**Credential:** A 32-byte value derived from the destination's public key and signature types, binding encryption to knowledge of the destination.

**CSRNG:** Cryptographically Secure Random Number Generator. Must provide unpredictable output suitable for key generation.

**DH (Diffie-Hellman):** A cryptographic protocol for securely establishing shared secrets. I2P uses X25519.

**Ed25519:** An elliptic curve signature scheme providing fast signatures with 128-bit security level.

**Ephemeral Key:** A short-lived cryptographic key, typically used once and then discarded.

**Floodfill:** I2P routers that store and serve network database entries, including encrypted LeaseSets.

**HKDF:** HMAC-based Key Derivation Function, used to derive multiple cryptographic keys from a single source.

**L (Order):** The order of the Ed25519 scalar field (approximately 2^252).

**Layer 0 (Outer):** The plaintext portion of an encrypted LeaseSet, containing blinded key and metadata.

**Layer 1 (Middle):** The first encrypted layer, containing client authorization data.

**Layer 2 (Inner):** The innermost encrypted layer, containing the actual LeaseSet2 data.

**LeaseSet2 (LS2):** Second version of I2P's network database entry format, introducing encrypted variants.

**NetDB:** The I2P network database, a distributed hash table storing router and destination information.

**Offline Keys:** A feature allowing the main signing key to remain in cold storage while a transient key handles daily operations.

**PSK (Pre-Shared Key):** A symmetric key shared in advance between two parties, used for PSK client authorization.

**Red25519:** An Ed25519-based signature scheme with key blinding support, based on ZCash RedDSA.

**Salt:** Random data used as input to key derivation functions to ensure unique outputs.

**SigType:** A numeric identifier for signature algorithms (e.g., 7 = Ed25519, 11 = Red25519).

**Subcredential:** A 32-byte value derived from the credential and blinded public key, binding encryption to a specific encrypted LeaseSet.

**Transient Key:** A temporary signing key used with offline keys, with a limited validity period.

**X25519:** An elliptic curve Diffie-Hellman protocol over Curve25519, providing key agreement.

---

## Document Information

**Status:** This document represents the current stable encrypted LeaseSet specification as implemented in I2P since June 2019. The protocol is mature and widely deployed.

**Contributing:** For corrections or improvements to this documentation, please submit issues or pull requests to the I2P specifications repository.

**Support:** For questions about implementing encrypted LeaseSets:
- I2P Forum: https://i2pforum.net/
- IRC: #i2p-dev on OFTC
- Matrix: #i2p-dev:matrix.org

**Acknowledgments:** This specification builds on work by the I2P development team, ZCash cryptography research, and Tor Project's key blinding research.