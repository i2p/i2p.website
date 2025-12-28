---
title: "UDP BitTorrent 通告请求"
description: "I2P 中的基于 UDP 的 BitTorrent 跟踪器 announce（上报请求）协议规范"
slug: "udp-announces"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## 概述

本规范记录了 I2P 中用于 UDP BitTorrent announce（向跟踪器的通告/查询）的协议。有关 I2P 中 BitTorrent 的整体规范，请参见 [I2P 上的 BitTorrent 文档](/docs/applications/bittorrent/)。有关本规范制定的背景和更多信息，请参见 [提案 160](/proposals/160-udp-trackers/)。

该协议已于 2025 年 6 月 24 日正式批准，并在 I2P 2.10.0 版本（API 0.9.67）中实现，发布于 2025 年 9 月 8 日。I2P 网络目前已启用对 UDP 跟踪器的支持，已有多个生产环境的跟踪器，并提供对 i2psnark 客户端的完整支持。

## 设计

本规范使用 repliable datagram2、repliable datagram3，以及 raw datagrams（原始数据报），其定义见[I2P 数据报规范](/docs/api/datagrams/)。Datagram2 和 Datagram3 是 repliable datagrams（可回复数据报）的变体，定义见[提案 163](/proposals/163-datagram2/)。Datagram2 增加了抗重放能力和对离线签名的支持。Datagram3 比旧的数据报格式更小，但不提供认证。

### BEP 15

