---
title: "多播"
number: "101"
author: "zzz"
created: "2008-12-08"
lastupdated: "2009-03-25"
status: "终止"
thread: "http://zzz.i2p/topics/172"
---

## 概述

基本想法：通过你的出站通道发送一个副本，出站端点分发到所有的入站网关。端到端加密被排除。

## 设计

- 新的多播通道消息类型（传递类型=0x03）
- 出站端点多播分发
- 新的 I2NP 多播消息类型？
- 新的 I2CP 多播发送消息类型
- 在 OutNetMessageOneShotJob 中不加密路由器到路由器（大蒜？）

应用程序：

- RTSP 代理？

Streamr：

- 调整 MTU？还是只在应用程序中进行？
- 按需接收和传输
