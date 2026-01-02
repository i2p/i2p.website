---
title: "I2PTunnel"
description: "用于与 I2P 交互并在 I2P 上提供服务的工具"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## 概述

I2PTunnel 是 I2P 的核心组件,用于在 I2P 网络上进行接口交互和提供服务。它通过 tunnel 抽象使基于 TCP 的应用程序和媒体流应用程序能够匿名运行。tunnel 的目的地可以通过[主机名](/docs/overview/naming)、[Base32](/docs/overview/naming#base32)或完整的目的地密钥来定义。

每个已建立的 tunnel 在本地监听(例如 `localhost:port`)并在内部连接到 I2P 目标地址。要托管服务,请创建一个指向所需 IP 和端口的 tunnel。系统会生成相应的 I2P destination 密钥,使该服务能够在 I2P 网络内被全局访问。I2PTunnel 网页界面位于 [I2P Router Tunnel Manager](http://localhost:7657/i2ptunnel/)。

---

## 默认服务

### 服务器隧道

- **I2P Webserver** – 一个指向 [localhost:7658](http://localhost:7658) 的 Jetty webserver 的 tunnel,用于在 I2P 上轻松托管网站。  
  - **Unix:** `$HOME/.i2p/eepsite/docroot`  
  - **Windows:** `%LOCALAPPDATA%\I2P\I2P Site\docroot` → `C:\Users\<username>\AppData\Local\I2P\I2P Site\docroot`

### 客户端隧道

- **I2P HTTP Proxy** – `localhost:4444` – 用于通过 outproxy 浏览 I2P 和互联网。  
- **I2P HTTPS Proxy** – `localhost:4445` – HTTP proxy 的安全变体。  
- **Irc2P** – `localhost:6668` – 默认的匿名 IRC 网络 tunnel。  
- **Git SSH (gitssh.idk.i2p)** – `localhost:7670` – 用于代码仓库 SSH 访问的客户端 tunnel。  
- **Postman SMTP** – `localhost:7659` – 用于发送邮件的客户端 tunnel。  
- **Postman POP3** – `localhost:7660` – 用于接收邮件的客户端 tunnel。

> 注意：只有 I2P Web 服务器是默认的**服务器 tunnel**；其他所有的都是连接到外部 I2P 服务的客户端 tunnel。

---

## 配置

I2PTunnel 配置规范记录在 [/spec/configuration](/docs/specs/configuration/)。

---

## 客户端模式

### 标准

打开一个本地 TCP 端口,连接到 I2P 目标地址上的服务。支持用逗号分隔的多个目标地址条目以实现冗余。

### HTTP

用于HTTP/HTTPS请求的代理tunnel。支持本地和远程outproxy、请求头剥离、缓存、身份验证和透明压缩。

**隐私保护：** - 剥离请求头：`Accept-*`、`Referer`、`Via`、`From` - 将主机头替换为 Base32 目标地址 - 强制执行符合 RFC 标准的逐跳剥离 - 添加透明解压缩支持 - 提供内部错误页面和本地化响应

**压缩行为：** - 请求可使用自定义头部 `X-Accept-Encoding: x-i2p-gzip` - 带有 `Content-Encoding: x-i2p-gzip` 的响应会被透明解压 - 根据 MIME 类型和响应长度评估压缩效率

**持久连接（2.5.0 版本新增）：** Hidden Services Manager 现在支持 I2P 托管服务的 HTTP Keepalive 和持久连接。这减少了延迟和连接开销，但尚未在所有跳点上实现完全符合 RFC 2616 标准的持久套接字。

**流水线（Pipelining）：** 仍不受支持且没有必要；现代浏览器已弃用该功能。

**User-Agent 行为：** - **Outproxy：** 使用当前的 Firefox ESR User-Agent。 - **内部：** 使用 `MYOB/6.66 (AN/ON)` 以保持匿名性一致。

### IRC 客户端

连接到基于 I2P 的 IRC 服务器。允许安全的命令子集，同时过滤标识符以保护隐私。

### SOCKS 4/4a/5

为 TCP 连接提供 SOCKS 代理功能。UDP 在 Java I2P 中尚未实现(仅在 i2pd 中可用)。

### 连接

为 SSL/TLS 连接实现 HTTP `CONNECT` 隧道。

### Streamr

通过基于 TCP 的封装启用 UDP 风格的流式传输。当与相应的 Streamr 服务器隧道配对时，支持媒体流传输。

![I2PTunnel Streamr 图示](/images/I2PTunnel-streamr.png)

---

## 服务器模式

### 标准服务器

创建一个映射到本地 IP:端口的 TCP destination。

### HTTP 服务器

创建一个与本地 Web 服务器交互的 destination。支持压缩（`x-i2p-gzip`）、请求头剥离和 DDoS 防护。现在还受益于**持久连接支持**（v2.5.0+）和**线程池优化**（v2.7.0–2.9.0）。

### HTTP 双向

**已弃用** – 仍然可用但不推荐使用。同时充当 HTTP 服务器和客户端，但不进行 outproxy（出口代理）。主要用于诊断回环测试。

### IRC 服务器

为 IRC 服务创建一个过滤目标，将客户端目标密钥作为主机名传递。

### Streamr 服务器

与 Streamr 客户端 tunnel 配合使用，以处理通过 I2P 传输的 UDP 风格数据流。

---

## 新功能（2.4.0–2.10.0）

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Introduced</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Summary</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Keepalive/Persistent Connections</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.5.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HTTP tunnels now support persistent sockets for I2P-hosted services, improving performance.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Thread Pooling Optimization</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.7.0-2.9.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reduced CPU overhead and latency by improving thread management.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Post-Quantum Encryption (ML-KEM)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Optional hybrid X25519+ML-KEM encryption to resist future quantum attacks.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NetDB Segmentation</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.4.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Isolates I2PTunnel contexts for improved security and privacy.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU1 Removal / SSU2 Adoption</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.4.0-2.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Upgraded transport layer; transparent to users.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2P-over-Tor Blocking</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Prevents inefficient and unstable I2P-over-Tor routing.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Browser Proxy (Proposal 166)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.7.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Introduced identity-aware proxy mode; details pending confirmation.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Java 17 Requirement (upcoming)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.11.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Future release will require Java 17+.</td>
    </tr>
  </tbody>
</table>
---

## 安全特性

- **头部剥离**以保护匿名性（Accept、Referer、From、Via）
- **User-Agent 随机化**，根据入站/出站代理而定
- **POST 速率限制**和**Slowloris 防护**
- 流传输子系统中的**连接节流**
- tunnel 层的**网络拥塞处理**
- **NetDB 隔离**防止跨应用泄漏

---

## 技术细节

- 默认目标密钥大小：516 字节（扩展 LS2 证书可能超出）
- Base32 地址：`{52–56+ 字符}.b32.i2p`
- Server tunnels 与 Java I2P 和 i2pd 保持兼容
- 已弃用功能：仅 `httpbidirserver`；自 0.9.59 版本以来无移除项
- 已验证所有平台的默认端口和文档根目录正确性

---

## 摘要

I2PTunnel 仍然是应用程序与 I2P 集成的核心基础。在 0.9.59 至 2.10.0 版本之间,它获得了持久连接支持、后量子加密以及重大的线程改进。大多数配置保持兼容,但开发者应验证其设置以确保符合现代传输和安全默认值。
