---
title: "不可见多重宿主"
number: "140"
author: "str4d"
created: "2017-05-22"
lastupdated: "2017-07-04"
status: "打开"
thread: "http://zzz.i2p/topics/2335"
toc: true
---

## 概述

本提案概述了一个协议设计，使 I2P 客户端、服务或外部负载均衡器进程能够透明地管理托管单个 [Destination](http://localhost:63465/docs/specs/common-structures/#destination) 的多个 router。

该提案目前没有指定具体的实现方式。它可以作为 [I2CP](/docs/specs/i2cp/) 的扩展来实现，或者作为一个新协议来实现。

## 动机

Multihoming是指使用多个router来托管同一个Destination。目前在I2P中实现multihoming的方法是在每个router上独立运行相同的Destination；客户端在任何特定时间使用的router是最后一个发布LeaseSet的router。

这是一个临时解决方案，在大规模网站中可能无法正常工作。假设我们有100个多归属router，每个都有16个tunnel。这意味着每10分钟有1600个LeaseSet发布，或者说每秒钟接近3个。floodfill节点会不堪重负，限流机制会启动。而这还没有考虑查询流量。

提案123通过元LeaseSet解决了这个问题，元LeaseSet列出了100个真实的LeaseSet哈希值。查找变成了一个两阶段过程：首先查找元LeaseSet，然后查找其中一个指定的LeaseSet。这是解决查找流量问题的好方案，但它本身会造成严重的隐私泄露：通过监控发布的元LeaseSet可以确定哪些多宿主路由器在线，因为每个真实的LeaseSet都对应一个单独的路由器。

我们需要一种方式让I2P客户端或服务能够将单个Destination分布到多个router上，这种方式从LeaseSet本身的角度来看与使用单个router无法区分。

## 设计

### Definitions

    User
        The person or organisation wanting to multihome their Destination(s). A
        single Destination is considered here without loss of generality (WLOG).

    Client
        The application or service running behind the Destination. It may be a
        client-side, server-side, or peer-to-peer application; we refer to it as
        a client in the sense that it connects to the I2P routers.

        The client consists of three parts, which may all be in the same process
        or may be split across processes or machines (in a multi-client setup):

        Balancer
            The part of the client that manages peer selection and tunnel
            building. There is a single balancer at any one time, and it
            communicates with all I2P routers. There may be failover balancers.

        Frontend
            The part of the client that can be operated in parallel. Each
            frontend communicates with a single I2P router.

        Backend
            The part of the client that is shared between all frontends. It has
            no direct communication with any I2P router.

    Router
        An I2P router run by the user that sits at the boundary between the I2P
        network and the user's network (akin to an edge device in corporate
        networks). It builds tunnels under the command of a balancer, and routes
        packets for a client or frontend.

### High-level overview

想象以下所需的配置：

- 一个具有单个 Destination 的客户端应用程序。
- 四个 router，每个管理三条入站 tunnel。
- 所有十二条 tunnel 都应该发布在单个 LeaseSet 中。

### Single-client

```
                -{ [Tunnel 1]===\
                 |-{ [Tunnel 2]====[Router 1]-----
                 |-{ [Tunnel 3]===/               \
                 |                                 \
                 |-{ [Tunnel 4]===\                 \
  [Destination]  |-{ [Tunnel 5]====[Router 2]-----   \
    \            |-{ [Tunnel 6]===/               \   \
     [LeaseSet]--|                               [Client]
                 |-{ [Tunnel 7]===\               /   /
                 |-{ [Tunnel 8]====[Router 3]-----   /
                 |-{ [Tunnel 9]===/                 /
                 |                                 /
                 |-{ [Tunnel 10]==\               /
                 |-{ [Tunnel 11]===[Router 4]-----
                  -{ [Tunnel 12]==/
```
### 定义

```
                -{ [Tunnel 1]===\
                 |-{ [Tunnel 2]====[Router 1]---------[Frontend 1]
                 |-{ [Tunnel 3]===/          \                    \
                 |                            \                    \
                 |-{ [Tunnel 4]===\            \                    \
  [Destination]  |-{ [Tunnel 5]====[Router 2]---\-----[Frontend 2]   \
    \            |-{ [Tunnel 6]===/          \   \                \   \
     [LeaseSet]--|                         [Balancer]            [Backend]
                 |-{ [Tunnel 7]===\          /   /                /   /
                 |-{ [Tunnel 8]====[Router 3]---/-----[Frontend 3]   /
                 |-{ [Tunnel 9]===/            /                    /
                 |                            /                    /
                 |-{ [Tunnel 10]==\          /                    /
                 |-{ [Tunnel 11]===[Router 4]---------[Frontend 4]
                  -{ [Tunnel 12]==/
```
### 高层概述

- 加载或生成一个 Destination。

- 与每个路由器建立一个会话，绑定到目标地址。

- 定期（大约每十分钟，但会根据tunnel活跃度有所增减）：

- 从每个路由器获取快速层级。

