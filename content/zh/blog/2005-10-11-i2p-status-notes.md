---
title: "2005-10-11 的 I2P 状态说明"
date: 2005-10-11
author: "jr"
description: "每周更新，涵盖 0.6.1.2 版本发布成功、新的 I2PTunnelIRCClient 代理（用于过滤不安全的 IRC 消息）、Syndie CLI（命令行界面）与 RSS 到 SML 的转换，以及 I2Phex 集成计划"
categories: ["status"]
---

大家好，又是星期二了

* Index

1) 0.6.1.2 2) I2PTunnelIRCClient 3) Syndie 4) I2Phex 5) Stego (隐写术) 和暗网 (关于骂战) 6) ???

* 1) 0.6.1.2

上周发布的 0.6.1.2 版本到目前为止进展相当顺利——网络中已有 75% 的节点完成升级，HTTP POST 运行良好，streaming lib（流式库）在推送数据方面相当高效（对一次 HTTP 请求的完整响应常常能在一次端到端往返中收到）。网络规模也有所增长——稳定时看起来大约有 400 个对等节点，但在周末 digg/gotroot [1] 提及的高峰期，随着 churn（节点频繁进出）进一步冲高到 600–700。

[1] http://gotroot.com/tiki-read_article.php?articleId=195     (是的，确实是很旧的文章，我知道，但有人又把它找出来了)

自 0.6.1.2 发布以来，又加入了更多改进——最近 irc2p 的 netsplits（网络分裂）的原因已经找到（并已修复），同时对 SSU 的数据包传输也进行了相当大的改进（可节省超过 5% 的数据包传输量）。我不确定 0.6.1.3 具体何时发布，但也许在本周晚些时候。到时候再看。

* 2) I2PTunnelIRCClient

前几天，经过一些讨论，dust 快速做了一个新的 I2PTunnel 扩展 - the "ircclient" proxy。它通过在 I2P 上对客户端与服务器之间收发的内容进行过滤来工作，剔除不安全的 IRC 消息，并重写那些需要调整的消息。经过一些测试，效果看起来相当不错，dust 已将其贡献给 I2PTunnel，并且现在可以通过 web 界面提供给用户。令人高兴的是，irc2p 的人已经修补了他们的 IRC 服务器，以丢弃不安全的消息，但现在我们不必再信任他们会这样做了 - 本地用户可以掌控自己的过滤。

使用起来很简单 - 不再像以前那样为 IRC 构建 "Client proxy（客户端代理）"，只需构建一个 "IRC proxy（IRC 代理）" 即可。若要将你现有的 "Client proxy" 转换为 "IRC proxy"，你可以（虽然有点尴尬）编辑 i2ptunnel.config 文件，把 "tunnel.1.type=client" 改为 "tunnel.1.ircclient"（或根据你的代理使用合适的编号）。

如果一切顺利，它将在下一个版本中成为 IRC 连接的默认 I2PTunnel 代理类型。

干得漂亮，dust，谢谢！

* 3) Syndie

Ragnarok 的定时分发功能似乎进展顺利，而自 0.6.1.2 发布以来，又推出了两个新功能——我添加了一个新的简化版 CLI（命令行界面），用于发布到 Syndie [2]；而 dust（好样的 dust！）迅速写出了一些代码，用于从 RSS/Atom 源中提取内容，拉取其中引用的任何附件或图像，并将 RSS 内容转换为 SML（!!!）[3][4]。

将这两者结合起来，其含义应该很清楚。有更多消息时会再通知。

[2] http://syndiemedia.i2p/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&entry=1128816000000&expand=true [3] http://syndiemedia.i2p/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&entry=1128816000001&expand=true [4] http://dust.i2p/Sucker.java     (我们很快就会把它集成到CVS中)

* 4) I2Phex

坊间传闻 I2Phex 运行得相当不错，但长期来看仍有一些问题持续存在。关于下一步如何推进，论坛 [5] 上已经有一些讨论，Phex 的首席开发者 GregorK 也参与发言，表示支持将 I2Phex 的功能重新整合回 Phex（或者至少让主线 Phex 为传输层提供一个简单的插件接口）。

这将会真的相当给力，因为这意味着需要维护的代码会少很多，而且我们还能受益于 Phex 团队改进代码库的成果。不过，要让它奏效，我们需要一些开发者站出来牵头这次迁移。I2Phex 的代码已经相当清楚地标明了 sirup 都改动了哪些地方，所以应该不会太难，但恐怕也谈不上小菜一碟 ;)

我现在实在没时间马上着手这件事，不过如果你想帮忙，可以去论坛看看。

[5] http://forum.i2p.net/viewforum.php?f=25

* 5) Stego and darknets (re: flamewar)

关于隐写术和暗网的讨论，邮件列表[6]最近相当活跃。该话题在很大程度上已转移到 Freenet 技术列表[7]，主题为“I2P conspiracy theories flamewar”，但仍在持续。

我不确定除了帖子本身的内容之外，我还有多少可补充的，不过有人提到这番讨论有助于他们对 I2P 和 Freenet 的理解，所以也许值得浏览一下。或者也未必 ;)

[6] http://dev.i2p.net/pipermail/i2p/2005-October/thread.html [7] nttp://news.gmane.org/gmane.network.freenet.technical

* 6) ???

如你所见，有很多令人兴奋的事情正在发生，而且我肯定还有一些内容没提到。几分钟后顺道来 #i2p 参加我们的每周会议，打个招呼吧！

=jr