供参考，[BEP 15](http://www.bittorrent.org/beps/bep_0015.html) 中定义的消息流程如下：

```
Client                        Tracker
  Connect Req. ------------->
    <-------------- Connect Resp.
  Announce Req. ------------->
    <-------------- Announce Resp.
  Announce Req. ------------->
    <-------------- Announce Resp.
```
连接阶段是为防止 IP 地址欺骗所必需的。tracker（追踪器）会返回一个连接 ID，客户端会在后续的 announce 请求中使用它。该连接 ID 在客户端默认 1 分钟后过期，而在 tracker 端为 2 分钟。

I2P 采用与 BEP 15 相同的消息流，这样做是为了便于现有具备 UDP 能力的客户端代码库采用、提高效率，以及出于下文将讨论的安全性考虑：

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
这相较于通过流式（TCP）的通告，潜在地可带来显著的带宽节省。虽然 Datagram2（数据报类型 2）的大小与一个流式 SYN 大致相当，但其原始响应要比流式的 SYN ACK 小得多。后续请求使用 Datagram3（数据报类型 3），而后续响应为原始。

announce 请求使用 Datagram3（I2P 的第3版数据报协议），因此跟踪器无需维护一个将连接ID映射到 announce 目的地或哈希的大型映射表。相反，跟踪器可以基于发送者哈希、当前时间戳（以某个时间间隔为基准）以及一个秘密值，以密码学方式生成连接ID。当收到 announce 请求时，跟踪器会验证该连接ID，然后将 Datagram3 的发送者哈希作为发送目标。

### 连接生命周期

[BEP 15](http://www.bittorrent.org/beps/bep_0015.html) 规定：在客户端侧，连接 ID 的有效期为一分钟；在追踪器侧为两分钟。该设置不可配置。除非客户端将 announce（向追踪器的通告请求）进行批处理，在一分钟的时间窗口内全部完成，否则这会限制潜在的效率提升。i2psnark 目前不会批量发送 announce；为避免流量突发，它会将它们分散开来。据报道，资深用户会同时运行上千个种子，将如此多的 announce 在一分钟内集中发送并不现实。

在此，我们建议对连接响应进行扩展，添加一个可选的连接生存期字段。默认情况下（若未提供），为一分钟。否则，客户端将使用以秒为单位指定的生存期，而跟踪器会将该连接 ID 额外保留一分钟。

### 与 BEP 15 的兼容性

该设计尽可能保持与 [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) 的兼容性，以尽量减少对现有客户端和跟踪器所需的更改。

唯一必需的更改是 announce 响应中对等节点信息的格式。connect 响应中添加 lifetime 字段并非必需，但如上所述，出于效率考虑，强烈建议这样做。

### 安全性分析

UDP 通告协议的一个重要目标是防止地址伪造。客户端必须真实存在，并携带一个真实的 leaseSet。它必须具有入站 tunnel，才能接收连接响应（Connect Response）。这些 tunnel 可以是 zero-hop（零跳）并可即时建立，但那会暴露创建者。该协议实现了这一目标。

### 问题

该协议尚不支持 blinded destinations（盲化目的地），但可以通过扩展来实现。详见下文。

## 规范

### 协议与端口

可回复的 Datagram2 使用 I2CP 协议 19；可回复的 Datagram3 使用 I2CP 协议 20；原始数据报使用 I2CP 协议 18。请求可以是 Datagram2 或 Datagram3。响应始终为原始数据报。较旧的可回复数据报（“Datagram1”）格式使用 I2CP 协议 17，绝不能用于请求或回复；如果在请求/回复端口上收到，必须予以丢弃。注意：Datagram1 的 I2CP 协议 17 仍用于 DHT（分布式哈希表）协议。

请求使用来自 announce URL 的 I2CP "to port"；见下文。请求的 "from port" 由客户端选择，但应为非零，并且与 DHT（分布式哈希表）使用的端口不同，以便可轻松对响应进行分类。Tracker 应拒绝在错误端口收到的请求。

响应会使用请求中的 I2CP "to port"（目标端口）。响应的 "from port"（源端口）是该请求的 "to port"。

### 通告 URL

announce URL（Tracker 公告 URL）格式未在 [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) 中规定，但与明网一样，UDP announce URLs 的形式为 "udp://host:port/path"。路径会被忽略，可以为空，但在明网上通常为 "/announce"。:port 部分应当始终存在；不过，如果省略了":port"部分，则使用默认的 I2CP 端口 6969，因为那是明网上常用的端口。也可能附加 CGI 参数 &a=b&c=d；这些参数可以被处理并包含在 announce 请求中，参见 [BEP 41](http://www.bittorrent.org/beps/bep_0041.html)。如果没有参数或路径，结尾的 / 也可以省略，[BEP 41](http://www.bittorrent.org/beps/bep_0041.html) 中亦有此意。

### 数据报格式

所有数值均按网络字节序（大端序）发送。不要指望数据包的大小恰好等于某个固定值。未来的扩展可能会增大数据包的大小。

#### 连接请求

客户端发往 tracker。16 字节。必须为可回复的 Datagram2（I2P 数据报第2版）。与 [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) 相同。无更改。

```
Offset  Size            Name            Value
0       64-bit integer  protocol_id     0x41727101980 // magic constant
8       32-bit integer  action          0 // connect
12      32-bit integer  transaction_id
```
#### 连接响应

Tracker 到客户端。16 或 18 字节。必须为原始数据。与 [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) 中相同，除非下文另有说明。

```
Offset  Size            Name            Value
0       32-bit integer  action          0 // connect
4       32-bit integer  transaction_id
8       64-bit integer  connection_id
16      16-bit integer  lifetime        optional  // Change from BEP 15
```
响应必须发送到 I2CP "to port"（目标端口），该端口为请求中接收到的 "from port"（来源端口）。

lifetime 字段是可选的，用于指示客户端的 connection_id 生命周期（单位为秒）。默认值为 60；如果指定，最小值也是 60。最大值为 65535（约 18 小时）。追踪器应将 connection_id 的维持时间设定为比客户端生命周期多 60 秒。

#### 通告请求

客户端到追踪器。至少 98 字节。必须为可回复的 Datagram3（I2P 的第三版数据报格式）。除下文另有说明外，与 [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) 相同。

connection_id 为在 connect response 中接收到的值。

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
84      32-bit integer  IP address      0     // default, unused in I2P
88      32-bit integer  key
92      32-bit integer  num_want        -1    // default
96      16-bit integer  port                  // must be same as I2CP from port
98      varies          options     optional  // As specified in BEP 41
```
相对于 [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) 的更改:

- key 被忽略
- IP 地址未使用
- 端口可能会被忽略，但必须与 I2CP from port 相同
- 如果存在，选项部分按 [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) 的定义

必须将响应发送到 I2CP 的 "to port"，该端口是作为请求的 "from port" 收到的。不要使用 announce request 中的端口。

#### 通告响应

从跟踪器到客户端。至少 20 字节。必须为原始数据。除下文注明的差异外，与 [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) 中相同。

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
与 [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) 相比的更改：

- 我们不使用 6 字节的 IPv4+port 或 18 字节的 IPv6+port，而是返回若干个 32 字节的 "compact responses"（紧凑响应），其中包含 SHA-256 二进制对等节点哈希值。与 TCP compact responses 类似，我们不包含端口号。

响应必须发送到 I2CP 的 "to port"，其值等于该请求的 "from port"。不要使用 announce 请求（公告请求）中的端口。

I2P 数据报的最大尺寸约为 64 KB；然而，若需可靠传输，应避免使用超过 4 KB 的数据报。为提高带宽效率，跟踪器应将最大对等节点数限制在约 50，这对应于在各层开销之前约 1600 字节的数据包，并且在分片后应能控制在两条 tunnel 消息的有效载荷上限之内。

与 BEP 15（BitTorrent 增强提案第 15 号）一样，不包含后续对等节点地址数量的计数（BEP 15 中为 IP/端口，此处为哈希）。尽管 BEP 15 未考虑这一点，但可以定义一个全零的对等节点结束标记，以指示对等节点信息已完整，随后将跟随一些扩展数据。

为了将来能够进行这种扩展，客户端应忽略一个 32 字节的全零哈希以及其后的任何数据。追踪器应当拒绝来自全零哈希的 announce 请求，尽管该哈希已被 Java routers 禁止。

#### 抓取

来自 [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) 的 scrape 请求/响应并非本规范所必需，但如有需要可以实现，无需任何修改。客户端必须先获取一个 connection ID。scrape 请求一律使用可回复的 Datagram3（I2P 的第3版数据报格式）。scrape 响应一律为 raw（原始数据报）。

#### 错误响应

从 Tracker 到客户端。最少 8 字节（当消息为空时）。必须是原始格式。与 [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) 中相同。无更改。

```
Offset  Size            Name            Value
0       32-bit integer  action          3 // error
4       32-bit integer  transaction_id
8       string          message
```
## 扩展

不包含扩展位或版本字段。客户端和跟踪器不应假定数据包具有某个固定大小。这样，就可以在不破坏兼容性的情况下添加额外字段。如有需要，建议使用 [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) 中定义的扩展格式。

连接响应已被修改，新增可选的连接ID有效期。

如果需要支持 blinded destination（对目标地址进行盲化的机制），我们可以选择：要么在 announce 请求的末尾附加 blinded 的 35 字节地址，要么在响应中请求以 [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) 格式（参数待定）返回 blinded 哈希。可以在一个全零的 32 字节哈希之后，将一组 blinded 的 35 字节 peer 地址添加到 announce 应答的末尾。

## 实现指南

有关未集成、非 I2CP 客户端和跟踪器所面临挑战的讨论，请参阅上面的设计部分。

### 客户端

对于给定的跟踪器主机名，客户端应优先使用 UDP 而不是 HTTP URL，并且不应同时向两者发送 announce 请求（向跟踪器通告自身状态的请求）。

已经支持 BEP 15（BitTorrent 增强提案第 15 号）的客户端应只需进行少量修改。

如果客户端支持 DHT（分布式哈希表）或其他数据报协议，最好为请求选择一个不同的 "from port"（源端口），以便回复回到该端口，并且不会与 DHT 消息混淆。客户端只会以原始数据报的形式接收回复。跟踪器永远不会向客户端发送可回复的 datagram2。

具有默认开放追踪器列表的客户端，应在确认哪些已知开放追踪器支持 UDP 之后，更新该列表以添加 UDP URL。

客户端可以选择是否实现请求的重传。若实现了重传，初始超时时间应至少为 15 秒，并在每次重传时将超时时间加倍（指数退避）。

客户端在收到错误响应后必须退避。

### 追踪器

已支持 BEP 15（BitTorrent 增强提案 15）的跟踪器只需要进行少量修改。本规范与 2014 年的提案不同之处在于：跟踪器必须在同一端口上支持接收可回复的 datagram2（第二版数据报）和 datagram3（第三版数据报）。

为将跟踪器的资源需求降到最低，本协议旨在消除对跟踪器的任何要求，即为后续验证而存储客户端哈希与连接ID之间的映射关系。之所以可行，是因为 announce 请求数据包是可回复的 Datagram3（数据报协议第3版）数据包，因此其中包含发送方的哈希。

推荐的实现是：

- 将当前 epoch（纪元）定义为以连接生命周期为分辨率的当前时间，`epoch = now / lifetime`。
- 定义一个密码学哈希函数 `H(secret, clienthash, epoch)`，其生成 8 字节输出。
- 生成一个用于所有连接的随机常量 secret（秘密值）。
- 对于连接响应，生成 `connection_id = H(secret, clienthash, epoch)`。
- 对于公告请求，在当前 epoch 中通过验证 `connection_id == H(secret, clienthash, epoch) || connection_id == H(secret, clienthash, epoch - 1)` 来校验接收到的连接ID。

## 部署状态

该协议已于2025年6月24日获批准，并自2025年9月起在 I2P 网络上全面投入运行。

### 当前实现

**i2psnark**: I2P 2.10.0 版本（API 0.9.67）包含对 UDP tracker（UDP 追踪器）的完整支持，发布于 2025 年 9 月 8 日。自该版本起，所有 I2P 安装默认包含 UDP tracker 功能。

**zzzot tracker**: 0.20.0-beta2 及更高版本支持 UDP announce（通过 UDP 向跟踪器汇报的请求）。截至 2025 年 10 月，以下生产环境的跟踪器正在运行: - opentracker.dg2.i2p - opentracker.simp.i2p - opentracker.skank.i2p

### 客户端兼容性说明

**SAM v3.3 限制**：使用 SAM（Simple Anonymous Messaging）的外部 BitTorrent 客户端需要 SAM v3.3 对 Datagram2/3（SAM 协议中的第二/第三代无连接数据报扩展）的支持。Java I2P 已提供该支持，但 i2pd（C++ 的 I2P 实现）目前尚不支持，这可能会限制其在基于 libtorrent 的客户端（如 qBittorrent）中的采用。

**I2CP 客户端**: 直接使用 I2CP 的客户端（例如 BiglyBT）可以在不受 SAM 限制的情况下实现对 UDP 追踪器的支持。

## 参考资料

- **[BEP15]**: [BitTorrent UDP 跟踪器协议](http://www.bittorrent.org/beps/bep_0015.html)
- **[BEP41]**: [UDP 跟踪器协议扩展](http://www.bittorrent.org/beps/bep_0041.html)
- **[DATAGRAMS]**: [I2P 数据报规范](/docs/api/datagrams/)
- **[Prop160]**: [UDP 跟踪器提案](/proposals/160-udp-trackers/)
- **[Prop163]**: [Datagram2 提案](/proposals/163-datagram2/)
- **[SPEC]**: [I2P 上的 BitTorrent](/docs/applications/bittorrent/)
