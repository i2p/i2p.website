---
title: "ChaCha 隧道层加密"
number: "153"
author: "chisana"
created: "2019-08-04"
lastupdated: "2019-08-05"
status: "Open"
thread: "http://zzz.i2p/topics/2753"
toc: true
---

## 概述

本提案基于提案152：ECIES隧道，并要求进行相应的更改。

只有通过支持ECIES-X25519隧道的BuildRequestRecord格式建立的隧道才能实现此规范。

此规范要求使用隧道构建选项格式来指示隧道层加密类型并传输层AEAD密钥。

### 目标

本提案的目标是：

- 用ChaCha20替换AES256/ECB+CBC，用于建立的隧道IV和层加密
- 使用ChaCha20-Poly1305进行跃点间AEAD保护
- 对于非隧道参与者，不可从现有隧道层加密中检测出
- 不对整体隧道消息长度进行任何更改

### 已建立的隧道消息处理

本节描述以下方面的更改：

- 出站和入站网关预处理和加密
- 参与者加密和后处理
- 出站和入站端点加密和后处理

有关当前隧道消息处理的概述，请参见 [Tunnel Implementation](/docs/tunnels/implementation/) 规范。

仅讨论支持ChaCha20层加密的路由器的更改。

在没有制定出将128位AES IV转换为64位ChaCha20随机数的安全协议之前，不考虑混合隧道的AES层加密的任何更改。Bloom过滤器可保证整个IV的唯一性，但唯一IV的前半部分可能是相同的。

这意味着层加密必须在隧道中的所有跃点中是相同的，并在隧道创建过程中使用隧道构建选项进行建立。

所有网关和隧道参与者都需要维护一个Bloom过滤器，以验证两个独立随机数。

本提案中提到的``nonceKey``取代了AES层加密中使用的``IVKey``。它是使用提案152中的相同KDF生成的。

### 跃点间消息的AEAD加密

需要为每对连续的跃点生成一个独特的``AEADKey``。
连续跃点将使用此密钥对内部ChaCha20加密隧道消息进行ChaCha20-Poly1305加解密。

隧道消息需要将内部加密帧长度减少16字节，以容纳Poly1305 MAC。

消息不能直接使用AEAD，因为出站隧道需要迭代解密。
只有在当前方式中使用ChaCha20而没有AEAD才能实现迭代解密。

```text
+----+----+----+----+----+----+----+----+
  |    隧道 ID      |   隧道随机数     |
  +----+----+----+----+----+----+----+----+
  | 隧道随机数 cont. |    混淆随机数      |
  +----+----+----+----+----+----+----+----+
  |  混淆随机数 cont.  |                   |
  +----+----+----+----+                   +
  |                                       |
  +           加密数据              +
  ~                                       ~
  |                                       |
  +                   +----+----+----+----+
  |                   |    Poly1305 MAC   |
  +----+----+----+----+                   +  
  |                                       |
  +                   +----+----+----+----+
  |                   |
  +----+----+----+----+

  隧道 ID :: `TunnelId`
         4 字节
         下一跃点的ID

  隧道随机数 ::
         8 字节
         隧道层随机数

  混淆随机数 ::
         8 字节
         隧道层随机数加密随机数

  加密数据 ::
         992 字节
         加密的隧道消息

  Poly1305 MAC ::
         16 字节

  总大小：1028字节
```

中间跃点（具有前后跃点），将有两个``AEADKeys``，一个用于解密前一个跃点的AEAD层，一个用于加密到下一个跃点的AEAD层。

所有中间跃点参与者因此将在其BuildRequestRecords中包含额外64字节的密钥材料。

出站端点和入站网关仅需额外32字节的密钥数据，因为它们之间不进行隧道层加密消息。

出站网关生成其``outAEAD``密钥，该密钥与第一个出站跃点的``inAEAD``密钥相同。

入站端点生成其``inAEAD``密钥，该密钥与最后一个入站跃点的``outAEAD``密钥相同。

中间跃点将接收一个``inAEADKey``和一个``outAEADKey``，分别用于解密接收到的消息和加密发送的消息。

例如，在具有中间跃点的隧道中：OBGW、A、B、OBEP：

- A的``inAEADKey``与OBGW的``outAEADKey``相同
- B的``inAEADKey``与A的``outAEADKey``相同
- B的``outAEADKey``与OBEP的``inAEADKey``相同

密钥是跳对特有的，所以OBEP的``inAEADKey``与A的``inAEADKey``不同，A的``outAEADKey``与B的``outAEADKey``不同，依此类推。

### 网关和隧道创建者消息处理

网关将以相同方式分片和捆绑消息，为指令-片段帧后的Poly1305 MAC保留空间。

包含AEAD帧（包括MAC）的内部I2NP消息可以跨片段分割，但任何丢失的片段将导致在端点处AEAD解密失败（MAC验证失败）。

### 网关预处理和加密

当隧道支持ChaCha20层加密时，网关将为每组消息生成两个64位随机数。

入站隧道：

