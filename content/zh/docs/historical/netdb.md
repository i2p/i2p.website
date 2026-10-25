---
title: "网络数据库讨论"
description: "关于floodfill、Kademlia实验以及netDb未来调优的历史记录"
slug: "netdb"
aliases:
  - "/zh/docs/legacy/netdb"
  - "/zh/docs/legacy/netdb/"
  - "/zh/netdb_discussion"
  - "/zh/netdb_discussion/"
lastUpdated: "2008-03"
accurateFor: "0.7"
---

注意：以下是关于 netDb 实现历史的讨论，并非当前信息。请参阅[主要 netDb 页面](/docs/overview/network-database)获取当前文档。

## 历史 {#status}

netDb 采用一种称为"floodfill"的简单技术进行分布式传播。很久以前，netDb 还使用 Kademlia DHT 作为备用算法。然而，它在我们的应用中效果不佳，在 0.6.1.20 版本中被完全禁用。

*（改编自 jrandom 在旧版 Syndie 中的帖子，2005年11月26日）*

floodfill netDb 实际上只是一个简单且可能是临时的措施，使用最简单的算法 - 将数据发送到 floodfill netDb 中的一个对等节点，等待 10 秒，从 netDb 中随机选择一个对等节点并要求它们发送条目，验证其正确插入/分发。如果验证对等节点没有回复，或者它们没有该条目，发送方会重复这个过程。当 floodfill netDb 中的对等节点从不在 floodfill netDb 中的对等节点接收到 netDb 存储时，它们会将其发送到 floodfill netDb 中的所有对等节点。

在某个时候，Kademlia 搜索/存储功能仍然存在。peers 认为 floodfill peers 对于每个密钥总是比任何不参与 netDb 的 peer 更"接近"。如果 floodfill peers 因某种原因失败，我们会回退到 Kademlia netDb。然而，Kademlia 随后被完全禁用了（见下文）。

最近，Kademlia 在 2009 年末被部分重新引入，作为限制每个 floodfill router 必须存储的 netDb 大小的一种方式。

### Floodfill算法的介绍

Floodfill 在 0.6.0.4 版本中引入，保留 Kademlia 作为备用算法。

*(改编自 jrandom 在旧版 Syndie 中的帖子，2005年11月26日)*

正如我经常说的，我并不特别拘泥于任何特定的技术——对我来说重要的是什么能带来结果。虽然我在过去几年中一直在研究各种 netDb 想法，但我们在过去几周面临的问题已经使其中一些达到了临界点。在实时网络上，将 netDb 冗余因子设置为 4 个节点（意味着我们会持续向新节点发送条目，直到其中 4 个确认收到），并将每个节点的超时时间设置为该节点平均回复时间的 4 倍，我们**仍然**平均需要发送到 40-60 个节点才能获得 4 个存储确认。这意味着发送的消息数量是应该发出数量的 36-56 倍，每条消息都使用 tunnel 并因此跨越 2-4 个链接。更进一步的是，这个值严重偏斜，因为在"失败"存储中（意味着在发送消息 60 秒后少于 4 人确认消息）发送到的平均节点数量在 130-160 个节点范围内。

这太疯狂了，特别是对于一个可能只有250个节点的网络来说。

最简单的答案是说"好吧，废话，jrandom，它坏了。修好它"，但这并不能真正触及问题的核心。与另一个当前的工作一致，我们很可能由于受限路由而存在大量网络问题——一些节点无法与其他某些节点通信，通常是由于NAT或防火墙问题。例如，如果距离特定netDb条目最近的K个节点都位于"受限路由"后面，使得netDb存储消息可以到达它们，但其他节点的netDb查找消息却无法到达，那么该条目将基本上无法访问。沿着这些思路进一步深入，并考虑到一些受限路由将以恶意目的创建的事实，很明显我们必须更仔细地研究长期的netDb解决方案。

