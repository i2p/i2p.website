---
title: "通过 I2P 使用 BitTorrent"
description: "I2P 上 BitTorrent 客户端和追踪器的协议规范"
slug: "bittorrent"
lastUpdated: "2026-08"
accurateFor: "0.9.70"
---

I2P 上有多个 bittorrent 客户端和 tracker。由于 I2P 寻址使用 Destination 而不是 IP 和端口，因此需要对 tracker 和客户端软件进行少量修改以在 I2P 上运行。这些修改在下文中进行了说明。请仔细注意与旧版 I2P 客户端和 tracker 兼容性的指导原则。

本页面规定了所有客户端和tracker共同的协议细节。特定的客户端和tracker可能会实现其他独特的功能或协议。

我们欢迎更多客户端和 tracker 软件移植到 I2P。

---

## 开发者通用指南

大多数非Java bittorrent客户端会通过[SAMv3](/docs/api/samv3/)连接到I2P。SAM会话（在I2P内部称为tunnel池或tunnel集合）被设计为长期存在的。大多数bittorrent客户端只需要一个会话，在启动时创建，在退出时关闭。I2P与Tor不同，Tor的电路可能会快速创建和丢弃。在设计应用程序使用超过一到两个同时会话，或快速创建和丢弃会话之前，请仔细思考并咨询I2P开发者。Bittorrent客户端绝不能为每个连接创建唯一的会话。设计你的客户端对announce和客户端连接使用同一个会话。

此外，请确保您的客户端设置（以及对用户关于 router 设置的指导，或者如果您捆绑了 router 则确保 router 默认设置）能够让您的用户向网络贡献的资源多于他们消耗的资源。I2P 是一个对等网络，如果一个流行的应用程序导致网络陷入永久性拥塞，网络就无法生存。

不要通过 I2P outproxy 向明网提供 bittorrent 支持，因为它很可能会被阻止。请咨询 outproxy 运营者以获取指导。

Java I2P 和 i2pd router 实现是独立的，在行为、功能支持和默认设置方面存在细微差异。请使用两个 router 的最新版本测试您的应用程序。

i2pd SAM 默认启用；Java I2P SAM 默认不启用。请为您的用户提供如何在 Java I2P 中启用 SAM 的说明（通过 router 控制台中的 /configclients），和/或在初始连接失败时为用户提供良好的错误信息，例如"确保 I2P 正在运行且 SAM 接口已启用"。

Java I2P 和 i2pd router 对 tunnel 数量有不同的默认设置。Java 的默认值是 2，i2pd 的默认值是 5。对于大多数低到中等带宽和低到中等连接数的情况，3 个就足够了。请在 SESSION CREATE 消息中指定 tunnel 数量，以在 Java I2P 和 i2pd router 之间获得一致的性能。

I2P支持多种签名和加密类型。为了兼容性，I2P默认使用旧的和低效的类型，因此所有客户端都应该指定较新的类型。

如果使用 SAM，签名类型在 DEST GENERATE 和 SESSION CREATE（用于瞬态）命令中指定。所有客户端应设置 SIGNATURE_TYPE=7 (Ed25519)。

加密类型在 SAM SESSION CREATE 命令或 i2cp 选项中指定。允许使用多种加密类型。一些 tracker 支持 ECIES-X25519，一些支持 ElGamal，还有一些同时支持两者。客户端应该设置 i2cp.leaseSetEncType=4,0（用于 ECIES-X25519 和 ElGamal），这样它们就可以连接到两种类型的 tracker。

DHT支持需要SAMv3.3 PRIMARY和SUBSESSIONS功能，以便在同一会话中同时使用TCP和UDP。这将需要客户端进行大量开发工作，除非客户端是用Java编写的。i2pd目前不支持SAMv3.3。libtorrent目前不支持SAMv3.3。

如果没有DHT支持，您可能希望自动向可配置的已知开放tracker列表进行通告，以便磁力链接能够正常工作。请咨询I2P用户以获取当前可用的开放tracker信息，并保持您的默认设置为最新。支持i2p_pex扩展也有助于缓解缺乏DHT支持的问题。

有关开发者如何确保应用程序仅使用所需资源的更多指导，请参阅 [SAMv3 规范](/docs/api/samv3/) 和 [我们的应用程序内嵌 I2P 指南](/docs/applications/embedding/)。如需进一步协助，请联系 I2P 或 i2pd 开发者。

---

## 公告

客户端通常在announce中包含一个伪造的port=6881参数，以兼容较旧的tracker。Tracker可以忽略port参数，并且不应要求提供该参数。

