---
title: "I2P 2005-01-18 状态说明"
date: 2005-01-18
author: "jr"
description: "每周 I2P 开发状态简报，涵盖网络状态、0.5 版 tunnel 路由设计、i2pmail.v2，以及 azneti2p_0.2 的安全修复"
categories: ["status"]
---

嗨，大家好，每周更新时间到了

* Index

1) 网络状态 2) 0.5 3) i2pmail.v2 4) azneti2p_0.2 5) ???

* 1) Net status

嗯，这里没什么可报告的 - 一切仍然像上周那样运作，网络规模也差不多，可能稍微大了一点。  一些很不错的新站点正在涌现 - 详情请参见论坛 [1] 和 orion [2]。

[1] http://forum.i2p.net/viewforum.php?f=16 [2] http://orion.i2p/

* 2) 0.5

感谢 postman、dox、frosk 和 cervantes 的帮助（以及所有通过他们的 router 进行 tunnel 传输数据的人 ;)，我们收集到了一整天的消息大小统计数据 [3]。那里有两组统计 - 缩放的高度和宽度。这样做的动机是希望探索不同消息填充策略对网络负载的影响，正如针对 0.5 版 tunnel 路由的某个草案 [4] 中所解释的那样。(ooOOoo 漂亮的图片)。

让我在翻查那些东西时感到发怵的是：即便使用一些相当简单、手工调优的填充阈值，把数据填充到那些固定大小，最终仍然会浪费超过25%的带宽。是啊，我知道，我们不会那么做。也许你们可以通过深入挖掘那些原始数据，想出更好的办法。

[3] http://dev.i2p.net/~jrandom/messageSizes/ [4] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/                                  tunnel.html?rev=HEAD#tunnel.padding

其实，那个[4]链接把我们带到了关于 tunnel 路由的 0.5 计划的现状。正如 Connelly 在[5]中所发帖所述，最近在 IRC 上围绕一些草案进行了大量讨论，polecat、bla、duck、nickster、detonate 等人都贡献了建议和探究性的问题（好吧，还有些讥讽 ;)）。一周多以后，我们发现了与[4]有关的一个潜在漏洞，情形是某个对手设法接管了入站 tunnel 网关，同时还控制了该 tunnel 后续路径中的另一个节点。虽然在大多数情况下，这本身并不会暴露端点，且随着网络增长，从概率上讲要实现这一点会越来越难，但这仍然糟糕透顶 (tm)。

于是引入了[6]。这解决了那个问题，使我们可以拥有任意长度的 tunnels（隧道），甚至还能解决世界饥饿问题[7]。不过，这也引出了另一个问题：攻击者可能在 tunnel 中构造环路，但基于 Taral 去年关于用于 ElGamal/AES 的会话标签的一个建议[8]，我们可以通过使用一系列同步的伪随机数发生器[9]，将造成的损害降到最低。

[5] http://dev.i2p.net/pipermail/i2p/2005-January/000557.html [6] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/                                             tunnel-alt.html?rev=HEAD [7] 猜猜哪条陈述是假的? [8] http://www.i2p.net/todo#sessionTag [9] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/                                 tunnel-alt.html?rev=HEAD#tunnel.prng

如果上面的内容听起来让人困惑，别担心——你看到的是一些棘手的设计问题的内部细节，正被摊到台面上抽丝剥茧。 如果上面*并不*让你感到困惑，请与我们联系，因为我们一直在寻找更多的头脑来一起深入讨论这些问题 :)

总之，正如我在邮件列表[10]中提到的，接下来我想把第二个策略[6]实现出来，以便把剩余的细节敲定。  目前对 0.5 的计划是把所有向后不兼容的变更整合在一起 - 新的 tunnel 加密等 - 并作为 0.5.0 发布，然后待其在网络上稳定下来，再推进 0.5 的其他部分[11]，例如按提案所述调整池化策略，并将其作为 0.5.1 发布。  我希望我们仍能在本月底发布 0.5.0，但到时候再看。

[10] http://dev.i2p.net/pipermail/i2p/2005-January/000558.html [11] http://www.i2p.net/roadmap#0.5

* 3) i2pmail.v2

前几天，postman 发布了一个关于下一代邮件基础设施的行动计划草案 [12]，看起来酷爆了。当然，我们总还能想出更多锦上添花的花哨功能，但从很多方面看，它的架构相当不错。去看看目前已经整理成文档的内容 [13]，并把你的想法告诉 postman！

[12] http://forum.i2p.net/viewtopic.php?t=259 [13] http://www.postman.i2p/mailv2.html

* 4) azneti2p_0.2

正如我在邮件列表 [14] 中所发帖所述，原始的 azneti2p 插件（用于 azureus）存在一个严重的匿名性漏洞。问题在于，在混合的种子（部分用户匿名、部分用户非匿名）的情况下，匿名用户会/直接/联系非匿名用户，而不是通过 I2P。Paul Gardner 和其他 azureus 开发者反应非常迅速，并立即发布了补丁。我所发现的问题在 azureus v. 2203-b12 + azneti2p_0.2 中已不存在。

我们还没有通读并审计代码来评估任何潜在的匿名性问题，所以“use at your own risk”（另一方面，在 1.0 发布之前，我们对 I2P 也说过同样的话）。如果你愿意参与，我知道 Azureus 的开发者会很感激就该插件提供更多的反馈和 bug 报告。我们当然会在发现任何其他问题时及时告知大家。

[14] http://dev.i2p.net/pipermail/i2p/2005-January/000553.html

* 5) ???

正如你所见，事情很多。我想我该提的差不多都说完了，但如果你还有其他想讨论的内容，请在40分钟后来参加一下会议（或者你只是想对上面那些事情吐槽一下也行）

=jr
