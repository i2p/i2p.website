---
title: "托管客户端"
description: "路由器管理的应用程序如何与 ClientAppManager 和端口映射器集成"
slug: "managed-clients"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## 1. 概述

[`clients.config`](/docs/specs/configuration/#clients-config) 中的条目告诉 router 在启动时启动哪些应用程序。每个条目可以作为**托管**客户端(首选)或**非托管**客户端运行。托管客户端与 `ClientAppManager` 协作，后者：

- 实例化应用程序并跟踪路由器控制台的生命周期状态
- 向用户提供启动/停止控制,并在路由器退出时强制执行干净的关闭
- 托管一个轻量级的**客户端注册表**和**端口映射器**,以便应用程序能够发现彼此的服务

非托管客户端仅调用 `main()` 方法;仅在无法现代化的遗留代码中使用它们。

## 2. 实现托管客户端

托管客户端必须实现 `net.i2p.app.ClientApp`(用于面向用户的应用程序)或 `net.i2p.router.app.RouterApp`(用于 router 扩展)。提供以下构造函数之一,以便管理器可以提供上下文和配置参数:

```java
public MyClientApp(I2PAppContext context, ClientAppManager manager, String[] args)
```
```java
public MyRouterApp(RouterContext context, ClientAppManager manager, String[] args)
```
`args` 数组包含在 `clients.config` 或 `clients.config.d/` 中各个文件里配置的值。尽可能扩展 `ClientApp` / `RouterApp` 辅助类以继承默认的生命周期连接。

### 2.1 Lifecycle Methods

托管客户端应当实现:

- `startup()` - 执行初始化并快速返回。必须至少调用一次 `manager.notify()` 以从 INITIALIZED 状态转换。
- `shutdown(String[] args)` - 释放资源并停止后台线程。必须至少调用一次 `manager.notify()` 以将状态更改为 STOPPING 或 STOPPED。
- `getState()` - 告知控制台应用程序是正在运行、启动中、停止中还是失败

当用户与控制台交互时,管理器会调用这些方法。

### 2.2 Advantages

- 路由器控制台中的准确状态报告
- 干净的重启,无线程泄漏或静态引用
- 应用程序停止后更低的内存占用
- 通过注入的上下文实现集中式日志记录和错误报告

## 3. Unmanaged Clients (Fallback Mode)

如果配置的类未实现托管接口，路由器将通过调用 `main(String[] args)` 来启动它，并且无法跟踪生成的进程。控制台显示的信息有限，且关闭钩子可能不会运行。此模式仅保留给无法采用托管 API 的脚本或一次性实用程序使用。

## 4. Client Registry

托管客户端和非托管客户端可以向管理器注册自身,以便其他组件可以通过名称检索引用:

```java
manager.register(this);
```
注册使用客户端的 `getName()` 返回值作为注册表键。已知的注册包括 `console`、`i2ptunnel`、`Jetty`、`outproxy` 和 `update`。使用 `ClientAppManager.getRegisteredApp(String name)` 检索客户端以协调功能（例如，console 查询 Jetty 以获取状态详情）。

注意，客户端注册表和端口映射器是两个独立的系统。客户端注册表通过名称查找实现应用程序间通信，而端口映射器将服务名称映射到主机:端口组合以实现服务发现。

## 3. 非托管客户端(回退模式)

端口映射器为内部 TCP 服务提供了一个简单的目录。注册回环端口,以便协作者避免使用硬编码地址:

```java
context.portMapper().register(PortMapper.SVC_HTTPS_PROXY, 4445);
```
或使用显式主机指定:

```java
context.portMapper().register(PortMapper.SVC_HTTP_PROXY, "127.0.0.1", 4444);
```
使用 `PortMapper.getPort(String name)`(如果未找到则返回 -1)或 `getPort(String name, int defaultPort)`(如果未找到则返回默认值)查找服务。使用 `isRegistered(String name)` 检查注册状态,并使用 `getActualHost(String name)` 获取已注册的主机。

来自 `net.i2p.util.PortMapper` 的常见端口映射服务常量:

- `SVC_CONSOLE` - Router console(路由器控制台)(默认端口 7657)
- `SVC_HTTP_PROXY` - HTTP 代理(默认端口 4444)
- `SVC_HTTPS_PROXY` - HTTPS 代理(默认端口 4445)
- `SVC_I2PTUNNEL` - I2PTunnel 管理器
- `SVC_SAM` - SAM bridge(默认端口 7656)
- `SVC_SAM_SSL` - SAM bridge SSL
- `SVC_SAM_UDP` - SAM UDP
- `SVC_BOB` - BOB bridge(默认端口 2827)
- `SVC_EEPSITE` - 标准 eepsite(默认端口 7658)
- `SVC_HTTPS_EEPSITE` - HTTPS eepsite
- `SVC_IRC` - IRC tunnel(默认端口 6668)
- `SVC_SUSIDNS` - SusiDNS

注意：`httpclient`、`httpsclient` 和 `httpbidirclient` 是 i2ptunnel tunnel 类型（用于 `tunnel.N.type` 配置），而不是端口映射器服务常量。

## 4. 客户端注册表

### 2.1 生命周期方法

从 0.9.42 版本开始,router 支持将配置拆分为 `clients.config.d/` 目录中的单个文件。每个文件包含单个客户端的属性,所有属性都以 `clientApp.0.` 为前缀:

```
clientApp.0.main=net.i2p.router.web.RouterConsoleRunner
clientApp.0.name=Router Console
clientApp.0.args=7657 ::1,127.0.0.1 ./webapps/
clientApp.0.delay=0
clientApp.0.onBoot=true
```
这是新安装和插件的推荐方法。

### 2.2 优势

为了向后兼容,传统格式使用顺序编号:

```
clientApp.0.main=net.i2p.router.web.RouterConsoleRunner
clientApp.0.name=Router Console
clientApp.0.args=7657 ::1,127.0.0.1 ./webapps/
clientApp.1.main=net.i2p.apps.systray.UrlLauncher
clientApp.1.name=URL Launcher
clientApp.1.delay=5
```
### 6.3 Configuration Properties

**必需：** - `main` - 实现 ClientApp 或 RouterApp 的完整类名，或包含静态 `main(String[] args)` 方法的类名

**可选：** - `name` - router console 的显示名称（默认为类名）- `args` - 空格或制表符分隔的参数（支持带引号的字符串）- `delay` - 启动前的延迟秒数（默认 120）- `onBoot` - 如果为 true 则强制 `delay=0` - `startOnLoad` - 启用/禁用客户端（默认 true）

**插件特定配置：** - `stopargs` - 关闭时传递的参数 - `uninstallargs` - 插件卸载时传递的参数 - `classpath` - 以逗号分隔的额外 classpath 条目

**插件的变量替换：** - `$I2P` - I2P 基础目录 - `$CONFIG` - 用户配置目录（例如，~/.i2p） - `$PLUGIN` - 插件目录 - `$OS` - 操作系统名称 - `$ARCH` - 架构名称

## 5. 端口映射器

- 优先使用托管客户端；仅在绝对必要时才回退到非托管客户端。
- 保持初始化和关闭过程轻量化,以确保控制台操作保持响应。
- 使用描述性的注册表和端口名称,以便诊断工具(和最终用户)了解服务的作用。
- 避免使用静态单例 - 依赖注入的上下文和管理器来共享资源。
- 在所有状态转换时调用 `manager.notify()` 以维护准确的控制台状态。
- 如果必须在单独的 JVM 中运行,请记录如何将日志和诊断信息呈现到主控制台。
- 对于外部程序,考虑使用 ShellService(在 1.7.0 版本中添加)以获得托管客户端的优势。

## 6. 配置格式

托管客户端在 **0.9.4 版本**（2012 年 12 月 17 日）中引入，并且截至 **2.10.0 版本**（2025 年 9 月 9 日）仍然是推荐的架构。在此期间，核心 API 保持稳定，没有任何破坏性变更：

- 构造函数签名保持不变
- 生命周期方法(startup、shutdown、getState)保持不变
- ClientAppManager 注册方法保持不变
- PortMapper 注册和查找方法保持不变

重要改进： - **0.9.42 (2019)** - clients.config.d/ 目录结构，用于存放独立配置文件 - **1.7.0 (2021)** - 新增 ShellService，用于外部程序状态跟踪 - **2.10.0 (2025)** - 当前版本，managed client API 无变更

下一个主要版本将要求至少 Java 17+（基础设施要求,而非 API 变更）。

## References

- [clients.config 规范](/docs/specs/configuration/#clients-config)
- [配置文件规范](/docs/specs/configuration/)
- [I2P 技术文档索引](/docs/)
- [ClientAppManager Javadoc](https://i2p.github.io/i2p.i2p/net/i2p/app/ClientAppManager.html) (API 0.9.66)
- [PortMapper Javadoc](https://i2p.github.io/i2p.i2p/net/i2p/util/PortMapper.html) (API 0.9.66)
- [ClientApp 接口](https://i2p.github.io/i2p.i2p/net/i2p/app/ClientApp.html) (API 0.9.66)
- [RouterApp 接口](https://i2p.github.io/i2p.i2p/net/i2p/router/app/RouterApp.html) (API 0.9.66)
- [备用 Javadoc (稳定版)](https://docs.i2p-projekt.de/javadoc/)
- [备用 Javadoc (明网镜像)](https://eyedeekay.github.io/javadoc-i2p/)

> **注意：** I2P 网络在 http://idk.i2p/javadoc-i2p/ 托管了完整的文档，访问需要 I2P router。如需通过明网访问，请使用上述 GitHub Pages 镜像。
