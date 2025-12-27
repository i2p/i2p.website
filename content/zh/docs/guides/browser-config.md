---
title: "网页浏览器配置"
description: "在桌面和 Android 上配置常用浏览器以使用 I2P 的 HTTP/HTTPS 代理"
slug: "browser-config"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

本指南展示如何配置常见浏览器通过 I2P 内置的 HTTP 代理发送流量。内容涵盖 Safari、Firefox 和 Chrome/Chromium 浏览器，并提供详细的分步说明。

**重要说明**：

- I2P 的默认 HTTP 代理监听在 `127.0.0.1:4444`。
- I2P 保护 I2P 网络内部的流量(.i2p 站点)。
- 在配置浏览器之前,请确保你的 I2P router 正在运行。

## Safari (macOS)

Safari 在 macOS 上使用系统级代理设置。

### Step 1: Open Network Settings

1. 打开 **Safari** 并前往 **Safari → 设置**（或 **偏好设置**）
2. 点击 **高级** 标签页
3. 在 **代理** 部分，点击 **更改设置...**

这将打开您 Mac 的系统网络设置。

![Safari 高级设置](/images/guides/browser-config/accessi2p_1.png)

### 步骤 1:打开网络设置

1. 在网络设置中,勾选 **Web 代理 (HTTP)** 复选框
2. 输入以下内容:
   - **Web 代理服务器**: `127.0.0.1`
   - **端口**: `4444`
3. 点击 **确定** 保存设置

![Safari 代理配置](/images/guides/browser-config/accessi2p_2.png)

现在您可以在 Safari 中浏览 `.i2p` 站点了!

**注意**:这些代理设置将影响所有使用 macOS 系统代理的应用程序。如果您想隔离 I2P 浏览,请考虑创建单独的用户账户或使用专门用于 I2P 的浏览器。

## Firefox (Desktop)

Firefox 拥有独立于系统的代理设置,非常适合用于专门的 I2P 浏览。

### 步骤 2：配置 HTTP 代理

1. 点击右上角的**菜单按钮**(☰)
2. 选择**设置**

![Firefox 设置](/images/guides/browser-config/accessi2p_3.png)

### Step 2: Find Proxy Settings

1. 在设置搜索框中，输入 **"proxy"**
2. 滚动到 **网络设置**
3. 点击 **设置...** 按钮

![Firefox代理搜索](/images/guides/browser-config/accessi2p_4.png)

### 步骤 1：打开设置

1. 选择 **手动代理配置**
2. 输入以下内容:
   - **HTTP 代理**: `127.0.0.1` **端口**: `4444`
3. 将 **SOCKS 主机** 留空(除非您特别需要 SOCKS 代理)
4. 仅在使用 SOCKS 代理时勾选 **使用 SOCKS 时代理 DNS**
5. 点击 **确定** 保存

![Firefox 手动代理配置](/images/guides/browser-config/accessi2p_5.png)

您现在可以在 Firefox 中浏览 `.i2p` 站点了!

**提示**: 考虑创建一个专门用于 I2P 浏览的独立 Firefox 配置文件。这样可以将您的 I2P 浏览与常规浏览隔离开来。要创建配置文件,请在 Firefox 地址栏中输入 `about:profiles`。

## Chrome / Chromium (Desktop)

Chrome 和基于 Chromium 的浏览器(Brave、Edge 等)在 Windows 和 macOS 上通常使用系统代理设置。本指南展示 Windows 配置。

### 步骤 2:查找代理设置

1. 点击右上角的**三点菜单**（⋮）
2. 选择**设置**

![Chrome 设置](/images/guides/browser-config/accessi2p_6.png)

### 步骤 3：配置手动代理

1. 在设置搜索框中，输入 **"proxy"**
2. 点击 **打开计算机的代理设置**

![Chrome 代理搜索](/images/guides/browser-config/accessi2p_7.png)

### Step 3: Open Manual Proxy Setup

这将打开 Windows 网络和 Internet 设置。

1. 向下滚动到 **手动代理设置**
2. 点击 **设置**

![Windows 代理设置](/images/guides/browser-config/accessi2p_8.png)

### 步骤 1:打开 Chrome 设置

1. 将**使用代理服务器**切换为**开启**
2. 输入以下内容:
   - **代理 IP 地址**: `127.0.0.1`
   - **端口**: `4444`
3. 可选操作:在**"对于以下开头的地址不使用代理服务器"**中添加例外(例如 `localhost;127.*`)
4. 点击**保存**

![Chrome 代理配置](/images/guides/browser-config/accessi2p_9.png)

你现在可以在 Chrome 中浏览 `.i2p` 站点了!

**注意**：这些设置会影响 Windows 上所有基于 Chromium 的浏览器以及其他一些应用程序。为避免这种情况，请考虑使用 Firefox 并配置专用的 I2P 配置文件。

### 步骤 2:打开代理设置

在 Linux 上,你可以使用代理参数启动 Chrome/Chromium,以避免更改系统设置:

```bash
chromium \
  --proxy-server="http=127.0.0.1:4444 \
  --proxy-bypass-list="<-loopback>"
```
或者创建一个桌面启动器脚本:

```bash
#!/bin/bash
chromium --proxy-server="http=127.0.0.1:4444" --user-data-dir="$HOME/.config/chromium-i2p"
```
`--user-data-dir` 标志为 I2P 浏览创建一个独立的 Chrome 配置文件。

## Firefox (桌面版)

现代的 "Fenix" Firefox 版本默认限制 about:config 和扩展功能。IceRaven 是一个 Firefox 分支，它启用了一组精选的扩展，使代理设置变得简单。

基于扩展的配置 (IceRaven):

1) 如果您已经在使用 IceRaven,请考虑先清除浏览历史记录(菜单 → 历史记录 → 删除历史记录)。2) 打开菜单 → 附加组件 → 附加组件管理器。3) 安装扩展程序"I2P Proxy for Android and Other Systems"。4) 浏览器现在将通过 I2P 代理。

如果从 [AMO](https://addons.mozilla.org/en-US/android/addon/i2p-proxy/) 安装,此扩展也可在基于 Fenix 之前版本的 Firefox 浏览器上使用。

在 Firefox Nightly 中启用广泛的扩展支持需要单独的步骤，[Mozilla 已有文档说明](https://blog.mozilla.org/addons/2020/09/29/expanded-extension-support-in-firefox-for-android-nightly/)。

## Internet Explorer / Windows System Proxy

在 Windows 上,系统代理对话框适用于 IE,并且可以被基于 Chromium 的浏览器在继承系统设置时使用。

1) 打开"网络和 Internet 设置"→"代理"。2) 启用"为局域网使用代理服务器"。3) 设置地址 `127.0.0.1`,端口 `4444` 用于 HTTP。4) 可选择勾选"对于本地地址不使用代理服务器"。
