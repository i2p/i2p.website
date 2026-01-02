---
title: "v3dgsend"
description: "用于通过 SAM v3 发送 I2P 数据报的命令行工具"
slug: "v3dgsend"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

> 状态：这是 `v3dgsend` 工具的简明参考。它是对 [数据报 API](/docs/api/datagrams/) 和 [SAM v3](/docs/api/samv3/) 文档的补充。

## 概述

`v3dgsend` 是一个命令行辅助工具,用于通过 SAM v3 接口发送 I2P 数据报。它适用于测试数据报传递、服务原型设计,以及在无需编写完整客户端的情况下验证端到端行为。

典型用途包括：

- 对目标地址进行数据报可达性冒烟测试
- 验证防火墙和地址簿配置
- 试验原始数据报与签名（可回复）数据报

## 使用方法

基本调用方式因平台和打包方式而异。常见选项包括：

- Destination: base64 Destination 或 `.i2p` 名称
- Protocol: raw (PROTOCOL 18) 或 signed (PROTOCOL 17)
- Payload: 内联字符串或文件输入

请参考您的发行版包管理或 `--help` 输出以获取确切的标志。

## 另请参阅

- [Datagram API](/docs/api/datagrams/)
- [SAM v3](/docs/api/samv3/)
- [Streaming Library](/docs/api/streaming/) (datagram 的替代方案)
