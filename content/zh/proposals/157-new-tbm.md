---
title: "更小的隧道构建消息"
number: "157"
author: "zzz, 原始"
created: "2020-10-09"
lastupdated: "2021-07-31"
status: "Closed"
thread: "http://zzz.i2p/topics/2957"
target: "0.9.51"
---

## 注意
自 API 版本 0.9.51 起实现。
网络部署和测试进行中。
可能会有小的修订。
最终规范请参见 [I2NP](/en/docs/spec/i2np/) 和 [Tunnel-Creation-ECIES](/en/docs/spec/tunnel-creation-ecies/)。



## 概览


### 摘要

目前加密的隧道构建请求和回复记录的大小是 528。
对于典型的可变隧道构建和可变隧道构建回复消息，
总大小为 2113 字节。此消息在反向路径上分为三个 1KB 的隧道
消息。

对于 ECIES-X25519 路由器，528 字节的记录格式更改在 [Prop152](/en/proposals/152-ecies-tunnels/) 和 [Tunnel-Creation-ECIES](/en/docs/spec/tunnel-creation-ecies/) 中指定。
对于隧道中混合使用 ElGamal 和 ECIES-X25519 路由器的情况，记录大小必须保持为
528 字节。然而，如果隧道中的所有路由器都是 ECIES-X25519，则可以使用新的、更小的
构建记录，因为 ECIES-X25519 加密的开销要小得多
 than ElGamal.

较小的消息可以节省带宽。此外，如果消息可以适合
单个隧道消息，反向路径将三倍更有效。

该提案定义了新的请求和回复记录以及新的构建请求和构建回复消息。

隧道创建者和创建的隧道中的所有跳跃必须是 ECIES-X25519，并且至少是版本 0.9.51。
在网络中的大多数路由器都是 ECIES-X25519 之前，这个提议将没有用。
预计到 2021 年底将实现这一目标。


### 目标

更多目标请参见 [Prop152](/en/proposals/152-ecies-tunnels/) 和 [Prop156](/en/proposals/156-ecies-routers/)。

- 较小的记录和消息
- 保留将来选项的足够空间，如在 [Prop152](/en/proposals/152-ecies-tunnels/) 和 [Tunnel-Creation-ECIES](/en/docs/spec/tunnel-creation-ecies/)中
- 适合反向路径的一个隧道消息
- 仅支持 ECIES 跳跃
- 保留在 [Prop152](/en/proposals/152-ecies-tunnels/) 和 [Tunnel-Creation-ECIES](/en/docs/spec/tunnel-creation-ecies/)中实现的改进
- 最大化与当前网络的兼容性
- 在 OBEP 中隐藏入站构建消息
- 在 IBGW 中隐藏出站构建回复消息
- 不需要对整个网络进行 "旗帜日" 升级
- 逐步推出以最小化风险
- 重用现有加密原语


### 非目标

更多非目标请参见 [Prop156](/en/proposals/156-ecies-routers/)。

- 不需要混合 ElGamal/ECIES 隧道
- 层加密变更，请参见 [Prop153](/en/proposals/153-chacha20-layer-encryption/)
- 不加速加密操作。假设 ChaCha20 和 AES 是相似的，
  即使是 AESNI，至少对于所涉及的小数据大小来说。


## 设计


### 记录

计算见附录。

加密的请求和回复记录将为 218 字节，而不是现在的 528 字节。

明文请求记录将为 154 字节，
相比之下，ElGamal 记录为 222 字节，
而根据 [Prop152](/en/proposals/152-ecies-tunnels/) 和 [Tunnel-Creation-ECIES](/en/docs/spec/tunnel-creation-ecies/)定义的 ECIES 记录为 464 字节。

明文响应记录将为 202 字节，
相比较，ElGamal 记录为 496 字节，
而根据 [Prop152](/en/proposals/152-ecies-tunnels/) 和 [Tunnel-Creation-ECIES](/en/docs/spec/tunnel-creation-ecies/)定义的 ECIES 记录为 512 字节。

