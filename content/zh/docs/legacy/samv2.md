---
title: "SAM V2 规范"
description: "传统简单匿名消息协议版本 2（已弃用）"
slug: "samv2"
aliases:
  - "/zh/docs/api/samv2"
  - "/zh/docs/api/samv2/"
  - "/zh/samv2"
  - "/zh/samv2/"
lastUpdated: "2025-03"
accurateFor: "0.9.20"
---

## 警告 - 已弃用 - 不支持 - 请使用 [SAMv3](/docs/api/samv3)

下面规定的是与 I2P 交互的简单客户端协议的第 2 版。

SAM V2 在 I2P 0.6.1.31 版本中引入。与 SAM V1 的重大差异用 "\*\*\*" 标记。替代方案：[SAM V1](/docs/api/sam)、[SAM V3](/docs/api/samv3)、[BOB](/docs/api/bob)。

## 版本 2 变更

SAM V2 在 I2P 版本 0.6.1.31 中引入。与版本 1 相比，SAM v2 提供了一种在同一个 I2P 目标上*并行*管理多个套接字的方法，即客户端不必等待一个套接字上的数据成功发送后才能在另一个套接字上发送数据。所有数据都通过同一个客户端\<--\>SAM 套接字传输。对于多套接字，请参见 [SAM V3](/docs/api/samv3)。

### I2P 0.9.14 变更

报告的版本仍为"2.0"。

- DEST GENERATE 现在支持 SIGNATURE_TYPE 参数。
- HELLO VERSION 中的 MIN 参数现在是可选的。
- HELLO VERSION 中的 MIN 和 MAX 参数现在支持单数字版本，如 "3"。

## 版本 2 协议

客户端应用程序与SAMv3桥接器通信，由桥接器处理所有I2P功能（使用流媒体库处理虚拟流，或直接使用I2CP处理异步消息）。

所有客户端<-->SAM桥接的通信都是通过单个TCP套接字进行的未加密和未认证传输。对SAM桥接的访问应该通过防火墙或其他方式进行保护（也许桥接可以通过ACL来控制接受来自哪些IP的连接）。

所有这些SAM消息都通过单行纯ASCII发送，以换行符（\\n）结尾。下面显示的格式仅为了可读性，虽然每条消息中的前两个单词必须保持其特定顺序，但键值对的顺序可以改变（例如"ONE TWO A=B C=D"或"ONE TWO C=D A=B"都是完全有效的结构）。此外，协议是大小写敏感的。

SAM消息使用UTF-8编码解析。键值对必须用单个空格分隔。如果值包含空格，可以用双引号包围，例如key="long value text"。没有转义机制。

通信可以采用三种不同的形式：

