---
title: "ECIES 隧道"
number: "152"
author: "chisana, zzz, orignal"
created: "2019-07-04"
lastupdated: "2025-03-05"
status: "Closed"
thread: "http://zzz.i2p/topics/2737"
target: "0.9.48"
implementedin: "0.9.48"
---

## 注意
网络部署和测试正在进行中。
可能会有小的修订。
参见 [SPEC](/en/docs/spec/) 获取官方规范。


## 总览

本文档提出对隧道建立消息加密的更改，
使用 [ECIES-X25519](/en/docs/spec/ecies/) 引入的加密原语。
这是整个提案 [Prop156](/en/proposals/156-ecies-routers/) 的一部分，
用于将路由器从 ElGamal 转换为 ECIES-X25519 密钥。

为了将网络从 ElGamal + AES256 过渡到 ECIES + ChaCha20，
需要使用具有混合 ElGamal 和 ECIES 路由器的隧道。
提供了处理混合隧道跳点的规格。
不会对 ElGamal 跳点的格式、处理或加密进行更改。

ElGamal 隧道创建者需要为每个跳点创建临时 X25519 密钥对，
并遵循此规格来创建包含 ECIES 跳点的隧道。

该提案指定了 ECIES-X25519 隧道构建所需的更改。
有关 ECIES 路由器所需的所有更改的概述，请参阅提案 156 [Prop156](/en/proposals/156-ecies-routers/)。

此提案保持隧道构建记录的相同大小，
以确保兼容性。较小的构建记录和消息将在之后实现 —— 参见 [Prop157](/en/proposals/157-new-tbm/)。


### 加密原语

没有引入新的加密原语。实现此提案所需的原语是：

