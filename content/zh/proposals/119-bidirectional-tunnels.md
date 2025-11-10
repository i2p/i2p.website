---
title: "双向隧道"
number: "119"
author: "orignal"
created: "2016-01-07"
lastupdated: "2016-01-07"
status: "需要研究"
thread: "http://zzz.i2p/topics/2041"
---

## 概述

本提案旨在于 I2P 中实现双向隧道。


## 动机

i2pd 计划引入仅通过其他 i2pd 路由器构建的双向隧道。目前，对于网络而言，这将看起来像是常规的入站和出站隧道。


## 设计

### 目标

1. 通过减少 TunnelBuild 消息的数量来降低网络和 CPU 使用。
2. 能够即时知道参与者是否已经离开。
3. 更精确的分析和统计。
4. 使用其他暗网作为中间对等节点。


### 隧道修改

隧道构建
```````````
隧道的构建方式与入站隧道相同。不需要回复消息。有一种特殊类型的参与者称为“入口”，并由标志标记，同时作为 IBGW 和 OBEP。消息的格式与 VaribaleTunnelBuild 相同，但 ClearText 包含不同的字段：

	in_tunnel_id
	out_tunnel_id
	in_next_tunnel_id
	out_next_tunnel_id
	in_next_ident
	out_next_ident
	layer_key, iv_key

它还将包含一个字段，说明下一个对等节点所在的暗网，并提供一些额外的信息，如果它不是 I2P。

隧道终止
`````````````````
如果对等节点想要离开，它创建一个用层密钥加密的 TunnelTermination 消息，并在“入”方向发送。如果一个参与者收到这样的消息，它将其用自己的层密钥加密，并发送给下一个对等节点。一旦消息到达隧道所有者，它开始逐个对等节点解密，直到获得未加密的消息。它会发现哪个对等节点已经离开，并终止隧道。
