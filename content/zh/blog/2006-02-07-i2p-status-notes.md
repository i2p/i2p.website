---
title: "I2P 2006-02-07 状态说明"
date: 2006-02-07
author: "jr"
description: "PRE 网络测试进展、针对 ElGamal 加密的短指数优化，以及支持 gwebcache 的 I2Phex 0.1.1.37"
categories: ["status"]
---

嗨，大家好，星期二又到了

* Index

1) 网络状态 2) _PRE 网络进度 3) I2Phex 0.1.1.37 4) ???

* 1) Net status

过去一周主网没有出现任何实质性变化，因此主网状态也几乎没有变化。另一方面……

* 2) _PRE net progress

上周，我开始将用于 0.6.1.10 版本的向后不兼容代码提交到 CVS 中的一个单独分支（i2p_0_6_1_10_PRE），并且一批志愿者帮助进行了测试。这个新的 _PRE 网络无法与现网通信，并且几乎没有任何有意义的匿名性（因为节点少于 10 个）。借助那些 routers 的 pen register（拨号记录器）日志，我们已经在新旧代码中定位并修复了几处较为严重的缺陷，不过进一步的测试和改进仍在进行中。

新的 tunnel 创建加密方案的一个方面是，创建者必须在一开始就为每个跳（hop）执行计算开销很大的非对称加密，而旧的 tunnel 创建方式只有在前一跳同意参与该 tunnel 时才进行加密。该加密可能需要 400-1000ms 甚至更多，具体取决于本地 CPU 性能以及 tunnel 的长度（它对每一跳都进行完整的 ElGamal 加密）。目前在 _PRE net 上使用的一项优化是采用短指数 [1] - 我们不再使用 2048bit 的 'x' 作为 ElGamal 密钥，而是使用 228bit 的 'x'，这是为与离散对数问题的计算工作量相匹配而建议的长度。这样将每跳加密时间降低了一个数量级，但并不影响解密时间。

关于使用短指数存在许多相互矛盾的观点，在一般情况下它并不安全；不过据我目前所了解，鉴于我们使用的是固定的安全素数（Oakley group 14 [2]），q 的阶应该没有问题。如果有人对此还有进一步的看法，我很乐意听到更多。

一个主要的替代方案是切换到 1024 位加密（这样我们或许就可以使用 160 位的短指数）。无论如何，这可能都是合适的；如果在 _PRE net（预发布网络）上使用 2048 位加密过于吃力，我们可能会在 _PRE net 内进行切换。否则，我们可能会等到 0.6.1.10 发布版，等新的加密方案更广泛地部署后，再评估是否有必要。如果看起来可能进行这样的切换，我们将提供更多信息。

[1] "关于使用短指数的 Diffie-Hellman 密钥协商" -     van Oorschot、Weiner 于 EuroCrypt 96。  镜像位于     http://dev.i2p.net/~jrandom/Euro96-DH.ps [2] http://www.ietf.org/rfc/rfc3526.txt

无论如何，_PRE net 上已经取得了大量进展，关于它的大部分交流都是在 irc2p 上的 #i2p_pre 频道中进行的。

* 3) I2Phex 0.1.1.37

Complication 已合并并修补了最新的 I2Phex 代码，以支持 gwebcaches（Gnutella Web 缓存），并与 Rawn 的 pycache 移植版兼容。这意味着用户可以下载 I2Phex，安装后点击 "Connect to the network"，一两分钟后，它会获取一些现有 I2Phex 节点的引用信息并连上网络。再也不用手动管理 i2phex.hosts 文件，或手动共享密钥了（太棒了）！默认提供两个 gwebcaches，但也可以通过修改 i2phex.cfg 中的 i2pGWebCache0、i2pGWebCache1 或 i2pGWebCache2 属性来更改，或者添加第三个。

干得好，Complication 和 Rawn！

* 4) ???

暂时就这些，这也挺好，因为我开会已经迟到了 :)  待会儿在 #i2p 见大家

=jr
