---
title: "夏季开发回顾：API"
date: 2016-07-02
author: "str4d"
description: "在 Summer Dev 的第一个月里，我们改进了面向 Java、Android 和 Python 开发者的 API 的易用性。"
categories: ["summer-dev"]
---

夏季开发正如火如荼地进行：我们忙着润滑各个环节、打磨细节、把环境收拾得井井有条。现在是时候发布我们的首次汇总，让你及时了解我们取得的进展！

## API 月

我们本月的目标是 "融入" - 使我们的 API 和库能够在各个社区的现有基础设施中工作，从而让应用开发者更高效地使用 I2P，用户也无需关注细节。

### Java / Android

I2P 客户端库现已在 Maven Central（Maven 中央仓库）上提供！这将使 Java 开发者在其应用程序中使用 I2P 变得更加简单。相比以往需要从现有安装中获取这些库，他们现在只需将 I2P 添加到其依赖中即可。升级到新版本也同样会更加容易。

I2P Android 客户端库也已更新，以使用新的 I2P 库。这意味着跨平台应用程序可以原生地与 I2P Android 或桌面版 I2P 协同工作。

### Java / Android

#### txi2p

Twisted 插件 `txi2p` 现在支持 I2P 内部端口，并可在本地、远程以及经端口转发的 SAM API 上无缝工作。有关使用说明，请查阅其文档，并在 GitHub 上报告任何问题。

#### i2psocket

`i2psocket` 的首个（测试版）版本已发布！它是标准 Python `socket` 库的直接替代品，并通过 SAM API 增加了对 I2P 的支持。请查看其 GitHub 页面以获取使用说明，并报告任何问题。

### Python

- zzz has been hard at work on Syndie, getting a headstart on Plugins month
- psi has been creating an I2P test network using i2pd, and in the process has found and fixed several i2pd bugs that will improve its compatibility with Java I2P

## Coming up: Apps month!

我们很高兴在七月与 Tahoe-LAFS 合作！长期以来，I2P 一直托管着最大的公共网格之一，使用的是打了补丁的 Tahoe-LAFS 版本。在应用月期间，我们将协助他们推进为 I2P 和 Tor 添加原生支持的工作，使 I2P 用户能够从上游的所有改进中受益。

我们还将与其他几个项目就其 I2P 集成计划进行沟通，并在设计方面提供帮助。敬请期待！

## Take part in Summer Dev!

在这些领域，我们还有许多希望落实的想法。如果你对隐私和匿名软件的开发、设计易用的网站或界面，或为用户撰写指南感兴趣：欢迎在 IRC 或 Twitter 上来和我们聊天！我们始终乐于欢迎新成员加入我们的社区。

我们会在这里随时更新；同时，你也可以在 Twitter 上使用标签 #I2PSummer 关注我们的进展，并分享你的想法和成果。让我们迎接夏天吧！
