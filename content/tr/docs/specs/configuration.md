---
title: "Yapılandırma Dosyası Spesifikasyonu"
description: "Router ve uygulamalar tarafından kullanılan I2P yapılandırma dosyalarının spesifikasyonu"
slug: "configuration"
aliases:
  - "/tr/configuration"
  - "/tr/configuration/"
category: "Formatlar"
lastUpdated: "2023-01"
accurateFor: "0.9.57"
---

## Genel Bakış

Bu sayfa, router ve çeşitli uygulamalar tarafından kullanılan I2P yapılandırma dosyalarının genel spesifikasyonunu sağlar. Ayrıca çeşitli dosyalarda bulunan bilgilere genel bir bakış sunar ve mevcut olduğunda ayrıntılı dokümantasyonlara bağlantılar verir.

## Genel Format

Bir I2P yapılandırma dosyası, aşağıdaki istisnalar dışında Java [Properties](http://docs.oracle.com/javase/1.5.0/docs/api/java/util/Properties.html#load%28java.io.InputStream%29) formatında belirtildiği gibi biçimlendirilir:

- Kodlama UTF-8 olmalıdır
- `\` dahil hiçbir kaçış karakterini kullanmaz veya tanımaz, bu nedenle satırlar devam ettirilemez
- `#` veya `;` yorum başlatır, ancak `!` başlatmaz
- `#` herhangi bir pozisyonda yorum başlatır ancak `;` yorum başlatmak için 1. sütunda olmalıdır
- Anahtarlarda başta ve sonda bulunan boşluklar kırpılmaz
- Değerlerde başta ve sonda bulunan boşluklar kırpılır
- `=` tek anahtar sonlandırma karakteridir (`:` veya boşluk değil)
- `=` içermeyen satırlar yok sayılır. 0.9.10 sürümü itibariyle, "" değerine sahip anahtarlar desteklenir.
- Kaçış karakteri olmadığından, anahtarlar `#`, `=`, veya `\n` içeremez veya `;` ile başlayamaz
- Kaçış karakteri olmadığından, değerler `#` veya `\n` içeremez veya `\r` ya da boşluk ile başlayıp bitemez

Dosyanın sıralanmış olması gerekmez, ancak çoğu uygulama dosyaya yazarken okunabilirlik ve manuel düzenleme kolaylığı için anahtara göre sıralama yapar.

Okuma ve yazma işlemleri DataHelper loadProps() ve storeProps() [DATAHELPER](http://docs.i2p-projekt.de/net/i2p/data/DataHelper.html) fonksiyonlarında uygulanmıştır. Dosya formatının, [Mapping](/docs/specs/common-structures/#type-mapping) bölümünde belirtilen I2P protokolleri için serileştirilmiş formattan önemli ölçüde farklı olduğunu unutmayın.

## Çekirdek kütüphane ve router

### İstemciler (clients.config)

Router konsolundaki /configclients üzerinden yapılandırılır. 0.9.42 sürümünden itibaren, varsayılan clients.config dosyası clients.config.d dizinindeki her istemci için ayrı yapılandırma dosyalarına bölünmüştür. Bölündükten sonra, bireysel dosyalardaki özellikler "clientApp.0." ön ekiyle başlar.

Format şu şekildedir:

Satırlar `clientApp.x.prop=val` formundadır, burada x uygulama numarasıdır. Uygulama numaraları 0 ile başlamalı ve ardışık olmalıdır.

Özellikler şunlardır:

**main** : Tam sınıf adı. Gerekli. : Bu sınıftaki constructor veya main() yöntemi, istemcinin yönetimli veya yönetimsiz olmasına bağlı olarak çalıştırılacaktır. Ayrıntılar için aşağıya bakınız.

**name** : Konsolda görüntülenecek isim.

**args** : Ana sınıfa iletilecek argümanlar, boşluk veya sekme ile ayrılır. Boşluk veya sekme içeren argümanlar `'` veya `"` ile tırnak içine alınabilir

**delay** : Başlamadan önceki saniye, varsayılan 120

**onBoot** : `{true|false}` : Varsayılan false, 0 gecikmesi zorlar, gecikme ayarını geçersiz kılar

**startOnLoad** : `{true|false}` : İstemci çalıştırılacak mı? Varsayılan true

Aşağıdaki ek özellikler yalnızca eklentiler tarafından kullanılır:

**stopargs** : İstemciyi durdurmak için argümanlar.

**uninstallargs** : İstemciyi kaldırmak için kullanılan argümanlar.

**classpath** : İstemci için virgülle ayrılmış ek classpath öğeleri.

Aşağıdaki değişimler yalnızca eklentiler için args, stopargs, uninstallargs ve classpath satırlarında yapılır:

**$I2P** : Temel I2P kurulum dizini

**$CONFIG** : Kullanıcının yapılandırma dizini (örn. ~/.i2p)

**$PLUGIN** : Bu eklentinin dizini (örn. ~/.i2p/plugins/foo)

**$OS** : İşletim sistemi adı (örn. "linux")

**$ARCH** : Mimari adı (örn. "amd64")

"main" dışındaki tüm özellikler isteğe bağlıdır. `#` ile başlayan satırlar yorumdur.

Gecikme süresi sıfırdan küçükse, istemci router RUNNING durumuna ulaşana kadar bekleyecek ve ardından yeni bir thread'de hemen başlayacaktır.

Gecikme sıfıra eşitse, istemci aynı thread'de hemen çalıştırılır, böylece istisnalar konsola yayılabilir. Bu durumda, istemci ya bir istisna fırlatmalı, hızlıca geri dönmeli veya kendi thread'ini oluşturmalıdır.

Gecikme sıfırdan büyükse, yeni bir thread'de çalıştırılacak ve istisnalar günlüğe kaydedilecek ancak konsola yayılmayacaktır.

İstemciler "yönetilen" veya "yönetilmeyen" olabilir.

### Logger (logger.config)

Router konsolunda /configlogging aracılığıyla yapılandırılır.

Özellikler şu şekildedir:

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
### Bireysel Plugin (plugins/*/plugin.config)

[Eklenti spesifikasyonuna](/docs/specs/plugin) bakın. Eklentilerin ayrıca clients.config, i2ptunnel.config ve webapps.config dosyalarını içerebileceğini unutmayın.

### Eklentiler (plugins.config)

Her yüklü eklenti için etkinleştir/devre dışı bırak.

Özellikler şu şekildedir:

```
plugin.{name}.startOnLoad=true|false
```
### Web Uygulamaları (webapps.config)

Her yüklü webapp için etkinleştir/devre dışı bırak.

Özellikler şu şekildedir:

```
webapps.{name}.classpath=[space- or comma-separated paths]
webapps.{name}.startOnLoad=true|false
```
### Router (router.config)

Router konsolunda /configadvanced üzerinden yapılandırılır.

## Uygulamalar

### Adres Defteri (addressbook/config.txt)

SusiDNS'teki belgelere bakın.

### I2PSnark (i2psnark.config.d/i2psnark.config)

Uygulama GUI'si aracılığıyla yapılandırılır.

### Bireysel i2psnark (i2psnark.config.d/*/*.config)

Bireysel bir torrent için yapılandırma. Uygulama arayüzü üzerinden yapılandırılır.

### I2PTunnel (i2ptunnel.config)

Router konsolundaki /i2ptunnel uygulaması aracılığıyla yapılandırılır. 0.9.42 sürümünden itibaren, varsayılan i2ptunnel.config dosyası i2ptunnel.config.d dizininde her tunnel için ayrı yapılandırma dosyalarına bölünmüştür. Bölündükten sonra, bireysel dosyalardaki özellikler "tunnel.N." ile ÖNEKLENMEMİŞTİR.

Not: "tunnel.N.option.i2cp.*" seçenekleri, I2CP seçenekleri gibi görünse de i2ptunnel içinde uygulanmıştır ve I2CP veya SAM gibi diğer arayüzler veya API'ler aracılığıyla DESTEKLENMEMEKTEDİR.

Özellikler şu şekildedir:

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
Not: Her 'N' 0'dan başlayan bir tunnel numarasıdır. Numaralandırmada boşluk olmamalıdır.

### Router Konsolu

Router konsolu router.config dosyasını kullanır.

### SusiMail (susimail.config)

zzz.i2p'deki yazıya bakın.

## Referanslar

- [DATAHELPER](http://docs.i2p-projekt.de/net/i2p/data/DataHelper.html)
- [Eşleme](/docs/specs/common-structures#type-mapping)
- [PLUGIN](/docs/specs/plugin)
- [Properties](http://docs.oracle.com/javase/1.5.0/docs/api/java/util/Properties.html#load%28java.io.InputStream%29)
