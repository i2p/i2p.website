---
title: "SAM V1 规范"
description: "传统简单匿名消息协议版本1（已弃用）"
slug: "sam"
aliases:
  - "/zh/docs/api/sam"
  - "/zh/docs/api/sam/"
  - "/zh/sam"
  - "/zh/sam/"
lastUpdated: "2025-03"
accurateFor: "0.9.20"
---

## 警告 - 已弃用 - 不支持 - 请使用 [SAMv3](/docs/api/samv3)

以下规定的是与 I2P 交互的简单客户端协议的第 1 版。更新的替代方案：[SAM V2](/docs/api/samv2)、[SAM V3](/docs/api/samv3)、[BOB](/docs/api/bob)。

## SAMv1 API 的语言库

- C
- C#
- Perl
- Python

这些库位于 I2P 源代码仓库中。

### I2P 0.9.14 更改

报告的版本仍然是"1.0"。

- DEST GENERATE 现在支持 SIGNATURE_TYPE 参数。
- HELLO VERSION 中的 MIN 参数现在是可选的。
- HELLO VERSION 中的 MIN 和 MAX 参数现在支持单位数版本，例如"3"。

## 版本 1 协议

客户端应用程序与SAMv3桥接器通信，该桥接器处理所有I2P功能（使用流库处理虚拟流，或直接使用I2CP处理异步消息）。

所有客户端\<--\>SAM bridge通信都是通过单个TCP套接字进行的未加密和未认证通信。应该通过防火墙或其他方式保护对SAM bridge的访问（也许bridge可以设置ACL来控制接受连接的IP地址）。

所有这些 SAM 消息都在单行纯 ASCII 中发送，以换行符（\\n）结尾。下面显示的格式仅为了可读性，虽然每条消息中的前两个词必须保持其特定顺序，但键值对的顺序可以改变（例如 "ONE TWO A=B C=D" 或 "ONE TWO C=D A=B" 都是完全有效的构造）。此外，协议区分大小写。

SAM 消息以 UTF-8 编码解释。键=值对必须用单个空格分隔。如果值包含空格，可以用双引号括起来，例如 key="long value text"。没有转义机制。

通信可以采用三种不同的形式：

