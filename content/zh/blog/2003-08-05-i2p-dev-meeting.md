---
title: "I2P 开发者会议，2003年8月5日"
date: 2003-08-05
author: "nop"
description: "第52次 I2P 开发者会议，涵盖 Java 开发状态、密码学更新和 SDK 进展"
categories: ["meeting"]
---

<h2 id="quick-recap">简要回顾</h2>

<p class="attendees-inline"><strong>出席者：</strong> hezekiah, jeremiah, jrand0m, mihi, nop, thecrypto</p>

<h2 id="meeting-log">会议记录</h2>

<div class="irc-log"> <nop>	好，会议开始了 <nop>	议程上有什么 -->	logger (logger@anon.iip) 加入了 #iip-dev -->	Anon02 (~anon@anon.iip) 加入了 #iip-dev <hezekiah>	Tue Aug  5 21:03:10 UTC 2003 <hezekiah>	欢迎来到第 N 次 iip-dev 会议。 <hezekiah>	议程上有什么？ <thecrypto>	Tue Aug  5 21:02:44 UTC 2003 <thecrypto>	已与 NTP 层级 2 同步 :) <hezekiah>	Tue Aug  5 21:03:13 UTC 2003 -->	ptm (~ptm@anon.iip) 加入了 #iip-dev <hezekiah>	刚刚与 NIST 同步了。 :) <mihi>	这种同步对 iip 的延迟没什么帮助 ;) <jrand0m>	nop：我想讨论的内容：Java 开发状态、Java 密码学状态、Python 开发状态、SDK 状态、命名服务 <hezekiah>	（我们_已经_要讨论命名服务了？） <jrand0m>	不是讨论设计，你这蠢货，那是 co 的专场。  要是有话题，就聊聊。 <hezekiah>	啊 *	jrand0m 把 LART 收起来 <jrand0m>	议程上还有别的吗？ <jrand0m>	或者我们开始吧？ <hezekiah>	嗯，我想不出还能加什么。 <hezekiah>	啊！ <hezekiah>	哦！ <jrand0m>	好。  Java 开发状态： <hezekiah>	不错。 <--	mrflibble 退出了（Ping 超时） <nop>	好 <nop>	议程 <nop>	1) 欢迎 <jrand0m>	截至今天，有一个 Java 客户端 API 和一个存根 Java router，二者可以互相通信。  另外，还有一个名为 ATalk 的应用，支持匿名 IM 和文件传输。 <nop>	2) IIP 1.1 中断 <nop>	3) I2P <nop>	4) 结束，附评论等 *	jrand0m 回到角落 <nop>	抱歉 	  joeyo jrand0m Aug 05 17:08:24 * hezekiah 给了 jrand0m 一顶傻帽，让他在角落里戴上。 ;-) <nop>	对此抱歉 <nop>	没看到你已经开始了 <nop>	也许我该去角落里 <hezekiah>	lol <jrand0m>	别担心。  第 1 项） *	hezekiah 也递给 nop 一顶傻帽。 :) <nop>	好，欢迎各位 <nop>	巴拉巴拉 <nop>	2) IIP 1.1 中断 -->	mrflibble (mrflibble@anon.iip) 加入了 #iip-dev <hezekiah>	第 52 次 iip-dev 会议，以及所有那些老套玩意儿！ <nop>	服务器最近硬盘扇区出了些问题，已经更换了 <nop>	我打算把这倒霉的服务器迁到一个更稳定、具备冗余的环境 <nop>	并且可能把多个 ircd 服务器的控制权分给别人 <nop>	不知道 <nop>	这个需要讨论 <--	Anon02 退出了（来自客户端的 EOF） <nop>	希望我们的服务器现在能保持运行，因为硬盘已经更换了 <nop>	给各位带来不便，抱歉 <nop>	3) I2P - jrand0m 请开始 <nop>	从角落出来，jrand0m *	hezekiah 走到角落，把 jrand0m 从椅子上拉起来，拖到讲台，拿走他的傻帽，把话筒递给他。 *	nop 走到那个角落去顶替他的位置 <hezekiah>	lol! <jrand0m>	抱歉，回来了 *	nop 从 hezekiah 那里抢过傻帽 *	nop 把它戴到自己头上 *	nop 为 jrand0m 鼓掌 *	jrand0m 只是看戏 <jrand0m>	呃……嗯，好吧 <hezekiah>	jrand0m: i2p, java 状态等。开讲吧！ <jrand0m>	所以，截至今天，有一个 Java 客户端 API 和一个存根 Java router，二者可以互相通信。  另外，还有一个名为 ATalk 的应用，支持匿名 IM 和文件传输。 <hezekiah>	已经能传文件了！？ <jrand0m>	是的，先生 <hezekiah>	哇。 <hezekiah>	我肯定是落伍了。 <jrand0m>	但不是最优雅的做法 <hezekiah>	lol <jrand0m>	它是把文件直接塞进一条消息里 <hezekiah>	哎哟。 <nop>	1.8Mb 的本地传输花了多久？ <jrand0m>	我用一个 4K 文件和一个 1.8Mb 文件测试过 <jrand0m>	几秒钟 <nop>	不错 <nop>	:) <hezekiah>	Java 这套东西现在做真正的加密了吗，还是仍然是假的？ <nop>	假的 <nop>	连我都知道 <nop>	:) <jrand0m>	我先自言自语预热了一下【比如从一个窗口给另一个窗口说声 hi】这样就不用处理第一次 elg 的开销 <jrand0m>	对，大部分都是假的 <thecrypto>	加密大多是假的 <thecrypto>	不过这个正在做 <hezekiah>	当然。 :) <jrand0m>	当然。 <jrand0m>	在这方面，thecrypto，要不要给我们更新一下？ <thecrypto>	嗯，目前我已经完成了 ElGamal 和 SHA256 <thecrypto>	现在我在做 DSA 的素数生成 <thecrypto>	我会发出 5 个，然后我们挑一个就行 <hezekiah>	nop：你不是也有用于 DSA 的素数要拿出来吗？ <thecrypto>	我们对 ElGamal 和 SHA256 也做了一些基准测试 <thecrypto>	而且都很快 <jrand0m>	关于 elg 的最新基准： <jrand0m>	密钥生成时间 平均: 4437 总计: 443759 最小: 	  872	   最大: 21110	   密钥生成/秒: 0 <jrand0m>	加密时间 平均    : 356 总计: 35657 最小: 	  431	   最大: 611	   加密 Bps: 179 <jrand0m>	解密时间 平均    : 983 总计: 98347 最小: 	  881	   最大: 2143	   解密 Bps: 65</div>

