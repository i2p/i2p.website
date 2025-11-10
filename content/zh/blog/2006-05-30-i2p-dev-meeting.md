---
title: "I2P 开发者会议 - 2006年5月30日"
date: 2006-05-30
author: "jrandom"
description: "2006年5月30日的 I2P 开发会议记录。"
categories: ["meeting"]
---

## 快速回顾

<p class="attendees-inline"><strong>出席：</strong> bar, cervantes, frosk, green, jrandom, tethrar</p>

## 会议记录

<div class="irc-log"> 16:00 &lt;jrandom&gt; 0) 嗨 16:00 &lt;jrandom&gt; 1) 网络状态 16:00 &lt;jrandom&gt; 2) 节点过滤 16:00 &lt;jrandom&gt; 3) Syndie 状态 16:00 &lt;jrandom&gt; 4) ??? 16:00 &lt;jrandom&gt; 0) 嗨 16:00  * jrandom 挥手 16:01 &lt;jrandom&gt; 每周状态说明已发布在 @ http://dev.i2p.net/pipermail/i2p/2006-May/001291.html 16:01 &lt;jrandom&gt; （提前了一小时发布哦 [或者说晚了几周，如果你想调侃我 ;]） 16:02 &lt;jrandom&gt; 好的，我们直接进入 1) 网络状态 16:02 &lt;jrandom&gt; 情况没有达到应有的状态。比拥塞崩溃期间要好，但现在理应比目前更好 16:03 &lt;jrandom&gt; 关于这点我没有更多可补充的，除非有人对 1) 有问题/担忧？ 16:03 &lt;@frosk&gt; 我用 .19 可以连续连 IRC 好几天，所以这边没意见 16:04 &lt;jrandom&gt; 不错 16:04 &lt;jrandom&gt; 是的，对一些人来说不错，但还不够好、也不够稳定。数据库里的统计看起来也不太理想 16:06 &lt;jrandom&gt; 好的，关于 1) 网络状态还有别的吗，或者我们转到 2)节点过滤？ 16:07 &lt;jrandom&gt; [此处插入移动音效] 16:09 &lt;jrandom&gt; 正如邮件中提到的，核心是稍微增强我们的节点选择。起初会有点危险，可能会允许一些主动的分区攻击，但如果按我预期运作，我们可以避免这些 16:10 &lt;jrandom&gt; （但要避免它基本上需要“杀掉”所有 router identities（路由器标识），这相当于一次网络重置，所以除非值得，我想避免这么做） 16:11 &lt;bar&gt; 重置一次还是反复重置？ 16:11 &lt;bar&gt; s/reset/killing 16:11 &lt;jrandom&gt; 至少一次，而且在随后所有重大的配置变更时也要这样做 16:12 &lt;jrandom&gt; （也就是把某些条件写进 router identity 的证书里，这意味着要更改 ident hash，这样他们就不能假装对一些人推送一种设置、对另一些人推送另一种设置） 16:13 &lt;bar&gt; 明白了 16:14 &lt;jrandom&gt; 好的，目前我想在这个话题上没有别的了，除非有人有问题/意见/担忧？ 16:15 &lt;jrandom&gt; （希望一两天内会有一个构建，稳定后再发布） 16:17 &lt;jrandom&gt; 好的，简单说一下 3).. 16:18 &lt;jrandom&gt; Syndie 进展顺利，尽管 amd64/amd32/x86/swt/gcj 之战并不总是好看，但我们会在六月准备好一个构建 16:19 &lt;jrandom&gt; （不过还是别跟我提 mingw/gcj ;)） 16:19 &lt;jrandom&gt; 目前在这方面我没什么可补充的，除非有人对 Syndie 的重做有问题/担忧？ 16:21 &lt;@cervantes&gt; mingw/gcj 的支持进展如何？ 16:21 &lt;@cervantes&gt; *躲* 16:22 &lt;@cervantes&gt; 我们能在六月发布前看到一些截图吗？ :) 16:23 &lt;jrandom&gt; 我肯定会拉些热心志愿者来做预发布测试 ;) 16:23 &lt;tethrar&gt; 算上我 ;) 16:23 &lt;jrandom&gt; w3wt 16:24 &lt;jrandom&gt; 好的，我们转到我知道大家一直在等的要点：4) ??? 16:24 &lt;jrandom&gt; 咋样啊？ 16:24 &lt;green&gt; 有没有计划让 I2P router 在 Via C7 上 "真正" 可用？jbigi 只比纯 Java 提升 30% 16:25 &lt;jrandom&gt; 30% 仍然 CPU 负担过重吗？是什么让它不算 "真正" 的？ 16:25 &lt;jrandom&gt; 不过不行，我没有数学或 C7 汇编技能来为 C7 做一个更好的 libGMP。 16:25 &lt;green&gt; 当然太吃 CPU 了，CPU 负载 100% :P 16:26 &lt;jrandom&gt; CPU 负载 100% 表明问题不在 jbigi，而在于 jbigi 被用得太多 16:26 &lt;jrandom&gt; 为此，是的，我们有很多改进在路上。 16:26 &lt;jrandom&gt; （例如减少连接的重新建立、提高 tunnel 构建成功率等） 16:27 &lt;jrandom&gt; （（而且如果 router 无法处理，就不会接收那么多 tunnel 请求）） 16:29 &lt;green&gt; 嗯，这是在一台专用机器上，带宽 100Mb/s，所以它应该能胜任 16:30 &lt;jrandom&gt; 不，带宽不是这里唯一受限的资源，显然还有 CPU ;) 16:33 &lt;jrandom&gt; 好的，这次会议还有别的议题吗？ 16:36 &lt;jrandom&gt; *咳嗽* 16:37  * jrandom 收尾 16:37  * jrandom *baf* 地把会议关了 </div>
