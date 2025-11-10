---
title: "I2P 2005-02-01 状态说明"
date: 2005-02-01
author: "jr"
description: "每周 I2P 开发状态简报，涵盖 0.5 版 tunnel 加密进展、新 NNTP 服务器，以及技术提案"
categories: ["status"]
---

大家好，到了每周状态更新时间

* Index

1) 0.5 状态 2) nntp（网络新闻传输协议） 3) 技术提案 4) ???

* 1) 0.5 status

在 0.5 版本方面已经取得了很多进展，昨天有一大批提交。router 的大部分现在使用了新的 tunnel 加密和 tunnel pooling [1]，并且在测试网络上运行良好。仍有一些关键部分尚待集成，而且代码显然不向后兼容，但我希望我们能在下周的某个时候进行更大范围的部署。

如前所述，初始的 0.5 版本将提供基础，使不同的 tunnel 对等节点选择与排序策略可以在其上运行。我们将从为探索性池和客户端池提供的一组基本可配置参数开始，但后续版本可能会为不同的用户类型加入其他选项。

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/tunnel-alt.html?rev=HEAD

* 2) nntp

正如在 LazyGuy 的站点 [2] 和我的博客 [3] 中提到的，我们已经在网络上部署并运行了一台新的 NNTP 服务器，可通过 nntp.fr.i2p 访问。虽然 LazyGuy 已经启动了一些使用 suck [4]（一种用于从 NNTP 拉取新闻的工具）的脚本来从 gmane 读取几个列表，但内容基本上都是出自 I2P 用户、服务于 I2P 用户、并面向 I2P 用户的。jdot、LazyGuy 和我研究了哪些新闻阅读器可以安全使用，看来有一些相当简单的解决方案。关于如何运行 slrn [5] 来进行匿名阅读和发帖，请参见我的博客。

[2] http://fr.i2p/ [3] http://jrandom.dev.i2p/ [4] http://freshmeat.net/projects/suck/ [5] http://freshmeat.net/projects/slrn/

* 3) tech proposals

Orion 和其他人在 ugha 的 wiki [6] 上发布了一系列针对各种技术问题的 RFC，以帮助更充分地探讨那些更棘手的客户端和应用级问题。请把那里作为讨论命名问题、SAM 的更新、swarming（群下载/群集传输）想法等内容的地方 - 当你在那里发帖时，我们就都可以在各自的地方协作，从而取得更好的结果。

[6] http://ugha.i2p/I2pRfc

* 4) ???

我暂时就说这些（正好，会议马上就要开始了）。  像往常一样，随时随地把你的想法发出来 :)

=jr
