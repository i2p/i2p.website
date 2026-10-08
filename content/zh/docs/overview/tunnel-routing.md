---
title: "Tunnel 路由"
description: "I2P tunnel 术语、构建和运行概述"
slug: "tunnel-routing"
lastUpdated: "2026-03"
accurateFor: "0.9.68"
---

## 概述

本页面包含 I2P tunnel 术语和操作的概述，并提供指向更多技术页面、详细信息和规范的链接。

正如在[介绍](/docs/overview/intro/)中简要说明的那样，I2P 构建虚拟的"tunnel"——通过一系列 router 的临时单向路径。这些 tunnel 被分类为入站 tunnel（传送给它的所有内容都会流向 tunnel 创建者）或出站 tunnel（tunnel 创建者将消息推送离开自己）。当 Alice 想要向 Bob 发送消息时，她通常会通过她现有的某个出站 tunnel 发送消息，并指示该 tunnel 的端点将消息转发到 Bob 当前某个入站 tunnel 的网关 router，然后该网关将消息传递给 Bob。

![Alice 通过她的出站 tunnel 连接到 Bob 的入站 tunnel](/images/tunnelSending.svg)

```
A: Outbound Gateway (Alice)
B: Outbound Participant
C: Outbound Endpoint
D: Inbound Gateway
E: Inbound Participant
F: Inbound Endpoint (Bob)
```
---

## Tunnel 词汇表

- **Tunnel gateway** - tunnel 中的第一个 router。对于入站 tunnel，这是在[网络数据库](/docs/overview/network-database/)中发布的 LeaseSet 中提到的那个。对于出站 tunnel，gateway 是发起的 router。（例如上面的 A 和 D）

- **Tunnel endpoint** - tunnel 中的最后一个 router。（例如上面的 C 和 F）

- **Tunnel 参与者** - tunnel 中除了网关或端点之外的所有 router（例如上述的 B 和 E）

- **n跳tunnel** - 具有特定路由器间跳数的tunnel，例如：
  - **0跳tunnel** - 网关同时也是端点的tunnel
  - **1跳tunnel** - 网关直接与端点通信的tunnel
  - **2跳（或更多跳）tunnel** - 至少有一个中间tunnel参与者的tunnel。（上述图表包含两个2跳tunnel - 一个从Alice出站，一个到Bob入站）

