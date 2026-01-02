---
title: "匹配 OBEPs 与 IBGWs"
number: "138"
author: "str4d"
created: "2017-04-10"
lastupdated: "2017-04-10"
status: "Open"
thread: "http://zzz.i2p/topics/2294"
toc: true
---

## 概述

该提案为出站隧道添加一个 I2CP 选项，促使在发送消息时选择或建立隧道，使得 OBEP 与目标 LeaseSet 的一个 IBGW 匹配。

## 动机

大多数 I2P 路由器采用一种丢包的拥塞管理形式。参考实现使用一种 WRED 策略，考虑到消息大小和传输距离（参见 [tunnel throttling 文档](/docs/specs/implementation/#tunnelthrottling)）。由于这种策略，丢包的主要来源是 OBEP。

## 设计

在发送消息时，发送方选择或建立的隧道中，OBEP 与接收者的一个 IBGW 是相同的路由器。通过这样做，消息将直接从一个隧道到另一个隧道，而无需在中间通过网络发送。

## 安全性影响

这一模式实际上意味着接收者正在选择发送者的 OBEP。为了维护当前的隐私性，这一模式将导致出站隧道比 outbound.length I2CP 选项指定的多构建一跳（最终跳可能在发送者的快速层外）。

## 规范

新增一个 I2CP 选项到 [I2CP 规范](/docs/specs/i2cp/)：

    outbound.matchEndWithTarget
        Boolean

        Default value: case-specific

        如果为真，路由器将为此会话期间发送的消息选择出站隧道，使得隧道的 OBEP 是目标 Destination 的一个 IBGW。如果不存在这样的隧道，路由器将构建一个。

## 兼容性

后向兼容性是有保证的，因为路由器总是可以发送消息给自己。

## 实现

### Java I2P

隧道构建和消息发送目前是独立的子系统：

- BuildExecutor 只知道出站隧道池的 outbound.* 选项，对于它们的使用没有可见性。

- OutboundClientMessageOneShotJob 只能从现有池中选择一个隧道；如果有客户端消息进入而没有出站隧道，路由器将丢弃消息。

实施该提案需要设计一种方法让这两个子系统进行交互。

### i2pd

一项测试实现已完成。

## 性能

该提案对延迟、RTT 和丢包率有各种影响：

- 在大多数情况下，这一模式可能需要在第一次消息时建立新隧道而不是使用现有隧道，从而增加延迟。

- 对于标准隧道，OBEP 可能需要找到和连接到 IBGW，增加延迟，从而增加第一次 RTT（因为这是在发送第一个数据包后发生）。使用这一模式，OBEP 需要在隧道构建期间找到和连接到 IBGW，增加相同的延迟但减少第一次 RTT（因为这是在发送第一个数据包前发生的）。

- 当前标准的 VariableTunnelBuild 大小是 2641 字节。因此预计对于大于此大小的平均消息，这一模式将导致较低的丢包率。

需要更多研究来调查这些效果，以便决定哪些标准隧道会从默认启用这一模式中受益。
