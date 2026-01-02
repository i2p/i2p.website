---
title: "从ECIES目标进行数据库查找"
number: "154"
author: "zzz"
created: "2020-03-23"
lastupdated: "2021-01-08"
status: "已关闭"
thread: "http://zzz.i2p/topics/2856"
target: "0.9.46"
implementedin: "0.9.46"
toc: true
---

## 注意
ECIES到ElG在0.9.46中已实现，并且提案阶段已关闭。
请参见[I2NP](/docs/specs/i2np/)以获取官方规范。
此提案仍可作为背景信息参考。
包含密钥的ECIES到ECIES已在0.9.48版中实现。
ECIES到ECIES（派生密钥）部分可能会在未来的提案中重新开放或合并。

## 概览

### 定义

- AEAD: ChaCha20/Poly1305
- DLM: I2NP数据库查找消息
- DSM: I2NP数据库存储消息
- DSRM: I2NP数据库搜索回复消息
- ECIES: ECIES-X25519-AEAD-Ratchet（提案144）
- ElG: ElGamal
- ENCRYPT(k, n, payload, ad): 如[ECIES](/docs/specs/ecies/)中定义
- LS: 租约集
- 查找: I2NP DLM
- 回复: I2NP DSM或DSRM

### 摘要

当发送针对LS的DLM到洪泛填充时，DLM通常指定回复被标签化，AES加密，并通过隧道发送到目的地。
对AES加密回复的支持已在0.9.7中添加。

在0.9.7中，指定AES加密回复是为了最小化ElG的巨大加密开销，并因为它复用了ElGamal/AES+SessionTags中的标签/AES工具。
然而，由于没有认证，并且这些回复不是前向保密的，AES回复可能在IBEP处被篡改。

对于[ECIES](/docs/specs/ecies/)目的地，提案144的目的是不再支持32字节标签和AES解密。
具体细节在该提案中有意未被包含。

此提案记录了一种请求ECIES加密回复的DLM的新选项。

### 目标

- 当请求加密回复通过隧道发送至ECIES目的地时，为DLM定义新标志
- 对于回复，添加前向保密和发送者认证以抵抗请求者（目的地）密钥泄露身份盗用（KCI）
- 保持请求者的匿名性
- 最小化加密开销

### 非目标

- 不改变查找（DLM）的加密或安全属性。
  查找仅对请求者密钥泄露具有前向保密性。
  加密是针对洪泛填充的静态密钥。
- 不对回复者（洪泛填充）的密钥泄露身份盗用（KCI）进行前向保密或发送者认证。
  洪泛填充是公共数据库，将响应来自任何人的查找请求。
- 在此提案中不设计ECIES路由器。
  路由器的X25519公钥去向尚待确定。

## 替代方案

在缺乏定义的加密方式回复ECIES目的地时，有几种替代方案：

1) 不请求加密回复。回复将是未加密的。
Java I2P目前使用这种方法。

2) 为仅ECIES目的地添加对32字节标签和AES加密回复的支持，并按照惯例请求AES加密回复。i2pd目前使用这种方法。

3) 按照惯例请求AES加密回复，但通过探测隧道将其路由回路由器。
Java I2P目前在某些情况下使用这种方法。

4) 对于双ElG和ECIES目的地，按照惯例请求AES加密回复。Java I2P目前使用这种方法。
i2pd尚未实现双加密目的地。

## 设计

- 新的DLM格式将在标志字段中添加一个位来指定ECIES加密回复。
  ECIES加密回复将使用[ECIES](/docs/specs/ecies/)现有会话消息格式，附加一个标签和ChaCha/Poly载荷和MAC。

- 定义两个变体。一个用于ElG路由器，其中DH操作不可用，另一个用于未来的ECIES路由器，其中DH操作可用并可能提供额外安全性。需要进一步研究。

由于ElG路由器不发布X25519公钥，因此其回复不可能进行DH。

## 规范

在[I2NP](/docs/specs/i2np/) DLM（DatabaseLookup）规范中，做出以下更改。

添加标志位4“ECIESFlag”以供新的加密选项使用。