有几种替代方案，但特别值得提及的有两种。第一种是简单地将 netDb 作为 Kademlia DHT 运行，使用完整网络的一个子集，其中所有这些节点都是外部可达的。不参与 netDb 的节点仍然会查询这些节点，但它们不会接收未经请求的 netDb 存储或查找消息。参与 netDb 既是自选择的也是用户淘汰的 - router 会选择是否在其 routerInfo 中发布一个标志，声明它们是否想要参与，而每个 router 选择它想要将哪些节点视为 netDb 的一部分（发布该标志但从不提供任何有用数据的节点将被忽略，本质上将它们从 netDb 中排除）。

另一个替代方案是回到过去的爆炸式方法，回归到DTSTTCPW（做最简单可行的事情）思维模式——一个floodfill netDb，但与上面的替代方案一样，只使用完整网络的一个子集。当用户想要将条目发布到floodfill netDb时，他们只需将其发送给参与的router之一，等待ACK确认，然后30秒后查询floodfill netDb中的另一个随机参与者以验证其是否正确分发。如果是的话，太好了；如果不是，只需重复这个过程。当floodfill router收到netDb存储请求时，它们会立即发送ACK确认并将netDb存储排队发送给所有已知的netDb对等节点。当floodfill router收到netDb查找请求时，如果它们有数据，就会回复数据，但如果没有，它们会回复floodfill netDb中其他大约20个对等节点的哈希值。

从网络经济学的角度来看，floodfill netDb 与原始广播 netDb 非常相似，不同之处在于发布条目的成本主要由 netDb 中的对等节点承担，而不是由发布者承担。进一步展开这一点并将 netDb 视为黑盒，我们可以看到 netDb 所需的总带宽为：

```
recvKBps = N * (L + 1) * (1 + F) * (1 + R) * S / T
```
其中：

```
N = number of routers in the entire network
L = average number of client destinations on each router
    (+1 for the routerInfo)
F = tunnel failure percentage
R = tunnel rebuild period, as a fraction of the tunnel lifetime
S = average netDb entry size
T = tunnel lifetime
```
代入几个值：

```
recvKBps = 1000 * (5 + 1) * (1 + 0.05) * (1 + 0.2) * 2KB / 10m
         = 25.2KBps
```
这反过来与 N 成线性比例扩展（在 100,000 个对等节点时，netDb 必须能够处理总计 2.5MBps 的 netDb 存储消息，或者在 300 个对等节点时处理 7.6KBps）。

虽然floodfill netDb会让每个netDb参与者直接接收到客户端生成的netDb存储的一小部分，但它们最终都会接收到所有条目，因此它们的所有链接都应该能够处理完整的recvKBps。反过来，它们都需要发送`(recvKBps/sizeof(netDb)) * (sizeof(netDb)-1)`来保持其他对等节点的同步。

一个 floodfill netDb 既不需要为 netDb 操作进行 tunnel 路由，也不需要对其能够"安全"回答的条目进行任何特殊选择，因为基本假设是它们都存储着所有内容。哦，关于 netDb 所需的磁盘使用量，对于任何现代机器来说仍然相当微不足道，每1000个对等节点大约需要11MB `(N * (L + 1) * S)`。

Kademlia netDb 将减少这些数字，理想情况下将它们降低到 K 乘以 M 分之一的值，其中 K = 冗余因子，M 是 netDb 中的 router 数量（例如 5/100，在 100,000 个 router 时产生 126KBps 的 recvKBps 和 536MB）。然而 Kademlia netDb 的缺点是在恶意环境中安全运行的复杂性增加了。

我现在考虑的是简单地在我们现有的活跃网络中实现和部署一个 floodfill netDb，让想要使用它的节点挑选出其他被标记为成员的节点并查询它们，而不是查询传统的 Kademlia netDb 节点。在这个阶段，带宽和磁盘需求都是微不足道的（7.6KBps 和 3MB 磁盘空间），这将完全从调试计划中移除 netDb - 剩余需要解决的问题将由与 netDb 无关的其他因素引起。

