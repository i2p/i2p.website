---
title: "插件规范"
description: "I2P插件的.xpi2p / .su3打包规则"
slug: "plugin"
aliases:
  - "/zh/plugin_spec"
  - "/zh/plugin_spec/"
lastUpdated: "2022-01"
accurateFor: "0.9.53"
type: docs
---

## 概述

本文档规定了一种 .xpi2p 文件格式（类似于 Firefox 的 .xpi 格式），但使用简单的 plugin.config 描述文件而不是 XML install.rdf 文件。此文件格式用于插件的初始安装和插件更新。

此外，本文档还简要概述了 router 如何安装插件，以及为插件开发者提供的策略和指导原则。

基本的 .xpi2p 文件格式与 i2pupdate.sud 文件（用于 router 更新的格式）相同，但安装程序会允许用户安装插件，即使它尚未知道签名者的密钥。

自发布版本 0.9.15 起，支持 SU3 文件格式并且优先使用。此格式支持更强的签名密钥。

> **注意：** 我们不再推荐以 xpi2p 格式分发插件。请使用 su3 格式。

标准目录结构允许用户安装以下类型的插件：

- 控制台网页应用
- 带有 cgi-bin、webapps 的新 eepsite
- 控制台主题
- 控制台翻译
- Java 程序
- 运行在独立 JVM 中的 Java 程序
- 任何 shell 脚本或程序

插件将其所有文件安装在 `~/.i2p/plugins/name/`（Windows 上为 `%APPDIR%\I2P\plugins\name\`）。安装程序会阻止安装到其他位置，不过插件在运行时可以访问其他位置的库文件。

这应该只被视为让安装、卸载和升级更容易的方式，并减少插件间的基本冲突。

然而，插件一旦运行，基本上就没有安全模型了。插件在与router相同的JVM中运行，具有相同的权限，可以完全访问文件系统、router、执行外部程序等。

## 详情

foo.xpi2p 是一个包含以下内容的已签名更新（sud）文件：

标准的 .sud 头部信息附加在 zip 文件前面，包含以下内容：

```text
40-byte DSA signature
16-byte plugin version in UTF-8, padded with trailing zeroes if necessary
```
包含以下内容的 Zip 文件：

### plugin.config 文件

此文件是必需的。它是一个标准的 I2P 配置文件，包含以下属性：

#### 必需属性

以下四个是必需的属性。前三个必须与已安装插件中的属性完全相同才能进行更新插件。

-   **name** - 将安装在此目录名称中。对于原生插件，您可能希望在不同的包中使用单独的名称 - 例如 foo-windows 和 foo-linux。
-   **key** - DSA 公钥，172个 B64 字符，以 '=' 结尾。SU3 格式则省略。
-   **signer** - 推荐使用 yourname@mail.i2p
-   **version** - 必须是 VersionComparator 可以解析的格式，例如 1.2.3-4。最多16字节（必须与sud版本匹配）。有效的数字分隔符是 '.'、'-' 和 '_'。对于更新插件，此版本必须大于已安装插件的版本。

#### 显示属性

如果存在以下属性的值，它们会在 router 控制台的 /configplugins 页面中显示：

-   **date** - Java 时间 - 长整型
-   **author** - 推荐使用 `yourname@mail.i2p`
-   **websiteURL** - `http://foo.i2p/`
-   **updateURL** - `http://foo.i2p/foo.xpi2p` - 更新检查器将检查此 URL 的第 41-56 字节以确定是否有新版本可用。自 1.7.0 (0.9.53) 起，可以在 URL 中使用 `$OS` 和 `$ARCH` 变量。不推荐使用。除非您之前以 xpi2p 格式分发过插件，否则请勿使用。
-   **updateURL.su3** - `http://foo.i2p/foo.su3` - su3 格式更新文件的位置，自 0.9.15 起。自 1.7.0 (0.9.53) 起，可以在 URL 中使用 `$OS` 和 `$ARCH` 变量。
-   **description** - 英语描述
-   **description_xx** - 用于语言 xx 的描述
-   **license** - 插件许可证
-   **disableStop=true** - 默认为 false。如果为 true，将不显示停止按钮。当没有 webapps 且没有带有 stopargs 的客户端时使用此选项。

