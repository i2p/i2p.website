---
title: "Diretrizes de Redação da Documentação do I2P"
description: "Manter a consistência, a precisão e a acessibilidade em toda a documentação técnica do I2P"
slug: "writing-guidelines"
lastUpdated: "2025-10"
---

**Objetivo:** Manter a consistência, a precisão e a acessibilidade em toda a documentação técnica do I2P

---

## Princípios Fundamentais

### 1. Verifique tudo

**Nunca presuma nem adivinhe.** Todas as afirmações técnicas devem ser verificadas em relação a: - Código-fonte atual do I2P (https://i2pgit.org/I2P_Developers/i2p.i2p/src/branch/master) - Documentação oficial da API (https://i2p.github.io/i2p.i2p/  - Especificações de configuração [/docs/specs/](/docs/) - Notas de versão recentes [/releases/](/categories/release/)

**Exemplo de verificação adequada:**

```markdown
❌ BAD: "The ClientApp interface probably requires three constructor parameters."
✅ GOOD: "The ClientApp interface requires this constructor signature: 
         public MyClientApp(I2PAppContext context, ClientAppManager manager, String[] args)"
```
### 2. Clareza Acima da Brevidade

Escreva para desenvolvedores que podem estar tendo contato com o I2P pela primeira vez. Explique os conceitos de forma completa, em vez de presumir conhecimento prévio.

**Exemplo:**

```markdown
❌ BAD: "Use the port mapper for service discovery."
✅ GOOD: "The port mapper offers a simple directory for internal TCP services. 
         Register loopback ports so other applications can discover your service 
         without hardcoded addresses."
```
### 3. Acessibilidade em primeiro lugar

A documentação deve ser acessível aos desenvolvedores na clearnet (internet comum), embora o I2P seja um overlay de rede. Sempre forneça alternativas acessíveis pela clearnet para recursos internos do I2P.

---

## Precisão técnica

### Documentação da API e da Interface

**Sempre inclua:** 1. Nomes completos de pacotes na primeira menção: `net.i2p.app.ClientApp` 2. Assinaturas completas de métodos com tipos de retorno 3. Nomes e tipos de parâmetros 4. Parâmetros obrigatórios vs opcionais

**Exemplo:**

```markdown
The `startup()` method has signature `void startup() throws IOException` and must 
execute without blocking. The method must call `ClientAppManager.notify()` at least 
once to transition from INITIALIZED state.
```
### Propriedades de Configuração

Ao documentar arquivos de configuração: 1. Mostre os nomes exatos das propriedades 2. Especifique a codificação do arquivo (UTF-8 para configurações do I2P) 3. Forneça exemplos completos 4. Documente os valores padrão 5. Anote a versão em que as propriedades foram introduzidas/alteradas

**Exemplo:**

```markdown
### clients.config Properties

**Required:**
- `clientApp.N.main` - Full class name (no default)

**Optional:**
- `clientApp.N.delay` - Seconds before starting (default: 120)
- `clientApp.N.onBoot` - Forces delay=0 if true (default: false, added in 0.9.4)
```
### Constantes e Enumerações

Ao documentar constantes, use os nomes reais do código:

```markdown
❌ BAD: "Common registrations include console, i2ptunnel, Jetty, sam, and bob"

✅ GOOD: "Common port mapper service constants from `net.i2p.util.PortMapper`:
- `SVC_CONSOLE` - Router console (default port 7657)
- `SVC_HTTP_PROXY` - HTTP proxy (default port 4444)
- `SVC_SAM` - SAM bridge (default port 7656)"
```
### Diferenciar Conceitos Semelhantes

O I2P possui vários sistemas sobrepostos. Sempre esclareça qual sistema você está documentando:

**Exemplo:**

```markdown
Note that client registry and port mapper are separate systems:
- **ClientAppManager registry** enables inter-application communication by name lookup
- **PortMapper** maps service names to host:port combinations for service discovery
- **i2ptunnel tunnel types** are configuration values (tunnel.N.type), not service registrations
```
---

## URLs e Referências da Documentação

### Regras de Acessibilidade de URLs

1. **Referências primárias** devem usar URLs acessíveis na clearnet (internet pública)
2. **URLs internas do I2P** (domínios .i2p) devem incluir notas de acessibilidade
3. **Sempre forneça alternativas** ao criar links para recursos internos do I2P

**Modelo para URLs internas do I2P:**

```markdown
> **Note:** The I2P network hosts comprehensive documentation at http://idk.i2p/javadoc-i2p/ 
> which requires an I2P router for access. For clearnet access, use the GitHub Pages 
> mirror at https://eyedeekay.github.io/javadoc-i2p/
```
### URLs de referência do I2P recomendadas

**Especificações oficiais:** - [Configuração](/docs/specs/configuration/) - [Plugin](/docs/specs/plugin/) - [Índice de Documentos](/docs/)

**Documentação da API (escolha a mais atual):** - Mais atual: https://i2p.github.io/i2p.i2p/ (API 0.9.66 a partir do I2P 2.10.0) - Espelho na clearnet: https://eyedeekay.github.io/javadoc-i2p/

**Código-fonte:** - GitLab (oficial): https://i2pgit.org/I2P_Developers/i2p.i2p/src/branch/master - Espelho no GitHub: https://github.com/i2p/i2p.i2p

### Padrões de Formato de Links

```markdown
✅ GOOD: [ClientApp Javadoc](https://i2p.github.io/i2p.i2p/net/i2p/app/ClientApp.html)
✅ GOOD: [Configuration Specification](https://geti2p.net/spec/configuration)

❌ BAD: See the ClientApp docs at http://idk.i2p/...
❌ BAD: [link](url) with no descriptive text
```
---

## Rastreamento de Versões

### Metadados do Documento

Todo documento técnico deve incluir metadados de versão no frontmatter (seção de cabeçalho no início do arquivo):

```markdown
---
title: "Document Title"
description: "Brief description"
slug: "url-slug"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "verified"
---
```
**Definições de campos:** - `lastUpdated`: Ano-mês em que o documento foi revisado/atualizado pela última vez - `accurateFor`: Versão do I2P em relação à qual o documento foi verificado - `reviewStatus`: Um de "draft", "needs-review", "verified", "outdated"

### Referências a versões no conteúdo

Ao mencionar versões: 1. Use **negrito** para a versão atual: "**versão 2.10.0** (setembro de 2025)" 2. Especifique tanto o número da versão quanto a data para referências históricas 3. Indique a versão da API separadamente da versão do I2P quando relevante

**Exemplo:**

```markdown
Managed clients were introduced in **version 0.9.4** (December 17, 2012) and 
remain the recommended architecture as of **version 2.10.0** (September 9, 2025). 
The current API version is **0.9.66**.
```
### Documentando mudanças ao longo do tempo

Para funcionalidades que evoluíram:

```markdown
**Version history:**
- **0.9.4 (December 2012)** - Managed clients introduced
- **0.9.42 (2019)** - clients.config.d/ directory structure added
- **1.7.0 (2021)** - ShellService added for external program tracking
- **2.10.0 (September 2025)** - Current release, no API changes to managed clients
```
### Avisos de descontinuação

Ao documentar recursos obsoletos:

```markdown
> **Deprecated:** This feature was deprecated in version X.Y.Z and will be removed 
> in version A.B.C. Use [alternative feature](link) instead.
```
---

## Padrões de Terminologia

### Termos oficiais do I2P

Use estes termos exatos de forma consistente:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Correct Term</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Avoid</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P router</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P node, I2P client (ambiguous)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">eepsite</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P website, hidden service (Tor term)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">connection, circuit (Tor term)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">netDb</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">network database, DHT</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">lease set</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">destination info</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">destination</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">address, endpoint</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">base64 destination</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P address, .i2p address</td>
    </tr>
  </tbody>
</table>
### Terminologia de Cliente Gerenciado

Ao documentar clientes gerenciados:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Use This</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Not This</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">managed client</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">managed application</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unmanaged client</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">legacy client, static client</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ClientAppManager</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">application manager, client manager</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">lifecycle methods</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">state methods, control methods</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">client registry</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">application registry, name service</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">port mapper</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">port registry, service directory</td>
    </tr>
  </tbody>
</table>
### Terminologia de Configuração

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Correct</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Incorrect</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>clients.config</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">clients.cfg, client.config</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>clients.config.d/</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">clients.d/, config.d/</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">router.config</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">router.cfg</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2ptunnel.config</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel.config</td>
    </tr>
  </tbody>
</table>
### Nomes de Pacotes e Classes

Use sempre nomes totalmente qualificados na primeira menção; depois, nomes curtos:

```markdown
The `net.i2p.app.ClientApp` interface requires implementation of three lifecycle 
methods. When a ClientApp starts, the manager calls `startup()`...
```
---

## Exemplos de Código e Formatação

### Exemplos de código em Java

Use realce de sintaxe adequado e exemplos completos:

```markdown
### Example: Registering with Port Mapper

\`\`\`java
// Register HTTP proxy service
context.portMapper().register(
    PortMapper.SVC_HTTP_PROXY, 
    "127.0.0.1", 
    4444
);

// Later, retrieve the port
int port = context.portMapper().getPort(PortMapper.SVC_HTTP_PROXY);
if (port == -1) {
    // Service not registered
}
\`\`\`
```
**Requisitos do exemplo de código:** 1. Inclua comentários explicando as linhas-chave 2. Mostre tratamento de erros quando relevante 3. Use nomes de variáveis realistas 4. Siga as convenções de codificação do I2P (indentação de 4 espaços) 5. Mostre as importações se não estiverem óbvias pelo contexto

### Exemplos de Configuração

Mostre exemplos completos e válidos de configuração:

```markdown
### Example: clients.config.d/ Entry

File: `clients.config.d/00-console.config`

\`\`\`properties
# Router console configuration
clientApp.0.main=net.i2p.router.web.RouterConsoleRunner
clientApp.0.name=Router Console
clientApp.0.args=7657 ::1,127.0.0.1 ./webapps/
clientApp.0.delay=0
clientApp.0.onBoot=true
\`\`\`
```
### Exemplos de Linha de Comando

Use `$` para comandos do usuário, `#` para root:

```markdown
\`\`\`bash
# Install I2P on Debian/Ubuntu
$ sudo apt-get install i2p

# Start the router
$ i2prouter start
\`\`\`
```
### Código em linha

Use backticks para: - Nomes de métodos: `startup()` - Nomes de classes: `ClientApp` - Nomes de propriedades: `clientApp.0.main` - Nomes de arquivos: `clients.config` - Constantes: `SVC_HTTP_PROXY` - Nomes de pacotes: `net.i2p.app`

---

## Tom e voz

### Profissional, porém acessível

Escreva para um público técnico sem ser condescendente:

```markdown
❌ BAD: "Obviously, you should implement the startup() method."
✅ GOOD: "Managed clients must implement the startup() method to initialize resources."

❌ BAD: "Even a junior dev knows you need to call notify()."
✅ GOOD: "The manager requires at least one notify() call during startup to track state transitions."
```
### Voz ativa

Use a voz ativa para maior clareza:

```markdown
❌ PASSIVE: "The ClientAppManager is notified by the client when state changes."
✅ ACTIVE: "The client notifies ClientAppManager when state changes."
```
### Imperativos para Instruções

Use imperativos diretos em conteúdo procedimental:

```markdown
✅ "Implement these three lifecycle methods:"
✅ "Call manager.notify() after changing state."
✅ "Register services using context.portMapper().register()"
```
### Evite jargão desnecessário

Explique os termos na primeira vez em que forem usados:

```markdown
✅ GOOD: "The netDb (network database) stores information about I2P routers and destinations."
❌ BAD: "Query the netDb for peer info." (no explanation)
```
### Diretrizes de Pontuação

1. **Sem travessões (em-dashes)** - use hífens comuns, vírgulas ou ponto e vírgula
2. Use **Oxford comma** (vírgula de Oxford) em listas: "console, i2ptunnel, and Jetty"
3. **Pontos finais dentro de blocos de código** apenas quando gramaticalmente necessário
4. **Listas em série** usam ponto e vírgula quando os itens contêm vírgulas

---

## Estrutura do Documento

### Ordem Padrão das Seções

Para a documentação da API:

1. **Visão geral** - o que a funcionalidade faz, por que ela existe
2. **Implementação** - como implementar/usar
3. **Configuração** - como configurá-la
4. **Referência da API** - descrições detalhadas de métodos/propriedades
5. **Exemplos** - exemplos completos e funcionais
6. **Boas práticas** - dicas e recomendações
7. **Histórico de versões** - quando foi introduzida, mudanças ao longo do tempo
8. **Referências** - links para documentação relacionada

### Hierarquia de Cabeçalhos

Use níveis de cabeçalho semânticos:

```markdown
# Document Title (h1 - only one per document)

## Major Section (h2)

### Subsection (h3)

#### Detail Section (h4)

**Bold text for emphasis within sections**
```
### Caixas de informação

Use citações em bloco para avisos especiais:

```markdown
> **Note:** Additional information that clarifies the main content.

> **Warning:** Important information about potential issues or breaking changes.

> **Deprecated:** This feature is deprecated and will be removed in version X.Y.Z.

> **Status:** Current implementation status or version information.
```
### Listas e Organização

**Listas não ordenadas** para itens não sequenciais:

```markdown
- First item
- Second item
- Third item
```
**Listas ordenadas** para etapas sequenciais:

```markdown
1. First step
2. Second step
3. Third step
```
**Listas de definições** para explicações de termos:

```markdown
**Term One**
: Explanation of term one

**Term Two**  
: Explanation of term two
```
---

## Armadilhas Comuns a Evitar

### 1. Confundir sistemas semelhantes

**Não confunda:** - registro do ClientAppManager vs. PortMapper - tipos de tunnel do i2ptunnel vs. constantes de serviço do PortMapper - ClientApp vs. RouterApp (contextos diferentes) - clientes gerenciados vs. não gerenciados

**Sempre esclareça qual sistema** você está discutindo:

```markdown
✅ "Register with ClientAppManager using manager.register(this) for name-based lookup."
✅ "Register with PortMapper using context.portMapper().register() for port discovery."
```
### 2. Referências a versões desatualizadas

**Não faça:** - Referir-se a versões antigas como "atuais" - Criar links para documentação da API desatualizada - Usar assinaturas de métodos descontinuadas em exemplos

**Faça:** - Verifique as notas de versão antes de publicar - Verifique se a documentação da API corresponde à versão atual - Atualize os exemplos para usar as melhores práticas atuais

### 3. URLs inacessíveis

**Não faça:** - Vincular apenas a domínios .i2p sem alternativas na clearnet (internet aberta) - Usar URLs de documentação quebradas ou desatualizadas - Vincular para caminhos locais file://

**Faça:** - Forneça alternativas na clearnet (internet pública/aberta) para todos os links internos do I2P - Verifique se os URLs estão acessíveis antes de publicar - Use URLs persistentes (geti2p.net, não hospedagem temporária)

### 4. Exemplos de Código Incompletos

**Não faça:** - Mostrar trechos sem contexto - Omitir tratamento de erros - Usar variáveis não definidas - Pular instruções de import quando não for óbvio

**Faça:** - Mostre exemplos completos e compiláveis - Inclua o tratamento de erros necessário - Explique o que cada linha significativa faz - Teste os exemplos antes de publicar

### 5. Declarações Ambíguas

```markdown
❌ "Some applications register services."
✅ "Applications implementing ClientApp may register with ClientAppManager 
   using manager.register(this) to enable name-based lookup."

❌ "Configuration files go in the config directory."
✅ "Modern I2P installations store client configurations in 
   $I2P/clients.config.d/ as individual files."
```
---

## Convenções do Markdown

### Nomenclatura de arquivos

Use kebab-case (palavras separadas por hífens) para nomes de arquivos: - `managed-clients.md` - `port-mapper-guide.md` - `configuration-reference.md`

### Formato do Frontmatter (metadados iniciais de um documento)

Sempre inclua o front matter YAML (metadados no início do arquivo):

```yaml
---
title: "Document Title"
description: "Brief description under 160 characters"
slug: "url-slug"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "verified"
---
```
### Formatação de links

**Links internos** (na documentação):

```markdown
See [clients.config specification](https://geti2p.net/spec/configuration#clients-config)
```
**Links externos** (para outros recursos):

```markdown
For more details, see [ClientApp Javadoc](https://i2p.github.io/i2p.i2p/net/i2p/app/ClientApp.html)
```
**Links para repositórios de código**:

```markdown
View source: [ClientApp.java](https://i2pgit.org/I2P_Developers/i2p.i2p/src/branch/master/core/java/src/net/i2p/app/ClientApp.java)
```
### Formatação de Tabelas

Use tabelas em GitHub-flavored Markdown (dialeto de Markdown do GitHub):

```markdown
| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `main` | String | (required) | Full class name |
| `delay` | Integer | 120 | Seconds before start |
| `onBoot` | Boolean | false | Force immediate start |
```
### Tags de linguagem para blocos de código

Sempre especifique a linguagem para o realce de sintaxe:

```markdown
\`\`\`java
// Java code
\`\`\`

\`\`\`bash
# Shell commands
\`\`\`

\`\`\`properties
# Configuration files
\`\`\`

\`\`\`xml
<!-- XML files -->
\`\`\`
```
---

## Lista de verificação de revisão

Antes de publicar a documentação, verifique:

- [ ] Todas as afirmações técnicas verificadas em relação ao código-fonte ou à documentação oficial
- [ ] Os números de versão e as datas estão atualizados
- [ ] Todos os URLs são acessíveis a partir do clearnet (internet aberta) (ou alternativas fornecidas)
- [ ] Os exemplos de código estão completos e testados
- [ ] A terminologia segue as convenções do I2P
- [ ] Sem travessões (use hífens simples ou outra pontuação)
- [ ] O frontmatter (cabeçalho de metadados) está completo e correto
- [ ] A hierarquia de títulos é semântica (h1 → h2 → h3)
- [ ] Listas e tabelas estão devidamente formatadas
- [ ] A seção de referências inclui todas as fontes citadas
- [ ] O documento segue as diretrizes de estrutura
- [ ] O tom é profissional, mas acessível
- [ ] Conceitos semelhantes são claramente diferenciados
- [ ] Sem links quebrados nem referências quebradas
- [ ] Os exemplos de configuração são válidos e atuais

---

**Feedback:** Se encontrar problemas ou tiver sugestões para estas diretrizes, envie-os por meio dos canais oficiais de desenvolvimento do I2P.
