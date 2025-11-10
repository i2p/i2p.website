---
title: "研究亮点"
date: 2019-10-25
author: "Hoàng Nguyên Phong"
description: "I2P 匿名网络及其抗审查性的实证研究"
categories: ["community"]
---

## 研究聚焦 - 对 I2P 匿名网络及其抗审查性的实证研究

以下博文由 Information Controls Fellow Hoàng Nguyên Phong 撰写。作为 ICFP 研究员，Phong 的研究聚焦于分析 I2P 网络的不同方面；I2P 是一种隐私增强型互联网工具，可通过匿名增强型网络访问在线内容，有助于规避国家施加的审查。与其接收机构马萨诸塞大学阿默斯特分校合作，Phong 研究了 I2P 网络的抗审查能力，其中包括识别国家审查者可能用来阻止访问 I2P 的封锁方法，并探讨使 I2P 更能抵御此类封锁的潜在解决方案。

Phong 发现 I2P 网络上存在封锁尝试（具体通过 DNS 污染、基于 SNI 的封锁、TCP 数据包注入以及针对特定页面的封锁），这些封锁来自五个国家：中国、阿曼、卡塔尔、伊朗和科威特。Phong 认为，由于封锁通常施加在 I2P 下载页面和 reseed 服务器（引导节点服务器）上，可以通过将这些内容的下载链接托管在大型云服务提供商上来缓解此类封锁，从而提高封锁的连带成本。Phong 还为该平台构建了一个指标门户，便于研究人员等更好地了解 I2P 的使用者，并发现该网络日均约有 20,000 个中继节点。

（摘自 OTF 博客文章）

- [Original Blog Post](https://homepage.np-tokumei.net/post/notes-otf-wrapup-blogpost/)
- [OTF Mirror of the Blog Post](https://www.opentech.fund/news/empirical-study-i2p-anonymity-network-and-its-censorship-resistance/)
- [I2P Metrics Portal](https://i2p-metrics.np-tokumei.net/)

该研究论文也可在此处获取:

- [Research Paper](https://www.researchgate.net/publication/327445307_An_Empirical_Study_of_the_I2P_Anonymity_Network_and_its_Censorship_Resistance)

在我们着手解决已识别的问题之际，我们感谢 Phong 及其合作者所做的出色研究。看到越来越多关于 I2P 的学术研究令人振奋，我们也很期待继续与他合作。
