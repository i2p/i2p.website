---
title: "用于加密 leaseSet 的 B32"
description: "加密的 LS2 leaseSet 的 Base 32 地址格式"
slug: "b32-for-encrypted-leasesets"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
status: "已实现"
---

## 概览

标准 Base 32 ("b32") 地址包含目标（Destination）的哈希值。这对加密的 LS2（LeaseSet 2，I2P 的新一代 leaseSet 格式；提案 123）不起作用。

对于加密的 LS2（提案 123），我们不能使用传统的 Base32 地址，因为它仅包含 destination（目标标识）的哈希。
它不提供非盲化公钥。
客户端必须知道 destination 的公钥、签名类型、盲化签名类型，以及一个可选的 secret（共享密钥）或私钥，才能获取并解密 leaseset。
因此，仅有一个 Base32 地址是不够的。
客户端需要完整的 destination（其中包含公钥），或者单独的公钥。
如果客户端在地址簿中保存了完整的 destination，且该地址簿支持按哈希反向查询，则可以取回公钥。

这种格式将公钥而不是哈希放入 base32 地址中。这种格式还必须包含公钥所使用的签名算法类型，以及盲化方案所使用的签名算法类型。

本文档为这些地址规定了 b32 格式。虽然我们在讨论中将这种新格式称为 "b33" 地址，但实际的新格式仍保留通常的 ".b32.i2p" 后缀。

## 实现状态

提案 123（新的 netDB 条目）在 0.9.43 版（2019 年 10 月）中已全部实现。加密的 LS2（第二代 leaseSet）功能集一直保持稳定，直至 2.10.0 版（2025 年 9 月），未对寻址格式或密码规范引入任何破坏性变更。

关键实现里程碑: - 0.9.38: 对带离线密钥的标准 LS2 的 Floodfill 支持 - 0.9.39: RedDSA 签名类型 11 与基本的加密/解密 - 0.9.40: 完整的 B32 地址支持 (提案 149) - 0.9.41: 基于 X25519 的逐客户端认证 - 0.9.42: 全部盲化（blinding）功能可用 - 0.9.43: 宣布实现完成 (2019 年 10 月)

## 设计

- 新格式包含未盲化公钥、未盲化签名类型以及盲化签名类型。
- 可选地指示私有链接对 secret（共享密钥）和/或私钥的要求。
- 使用现有的 ".b32.i2p" 后缀，但长度更长。
- 包含用于错误检测的校验和。
- 加密的 leaseSet 的地址由 56 个或更多编码字符（35 个或更多解码字节）标识，相比之下，传统 Base32 地址为 52 个字符（32 字节）。

## 规范

### 创建与编码

按如下方式构造一个形如 {56+ chars}.b32.i2p 的主机名（对应的二进制为 35+ 个字符）：

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
b32 末尾的任何未使用位都必须为 0。对于标准的 56 个字符（35 字节）地址，不存在未使用的位。

### 解码与验证

```
strip the ".b32.i2p" from the hostname
data = Base32.decode(hostname)
Calculate checksum = CRC-32(data[3:end])
Treat checksum as little-endian.
flags = data[0] ^ (byte) checksum
if 1 byte sigtypes:
  pubkey sigtype = data[1] ^ (byte) (checksum >> 8)
  blinded sigtype = data[2] ^ (byte) (checksum >> 16)
else (2 byte sigtypes):
  pubkey sigtype = data[1] ^ ((byte) (checksum >> 8)) || data[2] ^ ((byte) (checksum >> 16))
  blinded sigtype = data[3] || data[4]
parse the remainder based on the flags to get the public key
```
### 秘密与私钥位数

共享密钥和私钥的标志位用于向客户端、代理或其他客户端代码表明：解密该 leaseset 需要提供共享密钥和/或私钥。具体实现可能会提示用户提供所需数据，或者在缺少所需数据时拒绝连接尝试。

这些比特仅用作标识。绝不能在 B32 地址（基于 Base32 编码的 I2P 地址）本身中包含对称密钥或私钥，否则会危及安全。

## 密码学细节

### 盲化方案

该盲化方案采用基于 Ed25519 并借鉴 ZCash 设计的 RedDSA，使用 SHA-512 在 Ed25519 曲线上生成 Red25519 签名。这种方法确保被盲化的公钥仍然处于素数阶子群上，从而避免了一些替代设计中的安全隐患。

盲化密钥根据 UTC 日期每日轮换，使用以下公式：

```
blinded_key = BLIND(unblinded_key, date, optional_secret)
```
DHT 存储位置的计算方式如下：

