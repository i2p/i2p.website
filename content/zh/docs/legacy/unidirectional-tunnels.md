---
title: "单向 Tunnels"
description: "I2P 的单向 tunnel 设计的历史概述。"
slug: "unidirectional"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

> **历史说明：** 本页保留了旧版“Unidirectional Tunnels（单向隧道）”讨论，供参考。有关当前行为，请参阅现行的 [tunnel 实现文档](/docs/specs/implementation/)。

## 概述

I2P 构建 **单向的 tunnels**：一个 tunnel 承载出站流量，另一个独立的 tunnel 承载入站回复。这种结构可追溯至最早的网络设计，并且至今仍是与像 Tor 这样的双向电路系统相区别的关键特征。有关术语和实现细节，请参见 [tunnel 概览](/docs/overview/tunnel-routing/) 和 [tunnel 规范](/docs/specs/implementation/)。

## 回顾

- 单向 tunnel 将请求与响应流量分离，因此任何一组串通的对等节点只能观察到往返路径的一半。
- 时序攻击必须同时交叉两个 tunnel 池（出站和入站），而不是分析单一的电路，从而提高关联分析的难度。
- 独立的入站和出站池使 routers 能够按方向调整延迟、容量及故障处理特性。
- 缺点包括对等节点管理复杂性增加，以及为确保服务可靠交付而需要维护多个 tunnel 集合。

## 匿名性

Hermann 和 Grothoff 的论文，[*I2P is Slow… and What to Do About It*](http://grothoff.org/christian/i2p.pdf)，分析了针对单向 tunnels 的前驱攻击，指出有决心的对手最终可以确认长期在线的对等节点。社区反馈指出，该研究依赖于关于对手耐心和法律权力的特定假设，且没有将该方法与会影响双向设计的时序攻击进行权衡比较。持续的研究与实践经验不断强化了这样一种认识：单向 tunnels 是出于匿名性考量的有意选择，而非疏忽所致。
