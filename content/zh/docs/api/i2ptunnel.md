---
title: "I2PTunnel"
description: "用于与I2P接口并在I2P上提供服务的工具"
slug: "i2ptunnel"
aliases:
  - "/zh/i2ptunnel"
  - "/zh/i2ptunnel/"
  - "/zh/i2ptunnel_migration"
  - "/zh/i2ptunnel_migration/"
  - "/zh/i2ptunnel_services"
  - "/zh/i2ptunnel_services/"
lastUpdated: "2023-10"
accurateFor: "0.9.59"
---

## 概述 {#overview}

I2PTunnel 是一个在 I2P 上提供接口和服务的工具。I2PTunnel 的目标可以使用 [hostname](/docs/overview/naming)、[Base32](/docs/overview/naming#base32) 或完整的 516 字节 destination key 来定义。建立的 I2PTunnel 将在您的客户端机器上以 localhost:port 的形式可用。如果您希望在 I2P 网络上提供服务，只需创建指向相应 ip_address:port 的 I2PTunnel。系统将为该服务生成相应的 516 字节 destination key，并使其在整个 I2P 网络中可用。I2PTunnel 管理的网页界面可在 [localhost:7657/i2ptunnel/](http://localhost:7657/i2ptunnel/) 访问。

## 默认服务 {#default-services}

### 服务器 Tunnel {#default-server-tunnels}

- **I2P Webserver** - 一个指向运行在 [localhost:7658](http://localhost:7658) 上的 Jetty webserver 的 tunnel，用于在 I2P 上方便快速地托管网站。
  文档根目录为：
  - **Unix** - `$HOME/.i2p/eepsite/docroot`
  - **Windows** - `%LOCALAPPDATA%\I2P\I2P Site\docroot`，展开为：`C:\Users\**username**\AppData\Local\I2P\I2P Site\docroot`

### 客户端隧道 {#default-client-tunnels}

- **I2P HTTP Proxy** - *localhost:4444* - 一个用于通过 I2P 匿名浏览 I2P 网络和普通互联网的 HTTP 代理。通过 I2P 浏览互联网使用由 "Outproxies:" 选项指定的随机代理。
- **Irc2P** - *localhost:6668* - 到默认匿名 IRC 网络 Irc2P 的 IRC tunnel。
- **gitssh.idk.i2p** - *localhost:7670* - 项目 Git 存储库的 SSH 访问
- **smtp.postman.i2p** - *localhost:7659* - 由 hq.postman.i2p 的 postman 提供的 SMTP 服务
- **pop3.postman.i2p** - *localhost:7660* - hq.postman.i2p 的 postman 配套 POP 服务

## 配置 {#configuration}

[I2PTunnel 配置](/docs/specs/configuration)

## 客户端模式 {#client-modes}

### 标准 {#client-modes-standard}

打开一个本地 TCP 端口，连接到 I2P 网络内目标地址上的服务（如 HTTP、FTP 或 SMTP）。tunnel 会定向到逗号分隔（", "）的目标地址列表中的随机主机。

### HTTP {#client-mode-http}

一个HTTP客户端tunnel。该tunnel连接到HTTP请求中URL指定的目标地址。如果提供outproxy，支持代理到互联网。会从HTTP连接中移除以下headers：

- **Accept\*:** (不包括 "Accept" 和 "Accept-Encoding") 因为它们在不同浏览器之间差异很大，可以被用作识别符。
- **Referer:**
- **Via:**
- **From:**

HTTP客户端代理提供了多项服务来保护用户并提供更好的用户体验。

**请求头处理：** - 删除有隐私问题的请求头 - 路由到本地或远程出口代理 - 出口代理选择、缓存和可达性跟踪 - 主机名到目标地址查找 - 将主机头替换为 b32 - 添加头部以指示支持透明解压缩 - 强制连接：关闭 - 符合 RFC 的代理支持 - 符合 RFC 的逐跳头部处理和删除 - 可选的摘要和基本用户名/密码认证 - 可选的出口代理摘要和基本用户名/密码认证 - 为了提高效率，在传递前缓存所有头部 - 跳转服务器链接 - 跳转响应处理和表单（地址助手） - 盲化 b32 处理和凭证表单 - 支持标准 HTTP 和 HTTPS（CONNECT）请求

**响应头处理：** - 检查是否需要解压缩响应 - 强制连接：关闭 - 符合RFC规范的逐跳头处理和剥离 - 缓冲所有头信息以提高传输效率

**HTTP 错误响应：** - 针对许多常见和不太常见的错误，让用户了解发生了什么 - 超过 20 个独特的已翻译、已设计样式和格式化的错误页面，用于各种错误 - 内部 web 服务器用于提供表单、CSS、图片和错误页面

#### 透明响应压缩 {#transparent-response-compression}

i2ptunnel 响应压缩通过以下 HTTP 头部请求：

- **X-Accept-Encoding:** x-i2p-gzip;q=1.0, identity;q=0.5, deflate;q=0, gzip;q=0, *;q=0

服务器端在将请求发送到 web 服务器之前会剥离这个逐跳标头。不需要包含所有 q 值的复杂标头；服务器只需在标头中的任何位置查找 "x-i2p-gzip" 即可。

服务器端根据从网络服务器接收到的标头来决定是否压缩响应，包括 Content-Type、Content-Length 和 Content-Encoding，以评估响应是否可压缩以及是否值得消耗额外的 CPU 资源。如果服务器端压缩了响应，它会添加以下 HTTP 标头：

- **Content-Encoding:** x-i2p-gzip

如果响应中存在此标头，HTTP 客户端代理会透明地解压缩它。客户端会剥离此标头并在将响应发送给浏览器之前进行 gunzip 解压。请注意，我们在 I2CP 层仍然有底层的 gzip 压缩，如果响应在 HTTP 层没有被压缩，这种压缩仍然有效。

这种设计和当前实现在多个方面违反了 RFC 2616：

- X-Accept-Encoding 不是标准头部
- 不会按跳进行去分块/分块；它会端到端地传递分块
- 端到端传递 Transfer-Encoding 头部
- 使用 Content-Encoding 而不是 Transfer-Encoding 来指定每跳编码
- 当设置了 Content-Encoding 时禁止 x-i2p gzip 压缩（但我们可能本来也不想这样做）
- 服务器端对服务器发送的分块内容进行 gzip 压缩，而不是进行去分块-gzip-重新分块和去分块-gunzip-重新分块操作
- gzip 压缩后的内容不会再进行分块。RFC 2616 要求除"identity"以外的所有 Transfer-Encoding 都必须分块
- 因为在 gzip 外部（之后）没有分块，更难找到数据的结尾，这使得任何 keepalive 的实现都更加困难
- RFC 2616 规定如果存在 Transfer-Encoding 就不能发送 Content-Length，但我们这样做了。规范说如果存在 Transfer-Encoding 就忽略 Content-Length，浏览器确实这样做了，所以对我们来说是有效的

以向后兼容的方式实现符合标准的逐跳压缩的变更是进一步研究的主题。对 dechunk-gzip-rechunk 的任何变更都需要新的编码类型，可能是 x-i2p-gzchunked。这将与 Transfer-Encoding: gzip 相同，但出于兼容性原因必须采用不同的信号方式。任何变更都需要正式的提案。

#### 透明请求压缩 {#transparent-request-compression}

不支持，尽管 POST 会从中受益。请注意，我们在 I2CP 层仍然有底层的 gzip 压缩。

#### 持久性 {#persistence}

客户端和服务器代理目前在三个跳点（浏览器套接字、I2P套接字、服务器套接字）上都不支持RFC 2616 HTTP持久套接字。在每个跳点都会注入Connection: close头。实现持久连接的更改正在研究中。这些更改应该符合标准并向后兼容，不需要正式提案。

#### 流水线 {#pipelining}

客户端和服务器代理目前不支持 RFC 2616 HTTP 流水线技术，也没有计划支持。现代浏览器不支持通过代理进行流水线处理，因为大多数代理无法正确实现此功能。

#### 兼容性 {#compatibility}

代理实现必须与另一端的其他实现正确协作。客户端代理应该能够在服务器端没有HTTP感知的服务器代理（即标准tunnel）的情况下正常工作。并非所有实现都支持x-i2p-gzip。

#### 用户代理 {#user-agent}

根据tunnel是否使用outproxy，它会附加以下User-Agent：

- *Outproxy:* **User-Agent:** 使用来自 Windows 上最新 Firefox 版本的用户代理
- *内部 I2P 使用:* **User-Agent:** MYOB/6.66 (AN/ON)

### IRC 客户端 {#client-mode-irc}

创建一个连接到随机 IRC 服务器的连接，该服务器由逗号分隔（", "）的目标列表指定。由于匿名性考虑，仅允许使用白名单中的 IRC 命令子集。

以下允许列表用于从IRC服务器发送到IRC客户端的命令。

**允许列表：** - AUTHENTICATE - CAP - ERROR - H - JOIN - KICK - MODE - NICK - PART - PING - PROTOCTL - QUIT - TOPIC - WALLOPS

还有一个允许列表用于从IRC客户端发往IRC服务器的命令。由于IRC管理命令数量众多，该列表相当庞大。详情请查看IRCFilter.java源代码。

出站过滤器还会修改以下命令以删除识别信息：- NOTICE - PART - PING - PRIVMSG - QUIT - USER

### SOCKS 4/4a/5 {#client-mode-socks}

启用将 I2P router 用作 SOCKS 代理。

### SOCKS IRC {#client-mode-socks-irc}

启用将 I2P router 用作 SOCKS 代理，使用由 [IRC](#client-mode-irc) 客户端模式指定的命令白名单。

### CONNECT {#client-mode-connect}

创建一个 HTTP tunnel 并使用 HTTP 请求方法 "CONNECT" 来构建一个 TCP tunnel，通常用于 SSL 和 HTTPS。

### Streamr {#client-mode-streamr}

创建一个附加到 Streamr 客户端 I2PTunnel 的 UDP 服务器。streamr 客户端 tunnel 将订阅 streamr 服务器 tunnel。

![Streamr 图表](/images/I2PTunnel-streamr.png)

## 服务器模式 {#server-modes}

### 标准 {#server-mode-standard}

创建一个到本地 ip:port 的目标，并开放一个 TCP 端口。

### HTTP {#server-mode-http}

创建一个到本地HTTP服务器ip:port的destination。支持对带有Accept-encoding: x-i2p-gzip的请求进行gzip压缩，并在此类请求中以Content-encoding: x-i2p-gzip进行回复。

HTTP服务器代理提供多种服务，使网站托管更简单、更安全，并在客户端提供更好的用户体验。

**请求头处理：** - 头部验证 - 头部欺骗保护 - 头部大小检查 - 可选的入代理和用户代理拒绝 - 添加 X-I2P 头部，让网络服务器知道请求来自哪里 - 主机头部替换，使网络服务器虚拟主机更容易 - 强制连接：关闭 - 符合 RFC 标准的逐跳头部处理和剥离 - 缓冲所有头部后再传递以提高效率

**DDoS 防护：** - POST 限流 - 超时和 slowloris 攻击防护 - 所有 tunnel 类型在流传输中都有额外的限流机制

**响应头处理：** - 移除一些有隐私问题的头信息 - 检查 MIME 类型和其他头信息以决定是否压缩响应 - 强制连接：关闭 - 符合 RFC 标准的逐跳头信息处理和移除 - 为提高效率，在传递前缓冲所有头信息

**HTTP 错误响应：** - 针对许多常见和不常见的错误以及限流情况，让客户端用户知道发生了什么

**透明响应压缩：** - Web 服务器和/或 I2CP 层可能会进行压缩，但 Web 服务器通常不会压缩，而且在高层进行压缩是最有效的，即使 I2CP 也会压缩。HTTP 服务器代理与客户端代理协同工作，透明地压缩响应。

### HTTP 双向 {#server-mode-http-bidir}

*已弃用*

既可作为 I2PTunnel HTTP 服务器，也可作为不具备出口代理功能的 I2PTunnel HTTP 客户端。示例应用包括执行客户端类型请求的 Web 应用程序，或作为诊断工具对 I2P 站点进行环回测试。

### IRC 服务器 {#server-mode-irc}

创建一个destination，用于过滤客户端的注册序列，并将客户端的destination密钥作为主机名传递给IRC服务器。

### Streamr {#server-mode-streamr}

创建了一个连接到媒体服务器的UDP客户端。该UDP客户端与Streamr服务器I2PTunnel耦合。
