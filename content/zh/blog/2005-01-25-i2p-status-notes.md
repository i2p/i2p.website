---
title: "I2P 状态说明（2005-01-25）"
date: 2005-01-25
author: "jr"
description: "每周的 I2P 开发状态说明，涵盖 0.5 版本的 tunnel 路由进展、SAM 的 .NET 移植、GCJ 编译以及关于 UDP 传输的讨论"
categories: ["status"]
---

大家好，简短的每周状态更新

* Index

1) 0.5 状态 2) sam.net 3) gcj 进展 4) udp 5) ???

* 1) 0.5 status

在过去的一周里，0.5 这边取得了不少进展。我们之前讨论的问题已经解决，大幅简化了加密部分，并且消除了 tunnel 循环问题。新的技术[1]已经实现，单元测试也已到位。接下来，我会整合更多代码，把这些 tunnel 集成到主 router 中，然后完善 tunnel 管理和池化基础设施。等这些就绪后，我们会先在仿真环境中跑一遍，最终在一张并行网络上进行烧机测试，最后收尾定版，把它定为 0.5。

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/tunnel-alt.html?rev=HEAD

* 2) sam.net

smeghead 已经完成了一个将 SAM 协议移植到 .net 的新版本 - 兼容 c#、mono/gnu.NET（耶，smeghead！）。它在 cvs 的 i2p/apps/sam/csharp/ 下，并附带 nant 和其他辅助工具 - 现在各位 .net 开发者可以开始用 i2p 折腾了 :)

* 3) gcj progress

smeghead 最近简直势如破竹——截至最新一次统计，经过一些修改，router 已能在最新的 gcj [2] 构建下编译通过（太棒了！）。它还不能正常运行，不过，为了绕开 gcj 在处理某些内部类结构时的困惑而做出的这些修改，无疑是实打实的进步。也许 smeghead 能给我们更新一下进展？

[2] http://gcc.gnu.org/java/

* 4) udp

这里没太多可说的，不过 Nightblade 确实在论坛上提出了一系列有意思的疑虑 [3]，询问我们为何选择使用 UDP。如果你也有类似的担忧，或者对我们该如何解决我在回复中提到的问题有其他建议，欢迎加入讨论！

[3] http://forum.i2p.net/viewtopic.php?t=280

* 5) ???

好吧，好吧，我又把会议记录拖晚了，扣我工资吧 ;) 总之，最近事情很多，所以要么来频道参加会议，要么会后查看发布的日志，或者如果你有话要说，就在邮件列表上发帖。哦，顺便一提，我妥协了，已经在 i2p [4] 里开了个博客。

=jr [4] http://jrandom.dev.i2p/ (密钥在 http://dev.i2p.net/i2p/hosts.txt)
