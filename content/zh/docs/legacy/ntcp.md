---
title: "NTCP（基于NIO的TCP）"
description: "基于传统 Java NIO 的 I2P TCP 传输协议，已被 NTCP2 替代"
slug: "ntcp"
aliases:
  - "/zh/docs/transport/ntcp"
  - "/zh/docs/transport/ntcp/"
  - "/zh/docs/ntcp"
  - "/zh/docs/ntcp/"
  - "/zh/ntcp"
  - "/zh/ntcp/"
lastUpdated: "2021-10"
accurateFor: "0.9.52"
---

已弃用，不再支持。自 0.9.40 2019-05 版本起默认禁用。自 0.9.50 2021-05 版本起移除支持。已被 [NTCP2](/docs/specs/ntcp2) 替代。NTCP 是在 I2P 0.6.1.22 版本中引入的基于 Java NIO 的传输协议。Java NIO（新 I/O）不会遇到旧 TCP 传输协议中每个连接一个线程的问题。从 0.9.8 版本开始支持 NTCP-over-IPv6。

默认情况下，NTCP使用SSU自动检测到的IP/端口。在config.jsp中启用时，SSU会在外部地址变更或防火墙状态变化时通知/重启NTCP。现在您可以在没有静态IP或动态DNS服务的情况下启用入站TCP。

I2P中的NTCP代码相对轻量级（比SSU代码小1/4），因为它使用底层的Java TCP传输来实现可靠传输。

## Router 地址规范 {#ra}

以下属性存储在 netDb 中。

- **传输名称：** NTCP
- **主机：** IP (IPv4 或 IPv6)。
  允许使用简化的 IPv6 地址（带有 "::"）。
  以前允许使用主机名，但自 0.9.32 版本起已弃用。请参阅提案 141。
- **端口：** 1024 - 65535

## NTCP协议规范

### 标准消息格式

建立连接后，NTCP 传输会发送单独的 I2NP 消息，并带有简单的校验和。未加密的消息编码如下：

```
+-------+-------+-------+-------+-------+-------+-------+-------+
| sizeof(data)  |                                               |
+-------+-------+                                               +
|                            data                               |
~                                                               ~
|                                                               |
+                                       +-------+-------+-------+
|                                       |        padding
+-------+-------+-------+-------+-------+-------+-------+-------+
                                | Adler checksum of sz+data+pad |
+-------+-------+-------+-------+-------+-------+-------+-------+
```
然后数据使用 AES/256/CBC 进行加密。加密的会话密钥在建立连接时通过协商确定（使用 Diffie-Hellman 2048 位）。两个 router 之间的建立过程在 EstablishState 类中实现，详细说明如下。AES/256/CBC 加密的 IV 是前一个加密消息的最后 16 个字节。

需要0-15字节的填充来使消息的总长度（包括6个大小和校验和字节）成为16的倍数。当前最大消息大小为16 KB。因此当前最大数据大小为16 KB - 6，即16378字节。最小数据大小为1字节。

### 时间同步消息格式

一种特殊情况是数据大小为0的元数据消息。在这种情况下，未加密的消息编码如下：

```
+-------+-------+-------+-------+-------+-------+-------+-------+
|       0       |      timestamp in seconds     | uninterpreted
+-------+-------+-------+-------+-------+-------+-------+-------+
        uninterpreted           | Adler checksum of bytes 0-11  |
+-------+-------+-------+-------+-------+-------+-------+-------+
```
总长度：16 字节。时间同步消息大约每 15 分钟发送一次。该消息的加密方式与标准消息相同。

### 校验和

