---
title: "Clientes Gerenciados"
description: "Como aplicações gerenciadas pelo roteador se integram com o ClientAppManager e o mapeador de portas"
slug: "managed-clients"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## 1. Visão Geral

As entradas em [`clients.config`](/docs/specs/configuration/#clients-config) indicam ao router quais aplicações devem ser iniciadas na inicialização. Cada entrada pode ser executada como um cliente **gerenciado** (preferível) ou como um cliente **não gerenciado**. Os clientes gerenciados colaboram com o `ClientAppManager`, que:

- Instancia a aplicação e rastreia o estado do ciclo de vida para o console do roteador
- Expõe controles de iniciar/parar para o usuário e força encerramentos limpos na saída do roteador
- Hospeda um **registro de clientes** leve e um **mapeador de portas** para que as aplicações possam descobrir os serviços umas das outras

Clientes não gerenciados simplesmente invocam um método `main()`; use-os apenas para código legado que não pode ser modernizado.

## 2. Implementando um Cliente Gerenciado

Os clientes gerenciados devem implementar `net.i2p.app.ClientApp` (para aplicações voltadas ao usuário) ou `net.i2p.router.app.RouterApp` (para extensões do router). Forneça um dos construtores abaixo para que o gerenciador possa fornecer contexto e argumentos de configuração:

```java
public MyClientApp(I2PAppContext context, ClientAppManager manager, String[] args)
```
```java
public MyRouterApp(RouterContext context, ClientAppManager manager, String[] args)
```
O array `args` contém os valores configurados em `clients.config` ou arquivos individuais em `clients.config.d/`. Estenda as classes auxiliares `ClientApp` / `RouterApp` quando possível para herdar a conexão padrão do ciclo de vida.

### 2.1 Lifecycle Methods

Os clientes gerenciados devem implementar:

- `startup()` - executa a inicialização e retorna prontamente. Deve chamar `manager.notify()` pelo menos uma vez para transicionar do estado INITIALIZED.
- `shutdown(String[] args)` - libera recursos e para threads em segundo plano. Deve chamar `manager.notify()` pelo menos uma vez para mudar o estado para STOPPING ou STOPPED.
- `getState()` - informa ao console se a aplicação está em execução, iniciando, parando ou falhou

O gerenciador chama esses métodos conforme os usuários interagem com o console.

### 2.2 Advantages

- Relatórios de status precisos no console do roteador
- Reinicializações limpas sem vazamento de threads ou referências estáticas
- Menor consumo de memória após a aplicação parar
- Registro centralizado e relatório de erros através do contexto injetado

## 3. Unmanaged Clients (Fallback Mode)

Se a classe configurada não implementa uma interface gerenciada, o router a inicia invocando `main(String[] args)` e não consegue rastrear o processo resultante. O console exibe informações limitadas e os hooks de encerramento podem não ser executados. Reserve este modo para scripts ou utilitários de uso único que não podem adotar as APIs gerenciadas.

## 4. Client Registry

Clientes gerenciados e não gerenciados podem se registrar no gerenciador para que outros componentes possam obter uma referência por nome:

```java
manager.register(this);
```
O registo utiliza o valor de retorno do `getName()` do cliente como chave de registo. Os registos conhecidos incluem `console`, `i2ptunnel`, `Jetty`, `outproxy` e `update`. Obtenha um cliente com `ClientAppManager.getRegisteredApp(String name)` para coordenar funcionalidades (por exemplo, a consola consultando o Jetty para obter detalhes de estado).

Note que o registro de clientes e o mapeador de portas são sistemas separados. O registro de clientes permite a comunicação entre aplicações por meio de pesquisa de nomes, enquanto o mapeador de portas mapeia nomes de serviços para combinações host:porta para descoberta de serviços.

## 3. Clientes Não Gerenciados (Modo de Fallback)

O mapeador de portas oferece um diretório simples para serviços TCP internos. Registre portas de loopback para que colaboradores evitem endereços codificados diretamente:

```java
context.portMapper().register(PortMapper.SVC_HTTPS_PROXY, 4445);
```
Ou com especificação explícita do host:

```java
context.portMapper().register(PortMapper.SVC_HTTP_PROXY, "127.0.0.1", 4444);
```
Procure serviços usando `PortMapper.getPort(String name)` (retorna -1 se não for encontrado) ou `getPort(String name, int defaultPort)` (retorna o padrão se não for encontrado). Verifique o status de registro com `isRegistered(String name)` e recupere o host registrado com `getActualHost(String name)`.

Constantes comuns do serviço de mapeamento de portas de `net.i2p.util.PortMapper`:

- `SVC_CONSOLE` - Console do router (porta padrão 7657)
- `SVC_HTTP_PROXY` - Proxy HTTP (porta padrão 4444)
- `SVC_HTTPS_PROXY` - Proxy HTTPS (porta padrão 4445)
- `SVC_I2PTUNNEL` - Gerenciador I2PTunnel
- `SVC_SAM` - Bridge SAM (porta padrão 7656)
- `SVC_SAM_SSL` - Bridge SAM SSL
- `SVC_SAM_UDP` - SAM UDP
- `SVC_BOB` - Bridge BOB (porta padrão 2827)
- `SVC_EEPSITE` - Eepsite padrão (porta padrão 7658)
- `SVC_HTTPS_EEPSITE` - Eepsite HTTPS
- `SVC_IRC` - Túnel IRC (porta padrão 6668)
- `SVC_SUSIDNS` - SusiDNS

Nota: `httpclient`, `httpsclient` e `httpbidirclient` são tipos de túnel i2ptunnel (usados na configuração `tunnel.N.type`), não constantes de serviço de mapeamento de portas.

## 4. Registro de Clientes

### 2.1 Métodos de Ciclo de Vida

A partir da versão 0.9.42, o router suporta a divisão da configuração em arquivos individuais dentro do diretório `clients.config.d/`. Cada arquivo contém propriedades para um único cliente com todas as propriedades prefixadas com `clientApp.0.`:

```
clientApp.0.main=net.i2p.router.web.RouterConsoleRunner
clientApp.0.name=Router Console
clientApp.0.args=7657 ::1,127.0.0.1 ./webapps/
clientApp.0.delay=0
clientApp.0.onBoot=true
```
Esta é a abordagem recomendada para novas instalações e plugins.

### 2.2 Vantagens

Para compatibilidade retroativa, o formato tradicional usa numeração sequencial:

```
clientApp.0.main=net.i2p.router.web.RouterConsoleRunner
clientApp.0.name=Router Console
clientApp.0.args=7657 ::1,127.0.0.1 ./webapps/
clientApp.1.main=net.i2p.apps.systray.UrlLauncher
clientApp.1.name=URL Launcher
clientApp.1.delay=5
```
### 6.3 Configuration Properties

**Obrigatório:** - `main` - Nome completo da classe que implementa ClientApp ou RouterApp, ou que contém o método estático `main(String[] args)`

**Opcional:** - `name` - Nome de exibição para o console do router (padrão é o nome da classe) - `args` - Argumentos separados por espaço ou tabulação (suporta strings entre aspas) - `delay` - Segundos antes de iniciar (padrão 120) - `onBoot` - Força `delay=0` se verdadeiro - `startOnLoad` - Habilita/desabilita o cliente (padrão verdadeiro)

**Específico do plugin:** - `stopargs` - Argumentos passados durante o desligamento - `uninstallargs` - Argumentos passados durante a desinstalação do plugin - `classpath` - Entradas adicionais do classpath separadas por vírgula

**Substituição de variáveis para plugins:** - `$I2P` - Diretório base do I2P - `$CONFIG` - Diretório de configuração do usuário (ex., ~/.i2p) - `$PLUGIN` - Diretório do plugin - `$OS` - Nome do sistema operacional - `$ARCH` - Nome da arquitetura

## 5. Mapeador de Portas

- Prefira clientes gerenciados; recorra a não gerenciados apenas quando absolutamente necessário.
- Mantenha a inicialização e encerramento leves para que as operações do console permaneçam responsivas.
- Use nomes descritivos de registro e porta para que ferramentas de diagnóstico (e usuários finais) entendam o que um serviço faz.
- Evite singletons estáticos - confie no contexto injetado e no gerenciador para compartilhar recursos.
- Chame `manager.notify()` em todas as transições de estado para manter o status do console preciso.
- Se você precisar executar em uma JVM separada, documente como logs e diagnósticos são expostos ao console principal.
- Para programas externos, considere usar ShellService (adicionado na versão 1.7.0) para obter os benefícios de cliente gerenciado.

## 6. Formato de Configuração

Os clientes gerenciados foram introduzidos na **versão 0.9.4** (17 de dezembro de 2012) e permanecem como a arquitetura recomendada até a **versão 2.10.0** (9 de setembro de 2025). As APIs principais permaneceram estáveis com zero mudanças incompatíveis durante este período:

- Assinaturas de construtores inalteradas
- Métodos de ciclo de vida (startup, shutdown, getState) inalterados
- Métodos de registro do ClientAppManager inalterados
- Métodos de registro e busca do PortMapper inalterados

Melhorias notáveis: - **0.9.42 (2019)** - estrutura de diretório clients.config.d/ para arquivos de configuração individuais - **1.7.0 (2021)** - ShellService adicionado para rastreamento de estado de programas externos - **2.10.0 (2025)** - Versão atual sem alterações na API de cliente gerenciado

A próxima versão principal exigirá Java 17+ como mínimo (requisito de infraestrutura, não uma mudança de API).

## References

- [Especificação clients.config](/docs/specs/configuration/#clients-config)
- [Especificação de Arquivo de Configuração](/docs/specs/configuration/)
- [Índice de Documentação Técnica I2P](/docs/)
- [Javadoc do ClientAppManager](https://i2p.github.io/i2p.i2p/net/i2p/app/ClientAppManager.html) (API 0.9.66)
- [Javadoc do PortMapper](https://i2p.github.io/i2p.i2p/net/i2p/util/PortMapper.html) (API 0.9.66)
- [Interface ClientApp](https://i2p.github.io/i2p.i2p/net/i2p/app/ClientApp.html) (API 0.9.66)
- [Interface RouterApp](https://i2p.github.io/i2p.i2p/net/i2p/router/app/RouterApp.html) (API 0.9.66)
- [Javadoc Alternativo (estável)](https://docs.i2p-projekt.de/javadoc/)
- [Javadoc Alternativo (espelho clearnet)](https://eyedeekay.github.io/javadoc-i2p/)

> **Nota:** A rede I2P hospeda documentação abrangente em http://idk.i2p/javadoc-i2p/ que requer um router I2P para acesso. Para acesso pela clearnet, use o espelho do GitHub Pages acima.