- [虚拟流](/docs/api/streaming)
- [可回复数据报](/docs/specs/datagrams#repliable)（带有FROM字段的消息）
- [匿名数据报](/docs/specs/datagrams#raw)（原始匿名消息）

## SAM 连接握手

在客户端和网桥就协议版本达成一致之前，不能进行任何SAM通信，这是通过客户端发送HELLO消息和网桥发送HELLO REPLY消息来完成的：

```
HELLO VERSION MIN=$min MAX=$max
```
和

```
HELLO REPLY RESULT=$result VERSION=1.0
```
从 I2P 0.9.14 开始，MIN 参数是可选的。必须提供 MAX 参数，且必须大于或等于"1"并小于"2"才能使用版本 1。

RESULT 值可能是以下之一：

- `OK`
- `NOVERSION`

## SAM 会话

SAM 会话是通过客户端打开到 SAM 桥接器的套接字、执行握手并发送 SESSION CREATE 消息来创建的，当套接字断开连接时会话终止。

每个 I2P Destination 一次只能用于一个 SAM 会话，并且只能使用其中一种形式（通过其他形式接收的消息将被丢弃）。

客户端发送给桥接的 SESSION CREATE 消息如下：

```
SESSION CREATE
        STYLE={STREAM,DATAGRAM,RAW}
        DESTINATION={$name,TRANSIENT}
        [DIRECTION={BOTH,RECEIVE,CREATE}]
        [option=value]*
```
DESTINATION 指定用于发送和接收消息/流的目标。如果给定了 $name，SAM bridge 会在其本地存储（sam.keys 文件）中查找关联的目标（和私钥）。如果不存在匹配该名称的关联，它会创建一个新的。如果目标指定为 TRANSIENT，它总是创建一个新的。

请注意，DESTINATION 是一个标识符，*不是* Base 64 编码的数据。要指定 Destination，您必须使用 [SAM V3](/docs/api/samv3)。

DIRECTION 只能为 STREAM 会话指定，用于告知网桥客户端将创建或接收流，或者两者都有。如果未指定，将假定为 BOTH。当 DIRECTION=RECEIVE 时尝试创建出站流应该会导致错误，当 DIRECTION=CREATE 时传入的流将被忽略。

如果提供的附加选项未被SAM桥接器解释，则应将其传递到I2P会话配置中（例如"tunnels.depthInbound=0"）。这些选项在下文中有详细说明。

SAM bridge 本身应该已经配置了通过哪个 router 进行 I2P 通信（不过如果需要的话，可能有方法进行覆盖，例如 i2cp.tcp.host=localhost 和 i2cp.tcp.port=7654）。

收到会话创建消息后，SAM 桥接将回复会话状态消息，如下所示：

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

如果不正常，MESSAGE 应该包含关于为什么无法创建会话的人类可读信息。

请注意，如果未找到 $name 并创建了临时目标，系统不会给出警告。请注意，实际的临时 base 64 目标不会在回复中输出；输出的是在 SESSION CREATE 中提供的 $name 或 TRANSIENT。如果您需要这些功能，必须使用 [SAM V3](/docs/api/samv3)。

## SAM 虚拟流

虚拟流保证可靠且有序地发送，并在可用时立即提供失败和成功通知。

在使用 STYLE=STREAM 建立会话后，客户端和 SAM 桥都可以异步地来回发送各种消息来管理流，如下所示：

```
STREAM CONNECT
       ID=$id
       DESTINATION=$destination
```
这会从本地目的地到指定对等节点建立一个新的虚拟连接，并使用会话范围内的唯一ID对其进行标记。唯一ID是一个ASCII base 10整数，范围从1到(2^31-1)。

$destination 是 [Destination](/docs/specs/common-structures#type_Destination) 的 base 64 编码，根据签名类型不同，包含 516 个或更多的 base 64 字符（二进制格式为 387 个或更多字节）。

SAM bridge 必须用流状态消息回复此请求：

```
STREAM STATUS
       RESULT=$result
       ID=$id
       [MESSAGE=...]
```
RESULT 值可能是以下之一：

- `OK`
- `CANT_REACH_PEER`
- `I2P_ERROR`
- `INVALID_KEY`
- `TIMEOUT`

如果 RESULT 为 OK，则表示指定的目标已启动并授权了连接；如果无法建立连接（超时等），RESULT 将包含相应的错误值（可选择性地附带人类可读的 MESSAGE）。

在接收端，SAM 桥简单地按如下方式通知客户端：

```
STREAM CONNECTED
       DESTINATION=$destination
       ID=$id
```
这告诉客户端给定的目标已与它们创建了虚拟连接。后续的数据流将用给定的唯一ID标记，该ID是从-1到-(2^31-1)的ASCII十进制整数。

$destination 是 [Destination](/docs/specs/common-structures#type_Destination) 的 base 64 编码，根据签名类型不同，包含 516 个或更多 base 64 字符（二进制格式为 387 个或更多字节）。

当客户端想要在虚拟连接上发送数据时，操作如下：

```
STREAM SEND
       ID=$id
       SIZE=$numBytes\n[$numBytes of data]
```
这会将指定的数据添加到通过虚拟连接发送给对等方的缓冲区中。发送大小 $numBytes 是换行符后包含的 8 位字节数，可以是 1 到 32768（32KB）。

然后 SAM bridge 会尽力以最快最高效的方式传递消息，可能会将多个 SEND 消息缓冲在一起。如果传递数据时出现错误，或者远程端关闭连接，SAM bridge 会告知客户端：

```
STREAM CLOSED
       RESULT=$result
       ID=$id
       [MESSAGE=...]
```
RESULT 值可能是以下之一：

- `OK`
- `CANT_REACH_PEER`
- `I2P_ERROR`
- `PEER_NOT_FOUND`
- `TIMEOUT`

如果连接已被对等方正常关闭，$result 设置为 OK。如果 $result 不是 OK，MESSAGE 可能会传达描述性消息，如"peer unreachable"等。当客户端想要关闭连接时，它们向 SAM bridge 发送关闭消息：

```
STREAM CLOSE
       ID=$id
```
bridge随后清理所需的资源并丢弃该ID - 无法在其上发送或接收更多消息。

对于通信的另一端，每当对等节点发送了一些数据并且客户端可以接收时，SAM 桥接器会立即将其传递：

```
STREAM RECEIVED
       ID=$id
       SIZE=$numBytes\n[$numBytes of data]
```
当SAM bridge与客户端之间的连接断开时，所有流都会被隐式关闭。

## SAM 可回复数据报

虽然I2P本身不包含FROM地址，但为了便于使用，提供了一个额外的层作为可回复数据报——无序且不可靠的消息，最大可达31744字节，包含FROM地址（为头部材料留出最多1KB空间）。此FROM地址由SAM在内部进行身份验证（利用目标的签名密钥来验证源），并包含重放防护。

最小大小为1。为获得最佳传输可靠性，建议最大大小约为11 KB。

在使用 STYLE=DATAGRAM 建立 SAM 会话后，客户端可以向 SAM 桥发送：

```
DATAGRAM SEND
         DESTINATION=$destination
         SIZE=$numBytes\n[$numBytes of data]
```
当数据报到达时，网桥通过以下方式将其传递给客户端：

```
DATAGRAM RECEIVED
         DESTINATION=$destination
         SIZE=$numBytes\n[$numBytes of data]
```
$destination 是 [Destination](/docs/specs/common-structures#type_Destination) 的 base 64 编码，长度为 516 个或更多 base 64 字符（二进制格式为 387 个或更多字节），具体取决于签名类型。

SAM bridge 从不向客户端暴露身份验证标头或其他字段，仅传递发送方提供的数据。这种情况会持续到会话关闭（由客户端断开连接）。

## SAM 匿名数据报

为了最大化利用I2P的带宽，SAM允许客户端发送和接收匿名数据报，将身份验证和回复信息留给客户端自己处理。这些数据报是不可靠且无序的，最大可达32768字节。

最小大小为 1。为了获得最佳传输可靠性，建议最大大小约为 11 KB。

在建立STYLE=RAW的SAM会话后，客户端可以向SAM桥发送：

```
RAW SEND
    DESTINATION=$destination
    SIZE=$numBytes\n[$numBytes of data]
```
$destination 是 [Destination](/docs/specs/common-structures#type_Destination) 的 base 64 编码，根据签名类型不同，包含 516 个或更多 base 64 字符（二进制形式为 387 字节或更多）。

当原始数据报到达时，桥接器通过以下方式将其传递给客户端：

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
由以下回答

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

如果 NAME=ME，那么回复将包含当前会话使用的目标地址（在使用 TRANSIENT 会话时很有用）。如果 $result 不是 OK，MESSAGE 可能会包含描述性消息，如 "bad format" 等。

$destination 是 [Destination](/docs/specs/common-structures#type_Destination) 的 base 64 编码，根据签名类型不同，包含 516 个或更多 base 64 字符（二进制格式为 387 字节或更多）。

可以使用以下消息生成公钥和私钥的 base64 密钥：

```
DEST GENERATE
```
其回答是

```
DEST REPLY
     PUB=$destination
     PRIV=$privkey
```
从 I2P 0.9.14 开始，支持可选参数 SIGNATURE_TYPE。SIGNATURE_TYPE 值可以是任何受 [Key Certificates](/docs/specs/common-structures#type_Certificate) 支持的名称（例如 ECDSA_SHA256_P256，不区分大小写）或数字（例如 1）。默认值是 DSA_SHA1。

$destination 是 [Destination](/docs/specs/common-structures#type_Destination) 的 base 64 编码，根据签名类型不同，长度为 516 个或更多 base 64 字符（二进制格式为 387 个或更多字节）。

$privkey 是 [Destination](/docs/specs/common-structures#type_Destination) 后跟 [Private Key](/docs/specs/common-structures#type_PrivateKey) 再跟 [Signing Private Key](/docs/specs/common-structures#type_SigningPrivateKey) 连接后的 base 64 编码，根据签名类型不同，长度为 884 个或更多 base 64 字符（二进制为 663 个或更多字节）。

## RESULT 值

这些是 RESULT 字段可以携带的值及其含义：

| Value | Meaning |
|-------|---------|
| `OK` | 操作成功完成 |
| `CANT_REACH_PEER` | 对等节点存在，但无法到达 |
| `DUPLICATED_DEST` | 指定的目标地址已在使用中 |
| `I2P_ERROR` | 通用 I2P 错误（例如 I2CP 断开连接等） |
| `INVALID_KEY` | 指定的密钥无效（格式错误等） |
| `KEY_NOT_FOUND` | 命名系统无法解析给定名称 |
| `PEER_NOT_FOUND` | 在网络上找不到对等节点 |
| `TIMEOUT` | 等待事件时超时（例如对等节点响应） |
## Tunnel、I2CP 和流传输选项

这些选项可以作为 name=value 键值对传递到 SAM SESSION CREATE 行的末尾。

所有会话都可以包含 [I2CP 选项，如 tunnel 长度](/docs/protocol/i2cp#options)。STREAM 会话可以包含 [Streaming lib 选项](/docs/api/streaming#options)。请参考这些参考文档了解选项名称和默认值。

## Base 64 说明

Base 64 编码必须使用 I2P 标准 Base 64 字母表 "A-Z, a-z, 0-9, -, ~"。

## 客户端库实现

客户端库可用于 C、C++、C#、Perl 和 Python。这些库位于 I2P 源码包的 apps/sam/ 目录中。

## 默认 SAM 设置

默认的 SAM 端口是 7656。在 I2P Router 中，SAM 默认不启用；必须在路由器控制台的配置客户端页面或在 clients.config 文件中手动启动或配置为自动启动。
