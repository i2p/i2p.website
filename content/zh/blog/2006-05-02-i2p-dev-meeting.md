---
title: "I2P 开发者会议 - 2006年5月2日"
date: 2006-05-02
author: "jrandom"
description: "I2P 开发会议记录（2006年5月2日）。"
categories: ["meeting"]
---

## 快速回顾

<p class="attendees-inline"><strong>出席：</strong> green, jrandom</p>

## 会议记录

<div class="irc-log"> 16:09 &lt;jrandom&gt; 0) 嗨 16:09 &lt;jrandom&gt; 1) 网络状态 16:09 &lt;jrandom&gt; 2) Syndie 状态 16:09 &lt;jrandom&gt; 3) ??? 16:09 &lt;jrandom&gt; 0) 嗨 16:09  * jrandom 挥手 16:10 &lt;jrandom&gt; 每周状态说明已发布在 http://dev.i2p.net/pipermail/i2p/2006-May/001285.html 16:11 &lt;jrandom&gt; 好的，当大家读那封令人兴奋的邮件时，我们先直接进入 1) 网络状态 16:13 &lt;jrandom&gt; 到目前为止，看来整个拥塞崩溃问题已经修复了，并且 tunnel 创建速率表现不错。  不过，仍然有一些问题需要解决 16:14 &lt;jrandom&gt; 之前讨论过的循环行为（通常以 10–12 分钟为一个周期）仍然存在，导致拒绝（率）出现反向波动。  不过，在 -1 中对代码的新修复应该可以消除这一点 16:15 &lt;jrandom&gt; （也就是要/正确地/随机化 tunnel 的过期时间，而不是像之前那样的有问题的随机化） 16:16 &lt;jrandom&gt; 这些，再加上改进的 ssu 和 tunnel 测试调度，应该会有所帮助，但能到什么程度，我还不太确定 16:17 &lt;jrandom&gt; 好的，目前我关于这部分就这些。  关于 1) 网络状态，有没有任何问题/评论/担忧？ 16:18 &lt;green&gt; 嗯，最大带宽限制从未达到过，而且这和之前相差很大 16:18 &lt;green&gt; 就像在 1-7 中一样 16:18 &lt;green&gt; s/1-7/.12-7 16:18 &lt;jrandom&gt; 你的带宽共享百分比是怎么设的？  那现在是一个非常强力的控制项 16:19 &lt;green&gt; 80% 16:19 &lt;green&gt; 但只使用了总带宽的大约 40% 16:20 &lt;green&gt; 这只是一个“do nothing router” :P 16:20 &lt;jrandom&gt; 嗯，你的带宽多久会飙到 80%，以及你是否经常拒绝 tunnel 请求（http://localhost:7657/oldstats.jsp#tunnel.reject.30 和 tunnel.reject.*） 16:21 &lt;jrandom&gt; tunnel 请求中的周期性经常会让人误判为过载，其实并没有 16:21 &lt;jrandom&gt; （因为 routers 在其他时间有富余容量，只是在被冲击的时候没有） 16:22 &lt;green&gt; tunnel.reject.30 非常平缓，像 1,00，覆盖 14 025,00 个事件 16:22 &lt;jrandom&gt; 哦，抱歉，对那个统计来说关键是事件计数本身——你因为带宽过载已经拒绝了超过 14,000 个 tunnel 请求 16:23 &lt;jrandom&gt; （该统计的“值”是指在该事件中被拒绝的 tunnels 数量，而那总是 1，因为一个事件是由一条消息触发的） 16:27 &lt;jrandom&gt; 好的，如果关于 1) 网络状态 没有其他内容，我们就滑到 2) Syndie 状态 16:27 &lt;jrandom&gt; 关于 syndie，我没有太多要补充的，基本都在邮件里了，只是想做个更新 16:28 &lt;jrandom&gt; 好吧，如果没有人想就 syndie 提什么事，我们就跳到老朋友，3) ??? 16:28 &lt;jrandom&gt; 还有什么想在会议上提出的吗？ 16:31  * tethra 想对 .17 再次说声“谢谢”，因为它改进很多 16:33 &lt;jrandom&gt; 很高兴能帮上忙，而且还有更多东西在路上 16:33 &lt;jrandom&gt; 好的，如果今天的会议没有其他事项... 16:33  * jrandom 收尾 16:33  * jrandom 用 *baf* 结束了会议 </div>
