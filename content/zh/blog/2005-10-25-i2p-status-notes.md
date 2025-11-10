---
title: "I2P 2005-10-25 状态说明"
date: 2005-10-25
author: "jr"
description: "每周更新，内容包括：网络增长至 400-500 个对等节点、集成 Fortuna PRNG（伪随机数发生器）、支持 GCJ 的原生编译、i2psnark 轻量级 torrent 客户端，以及针对 tunnel 引导攻击的分析"
categories: ["status"]
---

大家好，前线又有新消息

* Index

1) 网络状态 2) Fortuna 集成 3) GCJ 状态 4) i2psnark 回归 5) 更多关于 bootstrapping（引导过程） 6) 病毒调查 7) ???

* 1) Net status

过去一周网络状况相当不错——整体看起来相当稳定、吞吐量正常，而且网络规模持续增长，已经进入 400-500 个对等节点的范围。自 0.6.1.3 版本发布以来也有一些显著改进，鉴于这些改进会影响性能和可靠性，我预计我们将在本周晚些时候发布 0.6.1.4 版本。

* 2) Fortuna integration

多亏了 Casey Marshall 的快速修复 [1]，我们已经能够集成 GNU-Crypto 的 Fortuna [2] 伪随机数生成器。这消除了在使用 blackdown JVM 时导致诸多挫折的根源，并让我们能够与 GCJ 顺畅配合工作。将 Fortuna 集成进 I2P 是 smeghead 开发 “pants”（一个基于 'ant' 的 'portage'）的主要原因之一，因此我们现在又一次成功地使用了 pants :)

[1] http://lists.gnu.org/archive/html/gnu-crypto-discuss/2005-10/msg00007.html [2] http://en.wikipedia.org/wiki/Fortuna

* 3) GCJ status

正如在邮件列表 [3] 中所述，我们现在可以使用 GCJ [4] 无缝运行 router（I2P 路由器）和大多数客户端。Web 控制台本身目前尚未完全可用，因此你需要通过 router.config 自行进行 router 配置（不过它应该可以开箱即用，并会在大约一分钟后启动你的 tunnels（隧道））。我还不完全确定 GCJ 将如何纳入我们的发布计划，不过我目前倾向于发布纯 Java，同时支持 Java 与原生编译版本。为了适配不同的操作系统和库版本而构建并分发大量不同的构建，这确实有点麻烦。大家对此有什么强烈的看法吗？

对 GCJ 的支持的另一个优点是可以从 C/C++/Python 等语言使用 streaming lib（流式库）。我不清楚是否有人在做这类集成，但这应该很值得做，所以如果你有兴趣在这方面开展开发，请告诉我！

[3] http://dev.i2p.net/pipermail/i2p/2005-October/001021.html [4] http://gcc.gnu.org/java/

* 4) i2psnark returns

虽然 i2p-bt 是移植到 I2P 并被广泛使用的第一个 BitTorrent 客户端，但很久之前 eco 就抢先一步完成了对 snark [5] 的移植。不幸的是，它没有持续跟进更新，也未能与其他匿名 BitTorrent 客户端保持兼容性，所以有一段时间基本销声匿迹。上周，我在 i2p-bt<->sam<->streaming lib（流式传输库）<->i2cp 链路的某处处理性能问题时遇到了一些麻烦，于是转向 mjw 的原始 snark 代码做了一个简单的移植 [6]，把所有 java.net.*Socket 调用替换为 I2PSocket* 调用，将 InetAddresses 替换为 Destinations（目标地址），并把 URLs 替换为 EepGet 调用。最终得到的是一个小巧的命令行 BitTorrent 客户端（编译后约 60KB），我们现在会随 I2P 发行版一同提供。

Ragnarok 已经开始动手改进其块选择算法，我们也希望能在 0.6.2 发布之前为它加入 Web 界面和 multitorrent（多种子）功能。如果你有兴趣帮忙，请与我们联系！ :)

[5] http://klomp.org/snark/ [6] http://dev.i2p.net/~jrandom/snark_diff.txt

* 5) More on bootstrapping

The mailing list has been pretty active lately, with Michael's new simulations and analysis of the tunnel construction. The discussion is still going on, with some good ideas from Toad, Tom, and polecat, so check it out if you want to get some input into the tradeoffs for some anonymity related design issues we'll be revamping for the 0.6.2 release [7].

对于那些对一些好看的可视化感兴趣的人，Michael 也能满足你，提供了一个模拟，用于展示攻击识别你的可能性——它随他们控制的网络百分比而变化[8]，也随你的 tunnel 活跃程度而变化[9]。

(干得好，Michael，谢谢！)

[7] http://dev.i2p.net/pipermail/i2p/2005-October/thread.html     (参见 "i2p tunnel bootstrap attack" 讨论串) [8] http://dev.i2p.net/~jrandom/fraction-of-attackers.png [9] http://dev.i2p.net/~jrandom/messages-per-tunnel.png

* 6) Virus investigations

最近有一些关于某个特定的支持 I2P 的应用程序随附传播潜在恶意软件问题的讨论，Complication 已经做了出色的深入调查。相关数据已公开，你可以自行判断。 [10]

感谢 Complication 对此所做的所有研究！

[10] http://forum.i2p.net/viewtopic.php?t=1122

* 7) ???

如你所见，事情真是多得很，不过我开会已经迟到了，还是把这个先保存然后发出去吧，对吧？在 #i2p 见 :)

=jr
