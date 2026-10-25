---
title: "Tunnel 创建规范（ElGamal）"
description: "基于传统 ElGamal 的 tunnel 构建规范，已被 X25519 替代"
slug: "elgamal-tunnel-creation"
aliases:
  - "/zh/tunnel-alt-creation"
  - "/zh/tunnel-alt-creation/"
lastUpdated: "2025-05"
accurateFor: "0.9.66"
---

## 概述 {#tunnelcreate-overview}

注意：已废弃 - 这是 ElGamal tunnel 构建规范。请参阅 [X25519 tunnel 构建规范](/docs/specs/tunnel-creation-ecies) 了解当前方法。

本文档详细说明了使用"非交互式伸缩"方法创建tunnel时所用的加密tunnel构建消息的细节。有关该过程的概述，包括节点选择和排序方法，请参见tunnel构建文档[TUNNEL-IMPL](/docs/specs/tunnel-implementation)。

tunnel 创建是通过沿着 tunnel 中对等节点路径传递的单个消息来完成的，该消息在传输过程中被就地重写，然后传输回 tunnel 创建者。这个单一的 tunnel 消息由可变数量的记录（最多8个）组成 - tunnel 中每个潜在的对等节点对应一个记录。单个记录使用非对称加密（ElGamal [CRYPTO-ELG](/docs/specs/cryptography#elgamal)）进行加密，只能由路径上的特定对等节点读取，同时在每个跳跃点添加额外的对称加密层（AES [CRYPTO-AES](/docs/specs/cryptography#AES)），以便仅在适当的时间暴露非对称加密的记录。

### 记录数量 {#number}

不是所有记录都必须包含有效数据。例如，3跳tunnel的构建消息可能包含更多记录来向参与者隐藏tunnel的实际长度。有两种构建消息类型。原始的Tunnel Build Message ([TBM](/docs/specs/i2np#msg-tunnelbuild)) 包含8个记录，这对于任何实际的tunnel长度都绰绰有余。较新的Variable Tunnel Build Message ([VTBM](/docs/specs/i2np#msg-variabletunnelbuild)) 包含1到8个记录。发起者可以在消息大小与所需的tunnel长度混淆量之间进行权衡。

在当前网络中，大多数tunnel长度为2或3跳。当前实现使用5记录VTBM来构建4跳或更少的tunnel，对于更长的tunnel则使用8记录TBM。5记录VTBM（分片后可以适配三个1KB的tunnel消息）减少了网络流量并提高了构建成功率，因为较小的消息不太容易被丢弃。

回复消息必须与构建消息具有相同的类型和长度。

### 请求记录规范 {#tunnelcreate-requestrecord}

同样在 I2NP 规范 [BRR](/docs/specs/i2np#struct-buildrequestrecord) 中有详细说明。

记录的明文，仅对被询问的跳点可见：

```
bytes     0-3: tunnel ID to receive messages as, nonzero
bytes    4-35: local router identity hash
bytes   36-39: next tunnel ID, nonzero
bytes   40-71: next router identity hash
bytes  72-103: AES-256 tunnel layer key
bytes 104-135: AES-256 tunnel IV key
bytes 136-167: AES-256 reply key
bytes 168-183: AES-256 reply IV
byte      184: flags
bytes 185-188: request time (in hours since the epoch, rounded down)
bytes 189-192: next message ID
bytes 193-221: uninterpreted / random padding
```
下一个tunnel ID和下一个router身份哈希字段用于指定tunnel中的下一跳，不过对于出站tunnel端点，它们指定重写后的tunnel创建回复消息应该发送到哪里。此外，下一个消息ID指定消息（或回复）应该使用的消息ID。

tunnel 层密钥、tunnel IV 密钥、回复密钥和回复 IV 都是由创建者生成的随机 32 字节值，仅用于此构建请求记录。

flags 字段包含以下内容：

```
Bit order: 76543210 (bit 7 is MSB)
bit 7: if set, allow messages from anyone
bit 6: if set, allow messages to anyone, and send the reply to the
       specified next hop in a Tunnel Build Reply Message
bits 5-0: Undefined, must set to 0 for compatibility with future options
```
位7表示该跳点将是入站网关（IBGW）。位6表示该跳点将是出站端点（OBEP）。如果两个位都未设置，该跳点将是中间参与者。两个位不能同时设置。

#### 请求记录创建

每个跳跃都获得一个随机的非零 Tunnel ID。当前和下一跳的 Tunnel ID 会被填入。每个记录都获得一个随机的 tunnel IV 密钥、回复 IV、层密钥和回复密钥。

#### 请求记录加密 {#encryption}

该明文记录使用跳点的公共加密密钥进行 ElGamal 2048 加密 [CRYPTO-ELG](/docs/specs/cryptography#elgamal)，并格式化为 528 字节记录：

```
bytes   0-15: First 16 bytes of the SHA-256 of the current hop's router identity
bytes 16-527: ElGamal-2048 encrypted request record
```
在512字节的加密记录中，ElGamal数据包含514字节ElGamal加密块[CRYPTO-ELG](/docs/specs/cryptography#elgamal)的第1-256字节和第258-513字节。块中的两个填充字节（位于位置0和257的零字节）被移除。

由于明文使用了完整的字段，因此除了 `SHA256(cleartext) + cleartext` 之外不需要额外的填充。

然后对每个528字节的记录进行迭代加密（使用AES解密，为每个hop使用回复密钥和回复IV），这样router身份只会在相应的hop中以明文形式存在。

### 跳点处理和加密 {#tunnelcreate-hopprocessing}

当一个hop收到TunnelBuildMessage时，它会查看其中包含的记录，寻找以自己的身份哈希（截断为16字节）开头的记录。然后它解密该记录中的ElGamal块并检索受保护的明文。此时，它们通过将AES-256回复密钥输入布隆过滤器来确保tunnel请求不是重复的。重复或无效的请求会被丢弃。未标记当前小时或前一小时（如果刚过整点不久）的记录必须被丢弃。例如，取时间戳中的小时，转换为完整时间，如果它比当前时间落后超过65分钟或提前5分钟，则为无效。布隆过滤器必须持续至少一个小时（加上几分钟以考虑时钟偏差），这样当前小时内未被记录中的小时时间戳检查拒绝的重复记录，将被过滤器拒绝。

在决定是否同意参与 tunnel 后，它们将包含请求的记录替换为加密的回复块。所有其他记录都使用包含的回复密钥和 IV 进行 AES-256 加密 [CRYPTO-AES](/docs/specs/cryptography#AES)。每个记录都使用相同的回复密钥和回复 IV 分别进行 AES/CBC 加密。CBC 模式不会在记录之间继续（链接）。

每个跳点只知道自己的响应。如果它同意，它将维护该 tunnel 直到过期，即使不会被使用，因为它无法知道所有其他跳点是否同意。

#### 回复记录规范 {#tunnelcreate-replyrecord}

当前跳点读取其记录后，会用回复记录替换该记录，说明其是否同意参与该tunnel，如果不同意，则会分类说明拒绝的原因。这只是一个1字节的值，0x0表示同意参与该tunnel，更高的值表示更高级别的拒绝。

定义了以下拒绝代码：

- TUNNEL_REJECT_PROBABALISTIC_REJECT = 10
- TUNNEL_REJECT_TRANSIENT_OVERLOAD = 20
- TUNNEL_REJECT_BANDWIDTH = 30
- TUNNEL_REJECT_CRIT = 50

为了向对等节点隐藏其他原因（如 router 关闭），当前实现对几乎所有拒绝都使用 TUNNEL_REJECT_BANDWIDTH。

回复使用加密块中传递的AES会话密钥进行加密，并用495字节的随机数据填充以达到完整的记录大小。填充数据放置在状态字节之前：

```
AES-256-CBC(SHA-256(padding+status) + padding + status, key, IV)

bytes   0-31 : SHA-256 of bytes 32-527
bytes 32-526 : Random padding
byte 527     : Reply value
```
这在 I2NP 规范 [BRR](/docs/specs/i2np#struct-buildrequestrecord) 中也有描述。

### Tunnel 构建消息准备 {#tunnelcreate-requestpreparation}

构建新的 Tunnel Build Message 时，必须首先构建所有的 Build Request Records，并使用 ElGamal [CRYPTO-ELG](/docs/specs/cryptography#elgamal) 进行非对称加密。然后使用路径中较早跳点的回复密钥和 IV，通过 AES [CRYPTO-AES](/docs/specs/cryptography#AES) 对每个记录进行预先解密。解密应按相反顺序运行，以便非对称加密的数据在前一跳加密后能在正确的跳点处以明文形式显示。

创建者会用随机数据填充那些个人请求不需要的多余记录。

### Tunnel Build Message Delivery {#tunnelcreate-requestdelivery}

对于出站tunnel，传递是直接从tunnel创建者到第一跳完成的，将TunnelBuildMessage打包，就好像创建者只是tunnel中的另一跳一样。对于入站tunnel，传递是通过现有的出站tunnel完成的。出站tunnel通常来自与正在构建的新tunnel相同的池。如果该池中没有可用的出站tunnel，则使用出站探索tunnel。在启动时，当还不存在出站探索tunnel时，使用虚假的0跳出站tunnel。

### Tunnel Build Message Endpoint Handling {#tunnelcreate-endpointhandling}

对于出站tunnel的创建，当请求到达出站端点时（由"允许向任何人发送消息"标志确定），该跳点按常规方式处理，加密回复以替代记录并加密所有其他记录，但由于没有"下一跳"来转发TunnelBuildMessage，它会将加密的回复记录放入TunnelBuildReplyMessage ([TBRM](/docs/specs/i2np#msg-tunnelbuildreply)) 或 VariableTunnelBuildReplyMessage ([VTBRM](/docs/specs/i2np#msg-variabletunnelbuildreply)) 中（消息类型和记录数量必须与请求匹配），并将其传递到请求记录中指定的回复tunnel。该回复tunnel将Tunnel Build Reply Message转发回tunnel创建者，就像处理其他任何消息一样 [TUNNEL-OP](/docs/specs/tunnel-implementation#tunnel.operation)。然后tunnel创建者处理它，如下所述。

回复tunnel由创建者按以下方式选择：通常是来自与正在构建的新出站tunnel相同池中的入站tunnel。如果该池中没有可用的入站tunnel，则使用入站探索性tunnel。在启动时，当还不存在入站探索性tunnel时，会使用一个伪造的0跳入站tunnel。

对于创建入站tunnel，当请求到达入站端点（也称为tunnel创建者）时，不需要生成显式的Tunnel Build Reply Message，router会处理每个回复，如下所示。

### Tunnel Build Reply Message Processing {#tunnelcreate-replyprocessing}

为了处理回复记录，创建者只需要使用 tunnel 中每个对等节点之后的每一跳的回复密钥和 IV（按相反顺序），对每个记录单独进行 AES 解密。这样就能显示回复内容，说明它们是否同意参与 tunnel 或拒绝的原因。如果所有节点都同意，tunnel 就被认为已创建并可以立即使用，但如果任何节点拒绝，tunnel 就会被丢弃。

协议和拒绝都会记录在每个对等节点的配置文件 [PEER-SELECTION](/docs/overview/peer-selection) 中，用于未来评估对等节点 tunnel 容量。

## 历史和注释 {#tunnelcreate-notes}

这个策略是在I2P邮件列表上Michael Rogers、Matthew Toseland (toad)和jrandom之间关于前驱攻击的讨论中提出的。请参见[TUNBUILD-SUMMARY](http://zzz.i2p/archive/2005-10/msg00138.html)、[TUNBUILD-REASONING](http://zzz.i2p/archive/2005-10/msg00129.html)。它在2006年2月16日的0.6.1.10版本中引入，这是I2P最后一次进行非向后兼容的更改。

注意事项：

- 此设计无法防止tunnel内的两个恶意节点对一个或多个请求或回复记录进行标记来检测它们是否在同一个tunnel中，但这样做可以被tunnel创建者在读取回复时检测到，从而导致该tunnel被标记为无效。

- 这种设计在非对称加密部分不包含工作量证明，不过16字节的身份哈希可以减半，后半部分用成本高达2^64的hashcash函数替代。

- 仅凭这种设计无法防止 tunnel 内的两个恶意节点使用时序信息来确定它们是否在同一个 tunnel 中。使用批处理和同步的请求传递可能会有所帮助（将请求批量处理并在（ntp同步的）分钟时刻发送）。然而，这样做会让节点通过延迟请求并在 tunnel 后续位置检测到延迟来"标记"请求，不过也许可以丢弃那些未在小时间窗口内传递的请求（尽管这样做需要高度的时钟同步）。或者，也许各个跳点可以在转发请求前注入随机延迟？

- 是否有任何非致命的方法来标记请求？

- 使用一小时分辨率的时间戳来防止重放攻击。此约束在 0.9.16 版本之前并未强制执行。

## 未来工作 {#future}

- 在当前实现中，originator 为自己留下一个空记录。因此，n 个记录的消息只能构建 n-1 跳的 tunnel。这对于入站 tunnel 似乎是必要的（倒数第二跳可以看到下一跳的哈希前缀），但对于出站 tunnel 则不然。这需要进一步研究和验证。如果可以在不损害匿名性的情况下使用剩余记录，我们应该这样做。

- 对上述注释中描述的可能标记攻击和时序攻击进行进一步分析。

- 仅使用 VTBM；不要选择不支持它的旧节点。

- Build Request Record 不指定 tunnel 生存时间或过期时间；
  每个跳点在 10 分钟后使 tunnel 过期，这是一个网络范围内的
  硬编码常量。我们可以使用标志字段中的一个位，并从填充中取出 4（或 8）
  字节来指定生存时间或过期时间。请求者
  只有在所有参与者都支持此选项时才会指定此选项。

## 参考资料 {#ref}

- [BRR](/docs/specs/i2np#struct-buildrequestrecord) - Build Request Record
- [CRYPTO-AES](/docs/specs/cryptography#AES) - AES Encryption
- [CRYPTO-ELG](/docs/specs/cryptography#elgamal) - ElGamal Encryption
- [HASHING-IT-OUT](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf) - Hashing It Out Paper
- [PEER-SELECTION](/docs/overview/peer-selection) - Peer Selection
- [PREDECESSOR](http://forensics.umass.edu/pubs/wright-tissec.pdf) - Predecessor Attack Paper
- [PREDECESSOR-2008](http://forensics.umass.edu/pubs/wright.tissec.2008.pdf) - Predecessor Attack Paper (2008)
- [TBM](/docs/specs/i2np#msg-tunnelbuild) - Tunnel Build Message
- [TBRM](/docs/specs/i2np#msg-tunnelbuildreply) - Tunnel Build Reply Message
- [TUNBUILD-REASONING](http://zzz.i2p/archive/2005-10/msg00129.html) - Tunnel Build Reasoning
- [TUNBUILD-SUMMARY](http://zzz.i2p/archive/2005-10/msg00138.html) - Tunnel Build Summary
- [TUNNEL-IMPL](/docs/specs/tunnel-implementation) - Tunnel Implementation
- [TUNNEL-OP](/docs/specs/tunnel-implementation#tunnel.operation) - Tunnel Operation
- [VTBM](/docs/specs/i2np#msg-variabletunnelbuild) - Variable Tunnel Build Message
- [VTBRM](/docs/specs/i2np#msg-variabletunnelbuildreply) - Variable Tunnel Build Reply Message
