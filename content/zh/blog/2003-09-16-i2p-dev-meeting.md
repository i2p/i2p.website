---
title: "I2P 开发者会议，2003年9月16日"
date: 2003-09-16
author: "jrand0m"
description: "第58次 I2P 开发者会议，涵盖 IM（即时通信）和命名服务应用、开发状态、加密密钥持久化以及规范更新"
categories: ["meeting"]
---

<h2 id="quick-recap">快速回顾</h2>

<p class="attendees-inline"><strong>出席：</strong> co, jrand0m, LeerokLacerta, mihi, mrflibble, mrsc, nop, shardy, thecrypto, w0rmus</p>

<h2 id="meeting-log">会议记录</h2>

<div class="irc-log"> [22:53] <jrand0m> 0) welcome
[22:54] <jrand0m> 1) apps:
[22:54] <jrand0m> 1.1) IM（即时通信）
[22:54] <jrand0m> 1.2) NS（命名服务）
[22:54] <jrand0m> 2) dev status:
[22:54] <jrand0m> 2.1) subsystems
[22:54] <jrand0m> 2.2) encryption key persistence
[22:54] <jrand0m> 2.3) todo
[22:54] <jrand0m> 3) spec stuff
[22:54] <jrand0m> 3.1) mods
[22:54] <jrand0m> 4) administravia:
[22:54] <jrand0m> 4.1) anon cvs
[22:54] <jrand0m> 5) ?
[22:55] <jrand0m> 好，0) welcome
[22:55] <jrand0m> 欢迎来到第 58 次会议
[22:55] <thecrypto> 就这些吗
[22:55] <jrand0m> 是的先生，除非还有人要补充？
[22:55] * nop 注意到 jrand0m 的编号是面向对象的 :)
[22:56] <nop> 3.1.2.2.4.5.8() ;)
[22:56] <jrand0m> 嘿，它们也可以是 structs ;)
[22:56] <nop> 哈哈
[22:56] <nop> 的确如此
[22:56] <jrand0m> 好，1.1) IM。thecrypto？
[22:56] <nop> 不过
[22:56] <nop> 2 有继承关系
[22:57] <nop> ;)
[22:57] <jrand0m> 呵
[22:57] <nop> 别理我
[22:57] <nop> 好的
[22:57] <nop> 抱歉
[22:57] <nop> 继续
[22:57] *** mihi_ (~none@anon.iip) 加入频道 #iip-dev
[22:57] <thecrypto> 好的，我现在在上传一些 IM 的基础规范
[22:58] <thecrypto> (Link: http://www.thecrypto.org/i2pim.sxw)http://www.thecrypto.org/i2pim.sxw 供 oowriter 使用
[22:58] <thecrypto> 我正在上传 pdf
[22:59] <nop> 如果你愿意我可以放到 i2p 站点上
[22:59] <thecrypto> 等我一下
[22:59] <thecrypto> 可以
[22:59] *** mrflibble (mrflibble@anon.iip) 加入频道 #iip-dev
[22:59] <jrand0m> 你想把它放到 i2p/apps/IM/doc/ 里吗？
[22:59] *** mihi_ 现在叫做 mihi_backup
[23:00] <nop> 我可以
[23:00] <nop> 行
[23:00] <jrand0m> 我是说进 cvs 里 :)
[23:00] <thecrypto> 我也可以做
[23:00] <jrand0m> （但放到网页上也不错）
[23:00] <nop> 哦
[23:00] <nop> 哈哈
[23:00] <thecrypto> (Link: http://www.thecrypto.org/i2pim.pdf)http://www.thecrypto.org/i2pim.pdf
[23:01] <MrEcho> “文件已损坏且无法修复” Adobe Reader 报错
[23:01] <thecrypto> 再试一次
[23:01] * jrand0m 这边打开没问题
[23:01] <co> MrEcho：PDF 文件吗？
[23:01] <jrand0m> （那个 sxw）
[23:01] <thecrypto> 刚才只上传了一部分
[23:01] <MrEcho> 现在好了
[23:01] <MrEcho> 呵呵
[23:02] <thecrypto> 基本上我只放了在线状态（presence）、在线/离线消息，还有一条 message 消息
[23:02] <thecrypto> 我不羞愧地从 I2NP 文档里抄了一些段落
[23:02] <thecrypto> :)
[23:02] <jrand0m> 呵 我就觉得有些地方眼熟 :)
[23:02] <thecrypto> 我也在上传我做的 UI
[23:02] <thecrypto> 我一直在做的那个
[23:03] <thecrypto> jrand0m：我需要创建目录 apps/IM/doc 吗
[23:03] <jrand0m> 是的，并且要逐个 cvs add
[23:03] <thecrypto> -kb?
[23:03] <jrand0m> 对
[23:03] <co> thecrypto：我记得 apps/ 已经有了。
[23:04] <jrand0m> presence 是什么？
[23:05] <thecrypto> 我先跑个 update
[23:05] <thecrypto> 不过很快就会进去
[23:05] *** Signoff: shardy (Ping timeout)
[23:05] <thecrypto> 我的意思是大家尽情撕规范
[23:05] <thecrypto> UI 也会很快进去
[23:05] <thecrypto> 如果有需要澄清的地方，就 anonymail、e-mail 什么的联系我，我来改
[23:05] <mrflibble> 我错过会议了？
[23:05] *** shardy (~shardy@anon.iip) 加入频道 #iip-dev
[23:05] <co> thecrypto：你也许还想在邮件列表上发个通知，附上文档链接。
[23:05] <thecrypto> 我以为我写上去了？
[23:05] <jrand0m> 没呢，mrflibble，我们还在第一项
[23:05] <co> mrflibble：会议进行中。
[23:05] <mrflibble> 哦 抱歉，我没看到 “logger”
[23:06] <jrand0m> thecrypto> 你说那是一个 destination，但那是用来发送消息的 destination 吗？离线消息怎么处理？
[23:06] <mihi> 这儿没有 mids，所以没有 logger ;)
[23:06] <mrflibble> 好的
[23:06] * mrflibble 继续潜水
[23:06] <jrand0m> 哦等等，这些只是在线状态通知，抱歉
[23:06] <mihi> 怎么订阅一个 presence？
[23:06] <thecrypto> jrand0m：不支持离线消息
[23:07] <thecrypto> 基本上
[23:07] <thecrypto> presence 只是把一个 destination 和一个名字打包在一起
[23:07] <thecrypto> 方便点
[23:08] <thecrypto> 如果我们想转到 NS，可以先讲 NS，之后再回到这个？
[23:09] <jrand0m> 行，酷
[23:09] <thecrypto> 你们也可以继续给我发问题
[23:09] <jrand0m> 其实，快速问一个
[23:09] <thecrypto> 说吧
[23:09] <jrand0m> 这个 IM 只支持纯文本吗？
[23:10] <thecrypto> 这个基础版是的，但我会加上文件支持
[23:10] <jrand0m> 酷~
[23:10] <thecrypto> 我只是想先把系统的开端搭起来，再在上面迭代
[23:10] <jrand0m> （迭代增量式）++
[23:11] <jrand0m> 好极了。我会进一步看这个，大家也都看看……现在转到 1.2) NS。co？
[23:11] <co> 命名服务规范 1.1 版（最终版）今天早些时候发布了。
[23:12] <jrand0m> （随后一片欢呼）
[23:12] <co> 基本上，我完成了程序需要的数据结构和网络消息部分。
[23:12] <co> 我会在周四发布客户端 API。
[23:12] <co> 然后开始实现 NS 应用。
[23:12] <jrand0m> 很好
[23:13] <co> 有一个想法变了，涉及 CA（证书颁发机构）在实体注册时的处理。
[23:13] <thecrypto> co：你会怎么实现？
[23:13] <thecrypto> co：是 name server 还是 client？
[23:14] <co> thecrypto：嗯，我会先实现必要的数据结构。
[23:14] <co> 然后是客户端，再是服务器和 CA 组件。
[23:14] <thecrypto> 好的
[23:15] <co> 正如我所说，我现在希望 CA 给新注册的实体签发一个证书。
[23:15] <co> 他们在修改记录时会把这个证书呈交给命名服务器。
[23:15] <co> 我还没有在这个版本里指定证书包含什么；这会放进下一版规范。
[23:16] <co> 大家觉得这是个坏主意吗？
[23:16] <jrand0m> 嗯。是否更简单/更安全的是让客户端用一对公钥/私钥？
[23:16] <jrand0m> 也就是在注册时提供一个用于更新的公钥并对注册请求签名，之后每次更新都签名一个更新请求
[23:16] <jrand0m> （这样 CA 永远拿不到私钥）
[23:17] <thecrypto> 顺带说一句：所有 I2PIM 的内容都已经提交到 cvs 仓库了
[23:17] <jrand0m> 很好
[23:17] <co> 这么做也许更简单。我会重新考虑这个问题。谢谢你的建议。
[23:17] <co> 如果没有别的问题，我关于命名服务就说这些。
[23:18] <jrand0m> 看起来不错，我还没看 1.1，我看完如果有问题会发邮件
[23:19] <co> 好。下一个话题？
[23:19] <jrand0m> 好，2.1) 子系统的开发状态。
[23:19] *** w0rmus (o0o@anon.iip) 加入频道 #iip-dev
[23:20] <jrand0m> 传输子系统已经足够好可以继续往前。对等体管理子系统用的是很蠢的算法做了个桩，但能用。network db、tunnel 管理和统计管理子系统还在路上。客户端子系统会很简单（直接复用 SDK 的本地-only router）
[23:21] <co> 你说的蠢算法是什么意思？
[23:21] <w0rmus> 不够快？
[23:21] <jrand0m> 嗯，对等体管理子系统没有跟踪对等体性能，只是返回随机的对等体。
[23:22] <jrand0m> 算法会随着进展更新和调优，以更好地做对等体选择
[23:22] <jrand0m> 我手头当前的任务是构建和处理 garlic messages（garlic 消息，一种 I2P 分层消息封装），这是个 PITA。
[23:23] <jrand0m> 但能搞，就是烦
[23:23] <jrand0m> 这其实引出 2.2) 加密密钥持久化。
[23:24] <jrand0m> garlic messages 用 ElG+AES 加密来包裹每个“clove”的层
[23:24] <jrand0m> 而私钥还用于其他地方（传输、客户端管理）
[23:25] *** Signoff: thecrypto (Ping timeout)
[23:25] <jrand0m> 把私钥和会话密钥一直留在内存里、永不落盘是理想的，但当 router 关闭（主动或故障）时就很糟糕
[23:26] <jrand0m> 大家对下面哪种做法有想法吗：1）绝不把密钥写盘，冒着过多不必要消息丢失的风险（因为无法解密）2）写盘前加密它们 3）直接明文写盘？
[23:26] <co> 选项 2。
[23:27] <nop> jrand0m 选项 2，或者按我们之前说的做
[23:27] <nop> 我们必须信任 localhost
[23:27] *** Signoff: cohesion (class)
[23:27] <nop> 我们假设 localhost 没被攻破
[23:27] <jrand0m> 选项 2 的古怪之处在于，要么用户必须在启动 router 时输入口令，要么会话密钥可以被获知
[23:27] <jrand0m> 说得对，nop。
[23:28] <nop> 再说我们是个传输层，没法太替他们担这个心，这可以在客户端侧调整，或者我们提供选项
[23:28] <nop> 取决于偏执等级
[23:28] <nop> 安全 vs 便利 的权衡
[23:29] <co> 那我建议默认 3，并给用户选择使用 2。
[23:29] <nop> 正是
[23:29] <jrand0m> 对。好在大家可以（而且应该！）拿 router 代码去改，做这种权衡——一个“tinfoil I2P router（偏执版）”和一个“jane sixpack I2P router（大众版）”
[23:29] <jrand0m> 好，酷，那我现在就先用简单的 3)
[23:30] <jrand0m> 好 2.3) todo
[23:30] * co 想在会议末尾回到 NS 话题。
[23:30] * nop 需要把 NS 的邮件读完
[23:30] <jrand0m> 行，你现在是第 #5 项
[23:30] <co> 我可以等到最后。
[23:31] <jrand0m> mihi 写了一些测试来指出 SDK 实现里的 bug。有些已修，有些没。修它们在 todo 上 :)
[23:32] <jrand0m> 另外，各种规范改了大概一打地方。我一有时间就更新文档并发出来，或者我可能先在 wiki 上放个勘误页
[23:33] <nop> word
[23:34] <jrand0m> 其他的 todo……嗯，我今天早上修了“Wrong Size generating key”这个问题，以及一些随机 bug
[23:34] <jrand0m> 好了，开发状态就这些。3) 规范相关
[23:35] <jrand0m> 3.1) 参见 todo 里的 mods。大多是排版修改。今天在实现 garlic 时碰到一个稍大点的变动。问题不大，只是需要挪动一些数据结构，并在加密上做点小技巧。我会把它写进勘误。
[23:35] <jrand0m> 3.2) 【我知道这项不在议程里，但还是说一下】规范问题
[23:35] <shardy> （马上回来，如果需要我我还在潜水）
[23:35] <jrand0m> 有人对任何规范有问题吗？
[23:35] <jrand0m> 不错 shardy
[23:36] <co> jrand0m：请再说一次哪个规范在哪个文档里。
[23:37] <jrand0m> (Link: http://wiki.invisiblenet.net/iip-wiki?I2PProtocolSpecs)http://wiki.invisiblenet.net/iip-wiki?I2PProtocolSpecs 上都有映射
[23:37] <co> 我去看一下。
[23:38] <jrand0m> （看着这个我想起还得把 secure reliable UDP 传输写成文档。这又是一个 todo……）
[23:39] <jrand0m> 最近有人问该看哪些规范——基本上，除非你想知道 router 怎么工作（或者你想帮忙实现），否则你不需要读 I2NP 规范。I2CP 和数据结构里 I2CP 的部分就够了
[23:40] <nop> jrand0m
[23:40] <jrand0m> 是的先生？
[23:41] <nop> 你说的 UDP 是指真的 UDP 包那种 UDP 吗
[23:41] <nop> 还是泛指一种 UDP 协议
[23:41] <jrand0m> 对，UDP 就是 UDP 包
[23:41] <nop> 用在 I2P 上
[23:41] *** thecrypt1 (~thecrypto@anon.iip) 加入频道 #iip-dev
[23:41] *** thecrypt1 现在叫做 thecrypto
[23:41] <jrand0m> i2p/code/router/java/src/net/invisiblenet/i2p/router/transport/udp 里有实现
[23:42] <thecrypto> 回来了
[23:42] <jrand0m> 欢迎回来
[23:42] <thecrypto> 有人能发我我不在时发生了什么吗？
[23:43] <jrand0m> 这个 UDP 实现挺简单——做一次 DH 交换，消息拆成 1K 包，用生成的密钥做 AES256 加密
[23:43] <jrand0m> 支持重密钥，但目前不是自动的
[23:43] <jrand0m> ACK 会打包返回（比如“我收到了消息 42 的所有包，直到第 18 个，但不包括 3 和 7”）
[23:44] <jrand0m> （而我先做 UDP 实现而不是 TCP 的实际原因是，UDP 以几乎零开销提供“免费”的异步 IO）
[23:45] <nop> 当然
[23:45] <jrand0m> 这个 UDP 实现还剩两件事——用 Station-to-Station（STS）协议抵御 MITMs（中间人攻击），以及加一个“糟了，我忘了会话密钥”的数据包
[23:45] <nop> 不错
[23:46] <jrand0m> 在 UDP 传输之后，我下一个想实现的是轮询 HTTP——这样就能同时支持普通用户（UDP）以及被防火墙/NAT/代理的用户（轮询 HTTP）
[23:47] <jrand0m> 好的，所以，是的，这需要写成规范文档 :)
[23:48] * jrand0m ！自扇一巴掌，因为先写代码再写规范
[23:48] <thecrypto> 先写代码再写规范对我有帮助
[23:48] <jrand0m> 对，迭代做效果最好
[23:48] <jrand0m> （实现过程中我们也在发现规范的问题，等等）
[23:49] <jrand0m> 好，这是 3) 规范。4) 行政杂务
[23:49] <jrand0m> 4.1) anon cvs。thecrypto？:)
[23:49] <thecrypto> 正好赶上
[23:49] <thecrypto> 嗯，我在看，我想 2401 现在被挡了
[23:49] <jrand0m> 你能在本地做 cvs -d :pserver: 吗？
[23:49] <thecrypto> 可能还要做点 inetd 的东西，谢谢 jrandom
[23:50] <jrand0m> 啊 酷
[23:50] <thecrypto> 我试试，我忘了你可以那样做了 :)
[23:51] <thecrypto> 命令就是 cvs -d :pserver: 吗？
[23:51] <jrand0m> cvs -d :pserver:anonymous@localhost:/home/cvsgroup/cvsroot/ co i2p
[23:52] <jrand0m> 另外，如果能放个 bugzilla 上去也很棒
[23:52] <thecrypto> acvs [checkout aborted]: connect to localhost(127.0.0.1):2401 failed: Connection refused
[23:52] <jrand0m> 行，加了 inetd.conf 那行并对 identd 发了 kill -HUP 之后呢？
[23:52] <thecrypto> 我去试下那条 inet 行，稍后回复你
[23:52] <jrand0m> 呃，inetd :)
[23:52] <jrand0m> 行，酷
[23:53] <thecrypto> pserver 跟在同一行吗？
[23:53] <jrand0m> 对，整行都放一起
[23:55] <jrand0m> 好了，行政杂务就这些，至少我能想到的
[23:55] <jrand0m> 5a) co，你上
[23:56] <co> 当两个人想注册相同的实体名，第二个会被拒绝。
[23:56] <co> 但如果我们用基于签名的方法，
[23:56] <co> 被拒的人仍然可以给命名服务器发消息
[23:56] <co> 让它修改记录。
[23:56] <co> 有两种可能：
[23:57] <co> 1) CA 把获批实体的公钥副本发给命名服务器。
[23:57] <co> 2) CA 给注册名字的人发一个由其私钥签名的证书。命名服务器会有 CA 的公钥来验证它。
[23:58] <co> 如果恶意用户让命名服务器修改某条记录，没有证书就会阻止修改。
[23:58] <co> 我当时是这么想的。
[23:59] <jrand0m> 但那样 CA 就知道密钥了——用非对称密码的话 CA 只会知道公钥，而且 CA 永远不想也不需要把那个公钥给任何人——那只是让合法更新者在请求更新时拿来做签名验证的
[00:00] <jrand0m> 你描述的更像对称密码——本质上就是用个口令
[00:00] <thecrypto> cvs 在跟我作对！
[00:00] <jrand0m> （证书就是 CA 和昵称合法持有者之间共享的机密）
[00:00] *** mrsc (~efgsdf@anon.iip) 加入频道 #iip-dev
[00:01] <jrand0m> 怎么了 thecrypto？
[00:01] <thecrypto> 我加了用户 anonymous，空密码，把它加进 readers 和 cvsgroup，但我得到 cvs login: authorization failed: server localhost rejected access to /home/cvsgroup/cvsroot for user anonymous
[00:01] <co> jrand0m：说得好。就当这部分规范还没定，我再想想。
[00:01] <jrand0m> 好的
[00:01] *** LeerokLacerta (~leerok@anon.iip) 加入频道 #iip-dev
[00:02] <LeerokLacerta> こんにちは。
[00:02] <jrand0m> 嗯 thecrypto，我不觉得你想要一个名为 anonymous 的操作系统用户
[00:02] <jrand0m> 嗨 LeerokLacerta
[00:02] <LeerokLacerta> 你好，jrand0m。
[00:02] <thecrypto> 我设了个密码，现在能用了
[00:03] <co> jrand0m：你看完规范如果还有建议也发我。
[00:03] <jrand0m> 会的，co
[00:03] <jrand0m> 不错 thecrypto……他们的 shell 是 /bin/false 吗？
[00:03] <thecrypto> 我现在得去找 cvs 手册里那个如何建用户的章节
[00:03] -> *thecrypto* 密码是什么？
[00:04] <thecrypto> 现在是了
[00:05] <jrand0m> 好，我们可以在会后处理这个。
[00:05] <jrand0m> 好，议程最后一点：5b) ?
[00:05] <jrand0m> 还有什么问题/想法/担忧吗？
[00:05] <thecrypto> 就看看 IM 应用
[00:06] <thecrypto> 现在它只会生成一个树，但能让你看到它开始的样子
[00:06] <LeerokLacerta> 没有 SOCKS？
[00:06] <thecrypto> 哦对，我忘了这个
[00:06] <jrand0m> 啊 酷 thecrypto
[00:06] <jrand0m> SOCKS？就是那个代理协议？
[00:06] <thecrypto> 有人擅长做图标吗？
[00:06] <LeerokLacerta> 是的。
[00:06] <LeerokLacerta> 我每次问到的答案都是“没有”。
[00:07] <jrand0m> 啊。是的，我们肯定会需要一个 SOCKS 代理，但目前没人做。
[00:07] <LeerokLacerta> 嗯。
[00:07] <jrand0m> 这是我们希望在 1.0 公测时具备的应用之一，这样人们能浏览基于 i2p 的站点，也能匿名浏览普通网页
[00:07] <mihi> 免费的 socks 代理已经够多了，我觉得 ;)
[00:08] <jrand0m> 正是，我们只需要集成它们
[00:08] <mihi> 但我不知道有 Java 的。
[00:08] <jrand0m> JAP 客户端应用也许可用，不过我不知道它是不是 GPL
[00:08] <mihi> JAP 客户端不包含代理。
[00:08] <thecrypto> 我这边 I2PIM 项目需要一些图标
[00:09] <thecrypto> 用来表示在线、离线和一群人
[00:09] <mihi> 唯一的代理是一个 http/ftp 代理，而且在最后一个 mix 里。
[00:10] <mihi> 就像 iip 一样——isproxy 并不懂任何 IRC 协议。
[00:10] <jrand0m> 嗯，那是出站侧——对于基于 i2p 的网站，我们需要一个东西来接受本地浏览器的代理请求，查找 dest，然后把消息发给相应的 dest
[00:10] <thecrypto> 有人感兴趣吗？
[00:11] <co> thecrypto：你可以从 GPL 的 gaim 项目里拿图标吗？
[00:11] * jrand0m 用 MS Paint 画出恐怖而无聊的图形
[00:11] <co> 因为它是 GPL 的，这个也是，除非我搞错了。
[00:11] <thecrypto> 行，我可以
[00:11] <jrand0m> 如果 I2PIM 用了 sdk 的客户端库，那 I2PIM 肯定是 GPL 的 :)
[00:12] <thecrypto> 啊，伟大的 GPL
[00:12] <jrand0m> LeerokLacerta> 你问这个有啥特别原因，还是只是想鞭策我们做？;)
[00:13] <thecrypto> gaim 的问题是，它们来自它支持的 IM 应用
[00:14] <thecrypto> 所以如果有人能做个 I2PIM 的图标就太好了
[00:15] * jrand0m 觉得我们暂时会有很多用画图涂鸦出来的图片……
[00:16] <jrand0m> 好，大家还有别的想法/问题/“commnets”吗？
[00:16] <nop> 我有 commnets
[00:16] <jrand0m> （除了“wtf 是 commnet”以外）
[00:16] <jrand0m> 这是会传染的吗？
[00:16] *** nixonite (~nixonite@anon.iip) 加入频道 #iip-dev
[00:16] <mrflibble> lol
[00:17] <jrand0m> 行，如果没有，那就差不多收尾了，议程项已完
[00:17] <nixonite> 我错过会议了吗？
[00:17] <jrand0m> 是的，GMT 晚上 9 点
[00:17] <jrand0m> 不过，严格来说你赶上了尾巴 :)
[00:17] <nixonite> 哦
[00:18] <co> nop：说来听听。
[00:18] <thecrypto> 所以评论是什么
[00:18] * jrand0m 以为 nop 只是拿我打字错误开涮，但如果他有评论，兄弟请讲
[00:20] <thecrypto> anon cvs 还是不待见我，明天再折腾
[00:20] <jrand0m> 给我 root，我把它弄起来
[00:21] <thecrypto> 找 nop 谈这个
[00:21] <jrand0m> 呵 行
[00:22] <jrand0m> 好吧，既然 nop 似乎又被拉回去干活了……
[00:22] <jrand0m> nop，还有其他人也是> 如果你们有任何评论/问题/担忧，要么告诉我们，要么发在邮件列表（或者写进 wiki）
[00:23] * jrand0m 装填完毕，用 *baf* 把会议轰到了终点。

</div>
