---
title: "应用程序开发"
description: "为什么要编写 I2P 专用应用程序、关键概念、开发选项以及简单的入门指南"
slug: "applications"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## 为什么要编写专门针对 I2P 的代码？

在 I2P 中使用应用程序有多种方式。使用 [I2PTunnel](/docs/api/i2ptunnel/) 可以让常规应用程序无需编程实现显式的 I2P 支持。这对于客户端-服务器场景非常有效,当你需要连接到单个网站时。你可以简单地使用 I2PTunnel 创建一个 tunnel 来连接该网站,如图 1 所示。

如果你的应用程序是分布式的,它将需要连接到大量的对等节点。使用 I2PTunnel 时,你需要为每个想要联系的对等节点创建一个新的 tunnel,如图 2 所示。这个过程当然可以自动化,但运行大量的 I2PTunnel 实例会产生大量开销。此外,对于许多协议,你需要强制每个人为所有对等节点使用相同的端口集——例如,如果你想可靠地运行 DCC 聊天,每个人都需要约定端口 10001 是 Alice,端口 10002 是 Bob,端口 10003 是 Charlie,依此类推,因为该协议包含 TCP/IP 特定信息(主机和端口)。

通用网络应用程序通常会发送大量可能被用于识别用户的额外数据。主机名、端口号、时区、字符集等信息往往在用户不知情的情况下被发送。因此,在设计网络协议时专门考虑匿名性可以避免暴露用户身份。

在确定如何在 I2P 上进行交互时,还需要考虑效率问题。streaming 库及其之上构建的应用使用类似于 TCP 的握手机制,而核心 I2P 协议(I2NP 和 I2CP)则严格基于消息(类似于 UDP,或在某些情况下类似于原始 IP)。重要的区别在于,I2P 的通信是在长肥网络(long fat network,高延迟高带宽网络)上运行的——每个端到端的消息都会有不小的延迟,但可以包含最多几 KB 的有效载荷。对于只需要简单请求和响应的应用,可以通过使用(尽力而为的)数据报来消除任何状态,并避免启动和关闭握手带来的延迟,而无需担心 MTU 检测或消息分片问题。

<figure style="text-align:center; margin: 2rem 0;">
  <img src="/images/i2ptunnel_serverclient.png" alt="Creating a server-client connection using I2PTunnel only requires creating a single tunnel." />
  <figcaption>Figure 1: Creating a server-client connection using I2PTunnel only requires creating a single tunnel.</figcaption>
</figure>
<figure style="text-align:center; margin: 2rem 0;">
  <img src="/images/i2ptunnel_peertopeer.png" alt="Setting up connections for a peer-to-peer applications requires a very large amount of tunnels." />
  <figcaption>Figure 2: Setting up connections for a peer-to-peer applications requires a very large amount of tunnels.</figcaption>
</figure>
总结来说，编写I2P特定代码有以下几个原因：

- 创建大量的 I2PTunnel 实例会消耗相当可观的资源,这对分布式应用来说是个问题(每个对等节点都需要一个新的 tunnel)。
- 通用网络协议通常会发送大量可用于识别用户身份的额外数据。专门为 I2P 编程可以创建不会泄露此类信息的网络协议,从而保护用户的匿名性和安全性。
- 为常规互联网设计的网络协议在 I2P 上可能效率低下,因为 I2P 是一个延迟要高得多的网络。

I2P 为开发者提供了标准的[插件接口](/docs/specs/plugin/)，以便应用程序可以轻松集成和分发。

用 Java 编写并可通过标准 webapps/app.war 使用 HTML 界面访问/运行的应用程序可能会被考虑纳入 I2P 发行版。

## 重要概念

使用 I2P 时需要适应一些变化：

### 目的地

运行在 I2P 上的应用程序从一个唯一的、具有加密安全性的端点（即"destination"）发送和接收消息。从 TCP 或 UDP 的角度来看,destination 在很大程度上可以被视为等同于主机名加端口号对,尽管存在一些差异。

