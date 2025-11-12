---
title: "下载 I2P"
description: "下载适用于 Windows、macOS、Linux、Android 等的最新版本 I2P"
type: "下载"
layout: "downloads"
current_version: "2.10.0"
android_version: "2.10.1"
downloads: I2P 是一个匿名网络，旨在保护用户的隐私和安全。通过使用路由器和隧道，I2P 能够隐藏用户的 IP 地址，并确保通信的匿名性。I2P 的网络数据库（netDb）存储了所有参与者的路由信息，允许数据包在网络中有效地传输。

I2P 支持多种协议，包括 NTCP2 和 SSU，这些协议用于在路由器之间建立安全连接。用户可以通过 I2PTunnel 访问 eepsite（托管在 I2P 网络上的网站），并使用 SAMv3 接口与 I2P 网络进行编程交互。

为了进一步增强隐私，I2P 使用大蒜加密（garlic encryption）技术，将多个消息封装在一起，增加了流量分析的难度。通过这种方式，I2P 提供了一个强大的工具来保护用户的在线活动免受监视和跟踪。
windows: I2P 是一个用于匿名通信的网络层。它通过使用路由器和隧道来保护用户的隐私。I2P 的核心组件包括 `router`, `tunnel`, `leaseSet`, 和 `netDb`。这些组件共同协作，以确保用户的通信是安全和匿名的。

在 I2P 中，`floodfill` 节点负责存储和传播网络数据库信息。它们是网络的关键部分，帮助其他路由器找到彼此。I2P 支持多种传输协议，包括 `NTCP2` 和 `SSU`，以便在不同的网络条件下提供灵活性。

用户可以通过 `SAMv3` 接口与 I2P 网络进行交互，或者使用 `I2PTunnel` 来访问 eepsite（I2P 内部网站）。`I2CP` 和 `I2NP` 是 I2P 的协议，用于在路由器之间传递信息。

大蒜加密（garlic encryption）是 I2P 的一项关键技术，允许将多个消息捆绑在一起进行传输，从而提高匿名性和效率。
file: "i2pinstall_2.10.0-0_windows.exe"
size: "~24M"
requirements: "需要 Java"
sha256: "f96110b00c28591691d409bd2f1768b7906b80da5cab2e20ddc060cbb4389fbf"
links: 在I2P网络中，通信通过多个“隧道”进行路由，以确保隐私和匿名性。每个I2P路由器都可以创建入站和出站隧道，这些隧道由多个“跳跃”组成。跳跃是指数据包在到达最终目的地之前经过的中间路由器。

I2P使用“蒜头加密”来保护数据，这种加密方法允许多个消息被打包在一起，以提高效率和安全性。每个消息都被加密，并且只有最终接收者能够解密它。

为了参与I2P网络，路由器必须与其他路由器交换信息。这是通过“网络数据库”（netDb）实现的，netDb存储了关于路由器和租赁集（leaseSet）的信息。租赁集包含了如何到达某个特定服务的信息。

I2P支持多种协议，包括NTCP2和SSU，这些协议用于路由器之间的通信。为了与I2P网络进行交互，用户可以使用I2PTunnel或SAMv3等工具。

I2P的一个常见用例是托管“eepsite”，这是一种通过I2P访问的网站。eepsite提供了与传统互联网网站类似的功能，但具有更高的隐私保护。
primary: "https://i2p.net/files/2.10.0/i2pinstall_2.10.0-0_windows.exe"
mirror: "https://mirror.stormycloud.org/2.10.0/i2pinstall_2.10.0-0_windows.exe"
torrent: "magnet:?xt=urn:btih:75d8c74e9cc52f5cb4982b941d7e49f9f890c458&dn=i2pinstall_2.10.0-0_windows.exe&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=http%3A%2F%2Ftracker2.postman.i2p%2Fannounce&tr=http%3A%2F%2Fopentracker.simp.i2p%2Fa&tr=http%3A%2F%2Fopentracker.skank.i2p%2Fa&tr=http%3A%2F%2Fopentracker.dg2.i2p%2Fa&tr=udp%3A%2F%2Fdht.transmissionbt.com%3A6881&tr=udp%3A%2F%2Fdht.aelitis.com%3A6881&tr=udp%3A%2F%2Frouter.bittorrent.com%3A6881"
i2p: "http://mirror.stormycloud.i2p/2.10.0/i2pinstall_2.10.0-0_windows.exe"
tor: "http://hhn4r4qyrmplmfiermza6p3d67a5ra7ecwjeoo5a5ddiogwhyjg675id.onion/2.10.0/i2pinstall_2.10.0-0_windows.exe"
windows_easy_installer: 以下是 I2P 网络的基本概述。I2P 是一个匿名网络，旨在保护用户的隐私和安全。通过使用路由器和隧道，I2P 可以隐藏用户的 IP 地址，并确保通信的匿名性。

