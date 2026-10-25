---
title: "Especificación del Archivo de Configuración"
description: "Especificación de los archivos de configuración de I2P utilizados por el router y las aplicaciones"
slug: "configuration"
aliases:
  - "/es/configuration"
  - "/es/configuration/"
category: "Formatos"
lastUpdated: "2023-01"
accurateFor: "0.9.57"
---

## Resumen

Esta página proporciona una especificación general de los archivos de configuración de I2P, utilizados por el router y varias aplicaciones. También ofrece una visión general de la información contenida en los diversos archivos, y enlaces a documentación detallada cuando esté disponible.

## Formato General

Un archivo de configuración de I2P está formateado como se especifica en Java [Properties](http://docs.oracle.com/javase/1.5.0/docs/api/java/util/Properties.html#load%28java.io.InputStream%29) con las siguientes excepciones:

- La codificación debe ser UTF-8
- No utiliza ni reconoce ningún escape, incluyendo `\`, por lo que las líneas no pueden continuarse
- `#` o `;` inicia un comentario, pero `!` no lo hace
- `#` inicia un comentario en cualquier posición pero `;` debe estar en la columna 1 para iniciar un comentario
- Los espacios en blanco al inicio y al final no se eliminan en las claves
- Los espacios en blanco al inicio y al final se eliminan en los valores
- `=` es el único carácter de terminación de clave (no `:` o espacios en blanco)
- Las líneas sin `=` se ignoran. A partir de la versión 0.9.10, se admiten claves con un valor de ""
- Como no hay escapes, las claves no pueden contener `#`, `=`, o `\n`, o empezar con `;`
- Como no hay escapes, los valores no pueden contener `#` o `\n`, o empezar o terminar con `\r` o espacios en blanco

El archivo no necesita estar ordenado, pero la mayoría de aplicaciones ordenan por clave al escribir al archivo, para facilitar la lectura y edición manual.

Las operaciones de lectura y escritura están implementadas en DataHelper loadProps() y storeProps() [DATAHELPER](http://docs.i2p-projekt.de/net/i2p/data/DataHelper.html). Ten en cuenta que el formato de archivo es significativamente diferente al formato serializado para protocolos I2P especificado en [Mapping](/docs/specs/common-structures/#type-mapping).

## Biblioteca principal y router

### Clientes (clients.config)

Configurado a través de /configclients en la consola del router. A partir de la versión 0.9.42, el archivo clients.config predeterminado se divide en archivos de configuración individuales para cada cliente en el directorio clients.config.d. Después de ser dividido, las propiedades en los archivos individuales tienen el prefijo "clientApp.0.".

El formato es el siguiente:

Las líneas tienen la forma `clientApp.x.prop=val`, donde x es el número de aplicación. Los números de aplicación DEBEN comenzar con 0 y ser consecutivos.

Las propiedades son las siguientes:

**main** : Nombre completo de la clase. Requerido. : El constructor o método main() en esta clase será ejecutado, dependiendo de si el cliente es gestionado o no gestionado. Ver detalles a continuación.

**name** : Nombre que se mostrará en la consola.

**args** : Argumentos para la clase principal, separados por espacios o tabulaciones. Los argumentos que contengan espacios o tabulaciones pueden ir entre comillas con `'` o `"`

**delay** : Segundos antes de iniciar, predeterminado 120

**onBoot** : `{true|false}` : Por defecto false, fuerza un retraso de 0, anula la configuración de retraso

**startOnLoad** : `{true|false}` : ¿Debe ejecutarse el cliente? Por defecto true

Las siguientes propiedades adicionales son utilizadas únicamente por plugins:

**stopargs** : Argumentos para detener el cliente.

**uninstallargs** : Argumentos para desinstalar el cliente.

**classpath** : Elementos adicionales del classpath para el cliente, separados por comas.

Las siguientes sustituciones se realizan en las líneas args, stopargs, uninstallargs y classpath, solo para plugins:

**$I2P** : El directorio base de instalación de I2P

**$CONFIG** : El directorio de configuración del usuario (ej. ~/.i2p)

**$PLUGIN** : Directorio de este plugin (ej. ~/.i2p/plugins/foo)

**$OS** : El nombre del sistema operativo (ej. "linux")

**$ARCH** : El nombre de la arquitectura (ej. "amd64")

Todas las propiedades excepto "main" son opcionales. Las líneas que comienzan con `#` son comentarios.

Si el retraso es menor que cero, el cliente esperará hasta que el router alcance el estado RUNNING y luego iniciará inmediatamente en un nuevo hilo.

Si el retraso es igual a cero, el cliente se ejecuta inmediatamente, en el mismo hilo, para que las excepciones puedan propagarse a la consola. En este caso, el cliente debería lanzar una excepción, regresar rápidamente, o generar su propio hilo.

Si el retraso es mayor que cero, se ejecutará en un hilo nuevo, y las excepciones se registrarán en el log pero no se propagarán a la consola.

Los clientes pueden ser "administrados" o "no administrados".

### Logger (logger.config)

Configurado a través de /configlogging en la consola del router.

Las propiedades son las siguientes:

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
### Plugin Individual (plugins/*/plugin.config)

Ver la [especificación de plugins](/docs/specs/plugin). Ten en cuenta que los plugins también pueden contener archivos clients.config, i2ptunnel.config y webapps.config.

### Plugins (plugins.config)

Habilitar/deshabilitar para cada plugin instalado.

Las propiedades son las siguientes:

```
plugin.{name}.startOnLoad=true|false
```
### Aplicaciones web (webapps.config)

Habilitar/deshabilitar para cada webapp instalada.

Las propiedades son las siguientes:

```
webapps.{name}.classpath=[space- or comma-separated paths]
webapps.{name}.startOnLoad=true|false
```
### Router (router.config)

Configurado a través de /configadvanced en la consola del router.

## Aplicaciones

### Libreta de direcciones (addressbook/config.txt)

Ver documentación en SusiDNS.

### I2PSnark (i2psnark.config.d/i2psnark.config)

Configurado a través de la interfaz gráfica de la aplicación.

### Individual i2psnark (i2psnark.config.d/*/*.config)

La configuración para un torrent individual. Se configura a través de la interfaz gráfica de la aplicación.

### I2PTunnel (i2ptunnel.config)

Configurado a través de la aplicación /i2ptunnel en la consola del router. A partir de la versión 0.9.42, el archivo i2ptunnel.config predeterminado se divide en archivos de configuración individuales para cada tunnel en el directorio i2ptunnel.config.d. Después de ser divididos, las propiedades en los archivos individuales NO tienen el prefijo "tunnel.N.".

Nota: Las opciones "tunnel.N.option.i2cp.*", aunque parezcan ser opciones de I2CP, están implementadas en i2ptunnel, y NO son compatibles a través de otras interfaces o APIs como I2CP o SAM.

Las propiedades son las siguientes:

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
Nota: Cada 'N' es un número de túnel que comienza con 0. No puede haber espacios en la numeración.

### Consola del Router

La consola del router utiliza el archivo router.config.

### SusiMail (susimail.config)

Ver publicación en zzz.i2p.

## Referencias

- [DATAHELPER](http://docs.i2p-projekt.de/net/i2p/data/DataHelper.html)
- [Mapeo](/docs/specs/common-structures#type-mapping)
- [PLUGIN](/docs/specs/plugin)
- [Properties](http://docs.oracle.com/javase/1.5.0/docs/api/java/util/Properties.html#load%28java.io.InputStream%29)