ip参数是客户端[Destination](/docs/specs/common-structures/#struct_Destination)的base 64编码，使用I2P Base 64字母表[A-Z][a-z][0-9]-~。[Destinations](/docs/specs/common-structures/#struct_Destination)长度为387+字节，因此Base 64编码为516+字节。客户端通常会在Base 64 Destination后附加".i2p"以与旧版tracker兼容。Tracker不应要求附加".i2p"。

其他参数与标准 bittorrent 中的相同。

客户端的当前 Destination 为 387 字节或更多（Base 64 编码为 516 字节或更多）。目前假设的合理最大值是 475 字节。由于 tracker 必须解码 Base64 来提供紧凑响应（见下文），tracker 应该在宣告时解码并拒绝错误的 Base64。

默认响应类型为非紧凑型。客户端可以通过参数 compact=1 请求紧凑型响应。tracker 可以在收到请求时返回紧凑型响应，但这不是强制要求。注意：所有主流 tracker 现在都支持紧凑型响应，至少有一个 tracker 在 announce 中要求 compact=1。所有客户端都应该请求并支持紧凑型响应。

强烈建议新 I2P 客户端的开发者通过自己的 tunnel 实现 announce，而不是使用端口 4444 的 HTTP 客户端代理。这样做既更高效，也允许 tracker 执行目标地址验证（见下文）。

UDP 通告的规范已于 2025 年 6 月最终确定。各种 I2P 客户端和 tracker 的支持将在 2025 年下半年陆续推出。请参阅下面的附加信息。

---

## 非紧凑型 Tracker 响应

注意：已弃用。所有流行的 tracker 现在都支持紧凑响应，至少有一个要求在 announce 中使用 compact=1。所有客户端都应该请求并支持紧凑响应。

非紧凑响应与标准 bittorrent 中的相同，但使用 I2P "ip"。这是一个长的 base64 编码的"DNS 字符串"，通常带有 ".i2p" 后缀。

Tracker 通常会包含一个虚假的端口键，或使用来自 announce 的端口，以兼容较旧的客户端。客户端必须忽略端口参数，并且不应要求提供该参数。

ip 键的值是客户端 [Destination](/docs/specs/common-structures/#struct_Destination) 的 base 64 编码，如上所述。为了与旧版本客户端兼容，tracker 通常会在 Base 64 Destination 后面追加 ".i2p"（如果 announce ip 中没有的话）。客户端不应要求响应中必须包含追加的 ".i2p"。

其他响应键和值与标准 bittorrent 中的相同。

---

## 紧凑型 Tracker 响应

在紧凑响应中，"peers" 字典键的值是一个单字节字符串，其长度是32字节的倍数。该字符串包含对等节点的二进制 [Destinations](/docs/specs/common-structures/#struct_Destination) 的连接 [32字节 SHA-256 哈希值](/docs/specs/common-structures/#type_Hash)。这个哈希值必须由 tracker 计算，除非使用了 destination 强制验证（见下文），在这种情况下可以将 X-I2P-DestHash 或 X-I2P-DestB32 HTTP 头中传递的哈希值转换为二进制并存储。peers 键可能缺失，或者 peers 值可能是零长度。

虽然紧凑响应支持对客户端和tracker都是可选的，但强烈建议启用，因为它可以将标准响应大小减少90%以上。

---

## 目标地址强制执行

一些（但不是全部）I2P bittorrent 客户端会通过自己的 tunnel 进行announce。Tracker 可以选择通过要求这样做来防止欺骗，并使用 I2PTunnel HTTP Server tunnel 添加的 HTTP 头来验证客户端的 [Destination](/docs/specs/common-structures/#struct_Destination)。这些头是 X-I2P-DestHash、X-I2P-DestB64 和 X-I2P-DestB32，它们是同一信息的不同格式。这些头无法被客户端伪造。强制要求 destination 的 tracker 完全不需要 ip announce 参数。

由于几个客户端使用HTTP代理而不是自己的tunnel来进行宣告，目标地址强制执行将阻止这些客户端的使用，除非或直到这些客户端转换为通过自己的tunnel进行宣告。

不幸的是，随着网络的增长，恶意行为的数量也会增加，因此我们预期所有tracker最终都会强制验证destinations。tracker和客户端开发者都应该为此做好准备。

---

## 宣布主机名

torrent 文件中的 Announce URL 主机名通常遵循 [I2P 命名标准](/docs/overview/naming/)。除了来自地址簿的主机名和".b32.i2p" Base 32 主机名外，还应该支持完整的 Base 64 Destination（无论是否附加".i2p"）。非开放的 tracker 应该能够识别任何这些格式的自己的主机名。

为了保护匿名性，客户端通常应该忽略种子文件中的非I2P宣布URL。

---

## 客户端连接

客户端到客户端的连接使用标准协议通过 TCP 进行。目前没有已知的 I2P 客户端支持 uTP 通信。

如上所述，I2P 使用 387+ 字节的 [Destinations](/docs/specs/common-structures/#struct_Destination) 作为地址。

如果客户端只有destination的哈希值（比如来自紧凑响应或PEX），它必须通过Base 32编码该哈希值，附加".b32.i2p"，然后查询命名服务来执行查找，命名服务会在可用时返回完整的Destination。

如果客户端在非紧凑响应中收到了对等方的完整 Destination，应该直接在连接建立中使用它。不要将 Destination 转换回 Base 32 哈希进行查找，这样做效率很低。

---

## 跨网络防护

为了保护匿名性，I2P bittorrent 客户端通常不支持非 I2P 的 announce 或对等连接。I2P HTTP 出口代理经常阻止 announce。目前没有已知的 SOCKS 出口代理支持 bittorrent 流量。

为了防止非I2P客户端通过HTTP内部代理使用，I2P tracker通常会阻止包含X-Forwarded-For HTTP标头的访问或公告。Tracker应该拒绝包含IPv4或IPv6 IP地址的标准网络公告，并且不在响应中传递这些公告。

---

## PEX

I2P PEX 基于 ut_pex。由于似乎没有 ut_pex 的正式规范可用，可能需要查看 libtorrent 源码以获得帮助。它是一个扩展消息，在[扩展握手](http://www.bittorrent.org/beps/bep_0010.html)中标识为 "i2p_pex"。它包含一个 bencoded 字典，最多有 3 个键："added"、"added.f" 和 "dropped"。added 和 dropped 值都是单个字节字符串，其长度是 32 字节的倍数。这些字节字符串是对等节点的二进制 [Destinations](/docs/specs/common-structures/#struct_Destination) 的 SHA-256 哈希值的连接。这与上面指定的 i2p 紧凑响应格式中的 peers 字典值格式相同。added.f 值（如果存在）与 ut_pex 中的相同。

---

## DHT

从 0.9.2 版本开始，i2psnark 客户端已包含 DHT 支持。与 [BEP 5](http://www.bittorrent.org/beps/bep_0005.html) 的初步差异如下所述，这些差异可能会发生变化。如果您希望开发支持 DHT 的客户端，请联系 I2P 开发人员。

与标准DHT不同，I2P DHT不在选项握手或PORT消息中使用位标识。它通过扩展消息进行通告，在[扩展握手](http://www.bittorrent.org/beps/bep_0010.html)中标识为"i2p_dht"。它包含一个bencoded字典，有两个键："port"和"rport"，都是整数。

紧凑节点信息中列出的UDP（数据报）端口用于接收可回复的（已签名）数据报。这用于查询，除了公告之外。我们称之为"查询端口"。这是扩展消息中的"port"值。查询使用[I2CP](/docs/specs/i2cp/)协议编号17。

除了UDP端口之外，我们还使用第二个数据报端口，等于查询端口 + 1。该端口用于接收未签名（原始）数据报，包括回复、错误和公告。该端口提高了效率，因为回复包含查询中发送的令牌，无需签名。我们称之为"响应端口"。这是扩展消息中的"rport"值。它必须等于查询端口 + 1。响应和公告使用[I2CP](/docs/specs/i2cp/)协议编号18。

紧凑对等节点信息是32字节（32字节SHA256哈希），而不是4字节IP + 2字节端口。没有对等节点端口。在响应中，"values"键是一个字符串列表，每个字符串包含一个紧凑对等节点信息。

紧凑节点信息为54字节（20字节节点ID + 32字节SHA256哈希 + 2字节端口），而不是20字节节点ID + 4字节IP + 2字节端口。在响应中，"nodes"键是一个包含连接的紧凑节点信息的单字节字符串。

安全节点ID要求：为了增加各种DHT攻击的难度，节点ID的前4个字节必须与目标Hash的前4个字节匹配，节点ID的接下来两个字节必须与目标hash的接下来两个字节与端口进行异或运算后的结果匹配。

在torrent文件中，无tracker的torrent字典"nodes"键仍待确定。它可以是一个32字节二进制字符串列表（SHA256哈希），而不是包含主机字符串和端口整数的列表的列表。替代方案：单个字节字符串包含连接的哈希，或仅包含字符串的列表。

---

## 数据报 (UDP) Tracker

I2P 中 UDP announce 的规范已于 2025 年 6 月最终确定。各种 I2P 客户端和 tracker 的支持将在 2025 年晚些时候陆续推出。与 [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) 的差异记录在 [UDP announce 规范](/docs/specs/udp-announces/) 中。该规范还要求支持 [新的 Datagram 2/3 格式](/docs/specs/datagrams/)。

---

## 附加信息

关于计算允许的快速集合的初步规范见[提案 172](/proposals/172-bep6-allowed-fast)

---

## 附加信息

- I2P bittorrent 标准通常在 [zzz.i2p](http://zzz.i2p/) 上讨论。
- 当前 tracker 软件功能对比图表[也可在那里找到](http://zzz.i2p/files/trackers.html)。
- [I2P bittorrent 常见问题解答](http://forum.i2p/viewtopic.php?t=2068)
- [I2P 上的 DHT 讨论](http://zzz.i2p/topics/812)
