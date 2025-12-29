---
title: "网络数据库"
description: "理解 I2P 的分布式网络数据库（netDb） - 一种用于 router 联系信息与目的地（Destination）查找的专用 DHT（分布式哈希表）"
slug: "network-database"
lastUpdated: "2025-03"
accurateFor: "2.10.0"
---

---

## 1. 概述

**netDb** 是一个专用的分布式数据库，仅包含两类数据： - **RouterInfos** – router 的联系信息 - **LeaseSets** – 目的地的联系信息

所有数据都经过密码学签名且可验证。每个条目都包含存活性信息，用于丢弃过时条目并替换陈旧条目，从而防范某些类别的攻击。

分发采用 **floodfill** 机制，其中一部分 routers 负责维护分布式数据库。

---

## 2. RouterInfo（路由器信息）

当 routers 需要联系其他 routers 时，它们会交换包含以下内容的 **RouterInfo** 包：

- **Router 身份** – 加密密钥、签名密钥、证书
- **联系地址** – 如何联系该 router
- **发布时间戳** – 该信息的发布时间
- **任意文本选项** – 能力标志与设置
- **密码学签名** – 证明真实性

### 2.1 能力标志位

各 Router 会通过其 RouterInfo（Router 信息）中的字母代码来通告其能力：

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Flag</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Meaning</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>f</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Floodfill participation</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>R</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reachable</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>U</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Unreachable</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>D</strong>, <strong>E</strong>, <strong>G</strong>, <strong>H</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Various capability indicators</td>
    </tr>
  </tbody>
</table>
### 2.2 带宽分类

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bandwidth</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>K</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Under 12 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>L</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">12–48 KBps (default)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>M</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">48–64 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>N</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64–128 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>O</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128–256 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>P</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">256–2000 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>X</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Over 2000 KBps</td>
    </tr>
  </tbody>
</table>
### 2.3 网络ID取值

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Value</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Current Network (default)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved for Future Networks</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3–15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forks and Test Networks</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">16–254</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">255</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved</td>
    </tr>
  </tbody>
</table>
### 2.4 RouterInfo 统计

Routers 发布可选的健康统计数据，用于网络分析： - 探索性 tunnel 构建成功/拒绝/超时率 - 1 小时平均参与 tunnel 数量

统计数据遵循 `stat_(statname).(statperiod)` 格式，值以分号分隔。

**示例统计：**

```
stat_tunnel.buildExploratoryExpire.60m = 0;0;0;53.14
stat_tunnel.buildExploratoryReject.60m = 0;0;0;15.51
stat_tunnel.buildExploratorySuccess.60m = 0;0;0;31.35
stat_tunnel.participatingTunnels.60m = 289.20
```
Floodfill routers 还可能发布：`netdb.knownLeaseSets` 和 `netdb.knownRouters`

### 2.5 家族选项

自 0.9.24 版本起，routers 可以声明家族成员关系（同一运营者）：

- **family**: 家族名称
- **family.key**: 签名类型代码与 base64 编码的签名公钥拼接而成
- **family.sig**: 对家族名称与 32 字节的 router 哈希的签名

同一家族中的多个 router 不会用于同一个 tunnel。

### 2.6 RouterInfo（路由器信息）过期

- 启动后的第一个小时内不过期
- 当已存储的 RouterInfos（路由信息对象）不超过 25 个时不过期
- 随着本地存储数量增加，过期时间会缩短（少于 120 个 routers 时为 72 小时；300 个 routers 时约为 30 小时）
- SSU 引介者约在 1 小时后过期
- Floodfills 对所有本地 RouterInfos 使用 1 小时的过期时间

---

## 3. LeaseSet（用于描述目的地可达性与入站 tunnel 租约的元数据）

**LeaseSets** 会记录针对特定目的地的 tunnel 入口点，并指定：

- **Tunnel 网关 router 身份**
- **4 字节的 tunnel ID**
- **Tunnel 过期时间**

LeaseSets 包含： - **Destination** – 加密密钥、签名密钥、证书 - **附加加密公钥** – 用于端到端 garlic encryption（大蒜加密） - **附加签名公钥** – 用于吊销（当前未使用） - **密码学签名**

