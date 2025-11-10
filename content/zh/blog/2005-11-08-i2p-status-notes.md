---
title: "I2P 2005-11-08 状态说明"
date: 2005-11-08
author: "jr"
description: "每周更新，涵盖 0.6.1.4 的稳定性、性能优化路线图、I2Phex 0.1.1.35 发布、I2P-Rufus BT 客户端开发、I2PSnarkGUI 进展，以及 Syndie UI 改版"
categories: ["status"]
---

大家好，又到星期二了

* Index

1) 网络状态 / 短期路线图 2) I2Phex 3) I2P-Rufus 4) I2PSnarkGUI 5) Syndie 6) ???

* 1) Net status / short term roadmap

0.6.1.4 仍然相当稳定，不过自那以后在 CVS 中又有一些错误修复。我还为 SSU 添加了一些优化，以便更高效地传输数据，希望一旦广泛部署后，能对网络产生显著影响。不过我暂时会暂缓 0.6.1.5 的发布，因为我还想把另外一些内容纳入下一个版本。当前计划是在本周末发布，所以请留意最新消息。

0.6.2 版本将包含大量出色的改进来应对更强大的对手，但有一件事它不会影响：性能。虽然匿名性无疑是 I2P 的全部意义所在，但如果吞吐量和时延很差，我们就不会有任何用户。因此，我的计划是在着手实现 0.6.2 的对等节点排序策略和新的 tunnel 创建技术之前，先把性能提升到应有的水平。

* 2) I2Phex

最近在 I2Phex 方面也有不少动向，并发布了新的 0.1.1.35 版本 [1]。CVS 中也有进一步的改动（感谢 Legion!），所以如果在本周晚些时候看到 0.1.1.36，我也不会感到惊讶。

在 gwebcache（基于 Web 的节点缓存）方面也取得了一些不错的进展（参见 http://awup.i2p/），不过据我所知，还没有人开始着手修改 I2Phex 以使用支持 I2P 的 gwebcache（有兴趣吗？告诉我一声！）

[1] http://forum.i2p.net/viewtopic.php?t=1157

* 3) I2P-Rufus

据传，defnax 和 Rawn 一直在对 Rufus BT 客户端动手改造，把 I2P-BT 中的一些与 I2P 相关的代码整合进去。我不清楚这个移植目前的状态，但听起来它会带来一些不错的功能。等到有更多进展，我们肯定会听到更多消息。

* 4) I2PSnarkGUI

还有一种传闻称，Markus 正在对一个新的 C# GUI 进行一些开发……在 PlanetPeer 上的截图看起来相当酷 [2]。我们仍然计划提供一个平台无关的 Web 界面，不过这个看起来也很不错。我相信随着该 GUI 的进展，我们会听到更多来自 Markus 的消息。

[2] http://board.planetpeer.de/index.php?topic=1338

* 5) Syndie

关于 Syndie 的 UI 改版[3]也有一些讨论正在进行中，我预计我们很快就能在这方面看到一些进展。dust 也在埋头推进 Sucker 的开发，为将更多 RSS/Atom 订阅源导入 Syndie 提供更好的支持，同时对 SML 本身也进行了一些改进。

[3] http://syndiemedia.i2p.net:8000/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&entry=1131235200000&expand=true

* 6) ???

像往常一样，事情多得很。几分钟后来 #i2p 参加我们每周的开发者会议。

=jr
