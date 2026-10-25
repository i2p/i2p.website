---
title: "Tunnel 实现"
description: "I2P tunnel 操作、构建和消息处理规范"
slug: "tunnel-implementation"
aliases:
  - "/zh/docs/specs/implementation"
  - "/zh/docs/specs/implementation/"
lastUpdated: "2019-07"
accurateFor: "0.9.41"
---

本页面记录了当前的 tunnel 实现。

## Tunnel 概述 {#tunnel.overview}

在 I2P 中，消息通过由对等节点组成的虚拟 tunnel 单向传递，利用任何可用的方式将消息传递给下一跳。消息到达 tunnel 的*网关*，被打包和/或分片成固定大小的 tunnel 消息，然后转发给 tunnel 中的下一跳，下一跳处理并验证消息的有效性，再发送给下一跳，如此往复，直到到达 tunnel 端点。该*端点*接收网关打包的消息，并按指示转发 - 要么发送给另一个 router，要么发送给另一个 router 上的另一个 tunnel，要么在本地处理。

Tunnel 的工作原理都相同，但可以分为两个不同的组别 - inbound tunnel 和 outbound tunnel。Inbound tunnel 有一个不可信的网关，将消息向下传递给 tunnel 创建者，创建者作为 tunnel 端点。对于 outbound tunnel，tunnel 创建者作为网关，将消息传出到远程端点。

tunnel的创建者会精确选择哪些节点将参与该tunnel，并为每个节点提供必要的配置数据。tunnel可以有任意数量的跳数。我们的目标是让参与者或第三方都难以确定tunnel的长度，甚至让串通的参与者也无法确定他们是否属于同一个tunnel（除非串通的节点在tunnel中彼此相邻）。

在实际应用中，一系列不同用途的tunnel池被使用——每个本地客户端目标都有自己的一组入站tunnel和出站tunnel，这些tunnel经过配置以满足其匿名性和性能需求。此外，router本身维护一系列池来参与网络数据库和管理tunnel本身。

I2P 本质上是一个分组交换网络，即使使用这些tunnel，也能够利用并行运行的多个tunnel，从而提高弹性和负载均衡。在核心 I2P 层之外，还有一个可选的端到端流媒体库供客户端应用程序使用，提供类似 TCP 的操作，包括消息重排序、重传、拥塞控制等。

I2P tunnel 术语概述在 [tunnel 概述页面](/docs/overview/tunnel-routing) 上。

## Tunnel 操作（消息处理） {#tunnel.operation}

### 概述

tunnel 建立后，[I2NP messages](/docs/specs/i2np) 会被处理并通过它传递。tunnel 操作有四个不同的过程，由 tunnel 中的各个节点承担。

1. 首先，tunnel 网关累积一定数量的
   I2NP 消息并将它们预处理成 tunnel 消息以便
   传递。
2. 接下来，该网关加密这些预处理的数据，然后
   将其转发到第一跳。
3. 该节点以及后续的 tunnel
   参与者会解开一层加密，验证它不是
   重复消息，然后将其转发到下一个节点。
4. 最终，tunnel 消息到达端点，在那里由网关原本打包的 I2NP 消息
   被重新组装并按要求转发。

中间 tunnel 参与者不知道他们是在入站还是出站 tunnel 中；他们总是为下一跳进行"加密"。因此，我们利用对称 AES 加密在出站 tunnel 网关进行"解密"，使明文在出站端点被显示出来。

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Role</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Preprocessing</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Encryption Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Postprocessing</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outbound Gateway (Creator)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fragment, Batch, and Pad</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Iteratively encrypt (using decryption operations)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Participant</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Decrypt (using an encryption operation)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outbound Endpoint</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Decrypt (using an encryption operation) to reveal plaintext tunnel message</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reassemble Fragments, Forward as instructed to Inbound Gateway or Router</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;" colspan="4"></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Inbound Gateway</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fragment, Batch, and Pad</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Participant</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Inbound Endpoint (Creator)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Iteratively decrypt to reveal plaintext tunnel message</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reassemble Fragments, Receive data</td>
    </tr>
  </tbody>
</table>
### 网关处理 {#tunnel.gateway}

#### 消息预处理 {#tunnel.preprocessing}

