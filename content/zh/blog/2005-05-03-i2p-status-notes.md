---
title: "2005-05-03 的 I2P 状态说明"
date: 2005-05-03
author: "jr"
description: "每周更新：涵盖网络稳定性、SSU UDP 传输实网测试成功、i2phex 文件共享进展，以及即将到来的 3–4 周缺席"
categories: ["status"]
---

嗨，大家，本周议程上有很多事项。

* Index

1) 网络状态 2) SSU 状态 3) i2phex 4) 失联 5) ???

* 1) Net status

整体网络健康状况没有大的变化——看起来相当稳定，尽管偶尔有些小波动，各项服务运行状况良好。自上次发布以来，CVS 有不少更新，但没有涉及阻断性（致命）缺陷的修复。在我搬家之前我们可能还会再发一个版本，只是为了让最新的 CVS 能更广泛地发布出去，不过我还不确定。

* 2) SSU status

听我老说 UDP 传输有很多进展，你是不是已经听腻了？那么，很遗憾——UDP 传输确实又取得了不少进展。周末期间，我们从私有网络测试环境迁移到正式网络，大约十来个 router 完成升级并公开了它们的 SSU 地址——这使得大多数用户可以通过 TCP 传输访问它们，同时让启用 SSU 的 router 能够通过 UDP 相互通信。

测试还处于非常早期阶段，但进展比我预期的要好得多。拥塞控制表现非常良好，吞吐量和延迟都相当令人满意 - 它能够正确识别实际带宽上限，并在与其他竞争的 TCP 流之间有效地共享该链路。

通过从热心志愿者那里收集到的统计数据，我们清楚地认识到，在高度拥塞的网络中要实现正确运行，选择性确认（Selective Acknowledgement，简称 SACK）代码至关重要。我在过去几天里实现并测试了这部分代码，并已更新 SSU 规范[1]，纳入了一种新的高效 SACK 技术。由于它与早期的 SSU 代码不向后兼容，参与测试的人员应暂时禁用 SSU 传输，直到新的构建版本准备好供测试（希望在一两天内）。

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/udp.html?rev=HEAD

* 3) i2phex

sirup 一直在努力将 phex 移植到 i2p，虽然在它准备好面向普通用户之前还有很多工作要做，但今晚早些时候我已经能把它启动起来，浏览 sirup 的共享文件，下载一些数据，并使用它那*咳* "instant" 聊天界面。

在 sirup 的 eepsite(I2P 站点) [2] 上有更多信息，已经在 i2p 社区的成员如果能协助测试就太好了（不过请在 sirup 批准其作为公开发布之前，且 i2p 至少达到 0.6、最好是 1.0 之前，先将其限定在 i2p 社区内部）。我相信 sirup 会参加本周的会议，届时也许我们能获得更多信息！

[2] http://sirup.i2p/

* 4) awol

Speaking of being around, I probably won't be here for next week's meeting and will be offline for the following 3-4 weeks. While that probably means there won't be any new releases, there are still a bunch of really interesting things for people to hack on:  = applications like feedspace, i2p-bt/ducktorrent, i2phex, fire2pe,     the addressbook, susimail, q, or something completely new.  = the eepproxy - it'd be great to get filtering, support for     persistent HTTP connections, 'listen on' ACLs, and perhaps an     exponential backoff to deal with outproxy timeouts (rather than     plain round robin)  = the PRNG (as discussed on the list)  = a PMTU library (either in Java or in C with JNI)  = the unit test bounty and the GCJ bounty  = router memory profiling and tuning  = and a whole lot more.

所以，如果你感到无聊并想帮忙，但又需要一些灵感，也许上面提到的某一项能让你开始行动。我可能会不时去一趟网吧，所以可以通过电子邮件联系到我，但回复时间会是 O(days)。

* 5) ???

好的，目前我想提的差不多就这些。对于想在接下来一周帮忙进行 SSU 测试的朋友，请留意我博客 [3] 上的信息。其他各位，会议上见！

=jr [3] http://jrandom.dev.i2p/
