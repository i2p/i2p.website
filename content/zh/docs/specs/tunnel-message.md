---
title: "Tunnel 消息规范"
description: "I2P 中 tunnel 消息格式规范"
slug: "tunnel-message"
aliases:
  - "/zh/docs/legacy/tunnel-message"
  - "/zh/docs/legacy/tunnel-message/"
  - "/zh/tunnel_message_spec"
  - "/zh/tunnel_message_spec/"
category: "设计"
lastUpdated: "2021-01"
accurateFor: "0.9.49"
---

## 概述

本文档规定了tunnel消息的格式。有关tunnel的一般信息，请参阅[tunnel文档](/docs/specs/tunnel-implementation)。

## 消息预处理

*tunnel gateway* 是 tunnel 的入口或第一跳。对于出站 tunnel，gateway 是该 tunnel 的创建者。对于入站 tunnel，gateway 位于 tunnel 创建者的对端。

网关*预处理* [I2NP](/docs/specs/i2np) 消息，通过将其分片和合并为隧道消息。

虽然I2NP消息的大小是可变的，从0到接近64 KB，但tunnel消息是固定大小的，大约1 KB。固定的消息大小限制了通过观察消息大小可能进行的几种类型的攻击。

创建tunnel消息后，它们将按照[tunnel文档](/docs/specs/tunnel-implementation)中描述的方式进行加密。

### Tunnel 消息（加密）

这些是 tunnel 数据消息加密后的内容。

