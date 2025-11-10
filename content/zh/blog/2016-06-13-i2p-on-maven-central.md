---
title: "I2P 在 Maven Central 上"
date: 2016-06-13
author: "str4d"
description: "I2P 客户端库现已在 Maven Central 上提供！"
categories: ["summer-dev"]
---

我们已经进入 Summer Dev 的 API 月近半程，并且在多个方面取得了显著进展。我很高兴地宣布，这些工作中的第一个已经完成：I2P 客户端库现已在 Maven Central 上可用！

这将使 Java 开发人员在其应用程序中使用 I2P 变得简单得多。他们无需再从当前安装中获取库，只需将 I2P 添加到其依赖项即可。升级到新版本同样会容易得多。

## 如何使用它们

有两个你需要了解的库：

- `net.i2p:i2p` - The core I2P APIs; you can use these to send individual datagrams.
- `net.i2p.client:streaming` - A TCP-like set of sockets for communicating over I2P.

将其中一个或两个添加到你的项目依赖项中，就可以开始了！

### Gradle

```
compile 'net.i2p:i2p:0.9.26'
compile 'net.i2p.client:streaming:0.9.26'
```
### Gradle

```xml
<dependency>
    <groupId>net.i2p</groupId>
    <artifactId>i2p</artifactId>
    <version>0.9.26</version>
</dependency>
<dependency>
    <groupId>net.i2p.client</groupId>
    <artifactId>streaming</artifactId>
    <version>0.9.26</version>
</dependency>
```
对于其他构建系统，请参阅 Maven Central 上关于核心库和流式库的页面。

Android 开发者应使用 I2P Android 客户端库，它包含相同的库以及面向 Android 的专用辅助组件。我将很快更新它，使其依赖新的 I2P 库，从而让跨平台应用程序能够与 I2P Android 或桌面版 I2P 原生协作。

## Get hacking!

请参阅我们的应用开发指南，以获取开始使用这些库的帮助。你也可以在 IRC 上的 #i2p-dev 与我们讨论它们。如果你开始使用它们，请在 Twitter 上使用话题标签 #I2PSummer 告诉我们你在做什么！
