---
title: "插件包格式"
description: "用于 I2P 插件的 .xpi2p / .su3 打包规则"
slug: "plugin"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## 概述

I2P 插件是扩展 router 功能的签名归档包。它们以 `.xpi2p` 或 `.su3` 文件形式发布，安装到 `~/.i2p/plugins/<name>/`（Windows 上为 `%APPDIR%\I2P\plugins\<name>\`），并以完整的 router 权限运行，且不使用沙箱。

### 支持的插件类型

- 控制台 Web 应用
- 包含 cgi-bin、Web 应用的新 eepsites
- 控制台主题
- 控制台翻译
- Java 程序（进程内或单独的 JVM）
- Shell 脚本和原生二进制文件

### 安全模型

**严重：** 插件在与 I2P router 相同的 JVM 中运行，并拥有与其相同的权限。它们可以不受限制地访问: - 文件系统 (读写) - Router API 和内部状态 - 网络连接 - 执行外部程序

插件应被视为完全受信任的代码。用户在安装前必须验证插件来源和签名。

---

## 文件格式

### SU3 格式（强烈推荐）

**状态：** 已启用，自 I2P 0.9.15 (2014年9月) 起为首选格式

`.su3` 格式提供： - **RSA-4096 签名密钥** (与 xpi2p 中的 DSA-1024 相比) - 签名存储在文件头中 - 魔数：`I2Psu3` - 更好的前向兼容性

**结构：**

```
[SU3 Header with RSA-4096 signature]
[ZIP Archive]
  ├── plugin.config (required)
  ├── console/
  ├── lib/
  ├── webapps/
  └── [other plugin files]
```
### XPI2P 格式（遗留，已弃用）

**状态：** 为向后兼容而提供支持，不建议用于新的插件

`.xpi2p` 格式使用较旧的加密签名： - **DSA-1024 签名**（按 NIST-800-57 已过时） - 在 ZIP 之前前置 40 字节的 DSA 签名 - 需要在 plugin.config 中包含 `key` 字段

**结构：**

```
[40-byte DSA signature]
[16-byte version string (UTF-8, zero-padded)]
[ZIP Archive]
```
**迁移路径：** 当从 xpi2p 迁移到 su3 时，在过渡期间同时提供 `updateURL` 和 `updateURL.su3`。较新的 router（0.9.15+）会自动优先选择 SU3。

---

## 归档布局与 plugin.config

### 必需文件

**plugin.config** - 标准的 I2P 配置文件，包含键值对

### 必需属性

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Property</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Format</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>name</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Installation directory name, must match for updates</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Alphanumeric, no spaces</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>signer</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Developer contact information</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>user@mail.i2p</code> format recommended</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>version</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Plugin version for update comparison</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Max 16 bytes, parsed by VersionComparator</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>key</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA public key (172 B64 chars ending with '=')</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Omit for SU3 format</strong></td></tr>
  </tbody>
</table>
**版本格式示例：** - `1.2.3` - `1.2.3-4` - `2.0.0-beta.1`

有效的分隔符：`.`（点号）、`-`（连字符）、`_`（下划线）

### 可选元数据属性

#### 显示信息

- `date` - 发布日期（Java long 类型时间戳）
- `author` - 开发者名称（建议使用 `user@mail.i2p`）
- `description` - 英文描述
- `description_xx` - 本地化描述（xx = 语言代码）
- `websiteURL` - 插件主页（`http://foo.i2p/`）
- `license` - 许可证标识符（例如，"Apache-2.0"、"GPL-3.0"）

#### 更新配置

- `updateURL` - XPI2P (I2P 插件包格式) 更新位置 (遗留)
- `updateURL.su3` - SU3 (I2P 签名更新包格式) 更新位置 (首选)
- `min-i2p-version` - 所需的最低 I2P 版本
- `max-i2p-version` - 兼容的最高 I2P 版本
- `min-java-version` - 最低 Java 版本 (例如，`1.7`、`17`)
- `min-jetty-version` - 最低 Jetty (Java Web 服务器) 版本 (对于 Jetty 6+ 使用 `6`)
- `max-jetty-version` - 最高 Jetty 版本 (对于 Jetty 5 使用 `5.99999`)

#### 安装行为

- `dont-start-at-install` - 默认值为 `false`。若为 `true`，则需要手动启动
- `router-restart-required` - 默认值为 `false`。通知用户更新后需要重启
- `update-only` - 默认值为 `false`。若插件尚未安装则失败
- `install-only` - 默认值为 `false`。若插件已存在则失败
- `min-installed-version` - 执行更新所需的最低已安装版本
- `max-installed-version` - 可更新的最高已安装版本
- `disableStop` - 默认值为 `false`。若为 `true`，隐藏停止按钮

