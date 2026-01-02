---
title: "流式传输协议"
description: "大多数 I2P 应用程序使用的类 TCP 传输协议"
slug: "streaming"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## 概述

**I2P Streaming Library** 在 I2P 的消息层之上提供可靠的、有序的、经过身份验证的传输，类似于 **IP 上的 TCP**。它位于 [I2CP 协议](/docs/specs/i2cp/)之上,几乎所有交互式 I2P 应用程序都使用它,包括 HTTP 代理、IRC、BitTorrent 和电子邮件。

### 核心特性

- 使用 **SYN**、**ACK** 和 **FIN** 标志的单阶段连接建立，可与有效载荷数据捆绑以减少往返次数。
- **滑动窗口拥塞控制**，针对 I2P 的高延迟环境调整了慢启动和拥塞避免机制。
- 数据包压缩（默认 4KB 压缩段），平衡重传成本和分片延迟。
- I2P destination 之间完全**经过身份验证、加密**且**可靠**的通道抽象。

这种设计使得小型 HTTP 请求和响应能够在单次往返中完成。SYN 数据包可以携带请求负载,而响应方的 SYN/ACK/FIN 可能包含完整的响应正文。

---

## API 基础

Java 流式 API 遵循标准的 Java socket 编程方式:

```java
I2PSocketManager mgr = I2PSocketManagerFactory.createManager(host, port, options);
I2PSocket socket       = mgr.connect(destination);
I2PServerSocket server = mgr.getServerSocket();
```
- `I2PSocketManagerFactory` 通过 I2CP 协商或复用 router 会话。
- 如果未提供密钥,会自动生成新的目标地址。
- 开发者可以通过 `options` 映射传递 I2CP 选项(例如 tunnel 长度、加密类型或连接设置)。
- `I2PSocket` 和 `I2PServerSocket` 与标准 Java `Socket` 接口保持一致,使迁移过程更加简单。

完整的 Javadocs 可从 I2P router 控制台或[此处](/docs/specs/streaming/)获取。

---

## 配置与调优

您可以在通过以下方式创建套接字管理器时传递配置属性:

```java
I2PSocketManagerFactory.createManager(host, port, properties);
```
### 密钥选项

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Default</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.maxWindowSize</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Maximum send window (bytes)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128 KB</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.initialRTO</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Initial retransmission timeout</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">9s</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.inactivityTimeout</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Timeout before connection close</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">90s</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.enforceProtocol</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Enforce protocol ID (prevents confusion)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">true</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.congestionAlgorithm</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Congestion control method</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default (AIMD TCP-like)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.disableRejectLogging</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Disable logging rejected packets</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">false</td>
    </tr>
  </tbody>
</table>
### 按工作负载的行为

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Workload</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended Settings</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>HTTP-like</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default parameters are ideal.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Bulk Transfer</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Increase window size to 256 KB or 512 KB; lengthen timeouts.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Real-time Streaming</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Lower tunnel length to 1-2 hops; adjust RTO downwards.</td>
    </tr>
  </tbody>
</table>
自 0.9.4 版本以来的新功能包括拒绝日志抑制、DSA 列表支持(0.9.21)以及强制协议执行(0.9.36)。自 2.10.0 版本以来的 router 包含传输层的后量子混合加密(ML-KEM + X25519)。

---

## 协议详情

每个流由一个**流ID**（Stream ID）标识。数据包携带类似于TCP的控制标志：`SYNCHRONIZE`、`ACK`、`FIN`和`RESET`。数据包可以同时包含数据和控制标志，从而提高短期连接的效率。

### 连接生命周期

1. **SYN 已发送** — 发起方包含可选数据。
2. **SYN/ACK 响应** — 响应方包含可选数据。
3. **ACK 最终确认** — 建立可靠性和会话状态。
4. **FIN/RESET** — 用于有序关闭或突然终止。

### 分片与重组

由于 I2P tunnel 会引入延迟和消息重新排序，该库会缓冲来自未知或提前到达的流的数据包。缓冲的消息会被存储直到同步完成，从而确保完整且有序的传递。

### 协议强制执行

选项 `i2p.streaming.enforceProtocol=true`(自 0.9.36 起为默认值)确保连接使用正确的 I2CP 协议号,防止共享同一 destination 的多个子系统之间发生冲突。

---

## 互操作性和最佳实践

流式协议与 **Datagram API** 共存，为开发者提供了面向连接和无连接传输方式之间的选择。

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Use Case</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended Transport</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reliable, ordered data (HTTP, IRC, FTP)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Streaming</strong></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connectionless or lossy data (DNS, telemetry)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Datagram</strong></td>
    </tr>
  </tbody>
</table>
### 共享客户端

应用程序可以通过作为**共享客户端**运行来重用现有的 tunnel，允许多个服务共享同一个 destination。虽然这减少了开销，但会增加跨服务关联的风险——请谨慎使用。

### 拥塞控制

- 流式传输层通过基于 RTT 的反馈持续适应网络延迟和吞吐量。
- 当 router 作为贡献节点（启用参与 tunnel）时,应用程序性能最佳。
- 类 TCP 拥塞控制机制可防止慢速节点过载,并帮助平衡各 tunnel 的带宽使用。

### 延迟考量

由于 I2P 会增加数百毫秒的基础延迟，应用程序应该尽量减少往返次数。在可能的情况下，将数据与连接建立过程捆绑在一起（例如，在 SYN 中包含 HTTP 请求）。避免依赖许多小型顺序交换的设计。

---

## 测试与兼容性

- 始终针对 **Java I2P** 和 **i2pd** 进行测试，以确保完全兼容。
- 尽管协议已标准化，但可能存在细微的实现差异。
- 优雅地处理较旧的 router——许多节点仍在运行 2.0 之前的版本。
- 使用 `I2PSocket.getOptions()` 和 `getSession()` 监控连接统计信息，以读取 RTT 和重传指标。

性能在很大程度上取决于 tunnel 配置：   - **短 tunnel（1-2 跳）** → 延迟较低，匿名性降低。   - **长 tunnel（3+ 跳）** → 匿名性较高，RTT 增加。

---

## 关键改进 (2.0.0–2.10.0)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Introduced</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Persistent ACK Bundling</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.0.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Optimized round-trip reduction for HTTP workloads.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Adaptive Window Scaling</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.3.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Improved large file transfer stability.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Thread Pooling and Socket Reuse</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.5.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reduced per-connection overhead.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Protocol Enforcement Default</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.36</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ensures correct stream usage.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Hybrid ML-KEM Ratchet</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Adds post-quantum hybrid encryption layer.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>i2pd Streaming API Compatibility Fixes</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.9.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Full parity with Java I2P library behavior.</td>
    </tr>
  </tbody>
</table>
---

## 概述

**I2P Streaming Library** 是 I2P 内所有可靠通信的支柱。它确保有序、经过身份验证、加密的消息传递,并在匿名环境中提供几乎可直接替代 TCP 的方案。

为了实现最佳性能：- 通过 SYN+payload 捆绑来最小化往返次数。- 根据工作负载调整窗口和超时参数。- 对于延迟敏感的应用程序，优先使用较短的 tunnel。- 使用拥塞友好的设计以避免使对等节点过载。
