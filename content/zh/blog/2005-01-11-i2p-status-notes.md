---
title: "I2P 2005-01-11 状态说明"
date: 2005-01-11
author: "jr"
description: "每周 I2P 开发状态说明，涵盖网络状态、0.5 进展、0.6 状态、azneti2p、FreeBSD 移植，以及将 hosts.txt 作为信任网络"
categories: ["status"]
---

嗨，大家好，到了每周更新的时间了

* Index

1) 网络状态 2) 0.5 进度 3) 0.6 状态 4) azneti2p 5) fbsd 6) hosts.txt 作为 WoT（信任网络） 7) ???

* 1) Net status

总体而言，网络运行良好，不过我们遇到了一些问题：其中一台 irc 服务器离线了，而我的 outproxy(出口代理)也出现了异常。不过，另一台 irc 服务器仍然在线(而且现在仍是如此)(不过目前尚未禁用 CTCP - 参见 [1])，所以我们还是能够满足我们对 irc 的需求 :)

[1] http://ugha.i2p/HowTo/IrcAnonymityGuide

* 2) 0.5 progress

有进展了，不断前进！好吧，我想我应该比这说得更详细一点。我终于把新的 tunnel 路由加密实现并测试完了（耶！），但在一些讨论中我们发现有一个可能导致匿名性泄露的地方，所以正在修订（第一跳会知道自己是第一跳，这很糟糕。不过修起来真的真的很容易）。总之，我希望很快就能更新并发布相关的文档和代码，而关于 0.5 版 tunnel 的运行 / 池化 / 等的文档会稍后发布。有新消息时会再更新。

* 3) 0.6 status

(什么!?)

Mule 已经开始研究 UDP 传输，我们也一直向 zab 请教他在 LimeWire 的 UDP 代码方面的经验。一切看起来很有前景，但还有很多工作要做（而且在路线图 [2] 上仍需数月）。有灵感或建议吗？参与进来，帮助我们把工作聚焦到需要完成的事项上！

[2] http://www.i2p.net/roadmap#0.6

* 4) azneti2p

当我拿到这个消息时，我兴奋得差点尿裤子，不过看起来 Azureus 的伙计们已经写出了一个 I2P 插件，既能匿名使用 tracker（跟踪器），也能进行匿名数据通信！多个种子也可以在同一个 I2P destination（I2P 目标地址）内工作，而且它直接使用 I2PSocket，从而与 streaming lib（流式传输库）紧密集成。azneti2p 插件目前还处在早期阶段，这次发布的是 0.1 版本，后续还有大量优化和易用性改进在路上，不过如果你愿意亲自动手，不妨去 I2P IRC 网络上的 i2p-bt 逛逛，加入这场乐趣 :)

对于喜欢冒险的用户，请获取最新版的 azureus [3]，查看他们的 i2p 使用指南 [4]，并获取该插件 [5]。

[3] http://azureus.sourceforge.net/index_CVS.php [4] http://azureus.sourceforge.net/doc/AnonBT/i2p/I2P_howto.htm [5] http://azureus.sourceforge.net/plugin_details.php?plugin=azneti2p

为了保持与 i2p-bt 的兼容性，duck 一直付出了近乎英雄般的努力；而就在我敲下这些文字的时候，#i2p-bt 里正进行着疯狂的开发，所以请留意很快就会发布的 i2p-bt 新版本。

* 5) fbsd

多亏了 lioux 的努力，i2p 现在在 FreeBSD Ports 中已有一个条目[6]。虽然我们并不打算推出大量面向不同发行版的特定安装方案，但只要我们为新版本发布提供足够的提前通知，他承诺会及时保持更新。对于 fbsd-current 的朋友们（指 FreeBSD-CURRENT 分支的用户）来说，这应该会很有帮助——感谢 lioux！

[6] http://www.freshports.org/net/i2p/

* 6) hosts.txt as WoT

随着 0.4.2.6 版本将 Ragnarok 的地址簿打包内置，保持你的 hosts.txt 持续添加新条目的过程完全由每位用户自行掌控。不仅如此，你还可以将地址簿订阅视为一种“穷人版”的信任网——你从你信任的网站导入新条目，让它为你引荐新的目的地（默认为 dev.i2p 和 duck.i2p）。

随着这种能力的到来，也带来了一个全新的维度——人们可以选择在自己的 hosts.txt 中收录哪些站点，以及不收录哪些。尽管过去那种对公众完全开放、放任自由的做法自有其用武之地，但如今命名系统不仅在理论上，而且在实践中都已实现完全分布式，人们将需要为发布他人的目的地制定各自的策略。

这里幕后重要的一点是：这是 I2P 社区的一个学习机会。此前，gott 和我都试图通过把 gott 的站点发布为 jrandom.i2p 来推动命名问题（该站点是他先提出申请的——我没有提出申请，而且我对该 URL 的内容没有任何控制权）。现在我们可以开始探索如何处理那些没有列在 http://dev.i2p.net/i2p/hosts.txt 或 forum.i2p 上的站点。未在这些位置发布并不会以任何方式阻止站点运行——你的 hosts.txt 只是你的本地地址簿。

Anyway, enough babbling, I just wanted to put people on notice so we can all see what is to be done.

* 7) ???

哇，事情可真多。这周很忙，而且我预计短期内也不会放缓。所以再过几分钟就来参加会议吧，我们可以聊聊这些事。

=jr
