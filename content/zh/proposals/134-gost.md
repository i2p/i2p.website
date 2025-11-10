---
title: "GOST Sig 类型"
number: "134"
author: "orignal"
created: "2017-02-18"
lastupdated: "2017-03-31"
status: "开放"
thread: "http://zzz.i2p/topics/2239"
---

## 概述

GOST R 34.10 椭圆曲线签名被俄罗斯的政府和企业使用。支持它可以简化现有应用程序（通常基于 CryptoPro）的集成。哈希函数为 32 或 64 字节的 GOST R 34.11。基本上，它与 EcDSA 的工作原理相同，签名和公钥的大小为 64 或 128 字节。

## 动机

椭圆曲线加密从未被完全信任，并产生了许多关于可能存在后门的猜测。因此，没有一种签名类型可以被所有人完全信任。增加一种签名类型将为人们提供更多选择，信任他们的选择。

## 设计

GOST R 34.10 使用标准椭圆曲线，具有自己的参数集。现有群体的数学可以重用。但是签名和验证是不同的，必须实现。参见 RFC: https://www.rfc-editor.org/rfc/rfc7091.txt GOST R 34.10 应与 GOST R 34.11 哈希一起工作。我们将使用 GOST R 34.10-2012（也称为 steebog），无论是 256 位还是 512 位。参见 RFC: https://tools.ietf.org/html/rfc6986

GOST R 34.10 没有指定参数，但有一些大家都在使用的好参数集。带有 64 字节公钥的 GOST R 34.10-2012 继承了 GOST R 34.10-2001 的 CryptoPro 参数集。参见 RFC: https://tools.ietf.org/html/rfc4357

然而，新的 128 字节密钥参数集由专门的技术委员会 tc26（tc26.ru）创建。参见 RFC: https://www.rfc-editor.org/rfc/rfc7836.txt

i2pd 中基于 Openssl 的实现显示它比 P256 更快，但比 25519 慢。

## 规格

只支持 GOST R 34.10-2012 和 GOST R 34.11-2012。两种新的签名类型： 9 - GOSTR3410_GOSTR3411_256_CRYPTO_PRO_A 代表公钥和签名类型为 64 字节，哈希大小为 32 字节，参数集为 CryptoProA（也称为 CryptoProXchA） 10 - GOSTR3410_GOSTR3411_512_TC26_A 代表公钥和签名类型为 128 字节，哈希大小为 64 字节，参数集来自 TC26。

## 迁移

这些签名类型应仅用作可选签名类型。不需要迁移。i2pd 已经支持它了。