- I2P destination 本身是一个密码学构造——发送到 destination 的所有数据都会被加密,就像普遍部署了 IPsec 一样,并且端点的(匿名化)位置会被签名,就像普遍部署了 DNSSEC 一样。
- I2P destination 是可移动的标识符——它们可以从一个 I2P router 移动到另一个(甚至可以"多宿主"——同时在多个 router 上运行)。这与 TCP 或 UDP 世界完全不同,在那里单个端点(端口)必须保持在单个主机上。
- I2P destination 又丑又大——在幕后,它们包含一个用于加密的 2048 位 ElGamal 公钥、一个用于签名的 1024 位 DSA 公钥,以及一个可变大小的证书,该证书可能包含工作量证明或盲化数据。

现有一些方法可以用简短易记的名称（例如"irc.duck.i2p"）来引用这些冗长难看的目标地址，但这些技术无法保证全局唯一性（因为它们存储在每个人机器上的本地数据库中），并且当前机制在可扩展性和安全性方面都不够理想（主机列表的更新是通过"订阅"命名服务来管理的）。将来可能会出现某种安全、人类可读、可扩展且全局唯一的命名系统，但应用程序不应依赖于它的存在。有关命名系统的[更多信息](/docs/overview/naming/)可供查阅。

虽然大多数应用程序不需要区分协议和端口,但 I2P *确实*支持它们。复杂的应用程序可以在每条消息的基础上指定协议、源端口和目标端口,以便在单个目标上复用流量。详细信息请参见 [datagram 页面](/docs/api/datagrams/)。简单的应用程序通过监听目标的"所有协议"和"所有端口"来运行。

### 匿名性与保密性

I2P 对网络上传输的所有数据都提供透明的端到端加密和身份验证——如果 Bob 发送数据到 Alice 的 destination（目标节点），只有 Alice 的 destination 能够接收它，并且如果 Bob 使用数据报或流式库，Alice 可以确定数据就是由 Bob 的 destination 发送的。

当然，I2P 透明地匿名化了 Alice 和 Bob 之间发送的数据，但它无法匿名化他们发送的内容本身。例如，如果 Alice 向 Bob 发送一个包含她的全名、政府身份证件和信用卡号码的表单，I2P 对此无能为力。因此，协议和应用程序应该清楚它们试图保护哪些信息以及它们愿意暴露哪些信息。

### I2P 数据报可达数 KB

使用 I2P 数据报（无论是原始数据报还是可回复数据报）的应用程序本质上可以按照 UDP 的方式来理解——数据报是无序的、尽力而为的、无连接的——但与 UDP 不同的是,应用程序不需要担心 MTU 检测,可以直接发送大型数据报。虽然上限名义上是 32 KB,但消息会被分片传输,从而降低整体可靠性。目前不建议使用超过 10 KB 的数据报。详情请参阅[数据报页面](/docs/api/datagrams/)。对于许多应用程序来说,10 KB 的数据足以容纳整个请求或响应,使它们能够在 I2P 中作为类似 UDP 的应用程序透明地运行,而无需编写分片、重发等功能。

## 开发选项

在I2P上有多种发送数据的方式,各有优缺点。streaming lib(流式库)是推荐的接口,被大多数I2P应用程序使用。

### 流媒体库

