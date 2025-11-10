---
title: "I2P 开发者会议"
date: 2003-07-15
author: "nop"
description: "I2P 开发会议，涵盖项目更新和技术讨论"
categories: ["meeting"]
---

(由 Wayback Machine 提供 http://www.archive.org/)

## 快速回顾

<p class="attendees-inline"><strong>出席：</strong> gott, hezekiah, jeremiah, jrand0m, mihi, Neo, nop, WinBear</p>

## 会议记录

<div class="irc-log"> --- 日志开启 Tue Jul 15 17:46:47 2003
17:46 < gott> 嗨。
17:46 <@nop> 先说一声，我刚才一直沉默。
17:46 <@hezekiah> Tue Jul 15 21:46:49 UTC 2003
17:47 <@hezekiah> 好的。iip-dev 会议开始了。
17:47 <@hezekiah> 这是第 48 次还是第 49 次？
17:47 < jrand0m> nop> 这就是为什么我们必须尽快把 router 	架构确定下来。我理解大家的推进速度不同，我们必须分段，这样不同组件可以 	各自推进
17:47 < mihi> 第 49 次
17:47 <@hezekiah> 好的！欢迎参加第 49 次 iip-dev 会议！
17:47 < jrand0m> 我在工作岗位上还有三天，之后每周将投入 90+ 小时 / 	来把这事跑起来
17:48 < jrand0m> 我知道，也不指望每个人都能做到，这也是我们需要	进行分工的原因
17:48 < jrand0m> 嗨 hezekiah :)
17:48 <@hezekiah> lol
17:48 <@nop> 反驳一下
17:48 <@hezekiah> 我等一分钟，然后我们可以走议程。 :)
17:48 <@nop> router 架构的安全性也取决于你 	不要操之过急
17:49 <@nop> 如果我们这么做
17:49 <@nop> 我们会疏忽
17:49 <@nop> 到时候可能得收拾一大堆烂摊子
17:49 -!- Rain [Rain@anon.iip] 已退出 [I Quit]
17:49 < jrand0m> nop> 不同意。 即使不实现 router（或甚至不知道网络将如何运作），我们仍然可以构建应用层和 API
17:49 <@nop> 这点我同意
17:50 <@nop> 我说的是底层网络
17:50 < jrand0m> 如果我们能就我发出的 API 达成一致，那就是我们所需的 	分工边界
17:50 < jrand0m> 对，router 实现和网络设计还没完成
17:50 <@nop> 好
17:50 <@nop> 哦，目前为止我肯定同意你的 API
17:51 <@hezekiah> jrand0m：有个问题。
17:51 < jrand0m> 说吧 hezekiah
17:51 <@hezekiah> 如果用 C 实现，会不一样。
17:51 < jrand0m> 不会差太多
17:51 < gott> 天哪
17:51 < jrand0m> 大写字母会更少，把对象换成 struct 就行
17:51 < gott> 大家考虑用哪些语言来实现？
17:51 < jrand0m> （针对 API）
17:51 <@hezekiah> 呃，jrand0m？C 里没有 'byte[]'。
17:51 < jrand0m> gott> 去看邮件归档，有一些示例答案
17:52 <@hezekiah> 你很可能会用 void* 加一个整数来指定 	长度。
17:52 < jrand0m> hezekiah> 那就用 unsigned int[]
17:52 < gott> jrand0m：难得有一场我不参与的“圣战”
17:52 <@hezekiah> 如果我没记错（nop 帮我确认一下），你不能 	让函数直接返回一个 unsigned int[]。
17:53 <@hezekiah> gott：不然呢？伪代码？
17:53 < jrand0m> 对，都是语法层面的变化。但是没错，如果有实质性差异，我们得尽快解决。（比如，今天）也许 	现在可以看看我发的题为 "high level 	router architecture and API" 的邮件，评审一下？
17:54 <@hezekiah> nop？UserX？愿意来做这个吗？
17:54 < jrand0m> 差异不大，但毕竟还是不同，是的。这就是为什么我在今天的邮件里说的是 Java API :)
17:54 -!- WinBear [WinBear@anon.iip] 加入了 #iip-dev
17:55 <@nop> 等下
17:55 <@nop> 正在往上看
17:55 -!- mihi_2 [~none@anon.iip] 加入了 #iip-dev
17:55 -!- mihi 现在叫做 nickthief60234
17:55 -!- mihi_2 现在叫做 mihi
17:55 < jrand0m> 欢迎回来 mihi
17:55 < gott> 顺便问下，这会儿是否在实时记录日志？
17:55 -!- nickthief60234 [~none@anon.iip] 已退出 [EOF From client]
17:55 <@hezekiah> gott：是的。
17:55 < mihi> 冗余为王 ;)
17:55 < gott> 那我待会儿再读。
17:55 -!- gott [~gott@anon.iip] 离开了 #iip-dev [gott]
17:56 <@nop> 好
17:56 <@nop> 是的
17:56 < WinBear> jrand0m：嗨
17:56 <@nop> 的确有差异
17:56 <@nop> 我们需要的是
17:56 < jrand0m> 嗨呀 WinBear
17:56 <@nop> 由一些特定的开发者组队，为这些语言编写主要的 API 层控制
17:56 <@nop> 我们知道 jrand0m 能搞定 Java
17:56 <@nop> 也很可能能和 thecrypto 搭档
17:56 <@nop> hezekiah 他们这帮可以做 C
17:56 <@nop> 如果 jeremiah 愿意的话
17:56 <@nop> 可以做 Python
17:56 <@hezekiah> 我也会 C++！ ;-)
17:56 <@nop> 好
17:56 <@nop> 也做 C++
17:57 <@hezekiah> lol
17:57 <@nop> C++ 可能也行
17:57 <@nop> 和 C 一起
17:57 <@nop> 只要你别把模板玩得太过分
17:57 < jrand0m> 呵
17:57 <@hezekiah> lol
17:57 <@hezekiah> 事实上，MSVC 能把 C 和 C++ 的目标文件链接在一起，	gcc 似乎不太喜欢这么干。
17:57 <@nop> 也就是说，坚持用与 C 兼容的 struct，或者这行不通？
17:57 < jrand0m> 在此之前的第一个问题是：哪些应用会用 	这些 API？我知道有些应用会想用 Java，iproxy 会用 C 吗？
17:58 <@hezekiah> nop：我认为 C 和 C++ 在对象层面并不兼容。
17:58 <@nop> 好
17:58 <@hezekiah> nop：C++ 跟 C 的相处并不会比 Java 更好多少。
17:58 <@nop> 那也许 USerX 可以做 C
17:58 <@nop> 而你可以负责 C++
17:58 <@hezekiah> We don
17:58 <@nop> ?
17:58 <@hezekiah> 如果你不想的话，甚至	都不需要“用”C++。只是我更倾向于它而已。
17:59 <@nop> 嗯，问题在于
17:59 <@nop> 有很多 C++ 开发者
17:59 <@nop> 尤其是在微软生态里
17:59 <@hezekiah> 即便在 Linux 世界也是。（见：KDE 和 Qt。）
17:59 < jrand0m> 如果只是做 .so 或 .a，C 和 C++ 在二进制层面是兼容的
17:59 < jrand0m> （btw）
18:00 <@nop> C 能不能作为 C++ 的好替代？也就是，C++ 开发者处理一个 C API 会不会比让一个 C 开发者处理 C++ API 更容易？
18:00 <@hezekiah> jrand0m：是的。你大概可以有库……但如果 	你能
18:00 <@hezekiah> jrand0m：连类都不能用的话，这就有点本末倒置了。
18:00 <@nop> 对
18:00 <@nop> 那就坚持用 C
18:01 <@nop> 因为 C++ 程序员仍然可以很容易地调用 C 库
18:01 <@hezekiah> 如果一个模块需要调用另一个的函数，最好它们 	用同一种语言。
18:01 <@hezekiah> nop：C++ 程序员通常对 C 也很熟……不过如果他们从来没/学过/ C，可能要花点功夫。
18:02 <@hezekiah> 不过，C 程序员不一定会 C++，因为 C 只是 	C++ 的子集。
18:02 -!- logger_ [~logger@anon.iip] 加入了 #iip-dev
18:02 -!- #iip-dev 主题：会议结束后日志文件会在线提供：	http://wiki.invisiblenet.net/?Meetings
18:02 [Users #iip-dev]
18:02 [@hezekiah] [+Ehud    ] [ leenookx] [ moltar] [ tek    ]
18:02 [@nop     ] [ jeremiah] [ logger_ ] [ Neo   ] [ WinBear]
18:02 [@UserX   ] [ jrand0m ] [ mihi    ] [ ptsc  ]
18:02 -!- Irssi：#iip-dev：共 14 个昵称 [3 个管理员, 0 个半管, 1 个有发言权, 10 个普通]
18:02 < jrand0m> 对
18:02 -!- Irssi：加入 #iip-dev 的同步在 9 秒内完成
18:02 < jrand0m> （with JMS :)）
18:03 -!- 你现在叫做 logger
18:03 < jrand0m> 好，我们能不能先评审一下总体架构，看看 	这些 API 是否真的相关？
18:03 <@nop> 行  
18:04 < jrand0m> :)
18:04 < jrand0m> 好，看看我发的带有 routerArchitecture.png。 	对那样的分层有何看法？
18:04 -!- tek [~tek@anon.iip] 已退出 []
18:05 < WinBear> jrand0m：那在 wiki 上吗？
18:05 < jrand0m> WinBear> 不，在邮件列表上，不过归档 	挂了。让我把它加到 wikki 上
18:06 <@hezekiah> 如果我错了请纠正我……
18:07 <@hezekiah> ……看起来我们会有 3 套彼此尽可能相似的 API。
18:07 <@hezekiah> 对吗？
18:07 < jrand0m> 是的 hezekiah
18:07 <@hezekiah> 那么既然每个 API 用的是不同的语言，它们 	都会各自有独立实现吗？
18:07 < jrand0m> 是的
18:07 <@hezekiah> 还是说 Java 或 Python 能访问一个 C 库？
18:08 < jrand0m> 能，但我们不想走那条路
18:08 < mihi> 对于 Java：JNI
18:08 <@hezekiah> 那么关于 Java、C、C++、Python 等一起 	工作的讨论就没意义了，因为它们根本不会一起工作？
18:08 < jrand0m> 我怎么往 wiki 里附图？
18:08 <@hezekiah> 每个 API 都有一个用对应语言写的后端。
18:08 < jrand0m> 不，hezekiah，看图
18:09 <@hezekiah> 哦，懂了！
18:09 <@hezekiah> 这些 API 并不链接到一个后端。
18:10 <@hezekiah> 它们通过套接字通信。
18:10 < jrand0m> si sr
18:10 <@hezekiah> 但这还是有点让人困惑。
18:10 <@hezekiah> 给我一点时间。 :)
18:11 <@hezekiah> 好。标着‘transport’的那一块是什么？
18:11 < jrand0m> 比如，双向 HTTP 传输、SMTP 传输、 	普通套接字传输、轮询式 HTTP 套接字，等等
18:11 < jrand0m> 在 router 之间搬运字节的东西
18:12 <@hezekiah> 好的。
18:12 <@hezekiah> 那我看到的图是某个人的电脑。
18:12 <@hezekiah> 他有一个 router，通过传输模块 	与他人的电脑通信。
18:12 < jrand0m> 没错
18:12 <@hezekiah> 甲方（Alice）在跑两个应用。
18:12 <@hezekiah> 一个用 C 写，另一个用 Java 写。
18:13 <@hezekiah> 两个都链接到一个库（也就是 API）。
18:13 < jrand0m> 两个都“链接”到各自的库（这些 API）
18:13 <@nop> 概念很简单
18:13 <@nop> 是的
18:13 <@hezekiah> 这些库从程序接收输入，加密，	然后通过套接字（UNIX 或 TCP）发送给 router……而 router 是 Alice 运行的另一个程序。
18:13 < jrand0m> 对
18:14 <@hezekiah> 好的。这有点像把 isproxy 拆成两部分。
18:14 < jrand0m> 猜对了 :)
18:14 <@hezekiah> 一部分是底层，用 C 写；另一部分是 	高层，用什么都行。
18:14 < jrand0m> 正是如此
18:14 <@hezekiah> 好的，我明白了。 :)
18:14 < jrand0m> w00t
18:14 <@hezekiah> 所以各语言之间并不需要彼此兼容。
18:14 < jrand0m> WinBear> 抱歉，我没法把它丢到 wiki 上，因为它只 	接受文本 :/
18:15 <@hezekiah> 既然它们都通过套接字和 router 通信， 	那按设计来说你完全可以用 PASCAL 写一个 API。
18:15 <@nop> 是的
18:15 <@nop> 任意的
18:15 < jrand0m> 对
18:15 <@nop> 它能处理任意套接字
18:15 < jrand0m> 不过有些东西需要标准化（比如 Destination（I2P 的目的地标识）、Lease 等这些数据结构）
18:15 < WinBear> jrand0m：根据 hezekiah 的描述我大概理解了
18:15 < jrand0m> 好说
18:16 <@hezekiah> jrand0m：对。通过套接字传输的字节结构和顺序，会在某个设计文档里规定
18:16 <@hezekiah> 在某处。
18:17 <@hezekiah> 但你依然可以用任何你喜欢的方式来实现那些字节的发送与 	接收。
18:17 <@nop> WinBear：这和 irc 客户端通过 isproxy 	工作的方式完全一样
18:17 < jrand0m> 没错
18:17 <@hezekiah> 好。
18:17 <@hezekiah> 我现在明白了。 :)
18:17 -!- moltar [~me@anon.iip] 离开了 #iip-dev [moltar]
18:17 <@nop> 嗯
18:17 <@nop> 也不完全是
18:17 <@hezekiah> 呃哦。
18:17 <@nop> 但想象一下它是怎么工作的
18:17 <@nop> 你就能理解“任意套接字”
18:17 <@nop> isproxy 只是路由
18:17 <@nop> 并转发
18:18 <@nop> 现在，jrand0m
18:18 <@nop> 快问一个
18:18 < jrand0m> si sr?
18:18 <@nop> 这个 API 只为新写、面向这个网络运行的应用而设计吗
18:18 -!- hezekiah 为 #iip-dev 设定模式 [+v logger]
18:18 < WinBear> nop：是用高层替换 irc 客户端吗？
18:18 < jrand0m> nop> 是的。 不过一个 SOCKS5 代理也可以用这个 API
18:18 <@nop> 或者能不能有个中间件，让已有 	标准客户端可用
18:18 <@nop> 比如
18:19 <@nop> 这样我们只需要写中间件 -> api
18:19 < jrand0m> （但注意没有 'lookup' 服务—— 	这个网络没有 DNS）
18:19 < jrand0m> 对
18:19 <@nop> 这样我们就能支持比如 Mozilla 等
18:19 <@nop> 他们只需写插件
18:19 < jrand0m> nop> 对
18:19 <@nop> 好
18:19 <@nop> 或者写传输层模块 :)
18:20 < jrand0m> （例如，让 SOCKS5 把 HTTP 外部代理硬编码到 	destination1、destination2 和 destination3）
18:20 <@nop> 好
18:20 < WinBear> 我想我懂了
18:21 < jrand0m> w00t
18:21 < jrand0m> 好，这个设计里我必须考虑的一点 	是把私钥保留在应用的内存空间里——router 永远 	不会拿到 destination 的私钥。
18:21 <@hezekiah> 所以应用只需把原始数据交给 API， 	就能通过 I2P 网络发送，其他事情不用担心。
18:22 <@hezekiah> 对吗？
18:22 < jrand0m> 这意味着 API 需要实现端到端那部分 	加密
18:22 < jrand0m> 没错 hezekiah
18:22 <@hezekiah> 好的。
18:22 <@nop> 是
18:22 <@nop> 这就是思路
18:22 <@nop> 它会替你处理好
18:22 <@nop> 你只需调用钩子
18:23 <@hezekiah> 一个快问：
18:23 <@hezekiah> 这个‘router’显然需要在它的传输层之上 	说某种协议。
18:23 < jrand0m> 对
18:23 <@hezekiah> 那就可以提供多个 router 的实现 	……
18:23 < jrand0m> 是的
18:24 <@hezekiah> ……只要它们都说同一种协议。
18:24 < jrand0m> （这也是为什么规范里为位桶（bit bucket）预留了占位）
18:24 < jrand0m> 对
18:24 <@hezekiah> 所以可以有一个用 Java 写的 router，一个用 	C 写的，还有一个用 PASCAL 写的。
18:24  * jrand0m 皱眉
18:24 < jrand0m> 但可以
18:24 <@hezekiah> 它们都能互通，因为它们通过 	TCP/IP 使用相同的协议通信。
18:24  * WinBear 一惊
18:24 <@hezekiah> jrand0m：是啊。我对自己的 PASCAL 岁月也没什么美好回忆。
18:25 < jrand0m> 嗯，比如 Pascal 可以通过 TCP 传输和 C 的那个通信， 	而 C 的那个又可以通过 HTTP 传输和 Java 的那个通信
18:25 <@hezekiah> 对。
18:25 < jrand0m> （传输只和同类传输对话，router 管理 	它们之间传递的消息，但不处理消息如何被传递）
18:26 <@hezekiah> 我想表达的是：协议相同，因此某人的 router 用什么语言实现并不重要。
18:26 < jrand0m> 对
18:26 <@hezekiah> 酷。
18:26 < jrand0m> 现在你明白为什么我对所有 C vs 	Java 等争论都说“无所谓”了吧？  :)
18:26 <@hezekiah> 嗯哼。
18:26 <@hezekiah> lol
18:27 <@hezekiah> 我得夸夸你，jrand0m。这会让开发者为这个网络写程序 	变得非常友好。
18:27 < jrand0m> 呵，其实这个 API 也不算原创。这就是 	面向消息的中间件（MOM）的工作方式
18:27 <@hezekiah> 你甚至可以做针对某些平台特性的专用 router（比如 64 位 CPU）。
18:28 < jrand0m> 绝对可以
18:28 <@hezekiah> jrand0m：还很谦虚呢！ ;-)
18:28 <@hezekiah> 嗯，在我看来不错。
18:28 < jrand0m> 好，UserX、nop，这样的分离合理吗？
18:28 <@nop> 当然
18:28 <@nop> userx 还在吗
18:29 <@hezekiah> 他已经闲置了 1:26。
18:29 < jrand0m> 好。那么我们有两个任务：设计网络， 	以及设计 API 的工作方式。
18:29 <@nop> 对
18:29 <@hezekiah> 一个简单问题：API 负责端到端加密。那么 	router 是否做节点到节点的加密？
18:29 <@nop> 是的
18:30 < jrand0m> 是
18:30 < jrand0m> （传输层）
18:30 <@hezekiah> 很好。 :)
18:30 <@nop> hezekiah：这和我们目前已有的非常相似
18:30 <@nop> 在这方面
18:31 < jrand0m> 好……呃，糟糕，thecrypto 不在，没法对 	性能模型提意见。
18:31 < Neo> 对于偏执党，应用也可以在进入 API 之前先做 PGP 加密 ;)
18:31 < jrand0m> 完全可以，neo
18:31 < jrand0m> 我甚至想过把端到端加密从 	API 里拿掉，交给应用自己做……
18:31 <@hezekiah> jrand0m：那就太残忍了。
18:31 < jrand0m> 呵呵
18:32 <@hezekiah> 顺便说，API 和 router 通过套接字通信。
18:32 <@hezekiah> 在 UNIX 上会用 UNIX sockets 还是本地 TCP/IP 	套接字？
18:32 < jrand0m> 大概为了简单起见就用本地 tcp/ip 吧
18:32 <@nop> 稍等
18:32 <@hezekiah> （我想你可以做一个同时接受两种的 router。）
18:33  * hezekiah 真挺喜欢这种可互换部件的设置
18:33 <@nop> 你稍等一下
18:34 <@hezekiah> 正在等…… :)
18:34 <@nop> 我打电话到 thecrypto 家里
18:34 <@nop> 看他能不能上来
18:34 < jrand0m> 呵呵，说得好
18:34 <@hezekiah> lol
18:34  * hezekiah 换上一口浓重的意大利口音
18:34 <@hezekiah> Nop ha' got ... CONNECTIONS!
18:34 < jeremiah> lo
18:34 <@nop> 嘿 jeremiah
18:35 < jrand0m> 嗨呀 jeremiah
18:35 <@nop> 你愿意在 API 层帮忙做一个 Python API 吗
18:35 < jeremiah> 当然
18:35  * jeremiah 回看之前的记录
18:35 < jrand0m> 呵，说得好
18:35  * nop 正在打电话
18:36 <@nop> 他不在家
18:36 <@nop> 他一小时后回来
18:36 < jrand0m> 好，还有谁看了那个 .xls，或对 	这个模型有意见？
18:37 <@hezekiah> 我看了那个 .xls……但我对 p2p 了解不多， 	所以大部分没看懂。
18:37 <@hezekiah> UserX 擅长这块。
18:37 <@nop> 我还得去读
18:37 < jrand0m> （btw，morphmix 给出的数字很夸张……他们说 	随机主机的平均 ping 时间在 20-150ms， 	而不是我预期的 3-500）
18:37 < jrand0m> 酷
18:37 <@nop> 是 staroffice 还是 openoffice？
18:37 < jrand0m> openoffice，但我导出了 .xls
18:37 <@nop> 哪个是 excell？
18:37 < jrand0m> 对
18:38 <@hezekiah> 顺便说一下，关于 API……
18:38 < jrand0m> si sr?
18:38 <@hezekiah> ……在 C 里，boolean 会是 int。
18:38 <@nop> 哪封邮件
18:38 <@nop> hezekiah：是的
18:38 <@hezekiah> 类会以结构体指针的形式传递。
18:38 <@nop> 除非你 typedef boolean
18:39 <@hezekiah> 而使用 byte[] 的函数会用 void*，并加一个额外参数来指定 	缓冲区长度。
18:39 <@nop> hezekiah：你太挑剔了 :)
18:39 < jrand0m> nop> 我现在访问不了归档，所以不确定 	主题行是什么，但它是上周发的……
18:39 <@nop> 留到会后再说
18:39 <@hezekiah> nop：挑剔？
18:39 < jrand0m> 呵，是啊，做 C API 的各位可以把这些细节搞定
18:39  * jeremiah 看完了之前的记录
18:39 <@nop> 文件叫什么
18:39 <@hezekiah> nop：我只是想把所有不同点找出来， 	这样我们就能像 jrand0m 说的那样敲定。
18:40 <@hezekiah> 我是在帮忙啦。 :)
18:40 <@nop> hezekiah：是，可能得会后
18:40 < jrand0m> nop> simple_latency.xls
18:40 <@hezekiah> boolean sendMessage(Destination dest, byte[] payload);
18:40 <@hezekiah>  会变成
18:40 <@hezekiah> int sendMessage(Destination dest, void* payload, int length);
18:40 <@hezekiah> 。
18:40 <@hezekiah> byte[]  recieveMessage(int msgId);
18:40 <@hezekiah>  它可以是：
18:41 <@hezekiah> void*  recieveMessage(int msgId, int* length);
18:41 <@hezekiah>  或者
18:41 <@nop> jrand0m：收到了
18:41 <@hezekiah> void recieveMessage(int msgId, void* buf, int* length);
18:41 <@hezekiah>  或者
18:41 < jrand0m> hezekia：为何不 typedef struct { int length; void* data; 	} Payload;
18:41 <@hezekiah> DataBlock* recieveMessage(int msgId)l
18:41 <@hezekiah> DataBlock* recieveMessage(int msgId);
18:41 < jeremiah> 那个 xls 在哪？
18:41 <@nop> 哦 iip-dev
18:41 <@hezekiah> jrand0m：你刚提到的那个 struct 基本上就是 	DataBlock。
18:42 < jrand0m> 说得对 hezekiah
18:42 <@nop> 主题 more models
18:42 <@hezekiah> C 版本很可能会用 DataBlock。
18:43 <@hezekiah> 除此之外，唯一需要注意的是每个 	“接口”只是一些函数的集合。
18:43 <@hezekiah> nop：我把 C API 里会存在的差异都找出来了吗？
18:43 < jrand0m> 对。也许 #include "i2psession.h" 或者类似的
18:43 < jeremiah> 有 Python API 的原型吗？
18:44 < jrand0m> 没有，jeremiah，我其实不太会 Python :/
18:44 <@nop> 我得重新过一遍 Java API，但我会说你抓得很准
18:44 < jrand0m> 但它大概会和 Java 类似，因为 Python 是 OO
18:44 < jeremiah> 好，我可以从 C 的那个派生一个
18:44  * nop 不是 Java 党
18:44 < jrand0m> 好的 jeremiah
18:44 < jeremiah> 几天前你发的东西里有 C API 吗？
18:44 <@hezekiah> 是的。Python 应该能应对 Java API。
18:44 < jrand0m> jeremiah> 那是 Java 的那个
18:45 < jrand0m> 哦，Java 的那个是今天的
18:45 < jrand0m> 更早那个是语言无关的
18:45 <@hezekiah> 嗯
18:45 <@nop> UserX 说他能帮忙做 C API
18:45 < jrand0m> 好
18:45 <@nop> 他现在工作很忙
18:46 < jrand0m> 不错
18:46 <@hezekiah> 最后一点：对于 C API，每个函数大概 	都会带一个指向结构体的指针，那结构体在 Java 里对应一个“接口”。
18:46 <@nop> hezekiah：看起来不错
18:46 <@nop> 看起来不错
18:46 <@hezekiah> I2PSession       createSession(String keyFileToLoadFrom, 	Properties options);
18:46 <@hezekiah>  会变成：
18:46 <@nop> Java 以及它那些非原生的数据类型
18:46 <@hezekiah> I2PSession* createSession(I2PClient* client, char* 	keyFileToLoadFrom, Properties* options);
18:46 <@nop> ;)
18:46 < jrand0m> 呵呵
18:46 < jrand0m> 对的 hezekiah
18:47 < jeremiah> 我们要处理 Unicode 吗？
18:47 <@hezekiah> 总之，如果你能接受这些差异，除此之外 C 和 	Java 的 API 应该是一致的。
18:47 <@hezekiah> nop？Unicode？ :)
18:47 < jrand0m> 要么 UTF8，要么 UTF16
18:48 <@hezekiah> 或许 Unicode 应该在应用层处理。
18:48 < jrand0m> 对，字符集都是消息内容层面的
18:48 <@hezekiah> 哦。
18:48 < jeremiah> 好
18:48 <@hezekiah> Java 的 String 是用 Unicode 的，对吧 jrand0m？
18:48 < jrand0m> 所有位桶都会按位定义
18:48 < jrand0m> 是的 hezekiah
18:48 < jrand0m> （除非你显式指示它们改变字符集）
18:49 <@hezekiah> 所以，若 C API 不用 Unicode 来实现字符串，发送给 Java API 的字符串就会与发送给 C API 的不同。
18:49 < jrand0m> 与此无关
18:49 <@hezekiah> 好的。
18:49 < jrand0m> (app->API != API->router.  we only define API->router)
18:49 <@hezekiah> 我是这个意思，jrand0m：
18:50 <@hezekiah> 如果我用 Java API 设置了密码，它会发到 	router。
18:50 < jrand0m> 密码？ 你是说你创建了一个 Destination？
18:50 <@hezekiah> 然后它找到另一个 router，再把它发给另一个 	用 C 实现的 API（？）。
18:50 <@hezekiah>   void            setPassphrase(String old, String new);
18:50 <@hezekiah> 就是这个函数。
18:51 < jrand0m> hezekiah> 那是访问 router 管理方法所用的 	管理口令
18:51 <@hezekiah> 啊
18:51 <@hezekiah> API 里有没有使用 Java String 的函数，最后会把那个 String 	发送到另一个 API？
18:51 < jrand0m> 99.9% 的应用只会用 I2PSession，不会用 I2PAdminSession
18:51 <@nop> 另外，经过 router 携带的任何东西都会转换成 	适合网络传输的格式，对吧？
18:51 <@hezekiah> 如果是那样，或许我们应该用 Unicode。
18:51 <@nop> Unicode 不会相关
18:52 < jrand0m> hezekiah> 不。 所有 router 间的信息都会由 	位桶定义
18:52 <@hezekiah> 好的。
18:52 < jrand0m> 对，nop，在传输层
18:52 <@hezekiah> （我猜位桶就是一个二进制缓冲区，对吗？）
18:53 < jrand0m> 位桶的意思是：第一位表示 X， 	第二位表示 Y，第 3-42 位表示 Z，等等
18:53 < jrand0m> （例如，我们也许想在证书位桶里用 X.509）

