---
title: "网络数据库讨论"
description: "关于 floodfill、Kademlia（分布式哈希表算法）实验，以及对 netDb 的未来调优的历史说明"
slug: "netdb"
reviewStatus: "needs-review"
---

> **注意：** 本存档讨论概述了针对网络数据库（netDb）的历史性方法。有关当前行为和指导，请参阅[netDb 主文档](/docs/specs/common-structures/)。

## 历史

I2P 的 netDb 使用一种简单的 floodfill 算法进行分发。早期版本还保留了一个 Kademlia DHT 的后备实现，但事实证明它不可靠，并在 0.6.1.20 版本中被完全禁用。floodfill 的设计会将发布的条目转发给一个参与的 router，等待确认，并在必要时与其他 floodfill 对等体重试。floodfill 对等体会将来自非 floodfill router 的存储消息广播给所有其他 floodfill 参与者。

在2009年末，为了减轻各个 floodfill routers 的存储负担，Kademlia 查询被部分重新引入。

### floodfill 简介

floodfill 最初出现在 0.6.0.4 版本中，而 Kademlia（一种分布式哈希表算法）仍作为后备方案可用。当时，严重的丢包和受限的路由使得从四个最近的对等节点获取确认变得困难，往往需要进行数十次冗余的存储尝试。转而采用由外部可达 routers 组成的 floodfill 子集，提供了一个务实的短期解决方案。

### 重新思考 Kademlia（分布式哈希表协议）

曾考虑的替代方案包括：

- 将 netDb 作为 Kademlia DHT（Kademlia 分布式哈希表）运行，且仅限选择参与并可达的 routers
- 保留 floodfill 模型，但将参与限制为有能力的 routers，并通过随机检查验证分布情况

floodfill 方法之所以胜出，是因为它更易于部署，而且 netDb 只承载元数据，而不承载用户数据。大多数目的地从不发布 LeaseSet，因为发送方通常会在 garlic messages（I2P 中用于将多条消息捆绑的封装机制）中捆绑其 LeaseSet。

## 当前状态（历史视角）

netDb（网络数据库）算法经过针对网络需求的调优，并且从历史上看可以从容应对几百个 router。早期的估算表明，3–5 个 floodfill router（负责存储和分发 netDb 条目的特殊 router）即可支撑大约 10,000 个节点。

### 更新的计算（2008年3月）

```
recvKBps = N * (L + 1) * (1 + F) * (1 + R) * S / T
```
其中：

- `N`: 网络中的 Routers 数量
- `L`: 每个 router 的客户端目的地平均数量（另加一个用于 `RouterInfo`）
- `F`: Tunnel 失败百分比
- `R`: 以 Tunnel 生命周期的分数表示的重建周期
- `S`: 平均 netDb 条目大小
- `T`: Tunnel 生命周期

使用 2008 年时期的参数取值（`N = 700`，`L = 0.5`，`F = 0.33`，`R = 0.5`，`S = 4 KB`，`T = 10 minutes`）得到：

```
recvKBps ≈ 700 * (0.5 + 1) * (1 + 0.33) * (1 + 0.5) * 4 KB / 10m ≈ 28 KBps
```
### Kademlia（DHT 分布式哈希表算法）会回归吗？

开发者在2007年初左右讨论了重新引入 Kademlia（分布式哈希表算法）。共识是：可以按需逐步扩展 floodfill 的容量，而 Kademlia 会为普通的 router 群体带来显著的复杂性和资源需求。除非 floodfill 容量变得不足，否则后备机制保持休眠状态。

### Floodfill 容量规划

将带宽等级为 `O` 的 routers 自动纳入 floodfill，虽然很有诱惑力，但如果敌对节点选择加入，则可能引发拒绝服务（DoS）场景的风险。历史分析表明，限制 floodfill 池（例如由 3–5 个对等体处理 ~10K 个 routers）更为安全。为维持一个既充足又受控的 floodfill 集，曾采用受信任的运营者或自动启发式方法。

## Floodfill 待办事项（历史）

> 本部分保留以作存档。netDb（网络数据库）主页面跟踪当前的路线图和设计考量。

诸如 2008 年 3 月 13 日期间仅有一个可用的 floodfill router 之类的运行事件，促使在 0.6.1.33 至 0.7.x 版本中交付了多项改进，包括：

- 随机化用于搜索的 floodfill 选择，并优先选择响应迅速的节点
- 在 router 控制台的 "Profiles" 页面显示更多 floodfill 指标
- 逐步缩小 netDb 条目大小，以降低 floodfill 带宽占用
- 基于通过节点档案数据收集到的性能，为部分 class `O` routers 自动选择加入
- 增强的封锁列表、floodfill 节点选择及探索启发式

那个时期遗留下来的想法包括：

- 使用 `dbHistory` 统计数据以更好地评估并选择 floodfill 对等节点
- 改进重试行为，避免反复联系故障对等节点
- 在选择过程中利用时延指标和 integration（集成）评分
- 更快速地检测并响应故障的 floodfill routers
- 继续降低对高带宽节点和 floodfill 节点的资源需求

即便在撰写这些说明时，网络仍被认为具有较强的弹性，并已建立起相应的基础设施，可以快速应对敌对的 floodfills 或以 floodfill 为目标的拒绝服务攻击。

## 补充说明

- router 控制台长期提供了增强的画像数据，以帮助分析 floodfill 的可靠性。
- 虽然历史上的一些评论曾推测采用 Kademlia 或其他分布式哈希表（DHT）方案，但在生产网络中，floodfill 仍然是主要算法。
- 前瞻性研究致力于在限制滥用机会的同时，使 floodfill 的准入具备自适应能力。
