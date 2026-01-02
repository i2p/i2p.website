---
title: "2019年8月会议日程"
date: 2019-07-29
author: "sadie"
description: "I2P 开发者本月将参加多场会议"
---

# 2019年8月会议日程

各位好，


下个月会很忙！在 Defcon 27 的两场工作坊与 I2P 开发者会面，并在 FOCI '19 与一直观察 I2P 审查的研究人员交流。

## I2P for Cryptocurrency Developers

**zzz**

- Monero Village
- August 9, 3:15pm
- Monero Village will be on the 26th floor of Bally's [map](https://defcon.org/html/defcon-27/dc-27-venue.html)

本次工作坊将帮助开发者设计通过 I2P 进行通信的应用程序，以实现匿名性与安全性。我们将讨论加密货币应用的常见需求，并审视各个应用的架构与特定需求；随后，我们将介绍 tunnel 通信、router 与库的选型，以及打包方案的选择，并解答与集成 I2P 相关的所有问题。

目标是创建安全、可伸缩、可扩展且高效的设计方案，以满足每个特定项目的需求。

## 面向加密货币开发者的 I2P

**我不知道**

- Crypto & Privacy Village
- Saturday August 10, 2pm - 3:30pm
- Planet Hollywood [map](https://defcon.org/images/defcon-27/maps/ph-final-public.pdf)
- This workshop is not recorded. So don't miss it!

本工作坊介绍应用程序如何与 I2P 匿名 P2P 网络协同工作的方式。开发者应当了解到，在其应用中使用匿名 P2P 并不必与他们在非匿名 P2P 应用中已经在做的事情有多大不同。它从介绍 I2P 插件系统开始，展示现有插件如何配置自身以通过 I2P 进行通信，以及每种方法的优缺点。随后，我们将继续讲解如何通过其 SAM 和 I2PControl API 以编程方式控制 I2P。最后，我们将深入 SAMv3 API，通过在 Lua 中创建一个使用它的新库，并编写一个简单的应用程序。

## 面向应用程序开发者的 I2P

**萨迪**

- FOCI '19
- Tuesday August 13th 10:30am
- Hyatt Regency Santa Clara
- Co-located with USENIX Security '19
- [Workshop Program](https://www.usenix.org/conference/foci19/workshop-program)

互联网审查的普遍存在推动了多个用于监测过滤活动的测量平台的创建。这些平台面临的一个重要挑战，围绕着测量深度与覆盖广度之间的权衡。在本文中，我们提出了一种机会式的审查测量基础设施，它构建在由志愿者运行的分布式 VPN 服务器网络之上，并据此测量了 I2P 匿名网络在全球范围内被封锁的程度。该基础设施不仅为我们提供了数量众多且地理分布多样的观测点，还使我们能够在网络栈的各个层级开展深入测量。借助该基础设施，我们在全球范围评估了四种不同 I2P 服务的可用性：官方主页、其镜像站点、reseed 服务器（用于分发初始节点信息的服务器），以及网络中的活跃中继节点。在为期一个月内，我们从 164 个国家的 1.7K 个网络位置共进行了 54K 次测量。通过采用多种检测域名封锁、网络数据包注入和拦截页面的技术，我们在五个国家发现了针对 I2P 的审查：中国、伊朗、阿曼、卡塔尔和科威特。最后，我们以讨论在 I2P 上绕过审查的潜在方法作为结论。

**注意：** 原始帖子中引用的图片（monerovillageblog.png、cryptovillageblog.png、censorship.jpg）可能需要添加到 `/static/images/blog/` 目录中。
