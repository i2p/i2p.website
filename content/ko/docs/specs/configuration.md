---
title: "설정 파일 규격"
description: "router와 애플리케이션에서 사용하는 I2P 설정 파일 사양"
slug: "configuration"
aliases:
  - "/ko/configuration"
  - "/ko/configuration/"
category: "형식"
lastUpdated: "2023-01"
accurateFor: "0.9.57"
---

## 개요

이 페이지는 router와 다양한 애플리케이션에서 사용되는 I2P 설정 파일의 일반적인 명세를 제공합니다. 또한 다양한 파일에 포함된 정보의 개요를 제공하고, 사용 가능한 경우 자세한 문서에 대한 링크를 제공합니다.

## 일반 형식

I2P 구성 파일은 Java [Properties](http://docs.oracle.com/javase/1.5.0/docs/api/java/util/Properties.html#load%28java.io.InputStream%29)에서 지정된 형식을 따르되, 다음과 같은 예외사항이 있습니다:

- 인코딩은 UTF-8이어야 함
- `\`를 포함한 어떤 이스케이프도 사용하거나 인식하지 않으므로 줄을 연결할 수 없음
- `#` 또는 `;`는 주석을 시작하지만 `!`는 그렇지 않음
- `#`는 어느 위치에서든 주석을 시작하지만 `;`는 주석을 시작하려면 1열에 있어야 함
- 키에서 앞뒤 공백이 제거되지 않음
- 값에서 앞뒤 공백이 제거됨
- `=`가 유일한 키 종료 문자임 (`:` 또는 공백 아님)
- `=`가 없는 줄은 무시됨. 릴리스 0.9.10부터 ""값을 가진 키가 지원됨.
- 이스케이프가 없으므로 키에는 `#`, `=`, 또는 `\n`이 포함될 수 없고 `;`로 시작할 수 없음
- 이스케이프가 없으므로 값에는 `#` 또는 `\n`이 포함될 수 없고 `\r` 또는 공백으로 시작하거나 끝날 수 없음

파일을 정렬할 필요는 없지만, 대부분의 애플리케이션은 읽기 쉽고 수동 편집을 용이하게 하기 위해 파일에 쓸 때 키별로 정렬합니다.

읽기와 쓰기는 DataHelper loadProps()와 storeProps() [DATAHELPER](http://docs.i2p-projekt.de/net/i2p/data/DataHelper.html)에서 구현됩니다. 파일 형식은 [Mapping](/docs/specs/common-structures/#type-mapping)에서 명시된 I2P 프로토콜의 직렬화 형식과 상당히 다르다는 점에 유의하세요.

## 핵심 라이브러리 및 router

### 클라이언트 (clients.config)

router console의 /configclients를 통해 구성됩니다. 릴리스 0.9.42부터 기본 clients.config 파일은 clients.config.d 디렉토리에서 각 클라이언트별로 개별 구성 파일로 분할됩니다. 분할된 후, 개별 파일의 속성들은 "clientApp.0." 접두사가 붙습니다.

형식은 다음과 같습니다:

라인은 `clientApp.x.prop=val` 형식이며, 여기서 x는 앱 번호입니다. 앱 번호는 반드시 0부터 시작하고 연속적이어야 합니다.

속성은 다음과 같습니다:

**main** : 전체 클래스 이름. 필수. : 클라이언트가 관리형인지 비관리형인지에 따라 이 클래스의 생성자 또는 main() 메서드가 실행됩니다. 자세한 내용은 아래를 참조하세요.

**name** : 콘솔에 표시될 이름.

**args** : 메인 클래스에 전달할 인수들로, 공백이나 탭으로 구분됩니다. 공백이나 탭을 포함하는 인수는 `'` 또는 `"`로 감쌀 수 있습니다

**delay** : 시작하기 전 대기 시간(초), 기본값 120

**onBoot** : `{true|false}` : 기본값 false, 지연 시간을 0으로 강제 설정하고 delay 설정을 무시함

**startOnLoad** : `{true|false}` : 클라이언트를 실행할지 여부입니다. 기본값은 true

다음 추가 속성들은 플러그인에서만 사용됩니다:

**stopargs** : 클라이언트를 중지하기 위한 인수들.

**uninstallargs** : 클라이언트를 제거하기 위한 인수입니다.

**classpath** : 클라이언트를 위한 추가적인 classpath 요소들, 쉼표로 구분됨.

다음 치환이 args, stopargs, uninstallargs, classpath 줄에서 플러그인에만 적용됩니다:

**$I2P** : I2P 기본 설치 디렉토리

**$CONFIG** : 사용자의 설정 디렉토리 (예: ~/.i2p)

**$PLUGIN** : 이 플러그인의 디렉토리 (예: ~/.i2p/plugins/foo)

**$OS** : 운영 체제 이름 (예: "linux")

**$ARCH** : 아키텍처 이름 (예: "amd64")

"main"을 제외한 모든 속성은 선택사항입니다. `#`로 시작하는 줄은 주석입니다.

지연 시간이 0보다 작으면, 클라이언트는 router가 RUNNING 상태에 도달할 때까지 기다린 후 새 스레드에서 즉시 시작됩니다.

지연 시간이 0과 같으면, 클라이언트가 같은 스레드에서 즉시 실행되어 예외가 콘솔로 전파될 수 있습니다. 이 경우, 클라이언트는 예외를 발생시키거나, 빠르게 반환하거나, 자체 스레드를 생성해야 합니다.

지연 시간이 0보다 크면 새 스레드에서 실행되며, 예외는 로그에 기록되지만 콘솔로 전파되지 않습니다.

클라이언트는 "관리형" 또는 "비관리형"일 수 있습니다.

### Logger (logger.config)

router console의 /configlogging을 통해 구성됩니다.

속성은 다음과 같습니다:

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
### 개별 플러그인 (plugins/*/plugin.config)

[플러그인 사양](/docs/specs/plugin)을 참조하세요. 플러그인에는 clients.config, i2ptunnel.config, webapps.config 파일도 포함될 수 있습니다.

### 플러그인 (plugins.config)

설치된 각 플러그인에 대해 활성화/비활성화합니다.

속성은 다음과 같습니다:

```
plugin.{name}.startOnLoad=true|false
```
### 웹앱 (webapps.config)

설치된 각 웹앱에 대해 활성화/비활성화합니다.

속성은 다음과 같습니다:

```
webapps.{name}.classpath=[space- or comma-separated paths]
webapps.{name}.startOnLoad=true|false
```
### Router (router.config)

router console의 /configadvanced를 통해 구성됩니다.

## 애플리케이션

### 주소록 (addressbook/config.txt)

SusiDNS의 문서를 참조하세요.

### I2PSnark (i2psnark.config.d/i2psnark.config)

애플리케이션 GUI를 통해 구성됩니다.

### 개별 i2psnark (i2psnark.config.d/*/*.config)

개별 torrent의 설정입니다. 애플리케이션 GUI를 통해 구성됩니다.

### I2PTunnel (i2ptunnel.config)

router console의 /i2ptunnel 애플리케이션을 통해 구성됩니다. 0.9.42 릴리스부터 기본 i2ptunnel.config 파일은 i2ptunnel.config.d 디렉토리의 각 tunnel별 개별 구성 파일로 분할됩니다. 분할된 후에는 개별 파일의 속성들이 "tunnel.N." 접두사를 붙이지 않습니다.

참고: "tunnel.N.option.i2cp.*" 옵션들은 I2CP 옵션으로 보이지만, i2ptunnel에서 구현되며, I2CP나 SAM과 같은 다른 인터페이스나 API를 통해서는 지원되지 않습니다.

속성은 다음과 같습니다:

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
참고: 각 'N'은 0부터 시작하는 터널 번호입니다. 번호 매김에는 빈 공간이 있어서는 안 됩니다.

### Router Console

router 콘솔은 router.config 파일을 사용합니다.

### SusiMail (susimail.config)

zzz.i2p의 게시물을 참조하세요.

## 참고자료

- [DATAHELPER](http://docs.i2p-projekt.de/net/i2p/data/DataHelper.html)
- [매핑](/docs/specs/common-structures#type-mapping)
- [플러그인](/docs/specs/plugin)
- [Properties](http://docs.oracle.com/javase/1.5.0/docs/api/java/util/Properties.html#load%28java.io.InputStream%29)
