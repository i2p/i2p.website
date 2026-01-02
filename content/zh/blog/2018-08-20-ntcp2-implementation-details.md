---
title: "NTCP2 实现细节"
date: 2018-08-20
author: "villain"
description: "I2P 新的传输协议实现细节和技术规范"
categories: ["development"]
---

I2P 的传输协议最初是在大约 15 年前开发的。当时的主要目标是隐藏传输的数据，而不是隐藏正在使用该协议这一事实。那时几乎没人认真考虑如何抵御 DPI（深度包检测）和对协议的审查。时代变了，尽管最初的传输协议仍然提供很强的安全性，但人们也需要一种新的传输协议。NTCP2 的设计旨在抵御当下的审查威胁，尤其是针对 DPI 对数据包长度的分析。此外，该新协议采用了最新的密码学成果。NTCP2 基于 [Noise Protocol Framework](https://noiseprotocol.org/noise.html)（Noise 协议框架），使用 SHA256 作为哈希函数，并采用 x25519 作为椭圆曲线 Diffie–Hellman（DH）密钥交换。

NTCP2 协议的完整规范可在[此处](/docs/specs/ntcp2/)找到。

## 新的密码学

NTCP2 要求在 I2P 的实现中添加以下加密算法：

- x25519
- HMAC-SHA256
- Chacha20
- Poly1305
- AEAD
- SipHash

与我们最初的协议 NTCP 相比，NTCP2 在 DH（Diffie-Hellman）功能上使用 x25519 替代 ElGamal，采用 AEAD/Chaha20/Poly1305 替代 AES-256-CBC/Adler32，并使用 SipHash 来混淆数据包的长度信息。NTCP2 所使用的密钥派生函数更加复杂，现在会使用大量的 HMAC-SHA256 调用。

*i2pd（C++）实现说明：上述所有算法（除 SipHash 外）均已在 OpenSSL 1.1.0 中实现。SipHash 将在即将发布的 OpenSSL 1.1.1 版本中加入。为兼容当前大多数系统使用的 OpenSSL 1.0.2，i2pd 核心开发者 [Jeff Becker](https://github.com/majestrate) 贡献了缺失密码算法的独立实现。*

## RouterInfo 变更

NTCP2 需要在现有的两把（加密密钥和签名密钥）之外再增加第三把（x25519）密钥。它称为静态密钥（static key），必须作为"s"参数添加到 RouterInfo 的地址中。该要求适用于 NTCP2 的发起方（Alice）和响应方（Bob）。如果有多个地址支持 NTCP2，例如 IPv4 和 IPv6，则所有这些地址的"s"必须相同。允许 Alice 的地址仅包含"s"参数，而不设置"host"和"port"。此外，还需要一个"v"参数，目前总是设为"2"。

NTCP2 地址可以声明为一个单独的 NTCP2 地址，或作为带有附加参数的旧式 NTCP 地址，在这种情况下，它将同时接受 NTCP 和 NTCP2 连接。Java I2P 实现使用第二种方式，i2pd（C++ 实现）使用第一种。

如果一个节点接受 NTCP2 连接，则必须在发布其 RouterInfo 时包含“i”参数；当该节点建立新连接时，该参数用作公钥的初始化向量（IV）。

## 建立连接

为了建立连接，双方都需要各自生成临时 x25519 密钥对。基于这些密钥和"静态"密钥，他们派生出一组用于数据传输的密钥。双方必须验证对端确实拥有该静态密钥对应的私钥，并且该静态密钥与 RouterInfo 中的一致。

为建立连接，将发送三条消息：

```
Alice                           Bob

SessionRequest ------------------->
<------------------- SessionCreated
SessionConfirmed ----------------->
```
对于每条消息，会计算一个共享的 x25519 密钥，称为«input key material》，随后使用 MixKey 函数生成消息加密密钥。在消息交换期间，会保持一个值 ck（链式密钥）。在生成用于数据传输的密钥时，该值被用作最终输入。

MixKey 函数在 I2P 的 C++ 实现中看起来大致如下：

```cpp
void NTCP2Establisher::MixKey (const uint8_t * inputKeyMaterial, uint8_t * derived)
{
    // temp_key = HMAC-SHA256(ck, input_key_material)
    uint8_t tempKey[32]; unsigned int len;
    HMAC(EVP_sha256(), m_CK, 32, inputKeyMaterial, 32, tempKey, &len);
    // ck = HMAC-SHA256(temp_key, byte(0x01))
    static uint8_t one[1] =  { 1 };
    HMAC(EVP_sha256(), tempKey, 32, one, 1, m_CK, &len);
    // derived = HMAC-SHA256(temp_key, ck || byte(0x02))
    m_CK[32] = 2;
    HMAC(EVP_sha256(), tempKey, 32, m_CK, 33, derived, &len);
}
```
**SessionRequest** 消息由 Alice 的 x25519 公钥（32 字节）、一个使用 AEAD/Chacha20/Poly1305 加密的数据块（16 字节）、一个哈希（16 字节），以及末尾的一些随机数据（填充）组成。填充长度在该加密数据块中定义。加密块还包含 **SessionConfirmed** 消息第二部分的长度。该数据块使用由 Alice 的临时密钥和 Bob 的静态密钥派生出的密钥进行加密并签名。MixKey 函数的初始 ck 值设为 SHA256（Noise_XKaesobfse+hs2+hs3_25519_ChaChaPoly_SHA256）。

由于 32 字节的 x25519 公钥可以被深度包检测（DPI）检测到，因此使用 AES-256-CBC 算法对其加密，密钥为 Bob 的地址的哈希，初始化向量（IV）为来自 RouterInfo 的 "i" 参数。

**SessionCreated** 消息与 **SessionRequest** 具有相同的结构，唯一的区别是密钥是基于双方的临时密钥计算得到的。在对来自 **SessionRequest** 消息的公钥进行加密/解密后生成的 IV（初始化向量）被用作对临时公钥进行加密/解密的 IV。

**SessionConfirmed** 消息包含两部分：静态公钥和 Alice 的 RouterInfo。与之前的消息不同之处在于，临时公钥使用与 **SessionCreated** 相同的密钥，通过 AEAD/Chaha20/Poly1305 加密。这使得消息的第一部分从 32 字节增加到 48 字节。第二部分同样使用 AEAD/Chaha20/Poly1305 加密，但使用的是由 Bob 的临时密钥和 Alice 的静态密钥计算得到的新密钥。RouterInfo 部分也可以附加随机数据填充，但这不是必需的，因为 RouterInfo 通常长度不固定。

## 数据传输密钥的生成

如果每次哈希和密钥验证都成功，那么在双方最后一次 MixKey 操作之后，必须存在一个共同的 ck 值。该值用于生成两套密钥 <k, sipk, sipiv>，分别用于连接的两端。"k" 是一个 AEAD/Chaha20/Poly1305 密钥，"sipk" 是一个 SipHash 密钥，"sipiv" 是 SipHash IV（初始向量）的初始值，每次使用后都会改变。

在 I2P 的 C++ 实现中，用于生成密钥的代码如下：

```cpp
void NTCP2Session::KeyDerivationFunctionDataPhase ()
{
    uint8_t tempKey[32]; unsigned int len;
    // temp_key = HMAC-SHA256(ck, zerolen)
    HMAC(EVP_sha256(), m_Establisher->GetCK (), 32, nullptr, 0, tempKey, &len);
    static uint8_t one[1] =  { 1 };
    // k_ab = HMAC-SHA256(temp_key, byte(0x01)).
    HMAC(EVP_sha256(), tempKey, 32, one, 1, m_Kab, &len);
    m_Kab[32] = 2;
    // k_ba = HMAC-SHA256(temp_key, k_ab || byte(0x02))
    HMAC(EVP_sha256(), tempKey, 32, m_Kab, 33, m_Kba, &len);
    static uint8_t ask[4] = { 'a', 's', 'k', 1 }, master[32];
    // ask_master = HMAC-SHA256(temp_key, "ask" || byte(0x01))
    HMAC(EVP_sha256(), tempKey, 32, ask, 4, master, &len);
    uint8_t h[39];
    memcpy (h, m_Establisher->GetH (), 32);
    memcpy (h + 32, "siphash", 7);
    // temp_key = HMAC-SHA256(ask_master, h || "siphash")
    HMAC(EVP_sha256(), master, 32, h, 39, tempKey, &len);
    // sip_master = HMAC-SHA256(temp_key, byte(0x01))
    HMAC(EVP_sha256(), tempKey, 32, one, 1, master, &len);
    // temp_key = HMAC-SHA256(sip_master, zerolen)
    HMAC(EVP_sha256(), master, 32, nullptr, 0, tempKey, &len);
   // sipkeys_ab = HMAC-SHA256(temp_key, byte(0x01)).
    HMAC(EVP_sha256(), tempKey, 32, one, 1, m_Sipkeysab, &len);
    m_Sipkeysab[32] = 2;
     // sipkeys_ba = HMAC-SHA256(temp_key, sipkeys_ab || byte(0x02))
    HMAC(EVP_sha256(), tempKey, 32, m_Sipkeysab, 33, m_Sipkeysba, &len);
}
```
*i2pd (C++) 实现说明："sipkeys" 数组的前16字节是一个 SipHash 密钥，最后8字节是 IV（初始化向量）。SipHash 需要两个 8 字节的密钥，但 i2pd 将它们作为一个 16 字节的密钥来处理。*

## 数据传输

数据以帧传输，每个帧包含3个部分:

- 2 bytes of frame length obfuscated with SipHash
- data encrypted with Chacha20
- 16 bytes of Poly1305 hash value

单个帧中可传输的数据最大长度为 65519 字节。

消息长度通过与当前 SipHash IV（初始化向量）的前两个字节执行 XOR（异或）运算来进行混淆。

加密数据部分包含多个数据块。每个块前面带有一个 3 字节的头部，用于定义块类型和块长度。通常传输的是 I2NP 类型的块，即头部被修改过的 I2NP 消息。一个 NTCP2 帧可以传输多个 I2NP 块。

另一种重要的数据块类型是随机数据块。建议在每个 NTCP2 帧中添加一个随机数据块。只能添加一个随机数据块，并且它必须是最后一个数据块。

以下是在当前 NTCP2 实现中使用的其他数据块：

- **RouterInfo** — usually contains Bob's RouterInfo after the connection has been established, but it can also contain RouterInfo of a random node for the purpose of speeding up floodfills (there is a flags field for that case).
- **Termination** — is used when a host explicitly terminates a connection and specifies a reason for that.
- **DateTime** — a current time in seconds.

## 摘要


新的 I2P 传输协议 NTCP2 能够有效抵御基于深度包检测（DPI）的审查。由于采用了更快的现代加密算法，它还降低了 CPU 负载。这使得 I2P 更容易在低端设备上运行，例如智能手机和家用 router。两大 I2P 实现均已完全支持 NTCP2，并自 0.9.36（Java）和 2.20（i2pd，C++）版本起可使用 NTCP2。
