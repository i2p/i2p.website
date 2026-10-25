---
title: "命名和地址簿"
description: "I2P 如何将人类可读的主机名映射到目标地址"
slug: "naming"
aliases:
  - "/zh/docs/specs/naming"
  - "/zh/docs/specs/naming/"
  - "/zh/docs/naming"
  - "/zh/docs/naming/"
lastUpdated: "2025-01"
accurateFor: "0.9.65"
---

## 概述

I2P 附带了一个通用命名库和一个基础实现，旨在基于本地名称到目标地址的映射工作，以及一个名为[地址簿](#address-book)的附加应用程序。I2P 还支持类似于 Tor 的 .onion 地址的 [Base32 主机名](#base32-names)。

地址簿是一个基于信任网络驱动的安全、分布式和人类可读的命名系统，只牺牲了所有人类可读名称必须全局唯一的要求，而仅要求本地唯一性。虽然I2P中的所有消息都通过其destination进行密码学寻址，但不同的人可以在本地地址簿中拥有指向不同destinations的"Alice"条目。人们仍然可以通过导入其信任网络中指定对等节点的已发布地址簿、添加第三方提供的条目，或者（如果某些人使用先到先得的注册系统组织一系列已发布的地址簿）选择将这些地址簿视为名称服务器来发现新名称，从而模拟传统的DNS。

注意：关于 I2P 命名系统的设计理念、常见反对意见和可能的替代方案，请参阅[命名讨论](/docs/legacy/naming/)页面。

---

## 命名系统组件

I2P中没有中央命名权威机构。所有主机名都是本地的。

命名系统相当简单，其大部分功能都在router外部的应用程序中实现，但这些应用程序与I2P发行版捆绑在一起。其组件包括：

1. 本地[命名服务](#naming-services)，它执行查找并处理[Base32 主机名](#base32-names)。
2. [HTTP 代理](#http-proxy)，它向 router 请求查找，并将用户指向远程跳转服务以协助处理失败的查找。
3. HTTP [主机添加表单](#host-add-services)，允许用户将主机添加到本地 hosts.txt 中。
4. HTTP [跳转服务](#jump-services)，提供自己的查找和重定向功能。
5. [地址簿](#address-book)应用程序，它将通过 HTTP 检索的外部主机列表与本地列表合并。
6. [SusiDNS](#susidns) 应用程序，它是一个用于地址簿配置和查看本地主机列表的简单 Web 前端。

---

## 命名服务

I2P中的所有目标地址都是516字节（或更长）的密钥。（更准确地说，它是一个256字节的公钥加上一个128字节的签名密钥再加上一个3字节或更多的证书，在Base64表示中是516字节或更多。现在使用非空[证书](/docs/legacy/naming/#certificates)来指示签名类型。因此，最近生成的目标地址中的证书都超过3字节。

如果应用程序（i2ptunnel 或 HTTP 代理）希望通过名称访问目标地址，router 会执行一个非常简单的本地查找来解析该名称。

### Hosts.txt 命名服务

hosts.txt 命名服务通过文本文件进行简单的线性搜索。该命名服务在 0.8.8 版本之前是默认服务，之后被 Blockfile 命名服务所取代。当文件增长到数千条条目后，hosts.txt 格式变得过于缓慢。

它按顺序对三个本地文件进行线性搜索，以查找主机名并将其转换为516字节的目标密钥。每个文件都采用简单的[配置文件格式](/docs/specs/configuration/)，格式为hostname=base64，每行一个。这些文件是：

1. privatehosts.txt
2. userhosts.txt
3. hosts.txt

### Blockfile 命名服务

Blockfile 命名服务将多个"地址簿"存储在名为 hostsdb.blockfile 的单个数据库文件中。此命名服务自 0.8.8 版本起成为默认选项。

blockfile 是多个有序映射（键值对）的简单磁盘存储，实现为跳表。blockfile 格式在 [Blockfile 页面](/docs/specs/blockfile/) 中指定。它以紧凑格式提供快速的 Destination 查找。虽然 blockfile 的开销很大，但目标地址以二进制格式存储，而不是像 hosts.txt 格式中的 Base 64。此外，blockfile 提供为每个条目存储任意元数据（如添加日期、来源和注释）的功能，以实现高级地址簿特性。blockfile 的存储需求比 hosts.txt 格式适度增加，并且 blockfile 的查找时间大约减少 10 倍。

在创建时，命名服务会从 hosts.txt 命名服务使用的三个文件中导入条目。blockfile 通过维护三个按顺序搜索的映射来模拟之前的实现，这些映射分别命名为 privatehosts.txt、userhosts.txt 和 hosts.txt。它还维护一个反向查找映射来实现快速反向查找。

### 其他命名服务功能

查找不区分大小写。使用第一个匹配项，不会检测冲突。在查找中不强制执行命名规则。查找会缓存几分钟。Base 32 解析在[下文](#base32-names)中描述。有关命名服务 API 的完整描述，请参阅[命名服务 Javadocs](http://idk.i2p/javadoc-i2p/net/i2p/client/naming/package-summary.html)。该 API 在 0.8.7 版本中进行了显著扩展，提供了添加和删除功能、与主机名一起存储任意属性以及其他功能。

### 替代和实验性命名服务

命名服务通过配置属性 `i2p.naming.impl=class` 来指定。其他实现方式也是可能的。例如，在 router 内部有一个实验性功能，可以通过网络进行实时查找（类似于 DNS）。更多信息请参见[讨论页面上的替代方案](/docs/legacy/naming/#alternatives)。

HTTP代理通过router对所有以'.i2p'结尾的主机名进行查找。否则，它会将请求转发到配置的HTTP出口代理。因此，在实践中，所有HTTP（I2P站点）主机名必须以伪顶级域名'.i2p'结尾。

如果 router 无法解析主机名，HTTP 代理会向用户返回一个错误页面，其中包含指向多个"跳转"服务的链接。详情请参见下文。

---

## .i2p.alt 域名

我们之前[申请保留 .i2p TLD](https://datatracker.ietf.org/doc/draft-grothoff-iesg-special-use-p2p-names/)，遵循了 [RFC 6761](https://www.rfc-editor.org/rfc/rfc6761.html) 中规定的程序。然而，这一申请以及所有其他申请都被拒绝了，RFC 6761 被宣布为一个"错误"。

经过 GNUnet 团队和其他人多年的努力，.alt 域名在 2023 年末被 [RFC 9476](https://www.rfc-editor.org/rfc/rfc9476.html) 保留为特殊用途顶级域名。虽然没有 IANA 认可的官方注册商，但我们已经在主要的非官方注册商 [GANA](https://gana.gnunet.org/dot-alt/dot_alt.html) 注册了 .i2p.alt 域名。这并不能阻止其他人使用该域名，但应该有助于阻止这种情况。

.alt 域名的一个好处是，理论上，DNS 解析器在更新以符合 RFC 9476 后将不会转发 .alt 请求，这将防止 DNS 泄漏。为了与 .i2p.alt 主机名兼容，I2P 软件和服务应该更新以通过去除 .alt 顶级域名来处理这些主机名。这些更新计划在 2024 年上半年进行。

目前，还没有计划将 .i2p.alt 作为显示和交换 I2P 主机名的首选形式。这是一个需要进一步研究和讨论的话题。

---

## 地址簿

### 传入订阅和合并

地址簿应用程序会定期检索其他用户的 hosts.txt 文件，经过多项检查后将它们与本地 hosts.txt 文件合并。命名冲突按照先到先得的原则解决。

订阅另一个用户的hosts.txt文件需要给予他们一定程度的信任。例如，你不希望他们通过在将新的主机/密钥条目传递给你之前快速输入自己的密钥来"劫持"一个新站点。

因此，默认配置的唯一订阅是 `http://i2p-projekt.i2p/hosts.txt (http://udhdrtrcetjm5sxzskjyr5ztpeszydbh4dpl3pl4utgqqw2v4jna.b32.i2p/hosts.txt)`，它包含了 I2P 发布版中包含的 hosts.txt 的副本。用户必须在本地地址簿应用程序中配置额外的订阅（通过 subscriptions.txt 或 [SusiDNS](#susidns)）。

其他一些公共地址簿订阅链接：

- http://i2host.i2p/cgi-bin/i2hostetag
- http://stats.i2p/cgi-bin/newhosts.txt

这些服务的运营者可能有不同的主机列表政策。出现在此列表中并不意味着获得认可。

### 命名规则

虽然在 I2P 内部希望不会对主机名有任何技术限制，但地址簿对从订阅导入的主机名强制执行了几项限制。这样做是为了基本的排版合理性和浏览器兼容性，以及安全考虑。这些规则本质上与 RFC2396 第 3.2.2 节中的规则相同。任何违反这些规则的主机名可能不会传播到其他 router。

命名规则：

- 名称在导入时会转换为小写。
- 名称在转换为小写后，会检查是否与现有的 userhosts.txt 和 hosts.txt（但不包括 privatehosts.txt）中的现有名称冲突。
- 转换为小写后必须只包含 [a-z] [0-9] '.' 和 '-'。
- 不能以 '.' 或 '-' 开头。
- 必须以 '.i2p' 结尾。
- 最多 67 个字符，包括 '.i2p'。
- 不能包含 '..'。
- 不能包含 '.-' 或 '-.'（从 0.6.1.33 版本开始）。
- 除了用于 IDN 的 'xn--' 外，不能包含 '--'。
- Base32 主机名（*.b32.i2p）保留用于 base 32 使用，因此不允许导入。
- 某些为项目使用而保留的主机名不被允许（proxy.i2p、router.i2p、console.i2p、mail.i2p、*.proxy.i2p、*.router.i2p、*.console.i2p、*.mail.i2p 和其他）
- 以 'www.' 开头的主机名不被鼓励，会被一些注册服务拒绝。一些地址簿实现会自动从查找中去掉 'www.' 前缀。因此注册 'www.example.i2p' 是不必要的，而为 'www.example.i2p' 和 'example.i2p' 注册不同的目标将使 'www.example.i2p' 对某些用户不可达。
- 检查密钥的 base64 有效性。
- 检查密钥是否与 hosts.txt（但不包括 privatehosts.txt）中的现有密钥冲突。
- 最小密钥长度 516 字节。
- 最大密钥长度 616 字节（以适应最多 100 字节的证书）。

通过订阅接收到的任何通过所有检查的名称都会通过本地命名服务添加。

请注意，主机名中的"."符号没有任何意义，不表示任何实际的命名或信任层次结构。如果名称"host.i2p"已经存在，没有任何措施可以阻止任何人向其hosts.txt文件添加名称"a.host.i2p"，并且这个名称可以被其他人的地址簿导入。拒绝非域名"所有者"使用子域名的方法（证书？）以及这些方法的可取性和可行性，是未来讨论的话题。

国际化域名（IDN）在 i2p 中也能工作（使用 punycode 'xn--' 格式）。要在 Firefox 的地址栏中正确显示 IDN .i2p 域名，请在 about:config 中添加 'network.IDN.whitelist.i2p (boolean) = true'。

由于地址簿应用程序完全不使用 privatehosts.txt，实际上这个文件是放置私人别名或为 hosts.txt 中已有站点设置"昵称"的唯一合适位置。

### 高级订阅源格式

从 0.9.26 版本开始，订阅站点和客户端可能支持高级的 hosts.txt 订阅协议，该协议包含元数据（包括签名）。此格式与标准的 hosts.txt hostname=base64destination 格式向后兼容。详情请参见[规范](/docs/specs/subscription/)。

### 发送订阅

地址簿会将合并后的hosts.txt发布到某个位置（通常是本地I2P站点主目录中的hosts.txt），供其他人访问以进行订阅。此步骤是可选的，默认情况下处于禁用状态。

### 托管和HTTP传输问题

地址簿应用程序与 eepget 一起，保存订阅的 web 服务器返回的 Etag 和/或 Last-Modified 信息。这大大减少了所需的带宽，因为如果没有任何更改，web 服务器在下次获取时将返回 '304 Not Modified'。

但是如果hosts.txt文件发生了更改，整个文件都会被下载。关于此问题的讨论请参见下文。

强烈建议提供静态 hosts.txt 或等效 CGI 应用程序的主机发送 Content-Length 标头，以及 Etag 或 Last-Modified 标头。还要确保服务器在适当时发送 '304 Not Modified' 响应。这将显著减少网络带宽使用，并降低损坏的可能性。

---

## 主机添加服务

主机添加服务是一个简单的CGI应用程序，它接受主机名和Base64密钥作为参数，并将其添加到本地的hosts.txt文件中。如果其他router订阅了该hosts.txt，新的主机名/密钥将会在网络中传播。

建议主机添加服务至少实施上述地址簿应用程序所施加的限制。主机添加服务可能对主机名和密钥施加额外限制，例如：

- 对"子域名"数量的限制。
- 通过各种方法对"子域名"进行授权。
- Hashcash 或签名证书。
- 对主机名和/或内容进行编辑审查。
- 按内容对主机进行分类。
- 保留或拒绝某些主机名。
- 对给定时间段内注册的名称数量进行限制。
- 注册和发布之间的延迟。
- 要求主机在线以进行验证。
- 过期和/或撤销。
- IDN 欺骗拒绝。

---

## 跳转服务

jump服务是一个简单的CGI应用程序，它接受一个主机名作为参数，并返回一个301重定向到正确的URL，同时附加一个`?i2paddresshelper=key`字符串。HTTP代理将解释这个附加的字符串，并使用该密钥作为实际目的地。此外，代理会缓存该密钥，因此在重启之前不需要地址助手。

请注意，与订阅服务类似，使用跳转服务意味着需要一定程度的信任，因为跳转服务可能恶意地将用户重定向到错误的目标地址。

为了提供最佳服务，jump 服务应该订阅多个 hosts.txt 提供商，以确保其本地主机列表保持最新。

---

## SusiDNS

SusiDNS 只是一个用于配置地址簿订阅和访问四个地址簿文件的 Web 界面前端。所有实际工作都由"地址簿"应用程序完成。

目前，SusiDNS 内部对地址簿命名规则的执行很少，因此用户可能会在本地输入一些主机名，这些主机名在地址簿订阅规则下会被拒绝。

---

## Base32 名称

I2P支持Base32主机名，类似于Tor的.onion地址。Base32地址比完整的516字符Base64目标地址或地址助手要短得多，也更容易处理。示例：`ukeu3k5oycgaauneqgtnvselmt4yemvoilkln7jpvamvfx7dnkdq.b32.i2p`

在 Tor 中，地址是 16 个字符（80 位），或者是 SHA-1 哈希的一半。I2P 使用 52 个字符（256 位）来表示完整的 SHA-256 哈希。格式为 {52 chars}.b32.i2p。Tor 有一个[提案](https://blog.torproject.org/blog/tor-weekly-news-%E2%80%94-december-4th-2013)要转换为相同的 {52 chars}.onion 格式用于他们的隐藏服务。Base32 在命名服务中实现，该服务通过 I2CP 查询 router 来查找 LeaseSet 以获取完整的 Destination。Base32 查找只有在 Destination 运行并发布 LeaseSet 时才会成功。由于解析可能需要网络数据库查找，因此可能比本地地址簿查找花费更长的时间。

Base32 地址可以在大多数使用主机名或完整目标地址的地方使用，但是在某些情况下，如果名称无法立即解析，它们可能会失败。例如，如果名称无法解析为目标地址，I2PTunnel 将会失败。

---

## 扩展 Base32 名称

扩展 base 32 名称在 0.9.40 版本中引入，用于支持加密 leaseSet。加密 leaseSet 的地址由 56 个或更多编码字符标识（不包括".b32.i2p"部分，即 35 个或更多解码字节），而传统 base 32 地址为 52 个字符（32 字节）。有关更多信息，请参阅提案 123 和 149。

标准 Base 32 ("b32") 地址包含目标的哈希值。这对于加密的 ls2（提案 123）不起作用。

您无法为加密的 LS2（提案 123）使用传统的 base 32 地址，因为它只包含目标的哈希值。它不提供非盲化的公钥。客户端必须知道目标的公钥、签名类型、盲化签名类型，以及可选的密钥或私钥来获取和解密 leaseSet。因此，仅凭 base 32 地址是不够的。客户端需要完整的目标（包含公钥）或单独的公钥。如果客户端在地址簿中有完整的目标，并且地址簿支持通过哈希值进行反向查找，那么可以检索到公钥。

因此我们需要一种新格式，将公钥而不是哈希值放入base32地址中。这种格式还必须包含公钥的签名类型和盲化方案的签名类型。

本节记录了这些地址的新 b32 格式。虽然我们在讨论中将这种新格式称为"b33"地址，但实际的新格式保留了通常的".b32.i2p"后缀。

### 创建和编码

构建一个格式为 {56+ chars}.b32.i2p 的主机名（二进制为 35+ 字符），步骤如下。首先，构建要进行 base 32 编码的二进制数据：

```
flag (1 byte)
  bit 0: 0 for one-byte sigtypes, 1 for two-byte sigtypes
  bit 1: 0 for no secret, 1 if secret is required
  bit 2: 0 for no per-client auth,
         1 if client private key is required
  bits 7-3: Unused, set to 0

public key sigtype (1 or 2 bytes as indicated in flags)
  If 1 byte, the upper byte is assumed zero

blinded key sigtype (1 or 2 bytes as indicated in flags)
  If 1 byte, the upper byte is assumed zero

public key
  Number of bytes as implied by sigtype
```
后处理和校验和：

```
Construct the binary data as above.
Treat checksum as little-endian.
Calculate checksum = CRC-32(data[3:end])
data[0] ^= (byte) checksum
data[1] ^= (byte) (checksum >> 8)
data[2] ^= (byte) (checksum >> 16)

hostname = Base32.encode(data) || ".b32.i2p"
```
b32末尾的任何未使用位必须为0。对于标准的56字符（35字节）地址，没有未使用的位。

### 解码和验证

```
Strip the ".b32.i2p" from the hostname
data = Base32.decode(hostname)
Calculate checksum = CRC-32(data[3:end])
Treat checksum as little-endian.
flags = data[0] ^ (byte) checksum
if 1 byte sigtypes:
  pubkey sigtype = data[1] ^ (byte) (checksum >> 8)
  blinded sigtype = data[2] ^ (byte) (checksum >> 16)
else (2 byte sigtypes) :
  pubkey sigtype = data[1] ^ ((byte) (checksum >> 8)) || data[2] ^ ((byte) (checksum >> 16))
  blinded sigtype = data[3] || data[4]
parse the remainder based on the flags to get the public key
```
### 密钥和私钥位数

secret 和 private key 位用于向客户端、代理或其他客户端代码指示需要 secret 和/或 private key 来解密 leaseset。特定实现可能会提示用户提供所需数据，或在缺少所需数据时拒绝连接尝试。

### 注意事项

- 将前3个字节与哈希进行XOR运算提供了有限的校验和能力，并确保开头的所有base32字符都是随机化的。只有少数几种标志和签名类型组合是有效的，因此任何拼写错误都可能创建无效组合并被拒绝。
- 在通常情况下（1字节签名类型，无密钥，无per-client auth），主机名将是{56 chars}.b32.i2p，解码为35字节，与Tor相同。
- Tor的2字节校验和有1/64K的假阴性率。使用3字节，减去一些被忽略的字节，我们的假阴性率接近百万分之一，因为大多数标志/签名类型组合都是无效的。
- Adler-32对于小输入和检测小变化来说是一个糟糕的选择。我们使用CRC-32代替。CRC-32速度快且广泛可用。
- 虽然超出了本规范的范围，router和/或客户端必须记住并缓存（可能是持久性的）公钥到destination的映射，反之亦然。
- 通过长度区分新旧格式。旧的b32地址总是{52 chars}.b32.i2p。新的是{56+ chars}.b32.i2p
- Tor讨论线程[在这里](https://lists.torproject.org/pipermail/tor-dev/2017-January/011816.html)
- 不要期望会出现2字节签名类型，我们目前只到13。现在不需要实现。
- 如果需要，新格式可以用在跳转链接中（并由跳转服务器提供），就像b32一样。
- 任何超过32字节的密钥、私钥或公钥都会超过DNS标签长度63字符的限制。浏览器可能不在意。
- 没有向后兼容性问题。较长的b32地址在旧软件中将无法转换为32字节哈希。
