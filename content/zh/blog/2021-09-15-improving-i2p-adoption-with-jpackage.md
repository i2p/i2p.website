---
title: "使用 Jpackage 和 I2P-Zero 提升 I2P 的普及度与上手引导"
date: 2021-09-15
slug: "improving-i2p-adoption-and-onboarding-using-jpackage-i2p-zero"
author: "idk"
description: "在您的应用程序中安装和嵌入 I2P 的多样化和新兴方法"
categories: ["general"]
---

在 I2P 的大部分发展历程中，它一直作为一个应用程序运行，依赖于平台上已安装的 Java 虚拟机。这一直是分发 Java 应用程序的常规方式，但对许多人而言，这导致了较为繁琐的安装过程。更复杂的是，在某一平台上让 I2P 易于安装的 "right answer" 可能与其他平台并不相同。举例来说，在基于 Debian 和 Ubuntu 的操作系统上，使用标准工具安装 I2P 十分简单，因为我们可以在我们的软件包中直接将所需的 Java 组件列为 "Required"；然而在 Windows 或 OSX 上，并没有这样的系统让我们确保已安装兼容的 Java。

显而易见的解决方案是由我们自己管理 Java 的安装，但这本身过去就是一个问题，而且超出了 I2P 的范畴。然而，在较新的 Java 版本中，出现了一组新的选项，有望为许多 Java 软件解决这个问题。这个令人兴奋的工具名为 **"Jpackage."**

## I2P-Zero 和无依赖的 I2P 安装

首个在构建无依赖的 I2P 软件包方面非常成功的尝试是 I2P-Zero，它最初由 Monero 项目创建，供 Monero 加密货币使用。该项目之所以令我们非常兴奋，是因为它成功创建了一个通用的 I2P router，能够轻松与 I2P 应用一起打包。尤其是在 Reddit 上，许多人表达了对设置 I2P-Zero router 简单性的偏好。

这确实向我们证明，使用现代的 Java 工具可以实现一个易于安装的、无依赖的 I2P 软件包，但 I2P-Zero 的使用场景与我们的稍有不同。它最适合那些需要一个 I2P router，并且能够通过其便捷的控制端口（端口号 "8051"）轻松进行控制的嵌入式应用。我们的下一步将是把这项技术适配到通用型 I2P 应用程序上。

## OSX 应用程序安全性更改影响 I2P IzPack 安装程序

在较新的 Mac OSX 版本中，这个问题变得更加迫切，因为无法再轻松使用以 .jar 格式提供的“Classic”安装程序。这是因为该应用程序未通过 Apple 官方的“公证”，因此被视为安全风险。**然而**，Jpackage 可以生成 .dmg 文件，该文件可以由 Apple 官方进行公证，从而方便地解决我们的问题。

由 Zlatinb 创建的全新 I2P .dmg 安装程序，使在 OSX 上安装 I2P 比以往任何时候都更容易，不再需要用户自行安装 Java，并按照规定的方式使用标准的 OSX 安装工具。新的 .dmg 安装程序让在 Mac OSX 上设置 I2P 比以往任何时候都更容易。

获取 [dmg](https://geti2p.net/en/download/mac)

## 未来的 I2P 易于安装

我最常从用户那里听到的一件事是，如果 I2P 想要被广泛采用，就必须让人们容易上手。许多人希望有一种“类似 Tor Browser 的”用户体验，引用（或转述）许多熟悉的 Reddit 用户的话。安装不应要求繁琐且容易出错的“安装后”步骤。许多新用户并没有做好以全面、完整的方式处理其浏览器配置的准备。为了解决这个问题，我们创建了 I2P Profile Bundle，它会配置 Firefox，使其能自动“开箱即用”地使用 I2P。随着它的发展，它添加了安全功能，并改进了与 I2P 本身的集成。在其最新版本中，它**also**捆绑了一个完整的、由 Jpackage 驱动的 I2P Router。I2P Firefox Profile 现在是一个面向 Windows 的完整 I2P 发行版，唯一剩余的依赖只有 Firefox 本身。这应当为 Windows 上的 I2P 用户提供前所未有的便利。

获取[安装程序](https://geti2p.net/en/download#windows)
