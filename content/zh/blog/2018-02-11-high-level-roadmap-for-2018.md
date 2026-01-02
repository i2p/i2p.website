---
title: "2018 年总体路线图"
date: 2018-02-11
slug: "high-level-roadmap-for-2018"
author: "str4d"
description: "2018 年将是新协议、新合作以及更明确的聚焦之年"
categories: ["roadmap"]
---

我们在 34C3 讨论的诸多议题之一，是来年应当将重点放在哪里。具体来说，我们希望制定一份路线图，清晰地区分我们要确保完成的事项与“如果能拥有就很不错”的事项，并且能够帮助新加入的贡献者在这两类工作中顺利上手。以下是我们的结论：

## 优先级：新的密码学！

许多当前的原语和协议仍保留着大约2005年的原始设计，需要改进。我们就此已有若干公开的提案和设想多年，但推进一直很慢。我们一致认为，这需要成为我们2018年的首要任务。核心组件包括：

- New transport protocols (to replace NTCP and SSU). See [Prop111](https://geti2p.net/spec/proposals/111).
- New onion-encryption protocol for building and using tunnels.
- New NetDB datatypes to enable enhanced Destinations. See [Prop123](https://geti2p.net/spec/proposals/123).
- Upgraded end-to-end protocol (replacing ElGamal).

围绕这一优先事项的工作分为几个方面：

- Writing proposals.
- Writing working implementations of them that we can test.
- Reviewing proposals.

如果不在所有这些方面开展工作，我们无法在整个网络范围内发布新的协议规范。

## 可选但有益: 代码复用

现在开始开展上述工作的一个好处在于，在过去的几年里，已经有一些独立的努力致力于创建简单的协议和协议框架，它们实现了我们为自身协议设定的许多目标，并且在更广泛的社区中获得了认可和采用。通过利用这些工作，我们能够获得"force multiplier"（倍增效应）：

- We benefit from protocol designs, security proofs, and code written by others, reducing the amount of work we need to do for the same level of feature-completeness and security assurances.

- Work we do can be leveraged by other communities, increasing their interest in collaborating with us, and thinking about I2P as a whole.

我的提案特别将借助[Noise Protocol Framework（Noise 协议框架）](https://noiseprotocol.org/)，以及[SPHINX packet format（SPHINX 数据包格式）](https://katzenpost.mixnetworks.org/docs/specs/sphinx.html)。为此，我已经与 I2P 社区之外的几位人士安排好了合作！

## 优先级：明网协作

说到这个话题，在过去大约六个月里，我们一直在逐步吸引更多关注。在 PETS2017、34C3 和 RWC2018 上，我就如何改进与更广泛社区的协作进行了几次非常好的讨论。这对于确保我们能够为新协议争取尽可能多的评审非常重要。我看到的最大障碍在于：目前大多数 I2P 的开发协作都是在 I2P 本身内部进行的，这大大增加了参与贡献所需的工作量。

The two priorities in this area are:

- Set up a project-run development forum that is accessible both inside and outside I2P.

- Set up mailing lists for review and discussion of proposals (possibly connected to the above forum).

其他被归类为可选的目标：

- Set up a usable git-to-mtn pathway, to enable us to effectively solicit clearnet contributions on GitHub while keeping the canonical dev environment on Monotone.

- Write a "position paper" that accurately explains I2P to academic audiences, and puts it in context with existing literature.

我预计与 I2P 之外的人开展的合作将完全在 GitHub 上进行，以尽量减少摩擦。

## 优先事项：为长生命周期发布做准备

I2P 现已进入 Debian Sid（其不稳定仓库），预计在大约一年半后会稳定下来，并且也已被收录进 Ubuntu 软件仓库，计划纳入四月发布的下一个 LTS 版本。我们将开始面对会多年留存的 I2P 版本，我们需要确保能够在网络中妥善应对它们的存在。

这里的首要目标是在接下来的一年内尽可能多地部署新协议，以赶上下一版 Debian 稳定发行版。对于那些需要历时数年才能完成部署的协议，我们应尽早纳入前向兼容性更改。

## 优先事项：现有应用的插件化

Debian 模型鼓励为不同组件提供独立的软件包。我们一致认为，将当前捆绑的 Java 应用程序与核心 Java router 解耦，会带来多方面的益处：

- It codifies the boundary between the applications and the router.

- It should make it easier to get these apps running with non-Java routers.

- It would enable third parties to create "I2P bundles" containing just the applications they want.

结合先前的优先事项，这使得 I2P 主项目更朝向类似于 Linux 内核的方向发展。我们将花更多时间聚焦于网络本身，让第三方开发者专注于使用该网络的应用（在过去几年我们对 API 和库所做的工作之后，这件事已显著变得更容易）。

## 锦上添花：应用改进

我们有一系列应用层面的改进想要推进，但鉴于我们还有其他优先事项，目前没有足够的开发时间来处理。这正是我们非常希望看到新贡献者加入的领域！一旦上述解耦完成，任何人都将能够在不依赖主 Java router（路由器）的情况下，显著更容易地独立开发某个特定应用。

我们非常希望有人能协助的其中一个应用是 I2P Android。我们将与 I2P 核心版本保持同步更新，并尽可能修复缺陷，但在改进底层代码以及可用性方面仍有许多工作可以做。

## 优先级：Susimail 和 I2P-Bote 稳定化

话虽如此，我们确实希望在近期专门着手 Susimail 和 I2P-Bote 的修复（其中一些已合入 0.9.33）。过去几年里，与其他 I2P 应用相比，它们的维护工作较少，因此我们想花些时间让它们的代码库达到同等水平，并让新贡献者更容易上手！

## 加分项：工单分诊

在多个 I2P 子系统和应用中，我们积压了大量工单。作为上述稳定化工作的一部分，我们希望清理一些长期存在的旧问题。更重要的是，我们要确保工单得到正确归类，以便新贡献者能够找到合适的工单来开展工作。

## 优先级：用户支持

我们将重点关注的一个方面，是与那些花时间报告问题的用户保持联系。谢谢！我们把反馈循环做得越短，就能越快解决新用户遇到的问题，他们继续参与社区的可能性也就越大。

## 我们非常欢迎你的帮助！

这些看起来都很有雄心，而且的确如此！不过，上面许多事项彼此重叠，通过周密的规划，我们可以在这些方面取得实质性进展。

如果你有兴趣帮助我们实现上述任何目标，欢迎来和我们聊聊！你可以在 OFTC 和 Freenode（#i2p-dev）以及 Twitter（@GetI2P）找到我们。