## 主要功能

- **匿名通信**：I2P 使用大蒜加密来保护数据传输。
- **去中心化**：网络数据库（netDb）分布在多个节点上，消除了单点故障。
- **灵活的协议**：支持多种协议，包括 HTTP、SMTP 和 BitTorrent。

## 如何开始

1. 下载并安装 I2P 软件。
2. 配置您的路由器以连接到 I2P 网络。
3. 使用 I2PTunnel 设置您的 eepsite（I2P 内部网站）。

有关更多信息，请访问 [I2P 官方网站](https://geti2p.net)。
file: "I2P-Easy-Install-Bundle-2.10.0-signed.exe"
size: "~162M"
requirements: "无需 Java - 捆绑 Java 运行时"
sha256: "afcc937004bcf41d4dd2e40de27f33afac3de0652705aef904834fd18afed4b6"
beta: true
links: I2P 是一个用于匿名通信的网络层。它通过使用路由器和隧道来保护用户的隐私。I2P 网络中的每个节点都运行一个路由器，该路由器负责管理入站和出站的流量。用户可以通过创建入站和出站隧道来发送和接收数据。

I2P 使用大蒜加密来确保数据的安全性。每个数据包都被加密并通过多个节点传输，以防止流量分析。I2P 的主要组件包括路由器、隧道、leaseSet 和 netDb。

要开始使用 I2P，用户需要下载并安装 I2P 软件。安装完成后，用户可以通过访问本地控制台来配置他们的路由器。I2P 提供了多种协议支持，包括 NTCP2 和 SSU，用于节点之间的通信。

I2P 还支持创建和访问 eepsite，这是一种托管在 I2P 网络上的匿名网站。用户可以使用 I2PTunnel 和 SAMv3 接口来与 I2P 网络进行交互。

有关更多信息，请访问 [I2P 官方网站](https://geti2p.net)。
primary: "https://i2p.net/files/2.10.0/I2P-Easy-Install-Bundle-2.10.0-signed.exe"
mirror: "https://mirror.stormycloud.org/2.10.0/I2P-Easy-Install-Bundle-2.10.0-signed.exe"
torrent: "magnet:?xt=urn:btih:79e1172aaa21e5bd395a408850de17eff1c5ec24&dn=I2P-Easy-Install-Bundle-2.10.0-signed.exe&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=http%3A%2F%2Ftracker2.postman.i2p%2Fannounce&tr=http%3A%2F%2Fopentracker.simp.i2p%2Fa&tr=http%3A%2F%2Fopentracker.skank.i2p%2Fa&tr=http%3A%2F%2Fopentracker.dg2.i2p%2Fa&tr=udp%3A%2F%2Fdht.transmissionbt.com%3A6881&tr=udp%3A%2F%2Fdht.aelitis.com%3A6881&tr=udp%3A%2F%2Frouter.bittorrent.com%3A6881"
i2p: "http://mirror.stormycloud.i2p/2.10.0/I2P-Easy-Install-Bundle-2.10.0-signed.exe"
tor: "http://hhn4r4qyrmplmfiermza6p3d67a5ra7ecwjeoo5a5ddiogwhyjg675id.onion/2.10.0/I2P-Easy-Install-Bundle-2.10.0-signed.exe"
mac_linux: I2P 是一个用于匿名通信的网络层。它通过使用路由器和隧道来隐藏用户的身份和位置。I2P 的主要组件包括路由器、隧道、leaseSet 和 netDb。路由器负责在网络中传递数据包，而隧道则用于在网络中创建匿名路径。leaseSet 是一个包含加密信息的数据结构，用于在网络中定位服务。netDb 是一个分布式数据库，存储有关网络参与者的信息。

I2P 支持多种协议，包括 NTCP2 和 SSU，这些协议用于在路由器之间建立连接。I2P 还提供了 SAMv3 和 I2PTunnel 等接口，允许应用程序与 I2P 网络进行交互。I2CP 是路由器与客户端之间的通信协议，而 I2NP 是用于在路由器之间传输数据的协议。

I2P 使用大蒜加密（garlic encryption）来保护数据的隐私和完整性。大蒜加密将多个消息捆绑在一起进行加密，从而提高安全性。I2P 网络中的网站称为 eepsite，它们通过 I2P 隧道进行访问。

要开始使用 I2P，用户需要下载并安装 I2P 软件。安装完成后，用户可以通过浏览器访问 I2P 控制台来配置和管理他们的路由器。
file: "i2pinstall_2.10.0.jar"
size: "约30M"
requirements: "Java 8 或更高版本"
sha256: "76372d552dddb8c1d751dde09bae64afba81fef551455e85e9275d3d031872ea"
links: 在I2P网络中，`router`是一个核心组件，负责管理`tunnel`和`leaseSet`。`router`通过`netDb`（网络数据库）与其他`router`交换信息。为了提高网络的可靠性和速度，某些`router`被配置为`floodfill`节点。

I2P支持多种传输协议，包括`NTCP2`和`SSU`。用户可以通过`SAMv3`接口与I2P网络进行交互，或者使用`I2PTunnel`来访问`eepsite`（I2P网站）。

配置I2P时，用户需要编辑`router.config`文件，并确保正确设置`I2CP`和`I2NP`参数。`garlic encryption`（大蒜加密）用于保护数据的隐私和安全。
primary: "https://i2p.net/files/2.10.0/i2pinstall_2.10.0.jar"
mirror: "https://mirror.stormycloud.org/2.10.0/i2pinstall_2.10.0.jar"
torrent: "magnet:?xt=urn:btih:20ce01ea81b437ced30b1574d457cce55c86dce2&dn=i2pinstall_2.10.0.jar&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=http%3A%2F%2Ftracker2.postman.i2p%2Fannounce&tr=http%3A%2F%2Fopentracker.simp.i2p%2Fa&tr=http%3A%2F%2Fopentracker.skank.i2p%2Fa&tr=http%3A%2F%2Fopentracker.dg2.i2p%2Fa&tr=udp%3A%2F%2Fdht.transmissionbt.com%3A6881&tr=udp%3A%2F%2Fdht.aelitis.com%3A6881&tr=udp%3A%2F%2Frouter.bittorrent.com%3A6881"
i2p: "http://mirror.stormycloud.i2p/2.10.0/i2pinstall_2.10.0.jar"
tor: "http://hhn4r4qyrmplmfiermza6p3d67a5ra7ecwjeoo5a5ddiogwhyjg675id.onion/2.10.0/i2pinstall_2.10.0.jar"
source: I2P 是一个匿名网络层，旨在保护用户的隐私和自由。它通过使用加密和动态路由来隐藏用户的身份和位置。I2P 网络由多个组件组成，包括路由器、隧道和 leaseSet。用户可以通过 I2P 访问 eepsite（托管在 I2P 网络上的网站）或使用 I2PTunnel 进行安全通信。

### 如何开始使用 I2P

1. 下载并安装 I2P 软件。
2. 启动 I2P 路由器控制台。
3. 配置您的浏览器以使用 I2P 代理。
4. 探索 I2P 网络中的 eepsite。

### 常见问题

- **I2P 如何保护我的隐私？**
  I2P 使用大蒜加密和动态路由来确保通信的安全性和匿名性。

- **如何配置 I2P 路由器？**
  通过路由器控制台，您可以调整带宽设置、管理隧道和查看网络数据库（netDb）信息。

- **什么是 floodfill？**
  floodfill 是一种特殊的路由器，负责存储和传播网络数据库信息，以提高网络的可靠性和可用性。

有关更多信息，请访问 [I2P 官方网站](https://geti2p.net)。
file: "i2psource_2.10.0.tar.bz2"
size: "~33M"
sha256: "3b651b761da530242f6db6536391fb781bc8e07129540ae7e96882bcb7bf2375"
links: ```
# I2P 网络概述

I2P 是一个匿名网络，旨在保护用户的隐私和自由。它通过使用路由器和隧道来隐藏用户的身份和位置。I2P 网络中的每个节点都可以是一个客户端或服务器，或者两者兼而有之。

## 路由器和隧道

在 I2P 中，路由器负责管理网络流量，而隧道则用于传输数据。每个隧道由多个路由器组成，以确保数据的安全性和匿名性。

## 数据库和 floodfill

I2P 使用一个分布式数据库（称为 netDb）来存储网络信息。某些路由器被指定为 floodfill 路由器，负责传播和存储这些信息。

## 传输协议

I2P 支持多种传输协议，包括 NTCP2 和 SSU。这些协议用于在路由器之间安全地传输数据。

## 使用 I2P

要使用 I2P，用户需要安装一个 I2P 路由器软件。安装后，用户可以通过 I2PTunnel 访问 eepsite（I2P 网络中的网站）或使用 SAMv3 接口与其他应用程序集成。

## 安全性和隐私

I2P 使用大蒜加密来保护用户的数据和隐私。通过这种加密方法，数据被分成多个加密层，只有目标节点才能解密。

## 结论

I2P 提供了一种强大的工具来保护用户的在线隐私。通过使用路由器、隧道和大蒜加密，I2P 确保用户的通信是安全和匿名的。
```
primary: "https://i2p.net/files/2.10.0/i2psource_2.10.0.tar.bz2"
torrent: "magnet:?xt=urn:btih:f62f519204abefb958d553f737ac0a7e84698f35&dn=i2psource_2.10.0.tar.bz2&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=http%3A%2F%2Ftracker2.postman.i2p%2Fannounce&tr=http%3A%2F%2Fopentracker.simp.i2p%2Fa&tr=http%3A%2F%2Fopentracker.skank.i2p%2Fa&tr=http%3A%2F%2Fopentracker.dg2.i2p%2Fa&tr=udp%3A%2F%2Fdht.transmissionbt.com%3A6881&tr=udp%3A%2F%2Fdht.aelitis.com%3A6881&tr=udp%3A%2F%2Frouter.bittorrent.com%3A6881"
github: "https://github.com/i2p/i2p.i2p"
android: 以下是 I2P 网络的基本概念和术语：

### I2P 网络架构

I2P 是一个匿名网络，旨在保护用户的隐私和安全。它通过使用多个加密层（称为大蒜加密）来实现这一点。I2P 网络由多个组件组成，包括路由器、隧道和网络数据库（netDb）。

- **路由器**：I2P 网络中的每个节点都运行一个路由器。路由器负责管理隧道和处理数据包。
- **隧道**：数据在 I2P 网络中通过隧道传输。每个隧道由多个路由器组成，确保数据的匿名性。
- **网络数据库（netDb）**：这是一个分布式数据库，存储有关路由器和租赁集（leaseSet）的信息。它使用泛洪填充（floodfill）机制来分发信息。

### 连接协议

I2P 支持多种连接协议，包括 NTCP2 和 SSU。这些协议用于在路由器之间建立安全连接。

- **NTCP2**：一种基于 TCP 的协议，提供可靠的连接。
- **SSU**：一种基于 UDP 的协议，适用于不可靠的网络环境。

### 应用接口

I2P 提供多种接口供应用程序使用，包括 SAMv3 和 I2PTunnel。

- **SAMv3**：一个简单的异步消息传递协议，允许应用程序与 I2P 网络进行通信。
- **I2PTunnel**：一个用于创建隧道的工具，支持多种服务类型，包括 HTTP 和 SOCKS 代理。

### 其他重要概念

- **租赁集（leaseSet）**：包含有关隧道的信息，用于在 I2P 网络中路由数据。
- **大蒜加密**：一种多层加密技术，确保数据的安全性和匿名性。
- **泛洪填充（floodfill）**：一种用于分发网络数据库信息的机制。

通过理解这些基本概念，用户可以更好地利用 I2P 网络来保护他们的隐私和安全。
file: "I2P.apk"
version: "2.10.1"
size: "~28 MB"
requirements: "Android 4.0+，最低512MB RAM"
sha256: "c3d4e5f6789012345678901234567890123456789012345678901234abcdef"
links: ### I2P 网络概述

I2P 是一个匿名网络，旨在保护用户的隐私和自由。它通过使用路由器和隧道来隐藏用户的身份和位置。I2P 网络中的每个节点都充当路由器，帮助传递加密信息。

#### 如何工作

I2P 使用大蒜加密来保护数据，并通过 `leaseSet` 和 `netDb` 来管理网络中的节点信息。`floodfill` 节点负责存储和传播网络数据库信息。

#### 连接类型

I2P 支持多种连接类型，包括 NTCP2 和 SSU，这些协议用于在路由器之间传输数据。用户可以通过 SAMv3 接口与 I2P 网络进行交互。

#### 托管 eepsite

要托管一个 eepsite，用户需要配置 `I2PTunnel` 来处理入站和出站流量。通过 `I2CP` 协议，用户可以管理他们的隧道和服务。

#### 结论

I2P 提供了一种强大的工具来保护在线隐私，使用户能够在不暴露身份的情况下安全地通信和共享信息。
primary: "https://download.i2p.io/android/I2P.apk"
torrent: "magnet:?xt=urn:btih:android_example"
i2p: "http://stats.i2p/android/I2P.apk"
mirrors: I2P 是一个用于匿名通信的网络层。它通过使用路由器和隧道来隐藏用户的 IP 地址，从而保护用户的隐私。I2P 网络中的每个节点都可以充当路由器，帮助转发流量。用户可以通过创建入站和出站隧道来发送和接收数据。

I2P 使用大蒜加密来确保数据的安全性。大蒜加密允许多个消息被打包在一起，从而提高了效率和安全性。I2P 网络数据库（netDb）存储了有关路由器和租赁集（leaseSet）的信息，帮助节点找到彼此。

为了连接到 I2P 网络，用户需要运行一个 I2P 路由器。路由器可以通过 NTCP2 和 SSU 协议与其他节点通信。I2P 还支持通过 SAMv3 和 I2PTunnel 等接口与应用程序集成。

要托管一个 eepsite（I2P 上的匿名网站），用户需要配置一个 I2P 隧道。I2P 隧道允许用户通过 I2P 网络访问和提供服务。配置文件通常位于 `i2ptunnel.config` 中。

I2P 的设计目标是提供一个去中心化和动态的网络，能够抵抗流量分析攻击。通过使用 I2CP 和 I2NP 协议，I2P 实现了灵活的消息传递和路由。
primary: 以下是I2P网络的基本概念：

### I2P网络概述

I2P（The Invisible Internet Project）是一个匿名网络层，旨在保护用户的隐私和安全。I2P通过使用路由器和隧道来隐藏用户的IP地址，从而实现匿名通信。

### 路由器和隧道

在I2P中，路由器是负责数据传输的节点。每个用户运行一个路由器，它通过多个隧道发送和接收数据。隧道是由多个路由器组成的路径，用于在网络中传输信息。

### 数据库和floodfill

I2P使用一个分布式数据库（netDb）来存储路由器和隧道的信息。某些路由器被称为floodfill路由器，它们负责将信息传播到整个网络。

### 加密和安全

I2P使用大蒜加密（garlic encryption）来保护数据的机密性。每个数据包包含多个消息，这些消息被加密并通过隧道发送，以确保安全性。

### 结论

I2P提供了一种强大的工具来保护用户的隐私。通过使用路由器、隧道和加密技术，I2P确保了用户的在线活动保持匿名和安全。
name: "StormyCloud"
location: "美国"
url: "https://stormycloud.org"
resources: 请确保您的 I2P 路由器已正确配置并正在运行。要检查路由器状态，请访问 `http://127.0.0.1:7657` 并查看控制台页面。如果您看到“Network: OK”，则表示路由器正常工作。

### 配置 I2PTunnel

1. 打开 I2P 控制台。
2. 导航到“隧道”页面。
3. 点击“创建新客户端隧道”。
4. 输入所需的设置，例如目标地址和端口。
5. 保存更改并启动隧道。

### 使用 SAMv3 接口

SAMv3 提供了一种与 I2P 网络进行交互的简单方法。要使用 SAMv3，您需要确保在 `i2p.config` 文件中启用了 SAMv3 服务。然后，您可以通过编程语言的库连接到 SAMv3 端口。

### 监控网络数据库 (netDb)

I2P 使用分布式网络数据库来存储路由器信息。要监控 netDb 活动，请在控制台中查看“网络数据库”部分。您可以看到 floodfill 路由器的状态和当前的 leaseSet 信息。

通过遵循这些步骤，您可以有效地管理和监控您的 I2P 环境。
archive: "https://download.i2p.io/archive/"
pgp_keys: "/downloads/pgp-keys"
---
