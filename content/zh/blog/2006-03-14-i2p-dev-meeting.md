---
title: "I2P 开发者会议 - 2006年3月14日"
date: 2006-03-14
author: "@jrandom"
description: "I2P development meeting log for March 14, 2006."
categories: ["meeting"]
---

## 简要回顾

<p class="attendees-inline"><strong>出席：</strong> bar, cervantes, Complication, fc, frosk, jrandom, ripple, susi23, tethra, tmp</p>

## 会议记录

<div class="irc-log"> 15:09 &lt;@jrandom&gt; 0) 嗨 15:09 &lt;@jrandom&gt; 1) 网络状态 15:09 &lt;@jrandom&gt; 2) ??? 15:09 &lt;@jrandom&gt; 0) 嗨 15:09  * jrandom 挥手 15:09 &lt;@jrandom&gt; 每周状态说明已发布在 http://dev.i2p.net/pipermail/i2p/2006-March/001270.html 15:10 &lt;@jrandom&gt; 当你们阅读那封长篇大论时，我们先进入 1) 网络状态 15:10 &lt;@jrandom&gt; 网络看起来仍然正常（耶） 15:12 &lt;bar&gt; 昨天我的 udp 连接创下新高，244 15:12 &lt;@jrandom&gt; 我在这方面没太多可补充的——有人有任何评论/问题/担忧吗？ 15:12 &lt;@jrandom&gt; 啊，不错 15:12 &lt;@jrandom&gt; 对，我这边也达到了峰值，目前有 338 个 SSU 连接 15:14  * jrandom 也进行了一些相当大的 i2psnark（I2P 自带的 BitTorrent 客户端）传输，不过速率不总是很理想 15:15 &lt;@jrandom&gt; 我在 stats.i2p 上看到关于 tunnel 选择有一些有趣的周期性变化，不过随着 .0.6.1.13 推出，这方面会有一些改动 15:17 &lt;@jrandom&gt; 我也在做低（更低）带宽的测试和优化，而这其实是目前拖住 ...13 的原因。我想很快会有些不错的东西到来，不过我们再看看进展如何 15:18 &lt;@jrandom&gt; 好，如果 1) 网络状态 没有其他内容，我们把话题交给大家——2) ??? 15:18 &lt;@jrandom&gt; 有人想提什么吗？ 15:18 &lt;+Complication&gt; 我只想汇报创纪录的在线时长，并补充说 build -6 在接受参与型 tunnel 时非常保守 15:19 &lt;+Complication&gt; （不过我之前已经提到过了） 15:19 &lt;@jrandom&gt; 不错——即使在更低的 peer 数量下，它表现也还可以，对吧？ 15:19 &lt;+Complication&gt; 其实最近 peer 数量有点上升 15:20 &lt;@jrandom&gt; 啊，OK 15:20 &lt;+Complication&gt; 现在更像是 50...100 15:20 &lt;+Complication&gt; （通常更接近 50 而不是 100） 15:20 &lt;@jrandom&gt; 哦，那相比之前仍然算比较低 15:20 &lt;+Complication&gt; 大约 30 的值似乎就是最低了 15:21 &lt;+Complication&gt; 不过总体来说运行良好 15:21 &lt;@jrandom&gt; 太好了 15:26  * jrandom 想借此机会向近期支持 I2P 的一些贡献者致意——特别感谢 bar、$anon、postman，以及 http://www.i2p.net/halloffame 上的其他各位！ 15:27 &lt;@jrandom&gt; 代码和内容的贡献当然至关重要，但资金支持能让我不必去普通的工作岗位，从而全职埋头 I2P 的开发，并且还能覆盖我们多样的基础设施成本 15:28 &lt;bar&gt; 我脸红了，不过谢谢 :) 15:28 &lt;@cervantes&gt; w00t 15:29 &lt;+Complication&gt; 不错 :) 15:31 &lt;ripple&gt; jrandom: pastebin.i2p...任务完成.... 15:32 &lt;@jrandom&gt; ripple: 多谢——看起来它的行为符合预期——在 OOM（内存耗尽）时，它会快速而惨烈地死亡，服务包装器会检测到并重启 router 15:32 &lt;@jrandom&gt; 好，关于会议还有别的吗？ 15:34 &lt;tmp&gt; 是的，让我们为 Betty 的恢复祈祷。 15:34  * tethra 祈祷 15:34 &lt;@jrandom&gt; 你们的祈祷得到了回应——她回来了 :) 15:34 &lt;tmp&gt; 信仰驱动的 I2P。 15:35 &lt;tmp&gt; 好的。 ;) 15:35 &lt;tethra&gt; 太棒了 15:35 &lt;tethra&gt; XD 15:35 &lt;fc&gt; tmp：那是某种传输协议还是什么？ 15:35 &lt;tethra&gt; 匿名祈祷？ 15:35 &lt;@jrandom&gt; betty == 我的笔记本电脑 15:35 &lt;tethra&gt; 连上帝都不知道你是谁！ 15:36 &lt;@frosk&gt; bar 如此给力捐赠的新机器怎么样了？ 15:36 &lt;+susi23&gt; jr：你没把它命名为 susi??? 真该羞羞你 ;) 15:37 &lt;@jrandom&gt; 新机器目前正在组装中，一台 x86_64（x2）机器，跑 Windows、Gentoo，也许还有 fbsd 15:37 &lt;@frosk&gt; 酷 15:37 &lt;@jrandom&gt; （一旦准备好，敬请期待我博客上的一些照片 ;) 15:38 &lt;fc&gt; bsd! bsd! bsd! ;) 15:38 &lt;@jrandom&gt; susi23：新的那台需要一个新名字... ;) 15:38 &lt;@cervantes&gt; susan! 15:39 &lt;@jrandom&gt; ;) 15:39 &lt;@jrandom&gt; 好，如果会议没有其他内容了... 15:39  * jrandom 收尾 15:39  * jrandom *baf* 地宣布会议结束 </div>
