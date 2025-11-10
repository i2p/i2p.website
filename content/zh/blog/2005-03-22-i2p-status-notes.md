---
title: "I2P 2005-03-22 状态说明"
date: 2005-03-22
author: "jr"
description: "每周 I2P 开发状态说明，涵盖 0.5.0.3 版本发布、tunnel（隧道）消息批处理的实现，以及自动更新工具"
categories: ["status"]
---

大家好，简单说一下最新进展

* Index

1) 0.5.0.3 2) 批处理 3) 更新 4) ???

* 0.5.0.3

新版本已经发布并广泛推送，大多数人都很快完成了升级——谢谢！我们修复了一些 bug，但没有什么颠覆性的变化——最大的一项是把 0.5 和 0.5.0.1 的用户从网络上移除。自那以后我一直在跟踪网络的行为，深入分析发生了什么，虽然确实有所改进，但仍然有一些事情需要解决。

在接下来一两天内将发布一个新版本，其中包含一个针对尚无人遇到、但会破坏新批处理代码的问题的修复。此外，还会提供一些工具，用于根据用户的偏好自动化更新流程，以及其他一些小改动。

* batching

正如我在博客中提到的，通过对 tunnel 消息进行一些非常简单的批量打包，有很大空间可以大幅降低网络所需的带宽和消息数量——与其不论大小都把每个 I2NP 消息单独放进一个 tunnel 消息中，不如通过加入一个短暂的延迟，在单个 tunnel 消息中打包多达 15 个或更多。收益最大的将是使用小消息的服务（例如 IRC），而大型文件传输受影响则不大。用于执行批量打包的代码已经实现并经过测试，但不幸的是，正式网络上存在一个 bug，会导致同一 tunnel 消息中除了第一个 I2NP 消息以外的所有消息被丢失。这就是我们将先发布一个包含该修复的过渡版本，随后在大约一周后发布启用批量打包版本的原因。

* updating

在这个过渡版本中，我们将发布一些经常讨论的 'autoupdate（自动更新）' 代码。我们已经提供了工具，可以定期检查可信的更新公告，以匿名或非匿名方式下载更新，然后要么直接安装，要么仅在 router 控制台上显示一条通知，告诉你它已准备就绪，等待安装。更新本身现在将采用 smeghead 的新签名更新格式，本质上就是更新包加上一个 DSA 签名。用于验证该签名的密钥将与 I2P 一并提供，并且可以在 router 控制台中进行配置。

The default behavior will be to simply periodically check for update announcements but not to act on them - just to display a one-click "Update now" feature on the router console.  There will be lots of other scenarios for different user needs, but they'll hopefully all be accounted for through a new configuration page.

* ???

我感觉有点不舒服，所以上面并没有把具体情况讲得很详细。欢迎来参加会议，把遗漏的部分补上 :)

哦，顺便说一句，我也会在接下来一两天内为自己发布一把新的 PGP 密钥（因为这把很快就会过期……），所以请留意。

=jr