[完整的流式传输库](/docs/specs/streaming/)现在是标准接口。它允许使用类似 TCP 的套接字进行编程,具体说明请参见[流式传输开发指南](#developing-with-the-streaming-library)。

### BOB

BOB 是 [Basic Open Bridge](/docs/legacy/bob/)，允许任何语言的应用程序与 I2P 建立流式连接。目前它缺少 UDP 支持，但在不久的将来计划添加 UDP 支持。BOB 还包含几个工具，例如目标密钥生成，以及验证地址是否符合 I2P 规范。最新信息和使用 BOB 的应用程序可以在这个 [I2P 站点](http://bob.i2p/) 找到。

### SAM, SAM V2, SAM V3

*不推荐使用 SAM。SAM V2 可以接受，推荐使用 SAM V3。*

SAM 是 [Simple Anonymous Messaging](/docs/legacy/sam/) 协议,允许用任何语言编写的应用程序通过普通 TCP socket 与 SAM bridge 通信,并让该 bridge 多路复用其所有 I2P 流量,透明地协调加密/解密和基于事件的处理。SAM 支持三种操作方式:

- 流(streams),用于当 Alice 和 Bob 想要可靠且有序地相互发送数据时
- 可回复数据报(repliable datagrams),用于当 Alice 想要向 Bob 发送一条 Bob 可以回复的消息时
- 原始数据报(raw datagrams),用于当 Alice 想要尽可能获得最大带宽和性能,而 Bob 不关心数据发送者是否经过身份验证时(例如传输的数据本身具有自身验证能力)

SAM V3 的目标与 SAM 和 SAM V2 相同,但不需要多路复用/解复用。每个 I2P 流都通过应用程序与 SAM 桥接之间各自独立的套接字来处理。此外,应用程序可以通过与 SAM 桥接的数据报通信来发送和接收数据报。

[SAM V2](/docs/legacy/samv2/) 是 imule 使用的新版本,修复了 [SAM](/docs/legacy/sam/) 中的一些问题。

[SAM V3](/docs/api/samv3/) 从 1.4.0 版本开始被 imule 使用。

### I2PTunnel

I2PTunnel 应用程序允许应用通过创建 I2PTunnel "客户端"应用程序（监听特定端口，并在打开该端口的套接字时连接到特定的 I2P destination）或 I2PTunnel "服务器"应用程序（监听特定的 I2P destination，每当收到新的 I2P 连接时就转发到特定的 TCP 主机/端口）来构建特定的类 TCP tunnel 到对等节点。这些数据流是 8 位清洁的，并通过与 SAM 使用的相同 streaming 库进行身份验证和保护，但创建多个独立的 I2PTunnel 实例会产生不小的开销，因为每个实例都有自己独立的 I2P destination 和自己的 tunnel 集、密钥等。

### SOCKS

I2P 支持 SOCKS V4 和 V5 代理。出站连接运行良好。入站（服务器）和 UDP 功能可能不完整且未经测试。

### Ministreaming（迷你流传输）

*已移除*

曾经有一个简单的"ministreaming"库,但现在 ministreaming.jar 只包含完整 streaming 库的接口。

### 数据报

*推荐用于类 UDP 应用*

[数据报库](/docs/api/datagrams/)允许发送类似UDP的数据包。可以使用：

- 可回复数据报
- 原始数据报

### I2CP

*不推荐*

[I2CP](/docs/specs/i2cp/) 本身是一个与语言无关的协议，但要用 Java 以外的语言实现 I2CP 库需要编写大量代码（加密例程、对象编组、异步消息处理等）。虽然可以用 C 或其他语言编写 I2CP 库，但使用 C 语言的 SAM 库可能会更加实用。

### Web 应用程序

I2P 自带 Jetty 网络服务器,改用 Apache 服务器配置起来也很简单。任何标准的 Web 应用技术都应该可以使用。

## 开始开发——简单指南

使用 I2P 进行开发需要一个正常运行的 I2P 安装和您自己选择的开发环境。如果您使用 Java，可以使用 [streaming library](#developing-with-the-streaming-library) 或 datagram library 开始开发。使用其他编程语言时，可以使用 SAM 或 BOB。

### 使用 Streaming 库进行开发

以下是原始页面示例的精简和现代化版本。完整示例请参见旧版页面或代码库中的 Java 示例。

```java
// Server example (excerpt)
I2PSocketManager manager = I2PSocketManagerFactory.createManager();
I2PServerSocket server = manager.getServerSocket();
I2PSocket socket = server.accept();
BufferedReader br = new BufferedReader(new InputStreamReader(socket.getInputStream()));
String s;
while ((s = br.readLine()) != null) {
    System.out.println("Received: " + s);
}
```
*代码示例：接收数据的基本服务器。*

```java
// Client example (excerpt)
I2PSocketManager manager = I2PSocketManagerFactory.createManager();
Destination dest = new Destination(serverDestBase64);
I2PSocket socket = manager.connect(dest);
BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
bw.write("Hello I2P!\n");
bw.flush();
```
*代码示例：客户端连接并发送一行数据。*