- [虚拟流](/docs/api/streaming)
- [可回复数据报](/docs/specs/datagrams#repliable)（带有 FROM 字段的消息）
- [匿名数据报](/docs/specs/datagrams#raw)（原始匿名消息）

## SAM 连接握手

在客户端和桥接器就协议版本达成一致之前，无法进行 SAM 通信，这通过客户端发送 HELLO 和桥接器发送 HELLO REPLY 来完成：

```
HELLO VERSION MIN=$min MAX=$max
```
和

```
*** HELLO REPLY RESULT=$result VERSION=2.0
```
从 I2P 0.9.14 版本开始，MIN 参数是可选的。必须提供 MAX 参数，且必须大于或等于 "2" 并小于 "3" 才能使用版本 2。

RESULT 值可能是以下之一：

- `OK`
- `NOVERSION`

## SAM 会话

SAM 会话通过客户端打开到 SAM 桥接器的套接字、执行握手并发送 SESSION CREATE 消息来创建，当套接字断开连接时会话终止。

每个 I2P Destination 一次只能用于一个 SAM 会话，并且只能使用其中一种形式（通过其他形式接收的消息会被丢弃）。

客户端发送给桥接器的 SESSION CREATE 消息如下：

```
SESSION CREATE
        STYLE={STREAM,DATAGRAM,RAW}
        DESTINATION={$name,TRANSIENT}
        [DIRECTION={BOTH,RECEIVE,CREATE}]
        [option=value]*
```
DESTINATION 指定用于发送和接收消息/流的目标地址。如果给出 $name，SAM 桥接会在其本地存储（sam.keys 文件）中查找相关联的 destination（和私钥）。如果不存在与该名称匹配的关联，它会创建一个新的。如果 destination 指定为 TRANSIENT，它总是创建一个新的。

注意 DESTINATION 是一个标识符，*不是* Base 64 编码的数据。要指定 Destination，您必须使用 [SAM V3](/docs/api/samv3)。

DIRECTION 只能为 STREAM 会话指定，用于指示桥接器客户端将创建或接收流，或者两者都进行。如果未指定，将假定为 BOTH。当 DIRECTION=RECEIVE 时尝试创建出站流应该会导致错误，当 DIRECTION=CREATE 时传入的流将被忽略。

给出的其他选项如果不被SAM桥接器解释，应该输入到I2P会话配置中（例如"tunnels.depthInbound=0"）。这些选项在下面有说明文档。

SAM bridge 本身应该已经配置好了它应该通过哪个 router 在 I2P 上进行通信（不过如果需要的话，可能有办法提供覆盖设置，例如 i2cp.tcp.host=localhost 和 i2cp.tcp.port=7654）。

在收到会话创建消息后，SAM桥将回复一个会话状态消息，如下所示：

```
SESSION STATUS
        RESULT=$result
        DESTINATION={$name,TRANSIENT}
        [MESSAGE=...]
```
RESULT 值可能是以下之一：

- `OK`
- `DUPLICATED_DEST`
- `I2P_ERROR`
- `INVALID_KEY`

如果不正常，MESSAGE 应该包含人类可读的信息，说明为什么无法创建会话。

注意，如果未找到 $name 并创建了临时目标地址，系统不会给出警告。注意在回复中不会输出实际的临时 base 64 目标地址；输出的是 SESSION CREATE 中提供的 $name 或 TRANSIENT。如果您需要这些功能，必须使用 [SAM V3](/docs/api/samv3)。

## SAM 虚拟流

虚拟流保证可靠有序地发送，并在可用时立即提供失败和成功通知。

在建立STYLE=STREAM会话后，客户端和SAM桥接都可以异步地相互发送各种消息来管理流，如下所列：

```
STREAM CONNECT
       ID=$id
       DESTINATION=$destination
```
这会从本地目标到指定对等节点建立一个新的虚拟连接，并用会话范围内的唯一ID对其进行标记。唯一ID是一个从1到(2^31-1)的ASCII十进制整数。

$destination 是 [Destination](/docs/specs/common-structures#type_Destination) 的 base 64 编码，根据签名类型的不同，包含 516 个或更多的 base 64 字符（二进制形式为 387 个或更多字节）。

SAM bridge 会回复一个流状态消息：

```
STREAM STATUS
       RESULT=$result
       ID=$id
       [MESSAGE=...]
```
RESULT 值可能为以下之一：

- `OK`
- `CANT_REACH_PEER`
- `I2P_ERROR`
- `INVALID_KEY`
- `TIMEOUT`

如果 RESULT 为 OK，表示指定的目标地址在线且已授权连接；如果连接不可能（超时等），RESULT 将包含相应的错误值（并附带可选的人类可读 MESSAGE）。

在接收端，SAM bridge 只是简单地通知客户端如下：

```
STREAM CONNECTED
       DESTINATION=$destination
       ID=$id
```
这告诉客户端给定的目标已经与它们建立了虚拟连接。后续的数据流将用给定的唯一ID进行标记，该ID是一个ASCII base 10整数，范围从-1到-(2^31-1)。

$destination 是 [Destination](/docs/specs/common-structures#type_Destination) 的 base 64 编码，根据签名类型不同，包含 516 个或更多 base 64 字符（二进制形式为 387 个或更多字节）。

当客户端想要在虚拟连接上发送数据时，它们按以下方式进行：

```
STREAM SEND
       ID=$id
       SIZE=$numBytes\n[$numBytes of data]
```
这要求 SAM bridge 将指定的数据添加到通过虚拟连接发送给对等节点的缓冲区中。发送大小 $numBytes 是换行符后包含的 8 位字节数，可以是 1 到 32768 (32KB)。

**\*\*\* SAM bridge 立即回复：**

```
*** STREAM SEND
***        ID=$id
***        RESULT=$result
***        STATE=$bufferState
```
**\*\*\*** 其中 $bufferState 可以是：

- `BUFFER_FULL` - SAM的缓冲区有32KB或更多数据要发送，后续的SEND请求将失败
- `READY` - SAM的缓冲区未满，下一个SEND请求将被批准成功

**\*\*\*** 并且 $result 是以下之一：

- `OK` - 数据已成功缓冲
- `FAILED` - 缓冲区已满，没有数据被缓冲

**\*\*\*** 如果 SAM bridge 回复了 BUFFER_FULL，它会在缓冲区再次可用时立即发送另一条消息：

```
*** STREAM READY_TO_SEND ID=$id
```
**\*\*\*** 当结果为OK时，SAM桥接器将尽力以最快、最高效的方式传递消息，可能会将多个SEND消息缓冲在一起。如果传递数据时出现错误，或者远程端关闭了连接，SAM桥接器将告知客户端：

```
STREAM CLOSED
       RESULT=$result
       ID=$id
       [MESSAGE=...]
```
RESULT值可能是以下之一：

- `OK`
- `CANT_REACH_PEER`
- `I2P_ERROR`
- `PEER_NOT_FOUND`
- `TIMEOUT`

如果连接已被对等节点正常关闭，$result 将设置为 OK。如果 $result 不是 OK，MESSAGE 可能会传达描述性消息，如"peer unreachable"等。当客户端想要关闭连接时，他们向 SAM bridge 发送关闭消息：

```
STREAM CLOSE
       ID=$id
```
然后bridge清理所需的内容并丢弃该ID - 无法在其上发送或接收进一步的消息。

对于通信的另一端，每当对等节点发送了一些数据并且客户端可以接收时，SAM桥接器会立即传递这些数据：

```
STREAM RECEIVED
       ID=$id
       SIZE=$numBytes\n[$numBytes of data]
```
**\*\*\*** 但是在SAM版本2.0中，客户端必须首先通过发送消息告诉SAM桥接器整个会话允许多少传入数据：

```
*** STREAM RECEIVE
***        ID=$id
***        LIMIT=$limit\n
```
**\*\*\*** 其中 $limit 可以是：

- `NONE` - SAM桥接将继续监听并传递传入数据（与1.0版本中的行为相同）
- 一个整数（小于2^64）- 接收字节数的限制，达到此数量后SAM桥接将停止在传入流上监听。当客户端准备好从流中接受更多字节时，它必须再次发送这样的消息，使用更大的$limit值。

**\*\*\*** 客户端必须在与对等节点的连接建立后发送此类 STREAM RECEIVE 消息，即在客户端从 SAM 桥接收到 "STREAM CONNECTED" 或 "STREAM STATUS RESULT=OK" 之后。

当SAM桥接和客户端之间的连接断开时，所有流都会被隐式关闭。

## SAM 可回复数据报

虽然I2P本身不包含FROM地址，但为了使用方便，提供了一个额外的层作为可回复数据报——无序且不可靠的消息，最大31744字节，包含FROM地址（为头部材料留出最多1KB空间）。这个FROM地址由SAM内部认证（利用destination的签名密钥验证源），并包含重放防护。

最小大小为 1。为了获得最佳传输可靠性，建议最大大小约为 11 KB。

在建立 STYLE=DATAGRAM 的 SAM 会话后，客户端可以向 SAM 网桥发送：

```
DATAGRAM SEND
         DESTINATION=$destination
         SIZE=$numBytes\n[$numBytes of data]
```
当数据报到达时，桥接通过以下方式将其传递给客户端：

```
DATAGRAM RECEIVED
         DESTINATION=$destination
         SIZE=$numBytes\n[$numBytes of data]
```
$destination 是 [Destination](/docs/specs/common-structures#type_Destination) 的 base 64 编码，根据签名类型，长度为 516 个或更多 base 64 字符（二进制形式为 387 个或更多字节）。

SAM bridge 永远不会向客户端暴露认证头部或其他字段，仅提供发送方提供的数据。这种状态会持续到会话关闭（通过客户端断开连接）。

## SAM 匿名数据报

为了最大限度地利用I2P的带宽，SAM允许客户端发送和接收匿名数据报，将身份验证和回复信息交给客户端自己处理。这些数据报是不可靠且无序的，最大可达32768字节。

最小大小为 1。为获得最佳传输可靠性，建议最大大小约为 11 KB。

在使用 STYLE=RAW 建立 SAM 会话后，客户端可以向 SAM 网桥发送：

```
RAW SEND
    DESTINATION=$destination
    SIZE=$numBytes\n[$numBytes of data]
```
$destination 是 [Destination](/docs/specs/common-structures#type_Destination) 的 base 64 编码，根据签名类型不同，包含 516 个或更多 base 64 字符（二进制格式为 387 个或更多字节）。

当原始数据报到达时，网桥通过以下方式将其传递给客户端：

```
RAW RECEIVED
    SIZE=$numBytes\n[$numBytes of data]
```
## SAM 实用功能

客户端可以使用以下消息向 SAM bridge 查询名称解析：

```
NAMING LOOKUP
       NAME=$name
```
其回答是

```
NAMING REPLY
       RESULT=$result
       NAME=$name
       [VALUE=$destination]
       [MESSAGE=$message]
```
RESULT 值可能是以下之一：

- `OK`
- `INVALID_KEY`
- `KEY_NOT_FOUND`

如果 NAME=ME，则回复将包含当前会话使用的目标地址（如果你使用的是 TRANSIENT 地址，这很有用）。如果 $result 不是 OK，MESSAGE 可能包含描述性消息，比如 "bad format" 等。

$destination 是 [Destination](/docs/specs/common-structures#type_Destination) 的 base 64 编码，根据签名类型不同，包含 516 个或更多的 base 64 字符（二进制形式为 387 个或更多字节）。

可以使用以下消息生成公钥和私钥的base64格式：

```
DEST GENERATE
```
由以下内容回答

```
DEST REPLY
     PUB=$destination
     PRIV=$privkey
```
自 I2P 0.9.14 版本起，支持可选参数 SIGNATURE_TYPE。SIGNATURE_TYPE 值可以是任何受 [Key Certificates](/docs/specs/common-structures#type_Certificate) 支持的名称（例如 ECDSA_SHA256_P256，不区分大小写）或数字（例如 1）。默认值为 DSA_SHA1。

$destination 是 [Destination](/docs/specs/common-structures#type_Destination) 的 base 64 编码，根据签名类型不同，包含 516 个或更多 base 64 字符（二进制格式为 387 个或更多字节）。

$privkey 是 [Destination](/docs/specs/common-structures#type_Destination) 后跟 [Private Key](/docs/specs/common-structures#type_PrivateKey) 再后跟 [Signing Private Key](/docs/specs/common-structures#type_SigningPrivateKey) 连接后的 base 64 编码，长度为 884 个或更多 base 64 字符（二进制格式为 663 个或更多字节），具体取决于签名类型。

## RESULT 值

以下是 RESULT 字段可以携带的值及其含义：

| Value | Meaning |
|-------|---------|
| `OK` | 操作成功完成 |
| `CANT_REACH_PEER` | 对等节点存在，但无法到达 |
| `DUPLICATED_DEST` | 指定的目标地址已在使用中 |
| `I2P_ERROR` | 通用 I2P 错误（例如 I2CP 连接断开等） |
| `INVALID_KEY` | 指定的密钥无效（格式错误等） |
| `KEY_NOT_FOUND` | 命名系统无法解析给定的名称 |
| `PEER_NOT_FOUND` | 在网络上找不到该对等节点 |
| `TIMEOUT` | 等待事件时超时（例如对等节点响应） |
## Tunnel、I2CP 和流选项

这些选项可以在 SAM SESSION CREATE 行的末尾以 name=value 对的形式传递。

所有会话都可以包含[I2CP选项，如tunnel长度](/docs/protocol/i2cp#options)。STREAM会话可以包含[Streaming库选项](/docs/api/streaming#options)。请参阅这些参考资料了解选项名称和默认值。

## Base 64 注释

Base 64 编码必须使用 I2P 标准 Base 64 字母表 "A-Z, a-z, 0-9, -, ~"。

## 客户端库实现

客户端库支持 C、C++、C#、Perl 和 Python。这些库位于 I2P 源码包的 apps/sam/ 目录中。其中一些可能较旧，尚未更新以支持 SAMv2。

## 默认 SAM 设置

默认的 SAM 端口是 7656。SAM 在 I2P Router 中默认不启用；必须手动启动，或在路由器控制台的配置客户端页面中配置为自动启动，或在 clients.config 文件中配置。
