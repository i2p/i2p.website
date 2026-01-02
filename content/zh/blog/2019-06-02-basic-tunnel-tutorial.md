---
title: "I2P tunnels 基础教程（配图）"
date: 2019-06-02
author: "idk"
description: "i2ptunnel 基本设置"
categories: ["tutorial"]
---

Although the Java I2P router comes pre-configured with a static web server, jetty, to provide the user's first eepSite, many require more sophisticated functionality from their web server and would rather create an eepSite with a different server. This is of course possible, and actually is really easy once you've done it one time.

尽管这很容易做到，但在动手之前有几件事需要考虑。你应当从你的 Web 服务器中移除可用于识别的特征，例如可能暴露身份的 HTTP 头部，以及会显示服务器/发行版类型的默认错误页面。关于由于应用程序配置不当而对匿名性造成的威胁的更多信息，请参阅：[Riseup 此处](https://riseup.net/en/security/network-security/tor/onionservices-best-practices), [Whonix 此处](https://www.whonix.org/wiki/Onion_Services), [这篇博文介绍了一些 OPSEC（操作安全）失误](https://blog.0day.rocks/securing-a-web-hidden-service-89d935ba1c1d), [以及 I2P 应用程序页面](https://geti2p.net/docs/applications/supported)。尽管其中很多信息是针对 Tor Onion Services（Tor 隐藏服务）而写的，但相同的流程和原则同样适用于通过 I2P 托管应用程序。

### 第一步：打开 Tunnel 向导

前往 127.0.0.1:7657 的 I2P 网页界面，并打开 [隐藏服务管理器](http://127.0.0.1:7657/i2ptunnelmgr)（链接到 localhost）。点击标有“Tunnel Wizard”的按钮开始。

### 步骤二：选择一个服务器 Tunnel

tunnel 向导非常简单。由于我们正在设置一个 http *服务器*，我们只需要选择一个*服务器* tunnel。

### 第三步：选择一个 HTTP Tunnel

HTTP tunnel 是一种针对托管 HTTP 服务优化的 tunnel 类型。它启用了专门为此目的定制的过滤和速率限制功能。标准 tunnel 也可能同样可用，但如果你选择标准 tunnel，就需要自行负责这些安全功能。有关 HTTP Tunnel 配置的更深入探讨将在下一篇教程中提供。

### 步骤四：为其命名并提供描述

为了便于你记住并区分你打算使用该 tunnel（隧道）的用途，请给它取一个清晰的昵称和描述。 如果你之后需要回来进行更多管理，你将在隐藏服务管理器中通过这些信息识别该 tunnel。

### 第五步：配置主机和端口

在此步骤中，您需要将 Web 服务器指向其正在监听的 TCP 端口。由于大多数 Web 服务器监听 80 端口或 8080 端口，示例中也是如此。如果您使用备用端口，或使用虚拟机或容器来隔离 Web 服务，则可能需要调整主机、端口，或两者都进行调整。

### 第六步：决定是否自动启动它

我想不出如何进一步阐述这一步。

### 第七步：检查您的设置

最后，请查看您所选择的设置。如果确认无误，请保存。如果您没有选择自动启动 tunnel，那么当您希望使您的服务可用时，请前往隐藏服务管理器并手动启动它。

### 附录：HTTP 服务器自定义选项

I2P 提供了一个详细的面板，用于以自定义方式配置 HTTP 服务器 tunnel（隧道）。我将通过逐一讲解它们来完成本教程。迟早会的。