标准和时间同步消息使用 [ZLIB 规范](http://tools.ietf.org/html/rfc1950) 中定义的 Adler-32 校验和。

### 空闲超时

空闲超时和连接关闭由各端点自行决定，可能会有所不同。当前实现会在连接数接近配置的最大值时降低超时时间，在连接数较少时提高超时时间。建议的最小超时时间为两分钟或更长，建议的最大超时时间为十分钟或更长。

### RouterInfo 交换

建立连接后，以及此后每30-60分钟，两个router通常应该使用DatabaseStoreMessage交换RouterInfo信息。但是，Alice应该检查队列中的第一条消息是否为DatabaseStoreMessage，以避免发送重复消息；这种情况在连接到floodfill router时经常发生。

### 建立序列

在建立状态中，有一个4阶段的消息序列来交换DH密钥和签名。在前两个消息中进行2048位的Diffie Hellman交换。然后，交换关键数据的签名以确认连接。

```
Alice                   contacts                      Bob
=========================================================
 X+(H(X) xor Bob.identHash)----------------------------->
 <----------------------------------------Y+E(H(X+Y)+tsB+padding, sk, Y[239:255])
 E(sz+Alice.identity+tsA+padding+S(X+Y+Bob.identHash+tsA+tsB), sk, hX_xor_Bob.identHash[16:31])--->
 <----------------------E(S(X+Y+Alice.identHash+tsA+tsB)+padding, sk, prev)
```
```
  Legend:
    X, Y: 256 byte DH public keys
    H(): 32 byte SHA256 Hash
    E(data, session key, IV): AES256 Encrypt
    S(): Signature
    tsA, tsB: timestamps (4 bytes, seconds since epoch)
    sk: 32 byte Session key
    sz: 2 byte size of Alice identity to follow
```
#### DH 密钥交换 {#DH}

初始的2048位DH密钥交换使用与I2P的[ElGamal加密](/docs/specs/cryptography#elgamal)相同的共享素数(p)和生成元(g)。

DH密钥交换包含多个步骤，如下所示。这些步骤与I2P router之间发送的消息的对应关系以粗体标出。

1. Alice 生成一个秘密整数 x。然后她计算 `X = g^x mod p`。
2. Alice 将 X 发送给 Bob **（消息 1）**。
3. Bob 生成一个秘密整数 y。然后他计算 `Y = g^y mod p`。
4. Bob 将 Y 发送给 Alice。**（消息 2）**
5. Alice 现在可以计算 `sessionKey = Y^x mod p`。
6. Bob 现在可以计算 `sessionKey = X^y mod p`。
7. Alice 和 Bob 现在都拥有共享密钥 `sessionKey = g^(x*y) mod p`。

然后使用 sessionKey 在 **Message 3** 和 **Message 4** 中交换身份。DH 交换的指数（x 和 y）长度在[密码学页面](/docs/specs/cryptography#exponent)中有文档记录。

#### 会话密钥详细信息

32字节的会话密钥创建如下：

1. 获取交换的 DH 密钥，表示为正的最小长度 BigInteger 字节数组（二进制补码大端序）
2. 如果最高有效位为 1（即 array[0] & 0x80 != 0），则在前面添加一个 0x00 字节，如 Java 的 BigInteger.toByteArray() 表示法
3. 如果该字节数组大于或等于 32 字节，则使用前面（最高有效位）的 32 字节
4. 如果该字节数组小于 32 字节，则追加 0x00 字节以扩展到 32 字节。*（几乎不可能发生）*

#### 消息 1（会话请求）

这是 DH 请求。Alice 已经拥有 Bob 的 [Router Identity](/docs/specs/common-structures#struct_RouterIdentity)、IP 地址和端口，这些信息包含在他发布到 [network database](/docs/overview/network-database) 的 [Router Info](/docs/specs/common-structures#struct_RouterInfo) 中。Alice 向 Bob 发送：

```
 X+(H(X) xor Bob.identHash)----------------------------->

    Size: 288 bytes
```
目录：

```
 +----+----+----+----+----+----+----+----+
 |         X, as calculated from DH      |
 +                                       +
 |                                       |
 ~               .   .   .               ~
 |                                       |
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |              HXxorHI                  |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +----+----+----+----+----+----+----+----+

  X :: 256 byte X from Diffie Hellman

  HXxorHI :: SHA256 Hash(X) xored with SHA256 Hash(Bob's RouterIdentity)
             (32 bytes)
```
**注意事项：**

- Bob 使用自己的 router hash 验证 HXxorHI。如果验证失败，说明 Alice 联系了错误的 router，Bob 会断开连接。

#### 消息 2 (会话已创建)

这是 DH 回复。Bob 发送给 Alice：

```
 <----------------------------------------Y+E(H(X+Y)+tsB+padding, sk, Y[239:255])

    Size: 304 bytes
```
未加密内容：

```
 +----+----+----+----+----+----+----+----+
 |         Y as calculated from DH       |
 +                                       +
 |                                       |
 ~               .   .   .               ~
 |                                       |
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |              HXY                      |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +----+----+----+----+----+----+----+----+
 |        tsB        |     padding       |
 +----+----+----+----+                   +
 |                                       |
 +----+----+----+----+----+----+----+----+

  Y :: 256 byte Y from Diffie Hellman

  HXY :: SHA256 Hash(X concatenated with Y)
         (32 bytes)

  tsB :: 4 byte timestamp (seconds since the epoch)

  padding :: 12 bytes random data
```
加密内容：

```
 +----+----+----+----+----+----+----+----+
 |         Y as calculated from DH       |
 +                                       +
 |                                       |
 ~               .   .   .               ~
 |                                       |
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |             encrypted data            |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +----+----+----+----+----+----+----+----+

  Y: 256 byte Y from Diffie Hellman

  encrypted data: 48 bytes AES encrypted using the DH session key and
                  the last 16 bytes of Y as the IV
```
**注意事项：**

- 如果根据 tsB 计算得出与 Bob 的时钟偏差过大，Alice 可能会断开连接。

#### 消息 3 (会话确认 A)

这包含了 Alice 的 router 身份信息，以及关键数据的签名。Alice 发送给 Bob：

```
 E(sz+Alice.identity+tsA+padding+S(X+Y+Bob.identHash+tsA+tsB), sk, hX_xor_Bob.identHash[16:31])--->

    Size: 448 bytes (typ. for 387 byte identity and DSA signature), see notes below
```
未加密内容：

```
 +----+----+----+----+----+----+----+----+
 |   sz    | Alice's Router Identity     |
 +----+----+                             +
 |                                       |
 ~               .   .   .               ~
 |                                       |
 +                        +----+----+----+
 |                        |     tsA
 +----+----+----+----+----+----+----+----+
      |             padding              |
 +----+                                  +
 |                                       |
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |              signature                |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +----+----+----+----+----+----+----+----+

  sz :: 2 byte size of Alice's router identity to follow (387+)

  ident :: Alice's 387+ byte RouterIdentity

  tsA :: 4 byte timestamp (seconds since the epoch)

  padding :: 0-15 bytes random data

  signature :: the Signature of the following concatenated data:
               X, Y, Bob's RouterIdentity, tsA, tsB.
               Alice signs it with the SigningPrivateKey associated with
               the SigningPublicKey in her RouterIdentity
```
加密内容：

```
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |             encrypted data            |
 ~               .   .   .               ~
 |                                       |
 +----+----+----+----+----+----+----+----+

  encrypted data: 448 bytes AES encrypted using the DH session key and
                  the last 16 bytes of HXxorHI (i.e., the last 16 bytes
                  of message #1) as the IV
                  448 is the typical length, but it could be longer, see below.
```
**注意事项：**

- Bob 验证签名，如果验证失败，则断开连接。
- 如果使用 tsA 计算出的与 Alice 的时钟偏差过大，Bob 可能会断开连接。
- Alice 将使用此消息加密内容的最后 16 个字节作为下一条消息的 IV。
- 直到 0.9.15 版本，router identity 始终为 387 字节，签名始终为 40 字节的 DSA 签名，填充始终为 15 字节。从 0.9.16 版本开始，router identity 可能长于 387 字节，签名类型和长度由 Alice 的 [Router Identity](/docs/specs/common-structures#struct_RouterIdentity) 中 [Signing Public Key](/docs/specs/common-structures#type_SigningPublicKey) 的类型决定。填充根据需要进行，使整个未加密内容的长度为 16 字节的倍数。
- 无法在不部分解密消息以读取 Router Identity 的情况下确定消息的总长度。由于 Router Identity 的最小长度为 387 字节，最小签名长度为 40（对于 DSA），因此最小总消息大小为 2 + 387 + 4 +（签名长度）+（填充到 16 字节），或者对于 DSA 为 2 + 387 + 4 + 40 + 15 = 448。接收方可以在解密之前读取这个最小量来确定实际的 Router Identity 长度。对于 Router Identity 中的小型证书，这可能就是整个消息，消息中不会有更多字节需要额外的解密操作。

#### 消息 4 (会话确认 B)

这是关键数据的签名。Bob 发送给 Alice：

```
 <----------------------E(S(X+Y+Alice.identHash+tsA+tsB)+padding, sk, prev)

    Size: 48 bytes (typ. for DSA signature), see notes below
```
未加密内容：

```
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |              signature                |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +----+----+----+----+----+----+----+----+
 |               padding                 |
 +----+----+----+----+----+----+----+----+

  signature :: the Signature of the following concatenated data:
               X, Y, Alice's RouterIdentity, tsA, tsB.
               Bob signs it with the SigningPrivateKey associated with
               the SigningPublicKey in his RouterIdentity

  padding :: 0-15 bytes random data
```
加密内容：

```
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |             encrypted data            |
 ~               .   .   .               ~
 |                                       |
 +----+----+----+----+----+----+----+----+

  encrypted data: Data AES encrypted using the DH session key and
                  the last 16 bytes of the encrypted contents of message #2 as the IV
                  48 bytes for a DSA signature, may vary for other signature types
```
**注意：**

- Alice 验证签名，如果失败，则断开连接。
- Bob 将使用此消息加密内容的最后 16 字节作为下一条消息的 IV。
- 在 0.9.15 版本之前，签名始终是 40 字节的 DSA 签名，填充始终是 8 字节。从 0.9.16 版本开始，签名类型和长度由 Bob 的 [Router Identity](/docs/specs/common-structures#struct_RouterIdentity) 中的 [Signing Public Key](/docs/specs/common-structures#type_SigningPublicKey) 类型隐含确定。填充根据需要调整，使整个未加密内容的长度为 16 字节的倍数。

#### 建立之后

连接建立完成，可以开始交换标准消息或时间同步消息。所有后续消息都使用协商的DH会话密钥进行AES加密。Alice将使用消息#3加密内容的最后16字节作为下一个IV。Bob将使用消息#4加密内容的最后16字节作为下一个IV。

### 检查连接消息

另外，当 Bob 收到连接时，它可能是一个检查连接（也许是因为 Bob 请求某人验证他的监听器而触发的）。检查连接目前没有被使用。但是，为了记录在案，检查连接的格式如下。检查信息连接将接收包含以下内容的 256 字节：

- 32 字节未解释的忽略数据
- 1 字节大小
- 构成本地 router IP 地址的相应字节数（由远程端到达）
- 本地 router 被到达的 2 字节端口号
- 远程端已知的 4 字节 i2p 网络时间（自纪元以来的秒数）
- 未解释的填充数据，直到第 223 字节
- 本地 router 身份哈希与第 32 字节到第 223 字节的 SHA256 的异或

从 0.9.12 版本开始，检查连接功能已完全禁用。

## 讨论

现在在 [NTCP 讨论页面](/docs/discussions/ntcp)。

## 未来工作 {#future}

- 最大消息大小应增加到大约 32 KB。

- 一组固定的数据包大小可能适合进一步向外部对手隐藏数据分片，但在此之前，tunnel、garlic 和端到端填充对于大多数需求应该是足够的。
  但是，目前没有超出下一个 16 字节边界的填充规定，无法创建有限数量的消息大小。

- 应该比较 NTCP 和 SSU 的内存利用率（包括内核的内存使用）。

- 建立消息是否可以通过某种方式进行随机填充，以阻挠基于初始数据包大小来识别 I2P 流量？
