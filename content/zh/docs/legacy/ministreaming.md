---
title: "Ministreaming 库"
description: "I2P 首个类 TCP 传输层的历史记录"
slug: "ministreaming"
aliases:
  - "/zh/ministreaming"
  - "/zh/ministreaming/"
lastUpdated: "2025-02"
accurateFor: "historical"
---

## 注意

ministreaming库已经被"完整"[streaming库](/docs/api/streaming)增强和扩展。Ministreaming已被弃用，与现今的应用程序不兼容。以下文档已过时。另请注意，streaming在同一个Java包（net.i2p.client.streaming）中扩展了ministreaming，因此当前的API文档包含两者。过时的ministreaming类和方法在Javadocs中明确标记为已弃用。

## Ministreaming 库

ministreaming库是核心[I2CP](/docs/protocol/i2cp)之上的一个层，它允许在不可靠、无序和未认证的消息层之上运行可靠、有序和已认证的消息流。就像TCP与IP的关系一样，这种流功能有一系列可用的权衡和优化，但为了不将该功能嵌入到基础I2P代码中，它被分离成自己的库，既保持了类似TCP的复杂性的独立性，也允许替代的优化实现。

ministreaming 库是由 mihi 作为其 [I2PTunnel](/docs/api/i2ptunnel) 应用程序的一部分编写的，后来被分离出来并在 BSD 许可证下发布。它被称为"mini"streaming 库是因为它在实现中做了一些简化，而更强大的 streaming 库可以进一步优化以在 I2P 上运行。ministreaming 库的两个主要问题是它使用传统的 TCP 两阶段建立协议和当前固定的窗口大小为 1。对于长期存在的流，建立问题是次要的，但对于短期流，如快速 HTTP 请求，影响可能很大。至于窗口大小，ministreaming 库不在发送的消息中维护任何 ID 或排序（也不包括任何应用层 ACK 或 SACK），因此在发送另一个消息之前，它必须等待平均两倍于发送消息所需的时间。

即使存在这些问题，ministreaming 库在许多情况下仍然表现良好，其 API 既非常简单，又能够在引入不同流实现时保持不变。该库部署在自己的 ministreaming.jar 中。希望使用它的 Java 开发者可以直接访问 API，而其他语言的开发者可以通过 [SAM](/docs/api/samv3) 的流支持来使用它。
