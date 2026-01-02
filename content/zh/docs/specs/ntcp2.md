---
title: "NTCP2 传输"
description: "用于 router 间链路的基于 Noise 的 TCP 传输"
slug: "ntcp2"
lastUpdated: "2025-10"
accurateFor: "0.9.66"
type: docs
---

## 概览

NTCP2 用基于 Noise 的握手取代了旧版 NTCP 传输，能够抵御流量指纹识别、加密长度字段，并支持现代加密套件。Routers 可以将 NTCP2 与 SSU2 一同运行，作为 I2P 网络中的两种强制性传输协议。NTCP（版本 1）在 0.9.40（2019 年 5 月）被弃用，并在 0.9.50（2021 年 5 月）被完全移除。

## Noise Protocol Framework（Noise 协议框架）

NTCP2 使用 Noise 协议框架 [修订版 33，2017-10-04](https://noiseprotocol.org/noise.html)，并带有 I2P 特定的扩展：

- **模式**: `Noise_XK_25519_ChaChaPoly_SHA256`
- **扩展标识符**: `Noise_XKaesobfse+hs2+hs3_25519_ChaChaPoly_SHA256`（用于 KDF 初始化，KDF 为“密钥派生函数”）
- **DH（Diffie-Hellman）函数**: X25519（RFC 7748） - 32 字节密钥，小端序编码
- **加密算法**: AEAD_CHACHA20_POLY1305（RFC 7539/RFC 8439）
  - 12 字节 nonce（随机数）：前 4 字节为 0，后 8 字节为计数器（小端序）
  - 最大 nonce 值：2^64 - 2（在达到 2^64 - 1 之前必须终止连接）
- **哈希函数**: SHA-256（32 字节输出）
- **MAC（消息认证码）**: Poly1305（16 字节认证标签）

### I2P 特定扩展

1. **AES 混淆**: 使用 Bob 的 router 哈希和公开的 IV，以 AES-256-CBC 加密临时密钥
2. **随机填充**: 消息 1-2 中为明文填充（已认证），消息 3 及之后为 AEAD 填充（已加密）
3. **SipHash-2-4 长度混淆**: 将两字节帧长度与 SipHash-2-4 的输出异或
4. **帧结构**: 数据阶段使用带长度前缀的帧（兼容 TCP 流式传输）
5. **基于块的有效载荷**: 采用带类型块的结构化数据格式

## 握手流程

```
Alice (Initiator)             Bob (Responder)
SessionRequest  ──────────────────────►
                ◄────────────────────── SessionCreated
SessionConfirmed ──────────────────────►
```
### 三消息握手

1. **SessionRequest** - Alice 的混淆临时密钥、选项、填充提示
2. **SessionCreated** - Bob 的混淆临时密钥、加密的选项、填充
3. **SessionConfirmed** - Alice 的加密的静态密钥和 RouterInfo（I2P router 的信息）（两个 AEAD（带关联数据的认证加密）帧）

### Noise（协议框架）消息模式

```
XK(s, rs):           Authentication   Confidentiality
  <- s               (Bob's static key known in advance)
  -> e, es                  0                2
  <- e, ee                  2                1
  -> s, se                  2                5
  <-                        2                5
```
**认证级别：** - 0: 无认证（任何一方都可能是发送者） - 2: 可抵抗密钥泄露冒充（KCI）攻击的发送方认证

**保密级别：** - 1: 临时（ephemeral）接收方（前向保密（forward secrecy），无接收方认证） - 2: 已知接收方，仅在发送方被攻破时提供前向保密 - 5: 强前向保密（临时-临时 + 临时-静态 DH（Diffie–Hellman））

## 消息规范

### 密钥记法

- `RH_A` = Alice 的 Router 哈希（32 字节，SHA-256）
- `RH_B` = Bob 的 Router 哈希（32 字节，SHA-256）
- `||` = 连接运算符
- `byte(n)` = 值为 n 的单个字节
- 除非另有说明，所有多字节整数均为**大端序**
- X25519 密钥为**小端序**（32 字节）

### 认证加密（ChaCha20-Poly1305）

**加密函数：**

```
AEAD_ChaCha20_Poly1305(key, nonce, associatedData, plaintext)
  → (ciphertext || MAC)
```
**参数：** - `key`：来自 KDF 的 32 字节加密密钥 - `nonce`：12 字节（4 个零字节 + 8 字节计数器，小端序） - `associatedData`：握手阶段为 32 字节哈希；数据阶段为零长度 - `plaintext`：要加密的数据（0 个或更多字节）

**输出：** - 密文：与明文长度相同 - MAC：16 字节（Poly1305 认证标签）

**Nonce（随机数）管理：** - 对每个密码实例的计数器从 0 开始 - 在该方向的每次 AEAD 操作后递增 - 数据阶段中 Alice→Bob 与 Bob→Alice 各自使用独立计数器 - 在计数器达到 2^64 - 1 之前必须终止连接

## 消息 1：SessionRequest（会话请求）

Alice 向 Bob 发起连接。

**Noise 操作**: `e, es` (临时密钥的生成与交换)

### 原始格式

```
+----+----+----+----+----+----+----+----+
|                                       |
+    AES-256-CBC Encrypted X (32B)      +
|    Key: RH_B, IV: Bob's published IV  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+    ChaChaPoly Frame (48 bytes)        +
|    Plaintext: 32B (X + options)       |
+    k from KDF-1, n=0, ad=h            +
|                                       |
+----+----+----+----+----+----+----+----+
|    Cleartext Padding (optional)       |
+    Length specified in options         +
|    0 to 65535 - 80 bytes              |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
**大小限制：** - 最小值：80 字节（32 AES + 48 AEAD） - 最大值：总计 65535 字节 - **特殊情况**：连接到 "NTCP" 地址时最大 287 字节（版本检测）

### 解密后的内容

```
+----+----+----+----+----+----+----+----+
|                                       |
+    X (Alice ephemeral public key)     +
|    32 bytes, X25519, little-endian    |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|           Options Block               |
+             (16 bytes)                +
|                                       |
+----+----+----+----+----+----+----+----+
|    Cleartext Padding (optional)       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
### 选项块 (16 字节，大端序)

```
+----+----+----+----+----+----+----+----+
| id | ver|  padLen | m3p2len | Rsvd(0) |
+----+----+----+----+----+----+----+----+
|        tsA        |   Reserved (0)    |
+----+----+----+----+----+----+----+----+

id      : 1 byte  - Network ID (2 for mainnet, 16-254 for testnets)
ver     : 1 byte  - Protocol version (currently 2)
padLen  : 2 bytes - Padding length in this message (0-65455)
m3p2len : 2 bytes - Length of SessionConfirmed part 2 frame
Rsvd    : 2 bytes - Reserved, set to 0
tsA     : 4 bytes - Unix timestamp (seconds since epoch)
Reserved: 4 bytes - Reserved, set to 0
```
**关键字段：** - **Network ID**（自 0.9.42 起）：快速拒绝跨网络连接 - **m3p2len**：消息 3 第 2 部分的精确大小（发送时必须匹配）

### 密钥派生函数（KDF-1）

**初始化协议：**

```
protocol_name = "Noise_XKaesobfse+hs2+hs3_25519_ChaChaPoly_SHA256"
h = SHA256(protocol_name)
ck = h  // Chaining key initialized to hash
```
**MixHash 操作：**

```
h = SHA256(h)                    // Null prologue
h = SHA256(h || rs)              // Bob's static key (known)
h = SHA256(h || e.pubkey)        // Alice's ephemeral key X
// h is now the associated data for message 1 AEAD
```
**MixKey 操作（es pattern，临时-静态握手模式）：**

```
dh_result = X25519(Alice.ephemeral_private, Bob.static_public)
temp_key = HMAC-SHA256(ck, dh_result)
ck = HMAC-SHA256(temp_key, byte(0x01))
k = HMAC-SHA256(temp_key, ck || byte(0x02))
// k is the cipher key for message 1
// ck is retained for message 2 KDF
```
### 实现说明

1. **AES 混淆**: 仅用于抵抗 DPI（深度包检测）；任何拥有 Bob 的 router 哈希和初始向量（IV）的人都可以解密 X
2. **重放防护**: Bob 必须将 X 的取值（或其加密等价物）缓存至少 2*D 秒（D = 最大时钟偏移）
3. **时间戳校验**: Bob 必须拒绝 |tsA - current_time| > D 的连接（通常 D = 60 秒）
4. **曲线校验**: Bob 必须验证 X 为有效的 X25519 点
5. **快速拒绝**: Bob 可在解密前检查 X[31] & 0x80 == 0（有效的 X25519 密钥其最高有效位（MSB）为 0）
6. **错误处理**: 任一失败时，Bob 在随机超时并读取随机字节后以 TCP RST（复位）关闭连接
7. **缓冲**: 为提高效率，Alice 必须一次性写出整个消息（包括填充）

## 消息 2: SessionCreated（会话已创建）

Bob 回复 Alice。

**Noise 操作**: `e, ee` (临时-临时 DH)

### 原始格式

```
+----+----+----+----+----+----+----+----+
|                                       |
+    AES-256-CBC Encrypted Y (32B)      +
|    Key: RH_B, IV: AES state from msg1 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+    ChaChaPoly Frame (48 bytes)        +
|    Plaintext: 32B (Y + options)       |
+    k from KDF-2, n=0, ad=h            +
|                                       |
+----+----+----+----+----+----+----+----+
|    Cleartext Padding (optional)       |
+    Length specified in options         +
|    0 to 65535 - 80 bytes              |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
### 解密内容

```
+----+----+----+----+----+----+----+----+
|                                       |
+    Y (Bob ephemeral public key)       +
|    32 bytes, X25519, little-endian    |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|           Options Block               |
+             (16 bytes)                +
|                                       |
+----+----+----+----+----+----+----+----+
|    Cleartext Padding (optional)       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
### 选项块（16 字节，大端序）

```
+----+----+----+----+----+----+----+----+
| Rsvd(0) | padLen  |   Reserved (0)    |
+----+----+----+----+----+----+----+----+
|        tsB        |   Reserved (0)    |
+----+----+----+----+----+----+----+----+

Rsvd    : 2 bytes - Reserved, set to 0
padLen  : 2 bytes - Padding length in this message
Reserved: 10 bytes - Reserved, set to 0
tsB     : 4 bytes - Unix timestamp (seconds since epoch)
```
### 密钥派生函数（KDF-2）

**MixHash（混合哈希）操作:**

```
h = SHA256(h || encrypted_payload_msg1)  // 32-byte ciphertext
if (msg1_padding_length > 0):
    h = SHA256(h || padding_from_msg1)
h = SHA256(h || e.pubkey)                // Bob's ephemeral key Y
// h is now the associated data for message 2 AEAD
```
**MixKey（密钥混合）操作（ee 模式）：**

```
dh_result = X25519(Bob.ephemeral_private, Alice.ephemeral_public)
temp_key = HMAC-SHA256(ck, dh_result)
ck = HMAC-SHA256(temp_key, byte(0x01))
k = HMAC-SHA256(temp_key, ck || byte(0x02))
// k is the cipher key for message 2
// ck is retained for message 3 KDF
```
**内存清理：**

```
// Overwrite ephemeral keys after ee DH
Alice.ephemeral_public = zeros(32)
Alice.ephemeral_private = zeros(32)  // Bob side
Bob.received_ephemeral = zeros(32)    // Bob side
```
### 实现说明

1. **AES 链式**: Y 加密使用来自消息 1 的 AES-CBC 状态（不重置）
2. **重放防护**: Alice 必须将 Y 值缓存至少 2*D 秒
3. **时间戳验证**: Alice 必须拒绝 |tsB - current_time| > D 的情况
4. **曲线验证**: Alice 必须验证 Y 是有效的 X25519 点
5. **错误处理**: 发生任何失败时 Alice 使用 TCP RST 关闭
6. **缓冲**: Bob 必须一次性刷新整条消息

## 消息 3：SessionConfirmed（会话确认）

Alice 确认会话并发送 RouterInfo。

**Noise（协议框架）操作**: `s, se` (静态密钥公开和静态-临时 DH)

### 两部分结构

消息 3 由**两个独立的 AEAD（带关联数据的认证加密）帧**组成：

1. **第 1 部分**: 固定长度的 48 字节帧，包含 Alice 的加密静态密钥
2. **第 2 部分**: 可变长度的帧，包含 RouterInfo（路由器信息）、选项和填充

### 原始格式

```
+----+----+----+----+----+----+----+----+
|    ChaChaPoly Frame 1 (48 bytes)      |
+    Plaintext: Alice static key (32B)  +
|    k from KDF-2, n=1, ad=h            |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+    ChaChaPoly Frame 2 (variable)      +
|    Length specified in msg1.m3p2len   |
+    k from KDF-3, n=0, ad=h            +
|    Plaintext: RouterInfo + padding    |
+                                       +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
**大小限制：** - 第 1 部分：恰好 48 字节 (32 明文 + 16 MAC) - 第 2 部分：长度由消息 1 指定 (m3p2len 字段) - 总上限：65535 字节 (第 1 部分最多 48，因此第 2 部分最多 65487)

### 解密内容

**第1部分：**

```
+----+----+----+----+----+----+----+----+
|                                       |
+    S (Alice static public key)        +
|    32 bytes, X25519, little-endian    |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
**第2部分：**

```
+----+----+----+----+----+----+----+----+
|    Block: RouterInfo (required)       |
+    Type=2, contains Alice's RI         +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
|    Block: Options (optional)          |
+    Type=1, padding parameters          +
|                                       |
+----+----+----+----+----+----+----+----+
|    Block: Padding (optional)          |
+    Type=254, random data               +
|    MUST be last block if present      |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
### 密钥派生函数（KDF-3）

**第1部分 (s 模式):**

```
h = SHA256(h || encrypted_payload_msg2)  // 32-byte ciphertext
if (msg2_padding_length > 0):
    h = SHA256(h || padding_from_msg2)

// Encrypt static key with message 2 cipher key
ciphertext = AEAD_ChaCha20_Poly1305(k_msg2, n=1, h, Alice.static_public)
h = SHA256(h || ciphertext)  // 48 bytes (32 + 16)
// h is now the associated data for message 3 part 2
```
**第2部分（se 模式）：**

```
dh_result = X25519(Alice.static_private, Bob.ephemeral_public)
temp_key = HMAC-SHA256(ck, dh_result)
ck = HMAC-SHA256(temp_key, byte(0x01))
k = HMAC-SHA256(temp_key, ck || byte(0x02))
// k is the cipher key for message 3 part 2
// ck is retained for data phase KDF

ciphertext = AEAD_ChaCha20_Poly1305(k, n=0, h, payload)
h = SHA256(h || ciphertext)
// h is retained for SipHash KDF
```
**内存清理：**

```
// Overwrite Bob's ephemeral key after se DH
Alice.received_ephemeral = zeros(32)  // Alice side
Bob.ephemeral_public = zeros(32)       // Bob side
Bob.ephemeral_private = zeros(32)      // Bob side
```
### 实现说明


## 数据阶段

在握手完成后，所有消息都使用带有经过混淆的长度字段的可变长度 AEAD（带关联数据的认证加密）帧。

### 密钥派生函数（数据阶段）

**拆分函数 (Noise 协议框架):**

```
// Generate transmit and receive keys
zerolen = ""  // Zero-length byte array
temp_key = HMAC-SHA256(ck, zerolen)

// Alice transmits to Bob
k_ab = HMAC-SHA256(temp_key, byte(0x01))

// Bob transmits to Alice  
k_ba = HMAC-SHA256(temp_key, k_ab || byte(0x02))

// Cleanup
ck = zeros(32)
temp_key = zeros(32)
```
**SipHash 密钥派生:**

```
// Generate additional symmetric key for SipHash
ask_master = HMAC-SHA256(temp_key, "ask" || byte(0x01))

// "siphash" is 7 bytes US-ASCII
temp_key2 = HMAC-SHA256(ask_master, h || "siphash")
sip_master = HMAC-SHA256(temp_key2, byte(0x01))

// Alice to Bob SipHash keys
temp_key3 = HMAC-SHA256(sip_master, zerolen)
sipkeys_ab = HMAC-SHA256(temp_key3, byte(0x01))
sipk1_ab = sipkeys_ab[0:7]   // 8 bytes, little-endian
sipk2_ab = sipkeys_ab[8:15]  // 8 bytes, little-endian
sipiv_ab = sipkeys_ab[16:23] // 8 bytes, IV

// Bob to Alice SipHash keys
sipkeys_ba = HMAC-SHA256(temp_key3, sipkeys_ab || byte(0x02))
sipk1_ba = sipkeys_ba[0:7]   // 8 bytes, little-endian
sipk2_ba = sipkeys_ba[8:15]  // 8 bytes, little-endian
sipiv_ba = sipkeys_ba[16:23] // 8 bytes, IV
```
### 帧结构

```
+----+----+----+----+----+----+----+----+
|Obfs Len |                             |
+----+----+    ChaChaPoly Frame         +
|    Encrypted Block Data               |
+    k_ab (Alice→Bob) or k_ba (Bob→Alice)|
|    Nonce starts at 0, increments      |
+    No associated data (empty string)  +
|                                       |
~           .   .   .                   ~
|                                       |
+----+----+----+----+----+----+----+----+
|    Poly1305 MAC (16 bytes)            |
+----+----+----+----+----+----+----+----+
```
**帧约束：** - 最小值：18 字节（2 字节的混淆长度 + 0 字节明文 + 16 字节的 MAC（消息认证码）） - 最大值：65537 字节（2 字节的混淆长度 + 65535 字节的帧） - 建议：每帧几 KB（尽量降低接收端延迟）

### SipHash 长度混淆

**目的**：防止深度包检测（DPI）识别帧边界

**算法：**

```
// Initialization (per direction)
IV[0] = sipiv  // From KDF

// For each frame:
IV[n] = SipHash-2-4(sipk1, sipk2, IV[n-1])
Mask[n] = IV[n][0:1]  // First 2 bytes of IV
ObfuscatedLength = ActualLength XOR Mask[n]

// Send 2-byte ObfuscatedLength, then ActualLength bytes
```
**解码：**

```
// Receiver maintains identical IV chain
IV[n] = SipHash-2-4(sipk1, sipk2, IV[n-1])
Mask[n] = IV[n][0:1]
ActualLength = ObfuscatedLength XOR Mask[n]
// Read ActualLength bytes (includes 16-byte MAC)
```
**注意：** - 每个方向使用独立的 IV（初始化向量）链（Alice→Bob 与 Bob→Alice） - 如果 SipHash（哈希函数）返回 uint64（无符号 64 位整数），使用最低有效的 2 个字节作为掩码 - 将 uint64 按小端字节序转换为下一个 IV

### 块格式

每个帧包含零个或多个块:

```
+----+----+----+----+----+----+----+----+
|Type| Length  |       Data              |
+----+----+----+                        +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type  : 1 byte  - Block type identifier
Length: 2 bytes - Big-endian, data size (0-65516)
Data  : Variable length payload
```
**大小限制:** - 最大帧: 65535 字节 (包括 MAC) - 最大块空间: 65519 字节 (帧 - 16 字节的 MAC) - 最大单个块: 65519 字节 (3 字节的头部 + 65516 字节的数据)

### 块类型

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DateTime</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Time synchronization (4-byte timestamp)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Options</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Padding parameters, dummy traffic</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo delivery/flooding</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2NP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2NP message with shortened header</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Termination</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Explicit connection close</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">224-253</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental features</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">254</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Padding</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Random padding (must be last)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">255</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Future extensions</td></tr>
  </tbody>
</table>
**块排序规则：** - **消息 3 第 2 部分**：RouterInfo、选项（可选）、填充（可选） - 不得包含其他类型 - **数据阶段**：顺序任意，但以下情况除外：   - 如果存在，填充必须为最后一个块   - 如果存在，终止必须为最后一个块（填充除外） - 每个帧允许包含多个 I2NP 块 - 每个帧不允许包含多个填充块

### 块类型 0: 日期时间

用于时钟偏移检测的时间同步。

```
+----+----+----+----+----+----+----+
| 0  |    4    |     timestamp     |
+----+----+----+----+----+----+----+

Type     : 0
Length   : 4 (big-endian)
Timestamp: 4 bytes, Unix seconds (big-endian)
```
**实现**：将时间四舍五入到最接近的秒，以防止时钟偏差的累积。

### 块类型 1：选项

填充和流量整形参数。

```
+----+----+----+----+----+----+----+----+
| 1  |  size   |tmin|tmax|rmin|rmax|tdmy|
+----+----+----+----+----+----+----+----+
|tdmy|  rdmy   |  tdelay |  rdelay |    |
+----+----+----+----+----+----+----+    +
|         more_options (TBD)            |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type  : 1
Length: 12+ bytes (big-endian)
```
**填充比** (4.4 fixed-point float, value/16.0; 4.4 定点浮点表示：整数部分 4 位、小数部分 4 位，数值 = value/16.0): - `tmin`: 发送最小填充比 (0.0 - 15.9375) - `tmax`: 发送最大填充比 (0.0 - 15.9375) - `rmin`: 接收最小填充比 (0.0 - 15.9375) - `rmax`: 接收最大填充比 (0.0 - 15.9375)

**示例：** - 0x00 = 0% 填充 - 0x01 = 6.25% 填充 - 0x10 = 100% 填充 (1:1 比例) - 0x80 = 800% 填充 (8:1 比例)

**填充流量:** - `tdmy`: 愿意发送的最大速率（2 字节，平均值按字节/秒计） - `rdmy`: 请求接收的速率（2 字节，平均值按字节/秒计）

**延迟插入:** - `tdelay`: 愿意插入的最大值 (2 字节，以毫秒为单位的平均值) - `rdelay`: 请求的延迟 (2 字节，以毫秒为单位的平均值)

**指南：** - 最小值表示期望的抗流量分析能力 - 最大值表示带宽约束 - 发送方应遵从接收方的最大值 - 在约束范围内，发送方可遵从接收方的最小值 - 无强制执行机制；各实现可能有所不同

### 块类型 2: RouterInfo（路由信息）

用于 netdb 填充和泛洪的 RouterInfo（路由器信息）递送。

```
+----+----+----+----+----+----+----+----+
| 2  |  size   |flg |    RouterInfo     |
+----+----+----+----+                   +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type : 2
Length: Flag (1 byte) + RouterInfo size
Flag : Bit 0 = flood request (1) or local store (0)
       Bits 1-7 = Reserved, set to 0
```
**用法：**

**在 Message 3 第 2 部分** (握手): - Alice 将她的 RouterInfo(路由器信息) 发送给 Bob - Flood 位通常为 0(本地存储) - RouterInfo 未进行 gzip 压缩

**在数据阶段：** - 任一方都可以发送其更新后的 RouterInfo - Flood bit（Flood 位） = 1：请求由 floodfill 分发（如果接收方为 floodfill） - Flood bit = 0：仅在本地 netdb 中存储

**验证要求：** 1. 验证签名类型受支持 2. 验证 RouterInfo 签名 3. 验证时间戳在可接受范围内 4. 对于握手: 验证静态密钥与 NTCP2 地址的 "s" 参数匹配 5. 对于数据阶段: 验证 router 哈希与会话对端匹配 6. 仅对包含已发布地址的 RouterInfos 进行泛洪

**注意：** - 无 ACK 机制（如有需要，可使用 I2NP DatabaseStore 并携带回复令牌） - 可能包含第三方 RouterInfos（路由信息对象；floodfill 用途） - 未进行 gzip 压缩（不同于 I2NP DatabaseStore）

### 块类型 3：I2NP 消息

I2NP 消息，采用缩短的 9 字节头部。

```
+----+----+----+----+----+----+----+----+
| 3  |  size   |type|    msg_id         |
+----+----+----+----+----+----+----+----+
|   expiration  |     I2NP payload      |
+----+----+----+                        +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type      : 3
Length    : 9 + payload_size (big-endian)
Type      : 1 byte, I2NP message type
Msg_ID    : 4 bytes, big-endian, I2NP message ID
Expiration: 4 bytes, big-endian, Unix timestamp (seconds)
Payload   : I2NP message body (length = size - 9)
```
**与 NTCP1 的差异：** - 过期时间：4 字节（秒） vs 8 字节（毫秒） - 长度：省略（可由块长度推导） - 校验和：省略（AEAD 提供完整性） - 头部：9 字节 vs 16 字节（减少 44%）

**分片:** - I2NP 消息不得跨块分片 - I2NP 消息不得跨帧分片 - 每帧允许多个 I2NP 块

### 块类型 4：终止

带原因码的显式连接关闭。

```
+----+----+----+----+----+----+----+----+
| 4  |  size   |  valid_frames_recv    |
+----+----+----+----+----+----+----+----+
| (continued) |rsn |   additional_data   |
+----+----+----+----+                   +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type            : 4
Length          : 9+ bytes (big-endian)
Valid_Frames_Recv: 8 bytes, big-endian (receive nonce value)
                  0 if error in handshake phase
Reason          : 1 byte (see table below)
Additional_Data : Optional (format unspecified, for debugging)
```
**原因代码：**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Reason</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Phase</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Normal close / unspecified</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Termination received</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Idle timeout</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Router shutdown</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data phase AEAD failure</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Incompatible options</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Incompatible signature type</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Clock skew</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Padding violation</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">9</td><td style="border:1px solid var(--color-border); padding:0.5rem;">AEAD framing error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Payload format error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Message 1 error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Message 2 error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">13</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Message 3 error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">14</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Intra-frame read timeout</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo signature verification fail</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">16</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Static key parameter mismatch</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">17</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Banned</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td></tr>
  </tbody>
</table>
**规则：** - 终止块必须是帧中最后一个非填充块 - 每个帧最多一个终止块 - 发送方应在发送后关闭连接 - 接收方应在接收后关闭连接

**错误处理：** - 握手错误：通常使用 TCP RST 关闭（不发送终止块） - 数据阶段的 AEAD（带关联数据的认证加密）错误：随机超时 + 随机读取，然后发送终止 - 有关安全流程，参见 "AEAD 错误处理" 一节

### 块类型 254：填充

用于增强对流量分析抗性的随机填充。

```
+----+----+----+----+----+----+----+----+
|254 |  size   |     random_data       |
+----+----+----+                        +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type: 254
Length: 0-65516 bytes (big-endian)
Data: Cryptographically random bytes
```
**规则：** - 如果存在，填充必须是帧中的最后一个块 - 允许零长度填充 - 每个帧中仅允许一个填充块 - 允许仅包含填充的帧 - 应遵循在 Options 块中协商的参数

**消息 1-2 中的填充:** - 位于 AEAD（带有关联数据的认证加密）帧之外（明文） - 包含在下一条消息的哈希链中（已认证） - 当下一条消息的 AEAD 校验失败时检测到篡改

**消息 3+ 和数据阶段中的填充：** - 在 AEAD（带关联数据的认证加密）帧（加密并认证）内 - 用于流量整形和长度混淆

## AEAD 错误处理

**关键安全要求：**

### 握手阶段（消息1-3）

**已知消息大小:** - 消息大小是预先确定或事先指定的 - AEAD（带关联数据的认证加密）认证失败是无歧义的

**Bob 对消息 1 失败的响应：** 1. 设置随机超时（范围取决于实现，建议 100-500ms） 2. 读取随机数量的字节（范围取决于实现，建议 1KB-64KB） 3. 使用 TCP RST（TCP复位）关闭连接（无响应） 4. 临时将源 IP 加入黑名单 5. 跟踪重复失败以实施长期封禁

**Alice 针对消息 2 失败的响应：** 1. 立即使用 TCP RST（重置标志）关闭连接 2. 不向 Bob 作出任何响应

**Bob 对消息 3 失败的响应:** 1. 使用 TCP RST 立即关闭连接 2. 不向 Alice 发送任何响应

### 数据阶段

**已混淆的消息大小:** - 长度字段经 SipHash 混淆 - 长度无效或 AEAD（带关联数据的认证加密）失败可能意味着:   - 攻击者探测   - 网络数据损坏   - SipHash 的 IV（初始化向量）不同步   - 恶意对等节点

**针对 AEAD（带关联数据的认证加密）或长度错误的响应：** 1. 设置随机超时（建议 100-500ms） 2. 读取随机数量的字节（建议 1KB-64KB） 3. 发送带有原因码 4（AEAD 失败）或 9（帧错误）的终止块 4. 关闭连接

**防止解密预言机攻击:** - 在随机超时之前，绝不向对端披露错误类型 - 在进行 AEAD（带关联数据的认证加密）校验之前，绝不跳过长度验证 - 将无效长度视同 AEAD 失败 - 对这两类错误使用相同的错误处理路径

**实施注意事项：** - 某些实现若 AEAD（带关联数据的认证加密）错误不频繁，可能会继续运行 - 在错误反复出现时应终止（建议阈值：每小时 3-5 次错误） - 在错误恢复与安全性之间取得平衡

## 已发布的 RouterInfo（router 信息记录）

### Router 地址格式

通过在已发布的 RouterAddress（router 地址）条目中包含特定选项来公布对 NTCP2 的支持。

**传输样式:** - `"NTCP2"` - 此端口仅使用 NTCP2 - `"NTCP"` - 此端口同时支持 NTCP 和 NTCP2（自动检测）   - **注意**: NTCP (v1) 支持已在 0.9.50 (May 2021) 中移除   - "NTCP" 样式现已废弃; 请改用 "NTCP2"

### 必需选项

**所有已发布的 NTCP2 地址：**

1. **`host`** - IP 地址（IPv4 或 IPv6）或主机名
   - 格式：标准 IP 表示法或域名
   - 对于仅出站或隐藏的 routers，可以省略

2. **`port`** - TCP 端口号
   - 格式：整数，1-65535
   - 对于仅出站或隐藏的 routers 可以省略

3. **`s`** - 静态公钥（X25519）
   - 格式：Base64 编码，44 个字符
   - 编码：I2P Base64 字母表
   - 来源：32 字节的 X25519 公钥，小端序

4. **`i`** - 用于 AES 的初始化向量（IV）
   - 格式：Base64 编码，24 个字符
   - 编码：I2P Base64 字母表
   - 来源：16 字节的 IV，大端序

5. **`v`** - 协议版本
   - 格式: 整数或用逗号分隔的整数
   - 当前: `"2"`
   - 未来: `"2,3"`（必须按数值顺序排列）

**可选选项：**

6. **`caps`** - 能力（自 0.9.50 起）
   - 格式：由能力字符组成的字符串
   - 取值：
     - `"4"` - IPv4 出站能力
     - `"6"` - IPv6 出站能力
     - `"46"` - 同时支持 IPv4 和 IPv6（推荐顺序）
   - 如果已发布 `host` 则不需要
   - 适用于隐藏的/位于防火墙后的 routers

7. **`cost`** - 地址优先级
   - 格式: 整数, 0-255
   - 数值越低 = 优先级越高
   - 建议: 普通地址使用 5-10
   - 建议: 未发布的地址使用 14

### RouterAddress 示例条目

**已发布的 IPv4 地址:**

```
<Address cost="5">
  <transport_style>NTCP2</transport_style>
  <options>
    <host>192.0.2.1</host>
    <port>8887</port>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <i>MDEyMzQ1Njc4OUFCQ0RFRg==</i>
    <v>2</v>
  </options>
</Address>
```
**隐藏 Router (仅出站):**

```
<Address cost="14">
  <transport_style>NTCP2</transport_style>
  <options>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <v>2</v>
    <caps>4</caps>
  </options>
</Address>
```
**双栈 Router：**

```
<!-- IPv4 Address -->
<Address cost="5">
  <transport_style>NTCP2</transport_style>
  <options>
    <host>192.0.2.1</host>
    <port>8887</port>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <i>MDEyMzQ1Njc4OUFCQ0RFRg==</i>
    <v>2</v>
  </options>
</Address>

<!-- IPv6 Address (same keys, same port) -->
<Address cost="5">
  <transport_style>NTCP2</transport_style>
  <options>
    <host>2001:db8::1</host>
    <port>8887</port>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <i>MDEyMzQ1Njc4OUFCQ0RFRg==</i>
    <v>2</v>
  </options>
</Address>
```
**重要规则：** - 使用**相同端口**的多个 NTCP2 地址必须使用**完全相同**的 `s`、`i` 和 `v` 值 - 不同端口可以使用不同的密钥 - 双栈 routers 应分别发布 IPv4 和 IPv6 地址

### 未发布的 NTCP2 地址

**针对仅出站的 router:**

如果一个 router 不接受传入的 NTCP2 连接，但会发起出站连接，它仍然必须发布一个包含以下内容的 RouterAddress（路由地址）：

```xml
<Address cost="14">
  <transport_style>NTCP2</transport_style>
  <options>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <v>2</v>
  </options>
</Address>
```
**目的:** - 允许 Bob 在握手期间验证 Alice 的静态密钥 - 用于消息 3 第 2 部分的 RouterInfo 验证所必需 - 无需 `i`、`host` 或 `port` (仅出站)

**替代方案：** - 为现有已发布的 "NTCP" 或 SSU 地址添加 `s` 和 `v`

### 公钥和IV轮换

**关键安全策略:**

**通用规则：** 1. **在 router 正在运行时切勿进行轮换** 2. **持久化存储密钥和 IV（初始化向量）** 跨重启 3. **跟踪先前的停机时间** 以确定是否符合轮换条件

**轮换前的最小停机时间：**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Router Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Min Downtime</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Reason</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Published NTCP2 address</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>1 month</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Many routers cache RouterInfo</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Published SSU only (no NTCP2)</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>1 day</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Moderate caching</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">No published addresses (hidden)</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>2 hours</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimal impact</td></tr>
  </tbody>
</table>
**附加触发条件:** - 本地 IP 地址变更: 无论是否停机，均可能轮换 - Router "rekey" (重新生成密钥) (新的 Router Hash): 生成新密钥

**理由：** - 防止通过密钥更改暴露重启时间 - 允许缓存的 RouterInfos（I2P 路由信息对象）自然过期 - 保持网络稳定性 - 减少失败的连接尝试

**实现：** 1. 持久化存储密钥、IV（初始化向量）和上次关闭时间戳 2. 在启动时，计算停机时间 = current_time - last_shutdown 3. 如果停机时间 > 对应 router 类型的最小值，则可以轮换 4. 如果 IP 发生变化或 rekeying（重新生成密钥），则可以轮换 5. 否则，复用先前的密钥和 IV

**IV（初始化向量）轮换：** - 适用与密钥轮换相同的规则 - 仅出现在已发布的地址中（非隐藏的 router） - 建议每当密钥更改时更换 IV

## 版本检测

**上下文：** 当 `transportStyle="NTCP"`（旧版）时，Bob 在同一端口上同时支持 NTCP v1 和 v2，并且必须自动检测协议版本。

**检测算法：**

```
1. Wait for at least 64 bytes (minimum NTCP2 message 1 size)

2. If received ≥ 288 bytes:
   → Connection is NTCP version 1 (NTCP1 message 1 is 288 bytes)

3. If received < 288 bytes:
   
   Option A (conservative, pre-NTCP2 majority):
   a. Wait additional short time (e.g., 100-500ms)
   b. If total received ≥ 288 bytes → NTCP1
   c. Otherwise → Attempt NTCP2 decode
   
   Option B (aggressive, post-NTCP2 majority):
   a. Attempt NTCP2 decode immediately:
      - Decrypt first 32 bytes (X key) with AES-256-CBC
      - Verify valid X25519 point (X[31] & 0x80 == 0)
      - Verify AEAD frame
   b. If decode succeeds → NTCP2
   c. If decode fails → Wait for more data or NTCP1
```
**快速最高有效位（MSB）检查：** - 在 AES 解密之前，验证：`encrypted_X[31] & 0x80 == 0` - 有效的 X25519 密钥应当最高位为 0 - 失败表明很可能是 NTCP1（或攻击） - 在失败时实现防探测机制（随机超时 + 读取）

**实现要求:**

1. **Alice 的职责：**
   - 在连接到"NTCP"地址时，将消息 1 限制为最多 287 字节
   - 将整个消息 1 缓冲并一次性写出
   - 提高通过单个 TCP 数据包传递的可能性

2. **Bob 的职责：**
   - 在确定版本之前先缓冲已接收的数据
   - 实现正确的超时处理
   - 使用 TCP_NODELAY 以快速进行版本检测
   - 在检测到版本后，将第 2 条消息整体一次性缓冲并刷新发送

**安全考虑：** - 分段攻击：Bob 应该能够抵御 TCP 分段 - 探测攻击：在失败时引入随机延迟并执行字节读取 - 拒绝服务（DoS）预防：限制并发的挂起连接数 - 读取超时：同时设置单次读取和总体超时（"slowloris"（慢速 HTTP 攻击）防护）

## 时钟偏差指南

**时间戳字段：** - 消息 1：`tsA`（Alice 的时间戳） - 消息 2：`tsB`（Bob 的时间戳） - 消息 3+：可选的 DateTime（日期时间）块

**最大时钟偏移（D）：** - 典型：**±60 秒** - 可按实现配置 - 偏移量 > D 通常是致命的

### Bob 的处理 (消息 1)

```
1. Receive tsA from Alice
2. skew = tsA - current_time
3. If |skew| > D:
   a. Still send message 2 (allows Alice to calculate skew)
   b. Include tsB in message 2
   c. Do NOT initiate handshake completion
   d. Optionally: Temporary ban Alice's IP
   e. After message 2 sent, close connection

4. If |skew| ≤ D:
   a. Continue handshake normally
```
**理由：** 即使在时钟偏差的情况下也发送消息 2，以便 Alice 诊断时钟问题。

### Alice 的处理（消息 2）

```
1. Receive tsB from Bob
2. RTT = (current_time_now - tsA_sent)
3. adjusted_skew = (tsB - current_time_now) - (RTT / 2)
4. If |adjusted_skew| > D:
   a. Close connection immediately
   b. If local clock suspect: Adjust clock or use external time source
   c. If Bob's clock suspect: Temporary ban Bob
   d. Log for operator review
5. If |adjusted_skew| ≤ D:
   a. Continue handshake normally
   b. Optionally: Track skew for time synchronization
```
**RTT（往返时延）调整：** - 从计算出的时钟偏移中减去一半的 RTT - 考虑网络传播时延 - 更准确的时钟偏移估计

### Bob 的处理 (消息 3)

```
1. If message 3 received (unlikely if skew exceeded in message 1)
2. Recalculate skew = tsA_received - current_time
3. If |adjusted_skew| > D:
   a. Send termination block (reason code 7: clock skew)
   b. Close connection
   c. Ban Alice for period (e.g., 1-24 hours)
```
### 时间同步

**DateTime 块 (数据阶段):** - 定期发送 DateTime 块 (类型 0) - 接收方可用于时钟校准 - 将时间戳四舍五入到最近一秒 (避免偏差)

**外部时间源：** - NTP（网络时间协议） - 系统时钟同步 - I2P 网络共识时间

**时钟调整策略：** - 如果本地时钟异常：调整系统时间或使用偏移量 - 如果对等方的时钟持续异常：将该对等方标记为有问题 - 跟踪 skew（时钟偏差）统计用于网络健康监测

## 安全属性

### 前向保密

**通过以下方式实现：** - 临时 Diffie-Hellman 密钥交换 (X25519) - 三次 DH 操作：es、ee、se (Noise XK 模式) - 握手完成后销毁临时密钥

**机密性演进：** - 消息 1：级别 2（发送方被攻陷时具备前向保密性） - 消息 2：级别 1（临时接收方） - 消息 3+：级别 5（强前向保密性）

**完美前向保密:** - 长期静态密钥被泄露也绝不会暴露过去的会话密钥 - 每个会话使用唯一的临时密钥 - 临时私钥从不复用 - 密钥协商后清理内存

**限制:** - 如果 Bob 的静态密钥泄露，消息 1 将易受攻击（但在 Alice 的密钥被攻破的情况下仍具有前向保密性） - 消息 1 可能遭受重放攻击（可通过时间戳和重放缓存缓解）

### 身份验证

**相互认证:** - Alice 通过第 3 条消息中的静态密钥完成认证 - Bob 通过持有静态私钥完成认证（握手成功即为隐式证明）

**密钥泄露冒充（KCI）抗性：** - 认证级别 2（对 KCI 具备抗性） - 即使攻击者拥有 Alice 的静态私钥（但没有 Alice 的临时密钥），也无法冒充 Alice - 即使攻击者拥有 Bob 的静态私钥（但没有 Bob 的临时密钥），也无法冒充 Bob

**静态密钥验证:** - Alice 预先知道 Bob 的静态密钥（来自 RouterInfo，I2P 路由信息文件） - Bob 在第 3 条消息中验证 Alice 的静态密钥与 RouterInfo 一致 - 防止中间人攻击

### 抗流量分析能力

**DPI（深度包检测）对抗措施:** 1. **AES 混淆:** 临时密钥被加密，看起来随机 2. **SipHash 长度混淆:** 帧长度非明文 3. **随机填充:** 消息大小可变，无固定模式 4. **加密帧:** 所有负载均使用 ChaCha20 加密

**重放攻击防护：** - 时间戳验证 (±60 秒) - 针对临时密钥的重放缓存 (有效期 2*D) - 随机数递增可防止会话内的数据包重放

**抗探测能力:** - AEAD（带关联数据的认证加密）失败时随机超时 - 在关闭连接前随机读取字节 - 握手失败时不响应 - 对多次失败的 IP 进行黑名单处理

**填充指南：** - 消息 1-2：明文填充（已认证） - 消息 3+：AEAD 帧内的加密填充 - 协商的填充参数（选项块） - 允许仅包含填充的帧

### 拒绝服务攻击缓解

**连接限制：** - 最大活动连接数（取决于实现） - 最大待处理握手数（例如，100-1000） - 每个 IP 的连接限制（例如，同时 3-10 个）

**资源保护:** - 对 DH 操作进行速率限制(开销高) - 每个套接字及全局的读取超时 - "Slowloris" 防护(总时间限制) - 针对滥用行为的 IP 黑名单

**快速拒绝:** - 网络ID不匹配 → 立即关闭 - 无效的 X25519 点 → 在解密前进行快速最高有效位（MSB）检查 - 时间戳超出范围 → 不进行计算直接关闭 - AEAD（带附加数据的认证加密）验证失败 → 不响应，随机延迟

**抗探测性：** - 随机超时：100-500ms（取决于实现） - 随机读取：1KB-64KB（取决于实现） - 不向攻击者提供错误信息 - 使用 TCP RST 关闭（无 FIN 握手）

### 密码学安全

**算法:** - **X25519**: 128 位安全性，椭圆曲线 DH（Curve25519） - **ChaCha20**: 256 位密钥流密码 - **Poly1305**: 信息论安全的 MAC - **SHA-256**: 128 位抗碰撞性，256 位抗原像性 - **HMAC-SHA256**: 用于密钥派生的伪随机函数（PRF）

**密钥长度：** - 静态密钥：32 字节 (256 位) - 临时密钥：32 字节 (256 位) - 加密密钥：32 字节 (256 位) - MAC (消息认证码)：16 字节 (128 位)

**已知问题：** - ChaCha20 的 nonce 重用会造成灾难性后果（通过计数器递增加以防止） - X25519 存在小子群问题（通过曲线验证加以缓解） - SHA-256 理论上易受长度扩展攻击影响（在 HMAC 中不可利用）

**无已知漏洞（截至2025年10月）：** - Noise Protocol Framework（噪声协议框架）已被广泛分析 - ChaCha20-Poly1305 已在 TLS 1.3 中部署 - X25519 已成为现代协议中的标准 - 对该构造暂无实用性攻击

## 参考资料

### 主要规范

- **[NTCP2 规范](/docs/specs/ntcp2/)** - I2P 官方规范
- **[提案 111](/proposals/111-ntcp-2/)** - 包含设计理由的原始设计文档
- **[Noise 协议框架](https://noiseprotocol.org/noise.html)** - 第 33 版（2017-10-04）

### 密码学标准

- **[RFC 7748](https://www.rfc-editor.org/rfc/rfc7748)** - 用于安全的椭圆曲线 (X25519)
- **[RFC 7539](https://www.rfc-editor.org/rfc/rfc7539)** - 用于 IETF 协议的 ChaCha20 和 Poly1305
- **[RFC 8439](https://www.rfc-editor.org/rfc/rfc8439)** - ChaCha20-Poly1305（取代 RFC 7539）
- **[RFC 2104](https://www.rfc-editor.org/rfc/rfc2104)** - HMAC：用于消息认证的带密钥哈希
- **[SipHash](https://www.131002.net/siphash/)** - 用于哈希函数应用的 SipHash-2-4

### 相关的 I2P 规范

- **[I2NP 规范](/docs/specs/i2np/)** - I2P 网络协议消息格式
- **[通用结构](/docs/specs/common-structures/)** - RouterInfo、RouterAddress 格式
- **[SSU 传输](/docs/legacy/ssu/)** - UDP 传输（最初版本，现为 SSU2）
- **[提案 147](/proposals/147-transport-network-id-check/)** - 传输网络 ID 检查（0.9.42）

### 实现参考

- **[I2P Java](https://github.com/i2p/i2p.i2p)** - 参考实现（Java）
- **[i2pd](https://github.com/PurpleI2P/i2pd)** - C++ 实现
- **[I2P 发布说明](/blog/)** - 版本历史和更新

### 历史背景

- **[站到站协议 (STS)](https://en.wikipedia.org/wiki/Station-to-Station_protocol)** - Noise 框架的灵感来源
- **[obfs4](https://gitlab.com/yawning/obfs4)** - 可插拔传输 (SipHash 长度混淆先例)

## 实现指南

### 强制性要求

**用于合规：**

1. **实现完整握手:**
   - 以正确的 KDF（密钥派生函数）链支持全部三条消息
   - 校验所有 AEAD（附加数据认证加密）标签
   - 验证 X25519（基于 Curve25519 的密钥交换算法）曲线点是否有效

2. **实现数据阶段:**
   - SipHash 长度混淆（双向）
   - 所有块类型: 0（日期时间）, 1（选项）, 2（RouterInfo）, 3（I2NP）, 4（终止）, 254（填充）
   - 正确的 nonce（一次性随机数）管理（独立计数器）

3. **安全特性：**
   - 重放防护（缓存临时密钥 2*D 的时间）
   - 时间戳校验（默认 ±60 秒）
   - 在消息 1-2 中加入随机填充
   - AEAD（带关联数据的认证加密）错误处理采用随机超时

4. **RouterInfo（路由信息）发布:**
   - 发布静态密钥（"s"）、IV（初始化向量，"i"）和版本（"v"）
   - 按照策略轮换密钥
   - 支持用于隐藏的 router 的 capabilities（能力）字段（"caps"）

5. **网络兼容性：**
   - 支持 network ID 字段（当前主网为 2）
   - 与现有的 Java 和 i2pd 实现互操作
   - 同时处理 IPv4 和 IPv6

### 推荐实践

**性能优化：**

1. **缓冲策略：**
   - 一次性发送完整消息（消息 1、2、3）
   - 对握手消息使用 TCP_NODELAY
   - 将多个数据块缓冲合并为单个帧
   - 将帧大小限制在几 KB（以最小化接收端延迟）

2. **连接管理:**
   - 尽可能复用连接
   - 实现连接池
   - 监控连接健康状况 (DateTime blocks，指与日期时间相关的阻塞)

3. **内存管理：**
   - 在使用后将敏感数据清零（短期密钥、DH 结果）
   - 限制并发握手（防止 DoS 拒绝服务）
   - 为频繁分配使用内存池

**安全加固：**

1. **抗探测性:**
   - 随机超时：100-500ms
   - 随机字节读取：1KB-64KB
   - 对多次失败的 IP 实施黑名单
   - 不向对等方提供错误细节

2. **资源限制：**
   - 每个 IP 的最大连接数：3-10
   - 最大待处理握手数：100-1000
   - 读取超时：每次操作 30-60 秒
   - 连接总超时：握手阶段 5 分钟

3. **密钥管理：**
   - 静态密钥和初始化向量（IV）的持久化存储
   - 安全随机生成（使用密码学安全随机数生成器）
   - 严格遵循密钥轮换策略
   - 切勿重复使用临时密钥

**监控与诊断：**

1. **指标:**
   - 握手成功/失败率
   - AEAD 错误率
   - 时钟偏移分布
   - 连接持续时间统计

2. **日志记录:**
   - 记录握手失败及其原因代码
   - 记录时钟偏差事件
   - 记录被封禁的 IP 地址
   - 绝不记录敏感的密钥材料

3. **测试:**
   - 针对 KDF 链的单元测试
   - 与其他实现的集成测试
   - 针对数据包处理的模糊测试
   - 针对抗 DoS 能力的负载测试

### 常见误区

**应避免的严重错误:**

1. **随机数重用：**
   - 切勿在会话中途重置随机数计数器
   - 每个方向使用独立的计数器
   - 在达到 2^64 - 1 之前终止会话

2. **密钥轮换:**
   - 切勿在 router 运行时轮换密钥
   - 切勿在不同会话间复用临时密钥
   - 遵循最小停机时间规则

3. **时间戳处理:**
   - 绝不接受已过期的时间戳
   - 计算偏差时始终根据 RTT（往返时延）进行调整
   - 将 DateTime 时间戳舍入到秒

4. **AEAD（带关联数据的认证加密）错误：**
   - 切勿向攻击者透露错误类型
   - 在关闭前始终使用随机延时
   - 将无效长度与 AEAD 失败同等处理

5. **填充:**
   - 切勿在已协商范围之外发送填充数据
   - 始终将填充块放在最后
   - 每个帧中绝不使用多个填充块

6. **RouterInfo:**
   - 始终验证静态密钥是否与 RouterInfo 匹配
   - 切勿泛洪未发布地址的 RouterInfos
   - 始终验证签名

### 测试方法论

**单元测试：**

1. **密码学原语:**
   - 针对 X25519（椭圆曲线密钥协商算法）、ChaCha20（流密码）、Poly1305（消息认证码算法/MAC）、SHA-256（哈希函数）的测试向量
   - HMAC-SHA256（基于密钥的哈希消息认证码，使用 SHA-256）的测试向量
   - SipHash-2-4（带密钥的短输入散列，用于哈希表防碰撞）的测试向量

2. **KDF 链（Key Derivation Function，密钥派生函数）:**
   - 针对全部三条消息的已知答案测试
   - 验证 chaining key（链密钥）的传递
   - 测试 SipHash IV（初始向量）的生成

3. **消息解析:**
   - 有效消息解码
   - 无效消息拒绝
   - 边界条件（空、最大大小）

**集成测试：**

1. **握手：**
   - 成功完成三次消息交互
   - 时钟偏移拒绝
   - 重放攻击检测
   - 无效密钥拒绝

2. **数据阶段：**
   - I2NP 消息传输
   - RouterInfo（路由信息）交换
   - 填充处理
   - 终止消息

3. **互操作性:**
   - 针对 Java I2P 进行测试
   - 针对 i2pd 进行测试
   - 测试 IPv4 和 IPv6
   - 测试已发布和隐藏的 routers

**安全测试：**

1. **负向测试：**
   - 无效的 AEAD 标签
   - 重放消息
   - 时钟偏移攻击
   - 畸形帧

2. **DoS（拒绝服务）测试：**
   - 连接泛洪
   - Slowloris 攻击（慢速 HTTP 头攻击）
   - CPU 耗尽（过度使用 DH/Diffie-Hellman 密钥交换）
   - 内存耗尽

3. **模糊测试:**
   - 随机握手报文
   - 随机的数据阶段帧
   - 随机的数据块类型和大小
   - 无效的密码学参数

### 从 NTCP 迁移

**关于遗留 NTCP 支持（现已移除）：**

NTCP（版本 1）已在 I2P 0.9.50（2021 年 5 月）中移除。所有当前实现都必须支持 NTCP2。历史说明：

1. **过渡期 (2018-2021):**
   - 0.9.36: 引入 NTCP2（默认禁用）
   - 0.9.37: 默认启用 NTCP2
   - 0.9.40: NTCP 已弃用
   - 0.9.50: NTCP 已移除

2. **版本检测：**
   - "NTCP" transportStyle 表明同时支持两个版本
   - "NTCP2" transportStyle 表明仅支持 NTCP2
   - 通过消息大小自动检测（287 与 288 字节）

3. **当前状态：**
   - 所有 router 必须支持 NTCP2
   - "NTCP" transportStyle 已废弃
   - 仅使用 "NTCP2" transportStyle

## 附录 A：Noise XK 模式

**标准 Noise XK 模式：**

```
XK(s, rs):
  <- s
  ...
  -> e, es
  <- e, ee
  -> s, se
```
**解释：**

- `<-` : 来自响应方（Bob）发往发起方（Alice）的消息
- `->` : 来自发起方（Alice）发往响应方（Bob）的消息
- `s` : 静态密钥（长期身份密钥）
- `rs` : 远端静态密钥（对端的静态密钥，事先已知）
- `e` : 临时密钥（特定于会话，按需生成）
- `es` : 临时-静态 DH（Diffie-Hellman）（Alice 的临时 × Bob 的静态）
- `ee` : 临时-临时 DH（Alice 的临时 × Bob 的临时）
- `se` : 静态-临时 DH（Alice 的静态 × Bob 的临时）

**密钥协商流程：**

1. **预消息:** Alice 知道 Bob 的静态公钥（来自 RouterInfo，I2P 的路由信息记录）
2. **消息 1:** Alice 发送临时密钥，执行 es DH（ephemeral-static，临时-静态）
3. **消息 2:** Bob 发送临时密钥，执行 ee DH（ephemeral-ephemeral，临时-临时）
4. **消息 3:** Alice 披露静态公钥，执行 se DH（static-ephemeral，静态-临时）

**安全属性：**

- Alice 已认证：是（由第 3 条消息）
- Bob 已认证：是（通过持有静态私钥）
- 前向保密：是（临时密钥已销毁）
- KCI（Key Compromise Impersonation，密钥泄露冒充攻击）抵抗能力：是（认证级别 2）

## 附录 B：Base64 编码

**I2P Base64 字母表：**

```
ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-~
```
**与标准 Base64 的差异：** - 字符 62-63：`-~` 代替 `+/` - 填充：相同（`=`）或根据上下文省略

**在 NTCP2 中的用法：** - 静态密钥 ("s"): 32 字节 → 44 个字符 (无填充) - IV (初始化向量) ("i"): 16 字节 → 24 个字符 (无填充)

**编码示例：**

```python
# 32-byte static key (hex): 
# f4489e1bb0597b39ca6cbf5ad9f5f1f09043e02d96cb9aa6a63742b3462429aa

# I2P Base64 encoded:
# 9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=
```
## 附录C：数据包捕获分析

**识别 NTCP2 流量：**

1. **TCP 握手:**
   - 标准的 TCP SYN、SYN-ACK、ACK
   - 目标端口通常为 8887 或类似端口

2. **消息 1 (SessionRequest, 会话请求):**
   - 来自 Alice 的首个应用数据
   - 80-65535 字节（通常为几百字节）
   - 看起来像随机数据（AES 加密的临时密钥）
   - 如果连接到 "NTCP" 地址，最大为 287 字节

3. **消息 2 (SessionCreated):**
   - 来自 Bob 的响应
   - 80-65535 字节（通常为几百字节）
   - 同样看起来是随机的

4. **消息 3 (SessionConfirmed，会话确认):**
   - 来自 Alice
   - 48 字节 + 可变 (RouterInfo (路由器信息) 大小 + 填充)
   - 通常为 1-4 KB

5. **数据阶段:**
   - 可变长度帧
   - 长度字段被混淆（看起来随机）
   - 加密的有效载荷
   - 填充使大小不可预测

**DPI 规避:** - 无明文头部 - 无固定模式 - 长度字段已混淆 - 随机填充使基于大小的启发式失效

**与 NTCP 的比较：** - NTCP 消息 1 始终为 288 字节（可识别） - NTCP2 消息 1 大小可变（不可识别） - NTCP 存在可识别的模式 - NTCP2 旨在抵抗深度包检测（DPI）

## 附录 D：版本历史

**主要里程碑：**

- **0.9.36** (2018年8月23日): 引入 NTCP2，默认禁用
- **0.9.37** (2018年10月4日): NTCP2 默认启用
- **0.9.40** (2019年5月20日): NTCP 已弃用
- **0.9.42** (2019年8月27日): 添加了网络 ID 字段 (提案 147)
- **0.9.50** (2021年5月17日): 移除了 NTCP，添加了 capabilities (能力标识) 支持
- **2.10.0** (2025年9月9日): 最新稳定版

**协议稳定性：** - 自 0.9.50 起无不兼容变更 - 持续提升抗探测能力 - 重点关注性能与可靠性 - 后量子密码学开发中（默认未启用）

**当前传输状态:** - NTCP2: 强制的 TCP 传输 - SSU2: 强制的 UDP 传输 - NTCP (v1): 已移除 - SSU (v1): 已移除
