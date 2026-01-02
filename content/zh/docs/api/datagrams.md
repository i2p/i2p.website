---
title: "数据报"
description: "I2CP 之上的认证、可回复和原始消息格式"
slug: "datagrams"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
toc: true
---

## 概述

数据报在 [I2CP](/docs/specs/i2cp/) 之上提供面向消息的通信，与流式库并行。它们支持**可回复的**、**经过身份验证的**或**原始**数据包，而无需面向连接的流。router 将数据报封装到 I2NP 消息和 tunnel 消息中，无论是 NTCP2 还是 SSU2 承载流量。

核心动机是允许应用程序（如tracker、DNS解析器或游戏）发送能够标识发送者的自包含数据包。

> **2025年新增：** I2P项目批准了**Datagram2（协议19）**和**Datagram3（协议20）**，这是十年来首次增加重放保护和更低开销的可回复消息传递功能。

---

## 1. 协议常量

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Value</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Introduced</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>PROTO_DATAGRAM</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">17</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Signed (repliable) datagram – “Datagram1”</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Original</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>PROTO_DATAGRAM_RAW</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unsigned (raw) datagram – no sender info</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Original</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>PROTO_DATAGRAM2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Signed + replay-protected datagram</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">API 0.9.66 (2025)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>PROTO_DATAGRAM3</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Repliable (no signature, hash only)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">API 0.9.66 (2025)</td>
    </tr>
  </tbody>
</table>
协议 19 和 20 在 **提案 163（2025 年 4 月）** 中正式确定。它们与 Datagram1 / RAW 共存以保持向后兼容性。

---

## 2. 数据报类型

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Repliable</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Authenticated</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Replay Protection</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Min Overhead</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Raw</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Minimal size; spoofable.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Datagram1</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">17</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">≈ 427</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Full Destination + signature.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Datagram2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">≈ 457</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Replay prevention + offline signatures; PQ-ready.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Datagram3</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">≈ 34</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Sender hash only; low overhead.</td>
    </tr>
  </tbody>
</table>
### 典型设计模式

- **请求 → 响应：** 发送一个签名的 Datagram2（请求 + nonce），接收一个原始或 Datagram3 回复（回显 nonce）。
- **高频率/低开销：** 优先使用 Datagram3 或 RAW。
- **经过身份验证的控制消息：** Datagram2。
- **传统兼容性：** Datagram1 仍然完全支持。

---

## 3. Datagram2 和 Datagram3 详细信息（2025）

### Datagram2（协议 19）

Datagram1 的增强替代版本。特性：- **防重放：** 4 字节防重放令牌。 - **离线签名支持：** 支持离线签名的 Destination 使用。 - **扩展签名覆盖范围：** 包括目标哈希、标志、选项、离线签名块、有效载荷。 - **后量子就绪：** 兼容未来的 ML-KEM 混合方案。 - **开销：** ≈ 457 字节（X25519 密钥）。

### Datagram3（协议 20）

弥合原始类型和签名类型之间的差距。特性：- **可在无签名情况下回复：**包含发送者的 32 字节哈希 + 2 字节标志。- **极小开销：**约 34 字节。- **无重放防御** — 应用程序必须自行实现。

这两种协议都是 API 0.9.66 的特性，自 2.9.0 版本起在 Java router 中实现；目前尚无 i2pd 或 Go 实现（截至 2025 年 10 月）。

---

## 4. 大小和分片限制

- **Tunnel 消息大小：** 1 028 字节（4 B Tunnel ID + 16 B IV + 1 008 B 有效载荷）。  
- **初始分片：** 956 B（典型的 TUNNEL 传输）。  
- **后续分片：** 996 B。  
- **最大分片数：** 63–64。  
- **实际限制：** ≈ 62 708 B（约 61 KB）。  
- **推荐限制：** ≤ 10 KB 以确保可靠传输（超过此限制丢包率呈指数增长）。

**开销总结：** - 数据报1 ≈ 427 B（最小）。- 数据报2 ≈ 457 B。- 数据报3 ≈ 34 B。- 附加层（I2CP gzip 头、I2NP、Garlic、Tunnel）：最坏情况下约 +5.5 KB。

---

## 5. I2CP / I2NP 集成

消息路径：1. 应用程序创建数据报（通过 I2P API 或 SAM）。2. I2CP 使用 gzip 头部（`0x1F 0x8B 0x08`，RFC 1952）和 CRC-32 校验和进行封装。3. 协议 + 端口号存储在 gzip 头部字段中。4. Router 封装为 I2NP 消息 → Garlic clove → 1 KB tunnel 片段。5. 片段穿越 outbound → 网络 → inbound tunnel。6. 重组后的数据报根据协议号传递给应用程序处理器。

