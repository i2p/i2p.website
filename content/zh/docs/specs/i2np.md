---
title: "I2NP 规范"
description: "I2P网络协议(I2NP)消息格式、优先级以及router间通信的通用结构。"
slug: "i2np"
aliases:
  - "/zh/spec/i2np"
  - "/zh/spec/i2np/"
  - "/zh/i2np_spec"
  - "/zh/i2np_spec/"
category: "协议"
lastUpdated: "2026-03"
accurateFor: "0.9.69"
---

## 概述

I2P网络协议（I2NP）是位于I2P传输协议之上的层。它是一个router到router的协议。它用于网络数据库查询和回复、创建tunnel，以及加密的router和客户端数据消息。I2NP消息可以点对点发送到另一个router，或者通过tunnel匿名发送到该router。

## 协议版本 {#versions}

所有 router 必须在 RouterInfo 属性的 "router.version" 字段中发布其 I2NP 协议版本。此版本字段是 API 版本，表示对各种 I2NP 协议功能的支持级别，不一定是实际的 router 版本。

如果替代的（非Java）router希望发布关于实际router实现的任何版本信息，它们必须在另一个属性中进行发布。除了下面列出的版本之外，还允许使用其他版本。支持将通过数字比较来确定；例如，0.9.13意味着支持0.9.12的功能。请注意，"coreVersion"属性不再在router信息中发布，并且从未用于确定I2NP协议版本。

以下是 I2NP 协议版本的基本概述。详情请见下文。

<table style="border-collapse: collapse; width: 100%;">
<thead>
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">API Version</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">Required I2NP Features</th>
</tr>
</thead>
<tbody>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.68</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Tunnel testing required</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">LeaseSet2 service record options (see proposal 167)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.65</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Tunnel build bandwidth parameters (see proposal 168)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.62</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Minimum peers will build tunnels through, as of 0.9.68<br>Minimum floodfill peers will send DSM to, as of 0.9.68</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.59</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Minimum peers will build tunnels through, as of 0.9.63<br>Minimum floodfill peers will send DSM to, as of 0.9.63</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.58</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Minimum peers will build tunnels through, as of 0.9.62<br>ElGamal Routers deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.55</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">SSU2 transport support (if published in router info)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.51</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Short tunnel build messages for ECIES-X25519 routers<br>Minimum peers will build tunnels through, as of 0.9.58<br>Minimum floodfill peers will send DSM to, as of 0.9.58</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.49</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Garlic messages to ECIES-X25519 routers</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.48</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES-X25519 Routers<br>ECIES-X25519 Build Request/Response records</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.46</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">DatabaseLookup flag bit 4 for AEAD reply</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.44</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES-X25519 keys in LeaseSet2</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.40</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">MetaLeaseSet may be sent in a DSM</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.39</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">EncryptedLeaseSet may be sent in a DSM<br>RedDSA_SHA512_Ed25519 signature type supported for destinations and leasesets</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">DSM type bits 3-0 now contain the type; LeaseSet2 may be sent in a DSM</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.36</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">NTCP2 transport support (if published in router info)<br>Minimum peers will build tunnels through, as of 0.9.46</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.28</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">RSA sig types disallowed<br>Minimum floodfill peers will send DSM to, as of 0.9.34</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.18</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">DSM type bits 7-1 ignored</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.16</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">RI key certs / ECDSA and EdDSA sig types<br>Note: RSA sig types also supported as of this version, but currently unused<br>DLM lookup types (DLM flag bits 3-2)<br>Minimum version compatible with vast majority of current network, since routers are now using the EdDSA sig type.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.15</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest/LS key certs w/ EdDSA Ed25519 sig type (if floodfill)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest/LS key certs w/ ECDSA P-256, P-384, and P-521 sig types (if floodfill)<br>Note: RSA sig types also supported as of this version, but currently unused<br>Nonzero expiration allowed in RouterAddress</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Encrypted DSM/DSRM replies supported (DLM flag bit 1) (if floodfill)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Nonzero DLM flag bits 7-1 allowed</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Requires zero expiration in RouterAddress</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Supports up to 16 leases in a DSM LS store (6 previously)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">VTBM and VTBRM message support</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Floodfill supports encrypted DSM stores</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.9 or lower</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">All messages and features not listed above</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.6.1.10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">TBM and TBRM messages introduced<br>Minimum version compatible with current network</td>
</tr>
</tbody>
</table>
请注意，还存在与传输相关的功能和兼容性问题；详情请参阅 NTCP 和 SSU 传输文档。

## 常用结构 {#structures}

以下结构是多个 I2NP 消息的元素。它们不是完整的消息。

### I2NP 消息头 {#struct-I2NPMessageHeader}

#### 描述

所有 I2NP 消息的通用头部，包含重要信息如校验和、过期时间等。

#### 目录

根据上下文的不同，使用了三种不同的格式；一种标准格式和两种短格式。

