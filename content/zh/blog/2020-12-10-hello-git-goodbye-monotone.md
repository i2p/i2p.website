---
title: "你好，Git，再见，Monotone"
date: 2020-12-10
author: "idk"
description: "你好，git，再见，mtn"
categories: ["Status"]
---

## 你好，Git，再见，Monotone

### The I2P Git Migration is nearly concluded

十多年来，I2P 一直依赖久经考验的 Monotone 服务来满足其版本控制需求，但在过去几年里，全球已普遍转向如今通用的 Git 版本控制系统。同一时期，I2P 网络变得更快、更可靠，而且针对 Git 不支持断点续传这一问题，也已经开发出易于使用的变通方案。

今天对 I2P 而言是一个重要的日子，我们关停了旧的 mtn i2p.i2p 分支，并且正式将核心 Java I2P 库的开发从 Monotone 迁移到 Git。

尽管我们过去使用 mtn 的做法曾遭质疑，而且它也并非一直是个受欢迎的选择，但我想借此机会，作为或许最后一个仍在使用 Monotone 的项目，向 Monotone 的开发者——无论现任还是前任、无论身在何处——致以感谢，感谢他们所创造的软件。

## GPG Signing

向 I2P 项目的代码仓库进行提交需要你为 git 提交配置 GPG 签名，这也包括 Merge Requests 和 Pull Requests。在 fork i2p.i2p 并提交任何内容之前，请先为你的 git 客户端配置 GPG 签名。

## GPG 签名

官方仓库托管在 https://i2pgit.org/i2p-hackers/i2p.i2p 和 https://git.idk.i2p/i2p-hackers/i2p.i2p，但在 Github 上也有一个“镜像”，位于 https://github.com/i2p/i2p.i2p。

既然我们现在使用 git，我们就可以将仓库从我们自托管的 Gitlab 实例同步到 Github，并且也可以反向同步。这意味着可以在 Gitlab 上创建并提交一个 merge request（合并请求），当它被合并时，结果会与 Github 同步；而在 Github 上的 Pull Request（拉取请求）在被合并后，也会出现在 Gitlab 上。

这意味着你可以根据自己的偏好，通过我们的 Gitlab 实例或通过 Github 向我们提交代码。不过，相比 Github，有更多 I2P 开发者会定期关注 Gitlab。提交到 Gitlab 的 MR（合并请求）通常比提交到 Github 的 PR（拉取请求）更有可能更快被合并。

## 官方仓库与 Gitlab/Github 同步

向所有在 git 迁移中提供帮助的人表示祝贺和感谢，特别是 zzz、eche|on、nextloop，以及我们的镜像站点维护者！虽然我们中的一些人会怀念 Monotone，但它已经成为 I2P 开发中新老参与者的障碍，我们很高兴加入使用 Git 管理分布式项目的开发者社区。