#### 控制台集成

- `consoleLinkName` - 控制台摘要栏链接的文本
- `consoleLinkName_xx` - 本地化的链接文本（xx = 语言代码）
- `consoleLinkURL` - 链接目标（例如，`/appname/index.jsp`）
- `consoleLinkTooltip` - 工具提示文本（自 0.7.12-6 起支持）
- `consoleLinkTooltip_xx` - 本地化的工具提示
- `console-icon` - 32x32 图标的路径（自 0.9.20 起支持）
- `icon-code` - 用于无 Web 资源插件的 Base64 编码 32x32 PNG（自 0.9.25 起）

#### 平台要求（仅显示）

- `required-platform-OS` - 操作系统要求（不强制执行）
- `other-requirements` - 其他要求（例如，"Python 3.8+"）

#### 依赖管理 (未实现)

- `depends` - 以逗号分隔的插件依赖项
- `depends-version` - 依赖项的版本要求
- `langs` - 语言包内容
- `type` - 插件类型（app/theme/locale/webapp）

### 更新 URL 变量替换

**功能状态：** 自 I2P 1.7.0 (0.9.53) 起可用

`updateURL` 和 `updateURL.su3` 都支持平台特定的变量：

**变量：** - `$OS` - 操作系统: `windows`, `linux`, `mac` - `$ARCH` - 架构: `386`, `amd64`, `arm64`

**示例：**

```properties
updateURL.su3=http://foo.i2p/downloads/foo-$OS-$ARCH.su3
```
**在 Windows AMD64 上的结果：**

```
http://foo.i2p/downloads/foo-windows-amd64.su3
```
这使面向特定平台的构建可以使用单个 plugin.config 文件。

---

## 目录结构

### 标准布局

```
plugins/
└── pluginname/
    ├── plugin.config (required)
    ├── console/
    │   ├── locale/          # Translation JARs
    │   ├── themes/          # Console themes
    │   ├── webapps/         # Web applications
    │   └── webapps.config   # Webapp configuration
    ├── eepsite/
    │   ├── cgi-bin/
    │   ├── docroot/
    │   ├── logs/
    │   ├── webapps/
    │   └── jetty.xml
    ├── lib/
    │   └── *.jar            # Plugin libraries
    └── clients.config       # Client startup configuration
```
### 目录用途