#### 控制台摘要栏链接属性

以下属性用于在控制台摘要栏中添加链接：

-   **consoleLinkName** - 将添加到摘要栏
-   **consoleLinkName_xx** - 用于语言 xx
-   **consoleLinkURL** - /appname/index.jsp
-   **consoleLinkTooltip** - 从 0.7.12-6 版本开始支持
-   **consoleLinkTooltip_xx** - 从 0.7.12-6 版本开始支持语言 xx

#### 控制台图标属性

以下可选属性可用于在控制台上添加自定义图标：

-   **console-icon** - 从 0.9.20 开始支持。仅适用于 webapps。指向 32x32 图像的路径，例如 /icon.png。从 1.7.0（API 0.9.53）开始，如果指定了 consoleLinkURL，则路径相对于该 URL。否则相对于 webapp 名称。适用于插件中的所有 webapps。
-   **icon-code** - 从 0.9.25 开始支持。为没有 web 资源的插件提供控制台图标。通过在 32x32 png 图像文件上调用 `net.i2p.data.Base64 encode FILE` 产生的 B64 字符串。

#### 安装程序属性

插件安装程序使用以下属性：

-   **type** - app/theme/locale/webapp/... (未实现，可能不必要)
-   **min-i2p-version** - 此插件需要的最低 I2P 版本
-   **max-i2p-version** - 此插件可运行的最高 I2P 版本
-   **min-java-version** - 此插件需要的最低 Java 版本
-   **min-jetty-version** - 从 0.8.13 版本开始支持，对于 Jetty 6 webapps 使用 6
-   **max-jetty-version** - 从 0.8.13 版本开始支持，对于 Jetty 5 webapps 使用 5.99999
-   **required-platform-OS** - 未实现 - 可能只是显示，不进行验证
-   **other-requirements** - 未实现，例如 python x.y - 安装程序不进行验证，仅向用户显示
-   **dont-start-at-install=true** - 默认为 false。安装或更新时不会启动插件。
-   **router-restart-required=true** - 默认为 false。在更新时不会重启 router 或插件，只是通知用户需要重启。
-   **update-only=true** - 默认为 false。如果为 true，当安装不存在时会失败。
-   **install-only=true** - 默认为 false。如果为 true，当安装存在时会失败。
-   **min-installed-version** - 如果存在安装，用于覆盖更新的最低版本
-   **max-installed-version** - 如果存在安装，用于覆盖更新的最高版本
-   **depends=plugin1,plugin2,plugin3** - 未实现
-   **depends-version=0.3.4,,5.6.7** - 未实现

#### 翻译属性

-   **langs=xx,yy,Klingon,...** - (未实现) (yy 是国家标志)

### 应用程序目录和文件

以下目录或文件都是可选的，但必须有一些内容存在，否则它不会执行任何操作：

