---
title: "UDP Trackers"
number: "160"
author: "zzz"
created: "2022-01-03"
lastupdated: "2025-06-25"
status: "已关闭"
thread: "http://zzz.i2p/topics/1634"
target: "0.9.67"
toc: true
---

## 状态

已于 2025-06-24 审查通过。规范文档位于 [UDP specification](/docs/specs/udp-bittorrent-announces/)。已在 zzzot 0.20.0-beta2 中实现。已在 i2psnark 中实现，自 API 0.9.67 版本起。请查看其他实现的文档了解状态。

## 概述

该提案是关于在 I2P 中实现 UDP tracker 的。

### Change History

一个关于在 I2P 中使用 UDP tracker 的初步提案于 2014 年 5 月发布在我们的 [bittorrent 规范页面](/docs/applications/bittorrent/) 上；这早于我们正式的提案流程，且从未实施。本提案创建于 2022 年初，简化了 2014 年版本。

由于此提案依赖于可回复的数据报，当我们在2023年初开始研究[Datagram2 提案](/proposals/163-datagram2/)时，该提案被暂停。该提案于2025年4月获得批准。

该提案的 2023 版本指定了两种模式："兼容性"和"快速"。进一步分析显示快速模式将是不安全的，并且对于拥有大量种子文件的客户端也会效率低下。此外，BiglyBT 表示偏好兼容性模式。对于任何支持标准 [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) 的 tracker 或客户端来说，这种模式将更容易实现。

虽然兼容模式在客户端从零开始实现起来更加复杂，但我们确实有从2023年开始的初步代码。

因此，这里的当前版本进一步简化，移除了快速模式，并删除了"兼容性"这一术语。当前版本切换到新的 Datagram2 格式，并添加了对 UDP 公告扩展协议 [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) 的引用。

此外，连接响应中还添加了连接 ID 生存期字段，以扩展此协议的效率收益。

## Motivation

随着用户基数的总体增长以及 bittorrent 用户数量的持续增加，我们需要让 tracker 和公告更加高效，以免 tracker 不堪重负。

Bittorrent 在 2008 年的 BEP 15 [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) 中提出了 UDP tracker，现在明网上的绝大多数 tracker 都是仅支持 UDP 的。

很难计算数据报与流协议的带宽节省量。可回复请求的大小与流 SYN 大致相同，但有效载荷约小 500 字节，因为 HTTP GET 有一个巨大的 600 字节 URL 参数字符串。原始回复比流 SYN ACK 要小得多，为 tracker 的出站流量提供了显著减少。

此外，还应该有特定于实现的内存减少，因为数据报比流连接需要的内存状态要少得多。

如[/proposals/169-pq-crypto/](/proposals/169-pq-crypto/)中所设想的后量子加密和签名将大幅增加加密和签名结构的开销，包括destinations、leasesets、streaming SYN和SYN ACK。在I2P采用PQ加密之前，尽可能减少这些开销非常重要。

## 动机

此提案使用可回复数据报2、可回复数据报3和原始数据报，如[/docs/api/datagrams/](/docs/api/datagrams/)中所定义。数据报2和数据报3是可回复数据报的新变体，在提案163 [/proposals/163-datagram2/](/proposals/163-datagram2/)中定义。数据报2添加了重放抵抗和离线签名支持。数据报3比旧的数据报格式更小，但没有身份验证。

### BEP 15

