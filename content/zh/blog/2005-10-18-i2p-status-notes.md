---
title: "I2P 2005-10-18 状态说明"
date: 2005-10-18
author: "jr"
description: "每周更新，涵盖 0.6.1.3 版本发布成功、与 Freenet 的协作讨论、tunnel 自举攻击分析、I2Phex 上传 bug 的进展，以及对称 NAT 悬赏"
categories: ["status"]
---

嗨，大家，又是星期二了

* Index

1) 0.6.1.3 2) Freenet、I2P 和暗网（天哪） 3) Tunnel 引导攻击 4) I2Phex 5) Syndie/Sucker 6) ??? [500+ 对称 NAT 悬赏]

* 1) 0.6.1.3

上周五我们发布了新的 0.6.1.3 版本，目前已有 70% 的网络完成升级，反馈非常积极。新的 SSU 改进似乎减少了不必要的重传，使得在更高速率下实现更高效的吞吐量；据我所知，IRC 代理或 Syndie 的改进也没有出现任何重大问题。

有一点值得注意的是，Eol 已在 rentacoder[1] 上设立了关于对称 NAT 支持的悬赏，因此希望我们在这方面能有所进展！

[1] http://rentacoder.com/RentACoder/misc/BidRequests/ShowBidRequest.asp?lngBidRequestId=349320

* 2) Freenet, I2P, and darknets (oh my)

我们终于把那条超过 100 条消息的讨论串告一段落，对这两个网络的定位、适用范围，以及我们在进一步协作上的空间都有了更清晰的认识。我在这里就不展开它们最适合哪些拓扑或威胁模型了，想了解更多可以去翻阅邮件列表。

在协作方面，我已经给 toad 发去了一些用于复用我们 SSU 传输的示例代码，这可能在短期内对 Freenet 的同事有所帮助。接下来，在 I2P 可行的环境中，我们或许会合作为 Freenet 用户提供预混合路由。

随着 Freenet 的推进，我们也可能让 Freenet 作为客户端应用运行在 I2P 之上，从而在运行它的用户之间实现自动化内容分发（例如传播 Syndie 归档和帖子）。不过我们会先看看 Freenet 规划中的负载与内容分发系统会如何运作。

* 3) Tunnel bootstrap attacks

Michael Rogers 就针对 I2P 的 tunnel 创建的一些有趣的新型攻击取得了联系 [2][3][4]。主要的攻击（在整个引导过程期间成功实施前任攻击）很有趣，但并不太实用 - 其成功概率为 (c/n)^t，其中 c 为攻击者数量，n 为网络中的对等节点数，t 为目标在其生命周期内构建的 tunnel 数 - 这比在该 router 已构建 h 条 tunnel 之后，攻击者接管一条 tunnel 的全部 h 跳的概率更低（P(success) = (c/n)^h）。

Michael 已在邮件列表上发布了关于另一项攻击的帖子，我们目前正在处理，因此你也可以在那里跟进。

[2] http://dev.i2p.net/pipermail/i2p/2005-October/001005.html [3] http://dev.i2p.net/pipermail/i2p/2005-October/001008.html [4] http://dev.i2p.net/pipermail/i2p/2005-October/001006.html

* 4) I2Phex

Striker 在修复上传 bug 上又取得了进展，据称他已经将问题定位。希望今晚就能提交到 CVS，随后不久将以 0.1.1.33 发布。更多信息请关注论坛 [5]。

[5] http://forum.i2p.net/viewforum.i2p?f=25

据说 redzara 在重新并入 Phex 主线方面也取得了相当不错的进展，所以在 Gregor 的帮助下，我们有望很快把一切更新到最新！

* 5) Syndie/Sucker

dust 也一直在和 Sucker 一起埋头开发，通过代码让 Syndie 能导入更多的 RSS/Atom 数据。也许我们可以把 Sucker 和 post CLI（命令行界面）进一步集成到 Syndie 中，甚至提供一个基于 Web 的控制界面，用来调度将不同的 RSS/Atom 订阅源导入到各个博客。拭目以待...

* 6) ???

除此之外还有不少进展，不过以上就是我所知的要点。若有人有任何问题或顾虑，或者想提出其他事项，今晚 UTC 时间 8 点欢迎来 #i2p 的会议聊聊！

=jr
