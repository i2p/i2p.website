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

本提案的部分内容已完成，并已在 0.9.38 和 0.9.39 版本中实现。   通用结构、I2CP、I2NP 及其他规范   现已更新，以反映当前支持的变更。

已完成的部分仍可能进行小幅修订。   本提案的其他部分仍在开发中，   并可能进行重大修订。

服务查找（类型 9 和 11）优先级较低，   尚未排期，可能会拆分为单独的提案。

## 概述

这是以下 4 个提案的更新与整合：

- 110 LS2
- 120 用于大规模多宿主的元 LS2（Meta LS2）
- 121 加密 LS2
- 122 无认证服务查找（任播）

这些提案大多是独立的，但为了逻辑清晰，我们为其中多个定义并使用了   通用格式。

以下提案与此相关：

- 140 隐式多宿主（与本提案不兼容）
- 142 新加密模板（用于新对称加密）
- 144 ECIES-X25519-AEAD-Ratchet
- 145 ECIES-P256
- 146 Red25519
- 148 EdDSA-BLAKE2b-Ed25519
- 149 B32 用于加密 LS2
- 150 Garlic Farm 协议
- 151 ECDSA Blinding

## 提案

本提案定义了 5 种新的 DatabaseEntry 类型，以及   将它们存储到网络数据库和从中检索的方法，   还包括签名和验证签名的方法。

### 目标

- 向后兼容
- LS2 可与旧式多宿主共用
- 支持无需新加密或原语
- 保持加密与签名的解耦；支持所有当前和未来版本
- 支持可选的离线签名密钥
- 降低时间戳精度以减少指纹识别
- 支持目的地使用新加密
- 支持大规模多宿主
- 修复现有加密 LS 的多个问题
- 可选的盲化以减少 floodfill 的可见性
- 加密支持单密钥和多个可撤销密钥
- 服务查找以简化 outproxy、应用 DHT 引导等查找
- 不破坏依赖 32 字节二进制目的地哈希的任何功能，例如 bittorrent
- 通过属性增加 leasesets 的灵活性，类似 routerinfos 中的机制
- 将发布时间戳和可变过期时间放入头部，以便即使内容被加密也能工作（不从最早租约推导时间戳）
- 所有新类型与现有 leasesets 位于相同的 DHT 空间和位置，  
  使用户可从旧 LS 迁移到 LS2，  
  或在 LS2、Meta 和加密之间切换，  
  而无需更改 Destination 或哈希。
- 现有 Destination 可转换为使用离线密钥，  
  或恢复为在线密钥，而无需更改 Destination 或哈希。

### 非目标 / 范围外

- 新的 DHT 轮转算法或共享随机数生成
- 具体的新加密类型和使用该类型进行端到端加密的方案  
  将在单独的提案中说明。  
  本文不指定或讨论任何新加密。
- RI 或隧道构建的新加密。  
  这将在单独的提案中说明。
- I2NP DLM / DSM / DSRM 消息的加密、传输和接收方法。  
  不作更改。
- 如何生成和管理 Meta，包括后端路由器间通信、管理、故障转移和协调。  
  可能会添加到 I2CP、i2pcontrol 或新协议中。  
  这可能不会被标准化。
- 如何实际实现和管理长期存在的隧道，或取消现有隧道。  
  这极其困难，没有它就无法实现合理的优雅关闭。
- 威胁模型变更
- 离线存储格式，或存储/检索/共享数据的方法。
- 实现细节不在本文讨论范围内，由各项目自行决定。

### 理由

LS2 添加了用于更改加密类型和未来协议变更的字段。

加密 LS2 通过使用非对称加密整个租约集，   修复了现有加密 LS 的多个安全问题。

Meta LS2 提供了灵活、高效、有效且大规模的多宿主。

服务记录（Service Record）和服务列表（Service List）提供任播服务，如命名查找和 DHT 引导。

### NetDB 数据类型

类型编号用于 I2NP 数据库查找/存储消息中。

“端到端”列指查询/响应是否作为大蒜消息发送到 Destination。

现有类型：

| NetDB 数据 | 查找类型 | 存储类型 |
|------------|-------------|------------|
| any        | 0           | any        |
| LS         | 1           | 1          |
| RI         | 2           | 0          |
| exploratory| 3           | DSRM       |
新类型：

| NetDB 数据     | 查找类型 | 存储类型 | 标准 LS2 头？ | 端到端发送？ |
|----------------|-------------|------------|------------------|------------------|
| LS2            | 1           | 3          | yes              | yes              |
| 加密 LS2       | 1           | 5          | no               | no               |
| Meta LS2       | 1           | 7          | yes              | no               |
| 服务记录       | n/a         | 9          | yes              | no               |
| 服务列表       | 4           | 11         | no               | no               |
### 说明

- 查找类型目前使用数据库查找消息中的位 3-2。  
  任何额外类型都需要使用位 4。

- 所有存储类型均为奇数，因为旧路由器会忽略数据库存储消息  
  类型字段的高位。  
  我们宁愿让解析失败为 LS 而不是压缩的 RI。

- 类型应在签名覆盖的数据中显式、隐式还是都不包含？

### 查找/存储流程

类型 3、5 和 7 可作为标准 leaseset 查找（类型 1）的响应返回。   类型 9 永远不会作为查找的响应返回。   类型 11 作为新的服务查找类型（类型 11）的响应返回。

只有类型 3 可在客户端到客户端的大蒜消息中发送。

### 格式

类型 3、7 和 9 具有通用格式::

```text
Standard LS2 Header
- as defined below

Type-Specific Part
- as defined below in each part

Standard LS2 Signature:
- Length as implied by sig type of signing key
```
标准 LS2 头

类型特定部分

### 隐私/安全考虑

标准 LS2 签名:

## 标准 LS2 头

类型 5（加密）不以 Destination 开头，具有   不同格式。见下文。

