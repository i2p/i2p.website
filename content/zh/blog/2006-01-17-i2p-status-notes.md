---
title: "2006-01-17 的 I2P 状态说明"
date: 2006-01-17
author: "jr"
description: "0.6.1.9 版本的网络状态、tunnel 创建的密码学改进，以及 Syndie 博客界面更新"
categories: ["status"]
---

大家好，又是星期二了

* Index

1) 网络状态与 0.6.1.9 2) Tunnel 创建加密算法 3) Syndie 博客 4) ???

* 1) Net status and 0.6.1.9

随着 0.6.1.9 发布且网络已有 70% 完成升级，所包含的大多数 bug 修复似乎都按预期工作。据反馈，新的速度分析已经能挑选出一些表现不错的对等节点。我听说在快速对等节点上，持续吞吐量可超过 300KBps，CPU 使用率为 50-70%，而其他 router 则在 100-150KBps 的区间，最慢的一些勉强能到 1-5KBps。不过，router 身份的更替仍然相当严重，所以看来我以为能降低这一情况的修复并没有奏效（或者这些变动确属正常）。

* 2) Tunnel creation crypto

在秋季，围绕我们如何构建我们的 tunnel，以及 Tor 风格的 telescopic（逐段扩展）tunnel 创建与 I2P 风格的探索式 tunnel 创建之间的权衡进行了大量讨论[1]。在此过程中，我们提出了一种组合方案[2]，它消除了 Tor 风格的 telescopic tunnel 创建[3]所带来的问题，保留了 I2P 的单向优势，并减少不必要的失败。由于当时还有许多其他事情在进行，这一新组合的实现被推迟了；但现在我们正接近 0.6.2 的发布，在此期间我们无论如何都需要重构 tunnel 创建代码，是时候把这件事敲定了。

我前几天草拟了一个新的 tunnel（隧道）加密方案的规范草案，并把它发到了我的 Syndie 博客上，在实际实现时出现的一些小改动之后，我们已经在 CVS [4] 中整理出了一份规范。CVS [5] 里也有实现它的基础代码，不过它还没有接入到实际的 tunnel 构建中。如果有人有空，我很希望能得到关于该规范的反馈。与此同时，我会继续开发新的 tunnel 构建代码。

[1] http://dev.i2p.net/pipermail/i2p/2005-October/thread.html 并     查看与引导攻击相关的讨论串 [2] http://dev.i2p.net/pipermail/i2p/2005-October/001064.html [3] http://dev.i2p.net/pipermail/i2p/2005-October/001057.html [4] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/                                tunnel-alt-creation.html?rev=HEAD [5] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/java/src/net/                        i2p/router/tunnel/BuildMessageTest.java

* 3) Syndie blogs

如前所述，这个新的 0.6.1.9 版本对 Syndie 博客界面进行了较大改版，其中包括 cervantes 的新样式，以及每个用户可自行选择的博客链接和徽标（例如 [6]）。你可以在个人资料页面点击 "configure your blog" 链接来控制左侧的那些链接，它会将你带到 http://localhost:7657/syndie/configblog.jsp。  一旦你在那里做出更改，下一次你将帖子推送到某个存档站点（archive）时，这些信息就会对他人可见。

[6] http://syndiemedia.i2p.net/     blog.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=

* 4) ???

既然我已经比会议晚到了20分钟，我就长话短说吧。我知道还有几件别的事在进行，不过与其在这里公开，不如想讨论的开发者来会议上提出。总之，就先这样，#i2p 见！

=jr