**console/**

-   **locale/** - 仅包含为基础 I2P 安装中应用程序提供的新资源包（翻译）的 jar 文件。此插件的资源包应放在 console/webapp/foo.war 或 lib/foo.jar 内部
-   **themes/** - router console 的新主题。将每个主题放在子目录中。
-   **webapps/** - （请参阅下面关于 webapps 的重要说明）.wars - 这些将在安装时运行，除非在 webapps.config 中被禁用。war 名称不必与插件名称相同。不要与基础 I2P 安装中的 war 名称重复。
-   **webapps.config** - 与 router 的 webapps.config 格式相同。还用于为 webapp classpath 指定 $PLUGIN/lib/ 或 $I2P/lib 中的额外 jar 文件，使用 `webapps.warname.classpath=$PLUGIN/lib/foo.jar,$I2P/lib/bar.jar`

> **注意：** 在 1.7.0 版本（API 0.9.53）之前，只有当 warname 与插件名称相同时才会加载 classpath 行。从 API 0.9.53 开始，classpath 设置适用于任何 warname。

> **注意：** 在 router 版本 0.7.12-9 之前，router 寻找的是 `plugin.warname.startOnLoad` 而不是 `webapps.warname.startOnLoad`。为了与旧版本 router 兼容，希望禁用 war 的插件应该包含这两行。

**eepsite/**

（请参阅下方关于 eepsite 的重要说明）

-   **cgi-bin/**
-   **docroot/**
-   **logs/**
-   **webapps/**
-   **jetty.xml** - 安装程序需要在此文件中进行变量替换以设置路径。此文件的位置和名称并不重要，只要在 clients.config 中设置即可 - 将其放在上一级目录可能更方便。

**lib/**

将任何 jar 文件放在这里，并在 console/webapps.config 和/或 clients.config 的 classpath 行中指定它们

### clients.config 文件

此文件是可选的，用于指定插件启动时要运行的客户端。它使用与路由器的 clients.config 文件相同的格式。有关格式以及客户端如何启动和停止的重要细节的更多信息，请参阅 clients.config 配置文件规范。

-   **clientApp.0.stopargs=foo bar stop baz** - 如果存在，将使用这些参数调用该类来停止客户端。所有停止任务都以零延迟调用。注意：router 无法判断您的非托管客户端是否正在运行。
-   **clientApp.0.uninstallargs=foo bar uninstall baz** - 如果存在，将在删除 $PLUGIN 之前使用这些参数调用该类。所有卸载任务都以零延迟调用。
-   **clientApp.0.classpath=$I2P/lib/foo.bar,$PLUGIN/lib/bar.jar** - 插件运行器将在 args 和 stopargs 行中进行变量替换，如下所示：
    -   `$I2P` - I2P 基础安装目录
    -   `$CONFIG` - I2P 配置目录（通常为 ~/.i2p）
    -   `$PLUGIN` - 此插件的安装目录（通常为 ~/.i2p/plugins/appname）
    -   `$OS` - 主机操作系统，格式为 `windows`、`linux`、`mac`
    -   `$ARCH` - 主机架构，格式为 `386`、`amd64`、`arm64`

（请参阅下面关于运行shell脚本或外部程序的重要说明）

## 插件安装器任务

这列出了当插件被 I2P 安装时会发生什么。

1.  下载 .xpi2p 文件。
2.  根据存储的密钥验证 .sud 签名。从 0.9.14.1 版本开始，如果没有匹配的密钥，安装将失败，除非设置了高级 router 属性以允许所有密钥。
3.  验证 zip 文件的完整性。
4.  提取 plugin.config 文件。
5.  验证 I2P 版本，以确保插件能够正常工作。
6.  检查 webapps 是否与现有的 $I2P 应用程序重复。
7.  停止现有的插件（如果存在）。
8.  如果 update=false，验证安装目录尚不存在，或询问是否覆盖。
9.  如果 update=true，验证安装目录确实存在，或询问是否创建。
10. 将插件解压到 appDir/plugins/name/ 目录。
11. 将插件添加到 plugins.config 文件中。

## 插件启动任务

这列出了插件启动时发生的情况。首先，检查 plugins.config 文件以查看需要启动哪些插件。对于每个插件：

1.  检查 clients.config，加载并启动每个项目（将配置的 jar 文件添加到 classpath）。
2.  检查 console/webapp 和 console/webapp.config。加载并启动所需的项目（将配置的 jar 文件添加到 classpath）。
3.  如果存在，将 console/locale/foo.jar 添加到翻译 classpath。
4.  如果存在，将 console/theme 添加到主题搜索路径。
5.  添加摘要栏链接。

## 控制台 Web 应用程序说明

带有后台任务的控制台 webapp 应该实现 ServletContextListener（参见 seedless 或 i2pbote 示例），或者在 servlet 中重写 destroy() 方法，以便能够被停止。从 router 版本 0.7.12-3 开始，控制台 webapp 在重启前总是会被停止，所以只要你这样做，就不需要担心多个实例的问题。同样从 router 版本 0.7.12-3 开始，控制台 webapp 会在 router 关闭时被停止。

不要在 webapp 中打包库 jar 文件；将它们放在 lib/ 目录中，并在 webapps.config 中设置 classpath。这样你就可以制作单独的安装和更新插件，其中更新插件不包含库 jar 文件。

永远不要在你的插件中捆绑 Jetty、Tomcat 或 servlet jar 文件，因为它们可能与 I2P 安装中的版本冲突。注意不要捆绑任何冲突的库。

不要包含 .java 或 .jsp 文件；否则 Jetty 会在安装时重新编译它们，这会增加启动时间。虽然大多数 I2P 安装在 classpath 中都有可用的 Java 和 JSP 编译器，但这并不能保证，可能在某些情况下无法正常工作。

目前，需要在 $PLUGIN 中添加 classpath 文件的 webapp 必须与插件同名。例如，插件 foo 中的 webapp 必须命名为 foo.war。

虽然I2P自0.9.30版本起就支持Servlet 3.0，但它不支持@WebContent的注解扫描（没有web.xml文件）。这需要几个额外的运行时jar包，而我们在标准安装中不提供这些包。如果您需要@WebContent支持，请联系I2P开发者。

## Eepsite 说明

目前还不清楚如何将插件安装到现有的 eepsite 中。router 与 eepsite 之间没有钩子连接，eepsite 可能正在运行也可能没有运行，而且可能存在多个 eepsite。更好的做法是启动自己的 Jetty 实例和 I2PTunnel 实例，创建一个全新的 eepsite。

它可以实例化一个新的I2PTunnel（有点像i2ptunnel CLI所做的），但当然不会出现在i2ptunnel图形界面中，那是一个不同的实例。但这没关系。然后你可以一起启动和停止i2ptunnel和jetty。

所以不要指望 router 会自动将其与现有的 eepsite 合并。这很可能不会发生。从 clients.config 启动新的 I2PTunnel 和 Jetty。最好的例子是 zzzot 和 pebble 插件。

如何在jetty.xml中进行路径替换？请参考zzzot和pebble插件的示例。

## 客户端启动/停止说明

从 0.9.4 版本开始，router 支持"托管"插件客户端。托管插件客户端由 `ClientAppManager` 实例化和启动。ClientAppManager 维护对客户端的引用并接收客户端状态的更新。托管插件客户端是首选的，因为它更容易实现状态跟踪以及启动和停止客户端。它还更容易避免客户端代码中的静态引用，这些引用可能导致客户端停止后的过度内存使用。有关编写托管客户端的更多信息，请参阅 clients.config 配置文件规范。

对于"非托管"插件客户端，router无法监控通过clients.config启动的客户端状态。插件作者应该尽可能优雅地处理多次启动或停止调用，可以通过保持静态状态表或使用PID文件等方式。避免在多次启动或停止时记录日志或抛出异常。这同样适用于在没有先前启动的情况下进行停止调用。从router版本0.7.12-3开始，插件将在router关闭时被停止，这意味着clients.config中所有带有stopargs的客户端都会被调用，无论它们之前是否已启动。

## Shell脚本和外部程序说明

要运行shell脚本或其他外部程序，请编写一个小型Java类来检查操作系统类型，然后在您提供的.bat或.sh文件上运行ShellCommand。I2P 1.7.0/0.9.53版本中添加了一个通用解决方案"ShellService"，它为单个命令执行状态跟踪并与ClientAppManager通信。

当 router 停止时，外部程序不会停止，而当 router 启动时会启动第二个副本。这通常可以通过使用 ShellService 来执行状态跟踪来缓解。如果这不适合您的用例，您可以编写一个包装类或 shell 脚本来执行常规的 PID 存储到 PID 文件中，并在启动时检查它。

## 其他插件指南

-   查看 i2p.scripts monotone 分支或 zzz 页面上的任何示例插件以获取 makeplugin.sh shell 脚本。这会自动化大部分密钥生成、插件 su3 文件创建和验证的任务。您应该将此脚本纳入您的插件构建过程。
-   强烈建议对插件的 jar 和 war 文件使用 Pack200，通常可以将插件大小缩小 60-65%。请参考 zzz 页面上的任何示例插件。Pack200 解包在 router 0.7.11-5 或更高版本上受支持，基本上所有支持插件的 router 都支持此功能。
-   插件不得尝试在 $I2P 中的任何地方写入文件，因为它可能是只读的，而且这也不是好的策略。
-   插件可以写入 $CONFIG，但建议仅将文件保存在 $PLUGIN 中。$PLUGIN 中的所有文件在卸载时都会被删除。
-   $CWD 可能在任何位置；不要假设它在特定位置，不要尝试相对于 $CWD 读取或写入文件。对于 ShellService，它始终与 $PLUGIN 相同。
-   Java 程序应该使用 I2PAppContext 中的目录获取器来查找自己的位置。
-   插件目录是 `I2PAppContext.getGlobalContext().getAppDir().getAbsolutePath() + "/plugins/" + appname`，或者在 clients.config 的 args 行中放置 $PLUGIN 参数。
-   所有配置文件必须使用 UTF-8 编码。
-   要在单独的 JVM 中运行，请使用 ShellCommand 配合 `java -cp foo:bar:baz my.main.class arg1 arg2 arg3`。
-   作为 clients.config 中 stopargs 的替代方案，Java 客户端可以使用 `I2PAppContext.addShutdownTask()` 注册关闭钩子。但这不会在升级时关闭插件，因此建议使用 stopargs。另外，将所有创建的线程设置为守护模式。
-   不要包含与标准安装中重复的类。必要时扩展这些类。
-   注意新旧安装之间 wrapper.config 中不同的 classpath 定义。
-   客户端会拒绝使用不同密钥名的重复密钥、使用不同密钥的重复密钥名，以及升级包中的不同密钥或密钥名。请保护好您的密钥。只生成一次。
-   不要在运行时修改 plugin.config 文件，因为它会在升级时被覆盖。在目录中使用不同的配置文件来存储运行时配置。
-   通常，插件不应该需要访问 $I2P/lib/router.jar。不要访问 router 类，除非您在做特殊操作。
-   由于每个版本都必须比之前的版本更高，您可以增强构建脚本，在版本末尾添加构建号。
-   插件绝不能调用 `System.exit()`。
-   请通过满足您捆绑的任何软件的许可证要求来尊重许可证。
-   router 将 JVM 时区设置为 UTC。如果插件需要知道用户的实际时区，它由 router 存储在 I2PAppContext 属性 `i2p.systemTimeZone` 中。

## 类路径

以下位于 $I2P/lib 中的 jar 文件可以假定在所有 I2P 安装的标准类路径中，无论原始安装版本多旧或多新。

i2p jar包中所有最新的公共API都在Javadocs中指定了since-release版本号。如果你的插件需要某些只在最新版本中可用的功能，请确保在plugin.config文件中设置min-i2p-version、min-jetty-version或两者的属性。

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Jar</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contains</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">addressbook.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Subscription and blockfile support</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need; use the NamingService interface</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">commons-logging.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Apache Logging</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Empty since release 0.9.30</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">commons-el.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">JSP Expressions Language</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For plugins with JSPs that use EL. As of release 0.9.30 (Jetty 9), this contains the EL 3.0 API.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Core API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">All plugins will need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2ptunnel.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2PTunnel</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For plugins with HTTP or other servers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jasper-compiler.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">nothing</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Empty since Jetty 6 (release 0.9)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jasper-runtime.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Jasper Compiler and Runtime, and some Tomcat utils</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Needed for plugins with JSPs</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">javax.servlet.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Servlet API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Needed for plugins with JSPs. As of release 0.9.30 (Jetty 9), this contains the Servlet 3.1 and JSP 2.3 APIs.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jbigi.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Binaries</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jetty-i2p.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Support utilities</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Some plugins will need. As of release 0.9.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">mstreaming.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Streaming API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins will need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">org.mortbay.jetty.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Jetty Base</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Only plugins starting their own Jetty instance will need. Recommended way of starting Jetty is with <code>net.i2p.jetty.JettyStart</code> in jetty-i2p.jar.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">router.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Router</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Only plugins using router context will need; most will not</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">routerconsole.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Console libraries</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need, not a public API</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">sam.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SAM API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">streaming.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Streaming Implementation</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins will need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">systray.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">URL Launcher</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins should not need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">systray4j.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Systray</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need. As of 0.9.26, no longer present.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">wrapper.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Router</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need</td>
    </tr>
  </tbody>
</table>
可以假设以下在 $I2P/lib 中的 jar 文件在所有 I2P 安装中都存在，无论原始安装多么旧或多么新，但不一定在类路径中：

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Jar</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contains</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jstl.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Standard Taglib</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For plugins using JSP tags</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">standard.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Standard Taglib</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For plugins using JSP tags</td>
    </tr>
  </tbody>
</table>
上面未列出的任何内容可能不存在于每个人的classpath中，即使您在自己的i2p版本的classpath中有它。如果您需要上面未列出的任何jar文件，请将$I2P/lib/foo.jar添加到您插件中clients.config或webapps.config指定的classpath中。

以前，在 clients.config 中指定的 classpath 条目会被添加到整个 JVM 的 classpath 中。然而，从 0.7.13-3 版本开始，这个问题通过使用类加载器得到了修复，现在按照最初的设计，在 clients.config 中指定的 classpath 仅适用于特定的线程。因此，请为每个客户端指定完整的所需 classpath。

## Java 版本说明

I2P 自 0.9.24 版本（2016年1月）起要求使用 Java 7。I2P 自 0.9.12 版本（2014年4月）起要求使用 Java 6。使用最新版本的 I2P 用户应当运行 1.7（7.0）JVM。

如果你的插件**不需要 1.7**：

-   确保所有 java 和 jsp 文件都使用 source="1.6" target="1.6" 进行编译。
-   确保所有捆绑的库 jar 文件也适用于 1.6 或更低版本。

如果你的插件**需要 1.7**：

-   注意在你的下载页面上。
-   在你的 plugin.config 中添加 min-java-version=1.7

无论如何，当使用 Java 8 编译时，你**必须**设置 bootclasspath 以防止运行时崩溃。

## 更新时 JVM 崩溃

注意 - 现在这些问题都应该已经修复了。

当更新插件的jar文件时，如果该插件自I2P启动以来一直在运行（即使插件后来被停止），JVM有崩溃的倾向。这个问题可能已经通过0.7.13-3版本中的类加载器实现得到了修复，但也可能没有。

最安全的做法是设计你的插件时将 jar 包放在 war 文件内部（对于 webapp），或者要求在更新后重启，或者不更新插件中的 jar 文件。

由于 webapp 内部类加载器的工作方式，如果您在 webapps.config 中指定 classpath，使用外部 jar 包_可能_是安全的。需要进行更多测试来验证这一点。如果只是为 webapp 需要，请不要在 clients.config 中使用"虚假"客户端来指定 classpath - 请改用 webapps.config。

最不安全的，也显然是大多数崩溃的根源，是在 clients.config 中的 classpath 里指定了插件 jar 文件的客户端。

这些在初始安装时都不应该是问题 - 插件的初始安装永远不应该需要重启。

## 参考资料

-   [配置文件规范](/docs/specs/configuration)
-   [DSA 密码学](/docs/specs/cryptography#DSA)
-   [更新规范](/docs/specs/updates)
