---
title: "Router 配置"
description: "I2P routers 和客户端的配置选项与格式"
slug: "configuration"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## 概述

本文件提供了 I2P 配置文件的全面技术规范，这些配置文件由 router 和各类应用程序使用。内容涵盖文件格式规范、属性定义，以及已根据 I2P 源代码和官方文档核实的实现细节。

### 范围

- Router 的配置文件与格式
- 客户端应用程序配置
- I2PTunnel 的 tunnel 配置
- 文件格式规范与实现
- 版本特定的特性与弃用

### 实现说明

配置文件通过 I2P 核心库中的 `DataHelper.loadProps()` 和 `storeProps()` 方法进行读写。该文件格式与 I2P 协议中使用的序列化格式有显著差异（参见[通用结构规范 - 类型映射](/docs/specs/common-structures/#type-mapping)）。

---

## 通用配置文件格式

I2P 配置文件遵循经修改的 Java Properties 格式，并具有特定的例外和约束。

### 格式规范

基于 [Java Properties](http://docs.oracle.com/javase/1.5.0/docs/api/java/util/Properties.html#load%28java.io.InputStream%29)，但有以下关键差异：

#### 编码

- **必须** 使用 UTF-8 编码（不要使用 ISO-8859-1，正如标准的 Java Properties（属性文件） 所使用的那样）
- 实现：在所有文件操作中使用 `DataHelper.getUTF8()` 工具方法

#### 转义序列

- **不** 识别转义序列（包括反斜杠 `\`）
- **不** 支持续行
- 反斜杠字符按字面解释

#### 注释字符

- `#` 在一行的任意位置都会开始一条注释
- `;` **仅当** 位于第 1 列（行首）时才开始注释
- `!` **不会** 开始注释（与 Java Properties 不同）

#### 键值分隔符

- `=` 是**唯一**有效的键值分隔符
- `:` **不**被识别为分隔符
- 空白字符**不**被识别为分隔符

#### 空白字符处理

- 键的前后空白字符**不会**被去除
- 值的前后空白字符**会**被去除

#### 行处理

- 未包含 `=` 的行会被忽略（视为注释或空行）
- 自 0.9.10 版本起支持空值（`key=`）
- 值为空的键会被正常存储和读取

#### 字符限制

**键不得包含**: - `#` (井号/英镑符号) - `=` (等号) - `\n` (换行符) - 不得以 `;` 开头 (分号)

**值不得包含**: - `#`（井号） - `\n`（换行符） - 不能以 `\r`（回车符）开头或结尾 - 不能以空白字符开头或结尾（会自动去除首尾空白）

### 文件排序

配置文件不必按键名排序。然而，大多数 I2P 应用程序在写入配置文件时，会按字母顺序对键名进行排序，以便： - 手动编辑 - 版本控制中的 diff（差异比较）操作 - 提高可读性

### 实现细节

#### 读取配置文件

```java
// Method signature from net.i2p.data.DataHelper
public static Properties loadProps(File file)
```
**行为**: - 读取 UTF-8 编码的文件 - 强制执行上述所有格式规则 - 验证字符限制 - 如果文件不存在，则返回空的 Properties 对象 - 读取错误时抛出 `IOException`

#### 编写配置文件

```java
// Method signature from net.i2p.data.DataHelper
public static void storeProps(Properties props, File file)
```
**行为**: - 写入 UTF-8 编码的文件 - 按字母顺序对键排序（除非使用 OrderedProperties（有序属性类）） - 将文件权限设置为 600 模式（仅用户读/写），自 0.8.1 版本起 - 对键或值中的无效字符抛出 `IllegalArgumentException` - 对写入错误抛出 `IOException`

#### 格式验证

该实现进行严格验证：
- 键和值会被检查是否包含禁止字符
- 无效条目会在写入操作时引发异常
- 读取时会静默忽略格式不正确的行（不含`=`的行）

### 格式示例

#### 有效的配置文件

```properties
# This is a comment
; This is also a comment (column 1 only)
key.with.dots=value with spaces
another_key=value=with=equals
empty.value=
numeric.value=12345
unicode.value=こんにちは
```
#### 无效配置示例

```properties
# INVALID: Key contains equals sign
invalid=key=value

# INVALID: Key contains hash
invalid#key=value

# INVALID: Value contains newline (implicit)
key=value
continues here

# INVALID: Semicolon comment not in column 1 (treated as key)
 ; not.a.comment=value
```
---

## 核心库与 Router 配置

### 客户端配置 (clients.config)

**位置**: `$I2P_CONFIG_DIR/clients.config` (旧版) 或 `$I2P_CONFIG_DIR/clients.config.d/` (现代)   **配置界面**: Router 控制台位于 `/configclients`   **格式变更**: 版本 0.9.42 (2019 年 8 月)

#### 目录结构 (版本 0.9.42+)

自 0.9.42 版本起，默认的 clients.config 文件会自动拆分为单独的配置文件：

```
$I2P_CONFIG_DIR/
├── clients.config.d/
│   ├── 00-webConsole.config
│   ├── 01-i2ptunnel.config
│   ├── 02-i2psnark.config
│   ├── 03-susidns.config
│   └── ...
└── clients.config (legacy, auto-migrated)
```
**迁移行为**: - 升级到 0.9.42+ 后首次运行时，将自动拆分单体文件 - 拆分文件中的属性以 `clientApp.0.` 为前缀 - 为向后兼容仍然支持旧格式 - 拆分格式支持模块化打包与插件管理

#### 属性格式

各行的形式为 `clientApp.x.prop=val`，其中 `x` 是应用编号。

**应用编号要求**: - 必须从 0 开始 - 必须连续（不得跳号） - 顺序决定启动顺序

#### 必需属性

##### 主要

- **类型**: 字符串（完全限定类名）
- **必需**: 是
- **描述**: 将根据客户端类型（受管 vs. 非受管）调用此类中的构造函数或 `main()` 方法
- **示例**: `clientApp.0.main=net.i2p.router.web.RouterConsoleRunner`

#### 可选属性

##### 名称

- **类型**: 字符串
- **是否必需**: 否
- **描述**: 在 router 控制台中显示的名称
- **示例**: `clientApp.0.name=Router Console`

##### 参数

- **类型**: 字符串（以空格或制表符分隔）
- **是否必需**: 否
- **说明**: 传递给主类构造函数或 main() 方法的参数
- **引用**: 含有空格或制表符的参数可以用 ' 或 " 括起来
- **示例**: `clientApp.0.args=-d $CONFIG/eepsite`

##### 延迟

- **类型**: 整数（秒）
- **必需**: 否
- **默认值**: 120
- **描述**: 在启动客户端之前等待的秒数
- **覆盖**: 被 `onBoot=true` 覆盖（将延迟设为 0）
- **特殊值**:
  - `< 0`: 等待 router 达到 RUNNING 状态，然后在新线程中立即启动
  - `= 0`: 在同一线程中立即运行（异常会传播到控制台）
  - `> 0`: 在延迟之后于新线程中启动（异常会被记录到日志，不会传播）

##### onBoot

- **类型**: 布尔值
- **必需**: 否
- **默认值**: false
- **说明**: 将延迟强制设为 0，覆盖显式的延迟设置
- **用例**: 在 router 启动时立即启动关键服务

##### startOnLoad

- **类型**: 布尔值
- **是否必需**: 否
- **默认值**: true
- **描述**: 是否启动客户端
- **使用场景**: 在不删除配置的情况下禁用客户端

#### 插件特定属性

这些属性仅供插件使用（非核心客户端）：

##### stopargs

- **类型**: 字符串（以空格或制表符分隔）
- **描述**: 用于停止客户端时传递的参数
- **变量替换**: 是（见下文）

##### uninstallargs

- **类型**: 字符串（以空格或制表符分隔）
- **描述**: 用于卸载客户端时传入的参数
- **变量替换**: 是（见下文）

##### 类路径

- **类型**: 字符串（逗号分隔的路径）
- **描述**: 客户端的附加 classpath（类路径）元素
- **变量替换**: 是（见下文）

#### 变量替换（仅限插件）

在插件的 `args`、`stopargs`、`uninstallargs` 和 `classpath` 中，会替换以下变量：

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Variable</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Expands To</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Example</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$I2P</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Base I2P installation directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>/usr/share/i2p</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$CONFIG</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">User configuration directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>~/.i2p</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$PLUGIN</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Plugin directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>~/.i2p/plugins/foo</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$OS</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Operating system name</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>linux</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$ARCH</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Architecture name</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>amd64</code></td>
    </tr>
  </tbody>
</table>
**注意**：变量替换仅适用于插件，不适用于核心客户端。

#### 客户端类型

##### 受管客户端

- 构造函数会以 `RouterContext` 和 `ClientAppManager` 作为参数被调用
- 客户端必须实现 `ClientApp` 接口
- 生命周期由 router 控制
- 可动态启动、停止和重启

##### 未托管客户端

- `main(String[] args)` 方法被调用
- 在独立线程中运行
- 生命周期不由 router 管理
- 遗留客户端类型

#### 示例配置

```properties
# Router Console (core client)
clientApp.0.main=net.i2p.router.web.RouterConsoleRunner
clientApp.0.name=Router Console
clientApp.0.args=-d $CONFIG/eepsite
clientApp.0.delay=0
clientApp.0.onBoot=true
clientApp.0.startOnLoad=true

# I2PTunnel (core client)
clientApp.1.main=net.i2p.i2ptunnel.TunnelControllerGroup
clientApp.1.name=I2PTunnel
clientApp.1.args=
clientApp.1.delay=120
clientApp.1.startOnLoad=true

# Plugin Example
clientApp.2.main=org.example.plugin.PluginMain
clientApp.2.name=Example Plugin
clientApp.2.args=-config $PLUGIN/config.properties
clientApp.2.stopargs=-shutdown
clientApp.2.uninstallargs=-remove $PLUGIN
clientApp.2.classpath=$PLUGIN/lib/plugin.jar,$PLUGIN/lib/dep.jar
clientApp.2.delay=240
clientApp.2.startOnLoad=true
```
---

### 日志记录器配置 (logger.config)

**位置**: `$I2P_CONFIG_DIR/logger.config`   **配置界面**: Router 控制台的 `/configlogging`

#### 属性参考

##### 控制台缓冲区配置

###### logger.consoleBufferSize

- **类型**: 整数
- **默认值**: 20
- **描述**: 在控制台中可缓冲的日志消息最大数量
- **范围**: 建议 1-1000

##### 日期和时间格式化

###### logger.dateFormat

- **类型**: 字符串 (SimpleDateFormat 模式)
- **默认**: 来自系统区域设置
- **示例**: `HH:mm:ss.SSS`
- **文档**: [Java SimpleDateFormat](https://docs.oracle.com/javase/8/docs/api/java/text/SimpleDateFormat.html)

##### 日志级别

###### logger.defaultLevel

- **类型**: 枚举
- **默认**: ERROR
- **可选值**: `CRIT`, `ERROR`, `WARN`, `INFO`, `DEBUG`
- **描述**: 所有类的默认日志级别

###### logger.minimumOnScreenLevel

- **类型**: 枚举
- **默认值**: CRIT
- **可选值**: `CRIT`, `ERROR`, `WARN`, `INFO`, `DEBUG`
- **说明**: 在屏幕上显示的消息的最低级别

###### logger.record.{class}

- **类型**: 枚举
- **取值**: `CRIT`, `ERROR`, `WARN`, `INFO`, `DEBUG`
- **描述**: 针对各个类的日志级别覆盖
- **示例**: `logger.record.net.i2p.router.transport.udp=DEBUG`

##### 显示选项

###### logger.displayOnScreen

- **类型**: 布尔值
- **默认值**: true
- **描述**: 是否在控制台输出中显示日志消息

###### logger.dropDuplicates

- **类型**: 布尔
- **默认值**: true
- **描述**: 丢弃连续重复的日志消息

###### logger.dropOnOverflow

- **类型**: 布尔
- **默认值**: false
- **描述**: 当缓冲区已满时丢弃消息（而非阻塞）

##### 刷新行为

###### logger.flushInterval

- **类型**: 整数（秒）
- **默认值**: 29
- **起始版本**: 0.9.18
- **描述**: 将日志缓冲区刷新到磁盘的频率

##### 格式配置

###### logger.format

- **类型**: 字符串（字符序列）
- **描述**: 日志消息格式模板
- **格式字符**:
  - `d` = 日期/时间
  - `c` = 类名
  - `t` = 线程名
  - `p` = 优先级（日志级别）
  - `m` = 消息
- **示例**: `dctpm` 会生成 `[时间戳] [类] [线程] [级别] 消息`

##### 压缩（版本 0.9.56+）

###### logger.gzip

- **类型**: 布尔值
- **默认值**: false
- **自**: 版本 0.9.56
- **描述**: 为已轮换的日志文件启用 gzip 压缩

###### logger.minGzipSize

- **类型**: 整数（字节）
- **默认值**: 65536
- **自版本**: 0.9.56
- **描述**: 触发压缩的最小文件大小（默认 64 KB）

##### 文件管理

###### logger.logBufferSize

- **类型**: 整数（字节）
- **默认值**: 1024
- **描述**: 在触发刷新前可缓冲的最大消息数

###### logger.logFileName

- **类型**: 字符串（文件路径）
- **默认值**: `logs/log-@.txt`
- **描述**: 日志文件命名模式（`@` 将被替换为轮转编号）

###### logger.logFilenameOverride

- **类型**: 字符串（文件路径）
- **描述**: 用于覆盖日志文件名（会禁用轮转模式）

###### logger.logFileSize

- **类型**: 字符串（带单位的大小）
- **默认值**: 10M
- **单位**: K（千字节）、M（兆字节）、G（吉字节）
- **示例**: `50M`, `1G`

###### logger.logRotationLimit

- **类型**: 整数
- **默认值**: 2
- **描述**: 轮转日志文件的最大编号 (log-0.txt 到 log-N.txt)

#### 示例配置

```properties
# Basic logging configuration
logger.consoleBufferSize=50
logger.dateFormat=yyyy-MM-dd HH:mm:ss.SSS
logger.defaultLevel=WARN
logger.displayOnScreen=true
logger.dropDuplicates=true
logger.dropOnOverflow=false

# Flushing and format
logger.flushInterval=30
logger.format=dctpm

# File management
logger.logBufferSize=2048
logger.logFileName=logs/log-@.txt
logger.logFileSize=25M
logger.logRotationLimit=5

# Compression (0.9.56+)
logger.gzip=true
logger.minGzipSize=131072

# On-screen filtering
logger.minimumOnScreenLevel=ERROR

# Per-class overrides
logger.record.net.i2p.router.transport=INFO
logger.record.net.i2p.router.tunnel=DEBUG
logger.record.net.i2p.crypto=WARN
```
---

### 插件配置

#### 单个插件配置 (plugins/*/plugin.config)

**位置**: `$I2P_CONFIG_DIR/plugins/{plugin-name}/plugin.config`   **格式**: 标准 I2P 配置文件格式   **文档**: [插件规范](/docs/specs/plugin/)

##### 必需属性

###### 名称

- **类型**: 字符串
- **必需**: 是
- **描述**: 插件显示名称
- **示例**: `name=I2P Plugin Example`

###### 密钥

- **类型**: 字符串（公钥）
- **是否必需**: 是（对于使用 SU3 签名的插件可省略）
- **说明**: 用于验证插件签名的公钥
- **格式**: Base64 编码的签名公钥

###### 签名者

- **类型**: 字符串
- **必需**: 是
- **描述**: 插件签名者身份
- **示例**: `signer=user@example.i2p`

###### 版本

- **类型**: 字符串（VersionComparator 格式，用于比较版本号）
- **必需**: 是
- **描述**: 用于更新检查的插件版本
- **格式**: 语义化版本（Semantic Versioning）或自定义可比较格式
- **示例**: `version=1.2.3`

##### 显示属性

###### 日期

- **类型**: Long (以毫秒为单位的 Unix 时间戳)
- **描述**: 插件发布日期

###### 作者

- **类型**: 字符串
- **描述**: 插件作者名称

###### websiteURL

- **类型**: 字符串 (URL)
- **描述**: 插件网站 URL

###### updateURL

- **类型**: 字符串 (URL)
- **描述**: 用于插件的更新检查 URL

###### updateURL.su3

- **类型**: 字符串（URL）
- **自**: 版本 0.9.15 起
- **描述**: SU3 格式的更新 URL（首选）

###### 描述

- **类型**: 字符串
- **描述**: 插件的英文描述

###### description_{language}

- **类型**: 字符串
- **描述**: 本地化的插件描述
- **示例**: `description_de=Deutsche Beschreibung`

###### 许可证

- **类型**: 字符串
- **描述**: 插件许可证标识符
- **示例**: `license=Apache 2.0`

##### 安装属性

###### 不要在安装时启动

- **类型**: 布尔值
- **默认值**: false
- **描述**: 防止在安装后自动启动

###### 需要重启 router

- **类型**: 布尔值
- **默认值**: false
- **描述**: 安装后需要重启 router

###### 仅安装

- **类型**: 布尔类型
- **默认值**: false
- **描述**: 仅安装一次（不更新）

###### 仅更新

- **类型**: 布尔值
- **默认值**: false
- **说明**: 仅更新现有安装（不进行全新安装）

##### 示例插件配置

```properties
# Required properties
name=Example I2P Plugin
signer=developer@mail.i2p
version=1.5.0

# Display properties
author=Plugin Developer
websiteURL=http://plugin.example.i2p
updateURL=http://plugin.example.i2p/update.xpi2p
updateURL.su3=http://plugin.example.i2p/update.su3
description=Example plugin demonstrating configuration
description_de=Beispiel-Plugin zur Demonstration der Konfiguration
license=MIT

# Installation behavior
dont-start-at-install=false
router-restart-required=false
```
#### 全局插件配置 (plugins.config)

**位置**: `$I2P_CONFIG_DIR/plugins.config`   **用途**: 全局启用/禁用已安装的插件

##### 属性格式

```properties
plugin.{name}.startOnLoad=true|false
```
- `{name}`: 来自 plugin.config 的插件名称
- `startOnLoad`: 是否在 router 启动时自动启动插件

##### 示例

```properties
plugin.i2psnark.startOnLoad=true
plugin.susimail.startOnLoad=true
plugin.susidns.startOnLoad=true
plugin.i2pbote.startOnLoad=false
```
---

### Web 应用程序配置（webapps.config）

**位置**: `$I2P_CONFIG_DIR/webapps.config`   **用途**: 启用/禁用并配置 Web 应用程序

#### 属性格式

##### webapps.{name}.startOnLoad

- **类型**: 布尔值
- **描述**: 是否在 router 启动时启动 Web 应用
- **格式**: `webapps.{name}.startOnLoad=true|false`

##### webapps.{name}.classpath

- **类型**: 字符串 (以空格或逗号分隔的路径)
- **描述**: 用于 Web 应用的额外类路径元素
- **格式**: `webapps.{name}.classpath=[paths]`

#### 变量替换

路径支持以下变量替换：

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Variable</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Expands To</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Context</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$I2P</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Base I2P directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Core webapps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$CONFIG</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">User config directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">All webapps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$PLUGIN</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Plugin directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Plugin webapps</td>
    </tr>
  </tbody>
</table>
#### 类路径解析

- **核心 Web 应用**：相对于 `$I2P/lib` 的路径
- **插件 Web 应用**：相对于 `$CONFIG/plugins/{appname}/lib` 的路径

#### 示例配置

```properties
# Router console
webapps.routerconsole.startOnLoad=true
webapps.routerconsole.classpath=routerconsole.jar

# I2PSnark
webapps.i2psnark.startOnLoad=true
webapps.i2psnark.classpath=i2psnark.jar

# SusiDNS
webapps.susidns.startOnLoad=true
webapps.susidns.classpath=susidns.jar

# Plugin webapp example
webapps.exampleplugin.startOnLoad=false
webapps.exampleplugin.classpath=$PLUGIN/lib/webapp.jar,$PLUGIN/lib/deps.jar
```
---

### Router 配置 (router.config)

**位置**: `$I2P_CONFIG_DIR/router.config`   **配置界面**: Router 控制台位于 `/configadvanced`   **用途**: 核心 Router 设置和网络参数

#### 配置类别

##### 网络配置

带宽设置:

```properties
i2np.bandwidth.inboundKBytesPerSecond=100
i2np.bandwidth.outboundKBytesPerSecond=50
i2np.bandwidth.share.percentage=80
```
传输配置：

```properties
# NTCP (TCP-based transport)
i2np.ntcp.port=8887
i2np.ntcp.enable=true
i2np.ntcp.autoip=true

# SSU (UDP-based transport)
i2np.udp.port=8887
i2np.udp.enable=true

# UPnP/NAT-PMP
i2np.upnp.enable=true
```
##### Router 行为

```properties
# Tunnel participation
router.maxParticipatingTunnels=200
router.sharePercentage=80

# Updates
router.updatePolicy=notify
router.updateURL=http://update.i2p2.i2p/

# Network integration
router.hiddenMode=false
router.clockSkewOffset=0
```
##### 控制台配置

```properties
# Language and display
routerconsole.lang=en
routerconsole.country=US
routerconsole.summaryRefresh=60

# Browser
routerconsole.browser=default

# Security
routerconsole.enableCompression=true
```
##### 时间配置

```properties
# NTP
time.disabled=false
time.sntpServerList=0.pool.ntp.org,1.pool.ntp.org
```
**注意**：Router 配置内容繁多。请在 router 控制台的 `/configadvanced` 页面查看完整的属性参考。

---

## 应用程序配置文件

### 地址簿配置 (addressbook/config.txt)

**位置**: `$I2P_CONFIG_DIR/addressbook/config.txt`   **应用**: SusiDNS   **用途**: 主机名解析和地址簿管理

#### 文件位置

##### router_addressbook

- **默认**: `../hosts.txt`
- **描述**: 主地址簿（系统范围的主机名）
- **格式**: 标准 hosts 文件格式

##### privatehosts.txt

- **位置**: `$I2P_CONFIG_DIR/addressbook/privatehosts.txt`
- **描述**: 私有主机名映射
- **优先级**: 最高（覆盖所有其他来源）

##### userhosts.txt

- **位置**: `$I2P_CONFIG_DIR/addressbook/userhosts.txt`
- **描述**: 用户添加的主机名映射
- **管理**: 通过 SusiDNS 界面

##### hosts.txt

- **位置**: `$I2P_CONFIG_DIR/addressbook/hosts.txt`
- **描述**: 已下载的公共地址簿
- **来源**: 订阅源

#### 命名服务

##### BlockfileNamingService (自 0.8.8 起为默认)

存储格式： - **文件**: `hostsdb.blockfile` - **位置**: `$I2P_CONFIG_DIR/addressbook/` - **性能**: 查询速度比 hosts.txt 快约 10 倍 - **格式**: 二进制数据库格式

旧版命名服务： - **格式**：纯文本 hosts.txt - **状态**：已弃用但仍受支持 - **使用场景**：手动编辑、版本控制

#### 主机名规则

I2P 主机名必须符合以下规范：

1. **顶级域名要求**: 必须以 `.i2p` 结尾
2. **最大长度**: 总计 67 个字符
3. **字符集**: `[a-z]`, `[0-9]`, `.` (句点), `-` (连字符)
4. **大小写**: 仅限小写
5. **开头限制**: 不能以 `.` 或 `-` 开头
6. **禁止的模式**: 不能包含 `..`、`.-` 或 `-.` (自 0.6.1.33 起)
7. **保留**: Base32 主机名 `*.b32.i2p` (52 个字符的 base32.b32.i2p)

##### 有效示例

```
example.i2p
my-site.i2p
test.example.i2p
site123.i2p
```
##### 无效示例

```
example.com          # Wrong TLD
-invalid.i2p         # Starts with hyphen
invalid..i2p         # Contains double dot
invalid.-.i2p        # Contains dot-hyphen
UPPERCASE.I2P        # Must be lowercase
verylonghostnameover67charactersthatexceedsthemaximumlength.i2p  # Too long
```
#### 订阅管理

##### subscriptions.txt

- **位置**: `$I2P_CONFIG_DIR/addressbook/subscriptions.txt`
- **格式**: 每行一个 URL
- **默认值**: `http://i2p-projekt.i2p/hosts.txt`

##### 订阅源格式（自 0.9.26 起）

带有元数据的高级提要格式：

```
#
# I2P Address Book Subscription Feed
# Format: hostname=destination [#property=value ...]
#

example.i2p=base64destination #added=20250101 #src=manual
another.i2p=base64destination #added=20250102 #src=feed1
```
元数据属性: - `added`: 主机名添加的日期 (YYYYMMDD 格式) - `src`: 来源标识符 - `sig`: 可选签名

**向后兼容性**: 简单的 hostname=destination 格式仍然受支持。

#### 示例配置

```properties
# Address book locations
router_addressbook=../hosts.txt
privatehosts.txt=$CONFIG/addressbook/privatehosts.txt
userhosts.txt=$CONFIG/addressbook/userhosts.txt
hosts.txt=$CONFIG/addressbook/hosts.txt

# Naming service
naming.service=BlockfileNamingService
naming.service.blockfile.location=$CONFIG/addressbook/hostsdb.blockfile

# Subscriptions
subscriptions.txt=$CONFIG/addressbook/subscriptions.txt
subscriptions.schedule=daily
subscriptions.proxy=false
```
---

### I2PSnark 配置 (i2psnark.config.d/i2psnark.config)

**位置**: `$I2P_CONFIG_DIR/i2psnark.config.d/i2psnark.config`   **应用程序**: I2PSnark BitTorrent 客户端   **配置界面**: Web 界面位于 http://127.0.0.1:7657/i2psnark

#### 目录结构

```
$I2P_CONFIG_DIR/i2psnark.config.d/
├── i2psnark.config
├── [torrent-hash-1]/
│   └── *.config
├── [torrent-hash-2]/
│   └── *.config
└── ...
```
#### 主配置 (i2psnark.config)

最小默认配置：

```properties
i2psnark.dir=i2psnark
```
可通过 Web 界面管理的附加属性：

```properties
# Basic settings
i2psnark.dir=i2psnark
i2psnark.autoStart=false
i2psnark.openTrackers=true

# Network settings
i2psnark.uploaders=8
i2psnark.upBW=40
i2psnark.seedPct=100

# I2CP settings
i2psnark.i2cpHost=127.0.0.1
i2psnark.i2cpPort=7654
```
#### 单个种子配置

**位置**: `$I2P_CONFIG_DIR/i2psnark.config.d/[torrent-hash]/*.config`   **格式**: 每个种子的设置   **管理**: 自动（通过 Web GUI）

属性包括： - 针对种子的上传/下载设置 - 文件优先级 - 跟踪器信息 - 对等节点限制

**注意**: Torrent 配置主要通过 Web 界面进行管理。不建议手动编辑。

#### 种子数据组织

数据存储与配置彼此独立：

```
$I2P_CONFIG_DIR/i2psnark/          # Data directory
├── *.torrent                       # Torrent metadata files
├── *.torrent.downloaded/           # Downloaded file directories
├── file1.dat                       # Direct file downloads
└── ...

$I2P_CONFIG_DIR/i2psnark.config.d/ # Configuration directory
├── i2psnark.config                 # Main config
└── [hashes]/                       # Per-torrent configs
```
---

### I2PTunnel 配置 (i2ptunnel.config)

**位置**: `$I2P_CONFIG_DIR/i2ptunnel.config`（旧版）或 `$I2P_CONFIG_DIR/i2ptunnel.config.d/`（现代版）   **配置界面**: Router 控制台位于 `/i2ptunnel`   **格式变更**: 版本 0.9.42（2019 年 8 月）

#### 目录结构 (版本 0.9.42+)

自 0.9.42 版本起，默认的 i2ptunnel.config 文件将自动拆分：

```
$I2P_CONFIG_DIR/
├── i2ptunnel.config.d/
│   ├── http-proxy/
│   │   └── tunnel.config
│   ├── irc-proxy/
│   │   └── tunnel.config
│   ├── ssh-service/
│   │   └── tunnel.config
│   └── ...
└── i2ptunnel.config (legacy, auto-migrated)
```
**关键格式差异**: - **单体格式**: 属性以 `tunnel.N.` 为前缀 - **拆分格式**: 属性**不**带前缀（例如，`description=`，而不是 `tunnel.0.description=`）

#### 迁移行为

在升级到 0.9.42 后首次运行： 1. 读取现有 i2ptunnel.config 2. 在 i2ptunnel.config.d/ 中创建各个 tunnel 的配置文件 3. 在拆分后的文件中去除属性前缀 4. 备份原始文件 5. 仍支持旧格式以保持向后兼容

#### 配置部分

I2PTunnel 配置的详细说明见下文的 [I2PTunnel 配置参考](#i2ptunnel-configuration-reference) 部分。属性说明适用于单一式（`tunnel.N.property`）和拆分式（`property`）两种格式。

---

## I2PTunnel 配置参考

本节提供 I2PTunnel 全部配置属性的全面技术参考。属性以拆分格式展示（不带 `tunnel.N.` 前缀）。若使用单体格式，则为所有属性添加 `tunnel.N.` 前缀，其中 N 为该 tunnel 的编号。

**重要**：被描述为 `tunnel.N.option.i2cp.*` 的属性仅在 I2PTunnel（I2P 隧道工具）中实现，且**不**受其他接口（例如 I2CP protocol（I2CP 协议）或 SAM API（SAM 接口））支持。

### 基本属性

#### tunnel.N.description (描述)

- **类型**: 字符串
- **上下文**: 所有 tunnels
- **描述**: 用于 UI 显示的人类可读的 tunnel 描述
- **示例**: `description=HTTP Proxy for outproxy access`

#### tunnel.N.name (名称)

- **类型**: 字符串
- **上下文**: 所有 tunnel
- **必需**: 是
- **描述**: 唯一的 tunnel 标识符和显示名称
- **示例**: `name=I2P HTTP Proxy`

#### tunnel.N.type (类型)

- **类型**: 枚举
- **上下文**: 所有 tunnel
- **必需**: 是
- **取值**:
  - `client` - 通用客户端 tunnel
  - `httpclient` - HTTP 代理客户端
  - `ircclient` - IRC 客户端 tunnel
  - `socksirctunnel` - SOCKS IRC 代理
  - `sockstunnel` - SOCKS 代理（版本 4、4a、5）
  - `connectclient` - CONNECT 代理客户端
  - `streamrclient` - Streamr 客户端
  - `server` - 通用服务器 tunnel
  - `httpserver` - HTTP 服务器 tunnel
  - `ircserver` - IRC 服务器 tunnel
  - `httpbidirserver` - 双向 HTTP 服务器
  - `streamrserver` - Streamr 服务器

#### tunnel.N.interface (接口)

- **类型**: 字符串（IP 地址或主机名）
- **上下文**: 仅适用于 Client tunnels（I2P 中的隧道）
- **默认值**: 127.0.0.1
- **描述**: 用于绑定传入连接的本地接口
- **安全说明**: 绑定到 0.0.0.0 将允许远程连接
- **示例**: `interface=127.0.0.1`

#### tunnel.N.listenPort (listenPort)

- **类型**: 整数
- **上下文**: 仅适用于 Client tunnels（客户端隧道）
- **范围**: 1-65535
- **描述**: 用于监听客户端连接的本地端口
- **示例**: `listenPort=4444`

#### tunnel.N.targetHost (targetHost)

- **类型**: 字符串（IP 地址或主机名）
- **上下文**: 仅限 Server tunnels
- **描述**: 用于转发连接的本地目标服务器
- **示例**: `targetHost=127.0.0.1`

#### tunnel.N.targetPort (targetPort)

- **类型**: 整数
- **上下文**: 仅用于服务器 tunnels
- **范围**: 1-65535
- **描述**: 要连接的 targetHost 上的端口
- **示例**: `targetPort=80`

#### tunnel.N.targetDestination (targetDestination)

- **类型**: 字符串（以逗号或空格分隔的目标地址）
- **上下文**: 仅限 Client tunnels
- **格式**: `destination[:port][,destination[:port]]`
- **描述**: 要连接的 I2P 目标地址（Destination）
- **示例**:
  - `targetDestination=example.i2p`
  - `targetDestination=example.i2p:8080`
  - `targetDestination=site1.i2p,site2.i2p:8080`

#### tunnel.N.i2cpHost (i2cpHost)

- **类型**: 字符串（IP 地址或主机名）
- **默认值**: 127.0.0.1
- **描述**: I2P router 的 I2CP 接口地址
- **注意**: 在 router 上下文中运行时将被忽略
- **示例**: `i2cpHost=127.0.0.1`

#### tunnel.N.i2cpPort (i2cpPort)

- **类型**: 整数
- **默认值**: 7654
- **范围**: 1-65535
- **描述**: I2P router 的 I2CP 端口
- **注意**: 在 router 上下文中运行时会被忽略
- **示例**: `i2cpPort=7654`

#### tunnel.N.startOnLoad (startOnLoad)

- **类型**: 布尔值
- **默认值**: true
- **说明**: 当 I2PTunnel 加载时是否启动 tunnel
- **示例**: `startOnLoad=true`

### 代理配置

#### tunnel.N.proxyList (proxyList)

- **类型**: 字符串（以逗号或空格分隔的主机名）
- **适用范围**: 仅限 HTTP 和 SOCKS 代理
- **描述**: outproxy（出站代理）主机列表
- **示例**: `proxyList=outproxy.example.i2p,backup.example.i2p`

### 服务器配置

#### tunnel.N.privKeyFile (privKeyFile)

- **类型**: 字符串（文件路径）
- **适用范围**: 服务器和持久化客户端 tunnels（隧道）
- **描述**: 包含持久化目标私钥的文件
- **路径**: 绝对路径或相对于 I2P 配置目录
- **示例**: `privKeyFile=eepsite/eepPriv.dat`

#### tunnel.N.spoofedHost (spoofedHost)

- **类型**: 字符串（主机名）
- **上下文**: 仅适用于 HTTP 服务器
- **默认值**: 目标（destination）的 Base32 主机名
- **描述**: 传递给本地服务器的 Host 请求头值
- **示例**: `spoofedHost=example.i2p`

#### tunnel.N.spoofedHost.NNNN (spoofedHost.NNNN)

- **类型**: 字符串（主机名）
- **适用范围**: 仅限 HTTP 服务器
- **描述**: 针对特定入站端口的虚拟主机覆盖
- **用例**: 在不同端口上托管多个站点
- **示例**: `spoofedHost.8080=site1.example.i2p`

### 客户端特定选项

#### tunnel.N.sharedClient (sharedClient)

- **类型**: 布尔值
- **上下文**: 仅适用于 Client tunnels
- **默认值**: false
- **描述**: 是否允许多个客户端共享该 tunnel
- **示例**: `sharedClient=false`

#### tunnel.N.option.persistentClientKey (persistentClientKey)

- **类型**: 布尔值
- **上下文**: 仅适用于客户端 tunnel
- **默认值**: false
- **描述**: 在重启之间保存并复用目标密钥
- **冲突**: 与 `i2cp.newDestOnResume=true` 互斥
- **示例**: `option.persistentClientKey=true`

### I2CP 选项 (I2PTunnel 实现)

**重要**: 这些属性以 `option.i2cp.` 为前缀，但**由 I2PTunnel 实现**，而不是在 I2CP 协议层实现。它们无法通过 I2CP 或 SAM API 使用。

#### tunnel.N.option.i2cp.delayOpen (option.i2cp.delayOpen)

- **类型**: 布尔值
- **适用范围**: 仅限客户端 tunnels
- **默认值**: false
- **描述**: 延迟创建 tunnel，直到首次连接
- **使用场景**: 为很少使用的 tunnels 节省资源
- **示例**: `option.i2cp.delayOpen=false`

#### tunnel.N.option.i2cp.newDestOnResume (option.i2cp.newDestOnResume)

- **类型**: 布尔值
- **上下文**: 仅用于 Client tunnels
- **默认值**: false
- **需要**: `i2cp.closeOnIdle=true`
- **冲突**: 与 `persistentClientKey=true` 互斥
- **描述**: 在空闲超时后创建新的 Destination（目标地址）
- **示例**: `option.i2cp.newDestOnResume=false`

#### tunnel.N.option.i2cp.leaseSetPrivateKey (option.i2cp.leaseSetPrivateKey)

- **类型**: 字符串（base64 编码的密钥）
- **上下文**: 仅适用于服务器 tunnels
- **描述**: 持久的私有 leaseset（I2P 中发布到 netDb 的可达性信息集合）加密密钥
- **使用场景**: 跨重启保持加密的 leaseset 一致性
- **示例**: `option.i2cp.leaseSetPrivateKey=AAAA...base64...`

#### tunnel.N.option.i2cp.leaseSetSigningPrivateKey (option.i2cp.leaseSetSigningPrivateKey)

- **Type**: 字符串 (sigtype:base64)
- **Context**: 仅用于 Server tunnels
- **Format**: `sigtype:base64key`
- **Description**: 持久化 leaseset（I2P 的租约集合）签名私钥
- **Example**: `option.i2cp.leaseSetSigningPrivateKey=7:AAAA...base64...`

### 服务器特定选项

#### tunnel.N.option.enableUniqueLocal (option.enableUniqueLocal)

- **类型**: 布尔值
- **适用范围**: 仅限服务器 tunnels
- **默认值**: false
- **说明**: 针对每个远程 I2P 目标使用唯一的本地 IP
- **使用场景**: 在服务器日志中跟踪客户端 IP
- **安全提示**: 可能降低匿名性
- **示例**: `option.enableUniqueLocal=false`

#### tunnel.N.option.targetForPort.NNNN (option.targetForPort.NNNN)

- **Type**: 字符串 (hostname:port)
- **Context**: 仅适用于 Server tunnels
- **Description**: 为传入端口 NNNN 覆盖 targetHost/targetPort
- **Use Case**: 基于端口将流量路由到不同的本地服务
- **Example**: `option.targetForPort.8080=localhost:8080`

### 线程池配置

#### tunnel.N.option.i2ptunnel.usePool (option.i2ptunnel.usePool)

- **类型**: 布尔值
- **适用范围**: 仅用于 Server tunnels
- **默认值**: true
- **描述**: 使用线程池进行连接处理
- **注意**: 对于标准服务器始终为 false (忽略)
- **示例**: `option.i2ptunnel.usePool=true`

#### tunnel.N.option.i2ptunnel.blockingHandlerCount (option.i2ptunnel.blockingHandlerCount)

- **类型**: 整数
- **上下文**: 仅用于服务器 tunnel
- **默认值**: 65
- **描述**: 最大线程池大小
- **注意**: 对标准服务器无效
- **示例**: `option.i2ptunnel.blockingHandlerCount=100`

### HTTP 客户端选项

#### tunnel.N.option.i2ptunnel.httpclient.allowInternalSSL (option.i2ptunnel.httpclient.allowInternalSSL)

- **类型**: 布尔型
- **上下文**: 仅限 HTTP 客户端
- **默认值**: false
- **说明**: 允许 SSL 连接到 .i2p 地址
- **示例**: `option.i2ptunnel.httpclient.allowInternalSSL=false`

#### tunnel.N.option.i2ptunnel.httpclient.disableAddressHelper (option.i2ptunnel.httpclient.disableAddressHelper)

- **类型**: 布尔值
- **上下文**: 仅限 HTTP 客户端
- **默认值**: false
- **描述**: 在代理响应中禁用地址助手链接
- **示例**: `option.i2ptunnel.httpclient.disableAddressHelper=false`

#### tunnel.N.option.i2ptunnel.httpclient.jumpServers (option.i2ptunnel.httpclient.jumpServers)

- **Type**: 字符串 (以逗号或空格分隔的 URL)
- **Context**: 仅限 HTTP 客户端
- **Description**: 用于主机名解析的 Jump server (I2P 的跳转服务器) URL
- **Example**: `option.i2ptunnel.httpclient.jumpServers=http://jump.i2p/jump,http://stats.i2p/jump`

#### tunnel.N.option.i2ptunnel.httpclient.sendAccept (option.i2ptunnel.httpclient.sendAccept)

- **类型**: 布尔值
- **上下文**: 仅限 HTTP 客户端
- **默认值**: false
- **描述**: 传递 Accept-* 请求头（以 Accept 开头的 HTTP 请求头，除 Accept 和 Accept-Encoding 外）
- **示例**: `option.i2ptunnel.httpclient.sendAccept=false`

#### tunnel.N.option.i2ptunnel.httpclient.sendReferer (option.i2ptunnel.httpclient.sendReferer)

- **类型**: 布尔值
- **上下文**: 仅适用于 HTTP 客户端
- **默认值**: false
- **描述**: 通过代理转发 Referer 请求头
- **隐私提示**: 可能泄露信息
- **示例**: `option.i2ptunnel.httpclient.sendReferer=false`

#### tunnel.N.option.i2ptunnel.httpclient.sendUserAgent (option.i2ptunnel.httpclient.sendUserAgent)

- **类型**: 布尔值
- **适用范围**: 仅限 HTTP 客户端
- **默认值**: false
- **说明**: 通过代理传递 User-Agent 头
- **隐私提示**: 可能泄露浏览器信息
- **示例**: `option.i2ptunnel.httpclient.sendUserAgent=false`

#### tunnel.N.option.i2ptunnel.httpclient.sendVia (option.i2ptunnel.httpclient.sendVia)

- **类型**: 布尔
- **上下文**: 仅适用于 HTTP 客户端
- **默认值**: false
- **说明**: 通过代理传递 Via 头部
- **示例**: `option.i2ptunnel.httpclient.sendVia=false`

#### tunnel.N.option.i2ptunnel.httpclient.SSLOutproxies (option.i2ptunnel.httpclient.SSLOutproxies)

- **类型**: 字符串（以逗号或空格分隔的目标地址）
- **上下文**: 仅限 HTTP 客户端
- **描述**: 用于 HTTPS 的网络内 SSL outproxies（出口代理）
- **示例**: `option.i2ptunnel.httpclient.SSLOutproxies=ssl-outproxy.i2p`

#### tunnel.N.option.i2ptunnel.useLocalOutproxy (option.i2ptunnel.useLocalOutproxy)

- **类型**: 布尔值
- **适用范围**: 仅限 HTTP 客户端
- **默认值**: true
- **描述**: 使用已注册的本地 outproxy（出口代理）插件
- **示例**: `option.i2ptunnel.useLocalOutproxy=true`

### HTTP 客户端身份验证

#### tunnel.N.option.proxyAuth (option.proxyAuth)

- **类型**: 枚举
- **上下文**: 仅限 HTTP 客户端
- **默认**: false
- **取值**: `true`, `false`, `basic`, `digest`
- **说明**: 代理访问需要本地身份验证
- **注意**: `true` 等同于 `basic`
- **示例**: `option.proxyAuth=basic`

#### tunnel.N.option.proxy.auth.USER.md5 (option.proxy.auth.USER.md5)

- **类型**: 字符串（32 个小写十六进制字符）
- **上下文**: 仅限 HTTP 客户端
- **要求**: `proxyAuth=basic` 或 `proxyAuth=digest`
- **说明**: 用户 USER 的密码的 MD5 哈希
- **弃用**: 请改用 SHA-256（0.9.56+）
- **示例**: `option.proxy.auth.alice.md5=5f4dcc3b5aa765d61d8327deb882cf99`

#### tunnel.N.option.proxy.auth.USER.sha256 (option.proxy.auth.USER.sha256)

- **类型**: 字符串（64 个字符的小写十六进制）
- **上下文**: 仅限 HTTP 客户端
- **要求**: `proxyAuth=digest`
- **起始版本**: 0.9.56
- **标准**: RFC 7616
- **描述**: 用户 USER 的密码的 SHA-256 哈希
- **示例**: `option.proxy.auth.alice.sha256=5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8`

### 出口代理认证

#### tunnel.N.option.outproxyAuth (option.outproxyAuth)

- **类型**: 布尔值
- **上下文**: 仅适用于 HTTP 客户端
- **默认值**: false
- **说明**: 向 outproxy（出口代理）发送认证信息
- **示例**: `option.outproxyAuth=false`

#### tunnel.N.option.outproxyUsername (option.outproxyUsername)

- **类型**: 字符串
- **上下文**: 仅限 HTTP 客户端
- **需要**: `outproxyAuth=true`
- **描述**: 用于 outproxy（出口代理）认证的用户名
- **示例**: `option.outproxyUsername=user`

#### tunnel.N.option.outproxyPassword (option.outproxyPassword)

- **类型**: 字符串
- **上下文**: 仅限 HTTP 客户端
- **要求**: `outproxyAuth=true`
- **描述**: 用于 outproxy（出口代理）认证的密码
- **安全性**: 以明文存储
- **示例**: `option.outproxyPassword=secret`

### SOCKS 客户端选项

#### tunnel.N.option.i2ptunnel.socks.proxy.default (option.i2ptunnel.socks.proxy.default)

- **类型**: 字符串（以逗号或空格分隔的目标地址）
- **上下文**: 仅适用于 SOCKS 客户端
- **描述**: I2P 网络内的 outproxy（出站代理），用于未指定端口
- **示例**: `option.i2ptunnel.socks.proxy.default=outproxy.i2p`

#### tunnel.N.option.i2ptunnel.socks.proxy.NNNN (option.i2ptunnel.socks.proxy.NNNN)

- **类型**: 字符串（以逗号或空格分隔的 destinations（I2P 目的地标识））
- **上下文**: 仅限 SOCKS 客户端
- **描述**: 专用于端口 NNNN 的网络内 outproxies（出口代理）
- **示例**: `option.i2ptunnel.socks.proxy.443=ssl-outproxy.i2p`

#### tunnel.N.option.outproxyType (option.outproxyType)

- **Type**: 枚举
- **Context**: 仅限 SOCKS 客户端
- **Default**: socks
- **Since**: 自 0.9.57 版本起
- **Values**: `socks`, `connect` (HTTPS)
- **Description**: 已配置的 outproxy（出口代理）的类型
- **Example**: `option.outproxyType=connect`

### HTTP 服务器选项

#### tunnel.N.option.maxPosts (option.maxPosts)

- **类型**: 整数
- **适用范围**: 仅限 HTTP 服务器
- **默认值**: 0（无限制）
- **说明**: 每个 postCheckTime 内，来自同一 Destination（I2P 目标标识）的最大 POST 请求数
- **示例**: `option.maxPosts=10`

#### tunnel.N.option.maxTotalPosts (option.maxTotalPosts)

- **Type**: 整数
- **Context**: 仅限 HTTP 服务器
- **Default**: 0（无限制）
- **Description**: 每个 postCheckTime 内来自所有 destinations（I2P 目标地址）的 POST 请求最大次数
- **Example**: `option.maxTotalPosts=50`

#### tunnel.N.option.postCheckTime (option.postCheckTime)

- **类型**: 整数（秒）
- **上下文**: 仅限 HTTP 服务器
- **默认值**: 300
- **描述**: 用于检查 POST 限制的时间窗口
- **示例**: `option.postCheckTime=600`

#### tunnel.N.option.postBanTime (option.postBanTime)

- **Type**: 整数（秒）
- **Context**: 仅限 HTTP 服务器
- **Default**: 1800
- **Description**: 当单个 destination（I2P 目标标识）超过 maxPosts 时的封禁时长
- **Example**: `option.postBanTime=3600`

#### tunnel.N.option.postTotalBanTime (option.postTotalBanTime)

- **类型**: 整数（秒）
- **适用范围**: 仅适用于 HTTP 服务器
- **默认值**: 600
- **描述**: 当超过 maxTotalPosts 后的封禁时长
- **示例**: `option.postTotalBanTime=1200`

### HTTP 服务器安全选项

#### tunnel.N.option.rejectInproxy (option.rejectInproxy)

- **类型**: 布尔
- **上下文**: 仅适用于 HTTP 服务器
- **默认值**: false
- **描述**: 拒绝看似经由 inproxy（入口代理；用于从明网访问 I2P 站点的 HTTP 网关）的连接
- **示例**: `option.rejectInproxy=false`

#### tunnel.N.option.rejectReferer (option.rejectReferer)

- **类型**: 布尔值
- **上下文**: 仅限 HTTP 服务器
- **默认值**: false
- **起始版本**: 0.9.25
- **描述**: 拒绝带有 Referer 请求头的连接
- **示例**: `option.rejectReferer=false`

#### tunnel.N.option.rejectUserAgents (option.rejectUserAgents)

- **类型**: 布尔值
- **上下文**: 仅适用于 HTTP 服务器
- **默认值**: false
- **起始版本**: 0.9.25
- **需要**: `userAgentRejectList` 属性
- **描述**: 拒绝与 User-Agent 匹配的连接
- **示例**: `option.rejectUserAgents=false`

#### tunnel.N.option.userAgentRejectList (option.userAgentRejectList)

- **类型**: 字符串（逗号分隔的匹配字符串）
- **适用范围**: 仅限 HTTP 服务器
- **自**: 自版本 0.9.25 起
- **大小写**: 大小写敏感匹配
- **特殊**: "none"（自 0.9.33 起）匹配空的 User-Agent
- **描述**: 要拒绝的 User-Agent 模式列表
- **示例**: `option.userAgentRejectList=Mozilla,Opera,none`

### IRC 服务器选项

#### tunnel.N.option.ircserver.fakeHostname (option.ircserver.fakeHostname)

- **类型**: 字符串（主机名模式）
- **上下文**: 仅限 IRC 服务器
- **默认值**: `%f.b32.i2p`
- **占位符**:
  - `%f` = 完整的 base32 目标地址哈希
  - `%c` = 遮蔽的目标地址哈希（参见 cloakKey）
- **描述**: 发送给 IRC 服务器的主机名格式
- **示例**: `option.ircserver.fakeHostname=%c.irc.i2p`

#### tunnel.N.option.ircserver.cloakKey (option.ircserver.cloakKey)

- **类型**: 字符串（密码短语）
- **适用范围**: 仅适用于 IRC 服务器
- **默认值**: 每个会话随机生成
- **限制**: 不得包含引号或空格
- **描述**: 用于实现一致主机名伪装的密码短语
- **使用场景**: 跨重启/服务器的持久用户跟踪
- **示例**: `option.ircserver.cloakKey=mysecretkey`

#### tunnel.N.option.ircserver.method (option.ircserver.method)

- **类型**: 枚举
- **适用范围**: 仅限 IRC 服务器
- **默认值**: user
- **可选值**: `user`、`webirc`
- **说明**: 用于 IRC 服务器的认证方法
- **示例**: `option.ircserver.method=webirc`

#### tunnel.N.option.ircserver.webircPassword (option.ircserver.webircPassword)

- **类型**: 字符串 (密码)
- **上下文**: 仅限 IRC 服务器
- **要求**: `method=webirc`
- **限制**: 不得包含引号或空格
- **描述**: 用于 WEBIRC 协议认证的密码
- **示例**: `option.ircserver.webircPassword=webircpass`

#### tunnel.N.option.ircserver.webircSpoofIP (option.ircserver.webircSpoofIP)

- **类型**: 字符串（IP 地址）
- **上下文**: 仅限 IRC 服务器
- **要求**: `method=webirc`
- **描述**: 用于 WEBIRC 协议的伪造 IP 地址
- **示例**: `option.ircserver.webircSpoofIP=10.0.0.1`

### SSL/TLS 配置

#### tunnel.N.option.useSSL (option.useSSL)

- **类型**: 布尔值
- **默认值**: false
- **适用范围**: 所有 tunnels
- **行为**:
  - **服务器**: 对与本地服务器的连接使用 SSL
  - **客户端**: 要求本地客户端使用 SSL
- **示例**: `option.useSSL=false`

#### tunnel.N.option.keystoreFile (option.keystoreFile)

- **类型**: 字符串 (文件路径)
- **上下文**: 仅用于 Client tunnels
- **默认值**: `i2ptunnel-(random).ks`
- **路径**: 若非绝对路径，则相对于 `$(I2P_CONFIG_DIR)/keystore/`
- **自动生成**: 如果不存在则创建
- **说明**: 包含 SSL 私钥的密钥库文件
- **示例**: `option.keystoreFile=my-tunnel.ks`

#### tunnel.N.option.keystorePassword (option.keystorePassword)

- **类型**: 字符串（密码）
- **适用范围**: 仅限客户端 tunnels
- **默认值**: changeit
- **自动生成**: 若创建新密钥库则随机生成密码
- **描述**: SSL 密钥库的密码
- **示例**: `option.keystorePassword=secretpassword`

#### tunnel.N.option.keyAlias (option.keyAlias)

- **类型**: 字符串（别名）
- **上下文**: 仅用于 Client tunnels
- **自动生成**: 如果生成了新密钥，则创建
- **描述**: 密钥库中的私钥别名
- **示例**: `option.keyAlias=mytunnel-key`

#### tunnel.N.option.keyPassword (option.keyPassword)

- **类型**: 字符串（密码）
- **上下文**: 仅限客户端 tunnels
- **自动生成**: 创建新密钥时生成随机密码
- **描述**: 密钥库中私钥的密码
- **示例**: `option.keyPassword=keypass123`

### 通用 I2CP 与 Streaming（流式传输）选项

所有 `tunnel.N.option.*` 属性（上文未特别说明的）在传递给 I2CP 接口和 streaming library（流式库）时，会去除 `tunnel.N.option.` 前缀。

**重要**：这些与 I2PTunnel 特定选项是分开的。参见： - [I2CP 规范](/docs/specs/i2cp/) - [Streaming Library 规范（流式传输库）](/docs/specs/streaming/)

示例流式传输选项：

```properties
option.i2cp.messageReliability=BestEffort
option.i2p.streaming.connectDelay=1000
option.i2p.streaming.maxWindowSize=128
```
### 完整的 Tunnel 示例

```properties
# HTTP Proxy (split format without tunnel.N. prefix)
name=I2P HTTP Proxy
description=HTTP proxy for accessing I2P sites and outproxy
type=httpclient
interface=127.0.0.1
listenPort=4444
targetDestination=
sharedClient=true
startOnLoad=true

# I2CP configuration
i2cpHost=127.0.0.1
i2cpPort=7654

# HTTP client options
option.i2ptunnel.httpclient.allowInternalSSL=false
option.i2ptunnel.httpclient.disableAddressHelper=false
option.i2ptunnel.httpclient.jumpServers=http://stats.i2p/cgi-bin/jump.cgi
option.i2ptunnel.httpclient.sendAccept=false
option.i2ptunnel.httpclient.sendReferer=false
option.i2ptunnel.httpclient.sendUserAgent=false

# Proxy authentication
option.proxyAuth=false

# Outproxy configuration
option.i2ptunnel.httpclient.SSLOutproxies=false.i2p
proxyList=false.i2p

# Client behavior
option.persistentClientKey=false
option.i2cp.delayOpen=false

# I2CP tunnel options
option.inbound.length=3
option.outbound.length=3
option.inbound.quantity=2
option.outbound.quantity=2
```
---

## 版本历史与特性时间线

### 版本 0.9.10 (2013)

**Feature**: 配置文件中的空值支持 - 现在支持具有空值的键（`key=`） - 此前会被忽略或导致解析错误

### 版本 0.9.18 (2015)

**功能**: 日志记录器刷新间隔配置 - 属性: `logger.flushInterval` (默认 29 秒) - 在保持可接受的日志延迟的同时降低磁盘 I/O

### 版本 0.9.23（2015年11月）

**重大变更**: 最低要求为 Java 7 - 已结束对 Java 6 的支持 - 为继续获得安全更新所必需

### 版本 0.9.25（2015）

**功能**：HTTP 服务器安全选项 - `tunnel.N.option.rejectReferer` - 拒绝带有 Referer 头的连接 - `tunnel.N.option.rejectUserAgents` - 拒绝特定的 User-Agent 头 - `tunnel.N.option.userAgentRejectList` - 要拒绝的 User-Agent 模式 - **使用场景**：缓解爬虫和不受欢迎客户端的访问

### 版本 0.9.33 (2018年1月)

**功能**: 增强的 User-Agent 过滤 - `userAgentRejectList` 字符串 "none" 可匹配空的 User-Agent - 针对 i2psnark、i2ptunnel、streaming、SusiMail 的更多错误修复

### 版本 0.9.41（2019 年）

**弃用**: 已从 Android 移除 BOB 协议 - Android 用户必须迁移到 SAM 或 I2CP

### 版本 0.9.42（2019年8月）

**重大变更**：配置文件拆分 - 将 `clients.config` 拆分为 `clients.config.d/` 目录结构 - 将 `i2ptunnel.config` 拆分为 `i2ptunnel.config.d/` 目录结构 - 升级后首次运行时自动迁移 - 支持模块化打包和插件管理 - 仍支持传统的单体格式

**其他功能**: - SSU 性能改进 - 跨网络防护 (提案 147) - 初始加密类型支持

### 版本 0.9.56（2021）

**功能**: 安全与日志改进 - `logger.gzip` - 对轮转日志启用 Gzip 压缩（默认值：false） - `logger.minGzipSize` - 压缩的最小大小（默认值：65536 字节） - `tunnel.N.option.proxy.auth.USER.sha256` - SHA-256 摘要认证（RFC 7616） - **安全**: SHA-256 取代 MD5 用于摘要认证

### 版本 0.9.57（2023年1月）

**功能**: SOCKS outproxy（出口代理）类型配置 - `tunnel.N.option.outproxyType` - 选择 outproxy 类型 (socks|connect) - 默认: socks - 为 HTTPS outproxy 提供 HTTPS CONNECT 支持

### 版本 2.6.0 (2024年7月)

**破坏性变更**: I2P-over-Tor 已被阻止 - 来自 Tor 出口节点 IP 地址的连接现已被拒绝 - **原因**: 降低 I2P 性能，浪费 Tor 出口资源 - **影响**: 通过 Tor 出口节点访问 I2P 的用户将被阻止 - 非出口中继和 Tor 客户端不受影响

### 版本 2.10.0 (2025年9月 - 至今)

**主要特性**: - **后量子密码学** 可用（可通过 Hidden Service Manager（隐藏服务管理器）选择启用） - **UDP tracker 支持**，用于 I2PSnark（I2P 内置的 BitTorrent 客户端），以降低 tracker 负载 - **Hidden Mode（隐藏模式）稳定性** 改进，以减少 RouterInfo 耗尽 - 针对拥塞的 router 的网络改进 - 增强的 UPnP/NAT 穿透 - NetDB 改进，包含更积极的 leaseset 移除 - 降低 router 事件的可观测性

**配置**: 未添加新的配置属性

**即将到来的重大变更**：下一个发行版（可能为 2.11.0 或 3.0.0）将需要 Java 17 或更高版本

---

## 弃用与不兼容变更

### 重大弃用

#### I2P-over-Tor 访问 (版本 2.6.0+)

- **状态**: 自 2024 年 7 月起已被封锁
- **影响**: 来自 Tor 出口节点 IP 地址的连接将被拒绝
- **原因**: 在未提供匿名性收益的情况下，会降低 I2P 网络性能
- **影响范围**: 仅限 Tor 出口节点，不包括中继或普通 Tor 客户端
- **替代方案**: 单独使用 I2P 或 Tor，不要组合使用

#### MD5 摘要认证

- **状态**: 已弃用（使用 SHA-256）
- **属性**: `tunnel.N.option.proxy.auth.USER.md5`
- **原因**: MD5 在密码学上已被攻破
- **替代项**: `tunnel.N.option.proxy.auth.USER.sha256`（自 0.9.56 起）
- **时间线**: 仍支持 MD5，但不推荐

### 配置架构变更

#### 单体式配置文件 (版本 0.9.42+)

- **受影响**: `clients.config`, `i2ptunnel.config`
- **状态**: 已弃用，改用拆分目录结构
- **迁移**: 升级到 0.9.42 后首次运行时自动进行
- **兼容性**: 旧格式仍然可用（向后兼容）
- **建议**: 新配置请使用拆分格式

### Java 版本要求

#### Java 6 支持

- **已结束**: 版本 0.9.23（2015年11月）
- **最低要求**: 自 0.9.23 起需要 Java 7

#### Java 17 要求 (即将到来)

- **状态**：重大即将变更
- **目标**：2.10.0 之后的下一次主版本发布（可能是 2.11.0 或 3.0.0）
- **当前最低要求**：Java 8
- **所需操作**：为迁移到 Java 17 做好准备
- **时间表**：将随发行说明公布

### 已移除的功能

#### BOB 协议（Android）

- **已移除**: 版本 0.9.41
- **平台**: 仅限 Android
- **替代方案**: SAM 或 I2CP 协议
- **桌面端**: BOB 在桌面平台仍可用

### 推荐的迁移

1. **认证**：从 MD5 迁移到 SHA-256 摘要认证
2. **配置格式**：迁移到为客户端和 tunnels 拆分的目录结构
3. **Java 运行时**：计划在下一个主要版本发布之前升级到 Java 17
4. **Tor 集成**：不要通过 Tor 的出口节点路由 I2P

---

## 参考资料

### 官方文档

- [I2P 配置规范](/docs/specs/configuration/) - 官方配置文件格式规范
- [I2P 插件规范](/docs/specs/plugin/) - 插件配置与打包
- [I2P 通用结构 - 类型映射](/docs/specs/common-structures/#type-mapping) - 协议数据序列化格式
- [Java Properties 格式](http://docs.oracle.com/javase/1.5.0/docs/api/java/util/Properties.html#load%28java.io.InputStream%29) - 基础格式规范

### 源代码

- [I2P Java Router 仓库](https://github.com/i2p/i2p.i2p) - GitHub 镜像
- [I2P 开发者 Gitea](https://i2pgit.org/I2P_Developers/i2p.i2p) - 官方 I2P 源代码仓库
- [DataHelper.java](https://github.com/i2p/i2p.i2p/blob/master/core/java/src/net/i2p/data/DataHelper.java) - 配置文件 I/O 实现

### 社区资源

- [I2P 论坛](https://i2pforum.net/) - 活跃的社区讨论与支持
- [I2P 网站](/) - 项目官方网站

### API 文档

- [DataHelper JavaDoc](https://i2pplus.github.io/javadoc/net/i2p/data/DataHelper.html) - 关于配置文件方法的 API 文档

### 规范状态

- **规范上次更新**: 2023年1月（版本 0.9.57）
- **当前 I2P 版本**: 2.10.0（2025年9月）
- **技术准确性**: 规范截至 2.10.0 仍然准确（无向后不兼容更改）
- **维护**: 这是一个持续维护的文档，会在配置格式修改时更新
