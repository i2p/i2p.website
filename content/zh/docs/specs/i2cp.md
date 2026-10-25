---
title: "I2P 客户端协议 (I2CP)"
description: "应用程序如何与 I2P router 协商会话、tunnel 和 leaseSet。"
slug: "i2cp"
aliases:
  - "/zh/docs/api/i2cp"
  - "/zh/docs/api/i2cp/"
  - "/zh/docs/specs/i2cp-spec"
  - "/zh/docs/specs/i2cp-spec/"
category: "协议"
lastUpdated: "2025-07"
accurateFor: "0.9.67"
---

## 概述

这是 I2P Control Protocol (I2CP) 的规范，它是客户端和 router 之间的低级接口。Java 客户端将使用 I2CP 客户端 API，该 API 实现了此协议。

目前没有已知的非Java实现的客户端库来实现I2CP。此外，面向套接字的（流式）应用程序需要流协议的实现，但也没有非Java库可用。因此，非Java客户端应该使用更高层的协议SAM [SAMv3](/docs/api/samv3/)，该协议有多种语言的库可用。

这是一个低级协议，Java I2P router内部和外部都支持。只有当客户端和router不在同一个JVM中时，该协议才会被序列化；否则，I2CP消息Java对象会通过内部JVM接口传递。C++ router i2pd也在外部支持I2CP。

更多信息请参见 I2CP 概览页面 [I2CP](/docs/specs/i2cp/)。

## 会话