```text
flags ::
       bit 4: ECIESFlag
               发行0.9.46之前被忽略
               从0.9.46版本开始：
               0  => 发送未加密或ElGamal回复
               1  => 使用包含的密钥发送ChaCha/Poly加密回复
                     （是否包括标签取决于第1位）
```

标志位4与第1位结合使用以确定回复加密模式。
标志位4仅可在向版本0.9.46或更高版本的路由器发送时设置。

在下表中，
“DH n/a”表示回复未加密。
“DH no”表示回复密钥已包含在请求中。
“DH yes”表示回复密钥是从DH操作中得出的。

=============  =========  =========  ======  ===  =======
Flag bits 4,1  From Dest  To Router  Reply   DH?  notes
=============  =========  =========  ======  ===  =======
0 0            Any        Any        no enc  n/a  current
0 1            ElG        ElG        AES     no   current
0 1            ECIES      ElG        AES     no   i2pd workaround
1 0            ECIES      ElG        AEAD    no   this proposal
1 0            ECIES      ECIES      AEAD    no   0.9.49
1 1            ECIES      ECIES      AEAD    yes  future
=============  =========  =========  ======  ===  =======

### ElG to ElG

ElG目的地向ElG路由器发送查找。

对规范的微小更改以检查新位4。
对现有二进制格式没有更改。

请求者密钥生成（澄清）：

```text
reply_key :: CSRNG(32) 32字节随机数据
  reply_tags :: 每个为CSRNG(32) 32字节随机数据
```

消息格式（添加ECIESFlag检查）：

```text
reply_key ::
       32字节 `SessionKey` 大端
       仅在加密Flag == 1 AND ECIESFlag == 0时包括，仅从发行版0.9.7开始

  tags ::
       1字节 `Integer`
       有效范围：1-32（通常为1）
       后随的回复标签数
       仅在加密Flag == 1 AND ECIESFlag == 0时包括，仅从发行版0.9.7开始

  reply_tags ::
       一个或多个32字节 `SessionTag`（通常一个）
       仅在加密Flag == 1 AND ECIESFlag == 0时包括，仅从发行版0.9.7开始
```

### ECIES to ElG

ECIES目的地向ElG路由器发送查找。
支持从0.9.46开始。

重新定义reply_key和reply_tags字段以用于ECIES加密回复。

请求者密钥生成：

```text
reply_key :: CSRNG(32) 32字节随机数据
  reply_tags :: 每个为CSRNG(8) 8字节随机数据
```

消息格式：
重新定义reply_key和reply_tags字段如下：

```text
reply_key ::
       32字节 ECIES `SessionKey` 大端
       仅在加密Flag == 0 AND ECIESFlag == 1时包括，仅从发行版0.9.46开始

  tags ::
       1字节 `Integer`
       必需值：1
       后随的回复标签数
       仅在加密Flag == 0 AND ECIESFlag == 1时包括，仅从发行版0.9.46开始

  reply_tags ::
       一个8字节 ECIES `SessionTag`
       仅在加密Flag == 0 AND ECIESFlag == 1时包括，仅从发行版0.9.46开始
```

回复是一个ECIES现有会话消息，如[ECIES](/docs/specs/ecies/)中定义。

```text
tag :: 8字节 reply_tag

  k :: 32字节 session key
     即reply_key。

  n :: 0

  ad :: 8字节 reply_tag

  payload :: 明文数据，DSM 或 DSRM。

  ciphertext = ENCRYPT(k, n, payload, ad)
```

### ECIES to ECIES (0.9.49)

ECIES目的地或路由器向ECIES路由器发送查找，附带回复密钥。
支持从0.9.49开始。

ECIES路由器在0.9.48中引入，参见[Prop156](/proposals/156-ecies-routers/)。
从0.9.49开始，ECIES目的地和路由器可以使用与上述“ECIES to ElG”部分相同的格式，在请求中包括回复密钥。
查找将使用[ECIES](/docs/specs/ecies/)中的“一次性格式”，因为请求者是匿名的。

对于使用派生密钥的新方法，请参见下一节。

### ECIES to ECIES (未来)

