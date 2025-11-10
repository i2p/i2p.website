---
title: "I2P 开发者会议 - 2017年12月5日"
date: 2017-12-05
author: "zzz"
description: "2017年12月5日的 I2P 开发会议记录。"
categories: ["meeting"]
---

## 快速回顾

<p class="attendees-inline"><strong>出席：</strong> str4d, orignal, zlatinb, zzz</p>

## 会议记录

<div class="irc-log"> 20:00:00 &lt;zzz&gt; 0) 嗨 20:00:00 &lt;zzz&gt; 1) 0.9.33 更新（zzz） 20:00:00 &lt;zzz&gt; 2) 34C3 筹备（zzz） 20:00:03 &lt;zzz&gt; 0) 嗨 20:00:05 &lt;zzz&gt; 嗨 20:00:30 &lt;zzz&gt; 1) 0.9.33 更新（zzz） 20:00:48 &lt;zzz&gt; 0.9.33 的开发已经有了一个强劲的开端，目前已有 20K 行 diff 20:00:55 &lt;zzz&gt; 很多不错的修复 20:01:17 &lt;zlatinb&gt; 嗨 20:01:42 &lt;zzz&gt; 另外，0.9.32 的 Android 版比我们两周的目标更晚，所以我们做了一些流程调整，确保在桌面版发布前先审查 Google Play 的崩溃情况 20:02:01 &lt;i2pr&gt; [Slack/str4d] 嗨 20:02:02 &lt;zzz&gt; 这应该能让 Android 版更早发布且质量更高 20:02:29 &lt;i2pr&gt; [Slack/str4d] 我本地还有更多 CSS 和 JSP 补丁，希望这个周末清理一下并提交到 mtn，方便更长时间的评审。 20:02:40 &lt;zzz&gt; 我认为我们有望在一月下旬发布 0.9.33。这意味着大的改动应在本月、CCC 之前合入 20:03:28 &lt;zzz&gt; 我们还有更多关于 streaming（流式传输）的微调要做，本周我一直在修复 susimail 的问题 20:04:12 &lt;zzz&gt; 关于 1) 还有其他的吗？ 20:04:24 &lt;zlatinb&gt; 如果可以的话，我建议把开发版放到 postman 的 tracker（种子追踪器）上 20:04:35 &lt;zlatinb&gt; 有些人会下载并尝试那上面出现的任何东西 20:04:50 &lt;zzz&gt; 我觉得你可以通过 bobthebuilder.com 上的磁力链接（magnet）或种子文件（torrent）获取它们 20:05:17 &lt;zlatinb&gt; 哦是的，只是出现在 postman 上会带来很高的曝光度 20:05:43 &lt;zzz&gt; 好的，和 bobthebuilder 的 op（管理员）聊聊这件事，主意不错 20:05:54 &lt;zzz&gt; 关于 1) 还有其他的吗？ 20:05:58 &lt;i2pr&gt; [Slack/str4d] 另外，我们现在在 Travis CI 上也有持续构建，所以也可以关注 https://travis-ci.org/i2p/i2p.i2p  以获取另一种视角 20:06:44 &lt;zzz&gt; str4d，如果你能为此设置一个 IRC 机器人，可能会有帮助，人们很难记得去查看一个网站 20:07:17 &lt;zzz&gt; 关于 1) 还有其他的吗？ 20:08:01 &lt;zzz&gt; 2) 34C3 筹备（zzz） 20:08:10 &lt;zzz&gt; 好的，贴纸这件事已经在掌控之中 20:08:25 &lt;zzz&gt; eche|on 拿着火车票 20:08:33 &lt;zzz&gt; hottuna 已经在 wiki 上给我们报名了 20:08:43 &lt;zzz&gt; Noisy Square 已经在 wiki 上出现了吗？ 20:08:50 &lt;zzz&gt; 另外，横幅在谁手里？ 20:09:23 &lt;zzz&gt; 除非有人先做，我稍后会建立 Twitter 的 DM（私信）群组 20:11:01 &lt;zzz&gt; 没有听到回应... 关于 2) 还有其他的吗？ 20:12:01 &lt;zzz&gt; 会议还有其他事项吗？ 20:12:33 &lt;orignal&gt; 也许把会议设得没那么频繁更合适？ 20:12:47 &lt;orignal&gt; 由于兴趣不足 20:12:56 &lt;orignal&gt; 但要加大宣传 20:13:09 &lt;i2pr&gt; [Slack/str4d] 期待！ 20:13:35 &lt;i2pr&gt; [Slack/str4d] 我觉得每月一次差不多合适 20:13:41 &lt;zzz&gt; orignal，也许吧，我们可以在 CCC 讨论。   20:13:47 &lt;i2pr&gt; [Slack/str4d] 这个时间是否合适总是可以讨论的 20:13:56 &lt;zzz&gt; 公关团队也许可以多做些宣传，当然 20:14:10 &lt;orignal&gt; 我会把它固定在发布前一周 20:14:16 &lt;i2pr&gt; [Slack/str4d] zzz，我刚把 IRC 通知的配置推送到了 i2p.i2p 20:14:34 &lt;zzz&gt; 另外，计划说明：我们下一次会议将在 CCC 线下面对面举行。我们在 1 月 2 日不会开会。 20:14:35 &lt;orignal&gt; 至少这样会有个明确的主题 20:14:44 &lt;zzz&gt; 我们的下一次 IRC 会议将在 2 月 6 日（周二）举行 20:15:33 &lt;zzz&gt; 请在 zzz.i2p 上查看有关 CCC 会议主题的帖子 20:15:42 &lt;zzz&gt; 如果有任何建议，请在那里添加 20:15:47 &lt;zzz&gt; 会议还有其他事项吗？ 20:15:52 * zzz 抓起 baffer 20:16:58 &lt;i2pr&gt; [Slack/str4d] 我会在 CCC 之前对提案做更多工作 20:17:11 * zzz *bafs* 宣布会议结束 </div>
