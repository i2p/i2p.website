---
title: "隐私解决方案的诞生"
date: 2014-08-15
author: "Meeh"
description: "组织启动"
categories: ["press"]
---

大家好！

今天我们宣布 Privacy Solutions 项目，这是一个开发并维护 I2P 软件的新组织。Privacy Solutions 包含多项新的开发工作，旨在基于 I2P 协议和技术，为用户提升隐私、安全和匿名性。

这些努力包括：

1. The Abscond browser bundle.
2. The i2pd C++ router project.
3. The "BigBrother" I2P network monitoring project.
4. The Anoncoin crypto-coin project.
5. The Monero crypto-coin project.

Privacy Solutions 的初始资金由 Anoncoin 和 Monero 项目的支持者提供。Privacy Solutions 是一家总部位于挪威的非营利性质组织，已在挪威政府的登记册中注册。（有点类似于美国的 501(c)3。）

Privacy Solutions 计划向挪威政府申请网络研究资助，鉴于 BigBrother（我们稍后会解释那是什么）以及那些计划将低时延网络作为主要传输层的代币。我们的研究将推动匿名性、安全性和隐私方面的软件技术取得进步。

首先简单介绍一下 Abscond Browser Bundle（Abscond 浏览器套件）。它最初是 Meeh 的个人项目，后来朋友们开始提交补丁；现在该项目正在尝试像 Tor 的浏览器套件那样，为 I2P 提供同样便捷的使用体验。我们的首个发行版已不远，只剩下一些 gitian 脚本任务，包括设置 Apple 工具链。此外，在宣布其为稳定版之前，我们将从 Java 实例中借助 PROCESS_INFORMATION（一个 C 语言结构体，用于保存进程的重要信息）对 I2P 进行监控。I2pd 也会在它准备就绪后替换 Java 版本，捆绑包中再附带 JRE 就没有意义了。你可以在 https://hideme.today/dev 了解有关 Abscond Browser Bundle 的更多信息。

我们还想通报 i2pd 的当前现状。I2pd 现在支持双向流式传输（bi-directional streaming），这使得不仅可以使用 HTTP，还可以使用长连接通信通道。已添加对 IRC 的即时支持。I2pd 用户能够像使用 Java I2P 一样使用它来访问 I2P IRC 网络。I2PTunnel 是 I2P 网络的关键功能之一，使非 I2P 应用程序能够透明通信。因此，它对 i2pd 至关重要，也是关键里程碑之一。

最后，如果你熟悉 I2P，你可能知道 Bigbrother.i2p，这是 Meeh 在一年多前制作的一个指标系统。最近我们注意到，自初始上线以来，Meeh 实际上从各节点的上报中拥有 100Gb 的非重复数据。这些数据也将迁移到 Privacy Solutions，并使用 NSPOF（无单点故障）后端重写。同时我们也将开始使用 Graphite (http://graphite.wikidot.com/screen-shots)。这将使我们能够在不给终端用户带来隐私问题的情况下，获得对网络的出色总体概览。客户端会过滤除国家、router hash 和 tunnel 构建成功率之外的所有数据。像往常一样，这项服务的名称是 Meeh 的一个小玩笑。

我们在这里对新闻稍作精简；如果你对更多信息感兴趣，请访问 https://blog.privacysolutions.no/ 我们仍在建设中，更多内容即将推出！

如需更多信息，请联系：press@privacysolutions.no

致以诚挚的问候，

Mikal "Meeh" Villa
