---
title: "SAM v2（Simple Anonymous Messaging，I2P 的简单匿名消息接口）"
description: "遗留版简单匿名消息传递协议"
slug: "samv2"
lastUpdated: "2025-03"
accurateFor: "0.9.20"
reviewStatus: "needs-review"
---

> **已弃用：** 随 I2P 0.6.1.31 一同发布的 SAM v2 已不再维护。新开发请使用 [SAM v3](/docs/api/samv3/)。v2 相比 v1 的唯一改进是支持在单个 SAM 连接上复用多个套接字。

## 版本说明

- 上报的版本字符串仍为 `"2.0"`。
- 自 0.9.14 起，`HELLO VERSION` 消息接受一位数的 `MIN`/`MAX` 值，并且 `MIN` 参数是可选的。
- `DEST GENERATE` 支持 `SIGNATURE_TYPE`，因此可以创建 Ed25519（椭圆曲线签名算法）目的地。

## 会话基础

```
SESSION CREATE STYLE={STREAM|DATAGRAM|RAW} DESTINATION={name|TRANSIENT} [DIRECTION={BOTH|RECEIVE|CREATE}] [option=value]
```
- 每个 Destination（I2P 目标标识）只能有一个活动的 SAM 会话（streams、datagrams 或 raw）。
- `STYLE` 用于选择虚拟流、已签名的数据报，或原始数据报。
- 其他选项会传递给 I2CP（例如，`tunnels.quantityInbound=3`）。
- 响应与 v1 相同：`SESSION STATUS RESULT=OK|DUPLICATED_DEST|I2P_ERROR|INVALID_KEY`。

## 消息编码

按行组织的 ASCII，使用空格分隔的 `key=value` 键值对（值可以用引号括起）。通信类型与 v1 相同：

- 通过 I2P streaming library (I2P 流式传输库) 提供的流
- 可回复数据报 (`PROTO_DATAGRAM`)
- 原始数据报 (`PROTO_DATAGRAM_RAW`)

## 何时使用

仅适用于无法迁移的遗留客户端。SAM v3 提供：

- 二进制目标地址交接 (`DEST GENERATE BASE64`)
- 子会话与 DHT 支持 (v3.3)
- 更好的错误报告和选项协商

参见：

- [SAM v1](/docs/legacy/sam/)
- [SAM v3](/docs/api/samv3/)
- [数据报 API](/docs/api/datagrams/)
- [流式协议](/docs/specs/streaming/)
