---
title: "认识你的维护者：StormyCloud"
date: 2022-09-07
author: "sadie"
description: "An interview with the maintainers of the StormyCloud Outproxy"
categories: ["general"]
---

## 与 StormyCloud Inc. 的对话

随着最新的 [I2P Java 发行版](https://geti2p.net/en/blog/2022/08/22/1.9.0-Release)，针对新的 I2P 安装，现有的 outproxy（出口代理）false.i2p 已被新的 StormyCloud outproxy 所替换。对于正在更新其 router 的用户，切换到 Stormycloud 服务可以很快完成。

在您的 Hidden Services Manager（隐藏服务管理器）中，将 Outproxies（出口代理）和 SSL Outproxies（SSL 出口代理）都更改为 exit.stormycloud.i2p，然后点击页面底部的保存按钮。

## StormyCloud Inc 是什么公司？

**StormyCloud Inc. 的使命**

捍卫互联网接入作为一项普遍人权。通过这样做，该组织保护用户的电子隐私，并通过促进对信息的不受限制的获取来建设社区，从而实现跨越国界的思想自由交流。这一点至关重要，因为互联网是当前能够为世界带来积极改变的最强大工具。

**愿景声明**

成为向宇宙中每一个人提供自由、开放互联网的先驱，因为互联网接入是基本人权 ([https://stormycloud.org/about-us/](https://stormycloud.org/about-us/))

我与 Dustin 见面打了个招呼，并进一步讨论了隐私、像 StormyCloud 这样的服务的必要性，以及促使该公司选择 I2P 的原因。

**创立 StormyCloud 的灵感来源是什么？**

2021 年底，我在 /r/tor 子版块上。有人在一个关于如何使用 Tor 的帖子里回复，谈到自己依靠 Tor 与家人保持联系。该用户的家人住在美国，但他/她当时身处一个互联网访问非常受限的国家。他/她必须对与谁交流以及说些什么格外谨慎。正因如此，他/她依赖 Tor。这让我想到：我可以在没有恐惧或限制的情况下与人沟通，而这本应对所有人都一样。

StormyCloud 的目标是尽我们所能，帮助尽可能多的人实现这一点。

**在启动 StormyCloud 的过程中遇到了哪些挑战？**

成本——贵得离谱。我们选择走数据中心这条路，因为我们所做的规模不是家庭网络所能实现的。既有设备开支，也有经常性的托管成本。

在成立非营利组织方面，我们借鉴了 Emerald Onion 的做法，并参考了他们的一些文档和总结的经验教训。Tor 社区提供了许多非常有用的资源。

**外界对你们的服务反响如何？**

在7月，我们通过所有服务处理了15亿次 DNS 请求。人们很欣赏我们不进行日志记录。数据根本不存在，而人们就喜欢这样。

**什么是 outproxy（出口代理）？**

outproxy（出口代理）类似于 Tor 的出口节点，它允许明网（普通互联网）流量通过 I2P 网络中继。换言之，它使 I2P 用户能够借助 I2P 网络的安全性访问互联网。

**What is special about the StormyCloud I2P Outproxy?**

首先，我们采用多宿主（multi-homed）架构，这意味着有多台服务器提供 outproxy（外部代理）流量服务。这确保该服务对社区始终可用。我们服务器上的所有日志每 15 分钟清空一次。这确保无论是执法机构还是我们自己都无法访问任何数据。我们支持通过 outproxy 访问 Tor 的 .onion 链接，而且我们的 outproxy 速度相当快。

**您如何定义隐私？您认为在越权与数据处理方面存在哪些问题？**

隐私是免受未经授权访问的自由。透明性很重要，例如采用选择加入机制——以 GDPR（欧盟通用数据保护条例）的要求为例。

一些大型公司正在囤积数据，并将其用于 [无需令状访问位置信息](https://www.eff.org/deeplinks/2022/08/fog-revealed-guided-tour-how-cops-can-browse-your-location-data)。科技公司正在对人们认为、且理应属于私密的内容过度介入，例如照片或消息。

持续开展关于如何保障通信安全，以及哪些工具或应用程序能够帮助实现这一点的宣传与教育非常重要。我们与外界信息的交互方式同样重要。我们需要信任，但要验证。

**I2P 如何与 StormyCloud 的使命与愿景声明相契合？**

I2P 是一个开源项目，其所提供的内容与 StormyCloud Inc. 的使命相一致。I2P 为流量和通信提供一层隐私和保护，该项目认为每个人都享有隐私权。

我们在 2022 年初与 Tor 社区的人交谈时了解到 I2P，并且很喜欢该项目正在做的事情。它看起来与 Tor 类似。

在我们介绍 I2P 及其功能时，我们意识到需要一个可靠的 outproxy（外部代理）。I2P 社区的成员给予了我们极大的支持，帮助我们创建并开始提供 outproxy 服务。

**结论**

对于我们在线生活中本应私密之事遭到监控的现象，保持警觉的必要性始终存在。任何数据的收集都应基于当事人的同意，隐私应当是默认的。

当我们无法信任我们的流量或通信不会在未经同意的情况下被监视时，所幸我们仍可接入那些从设计上就会对流量进行匿名化并隐藏我们位置的网络。

感谢 StormyCloud 以及所有为 Tor 和 I2P 提供 outproxies（出口代理）或节点的人，使人们在需要时能够更安全地访问互联网。我期待有更多人把这些互补网络的能力桥接起来，为所有人打造一个更健壮的隐私生态系统。

在 [https://stormycloud.org/](https://stormycloud.org/) 了解更多关于 StormyCloud Inc. 的服务，并通过在 [https://stormycloud.org/donate/](https://stormycloud.org/donate/) 捐款来支持他们的工作。
