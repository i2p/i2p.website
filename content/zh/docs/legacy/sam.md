---
title: "SAM v1"
description: "旧版 Simple Anonymous Messaging（简单匿名消息传递）协议（已弃用）"
slug: "sam"
lastUpdated: "2025-03"
accurateFor: "0.9.20"
reviewStatus: "needs-review"
---

> **已弃用：** SAM v1 仅保留用于历史参考。新应用应使用 [SAM v3](/docs/api/samv3/) 或 [BOB](/docs/legacy/bob/)。原始桥接程序仅支持 DSA-SHA1 Destination（目标地址）以及有限的选项集。

## 库

Java I2P 源代码树仍包含面向 C、C#、Perl 和 Python 的遗留绑定。它们已不再维护，主要为了归档兼容性而随发行版提供。

## 版本协商

客户端通过 TCP（默认 `127.0.0.1:7656`）连接并交换：

```
Client → HELLO VERSION MIN=1 MAX=1
Bridge → HELLO REPLY RESULT=OK VERSION=1.0
```
自 Java I2P 0.9.14 起，`MIN` 参数是可选的，并且 `MIN`/`MAX` 都接受一位数字形式（`"3"` 等），适用于已升级的桥接。

## 会话创建

```
SESSION CREATE STYLE={STREAM|DATAGRAM|RAW} DESTINATION={name|TRANSIENT} [DIRECTION={BOTH|RECEIVE|CREATE}] [option=value]*
```
- `DESTINATION=name` 会在 `sam.keys` 中加载或创建一个条目；`TRANSIENT` 始终创建一个临时 Destination（目标地址）。
- `STYLE` 用于选择虚拟流（类似 TCP）、签名数据报，或原始数据报。
- `DIRECTION` 仅适用于流会话；默认为 `BOTH`。
- 其他键/值对将作为 I2CP 选项传递（例如，`tunnels.quantityInbound=3`）。

网桥回复：

```
SESSION STATUS RESULT=OK DESTINATION=name
```
失败会返回 `DUPLICATED_DEST`、`I2P_ERROR` 或 `INVALID_KEY`，并可附带一条可选消息。

## 消息格式

SAM 消息为单行 ASCII，由以空格分隔的键/值对组成。键使用 UTF‑8 编码；如果值包含空格，可以用引号括起。未定义任何转义。

通信类型：

- **流** – 通过 I2P streaming library（I2P 的流式传输库）代理
- **可回复数据报** – 已签名的负载 (Datagram1)
- **原始数据报** – 未签名的负载 (Datagram RAW)

## 0.9.14 版本新增的选项

- `DEST GENERATE` 接受 `SIGNATURE_TYPE=...`（允许使用 Ed25519 等）
- `HELLO VERSION` 将 `MIN` 视为可选，并接受一位数的版本字符串

## 何时使用 SAM v1

仅在需要与无法更新的遗留软件互操作时使用。对于所有新的开发，请使用：

- [SAM v3](/docs/api/samv3/) 用于功能完备的流/数据报访问
- [BOB](/docs/legacy/bob/) 用于 Destination（目的地）管理（仍然有限，但支持更现代的功能）

## 参考资料

- [SAM v2](/docs/legacy/samv2/)
- [SAM v3](/docs/api/samv3/)
- [数据报规范](/docs/api/datagrams/)
- [流式协议](/docs/specs/streaming/)

SAM v1 为与 router 无关的应用开发奠定了基础，但生态系统已经向前发展了。请将本文档视为兼容性参考，而非起点。
