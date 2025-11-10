---
title: "如何切换到 StormyCloud Outproxy（出口代理）服务"
date: 2022-08-04
author: "idk"
description: "如何切换到 StormyCloud 出口代理（Outproxy）服务"
categories: ["general"]
---

## 如何切换到 StormyCloud Outproxy 服务

**一个全新的、专业的 Outproxy**

多年来，I2P 一直由一个默认的 outproxy（外部代理）`false.i2p` 提供服务，该 outproxy 的可靠性一直在下降。尽管已有数个竞争者出现以分担部分负载，但它们大多无法在默认情况下自愿为整个 I2P 实现的客户端提供服务。不过，运营 Tor 出口节点的专业非营利组织 StormyCloud 已经启动了一项新的、专业的 outproxy 服务，该服务已由 I2P 社区成员测试，并将在即将发布的版本中成为新的默认 outproxy。

**StormyCloud 是谁**

用他们自己的话说，StormyCloud 是：

> StormyCloud Inc 的使命：捍卫将访问互联网视为一项普遍人权。通过这样做，该组织保护用户的电子隐私，并通过促进不受限制的信息获取，从而推动跨越国界的思想自由交流，构建社区。这至关重要，因为互联网是当下可用于在世界上产生积极影响的最强大工具。

> 硬件：我们拥有全部硬件，当前将设备托管于一家 Tier 4 数据中心。我们目前拥有 10GBps 上行链路，并可在几乎无需改动的情况下升级至 40GBps。我们拥有自己的 ASN（自治系统编号）和 IP 地址空间（IPv4 和 IPv6）。

要了解更多关于 StormyCloud 的信息，请访问其[网站](https://www.stormycloud.org/)。

或者在 [I2P](http://stormycloud.i2p/) 上访问它们。

**切换到 I2P 上的 StormyCloud Outproxy（出口代理）**

要在*今天*切换到 StormyCloud outproxy（出口代理），您可以访问[Hidden Services Manager](http://127.0.0.1:7657/i2ptunnel/edit?tunnel=0)。进入该页面后，您应将 **Outproxies** 和 **SSL Outproxies** 的值更改为 `exit.stormycloud.i2p`。完成后，向下滚动到页面底部并点击“Save”按钮。

**感谢 StormyCloud**

我们感谢 StormyCloud 自愿为 I2P 网络提供高质量的 outproxy（出口代理）服务。