18:53 <@hezekiah> 我之前从没处理过这个。 18:54 <@hezekiah> 等到了再说吧。:) 18:54 < jrand0m> 呵，说得对 18:55 < jrand0m> 好，今天我想我们要讨论的四件事：*router 	架构，*性能模型，*攻击分析，*psyc。我们已经做完了第一件，thecrypto 不在线，所以也许我们把这个往后推（除非你对模型有想法，nop？） 18:57 <@hezekiah> 呃……jrand0m。我还有一个问题。 18:57 < jeremiah> jrand0m：网络规范的最新版本在哪？是不是你在 13 号发的那个？ 18:57 < jrand0m> si sr? 18:57 <@hezekiah> 嗯，router 架构是让 API 来处理密钥 	/由应用程序发送给它们/。 18:57 < jrand0m> jeremiah> 是的 18:57 <@nop> 我现在没有 18:58 <@hezekiah> 现在……我能看到 API 获取密钥的唯一方式是通过 createSession。 18:58 < jrand0m> hezekiah> router 会得到公钥和签名， 	不会得到私钥 18:58 < jrand0m> 对 18:58 <@hezekiah> 但那需要一个文件。 18:58 < jrand0m> 密钥存储在文件里，或者存储在 API 的内存里 18:58 < jrand0m> 是的 18:58 <@hezekiah> 那如果应用程序生成了密钥，为什么不能 	通过缓冲区直接把它发给 API？ 18:59 <@hezekiah> 真的必须把它存到文件里，然后再提供 	文件名吗？ 18:59 < jrand0m> 不，如果你愿意，它可以在内存里 18:59 <@hezekiah> 不过 API 里没有相应的函数来做到这些。 18:59 <@hezekiah> 只是个想法。 19:00 <@hezekiah> 如果密钥只生成一次并被反复使用 （像 GPG 密钥那样），那用文件就说得通。 19:00 -!- mihi [none@anon.iip] has quit [各位再见，天色不早了...] 19:00 <@hezekiah> 但如果会更频繁地生成，也许能通过某种 	结构体或缓冲区直接发给 API 会更好 19:00 <@hezekiah> 。 19:01 < jrand0m> 是的，它只生成一次（除非你戴着 	锡纸帽） 19:02 < jrand0m> 不过 createDestination(keyFileToSaveTo) 可以让你 	创建那个密钥 19:02 <@hezekiah> 好。 19:02 <@hezekiah> 所以确实没必要从 App 直接传给 API。用文件就够了。 19:03 <@hezekiah> 在我这么没礼貌地打断之前，我们说到哪儿了？:) 19:06 < jeremiah> 所以现在我们只是在做 router API，不是客户端的那个，对吧？ 19:06 < jrand0m> 嗯，我们暂时跳过性能分析 （希望下周前能在邮件列表里就此聊聊？）。攻击分析也可能同样处理（除非有人读了 	新规范并有评论） 19:07 <@hezekiah> 既然我们跳过那些，现在应该 	谈什么？ 19:07 <@hezekiah> psyc？ 19:07 < jrand0m> 除非还有谁有其他要提的意见…？ 19:08 <@hezekiah> 好吧，难得一次，我的“吐槽洞”（也就是臭名昭著的嘴）空了。 19:08 < jrand0m> hehe 19:09 < jrand0m> 好，谁对 IRC 这边会怎么运作，以及 psyc 是否相关或有用，有什么想法吗？ 19:09 < jeremiah> 顺便一提（这让我很恼火）：Wired 的“Wired, Tired, 	Expired”榜把 Waste 归为“wired” 19:09 < jrand0m> heh 19:09 < jrand0m> 你意识到我们会有多震撼所有人吗？ 19:09 < jeremiah> 没错 19:09 <@hezekiah> jrand0m：那是建立在我们能把它搞定的前提上。 19:10 < jrand0m> 我保证它会成功。 19:10 <@hezekiah> 外面还有很多失败的尝试。 19:10 < jrand0m> 我辞了工作来做这个。 19:10 <@hezekiah> 那我们就要把所有人都震住了。:) 19:10 <@hezekiah> 是啊。那你这么做，你的生计怎么办？ 19:10 <@hezekiah> GPL 代码可不怎么赚钱。;-) 19:10 < jrand0m> heh 19:11 <@hezekiah> 至于 psyc …… 我这么说吧： 19:11 <@hezekiah> 我第一次听说它还是你发邮件给我们 	提到的时候。 19:11 < jrand0m> 靠，这又不是我发现的 :) 19:11 <@hezekiah> 不过，IRC 大概是目前最为（即使不是 /最/） 	广泛的聊天协议之一。 19:11 <@hezekiah> 人们在 /知道/ psyc 是什么之前很久很久， 	就会想要 IRC 应用。 19:11 <@hezekiah> jrand0m：噢，抱歉。我忘了这个细节。:) 19:12 < jrand0m> psyc 可不这么看。 	他们的历史可以追溯到 86 年，我记得是这样 19:12 <@hezekiah> 关键在于，协议是否更优并不 	如谁在用它那么重要。 19:12 <@hezekiah> 他们的 _历史_ 也许确实可以追溯那么久。 19:12 <@hezekiah> 但有多少人 _在用_ Psyc？ 19:12 < jeremiah> 是啊，如果他们从我出生后一年的时候 	（咳）就存在，到现在还没多大动静 19:12 <@hezekiah> 我的意思是，即使它是更好的协议，大多数人还是 _在用_ IRC。 19:13 <@hezekiah> 我们可以打造这个星球上最好的 I2P 网络…… 19:13 -!- Ehud [logger@anon.iip] has quit [Ping 超时] 19:14 < jeremiah> 谁能简单解释一下我们为什么要关心这个？我以为 IRC 	只是可能的一个应用，但网络足够灵活，如果想的话也能支持 psyc 19:14 <@hezekiah> 对。 19:14 <@hezekiah> Psyc 可以做出来…… 19:14 <@hezekiah> ……但我的意思是我们应该先做 IRC，因为用它的人更多。

