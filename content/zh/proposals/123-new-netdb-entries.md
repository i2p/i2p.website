---
title: "新的 netDB 条目"
number: "123"
author: "zzz, str4d, orignal"
created: "2016-01-16"
lastupdated: "2020-07-18"
status: "打开"
thread: "http://zzz.i2p/topics/2051"
supercedes: "110, 120, 121, 122"
toc: true
---

## 状态

该提案的部分内容已完成，并在 0.9.38 和 0.9.39 版本中实现。Common Structures、I2CP、I2NP 和其他规范现已更新，以反映当前支持的更改。

已完成的部分仍可能进行小幅修订。本提案的其他部分仍在开发中，可能会有重大修订。

服务查找（类型 9 和 11）是低优先级且非计划性的，可能会分离到单独的提案中。

## 概述

这是对以下4个提案的更新和汇总：

- 110 LS2
- 120 用于大规模多宿主的 Meta LS2
- 121 加密的 LS2
- 122 未认证服务查找（任播）

这些提案大多数是独立的，但为了合理性，我们为其中几个定义并使用了通用格式。

以下提案有一定的相关性：

- 140 不可见多宿主 (与此提案不兼容)
- 142 新加密模板 (用于新的对称加密)
- 144 ECIES-X25519-AEAD-Ratchet
- 145 ECIES-P256
- 146 Red25519
- 148 EdDSA-BLAKE2b-Ed25519
- 149 加密 LS2 的 B32
- 150 Garlic Farm Protocol
- 151 ECDSA 盲化

## 提案

该提案定义了5种新的DatabaseEntry类型，以及将它们存储到网络数据库和从网络数据库检索它们的过程，还有对它们进行签名和验证这些签名的方法。

### Goals

- 向后兼容
- LS2 可与旧式多宿主配合使用
- 无需新的加密算法或原语来支持
- 保持加密和签名的解耦；支持所有当前和未来版本
- 启用可选的离线签名密钥
- 降低时间戳精度以减少指纹识别
- 为目标启用新的加密算法
- 启用大规模多宿主
- 修复现有加密 LS 的多个问题
- 可选盲化以减少 floodfill 的可见性
- 加密版本同时支持单密钥和多个可撤销密钥
- 服务查找功能，便于查找出站代理、应用程序 DHT 引导节点和其他用途
- 不破坏依赖 32 字节二进制目标哈希的任何功能，例如 bittorrent
- 通过属性为 leaseSet 添加灵活性，就像我们在 routerinfo 中拥有的一样
- 将发布时间戳和可变过期时间放在头部，这样即使内容被加密也能正常工作（不从最早的 lease 派生时间戳）
- 所有新类型都存在于相同的 DHT 空间和与现有 leaseSet 相同的位置，
  这样用户可以从旧的 LS 迁移到 LS2，
  或在 LS2、Meta 和 Encrypted 之间切换，
  而无需更改目标或哈希
- 现有目标可以转换为使用离线密钥，
  或回到在线密钥，而无需更改目标或哈希

### Non-Goals / Out-of-scope

- 新的 DHT 轮换算法或共享随机数生成
- 具体的新加密类型以及使用该新类型的端到端加密方案
  将在单独的提案中说明。
  此处不指定或讨论新的加密技术。
- 用于 RI 或隧道构建的新加密。
  这将在单独的提案中说明。
- I2NP DLM / DSM / DSRM 消息的加密、传输和接收方法。
  不会更改。
- 如何生成和支持 Meta，包括后端 router 间通信、管理、故障转移和协调。
  可能会为 I2CP 或 i2pcontrol 或新协议添加支持。
  这可能会标准化，也可能不会。
- 如何实际实现和管理更长过期时间的隧道，或取消现有隧道。
  这极其困难，没有这个功能就无法实现合理的优雅关闭。
- 威胁模型变化
- 离线存储格式，或存储/检索/共享数据的方法。
- 实现细节在此处不作讨论，留给各个项目自行处理。

### Justification

LS2 增加了用于更改加密类型和未来协议变更的字段。

加密 LS2 通过对整个 lease 集合使用非对称加密，修复了现有加密 LS 的几个安全问题。

Meta LS2 提供灵活、高效、有效且大规模的多宿主功能。

服务记录和服务列表提供任播服务，如命名查找和 DHT 引导。

### 目标

类型编号用于 I2NP 数据库查找/存储消息中。

end-to-end 列指的是查询/响应是否在 Garlic Message 中发送到目标地址。

现有类型：

| NetDB Data | Lookup Type | Store Type |
|------------|-------------|------------|
| any        | 0           | any        |
| LS         | 1           | 1          |
| RI         | 2           | 0          |
| exploratory| 3           | DSRM       |
新类型：

| NetDB Data     | Lookup Type | Store Type | Std. LS2 Header? | Sent end-to-end? |
|----------------|-------------|------------|------------------|------------------|
| LS2            | 1           | 3          | yes              | yes              |
| Encrypted LS2  | 1           | 5          | no               | no               |
| Meta LS2       | 1           | 7          | yes              | no               |
| Service Record | n/a         | 9          | yes              | no               |
| Service List   | 4           | 11         | no               | no               |
### 非目标 / 超出范围

- 查找类型目前是数据库查找消息中的第 3-2 位。
  任何额外的类型都需要使用第 4 位。

- 所有存储类型都是奇数，因为数据库存储消息类型字段中的高位会被旧的router忽略。
  我们宁愿解析失败时被识别为LS而不是压缩的RI。

- 签名覆盖的数据中，类型应该是显式的、隐式的，还是两者都不是？

### 理由说明

类型 3、5 和 7 可能作为标准 leaseSet 查找（类型 1）的响应返回。类型 9 永远不会作为查找的响应返回。类型 11 作为新服务查找类型（类型 11）的响应返回。

只有类型 3 可以在客户端到客户端的 Garlic 消息中发送。

### NetDB 数据类型

类型 3、7 和 9 都具有相同的格式：

标准 LS2 头部 - 如下所定义

类型特定部分 - 如下文各部分中定义

标准 LS2 签名：   - 长度由签名密钥的签名类型隐含确定

类型 5（加密）不以 Destination 开头，具有不同的格式。见下文。

类型 11（服务列表）是多个服务记录的聚合，具有不同的格式。请参见下文。

### 注意事项

待定

## Standard LS2 Header

类型 3、7 和 9 使用标准的 LS2 头部，具体规范如下：

### 查找/存储过程

```
Standard LS2 Header:
  - Type (1 byte)
    Not actually in header, but part of data covered by signature.
    Take from field in Database Store Message.
  - Destination (387+ bytes)
  - Published timestamp (4 bytes, big endian, seconds since epoch, rolls over in 2106)
  - Expires (2 bytes, big endian) (offset from published timestamp in seconds, 18.2 hours max)
  - Flags (2 bytes)
    Bit order: 15 14 ... 3 2 1 0
    Bit 0: If 0, no offline keys; if 1, offline keys
    Bit 1: If 0, a standard published leaseset.
           If 1, an unpublished leaseset. Should not be flooded, published, or
           sent in response to a query. If this leaseset expires, do not query the
           netdb for a new one, unless bit 2 is set.
    Bit 2: If 0, a standard published leaseset.
           If 1, this unencrypted leaseset will be blinded and encrypted when published.
           If this leaseset expires, query the blinded location in the netdb for a new one.
           If this bit is set to 1, set bit 1 to 1 also.
           As of release 0.9.42.
    Bits 3-15: set to 0 for compatibility with future uses
  - If flag indicates offline keys, the offline signature section:
    Expires timestamp (4 bytes, big endian, seconds since epoch, rolls over in 2106)
    Transient sig type (2 bytes, big endian)
    Transient signing public key (length as implied by sig type)
    Signature of expires timestamp, transient sig type, and public key,
    by the destination public key,
    length as implied by destination public key sig type.
    This section can, and should, be generated offline.
```
### 格式

- Unpublished/published: 用于端到端发送数据库存储时，发送router可能希望指示此leaseSet不应发送给其他节点。我们目前使用启发式方法来维护此状态。

