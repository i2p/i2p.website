---
title: "Bitcoin Core 增加对 I2P 的支持！"
date: 2021-09-18
author: "idk"
description: "新的用例与接受度日益增长的迹象"
categories: ["general"]
---

这是一件酝酿数月的大事：Bitcoin Core 已新增对 I2P 的官方支持！Bitcoin-over-I2P（运行在 I2P 上的 Bitcoin）节点可以在同时运行于 I2P 和 clearnet（明网）的节点帮助下，与其余 Bitcoin 节点进行充分交互，使其成为 Bitcoin 网络中的一等公民。看到像 Bitcoin 这样的大型社区开始关注 I2P 能为他们带来的优势，为全球用户提供隐私与可达性，令人振奋。

## 工作原理

I2P 支持是自动的，通过 SAM API 实现。这同样是令人振奋的消息，因为它凸显了 I2P 的独特强项，例如赋能应用开发者以编程且便捷的方式构建 I2P 连接。通过 I2P 使用 Bitcoin 的用户只需启用 SAM API，并在启用 I2P 的情况下运行 Bitcoin，就可以无需手动配置地使用 I2P。

## 配置您的 I2P Router

为了设置 I2P Router 以为比特币提供匿名连接，需要启用 SAM API。在 Java I2P 中，您应前往 http://127.0.0.1:7657/configclients，并使用“Start”按钮启动 SAM Application Bridge。您也可以通过勾选“Run at Startup”复选框并点击“Save Client Configuration.”来使 SAM Application Bridge 默认启用。

在 i2pd 中，SAM API 通常默认启用，但如果未启用，你应设置：

```
sam.enabled=true
```
在您的 i2pd.conf 文件中。

## 为匿名性和连通性配置您的比特币节点

要在匿名模式下启动 Bitcoin 本身，仍然需要编辑 Bitcoin 数据目录中的一些配置文件。该目录在 Windows 上为 %APPDATA%\Bitcoin，在 Linux 上为 ~/.bitcoin，在 Mac OSX 上为 ~/Library/Application Support/Bitcoin/。此外，还需要至少 22.0.0 版本才能具备 I2P 支持。

按照这些说明操作后，你应当拥有一个私有的比特币节点：I2P 连接使用 I2P，.onion 和 clearnet（明网）连接使用 Tor，从而确保你所有的连接都是匿名的。为方便起见，Windows 用户可通过打开开始菜单并搜索 "Run" 来打开其 Bitcoin 数据目录。在 Run 提示框中，输入 "%APPDATA%\Bitcoin"，然后按 Enter 键。

在该目录中创建一个名为 "i2p.conf." 的文件。在 Windows 上，保存时务必在文件名两侧加上引号，以防 Windows 为该文件添加默认的文件扩展名。该文件应包含以下与 I2P 相关的 Bitcoin 配置选项：

```
i2psam=127.0.0.1:7656
i2pacceptincoming=true
onlynet=i2p
```
接下来，你应该创建另一个名为 "tor.conf." 的文件。该文件应包含以下与 Tor 相关的配置选项：

```
proxy=127.0.0.1:9050
onion=127.0.0.1:9050
onlynet=tor
```
最后，你需要在 Data Directory（数据目录）中的比特币配置文件“bitcoin.conf”里包含这些配置选项。将以下两行添加到你的 bitcoin.conf 文件中：

```
includeconf=i2p.conf
includeconf=tor.conf
```
现在您的比特币节点已配置为仅使用匿名连接。为了启用与远程节点的直接连接，请删除以下开头的行：

```
onlynet=
```
如果您不要求您的比特币节点保持匿名，就可以这样做，这也有助于匿名用户连接到比特币网络的其余部分。
