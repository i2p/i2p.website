---
title: "ECIES-P256"
number: "145"
author: "orignal"
created: "2019-01-23"
lastupdated: "2019-01-24"
status: "Open"
thread: "http://zzz.i2p/topics/2418"
---

## 动机

ECIES-P256 比 ElGamal 快得多。已经有一些使用 ECIES-P256 加密类型的 i2pd eepsites，Java 应该能够与它们进行通信，反之亦然。自 2.16.0 (0.9.32 Java) 版本起，i2pd 已支持该类型。

## 概述

此提案引入了一种新的加密类型 ECIES-P256，可以出现在身份认证的证书部分，或作为 LeaseSet2 中的单独加密密钥类型。可以在 RouterInfo、LeaseSet1 和 LeaseSet2 中使用。

### ElGamal 密钥位置

回顾一下，
ElGamal 256 字节的公钥可以在以下数据结构中找到。
请参阅通用结构规范。

- 在路由器身份中
  这是路由器的加密密钥。

- 在目标中
  目标的公钥用于旧版的 i2cp-to-i2cp 加密，其在版本 0.6 中被禁用，目前未使用，除了用于 LeaseSet 加密的 IV，该功能已被弃用。
  LeaseSet 中使用了公钥。

- 在 LeaseSet 中
  这是目标的加密密钥。

在上述 3 种情况下，ECIES 公钥仍然占用 256 字节，尽管实际密钥长度为 64 字节。
其余部分必须用随机填充填充。

- 在 LS2 中
  这是目标的加密密钥。密钥大小为 64 字节。

### Key Certs 中的 EncTypes

ECIES-P256 使用加密类型 1。
加密类型 2 和 3 应保留用于 ECIES-P284 和 ECIES-P521。

### 非对称加密用途

本提案描述了 ElGamal 的替换方案:

1) 隧道构建消息 (密钥在 RouterIdentity 中)。ElGamal 块为 512 字节
  
2) 客户端到客户端的 ElGamal+AES/SessionTag (密钥在 LeaseSet 中，目标密钥未使用)。ElGamal 块为 514 字节

3) 路由器到路由器的 netdb 和其他 I2NP 消息的加密。ElGamal 块为 514 字节

### 目标

- 向后兼容
- 不更改现有数据结构
- 比 ElGamal 更具 CPU 效率

### 非目标

- RouterInfo 和 LeaseSet1 无法同时发布 ElGamal 和 ECIES-P256

### 理由

ElGamal/AES+SessionTag 引擎总是由于标签不足而卡住，导致 I2P 通信性能显著下降。
隧道构建是最繁重的操作，因为发起者每个隧道构建请求必须运行 3 次 ElGamal 加密。

## 所需的密码学基础

1) EC P256 曲线密钥生成和 DH

2) AES-CBC-256

3) SHA256

## 详细提案

使用 ECIES-P256 的目标以证书中的加密类型 1 发布自身。
身份中的 256 字节的前 64 字节应被解释为 ECIES 公钥，其余部分应被忽略。
LeaseSet 的单独加密密钥基于身份中的密钥类型。

### 针对 ElGamal/AES+SessionTags 的 ECIES 块

ECIES 块替换 ElGamal 块用于 ElGamal/AES+SessionTags。长度为 514 字节。
由两部分组成，每部分 257 字节。
第一部分以零开始，然后是 64 字节的 P256 瞬时公钥，其余 192 字节为随机填充。
第二部分以零开始，然后是 AES-CBC-256 加密的 256 字节，其内容与 ElGamal 相同。

### 隧道构建记录的 ECIES 块

隧道构建记录相同，但块中没有前导零。
一个隧道可以通过任何路由器的加密类型组合而成，并且是每个记录单独执行。
隧道的发起者根据隧道参与者发布的加密类型加密记录，隧道参与者根据自己的加密类型解密。

### AES-CBC-256 密钥

这是 ECDH 共享密钥的计算，其中 KDF 是 x 坐标上的 SHA256。
假设 Alice 是加密者，Bob 是解密者。
设 k 是 Alice 随机选择的瞬时 P256 私钥，P 是 Bob 的公钥。
S 是共享密钥 S(Sx, Sy)
Alice 通过用 P "协商" k 来计算 S，例如 S = k*P。

假设 K 是 Alice 的瞬时公钥，p 是 Bob 的私钥。
Bob 从接收消息的第一个块中取得 K 并计算 S = p*K

AES 加密密钥是 SHA256(Sx)，iv 是 Sy。
