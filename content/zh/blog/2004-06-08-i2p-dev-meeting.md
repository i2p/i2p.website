---
title: "I2P 开发者会议 - 2004年6月8日"
date: 2004-06-08
author: "duck"
description: "2004年6月8日的 I2P 开发会议记录。"
categories: ["meeting"]
---

## 快速回顾

<p class="attendees-inline"><strong>出席：</strong> cervantes, deer, duck, fvw, hypercubus, mihi, Nightblade, Sonium, ugha_node</p>

## 会议记录

<div class="irc-log"> 21:02:08 &lt;duck&gt; Tue Jun  8 21:02:08 UTC 2004 21:02:21 &lt;duck&gt; 到开会时间了 21:02:33 &lt;duck&gt; 文章在 http://dev.i2p.net/pipermail/i2p/2004-June/000268.html 21:02:39 &lt;duck&gt; 不过我在编号上确实犯了个错误 21:02:45 &lt;duck&gt; 所以第一个编号为 5 的条目将被跳过 21:02:53 &lt;hypercubus&gt; 耶！ 21:03:03  * duck 往他的啤酒里加了些冰 21:03:14  * mihi 想把第一个 #5 改成 #4 ;) 21:03:27 &lt;hypercubus&gt; 算了，我们下周就有两个第4项吧 ;-) 21:03:37  * duck 把 'hypercubus' 改名为 'mihi' 21:03:48 &lt;hypercubus&gt; 耶！ 21:03:49 &lt;duck&gt; 好 21:03:53 &lt;duck&gt; * 1) libsam 21:04:02 &lt;duck&gt; 频道里有 Nightblade 吗？ 21:04:39 &lt;duck&gt; (空闲     ：0 天 0 小时 0 分 58 秒) 21:05:03 &lt;hypercubus&gt; ;-) 21:05:53  * duck 重新拿回麦克风 21:06:15 &lt;duck&gt; Nightblade 为 C / C++ 写了一个 SAM 库 21:06:23 &lt;duck&gt; 我这边能编译通过……不过我只能说到这儿了 :) 21:06:37 &lt;mihi&gt; 没有测试用例吗？ ;) 21:07:06 &lt;duck&gt; 如果有任何 rFfreebsd 用户，Nightblade 可能会对你感兴趣 21:07:08 &lt;ugha_node&gt; 代码里对 strstr 的调用真让我恼火。 ;) 21:07:27 &lt;ugha_node&gt; duck：什么是 rFfreebsd？ 21:07:42 &lt;duck&gt; 就是我把 freebsd 打成那样了 21:08:00 &lt;mihi&gt; rm -rF freebsd? 21:08:29 &lt;ugha_node&gt; 可惜 -F 在 rm 里不起作用。 21:08:30 &lt;duck&gt; ugha_node：它是 bsd 许可的；所以修一下吧 21:08:41 &lt;fvw&gt; 听起来很靠谱 :). 可惜我前阵子把我最后一台 freebsd 机器卸掉了。我                  在别人机器上也有账号，并且愿意运行测试用例。 21:08:43 &lt;ugha_node&gt; duck：我可能会的。 :) 21:08:50 &lt;duck&gt; (该死的 BSD 嬉皮士) 21:09:09 &lt;duck&gt; 哦，简洁明了，frank 21:09:17 &lt;duck&gt; 还有关于 libsam 的评论吗？ 21:09:49 &lt;duck&gt; fvw：我想如果他有需要，Nightblade 会联系你 21:09:50  * fvw 咕哝着，抱怨那种完全合理的 unix 行为居然把他的 irc 客户端干掉了。 21:10:02 &lt;duck&gt; 不过因为他的邮件是一周前的了，他可能已经找到了一些东西 21:10:17 &lt;mihi&gt; fvw：？ 21:10:24 &lt;fvw&gt; 是啊，如果有人想接受我的提议，我好像错过了。尽管                  给我发邮件或什么的。 21:10:42  * duck 跳到 #2 21:10:46 &lt;hypercubus&gt; 呃，跳到哪里？ ;-) 21:10:54 &lt;duck&gt; 2) 用一个浏览器同时浏览 i2p 和普通 Web 21:10:57 &lt;fvw&gt; 刚装好系统，还没告诉我的 zsh 不要在后台 hup 东西。                  &lt;/offtopic&gt;

