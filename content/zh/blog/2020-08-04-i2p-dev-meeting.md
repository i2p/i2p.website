---
title: "I2P 开发者会议 - 2020年8月4日"
date: 2020-08-04
author: "i2p"
description: "I2P 开发会议记录（2020年8月4日）。"
categories: ["meeting"]
---

## 快速回顾

<p class="attendees-inline"><strong>出席：</strong> eyedeekay, zlatinb, zzz</p>

## 会议日志

<div class="irc-log">

(04:00:50 PM) eyedeekay1: 你好 zlatinb zzz mikalvmeeh eche|on，如果大家都准备好了，我们就开始开会。
(04:00:50 PM) eyedeekay1: 1）你好
(04:00:50 PM) eyedeekay1: 2）0.9.47 发布
(04:00:50 PM) eyedeekay1: 3）每月会议跟进
(04:00:50 PM) eyedeekay1: 4）Git 更新
(04:01:38 PM) eyedeekay1: 大家好，首先，很抱歉我没有注意到我在公告标题里把日期写错了。
(04:02:38 PM) zzz: 嗨
(04:02:58 PM) eyedeekay1: 嗨 zzz
(04:03:31 PM) zlatinb: 嗨
(04:03:42 PM) eyedeekay1: 嗨 zlatinb
(04:04:49 PM) eyedeekay1: 好的，那么 2）0.9.47 发布
(04:05:27 PM) eyedeekay1: 看起来我也赶不上在 0.9.47 前完成 rekeyOnIdle。
(04:05:58 PM) eyedeekay1: 这次我这边主要会包含一些界面元素的更新。
(04:06:19 PM) eyedeekay1: 关于 0.9.47 发布，zzz 或 zlatinb 有什么要补充的吗？
(04:06:43 PM) zzz: 摘要在 http://zzz.i2p/topics/2905
(04:06:49 PM) zzz: 标签冻结时间是从明天算起一周后
(04:06:53 PM) zzz: 大约 3 周后发布
(04:07:07 PM) zzz: diff 约 18,500 行，这很常见
(04:07:23 PM) zzz: 一切进展顺利。我还有几件事要收尾
(04:07:40 PM) zzz: 但我很有信心我们能按计划进行
(04:07:49 PM) zzz: EOT
(04:08:08 PM) eyedeekay1: 我看到昨天进来了不少更新，我一直在你推送的时候逐步查看。很高兴看到你的工作，非常感谢。
(04:08:41 PM) zzz: 那只是一些在我工作区放了好几周的杂项，没什么特别值得一提的
(04:09:42 PM) eyedeekay1: 不过跟着看依然很有收获。我不总是知道各个东西在哪里，观察你的工作有助于我辨认不同事情发生在代码的哪些地方
(04:09:43 PM) zzz: 只是尽量把东西整理好并推上去。有时我会把某些东西测试上好几个月
(04:10:28 PM) zzz: 当然，审阅别人的改动是学习和发现错误的好方法，继续保持
(04:10:39 PM) eyedeekay1: 会的
(04:10:42 PM) eyedeekay1: 如果没有别的，我要进行到 3）超时 1 分钟
(04:12:40 PM) eyedeekay1: 2）每月会议跟进：
(04:12:53 PM) eyedeekay1: 这是每月例会。
(04:12:53 PM) eyedeekay1: 我没有设置 WebIRC 网关，因为据我了解那样做会违反我们的 IRC 规则。
(04:13:13 PM) eyedeekay1: 我现在拿到了会议公告规则的副本，而且这些公告的责任归属也已向我说明清楚。
(04:13:25 PM) eyedeekay1: 9 月 1 日的公告，这次日期是正确的，已经发布。目前还没有议题，请按需添加：http://zzz.i2p/topics/2931-meeting-tues-september-1-8pm-utc
(04:14:55 PM) eyedeekay1: 当然，这会在 0.9.47 发布后不久进行
(04:15:45 PM) eyedeekay1: 关于第 2 项，大家还有什么吗？
(04:17:57 PM) eyedeekay1: 3）Git 迁移
(04:18:34 PM) eyedeekay1: Git 迁移终于开始推进了，我们有了一个计划，并开始按计划执行
(04:19:08 PM) eyedeekay1: nextloop 和我正在推进把接下来几个重要的 mtn（Monotone）分支镜像到 github
(04:19:27 PM) eyedeekay1: 在各自的 Git 迁移阶段完成之前，这些仍然是只读的，也就是说目前不接受 pull 或合并请求（MRs）
(04:20:04 PM) eyedeekay1: 有关这些阶段的详细描述请见：http://zzz.i2p/topics/2920-flipping-the-switch-on-git#10
(04:20:42 PM) eyedeekay1: 如果我授予 nextloop 在 github 上 i2p 命名空间中创建仓库的权限，并允许他向自己创建的仓库写入，这将对 nextloop 和我都有帮助。
(04:20:47 PM) zzz: 计划写得不错
(04:21:24 PM) eyedeekay1: 谢谢 zzz，很高兴它终于达到了可用状态
(04:22:17 PM) zzz: 它并不完美，但已经“可用”，我们可以据此进行讨论
(04:24:39 PM) eyedeekay1: 接下来我们要迁移的是网站，这很好，因为它相当简单，也没有其他东西依赖它，这应该会在本周进行
(04:25:26 PM) eyedeekay1: 不过关于 nextloop，我想确认，授予他为我们在 github 上创建/写入仓库的权限，是否获得了广泛认可？
(04:25:54 PM) zzz: 好的。等你修改计划/时间表，使其与 0.9.47 发布避免冲突
(04:26:25 PM) eyedeekay1: 收到，我已经在编辑器里打开了 :)
(04:26:48 PM) zzz: 你得去问目前的 github 管理员，他们现在不在，而且我也不在那个组里
(04:27:39 PM) eyedeekay1: 到目前为止，这个提议得到了他们的认可，不过还有一位还没回复。
(04:29:05 PM) zzz: 对我来说没问题，只要你们两位有可靠的沟通方式和备份。我认为我们不需要更多不响应的管理员了 :)
(04:29:53 PM) eyedeekay1: 我觉得我们可以做到
(04:30:06 PM) eyedeekay1: 所以 nextloop 将获得 github 权限
(04:31:40 PM) zzz: 长期不响应但拥有大量权限的人，或许在最坏情况（比如某人突然“被公交车撞”）时能作为一种备份，但这同样是潜在的安全风险，需要加以管理
(04:33:12 PM) eyedeekay1: 嗯
(04:33:20 PM) eyedeekay1: 如果第 3 项还有要在这里处理的事情，那我们现在处理；否则我们大概会在一天内在 zzz.i2p 的帖子里看到修订后的计划。
(04:33:45 PM) zzz: 太好了
(04:34:18 PM) mikalvmeeh: （我半在线，错过了打招呼）
(04:34:56 PM) eyedeekay1: 我们已经完成了计划中的议题，大家还有其他的吗？
(04:36:43 PM) eyedeekay1: 超时 1 分钟
(04:38:51 PM) eyedeekay1: *bafs* 好的，这次会议就到这里。请记住 9 月 1 日，下一次计划会议同一时间，UTC 晚上 8 点
(04:39:12 PM) eyedeekay1: 感谢各位参加 </div>