### 格式

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
### 理由

  - 如下定义

  - 如下各部分中定义

  - 长度由签名密钥的签名类型隐含

- 未发布/已发布：用于端到端发送数据库存储时，  
  发送路由器可能希望指示此 leaseset 不应发送给他人。  
  我们目前使用启发式方法维护此状态。

### 问题

- 已发布：取代了确定 leaseset “版本”所需的复杂逻辑。  
  目前，版本是最后过期租约的过期时间，  
  发布路由器在发布仅移除旧租约的 leaseset 时，  
  必须至少增加 1ms。

- 过期：允许 netdb 条目的过期时间早于其最后过期的 leaseset。  
  对于 LS2 可能无用（预期 leaseset 保持 11 分钟最大过期），  
  但对于其他新类型是必要的（见下文的 Meta LS 和服务记录）。

- 离线密钥是可选的，以降低初始/必需实现的复杂性。

### 说明

- 可进一步降低时间戳精度（10 分钟？）但需添加版本号。  
  这可能会破坏多宿主，除非我们有保序加密？  
  可能无法完全不用时间戳。

- 替代方案：3 字节时间戳（纪元 / 10 分钟），1 字节版本，2 字节过期

- 类型在数据/签名中是显式还是隐式？签名的“域”常量？

## 新 DatabaseEntry 类型

### LeaseSet 2

类型 11（服务列表）是多个服务记录的聚合，具有   不同格式。见下文。

- 路由器不应每秒发布超过一次 LS。  
  如果这样做，必须将发布时间戳人为增加 1  
  超过之前发布的 LS。

待定

    Standard LS flag (1)
类型 3、7 和 9 使用标准 LS2 头，如下指定：

    Standard LS2 type (3)
与现有 LeaseSet 的变更：

    Hash of destination
    This hash is then used to generate the daily "routing key", as in LS1
查找使用

    10 minutes, as in a regular LS.
存储使用

    Destination

### 格式

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
### 理由

- 路由器实现可缓存临时密钥和签名，  
  以避免每次验证。特别是 floodfill 和长期连接两端的路由器可从中受益。

- 离线密钥和签名仅适用于长期存在的目的地，  
  即服务器，而非客户端。

### 讨论

存储于

典型过期时间

由

- 添加发布时间戳、过期时间戳、标志和属性
- 添加加密类型
- 移除撤销密钥

本提案继续使用 leaseset 中的公钥作为   端到端加密密钥，并保留目的地中的公钥字段未使用，如现在一样。   加密类型未在目的地密钥证书中指定，将保持为 0。

- 属性：未来扩展和灵活性。  
  放在首位，以便必要时用于解析剩余数据。

### 新加密问题

一个被拒绝的替代方案是在目的地密钥证书中指定加密类型，   使用目的地中的公钥，而不使用 leaseset 中的公钥。   我们不计划这样做。

- 多个加密类型/公钥对  
  有助于过渡到新加密类型。另一种方法是  
  发布多个 leasesets，可能使用相同隧道，  
  如我们现在对 DSA 和 EdDSA 目的地所做的那样。  
  隧道中传入加密类型的识别  
  可使用现有的会话标签机制，  
  和/或使用每个密钥进行试解密。传入消息的长度也可能提供线索。

- 实际公钥的位置不变。
- 加密类型或公钥可在不更改目的地的情况下更改。
- 移除了未使用的撤销字段
- 与本提案中其他 DatabaseEntry 类型的基本兼容性
- 允许多个加密类型

- 公钥和加密类型的位置与 RouterInfo 不同
- 在 leaseset 中保留了未使用的公钥
- 需要全网实现；作为替代，实验性加密类型可使用，如果 floodfill 允许  
  （但参见相关提案 136 和 137 关于支持实验性签名类型）。  
  替代提案可能更容易为实验性加密类型实现和测试。

### 说明

- 加密类型代表曲线、密钥长度和端到端方案的组合，  
  包括 KDF 和 MAC（如果有）。

- 我们包含了密钥长度字段，以便 LS2  
  即使对于未知加密类型，floodfill 也能解析和验证。

- 第一个提议的新加密类型  
  可能是 ECIES/X25519。其端到端使用方式  
  （略微修改的 ElGamal/AES+SessionTag  
  或完全新的，如 ChaCha/Poly）将在一个或多个单独提案中指定。  
  另见 ECIES 提案 144 和 145。

### 加密 LS2

LS2 的优点：

- 租约中的 8 字节过期时间改为 4 字节。

LS2 的缺点：

其中一些超出本提案范围，   但暂时在此记录，因为我们尚未有   单独的加密提案。   另见 ECIES 提案 144 和 145。

- 如果我们实现撤销，可通过设置过期字段为零，  
  或零租约，或两者来实现。无需单独的撤销密钥。

目标：

    Standard LS flag (1)
加密 LS2 永远不会在端到端大蒜消息中发送。   使用上述标准 LS2。

    Encrypted LS2 type (5)
与现有加密 LeaseSet 的变更：

    Hash of blinded sig type and blinded public key
    Two byte sig type (big endian, e.g. 0x000b) || blinded public key
    This hash is then used to generate the daily "routing key", as in LS1
查找使用

    10 minutes, as in a regular LS, or hours, as in a meta LS.
存储使用

    Destination


### 定义

存储于