- 如 [Cryptography](/en/docs/spec/cryptography/) 中所示的 AES-256-CBC
- STREAM ChaCha20/Poly1305 函数：
  ENCRYPT(k, n, plaintext, ad) 和 DECRYPT(k, n, ciphertext, ad) —— 如 [NTCP2](/en/docs/spec/ntcp2/) [ECIES-X25519](/en/docs/spec/ecies/) 和 [RFC-7539](https://tools.ietf.org/html/rfc7539) 中所示
- X25519 DH 函数 —— 如 [NTCP2](/en/docs/spec/ntcp2/) 和 [ECIES-X25519](/en/docs/spec/ecies/) 中所示
- HKDF(salt, ikm, info, n) —— 如 [NTCP2](/en/docs/spec/ntcp2/) 和 [ECIES-X25519](/en/docs/spec/ecies/) 中所示

其他在别处定义的 Noise 函数：

- MixHash(d) —— 如 [NTCP2](/en/docs/spec/ntcp2/) 和 [ECIES-X25519](/en/docs/spec/ecies/) 中所示
- MixKey(d) —— 如 [NTCP2](/en/docs/spec/ntcp2/) 和 [ECIES-X25519](/en/docs/spec/ecies/) 中所示


### 目标

- 提高加密操作的速度
- 将 ElGamal + AES256/CBC 替换为隧道 BuildRequestRecords 和 BuildReplyRecords 中的 ECIES 原语。
- 对加密的 BuildRequestRecords 和 BuildReplyRecords 的大小（528 字节）不进行变更以保证兼容性
- 没有新的 I2NP 消息
- 维持加密的构建记录的大小以保证兼容性
- 为隧道建立消息添加前向保密性。
- 添加认证加密
- 检测跳点的 BuildRequestRecords 重排
- 增加时间戳的分辨率以便减少布隆过滤器的大小
- 添加隧道到期字段，以便能够实现变动的隧道生存期（仅限全 ECIES 隧道）
- 为未来功能添加可扩展的选项字段
- 重用现有的加密原语
- 在维护兼容性的同时尽可能提高隧道构建消息的安全性
- 支持具有混合 ElGamal/ECIES 节点的隧道
- 改善对构建消息的“标记”攻击的防御
- 跳点在处理构建消息之前不需要知道下一个跳点的加密类型，
因为它们可能在那时没有下一个跳点的 RI
- 最大限度地与当前网络兼容
- 对于 ElGamal 路由器，对隧道构建 AES 请求/回复加密不进行更改
- 对隧道 AES“层”加密不进行更改，请参阅 [Prop153](/en/proposals/153-chacha20-layer-encryption/)
- 继续支持 8 记录 TBM/TBRM 和可变大小的 VTBM/VTBRM
- 不要求整个网络进行“旗日”升级


### 非目标

- 需要“旗日”的隧道构建消息的完全重新设计。
- 缩小隧道构建消息（需要全部为 ECIES 的跳点和一个新的提案）
- 使用 [Prop143](/en/proposals/143-build-message-options/) 中定义的隧道构建选项，仅用于小消息
- 双向隧道，参见 [Prop119](/en/proposals/119-bidirectional-tunnels/)
- 更小的隧道构建消息，参见 [Prop157](/en/proposals/157-new-tbm/)


## 威胁模型

### 设计目标

- 没有跳点能够确定隧道的发起者。

- 中间跳点不得能够确定隧道的方向或它们在隧道中的位置。

- 没有跳点可以读取其他请求或回复记录的任何内容，除非是截断的路由器哈希和下一个跳点的临时密钥

- 出站构建的回复隧道的任何成员都无法读取任何回复记录。

- 入站构建的出站隧道的任何成员都无法读取任何请求记录，
除非 OBEP 可以看到截断的路由器哈希和 IBGW 的临时密钥




### 标记攻击

隧道构建设计的一个主要目标是使合谋的路由器 X 和 Y 难以知道它们在同一个隧道中。
如果路由器 X 在第 m 跳而路由器 Y 在第 m+1 跳，它们显然会知道。
但是如果路由器 X 在第 m 跳而路由器 Y 在第 m+n 跳（n>1），这应该会更加困难。

标记攻击是指中间跳点路由器 X 以某种方式修改隧道构建消息，使得当构建消息到达时，路由器 Y 能够检测到这种修改。
目标是任何被修改的消息在到达路由器 Y 之前都被 X 和 Y 之间的某个路由器拦截并丢弃。
对于那些未在路由器 Y 之前被丢弃的修改，隧道创建者应检测回复中的腐败并丢弃隧道。

可能的攻击：

- 修改构建记录
- 替换构建记录
- 添加或移除构建记录
- 重排构建记录

待办：当前设计是否能防止所有这些攻击？



## 设计

### Noise 协议框架

本提案根据 Noise 协议框架 [NOISE](https://noiseprotocol.org/noise.html) (修订版 34, 2018-07-11) 提供需求。
在 Noise 术语中，Alice 是发起者，而 Bob 是响应者。

本提案基于 Noise 协议 Noise_N_25519_ChaChaPoly_SHA256。
本 Noise 协议使用以下原语：

- 单向握手模式：N
  Alice 不将她的静态密钥传输给 Bob (N)

- DH 函数：X25519
  长度为 32 字节的 X25519 DH，如 [RFC-7748](https://tools.ietf.org/html/rfc7748) 中所述。

- 密码函数：ChaChaPoly
  AEAD_CHACHA20_POLY1305 如 [RFC-7539](https://tools.ietf.org/html/rfc7539) 第 2.8 节所述。
  12 字节的 nonce，前 4 个字节设为零。
  与 [NTCP2](/en/docs/spec/ntcp2/) 中的相同。

- 哈希函数：SHA256
  标准 32 字节哈希，已在 I2P 中广泛使用。

对框架的补充
````````````````````````````

无。


### 握手模式

握手使用 [Noise](https://noiseprotocol.org/noise.html) 握手模式。

使用以下字母映射：

- e = 一次性临时密钥
- s = 静态密钥
- p = 消息载荷

构建请求与 Noise N 模式相同。
这也与 [NTCP2](/en/docs/spec/ntcp2/) 中使用的 XK 模式的第一个（会话请求）消息相同。

  ```dataspec

<- s
  ...
  e es p ->




  ```


### 请求加密

构建请求记录由隧道创建者创建，并以非对称方式加密到单个跳点。
请求记录的这种非对称加密目前为 [Cryptography](/en/docs/spec/cryptography/) 中定义的 ElGamal，并包含一个 SHA-256 校验和。这个设计不是前向保密的。

新设计将使用单向 Noise 模式 "N"，采用 ECIES-X25519 临时-静态 DH 和 HKDF，
ChaCha20/Poly1305 AEAD 以实现前向保密、完整性和认证。
Alice 是隧道构建请求者。隧道中的每个跳点是 Bob。

(Payload Security Properties)

  ```text

N:                      Authentication   Confidentiality
    -> e, es                  0                2

    认证: 无（0）。
    此载荷可能由任何方发送，包括活跃攻击者。

    机密性: 2.
    加密到已知接收者，仅对发送者泄露前向保密，易受重放攻击。
    此载荷仅根据涉及接收者的静态密钥对的 DH 进行加密。
    如果接收者的静态私钥被泄露，即使是在日后，此载荷也可以被解密。
    由于接收者没有提供临时贡献，此消息也可能被重放。

    “e”: Alice 生成一个新的临时密钥对并将其存储在 e 变量中，清楚地将临时公钥写入消息缓冲区，并将公钥与旧 h 一起进行哈希以派生出新的 h。

    “es”: 在 Alice 的临时密钥对和 Bob 的静态密钥对之间执行 DH。
          结果与旧 ck 一起进行哈希以派生新的 ck 和 k，并将 n 设为 0。




  ```



### 回复加密

构建回复记录由跳点创建者创建并以对称方式加密给创建者。
回复记录的这种对称加密目前是带有前置 SHA-256 校验和的 AES。
这个设计不是前向保密的。

新设计将使用 ChaCha20/Poly1305 AEAD 以实现完整性和认证。


### 理由

请求中的临时公钥不需要用 AES 或 Elligator2 混淆。只有上一个跳点能看到它，而该跳点知道下一个跳点是 ECIES。

回复记录不需要完全的非对称加密和另一个 DH。



## 规格



### 构建请求记录

对于兼容性，ElGamal 和 ECIES 的加密 BuildRequestRecords 均为 528 字节。


请求记录未加密（ElGamal）
```````````````````````````````````````

作为参考，这是从 [I2NP](/en/docs/spec/i2np/) 中取来的 ElGamal 路由器的隧道 BuildRequestRecord 的当前规格。
未加密的数据在加密前被前置一个非零字节和数据的 SHA-256 哈希， 如 [Cryptography](/en/docs/spec/cryptography/) 中定义。

所有字段都是大端。

未加密大小：222 字节

  ```dataspec


bytes     0-3: 作为消息接收隧道 ID，非零
  bytes    4-35: 本地路由器标识哈希
  bytes   36-39: 下一个隧道 ID，非零
  bytes   40-71: 下一个路由器标识哈希
  bytes  72-103: AES-256 隧道层密钥
  bytes 104-135: AES-256 隧道 IV 密钥
  bytes 136-167: AES-256 回复密钥
  bytes 168-183: AES-256 回复 IV
  byte      184: 标志
  bytes 185-188: 请求时间（自纪元开始计算的小时数，向下取整）
  bytes 189-192: 下一个消息 ID
  bytes 193-221: 未解释 / 随机填充




  ```


请求记录加密（ElGamal）
`````````````````````````````````````

作为参考，这是从 [I2NP](/en/docs/spec/i2np/) 中取来的 ElGamal 路由器的隧道 BuildRequestRecord 的当前规格。

加密大小：528 字节

  ```dataspec


bytes    0-15: 跳点截断的标识哈希
  bytes  16-528: ElGamal 加密的 BuildRequestRecord




  ```




请求记录未加密（ECIES）
```````````````````````````````````````

这是为 ECIES-X25519 路由器提议的隧道 BuildRequestRecord 规格。
更改摘要：

- 移除未使用的 32 字节路由器哈希
- 将请求时间从小时改为分钟
- 添加到期字段以用于未来的可变隧道时间
- 为标志增加更多空间
- 添加更多的构建选项映射
- AES-256 回复密钥和 IV 不用于跳点自己的回复记录
- 未加密的记录更长，因为加密开销较少

请求记录不包含任何 ChaCha 回复密钥。
这些密钥是从 KDF 中派生的。见下文。

所有字段是大端的。

未加密大小：464 字节

  ```dataspec


bytes     0-3: 作为消息接收隧道 ID，非零
  bytes     4-7: 下一个隧道 ID，非零
  bytes    8-39: 下一个路由器标识哈希
  bytes   40-71: AES-256 隧道层密钥
  bytes  72-103: AES-256 隧道 IV 密钥
  bytes 104-135: AES-256 回复密钥
  bytes 136-151: AES-256 回复 IV
  byte      152: 标志
  bytes 153-155: 更多标志，未使用，为了兼容性设置为 0
  bytes 156-159: 自纪元以来（向下取整）的请求时间（分钟）
  bytes 160-163: 自创建以来（秒）的请求到期
  bytes 164-167: 下一个消息 ID
  bytes   168-x: 隧道构建选项（映射）
  bytes     x-x: 其他数据，如由标志或选项暗示
  bytes   x-463: 随机填充




  ```

标志字段与 [Tunnel-Creation](/en/docs/spec/tunnel-creation/) 中定义的相同，包含以下内容：

 位次序：76543210（位 7 是 MSB）
 位 7: 如果设置，允许来自任何人的消息
 位 6: 如果设置，允许向任何人发消息，并将回复发送到
        指定的下一个跳点的隧道构建回复消息中
 位 5-0: 未定义，必须设置为 0，以便与未来选项兼容

位 7 表示该跳点将成为入站网关（IBGW）。位 6 表示该跳点将成为出站端点（OBEP）。如果两个位都没有设置，该跳点将成为一个中间参与者。两者不能同时设置。

请求到期是用于未来的可变隧道持续时间。
目前，唯一支持的值是 600（10 分钟）。

隧道构建选项是 [Common](/en/docs/spec/common-structures/) 中定义的映射结构。
这是用于未来用途。目前未定义任何选项。
如果 Mapping 结构为空，则为两个字节 0x00 0x00。
映射（包括长度字段）的最大大小为 296 字节，
映射长度字段的最大值为 294。




请求记录加密（ECIES）
`````````````````````````````````````

所有字段都是大端的，除了小端的临时公钥。

加密大小：528 字节

  ```dataspec


bytes    0-15: 跳点截断的标识哈希
  bytes   16-47: 发送者的临时 X25519 公钥
  bytes  48-511: ChaCha20 加密的 BuildRequestRecord
  bytes 512-527: Poly1305 MAC




  ```



### 构建回复记录

对于兼容性，ElGamal 和 ECIES 的加密 BuildReplyRecords 均为 528 字节。


回复记录未加密（ElGamal）
`````````````````````````````````````
ElGamal 回复被 AES 加密。

所有字段都是大端的。

未加密大小：528 字节

  ```dataspec


bytes   0-31: 字节 32-527 的 SHA-256 校验和
  bytes 32-526: 随机数据
  byte     527: 回复

  总长度: 528




  ```


回复记录未加密（ECIES）
`````````````````````````````````````
这是为 ECIES-X25519 路由器提议的隧道 BuildReplyRecord 规格。
更改摘要：

- 添加构建回复选项映射
- 未加密的记录更长，因为加密开销较少

ECIES 回复通过 ChaCha20/Poly1305 加密。

所有字段都是大端的。

未加密大小：512 字节

  ```dataspec


bytes    0-x: 隧道构建回复选项（映射）
  bytes    x-x: 其他数据，如由选项暗示
  bytes  x-510: 随机填充
  byte     511: 回复字节




  ```

隧道构建回复选项是 [Common](/en/docs/spec/common-structures/) 中定义的映射结构。
这是用于未来用途。目前未定义任何选项。
如果 Mapping 结构为空，则为两个字节 0x00 0x00。
映射（包括长度字段）的最大大小为 511 字节，
映射长度字段的最大值为 509。

回复字节是一个以下值
如 [Tunnel-Creation](/en/docs/spec/tunnel-creation/) 中定义，以避免指纹：

- 0x00 (接受)
- 30 (TUNNEL_REJECT_BANDWIDTH)


回复记录加密（ECIES）
```````````````````````````````````

加密大小：528 字节

  ```dataspec


bytes   0-511: ChaCha20 加密的 BuildReplyRecord
  bytes 512-527: Poly1305 MAC




  ```

在完全过渡到 ECIES 记录后，范围填充规则与请求记录相同。


### 记录的对称加密

混合隧道是允许的，并且在从 ElGamal 过渡到 ECIES 时是必要的。
在过渡期间，将有越来越多的路由器依赖于 ECIES 密钥。

对称加密预处理将采用相同方式运行：

- “加密”：

  - 密码以解密模式运行
  - 请求记录是预先解密的（隐藏加密的请求记录）

- “解密”：

  - 密码以加密模式运行
  - 请求记录通过参与跳点加密（揭示下一个明文请求记录）

- ChaCha20 没有“模式”，所以只需运行三次：

  - 在预处理时一次
  - 跳点时一次
  - 回复后期处理时一次

当使用混合隧道时，隧道创建者需要根据当前和上一个跳点的加密类型
来基于结构化地加密 BuildRequestRecord。

每个跳点将使用自己的加密类型来加密 BuildReplyRecords，
以及 VariableTunnelBuildMessage (VTBM) 中的其他记录。

在回复路径上，端点（发送者）将需要撤销[多重加密](https://en.wikipedia.org/wiki/Multiple_encryption)，使用每个跳点的回复密钥。

作为一个清楚的示例，让我们看看一个 ECIES 被 ElGamal 包围的出站隧道：

- 发送者 (OBGW) -> ElGamal (H1) -> ECIES (H2) -> ElGamal (H3)

所有 BuildRequestRecords 都处于（使用 ElGamal 或 ECIES 的）加密状态。

当使用时，AES256/CBC 密码仍然用于每个记录，而不是在多个记录之间链接。

同样，ChaCha20 将用于加密每个记录，而不是在整个 VTBM 上流动。

请求记录由发送者 (OBGW) 预处理：

- H3 的记录被“加密”使用：

  - H2 的回复密钥（ChaCha20）
  - H1 的回复密钥（AES256/CBC）

- H2 的记录被“加密”使用：

  - H1 的回复密钥（AES256/CBC）

- H1 的记录无对称加密

只有 H2 检查回复加密标志，并看到其后跟 AES256/CBC。

经过每个跳点处理后，记录处于“解密”状态：

- H3 的记录被“解密”使用：

  - H3 的回复密钥（AES256/CBC）

- H2 的记录被“解密”使用：

  - H3 的回复密钥（AES256/CBC）
  - H2 的回复密钥（ChaCha20-Poly1305）

- H1 的记录被“解密”使用：

  - H3 的回复密钥（AES256/CBC）
  - H2 的回复密钥（ChaCha20）
  - H1 的回复密钥（AES256/CBC）

隧道创建者，即入站端点 (IBEP)，对回复进行后处理：

- H3 的记录被“加密”使用：

  - H3 的回复密钥（AES256/CBC）

- H2 的记录被“加密”使用：

  - H3 的回复密钥（AES256/CBC）
  - H2 的回复密钥（ChaCha20-Poly1305）

- H1 的记录被“加密”使用：

  - H3 的回复密钥（AES256/CBC）
  - H2 的回复密钥（ChaCha20）
  - H1 的回复密钥（AES256/CBC）


### 请求记录密钥（ECIES）

这些密钥在 ElGamal BuildRequestRecords 中是显式包含的。
对于 ECIES BuildRequestRecords，隧道密钥和 AES 回复密钥被包含，
但 ChaCha 回复密钥是从 DH 交换中派生的。
见 [Prop156](/en/proposals/156-ecies-routers/) 了解路由器静态 ECIES 密钥的详细信息。

以下描述了如何派生以前在请求记录中传输的密钥。


初始 ck 和 h 的 KDF
````````````````````````

这是 [NOISE](https://noiseprotocol.org/noise.html) 模式 "N" 的标准，具有标准协议名。

  ```text

这是“e”消息模式：

  // 定义 protocol_name。
  设置协议名称 = "Noise_N_25519_ChaChaPoly_SHA256"
  （31 字节，US-ASCII 编码，无 NULL 终止）。

  // 定义哈希 h = 32 字节
  // 填充到 32 字节。由于不超过 32 字节，因此请勿对其进行哈希处理。
  h = protocol_name || 0

  定义 ck = 32 字节链接密钥。将 h 数据复制到 ck。
  设链密钥 = h

  // MixHash(null prologue)
  h = SHA256(h);

  // 自此之后，所有路由器都可以预先计算。




  ```


请求记录的 KDF
````````````````````````

ElGamal 隧道创建者为隧道中的每个 ECIES 跳点生成一个临时 X25519 密钥对，
并使用上面的方案加密其 BuildRequestRecord。
ElGamal 隧道创建者将使用此规范之前的方案加密到 ElGamal 跳点。

ECIES 隧道创建者需要使用
[Tunnel-Creation](/en/docs/spec/tunnel-creation/) 中定义的方案来加密到每个 ElGamal 跳点的公钥。 ECIES 隧道创建者将使用上述方案加密到 ECIES 跳点。

这意味着隧道跳点将只会看到来自其相同加密类型的加密记录。

对于 ElGamal 和 ECIES 隧道创建者，他们将为加密到 ECIES 跳点的每个跳点生成唯一的临时 X25519 密钥对。

**重要**：
临时密钥必须在每个 ECIES 跳点和每个构建记录中唯一。
未能使用唯一的密钥将为合谋的跳点打开一个攻击向量，以确认它们处在同一个隧道中。

  ```dataspec


// 每个跳点的 X25519 静态密钥对（hesk, hepk）来自路由器身份
  hesk = GENERATE_PRIVATE()
  hepk = DERIVE_PUBLIC(hesk)

  // MixHash(hepk)
  // || 表示追加
  h = SHA256(h || hepk);

  // 自此之后，每个路由器对于所有传入构建请求都可以预先计算

  // 发送者为 VTBM 中的每个 ECIES 跳点生成一个 X25519 临时密钥对（sesk, sepk）
  sesk = GENERATE_PRIVATE()
  sepk = DERIVE_PUBLIC(sesk)

  // MixHash(sepk)
  h = SHA256(h || sepk);

  结束“e”消息模式。

  这是“es”消息模式：

  // Noise es
  // 发送方执行 X25519 DH，使用 Hop 的静态公钥。
  // 每个跳点，找到带有它们截短身份哈希的记录，
  // 并提取加密记录前面的发送者的临时密钥。
  sharedSecret = DH(sesk, hepk) = DH(hesk, sepk)

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // AEAD 参数加密/解密
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  // 保存以供回复记录 KDF 使用
  chainKey = keydata[0:31]

  // AEAD 参数
  k = keydata[32:63]
  n = 0
  plaintext = 464 字节构建请求记录
  ad = h
  ciphertext = ENCRYPT(k, n, plaintext, ad)

  结束“es”消息模式。

  // MixHash(ciphertext)
  // 保存以供回复记录 KDF 使用
  h = SHA256(h || ciphertext)




  ```

``replyKey``、``layerKey`` 和 ``layerIV`` 仍必须包含在 ElGamal 记录中，
并且可以随机生成。


### 请求记录加密（ElGamal）

如 [Tunnel-Creation](/en/docs/spec/tunnel-creation/) 中定义。
ElGamal 跳点的加密没有更改。




### 回复记录加密（ECIES）

回复记录是通过 ChaCha20/Poly1305 加密的。

  ```dataspec


// AEAD 参数
  k = 构建请求中的 chainkey
  n = 0
  plaintext = 512 字节构建回复记录
  ad = 构建请求中的 h

  ciphertext = ENCRYPT(k, n, plaintext, ad)




  ```



### 回复记录加密（ElGamal）

如 [Tunnel-Creation](/en/docs/spec/tunnel-creation/) 中定义。
ElGamal 跳点的加密没有更改。



### 安全分析

ElGamal 不为隧道构建消息提供前向保密性。

AES256/CBC 处境稍好些，只是易受一个理论上的已知明文`双经验族`攻击的影响。

唯一已知的针对 AES256/CBC 的实际攻击是填充 oracle 攻击，如果攻击者知道 IV 。

攻击者需要破解下一跳的 ElGamal 加密才能获取 AES256/CBC 密钥信息（回复密钥和 IV）。

相比之下，ElGamal 的 CPU 需求要比 ECIES 高得多，这可能导致资源耗尽。

ECIES，每个 BuildRequestRecord 或 VariableTunnelBuildMessage 使用新临时密钥提供前向保密。

ChaCha20Poly1305 提供 AEAD 加密，允许接收者在尝试解密前验证消息完整性。


## 理由

此设计最大程度地重用现有的加密原语、协议和代码。
此设计将风险降到最低。




## 实施注释

* 较旧的路由器不检查跳点的加密类型，将发送 ElGamal 加密的
  记录。有些最近的路由器存在缺陷，将发送各种形式的不良记录。
  实现者应在可能的情况下，在 DH 操作
  之前检测并拒绝这些记录，以减少 CPU 使用。


## 问题



## 迁移

请参阅 [Prop156](/en/proposals/156-ecies-routers/)。