如何选择节点来发布标志表明它们是 floodfill netDb 的一部分？在开始时，这可以作为高级配置选项手动完成（如果 router 无法验证其外部可达性则忽略）。如果太多节点设置了该标志，netDb 参与者如何选择要剔除哪些节点？同样，在开始时这可以作为高级配置选项手动完成（在丢弃不可达的节点之后）。我们如何避免 netDb 分区？通过让 router 查询 K 个随机的 netDb 节点来验证 netDb 是否正确执行 flood fill。不参与 netDb 的 router 如何发现新的 router 来建立隧道？也许可以通过发送特定的 netDb 查询来实现，这样 netDb router 将不会响应 netDb 中的节点，而是响应 netDb 外部的随机节点。

I2P的netDb与传统的负载承载DHT非常不同——它只携带网络元数据，而不携带任何实际载荷，这就是为什么即使使用floodfill算法的netDb也能够承载任意数量的I2P站点/IRC/bt/邮件/syndie等数据。随着I2P的发展，我们甚至可以进行一些优化来进一步分散负载（比如在netDb参与者之间传递布隆过滤器，以了解他们需要共享什么），但目前看来我们可以使用更简单的解决方案。

有一个事实值得深入探讨 - 并非所有 leaseSet 都需要发布到 netDb 中！实际上，大多数都不需要 - 只有那些会接收主动消息（即服务器）的目标才需要。这是因为从一个目标发送到另一个目标的 garlic 加密包装消息已经捆绑了发送者的 leaseSet，这样这两个目标之间的任何后续发送/接收（在短时间内）都可以在没有任何 netDb 活动的情况下工作。

所以，回到这些等式，我们可以将L从5改为大约0.1（假设每50个目标中只有1个是服务器）。之前的等式也忽略了回应客户端查询所需的网络负载，但虽然这个负载变化很大（基于用户活动），但与发布频率相比，很可能是非常微不足道的。

总之，虽然仍然没有什么神奇的效果，但带宽/磁盘空间需求减少了近1/5，这是一个不错的改善（以后可能会更多，这取决于routerInfo分发是直接作为对等连接建立的一部分，还是仅通过netDb进行）。

### 禁用 Kademlia 算法

Kademlia 在 0.6.1.20 版本中被完全禁用。

*（改编自 2007 年 11 月与 jrandom 的 IRC 对话）*

Kademlia需要基准网络无法提供的最低服务水平（带宽、CPU），即使加入分层机制后也是如此（纯粹的Kademlia在这一点上是荒谬的）。Kademlia根本无法工作。这是一个不错的想法，但不适用于敌对且不稳定的环境。

### 当前状态

netDb 在 I2P 网络中发挥着非常特定的作用，算法已经针对我们的需求进行了调优。这也意味着它还没有针对我们尚未遇到的需求进行调优。I2P 目前规模相对较小（几百个 router）。有一些计算表明，3-5 个 floodfill router 应该能够处理网络中的 10,000 个节点。netDb 实现在目前完全能够满足我们的需求，但随着网络的增长，可能还需要进一步的调优和错误修复。

### 计算更新 03-2008

当前数据：

```
recvKBps = N * (L + 1) * (1 + F) * (1 + R) * S / T
```
其中：

```
N = number of routers in the entire network
L = average number of client destinations on each router
    (+1 for the routerInfo)
F = tunnel failure percentage
R = tunnel rebuild period, as a fraction of the tunnel lifetime
S = average netDb entry size
T = tunnel lifetime
```
假设变化：

- L 现在大约是 .5，相比上面的 .1，这是由于 i2psnark 和其他应用程序的流行。
- F 大约是 .33，但 tunnel 测试中的错误在 0.6.1.33 中已修复，所以会变得好很多。
- 由于 netDb 大约有 2/3 的 5K routerInfos 和 1/3 的 2K leaseSets，所以 S = 4K。
  RouterInfo 大小在 0.6.1.32 和 0.6.1.33 中正在缩小，因为我们移除了不必要的统计信息。
