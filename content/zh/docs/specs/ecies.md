---
title: "ECIES-X25519-AEAD-Ratchet 加密规范（棘轮机制）"
description: "适用于 I2P 的椭圆曲线集成加密方案 (X25519 + AEAD)"
slug: "ecies"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
toc: true
---

## 概览

### 目的

ECIES-X25519-AEAD-Ratchet 是 I2P 的现代端到端加密协议（基于 ECIES、X25519 与 AEAD，并采用 Ratchet（棘轮）机制），用于取代旧版 ElGamal/AES+SessionTags 系统（基于 ElGamal 与 AES 并使用 SessionTags 的旧方案）。它提供前向保密性、认证加密，并在性能和安全性方面带来显著改进。

### 相较于 ElGamal/AES+SessionTags（会话标签）的关键改进

- **更小的密钥**：32 字节密钥，对比 256 字节的 ElGamal 公钥（减少 87.5%）
- **前向保密性**：通过 DH（Diffie–Hellman）棘轮实现（旧协议不支持）
- **现代密码学**：X25519 DH，ChaCha20-Poly1305 AEAD（带关联数据的认证加密），SHA-256
- **认证加密**：通过 AEAD 构造内置认证
- **双向协议**：配对的入站/出站会话，对比单向的旧版协议
- **高效标签**：8 字节会话标签，对比 32 字节标签（减少 75%）
- **流量混淆**：Elligator2 编码（将椭圆曲线点伪装为随机比特串）使握手与随机数据不可区分

### 部署状态

- **初始发布**: 版本 0.9.46 (2020 年 5 月 25 日)
- **网络部署**: 截至 2020 年已完成
- **当前状态**: 成熟，已广泛部署 (在生产环境运行 5 年以上)
- **Router 支持**: 需要 0.9.46 或更高版本
- **Floodfill 要求 (netDb 中的洪泛节点)**: 加密查询需要接近 100% 的采用率

### 实现状态

**已完全实现:** - 带绑定的 New Session (NS) 消息 - New Session Reply (NSR) 消息 - Existing Session (ES) 消息 - DH ratchet 机制（基于 Diffie-Hellman 的棘轮） - Session tag 和 symmetric key 棘轮 - DateTime、NextKey、ACK、ACK Request、Garlic Clove（I2P garlic encryption 中的子消息“蒜瓣”）和 Padding 块

**未实现 (截至 0.9.50 版本):** - MessageNumbers 块 (类型 6) - Options 块 (类型 5) - Termination 块 (类型 4) - 协议层自动响应 - 零静态密钥模式 - 多播会话

**注意**：版本 1.5.0 至 2.10.0（2021–2025）的实现状态需要核实，因为可能新增了一些功能。

---

## 协议基础

### Noise 协议框架

