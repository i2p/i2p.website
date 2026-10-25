---
title: "Konfigurationsdatei-Spezifikation"
description: "Spezifikation der I2P-Konfigurationsdateien, die vom Router und Anwendungen verwendet werden"
slug: "configuration"
aliases:
  - "/de/configuration"
  - "/de/configuration/"
category: "Formate"
lastUpdated: "2023-01"
accurateFor: "0.9.57"
---

## Überblick

Diese Seite bietet eine allgemeine Spezifikation der I2P-Konfigurationsdateien, die vom router und verschiedenen Anwendungen verwendet werden. Sie gibt auch einen Überblick über die Informationen, die in den verschiedenen Dateien enthalten sind, und verlinkt zu detaillierter Dokumentation, wo verfügbar.

## Allgemeines Format

Eine I2P-Konfigurationsdatei ist formatiert wie in Java [Properties](http://docs.oracle.com/javase/1.5.0/docs/api/java/util/Properties.html#load%28java.io.InputStream%29) spezifiziert, mit folgenden Ausnahmen:

- Kodierung muss UTF-8 sein
- Verwendet oder erkennt keine Escape-Zeichen, einschließlich `\`, daher können Zeilen nicht fortgesetzt werden
- `#` oder `;` beginnt einen Kommentar, aber `!` nicht
- `#` beginnt einen Kommentar an jeder Position, aber `;` muss in Spalte 1 stehen, um einen Kommentar zu beginnen
- Führende und nachgestellte Leerzeichen werden bei Schlüsseln nicht entfernt
- Führende und nachgestellte Leerzeichen werden bei Werten entfernt
- `=` ist das einzige Schlüssel-Abschlusszeichen (nicht `:` oder Leerzeichen)
- Zeilen ohne `=` werden ignoriert. Seit Release 0.9.10 werden Schlüssel mit dem Wert "" unterstützt.
- Da es keine Escape-Zeichen gibt, dürfen Schlüssel nicht `#`, `=` oder `\n` enthalten oder mit `;` beginnen
- Da es keine Escape-Zeichen gibt, dürfen Werte nicht `#` oder `\n` enthalten oder mit `\r` oder Leerzeichen beginnen oder enden

Die Datei muss nicht sortiert sein, aber die meisten Anwendungen sortieren beim Schreiben in die Datei nach Schlüssel, um das Lesen und manuelle Bearbeiten zu erleichtern.

Lese- und Schreibvorgänge sind in DataHelper loadProps() und storeProps() [DATAHELPER](http://docs.i2p-projekt.de/net/i2p/data/DataHelper.html) implementiert. Beachten Sie, dass sich das Dateiformat erheblich vom serialisierten Format für I2P-Protokolle unterscheidet, das in [Mapping](/docs/specs/common-structures/#type-mapping) spezifiziert ist.

## Kernbibliothek und Router

### Clients (clients.config)

Konfiguriert über /configclients in der router-Konsole. Ab Release 0.9.42 ist die Standard-clients.config-Datei in einzelne Konfigurationsdateien für jeden Client im clients.config.d-Verzeichnis aufgeteilt. Nach der Aufteilung werden die Eigenschaften in den einzelnen Dateien mit "clientApp.0." vorangestellt.

Das Format ist wie folgt:

Zeilen haben die Form `clientApp.x.prop=val`, wobei x die App-Nummer ist. App-Nummern MÜSSEN bei 0 beginnen und aufeinanderfolgend sein.

Die Eigenschaften sind wie folgt:

**main** : Vollständiger Klassenname. Erforderlich. : Der Konstruktor oder die main()-Methode in dieser Klasse wird ausgeführt, abhängig davon, ob der Client verwaltet oder unverwaltet ist. Siehe unten für Details.

**name** : Name, der in der Konsole angezeigt werden soll.

**args** : Argumente für die Hauptklasse, getrennt durch Leerzeichen oder Tabulatoren. Argumente, die Leerzeichen oder Tabulatoren enthalten, können mit `'` oder `"` in Anführungszeichen gesetzt werden

**delay** : Sekunden vor dem Start, Standard 120

**onBoot** : `{true|false}` : Standard false, erzwingt eine Verzögerung von 0, überschreibt die Verzögerungseinstellung

**startOnLoad** : `{true|false}` : Soll der Client überhaupt ausgeführt werden? Standard true

Die folgenden zusätzlichen Eigenschaften werden nur von Plugins verwendet:

**stopargs** : Argumente zum Stoppen des Clients.

**uninstallargs** : Argumente zum Deinstallieren des Clients.

**classpath** : Zusätzliche classpath-Elemente für den Client, getrennt durch Kommas.

Die folgenden Ersetzungen werden in den args-, stopargs-, uninstallargs- und classpath-Zeilen nur für Plugins vorgenommen:

**$I2P** : Das Basis-I2P-Installationsverzeichnis

**$CONFIG** : Das Konfigurationsverzeichnis des Benutzers (z.B. ~/.i2p)

**$PLUGIN** : Das Verzeichnis dieses Plugins (z.B. ~/.i2p/plugins/foo)

**$OS** : Der Name des Betriebssystems (z.B. "linux")

**$ARCH** : Der Architekturname (z.B. "amd64")

Alle Eigenschaften außer "main" sind optional. Zeilen, die mit `#` beginnen, sind Kommentare.

Wenn die Verzögerung weniger als null beträgt, wartet der Client, bis der Router den RUNNING-Status erreicht, und startet dann sofort in einem neuen Thread.

Wenn die Verzögerung gleich null ist, wird der Client sofort im selben Thread ausgeführt, sodass Ausnahmen an die Konsole weitergegeben werden können. In diesem Fall sollte der Client entweder eine Ausnahme werfen, schnell zurückkehren oder seinen eigenen Thread erzeugen.

Wenn die Verzögerung größer als null ist, wird es in einem neuen Thread ausgeführt, und Ausnahmen werden protokolliert, aber nicht an die Konsole weitergegeben.

Clients können "verwaltet" oder "unverwaltet" sein.

### Logger (logger.config)

Konfiguriert über /configlogging in der router-Konsole.

Die Eigenschaften sind wie folgt:

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
### Individuelles Plugin (plugins/*/plugin.config)

Siehe die [Plugin-Spezifikation](/docs/specs/plugin). Beachten Sie, dass Plugins auch clients.config-, i2ptunnel.config- und webapps.config-Dateien enthalten können.

### Plugins (plugins.config)

Aktivieren/Deaktivieren für jedes installierte Plugin.

Die Eigenschaften sind wie folgt:

```
plugin.{name}.startOnLoad=true|false
```
### Webapps (webapps.config)

Für jede installierte Webapp aktivieren/deaktivieren.

Die Eigenschaften sind wie folgt:

```
webapps.{name}.classpath=[space- or comma-separated paths]
webapps.{name}.startOnLoad=true|false
```
### Router (router.config)

Konfiguriert über /configadvanced in der router-Konsole.

## Anwendungen

### Adressbuch (addressbook/config.txt)

Siehe Dokumentation in SusiDNS.

### I2PSnark (i2psnark.config.d/i2psnark.config)

Konfiguriert über die Anwendungs-GUI.

### Individuelle i2psnark (i2psnark.config.d/*/*.config)

Die Konfiguration für einen einzelnen Torrent. Wird über die Anwendungs-GUI konfiguriert.

### I2PTunnel (i2ptunnel.config)

Konfiguriert über die /i2ptunnel Anwendung in der Router-Konsole. Ab Release 0.9.42 wird die Standard-i2ptunnel.config-Datei in einzelne Konfigurationsdateien für jeden tunnel im i2ptunnel.config.d-Verzeichnis aufgeteilt. Nach der Aufteilung sind die Eigenschaften in den einzelnen Dateien NICHT mit "tunnel.N." vorangestellt.

Hinweis: "tunnel.N.option.i2cp.*" Optionen, die als I2CP-Optionen erscheinen mögen, sind in i2ptunnel implementiert und werden NICHT über andere Schnittstellen oder APIs wie I2CP oder SAM unterstützt.

Die Eigenschaften sind wie folgt:

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
Hinweis: Jedes 'N' ist eine Tunnelnummer, die bei 0 beginnt. Es darf keine Lücken in der Nummerierung geben.

### Router-Konsole

Die Router-Konsole verwendet die router.config-Datei.

### SusiMail (susimail.config)

Siehe Beitrag auf zzz.i2p.

## Referenzen

- [DATAHELPER](http://docs.i2p-projekt.de/net/i2p/data/DataHelper.html)
- [Zuordnung](/docs/specs/common-structures#type-mapping)
- [PLUGIN](/docs/specs/plugin)
- [Properties](http://docs.oracle.com/javase/1.5.0/docs/api/java/util/Properties.html#load%28java.io.InputStream%29)
