---
title: "I2P 2006-03-21 状态说明"
date: 2006-03-21
author: "jr"
description: "用于网络统计的 JRobin 集成、biff 和 toopie IRC 机器人，以及新的 GPG 密钥公告"
categories: ["status"]
---

嗨，大家好，又到星期二了

* Index

1) 网络状态 2) jrobin 3) biff 和 toopie 4) 新密钥 5) ???

* 1) Net status

过去一周整体相当稳定，尚未发布新版本。我一直在推进 tunnel 限速和低带宽运行方面的工作；为配合这方面的测试，我已将 JRobin 与 Web 控制台以及我们的统计管理系统集成。

* 2) JRobin

JRobin [1] 是 RRDtool [2] 的纯 Java 移植，它让我们几乎不增加内存开销就能生成漂亮的图表，就像 zzz 一直批量产出的那些一样。我们已将其配置为完全在内存中工作，因此不会产生文件锁争用，更新数据库所需的时间也几乎不可察觉。JRobin 还有许多很不错的功能我们尚未加以利用，不过下一个版本将提供基本功能，并且还会提供一种将数据导出为 RRDtool 可理解格式的方式。

[1] http://www.jrobin.org/ [2] http://people.ee.ethz.ch/~oetiker/webtools/rrdtool/

* 3) biff and toopie

postman 一直在埋头开发一些很有用的机器人，很高兴地告诉大家，可爱的 biff 回来了 [3]，当你在 irc2p 上时，只要你收到（匿名）邮件，它就会提醒你。此外，postman 还为我们开发了一个全新的机器人——toopie——作为 I2P/irc2p 的信息机器人。我们仍在向 toopie 添加常见问题（FAQs），但它很快就会加入常用频道。感谢 postman！

[3] http://hq.postman.i2p/?page_id=15

* 4) new key

对于留意的各位，你们可能已经注意到，我的 GPG 密钥将在几天内到期。我的新密钥 @ http://dev.i2p.net/~jrandom 的指纹是 0209 9706 442E C4A9 91FA  B765 CE08 BC25 33DC 8D49，密钥 ID 为 33DC8D49。此帖由我的旧密钥签名，但接下来一年里的后续帖子（以及发布）将由新密钥签名。

* 5) ???

目前就这些——几分钟后顺道到 #i2p 参加我们的每周会议，打个招呼吧！

=jr
