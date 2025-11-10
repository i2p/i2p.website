---
title: "2006-10-03 的 I2P 状态说明"
date: 2006-10-03
author: "jr"
description: "网络性能分析、CPU 瓶颈排查、Syndie 1.0 发布规划，以及分布式版本控制评估"
categories: ["status"]
---

大家好，本周的状态笔记来得有些晚。

* Index

1) 网络状态 2) Router 开发状态 3) Syndie 设计理由（续） 4) Syndie 开发状态 5) 分布式版本控制 6) ???

* 1) Net status

过去一两周，irc 和其他服务总体相当稳定，不过 dev.i2p/squid.i2p/www.i2p/cvs.i2p 出现了几次小故障（由于一些临时的操作系统相关问题）。目前看来一切处于稳定状态。

* 2) Router dev status

关于 Syndie 的讨论还有另一面：“那么，这对 router 意味着什么？” 为了回答这个问题，让我先简单说明一下目前 router 的开发处于什么阶段。

On the whole, the thing holding the router back from 1.0 is in my view its performance, not its anonymity properties. Certainly, there are anonymity issues to improve, but while we do get pretty good performance for an anonymous network, our performance is not sufficient for wider use. In addition, improvements to the anonymity of the network will not improve its performance (in most instances I can think of, anonymity improvements reduce throughput and increase latency). We need to sort out the performance issues first, for if the performance is insufficient, the whole system is insufficient, regardless of how strong its anonymity techniques are.

那么，是什么在拖累我们的性能呢？说来也怪，似乎是我们的 CPU 使用率。在解释具体原因之前，先补充一些背景。

 - to prevent partitioning attacks, we all need to plausibly build
   our tunnels from the same pool of routers.
 - to allow the tunnels to be of manageable length (and source
   routed), the routers in that pool must be directly reachable by
   anyone.
 - the bandwidth costs of receiving and rejecting tunnel join
   requests exceeds the capacity of dialup users on burst.

因此，我们需要将 routers 分为不同层级 - 有些在全球范围内可达且具有较高带宽上限（tier A），有些则不是（tier B）。这在实际中已通过 netDb 中的容量信息实现，并且截至一两天前，tier B 与 tier A 的比例大约为 3 比 1（cap L、M、N 或 O 的 routers 有 93 个，而 cap K 的有 278 个）。

现在，在 tier A（A 级层）中基本上有两种需要管理的稀缺资源——带宽和 CPU。带宽可以通过常见的方法进行管理（将负载分散到一个广泛的节点池中，让一些节点处理海量流量[例如那些使用 T3 线路的]，以及拒绝或限速单个 tunnels 和连接）。

管理 CPU 使用更为困难。在 A 级 router 上观察到的主要 CPU 瓶颈是对 tunnel 构建请求的解密。大型 router 可能（而且确实）会被这一活动完全占用——例如，我的一台 router 的生命周期内平均 tunnel 解密时间为 225ms，而生命周期内 tunnel 请求解密的*average*频率是每 60 秒 254 次事件，或每秒 4.2 次。简单地将这两个数相乘就可以看出，仅 tunnel 请求解密就消耗了 95% 的 CPU（而且这还没有将事件计数中的峰值考虑在内）。那台 router 仍然设法同时参与 4-6000 条 tunnel，接受了约 80% 的已解密请求。

不幸的是，由于该 router 的 CPU 负载极高，它不得不在尚未解密之前就丢弃大量的 tunnel（隧道）构建请求（否则这些请求会在队列中等待太久，即使被接受，原始请求发起方也会认为它们已经丢失，或者负载过高而无从处理）。在这种情况下，该 router 的 80% 接受率看起来就差得多了 - 在其整个生命周期中，它解密了约 250k 个请求（也就是说约 200k 个被接受），但由于 CPU 过载，它不得不在解密队列中丢弃约 430k 个请求（把那 80% 的接受率变成了 30%）。