tunnel gateway的功能是将[I2NP messages](/docs/specs/i2np)分片并打包成固定大小的[tunnel messages](/docs/specs/tunnel-message)，然后加密这些tunnel messages。Tunnel messages包含以下内容：

- 一个 4 字节的 Tunnel ID
- 一个 16 字节的 IV（初始化向量）
- 一个校验和
- 必要时的填充
- 一个或多个 { 传递指令，I2NP 消息片段 } 对

Tunnel ID 是在每一跳使用的 4 字节数字 - 参与者知道应该监听哪个 tunnel ID 的消息，以及应该使用哪个 tunnel ID 转发到下一跳，每一跳都会选择它们接收消息的 tunnel ID。Tunnel 本身是短暂的（10 分钟）。即使后续的 tunnel 使用相同的对等节点序列构建，每一跳的 tunnel ID 也会改变。

为了防止对手通过调整消息大小来标记路径上的消息，所有 tunnel 消息都是固定的 1024 字节大小。为了容纳更大的 I2NP 消息以及更有效地支持较小的消息，gateway 会将较大的 I2NP 消息分割成包含在每个 tunnel 消息中的片段。endpoint 会在短时间内尝试从这些片段重建 I2NP 消息，但会在必要时丢弃它们。

详情请参阅 [tunnel 消息规范](/docs/specs/tunnel-message)。

### 网关加密

在将消息预处理为填充载荷后，gateway 构建一个随机的 16 字节 IV 值，根据需要对其和 tunnel 消息进行迭代加密，然后将元组 {tunnelID, IV, 加密的 tunnel 消息} 转发给下一跳。

gateway 处的加密方式取决于 tunnel 是入站还是出站。对于入站 tunnel，它们只需选择一个随机 IV，对其进行后处理和更新以生成 gateway 的 IV，然后使用该 IV 和自己的层密钥来加密预处理数据。对于出站 tunnel，它们必须使用 tunnel 中所有跳数的 IV 和层密钥对（未加密的）IV 和预处理数据进行迭代解密。出站 tunnel 加密的结果是，当每个对等节点对其进行加密时，端点将恢复初始的预处理数据。

### 参与者处理 {#tunnel.participant}

当一个节点收到tunnel消息时，它会检查该消息是否来自与之前相同的前一跳（在第一条消息通过tunnel时初始化）。如果前一个节点是不同的router，或者消息已经被处理过，则丢弃该消息。然后参与者使用其IV密钥通过AES256/ECB加密接收到的IV以确定当前IV，使用该IV与参与者的层密钥对数据进行加密，再次使用其IV密钥通过AES256/ECB加密当前IV，然后将元组{nextTunnelId, nextIV, encryptedData}转发到下一跳。这种对IV的双重加密（使用前后都加密）有助于解决某类确认攻击。

重复消息检测通过对消息 IV 使用衰减布隆过滤器来处理。每个 router 维护单个布隆过滤器，包含它参与的所有 tunnel 收到的消息的 IV 与第一个数据块的异或值，经过修改以在 10-20 分钟后丢弃已见条目（此时 tunnel 将过期）。布隆过滤器的大小和使用的参数足以使 router 的网络连接超过饱和，同时误报概率可忽略不计。输入布隆过滤器的唯一值是 IV 与第一个数据块的异或，以防止 tunnel 中非连续的串通节点通过交换 IV 和第一个数据块重新发送消息来标记该消息。

### 端点处理 {#tunnel.endpoint}

在 tunnel 的最后一跳接收并验证 tunnel 消息后，端点如何恢复网关编码的数据取决于 tunnel 是入站还是出站。对于出站 tunnel，端点像其他任何参与者一样使用其层密钥加密消息，暴露预处理的数据。对于入站 tunnel，端点也是 tunnel 创建者，因此他们只需使用每一步的层密钥和 IV 密钥按相反顺序迭代解密 IV 和消息。

此时，tunnel 端点已收到网关发送的预处理数据，然后可以将其解析为包含的 I2NP 消息，并根据其传递指令的要求转发这些消息。

## Tunnel 构建 {#tunnel.building}

