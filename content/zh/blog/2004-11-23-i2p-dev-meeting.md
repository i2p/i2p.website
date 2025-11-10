---
title: "I2P 开发者会议 - 2004年11月23日"
date: 2004-11-23
author: "jrandom"
description: "2004年11月23日的 I2P 开发会议记录。"
categories: ["meeting"]
---

## 快速回顾

<p class="attendees-inline"><strong>出席：</strong> jrandom, lba, postman, Ragnarok</p>

## 会议记录

<div class="irc-log"> 13:03 &lt;jrandom&gt; 0) 嗨 13:03 &lt;jrandom&gt; 1) 网络状态 13:03 &lt;jrandom&gt; 2) Streaming 库 13:04 &lt;jrandom&gt; 3) 0.4.2 13:04 &lt;jrandom&gt; 4) Addressbook.py 0.3.1 13:04 &lt;jrandom&gt; 5) ???  13:04 &lt;jrandom&gt; 0) 嗨 13:04  * jrandom 挥手 13:04 &lt;+postman&gt; 嗨 :) 13:04 &lt;jrandom&gt; 每周状态说明已发布到 http://dev.i2p.net/pipermail/i2p/2004-November/000490.html 13:05 &lt;jrandom&gt; 好吧，那就直接进入 1) 网络状态 13:05 &lt;jrandom&gt; 除邮件里已有的，我没什么可补充的 13:05 &lt;jrandom&gt; 关于上周的网络状态，有人想提什么吗？ 13:06 &lt;jrandom&gt; 如果没有，我们可以往下到 2) Streaming 库 13:06 &lt;jrandom&gt; 邮件里有很多相关信息，我让大家先消化一下 13:07 &lt;jrandom&gt; 虽然新的库会改进很多方面，但最重要的（依我拙见）是它的健壮性以及对拥塞的处理 13:08 &lt;jrandom&gt; 尤其是后者，因为我们已经见识过旧的库在严重拥塞时会变得多么不正常 13:08 &lt;jrandom&gt; 不过库里也刻意留空了不少东西，方便大家试验并进一步优化 13:09 &lt;jrandom&gt; 对此有人有问题吗，或者我们过去一个月每周都在炒冷饭了？  ;) 13:10 &lt;+Ragnarok&gt; 那就当作是有吧 13:10 &lt;jrandom&gt; 呵 13:10 &lt;jrandom&gt; 好，继续到 3) 0.4.2 13:10 &lt;jrandom&gt; 很快就会发布，目前只是在对安装流程做一些小更新 13:11 &lt;+postman&gt; 太好啦 13:11 &lt;+postman&gt; :) 13:11 &lt;jrandom&gt; 更新后的安装流程会对用户更友好，解决一些最常见的用户错误 13:12 &lt;jrandom&gt; （毕竟没人会看 router 控制台上的文字 ;) 13:12 &lt;jrandom&gt; 但这一两天就该准备好了，做些测试后我们应能在周五发布 13:12 &lt;jrandom&gt; （或者更早） 13:13 &lt;jrandom&gt; 不过正如我在邮件里提到的，它既向后兼容，也/不/向后兼容 13:13 &lt;+Ragnarok&gt; 棒极了 13:13 &lt;jrandom&gt; 关于我们该如何处理这件事，有没有什么强烈的偏好？ 13:13 &lt;jrandom&gt; 我们是否就直接发布 0.4.2，让大家在发现无法访问任何 eepsites 时再升级？ 13:14 &lt;jrandom&gt; （还是他们会把它卸载，然后说“dood i2p sux0rz”） 13:14  * jrandom 两者都不是 13:15 &lt;+Ragnarok&gt; 我建议标注为不兼容。 明确总是更好。 13:15 &lt;jrandom&gt; 嗯，文档和公告里会写明不兼容，并用大号粗体字标出必须升级 13:16 &lt;+Ragnarok&gt; 那就没理由发出混淆的信息了 13:16 &lt;jrandom&gt; 嗯 13:16 &lt;jrandom&gt; 不过我们还是可以通过那些旧的对等节点进行 tunnel 路由 13:16 &lt;jrandom&gt; 我也不确定，反正还有几天可以最后拍板 13:17 &lt;jrandom&gt; 只是给大家一个需要考虑的问题，同时警告各位需要升级到 0.4.2  13:17 &lt;jrandom&gt; :) 13:18 &lt;jrandom&gt; 好，关于 0.4.2 有任何问题/评论/顾虑吗，还是我们进入 4) Addressbook.py? 13:18 &lt;jrandom&gt; 那就算是进入了 13:18 &lt;jrandom&gt; Ragnarok：能给我们更新一下吗？ 13:20 &lt;+Ragnarok&gt; 当然。 小更新昨天发布。 修复了在 Windows 上的一些 bug，如果没有代理也不会直接崩溃。 真正值得注意的是，除非出现重大 bug，否则这可能是该版本的最后一次发布。 13:20 &lt;jrandom&gt; 好，酷 13:21 &lt;jrandom&gt; 能避免直接崩溃一直都是个很好的特性 13:21 &lt;lba&gt; 大家好 13:21 &lt;+Ragnarok&gt; 我计划基于 jrandom 在邮件列表上的想法，从零把它重新设计（其实就是设计出来）。 也可能会用 Java，如果我能搞定需要做的 XML 解析和 HTTP 相关的东西。 13:21 &lt;jrandom&gt; 太酷了 :) 13:21 &lt;jrandom&gt; 嗨 lba 13:22 &lt;+Ragnarok&gt; 好了，我这边就这些。 继续。 13:22 &lt;jrandom&gt; 不错，感谢更新 13:22 &lt;jrandom&gt; 好，如果那部分没别的了，我们就以飞快的速度进入 5) ??? 13:22 &lt;jrandom&gt; 还有谁想提点什么？ 13:23 &lt;+Ragnarok&gt; 这里还有别人吗？ 13:23 &lt;jrandom&gt; 呵，是啊，我们平时那帮爱抱怨的人今天不在 ;) 13:24 &lt;jrandom&gt; 不过他们稍后会跑到网站上来看日志的 [对，说的就是*你*] 13:24 &lt;jrandom&gt; 好，我想这可能是一年多来我们最短的一次会议 13:25 &lt;jrandom&gt; 那就收尾吧 13:25  * jrandom 收尾 13:25  * jrandom 用*baf*把会议关了 </div>
