---
title: "Tunnel 操作指南"
description: "用于通过 I2P tunnels 构建、加密和传输流量的统一规范。"
slug: "implementation"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
reviewStatus: "needs-review"
---

> **范围：** 本指南汇总了 tunnel 的实现、消息格式，以及两种 tunnel 创建规范（ECIES 和旧版 ElGamal）。现有深链接可继续通过上述别名使用。

## Tunnel 模型 {#tunnel-model}

I2P 通过*单向的 tunnel*转发有效载荷：由有序的 routers 组成，只在单一方向传输流量。两个目的地之间的一次完整往返需要四条 tunnel（两条出站、两条入站）。

先阅读 [Tunnel Overview](/docs/overview/tunnel-routing/) 以了解术语，然后使用本指南获取操作细节。

### 消息生命周期 {#message-lifecycle}

1. tunnel **网关** 将一个或多个 I2NP 消息打包，对其进行分片，并写入投递指令。
2. 该网关将负载封装为固定大小 (1024&nbsp;B) 的 tunnel 消息，必要时进行填充。
3. 每个**参与者** 验证前一跳，施加其加密层，并将 `{nextTunnelId, nextIV, encryptedPayload}` 转发到下一跳。
4. tunnel **端点** 移除最后一层，处理投递指令，重新组装分片，并分发重建后的 I2NP 消息。

重复检测使用一种以 IV（初始向量）与第一个密文分组的异或值作为键的衰减布隆过滤器，以阻止基于 IV 交换的标记攻击。

### 角色概览 {#roles}

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Role</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Pre-processing</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Crypto Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Post-processing</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outbound gateway (creator)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fragment, batch, pad</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Iteratively <em>decrypt</em> using every hop’s keys (so downstream peers encrypt)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to first hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Participant</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt IV and payload with hop keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outbound endpoint</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt once more to reveal plaintext payload</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deliver to target tunnel/destination</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Inbound gateway</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fragment, batch, pad</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt with local keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Inbound endpoint (creator)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Iteratively decrypt using stored hop keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reassemble and deliver locally</td>
    </tr>
  </tbody>
</table>
### 加密工作流程 {#encryption-workflow}

- **入站 tunnels:** 网关使用其层密钥加密一次；下游参与者继续加密，直到创建者解密最终有效载荷。
- **出站 tunnels:** 网关预先应用每一跳加密的逆运算，使得每个参与者都进行加密。当端点完成加密时，网关的原始明文被还原。

两个方向都将 `{tunnelId, IV, encryptedPayload}` 转发到下一跳。

---

## Tunnel 消息格式 {#tunnel-message-format}

Tunnel 网关将 I2NP 消息分片为固定大小的封包，以隐藏有效负载长度并简化逐跳处理。

### 加密布局 {#encrypted-layout}

```
+----------------+----------------+-------------------+
| Tunnel ID (4B) | IV (16B)       | Encrypted payload |
+----------------+----------------+-------------------+
```
- **Tunnel ID** – 用于下一跳的 32 位标识符（非零，每个构建周期轮换）。
- **IV** – 每条消息选择的 16 字节 AES IV。
- **加密有效负载** – 1008 字节的 AES-256-CBC 密文。

总大小：1028 字节。

### 解密后的布局 {#decrypted-layout}

当某个跳点移除了其加密层之后：

```
[Checksum (4B)][Padding ... 0x00 terminator]
[Delivery Instructions 1][I2NP fragment 1]
[Delivery Instructions 2][I2NP fragment 2]
...
```
- **校验和**用于验证解密后的数据块。
- **填充**是由随机的非零字节组成，并以一个零字节结束。
- **传递指令**告知端点如何处理每个分片（本地递送、转发到另一个 tunnel 等）。
- **分片**承载底层的 I2NP 消息；端点会在将其传递到更高层之前对其进行重组。

### 处理步骤 {#processing-steps}

1. 网关对 I2NP 消息进行分片并排队，短暂保留未完整的片段以便重组。
2. 网关使用相应的层密钥对载荷加密，并设置 tunnel ID 以及 IV（初始化向量）。
3. 每个参与者先加密 IV（AES-256/ECB），再加密载荷（AES-256/CBC），随后再次加密 IV 并转发消息。
4. 端点按相反顺序解密，验证校验和，执行投递指令，并重组这些片段。

---

## Tunnel 建立 (ECIES-X25519，椭圆曲线集成加密方案，基于 X25519) {#tunnel-creation-ecies}

现代的 routers 使用 ECIES-X25519 密钥来构建 tunnels，从而缩小构建消息的大小并实现前向保密。

