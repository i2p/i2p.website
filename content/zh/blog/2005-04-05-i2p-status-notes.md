---
title: "I2P 2005-04-05 状态说明"
date: 2005-04-05
author: "jr"
description: "每周更新，涵盖 0.5.0.5 版本发布问题、贝叶斯对等节点画像研究，以及 Q 应用进展"
categories: ["status"]
---

大家好，又到了每周更新的时间

* Index

1) 0.5.0.5 2) Bayesian peer profiling(贝叶斯对等节点画像) 3) Q 4) ???

* 1) 0.5.0.5

Last week's 0.5.0.5 release has had its ups and downs - the major change to address some attacks in the netDb seems to work as expected, but has exposed some long overlooked bugs in the netDb's operation. This has caused some substantial reliability issues, especially for eepsites(I2P Sites). The bugs have however been identified and addressed in CVS, and those fixes among a few others will be pushed out as a 0.5.0.6 release within the next day.

* 2) Bayesian peer profiling

bla 一直在研究通过对收集到的统计数据进行简单的贝叶斯过滤来改进我们的对等节点画像[1]。看起来很有前景，不过我不太确定目前的进展如何——也许我们可以在会议期间请 bla 提供一个更新？

[1] http://forum.i2p.net/viewtopic.php?t=598     http://theland.i2p/nodemon.html

* 3) Q

aum 的 Q 应用在核心功能以及由几位开发者构建的各种 xmlrpc 前端方面都有不少进展。据传，本周末我们可能会看到另一个 Q 构建版，包含在 http://aum.i2p/q/ 上所描述的一大批新功能。

* 4) ???

好吧，就写几条非常简短的状态更新，因为我*又一次*把时区搞混了（其实我也把日期搞混了，直到几小时前我还以为今天是周一）。总之，还有不少上面没提到的事情在进行中，顺道来参加会议看看都在忙些什么吧！

=jr