回复加密将使用 ChaCha20（不含 ChaCha20/Poly1305），
因此明文记录不需要是 16 字节的倍数。

请求记录通过使用 HKDF 创建层和回复密钥变小，
因此不需要在请求中显式包含。


### 隧道构建消息

两者都将是 "可变量的"，并具有一个字节的记录数量字段，
与现有可变消息一样。

ShortTunnelBuild: 类型 25
````````````````````````````

典型长度（4 个记录）: 873 字节

用于入站隧道构建时，
建议（但不要求）由原始发起人进行大蒜加密，
目标为入站网关（传送指令 ROUTER），
以隐藏来自 OBEP 的入站构建消息。
IBGW 解密消息，
将回复放入正确的槽中，
并将 ShortTunnelBuildMessage 发送到下一个跳跃。

选择记录长度，使得大蒜加密的 STBM 可以
适合单个隧道消息。请参见下文中的附录。



OutboundTunnelBuildReply: 类型 26
``````````````````````````````````````

我们定义一个新的 OutboundTunnelBuildReply 消息。
这仅用于出站隧道构建中。
目的是隐藏来自 IBGW 的出站构建回复消息。
必须由 OBEP 进行大蒜加密，目标为发起人
（传送指令 TUNNEL）。
OBEP 解密隧道构建消息，
构建一个 OutboundTunnelBuildReply 消息，
并将回复放入明文字段。
其他记录放入其他槽中。
然后使用派生的对称密钥对消息进行大蒜加密发送给发起人。


笔记
```````

通过对 OTBRM 和 STBM 进行大蒜加密，我们还避免了在配对隧道的 IBGW 和 OBEP 上的兼容性可能出现的任何潜在
问题。




### 消息流


  {% highlight %}
STBM：短隧道构建消息（类型 25）
  OTBRM：出站隧道构建回复消息（类型 26）

  出站构建 A-B-C
  通过现有入站 D-E-F 回复


                  新隧道
           STBM      STBM      STBM
  创建者 ------> A ------> B ------> C ---\
                                     OBEP   \
                                            | 大蒜包装
                                            | OTBRM
                                            | （TUNNEL 传送）
                                            | 从 OBEP 到
                                            | 创建者
                现有隧道             /
  创建者 <-------F---------E-------- D <--/
                                     IBGW



  入站构建 D-E-F
  通过现有出站 A-B-C 发送


                现有隧道
  创建者 ------> A ------> B ------> C ---\
                                    OBEP    \
                                            | 大蒜包装（可选）
                                            | STBM
                                            | （ROUTER 传送）
                                            | 从创建者
                  新隧道                | 到 IBGW
            STBM      STBM      STBM        /
  创建者 <------ F <------ E <------ D <--/
                                     IBGW



{% endhighlight %}



### 记录加密

请求和回复记录加密：如 [Prop152](/en/proposals/152-ecies-tunnels/) 和 [Tunnel-Creation-ECIES](/en/docs/spec/tunnel-creation-ecies/)中定义。

其他槽的回复记录加密：ChaCha20。


### 层加密

目前没有计划更改使用本规范构建的隧道的层加密；它将保持为 AES，
如当前用于所有隧道那样。

将层加密更改为 ChaCha20 是一个需要进一步研究的主题。



### 新隧道数据消息

目前没有计划更改使用本规范构建的隧道使用的 1KB 隧道数据消息。

引入新的更大或可变大小的 I2NP 消息以与本提案同步使用可能会有用，
以便在这些隧道中使用。
这将减少大消息的开销。
这是一个需要进一步研究的主题。




## 规格


### 短请求记录



短请求记录未加密部分
```````````````````````````````````````

这是 ECIES-X25519 路由器的隧道 BuildRequestRecord 的建议规范。
与 [Tunnel-Creation-ECIES](/en/docs/spec/tunnel-creation-ecies/) 的变化摘要：