- R = tunnel 构建周期：0.2 是一个非常低的值 - 可能是 0.7 - 
  但 0.6.1.32 中 build 算法的改进应该会在网络升级时将其降低到大约 0.2。
  现在称之为 0.5，网络中有一半处于 .30 或更早版本。

```
recvKBps = 700 * (0.5 + 1) * (1 + 0.33) * (1 + 0.5) * 4KB / 10m
         ~= 28KBps
```
这只是考虑了存储 - 那查询呢？

### Kademlia 算法的回归？

*(改编自2007年1月2日I2P会议)*

Kademlia netDb 就是无法正常工作。它是永久失效了还是会重新启用？如果重新启用，Kademlia netDb 中的节点将是网络中 router 的一个非常有限的子集（基本上是扩展数量的 floodfill 节点，如果/当 floodfill 节点无法处理负载时）。但在 floodfill 节点无法处理负载之前（以及无法添加其他能够处理的节点之前），这是不必要的。

### Floodfill的未来

*（改编自与jrandom在11/07的IRC对话）*

这里有一个提议：容量等级 O 自动成为 floodfill。嗯。除非我们确定，否则我们可能最终会以一种花哨的方式对所有 O 级 router 进行 DDoS 攻击。这确实是个问题：我们希望确保 floodfill 的数量尽可能少，同时提供足够的可达性。如果/当 netDb 请求失败时，我们需要增加 floodfill 节点的数量，但目前，我不知道有 netDb 获取问题。根据我的记录，有 33 个 "O" 级节点。33 个对于 floodfill 来说是/很多/的。

所以floodfill在该池中的对等节点数量被严格限制时效果最佳？而且floodfill池的大小不应该增长太多，即使网络本身会逐渐增长？据我记得，3-5个floodfill对等节点可以处理10K个router（我在旧的syndie中发布了一堆解释详细信息的数字）。这听起来是自动选择加入很难满足的要求，特别是如果选择加入的节点无法信任来自其他节点的数据。例如"让我看看我是否在前5名中"，并且只能信任关于自己的数据（例如"我肯定是O级，传输速度150 KB/s，运行了123天"）。而且前5名也是有敌意的。基本上，这和tor目录服务器一样——由受信任的人（即开发者）选择。是的，现在它可能被选择加入利用，但这很容易检测和处理。看起来最终，我们可能需要比Kademlia更有用的东西，并且只让合理有能力的对等节点加入该方案。N级及以上应该是足够大的数量来抑制对手造成拒绝服务攻击的风险，我希望如此。但那样的话，它必须与floodfill不同，即不会造成巨大的流量。大数量？对于基于DHT的netDb？不一定基于DHT。

### Floodfill 待办事项列表 {#todo}

注意：以下信息已过时。请查看[主要 netDb 页面](/docs/overview/network-database)了解当前状态和未来工作列表。

2008年3月13日，网络只剩下一个 floodfill 运行了几个小时（大约UTC时间18:00 - 20:00），这造成了很多麻烦。

在 0.6.1.33 中实施的两个变更应该能够减少由 floodfill 节点移除或变动造成的中断：

1. 每次随机化用于搜索的 floodfill 节点。
   这将最终帮助你绕过那些失效的节点。
   这个改变还修复了一个严重的 bug，该 bug 有时会让 floodfill 搜索代码陷入混乱。
2. 优先选择正在运行的 floodfill 节点。
   代码现在会尽可能避免使用那些被列入黑名单、失效或半小时内未收到消息的节点。

一个好处是更快地首次联系到 I2P Site（即当你需要首先获取 leaseset 时）。查找超时时间是10秒，所以如果你不是从询问一个宕机的对等节点开始，你可以节省10秒时间。

这些更改*可能*存在匿名性影响。例如，在 floodfill **存储**代码中，有注释说明不会避开被列入黑名单的节点，因为一个节点可能是"垃圾"的，然后看看会发生什么。搜索比存储的漏洞要少得多——它们频率更低，泄露的信息也更少。所以也许我们不认为需要担心这个问题？但如果我们想要调整这些更改，向被列为"下线"或被列入黑名单的节点发送消息仍然很容易，只是不将其计入我们要发送的2个节点中（因为我们实际上不期望得到回复）。