- Published: 替换了确定 leaseset "版本"所需的复杂逻辑。目前，版本是最晚过期的 lease 的过期时间，当发布路由器发布仅删除旧 lease 的 leaseset 时，必须将该过期时间至少增加 1 毫秒。

- Expires: 允许 netdb 条目的过期时间早于其最后过期的 leaseSet。对于 LS2 可能不太有用，因为 leaseSet 预期保持最多 11 分钟的过期时间，但对于其他新类型则是必要的（参见下面的 Meta LS 和 Service Record）。

- 离线密钥是可选的，用于降低初始/必需的实现复杂性。

### 隐私/安全考虑

- 可以进一步降低时间戳精度（10分钟？），但需要添加版本号。这可能会破坏多宿主功能，除非我们有保序加密？可能无法完全去除时间戳。

- Alternative: 3字节时间戳（纪元时间 / 10分钟），1字节版本，2字节过期时间

- 数据/签名中的类型是显式的还是隐式的？签名的"域"常量？

### Notes

- Router 不应该每秒发布超过一次 LS。
  如果这样做，它们必须人为地将发布的时间戳比之前发布的 LS 增加 1。

- Router 实现可以缓存临时密钥和签名以避免每次都进行验证。特别是 floodfill 和长期连接两端的 router 可以从中受益。

- 离线密钥和签名仅适用于长期存在的目标节点，
  即服务器，而非客户端。

## New DatabaseEntry types

### 格式

与现有 LeaseSet 的变更：

- 添加发布时间戳、过期时间戳、标志和属性
- 添加加密类型
- 移除撤销密钥

查询使用

    Standard LS flag (1)
存储于

    Standard LS2 type (3)
存储于

    Hash of destination
    This hash is then used to generate the daily "routing key", as in LS1
典型过期时间

    10 minutes, as in a regular LS.
发布者

    Destination

### 理由说明

```
Standard LS2 Header as specified above

  Standard LS2 Type-Specific Part
  - Properties (Mapping as specified in common structures spec, 2 zero bytes if none)
  - Number of key sections to follow (1 byte, max TBD)
  - Key sections:
    - Encryption type (2 bytes, big endian)
    - Encryption key length (2 bytes, big endian)
      This is explicit, so floodfills can parse LS2 with unknown encryption types.
    - Encryption key (number of bytes specified)
  - Number of lease2s (1 byte)
  - Lease2s (40 bytes each)
    These are leases, but with a 4-byte instead of an 8-byte expiration,
    seconds since the epoch (rolls over in 2106)

  Standard LS2 Signature:
  - Signature
    If flag indicates offline keys, this is signed by the transient pubkey,
    otherwise, by the destination pubkey
    Length as implied by sig type of signing key
    The signature is of everything above.
```
### 问题

- Properties: 未来扩展和灵活性。
  放在首位以便在必要时解析其余数据。

- 多种加密类型/公钥对是为了
  便于向新加密类型过渡。另一种方法是
  发布多个 leaseSet，可能使用相同的隧道，
  就像我们现在对 DSA 和 EdDSA 目标所做的那样。
  在隧道上识别传入的加密类型
  可以通过现有的会话标签机制完成，
  和/或使用每个密钥进行试验解密。传入
  消息的长度也可能提供线索。

### 注意事项

本提案继续使用 leaseset 中的公钥作为端到端加密密钥，并保持 Destination 中的公钥字段未使用，与当前状态一致。加密类型在 Destination 密钥证书中未指定，将保持为 0。

一个被否决的替代方案是在 Destination 密钥证书中指定加密类型，使用 Destination 中的公钥，而不使用 leaseset 中的公钥。我们不打算采用这种方案。

LS2的优势：

- 实际公钥的位置不会改变。
- 加密类型或公钥可能会改变，而不会改变 Destination。
- 移除未使用的吊销字段
- 与本提案中其他 DatabaseEntry 类型的基本兼容性
- 允许多种加密类型

LS2 的缺点：

- 公钥位置和加密类型与 RouterInfo 不同
- 在 leaseset 中维护未使用的公钥
- 需要在整个网络中实现；或者，如果 floodfill 允许的话，可以使用实验性加密类型
  （但请参见相关提案 136 和 137 关于对实验性签名类型支持的内容）。
  替代提案对于实验性加密类型可能更容易实现和测试。

### New Encryption Issues

其中一些内容超出了本提案的范围，但暂时在此记录这些注释，因为我们还没有单独的加密提案。另请参阅 ECIES 提案 144 和 145。

- 加密类型代表曲线、密钥长度和端到端方案的组合，
  包括 KDF 和 MAC（如果有的话）。

- 我们包含了密钥长度字段，这样即使对于未知的加密类型，floodfill 也能解析和验证 LS2。

- 第一个提议的新加密类型可能是 ECIES/X25519。它如何在端到端使用
  （要么是 ElGamal/AES+SessionTag 的轻微修改版本，
  要么是全新的方案，例如 ChaCha/Poly）将在一个或多个
  单独的提案中指定。
  另请参阅 ECIES 提案 144 和 145。

### LeaseSet 2

- 租约中的8字节过期时间更改为4字节。

- 如果我们实施撤销功能，可以通过将过期字段设置为零，或零 leases，或两者结合来实现。无需单独的撤销密钥。

- 加密密钥按服务器偏好顺序排列，最优选的在前。
  默认客户端行为是选择第一个支持的加密类型的密钥。客户端可能会基于
  加密支持、相对性能和其他因素使用其他选择算法。

### 格式

目标：

- 添加盲化
- 允许多种签名类型
- 不需要任何新的加密原语
- 可选择对每个接收者加密，可撤销
- 仅支持 Standard LS2 和 Meta LS2 的加密

加密的 LS2 绝不会在端到端 garlic 消息中发送。请使用上述标准 LS2。

与现有加密 LeaseSet 的变更：

- 为安全起见加密整个内容
- 安全加密，不仅仅使用 AES
- 对每个接收者进行加密

查找通过

    Standard LS flag (1)
存储于

    Encrypted LS2 type (5)
存储在

    Hash of blinded sig type and blinded public key
    Two byte sig type (big endian, e.g. 0x000b) || blinded public key
    This hash is then used to generate the daily "routing key", as in LS1
典型过期时间

    10 minutes, as in a regular LS, or hours, as in a meta LS.
发布者

    Destination

### 理由说明

我们定义以下函数，对应于用于加密 LS2 的密码学构建块：