在构建tunnel时，创建者必须向每个跳点发送包含必要配置数据的请求，并等待所有跳点都同意后才能启用tunnel。请求经过加密，只有需要了解特定信息（如tunnel层或IV密钥）的对等节点才能获得该数据。此外，只有tunnel创建者才能访问对等节点的回复。在构建tunnel时需要记住三个重要维度：使用什么对等节点（以及在哪里），如何发送请求（以及接收回复），以及如何维护它们。

### 节点选择 {#tunnel.peerselection}

除了两种类型的 tunnel（入站和出站）之外，还有两种用于不同 tunnel 的节点选择方式——探索性和客户端。探索性 tunnel 用于网络数据库维护和 tunnel 维护，而客户端 tunnel 用于端到端的客户端消息传输。

#### 探索性 Tunnel 节点选择 {#tunnel.selection.exploratory}

探索性tunnel是从网络子集中随机选择的对等节点构建的。特定的子集因本地router而异，并取决于它们的tunnel路由需求。通常，探索性tunnel是从随机选择的处于"未失败但活跃"配置文件类别中的对等节点构建的。除了单纯的tunnel路由之外，这些tunnel的次要目的是找到未充分利用的高容量对等节点，以便将它们提升为客户端tunnel使用。

探索性对等体选择在[对等体分析和选择页面](/docs/overview/peer-selection)中有进一步讨论。

#### 客户端 Tunnel 节点选择 {#tunnel.selection.client}

客户端 tunnel 的构建有着更严格的要求集合 - 本地 router 会从其"快速且高容量"配置文件类别中选择对等节点，以确保性能和可靠性能够满足客户端应用程序的需求。然而，除了这种基本选择之外，还有几个重要细节需要遵循，这取决于客户端的匿名性需求。

客户端节点选择在[节点分析和选择页面](/docs/overview/peer-selection)中有进一步讨论。

#### 隧道内的节点排序 {#ordering}

