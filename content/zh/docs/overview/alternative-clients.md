---
title: "I2P 替代客户端"
description: "社区维护的 I2P 客户端实现（2025年更新）"
slug: "alternative-clients"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

主要的 I2P 客户端实现使用 **Java**。如果您在特定系统上无法或不希望使用 Java,社区成员开发和维护了其他替代的 I2P 客户端实现。这些程序使用不同的编程语言或方法提供相同的核心功能。

---

## 对比表

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Client</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Language</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Maturity</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Actively Maintained</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Suitable For</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Java I2P</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Java</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stable</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Yes (official)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">General users</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Standard full router; includes console, plugins, and tools</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>i2pd</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">C++</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stable</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Low-resource systems, servers</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Lightweight, fully compatible with Java I2P, includes web console</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Go-I2P</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Go</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Experimental</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">⚙️ In development</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Developers, testing</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Early-stage Go implementation; not yet production ready</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2P+</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Java</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stable (fork)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Advanced users</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Enhanced Java I2P fork with UI and performance improvements</td>
    </tr>
  </tbody>
</table>
---

## i2pd (C++)

**网站：** [https://i2pd.website](https://i2pd.website)

**描述：** i2pd（*I2P Daemon*）是一个用 C++ 实现的全功能 I2P 客户端。它已经稳定用于生产环境多年（自2016年左右开始），并由社区积极维护。i2pd 完整实现了 I2P 网络协议和 API，使其与 Java I2P 网络完全兼容。这个 C++ router 常被用作轻量级替代方案，适用于无法使用或不希望使用 Java 运行时的系统。i2pd 包含一个内置的基于 Web 的控制台，用于配置和监控。它是跨平台的，并提供多种打包格式——甚至还有 Android 版本的 i2pd 可用（例如通过 F-Droid）。

---

## Go-I2P (Go)

**仓库：** [https://github.com/go-i2p/go-i2p](https://github.com/go-i2p/go-i2p)

**描述：** Go-I2P 是一个用 Go 编程语言编写的 I2P 客户端。它是 I2P router 的独立实现，旨在利用 Go 的高效性和可移植性。该项目正在积极开发中，但仍处于早期阶段，尚未完成全部功能。截至 2025 年，Go-I2P 被认为是实验性的——它正在由社区开发者积极开发，但在进一步成熟之前不建议用于生产环境。Go-I2P 的目标是在开发完成后提供一个现代化、轻量级的 I2P router，并与 I2P 网络完全兼容。

---

## I2P+（Java 分支）

**网站：** [https://i2pplus.github.io](https://i2pplus.github.io)

**描述：** I2P+ 是标准 Java I2P 客户端的一个由社区维护的分支。它不是用新语言重新实现的版本，而是 Java router 的增强版本，具有额外的特性和优化。I2P+ 专注于提供改进的用户体验和更好的性能，同时与官方 I2P 网络保持完全兼容。它引入了焕然一新的 Web 控制台界面、更加用户友好的配置选项，以及各种优化（例如，改进的种子性能和更好的网络对等节点处理，尤其是对于防火墙后面的 router）。I2P+ 与官方 I2P 软件一样需要 Java 环境，因此它不是非 Java 环境的解决方案。然而，对于拥有 Java 并希望获得具有额外功能的替代构建版本的用户来说，I2P+ 提供了一个极具吸引力的选择。这个分支与上游 I2P 发布版本保持同步更新（其版本号附加了"+"），可以从项目网站获取。
