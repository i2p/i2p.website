---
title: "ECDSA密钥遮蔽"
number: "151"
author: "orignal"
created: "2019-05-21"
lastupdated: "2019-05-29"
status: "Open"
thread: "http://zzz.i2p/topics/2717"
toc: true
---

## 动机

有些人不喜欢EdDSA或RedDSA。我们应该提供一些替代方案，让他们能够遮蔽ECDSA签名。

## 概述

这个提案描述了针对ECDSA签名类型1, 2, 3的密钥遮蔽。

## 提案

工作方式与RedDSA相同，但一切都是大端序。
只允许相同的签名类型，例如1->1, 2->2, 3->3。

### 定义

B
    曲线的基点

L
   椭圆曲线的群阶。曲线的属性。

DERIVE_PUBLIC(a)
    通过在椭圆曲线上乘以B将私钥转换为公钥

alpha
    对目的地知晓者已知的32字节随机数。

GENERATE_ALPHA(destination, date, secret)
    为当前日期生成alpha，适用于了解目的地和秘密的人。

a
    用于签署目的地的未遮蔽32字节签名私钥

A
    目标中的未遮蔽32字节签名公钥，
    = DERIVE_PUBLIC(a)，与相应曲线一致

a'
    用于签署加密租赁集的被遮蔽32字节签名私钥
    这是一个有效的ECDSA私钥。

A'
    目标中被遮蔽的32字节ECDSA签名公钥，
    可以通过DERIVE_PUBLIC(a')生成，或从A和alpha生成。
    这是曲线上的有效ECDSA公钥

H(p, d)
    采用个性化字符串p和数据d的SHA-256哈希函数，并生成长度为32字节的输出。

    使用SHA-256如下::

        H(p, d) := SHA-256(p || d)

HKDF(salt, ikm, info, n)
    一种密码学密钥派生函数，接受一些输入密钥材料ikm（应具有良好的熵，但不要求是均匀随机字符串），
    长度为32字节的salt和特定上下文的'info'值，生成适合用作密钥材料的n字节输出。

    按[RFC-5869](https://tools.ietf.org/html/rfc5869)中规定使用HKDF，并使用[RFC-2104](https://tools.ietf.org/html/rfc2104)中规定的HMAC哈希函数SHA-256。
    这意味着SALT_LEN最大为32字节。


### 遮蔽计算

每天（UTC）必须生成一个新的秘密alpha和被遮蔽密钥。
秘密alpha和被遮蔽密钥的计算如下。

生成alpha(destination, date, secret)，对所有相关方：

```text
// GENERATE_ALPHA(destination, date, secret)

  // secret是可选的，否则为空
  A = 目标的签名公钥
  stA = A的签名类型，2字节大端序（0x0001, 0x0002或0x0003）
  stA' = 被遮蔽公钥A'的签名类型，2字节大端序，总是与stA相同
  keydata = A || stA || stA'
  datestring = 当前日期的8字节ASCII YYYYMMDD
  secret = UTF-8编码字符串
  seed = HKDF(H("I2PGenerateAlpha", keydata), datestring || secret, "i2pblinding1", 64)
  // 将seed视为64字节大端值
  alpha = seed mod L
```


BLIND_PRIVKEY()，供发布租赁集的所有者使用：

```text
// BLIND_PRIVKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  a = 目标的签名私钥
  // 使用标量算术进行加法
  被遮蔽的签名私钥 = a' = BLIND_PRIVKEY(a, alpha) = (a + alpha) mod L
  被遮蔽的签名公钥 = A' = DERIVE_PUBLIC(a')
```


BLIND_PUBKEY()，供检索租赁集的用户使用：

```text
// BLIND_PUBKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  A = 目标的签名公钥
  // 使用群元素（曲线上的点）进行加法
  被遮蔽的公钥 = A' = BLIND_PUBKEY(A, alpha) = A + DERIVE_PUBLIC(alpha)
```


计算A'的两种方法都产生相同的结果，这是必要的。

## b33地址

ECDSA的公钥是(X,Y)对，因此对于P256，例如，它是64字节，而不是RedDSA的32字节。
因此，b33地址将更长，或者公钥可以像比特币钱包中那样以压缩格式存储。


## 参考文献

* [RFC-2104](https://tools.ietf.org/html/rfc2104)
* [RFC-5869](https://tools.ietf.org/html/rfc5869)