解决方案似乎集中在降低用于解密 tunnel 请求的相关 CPU 开销。如果我们将 CPU 时间削减一个数量级，就会显著提高 A 级 router 的处理能力，从而减少拒绝（包括显式拒绝以及由于丢弃请求而产生的隐式拒绝）。这反过来会提高 tunnel 构建成功率，降低租约过期的频率，进而减少由于重建 tunnel 给网络带来的带宽负载。

为此的一种方法是将 tunnel 构建请求从使用 2048 位的 Elgamal 改为，比如 1024 位或 768 位。不过问题在于，如果你破解了一个 tunnel 构建请求消息的加密，你就会知道该 tunnel 的完整路径。即便我们走这条路，这能给我们带来多大好处？将解密时间改善一个数量级的收益，可能会被 B 层与 A 层比例增加一个数量级（也就是所谓的搭便车者问题）所抵消，然后我们就会陷入困境，因为我们不可能再把它降到 512 位或 256 位的 Elgamal（还能有脸照镜子；）

另一种选择是使用较弱的加密，但去掉我们在新的 tunnel 构建过程中加入的针对数据包计数攻击的防护。这样将允许我们在类似 Tor 的伸缩式 tunnel 中使用完全临时的协商密钥（不过，这同样会使 tunnel 创建者暴露于可识别服务的、非常简单的被动式数据包计数攻击之下）。

另一种想法是在 netDb 中发布并使用更为明确的负载信息，使客户端能够更准确地检测到类似上述那种情况：某个高带宽 router 在甚至不查看的情况下就丢弃其 60% 的 tunnel 请求消息。沿着这一思路有一些值得尝试的实验，而且可以在完全向后兼容的情况下完成，因此我们应该很快就能看到它们。

所以，在我目前看来，这就是 router/网络 的瓶颈。对于我们如何应对它的任何建议，我们将不胜感激。

* 3) Syndie rationale continued

论坛上有一篇关于 Syndie 及其在整体中所处位置的内容详实的帖子 - 请在 <http://forum.i2p.net/viewtopic.php?t=1910> 查看

此外，我只想强调正在编写中的 Syndie 文档里的两段摘录。首先，来自 irc（以及尚未发布的 FAQ）：

<bar> 我一直在想，以后谁会有胆子够大来托管 syndie 的生产服务器/归档？
<bar> 那些东西难道不会像如今的 eepsites(I2P Sites) 一样容易被追踪到吗？
<jrandom> 公开的 syndie 归档没有能力*读取*论坛上发布的内容，除非论坛公开了用于此目的的密钥
<jrandom> 并参见 usecases.html 的第二段
<jrandom> 当然，被依法要求下架某个论坛的那些归档托管者大概会照做
<jrandom> （不过人们可以迁移到另一个归档，而不会中断论坛的运行）
<void> 是啊，你应该提到迁移到不同媒介将会是无缝的
<bar> 如果我的归档关闭了，我可以把整个论坛上传到一个新的归档，对吧？
<jrandom> 没错 bar
<void> 他们可以在迁移时同时使用两种方式
<void> 而且任何人都能够同步这些媒介
<jrandom> 对的 void

(尚未发布的) Syndie usecases.html 的相关部分是：

尽管许多不同的群体常常希望将讨论组织到一个在线论坛中，但传统论坛（网站、BBS 等）的中心化特性可能会带来问题。例如，托管该论坛的网站可能会因拒绝服务攻击或行政措施而被迫下线。此外，单一主机为监控该群体的活动提供了一个简便的切入点，因此即使论坛是伪匿名的，这些化名也可能被关联到发布或阅读单条消息的 IP。