CSRNG(n)

    n-byte output from a cryptographically-secure random number generator.

    In addition to the requirement of CSRNG being cryptographically-secure (and thus
    suitable for generating key material), it MUST be safe
    for some n-byte output to be used for key material when the byte sequences immediately
    preceding and following it are exposed on the network (such as in a salt, or encrypted
    padding). Implementations that rely on a potentially-untrustworthy source should hash
    any output that is to be exposed on the network. See [PRNG references](http://projectbullrun.org/dual-ec/ext-rand.html) and [Tor dev discussion](https://lists.torproject.org/pipermail/tor-dev/2015-November/009954.html).

H(p, d)

    SHA-256 hash function that takes a personalization string p and data d, and
    produces an output of length 32 bytes.

    Use SHA-256 as follows::

        H(p, d) := SHA-256(p || d)

STREAM

    The ChaCha20 stream cipher as specified in [RFC 7539 Section 2.4](https://tools.ietf.org/html/rfc7539#section-2.4), with the initial counter
    set to 1. S_KEY_LEN = 32 and S_IV_LEN = 12.

    ENCRYPT(k, iv, plaintext)
        Encrypts plaintext using the cipher key k, and nonce iv which MUST be unique for
        the key k. Returns a ciphertext that is the same size as the plaintext.

        The entire ciphertext must be indistinguishable from random if the key is secret.

    DECRYPT(k, iv, ciphertext)
        Decrypts ciphertext using the cipher key k, and nonce iv. Returns the plaintext.

SIG

    The RedDSA signature scheme (corresponding to SigType 11) with key blinding.
    It has the following functions:

    DERIVE_PUBLIC(privkey)
        Returns the public key corresponding to the given private key.

    SIGN(privkey, m)
        Returns a signature by the private key privkey over the given message m.

    VERIFY(pubkey, m, sig)
        Verifies the signature sig against the public key pubkey and message m. Returns
        true if the signature is valid, false otherwise.

    It must also support the following key blinding operations:

    GENERATE_ALPHA(data, secret)
        Generate alpha for those who know the data and an optional secret.
        The result must be identically distributed as the private keys.

    BLIND_PRIVKEY(privkey, alpha)
        Blinds a private key, using a secret alpha.

    BLIND_PUBKEY(pubkey, alpha)
        Blinds a public key, using a secret alpha.
        For a given keypair (privkey, pubkey) the following relationship holds::

            BLIND_PUBKEY(pubkey, alpha) ==
            DERIVE_PUBLIC(BLIND_PRIVKEY(privkey, alpha))

DH

    X25519 public key agreement system. Private keys of 32 bytes, public keys of 32
    bytes, produces outputs of 32 bytes. It has the following
    functions:

    GENERATE_PRIVATE()
        Generates a new private key.

    DERIVE_PUBLIC(privkey)
        Returns the public key corresponding to the given private key.

    DH(privkey, pubkey)
        Generates a shared secret from the given private and public keys.

HKDF(salt, ikm, info, n)

    A cryptographic key derivation function which takes some input key material ikm (which
    should have good entropy but is not required to be a uniformly random string), a salt
    of length 32 bytes, and a context-specific 'info' value, and produces an output
    of n bytes suitable for use as key material.

    Use HKDF as specified in [RFC 5869](https://tools.ietf.org/html/rfc5869), using the HMAC hash function SHA-256
    as specified in [RFC 2104](https://tools.ietf.org/html/rfc2104). This means that SALT_LEN is 32 bytes max.

### 讨论

加密的 LS2 格式由三个嵌套层组成：

- 包含存储和检索所需明文信息的外层。
- 处理客户端身份验证的中间层。
- 包含实际 LS2 数据的内层。

整体格式如下::

    Layer 0 data + Enc(layer 1 data + Enc(layer 2 data)) + Signature

注意加密的 LS2 是经过盲化的。Destination 不在头部中。DHT 存储位置是 SHA-256(sig type || blinded public key)，并且每天轮换。

不使用上述指定的标准 LS2 header。

#### Layer 0 (outer)

类型

    1 byte

    Not actually in header, but part of data covered by signature.
    Take from field in Database Store Message.

盲化公钥签名类型

    2 bytes, big endian
    This will always be type 11, identifying a Red25519 blinded key.

盲化公钥

    Length as implied by sig type

发布时间戳

    4 bytes, big endian

    Seconds since epoch, rolls over in 2106

过期时间

    2 bytes, big endian

    Offset from published timestamp in seconds, 18.2 hours max

标志

    2 bytes

    Bit order: 15 14 ... 3 2 1 0

    Bit 0: If 0, no offline keys; if 1, offline keys

    Other bits: set to 0 for compatibility with future uses

临时密钥数据

    Present if flag indicates offline keys

    Expires timestamp
        4 bytes, big endian

        Seconds since epoch, rolls over in 2106

    Transient sig type
        2 bytes, big endian

    Transient signing public key
        Length as implied by sig type

    Signature
        Length as implied by blinded public key sig type

        Over expires timestamp, transient sig type, and transient public key.

        Verified with the blinded public key.

lenOuterCiphertext

    2 bytes, big endian

outerCiphertext

    lenOuterCiphertext bytes

    Encrypted layer 1 data. See below for key derivation and encryption algorithms.

签名

    Length as implied by sig type of the signing key used

    The signature is of everything above.

    If the flag indicates offline keys, the signature is verified with the transient
    public key. Otherwise, the signature is verified with the blinded public key.

#### Layer 1 (middle)

标志

    1 byte
    
    Bit order: 76543210

    Bit 0: 0 for everybody, 1 for per-client, auth section to follow

    Bits 3-1: Authentication scheme, only if bit 0 is set to 1 for per-client, otherwise 000
              000: DH client authentication (or no per-client authentication)
              001: PSK client authentication

    Bits 7-4: Unused, set to 0 for future compatibility

DH 客户端认证数据

    Present if flag bit 0 is set to 1 and flag bits 3-1 are set to 000.

    ephemeralPublicKey
        32 bytes

    clients
        2 bytes, big endian

        Number of authClient entries to follow, 40 bytes each

    authClient
        Authorization data for a single client.
        See below for the per-client authorization algorithm.

        clientID_i
            8 bytes

        clientCookie_i
            32 bytes

PSK 客户端认证数据

    Present if flag bit 0 is set to 1 and flag bits 3-1 are set to 001.

    authSalt
        32 bytes

    clients
        2 bytes, big endian

        Number of authClient entries to follow, 40 bytes each

    authClient
        Authorization data for a single client.
        See below for the per-client authorization algorithm.

        clientID_i
            8 bytes

        clientCookie_i
            32 bytes

innerCiphertext

    Length implied by lenOuterCiphertext (whatever data remains)

    Encrypted layer 2 data. See below for key derivation and encryption algorithms.

#### Layer 2 (inner)

类型

    1 byte

    Either 3 (LS2) or 7 (Meta LS2)

数据

    LeaseSet2 data for the given type.

    Includes the header and signature.

### 新的加密问题

我们使用以下基于 Ed25519 和 [ZCash RedDSA](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf) 的密钥盲化方案。Re25519 签名基于 Ed25519 曲线，使用 SHA-512 作为哈希函数。

我们不使用 [Tor's rend-spec-v3.txt appendix A.2](https://spec.torproject.org/rend-spec-v3)，虽然它有相似的设计目标，但是其盲化公钥可能偏离素数阶子群，存在未知的安全隐患。

#### Goals

- 未混淆目标中的签名公钥必须是
  Ed25519 (sig type 7) 或 Red25519 (sig type 11)；
  不支持其他签名类型
- 如果签名公钥是离线的，瞬态签名公钥也必须是 Ed25519
- 混淆在计算上是简单的
- 使用现有的密码学原语
- 混淆的公钥无法被去混淆
- 混淆的公钥必须在 Ed25519 曲线和素数阶子群上
- 必须知道目标的签名公钥
  (不需要完整的目标) 才能派生混淆的公钥
- 可选择提供派生混淆公钥所需的额外密钥

#### Security

盲化方案的安全性要求 alpha 的分布与未盲化私钥的分布相同。然而，当我们将 Ed25519 私钥（sig type 7）盲化为 Red25519 私钥（sig type 11）时，分布是不同的。为了满足 [zcash section 4.1.6.1](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf) 的要求，Red25519（sig type 11）也应该用于未盲化密钥，以确保"重新随机化公钥与该密钥下签名的组合不会泄露其重新随机化来源的密钥。"我们允许现有目标使用 type 7，但建议将要加密的新目标使用 type 11。

#### Definitions

B

    The Ed25519 base point (generator) 2^255 - 19 as in [Ed25519](http://cr.yp.to/papers.html#ed25519)

L

    The Ed25519 order 2^252 + 27742317777372353535851937790883648493
    as in [Ed25519](http://cr.yp.to/papers.html#ed25519)

DERIVE_PUBLIC(a)

    Convert a private key to public, as in Ed25519 (mulitply by G)

alpha

    A 32-byte random number known to those who know the destination.

GENERATE_ALPHA(destination, date, secret)

    Generate alpha for the current date, for those who know the destination and the secret.
    The result must be identically distributed as Ed25519 private keys.

a

    The unblinded 32-byte EdDSA or RedDSA signing private key used to sign the destination

A

    The unblinded 32-byte EdDSA or RedDSA signing public key in the destination,
    = DERIVE_PUBLIC(a), as in Ed25519

a'

    The blinded 32-byte EdDSA signing private key used to sign the encrypted leaseset
    This is a valid EdDSA private key.

A'

    The blinded 32-byte EdDSA signing public key in the Destination,
    may be generated with DERIVE_PUBLIC(a'), or from A and alpha.
    This is a valid EdDSA public key, on the curve and on the prime-order subgroup.

LEOS2IP(x)

    Flip the order of the input bytes to little-endian

H*(x)

    32 bytes = (LEOS2IP(SHA512(x))) mod B, same as in Ed25519 hash-and-reduce

#### Blinding Calculations

每天（UTC时间）都必须生成新的秘密alpha和盲化密钥。秘密alpha和盲化密钥的计算方法如下。

为所有参与方生成GENERATE_ALPHA(destination, date, secret)：

```text
// GENERATE_ALPHA(destination, date, secret)

  // secret is optional, else zero-length
  A = destination's signing public key
  stA = signature type of A, 2 bytes big endian (0x0007 or 0x000b)
  stA' = signature type of blinded public key A', 2 bytes big endian (0x000b)
  keydata = A || stA || stA'
  datestring = 8 bytes ASCII YYYYMMDD from the current date UTC
  secret = UTF-8 encoded string
  seed = HKDF(H("I2PGenerateAlpha", keydata), datestring || secret, "i2pblinding1", 64)
  // treat seed as a 64 byte little-endian value
  alpha = seed mod L
```
BLIND_PRIVKEY()，用于发布 leaseset 的所有者：

```text
// BLIND_PRIVKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  // If for a Ed25519 private key (type 7)
  seed = destination's signing private key
  a = left half of SHA512(seed) and clamped as usual for Ed25519
  // else, for a Red25519 private key (type 11)
  a = destination's signing private key
  // Addition using scalar arithmentic
  blinded signing private key = a' = BLIND_PRIVKEY(a, alpha) = (a + alpha) mod L
  blinded signing public key = A' = DERIVE_PUBLIC(a')
```
BLIND_PUBKEY()，用于客户端检索租约集合(leaseset)：

```text
// BLIND_PUBKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  A = destination's signing public key
  // Addition using group elements (points on the curve)
  blinded public key = A' = BLIND_PUBKEY(A, alpha) = A + DERIVE_PUBLIC(alpha)
```
计算 A' 的两种方法产生相同的结果，这是必需的。

#### Signing

未盲化的 leaseset 由未盲化的 Ed25519 或 Red25519 签名私钥进行签名，并使用未盲化的 Ed25519 或 Red25519 签名公钥（签名类型 7 或 11）按常规方式进行验证。

如果签名公钥离线，未盲化的 leaseset 由未盲化的临时 Ed25519 或 Red25519 签名私钥签名，并使用未盲化的 Ed25519 或 Red25519 临时签名公钥（签名类型 7 或 11）进行常规验证。有关加密 leaseset 的离线密钥的其他说明，请参见下文。

对于加密后的 leaseset 的签名，我们使用 Red25519，基于 [RedDSA](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf) 来使用盲化密钥进行签名和验证。Red25519 签名基于 Ed25519 曲线，使用 SHA-512 作为哈希函数。

Red25519 与标准 Ed25519 完全相同，除了以下指定的差异。

#### Sign/Verify Calculations

加密 leaseset 的外层部分使用 Red25519 密钥和签名。

Red25519几乎与Ed25519完全相同。有两个区别：

Red25519私钥由随机数生成，然后必须对L取模进行约简，其中L在上文中已定义。Ed25519私钥由随机数生成，然后使用位掩码对第0字节和第31字节进行"钳制"操作。Red25519不执行此操作。上文定义的函数GENERATE_ALPHA()和BLIND_PRIVKEY()使用mod L生成合适的Red25519私钥。

在 Red25519 中，签名时 r 的计算使用了额外的随机数据，并使用公钥值而不是私钥的哈希值。由于随机数据的存在，每个 Red25519 签名都是不同的，即使使用相同的密钥对相同的数据进行签名也是如此。

签名：

```text
T = 80 random bytes
  r = H*(T || publickey || message)
  // rest is the same as in Ed25519
```
验证：

```text
// same as in Ed25519
```
### 注释

#### Derivation of subcredentials

作为盲化过程的一部分，我们需要确保加密的 LS2 只能被知道相应 Destination 签名公钥的人解密。不需要完整的 Destination。为了实现这一点，我们从签名公钥派生出一个凭证：

```text
A = destination's signing public key
  stA = signature type of A, 2 bytes big endian (0x0007 or 0x000b)
  stA' = signature type of A', 2 bytes big endian (0x000b)
  keydata = A || stA || stA'
  credential = H("credential", keydata)
```
个性化字符串确保凭证不会与任何用作 DHT 查找键的哈希发生冲突，例如纯粹的 Destination 哈希。

对于给定的盲化密钥，我们可以推导出一个子凭证：

```text
subcredential = H("subcredential", credential || blindedPublicKey)
```
subcredential 包含在下面的密钥派生过程中，这将这些密钥与对目标地址签名公钥的了解绑定在一起。

#### Layer 1 encryption

首先，准备密钥派生过程的输入：

```text
outerInput = subcredential || publishedTimestamp
```
接下来，生成一个随机盐值：

```text
outerSalt = CSRNG(32)
```
然后推导出用于加密第1层的密钥：

```text
keys = HKDF(outerSalt, outerInput, "ELS2_L1K", 44)
  outerKey = keys[0:31]
  outerIV = keys[32:43]
```
最后，第1层明文被加密并序列化：

```text
outerCiphertext = outerSalt || ENCRYPT(outerKey, outerIV, outerPlaintext)
```
#### Layer 1 decryption

盐值是从第1层密文中解析得到的：

```text
outerSalt = outerCiphertext[0:31]
```
然后推导出用于加密第1层的密钥：

```text
outerInput = subcredential || publishedTimestamp
  keys = HKDF(outerSalt, outerInput, "ELS2_L1K", 44)
  outerKey = keys[0:31]
  outerIV = keys[32:43]
```
最后，第1层密文被解密：

```text
outerPlaintext = DECRYPT(outerKey, outerIV, outerCiphertext[32:end])
```
#### Layer 2 encryption

当启用客户端授权时，``authCookie`` 按照下述方式计算。当禁用客户端授权时，``authCookie`` 是零长度字节数组。

加密过程与第1层类似：

```text
innerInput = authCookie || subcredential || publishedTimestamp
  innerSalt = CSRNG(32)
  keys = HKDF(innerSalt, innerInput, "ELS2_L2K", 44)
  innerKey = keys[0:31]
  innerIV = keys[32:43]
  innerCiphertext = innerSalt || ENCRYPT(innerKey, innerIV, innerPlaintext)
```
#### Layer 2 decryption

当客户端授权启用时，``authCookie`` 按照下面描述的方式计算。当客户端授权禁用时，``authCookie`` 是零长度字节数组。

解密过程与第1层类似：

```text
innerInput = authCookie || subcredential || publishedTimestamp
  innerSalt = innerCiphertext[0:31]
  keys = HKDF(innerSalt, innerInput, "ELS2_L2K", 44)
  innerKey = keys[0:31]
  innerIV = keys[32:43]
  innerPlaintext = DECRYPT(innerKey, innerIV, innerCiphertext[32:end])
```
### 加密的 LS2

当为 Destination 启用客户端授权时，服务器维护一个客户端列表，这些客户端被授权解密加密的 LS2 数据。每个客户端存储的数据取决于授权机制，包括每个客户端生成并通过安全的带外机制发送给服务器的某种形式的密钥材料。

有两种实现按客户端授权的替代方案：

#### DH client authorization

每个客户端生成一个 DH 密钥对 ``[csk_i, cpk_i]``，并将公钥 ``cpk_i`` 发送到服务器。

服务器处理
^^^^^^^^^^^^^^^^^

服务器生成一个新的 ``authCookie`` 和一个临时的 DH 密钥对：

```text
authCookie = CSRNG(32)
  esk = GENERATE_PRIVATE()
  epk = DERIVE_PUBLIC(esk)
```
然后对于每个授权客户端，服务器使用其公钥加密 ``authCookie``：

```text
sharedSecret = DH(esk, cpk_i)
  authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
  okm = HKDF(epk, authInput, "ELS2_XCA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
  clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
```
服务器将每个 ``[clientID_i, clientCookie_i]`` 元组连同 ``epk`` 一起放入加密 LS2 的第 1 层中。

客户端处理
^^^^^^^^^^^^^^^^^

客户端使用其私钥来推导出预期的客户端标识符 ``clientID_i``、加密密钥 ``clientKey_i`` 和加密初始化向量 ``clientIV_i``：

```text
sharedSecret = DH(csk_i, epk)
  authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
  okm = HKDF(epk, authInput, "ELS2_XCA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
```
然后客户端在第1层授权数据中搜索包含 ``clientID_i`` 的条目。如果存在匹配的条目，客户端对其进行解密以获取 ``authCookie``：

```text
authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie_i)
```
#### Pre-shared key client authorization

每个客户端生成一个32字节的密钥``psk_i``，并将其发送给服务器。或者，服务器可以生成密钥，并将其发送给一个或多个客户端。

服务器处理
^^^^^^^^^^^^^^^^^

服务器生成新的 ``authCookie`` 和盐值：

```text
authCookie = CSRNG(32)
  authSalt = CSRNG(32)
```
然后对于每个已授权的客户端，服务器使用其预共享密钥加密 ``authCookie``：

```text
authInput = psk_i || subcredential || publishedTimestamp
  okm = HKDF(authSalt, authInput, "ELS2PSKA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
  clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
```
服务器将每个 ``[clientID_i, clientCookie_i]`` 元组与 ``authSalt`` 一起放入加密 LS2 的第 1 层中。

客户端处理
^^^^^^^^^^^^^^^^^

客户端使用其预共享密钥来派生其预期的客户端标识符 ``clientID_i``、加密密钥 ``clientKey_i`` 和加密初始化向量 ``clientIV_i``：

```text
authInput = psk_i || subcredential || publishedTimestamp
  okm = HKDF(authSalt, authInput, "ELS2PSKA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
```
然后客户端在第1层授权数据中搜索包含 ``clientID_i`` 的条目。如果存在匹配的条目，客户端对其进行解密以获取 ``authCookie``：

```text
authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie_i)
```
#### Security considerations

上述两种客户端授权机制都为客户端成员身份提供了隐私保护。仅知道 Destination 的实体可以看到任何时候有多少客户端订阅，但无法追踪哪些客户端被添加或撤销。

服务器应该在每次生成加密的 LS2 时随机化客户端的顺序，以防止客户端了解自己在列表中的位置并推断出其他客户端何时被添加或撤销。

服务器可以选择通过在授权数据列表中插入随机条目来隐藏订阅的客户端数量。

DH 客户端授权的优势
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- 该方案的安全性并不完全依赖于客户端密钥材料的带外交换。客户端的私钥永远不需要离开其设备，因此能够拦截带外交换但无法破解 DH 算法的攻击者，既无法解密加密的 LS2，也无法确定客户端被授予访问权限的时长。

DH 客户端授权的缺点
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- 服务器端需要为 N 个客户端执行 N + 1 次 DH 运算。
- 客户端需要执行一次 DH 运算。
- 需要客户端生成密钥。

PSK客户端授权的优势
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- 不需要DH运算。
- 允许服务器生成密钥。
- 如果需要，允许服务器与多个客户端共享同一密钥。

PSK客户端授权的缺点
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- 该方案的安全性严重依赖于客户端密钥材料的带外交换。拦截特定客户端交换的攻击者可以解密该客户端被授权访问的任何后续加密LS2，并且能够确定客户端访问权限何时被撤销。

### 定义

参见提案 149。

你不能将加密的 LS2 用于 bittorrent，因为紧凑宣告回复只有 32 字节。这 32 字节只包含哈希值。没有空间来指示 leaseSet 是否加密，或签名类型。

### 格式

对于使用离线密钥的加密 leaseSet，盲化私钥也必须离线生成，每天生成一个。

由于可选的离线签名块位于加密 leaseSet 的明文部分，任何抓取 floodfill 的人都可以使用它来跟踪 leaseSet（但无法解密）数天时间。为了防止这种情况，密钥所有者也应该每天生成新的临时密钥。临时密钥和盲化密钥都可以提前生成，并批量交付给 router。

本提案中没有定义用于打包多个临时密钥和盲化密钥并将其提供给客户端或路由器的文件格式。本提案中也没有定义用于支持带有离线密钥的加密 leaseSet 的 I2CP 协议增强。

### Notes

- 使用加密 leaseSet 的服务会将加密版本发布到 floodfill 节点。但是，为了提高效率，一旦通过身份验证（例如通过白名单），它会在包装的 garlic 消息中向客户端发送未加密的 leaseSet。

- Floodfill 可能会将最大大小限制在合理值以防止滥用。

- 解密后，应该进行几项检查，包括确认内部时间戳和过期时间与顶层的匹配。

- ChaCha20 被选择而不是 AES。虽然在有 AES 硬件支持时速度相似，但当没有 AES 硬件支持时（如在低端 ARM 设备上），ChaCha20 的速度要快 2.5-3 倍。

- 我们不够关心速度问题，因此不使用带密钥的 BLAKE2b。它的输出大小足以容纳我们所需的最大 n 值（或者我们可以使用计数器参数为每个所需密钥调用一次）。BLAKE2b 比 SHA-256 快得多，带密钥的 BLAKE2b 会减少哈希函数调用的总次数。
  然而，请参阅提案 148，其中建议我们出于其他原因切换到 BLAKE2b。
  参见 [Secure key derivation performance](https://www.lvh.io/posts/secure-key-derivation-performance.html)。

### Meta LS2

这用于替代多宿主连接。与任何 leaseSet 一样，这由创建者签名。这是一个经过身份验证的目标哈希列表。

Meta LS2 是树形结构的顶层节点，可能也是中间节点。它包含多个条目，每个条目指向一个 LS、LS2 或另一个 Meta LS2，以支持大规模多宿主。Meta LS2 可能包含 LS、LS2 和 Meta LS2 条目的混合。树的叶子节点始终是 LS 或 LS2。该树是一个 DAG（有向无环图）；禁止出现循环；执行查找的客户端必须检测并拒绝跟随循环。

Meta LS2 的过期时间可能比标准 LS 或 LS2 长得多。顶级层可能在发布日期后几小时才过期。最大过期时间将由 floodfill 和客户端强制执行，具体时间待定。

Meta LS2的使用场景是大规模多宿主，但在关联路由器与leaseSet（在路由器重启时）方面，其保护程度不会超过当前LS或LS2所提供的保护。这相当于"facebook"使用场景，可能不需要关联保护。这种使用场景可能需要离线密钥，这些密钥在树的每个节点的标准头部中提供。

叶子路由器、中间节点和主Meta LS签名者之间协调的后端协议在此处未作规定。要求极其简单——只需验证对等节点是否在线，并每隔几小时发布一个新的LS。唯一的复杂性在于当故障发生时为顶级或中间级Meta LSes选择新的发布者。

混合匹配 leaseset（将来自多个 router 的 lease 组合、签名并在单个 leaseset 中发布）在提案 140"隐形多归属"中有记录。该提案按现有方式编写是站不住脚的，因为流连接不会"粘性"绑定到单个 router，参见 http://zzz.i2p/topics/2335 。

后端协议以及与路由器和客户端内部的交互，对于隐形多宿主来说会相当复杂。

为避免顶级 Meta LS 的 floodfill 过载，过期时间应至少设置为几个小时。客户端必须缓存顶级 Meta LS，并在重启时持久化未过期的数据。

我们需要为客户端定义一些遍历树的算法，包括回退机制，以便使用分散化。某些基于哈希距离、成本和随机性的函数。如果一个节点同时拥有 LS 或 LS2 和 Meta LS，我们需要知道何时允许使用这些 leaseSet，何时继续遍历树。

查找使用

    Standard LS flag (1)
存储于

    Meta LS2 type (7)
存储于

    Hash of destination
    This hash is then used to generate the daily "routing key", as in LS1
典型过期时间

    Hours. Max 18.2 hours (65535 seconds)
发布者

    "master" Destination or coordinator, or intermediate coordinators

### Format

```
Standard LS2 Header as specified above

  Meta LS2 Type-Specific Part
  - Properties (Mapping as specified in common structures spec, 2 zero bytes if none)
  - Number of entries (1 byte) Maximum TBD
  - Entries. Each entry contains: (40 bytes)
    - Hash (32 bytes)
    - Flags (2 bytes)
      TBD. Set all to zero for compatibility with future uses.
    - Type (1 byte) The type of LS it is referencing;
      1 for LS, 3 for LS2, 5 for encrypted, 7 for meta, 0 for unknown.
    - Cost (priority) (1 byte)
    - Expires (4 bytes) (4 bytes, big endian, seconds since epoch, rolls over in 2106)
  - Number of revocations (1 byte) Maximum TBD
  - Revocations: Each revocation contains: (32 bytes)
    - Hash (32 bytes)

  Standard LS2 Signature:
  - Signature (40+ bytes)
    The signature is of everything above.
```
标志和属性：供将来使用

### 盲化密钥推导

- 使用此功能的分布式服务将拥有一个或多个具有服务目标私钥的"主节点"。它们会（通过带外方式）确定当前活跃目标的列表并发布 Meta LS2。为了冗余，多个主节点可以进行多宿主（即并发发布）Meta LS2。

- 分布式服务可以从单个 destination 开始或使用旧式多宿主方式，然后过渡到 Meta LS2。标准的 LS 查找可能返回 LS、LS2 或 Meta LS2 中的任意一种。

- 当服务使用 Meta LS2 时，它没有隧道（leases）。

### Service Record

这是一个单独的记录，表明某个目标地址正在参与某项服务。它由参与者发送给floodfill节点。floodfill节点从不单独发送此记录，而只是将其作为服务列表的一部分发送。服务记录也可用于撤销对服务的参与，方法是将过期时间设置为零。

这不是一个 LS2，但它使用标准的 LS2 头部和签名格式。

查找使用

    n/a, see Service List
存储方式

    Service Record type (9)
存储于

    Hash of service name
    This hash is then used to generate the daily "routing key", as in LS1
典型过期时间

    Hours. Max 18.2 hours (65535 seconds)
发布者

    Destination

### Format

```
Standard LS2 Header as specified above

  Service Record Type-Specific Part
  - Port (2 bytes, big endian) (0 if unspecified)
  - Hash of service name (32 bytes)

  Standard LS2 Signature:
  - Signature (40+ bytes)
    The signature is of everything above.
```
### Notes

- 如果 expires 全为零，floodfill 应该撤销该记录，不再将其包含在服务列表中。

- 存储：floodfill 可能会严格限制这些记录的存储，并限制每个哈希存储的记录数量及其过期时间。也可以使用哈希白名单。

- 在相同哈希值处的任何其他 netDb 类型都具有优先级，因此服务记录永远不能覆盖 LS/RI，但 LS/RI 会覆盖该哈希值处的所有服务记录。

### Service List

这与 LS2 完全不同，使用的是不同的格式。

服务列表由 floodfill 创建并签名。它是未经认证的，这意味着任何人都可以通过向 floodfill 发布服务记录来加入服务。

Service List包含简短服务记录，而不是完整的服务记录。这些记录包含签名，但只包含哈希值而非完整的目标地址，因此在没有完整目标地址的情况下无法进行验证。

服务列表的安全性（如果有的话）和可取性尚待确定。Floodfill 可以将发布和查找限制在服务白名单内，但该白名单可能会根据实现或操作者偏好而有所不同。在不同实现之间就通用基础白名单达成共识可能是不可能的。

如果服务名称包含在上述服务记录中，那么 floodfill 运营者可能会提出异议；如果只包含哈希值，则没有验证，服务记录可能会"抢先"于任何其他 netdb 类型并存储在 floodfill 中。

查找使用

    Service List lookup type (11)
存储于

    Service List type (11)
存储于

    Hash of service name
    This hash is then used to generate the daily "routing key", as in LS1
典型到期时间

    Hours, not specified in the list itself, up to local policy
发布者

    Nobody, never sent to floodfill, never flooded.

### Format

不使用上述指定的标准 LS2 头部。

```
- Type (1 byte)
    Not actually in header, but part of data covered by signature.
    Take from field in Database Store Message.
  - Hash of the service name (implicit, in the Database Store message)
  - Hash of the Creator (floodfill) (32 bytes)
  - Published timestamp (8 bytes, big endian)

  - Number of Short Service Records (1 byte)
  - List of Short Service Records:
    Each Short Service Record contains (90+ bytes)
    - Dest hash (32 bytes)
    - Published timestamp (8 bytes, big endian)
    - Expires (4 bytes, big endian) (offset from published in ms)
    - Flags (2 bytes)
    - Port (2 bytes, big endian)
    - Sig length (2 bytes, big endian)
    - Signature of dest (40+ bytes)

  - Number of Revocation Records (1 byte)
  - List of Revocation Records:
    Each Revocation Record contains (86+ bytes)
    - Dest hash (32 bytes)
    - Published timestamp (8 bytes, big endian)
    - Flags (2 bytes)
    - Port (2 bytes, big endian)
    - Sig length (2 bytes, big endian)
    - Signature of dest (40+ bytes)

  - Signature of floodfill (40+ bytes)
    The signature is of everything above.
```
验证服务列表的签名：

- 在服务名称前添加哈希值
- 移除创建者的哈希值
- 检查修改内容的签名

验证每个短服务记录的签名：

- 获取目标地址
- 检查签名（发布时间戳 + 过期时间 + 标志位 + 端口 + 服务名称哈希值）

验证每个吊销记录的签名：

- 获取目标地址
- 检查签名（发布时间戳 + 4个零字节 + 标志位 + 端口 + 服务名称哈希值）

### Notes

- 我们使用签名长度而不是签名类型，这样我们就能支持未知的签名类型。

- 服务列表没有过期时间，接收者可以根据策略或单个记录的过期时间自行决定。

- Service Lists 不会被洪泛传播，只有单个 Service Records 会被洪泛传播。每个
  floodfill 创建、签名并缓存一个 Service List。floodfill 使用其
  自身的策略来决定缓存时间以及服务和撤销记录的最大数量。

## Common Structures Spec Changes Required

### 加密和处理

超出本提案的范围。添加到 ECIES 提案 144 和 145 中。

### New Intermediate Structures

为 Lease2、MetaLease、LeaseSet2Header 和 OfflineSignature 添加新结构。自版本 0.9.38 起生效。

### New NetDB Types

为每种新的 LeaseSet 类型添加结构，从上述内容中合并。对于 LeaseSet2、EncryptedLeaseSet 和 MetaLeaseSet，自 0.9.38 版本起生效。对于 Service Record 和 Service List，为初步和未计划的内容。

### New Signature Type

添加 RedDSA_SHA512_Ed25519 类型 11。公钥为 32 字节；私钥为 32 字节；哈希为 64 字节；签名为 64 字节。

## Encryption Spec Changes Required

超出本提案范围。请参阅提案 144 和 145。

## I2NP Changes Required

添加注意事项：LS2 只能发布到具有最低版本要求的 floodfill 节点。

### Database Lookup Message

添加服务列表查找类型。

### Changes

```
Flags byte: Lookup type field, currently bits 3-2, expands to bits 4-2.
  Lookup type 0x04 is defined as the service list lookup.

  Add note: Service list loookup may only be sent to floodfills with a minimum version.
  Minimum version is 0.9.38.
```
### 按客户端授权

添加所有新的存储类型。

### Changes

```
Type byte: Type field, currently bit 0, expands to bits 3-0.
  Type 3 is defined as a LS2 store.
  Type 5 is defined as a encrypted LS2 store.
  Type 7 is defined as a meta LS2 store.
  Type 9 is defined as a service record store.
  Type 11 is defined as a service list store.
  Other types are undefined and invalid.

  Add note: All new types may only be published to floodfills with a minimum version.
  Minimum version is 0.9.38.
```
## I2CP Changes Required

### I2CP Options

路由器端解释的新选项，在 SessionConfig Mapping 中发送：

```

  i2cp.leaseSetType=nnn       The type of leaseset to be sent in the Create Leaseset Message
                              Value is the same as the netdb store type in the table above.
                              Interpreted client-side, but also passed to the router in the
                              SessionConfig, to declare intent and check support.

  i2cp.leaseSetEncType=nnn[,nnn]  The encryption types to be used.
                                  Interpreted client-side, but also passed to the router in
                                  the SessionConfig, to declare intent and check support.
                                  See proposals 144 and 145.

  i2cp.leaseSetOfflineExpiration=nnn  The expiration of the offline signature, ASCII,
                                      seconds since the epoch.

  i2cp.leaseSetTransientPublicKey=[type:]b64  The base 64 of the transient private key,
                                              prefixed by an optional sig type number
                                              or name, default DSA_SHA1.
                                              Length as inferred from the sig type

  i2cp.leaseSetOfflineSignature=b64   The base 64 of the offline signature.
                                      Length as inferred from the destination
                                      signing public key type

  i2cp.leaseSetSecret=b64     The base 64 of a secret used to blind the
                              address of the leaseset, default ""

  i2cp.leaseSetAuthType=nnn   The type of authentication for encrypted LS2.
                              0 for no per-client authentication (the default)
                              1 for DH per-client authentication
                              2 for PSK per-client authentication

  i2cp.leaseSetPrivKey=b64    A base 64 private key for the router to use to
                              decrypt the encrypted LS2,
                              only if per-client authentication is enabled
```
客户端解释的新选项：

```

  i2cp.leaseSetType=nnn     The type of leaseset to be sent in the Create Leaseset Message
                            Value is the same as the netdb store type in the table above.
                            Interpreted client-side, but also passed to the router in the
                            SessionConfig, to declare intent and check support.

  i2cp.leaseSetEncType=nnn[,nnn]  The encryption types to be used.
                                  Interpreted client-side, but also passed to the router in
                                  the SessionConfig, to declare intent and check support.
                                  See proposals 144 and 145.

  i2cp.leaseSetSecret=b64     The base 64 of a secret used to blind the
                              address of the leaseset, default ""

  i2cp.leaseSetAuthType=nnn       The type of authentication for encrypted LS2.
                                  0 for no per-client authentication (the default)
                                  1 for DH per-client authentication
                                  2 for PSK per-client authentication

  i2cp.leaseSetBlindedType=nnn   The sig type of the blinded key for encrypted LS2.
                                 Default depends on the destination sig type.

  i2cp.leaseSetClient.dh.nnn=b64name:b64pubkey   The base 64 of the client name (ignored, UI use only),
                                                 followed by a ':', followed by the base 64 of the public
                                                 key to use for DH per-client auth. nnn starts with 0

  i2cp.leaseSetClient.psk.nnn=b64name:b64privkey   The base 64 of the client name (ignored, UI use only),
                                                   followed by a ':', followed by the base 64 of the private
                                                   key to use for PSK per-client auth. nnn starts with 0
```
### Session Config

请注意，对于离线签名，需要选项 i2cp.leaseSetOfflineExpiration、i2cp.leaseSetTransientPublicKey 和 i2cp.leaseSetOfflineSignature，并且签名是由临时签名私钥进行的。

### 加密 LS 与 Base 32 地址

Router 到客户端。无更改。租约(lease)使用 8 字节时间戳发送，即使返回的 leaseSet 是带有 4 字节时间戳的 LS2。请注意，响应可能是 Create Leaseset 或 Create Leaseset2 消息。

### 使用离线密钥的加密 LS

Router到客户端。无变化。租约使用8字节时间戳发送，即使返回的leaseSet将是带有4字节时间戳的LS2。请注意，响应可能是Create Leaseset或Create Leaseset2消息。

### 注意事项

客户端到路由器。新消息，用于替代创建 Leaseset 消息。

### Meta LS2

- 为了让路由器解析存储类型，该类型必须包含在消息中，
  除非它在会话配置中事先传递给路由器。
  对于通用解析代码，将其包含在消息本身中更容易。

- 为了让路由器知道私钥的类型和长度，
  它必须位于租约集（lease set）之后，除非解析器在会话配置中预先知道类型。
  对于通用解析代码来说，从消息本身获取这些信息更容易。

- 签名私钥，之前为撤销而定义但未使用，在 LS2 中不存在。

"Format

"

Could you please provide the actual text content that needs to be translated from English to Chinese?

Create Leaseset2 Message 的消息类型是 41。

### 注意事项

```
Session ID
  Type byte: Type of lease set to follow
             Type 1 is a LS
             Type 3 is a LS2
             Type 5 is a encrypted LS2
             Type 7 is a meta LS2
  LeaseSet: type specified above
  Number of private keys to follow (1 byte)
  Encryption Private Keys: For each public key in the lease set,
                           in the same order
                           (Not present for Meta LS2)
                           - Encryption type (2 bytes, big endian)
                           - Encryption key length (2 bytes, big endian)
                           - Encryption key (number of bytes specified)
```
### 服务记录

- 最低路由器版本为 0.9.39。
- 消息类型 40 的初步版本存在于 0.9.38 中，但格式已更改。
  类型 40 已被弃用且不受支持。

### 格式

- 需要更多更改来支持加密和元数据 LS。

### 注意事项

客户端到路由器。新消息。

### 服务列表

- 路由器需要知道目标是否为盲化状态。
  如果是盲化的并且使用密钥或每客户端身份验证，
  它也需要拥有该信息。

- 新格式 b32 地址（"b33"）的主机查找
  告知路由器该地址是盲化的，但在主机查找消息中没有机制
  将密钥或私钥传递给路由器。
  虽然我们可以扩展主机查找消息来添加这些信息，
  但定义一个新消息会更简洁。

- 我们需要一种程序化的方式让客户端告知 router。
  否则，用户必须手动配置每个目的地。

### 格式

在客户端向隐蔽目标发送消息之前，它必须在 Host Lookup 消息中查找"b33"，或者发送 Blinding Info 消息。如果隐蔽目标需要密钥或按客户端认证，客户端必须发送 Blinding Info 消息。

router不会对此消息发送回复。

### 注释

Blinding Info Message 的消息类型是 42。

### Format

```
Session ID
  Flags:       1 byte
               Bit order: 76543210
               Bit 0: 0 for everybody, 1 for per-client
               Bits 3-1: Authentication scheme, if bit 0 is set to 1 for per-client, otherwise 000
                         000: DH client authentication (or no per-client authentication)
                         001: PSK client authentication
               Bit 4: 1 if secret required, 0 if no secret required
               Bits 7-5: Unused, set to 0 for future compatibility
  Type byte:   Endpoint type to follow
               Type 0 is a Hash
               Type 1 is a host name String
               Type 2 is a Destination
               Type 3 is a Sig Type and Signing Public Key
  Blind Type:  2 byte blinded sig type (big endian)
  Expiration:  4 bytes, big endian, seconds since epoch
  Endpoint:    Data as specified above
               For type 0: 32 byte binary hash
               For type 1: host name String
               For type 2: binary Destination
               For type 3: 2 byte sig type (big endian)
                           Signing Public Key (length as implied by sig type)
  Private Key: Only if flag bit 0 is set to 1
               A 32-byte ECIES_X25519 private key
  Secret:      Only if flag bit 4 is set to 1
               A secret String
```
### 密钥证书

- 路由器最低版本为 0.9.43

### 新的中间结构

### 新的 NetDB 类型

为了支持对"b33"主机名的查找并在 router 没有所需信息时返回指示，我们为 Host Reply Message 定义了额外的结果代码，如下所示：

```
2: Lookup password required
   3: Private key required
   4: Lookup password and private key required
   5: Leaseset decryption failure
```
值 1-255 已经被定义为错误，因此不存在向后兼容性问题。

### 新的签名类型

路由器到客户端。新消息。

### Justification

客户端无法预先知道给定的 Hash 会解析为 Meta LS。

如果对目标地址(Destination)的 leaseset 查找返回 Meta LS，router 将执行递归解析。对于数据报，客户端不需要知道这一点；但是，对于流传输，由于协议会在 SYN ACK 中检查目标地址，它必须知道"真实"的目标地址是什么。因此，我们需要一个新的消息。

### Usage

router 会为从元 LS 中使用的实际目标维护一个缓存。当客户端向解析为元 LS 的目标发送消息时，router 会检查缓存中最后使用的实际目标。如果缓存为空，router 会从元 LS 中选择一个目标，并查找 leaseset。如果 leaseset 查找成功，router 会将该目标添加到缓存中，并向客户端发送一个元重定向消息。这只会执行一次，除非目标过期且必须更改。客户端也必须在需要时缓存该信息。元重定向消息不会作为每个 SendMessage 的回复而发送。

路由器仅向版本 0.9.47 或更高版本的客户端发送此消息。

客户端不会对此消息发送回复。

### 数据库查询消息

Meta Redirect Message 的消息类型是 43。

### 更改

```
Session ID (2 bytes) The value from the Send Message.
  Message ID generated by the router (4 bytes)
  4 byte nonce previously generated by the client
               (the value from the Send Message, may be zero)
  Flags:       2 bytes, bit order 15...0
               Unused, set to 0 for future compatibility
               Bit 0: 0 - the destination is no longer meta
                      1 - the destination is now meta
               Bits 15-1: Unused, set to 0 for future compatibility
  Original Destination (387+ bytes)
  (following fields only present if flags bit 0 is 1)
  MFlags:      2 bytes
               Unused, set to 0 for future compatibility
               From the Meta Lease for the actual Destination
  Expiration:  4 bytes, big endian, seconds since epoch
               From the Meta Lease for the actual Destination
  Cost (priority) 1 byte
               From the Meta Lease for the actual Destination
  Actual (real) Destination (387+ bytes)
```
### 数据库存储消息

如何生成和支持 Meta，包括 router 间通信和协调，超出了本提案的范围。请参见相关提案 150。

### 更新日志

离线签名无法在流式传输或可回复数据报中进行验证。请参阅下面的章节。

## Private Key File Changes Required

私钥文件 (eepPriv.dat) 格式虽然不是我们规范的官方组成部分，但在 [Java I2P javadocs](http://idk.i2p/javadoc-i2p/net/i2p/data/PrivateKeyFile.html) 中有文档记录，其他实现也支持该格式。这使得私钥可以在不同实现之间移植。

需要进行更改以存储临时公钥和离线签名信息。

### Changes

```
If the signing private key is all zeros, the offline information section follows:

  - Expires timestamp
    (4 bytes, big endian, seconds since epoch, rolls over in 2106)
  - Sig type of transient Signing Public Key (2 bytes, big endian)
  - Transient Signing Public key
    (length as specified by transient sig type)
  - Signature of above three fields by offline key
    (length as specified by destination sig type)
  - Transient Signing Private key
    (length as specified by transient sig type)
```
### I2CP 选项

添加对以下选项的支持：

```
-d days              (specify expiration in days of offline sig, default 365)
      -o offlinedestfile   (generate the online key file,
                            using the offline key file specified)
      -r sigtype           (specify sig type of transient key, default Ed25519)
```
## Streaming Changes Required

离线签名目前无法在流传输中进行验证。下面的更改将离线签名块添加到选项中。这避免了必须通过 I2CP 检索此信息的需要。

### 会话配置

```
Add new option:
  Bit:          11
  Flag:         OFFLINE_SIGNATURE
  Option order: 4
  Option data:  Variable bytes
  Function:     Contains the offline signature section from LS2.
                FROM_INCLUDED must also be set.
                Expires timestamp
                (4 bytes, big endian, seconds since epoch, rolls over in 2106)
                Transient sig type (2 bytes, big endian)
                Transient signing public key (length as implied by sig type)
                Signature of expires timestamp, transient sig type,
                and public key, by the destination public key,
                length as implied by destination public key sig type.

  Change option:
  Bit:          3
  Flag:         SIGNATURE_INCLUDED
  Option order: Change from 4 to 5

  Add information about transient keys to the
  Variable Length Signature Notes section:
  The offline signature option does not needed to be added for a CLOSE packet if
  a SYN packet containing the option was previously acked.
  More info TODO
```
### 请求租约集消息

- 另一种方法是仅添加一个标志，并通过 I2CP 检索瞬时公钥
  （参见上述主机查找/主机回复消息部分）

## 标准 LS2 头部

离线签名无法在可回复数据报处理中进行验证。需要一个标志来指示离线签名，但没有地方放置标志。这将需要一个全新的协议编号和格式。

### 请求变量租约集消息

```
Define new protocol 19 - Repliable datagram with options?
  - Destination (387+ bytes)
  - Flags (2 bytes)
    Bit order: 15 14 ... 3 2 1 0
    Bit 0: If 0, no offline keys; if 1, offline keys
    Bits 1-15: set to 0 for compatibility with future uses
  - If flag indicates offline keys, the offline signature section:
    Expires timestamp
    (4 bytes, big endian, seconds since epoch, rolls over in 2106)
    Transient sig type (2 bytes, big endian)
    Transient signing public key (length as implied by sig type)
    Signature of expires timestamp, transient sig type,
    and public key, by the destination public key,
    length as implied by destination public key sig type.
    This section can, and should, be generated offline.
  - Data
```
### 创建 Leaseset2 消息

- 替代方案是只需添加一个标志，并通过 I2CP 检索临时公钥
  （参见上面的主机查找/主机回复消息部分）
- 既然我们有了标志字节，还有什么其他选项应该现在添加吗？

## SAM V3 Changes Required

SAM 必须增强以支持 DESTINATION base 64 中的离线签名。

### 理由说明

```
Note that in the SESSION CREATE DESTINATION=$privkey,
  the $privkey raw data (before base64 conversion)
  may be optionally followed by the Offline Signature as specified in the
  Common Structures Specification.

  If the signing private key is all zeros, the offline information section follows:

  - Expires timestamp
    (4 bytes, big endian, seconds since epoch, rolls over in 2106)
  - Sig type of transient Signing Public Key (2 bytes, big endian)
  - Transient Signing Public key
    (length as specified by transient sig type)
  - Signature of above three fields by offline key
    (length as specified by destination sig type)
  - Transient Signing Private key (length as specified by transient sig type)
```
注意，离线签名仅支持 STREAM 和 RAW，不支持 DATAGRAM（直到我们定义新的 DATAGRAM 协议）。

请注意，SESSION STATUS 将返回一个全零的签名私钥和完全按照 SESSION CREATE 中提供的离线签名数据。

注意，DEST GENERATE 和 SESSION CREATE DESTINATION=TRANSIENT 不能用于创建离线签名目标。

### 消息类型

将版本升级到 3.4，还是保持在 3.1/3.2/3.3，这样就可以添加而不需要所有 3.2/3.3 的内容？

其他变更待定。请参阅上述 I2CP Host Reply Message 部分。

## BOB Changes Required

BOB 需要增强以支持离线签名和/或 Meta LS。这是低优先级的，可能永远不会被规范化或实现。SAM V3 是首选接口。

## Publishing, Migration, Compatibility

LS2（除了加密的 LS2）发布在与 LS1 相同的 DHT 位置。无法同时发布 LS1 和 LS2，除非 LS2 位于不同的位置。

加密的 LS2 发布在盲化密钥类型和密钥数据的哈希值处。然后使用此哈希值生成每日的"路由密钥"，就像 LS1 中一样。

LS2 只会在需要新功能时使用（新加密算法、加密 LS、元数据等）。LS2 只能发布到指定版本或更高版本的 floodfill。

发布 LS2 的服务器会知道任何连接的客户端都支持 LS2。它们可以在 garlic 中发送 LS2。

客户端仅在使用新加密时才会在 garlic 中发送 LS2。共享客户端会无限期使用 LS1？待办：如何让共享客户端同时支持旧加密和新加密？

## Rollout

0.9.38 包含对标准 LS2 的 floodfill 支持，包括离线密钥。

0.9.39 包含对 LS2 和 Encrypted LS2 的 I2CP 支持、sig type 11 签名/验证、floodfill 对 Encrypted LS2 的支持（sig types 7 和 11，不包含离线密钥），以及 LS2 加密/解密（不包含按客户端授权）。

0.9.40 计划包含支持使用每客户端授权对 LS2 进行加密/解密、floodfill 和 I2CP 对 Meta LS2 的支持、支持使用离线密钥的加密 LS2，以及对加密 LS2 的 b32 支持。

## 新的 DatabaseEntry 类型

加密的 LS2 设计很大程度上受到了 [Tor 的 v3 隐藏服务描述符](https://spec.torproject.org/rend-spec-v3) 的影响，两者具有相似的设计目标。