```
+----+----+----+----+----+----+----+----+
|    Tunnel ID      |       IV          |
+----+----+----+----+                   +
|                                       |
+                   +----+----+----+----+
|                   |                   |
+----+----+----+----+                   +
|                                       |
+           Encrypted Data              +
~                                       ~
|                                       |
+                   +-------------------+
|                   |
+----+----+----+----+
```
**Tunnel ID** :: [TunnelId](/docs/specs/common-structures#tunnelid) : 4 字节。下一跳的 ID，非零值。

**IV** :: : 16 字节。初始化向量。

**加密数据** :: : 1008 字节。加密的 tunnel 消息。

**总大小：1028 字节**

### Tunnel 消息（已解密）

这些是tunnel数据消息解密后的内容。

```
+----+----+----+----+----+----+----+----+
|    Tunnel ID      |       IV          |
+----+----+----+----+                   +
|                                       |
+                   +----+----+----+----+
|                   |     Checksum      |
+----+----+----+----+----+----+----+----+
|          nonzero padding...           |
~                                       ~
|                                       |
+                                  +----+
|                                  |zero|
+----+----+----+----+----+----+----+----+
|                                       |
|       Delivery Instructions  1        |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+       I2NP Message Fragment 1         +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
|       Delivery Instructions 2...      |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+       I2NP Message Fragment 2...      +
|                                       |
~                                       ~
|                                       |
+                   +-------------------+
|                   |
+----+----+----+----+
```
**Tunnel ID** :: [TunnelId](/docs/specs/common-structures#tunnelid) : 4字节。下一跳的ID，非零值。

**IV** :: : 16 字节。初始化向量。

**校验和** :: : 4 字节。消息内容（零字节后）+ IV 的 SHA256 哈希值的前 4 个字节。

**非零填充** :: : 0 或更多字节。用于填充的随机非零数据。

**Zero** :: : 1字节。值为0x00。

**传送指令** :: TunnelMessageDeliveryInstructions : 长度可变，但通常为 7、39、43 或 47 字节。指示片段和片段的路由。

**消息片段** :: : 1 到 996 字节，实际最大值取决于传递指令大小。部分或完整的 I2NP 消息。

**总大小：1028 字节**

#### 注意事项

- 填充（如果有的话）必须在指令/消息对之前。末尾不提供填充。
- 校验和不覆盖填充或零字节。从第一个传递指令开始获取消息，连接IV，然后对其进行哈希运算。

## tunnel 消息传递指令

指令用单个控制字节编码，后跟任何必要的附加信息。控制字节中的第一位（MSB）决定了如何解释消息头的其余部分 - 如果未设置，则消息要么未分片，要么这是消息中的第一个分片。如果已设置，则这是后续分片。

此规范仅适用于隧道消息内的传递指令。注意"传递指令"也用于 Garlic Cloves 内部，其格式明显不同。详情请参阅 [I2NP 文档](/docs/specs/i2np#garlicclovedeliveryinstructions)。请勿将以下规范用于 Garlic Clove 传递指令！

### 首个分片传递指令

如果第一个字节的MSB为0，这是一个初始的I2NP消息片段，或者是一个完整的（未分片的）I2NP消息，指令如下：

```
+----+----+----+----+----+----+----+----+
|flag|  Tunnel ID (opt)  |              |
+----+----+----+----+----+              +
|                                       |
+                                       +
|         To Hash (optional)            |
+                                       +
|                                       |
+                        +--------------+
|                        |dly | Message
+----+----+----+----+----+----+----+----+
 ID (opt) |extended opts (opt)|  size   |
+----+----+----+----+----+----+----+----+
```
**flag** :: : 1 字节。位序：76543210   - 第 7 位：0 表示初始分片或未分片消息   - 第 6-5 位：传递类型

    - 0x0 = LOCAL
    - 0x01 = TUNNEL
    - 0x02 = ROUTER
    - 0x03 = unused, invalid
    - Note: LOCAL is used for inbound tunnels only, unimplemented for outbound tunnels
- 第4位：是否包含延迟？未实现，始终为0。如果为1，则包含延迟字节。
  - 第3位：是否分片？如果为0，消息未分片，后续内容是完整消息。如果为1，消息已分片，指令中包含消息ID。
  - 第2位：扩展选项？未实现，始终为0。如果为1，则包含扩展选项。
  - 第1-0位：保留位，设为0以兼容未来使用

**Tunnel ID** :: [TunnelId](/docs/specs/common-structures#tunnelid) : 4字节。可选，当传递类型为TUNNEL时存在。目标tunnel ID，非零值。

**To Hash** :: : 32 字节。可选，当传递类型为 ROUTER 或 TUNNEL 时存在。如果是 ROUTER，则为 router 的 SHA256 哈希值。如果是 TUNNEL，则为网关 router 的 SHA256 哈希值。

**Delay** :: : 1字节。可选，如果包含延迟标志被设置则存在。在tunnel消息中：未实现，永远不存在；原始规范：第7位：类型（0 = 严格，1 = 随机化），第6-0位：延迟指数（2^值分钟）。

**消息 ID** :: : 4 字节。可选，仅当此消息是 2 个或更多分片中的第一个时才存在（即，如果分片位为 1）。一个唯一标识所有分片属于单个消息的 ID（当前实现使用 I2NPMessageHeader.msg_id）。

**扩展选项** :: : 2个或更多字节。可选，当扩展选项标志被设置时存在。未实现，从不存在；原始规范：一个字节长度，然后是相应数量的字节。

**size** :: : 2 字节。后续片段的长度。有效值：tunnel 消息中为 1 到大约 960。

**总长度：** 典型长度为：- LOCAL 传输（tunnel 消息）3 字节 - ROUTER 传输 35 字节或 TUNNEL 传输（未分片 tunnel 消息）39 字节 - ROUTER 传输 39 字节或 TUNNEL 传输（首个分片）43 字节

### 后续片段传递指令

如果第一个字节的最高有效位（MSB）为1，这是一个后续分片，指令如下：

```
+----+----+----+----+----+----+----+
|frag|     Message ID    |  size   |
+----+----+----+----+----+----+----+
```
**frag** :: : 1 字节。位顺序：76543210。二进制 1nnnnnnd：   - 位 7：1 表示这是一个后续分片   - 位 6-1：nnnnnn 是 6 位分片编号，从 1 到 63   - 位 0：d 为 1 表示最后一个分片，否则为 0

**消息ID** :: : 4字节。标识此片段所属的片段序列。这将与初始片段的消息ID匹配（标志位7设置为0且标志位3设置为1的片段）。

**size** :: : 2 字节。后续片段的长度。有效值：1 到 996。

**总长度：7 字节**

## 注释

### I2NP 消息最大大小

虽然 I2NP 消息的最大大小名义上是 64 KB，但实际大小会进一步受到将 I2NP 消息分片成多个 1 KB tunnel 消息的方法约束。最大分片数量是 64 个，而且初始分片可能不会完美地对齐在 tunnel 消息的开始位置。因此，消息名义上必须适合放入 63 个分片中。

初始分片的最大大小是956字节（假设使用TUNNEL传输模式）；后续分片的最大大小是996字节。因此最大大小大约是956 + (62 * 996) = 62708字节，或61.2KB。

### 排序、批处理、打包

Tunnel 消息可能会被丢弃或重新排序。创建 tunnel 消息的 tunnel gateway 可以自由实现任何批处理、混合或重新排序策略，以分割 I2NP 消息并将片段高效地打包到 tunnel 消息中。一般来说，最优打包是不可能实现的（"打包问题"）。Gateway 可以实现各种延迟和重新排序策略。

### 掩护流量

Tunnel 消息可能只包含填充数据（即完全没有传递指令或消息片段）用于掩护流量。这个功能尚未实现。

## 参考资料

- **[I2NP]** [I2NP Protocol](/docs/specs/i2np)
- **[I2NP-GC]** [GarlicClove](/docs/specs/i2np#garlicclove)
- **[I2NP-GCDI]** [GarlicCloveDeliveryInstructions](/docs/specs/i2np#garlicclovedeliveryinstructions)
- **[TUNNEL-IMPL]** [Tunnel 实现](/docs/specs/tunnel-implementation)
