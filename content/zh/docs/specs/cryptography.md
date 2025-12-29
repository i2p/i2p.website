---
title: "底层密码学"
description: "在整个 I2P 中使用的对称、非对称和签名密码学原语概述"
slug: "cryptography"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "needs-review"
---

> **状态：** 本页精炼汇总了遗留的“Low-level Cryptography Specification”。较新的 I2P 发行版（2.10.0，2025年10月）已完成向新的密码学原语的迁移。实现细节请参阅以下专项规范：[ECIES](/docs/specs/ecies/)、[Encrypted LeaseSets](/docs/specs/encryptedleaseset/)、[NTCP2](/docs/specs/ntcp2/)、[Red25519](/docs/specs/red25519-signature-scheme/)、[SSU2](/docs/specs/ssu2/)，以及 [Tunnel Creation (ECIES)](/docs/specs/implementation/)。

## 演进快照

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Functional Area</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Legacy Primitive</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Current / Planned Primitive</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Migration Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Transport key exchange</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Diffie–Hellman over 2048-bit prime (NTCP / SSU)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519 (NTCP2 / SSU2)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Completed (NTCP2 and SSU2 fully deployed)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">End-to-end encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ElGamal/AES+SessionTags</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECIES-X25519-AEAD-Ratchet</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Completed (2.4.0+)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Symmetric cipher</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256/CBC + HMAC-MD5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20/Poly1305 (AEAD)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Active (tunnel layer remains AES-256)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default signatures</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DSA-SHA1 (1024-bit)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA/RedDSA on Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fully migrated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Experimental / future</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Hybrid post-quantum encryption (opt-in)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">In testing (2.10.0)</td>
    </tr>
  </tbody>
  
</table>
## 非对称加密

### X25519（基于 Curve25519 的椭圆曲线密钥交换算法）

- 用于 NTCP2、ECIES-X25519-AEAD-Ratchet、SSU2 以及基于 X25519 的 tunnel 创建。  
- 通过 Noise 协议框架提供紧凑的密钥、常数时间操作和前向保密。  
- 使用 32 字节密钥提供 128 位安全性，并具备高效的密钥交换。

### ElGamal（旧版）

- 为与较旧的 routers 向后兼容而保留。  
- 基于 2048 位 Oakley Group 14 素数模数（RFC 3526），生成元 2。  
- 将 AES 会话密钥和 IV（初始化向量）加密为 514 字节的密文。  
- 缺乏认证加密和前向保密；所有现代端点都已迁移到 ECIES（椭圆曲线集成加密方案）。

## 对称加密

### ChaCha20/Poly1305（由 ChaCha20 流密码与 Poly1305 消息认证码组合的认证加密算法）

- 在 NTCP2、SSU2 和 ECIES 中默认使用的认证加密原语。  
- 提供 AEAD 安全性，并且在没有 AES 硬件支持的情况下也能保持高性能。  
- 依据 RFC 7539 实现（256‑bit 密钥，96‑bit 随机数，128‑bit 认证标签）。

### AES‑256/CBC（旧版）

- 仍用于 tunnel 层加密，其分组密码结构契合 I2P 的分层加密模型。  
- 使用 PKCS#5 填充和逐跳 IV（初始向量）变换。  
- 已纳入长期审查计划，但在密码学上仍然可靠。

## 签名

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Signature Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage Notes</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DSA‑SHA1 (1024‑bit)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Original default; still accepted for legacy Destinations.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA‑SHA256/384/512</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Used during 2014–2015 transition.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA‑SHA512‑Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default for Router and Destination identities (since 0.9.15).</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RedDSA‑SHA512‑Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Used for encrypted LeaseSet signatures (0.9.39+).</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Specialized</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA‑SHA512‑4096</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For out‑of‑band signing (su3 updates, reseeds, plugins).</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Application‑layer</td>
    </tr>
  </tbody>
</table>
## 哈希与密钥派生

- **SHA‑256:** 用于 DHT（分布式哈希表）密钥、HKDF（基于 HMAC 的密钥派生函数）以及旧版签名。  
- **SHA‑512:** 由 EdDSA/RedDSA（基于 Edwards 曲线的数字签名算法/RedDSA）使用，并用于 Noise（协议框架）HKDF 推导中。  
- **HKDF‑SHA256:** 在 ECIES（椭圆曲线集成加密方案）、NTCP2 和 SSU2 中派生会话密钥。  
- 按日轮换的 SHA‑256 派生用于保护 netDb 中 RouterInfo 和 LeaseSet 的存储位置。

## 传输层摘要

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Transport</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Key Exchange</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Encryption</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Authentication</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NTCP2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20/Poly1305</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AEAD</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default TCP transport</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SSU2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20/Poly1305</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AEAD</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default UDP transport</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SSU (Legacy)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DH‑2048</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES‑256/CBC + HMAC‑MD5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Legacy</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Removed (2.4.0)</td>
    </tr>
  </tbody>
</table>
两种传输协议均提供链路级前向保密和重放防护，并使用 Noise_XK 握手模式（Noise 协议框架中的 XK 模式）。

## Tunnel 层加密

- 继续使用 AES‑256/CBC 进行逐跳分层加密。  
- 出站网关执行迭代的 AES 解密；每一跳使用其层密钥和 IV（初始化向量）密钥重新加密。  
- 双 IV 加密可缓解关联与确认攻击。  
- 正在研究迁移到 AEAD，但目前尚无计划。

## 后量子密码学

- I2P 2.10.0 引入了**实验性的混合式后量子加密**。  
- 可通过 Hidden Service Manager（隐藏服务管理器）手动启用以进行测试。  
- 将 X25519 与抗量子 KEM（密钥封装机制）相结合（混合模式）。  
- 默认未启用；用于研究与性能评估。

## 可扩展性框架

- 加密和签名的*类型标识符*允许并行支持多种密码原语。  
- 当前映射包括：  
  - **加密类型：** 0 = ElGamal/AES+SessionTags，4 = ECIES‑X25519‑AEAD‑Ratchet。  
  - **签名类型：** 0 = DSA‑SHA1，7 = EdDSA‑SHA512‑Ed25519，11 = RedDSA‑SHA512‑Ed25519。  
- 该框架支持未来的升级，包括后量子密码方案，而不导致网络分裂。

## 密码学组合

- **传输层：** X25519 + ChaCha20/Poly1305（Noise 框架）。  
- **tunnel 层：** 采用 AES‑256/CBC 的分层加密，以保障匿名性。  
- **端到端：** ECIES‑X25519‑AEAD‑Ratchet，用于实现机密性和前向保密性。  
- **数据库层：** EdDSA/RedDSA 签名，用于确保真实性。

这些层共同实现纵深防御：即使某一层被攻陷，其他层仍能保持机密性与不可关联性。

## 摘要

I2P 2.10.0 的密码学栈以以下内容为中心：

- **Curve25519 (X25519)** 用于密钥交换  
- **ChaCha20/Poly1305** 用于对称加密  
- **EdDSA / RedDSA** 用于签名  
- **SHA‑256 / SHA‑512** 用于哈希与派生  
- **实验性后量子混合模式** 用于前向兼容

出于向后兼容性考虑，遗留的 ElGamal、AES‑CBC 和 DSA 仍被保留，但不再用于当前的传输协议或加密路径。
