---
title: "I2P 简介"
description: "I2P匿名网络的非技术性介绍"
slug: "intro"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "needs-review"
---

## 什么是 I2P？

The Invisible Internet Project (I2P) 是一个匿名网络层,支持抗审查的点对点通信。通过加密用户流量并将其通过由全球志愿者运行的分布式网络发送,实现匿名连接。

## 主要特性

### Anonymity

I2P 隐藏了消息的发送方和接收方。与传统互联网连接中您的 IP 地址对网站和服务可见不同,I2P 使用多层加密和路由来保护您的身份隐私。

### Decentralization

I2P 中没有中央权威机构。网络由志愿者维护,他们贡献带宽和计算资源。这使得它能够抵御审查和单点故障。

### 匿名性

I2P 内的所有流量都经过端到端加密。消息在网络中传输时会被多次加密,这与 Tor 的工作方式类似,但在实现上存在重要差异。

## How It Works

### 去中心化

I2P 使用"隧道"(tunnel)来路由流量。当你发送或接收数据时:

1. 你的路由器创建一个出站隧道(用于发送)
2. 你的路由器创建一个入站隧道(用于接收)
3. 消息经过加密并通过多个 router 发送
4. 每个 router 只知道前一跳和下一跳,不知道完整路径

### 端到端加密

I2P 通过"garlic encryption"改进了传统的洋葱路由:

- 多个消息可以捆绑在一起(就像一头大蒜中的蒜瓣)
- 这提供了更好的性能和额外的匿名性
- 使流量分析更加困难

### Network Database

I2P 维护一个分布式网络数据库，包含：

- 路由器信息
- 目标地址(类似于 .i2p 网站)
- 加密的路由数据

## Common Use Cases

### 隧道

访问或托管以 `.i2p` 结尾的网站 - 这些网站只能在 I2P 网络内访问,为主机和访问者提供强大的匿名性保障。

### Garlic Routing

通过 I2P 使用 BitTorrent 匿名分享文件。许多种子应用程序内置了 I2P 支持。

### 网络数据库

使用 I2P-Bote 或其他为 I2P 设计的电子邮件应用程序发送和接收匿名电子邮件。

### Messaging

通过 I2P 网络私密地使用 IRC、即时通讯或其他通信工具。

## Getting Started

准备尝试 I2P 了吗?查看我们的[下载页面](/downloads)以在您的系统上安装 I2P。

如需了解更多技术细节，请参阅[技术介绍](/docs/overview/tech-intro)或浏览完整的[文档](/docs)。

## 工作原理

- [技术介绍](/docs/overview/tech-intro) - 深入了解技术概念
- [威胁模型](/docs/overview/threat-model) - 理解 I2P 的安全模型
- [与 Tor 的比较](/docs/overview/comparison) - I2P 与 Tor 的区别
- [密码学](/docs/specs/cryptography) - I2P 加密算法详解