ECIES目的地或路由器向ECIES路由器发送查找，并从DH派生回复密钥。
尚未完全定义或支持，实现TBD。

查找将使用[ECIES](/docs/specs/ecies/)中的“一次性格式”，因为请求者是匿名的。

重新定义reply_key字段如下。没有关联的标签。
标签将在下面的KDF中生成。

此部分不完整，需要进一步研究。

```text
reply_key ::
       32字节X25519临时`PublicKey`的请求者，小端
       仅在加密Flag == 1 AND ECIESFlag == 1时包括，仅从发行版0.9.TBD开始
```

回复是一个ECIES现有会话消息，如[ECIES](/docs/specs/ecies/)中定义。
参见[ECIES](/docs/specs/ecies/)获取全部定义。

```text
// Alice的X25519临时密钥
  // aesk = Alice临时私钥
  aesk = GENERATE_PRIVATE()
  // aepk = Alice临时公钥
  aepk = DERIVE_PUBLIC(aesk)
  // Bob的X25519静态密钥
  // bsk = Bob私有静态密钥
  bsk = GENERATE_PRIVATE()
  // bpk = Bob公有静态密钥
  // bpk是RouterIdentity的一部分，或发布在RouterInfo中（TBD）
  bpk = DERIVE_PUBLIC(bsk)

  // (DH()
  //[chainKey, k] = MixKey(sharedSecret)
  // chainKey来自???
  sharedSecret = DH(aesk, bpk) = DH(bsk, aepk)
  keydata = HKDF(chainKey, sharedSecret, "ECIES-DSM-Reply1", 32)
  chainKey = keydata[0:31]

  1) rootKey = Payload Section的chainKey
  2) k 从New Session KDF或者split()

  // KDF_RK(rk, dh_out)
  keydata = HKDF(rootKey, k, "KDFDHRatchetStep", 64)

  // 输出1：未使用
  unused = keydata[0:31]
  // 输出2：初始化新会话标签和对称密钥棘轮
  // 用于Alice到Bob的传输
  ck = keydata[32:63]

  // 会话标签和对称密钥链密钥
  keydata = HKDF(ck, ZEROLEN, "TagAndKeyGenKeys", 64)
  sessTag_ck = keydata[0:31]
  symmKey_ck = keydata[32:63]

  tag :: 从[ECIES](/docs/specs/ecies/)中的RATCHET_TAG()生成的8字节标签

  k :: 从[ECIES](/docs/specs/ecies/)中的RATCHET_KEY()生成的32字节密钥

  n :: 标签的索引。通常为0。

  ad :: 8字节标签

  payload :: 明文数据，DSM或DSRM。

  ciphertext = ENCRYPT(k, n, payload, ad)
```

### 回复格式

这是现有的会话消息，与[ECIES](/docs/specs/ecies/)中相同，下面为参考复制。

```text
+----+----+----+----+----+----+----+----+
  |       会话标签                      |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +           负载部分                    +
  |       ChaCha20加密数据               |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305消息认证码                   |
  +              (MAC)                    +
  |             16字节                    |
  +----+----+----+----+----+----+----+----+

  会话标签 :: 8字节，明文

  负载部分加密数据 :: 剩余数据减去16字节

  MAC :: Poly1305消息认证码，16字节
```

## 正当性

查找消息中的回复加密参数，最早在0.9.7中引入，在层次结构上有些违背。
如此实现是为了效率。
但也因为查找是匿名的。

我们可以使查找格式通用化，例如使用加密类型字段，但这可能不是十分必要。

上述提案是最简单的并且对查找格式的更改最小化。

## 注意

向ElG路由器的数据库查找和存储必须按照惯例是ElGamal/AESSessionTag加密的。

## 问题

需要对两种ECIES回复选项的安全性进行进一步分析。

## 迁移

没有向后兼容性问题。路由器在其RouterInfo中宣布0.9.46或更高版本的router.version时必须支持此功能。
路由器不得向版本低于0.9.46的路由器发送包含新标志的DatabaseLookup。
如果误将带有第4位设定且第1位未设置的数据库查找消息发送给不支持的路由器，它可能会忽略提供的密钥和标签，并发送未加密的回复。
