---
title: "在 macOS 上安装 I2P(详细方式)"
description: "在 macOS 上手动安装 I2P 及其依赖项的分步指南"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## 您需要准备的内容

- 运行 macOS 10.14 (Mojave) 或更高版本的 Mac
- 安装应用程序所需的管理员权限
- 大约 15-20 分钟时间
- 用于下载安装程序的互联网连接

## 概述

此安装过程包含四个主要步骤:

1. **安装 Java** - 下载并安装 Oracle Java Runtime Environment
2. **安装 I2P** - 下载并运行 I2P 安装程序
3. **配置 I2P 应用** - 设置启动器并添加到程序坞
4. **配置 I2P 带宽** - 运行设置向导以优化您的连接

## 第一部分:安装 Java

I2P 需要 Java 才能运行。如果你已经安装了 Java 8 或更高版本,可以[跳到第二部分](#part-two-download-and-install-i2p)。

### Step 1: Download Java

访问 [Oracle Java 下载页面](https://www.oracle.com/java/technologies/downloads/) 并下载适用于 macOS 的 Java 8 或更高版本的安装程序。

![下载适用于 macOS 的 Oracle Java](/images/guides/macos-install/0-jre.png)

### Step 2: Run the Installer

在"下载"文件夹中找到已下载的 `.dmg` 文件,双击打开它。

![打开 Java 安装程序](/images/guides/macos-install/1-jre.png)

### Step 3: Allow Installation

macOS 可能会显示安全提示,因为安装程序来自已识别的开发者。点击**打开**继续。

![授予安装程序继续进行的权限](/images/guides/macos-install/2-jre.png)

### 步骤 1：下载 Java

点击 **Install** 开始 Java 安装过程。

![开始安装 Java](/images/guides/macos-install/3-jre.png)

### 步骤 2：运行安装程序

安装程序将复制文件并在您的系统上配置 Java。这通常需要 1-2 分钟。

![等待安装程序完成](/images/guides/macos-install/4-jre.png)

### 步骤 3：允许安装

当您看到成功消息时,Java 已安装完成!点击 **关闭** 以完成操作。

![Java 安装完成](/images/guides/macos-install/5-jre.png)

## Part Two: Download and Install I2P

现在 Java 已经安装完成，你可以安装 I2P router 了。

### 步骤 4：安装 Java

访问[下载页面](/downloads/)并下载 **I2P for Unix/Linux/BSD/Solaris** 安装程序（`.jar` 文件）。

![下载 I2P 安装程序](/images/guides/macos-install/0-i2p.png)

### 步骤 5：等待安装完成

双击下载的 `i2pinstall_X.X.X.jar` 文件。安装程序将启动并要求您选择首选语言。

![选择您的语言](/images/guides/macos-install/1-i2p.png)

### 步骤 6：安装完成

阅读欢迎信息并点击 **Next** 继续。

![安装程序介绍](/images/guides/macos-install/2-i2p.png)

### Step 4: Important Notice

安装程序将显示一条关于更新的重要通知。I2P 更新是**端到端签名**和验证的,即使安装程序本身未签名。点击 **Next**。

![关于更新的重要提示](/images/guides/macos-install/3-i2p.png)

### 步骤 1：下载 I2P

阅读 I2P 许可协议（BSD 风格许可证）。点击**下一步**接受。

![许可协议](/images/guides/macos-install/4-i2p.png)

### 步骤 2:运行安装程序

选择 I2P 的安装位置。推荐使用默认位置（`/Applications/i2p`）。点击**下一步**。

![选择安装目录](/images/guides/macos-install/5-i2p.png)

### 步骤 3:欢迎界面

保持所有组件被选中以进行完整安装。点击 **Next**。

![选择要安装的组件](/images/guides/macos-install/6-i2p.png)

### 步骤 4：重要提示

检查您的选择并点击 **Next** 开始安装 I2P。

![开始安装](/images/guides/macos-install/7-i2p.png)

### 步骤 5:许可协议

安装程序将复制 I2P 文件到您的系统。这大约需要 1-2 分钟。

![安装进行中](/images/guides/macos-install/8-i2p.png)

### 步骤 6：选择安装目录

安装程序会创建用于启动 I2P 的启动脚本。

![生成启动脚本](/images/guides/macos-install/9-i2p.png)

### 步骤 7：选择组件

安装程序会询问是否创建桌面快捷方式和菜单条目。做出选择后点击**下一步**。

![创建快捷方式](/images/guides/macos-install/10-i2p.png)

### 步骤 8：开始安装

成功！I2P 现已安装完成。点击 **完成** 结束安装。

![安装完成](/images/guides/macos-install/11-i2p.png)

## Part Three: Configure I2P App

现在让我们将 I2P 添加到你的"应用程序"文件夹和程序坞，以便轻松启动。

### 步骤 9：安装文件

打开访达并导航到您的**应用程序**文件夹。

![打开应用程序文件夹](/images/guides/macos-install/0-conf.png)

### 步骤 10：生成启动脚本

在 `/Applications/i2p/` 目录中查找 **I2P** 文件夹或 **Start I2P Router** 应用程序。

![查找 I2P 启动器](/images/guides/macos-install/1-conf.png)

### 步骤 11：安装快捷方式

将 **Start I2P Router** 应用程序拖动到您的程序坞以便快速访问。您也可以在桌面上创建一个替身。

![将 I2P 添加到您的 Dock](/images/guides/macos-install/2-conf.png)

**提示**：右键点击 Dock 中的 I2P 图标,选择 **选项 → 在 Dock 中保留**,使其永久固定。

## Part Four: Configure I2P Bandwidth

当您首次启动 I2P 时,您将进入一个设置向导来配置您的带宽设置。这有助于为您的连接优化 I2P 的性能。

### 步骤 12:安装完成

点击 Dock 中的 I2P 图标（或双击启动器）。您的默认网络浏览器将打开 I2P Router Console。

![I2P 路由器控制台欢迎界面](/images/guides/macos-install/0-wiz.png)

### Step 2: Welcome Wizard

设置向导将会欢迎您。点击 **Next** 开始配置 I2P。

![安装向导介绍](/images/guides/macos-install/1-wiz.png)

### 步骤 1：打开应用程序文件夹

选择您首选的**界面语言**并在**浅色**或**深色**主题之间进行选择。点击**下一步**。

![选择语言和主题](/images/guides/macos-install/2-wiz.png)

### 步骤 2：找到 I2P 启动器

向导将解释带宽测试。此测试连接到 **M-Lab** 服务以测量您的互联网速度。点击**下一步**继续。

![Bandwidth test explanation](/images/guides/macos-install/3-wiz.png)

### 步骤 3：添加到程序坞

点击 **Run Test** 来测量你的上传和下载速度。测试大约需要 30-60 秒。

![运行带宽测试](/images/guides/macos-install/4-wiz.png)

### Step 6: Test Results

查看您的测试结果。I2P 将根据您的连接速度推荐带宽设置。

![带宽测试结果](/images/guides/macos-install/5-wiz.png)

### 步骤 1：启动 I2P

选择您想要与 I2P 网络共享多少带宽:

- **自动**（推荐）：I2P 根据你的使用情况管理带宽
- **受限**：设置特定的上传/下载限制
- **无限制**：尽可能多地共享（适用于快速连接）

点击 **Next** 保存您的设置。

![配置带宽共享](/images/guides/macos-install/6-wiz.png)

### 步骤 2:欢迎向导

您的 I2P router 现在已配置完成并正在运行!router console 将显示您的连接状态,并允许您浏览 I2P 站点。

## Getting Started with I2P

现在 I2P 已安装并配置完成,您可以:

1. **浏览 I2P 站点**:访问 [I2P 主页](http://127.0.0.1:7657/home)查看热门 I2P 服务的链接
2. **配置浏览器**:设置[浏览器配置文件](/docs/guides/browser-config)以访问 `.i2p` 站点
3. **探索服务**:体验 I2P 电子邮件、论坛、文件共享等更多功能
4. **监控 router**:[控制台](http://127.0.0.1:7657/console)显示网络状态和统计信息

### 步骤 3:语言和主题

- **Router Console**: [http://127.0.0.1:7657/](http://127.0.0.1:7657/)
- **配置**: [http://127.0.0.1:7657/config](http://127.0.0.1:7657/config)
- **地址簿**: [http://127.0.0.1:7657/susidns/addressbook](http://127.0.0.1:7657/susidns/addressbook)
- **带宽设置**: [http://127.0.0.1:7657/config](http://127.0.0.1:7657/config)

## Re-running the Setup Wizard

如果您想更改带宽设置或稍后重新配置 I2P,可以从 Router Console 重新运行欢迎向导:

1. 访问 [I2P 设置向导](http://127.0.0.1:7657/welcome)
2. 再次按照向导步骤操作

## Troubleshooting

### 步骤 4:带宽测试信息

- **检查 Java**：在终端运行 `java -version` 确保已安装 Java
- **检查权限**：确保 I2P 文件夹具有正确的权限
- **检查日志**：查看 `~/.i2p/wrapper.log` 中的错误信息

### 步骤 5：运行带宽测试

- 确保 I2P 正在运行(检查 Router Console)
- 配置浏览器的代理设置,使用 HTTP 代理 `127.0.0.1:4444`
- 启动后等待 5-10 分钟,让 I2P 集成到网络中

### 步骤 6：测试结果

- 再次运行带宽测试并调整您的设置
- 确保您与网络共享了一些带宽
- 在路由器控制台中检查您的连接状态

## 第二部分:下载和安装 I2P

从 Mac 中移除 I2P:

1. 如果 I2P router 正在运行,请先退出
2. 删除 `/Applications/i2p` 文件夹
3. 删除 `~/.i2p` 文件夹(你的 I2P 配置和数据)
4. 从程序坞中移除 I2P 图标

## Next Steps

- **加入社区**：访问 [i2pforum.net](http://i2pforum.net) 或在 Reddit 上查看 I2P
- **了解更多**：阅读 [I2P 文档](/en/docs) 以理解网络的工作原理
- **参与其中**：考虑[为 I2P 做贡献](/en/get-involved)，参与开发或运行基础设施

恭喜！您现在已经是 I2P 网络的一部分了。欢迎来到隐形互联网！