### 3.1 LeaseSet 变体

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Unpublished</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Destinations used only for outgoing connections aren't published to floodfill routers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Revoked</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Published with zero leases, signed by additional signing key (not fully implemented)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>LeaseSet2 (LS2)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">As of 0.9.38, supports new encryption types, multiple encryption types, options, offline signing keys ([Proposal 123](/proposals/123-new-netdb-entries/))</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Meta LeaseSet</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tree-like DHT structure for multihomed services, supporting hundreds/thousands of destinations with long expirations (up to 18.2 hours)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Encrypted LeaseSet (LS1)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">All leases encrypted with separate key; only those with the key can decode and contact the destination</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Encrypted LeaseSet (LS2)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">As of 0.9.38, destination hidden with only blinded public key and expiration visible to floodfill</td>
    </tr>
  </tbody>
</table>
### 3.2 LeaseSet 过期

常规 LeaseSets 会在其最晚的租约到期时过期。LeaseSet2 的到期时间在头部中指定。EncryptedLeaseSet 和 MetaLeaseSet 的到期时间可能不同，并可能会施加最大值限制。

---

## 4. 引导

去中心化的 netDb 需要至少一个对等节点引用才能接入。**Reseeding（重新引导）** 会从志愿者的 netDb 目录中获取 RouterInfo 文件（`routerInfo-$hash.dat`）。首次启动会自动从随机选取的硬编码 URL 获取。

---

## 5. Floodfill 机制

floodfill netDb 采用简单的分布式存储：将数据发送给最接近的 floodfill 节点。当非 floodfill 节点发送存储消息（store）时，floodfill 会将其转发给与该特定键最接近的那部分 floodfill 节点。

Floodfill 的参与情况在 RouterInfo 中以能力标志（`f`）表示。

### 5.1 Floodfill 选择加入要求

不同于 Tor 的硬编码的可信目录服务器，I2P 的 floodfill（在 I2P 中用于分发 netDb 的节点角色）集合是**不受信任的**，并且会随着时间变化。

Floodfill 仅会在满足以下要求的高带宽 router 上自动启用: - 至少 128 KBytes/sec 的共享带宽 (手动配置) - 必须通过额外的健康检查 (出站消息队列时间、作业延迟)

当前的自动选择加入带来约**6% 的网络 floodfill 参与率**。

手动配置的 floodfill 与自动志愿成为 floodfill 的 routers 并存。当 floodfill 数量低于阈值时，高带宽的 routers 会自动志愿成为 floodfill。当 floodfill 数量过多时，它们会停止充当 floodfill。

### 5.2 Floodfill 角色

除了接受 netDb 的存储操作并响应查询之外，floodfills 还执行标准的 router 功能。它们更高的带宽通常意味着更高的 tunnel 参与度，但这与数据库服务并无直接关系。

---

## 6. Kademlia 接近度度量

netDb 使用基于 XOR（异或）的 **Kademlia 风格** 距离度量。RouterIdentity 或 Destination 的 SHA256 哈希用于生成 Kademlia 键（LS2 加密的 LeaseSets 除外；对于这类情况，键为对“类型字节 3 与盲化公钥拼接”的 SHA256）。

### 6.1 键空间轮换

为了提高 Sybil 攻击成本，系统不使用 `SHA256(key)`，而是使用：

```
SHA256(key + yyyyMMdd)
```
其中，日期是一个 8 字节的 ASCII UTC 日期。这会生成 **routing key（路由密钥）**，在每天的 UTC 午夜更换——称为 **keyspace rotation（密钥空间轮换）**。

Routing keys（路由密钥）从不会在 I2NP 消息中传输；它们仅用于本地距离判定。

---

## 7. 网络数据库分段

传统的 Kademlia DHT 无法保证存储信息的不可关联性。I2P 通过实现**分段**来防止将客户端 tunnels 与 routers 关联起来的攻击。

### 7.1 分段策略

router 会跟踪：
- 条目是通过 client tunnel 到达，还是直接到达
- 如果是通过 tunnel，到达的是哪个 client tunnel/目标
- 会跟踪通过多个 tunnel 到达的情况
- 会区分存储与查找的回复

