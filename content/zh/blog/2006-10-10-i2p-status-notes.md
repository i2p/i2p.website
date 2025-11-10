---
title: "I2P 状态说明（2006年10月10日）"
date: 2006-10-10
author: "jr"
description: "0.6.1.26 版本发布并获得正面反馈、Syndie 0.910a 接近 1.0，以及对 Syndie 的分布式版本控制进行评估"
categories: ["status"]
---

Hi y'all, brief status notes this week

* Index

1) 0.6.1.26 与网络状态 2) Syndie 开发状态 3) 分布式版本控制再探 4) ???

* 1) 0.6.1.26 and network status

前几天我们推出了 0.6.1.26 的新版本，其中包含来自 zzz 的大量 i2psnark 改进，以及来自 Complication 的一些新的 NTP 安全检查，整体反馈十分积极。网络似乎略有增长，且没有出现新的异常现象，不过仍有一些人在构建他们的 tunnels 时遇到困难（一如既往）。

* 2) Syndie development status

我们不断推出更多改进，目前的 alpha 版本为 0.910a。1.0 的功能清单基本已经满足，所以现在主要是修复 bug 和完善文档。如果你想帮忙测试，欢迎来 #i2p 逛逛 :)

另外，在频道里也有一些关于 Syndie GUI（图形界面）设计的讨论——meerboop 提出了一些很酷的点子，并且正在把这些想法写成文档。Syndie GUI 是 Syndie 2.0 发布的主要组件，所以我们越早让它运转起来，我们就越早征服世界^W^W^W^W能把 Syndie 推向那些毫无防备的大众。

我在 Syndie 博客中还发布了一份关于使用 Syndie 本身进行缺陷和功能请求跟踪的新提案。为便于访问，我已将该帖子导出为纯文本并发布到网页上 - 第 1 页位于 <http://dev.i2p.net/~jrandom/bugsp1.txt>，第 2 页位于 <http://dev.i2p.net/~jrandom/bugsp2.txt>

* 3) Distributed version control revisited

关于 Syndie 仍需确定的一件事是要使用哪种公开的版本控制系统，且如前所述，必须具备分布式与离线功能。我一直在研究市面上半打左右的开源方案（darcs、mercurial、git/cogito、monotone、arch、bzr、codeville），翻阅它们的文档、进行试用，并与其开发者交流。眼下，就功能和安全性而言，monotone 和 bzr 似乎是最好的（在仓库不受信任的情况下，我们需要通过强密码学手段确保只拉取到可验证的变更），而 monotone 与密码学的紧密集成尤其令人心动。不过，我还在通读数百页的文档，但根据我与 monotone 开发者的交流，他们似乎各方面都做得很对。

当然，无论我们最终选择哪种 DVCS（分布式版本控制系统），所有发布都会以纯 tar 包格式提供，而补丁将以纯 diff -uw 格式接受审核。不过，对于那些可能考虑参与开发的人，我很想听听你们的想法和偏好。

* 4) ???

如你所见，一如既往地有很多事情在发生。论坛上那个“解决世界饥饿”的主题帖也有了进一步的讨论，欢迎前往 <http://forum.i2p.net/viewtopic.php?t=1910> 查看。

如果你还有进一步想讨论的内容，欢迎今晚到 #i2p 参加我们的开发者会议，或者在论坛发帖或向邮件列表发信！

=jr
