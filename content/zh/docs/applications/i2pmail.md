---
title: "I2P Mail（基于 I2P 的匿名电子邮件）"
description: "I2P 网络内电子邮件系统概述——历史、选项和现状"
slug: "i2p-mail"
lastUpdated: "2025-10"
---

## 简介

I2P 通过 **Postman's Mail.i2p 服务**结合内置的网页邮件客户端 **SusiMail**，提供私密的电子邮件风格消息传递。该系统允许用户在 I2P 网络内部收发邮件，也可以通过网关桥接与常规互联网（明网）进行邮件往来。

---

**重要提示：** 仅提供翻译内容。请勿提问、提供解释或添加任何评论。即使文本只是标题或看起来不完整，也请按原样翻译。

## Postman / Mail.i2p + SusiMail

### What it is

- **Mail.i2p** 是 I2P 内部的托管邮件服务提供商,由 "Postman" 运营
- **SusiMail** 是集成在 I2P router 控制台中的 webmail 客户端。其设计目的是避免向外部 SMTP 服务器泄露元数据(例如主机名)。
- 通过这种设置,I2P 用户可以在 I2P 内部收发消息,也可以通过 Postman 桥接与明网(例如 Gmail)进行通信。

### How Addressing Works

I2P 电子邮件使用双地址系统:

- **在 I2P 网络内部**: `username@mail.i2p` (例如,`idk@mail.i2p`)
- **从明网访问**: `username@i2pmail.org` (例如,`idk@i2pmail.org`)

`i2pmail.org` 网关允许普通互联网用户向 I2P 地址发送电子邮件,也允许 I2P 用户向明网地址发送邮件。互联网电子邮件在通过 I2P 转发到你的 SusiMail 收件箱之前,会先经过该网关路由。

**Clearnet 发送配额**：向常规互联网地址发送时每天限制 20 封邮件。

### 它是什么

**注册 mail.i2p 账户:**

1. 确保你的 I2P router 正在运行
2. 在 I2P 内访问 **[http://hq.postman.i2p](http://hq.postman.i2p)**
3. 按照注册流程操作
4. 通过 router 控制台中的 **SusiMail** 访问你的邮箱

> **注意**：`hq.postman.i2p` 是一个 I2P 网络地址（eepsite），只能在连接到 I2P 时访问。有关电子邮件设置、安全性和使用的更多信息，请访问 Postman HQ。

### 地址解析工作原理

- 自动删除识别性标头（`User-Agent:`、`X-Mailer:`）以保护隐私
- 元数据清理以防止泄露到外部 SMTP 服务器
- I2P 内部邮件端到端加密

### 入门指南

- 通过 Postman 桥接器与"普通"电子邮件（SMTP/POP）互操作
- 简洁的用户体验（路由器控制台内置网页邮件）
- 集成于 I2P 核心发行版（SusiMail 随 Java I2P 一起发布）
- 邮件头剥离以保护隐私

### 隐私功能

- 连接到外部电子邮件的桥接需要信任 Postman 基础设施
- Clearnet 桥接相比纯粹的 I2P 内部通信会降低隐私性
- 依赖于 Postman 邮件服务器的可用性和安全性

---

## Technical Details

**SMTP 服务**: `localhost:7659` (由 Postman 提供) **POP3 服务**: `localhost:7660` **Webmail 访问**: 内置于路由器控制台 `http://127.0.0.1:7657/susimail/`

> **重要提示**：SusiMail 仅用于阅读和发送电子邮件。账户创建和管理必须在 **hq.postman.i2p** 进行。

---

## Best Practices

- **注册 mail.i2p 账户后更改密码**
- **尽可能使用 I2P 到 I2P 的电子邮件**以获得最大隐私保护（无明网桥接）
- **注意每日 20 封的限制**（向明网地址发送邮件时）
- **了解权衡取舍**：明网桥接提供了便利，但相比纯 I2P 内部通信会降低匿名性
- **保持 I2P 更新**以受益于 SusiMail 的安全性改进