- 使用ChaCha20加密IV和隧道消息
- 使用8字节的``tunnelNonce``和``obfsNonce``，鉴于隧道的生命周期
- 使用8字节``obfsNonce``来加密``tunnelNonce``
- 在2^(64 - 1) - 1组消息前销毁隧道：2^63 - 1 = 9,223,372,036,854,775,807

  - 限制随机数（nonce）数量，以避免64位随机数冲突
  - 随机数限制几乎不可能达到，因为这将超过每秒~15,372,286,728,091,294条消息，持续10分钟的隧道

- 根据预期元素数量调整Bloom过滤器的调谐（128条消息/秒，1024条消息/秒？待定）

隧道的入站网关（IBGW）处理从另一个隧道的出站端点（OBEP）接收到的消息。

此时，外层消息通过点对点传输加密。I2NP消息头在隧道层对OBEP和IBGW是可见的。内部I2NP消息被包装在使用端到端会话加密的Garlic cloves中。

IBGW将消息预处理成适当格式的隧道消息，并加密如下：

```text

// IBGW生成随机随机数，确保其Bloom过滤器中的每个随机数不冲突
  tunnelNonce = Random(len = 64-bits)
  obfsNonce = Random(len = 64-bits)
  // IBGW使用其tunnelNonce和layerKey对每个预处理的隧道消息进行ChaCha20“加密”
  encMsg = ChaCha20(msg = tunnel msg, nonce = tunnelNonce, key = layerKey)

  // 使用tunnelNonce和outAEADKey对每个消息的加密数据帧进行ChaCha20-Poly1305加密
  (encMsg, MAC) = ChaCha20-Poly1305-Encrypt(msg = encMsg, nonce = tunnelNonce, key = outAEADKey)
```

隧道消息格式将略微更改，使用两个8字节的随机数代替16字节的IV。
用于加密随机数的``obfsNonce``附加到8字节的``tunnelNonce``，
并由每个跃点使用加密的``tunnelNonce``和跃点的``nonceKey``加密。

在所有跃点预先解密消息集后，出站网关
使用``tunnelNonce``和其``outAEADKey``对每个隧道消息的密文部分进行ChaCha20-Poly1305 AEAD加密。

出站隧道：

- 迭代解密隧道消息
- ChaCha20-Poly1305对预先解密的隧道消息加密帧进行加密
- 使用与入站隧道相同的规则生成层随机数
- 每组发送的隧道消息生成一次随机数

```text

// 对于每组消息，生成唯一的随机数
  tunnelNonce = Random(len = 64-bits)
  obfsNonce = Random(len = 64-bits)

  // 对于每个跃点，使用当前跃点的IV密钥对前一个tunnelNonce进行ChaCha20
  tunnelNonce = ChaCha20(msg = prev. tunnelNonce, nonce = obfsNonce, key = hop's nonceKey)

  // 对于每个跃点，使用当前跃点的tunnelNonce和layerKey对隧道消息进行ChaCha20“解密”
  decMsg = ChaCha20(msg = tunnel msg(s), nonce = tunnelNonce, key = hop's layerKey)

  // 对于每个跃点，使用当前跃点的加密tunnelNonce和nonceKey对obfsNonce进行ChaCha20“解密”
  obfsNonce = ChaCha20(msg = obfsNonce, nonce = tunnelNonce, key = hop's nonceKey)

  // 在跃点处理后，使用第一跃点的加密tunnelNonce和inAEADKey对每个隧道消息的“解密”的数据帧进行ChaCha20-Poly1305加密
  (encMsg, MAC) = ChaCha20-Poly1305-Encrypt(msg = decMsg, nonce = first hop's encrypted tunnelNonce, key = first hop's inAEADKey / GW outAEADKey)
```

### 参与者处理

参与者将以相同方式追踪看到的消息，使用衰减的Bloom过滤器。

每个跃点需对接收的隧道随机数进行一次加密，以防止非连续勾结跃点的确认攻击。

跃点将加密接收到的随机数，以防止先前和后续跃点之间的确认攻击，
即勾结的非连续跃点能够识别它们属于同一隧道。

为了验证接收到的``tunnelNonce``和``obfsNonce``，参与者分别检查每个随机数在Bloom过滤器中的重复性。

验证后，参与者：

- 使用接收到的``tunnelNonce``和其``inAEADKey``对每个隧道消息的AEAD密文进行ChaCha20-Poly1305解密
- 使用其``nonceKey``和接收到的``obfsNonce``对``tunnelNonce``进行ChaCha20加密
- 使用加密的``tunnelNonce``和其``layerKey``对每个隧道消息的加密数据帧进行ChaCha20加密
- 使用加密的``tunnelNonce``和其``outAEADKey``对每个隧道消息的加密数据帧进行ChaCha20-Poly1305加密
- 使用其``nonceKey``和加密的``tunnelNonce``对``obfsNonce``进行ChaCha20加密
- 将{``nextTunnelId``，加密的（``tunnelNonce`` || ``obfsNonce``），AEAD密文 || MAC}元组发送到下一个跃点。

