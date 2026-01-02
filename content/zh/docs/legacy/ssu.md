---
title: "SSU (旧版)"
description: "最初的 Secure Semireliable UDP 传输"
slug: "ssu"
lastUpdated: "2025-01"
accurateFor: "0.9.64"
reviewStatus: "needs-review"
---

> **已弃用：** SSU 已被 SSU2（第二代 SSU 协议）取代。在 i2pd 2.44.0（API 0.9.56，2022 年 11 月）以及 Java I2P 2.4.0（API 0.9.61，2023 年 12 月）中已移除对 SSU 的支持。

SSU 提供了基于 UDP、带有拥塞控制、NAT 穿越以及对 introducer（引荐者）支持的半可靠传输。它通过为位于 NAT/防火墙之后的 routers 提供支持并协调进行 IP 发现，与 NTCP 形成互补。

## 地址元素

- `transport`: `SSU`
- `caps`: 能力标志 (`B`, `C`, `4`, `6` 等)
- `host` / `port`: IPv4 或 IPv6 监听（当被防火墙阻挡时可选）
- `key`: Base64 引入密钥
- `mtu`: 可选；默认 1484 (IPv4) / 1488 (IPv6)
- `ihost/ikey/iport/itag/iexp`: 当 router 被防火墙阻挡时的 introducer（引入者）条目

## 功能

- 使用 introducers（引介者）的协作式 NAT 穿越
- 通过对等节点测试和检查入站数据包来检测本地 IP
- 自动将防火墙状态中继到其他传输和 router 控制台
- 半可靠传递：消息在达到重传上限后被丢弃
- 使用加性增加/乘性减少和分片 ACK 位字段的拥塞控制

SSU 还处理元数据任务，如定时信标和 MTU 协商。所有功能现由 [SSU2](/docs/specs/ssu2/) 提供（采用现代密码学）。