Java 和 C++ 的实现都使用： - 一个 **"Main" netDb**，用于在 router 上下文中进行直接查找/floodfill 操作 - 在客户端上下文中的 **"Client Network Databases"** 或 **"Sub-Databases"**，用于捕获发送到客户端 tunnel 的条目

客户端的 netDbs（网络数据库）仅在客户端的生命周期内存在，只包含客户端 tunnel（隧道）条目。来自客户端 tunnel 的条目不能与直接到达的条目重叠。

每个 netDb 都会记录条目是以存储（可响应查找请求）的形式到达，还是以查找回复（仅在此前已向同一目标存储过时才响应）的形式到达。客户端从不使用主 netDb 中的条目来回答查询，只会使用客户端网络数据库条目。

综合策略会将 netDb **分片**，以抵御客户端与 router 的关联攻击。

---

## 8. 存储、验证与查找

### 8.1 将 RouterInfo（路由器信息）存储到对等节点

在 NTCP（I2P 基于 TCP 的传输协议）或 SSU 传输连接初始化期间用于交换本地 RouterInfo（路由器信息）的 I2NP `DatabaseStoreMessage`。

### 8.2 向对等节点存储 LeaseSet

包含本地 LeaseSet 的 I2NP `DatabaseStoreMessage` 会通过捆绑在 Destination 流量中的、经由 garlic encryption（I2P 特有的“garlic”聚合加密）加密的消息定期交换，从而在无需进行 LeaseSet 查找的情况下即可获得响应。

### 8.3 Floodfill 选择

`DatabaseStoreMessage` 会被发送到最接近当前路由键的 floodfill。通过本地数据库搜索来找到最近的 floodfill。即使实际上并非最近，泛洪也会通过向多个 floodfill 发送，使其“更接近”。

传统 Kademlia 在插入之前使用“find-closest（查找最近）”搜索。尽管 I2NP 缺少此类消息，routers 仍可通过将键的最低有效位取反（`key ^ 0x01`）来进行迭代式搜索，以确保真正发现最近邻节点。

### 8.4 将 RouterInfo（路由信息）存储到 floodfills

router 通过直接连接到一个 floodfill，发送带有非零 Reply Token 的 I2NP `DatabaseStoreMessage` 来发布 RouterInfo（路由信息）。该消息未进行端到端的 garlic encryption（直接连接，无中间节点）。floodfill 使用 Reply Token 作为 Message ID，回复一个 `DeliveryStatusMessage`。

routers 也可能通过探索型 tunnel 发送 RouterInfo（连接数限制、不兼容、隐藏 IP）。floodfill 节点在过载时可能会拒绝此类存储请求。

### 8.5 将 LeaseSet 存储到 Floodfills

LeaseSet（I2P 租约集合）的存储比 RouterInfo（I2P 路由信息记录）更为敏感。Routers（I2P 路由器）必须防止 LeaseSet 与其自身发生关联。

Routers 通过出站客户端 tunnel 发送带非零 Reply Token（回复令牌）的 `DatabaseStoreMessage` 来发布 LeaseSet。该消息使用 Destination's Session Key Manager（Destination 的会话密钥管理器）进行端到端的 garlic encryption，从而对该 tunnel 的出站端点不可见。floodfill 通过入站 tunnel 返回 `DeliveryStatusMessage` 进行回复。

### 8.6 洪泛过程

floodfill（目录填充节点）在本地存储之前，会使用依赖于负载、netdb 大小及其他因素的自适应准则验证 RouterInfo/LeaseSet。

在接收到有效的较新数据后，floodfill 会查找与路由键最近的 3 个 floodfill router，并对其进行"flood"传播。它会通过直接连接发送带零 Reply Token（回复令牌）的 I2NP `DatabaseStoreMessage`。其他 router 不会回复，也不会再次泛洪。

**重要约束：** - Floodfills 不得通过 tunnels 进行泛洪；仅允许直接连接 - Floodfills 从不泛洪已过期的 LeaseSet，或发布超过一小时的 RouterInfo（路由器信息数据结构）

