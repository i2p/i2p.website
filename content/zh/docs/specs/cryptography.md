---
title: "底层密码学规范"
description: "I2P中使用的密码学算法的底层详细信息"
slug: "cryptography"
aliases:
  - "/zh/how_cryptography"
  - "/zh/how_cryptography/"
category: "设计"
lastUpdated: "2025-05"
accurateFor: "0.9.66"
---

## 概述

> **注意：** 本文档大部分已过时。请参阅以下文档了解当前规范： > - [ECIES](/docs/specs/ecies) > - [Encrypted LeaseSet](/docs/specs/encryptedleaseset) > - [NTCP2](/docs/specs/ntcp2) > - [Red25519](/docs/specs/red25519) > - [SSU2](/docs/specs/ssu2) > - [Tunnel Creation (ECIES)](/docs/specs/tunnel-creation-ecies)

本页面详细说明了I2P中密码学的底层技术细节。

I2P内部使用了多种密码学算法。在I2P的最初设计中，每种类型只有一个算法 - 一个对称算法、一个非对称算法、一个签名算法和一个哈希算法。当时没有提供添加更多算法或迁移到更安全算法的机制。

近年来，我们添加了一个框架来以向后兼容的方式支持多种原语和组合。通过"签名类型"定义了众多具有不同密钥和签名长度的签名算法。通过"加密类型"定义了使用非对称和对称加密组合、具有不同密钥长度的端到端加密方案。

I2P 中的各种协议和数据结构包含用于指定签名类型和/或加密类型的字段。这些字段与类型定义一起，定义了密钥和签名长度以及使用它们所需的加密原语。签名和加密类型的定义在[通用结构规范](/docs/specs/common-structures)中。

原始的 I2P 协议 NTCP、SSU 和 ElGamal/AES+SessionTags 使用 ElGamal 非对称加密和 AES 对称加密的组合。较新的协议 NTCP2 和 ECIES-X25519-AEAD-Ratchet 使用 X25519 密钥交换和 ChaCha20/Poly1305 对称加密的组合。

- ECIES-X25519-AEAD-Ratchet 已替换 ElGamal/AES+SessionTags。
- NTCP2 已替换 NTCP。
- SSU2 已替换 SSU。
- X25519 tunnel 创建已替换 ElGamal tunnel 创建。

## 非对称加密

I2P中的原始非对称加密算法是ElGamal。较新的算法是ECIES X25519 DH密钥交换，在多个地方使用。

我们正在将所有 ElGamal 使用迁移到 X25519。

NTCP (使用 ElGamal) 已迁移到 NTCP2 (使用 X25519)。ElGamal/AES+SessionTag 正在迁移到 ECIES-X25519-AEAD-Ratchet。

### X25519

有关 X25519 使用的详细信息，请参阅 [NTCP2](/docs/specs/ntcp2) 和 [ECIES](/docs/specs/ecies)。

### ElGamal

ElGamal在I2P中的多个地方被使用：

- 用于加密 router 到 router 的 TunnelBuild 消息
- 用于端到端（destination 到 destination）加密，作为 ElGamal/AES+SessionTag 的一部分，使用 LeaseSet 中的加密密钥
- 用于加密发送到 floodfill router 的一些 netDb 存储和查询，作为 ElGamal/AES+SessionTag 的一部分（destination 到 router 或 router 到 router）。