ECIES-X25519-AEAD-Ratchet 基于 [Noise Protocol Framework（噪声协议框架）](https://noiseprotocol.org/)（修订版 34，2018-07-11），具体采用带有 I2P 特定扩展的 **IK**（交互式，已知远端静态密钥）握手模式。

### Noise 协议标识符

```
Noise_IKelg2+hs2_25519_ChaChaPoly_SHA256
```
**标识符组件:** - `Noise` - 基础框架 - `IK` - 带有已知远端静态密钥的交互式握手模式 - `elg2` - 用于临时密钥的 Elligator2 编码 (I2P 扩展) - `+hs2` - 在第二条消息之前调用 MixHash 以混入标签 (I2P 扩展) - `25519` - X25519 Diffie-Hellman 函数 - `ChaChaPoly` - ChaCha20-Poly1305 AEAD 密码 - `SHA256` - SHA-256 哈希函数

### Noise 握手模式

**IK 模式表示法:**

```
<- s                    (Bob's static key known to Alice)
...
-> e, es, s, ss         (Alice sends ephemeral, DH es, static key, DH ss)
<- e, ee, se            (Bob sends ephemeral, DH ee, DH se)
```
**记号含义:** - `e` - 临时密钥传输 - `s` - 静态密钥传输 - `es` - Alice 的临时密钥与 Bob 的静态密钥之间的 DH（Diffie-Hellman 密钥交换） - `ss` - Alice 的静态密钥与 Bob 的静态密钥之间的 DH - `ee` - Alice 的临时密钥与 Bob 的临时密钥之间的 DH - `se` - Bob 的静态密钥与 Alice 的临时密钥之间的 DH

### Noise 安全属性

使用 Noise（加密协议框架）的术语，IK pattern（IK 握手模式）提供：

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Message</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Authentication Level</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Confidentiality Level</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Message&nbsp;1 (NS)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;1 (sender auth, KCI vulnerable)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;2 (weak forward secrecy)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Message&nbsp;2 (NSR)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;2 (mutual auth)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;4 (weak forward secrecy)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Transport (ES)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;2 (mutual auth)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;5 (strong forward secrecy)</td>
    </tr>
  </tbody>
</table>
**认证级别：** - **第 1 级**：有效负载被认证为属于发送方静态密钥的所有者，但仍易受 Key Compromise Impersonation (KCI，密钥泄露后冒充) 攻击 - **第 2 级**：在 NSR 之后能够抵抗 KCI 攻击

**机密性级别：** - **第 2 级**: 如果发送方的静态密钥随后被泄露，仍能提供前向保密性 - **第 4 级**: 如果发送方的临时密钥随后被泄露，仍能提供前向保密性 - **第 5 级**: 在双方的临时密钥均被删除后，提供完全的前向保密性

### IK 与 XK 的差异

IK 模式不同于 NTCP2 和 SSU2 中使用的 XK 模式：

1. **四次 DH 运算**: IK（Noise 握手模式）使用 4 次 DH（Diffie-Hellman）运算（es, ss, ee, se），而 XK（Noise 握手模式）为 3 次
2. **即时认证**: Alice 在第一条消息中即完成认证（认证级别 1）
3. **更快的前向保密性**: 在第二条消息后（1-RTT）达到完全的前向保密性（级别 5）
4. **权衡**: 第一条消息的负载不具备前向保密性（相比之下，XK 的所有负载均具备前向保密性）

**摘要**: IK（Noise 协议中的握手模式）使得 Bob 的响应可以在 1-RTT（一轮往返时延）内送达并具备完全的前向保密性，但代价是初始请求不具备前向保密性。

### Signal Double Ratchet（双棘轮）概念

ECIES（椭圆曲线集成加密方案）融入了来自 [Signal 双重棘轮算法](https://signal.org/docs/specifications/doubleratchet/) 的概念：

- **DH 棘轮**: 通过定期交换新的 DH 密钥提供前向保密性
- **对称密钥棘轮**: 为每条消息派生新的会话密钥
- **会话标签棘轮**: 以确定性方式生成一次性使用的会话标签

**与 Signal 的关键差异：** - **棘轮更新频率更低**：I2P 仅在需要时执行棘轮更新（当标签接近耗尽或按策略） - **使用会话标签替代头部加密**：使用确定性的标签，而非加密的头部 - **显式 ACK（确认）**：使用带内的 ACK 块，而非仅依赖反向流量 - **标签棘轮与密钥棘轮分离**：对接收方更高效（可延迟密钥计算）

### I2P 对 Noise 协议框架的扩展

1. **Elligator2 Encoding（将椭圆曲线点编码为类随机字节的算法）**: 将临时密钥编码为与随机数不可区分
2. **在 NSR 前置标签**: 在 NSR 消息前添加 Session tag（会话标签），用于关联
3. **定义的负载格式**: 针对所有消息类型的基于块的负载结构
4. **I2NP 封装**: 所有消息都封装在 I2NP Garlic Message（大蒜消息）头部中
5. **独立的数据阶段**: 传输消息（ES，一种传输消息类型）偏离标准的 Noise（Noise 协议框架）数据阶段

---

## 密码学原语

### X25519 迪菲-赫尔曼

**规范**： [RFC 7748](https://tools.ietf.org/html/rfc7748)

**关键属性:** - **私钥大小**: 32 字节 - **公钥大小**: 32 字节 - **共享密钥大小**: 32 字节 - **字节序**: 小端序 - **曲线**: Curve25519

**操作：**

### X25519 GENERATE_PRIVATE()（生成私钥）

生成一个随机的 32 字节私钥：

```
privkey = CSRNG(32)
```
### X25519 DERIVE_PUBLIC(privkey)

派生出相应的公钥：

```
pubkey = curve25519_scalarmult_base(privkey)
```
返回以小端字节序表示的 32 字节公钥。

### X25519 DH(privkey, pubkey)（DH：Diffie-Hellman 密钥交换）

执行 Diffie-Hellman 密钥协商：

```
sharedSecret = curve25519_scalarmult(privkey, pubkey)
```
返回 32 字节的共享密钥。

**安全注意**: 实现方必须验证共享秘密不是全零（弱密钥）。如出现这种情况，应拒绝并中止握手。

### ChaCha20-Poly1305 AEAD（带关联数据的认证加密）

**规范**: [RFC 7539](https://tools.ietf.org/html/rfc7539) 第2.8节

**参数:** - **密钥长度**: 32 字节 (256 位) - **随机数大小**: 12 字节 (96 位) - **MAC 大小**: 16 字节 (128 位) - **块大小**: 64 字节 (内部)

**随机数格式:**

```
Byte 0-3:   0x00 0x00 0x00 0x00  (always zero)
Byte 4-11:  Little-endian counter (message number N)
```
**AEAD（带关联数据的认证加密）构造：**

AEAD（带关联数据的认证加密）将 ChaCha20 流密码与 Poly1305 MAC（消息认证码）结合起来：

1. 从密钥和 nonce (一次性随机数) 生成 ChaCha20 密钥流
2. 将明文与密钥流进行异或加密
3. 对 (关联数据 || 密文) 计算 Poly1305 MAC
4. 将 16 字节的 MAC 附加到密文之后

### ChaCha20-Poly1305 加密(k, n, plaintext, ad)

对明文进行认证加密：

```python
# Inputs
k = 32-byte cipher key
n = 12-byte nonce (first 4 bytes zero, last 8 bytes = message number)
plaintext = data to encrypt (0 to 65519 bytes)
ad = associated data (optional, used in MAC calculation)

# Output
ciphertext = chacha20_encrypt(k, n, plaintext)
mac = poly1305(ad || ciphertext, poly1305_key_gen(k, n))
return ciphertext || mac  # Total length = len(plaintext) + 16
```
**属性：** - 密文与明文长度相同（流密码） - 输出为 plaintext_length + 16 字节（包含 MAC） - 如果密钥是保密的，则整个输出与随机数据无法区分 - MAC（消息认证码）同时认证关联数据和密文

### ChaCha20-Poly1305 解密(k, n, ciphertext, ad)

解密并验证认证信息：

```python
# Split ciphertext and MAC
ct_without_mac = ciphertext[0:-16]
received_mac = ciphertext[-16:]

# Verify MAC
expected_mac = poly1305(ad || ct_without_mac, poly1305_key_gen(k, n))
if not constant_time_compare(received_mac, expected_mac):
    raise AuthenticationError("MAC verification failed")

# Decrypt
plaintext = chacha20_decrypt(k, n, ct_without_mac)
return plaintext
```
**关键安全要求：**
- 对于在相同密钥下的每条消息，Nonces（一次性随机数）必须保持唯一
- Nonces 绝不能被重用（重用将导致灾难性失败）
- MAC（消息认证码）验证必须使用常数时间比较，以防止时间侧信道攻击
- MAC 验证失败时必须完全拒绝该消息（不得进行任何部分解密）

### SHA-256 哈希函数

**规范**: NIST FIPS 180-4

**属性:** - **输出大小**: 32 字节 (256 位) - **块大小**: 64 字节 (512 位) - **安全级别**: 128 位 (抗碰撞性)

**操作：**

### 对 H(p, d) 进行 SHA-256 哈希

带个性化字符串的 SHA-256 哈希:

```
H(p, d) := SHA256(p || d)
```
其中 `||` 表示拼接，`p` 为个性化字符串，`d` 为数据。

### SHA-256 MixHash(d)

使用新数据更新 running hash（可增量更新的哈希）:

```
h = SHA256(h || d)
```
在整个 Noise 握手过程中用于维护握手记录哈希。

### HKDF 密钥派生

**规范**: [RFC 5869](https://tools.ietf.org/html/rfc5869)

**描述**: 基于 HMAC 的密钥派生函数，使用 SHA-256

**参数:** - **哈希函数**: HMAC-SHA256 - **盐长度**: 最多 32 字节 (SHA-256 输出大小) - **输出长度**: 可变 (最多 255 * 32 字节)

**HKDF 函数：**

```python
def HKDF(salt, ikm, info, length):
    """
    Args:
        salt: Salt value (32 bytes max for SHA-256)
        ikm: Input key material (any length)
        info: Context-specific info string
        length: Desired output length in bytes
    
    Returns:
        output: Derived key material (length bytes)
    """
    # Extract phase
    prk = HMAC-SHA256(salt, ikm)
    
    # Expand phase
    n = ceil(length / 32)
    t = b''
    okm = b''
    for i in range(1, n + 1):
        t = HMAC-SHA256(prk, t || info || byte(i))
        okm = okm || t
    
    return okm[0:length]
```
**常见使用模式：**

```python
# Generate two keys (64 bytes total)
keydata = HKDF(chainKey, sharedSecret, "KDFDHRatchetStep", 64)
nextRootKey = keydata[0:31]
chainKey = keydata[32:63]

# Generate session tag (8 bytes)
tagdata = HKDF(chainKey, CONSTANT, "SessionTagKeyGen", 64)
nextChainKey = tagdata[0:31]
sessionTag = tagdata[32:39]

# Generate symmetric key (32 bytes)
keydata = HKDF(chainKey, ZEROLEN, "SymmetricRatchet", 64)
nextChainKey = keydata[0:31]
sessionKey = keydata[32:63]
```
**ECIES 中使用的信息字符串:** - `"KDFDHRatchetStep"` - DH ratchet（棘轮）密钥派生 - `"TagAndKeyGenKeys"` - 初始化 tag（标签）和密钥链密钥 - `"STInitialization"` - 会话标签棘轮初始化 - `"SessionTagKeyGen"` - 会话标签生成 - `"SymmetricRatchet"` - 对称密钥生成 - `"XDHRatchetTagSet"` - DH 棘轮 tagset（标签集）密钥 - `"SessionReplyTags"` - NSR tagset 生成 - `"AttachPayloadKDF"` - NSR 负载密钥派生

### Elligator2（将椭圆曲线点伪装为均匀随机字节串的方案）编码

**用途**: 将 X25519 公钥编码，使其与均匀随机的长度为 32 字节的字节串不可区分。

**规范**: [Elligator2 论文](https://elligator.cr.yp.to/elligator-20130828.pdf)

**问题**：标准的 X25519 公钥具有可识别的结构。即使内容已被加密，观察者也可以通过检测这些密钥来识别握手消息。

**解决方案**：Elligator2（将椭圆曲线点编码为看起来随机的字符串的算法）在约 50% 的有效 X25519（基于 Curve25519 的 Diffie-Hellman 密钥交换方案）公钥与看起来随机的 254 位比特串之间提供一个双射映射。

**基于 Elligator2（用于隐藏公钥的椭圆曲线映射）的密钥生成：**

### Elligator2 GENERATE_PRIVATE_ELG2()

生成一个私钥，其对应的公钥可由 Elligator2（一种将椭圆曲线点编码为类随机字节串的方案）编码：

```python
while True:
    privkey = CSRNG(32)
    pubkey = DERIVE_PUBLIC(privkey)
    
    # Test if public key is Elligator2-encodable
    try:
        encoded = ENCODE_ELG2(pubkey)
        # Success - this key pair is suitable
        return privkey
    except NotEncodableError:
        # Try again with new random key
        continue
```
**重要**: 随机生成的私钥中约有 50% 会产生无法编码的公钥。必须将其丢弃，并尝试重新生成。

**性能优化**: 在后台线程中预先生成密钥，维护合适的密钥对池，避免在握手期间产生延迟。

### Elligator2（隐蔽映射算法）的 ENCODE_ELG2(pubkey)

将公钥编码为 32 个看似随机的字节：

```python
def ENCODE_ELG2(pubkey):
    """
    Encodes X25519 public key using Elligator2.
    
    Args:
        pubkey: 32-byte X25519 public key (little-endian)
    
    Returns:
        encoded: 32-byte encoded key indistinguishable from random
    
    Raises:
        NotEncodableError: If pubkey cannot be encoded
    """
    # Perform Elligator2 representative calculation
    # Returns 254-bit value (31.75 bytes)
    encodedKey = elligator2_encode(pubkey)
    
    # Add 2 random bits to MSB to make full 32 bytes
    randomByte = CSRNG(1)
    encodedKey[31] |= (randomByte & 0xc0)
    
    return encodedKey
```
**编码细节：** - Elligator2（椭圆曲线点编码方案）产生 254 位（不是完整的 256 位） - 第 31 个字节的最高 2 位是随机填充 - 结果在 32 字节空间内均匀分布 - 可成功编码约 50% 的有效 X25519 公钥

### Elligator2 DECODE_ELG2(encodedKey)

解码得到原始公钥：

```python
def DECODE_ELG2(encodedKey):
    """
    Decodes Elligator2-encoded key back to X25519 public key.
    
    Args:
        encodedKey: 32-byte encoded key
    
    Returns:
        pubkey: 32-byte X25519 public key (little-endian)
    """
    # Mask out 2 random padding bits from MSB
    encodedKey[31] &= 0x3f
    
    # Perform Elligator2 representative inversion
    pubkey = elligator2_decode(encodedKey)
    
    return pubkey
```
**安全属性：** - 编码后的密钥在计算上与随机字节不可区分 - 任何统计检验都无法可靠地检测到 Elligator2（隐匿映射算法）编码的密钥 - 解码是确定性的（相同的编码密钥总会产生相同的公钥） - 对可编码子集中的 ~50% 密钥，编码是双射的

**实现说明：** - 在生成阶段保存已编码的密钥，以避免在握手期间重新编码 - 在 Elligator2（将椭圆曲线点/公钥编码为类随机字节的算法）生成过程中被判定为不适用的密钥，仍可用于 NTCP2（其不需要 Elligator2） - 后台进行密钥生成对性能至关重要 - 由于 50% 的拒绝率，平均生成时间会翻倍

---

## 消息格式

### 概述

ECIES（椭圆曲线集成加密方案）定义了三种消息类型：

1. **新会话 (NS)**: 从 Alice 发往 Bob 的初始握手消息
2. **新会话回复 (NSR)**: Bob 发给 Alice 的握手回复
3. **现有会话 (ES)**: 此后在两个方向上的所有消息

所有消息都被封装在 I2NP Garlic Message 格式中，并叠加了额外的加密层。

### I2NP Garlic 消息容器

所有 ECIES 消息都封装在标准的 I2NP Garlic Message 头部中：

```
+----+----+----+----+----+----+----+----+
|type|      msg_id       |  expiration   |
+----+----+----+----+----+----+----+----+
                         |  size   |chks|
+----+----+----+----+----+----+----+----+
|      length       |                   |
+----+----+----+----+                   +
|          encrypted data               |
~                                       ~
```
**字段:** - `type`: 0x26 (Garlic 消息) - `msg_id`: 4 字节 I2NP 消息 ID - `expiration`: 8 字节 Unix 时间戳 (毫秒) - `size`: 2 字节有效负载大小 - `chks`: 1 字节校验和 - `length`: 4 字节加密数据长度 - `encrypted data`: ECIES 加密的有效负载

**用途**: 提供 I2NP 层的消息标识与路由功能。`length` 字段使接收方能够得知加密负载的总大小。

### 新会话 (NS) 消息

“New Session（新会话）”消息用于从 Alice 向 Bob 发起一个新的会话。它有三种变体：

1. **带绑定** (1b): 包含 Alice 的静态密钥，用于双向通信
2. **不带绑定** (1c): 省略静态密钥，用于单向通信
3. **一次性** (1d): 单消息模式，无需建立会话

### 带绑定的 NS Message (NS 消息) (类型 1b)

**用例**: 流式传输, 可回复的数据报, 任何需要回复的协议

**总长度**: 96 + payload_length 字节

**格式**:

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|   New Session Ephemeral Public Key    |
+             32 bytes                  +
|     Encoded with Elligator2           |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+         Static Key Section            +
|       ChaCha20 encrypted data         |
+            32 bytes                   +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+    (MAC) for Static Key Section       +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~          Variable length              ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
```
**字段详情：**

**临时公钥** (32 字节，明文): - Alice 的一次性 X25519 公钥 - 使用 Elligator2 编码（与随机数据不可区分） - 为每个 NS 消息新生成（绝不复用） - 小端序格式

**静态密钥部分** (加密后 32 字节，含 MAC 为 48 字节): - 包含 Alice 的 X25519 静态公钥 (32 字节) - 使用 ChaCha20 加密 - 使用 Poly1305 MAC (16 字节) 进行认证 - 由 Bob 用于将会话绑定到 Alice 的目的地

**有效载荷部分** (可变长度的加密数据，+16 字节 MAC): - 包含 Garlic Clove（I2P 中的“蒜瓣”消息单元）和其他块 - 必须包含 DateTime 块作为首个块 - 通常包含带有应用数据的 Garlic Clove 块 - 可包含用于即时密钥棘轮的 NextKey 块 - 使用 ChaCha20 加密 - 使用 Poly1305 MAC（16 字节）进行认证

**安全属性：** - 临时密钥提供前向保密性 - 静态密钥对 Alice 进行认证（绑定到目标） - 两个部分各自使用独立的 MAC（消息认证码），以实现域分离 - 整个握手执行 2 次 DH（Diffie-Hellman）运算（es, ss）

### 无绑定的 NS 消息（类型 1c）

**用例**：既不期望也不希望收到回复的原始数据报

**总长度**: 96 + payload_length 字节

**格式**:

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|   New Session Ephemeral Public Key    |
+             32 bytes                  +
|     Encoded with Elligator2           |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+           Flags Section               +
|       ChaCha20 encrypted data         |
+            32 bytes                   +
|           All zeros                   |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for above section       +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~          Variable length              ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
```
**关键差异**: Flags Section（标志部分）包含32个零字节，而不是静态密钥。

**检测**: Bob 通过解密该 32 字节区段并检查所有字节是否为零来确定消息类型: - 全为零 → 未绑定会话 (类型 1c) - 非零 → 使用静态密钥的绑定会话 (类型 1b)

**属性：** - 无静态密钥意味着不与 Alice 的目标地址绑定 - Bob 无法发送回复（未知目标地址） - 仅执行 1 次 DH（Diffie-Hellman）运算 - 遵循 Noise（协议框架）"N" 模式而非 "IK" - 在不需要回复的情况下更高效

**标志部分** (保留供将来使用): 目前全为 0。未来版本中可用于特性协商。

### NS 一次性消息（类型 1d）

**使用场景**: 单条匿名消息，不建立会话且不期望回复

**总长度**: 96 + payload_length 字节

**Format**: 与无绑定的 NS 相同（类型 1c）

**区别**:  - Type 1c 可以在同一会话中发送多条消息（随后为 ES messages（即 ES 消息）） - Type 1d 仅发送一条消息且不建立会话 - 在实践中，实现最初可能将二者视为相同

**特性：** - 最大匿名性（无静态密钥，无会话） - 双方均不保留会话状态 - 遵循 Noise "N" pattern（Noise 协议中的 N 模式） - 单次 DH 运算（es，临时-静态）

### 新会话应答（NSR）消息

Bob 发送一个或多个 NSR 消息来响应 Alice 的 NS 消息。NSR 完成了 Noise IK handshake（Noise 协议的 IK 模式握手），并建立了双向会话。

**总长度**: 72 + payload_length 字节

**格式**:

```
+----+----+----+----+----+----+----+----+
|       Session Tag   8 bytes           |
+----+----+----+----+----+----+----+----+
|                                       |
+        Ephemeral Public Key           +
|                                       |
+            32 bytes                   +
|     Encoded with Elligator2           |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+  (MAC) for Key Section (empty)        +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~          Variable length              ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
```
**字段详细信息：**

**Session Tag（会话标签）** (8 字节，明文): - 由 NSR 标签集生成（参见 KDF 相关章节） - 将此回复与 Alice 的 NS 消息相关联 - 使 Alice 能识别此 NSR 是对哪个 NS 的响应 - 一次性使用（绝不复用）

**临时公钥** (32 字节，明文): - Bob 的一次性 X25519 公钥 - 使用 Elligator2 编码 - 为每个 NSR 消息新生成 - 每次发送 NSR 都必须不同

**Key Section MAC（密钥区段的 MAC）** (16 字节): - 认证空数据（ZEROLEN） - 属于 Noise IK 协议（se 握手模式） - 使用握手记录哈希作为关联数据 - 对将 NSR 绑定到 NS 至关重要

**有效载荷部分** (可变长度): - 包含 garlic cloves (蒜瓣) 和数据块 - 通常包含应用层回复 - 可能为空 (ACK-only NSR) - 最大大小: 65519 字节 (65535 - 16 字节 MAC)

**多条 NSR 消息：**

Bob 可能会针对一个 NS（握手请求消息）发送多个 NSR（握手响应消息）： - 每个 NSR 都有唯一的临时密钥 - 每个 NSR 都有唯一的会话标签 - Alice 使用收到的第一个 NSR 来完成握手 - 其他 NSR 用于冗余（以防丢包）

**关键时序:** - Alice 在发送 ES 消息之前必须先收到一条 NSR 消息 - Bob 在发送 ES 消息之前必须先收到一条 ES 消息 - NSR 通过 split() 操作建立双向会话密钥

**安全属性：** - 完成 Noise IK 握手 - 进行 2 次额外的 Diffie-Hellman（DH）运算（ee、se） - 在 NS+NSR 范围内共进行 4 次 DH 运算 - 实现双向认证（级别 2） - 为 NSR 负载提供较弱的前向保密性（级别 4）

### 现有会话（ES）消息

在 NS/NSR handshake（NS/NSR 握手）之后的所有消息都使用 Existing Session（现有会话）格式。ES 消息由 Alice 和 Bob 双向使用。

**总长度**: 8 + payload_length + 16 字节（最小为 24 字节）

**格式**:

```
+----+----+----+----+----+----+----+----+
|       Session Tag   8 bytes           |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~          Variable length              ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+              (MAC)                    +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
```
**字段详细信息：**

**会话标签** (8 字节, 明文): - 由当前出站标签集生成 - 用于标识会话和消息编号 - 接收方查找该标签以获取会话密钥和 nonce（一次性随机数） - 一次性使用（每个标签仅使用一次） - 格式: HKDF 输出的前 8 个字节

**Payload Section** (可变长度): - 包含 Garlic Clove（I2P 蒜瓣消息单元）和块 - 没有必需的块（可以为空） - 常见块: Garlic Clove、NextKey、ACK、ACK Request、Padding - 最大大小: 65519 字节（65535 - 16 字节 MAC）

**MAC** (16 字节): - Poly1305 认证标签 - 在整个载荷上计算 - 关联数据：8 字节的会话标签 - 必须验证通过，否则消息将被拒绝

**标签查找流程：**

1. 接收方提取 8 字节标签
2. 在所有当前入站标签集中查找该标签
3. 取回关联的会话密钥与消息编号 N
4. 构造 nonce（随机数）：`[0x00, 0x00, 0x00, 0x00, N (8 bytes little-endian)]`
5. 使用 AEAD（带关联数据的认证加密），以该标签作为关联数据，解密负载
6. 从标签集中移除该标签（一次性使用）
7. 处理解密后的数据块

**未找到会话标签：**

如果在任何标签集中都找不到该标签： - 可能是 NS 消息 → 尝试 NS 解密 - 可能是 NSR 消息 → 尝试 NSR 解密 - 可能是乱序的 ES → 短暂等待标签集更新 - 可能是重放攻击 → 拒绝 - 可能是数据损坏 → 拒绝

**空载荷:**

ES 消息可以有空负载 (0 字节): - 当收到 ACK Request 时，充当显式 ACK（确认） - 提供不含应用数据的协议层响应 - 仍然会消耗一个 session tag（会话标签） - 当更高层没有可立即发送的数据时很有用

**安全属性：** - 在收到 NSR 后实现完全前向保密（Level 5） - 通过 AEAD（带关联数据的认证加密）实现认证加密 - 标签充当额外的关联数据 - 在需要进行棘轮（ratchet）之前，每个标签集最多 65535 条消息

---

## 密钥派生函数

本节记录 ECIES 中使用的全部 KDF（密钥派生函数）操作，并展示完整的密码学推导过程。

### 记号与常量

**常量：** - `ZEROLEN` - 零长度字节数组（空字符串） - `||` - 连接运算符

**变量:** - `h` - 握手记录的累积哈希 (32 字节) - `chainKey` - 用于 HKDF 的链密钥 (32 字节) - `k` - 对称加密密钥 (32 字节) - `n` - 随机数（nonce）/ 消息编号

**密钥：** - `ask` / `apk` - Alice 的静态私钥/公钥 - `aesk` / `aepk` - Alice 的临时私钥/公钥 - `bsk` / `bpk` - Bob 的静态私钥/公钥 - `besk` / `bepk` - Bob 的临时私钥/公钥

### NS 消息的密钥派生函数

### KDF 1：初始链密钥

在协议初始化时执行一次（可预先计算）：

```python
# Protocol name (40 bytes, ASCII, no null termination)
protocol_name = "Noise_IKelg2+hs2_25519_ChaChaPoly_SHA256"

# Initialize hash
h = SHA256(protocol_name)

# Initialize chaining key
chainKey = h

# MixHash with empty prologue
h = SHA256(h)

# State: chainKey and h initialized
# Can be precalculated for all outbound sessions
```
**结果：** - `chainKey` = 用于所有后续 KDF（密钥派生函数）的初始链密钥 - `h` = 初始握手记录哈希

### KDF 2: Bob 的静态密钥混合

Bob 只需执行一次此操作（可以为所有入站会话预先计算）:

```python
# Bob's static keys (published in LeaseSet)
bsk = GENERATE_PRIVATE()
bpk = DERIVE_PUBLIC(bsk)

# Mix Bob's public key into hash
h = SHA256(h || bpk)

# State: h updated with Bob's identity
# Can be precalculated by Bob for all inbound sessions
```
### KDF 3：Alice 的临时密钥生成

Alice 为每个 NS 消息生成全新的密钥：

```python
# Generate ephemeral key pair suitable for Elligator2
aesk = GENERATE_PRIVATE_ELG2()
aepk = DERIVE_PUBLIC(aesk)

# Mix ephemeral public key into hash
h = SHA256(h || aepk)

# Elligator2 encode for transmission
elg2_aepk = ENCODE_ELG2(aepk)

# State: h updated with Alice's ephemeral key
# Send elg2_aepk as first 32 bytes of NS message
```
### KDF 4: NS 静态密钥部分（即 DH）

派生用于加密 Alice 的静态密钥的密钥:

```python
# Perform first DH (ephemeral-static)
sharedSecret = DH(aesk, bpk)  # Alice computes
# Equivalent: sharedSecret = DH(bsk, aepk)  # Bob computes

# Derive cipher key from shared secret
keydata = HKDF(chainKey, sharedSecret, "", 64)
chainKey = keydata[0:31]
k = keydata[32:63]

# AEAD encryption parameters
nonce = 0
associated_data = h  # Current hash transcript

# Encrypt static key section
if binding_requested:
    plaintext = apk  # Alice's static public key (32 bytes)
else:
    plaintext = bytes(32)  # All zeros for unbound

ciphertext = ENCRYPT(k, nonce, plaintext, associated_data)
# ciphertext = 32 bytes encrypted + 16 bytes MAC = 48 bytes

# Mix ciphertext into hash
h = SHA256(h || ciphertext)

# State: Static key section encrypted, h updated
# Send ciphertext (48 bytes) as next part of NS message
```
### KDF 5：NS 有效载荷部分（ss DH，仅用于绑定）

对于已绑定的会话，执行第二次 DH（Diffie-Hellman 密钥交换）用于负载加密:

```python
if binding_requested:
    # Alice's static keys
    ask = GENERATE_PRIVATE()  # Alice's long-term key
    apk = DERIVE_PUBLIC(ask)
    
    # Perform second DH (static-static)
    sharedSecret = DH(ask, bpk)  # Alice computes
    # Equivalent: sharedSecret = DH(bsk, apk)  # Bob computes
    
    # Derive cipher key
    keydata = HKDF(chainKey, sharedSecret, "", 64)
    chainKey = keydata[0:31]
    k = keydata[32:63]
    
    nonce = 0
    associated_data = h
else:
    # Unbound: reuse keys from static key section
    # chainKey and k unchanged
    nonce = 1  # Increment nonce (reusing same key)
    associated_data = h

# Encrypt payload
payload = build_payload()  # DateTime + Garlic Cloves + etc.
ciphertext = ENCRYPT(k, nonce, payload, associated_data)

# Mix ciphertext into hash
h = SHA256(h || ciphertext)

# State: Payload encrypted, h contains complete NS transcript
# Save chainKey and h for NSR processing
# Send ciphertext as final part of NS message
```
**重要说明：**

1. **Bound vs Unbound**: 
   - Bound 执行 2 次 DH (Diffie-Hellman) 运算 (es + ss)
   - Unbound 执行 1 次 DH 运算 (仅 es)
   - Unbound 通过递增 nonce (随机数) 而不是派生新密钥

2. **密钥重用安全性**:
   - 不同的 nonce（一次性随机数）（0 与 1）可防止密钥/nonce 重用
   - 不同的关联数据（h 不同）提供域分离

3. **哈希交互记录**:
   - `h` 现在包含: protocol_name, 空的 prologue（序言）, bpk, aepk, static_key_ciphertext, payload_ciphertext
   - 此记录将 NS 消息的所有部分绑定在一起

### NSR 应答标签集 KDF（密钥派生函数）

Bob 为 NSR 消息生成标签：

```python
# Chain key from NS payload section
# chainKey = final chainKey from NS KDF

# Generate tagset key
tagsetKey = HKDF(chainKey, ZEROLEN, "SessionReplyTags", 32)

# Initialize NSR tagset (see DH_INITIALIZE below)
tagset_nsr = DH_INITIALIZE(chainKey, tagsetKey)

# Get tag for this NSR
tagsetEntry = tagset_nsr.GET_NEXT_ENTRY()
tag = tagsetEntry.SESSION_TAG  # 8 bytes

# State: tag available for NSR message
# Send tag as first 8 bytes of NSR
```
### NSR 消息的密钥派生函数

### KDF 6：NSR 临时密钥生成

Bob 为每个 NSR 生成一个新的临时密钥:

```python
# Mix tag into hash (I2P extension to Noise)
h = SHA256(h || tag)

# Generate ephemeral key pair
besk = GENERATE_PRIVATE_ELG2()
bepk = DERIVE_PUBLIC(besk)

# Mix ephemeral public key into hash
h = SHA256(h || bepk)

# Elligator2 encode for transmission
elg2_bepk = ENCODE_ELG2(bepk)

# State: h updated with tag and Bob's ephemeral key
# Send elg2_bepk as bytes 9-40 of NSR message
```
### KDF 7: NSR 密钥部分（ee 和 se DH）

派生用于 NSR 密钥部分的密钥：

```python
# Perform third DH (ephemeral-ephemeral)
sharedSecret_ee = DH(aesk, bepk)  # Alice computes
# Equivalent: sharedSecret_ee = DH(besk, aepk)  # Bob computes

# Mix ee into chain
keydata = HKDF(chainKey, sharedSecret_ee, "", 32)
chainKey = keydata[0:31]

# Perform fourth DH (static-ephemeral)
sharedSecret_se = DH(ask, bepk)  # Alice computes
# Equivalent: sharedSecret_se = DH(besk, apk)  # Bob computes

# Derive cipher key from se
keydata = HKDF(chainKey, sharedSecret_se, "", 64)
chainKey = keydata[0:31]
k = keydata[32:63]

# AEAD encryption of empty data (key section has no payload)
nonce = 0
associated_data = h
ciphertext = ENCRYPT(k, nonce, ZEROLEN, associated_data)
# ciphertext = 16 bytes (MAC only, no plaintext)

# Mix ciphertext into hash
h = SHA256(h || ciphertext)

# State: Key section encrypted, chainKey contains all 4 DH results
# Send ciphertext (16 bytes MAC) as bytes 41-56 of NSR
```
**关键**: 这就完成了 Noise IK 握手（Noise 协议中的 IK 模式）。`chainKey` 现在包含来自全部 4 次 DH 运算（es, ss, ee, se）的贡献。

### KDF（密钥派生函数）8：NSR 有效载荷部分

派生用于 NSR 负载加密的密钥：

```python
# Split chainKey into bidirectional keys
keydata = HKDF(chainKey, ZEROLEN, "", 64)
k_ab = keydata[0:31]   # Alice → Bob key
k_ba = keydata[32:63]  # Bob → Alice key

# Initialize ES tagsets for both directions
tagset_ab = DH_INITIALIZE(chainKey, k_ab)  # Alice → Bob
tagset_ba = DH_INITIALIZE(chainKey, k_ba)  # Bob → Alice

# Derive NSR payload key (Bob → Alice)
k_nsr = HKDF(k_ba, ZEROLEN, "AttachPayloadKDF", 32)

# Encrypt NSR payload
nonce = 0
associated_data = h  # Binds payload to entire NSR
payload = build_payload()  # Usually application reply
ciphertext = ENCRYPT(k_nsr, nonce, payload, associated_data)

# State: Bidirectional ES sessions established
# tagset_ab and tagset_ba ready for ES messages
# Send ciphertext as bytes 57+ of NSR message
```
**重要说明：**

1. **拆分操作**：
   - 为每个方向生成独立的密钥
   - 防止在 Alice→Bob 与 Bob→Alice 之间复用密钥

2. **NSR 负载绑定**:
   - 使用 `h` 作为关联数据，将负载与握手绑定
   - 独立的 KDF（"AttachPayloadKDF"）实现域分离

3. **ES 就绪**:
   - 在 NSR 之后，双方都可以发送 ES 消息
   - Alice 在发送 ES 之前必须先接收 NSR
   - Bob 在发送 ES 之前必须先接收 ES

### ES 消息的 KDF（密钥派生函数）

ES 消息使用来自 tagsets（标签集）的预生成会话密钥：

```python
# Sender gets next tag and key
tagsetEntry = outbound_tagset.GET_NEXT_ENTRY()
tag = tagsetEntry.SESSION_TAG     # 8 bytes
k = tagsetEntry.SESSION_KEY       # 32 bytes
N = tagsetEntry.INDEX             # Message number

# Construct nonce (12 bytes)
nonce = [0x00, 0x00, 0x00, 0x00] + little_endian_8_bytes(N)

# AEAD encryption
associated_data = tag  # Tag is associated data
payload = build_payload()
ciphertext = ENCRYPT(k, nonce, payload, associated_data)

# Send: tag || ciphertext (8 + len(ciphertext) bytes)
```
**接收方流程：**

```python
# Extract tag
tag = message[0:8]

# Look up tag in inbound tagsets
tagsetEntry = inbound_tagset.GET_SESSION_KEY(tag)
if tagsetEntry is None:
    # Not an ES message, try NS/NSR decryption
    return try_handshake_decryption(message)

k = tagsetEntry.SESSION_KEY
N = tagsetEntry.INDEX

# Construct nonce
nonce = [0x00, 0x00, 0x00, 0x00] + little_endian_8_bytes(N)

# AEAD decryption
associated_data = tag
ciphertext = message[8:]
try:
    payload = DECRYPT(k, nonce, ciphertext, associated_data)
except AuthenticationError:
    # MAC verification failed, reject message
    return reject_message()

# Process payload blocks
process_payload(payload)

# Remove tag from tagset (one-time use)
inbound_tagset.remove(tag)
```
### DH_INITIALIZE 函数

为单一方向创建一个 tagset（标签集合）：

```python
def DH_INITIALIZE(rootKey, k):
    """
    Initializes a tagset with session tag and symmetric key ratchets.
    
    Args:
        rootKey: Chain key from previous DH ratchet (32 bytes)
        k: Key material from split() or DH ratchet (32 bytes)
    
    Returns:
        tagset: Initialized tagset object
    """
    # Derive next root key and chain key
    keydata = HKDF(rootKey, k, "KDFDHRatchetStep", 64)
    nextRootKey = keydata[0:31]
    chainKey_tagset = keydata[32:63]
    
    # Derive separate chain keys for tags and keys
    keydata = HKDF(chainKey_tagset, ZEROLEN, "TagAndKeyGenKeys", 64)
    sessTag_ck = keydata[0:31]   # Session tag chain key
    symmKey_ck = keydata[32:63]  # Symmetric key chain key
    
    # Create tagset object
    tagset = Tagset()
    tagset.nextRootKey = nextRootKey
    tagset.sessTag_chainKey = sessTag_ck
    tagset.symmKey_chainKey = symmKey_ck
    tagset.lastIndex = -1
    
    return tagset
```
**使用场景：**

1. **NSR 标签集**: `DH_INITIALIZE(chainKey_from_NS, tagsetKey_NSR)`
2. **ES 标签集**: `DH_INITIALIZE(chainKey_from_NSR, k_ab or k_ba)`
3. **棘轮化标签集**: `DH_INITIALIZE(nextRootKey_from_previous, tagsetKey_from_DH)`

---

## 棘轮机制

ECIES（椭圆曲线集成加密方案）使用三个同步的棘轮机制，提供前向保密性和高效的会话管理。

### Ratchet（密钥棘轮）概述

**三种棘轮类型：**

1. **DH 棘轮**: 执行 Diffie-Hellman 密钥交换以生成新的根密钥
2. **会话标签棘轮**: 确定性地导出一次性会话标签
3. **对称密钥棘轮**: 导出用于消息加密的会话密钥

**关系：**

```
DH Ratchet (periodic)
    ↓
Creates new tagset
    ↓
Session Tag Ratchet (per message) ← synchronized → Symmetric Key Ratchet (per message)
    ↓                                                      ↓
Session Tags (8 bytes each)                      Session Keys (32 bytes each)
```
**关键属性：**

- **发送方**: 按需生成标签和密钥（无需存储）
- **接收方**: 为前视窗口预生成标签（需要存储）
- **同步**: 标签索引决定密钥索引（N_tag = N_key）
- **前向保密性**: 通过周期性的 DH ratchet 实现（DH ratchet：基于 Diffie-Hellman 的密钥棘轮机制）
- **效率**: 接收方可将密钥计算延后至接收到标签时再进行

### DH 棘轮

DH 棘轮通过定期交换新的临时密钥来提供前向保密性。

### DH 棘轮频率

**所需棘轮条件：** - 标签集接近耗尽（标签 65535 为最大值） - 特定于实现的策略：   - 消息计数阈值（例如，每 4096 条消息）   - 时间阈值（例如，每 10 分钟）   - 数据量阈值（例如，每 100 MB）

**建议的 First Ratchet（首次棘轮）**：标签编号约为 4096，以避免达到上限

**最大值:** - **最大标签集ID**: 65535 - **最大密钥ID**: 32767 - **每个标签集的最大消息数**: 65535 - **每个会话的理论最大数据量**: ~6.9 TB (64K 标签集 × 64K 消息 × 平均 1730 字节)

### DH Ratchet（Diffie-Hellman 棘轮）标签和密钥 ID

**初始标签集**（握手后）： - 标签集 ID：0 - 尚未发送任何 NextKey（后续密钥）块 - 尚未分配密钥 ID

**首次棘轮之后**: - 标签集 ID: 1 = (1 + Alice 的密钥 ID + Bob 的密钥 ID) = (1 + 0 + 0) - Alice 发送密钥 ID 为 0 的 NextKey - Bob 以密钥 ID 为 0 的 NextKey 回复

**后续标签集**: - 标签集ID = 1 + 发送方的密钥ID + 接收方的密钥ID - 例如: 标签集 5 = (1 + sender_key_2 + receiver_key_2)

**Tag Set（标签集）演进表：**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Tag Set ID</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Sender Key ID</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Receiver Key ID</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">n/a</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">n/a</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Initial tag set (post-NSR)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">First ratchet (both generate new keys)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Sender generates new key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Receiver generates new key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Sender generates new key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Receiver generates new key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">...</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">...</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">...</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Pattern repeats</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">65534</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32767 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32766</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Second-to-last tag set</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">65535</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32767</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32767 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Final tag set</td>
    </tr>
  </tbody>
</table>
\* = 本次棘轮生成了新密钥

**Key ID 规则：** - ID 从 0 开始按顺序递增 - 仅在生成新密钥时 ID 才递增 - 最大密钥 ID 为 32767 (15 位) - 达到密钥 ID 32767 后，需要新建会话

### DH 棘轮消息流

**角色：** - **标签发送方**: 持有出站标签集，发送消息 - **标签接收方**: 持有入站标签集，接收消息

**模式：** 标签发送方在标签集合即将耗尽时发起棘轮。

**消息流程图：**

```
Tag Sender                         Tag Receiver

       ... using tag set #0 ...

(Tag set #0 approaching exhaustion)
(Generate new key #0)

NextKey forward, request reverse, with key #0  -------->
(Repeat until NextKey ACK received)
                                   (Generate new key #0)
                                   (Perform DH: sender_key_0 × receiver_key_0)
                                   (Create inbound tag set #1)

        <---------------           NextKey reverse, with key #0
                                   (Repeat until tag from tag set #1 received)

(Receive NextKey with key #0)
(Perform DH: sender_key_0 × receiver_key_0)
(Create outbound tag set #1)


       ... using tag set #1 ...


(Tag set #1 approaching exhaustion)
(Generate new key #1)

NextKey forward, with key #1        -------->
(Repeat until NextKey ACK received)
                                   (Reuse existing key #0)
                                   (Perform DH: sender_key_1 × receiver_key_0)
                                   (Create inbound tag set #2)

        <--------------            NextKey reverse, id 0 (ACK)
                                   (Repeat until tag from tag set #2 received)

(Receive NextKey with id 0)
(Perform DH: sender_key_1 × receiver_key_0)
(Create outbound tag set #2)


       ... using tag set #2 ...


(Tag set #2 approaching exhaustion)
(Reuse existing key #1)

NextKey forward, request reverse, id 1  -------->
(Repeat until NextKey received)
                                   (Generate new key #1)
                                   (Perform DH: sender_key_1 × receiver_key_1)
                                   (Create inbound tag set #3)

        <--------------            NextKey reverse, with key #1

(Receive NextKey with key #1)
(Perform DH: sender_key_1 × receiver_key_1)
(Create outbound tag set #3)


       ... using tag set #3 ...

       (Pattern repeats: even-numbered tag sets
        use forward key, odd-numbered use reverse key)
```
**棘轮模式：**

**创建偶数编号的标签集** (2, 4, 6, ...): 1. 发送方生成新密钥 2. 发送方发送包含新密钥的 NextKey 块 3. 接收方发送包含旧密钥 ID 的 NextKey 块 (ACK 确认) 4. 双方基于 (新发送方密钥 × 旧接收方密钥) 执行 DH (Diffie-Hellman 密钥交换)

**创建奇数编号的标签集** (3, 5, 7, ...): 1. 发送方请求反向密钥（发送带请求标志的 NextKey） 2. 接收方生成新密钥 3. 接收方发送包含新密钥的 NextKey 块 4. 双方使用（旧的发送方密钥 × 新的接收方密钥）进行 DH（Diffie-Hellman 密钥交换）

### NextKey 块格式

请参见 Payload Format（载荷格式）部分，了解 NextKey block（NextKey 块）的详细规范。

**关键要素:** - **标志字节**:   - 位 0: 密钥存在 (1) 或仅 ID (0)   - 位 1: 反向密钥 (1) 或正向密钥 (0)   - 位 2: 请求反向密钥 (1) 或不请求 (0) - **密钥 ID**: 2 字节, 大端序 (0-32767) - **公钥**: 32 字节 X25519 (如果位 0 = 1)

**NextKey 块示例：**

```python
# Sender initiates ratchet with new key (key ID 0, tag set 1)
NextKey(flags=0x01, key_id=0, pubkey=sender_key_0)

# Receiver replies with new key (key ID 0, tag set 1)
NextKey(flags=0x03, key_id=0, pubkey=receiver_key_0)

# Sender ratchets again with new key (key ID 1, tag set 2)
NextKey(flags=0x01, key_id=1, pubkey=sender_key_1)

# Receiver ACKs with old key ID (tag set 2)
NextKey(flags=0x02, key_id=0)

# Sender requests reverse key (tag set 3)
NextKey(flags=0x04, key_id=1)

# Receiver sends new reverse key (key ID 1, tag set 3)
NextKey(flags=0x03, key_id=1, pubkey=receiver_key_1)
```
### DH 棘轮密钥派生函数

当交换新密钥时：

```python
# Tag sender generates or reuses key
if generating_new:
    sender_sk = GENERATE_PRIVATE()
    sender_pk = DERIVE_PUBLIC(sender_sk)
else:
    # Reuse existing key pair
    sender_pk = existing_sender_pk

# Tag receiver generates or reuses key
if generating_new:
    receiver_sk = GENERATE_PRIVATE()
    receiver_pk = DERIVE_PUBLIC(receiver_sk)
else:
    # Reuse existing key pair
    receiver_pk = existing_receiver_pk

# Both parties perform DH
sharedSecret = DH(sender_sk, receiver_pk)

# Derive tagset key
tagsetKey = HKDF(sharedSecret, ZEROLEN, "XDHRatchetTagSet", 32)

# Get next root key from previous tagset
rootKey = previous_tagset.nextRootKey

# Initialize new tagset
new_tagset = DH_INITIALIZE(rootKey, tagsetKey)

# Tag sender: outbound tagset
# Tag receiver: inbound tagset
```
**关键时序:**

**标签发送方:** - 立即创建新的出站标签集 - 立即开始使用新标签 - 删除旧的出站标签集

**标签接收方：** - 创建新的入站标签集 - 在宽限期（3 分钟）内保留旧的入站标签集 - 在宽限期内同时接受来自新旧标签集的标签 - 宽限期结束后删除旧的入站标签集

### DH棘轮状态管理

**发送方状态：** - 当前出站标签集 - 标签集ID和密钥ID - 下一个根密钥（用于下一个 ratchet（棘轮机制）） - 当前标签集中的消息计数

**接收方状态:** - 当前入站标签集（在宽限期内可能有 2 个） - 用于缺口检测的先前消息编号（PN） - 预生成标签的前瞻窗口 - 下一个根密钥（用于下一轮棘轮）

**状态转换规则：**

1. **在首次 Ratchet（密码学棘轮机制）之前**:
   - 使用标签集 0（来自 NSR）
   - 未分配任何密钥 ID

2. **启动 Ratchet（棘轮机制）**:
   - 生成新密钥（如果本轮由发送方负责生成）
   - 在 ES message（ES 消息）中发送 NextKey block（NextKey 块）
   - 在创建新的出站标签集合之前等待 NextKey reply（NextKey 回复）

3. **接收 Ratchet 请求（棘轮机制）**:
   - 生成新密钥（如果本轮由接收方生成）
   - 使用接收到的密钥执行 DH（Diffie-Hellman 密钥交换）
   - 创建新的入站标签集
   - 发送 NextKey 回复（下一轮密钥）
   - 在宽限期内保留旧的入站标签集

4. **完成 Ratchet（加密棘轮机制）**:
   - 接收 NextKey（下一密钥）回复
   - 执行 DH（Diffie-Hellman 密钥交换）
   - 创建新的出站 tag set（标签集）
   - 开始使用新的标签

### Session Tag Ratchet（会话标签棘轮机制）

Session tag ratchet（会话标签棘轮机制）以确定性的方式生成一次性使用的 8 字节会话标签。

### 会话标签棘轮的目的

- 取代显式标签传输（ElGamal 发送 32 字节的标签）
- 允许接收方预生成用于前瞻窗口的标签
- 发送方按需生成（无需存储）
- 通过索引与对称密钥棘轮同步

### 会话标签棘轮公式

**初始化：**

```python
# From DH_INITIALIZE
sessTag_ck = initial_chain_key  # 32 bytes

# Initialize session tag ratchet
keydata = HKDF(sessTag_ck, ZEROLEN, "STInitialization", 64)
sessTag_chainKey = keydata[0:31]    # First chain key
SESSTAG_CONSTANT = keydata[32:63]   # Constant for all tags in this tagset
```
**标签生成（针对标签 N）：**

```python
# Generate tag N
keydata = HKDF(sessTag_chainKey_(N-1), SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
sessTag_chainKey_N = keydata[0:31]  # Chain key for next tag
tag_N = keydata[32:39]              # Session tag (8 bytes)

# Chain continues for each tag
# tag_0, tag_1, tag_2, ..., tag_65535
```
**完整序列：**

```python
# Tag 0
keydata_0 = HKDF(sessTag_chainKey, SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
sessTag_chainKey_0 = keydata_0[0:31]
tag_0 = keydata_0[32:39]

# Tag 1
keydata_1 = HKDF(sessTag_chainKey_0, SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
sessTag_chainKey_1 = keydata_1[0:31]
tag_1 = keydata_1[32:39]

# Tag N
keydata_N = HKDF(sessTag_chainKey_(N-1), SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
sessTag_chainKey_N = keydata_N[0:31]
tag_N = keydata_N[32:39]
```
### 会话标签棘轮发送端实现

```python
class OutboundTagset:
    def __init__(self, sessTag_ck):
        # Initialize
        keydata = HKDF(sessTag_ck, ZEROLEN, "STInitialization", 64)
        self.chainKey = keydata[0:31]
        self.constant = keydata[32:63]
        self.index = -1
    
    def get_next_tag(self):
        # Increment index
        self.index += 1
        
        if self.index > 65535:
            raise TagsetExhausted("Ratchet required")
        
        # Generate tag
        keydata = HKDF(self.chainKey, self.constant, "SessionTagKeyGen", 64)
        self.chainKey = keydata[0:31]
        tag = keydata[32:39]
        
        return (tag, self.index)
```
**发送方流程：** 1. 对每条消息调用 `get_next_tag()` 2. 在 ES 消息中使用返回的标签 3. 存储索引 N 以便潜在的 ACK（确认）跟踪 4. 无需存储标签（按需生成）

### 会话标签棘轮接收端实现

```python
class InboundTagset:
    def __init__(self, sessTag_ck, look_ahead=32):
        # Initialize
        keydata = HKDF(sessTag_ck, ZEROLEN, "STInitialization", 64)
        self.chainKey = keydata[0:31]
        self.constant = keydata[32:63]
        self.index = -1
        self.look_ahead = look_ahead
        self.tags = {}  # Dictionary: tag -> index
        
        # Pre-generate initial tags
        self.extend(look_ahead)
    
    def extend(self, count):
        """Generate 'count' more tags"""
        for _ in range(count):
            self.index += 1
            
            if self.index > 65535:
                return  # Cannot exceed maximum
            
            # Generate tag
            keydata = HKDF(self.chainKey, self.constant, "SessionTagKeyGen", 64)
            self.chainKey = keydata[0:31]
            tag = keydata[32:39]
            
            # Store tag
            self.tags[tag] = self.index
    
    def lookup_tag(self, tag):
        """Look up tag and return index"""
        if tag in self.tags:
            index = self.tags[tag]
            # Remove tag (one-time use)
            del self.tags[tag]
            return index
        return None
    
    def check_and_extend(self):
        """Extend if tag count is low"""
        current_count = len(self.tags)
        if current_count < self.look_ahead // 2:
            # Extend to restore window
            self.extend(self.look_ahead - current_count)
```
**接收端流程：** 1. 为前瞻窗口预先生成标签（例如 32 个标签） 2. 将标签存入哈希表或字典 3. 消息到达时，查找标签以获取索引 N 4. 从存储中移除该标签（一次性使用） 5. 若标签数量低于阈值，则扩展窗口

### 会话标签前瞻策略

**目的**: 在内存使用与乱序消息处理之间取得平衡

**推荐的前瞻大小：**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Tagset Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Initial Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Maximum Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR tagset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Short-lived</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ES tagset 0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">24</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">160</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Initial ES tagset</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ES tagset 1+</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">160</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">160</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Ratcheted tagsets</td>
    </tr>
  </tbody>
</table>
**自适应前瞻：**

```python
# Dynamic look-ahead based on highest tag received
look_ahead = min(tsmax, tsmin + N // 4)

# Example:
# tsmin = 24, tsmax = 160
# N = 0:   look_ahead = min(160, 24 + 0/4) = 24
# N = 100: look_ahead = min(160, 24 + 100/4) = 49
# N = 500: look_ahead = min(160, 24 + 500/4) = 149
# N = 544: look_ahead = min(160, 24 + 544/4) = 160
```
**Trim Behind（向后裁剪）：**

```python
# Trim tags far behind highest received
trim_behind = look_ahead // 2

# If highest received tag is N=100, trim tags below N=50
```
**内存计算:**

```python
# Per tag: 8 bytes (tag) + 2 bytes (index) + overhead ≈ 16 bytes
# Look-ahead of 160 tags ≈ 2.5 KB per inbound tagset

# With multiple sessions:
# 100 inbound sessions × 2.5 KB = 250 KB total
```
### 会话标签乱序处理

**场景**: 消息乱序到达

```
Expected: tag_5, tag_6, tag_7, tag_8
Received: tag_5, tag_7, tag_6, tag_8
```
**接收端行为：**

1. 接收 tag_5:
   - 查找: 在索引 5 处找到
   - 处理消息
   - 移除 tag_5
   - 已接收的最高编号: 5

2. 接收 tag_7 (乱序):
   - 查找：在索引 7 处找到
   - 处理消息
   - 移除 tag_7
   - 已接收的最高值：7
   - 注意：tag_6 仍在存储中(尚未接收)

3. 接收 tag_6 (延迟):
   - 查找: 在索引 6 处找到
   - 处理消息
   - 移除 tag_6
   - 最高已接收: 7 (未变)

4. 接收 tag_8：
   - 查找：在索引 8 处找到
   - 处理消息
   - 移除 tag_8
   - 已接收的最高序号：8

**窗口维护：** - 跟踪已接收的最高索引 - 维护缺失索引（缺口）列表 - 根据最高索引扩展窗口 - 可选：在超时后使旧的缺口失效

### 对称密钥棘轮

对称密钥棘轮生成与会话标签同步的 32 字节加密密钥。

### 对称密钥棘轮的目的

- 为每条消息提供唯一的加密密钥
- 与会话标签棘轮同步（使用相同索引）
- 发送方可按需生成
- 接收方可延迟生成，直到收到会话标签

### 对称密钥棘轮公式

**初始化：**

```python
# From DH_INITIALIZE
symmKey_ck = initial_chain_key  # 32 bytes

# No additional initialization needed
# Unlike session tag ratchet, no constant is derived
```
**密钥生成（针对密钥 N）：**

```python
# Generate key N
SYMMKEY_CONSTANT = ZEROLEN  # Empty string
keydata = HKDF(symmKey_chainKey_(N-1), SYMMKEY_CONSTANT, "SymmetricRatchet", 64)
symmKey_chainKey_N = keydata[0:31]  # Chain key for next key
key_N = keydata[32:63]              # Session key (32 bytes)
```
**完整序列：**

```python
# Key 0
keydata_0 = HKDF(symmKey_ck, ZEROLEN, "SymmetricRatchet", 64)
symmKey_chainKey_0 = keydata_0[0:31]
key_0 = keydata_0[32:63]

# Key 1
keydata_1 = HKDF(symmKey_chainKey_0, ZEROLEN, "SymmetricRatchet", 64)
symmKey_chainKey_1 = keydata_1[0:31]
key_1 = keydata_1[32:63]

# Key N
keydata_N = HKDF(symmKey_chainKey_(N-1), ZEROLEN, "SymmetricRatchet", 64)
symmKey_chainKey_N = keydata_N[0:31]
key_N = keydata_N[32:63]
```
### 对称密钥棘轮发送方实现

```python
class OutboundKeyRatchet:
    def __init__(self, symmKey_ck):
        self.chainKey = symmKey_ck
        self.index = -1
    
    def get_key(self, index):
        """Generate key for specific index"""
        # Fast-forward to desired index if needed
        while self.index < index:
            self.index += 1
            keydata = HKDF(self.chainKey, ZEROLEN, "SymmetricRatchet", 64)
            self.chainKey = keydata[0:31]
            if self.index == index:
                return keydata[32:63]
        
        # Should not reach here if called correctly
        raise ValueError("Key already generated")
```
**发送方流程：** 1. 获取下一个标签及其索引 N 2. 为索引 N 生成密钥 3. 使用该密钥加密消息 4. 无需存储密钥

### 对称密钥棘轮接收方实现

**策略 1：延迟生成（推荐）**

```python
class InboundKeyRatchet:
    def __init__(self, symmKey_ck):
        self.chainKey = symmKey_ck
        self.index = -1
        self.cache = {}  # Optional: cache recently used keys
    
    def get_key(self, index):
        """Generate key for specific index"""
        # Check cache first (optional optimization)
        if index in self.cache:
            key = self.cache[index]
            del self.cache[index]
            return key
        
        # Fast-forward to desired index
        while self.index < index:
            self.index += 1
            keydata = HKDF(self.chainKey, ZEROLEN, "SymmetricRatchet", 64)
            self.chainKey = keydata[0:31]
            
            if self.index == index:
                return keydata[32:63]
        
        raise ValueError("Index already passed")
```
**延迟生成流程：** 1. 接收带有标签的 ES message（ES 消息） 2. 查找该标签以获得索引 N 3. 生成从 0 到 N 的密钥（如果尚未生成） 4. 使用密钥 N 解密消息 5. 链密钥现在位于索引 N

**优点:** - 内存占用最小 - 仅在需要时才生成密钥 - 实现简单

**缺点：** - 首次使用时必须生成从 0 到 N 的所有密钥 - 在没有缓存的情况下无法处理乱序消息

**策略 2：使用标签窗口的预生成（替代方案）**

```python
class InboundKeyRatchet:
    def __init__(self, symmKey_ck):
        self.chainKey = symmKey_ck
        self.index = -1
        self.keys = {}  # Dictionary: index -> key
    
    def extend(self, count):
        """Pre-generate 'count' more keys"""
        for _ in range(count):
            self.index += 1
            keydata = HKDF(self.chainKey, ZEROLEN, "SymmetricRatchet", 64)
            self.chainKey = keydata[0:31]
            key = keydata[32:63]
            self.keys[self.index] = key
    
    def get_key(self, index):
        """Retrieve pre-generated key"""
        if index in self.keys:
            key = self.keys[index]
            del self.keys[index]
            return key
        return None
```
**预生成流程：** 1. 预生成与标签窗口相匹配的密钥（例如，32 个密钥） 2. 将密钥按消息编号建立索引并存储 3. 当收到标签时，查找对应的密钥 4. 随着标签被使用，扩展窗口

**优势：** - 自然处理乱序消息 - 密钥检索速度快 (无生成延迟)

**缺点：** - 更高的内存占用（每个密钥 32 字节，相比每个标签 8 字节） - 必须使密钥与标签保持同步

**内存比较:**

```python
# Look-ahead of 160:
# Tags only:  160 × 16 bytes = 2.5 KB
# Tags+Keys:  160 × (16 + 32) bytes = 7.5 KB
# 
# For 100 sessions:
# Tags only:  250 KB
# Tags+Keys:  750 KB
```
### 使用会话标签的对称棘轮同步

**关键要求**: 会话标签索引必须等于对称密钥索引

```python
# Sender
tag, index = outbound_tagset.get_next_tag()
key = outbound_keyratchet.get_key(index)  # Same index
nonce = construct_nonce(index)
ciphertext = ENCRYPT(key, nonce, payload, tag)

# Receiver
index = inbound_tagset.lookup_tag(tag)
key = inbound_keyratchet.get_key(index)  # Same index
nonce = construct_nonce(index)
plaintext = DECRYPT(key, nonce, ciphertext, tag)
```
**失效模式：**

如果同步中断： - 解密使用了错误的密钥 - MAC（消息认证码）验证失败 - 消息被拒绝

**预防：** - 始终为标签和密钥使用相同的索引 - 绝不要在任一 ratchet（密钥棘轮）中跳过索引 - 谨慎处理乱序消息

### 对称棘轮的一次性随机数构造

Nonce（一次性随机数）源自消息编号：

```python
def construct_nonce(index):
    """
    Construct 12-byte nonce for ChaCha20-Poly1305
    
    Args:
        index: Message number (0-65535)
    
    Returns:
        nonce: 12-byte nonce
    """
    # First 4 bytes are always zero
    nonce = bytearray(12)
    nonce[0:4] = b'\x00\x00\x00\x00'
    
    # Last 8 bytes are little-endian message number
    nonce[4:12] = index.to_bytes(8, byteorder='little')
    
    return bytes(nonce)
```
**示例：**

```python
index = 0:     nonce = 0x00000000 0000000000000000
index = 1:     nonce = 0x00000000 0100000000000000
index = 255:   nonce = 0x00000000 FF00000000000000
index = 256:   nonce = 0x00000000 0001000000000000
index = 65535: nonce = 0x00000000 FFFF000000000000
```
**重要属性：** - Nonces（一次性随机数）对于标签集中的每条消息都是唯一的 - Nonces 永不重复（一次性标签可确保这一点） - 8 字节计数器允许 2^64 条消息（我们只使用 2^16） - Nonce 格式符合 RFC 7539 的基于计数器的构造

---

## 会话管理

### 会话上下文

所有入站和出站会话都必须属于特定的上下文：

1. **Router 上下文**: 为 router 本身的会话
2. **目标上下文**: 为特定本地目标（客户端应用）的会话

**关键规则**: 为防止关联攻击，会话不得在不同上下文之间共享。

**实现：**

```python
class SessionKeyManager:
    """Context for managing sessions (router or destination)"""
    def __init__(self, context_id):
        self.context_id = context_id
        self.inbound_sessions = {}   # far_end_dest -> [sessions]
        self.outbound_sessions = {}  # far_end_dest -> session
        self.static_keypair = generate_keypair()  # Context's identity
    
    def get_outbound_session(self, destination):
        """Get or create outbound session to destination"""
        if destination not in self.outbound_sessions:
            self.outbound_sessions[destination] = create_outbound_session(destination)
        return self.outbound_sessions[destination]
    
    def add_inbound_session(self, session, destination=None):
        """Add inbound session, optionally bound to destination"""
        if destination:
            if destination not in self.inbound_sessions:
                self.inbound_sessions[destination] = []
            self.inbound_sessions[destination].append(session)
        else:
            # Unbound session
            self.inbound_sessions[None].append(session)
```
**Java I2P 实现：**

在 Java I2P 中，`SessionKeyManager` 类提供以下功能： - 每个 router 一个 `SessionKeyManager` - 每个本地 destination（目的地）一个 `SessionKeyManager` - 在每个上下文内分别管理 ECIES 和 ElGamal 会话

### 会话绑定

**绑定** 将会话与特定的远端目标关联起来。

### 绑定会话

**特性：** - 在 NS message（NS 握手消息）中包含发送方的静态密钥 - 接收方可以识别发送方的目的地 - 支持双向通信 - 每个目的地仅一个出站会话 - 可能存在多个入站会话（在过渡期间）

**用例：** - 流式连接（类似 TCP） - 可回复的数据报 - 任何需要请求/响应的协议

**绑定过程：**

```python
# Alice creates bound outbound session
outbound_session = OutboundSession(
    destination=bob_destination,
    static_key=alice_static_key,
    bound=True
)

# Alice sends NS with static key
ns_message = build_ns_message(
    ephemeral_key=alice_ephemeral_key,
    static_key=alice_static_key,  # Included for binding
    payload=data
)

# Bob receives NS
bob_receives_ns(ns_message)
# Bob extracts Alice's static key
alice_static_key = decrypt_static_key_section(ns_message)

# Bob looks up Alice's destination (from bundled LeaseSet)
alice_destination = lookup_destination_by_static_key(alice_static_key)

# Bob creates bound inbound session
inbound_session = InboundSession(
    destination=alice_destination,
    bound=True
)

# Bob pairs with outbound session
outbound_session = OutboundSession(
    destination=alice_destination,
    bound=True
)
```
**优势:** 1. **Ephemeral-Ephemeral DH**: 回应使用 ee DH（临时-临时 Diffie-Hellman，完全前向保密） 2. **会话连续性**: Ratchets（棘轮机制）保持与同一目标的绑定 3. **安全性**: 防止会话劫持（经静态密钥认证） 4. **效率**: 每个目标仅有一个会话（无重复）

### 未绑定会话

**特性：** - NS message（协议中的 NS 消息类型）中没有静态密钥（flags 字段全为 0） - 接收方无法识别发送方 - 仅支持单向通信 - 允许针对同一目标建立多个会话

**使用场景:** - 原始数据报（fire-and-forget，发后不管） - 匿名发布 - 广播式消息传递

**属性：** - 更匿名（无发送方身份标识） - 更高效（握手中 1 次 DH 对比 2 次 DH） - 无法回复（接收方不知道该回复到哪里） - 无会话棘轮机制（一次性或有限次使用）

### 会话配对

**配对** 将入站会话与出站会话连接起来，以进行双向通信。

### 创建配对会话

**Alice 的视角（发起方）：**

```python
# Create outbound session to Bob
outbound_session = create_outbound_session(bob_destination)

# Create paired inbound session
inbound_session = create_inbound_session(
    paired_with=outbound_session,
    bound_to=bob_destination
)

# Link them
outbound_session.paired_inbound = inbound_session
inbound_session.paired_outbound = outbound_session

# Send NS message
send_ns_message(outbound_session, payload)
```
**Bob 的视角（响应方）：**

```python
# Receive NS message
ns_message = receive_ns_message()

# Create inbound session
inbound_session = create_inbound_session_from_ns(ns_message)

# If NS contains static key (bound):
if ns_message.has_static_key():
    alice_destination = extract_destination(ns_message)
    inbound_session.bind_to(alice_destination)
    
    # Create paired outbound session
    outbound_session = create_outbound_session(alice_destination)
    
    # Link them
    outbound_session.paired_inbound = inbound_session
    inbound_session.paired_outbound = outbound_session

# Send NSR
send_nsr_message(inbound_session, outbound_session, payload)
```
### 会话配对的优势

1. **带内 ACK**: 无需单独的 clove（garlic encryption 中的子消息）即可确认消息
2. **高效棘轮**: 双向棘轮同步推进
3. **流量控制**: 可以在配对会话之间实现背压
4. **状态一致性**: 更易维护同步状态

### 会话配对规则

- 出站会话可能未配对（未绑定的 NS）
- 已绑定 NS 的入站会话应当配对
- 配对发生在会话创建时，而不是之后
- 已配对的会话绑定到相同的目标
- 棘轮过程相互独立，但保持协调

### 会话生命周期

### 会话生命周期：创建阶段

**出站会话创建 (Alice):**

```python
def create_outbound_session(destination, bound=True):
    session = OutboundSession()
    session.destination = destination
    session.bound = bound
    session.state = SessionState.NEW
    session.created_time = now()
    
    # Generate keys for NS message
    session.ephemeral_keypair = generate_elg2_keypair()
    if bound:
        session.static_key = context.static_keypair.public_key
    
    # Will be populated after NSR received
    session.outbound_tagset = None
    session.inbound_tagset = None
    
    return session
```
**入站会话创建 (Bob):**

```python
def create_inbound_session_from_ns(ns_message):
    session = InboundSession()
    session.state = SessionState.ESTABLISHED
    session.created_time = now()
    
    # Extract from NS
    session.remote_ephemeral_key = ns_message.ephemeral_key
    session.remote_static_key = ns_message.static_key
    
    if session.remote_static_key:
        session.bound = True
        session.destination = lookup_destination(session.remote_static_key)
    else:
        session.bound = False
        session.destination = None
    
    # Generate keys for NSR
    session.ephemeral_keypair = generate_elg2_keypair()
    
    # Create tagsets from KDF
    session.inbound_tagset = create_tagset_from_nsr()
    session.outbound_tagset = create_tagset_from_nsr()
    
    return session
```
### 会话生命周期：活跃阶段

**状态转换:**

```
NEW (outbound only)
  ↓
  NS sent
  ↓
PENDING_REPLY (outbound only)
  ↓
  NSR received
  ↓
ESTABLISHED
  ↓
  ES messages exchanged
  ↓
ESTABLISHED (ongoing)
  ↓
  (optional) RATCHETING
  ↓
ESTABLISHED
```
**活跃会话维护：**

```python
def maintain_active_session(session):
    # Update last activity time
    session.last_activity = now()
    
    # Check for ratchet needed
    if session.outbound_tagset.needs_ratchet():
        initiate_ratchet(session)
    
    # Check for incoming ratchet
    if received_nextkey_block():
        process_ratchet(session)
    
    # Trim old tags from inbound tagset
    session.inbound_tagset.expire_old_tags()
    
    # Check session health
    if session.idle_time() > SESSION_TIMEOUT:
        mark_session_idle(session)
```
### 会话生命周期：过期阶段

**会话超时值：**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Session Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Sender Timeout</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Receiver Timeout</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR tagset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">N/A</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Short-lived</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ES tagset 0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Initial</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ES tagset 1+</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Ratcheted</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Old tagset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">N/A</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">After ratchet</td>
    </tr>
  </tbody>
</table>
**过期逻辑:**

```python
def check_session_expiration():
    for session in active_sessions:
        # Outbound session expiration (sender)
        if session.is_outbound():
            if session.idle_time() > 8 * 60:  # 8 minutes
                expire_outbound_session(session)
        
        # Inbound session expiration (receiver)
        else:
            if session.idle_time() > 10 * 60:  # 10 minutes
                expire_inbound_session(session)
    
    # Old tagsets (after ratchet)
    for tagset in old_tagsets:
        if tagset.age() > 3 * 60:  # 3 minutes
            delete_tagset(tagset)
```
**关键规则**：出站会话必须先于入站会话过期，以防止不同步。

**优雅终止：**

```python
def terminate_session(session, reason=0):
    # Send Termination block (if implemented)
    send_termination_block(session, reason)
    
    # Mark session for deletion
    session.state = SessionState.TERMINATED
    
    # Keep session briefly for final messages
    schedule_deletion(session, delay=30)  # 30 seconds
    
    # Notify paired session
    if session.paired_session:
        session.paired_session.mark_remote_terminated()
```
### 多个 NS 消息

**场景**：Alice 的 NS 消息丢失，或 NSR 应答丢失。

**Alice 的行为：**

```python
class OutboundSession:
    def __init__(self):
        self.ns_messages_sent = []
        self.ns_timer = None
        self.max_ns_attempts = 5
    
    def send_ns_message(self, payload):
        # Generate new ephemeral key for each NS
        ephemeral_key = generate_elg2_keypair()
        
        ns_message = build_ns_message(
            ephemeral_key=ephemeral_key,
            static_key=self.static_key,
            payload=payload
        )
        
        # Store state for this NS
        ns_state = {
            'ephemeral_key': ephemeral_key,
            'chainkey': compute_chainkey(ns_message),
            'hash': compute_hash(ns_message),
            'tagset': derive_nsr_tagset(ns_message),
            'sent_time': now()
        }
        self.ns_messages_sent.append(ns_state)
        
        # Send message
        send_message(ns_message)
        
        # Set timer for retry
        if not self.ns_timer:
            self.ns_timer = set_timer(1.0, self.on_ns_timeout)
    
    def on_ns_timeout(self):
        if len(self.ns_messages_sent) >= self.max_ns_attempts:
            # Give up
            fail_session("No NSR received after {self.max_ns_attempts} attempts")
            return
        
        # Retry with new NS message
        send_ns_message(self.payload)
    
    def on_nsr_received(self, nsr_message):
        # Cancel timer
        cancel_timer(self.ns_timer)
        
        # Find which NS this NSR responds to
        tag = nsr_message.tag
        for ns_state in self.ns_messages_sent:
            if tag in ns_state['tagset']:
                # This NSR corresponds to this NS
                self.active_ns_state = ns_state
                break
        
        # Process NSR and complete handshake
        complete_handshake(nsr_message, self.active_ns_state)
        
        # Discard other NS states
        self.ns_messages_sent = []
```
**重要属性：**

1. **独立的临时密钥**: 每个 NS 使用不同的临时密钥
2. **独立的握手**: 每个 NS 创建单独的握手状态
3. **NSR 关联**: NSR 标记用于标识其响应的是哪个 NS
4. **状态清理**: 在 NSR 成功后，未使用的 NS 状态将被丢弃

**防范攻击：**

为防止资源耗尽：

```python
# Limit NS sending rate
max_ns_rate = 5 per 10 seconds per destination

# Limit total NS attempts
max_ns_attempts = 5

# Limit total pending NS states
max_pending_ns = 10 per context
```
### 多个 NSR 消息

**场景**：Bob 发送多个 NSRs（回复消息；例如，将回复数据拆分为多条消息）。

**Bob 的行为：**

```python
class InboundSession:
    def send_nsr_replies(self, payload_chunks):
        # One NS received, multiple NSRs to send
        for chunk in payload_chunks:
            # Generate new ephemeral key for each NSR
            ephemeral_key = generate_elg2_keypair()
            
            # Get next tag from NSR tagset
            tag = self.nsr_tagset.get_next_tag()
            
            nsr_message = build_nsr_message(
                tag=tag,
                ephemeral_key=ephemeral_key,
                payload=chunk
            )
            
            send_message(nsr_message)
        
        # Wait for ES message from Alice
        self.state = SessionState.AWAITING_ES
```
**Alice 的行为:**

```python
class OutboundSession:
    def on_nsr_received(self, nsr_message):
        if self.state == SessionState.PENDING_REPLY:
            # First NSR received
            complete_handshake(nsr_message)
            self.state = SessionState.ESTABLISHED
            
            # Create ES sessions
            self.es_outbound_tagset = derive_es_outbound_tagset()
            self.es_inbound_tagset = derive_es_inbound_tagset()
            
            # Send ES message (ACK)
            send_es_message(empty_payload)
        
        elif self.state == SessionState.ESTABLISHED:
            # Additional NSR received
            # Decrypt and process payload
            payload = decrypt_nsr_payload(nsr_message)
            process_payload(payload)
            
            # These NSRs are from other NS attempts, ignore handshake
```
**Bob 的清理:**

```python
class InboundSession:
    def on_es_received(self, es_message):
        # First ES received from Alice
        # This confirms which NSR Alice used
        
        # Clean up other handshake states
        for other_ns_state in self.pending_ns_states:
            if other_ns_state != self.active_ns_state:
                delete_ns_state(other_ns_state)
        
        # Delete unused NSR tagsets
        for tagset in self.nsr_tagsets:
            if tagset != self.active_nsr_tagset:
                delete_tagset(tagset)
        
        self.state = SessionState.ESTABLISHED
```
**重要属性：**

1. **允许多个 NSR（NS 请求）**: Bob 可以针对每个 NS（会话）发送多个 NSR
2. **使用不同的临时密钥**: 每个 NSR 应使用唯一的临时密钥
3. **相同的 NSR tagset（标签集）**: 同一 NS 的所有 NSR 使用相同的 tagset
4. **先到的 ES（响应消息）胜出**: 由 Alice 首个到达的 ES 决定哪个 NSR 成功
5. **在 ES 之后清理**: 收到 ES 后，Bob 丢弃未使用的状态

### 会话状态机

**完整状态图：**

```
                    Outbound Session                    Inbound Session

                         NEW
                          |
                     send NS
                          |
                   PENDING_REPLY -------------------- receive NS ---> ESTABLISHED
                          |                                                |
                   receive NSR                                        send NSR
                          |                                                |
                    ESTABLISHED <---------- receive ES ------------- AWAITING_ES
                          |                     |                          |
                    ┌─────┴─────┐               |                    receive ES
                    |           |               |                          |
              send ES      receive ES           |                    ESTABLISHED
                    |           |               |                          |
                    └─────┬─────┘               |                ┌─────────┴─────────┐
                          |                     |                |                   |
                          |                     |          send ES              receive ES
                          |                     |                |                   |
                          |                     |                └─────────┬─────────┘
                          |                     |                          |
                          └─────────────────────┴──────────────────────────┘
                                              ACTIVE
                                                |
                                         idle timeout
                                                |
                                             EXPIRED
```
**状态描述：**

- **NEW**: 已创建出站会话，尚未发送 NS（握手消息）
- **PENDING_REPLY**: 已发送 NS，正在等待 NSR（握手响应消息）
- **AWAITING_ES**: 已发送 NSR，正在等待来自 Alice 的首个 ES（加密数据消息）
- **ESTABLISHED**: 握手完成，可以发送/接收 ES
- **ACTIVE**: 正在主动交换 ES 消息
- **RATCHETING**: DH ratchet（Diffie-Hellman 棘轮，密钥轮换过程）进行中（ACTIVE 的子集）
- **EXPIRED**: 会话超时，待删除
- **TERMINATED**: 会话被显式终止

---

## 有效载荷格式

所有 ECIES（椭圆曲线集成加密方案）消息（NS、NSR、ES）的负载部分使用一种与 NTCP2 类似的基于块的格式。

### 块结构

**通用格式:**

```
+----+----+----+----+----+----+----+----+
|blk |  size   |       data             |
+----+----+----+                        +
|                                       |
~               ...                     ~
|                                       |
+----+----+----+----+----+----+----+----+
|blk |  size   |       data             |
+----+----+----+                        +
|                                       |
~               ...                     ~
|                                       |
+----+----+----+----+----+----+----+----+
```
**字段：**

- `blk`: 1 字节 - 块类型编号
- `size`: 2 字节 - 数据字段的大端序大小 (0-65516)
- `data`: 可变长度 - 块特定数据

**约束：**

- 最大 ChaChaPoly 帧：65535 字节
- Poly1305 MAC：16 字节
- 最大总块大小：65519 字节 (65535 - 16)
- 最大单个块：65519 字节 (包含 3 字节头部)
- 最大单个块数据：65516 字节

### 块类型

**已定义的块类型：**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DateTime</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">7 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Required in NS</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1-3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Future use</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Termination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">9+ bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unimplemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Session termination</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Options</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">21+ bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unimplemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Session options</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">MessageNumbers</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">5 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unimplemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">PN value</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NextKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">3 or 35 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DH ratchet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ACK</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">4+ bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Message acknowledgment</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">9</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ACK Request</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">3 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Request ACK</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Future use</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Garlic Clove</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Variable</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Application data</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12-223</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Future use</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">224-253</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Variable</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Testing features</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">254</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Padding</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Variable</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Traffic shaping</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">255</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Future extension</td>
    </tr>
  </tbody>
</table>
**未知块处理：**

各实现必须（MUST）忽略具有未知类型编号的块，并将其视为填充。这可确保前向兼容性。

### 块排序规则

### NS 消息排序

**必需：** - DateTime 块必须位于首位

**允许：** - Garlic Clove (蒜瓣) (类型 11) - 选项 (类型 5) - 若已实现 - 填充 (类型 254)

**禁止：** - NextKey, ACK, ACK Request, Termination, MessageNumbers

**有效的 NS 载荷示例：**

```
DateTime (0) | Garlic Clove (11) | Garlic Clove (11) | Padding (254)
```
### NSR 消息排序

**必需：** - 无（有效载荷可能为空）

**允许：** - Garlic Clove（garlic encryption 的子消息） (type 11) - 选项 (type 5) - 如已实现 - 填充 (type 254)

**禁止：** - DateTime, NextKey, ACK, ACK Request, Termination, MessageNumbers

**有效的 NSR 负载示例：**

```
Garlic Clove (11) | Garlic Clove (11) | Padding (254)
```
或

```
(empty - ACK only)
```
### ES 消息顺序

**必需：** - 无（有效载荷可为空）

**允许（任意顺序）：** - Garlic Clove (type 11) - NextKey (type 7) - ACK (type 8) - ACK Request (type 9) - Termination (type 4) - 如果已实现 - MessageNumbers (type 6) - 如果已实现 - Options (type 5) - 如果已实现 - Padding (type 254)

**特殊规则：** - Termination（终止）必须为最后一个块（除 Padding（填充）外） - Padding 必须为最后一个块 - 允许多个 Garlic Cloves（蒜瓣） - 最多允许 2 个 NextKey blocks（NextKey 块）（正向和反向） - 不允许多个 Padding 块

**ES 有效载荷示例：**

```
Garlic Clove (11) | ACK (8) | Padding (254)
```
```
NextKey (7) | Garlic Clove (11) | Garlic Clove (11)
```
```
NextKey (7) forward | NextKey (7) reverse | Garlic Clove (11)
```
```
ACK Request (9) | Garlic Clove (11) | Termination (4) | Padding (254)
```
### DateTime 块（类型 0）

**用途**: 用于防重放和时钟偏移校验的时间戳

**大小**: 7 字节（3 字节头部 + 4 字节数据）

**格式：**

```
+----+----+----+----+----+----+----+
| 0  |    4    |     timestamp     |
+----+----+----+----+----+----+----+
```
**字段:**

- `blk`: 0
- `size`: 4（大端序）
- `timestamp`: 4 字节 - 以秒为单位的 Unix 时间戳（无符号，大端序）

**时间戳格式：**

```python
timestamp = int(time.time())  # Seconds since 1970-01-01 00:00:00 UTC
# Wraps around in year 2106 (4-byte unsigned maximum)
```
**验证规则：**

```python
MAX_CLOCK_SKEW_PAST = 5 * 60      # 5 minutes
MAX_CLOCK_SKEW_FUTURE = 2 * 60    # 2 minutes

def validate_datetime(timestamp):
    now = int(time.time())
    age = now - timestamp
    
    if age < -MAX_CLOCK_SKEW_FUTURE:
        return False  # Too far in future
    
    if age > MAX_CLOCK_SKEW_PAST:
        return False  # Too old
    
    return True
```
**重放防护：**

```python
class ReplayFilter:
    def __init__(self, duration=5*60):
        self.duration = duration  # 5 minutes
        self.seen_messages = BloomFilter(size=100000, false_positive_rate=0.001)
        self.cleanup_timer = RepeatTimer(60, self.cleanup)
    
    def check_replay(self, ephemeral_key, timestamp):
        # Check timestamp validity
        if not validate_datetime(timestamp):
            return False
        
        # Check if ephemeral key seen recently
        if ephemeral_key in self.seen_messages:
            return False  # Replay attack
        
        # Add to seen messages
        self.seen_messages.add(ephemeral_key)
        return True
    
    def cleanup(self):
        # Expire old entries (Bloom filter automatically ages out)
        pass
```
**实现说明：**

1. **NS Messages（NS 消息）**: DateTime 必须是第一个块
2. **NSR/ES Messages（NSR/ES 消息）**: 通常不包含 DateTime
3. **重放窗口**: 建议的最小值为 5 分钟
4. **布隆过滤器**: 建议用于高效的重放检测
5. **时钟偏差**: 允许落后 5 分钟、超前 2 分钟

### Garlic Clove Block（蒜瓣块） (Type 11)

**目的**: 封装 I2NP 消息以便传递

**格式：**

```
+----+----+----+----+----+----+----+----+
| 11 |  size   |                        |
+----+----+----+                        +
|      Delivery Instructions            |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|type|  Message_ID       | Expiration  |
+----+----+----+----+----+----+----+----+
     |      I2NP Message body           |
+----+                                  +
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
```
**字段：**

- `blk`: 11
- `size`: 蒜瓣的总大小（可变）
- `Delivery Instructions`: 如 I2NP 规范所述
- `type`: I2NP 消息类型（1 字节）
- `Message_ID`: I2NP 消息 ID（4 字节）
- `Expiration`: 以秒为单位的 Unix 时间戳（4 字节）
- `I2NP Message body`: 可变长度的消息数据

**投递指令格式:**

**本地投递** (1 字节):

```
+----+
|0x00|
+----+
```
**目的地递送** (33 字节):

```
+----+----+----+----+----+----+----+----+
|0x01|                                  |
+----+        Destination Hash         +
|              32 bytes                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
**Router Delivery** (33 字节):

```
+----+----+----+----+----+----+----+----+
|0x02|                                  |
+----+         Router Hash              +
|              32 bytes                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
**Tunnel 投递** (37 字节):

```
+----+----+----+----+----+----+----+----+
|0x03|         Tunnel ID                |
+----+----+----+----+----+              +
|           Router Hash                 |
+              32 bytes                 +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
**I2NP 消息头** (共 9 字节):

```
+----+----+----+----+----+----+----+----+
|type|      msg_id       |  expiration   |
+----+----+----+----+----+----+----+----+
     |                                   |
```
- `type`: I2NP 消息类型（Database Store、Database Lookup、Data 等）
- `msg_id`: 4 字节消息标识符
- `expiration`: 4 字节 Unix 时间戳（秒）

**与 ElGamal 蒜瓣格式相比的重要差异：**

1. **无证书**: 证书字段省略（在 ElGamal（公钥加密算法）中未使用）
2. **无 Clove ID**: Clove（蒜瓣）ID 省略（过去始终为 0）
3. **无 Clove 过期时间**: 改用 I2NP 消息过期时间
4. **紧凑头部**: 9 字节的 I2NP 头部，相比更大的 ElGamal 格式
5. **每个 Clove 为独立块**: 无 CloveSet（Clove 集合）结构

**多个 Cloves（蒜瓣）:**

```python
# Multiple Garlic Cloves in one message
payload = [
    build_datetime_block(),
    build_garlic_clove(i2np_message_1),
    build_garlic_clove(i2np_message_2),
    build_garlic_clove(i2np_message_3),
    build_padding_block()
]
```
**Cloves（蒜瓣）中的常见 I2NP 消息类型:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseStore</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Publishing LeaseSet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseLookup</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Requesting LeaseSet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DeliveryStatus</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ACK (legacy, avoid in ECIES)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Streaming data</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">21</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Garlic</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Nested garlic messages</td>
    </tr>
  </tbody>
</table>
**蒜瓣处理：**

```python
def process_garlic_clove(clove_data):
    # Parse delivery instructions
    delivery_type = clove_data[0]
    
    if delivery_type == 0x00:
        # Local delivery
        offset = 1
    elif delivery_type == 0x01:
        # Destination delivery
        dest_hash = clove_data[1:33]
        offset = 33
    elif delivery_type == 0x02:
        # Router delivery
        router_hash = clove_data[1:33]
        offset = 33
    elif delivery_type == 0x03:
        # Tunnel delivery
        tunnel_id = struct.unpack('>I', clove_data[1:5])[0]
        router_hash = clove_data[5:37]
        offset = 37
    
    # Parse I2NP header
    i2np_type = clove_data[offset]
    msg_id = struct.unpack('>I', clove_data[offset+1:offset+5])[0]
    expiration = struct.unpack('>I', clove_data[offset+5:offset+9])[0]
    
    # Extract I2NP body
    i2np_body = clove_data[offset+9:]
    
    # Process message
    process_i2np_message(i2np_type, msg_id, expiration, i2np_body)
```
### NextKey (下一密钥) 块 (类型 7)

**用途**: DH 棘轮密钥交换

**格式（包含键 - 38 字节）：**

```
+----+----+----+----+----+----+----+----+
| 7  |   35    |flag|  key ID |         |
+----+----+----+----+----+----+         +
|                                       |
+     Next DH Ratchet Public Key        +
|              32 bytes                 |
+                                       +
|                                       |
+                             +----+----+
|                             |
+----+----+----+----+----+----+
```
**格式 (仅密钥 ID - 6 字节):**

```
+----+----+----+----+----+----+
| 7  |    3    |flag|  key ID |
+----+----+----+----+----+----+
```
**字段：**

- `blk`: 7
- `size`: 3 (仅 ID) 或 35 (带密钥)
- `flag`: 1 字节 - 标志位
- `key ID`: 2 字节 - 大端序的密钥标识符 (0-32767)
- `Public Key`: 32 字节 - X25519 公钥 (小端序), 若标志位 0 = 1

**标志位：**

```
Bit 7 6 5 4 3 2 1 0
    | | | | | | | |
    | | | | | | | +-- Bit 0: Key present (1) or ID only (0)
    | | | | | | +---- Bit 1: Reverse key (1) or forward key (0)
    | | | | | +------ Bit 2: Request reverse key (1) or no request (0)
    | | | | |
    +-+-+-+-+-------- Bits 3-7: Reserved (set to 0)
```
**标志示例：**

```python
# Forward key present
flags = 0x01  # Binary: 00000001

# Reverse key present
flags = 0x03  # Binary: 00000011

# Forward key ID only (ACK)
flags = 0x00  # Binary: 00000000

# Reverse key ID only (ACK)
flags = 0x02  # Binary: 00000010

# Forward key ID with reverse request
flags = 0x04  # Binary: 00000100
```
**密钥 ID 规则：**

- ID 按顺序递增：0, 1, 2, ..., 32767
- ID 仅在生成新密钥时递增
- 在下一次 ratchet（棘轮机制）之前，同一个 ID 会用于多条消息
- 最大 ID 为 32767（之后必须开始新的会话）

**使用示例：**

```python
# Initiating ratchet (sender generates new key)
nextkey = NextKeyBlock(
    flags=0x01,           # Key present, forward
    key_id=0,
    public_key=sender_new_pk
)

# Replying to ratchet (receiver generates new key)
nextkey = NextKeyBlock(
    flags=0x03,           # Key present, reverse
    key_id=0,
    public_key=receiver_new_pk
)

# Acknowledging ratchet (no new key from sender)
nextkey = NextKeyBlock(
    flags=0x02,           # ID only, reverse
    key_id=0
)

# Requesting reverse ratchet
nextkey = NextKeyBlock(
    flags=0x04,           # Request reverse, forward ID
    key_id=1
)
```
**处理逻辑：**

```python
def process_nextkey_block(block):
    flags = block.flags
    key_id = block.key_id
    
    key_present = (flags & 0x01) != 0
    is_reverse = (flags & 0x02) != 0
    request_reverse = (flags & 0x04) != 0
    
    if key_present:
        public_key = block.public_key
        
        if is_reverse:
            # Reverse key received
            perform_dh_ratchet(receiver_key=public_key, key_id=key_id)
            # Sender should ACK with own key ID
        else:
            # Forward key received
            perform_dh_ratchet(sender_key=public_key, key_id=key_id)
            # Receiver should reply with reverse key
            send_reverse_key(generate_new_key())
    
    else:
        # Key ID only (ACK)
        if is_reverse:
            # Reverse key ACK
            confirm_reverse_ratchet(key_id)
        else:
            # Forward key ACK
            confirm_forward_ratchet(key_id)
    
    if request_reverse:
        # Sender requests receiver to generate new key
        send_reverse_key(generate_new_key())
```
**多个 NextKey（下一密钥）块：**

当双向同时进行棘轮推进（ratcheting）时，单个 ES message（ES 消息）最多可包含 2 个 NextKey blocks（NextKey 块）：

```python
# Both directions ratcheting
payload = [
    NextKeyBlock(flags=0x01, key_id=2, public_key=forward_key),  # Forward
    NextKeyBlock(flags=0x03, key_id=1, public_key=reverse_key),  # Reverse
    build_garlic_clove(data)
]
```
### ACK（确认）块（类型 8）

**目的**: 在带内确认已接收的消息

**格式（单个 ACK - 7 字节）：**

```
+----+----+----+----+----+----+----+
| 8  |    4    |tagsetid |   N     |
+----+----+----+----+----+----+----+
```
**格式（多个 ACK（确认））：**

```
+----+----+----+----+----+----+----+----+
| 8  |  size   |tagsetid |   N     |    |
+----+----+----+----+----+----+----+    +
|            more ACKs                  |
~               ...                     ~
|                                       |
+----+----+----+----+----+----+----+----+
```
**字段：**

- `blk`: 8
- `size`: 4 * ACK（确认）数量（最少 4）
- 对于每个 ACK:
  - `tagsetid`: 2 字节 - 大端序的标签集 ID（0-65535）
  - `N`: 2 字节 - 大端序的消息编号（0-65535）

**标签集 ID 的确定:**

```python
# Tag set 0 (initial, after NSR)
tagset_id = 0

# After first ratchet (tag set 1)
# Both Alice and Bob sent key ID 0
tagset_id = 1 + 0 + 0 = 1

# After second ratchet (tag set 2)
# Alice sent key ID 1, Bob still using key ID 0
tagset_id = 1 + 1 + 0 = 2

# After third ratchet (tag set 3)
# Alice still using key ID 1, Bob sent key ID 1
tagset_id = 1 + 1 + 1 = 3
```
**单个 ACK（确认）示例：**

```python
# ACK message from tag set 5, message number 127
ack_block = ACKBlock(
    tagset_id=5,
    message_number=127
)

# Wire format (7 bytes):
# 08 00 04 00 05 00 7F
# |  |  |  |  |  |  |
# |  |  |  |  |  |  +-- N (127)
# |  |  |  |  +--------- N high byte
# |  |  |  +------------ tagset_id (5)
# |  |  +--------------- tagset_id high byte
# |  +------------------ size (4)
# +--------------------- type (8)
```
**多个 ACK 示例:**

```python
# ACK three messages
ack_block = ACKBlock([
    (tagset_id=3, N=42),
    (tagset_id=3, N=43),
    (tagset_id=4, N=0)
])

# Wire format (15 bytes):
# 08 00 0C 00 03 00 2A 00 03 00 2B 00 04 00 00
#                (ts=3, N=42) (ts=3, N=43) (ts=4, N=0)
```
**处理：**

```python
def process_ack_block(block):
    num_acks = block.size // 4
    
    for i in range(num_acks):
        offset = i * 4
        tagset_id = struct.unpack('>H', block.data[offset:offset+2])[0]
        message_num = struct.unpack('>H', block.data[offset+2:offset+4])[0]
        
        # Mark message as acknowledged
        mark_acked(tagset_id, message_num)
        
        # May trigger retransmission timeout cancellation
        cancel_retransmit_timer(tagset_id, message_num)
```
**何时发送确认(ACK):**

1. **显式 ACK（确认）请求**: 始终对 ACK 请求块作出响应
2. **LeaseSet 递送**: 当发送方在消息中包含 LeaseSet 时
3. **会话建立**: 可对 NS/NSR 进行 ACK（尽管协议更倾向于通过 ES 实现隐式 ACK）
4. **棘轮确认**: 可对 NextKey 的接收进行 ACK
5. **应用层**: 按更高层协议的要求（例如，Streaming）

**ACK（确认）时序:**

```python
class ACKManager:
    def __init__(self):
        self.pending_acks = []
        self.ack_timer = None
    
    def request_ack(self, tagset_id, message_num):
        self.pending_acks.append((tagset_id, message_num))
        
        if not self.ack_timer:
            # Delay ACK briefly to allow higher layer to respond
            self.ack_timer = set_timer(0.1, self.send_acks)  # 100ms
    
    def send_acks(self):
        if self.pending_acks and not has_outbound_data():
            # No higher layer data, send explicit ACK
            send_es_message(build_ack_block(self.pending_acks))
        
        # Otherwise, ACK will piggyback on next ES message
        self.pending_acks = []
        self.ack_timer = None
```
### ACK Request Block（确认请求块）（类型 9）

**目的**: 请求对当前消息进行带内确认

**格式：**

```
+----+----+----+----+
| 9  |    1    |flg |
+----+----+----+----+
```
**字段：**

- `blk`: 9
- `size`: 1
- `flg`: 1 字节 - 标志位（所有位当前未使用，设为 0）

**用法：**

```python
# Request ACK for this message
payload = [
    build_ack_request_block(),
    build_garlic_clove(important_data)
]
```
**接收方响应：**

收到 ACK 请求时：

1. **带即时数据**: 将 ACK 块包含在即时响应中
2. **无即时数据**: 启动定时器（例如，100ms），如果定时器到期则发送带 ACK 的空 ES
3. **标签集 ID**: 使用当前入站标签集 ID
4. **消息编号**: 使用与接收到的会话标签关联的消息编号

**处理：**

```python
def process_ack_request(message):
    # Extract message identification
    tagset_id = message.tagset_id
    message_num = message.message_num
    
    # Schedule ACK
    schedule_ack(tagset_id, message_num)
    
    # If no data to send immediately, start timer
    if not has_pending_data():
        set_timer(0.1, lambda: send_ack_only(tagset_id, message_num))
```
**何时使用 ACK 请求：**

1. **关键消息**: 必须收到确认的消息
2. **LeaseSet 传递**: 当捆绑一个 LeaseSet 时
3. **Session Ratchet**: （会话棘轮，一种会话密钥更新机制）在发送 NextKey block（NextKey 块，用于会话密钥更新）之后
4. **传输结束**: 当发送方没有更多数据可发送但希望得到确认时

**何时不应使用：**

1. **流式协议**: 流式层处理 ACK
2. **高频消息**: 避免对每条消息都发起 ACK 请求（额外开销）
3. **不重要的数据报**: 原始数据报通常不需要 ACK

### 终止块（类型 4）

**状态**: 未实现

**目的**: 优雅地终止会话

**格式：**

```
+----+----+----+----+----+----+----+----+
| 4  |  size   | rsn|     addl data     |
+----+----+----+----+                   +
~               ...                     ~
+----+----+----+----+----+----+----+----+
```
**字段：**

- `blk`: 4
- `size`: 1 个或更多字节
- `rsn`: 1 字节 - 原因代码
- `addl data`: 可选的附加数据 (格式取决于原因)

**原因代码：**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Meaning</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Additional Data</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Normal close / unspecified</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">None</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Termination received</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">None</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Idle timeout</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">None (implementation-specific)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Resource exhaustion</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">None (implementation-specific)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4+</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implementation-specific</td>
    </tr>
  </tbody>
</table>
**用法（实现后）：**

```python
# Normal session close
termination = TerminationBlock(
    reason=0,
    additional_data=b''
)

# Session termination due to received termination
termination = TerminationBlock(
    reason=1,
    additional_data=b''
)
```
**规则：**

- 除 Padding（填充）外，必须是最后一个块
- 如果存在，Padding 必须紧随 Termination（终止）之后
- 不允许出现在 NS 或 NSR 消息中
- 仅允许出现在 ES 消息中

### 选项块 (类型 5)

**状态**: 未实现

**目的**: 协商会话参数

**格式：**

```
+----+----+----+----+----+----+----+----+
| 5  |  size   |ver |flg |STL |STimeout |
+----+----+----+----+----+----+----+----+
|  SOTW   |  RITW   |tmin|tmax|rmin|rmax|
+----+----+----+----+----+----+----+----+
|  tdmy   |  rdmy   |  tdelay |  rdelay |
+----+----+----+----+----+----+----+----+
|              more_options             |
~               ...                     ~
|                                       |
+----+----+----+----+----+----+----+----+
```
**字段：**

- `blk`: 5
- `size`: 21 字节或以上
- `ver`: 1 字节 - 协议版本（必须为 0）
- `flg`: 1 字节 - 标志位（当前所有位未使用）
- `STL`: 1 字节 - 会话标签长度（必须为 8）
- `STimeout`: 2 字节 - 会话空闲超时（以秒为单位，大端序）
- `SOTW`: 2 字节 - 发送方出站标签窗口（大端序）
- `RITW`: 2 字节 - 接收方入站标签窗口（大端序）
- `tmin`, `tmax`, `rmin`, `rmax`: 各 1 字节 - 填充参数（4.4 固定点）
- `tdmy`: 2 字节 - 愿意发送的最大填充流量（字节/秒，大端序）
- `rdmy`: 2 字节 - 请求的填充流量（字节/秒，大端序）
- `tdelay`: 2 字节 - 愿意插入的最大消息内延迟（毫秒，大端序）
- `rdelay`: 2 字节 - 请求的消息内延迟（毫秒，大端序）
- `more_options`: 变长 - 未来扩展

**填充参数 (4.4 定点数):**

```python
def encode_padding_ratio(ratio):
    """
    Encode padding ratio as 4.4 fixed-point
    
    ratio: 0.0 to 15.9375
    returns: 0x00 to 0xFF
    """
    return int(ratio * 16)

def decode_padding_ratio(encoded):
    """
    Decode 4.4 fixed-point to ratio
    
    encoded: 0x00 to 0xFF
    returns: 0.0 to 15.9375
    """
    return encoded / 16.0

# Examples:
# 0x00 = 0.0 (no padding)
# 0x01 = 0.0625 (6.25% padding)
# 0x10 = 1.0 (100% padding - double traffic)
# 0x80 = 8.0 (800% padding - 9x traffic)
# 0xFF = 15.9375 (1593.75% padding)
```
**标签窗口协商：**

```python
# SOTW: Sender's recommendation for receiver's inbound window
# RITW: Sender's declaration of own inbound window

# Receiver calculates actual inbound window:
inbound_window = calculate_window(
    sender_suggestion=SOTW,
    own_constraints=MAX_INBOUND_TAGS,
    own_resources=available_memory()
)

# Sender uses:
# - RITW to know how far ahead receiver will accept
# - Own SOTW to hint optimal window size
```
**默认值（未协商选项时）：**

```python
DEFAULT_OPTIONS = {
    'version': 0,
    'session_tag_length': 8,
    'session_timeout': 600,  # 10 minutes
    'sender_outbound_tag_window': 160,
    'receiver_inbound_tag_window': 160,
    'tmin': 0x00,  # No minimum padding
    'tmax': 0x10,  # Up to 100% padding
    'rmin': 0x00,  # No minimum requested
    'rmax': 0x10,  # Up to 100% requested
    'tdmy': 0,     # No dummy traffic
    'rdmy': 0,     # No dummy traffic requested
    'tdelay': 0,   # No delay
    'rdelay': 0    # No delay requested
}
```
### MessageNumbers 块 (类型 6)

**状态**: 未实现

**目的**: 指示在前一个标签集中发送的最后一条消息（从而实现序号缺失检测）

**格式：**

```
+----+----+----+----+----+
| 6  |    2    |  PN    |
+----+----+----+----+----+
```
**字段：**

- `blk`: 6
- `size`: 2
- `PN`: 2 字节 - 上一个标签集的最后消息编号（大端序，0-65535）

**PN (Previous Number，前一编号) 定义：**

PN 是上一标签集中最后发送的标签的索引。

**用法（实现后）：**

```python
# After ratcheting to new tag set
# Old tag set: sent messages 0-4095
# New tag set: sending first message

payload = [
    MessageNumbersBlock(PN=4095),
    build_garlic_clove(data)
]
```
**接收端的好处：**

```python
def process_message_numbers(pn_value):
    # Receiver can now:
    
    # 1. Determine if any messages were skipped
    highest_received_in_old_tagset = 4090
    if pn_value > highest_received_in_old_tagset:
        missing_count = pn_value - highest_received_in_old_tagset
        # 5 messages were never received
    
    # 2. Delete tags higher than PN from old tagset
    for tag_index in range(pn_value + 1, MAX_TAG_INDEX):
        delete_tag(old_tagset, tag_index)
    
    # 3. Expire tags ≤ PN after grace period (e.g., 2 minutes)
    schedule_deletion(old_tagset, delay=120)
```
**规则：**

- 在 tag set（标签集）0 中不得发送（没有先前的 tag set）
- 仅在 ES messages（ES 类型消息）中发送
- 仅在新的 tag set 的起始消息中发送
- PN value（PN 值）是从发送方的视角出发的（指发送方上一次发送的 tag）

**与 Signal 的关系：**

在 Signal Double Ratchet（双重棘轮算法）中，PN 位于消息头中。在 ECIES（椭圆曲线集成加密方案）中，它位于加密载荷内，且是可选的。

### Padding Block（填充块）(类型 254)

**Purpose**: 抵抗流量分析并对消息大小进行混淆

**格式：**

```
+----+----+----+----+----+----+----+----+
|254 |  size   |      padding           |
+----+----+----+                        +
|                                       |
~               ...                     ~
|                                       |
+----+----+----+----+----+----+----+----+
```
**字段：**

- `blk`: 254
- `size`: 0-65516 字节（大端序）
- `padding`: 随机或全零数据

**规则：**

- 必须是消息中的最后一个块
- 不允许存在多个填充块
- 可以为零长度（仅 3 字节头部）
- 填充数据可以为全零或随机字节

**默认填充：**

```python
DEFAULT_PADDING_MIN = 0
DEFAULT_PADDING_MAX = 15

def generate_default_padding():
    size = random.randint(DEFAULT_PADDING_MIN, DEFAULT_PADDING_MAX)
    data = random.bytes(size)  # or zeros
    return PaddingBlock(size, data)
```
**抗流量分析策略：**

**策略 1：随机大小（默认）**

```python
# Add 0-15 bytes random padding to each message
padding_size = random.randint(0, 15)
padding_block = PaddingBlock(padding_size, random.bytes(padding_size))
```
**策略 2：四舍五入到指定倍数**

```python
# Round total message size to next multiple of 64
target_size = ((message_size + 63) // 64) * 64
padding_size = target_size - message_size - 3  # -3 for block header
padding_block = PaddingBlock(padding_size, random.bytes(padding_size))
```
**策略 3：固定消息大小**

```python
# Always send 1KB messages
TARGET_MESSAGE_SIZE = 1024
padding_size = TARGET_MESSAGE_SIZE - message_size - 3
padding_block = PaddingBlock(padding_size, random.bytes(padding_size))
```
**策略 4：协商填充（选项块）**

```python
# Calculate padding based on negotiated parameters
# tmin, tmax from Options block
min_padding = int(payload_size * tmin_ratio)
max_padding = int(payload_size * tmax_ratio)
padding_size = random.randint(min_padding, max_padding)
padding_block = PaddingBlock(padding_size, random.bytes(padding_size))
```
**纯填充消息：**

消息可能完全由填充组成（无应用数据）：

```python
# Dummy traffic message
payload = [
    PaddingBlock(random.randint(100, 500), random.bytes(...))
]
```
**实现说明:**

1. **全零填充**: 可接受 (将由 ChaCha20 加密)
2. **随机填充**: 在加密后不提供额外的安全性，但会消耗更多熵
3. **性能**: 生成随机填充的开销可能较大；可考虑使用零填充
4. **内存**: 大的填充块会消耗带宽；请谨慎设定最大尺寸

---

## 实现指南

### 先决条件

**密码学库:**

- **X25519**: libsodium、NaCl 或 Bouncy Castle
- **ChaCha20-Poly1305**: libsodium、OpenSSL 1.1.0+ 或 Bouncy Castle
- **SHA-256**: OpenSSL、Bouncy Castle 或编程语言内置支持
- **Elligator2**: 库支持有限；可能需要自定义实现

**Elligator2（密码学隐蔽编码算法）实现：**

Elligator2（将椭圆曲线点映射为均匀随机位串的编码方法）尚未被广泛实现。可选方案：

1. **OBFS4**：Tor 的 obfs4 可插拔传输包含对 Elligator2（用于隐藏椭圆曲线点的映射算法）的实现
2. **自定义实现**：基于 [Elligator2 论文](https://elligator.cr.yp.to/elligator-20130828.pdf)
3. **kleshni/Elligator**：GitHub 上的参考实现

**Java I2P 说明：** Java I2P 使用 net.i2p.crypto.eddsa 库，并包含自定义的 Elligator2（椭圆曲线点映射技术）扩展。

### 推荐的实现顺序

**阶段 1：核心密码学** 1. X25519 DH 密钥生成与交换 2. ChaCha20-Poly1305 AEAD 加密/解密 3. SHA-256 哈希与 MixHash 4. HKDF 密钥派生 5. Elligator2 编码/解码（可先使用测试向量）

**第 2 阶段：消息格式** 1. NS 消息 (未绑定) - 最简单的格式 2. NS 消息 (已绑定) - 添加静态密钥 3. NSR 消息 4. ES 消息 5. 块解析与生成

**第 3 阶段：会话管理** 1. 会话创建与存储 2. 标签集管理 (发送方和接收方) 3. 会话标签棘轮 4. 对称密钥棘轮 5. 标签查找与窗口管理

**第 4 阶段：DH 棘轮** 1. NextKey 块处理 2. DH 棘轮 KDF（密钥派生函数） 3. 棘轮之后的标签集创建 4. 多标签集管理

**第 5 阶段：协议逻辑** 1. NS/NSR/ES 状态机 2. 重放防护 (DateTime, 布隆过滤器) 3. 重传逻辑 (多个 NS/NSR) 4. ACK 处理

**第6阶段：集成** 1. I2NP Garlic Clove（蒜瓣）处理 2. LeaseSet 打包 3. 流式传输协议集成 4. 数据报协议集成

### 发送端实现

**出站会话生命周期：**

```python
class OutboundSession:
    def __init__(self, destination, bound=True):
        self.destination = destination
        self.bound = bound
        self.state = SessionState.NEW
        
        # Keys for NS message
        self.ephemeral_keypair = generate_elg2_keypair()
        if bound:
            self.static_key = context.static_keypair
        
        # Will be populated after NSR
        self.outbound_tagset = None
        self.outbound_keyratchet = None
        self.inbound_tagset = None
        self.inbound_keyratchet = None
        
        # Timing
        self.created_time = now()
        self.last_activity = now()
        
        # Retransmission
        self.ns_attempts = []
        self.ns_timer = None
    
    def send_initial_message(self, payload):
        """Send NS message"""
        # Build NS message
        ns_message = self.build_ns_message(payload)
        
        # Send
        send_to_network(self.destination, ns_message)
        
        # Track for retransmission
        self.ns_attempts.append({
            'message': ns_message,
            'time': now(),
            'ephemeral_key': self.ephemeral_keypair,
            'kdf_state': self.save_kdf_state()
        })
        
        # Start timer
        self.ns_timer = set_timer(1.0, self.on_ns_timeout)
        self.state = SessionState.PENDING_REPLY
    
    def build_ns_message(self, payload):
        """Construct NS message"""
        # KDF initialization
        chainKey, h = self.initialize_kdf()
        
        # Ephemeral key section
        elg2_ephemeral = ENCODE_ELG2(self.ephemeral_keypair.public_key)
        h = SHA256(h || self.destination.static_key)
        h = SHA256(h || self.ephemeral_keypair.public_key)
        
        # es DH
        es_shared = DH(self.ephemeral_keypair.private_key, 
                       self.destination.static_key)
        keydata = HKDF(chainKey, es_shared, "", 64)
        chainKey = keydata[0:31]
        k_static = keydata[32:63]
        
        # Encrypt static key section
        if self.bound:
            static_section = self.static_key.public_key
        else:
            static_section = bytes(32)
        
        static_ciphertext = ENCRYPT(k_static, 0, static_section, h)
        h = SHA256(h || static_ciphertext)
        
        # ss DH (if bound)
        if self.bound:
            ss_shared = DH(self.static_key.private_key, 
                          self.destination.static_key)
            keydata = HKDF(chainKey, ss_shared, "", 64)
            chainKey = keydata[0:31]
            k_payload = keydata[32:63]
            nonce = 0
        else:
            k_payload = k_static
            nonce = 1
        
        # Build payload blocks
        payload_data = self.build_ns_payload(payload)
        
        # Encrypt payload
        payload_ciphertext = ENCRYPT(k_payload, nonce, payload_data, h)
        h = SHA256(h || payload_ciphertext)
        
        # Save KDF state for NSR processing
        self.ns_chainkey = chainKey
        self.ns_hash = h
        
        # Assemble message
        return elg2_ephemeral + static_ciphertext + payload_ciphertext
    
    def build_ns_payload(self, application_data):
        """Build NS payload blocks"""
        blocks = []
        
        # DateTime block (required, first)
        blocks.append(build_datetime_block())
        
        # Garlic Clove(s) with application data
        blocks.append(build_garlic_clove(application_data))
        
        # Optionally bundle LeaseSet
        if should_send_leaseset():
            blocks.append(build_garlic_clove(build_leaseset_store()))
        
        # Padding
        blocks.append(build_padding_block(random.randint(0, 15)))
        
        return encode_blocks(blocks)
    
    def on_nsr_received(self, nsr_message):
        """Process NSR and establish ES session"""
        # Cancel retransmission timer
        cancel_timer(self.ns_timer)
        
        # Parse NSR
        tag = nsr_message[0:8]
        elg2_bob_ephemeral = nsr_message[8:40]
        key_section_mac = nsr_message[40:56]
        payload_ciphertext = nsr_message[56:]
        
        # Find corresponding NS attempt
        ns_state = self.find_ns_by_tag(tag)
        if not ns_state:
            raise ValueError("NSR tag doesn't match any NS")
        
        # Restore KDF state
        chainKey = ns_state['chainkey']
        h = ns_state['hash']
        
        # Decode Bob's ephemeral key
        bob_ephemeral = DECODE_ELG2(elg2_bob_ephemeral)
        
        # Mix tag and Bob's ephemeral into hash
        h = SHA256(h || tag)
        h = SHA256(h || bob_ephemeral)
        
        # ee DH
        ee_shared = DH(self.ephemeral_keypair.private_key, bob_ephemeral)
        keydata = HKDF(chainKey, ee_shared, "", 32)
        chainKey = keydata[0:31]
        
        # se DH
        se_shared = DH(self.static_key.private_key, bob_ephemeral)
        keydata = HKDF(chainKey, se_shared, "", 64)
        chainKey = keydata[0:31]
        k_key_section = keydata[32:63]
        
        # Verify key section MAC
        try:
            DECRYPT(k_key_section, 0, key_section_mac, h)
        except AuthenticationError:
            raise ValueError("NSR key section MAC verification failed")
        
        h = SHA256(h || key_section_mac)
        
        # Split for bidirectional ES
        keydata = HKDF(chainKey, ZEROLEN, "", 64)
        k_ab = keydata[0:31]  # Alice → Bob
        k_ba = keydata[32:63]  # Bob → Alice
        
        # Initialize ES tagsets
        self.outbound_tagset = DH_INITIALIZE(chainKey, k_ab)
        self.inbound_tagset = DH_INITIALIZE(chainKey, k_ba)
        
        # Decrypt NSR payload
        k_nsr = HKDF(k_ba, ZEROLEN, "AttachPayloadKDF", 32)
        try:
            payload = DECRYPT(k_nsr, 0, payload_ciphertext, h)
        except AuthenticationError:
            raise ValueError("NSR payload MAC verification failed")
        
        # Process NSR payload blocks
        self.process_payload_blocks(payload)
        
        # Session established
        self.state = SessionState.ESTABLISHED
        self.last_activity = now()
        
        # Send ES message (implicit ACK)
        self.send_es_ack()
    
    def send_es_message(self, payload):
        """Send ES message"""
        if self.state != SessionState.ESTABLISHED:
            raise ValueError("Session not established")
        
        # Get next tag and key
        tag, index = self.outbound_tagset.get_next_tag()
        key = self.outbound_keyratchet.get_key(index)
        
        # Construct nonce
        nonce = construct_nonce(index)
        
        # Build payload blocks
        payload_data = self.build_es_payload(payload)
        
        # AEAD encryption
        ciphertext = ENCRYPT(key, nonce, payload_data, tag)
        
        # Assemble message
        es_message = tag + ciphertext
        
        # Send
        send_to_network(self.destination, es_message)
        
        # Update activity
        self.last_activity = now()
        
        # Check if ratchet needed
        if self.outbound_tagset.should_ratchet():
            self.initiate_ratchet()
```
### 接收端实现

**入站会话生命周期：**

```python
class InboundSession:
    def __init__(self):
        self.state = None
        self.bound = False
        self.destination = None
        
        # Keys
        self.remote_ephemeral_key = None
        self.remote_static_key = None
        self.ephemeral_keypair = None
        
        # Tagsets
        self.inbound_tagset = None
        self.outbound_tagset = None
        
        # Timing
        self.created_time = None
        self.last_activity = None
        
        # Paired session
        self.paired_outbound = None
    
    @staticmethod
    def try_decrypt_ns(message):
        """Attempt to decrypt as NS message"""
        # Parse NS structure
        elg2_ephemeral = message[0:32]
        static_ciphertext = message[32:80]  # 32 + 16
        payload_ciphertext = message[80:]
        
        # Decode ephemeral key
        try:
            alice_ephemeral = DECODE_ELG2(elg2_ephemeral)
        except:
            return None  # Not a valid Elligator2 encoding
        
        # Check replay
        if is_replay(alice_ephemeral):
            return None
        
        # KDF initialization
        chainKey, h = initialize_kdf()
        
        # Mix keys
        h = SHA256(h || context.static_keypair.public_key)
        h = SHA256(h || alice_ephemeral)
        
        # es DH
        es_shared = DH(context.static_keypair.private_key, alice_ephemeral)
        keydata = HKDF(chainKey, es_shared, "", 64)
        chainKey = keydata[0:31]
        k_static = keydata[32:63]
        
        # Decrypt static key section
        try:
            static_data = DECRYPT(k_static, 0, static_ciphertext, h)
        except AuthenticationError:
            return None  # Not a valid NS message
        
        h = SHA256(h || static_ciphertext)
        
        # Check if bound or unbound
        if static_data == bytes(32):
            # Unbound
            alice_static_key = None
            k_payload = k_static
            nonce = 1
        else:
            # Bound - perform ss DH
            alice_static_key = static_data
            ss_shared = DH(context.static_keypair.private_key, alice_static_key)
            keydata = HKDF(chainKey, ss_shared, "", 64)
            chainKey = keydata[0:31]
            k_payload = keydata[32:63]
            nonce = 0
        
        # Decrypt payload
        try:
            payload = DECRYPT(k_payload, nonce, payload_ciphertext, h)
        except AuthenticationError:
            return None
        
        h = SHA256(h || payload_ciphertext)
        
        # Create session
        session = InboundSession()
        session.state = SessionState.ESTABLISHED
        session.created_time = now()
        session.last_activity = now()
        session.remote_ephemeral_key = alice_ephemeral
        session.remote_static_key = alice_static_key
        session.bound = (alice_static_key is not None)
        session.ns_chainkey = chainKey
        session.ns_hash = h
        
        # Extract destination if bound
        if session.bound:
            session.destination = extract_destination_from_payload(payload)
        
        # Process payload
        session.process_payload_blocks(payload)
        
        return session
    
    def send_nsr_reply(self, reply_payload):
        """Send NSR message"""
        # Generate NSR tagset
        tagsetKey = HKDF(self.ns_chainkey, ZEROLEN, "SessionReplyTags", 32)
        nsr_tagset = DH_INITIALIZE(self.ns_chainkey, tagsetKey)
        
        # Get tag
        tag, _ = nsr_tagset.get_next_tag()
        
        # Mix tag into hash
        h = SHA256(self.ns_hash || tag)
        
        # Generate ephemeral key
        self.ephemeral_keypair = generate_elg2_keypair()
        bob_ephemeral = self.ephemeral_keypair.public_key
        elg2_bob_ephemeral = ENCODE_ELG2(bob_ephemeral)
        
        # Mix ephemeral key
        h = SHA256(h || bob_ephemeral)
        
        chainKey = self.ns_chainkey
        
        # ee DH
        ee_shared = DH(self.ephemeral_keypair.private_key, 
                      self.remote_ephemeral_key)
        keydata = HKDF(chainKey, ee_shared, "", 32)
        chainKey = keydata[0:31]
        
        # se DH
        se_shared = DH(context.static_keypair.private_key, 
                      self.remote_ephemeral_key)
        keydata = HKDF(chainKey, se_shared, "", 64)
        chainKey = keydata[0:31]
        k_key_section = keydata[32:63]
        
        # Encrypt key section (empty)
        key_section_ciphertext = ENCRYPT(k_key_section, 0, ZEROLEN, h)
        h = SHA256(h || key_section_ciphertext)
        
        # Split for bidirectional ES
        keydata = HKDF(chainKey, ZEROLEN, "", 64)
        k_ab = keydata[0:31]  # Alice → Bob
        k_ba = keydata[32:63]  # Bob → Alice
        
        # Initialize ES tagsets
        self.inbound_tagset = DH_INITIALIZE(chainKey, k_ab)
        self.outbound_tagset = DH_INITIALIZE(chainKey, k_ba)
        
        # Build reply payload
        payload_data = build_payload_blocks(reply_payload)
        
        # Encrypt payload
        k_nsr = HKDF(k_ba, ZEROLEN, "AttachPayloadKDF", 32)
        payload_ciphertext = ENCRYPT(k_nsr, 0, payload_data, h)
        
        # Assemble NSR
        nsr_message = tag + elg2_bob_ephemeral + key_section_ciphertext + payload_ciphertext
        
        # Send
        send_to_network(self.destination, nsr_message)
        
        # Wait for ES
        self.state = SessionState.AWAITING_ES
        self.last_activity = now()
    
    def on_es_received(self, es_message):
        """Process first ES message"""
        if self.state == SessionState.AWAITING_ES:
            # First ES received, confirms session
            self.state = SessionState.ESTABLISHED
        
        # Process ES message
        self.process_es_message(es_message)
    
    def process_es_message(self, es_message):
        """Decrypt and process ES message"""
        # Extract tag
        tag = es_message[0:8]
        ciphertext = es_message[8:]
        
        # Look up tag
        index = self.inbound_tagset.lookup_tag(tag)
        if index is None:
            raise ValueError("Tag not found")
        
        # Get key
        key = self.inbound_keyratchet.get_key(index)
        
        # Construct nonce
        nonce = construct_nonce(index)
        
        # Decrypt
        try:
            payload = DECRYPT(key, nonce, ciphertext, tag)
        except AuthenticationError:
            raise ValueError("ES MAC verification failed")
        
        # Process blocks
        self.process_payload_blocks(payload)
        
        # Update activity
        self.last_activity = now()
```
### 消息分类

**区分消息类型：**

```python
def classify_message(message):
    """Determine message type"""
    
    # Minimum lengths
    if len(message) < 24:
        return None  # Too short
    
    # Check for session tag (8 bytes)
    tag = message[0:8]
    
    # Try ES decryption first (most common)
    session = lookup_session_by_tag(tag)
    if session:
        return ('ES', session)
    
    # Try NSR decryption (tag + Elligator2 key)
    if len(message) >= 72:
        # Check if bytes 8-40 are valid Elligator2
        try:
            nsr_ephemeral = DECODE_ELG2(message[8:40])
            nsr_session = find_pending_nsr_by_tag(tag)
            if nsr_session:
                return ('NSR', nsr_session)
        except:
            pass
    
    # Try NS decryption (starts with Elligator2 key)
    if len(message) >= 96:
        try:
            ns_ephemeral = DECODE_ELG2(message[0:32])
            ns_session = InboundSession.try_decrypt_ns(message)
            if ns_session:
                return ('NS', ns_session)
        except:
            pass
    
    # Check ElGamal/AES (for dual-key compatibility)
    if len(message) >= 514:
        if (len(message) - 2) % 16 == 0:
            # Might be ElGamal NS
            return ('ELGAMAL_NS', None)
        elif len(message) % 16 == 0:
            # Might be ElGamal ES
            return ('ELGAMAL_ES', None)
    
    return None  # Unknown message type
```
### 会话管理最佳实践

**会话存储：**

```python
class SessionKeyManager:
    def __init__(self):
        # Outbound sessions (one per destination)
        self.outbound_sessions = {}  # destination -> OutboundSession
        
        # Inbound sessions (multiple per destination during transition)
        self.inbound_sessions = []  # [InboundSession]
        
        # Session tag lookup (fast path for ES messages)
        self.tag_to_session = {}  # tag -> InboundSession
        
        # Limits
        self.max_inbound_sessions = 1000
        self.max_tags_per_session = 160
    
    def get_outbound_session(self, destination):
        """Get or create outbound session"""
        if destination not in self.outbound_sessions:
            session = OutboundSession(destination)
            self.outbound_sessions[destination] = session
        return self.outbound_sessions[destination]
    
    def add_inbound_session(self, session):
        """Add new inbound session"""
        # Check limits
        if len(self.inbound_sessions) >= self.max_inbound_sessions:
            self.expire_oldest_session()
        
        self.inbound_sessions.append(session)
        
        # Add tags to lookup table
        self.register_session_tags(session)
    
    def register_session_tags(self, session):
        """Register session's tags in lookup table"""
        for tag in session.inbound_tagset.get_all_tags():
            self.tag_to_session[tag] = session
    
    def lookup_tag(self, tag):
        """Fast tag lookup"""
        return self.tag_to_session.get(tag)
    
    def expire_sessions(self):
        """Periodic session expiration"""
        now_time = now()
        
        # Expire outbound sessions
        for dest, session in list(self.outbound_sessions.items()):
            if session.idle_time(now_time) > 8 * 60:
                del self.outbound_sessions[dest]
        
        # Expire inbound sessions
        expired = []
        for session in self.inbound_sessions:
            if session.idle_time(now_time) > 10 * 60:
                expired.append(session)
        
        for session in expired:
            self.remove_inbound_session(session)
    
    def remove_inbound_session(self, session):
        """Remove inbound session and clean up tags"""
        self.inbound_sessions.remove(session)
        
        # Remove tags from lookup
        for tag in session.inbound_tagset.get_all_tags():
            if tag in self.tag_to_session:
                del self.tag_to_session[tag]
```
**内存管理：**

```python
class TagMemoryManager:
    def __init__(self, max_memory_kb=10240):  # 10 MB default
        self.max_memory = max_memory_kb * 1024
        self.current_memory = 0
        self.max_tags_per_session = 160
        self.min_tags_per_session = 32
    
    def calculate_tag_memory(self, session):
        """Calculate memory used by session tags"""
        tag_count = len(session.inbound_tagset.tags)
        # Each tag: 8 bytes (tag) + 2 bytes (index) + 32 bytes (key, optional)
        # + overhead
        bytes_per_tag = 16 if session.defer_keys else 48
        return tag_count * bytes_per_tag
    
    def check_pressure(self):
        """Check if under memory pressure"""
        return self.current_memory > (self.max_memory * 0.9)
    
    def handle_pressure(self):
        """Reduce memory usage when under pressure"""
        if not self.check_pressure():
            return
        
        # Strategy 1: Reduce look-ahead windows
        for session in all_sessions:
            if session.look_ahead > self.min_tags_per_session:
                session.reduce_look_ahead(self.min_tags_per_session)
        
        # Strategy 2: Trim old tags aggressively
        for session in all_sessions:
            session.inbound_tagset.trim_behind(aggressive=True)
        
        # Strategy 3: Refuse new ratchets
        for session in all_sessions:
            if session.outbound_tagset.should_ratchet():
                session.defer_ratchet = True
        
        # Strategy 4: Expire idle sessions early
        expire_idle_sessions(threshold=5*60)  # 5 min instead of 10
```
### 测试策略

**单元测试：**

```python
def test_x25519_dh():
    """Test X25519 key exchange"""
    alice_sk = GENERATE_PRIVATE()
    alice_pk = DERIVE_PUBLIC(alice_sk)
    
    bob_sk = GENERATE_PRIVATE()
    bob_pk = DERIVE_PUBLIC(bob_sk)
    
    # Both sides compute same shared secret
    alice_shared = DH(alice_sk, bob_pk)
    bob_shared = DH(bob_sk, alice_pk)
    
    assert alice_shared == bob_shared

def test_elligator2_encode_decode():
    """Test Elligator2 roundtrip"""
    sk = GENERATE_PRIVATE_ELG2()
    pk = DERIVE_PUBLIC(sk)
    
    encoded = ENCODE_ELG2(pk)
    decoded = DECODE_ELG2(encoded)
    
    assert decoded == pk

def test_chacha_poly_encrypt_decrypt():
    """Test ChaCha20-Poly1305 AEAD"""
    key = CSRNG(32)
    nonce = construct_nonce(42)
    plaintext = b"Hello, I2P!"
    ad = b"associated_data"
    
    ciphertext = ENCRYPT(key, nonce, plaintext, ad)
    decrypted = DECRYPT(key, nonce, ciphertext, ad)
    
    assert decrypted == plaintext

def test_session_tag_ratchet():
    """Test session tag generation"""
    sessTag_ck = CSRNG(32)
    tagset = SessionTagRatchet(sessTag_ck)
    
    # Generate 100 tags
    tags = [tagset.get_next_tag() for _ in range(100)]
    
    # All tags should be unique
    assert len(set(tags)) == 100
    
    # Each tag should be 8 bytes
    for tag in tags:
        assert len(tag) == 8
```
**集成测试：**

```python
def test_ns_nsr_handshake():
    """Test NS/NSR handshake"""
    # Alice creates outbound session
    alice_session = OutboundSession(bob_destination, bound=True)
    
    # Alice sends NS
    ns_message = alice_session.build_ns_message(b"Hello Bob")
    
    # Bob receives NS
    bob_session = InboundSession.try_decrypt_ns(ns_message)
    assert bob_session is not None
    assert bob_session.bound == True
    
    # Bob sends NSR
    nsr_message = bob_session.build_nsr_message(b"Hello Alice")
    
    # Alice receives NSR
    alice_session.on_nsr_received(nsr_message)
    assert alice_session.state == SessionState.ESTABLISHED
    
    # Both should have matching ES tagsets
    # (Cannot directly compare, but can test by sending ES messages)

def test_es_bidirectional():
    """Test ES messages in both directions"""
    # (After NS/NSR handshake)
    
    # Alice sends ES to Bob
    es_alice_to_bob = alice_session.send_es_message(b"Data from Alice")
    
    # Bob receives ES
    bob_session.process_es_message(es_alice_to_bob)
    
    # Bob sends ES to Alice
    es_bob_to_alice = bob_session.send_es_message(b"Data from Bob")
    
    # Alice receives ES
    alice_session.process_es_message(es_bob_to_alice)

def test_dh_ratchet():
    """Test DH ratchet"""
    # (After established session)
    
    # Alice initiates ratchet
    alice_session.initiate_ratchet()
    nextkey_alice = build_nextkey_block(
        flags=0x01,
        key_id=0,
        public_key=alice_new_key
    )
    
    # Send to Bob
    bob_session.process_nextkey_block(nextkey_alice)
    
    # Bob replies
    nextkey_bob = build_nextkey_block(
        flags=0x03,
        key_id=0,
        public_key=bob_new_key
    )
    
    # Send to Alice
    alice_session.process_nextkey_block(nextkey_bob)
    
    # Both should now be using new tagsets
    assert alice_session.outbound_tagset.id == 1
    assert bob_session.inbound_tagset.id == 1
```
**测试向量：**

实现规范中的测试向量：

1. **Noise IK Handshake**（Noise 协议 IK 握手模式）：使用标准的 Noise 测试向量
2. **HKDF**（基于 HMAC 的密钥派生函数）：使用 RFC 5869 测试向量
3. **ChaCha20-Poly1305**（由流加密 ChaCha20 与认证算法 Poly1305 组成的 AEAD 模式）：使用 RFC 7539 测试向量
4. **Elligator2**（一种将椭圆曲线点伪装为均匀随机比特串的编码方案）：使用 Elligator2 论文或 OBFS4 的测试向量

**互操作性测试：**

1. **Java I2P**: 针对 Java I2P 参考实现进行测试
2. **i2pd**: 针对 C++ 的 i2pd 实现进行测试
3. **Packet Captures**: 使用 Wireshark 解析器（若可用）验证消息格式
4. **Cross-Implementation**: 创建一个可在不同实现之间进行发送/接收的测试框架

### 性能注意事项

**密钥生成：**

Elligator2（将椭圆曲线公钥伪装成随机数据的方案）的密钥生成开销较大（50% 的拒绝率）：

```python
class KeyPool:
    """Pre-generate keys in background thread"""
    def __init__(self, pool_size=10):
        self.pool = Queue(maxsize=pool_size)
        self.generator_thread = Thread(target=self.generate_keys, daemon=True)
        self.generator_thread.start()
    
    def generate_keys(self):
        while True:
            if not self.pool.full():
                keypair = generate_elg2_keypair()
                # Also compute encoded form
                encoded = ENCODE_ELG2(keypair.public_key)
                self.pool.put((keypair, encoded))
            else:
                sleep(0.1)
    
    def get_keypair(self):
        try:
            return self.pool.get(timeout=1.0)
        except Empty:
            # Pool exhausted, generate inline
            return generate_elg2_keypair()
```
**标签查找:**

使用哈希表实现 O(1) 的标签查找：

```python
class FastTagLookup:
    def __init__(self):
        self.tag_to_session = {}  # Python dict is hash table
    
    def add_tag(self, tag, session, index):
        # 8-byte tag as bytes is hashable
        self.tag_to_session[tag] = (session, index)
    
    def lookup_tag(self, tag):
        return self.tag_to_session.get(tag)
```
**内存优化：**

延后生成对称密钥:

```python
class DeferredKeyRatchet:
    """Only generate keys when needed"""
    def __init__(self, symmKey_ck):
        self.chainKey = symmKey_ck
        self.index = -1
        self.cache = LRUCache(maxsize=32)  # Cache recent keys
    
    def get_key(self, index):
        # Check cache first
        if index in self.cache:
            return self.cache[index]
        
        # Generate keys up to index
        while self.index < index:
            self.index += 1
            keydata = HKDF(self.chainKey, ZEROLEN, "SymmetricRatchet", 64)
            self.chainKey = keydata[0:31]
            
            if self.index == index:
                key = keydata[32:63]
                self.cache[index] = key
                return key
```
**批处理:**

批量处理多条消息：

```python
def process_message_batch(messages):
    """Process multiple messages efficiently"""
    results = []
    
    # Group by type
    ns_messages = []
    nsr_messages = []
    es_messages = []
    
    for msg in messages:
        msg_type = classify_message(msg)
        if msg_type[0] == 'NS':
            ns_messages.append(msg)
        elif msg_type[0] == 'NSR':
            nsr_messages.append(msg)
        elif msg_type[0] == 'ES':
            es_messages.append(msg)
    
    # Process in batches
    # ES messages are most common, process first
    for msg in es_messages:
        results.append(process_es_message(msg))
    
    for msg in nsr_messages:
        results.append(process_nsr_message(msg))
    
    for msg in ns_messages:
        results.append(process_ns_message(msg))
    
    return results
```
---

## 安全注意事项

### 威胁模型

**对手能力：**

1. **被动观察者**：可以观察所有网络流量
2. **主动攻击者**：可以注入、修改、丢弃、重放消息
3. **被攻陷的节点**：可能攻陷 router 或目的地
4. **流量分析**：可以对流量模式进行统计分析

**安全目标：**

1. **机密性**: 消息内容对观察者不可见
2. **认证**: 发送方身份已验证(适用于绑定会话)
3. **前向保密性**: 即使密钥被泄露，过去的消息仍保持机密
4. **防重放**: 旧消息无法被重放
5. **流量混淆**: 握手与随机数据不可区分

### 密码学假设

**困难性假设：**

1. **X25519 CDH**: 在 Curve25519 上，计算性 Diffie-Hellman 问题是困难的
2. **ChaCha20 PRF**: ChaCha20 是一种伪随机函数
3. **Poly1305 MAC**: Poly1305 在选择消息攻击下不可伪造
4. **SHA-256 CR**: SHA-256 具有抗碰撞性
5. **HKDF Security**: HKDF 能够提取并扩展为均匀分布的密钥

**安全级别：**

- **X25519**: ~128 位安全强度 (曲线阶 2^252)
- **ChaCha20**: 256 位密钥, 256 位安全强度
- **Poly1305**: 128 位安全强度 (碰撞概率)
- **SHA-256**: 128 位抗碰撞性, 256 位原像抵抗性

### 密钥管理

**密钥生成：**

```python
# CRITICAL: Use cryptographically secure RNG
def CSRNG(length):
    # GOOD: os.urandom, secrets.token_bytes (Python)
    # GOOD: /dev/urandom (Linux)
    # GOOD: BCryptGenRandom (Windows)
    # BAD: random.random(), Math.random() (NOT cryptographically secure)
    return os.urandom(length)

# CRITICAL: Validate keys
def validate_x25519_key(pubkey):
    # Check for weak keys (all zeros, small order points)
    if pubkey == bytes(32):
        raise WeakKeyError("All-zero public key")
    
    # Perform DH to check for weak shared secrets
    test_shared = DH(test_private_key, pubkey)
    if test_shared == bytes(32):
        raise WeakKeyError("Results in zero shared secret")
```
**密钥存储：**

```python
# CRITICAL: Protect private keys
class SecureKeyStorage:
    def __init__(self):
        # Store in memory with protection
        self.keys = {}
        
        # Option 1: Memory locking (prevent swapping to disk)
        # mlock(self.keys)
        
        # Option 2: Encrypted storage
        # self.encryption_key = derive_from_password()
    
    def store_key(self, key_id, private_key):
        # Option: Encrypt before storage
        # encrypted = encrypt(private_key, self.encryption_key)
        # self.keys[key_id] = encrypted
        self.keys[key_id] = private_key
    
    def delete_key(self, key_id):
        # Securely wipe memory
        if key_id in self.keys:
            key = self.keys[key_id]
            # Overwrite with zeros before deletion
            for i in range(len(key)):
                key[i] = 0
            del self.keys[key_id]
```
**密钥轮换:**

```python
# CRITICAL: Rotate keys regularly
class KeyRotationPolicy:
    def __init__(self):
        self.max_messages_per_tagset = 4096  # Ratchet before 65535
        self.max_tagset_age = 10 * 60       # 10 minutes
        self.max_session_age = 60 * 60      # 1 hour
    
    def should_ratchet(self, tagset):
        return (tagset.messages_sent >= self.max_messages_per_tagset or
                tagset.age() >= self.max_tagset_age)
    
    def should_replace_session(self, session):
        return session.age() >= self.max_session_age
```
### 攻击缓解措施

### 重放攻击缓解措施

**日期时间验证：**

```python
MAX_CLOCK_SKEW_PAST = 5 * 60
MAX_CLOCK_SKEW_FUTURE = 2 * 60

def validate_datetime(timestamp):
    now = int(time.time())
    age = now - timestamp
    
    if age < -MAX_CLOCK_SKEW_FUTURE:
        raise ReplayError("Timestamp too far in future")
    
    if age > MAX_CLOCK_SKEW_PAST:
        raise ReplayError("Timestamp too old")
    
    return True
```
**用于 NS 消息的布隆过滤器：**

```python
class ReplayFilter:
    def __init__(self, capacity=100000, error_rate=0.001, duration=5*60):
        self.bloom = BloomFilter(capacity=capacity, error_rate=error_rate)
        self.duration = duration
        self.entries = []  # (timestamp, ephemeral_key)
    
    def check_replay(self, ephemeral_key, timestamp):
        # Validate timestamp
        if not validate_datetime(timestamp):
            return False
        
        # Check Bloom filter
        if ephemeral_key in self.bloom:
            # Potential replay (or false positive)
            # Check exact match in entries
            for ts, key in self.entries:
                if key == ephemeral_key:
                    return False  # Definite replay
        
        # Add to filter
        self.bloom.add(ephemeral_key)
        self.entries.append((timestamp, ephemeral_key))
        
        # Expire old entries
        self.expire_old_entries()
        
        return True
    
    def expire_old_entries(self):
        now = int(time.time())
        self.entries = [(ts, key) for ts, key in self.entries
                       if now - ts < self.duration]
```
**会话标签一次性使用：**

```python
def process_session_tag(tag):
    # Look up tag
    entry = tagset.lookup_tag(tag)
    if entry is None:
        raise ValueError("Invalid session tag")
    
    # CRITICAL: Remove tag immediately (one-time use)
    tagset.remove_tag(tag)
    
    # Use associated key
    return entry.key, entry.index
```
### 密钥妥协冒充（KCI）缓解措施

**问题**: NS 消息认证易受 KCI (密钥泄露冒充) 攻击 (认证级别 1)

**缓解措施**:

1. 尽快过渡到 NSR（认证级别 2）
2. 不要在涉及安全关键操作时信任 NS payload（NS 的载荷数据）
3. 在执行不可逆操作之前，等待 NSR 确认

```python
def process_ns_message(ns_message):
    # NS authenticated at Level 1 (KCI vulnerable)
    # Do NOT perform security-critical operations yet
    
    # Extract sender's static key
    sender_key = ns_message.static_key
    
    # Mark session as pending Level 2 authentication
    session.auth_level = 1
    session.sender_key = sender_key
    
    # Send NSR
    send_nsr_reply(session)

def process_first_es_message(es_message):
    # Now we have Level 2 authentication (KCI resistant)
    session.auth_level = 2
    
    # Safe to perform security-critical operations
    process_security_critical_operation(es_message)
```
### 拒绝服务（DoS）缓解措施

**NS 泛洪防护:**

```python
class NSFloodProtection:
    def __init__(self):
        self.ns_count = defaultdict(int)  # source -> count
        self.ns_timestamps = defaultdict(list)  # source -> [timestamps]
        
        self.max_ns_per_source = 5
        self.rate_window = 10  # seconds
        self.max_concurrent_ns = 100
    
    def check_ns_allowed(self, source):
        # Global limit
        total_pending = sum(self.ns_count.values())
        if total_pending >= self.max_concurrent_ns:
            return False
        
        # Per-source rate limit
        now = time.time()
        timestamps = self.ns_timestamps[source]
        
        # Remove old timestamps
        timestamps = [ts for ts in timestamps if now - ts < self.rate_window]
        self.ns_timestamps[source] = timestamps
        
        # Check rate
        if len(timestamps) >= self.max_ns_per_source:
            return False
        
        # Allow NS
        timestamps.append(now)
        self.ns_count[source] += 1
        return True
    
    def on_session_established(self, source):
        # Decrease pending count
        if self.ns_count[source] > 0:
            self.ns_count[source] -= 1
```
**标签存储限制：**

```python
class TagStorageLimit:
    def __init__(self, max_tags=1000000):
        self.max_tags = max_tags
        self.current_tags = 0
    
    def can_create_session(self, look_ahead):
        if self.current_tags + look_ahead > self.max_tags:
            return False
        return True
    
    def add_tags(self, count):
        self.current_tags += count
    
    def remove_tags(self, count):
        self.current_tags -= count
```
**自适应资源管理：**

```python
class AdaptiveResourceManager:
    def __init__(self):
        self.load_level = 0  # 0 = low, 1 = medium, 2 = high, 3 = critical
    
    def adjust_parameters(self):
        if self.load_level == 0:
            # Normal operation
            return {
                'max_look_ahead': 160,
                'max_sessions': 1000,
                'session_timeout': 10 * 60
            }
        
        elif self.load_level == 1:
            # Moderate load
            return {
                'max_look_ahead': 80,
                'max_sessions': 800,
                'session_timeout': 8 * 60
            }
        
        elif self.load_level == 2:
            # High load
            return {
                'max_look_ahead': 32,
                'max_sessions': 500,
                'session_timeout': 5 * 60
            }
        
        else:  # load_level == 3
            # Critical load
            return {
                'max_look_ahead': 16,
                'max_sessions': 200,
                'session_timeout': 3 * 60
            }
```
### 抗流量分析能力

**Elligator2 编码：**

确保握手消息与随机数据不可区分：

```python
# NS and NSR start with Elligator2-encoded ephemeral keys
# Observer cannot distinguish from random 32-byte string
```
**填充策略：**

```python
# Resist message size fingerprinting
def add_padding(payload, strategy='random'):
    if strategy == 'random':
        # Random padding 0-15 bytes
        size = random.randint(0, 15)
    
    elif strategy == 'round':
        # Round to next 64-byte boundary
        target = ((len(payload) + 63) // 64) * 64
        size = target - len(payload) - 3  # -3 for block header
    
    elif strategy == 'fixed':
        # Always 1KB messages
        size = 1024 - len(payload) - 3
    
    return build_padding_block(size)
```
**计时攻击:**

```python
# CRITICAL: Use constant-time operations
def constant_time_compare(a, b):
    """Constant-time byte string comparison"""
    if len(a) != len(b):
        return False
    
    result = 0
    for x, y in zip(a, b):
        result |= x ^ y
    
    return result == 0

# CRITICAL: Constant-time MAC verification
def verify_mac(computed_mac, received_mac):
    if not constant_time_compare(computed_mac, received_mac):
        # Always take same time regardless of where comparison fails
        raise AuthenticationError("MAC verification failed")
```
### 实现中的陷阱

**常见错误：**

1. **Nonce 重用（一次性随机数）**: 绝不要重用 (key, nonce) 对
   ```python
   # BAD: Reusing nonce with same key
   ciphertext1 = ENCRYPT(key, nonce, plaintext1, ad1)
   ciphertext2 = ENCRYPT(key, nonce, plaintext2, ad2)  # CATASTROPHIC

# 正确：针对每条消息使用唯一的 nonce（一次性随机数）    ciphertext1 = ENCRYPT(key, nonce1, plaintext1, ad1)    ciphertext2 = ENCRYPT(key, nonce2, plaintext2, ad2)

   ```

2. **Ephemeral Key Reuse**: Generate fresh ephemeral key for each NS/NSR
   ```python
# 错误：重复使用临时密钥    ephemeral_key = generate_elg2_keypair()    send_ns_message(ephemeral_key)    send_ns_message(ephemeral_key)  # 错误

# 良好：每条消息使用新密钥    send_ns_message(generate_elg2_keypair())    send_ns_message(generate_elg2_keypair())

   ```

3. **Weak RNG**: Use cryptographically secure random number generator
   ```python
# 不佳：非加密安全的随机数生成器    import random    key = bytes([random.randint(0, 255) for _ in range(32)])  # 不安全

# 良好：密码学安全的随机数生成器（RNG）    import os    key = os.urandom(32)

   ```

4. **Timing Attacks**: Use constant-time comparisons
   ```python
# 不当：提前退出式比较    if computed_mac == received_mac:  # 时序泄漏

       pass
   
# 良好：恒定时间比较    if constant_time_compare(computed_mac, received_mac):

       pass
   ```

5. **Incomplete MAC Verification**: Always verify before using data
   ```python
# 错误: 在验证之前解密    plaintext = chacha20_decrypt(key, nonce, ciphertext)    mac_ok = verify_mac(mac, plaintext)  # 为时已晚    if not mac_ok:

       return error
   
# 正确：AEAD（带关联数据的认证加密）在解密前进行验证    try:

       plaintext = DECRYPT(key, nonce, ciphertext, ad)  # Verifies MAC first
except AuthenticationError:

       return error
   ```

6. **Key Deletion**: Securely wipe keys from memory
   ```python
# 错误：简单删除    del private_key  # 仍在内存中

# 推荐：删除前先覆盖    for i in range(len(private_key)):

       private_key[i] = 0
del private_key

   ```

### Security Audits

**Recommended Audits:**

1. **Cryptographic Review**: Expert review of KDF chains and DH operations
2. **Implementation Audit**: Code review for timing attacks, key management, RNG usage
3. **Protocol Analysis**: Formal verification of handshake security properties
4. **Side-Channel Analysis**: Timing, power, and cache attacks
5. **Fuzzing**: Random input testing for parser robustness

**Test Cases:**

```python
# 安全关键测试用例

def test_nonce_uniqueness():

    """Ensure nonces are never reused"""
    nonces = set()
    for i in range(10000):
        nonce = construct_nonce(i)
        assert nonce not in nonces
        nonces.add(nonce)

def test_key_isolation():

    """Ensure sessions don't share keys"""
    session1 = create_session(destination1)
    session2 = create_session(destination2)
    
    assert session1.key != session2.key

def test_replay_prevention():

    """Ensure replay attacks are detected"""
    ns_message = create_ns_message()
    
    # First delivery succeeds
    assert process_ns_message(ns_message) == True
    
    # Replay fails
    assert process_ns_message(ns_message) == False

def test_mac_verification():

    """Ensure MAC verification is enforced"""
    key = CSRNG(32)
    nonce = construct_nonce(0)
    plaintext = b"test"
    ad = b"test_ad"
    
    ciphertext = ENCRYPT(key, nonce, plaintext, ad)
    
    # Correct MAC verifies
    assert DECRYPT(key, nonce, ciphertext, ad) == plaintext
    
    # Corrupted MAC fails
    corrupted = ciphertext[:-1] + bytes([ciphertext[-1] ^ 0xFF])
    with pytest.raises(AuthenticationError):
        DECRYPT(key, nonce, corrupted, ad)
```

---

## Configuration and Deployment

### I2CP Configuration

**Enable ECIES Encryption:**

```properties
# 仅限 ECIES（椭圆曲线集成加密方案，推荐用于新部署）

i2cp.leaseSetEncType=4

# 双密钥（ECIES + ElGamal，出于兼容性考虑）

i2cp.leaseSetEncType=4,0

# 仅限 ElGamal（遗留，不推荐）

i2cp.leaseSetEncType=0

```

**LeaseSet Type:**

```properties
# 标准 LS2（第二代 leaseSet，最常见）

i2cp.leaseSetType=3

# 加密的 LS2（blinded destinations（盲化目的地））

i2cp.leaseSetType=5

# Meta LS2（多个目的地）

i2cp.leaseSetType=7

```

**Additional Options:**

```properties
# 用于 ECIES（椭圆曲线集成加密方案）的静态密钥（可选，未指定时自动生成）

# 32 字节的 X25519 公钥，Base64 编码

i2cp.leaseSetPrivateKey=<base64-encoded-key>

# 签名类型 (用于 LeaseSet)

i2cp.leaseSetSigningPrivateKey=<base64-encoded-key> i2cp.leaseSetSigningType=7  # Ed25519

```

### Java I2P Configuration

**router.config:**

```properties
# router 到 router 的 ECIES（椭圆曲线集成加密方案）

i2p.router.useECIES=true

```

**Build Properties:**

```java
// 适用于 I2CP 客户端 (Java) Properties props = new Properties(); props.setProperty("i2cp.leaseSetEncType", "4"); props.setProperty("i2cp.leaseSetType", "3");

I2PSession session = i2pClient.createSession(props);

```

### i2pd Configuration

**i2pd.conf:**

```ini
[限制]

# ECIES（椭圆曲线集成加密方案）会话内存限制

ecies.memory = 128M

[ecies]

# 启用 ECIES（椭圆曲线集成加密方案）

enabled = true

# 仅限 ECIES 或双密钥

compatibility = true  # true = 双密钥，false = 仅 ECIES

```

**Tunnels Configuration:**

```ini
[my-service] type = http host = 127.0.0.1 port = 8080 keys = my-service-keys.dat

# 仅 ECIES（椭圆曲线集成加密方案）

ecies = true

```

### Compatibility Matrix

**Router Version Support:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">ECIES Support</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">LS2 Support</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Dual-Key</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">&lt; 0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">❌ No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">❌ No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">N/A</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy only</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.38-0.9.45</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">❌ No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">N/A</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LS2 only</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.46-0.9.50</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Initial ECIES</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.5.0+</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.0.0+</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
  </tbody>
</table>

**Destination Compatibility:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Destination Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Can Connect To</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-only</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-only, Dual-key</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Requires 0.9.46+ routers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Dual-key</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Maximum compatibility</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal-only</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal-only, Dual-key</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy</td>
    </tr>
  </tbody>
</table>

**FloodFill Requirements:**

- **ECIES-only destinations**: Require majority of floodfills on 0.9.46+ for encrypted lookups
- **Dual-key destinations**: Work with any floodfill version
- **Current status**: Near 100% floodfill adoption as of 2025

### Migration Guide

**Migrating from ElGamal to ECIES:**

**Step 1: Enable Dual-Key Mode**

```properties
# 在保留 ElGamal 的同时添加 ECIES

i2cp.leaseSetEncType=4,0

```

**Step 2: Monitor Connections**

```bash
# 检查连接类型

i2prouter.exe status

# 或

http://127.0.0.1:7657/peers

```

**Step 3: Switch to ECIES-Only (after testing)**

```properties
# 移除 ElGamal（ElGamal 加密算法）

i2cp.leaseSetEncType=4

```

**Step 4: Restart Application**

```bash
# 重启 I2P router 或应用程序

systemctl restart i2p

# 或

i2prouter.exe restart

```

**Rollback Plan:**

```properties
# 如遇问题，回退为仅使用 ElGamal

i2cp.leaseSetEncType=0

```

### Performance Tuning

**Session Limits:**

```properties
# 最大入站会话数

i2p.router.maxInboundSessions=1000

# 最大出站会话数

i2p.router.maxOutboundSessions=1000

# 会话超时（秒）

i2p.router.sessionTimeout=600

```

**Memory Limits:**

```properties
# 标签存储上限（KB）

i2p.ecies.maxTagMemory=10240  # 10 MB

# 前瞻窗口

i2p.ecies.tagLookAhead=160 i2p.ecies.tagLookAheadMin=32

```

**Ratchet Policy:**

```properties
# 棘轮前的消息

i2p.ecies.ratchetThreshold=4096

# ratchet（棘轮）之前的时间（秒）

i2p.ecies.ratchetTimeout=600  # 10 分钟

```

### Monitoring and Debugging

**Logging:**

```properties
# 启用 ECIES（椭圆曲线集成加密方案）调试日志

logger.i2p.router.transport.ecies=DEBUG

```

**Metrics:**

Monitor these metrics:

1. **NS Success Rate**: Percentage of NS messages receiving NSR
2. **Session Establishment Time**: Time from NS to first ES
3. **Tag Storage Usage**: Current memory usage for tags
4. **Ratchet Frequency**: How often sessions ratchet
5. **Session Lifetime**: Average session duration

**Common Issues:**

1. **NS Timeout**: No NSR received
   - Check destination is online
   - Check floodfill availability
   - Verify LeaseSet published correctly

2. **High Memory Usage**: Too many tags stored
   - Reduce look-ahead window
   - Decrease session timeout
   - Implement aggressive expiration

3. **Frequent Ratchets**: Sessions ratcheting too often
   - Increase ratchet threshold
   - Check for retransmissions

4. **Session Failures**: ES messages failing to decrypt
   - Verify tag synchronization
   - Check for replay attacks
   - Validate nonce construction

---

## References

### Specifications

1. **ECIES Proposal**: [Proposal 144](/proposals/144-ecies-x25519-aead-ratchet/)
2. **I2NP**: [I2NP Specification](/docs/specs/i2np/)
3. **Common Structures**: [Common Structures Specification](/docs/specs/common-structures/)
4. **NTCP2**: [NTCP2 Specification](/docs/specs/ntcp2/)
5. **SSU2**: [SSU2 Specification](/docs/specs/ssu2/)
6. **I2CP**: [I2CP Specification](/docs/specs/i2cp/)
7. **ElGamal/AES+SessionTags**: [ElGamal/AES Specification](/docs/legacy/elgamal-aes/)

### Cryptographic Standards

1. **Noise Protocol Framework**: [Noise Specification](https://noiseprotocol.org/noise.html) (Revision 34, 2018-07-11)
2. **Signal Double Ratchet**: [Signal Specification](https://signal.org/docs/specifications/doubleratchet/)
3. **RFC 7748**: [Elliptic Curves for Security (X25519)](https://tools.ietf.org/html/rfc7748)
4. **RFC 7539**: [ChaCha20 and Poly1305 for IETF Protocols](https://tools.ietf.org/html/rfc7539)
5. **RFC 5869**: [HKDF (HMAC-based Key Derivation Function)](https://tools.ietf.org/html/rfc5869)
6. **RFC 2104**: [HMAC: Keyed-Hashing for Message Authentication](https://tools.ietf.org/html/rfc2104)
7. **Elligator2**: [Elligator Paper](https://elligator.cr.yp.to/elligator-20130828.pdf)

### Implementation Resources

1. **Java I2P**: [i2p.i2p Repository](https://github.com/i2p/i2p.i2p)
2. **i2pd (C++)**: [i2pd Repository](https://github.com/PurpleI2P/i2pd)
3. **OBFS4 (Elligator2)**: [obfs4proxy Repository](https://gitlab.com/yawning/obfs4)

### Additional Information

1. **I2P Website**: [/](/)
2. **I2P Forum**: [https://i2pforum.net](https://i2pforum.net)
3. **I2P Wiki**: [https://wiki.i2p-projekt.de](https://wiki.i2p-projekt.de)

---

## Appendix A: KDF Summary

**All KDF Operations in ECIES:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Input</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Info String</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Output</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NS Initial ChainKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">protocol_name</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">(none - SHA256)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">h, chainKey</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NS Static Key Section</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, es_shared</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">""</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, k</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NS Payload Section (bound)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, ss_shared</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">""</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, k</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR Tagset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"SessionReplyTags"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">tagsetKey</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR ee DH</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, ee_shared</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">""</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR se DH</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, se_shared</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">""</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, k</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR Split</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">""</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">k_ab, k_ba</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR Payload</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">k_ba</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"AttachPayloadKDF"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">k_nsr</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DH Initialize</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">rootKey, k</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"KDFDHRatchetStep"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">nextRootKey, chainKey</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Tag and Key Chain Keys</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"TagAndKeyGenKeys"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">sessTag_ck, symmKey_ck</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Session Tag Init</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">sessTag_ck</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"STInitialization"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, CONSTANT</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Session Tag Gen</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, CONSTANT</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"SessionTagKeyGen"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, tag</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Symmetric Key Gen</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"SymmetricRatchet"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DH Ratchet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">sharedSecret</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"XDHRatchetTagSet"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">tagsetKey</td>
    </tr>
  </tbody>
</table>

---

## Appendix B: Message Size Calculator

**Calculate message sizes for capacity planning:**

```python
def calculate_ns_size(payload_size, bound=True):

    """Calculate New Session message size"""
    ephemeral_key = 32
    static_section = 32 + 16  # encrypted + MAC
    payload_encrypted = payload_size + 16  # + MAC
    
    return ephemeral_key + static_section + payload_encrypted

def calculate_nsr_size(payload_size):

    """Calculate New Session Reply message size"""
    tag = 8
    ephemeral_key = 32
    key_section_mac = 16
    payload_encrypted = payload_size + 16  # + MAC
    
    return tag + ephemeral_key + key_section_mac + payload_encrypted

def calculate_es_size(payload_size):

    """Calculate Existing Session message size"""
    tag = 8
    payload_encrypted = payload_size + 16  # + MAC
    
    return tag + payload_encrypted

# 示例

print("NS (绑定，1KB 负载):", calculate_ns_size(1024, bound=True), "字节")

# 输出：1120 字节

print("NSR (1KB 负载):", calculate_nsr_size(1024), "字节")

# 输出：1096 字节

print("ES (1KB payload):", calculate_es_size(1024), "bytes")

# 输出: 1048 字节

```

---

## Appendix C: Glossary

**AEAD**: Authenticated Encryption with Associated Data - encryption mode that provides both confidentiality and authenticity

**Authentication Level**: Noise protocol security property indicating strength of sender identity verification

**Binding**: Association of a session with a specific far-end destination

**ChaCha20**: Stream cipher designed by Daniel J. Bernstein

**ChainKey**: Cryptographic key used in HKDF chains to derive subsequent keys

**Confidentiality Level**: Noise protocol security property indicating strength of forward secrecy

**DH**: Diffie-Hellman key agreement protocol

**Elligator2**: Encoding technique to make elliptic curve points indistinguishable from random

**Ephemeral Key**: Short-lived key used only for a single handshake

**ES**: Existing Session message (used after handshake completion)

**Forward Secrecy**: Property ensuring past communications remain secure if keys are compromised

**Garlic Clove**: I2NP message container for end-to-end delivery

**HKDF**: HMAC-based Key Derivation Function

**IK Pattern**: Noise handshake pattern where initiator sends static key immediately

**KCI**: Key Compromise Impersonation attack

**KDF**: Key Derivation Function - cryptographic function for generating keys from other keys

**LeaseSet**: I2P structure containing a destination's public keys and tunnel information

**LS2**: LeaseSet version 2 with encryption type support

**MAC**: Message Authentication Code - cryptographic checksum proving authenticity

**MixHash**: Noise protocol function for maintaining running hash transcript

**NS**: New Session message (initiates new session)

**NSR**: New Session Reply message (response to NS)

**Nonce**: Number used once - ensures unique encryption even with same key

**Pairing**: Linking an inbound session with an outbound session for bidirectional communication

**Poly1305**: Message authentication code designed by Daniel J. Bernstein

**Ratchet**: Cryptographic mechanism for deriving sequential keys

**Session Tag**: 8-byte one-time identifier for existing session messages

**Static Key**: Long-term key associated with a destination's identity

**Tag Set**: Collection of session tags derived from a common root

**X25519**: Elliptic curve Diffie-Hellman key agreement using Curve25519

---