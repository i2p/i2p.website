---
title: "I2P 2006-02-14 状态说明"
date: 2006-02-14
author: "jr"
description: "0.6.1.10 发布公告，包含与旧版本不兼容、PRE network 进展，以及 Syndie 活跃度提升"
categories: ["status"]
---

大家好，今天做个简要更新。

* Index

1) 网络状态 2) 0.6.1.10 3) Syndie 活动 4) ???

* 1) Net status

正如我上周所说，"过去一周线上网络（live net）没有任何实质性的变化，因此线上网络的状态也没有太大变化。另一方面..."

* 2) 0.6.1.10

There has been more progress with the _PRE network to get us to the 0.6.1.10 release, and the other day I gave y'all the 5 day warning [1].  Things are still on track, so I expect 0.6.1.10 to be out sometime late thursday.  The release will not be backwards compatible, and your router will likely create a new router identity and require reseeding to get onto the new network.  This should happen transparently though.

[1] http://dev.i2p.net/pipermail/i2p/2006-February/001259.html

不过，给 CVS 用户一句提醒——今晚的会议结束后，我将开始把 _PRE 分支合并回主干，所以在 0.6.1.10 发布之前请暂时不要使用 CVS。

* 3) Syndie activity

最近 Syndie 上的流量有所增加，这挺酷的，所以不妨去你本地的实例 [2] 或公共节点 [3] 看看发生了什么。

[2] http://localhost:7657/syndie/blogs.jsp [3] http://syndiemedia.i2p.net/blogs.jsp

* 4) ???

目前就这些，几分钟后到会议那边来打个招呼！

=jr
