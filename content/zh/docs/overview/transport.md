---
title: "传输概述"
description: "I2P点对点router通信传输层概述"
slug: "transport"
aliases:
  - "/zh/transport"
  - "/zh/transport/"
lastUpdated: "2026-03"
accurateFor: "0.9.69"
---

## I2P 中的传输协议

I2P中的"transport"（传输层）是两个router之间直接点对点通信的方法。Transport必须提供针对外部对手的机密性和完整性保护，同时验证所联系的router确实是应该接收给定消息的那个router。

I2P 同时支持多种传输协议。目前已实现三种传输协议：

1. [NTCP](/docs/legacy/ntcp/)，一个Java新I/O (NIO) TCP传输协议
2. [SSU](/docs/legacy/ssu/)，或安全半可靠UDP
3. [NTCP2](/docs/specs/ntcp2/)，NTCP的新版本

每种都提供"连接"范式，具有身份验证、流量控制、确认和重传功能。

- 可靠传递 [I2NP](/docs/specs/i2np/) 消息。传输层仅支持 I2NP 消息传递。它们不是通用数据管道。
- 并非所有传输都保证消息的顺序传递。
- 维护一组 router 地址，每种传输一个或多个地址，router 将其作为全局联系信息发布（RouterInfo）。每种传输可以使用这些地址中的一个进行连接，这些地址可能是 IPv4 或（自版本 0.9.8 起）IPv6。
- 为每条出站消息选择最佳传输
- 按优先级对出站消息进行排队
- 根据 router 配置进行带宽限制，包括出站和入站
- 建立和拆除传输连接
- 点对点通信加密
- 维护每种传输的连接限制，实施这些限制的各种阈值，并将阈值状态传达给 router，以便其根据状态进行操作更改
- 使用 UPnP（通用即插即用）开放防火墙端口
- 协作式 NAT/防火墙穿越
- 通过多种方法检测本地 IP，包括 UPnP、检查传入连接和枚举网络设备
- 在传输之间协调防火墙状态和本地 IP 及其变化
- 向 router 和用户界面传达防火墙状态和本地 IP 及其变化
- 确定一致性时钟，用于定期更新 router 时钟，作为 NTP 的备份
- 维护每个对等节点的状态，包括是否已连接、是否最近连接过以及上次尝试时是否可达
- 根据本地规则集验证有效的 IP 地址
- 遵守 router 维护的自动和手动禁用对等节点列表，拒绝与这些对等节点的出站和入站连接

---

I2P 中的传输子系统提供以下服务：

## 传输服务

---

- router 没有发布地址，因此被认为是"隐藏的"，无法接收传入连接
- router 处于防火墙后面，因此发布一个包含协作对等节点或"介绍者"列表的 SSU 地址，这些介绍者将协助进行 NAT 穿越（详情请参见 [SSU 规范](/docs/legacy/ssu/)）
- router 不在防火墙后面或其 NAT 端口已开放；它发布包含可直接访问的 IP 和端口的 NTCP 和 SSU 地址

传输子系统维护一组router地址，每个地址都包含传输方法、IP和端口信息。这些地址构成了对外公布的联系点，由router发布到netDb中。地址还可以包含任意一组额外的选项。

## 传输地址

每种传输方法可能会发布多个 router 地址。

典型场景包括：

---

- 传输偏好的配置
- 传输是否已连接到对等节点
- 当前连接数与各种连接限制阈值的比较
- 最近对该对等节点的连接尝试是否失败
- 消息大小，因为不同传输有不同的大小限制
- 对等节点是否可以接受该传输的传入连接，如其 RouterInfo 中所宣告的
- 连接是否为间接连接（需要引介者）或直接连接
- 对等节点的传输偏好，如其 RouterInfo 中所宣告的

传输系统仅传送 [I2NP messages](/docs/specs/i2np/)。为任何消息选择的传输方式独立于上层协议和内容（router 或客户端消息，外部应用程序是否使用 TCP 或 UDP 连接到 I2P，上层是否使用 [the streaming library](/docs/api/streaming/) 或 [datagrams](/docs/api/datagrams/) 等）。

## 传输选择

对于每个传出消息，传输系统会向每个传输层征求"投标"。投标值最低（最优）的传输层赢得投标并接收消息进行传递。传输层可以拒绝投标。

传输层是否出价以及出价值取决于众多因素：

一般来说，出价值的选择确保两个router在任何时候只通过单一传输方式连接。然而，这并不是强制要求。

- 类似 TLS/SSH 的传输协议
- 适用于无法被所有其他 router 访问的 router 的"间接"传输协议（"受限路由"的一种形式）
- 与 Tor 兼容的可插拔传输协议

---

可能会开发其他传输协议，包括：

## 新传输协议和未来工作

我们继续调整每种传输协议的默认连接限制。I2P被设计为一个"网状网络"，假设任何router都可以连接到任何其他router。这个假设可能会被超出连接限制的router以及位于限制性状态防火墙后的router（受限路由）所打破。

- 类似 TLS/SSH 的传输方式
- 用于无法被所有其他路由器直接访问的路由器的“间接”传输方式（一种“受限路由”形式）
- 兼容 Tor 的可插拔传输协议

当前SSU的连接限制比NTCP更高，这基于NTCP连接的内存需求比SSU更高的假设。然而，由于NTCP缓冲区部分位于内核中，而SSU缓冲区位于Java堆上，这个假设很难验证。

分析[Breaking and Improving Protocol Obfuscation](http://www.iis.se/docs/hjelmvik_breaking.pdf)，了解传输层填充如何改善情况。

分析《Breaking and Improving Protocol Obfuscation》(http://www.iis.se/docs/hjelmvik_breaking.pdf)，并研究传输层填充如何改善现状。