该协议设计用于在单个TCP连接上处理多个"会话"，每个会话都有一个2字节的会话ID，但是，多会话功能直到0.9.21版本才实现。请参阅[下面的多会话部分](#multisession)。不要尝试在0.9.21版本之前的router上的单个I2CP连接中使用多个会话。

似乎还有一些规定允许单个客户端通过不同连接与多个 router 通信。这也未经测试，可能没有实用价值。

断开连接后无法维护会话，也无法在不同的I2CP连接上恢复会话。当套接字关闭时，会话即被销毁。

## 示例消息序列

注意：下面的示例不显示客户端首次连接到 router 时必须发送的协议字节 (0x2a)。有关连接初始化的更多信息请参见 I2CP 概述页面 [I2CP](/docs/specs/i2cp/)。

### 标准会话建立

```
  Client                                           Router

                           --------------------->  Get Date Message
        Set Date Message  <---------------------
                           --------------------->  Create Session Message
  Session Status Message  <---------------------
Request LeaseSet Message  <---------------------
                           --------------------->  Create LeaseSet Message

```
### 获取带宽限制（简单会话）

```
  Client                                           Router

                           --------------------->  Get Bandwidth Limits Message
Bandwidth Limits Message  <---------------------

```
### 目标查找（简单会话）

```
  Client                                           Router

                           --------------------->  Dest Lookup Message
      Dest Reply Message  <---------------------

```
### 发送消息

现有会话，使用 i2cp.messageReliability=none

```
  Client                                           Router

                           --------------------->  Send Message Message

```
现有会话，设置 i2cp.messageReliability=none 且 nonce 非零

```
  Client                                           Router

                           --------------------->  Send Message Message
  Message Status Message  <---------------------
  (succeeded)

```
现有会话，设置 i2cp.messageReliability=BestEffort

```
  Client                                           Router

                           --------------------->  Send Message Message
  Message Status Message  <---------------------
  (accepted)
  Message Status Message  <---------------------
  (succeeded)

```
### 传入消息

现有会话，设置 i2cp.fastReceive=true（从 0.9.4 版本开始）

```
  Client                                           Router

 Message Payload Message  <---------------------

```
现有会话，使用 i2cp.fastReceive=false（已弃用）

```
  Client                                           Router

  Message Status Message  <---------------------
  (available)
                           --------------------->  Receive Message Begin Message
 Message Payload Message  <---------------------
                           --------------------->  Receive Message End Message

```
### 多会话说明 {#multisession}

从router版本0.9.21开始，支持在单个I2CP连接上建立多个会话。首先创建的会话是"主会话"。其他会话是"子会话"。子会话用于支持多个目的地共享一组通用的tunnel。初始应用是主会话使用ECDSA签名密钥，而子会话使用DSA签名密钥与旧的eepsite通信。

子会话与主会话共享相同的入站和出站隧道池。子会话必须使用与主会话相同的加密密钥。这同时适用于 LeaseSet 加密密钥和（未使用的）destination 加密密钥。子会话必须在 destination 中使用不同的签名密钥，因此 destination 哈希与主会话不同。由于子会话使用与主会话相同的加密密钥和隧道，所有人都能明显看出这些 destination 运行在同一个 router 上，因此通常的反关联匿名性保证不适用。

子会话通过发送CreateSession消息并接收SessionStatus消息回复来创建，如常规操作一样。子会话必须在主会话创建之后才能创建。成功时，SessionStatus响应将包含一个唯一的会话ID，与主会话的ID不同。虽然CreateSession消息应该按顺序处理，但没有确切的方法将CreateSession消息与响应关联，因此客户端不应同时发出多个CreateSession消息。子会话的SessionConfig选项如果与主会话不同，可能不会被接受。特别是，由于子会话使用与主会话相同的tunnel池，tunnel选项可能会被忽略。

router 将为每个目标地址向客户端发送单独的 RequestVariableLeaseSet 消息，客户端必须为每个目标地址回复一个 CreateLeaseSet 消息。两个目标地址的租约不一定相同，即使它们是从同一个 tunnel 池中选择的。

子会话可以像往常一样通过 DestroySession 消息销毁。这不会销毁主会话或停止 I2CP 连接。然而，销毁主会话将销毁所有子会话并停止 I2CP 连接。Disconnect 消息会销毁所有会话。

请注意，大部分但不是全部的I2CP消息都包含会话ID。对于不包含会话ID的消息，客户端可能需要额外的逻辑来正确处理router响应。DestLookup和DestReply不包含会话ID；请改用更新的HostLookup和HostReply。GetBandwidthLimts和BandwidthLimits不包含会话ID，但是响应不是特定于会话的。

### 版本说明 {#notes}

客户端发送的初始协议版本字节（0x2a）预计不会改变。在 0.8.7 版本发布之前，客户端无法获得 router 的版本信息，这导致新客户端无法与旧 router 配合工作。从 0.8.7 版本开始，双方的协议版本字符串会在 Get/Set Date Messages 中交换。今后，客户端可以使用这些信息与旧 router 正确通信。客户端和 router 不应发送对方不支持的消息，因为它们通常会在收到不支持的消息时断开会话连接。

交换的版本信息是"核心"API版本或I2CP协议版本，不一定是router版本。

I2CP 协议版本的基本摘要如下。详细信息请参见下文。

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Version</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Required I2CP Features</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.67</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">PQ Hybrid ML-KEM (enc types 5-7) supported in LS</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Host lookup/reply extensions (see proposal 167)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.62</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">MessageStatus message Loopback error code</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.46</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">X25519 (enc type 4) supported in LS</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.43</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">BlindingInfo message supported; Additional HostReply message failure codes</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">EncryptedLeaseSet options; MessageStatus message Meta LS error code</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.39</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">CreateLeaseSet2 message and options supported; Dest/LS key certs w/ RedDSA Ed25519 sig type supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Preliminary CreateLeaseSet2 message supported (abandoned)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.21</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Multiple sessions on a single I2CP connection supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.20</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Additional SetDate messages may be sent to the client at any time</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.16</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Authentication, if enabled, is required via GetDate before all other messages</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.15</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest/LS key certs w/ EdDSA Ed25519 sig type supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.14</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Per-message override of messageReliability=none with nonzero nonce</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest/LS key certs w/ ECDSA P-256, P-384, and P-521 sig types supported; RSA sig types also supported but currently unused</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Host Lookup and Host Reply messages supported; Authentication mapping in Get Date message supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Request Variable Lease Set message supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Additional Message Status codes defined</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Send Message nonce=0 allowed; Fast receive mode is the default</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Send Message Expires flag tag bits supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Supports up to 16 leases in a lease set (6 previously)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Get Date and Set Date version strings included. If not present, the client or router is version 0.8.6 or older.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Send Message Expires flag bits supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest Lookup and Get Bandwidth messages supported in standard session; Concurrent Dest Lookup messages supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.messageReliability=none supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Get Bandwidth Limits and Bandwidth Limits messages supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Send Message Expires message supported; Reconfigure Session message supported; Ports and protocol numbers in gzip header</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest Lookup and Dest Reply messages supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.6.5 or lower</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">All messages and features not listed above</td>
</tr>
</table>
## 常用结构 {#structures}

### I2CP 消息头 {#struct-I2CPMessageHeader}

#### 描述

所有 I2CP 消息的通用头部，包含消息长度和消息类型。

#### 目录

1.  4字节[Integer](/docs/specs/common-structures/#integer)，指定消息体的长度
2.  1字节[Integer](/docs/specs/common-structures/#integer)，指定消息类型
3.  I2CP消息体，0字节或更多字节

#### 注意事项

实际消息长度限制约为 64 KB。

### 消息 ID {#struct-MessageId}

#### 描述

唯一标识在特定时间点等待在特定 router 上的消息。这总是由 router 生成，与客户端生成的随机数（nonce）不同。

#### 目录

1.  4字节 [Integer](/docs/specs/common-structures/#integer)

#### 注释

消息ID仅在会话内唯一；它们并非全局唯一。

### 负载 {#struct-Payload}

#### 描述

这个结构是从一个目标地址传递到另一个目标地址的消息内容。

#### 目录

1.  4 字节 [Integer](/docs/specs/common-structures/#integer) 长度
2.  对应字节数

#### 注释

载荷采用 gzip 格式，如 I2CP 概述页面 [I2CP-FORMAT](/docs/specs/i2cp/#format) 中所指定的。

实际消息长度限制约为 64 KB。

### 会话配置 {#struct-SessionConfig}

#### 描述

定义特定客户端会话的配置选项。

#### 目录

1.  [Destination](/docs/specs/common-structures/#destination)
2.  选项的[Mapping](/docs/specs/common-structures/#mapping)
3.  创建[Date](/docs/specs/common-structures/#date)
4.  前3个字段的[Signature](/docs/specs/common-structures/#signature)，
    由[SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey)签名

#### 注释

- 选项在 I2CP 概述页面中有详细说明
  [I2CP-OPTIONS](/docs/specs/i2cp/#options)。
- [映射](/docs/specs/common-structures/#mapping) 必须按键排序，这样
  签名才能在 router 中正确验证。
- 创建日期必须在 router 处理时的当前时间 +/- 30 秒范围内，
  否则配置将被拒绝。

#### 离线签名

- 如果 [Destination](/docs/specs/common-structures/#destination) 是离线签名的，
  [Mapping](/docs/specs/common-structures/#mapping) 必须包含三个选项
  i2cp.leaseSetOfflineExpiration、i2cp.leaseSetTransientPublicKey 和
  i2cp.leaseSetOfflineSignature。然后
  [Signature](/docs/specs/common-structures/#signature) 由临时
  [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey) 生成，
  并使用 i2cp.leaseSetTransientPublicKey 中指定的
  [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) 进行验证。
  详情请参见 [I2CP-OPTIONS](/docs/specs/i2cp/#options)。

### 会话 ID {#struct-SessionId}

#### 描述

在特定时间点唯一标识特定 router 上的会话。

#### 目录

1.  2 字节 [Integer](/docs/specs/common-structures/#integer)

#### 注意事项

会话ID 0xffff 用于表示"无会话"，例如用于主机名查找。

## 消息

另请参阅 [I2CP Javadocs](http://javadoc.i2p.net/net/i2p/data/i2cp/package-summary.html)。

### 消息类型 {#types}

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Message</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Direction</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Since</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#BandwidthLimitsMessage">BandwidthLimitsMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">23</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.2</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#BlindingInfoMessage">BlindingInfoMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">42</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.43</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#CreateLeaseSetMessage">CreateLeaseSetMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#CreateLeaseSet2Message">CreateLeaseSet2Message</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.39</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#CreateSessionMessage">CreateSessionMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#DestLookupMessage">DestLookupMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">34</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#DestReplyMessage">DestReplyMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">35</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#DestroySessionMessage">DestroySessionMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#DisconnectMessage">DisconnectMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">bidir.</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">30</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#GetBandwidthLimitsMessage">GetBandwidthLimitsMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.2</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#GetDateMessage">GetDateMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#HostLookupMessage">HostLookupMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.11</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#HostReplyMessage">HostReplyMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">39</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.11</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#MessagePayloadMessage">MessagePayloadMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">31</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#MessageStatusMessage">MessageStatusMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">22</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#ReceiveMessageBeginMessage">ReceiveMessageBeginMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#ReceiveMessageEndMessage">ReceiveMessageEndMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#ReconfigureSessionMessage">ReconfigureSessionMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#ReportAbuseMessage">ReportAbuseMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">bidir.</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">29</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#RequestLeaseSetMessage">RequestLeaseSetMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">21</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#RequestVariableLeaseSetMessage">RequestVariableLeaseSetMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">37</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#SendMessageMessage">SendMessageMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#SendMessageExpiresMessage">SendMessageExpiresMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">36</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#SessionStatusMessage">SessionStatusMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">20</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#SetDateMessage">SetDateMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">33</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
</table>
### BandwidthLimitsMessage {#BandwidthLimitsMessage}

#### 描述

告知客户端带宽限制是什么。

由 Router 发送给 Client，作为对 [GetBandwidthLimitsMessage](#GetBandwidthLimitsMessage) 的响应。

#### 目录

1.  4 字节 [Integer](/docs/specs/common-structures/#integer) 客户端入站限制
    (KBps)
2.  4 字节 [Integer](/docs/specs/common-structures/#integer) 客户端出站限制
    (KBps)
3.  4 字节 [Integer](/docs/specs/common-structures/#integer) Router 入站限制
    (KBps)
4.  4 字节 [Integer](/docs/specs/common-structures/#integer) Router 入站突发限制
    (KBps)
5.  4 字节 [Integer](/docs/specs/common-structures/#integer) Router 出站限制
    (KBps)
6.  4 字节 [Integer](/docs/specs/common-structures/#integer) Router 出站突发
    限制 (KBps)
7.  4 字节 [Integer](/docs/specs/common-structures/#integer) Router 突发时间
    (秒)
8.  九个 4 字节 [Integer](/docs/specs/common-structures/#integer) (未定义)

#### 注意事项

客户端限制可能是唯一设置的值，可能是实际的 router 限制，或者是 router 限制的百分比，或者是特定于特定客户端的，具体取决于实现。所有标记为 router 限制的值可能都为 0，具体取决于实现。截至 0.7.2 版本。

### BlindingInfoMessage {#BlindingInfoMessage}

#### 描述

通知router某个目的地是盲化的，可选择提供查找密码和用于解密的私钥。详情请参见提案123和149。

router需要知道目标是否是盲化的。如果目标是盲化的并且使用密钥或按客户端认证，它也需要获得这些信息。

对新格式 b32 地址（"b33"）的主机查找告诉 router 该地址是盲化的，但在主机查找消息中没有机制将密钥或私钥传递给 router。虽然我们可以扩展主机查找消息来添加该信息，但定义一个新消息会更简洁。

此消息为客户端提供了一种程序化的方式来告知router。否则，用户将必须手动配置每个目标。

#### 用法

在客户端向盲化目标发送消息之前，它必须在主机查找消息中查找"b33"，或者发送盲化信息消息。如果盲化目标需要密钥或每客户端认证，客户端必须发送盲化信息消息。

router不会对此消息发送回复。由客户端发送到router。

#### 目录

1.  [Session ID](#struct-sessionid)
2.  1 字节 [Integer](/docs/specs/common-structures/#integer) 标志

> - 位序：76543210 > - 位 0：0 表示所有人，1 表示按客户端 > - 位 3-1：认证方案，如果位 0 设置为 1 表示按客户端，否则为 000 >   - 000：DH 客户端认证（或无按客户端认证） >   - 001：PSK 客户端认证 > - 位 4：1 表示需要密钥，0 表示不需要密钥 > - 位 7-5：未使用，设为 0 以确保未来兼容性

3.  1 字节 [Integer](/docs/specs/common-structures/#integer) 端点类型

> - 类型 0 是一个 [Hash](/docs/specs/common-structures/#hash) > - 类型 1 是一个主机名 [String](/docs/specs/common-structures/#string) > - 类型 2 是一个 [Destination](/docs/specs/common-structures/#destination) > - 类型 3 是一个签名类型和 >   [SigningPublicKey](/docs/specs/common-structures/#signingpublickey)

4.  2 字节 [Integer](/docs/specs/common-structures/#integer) 盲签名类型
5.  4 字节 [Integer](/docs/specs/common-structures/#integer) 自纪元以来的过期秒数
6.  端点：按指定格式的数据，以下之一

> - 类型 0：32 字节 [Hash](/docs/specs/common-structures/#hash) > > - 类型 1：主机名 [String](/docs/specs/common-structures/#string) > > - 类型 2：二进制 [Destination](/docs/specs/common-structures/#destination) > >  > >  - 类型 3：2 字节 [Integer](/docs/specs/common-structures/#integer) 签名类型，后跟 > >  -   [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) （长度由 >       签名类型隐含确定）

7.  [PrivateKey](/docs/specs/common-structures/#privatekey) 解密密钥 仅当标志位 0 设置为 1 时存在。一个 32 字节的 ECIES_X25519 私钥，小端序
8.  [String](/docs/specs/common-structures/#string) 查找密码 仅当标志位 4 设置为 1 时存在。

#### 注意事项

- 截至 0.9.43 版本发布。
- Hash 端点类型可能不太有用，除非 router 可以在地址簿中进行反向查找以获取 Destination。
- 主机名端点类型可能不太有用，除非 router 可以在地址簿中进行查找以获取 Destination。

### CreateLeaseSetMessage {#CreateLeaseSetMessage}

已弃用。无法用于 LeaseSet2、离线密钥、非 ElGamal 加密类型、多种加密类型或加密的 LeaseSet。请在所有 0.9.39 或更高版本的 router 上使用 CreateLeaseSet2Message。

#### 说明

此消息是对 [RequestLeaseSetMessage](#RequestLeaseSetMessage) 或 [RequestVariableLeaseSetMessage](#RequestVariableLeaseSetMessage) 的响应，包含所有应发布到 I2NP 网络数据库的 [Lease](/docs/specs/common-structures/#lease) 结构。

从客户端发送到 Router。

#### 目录

1.  [Session ID](#struct-sessionid)
2.  DSA [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey) 或 20
    字节忽略
3.  [PrivateKey](/docs/specs/common-structures/#privatekey)
4.  [LeaseSet](/docs/specs/common-structures/#leaseset)

#### 注释

SigningPrivateKey 与 LeaseSet 中的 [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) 匹配，仅当签名密钥类型为 DSA 时。这用于 LeaseSet 撤销功能，该功能尚未实现且不太可能被实现。如果签名密钥类型不是 DSA，此字段包含 20 字节的随机数据。此字段的长度始终为 20 字节，不会等于非 DSA 签名私钥的长度。

PrivateKey 与 LeaseSet 中的 [PublicKey](/docs/specs/common-structures/#publickey) 相匹配。PrivateKey 是解密 garlic 路由消息所必需的。

撤销功能尚未实现。在任何客户端库中都尚未实现连接到多个 router 的功能。

### CreateLeaseSet2Message {#CreateLeaseSet2Message}

#### 描述

此消息是对 [RequestLeaseSetMessage](#RequestLeaseSetMessage) 或 [RequestVariableLeaseSetMessage](#RequestVariableLeaseSetMessage) 的响应，包含应发布到 I2NP 网络数据库的所有 [Lease](/docs/specs/common-structures/#lease) 结构。

由客户端发送到 router。从 0.9.39 版本开始支持。从 0.9.41 版本开始支持 EncryptedLeaseSet 的每客户端身份验证。I2CP 尚不支持 MetaLeaseSet。更多信息请参见提案 123。

#### 目录

1.  [Session ID](#struct-sessionid)
2.  一个字节的后续 lease set 类型。

> - 类型 1 是 [LeaseSet](/docs/specs/common-structures/#leaseset)（已弃用）> - 类型 3 是 [LeaseSet2](/docs/specs/common-structures/#leaseset2) > - 类型 5 是 [EncryptedLeaseSet](/docs/specs/common-structures/#leaseset2) > - 类型 7 是 [MetaLeaseSet](/docs/specs/common-structures/#leaseset2)

3.  [LeaseSet](/docs/specs/common-structures/#leaseset) 或
    [LeaseSet2](/docs/specs/common-structures/#leaseset2) 或
    [EncryptedLeaseSet](/docs/specs/common-structures/#leaseset2) 或
    [MetaLeaseSet](/docs/specs/common-structures/#leaseset2)
4.  一个字节，表示后续私钥的数量。
5.  [PrivateKey](/docs/specs/common-structures/#privatekey) 列表。与 lease set 中的每个公钥对应，顺序相同。（Meta LS2 中不存在）

> - 加密类型 (2 字节 [Integer](/docs/specs/common-structures/#integer)) > - 加密密钥长度 (2 字节 [Integer](/docs/specs/common-structures/#integer)) > - 加密 [PrivateKey](/docs/specs/common-structures/#privatekey) (指定的字节数)

#### 注释

PrivateKeys 与 LeaseSet 中的每个 [PublicKey](/docs/specs/common-structures/#publickey) 相匹配。PrivateKeys 是解密 garlic 路由消息所必需的。

有关加密 LeaseSet 的更多信息，请参阅提案 123。

MetaLeaseSet的内容和格式是初步的，可能会发生变化。目前没有为管理多个router指定协议。请参阅提案123以获取更多信息。

用于撤销且未使用的签名私钥在 LS2 中不存在。

初步版本使用消息类型40在0.9.38中实现，但格式已更改。类型40已废弃且不再支持。类型41在0.9.39之前无效。

### CreateSessionMessage {#CreateSessionMessage}

#### 描述

此消息由客户端发送以启动会话，会话定义为单个 Destination 与网络的连接，所有发送给该 Destination 的消息都将通过此连接传递，该 Destination 发送给任何其他 Destination 的所有消息也将通过此连接发送。

从客户端发送到 router。router 会响应一个 [SessionStatusMessage](#SessionStatusMessage)。

#### 目录

1.  [会话配置](#struct-sessionconfig)

#### 注意事项

- 这是客户端发送的第二条消息。之前客户端发送了一个 [GetDateMessage](#GetDateMessage) 并收到了一个 [SetDateMessage](#SetDateMessage) 响应。
- 如果会话配置中的日期与 router 当前时间相差太远（超过 +/- 30 秒），会话将被拒绝。
- 如果 router 上已经存在针对此目标地址的会话，会话将被拒绝。
- 会话配置中的 [Mapping](/docs/specs/common-structures/#mapping) 必须按键排序，以便在 router 中正确验证签名。

### DestLookupMessage {#DestLookupMessage}

#### 描述

从客户端发送到 router。router 会响应一个 [DestReplyMessage](#DestReplyMessage)。

#### 目录

1.  SHA-256 [哈希](/docs/specs/common-structures/#hash)

#### 注意事项

截至 0.7 版本。

从 0.8.3 版本开始，支持多个未完成的查找，并且在 I2PSimpleSession 和标准会话中都支持查找。

从 0.9.11 版本开始，推荐使用 [HostLookupMessage](#HostLookupMessage)。

### DestReplyMessage {#DestReplyMessage}

#### 描述

从 Router 发送到客户端，作为对 [DestLookupMessage](#DestLookupMessage) 的响应。

#### 目录

1.  成功时返回 [Destination](/docs/specs/common-structures/#destination)，或
    失败时返回 [Hash](/docs/specs/common-structures/#hash)

#### 注意事项

截至 0.7 版本。

从 0.8.3 版本开始，如果查找失败，会返回请求的 Hash，这样客户端可以同时进行多个查找并将回复与查找请求进行关联。要将 Destination 响应与请求进行关联，需要获取 Destination 的 Hash。在 0.8.3 版本之前，失败时响应为空。

### DestroySessionMessage {#DestroySessionMessage}

#### 描述

此消息由客户端发送以销毁会话。

从客户端发送到 router。router 应该响应一个 [SessionStatusMessage](#SessionStatusMessage)（已销毁）。但是，请参阅下面的重要说明。

#### 目录

1.  [会话 ID](#struct-sessionid)

#### 注意事项

此时 router 应该释放与该会话相关的所有资源。

在API 0.9.66之前，Java I2P router和客户端库与此规范有很大偏差。router从不发送SessionStatus(Destroyed)响应。如果没有会话剩余，它会发送[DisconnectMessage](#DisconnectMessage)。如果还有子会话或主会话仍然存在，它不会回复。

Java 客户端库通过销毁所有会话并重新连接来响应 SessionStatus 消息。

在具有多个会话的连接上销毁单个子会话可能在各种 router 和客户端实现中未经充分测试或无法正常工作。请谨慎使用。

实现应该将主会话的销毁视为所有子会话的销毁，但允许销毁单个子会话并保持连接开启，但 Java I2P 目前不这样做。如果 Java I2P 的行为在后续版本中发生变化，将在此处记录。

### DisconnectMessage {#DisconnectMessage}

#### 描述

告知对方存在问题，当前连接即将被销毁。这将结束该连接上的所有会话。socket 将很快关闭。可以从 router 发送到客户端，也可以从客户端发送到 router。

#### 目录

1.  原因 [String](/docs/specs/common-structures/#string)

#### 注意事项

仅在router到客户端方向实现，至少在Java I2P中是这样。

### GetBandwidthLimitsMessage {#GetBandwidthLimitsMessage}

#### 描述

请求router说明其当前的带宽限制。

从客户端发送到 Router。Router 会响应一个 [BandwidthLimitsMessage](#BandwidthLimitsMessage)。

#### 目录

*无*

#### 注释

截至 0.7.2 版本。

从 0.8.3 版本开始，I2PSimpleSession 和标准会话都支持此功能。

### GetDateMessage {#GetDateMessage}

#### 描述

从客户端发送到 router。router 会响应一个 [SetDateMessage](#SetDateMessage)。

#### 目录

1.  I2CP API 版本 [String](/docs/specs/common-structures/#string)
2.  身份验证 [Mapping](/docs/specs/common-structures/#mapping)（可选，自 0.9.11 版本开始）

#### 注释

- 通常是客户端在发送协议版本字节后发送的第一条消息。
- 从0.8.7版本开始包含版本字符串。只有当客户端和router不在同一个JVM中时这才有用。如果不存在版本字符串，则客户端版本为0.8.6或更早。
- 从0.9.11版本开始，可能包含认证[Mapping](/docs/specs/common-structures/#mapping)，包含键i2cp.username和i2cp.password。由于此消息未签名，Mapping无需排序。在0.9.10及之前的版本中，认证包含在[Session Config](#struct-sessionconfig) Mapping中，并且对[GetDateMessage](#GetDateMessage)、[GetBandwidthLimitsMessage](#GetBandwidthLimitsMessage)或[DestLookupMessage](#DestLookupMessage)不强制进行认证。当启用时，从0.9.16版本开始，在任何其他消息之前都需要通过[GetDateMessage](#GetDateMessage)进行认证。这只在router上下文之外有用。这是一个不兼容的更改，但只会影响router上下文之外带有认证的会话，这种情况应该很少见。

### HostLookupMessage {#HostLookupMessage}

#### 描述

从客户端发送到 Router。router 会响应一个 [HostReplyMessage](#HostReplyMessage)。

这替代了 [DestLookupMessage](#DestLookupMessage) 并添加了请求 ID、超时时间和主机名查找支持。由于它也支持 Hash 查找，如果 router 支持的话，可用于所有查找操作。对于主机名查找，router 将查询其上下文的命名服务。这仅在客户端位于 router 上下文之外时才有用。在 router 上下文内部，客户端应该自己查询命名服务，这样效率更高。

#### 目录

1.  [Session ID](#struct-sessionid)
2.  4 字节 [Integer](/docs/specs/common-structures/#integer) 请求 ID
3.  4 字节 [Integer](/docs/specs/common-structures/#integer) 超时时间 (ms)
4.  1 字节 [Integer](/docs/specs/common-structures/#integer) 请求类型
5.  SHA-256 [Hash](/docs/specs/common-structures/#hash) 或主机名
    [String](/docs/specs/common-structures/#string) 或
    [Destination](/docs/specs/common-structures/#destination)

请求类型：

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Lookup key (item 5)</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">As of</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Hash</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">host name String</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Hash</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">host name String</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Destination</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
</tr>
</table>
类型 2-4 请求将 LeaseSet 中的选项映射在 HostReply 消息中返回。参见提案 167。

#### 注意事项

- 自版本 0.9.11 起。对于较旧的 router，请使用 [DestLookupMessage](#DestLookupMessage)。
- 会话 ID 和请求 ID 将在 [HostReplyMessage](#HostReplyMessage) 中返回。如果没有会话，请使用 0xFFFF 作为会话 ID。
- 超时对于哈希查找很有用。建议最小值为 10,000（10 秒）。将来对于远程命名服务查找也可能有用。对于本地主机名查找，该值可能不会被采用，因为本地查找应该很快。
- 支持 Base 32 主机名查找，但建议先将其转换为哈希。

### HostReplyMessage {#HostReplyMessage}

#### 描述

由 Router 发送给客户端，作为对 [HostLookupMessage](#HostLookupMessage) 的响应。

#### 目录

1.  [Session ID](#struct-sessionid)
2.  4 字节 [Integer](/docs/specs/common-structures/#integer) 请求 ID
3.  1 字节 [Integer](/docs/specs/common-structures/#integer) 结果代码

> - 0: 成功 > - 1: 失败 > - 2: 需要查找密码（从 0.9.43 开始）> - 3: 需要私钥（从 0.9.43 开始）> - 4: 需要查找密码和私钥（从 0.9.43 开始）> - 5: leaseSet 解密失败（从 0.9.43 开始）> - 6: leaseSet 查找失败（从 0.9.66 开始）> - 7: 不支持的查找类型（从 0.9.66 开始）

4.  [Destination](/docs/specs/common-structures/#destination)，仅在结果代码为零时存在，但查找类型 2-4 也可能返回此项。见下文。
5.  [Mapping](/docs/specs/common-structures/#mapping)，仅在结果代码为零时存在，仅对查找类型 2-4 返回。从 0.9.66 版本开始。见下文。

#### 查找类型 2-4 的响应

提案167定义了额外的查找类型，如果存在的话，会返回leaseset中的所有选项。对于查找类型2-4，router必须获取leaseset，即使查找键已在地址簿中。

如果成功，HostReply 将包含来自 leaseset 的选项映射，并将其作为目标后的第 5 项包含在内。如果映射中没有选项，或者 leaseset 是版本 1，它仍然会作为空映射包含在内（两个字节：0 0）。来自 leaseset 的所有选项都将被包含，不仅仅是服务记录选项。例如，可能存在未来定义的参数选项。返回的映射可能排序也可能不排序，取决于实现。

当 leaseset 查找失败时，回复将包含新的错误代码 6（Leaseset 查找失败）并且不会包含映射。当返回错误代码 6 时，Destination 字段可能存在也可能不存在。如果地址簿中的主机名查找成功，或者之前的查找成功并且结果被缓存，或者 Destination 在查找消息中存在（查找类型 4），则该字段将存在。

如果不支持某种查找类型，回复将包含新的错误代码7（不支持的查找类型）。

#### 注意事项

- 自 0.9.11 版本起。参见 [HostLookupMessage](#HostLookupMessage)
  注释。
- session ID 和 request ID 来自
  [HostLookupMessage](#HostLookupMessage)。
- 结果代码为 0 表示成功，1-255 表示失败。1 表示
  通用失败。自 0.9.43 起，定义了额外的失败代码 2-5 来
  支持 "b33" 查找的扩展错误。更多信息请参见提案
  123 和 149。自 0.9.66 起，定义了额外的
  失败代码 6-7 来支持 type 2-4
  查找的扩展错误。更多信息请参见提案 167。

### MessagePayloadMessage {#MessagePayloadMessage}

#### 描述

将消息的有效载荷传递给客户端。

从 Router 发送到客户端。如果 i2cp.fastReceive=true（这不是默认设置），客户端会响应一个 [ReceiveMessageEndMessage](#ReceiveMessageEndMessage)。

#### 目录

1.  [会话ID](#struct-sessionid)
2.  [消息ID](#struct-messageid)
3.  [载荷](#struct-payload)

#### 注释

### MessageStatusMessage {#MessageStatusMessage}

#### 描述

通知客户端传入或传出消息的传递状态。从router发送到客户端。如果此消息表明有传入消息可用，客户端将使用 [ReceiveMessageBeginMessage](#ReceiveMessageBeginMessage) 响应。对于传出消息，这是对 [SendMessageMessage](#SendMessageMessage) 或 [SendMessageExpiresMessage](#SendMessageExpiresMessage) 的响应。

#### 目录

1.  [Session ID](#struct-sessionid)
2.  由 router 生成的 [Message ID](#struct-messageid)
3.  1 字节 [Integer](/docs/specs/common-structures/#integer) 状态
4.  4 字节 [Integer](/docs/specs/common-structures/#integer) 大小
5.  4 字节 [Integer](/docs/specs/common-structures/#integer) 之前由客户端生成的 nonce

#### 注释

在版本 0.9.4 之前，已知的状态值为：0 表示消息可用，1 表示已接受，2 表示尽力而为成功，3 表示尽力而为失败，4 表示保证传输成功，5 表示保证传输失败。大小整数指定可用消息的大小，仅在状态 = 0 时相关。尽管保证传输尚未实现（尽力而为是唯一的服务），当前的 router 实现使用保证传输状态码，而不是尽力而为状态码。

从 router 版本 0.9.5 开始，定义了额外的状态码，但它们不一定已经实现。详情请参见 [MessageStatusMessage Javadocs](http://javadoc.i2p.net/net/i2p/data/i2cp/MessageStatusMessage.html)。对于出站消息，状态码 1、2、4 和 6 表示成功；其他所有状态码都表示失败。返回的失败状态码可能有所不同，且具体实现相关。

所有状态码：

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Status Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">As Of Release</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Name</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Description</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Available</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">DEPRECATED. For incoming messages only. All other status codes below are for outgoing messages. The included size is the size in bytes of the available message. This is unused in "fast receive" mode, which is the default as of release 0.9.4.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Accepted</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Outgoing message accepted by the local router for delivery. The included nonce matches the nonce in the <a href="#SendMessageMessage">SendMessageMessage</a>, and the included Message ID will be used for subsequent success or failure notification.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Best Effort Success</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Probable success (unused)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Best Effort Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Probable failure</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Guaranteed Success</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Probable success</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Guaranteed Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Generic failure, specific cause unknown. May not really be a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local Success</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local delivery successful. The destination was another client on the same router.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local delivery failure. The destination was another client on the same router.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Router Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The local router is not ready, has shut down, or has major problems. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">9</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Network Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The local computer apparently has no network connectivity at all. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Session</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The I2CP session is invalid or closed. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Message</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The message payload is invalid or zero-length or too big. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Options</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Something is invalid in the message options, or the expiration is in the past or too far in the future. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">13</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Overflow Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Some queue or buffer in the router is full and the message was dropped. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">14</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Message Expired</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The message expired before it could be sent. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">15</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Local Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The client has not yet signed a <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a>, or the local keys are invalid, or it has expired, or it does not have any tunnels in it. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">No Local Tunnels</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local problems. No outbound tunnel to send through, or no inbound tunnel if a reply is required. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">17</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Unsupported Encryption</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The certs or options in the <a href="/docs/specs/common-structures/#destination">Destination</a> or its <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a> indicate that it uses an encryption format that we don't support, so we can't talk to it. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">18</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Destination</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Something is wrong with the far-end <a href="/docs/specs/common-structures/#destination">Destination</a>. Bad format, unsupported options, certificates, etc. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">19</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">We got the far-end <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a> but something strange is wrong with it. Unsupported options or certificates, no tunnels, etc. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">20</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Expired Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">We got the far-end <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a> but it's expired and we can't get a new one. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">21</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">No Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Could not find the far-end <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a>. This is a common failure, equivalent to a DNS lookup failure. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">22</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Meta Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The far-end destination's lease set was a meta lease set, and cannot be sent to. The client should request the meta lease set's contents with a HostLookupMessage, and select one of the hashes contained within to look up and send to. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">23</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.62</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Loopback Denied</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The message was attempted to be sent from and to the same destination or session. This is a guaranteed failure.</td>
</tr>
</table>
当 status = 1（已接受）时，nonce 与 [SendMessageMessage](#SendMessageMessage) 中的 nonce 匹配，包含的消息 ID 将用于后续的成功或失败通知。否则，nonce 可能会被忽略。

### ReceiveMessageBeginMessage {#ReceiveMessageBeginMessage}

已弃用。i2pd 不支持。

#### 描述

请求 router 投递之前已通知的消息。由客户端发送给 router。router 会回应一个 [MessagePayloadMessage](#MessagePayloadMessage)。

#### 目录

1.  [会话 ID](#struct-sessionid)
2.  [消息 ID](#struct-messageid)

#### 注意事项

[ReceiveMessageBeginMessage](#ReceiveMessageBeginMessage) 作为对 [MessageStatusMessage](#MessageStatusMessage) 的响应发送，表明有新消息可供获取。如果 [ReceiveMessageBeginMessage](#ReceiveMessageBeginMessage) 中指定的消息 ID 无效或不正确，router 可能根本不回复，或者可能发回 [DisconnectMessage](#DisconnectMessage)。

这在"快速接收"模式下不使用，该模式自0.9.4版本起成为默认模式。

### ReceiveMessageEndMessage {#ReceiveMessageEndMessage}

已弃用。i2pd 不支持。

#### 描述

告知router消息已成功投递完成，router可以丢弃该消息。

从客户端发送到 Router。

#### 目录

1.  [会话 ID](#struct-sessionid)
2.  [消息 ID](#struct-messageid)

#### 注释

[ReceiveMessageEndMessage](#ReceiveMessageEndMessage) 在 [MessagePayloadMessage](#MessagePayloadMessage) 完全传递消息负载后发送。

在"快速接收"模式下这是未使用的，该模式从 0.9.4 版本开始成为默认模式。

### ReconfigureSessionMessage {#ReconfigureSessionMessage}

#### 描述

从客户端发送到 Router 以更新会话配置。router 会响应一个 [SessionStatusMessage](#SessionStatusMessage)。

#### 目录

1.  [会话 ID](#struct-sessionid)
2.  [会话配置](#struct-sessionconfig)

#### 注释

- 自版本 0.7.1 起。
- 如果 Session Config 中的 Date 与 router 当前时间相差太远（超过 +/- 30 秒），session 将被拒绝。
- Session Config 中的 [Mapping](/docs/specs/common-structures/#mapping) 必须按键排序，以便 router 中的签名能够正确验证。
- 某些配置选项可能只能在 [CreateSessionMessage](#CreateSessionMessage) 中设置，此处的更改将不会被 router 识别。对 tunnel 选项 inbound.\* 和 outbound.\* 的更改始终会被识别。
- 一般来说，router 应该将更新的配置与当前配置合并，因此更新的配置只需要包含新的或更改的选项。但是，由于合并的原因，选项无法以这种方式删除；它们必须显式设置为所需的默认值。

### ReportAbuseMessage {#ReportAbuseMessage}

已弃用、未使用、不支持

#### 描述

告知对方（客户端或router）他们正在遭受攻击，可能会引用特定的MessageId。如果router正在遭受攻击，客户端可以决定迁移到另一个router；如果客户端正在遭受攻击，router可以重建其路由或将发送攻击消息的某些对等节点加入黑名单。

从router发送到客户端或从客户端发送到router。

#### 目录

1.  [Session ID](#struct-sessionid)
2.  1 字节 [Integer](/docs/specs/common-structures/#integer) 滥用严重程度（0 表示轻微滥用，255 表示极度滥用）
3.  原因 [String](/docs/specs/common-structures/#string)
4.  [Message ID](#struct-messageid)

#### 注释

未使用。未完全实现。router和客户端都可以生成[ReportAbuseMessage](#ReportAbuseMessage)，但接收到消息时都没有处理程序。

### RequestLeaseSetMessage {#RequestLeaseSetMessage}

已弃用。i2pd不支持。Java I2P从0.9.7版本或更高版本（2013-07）开始不再向客户端发送此消息。请使用RequestVariableLeaseSetMessage。

#### 描述

请求客户端授权包含特定的一组入站 tunnel。从 Router 发送到客户端。客户端使用 [CreateLeaseSetMessage](#CreateLeaseSetMessage) 响应。

在会话中发送的第一条此类消息是向客户端发出的信号，表示tunnel已建立并准备好传输流量。router必须等到至少建立了一条入站tunnel和一条出站tunnel后才能发送第一条此类消息。如果在一段时间内（建议：5分钟或更长时间）没有收到第一条此类消息，客户端应该超时并销毁该会话。

#### 目录

1.  [Session ID](#struct-sessionid)
2.  1 字节 [Integer](/docs/specs/common-structures/#integer) tunnel 数量
3.  对应数量的配对：
    1.  [Hash](/docs/specs/common-structures/#hash)
    2.  [TunnelId](/docs/specs/common-structures/#tunnelid)
4.  结束 [Date](/docs/specs/common-structures/#date)

#### 注意事项

这会请求一个 [LeaseSet](/docs/specs/common-structures/#leaseset)，其中所有 [Lease](/docs/specs/common-structures/#lease) 条目都设置为在同一时间过期。对于客户端版本 0.9.7 或更高版本，使用 [RequestVariableLeaseSetMessage](#RequestVariableLeaseSetMessage)。

### RequestVariableLeaseSetMessage {#RequestVariableLeaseSetMessage}

#### 描述

请求客户端授权包含特定的入站 tunnel 集合。

从 router 发送到客户端。客户端用 [CreateLeaseSetMessage](#CreateLeaseSetMessage) 或 [CreateLeaseSet2Message](#CreateLeaseSet2Message) 响应。

在会话中发送的第一条此类消息是向客户端发出的信号，表示tunnel已构建并准备好传输流量。router在至少构建了一个入站tunnel和一个出站tunnel之前，不得发送第一条此类消息。如果在一定时间内（建议：5分钟或更长时间）未收到第一条此类消息，客户端应该超时并销毁会话。

#### 目录

1.  [Session ID](#struct-sessionid)
2.  1 字节 [Integer](/docs/specs/common-structures/#integer) 隧道数量
3.  对应数量的 [Lease](/docs/specs/common-structures/#lease) 条目

#### 注释

这请求一个具有每个 [Lease](/docs/specs/common-structures/#lease) 单独过期时间的 [LeaseSet](/docs/specs/common-structures/#leaseset)。

自 0.9.7 版本开始。对于该版本之前的客户端，请使用 [RequestLeaseSetMessage](#RequestLeaseSetMessage)。

### SendMessageMessage {#SendMessageMessage}

#### 描述

这是客户端向[目标地址](/docs/specs/common-structures/#destination)发送消息（负载）的方式。router 将使用默认的过期时间。

从客户端发送到路由器。router 会响应一个 [MessageStatusMessage](#MessageStatusMessage)。

#### 目录

1.  [Session ID](#struct-sessionid)
2.  [Destination](/docs/specs/common-structures/#destination)
3.  [Payload](#struct-payload)
4.  4 字节 [Integer](/docs/specs/common-structures/#integer) nonce

#### 注意事项

一旦 [SendMessageMessage](#SendMessageMessage) 完整到达，router 应该返回一个 [MessageStatusMessage](#MessageStatusMessage) 表明已接受投递。该消息将包含此处发送的相同 nonce。稍后，基于会话配置的投递保证，router 可能还会发送另一个 [MessageStatusMessage](#MessageStatusMessage) 来更新状态。

从 0.8.1 版本开始，如果设置了 i2cp.messageReliability=none，router 不会发送 [MessageStatusMessage](#MessageStatusMessage)。

在 0.9.4 版本之前，不允许 nonce 值为 0。从 0.9.4 版本开始，允许 nonce 值为 0，这告诉 router 它不应该发送 [MessageStatusMessage](#MessageStatusMessage)，即仅对此消息表现为 i2cp.messageReliability=none。

在 0.9.14 版本之前，设置了 i2cp.messageReliability=none 的会话无法在单个消息的基础上进行覆盖。从 0.9.14 版本开始，在设置了 i2cp.messageReliability=none 的会话中，客户端可以通过将 nonce 设置为非零值来请求接收 [MessageStatusMessage](#MessageStatusMessage) 以获得投递成功或失败的状态。router 不会发送"已接受"的 [MessageStatusMessage](#MessageStatusMessage)，但稍后会向客户端发送一个具有相同 nonce 和成功或失败值的 [MessageStatusMessage](#MessageStatusMessage)。

### SendMessageExpiresMessage {#SendMessageExpiresMessage}

#### 描述

从客户端发送到 router。与 [SendMessageMessage](#SendMessageMessage) 相同，但包含过期时间和选项。

#### 目录

1.  [Session ID](#struct-sessionid)
2.  [Destination](/docs/specs/common-structures/#destination)
3.  [Payload](#struct-payload)
4.  4 字节 [Integer](/docs/specs/common-structures/#integer) nonce
5.  2 字节标志位（选项）
6.  过期 [Date](/docs/specs/common-structures/#date) 从 8 字节截断为 6 字节

#### 注释

截至 0.7.1 版本发布。

在"尽力而为"模式下，一旦SendMessageExpiresMessage完整到达，router应该返回一个MessageStatusMessage，说明消息已被接受等待投递。该消息将包含此处发送的相同nonce。稍后，基于会话配置的投递保证，router可能会额外发送另一个MessageStatusMessage来更新状态。

从0.8.1版本开始，如果设置了i2cp.messageReliability=none，router将不会发送任何消息状态消息。

在0.9.4版本之前，不允许nonce值为0。从0.9.4版本开始，允许nonce值为0，这告诉router不应发送任何Message Status Message，即仅对此消息表现为i2cp.messageReliability=none。

在 0.9.14 版本之前，设置了 i2cp.messageReliability=none 的会话无法在单个消息基础上进行覆盖。从 0.9.14 版本开始，在设置了 i2cp.messageReliability=none 的会话中，客户端可以通过将 nonce 设置为非零值来请求接收包含投递成功或失败信息的 Message Status Message。router 不会发送"accepted" Message Status Message，但稍后会向客户端发送带有相同 nonce 和成功或失败值的 Message Status Message。

#### 标志字段

从版本 0.8.4 开始，Date 的高两个字节被重新定义为包含标志位。为了向后兼容，这些标志位必须默认为全零。直到公元 10889 年之前，Date 不会侵占标志位字段。应用程序可以使用这些标志位向 router 提供提示，指示是否应该随消息一起传递 LeaseSet 和/或 ElGamal/AES Session Tags。这些设置将显著影响协议开销的数量和消息传递的可靠性。从版本 0.9.2 开始，各个标志位定义如下。定义可能会发生变化。请使用 SendMessageOptions 类来构造标志位。

位序：15...0

位 15-11

:   未使用，必须为零

位 10-9

:   消息可靠性覆盖（未实现，将被移除）。

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Field value</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Description</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">00</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Use session setting i2cp.messageReliability (default)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">01</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Use "best effort" message reliability for this message, overriding the session setting. The router will send one or more MessageStatusMessages in response. Unused. Use a nonzero nonce value to override a session setting of "none".</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Use "guaranteed" message reliability for this message, overriding the session setting. The router will send one or more MessageStatusMessages in response. Unused. Use a nonzero nonce value to override a session setting of "none".</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Unused. Use a nonce value of 0 to force "none" and override a session setting of "best effort" or "guaranteed".</td>
</tr>
</table>
位 8

:   如果为1，不要在此消息的garlic中捆绑lease set。如果

    0, the router may bundle a lease set at its discretion.

位 7-4

:   低标签阈值。如果可用标签数少于此值，

    send more. This is advisory and does not force tags to be delivered.
    For ElGamal only. Ignored for ECIES-Ratchet.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Field value</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Tag threshold</th>
</tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0000</td><td style="border: 1px solid var(--color-border); padding: 8px;">Use session key manager settings</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0001</td><td style="border: 1px solid var(--color-border); padding: 8px;">2</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0010</td><td style="border: 1px solid var(--color-border); padding: 8px;">3</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0011</td><td style="border: 1px solid var(--color-border); padding: 8px;">6</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0100</td><td style="border: 1px solid var(--color-border); padding: 8px;">9</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0101</td><td style="border: 1px solid var(--color-border); padding: 8px;">14</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0110</td><td style="border: 1px solid var(--color-border); padding: 8px;">20</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0111</td><td style="border: 1px solid var(--color-border); padding: 8px;">27</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1000</td><td style="border: 1px solid var(--color-border); padding: 8px;">35</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1001</td><td style="border: 1px solid var(--color-border); padding: 8px;">45</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1010</td><td style="border: 1px solid var(--color-border); padding: 8px;">57</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1011</td><td style="border: 1px solid var(--color-border); padding: 8px;">72</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1100</td><td style="border: 1px solid var(--color-border); padding: 8px;">92</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1101</td><td style="border: 1px solid var(--color-border); padding: 8px;">117</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1110</td><td style="border: 1px solid var(--color-border); padding: 8px;">147</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1111</td><td style="border: 1px solid var(--color-border); padding: 8px;">192</td></tr>
</table>
第 3-0 位

:   如果需要，发送的标签数量。这是建议性的，并不

    force tags to be delivered. For ElGamal only. Ignored for
    ECIES-Ratchet.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Field value</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Tags to send</th>
</tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0000</td><td style="border: 1px solid var(--color-border); padding: 8px;">Use session key manager settings</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0001</td><td style="border: 1px solid var(--color-border); padding: 8px;">2</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0010</td><td style="border: 1px solid var(--color-border); padding: 8px;">4</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0011</td><td style="border: 1px solid var(--color-border); padding: 8px;">6</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0100</td><td style="border: 1px solid var(--color-border); padding: 8px;">8</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0101</td><td style="border: 1px solid var(--color-border); padding: 8px;">12</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0110</td><td style="border: 1px solid var(--color-border); padding: 8px;">16</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0111</td><td style="border: 1px solid var(--color-border); padding: 8px;">24</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1000</td><td style="border: 1px solid var(--color-border); padding: 8px;">32</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1001</td><td style="border: 1px solid var(--color-border); padding: 8px;">40</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1010</td><td style="border: 1px solid var(--color-border); padding: 8px;">51</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1011</td><td style="border: 1px solid var(--color-border); padding: 8px;">64</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1100</td><td style="border: 1px solid var(--color-border); padding: 8px;">80</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1101</td><td style="border: 1px solid var(--color-border); padding: 8px;">100</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1110</td><td style="border: 1px solid var(--color-border); padding: 8px;">125</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1111</td><td style="border: 1px solid var(--color-border); padding: 8px;">160</td></tr>
</table>
### SessionStatusMessage {#SessionStatusMessage}

#### 描述

指示客户端其会话的状态。

从 router 发送到客户端，作为对 [CreateSessionMessage](#CreateSessionMessage)、[ReconfigureSessionMessage](#ReconfigureSessionMessage) 或 [DestroySessionMessage](#DestroySessionMessage) 的响应。在所有情况下，包括响应 [CreateSessionMessage](#CreateSessionMessage) 时，router 都应立即响应（不要等待 tunnel 构建完成）。

#### 目录

1.  [Session ID](#struct-sessionid)
2.  1 字节 [Integer](/docs/specs/common-structures/#integer) 状态

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Status</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Since</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Name</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Definition</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Destroyed</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The session with the given ID is terminated. May be a response to a <a href="#DestroySessionMessage">DestroySessionMessage</a>.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Created</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">In response to a <a href="#CreateSessionMessage">CreateSessionMessage</a>, a new session with the given ID is now active.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Updated</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">In response to a <a href="#ReconfigureSessionMessage">ReconfigureSessionMessage</a>, an existing session with the given ID has been reconfigured.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Invalid</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">In response to a <a href="#CreateSessionMessage">CreateSessionMessage</a>, the configuration is invalid. The included session ID should be ignored. In response to a <a href="#ReconfigureSessionMessage">ReconfigureSessionMessage</a>, the new configuration is invalid for the session with the given ID.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Refused</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">In response to a <a href="#CreateSessionMessage">CreateSessionMessage</a>, the router was unable to create the session, perhaps due to limits being exceeded. The included session ID should be ignored.</td>
</tr>
</table>
#### 说明

状态值在上面已定义。如果状态为 Created，则 Session ID 是会话其余部分要使用的标识符。

### SetDateMessage {#SetDateMessage}

#### 描述

当前日期和时间。作为初始握手的一部分从 Router 发送到客户端。从 0.9.20 版本开始，也可以在握手后的任何时间发送，以通知客户端时钟偏移。

#### 目录

1.  [Date](/docs/specs/common-structures/#date)
2.  I2CP API 版本 [String](/docs/specs/common-structures/#string)

#### 注释

这通常是 router 发送的第一条消息。版本字符串从 0.8.7 版本开始包含。这只有在客户端和 router 不在同一个 JVM 中时才有用。如果不存在，则 router 是 0.8.6 或更早的版本。

不会向同一JVM中的客户端发送额外的SetDate消息。

## 参考资料

- [Date](/docs/specs/common-structures/#date)
- [Destination](/docs/specs/common-structures/#destination)
- [EncryptedLeaseSet](/docs/specs/common-structures/#leaseset2)
- [Hash](/docs/specs/common-structures/#hash)
- [I2CP 概述](/docs/specs/i2cp/)
- [I2CP Javadocs](http://javadoc.i2p.net/net/i2p/data/i2cp/package-summary.html)
- [Integer](/docs/specs/common-structures/#integer)
- [Lease](/docs/specs/common-structures/#lease)
- [LeaseSet](/docs/specs/common-structures/#leaseset)
- [LeaseSet2](/docs/specs/common-structures/#leaseset2)
- [Mapping](/docs/specs/common-structures/#mapping)
- [MetaLeaseSet](/docs/specs/common-structures/#leaseset2)
- [MessageStatusMessage Javadocs](http://javadoc.i2p.net/net/i2p/data/i2cp/MessageStatusMessage.html)
- [PrivateKey](/docs/specs/common-structures/#privatekey)
- [PublicKey](/docs/specs/common-structures/#publickey)
- [RouterIdentity](/docs/specs/common-structures/#routeridentity)
- [SAMv3](/docs/api/samv3/)
- [Signature](/docs/specs/common-structures/#signature)
- [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey)
- [SigningPublicKey](/docs/specs/common-structures/#signingpublickey)
- [String](/docs/specs/common-structures/#string)
- [TunnelId](/docs/specs/common-structures/#tunnelid)
