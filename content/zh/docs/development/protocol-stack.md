---
title: "协议栈"
description: "I2P 协议栈层次概述"
slug: "protocol-stack"
lastUpdated: "2024-01"
accurateFor: "0.9.61"
aliases:
  - "/zh/docs/develop/protocol-stack"
  - "/zh/docs/develop/protocol-stack/"
  - "/zh/protocols"
  - "/zh/protocols/"
---

I2P协议栈是一个分层设计，能够实现匿名通信。每一层都在下层功能的基础上增加特定的能力。有关每个组件的更多详细信息，请参阅[技术文档索引](/docs/develop/overview)。

## 互联网层 {#internet}

**IP** - Internet Protocol（互联网协议）允许对常规互联网上的主机进行寻址，并使用尽力而为的传输方式在互联网上路由数据包。

## 传输层 {#transport}

- **TCP** - 传输控制协议，允许可靠、有序的数据包传输
- **UDP** - 用户数据报协议，允许不可靠、无序的数据包传输

## I2P 传输层 {#i2p-transport}

加密的 router 到 router 连接（尚未匿名）：

- **[NTCP2](/docs/specs/ntcp2)** - 基于 NIO 的 TCP 传输协议
- **[SSU2](/docs/specs/ssu2)** - 安全半可靠 UDP 传输协议

## I2P Tunnel 层 {#tunnels}

提供完全匿名的加密tunnel连接：

- **[Tunnel messages](/docs/legacy/tunnel-message)** - 加密的I2NP消息和用于传递的加密指令
- **[I2NP messages](/docs/specs/i2np)** - 具有分层加密的协议消息，用于多跳匿名路由

## I2P Garlic Layer {#garlic}

提供加密和匿名的端到端 I2P 消息传递：

- **[Garlic messages](/docs/overview/garlic-routing)** - 用于匿名传输的封装I2NP消息

## I2P 客户端层 {#client}

- **[I2CP](/docs/specs/i2cp)** - I2P Control Protocol 允许应用程序访问 I2P 网络，无需直接使用 router API

## I2P 端到端传输层 {#e2e-transport}

- **[Streaming Library](/docs/api/streaming)** - 提供类似于TCP的可靠、有序传输
- **[Datagram Library](/docs/api/datagrams)** - 提供类似于UDP的不可靠传输

## I2P 应用接口层 {#app-interface}

应用程序开发者的可选接口：

- **[I2PTunnel](/docs/api/i2ptunnel)** - 将 TCP 连接隧道化进出 I2P 网络
- **[SAMv3](/docs/api/samv3)** - 面向非 Java 应用程序的简单匿名消息传递协议

## I2P 应用代理层 {#app-proxy}

标准互联网协议的代理：

- **HTTP** - 网页浏览代理
- **IRC** - Internet Relay Chat 代理
- **[SOCKS](/docs/api/socks)** - SOCKS4/4a/5 代理
- **Streamr** - UDP 流媒体代理

## 应用程序 {#applications}

应用程序可以在不同层次与I2P进行接口连接：

**流式/数据报应用程序：** - 直接使用流式或数据报库的I2P原生应用程序

**SAM 应用程序：** - 使用 SAM 协议的任何语言编写的应用程序

**I2P专用应用程序：** - 专门为I2P设计的应用程序（I2PSnark、SusiMail等）

**标准互联网应用程序：** - 使用I2P代理的常规应用程序（网页浏览器、IRC客户端等）

## 协议栈图 {#diagram}

![I2P 协议栈](/images/protocol_stack.png)

注意：SAM 可以同时使用流库和数据报。