此外，论坛不仅是去中心化的，其组织方式也是自组织的，同时又与其他组织方式完全兼容。这意味着，一些小群体可以采用一种技术来运行他们的论坛（例如把消息粘贴到一个 wiki 站点上进行分发），另一些人则可以采用另一种技术来运行他们的论坛（例如将消息发布到像 OpenDHT 这样的分布式哈希表中）。而如果有个人同时了解这两种技术，就可以把这两个论坛同步起来。这样，仅了解该 wiki 站点的人就能在彼此毫不相知的情况下，与仅了解 OpenDHT 服务的人进行交流。进一步说，Syndie 允许各个小组（cell）在与整个组织范围内沟通的同时，控制自身的对外可见性。

* 4) Syndie dev status

最近 Syndie 取得了不少进展，已经在 IRC 频道向大家发布了 7 个 alpha 版本。可脚本化接口中的大多数重大问题都已得到解决，我希望我们能在本月晚些时候发布 Syndie 1.0。

我刚才说“1.0”了吗？当然了！虽然 Syndie 1.0 将是一个基于文本的应用程序，在可用性方面甚至难以与其他同类的基于文本的应用（如 mutt 或 tin）相提并论，但它将提供完整的功能集，支持基于 HTTP 和基于文件的联合分发策略，并希望能向潜在的开发者展示 Syndie 的能力。

目前，我暂定推出 Syndie 1.1 版本（让用户更好地整理他们的存档和阅读习惯），并且可能还会有 1.2 版本，用于集成一些搜索功能（包括简单搜索，甚至可能包括 Lucene 的全文搜索）。Syndie 2.0 很可能会是首个 GUI（图形用户界面）版本，而浏览器插件将随 3.0 一同推出。当然，一旦实现，还将增加对更多存档和消息分发网络的支持（freenet, mixminion/mixmaster/smtp, opendht, gnutella 等）。

不过我也意识到，Syndie 1.0 不会成为一些人所期望的那种惊天动地的产品，因为基于文本的应用确实主要面向极客，但我想试着打破我们把"1.0"视为最终发布的习惯，转而把它看作一个开始。

* 5) Distributed version control

到目前为止，我一直在凑合着用 Subversion 作为 Syndie 的版本控制系统（VCS），尽管我真正熟悉的只有 CVS 和 ClearCase。这主要是因为我大多数时间不在线，即便在线也是拨号上网，速度很慢，所以 Subversion 的本地 diff/revert 等功能就很方便。不过，昨天 void 提醒我，不如考虑研究一下某种分布式版本控制系统。

几年前在为 I2P 评估一个 VCS（版本控制系统）时，我看过它们，但因为当时我不需要它们的离线功能（那时我的网络连接很好），所以觉得没必要花时间去学习。现在情况已不同，因此我正在更深入地了解它们。

- From what I can see, darcs, monotone, and codeville are the top

在候选方案中，darcs 的基于补丁的 VCS（版本控制系统）看起来尤其有吸引力。比如说，我可以在本地完成所有工作，然后只需用 scp 把经 gzip 和 gpg 处理的 diffs 上传到 dev.i2p.net 上的一个 Apache 目录，而其他人可以通过把他们经 gzip 和 gpg 处理的 diffs 发布到他们自己选择的位置来贡献更改。到了需要给发行版打标签的时候，我会生成一个 darcs diff，它指明该发行版所包含的补丁集合，并像其他的一样把那个 .gz'ed/.gpg'ed diff 上传上去（当然，也会发布实际的 tar.bz2、.exe 和 .zip 文件 ;)）

而且，尤其值得注意的一点是，这些经 gzip/gpg 处理的 diff（差异）可以作为附件发布到 Syndie 消息中，从而使 Syndie 能够自托管。

不过，有人有使用这些东西的经验吗？有什么建议吗？

* 6) ???

这次只有 24 屏的文字（包括论坛帖子） ;) 很遗憾我没能参加会议，但一如既往，如果你有任何想法或建议，我非常乐意听取。只需在邮件列表、论坛发帖，或者到 IRC 上来聊聊。

=jr