- 将未加密长度从 464 更改为 154 字节
- 将加密长度从 528 更改为 218 字节
- 删除层和回复密钥及 IV，它们将从 split() 和 KDF 生成


请求记录不包含任何 ChaCha 回复密钥。
这些密钥是从一个 KDF 派生的。见下文。

所有字段都是大端格式。

未加密大小：154 字节。


  {% highlight lang='dataspec' %}

bytes 0-3: 接收消息的隧道 ID，非零
  bytes 4-7: 下一个隧道 ID，非零
  bytes 8-39: 下一个路由器身份哈希
  byte 40: 标志位
  bytes 41-42: 更多标志，未使用，设置为 0 以实现兼容性
  byte 43: 层加密类型
  bytes 44-47: 请求时间（自纪元以来的分钟数，向下取整）
  bytes 48-51: 请求的过期时间（自创建以来的秒数）
  bytes 52-55: 下一个消息 ID
  bytes 56-x: 隧道构建选项（Mapping）
  bytes x-x: 由标志或选项暗示的其他数据
  bytes x-153: 随机填充（见下文）

{% endhighlight %}


标志字段与 [Tunnel-Creation](/en/docs/spec/tunnel-creation/) 中定义相同，包含以下内容::

 位序：76543210（位 7 是 MSB）
 位 7：如果设置，允许来自任何人的消息
 位 6：如果设置，允许对任何人的消息，并将回复发送到
        指定的下一个跳跃在隧道构建回复消息中
 位 5-0：未定义，必须设置为 0 以实现与未来选项的兼容性

位 7 表示跳跃将是入站网关（IBGW）。位 6
表示跳跃将是出站端点（OBEP）。如果两者均未设置，
则跳跃将是中间参与者。不能同时设置两者。

层加密类型：0 为 AES（如当前隧道中）；
1 为未来（ChaCha？）

请求过期适用于未来的变量隧道持续时间。
目前唯一支持的值是 600 (10 分钟)。

创建者临时公钥是一个 ECIES 密钥，大端。
它用于 IBGW 层和回复密钥及 IVs 的 KDF。
这仅在入站隧道构建消息的明文记录中包含。
这是必需的，因为此层没有用于构建记录的 DH。

隧道构建选项是一个 Mapping 结构，如 [Common](/en/docs/spec/common-structures/) 中定义。
这是为了将来使用。目前尚未定义任何选项。
如果 Mapping 结构为空，则为两个字节 0x00 0x00。
Mapping 的最大大小（包括长度字段）为 98 字节，Mapping 长度字段的最大值为96。



短请求记录加密部分
`````````````````````````````````````

除了临时公钥为小端格式外，所有字段都是大端格式。

加密大小：218 字节


  {% highlight lang='dataspec' %}

bytes 0-15: 节点的截断身份哈希
  bytes 16-47: 发送方的临时 X25519 公钥
  bytes 48-201: ChaCha20 加密的 ShortBuildRequestRecord
  bytes 202-217: Poly1305 MAC

{% endhighlight %}



### 短回复记录


短回复记录未加密部分
`````````````````````````````````````
这是 ECIES-X25519 路由器的隧道 ShortBuildReplyRecord 的建议规范。
与 [Tunnel-Creation-ECIES](/en/docs/spec/tunnel-creation-ecies/) 的变化摘要：

- 将未加密长度从 512 更改为 202 字节
- 将加密长度从 528 更改为 218 字节


ECIES 回复使用 ChaCha20/Poly1305 加密。

所有字段都是大端格式。

未加密大小：202 字节。


  {% highlight lang='dataspec' %}

bytes 0-x: 隧道构建回复选项（Mapping）
  bytes x-x: 由选项暗示的其他数据
  bytes x-200: 随机填充（见下文）
  byte 201: 回复字节

{% endhighlight %}

隧道构建回复选项是一个 Mapping 结构，如 [Common](/en/docs/spec/common-structures/) 中定义。
这是为了将来使用。目前尚未定义任何选项。
如果 Mapping 结构为空，则为两个字节 0x00 0x00。
Mapping 的最大大小（包括长度字段）为 201 字节，Mapping 长度字段的最大值为199。