- **Tunnel ID** - 一个[4字节整数](/docs/specs/common-structures/#type_TunnelId)，在tunnel的每个跳点都不同，并且在router上的所有tunnel中唯一。由tunnel创建者随机选择。

---

## Tunnel 构建信息

执行三种角色（gateway、participant、endpoint）的 router 在初始的 [Tunnel Build Message](/docs/specs/tunnel-creation/) 中被给予不同的数据片段来完成它们的任务：

**tunnel 网关获得：**

- **tunnel encryption key** - 用于加密消息和指令到下一跳的 [AES 私钥](/docs/specs/common-structures/#type_SessionKey)
- **tunnel IV key** - 用于对发送到下一跳的 IV 进行双重加密的 [AES 私钥](/docs/specs/common-structures/#type_SessionKey)
- **reply key** - 用于加密 tunnel 构建请求回复的 [AES 公钥](/docs/specs/common-structures/#type_SessionKey)
- **reply IV** - 用于加密 tunnel 构建请求回复的 IV
- **tunnel id** - 4 字节整数（仅限入站网关）
- **next hop** - 路径中下一个 router 是哪个（除非这是一个 0 跳 tunnel，网关也是端点）
- **next tunnel id** - 下一跳上的 tunnel ID

**所有中间tunnel参与者获得：**

- **tunnel encryption key** - 用于加密消息和指令到下一跳的 [AES 私钥](/docs/specs/common-structures/#type_SessionKey)
- **tunnel IV key** - 用于对发送到下一跳的 IV 进行双重加密的 [AES 私钥](/docs/specs/common-structures/#type_SessionKey)
- **reply key** - 用于加密 tunnel 构建请求回复的 [AES 公钥](/docs/specs/common-structures/#type_SessionKey)
- **reply IV** - 用于加密 tunnel 构建请求回复的 IV
- **tunnel id** - 4 字节整数
- **next hop** - 路径中的下一个 router
- **next tunnel id** - 下一跳上的 tunnel ID

**tunnel 端点获得：**

- **tunnel 加密密钥** - 用于加密发送到端点（自身）的消息和指令的 [AES 私钥](/docs/specs/common-structures/#type_SessionKey)
- **tunnel IV 密钥** - 用于对发送到端点（自身）的 IV 进行双重加密的 [AES 私钥](/docs/specs/common-structures/#type_SessionKey)
- **回复密钥** - 用于加密 tunnel 构建请求回复的 [AES 公钥](/docs/specs/common-structures/#type_SessionKey)（仅用于出站端点）
- **回复 IV** - 用于加密 tunnel 构建请求回复的 IV（仅用于出站端点）
- **tunnel id** - 4 字节整数（仅用于出站端点）
- **回复 router** - 发送回复通过的 tunnel 的入站网关（仅用于出站端点）
- **回复 tunnel id** - 回复 router 的 tunnel ID（仅用于出站端点）

详细信息请参见 [tunnel 创建规范](/docs/specs/tunnel-creation/)。

---

## Tunnel 池化

用于特定目的的多个 tunnel 可以被归组为一个"tunnel pool"，如 [tunnel 规范](/docs/specs/tunnel-implementation/#tunnel.pooling) 中所述。这提供了冗余性和额外的带宽。router 自身使用的池称为"exploratory tunnels"。应用程序使用的池称为"client tunnels"。

---

## 隧道长度

如上所述，每个客户端请求其router提供包含至少一定跳数的tunnel。决定在自己的出站和入站tunnel中使用多少个router对I2P提供的延迟、吞吐量、可靠性和匿名性有重要影响 - 消息需要通过的节点越多，到达目的地的时间就越长，其中一个router过早失效的可能性就越大。tunnel中的router越少，对手就越容易发起流量分析攻击并破解某人的匿名性。tunnel长度由客户端通过[I2CP选项](/docs/specs/i2cp/#options)指定。tunnel中的最大跳数为7。

### 0跳tunnel

在tunnel中没有远程router的情况下，用户具有非常基本的合理推诿性（因为没有人能确定发送消息的对等节点不是仅仅作为tunnel的一部分进行转发）。然而，进行统计分析攻击并注意到针对特定目的地的消息总是通过单个网关发送将是相当容易的。针对出站0跳tunnel的统计分析更为复杂，但可能显示类似的信息（尽管实施起来会稍微困难一些）。

### 1跳tunnel

当 tunnel 中只有一个远程 router 时，用户既具有合理推诿性又具有基本匿名性，只要他们没有面对内部对手（如[威胁模型](/docs/overview/threat-model/)中所述）。然而，如果对手运行足够数量的 router，使得 tunnel 中的单个远程 router 经常是那些被攻陷的 router 之一，他们就能够发起上述统计流量分析攻击。

### 2跳tunnel

当tunnel中有两个或更多远程router时，发起流量分析攻击的成本会增加，因为需要攻破许多远程router才能发起此类攻击。

### 3跳（或更多）tunnel

为了降低遭受[某些攻击](https://blog.torproject.org/one-cell-enough-break-tors-anonymity/)的风险，建议使用3个或更多跳数以获得最高级别的保护。[最近的研究](https://blog.torproject.org/one-cell-enough-break-tors-anonymity/)也得出结论：超过3个跳数并不能提供额外的保护。

### Tunnel 默认长度

router 默认为其探索性隧道使用 2 跳 tunnel。客户端 tunnel 默认值由应用程序使用 [I2CP 选项](/docs/specs/i2cp/#options) 设置。大多数应用程序默认使用 2 或 3 跳。

---

## Tunnel 测试

所有 tunnel 都会被其创建者定期测试，通过向出站 tunnel 发送 DeliveryStatusMessage 并绑定到另一个入站 tunnel（同时测试两个 tunnel）。如果任一 tunnel 连续多次测试失败，就会被标记为不再正常工作。如果它被用于客户端的入站 tunnel，则会创建新的 leaseSet。Tunnel 测试失败也会反映在[对等体配置文件中的容量评级](/docs/overview/peer-selection/#capacity)中。

---

Tunnel 创建由 [garlic routing](/docs/overview/garlic-routing/) 处理，向 router 发送 Tunnel Build Message，请求其参与 tunnel（为其提供所有适当的信息，如上所述，以及一个证书，目前是一个'null'证书，但在必要时将支持 hashcash 或其他非免费证书）。该 router 将消息转发到 tunnel 中的下一跳。详细信息请参见 [tunnel creation specification](/docs/specs/tunnel-creation/)。

## Tunnel 创建

---

多层加密由隧道消息的[garlic encryption](/docs/overview/garlic-routing/)处理。详细信息请参见[隧道规范](/docs/specs/tunnel-implementation/)。每一跳的IV都使用单独的密钥进行加密，具体说明见该文档。

## Tunnel 加密

---

---

## 未来工作

- 可以使用其他 tunnel 测试技术，比如将多个测试用 garlic encryption 包装成 cloves，单独测试各个 tunnel 参与者等。

- 移至3跳探索tunnel默认设置。

- 在遥远的未来版本中，可能会实现指定池化、混合和干扰数据生成设置的选项。

- 在未来的远期版本中，可能会实施对tunnel生命周期内允许的消息数量和大小的限制（例如每分钟不超过300条消息或1MB）。

---

## 另请参见

- [Tunnel 规范](/docs/specs/tunnel-implementation/)
- [Tunnel 创建规范](/docs/specs/tunnel-creation/)
- [单向 tunnel](/docs/legacy/unidirectional/)
- [Tunnel 消息规范](/docs/specs/tunnel-message/)
- [Garlic routing](/docs/overview/garlic-routing/)
- [ElGamal/AES+SessionTag](/docs/specs/elgamal-aes/)
- [I2CP 选项](/docs/specs/i2cp/#options)