- 使用对等节点的超集来构建往返每个 router 的隧道。

    - By default, tunnels to/from a particular router will use peers from
      that router's fast tier, but this is not enforced by the protocol.

- 从所有活跃的路由器收集活跃入站隧道集合，并创建一个 LeaseSet。

- 通过一个或多个 router 发布 LeaseSet。

### 单客户端

要创建和管理这个配置，客户端需要以下超出当前 [I2CP](/docs/specs/i2cp/) 所提供功能的新功能：

- 告诉 router 构建隧道，但不为其创建 LeaseSet。
- 获取入站池中当前隧道的列表。

此外，以下功能将使客户端在管理其 tunnel 方面具有显著的灵活性：

- 获取一个 router 快速层的内容。
- 告诉一个 router 使用给定的对等节点列表构建入站或出站 tunnel。

### 多客户端

```
         Client                           Router

                    --------------------->  Create Session
   Session Status  <---------------------
                    --------------------->  Get Fast Tier
        Peer List  <---------------------
                    --------------------->  Create Tunnel
    Tunnel Status  <---------------------
                    --------------------->  Get Tunnel Pool
      Tunnel List  <---------------------
                    --------------------->  Publish LeaseSet
                    --------------------->  Send Packet
      Send Status  <---------------------
  Packet Received  <---------------------
```
### 通用客户端进程

**创建会话** - 为给定的 Destination 创建会话。

**Session Status** - 确认会话已建立，客户端现在可以开始构建tunnel。

**Get Fast Tier** - 请求当前 router 考虑用于构建 tunnel 的对等节点列表。

**Peer List** - router已知的对等节点列表。

**创建隧道** - 请求 router 通过指定的对等节点构建新隧道。

**Tunnel状态** - 特定tunnel构建的结果，一旦可用即显示。

**Get Tunnel Pool** - 请求获取目标地址的入站或出站池中当前隧道的列表。

**Tunnel 列表** - 请求池的 tunnel 列表。

**发布 LeaseSet** - 请求 router 通过目标地址的某个出站 tunnel 发布提供的 LeaseSet。无需回复状态；router 应该持续重试，直到确信 LeaseSet 已被发布。

**发送数据包** - 来自客户端的出站数据包。可选择指定数据包必须（应该？）通过的出站tunnel。

**发送状态** - 通知客户端数据包发送的成功或失败。

**数据包已接收** - 客户端接收到的传入数据包。可选择性地指定接收该数据包的入站tunnel(?)

## Security implications

从router的角度来看，这种设计在功能上等同于现状。router仍然构建所有tunnel，维护自己的对等配置文件，并强制执行router和客户端操作之间的分离。默认配置是完全相同的，因为该router的tunnel是从其自己的快速层构建的。

从netDB的角度来看，通过此协议创建的单个LeaseSet与现状相同，因为它利用了预先存在的功能。然而，对于接近16个Lease的较大LeaseSet，观察者可能能够确定该LeaseSet是多宿主的：

- 快速层的当前最大大小为 75 个节点。入站网关（IBGW，在 Lease 中发布的节点）从该层的一部分中选择（通过哈希而非计数按隧道池随机分区）：

      1 hop
          The whole fast tier

      2 hops
          Half of the fast tier
          (the default until mid-2014)

      3+ hops
          A quarter of the fast tier
          (3 being the current default)

这意味着平均来说，IBGW 将来自一组 20-30 个对等节点。

- 在单宿主设置中，一个完整的 16-tunnel LeaseSet 将有 16 个 IBGW，这些 IBGW 从最多（比如）20 个对等节点的集合中随机选择。

- 在使用默认配置的4个router多宿主设置中，一个完整的16-tunnel LeaseSet将从最多80个对等节点的集合中随机选择16个IBGW，尽管各router之间可能会有一部分共同的对等节点。

因此，使用默认配置时，通过统计分析可能会发现某个 LeaseSet 是由此协议生成的。也可能会推断出有多少个 router，尽管快速层级上的节点变动会降低这种分析的有效性。

由于客户端完全控制选择哪些对等节点，通过从缩减的对等节点集合中选择IBGW，可以减少或消除这种信息泄露。

## Compatibility

这种设计与网络完全向后兼容，因为LeaseSet格式没有任何改动。所有router都需要了解新协议，但这不是问题，因为它们都由同一个实体控制。

## Performance and scalability notes

每个 LeaseSet 最多包含 16 个 Lease 的上限在此提案中保持不变。对于需要更多隧道的目标地址，有两种可能的网络修改：

- 增加LeaseSet大小的上限。这是最简单的实现方式（尽管在能够广泛使用之前仍需要全网络的支持），但可能会由于数据包更大而导致查找速度变慢。最大可行的LeaseSet大小由底层传输协议的MTU定义，因此约为16kB。

- 实现提案 123 以支持分层 LeaseSets。结合此提案，子 LeaseSets 的目的地可以分布在多个 routers 上，有效地像明网服务的多个 IP 地址一样工作。

## Acknowledgements

感谢 psi 的讨论，促成了这个提案。
