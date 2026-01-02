---
title: "OBEP传输到1-of-N或N-of-N隧道"
number: "125"
author: "zzz, str4d"
created: "2016-03-10"
lastupdated: "2017-04-07"
status: "开放"
thread: "http://zzz.i2p/topics/2099"
toc: true
---

## 概述

本提案涵盖了改善网络性能的两个改进：

- 通过向OBEP提供一个替代列表而不是单一选项，将IBGW选择委托给OBEP。

- 启用OBEP的多播数据包路由。

## 动机

在直接连接的情况下，该想法是通过赋予OBEP连接IBGWs的灵活性来减少连接拥塞。能够指定多个隧道还使我们能够在OBEP实现多播（通过向所有指定隧道传递消息）。

此提案的委托部分的一个替代方案是通过发送一个[LeaseSet](http://localhost:63465/docs/specs/common-structures/#leaseset)哈希，该哈希类似于现有的指定目标[RouterIdentity](http://localhost:63465/docs/specs/common-structures/#common-structure-specification)哈希的能力。这将导致消息更小并且可能出现更新的LeaseSet。然而：

1. 这将强迫OBEP进行查找

2. LeaseSet可能未发布到洪泛，所以查找会失败。

3. LeaseSet可能被加密，因此OBEP无法获取租约。

4. 指定LeaseSet会向OBEP透露消息的[Destination](/docs/specs/common-structures/#destination)，否则他们只能通过在网络中抓取所有LeaseSet并寻找匹配的Lease来发现。

## 设计

发起者（OBGW）将在传递指令[TUNNEL-DELIVERY](/docs/specs/i2np/#tunnel-message-delivery-instructions)放置一些（全部？）目标[Leases](http://localhost:63465/docs/specs/common-structures/#lease)，而不是只选择一个。

OBEP将选择其中一个进行传递。OBEP如果可用，将选择一个它已经连接或已知的。这将使OBEP-IBGW路径更快更可靠，并减少整体网络连接。

我们有一个未使用的传递类型（0x03）和两个剩余位（0和1）在[TUNNEL-DELIVERY](/docs/specs/i2np/#tunnel-message-delivery-instructions)的标志中，我们可以利用这些来实现这些功能。

## 安全影响

此提案不会改变有关OBGW的目标Destination或他们对NetDB的视图所泄露的信息量：

- 控制OBEP并从NetDB抓取LeaseSet的对手已经可以通过搜索[TunnelId](http://localhost:63465/docs/specs/common-structures/#tunnelid) / [RouterIdentity](http://localhost:63465/docs/specs/common-structures/#common-structure-specification)对来确定消息是否发送到某个特定Destination。最坏情况下，TMDI中多个Leases的存在可能会使其在对手数据库中更快找到匹配项。

- 操作恶意Destination的对手已经可以通过发布包含不同入站隧道的LeaseSets给不同洪泛点，并观察OBGW连接通过哪些隧道，来获取有关连接受害者的NetDB视图的信息。从他们的角度来看，OBEP选择使用哪条隧道在功能上与OBGW进行选择完全相同。

多播标志泄露了OBGW正在向OBEPs进行多播的事实。这在实现更高级别协议时应考虑性能与隐私的权衡。作为可选标志，用户可以为其应用做出适当的决定。然而，作为兼容应用的默认行为可能有好处，因为各种应用的广泛使用可以减少哪个特定应用发出消息的信息泄漏。

## 规范

第一片段传递指令[TUNNEL-DELIVERY](/docs/specs/i2np/#tunnel-message-delivery-instructions)将修改如下：

```
+----+----+----+----+----+----+----+----+
|flag|  隧道 ID (opt)  |              |
+----+----+----+----+----+              +
|                                       |
+                                       +
|         到哈希 (optional)            |
+                                       +
|                                       |
+                        +----+----+----+
|                        |dly |  消息  
+----+----+----+----+----+----+----+----+
 ID (opt) |扩展选项 (opt)|cnt | (o)
+----+----+----+----+----+----+----+----+
 隧道 ID N   |                        |
+----+----+----+                        +
|                                       |
+                                       +
|         到哈希 N (optional)          |
+                                       +
|                                       |
+              +----+----+----+----+----+
|              | 隧道 ID N+1 (o) |    |
+----+----+----+----+----+----+    +
|                                       |
+                                       +
|         到哈希 N+1 (optional)        |
+                                       +
|                                       |
+                                  +----+
|                                  | sz
+----+----+----+----+----+----+----+----+
     |
+----+

标志 ::
       1 字节
       比特顺序：76543210
       比特6-5：传递类型
                 0x03 = 隧道
       比特0：多播？如果0，传递到一个隧道
                         如果1，传递到所有隧道
                         如果传递类型不是隧道，则设为0以兼容未来使用

计数 ::
       1 字节
       可选，当传递类型是隧道时存在
       2-255 - 后跟的id/hash对的数量

隧道ID :: `TunnelId`
到哈希 ::
       每个36字节
       可选，当传递类型是隧道时存在
       id/hash对

总长度：典型长度是：
       75字节用于计数2隧道传递（未分段隧道消息）；
       79字节用于计数2隧道传递（第一片段）

其余传递指令不变
```

## 兼容性

唯一需要理解新规范的节点是OBGWs和OBEPs。因此，我们可以通过使其使用取决于目标I2P版本[VERSIONS](/docs/specs/i2np/#protocol-versions)，将这次改变与现有网络兼容：

* OBGWs在建立出站隧道时，须基于其[RouterInfo](http://localhost:63465/docs/specs/common-structures/#routerinfo)中广告的I2P版本选择兼容OBEPs。

* 广告目标版本的节点必须支持解析新标志，并且不得将指令作为无效指令拒绝。