21:11:09 &lt;fvw&gt; hypercubus：我想我在公共用户邮件列表上。fvw.i2p@var.cx
21:12:11 &lt;duck&gt; 有些内容是关于把所有顶级域名（TLD）添加到你的浏览器代理忽略列表里
21:12:23 &lt;fvw&gt; 那个需要讨论吗？我觉得在                  邮件列表上基本已经处理了。
21:12:24 &lt;duck&gt; 我觉得这是个很粗陋的权宜之计
21:12:36 &lt;fvw&gt; 是的，那已经提到过了。欢迎回来。
21:12:47 &lt;duck&gt; fvw：我没看那个讨论串 :)
21:13:12 &lt;duck&gt; 好吧，如果你不想讨论这个，就跳到 #3
21:13:19 &lt;duck&gt; * 3) 聊天频道
21:13:23 &lt;hypercubus&gt; cervantes 的脚本在 Konqueror 3.2.2、Firefox 0.8 和                         Opera 7.51 上运行得非常好，都是 Gentoo 搭配 KDE 3.2.2
21:13:39  * mihi 在 #4 做了标记
21:13:55 &lt;duck&gt; #i2p-chat 是这里用于离题闲聊和轻量支持的备用频道
21:14:08 &lt;duck&gt; 我不知道是谁注册的
21:14:12 &lt;hypercubus&gt; 是我
21:14:17 &lt;duck&gt; 那最好小心点 :)
21:14:22 &lt;fvw&gt; 呃，这里没有 #4，只有两个 #5 :)
21:14:33 &lt;hypercubus&gt; 要是需要的时候我还能记得密码就算走运了 ;-)
21:14:33 &lt;mihi&gt; [22:27] -ChanServ-      频道: #i2p-chat
21:14:33 &lt;mihi&gt; [22:27] -ChanServ-      联系人: hypercubus &lt;&lt;在线&gt;&gt;