**console/locale/** - 包含 I2P 基础翻译资源包的 JAR 文件 - 插件特定的翻译应位于 `console/webapps/*.war` 或 `lib/*.jar`

**console/themes/** - 每个子目录都包含一个完整的控制台主题 - 自动添加到主题搜索路径中

**console/webapps/** - 用于控制台集成的 `.war` 文件 - 除非在 `webapps.config` 中禁用，否则会自动启动 - WAR 名称无需与插件名称匹配

**eepsite/** - 完整的 eepsite，带有自己的 Jetty 实例 - 需要带有变量替换的 `jetty.xml` 配置 - 参见 zzzot 和 pebble 插件示例

**lib/** - 插件 JAR 库 - 可通过 `clients.config` 或 `webapps.config` 在类路径中指定

---

## Web 应用程序配置

### webapps.config 格式

用于控制 Web 应用行为的标准 I2P 配置文件。

**语法：**

```properties
# Disable autostart
webapps.warname.startOnLoad=false

# Add classpath JARs (as of API 0.9.53, works for any warname)
webapps.warname.classpath=$PLUGIN/lib/foo.jar,$I2P/lib/bar.jar
```
**重要说明：** - 在 router 0.7.12-9 之前，为兼容性请使用 `plugin.warname.startOnLoad` - 在 API 0.9.53 之前，仅当 warname（WAR 名称）与插件名称匹配时，classpath（类路径）才可用 - 自 0.9.53+ 起，classpath 适用于任何 Web 应用名称

### Web 应用最佳实践

1. **ServletContextListener 实现**
   - 实现 `javax.servlet.ServletContextListener` 用于清理
   - 或在 servlet 中重写 `destroy()`
   - 确保在更新期间以及 router 停止时正确关闭

2. **库管理**
   - 将共享的 JAR 放在 `lib/` 中，而非 WAR 包内
   - 通过 `webapps.config` 的类路径进行引用
   - 支持插件单独安装/更新

3. **避免库冲突**
   - 切勿打包 Jetty、Tomcat 或 servlet 的 JAR
   - 切勿打包来自标准 I2P 安装的 JAR
   - 请查看类路径（classpath）部分以获取标准库

4. **编译要求**
   - 不要包含 `.java` 或 `.jsp` 源文件
   - 预编译所有 JSP 页面以避免启动延迟
   - 不能假定 Java/JSP 编译器可用

5. **Servlet API 兼容性**
   - I2P 支持 Servlet 3.0（自 0.9.30 起）
   - **不支持注解扫描**（@WebContent）
   - 必须提供传统的 `web.xml` 部署描述符

6. **Jetty 版本**
   - 当前：Jetty 9 (I2P 0.9.30+)
   - 使用 `net.i2p.jetty.JettyStart` 实现抽象
   - 避免受 Jetty API 变更影响

---

## 客户端配置

### clients.config 格式

定义由插件启动的客户端（服务）。

**基础客户端：**

```properties
clientApp.0.main=com.example.PluginMain
clientApp.0.name=Example Plugin Service
clientApp.0.delay=30
clientApp.0.args=arg1 arg2 $PLUGIN/config.properties
```
**带有停止/卸载的客户端:**

```properties
clientApp.0.stopargs=stop
clientApp.0.uninstallargs=uninstall
clientApp.0.classpath=$PLUGIN/lib/plugin.jar,$I2P/lib/i2p.jar
```
### 属性参考

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Property</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>main</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Fully qualified class name implementing ClientApp interface</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>name</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Display name for user interface</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>delay</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Startup delay in seconds (default: 0)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>args</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Space-separated arguments passed to constructor</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>stopargs</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Arguments for shutdown (must handle gracefully)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>uninstallargs</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Arguments called before plugin deletion</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>classpath</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Comma-separated JAR paths</td></tr>
  </tbody>
</table>
### 变量替换

以下变量会在 `args`、`stopargs`、`uninstallargs` 和 `classpath` 中被替换：

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Variable</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Replacement</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$I2P</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2P base installation directory</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$CONFIG</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2P configuration directory (typically <code>~/.i2p</code>)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$PLUGIN</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">This plugin's directory (<code>$CONFIG/plugins/name</code>)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$OS</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Operating system: <code>windows</code>, <code>linux</code>, <code>mac</code></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$ARCH</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Architecture: <code>386</code>, <code>amd64</code>, <code>arm64</code></td></tr>
  </tbody>
</table>
### 托管与非托管客户端

**受管客户端（自 0.9.4 起推荐）：** - 由 ClientAppManager 实例化 - 保留引用并跟踪状态 - 更易于生命周期管理 - 更好的内存管理

**非托管客户端：** - 由 router 启动， 无状态跟踪 - 必须能优雅地处理多次启动/停止调用 - 使用静态状态信息或 PID 文件进行协调 - 在 router 关闭时会被调用（自 0.7.12-3 起）

### ShellService（自 0.9.53 / 1.7.0 起）

用于运行外部程序并自动跟踪状态的通用解决方案。

**功能：** - 管理进程生命周期 - 与 ClientAppManager 通信 - 自动 PID 管理 - 跨平台支持

**用法：**

```properties
clientApp.0.main=net.i2p.apps.ShellService
clientApp.0.args=$PLUGIN/bin/myservice.sh
```
平台特定脚本：

```properties
clientApp.0.args=$PLUGIN/bin/myservice-$OS.$ARCH
```
**替代方案（遗留）：** 编写一个 Java 包装器以检查操作系统类型，并使用相应的 `.bat` 或 `.sh` 文件调用 `ShellCommand`。

---

## 安装过程

### 用户安装流程

1. 用户将插件 URL 粘贴到 Router 控制台插件配置页面（`/configplugins`）
2. Router 下载插件文件
3. 签名验证（如果密钥未知且启用严格模式则失败）
4. ZIP 完整性检查
5. 解压并解析 `plugin.config`
6. 版本兼容性验证（`min-i2p-version`、`min-java-version` 等）
7. Web 应用名称冲突检测
8. 若为更新则停止现有插件
9. 目录验证（必须位于 `plugins/` 下）
10. 将所有文件解压到插件目录
11. 更新 `plugins.config`
12. 启动插件（除非 `dont-start-at-install=true`）

### 安全与信任

**密钥管理：** - 针对新签名者采用 First-key-seen 信任模型（首次见到的密钥即被信任） - 仅预置 jrandom 和 zzz 的密钥 - 自 0.9.14.1 起，默认拒绝未知密钥 - 可通过高级属性为开发用途覆盖默认设置

**安装限制：** - 归档文件只能解压到插件目录 - 安装程序会拒绝 `plugins/` 之外的路径 - 安装后，插件可以访问其他位置的文件 - 无沙箱或权限隔离

---

## 更新机制

### 更新检查流程

1. router 从 plugin.config 读取 `updateURL.su3`（优先）或 `updateURL`
2. 通过 HTTP HEAD 或部分 GET 请求获取第 41–56 字节
3. 从远程文件提取版本字符串
4. 使用 VersionComparator 与已安装版本比较
5. 如果为更高版本，则根据设置提示用户或自动下载
6. 停止插件
7. 安装更新
8. 启动插件（除非用户偏好已更改）

### 版本比较

将版本解析为以点/连字符/下划线分隔的组件： - `1.2.3` < `1.2.4` - `1.2.3` < `1.2.3-1` - `2.0.0` > `1.9.9`

**最大长度：** 16 字节（必须与 SUD/SU3 头部匹配；SUD/SU3 为 I2P 签名更新文件格式）

### 更新最佳实践

1. 每次发布都递增版本号
2. 从上一版本测试升级路径
3. 重大变更时考虑使用 `router-restart-required`
4. 迁移期间同时提供 `updateURL` 和 `updateURL.su3`
5. 测试时使用构建号后缀（`1.2.3-456`）

---

## 类路径与标准库

### 在类路径中始终可用

以下来自 `$I2P/lib` 的 JAR 包在 I2P 0.9.30+ 中始终在类路径中：

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">JAR</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Plugin Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Core API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Required for all plugins</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>mstreaming.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Streaming API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins need</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>streaming.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Streaming implementation</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins need</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2ptunnel.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">I2PTunnel</td><td style="border:1px solid var(--color-border); padding:0.6rem;">HTTP/server plugins</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>router.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Router internals</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Rarely needed, avoid if possible</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>javax.servlet.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Servlet 3.1, JSP 2.3 API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins with servlets/JSPs</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>jasper-runtime.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Jasper compiler/runtime</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins with JSPs</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>commons-el.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">EL 3.0 API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">JSPs using expression language</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>jetty-i2p.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Jetty utilities</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins starting Jetty</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>org.mortbay.jetty.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Jetty 9 base</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Custom Jetty instances</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>sam.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">SAM API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Rarely needed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>addressbook.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Subscription/blockfile</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Use NamingService instead</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>routerconsole.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Console libraries</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Not public API, avoid</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>jbigi.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Native crypto</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins should not need</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>systray.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">URL launcher</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Rarely needed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>wrapper.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Service wrapper</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins should not need</td></tr>
  </tbody>
</table>
### 特别说明

**commons-logging.jar:** - 自 0.9.30 起为空 - 0.9.30 之前：Apache Tomcat JULI - 0.9.24 之前：Commons Logging + JULI - 0.9 之前：仅 Commons Logging

**jasper-compiler.jar:** - 自 Jetty 6 (0.9) 起为空

**systray4j.jar:** - 已在 0.9.26 版本中移除

### 未在类路径中（必须指定）

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">JAR</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>jstl.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Standard Taglib</td><td style="border:1px solid var(--color-border); padding:0.6rem;">JSP tag libraries</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>standard.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Standard Taglib</td><td style="border:1px solid var(--color-border); padding:0.6rem;">JSP tag libraries</td></tr>
  </tbody>
</table>
### 类路径规范

**在 clients.config 中：**

```properties
clientApp.0.classpath=$PLUGIN/lib/mylib.jar,$I2P/lib/i2p.jar
```
**在 webapps.config 中：**

```properties
webapps.mywebapp.classpath=$PLUGIN/lib/mylib.jar,$I2P/lib/jstl.jar
```
**重要：** 从 0.7.13-3 起，类路径是特定于线程的，而不是 JVM 全局的。请为每个客户端指定完整的类路径。

---

## Java 版本要求

### 当前系统要求（2025年10月）

**I2P 2.10.0 及更早版本：** - 最低要求：Java 7 (自 2016 年 1 月的 0.9.24 起为必需) - 建议：Java 8 或更高版本

**I2P 2.11.0 及更高版本 (即将发布):** - **最低要求: Java 17+** (已在 2.9.0 发行说明中宣布) - 已提前两个版本给出预告 (2.9.0 → 2.10.0 → 2.11.0)

### 插件兼容性策略

**为获得最大兼容性（适用于 I2P 2.10.x 及之前的版本）：**

```xml
<javac source="1.7" target="1.7" />
```
```properties
min-java-version=1.7
```
**针对 Java 8+ 特性：**

```xml
<javac source="1.8" target="1.8" />
```
```properties
min-java-version=1.8
```
**对于 Java 11+ 特性：**

```xml
<javac source="11" target="11" />
```
```properties
min-java-version=11
```
**为 2.11.0+ 做准备：**

```xml
<javac source="17" target="17" />
```
```properties
min-java-version=17
min-i2p-version=2.11.0
```
### 编译最佳实践

**使用较新 JDK 为较旧的目标版本进行编译时：**

```xml
<javac source="1.7" target="1.7" 
       bootclasspath="${java7.home}/jre/lib/rt.jar"
       includeantruntime="false" />
```
这可防止使用在目标 Java 版本中不可用的 API。

---

## Pack200 压缩 - 已废弃

### 重要更新：请勿使用 Pack200（Java 的 JAR 压缩格式）

**状态:** 已弃用并移除

原始规范强烈建议使用 Pack200 压缩，以将大小缩减 60-65%。**这已不再适用。**

**时间线：** - **JEP 336：** Pack200 在 Java 11 中被弃用（2018 年 9 月） - **JEP 367：** Pack200 在 Java 14 中被移除（2020 年 3 月）

**I2P 官方更新规范指出：** > "zip 中的 Jar 和 war 文件不再像上文针对 'su2' 文件所述那样使用 pack200（Java 的打包/压缩格式）进行压缩，因为较新的 Java 运行时已不再支持它。"

**该怎么做：**

1. **立即从构建流程中移除 pack200（已弃用的 JAR 压缩格式）**
2. **使用标准 ZIP 压缩**
3. **考虑替代方案：**
   - ProGuard/R8（用于代码缩减）
   - UPX（用于原生二进制文件的压缩）
   - 现代压缩算法（zstd、brotli），如果提供自定义解压器

**针对现有插件：** - 旧版 router（0.7.11-5 至 Java 10）仍可解包 pack200 - 新版 router（Java 11+）无法解包 pack200 - 重新发布插件，不使用 pack200 压缩

---

## 签名密钥与安全性

### 密钥生成（SU3 格式）

使用 i2p.scripts 仓库中的 `makeplugin.sh` 脚本:

```bash
# Generate new signing key
./makeplugin.sh keygen

# Keys stored in ~/.i2p-plugin-keys/
```
**关键信息：** - 算法: RSA_SHA512_4096 - 格式: X.509 证书 - 存储: Java 密钥库格式

### 插件签名

```bash
# Create signed su3 file
./makeplugin.sh sign myplugin.zip myplugin.su3 keyname

# Verify signature
./makeplugin.sh verify myplugin.su3
```
### 密钥管理最佳实践

1. **一次生成，永久保护**
   - Routers 会拒绝密钥名重复但密钥不同的情况
   - Routers 会拒绝密钥相同但密钥名不同的情况
   - 若密钥/名称不匹配，将拒绝更新

2. **安全存储**
   - 安全地备份密钥库
   - 使用强密码短语
   - 切勿提交到版本控制系统

3. **密钥轮换**
   - 当前架构不支持
   - 规划长期密钥使用
   - 考虑用于团队开发的多重签名方案

### 遗留 DSA 签名（XPI2P）

**状态：** 功能正常但已过时

xpi2p 格式所使用的 DSA-1024 签名： - 40 字节签名 - 172 个 base64 字符的公钥 - NIST-800-57 建议最小为 (L=2048, N=224) - I2P 使用更弱的 (L=1024, N=160)

**建议：** 改用采用 RSA-4096 的 SU3（I2P 更新/插件的签名封装格式）。

---

## 插件开发指南

### 必备最佳实践

1. **文档**
   - 提供包含安装说明的清晰 README（自述文件）
   - 记录配置选项及其默认值
   - 每次发布时包含变更日志
   - 注明所需的 I2P/Java 版本

2. **大小优化**
   - 只包含必要的文件
   - 切勿捆绑 router 的 JAR 包
   - 将安装包与更新包分离（库位于 lib/）
   - ~~使用 Pack200 压缩~~ **已废弃 - 使用标准 ZIP**

3. **配置**
   - 切勿在运行时修改 `plugin.config`
   - 为运行时设置使用单独的配置文件
   - 记录并说明所需的 router 设置（SAM 端口、tunnels 等）
   - 尊重用户的现有配置

4. **资源使用**
   - 避免在默认设置下过度占用带宽
   - 实现合理的 CPU 使用限制
   - 在关闭时清理资源
   - 在适当情况下使用守护线程

5. **测试**
   - 在所有平台上测试安装/升级/卸载
   - 测试从上一版本更新
   - 在更新过程中验证 Web 应用的停止/重启
   - 使用最低支持的 I2P 版本进行测试

6. **文件系统**
   - 切勿写入 `$I2P`（可能是只读）
   - 将运行时数据写入 `$PLUGIN` 或 `$CONFIG`
   - 使用 `I2PAppContext` 进行目录发现
   - 不要假定 `$CWD` 的位置

7. **兼容性**
   - 不要重复实现标准的 I2P 类
   - 必要时扩展类，不要替换
   - 在 plugin.config 中检查 `min-i2p-version`、`min-jetty-version`
   - 如果要支持较旧的 I2P 版本，请进行测试

8. **关闭处理**
   - 在 clients.config 中正确配置 `stopargs`
   - 注册关闭钩子: `I2PAppContext.addShutdownTask()`
   - 优雅地处理多次启动/停止调用
   - 将所有线程设置为守护线程

9. **安全**
   - 验证所有外部输入
   - 切勿调用 `System.exit()`
   - 尊重用户隐私
   - 遵循安全编码实践

10. **许可协议**
    - 明确说明插件许可协议
    - 遵守捆绑库的许可协议
    - 包含必要的署名信息
    - 如有要求，提供源代码获取途径

### 高级注意事项

**时区处理:** - Router 将 JVM 时区设置为 UTC - 用户的实际时区: `I2PAppContext` 属性 `i2p.systemTimeZone`

**目录发现：**

```java
// Plugin directory
String pluginDir = I2PAppContext.getGlobalContext()
    .getAppDir().getAbsolutePath() + "/plugins/" + pluginName;

// Or use $PLUGIN variable in clients.config args
```
**版本编号:** - 使用语义化版本 (major.minor.patch) - 为测试添加构建号 (1.2.3-456) - 确保更新时版本号单调递增

**Router 类访问:** - 一般应避免依赖 `router.jar` - 改用 `i2p.jar` 中的公共 API - 未来的 I2P 可能会限制对 Router 类的访问

**JVM 崩溃预防（历史）：** - 已在 0.7.13-3 修复 - 正确使用类加载器 - 避免在正在运行的插件中更新 JAR 文件 - 如有必要，设计为在更新时重启（restart-on-update）

---

## eepsite 插件

### 概述

插件可以提供完整的 eepsites（I2P 上的匿名网站），并配有其自有的 Jetty 和 I2PTunnel 实例。

### 架构

**请勿尝试：** - 安装到现有的 eepsite（I2P 隐匿站点） - 与 router 的默认 eepsite 合并 - 假定仅有一个 eepsite 可用

**改为：** - 启动新的 I2PTunnel 实例（通过 CLI（命令行界面）方式） - 启动新的 Jetty 实例 - 在 `clients.config` 中配置二者

### 示例结构

```
plugins/myeepsite/
├── plugin.config
├── clients.config          # Starts Jetty + I2PTunnel
├── eepsite/
│   ├── jetty.xml          # Requires variable substitution
│   ├── docroot/
│   ├── webapps/
│   └── logs/
└── lib/
    └── [dependencies]
```
### jetty.xml 中的变量替换

将 `$PLUGIN` 变量用于路径：

```xml
<Set name="resourceBase">$PLUGIN/eepsite/docroot</Set>
```
Router 会在插件启动时执行替换。

### 示例

参考实现: - **zzzot 插件** - BT 追踪器 - **pebble 插件** - 博客平台

两者都可在 zzz 的插件页面（I2P-internal）获取。

---

## 控制台集成

### 摘要栏链接

为 router 控制台摘要栏添加可点击链接：

```properties
consoleLinkName=My Plugin
consoleLinkURL=/myplugin/
consoleLinkTooltip=Open My Plugin Interface
```
本地化版本：

```properties
consoleLinkName_de=Mein Plugin
consoleLinkTooltip_de=Öffne Mein Plugin Schnittstelle
```
### 控制台图标

**镜像文件 (自 0.9.20 起):**

```properties
console-icon=/myicon.png
```
如果已指定，则路径相对于 `consoleLinkURL`（自 0.9.53 起）；否则相对于 Web 应用名称。

**嵌入式图标（自 0.9.25 起）：**

```properties
icon-code=iVBORw0KGgoAAAANSUhEUgAAA...Base64EncodedPNG...
```
使用以下方式生成：

```bash
base64 -w 0 icon-32x32.png
```
或者使用 Java：

```bash
java -cp i2p.jar net.i2p.data.Base64 encode icon.png
```
要求：- 32x32 像素 - PNG 格式 - Base64 编码（无换行）

---

## 国际化

### 翻译包

**针对 I2P 基础翻译：** - 将 JAR 包放置于 `console/locale/` - 包含现有 I2P 应用的资源包 - 命名：`messages_xx.properties` (xx = 语言代码)

**针对插件特定的翻译：** - 将其包含在 `console/webapps/*.war` - 或包含在 `lib/*.jar` - 使用标准的 Java ResourceBundle 方法

### plugin.config 中的本地化字符串

```properties
description=My awesome plugin
description_de=Mein tolles Plugin
description_fr=Mon plugin génial
description_es=Mi plugin increíble
```
支持的字段：- `description_xx` - `consoleLinkName_xx` - `consoleLinkTooltip_xx`

### 控制台主题翻译

位于 `console/themes/` 的主题会自动添加到主题搜索路径中。

---

## 特定于平台的插件

### 分离式软件包方案

为每个平台使用不同的插件名称：

```properties
# Windows package
name=myplugin-windows

# Linux package  
name=myplugin-linux

# macOS package
name=myplugin-mac
```
### 变量替换方法

单个 plugin.config，包含平台变量：

```properties
name=myplugin
updateURL.su3=http://myplugin.i2p/downloads/myplugin-$OS-$ARCH.su3
```
在 clients.config 中：

```properties
clientApp.0.main=net.i2p.apps.ShellService
clientApp.0.args=$PLUGIN/bin/myapp-$OS-$ARCH
```
### 运行时操作系统检测

Java 中的条件执行思路：

```java
String os = System.getProperty("os.name").toLowerCase();
if (os.contains("win")) {
    // Windows-specific code
} else if (os.contains("nix") || os.contains("nux")) {
    // Linux-specific code
} else if (os.contains("mac")) {
    // macOS-specific code
}
```
---

## 故障排除

### 常见问题

**插件无法启动：** 1. 检查 I2P 版本兼容性（`min-i2p-version`） 2. 验证 Java 版本（`min-java-version`） 3. 检查 router 日志是否有错误 4. 确认类路径中包含所有必需的 JAR 文件

**Web 应用无法访问：** 1. 确认 `webapps.config` 未将其禁用 2. 检查 Jetty（Java Web 服务器）版本兼容性（`min-jetty-version`） 3. 确认存在 `web.xml`（不支持注解扫描） 4. 检查是否存在冲突的 Web 应用名称

**更新失败：** 1. 确认版本号已提升 2. 检查签名与签名密钥是否匹配 3. 确保插件名称与已安装的版本匹配 4. 检查 `update-only`/`install-only` 设置

**外部程序无法停止：** 1. 使用 ShellService（Shell 服务组件）进行自动化生命周期管理 2. 正确实现对 `stopargs` 的处理 3. 检查 PID 文件清理 4. 验证进程是否已终止

### 调试日志

启用 router 的调试日志：

```
logger.record.net.i2p.router.web.ConfigPluginsHandler=DEBUG
```
检查日志：

```
~/.i2p/logs/log-router-0.txt
```
---

## 参考信息

### 官方规范

- [插件规范](/docs/specs/plugin/)
- [配置格式](/docs/specs/configuration/)
- [更新规范](/docs/specs/updates/)
- [密码学](/docs/specs/cryptography/)

### I2P 版本历史

**当前版本:** - **I2P 2.10.0** (2025年9月8日)

**自 0.9.53 以来的主要版本：** - 2.10.0 (2025 年 9 月) - Java 17+ 公告 - 2.9.0 (2025 年 6 月) - Java 17+ 警告 - 2.8.0 (2024 年 10 月) - 后量子密码学测试 - 2.6.0 (2024 年 5 月) - 对 I2P-over-Tor 的阻断 - 2.4.0 (2023 年 12 月) - NetDB 安全性改进 - 2.2.0 (2023 年 3 月) - 拥塞控制 - 2.1.0 (2023 年 1 月) - 网络改进 - 2.0.0 (2022 年 11 月) - SSU2 传输协议 - 1.7.0/0.9.53 (2022 年 2 月) - ShellService, 变量替换 - 0.9.15 (2014 年 9 月) - 引入 SU3 格式

**版本编号:** - 0.9.x 系列: 截至 0.9.53 版本 - 2.x 系列: 自 2.0.0 起 (引入 SSU2)

### 开发者资源

**源代码:** - 主仓库: https://i2pgit.org/I2P_Developers/i2p.i2p - GitHub 镜像: https://github.com/i2p/i2p.i2p

**插件示例:** - zzzot (BitTorrent 追踪器) - pebble (博客平台) - i2p-bote (无服务器电子邮件) - orchid (Tor 客户端) - seedless (对等交换)

**构建工具：** - makeplugin.sh - 密钥生成与签名 - 位于 i2p.scripts 仓库中 - 自动化 su3（签名更新文件格式）的创建与验证

### 社区支持

**论坛:** - [I2P 论坛](https://i2pforum.net/) - [zzz.i2p](http://zzz.i2p/) (I2P 内部)

**IRC/聊天:** - #i2p-dev 在 OFTC 上 - I2P 网络内的 IRC

---

## 附录 A：完整的 plugin.config 示例

```properties
# Required fields
name=example-plugin
signer=developer@mail.i2p
version=1.2.3

# Update configuration
updateURL.su3=http://example.i2p/plugins/example-$OS-$ARCH.su3
min-i2p-version=2.0.0
min-java-version=17

# Display information
date=1698796800000
author=Example Developer <developer@mail.i2p>
websiteURL=http://example.i2p/
license=Apache-2.0

description=An example I2P plugin demonstrating best practices
description_de=Ein Beispiel-I2P-Plugin zur Demonstration bewährter Praktiken
description_es=Un plugin I2P de ejemplo que demuestra las mejores prácticas

# Console integration
consoleLinkName=Example Plugin
consoleLinkName_de=Beispiel-Plugin
consoleLinkURL=/example/
consoleLinkTooltip=Open the Example Plugin control panel
consoleLinkTooltip_de=Öffne das Beispiel-Plugin-Kontrollfeld
console-icon=/icon.png

# Installation behavior
dont-start-at-install=false
router-restart-required=false

# Platform requirements (informational)
required-platform-OS=All platforms supported
other-requirements=Requires 512MB free disk space
```
---

## 附录B：完整的 clients.config 示例

```properties
# Main service client (managed)
clientApp.0.main=com.example.plugin.MainService
clientApp.0.name=Example Plugin Main Service
clientApp.0.delay=30
clientApp.0.args=$PLUGIN/config.properties --port=7656
clientApp.0.stopargs=shutdown
clientApp.0.uninstallargs=cleanup
clientApp.0.classpath=$PLUGIN/lib/example.jar,$I2P/lib/i2p.jar,$I2P/lib/mstreaming.jar

# External program via ShellService
clientApp.1.main=net.i2p.apps.ShellService
clientApp.1.name=Example Native Helper
clientApp.1.delay=35
clientApp.1.args=$PLUGIN/bin/helper-$OS-$ARCH --config $PLUGIN/helper.conf
clientApp.1.classpath=$I2P/lib/i2p.jar

# Jetty eepsite
clientApp.2.main=net.i2p.jetty.JettyStart
clientApp.2.name=Example Eepsite
clientApp.2.delay=40
clientApp.2.args=$PLUGIN/eepsite/jetty.xml
clientApp.2.stopargs=$PLUGIN/eepsite/jetty.xml stop
clientApp.2.classpath=$PLUGIN/lib/example-web.jar,$I2P/lib/i2p.jar

# I2PTunnel for eepsite
clientApp.3.main=net.i2p.i2ptunnel.TunnelControllerGroup
clientApp.3.name=Example Eepsite Tunnel
clientApp.3.delay=45
clientApp.3.args=$PLUGIN/eepsite/i2ptunnel.config
```
---

## 附录 C：完整的 webapps.config 示例

```properties
# Disable autostart for admin webapp
webapps.example-admin.startOnLoad=false

# Main webapp with classpath
webapps.example.startOnLoad=true
webapps.example.classpath=$PLUGIN/lib/example-core.jar,$PLUGIN/lib/commons-utils.jar,$I2P/lib/jstl.jar,$I2P/lib/standard.jar

# Legacy support (pre-0.7.12-9)
plugin.example.startOnLoad=true
```
---

## 附录 D: 迁移清单 (0.9.53 到 2.10.0)

### 必要的更改

- [ ] **从构建流程中移除 Pack200 压缩**
  - 从 Ant/Maven/Gradle 脚本中移除 pack200 任务
  - 在不使用 pack200 的情况下重新发布现有插件

- [ ] **审查 Java 版本要求**
  - 考虑对新功能要求 Java 11+
  - 计划在 I2P 2.11.0 中要求 Java 17+
  - 在 plugin.config 中更新 `min-java-version`

- [ ] **更新文档**
  - 移除对 Pack200 的引用
  - 更新 Java 版本要求
  - 更新 I2P 版本引用（0.9.x → 2.x）

### 建议的更改

- [ ] **加强密码学签名**
  - 如果尚未完成，请从 XPI2P（I2P 插件打包/签名格式）迁移到 SU3（I2P 插件打包/签名格式）
  - 为新插件使用 RSA-4096 密钥

- [ ] **利用新功能 (如果使用 0.9.53+)**
  - 使用 `$OS` / `$ARCH` 变量用于特定平台的更新
  - 使用 ShellService 运行外部程序
  - 使用改进的 webapp 类路径 (适用于任何 WAR 名称)

- [ ] **测试兼容性**
  - 在 I2P 2.10.0 上进行测试
  - 使用 Java 8、11、17 进行验证
  - 在 Windows、Linux、macOS 上检查

### 可选增强功能

- [ ] 实现正确的 ServletContextListener（Servlet 上下文监听器）
- [ ] 添加本地化说明
- [ ] 提供控制台图标
- [ ] 改进关闭处理
- [ ] 添加全面的日志记录
- [ ] 编写自动化测试
