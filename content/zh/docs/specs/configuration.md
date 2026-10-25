---
title: "配置文件规范"
description: "router 和应用程序使用的 I2P 配置文件规范"
slug: "configuration"
aliases:
  - "/zh/configuration"
  - "/zh/configuration/"
category: "格式"
lastUpdated: "2023-01"
accurateFor: "0.9.57"
---

## 概览

本页面提供了I2P配置文件的通用规范，这些文件被router和各种应用程序使用。它还概述了各种文件中包含的信息，并在可用的情况下提供了详细文档的链接。

## 通用格式

I2P配置文件按照Java [Properties](http://docs.oracle.com/javase/1.5.0/docs/api/java/util/Properties.html#load%28java.io.InputStream%29)规范格式化，但有以下例外：

- 编码必须是 UTF-8
- 不使用或识别任何转义字符，包括 `\`，因此行不能被续行
- `#` 或 `;` 开始注释，但 `!` 不能
- `#` 可以在任何位置开始注释，但 `;` 必须在第 1 列才能开始注释
- 键的前导和尾随空白字符不会被删除
- 值的前导和尾随空白字符会被删除
- `=` 是唯一的键终止字符（不是 `:` 或空白字符）
- 没有 `=` 的行会被忽略。从 0.9.10 版本开始，支持值为 "" 的键
- 由于没有转义字符，键不能包含 `#`、`=` 或 `\n`，也不能以 `;` 开始
- 由于没有转义字符，值不能包含 `#` 或 `\n`，也不能以 `\r` 或空白字符开始或结束

文件无需排序，但大多数应用程序在写入文件时会按键排序，以便于阅读和手动编辑。

读取和写入操作在 DataHelper loadProps() 和 storeProps() [DATAHELPER](http://docs.i2p-projekt.de/net/i2p/data/DataHelper.html) 中实现。请注意，文件格式与 [映射](/docs/specs/common-structures/#type-mapping) 中指定的 I2P 协议序列化格式有显著差异。

## 核心库和router

### 客户端 (clients.config)

通过 router console 中的 /configclients 进行配置。从 0.9.42 版本开始，默认的 clients.config 文件被拆分为 clients.config.d 目录中每个客户端的单独配置文件。拆分后，单独文件中的属性都以 "clientApp.0." 为前缀。

格式如下：

配置行的格式为 `clientApp.x.prop=val`，其中 x 是应用程序编号。应用程序编号必须从 0 开始且连续。

属性如下：

**main** : 完整类名。必需。: 此类中的构造函数或main()方法将被运行，这取决于客户端是托管的还是非托管的。详细信息请参见下文。

**name** : 在控制台上显示的名称。

**args** : 主类的参数，用空格或制表符分隔。包含空格或制表符的参数可以用 `'` 或 `"` 引用

**delay** : 启动前的延迟秒数，默认为 120

**onBoot** : `{true|false}` : 默认为 false，强制延迟为 0，覆盖延迟设置

**startOnLoad** : `{true|false}` : 客户端是否要运行？默认为 true

以下附加属性仅由插件使用：

**stopargs** : 停止客户端的参数。

**uninstallargs** : 卸载客户端的参数。

**classpath** : 客户端的额外 classpath 元素，用逗号分隔。

以下替换仅适用于插件的 args、stopargs、uninstallargs 和 classpath 行：

**$I2P** : I2P 基本安装目录

**$CONFIG**：用户的配置目录（例如 ~/.i2p）

**$PLUGIN** : 此插件的目录（例如 ~/.i2p/plugins/foo）

**$OS** : 操作系统名称（例如 "linux"）

**$ARCH** : 架构名称（例如 "amd64"）

除了"main"之外的所有属性都是可选的。以`#`开头的行是注释。

如果延迟小于零，客户端将等待直到 router 达到 RUNNING 状态，然后立即在新线程中启动。

如果延迟等于零，客户端会立即运行，在同一个线程中，以便异常可以传播到控制台。在这种情况下，客户端应该要么抛出异常，要么快速返回，要么生成自己的线程。

如果延迟大于零，它将在新线程中运行，异常将被记录但不会传播到控制台。

客户端可以是"托管的"或"非托管的"。

### 日志记录器 (logger.config)

通过路由器控制台中的 /configlogging 进行配置。

属性如下：

```
# Default 20
logger.consoleBufferSize=n
# Default from locale; format as specified by Java SimpleDateFormat
logger.dateFormat=HH:mm:ss.SSS
# Default ERROR
logger.defaultLevel=CRIT|ERROR|WARN|INFO|DEBUG
# Default true
logger.displayOnScreen=true|false
# Default true
logger.dropDuplicates=true|false
# Default false
logger.dropOnOverflow=true|false
# As of 0.9.18. Default 29 (seconds)
logger.flushInterval=nnn
# d = date, c = class, t = thread name, p = priority, m = message
logger.format={dctpm}*
# As of 0.9.56. Default false
logger.gzip=true|false
# Max to buffer before flushing. Default 1024
logger.logBufferSize=n
# Default logs/log-@.txt; @ replaced with number
logger.logFileName=name
logger.logFilenameOverride=name
# Default 10M
logger.logFileSize=nnn[K|M|G]
# Highest file number. Default 2
logger.logRotationLimit=n
# As of 0.9.56. Default 65536 (bytes)
logger.minGzipSize=nnnnn
# Default CRIT
logger.minimumOnScreenLevel=CRIT|ERROR|WARN|INFO|DEBUG
logger.record.{class}=CRIT|ERROR|WARN|INFO|DEBUG
```
### 单个插件 (plugins/*/plugin.config)

参见 [plugin specification](/docs/specs/plugin)。注意插件也可能包含 clients.config、i2ptunnel.config 和 webapps.config 文件。

### 插件 (plugins.config)

为每个已安装的插件启用/禁用。

属性如下：

```
plugin.{name}.startOnLoad=true|false
```
### 网络应用程序 (webapps.config)

为每个已安装的网络应用启用/禁用。

属性如下：

```
webapps.{name}.classpath=[space- or comma-separated paths]
webapps.{name}.startOnLoad=true|false
```
### Router (router.config)

通过 router console 中的 /configadvanced 进行配置。

## 应用程序

### 地址簿 (addressbook/config.txt)

请参阅 SusiDNS 中的文档。

### I2PSnark (i2psnark.config.d/i2psnark.config)

通过应用程序图形界面进行配置。

### 单个 i2psnark (i2psnark.config.d/*/*.config)

单个种子的配置。通过应用程序图形界面进行配置。

### I2PTunnel (i2ptunnel.config)

通过路由器控制台中的 /i2ptunnel 应用程序进行配置。从 0.9.42 版本开始，默认的 i2ptunnel.config 文件被拆分为 i2ptunnel.config.d 目录中每个 tunnel 的独立配置文件。拆分后，独立文件中的属性不再以 "tunnel.N." 为前缀。

注意："tunnel.N.option.i2cp.*" 选项虽然看起来像是 I2CP 选项，但实际上是在 i2ptunnel 中实现的，通过其他接口或 API（如 I2CP 或 SAM）并不支持这些选项。

属性如下：

```
# Display description for UI
tunnel.N.description=

# Router IP address or host name. Ignored if in router context.
tunnel.N.i2cpHost=127.0.0.1

# Router I2CP port. Ignored if in router context.
tunnel.N.i2cpPort=nnnn

# For clients only. Local listen IP address or host name.
tunnel.N.interface=127.0.0.1

# For clients only. Local listen port.
tunnel.N.listenPort=nnnn

# Display name for UI
tunnel.N.name=

# Servers only. Default false. Originate connections to local server with a
# unique IP per-remote-destination.
tunnel.N.option.enableUniqueLocal=true|false

# Clients only. Do not open the socket manager and build tunnels
# until the first socket is opened on the local port.
# Default false
tunnel.N.option.i2cp.delayOpen=true|false

# Servers only. Persistent private leaseset key
tunnel.N.option.i2cp.leaseSetPrivateKey=base64

# Servers only. Persistent private leaseset key
tunnel.N.option.i2cp.leaseSetSigningPrivateKey=sigtype:base64

# Clients only. Create a new destination when reopening the socket manager,
# after it was previously closed due to an idle timeout.
# Default false
# When true, requires I2CP option i2cp.closeOnIdle=true
# When true, tunnel.N.option.persistentClientKey must be unset or false
tunnel.N.option.i2cp.newDestOnResume=true|false

# Servers only. The maximum size of the thread pool, default 65. Ignored
# for standard servers.
tunnel.N.option.i2ptunnel.blockingHandlerCount=nnn

# HTTP client only. Whether to use allow SSL connections to i2p addresses.
# Default false.
tunnel.N.option.i2ptunnel.httpclient.allowInternalSSL=true|false

# HTTP client only. Whether to disable address helper links. Default false.
tunnel.N.option.i2ptunnel.httpclient.disableAddressHelper=true|false

# HTTP client only. Comma- or space-separated list of jump server URLs.
tunnel.N.option.i2ptunnel.httpclient.jumpServers=http://example.i2p/jump

# HTTP client only. Whether to pass Accept* headers through. Default false.
# Note: Does not affect "Accept" and "Accept-Encoding".
tunnel.N.option.i2ptunnel.httpclient.sendAccept=true|false

# HTTP client only. Whether to pass Referer headers through. Default false.
tunnel.N.option.i2ptunnel.httpclient.sendReferer=true|false

# HTTP client only. Whether to pass User-Agent headers through. Default
# false.
tunnel.N.option.i2ptunnel.httpclient.sendUserAgent=true|false

# HTTP client only. Whether to pass Via headers through. Default false.
tunnel.N.option.i2ptunnel.httpclient.sendVia=true|false

# HTTP client only. Comma- or space-separated list of in-network SSL
# outproxies.
tunnel.N.option.i2ptunnel.httpclient.SSLOutproxies=example.i2p

# SOCKS client only. Comma- or space-separated list of in-network
# outproxies for any ports not specified.
tunnel.N.option.i2ptunnel.socks.proxy.default=example.i2p

# SOCKS client only. Comma- or space-separated list of in-network
# outproxies for port NNNN.
tunnel.N.option.i2ptunnel.socks.proxy.NNNN=example.i2p

# HTTP client only. Whether to use a registered local outproxy plugin.
# Default true.
tunnel.N.option.i2ptunnel.useLocalOutproxy=true|false

# Servers only. Whether to use a thread pool. Default true. Ignored for
# standard servers, always false.
tunnel.N.option.i2ptunnel.usePool=true|false

# IRC Server only. Only used if fakeHostname contains a %c.  If unset,
# cloak with a random value that is persistent for the life of this tunnel.
# If set, cloak with the hash of this passphrase.  Use to have consistent
# mangling across restarts, or for multiple IRC servers cloak consistently
# to be able to track users even when they switch servers.  Note: don't
# quote or put spaces in the passphrase, the i2ptunnel gui can't handle it.
tunnel.N.option.ircserver.cloakKey=

# IRC Server only. Set the fake hostname sent by I2PTunnel, %f is the full
# B32 destination hash, %c is the cloaked hash.
tunnel.N.option.ircserver.fakeHostname=%f.b32.i2p

# IRC Server only. Default user.
tunnel.N.option.ircserver.method=user|webirc

# IRC Server only. The password to use for the webirc protocol.  Note:
# don't quote or put spaces in the passphrase, the i2ptunnel gui can't
# handle it.
tunnel.N.option.ircserver.webircPassword=

# IRC Server only.
tunnel.N.option.ircserver.webircSpoofIP=

# For clients only. Alias for the private key in the keystore for the SSL
# socket. Will be autogenerated if a new key is created.
tunnel.N.option.keyAlias=

# For clients only. Password for the private key for the SSL socket. Will be
# autogenerated if a new key is created.
tunnel.N.option.keyPassword=

# For clients only. Path to the keystore file containing the private key for
# the SSL socket. Will be autogenerated if a new keystore is created.
# Relative to $(I2P_CONFIG_DIR)/keystore/ if not absolute.
tunnel.N.option.keystoreFile=i2ptunnel-(random string).ks

# For clients only. Password for the keystore containing the private key for
# the SSL socket. Default is "changeit".
tunnel.N.option.keystorePassword=changeit

# HTTP Server only. Max number of POSTs allowed for one destination per
# postCheckTime. Default 0 (unlimited)
tunnel.N.option.maxPosts=nnn

# HTTP Server only. Max number of POSTs allowed for all destinations per
# postCheckTime. Default 0 (unlimited)
tunnel.N.option.maxTotalPosts=nnn

# HTTP Clients only. Whether to send authorization to an outproxy. Default
# false.
tunnel.N.option.outproxyAuth=true|false

# HTTP Clients only. The password for the outproxy authorization.
tunnel.N.option.outproxyPassword=

# HTTP Clients only. The username for the outproxy authorization.
tunnel.N.option.outproxyUsername=

# SOCKS client only. The type of the configured outproxies: socks or connect (HTTPS).
# Default socks. As of 0.9.57.
tunnel.N.option.outproxyType=socks|connect

# Clients only. Whether to store a destination in a private key file and
# reuse it. Default false.
# When true, tunnel.N.option.newDestOnResume must be unset or false
tunnel.N.option.persistentClientKey=true|false

# HTTP Server only. Time period for banning POSTs from a single destination
# after maxPosts is exceeded, in seconds. Default 1800 seconds.
tunnel.N.option.postBanTime=nnn

# HTTP Server only. Time period for checking maxPosts and maxTotalPosts, in
# seconds. Default 300 seconds.
tunnel.N.option.postCheckTime=nnn

# HTTP Server only. Time period for banning all POSTs after maxTotalPosts
# is exceeded, in seconds. Default 600 seconds.
tunnel.N.option.postTotalBanTime=nnn

# HTTP Clients only. Whether to require local authorization for the proxy.
# Default false. "true" is the same as "basic".
tunnel.N.option.proxyAuth=true|false|basic|digest

# HTTP Clients only. The MD5 of the password for local authorization for
# user USER.
tunnel.N.option.proxy.auth.USER.md5=(32 char lowercase hex)

# HTTP Clients only. The SHA-256 of the password for local authorization for
# user USER. (RFC 7616) Since 0.9.56
tunnel.N.option.proxy.auth.USER.sha256=(64 char lowercase hex)

# HTTP Servers only. Whether to reject incoming connections apparently via
# an inproxy. Default false.
tunnel.N.option.rejectInproxy=true|false

# HTTP Servers only. Whether to reject incoming connections containing a
# referer header. Default false. Since 0.9.25.
tunnel.N.option.rejectReferer=true|false

# HTTP Servers only. Whether to reject incoming connections containing
# specific user-agent headers. Default false. Since 0.9.25. See
# tunnel.N.option.userAgentRejectList
tunnel.N.option.rejectUserAgents=true|false

# Servers only. Overrides targetHost and targetPort for incoming port NNNN.
tunnel.N.option.targetForPort.NNNN=hostnameOrIP:nnnn

# HTTP Servers only. Comma-separated list of strings to match in the
# user-agent header. Since 0.9.25. Example: "Mozilla,Opera". Case-sensitive.
# As of 0.9.33, a string of "none" may be used to match an empty user-agent.
# See tunnel.N.option.rejectUserAgents
tunnel.N.option.userAgentRejectList=string1[,string2]*

# Default false. For servers, use SSL for connections to local server. For
# clients, SSL is required for connections from local clients.
tunnel.N.option.useSSL=false

# Each option is passed to I2CP and streaming with "tunnel.N.option."
# stripped off. See those docs.
tunnel.N.option.*=

# For servers and clients with persistent keys only. Absolute path or
# relative to config directory.
tunnel.N.privKeyFile=filename

# For proxies only. Comma- or space-separated host names.
tunnel.N.proxyList=example.i2p[,example2.i2p]

# For clients only. Default false.
tunnel.N.sharedClient=true|false

# For HTTP servers only. Host name to be passed to the local server in the
# HTTP headers.  Default is the base 32 hostname.
tunnel.N.spoofedHost=example.i2p

# For HTTP servers only. Host name to be passed to the local server in the
# HTTP headers.  Overrides above setting for incoming port NNNN, to allow
# virtual hosts.
tunnel.N.spoofedHost.NNNN=example.i2p

# Default true
tunnel.N.startOnLoad=true|false

# For clients only. Comma- or space-separated host names or host:port.
tunnel.N.targetDestination=example.i2p[:nnnn][,example2.i2p[:nnnn]]

# For servers only. Local IP address or host name to connect to.
tunnel.N.targetHost=

# For servers only. Port on targetHost to connect to.
tunnel.N.targetPort=nnnn

# The type of i2ptunnel
tunnel.N.type=client|connectclient|httpbidirserver|httpclient|httpserver|ircclient|ircserver|
          server|socksirctunnel|sockstunnel|streamrclient|streamrserver
```
注意：每个 'N' 是一个从 0 开始的 tunnel 编号。编号中不能有任何间隔。

### Router 控制台

router 控制台使用 router.config 文件。

### SusiMail (susimail.config)

请查看 zzz.i2p 上的帖子。

## 参考资料

- [DATAHELPER](http://docs.i2p-projekt.de/net/i2p/data/DataHelper.html)
- [映射](/docs/specs/common-structures#type-mapping)
- [插件](/docs/specs/plugin)
- [属性](http://docs.oracle.com/javase/1.5.0/docs/api/java/util/Properties.html#load%28java.io.InputStream%29)