21:14:33 &lt;mihi&gt; [22:27] -ChanServ-    备用：cervantes &lt;&lt;ONLINE&gt;&gt; 21:14:37 &lt;mihi&gt; [22:27] -ChanServ-   注册于：4天前（0小时2分41秒） 21:15:12 &lt;hypercubus&gt; 我把 op 权限给了几个信任的人，以便我不在的时候遇到麻烦可以处理 21:15:24 &lt;duck&gt; 听起来不错 21:15:39 &lt;duck&gt; 可能有点小题大做 21:15:51 &lt;hypercubus&gt; 在 IRC 上你永远不知道会发生什么 ;-) 21:15:55 &lt;duck&gt; 不过在那个 protogirl 加入这里之后，我觉得清理一下这个频道会比较好 21:16:03 &lt;hypercubus&gt; 呵 21:16:27 &lt;hypercubus&gt; 反正接下来几个月某个时候我们肯定会需要它 21:16:34 &lt;duck&gt; 嗯 21:16:48 &lt;duck&gt; 然后 freenode 的人就会把我们踢出去  21:16:55 &lt;hypercubus&gt; ;-) 21:17:13 &lt;duck&gt; 他们不喜欢任何不写进他们‘kampf’里的东西 21:17:16 &lt;duck&gt; 呃 21:17:44  * duck 移动到 $nextitem 并触发了 mihi 的断点 21:17:47 &lt;hypercubus&gt; 我想把新频道和支持（support）挂钩，会让它在 freenode 看来更名正言顺 21:18:47 &lt;duck&gt; hypercubus: 你可能会吃惊 21:19:04 &lt;hypercubus&gt; *咳* 我得承认我没把所有政策都读完... 21:19:24 &lt;duck&gt; 这就是俄罗斯轮盘赌 21:19:39 &lt;hypercubus&gt; 嗯，没想到会这么严重 21:19:52  * duck 正在消极发言 21:19:54 &lt;hypercubus&gt; 好吧，我会研究一下我们能做什么 21:20:09 &lt;fvw&gt; 抱歉，我肯定漏了什么。为什么 freenode 会把我们踢走？ 21:20:21  * duck 看了看 mihi 的断点的超时计数器 21:20:32 &lt;duck&gt; fvw: 他们更专注于开发相关的频道 21:20:35 &lt;mihi&gt; ？ 21:20:53 &lt;mihi&gt; duck: 这个断点会在 /^4).*/ 上触发 21:21:01 &lt;duck&gt; mihi: 但是没有 #4 21:21:06 &lt;fvw&gt; 那又怎样？I2P 还处在非常早期的 alpha 阶段，现在连支持（support）都算开发。 21:21:11 &lt;fvw&gt; （不，你不能引用我的这句话） 21:21:36 &lt;duck&gt; fvw: 你可能不熟悉之前在 IIP 上发生的那些讨论类型 21:21:38 &lt;hypercubus&gt; 是啊，但我们有 *2* 个频道来做这个 21:21:45 &lt;duck&gt; 而且这些很可能会发生在 #i2p 频道里 21:22:04 &lt;duck&gt; 我很确定 freenode 不会喜欢那样。 21:22:10 &lt;Nightblade&gt; 我现在在了 21:22:49 &lt;hypercubus&gt; 我们给他们捐一台玛格丽塔鸡尾酒机什么的 21:22:49 &lt;mihi&gt; duck: 你指的是什么？刷屏？还是 #cl？还是啥？ 21:23:08 &lt;fvw&gt; 是在 IIP 上的讨论还是在 #iip 上的讨论？我在 #iip 上从没见过除了开发（devel）和支持（support）之外的内容。而且在 IIP 上的讨论会转移到 I2P，而不是 #i2p@freenode。 21:23:09 &lt;duck&gt; 各种不政治正确的言论 21:23:36 &lt;fvw&gt; 还有玛格丽塔鸡尾酒机？噢，我也想要。 21:23:54 &lt;duck&gt; 哎呀算了 21:24:38 &lt;hypercubus&gt; 我们要重新讨论一下 2) 吗？ 21:24:58 &lt;duck&gt; hypercubus: 关于浏览器代理你还有什么要补充的吗？ 21:25:18 &lt;hypercubus&gt; 哎呀，是第 1 项……既然 Nightblade 刚刚莅临 ;-) 21:25:33 &lt;duck&gt; Nightblade: 我们擅自‘讨论’了 libsam 21:25:42 &lt;Nightblade&gt; 好，我说几句 21:25:48 &lt;hypercubus&gt; 不过对，关于浏览器那事我想起来还有件没在邮件列表里提到的 21:25:56 &lt;duck&gt; Nightblade: fvw 说他也许能帮忙做一些 FreeBSD 的测试 21:26:20 &lt;fvw&gt; 我不再有 FreeBSD 机器了，但我在一些 FreeBSD 机器上有账号，给我测试用例，我很乐意跑一跑。 21:27:02 &lt;Nightblade&gt; 我已经开始做一个 C++ 的 DHT，使用的是 Libsam（C）。目前虽然我花了不少功夫，但进展还不是特别大。现在 DHT 里的节点可以通过 SAM 数据消息互相“ping” 21:27:09 &lt;Nightblade&gt; 在这个过程中我发现了 libsam 里的几个小 bug 21:27:18 &lt;Nightblade&gt; 我之后会发布一个新版本 21:27:51 &lt;ugha_node&gt; Nightblade: 能不能把 libsam 里那些‘strstr’调用去掉？ :) 21:27:52 &lt;Nightblade&gt; 测试用例是：尝试编译它，然后把错误报告给我 21:28:01 &lt;Nightblade&gt; strstr 有什么问题？ 21:28:21 &lt;ugha_node&gt; 它并不是用来替代 strcmp 的。 21:28:38 &lt;Nightblade&gt; 哦对了，我还准备把 libsam 移植到 Windows，不过这不是近期的事 21:29:07 &lt;Nightblade&gt; 除了审美之外，我现在的用法有什么问题吗？ 21:29:15 &lt;Nightblade&gt; 你可以把修改发给我，或者告诉我你更想怎么做 21:29:19 &lt;Nightblade&gt; 那只是看起来是最简单的办法 21:29:21 &lt;ugha_node&gt; Nightblade: 我没注意到有什么。 21:29:32 &lt;fvw&gt; 当然，strcmp 比 strstr 更高效。 21:29:36 &lt;ugha_node&gt; 不过我只是粗略看了一下。 21:30:20 &lt;ugha_node&gt; fvw: 你有时可以利用把 strstr 当成 strcmp 来用的代码进行攻击，但这里不是那种情况。 21:31:22 &lt;Nightblade&gt; 嗯，我现在看到有些地方可以改了 21:31:28 &lt;fvw&gt; 那也是，不过我想你会注意到这一点。嗯，实际上你得用 strncmp 才能防止那类利用。但这不是重点。 21:31:31 &lt;Nightblade&gt; 我不记得为什么当时那么做了 21:31:57 &lt;ugha_node&gt; fvw: 我同意。 21:32:27 &lt;Nightblade&gt; 哦我想起来为什么了 21:32:40 &lt;Nightblade&gt; 那是个偷懒的做法，这样就不用去算给 strncmp 的长度了 21:32:49 &lt;duck&gt; 呵 21:32:52 &lt;ugha_node&gt; Nightblade: 呵呵。 21:33:01 &lt;fvw&gt; 用 min(strlen(foo), sizeof(*foo)) 21:33:04 &lt;hypercubus&gt; 要开始惩罚了吗？ 21:33:15 &lt;fvw&gt; 我以为该先来口交？*低头躲* 21:33:32 &lt;fvw&gt; 好吧，我想该下一个议题了。Hypercube 对代理这块有评论？ 21:33:38 &lt;hypercubus&gt; 呵 21:33:54 &lt;duck&gt; 放马过来！ 21:34:03 &lt;Nightblade&gt; 我会在下个版本里做出修改——至少改一部分 21:34:25 &lt;hypercubus&gt; 好，这个几周前在频道里简短讨论过，但我觉得值得再谈一次 21:34:48 &lt;deer&gt; * Sugadude 自愿来进行口交。 21:34:59 &lt;hypercubus&gt; 与其把 TLD 加到浏览器的阻止列表里，或者使用代理脚本，还有第三种办法 21:35:29 &lt;hypercubus&gt; 就匿名性而言，它不该有前两种方法的那些缺点 21:36:17 &lt;fvw&gt; 你要以只要$29.99的超低价告诉我们吗？快说吧！ 21:36:27 &lt;hypercubus&gt; 那就是让 eeproxy 重写传入的 HTML 页面，把页面嵌进一个 frameset 里……   21:36:58 &lt;hypercubus&gt; 主框架包含请求的 HTTP 内容，另一个框架作为控制条 21:37:13 &lt;hypercubus&gt; 并允许你随时开启/关闭代理 21:37:40 &lt;hypercubus&gt; 并且还会提醒你（比如通过彩色边框或其他提示方式）你正在非匿名地浏览 21:37:54 &lt;fvw&gt; 你打算怎样防止一个 I2P 站点（带 JavaScript 等）把匿名性给关掉？ 21:37:59  * duck 试图应用 jrandom-skill-level-of 的容忍度 21:37:59 &lt;hypercubus&gt; 或者 eepsite 页面中的某个链接指向 RealWeb(tm) 21:38:04 &lt;duck&gt; 酷！做吧！ 21:38:16 &lt;fvw&gt; 你还是得做点类似 fproxy 的东西，或者做个不受浏览器控制的切换机制。 21:38:29 &lt;ugha_node&gt; fvw: 对。 21:39:10 &lt;hypercubus&gt; 这就是我又把这个话题抛出来的原因，也许有人会有如何保障其安全性的点子 21:39:31 &lt;hypercubus&gt; 但在我看来，这对大多数 I2P 终端用户来说将是非常需要的东西 21:39:33 &lt;hypercubus&gt; *用户 21:40:04 &lt;hypercubus&gt; 因为 TLD/代理脚本/专用浏览器 这些做法对普通网民来说要求太高了 21:40:29 &lt;fvw&gt; 从长期看，我觉得做一个类似 fproxy 的东西是最好的思路。但在我看来这绝对不是当务之急，而且我其实也不认为浏览网站会是 I2P 的杀手级应用。 21:40:42 &lt;Sonium&gt; netDb 到底是什么？ 21:40:59 &lt;duck&gt; Sonium: 已知 router 的数据库 21:41:10 &lt;hypercubus&gt; 对大多数用户来说 fproxy 太麻烦了 21:41:32 &lt;Sonium&gt; 这样的数据库不会损害匿名性吗？ 21:41:39 &lt;hypercubus&gt; 我认为这是 freenet 在非开发者社区里一直没流行起来的部分原因 21:41:41 &lt;fvw&gt; hypercube: 不一定。代理自动配置（“PAC”）可以让它简单到只需在浏览器配置里填一个值。我认为我们不该低估这样一个事实：在可预见的未来，所有 I2P 用户至少在计算机方面都略懂一二。（尽管 freenet-support 上的所有证据似乎并非如此） 21:42:00 &lt;ugha_node&gt; Sonium: 不会，“坏人”无论如何都可以手动收集那些信息。 21:42:21 &lt;Sonium&gt; 但如果 NetDb 挂了，i2p 也就挂了，对吗？ 21:42:29 &lt;fvw&gt; hypercubus: 不完全是，我觉得自 0.5 早期以来它一直没工作过这一事实才更该被归咎。 &lt;/offtopic time="once again"&gt;

