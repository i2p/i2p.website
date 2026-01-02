---
title: "在您的应用程序中嵌入 I2P"
description: "更新了与您的应用程序捆绑 I2P router 的实用指南（负责任地）"
slug: "embedding"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

将 I2P 与您的应用程序捆绑是引导用户的强大方式——但前提是 router 配置得当且负责任。

## 1. 与路由器团队协调

- 在打包之前联系 **Java I2P** 和 **i2pd** 的维护者。他们可以审查你的默认配置并指出兼容性问题。
- 选择适合你技术栈的 router 实现:
  - **Java/Scala** → Java I2P
  - **C/C++** → i2pd
  - **其他语言** → 打包一个 router 并使用 [SAM v3](/docs/api/samv3/) 或 [I2CP](/docs/specs/i2cp/) 进行集成
- 验证 router 二进制文件和依赖项(Java 运行时、ICU 等)的再分发条款。

## 2. 推荐的配置默认值

力求"贡献大于消耗"。现代默认设置优先考虑网络健康和稳定性。

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Setting</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended Default (2025)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Bandwidth share</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">80% for participating tunnels </td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel quantities</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2pd: 3 inbound / 3 outbound; Java I2P: 2 inbound / 2 outbound. </td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature &amp; encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Use Ed25519 (<code>SIGNATURE_TYPE=7</code>) and advertise ECIES-X25519 + ElGamal (<code>i2cp.leaseSetEncType=4,0</code>).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Client protocols</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Use SAM v3 or I2CP.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">API listeners</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Bind SAM/I2CP to <code>127.0.0.1</code> only. Disable if not needed.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UI toggles</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Expose bandwidth controls, logs, and an opt-in checkbox for participating tunnels.</td>
    </tr>
  </tbody>
</table>
### 参与隧道仍然至关重要

**不要**禁用参与隧道（participating tunnels）。

1. 不中继数据的路由器自身性能会更差。
2. 网络依赖于志愿者的容量分享。
3. 掩护流量(中继流量)可以提升匿名性。

**官方最低要求：** - 共享带宽：≥ 12 KB/s   - Floodfill 自动加入：≥ 128 KB/s   - 推荐配置：2 条入站 / 2 条出站 tunnel（Java I2P 默认值）

## 3. 持久化与重新播种

持久化状态目录(`netDb/`、profiles、certificates)必须在运行之间保留。

如果没有持久化，您的用户将在每次启动时触发 reseed（重新获取种子）——这会降低性能并增加 reseed 服务器的负载。

如果无法保持持久性（例如，容器或临时安装）：

1. 在安装程序中捆绑 **1,000–2,000 个 router infos**。
2. 运行一个或多个自定义 reseed 服务器以分担公共服务器的负载。

配置变量：- 基础目录：`i2p.dir.base` - 配置目录：`i2p.dir.config` - 包含用于重新种子的 `certificates/`。

## 4. 安全性和暴露风险

- 保持 router console (`127.0.0.1:7657`) 仅限本地访问。
- 如果需要对外暴露 UI,请使用 HTTPS。
- 除非必需,否则禁用外部 SAM/I2CP。
- 检查包含的插件——仅打包您的应用程序支持的插件。
- 始终为远程 console 访问添加身份验证。

**自2.5.0版本以来引入的安全功能：** - 应用程序之间的NetDB隔离（2.4.0+）   - DoS缓解和Tor黑名单（2.5.1）   - NTCP2探测抵抗（2.9.0）   - Floodfill router选择改进（2.6.0+）

## 5. 支持的 API（2025）

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">API</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SAM v3 (3.3)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Active</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Recommended bridge for non-Java apps.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2CP</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Active</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stable protocol core, used internally by Java I2P.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2PControl</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Active</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">JSON-RPC API; plugin maintained.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>BOB</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">⚠️ Deprecated</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Removed from Java I2P since 1.7.0; use SAM v3 instead.</td>
    </tr>
  </tbody>
</table>
所有官方文档位于 `/docs/api/` 目录下 — 旧的 `/spec/samv3/` 路径**不**存在。

## 6. 网络和端口

典型默认端口：- 4444 – HTTP 代理   - 4445 – HTTPS 代理   - 7654 – I2CP   - 7656 – SAM Bridge   - 7657 – Router Console   - 7658 – 本地 I2P 站点   - 6668 – IRC 代理   - 9000–31000 – 随机 router 端口（UDP/TCP 入站）

路由器在首次运行时会随机选择一个入站端口。端口转发可以提高性能,但 UPnP 可能会自动处理此操作。

## 7. 现代变化（2024–2025）

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Change</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Details</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU1 Transport</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Removed</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SSU2 is now the exclusive UDP transport.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2P-over-Tor</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Blocked</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Since 2.6.0 (July 2024).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Datagram2/3</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Added</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Authenticated, repliable datagram formats (2.9.0).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>LeaseSet service records</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Added</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Enables service discovery (Proposal 167).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Tunnel build parameters</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Improved</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Adaptive congestion handling (2.9.0+).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Post-quantum crypto</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Introduced (beta)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ML-KEM hybrid ratchet, opt-in from 2.10.0.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Java 17 requirement</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Announced</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Becomes mandatory in 2.11.0 (early 2026).</td>
    </tr>
  </tbody>
</table>
## 8. 用户体验与测试

- 说明 I2P 的功能以及为什么要共享带宽。
- 提供 router 诊断信息(带宽、tunnel、reseed 状态)。
- 在 Windows、macOS 和 Linux(包括低内存配置)上测试安装包。
- 验证与 **Java I2P** 和 **i2pd** 节点的互操作性。
- 测试从网络中断和非正常退出中的恢复能力。

## 9. 社区资源

- 论坛：[i2pforum.net](https://i2pforum.net) 或在 I2P 内访问 `http://i2pforum.i2p`。
- 代码：[i2pgit.org/I2P_Developers/i2p.i2p](https://i2pgit.org/I2P_Developers/i2p.i2p)。
- IRC（Irc2P 网络）：`#i2p-dev`、`#i2pd`。
  - `#i2papps` 未经验证；可能不存在。
  - 请明确您的频道托管在哪个网络（Irc2P 还是 ilita.i2p）。

负责任的嵌入意味着在用户体验、性能和网络贡献之间取得平衡。使用这些默认值,与 router 维护者保持同步,并在发布前进行实际负载测试。
