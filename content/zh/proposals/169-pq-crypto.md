---
title: "后量子密码协议"
aliases:
  - "/proposals/169-pq-crypto"
  - "/proposals/169-pq-crypto/"
number: "169"
author: "zzz, orignal, drzed, eyedeekay"
created: "2025-01-21"
lastupdated: "2026-10-24"
status: "打开"
thread: "http://zzz.i2p/topics/3294"
target: "0.9.80"
toc: true
---

### 状态

| 协议/功能 | 状态 |
|--------------------|--------|
| Ratchet | 在 Java I2P 和 i2pd 中完成 |
| NTCP2 | 2026年第一季度测试版 |
| SSU2 | 即将开始实施，2026年第二三季度测试版 |
| MLDSA SigTypes | 低优先级，可能在2027年以后 |
## 概述

虽然对合适的后量子（PQ）密码学的研究和竞争已经进行了十年，但直到最近选择才变得明确。

我们在2022年开始研究PQ密码学的影响 [zzz.i2p](http://zzz.i2p/topics/3294)。

TLS 标准在过去两年中增加了混合加密支持，由于 Chrome 和 Firefox 的支持，它现在被用于互联网上很大一部分加密流量 [Cloudflare](https://blog.cloudflare.com/pq-2024/)。

NIST 最近最终确定并发布了后量子密码学的推荐算法 [NIST](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards)。几个常见的密码学库现在已经支持 NIST 标准，或者将在不久的将来发布相关支持。

[Cloudflare](https://blog.cloudflare.com/pq-2024/) 和 [NIST](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards) 都建议立即开始迁移。另请参见2022年NSA PQ常见问题解答 [NSA](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF)。I2P应该在安全性和密码学方面成为领导者。现在是实施推荐算法的时候了。利用我们灵活的加密类型和签名类型系统，我们将为混合加密以及后量子和混合签名添加类型。

## 目标

- 选择抗量子算法
- 在适当的 I2P 协议中添加纯量子和混合算法
- 定义多个变体
- 在实施、测试、分析和研究后选择最佳变体
- 增量添加支持并保持向后兼容性

## 非目标

- 不要更改单向（Noise N）加密协议
- 不要放弃SHA256，近期内不会受到PQ威胁
- 目前不要选择最终的首选变体

## 威胁模型

- OBEP 或 IBGW 的 router，可能串通，
  存储 garlic 消息以供后续解密（前向保密）
- 网络观察者
  存储传输消息以供后续解密（前向保密）
- 网络参与者为 RI、LS、流传输、数据报
  或其他结构伪造签名

## 受影响的协议

我们将修改以下协议，大致按开发顺序排列。整体推出时间可能从2025年底到2027年中期。详情请参见下面的优先级和推出部分。

| 协议 / 功能 | 状态 |
|--------------------|--------|
| Hybrid MLKEM Ratchet 和 LS | 2025年6月批准；2025年8月测试版；2025年11月发布 |
| Hybrid MLKEM NTCP2 | 已在实时网络测试，2026年2月批准；目标2026年5月测试版；目标2026年8月发布 |
| Hybrid MLKEM SSU2 | 2026年2月批准；目标2026年8月测试版；目标2026年11月发布 |
| MLDSA SigTypes 12-14 | 提案已稳定但可能要到2027年才能最终确定 |
| MLDSA Dests | 已在实时网络测试，需要网络升级以支持 floodfill |
| Hybrid SigTypes 15-17 | 初步阶段 |
| Hybrid Dests | |
## 设计

我们将支持基于但不兼容 CRYSTALS-Kyber 和 CRYSTALS-Dilithium（3.1、3 及更早版本）的 NIST FIPS 203 和 204 标准 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)。

### 密钥交换

我们将在以下协议中支持混合密钥交换：

| Proto   | Noise Type | Support PQ only? | Support Hybrid? |
|---------|------------|------------------|-----------------|
| NTCP2   | XK         | 否               | 是              |
| SSU2    | XK         | 否               | 是              |
| Ratchet | IK         | 否               | 是              |
| TBM     | N          | 否               | 否              |
| NetDB   | N          | 否               | 否              |
PQ KEM 仅提供临时密钥，不直接支持静态密钥握手，如 Noise XK 和 IK。

Noise N 不使用双向密钥交换，因此不适用于混合加密。

因此，我们将仅支持混合加密，适用于 NTCP2、SSU2 和 Ratchet。我们将按照 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) 中的定义，定义三种 ML-KEM 变体，总共 3 种新的加密类型。混合类型将仅与 X25519 结合定义。

新的加密类型包括：

| 类型 | 代码 |
|------|------|
| MLKEM512_X25519 | 5 |
| MLKEM768_X25519 | 6 |
| MLKEM1024_X25519 | 7 |
开销将会很大。典型的消息1和消息2大小（用于XK和IK）目前约为100字节（在任何额外载荷之前）。根据算法的不同，这将增加8倍到15倍。

### 签名

我们将在以下结构中支持 PQ 和混合签名：

因此我们将同时支持纯PQ和混合签名。我们将按照[FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)中的定义支持三种ML-DSA变体，三种与Ed25519结合的混合变体，以及三种仅用于SU3文件的带预哈希的纯PQ变体，总共9种新的签名类型。混合类型只会与Ed25519结合定义。我们将使用标准的ML-DSA，而不是预哈希变体(HashML-DSA)，但SU3文件除外。

| 类型 | 仅支持 PQ？ | 支持混合？ |
|------|-------------|------------|
| RouterInfo | 是 | 是 |
| LeaseSet | 是 | 是 |
| Streaming SYN/SYNACK/Close | 是 | 是 |
| Repliable Datagrams | 是 | 是 |
| Datagram2 (prop. 163) | 是 | 是 |
| I2CP create session msg | 是 | 是 |
| SU3 文件 | 是 | 是 |
| X.509 证书 | 是 | 是 |
| Java keystores | 是 | 是 |
我们将使用"对冲"或随机化签名变体，而不是"确定性"变体，如 [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) 第 3.4 节所定义。这确保了每个签名都是不同的，即使是对相同数据进行签名，并提供了额外的侧信道攻击防护。有关算法选择（包括编码和上下文）的更多详细信息，请参阅下面的实现说明部分。

新的签名类型有：

X.509 证书和其他 DER 编码将使用 [IETF 草案](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/) 中定义的复合结构和 OID。

| 类型 | 代码 |
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
开销将是巨大的。典型的 Ed25519 destination 和 router identity 大小为 391 字节。根据算法不同，这些将增加 3.5 倍到 6.8 倍。Ed25519 签名为 64 字节。根据算法不同，这些将增加 38 倍到 76 倍。典型的已签名 RouterInfo、LeaseSet、可回复数据报和已签名流消息约为 1KB。根据算法不同，这些将增加 3 倍到 8 倍。

由于新的destination和router identity类型将不包含填充，它们将不可压缩。在传输过程中进行gzip压缩的destination和router identity的大小将根据算法增加12倍至38倍。

对于目标节点，新的签名类型在 leaseSet 中支持所有加密类型。在密钥证书中将加密类型设置为 NONE (255)。

### 合法组合

对于RouterIdentities，ElGamal加密类型已被弃用。新的签名类型仅支持X25519（类型4）加密。新的加密类型将在RouterAddresses中指示。密钥证书中的加密类型将继续为类型4。

SHA3-256、SHAKE128 和 SHAKE256 的测试向量可在 [NIST](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values) 找到。

### 需要新的加密技术

- ML-KEM (前称 CRYSTALS-Kyber) [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
- ML-DSA (前称 CRYSTALS-Dilithium) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)
- SHA3-128 (前称 Keccak-256) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf) 仅用于 SHAKE128
- SHA3-256 (前称 Keccak-512) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
- SHAKE128 和 SHAKE256 (SHA3-128 和 SHA3-256 的 XOF 扩展) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)

