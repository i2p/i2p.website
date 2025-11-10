---
title: "Windows Easy-Install 2.1.0 版本发布"
date: 2023-01-13
author: "idk"
description: "Windows Easy-Install Bundle 2.1.0 发布，以提升稳定性和性能"
categories: ["release"]
---

## 更新详情

适用于 Windows 的 I2P 简易安装包 2.1.0 版本已发布。与往常一样，此版本包含更新的 I2P Router。本次 I2P 版本提供了改进的应对网络拥塞的策略。这些改进应当提升性能、连通性，并保障 I2P 网络的长期健康。

本次发布主要对浏览器配置文件启动器进行了底层改进。通过支持通过环境变量配置 Tor Browser Bundle（Tor 浏览器套件，简称 TBB），改进了兼容性。Firefox 配置文件已更新，扩展的基础版本也已更新。我们还对整个代码库和部署流程进行了改进。

很遗憾，此版本仍然是未签名的 .exe 安装程序。请在使用前验证该安装程序的校验和。另一方面，更新由我的 I2P 签名密钥签名，因此是安全的。

本版本使用 OpenJDK 19 编译。它使用 i2p.plugins.firefox version 1.0.7 作为启动浏览器的库。它使用 i2p.i2p version 2.1.0 作为 I2P router，并用于提供应用程序。一如既往，建议您尽早将 I2P router 更新至最新版本。
