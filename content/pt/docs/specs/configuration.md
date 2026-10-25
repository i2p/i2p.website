---
title: "Especificação do Arquivo de Configuração"
description: "Especificação dos arquivos de configuração I2P utilizados pelo router e aplicações"
slug: "configuration"
aliases:
  - "/pt/configuration"
  - "/pt/configuration/"
category: "Formatos"
lastUpdated: "2023-01"
accurateFor: "0.9.57"
---

## Visão Geral

Esta página fornece uma especificação geral dos arquivos de configuração do I2P, usados pelo router e várias aplicações. Também oferece uma visão geral das informações contidas nos diversos arquivos e links para documentação detalhada quando disponível.

## Formato Geral

Um arquivo de configuração I2P é formatado conforme especificado nas [Properties](http://docs.oracle.com/javase/1.5.0/docs/api/java/util/Properties.html#load%28java.io.InputStream%29) do Java com as seguintes exceções:

- A codificação deve ser UTF-8
- Não usa ou reconhece escapes, incluindo `\`, então as linhas não podem ser continuadas
- `#` ou `;` inicia um comentário, mas `!` não
- `#` inicia um comentário em qualquer posição, mas `;` deve estar na coluna 1 para iniciar um comentário
- Espaços em branco iniciais e finais não são removidos das chaves
- Espaços em branco iniciais e finais são removidos dos valores
- `=` é o único caractere de terminação de chave (não `:` ou espaços em branco)
- Linhas sem `=` são ignoradas. A partir da versão 0.9.10, chaves com valor "" são suportadas.
- Como não há escapes, as chaves não podem conter `#`, `=`, ou `\n`, ou começar com `;`
- Como não há escapes, os valores não podem conter `#` ou `\n`, ou começar ou terminar com `\r` ou espaços em branco

O arquivo não precisa estar ordenado, mas a maioria das aplicações ordena por chave ao escrever no arquivo, para facilitar a leitura e edição manual.

Leituras e escritas são implementadas em DataHelper loadProps() e storeProps() [DATAHELPER](http://docs.i2p-projekt.de/net/i2p/data/DataHelper.html). Note que o formato do arquivo é significativamente diferente do formato serializado para protocolos I2P especificado em [Mapping](/docs/specs/common-structures/#type-mapping).

## Biblioteca principal e router

### Clientes (clients.config)

Configurado via /configclients no console do router. A partir da versão 0.9.42, o arquivo clients.config padrão é dividido em arquivos de configuração individuais para cada cliente no diretório clients.config.d. Após ser dividido, as propriedades nos arquivos individuais são prefixadas com "clientApp.0.".

O formato é o seguinte:

As linhas são da forma `clientApp.x.prop=val`, onde x é o número da aplicação. Os números das aplicações DEVEM começar com 0 e ser consecutivos.

As propriedades são as seguintes:

**main** : Nome completo da classe. Obrigatório. : O construtor ou método main() nesta classe será executado, dependendo se o cliente é gerenciado ou não gerenciado. Veja os detalhes abaixo.

**name** : Nome a ser exibido no console.

**args** : Argumentos para a classe principal, separados por espaços ou tabulações. Argumentos que contenham espaços ou tabulações podem ser citados com `'` ou `"`

**delay** : Segundos antes de iniciar, padrão 120

**onBoot** : `{true|false}` : Padrão false, força um atraso de 0, substitui a configuração de atraso

**startOnLoad** : `{true|false}` : O cliente deve ser executado? Padrão true

As seguintes propriedades adicionais são usadas apenas por plugins:

**stopargs** : Argumentos para parar o cliente.

**uninstallargs** : Argumentos para desinstalar o cliente.

**classpath** : Elementos adicionais do classpath para o cliente, separados por vírgulas.

As seguintes substituições são feitas nas linhas args, stopargs, uninstallargs e classpath, apenas para plugins:

**$I2P** : O diretório base de instalação do I2P

**$CONFIG** : O diretório de configuração do usuário (ex: ~/.i2p)

**$PLUGIN** : Diretório deste plugin (ex.: ~/.i2p/plugins/foo)

**$OS** : O nome do sistema operacional (ex: "linux")

**$ARCH** : O nome da arquitetura (ex: "amd64")

Todas as propriedades exceto "main" são opcionais. Linhas que começam com `#` são comentários.

Se o atraso for menor que zero, o cliente aguardará até que o router atinja o estado RUNNING e então iniciará imediatamente em uma nova thread.

Se o atraso for igual a zero, o cliente é executado imediatamente, na mesma thread, para que as exceções possam ser propagadas para o console. Neste caso, o cliente deve ou lançar uma exceção, retornar rapidamente, ou criar sua própria thread.

Se o atraso for maior que zero, será executado em uma nova thread, e as exceções serão registradas em log mas não propagadas para o console.

Os clientes podem ser "gerenciados" ou "não gerenciados".

### Logger (logger.config)

Configurado via /configlogging no console do router.

As propriedades são as seguintes:

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

Consulte a [especificação de plugin](/docs/specs/plugin). Note que os plugins também podem conter arquivos clients.config, i2ptunnel.config e webapps.config.

### Plugins (plugins.config)

Habilitar/desabilitar para cada plugin instalado.

As propriedades são as seguintes:

```
plugin.{name}.startOnLoad=true|false
```
### Aplicações Web (webapps.config)

Habilitar/desabilitar para cada webapp instalada.

As propriedades são as seguintes:

```
webapps.{name}.classpath=[space- or comma-separated paths]
webapps.{name}.startOnLoad=true|false
```
### Router (router.config)

Configurado via /configadvanced no console do router.

## Aplicações

### Catálogo de Endereços (addressbook/config.txt)

Consulte a documentação no SusiDNS.

### I2PSnark (i2psnark.config.d/i2psnark.config)

Configurado através da interface gráfica da aplicação.

### Individual i2psnark (i2psnark.config.d/*/*.config)

A configuração para um torrent individual. Configurada através da interface gráfica da aplicação.

### I2PTunnel (i2ptunnel.config)

Configurado através da aplicação /i2ptunnel no console do router. A partir da versão 0.9.42, o arquivo padrão i2ptunnel.config é dividido em arquivos de configuração individuais para cada tunnel no diretório i2ptunnel.config.d. Após serem divididas, as propriedades nos arquivos individuais NÃO são prefixadas com "tunnel.N.".

Nota: As opções "tunnel.N.option.i2cp.*", embora pareçam ser opções I2CP, são implementadas no i2ptunnel, e NÃO são suportadas através de outras interfaces ou APIs como I2CP ou SAM.

As propriedades são as seguintes:

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
Nota: Cada 'N' é um número de tunnel começando com 0. Pode não haver lacunas na numeração.

### Console do Router

O console do router usa o arquivo router.config.

### SusiMail (susimail.config)

Veja a postagem em zzz.i2p.

## Referências

- [DATAHELPER](http://docs.i2p-projekt.de/net/i2p/data/DataHelper.html)
- [Mapeamento](/docs/specs/common-structures#type-mapping)
- [PLUGIN](/docs/specs/plugin)
- [Properties](http://docs.oracle.com/javase/1.5.0/docs/api/java/util/Properties.html#load%28java.io.InputStream%29)
