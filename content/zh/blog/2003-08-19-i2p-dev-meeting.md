---
title: "I2P 开发者会议，2003年8月19日"
date: 2003-08-19
author: "jrand0m"
description: "第54次 I2P 开发者会议，涵盖 SDK 更新、I2NP 评审、密码学进展以及开发状态"
categories: ["meeting"]
---

<h2 id="quick-recap">快速回顾</h2>

<p class="attendees-inline"><strong>出席：</strong> cohesion, hezekiah, jrand0m, mihi, nop, thecrypto</p>

<h2 id="meeting-log">会议记录</h2>

<div class="irc-log"> --- 日志打开时间 Tue Aug 19 16:56:12 2003 17:00 -!- logger [logger@anon.iip] 加入了 #iip-dev 17:00 -!- #iip-dev 的主题: 每周 IIP 开发会议，以及其他	 开发者之间的对话都在这里进行。 17:00 [Users #iip-dev] 17:00 [ cohesion] [ leenookx  ] [ mihi] [ shardy_  ] [ UserXClone] 17:00 [ Ehud    ] [ logger    ] [ nop ] [ thecrypto] [ velour    ] 17:00 [ hezekiah] [ lonelynerd] [ Rain] [ UserX    ] [ WinBear   ] 17:00 -!- Irssi: #iip-dev: 共 15 个昵称 [0 ops, 0 halfops, 0 voices, 15 普通] 17:00 -!- Irssi: 加入 #iip-dev 的会话在 7 秒内同步完成 17:00 < hezekiah> 好的！ :) 17:00 < hezekiah> 两个记录器都就位了。 :) 17:01 < thecrypto> 耶！ 17:03 < hezekiah> 嗯…… 17:03 < hezekiah> 这次会议本该在 3 分钟前开始。 17:03 < hezekiah> 不知道怎么回事。 17:04 < thecrypto> 嗯，谁在挂机 17:04 < hezekiah> jrand0m 甚至不在线。 17:04 < hezekiah> nop 挂机了 15 分钟。 17:05 < nop> 嗨 17:05 < nop> 抱歉 17:05 < nop> 我工作这会儿超级忙 17:05 < mihi> [22:36] * jrand0m 去吃晚饭了，但我会在半小时内回来参加会议 17:05 -!- jrand0m [~jrandom@anon.iip] 加入了 #iip-dev 17:05 < hezekiah> 嗨，jrand0m。 17:05 < nop> 嗨 17:05 < nop> 好吧，是这样的 17:05 < nop> 我现在在公司不能被人看到我上 IIP 17:05 < nop> 所以我待会儿再和你们联系 17:05 < nop> 昨天因为这事被上头提醒了一下 17:05 < nop> 所以 17:05 < hezekiah> 拜，nop。 17:05 < thecrypto> 拜 17:06 < nop> 我会挂在频道里 17:06 < nop> 只是不会太明显 :) 17:06 < hezekiah> jrand0m？既然最近你说得最多，这次会议的议程里 	 你想加点什么吗？ 17:07 < jrand0m> 回来啦 17:08 < jrand0m> 好的，香蒜酱意面不错。 17:08 < jrand0m> 让我把类似议程的东西调出来 17:09 -!- Lookaround [~chatzilla@anon.iip] 加入了 #iip-dev 17:09 < jrand0m> x.1) i2cp sdk 更改 x.2) i2np 评审 x.3) 轮询 http 	 传输 x.4) 开发状态 x.5) 待办 x.6) 接下来两周的计划 17:09 < jrand0m> （把 x 放到议程里合适的位置） 17:10 < thecrypto> 你就是议程 17:10 < hezekiah> jrand0m: 我没什么要说的，而且 nop 能 17:10 < hezekiah> 不能说话。 17:10 < jrand0m> lol 17:10 < hezekiah> UserX 多半也不会加什么（他通常不会），所以就我而 	 言，交给你了。:0 17:10 < hezekiah> :) 17:10 < jrand0m> 行。我们在记录吗？ 17:10 < jrand0m> 呵 17:10 < hezekiah> 我把一切都在记录。 17:10 < jrand0m> 酷。好。0.1) 欢迎。 17:10 < jrand0m> 嗨。 17:11 < jrand0m> 0.2) 邮件列表 17:11 < jrand0m> 列表现在挂了，会尽快恢复。恢复了你们就知道了 :) 17:11 < jrand0m> 这段时间，用 wiki 或用 iip 聊天。 17:11 < jrand0m> 1.1) i2cp SDK 更改 17:12 < jrand0m> SDK 已更新，修了一些 bug，还引入了规范里的新东 	 西。 17:12 < jrand0m> 我昨天把信息发到列表上了。 17:13 < jrand0m> hezekiah/thecrypto/jeremiah> 对我发的内容有什么问题吗， 	 或者对实现这些更改的计划有什么想法？（或者我没考虑到的其他替 	 代方案？） 17:13 < hezekiah> 我这几天像只被砍了头的鸡一样跑来跑去准备上大学。 17:13 < jrand0m> 行，明白。 17:13 < hezekiah> 我粗略看了下你写的，但还没真正看规范的更改。 17:13 < jrand0m> 我们大概没剩下你多少时间了，是吧…… 17:13 < hezekiah> 在我到学校之前都不会有。 17:14 < hezekiah> 等我到了，最少也会有一周没消息，要适应一下。 17:14 < jrand0m> 到了那儿你还得安顿很多事（如果我没记错的话，从我 	 上学时的经历看 ;) 17:14 < jrand0m> 呵，说的也是。 17:14 < hezekiah> 到那时候，我应该会更高效些，也有更多时间能写代 	 码。 17:14 < jrand0m> 酷 17:14 < thecrypto> 我只是在做加密，所以我真正担心的是数据结构， 	 等我把 CTS（密文窃取）模式做完，大概就去搞那个 17:14 < hezekiah> 总之，这是我的预估。 17:14 < jrand0m> 太棒了 thecrypto 17:15 < jrand0m> 好消息是，SDK 跑得很好（mihi 发现的 bug 已经修好 	 了 [yay mihi!]），即使不更新规范也没问题。 17:15 -!- arsenic [~none@anon.iip] 加入了 #iip-dev 17:16 < jrand0m> 好，继续 1.2) i2np 评审 17:16 < jrand0m> 有人看过文档吗？ 17:16 < jrand0m> ;) 17:16 < hezekiah> 还没有。 17:16 < hezekiah> 正如我说的，我目前就像只被砍了头的鸡。 17:17 < hezekiah> 对了 jrand0m，你好像喜欢发 PDF。 17:17 < jrand0m> 大家都能读 openoffice .swx 吗？ 17:17 < hezekiah> 我能。 17:17 < jrand0m> [如果可以，我就发 swx] 17:17 -!- abesimpson [~k@anon.iip] 加入了 #iip-dev 17:17 < thecrypto> 我可以 17:17 < hezekiah> 我在 KGhostView 里不能搜索 PDF 里的文本。 17:17 < hezekiah> 这很要命。 17:17 < jrand0m> 那真糟糕 hezekiah 17:17 -!- mrflibble [mrflibble@anon.iip] 加入了 #iip-dev 17:17 < hezekiah> Linux 版的 Adobe Acrobat 也不太友好。 17:18 < jrand0m> 好，那就用 openoffice 格式，不用 pdf 了。 17:18 < hezekiah> 酷。 17:18 < jrand0m> 嗯，好。I2NP 对 LeaseSet 结构有几点小改动（反映了 	 之前发的 I2CP 更改），除此之外基本就位。 17:19 < hezekiah> jrand0m：这些文档都在 cathedral 的 CVS 里吗？ 17:19 < nop> 哦 17:19 < nop> 我能插句话吗 17:19 < hezekiah> 也就是你发到列表上的那些 PDF 文件的副本之类。 17:19 < hezekiah> nop：请说。 17:19 < nop> 这有点跑题，但很重要 17:19 -!- ChZEROHag [hag@anon.iip] 加入了 #iip-dev 17:19 < nop> IIP-dev 和邮件系统现在有点不太稳定 17:19 < hezekiah> 我注意到了。 17:19 < nop> 所以请大家多包涵一阵 17:20 < nop> 我们正努力把它跑起来 17:20 < nop> 但它内置了 spam assassin 17:20 < nop> 这是好消息 17:20 < nop> :) 17:20 < nop> 还有很多其他功能 17:20 < jrand0m> 有预计时间吗 nop，关于列表？ 17:20  * ChZEROHag 探头打个招呼 17:20 < jrand0m> （我知道你很忙，不是催，就是问问） 17:20 < nop> 希望明天之前 17:20 < jrand0m> 酷 17:20 < nop> 邮件管理员在处理 17:21  * hezekiah 注意到 jrand0m 对 iip-dev 列表是有多么“喜欢”。 ;-) 17:21 < nop> 哈哈 17:21 < hezekiah> Go delta407! 17:21 < nop> 总之 17:21 < jrand0m> 把决策公开记录下来是最好的 hezekiah ;) 17:21 < nop> 回到我们正常的会议 17:21 < jrand0m> 呵 17:21 -!- nop 现在名为 nop_afk 17:21 < hezekiah> jrand0m：我们说到哪了？ 17:21 < jrand0m> 好，回答你的问题 hezekiah> 有些在，但最新的没有。 	 我会改成放 openoffice 格式。 17:21 < jrand0m> 而不是 pdf 17:22 < hezekiah> 好的。 17:22 < hezekiah> 如果所有文档都在 CVS 里就太酷了。 17:22 < jrand0m> 当然，它们会的 17:22 < hezekiah> 那我只要更新，就知道自己拿的是最新版本。 17:22 < jrand0m> （目前有三份草稿还没放上去） 17:22 < hezekiah> （顺便稍微跑题一下，cathedral 是否已经开放匿名 	 访问了？） 17:23 < jrand0m> 还没有。 17:23 < jrand0m> 好的，周五之前，我希望能有一份完整形态的 I2NP 的 	 新草稿【也就是 Kademlia 说明部分不再有 ...，以及示例实现细 	 节】 17:24 < jrand0m> 没有重大改动。只是把说明补得更清楚。 17:24 < hezekiah> 太好了。 17:24 < hezekiah> 里面会提供数据结构的字节布局吗？ 17:24 < jrand0m> 1.3) I2P 轮询 HTTP 传输规范。 17:24 < jrand0m> 不会，字节布局会放在数据结构规范里，而且应该转成 	 标准格式而不是 html 17:25 < jrand0m> （不过 I2NP 已经有所有必要的字节布局） 17:25 < jrand0m> （（如果你读了的话，咳咳 ;) 17:25 < hezekiah> 好的。 17:25 < hezekiah> lol 17:25 < hezekiah> 抱歉啊。 17:25 < hezekiah> 正如我说的，我最近真的很忙。 17:25 < jrand0m> 呵，没关系，你马上就要去上大学了，按理说你该去狂 	 欢的 :) 17:25 < hezekiah> 狂欢？ 17:25 < jrand0m> 好，1.3) I2NP 轮询 HTTP 传输规范 17:25 < hezekiah> 嗯……看来我有点怪。 17:25 < jrand0m> 呵 17:26 < jrand0m> 好，我之前试着发过，很快我会提交。它是一个快速 	 粗糙的传输协议，和 I2NP 配合使用，允许 router 在没有直接连接 	 的情况下来回发送数据（例如防火墙、代理等） 17:27 < jrand0m> 我“希望”有人能看懂它怎么工作，然后构建类似的传 	 输（例如双向 TCP、UDP、直接 HTTP 等） 17:27 -!- mihi [none@anon.iip] 退出 [Ping 超时] 17:27 < hezekiah> 嗯，我不 17:27 < jrand0m> 在把 I2NP 拿出去评审之前，我们需要包含示例传输， 	 这样大家能看到全貌 17:27 < hezekiah> 不觉得我近期会去构建任何传输。;-) 17:27 -!- WinBear_ [~WinBear@anon.iip] 加入了 #iip-dev 17:27 < hezekiah> TCP 在 Java 和 Python 上是可用的。 17:27 < hezekiah> （至少 client-to-router 是。） 17:27 < jrand0m> 没关系，我只是把它列给那些想贡献的人当待办 17:28 < hezekiah> 对。 17:28 < jrand0m> 对，client-router 的需求和 router-router 不一样。 17:28 < jrand0m> 好，继续，1.4) 开发状态 17:28 < jrand0m> thecrypto，CBC 进展如何？ 17:28 < thecrypto> CBC 已提交 17:28 < jrand0m> w00000t 17:28 < thecrypto> CTS 快完成了 17:28 < hezekiah> thecrypto：CTS 是什么？ 17:29 < thecrypto> 我只需要想好如何把它实现得更优雅 17:29 < jrand0m> CTS 就是密文窃取 :) 17:29 < hezekiah> 啊！ 17:29 < thecrypto> CipherText Stealing（密文窃取） 17:29 -!- WinBear [WinBear@anon.iip] 退出 [客户端 EOF] 17:29 < jrand0m> 你看过 nop 提供的参考资料了吗？ 17:29 < hezekiah> 好的。我们会使用 CBC 搭配 CTS，而不是填充。 17:29 < hezekiah> 嗯。 17:29 < thecrypto> 基本上，它能让消息长度恰好合适 17:29 < jrand0m> 这在 Python 那边可行吗 hezekiah？ 17:29 < hezekiah> 我可能得好好“修理”一下我用的那个 Python 加密库， 	 才能让它正确使用 CTS。 17:30 < hezekiah> 我一直更偏好 CTS 而不是填充，但我不知道 PyCrypt 	 是怎么做的。 17:30 < jrand0m> Python 开箱即用地能做什么来实现精确的消息长度还原？ 17:30 < thecrypto> 你只需要改变处理最后两块的方式 17:30 < hezekiah> 我觉得那个库可能要大改一番。 17:30 < hezekiah> jrand0m：Python 里的 CBC 是透明的。你只要把缓冲区 	 传给 AES 对象的加密函数。 17:31 < hezekiah> 它会吐出密文。