回复字节是以下值之一
如 [Tunnel-Creation](/en/docs/spec/tunnel-creation/) 中定义，以避免指纹：

- 0x00（接受）
- 30（TUNNEL_REJECT_BANDWIDTH）


短回复记录加密部分
```````````````````````````````````

加密大小：218 字节


  {% highlight lang='dataspec' %}

bytes 0-201: ChaCha20 加密的 ShortBuildReplyRecord
  bytes 202-217: Poly1305 MAC

{% endhighlight %}



### KDF

见下文的 KDF 部分。




### ShortTunnelBuild
I2NP 类型 25

此消息发送给中间跳跃，OBEP 和 IBEP（创建者）。
不得发送给 IBGW（改用大蒜包装的 InboundTunnelBuild）。
当接收到 OBEP 时，会转化为一个 OutboundTunnelBuildReply，
大蒜包装，并发送给发起人。



  {% highlight lang='dataspec' %}
+----+----+----+----+----+----+----+----+
  | num| ShortBuildRequestRecords...
  +----+----+----+----+----+----+----+----+

  num ::
         1 字节 `整数`
         有效值：1-8

  记录大小：218 字节
  总大小：1+$num*218
{% endhighlight %}

笔记
`````
* 典型的记录数为 4，总大小为 873。




### OutboundTunnelBuildReply
I2NP 类型 26

此消息由 OBEP 通过现有入站隧道仅发送给 IBEP（创建者）。
不得发送给任何其他跳跃。
总是大蒜加密。


  {% highlight lang='dataspec' %}
+----+----+----+----+----+----+----+----+
  | num|                                  |
  +----+                                  +
  |      ShortBuildReplyRecords...        |
  +----+----+----+----+----+----+----+----+

  num ::
         记录总数,
         1 字节 `整数`
         有效值：1-8

  ShortBuildReplyRecords ::
         加密记录
         长度：num * 218

  加密记录大小：218 字节
  总大小：1+$num*218
{% endhighlight %}

