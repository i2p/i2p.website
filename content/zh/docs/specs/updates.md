---
title: "软件更新规范"
description: "面向 I2P router 的安全签名更新机制与更新源结构"
slug: "updates"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## 概述

router 会自动通过轮询在 I2P 网络中分发的已签名新闻源来检查更新。当有更高版本被公告时，router 会下载经密码学签名的更新归档（`.su3`），并将其暂存以待安装。   该系统确保官方发布的分发具有**经认证、防篡改**，以及**多通道**的特性。

自 I2P 2.10.0 起，更新系统使用: - **RSA-4096 / SHA-512** 签名 - **SU3 容器格式**（取代旧版 SUD/SU2） - **冗余镜像：** I2P 网络内的 HTTP、明网 HTTPS，以及 BitTorrent

---

## 1. 新闻源

各个 router 每隔数小时轮询已签名的 Atom 提要，以发现新版本和安全公告。   该提要会被签名，并作为一个 `.su3` 文件分发，其中可能包含：

- `<i2p:version>` — 新版本号  
- `<i2p:minVersion>` — 最低支持的 router 版本  
- `<i2p:minJavaVersion>` — 所需的最低 Java 运行时  
- `<i2p:update>` — 列出多个下载镜像（I2P、HTTPS、torrent）  
- `<i2p:revocations>` — 证书吊销数据  
- `<i2p:blocklist>` — 针对被攻陷节点的网络级封锁列表

### 订阅源分发

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Channel</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2P HTTP (eepsite)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Primary update source</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Private, resilient</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Clearnet HTTPS</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fallback mirror</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Public fallback</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>BitTorrent magnet</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Distributed channel</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reduces mirror load</td>
    </tr>
  </tbody>
</table>
Routers 首选 I2P 源，但在必要时可以回退到明网或 BitTorrent 分发。

---

## 2. 文件格式

### SU3 (当前标准)

在 0.9.9 中引入的 SU3 已取代旧版的 SUD 和 SU2 格式。   每个文件包含一个文件头、负载和尾部签名。

**头部结构** <table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">   <thead>

    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
</thead>   <tbody>

    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Magic</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>"I2Psu3"</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Format Version</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>0</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature Type</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">e.g., <code>0x000B</code> (RSA-SHA512-4096)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature Length</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>512 bytes</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Version String</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Router version</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signer ID</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Certificate name</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Content Type</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1 = router update, 3 = reseed, 4 = news feed</td>
    </tr>
</tbody> </table>

**签名验证步骤** 1. 解析头部并识别签名算法。   2. 使用已存储的签名者证书核验哈希与签名。   3. 确认签名者未被吊销。   4. 将嵌入的版本字符串与有效载荷元数据进行比对。

Routers 随附受信任的签名者证书（目前为 **zzz** 和 **str4d**），并拒绝任何未签名或已吊销的来源。

### SU2（已废弃）

- `.su2` 扩展名用于 Pack200（Java 的 Pack200 压缩格式）压缩的 JAR 包。  
- 在 Java 14 将 Pack200（JEP 367）标记为弃用后被移除。  
- 在 I2P 0.9.48+ 中已禁用；现已完全由 ZIP 压缩取代。

### SUD (旧版)

- 早期的 DSA-SHA1 签名 ZIP 格式（0.9.9 之前）。  
- 无签名者 ID 或头部，完整性保障有限。  
- 由于加密强度较弱且缺乏版本强制机制而被取代。

---

## 3. 更新流程

### 3.1 头部验证

router 仅获取 **SU3 header**（SU3 文件头），在下载完整文件之前用于验证版本字符串。   这可避免在过期的镜像或过时的版本上浪费带宽。

### 3.2 完整下载

在验证头部之后，router 会从以下来源下载完整的 `.su3` 文件： - 网络内 eepsite 镜像 (优先)   - HTTPS 明网镜像 (备用)   - BitTorrent (可选的对等协助分发)

下载使用标准的 I2PTunnel HTTP 客户端，具备重试、超时处理和镜像回退功能。

### 3.3 签名验证

每个下载的文件都会经过： - **签名检查：** RSA-4096/SHA512 验证   - **版本匹配：** 头部与有效载荷版本对比检查   - **防降级：** 确保更新版本高于已安装版本

无效或不匹配的文件会被立即丢弃。

### 3.4 安装阶段

验证完成后： 1. 将 ZIP 压缩包内容解压到临时目录   2. 删除 `deletelist.txt` 中列出的文件   3. 如果包含 `lib/jbigi.jar`，则替换原生库   4. 将签名者证书复制到 `~/.i2p/certificates/`   5. 将更新移动到 `i2pupdate.zip`，以便在下次重启时应用

更新将在下次启动时自动安装，或在手动触发“立即安装更新”时安装。

---

## 4. 文件管理

### deletelist.txt

一份纯文本列表，列出在解包新内容之前应删除的过时文件。

**规则：** - 每行一个路径（仅限相对路径） - 以 `#` 开头的行将被忽略 - 拒绝 `..` 和绝对路径

### 本地库

为防止陈旧或不匹配的原生二进制文件： - 如果 `lib/jbigi.jar` 存在，将删除旧的 `.so` 或 `.dll` 文件   - 确保平台特定的库被重新提取

---

## 5. 证书管理

router 可以通过更新或新闻源中的撤销通知接收**新的签名者证书**。

- 新的 `.crt` 文件会被复制到证书目录。  
- 在后续验证之前，会删除已吊销的证书。  
- 支持密钥轮换，无需用户手动干预。

所有更新均使用**air-gapped（物理隔离）签名系统**进行离线签名。   私钥绝不会存储在构建服务器上。

---

## 6. 开发者指南

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Topic</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Details</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Signing</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Use RSA-4096 (SHA-512) via <code>apps/jetty/news</code> SU3 tooling.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Mirror Policy</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P eepsite preferred, clearnet HTTPS fallback, torrent optional.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Testing</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Validate updates from prior releases, across all OS platforms.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Version Enforcement</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>minVersion</code> prevents incompatible upgrades.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Certificate Rotation</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Distribute new certs in updates and revocation lists.</td>
    </tr>
  </tbody>
</table>
未来的版本将探索后量子签名的集成（参见 Proposal 169）以及可复现构建。

---

## 7. 安全概述

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Threat</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Mitigation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Tampering</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Cryptographic signature (RSA-4096/SHA512)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Key Compromise</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Feed-based certificate revocation</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Downgrade Attack</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Version comparison enforcement</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Mirror Hijack</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature verification, multiple mirrors</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>DoS</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fallback to alternate mirrors/torrents</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>MITM</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HTTPS transport + signature-level integrity</td>
    </tr>
  </tbody>
</table>
---

## 8. 版本管理

- Router: **2.10.0 (API 0.9.67)**  
- 采用 `Major.Minor.Patch` 的语义化版本控制。  
- 最小版本强制机制可防止不安全的升级。  
- 支持的 Java: **Java 8–17**。未来的 2.11.0+ 将要求 Java 17+。

---
