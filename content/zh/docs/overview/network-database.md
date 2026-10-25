---
title: "Network Database（网络数据库）"
description: "理解I2P的分布式网络数据库(netDb) - 一个专门用于router联系信息和目标查找的DHT"
slug: "network-database"
aliases:
  - "/zh/how_networkdatabase"
  - "/zh/how_networkdatabase/"
lastUpdated: "2025-03"
accurateFor: "0.9.65"
---

## 概述

I2P的netDb是一个专门的分布式数据库，仅包含两种类型的数据 - router联系信息（**RouterInfos**）和目标联系信息（**LeaseSets**）。每条数据都由相应方签名，并由任何使用或存储它的人进行验证。此外，数据内部包含活跃性信息，允许丢弃无关条目，用较新条目替换较旧条目，并防范某些类别的攻击。

netDb 使用一种名为 "floodfill" 的简单技术进行分发，其中所有 router 的一个子集，称为 "floodfill router"，负责维护这个分布式数据库。

---

## RouterInfo

当一个 I2P router 想要联系另一个 router 时，它们需要知道一些关键的数据片段 - 所有这些都被 router 打包并签名到一个称为 "RouterInfo" 的结构中，该结构以 router 身份的 SHA256 作为键进行分发。该结构本身包含：

- router的身份（一个加密密钥、一个签名密钥和一个证书）
- 可以联系到它的联系地址
- 发布时间
- 一组任意的文本选项
- 上述内容的签名，由身份的签名密钥生成

### 期望选项

以下文本选项虽然不是严格要求的，但预期应该存在：

- **caps** (能力标志 - 用于指示 floodfill 参与情况、大致带宽和感知可达性)
  - **D**: 中度拥塞 (自 0.9.58 版本起)
  - **E**: 高度拥塞 (自 0.9.58 版本起)
  - **f**: Floodfill
  - **G**: 拒绝所有 tunnel (自 0.9.58 版本起)
  - **H**: 隐藏
  - **K**: 低于 12 KBps 共享带宽
  - **L**: 12 - 48 KBps 共享带宽 (默认)
  - **M**: 48 - 64 KBps 共享带宽
  - **N**: 64 - 128 KBps 共享带宽
  - **O**: 128 - 256 KBps 共享带宽
  - **P**: 256 - 2000 KBps 共享带宽 (自 0.9.20 版本起，见下方注释)
  - **R**: 可达
  - **U**: 不可达
  - **X**: 超过 2000 KBps 共享带宽 (自 0.9.20 版本起，见下方注释)

"共享带宽" == (共享 %) * min(入站带宽, 出站带宽)

为了与较旧的 router 兼容，一个 router 可能会发布多个带宽字母，例如"PO"。

注意：P 和 X 带宽等级之间的边界可能是 2000 或 2048 KBps，由实现者选择。

- **netId** = 2 (基本网络兼容性 - router 将拒绝与具有不同 netId 的对等节点通信)
- **router.version** (用于确定与新功能和消息的兼容性)

关于 R/U 能力的注意事项：router 通常应该发布 R 或 U 能力，除非可达性状态目前未知。R 表示 router 在至少一个传输地址上是直接可达的（不需要介绍者，未被防火墙阻挡）。U 表示 router 在任何传输地址上都不是直接可达的。

已弃用选项：- ~~coreVersion~~ （从未使用，在 0.9.24 版本中移除）- ~~stat_uptime~~ = 90m （自 0.7.9 版本起未使用，在 0.9.24 版本中移除）

这些值被其他 router 用于基本决策。我们是否应该连接到这个 router？我们是否应该尝试通过这个 router 路由 tunnel？特别是带宽能力标志，仅用于确定 router 是否满足路由 tunnel 的最低阈值。超过最低阈值后，广播的带宽在 router 中的任何地方都不会被使用或信任，除了在用户界面中显示以及用于调试和网络分析。

有效的 NetID 编号：

| 用途 | NetID 编号 |
|-------|--------------|
| 保留 | 0 |
| 保留 | 1 |
| 当前网络（默认） | 2 |
| 保留的未来网络 | 3 - 15 |
| 分叉和测试网络 | 16 - 254 |
| 保留 | 255 |
### 其他选项

