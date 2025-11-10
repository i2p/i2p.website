---
title: "I2P 2005-02-22 状态说明"
date: 2005-02-22
author: "jr"
description: "每周 I2P 开发状态笔记，涵盖 0.5 版本发布成功、即将发布的 0.5.0.1 缺陷修复版、tunnel 对等节点排序策略，以及 azneti2p 更新"
categories: ["status"]
---

大家好，每周更新时间到了

* Index

1) 0.5 2) 后续步骤 3) azneti2p 4) ???

* 1) 0.5

正如大家所知，我们终于发布了 0.5，总体来说表现相当不错。我非常感谢大家更新得如此迅速——在第一天内，网络中已有 50-75% 升级到 0.5！由于采用速度很快，我们能够更快地看到各项变更的影响，进而也发现了一些 bug。虽然仍然存在一些遗留问题，我们会在今晚稍晚时候发布新的 0.5.0.1 版本，以解决其中最重要的问题。

作为这些 bug 的附带好处，看到 routers 可以处理数千个 tunnels，挺有意思的 ;)

* 2) Next steps

After the 0.5.0.1 release, there may be another build to experiment with some changes in the exploratory tunnel building (such as using only one or two not-failing peers, the rest being high capacity, instead of all of the peers being not-failing).  After that, we'll be jumping towards 0.5.1, which will improve the tunnel throughput (by batching multiple small messages into a single tunnel message) and allow the user more control over their suceptability to the predecessor attack.

这些控制将采取按客户端的对等节点排序和选择策略的形式，一个用于 inbound gateway（入站网关）和 outbound endpoint（出站端点），另一个用于其余的 tunnel。  我预见的策略粗略概述如下：  = random（我们现在已有的）  = balanced（明确尝试降低我们使用每个对等节点的频率）  = strict（如果我们曾经使用 A-->B-->C，它们保持该顺序            在随后的 tunnel 中 [受时间限制]）  = loose（为客户端生成一个随机密钥，计算该密钥与每个对等节点的 XOR（异或）           ，并始终按照与该密钥的距离对所选对等节点进行排序           [受时间限制]）  = fixed（始终按 MBTF 使用相同的对等节点）

总之，计划就是这样，不过我还不确定会先推出哪些策略。非常欢迎提出建议 :)

* 3) azneti2p

azureus 那边的团队一直在努力推出一连串的更新，他们最新的 b34 快照 [1] 似乎包含了一些与 I2P 相关的 bug 修复。虽然自从我上次提出那个匿名性问题以来还没来得及审计源码，但他们已经修复了那个特定的 bug，所以如果你想尝鲜，就去下载他们的更新试试吧！

[1] http://azureus.sourceforge.net/index_CVS.php

* 4) ???

最近事情多得很，我肯定还远没讲全。再过几分钟来参加会议看看最新情况吧！

=jr