```text

// 为了验证，隧道跃点应检查Bloom过滤器以确保每个接收到的随机数的唯一性
  // 验证后，使用接收到的tunnelNonce和inAEADKey解开AEAD帧
  encTunMsg = ChaCha20-Poly1305-Decrypt(msg = received encMsg \|\| MAC, nonce = received tunnelNonce, key = inAEADKey)

  // 使用obfsNonce和跃点的nonceKey对tunnelNonce进行ChaCha20加密
  tunnelNonce = ChaCha20(msg = received tunnelNonce, nonce = received obfsNonce, key = nonceKey)

  // 使用加密的tunnelNonce和跃点的layerKey对每个隧道消息的加密数据帧进行ChaCha20加密
  encMsg = ChaCha20(msg = encTunMsg, nonce = tunnelNonce, key = layerKey)

  // 为了AEAD保护，还使用加密的tunnelNonce和跃点的outAEADKey对每条消息的加密数据帧进行ChaCha20-Poly1305加密
  (encMsg, MAC) = ChaCha20-Poly1305-Encrypt(msg = encMsg, nonce = tunnelNonce, key = outAEADKey)

  // 使用加密的tunnelNonce和跃点的nonceKey对接收的obfsNonce进行ChaCha20加密
  obfsNonce = ChaCha20(msg = obfsNonce, nonce = tunnelNonce, key = nonceKey)
```

### 入站端点处理

对于ChaCha20隧道，将使用以下方案来解密每条隧道消息：

- 独立验证接收到的``tunnelNonce``和``obfsNonce``，以避免在其Bloom过滤器中的重复性
- 使用接收到的``tunnelNonce``和``inAEADKey``对加密数据帧进行ChaCha20-Poly1305解密
- 使用接收到的``tunnelNonce``和跃点的``layerKey``对加密数据帧进行ChaCha20解密
- 使用跃点的``nonceKey``和接收到的``tunnelNonce``对``obfsNonce``进行ChaCha20解密，以获得前一个``obfsNonce``
- 使用跃点的``nonceKey``和解密的``obfsNonce``对接收到的``tunnelNonce``进行ChaCha20解密，以获得前一个``tunnelNonce``
- 使用解密的``tunnelNonce``和前一跃点的``layerKey``对加密数据进行ChaCha20解密
- 重复对隧道中每个跃点的随机数和层解密的步骤，直到返回到IBGW
- AEAD帧解密仅需要在第一轮中进行

```text

// 在第一轮中，使用接收到的tunnelNonce和inAEADKey对每个消息的加密数据帧和MAC进行ChaCha20-Poly1305解密
  msg = encTunMsg \|\| MAC
  tunnelNonce = received tunnelNonce
  encTunMsg = ChaCha20-Poly1305-Decrypt(msg, nonce = tunnelNonce, key = inAEADKey)

  // 对隧道返回到IBGW的每个跃点重复
  // 在每轮中，使用上一轮解密的tunnelNonce对每条消息的加密数据帧进行ChaCha20解密
  decMsg = ChaCha20(msg = encTunMsg, nonce = tunnelNonce, key = layerKey)
  obfsNonce = ChaCha20(msg = obfsNonce, nonce = tunnelNonce, key = nonceKey)
  tunnelNonce = ChaCha20(msg = tunnelNonce, nonce = obfsNonce, key = nonceKey)
```

### 使用ChaCha20+ChaCha20-Poly1305的隧道层加密的安全分析

从AES256/ECB+AES256/CBC转换为ChaCha20+ChaCha20-Poly1305具有一些优点，并产生新安全考量。

最大的安全考量是，ChaCha20和ChaCha20-Poly1305的随机数对每条消息来说必须是唯一的，并且密钥的整个生命周期内必须如此。

未能在使用相同密钥的不同消息上使用唯一的随机数将破坏ChaCha20和ChaCha20-Poly1305。

使用附加的``obfsNonce``允许IBEP解密每个跃点层加密的``tunnelNonce``，恢复先前的随机数。

与``tunnelNonce``一同的``obfsNonce``不向隧道跃点透露任何新信息，因为``obfsNonce``是使用加密的``tunnelNonce``进行加密的。这还允许IBEP以类似于``tunnelNonce``恢复的方式恢复之前的``obfsNonce``。

最大的安全优势是，对ChaCha20没有确认攻击或Oracle攻击，而使用ChaCha20-Poly1305的跃点之间增加了针对密文篡改的AEAD保护，防止带外的中间人攻击。

对于重新使用密钥的AES256/ECB + AES256/CBC（如隧道层加密时）存在实际的Oracle攻击。

对AES256/ECB的Oracle攻击不起作用，因为使用了双重加密，并且加密是单个块（隧道IV）。

对AES256/CBC的填充Oracle攻击不起作用，因为没有使用填充。如果隧道消息长度发生更改至非mod-16长度，AES256/CBC仍不会因不接受重复的IV而受影响。

通过不允许使用相同IV进行多次Oracle调用，这两种攻击也被阻止，因为重复的IV被拒绝。

## 参考

* [Tunnel-Implementation](/docs/tunnels/implementation/)
