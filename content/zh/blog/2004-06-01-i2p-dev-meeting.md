---
title: "I2P 开发者会议 - 2004年6月01日"
date: 2004-06-01
author: "duck"
description: "2004年6月1日的 I2P 开发会议记录。"
categories: ["meeting"]
---

## 快速回顾

<p class="attendees-inline"><strong>出席：</strong> deer, duck, hypercubus, Masterboy, mihi, Nightblade, tessier, wilde</p>

## 会议记录

<div class="irc-log"> [22:59] &lt;duck&gt; Tue Jun  1 21:00:00 UTC 2004 [23:00] &lt;duck&gt; 大家好！ [23:00] &lt;mihi&gt; 嗨 duck [23:00] &lt;duck&gt; http://dev.i2p.net/pipermail/i2p/2004-June/000250.html [23:00] &lt;duck&gt; 我的提案： [23:00] * Masterboy 已加入 #i2p

[23:00] &lt;duck&gt; 1) 代码进展
[23:00] &lt;duck&gt; 2) 精选内容
[23:00] &lt;duck&gt; 3) 测试网络状态
[23:00] &lt;duck&gt; 4) 悬赏
[23:00] &lt;duck&gt; 5) ???
[23:00] &lt;Masterboy&gt; 嗨:)
[23:00] &lt;duck&gt; .
[23:01] &lt;duck&gt; 既然 jrandom 不在，我们就得自己来
[23:01] &lt;duck&gt; （我知道他在记录并验证我们的独立性）
[23:01] &lt;Masterboy&gt; 没问题:P
[23:02] &lt;duck&gt; 除非议程有问题，我建议我们就按它来
[23:02] &lt;duck&gt; 不过如果你们不这么做，我也没啥办法 :)
[23:02] &lt;duck&gt; .
[23:02] &lt;mihi&gt; ;)
[23:02] &lt;duck&gt; 1) 代码进展
[23:02] &lt;duck&gt; 提交到 cvs 的代码不多
[23:02] &lt;duck&gt; 我这周确实赢得了奖杯：http://duck.i2p/duck_trophy.jpg
[23:03] * hypercubus 还没有 cvs 账号
[23:03] &lt;Masterboy&gt; 那谁提交了点什么？
[23:03] &lt;duck&gt; 有人在偷偷写代码吗？
[23:03] * Nightblade 加入了 #I2P

[23:03] &lt;hypercubus&gt; BrianR 正在做一些东西
[23:04] &lt;hypercubus&gt; 我大概已经把 0.4 安装程序粗糙地做了 20%。
[23:04] &lt;duck&gt; hypercubus：如果你有东西，就提供 diffs，$dev 会替你提交。
[23:04] &lt;duck&gt; 当然，严格的许可协议仍然适用。
[23:05] &lt;duck&gt; hypercubus：不错，还有什么问题 / 值得一提的事情吗？
[23:06] &lt;hypercubus&gt; 还没有，不过我可能需要几位 BSD 的人来测试预安装程序的 shell 脚本
[23:06] * duck 四处翻找了一下
[23:06] &lt;Nightblade&gt; 它是纯文本的吗
[23:07] &lt;mihi&gt; duck：在 duck_trophy.jpg 里哪个是你？
[23:07] &lt;mihi&gt; ;)
[23:07] &lt;Nightblade&gt; luckypunk 有 freebsd，我的 ISP 也有 freebsd，不过他们的配置有点乱
[23:07] &lt;Nightblade&gt; 我是说我的网站托管的 ISP，不是 Comcast
[23:08] &lt;duck&gt; mihi：戴眼镜的是左边那个。wilde 是右边把奖杯递给我的那位
[23:08] * wilde 挥手
[23:08] &lt;hypercubus&gt; 你可以选择…… 如果你已安装了 java，可以完全跳过预安装程序……    如果你没有安装 java，你可以运行 linux 二进制或 win32 二进制的预安装程序（控制台模式），或者    通用的 *nix 脚本预安装程序（控制台模式）
[23:08] &lt;hypercubus&gt; 主安装程序让你可以选择使用控制台模式或炫酷的 GUI 模式
[23:08] &lt;Masterboy&gt; 我很快会装 freebsd，所以以后我也会试试这个安装程序
[23:09] &lt;hypercubus&gt; 好，太好了……我还不知道除了 jrandom 之外还有没有人在用它
[23:09] &lt;Nightblade&gt; 在 freebsd 上，java 是通过 "javavm" 调用的，而不是 "java"
[23:09] &lt;hypercubus&gt; 是按 Sun 的源码构建的吗？
[23:09] &lt;mihi&gt; freebsd 支持符号链接（symlink） ;)
[23:10] &lt;hypercubus&gt; 总之，二进制预安装程序已经 100% 完成了
[23:10] &lt;hypercubus&gt; 用 gcj 编译成原生可执行程序
[23:11] &lt;hypercubus&gt; 它只会让你输入安装目录，然后会替你获取一个 JRE
[23:11] &lt;duck&gt; 太棒了
[23:11] &lt;Nightblade&gt; 不错
[23:11] &lt;hypercubus&gt; jrandom 正在为 i2p 打包一个定制的 JRE

