---
title: "SOCKS 代理"
description: "安全使用 I2P 的 SOCKS tunnel（更新至 2.10.0 版本）"
slug: "socks"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

> **注意：** SOCKS tunnel 会直接转发应用程序负载而不对其进行清理。许多协议会泄露 IP 地址、主机名或其他标识符。只能在经过匿名性审计的软件中使用 SOCKS。

---

## 1. 概述

I2P 通过 **I2PTunnel 客户端**为出站连接提供 **SOCKS 4、4a 和 5** 代理支持。它使标准应用程序能够访问 I2P 目的地,但**无法访问明网**。**没有 SOCKS outproxy**,所有流量都保持在 I2P 网络内。

### 实现摘要

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Parameter</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Java I2P</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">i2pd</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default Port</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">User-defined</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>127.0.0.1:4447</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported SOCKS Versions</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4, 4a, 5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4, 4a, 5</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UDP Mode</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stubbed (non-functional)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stubbed (non-functional)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Persistent Keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Since 0.9.9</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Shared Client Tunnels</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outproxy Support</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">❌ None</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">❌ None</td>
    </tr>
  </tbody>
</table>
**支持的地址类型：** - `.i2p` 主机名（地址簿条目） - Base32 哈希值（`.b32.i2p`） - 不支持 Base64 或明网地址

---

## 2. 安全风险和限制

### 应用层泄漏

SOCKS 在应用层下方运行，无法清理协议。许多客户端（例如浏览器、IRC、电子邮件）包含会泄露您的 IP 地址、主机名或系统详细信息的元数据。

常见的泄露包括：- 邮件头或 IRC CTCP 响应中的 IP 地址   - 协议负载中的真实姓名/用户名   - 带有操作系统指纹的用户代理字符串   - 外部 DNS 查询   - WebRTC 和浏览器遥测数据

**I2P 无法防止这些泄漏**——它们发生在 tunnel 层之上。仅对**经过审计的客户端**使用 SOCKS,这些客户端需专为匿名性设计。

### 共享隧道身份

如果多个应用程序共享同一个 SOCKS tunnel，它们将共享相同的 I2P destination 身份。这会导致不同服务之间的关联或指纹识别问题。

**缓解措施：** 为每个应用程序使用**非共享隧道**，并启用**持久密钥**以在重启后保持一致的加密身份。

### UDP 模式已被移除

SOCKS5 中的 UDP 支持尚未实现。该协议会宣告 UDP 功能，但调用会被忽略。请使用仅支持 TCP 的客户端。

### 设计上不提供出口代理

与 Tor 不同,I2P **不**提供基于 SOCKS 的明网出口代理。尝试访问外部 IP 将会失败或暴露身份。如果需要出口代理功能,请使用 HTTP 或 HTTPS 代理。

---

## 3. 历史背景

开发者长期以来不鼓励将 SOCKS 用于匿名用途。来自内部开发者讨论以及 2004 年的 [Meeting 81](/zh/blog/2004/03/16/i2p-dev-meeting-march-16-2004/) 和 [Meeting 82](/zh/blog/2004/03/23/i2p-dev-meeting-march-23-2004/):

> "转发任意流量是不安全的,作为匿名软件的开发者,我们有责任将终端用户的安全放在首位。"

包含 SOCKS 支持是为了兼容性，但不建议在生产环境中使用。几乎所有互联网应用程序都会泄露不适合匿名路由的敏感元数据。

---

## 4. 配置

### Java I2P

1. 打开 [I2PTunnel Manager](http://127.0.0.1:7657/i2ptunnel)  
2. 创建一个类型为 **"SOCKS 4/4a/5"** 的新客户端 tunnel  
3. 配置选项:  
   - 本地端口(任何可用端口)  
   - 共享客户端:*禁用*,为每个应用程序使用独立身份  
   - 持久密钥:*启用*以减少密钥关联  
4. 启动 tunnel

### i2pd

i2pd 默认启用 SOCKS5 支持，监听地址为 `127.0.0.1:4447`。可以在 `i2pd.conf` 的 `[SOCKSProxy]` 部分配置端口、主机地址和 tunnel 参数。

---

## 5. 开发时间表

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Change</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Date</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.7.1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Initial SOCKS 4/4a/5 support</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2010</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.9</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Added persistent keying</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2013</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1.7.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">BOB API deprecated and removed</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2022</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P-over-Tor blocked to improve network health</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2024</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Post-quantum hybrid encryption introduced</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2025</td>
    </tr>
  </tbody>
</table>
SOCKS 模块本身自 2013 年以来没有进行重大的协议更新,但周围的 tunnel 栈已经获得了性能和密码学方面的改进。

---

## 6. 推荐的替代方案

对于任何**生产环境**、**面向公众**或**安全关键型**应用程序，请使用官方 I2P API 之一，而不是 SOCKS：

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">API</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended For</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SAM v3 (3.3)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Simple Anonymous Messaging API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Cross-language apps needing socket-like I/O</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Streaming Library</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TCP-like sockets for Java</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Native Java integrations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2CP</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Low-level router communication</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Custom protocols, router-level integration</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>BOB</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated (removed 2022)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Legacy only; migrate to SAM</td>
    </tr>
  </tbody>
</table>
这些 API 提供了适当的目标隔离、密码学身份控制以及更好的路由性能。

---

## 7. OnionCat / GarliCat

OnionCat 通过其 GarliCat 模式（`fd60:db4d:ddb5::/48` IPv6 范围）支持 I2P。仍然可用，但自 2019 年以来开发活动有限。

**使用注意事项：** - 需要在 SusiDNS 中手动配置 `.oc.b32.i2p`   - 需要静态 IPv6 分配   - I2P 项目未正式支持

仅推荐用于高级 VPN-over-I2P 配置。

---

## 8. 最佳实践

如果你必须使用 SOCKS：1. 为每个应用程序创建单独的 tunnel。2. 禁用共享客户端模式。3. 启用持久密钥。4. 强制使用 SOCKS5 DNS 解析。5. 审计协议行为以防泄漏。6. 避免明网连接。7. 监控网络流量以防泄漏。

---

## 9. 技术摘要

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Parameter</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Supported SOCKS Versions</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4, 4a, 5</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Transport</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TCP only</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>UDP Support</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stubbed (non-functional)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Clearnet Access</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Not supported</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Default Ports</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Java I2P: user-set; i2pd: <code>127.0.0.1:4447</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Persistent Keying</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported since 0.9.9</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Shared Tunnels</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported (discouraged)</td>
    </tr>
  </tbody>
</table>
---

## 10. 结论

I2P 中的 SOCKS 代理提供了与现有 TCP 应用程序的基本兼容性,但**并非为强匿名性保证而设计**。它应仅用于受控的、经过审计的测试环境。

> 对于正式部署，请迁移到 **SAM v3** 或 **Streaming API**。这些 API 隔离应用程序身份，使用现代密码学，并持续获得开发支持。

---

### 其他资源

- [官方 SOCKS 文档](/docs/api/socks/)  
- [SAM v3 规范](/docs/api/samv3/)  
- [Streaming 库文档](/docs/specs/streaming/)  
- [I2PTunnel 参考](/docs/specs/implementation/)  
- [I2P 开发者文档](https://i2pgit.org/I2P_Developers/i2p.i2p)  
- [社区论坛](https://i2pforum.net)
