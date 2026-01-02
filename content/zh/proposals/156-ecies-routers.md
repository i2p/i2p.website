---
title: "ECIES 路由器"
number: "156"
author: "zzz, orignal"
created: "2020-09-01"
lastupdated: "2025-03-05"
status: "Closed"
thread: "http://zzz.i2p/topics/2950"
target: "0.9.51"
toc: true
---

## 注意
网络部署和测试正在进行中。
可能会有修订。
状态：

- ECIES 路由器已在 0.9.48 中实现，详情见 [Common](/docs/specs/common-structures/)。
- 隧道构建已在 0.9.48 中实现，详情见 [Tunnel-Creation-ECIES](/docs/specs/implementation/#tunnel-creation-ecies)。
- 到 ECIES 路由器的加密消息已在 0.9.49 中实现，详情见 [ECIES-ROUTERS](/docs/specs/ecies/)。
- 新的隧道构建消息已在 0.9.51 中实现。


## 概述


### 摘要

路由器身份目前包含一个 ElGamal 加密密钥。
这是自 I2P 开始以来的标准。
ElGamal 速度较慢，需要在其使用的所有地方进行替换。

关于 LS2 的提案 [Prop123](/proposals/123-new-netdb-entries/) 和 ECIES-X25519-AEAD-Ratchet [Prop144](/proposals/144-ecies-x25519-aead-ratchet/) 
（现在在 [ECIES](/docs/specs/ecies/) 中指定）定义了用 ECIES 替换目的地的 ElGamal。

本提案定义了用 ECIES-X25519 替换路由器的 ElGamal。
本提案提供了所需更改的概述。
大部分细节在其他提案和规范中。
请参见参考部分的链接。


### 目标

参见 [Prop152](/proposals/152-ecies-tunnels/)，了解其他目标。

- 在路由器身份中用 ECIES-X25519 替换 ElGamal
- 复用现有加密原语
- 在可能的情况下提高隧道构建消息的安全性，同时保持兼容性
- 支持包含 ElGamal/ECIES 节点的混合隧道
- 最大化与当前网络的兼容性
- 不需要对整个网络进行“旗日”升级
- 逐步推出以最小化风险
- 新的、更小的隧道构建消息


### 非目标

参见 [Prop152](/proposals/152-ecies-tunnels/)，了解其他非目标。

- 不要求双密钥路由器
- 层加密更改，参见 [Prop153](/proposals/153-chacha20-layer-encryption/)


## 设计


### 密钥位置和加密类型

对于目的地，密钥在租约集中而不在目的地，我们支持在同一租约集中使用多种加密类型。

对于路由器，路由器的加密密钥在其路由器身份中。参见通用结构规范 [Common](/docs/specs/common-structures/)。

对于路由器，我们将用 32 字节的 X25519 密钥和 224 字节的填充替换路由器身份中的 256 字节 ElGamal 密钥。
这将通过密钥证书中的加密类型指示。
加密类型（与 LS2 中使用的相同）为 4。
这表示一个小端32字节的 X25519 公钥。
这是在通用结构规范 [Common](/docs/specs/common-structures/) 中定义的标准结构。

这与提案 145 中为加密类型 1-3 提出的关于 ECIES-P256 的方法相同 [Prop145](/proposals/145-ecies/)。
虽然这个提案从未被采纳，但 Java 实现开发人员通过在代码库中的多个地方添加检查来为路由器身份密钥证书中的加密类型做准备。这些工作大多是在 2019 年中旬完成的。


### 隧道构建消息

为了使用 ECIES 而不是 ElGamal，需要对隧道创建规范 [Tunnel-Creation](/docs/specs/implementation/#tunnel-creation-ecies) 进行几项更改。
此外，我们将改进隧道构建消息以提高安全性。

在第一阶段，我们将更改 ECIES 跳的构建请求记录和构建响应记录的格式和加密。
这些更改将与现有的 ElGamal 路由器兼容。
这些更改在提案 152 [Prop152](/proposals/152-ecies-tunnels/) 中定义。

在第二阶段，我们将添加新的构建请求消息、构建回复消息、构建请求记录和构建响应记录的版本。
尺寸将缩小以提高效率。
这些更改必须由隧道中的所有跳支持，并且所有跳都必须是 ECIES。
这些更改在提案 157 [Prop157](/proposals/157-new-tbm/) 中定义。


### 端到端加密

#### 历史

在 Java I2P 的原始设计中，路由器及其所有本地目的地共享单个 ElGamal 会话密钥管理器 (SKM)。
因为共享 SKM 可能泄露信息并允许攻击者进行关联，所以设计被更改为支持路由器和每个目的地使用单独的 ElGamal SKM。
ElGamal 设计仅支持匿名发送者；发送方仅发送临时密钥，而不是静态密钥。
消息与发送者的身份无关。

随后，我们在 ECIES-X25519-AEAD-Ratchet [Prop144](/proposals/144-ecies-x25519-aead-ratchet/) 中设计了 ECIES Ratchet SKM，现在在 [ECIES](/docs/specs/ecies/) 中指定。
该设计使用了 Noise “IK” 模式，该模式在第一条消息中包含了发送者的静态密钥。
该协议用于 ECIES（类型 4）目的地。
IK 模式不允许匿名发送者。

因此，我们在提案中包括了一种方法，即使用零填充静态密钥向 Ratchet SKM 发送匿名消息。
这模拟了一个兼容的方式的 Noise “N” 模式，因此 ECIES SKM 可以接收匿名和非匿名消息。
目的是使用零密钥来实现 ECIES 路由器。


#### 使用案例和威胁模型

发送给路由器的消息的使用案例和威胁模型与目的地之间的端到端消息的使用案例和威胁模型大不相同。


目的地使用案例和威胁模型：

- 来自/到目的地的非匿名（发送方包含静态密钥）
- 高效支持目的地之间的持续流量（全握手、流式传输、标记）
- 始终通过出站和入站隧道发送
- 隐藏来自 OBEP 和 IBGW 的所有识别特征，需要 Elligator2 编码的临时密钥。
- 两个参与者必须使用相同的加密类型


路由器使用案例和威胁模型：

- 来自路由器或目的地的匿名消息（发送方不包含静态密钥）
- 仅用于加密的数据库查找和存储，通常发送给 floodfills
- 偶然消息
- 多个消息不应被关联
- 始终通过出站隧道直接发送到路由器。不使用入站隧道
- OBEP 知道它正在将消息转发给路由器，并知道其加密类型
- 两个参与者可能有不同的加密类型
- 数据库查找回复是一次性消息，使用数据库查找消息中的回复密钥和标记
- 数据库存储确认是一次性消息，使用捆绑的交付状态消息


路由器使用案例非目标：

- 不需要非匿名消息
- 不需要通过入站探索隧道发送消息（路由器不发布探索租约集）
- 不需要使用标记进行持续的消息流量
- 不需要为目的地运行“双密钥”会话密钥管理器（详见 [ECIES](/docs/specs/ecies/)）。路由器只有一个公钥。


#### 设计结论

ECIES 路由器 SKM 不需要为目的地指定的完整 Ratchet SKM（见 [ECIES](/docs/specs/ecies/)）。
没有需要使用 IK 模式发送非匿名消息的要求。
威胁模型不需要 Elligator2 编码的临时密钥。

因此，路由器 SKM 将使用 Noise "N" 模式，与 [Prop152](/proposals/152-ecies-tunnels/) 为隧道构建指定的相同。
它将使用与 [ECIES](/docs/specs/ecies/) 为目的地指定的相同的负载格式。
IK 指定的零静态密钥（无绑定或会话）模式将不使用。

查找的回复将使用查找中的请求加密进行 Ratchet 标记加密。
如 [Prop154](/proposals/154-ecies-lookups/) 中记录的那样，现在在 [I2NP](/docs/specs/i2np/) 中指定。

设计使路由器能够拥有单个 ECIES 会话密钥管理器。
没有必要像在 [ECIES](/docs/specs/ecies/) 中为目的地描述的那样运行“双密钥”会话密钥管理器。
路由器只有一个公钥。

ECIES 路由器没有 ElGamal 静态密钥。
路由器仍然需要一个 ElGamal 的实现，通过 ElGamal 路由器建造隧道并向 ElGamal 路由器发送加密消息。

ECIES 路由器可能需要一个部分 ElGamal 会话密钥管理器，以接收从 0.9.46 之前的 floodfill 路由器作为 NetDB 查找回复的 ElGamal 标记消息，因为这些路由器没有 [Prop152](/proposals/152-ecies-tunnels/) 中指定的 ECIES 标记回复的实现。
如果没有， ECIES 路由器可能不会请求来自 0.9.46 之前的 floodfill 路由器的加密回复。

这是可选的。决定可能会在各种 I2P 实现中有所不同，并可能取决于网络升级到 0.9.46 或更高版本的数量。
截至目前，约 85% 的网络为 0.9.46 或更高版本。


## 规范

X25519：详见 [ECIES](/docs/specs/ecies/)。

路由器身份和密钥证书：详见 [Common](/docs/specs/common-structures/)。

隧道构建：详见 [Prop152](/proposals/152-ecies-tunnels/)。

新隧道构建消息：详见 [Prop157](/proposals/157-new-tbm/)。


### 请求加密

请求加密与 [Tunnel-Creation-ECIES](/docs/specs/implementation/#tunnel-creation-ecies) 和 [Prop152](/proposals/152-ecies-tunnels/) 中指定的一致，
使用 Noise “N” 模式。

查找的回复将使用请求中的 Ratchet 标记加密。
数据库查找请求消息包含 32 字节的回复密钥和 8 字节的回复标记，
详见 [I2NP](/docs/specs/i2np/) 和 [Prop154](/proposals/154-ecies-lookups/)。密钥和标记用于加密回复。

不创建标记集。
不会使用 ECIES-X25519-AEAD-Ratchet [Prop144](/proposals/144-ecies-x25519-aead-ratchet/) 和 [ECIES](/docs/specs/ecies/) 指定的零静态密钥方案。
临时密钥不会进行 Elligator2 编码。

通常，这些将是新的会话消息，并将使用零静态密钥（无绑定或会话）发送，因为消息的发送者是匿名的。


#### 初始 ck 和 h 的 KDF

这是标准的 [NOISE](https://noiseprotocol.org/noise.html)，用于模式 "N" 和标准协议名称。
这与 [Tunnel-Creation-ECIES](/docs/specs/implementation/#tunnel-creation-ecies) 和 [Prop152](/proposals/152-ecies-tunnels/) 中为隧道构建消息指定的一样。


  ```text

这是 "e" 消息模式：

  // 定义 protocol_name。
  将 protocol_name 设置为 "Noise_N_25519_ChaChaPoly_SHA256"
  （31 字节，US-ASCII 编码，无 NULL 终止）。

  // 定义 Hash h = 32 字节
  // 填充到 32 字节。不要哈希，因为它不超过 32 字节。
  h = protocol_name || 0

  定义 ck = 32 字节链接密钥。复制 h 数据到 ck。
  设置 chainKey = h

  // MixHash(null 引言)
  h = SHA256(h);

  // 直到这里，所有路由器都可以预计算。


  ```


#### 消息的 KDF

消息创建者为每个消息生成一个临时 X25519 密钥对。
每个消息都必须有唯一的临时密钥。
这与 [Tunnel-Creation-ECIES](/docs/specs/implementation/#tunnel-creation-ecies) 和 [Prop152](/proposals/152-ecies-tunnels/) 中为隧道构建消息指定的相同。


  ```dataspec


// 目标路由器的 X25519 静态密钥对 (hesk, hepk) 来自路由器身份
  hesk = 生成私钥()
  hepk = 派生公钥(hesk)

  // MixHash(hepk)
  // || 以下表示追加
  h = SHA256(h || hepk);

  // 直到这里，每个路由器都可以为所有传入消息预计算

  // 发送者生成一个 X25519 临时密钥对
  sesk = 生成私钥()
  sepk = 派生公钥(sesk)

  // MixHash(sepk)
  h = SHA256(h || sepk);

  结束 "e" 消息模式。

  这是 "es" 消息模式：

  // Noise es
  // 发送者使用接收者的静态公钥执行 X25519 DH。
  // 目标路由器
  // 从加密记录前提取发送者的临时密钥。
  sharedSecret = DH(sesk, hepk) = DH(hesk, sepk)

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // ChaChaPoly 参数用于加密/解密
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  // 链接密钥不使用
  //chainKey = keydata[0:31]

  // AEAD 参数
  k = keydata[32:63]
  n = 0
  明文 = 464 字节构建请求记录
  ad = h
  密文 = ENCRYPT(k, n, 明文, ad)

  结束 "es" 消息模式。

  // MixHash(ciphertext) 是不需要的
  //h = SHA256(h || ciphertext)


  ```


#### 负载

负载与 [ECIES](/docs/specs/ecies/) 和 [Prop144](/proposals/144-ecies-x25519-aead-ratchet/) 中定义的块格式相同。
所有消息必须包含防止重放的 DateTime 块。


### 回复加密

对数据库查找消息的回复是数据库存储或数据库搜索回复消息。
它们被加密为现有会话消息，使用包含在 [I2NP](/docs/specs/i2np/) 和 [Prop154](/proposals/154-ecies-lookups/) 中指定的 32 字节的回复密钥和 8 字节的回复标记。


数据库存储消息没有明确的回复。
发送者可以将自己的回复捆绑为发送给自己的大蒜消息，包含一个交付状态消息。


## 原因

该设计最大限度地复用现有加密原语、协议和代码。

该设计将风险降至最低。


## 实施说明

较老的路由器不检查路由器的加密类型，并会发送 ElGamal 加密的构建记录或网络数据库消息。
一些最近的路由器存在漏洞，并会发送各种类型的格式不当的构建记录。
一些最近的路由器可能会发送非匿名（完整的 ratchet）网络数据库消息。
实现者应尽早检测并拒绝这些记录和消息，以减少 CPU 使用率。


## 问题

提案 145 [Prop145](/proposals/145-ecies/) 是否会重写以便与
提案 152 [Prop152](/proposals/152-ecies-tunnels/) 兼容尚不确定。


## 迁移

实施、测试和推广将在几个版本中完成，约需一年时间。
阶段如下。每个阶段分配给特定版本尚未决定，取决于开发进度。

每个 I2P 实现的实施和迁移细节可能有所不同。


### 基本点对点

ECIES 路由器可以连接到并从 ElGamal 路由器接收连接。
这应该在现阶段可行，因为到 2019 年中期，Java 代码库已经添加了一些检查来响应未完成的提案 145 [Prop145](/proposals/145-ecies/)。
确保代码库中没有任何内容阻止与非 ElGamal 路由器的点对点连接。

代码正确性检查：

- 确保 ElGamal 路由器不会请求 AEAD 加密回复给数据库查找消息（当回复通过探索隧道返回给路由器时）
- 确保 ECIES 路由器不会请求 AES 加密回复给数据库查找消息（当回复通过探索隧道返回给路由器时）

直到后续阶段，规范和实现完成时：

- 确保 ElGamal 路由器不会尝试通过 ECIES 路由器构建隧道。
- 确保 ElGamal 路由器不会向 ECIES floodfill 路由器发送加密的 ElGamal 消息。
  （数据库查找和数据库存储）
- 确保 ECIES 路由器不会向 ElGamal floodfill 路由器发送加密的 ECIES 消息。
  （数据库查找和数据库存储）
- 确保 ECIES 路由器不会自动成为 floodfill。

无需进行更改。
如果需要更改，目标发行版：0.9.48


### NetDB 兼容性

确保 ECIES 路由器信息可以存储到 ElGamal floodfills 并从中检索。
这应该在现阶段可行，因为到 2019 年中期，Java 代码库已经添加了一些检查来响应未完成的提案 145 [Prop145](/proposals/145-ecies/)。
确保代码库中没有任何内容阻止在网络数据库中存储非 ElGamal RouterInfos。

无需进行更改。
如果需要更改，目标发行版：0.9.48


### 隧道构建

按照提案 152 [Prop152](/proposals/152-ecies-tunnels/) 实施隧道构建。
首先让 ECIES 路由器构建与所有 ElGamal 跳的隧道；
通过构建入站隧道来测试和调试。

然后测试和支持 ECIES 路由器构建带有混合 ElGamal 和 ECIES 跳的隧道。

然后启用通过 ECIES 路由器的隧道构建。
除非在发布后对提案152进行不兼容的更改，否则不需要最低版本检查。

目标发布：0.9.48，2020 年下半年


### 向 ECIES floodfills 的 Ratchet 消息

按照提案 144 [Prop144](/proposals/144-ecies-x25519-aead-ratchet/) 实施和测试 ECIES 消息（带有零静态密钥）由 ECIES floodfills 接收。
实现和测试由 ECIES 路由器接收的对数据库查找消息的 AEAD 回复。

启用 ECIES 路由器的自动 floodfill。
然后启用发送 ECIES 消息到 ECIES 路由器。
除非在发布后对提案152进行不兼容的更改，否则不需要最低版本检查。

目标发布：0.9.49，2021 年初。
ECIES 路由器可以自动成为 floodfill。


### 重新密钥和新安装

新安装将在版本 0.9.49 中默认使用 ECIES。

逐步重新密钥所有路由器以最大限度地减少风险和对网络的干扰。
使用现有代码，该代码多年前曾用于签名类型迁移的重新密钥。
此代码在每次重启时给予每个路由器一个小的重新密钥随机概率。
经过多次重启，路由器可能会重新密钥为 ECIES。

开始重新密钥的标准是足够多的网络节点（可能是 50%）可以通过 ECIES 路由器构建隧道（0.9.48 或更高版本）。

在激进地重新密钥整个网络之前，绝大多数（可能是 90% 或更多）必须能够通过 ECIES 路由器构建隧道（0.9.48 或更高版本）
并向 ECIES floodfills 发送消息（0.9.49 或更高版本）。
这个目标可能在 0.9.52 版本中达到。

重新密钥将需要数个版本。

目标发布：
0.9.49 以便新路由器默认使用 ECIES；
0.9.49 开始缓慢重新密钥；
0.9.50 - 0.9.52 反复增加重新密钥率；
2021 年底大部分网络完成重新密钥。


### 新的隧道构建消息（阶段 2）

按照提案 157 [Prop157](/proposals/157-new-tbm/) 实施和测试新的隧道构建消息。
在版本 0.9.51 中推出支持。
进行额外测试，然后在版本 0.9.52 中启用。

测试将很困难。
在广泛测试之前，网络的一个好的子集必须支持它。
在广泛有用之前，必须有大多数网络支持它。
如果在测试后需要对规范或实现进行更改，这将推迟推出额外版本。

目标发布：0.9.52，2021 年底。


### 重新密钥完成

届时，早于某个待定版本的路由器将无法通过大多数对等体构建隧道。

目标发布：0.9.53，2022 年初。


