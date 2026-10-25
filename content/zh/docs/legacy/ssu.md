---
title: "SSU（安全半可靠UDP）"
description: "原始UDP传输协议规范（已弃用，被SSU2替代）"
slug: "ssu"
aliases:
  - "/zh/docs/transport/ssu"
  - "/zh/docs/transport/ssu/"
  - "/zh/docs/transports/ssu"
  - "/zh/docs/transports/ssu/"
  - "/zh/docs/specs/ssu-spec"
  - "/zh/docs/specs/ssu-spec/"
category: "传输协议"
lastUpdated: "2024-01"
accurateFor: "0.9.61"
---

## 概述

已弃用 - SSU 已被 SSU2 替代。i2pd 在 2.44.0 版本（API 0.9.56）2022年11月中移除了 SSU 支持。Java I2P 在 2.4.0 版本（API 0.9.61）2023年12月中移除了 SSU 支持。

更多信息请参见 [SSU 概览](/docs/transport/ssu/)。

## DH 密钥交换 {#dh}

初始的2048位DH密钥交换在[SSU密钥页面](/docs/transport/ssu/#keys)中有描述。此交换使用与I2P的[ElGamal加密](/docs/specs/cryptography/#elgamal)相同的共享素数。

## 消息头 {#header}

所有UDP数据报都以16字节的MAC（消息认证码）和16字节的IV（初始化向量）开始，然后是使用适当密钥加密的可变大小载荷。使用的MAC是HMAC-MD5，截断为16字节，而密钥是完整的32字节AES256密钥。MAC的具体构造是以下内容的前16字节：

```
HMAC-MD5(encryptedPayload + IV + (payloadLength ^ protocolVersion ^ ((netid - 2) << 8)), macKey)
```
其中'+'表示追加，'^'表示异或。

IV 为每个数据包随机生成。encryptedPayload 是从标志字节开始的消息的加密版本（先加密后MAC）。MAC 中使用的 payloadLength 是一个 2 字节无符号整数，大端序。注意 protocolVersion 为 0，因此异或操作是无操作。macKey 要么是 introduction key，要么由交换的 DH key 构造（详见下文），具体由下面每个消息指定。

**警告** - 这里使用的 HMAC-MD5-128 是非标准的，详细信息请参见 [HMAC 详细信息](/docs/specs/cryptography/#udp)。

负载本身（即从标志字节开始的消息）使用IV和sessionKey进行AES256/CBC加密，重放防护在其主体内处理，如下所述。

protocolVersion 是一个 2 字节无符号整数，大端序，当前设置为 0。使用不同协议版本的节点将无法与此节点通信，但不使用此标志的早期版本可以通信。

使用 ((netid - 2) << 8) 的异或运算来快速识别跨网络连接。netid 是一个 2 字节无符号整数，大端序，目前设置为 2。自 0.9.42 版本开始。更多信息请参见提案 147。由于当前网络 ID 为 2，这对当前网络来说是无操作的，并且向后兼容。来自测试网络的任何连接都应该有不同的 ID，并且会导致 HMAC 失败。

### HMAC 规范

- 内部填充：0x36...
- 外部填充：0x5C...
- 密钥：32 字节
- 哈希摘要函数：MD5，16 字节
- 块大小：64 字节
- MAC 大小：16 字节
- C 实现示例：
  - [i2pd](https://github.com/PurpleI2P/i2pd) 中的 hmac.h
  - [i2pcpp](http://git.repo.i2p/w/i2pcpp.git) 中的 I2PHMAC.cpp
- Java 实现示例：
  - [I2P](https://github.com/i2p/i2p.i2p) 中的 I2PHMac.java

### 会话密钥详细信息

32字节的会话密钥创建如下：

1. 取得交换的DH密钥，表示为正的最小长度BigInteger字节数组（二进制补码大端序）
2. 如果最高有效位为1（即 array[0] & 0x80 != 0），则在前面添加一个0x00字节，如Java的BigInteger.toByteArray()表示法
3. 如果字节数组大于或等于32字节，则使用前面（最高有效位）的32字节
4. 如果字节数组少于32字节，则追加0x00字节扩展到32字节。*极不可能 - 请参见下面的注释。*

### MAC 密钥详情

32字节的MAC密钥创建如下：

1. 取上述会话密钥详情步骤2中交换的DH密钥字节数组，如有必要在前面加上0x00字节。
2. 如果该字节数组大于或等于64字节，MAC密钥是该字节数组的第33-64字节。
3. 如果该字节数组少于64字节，MAC密钥是该字节数组的SHA-256哈希值。*从0.9.8版本开始。见下方注释。*

#### 重要提示

0.9.8 版本之前的代码存在问题，无法正确处理 32 到 63 字节之间的 DH 密钥字节数组（上述第 3 和第 4 步），连接会失败。由于这些情况从未正常工作过，因此在 0.9.8 版本中按照上述描述重新定义了它们，0-32 字节的情况也被重新定义。由于标准交换的 DH 密钥是 256 字节，最小表示少于 64 字节的概率微乎其微。

### 头部格式

在 AES 加密的载荷中，各种消息都有一个最小的通用结构 - 一个字节的标志位和一个四字节的发送时间戳（自 Unix 纪元以来的秒数）。

头部格式为：

```
Header: 37+ bytes
  Encryption starts with the flag byte.
  +----+----+----+----+----+----+----+----+
  |                  MAC                  |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                   IV                  |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |flag|        time       |              |
  +----+----+----+----+----+              +
  | keying material (optional)            |
  +                                       +
  |                                       |
  ~                                       ~
  |                                       |
  +                        +----+----+----+
  |                        |#opt|         |
  +----+----+----+----+----+----+         +
  | #opt extended option bytes (optional) |
  ~                                       ~
  ~                                       ~
  +----+----+----+----+----+----+----+----+
```
标志字节包含以下位字段：

```
Bit order: 76543210 (bit 7 is MSB)

  bits 7-4: payload type
     bit 3: If 1, rekey data is included. Always 0, unimplemented
     bit 2: If 1, extended options are included. Always 0 before release
            0.9.24.
  bits 1-0: reserved, set to 0 for compatibility with future uses
```
在没有重新生成密钥和扩展选项的情况下，头部大小为 37 字节。

### 重新生成密钥 {#rekey}

如果设置了重新生成密钥标志，则时间戳后跟随64字节的密钥材料。

在重新生成密钥时，密钥材料的前32字节被输入到SHA256中以产生新的MAC密钥，接下来的32字节被输入到SHA256中以产生新的会话密钥，但这些密钥不会立即使用。对方也应该设置重新生成密钥标志并使用相同的密钥材料进行回复。一旦双方都发送并接收了这些值，就应该使用新密钥并丢弃之前的密钥。保留旧密钥一段时间可能是有用的，以应对数据包丢失和重新排序的情况。

注意：密钥更新功能目前尚未实现。

### 扩展选项 {#extend}

如果设置了扩展选项标志，会附加一个单字节的选项大小值，后跟相应数量的扩展选项字节。扩展选项一直是规范的一部分，但直到 0.9.24 版本才得以实现。当存在扩展选项时，选项格式特定于消息类型。请参阅下面的消息文档，了解给定消息是否需要扩展选项以及指定的格式。虽然 Java router 始终能识别该标志和选项长度，但其他实现并非如此。因此，不要向 0.9.24 版本之前的 router 发送扩展选项。

## 填充

所有消息包含0个或更多字节的填充。每个消息必须填充到16字节边界，这是[AES256加密层](/docs/specs/cryptography/#AES)所要求的。

在 0.9.7 版本之前，消息只会填充到下一个 16 字节边界，而不是 16 字节倍数的消息可能会无效。

从 0.9.7 版本开始，消息可以填充到任意长度，只要遵守当前的 MTU。最后一个 16 字节块之外的任何额外 1-15 个填充字节无法被加密或解密，将被忽略。但是，完整长度和所有填充都包含在 MAC 计算中。

从 0.9.8 版本开始，传输的消息不一定是 16 字节的倍数。SessionConfirmed 消息是个例外，见下文。

## 密钥

SessionCreated和SessionConfirmed消息中的签名是使用来自[RouterIdentity](/docs/specs/common-structures/#routeridentity)的[SigningPublicKey](/docs/specs/common-structures/#signingpublickey)生成的，该密钥通过在网络数据库中发布进行带外分发，以及相关联的[SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey)。

在 0.9.15 版本之前（包含该版本），签名算法始终是 DSA，签名长度为 40 字节。

从0.9.16版本开始，签名算法可以通过Bob的[RouterIdentity](/docs/specs/common-structures/#routeridentity)中的[KeyCertificate](/docs/specs/common-structures/#key-certificates)来指定。

引入密钥和会话密钥都是32字节，由通用结构规范[SessionKey](/docs/specs/common-structures/#sessionkey)定义。用于MAC和加密的密钥在下面每个消息中指定。

Introduction keys 通过外部渠道（网络数据库）传递，在 0.9.47 版本之前，它们传统上与 router Hash 相同，但从 0.9.48 版本开始可能是随机的。

## 注释

### IPv6

协议规范允许使用4字节的IPv4地址和16字节的IPv6地址。从0.9.8版本开始支持SSU-over-IPv6。有关IPv6支持的详细信息，请参阅下面各个消息的文档。

### 时间戳 {#time}

虽然I2P的大部分功能使用8字节的[Date](/docs/specs/common-structures/#date)时间戳，具有毫秒级分辨率，但SSU使用4字节无符号整数时间戳，具有1秒的分辨率。由于这些值是无符号的，它们直到2106年2月才会发生回绕。

## 消息

定义了10种消息（负载类型）：

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Message</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Notes</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#sessionrequest">SessionRequest</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#sessioncreated">SessionCreated</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#sessionconfirmed">SessionConfirmed</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#relayrequest">RelayRequest</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#relayresponse">RelayResponse</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#relayintro">RelayIntro</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#data">Data</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#peertest">PeerTest</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#sessiondestroyed">SessionDestroyed</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Implemented as of 0.8.9</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">n/a</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#holepunch">HolePunch</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
</table>
### SessionRequest（类型 0）{#sessionrequest}

这是建立会话发送的第一条消息。

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice to Bob</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">256 byte X, to begin the DH agreement; 1 byte IP address size; that many bytes representation of Bob's IP address; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, as retrieved from the network database</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, as retrieved from the network database</td>
</tr>
</table>
消息格式：

```
+----+----+----+----+----+----+----+----+
|         X, as calculated from DH      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|size| that many byte IP address (4-16) |
+----+----+----+----+----+----+----+----+
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
在当前实现中包含头部的典型大小：304（IPv4）或 320（IPv6）字节（非16倍数填充之前）

#### 扩展选项

注意：在 0.9.24 版本中实现。

- 最小长度：3（选项长度字节 + 2 字节）
- 选项长度：最小 2
- 2 字节标志：

```
Bit order: 15...76543210 (bit 15 is MSB)

      bit 0: 1 for Alice to request a relay tag from Bob in the
             SessionCreated response, 0 if Alice does not need a relay tag.
             Note that "1" is the default if no extended options are present
  bits 15-1: unused, set to 0 for compatibility with future uses
```
#### 注意事项

- 支持 IPv4 和 IPv6 地址。
- 未解释的数据可能在将来用于质询。

### SessionCreated（类型 1）{#sessioncreated}

这是对 [SessionRequest](#sessionrequest) 的响应。

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob to Alice</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">256 byte Y, to complete the DH agreement; 1 byte IP address size; that many bytes representation of Alice's IP address; 2 byte Alice's port number; 4 byte relay (introduction) tag which Alice can publish (else 0x00000000); 4 byte timestamp (seconds from the epoch) for use in the DSA signature; Bob's <a href="/docs/specs/common-structures/#signature">Signature</a> of the critical exchanged data (X + Y + Alice's IP + Alice's port + Bob's IP + Bob's port + Alice's new relay tag + Bob's signed on time), encrypted with another layer of encryption using the negotiated sessionKey. The IV is reused here. See notes for length information.; 0-15 bytes of padding of the signature, using random data, to a multiple of 16 bytes, so that the signature + padding may be encrypted with an additional layer of encryption using the negotiated session key as part of the DSA block.; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, with an additional layer of encryption over the 40 byte signature and the following 8 bytes padding.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey</td>
</tr>
</table>
消息格式：

```
+----+----+----+----+----+----+----+----+
|         Y, as calculated from DH      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|size| that many byte IP address (4-16) |
+----+----+----+----+----+----+----+----+
| Port (A)| public relay tag  |  signed
+----+----+----+----+----+----+----+----+
  on time |                             |
+----+----+                             +
|                                       |
+                                       +
|             signature                 |
+                                       +
|                                       |
+                                       +
|                                       |
+         +----+----+----+----+----+----+
|         |   (0-15 bytes of padding) 
+----+----+----+----+----+----+----+----+
          |                             |
+----+----+                             +
|           arbitrary amount            |
~        of uninterpreted data          ~
~                .  .  .                ~
```
当前实现中包含头部的典型大小：368 字节（IPv4 或 IPv6）（在非 mod-16 填充之前）

#### 注意事项

- 支持 IPv4 和 IPv6 地址。
- 如果 relay tag 不为零，Bob 提供充当 Alice 的介绍者。Alice 随后可能在网络数据库中发布 Bob 的地址和 relay tag。
- 对于签名，Bob 必须使用其外部端口，因为这是 Alice 将用于验证的端口。如果 Bob 的 NAT/防火墙将其内部端口映射到不同的外部端口，而 Bob 不知道这一点，Alice 的验证将失败。
- 有关签名的详细信息，请参阅上面的[密钥](#keys)部分。Alice 已经从网络数据库获得了 Bob 的公共签名密钥。
- 在 0.9.15 版本之前，签名始终是 40 字节的 DSA 签名，填充始终是 8 字节。从 0.9.16 版本开始，签名类型和长度由 Bob 的 [RouterIdentity](/docs/specs/common-structures/#routeridentity) 中 [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) 的类型隐含确定。填充根据需要调整到 16 字节的倍数。
- 这是唯一使用发送者 intro key 的消息。所有其他消息都使用接收者的 intro key 或已建立的会话密钥。
- 在当前实现中，签名时间似乎未使用或未验证。
- 未解释的数据可能在将来用于挑战。
- 头部中的扩展选项：不期望出现，未定义。

### SessionConfirmed（类型 2）{#sessionconfirmed}

这是对 [SessionCreated](#sessioncreated) 消息的响应，也是建立会话的最后一步。如果 Router Identity 必须分片，可能需要多个 SessionConfirmed 消息。

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice to Bob</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 byte identity fragment info (bits 7-4: current identity fragment # 0-14; bits 3-0: total identity fragments (F) 1-15); 2 byte size of the current identity fragment; that many byte fragment of Alice's <a href="/docs/specs/common-structures/#routeridentity">RouterIdentity</a>; After the last identity fragment only: 4 byte signed-on time; N bytes padding, currently uninterpreted; After the last identity fragment only: The remaining bytes contain Alice's <a href="/docs/specs/common-structures/#signature">Signature</a> of the critical exchanged data (X + Y + Alice's IP + Alice's port + Bob's IP + Bob's port + Alice's new relay tag + Alice's signed on time). See notes for length information.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob sessionKey, as generated from the DH exchange</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob MAC Key, as generated from the DH exchange</td>
</tr>
</table>
**片段 0 到 F-2**（仅当 F > 1 时；目前未使用，参见下面的注释）：

```
+----+----+----+----+----+----+----+----+
|info| cursize |                        |
+----+----+----+                        +
|      fragment of Alice's full         |
~            Router Identity            ~
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
**片段 F-1（最后或唯一片段）：**

```
+----+----+----+----+----+----+----+----+
|info| cursize |                        |
+----+----+----+                        +
|     last fragment of Alice's full     |
~            Router Identity            ~
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|  signed on time   |                   |
+----+----+----+----+                   +
|  arbitrary amount of uninterpreted    |
~      data, until the signature at     ~
~       end of the current packet       ~
|  Packet length must be mult. of 16    |
+----+----+----+----+----+----+----+----+
+                                       +
|                                       |
+                                       +
|             signature                 |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
在当前实现中包括头部的典型大小：512字节（使用Ed25519签名）或480字节（使用DSA-SHA1签名）（在非16字节对齐填充之前）

#### 注意事项

- 在当前实现中，最大片段大小为 512 字节。应该扩展此限制，以便更长的签名可以在不分片的情况下工作。当前实现无法正确处理跨两个片段分割的签名。
- 典型的 [RouterIdentity](/docs/specs/common-structures/#routeridentity) 为 387 字节，因此从不需要分片。如果新的加密方法扩展了 RouterIdentity 的大小，必须仔细测试分片方案。
- 没有请求或重新传递丢失片段的机制。
- 总片段数字段 F 必须在所有片段中设置相同。
- 有关 DSA 签名的详细信息，请参见上面的 [Keys](#keys) 部分。
- 签名时间在当前实现中似乎未被使用或验证。
- 由于签名位于末尾，最后一个或唯一数据包中的填充必须将总数据包填充到 16 字节的倍数，否则签名将无法正确解密。这与所有其他消息类型不同，其他消息类型的填充位于末尾。
- 在 0.9.15 版本之前，签名始终是 40 字节的 DSA 签名。从 0.9.16 版本开始，签名类型和长度由 Alice 的 [RouterIdentity](/docs/specs/common-structures/#routeridentity) 中的 [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) 类型隐含确定。必要时填充到 16 字节的倍数。
- 头部中的扩展选项：不期望，未定义。

### SessionDestroyed (类型 8) {#sessiondestroyed}

SessionDestroyed 消息在 0.8.1 版本中实现（仅接收），并从 0.8.9 版本开始发送。

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice to Bob or Bob to Alice</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">none</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob sessionKey</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob MAC Key</td>
</tr>
</table>
此消息不包含任何数据。在当前实现中包含头部的典型大小：48字节（在非16位模填充之前）

#### 注意事项

- 使用发送方或接收方介绍密钥接收到的销毁消息将被忽略。
- 头部中的扩展选项：不被期望，未定义。

### RelayRequest (类型 3) {#relayrequest}

这是Alice发送给Bob的第一条消息，请求介绍给Charlie。

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice to Bob</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4 byte relay (introduction) tag, nonzero, as received by Alice in the SessionCreated message from Bob; 1 byte IP address size; that many byte representation of Alice's IP address; 2 byte port number (of Alice); 1 byte challenge size; that many bytes to be relayed to Charlie in the intro; Alice's 32-byte introduction key (so Bob can reply with Charlie's info); 4 byte nonce of Alice's relay request; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, as retrieved from the network database (or Alice/Bob sessionKey, if established)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, as retrieved from the network database (or Alice/Bob MAC Key, if established)</td>
</tr>
</table>
消息格式：

```
+----+----+----+----+----+----+----+----+
|      relay tag    |size| Alice IP addr
+----+----+----+----+----+----+----+----+
     | Port (A)|size| challenge bytes   |
+----+----+----+----+                   +
|      to be delivered to Charlie       |
+----+----+----+----+----+----+----+----+
| Alice's intro key                     |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|       nonce       |                   |
+----+----+----+----+                   +
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
在当前实现中包含头部的典型大小：96字节（不包含Alice IP）或112字节（包含4字节Alice IP）（在非16模填充之前）

#### 注释

- IP地址只有在与数据包的源地址和端口不同时才会包含。
- 此消息可通过IPv4或IPv6发送。
  如果消息通过IPv6发送IPv4介绍，
  或者（从0.9.50版本开始）通过IPv4发送IPv6介绍，
  Alice必须包含她的介绍地址和端口。
  这在0.9.50版本开始支持。
- 如果Alice包含了她的地址/端口，Bob可以在继续之前执行额外的验证。
  - 在0.9.24版本之前，Java I2P会拒绝任何与连接不同的地址或端口。
- Challenge未实现，challenge大小始终为零
- IPv6中继从0.9.50版本开始支持。
- 在0.9.12版本之前，始终使用Bob的intro key。从0.9.12版本开始，如果Alice和Bob之间存在已建立的会话，则使用session key。实际上，必须存在已建立的会话，因为Alice只能从session created消息中获取nonce（introduction tag），而Bob会在会话销毁后将introduction tag标记为无效。
- 头部中的扩展选项：不期望，未定义。

### RelayResponse (类型 4) {#relayresponse}

这是对 [RelayRequest](#relayrequest) 的响应，从 Bob 发送给 Alice。

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob to Alice</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 byte IP address size; that many byte representation of Charlie's IP address; 2 byte Charlie's port number; 1 byte IP address size; that many byte representation of Alice's IP address; 2 byte Alice's port number; 4 byte nonce sent by Alice; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice's introKey, as received in the Relay Request (or Alice/Bob sessionKey, if established)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice's introKey, as received in the Relay Request (or Alice/Bob MAC Key, if established)</td>
</tr>
</table>
消息格式：

```
+----+----+----+----+----+----+----+----+
|size|    Charlie IP     | Port (C)|size|
+----+----+----+----+----+----+----+----+
|    Alice IP       | Port (A)|  nonce
+----+----+----+----+----+----+----+----+
          |   arbitrary amount of       |
+----+----+                             +
|          uninterpreted data           |
~                .  .  .                ~
```
在当前实现中包含头部的典型大小：64（Alice IPv4）或 80（Alice IPv6）字节（非16倍数填充之前）

#### 注意事项

- 此消息可以通过 IPv4 或 IPv6 发送。
- Alice 的 IP 地址/端口是 Bob 接收 RelayRequest 时的表面 IP/端口（不一定是 Alice 在 RelayRequest 中包含的 IP），可能是 IPv4 或 IPv6。Alice 目前在接收时会忽略这些。
- Charlie 的 IP 地址可能是 IPv4，或者从 0.9.50 版本开始，也可能是 IPv6，因为这是 Alice 在 Hole Punch 之后发送 SessionRequest 的目标地址。
- 从 0.9.50 版本开始支持 IPv6 中继。
- 在 0.9.12 版本之前，总是使用 Alice 的 intro key。从 0.9.12 版本开始，如果 Alice 和 Bob 之间已建立会话，则使用 session key。
- 标头中的扩展选项：不期望有，未定义。

### RelayIntro (类型 5) {#relayintro}

这是Alice的介绍，由Bob发送给Charlie。

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob to Charlie</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 byte IP address size; that many byte representation of Alice's IP address; 2 byte port number (of Alice); 1 byte challenge size; that many bytes relayed from Alice; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob/Charlie sessionKey</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob/Charlie MAC Key</td>
</tr>
</table>
消息格式：

```
+----+----+----+----+----+----+----+----+
|size|     Alice IP      | Port (A)|size|
+----+----+----+----+----+----+----+----+
|      that many bytes of challenge     |
+                                       +
|        data relayed from Alice        |
+----+----+----+----+----+----+----+----+
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
在当前实现中包含头部的典型大小：48 字节（在非模16填充之前）

#### 注意事项

- 对于 IPv4，Alice 的 IP 地址始终为 4 字节，因为 Alice 试图通过 IPv4 连接到 Charlie。
  从 0.9.50 版本开始，支持 IPv6，Alice 的 IP 地址可能为 16 字节。
- 对于 IPv4，此消息必须通过已建立的 IPv4 连接发送，
  因为这是 Bob 知道 Charlie 的 IPv4 地址以便在 RelayResponse 中返回给 Alice 的唯一方式。
  从 0.9.50 版本开始，支持 IPv6，此消息可以通过已建立的 IPv6 连接发送。
- 从 0.9.50 版本开始，任何使用 introducers 发布的 SSU 地址必须在 "caps" 选项中包含 "4" 或 "6"。
- Challenge 未实现，challenge 大小始终为零
- 标头中的扩展选项：不期望，未定义。

### 数据 (类型 6) {#data}

此消息用于数据传输和确认。

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Any</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob sessionKey</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob MAC Key</td>
</tr>
</table>
**数据：** 1字节标志（见下文）；如果包含显式ACK：1字节ACK数量，相应数量的4字节MessageId被完全确认；如果包含ACK位字段：1字节ACK位字段数量，相应数量的4字节MessageId + 1个或多个字节的ACK位字段（见注释）；如果包含扩展数据：1字节数据大小，相应字节数的扩展数据（当前未解释）；1字节片段数量（可以为零）；如果非零，则包含相应数量的消息片段。

```
Flags byte:
  Bit order: 76543210 (bit 7 is MSB)
  bit 7: explicit ACKs included
  bit 6: ACK bitfields included
  bit 5: reserved
  bit 4: explicit congestion notification (ECN)
  bit 3: request previous ACKs
  bit 2: want reply
  bit 1: extended data included (unused, never set)
  bit 0: reserved
```
每个片段包含：- 4 字节 messageId - 3 字节片段信息：   - 位 23-17：片段编号 0 - 127   - 位 16：isLast（1 = true）   - 位 15-14：未使用，设置为 0 以兼容未来用途   - 位 13-0：片段大小 0 - 16383 - 相应字节数的片段数据

消息格式：

```
+----+----+----+----+----+----+----+----+
|flag| (additional headers, determined  |
+----+                                  +
~ by the flags, such as ACKs or         ~
| bitfields                             |
+----+----+----+----+----+----+----+----+
|#frg|     messageId     |   frag info  |
+----+----+----+----+----+----+----+----+
| that many bytes of fragment data      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|     messageId     |   frag info  |    |
+----+----+----+----+----+----+----+    +
| that many bytes of fragment data      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|     messageId     |   frag info  |    |
+----+----+----+----+----+----+----+    +
| that many bytes of fragment data      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
#### ACK 位字段注释

位字段使用每个字节的低7位，高位指定是否有额外的位字段字节跟随（1 = 是，0 = 当前位字段字节是最后一个）。这些7位数组序列表示是否已接收到片段 - 如果位为1，则表示已接收到该片段。为了澄清，假设已接收到片段0、2、5和9，位字段字节将如下所示：

```
byte 0:
   Bit order: 76543210 (bit 7 is MSB)
   bit 7: 1 (further bitfield bytes follow)
   bit 6: 0 (fragment 6 not received)
   bit 5: 1 (fragment 5 received)
   bit 4: 0 (fragment 4 not received)
   bit 3: 0 (fragment 3 not received)
   bit 2: 1 (fragment 2 received)
   bit 1: 0 (fragment 1 not received)
   bit 0: 1 (fragment 0 received)
byte 1:
   Bit order: 76543210 (bit 7 is MSB)
   bit 7: 0 (no further bitfield bytes)
   bit 6: 0 (fragment 13 not received)
   bit 5: 0 (fragment 12 not received)
   bit 4: 0 (fragment 11 not received)
   bit 3: 0 (fragment 10 not received)
   bit 2: 1 (fragment 9 received)
   bit 1: 0 (fragment 8 not received)
   bit 0: 0 (fragment 7 not received)
```
#### 注意事项

- 当前实现会为先前已确认的消息添加有限数量的重复确认，如果有空间可用的话。
- 如果片段数量为零，这是一个仅确认或保活消息。
- ECN功能未实现，该位从不设置。
- 在当前实现中，当片段数量大于零时设置想要回复位，当没有片段时不设置。
- 扩展数据未实现且从不存在。
- 多片段接收在所有版本中都受支持。多片段传输在0.9.16版本中实现。
- 当前实现中，最大片段数为64（最大片段编号 = 63）。
- 当前实现中，最大片段大小当然小于MTU。
- 注意不要超过最大MTU，即使有大量ACK需要发送。
- 协议允许零长度片段，但没有理由发送它们。
- 在SSU中，数据使用简短的5字节I2NP头部，后跟I2NP消息的载荷，而不是标准的16字节I2NP头部。简短的I2NP头部仅包含1字节的I2NP类型和4字节的秒级过期时间。I2NP消息ID用作片段的消息ID。I2NP大小从片段大小组装而成。不需要I2NP校验和，因为UDP消息完整性通过解密确保。
- 消息ID不是序列号，也不是连续的。SSU不保证按序交付。虽然我们使用I2NP消息ID作为SSU消息ID，但从SSU协议的角度来看，它们是随机数。实际上，由于router对所有对等节点使用单一布隆过滤器，消息ID必须是实际的随机数。
- 因为没有序列号，无法确定ACK是否已接收。当前实现例行发送大量重复ACK。重复ACK不应被视为拥塞的指示。
- ACK位域注释：数据包接收者不知道消息中有多少片段，除非它已接收到最后一个片段。因此，响应中发送的位域字节数可能少于或多于片段数除以7。例如，如果接收者看到的最高片段编号是4，只需要发送一个字节，即使总共可能有13个片段。每个确认的消息ID最多可以包含10个字节（即(64 / 7) + 1）。
- 头部中的扩展选项：不期望，未定义。

### PeerTest（类型 7）{#peertest}

详情请参见 [SSU Peer Testing](/docs/transport/ssu/#peerTesting)。注意：从 0.9.27 版本开始支持 IPv6 peer testing。

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Any</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4 byte nonce; 1 byte IP address size (may be zero); that many byte representation of Alice's IP address, if size > 0; 2 byte Alice's port number; Alice's or Charlie's 32-byte introduction key; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">See notes below</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">See notes below</td>
</tr>
</table>
使用的加密密钥（按出现顺序列出）：1. 从 Alice 发送到 Bob 时：Alice/Bob sessionKey 2. 从 Bob 发送到 Charlie 时：Bob/Charlie sessionKey 3. 从 Charlie 发送到 Bob 时：Bob/Charlie sessionKey 4. 从 Bob 发送到 Alice 时：Alice/Bob sessionKey（或对于 0.9.52 版本之前的 Bob，使用 Alice 的 introKey）5. 从 Charlie 发送到 Alice 时：Alice 的 introKey，从 Bob 的 PeerTest 消息中接收 6. 从 Alice 发送到 Charlie 时：Charlie 的 introKey，从 Charlie 的 PeerTest 消息中接收

使用的 MAC Key（按发生顺序列出）：1. 当从 Alice 发送到 Bob 时：Alice/Bob MAC Key 2. 当从 Bob 发送到 Charlie 时：Bob/Charlie MAC Key 3. 当从 Charlie 发送到 Bob 时：Bob/Charlie MAC Key 4. 当从 Bob 发送到 Alice 时：Alice 的 introKey，从 Alice 的 PeerTest 消息中接收到的 5. 当从 Charlie 发送到 Alice 时：Alice 的 introKey，从 Bob 的 PeerTest 消息中接收到的 6. 当从 Alice 发送到 Charlie 时：Charlie 的 introKey，从 Charlie 的 PeerTest 消息中接收到的

消息格式：

```
+----+----+----+----+----+----+----+----+
|    test nonce     |size| Alice IP addr
+----+----+----+----+----+----+----+----+
     | Port (A)|                        |
+----+----+----+                        +
| Alice or Charlie's                    |
+ introduction key (Alice's is sent to  +
| Bob and Charlie, while Charlie's is   |
+ sent to Alice)                        +
|                                       |
+              +----+----+----+----+----+
|              | arbitrary amount of    |
+----+----+----+                        |
| uninterpreted data                    |
~                .  .  .                ~
```
当前实现中包含头部的典型大小：80 字节（非 16 倍数填充之前）

#### 注释

- 当由 Alice 发送时，IP 地址大小为 0，IP 地址不存在，端口为 0，因为 Bob 和 Charlie 不使用这些数据；目的是确定 Alice 的真实 IP 地址/端口并告知 Alice；Bob 和 Charlie 不关心 Alice 认为她的地址是什么。
- 当由 Bob 或 Charlie 发送时，IP 和端口存在，IP 地址为 4 或 16 字节。从 0.9.27 版本开始支持 IPv6 测试。
- 当由 Charlie 发送给 Alice 时，IP 和端口如下：
  第一次（消息 5）：Alice 在消息 2 中请求的 IP 和端口。
  第二次（消息 7）：接收消息 6 时 Alice 的实际 IP 和端口。
- IPv6 注意事项：在 0.9.26 版本及之前，仅支持 IPv4 地址测试。因此，所有 Alice-Bob 和 Alice-Charlie 通信必须通过 IPv4。然而，Bob-Charlie 通信可以通过 IPv4 或 IPv6。在 PeerTest 消息中指定 Alice 的地址时，必须是 4 字节。
  从 0.9.27 版本开始，支持 IPv6 地址测试，如果 Bob 和 Charlie 在其发布的 IPv6 地址中用 'B' 能力标识表示支持，则 Alice-Bob 和 Alice-Charlie 通信可以通过 IPv6。
  详情请参见提案 126。
- Alice 使用现有会话通过她希望测试的传输协议（IPv4 或 IPv6）向 Bob 发送请求。
  当 Bob 通过 IPv4 收到来自 Alice 的请求时，Bob 必须选择一个公布 IPv4 地址的 Charlie。
  当 Bob 通过 IPv6 收到来自 Alice 的请求时，Bob 必须选择一个公布 IPv6 地址的 Charlie。
  实际的 Bob-Charlie 通信可以通过 IPv4 或 IPv6（即，独立于 Alice 的地址类型）。
- 对等节点必须维护一个活跃测试状态（nonce）表。收到 PeerTest 消息时，在表中查找 nonce。如果找到，这是一个现有测试，你知道你的角色（Alice、Bob 或 Charlie）。否则，如果 IP 不存在且端口为 0，这是一个新测试，你是 Bob。
  否则，这是一个新测试，你是 Charlie。
- 从 0.9.15 版本开始，Alice 必须与 Bob 建立会话并使用会话密钥。
- 在 API 版本 0.9.52 之前，在某些实现中，Bob 使用 Alice 的介绍密钥而不是 Alice/Bob 会话密钥回复 Alice，即使 Alice 和 Bob 已经建立了会话（从 0.9.15 开始）。
  从 API 版本 0.9.52 开始，Bob 在所有实现中都会正确使用会话密钥，如果 Bob 是 API 版本 0.9.52 或更高版本，Alice 应该拒绝使用 Alice 介绍密钥从 Bob 收到的消息。
- 头部中的扩展选项：不期望，未定义。

### HolePunch {#holepunch}

HolePunch 只是一个没有数据的 UDP 数据包。它未经身份验证也未加密。它不包含 SSU 头部，因此没有消息类型编号。它作为 Introduction 序列的一部分从 Charlie 发送到 Alice。

## 示例数据报 {#sampledatagrams}

### 最小数据消息

- 无分片，无 ACK，无 NACK 等
- 大小：39 字节

```
+----+----+----+----+----+----+----+----+
|                  MAC                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                   IV                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag|        time       |flag|#frg|    |
+----+----+----+----+----+----+----+    +
|  padding to fit a full AES256 block   |
+----+----+----+----+----+----+----+----+
```
### 带有载荷的最小数据消息

- 大小：46+fragmentSize 字节

```
+----+----+----+----+----+----+----+----+
|                  MAC                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                   IV                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag|        time       |flag|#frg|
+----+----+----+----+----+----+----+----+
  messageId    |   frag info  |         |
----+----+----+----+----+----+         +
| that many bytes of fragment data      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
```
## 参考资料

- [AES 加密](/docs/specs/cryptography/#AES)
- [通用结构规范](/docs/specs/common-structures/)
- [日期](/docs/specs/common-structures/#date)
- [ElGamal 加密](/docs/specs/cryptography/#elgamal)
- [HMAC 详细信息](/docs/specs/cryptography/#udp)
- [I2P 源代码](https://github.com/i2p/i2p.i2p)
- [i2pd 源代码](https://github.com/PurpleI2P/i2pd)
- [KeyCertificate](/docs/specs/common-structures/#key-certificates)
- [RouterIdentity](/docs/specs/common-structures/#routeridentity)
- [SessionKey](/docs/specs/common-structures/#sessionkey)
- [Signature](/docs/specs/common-structures/#signature)
- [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey)
- [SigningPublicKey](/docs/specs/common-structures/#signingpublickey)
- [SSU 概览](/docs/transport/ssu/)
- [SSU 密钥](/docs/transport/ssu/#keys)
- [SSU 对等测试](/docs/transport/ssu/#peerTesting)