### 8.7 RouterInfo（路由器信息）与 LeaseSet 查找

I2NP `DatabaseLookupMessage` 会向 floodfill routers（负责存储和传播 netdb 的特殊 router）请求 netdb 条目。查询通过出站探索 tunnel 发送；回复会指定入站探索 tunnel 作为返回路径。

查询通常会并行发送到两个距离所请求键最近的“良好”的 floodfill routers。

- **本地匹配**: 接收 I2NP `DatabaseStoreMessage` 响应
- **无本地匹配**: 接收 I2NP `DatabaseSearchReplyMessage`，其中包含接近该键的其他 floodfill router 的引用

自 0.9.5 起，LeaseSet 查找使用端到端 garlic encryption。由于 ElGamal 的开销，RouterInfo（路由信息）查找未加密，因此容易遭受出站端点嗅探。

自 0.9.7 起，查找响应包含会话密钥和标签，从而对入站网关隐藏响应。

### 8.8 迭代查找

0.8.9 之前：两个并行的冗余查找，不使用递归或迭代路由。

自 0.8.9 起：**迭代查找** 采用无冗余实现——更高效、更可靠，且更适合 floodfill 知识不完整的情况。随着网络规模增长且 routers 了解的 floodfills 更少，查找的复杂度趋近于 O(log n)。

即使没有更近的节点引用，迭代查询也会继续，从而防止恶意黑洞行为。当前的最大查询次数和超时设置仍然适用。

### 8.9 验证

**RouterInfo 验证**: 自 0.9.7.1 起已禁用，以防止 "Practical Attacks Against the I2P Network" 论文中描述的攻击。

**LeaseSet 验证**: Routers 等待约 10 秒，然后通过出站客户端 tunnel 向不同的 floodfill 进行查找。端到端的 garlic encryption（大蒜式加密，一种将多条消息封装在一起的 I2P 加密方式）使其对出站端点不可见。响应通过入站 tunnels 返回。

自 0.9.7 起，回复以会话密钥/标签隐藏（session key/tag hiding）的方式加密，从而对入站网关（inbound gateway）不可见。

### 8.10 探索

**探索（Exploration）** 涉及使用随机键进行 netdb 查询，以发现新的 routers。Floodfills 会返回包含与所请求键接近的非 floodfill router 哈希的 `DatabaseSearchReplyMessage`。Exploration 查询会在 `DatabaseLookupMessage` 中设置一个特殊标志位。

---

## 9. 多宿主

使用相同私钥/公钥（传统的 `eepPriv.dat`）的 Destination（目标地址）可以在多个 router 上同时托管。每个实例都会定期发布已签名的 LeaseSet；对查找请求的响应会返回最新发布的 LeaseSet。 在 LeaseSet 的最长有效期为 10 分钟的情况下，中断最多持续约 10 分钟。

自 0.9.38 起，**Meta LeaseSets**（元 LeaseSet，指可聚合多个 Destination 的 LeaseSet 类型）支持使用提供相同服务的独立 Destinations（I2P 目的地标识）的大型多宿主服务。Meta LeaseSet 条目可以是 Destinations 或其他 Meta LeaseSets，且有效期可长达 18.2 小时，从而允许数百/数千个 Destinations 承载相同的服务。

---

## 10. 威胁分析

目前约有 1700 个 floodfill routers 正在运行。随着网络的增长，大多数攻击变得更难实施，或影响更小。

### 10.1 通用缓解措施

- **增长**: 更多的 floodfill routers 会使攻击更难实施或影响更小
- **冗余**: 所有 netdb 条目会通过泛洪存储在距离该密钥最近的 3 个 floodfill routers 上
- **签名**: 所有条目均由创建者签名；无法伪造

### 10.2 缓慢或无响应的 Routers

Routers 为 floodfills 维护扩展的对等节点档案统计信息： - 平均响应时间 - 查询应答百分比 - 存储验证成功百分比 - 上次成功存储 - 上次成功查找 - 上次响应

router 在为选择最近的 floodfill 判定 "goodness"（优良度）时，会使用这些度量指标。完全无响应的 router 会被迅速识别并规避；部分恶意的 router 则带来更大的挑战。

