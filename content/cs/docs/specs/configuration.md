---
title: "Specifikace konfiguračního souboru"
description: "Specifikace konfiguračních souborů I2P používaných routerem a aplikacemi"
slug: "configuration"
aliases:
  - "/cs/configuration"
  - "/cs/configuration/"
category: "Formáty"
lastUpdated: "2023-01"
accurateFor: "0.9.57"
---

## Přehled

Tato stránka poskytuje obecnou specifikaci konfiguračních souborů I2P, které používá router a různé aplikace. Také poskytuje přehled informací obsažených v různých souborech a odkazy na podrobnou dokumentaci, kde je k dispozici.

## Obecný formát

Konfigurační soubor I2P je formátován podle specifikace Java [Properties](http://docs.oracle.com/javase/1.5.0/docs/api/java/util/Properties.html#load%28java.io.InputStream%29) s následujícími výjimkami:

- Kódování musí být UTF-8
- Nepoužívá ani nerozpoznává žádné escape sekvence, včetně `\`, takže řádky nelze pokračovat
- `#` nebo `;` začíná komentář, ale `!` nezačíná
- `#` začíná komentář na jakékoli pozici, ale `;` musí být ve sloupci 1, aby začal komentář
- Úvodní a koncové mezery nejsou u klíčů odstraněny
- Úvodní a koncové mezery jsou u hodnot odstraněny
- `=` je jediný znak ukončující klíč (ne `:` nebo mezera)
- Řádky bez `=` jsou ignorovány. Od vydání 0.9.10 jsou podporovány klíče s hodnotou ""
- Protože neexistují escape sekvence, klíče nesmí obsahovat `#`, `=` nebo `\n`, ani začínat `;`
- Protože neexistují escape sekvence, hodnoty nesmí obsahovat `#` nebo `\n`, ani začínat nebo končit `\r` nebo mezerou

Soubor nemusí být seřazen, ale většina aplikací při zápisu do souboru řadí podle klíče pro snadnější čtení a ruční úpravy.

Čtení a zápis jsou implementovány v DataHelper loadProps() a storeProps() [DATAHELPER](http://docs.i2p-projekt.de/net/i2p/data/DataHelper.html). Všimněte si, že formát souboru se významně liší od serializovaného formátu pro I2P protokoly specifikovaného v [Mapping](/docs/specs/common-structures/#type-mapping).

## Základní knihovna a router

### Klienti (clients.config)

Konfiguruje se přes /configclients v konzoli routeru. Od verze 0.9.42 je výchozí soubor clients.config rozdělen do jednotlivých konfiguračních souborů pro každého klienta v adresáři clients.config.d. Po rozdělení jsou vlastnosti v jednotlivých souborech opatřeny prefixem "clientApp.0.".

Formát je následující:

Řádky mají formu `clientApp.x.prop=val`, kde x je číslo aplikace. Čísla aplikací MUSÍ začínat 0 a být po sobě jdoucí.

Vlastnosti jsou následující:

**main** : Úplný název třídy. Povinný. : Konstruktor nebo metoda main() v této třídě bude spuštěna v závislosti na tom, zda je klient spravovaný nebo nespravovaný. Podrobnosti viz níže.

**name** : Název, který se zobrazí na konzoli.

**args** : Argumenty pro hlavní třídu, oddělené mezerami nebo tabulátory. Argumenty obsahující mezery nebo tabulátory mohou být uzavřeny do uvozovek `'` nebo `"`

**delay** : Sekundy před spuštěním, výchozí 120

**onBoot** : `{true|false}` : Výchozí false, vynutí zpoždění 0, přepíše nastavení zpoždění

**startOnLoad** : `{true|false}` : Má být klient vůbec spuštěn? Výchozí true

Následující dodatečné vlastnosti jsou používány pouze pluginy:

**stopargs** : Argumenty pro zastavení klienta.

**uninstallargs** : Argumenty pro odinstalování klienta.

**classpath** : Další prvky classpath pro klienta, oddělené čárkami.

Následující substituce jsou prováděny v řádcích args, stopargs, uninstallargs a classpath pouze pro pluginy:

**$I2P** : Základní instalační adresář I2P

**$CONFIG** : Konfigurační adresář uživatele (např. ~/.i2p)

**$PLUGIN** : Adresář tohoto pluginu (např. ~/.i2p/plugins/foo)

**$OS** : Název operačního systému (např. "linux")

**$ARCH** : Název architektury (např. "amd64")

Všechny vlastnosti kromě "main" jsou volitelné. Řádky začínající `#` jsou komentáře.

Pokud je zpoždění menší než nula, klient bude čekat, dokud router nedosáhne stavu RUNNING, a poté se okamžitě spustí v novém vlákně.

Pokud je zpoždění rovno nule, klient se spustí okamžitě ve stejném vláknu, takže výjimky mohou být propagovány do konzole. V tomto případě by klient měl buď vyhodit výjimku, rychle se vrátit, nebo vytvořit své vlastní vlákno.

Pokud je zpoždění větší než nula, bude spuštěno v novém vlákně a výjimky budou zaznamenány do logu, ale nebudou propagovány do konzole.

Klienti mohou být "spravovaní" nebo "nespravovaní".

### Logger (logger.config)

Konfigurováno přes /configlogging v konzoli routeru.

Vlastnosti jsou následující:

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
### Individuální Plugin (plugins/*/plugin.config)

Viz [specifikaci pluginu](/docs/specs/plugin). Všimněte si, že pluginy mohou také obsahovat soubory clients.config, i2ptunnel.config a webapps.config.

### Pluginy (plugins.config)

Povolit/zakázat pro každý nainstalovaný plugin.

Vlastnosti jsou následující:

```
plugin.{name}.startOnLoad=true|false
```
### Webové aplikace (webapps.config)

Povolit/zakázat pro každou nainstalovanou webovou aplikaci.

Vlastnosti jsou následující:

```
webapps.{name}.classpath=[space- or comma-separated paths]
webapps.{name}.startOnLoad=true|false
```
### Router (router.config)

Konfigurace přes /configadvanced v konzoli routeru.

## Aplikace

### Adresář (addressbook/config.txt)

Viz dokumentaci v SusiDNS.

### I2PSnark (i2psnark.config.d/i2psnark.config)

Konfigurováno prostřednictvím grafického rozhraní aplikace.

### Jednotlivé i2psnark (i2psnark.config.d/*/*.config)

Konfigurace pro jednotlivý torrent. Konfiguruje se přes grafické uživatelské rozhraní aplikace.

### I2PTunnel (i2ptunnel.config)

Konfigurováno prostřednictvím aplikace /i2ptunnel v konzole routeru. Od verze 0.9.42 je výchozí soubor i2ptunnel.config rozdělen na jednotlivé konfigurační soubory pro každý tunnel v adresáři i2ptunnel.config.d. Po rozdělení NEJSOU vlastnosti v jednotlivých souborech předponovány "tunnel.N.".

Poznámka: Možnosti "tunnel.N.option.i2cp.*", i když se zdají být I2CP možnosti, jsou implementovány v i2ptunnel a NEJSOU podporovány prostřednictvím jiných rozhraní nebo API jako jsou I2CP nebo SAM.

Vlastnosti jsou následující:

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
Poznámka: Každé 'N' je číslo tunnelu začínající 0. V číslování nesmí být žádné mezery.

### Router Console

Konzole routeru používá soubor router.config.

### SusiMail (susimail.config)

Viz příspěvek na zzz.i2p.

## Reference

- [DATAHELPER](http://docs.i2p-projekt.de/net/i2p/data/DataHelper.html)
- [Mapování](/docs/specs/common-structures#type-mapping)
- [PLUGIN](/docs/specs/plugin)
- [Properties](http://docs.oracle.com/javase/1.5.0/docs/api/java/util/Properties.html#load%28java.io.InputStream%29)