典型过期时间

    n-byte output from a cryptographically-secure random number generator.

    In addition to the requirement of CSRNG being cryptographically-secure (and thus
    suitable for generating key material), it MUST be safe
    for some n-byte output to be used for key material when the byte sequences immediately
    preceding and following it are exposed on the network (such as in a salt, or encrypted
    padding). Implementations that rely on a potentially-untrustworthy source should hash
    any output that is to be exposed on the network. See [PRNG references](http://projectbullrun.org/dual-ec/ext-rand.html) and [Tor dev discussion](https://lists.torproject.org/pipermail/tor-dev/2015-November/009954.html).

由

    SHA-256 hash function that takes a personalization string p and data d, and
    produces an output of length 32 bytes.

    Use SHA-256 as follows::

        H(p, d) := SHA-256(p || d)

我们定义以下函数，对应于用于加密 LS2 的加密构建块：

    The ChaCha20 stream cipher as specified in [RFC 7539 Section 2.4](https://tools.ietf.org/html/rfc7539#section-2.4), with the initial counter
    set to 1. S_KEY_LEN = 32 and S_IV_LEN = 12.

    ENCRYPT(k, iv, plaintext)
        Encrypts plaintext using the cipher key k, and nonce iv which MUST be unique for
        the key k. Returns a ciphertext that is the same size as the plaintext.

        The entire ciphertext must be indistinguishable from random if the key is secret.

    DECRYPT(k, iv, ciphertext)
        Decrypts ciphertext using the cipher key k, and nonce iv. Returns the plaintext.


CSRNG(n)

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

H(p, d)

    X25519 public key agreement system. Private keys of 32 bytes, public keys of 32
    bytes, produces outputs of 32 bytes. It has the following
    functions:

    GENERATE_PRIVATE()
        Generates a new private key.

    DERIVE_PUBLIC(privkey)
        Returns the public key corresponding to the given private key.

    DH(privkey, pubkey)
        Generates a shared secret from the given private and public keys.

STREAM

    A cryptographic key derivation function which takes some input key material ikm (which
    should have good entropy but is not required to be a uniformly random string), a salt
    of length 32 bytes, and a context-specific 'info' value, and produces an output
    of n bytes suitable for use as key material.

    Use HKDF as specified in [RFC 5869](https://tools.ietf.org/html/rfc5869), using the HMAC hash function SHA-256
    as specified in [RFC 2104](https://tools.ietf.org/html/rfc2104). This means that SALT_LEN is 32 bytes max.


### 格式

SIG

- 加密密钥按服务器偏好排序，最优先的在前。  
  客户端默认行为是选择第一个支持的加密类型的密钥。  
  客户端可基于加密支持、相对性能和其他因素使用其他选择算法。

DH

    Layer 0 data + Enc(layer 1 data + Enc(layer 2 data)) + Signature

HKDF(salt, ikm, info, n)

加密 LS2 格式由三层嵌套组成：

#### 第 0 层（外层）

整体格式如下::

    1 byte

    Not actually in header, but part of data covered by signature.
    Take from field in Database Store Message.

注意加密 LS2 是盲化的。头中没有 Destination。   DHT 存储位置是 SHA-256(sig type || 盲化公钥)，每日轮转。

    2 bytes, big endian
    This will always be type 11, identifying a Red25519 blinded key.

不使用上述指定的标准 LS2 头。

    Length as implied by sig type

类型

    4 bytes, big endian

    Seconds since epoch, rolls over in 2106

盲化公钥签名类型

    2 bytes, big endian

    Offset from published timestamp in seconds, 18.2 hours max

盲化公钥

    2 bytes

    Bit order: 15 14 ... 3 2 1 0

    Bit 0: If 0, no offline keys; if 1, offline keys

    Other bits: set to 0 for compatibility with future uses

发布时间戳

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

过期

    2 bytes, big endian

标志

    lenOuterCiphertext bytes

    Encrypted layer 1 data. See below for key derivation and encryption algorithms.

临时密钥数据

    Length as implied by sig type of the signing key used

    The signature is of everything above.

    If the flag indicates offline keys, the signature is verified with the transient
    public key. Otherwise, the signature is verified with the blinded public key.


#### 第 1 层（中间层）

lenOuterCiphertext

    1 byte
    
    Bit order: 76543210

    Bit 0: 0 for everybody, 1 for per-client, auth section to follow

    Bits 3-1: Authentication scheme, only if bit 0 is set to 1 for per-client, otherwise 000
              000: DH client authentication (or no per-client authentication)
              001: PSK client authentication

    Bits 7-4: Unused, set to 0 for future compatibility

outerCiphertext

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

签名

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


标志

    Length implied by lenOuterCiphertext (whatever data remains)

    Encrypted layer 2 data. See below for key derivation and encryption algorithms.


#### 第 2 层（内层）

DH 客户端认证数据

    1 byte

    Either 3 (LS2) or 7 (Meta LS2)

PSK 客户端认证数据

    LeaseSet2 data for the given type.

    Includes the header and signature.


### 盲化密钥派生

innerCiphertext

类型

#### 目标

- 添加盲化
- 允许多个签名类型
- 不需要任何新加密原语
- 可选地加密给每个接收者，可撤销
- 仅支持加密标准 LS2 和 Meta LS2

#### 安全性

数据

#### 定义

我们使用以下方案进行密钥盲化，   基于 Ed25519 和 [ZCash RedDSA](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf)。   Re25519 签名在 Ed25519 曲线上，使用 SHA-512 作为哈希。

    The Ed25519 base point (generator) 2^255 - 19 as in [Ed25519](http://cr.yp.to/papers.html#ed25519)

我们不使用 [Tor's rend-spec-v3.txt appendix A.2](https://spec.torproject.org/rend-spec-v3)，   因为其盲化公钥可能不在素数阶子群中，安全影响未知。

    The Ed25519 order 2^252 + 27742317777372353535851937790883648493
    as in [Ed25519](http://cr.yp.to/papers.html#ed25519)

盲化方案的安全性要求 alpha 的分布与未盲化私钥相同。   然而，当我们盲化 Ed25519 私钥（签名类型 7）   到 Red25519 私钥（签名类型 11）时，分布不同。   为满足 [zcash 第 4.1.6.1 节](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf) 的要求，   Red25519（签名类型 11）也应用于未盲化密钥，   以便“重新随机化的公钥和该密钥下的签名组合   不会泄露从中重新随机化的密钥”。   我们允许类型 7 用于现有目的地，但建议   新目的地使用类型 11。

    Convert a private key to public, as in Ed25519 (mulitply by G)

B

    A 32-byte random number known to those who know the destination.

L

    Generate alpha for the current date, for those who know the destination and the secret.
    The result must be identically distributed as Ed25519 private keys.

DERIVE_PUBLIC(a)

    The unblinded 32-byte EdDSA or RedDSA signing private key used to sign the destination

alpha

    The unblinded 32-byte EdDSA or RedDSA signing public key in the destination,
    = DERIVE_PUBLIC(a), as in Ed25519

GENERATE_ALPHA(destination, date, secret)

    The blinded 32-byte EdDSA signing private key used to sign the encrypted leaseset
    This is a valid EdDSA private key.

a

    The blinded 32-byte EdDSA signing public key in the Destination,
    may be generated with DERIVE_PUBLIC(a'), or from A and alpha.
    This is a valid EdDSA public key, on the curve and on the prime-order subgroup.

A

    Flip the order of the input bytes to little-endian

a'

    32 bytes = (LEOS2IP(SHA512(x))) mod B, same as in Ed25519 hash-and-reduce


#### 盲化计算

A'

LEOS2IP(x)

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
H*(x)

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
每天（UTC）必须生成新的密钥 alpha 和盲化密钥。   密钥 alpha 和盲化密钥计算如下。

```text
// BLIND_PUBKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  A = destination's signing public key
  // Addition using group elements (points on the curve)
  blinded public key = A' = BLIND_PUBKEY(A, alpha) = A + DERIVE_PUBLIC(alpha)
```
GENERATE_ALPHA(destination, date, secret)，适用于所有方：

#### 签名

BLIND_PRIVKEY()，由发布 leaseset 的所有者使用：

BLIND_PUBKEY()，由检索 leaseset 的客户端使用：

两种计算 A' 的方法产生相同结果，符合要求。

未盲化 leaseset 由未盲化 Ed25519 或 Red25519 签名私钥签名，   并使用未盲化 Ed25519 或 Red25519 签名公钥（签名类型 7 或 11）验证，如常。

#### 签名/验证计算

如果签名公钥是离线的，   未盲化 leaseset 由未盲化临时 Ed25519 或 Red25519 签名私钥签名，   并使用未盲化 Ed25519 或 Red25519 临时签名公钥（签名类型 7 或 11）验证，如常。   有关加密 leaseset 的离线密钥的额外说明见下文。

对于加密 leaseset 的签名，我们使用 Red25519，基于 [RedDSA](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf)   使用盲化密钥进行签名和验证。   Red25519 签名在 Ed25519 曲线上，使用 SHA-512 作为哈希。

Red25519 与标准 Ed25519 几乎相同，仅在以下方面不同。

加密 leaseset 的外层使用 Red25519 密钥和签名。

Red25519 与 Ed25519 几乎相同。有两个区别：

```text
T = 80 random bytes
  r = H*(T || publickey || message)
  // rest is the same as in Ed25519
```
Red25519 私钥由随机数生成，然后必须对 L 取模，L 如上定义。   Ed25519 私钥由随机数生成，然后使用   字节 0 和 31 的位掩码进行“钳位”。Red25519 不这样做。   上述定义的 GENERATE_ALPHA() 和 BLIND_PRIVKEY() 函数使用 mod L 生成正确的   Red25519 私钥。

```text
// same as in Ed25519
```
### 加密和处理

#### 子凭据派生

在 Red25519 中，签名计算 r 使用额外的随机数据，   并使用公钥值而非私钥的哈希。   由于随机数据，每次 Red25519 签名都不同，即使   使用相同密钥签名相同数据。

```text
A = destination's signing public key
  stA = signature type of A, 2 bytes big endian (0x0007 or 0x000b)
  stA' = signature type of A', 2 bytes big endian (0x000b)
  keydata = A || stA || stA'
  credential = H("credential", keydata)
```
签名：

验证：

```text
subcredential = H("subcredential", credential || blindedPublicKey)
```
作为盲化过程的一部分，我们需要确保加密 LS2 只能被知道对应目的地签名公钥的人解密。   不需要完整目的地。   为实现此目的，我们从签名公钥派生凭据：

#### 第 1 层加密

个性化字符串确保凭据不会与用作 DHT 查找键的任何哈希冲突，例如纯目的地哈希。

```text
outerInput = subcredential || publishedTimestamp
```
对于给定盲化密钥，我们可以派生子凭据：

```text
outerSalt = CSRNG(32)
```
子凭据包含在以下密钥派生过程中，将这些密钥绑定到知道目的地签名公钥的知识。

```text
keys = HKDF(outerSalt, outerInput, "ELS2_L1K", 44)
  outerKey = keys[0:31]
  outerIV = keys[32:43]
```
首先，准备密钥派生过程的输入：

```text
outerCiphertext = outerSalt || ENCRYPT(outerKey, outerIV, outerPlaintext)
```
#### 第 1 层解密

然后，生成随机盐：

```text
outerSalt = outerCiphertext[0:31]
```
然后，派生用于加密第 1 层的密钥：

```text
outerInput = subcredential || publishedTimestamp
  keys = HKDF(outerSalt, outerInput, "ELS2_L1K", 44)
  outerKey = keys[0:31]
  outerIV = keys[32:43]
```
最后，加密并序列化第 1 层明文：

```text
outerPlaintext = DECRYPT(outerKey, outerIV, outerCiphertext[32:end])
```
#### 第 2 层加密

从第 1 层密文中解析盐：

然后，派生用于加密第 1 层的密钥：

```text
innerInput = authCookie || subcredential || publishedTimestamp
  innerSalt = CSRNG(32)
  keys = HKDF(innerSalt, innerInput, "ELS2_L2K", 44)
  innerKey = keys[0:31]
  innerIV = keys[32:43]
  innerCiphertext = innerSalt || ENCRYPT(innerKey, innerIV, innerPlaintext)
```
#### 第 2 层解密

最后，解密第 1 层密文：

当启用客户端授权时，``authCookie`` 按下文所述计算。   当禁用客户端授权时，``authCookie`` 为空字节数组。

```text
innerInput = authCookie || subcredential || publishedTimestamp
  innerSalt = innerCiphertext[0:31]
  keys = HKDF(innerSalt, innerInput, "ELS2_L2K", 44)
  innerKey = keys[0:31]
  innerIV = keys[32:43]
  innerPlaintext = DECRYPT(innerKey, innerIV, innerCiphertext[32:end])
```
### 每个客户端授权

加密过程与第 1 层类似：

当启用客户端授权时，``authCookie`` 按下文所述计算。   当禁用客户端授权时，``authCookie`` 为空字节数组。

#### DH 客户端授权

解密过程与第 1 层类似：

当目的地启用客户端授权时，服务器维护一个授权解密加密 LS2 数据的客户端列表。   每个客户端存储的数据取决于授权机制，包括每个客户端生成并通过安全带外机制发送给服务器的某种形式的密钥材料。

```text
authCookie = CSRNG(32)
  esk = GENERATE_PRIVATE()
  epk = DERIVE_PUBLIC(esk)
```
实现每个客户端授权有两种替代方案：

```text
sharedSecret = DH(esk, cpk_i)
  authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
  okm = HKDF(epk, authInput, "ELS2_XCA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
  clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
```
每个客户端生成 DH 密钥对 ``[csk_i, cpk_i]``，并将公钥 ``cpk_i`` 发送给服务器。

服务器处理 ^^^^^^^^^^^^^^^^^ 服务器生成新的 ``authCookie`` 和临时 DH 密钥对：

```text
sharedSecret = DH(csk_i, epk)
  authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
  okm = HKDF(epk, authInput, "ELS2_XCA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
```
然后，对于每个授权客户端，服务器使用其公钥加密 ``authCookie``：

```text
authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie_i)
```
#### 预共享密钥客户端授权

服务器将每个 ``[clientID_i, clientCookie_i]`` 元组放入加密 LS2 的第 1 层，连同 ``epk``。

客户端处理 ^^^^^^^^^^^^^^^^^ 客户端使用其私钥派生其预期的客户端标识符 ``clientID_i``、加密密钥 ``clientKey_i`` 和加密 IV ``clientIV_i``：

```text
authCookie = CSRNG(32)
  authSalt = CSRNG(32)
```
然后，客户端在第 1 层授权数据中搜索包含 ``clientID_i`` 的条目。如果存在匹配条目，客户端解密以获取 ``authCookie``：

```text
authInput = psk_i || subcredential || publishedTimestamp
  okm = HKDF(authSalt, authInput, "ELS2PSKA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
  clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
```
每个客户端生成 32 字节密钥 ``psk_i``，并将其发送给服务器。   或者，服务器可以生成密钥，并将其发送给一个或多个客户端。

服务器处理 ^^^^^^^^^^^^^^^^^ 服务器生成新的 ``authCookie`` 和盐：

```text
authInput = psk_i || subcredential || publishedTimestamp
  okm = HKDF(authSalt, authInput, "ELS2PSKA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
```
然后，对于每个授权客户端，服务器使用其预共享密钥加密 ``authCookie``：

```text
authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie_i)
```
#### 安全考虑

服务器将每个 ``[clientID_i, clientCookie_i]`` 元组放入加密 LS2 的第 1 层，连同 ``authSalt``。

客户端处理 ^^^^^^^^^^^^^^^^^ 客户端使用其预共享密钥派生其预期的客户端标识符 ``clientID_i``、加密密钥 ``clientKey_i`` 和加密 IV ``clientIV_i``：

然后，客户端在第 1 层授权数据中搜索包含 ``clientID_i`` 的条目。如果存在匹配条目，客户端解密以获取 ``authCookie``：

上述两种客户端授权机制都提供客户端成员的隐私。   只知道目的地的实体可以看到当前有多少客户端订阅，但无法跟踪哪些客户端被添加或撤销。

- 为安全加密整个内容
- 安全加密，不仅使用 AES。
- 加密给每个接收者

服务器每次生成加密 LS2 时应随机化客户端顺序，以防止客户端了解其在列表中的位置并推断其他客户端何时被添加或撤销。

- 外层包含存储和检索所需的必要明文信息。
- 中间层处理客户端认证。
- 内层包含实际的 LS2 数据。

服务器可以选择通过在授权数据列表中插入随机条目来隐藏订阅的客户端数量。

- 未盲化目的地中的签名公钥必须是  
  Ed25519（签名类型 7）或 Red25519（签名类型 11）；  
  不支持其他签名类型
- 如果签名公钥是离线的，临时签名公钥也必须是 Ed25519
- 盲化在计算上简单
- 使用现有加密原语
- 盲化公钥无法被反盲化
- 盲化公钥必须在 Ed25519 曲线和素数阶子群上
- 必须知道目的地的签名公钥  
  （不需要完整目的地）以派生盲化公钥
- 可选地提供派生盲化公钥所需的额外密钥

DH 客户端授权的优点 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- 方案的安全性不完全依赖于客户端密钥材料的带外交换。客户端的私钥永远不需要离开其设备，因此能够拦截带外交换但无法破解 DH 算法的对手无法解密加密 LS2，或确定客户端被授予访问权限的时间。

### 带 Base 32 地址的加密 LS

DH 客户端授权的缺点 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

PSK 客户端授权的优点 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

### 带离线密钥的加密 LS

PSK 客户端授权的缺点 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

参见提案 149。

你不能对 bittorrent 使用加密 LS2，因为紧凑公告回复是 32 字节。   32 字节仅包含哈希。没有空间指示 leaseset 是否加密，或签名类型。

### 说明

- 服务器端需要 N + 1 次 DH 操作（N 个客户端）。
- 客户端需要一次 DH 操作。
- 客户端需要生成密钥。

- 不需要 DH 操作。
- 允许服务器生成密钥。
- 允许服务器与多个客户端共享相同密钥（如果需要）。

- 方案的安全性严重依赖于客户端密钥材料的带外交换。能够拦截特定客户端交换的对手可以解密该客户端被授权的任何后续加密 LS2，并确定客户端访问何时被撤销。

- 使用加密 leaseset 的服务会将加密版本发布到 floodfill。  
  但为提高效率，一旦通过认证（例如通过白名单），  
  它会向客户端发送未加密的 leaseset 到封装的大蒜消息中。

- Floodfill 可能会将最大大小限制为合理值以防止滥用。

### Meta LS2

对于带离线密钥的加密 leaseset，盲化私钥也必须离线生成，每天一个。

由于可选的离线签名块在加密 leaseset 的明文部分，   任何抓取 floodfill 的人都可以使用它来跟踪 leaseset（但无法解密）数天。   为防止此情况，密钥所有者也应为每天生成新的临时密钥。   临时和盲化密钥都可以提前生成，并批量交付给路由器。

本提案未定义用于打包多个临时和盲化密钥并提供给客户端或路由器的文件格式。   本提案未定义支持带离线密钥的加密 leaseset 的 I2CP 协议增强。

这用于替换多宿主。像任何 leaseset 一样，由创建者签名。   这是目的地哈希的认证列表。

Meta LS2 是树结构的顶部，也可能是中间节点。   它包含多个条目，每个指向一个 LS、LS2 或另一个 Meta LS2，   以支持大规模多宿主。   Meta LS2 可以包含 LS、LS2 和 Meta LS2 条目的混合。   树的叶子始终是 LS 或 LS2。   树是有向无环图（DAG）；禁止循环；进行查找的客户端必须检测并拒绝跟随循环。

Meta LS2 的过期时间可以比标准 LS 或 LS2 长得多。   顶级可能在发布日期后几小时过期。   最大过期时间将由 floodfill 和客户端强制执行，待定。

Meta LS2 的用例是大规模多宿主，但在路由器重启时对路由器与 leaseset 的关联保护不比现在使用 LS 或 LS2 提供的更多。   这相当于“facebook”用例，可能不需要关联保护。此用例可能需要离线密钥，   在树的每个节点的标准头中提供。

叶路由器、中间和主 Meta LS 签名者之间协调的后端协议未在此指定。   要求非常简单——只需验证对等方是否在线，   并每几小时发布一个新 LS。唯一复杂的是在失败时为顶级或中间级 Meta LS 选择新发布者。

在提案 140 “隐式多宿主”中记录了混合 leaseset，其中来自多个路由器的租约被组合、签名并在单个 leaseset 中发布。   此提案如所写不可行，因为流连接不会“粘滞”到单个路由器，参见 http://zzz.i2p/topics/2335 。

隐式多宿主的后端协议和与路由器及客户端内部的交互将非常复杂。

    Standard LS flag (1)
为避免顶级 Meta LS 的 floodfill 过载，过期时间至少应为几小时。   客户端必须缓存顶级 Meta LS，并在未过期时跨重启持久化。

    Meta LS2 type (7)
我们需要定义客户端遍历树的算法，包括回退，   以便使用分散。一些哈希距离、成本和随机性的函数。   如果节点同时有 LS 或 LS2 和 Meta LS，我们需要知道何时可以使用这些 leaseset，何时应继续遍历树。

    Hash of destination
    This hash is then used to generate the daily "routing key", as in LS1
查找使用

    Hours. Max 18.2 hours (65535 seconds)
存储使用

    "master" Destination or coordinator, or intermediate coordinators

### 格式

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
存储于

### 说明

- 解密后，应进行几项检查，包括内部时间戳和过期时间与顶层匹配。

- 选择了 ChaCha20 而非 AES。虽然在有 AES 硬件支持时速度相似，  
  但在没有 AES 硬件支持时（如低端 ARM 设备），ChaCha20 快 2.5-3 倍。

- 我们对速度不够关心，因此不使用带密钥的 BLAKE2b。  
  它的输出大小足以容纳我们所需的最大 n（或我们可以用计数器参数调用一次以获取每个所需密钥）。  
  BLAKE2b 比 SHA-256 快得多，带密钥的 BLAKE2b 会减少哈希函数调用总数。  
  但参见提案 148，其中提议我们因其他原因切换到 BLAKE2b。  
  参见 [Secure key derivation performance](https://www.lvh.io/posts/secure-key-derivation-performance.html)。

### 服务记录

典型过期时间

由

标志和属性：供将来使用

    n/a, see Service List
这是单个记录，说明目的地正在参与某项服务。   它由参与者发送到 floodfill。   它永远不会由 floodfill 单独发送，仅作为服务列表的一部分。   服务记录也用于撤销参与服务，通过将过期时间设为零。

    Service Record type (9)
这不是 LS2，但使用标准 LS2 头和签名格式。

    Hash of service name
    This hash is then used to generate the daily "routing key", as in LS1
查找使用

    Hours. Max 18.2 hours (65535 seconds)
存储使用

    Destination

### 格式

```
Standard LS2 Header as specified above

  Service Record Type-Specific Part
  - Port (2 bytes, big endian) (0 if unspecified)
  - Hash of service name (32 bytes)

  Standard LS2 Signature:
  - Signature (40+ bytes)
    The signature is of everything above.
```
### 说明

- 使用此功能的分布式服务将有一个或多个拥有服务目的地私钥的“主”节点。  
  他们将（带外）确定当前活动目的地列表并发布 Meta LS2。  
  为冗余，多个主节点可以多宿主（即并发发布）Meta LS2。

- 分布式服务可以从单个目的地或使用旧式多宿主开始，然后过渡到 Meta LS2。  
  标准 LS 查找可以返回 LS、LS2 或 Meta LS2 中的任何一个。

- 当服务使用 Meta LS2 时，它没有隧道（租约）。

### 服务列表

存储于

典型过期时间

由

这与 LS2 完全不同，使用不同格式。

服务列表由 floodfill 创建和签名。它是无认证的，   因为任何人都可以通过向 floodfill 发布服务记录来加入服务。

服务列表包含短服务记录，而非完整服务记录。   它们包含签名但只有哈希，没有完整目的地，因此无法在没有完整目的地的情况下验证。

    Service List lookup type (11)
服务列表的安全性（如果有）和可取性待定。   floodfill 可限制发布和查找到服务白名单，   但该白名单可能因实现或操作员偏好而异。   可能无法在实现间就共同基础白名单达成共识。

    Service List type (11)
如果服务名称包含在上述服务记录中，   floodfill 操作员可能反对；如果仅包含哈希，   则无验证，服务记录可能“提前”进入任何其他 netdb 类型并存储在 floodfill 中。

    Hash of service name
    This hash is then used to generate the daily "routing key", as in LS1
查找使用

    Hours, not specified in the list itself, up to local policy
存储使用

    Nobody, never sent to floodfill, never flooded.

### 格式

存储于

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
典型过期时间

- 如果过期时间全为零，floodfill 应撤销记录，不再将其包含在服务列表中。

由

- 存储：floodfill 可严格限制这些记录的存储，限制每个哈希存储的记录数量及其过期时间。  
  也可使用白名单。

不使用上述指定的标准 LS2 头。

- 任何其他在相同哈希的 netdb 类型优先，因此服务记录永远不能覆盖 LS/RI，但 LS/RI 会覆盖该哈希的所有服务记录。

### 说明

- 前缀服务名称的哈希
- 移除创建者的哈希
- 验证修改后内容的签名

- 获取目的地
- 验证 (发布时间戳 + 过期 + 标志 + 端口 + 服务名称的哈希) 的签名

- 获取目的地
- 验证 (发布时间戳 + 4 个零字节 + 标志 + 端口 + 服务名称的哈希) 的签名

## 通用结构规范变更要求

### 密钥证书

验证服务列表签名：

### 新中间结构

验证每个短服务记录签名：

### 新 NetDB 类型

验证每个撤销记录签名：

### 新签名类型

本提案范围外。   添加到 ECIES 提案 144 和 145。

## 加密规范变更要求

添加 Lease2、MetaLease、LeaseSet2Header 和 OfflineSignature 的新结构。   自 0.9.38 版本起生效。

## I2NP 变更要求

添加每个新 leaseset 类型的结构，从上文整合。   对于 LeaseSet2、EncryptedLeaseSet 和 MetaLeaseSet，   自 0.9.38 版本起生效。   对于服务记录和服务列表，   初步且未排期。

### 数据库查找消息

添加 RedDSA_SHA512_Ed25519 类型 11。   公钥 32 字节；私钥 32 字节；哈希 64 字节；签名 64 字节。

### 变更

```
Flags byte: Lookup type field, currently bits 3-2, expands to bits 4-2.
  Lookup type 0x04 is defined as the service list lookup.

  Add note: Service list loookup may only be sent to floodfills with a minimum version.
  Minimum version is 0.9.38.
```
### 数据库存储消息

本提案范围外。   参见提案 144 和 145。

### 变更

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
## I2CP 变更要求

### I2CP 选项

添加说明：LS2 只能发布到具有最低版本的 floodfill。

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
添加服务列表查找类型。

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
### 会话配置

添加所有新存储类型。

### 请求 leaseset 消息

路由器端解释的新选项，在 SessionConfig 映射中发送：

### 请求可变 leaseset 消息

客户端端解释的新选项：

### 创建 leaseset2 消息

注意，对于离线签名，选项   i2cp.leaseSetOfflineExpiration、   i2cp.leaseSetTransientPublicKey 和   i2cp.leaseSetOfflineSignature 是必需的，   且签名由临时签名私钥完成。

### 理由

- 我们使用签名长度而非签名类型，以支持未知签名类型。

- 服务列表没有过期时间，接收者可根据策略或单个记录的过期时间自行决定。

- 服务列表不泛洪，只有单个服务记录泛洪。每个 floodfill 创建、签名并缓存服务列表。  
  floodfill 使用其自身策略决定缓存时间和最大服务及撤销记录数。

### 消息类型

路由器到客户端。   无变更。   租约以 8 字节时间戳发送，即使返回的 leaseset 将是带 4 字节时间戳的 LS2。   注意，响应可能是创建 leaseset 或创建 leaseset2 消息。

### 格式

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
### 说明

- 为让路由器解析存储类型，类型必须在消息中，  
  除非在会话配置中提前传递给路由器。  
  为共用解析代码，更容易在消息本身中包含它。

### 问题

- 为让路由器知道私钥的类型和长度，  
  它必须在 leaseset 之后，除非解析器在会话配置中提前知道类型。  
  为共用解析代码，更容易从消息本身知道它。

### 盲化信息消息

路由器到客户端。   无变更。   租约以 8 字节时间戳发送，即使返回的 leaseset 将是带 4 字节时间戳的 LS2。   注意，响应可能是创建 leaseset 或创建 leaseset2 消息。

### 理由

- 签名私钥，以前为撤销定义但未使用，  
  在 LS2 中不存在。

- 最低路由器版本为 0.9.39。
- 0.9.38 中有消息类型 40 的初步版本，但格式已更改。  
  类型 40 已废弃且不受支持。

- 需要更多变更以支持加密和 meta LS。

### 用法

客户端到路由器。   新消息，用于替代创建 leaseset 消息。

创建 leaseset2 消息的消息类型为 41。

### 消息类型

客户端到路由器。   新消息。

### 格式

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
### 说明

- 路由器需要知道目的地是否被盲化。  
  如果被盲化并使用密钥或每个客户端认证，  
  它也需要有该信息。

### 问题

### 主机回复消息（加密）

在客户端向盲化目的地发送消息之前，必须   在主机查找消息中查找“b33”，或发送盲化信息消息。   如果盲化目的地需要密钥或每个客户端认证，   客户端必须发送盲化信息消息。

```
2: Lookup password required
   3: Private key required
   4: Lookup password and private key required
   5: Leaseset decryption failure
```
路由器不对此消息回复。

### Meta 重定向消息

盲化信息消息的消息类型为 42。

### 理由

为支持“b33”主机名的查找并返回指示   如果路由器没有所需信息，我们为   主机回复消息定义额外的结果代码，如下：

值 1-255 已定义为错误，因此没有   向后兼容性问题。

### 用法

路由器到客户端。   新消息。

客户端事先不知道给定哈希将解析   为 Meta LS。

如果对目的地的 leaseset 查找返回 Meta LS，   路由器将进行递归解析。   对于数据报，客户端端不需要知道；   但对于流，协议在 SYN ACK 中检查目的地，   它必须知道“真实”目的地。   因此，我们需要新消息。

### 消息类型

路由器维护从 meta LS 使用的实际目的地的缓存。   当客户端向解析为 meta LS 的目的地发送消息时，   路由器检查缓存中上次使用的实际目的地。   如果缓存为空，路由器从 meta LS 选择一个目的地，   并查找 leaseset。   如果 leaseset 查找成功，路由器将该目的地   添加到缓存，并向客户端发送 Meta 重定向消息。   这只做一次，除非目的地过期并必须更改。   客户端也必须在需要时缓存信息。   Meta 重定向消息不会作为每个 SendMessage 的回复发送。

### 格式

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
### 为支持 Meta 所做的更改

路由器只向版本 0.9.47 或更高的客户端发送此消息。

### 支持离线密钥的更改

客户端不对此消息回复。

## 需要更改私钥文件

Meta 重定向消息的消息类型为 43。

需要进行修改，以存储临时公钥和离线签名信息。

### 变更

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
### 私钥文件 CLI 所需变更

添加对以下选项的支持：

```
-d days              (specify expiration in days of offline sig, default 365)
      -o offlinedestfile   (generate the online key file,
                            using the offline key file specified)
      -r sigtype           (specify sig type of transient key, default Ed25519)
```
## 需要进行的流传输变更

目前无法在 streaming 中验证离线签名。下面的更改将离线签名块添加到选项中。这样就不必通过 I2CP 获取此信息。

### 变更

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
### 说明

- 新格式 b32 地址（“b33”）的主机查找  
  告诉路由器地址被盲化，但没有机制在主机查找消息中  
  传递密钥或私钥给路由器。  
  虽然我们可以扩展主机查找消息以添加该信息，  
  但定义新消息更清晰。

## 可回复数据报所需更改

在可回复数据报处理中无法验证离线签名。需要一个标志来指示离线签名，但没有地方放置该标志。这将需要全新的协议号和格式。

### 变更

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
### 说明

- 我们需要客户端告诉路由器的程序化方式。  
  否则，用户必须手动配置每个目的地。

## 所需的 SAM V3 更改

必须增强 SAM，使其支持 DESTINATION base 64 中的离线签名。

### 变更

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
请注意，离线签名仅支持 STREAM 和 RAW，不支持 DATAGRAM（除非我们定义一个新的 DATAGRAM 协议）。

请注意，SESSION STATUS 将返回全零的 Signing Private Key，以及完全按照 SESSION CREATE 中所提供内容返回的 Offline Signature 数据。

请注意，DEST GENERATE 和 SESSION CREATE DESTINATION=TRANSIENT 不能用于创建离线签名的 destination。

### 问题

将版本号提升到 3.4，还是保留在 3.1/3.2/3.3，以便无需所有 3.2/3.3 的内容也能添加？

其他更改待定。请参见上文的 I2CP Host Reply Message 部分。

## BOB 所需的变更

BOB 需要增强以支持离线签名和/或 Meta LS。此项优先级较低，可能永远不会被规范或实现。SAM V3 是首选接口。

## 发布、迁移、兼容性

LS2（加密 LS2 除外）与 LS1 发布在相同的 DHT 位置。无法同时发布 LS1 和 LS2，除非 LS2 位于不同的位置。

Encrypted LS2 会发布在 blinded key type 与 key data 的哈希处。随后该哈希用于生成每日的“routing key”，与 LS1 中相同。

仅当需要新功能（新加密、加密 LS、meta 等）时才会使用 LS2。LS2 只能发布到指定版本或更高版本的 floodfill。

发布 LS2 的服务器会知道，任何连接的客户端都支持 LS2。它们可以在 garlic 中发送 LS2。

客户端只有在使用新加密时才会在 garlics 中发送 LS2。共享客户端会无限期地使用 LS1？TODO：如何让共享客户端同时支持旧加密和新加密？

## 推出

0.9.38 包含对标准 LS2 的 floodfill 支持，包括离线密钥。

0.9.39 包含对 LS2 和 Encrypted LS2 的 I2CP 支持、sig type 11 签名/验证、floodfill 对 Encrypted LS2 的支持（sig types 7 和 11，不含离线密钥），以及 LS2 的加密/解密（不含按客户端授权）。

0.9.40 计划包含：支持按客户端授权的 LS2 加密/解密，floodfill 和 I2CP 对 Meta LS2 的支持，对带离线密钥的加密 LS2 的支持，以及对加密 LS2 的 b32 支持。

## 致谢

加密的 LS2 设计深受 [Tor 的 v3 隐藏服务描述符](https://spec.torproject.org/rend-spec-v3) 的影响，后者具有类似的设计目标。

## 参考资料

- 最低路由器版本为 0.9.43