17:31 < hezekiah> 事情就这样，讲完了。
17:31 < jrand0m> D(E(data,key),key) == data 吗？逐字节一致，大小也完全相同？
17:31 < hezekiah> 所以如果它脑洞大开用的是 padding（填充）而不是 CTS（密文窃取），我可能得深入它的内部把它修好。
17:31 < jrand0m> （不管输入大小？）
17:31 -!- mihi [~none@anon.iip] 加入了 #iip-dev
17:31 < hezekiah> jrand0m：是的，应该如此。
17:31 < jrand0m> hezekiah> 如果你能看看它具体用的是什么填充算法，那就太好了
17:32 < hezekiah> 好的。
17:32  * jrand0m 犹豫要不要去改一个 Python 加密库，万一这个库已经用了标准且有用的机制
17:32 < hezekiah> 不管怎样，CBC with CTS 听起来不错。
17:32 < hezekiah> jrand0m：这个 Python 加密库简直臭透了。
17:32 < jrand0m> 呵，行
17:33 < thecrypto> 我只需要算一下怎么处理那两个块
17:33 < hezekiah> jrand0m：ElGamal 得用 C 完全重写，才能快到可用。
17:33 < jrand0m> hezekiah> Python 版 elg 处理 256 字节的基准是多少？这个每次目标到目标通信只做一次……
17:34 < jrand0m> （如果你随口就能说的话）
17:34 < hezekiah> 我得测一下。
17:34 < hezekiah> 加密我记得也就一两秒。
17:34 < jrand0m> < 5 秒，< 2 秒，> 10 秒，> 30 秒？
17:34 < thecrypto> 我大概会折腾一下
17:34 < hezekiah> 解密可能在 5 到 10 秒之间。
17:34 < jrand0m> 不错。
17:35 < jrand0m> hezekiah> 你和 jeremiah 谈过吗，或者有没有 Python 客户端 API 的进展消息？
17:35 < hezekiah> thecrypto：你只需要写一个能和 Python 协作的 C 模块就行。
17:35 < hezekiah> 我不知道他最近在忙什么。
17:35 < hezekiah> 我回来之后就没和他联系过。
17:35 < jrand0m> 行
17:35 < jrand0m> 还有其他开发状态方面的想法吗？
17:36 < hezekiah> 嗯，我这边没有。
17:36 < hezekiah> 我已经说了我现在的空闲时间状况。
17:36 < jrand0m> 好的。 明白。
17:36 < hezekiah> 我唯一的计划是把 C API 搭起来，并把 Python router 拉回到符合规范的状态。
17:37 < jrand0m> 行
17:37 < hezekiah> 天哪！
17:37 < jrand0m> 1.4) 待办
17:37 < jrand0m> 是的，先生？
17:37 < hezekiah> 这个 Python 加密库居然没实现 CTS（密文窃取）或填充！
17:37 < hezekiah> 我得手工实现。
17:37 < jrand0m> 嗯？它要求数据长度必须是 16 字节的倍数？
17:37 < hezekiah> 对。
17:38 < jrand0m> 呵
17:38 < jrand0m> 哎，好吧。
17:38 < hezekiah> 目前 Python router 用的是填充。
17:38 < jrand0m> 好。这里有些尚未完成但需要做的事项。
17:38 < hezekiah> 我现在想起来了。
17:38 < hezekiah> 嗯，让
17:38 < hezekiah> 咱们坦白说一件事。
17:38 < hezekiah> Python router 其实从来就不是为了真正使用而做的。
17:39 < hezekiah> 它主要是为了让我非常熟悉规范，同时还能达到另一个目的：
17:39 < hezekiah> 它迫使 Java router _严格_ 遵循规范。
17:39 < jrand0m> 两个目标都很重要。
17:39 < hezekiah> 有时候 Java router 并不完全符合，这时 Python router 就会大声抗议。
17:39 < hezekiah> 所以它并不需要很快或很稳定。
17:39 < jrand0m> 再说我也不确定它将来不会在 SDK 里用到
17:39 < jrand0m> 对。没错。
17:39 < jrand0m> 不过 Python 客户端 API 是另一回事
17:39 < hezekiah> 而 Python 客户端 API 就需要像样一些。
17:40 < jrand0m> 正是。
17:40 < hezekiah> 不过那是 jeremiah 的问题。:)
17:40 < hezekiah> 我把那部分交给他了。
17:40 < jrand0m> SDK 的仅本地 router 只供客户端开发使用
17:40 < jrand0m> lol
17:40 < jrand0m> 好，言归正传…… ;)
17:40 < hezekiah> ;-)
17:41 < jrand0m> - 我们需要有人开始做一个给 i2p 用的小网页，用来发布各种 I2P 相关规范，供同行评审。
17:41 < jrand0m> 我希望能在 9/1 之前准备好。
17:41 < hezekiah> 好的。我现在就声明，你们肯定不想让我来做这个。
17:41 < hezekiah> 我不是个擅长做网页的人。:)
17:41 < jrand0m> 我也不是，如果有人看过我的 flog 就知道了 ;)
17:41 < jrand0m> cohesion？  ;)
17:41 < hezekiah> lol
17:42 < hezekiah> 可怜的 cohesion，总被分配脏活累活。:-)
17:42  * cohesion 正在翻阅聊天记录
17:42 < hezekiah> ;)
17:42 < jrand0m> 呵
17:42 < cohesion> jrand0m：我来做
17:42 < cohesion> me@jasonclinton.com
17:42 < cohesion> 把规范发给我
17:42 < jrand0m> 行，gracias。
17:42 < jrand0m> 规范还没都写完。
17:43 < jrand0m> 但需要放上去的内容包括：
17:43 < cohesion> 行，把你现有的和希望放上的都给我
17:43 < jrand0m> - I2CP 规范、I2NP 规范、Polling HTTP Transport 规范、TCP Transport 规范、安全性分析、性能分析、数据结构规范，以及一个 readme/intro
17:44 < jrand0m> （这 7 个文档会是 PDF 和/或 文本格式）
17:44 < cohesion> 好
17:44 < jrand0m> 除了 readme/intro 之外
17:45 < jrand0m> 我希望这些文档下周（8/26）都能准备好。这样你有足够时间在 9/1 之前整理出一个小页面吗？
17:46 < jrand0m> 好。接下来还需要做的是一个 I2P 网络模拟器。
17:46 < jrand0m> 有人在找计算机课程项目吗？  ;)
17:46 < hezekiah> lol
17:46 < cohesion> jrand0m：可以做
17:47 < hezekiah> 我这还得再过几年才行。 ;-)
17:47 < jrand0m> 不错，cohesion
17:47 < thecrypto> 我还要一年
17:47  * cohesion 回去干活了
17:47 < jrand0m> 谢啦 cohesion
17:48 < jrand0m> 好，1.6）接下来两周。我要把这些规范、文档和分析整理出来。我会尽快 post &amp; commit。
17:48 < jrand0m> 请务必阅读规范并给出意见
17:48 < jrand0m> :)
17:48 < hezekiah> jrand0m：好的。我一有时间就开始看。:)
17:48 < jrand0m> 我更希望大家把评论发到列表，但如果想匿名，就私下把意见发给我，我会匿名把回复贴到列表上。
17:49 < hezekiah> （你觉得把这些文档的 OpenOffice 文件放到 CVS 上的大致时间是？）
17:49 < jrand0m> 会议结束后 10 分钟内我就能提交最新的版本。
17:49 < hezekiah> 太好了。:)
17:50 < jrand0m> 好，1.* 到此结束。
17:50 < jrand0m> 2.x）评论/问题/顾虑/吐槽？
17:50 < jrand0m> mihi，SDK 的修改用得怎么样？
17:51 < jrand0m> 或者其他人呢？  :)
17:51 < hezekiah> jrand0m：你说的这个 SDK 修改是啥？
17:52 < jrand0m> hezekiah> 前几天给 SDK 提交了两个 bug 修复，已经提交（&amp; posted）
17:52 < hezekiah> 啊
17:52 < hezekiah> 不错。
17:52 < jrand0m> （轮换消息ID，同步写入）
17:52 < hezekiah> 只是 Java 这边，还是也包括 Python 那边？
17:52 < jrand0m> 我不会说 Python。
17:53 < hezekiah> lol
17:53 < jrand0m> 不确定那边有没有这些 bug。你是否每 255 条消息轮换一次消息ID，并同步写入？
17:54 < hezekiah> 我想 Python router 这两样都有做
17:54 < jrand0m> 不错。
17:54 < jrand0m> 如果没有的话我们会告诉你的 ;)
17:54 < hezekiah> 你说的“同步写入”具体指什么？
17:55 < jrand0m> 也就是在多个客户端同时尝试向某个客户端发送消息时，确保不会同时把多条消息写给它。
17:55 < hezekiah> 通过 TCP 连接发送的数据都会按产生顺序发送。
17:56 < hezekiah> 所以不会出现先是消息 A 的 1/2，然后是消息 B 的 1/3。
17:56 < jrand0m> 行
17:56 < hezekiah> 你会先收到消息 A，然后是消息 B。
17:56 < hezekiah> 好……如果没人要说话，那我建议我们散会。
17:56 < mihi> 我做的简单 TCP/IP over I2p 似乎能跑了……
17:56 < jrand0m> 太棒了!!
17:56  * mihi 刚才有点挂机，抱歉
17:57 < hezekiah> 还有谁要说点什么吗？
17:57 < jrand0m> mihi> 那我们就能在上面跑 pserver 了？
17:57 < mihi> 只要你别一下子创建特别多的连接就行。
17:57 < mihi> jrand0m：我想可以——我已经能通过它访问 Google 了
17:57 < jrand0m> 不错
17:57 < jrand0m> mihi++
17:57 < mihi> jrand0m-ava
17:57 < jrand0m> 所以你有一个出站代理（outproxy）和一个入站代理（inproxy）？
17:58 < mihi> 没错。
17:58 < jrand0m> 酷
17:58 < mihi> 目的端需要密钥，源端按需生成
17:58  * hezekiah 把 *baf*er 递给 jrand0m。伙计，用完了就把这玩意儿砸了吧。
17:58 < jrand0m> 对。希望等 co 的命名服务准备好后能帮上忙。
17:59 < jrand0m> 好的，太棒了。mihi，如果我们能帮什么忙，告诉我或者任何人就行 :)
17:59 < mihi> 把 128 个消息ID 的那个问题修了，或者做一个更好的“GUARANTEED”支持
17:59  * jrand0m 因为 nop_afk 有真工作而用 *baf* 朝他头上敲了一下
18:00 < mihi> jrand0m：滥用 baf 要付出 20 个 yodels
18:00 < jrand0m> lol
18:00 < jrand0m> 更好的 guaranteed 支持？
18:00 < jrand0m> （也就是比文档里描述的性能更好？我们会在实现里修复）
18:00 < mihi> 你测试过我那个 start_thread=end_thread=300 的用例吗？
18:01 < mihi> 它会单向生成大量消息，结果把所有消息ID 都吃光了……
18:01 < jrand0m> 嗯，没有，还没看到那条信息
18:01 < hezekiah> jrand0m：把消息ID 做成 2 字节是否合理？
18:01  * jrand0m 试过 200 / 201，不过在最新版本里已经修了
18:01 -!- cohesion [cohesion@anon.iip] 退出了 [去参加 LUG 聚会]
18:01 < mihi> 哪个“最新”？
18:01 < hezekiah> 那他们就会有 65535 个消息ID（如果不算 msgid 0 的话）
18:01 < hezekiah> 。
18:02 < jrand0m> 2 字节的消息ID 没坏处。我对这个改动没意见。
18:02 < jrand0m> mihi> 我发邮件给你的那个
18:02 < mihi> 如果你有比发给我更“最新”的，就再发一份（或者给我 CVS 权限）
18:03 < mihi> 嗯，我这在 200/201 的情况下还是失败（300 也一样）
18:03 < jrand0m> 嗯。我再多测测、调调试，把结果发你。
18:03 < mihi> 谢谢。
18:04 < jrand0m> 好。
18:04  * jrand0m 宣布本次会议
18:04 < jrand0m> 已 *baf*
18:04  * hezekiah 恭恭敬敬地把 *baf*er 挂到它的专用架子上。
18:05  * hezekiah 随后转身走出门，随手把门重重关上。baffer 从架子上掉了下来。
18:05 < hezekiah> ;-) --- 日志关闭 Tue Aug 19 18:05:36 2003 </div>