在 tunnel 内对节点进行排序是为了应对[前驱攻击](http://forensics.umass.edu/pubs/wright-tissec.pdf)（[2008年更新](http://forensics.umass.edu/pubs/wright.tissec.2008.pdf)）。

为了阻挠前驱攻击，tunnel 选择会严格按顺序保持所选择的对等节点 - 如果 A、B 和 C 在特定 tunnel 池的一个 tunnel 中，A 之后的跳点始终是 B，B 之后的跳点始终是 C。

排序是通过在启动时为每个tunnel池生成一个随机的32字节密钥来实现的。对等节点不应该能够猜测排序方式，否则攻击者可能会制造两个相距很远的router哈希值，以最大化出现在tunnel两端的机会。对等节点按照（对等节点哈希值与随机密钥连接后）的SHA256哈希值与随机密钥的异或距离进行排序：

```
      p = peer hash
      k = random key
      d = XOR(H(p+k), k)
```
由于每个 tunnel 池使用不同的随机密钥，排序在单个池内是一致的，但在不同池之间则不一致。每次 router 重启时都会生成新的密钥。

### 请求传递 {#tunnel.request}

多跳隧道使用单个构建消息来建立，该消息会被重复解密和转发。用[Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf)的术语来说，这是"非交互式"望远镜式隧道构建。

这种tunnel请求准备、传递和响应方法[设计](/docs/specs/tunnel-creation)用于减少暴露的前置节点数量，减少传输的消息数量，验证正确的连接性，并避免传统望远镜式tunnel创建的消息计数攻击。（这种通过已建立的tunnel部分发送消息来扩展tunnel的方法，在"Hashing it out"论文中被称为"交互式"望远镜式tunnel构建。）

tunnel 请求和响应消息的详细信息，以及它们的加密，[在此处指定](/docs/specs/tunnel-creation)。

节点可能会因为各种原因拒绝tunnel创建请求，不过已知有四种严重程度递增的拒绝类型：概率性拒绝（由于接近router容量，或响应大量请求），瞬时过载，带宽过载，以及关键故障。当收到这些拒绝时，tunnel创建者会解释这四种情况，以帮助调整他们对相关router的配置文件。

有关对等节点分析的更多信息，请参见[对等节点分析和选择页面](/docs/overview/peer-selection)。

### Tunnel 池 {#tunnel.pooling}

为了实现高效运行，router 维护着一系列 tunnel 池，每个池管理着一组用于特定目的的 tunnel，并具有各自的配置。当需要为特定目的使用 tunnel 时，router 会从相应的池中随机选择一个。总的来说，有两个探索性 tunnel 池——一个入站和一个出站——每个都使用 router 的默认配置。此外，每个本地目标都有一对池——一个入站和一个出站 tunnel 池。这些池使用本地目标通过 [I2CP](/docs/specs/i2cp) 连接到 router 时指定的配置，或者如果没有指定则使用 router 的默认配置。

每个池在其配置中都有几个关键设置，定义了要保持活跃的 tunnel 数量、在发生故障时要维护的备用 tunnel 数量、tunnel 应该有多长、这些长度是否应该随机化，以及配置单个 tunnel 时允许的任何其他设置。配置选项在 [I2CP 页面](/docs/specs/i2cp) 中有详细说明。

### Tunnel 长度和默认值 {#length}

[在 tunnel 概览页面](/docs/overview/tunnel-routing#length)。

### 预期构建策略和优先级 {#strategy}

Tunnel构建成本很高，而且tunnel在构建后会在固定时间后过期。然而，当一个池的tunnel用尽时，目标基本上就失效了。此外，tunnel构建成功率可能会因本地和全球网络条件而大幅变化。因此，保持一个预见性的、自适应的构建策略非常重要，以确保在需要之前成功构建新的tunnel，而不会构建过多的tunnel、过早构建，或者消耗过多的CPU或带宽来创建和发送加密的构建消息。

对于每个元组 {exploratory/client, in/out, length, length variance}，router 会维护成功建立 tunnel 所需时间的统计数据。使用这些统计数据，它计算应该在 tunnel 到期前多长时间开始尝试建立替换 tunnel。随着到期时间的临近而没有成功的替换，它会开始并行进行多个构建尝试，然后在必要时增加并行尝试的数量。

为了限制带宽和CPU使用量，router还限制了所有池中未完成构建尝试的最大数量。关键构建（用于探索性tunnel的构建，以及tunnel已耗尽的池的构建）会被优先处理。

## Tunnel 消息限流 {#tunnel.throttling}

尽管I2P内的tunnel与电路交换网络相似，但I2P内的一切都严格基于消息传递——tunnel仅仅是帮助组织消息传递的记账技巧。对消息的可靠性或顺序性不做任何假设，重传由更高层处理（例如I2P的客户端层流媒体库）。这使得I2P能够利用包交换和电路交换网络都可用的限流技术。例如，每个router可以跟踪每个tunnel使用数据量的移动平均值，将其与router参与的所有其他tunnel使用的平均值相结合，并能够根据其容量和利用率接受或拒绝额外的tunnel参与请求。另一方面，每个router可以简单地丢弃超出其容量的消息，利用在普通互联网上使用的研究成果。

在当前的实现中，router 实施加权随机早期丢弃(WRED)策略。对于所有参与的 router（内部参与者、入站网关和出站端点），当接近带宽限制时，router 将开始随机丢弃部分消息。随着流量越来越接近或超过限制，更多的消息会被丢弃。对于内部参与者，所有消息都经过分段和填充，因此大小相同。然而，在入站网关和出站端点，丢弃决策是基于完整的（合并的）消息做出的，并且会考虑消息大小。较大的消息更容易被丢弃。此外，消息在出站端点比在入站网关更容易被丢弃，因为这些消息在传输过程中还没有"走得很远"，因此丢弃这些消息的网络成本更低。

## 未来工作 {#future}

### 混合/批处理 {#tunnel.mixing}

在网关和每个跳点上可以使用哪些策略来延迟、重新排序、重新路由或填充消息？这些操作应该在多大程度上自动完成，有多少应该配置为每个 tunnel 或每个跳点的设置，以及 tunnel 的创建者（进而用户）应该如何控制这些操作？所有这些都是未知的，将在遥远的未来版本中解决。

### 填充

填充策略可以在多个层面使用，解决向不同对手泄露消息大小信息的问题。当前固定的tunnel消息大小为1024字节。然而在此范围内，分片消息本身完全不会被tunnel填充，不过对于端到端消息，它们可能作为garlic wrapping的一部分进行填充。

### WRED

WRED策略对端到端性能以及防止网络拥塞崩溃具有重要影响。应该仔细评估和改进当前的WRED策略。