19:14 <@hezekiah> jrand0m，我们可以打造一个很棒的 I2P 网络，但除非它有他们想要的东西，人们不会	使用它。 19:14 < jrand0m> jeremiah> psyc 之所以有意思，是因为我们可能	想用和 psyc 相同的方式来实现 IRC
19:15 <@hezekiah> 因此我们应该给他们提供一款‘杀手级应用’。
19:15 < jeremiah> ok
19:15 < jrand0m> 对，IIP 是 Invisible IRC Project，并且会让人们	运行 IRC
19:16 < jrand0m> 在没有中心服务器（实际上根本没有任何服务器）的情况下，	要花很多心思来弄清楚 IRC 将如何工作。
	psyc 可能对此有一个答案
19:16 < jrand0m> 不过也有其他办法
19:17 <@hezekiah> 就像我说的，psyc 也许会更好，但人们想用的是 IRC，	不是 psyc。
19:17 < jrand0m> 他们会的
19:17 < jrand0m> 他们会用 IRC
19:17 <@hezekiah> 一切都靠市场营销，宝贝！ ;-)
19:17 < jeremiah> 我今晚会试着读一下规范和一些关于 psyc 的资料
19:17 < jrand0m> 没错
19:17 <@hezekiah> lol
19:17 < jeremiah> 计划明天 5:00 UTC 见面？
19:17 <@hezekiah> 不？
19:18 < jeremiah> 或者任何时候都行
19:18 < jrand0m> 我在 iip 上 24x7 :)
19:18 < jeremiah> 是啊，但我还得吃饭
19:18 <@hezekiah> jrand0m：我注意到了。
19:18 < jrand0m> 05:00 UTC 还是 17:00 UTC？
19:18 <@hezekiah> jeremiah：LOL！
19:18 <@hezekiah> 嗯，iip-dev 会议正式开始的时间是 21:00 UTC。
19:18 -!- Ehud [~logger@anon.iip] 已加入 #iip-dev
19:19 < jeremiah> ok，我刚才说 05:00 UTC 只是随口胡扯。
19:19 < jeremiah> mids 在哪？
19:19 <@hezekiah> mids 暂时离开这个项目了。
19:19 <@hezekiah> 你几次会议前不是还在吗？
19:19 < jeremiah> ok
19:19 < jeremiah> 看来不是
19:19 <@hezekiah> 我们还在议程里安排了个类似告别会的环节。
19:19 < jeremiah> 哦
19:20 <@hezekiah> 好的……
19:20 <@hezekiah> 议程上还有其他事项吗？
19:20  * jrand0m 我这边没剩什么了
19:20 < jeremiah> 关于 psyc：
19:20 < jeremiah> 如果这是 psyc 的一个特性，我记得你	不久前提到过
19:20  * hezekiah 一开始就没准备过议程
19:21 <@hezekiah> pace
19:21 <@hezekiah> place
19:21 < jeremiah> 我觉得让每个用户向房间里	每个其他用户都发送一条消息并不是个聪明的主意
19:21 <@hezekiah> 好了！
19:21 < jrand0m> jeremiah> 所以你的意思是让冗余的、被指定的 pseudoservers	来转发这些消息？
19:21 < jrand0m> (pseudoservers = 频道中持有用户列表	的节点)
19:21 < jeremiah> 我也不觉得‘broadcasting’有多聪明，不过它

