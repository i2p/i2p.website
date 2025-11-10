---
title: "I2P 2005-11-01 的状态说明"
date: 2005-11-01
author: "jr"
description: "每周更新，涵盖 0.6.1.4 版本发布成功、bootstrap（引导）攻击分析、I2Phex 0.1.1.34 安全修复、voi2p 语音应用开发，以及 Syndie RSS 订阅源集成"
categories: ["status"]
---

大家好，又到了每周的那个时候了

* Index

1) 0.6.1.4 和网络状态 2) boostraps（引导）, predecessors（前驱节点）, 全局被动攻击者, 和 CBR 3) i2phex 0.1.1.34 4) voi2p 应用 5) syndie 和 sucker 6) ???

* 1) 0.6.1.4 and net status

上周六发布的 0.6.1.4 看起来进展相当顺利——全网已有 75% 完成升级（谢谢！），其余的大多数也仍在使用 0.6.1.3。整体运行情况看起来相当不错，虽然我没听到太多反馈——无论正面的还是负面的——我想如果它很糟，大家应该会大声抱怨的 :)

特别是，我很想听取使用拨号调制解调器连接的用户的任何反馈，因为我所做的测试只是对这类连接的基本模拟。

* 2) boostraps, predecessors, global passive adversaries, and CBR

关于几个想法，邮件列表上出现了更多讨论，并且有关 bootstrap 攻击（引导阶段攻击）的摘要已上线[1]。我在为选项 3 制定加密规范方面取得了一些进展，虽然目前尚未发布任何内容，不过这相当简单明了。

[1] http://dev.i2p.net/pipermail/i2p/2005-October/001146.html

我们已经就如何通过恒定比特率（CBR）tunnels 提升对强大对手的抵抗能力进行了进一步讨论；尽管我们可以选择探索这一路径，但它目前被安排在 I2P 3.0，因为要正确使用它需要大量资源，而且这种开销很可能会对谁愿意在这种开销下使用 I2P，以及哪些群体能够或根本无法使用 I2P，产生可衡量的影响。

* 3) I2Phex 0.1.1.34

上周六我们还发布了一个新的 I2Phex 版本 [2]，修复了一个文件描述符泄漏，该问题最终会导致 I2Phex 出现故障（感谢 Complication！），并删除了一些会使他人能够远程指示你的 I2Phex 实例下载特定文件的代码（感谢 GregorK！）。强烈建议升级。

CVS 版本（尚未发布）也进行了更新，解决了一些同步问题——Phex 假设某些网络操作会被立即处理，而 I2P 有时需要一段时间才能完成这些操作 :) 这会表现为 GUI（图形用户界面）短暂卡住、下载或上传停滞，或连接被拒绝（也可能以其他方式）。该更新尚未经过充分测试，但很可能会在本周推送到 0.1.1.35 版本。我相信，一旦有更多消息，论坛上会发布更多信息。

[2] http://forum.i2p.net/viewtopic.php?t=1143

* 4) voi2p app

Aum is churning away on his new voice (and text) over I2P app, and while I haven't seen it yet, it sounds neat. Perhaps Aum can give us an update in the meeting, or we can just wait patiently for the first alpha release :)

* 5) syndie and sucker

dust 一直在埋头开发 syndie 和 sucker，而 I2P 最新的 CVS 构建现在允许你自动从 RSS 和 Atom 订阅源拉取内容，并将其发布到你的 syndie 博客。目前，你必须在 wrapper.config 中显式添加 lib/rome-0.7.jar 和 lib/jdom.jar（wrapper.java.classpath.20 和 21），不过我们之后会把它们打包进去，这样就不再需要手动添加了。这个功能仍在开发中，而且 rome 0.8（尚未发布）看起来会带来一些很酷的特性，比如可以从订阅源中抓取 enclosure（RSS 附件项），sucker 随后就能把它作为附件导入到一篇 syndie 帖子里（当然，现在它已经能处理图片和链接了！）

像所有的 RSS 源一样，在内容收录方式上似乎存在一些不一致，因此有些源导入起来比其他的更顺畅。我想，如果大家能用不同的源来帮忙测试，并把它在某些源上出错的问题反馈给 dust，那应该会很有帮助。总之，这东西看起来相当令人兴奋，干得漂亮，dust！

* 6) ???

目前就这些，不过如果有人有任何问题，或想进一步讨论一些事情，欢迎在 GMT 晚上 8 点的会议上顺道过来（记得夏令时！）

=jr