**完整性：** CRC-32（来自 I2CP）+ 可选的加密签名（Datagram1/2）。数据报本身内部没有单独的校验和字段。

---

## 6. 编程接口

### Java API

包 `net.i2p.client.datagram` 包含：- `I2PDatagramMaker` – 构建签名数据报。   - `I2PDatagramDissector` – 验证并提取发送者信息。   - `I2PInvalidDatagramException` – 验证失败时抛出。

`I2PSessionMuxedImpl` (`net.i2p.client.impl.I2PSessionMuxedImpl`) 为共享一个 Destination 的应用程序管理协议和端口复用。

**Javadoc 访问：** - [idk.i2p Javadoc](http://idk.i2p/javadoc-i2p/)（仅限 I2P 网络） - [Javadoc 镜像](https://eyedeekay.github.io/javadoc-i2p/)（明网镜像） - [官方 Javadocs](http://docs.i2p-projekt.de/javadoc/)（官方文档）

### SAM v3 支持

- SAM 3.2 (2016): 添加了 PORT 和 PROTOCOL 参数。
- SAM 3.3 (2016): 引入了 PRIMARY/subsession 模型；允许在一个 Destination 上同时使用流和数据报。
- 对 Datagram2 / 3 会话样式的支持已添加到 2025 年规范（实现待定）。
- 官方规范：[SAM v3 规范](/docs/api/samv3/)

### i2ptunnel 模块

- **udpTunnel：** I2P UDP 应用的完全功能基础（`net.i2p.i2ptunnel.udpTunnel`）。
- **streamr：** 可用于音视频流传输（`net.i2p.i2ptunnel.streamr`）。
- **SOCKS UDP：** 截至 2.10.0 版本**不可用**（仅有 UDP 存根）。

> 对于通用 UDP，请使用 Datagram API 或直接使用 udpTunnel——不要依赖 SOCKS UDP。

---

## 7. 生态系统和语言支持 (2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Language</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Library / Package</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">SAM Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Java</td><td style="border:1px solid var(--color-border); padding:0.5rem;">core API (net.i2p.client.datagram)</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✓ full support</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">C++</td><td style="border:1px solid var(--color-border); padding:0.5rem;">i2pd / libsam3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2 partial</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Limited</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Go</td><td style="border:1px solid var(--color-border); padding:0.5rem;">go-i2p / sam3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1–3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td><td style="border:1px solid var(--color-border); padding:0.5rem;">i2plib, i2p.socket, txi2p</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Rust</td><td style="border:1px solid var(--color-border); padding:0.5rem;">i2p-rs, i2p_client</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">C#</td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2PSharp</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">JS/TS</td><td style="border:1px solid var(--color-border); padding:0.5rem;">node-i2p, i2p-sam</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Haskell</td><td style="border:1px solid var(--color-border); padding:0.5rem;">network-anonymous-i2p</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Lua</td><td style="border:1px solid var(--color-border); padding:0.5rem;">mooni2p</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental</td></tr>
  </tbody>
</table>
Java I2P 是目前唯一支持完整 SAM 3.3 subsessions 和 Datagram2 API 的 router。

---

## 8. 示例用法 – UDP Tracker (I2PSnark 2.10.0)

Datagram2/3 的首个实际应用：

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Datagram Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Announce Request</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Datagram3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Repliable but low-overhead update</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Response</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Raw Datagram</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimal payload return</td></tr>
  </tbody>
</table>
模式演示了如何混合使用经过身份验证的数据报和轻量级数据报，以平衡安全性和性能。

---

## 9. 安全性和最佳实践

- 对于任何需要身份验证的交换或当重放攻击很重要时，使用 Datagram2。
- 对于需要快速可回复响应且具有中等信任度的场景，优先使用 Datagram3。
- 对于公共广播或匿名数据，使用 RAW。
- 保持有效载荷 ≤ 10 KB 以确保可靠传输。
- 请注意 SOCKS UDP 仍然无法正常工作。
- 始终在接收时验证 gzip CRC 和数字签名。

---

## 10. 技术规范

本节介绍底层数据报格式、封装和协议细节。

### 10.1 协议识别

数据报格式**不**共享通用头部。Router 无法仅从有效载荷字节推断类型。

当混合使用多种数据报类型时——或者当将数据报与流式传输结合使用时——需要明确设置：- **协议号**（通过 I2CP 或 SAM）- 可选的 **端口号**，如果您的应用程序需要复用多个服务

不建议将协议保持未设置状态（`0` 或 `PROTO_ANY`），这可能会导致路由或传递错误。

### 10.2 原始数据报

不可回复数据报不携带发送者或认证数据。它们是不透明的有效载荷,在更高级别的数据报 API 之外处理,但通过 SAM 和 I2PTunnel 提供支持。

**协议：** `18` (`PROTO_DATAGRAM_RAW`)

**格式：**

```
+----+----+----+----+----//
|     payload...
+----+----+----+----+----//
```
负载长度受传输限制约束（实际最大约 32 KB，通常远小于此值）。

### 10.3 Datagram1（可回复数据报）

嵌入发送者的 **Destination** 和用于身份验证及回复寻址的 **Signature**。

**协议：** `17` (`PROTO_DATAGRAM`)

**开销：** ≥427 字节 **有效载荷：** 最多 ~31.5 KB（受传输层限制）

**格式：**

```
+----+----+----+----+----+----+----+----+
|               from                    |
+                                       +
|                                       |
~             Destination bytes         ~
|                                       |
+----+----+----+----+----+----+----+----+
|             signature                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|     payload...
+----+----+----+----//
```
- `from`: 一个 Destination (387+ 字节)
- `signature`: 与密钥类型匹配的签名
  - 对于 DSA_SHA1: 对载荷的 SHA-256 哈希值的签名
  - 对于其他密钥类型: 直接对载荷的签名

**注意：** - 非DSA类型的签名在I2P 0.9.14中标准化。- LS2（提案123）离线签名目前在Datagram1中不受支持。

### 10.4 Datagram2 格式

一个改进的可回复数据报，增加了[提案 163](/proposals/163-datagram2/) 中定义的**重放抵抗**功能。

**协议：** `19` (`PROTO_DATAGRAM2`)

实现正在进行中。应用程序应包含随机数（nonce）或时间戳检查以提供冗余保护。

### 10.5 Datagram3 格式

提供**可回复但未认证**的数据报。依赖于 router 维护的会话认证,而非嵌入的 destination 和签名。

**协议：** `20` (`PROTO_DATAGRAM3`) **状态：** 自 0.9.66 版本起开发中

适用于以下情况：- 目标地址较大（例如，后量子密钥）- 在其他层进行身份验证 - 带宽效率至关重要

### 10.6 数据完整性

数据报的完整性通过 I2CP 层中的 **gzip CRC-32 校验和**来保护。数据报有效载荷格式本身不存在显式的校验和字段。

### 10.7 数据包封装

每个数据报都被封装为单个 I2NP 消息或作为 **Garlic Message** 中的单个 clove。I2CP、I2NP 和 tunnel 层处理长度和帧 —— 数据报协议中没有内部分隔符或长度字段。

### 10.8 后量子（PQ）考虑因素

如果实施 **Proposal 169**（ML-DSA 签名），签名和目标地址的大小将急剧增加——从约 455 字节增加到 **≥3739 字节**。这一变化将大幅增加数据报开销并降低有效载荷容量。

**Datagram3** 依赖会话级认证(而非嵌入式签名),很可能成为后量子 I2P 环境中的首选设计。

---

## 11. 参考文献

- [提案 163 – Datagram2 和 Datagram3](/proposals/163-datagram2/)
- [提案 160 – UDP Tracker 集成](/proposals/160-udp-trackers/)
- [提案 144 – Streaming MTU 计算](/proposals/144-ecies-x25519-aead-ratchet/)
- [提案 169 – 后量子签名](/proposals/169-pq-crypto/)
- [I2CP 规范](/docs/specs/i2cp/)
- [I2NP 规范](/docs/specs/i2np/)
- [Tunnel 消息规范](/docs/specs/implementation/)
- [SAM v3 规范](/docs/api/samv3/)
- [i2ptunnel 文档](/docs/api/i2ptunnel/)

## 12. 更新日志要点（2019 – 2025）

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Year</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Release</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Change</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2019</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.43</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Datagram API stabilization</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2021</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.50</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Protocol port handling reworked</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2022</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2.0.0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 adoption completed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2024</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2.6.0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy transport removal simplified UDP code</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2025</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2.9.0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Datagram2/3 support added (Java API)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2025</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2.10.0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">UDP Tracker implementation released</td></tr>
  </tbody>
</table>
---

## 13. 总结

数据报子系统现在支持四种协议变体,提供从完全认证到轻量级原始传输的全方位选择。开发者应针对安全敏感的使用场景迁移至 **Datagram2**,针对需要高效回复的流量迁移至 **Datagram3**。所有旧类型保持兼容以确保长期互操作性。