- **构建消息：** 单个 `TunnelBuild`（或 `VariableTunnelBuild`）I2NP 消息承载 1–8 条加密的构建记录，每一跳一条。
- **层密钥：** 创建者使用该跳的静态 X25519（椭圆曲线密钥交换算法）身份以及创建者的临时密钥，通过 HKDF（基于HMAC的密钥派生函数）导出每跳的层密钥、IV（初始化向量）和回复密钥。
- **处理：** 每一跳解密其记录，验证请求标志，写入回复块（成功或详细失败代码），重新加密其余记录，并转发该消息。
- **回复：** 创建者会接收到一个使用 garlic encryption 封装的回复消息。标记为失败的记录包含一个严重性代码，以便 router 能够为该对等体建立画像。
- **兼容性：** 为了向后兼容，router 仍可接受传统的 ElGamal（公钥加密算法）构建，但新的 tunnel 默认使用 ECIES（椭圆曲线集成加密方案）。

> 关于逐字段的常量和密钥派生说明，请参见 ECIES（椭圆曲线集成加密方案）提案历史和 router 源码；本指南涵盖操作流程。

---

## 旧版 Tunnel 创建 (ElGamal-2048) {#tunnel-creation-elgamal}

最初的 tunnel 构建格式使用了 ElGamal 公钥。现代的 routers 仅保留有限的向后兼容支持。

> **状态：** 已过时。为历史参考而保留于此，并供维护与遗留版本兼容的工具的人员使用。

- **Non-interactive telescoping（非交互式逐段伸展）:** 单个构建消息贯穿整个路径。每一跳解密其 528 字节的记录，更新消息并将其转发。
- **可变长度:** 可变 Tunnel 构建消息（VTBM）允许包含 1–8 条记录。早期的固定消息始终包含八条记录，以混淆 tunnel 的长度。
- **请求记录布局:**

```
Bytes 0–3    : Tunnel ID (receiving ID)
Bytes 4–35   : Current hop router hash
Bytes 36–39  : Next tunnel ID
Bytes 40–71  : Next hop router hash
Bytes 72–103 : AES-256 layer key
Bytes 104–135: AES-256 IV key
Bytes 136–167: AES-256 reply key
Bytes 168–183: AES-256 reply IV
Byte 184     : Flags (bit7=IBGW, bit6=OBEP)
Bytes 185–188: Request time (hours since epoch)
Bytes 189–192: Next message ID
Bytes 193–221: Padding
```
- **标志：** 第7位表示入站网关（IBGW）；第6位表示出站端点（OBEP）。二者互斥。
- **加密：** 每条记录使用该跳点的公钥进行 ElGamal-2048（ElGamal 2048位公钥加密算法）加密。对称的 AES-256-CBC（AES 256位CBC模式）分层确保只有预定的跳点能够读取其记录。
- **要点：** tunnel ID 均为非零的 32 位值；创建者可以插入填充记录以隐藏实际的 tunnel 长度；可靠性取决于重试失败的构建。

---

## Tunnel 池和生命周期 {#tunnel-pools}

router 会为探测流量以及每个 I2CP 会话分别维护独立的入站和出站 tunnel 池。

- **节点选择:** 探索型 tunnels 从“active, not failing”的节点桶中选取以提升多样性; 客户端 tunnels 更偏好快速、高容量的节点。
- **确定性排序:** 节点按 `SHA256(peerHash || poolKey)` 与该池随机密钥之间的 XOR 距离（按位异或距离）进行排序。该密钥在重启时轮换, 既保证单次运行内的稳定性, 又在跨运行时抑制前驱攻击。
- **生命周期:** routers 按 `{mode, direction, length, variance}` 元组跟踪历史构建时间。随着 tunnels 接近到期, 会提前启动替换; 在发生失败时, router 会增加并行构建数量, 同时对未完成的尝试设定上限。
- **配置可调项:** 活动/备份 tunnel 数量、跳数及其方差、零跳许可以及构建速率限制, 均可按池进行调节。

---

## 拥塞与可靠性 {#congestion}

尽管 tunnels 类似于电路，routers 将它们视为消息队列。为了将时延保持在可控范围内，会使用加权随机早期丢弃（WRED）：

- 当利用率接近配置的上限时，丢弃概率会上升。
- 参与方按固定大小的片段进行计算；网关/端点会根据片段的合计大小决定丢弃，优先丢弃大型有效负载。
- 出站端点会先于其他角色执行丢弃，以尽可能减少网络资源消耗。

保证交付留给更高层（例如 [Streaming library](/docs/specs/streaming/)）。需要可靠性的应用必须自行处理重传和确认。

---

## 延伸阅读 {#further-reading}

- [节点选择](/docs/overview/tunnel-routing#peer-selection/)
- [Tunnel 概述](/docs/overview/tunnel-routing/)
- [旧版 Tunnel 实现](/docs/legacy/old-implementation/)