seems like it'll require a _lot_ of bandwith for a given user who may be on 	a modem, and with the lag from sending say... 20 messages separately would 	screw up conversation 19:21 < jeremiah> 我不确定最好的解决方案是什么，也许那就是一种办法 19:22 < jeremiah> 我觉得如果你需要，直接消息会很好， 	不过也有些情况下可能并没有那么重要 19:22 <@hezekiah> 消息需要用作者的私钥签名，才能保证真实性。 19:22 <@hezekiah> 不过这个问题很长一段时间都无关紧要， 	我觉得 jeremiah 说得有道理 19:22 < jrand0m> hezekiah> 那就得是用户想要可证明的通信了 :) 19:23 < jrand0m> 的确如此。 19:23 <@hezekiah> 如果我得给一个频道里的 100 个用户发消息…… 19:23 < jeremiah> 虽然我平均一条消息只有几百字节， 	所以发给几百个用户也许没那么难 19:23 <@hezekiah> ……那我的对话就会/非常/慢。 19:23 < jeremiah> 尤其是你不等待响应的话 19:23 <@hezekiah> 发一条消息要 20K。 19:23 <@hezekiah> 我不这么认为。:) 19:23 < jrand0m> 嗯，如果一个频道里有 100 个用户，得*有人* 	发出 100 条消息 19:23 < jeremiah> 是 20K？ 19:23 < jeremiah> 哦，对 19:23 <@hezekiah> 200 个用户 19:24 < jeremiah> 嗯 19:24 < jeremiah> routers 做这个不是很擅长吗？ 19:24 < jeremiah> 我们基本可以认为它们有不错的带宽， 对吧？ 19:24 <@hezekiah> 我以为每个人都有一个“router implementation” 19:24 < jrand0m> 不一定。 如果有中继，提名机制 	需要把这点考虑进去 19:24 < jrand0m> 是的 hezekiah 19:24 < jeremiah> 我还没读过规范 19:25 < jrand0m> a router 就是你的本地 router 19:25 <@hezekiah> 呃！ 19:25 <@hezekiah> 我还在把你们的昵称搞混！ 19:25 <@hezekiah> lol 19:25 < jrand0m> 呵呵 19:25 <@hezekiah> 嗯……nop 去哪儿了？ 19:25 <@hezekiah> 哦。 19:26 <@hezekiah> 他还在。 19:26 <@hezekiah> 我刚刚还以为他走了， 19:26 < jrand0m> 不过 jeremiah 说得对，psyc 有些想法值得我们 	考虑，虽然也许我们会否决它们 19:26 <@hezekiah> 我们先把网络跑起来吧。 19:26  * jrand0m 为此干杯 19:26 <@hezekiah> 如果你的目光老是盯着终点线，你会被 	离你 3 英寸远的石头绊倒。 19:27  * jeremiah 备受鼓舞 19:27 <@hezekiah> lol 19:27 < jrand0m> 我觉得如果我们能争取在下周前审阅 	网络规范就太好了，任何人有想法或意见就给 iip-dev 发邮件。 我是不是疯了？ 19:27 <@hezekiah> nop？你还有要加进议程的内容吗， 	还是我们休会？ 19:27 <@hezekiah> jrand0m：嗯，我不确定我能不能在 	下周前把那些都读完，但我可以试试。:) 19:27 < jrand0m> 嘿 19:28 < jrand0m> 一共就 15 页，读起来挺累的 ;) 19:28 <@hezekiah> 15 页？ 19:28 <@hezekiah> 看起来更像 120！ 19:29 < jrand0m> 呵，嗯，取决于你的分辨率吧 ;) 19:29 < jeremiah> 他放了很多锚点，看起来 	好像很庞大 19:29 < jrand0m> 呵呵 19:29 <@hezekiah> 左边可是有远不止 15 个链接啊，伙计！ 19:29 <@hezekiah> ‘招了吧！’ 19:29 <@hezekiah> 肯定不止 15。:) 19:29 <@hezekiah> 哦！ 19:29 <@hezekiah> 那些不是页面！只是锚点而已！ 19:29 <@hezekiah> 得救了！ 19:30  * hezekiah 感觉自己像刚从溺水中获救的海员 19:30 < jeremiah> 同学们翻到第 4 卷第 2 章 消息字节结构 19:30 < jrand0m> lol 19:30 <@hezekiah> lol 19:30 <@nop> adjourn 19:30 <@hezekiah> *baf*! 19:30 <@hezekiah> 下周 21:00 UTC，老地方。 19:30 <@hezekiah> 到时见。:) 19:30 < jeremiah> 再见 --- 日志关闭 Tue Jul 15 19:30:51 2003 </div>