### 10.3 女巫攻击 (完整键空间)

攻击者可能在整个键空间中创建大量 floodfill routers，从而实施一种有效的拒绝服务（DoS）攻击。

If 行为不足以被指定为"bad"，可能的应对包括: - 通过控制台新闻、网站、论坛公布并汇编不良 router 哈希/IP 列表 - 在全网启用 floodfill ("用更多的 Sybil（女巫攻击）对抗 Sybil") - 在新软件版本中硬编码"bad"列表 - 改进 peer profile（对等节点画像）的指标与阈值以便自动识别 - 基于 IP 网段的资格限制，禁止同一 IP 网段内存在多个 floodfill - 基于订阅的自动黑名单（类似 Tor 的共识）

更大的网络会使这变得更难。

### 10.4 Sybil 攻击（部分键空间）

攻击者可能创建 8–15 个在键空间中紧密聚集的 floodfill routers。针对该键空间的所有查找/存储都会被定向到攻击者的 routers，从而能够对特定的 I2P 站点实施 DoS（拒绝服务）攻击。

由于键空间对加密的 SHA256 哈希进行索引，攻击者需要采用暴力穷举，才能生成与目标在键空间中足够接近的 routers。

**防御**：Kademlia（分布式哈希表 DHT 算法）的接近度算法会随时间变化，使用 `SHA256(key + YYYYMMDD)`，并在 UTC 午夜每日变更。这样的**键空间轮换**迫使攻击者每天重新构建其攻击。

> **注意**: 最新研究表明，密钥空间轮换的效果并不显著——攻击者可以预先计算 router 哈希值，只需几个 routers 即可在轮换后半小时内对密钥空间的部分区域实施日蚀。

每日轮换的后果：分布式 netdb 在轮换后的几分钟内会变得不可靠——在新的最近 router 接收到存储条目之前，查询会失败。

### 10.5 引导攻击

攻击者可能接管 reseed 网站（用于新节点初始引导获取网络信息的站点），或诱骗开发者添加带有敌意的 reseed 网站，从而使新的 router 在启动时进入被隔离/多数控制的网络。

**已实施的防御措施：** - 从多个 reseed（重新播种）站点获取 RouterInfo 子集，而不是单一站点 - 网络外部的 reseed 监控定期轮询站点 - 自 0.9.14 起，reseed 数据包为签名的 zip 文件，并对下载的签名进行验证（参见 [su3 specification](/docs/specs/updates)）

### 10.6 查询捕获

Floodfill routers 可能会通过所返回的引用将对等节点"引导"至攻击者控制的 routers。

由于频率较低，通过探索获得的可能性不大；router 获取对等节点引用主要依赖于正常的 tunnel 构建。

自 0.8.9 起，已实现迭代查找。`DatabaseSearchReplyMessage` 中返回的 floodfill 引用如果更接近查找键，则会被继续跟进。发起请求的 router 不会信任这些引用所声称的接近度。即便没有更近的键，查找仍会继续，直到超时或达到查询上限，从而防止恶意黑洞攻击。

### 10.7 信息泄露

I2P 中的 DHT（分布式哈希表）信息泄露需要进一步调查。Floodfill routers 会通过观察查询来收集信息。当恶意节点占比达到 20% 时，先前描述的 Sybil 攻击威胁会因多种原因而变得严重。

---

## 11. 未来工作

- 对额外的 netDb 查询和响应进行端到端加密
- 更好的查询响应跟踪方法
- 针对键空间轮换可靠性问题的缓解方法

---

## 12. 参考文献

- [通用结构规范](/docs/specs/common-structures/) – RouterInfo（路由器信息）和 LeaseSet（租约集合）结构
- [I2NP（I2P 网络协议）规范](/docs/specs/i2np/) – 数据库消息类型
- [提案 123：新的 netDb（网络数据库）条目](/proposals/123-new-netdb-entries) – LeaseSet2（第二代 LeaseSet）规范
- [历史 netDb 讨论](/docs/netdb/) – 开发历史和已归档的讨论
