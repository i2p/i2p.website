---
title: "I2P 开发者会议 - 2019年9月3日"
date: 2019-09-03
author: "zzz"
description: "I2P 2019年9月3日开发会议记录。"
categories: ["meeting"]
---

## 快速回顾

<p class="attendees-inline"><strong>出席：</strong> eyedeekay, sadie, zlatinb, zzz</p>

## 会议记录

<div class="irc-log">                注意：sadie 的消息在会议期间未显示，已在下方粘贴。

20:00:00 &lt;zzz&gt; 0) 嗨
20:00:00 &lt;zzz&gt; 1) 0.9.42 发布状态 (zzz)
20:00:00 &lt;zzz&gt; 2) I2P 浏览器“labs”项目状态 (sadie, meeh)
20:00:00 &lt;zzz&gt; 3) Outproxy（出口代理）用例/状态 (sadie)
20:00:00 &lt;zzz&gt; 4) 0.9.43 开发状态 (zzz)
20:00:00 &lt;zzz&gt; 5) 提案状态 (zzz)
20:00:00 &lt;zzz&gt; 6) 状态 scrum (zlatinb)
20:00:04 &lt;zzz&gt; 0) 嗨
20:00:06 &lt;zzz&gt; 嗨
20:00:17 &lt;zlatinb&gt; 嗨
20:00:30 &lt;zzz&gt; 1) 0.9.42 发布状态 (zzz)
20:00:48 &lt;zzz&gt; 上周发布进行得相当顺利
20:00:56 &lt;zzz&gt; 只剩下少数几件事
20:01:27 &lt;zzz&gt; 让 github bridge 恢复工作（nextloop）、Debian sid 包（mhatta），以及我们在 41 中忘记了的 Android 客户端库（meeh）
20:01:37 &lt;zzz&gt; nextloop、meeh，这些事项有预计完成时间吗？
20:03:06 &lt;zzz&gt; 关于 1) 还有别的吗？
20:04:02 &lt;zzz&gt; 2) I2P 浏览器“labs”项目状态 (sadie, meeh)
20:04:25 &lt;zzz&gt; sadie、meeh，现在的状态如何，下一步的里程碑是什么？          &lt;sadie&gt; 原计划周五发布 Beta 5，但出现了一些问题。看起来有些已经准备好了 https://i2bbparts.meeh.no/i2p-browser/ 但我确实需要听 meeh 确认下一次的截止日期。          &lt;sadie&gt; Lab 页面将在本周末上线。下一个浏览器里程碑将讨论 Beta 6 发布的控制台需求
20:05:51 &lt;zzz&gt; 关于 2) 还有别的吗？
20:06:43 &lt;zzz&gt; 3) Outproxy（出口代理）用例/状态 (sadie)
20:06:57 &lt;zzz&gt; sadie，现在的状态如何，下一步的里程碑是什么？          &lt;sadie&gt; 任何人都可以在工单 2472 上查看我们的会议记录。我们已经确定了用例状态，并整理了一份需求清单。下一步里程碑将是“朋友和家人”用例的用户需求，以及“朋友和家人”和“通用途例”的开发需求，以便看出它们可能在哪些方面重叠
20:08:05 &lt;zzz&gt; 关于 3) 还有别的吗？
20:08:19 &lt;eyedeekay&gt; 抱歉我迟到了
20:09:01 &lt;zzz&gt; 4) 0.9.43 开发状态 (zzz)
20:09:21 &lt;zzz&gt; 我们刚开始 43 周期，计划大约 7 周后发布
20:09:40 &lt;zzz&gt; 我们已经更新了网站上的路线图，但还会再增加一些项
20:10:06 &lt;zzz&gt; 我一直在修复一些 IPv6 缺陷，并加速 tunnel 的 AES 处理
20:10:30 &lt;zzz&gt; 很快我会把注意力转向新的盲化信息 I2CP 消息
20:10:59 &lt;zzz&gt; eyedeekay、zlatinb，关于 .43 你们还有要补充的吗？
20:11:46 &lt;eyedeekay&gt; 我觉得没有
20:12:02 &lt;zlatinb&gt; 可能会有更多测试网方面的工作
20:12:32 &lt;zzz&gt; 是的，关于 SSU，我们还有几张 jogger 工单要看
20:12:48 &lt;zzz&gt; 关于 4) 还有别的吗？
20:14:00 &lt;zzz&gt; 5) 提案状态 (zzz)
20:14:20 &lt;zzz&gt; 我们的主要精力放在非常复杂的新加密提案 144 上
20:14:48 &lt;zzz&gt; 近几周我们取得了不错的进展，并对提案本身做了重大更新
20:15:35 &lt;zzz&gt; 还有一些清理和空白需要补上，但我希望它已经足够成熟，我们很快就能开始编写一些单元测试实现，也许在本月底之前
20:16:17 &lt;zzz&gt; 另外，提案 123（加密的 LS2）的盲化信息消息，我将在下周开始编码后再审视一次
20:16:52 &lt;zzz&gt; 另外，我们预计很快会收到 chisana 关于提案 152（tunnel 构建消息）的更新
20:17:27 &lt;zzz&gt; 我们上个月完成了提案 147（跨网络防护），i2p 和 i2pd 都已实现并包含在 .42 版本中
20:18:23 &lt;zzz&gt; 所以事情都在推进中，尽管 144 看起来进展缓慢又艰巨，它其实也在稳步前进
20:18:27 &lt;zzz&gt; 关于 5) 还有别的吗？
20:20:00 &lt;zzz&gt; 6) 状态 scrum (zlatinb)
20:20:05 &lt;zzz&gt; 交给你了，zlatinb
20:20:42 &lt;zlatinb&gt; 嗨，请简要说明：1) 自上次 scrum 以来你做了什么 2) 下个月你计划做什么 3) 有阻碍或需要帮助的吗。完成后说 EOT
20:21:23 &lt;zlatinb&gt; 我：1) 在测试网上做了各种实验以加速大容量传输 2) 在希望更大一些的服务器/网络上做更多测试网工作 3) 无阻碍 EOT
20:22:15 &lt;zzz&gt; 1) 缺陷修复、配置拆分更改、.42 发布、提案、DEFCON 工作坊（参见我在 i2pforum 和我们网站上的行程报告）
20:23:56 &lt;zzz&gt; 2) 缺陷修复、提案 144、盲化信息消息、提速、协助 Outproxy（出口代理）研究、修复被 conf. 拆分弄坏的 SSL 向导
20:24:20 &lt;zzz&gt; 更多 IPv6 修复
20:24:38 &lt;zzz&gt; 3) 无阻碍 EOT
20:24:50 &lt;eyedeekay&gt; 1) 自上次 scrum 以来，我一直在做缺陷修复、网站、推进 outproxy 提案，以及与 i2ptunnels 有关的工作。2) 继续重组并改进网站的呈现。推进 outproxy 提案 3) 无阻碍 EOT          &lt;sadie&gt; 1) 参加了 FOCI，研究了资助选项，会见了潜在资助方，与 Tails（包括 Mhatta）开了会，处理 I2P 浏览器品牌，与 IDK 一起进行网站更新，为上一次发布对控制台做了些小改动          &lt;sadie&gt; 2) 下个月我将处理资助申请、改进控制台和网站、设置向导、在多伦多参加 Our Networks，推进 I2P 浏览器和 Outproxy 研究          &lt;sadie&gt; 3) 无阻碍 EOT
20:25:29 &lt;zlatinb&gt; scrum.setTimeout( 60 * 1000 );
20:27:04 &lt;zzz&gt; 好的，超时了
20:27:10 &lt;zlatinb&gt; ScrumTimeoutException
20:27:41 &lt;zzz&gt; 最后一次呼叫 sadie、meeh、nextloop 回到 1)-3)
20:27:52 &lt;zzz&gt; 会议还有其他主题吗？
20:28:47 * zzz 抓起了 baffer
20:30:00 * zzz ***bafs*** 会议结束
</div>
