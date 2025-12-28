---
title: "Datagram2 协议"
number: "163"
author: "zzz, orignal, drzed, eyedeekay"
created: "2023-01-24"
lastupdated: "2025-04-16"
status: "Closed"
thread: "http://zzz.i2p/topics/3540"
target: "0.9.66"
toc: true
---

## 状态

于2025-04-15审核批准。
更改已纳入规范。
自 API 0.9.66 起在 Java I2P 中实现。
查看实现文档了解状态。


## 概述

从 [Prop123](/proposals/123-new-netdb-entries/) 中单独提取为一个独立提案。

离线签名无法在可回复数据报处理中验证。
需要一个标志来指示离线签名，但没有地方放置标志。

将需要一个全新的 I2CP协议号和格式，
将其添加到 [DATAGRAMS](/docs/api/datagrams/) 规范中。
我们称之为"Datagram2"。


## 目标

- 增加对离线签名的支持
- 增加重播抵抗
- 增加无签名的风味
- 添加标志和选项字段以供扩展


## 非目标

全面的端到端协议支持拥塞控制等。
那将建立在 Datagram2 之上，或作为其替代品，它是一个低级协议。
在 Datagram2 的基础上设计一个高性能协议没有意义，
因为来自字段和签名的开销。
任何此类协议应首先使用 Datagram2 进行初始握手，然后
切换到 RAW 数据报。


## 动机

自2019年其他地方完成的 LS2 工作后遗留。

预计首个使用 Datagram2 的应用程序将是
bittorrent UDP 通告，已在 i2psnark 和 zzzot 中实现，
详见 [Prop160](/proposals/160-udp-trackers/)。


## 可回复数据报规范

供参考，
以下是对可回复数据报规范的回顾，
从 [Datagrams](/docs/api/datagrams/) 中复制。
可回复数据报的标准 I2CP 协议号为 PROTO_DATAGRAM (17)。

```text
+----+----+----+----+----+----+----+----+
  | from                                  |
  +                                       +
  |                                       |
  ~                                       ~
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  |                                       |
  +----+----+----+----+----+----+----+----+
  | signature                             |
  +                                       +
  |                                       |
  +                                       +
  |                                       |
  +                                       +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  | payload...
  +----+----+----+----//


  from :: 一个 `Destination`
          长度: 387+ 字节
          数据报的发起者和签署者

  signature :: 一个 `Signature`
               签名类型必须与 $from 的公钥签名类型匹配
               长度: 40+ 字节，由签名类型暗示。
               对于默认的 DSA_SHA1 密钥类型：
                  SHA-256 哈希的 DSA `Signature`。
               对于其他密钥类型：
                  `Signature` 的有效负载。
               签名可通过 $from 的签名公钥验证。

  payload ::  数据
              长度: 0 到大约 31.5 KB（参见注释）

  总长度: 有效负载长度 + 423+
```


## 设计

- 定义新协议19 - 带选项的可回复数据报。
- 定义新协议20 - 无签名的可回复数据报。
- 添加标志字段用于离线签名和未来扩展
- 将签名移到有效负载之后以便于处理
- 新的签名规范不同于可回复数据报或流，因此
  如果解释为可回复数据报或流，签名验证将失败。
  这是通过将签名移到有效负载后实现的，
  并在签名函数中包含目标哈希。
- 为数据报添加重播预防，就像在 [Prop164](/proposals/164-streaming/) 中为流所做的那样。
- 添加任意选项部分
- 重用来自 [Common](/docs/specs/common-structures/) 和 [Streaming](/docs/specs/streaming/) 的离线签名格式。
- 离线签名部分必须位于变量长度之前
  有效负载和签名部分，因为它指定了签名的长度。


## 规范

### 协议

Datagram2 的新 I2CP 协议编号为19。
将其添加为 PROTO_DATAGRAM2 到 [I2CP](/docs/specs/i2cp/)。

Datagram3 的新 I2CP 协议编号为20。
将其添加为 PROTO_DATAGRAM2 到 [I2CP](/docs/specs/i2cp/)。


### Datagram2 格式

将 Datagram2 添加到 [DATAGRAMS](/docs/api/datagrams/) 作为如下所示：

```text
+----+----+----+----+----+----+----+----+
  |                                       |
  ~            from                       ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  flags  |     options (optional)      |
  +----+----+                             +
  ~                                       ~
  ~                                       ~
  +----+----+----+----+----+----+----+----+
  |                                       |
  ~     offline_signature (optional)      ~
  ~   expires, sigtype, pubkey, offsig    ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  ~            payload                    ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  ~            signature                  ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  from :: 一个 `Destination`
          长度: 387+ 字节
          数据报的发起者和（除非离线签名）签署者

  flags :: (2 字节)
           Bit 顺序: 15 14 ... 3 2 1 0
           Bits 3-0: 版本: 0x02 (0 0 1 0)
           Bit 4: 如果为0，则无选项；如果为1，则包含选项映射
           Bit 5: 如果为0，则无离线签名；如果为1 ，则离线签名
           Bits 15-6: 未使用，设置为0以便于将来使用

  options :: (如果存在则为2+ 字节)
           如果标志指示存在选项，一个 `Mapping`
           包含任意文本选项

  offline_signature ::
               如果标志指示离线密钥，则离线签名部分，
               如通用结构规范中指定的，
               具有以下4个字段。长度：根据在线和离线
               签名类型变化，通常102字节用于Ed25519
               此部分可以，也应该，离线生成。

    expires :: 过期时间戳
               (4字节，大端，秒自纪元以来，2106年溢出)

    sigtype :: 临时签名类型（2字节，大端）

    pubkey :: 临时签名公钥（长度由签名类型暗示），
              通常为Ed25519签名类型的32字节。

    offsig :: 一个 `Signature`
              签署到期时间戳、临时签名类型
              和公钥，由目的地公钥签署，
              长度：40+ 字节，由签名类型暗示，通常
              用于Ed25519签名类型的64字节。

  payload ::  数据
              长度: 0 到大约 61 KB（参见注释）

  signature :: 一个 `Signature`
               签名类型必须和 $from 的公钥类型相匹配
               （如果没有离线签名）或临时签名类型
               （如果是离线签名）
               长度：40+字节，由签名类型暗示，通常
               为Ed25519签名类型的64字节。
               `Signature` 对有效负载和其他字段的签名，如下所述。
               签名通过 $from 的签名公钥验证
               （如果没有离线签名）或临时公钥
               （如果是离线签名）

```

