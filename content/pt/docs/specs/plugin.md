---
title: "Formato do Pacote de Plugin"
description: "Regras de empacotamento em .xpi2p / .su3 para plugins do I2P"
slug: "plugin"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## Visão geral

Os plugins do I2P são arquivos assinados que ampliam a funcionalidade do router. Eles são distribuídos como arquivos `.xpi2p` ou `.su3`, instalam-se em `~/.i2p/plugins/<name>/` (ou `%APPDIR%\I2P\plugins\<name>\` no Windows) e executam com permissões completas do router, sem sandboxing (sem ambiente de isolamento).

### Tipos de plugins suportados

- Aplicativos web do Console
- Novos eepsites com cgi-bin, aplicativos web
- Temas do Console
- Traduções do Console
- Programas Java (no mesmo processo ou em uma JVM separada)
- Scripts de shell e binários nativos

### Modelo de Segurança

**CRÍTICO:** Plugins são executados na mesma JVM (Máquina Virtual Java) com permissões idênticas às do I2P router. Têm acesso irrestrito a: - Sistema de arquivos (leitura e escrita) - APIs do router e estado interno - Conexões de rede - Execução de programas externos

Plugins devem ser tratados como código de total confiança. Os usuários devem verificar as origens e as assinaturas dos plugins antes da instalação.

---

## Formatos de arquivo

### Formato SU3 (Altamente recomendado)

**Status:** Ativo, formato preferido desde o I2P 0.9.15 (setembro de 2014)

O formato `.su3` oferece: - **chaves de assinatura RSA-4096** (vs. DSA-1024 em xpi2p) - Assinatura armazenada no cabeçalho do arquivo - Número mágico: `I2Psu3` - Melhor compatibilidade futura

**Estrutura:**

```
[SU3 Header with RSA-4096 signature]
[ZIP Archive]
  ├── plugin.config (required)
  ├── console/
  ├── lib/
  ├── webapps/
  └── [other plugin files]
```
### Formato XPI2P (Legado, Obsoleto)

**Status:** Suportado para compatibilidade com versões anteriores, não recomendado para novos plugins

O formato `.xpi2p` usa assinaturas criptográficas mais antigas: - **Assinaturas DSA-1024** (obsoletas segundo a NIST-800-57) - Assinatura DSA de 40 bytes anteposta ao ZIP - Requer o campo `key` em plugin.config

**Estrutura:**

```
[40-byte DSA signature]
[16-byte version string (UTF-8, zero-padded)]
[ZIP Archive]
```
**Caminho de migração:** Ao migrar de xpi2p para su3, forneça tanto `updateURL` quanto `updateURL.su3` durante a transição. Os routers modernos (0.9.15+) priorizam automaticamente SU3.

---

## Estrutura do arquivo e plugin.config

### Arquivos necessários

**plugin.config** - Arquivo de configuração padrão do I2P com pares chave-valor

### Propriedades obrigatórias

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Property</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Format</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>name</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Installation directory name, must match for updates</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Alphanumeric, no spaces</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>signer</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Developer contact information</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>user@mail.i2p</code> format recommended</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>version</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Plugin version for update comparison</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Max 16 bytes, parsed by VersionComparator</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>key</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA public key (172 B64 chars ending with '=')</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Omit for SU3 format</strong></td></tr>
  </tbody>
</table>
**Exemplos de formato de versão:** - `1.2.3` - `1.2.3-4` - `2.0.0-beta.1`

Separadores válidos: `.` (ponto), `-` (hífen), `_` (sublinhado)

### Propriedades de Metadados Opcionais

#### Informações de exibição

- `date` - Data de lançamento (carimbo de data/hora long do Java)
- `author` - Nome do desenvolvedor (recomendado `user@mail.i2p`)
- `description` - Descrição em inglês
- `description_xx` - Descrição localizada (xx = código de idioma)
- `websiteURL` - Página inicial do plugin (`http://foo.i2p/`)
- `license` - Identificador da licença (por exemplo, "Apache-2.0", "GPL-3.0")

#### Configuração de Atualização

- `updateURL` - Local de atualização do XPI2P (legado)
- `updateURL.su3` - Local de atualização do SU3 (preferido)
- `min-i2p-version` - Versão mínima do I2P exigida
- `max-i2p-version` - Versão máxima do I2P compatível
- `min-java-version` - Versão mínima do Java (por exemplo, `1.7`, `17`)
- `min-jetty-version` - Versão mínima do Jetty (use `6` para Jetty 6+)
- `max-jetty-version` - Versão máxima do Jetty (use `5.99999` para Jetty 5)

#### Comportamento da Instalação

- `dont-start-at-install` - Padrão `false`. Se `true`, exige início manual
- `router-restart-required` - Padrão `false`. Informa ao usuário que é necessário reiniciar após a atualização
- `update-only` - Padrão `false`. Falha se o plugin ainda não estiver instalado
- `install-only` - Padrão `false`. Falha se o plugin já estiver instalado
- `min-installed-version` - Versão mínima necessária para a atualização
- `max-installed-version` - Versão máxima que pode ser atualizada
- `disableStop` - Padrão `false`. Oculta o botão de parar se `true`

#### Integração com o Console

- `consoleLinkName` - Texto para o link da barra de resumo do console
- `consoleLinkName_xx` - Texto do link localizado (xx = código de idioma)
- `consoleLinkURL` - Destino do link (por exemplo, `/appname/index.jsp`)
- `consoleLinkTooltip` - Texto exibido ao passar o mouse (suportado desde 0.7.12-6)
- `consoleLinkTooltip_xx` - Dica de ferramenta localizada
- `console-icon` - Caminho para o ícone de 32x32 (suportado desde 0.9.20)
- `icon-code` - PNG 32x32 codificado em Base64 para plugins sem recursos web (desde 0.9.25)

#### Requisitos de Plataforma (somente exibição)

- `required-platform-OS` - Requisito do sistema operacional (não imposto)
- `other-requirements` - Requisitos adicionais (por exemplo, "Python 3.8+")

#### Gerenciamento de dependências (Não implementado)

- `depends` - Dependências do plugin, separadas por vírgulas
- `depends-version` - Requisitos de versão para as dependências
- `langs` - Conteúdo do pacote de idiomas
- `type` - Tipo de plugin (app/theme/locale/webapp)

### Substituição de variáveis na URL de atualização

**Estado da funcionalidade:** Disponível desde I2P 1.7.0 (0.9.53)

Tanto `updateURL` quanto `updateURL.su3` suportam variáveis específicas da plataforma:

**Variáveis:** - `$OS` - Sistema operacional: `windows`, `linux`, `mac` - `$ARCH` - Arquitetura: `386`, `amd64`, `arm64`

**Exemplo:**

```properties
updateURL.su3=http://foo.i2p/downloads/foo-$OS-$ARCH.su3
```
**Resultado no Windows AMD64:**

```
http://foo.i2p/downloads/foo-windows-amd64.su3
```
Isso permite um único arquivo plugin.config para compilações específicas da plataforma.

---

## Estrutura de diretórios

### Layout padrão

```
plugins/
└── pluginname/
    ├── plugin.config (required)
    ├── console/
    │   ├── locale/          # Translation JARs
    │   ├── themes/          # Console themes
    │   ├── webapps/         # Web applications
    │   └── webapps.config   # Webapp configuration
    ├── eepsite/
    │   ├── cgi-bin/
    │   ├── docroot/
    │   ├── logs/
    │   ├── webapps/
    │   └── jetty.xml
    ├── lib/
    │   └── *.jar            # Plugin libraries
    └── clients.config       # Client startup configuration
```
### Finalidades do Diretório

**console/locale/** - Arquivos JAR com conjuntos de recursos para as traduções básicas do I2P - As traduções específicas de plugins devem estar em `console/webapps/*.war` ou `lib/*.jar`

**console/themes/** - Cada subdiretório contém um tema completo do console - Adicionado automaticamente ao caminho de busca de temas

**console/webapps/** - arquivos `.war` para integração com o console - Iniciados automaticamente, a menos que desativados em `webapps.config` - O nome do WAR não precisa corresponder ao nome do plugin

**eepsite/** - eepsite completo com sua própria instância do Jetty - Requer configuração de `jetty.xml` com substituição de variáveis - Veja exemplos de zzzot e do plugin pebble

**lib/** - Bibliotecas JAR de plug-ins - Especifique no classpath via `clients.config` ou `webapps.config`

---

## Configuração do aplicativo web

### Formato de webapps.config

Arquivo de configuração padrão do I2P que controla o comportamento do aplicativo web.

**Sintaxe:**

```properties
# Disable autostart
webapps.warname.startOnLoad=false

# Add classpath JARs (as of API 0.9.53, works for any warname)
webapps.warname.classpath=$PLUGIN/lib/foo.jar,$I2P/lib/bar.jar
```
**Notas importantes:** - Antes do router 0.7.12-9, use `plugin.warname.startOnLoad` para compatibilidade - Antes da API 0.9.53, classpath só funcionava se o warname (nome do WAR) correspondesse ao nome do plugin - A partir da 0.9.53+, classpath funciona para qualquer nome de webapp (aplicativo web)

### Boas práticas para aplicações web

1. **Implementação de ServletContextListener**
   - Implemente `javax.servlet.ServletContextListener` para limpeza
   - Ou sobrescreva `destroy()` no servlet
   - Garante o encerramento adequado durante atualizações e a parada do router

2. **Gerenciamento de Bibliotecas**
   - Coloque JARs compartilhados em `lib/`, não dentro do WAR
   - Referencie pelo classpath em `webapps.config`
   - Permite a instalação/atualização separada de plugins

3. **Evite bibliotecas conflitantes**
   - Nunca empacote Jetty, Tomcat ou JARs de servlet
   - Nunca empacote JARs da instalação padrão do I2P
   - Verifique a seção classpath para bibliotecas padrão

4. **Requisitos de Compilação**
   - Não incluir arquivos de código-fonte `.java` ou `.jsp`
   - Pré-compilar todas as JSPs para evitar atrasos na inicialização
   - Não se pode presumir a disponibilidade de um compilador Java/JSP

5. **Compatibilidade com a Servlet API**
   - O I2P suporta Servlet 3.0 (desde 0.9.30)
   - **Varredura de anotações NÃO é suportada** (@WebContent)
   - É necessário fornecer o descritor de implantação tradicional `web.xml`

6. **Versão do Jetty**
   - Atual: Jetty 9 (I2P 0.9.30+)
   - Use `net.i2p.jetty.JettyStart` como camada de abstração
   - Protege contra alterações na API do Jetty

---

## Configuração do Cliente

### Formato de clients.config

Define os clientes (serviços) iniciados com o plugin.

**Cliente básico:**

```properties
clientApp.0.main=com.example.PluginMain
clientApp.0.name=Example Plugin Service
clientApp.0.delay=30
clientApp.0.args=arg1 arg2 $PLUGIN/config.properties
```
**Cliente com Parar/Desinstalar:**

```properties
clientApp.0.stopargs=stop
clientApp.0.uninstallargs=uninstall
clientApp.0.classpath=$PLUGIN/lib/plugin.jar,$I2P/lib/i2p.jar
```
### Referência de Propriedades

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Property</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>main</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Fully qualified class name implementing ClientApp interface</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>name</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Display name for user interface</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>delay</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Startup delay in seconds (default: 0)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>args</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Space-separated arguments passed to constructor</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>stopargs</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Arguments for shutdown (must handle gracefully)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>uninstallargs</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Arguments called before plugin deletion</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>classpath</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Comma-separated JAR paths</td></tr>
  </tbody>
</table>
### Substituição de Variáveis

As seguintes variáveis são substituídas em `args`, `stopargs`, `uninstallargs` e `classpath`:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Variable</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Replacement</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$I2P</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2P base installation directory</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$CONFIG</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2P configuration directory (typically <code>~/.i2p</code>)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$PLUGIN</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">This plugin's directory (<code>$CONFIG/plugins/name</code>)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$OS</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Operating system: <code>windows</code>, <code>linux</code>, <code>mac</code></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$ARCH</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Architecture: <code>386</code>, <code>amd64</code>, <code>arm64</code></td></tr>
  </tbody>
</table>
### Clientes Gerenciados vs. Não Gerenciados

**Clientes gerenciados (Recomendados, desde 0.9.4):** - Instanciados por ClientAppManager - Mantêm rastreamento de referências e de estado - Gerenciamento do ciclo de vida mais fácil - Melhor gerenciamento de memória

**Clientes não gerenciados:** - Iniciados pelo router, sem rastreamento de estado - Devem lidar de forma adequada com múltiplas chamadas de início/parada - Use estado estático ou arquivos PID para coordenação - Chamados no desligamento do router (a partir da versão 0.7.12-3)

### ShellService (desde 0.9.53 / 1.7.0)

Solução generalizada para executar programas externos com rastreamento automático de estado.

**Recursos:** - Gerencia o ciclo de vida do processo - Comunica-se com o ClientAppManager - Gerenciamento automático de PID - Suporte multiplataforma

**Uso:**

```properties
clientApp.0.main=net.i2p.apps.ShellService
clientApp.0.args=$PLUGIN/bin/myservice.sh
```
Para scripts específicos da plataforma:

```properties
clientApp.0.args=$PLUGIN/bin/myservice-$OS.$ARCH
```
**Alternativa (legado):** Escreva um wrapper (camada de encapsulamento) em Java que verifique o tipo de sistema operacional e chame `ShellCommand` com o arquivo `.bat` ou `.sh` apropriado.

---

## Processo de Instalação

### Fluxo de Instalação do Usuário

1. O usuário cola a URL do plugin na Página de Configuração de Plugins do Console do Router (`/configplugins`)
2. O Router faz o download do arquivo do plugin
3. Verificação da assinatura (falha se a chave for desconhecida e o modo estrito estiver ativado)
4. Verificação de integridade do ZIP
5. Extrair e analisar `plugin.config`
6. Verificação de compatibilidade de versão (`min-i2p-version`, `min-java-version`, etc.)
7. Detecção de conflito de nome de aplicação web
8. Parar o plugin existente em caso de atualização
9. Validação do diretório (deve estar sob `plugins/`)
10. Extrair todos os arquivos para o diretório do plugin
11. Atualizar `plugins.config`
12. Iniciar o plugin (a menos que `dont-start-at-install=true`)

### Segurança e Confiança

**Gerenciamento de chaves:** - Modelo de confiança First-key-seen (primeira chave vista) para novos signatários - Apenas as chaves de jrandom e zzz vêm pré-incluídas - A partir da 0.9.14.1, chaves desconhecidas são rejeitadas por padrão - Uma propriedade avançada pode sobrescrever para desenvolvimento

**Restrições de Instalação:** - Arquivos compactados devem ser extraídos apenas no diretório do plugin - O instalador rejeita caminhos fora de `plugins/` - Os plugins podem acessar arquivos em outros locais após a instalação - Sem sandboxing (ambiente isolado) ou isolamento de privilégios

---

## Mecanismo de Atualização

### Processo de verificação de atualizações

1. Router lê `updateURL.su3` (preferido) ou `updateURL` de plugin.config
2. Solicitação HTTP HEAD ou GET parcial para obter os bytes 41-56
3. Extrair a string de versão do arquivo remoto
4. Comparar com a versão instalada usando VersionComparator
5. Se for mais recente, solicitar ao usuário ou baixar automaticamente (com base nas configurações)
6. Parar o plugin
7. Instalar a atualização
8. Iniciar o plugin (a menos que a preferência do usuário tenha sido alterada)

### Comparação de versões

Versões interpretadas como componentes separados por ponto/hífen/sublinhado: - `1.2.3` < `1.2.4` - `1.2.3` < `1.2.3-1` - `2.0.0` > `1.9.9`

**Comprimento máximo:** 16 bytes (deve corresponder ao cabeçalho SUD/SU3)

### Boas práticas de atualização

1. Sempre incremente a versão a cada lançamento
2. Teste o caminho de atualização a partir da versão anterior
3. Considere `router-restart-required` para alterações importantes
4. Forneça tanto `updateURL` quanto `updateURL.su3` durante a migração
5. Use o sufixo do número de compilação para testes (`1.2.3-456`)

---

## Classpath (caminho de classes) e Bibliotecas Padrão

### Sempre disponível no Classpath

Os seguintes arquivos JAR de `$I2P/lib` estão sempre no classpath no I2P 0.9.30+:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">JAR</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Plugin Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Core API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Required for all plugins</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>mstreaming.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Streaming API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins need</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>streaming.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Streaming implementation</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins need</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2ptunnel.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">I2PTunnel</td><td style="border:1px solid var(--color-border); padding:0.6rem;">HTTP/server plugins</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>router.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Router internals</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Rarely needed, avoid if possible</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>javax.servlet.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Servlet 3.1, JSP 2.3 API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins with servlets/JSPs</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>jasper-runtime.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Jasper compiler/runtime</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins with JSPs</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>commons-el.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">EL 3.0 API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">JSPs using expression language</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>jetty-i2p.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Jetty utilities</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins starting Jetty</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>org.mortbay.jetty.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Jetty 9 base</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Custom Jetty instances</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>sam.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">SAM API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Rarely needed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>addressbook.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Subscription/blockfile</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Use NamingService instead</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>routerconsole.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Console libraries</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Not public API, avoid</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>jbigi.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Native crypto</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins should not need</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>systray.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">URL launcher</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Rarely needed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>wrapper.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Service wrapper</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins should not need</td></tr>
  </tbody>
</table>
### Notas especiais

**commons-logging.jar:** - Vazio desde 0.9.30 - Antes da 0.9.30: Apache Tomcat JULI (implementação do java.util.logging do Tomcat) - Antes da 0.9.24: Commons Logging (biblioteca Apache Commons Logging) + JULI - Antes da 0.9: Apenas Commons Logging

**jasper-compiler.jar:** - Vazio desde o Jetty 6 (0.9)

**systray4j.jar:** - Removido na versão 0.9.26

### Não está no Classpath (é necessário especificar)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">JAR</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>jstl.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Standard Taglib</td><td style="border:1px solid var(--color-border); padding:0.6rem;">JSP tag libraries</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>standard.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Standard Taglib</td><td style="border:1px solid var(--color-border); padding:0.6rem;">JSP tag libraries</td></tr>
  </tbody>
</table>
### Especificação do Classpath (lista de caminhos de classes do Java)

**Em clients.config:**

```properties
clientApp.0.classpath=$PLUGIN/lib/mylib.jar,$I2P/lib/i2p.jar
```
**Em webapps.config:**

```properties
webapps.mywebapp.classpath=$PLUGIN/lib/mylib.jar,$I2P/lib/jstl.jar
```
**Importante:** A partir da 0.7.13-3, os classpaths (lista de caminhos de classes) são específicos a cada thread, não em toda a JVM. Especifique o classpath completo para cada cliente.

---

## Requisitos de versão do Java

### Requisitos atuais (outubro de 2025)

**I2P 2.10.0 e anteriores:** - Mínimo: Java 7 (necessário desde 0.9.24, janeiro de 2016) - Recomendado: Java 8 ou superior

**I2P 2.11.0 e posteriores (EM BREVE):** - **Mínimo: Java 17+** (anunciado nas notas de lançamento da versão 2.9.0) - Aviso prévio de duas versões emitido (2.9.0 → 2.10.0 → 2.11.0)

### Estratégia de compatibilidade de plugins

**Para máxima compatibilidade (até o I2P 2.10.x):**

```xml
<javac source="1.7" target="1.7" />
```
```properties
min-java-version=1.7
```
**Para recursos do Java 8+:**

```xml
<javac source="1.8" target="1.8" />
```
```properties
min-java-version=1.8
```
**Para recursos do Java 11+:**

```xml
<javac source="11" target="11" />
```
```properties
min-java-version=11
```
**Preparando-se para 2.11.0+:**

```xml
<javac source="17" target="17" />
```
```properties
min-java-version=17
min-i2p-version=2.11.0
```
### Boas práticas de compilação

**Ao compilar com um JDK mais recente para uma versão de destino mais antiga:**

```xml
<javac source="1.7" target="1.7" 
       bootclasspath="${java7.home}/jre/lib/rt.jar"
       includeantruntime="false" />
```
Isso impede o uso de APIs que não estão disponíveis na versão de destino do Java.

---

## Compressão Pack200 - OBSOLETA

### Atualização crítica: Não use Pack200 (formato de compactação do Java)

**Estado:** OBSOLETO E REMOVIDO

A especificação original recomendava fortemente a compressão Pack200 (método de compressão do Java) para uma redução de tamanho de 60-65%. **Isso não é mais válido.**

**Linha do tempo:** - **JEP 336:** Pack200 marcado como obsoleto no Java 11 (setembro de 2018) - **JEP 367:** Pack200 removido no Java 14 (março de 2020)

**A especificação oficial de atualizações do I2P afirma:** > "Arquivos JAR e WAR no arquivo ZIP não são mais compactados com o pack200 (ferramenta de compactação do Java), conforme documentado acima para arquivos 'su2', porque os ambientes de execução Java recentes não o suportam mais."

**O que fazer:**

1. **Remova o pack200 dos processos de compilação imediatamente**
2. **Use a compressão ZIP padrão**
3. **Considere alternativas:**
   - ProGuard/R8 para redução de código
   - UPX para binários nativos
   - Algoritmos de compressão modernos (zstd, brotli) se for fornecido um descompactador personalizado

**Para plugins existentes:** - routers antigos (0.7.11-5 até o Java 10) ainda podem descompactar pack200 - routers novos (Java 11+) não podem descompactar pack200 - Relançar plugins sem compressão pack200

---

## Chaves de Assinatura e Segurança

### Geração de chaves (Formato SU3)

Use o script `makeplugin.sh` do repositório i2p.scripts:

```bash
# Generate new signing key
./makeplugin.sh keygen

# Keys stored in ~/.i2p-plugin-keys/
```
**Principais detalhes:** - Algoritmo: RSA_SHA512_4096 - Formato: certificado X.509 - Armazenamento: formato de keystore do Java

### Assinando plugins

```bash
# Create signed su3 file
./makeplugin.sh sign myplugin.zip myplugin.su3 keyname

# Verify signature
./makeplugin.sh verify myplugin.su3
```
### Boas práticas de gerenciamento de chaves

1. **Gere uma vez, proteja para sempre**
   - Routers rejeitam nomes de chave duplicados com chaves diferentes
   - Routers rejeitam chaves duplicadas com nomes de chave diferentes
   - Atualizações são rejeitadas se houver incompatibilidade entre chave e nome

2. **Armazenamento seguro**
   - Fazer backup do keystore (repositório de chaves) com segurança
   - Usar uma frase-senha forte
   - Nunca fazer commit no controle de versão

3. **Rotação de chaves**
   - Não é suportado pela arquitetura atual
   - Planeje o uso de chaves a longo prazo
   - Considere esquemas de multiassinatura para desenvolvimento em equipe

### Assinatura DSA legada (XPI2P)

**Estado:** Funcional, mas obsoleto

Assinaturas DSA-1024 usadas pelo formato xpi2p: - assinatura de 40 bytes - chave pública de 172 caracteres em base64 - NIST-800-57 recomenda (L=2048, N=224) no mínimo - o I2P usa parâmetros mais fracos (L=1024, N=160)

**Recomendação:** Use SU3 com RSA-4096 em vez disso.

---

## Diretrizes de Desenvolvimento de Plugins

### Boas Práticas Essenciais

1. **Documentação**
   - Fornecer um README claro com instruções de instalação
   - Documentar as opções de configuração e os valores padrão
   - Incluir um registro de alterações em cada versão
   - Especificar as versões requeridas de I2P/Java

2. **Otimização do tamanho**
   - Incluir apenas os arquivos necessários
   - Nunca empacote os JARs do router
   - Separe pacotes de instalação vs. atualização (bibliotecas em lib/)
   - ~~Use a compactação Pack200~~ **OBSOLETO - Use ZIP padrão**

3. **Configuração**
   - Nunca modifique `plugin.config` em tempo de execução
   - Use um arquivo de configuração separado para configurações de tempo de execução
   - Documente as configurações necessárias do router (portas SAM, tunnels, etc.)
   - Respeite a configuração existente do usuário

4. **Uso de recursos**
   - Evite consumo agressivo de largura de banda por padrão
   - Implemente limites razoáveis para o uso de CPU
   - Libere recursos no encerramento
   - Use daemon threads (threads em segundo plano que não impedem o encerramento do processo) quando apropriado

5. **Testes**
   - Testar instalação/atualização/desinstalação em todas as plataformas
   - Testar atualizações a partir da versão anterior
   - Verificar interrupção/reinício da aplicação web durante as atualizações
   - Testar com a versão mínima suportada do I2P

6. **Sistema de arquivos**
   - Nunca escreva em `$I2P` (pode ser somente leitura)
   - Grave dados em tempo de execução em `$PLUGIN` ou `$CONFIG`
   - Use `I2PAppContext` para descoberta de diretórios
   - Não presuma a localização de `$CWD`

7. **Compatibilidade**
   - Não duplique classes padrão do I2P
   - Estenda classes se necessário, não as substitua
   - Verifique `min-i2p-version`, `min-jetty-version` em plugin.config
   - Teste com versões mais antigas do I2P se pretende suportá-las

8. **Tratamento do encerramento**
   - Implementar `stopargs` adequados em clients.config
   - Registrar ganchos de encerramento: `I2PAppContext.addShutdownTask()`
   - Lidar com múltiplas chamadas de iniciar/parar de forma adequada
   - Definir todas as threads para o modo daemon (processo em segundo plano)

9. **Segurança**
   - Valide toda a entrada externa
   - Nunca chame `System.exit()`
   - Respeite a privacidade do usuário
   - Siga práticas de codificação segura

10. **Licenciamento**
    - Especifique claramente a licença do plugin
    - Respeite as licenças das bibliotecas incluídas
    - Inclua os créditos exigidos
    - Forneça acesso ao código-fonte, se exigido

### Considerações avançadas

**Tratamento de fuso horário:** - Router configura o fuso horário da JVM para UTC - Fuso horário real do usuário: propriedade `i2p.systemTimeZone` de `I2PAppContext`

**Descoberta de diretório:**

```java
// Plugin directory
String pluginDir = I2PAppContext.getGlobalContext()
    .getAppDir().getAbsolutePath() + "/plugins/" + pluginName;

// Or use $PLUGIN variable in clients.config args
```
**Numeração de versão:** - Use versionamento semântico (major.minor.patch) - Adicione número de build (compilação) para testes (1.2.3-456) - Garanta aumento monotônico nas atualizações

**Acesso às classes do router:** - De modo geral, evite dependências de `router.jar` - Use as APIs públicas em `i2p.jar` em vez disso - Versões futuras do I2P podem restringir o acesso às classes do router

**Prevenção de falhas da JVM (Histórico):** - Corrigido na versão 0.7.13-3 - Use os carregadores de classes corretamente - Evite atualizar JARs em plugin em execução - Projete para reinicialização na atualização, se necessário

---

## Plugins do Eepsite

### Visão geral

Plugins podem fornecer eepsites completos com suas próprias instâncias do Jetty (servidor web Java) e do I2PTunnel.

### Arquitetura

**Não tente:** - Instalar em um eepsite existente - Mesclar com o eepsite padrão do router - Assumir a disponibilidade de um único eepsite

**Em vez disso:** - Iniciar uma nova instância do I2PTunnel (via CLI) - Iniciar uma nova instância do Jetty - Configurar ambos em `clients.config`

### Estrutura de exemplo

```
plugins/myeepsite/
├── plugin.config
├── clients.config          # Starts Jetty + I2PTunnel
├── eepsite/
│   ├── jetty.xml          # Requires variable substitution
│   ├── docroot/
│   ├── webapps/
│   └── logs/
└── lib/
    └── [dependencies]
```
### Substituição de variáveis em jetty.xml

Use a variável `$PLUGIN` para caminhos:

```xml
<Set name="resourceBase">$PLUGIN/eepsite/docroot</Set>
```
O Router realiza substituições durante a inicialização do plugin.

### Exemplos

Implementações de referência: - **zzzot plugin** - Rastreador de torrents - **pebble plugin** - Plataforma de blog

Ambos disponíveis na página de plugins do zzz (interna ao I2P).

---

## Integração com o Console

### Links da Barra de Resumo

Adicionar link clicável à barra de resumo do console do router:

```properties
consoleLinkName=My Plugin
consoleLinkURL=/myplugin/
consoleLinkTooltip=Open My Plugin Interface
```
Versões localizadas:

```properties
consoleLinkName_de=Mein Plugin
consoleLinkTooltip_de=Öffne Mein Plugin Schnittstelle
```
### Ícones do Console

**Arquivo de imagem (desde 0.9.20):**

```properties
console-icon=/myicon.png
```
Caminho relativo a `consoleLinkURL`, se especificado (desde 0.9.53); caso contrário, relativo ao nome da aplicação web.

**Ícone incorporado (desde 0.9.25):**

```properties
icon-code=iVBORw0KGgoAAAANSUhEUgAAA...Base64EncodedPNG...
```
Gerar com:

```bash
base64 -w 0 icon-32x32.png
```
Ou Java:

```bash
java -cp i2p.jar net.i2p.data.Base64 encode icon.png
```
Requisitos: - 32x32 pixels - formato PNG - codificado em Base64 (sem quebras de linha)

---

## Internacionalização

### Pacotes de Tradução

**Para traduções básicas do I2P:** - Coloque os JARs em `console/locale/` - Contêm pacotes de recursos para os aplicativos I2P existentes - Nomenclatura: `messages_xx.properties` (xx = código do idioma)

**Para traduções específicas de plugins:** - Inclua em `console/webapps/*.war` - Ou inclua em `lib/*.jar` - Use a abordagem padrão do Java ResourceBundle (conjunto de recursos do Java)

### Strings localizadas no plugin.config

```properties
description=My awesome plugin
description_de=Mein tolles Plugin
description_fr=Mon plugin génial
description_es=Mi plugin increíble
```
Campos suportados: - `description_xx` - `consoleLinkName_xx` - `consoleLinkTooltip_xx`

### Tradução do Tema do Console

Temas em `console/themes/` são adicionados automaticamente ao caminho de pesquisa de temas.

---

## Plugins específicos da plataforma

### Abordagem de Pacotes Separados

Use nomes de plug-in diferentes para cada plataforma:

```properties
# Windows package
name=myplugin-windows

# Linux package  
name=myplugin-linux

# macOS package
name=myplugin-mac
```
### Abordagem de Substituição de Variáveis

Único plugin.config com variáveis de plataforma:

```properties
name=myplugin
updateURL.su3=http://myplugin.i2p/downloads/myplugin-$OS-$ARCH.su3
```
Em clients.config:

```properties
clientApp.0.main=net.i2p.apps.ShellService
clientApp.0.args=$PLUGIN/bin/myapp-$OS-$ARCH
```
### Detecção do sistema operacional em tempo de execução

Abordagem em Java para execução condicional:

```java
String os = System.getProperty("os.name").toLowerCase();
if (os.contains("win")) {
    // Windows-specific code
} else if (os.contains("nix") || os.contains("nux")) {
    // Linux-specific code
} else if (os.contains("mac")) {
    // macOS-specific code
}
```
---

## Solução de problemas

### Problemas Comuns

**O plugin não inicia:** 1. Verifique a compatibilidade com a versão do I2P (`min-i2p-version`) 2. Verifique a versão do Java (`min-java-version`) 3. Verifique os logs do router em busca de erros 4. Verifique se todos os JARs necessários estão no classpath

**Webapp Não Acessível:** 1. Confirme que `webapps.config` não o desativa 2. Verifique a compatibilidade da versão do Jetty (`min-jetty-version`) 3. Verifique se `web.xml` está presente (a varredura de anotações não é suportada) 4. Verifique se há nomes de webapps conflitantes

**Falhas na atualização:** 1. Verifique se o número da versão foi incrementado 2. Verifique se a assinatura corresponde à chave de assinatura 3. Certifique-se de que o nome do plugin corresponda à versão instalada 4. Revise as configurações de `update-only`/`install-only`

**Programa externo não encerra:** 1. Use ShellService para gerenciamento automático do ciclo de vida 2. Implemente o tratamento adequado de `stopargs` 3. Verifique a limpeza do arquivo PID 4. Verifique o encerramento do processo

### Registro de depuração

Ativar o log de depuração no router:

```
logger.record.net.i2p.router.web.ConfigPluginsHandler=DEBUG
```
Verifique os logs:

```
~/.i2p/logs/log-router-0.txt
```
---

## Informações de referência

### Especificações oficiais

- [Especificação do Plugin](/docs/specs/plugin/)
- [Formato de Configuração](/docs/specs/configuration/)
- [Especificação de Atualização](/docs/specs/updates/)
- [Criptografia](/docs/specs/cryptography/)

### Histórico de versões do I2P

**Versão atual:** - **I2P 2.10.0** (8 de setembro de 2025)

**Principais lançamentos desde 0.9.53:** - 2.10.0 (set 2025) - anúncio do Java 17+ - 2.9.0 (jun 2025) - aviso sobre o Java 17+ - 2.8.0 (out 2024) - testes de criptografia pós-quântica - 2.6.0 (mai 2024) - bloqueio de I2P-over-Tor (I2P através do Tor) - 2.4.0 (dez 2023) - melhorias de segurança no NetDB (banco de dados da rede) - 2.2.0 (mar 2023) - controle de congestionamento - 2.1.0 (jan 2023) - melhorias de rede - 2.0.0 (nov 2022) - protocolo de transporte SSU2 - 1.7.0/0.9.53 (fev 2022) - ShellService (serviço de shell), substituição de variáveis - 0.9.15 (set 2014) - introdução do formato SU3

**Numeração de versões:** - série 0.9.x: até a versão 0.9.53 - série 2.x: a partir da 2.0.0 (introdução do SSU2)

### Recursos para Desenvolvedores

**Código-fonte:** - Repositório principal: https://i2pgit.org/I2P_Developers/i2p.i2p - Espelho no GitHub: https://github.com/i2p/i2p.i2p

**Exemplos de plugins:** - zzzot (rastreador BitTorrent) - pebble (plataforma de blog) - i2p-bote (e-mail sem servidor) - orchid (cliente Tor) - seedless (troca de pares)

**Ferramentas de compilação:** - makeplugin.sh - Geração e assinatura de chaves - Disponível no repositório i2p.scripts - Automatiza a criação e a verificação de su3

### Suporte da Comunidade

**Fóruns:** - [I2P Forum](https://i2pforum.net/) - [zzz.i2p](http://zzz.i2p/) (interno ao I2P)

**IRC/Bate-papo:** - #i2p-dev na OFTC - IRC do I2P dentro da rede

---

## Apêndice A: Exemplo completo de plugin.config

```properties
# Required fields
name=example-plugin
signer=developer@mail.i2p
version=1.2.3

# Update configuration
updateURL.su3=http://example.i2p/plugins/example-$OS-$ARCH.su3
min-i2p-version=2.0.0
min-java-version=17

# Display information
date=1698796800000
author=Example Developer <developer@mail.i2p>
websiteURL=http://example.i2p/
license=Apache-2.0

description=An example I2P plugin demonstrating best practices
description_de=Ein Beispiel-I2P-Plugin zur Demonstration bewährter Praktiken
description_es=Un plugin I2P de ejemplo que demuestra las mejores prácticas

# Console integration
consoleLinkName=Example Plugin
consoleLinkName_de=Beispiel-Plugin
consoleLinkURL=/example/
consoleLinkTooltip=Open the Example Plugin control panel
consoleLinkTooltip_de=Öffne das Beispiel-Plugin-Kontrollfeld
console-icon=/icon.png

# Installation behavior
dont-start-at-install=false
router-restart-required=false

# Platform requirements (informational)
required-platform-OS=All platforms supported
other-requirements=Requires 512MB free disk space
```
---

## Apêndice B: Exemplo completo de clients.config

```properties
# Main service client (managed)
clientApp.0.main=com.example.plugin.MainService
clientApp.0.name=Example Plugin Main Service
clientApp.0.delay=30
clientApp.0.args=$PLUGIN/config.properties --port=7656
clientApp.0.stopargs=shutdown
clientApp.0.uninstallargs=cleanup
clientApp.0.classpath=$PLUGIN/lib/example.jar,$I2P/lib/i2p.jar,$I2P/lib/mstreaming.jar

# External program via ShellService
clientApp.1.main=net.i2p.apps.ShellService
clientApp.1.name=Example Native Helper
clientApp.1.delay=35
clientApp.1.args=$PLUGIN/bin/helper-$OS-$ARCH --config $PLUGIN/helper.conf
clientApp.1.classpath=$I2P/lib/i2p.jar

# Jetty eepsite
clientApp.2.main=net.i2p.jetty.JettyStart
clientApp.2.name=Example Eepsite
clientApp.2.delay=40
clientApp.2.args=$PLUGIN/eepsite/jetty.xml
clientApp.2.stopargs=$PLUGIN/eepsite/jetty.xml stop
clientApp.2.classpath=$PLUGIN/lib/example-web.jar,$I2P/lib/i2p.jar

# I2PTunnel for eepsite
clientApp.3.main=net.i2p.i2ptunnel.TunnelControllerGroup
clientApp.3.name=Example Eepsite Tunnel
clientApp.3.delay=45
clientApp.3.args=$PLUGIN/eepsite/i2ptunnel.config
```
---

## Apêndice C: Exemplo completo de webapps.config

```properties
# Disable autostart for admin webapp
webapps.example-admin.startOnLoad=false

# Main webapp with classpath
webapps.example.startOnLoad=true
webapps.example.classpath=$PLUGIN/lib/example-core.jar,$PLUGIN/lib/commons-utils.jar,$I2P/lib/jstl.jar,$I2P/lib/standard.jar

# Legacy support (pre-0.7.12-9)
plugin.example.startOnLoad=true
```
---

## Apêndice D: Lista de Verificação de Migração (de 0.9.53 para 2.10.0)

### Alterações necessárias

- [ ] **Remover a compressão Pack200 do processo de build**
  - Remover as tarefas pack200 dos scripts Ant/Maven/Gradle
  - Republicar os plugins existentes sem pack200

- [ ] **Revisar os requisitos de versão do Java**
  - Considerar exigir Java 11+ para novos recursos
  - Planejar a exigência de Java 17+ no I2P 2.11.0
  - Atualizar `min-java-version` em plugin.config

- [ ] **Atualizar a documentação**
  - Remover referências a Pack200 (formato de compressão de JAR do Java)
  - Atualizar os requisitos de versão do Java
  - Atualizar referências de versão do I2P (0.9.x → 2.x)

### Alterações recomendadas

- [ ] **Reforçar as assinaturas criptográficas**
  - Migrar de XPI2P (formato antigo de pacote de plugin do I2P) para SU3 (formato atual de pacote assinado do I2P) se ainda não tiver sido feito
  - Usar chaves RSA-4096 para novos plugins

- [ ] **Aproveite os novos recursos (se estiver usando 0.9.53+)**
  - Use as variáveis `$OS` / `$ARCH` para atualizações específicas da plataforma
  - Use o ShellService (serviço de shell) para programas externos
  - Use o classpath aprimorado para webapps (funciona com qualquer nome de WAR)

- [ ] **Testar compatibilidade**
  - Testar no I2P 2.10.0
  - Verificar com Java 8, 11 e 17
  - Verificar no Windows, no Linux e no macOS

### Aprimoramentos Opcionais

- [ ] Implementar corretamente o ServletContextListener
- [ ] Adicionar descrições localizadas
- [ ] Fornecer ícone do console
- [ ] Melhorar o tratamento do encerramento
- [ ] Adicionar registro de logs abrangente
- [ ] Escrever testes automatizados
