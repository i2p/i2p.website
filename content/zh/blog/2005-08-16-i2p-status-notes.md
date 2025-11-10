---
title: "I2P 2005-08-16 状态说明"
date: 2005-08-16
author: "jr"
description: "简要更新，涵盖 PeerTest 状态、Irc2P 网络过渡、Feedspace GUI 进展，以及会议时间调整为 GMT 晚上 8 点"
categories: ["status"]
---

大家好，今天只有一些简短的说明。

* Index:

1) PeerTest 状态 2) Irc2P 3) Feedspace 4) 元话题 5) ???

* 1) PeerTest status

如前所述，即将发布的 0.6.1 版本将包含一系列测试，以更精细地配置 router 并验证可达性（或指出需要完成的工作），虽然我们已经在 CVS 中放入了一些代码并经过了两次构建，但在其能够如期顺畅运行之前，仍然需要做一些改进。当前，我正在对 [1] 中记录的测试流程做一些小的修改：增加一个用于验证 Charlie 可达性的额外数据包，并将 Bob 对 Alice 的回复延迟到 Charlie 已经响应之后。这样应当减少用户看到的不必要的 "ERR-Reject" 状态值的数量，因为在有一个可参与测试的 Charlie 之前，Bob 不会回复 Alice（而当 Bob 没有回复时，Alice 会看到状态为 "Unknown"）。

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/udp.html#peerTesting

总之，嗯，就这样——明天应该会发布 0.6.0.2-3，等彻底测试完成后会作为正式版本发布。

* 2) Irc2P

正如在论坛 [2] 中提到的，使用 IRC 的 I2P 用户需要更新配置，以切换到新的 IRC 网络。Duck 将暂时下线，为了 [redacted]，与其在此期间指望服务器不出问题，postman 和 smeghead 已经挺身而出，为大家搭建了一个新的 IRC 网络供使用。Postman 还在 [3] 镜像了 duck 的 tracker（跟踪器）和 i2p-bt 站点，而且我想我在新的 IRC 网络上看到有人提到 susi 正在启动一个新的 IdleRPG 实例（更多信息请查看频道列表）。

我要感谢那些负责旧的 i2pirc network 的人（duck、baffled、metropipe 团队、postman），以及负责新的 irc2p network 的人（postman、arcturus）！有趣的服务和内容让 I2P 变得值得使用，而把它们做出来就要靠大家了！

[2] http://forum.i2p.net/viewtopic.php?t=898 [3] http://hq.postman.i2p/

* 3) Feedspace

说到这个，前几天我翻看了 frosk 的博客，看来 Feedspace 又有了一些进展——尤其是一个不错的小巧的 GUI（图形界面）。我知道它可能还没到可以测试的阶段，不过我相信到时候 frosk 会把一些代码发给我们。顺带一提，我还听说有个传闻：另一个注重匿名性的基于 Web 的博客工具正在筹备中，等准备好后能够与 Feedspace 对接。不过同样，等它准备就绪时，我们肯定会听到更多消息。

* 4) meta

作为一个贪婪的混蛋，我想把会议时间提前一点 - 不再是 9PM GMT，试试 8PM GMT。为什么？因为这更符合我的日程安排 ;)（离我最近的网吧不营业到很晚）。

* 5) ???

目前就这样吧——为了今晚的会议，我会尽量待在一家网吧，所以欢迎在 GMT 时间 *8*P 在 /new/ irc 服务器 {irc.postman.i2p, irc.arcturus.i2p} 上加入 #i2p。我们可能会架设一个连接到 irc.freenode.net 的 changate 机器人——有人愿意运行一个吗？

嗨，=jr