[23:12] &lt;deer&gt; &lt;j&gt; . [23:12] &lt;Nightblade&gt; 如果你从 FreeBSD ports 集合安装 Java，你会使用一个名为    javavm 的包装脚本 [23:12] &lt;deer&gt; &lt;r&gt; . [23:12] &lt;hypercubus&gt; 总之，这玩意儿会几乎完全自动化 [23:12] &lt;deer&gt; &lt;r&gt; . [23:12] &lt;deer&gt; &lt;r&gt; . [23:12] &lt;deer&gt; &lt;r&gt; . [23:12] &lt;deer&gt; &lt;duck&gt; r: 住手 [23:12] &lt;deer&gt; &lt;r&gt; . [23:12] &lt;deer&gt; &lt;m&gt; . [23:13] &lt;deer&gt; &lt;m&gt; 蠢到爆的 irc 服务器，不支持 pipelining（流水线化） :( [23:13] &lt;duck&gt; hypercubus: 有 ETA（预计完成时间）吗？ [23:14] &lt;deer&gt; &lt;m&gt; 糟了，问题是“Nick change too fast” :( [23:14] &lt;hypercubus&gt; 我仍然预计在不到一个月内完成，在 0.4 成熟到可以发布之前 [23:14] &lt;hypercubus&gt; 不过目前我正在为我的开发系统编译一个新的操作系统，所以    还要几天我才能回到安装器上 ;-) [23:14] &lt;hypercubus&gt; 但别担心 [23:15] &lt;duck&gt; 好的。那下周会有更多消息 :) [23:15] &lt;duck&gt; 还有做其他编码吗？ [23:15] &lt;hypercubus&gt; 但愿吧……除非电力公司又坑我 [23:16] * duck 移动到 #2 [23:16] &lt;duck&gt; * 2) 精选内容 [23:16] &lt;duck&gt; 本周做了很多流媒体音频（ogg/vorbis） [23:16] &lt;duck&gt; baffled 在运行他的 egoplay 流，我也在运行一个流 [23:16] &lt;Masterboy&gt; 而且效果相当不错 [23:17] &lt;duck&gt; 在我们的网站上你可以找到如何使用它的说明 [23:17] &lt;hypercubus&gt; 有大致的统计数据给我们吗？ [23:17] &lt;duck&gt; 如果你使用了那上面未列出的播放器，并摸索出如何使用的方法，请发给我，我会加上 [23:17] &lt;Masterboy&gt; duck 你的网站上 baffled 的流的链接在哪里？ [23:17] &lt;Masterboy&gt; :P [23:17] &lt;duck&gt; hypercubus: 4kB/s 表现还不错 [23:18] &lt;duck&gt; 用 ogg 也不算太糟 [23:18] &lt;hypercubus&gt; 但这看起来仍然是平均速度？ [23:18] &lt;duck&gt; 我的观察是，那就是上限 [23:18] &lt;duck&gt; 不过这全靠配置调优 [23:19] &lt;hypercubus&gt; 知道为什么那似乎是上限吗？ [23:19] &lt;hypercubus&gt; 而且我说的不只是流媒体 [23:19] &lt;hypercubus&gt; 还有下载 [23:20] &lt;Nightblade&gt; 我昨天从 duck 的托管服务下载了一些大文件（几兆字节），速度也大约是 4kb-5kb [23:20] &lt;duck&gt; 我认为是 rtt（往返时延） [23:20] &lt;Nightblade&gt; 就是那些 Chips 电影 [23:20] &lt;hypercubus&gt; 4-5 似乎比我自从开始使用 i2p 以来一直稳定得到的约 ~3 有所改善

