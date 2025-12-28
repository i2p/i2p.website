---
title: "Ministreaming（精简流式传输）库"
description: "I2P 的首个类似 TCP 的传输层的历史注记"
slug: "ministreaming"
lastUpdated: "2025-02"
accurateFor: "historical"
---

> **已弃用：** ministreaming 库（简化的流式库）早于如今的[流式库](/docs/specs/streaming/)。现代应用程序必须使用完整的流式 API 或 SAM v3。以下信息仅为审阅随 `ministreaming.jar` 提供的遗留源代码的开发者而保留。

## 概述

Ministreaming（轻量级流式传输协议）构建在 [I2CP](/docs/specs/i2cp/) 之上，为 I2P 的消息层提供可靠、按序的传递——就像运行在 IP 之上的 TCP 一样。它最初从早期的 **I2PTunnel** 应用（BSD 许可）中拆分出来，以便替代性传输机制能够独立演进。

关键设计约束:

- 经典的两阶段（SYN/ACK/FIN）连接建立流程，借鉴自 TCP
- 固定窗口大小为 **1** 个数据包
- 无每个数据包的 ID 或选择性确认

这些选择使实现保持精简，但也限制了吞吐量——每个数据包在发送下一个之前通常要等待将近两个往返时延（RTT）。对于长生命周期的流，这种开销尚可接受，但短的 HTTP 风格交互会明显受影响。

## 与流式传输库的关系

当前的 streaming 库沿用同一 Java 包（`net.i2p.client.streaming`）。已弃用的类和方法仍保留在 Javadoc 文档中，并有清晰标注，以便开发者识别 ministreaming（早期精简版流式库）时代的 API。当 streaming 库取代 ministreaming 时，它新增了：

- 更智能的连接建立，往返次数更少
- 自适应拥塞窗口与重传逻辑
- 在易丢包的 tunnels 上具有更佳性能

## Ministreaming 曾在何时有用？

尽管存在局限，ministreaming（精简型流式传输）在最早的部署中仍提供了可靠的传输。该 API 刻意保持精简并具有前瞻性，以便可以在不破坏调用方的情况下替换为其他流式传输引擎。Java 应用直接链接使用；非 Java 客户端则通过 [SAM](/docs/legacy/sam/) 对流式传输会话的支持来获取同等功能。

目前，`ministreaming.jar` 仅作为兼容层使用。新的开发应当：

1. 选用完整的流式库（Java）或 SAM v3（`STREAM` 风格）  
2. 在现代化代码时，移除所有残留的固定窗口假设  
3. 优先使用更大的窗口大小和优化的连接握手，以改进对延迟敏感的工作负载

## 参考

- [Streaming 库文档](/docs/specs/streaming/)
- [Streaming Javadoc](http://idk.i2p/javadoc-i2p/net/i2p/client/streaming/package-summary.html) – 包含已弃用的 ministreaming 类
- [SAM v3 规范](/docs/api/samv3/) – 为非 Java 应用程序提供流式传输支持

如果你遇到仍然依赖于 ministreaming（I2P 早期的简化流式库）的代码，请计划将其移植到现代的 Streaming API——网络及其工具链都期望较新的行为。