笔记
`````
* 典型的记录数为 4，总大小为 873。
* 此消息应为大蒜加密。



### KDF

我们使用隧道构建记录加密/解密后 Noise 状态中的 ck 来导出以下密钥：回复密钥、AES 层密钥、AES IV 密钥、OBEP 的大蒜回复密钥/标签。

回复密钥:
与长记录不同，我们不能使用 ck 的左侧部分作为回复密钥，因为它不是最后一个并将被稍后使用。
回复密钥用于使用 AEAD/Chaha20/Poly1305 和 Chacha20 加密该记录，以回复其他记录。
两者都使用相同的密钥，nonce 是消息中记录的位置，从 0 开始。


  {% highlight lang='dataspec' %}
keydata = HKDF(ck, ZEROLEN, "SMTunnelReplyKey", 64)
  replyKey = keydata[32:63]
  ck = keydata[0:31]

  层密钥：
  层密钥目前总是 AES，但同样的 KDF 可以从 Chacha20 中使用

  keydata = HKDF(ck, ZEROLEN, "SMTunnelLayerKey", 64)
  layerKey = keydata[32:63]

  非 OBEP 记录的 IV 密钥：
  ivKey = keydata[0:31]
  因为它是最后一个

  OBEP 记录的 IV 密钥：
  ck = keydata[0:31]
  keydata = HKDF(ck, ZEROLEN, "TunnelLayerIVKey", 64)
  ivKey = keydata[32:63]
  ck = keydata[0:31]

  OBEP 大蒜回复密钥/标签：
  keydata = HKDF(ck, ZEROLEN, "RGarlicKeyAndTag", 64)
  replyKey = keydata[32:63]
  replyTag = keydata[0:7]

{% endhighlight %}





## 正当理由

此设计最大程度地重用了现有的加密原语、协议和代码。

此设计降低了风险。

在 Java 测试中，ChaCha20 稍微比 AES 快一些。
ChaCha20 避免了数据大小必须是 16 的倍数的要求。


## 实施注意事项

- 与现有的可变隧道构建消息一样，
  不推荐少于 4 条记录的消息。
  典型默认值为 3 个跳。
  入站隧道必须使用额外的记录来构建
  原始发起人，因此最后一个跳跃不知道它是最后一个。
  为了使中间跳跃不知道隧道是入站还是出站，
  出站隧道也应该使用 4 条记录来构建。



## 问题



## 迁移

实施、测试和推广将需要几个版本
大约一年。各个阶段如下。每个阶段分配给特定版本的安排将取决于
的发展速度。

每个 I2P 实现的详细实现和迁移可能会有所不同。

隧道创建者必须确保创建的隧道中的所有跳跃都是 ECIES-X25519，并且至少是版本 TBD。
隧道创建者不必是 ECIES-X25519；它可以是 ElGamal。
然而，如果创建者是 ElGamal，则会向最近的跳跃泄露它是创建者的信息。
因此，实际上，这些隧道应该只由 ECIES 路由器创建。

不应该要求配对隧道 OBEP 或 IBGW 是 ECIES 或
的任何特定版本。
新消息被大蒜包装，并且在配对隧道的 OBEP 或 IBGW 上不可见。

阶段 1：实现，默认不启用

阶段 2（下一个版本）：默认启用

没有向后兼容性问题。新的消息只能发送给支持它们的路由器。




## 附录


如果没有未加密入站 STBM 的大蒜开销，
如果我们不使用 ITBM：



  {% highlight lang='text' %}
当前 4 槽大小：4 * 528 + 开销 = 3 个隧道消息

  4 槽构建消息以适应一个隧道消息，仅节奏：

  1024
  - 21 分片头
  ----
  1003
  - 35 未分片的 ROUTER 传送指令
  ----
  968
  - 16 I2NP 头
  ----
  952
  - 1 槽数
  ----
  951
  / 4 槽
  ----
  237 新的加密构建记录大小（而不是现在的 528）
  - 16 截断哈希
  - 32 临时密钥
  - 16 MAC
  ----
  173 明文构建记录最大值（而不是现在的 222）



{% endhighlight %}


对于我们不使用 ITBM 的情况，使用 "N" 噪声模式对入站 STBM 进行大蒜加密的开销：


  {% highlight lang='text' %}
当前 4 槽大小：4 * 528 + 开销 = 3 个隧道消息

  4 槽大蒜加密的构建消息以适应一个隧道消息，仅节奏：

  1024
  - 21 分片头
  ----
  1003
  - 35 未分片的 ROUTER 传送指令
  ----
  968
  - 16 I2NP 头
  - 4 长度
  ----
  948
  - 32 字节临时密钥
  ----
  916
  - 7 字节 DateTime 块
  ----
  909
  - 3 字节大蒜块开销
  ----
  906
  - 9 字节 I2NP 头
  ----
  897
  - 1 字节大蒜本地传送指令
  ----
  896
  - 16 字节 Poly1305 MAC
  ----
  880
  - 1 槽数
  ----
  879
  / 4 槽
  ----
  219 新的加密构建记录大小（而不是现在的 528）
  - 16 截断哈希
  - 32 临时密钥
  - 16 MAC
  ----
  155 明文构建记录最大值（而不是现在的 222）


{% endhighlight %}

笔记：

在未使用填充的情况下，当前构建记录明文大小：193

去除完整的路由器哈希和 HKDF 生成的密钥/IV 释放出大量的空间以供将来选项使用。
如果一切都是 HKDF，所需的明文空间大约为 58 字节（无任何选项）。

大蒜包装的 OTBRM 略小于大蒜包装的 STBM，
因为传送指令为本地而非路由器，
不包括 DATETIME 块，以及
它使用 8 字节的标签而不是完整 'N' 消息的 32 字节临时密钥。



## 参考资料
