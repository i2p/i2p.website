---
title: "I2P 开发者会议 - 2003年11月11日"
date: 2003-11-11
author: "jrand0m"
description: "I2P 开发会议，涵盖 router 状态、路线图更新、原生 modPow（模幂运算）实现、GUI 安装程序，以及许可协议讨论"
categories: ["meeting"]
---

(由 Wayback Machine 提供 http://www.archive.org/)

## 快速回顾

<p class="attendees-inline"><strong>出席：</strong> dish, dm, jrand0m, MrEcho, nop</p>

(会议记录经过编辑，以掩盖 iip 在会议中途崩溃且出现大量 ping 超时的事实，所以不要把它当作一篇平铺直叙的记录来读)

## 会议记录

<div class="irc-log"> [22:02] &lt;jrand0m&gt; 议程 [22:02] &lt;jrand0m&gt; 0) 欢迎 [22:02] &lt;jrand0m&gt; 1) i2p router [22:02] &lt;jrand0m&gt; 1.1) 状态 [22:02] &lt;jrand0m&gt; 1.2) 路线图变更 [22:02] &lt;jrand0m&gt; 1.3) 待认领的子项目 [22:02] &lt;jrand0m&gt; 2) 本地 modPow [22:03] &lt;jrand0m&gt; 2) GUI 安装程序 [22:03] &lt;jrand0m&gt; 3) IM [22:03] &lt;jrand0m&gt; 4) 命名服务 [22:03] &lt;MrEcho&gt; 我看到了那段 .c 代码 [22:03] &lt;jrand0m&gt; 5) 许可 [22:03] &lt;jrand0m&gt; 6) 其他？ [22:03] &lt;jrand0m&gt; 0) 欢迎 [22:03] &lt;jrand0m&gt; 嗨。 [22:03] &lt;nop&gt; 嗨 [22:03] &lt;jrand0m&gt; 会议 2^6 [22:04] &lt;jrand0m&gt; nop，有要补充到议程里的项目吗？ [22:04] &lt;jrand0m&gt; 好的，1.1) router 状态 [22:04] &lt;jrand0m&gt; 我们是 0.2.0.3，按我上次听到的说法，它是可用的 [22:04] &lt;MrEcho&gt; &gt; 0.2.0.3 [22:04] &lt;MrEcho&gt; 对吧？ [22:05] &lt;MrEcho&gt; 我在跑它……看起来没问题 [22:05] &lt;nop&gt; 不 [22:05] &lt;jrand0m&gt; 0.2.0.3 发布后有一些小的提交，不到出新版本的程度 [22:05] &lt;nop&gt; 我只是想赶上进度 [22:05] &lt;jrand0m&gt; 酷 [22:06] &lt;jrand0m&gt; 鉴于 0.2.0.x 的经验和反馈，我们更新了路线图，让运行时占用更少资源 [22:06] &lt;jrand0m&gt; （也就是让人们能跑 web 服务器/等，而不会吃满他们的 CPU） [22:06] &lt;jrand0m&gt; 具体来说（进入议程 1.2）：http://wiki.invisiblenet.net/iip-wiki?I2PRoadmap [22:06] &lt;MrEcho&gt; 我注意到大多数 router 使用：TransportStyle: PHTTP [22:07] &lt;MrEcho&gt; 它会自动走 phttp，还是会先尝试 tcp？ [22:07] &lt;jrand0m&gt; 嗯，大多数 router 应该支持 PHTTP，如果它们能接受入站连接，也应该支持 TCP [22:07] &lt;jrand0m&gt; 只要可能就会使用 TCP [22:07] &lt;jrand0m&gt; PHTTP 的权重成本大约比 TCP 高 1000 倍 [22:08] &lt;jrand0m&gt; （参见 GetBidsJob，它会询问每个传输认为向某个对等体发送消息的代价） [22:08] &lt;jrand0m&gt; （另见 TCPTransport.getBid 和 PHTTPTransport.getBid 所用到的数值） [22:08] &lt;MrEcho&gt; 好 [22:08] &lt;jrand0m&gt; 你经常用 PHTTP 来收发消息吗？ [22:09] &lt;jrand0m&gt; （那可能表明你的 TCP 监听器不可达） [22:09] &lt;MrEcho&gt; 我这边没有填那些 URL [22:09] &lt;jrand0m&gt; 啊，OK。 [22:09] &lt;MrEcho&gt; 哦，是的 [22:10] &lt;jrand0m&gt; 好的，嗯，我的 router 和你之间有打开的 TCP 连接 [22:10] &lt;dm&gt; 它们真是热情好客啊。 [22:10] * jrand0m 很高兴你们让我实现了 routerConsole.html，这样我们就不必为了这些破事儿去翻日志了 [22:11] &lt;MrEcho&gt; 如果连不上 tcp 会转到 phttp 吗？有超时吗？时间是多长？ [22:11] &lt;jrand0m&gt; 总之，路线图的重大变化是 0.2.1 会实现 AES+SessionTag 相关的内容 [22:11] &lt;MrEcho&gt; 或者我们能把那个做成一个设置吗？ [22:11] &lt;jrand0m&gt; 如果遇到 TCP 连接被拒绝/找不到主机/等情况，它会立即放弃该次尝试，然后尝试下一个可用的 bid [22:12] &lt;MrEcho&gt; 所以不会重试 [22:12] &lt;jrand0m&gt; phttp 的超时是 30 秒，如果我没记错的话 [22:12] &lt;jrand0m&gt; 没必要重试。要么你有一个已建立的 TCP 连接可以发送数据，要么没有 :) [22:12] &lt;MrEcho&gt; lol 好的 [22:13] &lt;MrEcho&gt; 之后它每次还会尝试 tcp，还是会跳过直接用 phttp 建下一个连接？ [22:13] &lt;jrand0m&gt; 目前它每次都会尝试 tcp。 [22:13] &lt;jrand0m&gt; 传输层还不会保存历史 [22:13] &lt;MrEcho&gt; 好的，酷 [22:14] &lt;jrand0m&gt; （不过如果一个对等体失败 4 次，它会被拉黑 8 分钟） [22:14] &lt;MrEcho&gt; 那么对方收到 phttp 消息后，应该会通过 tcp 连接到发送该消息的 router，对吧？ [22:14] &lt;jrand0m&gt; 对。一旦建立了任何 tcp 连接，它就可以用它。 [22:14] &lt;jrand0m&gt; （但如果双方都只有 phttp，显然只能用 phttp） [22:15] &lt;MrEcho&gt; 那就意味着它无法和任何东西建立 tcp 连接 [22:15] &lt;MrEcho&gt; ……不过是的 [22:16] &lt;MrEcho&gt; 真希望有办法绕过这个 [22:16] &lt;jrand0m&gt; 不，我的 router 里有一个没有 TCP 地址——只有 PHTTP。但我会与有 TCP 地址的对等体建立 TCP 连接。 [22:16] &lt;jrand0m&gt; （然后他们就可以沿着那个 TCP 连接回发消息，而不是给我发送更慢的 PHTTP 消息） [22:17] &lt;jrand0m&gt; 还是你不是这个意思？ [22:17] &lt;MrEcho&gt; 是的，我搞混了 [22:17] &lt;jrand0m&gt; 行，没问题 [22:18] &lt;jrand0m&gt; 所以，关于更新后的时间安排请看更新过的路线图 ((Link: http://wiki.invisiblenet.net/iip-wiki?I2PRoadmap)http://wiki.invisiblenet.net/iip-wiki?I2PRoadmap) [22:18] &lt;jrand0m&gt; 好的，1.3) 待认领的子项目 [22:19] &lt;jrand0m&gt; 我终于把我 palmpilot 上的一堆待办列表放进了 wiki，在 (Link: http://wiki.invisiblenet.net/iip-wiki?OpenSubprojects)http://wiki.invisiblenet.net/iip-wiki?OpenSubprojects [22:19] &lt;jrand0m&gt; 所以如果你无聊正想找点代码项目做…… :) [22:19] &lt;MrEcho&gt; 真是的 [22:20] &lt;MrEcho&gt; 我已经有 2 个了 [22:20] &lt;dish&gt; 你还有个 palmpilot，太精英了 [22:20] &lt;MrEcho&gt; 我的挂了 [22:20] &lt;jrand0m&gt; mihi&gt; 里面有一条关于 I2PTunnel 的条目，描述了我不久前的一个想法 [22:20] &lt;MrEcho&gt; 不知道它怎么了 [22:21] &lt;jrand0m&gt; 是啊，我以前用过 palm，最近有人为这项事业捐了一个给我 ;) [22:21] &lt;dish&gt; 会议上能不能加一条议程，讨论 userX 上次发话是什么时候 [22:21] &lt;MrEcho&gt; 该死的玩意儿现在连电都开不了 [22:21] &lt;MrEcho&gt; lol [22:22] &lt;jrand0m&gt; 我觉得 UserX 有四五个月没说过话了 ;) [22:22] &lt;MrEcho&gt; 那是个机器人之类的吗？ [22:22] &lt;dish&gt; 他们 5 个月前说了什么？ [22:22] &lt;MrEcho&gt; 我敢打赌那是在他曾经能访问的一台机器上跑着的 BitchX……然后他忘了它 [22:22] &lt;jrand0m&gt; 他说他下周会回来说说对 anonCommFramework（i2p 的旧名字）的看法 ;) [22:23] &lt;dish&gt; 哈哈 [22:23] &lt;jrand0m&gt; 不过我想他是忙了。生活就是这样 [22:23] &lt;jrand0m&gt; 好的，2) 本地 modPow [22:23] &lt;MrEcho&gt; 我看到了那段 c 代码 [22:24] &lt;jrand0m&gt; 我拼了个 .c 桩代码和一个 Java 类，用来演示如何集成像 GMP 或其他 MPI 库，不过显然它现在还不能用 [22:25] &lt;jrand0m&gt; 如果能有一个小型的 C 类集合和相应的简单 Java 包装类，我们就可以为 windows、osx、*bsd、linux 构建，并以 GPL 方式打包，那就太好了</div>

