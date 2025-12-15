---
title: "大蒜农场协议"
number: "150"
author: "zzz"
created: "2019-05-02"
lastupdated: "2019-05-20"
status: "开放"
thread: "http://zzz.i2p/topics/2234"
toc: true
---

## 概述

这是基于 JRaft 以及其用于 TCP 实现的 "exts" 代码和 "dmprinter" 示例应用程序的 Garlic Farm 线协议规范 [JRAFT](https://github.com/datatechnology/jraft)。 JRaft 是 Raft 协议的一种实现 [RAFT](https://ramcloud.stanford.edu/wiki/download/attachments/11370504/raft.pdf)。

我们找不到任何有记录的线协议实现。然而，JRaft 实现足够简单，我们可以检查代码然后记录其协议。本提案是该努力的结果。

这将是协调发布 Meta LeaseSet 中条目的路由器的后端。详情参见提案 123。

## 目标

- 代码尺寸小
- 基于现有实现
- 无序列化 Java 对象或任何特定于 Java 的功能或编码
- 任何引导程序都超出范围。假设至少有一个其他服务器是硬编码的或以此协议之外的方式配置的。
- 支持带外和基于 I2P 的使用场景。

## 设计

Raft 协议不是一个具体协议；它仅定义一个状态机。因此，我们记录了 JRaft 的具体协议并基于其协议构建我们的协议。除了添加身份验证握手外，JRaft 协议没有变化。

Raft 选举出一个负责发布日志的领导者。日志包含 Raft 配置数据和应用数据。应用数据包含每个服务器路由器的状态和 Meta LS2 集群的目的地。服务器使用一个通用算法来确定 Meta LS2 的发布者和内容。Meta LS2 的发布者不一定是 Raft 的领导者。

## 规格

线协议通过 SSL 套接字或非 SSL 的 I2P 套接字进行。I2P 套接字通过 HTTP 代理进行代理。不支持因特网非 SSL 套接字。

### 握手与认证

JRaft 未定义。

目标：

- 用户/密码认证方法
- 版本标识符
- 集群标识符
- 可扩展性
- 使用 I2P 套接字时便于代理
- 不需要不必要地暴露服务器为 Garlic Farm 服务器
- 简单协议，因此不需要完整的 web 服务器实现
- 与通用标准兼容，因此如果愿意，实现可以使用标准库

我们将使用一种类似 websocket 的握手 [WEBSOCKET](https://en.wikipedia.org/wiki/WebSocket) 和 HTTP 摘要认证 [RFC-2617](https://tools.ietf.org/html/rfc2617)。 不支持 RFC 2617 基本认证。通过 HTTP 代理进行代理时，请按照 [RFC-2616](https://tools.ietf.org/html/rfc2616) 指定的与代理通信。

凭证
```````````

用户名和密码是按集群还是按服务器区分，依赖于实现。

HTTP 请求 1
``````````````

发起方将发送以下内容。

所有行都需使用 CRLF 作为 HTTP 的要求。

```text
GET /GarlicFarm/CLUSTER/VERSION/websocket HTTP/1.1
  Host: (ip):(port)
  Cache-Control: no-cache
  Connection: close
  (其他标头被忽略)
  (空行)

  CLUSTER 是集群的名称（默认 "farm"）
  VERSION 是 Garlic Farm 版本（当前为 "1"）
```

HTTP 响应 1
```````````````

如果路径不正确，接收者将发送标准的 "HTTP/1.1 404 Not Found" 响应，正如 [RFC-2616](https://tools.ietf.org/html/rfc2616) 所指。

如果路径正确，接收者将发送标准的 "HTTP/1.1 401 Unauthorized" 响应，包括 WWW-Authenticate HTTP 摘要认证标头，如 [RFC-2617](https://tools.ietf.org/html/rfc2617) 所指。

双方然后将关闭套接字。

HTTP 请求 2
``````````````

发起方将发送以下内容，如 [RFC-2617](https://tools.ietf.org/html/rfc2617) 和 [WEBSOCKET](https://en.wikipedia.org/wiki/WebSocket) 所指。

所有行都需使用 CRLF 作为 HTTP 的要求。

```text
GET /GarlicFarm/CLUSTER/VERSION/websocket HTTP/1.1
  Host: (ip):(port)
  Cache-Control: no-cache
  Connection: keep-alive, Upgrade
  Upgrade: websocket
  (Sec-Websocket-* 标头如果通过代理)
  Authorization: (HTTP 摘要认证标头如 RFC 2617)
  (其他标头被忽略)
  (空行)

  CLUSTER 是集群的名称（默认 "farm"）
  VERSION 是 Garlic Farm 版本（当前为 "1"）
```

HTTP 响应 2
```````````````

如果认证不正确，接收者将发送另一个标准的 "HTTP/1.1 401 Unauthorized" 响应，如 [RFC-2617](https://tools.ietf.org/html/rfc2617) 所指。

如果认证正确，接收者将发送以下响应，如 [WEBSOCKET](https://en.wikipedia.org/wiki/WebSocket) 所指。

所有行都需使用 CRLF 作为 HTTP 的要求。

```text
HTTP/1.1 101 Switching Protocols
  Connection: Upgrade
  Upgrade: websocket
  (Sec-Websocket-* 标头)
  (其他标头被忽略)
  (空行)
```

此后接收，套接字保持开放。如下所定义的 Raft 协议开始，在同一套接字上进行。

缓存
`````````

凭证应缓存至少一小时，以便随后连接可以直接跳到上面的 "HTTP Request 2"。

### 消息类型

消息有两种类型，请求和响应。请求可能包含日志条目，并且大小不固定；响应不包含日志条目，并且是固定大小。

消息类型 1-4 是 Raft 定义的标准 RPC 消息。这是核心 Raft 协议。

消息类型 5-15 是 JRaft 定义的扩展 RPC 消息，以支持客户端、动态服务器更改以及高效日志同步。

消息类型 16-17 是 Raft 第 7 节中定义的日志压缩 RPC 消息。

| 消息 | 编号 | 发送方 | 接收方 | 备注 |
|------|------|--------|--------|------|
| RequestVoteRequest | 1 | 候选人 | 跟随者 | 标准 Raft RPC；不应包含日志条目 |
| RequestVoteResponse | 2 | 跟随者 | 候选人 | 标准 Raft RPC |
| AppendEntriesRequest | 3 | 领导者 | 跟随者 | 标准 Raft RPC |
| AppendEntriesResponse | 4 | 跟随者 | 领导者 / 客户端 | 标准 Raft RPC |
| ClientRequest | 5 | 客户端 | 领导者 / 跟随者 | 响应是 AppendEntriesResponse；必须仅包含应用程序日志条目 |
| AddServerRequest | 6 | 客户端 | 领导者 | 必须仅包含一个 ClusterServer 日志条目 |
| AddServerResponse | 7 | 领导者 | 客户端 | 领导者也会发送 JoinClusterRequest |
| RemoveServerRequest | 8 | 跟随者 | 领导者 | 必须仅包含一个 ClusterServer 日志条目 |
| RemoveServerResponse | 9 | 领导者 | 跟随者 | |
| SyncLogRequest | 10 | 领导者 | 跟随者 | 必须仅包含一个 LogPack 日志条目 |
| SyncLogResponse | 11 | 跟随者 | 领导者 | |
| JoinClusterRequest | 12 | 领导者 | 新服务器 | 邀请加入；必须仅包含一个 Configuration 日志条目 |
| JoinClusterResponse | 13 | 新服务器 | 领导者 | |
| LeaveClusterRequest | 14 | 领导者 | 跟随者 | 命令离开 |
| LeaveClusterResponse | 15 | 跟随者 | 领导者 | |
| InstallSnapshotRequest | 16 | 领导者 | 跟随者 | Raft 第 7 节；必须仅包含一个 SnapshotSyncRequest 日志条目 |
| InstallSnapshotResponse | 17 | 跟随者 | 领导者 | Raft 第 7 节 |

### 建立

在 HTTP 握手后，建立序列如下：

```text
新服务器 Alice              随机跟随者 Bob

  ClientRequest   ------->
          <---------   AppendEntriesResponse

  如果 Bob 说他是领导者，则继续如下。
  否则，Alice 必须从 Bob 断开连接并连接到领导者。

  新服务器 Alice              领导者 Charlie

  ClientRequest   ------->
          <---------   AppendEntriesResponse
  AddServerRequest   ------->
          <---------   AddServerResponse
          <---------   JoinClusterRequest
  JoinClusterResponse  ------->
          <---------   SyncLogRequest
                       或者 InstallSnapshotRequest
  SyncLogResponse  ------->
  或者 InstallSnapshotResponse
```

断开序列：

```text
跟随者 Alice              领导者 Charlie

  RemoveServerRequest   ------->
          <---------   RemoveServerResponse
          <---------   LeaveClusterRequest
  LeaveClusterResponse  ------->
```

选举序列：

```text
候选人 Alice              跟随者 Bob

  RequestVoteRequest   ------->
          <---------   RequestVoteResponse

  如果 Alice 赢得选举：

  领导者 Alice              跟随者 Bob

  AppendEntriesRequest   ------->
  (心跳)
          <---------   AppendEntriesResponse
```

### 定义

- 来源：标识消息的发起方
- 目的地：标识消息的接收方
- 任期：参见 Raft。初始化为 0，单调递增
- 索引：参见 Raft。初始化为 0，单调递增

### 请求

请求包含一个头和零个或多个日志条目。请求包含一个固定大小的头和大小可变的日志条目。

请求头
``````````````

请求头为 45 字节，如下所示。所有值为无符号大端序。

```dataspec
消息类型：         1 字节
  来源：            ID，4 字节整数
  目的地：          ID，4 字节整数
  任期：            当前任期（见备注），8 字节整数
  上次日志任期：    8 字节整数
  上次日志索引：    8 字节整数
  提交索引：        8 字节整数
  日志条目大小：    字节总数，4 字节整数
  日志条目：        见下文，指定长度
```

#### 备注

在 RequestVoteRequest 中，任期是候选人的任期。否则，它是领导者的当前任期。

在 AppendEntriesRequest 中，当日志条目大小为零时，此消息是心跳（保持活跃）消息。

日志条目
```````````

日志包含零个或多个日志条目。每个日志条目如下。所有值为无符号大端序。

```dataspec
任期：          8 字节整数
  值类型：        1 字节
  条目大小：      字节数，4 字节整数
  条目：          指定长度
```

日志内容
````````````

所有值为无符号大端序。

| 日志值类型 | 编号 |
|------------|------|
| 应用程序 | 1 |
| 配置 | 2 |
| 集群服务器 | 3 |
| 日志包 | 4 |
| 快照同步请求 | 5 |

#### 应用程序

应用程序内容为 UTF-8 编码的 [JSON](https://www.json.org/)。参见下文的应用层部分。

#### 配置

用于领导者序列化新集群配置并将其复制到同行。包含零个或多个 ClusterServer 配置。

```dataspec
日志索引：  8 字节整数
  上次日志索引：  8 字节整数
  每个服务器的 ClusterServer 数据：
    ID：                4 字节整数
    端点数据长度：   字节数，4 字节整数
    端点数据：        形式为 "tcp://localhost:9001" 的 ASCII 字符串，指定长度
```

#### 集群服务器

集群中某个服务器的配置信息。只包含在 AddServerRequest 或 RemoveServerRequest 消息中。

用于 AddServerRequest 消息：

```dataspec
ID：                4 字节整数
  端点数据长度：   字节数，4 字节整数
  端点数据：        形式为 "tcp://localhost:9001" 的 ASCII 字符串，指定长度
```

用于 RemoveServerRequest 消息：

```dataspec
ID：                4 字节整数
```

#### 日志包

只包含在 SyncLogRequest 消息中。

以下内容在传输前进行 gzip 压缩：

```dataspec
索引数据长度： 字节数，4 字节整数
  日志数据长度：    字节数，4 字节整数
  索引数据：       每个索引 8 字节，指定长度
  日志数据：       指定长度
```

#### 快照同步请求

只包含在 InstallSnapshotRequest 消息中。

```dataspec
上次日志索引： 8 字节整数
  上次日志任期：   8 字节整数
  配置数据长度： 字节数，4 字节整数
  配置数据：      指定长度
  偏移量：        数据库中的数据偏移量，以字节计，8 字节整数
  数据长度：      字节数，4 字节整数
  数据：          指定长度
  完成：          1 表示完成，0 表示未完成（1 字节）
```

### 响应

所有响应为 26 字节，如下所示。所有值为无符号大端序。

```dataspec
消息类型：   1 字节
  来源：         ID，4 字节整数
  目的地：       通常为实际目的地 ID（见备注），4 字节整数
  任期：         当前任期，8 字节整数
  下一个索引：   初始化为领导者上次日志索引 + 1，8 字节整数
  被接受：       1 表示被接受，0 表示不被接受（见备注），1 字节
```

备注
``````

目的地 ID 通常是此消息的实际目的地。然而，对于 AppendEntriesResponse、AddServerResponse 和 RemoveServerResponse，它是当前领导者的 ID。

在 RequestVoteResponse 中，被接受为 1 表示对候选人（请求者）投票，0 表示不投票。

## 应用层

每个服务器定期在 ClientRequest 中将应用数据发布到日志中。应用数据包含每个服务器路由器的状态和 Meta LS2 集群的目的地。服务器使用通用算法来确定 Meta LS2 的发布者和内容。日志中具有最近最佳状态的服务器是 Meta LS2 的发布者。Meta LS2 的发布者不一定是 Raft 的领导者。

### 应用数据内容

应用程序内容为 UTF-8 编码的 [JSON](https://www.json.org/)，以简单性和可扩展性为目标。完整规范尚未制定。目标是提供足够的数据来编写算法以确定发布 Meta LS2 的“最佳”路由器，以及发布者拥有足够的信息来对 Meta LS2 中的目的地进行加权。数据将包含路由器和目的地的统计信息。

数据可能会在第一版中选配性地包含其他服务器的健康远距感应数据，以及获取 Meta LS 的能力。这些数据在第一个版本中不会支持。

数据可能会在第一版中选配性地包含由管理员客户端发布的配置信息。这些数据在第一个版本中不会支持。

如果“name: value”被列出，则指定了 JSON map 的键和值。否则，规范尚未制定。

集群数据（顶层）：

- cluster: 集群名称
- date: 此数据的日期（长整型，自纪元以来的毫秒数）
- id: Raft ID（整数）

配置数据（config）：

- 任何配置参数

MetaLS 发布状态（meta）：

- destination: metals 目的地，base64 编码
- lastPublishedLS: 如果存在，为上次发布的 metals 的 base64 编码
- lastPublishedTime: 以毫秒计，或从未为 0
- publishConfig: 发布者配置状态，关闭/开启/自动
- publishing: metals 发布者状态布尔值 true/false

路由器数据（router）：

- lastPublishedRI: 如果存在，则是最后发布的路由器信息的 base64 编码
- uptime: 在线时间，以毫秒计
- 任务滞后
- 探索隧道
- 参与隧道
- 配置带宽
- 当前带宽

目的地（destinations）：
列表

目的地数据：

- destination: 目的地，base64 编码
- uptime: 在线时间，以毫秒计
- 配置隧道
- 当前隧道
- 配置带宽
- 当前带宽
- 配置连接
- 当前连接
- 黑名单数据

远程路由器感应数据：

- 上次看到的 RI 版本
- LS 获取时间
- 连接测试数据
- 最接近的洪泛填充配置文件数据
  为了昨天、今天和明天的时间段

远程目的地感应数据：

- 上次看到的 LS 版本
- LS 获取时间
- 连接测试数据
- 最接近的洪泛填充配置文件数据
  为了昨天、今天和明天的时间段

Meta LS 感应数据：

- 上次看到的版本
- 获取时间
- 最接近的洪泛填充配置文件数据
  为了昨天、今天和明天的时间段

## 管理接口

待定，可能是一个单独的提案。不需要在第一个版本中提供。

管理接口的要求：

- 支持多个主控目的地，即多个虚拟集群（农场）
- 提供共享集群状态的综合视图 - 所有成员发布的统计信息、当前的领导者是谁等
- 能够强制从集群中移除一个参与者或领导者
- 能够强制发布 metaLS（如果当前节点是发布者）
- 能够将散列排除在 metaLS 之外（如果当前节点是发布者）
- 配置导入/导出功能以进行批量部署

## 路由器接口

待定，可能是一个单独的提案。i2pcontrol 在第一个版本中不是必需的，详细更改将在单独提案中包括。

Garlic Farm 到路由器 API 的要求（在 JVM Java 中或 i2pcontrol）

- getLocalRouterStatus()
- getLocalLeafHash(Hash masterHash)
- getLocalLeafStatus(Hash leaf)
- getRemoteMeasuredStatus(Hash masterOrLeaf) // 可能不在 MVP 中
- publishMetaLS(Hash masterHash, List<MetaLease> contents) // 或签名的 MetaLeaseSet？谁签名？
- stopPublishingMetaLS(Hash masterHash)
- 身份验证待定？

## 理由

Atomix 体积太大，不允许我们自定义从而通过 I2P 路由协议。而且，它的线格式是未记录的，并依赖于 Java 序列化。

## 备注

无。

## 问题

- 客户端没有办法发现和连接到未知领导者。对一个跟随者来说，在 AppendEntriesResponse 中作为日志条目发送配置将是一个微小的改变。

## 迁移

无向后兼容性问题。

## 参考文献

* [JRAFT](https://github.com/datatechnology/jraft)
* [JSON](https://json.org/)
* [RAFT](https://ramcloud.stanford.edu/wiki/download/attachments/11370504/raft.pdf)
* [RFC-2616](https://tools.ietf.org/html/rfc2616)
* [RFC-2617](https://tools.ietf.org/html/rfc2617)
* [WEBSOCKET](https://en.wikipedia.org/wiki/WebSocket)
