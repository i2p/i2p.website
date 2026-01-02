---
title: "安装自定义插件"
description: "安装、更新和开发路由器插件"
slug: "plugins"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

I2P 的插件框架允许您在不修改核心安装的情况下扩展 router 功能。可用的插件涵盖邮件、博客、IRC、存储、wiki、监控工具等。

> **安全提示：**插件以与路由器相同的权限运行。对待第三方下载应与对待任何已签名的软件更新一样——在安装前验证来源。

## 1. 安装插件

1. 从项目页面复制插件的下载 URL。  
   ![Copy plugin URL](/images/plugins/plugin-step-0.png)
2. 打开路由器控制台的[插件配置页面](http://127.0.0.1:7657/configplugins)。  
   ![Open plugin configuration](/images/plugins/plugin-step-1.png)
3. 将 URL 粘贴到安装字段中,然后点击 **Install Plugin**。  
   ![Install plugin](/images/plugins/plugin-step-2.png)

路由器会获取已签名的归档文件,验证签名,并立即激活插件。大多数插件会添加控制台链接或后台服务,无需重启路由器。

## 2. 为什么插件很重要

- 为终端用户提供一键分发——无需手动编辑 `wrapper.config` 或 `clients.config`
- 保持核心 `i2pupdate.su3` 包的精简，同时按需提供大型或小众功能
- 可选的每插件 JVM 在需要时提供进程隔离
- 自动检查与路由器版本、Java 运行时和 Jetty 的兼容性
- 更新机制与路由器一致：签名包和增量下载
- 支持控制台集成、语言包、UI 主题和非 Java 应用程序（通过脚本）
- 支持策划的"应用商店"目录，如 `plugins.i2p`

## 3. 管理已安装的插件

使用 [I2P Router Plugin's](http://127.0.0.1:7657/configclients.jsp#plugin) 上的控制选项来:

- 检查单个插件的更新
- 一次性检查所有插件（在 router 升级后自动触发）
- 一键安装所有可用更新  
  ![Update plugins](/images/plugins/plugin-update-0.png)
- 为注册服务的插件启用/禁用自动启动
- 干净地卸载插件

## 4. 构建你自己的插件

1. 查看[插件规范](/docs/specs/plugin/)了解打包、签名和元数据要求。
2. 使用 [`makeplugin.sh`](https://github.com/i2p/i2p.scripts/tree/master/plugin/makeplugin.sh) 将现有的二进制文件或 Web 应用程序封装成可安装的归档文件。
3. 发布安装和更新 URL,以便 router 能够区分首次安装和增量升级。
4. 在项目页面上醒目地提供校验和与签名密钥,帮助用户验证真实性。

寻找示例?浏览 `plugins.i2p` 上社区插件的源代码(例如 `snowman` 示例)。

## 5. 已知限制

- 更新包含纯 JAR 文件的插件可能需要重启路由器,因为 Java 类加载器会缓存类。
- 控制台可能显示 **停止** 按钮,即使插件没有活动进程。
- 在独立 JVM 中启动的插件会在当前工作目录中创建 `logs/` 目录。
- 签名密钥首次出现时会自动受信任;不存在中央签名机构。
- Windows 有时在卸载插件后会留下空目录。
- 在 Java 5 JVM 上安装仅支持 Java 6 的插件会因 Pack200 压缩而报告"插件已损坏"。
- 主题和翻译插件基本上未经测试。
- 自动启动标志对于非托管插件并不总是持久保存。

## 6. 要求与最佳实践

- I2P **0.7.12 及更新版本**支持插件功能。
- 保持路由器和插件更新以获取安全修复。
- 提供简明的版本说明，让用户了解版本之间的变化。
- 尽可能在 I2P 内通过 HTTPS 托管插件存档，以最小化明网元数据暴露。

## 7. 延伸阅读

- [插件规范](/docs/specs/plugin/)
- [客户端应用程序框架](/docs/applications/managed-clients/)
- [I2P 脚本仓库](https://github.com/i2p/i2p.scripts/) 用于打包工具