21:42:44 &lt;fvw&gt; Sonium：你可以拥有不止一个 netdb（网络数据库）（任何人都可以运行一个）
21:42:58 &lt;hypercubus&gt; 我们已经有 pac 了，尽管从技术角度看它效果非常出色，现实中它并不能保护                         avg. jog 的匿名性
21:43:03 &lt;hypercubus&gt; *avg. joe
21:43:22 &lt;ugha_node&gt; fvw：呃…每个 router（I2P 路由器/节点）都有自己的 netDb。
21:43:42 &lt;duck&gt; 好的。我快要晕倒了。你们结束后一定要用 *baff* 把会议关掉
21:43:52 &lt;ugha_node&gt; I2P 现在已经没有任何中心化依赖了。
21:44:07 &lt;hypercubus&gt; 好吧，我只是想把这个想法正式记录到日志里 ;-)
21:44:30 &lt;fvw&gt; ugha_node：好吧，那就是一个发布出去的 netdb。 我其实还没有运行节点（还没有），对于术语也不太熟。
21:44:34 &lt;ugha_node&gt; 嗯。mihi 不是想说点什么吗？
21:45:05  * fvw 喂给 duck 咖啡味巧克力，让他还能再撑一会儿继续运行。
21:45:07 &lt;mihi&gt; 不用 :)
21:45:21 &lt;mihi&gt; duck 是网络设备吗？ ;)
21:45:25 &lt;ugha_node&gt; mihi：顺便问一下，你会认领那个窗口大小提升的赏金吗？
21:45:28  * fvw 给 duck 喂了酒味巧克力，让他无限期关机。
21:45:30 &lt;hypercubus&gt; 用瑞典语
21:45:52 &lt;mihi&gt; ugha_node：什么赏金？
21:46:00 &lt;hypercubus&gt; 好，那继续第 5 项，来段 rant-a-rama？ ;-)
21:46:13 &lt;ugha_node&gt; mihi：http://www.i2p.net/node/view/224
21:46:27  * duck 吃了点 fvw 的巧克力
21:47:16 &lt;mihi&gt; ugha_node：绝对不行；抱歉
21:47:36 &lt;ugha_node&gt; mihi：呃，好吧。:(
21:48:33  * mihi 前阵子试着改造过那个“旧的” streaming API，但它的 bug 太多了……
21:48:53 &lt;mihi&gt; 但在我看来（imho），修那个比修我写的会更容易……
21:49:21 &lt;ugha_node&gt; 嘿。
21:49:42 &lt;hypercubus&gt; 真谦虚
21:49:46 &lt;mihi&gt; 因为它已经有一些（坏掉的）“重排序”支持了
21:50:49 &lt;Sonium&gt; 有办法让 deer 告诉我们 i2p-#i2p 频道上有多少人吗？
21:51:01 &lt;duck&gt; 没有
21:51:08 &lt;hypercubus&gt; 没有，不过我可以把这个功能加到 bogobot 上
21:51:08 &lt;Sonium&gt; :/
21:51:11 &lt;Nightblade&gt; !list
21:51:13 &lt;deer&gt; &lt;duck&gt; 10 人
21:51:13 &lt;hypercubus&gt; 等我把安装程序做完 ;-)
21:51:24 &lt;Sonium&gt; !list
21:51:32 &lt;Sonium&gt; o_O
21:51:35 &lt;mihi&gt; Sonium ;)
21:51:38 &lt;ugha_node&gt; 这不是 fserv 频道！
21:51:39 &lt;Sonium&gt; 刚才是个小把戏！
21:51:40 &lt;ugha_node&gt; :)
21:51:41 &lt;hypercubus&gt; 应该是 !who
21:51:44 &lt;deer&gt; &lt;duck&gt; ant duck identiguy Pseudonym ugha2p bogobot hirvox jrandom Sugadude                   unknown
21:51:48 &lt;cervantes&gt; 糟，错过了会议
21:51:57 &lt;ugha_node&gt; !list
21:52:01 &lt;Nightblade&gt; !who
21:52:11 &lt;deer&gt; &lt;duck&gt; !who-your-mom
21:52:17 &lt;mihi&gt; !who !has !the !list ?
21:52:21 &lt;fvw&gt; !yesletsallspamthechannelwithinoperativecommands
21:52:33 &lt;Nightblade&gt; !ban fvw!*@*
21:52:42 &lt;mihi&gt; !ban *!*@*
21:52:50 &lt;hypercubus&gt; 我感觉法槌要落下了
21:52:51 &lt;duck&gt; 看来是个收尾的好时机
21:52:55 &lt;Sonium&gt; 顺便，你也应该实现一个像 chanserv 有的 !8 命令
21:52:59 &lt;fvw&gt; 好的，现在这事搞定了，我们就关…对。就这样。
21:53:00  * hypercubus 有预感能力
21:53:05 &lt;duck&gt; *BAFF*
21:53:11 &lt;Nightblade&gt; !baff
21:53:12 &lt;hypercubus&gt; 我的头发，我的头发
21:53:24  * fvw 指着 hypercube 大笑。你的头发！你的头发！
</div>
