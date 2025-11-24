---
title: "UDP跟踪器"
number: "160"
author: "zzz"
created: "2022-01-03"
lastupdated: "2025-06-25"
status: "Closed"
thread: "http://zzz.i2p/topics/1634"
target: "0.9.67"
---

## 状态

在2025-06-24的审查中获得批准。
规范在[UDP specification](/en/docs/spec/udp-bittorrent-announces/)。
实现于zzzot 0.20.0-beta2中。
在i2psnark中作为API 0.9.67实现。
检查其他实现的文档以获取状态。


## 概述

该提案是为I2P实现UDP跟踪器。


### 变更历史

I2P中UDP跟踪器的初步提案在我们的bittorrent规范页面[/en/docs/applications/bittorrent/](/en/docs/applications/bittorrent/)上发布于2014年5月；这早于我们的正式提案流程，并且从未被实现。
该提案于2022年初创建，简化了2014年的版本。

由于此提案依赖于可回复的数据报，当我们在2023年初开始致力于Datagram2提案[/en/proposals/163-datagram2/](/en/proposals/163-datagram2/)时被搁置。
该提案于2025年4月批准。

2023年的这个提案版本指定了两种模式，“兼容性”和“快速”。
进一步分析显示，快速模式将是不安全的，对于有大量种子的客户端也会效率低下。
此外，BiglyBT表示更倾向于兼容性模式。
这种模式对于支持标准[BEP 15](http://www.bittorrent.org/beps/bep_0015.html)的任何跟踪器或客户端来说将更容易实现。

虽然对于客户端侧从头开始实现兼容模式更为复杂，但我们确实在2023年开始了初步的代码。

因此，这里当前版本进一步简化以移除快速模式，并移除术语“兼容性”。 当前版本切换到新的Datagram2格式，并添加了对UDP宣布扩展协议[BEP 41](http://www.bittorrent.org/beps/bep_0041.html)的参考。

此外，在连接响应中添加了一个连接ID生命周期字段，以扩展该协议的效率增益。


## 动机

随着总体上用户基础和特定软件下载用户数量的不断增长，我们需要提高跟踪器和宣布的效率，以免跟踪器不堪重负。

Bittorrent在BEP 15 [BEP 15](http://www.bittorrent.org/beps/bep_0015.html)中于2008年提出了UDP跟踪器，现在绝大多数在清网中的跟踪器都是仅UDP的。

计算数据报与流协议的带宽节省是困难的。 一个可回复的请求与一个流式SYN差不多大小，但由于HTTP GET有一个巨大的600字节的URL参数字符串，载荷要小约500字节。
原始回复比流式SYN ACK要小得多，显著减少了跟踪器的出站流量。

此外，由于数据报需要的内存状态比流连接少得多，因此应该有特定实现的内存减少。

如[/en/proposals/169-pq-crypto/](/en/proposals/169-pq-crypto/)中设想的后量子加密和签名将大幅增加加密和签名结构（包括目的地、租约集、流式SYN和SYN ACK）的开销。 在I2P中采用PQ加密之前，尽量减少这种开销是很重要的。


## 设计

该提案使用可回复的数据报2、可回复的数据报3和原始数据报，如[/en/docs/spec/datagrams/](/en/docs/spec/datagrams/)中定义。
数据报2和数据报3是可回复的数据报的新变种，在提案163 [/en/proposals/163-datagram2/](/en/proposals/163-datagram2/)中定义。
数据报2增加了重放抵抗和离线签名支持。
数据报3比旧的数据报格式更小，但没有认证。


### BEP 15

在[BEP 15](http://www.bittorrent.org/beps/bep_0015.html)中定义的信息流参考如下：

```
客户端                        跟踪器
    连接请求 ------------->
      <-------------- 连接响应
    声明请求 -------------> 
      <-------------- 声明响应
    声明请求 ------------->
      <-------------- 声明响应
```

连接阶段是为了防止IP地址欺骗。
跟踪器返回一个连接ID，客户端在后续的声明中使用该ID。
默认情况下，该连接ID在客户端过期时间为一分钟，在跟踪器上为两分钟。

I2P将使用与BEP 15相同的信息流，以便在现有的支持UDP的客户端代码库中易于采用：
出于效率和下面讨论的安全原因：

```
客户端                        跟踪器
    连接请求 ------------->       (可回复数据报2)
      <-------------- 连接响应   (原始)
    声明请求 ------------->      (可回复数据报3)
      <-------------- 声明响应  (原始)
    声明请求 ------------->      (可回复数据报3)
      <-------------- 声明响应  (原始)
             ...
```

这潜在地通过流式（TCP）声明提供了大量的带宽节省。
虽然数据报2的大小与流式SYN相当，但原始响应比流式SYN ACK要小得多。
后续请求使用数据报3，后续响应为原始。

声明请求是数据报3，因此跟踪器无需维护大型映射表以标识连接ID和声明目的地或哈希。
相反，跟踪器可加密地从发送者哈希、当前时间戳（基于某个间隔）和一个密钥生成连接ID。
当接收到声明请求时，跟踪器验证连接ID，然后使用数据报3发送者哈希作为发送目标。


### 跟踪器/客户端支持

对于集成的应用程序（路由器和客户端在一个进程中，例如i2psnark和ZzzOT Java插件）或基于I2CP的应用程序（例如BiglyBT），应该很容易单独实现和路由流式和数据报流量。
预计ZzzOT和i2psnark会是该提案的第一个跟踪器和客户端实现。

非集成的跟踪器和客户端将在下文中讨论。


跟踪器
````````

已知有四种I2P跟踪器实现：

- zzzot，一个集成的Java路由器插件，在opentracker.dg2.i2p和其他几个地方运行
- tracker2.postman.i2p，可能在Java路由器和HTTP服务器隧道后面运行
- 旧版C opentracker，由zzz移植，注释掉了UDP支持
- 新版C opentracker，由r4sas移植，可能在opentracker.r4sas.i2p和其他地方运行，可能也在i2pd路由器和HTTP服务器隧道后面

对于目前使用HTTP服务器隧道接收声明请求的外部跟踪器应用程序，实现可能相当困难。
可以开发一个专用隧道来将数据报转换为本地HTTP请求/响应。
或者，可以设计一个能处理HTTP请求和数据报的专用隧道，该隧道会将数据报转发到外部进程。
这些设计决策在很大程度上取决于具体的路由器和跟踪器实现，并不在此提案的范围之内。


客户端
```````
如qBittorrent和其他libtorrent基础的外部SAM-based torrent客户端将需要SAM v3.3 [/en/docs/api/samv3/](/en/docs/api/samv3/)，这不被i2pd支持。
这也需要用于DHT支持，并且复杂度足以至今没有已知的SAM torrent客户端实现它。
预计近期没有该提案的SAM based实现。


### 连接生命周期

[BEP 15](http://www.bittorrent.org/beps/bep_0015.html)规定连接ID在客户端过期时间为一分钟，在跟踪器上为两分钟。
它是不可配置的。
这限制了潜在的效率增益，除非客户端批量宣布所有操作在一个一分钟窗口内完成。
i2psnark目前不进行批量宣布；它将它们分散开来，以避免流量高峰。
报告称高级用户一次可运行成千上万个种子，同时在一分钟内突然爆发那么多次宣布是不现实的。

在此，我们建议扩展连接响应以添加一个可选的连接生命周期字段。
如果未指定，则默认值为一分钟。否则，客户端应使用以秒为单位指定的生命周期，并且跟踪器将在客户端生命周期的基础上多保持一分钟的连接ID。


### 与BEP 15的兼容性

该设计尽可能保持与[BEP 15](http://www.bittorrent.org/beps/bep_0015.html)的兼容，以限制对现有客户端和跟踪器所需的更改。

唯一需要的更改是宣布响应中的对等信息格式。
为提高效率，强烈建议为连接响应中的生命周期字段添加，但不是必须的，如上所述。



### 安全分析

UDP宣布协议的重要目标之一是防止地址欺骗。
客户端必须真实存在并绑定一个真实的lease set。
它必须有入站隧道以接收连接响应。
这些隧道可以是零跳并立刻建立，但那将暴露创造者。
该协议实现了这个目标。



### 问题

- 该提案不支持盲目的目的地，但可以扩展以支持。见下文。




## 规范

### 协议和端口

可回复数据报2使用I2CP协议19；可回复数据报3使用I2CP协议20；原始数据报使用I2CP协议18。 请求可以是数据报2或数据报3。响应始终是原始的。 不得对请求或回复使用较老的可回复数据报（"数据报1"）格式，该数据报使用I2CP协议17；当在请求/回复端口接收到时必须将其丢弃。 请注意，数据报1协议17仍然用于DHT协议。

请求使用announce URL中的I2CP“to port”；见下文。
请求"from port"由客户端选择，但应为非零，并与DHT使用的端口不同，以便轻松分类响应。
跟踪器应该拒绝在错误端口接收到的请求。

响应使用请求中的I2CP“to port”。
请求“from port”是请求中的“to port”。


### 声明URL

声明URL格式未在[BEP 15](http://www.bittorrent.org/beps/bep_0015.html)中指定，但如同在清网中，UDP声明URL的格式为"udp://host:port/path"。
路径被忽略，可以为空，但在清网中通常为"/announce"。
:port部分应该始终存在，然而，如果省略了“:port”部分，使用默认I2CP端口6969，因为那是清网中的常用端口。
可能还有附加的cgi参数&a=b&c=d，可以在宣布请求中处理并提供，请参见[BEP 41](http://www.bittorrent.org/beps/bep_0041.html)。
如果没有参数或路径，尾随的/可能也可省略，正如[BEP 41](http://www.bittorrent.org/beps/bep_0041.html)所暗示的。


### 数据报格式

所有值均以网络字节顺序（大端）发送。 不要期望包的大小确切相等。 将来的扩展可能会增加包的大小。



连接请求
```````````````

客户端到跟踪器。
16字节。必须是可回复的数据报2。与[BEP 15](http://www.bittorrent.org/beps/bep_0015.html)相同。没有变化。


```
偏移  大小            名称            值
  0       64-bit integer  protocol_id     0x41727101980 // 魔法常量
  8       32-bit integer  action          0 // 连接
  12      32-bit integer  transaction_id
```



连接响应
````````````````

跟踪器到客户端。
16或18字节。必须是原始的。与[BEP 15](http://www.bittorrent.org/beps/bep_0015.html)相同，除了如下所述。


```
偏移  大小            名称            值
  0       32-bit integer  action          0 // 连接
  4       32-bit integer  transaction_id
  8       64-bit integer  connection_id
  16      16-bit integer  lifetime        可选  // 与BEP 15的变化
```

响应必须发送到作为请求“from port”收到的I2CP“to port”。

lifetime字段是可选的，表示client lifetime中的connection_id秒数。
默认值是60，如果指定，最小值是60。
最大值是65535或大约18小时。
跟踪器保持connection_id比client lifetime多60秒。


声明请求
````````````````

客户端到跟踪器。
最少98字节。必须是可回复的数据报3。与[BEP 15](http://www.bittorrent.org/beps/bep_0015.html)相同，除了如下所述。

connection_id与连接响应中接收到的一致。



```
偏移  大小            名称            值
  0       64-bit integer  connection_id
  8       32-bit integer  action          1     // 声明
  12      32-bit integer  transaction_id
  16      20-byte string  info_hash
  36      20-byte string  peer_id
  56      64-bit integer  downloaded
  64      64-bit integer  left
  72      64-bit integer  uploaded
  80      32-bit integer  event           0     // 0: 没有; 1: 完成; 2: 已开始; 3: 已停止
  84      32-bit integer  IP地址          0     // 默认
  88      32-bit integer  key
  92      32-bit integer  num_want        -1    // 默认
  96      16-bit integer  port
  98      各种            选项     可选  // 如BEP 41中规定
```

与[BEP 15](http://www.bittorrent.org/beps/bep_0015.html)的变化：

- key被忽略
- port可能被忽略
- options部分，如存在，按[BEP 41](http://www.bittorrent.org/beps/bep_0041.html)中规定

响应必须发送到作为请求“from port”收到的I2CP“to port”。
请勿使用宣布请求中的端口。



声明响应
`````````````````

跟踪器到客户端。
至少20字节。必须是原始的。与[BEP 15](http://www.bittorrent.org/beps/bep_0015.html)相同，除了如下所述。



```
偏移  大小            名称            值
  0           32-bit integer  action          1 // 声明
  4           32-bit integer  transaction_id
  8           32-bit integer  interval
  12          32-bit integer  leechers
  16          32-bit integer  seeders
  20   32 * n 32-byte hash    二进制哈希     // 与BEP 15的变化
  ...                                           // 与BEP 15的变化
```

与[BEP 15](http://www.bittorrent.org/beps/bep_0015.html)的变化：

- 我们返回的是32字节“精简响应”的SHA-256二进制对等体哈希的倍数，而不是6字节的IPv4+端口或18字节的IPv6+端口。
  与TCP精简响应一样，我们不包括端口。

响应必须发送到作为请求“from port”收到的I2CP“to port”。
请勿使用宣布请求中的端口。

I2P数据报具有非常大的最大大小约为64 KB；然而，为了可靠传输，应避免超过4 KB的数据报。
为了带宽效率，跟踪器可能应将最大对等体限制在大约50个，这对应于约1600字节包在不同层的开销之前，并应在分片后限制在两个隧道消息负载限制内。

与BEP 15一样，不包括后续的对等体地址（BEP 15的IP/port，这里的哈希）数量。
虽然BEP 15中不包含，但经过改革的对等体标记的所有零可以定义为表明对等信息已完成并跟随一些扩展数据。

为了将来可能的扩展，客户端应忽略32字节全零哈希，以及其后任何数据。
跟踪器应拒绝从全零哈希中宣布，尽管Java路由器已经禁止了该哈希。


抓取
``````

[BEP 15](http://www.bittorrent.org/beps/bep_0015.html)中的抓取请求/响应不是该提案所必需的，但可以根据需要实现，无需更改。
客户端必须首先获得连接ID。
抓取请求始终是可回复的数据报3。
抓取响应始终是原始的。



错误响应
````````````````

跟踪器到客户端。
最少8字节（如果消息为空）。
必须是原始的。与[BEP 15](http://www.bittorrent.org/beps/bep_0015.html)相同。没有变化。

```
偏移  大小            名称            值
  0       32-bit integer  action          3 // error
  4       32-bit integer  transaction_id
  8       string          消息

```



## 扩展

不包括扩展位或版本字段。
客户端和跟踪器不应假定数据包的大小。
通过这种方式，可以添加附加字段而不破坏兼容性。
如果需要，建议使用[BEP 41](http://www.bittorrent.org/beps/bep_0041.html)中定义的扩展格式。

连接响应被修改以添加一个可选的连接ID生命周期。

如果需要盲目的目标支持，我们可以添加盲目的35字节地址到宣布请求的末尾，或者请求盲目的响应哈希，使用[BEP 41](http://www.bittorrent.org/beps/bep_0041.html)格式（待定参数）。
一组盲目的35字节对等地址可以被添加到宣布回复的末尾，在全零32字节哈希之后。



## 实施指南

看到设计部分以上非集成，非I2CP客户端和跟踪器的实现挑战讨论。


### 客户端

对于给定的跟踪器主机名，客户端应优先选择UDP而非HTTP URL，且不应同时宣布给两者。

具有现有BEP 15支持的客户端只需很小的修改。

如果客户端支持DHT或其他数据报协议，可能应选择不同的端口作为请求“from port”，以便回复返回到该端口并不与DHT消息混淆。
客户端仅接收原始数据报作为回复。
跟踪器绝不会发送可回复数据报2到客户端。

具有默认开放跟踪器列表的客户端应更新列表，在已知开放跟踪器支持UDP之后添加UDP URL。

客户端可以实施或不实施请求的重新传输。
若要实施重新传输，应使用至少15秒的初始超时，并较每次重新传输时间加倍（指数退避）。

客户端接收到错误响应后必须退避。


### 跟踪器

具有现有BEP 15支持的跟踪器需只需进行小的修改。
该提案不同于2014年的提案，因为此跟踪器必须在同一端口上支持接收可回复数据报2和数据报3。

为了最小化跟踪器的资源需求，此协议被设计为消除跟踪器必须存储客户端哈希和连接ID映射以供后续验证的任何要求。
这是可能的，因为宣布请求包是可回复的数据报3包，因此它包含发送者的哈希。

建议实现是：

- 定义当前纪元为当前时间与连接生命周期的分辨率，``epoch = now / lifetime``。
- 定义一个加密哈希函数``H(secret, clienthash, epoch)``，生成一个8字节的输出。
- 为所有连接生成使用的随机常数secret。
- 对于连接响应，生成``connection_id = H(secret, clienthash, epoch)``。
- 对于宣布请求，验证接收到的连接ID在当前纪元中通过验证
  ``connection_id == H(secret, clienthash, epoch) || connection_id == H(secret, clienthash, epoch - 1)``。

## 迁移

现有客户端不支持UDP宣布URL并忽略它们。

现有跟踪器不支持接收可回复或原始数据报，它们将被丢弃。

该提案是完全可选的。无论何时，客户端和跟踪器都不要求实现它。



## 部署

预计第一个实现将是ZzzOT和i2psnark。
它们将用于测试和验证此提案。

其他实施将根据需要在测试和验证完成后进行。



## 参考

.. [BEP15]
    http://www.bittorrent.org/beps/bep_0015.html

.. [BEP41]
    http://www.bittorrent.org/beps/bep_0041.html

.. [DATAGRAMS]
    {{ spec_url('datagrams') }}

.. [Prop163]
    {{ proposal_url('163') }}

.. [Prop169]
    {{ proposal_url('169') }}

.. [SAMv3]
    {{ site_url('docs/api/samv3') }}

.. [SPEC]
    {{ site_url('docs/applications/bittorrent', True) }}

.. [UDP]
    {{ spec_url('udp-announces') }}