标准的16字节格式包含1个字节的[Integer](/docs/specs/common-structures/#integer)，用于指定此消息的类型，后跟4个字节的[Integer](/docs/specs/common-structures/#integer)，用于指定消息ID。之后是一个过期[Date](/docs/specs/common-structures/#date)，后跟2个字节的[Integer](/docs/specs/common-structures/#integer)，用于指定消息载荷的长度，再后跟一个[Hash](/docs/specs/common-structures/#hash)，该哈希值被截断为第一个字节。在此之后是实际的消息数据。

短格式使用4字节的秒级过期时间，而不是8字节的毫秒级过期时间。短格式不包含校验和或大小信息，这些信息由封装层提供，具体取决于上下文。

```
Standard (16 bytes):

+----+----+----+----+----+----+----+----+
|type|      msg_id       |  expiration
+----+----+----+----+----+----+----+----+
                         |  size   |chks|
+----+----+----+----+----+----+----+----+

Short (SSU, 5 bytes) (obsolete):

+----+----+----+----+----+
|type| short_expiration  |
+----+----+----+----+----+

Short (NTCP2, SSU2, and ECIES-Ratchet Garlic Cloves, 9 bytes):

+----+----+----+----+----+----+----+----+
|type|      msg_id       | short_expira-
+----+----+----+----+----+----+----+----+
 tion|
+----+

type :: Integer
        length -> 1 byte
        purpose -> identifies the message type (see table below)

msg_id :: Integer
          length -> 4 bytes
          purpose -> uniquely identifies this message (for some time at least)
                     This is usually a locally-generated random number, but
                     for outgoing tunnel build messages it may be derived from
                     the incoming message. See below.

expiration :: Date
              8 bytes
              date this message will expire

short_expiration :: Integer
                    4 bytes
                    date this message will expire (seconds since the epoch)

size :: Integer
        length -> 2 bytes
        purpose -> length of the payload

chks :: Integer
        length -> 1 byte
        purpose -> checksum of the payload
                   SHA256 hash truncated to the first byte

data ::
        length -> $size bytes
        purpose -> actual message contents
```
#### 注释

- 当通过 [SSU](/docs/transports/ssu/) 传输时，不使用16字节的标准头部。只包含1字节的类型和4字节的过期时间（以秒为单位）。消息ID和大小被整合到SSU数据包格式中。由于错误会在解密过程中被捕获，因此不需要校验和。

- 当通过 [NTCP2](/docs/specs/ntcp2/) 或 [SSU2](/docs/specs/ssu2/) 传输时，不使用 16 字节标准头部。只包含 1 字节类型、4 字节消息 ID 和 4 字节过期时间（以秒为单位）。大小信息包含在 NTCP2 和 SSU2 数据包格式中。由于错误会在解密过程中被捕获，因此不需要校验和。

- 对于包含在其他消息和结构中的I2NP消息（Data、TunnelData、TunnelGateway和GarlicClove），也需要标准头部。从0.8.12版本开始，为了减少开销，在协议栈的某些地方禁用了校验和验证。然而，为了与旧版本兼容，仍然需要生成校验和。确定协议栈中已知远端router版本且可以禁用校验和生成的节点，是未来研究的一个主题。

- 短过期时间是无符号的，将在2106年2月7日回绕。从那个日期开始，必须添加偏移量才能获得正确的时间。

- 实现可能会拒绝过期时间过远的消息。建议的最大过期时间为未来60秒。

### BuildRequestRecord {#struct-BuildRequestRecord}

已弃用，仅在当前网络中包含 ElGamal router 的 tunnel 时使用。参见 [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/)。

#### 描述

在多条记录集合中的一条记录，用于请求在tunnel中创建一跳。更多详情请参见[tunnel概览](/docs/specs/tunnel-implementation/)和[ElGamal tunnel创建规范](/docs/specs/tunnel-creation/)。

对于 ECIES-X25519 BuildRequestRecords，请参见 [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/)。

#### 目录 (ElGamal)

用于接收消息的 [TunnelId](/docs/specs/common-structures/#tunnelid)，后面跟着我们的 [RouterIdentity](/docs/specs/common-structures/#routeridentity) 的 [Hash](/docs/specs/common-structures/#hash)。之后是下一个 router 的 [RouterIdentity](/docs/specs/common-structures/#routeridentity) 的 [TunnelId](/docs/specs/common-structures/#tunnelid) 和 [Hash](/docs/specs/common-structures/#hash)。

ElGamal 和 AES 加密：

```
+----+----+----+----+----+----+----+----+
| encrypted data...                     |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

encrypted_data :: ElGamal and AES encrypted data
                  length -> 528

total length: 528
```
ElGamal 加密：

```
+----+----+----+----+----+----+----+----+
| toPeer                                |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| encrypted data...                     |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

toPeer :: First 16 bytes of the SHA-256 Hash of the peer's RouterIdentity
          length -> 16 bytes

encrypted_data :: ElGamal-2048 encrypted data (see notes)
                  length -> 512

total length: 528
```
明文：

```
+----+----+----+----+----+----+----+----+
| receive_tunnel    | our_ident         |
+----+----+----+----+                   +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+                   +----+----+----+----+
|                   | next_tunnel       |
+----+----+----+----+----+----+----+----+
| next_ident                            |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| layer_key                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| iv_key                                |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| reply_key                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| reply_iv                              |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag| request_time      | send_msg_id
+----+----+----+----+----+----+----+----+
     |                                  |
+----+                                  +
|         29 bytes padding              |
+                                       +
|                                       |
+                             +----+----+
|                             |
+----+----+----+----+----+----+

receive_tunnel :: TunnelId
                  length -> 4 bytes
                  nonzero

our_ident :: Hash
             length -> 32 bytes

next_tunnel :: TunnelId
               length -> 4 bytes
               nonzero

next_ident :: Hash
              length -> 32 bytes

layer_key :: SessionKey
             length -> 32 bytes

iv_key :: SessionKey
          length -> 32 bytes

reply_key :: SessionKey
             length -> 32 bytes

reply_iv :: data
            length -> 16 bytes

flag :: Integer
        length -> 1 byte

request_time :: Integer
                length -> 4 bytes
                Hours since the epoch, i.e. current time / 3600

send_message_id :: Integer
                   length -> 4 bytes

padding :: Data
           length -> 29 bytes
           source -> random

total length: 222
```
#### 说明

- 在512字节的加密记录中，ElGamal数据包含514字节ElGamal加密块[CRYPTO-ELG](/docs/specs/cryptography/#elgamal)的第1-256字节和第258-513字节。块中的两个填充字节（位于位置0和257的零字节）被移除。

- 有关字段内容的详细信息，请参阅[tunnel创建规范](/docs/specs/tunnel-creation/)。

### BuildResponseRecord {#struct-BuildResponseRecord}

已弃用，仅在当前网络中包含 ElGamal router 的 tunnel 时使用。参见 [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/)。

#### 描述

在包含多个记录的集合中的一个记录，用于响应构建请求。更多详细信息请参见 [tunnel 概述](/docs/specs/tunnel-implementation/) 和 [ElGamal tunnel 创建规范](/docs/specs/tunnel-creation/)。

对于 ECIES-X25519 BuildResponseRecords，请参见 [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/)。

#### 目录 (ElGamal)

```
Encrypted:

bytes 0-527 :: AES-encrypted record (note: same size as BuildRequestRecord)

Unencrypted:

+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|                                       |
+   SHA-256 Hash of following bytes     +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| random data...                        |
~                                       ~
|                                       |
+                                  +----+
|                                  | ret|
+----+----+----+----+----+----+----+----+

bytes 0-31   :: SHA-256 Hash of bytes 32-527
bytes 32-526 :: random data
byte  527    :: reply

total length: 528
```
#### 注释

- 随机数据字段在未来可以用于将拥塞或对等节点连接信息返回给请求者。

- 有关回复字段的详细信息，请参阅 [tunnel 创建规范](/docs/specs/tunnel-creation/)。

### ShortBuildRequestRecord {#struct-ShortBuildRequestRecord}

仅适用于 ECIES-X25519 router，自 API 版本 0.9.51 起。加密后为 218 字节。参见 [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/)。

### ShortBuildResponseRecord {#struct-ShortBuildResponseRecord}

仅适用于 ECIES-X25519 router，自 API 版本 0.9.51 起。加密后为 218 字节。参见 [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/)。

### GarlicClove {#struct-GarlicClove}

警告：这是在ElGamal加密的garlic消息中使用的garlic clove格式[CRYPTO-ELG](/docs/specs/cryptography/#elgamal)。ECIES-AEAD-X25519-Ratchet garlic消息和garlic clove的格式有显著不同；请参见[ECIES](/docs/specs/ecies/)规范。

```
Unencrypted:

+----+----+----+----+----+----+----+----+
| Delivery Instructions                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| I2NP Message                          |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|    Clove ID       |     Expiration
+----+----+----+----+----+----+----+----+
                    | Certificate  |
+----+----+----+----+----+----+----+

Delivery Instructions :: as defined below
       Length varies but is typically 1, 33, or 37 bytes

I2NP Message :: Any I2NP Message

Clove ID :: 4 byte Integer

Expiration :: Date (8 bytes)

Certificate :: Always NULL in the current implementation (3 bytes total, all zeroes)
```
#### 注释

- Clove 永远不会被分片。当在 Garlic Clove 中使用时，Delivery Instructions 标志字节的第一位指定加密。如果此位为 0，则 clove 不加密。如果为 1，则 clove 被加密，并且一个 32 字节的 Session Key 紧跟在标志字节之后。Clove 加密尚未完全实现。

- 另请参阅 [garlic routing 规范](/docs/overview/garlic-routing/)。

- 最大长度是所有clove总长度和GarlicMessage最大长度的函数。

- 在未来，证书可能会用于 HashCash 来为路由"付费"。

- 消息可以是任何 I2NP 消息（包括 GarlicMessage，虽然在实践中不使用）。实际使用的消息是 DataMessage、DeliveryStatusMessage 和 DatabaseStoreMessage。

- Clove ID通常在传输时设置为随机数，并在接收时检查重复项（与顶级消息ID使用相同的消息ID空间）

### Garlic Clove 传递指令 {#struct-GarlicCloveDeliveryInstructions}

这是用于 ElGamal 加密的 [CRYPTO-ELG](/docs/specs/cryptography/#elgamal) 和 ECIES-AEAD-X25519-Ratchet 加密的 [ECIES](/docs/specs/ecies/) garlic cloves 的格式。

本规范仅适用于 Garlic Clove 内部的传递指令。请注意，"传递指令"也用于 Tunnel Message 内部，但格式有显著差异。详情请参阅 [Tunnel Message 文档](/docs/legacy/tunnel-message/#tunnel-message-delivery-instructions)。请勿将以下规范用于 Tunnel Message 传递指令！

会话密钥和延迟字段未使用且从不存在，因此三种可能的长度分别是 1（LOCAL）、33（ROUTER 和 DESTINATION）和 37（TUNNEL）字节。

```
+----+----+----+----+----+----+----+----+
|flag|                                  |
+----+                                  +
|                                       |
+       Session Key (optional)          +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+--------------+
|    |                                  |
+----+                                  +
|                                       |
+         To Hash (optional)            +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+--------------+
|    |  Tunnel ID (opt)  |  Delay (opt)
+----+----+----+----+----+----+----+----+
     |
+----+

flag ::
       1 byte
       Bit order: 76543210
       bit 7: encrypted? Unimplemented, always 0
                If 1, a 32-byte encryption session key is included
       bits 6-5: delivery type
                0x0 = LOCAL, 0x01 = DESTINATION, 0x02 = ROUTER, 0x03 = TUNNEL
       bit 4: delay included?  Not fully implemented, always 0
                If 1, four delay bytes are included
       bits 3-0: reserved, set to 0 for compatibility with future uses

Session Key ::
       32 bytes
       Optional, present if encrypt flag bit is set.
       Unimplemented, never set, never present.

To Hash ::
       32 bytes
       Optional, present if delivery type is DESTINATION, ROUTER, or TUNNEL
          If DESTINATION, the SHA256 Hash of the destination
          If ROUTER, the SHA256 Hash of the router
          If TUNNEL, the SHA256 Hash of the gateway router

Tunnel ID :: TunnelId
       4 bytes
       Optional, present if delivery type is TUNNEL
       The destination tunnel ID, nonzero

Delay :: Integer
       4 bytes
       Optional, present if delay included flag is set
       Not fully implemented. Specifies the delay in seconds.

Total length: Typical length is:
       1 byte for LOCAL delivery;
       33 bytes for ROUTER / DESTINATION delivery;
       37 bytes for TUNNEL delivery
```
## 消息

<table style="border-collapse: collapse; width: 100%;">
<thead>
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">Message</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">Since</th>
</tr>
</thead>
<tbody>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-DatabaseStore">DatabaseStore</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-DatabaseLookup">DatabaseLookup</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-DatabaseSearchReply">DatabaseSearchReply</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-DeliveryStatus">DeliveryStatus</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-Garlic">Garlic</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-TunnelData">TunnelData</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">18</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-TunnelGateway">TunnelGateway</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">19</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-Data">Data</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">20</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-TunnelBuild">TunnelBuild</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">21</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-TunnelBuildReply">TunnelBuildReply</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">22</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-VariableTunnelBuild">VariableTunnelBuild</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">23</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.12</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-VariableTunnelBuildReply">VariableTunnelBuildReply</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">24</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.12</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-ShortTunnelBuild">ShortTunnelBuild</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">25</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.51</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-OutboundTunnelBuildReply">OutboundTunnelBuildReply</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">26</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.51</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Reserved</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Reserved for experimental messages</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">224-254</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Reserved for future expansion</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">255</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
</tbody>
</table>
### DatabaseStore {#msg-DatabaseStore}

#### 描述

一个未经请求的数据库存储，或对成功的 [DatabaseLookup](#msg-DatabaseLookup) 消息的响应

#### 目录

未压缩的 LeaseSet、LeaseSet2、MetaLeaseSet 或 EncryptedLeaseset，或者压缩的 RouterInfo

```
with reply token:
+----+----+----+----+----+----+----+----+
| SHA256 Hash as key                    |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|type| reply token       | reply_tunnelId
+----+----+----+----+----+----+----+----+
     | SHA256 of the gateway RouterInfo |
+----+                                  +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+----+----+----+
|    | data ...
+----+-//

with reply token == 0:
+----+----+----+----+----+----+----+----+
| SHA256 Hash as key                    |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|type|         0         | data ...
+----+----+----+----+----+-//

key ::
    32 bytes
    SHA256 hash

type ::
     1 byte
     type identifier
     bit 0:
             0    RouterInfo
             1    LeaseSet or variants listed below
     bits 3-1:
            Through release 0.9.17, must be 0
            As of release 0.9.18, ignored, reserved for future options, set to 0 for compatibility
            As of release 0.9.38, the remainder of the type identifier:
            0: RouterInfo or LeaseSet (types 0 or 1)
            1: LeaseSet2 (type 3)
            2: EncryptedLeaseSet (type 5)
            3: MetaLeaseSet (type 7)
            4-7: Unsupported, invalid
     bits 7-4:
            Through release 0.9.17, must be 0
            As of release 0.9.18, ignored, reserved for future options, set to 0 for compatibility

reply token ::
            4 bytes
            If greater than zero, a DeliveryStatusMessage
            is requested with the Message ID set to the value of the Reply Token.
            A floodfill router is also expected to flood the data to the closest floodfill peers
            if the token is greater than zero.

reply_tunnelId ::
               4 byte TunnelId
               Only included if reply token > 0
               This is the TunnelId of the inbound gateway of the tunnel the response should be sent to
               If $reply_tunnelId is zero, the reply is sent directy to the reply gateway router.

reply gateway ::
              32 bytes
              Hash of the RouterInfo entry to reach the gateway
              Only included if reply token > 0
              If $reply_tunnelId is nonzero, this is the router hash of the inbound gateway
              of the tunnel the response should be sent to.
              If $reply_tunnelId is zero, this is the router hash the response should be sent to.

data ::
     If type == 0, data is a 2-byte Integer specifying the number of bytes that follow,
                   followed by a gzip-compressed RouterInfo. See note below.
     If type == 1, data is an uncompressed LeaseSet.
     If type == 3, data is an uncompressed LeaseSet2.
     If type == 5, data is an uncompressed EncryptedLeaseSet.
     If type == 7, data is an uncompressed MetaLeaseSet.
```
#### 注意事项

- 出于安全考虑，如果消息是通过tunnel接收的，则忽略回复字段。

- 该键是 RouterIdentity 或 Destination 的"真实"哈希值，而不是路由键。

- 类型 3、5 和 7 从版本 0.9.38 开始支持。更多信息请参见提案 123。这些类型只应发送给版本 0.9.38 或更高版本的 router。

- 作为减少连接的优化，如果类型是LeaseSet，包含了回复令牌，回复tunnel ID非零，并且回复网关/tunnelID对在LeaseSet中作为租约被找到，接收者可以将回复重新路由到LeaseSet中的任何其他租约。

- 为了隐藏 router 操作系统和实现，通过将修改时间设置为 0、操作系统字节设置为 0xFF，并将 XFL 设置为 0x02（最大压缩，最慢算法）来匹配 Java router 实现的 gzip。参见 RFC 1952。压缩后的 router 信息的前 10 个字节将是（十六进制）：1F 8B 08 00 00 00 00 00 02 FF

### DatabaseLookup {#msg-DatabaseLookup}

#### 描述

在网络数据库中查找项目的请求。响应是 [DatabaseStore](#msg-DatabaseStore) 或 [DatabaseSearchReply](#msg-DatabaseSearchReply)。

#### 目录

```
+----+----+----+----+----+----+----+----+
| SHA256 hash as the key to look up     |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| SHA256 hash of the routerInfo         |
+ who is asking or the gateway to       +
| send the reply to                     |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag| reply_tunnelId    | size    |    |
+----+----+----+----+----+----+----+    +
| SHA256 of key1 to exclude             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                  +----+
|                                  |    |
+----+----+----+----+----+----+----+    +
| SHA256 of key2 to exclude             |
+                                       +
~                                       ~
+                                  +----+
|                                  |    |
+----+----+----+----+----+----+----+    +
|                                       |
+                                       +
|   Session key if reply encryption     |
+   was requested                       +
|                                       |
+                                  +----+
|                                  |tags|
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|   Session tags if reply encryption    |
+   was requested                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

key ::
    32 bytes
    SHA256 hash of the object to lookup

from ::
     32 bytes
     if deliveryFlag == 0, the SHA256 hash of the routerInfo entry this
                           request came from (to which the reply should be
                           sent)
     if deliveryFlag == 1, the SHA256 hash of the reply tunnel gateway (to
                           which the reply should be sent)

flags ::
     1 byte
     bit order: 76543210
     bit 0: deliveryFlag
             0  => send reply directly
             1  => send reply to some tunnel
     bit 1: encryptionFlag
             through release 0.9.5, must be set to 0
             as of release 0.9.6, ignored
             as of release 0.9.7:
             0  => send unencrypted reply
             1  => send AES encrypted reply using enclosed key and tag
     bits 3-2: lookup type flags
             through release 0.9.5, must be set to 00
             as of release 0.9.6, ignored
             as of release 0.9.16:
             00  => ANY lookup, return RouterInfo or LeaseSet or
                    DatabaseSearchReplyMessage. DEPRECATED.
                    Use LS or RI lookup as of 0.9.16.
             01  => LS lookup, return LeaseSet or
                    DatabaseSearchReplyMessage
                    As of release 0.9.38, may also return a
                    LeaseSet2, MetaLeaseSet, or EncryptedLeaseSet.
             10  => RI lookup, return RouterInfo or
                    DatabaseSearchReplyMessage
             11  => exploration lookup, return RouterInfo or
                    DatabaseSearchReplyMessage containing
                    non-floodfill routers only (replaces an
                    excludedPeer of all zeroes)
     bit 4: ECIESFlag
             before release 0.9.46 ignored
             as of release 0.9.46:
             0  => send unencrypted or ElGamal reply
             1  => send ChaCha/Poly encrypted reply using enclosed key
                   (whether tag is enclosed depends on bit 1)
     bits 7-5:
             through release 0.9.5, must be set to 0
             as of release 0.9.6, ignored, set to 0 for compatibility with
             future uses and with older routers

reply_tunnelId ::
               4 byte TunnelID
               only included if deliveryFlag == 1
               tunnelId of the tunnel to send the reply to, nonzero

size ::
     2 byte Integer
     valid range: 0-512
     number of peers to exclude from the DatabaseSearchReplyMessage

excludedPeers ::
              $size SHA256 hashes of 32 bytes each (total $size*32 bytes)
              if the lookup fails, these peers are requested to be excluded
              from the list in the DatabaseSearchReplyMessage.
              if excludedPeers includes a hash of all zeroes, the request is
              exploratory, and the DatabaseSearchReplyMessage is requested
              to list non-floodfill routers only.

reply_key ::
     32 byte key
     see below

tags ::
     1 byte Integer
     valid range: 1-32 (typically 1)
     the number of reply tags that follow
     see below

reply_tags ::
     one or more 8 or 32 byte session tags (typically one)
     see below
```
#### 回复加密

注意：从 API 0.9.58 开始，ElGamal router 已被弃用。由于现在建议查询的最低 floodfill 版本为 0.9.58，实现不需要为 ElGamal floodfill router 实现加密。ElGamal 目标仍然受支持。

标志位4与位1结合使用来确定回复加密模式。标志位4只能在发送给版本0.9.46或更高版本的router时设置。详细信息请参见提案154和156。

在下表中，"DH n/a"表示回复未加密。"DH no"表示回复密钥包含在请求中。"DH yes"表示回复密钥来源于DH操作。

<table style="border-collapse: collapse; width: 100%;">
<thead>
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">Flag bits 4,1</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">From</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">To Router</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">Reply</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">DH?</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">notes</th>
</tr>
</thead>
<tbody>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Any</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Any</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">no enc</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">n/a</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">no encryption</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ElG</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ElG</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">no</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">As of 0.9.7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ElG</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AEAD</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">no</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">As of 0.9.46</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AEAD</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">no</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">As of 0.9.49</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ElG</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">yes</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">TBD</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AEAD</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">yes</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">TBD</td>
</tr>
</tbody>
</table>
#### 无加密

reply_key、tags 和 reply_tags 不存在。

#### ElG 到 ElG

从 0.9.7 版本开始支持。从 0.9.58 版本开始弃用。ElG 目标向 ElG router 发送查找请求。

请求者密钥生成：

```
reply_key :: CSRNG(32) 32 bytes random data
reply_tags :: Each is CSRNG(32) 32 bytes random data
```
消息格式：

```
reply_key ::
     32 byte SessionKey big-endian
     only included if encryptionFlag == 1 AND ECIESFlag == 0, only as of release 0.9.7

tags ::
     1 byte Integer
     valid range: 1-32 (typically 1)
     the number of reply tags that follow
     only included if encryptionFlag == 1 AND ECIESFlag == 0, only as of release 0.9.7

reply_tags ::
     one or more 32 byte SessionTags (typically one)
     only included if encryptionFlag == 1 AND ECIESFlag == 0, only as of release 0.9.7
```
#### ECIES 到 ElG

自 0.9.46 版本开始支持。自 0.9.58 版本起已弃用。ECIES 目标节点向 ElG router 发送查找请求。reply_key 和 reply_tags 字段被重新定义用于 ECIES 加密的回复。

请求者密钥生成：

```
reply_key :: CSRNG(32) 32 bytes random data
reply_tags :: Each is CSRNG(8) 8 bytes random data
```
消息格式：重新定义 reply_key 和 reply_tags 字段如下：

```
reply_key ::
     32 byte ECIES SessionKey big-endian
     only included if encryptionFlag == 0 AND ECIESFlag == 1, only as of release 0.9.46

tags ::
     1 byte Integer
     required value: 1
     the number of reply tags that follow
     only included if encryptionFlag == 0 AND ECIESFlag == 1, only as of release 0.9.46

reply_tags ::
     an 8 byte ECIES SessionTag
     only included if encryptionFlag == 0 AND ECIESFlag == 1, only as of release 0.9.46
```
回复是一个 ECIES 现有会话消息，如 [ECIES](/docs/specs/ecies/) 中定义的那样。

#### 回复格式

这是现有的会话消息，与 [ECIES](/docs/specs/ecies/) 中的相同，以下复制供参考。

```
+----+----+----+----+----+----+----+----+
|       Session Tag                     |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+              (MAC)                    +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Session Tag :: 8 bytes, cleartext

Payload Section encrypted data :: remaining data minus 16 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
AEAD 参数：

```
tag :: 8 byte reply_tag

k :: 32 byte session key
   The reply_key.

n :: 0

ad :: The 8 byte reply_tag

payload :: Plaintext data, the DSM or DSRM.

ciphertext = ENCRYPT(k, n, payload, ad)
```
#### ECIES 到 ECIES (0.9.49)

ECIES 目标或 router 向 ECIES router 发送查找请求。自 0.9.49 版本起支持。

ECIES router 在 0.9.48 版本中引入，参见 [Proposal 156](/proposals/156/)。ECIES 目标和 router 可能使用与上述"ECIES 到 ElG"部分相同的格式，在请求中包含回复密钥。查找消息加密在 [ECIES-ROUTERS](/docs/specs/ecies-routers/) 中指定。请求者是匿名的。

#### ECIES 到 ECIES（未来）

此选项尚未完全定义。请参阅 [提案 156](/proposals/156/)。

#### 注意事项

- 在 0.9.16 版本之前，密钥可能用于 RouterInfo 或 LeaseSet，因为它们在同一个密钥空间中，并且没有标志来请求仅特定类型的数据。

- 自0.9.7版本起的加密标志、回复密钥和回复标签。

- 加密回复只有在响应通过tunnel传输时才有用。

- 如果实现了替代的 DHT 查找策略（例如递归查找），包含的标签数量可能大于一个。

- 查找密钥和排除密钥是"真实"的哈希值，而不是路由密钥。

- 从 0.9.38 版本开始，可能会返回类型 3、5 和 7。更多信息请参见提案 123。

- 探索性查找注意事项：探索性查找被定义为返回接近密钥的非 floodfill 哈希列表。但是，请参阅 DatabaseSearchReply 的重要注意事项了解实现变体。此外，本规范从未明确说明接收方是否应该查找搜索密钥以获取 RI，如果存在则返回 DatabaseStore 而不是 DSRM。Java 确实进行查找；i2pd 不进行。因此，不建议对先前接收的哈希使用探索性查找。

### DatabaseSearchReply {#msg-DatabaseSearchReply}

#### 描述

对失败的 [DatabaseLookup](#msg-DatabaseLookup) 消息的响应

#### 目录

与请求的密钥最接近的 router 哈希列表

```
+----+----+----+----+----+----+----+----+
| SHA256 hash as query key              |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| num| peer_hashes                      |
+----+                                  +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+----+----+----+
|    | from                             |
+----+                                  +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+----+----+----+
|    |
+----+

key ::
    32 bytes
    SHA256 of the object being searched

num ::
    1 byte Integer
    number of peer hashes that follow, 0-255

peer_hashes ::
          $num SHA256 hashes of 32 bytes each (total $num*32 bytes)
          SHA256 of the RouterIdentity that the other router thinks is close
          to the key

from ::
     32 bytes
     SHA256 of the RouterInfo of the router this reply was sent from
```
#### 注意事项

- 'from' 哈希值未经身份验证，不可信任。

- 返回的节点哈希值不一定比被查询的 router 更接近目标密钥。对于常规查找的回复，这有助于发现新的 floodfill 节点和进行"向后"搜索（远离密钥方向），以提高鲁棒性。

- 探索查找的密钥通常是随机生成的。因此，响应中的非 floodfill peer_hashes 可以使用优化算法进行选择，例如提供接近密钥但不一定是整个本地网络数据库中最近的节点，以避免对整个本地数据库进行低效的排序或搜索。缓存等其他策略也可能是合适的。这取决于具体实现。

- 典型返回的哈希数量：3

- 建议返回的最大哈希数量：16

- 查找密钥、对等节点哈希值和来源哈希值都是"真实"哈希值，而不是路由密钥。

### DeliveryStatus {#msg-DeliveryStatus}

#### 描述

一个简单的消息确认。通常由消息发起者创建，与消息本身一起包装在 Garlic Message 中，由目标节点返回。

此消息也用于隧道测试，发起方通过出站隧道将其发送至入站隧道，再返回自身。在此应用场景中，消息通常也经过大蒜加密（Garlic wrapped）。自 API 版本 0.9.68（2026-02）起，隧道测试成为必要要求，因为路由器被允许丢弃在前两分钟内未收到任何流量的参与隧道。

#### 目录

已传递消息的 ID，以及创建或到达时间。

```
+----+----+----+----+----+----+----+----+----+----+----+----+
| msg_id            |           time_stamp                  |
+----+----+----+----+----+----+----+----+----+----+----+----+

msg_id :: Integer
       4 bytes
       unique ID of the message we deliver the DeliveryStatus for (see
       I2NPMessageHeader for details)

time_stamp :: Date
             8 bytes
             time the message was successfully created or delivered
```
#### 注释

- 看起来时间戳总是由创建者设置为当前时间。然而代码中有几处使用了这个功能，将来可能会添加更多用途。

- 此消息还用作 SSU [SSU-ED](/docs/transports/ssu/#establishDirect) 中的会话建立确认。在这种情况下，消息 ID 设置为随机数，"到达时间"设置为当前网络范围 ID，即 2（即 0x0000000000000002）。

### Garlic {#msg-Garlic}

警告：此格式用于 ElGamal 加密的 garlic 消息 [CRYPTO-ELG](/docs/specs/cryptography/#elgamal)。ECIES-AEAD-X25519-Ratchet garlic 消息及 garlic cloves 的格式有显著不同；详见 [ECIES](/docs/specs/ecies/) 规范。

#### 描述

用于封装多个加密的 I2NP 消息

#### 目录

解密后，得到一系列[大蒜瓣](#struct-GarlicClove)和附加数据，也称为瓣集合（Clove Set）。

已加密：

```
+----+----+----+----+----+----+----+----+
|      length       | data              |
+----+----+----+----+                   +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

length ::
       4 byte Integer
       number of bytes that follow 0 - 64 KB

data ::
     $length bytes
     ElGamal encrypted data
```
解密后的数据，也称为Clove集合：

```
+----+----+----+----+----+----+----+----+
| num|  clove 1                         |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|         clove 2 ...                   |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Certificate  |   Message_ID      |
+----+----+----+----+----+----+----+----+
          Expiration               |
+----+----+----+----+----+----+----+

num ::
     1 byte Integer number of GarlicCloves to follow

clove ::  a GarlicClove

Certificate :: always NULL in the current implementation (3 bytes total, all zeroes)

Message_ID :: 4 byte Integer

Expiration :: Date (8 bytes)
```
#### 注释

- 当未加密时，数据包含一个或多个 [Garlic Cloves](#struct-GarlicClove)。

- AES加密块被填充到最少128字节；加上32字节的Session Tag，加密消息的最小大小为160字节；加上4个长度字节，Garlic Message的最小大小为164字节。

- 实际最大长度小于64 KB；请参见 [I2NP](/docs/protocol/i2np/)。

- 另请参见 [ElGamal/AES 规范](/docs/specs/elgamal-aes/)。

- 另请参阅[garlic routing 规范](/docs/overview/garlic-routing/)。

- AES 加密块的 128 字节最小大小目前不可配置，但是 GarlicMessage 中 GarlicClove 内 DataMessage 的最小大小（包含开销）本来就是 128 字节。未来可能会添加一个可配置选项来增加最小大小。

- 消息ID通常在发送时设置为随机数，在接收时似乎会被忽略。

- 在未来，证书可能会被用于 HashCash 来为路由进行"付费"。

### TunnelData {#msg-TunnelData}

#### 描述

从隧道的网关或参与者发送给下一个参与者或终点的消息。该数据具有固定长度，包含被分片、批量处理、填充并加密的 I2NP 消息。

#### 目录

```
+----+----+----+----+----+----+----+----+
|     tunnnelID     | data              |
+----+----+----+----+                   |
|                                       |
~                                       ~
~                                       ~
|                                       |
+                   +----+----+----+----+
|                   |
+----+----+----+----+

tunnelId ::
         4 byte TunnelId
         identifies the tunnel this message is directed at
         nonzero

data ::
     1024 bytes
     payload data.. fixed to 1024 bytes
```
#### 注释

- 此消息的 I2NP 消息 ID 在每一跳都设置为新的随机数。

- 另请参阅 [Tunnel Message Specification](/docs/legacy/tunnel-message/)

### TunnelGateway {#msg-TunnelGateway}

#### 描述

封装另一个 I2NP 消息，以便发送到隧道的入站网关。

#### 目录

```
+----+----+----+----+----+----+----+-//
| tunnelId          | length  | data...
+----+----+----+----+----+----+----+-//

tunnelId ::
         4 byte TunnelId
         identifies the tunnel this message is directed at
         nonzero

length ::
       2 byte Integer
       length of the payload

data ::
     $length bytes
     actual payload of this message
```
#### 注释

- 载荷是一个带有标准16字节头部的I2NP消息。

### 数据 {#msg-Data}

#### 描述

由大蒜消息（Garlic Messages）和大蒜瓣（Garlic Cloves）用于封装任意数据。

#### 目录

一个长度整数，后跟不透明数据。

```
+----+----+----+----+----+-//-+
| length            | data... |
+----+----+----+----+----+-//-+

length ::
       4 bytes
       length of the payload

data ::
     $length bytes
     actual payload of this message
```
#### 注释

- 此消息不包含路由信息，永远不会以"未包装"的形式发送。它只在 `Garlic` 消息内部使用。

### TunnelBuild {#msg-TunnelBuild}

已弃用，请使用 [VariableTunnelBuild](#msg-VariableTunnelBuild)

```
+----+----+----+----+----+----+----+----+
| Record 0 ...                          |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Record 1 ...                          |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Record 7 ...                          |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

Just 8 BuildRequestRecords attached together
record size: 528 bytes
total size: 8*528 = 4224 bytes
```
#### 注意事项

- 从 0.9.48 版本开始，也可能包含 ECIES-X25519 BuildRequestRecords，参见 [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/)。

- 另请参阅 [tunnel 创建规范](/docs/specs/tunnel-creation/)。

- 此消息的 I2NP 消息 ID 必须根据 tunnel 创建规范进行设置。

- 虽然这个消息在今天的网络中很少见到，已被`VariableTunnelBuild`消息取代，但它仍可能用于很长的tunnel，并且尚未被弃用。router必须实现。

### TunnelBuildReply {#msg-TunnelBuildReply}

已弃用，请使用 [VariableTunnelBuildReply](#msg-VariableTunnelBuildReply)

```
Same format as TunnelBuildMessage, with BuildResponseRecords
```
#### 注意事项

- 自 0.9.48 版本起，也可能包含 ECIES-X25519 BuildResponseRecords，参见 [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/)。

- 另请参阅 [tunnel 创建规范](/docs/specs/tunnel-creation/)。

- 此消息的 I2NP 消息 ID 必须根据 tunnel 创建规范进行设置。

- 虽然这个消息在今天的网络中很少见到，已经被 `VariableTunnelBuildReply` 消息所取代，但它仍可能用于非常长的 tunnel，并且尚未被弃用。router 必须实现。

### VariableTunnelBuild {#msg-VariableTunnelBuild}

```
+----+----+----+----+----+----+----+----+
| num| BuildRequestRecords...
+----+----+----+----+----+----+----+----+

Same format as TunnelBuildMessage, except for the addition of a $num field
in front and $num number of BuildRequestRecords instead of 8

num ::
       1 byte Integer
       Valid values: 1-8

record size: 528 bytes
total size: 1+$num*528
```
#### 注释

- 从 0.9.48 版本开始，可能还包含 ECIES-X25519 BuildRequestRecords，请参见 [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/)。

- 此消息在 router 版本 0.7.12 中引入，可能不会发送给早于该版本的 tunnel 参与者。

- 另请参见[tunnel创建规范](/docs/specs/tunnel-creation/)。

- 此消息的 I2NP 消息 ID 必须根据 tunnel 创建规范进行设置。

- 当今网络中记录的典型数量是4，总大小为2113。

### VariableTunnelBuildReply {#msg-VariableTunnelBuildReply}

```
+----+----+----+----+----+----+----+----+
| num| BuildResponseRecords...
+----+----+----+----+----+----+----+----+

Same format as VariableTunnelBuildMessage, with BuildResponseRecords.
```
#### 注释

- 从 0.9.48 版本开始，也可能包含 ECIES-X25519 BuildResponseRecords，参见 [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/)。

- 此消息在 router 版本 0.7.12 中引入，可能不会发送给早于该版本的 tunnel 参与者。

- 另请参阅 [tunnel 创建规范](/docs/specs/tunnel-creation/)。

- 此消息的 I2NP 消息 ID 必须根据 tunnel 创建规范进行设置。

- 在当前网络中，典型的记录数量是 4 个，总大小为 2113。

### ShortTunnelBuild {#msg-ShortTunnelBuild}

#### 描述

自 API 版本 0.9.51 起，仅适用于 ECIES-X25519 路由器。

```
+----+----+----+----+----+----+----+----+
| num| ShortBuildRequestRecords...
+----+----+----+----+----+----+----+----+

Same format as VariableTunnelBuildMessage,
except that the record size is 218 bytes instead of 528

num ::
       1 byte Integer
       Valid values: 1-8

record size: 218 bytes
total size: 1+$num*218
```
#### 注释

- 自 0.9.51 版本起。请参阅 [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/)。

- 此消息在 router 版本 0.9.51 中引入，可能不会发送给早于该版本的 tunnel 参与者。

- 当前网络中记录的典型数量是4个，总大小为873。

### OutboundTunnelBuildReply {#msg-OutboundTunnelBuildReply}

#### 描述

从新隧道的出站端点发送给发起方。自 API 版本 0.9.51 起，仅适用于 ECIES-X25519 路由器。

```
+----+----+----+----+----+----+----+----+
| num| ShortBuildResponseRecords...
+----+----+----+----+----+----+----+----+

Same format as ShortTunnelBuildMessage, with ShortBuildResponseRecords.
```
#### 注释

- 自 0.9.51 版本起。参见 [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/)。

- 当今网络中记录的典型数量是4个，总大小为873。

## 参考资料

- **[CRYPTO-ELG]** [密码学 - ElGamal](/docs/specs/cryptography/#elgamal)
- **[Date]** [通用结构 - 日期](/docs/specs/common-structures/#date)
- **[ECIES]** [ECIES 规范](/docs/specs/ecies/)
- **[ECIES-ROUTERS]** [ECIES Router 规范](/docs/specs/ecies-routers/)
- **[ElG-AES]** [ElGamal/AES](/docs/specs/elgamal-aes/)
- **[GARLICSPEC]** [Garlic 路由](/docs/overview/garlic-routing/)
- **[Hash]** [通用结构 - 哈希](/docs/specs/common-structures/#hash)
- **[I2NP]** [I2NP 协议](/docs/protocol/i2np/)
- **[Integer]** [通用结构 - 整数](/docs/specs/common-structures/#integer)
- **[NTCP2]** [NTCP2 规范](/docs/specs/ntcp2/)
- **[Prop156]** [提案 156](/proposals/156/)
- **[Prop157]** [提案 157](/proposals/157/)
- **[RouterIdentity]** [通用结构 - RouterIdentity](/docs/specs/common-structures/#routeridentity)
- **[SSU]** [SSU 传输](/docs/transports/ssu/)
- **[SSU-ED]** [SSU 传输 - 建立直连](/docs/transports/ssu/#establishDirect)
- **[SSU2]** [SSU2 规范](/docs/specs/ssu2/)
- **[TMDI]** [Tunnel 消息传递指令](/docs/legacy/tunnel-message/#tunnel-message-delivery-instructions)
- **[TUNNEL-CREATION]** [Tunnel 创建规范](/docs/specs/tunnel-creation/)
- **[TUNNEL-CREATION-ECIES]** [ECIES Tunnel 创建](/docs/specs/tunnel-creation-ecies/)
- **[TUNNEL-IMPL]** [Tunnel 实现](/docs/specs/tunnel-implementation/)
- **[TUNNEL-MSG]** [Tunnel 消息规范](/docs/legacy/tunnel-message/)
- **[TunnelId]** [通用结构 - TunnelId](/docs/specs/common-structures/#tunnelid)
