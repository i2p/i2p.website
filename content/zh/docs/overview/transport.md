---
title: "传输层"
description: "理解 I2P 的传输层 - router 之间的点对点通信方法，包括 NTCP2 和 SSU2"
slug: "transport"
lastUpdated: "2025-03"
accurateFor: "2.10.0"
---

---

## 1. 概述

在 I2P 中，**传输** 是在 routers 之间进行直接、点对点通信的方法。这些机制在验证 router 的身份的同时，确保机密性和完整性。

每种传输都基于具备认证、流量控制、确认和重传能力的连接范式运行。

---

## 2. 当前传输协议

I2P 目前支持两种主要的传输协议：

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Transport</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NTCP2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TCP</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise-based TCP transport with modern encryption (as of 0.9.36)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UDP</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Secure Semireliable UDP with modern encryption (as of 0.9.56)</td>
    </tr>
  </tbody>
</table>
### 2.1 旧版传输（已弃用）

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Transport</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NTCP</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TCP</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Replaced by NTCP2; removed in 0.9.62</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UDP</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Replaced by SSU2; removed in 0.9.62</td>
    </tr>
  </tbody>
</table>
---

## 3. 传输服务

传输子系统提供以下服务：

### 3.1 消息传递

- 可靠的 [I2NP](/docs/specs/i2np/) 消息投递（transports（传输层/传输模块）仅处理 I2NP 消息）
- 在所有情况下**不**保证按序交付
- 基于优先级的消息排队

### 3.2 连接管理

- 连接建立与关闭
- 带有阈值强制执行的连接上限管理
- 按对等节点的状态跟踪
- 自动与手动的对等节点封禁列表执行

### 3.3 网络配置

- 每种传输可使用多个 router 地址 (自 v0.9.8 起支持 IPv4 和 IPv6)
- 通过 UPnP 打开防火墙端口
- 支持 NAT/防火墙穿透
- 通过多种方法检测本地 IP

### 3.4 安全

- 用于点对点交换的加密
- 按本地规则进行 IP 地址验证
- 时钟共识确定 (NTP 作为后备)

### 3.5 带宽管理

- 入站和出站带宽限制
- 针对出站消息的最佳传输选择

---

## 4. 传输地址

该子系统维护 router 的联系点列表：

- 传输方式 (NTCP2, SSU2)
- IP 地址
- 端口号
- 可选参数

每种传输方式可以有多个地址。

### 4.1 常见地址配置

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Configuration</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Hidden</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Routers with no published addresses</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Firewalled</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Routers publishing SSU2 addresses with "introducer" peer lists for NAT traversal</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Unrestricted</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Routers advertising both NTCP2 and SSU2 addresses on IPv4 and/or IPv6</td>
    </tr>
  </tbody>
</table>
---

## 5. 传输协议选择

系统在不依赖上层协议的情况下，为[I2NP messages](/docs/specs/i2np/)选择传输方式。选择采用一种**竞价机制**，每种传输方式提交出价，数值最低者获胜。

### 5.1 出价确定因素

- 传输偏好设置
- 现有对等方连接
- 当前连接数与阈值的对比
- 近期连接尝试历史
- 消息大小限制
- 对等方 RouterInfo 的传输能力
- 连接的直接性（直接连接与依赖 introducer（引介者）的连接）
- 对等方公告的传输偏好

通常，两台 routers 会同时维持单一传输方式的连接，但也可以同时建立多传输方式的连接。

---

## 6. NTCP2

**NTCP2** (新传输协议 2) 是 I2P 的现代化、基于 TCP 的传输协议，首次在 0.9.36 版本中引入。

### 6.1 关键特性

- 基于 **Noise Protocol Framework**（Noise 协议框架）（Noise_XK 模式）
- 使用 **X25519** 进行密钥交换
- 使用 **ChaCha20/Poly1305** 进行认证加密
- 使用 **BLAKE2s** 进行哈希
- 协议混淆以抵抗 DPI（深度包检测）
- 可选填充以抵抗流量分析

