---
title: "2018 年总体路线图"
date: 2018-02-11
slug: "high-level-roadmap-for-2018"
author: "str4d"
description: "2018年将是新协议、新合作涌现、关注重点更加明确的一年。"
categories: ["roadmap"]
---

在 34C3 上，我们讨论的诸多话题之一是来年应当把重点放在哪里。尤其是，我们希望制定一份清晰的路线图，明确哪些是我们必须确保完成的，哪些是如果能够实现就更理想的，并且能够帮助新加入者上手参与这两类工作。以下是我们的结论：

## 优先级：新的密码（学！）

许多现有的原语和协议仍沿用大约 2005 年的最初设计，亟需改进。多年来我们一直有若干公开提案和设想，但推进一直很慢。我们一致认为，这需要成为我们 2018 年的首要任务。核心组成包括：

- New transport protocols (to replace NTCP and SSU). See Prop111.
- New onion-encryption protocol for building and using tunnels.
- New NetDB datatypes to enable enhanced Destinations. See Prop123.
- Upgraded end-to-end protocol (replacing ElGamal).

围绕这一优先事项的工作分为几个方面：

- Writing proposals.
- Writing working implementations of them that we can test.
- Reviewing proposals.

如果不在所有这些领域开展工作，我们无法在整个网络范围内发布新的协议规范。

## 加分项：代码复用

现在开始上述工作的一个好处在于：在过去几年里，已有一些相互独立的努力致力于创建简单的协议和协议框架，它们实现了我们为自己的协议设定的许多目标，并已在更广泛的社区中获得了认可和采用。通过利用这些工作，我们可以获得一种 "倍增效应"：

- We benefit from protocol designs, security proofs, and code written by others, reducing the amount of work we need to do for the same level of feature-completeness and security assurances.

- Work we do can be leveraged by other communities, increasing their interest in collaborating with us, and thinking about I2P as a whole.

我的提案将特别利用 [Noise Protocol Framework（Noise 协议框架）](https://noiseprotocol.org/)，以及 [SPHINX packet format（SPHINX 数据包格式）](https://katzenpost.mixnetworks.org/docs/specs/sphinx.html)。为此，我已经与 I2P 之外的几位人士安排了合作！

## 优先级: 明网协作

关于这个话题，在过去大约六个月里，我们一直在逐步引起关注。在 PETS2017、34C3 和 RWC2018 期间，我就如何改进与更广泛社区的协作进行了很好的讨论。这对于确保我们能为新协议争取尽可能多的评审非常重要。我看到的最大障碍在于：目前 I2P 的大部分开发协作是在 I2P 内部进行的，这显著增加了参与贡献所需的工作量。

在该领域的两个优先事项是：

- Set up a project-run development forum that is accessible both inside and outside I2P.

- Set up mailing lists for review and discussion of proposals (possibly connected to the above forum).

被归类为可有可无的其他目标：

- Set up a usable git-to-mtn pathway, to enable us to effectively solicit clearnet contributions on GitHub while keeping the canonical dev environment on Monotone.

- Write a "position paper" that accurately explains I2P to academic audiences, and puts it in context with existing literature.

我预计与 I2P 之外人员的协作将完全在 GitHub 上进行，以将摩擦降到最低。

## 优先级：为长生命周期版本做准备

I2P 现已进入 Debian Sid（其不稳定仓库），预计在大约一年半后趋于稳定；同时也已被纳入 Ubuntu 仓库，计划收录进四月发布的下一个 LTS 版本。我们将开始面对会在多年内长期存在的 I2P 版本，并且需要确保我们能够应对它们在网络中的存在。

我们的首要目标是在明年内尽可能多地部署新的协议，以赶上下一次 Debian 稳定版发布。对于那些需要多年部署的协议，我们应尽可能早地纳入前向兼容性更改。

## 优先事项：现有应用的插件化

Debian 的模型鼓励为不同组件提供单独的软件包。我们一致认为，将目前捆绑的 Java 应用程序与核心 Java router 解耦，将在多个方面带来好处：

- It codifies the boundary between the applications and the router.

- It should make it easier to get these apps running with non-Java routers.

- It would enable third parties to create "I2P bundles" containing just the applications they want.

结合此前的优先事项，这将使 I2P 主项目更趋向于类似 Linux 内核的定位。我们将把更多时间放在网络本身上，让第三方开发者专注于使用该网络的应用（在过去几年我们对 API 和库所做的工作之后，这样做要容易得多）。

## 可选项：应用改进

我们希望进行一系列应用层面的改进，但鉴于我们还有其他优先事项，目前没有足够的开发时间来实现这些改进。这是一个我们非常希望有新贡献者参与的领域！一旦上述解耦完成，开发者独立于主 Java router 开发特定应用将会显著更容易。

我们非常希望获得帮助的其中一个应用是 I2P Android。我们将让它与 I2P 核心发布保持同步更新，并尽我们所能修复缺陷，但在改进底层代码和可用性方面仍有很多工作可做。

## 优先事项：提升 Susimail 和 I2P-Bote 的稳定性

话虽如此，我们确实希望在近期专门推进 Susimail 和 I2P-Bote 的修复工作（其中一些已在 0.9.33 中发布）。过去几年，它们相比其他 I2P 应用获得的投入较少，因此我们想花些时间让它们的代码库达到同等水平，并让新贡献者更容易上手！

## 可选项：工单分诊

我们在多个 I2P 子系统和应用中有大量积压的工单。作为上述稳定化工作的一部分，我们希望清理一些较早且长期存在的问题。更重要的是，我们希望确保工单得到妥善归类，以便新贡献者能找到适合着手处理的工单。

## 优先级：用户支持

我们将重点关注的一个方面，是与那些花时间报告问题的用户保持联系。谢谢！我们把反馈循环做得越短，就能越快解决新用户面临的问题，也就越有可能让他们继续参与社区。

## 我们非常欢迎您的帮助！

这些看起来都很雄心勃勃，确实如此！但上述许多事项彼此重叠，只要精心规划，我们就能在这些方面取得实质性进展。

如果你有兴趣帮助实现上述任何目标，欢迎来和我们聊天！你可以在 OFTC 和 Freenode（#i2p-dev），以及 Twitter（@GetI2P）找到我们。