[23:20] &lt;Masterboy&gt; 4-5kb 不错了..
[23:20] &lt;duck&gt; windowsize 为 1 的情况下，你不会快多少..
[23:20] &lt;duck&gt; windowsize&gt;1 悬赏：http://www.i2p.net/node/view/224
[23:21] &lt;duck&gt; mihi：也许你可以评论一下？
[23:21] &lt;hypercubus&gt; 但它惊人地稳定在 3 kbps
[23:21] &lt;mihi&gt; 关于什么？在 ministreaming 下把 windowsize&gt;1：如果你能做到你就是个法师 ;)
[23:21] &lt;hypercubus&gt; 带宽计上没有卡顿……一条相当平滑的曲线
[23:21] &lt;duck&gt; mihi：关于为什么它能稳定在 4kb/s
[23:21] &lt;mihi&gt; 不知道。我听不到任何声音 :(
[23:22] &lt;duck&gt; mihi：对于所有 i2ptunnel 传输
[23:22] &lt;Masterboy&gt; mihi 你需要配置 ogg 流媒体插件..
[23:22] &lt;mihi&gt; Masterboy：？
[23:23] &lt;mihi&gt; 不，i2ptunnel 内部对速度没有限制。那一定是在 router 里...
[23:23] &lt;duck&gt; 我的想法：最大包大小：32kB，5 秒 rtt：32kB/5s =~ 6.5kb/s
[23:24] &lt;hypercubus&gt; 聊起来有道理
[23:25] &lt;duck&gt; 好的..
[23:25] &lt;duck&gt; 其他内容：
[23:25] * hirvox 加入了 #i2p

[23:25] <duck> Naughtious 有了一个新的 eepsite
[23:25] <duck> anonynanny.i2p
[23:25] <duck> 密钥已经提交到 cvs，而且他把它放在 ugha 的 wiki 上了
[23:25] * mihi 正在听 “sitting in the ...” - duck++
[23:25] <Nightblade> 试试看能不能以 4kb 的速度打开两三个 stream，这样你就能判断问题是在 router 里还是在 streaming 库里
[23:26] <duck> Naughtious：你在吗？说说你的计划吧 :)
[23:26] <Masterboy> 我读到他说他提供托管
[23:26] <duck> Nightblade：我试过从 baffled 做 3 个并行下载，每个都有 3-4kB
[23:26] <Nightblade> 我懂了
[23:27] <mihi> Nightblade：那你怎么判断的？
[23:27] * mihi 喜欢用 “stop&go” 模式听 ;)
[23:27] <Nightblade> 嗯，如果 router 里有某种限制只能一次处理 4kb
[23:27] <Nightblade> 或者是别的问题
[23:28] <hypercubus> 有人能解释一下这个 anonynanny 站吗？我现在没有运行中的 i2p router
[23:28] <mihi> hypercubus：就是个 wiki 或类似的东西
[23:28] <duck> plone CMS 的部署，开放注册
[23:28] <duck> 允许文件上传和网站相关内容
[23:28] <duck> 通过 Web 界面
[23:28] <Nightblade> 另一件可以做的事是测试 “repliable datagram（可回复的数据报）” 的吞吐量，据我所知（afaik）它和 stream 是一样的，只是没有确认（acks）
[23:28] <duck> 跟 drupal 很像
[23:28] <hypercubus> 对，我以前跑过 plone
[23:29] <duck> Nightblade：我一直在考虑用 Airhook 来管理这些
[23:29] <duck> 但目前只有一些基本想法
[23:29] <hypercubus> wiki 内容是随意的，还是聚焦某个主题？
[23:29] <Nightblade> 我想 Airhook 是 GPL 授权的
[23:29] <duck> 我说的是协议
[23:29] <duck> 不是代码
[23:29] <Nightblade> 啊 :)
[23:30] <duck> hypercubus：他想要高质量内容，而且让你来提供 :)
[23:30] <Masterboy> 把你自己最好的 pr0n 传上去吧 hyper;P
[23:30] <duck> 好吧
[23:30] * Masterboy 也会试试这么做
[23:30] <hypercubus> 是啊，任何人跑一个开放的 wiki 都是在呼唤高质量内容 ;-)
[23:31] <duck> 好吧
[23:31] * duck 移动到 #3
[23:31] <duck> * 3) 测试网络状态
[23:31] <Nightblade> “Airhook 能优雅地处理间歇性、不可靠或延迟的网络”  <-- 呵呵，对 I2P 的描述不太乐观！
[23:31] <duck> 最近情况如何？
[23:32] <duck> 把关于把数据报跑在 i2p 之上的讨论放到最后
[23:32] <tessier> 我喜欢跑到开放的 wiki 上贴这个链接：http://www.fissure.org/humour/pics/squirre   l.jpg
[23:32] <tessier> airhook 很赞
[23:32] <tessier> 我也在考虑用它来构建一个 P2P 网络
[23:32] <Nightblade> 在我看来很可靠（#3）
[23:32] <Nightblade> 是我见过的最佳状态
[23:33] <duck> 是啊
[23:33] <mihi> 运行很好——至少对于 stop&go 音频流
[23:33] <duck> 我在 irc 上看到的在线时长很可观
[23:33] <hypercubus> 同意……在我的 router 控制台里看到更多蓝色小人了
[23:33] <Nightblade> mihi：你在听 techno 吗？:)
[23:33] <duck> 但很难判断，因为 bogobot 似乎无法处理跨过 00:00 的连接
[23:33] <tessier> 对我来说音频流非常好，但加载网站经常要多试几次
[23:33] <Masterboy> 我觉得 i2p 跑 6 小时后非常好用，在第 6 个小时我用了 irc 7 小时，所以我的 router 总共跑了 13 小时
[23:33] <duck> （*提示*）
[23:34] <hypercubus> duck：呃……呵呵
[23:34] <hypercubus> 我想我能修
[23:34] <hypercubus> 你的日志是按天设置的吗？
[23:34] <duck> hypercubus++
[23:34] <hypercubus> 日志轮换是说
[23:34] <duck> 哦是的
[23:34] <duck> duck--
[23:34] <hypercubus> 那就是原因
[23:34] <Nightblade> 我一整天都在上班，回家开了电脑启动 i2p，几分钟后就上了 duck 的 irc 服务器
[23:35] <duck> 我碰到一些奇怪的 DNF
[23:35] <duck> 就算连接我自己的 eepsite 也会这样
[23:35] <duck> (http://dev.i2p.net/bugzilla/show_bug.cgi?id=74)
[23:35] <duck> 我觉得这就是现在导致大多数问题的原因
[23:35] <hypercubus> bogoparser 只会分析完全包含在单个日志文件中的在线时长……所以如果日志文件只覆盖 24 小时，就不会有人显示为连接超过 24 小时
[23:35] <duck> 我想 Masterboy 和 ughabugha 也遇到过……
[23:36] <Masterboy> 是的
[23:36] <duck> （修好它你肯定会赢下周的奖杯！）
[23:37] <deer> <mihi> bogobot 很兴奋？;)
[23:37] <Masterboy> 我试我的网站，有时候我点刷新它就走另一条路由？然后我得等它加载，但我从不等；P 我再点一次就立刻出来了
[23:37] <deer> <mihi> 哎呀，抱歉。忘了这是有网关的……
[23:38] <duck> Masterboy：超时时间是 61 秒吗？
[23:39] <duck> mihi：bogobot 现在设为每周轮换
[23:39] * mihi 已退出 IRC（“再见，祝会议愉快”）
[23:40] <Masterboy> 抱歉我没在我的网站上检查，当我不能立刻连上时我就点刷新，然后它就立刻出来了……
[23:40] <duck> 嗯
[23:40] <duck> 总之需要修
[23:41] <duck> .... #4
[23:41] <Masterboy> 我觉得每次给的路由都不一样
[23:41] <duck> * 4) 悬赏
[23:41] <duck> Masterboy：本地连接应该被缩短
[23:42] <duck> wilde 对悬赏有些想法……你在吗？
[23:42] <Masterboy> 也许是对等体选择的 bug
[23:42] <wilde> 我不确定这是不是该进议程的
[23:42] <duck> 哦
[23:42] <wilde> 好吧，想法大概是：
[23:42] <Masterboy> 我觉得等我们公开后，悬赏系统会更好用
[23:43] <Nightblade> masterboy：是的，每个连接都有两个 tunnel，至少我从读 router.config 的理解是这样
[23:43] <wilde> 我们可以用这一个月做一些小范围的 i2p 宣传，把悬赏池多积累一点
[23:43] <Masterboy> 我能看到 Mute 项目进展不错——他们拿到了 600$，但他们还没写多少代码呢；P
[23:44] <wilde> 目标对准自由社群、密码学圈等
[23:44] <Nightblade> 我觉得 jrandom 不想要宣传
[23:44] <wilde> 不是那种公开的 Slashdot 级别关注，不
[23:44] <hypercubus> 我观察到的也是这样
[23:44] <Masterboy> 我想再推一把——等我们公开后系统会好很多；P
[23:45] <wilde> Masterboy：悬赏可以加快 myi2p 的开发，比如说
[23:45] <Masterboy> 而且正如 jr 所说，1.0 之前不公开，0.4 之后才会有点关注
[23:45] <Masterboy> *写道
[23:45] <wilde> 如果某个悬赏有 $500+，人们实际上可以撑几个星期
[23:46] <hypercubus> 棘手的是，即便我们只针对一个小的开发者群体，比如说咳 Mute 的开发者，那些家伙可能会把 i2p 的消息传播得比我们希望的更广
[23:46] <Nightblade> 有人可以靠修 i2p 的 bug 谋生了
[23:46] <hypercubus> 而且传播得太早
[23:46] <wilde> i2p 的链接已经在很多公共地方出现了
[23:46] <Masterboy> 你用 google 就能找到 i2p

