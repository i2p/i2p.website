---
title: "节点分析和选择"
description: "I2P router 如何分析和选择节点来构建 tunnel"
slug: "peer-selection"
aliases:
  - "/zh/how_peerselection"
  - "/zh/how_peerselection/"
lastUpdated: "2024-02"
accurateFor: "0.9.62"
---

## 注意

本页面描述了截至2010年Java I2P实现的节点分析和选择机制。虽然大体上仍然准确，但一些细节可能已不再正确。我们持续改进封禁、阻止和选择策略，以应对新的威胁、攻击和网络状况。当前网络有多个router实现版本。其他I2P实现可能有完全不同的分析和选择策略，或者可能根本不使用分析。

## 概述 {#overview}

### 节点性能分析 {#profiling}

**对等节点分析**是基于**观察到的**其他 router 或对等节点性能收集数据，并将这些对等节点分类到不同组别的过程。分析过程**不会**使用对等节点自身在[网络数据库](/docs/overview/network-database)中发布的任何声称的性能数据。

配置文件用于两个目的：

1. 选择用于中继我们流量的节点，详见下文
2. 从 floodfill router 集合中选择用于网络数据库存储和查询的节点，
   详见[网络数据库](/docs/overview/network-database)页面

### 节点选择 {#selection}

**Peer selection** 是选择网络上哪些 router 来中继我们的消息（我们将邀请哪些节点加入我们的 tunnel）的过程。为了实现这一点，我们跟踪每个节点的表现（节点的"profile"），并使用这些数据来估算它们的速度、接受我们请求的频率，以及它们是否看起来过载或无法可靠地执行它们同意的任务。

