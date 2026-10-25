---
title: "Garlic Routing"
description: "理解I2P中的garlic routing术语、架构和实现"
slug: "garlic-routing"
aliases:
  - "/zh/how_garlicrouting"
  - "/zh/how_garlicrouting/"
lastUpdated: "2025-10"
accurateFor: "0.9.12"
---

## Garlic Routing 和"Garlic"术语

在提及I2P技术时，"garlic routing"和"garlic encryption"这两个术语经常被相当宽泛地使用。在这里，我们解释这些术语的历史、各种含义，以及"garlic"方法在I2P中的使用。

"Garlic routing"一词最初由[Michael J. Freedman](https://www.cs.princeton.edu/~mfreed/)在Roger Dingledine的Free Haven[硕士论文](https://www.freehaven.net/papers.html)第8.1.1节（2000年6月）中提出，该概念源于[Onion Routing](https://www.onion-router.net/)。

"Garlic"这个术语最初可能是由I2P开发者使用的，因为I2P实现了Freedman所描述的一种打包形式，或者只是为了强调与Tor的一般差异。具体的推理可能已经湮没在历史中。一般来说，当提到I2P时，术语"garlic"可能意味着三种含义之一：

1. 分层加密
2. 将多个消息打包在一起
3. ElGamal/AES 加密

不幸的是，I2P 在过去几年中对"garlic"术语的使用并不总是准确的；因此读者在遇到该术语时需要谨慎理解。希望下面的解释能够澄清这些问题。

### 分层加密

洋葱路由是一种通过一系列对等节点构建路径或tunnel的技术，然后使用该tunnel。消息由发起者重复加密，然后由每个跳点解密。在构建阶段，每个对等节点只能看到下一跳的路由指令。在操作阶段，消息通过tunnel传递，消息及其路由指令只对tunnel的端点可见。

这类似于 Mixmaster（参见[网络比较](/docs/overview/comparison/)）发送消息的方式——获取一条消息，用接收者的公钥加密它，然后将该加密消息连同指定下一跳的指令一起再次加密，接着将得到的加密消息继续这个过程，直到路径上的每一跳都有一层加密。

在这个意义上，"garlic routing"作为一般概念与"onion routing"是相同的。当然，在I2P中的实现与Tor中的实现存在几个差异；请参见下文。即便如此，两者有很多相似之处，因此I2P受益于[大量关于onion routing的学术研究](https://www.onion-router.net/Publications.html)、[Tor和类似mixnet的研究](https://freehaven.net/anonbib/topic.html)。

### 捆绑多个消息

Michael Freedman 将"garlic routing"定义为洋葱路由的扩展，其中多个消息被捆绑在一起。他称每个消息为"bulb"。所有消息都有各自的传递指令，在端点处被暴露出来。这允许将洋葱路由的"回复块"与原始消息高效地捆绑在一起。

这个概念在I2P中得到了实现，如下所述。我们将garlic"球茎"称为"瓣"。可以包含任意数量的消息，而不是仅仅一条消息。这与Tor中实现的洋葱路由有显著区别。然而，这只是I2P和Tor之间众多主要架构差异中的一个；也许仅凭这一点，还不足以证明术语变更的合理性。

与Freedman描述的方法的另一个不同之处在于路径是单向的——没有像洋葱路由或mixmaster回复块中那样的"转折点"，这大大简化了算法并允许更灵活和可靠的传递。

### ElGamal/AES 加密

在某些情况下，"garlic encryption"可能仅仅指[ElGamal/AES+SessionTag](/docs/specs/elgamal-aes/)加密（没有多层加密）。

---

## I2P 中的 "Garlic" 方法

现在我们已经定义了各种"garlic"术语，我们可以说I2P在三个地方使用garlic routing、捆绑和加密：

1. 用于构建和通过 tunnel 路由（分层加密）
2. 用于确定端到端消息传递的成功或失败（捆绑）
3. 用于发布一些网络数据库条目（降低成功流量分析攻击的概率）（ElGamal/AES）

此外，这种技术还可以通过多种重要方式来提升网络性能，包括利用传输延迟/吞吐量权衡，以及通过冗余路径分支数据来提高可靠性。

### Tunnel构建和路由

在I2P中，tunnel是单向的。每一方都构建两个tunnel，一个用于出站流量，一个用于入站流量。因此，单次往返消息和回复需要四个tunnel。

Tunnel 的构建和使用采用分层加密技术。详细说明请参阅 [tunnel 实现页面](/docs/specs/tunnel-implementation/)。我们使用 [ElGamal/AES+SessionTag](/docs/specs/elgamal-aes/) 进行加密。

tunnel 是传输所有 [I2NP 消息](/docs/specs/i2np/) 的通用机制，而 Garlic 消息不用于构建 tunnel。我们不会将多个 I2NP 消息打包到单个 Garlic 消息中以在出站 tunnel 端点进行解包；tunnel 加密已经足够了。

### 端到端消息捆绑

在 tunnel 之上的层级中，I2P 在[目标节点](/docs/specs/common-structures/)之间传递端到端消息。就像在单个 tunnel 内一样，我们使用 [ElGamal/AES+SessionTag](/docs/specs/elgamal-aes/) 进行加密。通过 [I2CP interface](/docs/api/i2cp/) 传递给 router 的每个客户端消息都会成为一个单独的 Garlic Clove，在 Garlic Message 内包含自己的传递指令。传递指令可以指定一个 Destination、router 或 tunnel。

通常，Garlic Message 只包含一个 clove。但是，router 会定期在 Garlic Message 中捆绑两个额外的 clove：

![Garlic Message Cloves](/images/garliccloves.svg)

1. **传递状态消息**，带有传递指令，指定将其发送回始发router作为确认。这类似于参考文献中描述的"回复块"或"回复洋葱"。它用于确定端到端消息传递的成功或失败。始发router如果在预期时间内未收到传递状态消息，可能会修改到远端目标的路由，或采取其他行动。

2. **数据库存储消息**，包含发起方目标的 LeaseSet，并带有指定远端目标 router 的传递指令。通过定期捆绑 LeaseSet，router 确保远端能够维持通信。否则远端将不得不向 floodfill router 查询网络数据库条目，并且所有 LeaseSet 都必须发布到网络数据库，如[网络数据库页面](/docs/specs/common-structures/)中所述。

默认情况下，当本地 LeaseSet 发生变化、传递额外的 Session Tags 或者消息在前一分钟内未被捆绑时，Delivery Status 和 Database Store Messages 会被打包在一起。

显然，这些额外的消息目前是为特定目的而捆绑的，并非通用路由方案的一部分。

从0.9.12版本开始，传递状态消息由发起者包装在另一个Garlic Message中，这样内容就被加密了，对返回路径上的router不可见。

### 存储到 Floodfill 网络数据库

如[网络数据库页面](/docs/specs/common-structures/)所解释的，本地 leaseSet 被发送到 floodfill router，包装在 Database Store Message 中并封装在 Garlic Message 内，因此对隧道的出站网关不可见。

---

## 未来工作

Garlic Message 机制非常灵活，为实现多种类型的混合网络传递方法提供了结构。结合隧道消息传递指令中未使用的延迟选项，可以实现广泛的批处理、延迟、混合和路由策略。

特别是，在出站 tunnel 端点处存在更大灵活性的潜力。消息可能从那里路由到多个 tunnel 中的一个（从而最小化点对点连接），或者多播到多个 tunnel 以实现冗余，或用于流媒体音频和视频。

这些实验可能会与确保安全性和匿名性的需求产生冲突，例如限制某些路由路径、限制可能沿各种路径转发的I2NP消息类型，以及强制执行某些消息过期时间。

作为 ElGamal/AES 加密的一部分，garlic 消息包含发送方指定数量的填充数据，允许发送方主动采取对抗流量分析的对策。除了需要填充到16字节的倍数这一要求外，这一功能目前并未被使用。

与 [floodfill routers](/docs/specs/common-structures/) 之间额外消息的加密。

---

## 参考资料

- garlic routing 术语最早由 Roger Dingledine 在 Free Haven [硕士论文](https://www.freehaven.net/papers.html)（2000年6月）中提出，参见由 [Michael J. Freedman](https://www.cs.princeton.edu/~mfreed/) 撰写的第8.1.1节。
- [Onion Router 出版物](https://www.onion-router.net/Publications.html)
- [洋葱路由（维基百科）](https://en.wikipedia.org/wiki/Onion_routing)
- [Garlic Routing（维基百科）](https://en.wikipedia.org/wiki/Garlic_routing)
- [Tor 项目](https://www.torproject.org/)
- [Free Haven Anonbib](https://freehaven.net/anonbib/topic.html)
- 洋葱路由最初由 David M. Goldschlag、Michael G. Reed 和 Paul F. Syverson 在1996年的 [隐藏路由信息](https://www.onion-router.net/Publications/IH-1996.pdf) 中描述。