有几个地方会选择 floodfill 节点 - 这个修复只解决了其中一个 - 普通节点从哪里搜索 [一次2个]。其他应该实现更好 floodfill 选择的地方：

1. 常规节点存储到的对象 [一次1个]
   (随机 - 需要添加限定条件，因为超时时间很长)
2. 常规节点搜索以验证存储的对象 [一次1个]
   (随机 - 需要添加限定条件，因为超时时间很长)
3. floodfill节点在搜索失败时回复的对象 (距离搜索最近的3个)
4. floodfill节点泛洪到的对象 (所有其他floodfill节点)
5. 在NTCP每6小时"窃语"中发送的floodfill节点列表
   (尽管由于其他floodfill改进，这可能不再必要)

还有很多可以做且应该做的事情：

- 使用"dbHistory"统计信息更好地评估 floodfill 节点的集成度
- 使用"dbHistory"统计信息立即响应不回复的 floodfill 节点
- 在重试方面更智能 - 重试由上层处理，而不是在 FloodOnlySearchJob 中，所以它会进行另一次随机排序并重新尝试，而不是有目的地跳过我们刚刚尝试过的 ff 节点。
- 进一步改进集成统计信息
- 实际使用集成统计信息，而不仅仅是 netDb 中的 floodfill 指示
- 也使用延迟统计信息？
- 在识别失效的 floodfill 节点方面进一步改进

最近完成：

- [在 Release 0.6.3 中]
  基于网络分析，为一定比例的 O 类节点实现自动选择加入 floodfill
- [在 Release 0.6.3 中]
  继续减少 netDb 条目大小以减少 floodfill 流量 -
  我们现在已达到监控网络所需的最小统计数据数量。
- [在 Release 0.6.3 中]
  手动排除 floodfill 节点列表
  （按 router 身份的[屏蔽列表](/docs/overview/threat-model#blocklist)）
- [在 Release 0.6.3 中]
  更好的存储 floodfill 节点选择：
  避免选择 netDb 过时、最近存储失败或被永久列入黑名单的节点。
- [在 Release 0.6.4 中]
  优先选择已连接的 floodfill 节点进行 RouterInfo 存储，以
  减少与 floodfill 节点的直接连接数量。
- [在 Release 0.6.5 中]
  不再是 floodfill 的节点在响应查询时发送其 routerInfo，
  以便执行查询的 router 知道它不再是 floodfill。
- [在 Release 0.6.5 中]
  进一步调整自动成为 floodfill 的要求
- [在 Release 0.6.5 中]
  修复响应时间分析，为优先选择快速 floodfill 做准备
- [在 Release 0.6.5 中]
  改进屏蔽列表功能
- [在 Release 0.7 中]
  修复 netDb 探索
- [在 Release 0.7 中]
  默认启用屏蔽列表，屏蔽已知的问题制造者
- [最近几个版本中的多项改进，持续努力中]
  减少高带宽和 floodfill router 的资源需求

这是一个很长的清单，但要让网络能够抵御大量节点频繁开关 floodfill 开关或伪装成 floodfill router 所造成的拒绝服务攻击，就需要做这么多工作。当我们只有两个 ff router，并且它们都是 24/7 运行时，这些都不是问题。再次说明，jrandom 的缺席让我们看到了需要改进的地方。

为了协助这项工作，从 0.6.1.33 版本开始，floodfill 节点的额外配置文件数据现在会显示在路由器控制台的"配置文件"页面中。我们将使用这些数据来分析哪些数据适合用于评估 floodfill 节点。

网络目前相当有韧性，但我们将继续改进用于测量和响应 floodfill 节点性能和可靠性的算法。虽然我们目前还没有完全防御恶意 floodfill 或 floodfill DDOS 的潜在威胁，但大部分基础设施已经到位，我们已做好充分准备，能够在需要时迅速做出反应。