总长度：最小433 + 有效负载长度；
典型的X25519发送者且无离线签名情况下的长度：
457 + 有效负载长度。
注意，消息通常会在I2CP层使用gzip压缩，
如果来源地可压缩，会大大节省。

注意：离线签名格式与通用结构规范 [Common](/docs/specs/common-structures/) 和 [Streaming](/docs/specs/streaming/) 中相同。

### 签名

签名覆盖以下字段。

- 前置序列：目标目的地的32字节哈希（不包括在数据报中）
- 标志
- 选项（如果存在）
- 离线签名（如果存在）
- 有效负载

在可回复数据报中，对于 DSA_SHA1 密钥类型，签名是对
有效负载的 SHA-256 哈希，而不是对有效负载本身；在这里，签名始终是对上述字段（不是哈希）进行的，
无论密钥类型如何。


### ToHash 验证

接收者必须验证签名（使用他们的目标哈希）
并在失败时丢弃数据报，以防止重播。


### Datagram3 格式

将 Datagram3 添加到 [DATAGRAMS](/docs/api/datagrams/) 作为如下所示：

```text
+----+----+----+----+----+----+----+----+
  |                                       |
  ~            fromhash                   ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  flags  |     options (optional)      |
  +----+----+                             +
  ~                                       ~
  ~                                       ~
  +----+----+----+----+----+----+----+----+
  |                                       |
  ~            payload                    ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  fromhash :: 一个 `Hash`
              长度：32字节
              数据报的发起者

  flags :: (2 字节)
           Bit 顺序: 15 14 ... 3 2 1 0
           Bits 3-0: 版本: 0x03 (0 0 1 1)
           Bit 4: 如果为0，则无选项；如果为1，则包含选项映射
           Bits 15-5: 未使用，设置为0以保持与未来用途的兼容性

  options :: (如果存在则为2+ 字节)
           如果标志指示存在选项，一个 `Mapping`
           包含任意文本选项

  payload ::  数据
              长度: 0 到约 61 KB（参见注释）

```

总长度：最低34 + 有效负载长度。


### SAM

将 STYLE=DATAGRAM2 和 STYLE=DATAGRAM3 添加到 SAMv3 规范。
更新关于离线签名的信息。


### 开销

此设计为可回复数据报增加了2字节的开销以用于标志。
这是可以接受的。


## 安全分析

在签名中包含目标哈希应该能够有效地防止重播攻击。

Datagram3 格式缺乏签名，因此无法验证发送者，
并可能发生重播攻击。任何所需的验证必须在应用程序层完成，
或者由路由器在棘轮层完成。


## 备注

- 实际长度受到协议的底层限制 - 隧道
  消息规范 [TUNMSG](/docs/specs/tunnel-message/#notes) 将消息限制在约 61.2 KB，而传输
  [TRANSPORT](/docs/transport/) 当前将消息限制在约 64 KB，因此这里的数据长度限制为约 61 KB。
- 见关于大数据报可靠性的相关重要注释 [API](/docs/api/datagrams/)。为了
  获得最佳效果，将有效负载限制在约 10 KB 或更少。


## 兼容性

无。应用程序必须被重写以根据协议和/或端口路由 Datagram2 I2CP 消息。
错误路由为可回复数据报或流消息的 Datagram2 消息将基于签名、格式或两者失败。


## 迁移

每个 UDP 应用程序必须单独检测支持并迁移。
最突出的 UDP 应用程序是 bittorrent。

### Bittorrent

Bittorrent DHT: 可能需要扩展标志，
例如 i2p_dg2，与 BiglyBT 协调

Bittorrent UDP 通告 [Prop160](/proposals/160-udp-trackers/)：从一开始就设计。
与 BiglyBT、i2psnark、zzzot 协调

### 其他

Bote：不太可能迁移，未积极维护

Streamr：没有人在使用它，没有计划迁移

SAM UDP 应用：未知


## 参考

* [API](/docs/api/datagrams/)
* [BT-SPEC](/docs/applications/bittorrent/)
* [Common](/docs/specs/common-structures/)
* [DATAGRAMS](/docs/api/datagrams/)
* [I2CP](/docs/specs/i2cp/)
* [Prop123](/proposals/123-new-netdb-entries/)
* [Prop160](/proposals/160-udp-trackers/)
* [Prop164](/proposals/164-streaming/)
* [Streaming](/docs/specs/streaming/)
* [TRANSPORT](/docs/transport/)
* [TUNMSG](/docs/specs/tunnel-message/#notes)