[23:47] &lt;hypercubus&gt; 偏僻的公共场所 ;-)（我是在一个 freesite（Freenet 上的网站）上看到那个 I2P 链接的... 我很走运，那个该死的 freesite 居然还加载出来了！）
[23:47] &lt;wilde&gt; http://en.wikipedia.org/wiki/I2p
[23:47] &lt;Masterboy&gt; 但我同意在 0.4 完成之前不要做宣传
[23:47] &lt;Masterboy&gt; 啥？？？？？
[23:47] &lt;wilde&gt; http://www.ovmj.org/GNUnet/links.php3?xlang=English
[23:48] &lt;Masterboy&gt; protol0l 做得很棒；P
[23:48] &lt;Masterboy&gt; ;))))))
[23:48] &lt;hypercubus&gt; 好个笔误 ;-)
[23:48] &lt;wilde&gt; 不管怎样，我同意我们仍然应该保持 I2P 低调（jr 看看这份日志 ;)
[23:49] &lt;Masterboy&gt; 谁干的？
[23:49] &lt;Masterboy&gt; 我觉得 Freenet 团队的讨论引起了更多关注..
[23:50] &lt;Masterboy&gt; 而且 jr 和 toad 的讨论也给了大众很多信息..
[23:50] &lt;Masterboy&gt; 所以，就像 ugh 的 wiki 里说的——这事我们都可以怪 jr；P
[23:50] &lt;wilde&gt; 好吧，总之，我们看看能不能在不引来 /. 的情况下弄到点儿钱
[23:50] &lt;Masterboy&gt; 同意
[23:50] &lt;hypercubus&gt; Freenet 开发者列表可算不上我所谓的“大众” ;-)
[23:50] &lt;wilde&gt; .
[23:51] &lt;hypercubus&gt; wilde：你会比想象中更快拿到很多 $
[23:51] &lt;wilde&gt; 得了吧，就连我妈都订阅了 freenet-devl
[23:51] &lt;duck&gt; 我妈是通过 gmame 看的
[23:51] &lt;deer&gt; &lt;clayboy&gt; 这里的学校都在教 freenet-devl
[23:52] &lt;wilde&gt; .
[23:52] &lt;Masterboy&gt; 那么等我们到 0.4 稳定版后会看到更多悬赏..
[23:53] &lt;Masterboy&gt; 也就是再过 2 个月；P
[23:53] &lt;wilde&gt; 那只 duck 去哪儿了？
[23:53] &lt;duck&gt; 谢谢，wilde
[23:53] &lt;hypercubus&gt; 不过，作为迄今唯一的悬赏领取者，我得说赏金并没有影响我接受这个挑战的决定
[23:54] &lt;wilde&gt; 呵呵，要是多 100 倍就会了
[23:54] &lt;duck&gt; 你对这个世界来说太好了
[23:54] &lt;Nightblade&gt; 哈哈
[23:54] * duck 移动到 #5
[23:54] &lt;hypercubus&gt; wilde，100 美元对我来说算不了什么 ;-)
[23:54] &lt;duck&gt; 100 * 10 = 1000
[23:55] * duck pops("5 airhook")
[23:55] &lt;duck&gt; tessier：对它有任何实战经验吗
[23:55] &lt;duck&gt; (http://www.airhook.org/)
[23:55] * Masterboy 打算试试这玩意:P
[23:56] &lt;duck&gt; Java 实现（不确定它现在还能不能用） http://cvs.ofb.net/airhook-j/
[23:56] &lt;duck&gt; Python 实现（很乱，过去是能用的） http://cvs.sourceforge.net/viewcvs.py/khashmir   /khashmir/airhook.py
[23:58] * duck 打开了吐槽阀门
[23:58] &lt;Nightblade&gt; j 的那个也是 GPL
[23:58] &lt;duck&gt; 把它改成公有领域
[23:58] &lt;hypercubus&gt; 阿门
[23:58] &lt;Nightblade&gt; 整个协议文档只有大约 3 页——应该不会那么难
[23:59] &lt;Masterboy&gt; 没有什么是难的
[23:59] &lt;Masterboy&gt; 只是没那么容易
[23:59] &lt;duck&gt; 不过我觉得它的规格还不完整
[23:59] * hypercubus 把 masterboy 的幸运饼干没收了
[23:59] &lt;duck&gt; 你可能需要深入 C 代码，把它当作参考实现
[00:00] &lt;Nightblade&gt; 我本来会亲自做，但我现在正忙于其他 i2p 的事情
[00:00] &lt;Nightblade&gt; （还有我的全职工作）
[00:00] &lt;hypercubus&gt; duck：也许可以为它设个悬赏？
[00:00] &lt;Nightblade&gt; 已经有了
[00:00] &lt;Masterboy&gt; ?
[00:00] &lt;Masterboy&gt; 啊，Pseudonyms
[00:00] &lt;duck&gt; 它可以在两个层面上使用
[00:00] &lt;duck&gt; 1）作为除 TCP 之外的一种传输方式
[00:01] &lt;duck&gt; 2）作为在 i2cp/sam 内部处理数据报的协议
[00:01] &lt;hypercubus&gt; 那就值得认真考虑了
[00:01] &lt;hypercubus&gt; &lt;/obvious&gt;

[00:02] &lt;Nightblade&gt; duck: 我注意到 SAM 中的可回复数据报最大为 31kb，而 stream 最大为 32kb——这让我觉得在可回复数据报模式下，每个数据包都会附带发送者的 destination（目的地标识），而在 stream 模式下只在开始时发送——
[00:02] &lt;Masterboy&gt; 嗯，airhook 的 CVS 更新不太及时..
[00:03] &lt;Nightblade&gt; 这让我觉得通过 SAM 在可回复数据报之上再做一个协议会很低效
[00:03] &lt;duck&gt; airhook 的消息大小是 256 字节，I2CP 的是 32kb，所以你至少需要改动一点
[00:04] &lt;Nightblade&gt; 其实如果你想在 SAM 里做这个协议，你可以直接用匿名数据报，并让第一个包包含发送者的 destination.... 等等等等 - 我有很多想法，但没有足够的时间去写代码
[00:06] &lt;duck&gt; 但另一方面，你还会遇到验证签名的问题
[00:06] &lt;duck&gt; 所以可能有人会给你发假包
[00:06] &lt;Masterboy&gt; 主题:::: SAM
[00:06] &lt;Masterboy&gt; ;P
[00:07] &lt;Nightblade&gt; 没错
[00:08] &lt;Nightblade&gt; 但如果你回发到那个 destination，而没有收到确认（acknowledgement），你就知道那是个冒牌货
[00:08] &lt;Nightblade&gt; 那就必须有一个握手
[00:08] &lt;duck&gt; 但为此你需要应用层的握手
[00:08] &lt;Nightblade&gt; 不，并不一定
[00:09] &lt;Nightblade&gt; 把它放到一个用于访问 SAM 的库里就行
[00:09] &lt;Nightblade&gt; 不过那是个不太好的做法
[00:09] &lt;Nightblade&gt; 这样做
[00:09] &lt;duck&gt; 你也可以使用分离的 tunnel（通道）
[00:09] &lt;Nightblade&gt; 它应该在 streaming 库里
[00:11] &lt;duck&gt; 对，讲得通
[00:12] &lt;duck&gt; 好
[00:12] &lt;duck&gt; 我感觉有点*baff*-y
[00:13] &lt;Nightblade&gt; 嗯
[00:13] * duck *baffs* </div>