(在此插入重大 iip 故障)

[22:38] &lt;MrEcho&gt; 我最后看到的是：[13:25] &lt;jrand0m&gt; 好的，2）原生 modPow
[22:38] &lt;jrand0m&gt; 嗨 MrEcho
[22:38] &lt;jrand0m&gt; 嗯，看起来一个主代理崩了
[22:39] &lt;jrand0m&gt; 我再等 2 分钟再重启
[22:39] &lt;MrEcho&gt; 好
[22:39] &lt;MrEcho&gt; 25 美元一次性，我可以在 thenidus.net 上拿到完整的 Java 支持……那是我其中一个站点
[22:40] &lt;jrand0m&gt; 25 美元？他们收你安装软件的钱？
[22:40] &lt;MrEcho&gt; 不太清楚……这是个套餐
[22:40] &lt;MrEcho&gt; 正在和我朋友聊
[22:40] &lt;jrand0m&gt; 不过我不确定代码已经稳定到可以出去租一堆托管点来架设 routers。还没到那步 :)
[22:41] &lt;dm&gt; 什么的套餐？
[22:41] &lt;MrEcho&gt; java - jsp
[22:41] &lt;jrand0m&gt; 好，我把之前发的再发一遍：
[22:41] &lt;jrand0m&gt; 我拼了个桩（stub）.c 和 Java 类，演示如何集成像 GMP 或其他 MPI 库，但显然还不能工作
[22:41] &lt;jrand0m&gt; 比较理想的是，我们有一小包 C 类以及一个很简单的 Java 包装类，可以为 Windows、OSX、*BSD、Linux 构建，并用 GPL（或更宽松的许可证）打包发布
[22:41] &lt;jrand0m&gt; 不过随着新路线图把 AES+SessionTag 作为我当前的行动项，这件事没以前那么紧迫了。
[22:42] &lt;jrand0m&gt; 不过如果有人愿意接手，那就太好了（而且我敢肯定我们都熟悉的另一个项目也会对这种打包感兴趣）
[22:43] &lt;dm&gt; frazaa?
[22:43] &lt;jrand0m&gt; 呵，某种意义上是 ;)
[22:44] &lt;jrand0m&gt; 好，3）图形界面安装程序
[22:44] &lt;jrand0m&gt; MrEcho&gt; 嗨
[22:44] &lt;MrEcho&gt; :)
[22:44] &lt;MrEcho&gt; 呵呵
[22:44] &lt;MrEcho&gt; 进展顺利
[22:44] &lt;jrand0m&gt; 酷
[22:44] &lt;MrEcho&gt; 没啥花哨的
[22:45] &lt;MrEcho&gt; 我有些很酷的点子能把它做得很炫……不过还早
[22:45] &lt;jrand0m&gt; 我在想安装程序是否应该加入：1）一个选项，从 http://.../i2pdb/ 自动获取种子；2）自动获取 http://.../i2p/squid.dest 并顺便创建一个 runSquid.bat/runSquid.sh？
[22:45] &lt;jrand0m&gt; 好
[22:46] &lt;jrand0m&gt; 对，我们希望安装程序尽可能简单——你说的那些花哨东西是啥？
[22:46] &lt;MrEcho&gt; 问题是……当你执行 java -jar installer 时，因为你目前的设置，它默认走非 GUI 模式
[22:46] &lt;MrEcho&gt; 我们要怎么做到双击 jar 文件就能启动 GUI
[22:47] &lt;jrand0m&gt; install.jar &lt;-- 非 GUI， installgui.jar &lt;-- GUI
[22:47] &lt;jrand0m&gt; 代码分开，包也分开
[22:47] &lt;MrEcho&gt; 花哨指的是那些你可能注意不到的细节……但整体会很干净利落
[22:47] &lt;jrand0m&gt; 酷
[22:47] &lt;MrEcho&gt; 哦，好的
[22:48] &lt;jrand0m&gt; （或者 install &lt;-- GUI，installcli &lt;-- CLI。再看进展吧）
[22:49] &lt;jrand0m&gt; 关于 GUI 还有别的么，还是我们跳到第 4 项？
[22:49] &lt;jrand0m&gt; （你心里有没有时间表？不催，就问问）
[22:51] &lt;MrEcho&gt; 现在还没想好
[22:51] &lt;jrand0m&gt; 好嘞
[22:51] &lt;jrand0m&gt; 好，4）IM
[22:51] &lt;jrand0m&gt; thecrypto 不在，所以……
[22:51] &lt;jrand0m&gt; 5）命名服务
[22:51] &lt;jrand0m&gt; wiht 也不在……
[22:51] &lt;jrand0m&gt; ping
[22:52] &lt;dish&gt; 你的议程编号搞错了
[22:52] &lt;dish&gt; 3）IM
[22:52] &lt;jrand0m&gt; 对，我前面把“第 2 项”列了两次
[22:52] &lt;dish&gt; 4）命名
[22:52] &lt;dish&gt; ;)
[22:52] &lt;jrand0m&gt; （原生 modPow 和 GUI 安装程序）
[22:52] &lt;jrand0m&gt; 瞧，我们很“动态”之类的
[22:59] &lt;jrand0m&gt; 好，为了日志我想我继续吧
[22:59] &lt;jrand0m&gt; 6）许可协议
[23:00] &lt;jrand0m&gt; 我在考虑用比 GPL 限制更少的许可。我们用了一些 MIT 代码，另外有一个文件是 GPL（不过那只是 base64 编码，替换很容易）。除此之外，所有代码要么归我，要么归 thecrypto 版权所有。
[23:00] * dish 查看 mihi 的 I2P tunnel 相关代码部分
[23:01] &lt;jrand0m&gt; 哦对，mihi 已经按 GPL 发布了，但如果他愿意，他也可以换成别的许可来发布
[23:01] &lt;jrand0m&gt; （不过 i2ptunnel 本质上是第三方应用，可以按它想要的方式选择许可）
[23:02] &lt;jrand0m&gt; （不过由于 i2p SDK 是 GPL，他被迫也得用 GPL）
[23:02] &lt;MrEcho&gt; 终于该到了
[23:02] &lt;jrand0m&gt; 我也不太清楚。许可协议不是我的强项，但我至少倾向于转到 LGPL
[23:02] * dish 把对 I2P HTTP Client 的 10–20 行修改按 mihi 的许可来发布
[23:03] &lt;jrand0m&gt; 呵呵 :)
[23:06] &lt;jrand0m&gt; 总之，7）其他？
[23:07] &lt;jrand0m&gt; 关于 i2p 有任何问题/顾虑/想法吗？
[23:07] &lt;dish&gt; 我问一个
[23:07] &lt;dish&gt; I2P 有没有“组名”功能？
[23:07] &lt;jrand0m&gt; 组名功能？
[23:07] &lt;dm&gt; 探索频道小队！
[23:07] &lt;MrEcho&gt; 哈哈
[23:08] &lt;dish&gt; 比如你想要一个私有或独立的网络，但如果有些 router 不小心混在一起，没有组名的话，这两个网络就会合并
[23:08] &lt;MrEcho&gt; 他想到的是 waste
[23:08] &lt;jrand0m&gt; 啊
[23:08] &lt;dish&gt; 我不确定你们会不会要这个，我只是随便问问以防万一
[23:09] &lt;jrand0m&gt; 会的，早期做网络设计时我考虑过这个
[23:09] &lt;jrand0m&gt; 这比我们现在（或者相对不远的将来 [6-12 个月]）需要的要高级，但以后可能会整合进来
[23:09] &lt;dish&gt; 或者这是个坏主意，因为把它保持为一个大型网络更好？
[23:09] &lt;dm&gt; i2pisdead
[23:09] &lt;jrand0m&gt; 呵 dm
[23:10] &lt;nop&gt; 闭嘴
[23:10] &lt;jrand0m&gt; 不，dish，这是个好主意
[23:10] &lt;dm&gt; nop：硬汉？
[23:10] &lt;jrand0m&gt; 这本质上就是 0.2.3 版要做的——受限路由
[23:10] &lt;jrand0m&gt; （也就是你有一小组私有（受信任）的对等体，不想让所有人知道他们是谁，但仍希望能与之通信）
[23:15] &lt;jrand0m&gt; 好，还有别的吗？
[23:15] &lt;nop&gt; 没有，我只是逗你们玩
[23:18] &lt;dm&gt; 搞笑的人？
[23:20] &lt;jrand0m&gt; 好吧，嗯，/挺有意思/ 的会议，中间还夹了几次 iip 崩溃 ;)
[23:21] * jrand0m 把会议 *baf* 地结束了 </div>
