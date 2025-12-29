---
title: "Garlic Routing（大蒜路由）"
description: "理解 I2P 中 garlic routing 的术语、架构和现代实现"
slug: "garlic-routing"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

---

## 1. 概述

**Garlic routing**（大蒜路由）仍然是I2P的核心创新之一,它结合了分层加密、消息捆绑和单向tunnel。虽然在概念上与**onion routing**（洋葱路由）类似,但它扩展了该模型,将多个加密消息("cloves",瓣)捆绑在单个信封("garlic",蒜)中,从而提高了效率和匿名性。

术语 *garlic routing* 由 [Michael J. Freedman](https://www.cs.princeton.edu/~mfreed/) 在 [Roger Dingledine 的 Free Haven 硕士论文](https://www.freehaven.net/papers.html)（2000 年 6 月,§8.1.1）中首次提出。I2P 开发者在 2000 年代初期采用了这个术语,以体现其消息捆绑增强功能和单向传输模型,将其与 Tor 的电路交换设计区分开来。

> **总结：** Garlic routing（洋葱路由）= 分层加密 + 消息捆绑 + 通过单向隧道匿名传递。

---

## 2. "Garlic" 术语

历史上，术语 *garlic* 在 I2P 中曾在三种不同的语境下使用：

1. **分层加密** – tunnel 级别的洋葱式保护  
2. **捆绑多条消息** – 在一个"garlic message"中包含多个"cloves"  
3. **端到端加密** – 原为 *ElGamal/AES+SessionTags*,现为 *ECIES‑X25519‑AEAD‑Ratchet*

虽然架构保持不变，但加密方案已经完全现代化。

---

## 3. 分层加密

Garlic routing 与洋葱路由共享其基本原理:每个 router 仅解密一层加密,只了解下一跳而不知道完整路径。

然而，I2P 实现的是**单向 tunnel**，而不是双向电路：

- **Outbound tunnel**：从创建者发送消息出去
- **Inbound tunnel**：将消息带回创建者

一次完整的往返通信（Alice ↔ Bob）使用四条 tunnel：Alice 的 outbound → Bob 的 inbound，然后 Bob 的 outbound → Alice 的 inbound。这种设计相比双向电路**将关联数据暴露减半**。

关于隧道实现细节，请参阅[隧道规范](/docs/specs/implementation)和[隧道创建（ECIES）](/docs/specs/implementation)规范。

---

## 4. 捆绑多个消息（"蒜瓣"）

Freedman 最初的 garlic routing 设想是在一条消息中捆绑多个加密的"bulbs"。I2P 将其实现为 **garlic message** 内部的 **cloves**——每个 clove 都有自己的加密传递指令和目标(router、destination 或 tunnel)。

Garlic 捆绑允许 I2P：

- 将确认和元数据与数据消息结合
- 减少可观察的流量模式
- 支持复杂的消息结构而无需额外连接

![Garlic Message Cloves](/images/garliccloves.png)   *图1：一个 Garlic Message 包含多个 clove（消息片段），每个都有自己的传递指令。*

典型的丁香包括：

1. **传输状态消息** — 确认传输成功或失败的应答消息。  
   这些消息被包裹在各自的 garlic 层中以保持机密性。
2. **数据库存储消息** — 自动捆绑的 LeaseSet,使对等节点无需重新查询 netDb 即可回复。

当出现以下情况时，Cloves 会被捆绑：

- 必须发布新的 LeaseSet
- 传递新的会话标签
- 最近没有发生捆绑（默认约 1 分钟）

Garlic 消息在单个数据包中实现多个加密组件的高效端到端传输。

---

## 5. 加密演进

### 5.1 Historical Context

早期文档（≤ v0.9.12）描述了 *ElGamal/AES+SessionTags* 加密：   - **ElGamal 2048 位**封装 AES 会话密钥   - **AES‑256/CBC** 用于有效载荷加密   - 32 字节会话标签每条消息使用一次

该密码系统已**弃用**。

### 5.2 ECIES‑X25519‑AEAD‑Ratchet (Current Standard)

在2019年至2023年间,I2P完全迁移到了ECIES‑X25519‑AEAD‑Ratchet。现代技术栈标准化了以下组件:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Layer</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">ECIES Primitive or Concept</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Transport Layer (NTCP2, SSU2)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise_NX → X25519, ChaCha20/Poly1305, BLAKE2s</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2NP Delivery</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECIES‑X25519‑AEAD (ChaCha20/Poly1305)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Session Management</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ratchet with rekey records, per-clove key material</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline Authentication</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA (Ed25519) with LeaseSet2/MetaLeaseSet chains</td>
    </tr>
  </tbody>
</table>
ECIES 迁移的好处：

- **前向保密性**，通过每条消息的棘轮密钥实现
- **载荷大小减少**，与 ElGamal 相比
- **弹性**，抵抗密码分析技术的进步
- **兼容性**，支持未来的后量子混合方案（见提案 169）

更多详情：请参阅 [ECIES 规范](/docs/specs/ecies) 和 [EncryptedLeaseSet 规范](/docs/specs/encryptedleaseset)。

---

## 6. LeaseSets and Garlic Bundling

Garlic envelope（大蒜信封）经常包含 leaseSet 来发布或更新目标可达性信息。

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Key Capabilities</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Distribution Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">LeaseSet (legacy)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Single encryption/signature pair</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Accepted for backward compatibility</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">LeaseSet2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Multiple crypto suites, offline signing keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default for modern routers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EncryptedLeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Access-controlled, destination hidden from floodfill</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Requires shared decryption key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MetaLeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Aggregates multiple destinations or multi-homed services</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Extends LeaseSet2 fields recursively</td>
    </tr>
  </tbody>
</table>
所有 LeaseSet 都通过由专用 router 维护的 *floodfill DHT* 分发。发布内容会经过验证、添加时间戳并进行速率限制，以减少元数据关联。

请参阅[网络数据库文档](/docs/specs/common-structures)了解详情。

---

## 7. Modern “Garlic” Applications within I2P

garlic encryption（大蒜加密）和消息捆绑技术贯穿整个 I2P 协议栈：

1. **tunnel 创建和使用** — 每跳分层加密  
2. **端到端消息传递** — 捆绑的 garlic 消息,包含克隆确认和 LeaseSet cloves  
3. **netDb 发布** — 用 garlic 信封包装的 LeaseSets,以保护隐私  
4. **SSU2 和 NTCP2 传输** — 使用 Noise 框架和 X25519/ChaCha20 原语的底层加密

因此，Garlic routing（大蒜路由）既是一种*加密分层方法*，也是一种*网络消息传递模型*。

---

## 6. LeaseSet 和 Garlic 捆绑

I2P的文档中心[可在此处获取](/docs/)，持续维护中。相关的活跃规范包括：

- [ECIES 规范](/docs/specs/ecies) — ECIES‑X25519‑AEAD‑Ratchet
- [Tunnel 创建（ECIES）](/docs/specs/implementation) — 现代 tunnel 构建协议
- [I2NP 规范](/docs/specs/i2np) — I2NP 消息格式
- [SSU2 规范](/docs/specs/ssu2) — SSU2 UDP 传输
- [通用结构](/docs/specs/common-structures) — netDb 和 floodfill 行为

学术验证：Hoang 等人（IMC 2018，USENIX FOCI 2019）和 Muntaka 等人（2025）证实了 I2P 设计的架构稳定性和运行弹性。

---

## 7. I2P 中的现代"Garlic"应用

正在进行的提案：

- **提案 169：** 混合后量子加密（ML-KEM 512/768/1024 + X25519）  
- **提案 168：** 传输带宽优化  
- **数据报和流式传输更新：** 增强的拥塞管理

未来的改进可能包括额外的消息延迟策略或在 garlic-message 级别实现多隧道冗余，这些都基于 Freedman 最初描述的未使用的传输选项。

---

## 8. 当前文档和参考资料

- Freedman, M. J. & Dingledine, R. (2000). *Free Haven Master's Thesis,* § 8.1.1. [Free Haven Papers](https://www.freehaven.net/papers.html)  
- [Onion Router Publications](https://www.onion-router.net/Publications.html)  
- [Garlic Routing (Wikipedia)](https://en.wikipedia.org/wiki/Garlic_routing)  
- [Tor Project](https://www.torproject.org/)  
- [Free Haven Anonbib](https://freehaven.net/anonbib/topic.html)  
- Goldschlag, D. M., Reed, M. G., Syverson, P. F. (1996). *Hiding Routing Information.* NRL Publication.

---
