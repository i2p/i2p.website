---
title: "性能"
description: "I2P网络性能：速度、连接和资源管理"
slug: "performance"
aliases:
  - "/zh/about/performance/future"
  - "/zh/about/performance/future/"
  - "/zh/about/performance/history"
  - "/zh/about/performance/history/"
  - "/zh/performance"
  - "/zh/performance/"
  - "/zh/performance-history"
  - "/zh/performance-history/"
  - "/zh/benchmarks"
  - "/zh/benchmarks/"
lastUpdated: "2025-01"
accurateFor: "0.9.65"
---

## I2P 网络性能：速度、连接和资源管理

I2P 网络是完全动态的。每个客户端都被其他节点所知晓，并会测试本地已知节点的可达性和容量。只有可达且有能力的节点才会被保存到本地 netDb 中。在 tunnel 构建过程中，会从这个节点池中选择最佳资源来构建 tunnel。由于测试持续进行，节点池会不断变化。每个 I2P 节点都知道 netDb 的不同部分，这意味着每个 router 都有不同的 I2P 节点集合可用于 tunnel。即使两个 router 拥有相同的已知节点子集，可达性和容量测试也可能显示不同的结果，因为当一个 router 进行测试时其他 router 可能正在承载负载，但当第二个 router 测试时却可能空闲。

这解释了为什么每个I2P节点都有不同的节点来构建tunnel。因为每个I2P节点都有不同的延迟和带宽，通过这些节点构建的tunnel具有不同的延迟和带宽值。而且由于每个I2P节点都构建了不同的tunnel，所以没有两个I2P节点拥有相同的tunnel集合。

服务器/客户端被称为"destination"（目标），每个destination至少有一条入站tunnel和一条出站tunnel。默认情况下每条tunnel有3跳。这意味着完整的客户端-服务器-客户端往返需要12跳（即12个不同的I2P节点）。

每个数据包都会通过6个其他I2P节点才能到达服务器：

```
client - hop1 - hop2 - hop3 - hopa1 - hopa2 - hopa3 - server
```
并在返回路径上经过6个不同的I2P节点：

```
server - hopb1 - hopb2 - hopb3 - hopc1 - hopc2 - hopc3 - client
```
网络上的流量需要在发送新数据之前收到ACK确认，它需要等到服务器返回ACK：发送数据，等待ACK，发送更多数据，等待ACK。由于RTT（往返时间）是由往返过程中每个I2P节点和每个连接的延迟累加而成，通常需要1-3秒ACK才能返回到客户端。由于TCP和I2P传输设计，数据包的大小是有限的。这些条件共同设定了每个tunnel最大带宽限制为20-50 kbyte/秒。然而，如果tunnel中只有一跳的带宽只有5 kb/秒，那么整个tunnel就被限制在5 kb/秒，与延迟和其他限制无关。

加密、延迟以及tunnel构建方式使得构建tunnel在CPU时间上代价相当昂贵。这就是为什么一个目的地只允许拥有最多6条入站tunnel和6条出站tunnel来传输数据。由于每条tunnel最大速度为50 kb/秒，一个目的地总共可以使用大约300 kb/秒的流量（实际上如果使用较短的tunnel且匿名性较低或无匿名性，速度可能会更快）。已使用的tunnel每10分钟会被丢弃，并构建新的tunnel。这种tunnel的更换，以及有时客户端关闭或失去网络连接，会导致tunnel和连接中断。这种情况的例子可以在IRC2P网络中看到连接丢失（ping超时），或者在使用eepget时遇到。

由于目的地数量有限，每个目的地的tunnel数量也有限，一个I2P节点只会使用其他I2P节点上有限数量的tunnel。例如，如果一个I2P节点是上述小例子中的"hop1"，我们只能看到1个来自客户端的参与tunnel。如果我们汇总整个I2P网络，只有相当有限数量的参与tunnel能够被构建，总带宽也有限。如果将这些有限的数量分布到所有I2P节点上，那么可用的带宽/容量只有一小部分可以使用。

为了保持匿名性，整个网络不应该使用单一的 router 来构建 tunnel。如果一个 router 为所有 I2P 节点充当 tunnel router，它就会成为一个真正的单点故障，同时也成为收集客户端 IP 和数据的中心点。这就是为什么网络在 tunnel 构建过程中将流量分布到各个节点的原因。

性能方面的另一个考量是I2P处理网状网络的方式。每个连接的逐跳传输在I2P节点上使用一个TCP或UDP连接。当有1000个连接时，就会看到1000个TCP连接。这是相当多的，而一些家用和小型办公室router只允许少量连接。I2P尝试将这些连接限制在每种UDP和TCP类型下1500个以内。这也限制了通过I2P节点路由的流量数量。

如果一个节点是可达的，带宽设置为共享 >128 kbyte/sec 且 24/7 可达，那么经过一段时间后它应该被用于参与流量。如果它在此期间断开，其他节点对该 I2P 节点进行的测试会告诉它们该节点不可达。这会在其他节点上阻止该节点至少 24 小时。因此，那些测试该节点为断开状态的其他节点在 24 小时内不会使用该节点来构建 tunnel。这就是为什么在重启/关闭你的 I2P router 后，你的流量在至少 24 小时内会较低的原因。

此外，其他I2P节点需要了解一个I2P router才能测试其可达性和容量。当您与网络交互时，可以加快这个过程，例如通过使用应用程序或访问I2P站点，这将导致更多的tunnel构建，从而为网络上的节点提供更多的活动和可达性测试。

---

## 性能改进

关于可能的未来性能改进，请参见[未来性能改进](/docs/overview/performance#future)。

有关过去的性能改进，请参阅[性能历史](/docs/overview/performance#history)。
