---
title: "I2P 状态说明（2006-02-21）"
date: 2006-02-21
author: "jr"
description: "0.6.1.10 版本中的网络问题，快速推出的 0.6.1.11 后续版本，以及 IE 安全问题"
categories: ["status"]
---

大家好，又是星期二了

* Index

1) 网络状态 2) ???

* 1) Net status

自 0.6.1.10 发布以来，网络经历了一些波折，部分原因在于向后不兼容，另一些原因则是出现了意料之外的 bug。0.6.1.10 的可靠性和运行时间都不够理想，因此在过去的 5 天里连续发布了一系列补丁，最终推出了新的 0.6.1.11 版本 - http://dev.i2p.net/pipermail/i2p/2006-February/001263.html

在 0.6.1.10 中发现的大多数缺陷自去年九月的 0.6 发布起就已存在，但在仍可回退到替代传输协议（TCP）时并不明显。我的本地测试网络会模拟数据包故障，但并未真正覆盖 router 波动（节点频繁加入/离开）以及其他持续性的网络故障。_PRE 测试网络还包含了一组自我挑选的、相当可靠的对等节点，因此在正式发布之前仍有相当多的情形没有被充分探索。这显然是个问题，下一次我们会确保纳入更广泛的场景。

* 2) ???

There's a bunch of things going on at the moment, but the new 0.6.1.11 release jumped to the head of the queue.  The network will continue to be a bit bumpy until a large number of people are up to date, after which work will continue moving forward.  One thing worth mentioning is that cervantes is working through some sort of IE-related security domain exploit, and while I'm not sure if he is ready to explain the details, preliminary results suggest its viable, so the anonymity-minded out there should avoid IE in the meantime (but you knew that anyway ;).  Perhaps cervantes can give us a summary in the meeting?

总之，暂时我就说这些 - 几分钟后顺道来会议上打个招呼吧！

=jr
