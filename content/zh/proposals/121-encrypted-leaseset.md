---
title: "加密的 LeaseSet"
number: "121"
author: "zzz"
created: "2016-01-11"
lastupdated: "2016-01-12"
status: "Rejected"
thread: "http://zzz.i2p/topics/2047"
supercededby: "123"
---

## 概述

本提案旨在重新设计加密 LeaseSet 的机制。

## 动机

当前的加密 LS 既糟糕又不安全。作为设计和实现者，我可以这么说。

原因：

- AES CBC 加密
- 所有人共享一个 AES 密钥
- 租约到期信息仍然暴露
- 加密公钥仍然暴露

## 设计

### 目标

- 使整个过程不透明
- 为每个接收者提供密钥

### 策略

仿效 GPG/OpenPGP 的方式。用非对称加密为每个接收者加密一个对称密钥。数据用该非对称密钥解密。参见例如 [RFC-4880-S5.1]_
如果我们能找到一个小而快的算法。

关键是找到一个小而快的非对称加密。ElGamal 在 514 字节处有点痛苦。我们可以做得更好。

参见例如 http://security.stackexchange.com/questions/824...

这适用于少量接收者（或实际上是密钥；如果你愿意，你仍然可以将密钥分发给多个人）。

## 规格

- 目的地
- 发布时间戳
- 到期
- 标记
- 数据长度
- 加密数据
- 签名

加密数据可以加上某种 enctype 指示符，也可以没有。

## 参考资料

.. [RFC-4880-S5.1]
    https://tools.ietf.org/html/rfc4880#section-5.1
