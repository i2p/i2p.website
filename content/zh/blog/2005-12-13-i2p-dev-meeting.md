---
title: "I2P 开发者会议 - 2005年12月13日"
date: 2005-12-13
author: "jrandom"
description: "I2P 开发会议记录（2005 年 12 月 13 日）。"
categories: ["meeting"]
---

## 快速回顾

<p class="attendees-inline"><strong>出席者：</strong> cervantes, jrandom, spaetz</p>

## 会议记录

<div class="irc-log"> 15:15 &lt;jrandom&gt; 0) 嗨 15:15 &lt;jrandom&gt; 1) 网络状态和负载测试 15:15 &lt;jrandom&gt; 2) I2PSnark 15:15 &lt;jrandom&gt; 3) Syndie 15:15 &lt;jrandom&gt; 4) ??? 15:15 &lt;jrandom&gt; 0) 嗨 15:15  * jrandom 挥手 15:15 &lt;jrandom&gt; 每周状态说明已发布在 @ http://dev.i2p.net/pipermail/i2p/2005-December/001239.html 15:15 &lt;jrandom&gt; （本周在会议*之前*——谁能想到呢？） 15:16 &lt;jrandom&gt; 倒也没啥关系，反正你们都要等会议开始才会去看 ;) 15:16 &lt;jrandom&gt; 那么，继续进入 1) 网络状态和负载测试 15:16 &lt;@cervantes&gt; 嘿！ 15:17 &lt;jrandom&gt; 谢谢你出力，cervantes ;) 15:17 &lt;@cervantes&gt; 读什么？ 15:17 -!- DreamTheaterFan [anonymous@irc2p] 已退出 [连接被对端重置] 15:17 &lt;jrandom&gt; 除了邮件里的内容外我没太多要补充的，关于 1) 有人有问题或评论吗？ 15:19 &lt;spaetz&gt; 负载测试是在*那个* I2P 网络上进行的吗，还是你们有一个私有网络来做这个？ 15:19 &lt;jrandom&gt; 我是在真实网络上做的 15:19 &lt;spaetz&gt; 只是好奇 15:19 &lt;spaetz&gt; 好 15:20 &lt;jrandom&gt; 不过是很谨慎地进行的，对处于负载下的对等端会强力退避，而且当然会遵守对 tunnel 的拒绝 15:20 &lt;@cervantes&gt; 最近 irc2p 的不稳定与这些测试无关 15:21 &lt;@cervantes&gt; （以防你在想这事） 15:21 &lt;jrandom&gt; 新的设置应对得怎么样，cervantes？ 15:21 &lt;@cervantes&gt; 到目前为止一直非常稳固 15:22 &lt;jrandom&gt; 酷 15:22 &lt;@cervantes&gt; 只是花了些枯燥的功夫才追查到那些怪异小毛病的根源 15:24 &lt;jrandom&gt; 好的，还有别人有任何问题/评论，还是我们跳到 2) I2PSnark？ 15:25 &lt;jrandom&gt; 就当我们已经跳过去了 15:26 &lt;jrandom&gt; 好的，基本上 I2PSnark 又该能正常工作了……有几个 BT 规范中尚未包含、但被 azureus 和 rufus 使用的属性，导致了不兼容，不过对于我能看到的那些情况，我们现在已经兼容了 15:26 &lt;jrandom&gt; i2psnark 现在在我测试过的所有种子上都能正常工作，但如果有人遇到问题，请告诉我 15:27 &lt;jrandom&gt; 促使我修复它的部分动力与一些 SAM 缺陷有关，因为 I2PSnark 不使用 SAM 15:28 &lt;jrandom&gt; 这方面也没太多要补充的……除非有人有问题，否则我们继续到 3) Syndie 15:29 -!- Xunk [Xunk@irc2p] 已退出 [连接被对端重置] 15:30 &lt;jrandom&gt; 好的，除了邮件里的内容外，这方面我也没太多可补充的 15:31 -!- Xunk [Xunk@irc2p] 已加入 #i2p 15:31 &lt;jrandom&gt; 如果没有关于 Syndie 的问题，我们继续，进入自由讨论，4) ??? 15:31 -!- DreamTheaterFan [anonymous@irc2p] 已加入 #i2p 15:32  * jrandom 想起来 clunk 不在议程上，还有其他一些事。 有人有想提的内容吗？ 15:32 &lt;@cervantes&gt; 老兄，推进得真快 though 15:32 &lt;@cervantes&gt; *through 15:33 -!- bar [bar@irc2p] 已退出 [连接被对端重置] 15:33 &lt;jrandom&gt; 嗯，没必要为了在会议日志里多几行字而说话 :) 15:33 -!- bar [bar@irc2p] 已加入 #i2p 15:33 -!- mode/#i2p [+v bar] by chanserv 15:33 -!- mule [mule@irc2p] 已加入 #i2p 15:35 &lt;jrandom&gt; 好了，如果没有别的…… 15:35  * jrandom 开始收尾 15:35  * jrandom *baf* 地宣布会议结束 </div>