<hezekiah>	min 和 max：单位是秒吗？
<jrand0m>	注意 Bps 实际上没什么用，因为我们只加密/解密 	  64 字节
<thecrypto>	毫秒
<jrand0m>	不，抱歉，都是毫秒
<hezekiah>	酷。 :)
<hezekiah>	这些都是用 Java 做的吗？
<thecrypto>	是的
<thecrypto>	纯 Java
<hezekiah>	好的。我已经彻底被折服了。 :)
<jrand0m>	100%。  P4 1.8
<thecrypto>	在我 800 Mhz 的机器上差不多
<hezekiah>	我怎么做同样的测试？
<jrand0m>	sha256 基准测试：
<jrand0m>	短消息时间平均值  : 0 total: 0	min: 0	max: 	  0  Bps: NaN
<jrand0m>	中等消息时间平均值 : 1 total: 130	min: 0	max: 	  10 Bps: 7876923
<jrand0m>	长消息时间平均值   : 146	total: 14641	min: 	  130	   max: 270	   Bps: 83037
<thecrypto>	运行 ElGamalBench 程序
<hezekiah>	好的。
<hezekiah>	我去找找。
<jrand0m>	(短大小：~10 字节，中：~10KB，长：~ 1MB)
<jrand0m>	java -cp i2p.jar ElGamalBench
<jrand0m>	(在运行 "ant all" 之后)
<hezekiah>	jrand0m: 谢谢。 :)
<jrand0m>	不客气
<thecrypto>	NaN 的意思是它快到我们最后会出现除以 0 	  —— 太快了 :)
<hezekiah>	sha 的基准测试是什么？
<jrand0m>	java -cp i2p.jar SHA256Bench
-->	Neo (anon@anon.iip) 加入了 #iip-dev
<hezekiah>	好的。
<jrand0m>	我们可能想把那些移到相关引擎的 main() 方法里，但它们 	  目前放在那里也很好
<hezekiah>	让我们看看把这些跑在 AMD K6-2 333MHz 上有多快（这是一颗 	  并不以整数运算见长的芯片。）
<jrand0m>	呵
<jrand0m>	好，所以我们还剩 DSA 和 AES，对吧？
<jrand0m>	这些都太赞了，thecrypto。  干得好。
<thecrypto>	嗯
<jrand0m>	我能烦你问下另外两个的预计时间吗？  ;)
<hezekiah>	如果在我的机器上哪怕能接近你那边的速度， 	  你就得教教我是怎么做到的。 ;-)
<thecrypto>	DSA 基本完成了，只要我把素数准备好就能搞定
<nop>	hezekiah 你试过 Python 的 sslcrypto 吗
<thecrypto>	从素数生成器那边拷点代码之类的 	  就能搞定
<nop>	就是那个链接里的那个
<hezekiah>	nop: sslcrypto 对我们没用。
<hezekiah>	nop: 它没有实现 ElGamal _或_ AES _或_ sha256。
<thecrypto>	AES 基本完成了，只是某处还有个错误我还在努力找出来并把它 	  干掉，一旦解决这个问题，就能收工
<jrand0m>	thecrypto> 那么到周五，DSA 的密钥生成、签名、验证，以及 AES 的加密、 	  解密，能支持任意大小的输入？
<nop>	McNab 的网站上的那个没有吗？
<thecrypto>	对
<nop>	糟了
<thecrypto>	应该周五
<thecrypto>	很可能周四
<jrand0m>	thecrypto> 那包括 UnsignedBigInteger 那些东西吗？
<thecrypto>	因为夏令营下周的会议我会缺席， 	  之后我就回来
<thecrypto>	jrand0m: 大概不会
<jrand0m>	好。
<jrand0m>	所以目前，Java 和 Python 之间的互操作性 	  挂了。
<jrand0m>	指的是加密这块。
---	通知：jeremiah 已上线 (anon.iip)。
-->	jeremiah (~chatzilla@anon.iip) 加入了 #iip-dev
<jrand0m>	(也就是用于签名、密钥、加密和解密)

