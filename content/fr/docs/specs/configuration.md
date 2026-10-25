---
title: "Spécification du fichier de configuration"
description: "Spécification des fichiers de configuration I2P utilisés par le router et les applications"
slug: "configuration"
aliases:
  - "/fr/configuration"
  - "/fr/configuration/"
category: "Formats"
lastUpdated: "2023-01"
accurateFor: "0.9.57"
---

## Aperçu général

Cette page fournit une spécification générale des fichiers de configuration I2P, utilisés par le router et diverses applications. Elle donne également un aperçu des informations contenues dans les différents fichiers, et des liens vers la documentation détaillée lorsqu'elle est disponible.

## Format général

Un fichier de configuration I2P est formaté selon les spécifications des [Properties](http://docs.oracle.com/javase/1.5.0/docs/api/java/util/Properties.html#load%28java.io.InputStream%29) Java avec les exceptions suivantes :

- L'encodage doit être UTF-8
- N'utilise ni ne reconnaît aucune séquence d'échappement, y compris `\`, donc les lignes ne peuvent pas être continuées
- `#` ou `;` démarre un commentaire, mais `!` ne le fait pas
- `#` démarre un commentaire à n'importe quelle position mais `;` doit être en colonne 1 pour démarrer un commentaire
- Les espaces en début et fin de ligne ne sont pas supprimés pour les clés
- Les espaces en début et fin de ligne sont supprimés pour les valeurs
- `=` est le seul caractère de terminaison de clé (pas `:` ou les espaces)
- Les lignes sans `=` sont ignorées. À partir de la version 0.9.10, les clés avec une valeur de "" sont supportées.
- Comme il n'y a pas de séquences d'échappement, les clés ne peuvent pas contenir `#`, `=`, ou `\n`, ou commencer par `;`
- Comme il n'y a pas de séquences d'échappement, les valeurs ne peuvent pas contenir `#` ou `\n`, ou commencer ou finir par `\r` ou des espaces

Le fichier n'a pas besoin d'être trié, mais la plupart des applications trient par clé lors de l'écriture dans le fichier, pour faciliter la lecture et l'édition manuelle.

Les opérations de lecture et d'écriture sont implémentées dans DataHelper loadProps() et storeProps() [DATAHELPER](http://docs.i2p-projekt.de/net/i2p/data/DataHelper.html). Notez que le format de fichier est significativement différent du format sérialisé pour les protocoles I2P spécifié dans [Mapping](/docs/specs/common-structures/#type-mapping).

## Bibliothèque centrale et router

### Clients (clients.config)

Configuré via /configclients dans la console du router. À partir de la version 0.9.42, le fichier clients.config par défaut est divisé en fichiers de configuration individuels pour chaque client dans le répertoire clients.config.d. Après division, les propriétés dans les fichiers individuels sont préfixées par "clientApp.0.".

Le format est le suivant :

Les lignes sont de la forme `clientApp.x.prop=val`, où x est le numéro de l'application. Les numéros d'application DOIVENT commencer par 0 et être consécutifs.

Les propriétés sont les suivantes :

**main** : Nom complet de la classe. Requis. : Le constructeur ou la méthode main() de cette classe sera exécuté, selon que le client soit géré ou non géré. Voir ci-dessous pour plus de détails.

**name** : Nom à afficher sur la console.

**args** : Arguments de la classe principale, séparés par des espaces ou des tabulations. Les arguments contenant des espaces ou des tabulations peuvent être mis entre guillemets avec `'` ou `"`

**delay** : Secondes avant le démarrage, par défaut 120

**onBoot** : `{true|false}` : Par défaut false, force un délai de 0, remplace le paramètre de délai

**startOnLoad** : `{true|false}` : Le client doit-il être exécuté ? Par défaut true

Les propriétés supplémentaires suivantes sont utilisées uniquement par les plugins :

**stopargs** : Arguments pour arrêter le client.

**uninstallargs** : Arguments pour désinstaller le client.

**classpath** : Éléments de classpath supplémentaires pour le client, séparés par des virgules.

Les substitutions suivantes sont effectuées dans les lignes args, stopargs, uninstallargs et classpath, pour les plugins uniquement :

**$I2P** : Le répertoire d'installation de base d'I2P

**$CONFIG** : Le répertoire de configuration de l'utilisateur (par exemple ~/.i2p)

**$PLUGIN** : Le répertoire de ce plugin (par exemple ~/.i2p/plugins/foo)

**$OS** : Le nom du système d'exploitation (par exemple "linux")

**$ARCH** : Le nom de l'architecture (par exemple "amd64")

Toutes les propriétés sauf "main" sont optionnelles. Les lignes commençant par `#` sont des commentaires.

Si le délai est inférieur à zéro, le client attendra que le router atteigne l'état RUNNING puis démarrera immédiatement dans un nouveau thread.

Si le délai est égal à zéro, le client est exécuté immédiatement, dans le même thread, afin que les exceptions puissent être propagées vers la console. Dans ce cas, le client doit soit lever une exception, retourner rapidement, ou créer son propre thread.

Si le délai est supérieur à zéro, il sera exécuté dans un nouveau thread, et les exceptions seront enregistrées mais ne seront pas propagées vers la console.

Les clients peuvent être "gérés" ou "non gérés".

### Logger (logger.config)

Configuré via /configlogging dans la console du router.

Les propriétés sont les suivantes :

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
### Plugin Individuel (plugins/*/plugin.config)

Voir la [spécification des plugins](/docs/specs/plugin). Notez que les plugins peuvent également contenir des fichiers clients.config, i2ptunnel.config et webapps.config.

### Plugins (plugins.config)

Activer/désactiver pour chaque plugin installé.

Les propriétés sont les suivantes :

```
plugin.{name}.startOnLoad=true|false
```
### Applications web (webapps.config)

Activer/désactiver pour chaque webapp installée.

Les propriétés sont les suivantes :

```
webapps.{name}.classpath=[space- or comma-separated paths]
webapps.{name}.startOnLoad=true|false
```
### Router (router.config)

Configuré via /configadvanced dans la console du router.

## Applications

### Carnet d'adresses (addressbook/config.txt)

Voir la documentation dans SusiDNS.

### I2PSnark (i2psnark.config.d/i2psnark.config)

Configuré via l'interface graphique de l'application.

### i2psnark individuel (i2psnark.config.d/*/*.config)

La configuration pour un torrent individuel. Configurée via l'interface graphique de l'application.

### I2PTunnel (i2ptunnel.config)

Configuré via l'application /i2ptunnel dans la console du router. À partir de la version 0.9.42, le fichier i2ptunnel.config par défaut est divisé en fichiers de configuration individuels pour chaque tunnel dans le répertoire i2ptunnel.config.d. Après la division, les propriétés dans les fichiers individuels ne sont PAS préfixées par "tunnel.N.".

Note : Les options "tunnel.N.option.i2cp.*", bien qu'elles semblent être des options I2CP, sont implémentées dans i2ptunnel, et ne sont PAS prises en charge via d'autres interfaces ou API telles que I2CP ou SAM.

Les propriétés sont les suivantes :

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
Note : Chaque 'N' est un numéro de tunnel commençant par 0. Il ne doit pas y avoir d'espaces dans la numérotation.

### Console du Router

La console du router utilise le fichier router.config.

### SusiMail (susimail.config)

Voir le message sur zzz.i2p.

## Références

- [DATAHELPER](http://docs.i2p-projekt.de/net/i2p/data/DataHelper.html)
- [Correspondance](/docs/specs/common-structures#type-mapping)
- [PLUGIN](/docs/specs/plugin)
- [Properties](http://docs.oracle.com/javase/1.5.0/docs/api/java/util/Properties.html#load%28java.io.InputStream%29)
