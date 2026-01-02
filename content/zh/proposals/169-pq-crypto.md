---
title: "后量子密码协议"
number: "169"
author: "zzz, orignal, drzed, eyedeekay"
created: "2025-01-21"
lastupdated: "2025-06-12"
status: "打开"
thread: "http://zzz.i2p/topics/3294"
target: "0.9.80"
toc: true
---

## 概述

虽然对合适的后量子(PQ)密码学的研究和竞争已经进行了十年，但直到最近选择才变得明确。

我们在 2022 年开始研究 PQ 密码学的影响 [zzz.i2p](http://zzz.i2p/topics/3294)。

在过去两年中，TLS 标准增加了混合加密支持，由于 Chrome 和 Firefox 的支持，现在它已被用于互联网上很大一部分的加密流量 [Cloudflare](https://blog.cloudflare.com/pq-2024/)。

美国国家标准与技术研究院（NIST）最近完成并发布了后量子密码学的推荐算法 [NIST](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards)。多个常见的密码学库现已支持NIST标准，或将在不久的将来发布相关支持。

[Cloudflare](https://blog.cloudflare.com/pq-2024/) 和 [NIST](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards) 都建议立即开始迁移。另请参阅2022年NSA后量子常见问题解答 [NSA](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF)。I2P应该在安全和密码学方面成为领导者。现在是实施推荐算法的时候了。使用我们灵活的加密类型和签名类型系统，我们将为混合加密以及后量子和混合签名添加类型。

## 目标

- 选择抗量子算法
- 在适当的 I2P 协议中添加纯量子和混合算法
- 定义多个变体
- 在实施、测试、分析和研究后选择最佳变体
- 增量添加支持并保持向后兼容性

## 非目标

- 不要更改单向（Noise N）加密协议
- 不要放弃 SHA256，它在近期内不会受到 PQ 的威胁
- 目前不要选择最终的首选变体

## 威胁模型

- OBEP 或 IBGW 处的 router，可能串通合作，
  存储 garlic 消息以供后续解密（前向保密）
- 网络观察者
  存储传输消息以供后续解密（前向保密）
- 网络参与者为 RI、LS、流传输、数据报
  或其他结构伪造签名

## 受影响的协议

我们将按照大致的开发顺序修改以下协议。整体推广时间可能从2025年底到2027年中期。详情请参见下面的优先级和推广部分。

| Protocol / Feature | Status |
|--------------------|--------|
| Hybrid MLKEM Ratchet and LS | Approved 2026-06; beta target 2025-08; release target 2025-11 |
| Hybrid MLKEM NTCP2 | Some details to be finalized |
| Hybrid MLKEM SSU2 | Some details to be finalized |
| MLDSA SigTypes 12-14 | Proposal is stable but may not be finalized until 2026 |
| MLDSA Dests | Tested on live net, requires net upgrade for floodfill support |
| Hybrid SigTypes 15-17 | Preliminary |
| Hybrid Dests | |
## 设计

我们将支持 NIST FIPS 203 和 204 标准 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)，这些标准基于 CRYSTALS-Kyber 和 CRYSTALS-Dilithium（版本 3.1、3 及更早版本），但与其不兼容。

### Key Exchange

我们将在以下协议中支持混合密钥交换：

| Proto   | Noise Type | Support PQ only? | Support Hybrid? |
|---------|------------|------------------|-----------------|
| NTCP2   | XK         | no               | yes             |
| SSU2    | XK         | no               | yes             |
| Ratchet | IK         | no               | yes             |
| TBM     | N          | no               | no              |
| NetDB   | N          | no               | no              |
PQ KEM 仅提供临时密钥，不直接支持静态密钥握手，如 Noise XK 和 IK。

Noise N 不使用双向密钥交换，因此不适用于混合加密。

因此，我们将仅支持混合加密，用于 NTCP2、SSU2 和 Ratchet。我们将按照 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) 中的定义来定义三种 ML-KEM 变体，总共新增 3 种加密类型。混合类型仅与 X25519 结合定义。

新的加密类型包括：

| Type | Code |
|------|------|
| MLKEM512_X25519 | 5 |
| MLKEM768_X25519 | 6 |
| MLKEM1024_X25519 | 7 |
开销将会很大。典型的消息 1 和 2 大小（对于 XK 和 IK）目前约为 100 字节（在任何额外载荷之前）。根据算法不同，这将增加 8 到 15 倍。

### Signatures

我们将在以下结构中支持 PQ 和混合签名：

| Type | Support PQ only? | Support Hybrid? |
|------|------------------|-----------------|
| RouterInfo | yes | yes |
| LeaseSet | yes | yes |
| Streaming SYN/SYNACK/Close | yes | yes |
| Repliable Datagrams | yes | yes |
| Datagram2 (prop. 163) | yes | yes |
| I2CP create session msg | yes | yes |
| SU3 files | yes | yes |
| X.509 certificates | yes | yes |
| Java keystores | yes | yes |
因此我们将支持仅PQ和混合签名两种方式。我们将定义三个ML-DSA变体，如[FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)中所述，三个与Ed25519结合的混合变体，以及三个仅用于SU3文件的带预哈希的仅PQ变体，总共9种新的签名类型。混合类型仅与Ed25519结合定义。我们将使用标准ML-DSA，而非预哈希变体(HashML-DSA)，除了SU3文件。

我们将使用"对冲"或随机化签名变体，而不是"确定性"变体，如 [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) 第3.4节所定义。这确保了每个签名都是不同的，即使是对相同数据进行签名，并提供了针对侧信道攻击的额外保护。有关算法选择（包括编码和上下文）的更多详细信息，请参阅下面的实现说明部分。

新的签名类型包括：

| Type | Code |
|------|------|
| MLDSA44 | 12 |
| MLDSA65 | 13 |
| MLDSA87 | 14 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 |
| MLDSA44ph | 18 |
| MLDSA65ph | 19 |
| MLDSA87ph | 20 |
X.509证书和其他DER编码将使用[IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/)中定义的复合结构和OID。

开销将会相当大。典型的 Ed25519 destination 和 router identity 大小为 391 字节。根据算法不同，这些将增加 3.5 倍到 6.8 倍。Ed25519 签名为 64 字节。根据算法不同，这些将增加 38 倍到 76 倍。典型的已签名 RouterInfo、LeaseSet、可回复数据报和已签名流消息约为 1KB。根据算法不同，这些将增加 3 倍到 8 倍。

由于新的目标地址和 router 身份类型将不包含填充，它们将不可压缩。在传输过程中经过 gzip 压缩的目标地址和 router 身份的大小将根据算法增加 12 倍至 38 倍。

### Legal Combinations

对于 Destinations，新的签名类型支持 leaseset 中的所有加密类型。将密钥证书中的加密类型设置为 NONE (255)。

对于 RouterIdentities，ElGamal 加密类型已被弃用。新的签名类型仅支持 X25519（类型 4）加密。新的加密类型将在 RouterAddresses 中标明。密钥证书中的加密类型将继续为类型 4。

### New Crypto Required

- ML-KEM（原名 CRYSTALS-Kyber）[FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
- ML-DSA（原名 CRYSTALS-Dilithium）[FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)
- SHA3-128（原名 Keccak-256）[FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf) 仅用于 SHAKE128
- SHA3-256（原名 Keccak-512）[FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
- SHAKE128 和 SHAKE256（SHA3-128 和 SHA3-256 的 XOF 扩展）[FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)

SHA3-256、SHAKE128 和 SHAKE256 的测试向量可在 [NIST](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values) 找到。

请注意，Java bouncycastle库支持以上所有功能。C++库支持已包含在OpenSSL 3.5中[OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)。

### Alternatives

我们不会支持 [FIPS 205](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.205.pdf) (Sphincs+)，它比 ML-DSA 慢得多且体积大得多。我们不会支持即将推出的 FIPS206 (Falcon)，它尚未标准化。我们不会支持 NTRU 或其他未被 NIST 标准化的 PQ 候选方案。

### Rosenpass

有一些研究 [paper](https://eprint.iacr.org/2020/379.pdf) 关于将 Wireguard (IK) 适配为纯后量子密码学，但该论文中存在几个开放性问题。后来，这种方法被实现为 Rosenpass [Rosenpass](https://rosenpass.eu/) [whitepaper](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf)，用于后量子 Wireguard。

Rosenpass 使用类似 Noise KK 的握手，配合预共享的 Classic McEliece 460896 静态密钥（每个 500 KB）和 Kyber-512（本质上是 MLKEM-512）临时密钥。由于 Classic McEliece 密文只有 188 字节，而 Kyber-512 公钥和密文大小合理，两个握手消息都能适合标准 UDP MTU。PQ KK 握手输出的共享密钥（osk）被用作标准 Wireguard IK 握手的输入预共享密钥（psk）。因此总共有两个完整的握手过程，一个是纯 PQ 的，一个是纯 X25519 的。

我们无法用这些方法来替换我们的XK和IK握手，因为：

- 我们无法进行 KK，Bob 没有 Alice 的静态密钥
- 500KB 的静态密钥太大了
- 我们不希望有额外的往返通信

白皮书中包含了很多有价值的信息，我们会审阅它以获取想法和灵感。待办事项。

## Specification

### 密钥交换

按照以下方式更新通用结构文档 [/docs/specs/common-structures/](/docs/specs/common-structures/) 中的章节和表格：

### 签名

新的公钥类型包括：

| Type | Public Key Length | Since | Usage |
|------|-------------------|-------|-------|
| MLKEM512_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM768_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM1024_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM512 | 800 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM768 | 1184 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM1024 | 1568 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM512_CT | 768 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM768_CT | 1088 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM1024_CT | 1568 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| NONE | 0 | 0.9.xx | See proposal 169, for destinations with PQ sig types only, not for RIs or Leasesets |
混合公钥是 X25519 密钥。KEM 公钥是从 Alice 发送到 Bob 的临时 PQ 密钥。编码和字节序在 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) 中定义。

MLKEM*_CT 密钥实际上并不是公钥，它们是在 Noise 握手过程中从 Bob 发送给 Alice 的"密文"。这里列出它们是为了完整性。

### 合法组合

新的私钥类型包括：

| Type | Private Key Length | Since | Usage |
|------|---------------------|-------|-------|
| MLKEM512_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM768_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM1024_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM512 | 1632 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM768 | 2400 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM1024 | 3168 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
混合私钥是 X25519 密钥。KEM 私钥仅供 Alice 使用。KEM 编码和字节序在 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) 中定义。

### 需要新的加密算法

新的签名公钥类型包括：

| Type | Length (bytes) | Since | Usage |
|------|----------------|-------|-------|
| MLDSA44 | 1312 | 0.9.xx | See proposal 169 |
| MLDSA65 | 1952 | 0.9.xx | See proposal 169 |
| MLDSA87 | 2592 | 0.9.xx | See proposal 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 1344 | 0.9.xx | See proposal 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 1984 | 0.9.xx | See proposal 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 2624 | 0.9.xx | See proposal 169 |
| MLDSA44ph | 1344 | 0.9.xx | Only for SU3 files, not for netdb structures |
| MLDSA65ph | 1984 | 0.9.xx | Only for SU3 files, not for netdb structures |
| MLDSA87ph | 2624 | 0.9.xx | Only for SU3 files, not for netdb structures |
混合签名公钥是 Ed25519 密钥后跟 PQ 密钥，如 [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/) 中所述。编码和字节顺序在 [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) 中定义。

### 替代方案

新的签名私钥类型包括：

| Type | Length (bytes) | Since | Usage |
|------|----------------|-------|-------|
| MLDSA44 | 2560 | 0.9.xx | See proposal 169 |
| MLDSA65 | 4032 | 0.9.xx | See proposal 169 |
| MLDSA87 | 4896 | 0.9.xx | See proposal 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2592 | 0.9.xx | See proposal 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 4064 | 0.9.xx | See proposal 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4928 | 0.9.xx | See proposal 169 |
| MLDSA44ph | 2592 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
| MLDSA65ph | 4064 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
| MLDSA87ph | 4928 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
混合签名私钥是 Ed25519 密钥后跟 PQ 密钥，如 [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/) 所述。编码和字节序在 [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) 中定义。

### Rosenpass

新的签名类型包括：

| Type | Length (bytes) | Since | Usage |
|------|----------------|-------|-------|
| MLDSA44 | 2420 | 0.9.xx | See proposal 169 |
| MLDSA65 | 3309 | 0.9.xx | See proposal 169 |
| MLDSA87 | 4627 | 0.9.xx | See proposal 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2484 | 0.9.xx | See proposal 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 3373 | 0.9.xx | See proposal 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4691 | 0.9.xx | See proposal 169 |
| MLDSA44ph | 2484 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
| MLDSA65ph | 3373 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
| MLDSA87ph | 4691 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
混合签名是 Ed25519 签名后跟 PQ 签名，如 [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/) 中所述。混合签名通过验证两个签名来进行验证，如果其中任何一个失败则验证失败。编码和字节顺序在 [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) 中定义。

### Key Certificates

新的签名公钥类型包括：

| Type | Type Code | Total Public Key Length | Since | Usage |
|------|-----------|-------------------------|-------|-------|
| MLDSA44 | 12 | 1312 | 0.9.xx | See proposal 169 |
| MLDSA65 | 13 | 1952 | 0.9.xx | See proposal 169 |
| MLDSA87 | 14 | 2592 | 0.9.xx | See proposal 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 0.9.xx | See proposal 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 0.9.xx | See proposal 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 0.9.xx | See proposal 169 |
| MLDSA44ph | 18 | n/a | 0.9.xx | Only for SU3 files |
| MLDSA65ph | 19 | n/a | 0.9.xx | Only for SU3 files |
| MLDSA87ph | 20 | n/a | 0.9.xx | Only for SU3 files |
新的加密公钥类型包括：

| Type | Type Code | Total Public Key Length | Since | Usage |
|------|-----------|-------------------------|-------|-------|
| MLKEM512_X25519 | 5 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM768_X25519 | 6 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM1024_X25519 | 7 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| NONE | 255 | 0 | 0.9.xx | See proposal 169 |
混合密钥类型绝不包含在密钥证书中；仅包含在 leaseSet 中。

对于具有 Hybrid 或 PQ 签名类型的目标，加密类型使用 NONE（类型 255），但没有加密密钥，整个 384 字节的主要部分都用于签名密钥。

### 通用结构

以下是新 Destination 类型的长度。所有类型的加密类型都是 NONE（类型 255），加密密钥长度被视为 0。整个 384 字节部分用于签名公钥的第一部分。注意：这与 ECDSA_SHA512_P521 和 RSA 签名类型的规范不同，在那些类型中我们在 destination 中保留了 256 字节的 ElGamal 密钥，即使它未被使用。

无填充。总长度为 7 + 总密钥长度。密钥证书长度为 4 + 超额密钥长度。

MLDSA44 的示例 1319 字节目标字节流：

skey[0:383] 5 (932 >> 8) (932 & 0xff) 00 12 00 255 skey[384:1311]

| Type | Type Code | Total Public Key Length | Main | Excess | Total Dest Length |
|------|-----------|-------------------------|------|--------|-------------------|
| MLDSA44 | 12 | 1312 | 384 | 928 | 1319 |
| MLDSA65 | 13 | 1952 | 384 | 1568 | 1959 |
| MLDSA87 | 14 | 2592 | 384 | 2208 | 2599 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 384 | 960 | 1351 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 384 | 1600 | 1991 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 384 | 2240 | 2631 |
### PublicKey

以下是新 Destination 类型的长度。所有类型的加密类型都是 X25519（类型 4）。X28819 公钥后的整个 352 字节部分用于签名公钥的第一部分。无填充。总长度为 39 + 总密钥长度。密钥证书长度为 4 + 多余密钥长度。

MLDSA44 的 1351 字节 router identity 字节流示例：

enckey[0:31] skey[0:351] 5 (960 >> 8) (960 & 0xff) 00 12 00 4 skey[352:1311]

| Type | Type Code | Total Public Key Length | Main | Excess | Total RouterIdent Length |
|------|-----------|-------------------------|------|--------|--------------------------|
| MLDSA44 | 12 | 1312 | 352 | 960 | 1351 |
| MLDSA65 | 13 | 1952 | 352 | 1600 | 1991 |
| MLDSA87 | 14 | 2592 | 352 | 2240 | 2631 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 352 | 992 | 1383 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 352 | 1632 | 2023 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 352 | 2272 | 2663 |
### 私钥

握手使用 [Noise Protocol](https://noiseprotocol.org/noise.html) 握手模式。

使用以下字母映射：

- e = 一次性临时密钥
- s = 静态密钥
- p = 消息载荷
- e1 = 一次性临时 PQ 密钥，从 Alice 发送到 Bob
- ekem1 = KEM 密文，从 Bob 发送到 Alice

针对混合前向保密 (hfs) 对 XK 和 IK 的以下修改如 [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) 第 5 节所述：

```
XK:                       XKhfs:
  <- s                      <- s
  ...                       ...
  -> e, es, p               -> e, es, e1, p
  <- e, ee, p               <- e, ee, ekem1, p
  -> s, se                  -> s, se
  <- p                      <- p
  p ->                      p ->


  IK:                       IKhfs:
  <- s                      <- s
  ...                       ...
  -> e, es, s, ss, p       -> e, es, e1, s, ss, p
  <- tag, e, ee, se, p     <- tag, e, ee, ekem1, se, p
  <- p                     <- p
  p ->                     p ->

  e1 and ekem1 are encrypted. See pattern definitions below.
  NOTE: e1 and ekem1 are different sizes (unlike X25519)
```
e1 模式定义如下，如 [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) 第 4 节所述：

```
For Alice:
  (encap_key, decap_key) = PQ_KEYGEN()

  // EncryptAndHash(encap_key)
  ciphertext = ENCRYPT(k, n, encap_key, ad)
  n++
  MixHash(ciphertext)

  For Bob:

  // DecryptAndHash(ciphertext)
  encap_key = DECRYPT(k, n, ciphertext, ad)
  n++
  MixHash(ciphertext)
```
ekem1 模式定义如下，具体规范见 [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) 第 4 节：

```
For Bob:

  (kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

  // EncryptAndHash(kem_ciphertext)
  ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)
  MixHash(ciphertext)

  // MixKey
  MixKey(kem_shared_key)


  For Alice:

  // DecryptAndHash(ciphertext)
  kem_ciphertext = DECRYPT(k, n, ciphertext, ad)
  MixHash(ciphertext)

  // MixKey
  kem_shared_key = DECAPS(kem_ciphertext, decap_key)
  MixKey(kem_shared_key)
```
### SigningPublicKey

#### Issues

- 我们是否应该更改握手哈希函数？参见 [comparison](https://kerkour.com/fast-secure-hash-function-sha256-sha512-sha3-blake3)。
  SHA256 对后量子攻击并不脆弱，但如果我们确实想升级
  哈希函数，现在是时候了，趁着我们正在更改其他东西。
  当前的 IETF SSH 提案 [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-sshm-mlkem-hybrid-kex/) 是使用 MLKEM768
  配合 SHA256，以及 MLKEM1024 配合 SHA384。该提案包含
  安全考虑的讨论。
- 我们是否应该停止发送 0-RTT ratchet 数据（除了 leaseSet）？
- 如果我们不发送 0-RTT 数据，是否应该将 ratchet 从 IK 切换到 XK？

#### Overview

本节适用于 IK 和 XK 协议。

混合握手在 [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) 中定义。第一条消息从 Alice 发送到 Bob，在消息载荷之前包含 e1（封装密钥）。这被视为额外的静态密钥；对其调用 EncryptAndHash()（作为 Alice）或 DecryptAndHash()（作为 Bob）。然后按常规方式处理消息载荷。

第二条消息，从 Bob 到 Alice，在消息载荷之前包含 ekem1 和密文。这被视为一个额外的静态密钥；对其调用 EncryptAndHash()（作为 Bob）或 DecryptAndHash()（作为 Alice）。然后，计算 kem_shared_key 并调用 MixKey(kem_shared_key)。接着按常规方式处理消息载荷。

#### Defined ML-KEM Operations

我们定义以下函数，对应于 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) 中定义的密码学构建块。

(encap_key, decap_key) = PQ_KEYGEN()

    Alice creates the encapsulation and decapsulation keys
    The encapsulation key is sent in message 1.
    encap_key and decap_key sizes vary based on ML-KEM variant.

(ciphertext, kem_shared_key) = ENCAPS(encap_key)

    Bob calculates the ciphertext and shared key,
    using the ciphertext received in message 1.
    The ciphertext is sent in message 2.
    ciphertext size varies based on ML-KEM variant.
    The kem_shared_key is always 32 bytes.

kem_shared_key = DECAPS(ciphertext, decap_key)

    Alice calculates the shared key,
    using the ciphertext received in message 2.
    The kem_shared_key is always 32 bytes.

注意，encap_key 和 ciphertext 都在 Noise 握手消息 1 和 2 的 ChaCha/Poly 块内进行了加密。它们将作为握手过程的一部分被解密。

kem_shared_key 通过 MixHash() 混合到链式密钥中。详细信息请参见下文。

#### Alice KDF for Message 1

对于 XK：在 'es' 消息模式之后和载荷之前，添加：

或者

对于 IK：在 'es' 消息模式之后和 's' 消息模式之前，添加：

```
This is the "e1" message pattern:
  (encap_key, decap_key) = PQ_KEYGEN()

  // EncryptAndHash(encap_key)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, encap_key, ad)
  n++

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)


  End of "e1" message pattern.

  NOTE: For the next section (payload for XK or static key for IK),
  the keydata and chain key remain the same,
  and n now equals 1 (instead of 0 for non-hybrid).
```
#### Bob KDF for Message 1

对于 XK：在 'es' 消息模式之后、载荷之前，添加：

或者

对于 IK：在 'es' 消息模式之后和 's' 消息模式之前，添加：

```
This is the "e1" message pattern:

  // DecryptAndHash(encap_key_section)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  encap_key = DECRYPT(k, n, encap_key_section, ad)
  n++

  // MixHash(encap_key_section)
  h = SHA256(h || encap_key_section)

  End of "e1" message pattern.

  NOTE: For the next section (payload for XK or static key for IK),
  the keydata and chain key remain the same,
  and n now equals 1 (instead of 0 for non-hybrid).
```
#### Bob KDF for Message 2

对于 XK：在 'ee' 消息模式之后和载荷之前，添加：

或者

对于 IK：在 'ee' 消息模式之后和 'se' 消息模式之前，添加：

```
This is the "ekem1" message pattern:

  (kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

  // EncryptAndHash(kem_ciphertext)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)

  // MixKey(kem_shared_key)
  keydata = HKDF(chainKey, kem_shared_key, "", 64)
  chainKey = keydata[0:31]

  End of "ekem1" message pattern.
```
#### Alice KDF for Message 2

在 'ee' 消息模式之后（对于 IK，在 'ss' 消息模式之前），添加：

```
This is the "ekem1" message pattern:

  // DecryptAndHash(kem_ciphertext_section)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  kem_ciphertext = DECRYPT(k, n, kem_ciphertext_section, ad)

  // MixHash(kem_ciphertext_section)
  h = SHA256(h || kem_ciphertext_section)

  // MixKey(kem_shared_key)
  kem_shared_key = DECAPS(kem_ciphertext, decap_key)
  keydata = HKDF(chainKey, kem_shared_key, "", 64)
  chainKey = keydata[0:31]

  End of "ekem1" message pattern.
```
#### KDF for Message 3 (XK only)

未更改

#### KDF for split()

未更改

### SigningPrivateKey（签名私钥）

按以下方式更新ECIES-Ratchet规范 [/docs/specs/ecies/](/docs/specs/ecies/)：

#### Noise identifiers

- "Noise_IKhfselg2_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM1024_ChaChaPoly_SHA256"

#### 1b) New session format (with binding)

变更：当前的 ratchet 在第一个 ChaCha 部分包含静态密钥，在第二部分包含有效载荷。使用 ML-KEM 后，现在有三个部分。第一部分包含加密的 PQ 公钥。第二部分包含静态密钥。第三部分包含有效载荷。

加密格式：

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
  +           ML-KEM encap_key            +
  |       ChaCha20 encrypted data         |
  +      (see table below for length)     +
  |                                       |
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +    (MAC) for encap_key Section        +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +           X25519 Static Key           +
  |       ChaCha20 encrypted data         |
  +             32 bytes                  +
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
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) for Payload Section     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
```
解密格式：

```
Payload Part 1:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +       ML-KEM encap_key                +
  |                                       |
  +      (see table below for length)     +
  |                                       |
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Payload Part 2:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +       X25519 Static Key               +
  |                                       |
  +      (32 bytes)                       +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+

  Payload Part 3:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |                                       |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
```
大小：

| Type | Type Code | X len | Msg 1 len | Msg 1 Enc len | Msg 1 Dec len | PQ key len | pl len |
|------|-----------|-------|-----------|---------------|---------------|------------|--------|
| X25519 | 4 | 32 | 96+pl | 64+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 912+pl | 880+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1296+pl | 1360+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1680+pl | 1648+pl | 1568+pl | 1568 | pl |
请注意，负载必须包含一个 DateTime 块，因此最小负载大小为 7。可以据此计算最小消息 1 大小。

#### 1g) New Session Reply format

变更：当前的 ratchet 在第一个 ChaCha 部分有空载荷，载荷在第二部分中。使用 ML-KEM 时，现在有三个部分。第一部分包含加密的 PQ 密文。第二部分有空载荷。第三部分包含载荷。

加密格式：

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
  |                                       |
  +                                       +
  | ChaCha20 encrypted ML-KEM ciphertext  |
  +      (see table below for length)     +
  ~                                       ~
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +  (MAC) for ciphertext Section         +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +  (MAC) for key Section (no data)      +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |       ChaCha20 encrypted data         |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) for Payload Section     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
```
解密格式：

```
Payload Part 1:


  +----+----+----+----+----+----+----+----+
  |                                       |
  +       ML-KEM ciphertext               +
  |                                       |
  +      (see table below for length)     +
  |                                       |
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Payload Part 2:

  empty

  Payload Part 3:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |                                       |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
```
大小：

| Type | Type Code | Y len | Msg 2 len | Msg 2 Enc len | Msg 2 Dec len | PQ CT len | opt len |
|------|-----------|-------|-----------|---------------|---------------|-----------|---------|
| X25519 | 4 | 32 | 72+pl | 32+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 856+pl | 816+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1176+pl | 1136+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1656+pl | 1616+pl | 1568+pl | 1568 | pl |
请注意，虽然消息2通常会有非零载荷，但ratchet规范[/docs/specs/ecies/](/docs/specs/ecies/)并不要求如此，因此最小载荷大小为0。可以相应地计算消息2的最小大小。

### 签名

按如下方式更新 NTCP2 规范 [/docs/specs/ntcp2/](/docs/specs/ntcp2/)：

#### Noise identifiers

- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM1024_ChaChaPoly_SHA256"

#### 1) SessionRequest

变更：当前的 NTCP2 仅包含 ChaCha 部分中的选项。使用 ML-KEM 后，ChaCha 部分还将包含加密的 PQ 公钥。

原始内容：

```
+----+----+----+----+----+----+----+----+
  |                                       |
  +        obfuscated with RH_B           +
  |       AES-CBC-256 encrypted X         |
  +             (32 bytes)                +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaChaPoly frame (MLKEM)            |
  +      (see table below for length)     +
  |   k defined in KDF for message 1      |
  +   n = 0                               +
  |   see KDF for associated data         |
  ~   n = 0                               ~
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaChaPoly frame (options)          |
  +         32 bytes                      +
  |   k defined in KDF for message 1      |
  +   n = 0                               +
  |   see KDF for associated data         |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  ~         padding (optional)            ~
  |     length defined in options block   |
  +----+----+----+----+----+----+----+----+

  Same as before except add a second ChaChaPoly frame
```
未加密数据（未显示 Poly1305 认证标签）：

```
+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                   X                   |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM encap_key            |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |               options                 |
  +              (16 bytes)               +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  +         padding (optional)            +
  |     length defined in options block   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+
```
大小：

| Type | Type Code | X len | Msg 1 len | Msg 1 Enc len | Msg 1 Dec len | PQ key len | opt len |
|------|-----------|-------|-----------|---------------|---------------|------------|---------|
| X25519 | 4 | 32 | 64+pad | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 880+pad | 848 | 816 | 800 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1264+pad | 1232 | 1200 | 1184 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1648+pad | 1616 | 1584 | 1568 | 16 |
注意：类型代码仅供内部使用。Router 将保持类型 4，支持情况将在 router 地址中指示。

#### 2) SessionCreated

变更：当前的 NTCP2 只包含 ChaCha 部分中的选项。使用 ML-KEM 后，ChaCha 部分还将包含加密的 PQ 公钥。

原始内容：

```
+----+----+----+----+----+----+----+----+
  |                                       |
  +        obfuscated with RH_B           +
  |       AES-CBC-256 encrypted Y         |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaChaPoly frame (MLKEM)            |
  +   Encrypted and authenticated data    +
  -      (see table below for length)     -
  +   k defined in KDF for message 2      +
  |   n = 0; see KDF for associated data  |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaChaPoly frame (options)          |
  +   Encrypted and authenticated data    +
  -           32 bytes                    -
  +   k defined in KDF for message 2      +
  |   n = 0; see KDF for associated data  |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  +         padding (optional)            +
  |     length defined in options block   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Same as before except add a second ChaChaPoly frame
```
未加密数据（未显示 Poly1305 认证标签）：

```
+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                  Y                    |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM Ciphertext           |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |               options                 |
  +              (16 bytes)               +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  +         padding (optional)            +
  |     length defined in options block   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+
```
大小：

| Type | Type Code | Y len | Msg 2 len | Msg 2 Enc len | Msg 2 Dec len | PQ CT len | opt len |
|------|-----------|-------|-----------|---------------|---------------|-----------|---------|
| X25519 | 4 | 32 | 64+pad | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 848+pad | 816 | 784 | 768 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1136+pad | 1104 | 1104 | 1088 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1616+pad | 1584 | 1584 | 1568 | 16 |
注意：类型代码仅供内部使用。Router 将保持类型 4，支持情况将在 router 地址中指示。

#### 3) SessionConfirmed

未更改

#### Key Derivation Function (KDF) (for data phase)

未改变

### 密钥证书

按以下方式更新 SSU2 规范 [/docs/specs/ssu2/](/docs/specs/ssu2/)：

#### Noise identifiers

- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM1024_ChaChaPoly_SHA256"

#### Long Header

长头部为32字节。它在会话创建之前使用，用于Token请求、SessionRequest、SessionCreated和重试。它也用于会话外的Peer Test和Hole Punch消息。

TODO：我们可以在内部使用版本字段，对MLKEM512使用3，对MLKEM768使用4。我们是仅对类型0和1这样做，还是对所有6种类型都这样做？

头部加密之前：

```

+----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+

  Destination Connection ID :: 8 bytes, unsigned big endian integer

  Packet Number :: 4 bytes, unsigned big endian integer

  type :: The message type = 0, 1, 7, 9, 10, or 11

  ver :: The protocol version, equal to 2
         TODO We could internally use the version field and use 3 for MLKEM512 and 4 for MLKEM768.

  id :: 1 byte, the network ID (currently 2, except for test networks)

  flag :: 1 byte, unused, set to 0 for future compatibility

  Source Connection ID :: 8 bytes, unsigned big endian integer

  Token :: 8 bytes, unsigned big endian integer

```
#### Short Header

未更改

#### SessionRequest (Type 0)

变更：当前的 SSU2 在 ChaCha 部分仅包含块数据。使用 ML-KEM 后，ChaCha 部分还将包含加密的 PQ 公钥。

原始内容：

```
+----+----+----+----+----+----+----+----+
  |  Long Header bytes 0-15, ChaCha20     |
  +  encrypted with Bob intro key         +
  |    See Header Encryption KDF          |
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 16-31, ChaCha20    |
  +  encrypted with Bob intro key n=0     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +       X, ChaCha20 encrypted           +
  |       with Bob intro key n=0          |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (MLKEM)     |
  +          (length varies)              +
  |  k defined in KDF for Session Request |
  +  n = 0                                +
  |  see KDF for associated data          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (payload)   |
  +          (length varies)              +
  |  k defined in KDF for Session Request |
  +  n = 0                                +
  |  see KDF for associated data          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
未加密数据（未显示 Poly1305 身份验证标签）：

```
+----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                   X                   |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM encap_key            |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     Noise payload (block data)        |
  +          (length varies)              +
  |     see below for allowed blocks      |
  +----+----+----+----+----+----+----+----+
```
大小，不包括 IP 开销：

| Type | Type Code | X len | Msg 1 len | Msg 1 Enc len | Msg 1 Dec len | PQ key len | pl len |
|------|-----------|-------|-----------|---------------|---------------|------------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 896+pl | 832+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1280+pl | 1216+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | n/a | too big | | | | |
注意：类型代码仅供内部使用。Router 将保持类型 4，支持将在 router 地址中指示。

MLKEM768_X25519的最小MTU：IPv4约为1316，IPv6约为1336。

#### SessionCreated (Type 1)

变更：当前的 SSU2 在 ChaCha 部分只包含块数据。使用 ML-KEM 后，ChaCha 部分还将包含加密的 PQ 公钥。

原始内容：

```
+----+----+----+----+----+----+----+----+
  |  Long Header bytes 0-15, ChaCha20     |
  +  encrypted with Bob intro key and     +
  | derived key, see Header Encryption KDF|
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 16-31, ChaCha20    |
  +  encrypted with derived key n=0       +
  |  See Header Encryption KDF            |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +       Y, ChaCha20 encrypted           +
  |       with derived key n=0            |
  +              (32 bytes)               +
  |       See Header Encryption KDF       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 data (MLKEM)               |
  +   Encrypted and authenticated data    +
  |  length varies                        |
  +  k defined in KDF for Session Created +
  |  n = 0; see KDF for associated data   |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 data (payload)             |
  +   Encrypted and authenticated data    +
  |  length varies                        |
  +  k defined in KDF for Session Created +
  |  n = 0; see KDF for associated data   |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
未加密数据（未显示 Poly1305 认证标签）：

```
+----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                  Y                    |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM Ciphertext           |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     Noise payload (block data)        |
  +          (length varies)              +
  |      see below for allowed blocks     |
  +----+----+----+----+----+----+----+----+
```
大小，不包括 IP 开销：

| Type | Type Code | Y len | Msg 2 len | Msg 2 Enc len | Msg 2 Dec len | PQ CT len | pl len |
|------|-----------|-------|-----------|---------------|---------------|-----------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 864+pl | 800+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1184+pl | 1118+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | n/a | too big | | | | |
注意：类型代码仅供内部使用。Router将保持类型4，支持情况将在router地址中显示。

MLKEM768_X25519 的最小 MTU：IPv4 约为 1316，IPv6 约为 1336。

#### SessionConfirmed (Type 2)

未更改

#### KDF for data phase

未更改

#### 问题

Relay 块、Peer Test 块和 Peer Test 消息都包含签名。不幸的是，PQ 签名比 MTU 更大。目前没有机制可以将 Relay 或 Peer Test 块或消息分片到多个 UDP 数据包中。必须扩展协议以支持分片。这将在单独的待定提案中完成。在此之前，将不支持 Relay 和 Peer Test。

#### 概述

我们可以在内部使用版本字段，对 MLKEM512 使用 3，对 MLKEM768 使用 4。

对于消息 1 和 2，MLKEM768 会使数据包大小超过 1280 字节的最小 MTU。如果 MTU 过低，可能就不支持该连接。

对于消息 1 和 2，MLKEM1024 会使数据包大小超出 1500 的最大 MTU。这将需要对消息 1 和 2 进行分片，这会是一个很大的复杂化问题。可能不会这样做。

中继和对等测试：见上文

### 目标地址大小

TODO: 是否有更高效的方式来定义签名/验证以避免复制签名？

### RouterIdent 大小

待办事项

[IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/) 第 8.1 节不允许在 X.509 证书中使用 HashML-DSA，并且不为 HashML-DSA 分配 OID，这是由于实现复杂性和安全性降低的原因。

对于 SU3 文件的 PQ-only 签名，使用证书中定义在 [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/) 的非预哈希变体的 OID。我们不定义 SU3 文件的混合签名，因为我们可能需要对文件进行两次哈希（尽管 HashML-DSA 和 X2559 使用相同的哈希函数 SHA512）。此外，在 X.509 证书中连接两个密钥和签名将是完全非标准的。

请注意，我们不允许对 SU3 文件进行 Ed25519 签名，虽然我们已经定义了 Ed25519ph 签名，但我们从未就其 OID 达成一致，也从未使用过它。

普通的签名类型不允许用于 SU3 文件；请使用 ph（预哈希）变体。

### 握手模式

新的最大 Destination 大小将是 2599（base 64 格式为 3468）。

更新其他提供Destination大小指导的文档，包括：

- SAMv3
- Bittorrent
- 开发者指南
- 命名 / 地址簿 / 跳转服务器
- 其他文档

## Overhead Analysis

### Noise 握手密钥派生函数

大小增加（字节）：

| Type | Pubkey (Msg 1) | Cipertext (Msg 2) |
|------|----------------|-------------------|
| MLKEM512_X25519 | +816 | +784 |
| MLKEM768_X25519 | +1200 | +1104 |
| MLKEM1024_X25519 | +1584 | +1584 |
速度：

根据 [Cloudflare](https://blog.cloudflare.com/pq-2024/) 报告的速度：

| Type | Relative speed |
|------|----------------|
| X25519 DH/keygen | baseline |
| MLKEM512 | 2.25x faster |
| MLKEM768 | 1.5x faster |
| MLKEM1024 | 1x (same) |
| XK | 4x DH (keygen + 3 DH) |
| MLKEM512_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 4.9x DH = 22% slower |
| MLKEM768_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 5.3x DH = 32% slower |
| MLKEM1024_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 6x DH = 50% slower |
Java 中的初步测试结果：

| Type | Relative DH/encaps | DH/decaps | keygen |
|------|-------------------|-----------|--------|
| X25519 | baseline | baseline | baseline |
| MLKEM512 | 29x faster | 22x faster | 17x faster |
| MLKEM768 | 17x faster | 14x faster | 9x faster |
| MLKEM1024 | 12x faster | 10x faster | 6x faster |
### Signatures

大小：

假设 RIs 使用 X25519 加密类型的典型密钥、签名、RIdent、Dest 大小或大小增加（包含 Ed25519 作为参考）。列出的 Router Info、LeaseSet、可回复数据报以及两个流传输（SYN 和 SYN ACK）数据包的增加大小。当前的 Destinations 和 Leasesets 包含重复填充，在传输过程中可以压缩。新类型不包含填充且无法压缩，导致传输中的大小增加幅度更大。请参见上面的设计部分。

| Type | Pubkey | Sig | Key+Sig | RIdent | Dest | RInfo | LS/Streaming/Datagram (each msg) |
|------|--------|-----|---------|--------|------|-------|----------------------------------|
| EdDSA_SHA512_Ed25519 | 32 | 64 | 96 | 391 | 391 | baseline | baseline |
| MLDSA44 | 1312 | 2420 | 3732 | 1351 | 1319 | +3316 | +3284 |
| MLDSA65 | 1952 | 3309 | 5261 | 1991 | 1959 | +5668 | +5636 |
| MLDSA87 | 2592 | 4627 | 7219 | 2631 | 2599 | +7072 | +7040 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 1344 | 2484 | 3828 | 1383 | 1351 | +3412 | +3380 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 1984 | 3373 | 5357 | 2023 | 1991 | +5668 | +5636 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 2624 | 4691 | 7315 | 2663 | 2631 | +7488 | +7456 |
速度：

据 [Cloudflare](https://blog.cloudflare.com/pq-2024/) 报告的速度：

| Type | Relative speed sign | verify |
|------|---------------------|--------|
| EdDSA_SHA512_Ed25519 | baseline | baseline |
| MLDSA44 | 5x slower | 2x faster |
| MLDSA65 | ??? | ??? |
| MLDSA87 | ??? | ??? |
Java 初步测试结果：

| Type | Relative speed sign | verify | keygen |
|------|---------------------|--------|--------|
| EdDSA_SHA512_Ed25519 | baseline | baseline | baseline |
| MLDSA44 | 4.6x slower | 1.7x faster | 2.6x faster |
| MLDSA65 | 8.1x slower | same | 1.5x faster |
| MLDSA87 | 11.1x slower | 1.5x slower | same |
## Security Analysis

NIST 安全类别在 [NIST presentation](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf) 第 10 页幻灯片中有总结。初步标准：对于混合协议，我们的最低 NIST 安全类别应为 2 级，对于纯 PQ 协议应为 3 级。

| Category | As Secure As |
|----------|--------------|
| 1 | AES128 |
| 2 | SHA256 |
| 3 | AES192 |
| 4 | SHA384 |
| 5 | AES256 |
### Handshakes

这些都是混合协议。可能需要优先选择 MLKEM768；MLKEM512 的安全性不够。

NIST 安全类别 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf):

| Algorithm | Security Category |
|-----------|-------------------|
| MLKEM512 | 1 |
| MLKEM768 | 3 |
| MLKEM1024 | 5 |
### Signatures

该提案定义了混合和仅 PQ 的签名类型。MLDSA44 混合类型比 MLDSA65 仅 PQ 类型更可取。MLDSA65 和 MLDSA87 的密钥和签名大小对我们来说可能太大了，至少在最初阶段是如此。

NIST 安全类别 [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)：

| Algorithm | Security Category |
|-----------|-------------------|
| MLDSA44 | 2 |
| MLKEM67 | 3 |
| MLKEM87 | 5 |
## Type Preferences

虽然我们将定义并实现3种加密和9种签名类型，但我们计划在开发过程中测量性能，并进一步分析增加的结构大小所带来的影响。我们还将继续研究和监测其他项目和协议的发展情况。

经过一年或更长时间的开发后，我们将尝试为每个使用场景确定首选类型或默认设置。选择时需要在带宽、CPU和预估安全级别之间进行权衡。并非所有类型都适用或允许用于所有使用场景。

初步偏好设置如下，可能会有变更：

加密：MLKEM768_X25519

签名：MLDSA44_EdDSA_SHA512_Ed25519

初步限制如下，可能会有变更：

加密：SSU2 不允许使用 MLKEM1024_X25519

签名：MLDSA87和混合变体可能过大；MLDSA65和混合变体可能过大

## Implementation Notes

### Library Support

Bouncycastle、BoringSSL 和 WolfSSL 库现在支持 MLKEM 和 MLDSA。OpenSSL 支持将在 2025 年 4 月 8 日的 3.5 版本中提供 [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)。

Java I2P 所采用的 southernstorm.com Noise 库包含了对混合握手的初步支持，但我们将其作为未使用功能删除了；我们将需要重新添加并更新它以匹配 [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf)。

### Signing Variants

我们将使用"对冲"或随机化签名变体，而不是"确定性"变体，如 [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) 第3.4节所定义。这确保了每个签名都是不同的，即使对相同数据进行签名，并提供针对侧信道攻击的额外保护。虽然 [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) 规定"对冲"变体是默认值，但在各种库中这可能是也可能不是真实情况。实现者必须确保使用"对冲"变体进行签名。

我们使用标准签名过程（称为 Pure ML-DSA Signature Generation），该过程内部将消息编码为 0x00 || len(ctx) || ctx || message，其中 ctx 是一些大小为 0x00..0xFF 的可选值。我们没有使用任何可选上下文。len(ctx) == 0。此过程在 [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) 算法 2 第 10 步和算法 3 第 5 步中定义。注意，某些已发布的测试向量可能需要设置一种模式，其中消息不被编码。

### Reliability

大小增加将导致 NetDB 存储、流式握手和其他消息的隧道分片大幅增加。请检查性能和可靠性变化。

### Structure Sizes

查找并检查任何限制 router info 和 leaseSet 字节大小的代码。

### NetDB

检查并可能减少存储在RAM或磁盘上的最大LS/RI数量，以限制存储增长。提高floodfill的最低带宽要求？

### Ratchet

#### 已定义的 ML-KEM 操作

基于对消息1（新会话消息）的长度检查，应该可以在同一tunnel上自动分类/检测多种协议。以MLKEM512_X25519为例，消息1的长度比当前ratchet协议大816字节，最小消息1大小（仅包含DateTime载荷）为919字节。当前ratchet的大多数消息1大小的载荷都小于816字节，因此可以将它们分类为非混合ratchet。大消息可能是POST请求，这种情况比较少见。

因此推荐的策略是：

- 如果消息 1 小于 919 字节，则为当前的 ratchet 协议。
- 如果消息 1 大于或等于 919 字节，则可能是 MLKEM512_X25519。
  先尝试 MLKEM512_X25519，如果失败，则尝试当前的 ratchet 协议。

这应该允许我们在同一个destination上高效支持标准ratchet和混合ratchet，就像我们之前在同一个destination上支持ElGamal和ratchet一样。因此，我们可以比无法为同一个destination支持双协议的情况下更快地迁移到MLKEM混合协议，因为我们可以向现有的destination添加MLKEM支持。

必需支持的组合有：

- X25519 + MLKEM512
- X25519 + MLKEM768
- X25519 + MLKEM1024

以下组合可能较为复杂，不要求必须支持，但可能会支持，这取决于具体实现：

- 多于一个 MLKEM
- ElG + 一个或多个 MLKEM
- X25519 + 一个或多个 MLKEM
- ElG + X25519 + 一个或多个 MLKEM

我们可能不会尝试在同一个目标上支持多种 MLKEM 算法（例如，MLKEM512_X25519 和 MLKEM_768_X25519）。只选择一种；然而，这取决于我们选择首选的 MLKEM 变体，这样 HTTP 客户端 tunnel 就可以使用其中一种。依赖于具体实现。

我们可能会尝试在同一个目标上支持三种算法（例如 X25519、MLKEM512_X25519 和 MLKEM769_X25519）。分类和重试策略可能过于复杂。配置和配置界面可能过于复杂。依赖于具体实现。

我们可能不会尝试在同一个目标上支持 ElGamal 和混合算法。ElGamal 已经过时，而且仅支持 ElGamal + 混合（没有 X25519）没有太大意义。此外，ElGamal 和混合新会话消息都很大，因此分类策略通常必须尝试两种解密方式，这会很低效。具体实现方式依赖于实现。

客户端可以在相同的隧道上对 X25519 和混合协议使用相同或不同的 X25519 静态密钥，具体取决于实现。

#### Alice KDF for Message 1（Alice 消息 1 的密钥派生函数）

ECIES 规范允许在 New Session Message 载荷中包含 Garlic Messages，这使得初始流数据包（通常是 HTTP GET）能够与客户端的 leaseset 一起进行 0-RTT 传输。然而，New Session Message 载荷不具备前向保密性。由于本提案强调为 ratchet 增强前向保密性，实现可能会或应该推迟包含流载荷或完整流消息，直到第一个 Existing Session Message。这将以牺牲 0-RTT 传输为代价。策略也可能取决于流量类型或隧道类型，或者例如取决于 GET 与 POST 的区别。具体实现相关。

#### 消息 1 的 Bob KDF

在同一目标上使用 MLKEM、MLDSA 或两者都使用，将大幅增加新会话消息的大小，如上所述。这可能会显著降低新会话消息通过 tunnel 传递的可靠性，因为它们必须被分片成多个 1024 字节的 tunnel 消息。传递成功率与分片数量成指数关系。实现可以使用各种策略来限制消息大小，但代价是牺牲 0-RTT 传递。取决于具体实现。

### Ratchet

我们可以在会话请求中设置临时密钥的最高有效位（key[31] & 0x80）来表示这是一个混合连接。这将允许我们在同一端口上同时运行标准 NTCP 和混合 NTCP。只支持一种混合变体，并在 router 地址中公告。例如，v=2,3 或 v=2,4 或 v=2,5。

如果我们不这样做，我们需要不同的传输地址/端口，以及一个新的协议名称，例如"NTCP1PQ1"。

注意：类型代码仅供内部使用。Router将保持类型4，支持情况将在router地址中指示。

待办事项

### SSU2

可能需要不同的传输地址/端口，但希望不需要，我们有一个带有消息1标志的头部。我们可以在内部使用版本字段，对MLKEM512使用3，对MLKEM768使用4。也许地址中只用v=2,3,4就足够了。但我们需要为两个新算法提供标识符：3a, 3b？

检查并验证 SSU2 是否能够处理跨多个数据包分片的 RI（6-8 个？）。i2pd 目前最多只支持 2 个分片？

注意：类型码仅供内部使用。Router 将保持类型 4，支持情况将在 router 地址中指示。

待办事项

## Router Compatibility

### Transport Names

如果我们可以在同一端口上运行标准和混合版本，并使用版本标志，我们可能不需要新的传输名称。

如果我们确实需要新的传输名称，它们将是：

| Transport | Type |
|-----------|------|
| NTCP2PQ1 | MLKEM512_X25519 |
| NTCP2PQ2 | MLKEM768_X25519 |
| NTCP2PQ3 | MLKEM1024_X25519 |
| SSU2PQ1 | MLKEM512_X25519 |
| SSU2PQ2 | MLKEM768_X25519 |
请注意，SSU2 无法支持 MLKEM1024，它太大了。

### Router Enc. Types

我们有几个备选方案需要考虑：

#### Bob KDF for Message 2 的密钥派生函数

不推荐。仅使用上述与 router 类型匹配的新传输协议。较旧的 router 无法连接、通过其构建隧道或向其发送 netDb 消息。需要数个发布周期来调试并确保支持后才能默认启用。相比下面的替代方案，可能会延长推广时间一年或更久。

#### Alice KDF for Message 2（Alice 密钥派生函数用于消息 2）

推荐。由于PQ不会影响X25519静态密钥或N握手协议，我们可以保持router为类型4，只是宣告新的传输方式。较旧的router仍然可以连接、通过其构建tunnel或向其发送netDb消息。

#### KDF for Message 3（仅限 XK）

类型 4 router 可以同时公布 NTCP2 和 NTCP2PQ* 地址。这些地址可以使用相同的静态密钥和其他参数，也可以不使用。这些协议可能需要使用不同的端口；在同一个端口上同时支持 NTCP2 和 NTCP2PQ* 协议会非常困难，因为没有头部或帧结构能够让 Bob 对传入的 Session Request 消息进行分类和成帧。

分离端口和地址对于 Java 来说会比较困难，但对于 i2pd 来说则很直接。

#### split() 的 KDF

Type 4 router可以同时广播SSU2和SSU2PQ*地址。通过添加的头部标志，Bob可以在第一条消息中识别传入的传输类型。因此，我们可以在同一端口上同时支持SSU2和SSUPQ*。

这些可以作为单独的地址发布（如 i2pd 在之前的过渡中所做的那样），或者在同一个地址中使用参数来表示 PQ 支持（如 Java i2p 在之前的过渡中所做的那样）。

如果在相同地址，或在不同地址的相同端口上，这些将使用相同的静态密钥和其他参数。如果在不同地址的不同端口上，这些可以使用相同的静态密钥和其他参数，也可以不使用。

对于 Java 来说，分离端口和地址会比较困难，但对于 i2pd 来说则很简单。

#### Recommendations

待办事项

### NTCP2

#### Noise 标识符

较旧的 router 会验证 RI，因此无法连接、通过其构建隧道或向其发送 netDb 消息。需要几个发布周期来调试并确保支持后才能默认启用。会遇到与 enc. type 5/6/7 部署相同的问题；相比上述列出的 type 4 enc. type 部署替代方案，可能会将部署时间延长一年或更久。

没有替代方案。

### LS Enc. Types

#### 1b) 新会话格式（带绑定）

这些可能会在使用较旧的 type 4 X25519 密钥的 LS 中出现。较旧的 router 会忽略未知的密钥。

目的地可以支持多种密钥类型，但只能通过对消息1使用每个密钥进行试验性解密来实现。可以通过维护每个密钥成功解密的计数，并首先尝试使用最常用的密钥来减轻开销。Java I2P在同一目的地上对ElGamal+X25519使用这种策略。

### Dest. Sig. Types

#### 1g) 新会话回复格式

Router 验证 leaseSet 签名，因此无法连接或接收类型 12-17 目标的 leaseSet。需要几个发布周期来调试并确保支持后才能默认启用。

无替代方案。

## 规范

最有价值的数据是端到端流量，使用 ratchet 加密。作为 tunnel 跳之间的外部观察者，数据会再被加密两次，分别是 tunnel 加密和传输加密。作为 OBEP 和 IBGW 之间的外部观察者，数据只会再被加密一次，即传输加密。作为 OBEP 或 IBGW 参与者，ratchet 是唯一的加密。然而，由于 tunnel 是单向的，要捕获 ratchet 握手中的两条消息需要 router 之间的串通，除非 tunnel 的构建将 OBEP 和 IBGW 放在同一个 router 上。

目前最令人担忧的后量子威胁模型是现在存储流量，以便在多年后进行解密（前向保密）。混合方法可以提供保护。

PQ威胁模型是在合理时间内（比如几个月内）破解认证密钥，然后冒充认证或近乎实时地进行解密，这种威胁还很遥远？而这正是我们希望迁移到PQC静态密钥的时机。

因此，最早的PQ威胁模型是OBEP/IBGW存储流量以备后续解密。我们应该首先实现混合棘轮机制。

Ratchet 是最高优先级。传输协议次之。签名是最低优先级。

签名推出也将比加密推出晚一年或更长时间，因为无法实现向后兼容性。此外，MLDSA在行业中的采用将由CA/Browser Forum和证书颁发机构标准化。CA首先需要硬件安全模块(HSM)支持，但目前尚不可用 [CA/Browser Forum](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/)。我们期望CA/Browser Forum推动特定参数选择的决策，包括是否支持或要求复合签名 [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/)。

| Milestone | Target |
|-----------|--------|
| Ratchet beta | Late 2025 |
| Select best enc type | Early 2026 |
| NTCP2 beta | Early 2026 |
| SSU2 beta | Mid 2026 |
| Ratchet production | Mid 2026 |
| Ratchet default | Late 2026 |
| Signature beta | Late 2026 |
| NTCP2 production | Late 2026 |
| SSU2 production | Early 2027 |
| Select best sig type | Early 2027 |
| NTCP2 default | Early 2027 |
| SSU2 default | Mid 2027 |
| Signature production | Mid 2027 |
## Migration

如果我们无法在相同的tunnel上同时支持旧的和新的ratchet协议，迁移将会变得更加困难。

我们应该能够像处理X25519时那样，逐一尝试这两种方法来验证。

## Issues

- Noise 哈希选择 - 继续使用 SHA256 还是升级？
  SHA256 在未来 20-30 年应该都是安全的，不会受到后量子算法威胁，
  参见 [NIST presentation](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf) 和 [NIST presentation](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf)。
  如果 SHA256 被破解，我们面临的问题会更严重（netdb）。
- NTCP2 独立端口，独立 router 地址
- SSU2 中继 / 节点测试
- SSU2 版本字段
- SSU2 router 地址版本