附加文本选项包括少量关于 router 健康状况的统计信息，这些信息被 [stats.i2p](http://stats.i2p/) 等站点汇总，用于网络性能分析和调试。选择这些统计信息是为了向开发人员提供关键数据，例如 tunnel 构建成功率，同时平衡对此类数据的需求与泄露这些数据可能产生的副作用。当前统计信息仅限于：

- 探索性隧道构建成功率、拒绝率和超时率
- 1小时内参与隧道的平均数量

这些是可选的，但如果包含的话，有助于分析网络范围的性能。从API 0.9.58开始，这些统计数据已被简化和标准化，如下所示：

- 选项键为 stat_(统计名称).(统计周期)
- 选项值以 ';' 分隔
- 事件计数或标准化百分比的统计使用第4个值；前三个值未使用但必须存在
- 平均值统计使用第1个值，不需要 ';' 分隔符
- 为了在统计分析中对所有 router 进行等权重处理，以及为了额外的匿名性，router 应该仅在运行时间达到一小时或更长时间后才包含这些统计信息，并且只在每16次发布 RI 时包含一次。

示例：

```
stat_tunnel.buildExploratoryExpire.60m = 0;0;0;53.14
stat_tunnel.buildExploratoryReject.60m = 0;0;0;15.51
stat_tunnel.buildExploratorySuccess.60m = 0;0;0;31.35
stat_tunnel.participatingTunnels.60m = 289.20
```
Floodfill router 可能会发布关于其网络数据库中条目数量的额外数据。这些数据是可选的，但如果包含的话，有助于分析全网性能。

以下两个选项应该被 floodfill router 包含在每个发布的 RI 中：

- **netdb.knownLeaseSets**
- **netdb.knownRouters**

示例：

```
netdb.knownLeaseSets = 158
netdb.knownRouters = 11374
```
发布的数据可以在 router 的用户界面中查看，但不会被任何其他 router 使用或信任。

### 家族选项

从0.9.24版本开始，router可以声明它们属于同一个"家族"，由同一实体运营。同一家族中的多个router不会被用在单个tunnel中。

family 选项包括：

- **family** (家族名称)
- **family.key** 家族的 [Signing Public Key](/docs/specs/common-structures/#type_SigningPublicKey) 的签名类型代码（ASCII 数字）连接 ':' 再连接 base 64 格式的 Signing Public Key
- **family.sig** ((UTF-8 格式的家族名称) 连接 (32 字节 router 哈希)) 的签名，采用 base 64 格式

### RouterInfo 过期

RouterInfo 没有固定的过期时间。每个 router 可以自由维护自己的本地策略，在 RouterInfo 查找频率与内存或磁盘使用之间进行权衡。在当前实现中，有以下通用策略：

- 在运行时间的第一个小时内没有过期机制，因为持久存储的数据可能已经过时。
- 如果 RouterInfo 数量为 25 个或更少，则没有过期机制。
- 随着本地 RouterInfo 数量的增长，过期时间会缩短，以尝试维持合理的 RouterInfo 数量。当路由器少于 120 个时，过期时间为 72 小时，而当路由器数量为 300 个时，过期时间约为 30 小时。
- 包含 [SSU](/docs/legacy/ssu/) introducer 的 RouterInfo 在大约一小时后过期，因为 introducer 列表大约在那个时间过期。
- Floodfill 对所有本地 RouterInfo 使用短过期时间（1 小时），因为有效的 RouterInfo 会频繁地重新发布给它们。

### RouterInfo 持久化存储

RouterInfo会定期写入磁盘，以便在重启后仍然可用。

可能需要持久存储具有长过期时间的元 LeaseSet。这取决于具体实现。

### 另请参阅

- [RouterInfo 规范](/docs/specs/common-structures/#struct_RouterInfo)
- [RouterInfo Javadoc](http://idk.i2p/javadoc-i2p/net/i2p/data/router/RouterInfo.html)

---

## LeaseSet

在 netDb 中分发的第二种数据是"LeaseSet"——记录特定客户端目标的一组**tunnel 入口点（leases）**。每个 lease 都指定以下信息：

- tunnel 网关 router（通过指定其身份）
- 该 router 上用于发送消息的 tunnel ID（一个 4 字节数字）
- 该 tunnel 何时过期。

leaseSet 本身存储在 netDb 中，使用从目标地址 SHA256 派生的密钥。一个例外是加密 leaseSet (LS2)，从 0.9.38 版本开始。DHT 密钥使用类型字节 (3) 后跟盲化公钥的 SHA256，然后按常规轮换。请参见下面的 Kademlia 接近度度量部分。

除了这些租约之外，LeaseSet 还包括：

- 目标本身（一个加密密钥、一个签名密钥和一个证书）
- 附加加密公钥：用于 garlic 消息的端到端加密
- 附加签名公钥：用于 LeaseSet 撤销，但目前未使用。
- 所有 LeaseSet 数据的签名，以确保目标发布了该 LeaseSet。

- [Lease 规范](/docs/specs/common-structures/#struct_Lease)
- [LeaseSet 规范](/docs/specs/common-structures/#struct_LeaseSet)
- [Lease Javadoc](http://idk.i2p/javadoc-i2p/net/i2p/data/Lease.html)
- [LeaseSet Javadoc](http://idk.i2p/javadoc-i2p/net/i2p/data/LeaseSet.html)

从 0.9.38 版本开始，定义了三种新类型的 leaseSet：LeaseSet2、MetaLeaseSet 和 EncryptedLeaseSet。详见下文。

### 未发布的 LeaseSet

仅用于出站连接的目标地址的 leaseSet 是*未发布的*。它从不发送到 floodfill router 进行发布。"客户端" tunnel，比如用于网页浏览和 IRC 客户端的 tunnel，都是未发布的。服务器仍然能够向这些未发布的目标地址发送消息，这是因为 [I2NP 存储消息](#leaseset-storage-to-peers)。

### 已撤销的 LeaseSet

LeaseSet 可以通过发布一个包含零个租约的新 LeaseSet 来*撤销*。撤销操作必须由 LeaseSet 中的附加签名密钥进行签名。撤销功能尚未完全实现，目前尚不清楚是否有任何实际用途。这是该签名密钥的唯一计划用途，因此目前处于未使用状态。

### LeaseSet2 (LS2)

从 0.9.38 版本开始，floodfill 支持新的 LeaseSet2 结构。这个结构与旧的 LeaseSet 结构非常相似，并且具有相同的用途。新结构提供了支持新加密类型、多种加密类型、选项、离线签名密钥和其他功能所需的灵活性。详情请参阅提案 123。

### 元 LeaseSet (LS2)

从 0.9.38 版本开始，floodfill 支持新的 Meta LeaseSet 结构。该结构在 DHT 中提供树状结构，用于引用其他 LeaseSets。使用 Meta LeaseSets，站点可以实现大型多宿主服务，其中使用多个不同的 Destinations 来提供共同的服务。Meta LeaseSet 中的条目是 Destinations 或其他 Meta LeaseSets，并且可能具有很长的过期时间，最长可达 18.2 小时。使用此功能，应该可以运行数百或数千个 Destinations 来托管共同的服务。详情请参见提案 123。

### 加密的 LeaseSets (LS1)

本节描述了使用固定对称密钥加密 LeaseSet 的旧的、不安全的方法。有关加密 LeaseSet 的 LS2 版本，请参见下文。

在*加密的* LeaseSet 中，所有 Lease 都使用单独的密钥进行加密。只有拥有密钥的用户才能解码这些 lease，从而联系到目标地址。没有标志或其他直接指示表明 LeaseSet 是加密的。加密的 LeaseSet 并未广泛使用，研究是否可以改进加密 LeaseSet 的用户界面和实现是未来工作的一个主题。

### 加密的 LeaseSets (LS2)

从 0.9.38 版本开始，floodfill 支持一种新的 EncryptedLeaseSet 结构。Destination 被隐藏，floodfill 只能看到一个盲化公钥和过期时间。只有拥有完整 Destination 的用户才能解密该结构。该结构存储在基于盲化公钥哈希值的 DHT 位置，而不是基于 Destination 哈希值的位置。详情请参见提案 123。

### LeaseSet 过期

对于常规的 LeaseSet，过期时间是其租约中最晚过期时间。对于新的 LeaseSet2 数据结构，过期时间在头部中指定。对于 LeaseSet2，过期时间应该与其租约的最晚过期时间匹配。对于 EncryptedLeaseSet 和 MetaLeaseSet，过期时间可能会有所不同，最大过期时间可能会被强制执行，具体待确定。

### LeaseSet 持久化存储

不需要对 LeaseSet 数据进行持久存储，因为它们很快就会过期。但是，对于具有较长过期时间的 EncryptedLeaseSet 和 MetaLeaseSet 数据，建议进行持久存储。

### 加密密钥选择 (LS2)

LeaseSet2 可能包含多个加密密钥。这些密钥按服务器偏好顺序排列，最优选的在前。默认客户端行为是选择第一个支持的加密类型的密钥。客户端可以基于加密支持、相对性能和其他因素使用其他选择算法。

---

## 引导启动

netDb 是去中心化的，但是你确实需要至少一个对等节点的引用，以便集成过程将你连接进来。这是通过使用活跃对等节点的 RouterInfo 来"重新播种"你的 router 来实现的 - 具体来说，就是检索他们的 `routerInfo-$hash.dat` 文件并将其存储在你的 `netDb/` 目录中。任何人都可以为你提供这些文件 - 你甚至可以通过公开自己的 netDb 目录来向他人提供这些文件。为了简化这个过程，志愿者们在常规（非 I2P）网络上发布他们的 netDb 目录（或其子集），这些目录的 URL 被硬编码在 I2P 中。当 router 首次启动时，它会自动从这些 URL 中随机选择一个进行获取。

---

## Floodfill

floodfill netDb 是一个简单的分布式存储机制。存储算法很简单：将数据发送给已宣布自己为 floodfill router 的最近节点。当 floodfill netDb 中的节点从不在 floodfill netDb 中的节点接收到 netDb 存储请求时，它们会将其发送给 floodfill netDb 节点的一个子集。被选择的节点是根据 [XOR 度量标准](#kademlia-closeness-metric) 距离特定密钥最近的那些节点。

确定谁是 floodfill netDb 的一部分是很简单的 - 这在每个 router 发布的 routerInfo 中作为一项能力被暴露出来。

Floodfill 没有中央权威机构，也不形成"共识" - 它们只实现一个简单的 DHT 覆盖网络。

### Floodfill Router 选择加入

与 Tor 不同的是，Tor 的目录服务器是硬编码的、受信任的，并且由已知实体运营，而 I2P floodfill 对等节点集合的成员无需被信任，并且会随时间变化。

为了提高netDb的可靠性，并最大程度减少netDb流量对router的影响，floodfill功能只在配置了高带宽限制的router上自动启用。具有高带宽限制的router（必须手动配置，因为默认值要低得多）被认为是运行在低延迟连接上，并且更可能24/7可用。目前floodfill router的最低共享带宽为128 KBytes/sec。

此外，router必须通过几个额外的健康测试（出站消息队列时间、作业延迟等），然后才能自动启用floodfill操作。

根据当前的自动选择加入规则，网络中大约6%的router是floodfill router。

虽然一些节点是手动配置为 floodfill 的，但其他节点只是高带宽 router，当 floodfill 节点数量低于阈值时会自动志愿承担此角色。这可以防止因攻击导致大部分或全部 floodfill 丢失而对网络造成长期损害。反过来，当存在过多 floodfill 时，这些节点也会取消自己的 floodfill 状态。

### Floodfill Router 角色

floodfill router 除了具备非 floodfill router 的所有服务外，其额外的服务仅限于接受 netDb 存储和响应 netDb 查询。由于它们通常具有高带宽，因此更有可能参与大量的 tunnel（即为其他人充当"中继"），但这与它们的分布式数据库服务没有直接关系。

---

## Kademlia 接近度度量

netDb使用简单的Kademlia风格XOR度量来确定接近度。要创建Kademlia密钥，需要计算RouterIdentity或Destination的SHA256哈希值。一个例外是加密LeaseSet（LS2），从0.9.38版本开始。DHT密钥使用类型字节（3）后跟盲化公钥的SHA256，然后按常规方式轮换。

对此算法进行了修改，以增加[Sybil攻击](#sybil-attack-partial-keyspace)的成本。不再使用被查找或存储的密钥的SHA256哈希，而是对32字节的二进制搜索密钥附加上以8字节ASCII字符串yyyyMMdd表示的UTC日期进行SHA256哈希，即SHA256(key + yyyyMMdd)。这被称为"routing key"（路由密钥），它在每天UTC午夜时分都会发生变化。只有搜索密钥以这种方式修改，floodfill router哈希不会修改。DHT的这种日常转换有时被称为"keyspace rotation"（密钥空间轮换），尽管严格来说它并不是真正的轮换。

路由密钥从不在任何I2NP消息中通过网络传输，它们仅在本地用于确定距离。

---

## 网络数据库分段 - 子数据库

传统的 Kademlia 风格 DHT 并不关心保护存储在 DHT 中任何特定节点上信息的不可关联性。例如，一条信息可能被存储到 DHT 中的一个节点，然后无条件地从该节点请求回来。在 I2P 中使用 netDb 时，情况并非如此，存储在 DHT 中的信息只能在某些已知的"安全"情况下才能共享。这是为了防止一类攻击，恶意行为者可能试图通过向客户端 tunnel 发送存储请求，然后直接从可疑的客户端 tunnel "主机"请求信息回来，从而将客户端 tunnel 与 router 关联起来。

### 分段结构

I2P router 可以实现针对此类攻击的有效防御，但需要满足一些条件。网络数据库实现应该能够跟踪数据库条目是通过客户端隧道接收的还是直接接收的。如果是通过客户端隧道接收的，那么它还应该跟踪该条目是通过哪个客户端隧道接收的，使用客户端的本地目标地址。如果条目是通过多个客户端隧道接收的，那么 netDb 应该跟踪观察到该条目的所有目标地址。它还应该跟踪条目是作为查找请求的回复接收的，还是作为存储操作接收的。

在Java和C++实现中，这是通过使用单个"主"netDb来首先进行直接查找和floodfill操作来实现的。这个主netDb存在于router上下文中。然后，每个客户端都被分配自己版本的netDb，用于捕获发送到客户端tunnel的数据库条目并响应通过客户端tunnel发送的查找请求。我们称这些为"客户端网络数据库"或"子数据库"，它们存在于客户端上下文中。由客户端操作的netDb仅在客户端的生命周期内存在，并且仅包含与客户端tunnel通信的条目。这使得通过客户端tunnel发送的条目不可能与直接发送到router的条目重叠。

此外，每个 netDb 需要能够记住数据库条目是因为被发送到我们的某个目标而收到的，还是作为查找的一部分由我们请求而收到的。如果数据库条目是作为存储收到的，即某个其他 router 发送给我们的，那么当另一个 router 查找该键时，netDb 应该响应对该条目的请求。但是，如果它是作为查询的回复收到的，那么只有当该条目已经存储到相同目标时，netDb 才应该回复对该条目的查询。客户端永远不应该使用主 netDb 中的条目来回答查询，只能使用其自己的客户端网络数据库。

这些策略应该结合使用，以便同时应用两种方法。结合使用时，它们会对 netDb 进行"分段"并保护其免受攻击。

---

## 存储、验证和查找机制

### RouterInfo 存储到对等节点

包含本地 RouterInfo 的 [I2NP](/docs/specs/i2np/) DatabaseStoreMessages 作为 [NTCP](/docs/specs/ntcp2/) 或 [SSU](/docs/specs/ssu2/) 传输连接初始化的一部分与对等节点进行交换。

### 向对等节点存储 LeaseSet

包含本地 LeaseSet 的 [I2NP](/docs/specs/i2np/) DatabaseStoreMessages 会通过将其与来自相关 Destination 的正常流量一起打包在 garlic 消息中，定期与对等节点交换。这允许初始响应和后续响应被发送到适当的 Lease，而无需进行任何 LeaseSet 查找，也不需要通信的 Destinations 发布 LeaseSets。

### Floodfill 选择

DatabaseStoreMessage 应该发送到与正在存储的 RouterInfo 或 LeaseSet 的当前路由密钥最接近的 floodfill。目前，最接近的 floodfill 是通过在本地数据库中搜索找到的。即使该 floodfill 实际上不是最接近的，它也会通过将消息发送到多个其他 floodfill 来将其泛洪到"更接近"的位置。这提供了高度的容错能力。

在传统的 Kademlia 中，节点在将项目插入 DHT 到最接近的目标之前会执行"查找最接近"搜索。由于验证操作往往会发现更接近的 floodfill（如果存在的话），router 将快速改进其对定期发布的 RouterInfo 和 LeaseSet 的 DHT "邻域"知识。虽然 I2NP 没有定义"查找最接近"消息，但如果有必要，router 可以简单地对最低有效位翻转的密钥（即 key ^ 0x01）进行迭代搜索，直到在 DatabaseSearchReplyMessages 中没有收到更接近的对等节点。这确保即使更远的对等节点拥有 netDb 项目，也能找到真正最接近的对等节点。

### RouterInfo 存储到 Floodfills

router通过直接连接到floodfill router并发送一个带有非零Reply Token的[I2NP](/docs/specs/i2np/) DatabaseStoreMessage来发布自己的RouterInfo。该消息不进行端到端garlic encryption，因为这是直接连接，所以没有中间的router（而且也没有必要隐藏这些数据）。floodfill router会回复一个[I2NP](/docs/specs/i2np/) DeliveryStatusMessage，其Message ID设置为Reply Token的值。

在某些情况下，router也可能通过探索性tunnel发送RouterInfo DatabaseStoreMessage；例如，由于连接限制、连接不兼容性，或希望向floodfill隐藏实际IP地址。在过载时或基于其他标准，floodfill可能不接受此类存储；是否明确声明RouterInfo的非直接存储为非法行为，这是一个需要进一步研究的话题。

### LeaseSet 存储到 Floodfills

LeaseSet的存储比RouterInfo敏感得多，因为router必须确保LeaseSet不能与该router产生关联。

router通过为该目的地通过出站客户端tunnel发送带有非零Reply Token的[I2NP](/docs/specs/i2np/) DatabaseStoreMessage来发布本地leaseSet。该消息使用目的地的会话密钥管理器进行端到端garlic加密，以对tunnel的出站端点隐藏消息。floodfill router回复一个[I2NP](/docs/specs/i2np/) DeliveryStatusMessage，其中消息ID设置为Reply Token的值。此消息被发送回客户端的一个入站tunnel。

### 泛洪

像任何 router 一样，floodfill 使用各种标准来验证 LeaseSet 或 RouterInfo，然后才在本地存储。这些标准可能是自适应的，并且依赖于当前条件，包括当前负载、netDb 大小和其他因素。所有验证都必须在 flooding 之前完成。

当一个 floodfill router 接收到包含有效 RouterInfo 或 LeaseSet 的 DatabaseStoreMessage，且该信息比之前存储在本地 NetDb 中的更新时，它会"泛洪"该信息。为了泛洪一个 NetDb 条目，它会查找几个（目前是3个）最接近该 NetDb 条目路由密钥的 floodfill router。（路由密钥是 RouterIdentity 或 Destination 的 SHA256 哈希值加上日期（yyyyMMdd）后缀。）通过泛洪到最接近密钥的节点，而不是最接近自身的节点，floodfill 确保存储能到达正确的位置，即使存储路由器对该路由密钥的 DHT "邻域"没有良好的了解。

然后 floodfill 直接连接到这些对等节点中的每一个，并发送一个 Reply Token 为零的 [I2NP](/docs/specs/i2np/) DatabaseStoreMessage。该消息不进行端到端 garlic encryption，因为这是直接连接，所以没有中间 router（而且也没有必要隐藏这些数据）。其他 router 不会回复或重新泛洪，因为 Reply Token 是零。

Floodfill 节点不得通过隧道进行泛洪；DatabaseStoreMessage 必须通过直接连接发送。

Floodfill 节点绝不能洪泛已过期的 LeaseSet 或发布时间超过一小时的 RouterInfo。

### RouterInfo 和 LeaseSet 查找

[I2NP](/docs/specs/i2np/) DatabaseLookupMessage 用于从 floodfill router 请求 netDb 条目。查找请求通过 router 的一个出站探索性 tunnel 发送。回复被指定通过 router 的一个入站探索性 tunnel 返回。

查找请求通常会并行发送给距离请求密钥最近的两个"良好"（连接不会失败）floodfill router。

如果floodfill router在本地找到了密钥，它会用一个[I2NP](/docs/specs/i2np/) DatabaseStoreMessage来响应。如果floodfill router在本地没有找到密钥，它会用一个[I2NP](/docs/specs/i2np/) DatabaseSearchReplyMessage来响应，该消息包含一个接近该密钥的其他floodfill router列表。

从 0.9.5 版本开始，LeaseSet 查找采用端到端的 garlic encryption。RouterInfo 查找未加密，因此容易被客户端 tunnel 的出站端点 (OBEP) 窥探。这是由于 ElGamal 加密的开销较大。RouterInfo 查找加密可能会在未来版本中启用。

从0.9.7版本开始，对LeaseSet查找的回复（DatabaseStoreMessage或DatabaseSearchReplyMessage）将通过在查找中包含会话密钥和标签来进行加密。这样可以向回复tunnel的入站网关（IBGW）隐藏回复内容。如果我们启用查找加密，对RouterInfo查找的响应也将被加密。

(参考：[Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf) 第2.2-2.3节，了解下文斜体术语的定义)

由于网络规模相对较小和flooding冗余，查找通常是O(1)而不是O(log n)。router很可能知道一个足够接近key的floodfill router，可以在第一次尝试时就得到答案。在0.8.9版本之前，router使用查找冗余度为二（即，向不同的对等节点并行执行两次查找），并且没有实现*递归*或*迭代*路由查找。查询是*同时通过多条路由发送*来*减少查询失败的可能性*。

从 0.8.9 版本开始，*迭代查找* 已实现且无查找冗余。这是一种更高效、更可靠的查找方式，在并非所有 floodfill 对等节点都已知的情况下工作效果更好，并且消除了网络增长的严重限制。随着网络增长，每个 router 只知道 floodfill 对等节点的一小部分，查找将变为 O(log n)。即使对等节点没有返回更接近密钥的引用，查找也会继续使用下一个最近的对等节点，以增加健壮性，并防止恶意的 floodfill 将密钥空间的一部分变成黑洞。查找将持续进行，直到达到总查找超时时间，或查询的对等节点数量达到最大值。

*节点ID*是*可验证的*，因为我们直接使用router哈希值作为节点ID和Kademlia密钥。通常会忽略不接近搜索密钥的错误响应。考虑到当前网络规模，router对*目标ID空间邻域有详细了解*。

### RouterInfo 存储验证

注意：从 0.9.7.1 版本开始，RouterInfo 验证已被禁用，以防止论文 [Practical Attacks Against the I2P Network](http://wwwcip.informatik.uni-erlangen.de/~spjsschl/i2p.pdf) 中描述的攻击。目前尚不清楚是否可以重新设计验证机制来安全地执行此操作。

为了验证存储是否成功，router 只需等待大约 10 秒钟，然后向另一个靠近该密钥的 floodfill router（但不是发送存储请求的那个）发送查找请求。查找请求通过 router 的出站探索 tunnel 之一发送。查找请求使用端到端 garlic encryption 进行加密，以防止出站端点(OBEP)进行窥探。

### LeaseSet 存储验证

为了验证存储是否成功，router 只需等待大约 10 秒钟，然后向另一个接近该密钥的 floodfill router（但不是发送存储请求的那个）发送查找请求。查找请求通过正在验证的 LeaseSet 目标的出站客户端 tunnel 之一发出。为了防止出站 tunnel 的 OBEP 进行窥探，查找请求使用端到端 garlic encryption 进行加密。回复被指定通过客户端的入站 tunnel 之一返回。

从 0.9.7 版本开始，RouterInfo 和 LeaseSet 查找的回复（DatabaseStoreMessage 或 DatabaseSearchReplyMessage）都将被加密，以向回复 tunnel 的入站网关（IBGW）隐藏回复内容。

### 探索

*Exploration* 是netDb查找的一种特殊形式，router试图了解新的router。它通过向floodfill router发送[I2NP](/docs/specs/i2np/) DatabaseLookup消息来实现这一点，查找一个随机密钥。由于这种查找会失败，floodfill通常会回复一个[I2NP](/docs/specs/i2np/) DatabaseSearchReplyMessage，其中包含接近该密钥的floodfill router的哈希值。这并没有帮助，因为请求的router可能已经知道这些floodfill，而且将所有floodfill router添加到DatabaseLookup消息的"不包含"字段中是不现实的。对于exploration查询，请求的router在DatabaseLookup消息中设置一个特殊标志。然后floodfill将只回复接近所请求密钥的非floodfill router。

### 查找响应的注意事项

查找请求的响应要么是数据库存储消息（成功时），要么是数据库搜索回复消息（失败时）。DSRM 包含一个"from" router 哈希字段来指示回复的来源；DSM 则没有。DSRM 的"from"字段未经身份验证，可能被伪造或无效。没有其他响应标签。因此，当并行发出多个请求时，很难监控各个 floodfill router 的性能。

---

## 多宿主

目标节点可以通过使用相同的私钥和公钥（传统上存储在eepPriv.dat文件中）同时托管在多个router上。由于两个实例都会定期将其签名的leaseSet发布到floodfill节点，当节点请求数据库查找时，将返回最近发布的leaseSet。由于leaseSet的生存期最多为10分钟，如果某个特定实例发生故障，停机时间最多为10分钟，通常会远少于此时间。多宿主功能已经过验证，并且正在网络中的多个服务使用。

从 0.9.38 版本开始，floodfill 支持新的 Meta LeaseSet 结构。该结构在 DHT 中提供树状结构，用于引用其他 LeaseSet。使用 Meta LeaseSet，站点可以实现大型多宿主服务，其中使用多个不同的 Destination 来提供通用服务。Meta LeaseSet 中的条目是 Destination 或其他 Meta LeaseSet，并且可能具有较长的过期时间，最长可达 18.2 小时。使用此功能，应该可以运行数百或数千个托管通用服务的 Destination。详细信息请参见提案 123。

---

## 威胁分析

在[威胁模型页面](/docs/overview/threat-model/#floodfill)上也有讨论。

恶意用户可能会尝试通过创建一个或多个 floodfill router 并精心设计它们来提供错误、缓慢或无响应的服务，从而损害网络。下面讨论了一些场景。

### 通过增长进行的一般缓解措施

网络中目前大约有1700个floodfill router。随着网络规模和floodfill router数量的增加，以下大部分攻击将变得更加困难，或者影响会减少。

### 通过冗余实现通用缓解

通过泛洪，所有 netDb 条目都存储在距离密钥最近的 3 个 floodfill router 上。

### 伪造

所有 netDb 条目都由其创建者签名，因此任何 router 都无法伪造 RouterInfo 或 leaseSet。

### 缓慢或无响应

每个 router 为每个 floodfill router 在[对等体配置文件](/docs/overview/peer-selection/)中维护一组扩展的统计信息，涵盖该对等体的各种质量指标。该集合包括：

- 平均响应时间
- 返回所请求数据的查询百分比
- 成功验证的存储百分比
- 最后一次成功存储
- 最后一次成功查找
- 最后一次响应

每当 router 需要确定哪个 floodfill router 最接近某个密钥时，它会使用这些指标来确定哪些 floodfill router 是"良好的"。用于确定"良好性"的方法和阈值相对较新，仍需要进一步分析和改进。虽然完全无响应的 router 会被快速识别并避免，但那些只是偶尔恶意的 router 可能更难处理。

### 女巫攻击（全密钥空间）

攻击者可能通过创建大量分布在整个密钥空间中的 floodfill router 来发起 [Sybil 攻击](https://www.freehaven.net/anonbib/cache/sybil.pdf)。

（在一个相关的例子中，一位研究员最近创建了[大量的 Tor 中继](http://blog.torproject.org/blog/june-2010-progress-report)。）如果成功的话，这可能会对整个网络构成有效的拒绝服务攻击。

如果 floodfill 节点的不当行为还不足以通过上述对等节点档案指标被标记为"坏"节点，这是一个很难处理的情况。Tor 在中继节点情况下的响应可以更加灵活，因为可疑的中继节点可以手动从共识中移除。下面列出了 I2P 网络的一些可能响应，但没有一个是完全令人满意的：

- 编译一份恶意 router 哈希或 IP 列表，并通过各种方式（控制台新闻、网站、论坛等）公布该列表；用户必须手动下载列表并将其添加到本地"黑名单"中。
- 要求网络中的每个人手动启用 floodfill（用更多 Sybil 攻击对抗 Sybil 攻击）
- 发布包含硬编码"恶意"列表的新软件版本
- 发布改进对等体配置文件指标和阈值的新软件版本，尝试自动识别"恶意"对等体。
- 添加软件，如果在单个 IP 块中有太多 floodfill 则取消其资格
- 实现由单个个人或团体控制的基于订阅的自动黑名单。这本质上会实现 Tor "共识"模型的一部分。不幸的是，这也会给单个个人或团体阻止任何特定 router 或 IP 参与网络的权力，甚至完全关闭或摧毁整个网络。

随着网络规模的增长，这种攻击变得更加困难。

### Sybil 攻击（部分密钥空间）

攻击者可能通过创建少量（8-15个）在密钥空间中紧密聚集的 floodfill router 来发起[女巫攻击](https://www.freehaven.net/anonbib/cache/sybil.pdf)，并广泛分发这些 router 的 RouterInfo。然后，该密钥空间中某个密钥的所有查找和存储都会被定向到攻击者的某个 router 上。如果成功，这可能对特定的 I2P 站点构成有效的拒绝服务攻击。

由于密钥空间是通过密钥的加密（SHA256）哈希进行索引的，攻击者必须使用暴力破解方法反复生成 router 哈希，直到获得足够多与密钥足够接近的哈希值。完成此操作所需的计算能力（取决于网络规模）尚不清楚。

作为对这种攻击的部分防御措施，用于确定 Kademlia "接近度"的算法会随时间变化。我们不使用密钥的哈希值（即 H(k)）来确定接近度，而是使用密钥附加当前日期字符串的哈希值，即 H(k + YYYYMMDD)。一个称为"routing key generator"的函数执行此操作，将原始密钥转换为"routing key"。换句话说，整个 netDb 密钥空间每天在 UTC 午夜时都会"旋转"。任何部分密钥空间攻击都必须每天重新生成，因为在旋转后，攻击 router 将不再接近目标密钥，也不再彼此接近。

随着网络规模的增长，这种攻击变得更加困难。然而，最近的研究表明，密钥空间轮换并不是特别有效。攻击者可以提前预计算大量的 router 哈希值，并且只需要少数几个 router 就足以在轮换后半小时内"遮蔽"密钥空间的一部分。

每日密钥空间轮换的一个后果是，分布式网络数据库可能在轮换后的几分钟内变得不可靠——查找会失败，因为新的"最近"router尚未接收到存储。问题的严重程度以及缓解方法（例如在午夜进行netDb"交接"）是进一步研究的主题。

### Bootstrap 攻击

攻击者可能通过控制reseed网站，或欺骗开发者将其reseed网站添加到router的硬编码列表中，来尝试将新router启动到一个被隔离或被攻击者控制的网络中。

有几种防御措施是可能的，其中大部分已经在计划中：

- 禁止从 HTTPS 降级到 HTTP 进行重新播种。中间人攻击者可以简单地阻止 HTTPS，然后响应 HTTP。
- 在安装程序中捆绑重新播种数据

已实施的防护措施：

- 修改 reseed 任务，从多个 reseed 站点获取 RouterInfo 子集，而不是仅使用单个站点
- 创建一个网络外的 reseed 监控服务，定期轮询 reseed 网站并验证数据是否过时或与网络的其他视图不一致
- 从 0.9.14 版本开始，reseed 数据被打包到签名的 zip 文件中，下载时会验证签名。详情请参阅 [su3 规范](/docs/specs/updates/#su3)。

### 查询捕获

另见 [查找](#routerinfo-and-leaseset-lookup)（参考：[Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf) 第2.2-2.3节，了解下面斜体术语的含义）

类似于引导攻击，攻击者使用 floodfill router 可以尝试通过返回其控制的 router 引用来"引导"对等节点到由其控制的 router 子集。

这种方法通过探索来实现是不太可能成功的，因为探索是一个低频任务。Router 主要通过正常的隧道构建活动来获取大部分对等节点引用。探索结果通常限于少数几个 router 哈希值，并且每次探索查询都是定向到随机的 floodfill router。

从 0.8.9 版本开始，实现了*迭代查找*。对于在 [I2NP](/docs/specs/i2np/) DatabaseSearchReplyMessage 响应中返回的 floodfill router 引用，如果这些引用更接近（或是次接近）查找键，则会跟随这些引用。请求的 router 不会信任这些引用确实更接近键（即它们是*可验证正确的*）。查找也不会在找不到更接近的键时停止，而是继续查询次接近的节点，直到超时或达到最大查询次数。这可以防止恶意的 floodfill 将部分键空间变成黑洞。此外，每日键空间轮换要求攻击者在所需的键空间区域内重新生成 router 信息。这种设计确保了 [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf) 中描述的查询捕获攻击变得更加困难。

### 基于DHT的中继选择

（参考：[Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf) 第3节）

这与 floodfill 关系不大，但请参阅[节点选择页面](/docs/overview/peer-selection/)了解隧道节点选择漏洞的讨论。

### 信息泄露

（参考：[In Search of an Anonymous and Secure Lookup](https://www.freehaven.net/anonbib/cache/ccs10-lookup.pdf) 第 3 节）

这篇论文解决了 Torsk 和 NISAN 使用的"Finger Table" DHT 查找中的弱点。乍一看，这些问题似乎不适用于 I2P。首先，Torsk 和 NISAN 对 DHT 的使用与 I2P 中的使用有显著差异。其次，I2P 的 netDb 查找与[节点选择](/docs/overview/peer-selection/)和[tunnel 构建](/docs/overview/tunnel-routing/)过程只有松散的关联；只有先前已知的节点才会用于 tunnel。此外，节点选择与任何 DHT 键接近性的概念都无关。

当I2P网络变得更大时，其中一些实际上可能会变得更有趣。目前，每个router都知道网络的很大一部分，因此在网络数据库中查找特定的Router Info并不能强烈表明将来有意在tunnel中使用该router。也许当网络规模扩大100倍时，查找可能会更具相关性。当然，更大的网络使得Sybil攻击变得更加困难。

然而，I2P 中 DHT 信息泄露的总体问题需要进一步调查。floodfill router 能够观察查询并收集信息。当然，在 *f* = 0.2（20% 恶意节点，如论文中所述）的水平上，我们预期我们描述的许多 Sybil 威胁（[这里](/docs/overview/threat-model/#sybil)、[这里](#sybil-attack-full-keyspace) 和 [这里](#sybil-attack-partial-keyspace)）会因多种原因变得有问题。

---

## 历史

[已移至 netDb 讨论页面](/docs/legacy/netdb/)。

---

## 未来工作

额外 netDb 查找和响应的端到端加密。

更好的查找响应跟踪方法。
