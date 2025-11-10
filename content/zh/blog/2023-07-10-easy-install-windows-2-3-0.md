---
title: "Windows 版 Easy-Install 2.3.0 已发布"
date: 2023-07-10
author: "idk"
description: "Windows 版 Easy-Install 2.3.0 发布"
categories: ["release"]
---

适用于 Windows 的 I2P Easy-Install 安装包 2.3.0 版本现已发布。与往常一样，此次发布包含更新的 I2P router 版本。这也涵盖会影响在该网络上托管服务的用户的安全问题。

这将是最后一个会与 I2P Desktop GUI 不兼容的 Easy-Install bundle 版本。它已更新，包含所有随附 WebExtensions 的新版本。I2P in Private Browsing 中一个导致其与自定义主题不兼容的长期存在的错误已被修复。仍建议用户*不要*安装自定义主题。在 Firefox 中，Snark 选项卡不会自动固定到标签页顺序的顶部。除使用备用 cookieStores 外，Snark 选项卡现在与普通浏览器选项卡的行为一致。

**不幸的是，此发行版仍然是未签名的 `.exe` 安装程序。** 在使用之前，请验证安装程序的校验和。**另一方面，更新** 由我的 I2P 签名密钥签名，因此是安全的。

此版本使用 OpenJDK 20 进行编译。它使用 i2p.plugins.firefox 1.1.0 版本作为启动浏览器的库。它使用 i2p.i2p 2.3.0 版本作为 I2P router（I2P 路由器），并用于提供应用。与往常一样，建议您在方便时尽快将 I2P router 更新到最新版本。

- [Easy-Install Bundle Source](http://git.idk.i2p/i2p-hackers/i2p.firefox/-/tree/i2p-firefox-2.3.0)
- [Router Source](http://git.idk.i2p/i2p-hackers/i2p.i2p/-/tree/i2p-2.3.0)
- [Profile Manager Source](http://git.idk.i2p/i2p-hackers/i2p.plugins.firefox/-/tree/1.1.0)