注意，Java bouncycastle 库支持上述所有算法。C++ 库支持在 OpenSSL 3.5 中提供 [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)。

我们不会支持 [FIPS 205](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.205.pdf) (Sphincs+)，它比 ML-DSA 慢得多且体积大得多。我们不会支持即将发布的 FIPS206 (Falcon)，它尚未标准化。我们不会支持 NTRU 或其他未被 NIST 标准化的后量子候选算法。

### 替代方案

有一些研究[论文](https://eprint.iacr.org/2020/379.pdf)探讨了将 Wireguard (IK) 适配为纯后量子密码学，但该论文中存在几个开放性问题。后来，这种方法被实现为 Rosenpass [Rosenpass](https://rosenpass.eu/) [白皮书](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf)，用于后量子 Wireguard。

### Rosenpass

Rosenpass 使用类似 Noise KK 的握手协议，采用预共享的 Classic McEliece 460896 静态密钥（每个 500 KB）和 Kyber-512（本质上是 MLKEM-512）临时密钥。由于 Classic McEliece 密文只有 188 字节，而 Kyber-512 公钥和密文大小合理，因此两个握手消息都能在标准 UDP MTU 内传输。来自 PQ KK 握手的输出共享密钥（osk）被用作标准 Wireguard IK 握手的输入预共享密钥（psk）。因此总共有两次完整的握手，一次是纯 PQ 握手，一次是纯 X25519 握手。

我们无法用这些方法来替换我们的XK和IK握手，因为：

白皮书中有很多有价值的信息，我们会审阅它以获取想法和灵感。待办事项。

- 我们无法执行 KK，Bob 没有 Alice 的静态密钥
- 500KB 的静态密钥太大了
- 我们不想要额外的往返通信

按如下方式更新通用结构文档 [/docs/specs/common-structures/](/docs/specs/common-structures/) 中的章节和表格：

## 规范

### 通用结构

新的公钥类型包括：

#### 问题

混合公钥是 X25519 密钥。KEM 公钥是从 Alice 发送到 Bob 的临时 PQ 密钥。编码和字节顺序在 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) 中定义。

| 类型 | 公钥长度 | 版本 | 用途 |
|------|---------|------|------|
| MLKEM512_X25519 | 32 | 0.9.xx | 参见提案 169，仅用于 leaseSet，不用于 RI 或 Destination |
| MLKEM768_X25519 | 32 | 0.9.xx | 参见提案 169，仅用于 leaseSet，不用于 RI 或 Destination |
| MLKEM1024_X25519 | 32 | 0.9.xx | 参见提案 169，仅用于 leaseSet，不用于 RI 或 Destination |
| MLKEM512 | 800 | 0.9.xx | 参见提案 169，仅用于握手，不用于 leaseSet、RI 或 Destination |
| MLKEM768 | 1184 | 0.9.xx | 参见提案 169，仅用于握手，不用于 leaseSet、RI 或 Destination |
| MLKEM1024 | 1568 | 0.9.xx | 参见提案 169，仅用于握手，不用于 leaseSet、RI 或 Destination |
| MLKEM512_CT | 768 | 0.9.xx | 参见提案 169，仅用于握手，不用于 leaseSet、RI 或 Destination |
| MLKEM768_CT | 1088 | 0.9.xx | 参见提案 169，仅用于握手，不用于 leaseSet、RI 或 Destination |
| MLKEM1024_CT | 1568 | 0.9.xx | 参见提案 169，仅用于握手，不用于 leaseSet、RI 或 Destination |
| NONE | 0 | 0.9.xx | 参见提案 169，仅用于具有 PQ 签名类型的 destination，不用于 RI 或 leaseSet |
MLKEM*_CT 密钥实际上并不是公钥，它们是在 Noise 握手中从 Bob 发送给 Alice 的"密文"。在这里列出它们是为了完整性。

新的私钥类型包括：

#### 私钥

混合私钥是 X25519 密钥。KEM 私钥仅供 Alice 使用。KEM 编码和字节序在 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) 中定义。

| 类型 | 私钥长度 | 起始版本 | 用途 |
|------|---------------------|-------|-------|
| MLKEM512_X25519 | 32 | 0.9.xx | 参见提案 169，仅用于 Leasesets，不用于 RIs 或 Destinations |
| MLKEM768_X25519 | 32 | 0.9.xx | 参见提案 169，仅用于 Leasesets，不用于 RIs 或 Destinations |
| MLKEM1024_X25519 | 32 | 0.9.xx | 参见提案 169，仅用于 Leasesets，不用于 RIs 或 Destinations |
| MLKEM512 | 1632 | 0.9.xx | 参见提案 169，仅用于握手，不用于 Leasesets、RIs 或 Destinations |
| MLKEM768 | 2400 | 0.9.xx | 参见提案 169，仅用于握手，不用于 Leasesets、RIs 或 Destinations |
| MLKEM1024 | 3168 | 0.9.xx | 参见提案 169，仅用于握手，不用于 Leasesets、RIs 或 Destinations |
新的签名公钥类型包括：

#### SigningPublicKey

混合签名公钥是 Ed25519 密钥后跟 PQ 密钥，如 [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/) 中所述。编码和字节顺序在 [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) 中定义。

| 类型 | 长度（字节） | 版本 | 用途 |
|------|----------------|-------|-------|
| MLDSA44 | 1312 | 0.9.xx | 参见提案 169 |
| MLDSA65 | 1952 | 0.9.xx | 参见提案 169 |
| MLDSA87 | 2592 | 0.9.xx | 参见提案 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 1344 | 0.9.xx | 参见提案 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 1984 | 0.9.xx | 参见提案 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 2624 | 0.9.xx | 参见提案 169 |
| MLDSA44ph | 1344 | 0.9.xx | 仅用于 SU3 文件，不用于 netDb 结构 |
| MLDSA65ph | 1984 | 0.9.xx | 仅用于 SU3 文件，不用于 netDb 结构 |
| MLDSA87ph | 2624 | 0.9.xx | 仅用于 SU3 文件，不用于 netDb 结构 |
新的签名私钥类型包括：

#### SigningPrivateKey

混合签名私钥是 Ed25519 密钥后跟 PQ 密钥，如 [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/) 中所述。编码和字节顺序在 [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) 中定义。

| 类型 | 长度（字节） | 起始版本 | 用法 |
|------|----------------|-------|-------|
| MLDSA44 | 2560 | 0.9.xx | 参见提案 169 |
| MLDSA65 | 4032 | 0.9.xx | 参见提案 169 |
| MLDSA87 | 4896 | 0.9.xx | 参见提案 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2592 | 0.9.xx | 参见提案 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 4064 | 0.9.xx | 参见提案 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4928 | 0.9.xx | 参见提案 169 |
| MLDSA44ph | 2592 | 0.9.xx | 仅用于 SU3 文件，不用于 netDb 结构。参见提案 169 |
| MLDSA65ph | 4064 | 0.9.xx | 仅用于 SU3 文件，不用于 netDb 结构。参见提案 169 |
| MLDSA87ph | 4928 | 0.9.xx | 仅用于 SU3 文件，不用于 netDb 结构。参见提案 169 |
新的签名类型有：

混合签名是 Ed25519 签名后跟 PQ 签名，如 [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/) 中所述。混合签名通过验证两个签名来验证，如果任何一个失败则验证失败。编码和字节序在 [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) 中定义。