```
SHA256(type_byte || blinded_public_key)
```
### 加密

加密的 leaseset 使用 ChaCha20 流密码进行加密，之所以选择它，是因为在缺乏 AES 硬件加速的设备上具有更优的性能。该规范采用 HKDF 进行密钥派生，并使用 X25519 进行 Diffie-Hellman 运算。

加密的 leasesets 具有三层结构: - 外层: 明文元数据 - 中间层: 客户端认证（DH 或 PSK 方法） - 内层: 包含租约信息的实际 LS2 数据

### 身份验证方法

针对每个客户端的身份验证支持两种方法：

**DH 认证**: 使用 X25519（基于 Curve25519 的密钥协商算法）进行密钥协商。每个已授权的客户端向服务器提供其公钥，服务器使用由 ECDH（椭圆曲线 Diffie-Hellman 密钥交换）派生的共享密钥对中间层进行加密。

**PSK 身份验证**: 直接使用预共享密钥进行加密。

B32 地址中的第 2 个标志位表示是否需要针对每个客户端的身份验证。

## 缓存

虽然这超出了本规范的范围，但 routers 和客户端必须记住并缓存（建议持久化）从公钥到 Destination（目标标识）的映射，以及反向映射。

blockfile naming service（blockfile 命名服务）作为自 0.9.8 版起 I2P 的默认地址簿系统，维护多个地址簿，并包含专用的反向查找映射，支持按哈希的快速查找。 当最初只知道哈希时，此功能对于加密的 leaseSet 解析至关重要。

## 签名类型

截至 I2P 版本 2.10.0，签名类型 0 至 11 已定义。单字节编码仍然是标准，双字节编码虽可用，但在实践中未使用。

**常用类型：** - 类型 0 (DSA_SHA1)：对 router 已弃用，仍支持用于目的地 - 类型 7 (EdDSA_SHA512_Ed25519)：当前用于 router 身份和目的地的标准 - 类型 11 (RedDSA_SHA512_Ed25519)：仅用于支持盲化的加密 LS2 leasesets

**重要说明**：只有 Ed25519（类型 7）和 Red25519（类型 11）支持加密的 leaseSet 所需的盲化。其他签名类型不能用于此功能。

类型 9-10（GOST 算法）仍为保留状态，但尚未实现。类型 4-6 和 8 被标记为 "offline only"，用于离线签名密钥。

## 备注

- 通过长度区分旧版与新版变体。旧版 b32 地址始终为 {52 chars}.b32.i2p。新版为 {56+ chars}.b32.i2p
- base32 编码遵循 RFC 4648 标准，解码不区分大小写，输出优先使用小写
- 当使用具有更大公钥的签名类型时，地址可能超过 200 个字符（例如 ECDSA P521，132 字节密钥）
- 如有需要，新格式可用于 jump links（跳转链接）（并可由 jump servers（跳转服务器）提供），与标准 b32 一样
- 为增强隐私，blinded keys（盲化密钥）会基于 UTC 日期每日轮换
- 该格式与 Tor 的 rend-spec-v3.txt 附录 A.2 的方法不同，这种差异在使用不在曲线上的（off-curve）盲化公钥时可能带来潜在的安全影响

## 版本兼容性

本规范在 I2P 版本 0.9.47（2020 年 8 月）至 2.10.0（2025 年 9 月）期间均准确适用。在此期间，B32 addressing format（B32 地址格式）、encrypted LS2 structure（加密的 LS2 结构）以及密码学实现均未发生任何破坏兼容性的更改。使用 0.9.47 创建的所有地址与当前版本保持完全兼容。

## 参考资料

**CRC-32** - [CRC-32（维基百科）](https://en.wikipedia.org/wiki/CRC-32) - [RFC 3309：流控制传输协议校验和](https://tools.ietf.org/html/rfc3309)

**I2P 规范** - [加密 LeaseSet 规范](/docs/specs/encryptedleaseset/) - [提案 123：新的 netDB 条目](/proposals/123-new-netdb-entries/) - [提案 149：用于加密 LS2（LeaseSet v2，LeaseSet 第2版）的 B32](/proposals/149-b32-encrypted-ls2/) - [通用结构规范](/docs/specs/common-structures/) - [命名与地址簿](/docs/overview/naming/)

**Tor 比较** - [Tor 讨论帖（设计背景）](https://lists.torproject.org/pipermail/tor-dev/2017-January/011816.html)

**其他资源** - [I2P 项目](/) - [I2P 论坛](https://i2pforum.net) - [Java API 文档](http://docs.i2p-projekt.de/javadoc/)
