---
title: "Configuração do Router"
description: "Opções de configuração e formatos para routers e clientes do I2P"
slug: "configuration"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## Visão geral

Este documento fornece uma especificação técnica abrangente dos arquivos de configuração do I2P usados pelo router e por várias aplicações. Abrange especificações de formato de arquivo, definições de propriedades e detalhes de implementação validados em relação ao código-fonte do I2P e à documentação oficial.

### Escopo

- Arquivos e formatos de configuração do router
- Configurações de aplicativos cliente
- Configurações de tunnel do I2PTunnel
- Especificações do formato de arquivo e implementação
- Funcionalidades específicas de versão e descontinuações

### Notas de Implementação

Os arquivos de configuração são lidos e escritos usando os métodos `DataHelper.loadProps()` e `storeProps()` na biblioteca principal do I2P. O formato do arquivo difere significativamente do formato serializado usado nos protocolos do I2P (consulte [Especificação de Estruturas Comuns - Mapeamento de Tipos](/docs/specs/common-structures/#type-mapping)).

---

## Formato geral do arquivo de configuração

Os arquivos de configuração do I2P seguem um formato Java Properties modificado, com exceções e restrições específicas.

### Especificação do Formato

Baseado em [Java Properties](http://docs.oracle.com/javase/1.5.0/docs/api/java/util/Properties.html#load%28java.io.InputStream%29) com as seguintes diferenças críticas:

#### Codificação

- **DEVE** usar codificação UTF-8 (NÃO ISO-8859-1, como no Java Properties (propriedades do Java) padrão)
- Implementação: Usa os utilitários `DataHelper.getUTF8()` para todas as operações de arquivo

#### Sequências de escape

- **NÃO** são reconhecidas sequências de escape (incluindo a barra invertida `\`)
- A continuação de linha **NÃO** é suportada
- Caracteres de barra invertida são tratados como literais

#### Caracteres de comentário

- `#` inicia um comentário em qualquer posição na linha
- `;` inicia um comentário **somente** quando estiver na coluna 1
- `!` **NÃO** inicia um comentário (diferente de Java Properties)

#### Separadores de chave-valor

- `=` é o **ÚNICO** separador válido de chave-valor
- `:` **NÃO** é reconhecido como separador
- Espaços em branco **NÃO** são reconhecidos como separador

#### Tratamento de espaços em branco

- Espaços em branco no início e no fim **NÃO** são removidos nas chaves
- Espaços em branco no início e no fim **SÃO** removidos nos valores

#### Processamento de linhas

- Linhas sem `=` são ignoradas (tratadas como comentários ou linhas em branco)
- Valores vazios (`key=`) são suportados a partir da versão 0.9.10
- Chaves com valores vazios são armazenadas e recuperadas normalmente

#### Restrições de caracteres

**As chaves NÃO podem conter**: - `#` (sinal de cerquilha/jogo da velha) - `=` (sinal de igual) - `\n` (caractere de nova linha) - Não podem começar com `;` (ponto e vírgula)

**Valores NÃO podem conter**: - `#` (hash/sinal de número) - `\n` (caractere de nova linha) - Não pode começar nem terminar com `\r` (retorno de carro) - Não pode começar nem terminar com espaços em branco (removidos automaticamente)

### Ordenação de arquivos

Os arquivos de configuração não precisam ser ordenados por chave. No entanto, a maioria dos aplicativos I2P ordena as chaves alfabeticamente ao escrever arquivos de configuração para facilitar: - Edição manual - Operações de diff de controle de versão - Legibilidade humana

### Detalhes de Implementação

#### Leitura de arquivos de configuração

```java
// Method signature from net.i2p.data.DataHelper
public static Properties loadProps(File file)
```
**Comportamento**: - Lê arquivos codificados em UTF-8 - Aplica todas as regras de formato descritas acima - Valida as restrições de caracteres - Retorna um objeto Properties vazio se o arquivo não existir - Lança `IOException` em caso de erros de leitura

#### Escrevendo arquivos de configuração

```java
// Method signature from net.i2p.data.DataHelper
public static void storeProps(Properties props, File file)
```
**Comportamento**: - Escreve arquivos codificados em UTF-8 - Ordena as chaves alfabeticamente (a menos que OrderedProperties seja usado) - Define as permissões do arquivo para o modo 600 (apenas leitura/gravação do usuário) a partir da versão 0.8.1 - Lança `IllegalArgumentException` para caracteres inválidos em chaves ou valores - Lança `IOException` em caso de erros de escrita

#### Validação de formato

A implementação realiza validação rigorosa: - Chaves e valores são verificados quanto a caracteres proibidos - Entradas inválidas causam exceções durante operações de escrita - A leitura ignora silenciosamente linhas malformadas (linhas sem `=`)

### Exemplos de Formato

#### Arquivo de configuração válido

```properties
# This is a comment
; This is also a comment (column 1 only)
key.with.dots=value with spaces
another_key=value=with=equals
empty.value=
numeric.value=12345
unicode.value=こんにちは
```
#### Exemplos de Configuração Inválida

```properties
# INVALID: Key contains equals sign
invalid=key=value

# INVALID: Key contains hash
invalid#key=value

# INVALID: Value contains newline (implicit)
key=value
continues here

# INVALID: Semicolon comment not in column 1 (treated as key)
 ; not.a.comment=value
```
---

## Biblioteca principal e configuração do router

### Configuração de clientes (clients.config)

**Localização**: `$I2P_CONFIG_DIR/clients.config` (legado) ou `$I2P_CONFIG_DIR/clients.config.d/` (moderno)   **Interface de configuração**: Console do Router em `/configclients`   **Alteração de formato**: Versão 0.9.42 (agosto de 2019)

#### Estrutura de diretórios (Versão 0.9.42+)

A partir da versão 0.9.42, o arquivo clients.config padrão é dividido automaticamente em arquivos de configuração individuais:

```
$I2P_CONFIG_DIR/
├── clients.config.d/
│   ├── 00-webConsole.config
│   ├── 01-i2ptunnel.config
│   ├── 02-i2psnark.config
│   ├── 03-susidns.config
│   └── ...
└── clients.config (legacy, auto-migrated)
```
**Comportamento de migração**: - Na primeira execução após a atualização para 0.9.42+, o arquivo monolítico é dividido automaticamente - As propriedades nos arquivos divididos são prefixadas com `clientApp.0.` - O formato legado ainda é suportado para compatibilidade com versões anteriores - O formato dividido permite empacotamento modular e gerenciamento de plugins

#### Formato da propriedade

As linhas têm a forma `clientApp.x.prop=val`, em que `x` é o número do aplicativo.

**Requisitos de numeração de aplicativos**: - DEVE começar com 0 - DEVE ser consecutiva (sem intervalos) - A ordem determina a sequência de inicialização

#### Propriedades Obrigatórias

##### principal

- **Tipo**: String (nome totalmente qualificado da classe)
- **Obrigatório**: Sim
- **Descrição**: O construtor ou o método `main()` desta classe será invocado dependendo do tipo de cliente (gerenciado vs. não gerenciado)
- **Exemplo**: `clientApp.0.main=net.i2p.router.web.RouterConsoleRunner`

#### Propriedades opcionais

##### nome

- **Tipo**: String
- **Obrigatório**: Não
- **Descrição**: Nome exibido na console do router
- **Exemplo**: `clientApp.0.name=Router Console`

##### argumentos

- **Tipo**: String (separada por espaço ou tabulação)
- **Obrigatório**: Não
- **Descrição**: Argumentos passados ao construtor da classe principal ou ao método main()
- **Aspas**: Argumentos que contêm espaços ou tabulações podem ser colocados entre aspas com `'` ou `"`
- **Exemplo**: `clientApp.0.args=-d $CONFIG/eepsite`

##### atraso

- **Tipo**: Inteiro (segundos)
- **Obrigatório**: Não
- **Padrão**: 120
- **Descrição**: Segundos a esperar antes de iniciar o cliente
- **Substituições**: Substituído por `onBoot=true` (define o atraso como 0)
- **Valores especiais**:
  - `< 0`: Aguarda o router chegar ao estado RUNNING e então inicia imediatamente em nova thread
  - `= 0`: Executa imediatamente na mesma thread (exceções se propagam para o console)
  - `> 0`: Inicia após o atraso em nova thread (exceções registradas, não propagadas)

##### onBoot

- **Tipo**: Booleano
- **Obrigatório**: Não
- **Padrão**: false
- **Descrição**: Força atraso de 0, sobrepõe a configuração explícita de atraso
- **Caso de uso**: Iniciar serviços críticos imediatamente na inicialização do router

##### startOnLoad

- **Tipo**: Booleano
- **Obrigatório**: Não
- **Padrão**: true
- **Descrição**: Se o cliente deve ser iniciado
- **Caso de uso**: Desativar clientes sem remover a configuração

#### Propriedades Específicas do Plugin

Estas propriedades são usadas apenas por plugins (não por clientes do núcleo):

##### stopargs

- **Tipo**: String (separada por espaço ou tabulação)
- **Descrição**: Argumentos passados para encerrar o cliente
- **Substituição de variáveis**: Sim (veja abaixo)

##### uninstallargs

- **Tipo**: String (separada por espaços ou tabulações)
- **Descrição**: Argumentos passados para desinstalar o cliente
- **Substituição de variáveis**: Sim (consulte abaixo)

##### classpath (caminho de classes)

- **Tipo**: String (caminhos separados por vírgula)
- **Descrição**: Elementos adicionais no classpath do cliente
- **Substituição de variáveis**: Sim (veja abaixo)

#### Substituição de variáveis (apenas para plugins)

As seguintes variáveis são substituídas em `args`, `stopargs`, `uninstallargs` e `classpath` para plugins:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Variable</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Expands To</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Example</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$I2P</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Base I2P installation directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>/usr/share/i2p</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$CONFIG</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">User configuration directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>~/.i2p</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$PLUGIN</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Plugin directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>~/.i2p/plugins/foo</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$OS</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Operating system name</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>linux</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$ARCH</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Architecture name</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>amd64</code></td>
    </tr>
  </tbody>
</table>
**Nota**: A substituição de variáveis é realizada apenas para plugins, não para clientes do núcleo.

#### Tipos de clientes

##### Clientes gerenciados

- O construtor é chamado com os parâmetros `RouterContext` e `ClientAppManager`
- O cliente deve implementar a interface `ClientApp`
- Ciclo de vida controlado pelo router
- Pode ser iniciado, parado e reiniciado dinamicamente

##### Clientes não gerenciados

- O método `main(String[] args)` é chamado
- Executa em thread (linha de execução) separada
- Ciclo de vida não gerenciado pelo router
- Tipo de cliente legado

#### Exemplo de Configuração

```properties
# Router Console (core client)
clientApp.0.main=net.i2p.router.web.RouterConsoleRunner
clientApp.0.name=Router Console
clientApp.0.args=-d $CONFIG/eepsite
clientApp.0.delay=0
clientApp.0.onBoot=true
clientApp.0.startOnLoad=true

# I2PTunnel (core client)
clientApp.1.main=net.i2p.i2ptunnel.TunnelControllerGroup
clientApp.1.name=I2PTunnel
clientApp.1.args=
clientApp.1.delay=120
clientApp.1.startOnLoad=true

# Plugin Example
clientApp.2.main=org.example.plugin.PluginMain
clientApp.2.name=Example Plugin
clientApp.2.args=-config $PLUGIN/config.properties
clientApp.2.stopargs=-shutdown
clientApp.2.uninstallargs=-remove $PLUGIN
clientApp.2.classpath=$PLUGIN/lib/plugin.jar,$PLUGIN/lib/dep.jar
clientApp.2.delay=240
clientApp.2.startOnLoad=true
```
---

### Configuração do Logger (logger.config)

**Localização**: `$I2P_CONFIG_DIR/logger.config`   **Interface de configuração**: console do router em `/configlogging`

#### Referência de Propriedades

##### Configuração do buffer do console

###### logger.consoleBufferSize

- **Tipo**: Inteiro
- **Padrão**: 20
- **Descrição**: Número máximo de mensagens de log a serem armazenadas em buffer no console
- **Intervalo**: 1-1000 recomendado

##### Formatação de data e hora

###### logger.dateFormat

- **Tipo**: String (padrão do SimpleDateFormat)
- **Padrão**: Da localidade do sistema
- **Exemplo**: `HH:mm:ss.SSS`
- **Documentação**: [Java SimpleDateFormat](https://docs.oracle.com/javase/8/docs/api/java/text/SimpleDateFormat.html)

##### Níveis de Log

###### logger.defaultLevel

- **Tipo**: Enum
- **Padrão**: ERROR
- **Valores**: `CRIT`, `ERROR`, `WARN`, `INFO`, `DEBUG`
- **Descrição**: Nível de log padrão para todas as classes

###### logger.minimumOnScreenLevel

- **Tipo**: Enumeração
- **Padrão**: CRIT
- **Valores**: `CRIT`, `ERROR`, `WARN`, `INFO`, `DEBUG`
- **Descrição**: Nível mínimo para mensagens exibidas na tela

###### logger.record.{class}

- **Tipo**: Enumeração
- **Valores**: `CRIT`, `ERROR`, `WARN`, `INFO`, `DEBUG`
- **Descrição**: Sobrescrita do nível de log por classe
- **Exemplo**: `logger.record.net.i2p.router.transport.udp=DEBUG`

##### Opções de Exibição

###### logger.displayOnScreen

- **Tipo**: Booleano
- **Padrão**: true
- **Descrição**: Se deve exibir mensagens de log na saída do console

###### logger.dropDuplicates

- **Tipo**: Booleano
- **Padrão**: true
- **Descrição**: Descarta mensagens de log duplicadas consecutivas

###### logger.dropOnOverflow

- **Tipo**: Booleano
- **Padrão**: false
- **Descrição**: Descarta mensagens quando o buffer está cheio (em vez de bloquear)

##### Comportamento de flushing (esvaziamento do buffer)

###### logger.flushInterval

- **Tipo**: Inteiro (segundos)
- **Padrão**: 29
- **Desde**: Versão 0.9.18
- **Descrição**: Com que frequência gravar o buffer de log em disco

##### Configuração do Formato

###### logger.format

- **Tipo**: String (sequência de caracteres)
- **Descrição**: Modelo de formato de mensagem de log
- **Caracteres de formato**:
  - `d` = data/hora
  - `c` = nome da classe
  - `t` = nome da thread
  - `p` = prioridade (nível de log)
  - `m` = mensagem
- **Exemplo**: `dctpm` produz `[carimbo de data/hora] [classe] [thread] [nível] mensagem`

##### Compressão (Versão 0.9.56+)

###### logger.gzip

- **Tipo**: Booleano
- **Padrão**: false
- **Desde**: Versão 0.9.56
- **Descrição**: Ativar a compactação gzip para arquivos de log rotacionados

###### logger.minGzipSize

- **Tipo**: Inteiro (bytes)
- **Padrão**: 65536
- **Desde**: Versão 0.9.56
- **Descrição**: Tamanho mínimo de arquivo para ativar a compressão (64 KB padrão)

##### Gerenciamento de Arquivos

###### logger.logBufferSize

- **Tipo**: Inteiro (bytes)
- **Padrão**: 1024
- **Descrição**: Máximo de mensagens a armazenar em buffer antes de descarregar

###### logger.logFileName

- **Tipo**: String (caminho de arquivo)
- **Padrão**: `logs/log-@.txt`
- **Descrição**: Padrão de nomenclatura do arquivo de log (`@` substituído pelo número de rotação)

###### logger.logFilenameOverride

- **Tipo**: String (caminho de arquivo)
- **Descrição**: Substituição do nome do arquivo de log (desativa o padrão de rotação)

###### logger.logFileSize

- **Tipo**: String (tamanho com unidade)
- **Padrão**: 10M
- **Unidades**: K (quilobytes), M (megabytes), G (gigabytes)
- **Exemplo**: `50M`, `1G`

###### logger.logRotationLimit

- **Tipo**: Inteiro
- **Padrão**: 2
- **Descrição**: Maior número de arquivo na rotação (log-0.txt até log-N.txt)

#### Exemplo de configuração

```properties
# Basic logging configuration
logger.consoleBufferSize=50
logger.dateFormat=yyyy-MM-dd HH:mm:ss.SSS
logger.defaultLevel=WARN
logger.displayOnScreen=true
logger.dropDuplicates=true
logger.dropOnOverflow=false

# Flushing and format
logger.flushInterval=30
logger.format=dctpm

# File management
logger.logBufferSize=2048
logger.logFileName=logs/log-@.txt
logger.logFileSize=25M
logger.logRotationLimit=5

# Compression (0.9.56+)
logger.gzip=true
logger.minGzipSize=131072

# On-screen filtering
logger.minimumOnScreenLevel=ERROR

# Per-class overrides
logger.record.net.i2p.router.transport=INFO
logger.record.net.i2p.router.tunnel=DEBUG
logger.record.net.i2p.crypto=WARN
```
---

### Configuração do plugin

#### Configuração individual do plugin (plugins/*/plugin.config)

**Localização**: `$I2P_CONFIG_DIR/plugins/{plugin-name}/plugin.config`   **Formato**: Formato padrão de arquivo de configuração do I2P   **Documentação**: [Especificação do Plugin](/docs/specs/plugin/)

##### Propriedades obrigatórias

###### nome

- **Tipo**: String
- **Obrigatório**: Sim
- **Descrição**: Nome de exibição do plugin
- **Exemplo**: `name=I2P Plugin Example`

###### chave

- **Tipo**: String (chave pública)
- **Obrigatório**: Sim (omitir para plugins assinados com SU3)
- **Descrição**: Chave pública de assinatura do plugin para verificação
- **Formato**: Chave de assinatura codificada em Base64

###### signatário

- **Tipo**: String
- **Obrigatório**: Sim
- **Descrição**: Identidade do assinante do plugin
- **Exemplo**: `signer=user@example.i2p`

###### versão

- **Tipo**: String (formato VersionComparator)
- **Obrigatório**: Sim
- **Descrição**: Versão do plugin para verificação de atualizações
- **Formato**: Versionamento semântico ou formato comparável personalizado
- **Exemplo**: `version=1.2.3`

##### Propriedades de Exibição

###### data

- **Tipo**: Long (timestamp Unix em milissegundos)
- **Descrição**: Data de lançamento do plugin

###### autor

- **Tipo**: String
- **Descrição**: Nome do autor do plugin

###### websiteURL

- **Tipo**: String (URL)
- **Descrição**: URL do site do plugin

###### updateURL

- **Tipo**: String (URL)
- **Descrição**: URL de verificação de atualização do plugin

###### updateURL.su3

- **Tipo**: String (URL)
- **Desde**: Versão 0.9.15
- **Descrição**: URL de atualização no formato SU3 (preferencial)

###### descrição

- **Tipo**: String
- **Descrição**: Descrição do plugin em inglês

###### description_{language}

- **Tipo**: String
- **Descrição**: Descrição localizada do plugin
- **Exemplo**: `description_de=Deutsche Beschreibung`

###### licença

- **Tipo**: Cadeia de caracteres
- **Descrição**: Identificador de licença do plugin
- **Exemplo**: `license=Apache 2.0`

##### Propriedades de Instalação

###### não iniciar na instalação

- **Tipo**: Booleano
- **Padrão**: false
- **Descrição**: Impedir início automático após a instalação

###### É necessário reiniciar o router

- **Tipo**: Booleano
- **Padrão**: false
- **Descrição**: Exigir reinicialização do router após a instalação

###### somente instalação

- **Tipo**: Booleano
- **Padrão**: false
- **Descrição**: Instalar apenas uma vez (sem atualizações)

###### somente atualização

- **Tipo**: Booleano
- **Padrão**: false
- **Descrição**: Atualizar somente a instalação existente (sem instalação nova)

##### Exemplo de Configuração de Plugin

```properties
# Required properties
name=Example I2P Plugin
signer=developer@mail.i2p
version=1.5.0

# Display properties
author=Plugin Developer
websiteURL=http://plugin.example.i2p
updateURL=http://plugin.example.i2p/update.xpi2p
updateURL.su3=http://plugin.example.i2p/update.su3
description=Example plugin demonstrating configuration
description_de=Beispiel-Plugin zur Demonstration der Konfiguration
license=MIT

# Installation behavior
dont-start-at-install=false
router-restart-required=false
```
#### Configuração Global de Plugins (plugins.config)

**Local**: `$I2P_CONFIG_DIR/plugins.config`   **Finalidade**: Ativar/desativar plugins instalados globalmente

##### Formato de Propriedade

```properties
plugin.{name}.startOnLoad=true|false
```
- `{name}`: Nome do plugin definido em plugin.config
- `startOnLoad`: Se deve iniciar o plugin na inicialização do router

##### Exemplo

```properties
plugin.i2psnark.startOnLoad=true
plugin.susimail.startOnLoad=true
plugin.susidns.startOnLoad=true
plugin.i2pbote.startOnLoad=false
```
---

### Configuração de Aplicações Web (webapps.config)

**Localização**: `$I2P_CONFIG_DIR/webapps.config`   **Finalidade**: Ativar/desativar e configurar aplicações web

#### Formato da Propriedade

##### webapps.{name}.startOnLoad

- **Tipo**: Booleano
- **Descrição**: Indica se o aplicativo web deve ser iniciado na inicialização do router
- **Formato**: `webapps.{name}.startOnLoad=true|false`

##### webapps.{name}.classpath

- **Tipo**: String (caminhos separados por espaço ou vírgula)
- **Descrição**: Elementos adicionais de classpath para a aplicação web
- **Formato**: `webapps.{name}.classpath=[paths]`

#### Substituição de Variáveis

Os caminhos oferecem suporte às seguintes substituições de variáveis:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Variable</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Expands To</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Context</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$I2P</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Base I2P directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Core webapps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$CONFIG</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">User config directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">All webapps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$PLUGIN</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Plugin directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Plugin webapps</td>
    </tr>
  </tbody>
</table>
#### Resolução do Classpath

- **Aplicações web do núcleo**: Caminhos relativos a `$I2P/lib`
- **Aplicações web de plugins**: Caminhos relativos a `$CONFIG/plugins/{appname}/lib`

#### Exemplo de configuração

```properties
# Router console
webapps.routerconsole.startOnLoad=true
webapps.routerconsole.classpath=routerconsole.jar

# I2PSnark
webapps.i2psnark.startOnLoad=true
webapps.i2psnark.classpath=i2psnark.jar

# SusiDNS
webapps.susidns.startOnLoad=true
webapps.susidns.classpath=susidns.jar

# Plugin webapp example
webapps.exampleplugin.startOnLoad=false
webapps.exampleplugin.classpath=$PLUGIN/lib/webapp.jar,$PLUGIN/lib/deps.jar
```
---

### Configuração do Router (router.config)

**Localização**: `$I2P_CONFIG_DIR/router.config`   **Interface de configuração**: console do router em `/configadvanced`   **Finalidade**: Configurações centrais do router e parâmetros de rede

#### Categorias de configuração

##### Configuração de Rede

Configurações de largura de banda:

```properties
i2np.bandwidth.inboundKBytesPerSecond=100
i2np.bandwidth.outboundKBytesPerSecond=50
i2np.bandwidth.share.percentage=80
```
Configuração de transporte:

```properties
# NTCP (TCP-based transport)
i2np.ntcp.port=8887
i2np.ntcp.enable=true
i2np.ntcp.autoip=true

# SSU (UDP-based transport)
i2np.udp.port=8887
i2np.udp.enable=true

# UPnP/NAT-PMP
i2np.upnp.enable=true
```
##### Comportamento do Router

```properties
# Tunnel participation
router.maxParticipatingTunnels=200
router.sharePercentage=80

# Updates
router.updatePolicy=notify
router.updateURL=http://update.i2p2.i2p/

# Network integration
router.hiddenMode=false
router.clockSkewOffset=0
```
##### Configuração do Console

```properties
# Language and display
routerconsole.lang=en
routerconsole.country=US
routerconsole.summaryRefresh=60

# Browser
routerconsole.browser=default

# Security
routerconsole.enableCompression=true
```
##### Configuração de horário

```properties
# NTP
time.disabled=false
time.sntpServerList=0.pool.ntp.org,1.pool.ntp.org
```
**Nota**: A configuração do router é extensa. Consulte o console do router em `/configadvanced` para a referência completa das propriedades.

---

## Arquivos de configuração de aplicativos

### Configuração do Livro de Endereços (addressbook/config.txt)

**Localização**: `$I2P_CONFIG_DIR/addressbook/config.txt`   **Aplicativo**: SusiDNS   **Finalidade**: Resolução de nomes de host e gerenciamento do livro de endereços

#### Locais dos arquivos

##### router_addressbook

- **Padrão**: `../hosts.txt`
- **Descrição**: Livro de endereços principal (nomes de host em todo o sistema)
- **Formato**: Formato padrão do arquivo hosts

##### privatehosts.txt

- **Localização**: `$I2P_CONFIG_DIR/addressbook/privatehosts.txt`
- **Descrição**: Mapeamentos privados de nomes de host
- **Prioridade**: Máxima (sobrepõe-se a todas as outras fontes)

##### userhosts.txt

- **Localização**: `$I2P_CONFIG_DIR/addressbook/userhosts.txt`
- **Descrição**: Mapeamentos de nomes de host adicionados pelo usuário
- **Gerenciamento**: Via interface SusiDNS

##### hosts.txt

- **Localização**: `$I2P_CONFIG_DIR/addressbook/hosts.txt`
- **Descrição**: Livro de endereços público baixado
- **Fonte**: feeds de assinatura

#### Serviço de Nomes

##### BlockfileNamingService (Padrão desde 0.8.8)

Formato de armazenamento: - **Arquivo**: `hostsdb.blockfile` - **Localização**: `$I2P_CONFIG_DIR/addressbook/` - **Desempenho**: ~10x consultas mais rápidas do que em hosts.txt - **Formato**: Formato de banco de dados binário

Serviço de nomes legado: - **Formato**: Texto simples hosts.txt - **Status**: Obsoleto, mas ainda suportado - **Caso de uso**: Edição manual, controle de versão

#### Regras de nomes de host

Os nomes de host do I2P devem estar em conformidade com:

1. **Requisito de TLD**: Deve terminar com `.i2p`
2. **Comprimento máximo**: 67 caracteres no total
3. **Conjunto de caracteres**: `[a-z]`, `[0-9]`, `.` (ponto), `-` (hífen)
4. **Maiúsculas/minúsculas**: Somente minúsculas
5. **Restrições de início**: Não pode começar com `.` ou `-`
6. **Padrões proibidos**: Não pode conter `..`, `.-` ou `-.` (desde 0.6.1.33)
7. **Reservado**: Nomes de host Base32 `*.b32.i2p` (52 caracteres de base32.b32.i2p)

##### Exemplos válidos

```
example.i2p
my-site.i2p
test.example.i2p
site123.i2p
```
##### Exemplos inválidos

```
example.com          # Wrong TLD
-invalid.i2p         # Starts with hyphen
invalid..i2p         # Contains double dot
invalid.-.i2p        # Contains dot-hyphen
UPPERCASE.I2P        # Must be lowercase
verylonghostnameover67charactersthatexceedsthemaximumlength.i2p  # Too long
```
#### Gerenciamento de Assinaturas

##### subscriptions.txt

- **Localização**: `$I2P_CONFIG_DIR/addressbook/subscriptions.txt`
- **Formato**: Um URL por linha
- **Padrão**: `http://i2p-projekt.i2p/hosts.txt`

##### Formato do Feed de Assinatura (Desde a versão 0.9.26)

Formato avançado de feed com metadados:

```
#
# I2P Address Book Subscription Feed
# Format: hostname=destination [#property=value ...]
#

example.i2p=base64destination #added=20250101 #src=manual
another.i2p=base64destination #added=20250102 #src=feed1
```
Propriedades de metadados: - `added`: Data em que o nome de host foi adicionado (formato YYYYMMDD) - `src`: Identificador de origem - `sig`: Assinatura opcional

**Retrocompatibilidade**: O formato simples hostname=destination ainda é suportado.

#### Exemplo de Configuração

```properties
# Address book locations
router_addressbook=../hosts.txt
privatehosts.txt=$CONFIG/addressbook/privatehosts.txt
userhosts.txt=$CONFIG/addressbook/userhosts.txt
hosts.txt=$CONFIG/addressbook/hosts.txt

# Naming service
naming.service=BlockfileNamingService
naming.service.blockfile.location=$CONFIG/addressbook/hostsdb.blockfile

# Subscriptions
subscriptions.txt=$CONFIG/addressbook/subscriptions.txt
subscriptions.schedule=daily
subscriptions.proxy=false
```
---

### Configuração do I2PSnark (i2psnark.config.d/i2psnark.config)

**Localização**: `$I2P_CONFIG_DIR/i2psnark.config.d/i2psnark.config`   **Aplicativo**: cliente BitTorrent I2PSnark   **Interface de Configuração**: GUI Web em http://127.0.0.1:7657/i2psnark

#### Estrutura de diretórios

```
$I2P_CONFIG_DIR/i2psnark.config.d/
├── i2psnark.config
├── [torrent-hash-1]/
│   └── *.config
├── [torrent-hash-2]/
│   └── *.config
└── ...
```
#### Configuração Principal (i2psnark.config)

Configuração padrão mínima:

```properties
i2psnark.dir=i2psnark
```
Propriedades adicionais gerenciadas via interface web:

```properties
# Basic settings
i2psnark.dir=i2psnark
i2psnark.autoStart=false
i2psnark.openTrackers=true

# Network settings
i2psnark.uploaders=8
i2psnark.upBW=40
i2psnark.seedPct=100

# I2CP settings
i2psnark.i2cpHost=127.0.0.1
i2psnark.i2cpPort=7654
```
#### Configuração individual de torrents

**Localização**: `$I2P_CONFIG_DIR/i2psnark.config.d/[torrent-hash]/*.config`   **Formato**: Configurações por torrent   **Gerenciamento**: Automático (via interface web)

As propriedades incluem: - Configurações de upload/download específicas do torrent - Prioridades de arquivos - Informações do rastreador - Limites de pares

**Nota**: As configurações de torrent são gerenciadas principalmente pela interface web. A edição manual não é recomendada.

#### Organização de Dados de Torrent

O armazenamento de dados é separado da configuração:

```
$I2P_CONFIG_DIR/i2psnark/          # Data directory
├── *.torrent                       # Torrent metadata files
├── *.torrent.downloaded/           # Downloaded file directories
├── file1.dat                       # Direct file downloads
└── ...

$I2P_CONFIG_DIR/i2psnark.config.d/ # Configuration directory
├── i2psnark.config                 # Main config
└── [hashes]/                       # Per-torrent configs
```
---

### Configuração do I2PTunnel (i2ptunnel.config)

**Localização**: `$I2P_CONFIG_DIR/i2ptunnel.config` (legado) ou `$I2P_CONFIG_DIR/i2ptunnel.config.d/` (moderno)   **Interface de configuração**: console do Router em `/i2ptunnel`   **Alteração de formato**: Versão 0.9.42 (agosto de 2019)

#### Estrutura de Diretórios (Versão 0.9.42+)

A partir da versão 0.9.42, o arquivo padrão i2ptunnel.config é dividido automaticamente:

```
$I2P_CONFIG_DIR/
├── i2ptunnel.config.d/
│   ├── http-proxy/
│   │   └── tunnel.config
│   ├── irc-proxy/
│   │   └── tunnel.config
│   ├── ssh-service/
│   │   └── tunnel.config
│   └── ...
└── i2ptunnel.config (legacy, auto-migrated)
```
**Diferença crítica de formato**: - **Formato monolítico**: Propriedades prefixadas com `tunnel.N.` - **Formato dividido**: Propriedades **NÃO** prefixadas (por exemplo, `description=`, não `tunnel.0.description=`)

#### Comportamento de Migração

Na primeira execução após a atualização para a 0.9.42: 1. O i2ptunnel.config existente é lido 2. As configurações individuais de tunnel são criadas em i2ptunnel.config.d/ 3. As propriedades têm os prefixos removidos nos arquivos separados 4. É feito backup do arquivo original 5. O formato legado ainda é suportado para compatibilidade com versões anteriores

#### Seções de Configuração

A configuração do I2PTunnel está documentada em detalhes na seção [Referência de Configuração do I2PTunnel](#i2ptunnel-configuration-reference) abaixo. As descrições das propriedades são aplicáveis tanto ao formato monolítico (`tunnel.N.property`) quanto ao formato separado (`property`).

---

## Referência de Configuração do I2PTunnel

Esta seção fornece uma referência técnica abrangente para todas as propriedades de configuração do I2PTunnel. As propriedades são exibidas no formato dividido (sem o prefixo `tunnel.N.`). No formato monolítico, adicione o prefixo `tunnel.N.` a todas as propriedades, em que N é o número do tunnel.

**Importante**: As propriedades descritas como `tunnel.N.option.i2cp.*` são implementadas no I2PTunnel e **NÃO** são suportadas por outras interfaces, como o protocolo I2CP ou a SAM API.

### Propriedades básicas

#### tunnel.N.description (descrição)

- **Tipo**: String
- **Contexto**: Todos os tunnels
- **Descrição**: Descrição de tunnel legível por humanos para exibição na interface do usuário
- **Exemplo**: `description=HTTP Proxy for outproxy access`

#### tunnel.N.name (nome)

- **Tipo**: String
- **Contexto**: Todos os tunnels
- **Obrigatório**: Sim
- **Descrição**: Identificador de tunnel exclusivo e nome de exibição
- **Exemplo**: `name=I2P HTTP Proxy`

#### tunnel.N.type (tipo)

- **Tipo**: Enumeração
- **Contexto**: Todos os tunnels
- **Obrigatório**: Sim
- **Valores**:
  - `client` - Tunnel de cliente genérico
  - `httpclient` - Cliente de proxy HTTP
  - `ircclient` - Tunnel de cliente IRC
  - `socksirctunnel` - Proxy SOCKS para IRC
  - `sockstunnel` - Proxy SOCKS (versão 4, 4a, 5)
  - `connectclient` - Cliente de proxy CONNECT
  - `streamrclient` - Cliente Streamr
  - `server` - Tunnel de servidor genérico
  - `httpserver` - Tunnel de servidor HTTP
  - `ircserver` - Tunnel de servidor IRC
  - `httpbidirserver` - Servidor HTTP bidirecional
  - `streamrserver` - Servidor Streamr

#### tunnel.N.interface (interface)

- **Tipo**: String (endereço IP ou nome de host)
- **Contexto**: Apenas tunnels de cliente
- **Padrão**: 127.0.0.1
- **Descrição**: Interface local à qual vincular para conexões de entrada
- **Nota de segurança**: Vincular a 0.0.0.0 permite conexões remotas
- **Exemplo**: `interface=127.0.0.1`

#### tunnel.N.listenPort (listenPort)

- **Tipo**: Inteiro
- **Contexto**: Apenas tunnels de cliente
- **Intervalo**: 1-65535
- **Descrição**: Porta local para escutar conexões de clientes
- **Exemplo**: `listenPort=4444`

#### tunnel.N.targetHost (targetHost)

- **Tipo**: String (endereço IP ou nome de host)
- **Contexto**: Apenas para tunnels de servidor
- **Descrição**: Servidor local para o qual encaminhar conexões
- **Exemplo**: `targetHost=127.0.0.1`

#### tunnel.N.targetPort (targetPort)

- **Tipo**: Inteiro
- **Contexto**: Apenas tunnels de servidor
- **Intervalo**: 1-65535
- **Descrição**: Porta no targetHost para se conectar
- **Exemplo**: `targetPort=80`

#### tunnel.N.targetDestination (targetDestination)

- **Tipo**: String (destinos separados por vírgula ou espaço)
- **Contexto**: Apenas client tunnels
- **Formato**: `destination[:port][,destination[:port]]`
- **Descrição**: destino(s) I2P para se conectar
- **Exemplos**:
  - `targetDestination=example.i2p`
  - `targetDestination=example.i2p:8080`
  - `targetDestination=site1.i2p,site2.i2p:8080`

#### tunnel.N.i2cpHost (i2cpHost)

- **Tipo**: String (endereço IP ou nome de host)
- **Padrão**: 127.0.0.1
- **Descrição**: Endereço da interface I2CP do router I2P
- **Observação**: Ignorado quando executado no contexto do router
- **Exemplo**: `i2cpHost=127.0.0.1`

#### tunnel.N.i2cpPort (i2cpPort)

- **Tipo**: Inteiro
- **Padrão**: 7654
- **Intervalo**: 1-65535
- **Descrição**: porta I2CP do router I2P
- **Observação**: Ignorado quando executado no contexto do router
- **Exemplo**: `i2cpPort=7654`

#### tunnel.N.startOnLoad (startOnLoad)

- **Tipo**: Booleano
- **Padrão**: true
- **Descrição**: Se o tunnel (túnel) deve iniciar quando o I2PTunnel (ferramenta de túnel do I2P) for carregado
- **Exemplo**: `startOnLoad=true`

### Configuração do proxy

#### tunnel.N.proxyList (proxyList)

- **Tipo**: String (nomes de host separados por vírgula ou espaço)
- **Contexto**: Apenas proxies HTTP e SOCKS
- **Descrição**: Lista de hosts de outproxy (proxy de saída)
- **Exemplo**: `proxyList=outproxy.example.i2p,backup.example.i2p`

### Configuração do Servidor

#### tunnel.N.privKeyFile (privKeyFile)

- **Tipo**: String (caminho de arquivo)
- **Contexto**: Servidores e tunnels de cliente persistentes
- **Descrição**: Arquivo contendo chaves privadas de destino persistentes
- **Caminho**: Absoluto ou relativo ao diretório de configuração do I2P
- **Exemplo**: `privKeyFile=eepsite/eepPriv.dat`

#### tunnel.N.spoofedHost (spoofedHost)

- **Tipo**: String (nome de host)
- **Contexto**: Somente servidores HTTP
- **Padrão**: nome de host Base32 do destino
- **Descrição**: Valor do cabeçalho Host passado ao servidor local
- **Exemplo**: `spoofedHost=example.i2p`

#### tunnel.N.spoofedHost.NNNN (spoofedHost.NNNN)

- **Tipo**: String (nome do host)
- **Contexto**: Apenas servidores HTTP
- **Descrição**: Sobrescrita do host virtual para uma porta de escuta específica
- **Caso de uso**: Hospedar vários sites em portas diferentes
- **Exemplo**: `spoofedHost.8080=site1.example.i2p`

### Opções específicas do cliente

#### tunnel.N.sharedClient (sharedClient)

- **Tipo**: Booleano
- **Contexto**: Somente Client tunnels
- **Padrão**: false
- **Descrição**: Se vários clientes podem compartilhar este tunnel
- **Exemplo**: `sharedClient=false`

#### tunnel.N.option.persistentClientKey (persistentClientKey)

- **Tipo**: Booleano
- **Contexto**: Apenas tunnels do cliente
- **Padrão**: false
- **Descrição**: Armazena e reutiliza chaves de destino entre reinicializações
- **Conflito**: Mutuamente exclusivo com `i2cp.newDestOnResume=true`
- **Exemplo**: `option.persistentClientKey=true`

### Opções do I2CP (Implementação do I2PTunnel)

**Importante**: Essas propriedades têm o prefixo `option.i2cp.`, mas são **implementadas no I2PTunnel**, não na camada de protocolo I2CP. Elas não estão disponíveis via I2CP ou APIs do SAM.

#### tunnel.N.option.i2cp.delayOpen (option.i2cp.delayOpen)

- **Tipo**: Booleano
- **Contexto**: Apenas tunnels de cliente
- **Padrão**: false
- **Descrição**: Atrasar a criação do tunnel até a primeira conexão
- **Caso de uso**: Poupar recursos em tunnels raramente usados
- **Exemplo**: `option.i2cp.delayOpen=false`

#### tunnel.N.option.i2cp.newDestOnResume (option.i2cp.newDestOnResume)

- **Tipo**: Booleano
- **Contexto**: Somente para Client tunnels
- **Padrão**: false
- **Requer**: `i2cp.closeOnIdle=true`
- **Conflito**: Mutuamente exclusivo com `persistentClientKey=true`
- **Descrição**: Criar um novo destino após o tempo limite de inatividade
- **Exemplo**: `option.i2cp.newDestOnResume=false`

#### tunnel.N.option.i2cp.leaseSetPrivateKey (option.i2cp.leaseSetPrivateKey)

- **Tipo**: String (chave codificada em base64)
- **Contexto**: Apenas server tunnels
- **Descrição**: Chave de criptografia privada persistente do leaseset
- **Caso de uso**: Manter o leaseset criptografado consistente após reinicializações
- **Exemplo**: `option.i2cp.leaseSetPrivateKey=AAAA...base64...`

#### tunnel.N.option.i2cp.leaseSetSigningPrivateKey (option.i2cp.leaseSetSigningPrivateKey)

- **Tipo**: String (sigtype:base64)
- **Contexto**: Apenas Server tunnels
- **Formato**: `sigtype:base64key`
- **Descrição**: Chave privada de assinatura de leaseset persistente
- **Exemplo**: `option.i2cp.leaseSetSigningPrivateKey=7:AAAA...base64...`

### Opções Específicas do Servidor

#### tunnel.N.option.enableUniqueLocal (option.enableUniqueLocal)

- **Tipo**: Booleano
- **Contexto**: Apenas para tunnels de servidor
- **Padrão**: false
- **Descrição**: Usar um IP local exclusivo por destino I2P remoto
- **Caso de uso**: Rastrear IPs de clientes nos logs do servidor
- **Observação de segurança**: Pode reduzir o anonimato
- **Exemplo**: `option.enableUniqueLocal=false`

#### tunnel.N.option.targetForPort.NNNN (option.targetForPort.NNNN)

- **Tipo**: String (hostname:port)
- **Contexto**: Apenas tunnels de servidor
- **Descrição**: Substitui targetHost/targetPort para a porta de entrada NNNN
- **Caso de uso**: Roteamento baseado em porta para diferentes serviços locais
- **Exemplo**: `option.targetForPort.8080=localhost:8080`

### Configuração do Pool de Threads

#### tunnel.N.option.i2ptunnel.usePool (option.i2ptunnel.usePool)

- **Tipo**: Booleano
- **Contexto**: Apenas para server tunnels
- **Padrão**: true
- **Descrição**: Usar pool de threads para tratamento de conexões
- **Observação**: Sempre false para servidores padrão (ignorado)
- **Exemplo**: `option.i2ptunnel.usePool=true`

#### tunnel.N.option.i2ptunnel.blockingHandlerCount (option.i2ptunnel.blockingHandlerCount)

- **Tipo**: Inteiro
- **Contexto**: Apenas para server tunnels
- **Padrão**: 65
- **Descrição**: Tamanho máximo do pool de threads
- **Nota**: Ignorado para servidores padrão
- **Exemplo**: `option.i2ptunnel.blockingHandlerCount=100`

### Opções do cliente HTTP

#### tunnel.N.option.i2ptunnel.httpclient.allowInternalSSL (option.i2ptunnel.httpclient.allowInternalSSL)

- **Tipo**: Booleano
- **Contexto**: Apenas clientes HTTP
- **Padrão**: false
- **Descrição**: Permitir conexões SSL para endereços .i2p
- **Exemplo**: `option.i2ptunnel.httpclient.allowInternalSSL=false`

#### tunnel.N.option.i2ptunnel.httpclient.disableAddressHelper (option.i2ptunnel.httpclient.disableAddressHelper)

- **Tipo**: Booleano
- **Contexto**: Apenas clientes HTTP
- **Padrão**: false
- **Descrição**: Desativar links de address helper (assistente de endereço) nas respostas do proxy
- **Exemplo**: `option.i2ptunnel.httpclient.disableAddressHelper=false`

#### tunnel.N.option.i2ptunnel.httpclient.jumpServers (option.i2ptunnel.httpclient.jumpServers)

- **Tipo**: String (URLs separadas por vírgula ou espaço)
- **Contexto**: Somente clientes HTTP
- **Descrição**: URLs de jump server (servidor de salto) para resolução de nomes de host
- **Exemplo**: `option.i2ptunnel.httpclient.jumpServers=http://jump.i2p/jump,http://stats.i2p/jump`

#### tunnel.N.option.i2ptunnel.httpclient.sendAccept (option.i2ptunnel.httpclient.sendAccept)

- **Tipo**: Booleano
- **Contexto**: apenas clientes HTTP
- **Padrão**: false
- **Descrição**: Repassar os cabeçalhos Accept-* (exceto Accept e Accept-Encoding)
- **Exemplo**: `option.i2ptunnel.httpclient.sendAccept=false`

#### tunnel.N.option.i2ptunnel.httpclient.sendReferer (option.i2ptunnel.httpclient.sendReferer)

- **Tipo**: Booleano
- **Contexto**: Apenas clientes HTTP
- **Padrão**: false
- **Descrição**: Encaminhar os cabeçalhos Referer através do proxy
- **Nota de privacidade**: Pode expor informações
- **Exemplo**: `option.i2ptunnel.httpclient.sendReferer=false`

#### tunnel.N.option.i2ptunnel.httpclient.sendUserAgent (option.i2ptunnel.httpclient.sendUserAgent)

- **Tipo**: Booleano
- **Contexto**: apenas clientes HTTP
- **Padrão**: false
- **Descrição**: Encaminhar cabeçalhos User-Agent pelo proxy
- **Observação de privacidade**: Pode vazar informações do navegador
- **Exemplo**: `option.i2ptunnel.httpclient.sendUserAgent=false`

#### tunnel.N.option.i2ptunnel.httpclient.sendVia (option.i2ptunnel.httpclient.sendVia)

- **Tipo**: Booleano
- **Contexto**: Apenas clientes HTTP
- **Padrão**: false
- **Descrição**: Passar cabeçalhos Via através do proxy
- **Exemplo**: `option.i2ptunnel.httpclient.sendVia=false`

#### tunnel.N.option.i2ptunnel.httpclient.SSLOutproxies (option.i2ptunnel.httpclient.SSLOutproxies)

- **Tipo**: String (destinos separados por vírgulas ou espaços)
- **Contexto**: Somente clientes HTTP
- **Descrição**: Outproxies SSL na rede (proxies de saída) para HTTPS
- **Exemplo**: `option.i2ptunnel.httpclient.SSLOutproxies=ssl-outproxy.i2p`

#### tunnel.N.option.i2ptunnel.useLocalOutproxy (option.i2ptunnel.useLocalOutproxy)

- **Tipo**: Booleano
- **Contexto**: Somente clientes HTTP
- **Padrão**: true
- **Descrição**: Usar plugins de outproxy (proxy de saída) locais registrados
- **Exemplo**: `option.i2ptunnel.useLocalOutproxy=true`

### Autenticação do cliente HTTP

#### tunnel.N.option.proxyAuth (option.proxyAuth)

- **Tipo**: Enumeração
- **Contexto**: Somente clientes HTTP
- **Padrão**: false
- **Valores**: `true`, `false`, `basic`, `digest`
- **Descrição**: Exigir autenticação local para acesso ao proxy
- **Observação**: `true` é equivalente a `basic`
- **Exemplo**: `option.proxyAuth=basic`

#### tunnel.N.option.proxy.auth.USER.md5 (option.proxy.auth.USER.md5)

- **Tipo**: String (hexadecimal em minúsculas de 32 caracteres)
- **Contexto**: apenas clientes HTTP
- **Requer**: `proxyAuth=basic` ou `proxyAuth=digest`
- **Descrição**: hash MD5 da senha do usuário USER
- **Obsoleto**: Use SHA-256 em vez disso (0.9.56+)
- **Exemplo**: `option.proxy.auth.alice.md5=5f4dcc3b5aa765d61d8327deb882cf99`

#### tunnel.N.option.proxy.auth.USER.sha256 (option.proxy.auth.USER.sha256)

- **Tipo**: String (hexadecimal em minúsculas de 64 caracteres)
- **Contexto**: apenas clientes HTTP
- **Requer**: `proxyAuth=digest`
- **Desde**: Versão 0.9.56
- **Padrão**: RFC 7616
- **Descrição**: hash SHA-256 da senha do usuário USER
- **Exemplo**: `option.proxy.auth.alice.sha256=5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8`

### Autenticação do outproxy (proxy de saída do I2P)

#### tunnel.N.option.outproxyAuth (option.outproxyAuth)

- **Tipo**: Booleano
- **Contexto**: Apenas clientes HTTP
- **Padrão**: false
- **Descrição**: Enviar autenticação ao outproxy (proxy de saída)
- **Exemplo**: `option.outproxyAuth=false`

#### tunnel.N.option.outproxyUsername (option.outproxyUsername)

- **Tipo**: String
- **Contexto**: Apenas clientes HTTP
- **Requer**: `outproxyAuth=true`
- **Descrição**: Nome de usuário para autenticação do outproxy
- **Exemplo**: `option.outproxyUsername=user`

#### tunnel.N.option.outproxyPassword (option.outproxyPassword)

- **Tipo**: String
- **Contexto**: Somente clientes HTTP
- **Requer**: `outproxyAuth=true`
- **Descrição**: Senha para autenticação do outproxy
- **Segurança**: Armazenado em texto simples
- **Exemplo**: `option.outproxyPassword=secret`

### Opções do cliente SOCKS

#### tunnel.N.option.i2ptunnel.socks.proxy.default (option.i2ptunnel.socks.proxy.default)

- **Tipo**: String (destinos separados por vírgula ou espaço)
- **Contexto**: Apenas clientes SOCKS
- **Descrição**: Outproxies (proxies de saída) na rede para portas não especificadas
- **Exemplo**: `option.i2ptunnel.socks.proxy.default=outproxy.i2p`

#### tunnel.N.option.i2ptunnel.socks.proxy.NNNN (option.i2ptunnel.socks.proxy.NNNN)

- **Tipo**: String (destinos separados por vírgula ou espaço)
- **Contexto**: Apenas clientes SOCKS
- **Descrição**: Outproxies (proxies de saída) na rede especificamente para a porta NNNN
- **Exemplo**: `option.i2ptunnel.socks.proxy.443=ssl-outproxy.i2p`

#### tunnel.N.option.outproxyType (option.outproxyType)

- **Tipo**: Enumeração
- **Contexto**: Somente para clientes SOCKS
- **Padrão**: socks
- **Desde**: Versão 0.9.57
- **Valores**: `socks`, `connect` (HTTPS)
- **Descrição**: Tipo de outproxy (servidor proxy de saída) configurado
- **Exemplo**: `option.outproxyType=connect`

### Opções do Servidor HTTP

#### tunnel.N.option.maxPosts (option.maxPosts)

- **Tipo**: Inteiro
- **Contexto**: Apenas servidores HTTP
- **Padrão**: 0 (ilimitado)
- **Descrição**: Máximo de POSTs de um único Destination (identificador de serviço no I2P) por postCheckTime
- **Exemplo**: `option.maxPosts=10`

#### tunnel.N.option.maxTotalPosts (option.maxTotalPosts)

- **Tipo**: Inteiro
- **Contexto**: Apenas servidores HTTP
- **Padrão**: 0 (ilimitado)
- **Descrição**: Máximo de POSTs de todos os destinos por postCheckTime
- **Exemplo**: `option.maxTotalPosts=50`

#### tunnel.N.option.postCheckTime (option.postCheckTime)

- **Tipo**: Inteiro (segundos)
- **Contexto**: apenas servidores HTTP
- **Padrão**: 300
- **Descrição**: Janela de tempo para verificar limites de POST
- **Exemplo**: `option.postCheckTime=600`

#### tunnel.N.option.postBanTime (option.postBanTime)

- **Tipo**: Inteiro (segundos)
- **Contexto**: Somente servidores HTTP
- **Padrão**: 1800
- **Descrição**: Duração do banimento após maxPosts ser excedido para um único destino
- **Exemplo**: `option.postBanTime=3600`

#### tunnel.N.option.postTotalBanTime (option.postTotalBanTime)

- **Tipo**: Inteiro (segundos)
- **Contexto**: Apenas servidores HTTP
- **Padrão**: 600
- **Descrição**: Duração do banimento após maxTotalPosts ser excedido
- **Exemplo**: `option.postTotalBanTime=1200`

### Opções de Segurança do Servidor HTTP

#### tunnel.N.option.rejectInproxy (option.rejectInproxy)

- **Tipo**: Booleano
- **Contexto**: apenas servidores HTTP
- **Padrão**: false
- **Descrição**: Rejeita conexões que aparentemente vêm por um inproxy (proxy de entrada)
- **Exemplo**: `option.rejectInproxy=false`

#### tunnel.N.option.rejectReferer (option.rejectReferer)

- **Tipo**: Booleano
- **Contexto**: Apenas servidores HTTP
- **Padrão**: false
- **Desde**: Versão 0.9.25
- **Descrição**: Rejeita conexões com o cabeçalho Referer
- **Exemplo**: `option.rejectReferer=false`

#### tunnel.N.option.rejectUserAgents (option.rejectUserAgents)

- **Tipo**: Booleano
- **Contexto**: Apenas servidores HTTP
- **Padrão**: false
- **Desde**: Versão 0.9.25
- **Requer**: propriedade `userAgentRejectList`
- **Descrição**: Rejeita conexões com User-Agent correspondente
- **Exemplo**: `option.rejectUserAgents=false`

#### tunnel.N.option.userAgentRejectList (option.userAgentRejectList)

- **Tipo**: String (strings de correspondência separadas por vírgulas)
- **Contexto**: apenas servidores HTTP
- **Desde**: Versão 0.9.25
- **Maiúsculas/minúsculas**: correspondência sensível a maiúsculas/minúsculas
- **Especial**: "none" (desde 0.9.33) corresponde a um User-Agent vazio
- **Descrição**: Lista de padrões de User-Agent a rejeitar
- **Exemplo**: `option.userAgentRejectList=Mozilla,Opera,none`

### Opções do servidor IRC

#### tunnel.N.option.ircserver.fakeHostname (option.ircserver.fakeHostname)

- **Type**: String (padrão de nome de host)
- **Context**: Apenas servidores IRC
- **Default**: `%f.b32.i2p`
- **Tokens**:
  - `%f` = Hash de destino base32 completo
  - `%c` = Hash de destino ofuscado (ver cloakKey)
- **Description**: Formato do nome de host enviado ao servidor IRC
- **Example**: `option.ircserver.fakeHostname=%c.irc.i2p`

#### tunnel.N.option.ircserver.cloakKey (option.ircserver.cloakKey)

- **Tipo**: String (frase secreta)
- **Contexto**: Somente servidores IRC
- **Padrão**: Aleatório por sessão
- **Restrições**: Sem aspas nem espaços
- **Descrição**: Frase secreta para mascaramento consistente do nome de host
- **Caso de uso**: Rastreamento persistente de usuário entre reinicializações/servidores
- **Exemplo**: `option.ircserver.cloakKey=mysecretkey`

#### tunnel.N.option.ircserver.method (option.ircserver.method)

- **Tipo**: Enum
- **Contexto**: Somente para servidores IRC
- **Padrão**: user
- **Valores**: `user`, `webirc`
- **Descrição**: Método de autenticação para o servidor IRC
- **Exemplo**: `option.ircserver.method=webirc`

#### tunnel.N.option.ircserver.webircPassword (option.ircserver.webircPassword)

- **Tipo**: String (senha)
- **Contexto**: Apenas servidores IRC
- **Requer**: `method=webirc`
- **Restrições**: Sem aspas nem espaços
- **Descrição**: Senha para autenticação do protocolo WEBIRC
- **Exemplo**: `option.ircserver.webircPassword=webircpass`

#### tunnel.N.option.ircserver.webircSpoofIP (option.ircserver.webircSpoofIP)

- **Tipo**: String (endereço IP)
- **Contexto**: apenas servidores IRC
- **Requer**: `method=webirc`
- **Descrição**: endereço IP falsificado para o protocolo WEBIRC
- **Exemplo**: `option.ircserver.webircSpoofIP=10.0.0.1`

### Configuração de SSL/TLS

#### tunnel.N.option.useSSL (option.useSSL)

- **Tipo**: Booleano
- **Padrão**: false
- **Contexto**: Todos os tunnels
- **Comportamento**:
  - **Servidores**: Usar SSL para conexões com o servidor local
  - **Clientes**: Exigir SSL de clientes locais
- **Exemplo**: `option.useSSL=false`

#### tunnel.N.option.keystoreFile (option.keystoreFile)

- **Tipo**: String (caminho de arquivo)
- **Contexto**: Apenas client tunnels
- **Padrão**: `i2ptunnel-(random).ks`
- **Caminho**: Relativo a `$(I2P_CONFIG_DIR)/keystore/` se não for absoluto
- **Gerado automaticamente**: Criado se não existir
- **Descrição**: Arquivo keystore (repositório de chaves) contendo a chave privada SSL
- **Exemplo**: `option.keystoreFile=my-tunnel.ks`

#### tunnel.N.option.keystorePassword (option.keystorePassword)

- **Tipo**: String (senha)
- **Contexto**: Apenas client tunnels
- **Padrão**: changeit
- **Gerado automaticamente**: Senha aleatória se um novo keystore for criado
- **Descrição**: Senha para o keystore (repositório de chaves) SSL
- **Exemplo**: `option.keystorePassword=secretpassword`

#### tunnel.N.option.keyAlias (option.keyAlias)

- **Tipo**: String (apelido)
- **Contexto**: Apenas tunnels de cliente
- **Gerado automaticamente**: Criado se uma nova chave for gerada
- **Descrição**: Apelido para a chave privada no keystore (repositório de chaves)
- **Exemplo**: `option.keyAlias=mytunnel-key`

#### tunnel.N.option.keyPassword (option.keyPassword)

- **Tipo**: String (senha)
- **Contexto**: Apenas Client tunnels
- **Gerado automaticamente**: Senha aleatória se uma nova chave for criada
- **Descrição**: Senha para a chave privada no keystore
- **Exemplo**: `option.keyPassword=keypass123`

### Opções genéricas de I2CP e de Streaming

Todas as propriedades `tunnel.N.option.*` (não especificamente documentadas acima) são encaminhadas à interface I2CP e à biblioteca de streaming, com o prefixo `tunnel.N.option.` removido.

**Importante**: Estas são distintas das opções específicas do I2PTunnel. Consulte: - [Especificação do I2CP](/docs/specs/i2cp/) - [Especificação da Biblioteca de Streaming](/docs/specs/streaming/)

Exemplos de opções de streaming:

```properties
option.i2cp.messageReliability=BestEffort
option.i2p.streaming.connectDelay=1000
option.i2p.streaming.maxWindowSize=128
```
### Exemplo completo de Tunnel (túnel)

```properties
# HTTP Proxy (split format without tunnel.N. prefix)
name=I2P HTTP Proxy
description=HTTP proxy for accessing I2P sites and outproxy
type=httpclient
interface=127.0.0.1
listenPort=4444
targetDestination=
sharedClient=true
startOnLoad=true

# I2CP configuration
i2cpHost=127.0.0.1
i2cpPort=7654

# HTTP client options
option.i2ptunnel.httpclient.allowInternalSSL=false
option.i2ptunnel.httpclient.disableAddressHelper=false
option.i2ptunnel.httpclient.jumpServers=http://stats.i2p/cgi-bin/jump.cgi
option.i2ptunnel.httpclient.sendAccept=false
option.i2ptunnel.httpclient.sendReferer=false
option.i2ptunnel.httpclient.sendUserAgent=false

# Proxy authentication
option.proxyAuth=false

# Outproxy configuration
option.i2ptunnel.httpclient.SSLOutproxies=false.i2p
proxyList=false.i2p

# Client behavior
option.persistentClientKey=false
option.i2cp.delayOpen=false

# I2CP tunnel options
option.inbound.length=3
option.outbound.length=3
option.inbound.quantity=2
option.outbound.quantity=2
```
---

## Histórico de versões e cronologia de funcionalidades

### Versão 0.9.10 (2013)

**Funcionalidade**: Suporte a valores vazios em arquivos de configuração - Chaves com valores vazios (`key=`) agora são suportadas - Anteriormente eram ignoradas ou causavam erros de análise

### Versão 0.9.18 (2015)

**Funcionalidade**: Configuração do intervalo de flush (esvaziamento do buffer) do logger - Propriedade: `logger.flushInterval` (padrão de 29 segundos) - Reduz a E/S de disco mantendo uma latência de log aceitável

### Versão 0.9.23 (novembro de 2015)

**Alteração importante**: Java 7 como requisito mínimo - fim do suporte ao Java 6 - necessário para continuar recebendo atualizações de segurança

### Versão 0.9.25 (2015)

**Recursos**: opções de segurança do servidor HTTP - `tunnel.N.option.rejectReferer` - Rejeita conexões com cabeçalho Referer - `tunnel.N.option.rejectUserAgents` - Rejeita cabeçalhos User-Agent específicos - `tunnel.N.option.userAgentRejectList` - Padrões de User-Agent para rejeitar - **Caso de uso**: Mitigar rastreadores e clientes indesejados

### Versão 0.9.33 (janeiro de 2018)

**Recurso**: Filtragem de User-Agent aprimorada - a cadeia "none" em `userAgentRejectList` corresponde a um User-Agent vazio - Correções de bugs adicionais para i2psnark, i2ptunnel, streaming, SusiMail

### Versão 0.9.41 (2019)

**Descontinuação**: Protocolo BOB removido do Android - usuários do Android devem migrar para SAM ou I2CP

### Versão 0.9.42 (agosto de 2019)

**Mudança importante**: Separação dos arquivos de configuração - `clients.config` separado em uma estrutura de diretórios `clients.config.d/` - `i2ptunnel.config` separado em uma estrutura de diretórios `i2ptunnel.config.d/` - Migração automática na primeira execução após a atualização - Permite empacotamento modular e gerenciamento de plugins - O formato monolítico legado ainda é suportado

**Recursos adicionais**: - Melhorias de desempenho do SSU - Prevenção de interconexão entre redes (Proposta 147) - Suporte inicial a tipos de criptografia

### Versão 0.9.56 (2021)

**Funcionalidades**: Melhorias de segurança e de registro em log - `logger.gzip` - Compressão Gzip para logs rotacionados (padrão: false) - `logger.minGzipSize` - Tamanho mínimo para compressão (padrão: 65536 bytes) - `tunnel.N.option.proxy.auth.USER.sha256` - Autenticação digest SHA-256 (RFC 7616) - **Segurança**: SHA-256 substitui MD5 para autenticação digest

### Versão 0.9.57 (janeiro de 2023)

**Recurso**: Configuração do tipo de outproxy SOCKS (proxy de saída) - `tunnel.N.option.outproxyType` - Seleciona o tipo de outproxy (socks|connect) - Padrão: socks - Suporte a HTTPS CONNECT para outproxies HTTPS

### Versão 2.6.0 (julho de 2024)

**Mudança incompatível**: I2P-over-Tor bloqueado - Conexões provenientes de endereços IP de nós de saída do Tor agora são rejeitadas - **Motivo**: Degrada o desempenho do I2P, desperdiça recursos dos nós de saída do Tor - **Impacto**: Usuários que acessarem o I2P por meio de nós de saída do Tor serão bloqueados - Nós retransmissores não de saída e clientes Tor não são afetados

### Versão 2.10.0 (setembro de 2025 - atual)

**Principais recursos**: - **Criptografia pós-quântica** disponível (ativação opcional via Hidden Service Manager) - **Suporte a tracker UDP** para o I2PSnark para reduzir a carga do tracker - **Estabilidade do Modo Oculto** melhorias para reduzir o esgotamento de RouterInfo - Melhorias de rede para routers congestionados - Atravessamento UPnP/NAT aprimorado - Melhorias no NetDB com remoção agressiva de leaseset - Reduções de observabilidade para eventos do router

**Configuração**: Nenhuma nova propriedade de configuração foi adicionada

**Alteração crítica iminente**: A próxima versão (provavelmente 2.11.0 ou 3.0.0) exigirá Java 17 ou posterior

---

## Funcionalidades obsoletas e alterações incompatíveis

### Descontinuações Críticas

#### Acesso ao I2P-over-Tor (Versão 2.6.0+)

- **Status**: BLOQUEADO desde julho de 2024
- **Impacto**: Conexões provenientes de IPs de nós de saída do Tor rejeitadas
- **Motivo**: Prejudica o desempenho da rede I2P sem fornecer benefícios de anonimato
- **Afeta**: Apenas nós de saída do Tor, não nós de retransmissão nem clientes comuns do Tor
- **Alternativa**: Use I2P ou Tor separadamente, não em conjunto

#### Autenticação Digest MD5

- **Status**: Obsoleto (use SHA-256)
- **Property**: `tunnel.N.option.proxy.auth.USER.md5`
- **Reason**: MD5 criptograficamente quebrado
- **Replacement**: `tunnel.N.option.proxy.auth.USER.sha256` (desde 0.9.56)
- **Timeline**: MD5 ainda é suportado, mas desaconselhado

### Alterações na Arquitetura de Configuração

#### Arquivos de Configuração Monolíticos (Versão 0.9.42+)

- **Afetados**: `clients.config`, `i2ptunnel.config`
- **Status**: Descontinuado em favor de uma estrutura de diretórios separada
- **Migração**: Automática na primeira execução após a atualização para a versão 0.9.42
- **Compatibilidade**: O formato legado ainda funciona (compatível com versões anteriores)
- **Recomendação**: Use o formato separado para novas configurações

### Requisitos de versão do Java

#### Suporte ao Java 6

- **Encerrada**: Versão 0.9.23 (novembro de 2015)
- **Mínimo**: Java 7 necessário desde 0.9.23

#### Requisito do Java 17 (Em breve)

- **Status**: MUDANÇA CRÍTICA IMINENTE
- **Alvo**: Próxima versão principal após 2.10.0 (provavelmente 2.11.0 ou 3.0.0)
- **Mínimo atual**: Java 8
- **Ação necessária**: Preparar-se para a migração para o Java 17
- **Cronograma**: A ser anunciado com as notas de versão

### Funcionalidades removidas

#### Protocolo BOB (Android)

- **Removido**: Versão 0.9.41
- **Plataforma**: Somente Android
- **Alternativa**: protocolos SAM ou I2CP
- **Desktop**: BOB (ponte básica do I2P) ainda está disponível em plataformas desktop

### Migrações recomendadas

1. **Autenticação**: Migrar de MD5 para autenticação digest com SHA-256
2. **Formato de Configuração**: Migrar para estrutura de diretórios separada para clientes e tunnels
3. **Ambiente de Execução Java**: Planejar a atualização para Java 17 antes da próxima versão principal
4. **Integração com Tor**: Não rotear o I2P por meio de nós de saída do Tor

---

## Referências

### Documentação oficial

- [Especificação de Configuração do I2P](/docs/specs/configuration/) - Especificação oficial do formato de arquivo de configuração
- [Especificação de Plugin do I2P](/docs/specs/plugin/) - Configuração e empacotamento de plugins
- [Estruturas Comuns do I2P - Mapeamento de Tipos](/docs/specs/common-structures/#type-mapping) - Formato de serialização de dados do protocolo
- [Formato de Propriedades do Java](http://docs.oracle.com/javase/1.5.0/docs/api/java/util/Properties.html#load%28java.io.InputStream%29) - Especificação do formato base

### Código-fonte

- [Repositório do I2P Java Router](https://github.com/i2p/i2p.i2p) - Espelho no GitHub
- [Gitea dos Desenvolvedores do I2P](https://i2pgit.org/I2P_Developers/i2p.i2p) - Repositório oficial do código-fonte do I2P
- [DataHelper.java](https://github.com/i2p/i2p.i2p/blob/master/core/java/src/net/i2p/data/DataHelper.java) - Implementação de E/S (entrada/saída) de arquivo de configuração

### Recursos da comunidade

- [Fórum I2P](https://i2pforum.net/) - Discussões ativas da comunidade e suporte
- [Site do I2P](/) - Site oficial do projeto

### Documentação da API

- [DataHelper JavaDoc](https://i2pplus.github.io/javadoc/net/i2p/data/DataHelper.html) - Documentação da API para métodos de arquivos de configuração

### Status da Especificação

- **Última atualização da especificação**: Janeiro de 2023 (Versão 0.9.57)
- **Versão atual do I2P**: 2.10.0 (Setembro de 2025)
- **Precisão técnica**: A especificação permanece precisa até a versão 2.10.0 (sem alterações incompatíveis)
- **Manutenção**: Documento vivo atualizado quando o formato de configuração é modificado