<nop>	嗯，也许我们应该把重点更多放在 C/C++ 上
<thecrypto>	嗯，一旦我们把它完全跑起来，就能确保 	  java 和 python 彼此能互通
<jrand0m>	你外出的时候我会研究一下 unsigned 相关的东西。
<jeremiah>	有人能把聊天记录发邮件给我吗？ jeremiah@kingprimate.com
<hezekiah>	jeremiah：给我一分钟。 :)
<jrand0m>	nop> 我们有做 C/C++ 的开发者吗？
<nop>	有一个人，是的
<nop>	还有 Hezekiah，我们知道他也能做
<jrand0m>	或者我们可以请 hezekiah + 	  jeremiah 提供一个 python 开发状态更新，看看什么时候会有更多人加入 c/c++ 的开发
<jrand0m>	对，当然。  不过 hez+jeremiah 目前在做 python 	  （对吧？）
<hezekiah>	是的。
<--	mrflibble 已退出 (Ping 超时)
<hezekiah>	我算是给可怜的 jeremiah 添了不少麻烦。
<nop>	我只是说，如果 python 速度不够快的话
<hezekiah>	python 主要是为了让我理解这个网络。
<nop>	啊哈
<hezekiah>	一旦我让它基本遵循完整的规范，我打算 	  把它交给 jeremiah，按他的想法来处理。
<hezekiah>	它并不是要做一个超强的规范实现。
<hezekiah>	（如果我要那样，我会用 C++。）
<jeremiah>	嗯，如果我没记错的话，这个应用其实没有特别吃 CPU 的部分， 	  除了加密；而且理想情况下那部分无论如何都会由 C 来处理，对吧？
<jrand0m>	当然，jeremiah。一切取决于应用
-->	mrflibble (mrflibble@anon.iip) 加入了 #iip-dev
<hezekiah>	jeremiah：理论上是。
<jrand0m>	那么我们在 python 这边进度如何？  客户端 API、仅本地的 	  router，等等？
<jeremiah>	python 的实现也会让我们从一开始就知道 	  可以做哪些优化……我想尽量让它保持最新，或者在可能的情况下， 	  领先于 C 的实现
<hezekiah>	jrand0m：好的。我这边的情况是这样的。
<hezekiah>	从_理论上_讲，router 应该能够处理 	  来自客户端的所有非管理消息。
<hezekiah>	不过我还没有客户端，所以没法调试 	  它（也就是说，仍然有 bug。）
<hezekiah>	我现在正在做客户端。
<jrand0m>	'k。  如果你能禁用签名验证，我们现在应该就可以 	  让 java 客户端对接它运行了
<hezekiah>	我希望一两天内把除管理消息以外的部分 	  完成。
<jrand0m>	我们可以在会议结束后测试一下
<hezekiah>	jrand0m：好。
<jeremiah>	自上次会议以来我主要在处理现实中的事情， 	  我可以做客户端 API，只是一直在尝试把我的思路 	  与 hezekiah 的对齐
<jrand0m>	酷
<hezekiah>	jeremiah：你知道吗，先等等。
<hezekiah>	jeremiah：我现在可能丢了太多新东西给你 	  处理。
<jeremiah>	hezekiah：对，我本来要说的是你 	  大概应该先把基础部分实现了
<hezekiah>	jeremiah：再过一阵它就会稳定下来，你就 	  可以开始打磨了。（有很多 TODO 注释需要帮忙。）
<jeremiah>	等我弄清楚全貌之后，我就可以再把它扩展
<hezekiah>	没错。
<hezekiah>	这些代码就交给你来维护了。 :)
<jrand0m>	酷。  那预计 1-2 周会有可用的 python router + 客户端 API？
<hezekiah>	我下周要去度假，所以大概是吧。
<hezekiah>	我们很快会有 router 与 router 之间的更多细节吗？
<jrand0m>	不会。
<jrand0m>	嗯，会。
<jrand0m>	可是不会。
<hezekiah>	哈哈
<jeremiah>	hezekiah：假期多长？
<hezekiah>	1 周。
<jeremiah>	好
<jrand0m>	（也就是说，一旦 SDK 发布，我的 100% 时间就投入到 I2NP）
<hezekiah>	我希望在去度假之前 	  写完所有非管理功能
<hezekiah>	.
<jrand0m>	不过你回来后不久就要去上大学了，对吧？
<hezekiah>	I2NP?
<hezekiah>	对。
<jrand0m>	网络协议
<hezekiah>	度假回来后我大概还有 1 周时间。
<hezekiah>	然后我就走了。
<hezekiah>	而且我的空闲时间会骤降。
<jrand0m>	所以那 1 周应该只用来调试
<jeremiah>	不过 hez 不在的时候我可以继续写代码
<jrand0m>	没错
<jrand0m>	jeremiah，你暑假安排怎么样？
<hezekiah>	jeremiah：也许你可以把那些管理功能做起来？