### 6.2 连接建立

1. **会话请求** (Alice → Bob): 临时 X25519 密钥 + 加密的有效负载
2. **会话已创建** (Bob → Alice): 临时密钥 + 加密的确认
3. **会话确认** (Alice → Bob): 包含 RouterInfo（路由器信息）的最终握手

所有后续数据均使用从握手中派生的会话密钥进行加密。

有关完整细节，请参见 [NTCP2 规范](/docs/specs/ntcp2/)。

---

## 7. SSU2

**SSU2** (安全、半可靠的 UDP 2) 是用于 I2P 的现代、基于 UDP 的传输协议，在 0.9.56 版本中引入。

### 7.1 关键特性

- 基于 **Noise 协议框架** (Noise_XK 模式)
- 使用 **X25519** 进行密钥交换
- 使用 **ChaCha20/Poly1305** 进行认证加密
- 带选择性确认的半可靠传输
- 通过打洞和中继/引入实现 NAT 穿越
- 支持连接迁移
- 路径 MTU 发现

### 7.2 相较于 SSU (旧版) 的优势

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">SSU (Legacy)</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">SSU2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ElGamal + AES</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519 + ChaCha20/Poly1305</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Header encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Partial</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Full (ChaCha20)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connection ID</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fixed</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypted, rotatable</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NAT traversal</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Basic introduction</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Enhanced hole punching + relay</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Obfuscation</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Minimal</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Improved (variable padding)</td>
    </tr>
  </tbody>
</table>
有关完整详情，请参阅 [SSU2 规范](/docs/specs/ssu2/)。

---

## 8. NAT 穿越

两种传输协议均支持 NAT 穿透，以便位于防火墙之后的 router 也能参与网络。

### 8.1 SSU2 介绍

当 router 无法直接接收入站连接时：

1. Router 在其 RouterInfo 中发布 **introducer**（介绍者）地址
2. 发起连接的对等节点向 introducer 发送介绍请求
3. Introducer 将连接信息转发给处于防火墙后的 Router
4. 处于防火墙后的 Router 发起出站连接（打洞）
5. 建立直接通信

### 8.2 NTCP2 与防火墙

NTCP2 需要入站 TCP 连通性。位于 NAT（网络地址转换）后的 Routers 可以:

- 使用 UPnP 自动打开端口
- 手动配置端口转发
- 依赖 SSU2 处理入站连接，同时使用 NTCP2 处理出站连接

---

## 9. 协议混淆

这两种现代传输协议都包含混淆功能：

- **随机填充** 在握手消息中
- **加密的头部**，不暴露协议指纹
- **可变长度的消息** 以抵抗流量分析
- **无固定模式** 在连接建立过程中

> **注意**：传输层混淆起到补充作用，但不能替代 I2P 的 tunnel 架构所提供的匿名性。

---

## 10. 未来开发

计划中的研究和改进包括：

- **可插拔传输** – 兼容 Tor 的混淆插件
- **基于 QUIC 的传输** – 研究 QUIC 协议的优势
- **连接数上限优化** – 研究最佳的对等节点连接数上限
- **增强型填充策略** – 提升抗流量分析能力

---

## 11. 参考资料

- [NTCP2 规范](/docs/specs/ntcp2/) – 基于 Noise 的 TCP 传输（Noise 协议框架）
- [SSU2 规范](/docs/specs/ssu2/) – 安全的半可靠 UDP 2
- [I2NP 规范](/docs/specs/i2np/) – I2P 网络协议消息
- [通用结构](/docs/specs/common-structures/) – RouterInfo 和地址结构
- [NTCP 历史讨论](/docs/ntcp/) – 旧版传输的开发历史
- [遗留 SSU 文档](/docs/legacy/ssu/) – 原始 SSU 规范（已弃用）