#### 签名

新的签名公钥类型包括：

| 类型 | 长度（字节） | 起始版本 | 用途 |
|------|----------------|-------|-------|
| MLDSA44 | 2420 | 0.9.xx | 参见提案 169 |
| MLDSA65 | 3309 | 0.9.xx | 参见提案 169 |
| MLDSA87 | 4627 | 0.9.xx | 参见提案 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2484 | 0.9.xx | 参见提案 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 3373 | 0.9.xx | 参见提案 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4691 | 0.9.xx | 参见提案 169 |
| MLDSA44ph | 2484 | 0.9.xx | 仅用于 SU3 文件，不用于 netDb 结构。参见提案 169 |
| MLDSA65ph | 3373 | 0.9.xx | 仅用于 SU3 文件，不用于 netDb 结构。参见提案 169 |
| MLDSA87ph | 4691 | 0.9.xx | 仅用于 SU3 文件，不用于 netDb 结构。参见提案 169 |
新的加密公钥类型包括：

#### 密钥证书

混合签名公钥是 Ed25519 密钥后跟 PQ 密钥，如 [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/) 中所述。编码和字节顺序在 [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) 中定义。

| 类型 | 类型代码 | 总公钥长度 | 起始版本 | 用途 |
|------|-----------|-------------------------|-------|-------|
| MLDSA44 | 12 | 1312 | 0.9.xx | 见提案 169 |
| MLDSA65 | 13 | 1952 | 0.9.xx | 见提案 169 |
| MLDSA87 | 14 | 2592 | 0.9.xx | 见提案 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 0.9.xx | 见提案 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 0.9.xx | 见提案 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 0.9.xx | 见提案 169 |
| MLDSA44ph | 18 | n/a | 0.9.xx | 仅用于 SU3 文件 |
| MLDSA65ph | 19 | n/a | 0.9.xx | 仅用于 SU3 文件 |
| MLDSA87ph | 20 | n/a | 0.9.xx | 仅用于 SU3 文件 |
对于使用 Hybrid 或 PQ 签名类型的目标，加密类型使用 NONE（类型 255），但没有加密密钥，整个 384 字节的主要部分都用于签名密钥。

| 类型 | 类型代码 | 公钥总长度 | 起始版本 | 用途 |
|------|-----------|-------------------------|-------|-------|
| MLKEM512_X25519 | 5 | 32 | 0.9.xx | 参见提案 169，仅用于 LeaseSet，不用于 RI 或 Destination |
| MLKEM768_X25519 | 6 | 32 | 0.9.xx | 参见提案 169，仅用于 LeaseSet，不用于 RI 或 Destination |
| MLKEM1024_X25519 | 7 | 32 | 0.9.xx | 参见提案 169，仅用于 LeaseSet，不用于 RI 或 Destination |
| NONE | 255 | 0 | 0.9.xx | 参见提案 169 |
混合密钥类型绝不会包含在密钥证书中；只会包含在 leaseSet 中。

无填充。总长度为 7 + 总密钥长度。密钥证书长度为 4 + 超出密钥长度。

#### 目标地址大小

以下是新 Destination 类型的长度。所有类型的加密类型都是 NONE（类型 255），加密密钥长度被视为 0。整个 384 字节部分用于签名公钥的第一部分。注意：这与 ECDSA_SHA512_P521 和 RSA 签名类型的规范不同，在那些类型中，我们在目标中保留了 256 字节的 ElGamal 密钥，即使它没有被使用。

skey[0:383] 5 (932 >> 8) (932 & 0xff) 00 12 00 255 skey[384:1311]

MLDSA44 的 1319 字节目标字节流示例：

MLDSA44 的示例 1351 字节 router identity 字节流：

| Type | Type Code | Total Public Key Length | Main | Excess | Total Dest Length |
|------|-----------|-------------------------|------|--------|-------------------|
| MLDSA44 | 12 | 1312 | 384 | 928 | 1319 |
| MLDSA65 | 13 | 1952 | 384 | 1568 | 1959 |
| MLDSA87 | 14 | 2592 | 384 | 2208 | 2599 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 384 | 960 | 1351 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 384 | 1600 | 1991 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 384 | 2240 | 2631 |
#### RouterIdent 大小

以下是新 Destination 类型的长度。所有类型的加密类型都是 X25519（类型 4）。X25519 公钥之后的整个 352 字节部分用于签名公钥的第一部分。无填充。总长度为 39 + 总密钥长度。密钥证书长度为 4 + 超出密钥长度。

握手使用 [Noise Protocol](https://noiseprotocol.org/noise.html) 握手模式。

enckey[0:31] skey[0:351] 5 (960 >> 8) (960 & 0xff) 00 12 00 4 skey[352:1311]

| 类型 | 类型代码 | 总公钥长度 | 主要 | 多余 | 总RouterIdent长度 |
|------|-----------|-------------------------|------|--------|--------------------------|
| MLDSA44 | 12 | 1312 | 352 | 960 | 1351 |
| MLDSA65 | 13 | 1952 | 352 | 1600 | 1991 |
| MLDSA87 | 14 | 2592 | 352 | 2240 | 2631 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 352 | 992 | 1383 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 352 | 1632 | 2023 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 352 | 2272 | 2663 |
### PublicKey

以下对 XK 和 IK 的混合前向保密 (hfs) 修改按照 [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) 第 5 节的规定：

e1 模式的定义如下，如 [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) 第 4 节所述：

#### split() 的密钥派生函数

```

  M = message
  Prefix = "CompositeAlgorithmSignatures2025" (32 bytes, not null terminated)
  Label = (30 bytes, not null terminated), one of:
          "COMPSIG-MLDSA44-Ed25519-SHA512"
          "COMPSIG-MLDSA65-Ed25519-SHA512"
          "COMPSIG-MLDSA87-Ed25519-SHA512"  // not in [COMPOSITE-SIGS]
  ctx = "" (0 bytes)
  len(ctx) = 0  (1 byte)
  PH(M) = SHA512(M) (64 bytes)


  Compute a hash of the message prepended as follows:

  M' = Prefix || Label || len(ctx) || ctx || PH( M )

  M' length is 127 bytes.

  Sign the prehashed message M':

  signature = MLDSA_SIGN(M') || Ed25519_SIGN(M')

```
#### Noise 标识符

ekem1 模式的定义如下，如 [Noise HFS 规范](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) 第 4 节所述：

```

  M' = as above

  signature = MLDSA_VERIFY(M') && Ed25519_VERIFY(M')


```
#### 1b) 新会话格式（带绑定）

本节适用于 IK 和 XK 协议。

### 握手模式

混合握手在 [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) 中定义。第一个消息，从 Alice 到 Bob，在消息有效载荷之前包含 e1，即封装密钥。这被视为一个额外的静态密钥；（作为 Alice）对其调用 EncryptAndHash() 或（作为 Bob）调用 DecryptAndHash()。然后像往常一样处理消息有效载荷。

使用以下字母映射：

- e = 一次性临时密钥
- s = 静态密钥
- p = 消息载荷
- e1 = 一次性临时PQ密钥，从Alice发送到Bob
- ekem1 = KEM密文，从Bob发送到Alice

我们定义以下函数，对应于 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) 中定义的加密构建块。

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
(encap_key, decap_key) = PQ_KEYGEN()

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
(ciphertext, kem_shared_key) = ENCAPS(encap_key)

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
### Noise 握手 KDF

#### 1b) 新会话格式（带绑定）