我们使用 IETF [RFC-3526](http://tools.ietf.org/html/rfc3526) 给出的通用素数进行 2048 位 ElGamal 加密和解密。我们目前只使用 ElGamal 在单个块中加密 IV 和会话密钥，然后使用该密钥和 IV 进行 AES 加密载荷。

未加密的 ElGamal 包含：

```
+----+----+----+----+----+----+----+----+
|nonz|           H(data)                |
+----+                                  +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+----+----+----+
|    |  data...
+----+----+----+-//
```
H(data) 是对 ElGamal 块中加密数据的 SHA256 哈希值，前面有一个随机的非零字节。从 0.9.28 版本开始，这个字节是真正随机的；在此之前它总是 0xFF。将来可能会用于标志位。块中加密的数据最多可以有 222 字节长。由于如果明文小于 222 字节，加密数据可能包含大量的零，建议上层协议用随机数据将明文填充到 222 字节。总长度：通常为 255 字节。

加密的 ElGamal 包含：

```
+----+----+----+----+----+----+----+----+
|  zero padding...       |              |
+----+----+----+-//-+----+              +
|                                       |
+                                       +
|       ElG encrypted part 1            |
~                                       ~
|                                       |
+    +----+----+----+----+----+----+----+
|    |   zero padding...      |         |
+----+----+----+----+-//-+----+         +
|                                       |
+                                       +
|       ElG encrypted part 2            |
~                                       ~
|                                       |
+         +----+----+----+----+----+----+
|         +
+----+----+
```
每个加密部分都会在前面填充零，使其大小恰好为 257 字节。总长度：514 字节。在典型使用情况下，更高层会将明文数据填充到 222 字节，从而产生 255 字节的未加密块。这被编码为两个 256 字节的加密部分，并且在此层的每个部分前都有一个字节的零填充。

请参阅 ElGamal 代码 [ElGamalEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/ElGamalEngine.java)。

共享素数是用于 2048 位密钥的 Oakley 素数 [RFC-3526-S3](http://tools.ietf.org/html/rfc3526#section-3)：

```
2^2048 - 2^1984 - 1 + 2^64 * { [2^1918 pi] + 124476 }
```
或作为十六进制值：

```
FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1
29024E08 8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD
EF9519B3 CD3A431B 302B0A6D F25F1437 4FE1356D 6D51C245
E485B576 625E7EC6 F44C42E9 A637ED6B 0BFF5CB6 F406B7ED
EE386BFB 5A899FA5 AE9F2411 7C4B1FE6 49286651 ECE45B3D
C2007CB8 A163BF05 98DA4836 1C55D39A 69163FA8 FD24CF5F
83655D23 DCA3AD96 1C62F356 208552BB 9ED52907 7096966D
670C354E 4ABC9804 F1746C08 CA18217C 32905E46 2E36CE3B
E39E772C 180E8603 9B2783A2 EC07A28F B5C55DF0 6F4C52C9
DE2BCBF6 95581718 3995497C EA956AE5 15D22618 98FA0510
15728E5A 8AACAA68 FFFFFFFF FFFFFFFF
```
使用 2 作为生成元。

#### 短指数 {#exponent}

虽然标准指数大小为2048位（256字节），I2P PrivateKey为完整的256字节，但在某些情况下我们使用226位（28.25字节）的短指数大小。这对于与Oakley素数一起使用应该是安全的[vanOorschot1996] [BENCHMARKS]。

此外，根据这个 sci.crypt 讨论串 [SCI.CRYPT]，[Koshiba2004] 显然也支持这一点。PrivateKey 的其余部分用零填充。

在0.9.8版本之前，所有router都使用短指数。从0.9.8版本开始，64位x86 router使用完整的2048位指数。现在所有router都使用完整指数，除了少数运行在极慢硬件上的router，由于担心处理器负载问题，它们仍然使用短指数。对于这些平台转换到更长指数的问题仍需进一步研究。

#### 过时性

需要研究网络对 ElGamal 攻击的脆弱性以及过渡到更长位长度的影响。要使任何更改保持向后兼容性可能会相当困难。

## 对称加密

I2P 中原始的对称加密算法是 AES。较新的算法是 Authenticated Encryption with Associated Data (AEAD) ChaCha20/Poly1305，在多个地方使用。

我们正在将所有 AES 使用迁移到 ChaCha20/Poly1305。

NTCP（使用 AES）已迁移到 NTCP2（使用 ChaCha20/Poly1305）。ElGamal/AES+SessionTag 正在迁移到 ECIES-X25519-AEAD-Ratchet。

### ChaCha20/Poly1305

有关 ChaCha20/Poly1305 使用的详细信息，请参见 [NTCP2](/docs/specs/ntcp2) 和 [ECIES](/docs/specs/ecies)。

### AES

AES 用于对称加密，在以下几种情况下：

- 用于 SSU 传输加密（参见"传输"章节）在 DH 密钥交换之后
- 用于端到端（目标到目标）加密，作为 ElGamal/AES+SessionTag 的一部分
- 用于加密发送到 floodfill router 的一些 netDb 存储和查询，作为 ElGamal/AES+SessionTag 的一部分（目标到 router 或 router 到 router）。
- 用于加密从 router 发送给自身的周期性 tunnel 测试消息，通过其自身的 tunnel。

我们使用AES加密，采用256位密钥和128位分组，工作模式为CBC。所使用的填充方式按照IETF [RFC-2313](http://tools.ietf.org/html/rfc2313)规范（PKCS#5 1.5，第8.1节（针对块类型02））。在这种情况下，填充由伪随机生成的八位字节组成，以匹配16字节分组。具体来说，请参阅CBC代码[CryptixAESEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/CryptixAESEngine.java)和Cryptix AES实现[CryptixRijndael_Algorithm](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/CryptixRijndael_Algorithm.java)，以及ElGamalAESEngine.getPadding函数中的填充实现[ElGamalAESEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/ElGamalAESEngine.java)。

#### 废弃

需要研究网络对AES攻击的脆弱性以及转向更长位长度的影响。使任何更改向后兼容可能相当困难。

## 签名 {#sig}

签名类型定义了众多签名算法，具有不同的密钥和签名长度。添加更多签名类型相对容易。

EdDSA-SHA512-Ed25519 是当前默认的签名算法。DSA 是我们添加签名类型支持之前的原始算法，目前仍在网络中使用。

### DSA

签名使用1024位[DSA](http://en.wikipedia.org/wiki/Digital_Signature_Algorithm)(L=1024, N=160)生成和验证，具体实现见[DSAEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/DSAEngine.java)。选择DSA是因为它在签名方面比ElGamal快得多。

#### 种子

160 位:

```
86108236b8526e296e923a4015b4282845b572cc
```
#### 计数器

```
33
```
#### DSA 素数 (p)

1024 位:

```
9C05B2AA 960D9B97 B8931963 C9CC9E8C 3026E9B8 ED92FAD0
A69CC886 D5BF8015 FCADAE31 A0AD18FA B3F01B00 A358DE23
7655C496 4AFAA2B3 37E96AD3 16B9FB1C C564B5AE C5B69A9F
F6C3E454 8707FEF8 503D91DD 8602E867 E6D35D22 35C1869C
E2479C3B 9D5401DE 04E0727F B33D6511 285D4CF2 9538D9E3
B6051F5B 22CC1C93
```
#### DSA 商数 (q)

```
A5DFC28F EF4CA1E2 86744CD8 EED9D29D 684046B7
```
#### DSA 生成元 (g)

1024 位：

```
0C1F4D27 D40093B4 29E962D7 223824E0 BBC47E7C 832A3923
6FC683AF 84889581 075FF908 2ED32353 D4374D73 01CDA1D2
3C431F46 98599DDA 02451824 FF369752 593647CC 3DDC197D
E985E43D 136CDCFC 6BD5409C D2F45082 1142A5E6 F8EB1C3A
B5D0484B 8129FCF1 7BCE4F7F 33321C3C B3DBB14A 905E7B2B
3E93BE47 08CBCC82
```
SigningPublicKey 是 1024 位。SigningPrivateKey 是 160 位。

#### 过时性

[NIST-800-57](http://csrc.nist.gov/publications/nistpubs/800-57/sp800-57-Part1-revised2_Mar08-2007.pdf) 建议在2010年之后使用最小值为(L=2048, N=224)。这可以通过"密钥周期"或给定密钥的生命周期在一定程度上得到缓解。

这个质数是在2003年选择的，选择这个数字的人（TheCrypto）目前已不再是I2P开发者。因此，我们不知道所选择的质数是否为"强质数"。如果将来出于某种目的选择更大的质数，那应该是一个强质数，并且我们会记录构造过程。

## 新的签名算法

从0.9.12版本开始，router支持比1024位DSA更安全的额外签名算法。首次使用是针对Destinations；对Router Identities的支持在0.9.16版本中添加。现有的Destinations无法从旧签名迁移到新签名；但是，支持单个tunnel使用多个Destinations，这提供了一种切换到较新签名类型的方法。签名类型编码在Destination和Router Identity中，因此可以随时添加新的签名算法或曲线。

当前支持的签名类型如下：

- DSA-SHA1
- ECDSA-SHA256-P256
- ECDSA-SHA384-P384（未被广泛使用）
- ECDSA-SHA512-P521（未被广泛使用）
- EdDSA-SHA512-Ed25519（自 0.9.15 版本起为默认）
- RedDSA-SHA512-Ed25519（自 0.9.39 版本起）

其他签名类型仅在应用层使用，主要用于签名和验证su3文件。这些签名类型如下：

- RSA-SHA256-2048（未广泛使用）
- RSA-SHA384-3072（未广泛使用）
- RSA-SHA512-4096
- EdDSA-SHA512-Ed25519ph（自0.9.25版本起；未广泛使用）

### ECDSA

ECDSA 使用标准的 NIST 曲线和标准的 SHA-2 哈希。

我们在 0.9.16 - 0.9.19 发布时间框架内将新目的地迁移到 ECDSA-SHA256-P256。从 0.9.16 版本开始支持 Router Identity 的使用，现有 router 的迁移发生在 2015 年。

### RSA

标准 RSA PKCS#1 v1.5 (RFC 2313)，使用公共指数 F4 = 65537。

RSA现在用于签署所有带外可信内容，包括router更新、重新播种、插件和新闻。签名嵌入在"su3"格式中[UPDATES]。推荐使用4096位密钥，所有已知签名者都使用这种密钥长度。RSA不用于、也不计划用于任何网络内Destination或Router Identity。

### EdDSA 25519

使用 curve 25519 和标准 512 位 SHA-2 哈希的标准 EdDSA。

从 0.9.15 版本开始支持。

Destinations 和 Router Identities 在2015年末进行了迁移。

### RedDSA 25519

使用curve 25519和标准512位SHA-2哈希的标准EdDSA，但使用不同的私钥，并对签名进行了少量修改。用于加密的leaseSet。详情请参见[EncryptedLeaseSet](/docs/specs/encryptedleaseset)和[Red25519](/docs/specs/red25519)。

从 0.9.39 版本开始支持。

## 哈希值

哈希用于签名算法和作为网络DHT中的密钥。

较旧的签名算法使用 SHA1 和 SHA256。较新的签名算法使用 SHA512。DHT 使用 SHA256。

### SHA256

I2P 中的 DHT 哈希值使用标准的 SHA256。

#### 废弃

需要研究网络对SHA-256攻击的脆弱性以及过渡到更长哈希的影响。要使任何更改都向后兼容可能会相当困难。

## 传输协议

在最底层协议层，router 之间的点对点通信由传输层安全保护。

NTCP2 连接使用 X25519 Diffie-Hellman 和 ChaCha20/Poly1305 认证加密。

SSU 和已过时的 NTCP 传输协议使用 256 字节（2048 位）Diffie-Hellman 密钥交换，使用与上述 ElGamal 相同的共享质数和生成元，然后使用如上所述的对称 AES 加密。

SSU 计划迁移到 SSU2（使用 X25519 和 ChaCha20/Poly1305）。

所有传输方式都在传输链路上提供完全前向保密性 [PFS](http://en.wikipedia.org/wiki/Perfect_forward_secrecy)。

### NTCP2 连接 {#tcp}

NTCP2 连接使用 X25519 Diffie-Hellman 和 ChaCha20/Poly1305 认证加密，以及 Noise 协议框架 [Noise](https://noiseprotocol.org/noise.html)。

详细信息和参考资料请参见 NTCP2 规范 [NTCP2](/docs/specs/ntcp2)。

### UDP 连接 {#udp}

SSU（UDP 传输）在通过 2048 位 Diffie-Hellman 交换协商临时会话密钥后，使用 AES256/CBC 对每个数据包进行加密，同时使用显式 IV 和 MAC（HMAC-MD5-128），并通过与其他 router 的 DSA 密钥进行站到站身份验证，此外每个网络消息都有自己的哈希值用于本地完整性检查。

详情请参阅 SSU 规范。

警告 - I2P在SSU中使用的HMAC-MD5-128显然不是标准的。显然，SSU的早期版本使用了HMAC-SHA256，然后出于性能考虑切换到了MD5-128，但保留了32字节的缓冲区大小不变。详情请参见HMACGenerator.java和2005-07-05状态说明。

### NTCP 连接

NTCP 已不再使用，它已被 NTCP2 取代。

NTCP 连接通过 2048 位 Diffie-Hellman 实现进行协商，使用 router 的身份来进行站对站协议，然后是一些加密的协议特定字段，所有后续数据都使用 AES 加密（如上所述）。使用 DH 协商而不是 ElGamalAES+SessionTag 的主要原因是它提供了"（完全）前向保密性"[PFS](http://en.wikipedia.org/wiki/Perfect_forward_secrecy)，而 ElGamalAES+SessionTag 则不提供。

## 参考资料

- [BENCHMARKS](https://web.archive.org/web/20080423000000*/http://www.eskimo.com/~weidai/benchmarks.html) - Crypto++ 基准测试，原始链接为 http://www.eskimo.com/~weidai/benchmarks.html（现已失效），从 http://www.archive.org/ 救回，日期为 2008 年 4 月 23 日。
- [Common](/docs/specs/common-structures) - 通用结构规范
- [CryptixAESEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/CryptixAESEngine.java)
- [CryptixRijndael_Algorithm](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/CryptixRijndael_Algorithm.java)
- [DSA](http://en.wikipedia.org/wiki/Digital_Signature_Algorithm)
- [DSAEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/DSAEngine.java)
- [ECIES](/docs/specs/ecies)
- [ElGamalAESEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/ElGamalAESEngine.java)
- [ElGamalEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/ElGamalEngine.java)
- [EncryptedLeaseSet](/docs/specs/encryptedleaseset)
- [Koshiba2004](http://www.springerlink.com/content/2jry7cftp5bpdghm/) - Koshiba & Kurosawa. Short Exponent Diffie-Hellman Problems. PKC 2004, LNCS 2947, pp. 173-186
- [NIST-800-57](http://csrc.nist.gov/publications/nistpubs/800-57/sp800-57-Part1-revised2_Mar08-2007.pdf)
- [Noise](https://noiseprotocol.org/noise.html)
- [NTCP2](/docs/specs/ntcp2)
- [PFS](http://en.wikipedia.org/wiki/Perfect_forward_secrecy)
- [Red25519](/docs/specs/red25519)
- [RFC-2313](http://tools.ietf.org/html/rfc2313)
- [RFC-3526](http://tools.ietf.org/html/rfc3526)
- [RFC-3526-S3](http://tools.ietf.org/html/rfc3526#section-3)
- [SCI.CRYPT](https://groups.google.com/forum/#!topic/sci.crypt/GFWl76dBZnc)
- [SHA-2](https://en.wikipedia.org/wiki/SHA-2)
- [SSU2](/docs/specs/ssu2)
- [UPDATES](/docs/specs/updates)
- [vanOorschot1996](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.14.5952&rep=rep1&type=pdf) - van Oorschot, Weiner. On Diffie-Hellman Key Agreement with Short Exponents. EuroCrypt '96