作为参考，[BEP 15](http://www.bittorrent.org/beps/bep_0015.html) 中定义的消息流程如下：

```
Client                        Tracker
    Connect Req. ------------->
      <-------------- Connect Resp.
    Announce Req. ------------->
      <-------------- Announce Resp.
    Announce Req. ------------->
      <-------------- Announce Resp.
```
连接阶段是防止IP地址欺骗所必需的。tracker返回一个连接ID，客户端在后续的通告中使用该ID。这个连接ID在客户端默认一分钟后过期，在tracker上默认两分钟后过期。

I2P 将使用与 BEP 15 相同的消息流，以便在现有支持 UDP 的客户端代码库中易于采用：为了效率，以及出于下面讨论的安全原因：

```
Client                        Tracker
    Connect Req. ------------->       (Repliable Datagram2)
      <-------------- Connect Resp.   (Raw)
    Announce Req. ------------->      (Repliable Datagram3)
      <-------------- Announce Resp.  (Raw)
    Announce Req. ------------->      (Repliable Datagram3)
      <-------------- Announce Resp.  (Raw)
             ...
```
这相比流式传输 (TCP) 公告可能节省大量带宽。虽然 Datagram2 与流式传输 SYN 的大小大致相同，但原始响应比流式传输 SYN ACK 要小得多。后续请求使用 Datagram3，后续响应为原始格式。

announce请求使用Datagram3，这样tracker就无需维护一个从连接ID到announce目标或哈希值的大型映射表。相反，tracker可以通过发送方哈希值、当前时间戳（基于某个时间间隔）和一个秘密值来加密生成连接ID。当收到announce请求时，tracker验证连接ID，然后使用Datagram3发送方哈希值作为发送目标。

### 变更历史

对于集成应用程序（router和客户端在一个进程中，例如i2psnark和ZzzOT Java插件），或基于I2CP的应用程序（例如BiglyBT），实现和单独路由流式传输和数据报流量应该是直接的。预计ZzzOT和i2psnark将成为首批实现此提案的tracker和客户端。

下面将讨论非集成式 tracker 和客户端。

#### Trackers

目前已知有四种I2P tracker实现：

- zzzot，一个集成的 Java router 插件，运行在 opentracker.dg2.i2p 和其他几个地址
- tracker2.postman.i2p，推测运行在 Java router 和 HTTP Server tunnel 后面
- 旧版 C opentracker，由 zzz 移植，UDP 支持已注释掉
- 新版 C opentracker，由 r4sas 移植，运行在 opentracker.r4sas.i2p 和可能的其他地址，
  推测运行在 i2pd router 和 HTTP Server tunnel 后面

对于当前使用HTTP服务器tunnel来接收announce请求的外部tracker应用程序，实现可能会相当困难。可以开发一个专门的tunnel来将数据报转换为本地HTTP请求/响应。或者，可以设计一个既处理HTTP请求又处理数据报的专门tunnel，将数据报转发给外部进程。这些设计决策将很大程度上取决于具体的router和tracker实现，超出了本提案的范围。

#### Clients

基于SAM的外部torrent客户端（如qbittorrent和其他基于libtorrent的客户端）需要[SAM v3.3](/docs/api/samv3/)，但i2pd不支持此版本。DHT支持也需要此版本，而且实现复杂到目前没有已知的SAM torrent客户端实现了它。预计短期内不会有基于SAM的此提案实现。

### Connection Lifetime

[BEP 15](http://www.bittorrent.org/beps/bep_0015.html) 规定连接 ID 在客户端一分钟后过期，在 tracker 两分钟后过期。这是不可配置的。这限制了潜在的效率提升，除非客户端批量处理公告以在一分钟窗口内完成所有操作。i2psnark 目前不批量处理公告；它将公告分散开来，以避免流量突发。据报告，高级用户同时运行数千个 torrent，将如此多的公告在一分钟内突发是不现实的。

在这里，我们建议扩展连接响应以添加一个可选的连接生存期字段。如果不存在，默认值为一分钟。否则，客户端应使用以秒为单位指定的生存期，tracker 将多维护连接 ID 一分钟。

### Compatibility with BEP 15

此设计尽可能保持与 [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) 的兼容性，以限制现有客户端和tracker所需的更改。

唯一必需的更改是在宣告响应中对等节点信息的格式。在连接响应中添加生存时间字段不是必需的，但强烈建议添加以提高效率，如上所述。

### BEP 15

UDP 宣告协议的一个重要目标是防止地址欺骗。客户端必须真实存在并捆绑一个真实的 leaseSet。它必须具有入站 tunnel 来接收连接响应。这些 tunnel 可以是零跳并立即构建，但这会暴露创建者。该协议实现了这一目标。

### Tracker/Client 支持

- 此提案不支持盲化目标地址，
  但可能会扩展以支持此功能。见下文。

## 设计

### Protocols and Ports

Repliable Datagram2 使用 I2CP 协议 19；repliable Datagram3 使用 I2CP 协议 20；原始数据报使用 I2CP 协议 18。请求可以是 Datagram2 或 Datagram3。响应始终是原始格式。使用 I2CP 协议 17 的旧版 repliable datagram（"Datagram1"）格式不得用于请求或回复；如果在请求/回复端口上收到这些数据，必须丢弃。请注意，Datagram1 协议 17 仍用于 DHT 协议。

请求使用来自公告URL的I2CP "to port"；见下文。请求"from port"由客户端选择，但应为非零值，且与DHT使用的端口不同，以便响应可以轻松分类。Tracker应拒绝在错误端口上接收到的请求。

响应使用请求中的 I2CP "to port"。请求的 "from port" 是请求中的 "to port"。

### Announce URL

虽然[BEP 15](http://www.bittorrent.org/beps/bep_0015.html)中没有指定announce URL格式，但与明网一样，UDP announce URL的格式为"udp://host:port/path"。路径会被忽略，可以为空，但在明网上通常是"/announce"。:port部分应该始终存在，但是如果省略了":port"部分，则使用默认的I2CP端口6969，因为这是明网上的常用端口。还可能会附加cgi参数&a=b&c=d，这些参数可能会被处理并在announce请求中提供，请参见[BEP 41](http://www.bittorrent.org/beps/bep_0041.html)。如果没有参数或路径，也可以省略尾随的/，如[BEP 41](http://www.bittorrent.org/beps/bep_0041.html)中所暗示的。

### 连接生命周期

所有值都以网络字节顺序（大端序）发送。不要期望数据包具有确切的特定大小。未来的扩展可能会增加数据包的大小。

#### Connect Request

客户端到 tracker。16 字节。必须是可回复的 Datagram2。与 [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) 中的相同。无变化。

```
Offset  Size            Name            Value
  0       64-bit integer  protocol_id     0x41727101980 // magic constant
  8       32-bit integer  action          0 // connect
  12      32-bit integer  transaction_id
```
#### Connect Response

Tracker 到客户端。16 或 18 字节。必须是原始数据。与 [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) 相同，除了以下注明的部分。

```
Offset  Size            Name            Value
  0       32-bit integer  action          0 // connect
  4       32-bit integer  transaction_id
  8       64-bit integer  connection_id
  16      16-bit integer  lifetime        optional  // Change from BEP 15
```
响应必须发送到I2CP的"to port"，该端口是作为请求的"from port"接收到的。

lifetime 字段是可选的，表示 connection_id 客户端生存时间，以秒为单位。默认值是 60，如果指定的话最小值是 60。最大值是 65535 或大约 18 小时。tracker 应该维护 connection_id 的时间比客户端生存时间多 60 秒。

#### Announce Request

客户端到 tracker。最少 98 字节。必须是可回复的 Datagram3。与 [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) 相同，除了下面注明的部分。

connection_id 是在连接响应中接收到的。

```
Offset  Size            Name            Value
  0       64-bit integer  connection_id
  8       32-bit integer  action          1     // announce
  12      32-bit integer  transaction_id
  16      20-byte string  info_hash
  36      20-byte string  peer_id
  56      64-bit integer  downloaded
  64      64-bit integer  left
  72      64-bit integer  uploaded
  80      32-bit integer  event           0     // 0: none; 1: completed; 2: started; 3: stopped
  84      32-bit integer  IP address      0     // default
  88      32-bit integer  key
  92      32-bit integer  num_want        -1    // default
  96      16-bit integer  port
  98      varies          options     optional  // As specified in BEP 41
```
与 [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) 的变更：

- key 被忽略
- port 可能被忽略
- options 部分（如果存在）按 [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) 中的定义

响应必须发送到作为请求"from port"接收到的 I2CP "to port"。不要使用来自 announce 请求的端口。

#### Announce Response

Tracker 到客户端。最少 20 字节。必须是原始格式。与 [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) 相同，除了以下注明的内容。

```
Offset  Size            Name            Value
  0           32-bit integer  action          1 // announce
  4           32-bit integer  transaction_id
  8           32-bit integer  interval
  12          32-bit integer  leechers
  16          32-bit integer  seeders
  20   32 * n 32-byte hash    binary hashes     // Change from BEP 15
  ...                                           // Change from BEP 15
```
与 [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) 的变更：

- 我们返回32字节"紧凑响应"的倍数，包含SHA-256二进制对等节点哈希，而不是6字节IPv4+端口或18字节IPv6+端口。与TCP紧凑响应一样，我们不包含端口。

响应必须发送到从请求"发送端口"接收到的I2CP"目标端口"。不要使用来自announce请求的端口。

I2P 数据报有一个非常大的最大大小，约为 64 KB；然而，为了可靠传输，应避免使用大于 4 KB 的数据报。为了带宽效率，tracker 应该将最大对等节点数限制在大约 50 个，这对应于各层开销前约 1600 字节的数据包，并且应在分片后的双隧道消息负载限制内。

如在 BEP 15 中一样，没有包含后续对等节点地址数量的计数（BEP 15 中为 IP/端口，这里为哈希值）。虽然在 BEP 15 中未考虑，但可以定义一个全零的对等节点结束标记来表示对等节点信息已完整，后面跟着一些扩展数据。

为了让未来的扩展成为可能，客户端应该忽略32字节全零哈希值以及其后的任何数据。Tracker应该拒绝来自全零哈希值的通告，尽管该哈希值已经被Java router禁用。

#### Scrape

来自 [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) 的 Scrape 请求/响应并非本提议所必需，但如果需要可以实现，无需更改。客户端必须首先获取连接 ID。scrape 请求始终是可回复的 Datagram3。scrape 响应始终是原始格式。

#### 跟踪器

Tracker到客户端。最少8字节（如果消息为空）。必须是原始格式。与[BEP 15](http://www.bittorrent.org/beps/bep_0015.html)中相同。无变化。

```
Offset  Size            Name            Value
  0       32-bit integer  action          3 // error
  4       32-bit integer  transaction_id
  8       string          message
```
## Extensions

扩展位或版本字段未包含在内。客户端和tracker不应假设数据包具有特定大小。这样，可以在不破坏兼容性的情况下添加额外字段。如果需要，建议使用[BEP 41](http://www.bittorrent.org/beps/bep_0041.html)中定义的扩展格式。

连接响应被修改以添加可选的连接 ID 生存期。

如果需要 blinded destination 支持，我们可以将 blinded 35字节地址添加到通告请求的末尾，或者使用 [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) 格式在响应中请求 blinded 哈希（参数待定）。blinded 35字节对等地址集合可以在全零32字节哈希之后添加到通告回复的末尾。

## Implementation guidelines

有关非集成、非I2CP客户端和tracker面临的挑战的讨论，请参见上面的设计部分。

### 与 BEP 15 的兼容性

对于给定的 tracker 主机名，客户端应优先选择 UDP 而非 HTTP URL，并且不应同时向两者进行 announce。

支持现有 BEP 15 的客户端应该只需要进行少量修改。

如果客户端支持 DHT 或其他数据报协议，它应该选择一个不同的端口作为请求的"来源端口"，这样回复就会返回到那个端口，而不会与 DHT 消息混淆。客户端只接收原始数据报作为回复。Tracker 永远不会向客户端发送可回复的数据报2。

具有默认 opentracker 列表的客户端应在已知 opentracker 支持 UDP 后更新列表以添加 UDP URL。

客户端可以实现或不实现请求的重传。如果实现重传，应该使用至少 15 秒的初始超时，并且每次重传时将超时时间加倍（指数退避）。

客户端在收到错误响应后必须退避。

### 安全分析

支持现有 BEP 15 的 Tracker 应该只需要少量修改。这个提案与 2014 年的提案不同，tracker 必须支持在同一端口上接收可回复的 datagram2 和 datagram3。

为了最小化 tracker 资源需求，该协议的设计消除了 tracker 存储客户端哈希到连接 ID 映射以供后续验证的任何要求。这是可能的，因为宣告请求数据包是一个可回复的 Datagram3 数据包，所以它包含发送者的哈希值。

推荐的实现方式是：

- 将当前纪元定义为以连接生存期为分辨率的当前时间，
  ``epoch = now / lifetime``。
- 定义一个加密哈希函数 ``H(secret, clienthash, epoch)``，该函数生成
  8 字节输出。
- 生成用于所有连接的随机常量密钥。
- 对于连接响应，生成 ``connection_id = H(secret,  clienthash, epoch)``
- 对于通告请求，通过验证以下条件来验证当前纪元中接收到的连接 ID：
  ``connection_id == H(secret, clienthash, epoch) || connection_id == H(secret, clienthash, epoch - 1)``

## Migration

现有客户端不支持 UDP announce URL 并会忽略它们。

现有的 tracker 不支持接收可回复或原始数据报，这些数据报将被丢弃。

此提案完全是可选的。客户端和 tracker 都不需要在任何时候实现它。

## Rollout

首次实现预计将在 ZzzOT 和 i2psnark 中进行。它们将用于测试和验证此提案。

测试和验证完成后，将根据需要开发其他实现。
