---
title: "I2P: 一个可扩展的匿名通信框架"
description: "I2P 架构和运行的技术介绍"
slug: "tech-intro"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## 简介

I2P 是一个可扩展、自组织、弹性的分组交换匿名网络层,可以在其上运行任意数量的不同的注重匿名性或安全性的应用程序。这些应用程序可以各自在匿名性、延迟和吞吐量之间进行权衡,而无需担心自由路由混合网络的正确实现,从而使它们的活动能够融入已经在 I2P 上运行的更大匿名用户群体中。

已有的应用程序提供了完整的典型互联网活动范围——**匿名**网页浏览、网站托管、聊天、文件共享、电子邮件、博客和内容聚合，以及其他几个正在开发中的应用程序。

- **网页浏览：** 使用任何支持代理的现有浏览器
- **聊天：** IRC 和其他协议
- **文件共享：** [I2PSnark](#i2psnark) 和其他应用程序
- **电子邮件：** [Susimail](#i2pmail) 和其他应用程序
- **博客：** 使用任何本地网络服务器，或可用的插件

与托管在内容分发网络（如 [Freenet](/docs/overview/comparison#freenet) 或 [GNUnet](https://www.gnunet.org/)）中的网站不同，I2P 上托管的服务是完全交互式的——有传统的网页式搜索引擎、公告板、可以评论的博客、数据库驱动的站点，以及无需在本地安装即可查询静态系统（如 Freenet）的桥接服务。

通过所有这些支持匿名的应用程序，I2P 作为**面向消息的中间件**运行——应用程序指定要发送到加密标识符（一个"destination"）的数据，I2P 确保其安全且匿名地到达。I2P 还包含一个简单的[流式传输库](#streaming)，允许 I2P 的匿名尽力传输消息作为可靠的、有序的流进行传输，提供针对网络高带宽延迟积调优的基于 TCP 的拥塞控制。

虽然已经开发了简单的 SOCKS 代理来连接现有应用程序,但其价值有限,因为大多数应用程序在匿名环境中会泄露敏感信息。最安全的方法是**审计和改造**应用程序,使其直接使用 I2P 的 API。

I2P 不是一个研究项目——无论是学术性、商业性还是政府性质的——而是一项旨在提供可用匿名性的工程实践。自 2003 年初以来,它一直由分布在全球的贡献者团队持续开发。所有 I2P 工作都是在[官方网站](https://geti2p.net/)上的**开源**项目,主要发布到公共领域,部分组件采用宽松的 BSD 风格许可证。还有几个采用 GPL 许可的客户端应用程序可用,例如 [I2PTunnel](#i2ptunnel)、[Susimail](#i2pmail) 和 [I2PSnark](#i2psnark)。资金完全来自用户捐赠。

---

## 操作

### Overview

I2P 明确区分了 router（参与网络的节点）和 destination（应用程序的匿名端点）。运行 I2P 本身并不是秘密；隐藏的是用户**正在做什么**以及他们的 destination 使用哪个 router。终端用户通常运行多个 destination（例如，一个用于网页浏览，另一个用于托管服务，还有一个用于 IRC）。

I2P 中的一个关键概念是 **tunnel**（隧道）——一条通过一系列 router 的单向加密路径。每个 router 只解密一层，并且只知道下一跳。Tunnel 每 10 分钟过期一次，必须重新构建。

![入站和出站隧道示意图](/images/tunnels.png)   *图1：存在两种类型的tunnel——inbound和outbound。*

- **Outbound tunnels** 将消息从创建者发送出去。
- **Inbound tunnels** 将消息带回创建者。

结合这些可以实现双向通信。例如，"Alice"使用outbound tunnel发送到"Bob"的inbound tunnel。Alice用路由指令加密她的消息发送到Bob的inbound gateway。

另一个关键概念是**网络数据库**（network database 或 netDb），它分发关于 router 和目的地的元数据：

- **RouterInfo:** 包含路由器联系信息和密钥材料。  
- **LeaseSet:** 包含联系目标地址所需的信息(tunnel 网关、过期时间、加密密钥)。

路由器直接将其 RouterInfo 发布到 netDb；而 LeaseSet 则通过出站 tunnel 发送以保护匿名性。

为了构建隧道，Alice 向 netDb 查询 RouterInfo 条目以选择节点，并逐跳发送加密的隧道构建消息，直到隧道建立完成。

![路由器信息用于构建隧道](/images/netdb_get_routerinfo_2.png)   *图 2：路由器信息用于构建隧道。*

要向 Bob 发送数据，Alice 查找 Bob 的 LeaseSet，并使用她的一条出站 tunnel 将数据路由到 Bob 的入站 tunnel 网关。

![LeaseSet 连接入站和出站隧道](/images/netdb_get_leaseset.png)   *图 3：LeaseSet 连接出站和入站隧道。*

因为 I2P 是基于消息的，它添加了**端到端 garlic encryption（大蒜加密）**来保护消息，即使从出站端点或入站网关也无法窥探。一个 garlic 消息包裹多个加密的"cloves"（消息片段）以隐藏元数据并提高匿名性。

应用程序可以直接使用消息接口，或者依赖[流式库](#streaming)来建立可靠的连接。

---

### Tunnels

入站和出站隧道都使用分层加密,但构建方式有所不同:

- 在**入站 tunnel** 中，创建者（端点）解密所有层。
- 在**出站 tunnel** 中，创建者（网关）预先解密各层，以确保端点的清晰性。

I2P通过延迟和可靠性等间接指标对节点进行分析，无需直接探测。基于这些分析结果，节点被动态分组为四个层级：

1. 快速且高容量
2. 高容量
3. 未失败
4. 失败中

Tunnel 对等节点选择通常优先选择高容量的对等节点,随机选择以平衡匿名性和性能,并采用额外的基于 XOR 的排序策略来缓解前驱攻击和 netDb 收集。

有关更深入的细节，请参阅 [Tunnel 规范](/docs/specs/implementation)。

---

### 概述

参与 **floodfill** 分布式哈希表（DHT）的 router 会存储并响应 LeaseSet 查询。该 DHT 使用 [Kademlia](https://en.wikipedia.org/wiki/Kademlia) 的一个变体。Floodfill router 会在具有足够容量和稳定性时自动选择,也可以手动配置。

- **RouterInfo:** 描述一个 router 的能力和传输方式。  
- **LeaseSet:** 描述一个 destination 的 tunnel 和加密密钥。

netDb 中的所有数据都由发布者签名并加上时间戳,以防止重放攻击或过期条目攻击。时间同步通过 SNTP 和传输层偏差检测来维护。

#### Additional concepts

- **未发布和加密的 LeaseSet：**  
  目的地可以通过不发布其 LeaseSet 来保持私密性，仅与受信任的对等节点共享。访问需要相应的解密密钥。

- **引导启动（重新种子化）：**  
  新的 router 需要从可信的 HTTPS reseed 服务器获取已签名的 RouterInfo 文件来加入网络。

- **查找可扩展性：**  
  I2P 使用**迭代式**而非递归式查找来提高 DHT 可扩展性和安全性。

---

### 隧道

现代 I2P 通信使用两种完全加密的传输协议：

- **[NTCP2](/docs/specs/ntcp2):** 基于加密 TCP 的协议  
- **[SSU2](/docs/specs/ssu2):** 基于加密 UDP 的协议

两者都构建于现代 [Noise Protocol Framework](https://noiseprotocol.org/) 之上,提供强大的身份验证和抵抗流量指纹识别的能力。它们取代了旧版 NTCP 和 SSU 协议(自 2023 年起已完全停用)。

**NTCP2** 通过 TCP 提供加密、高效的流式传输。

**SSU2** 提供基于 UDP 的可靠性、NAT 穿透和可选的打洞功能。SSU2 在概念上类似于 WireGuard 或 QUIC，在可靠性和匿名性之间取得平衡。

Router 可能同时支持 IPv4 和 IPv6,在 netDb 中发布其传输地址和成本。连接的传输方式通过**竞价系统**动态选择,以优化条件和现有链接。

---

### 网络数据库 (netDb)

I2P 在所有组件中使用分层加密：传输层、tunnel、garlic 消息和 netDb。

当前的基本组件包括：

- X25519 用于密钥交换
- EdDSA (Ed25519) 用于签名
- ChaCha20-Poly1305 用于认证加密
- SHA-256 用于哈希
- AES256 用于 tunnel 层加密

旧版算法（ElGamal、DSA-SHA1、ECDSA）保留以实现向后兼容性。

I2P 目前正在引入混合后量子 (PQ) 密码学方案，将 **X25519** 与 **ML-KEM** 结合，以抵御"现在收集，以后解密"攻击。

#### Garlic Messages

Garlic 消息通过将多个加密的"瓣"（cloves）与独立的传递指令组合在一起来扩展洋葱路由。这些允许消息级别的路由灵活性和统一的流量填充。

#### Session Tags

支持两种端到端加密的密码学系统：

- **ElGamal/AES+SessionTags (传统方式):**  
  使用预先传递的会话标签作为 32 字节随机数。现已弃用,因为效率低下。

- **ECIES-X25519-AEAD-Ratchet（当前）：**  
  使用 ChaCha20-Poly1305 和同步的基于 HKDF 的 PRNG 来动态生成临时会话密钥和 8 字节标签,在保持前向保密性的同时减少 CPU、内存和带宽开销。

---

## Future of the Protocol

关键研究领域聚焦于维护针对国家级对手的安全性以及引入后量子保护。两个早期设计概念——**受限路由**和**可变延迟**——已被现代发展所取代。

### Restricted Route Operation

最初的受限路由概念旨在隐藏IP地址。这一需求已在很大程度上通过以下方式得到缓解:

- UPnP 自动端口转发
- SSU2 中的强大 NAT 穿透
- IPv6 支持
- 协作式介绍节点和 NAT 打洞
- 可选的覆盖网络（如 Yggdrasil）连接

因此，现代 I2P 无需复杂的受限路由即可更实际地实现相同目标。

---

## Similar Systems

I2P整合了面向消息的中间件、分布式哈希表(DHT)和混合网络(mixnet)的概念。其创新之处在于将这些技术结合成一个可用的、自组织的匿名平台。

### 传输协议

*[网站](https://www.torproject.org/)*

**Tor** 和 **I2P** 有着共同的目标，但在架构上有所不同：

- **Tor:** 电路交换；依赖可信的目录授权机构。（约1万个中继节点）  
- **I2P:** 分组交换；完全分布式的 DHT 驱动网络。（约5万个 routers）

I2P的单向tunnel暴露更少的元数据并允许灵活的路由路径,而Tor专注于匿名的**互联网访问(outproxying出口代理)**。I2P则支持匿名的**网络内托管**。

### 密码学

*[网站](https://freenetproject.org/)*

**Freenet** 专注于匿名、持久的文件发布和检索。相比之下，**I2P** 提供了一个用于交互式使用（网页、聊天、种子下载）的**实时通信层**。这两个系统相互补充——Freenet 提供抗审查的存储；I2P 提供传输匿名性。

### Other Networks

- **Lokinet:** 基于IP的覆盖网络,使用激励性服务节点。
- **Nym:** 下一代混合网络,强调通过覆盖流量进行元数据保护,但延迟较高。

---

## Appendix A: Application Layer

I2P 本身仅处理消息传输。应用层功能通过 API 和库在外部实现。

### Streaming Library {#streaming}

**流式库（streaming library）**作为 I2P 的 TCP 类似物发挥作用，采用滑动窗口协议和针对高延迟匿名传输优化的拥塞控制。

由于消息捆绑优化，典型的 HTTP 请求/响应模式通常可以在单次往返中完成。

### Naming Library and Address Book

*开发者：mihi, Ragnarok*   请参阅[命名和地址簿](/docs/overview/naming)页面。

I2P的命名系统是**本地和去中心化的**，避免了类似DNS的全局名称。每个router在本地维护一个从人类可读名称到目标地址的映射。可选的基于信任网络的地址簿可以从可信节点共享或导入。

这种方法避免了中心化权威机构，并规避了全局或投票式命名系统中固有的女巫攻击(Sybil attack)漏洞。

### 受限路由操作

*开发者：mihi*

**I2PTunnel** 是主要的客户端层接口，用于实现匿名 TCP 代理。它支持：

- **客户端 tunnel**（出站到 I2P 目的地）  
- **HTTP 客户端 (eepproxy)** 用于 ".i2p" 域名  
- **服务器 tunnel**（从 I2P 入站到本地服务）  
- **HTTP 服务器 tunnel**（安全代理 Web 服务）

出站代理(到常规互联网)是可选的,由志愿者运行的"服务器"隧道实现。

### I2PSnark {#i2psnark}

*开发者：jrandom 等人 — 从 [Snark](http://www.klomp.org/snark/) 移植*

I2P 自带的 **I2PSnark** 是一个匿名多种子 BitTorrent 客户端,支持 DHT 和 UDP,可通过 Web 界面访问。

### Tor

*开发者：postman, susi23, mastiejaner*

**I2Pmail** 通过 I2PTunnel 连接提供匿名电子邮件服务。**Susimail** 是一个专门构建的基于网页的客户端,用于防止传统电子邮件客户端中常见的信息泄露。[mail.i2p](https://mail.i2p/) 服务具有病毒过滤、[hashcash](https://en.wikipedia.org/wiki/Hashcash) 配额以及 outproxy 分离等功能,以提供额外的保护。

---
