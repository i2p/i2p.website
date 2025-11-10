---
title: "Windows 简易安装套件 1.9.0 发布"
date: 2022-08-28
author: "idk"
description: "Windows 简易安装捆绑包 1.9.0 - 重大稳定性/兼容性改进"
categories: ["release"]
---

## 本次更新包含全新的 1.9.0 router，以及针对捆绑包用户的重大易用性改进。

此版本包含新的 I2P 1.9.0 router，并基于 Java 18.02.1。

旧的批处理脚本已逐步淘汰，转而采用 jpackage 本身提供的更灵活、更稳定的解决方案。这应能修复批处理脚本中存在的与路径查找和路径加引号相关的所有错误。升级后，可以安全地删除这些批处理脚本。它们将在下次更新时由安装程序移除。

一个用于管理浏览工具的子项目已启动：i2p.plugins.firefox，它具备在多个平台上自动且稳定地配置 I2P 浏览器的强大能力。它被用来取代批处理脚本，同时也可作为跨平台的 I2P 浏览器管理工具。欢迎在源代码仓库提交贡献：http://git.idk.i2p/idk/i2p.plugins.firefox

本次发布改进了与外部运行的 I2P router 的兼容性，例如 IzPack 安装程序提供的 I2P router，以及第三方 router 实现（如 i2pd）。通过改进对外部 router 的发现，减少了系统资源占用、缩短了启动时间，并避免资源冲突的发生。

除此之外，此配置文件已更新至 Arkenfox 配置文件的最新版本。I2P in Private Browsing 和 NoScript 均已更新。为便于针对不同威胁模型评估不同配置，已对该配置文件进行了重构。