<thecrypto>	我从假期回来后还有一个月可以继续做这些事情
<jrand0m>	过自己的生活，还是像我们其他这些 l00sers 一样？  :)
<jeremiah>	也许
<hezekiah>	100sers?
<hezekiah>	100ser 是什么？
<jeremiah>	我22号就要去上大学了，除此之外我可以开发
<mihi>	hezekiah：一个失败者
<jeremiah>	在我走之前的最后一周，我所有的朋友都不在……所以我可以进入超高速开发模式
<hezekiah>	mihi：啊！
<jrand0m>	呵呵
<hezekiah>	好。我们议程进行到哪儿了？
<hezekiah>	也就是，接下来是什么？
<jrand0m>	SDK 状态
<jrand0m>	SDK == 一个客户端实现、一个仅本地的 router 实现、一个应用，以及文档。
<jrand0m>	我想在下周二之前发布出来。
<hezekiah>	jeremiah：那个积压的东西正在路上。抱歉我刚才忘了你。 :)
<jeremiah>	谢谢
<jrand0m>	好，co 不在，所以命名服务的事情大概有点儿离题了
<jrand0m>	等他放出规格说明或他在场的时候，我们可以再讨论命名服务
<jrand0m>	好，I2P 的内容到此为止
<jrand0m>	还有谁有 I2P 的内容？否则我们继续：
<nop> 4) 结束，顺便评论等等
<hezekiah>	我想不出别的了。
<jrand0m>	我想大家都看过 http://www.cnn.com/2003/TECH/internet/08/05/anarchist.prison.ap/index.html 了吧？
<thecrypto>	我这儿没有
<jrand0m>	(nop 之前在这里贴过)
<hezekiah>	那个因为链接到造炸弹网站而被逮捕的家伙的新闻？
<jrand0m>	是的
<jrand0m>	这与我们需要尽快把 I2P 跑起来的相关性应该是显而易见的 ;)
<hezekiah>	好！jeremiah，那些日志已经发出去了。
<jeremiah>	谢谢
<jrand0m>	大家有没有问题/评论/想法/飞盘，还是说我们要创造史上最短会议记录？
*	thecrypto 扔出一个飞盘 <--	logger 已退出 (Ping timeout)
<jrand0m>	天哪，你们今天都这么安静 ;)
<mihi>	问题：
<mihi>	非开发者到哪里能拿到你们的 Java 代码？
<jrand0m>	是的，先生？
<thecrypto>	还没有
<mihi>	404
<jrand0m>	等我们准备发布时就会提供。也就是说，源代码会随 SDK 一起放出
<jrand0m>	呵
<jrand0m>	是啊，我们不用 SF
<hezekiah>	nop：有没有可能找个时间把匿名 CVS 搞起来？
<hezekiah>	时间？
<--	mrflibble 已退出 (Ping timeout)
<nop>	嗯，我会打开一个非标准端口
<jrand0m>	hezekiah> 代码上加上 GPL 许可后我们就会提供那个
<nop>	不过我正在弄 viewcvs
<jrand0m>	也就是说不是现在，因为 GPL 文档还没加到代码里
<hezekiah>	jrand0m：它已经在所有 Python 代码目录里了，所有 Python 源文件也都声明在 GPL-2 之下。
<jrand0m>	hezekiah> 那是在 cathedral 上吗？
<hezekiah>	是的。
<jrand0m>	啊，好的。i2p/core/code/python？ 还是别的模块？
*	jrand0m 还没在里面看到它
<hezekiah>	每个 Python 代码目录里都有一个 COPYING 文件，包含 GPL-2，而且每个源文件都把许可设为 GPL-2
<hezekiah>	是 i2p/router/python 和 i2p/api/python
<jrand0m>	'k
<jrand0m>	所以，没错，到下周二我们会有 SDK + 公共源码访问。
<hezekiah>	酷。
<hezekiah>	或者像你爱说的那样，wikked。 ;-)
<jrand0m>	呵
<jrand0m>	nada mas?
<hezekiah>	nada mas? 那是什么意思！？
<jeremiah>	没别的了
*	jrand0m 建议你在大学学点西班牙语
-->	mrflibble (mrflibble@anon.iip) 加入了 #iip-dev
<hezekiah>	还有人有问题吗？
<hezekiah>	第一次！
<--	ptm (~ptm@anon.iip) 离开了 #iip-dev (ptm)
<hezekiah>	第二次！
<--	mrflibble 已退出 (mr. flibble 说“game over boys”)
<hezekiah>	要说现在说……或者等你想说的时候再说！
<thecrypto>	好，我要把 ElGamal 再优化一下，所以将来可以期待更快的 ElGamal 基准测试
<jrand0m>	在调优之前请先专注于 DSA 和 AES……拜——托——啦 :)
<thecrypto>	我会的
<hezekiah>	他之所以这么做，是因为我又在给大家找麻烦了。 ;-)
<thecrypto>	我在生成 DSA 素数
-->	mrflibble (mrflibble@anon.iip) 加入了 #iip-dev
<thecrypto>	嗯，至少现在在做一个生成 DSA 素数的程序
<hezekiah>	Java 里的 ElGamal 不太喜欢 AMD K-6 II 333MHz。
<hezekiah>	好。
<hezekiah>	提问环节结束！
<jrand0m>	好，hez，我们结束了。 你想不想小聚一下，推进 Java 客户端和 Python router 的工作？
<hezekiah>	各位公民，下周见！
*	hezekiah 猛地敲下*baf*er
</div>