- 我们是否应该改变握手哈希函数？请参见[比较](https://kerkour.com/fast-secure-hash-function-sha256-sha512-sha3-blake3)。
  SHA256 对后量子（PQ）攻击不脆弱，但如果我们确实想要升级
  我们的哈希函数，现在正是时候，趁我们正在改变其他事情。
  当前的 IETF SSH 提案 [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-sshm-mlkem-hybrid-kex/) 是使用 MLKEM768
  与 SHA256，以及 MLKEM1024 与 SHA384。该提案包含
  对安全考虑的讨论。
- 我们是否应该停止发送 0-RTT ratchet 数据（除了 leaseSet）？
- 如果我们不发送 0-RTT 数据，是否应该将 ratchet 从 IK 切换到 XK？

#### 概述

kem_shared_key = DECAPS(ciphertext, decap_key)

请注意，encap_key 和 ciphertext 都在 Noise 握手消息 1 和 2 的 ChaCha/Poly 块内被加密。它们将作为握手过程的一部分被解密。

第二条消息，从 Bob 到 Alice，在消息载荷之前包含 ekem1，即密文。这被视为额外的静态密钥；对其调用 EncryptAndHash()（作为 Bob）或 DecryptAndHash()（作为 Alice）。然后，计算 kem_shared_key 并调用 MixKey(kem_shared_key)。然后按常规处理消息载荷。

#### 已定义的 ML-KEM 操作

对于 XK：在 'es' 消息模式之后和有效载荷之前，添加：

或者

    Alice creates the encapsulation and decapsulation keys
    The encapsulation key is sent in message 1.
    encap_key and decap_key sizes vary based on ML-KEM variant.

对于 IK：在 'es' 消息模式之后和 's' 消息模式之前，添加：

    Bob calculates the ciphertext and shared key,
    using the ciphertext received in message 1.
    The ciphertext is sent in message 2.
    ciphertext size varies based on ML-KEM variant.
    The kem_shared_key is always 32 bytes.

对于 XK：在 'es' 消息模式之后和载荷之前，添加：

    Alice calculates the shared key,
    using the ciphertext received in message 2.
    The kem_shared_key is always 32 bytes.

或

kem_shared_key 通过 MixHash() 混合到链式密钥中。详细信息请参见下文。

#### Alice KDF for Message 1

对于 XK：在 'ee' 消息模式之后和载荷之前，添加：

或

对于 IK：在 'ee' 消息模式之后和 'se' 消息模式之前，添加：

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
#### Bob KDF 用于消息 1

对于 XK：在 'ee' 消息模式之后和载荷之前，添加：

或

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
#### 消息 2 的 Bob KDF

按如下方式更新 ECIES-Ratchet 规范 [/docs/specs/ecies/](/docs/specs/ecies/)：

或

加密格式：

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

  // AEAD parameters for payload section
  ... as in standard SSU2 ...
  k = keydata[32:63]
  ...

```
#### Alice KDF for Message 2

在 'ee' 消息模式之后（以及在 IK 的 'ss' 消息模式之前），添加：

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

  // AEAD parameters for payload section
  ... as in standard SSU2 ...
  k = keydata[32:63]
  ...

```
#### 消息 3 的 KDF（仅限 XK）

unchanged

#### Noise 标识符

unchanged

### 棘轮

变更：当前的ratchet在第一个ChaCha部分有空负载，在第二部分有负载。使用ML-KEM后，现在有三个部分。第一部分包含加密的PQ密文。第二部分有空负载。第三部分包含负载。

#### 长报头

- "Noise_IKhfselg2_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM1024_ChaChaPoly_SHA256"

#### 短标头

变更：当前的 ratchet 在第一个 ChaCha 段中包含静态密钥，在第二段中包含有效负载。使用 ML-KEM 后，现在有三个段。第一段包含加密的 PQ 公钥。第二段包含静态密钥。第三段包含有效负载。

解密格式：

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

| 类型 | 类型代码 | X 长度 | 消息 1 长度 | 消息 1 加密长度 | 消息 1 解密长度 | PQ 密钥长度 | pl 长度 |
|------|-----------|-------|-----------|---------------|---------------|------------|--------|
| X25519 | 4 | 32 | 96+pl | 64+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 912+pl | 880+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1296+pl | 1360+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1680+pl | 1648+pl | 1568+pl | 1568 | pl |
注意有效载荷必须包含一个 DateTime 块，因此最小有效载荷大小为 7。可以据此计算最小消息 1 大小。

#### 1g) 新会话回复格式

变更：当前的 NTCP2 仅包含 ChaCha 部分中的选项。使用 ML-KEM 后，ChaCha 部分还将包含加密的 PQ 公钥。

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

| 类型 | 类型代码 | Y 长度 | 消息 2 长度 | 消息 2 加密长度 | 消息 2 解密长度 | PQ CT 长度 | 可选长度 |
|------|-----------|-------|-----------|---------------|---------------|-----------|---------|
| X25519 | 4 | 32 | 72+pl | 32+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 856+pl | 816+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1176+pl | 1136+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1656+pl | 1616+pl | 1568+pl | 1568 | pl |
注意，虽然消息2通常会有非零载荷，但ratchet规范 [/docs/specs/ecies/](/docs/specs/ecies/) 并不要求如此，因此最小载荷大小为0。消息2的最小大小可以据此计算。

### NTCP2

按如下方式更新 NTCP2 规范 [/docs/specs/ntcp2/](/docs/specs/ntcp2/)：

#### Noise 标识符

- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM1024_ChaChaPoly_SHA256"

#### 1) SessionRequest

原始内容：

为了使PQ和非PQ的NTCP2能够在同一个router地址和端口上得到支持，我们使用X值（X25519临时公钥）的最高有效位来标记这是一个PQ连接。对于非PQ连接，这个位始终未设置。

注意：消息 1 选项块中的版本字段必须设置为 2，即使对于 PQ 连接也是如此。

对于Bob，在对X进行AES去混淆后，测试X[31] & 0x80。如果该位被设置，则用X[31] &= 0x7f清除它，并通过Noise作为PQ连接进行解密。如果该位未设置，则像往常一样通过Noise作为非PQ连接进行解密。

对于在不同 router 地址和端口上发布的 PQ NTCP2，这不是必需的。

如需更多信息，请参见下面的已发布地址部分。

未加密数据（未显示 Poly1305 认证标签）：

```
  +----+----+----+----+----+----+----+----+
  |        MS bit set to 1 and then       |
  +        obfuscated with RH_B           +
  |       AES-CBC-256 encrypted X         |
  +             (32 bytes)                +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaChaPoly encrypted data (MLKEM)   |
  +      (see table below for length)     +
  |   k defined in KDF for message 1      |
  +   n = 0                               +
  |   see KDF for associated data         |
  ~                                       ~
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (options)   |
  +         16 bytes                      +
  |   k defined in KDF for message 1      |
  +   n = 1                               +
  |   see KDF for associated data         |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  ~         padding (optional)            ~
  |     length defined in options block   |
  +----+----+----+----+----+----+----+----+

  Same as current specification except add a second ChaChaPoly frame
```
未加密数据（未显示 Poly1305 身份验证标签）：

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
注意：类型代码仅供内部使用。Router将保持类型4，并且支持将在router地址中指示。

大小：

| 类型 | 类型码 | X 长度 | 消息 1 长度 | 消息 1 加密长度 | 消息 1 解密长度 | PQ 密钥长度 | 选项长度 |
|------|-----------|-------|-----------|---------------|---------------|------------|---------|
| X25519 | 4 | 32 | 64+pad | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 880+pad | 848 | 816 | 800 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1264+pad | 1232 | 1200 | 1184 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1648+pad | 1616 | 1584 | 1568 | 16 |
注意：类型代码仅供内部使用。Router 将保持类型 4，支持情况将在 router 地址中指示。

#### 2) SessionCreated

原始内容：

未加密数据（未显示 Poly1305 认证标签）：

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
  |   ChaCha20 encrypted data (MLKEM)     |
  -      (see table below for length)     -
  +   k defined in KDF for message 2      +
  |  (before mixKey)                      |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 encrypted data (options)   |
  +         16 bytes                      +
  +   k defined in KDF for message 2      +
  |  (after mixKey)                       |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  +         padding (optional)            +
  |     length defined in options block   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Same as current specification except add a second ChaChaPoly frame
```
尺寸：

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

| 类型 | 类型代码 | Y 长度 | 消息 2 长度 | 消息 2 加密长度 | 消息 2 解密长度 | PQ CT 长度 | opt 长度 |
|------|-----------|-------|-----------|---------------|---------------|-----------|---------|
| X25519 | 4 | 32 | 64+pad | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 848+pad | 816 | 784 | 768 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1168+pad | 1136 | 1104 | 1088 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1648+pad | 1616 | 1584 | 1568 | 16 |
注意：类型代码仅供内部使用。Router 将保持类型 4，支持情况将在 router 地址中指示。

#### 3) SessionConfirmed

未更改

#### 密钥派生函数 (KDF)（用于数据阶段）

未更改

#### 发布地址

在所有情况下，请照常使用 NTCP2 传输名称。

使用与非 PQ、未受防火墙限制时相同的地址/端口。仅支持一种 PQ 变体。在 router 地址中，照常发布 v=2，并发布新参数 pq=[3|4|5] 以表示 MLKEM 512/768/1024。Alice 在会话请求中设置临时密钥的 MSB（key[31] & 0x80），以表明这是一个混合连接。参见上文。较旧的 router 会忽略 pq 参数，并照常以非 pq 方式连接。

防火墙地址（未发布IP）：在 router 地址中，发布 v=2（照常）。无需发布 pq 参数。

Alice可以使用Bob发布的PQ变体连接到PQ Bob，无论Alice是否在她的router信息中宣传pq支持，或者她是否宣传相同的变体。

在当前规范中，消息 1 和消息 2 被定义为具有"合理"数量的填充，建议范围为 0-31 字节，且未指定最大值。

#### 最大填充

在 API 0.9.68（版本 2.11.0）之前，Java I2P 对非 PQ 连接实现了最多 256 字节的填充，但这之前没有被文档化。从 API 0.9.69（版本 2.12.0）开始，Java I2P 对非 PQ 连接实现了与 MLKEM-512 相同的最大填充。请参见下表。

使用定义的消息大小作为最大填充量，也就是说，对于 PQ 连接，最大填充量将使消息大小翻倍，如下所示：

使用已定义的消息大小作为最大填充，即最大填充会使 PQ 连接的消息大小加倍，如下所示：

| 消息最大填充 | non-PQ (到 0.9.68) | non-PQ (从 0.9.69 开始) | MLKEM-512 | MLKEM-768 | MLKEM-1024 |
|---------------------|----------------------|-----------------------|-----------|-----------|------------|
| Session Request  |   256   |   880   |    880   |     1264   |    1648  |
| Session Created  |   256   |   848   |    848   |     1136   |    1616  |
### SSU2

请注意，MLKEM-1024 不支持用于 SSU2，因为密钥过大，无法适配标准的 1500 字节数据报。

#### Noise 标识符

- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"

长头部为 32 字节。它在会话创建之前使用，用于 Token Request、SessionRequest、SessionCreated 和 Retry。它也用于会话外的 Peer Test 和 Hole Punch 消息。

#### 前向保密

在以下消息中，将长头部中的 ver（版本）字段设置为 3 或 4，以指示 MLKEM-512 或 MLKEM-768。

在以下消息中，将长头部中的 ver（版本）字段设置为 2，如往常一样，即使支持 MLKEM-512 或 MLKEM-768。如果对端支持，实现也可以将值设置为 3 或 4，但这不是必需的。实现应该接受任何 2-4 的值。

- (0) 会话请求
- (1) 会话已创建
- (9) 重试
- (10) 令牌请求
- (11) 打洞

未加密数据（未显示 Poly1305 认证标签）：

- (7) 对等测试（会话外消息 5-7）

大小，不包括 IP 开销：

- 中继请求
- 中继响应
- 中继介绍
- 节点测试

注意：类型代码仅供内部使用。Router将保持类型4，支持情况将在router地址中指示。

未改变

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

  ver :: The protocol version = 2, 3, or 4 for non-PQ, MLKEM512, MLKEM768

  id :: 1 byte, the network ID (currently 2, except for test networks)

  flag :: 1 byte, unused, set to 0 for future compatibility

  Source Connection ID :: 8 bytes, unsigned big endian integer

  Token :: 8 bytes, unsigned big endian integer

```
#### 新会话大小

unchanged

#### SessionRequest（类型 0）

用于欺骗保护的KDF更改：为了解决提案165 [Prop165]_ 中提出的问题，但采用不同的解决方案，我们修改了会话请求的KDF。这仅适用于PQ会话。非PQ会话的KDF保持不变。

原始内容：

```

// End of KDF for initial chain key (unchanged)
  // Bob static key
  // MixHash(bpk)
  h = SHA256(h || bpk);

  // Start of KDF for session request
  // NEW for PQ only
  // bhash = Bob router hash (32 bytes)
  // MixHash(bhash)
  h = SHA256(h || bhash);

  // Rest of KDF for session request, unchanged, as in SSU2 spec
  // MixHash(header)
  h = SHA256(h || header)

  ...

```
未加密数据（未显示 Poly1305 认证标签）：

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
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (payload)   |
  +          (length varies)              +
  |  k defined in KDF for Session Request |
  +  n = 1                                +
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
MLKEM768_X25519 的最小 MTU：IPv4 为 1318，IPv6 为 1338。详见下文。

| 类型 | 类型代码 | X 长度 | 消息 1 长度 | 消息 1 加密长度 | 消息 1 解密长度 | PQ 密钥长度 | pl 长度 |
|------|-----------|-------|-----------|---------------|---------------|------------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 896+pl | 832+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1280+pl | 1216+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | n/a | 太大 | | | | |
注意：类型代码仅供内部使用。Router 将保持类型 4，支持情况将在 router 地址中指示。

变更：当前 SSU2 在 ChaCha 部分仅包含块数据。使用 ML-KEM 后，ChaCha 部分还将包含加密的 PQ 公钥。

未加密数据（未显示Poly1305认证标签）：

#### SessionCreated (类型 1)

原始内容：

未加密数据（未显示 Poly1305 认证标签）：

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
  |   ChaCha20 encrypted data (MLKEM)     |
  ~  length varies                        ~
  +  k defined in KDF for Session Created +
  |  (before mixKey)                      |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 encrypted data (payload)   |
  ~  length varies                        ~
  +  k defined in KDF for Session Created +
  |  (after mixKey)                       |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
尺寸：

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

| 类型 | 类型代码 | Y 长度 | Msg 2 长度 | Msg 2 加密长度 | Msg 2 解密长度 | PQ CT 长度 | pl 长度 |
|------|-----------|-------|-----------|---------------|---------------|-----------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 864+pl | 800+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1184+pl | 1120+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | n/a | 过大 | | | | |
注意：类型代码仅供内部使用。Router 将保持类型 4，支持情况将在 router 地址中指示。

变更：当前 SSU2 在 ChaCha 部分仅包含块数据。使用 ML-KEM 后，ChaCha 部分还将包含加密的 PQ 公钥。

PQ 签名：Relay 块、Peer Test 块和 Peer Test 消息都包含签名。不幸的是，PQ 签名大于 MTU。目前没有机制将 Relay 或 Peer Test 块或消息分片到多个 UDP 数据包中。协议必须扩展以支持分片。这将在一个单独的待定提案中完成。在此之前，Relay 和 Peer Test 将不被支持。

#### SessionConfirmed（类型 2）

unchanged

#### 数据阶段的 KDF

unchanged

#### 中继和对等测试

以下数据块包含版本字段。它们将保持版本 2（为了与非 PQ Bob 兼容），并且不会为了 PQ 而更改为版本 3/4。

- SAMv3
- Bittorrent
- 开发者指南
- 命名 / 地址簿 / 跳转服务器
- 其他文档

在所有情况下，照常使用 SSU2 传输名称。不支持 MLKEM-1024。

#### 发布地址

使用与非PQ、非防火墙相同的地址/端口。支持一种或两种PQ变体。在router地址中，发布v=2（如常）和新参数pq=[3|4|3,4|4,3]来表示MLKEM 512/768/两者。MTU小于下方指定最小值的router不得发布包含"4"的"pq"参数。发布4,3表示偏好MLKEM-768，或发布3,4表示偏好MLKEM-512。实际版本由发起方决定，偏好可能不被采用。MTU小于下方指定最小值的router不得使用MLKEM768连接。较旧的router将忽略pq参数并照常进行非pq连接。

使用 MLKEM768 时需谨慎，避免超过 MTU。MLKEM768_X25519 的最小 MTU 对于 IPv4 是 1318，对于 IPv6 是 1338（假设最小负载为 10 字节，包含 DateTime 和 Padding 或 RelayTagRequest 块）。SSU2 的一般最小 MTU 是 1280，因此并非所有对等节点都可以使用 MLKEM768。如果实际 MTU 小于最小值（无论是本地还是对等节点宣告的），请勿发布或使用 MLKEM768。注意不要包含会导致消息 1 或 2 超过本地或远程 MTU 的填充大小。

防火墙后地址（未发布IP）：在router地址中，发布v=2（如往常一样）。防火墙后地址中必须发布pq参数，以支持中继。

Alice 可以使用 Bob 发布的 PQ 变体连接到 PQ Bob，无论 Alice 是否在她的 router 信息中宣传 pq 支持，或者她是否宣传相同的变体。

在当前规范中，消息 1 和消息 2 被定义为具有"合理"数量的填充，建议范围为 0-31 字节，且未指定最大值。

#### MTU

我们可以在内部使用版本字段，对 MLKEM512 使用 3，对 MLKEM768 使用 4。

### 流媒体

对于消息 1 和 2，MLKEM768 会使数据包大小超过 1280 字节的最小 MTU。如果 MTU 过低，可能就不支持该连接。

### SU3 文件

对于消息1和消息2，MLKEM1024会使数据包大小超过1500字节的最大MTU。这将需要对消息1和消息2进行分片，这将是一个很大的复杂问题。可能不会这样做。

中继和对等测试：见上文

TODO: 是否有更高效的方式来定义签名/验证以避免复制签名？

待办事项

[IETF草案](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/)第8.1节禁止在X.509证书中使用HashML-DSA，并且不为HashML-DSA分配OID，这是由于实现复杂性和安全性降低的原因。

### 其他规范

新的最大 Destination 大小将为 2599（Base 64 编码下为 3468）。

请注意，我们不允许对 SU3 文件使用 Ed25519 签名，虽然我们已经定义了 Ed25519ph 签名，但我们从未就其 OID 达成一致，也从未使用过它。

- 如果消息1小于919字节，则使用当前的ratchet协议。
- 如果消息1大于或等于919字节，则可能是MLKEM512_X25519。
  先尝试MLKEM512_X25519，如果失败，则尝试当前的ratchet协议。

## 开销分析

### 密钥交换

SU3 文件不允许使用普通的签名类型；请使用 ph（预哈希）变体。

| 类型 | Pubkey (Msg 1) | Cipertext (Msg 2) |
|------|----------------|-------------------|
| MLKEM512_X25519 | +816 | +784 |
| MLKEM768_X25519 | +1200 | +1104 |
| MLKEM1024_X25519 | +1584 | +1584 |
新的最大 Destination 大小将为 2599（base 64 编码中为 3468）。

更新其他提供 Destination 大小指导的文档，包括：

| 类型 | 相对速度 |
|------|----------------|
| X25519 DH/keygen | 基准 |
| MLKEM512 | 快2.25倍 |
| MLKEM768 | 快1.5倍 |
| MLKEM1024 | 1倍（相同） |
| XK | 4x DH（keygen + 3 DH） |
| MLKEM512_X25519 | 4x DH + 2x PQ（keygen + enc/dec）= 4.9x DH = 慢22% |
| MLKEM768_X25519 | 4x DH + 2x PQ（keygen + enc/dec）= 5.3x DH = 慢32% |
| MLKEM1024_X25519 | 4x DH + 2x PQ（keygen + enc/dec）= 6x DH = 慢50% |
大小增加（字节）：

| 类型 | 相对 DH/encaps | DH/decaps | keygen |
|------|-------------------|-----------|--------|
| X25519 | baseline | baseline | baseline |
| MLKEM512 | 快29倍 | 快22倍 | 快17倍 |
| MLKEM768 | 快17倍 | 快14倍 | 快9倍 |
| MLKEM1024 | 快12倍 | 快10倍 | 快6倍 |
### 签名

#### 尺寸

根据 [Cloudflare](https://blog.cloudflare.com/pq-2024/) 报告的速度：

| 类型 | 公钥 | 签名 | 密钥+签名 | RIdent | Dest | RInfo | LS/Streaming/Datagram (每条消息) |
|------|--------|-----|---------|--------|------|-------|----------------------------------|
| EdDSA_SHA512_Ed25519 | 32 | 64 | 96 | 391 | 391 | 基准 | 基准 |
| MLDSA44 | 1312 | 2420 | 3732 | 1351 | 1319 | +3316 | +3284 |
| MLDSA65 | 1952 | 3309 | 5261 | 1991 | 1959 | +5668 | +5636 |
| MLDSA87 | 2592 | 4627 | 7219 | 2631 | 2599 | +7072 | +7040 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 1344 | 2484 | 3828 | 1383 | 1351 | +3412 | +3380 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 1984 | 3373 | 5357 | 2023 | 1991 | +5668 | +5636 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 2624 | 4691 | 7315 | 2663 | 2631 | +7488 | +7456 |
#### 速度

更新其他提供 Destination 大小指导的文档，包括：

| 类型 | 相对速度符号 | 验证 |
|------|---------------------|--------|
| EdDSA_SHA512_Ed25519 | 基准 | 基准 |
| MLDSA44 | 慢5倍 | 快2倍 |
| MLDSA65 | ??? | ??? |
| MLDSA87 | ??? | ??? |
大小增加（字节）：

| 类型 | 相对签名速度 | 验证 | 密钥生成 |
|------|---------------------|--------|--------|
| EdDSA_SHA512_Ed25519 | 基准 | 基准 | 基准 |
| MLDSA44 | 慢4.6倍 | 快1.7倍 | 快2.6倍 |
| MLDSA65 | 慢8.1倍 | 相同 | 快1.5倍 |
| MLDSA87 | 慢11.1倍 | 慢1.5倍 | 相同 |
## 安全分析

典型的密钥、签名、RIdent、Dest大小或大小增加（包含Ed25519作为参考），假设RI使用X25519加密类型。列出的Router Info、LeaseSet、可回复数据报以及两个流式传输（SYN和SYN ACK）数据包的增加大小。当前的Destinations和Leasesets包含重复填充且在传输中可压缩。新类型不包含填充且不可压缩，导致传输中的大小增加幅度更大。请参阅上述设计部分。

| 类别 | 安全程度相当于 |
|----------|--------------|
| 1 | AES128 |
| 2 | SHA256 |
| 3 | AES192 |
| 4 | SHA384 |
| 5 | AES256 |
### 握手

根据 [Cloudflare](https://blog.cloudflare.com/pq-2024/) 报告的速度：

Java初步测试结果：

| 算法 | 安全类别 |
|-----------|-------------------|
| MLKEM512 | 1 |
| MLKEM768 | 3 |
| MLKEM1024 | 5 |
### 签名

NIST 安全类别在 [NIST presentation](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf) 第 10 页幻灯片中有总结。初步标准：混合协议的最低 NIST 安全类别应为 2，纯 PQ 协议应为 3。

这些都是混合协议。实现应该优先选择 MLKEM768；MLKEM512 的安全性不足。

| 算法 | 安全类别 |
|-----------|-------------------|
| MLDSA44 | 2 |
| MLKEM67 | 3 |
| MLKEM87 | 5 |
## 类型偏好

NIST 安全类别 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)：

本提案定义了混合和纯PQ签名类型。MLDSA44混合类型比MLDSA65纯PQ类型更可取。MLDSA65和MLDSA87的密钥和签名大小对我们来说可能太大了，至少在初期是这样。

NIST 安全类别 [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)：

虽然我们将定义和实现3种加密和9种签名类型，但我们计划在开发过程中测量性能，并进一步分析增加结构大小的影响。我们还将继续研究和监控其他项目和协议的发展。

经过一年或更长时间的开发后，我们将尝试为每个用例确定首选类型或默认设置。选择时需要在带宽、CPU和预估安全级别之间进行权衡。并非所有类型都适合或允许用于所有用例。

初步偏好设置如下，可能会有所变更：

加密算法：MLKEM768_X25519

## 实现说明

### 库支持

签名：MLDSA44_EdDSA_SHA512_Ed25519

初步限制如下，可能会有变更：

### 签名变体

加密：SSU2 不允许使用 MLKEM1024_X25519

签名：MLDSA87 和混合变体可能太大；MLDSA65 和混合变体可能太大

### 可靠性

Bouncycastle、BoringSSL 和 WolfSSL 库现在已支持 MLKEM 和 MLDSA。OpenSSL 的支持将在 2025 年 4 月 8 日发布的 3.5 版本中提供 [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)。

### 结构体大小

Java I2P 采用的 southernstorm.com Noise 库包含了对混合握手的初步支持，但我们将其移除了，因为它未被使用；我们将不得不重新添加它并更新以匹配 [Noise HFS 规范](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf)。

### NetDB

我们将使用"对冲"或随机化签名变体，而非"确定性"变体，如 [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) 第 3.4 节所定义。这确保了每个签名都不相同，即使对相同数据进行签名，并提供了针对侧信道攻击的额外保护。虽然 [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) 规定"对冲"变体是默认选择，但在各种库中这可能成立也可能不成立。实现者必须确保使用"对冲"变体进行签名。

### 棘轮

#### 问题

我们使用正常的签名过程（称为纯 ML-DSA 签名生成），该过程在内部将消息编码为 0x00 || len(ctx) || ctx || message，其中 ctx 是一些大小为 0x00..0xFF 的可选值。我们不使用任何可选上下文。len(ctx) == 0。此过程在 [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) 算法 2 步骤 10 和算法 3 步骤 5 中定义。请注意，一些已发布的测试向量可能需要设置一种模式，其中消息不被编码。

大小增加将导致 NetDB 存储、流式握手和其他消息出现更多的 tunnel 分片。请检查性能和可靠性变化。

- X25519 + MLKEM512
- X25519 + MLKEM768
- X25519 + MLKEM1024

查找并检查任何限制 router info 和 leaseSet 字节大小的代码。

审查并可能减少在RAM或磁盘中存储的最大LS/RI数量，以限制存储增长。提高floodfill的最低带宽要求？

- 多个 MLKEM
- ElG + 一个或多个 MLKEM
- X25519 + 一个或多个 MLKEM
- ElG + X25519 + 一个或多个 MLKEM

基于消息1（新会话消息）的长度检查，应该可以在相同的tunnel上自动分类/检测多种协议。以MLKEM512_X25519为例，消息1的长度比当前ratchet协议大816字节，最小消息1大小（仅包含DateTime负载）为919字节。当前ratchet的大多数消息1大小的负载都小于816字节，因此可以将它们分类为非混合ratchet。大消息可能是POST请求，这种情况比较少见。

- Noise Hash 选择 - 继续使用 SHA256 还是升级？
  SHA256 应该还能再用 20-30 年，不受 PQ 威胁，
  参见 [NIST 演示文稿](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf) 和 [NCCOE 演示文稿](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf)。
  如果 SHA256 被破解，我们还有更严重的问题 (netDb)。
- NTCP2 独立端口，独立 router 地址
- SSU2 中继 / peer 测试
- SSU2 版本字段
- SSU2 router 地址版本

因此推荐的策略是：

这应该允许我们在同一个目的地上有效地支持标准 ratchet 和混合 ratchet，就像我们之前在同一个目的地上支持 ElGamal 和 ratchet 一样。因此，我们可以比不能在同一个目的地支持双协议的情况下更快地迁移到 MLKEM 混合协议，因为我们可以向现有目的地添加 MLKEM 支持。

所需支持的组合包括：

以下组合可能比较复杂，不要求必须支持，但可以根据具体实现来决定是否支持：

#### 共享隧道

我们可能不会尝试在同一个目标上支持多种 MLKEM 算法（例如，MLKEM512_X25519 和 MLKEM_768_X25519）。只选择一种即可；然而，这取决于我们选择一个首选的 MLKEM 变体，这样 HTTP 客户端 tunnel 就可以使用一种。这是实现相关的。

#### 新会话大小

我们可能会尝试在同一个目标上支持三种算法（例如 X25519、MLKEM512_X25519 和 MLKEM769_X25519）。分类和重试策略可能过于复杂。配置和配置界面可能过于复杂。依赖于具体实现。

### NTCP2

我们可能不会尝试在同一个目标上同时支持 ElGamal 和混合算法。ElGamal 已经过时，而且只有 ElGamal + 混合算法（没有 X25519）意义不大。此外，ElGamal 和混合新会话消息都很大，因此分类策略通常必须尝试两种解密方法，这会很低效。这取决于具体实现。

#### 混淆

客户端可以在同一个tunnel上对X25519和混合协议使用相同或不同的X25519静态密钥，这取决于具体实现。

ECIES 规范允许在新会话消息载荷中包含 Garlic Messages，这使得可以进行 0-RTT 传输初始流数据包（通常是 HTTP GET）以及客户端的 leaseSet。然而，新会话消息载荷不具备前向保密性。由于此提案强调增强 ratchet 的前向保密性，实现可能或应该推迟包含流载荷或完整流消息，直到第一个现有会话消息。这将以牺牲 0-RTT 传输为代价。策略也可能取决于流量类型或 tunnel 类型，或者例如 GET 与 POST 的区别。具体取决于实现。

在同一个目的地上使用 MLKEM、MLDSA 或两者都使用，将会如上所述大幅增加新会话消息的大小。这可能会显著降低新会话消息通过 tunnel 传输的可靠性，因为它们必须被分割成多个 1024 字节的 tunnel 消息。传输成功率与片段数量呈指数关系。实现可以使用各种策略来限制消息大小，但会以牺牲 0-RTT 传输为代价。具体取决于实现。

注意：类型代码仅供内部使用。Router 将保持类型 4，支持情况将在 router 地址中指示。

### SSU2

我们在会话请求中设置临时密钥的最高有效位（key[31] & 0x80）来指示这是一个混合连接。这允许我们在同一个端口上同时运行标准 NTCP 和混合 NTCP。只支持一种混合变体，并在 router 地址中进行广告。例如，v=2,3 或 v=2,4 或 v=2,5。

作为 Bob，在去混淆后测试 (X[31] & 0x80) != 0。如果成立，则这是一个 PQ 连接。

注意：类型代码仅供内部使用。Router 将保持类型 4，支持情况将在 router 地址中指示。

## Router 兼容性

### 传输名称

NTCP2-PQ 所需的最低 router 版本待定。

### Router 加密类型

我们使用长标头中的版本字段，对于 MLKEM512 设置为 3，对于 MLKEM768 设置为 4。地址中的 v=2,3,4 就足够了。

#### 混淆

检查并验证 SSU2 是否能够处理跨多个数据包（6-8个？）分片的 MLDSA 签名 RI。

#### Type 5/6/7 Router

注意：类型代码仅供内部使用。Router将保持类型4，支持将在router地址中指示。

#### Type 4 Router

在所有情况下，像往常一样使用 NTCP2 和 SSU2 传输名称。

### Router 签名类型

#### 建议

我们有几个备选方案需要考虑：

不推荐。仅使用上述与 router 类型匹配的新传输协议。旧版 router 无法连接、构建 tunnel 或发送 netDb 消息。需要经过几个发布周期进行调试并确保支持后才能默认启用。相比下面的替代方案，可能会延长推出时间一年或更久。

### LS 加密类型

#### 类型 12-17 Router

推荐。由于PQ不影响X25519静态密钥或N握手协议，我们可以保持router为类型4，只需要广告新的传输协议。较旧的router仍然可以连接、通过其建立tunnel或向其发送netDb消息。

建议在 Ratchet、NTCP2 和 SSU2 中使用 MLKEM-768，因为它在安全性和密钥长度之间提供了最佳平衡。

### 目标签名类型

#### 类型 5-7 LS 密钥

较旧的 router 会验证 RIs，因此无法连接、通过其构建 tunnel 或向其发送 netDb 消息。需要几个发布周期来调试并确保支持后才能默认启用。会遇到与加密类型 5/6/7 推出相同的问题；相比上述列出的类型 4 加密类型推出替代方案，可能会将推出时间延长一年或更长时间。

不推荐。仅使用上述与 router 类型匹配的新传输协议。旧版 router 无法连接、构建 tunnel 或发送 netDb 消息。需要经过几个发布周期进行调试并确保支持后才能默认启用。相比下面的替代方案，可能会延长推出时间一年或更久。

## 优先级和推广

无替代方案。

目标地址可以支持多种密钥类型，但只能通过使用每个密钥对消息1进行试验性解密来实现。可以通过维护每个密钥成功解密的计数，并首先尝试使用最常用的密钥来减轻开销。Java I2P在同一目标地址上对ElGamal+X25519使用这种策略。

Router 会验证 leaseSet 签名，因此无法连接或接收类型 12-17 目标的 leaseSet。需要经过几个发布周期来调试并确保支持，然后才能默认启用。

没有替代方案。

最有价值的数据是端到端流量，使用ratchet加密。作为tunnel跳跃之间的外部观察者，数据会被额外加密两次，分别是tunnel加密和传输加密。作为OBEP和IBGW之间的外部观察者，数据只会被额外加密一次，即传输加密。作为OBEP或IBGW参与者，ratchet是唯一的加密方式。然而，由于tunnel是单向的，要捕获ratchet握手中的两个消息需要串通的router，除非tunnel是在同一个router上构建OBEP和IBGW。

PQ威胁模型中，在某个合理时间段内（比如几个月）破解身份验证密钥，然后冒充身份验证或进行几乎实时解密的威胁，还要更遥远一些？而那时我们才需要迁移到PQC静态密钥。

I2P 中对 MLDSA 签名的支持工作将暂停至 2027 年底或 2028 年，等待标准机构选定算法、可能缩小密钥和/或签名尺寸，并推动行业采用。详见 [CABFORUM](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/)、[COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/) 和 [PLANTS](https://datatracker.ietf.org/wg/plants/about/)。此外，MLDSA 在行业中的采用将由 IETF、CA/浏览器论坛（CA/Browser Forum）和证书颁发机构（CA）进行标准化。CA 首先需要硬件安全模块（HSM）的支持，而目前尚不可用 [CA/Browser Forum](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/)。我们预计 IETF 和 CA/浏览器论坛将主导关于具体参数选择的决策，包括是否支持或要求使用复合签名 [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/)。

| 里程碑 | 目标时间 |
|-----------|--------|
| Ratchet beta | 2025年末 |
| 选择最佳加密类型 | 2026年初 |
| NTCP2 beta | 2026年初 |
| SSU2 beta | 2026年中 |
| Ratchet 生产版 | 2026年中 |
| Ratchet 默认 | 2026年末 |
| 签名 beta | 2026年末 |
| NTCP2 生产版 | 2026年末 |
| SSU2 生产版 | 2027年初 |
| 选择最佳签名类型 | 2027年初 |
| NTCP2 默认 | 2027年初 |
| SSU2 默认 | 2027年中 |
| 签名生产版 | 2027年中 |
## 迁移

Ratchet 是最高优先级。传输协议是次要的。签名是最低优先级。

签名推出也将比加密推出晚一年或更长时间，因为无法实现向后兼容性。此外，MLDSA在行业中的采用将由CA/Browser Forum和证书颁发机构进行标准化。CA首先需要硬件安全模块(HSM)支持，但目前尚不可用[CA/Browser Forum](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/)。我们期望CA/Browser Forum推动关于特定参数选择的决策，包括是否支持或要求复合签名[IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/)。

## 问题

SHA256 应该在未来 20-30 年内仍然安全，不会受到后量子计算（PQ）的威胁，参见 [NIST 演示文稿](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf) 和 [NCCOE 演示文稿](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf)。如果 SHA256 被攻破，我们将面临更严重的问题（例如 netDb）。

## 参考资料

* [CABFORUM](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/)
* [Choosing-Hash](https://kerkour.com/fast-secure-hash-function-sha256-sha512-sha3-blake3)
* [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/)
* [COMMON](/docs/specs/common-structures/)
* [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/)
* [ECIES](/docs/specs/ecies/)
* [FORUM](http://zzz.i2p/topics/3294)
* [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
* [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
* [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)
* [FIPS205](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.205.pdf)
* [MLDSA-OIDS](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/)
* [NIST-PQ](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards)
* [NIST-PQ-UPDATE](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf)
* [NIST-PQ-END](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf)
* [NIST-VECTORS](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values)
* [Noise](https://noiseprotocol.org/noise.html)
* [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf)
* [NSA-PQ](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF)
* [NTCP2](/docs/specs/ntcp2/)
* [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)
* [Prop165](/docs/proposals/165/)
* [PQ-WIREGUARD](https://eprint.iacr.org/2020/379.pdf)
* [RFC-2104](https://tools.ietf.org/html/rfc2104)
* [Rosenpass](https://rosenpass.eu/)
* [Rosenpass-Whitepaper](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf)
* [SSH-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-sshm-mlkem-hybrid-kex/)
* [SSU2](/docs/specs/ssu2/)
* [TLS-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-tls-hybrid-design/)
