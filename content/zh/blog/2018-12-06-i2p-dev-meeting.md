---
title: "I2P 开发者会议 - 2018年12月6日"
date: 2018-12-06
author: "zzz"
description: "2018年12月6日的 I2P 开发会议记录。"
categories: ["meeting"]
---

## 简要回顾

<p class="attendees-inline"><strong>出席：</strong> alex, zlatinb, zzz</p>

## 会议记录

<div class="irc-log"> 20:00:00 &lt;zzz&gt; 0) 嗨 20:00:00 &lt;zzz&gt; 1) 0.9.38 开发状态（zzz） 20:00:00 &lt;zzz&gt; 2) LS2 状态（zzz） 20:00:00 &lt;zzz&gt; 3) 35c3 情况（echelon） 20:00:00 &lt;zzz&gt; 4) 状态 scrum（zlatinb） 20:00:03 &lt;zzz&gt; 0) 嗨 20:00:05 &lt;zzz&gt; 嗨 20:00:08 &lt;zlatinb&gt; 嗨 20:00:13 &lt;zzz&gt; 1) 0.9.38 开发状态（zzz） 20:00:32 &lt;zzz&gt; 38 看起来会是一次非常大的发布，我们已经有超过 3 万行的 diff 了 20:01:03 &lt;zzz&gt; 到目前为止已提交的新内容包括新的向导的基础部分、全新的 geoip 实现，以及初步的 LS2 支持 20:01:26 &lt;zzz&gt; 37 运行得很顺利，全网已有 75% 或更多在运行它，未报告 NTCP2 问题 20:01:55 &lt;zzz&gt; 图标和 CSS 的更改应该会在下周开始显现 20:02:21 &lt;zzz&gt; 我们的计划是在一月下旬发布。假期要休两周的情况下，从现在到那时仍有很多事情要做 20:02:26 &lt;zzz&gt; 但到目前为止一切进展顺利 20:02:50 &lt;zzz&gt; 我鼓励大家测试来自 bobthebuilder.i2p 的开发版构建，或者自己构建 20:03:08 &lt;zzz&gt; 改动很多，我们需要测试者，现在就把问题找出来，而不是发布之后 20:03:15 &lt;zzz&gt; 关于 1) 还有别的吗？ 20:04:16 &lt;zzz&gt; 2) LS2 状态（zzz） 20:04:47 &lt;zzz&gt; 我们昨天开了第 19 次每周会议。LS2 的基础部分已经完成，我正在为 38 实现它 20:05:28 &lt;zzz&gt; 目前我们在并行做两件事——编写加密的 LS2 规范，并着手 proposal 144，它定义了一个依赖于 LS2 的新加密算法和端到端协议 20:05:43 &lt;zzz&gt; 加密版 LS2 很快就会收尾。 20:06:24 &lt;zzz&gt; proposal 144，我们称之为 ECIES-X25519-AEAD-ratchet，相当复杂，我认为需要一两个月来打磨 20:06:41 &lt;zzz&gt; 会议在每周一 UTC 7:30 于 #ls2 举行，欢迎所有人参加 20:06:55 &lt;zzz&gt; 关于 2) 还有别的吗？ 20:08:00 &lt;zzz&gt; 3) 35c3 情况（echelon） 20:08:17 &lt;zzz&gt; 我想 echelon 今天来不了 20:08:46 &lt;zzz&gt; 我知道他在做桌面横幅方案，还有要发放的糖果，而且他把我们的票都买好了 20:08:56 &lt;zzz&gt; 所以我觉得我们准备得不错，三周后现场见 20:09:01 &lt;zzz&gt; 关于 3) 还有别的吗？ 20:09:51 &lt;zzz&gt; 哦，还有个提醒，1 月 1 日我们不会在这里开会，我们的会议将会在 CCC 举行。这里的下一次会议是 2 月 5 日 20:10:11 &lt;zzz&gt; 4) 状态 scrum（zlatinb） 20:10:15 &lt;zzz&gt; zlatinb，请开始  20:10:28 &lt;zlatinb&gt; 嗨。我们打算并行进行 scrum（敏捷站会），反正在 IRC 上也很容易跟进。直接开始输入：1) 过去一个月你做了什么 2) 下个月你计划做什么 3) 有任何阻碍或需要帮助的吗。用 EOT 结束你的报告 20:10:56 &lt;zzz&gt; 好的，让我们看看进展如何…… 20:11:10 &lt;alex_the_designerr&gt; alex 我真的很喜欢这里的六边形： 图标工作正在推进，正如 zzz 在 1) 中提到的 20:11:30 &lt;alex_the_designerr&gt; 上个月我做了网站更新和一些 logo 工作 20:11:48 &lt;zlatinb&gt; 1) 进行新手引导相关工作，主要是向导，以及使用 IDK 的 Windows 版 Firefox 安装程序。拿到了签名证书，这样我们的 Windows 安装程序就可以签名了。在 snark 上做了一些小的试验性改动 20:12:09 &lt;alex_the_designerr&gt; 下个月我将完成新网站的首版发布、合并图标，并且 *希望* 获得对新 logo 的认可 20:12:21 &lt;zlatinb&gt; 2) 完成 Windows 版 Firefox 配置文件安装器以及 0.9.38 的向导工作 20:12:32 &lt;alex_the_designerr&gt; 扩展目标是 personas（用户画像）和图案 20:13:01 &lt;alex_the_designerr&gt; 没有阻碍，就是抓紧推进 EOT 20:13:06 &lt;zlatinb&gt; 3) 没有阻碍，但需要与 zzz 密切合作，以一种有意义的方式把东西放进 monotone；如果要在 OSX 复用 Firefox 配置文件，也需要与 meeh 合作 20:13:07 &lt;zlatinb&gt; EOT 20:13:09 &lt;zzz&gt; 我：1) 向导、geoip、LS2、提案 144、修复缺陷； 2) LS2、提案 144、整合设计团队的改动、修复缺陷、准备 35C3、35C3、搭建签名机器； 3) 无阻碍 EOT 20:13:57 &lt;zlatinb&gt; 团队里还有其他人吗？ 20:14:30 &lt;zlatinb&gt; 看起来没有了。关于 4) 我这边就这些 20:14:47 &lt;zzz&gt; 好的，关于这次会议还有其他事项吗？ 20:15:49 * zzz 找到 baffer 20:16:06 * zzz *bafs* 会议结束 </div>