与其他一些匿名网络不同，在 I2P 中，声明的带宽是不可信的，**仅**用于避免选择那些声明带宽过低而不足以用于路由 tunnel 的节点。所有节点选择都是通过性能分析来完成的。这可以防止基于节点声明高带宽来捕获大量 tunnel 的简单攻击。它也使[时序攻击](/docs/overview/threat-model#timing)变得更加困难。

对等节点选择执行得相当频繁，因为一个 router 可能维护大量的客户端和探索性 tunnel，而 tunnel 的生命周期只有 10 分钟。

### 更多信息 {#further-info}

更多信息请参见在 [PET-CON 2009.1](http://web.archive.org/web/20100413184504/http://www.pet-con.org/index.php/PET_Convention_2009.1) 上发表的论文 [Peer Profiling and Selection in the I2P Anonymous Network](/pdf/I2P-PET-CON-2009.1.pdf)。论文发表后的一些小改动请参见[下面](#notes)的注释。

## 配置文件 {#profiles}

每个节点都有一组关于它们的数据点收集，包括它们回复 netDb 查询需要多长时间的统计数据，它们的 tunnel 失败频率，以及它们能够向我们介绍多少新节点，还有一些简单的数据点，比如我们最后一次收到它们消息的时间或最后一次通信错误发生的时间。

Profiles 相当小，只有几 KB。为了控制内存使用，随着 profiles 数量的增长，profile 过期时间会缩短。Profiles 保存在内存中直到 router 关闭，此时它们会被写入磁盘。在启动时，会读取 profiles，因此 router 无需重新初始化所有 profiles，从而允许 router 在启动后快速重新融入网络。

## 节点摘要 {#summaries}

虽然配置文件本身可以被视为对等节点性能的摘要，但为了实现有效的对等节点选择，我们将每个摘要分解为四个简单的值，分别表示对等节点的速度、容量、它在网络中的集成程度，以及是否存在故障。

### 速度 {#speed}

速度计算只是通过配置文件并估计我们在一分钟内通过该节点在单个 tunnel 上可以发送或接收多少数据。对于这个估计，它只查看前一分钟的性能表现。

### 容量 {#capacity}

容量计算只是遍历配置文件，估算节点在给定时间段内愿意参与的tunnel数量。为了进行这个估算，它会查看节点接受、拒绝和丢弃了多少tunnel构建请求，以及有多少已同意的tunnel后来失败了。虽然计算采用时间加权，使得近期活动比较早的活动权重更高，但可能会包含长达48小时的统计数据。

识别和避免不可靠及无法访问的节点至关重要。不幸的是，由于tunnel构建和测试需要多个节点的参与，很难准确识别构建请求丢失或测试失败的根本原因。router会为每个节点分配失败概率，并在容量计算中使用该概率。丢包和测试失败的权重远高于拒绝。

## 对等节点组织 {#organization}

如上所述，我们深入分析每个对等节点的配置文件来得出一些关键计算结果，基于这些结果，我们将每个对等节点组织为三个组别——快速、高容量和标准。

这些分组并不是相互排斥的，也不是毫不相关的：

- 如果节点的容量计算达到或超过所有节点的中位数，则该节点被认为是"高容量"的。
- 如果节点已经是"高容量"且其速度计算达到或超过所有节点的中位数，则该节点被认为是"快速"的。
- 如果节点不是"高容量"，则该节点被认为是"标准"的。

### 群组大小限制 {#group-limits}

群组的大小可能会受到限制。

- 快速组限制为30个对等节点。
  如果会有更多，只有速度评级最高的节点会被放入该组。
- 高容量组限制为75个对等节点（包括快速组）。
  如果会有更多，只有容量评级最高的节点会被放入该组。
- 标准组没有固定限制，但比存储在本地网络数据库中的RouterInfo数量要少一些。
  在当今网络中的活跃router上，可能有大约1000个RouterInfo和500个对等节点配置文件（包括快速组和高容量组中的那些）。

## 重新计算和稳定性 {#recalculation}

摘要每45秒重新计算一次，peers会重新分组排序。

这些分组往往相当稳定，也就是说，在每次重新计算时排名变化不大。处于快速和高容量分组中的节点会有更多 tunnel 通过它们构建，这提高了它们的速度和容量评级，从而进一步巩固了它们在该分组中的地位。

## 节点选择 {#peer-selection}

router从上述组中选择节点来构建tunnel。

### 客户端隧道的节点选择 {#client-tunnels}

客户端 tunnel 用于应用程序流量，例如 HTTP 代理和 Web 服务器。

为了减少对[某些攻击](http://blog.torproject.org/blog/one-cell-enough)的易感性并提高性能，用于构建客户端 tunnel 的节点是从最小的组（即"快速"组）中随机选择的。在选择节点时，不会偏向于选择之前曾参与同一客户端 tunnel 的节点。

### 探索性隧道的节点选择 {#exploratory-tunnels}

探索性tunnel用于router管理目的，例如网络数据库流量和测试客户端tunnel。探索性tunnel也用于联系以前未连接的router，这就是为什么它们被称为"探索性"的原因。这些tunnel通常是低带宽的。

用于构建探索性 tunnel 的节点通常从标准组中随机选择。如果这些构建尝试的成功率相比客户端 tunnel 构建成功率较低，router 将改为从高容量组中随机选择节点的加权平均值。这有助于即使在网络性能较差时也能保持令人满意的构建成功率。选择节点时不会偏向于之前参与过探索性 tunnel 的节点。

由于标准组包含了 router 所知道的绝大部分对等节点，探索性 tunnel 实质上是通过从所有对等节点中随机选择来构建的，直到构建成功率变得过低为止。

### 限制 {#restrictions}

为了防止一些简单的攻击并提升性能，存在以下限制：

- 来自同一个 /16 IP 空间的两个对等节点不能在同一个 tunnel 中。
- 一个对等节点最多只能参与该 router 创建的所有 tunnel 的 33%。
- 带宽极低的对等节点不会被使用。
- 最近连接尝试失败的对等节点不会被使用。

### 隧道中的节点排序 {#ordering}

Peers 在 tunnel 内部是有序排列的，以应对[前驱攻击](http://forensics.umass.edu/pubs/wright-tissec.pdf)（[2008年更新](http://forensics.umass.edu/pubs/wright.tissec.2008.pdf)）。更多信息请参见 [tunnel 页面](/docs/specs/tunnel-implementation#ordering)。

## 未来工作 {#future}

- 根据需要继续分析和调整速度和容量计算
- 如有必要，实施更激进的淘汰策略以控制内存使用，适应网络增长
- 评估群组大小限制
- 如果配置了，使用 GeoIP 数据来包含或排除某些对等节点

## 注意事项 {#notes}

对于那些正在阅读论文[I2P匿名网络中的节点分析和选择](/pdf/I2P-PET-CON-2009.1.pdf)的读者，请注意自该论文发表以来I2P的以下小幅变化：

- Integration 计算仍未使用
- 在论文中，"groups"被称为"tiers"
- "Failing" tier 不再使用
- "Not Failing" tier 现在被命名为"Standard"

## 参考资料 {#references}

- [I2P 匿名网络中的节点分析和选择](/pdf/I2P-PET-CON-2009.1.pdf)
- [一个信元就足够](http://blog.torproject.org/blog/one-cell-enough)
- [Tor 入口守卫](https://wiki.torproject.org/noreply/TheOnionRouter/TorFAQ#EntryGuards)
- [Murdoch 2007 论文](http://freehaven.net/anonbib/#murdoch-pet2007)
- [Tor 调优](http://www.crhc.uiuc.edu/~nikita/papers/tuneup-cr.pdf)
- [针对 Tor 的低资源路由攻击](http://cs.gmu.edu/~mccoy/papers/wpes25-bauer.pdf)
