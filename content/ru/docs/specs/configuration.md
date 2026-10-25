---
title: "Спецификация файла конфигурации"
description: "Спецификация конфигурационных файлов I2P, используемых router и приложениями"
slug: "configuration"
aliases:
  - "/ru/configuration"
  - "/ru/configuration/"
category: "Форматы"
lastUpdated: "2023-01"
accurateFor: "0.9.57"
---

## Обзор

Эта страница содержит общую спецификацию конфигурационных файлов I2P, используемых router и различными приложениями. Она также предоставляет обзор информации, содержащейся в различных файлах, и ссылки на подробную документацию там, где она доступна.

## Общий формат

Конфигурационный файл I2P отформатирован в соответствии со спецификацией Java [Properties](http://docs.oracle.com/javase/1.5.0/docs/api/java/util/Properties.html#load%28java.io.InputStream%29) со следующими исключениями:

- Кодировка должна быть UTF-8
- Не использует и не распознает никаких экранирующих символов, включая `\`, поэтому строки не могут быть продолжены
- `#` или `;` начинает комментарий, но `!` не начинает
- `#` начинает комментарий в любой позиции, но `;` должна быть в первой колонке, чтобы начать комментарий
- Пробелы в начале и конце не обрезаются у ключей
- Пробелы в начале и конце обрезаются у значений
- `=` является единственным символом завершения ключа (не `:` или пробел)
- Строки без `=` игнорируются. Начиная с релиза 0.9.10 поддерживаются ключи со значением ""
- Поскольку экранирующих символов нет, ключи не могут содержать `#`, `=` или `\n`, или начинаться с `;`
- Поскольку экранирующих символов нет, значения не могут содержать `#` или `\n`, или начинаться или заканчиваться на `\r` или пробел

Файл не обязательно должен быть отсортирован, но большинство приложений сортируют по ключу при записи в файл для удобства чтения и ручного редактирования.

Чтение и запись реализованы в DataHelper loadProps() и storeProps() [DATAHELPER](http://docs.i2p-projekt.de/net/i2p/data/DataHelper.html). Обратите внимание, что формат файла значительно отличается от сериализованного формата для протоколов I2P, указанного в [Mapping](/docs/specs/common-structures/#type-mapping).

## Основная библиотека и router

### Клиенты (clients.config)

Настраивается через /configclients в консоли router. Начиная с релиза 0.9.42, файл clients.config по умолчанию разделён на отдельные конфигурационные файлы для каждого клиента в директории clients.config.d. После разделения свойства в отдельных файлах имеют префикс "clientApp.0.".

Формат следующий:

Строки имеют вид `clientApp.x.prop=val`, где x — это номер приложения. Номера приложений ДОЛЖНЫ начинаться с 0 и быть последовательными.

Свойства следующие:

**main** : Полное имя класса. Обязательно. : Будет выполнен конструктор или метод main() в этом классе, в зависимости от того, является ли клиент управляемым или неуправляемым. См. подробности ниже.

**name** : Имя, которое будет отображаться в консоли.

**args** : Аргументы для основного класса, разделенные пробелами или табуляциями. Аргументы, содержащие пробелы или табуляции, могут быть заключены в кавычки `'` или `"`

**delay** : Секунды до запуска, по умолчанию 120

**onBoot** : `{true|false}` : По умолчанию false, принудительно устанавливает задержку 0, переопределяет настройку задержки

**startOnLoad** : `{true|false}` : Должен ли клиент запускаться вообще? По умолчанию true

Следующие дополнительные свойства используются только плагинами:

**stopargs** : Аргументы для остановки клиента.

**uninstallargs** : Аргументы для удаления клиента.

**classpath** : Дополнительные элементы classpath для клиента, разделенные запятыми.

В строках args, stopargs, uninstallargs и classpath выполняются следующие подстановки, только для плагинов:

**$I2P** : Базовая директория установки I2P

**$CONFIG** : Каталог конфигурации пользователя (например ~/.i2p)

**$PLUGIN** : Директория этого плагина (например, ~/.i2p/plugins/foo)

**$OS** : Название операционной системы (например, "linux")

**$ARCH** : Название архитектуры (например, "amd64")

Все свойства, кроме "main", являются необязательными. Строки, начинающиеся с `#`, являются комментариями.

Если задержка меньше нуля, клиент будет ждать, пока router не достигнет состояния RUNNING, а затем немедленно запустится в новом потоке.

Если задержка равна нулю, клиент запускается немедленно в том же потоке, так что исключения могут быть переданы в консоль. В этом случае клиент должен либо выбросить исключение, либо быстро завершиться, либо создать свой собственный поток.

Если задержка больше нуля, выполнение будет происходить в новом потоке, и исключения будут записываться в журнал, но не передаваться в консоль.

Клиенты могут быть "управляемыми" или "неуправляемыми".

### Логгер (logger.config)

Настраивается через /configlogging в консоли router.

Свойства следующие:

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
### Индивидуальный плагин (plugins/*/plugin.config)

См. [спецификацию плагинов](/docs/specs/plugin). Обратите внимание, что плагины также могут содержать файлы clients.config, i2ptunnel.config и webapps.config.

### Плагины (plugins.config)

Включить/отключить для каждого установленного плагина.

Свойства следующие:

```
plugin.{name}.startOnLoad=true|false
```
### Веб-приложения (webapps.config)

Включить/отключить для каждого установленного веб-приложения.

Свойства следующие:

```
webapps.{name}.classpath=[space- or comma-separated paths]
webapps.{name}.startOnLoad=true|false
```
### Router (router.config)

Настраивается через /configadvanced в консоли router'а.

## Приложения

### Адресная книга (addressbook/config.txt)

См. документацию в SusiDNS.

### I2PSnark (i2psnark.config.d/i2psnark.config)

Настраивается через графический интерфейс приложения.

### Индивидуальный i2psnark (i2psnark.config.d/*/*.config)

Конфигурация для отдельного торрента. Настраивается через графический интерфейс приложения.

### I2PTunnel (i2ptunnel.config)

Настраивается через приложение /i2ptunnel в консоли router'а. Начиная с версии 0.9.42, файл i2ptunnel.config по умолчанию разделён на отдельные файлы конфигурации для каждого tunnel'а в директории i2ptunnel.config.d. После разделения свойства в отдельных файлах НЕ имеют префикса "tunnel.N.".

Примечание: Опции "tunnel.N.option.i2cp.*", хотя и выглядят как I2CP опции, реализованы в i2ptunnel и НЕ поддерживаются через другие интерфейсы или API, такие как I2CP или SAM.

Свойства следующие:

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
Примечание: Каждый 'N' — это номер туннеля, начинающийся с 0. Не должно быть пропусков в нумерации.

### Консоль Router'а

Консоль router использует файл router.config.

### SusiMail (susimail.config)

Смотрите пост на zzz.i2p.

## Ссылки

- [DATAHELPER](http://docs.i2p-projekt.de/net/i2p/data/DataHelper.html)
- [Отображение](/docs/specs/common-structures#type-mapping)
- [PLUGIN](/docs/specs/plugin)
- [Properties](http://docs.oracle.com/javase/1.5.0/docs/api/java/util/Properties.html#load%28java.io.InputStream%29)
