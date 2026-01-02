---
title: "Diretrizes para Desenvolvedores e Estilo de Código"
description: "Diretrizes completas para contribuir com o I2P: fluxo de trabalho, ciclo de lançamento, estilo de código, registro de logs, licenciamento e tratamento de problemas"
slug: "dev-guidelines"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

Leia primeiro o [Guia para Novos Desenvolvedores](/docs/develop/new-developers/).

## Diretrizes Básicas e Estilo de Codificação

A maioria dos pontos a seguir deve ser senso comum para qualquer pessoa que tenha trabalhado em código aberto ou em um ambiente de programação comercial. O seguinte se aplica principalmente ao ramo de desenvolvimento principal i2p.i2p. As diretrizes para outros ramos, plugins e aplicativos externos podem ser substancialmente diferentes; consulte o desenvolvedor apropriado para orientação.

### Comunidade

- Por favor, não apenas escreva código. Se puder, participe de outras atividades de desenvolvimento, incluindo: discussões de desenvolvimento e suporte no IRC e i2pforum.i2p; testes; relatórios de bugs e respostas; documentação; revisões de código; etc.
- Desenvolvedores ativos devem estar disponíveis periodicamente no IRC `#i2p-dev`. Esteja ciente do ciclo de lançamento atual. Respeite os marcos de lançamento, como congelamento de funcionalidades, congelamento de tags e o prazo de check-in para um lançamento.

### Ciclo de Lançamento

O ciclo normal de lançamento é de 10–16 semanas, quatro lançamentos por ano. A seguir estão os prazos aproximados dentro de um ciclo típico de 13 semanas. Os prazos reais para cada lançamento são definidos pelo gerente de lançamento após consulta com a equipe completa.

- 1–2 dias após o lançamento anterior: Check-ins no trunk são permitidos.
- 2–3 semanas após o lançamento anterior: Prazo para propagar mudanças importantes de outros branches para o trunk.
- 4–5 semanas antes do lançamento: Prazo para solicitar novos links na página inicial.
- 3–4 semanas antes do lançamento: Feature freeze. Prazo para novos recursos importantes.
- 2–3 semanas antes do lançamento: Realizar reunião do projeto para revisar solicitações de novos links na página inicial, se houver.
- 10–14 dias antes do lançamento: String freeze. Não são permitidas mais alterações em strings traduzidas (marcadas). Enviar strings para o Transifex, anunciar prazo de tradução no Transifex.
- 10–14 dias antes do lançamento: Prazo para recursos. Apenas correções de bugs após este momento. Não são permitidos mais recursos, refatoração ou limpeza.
- 3–4 dias antes do lançamento: Prazo para tradução. Obter traduções do Transifex e fazer check-in.
- 3–4 dias antes do lançamento: Prazo para check-in. Não são permitidos check-ins após este momento sem a permissão do responsável pelo lançamento.
- Horas antes do lançamento: Prazo para revisão de código.

### Git

- Tenha uma compreensão básica de sistemas de controle de código distribuído, mesmo que você nunca tenha usado git antes. Peça ajuda se precisar. Uma vez enviado, os commits são para sempre; não há como desfazer. Por favor, tenha cuidado. Se você nunca usou git antes, comece com passos pequenos. Faça commit de algumas pequenas alterações e veja como funciona.
- Teste suas alterações antes de fazer commit delas. Se você preferir o modelo de desenvolvimento de commit‑antes‑de‑testar, use seu próprio branch de desenvolvimento na sua própria conta e crie um MR assim que o trabalho estiver pronto. Não quebre a build. Não cause regressões. Caso você faça isso (acontece), por favor não desapareça por um longo período após enviar sua alteração.
- Se sua alteração for não trivial, ou se você quiser que as pessoas a testem e precisar de bons relatórios de teste para saber se sua alteração foi testada ou não, adicione um comentário de check-in ao `history.txt` e incremente a revisão da build em `RouterVersion.java`.
- Não faça commit de alterações importantes no branch principal i2p.i2p no final do ciclo de lançamento. Se um projeto levará mais de alguns dias, crie seu próprio branch no git, na sua própria conta, e faça o desenvolvimento lá para não bloquear os lançamentos.
- Para grandes alterações (geralmente falando, mais de 100 linhas, ou tocando mais de três arquivos), faça commit em um novo branch na sua própria conta do GitLab, crie um MR e atribua um revisor. Atribua o MR a você mesmo. Faça merge do MR você mesmo assim que o revisor aprovar.
- Não crie branches WIP na conta principal I2P_Developers (exceto para i2p.www). WIP pertence à sua própria conta. Quando o trabalho estiver concluído, crie um MR. Os únicos branches na conta principal devem ser para forks verdadeiros, como um lançamento pontual.
- Faça desenvolvimento de forma transparente e com a comunidade em mente. Faça commit frequentemente. Faça commit ou merge no branch principal com a maior frequência possível, dados os diretrizes acima. Se você estiver trabalhando em algum grande projeto no seu próprio branch/conta, avise as pessoas para que elas possam acompanhar e revisar/testar/comentar.

### Estilo de Código

- O estilo de codificação em grande parte do código é de 4 espaços para indentação. Não use tabs. Não reformate o código. Se sua IDE ou editor quiser reformatar tudo, controle-o. Em alguns lugares, o estilo de codificação é diferente. Use o bom senso. Emule o estilo no arquivo que você está modificando.
- Todas as novas classes e métodos públicos e package-private requerem Javadocs. Adicione `@since` número-da-versão. Javadocs para novos métodos privados são desejáveis.
- Para quaisquer Javadocs adicionados, não deve haver erros ou avisos de doclint. Execute `ant javadoc` com Oracle Java 14 ou superior para verificar. Todos os parâmetros devem ter linhas `@param`, todos os métodos não-void devem ter linhas `@return`, todas as exceções declaradas como lançadas devem ter linhas `@throws`, e nenhum erro HTML.
- Classes em `core/` (i2p.jar) e porções do i2ptunnel fazem parte da nossa API oficial. Existem vários plugins externos e outras aplicações que dependem desta API. Tenha cuidado para não fazer alterações que quebrem a compatibilidade. Não adicione métodos à API a menos que sejam de utilidade geral. Javadocs para métodos da API devem ser claros e completos. Se você adicionar ou alterar a API, também atualize a documentação no site (branch i2p.www).
- Marque strings para tradução quando apropriado, o que é verdade para todas as strings de UI. Não altere strings marcadas existentes a menos que seja realmente necessário, pois isso quebrará as traduções existentes. Não adicione ou altere strings marcadas após o congelamento de tags no ciclo de lançamento para que os tradutores tenham a chance de atualizar antes do lançamento.
- Use genéricos e classes concorrentes sempre que possível. I2P é uma aplicação altamente multi-threaded.
- Familiarize-se com armadilhas comuns de Java que são detectadas pelo FindBugs/SpotBugs. Execute `ant findbugs` para saber mais.
- Java 8 é necessário para construir e executar I2P a partir da versão 0.9.47. Não use classes ou métodos Java 7 ou 8 em subsistemas embarcados: addressbook, core, i2ptunnel.jar (não-UI), mstreaming, router, routerconsole (apenas news), streaming. Esses subsistemas são usados por Android e aplicações embarcadas que requerem apenas Java 6. Todas as classes devem estar disponíveis na API 14 do Android. Recursos de linguagem Java 7 são aceitáveis nesses subsistemas se suportados pela versão atual do Android SDK e eles compilam para código compatível com Java 6.
- Try-with-resources não pode ser usado em subsistemas embarcados, pois requer `java.lang.AutoCloseable` no runtime, e isso não está disponível até a API 19 do Android (KitKat 4.4).
- O pacote `java.nio.file` não pode ser usado em subsistemas embarcados, pois não está disponível até a API 26 do Android (Oreo 8).
- Além das limitações acima, classes, métodos e construções Java 8 podem ser usados apenas nos seguintes subsistemas: BOB, desktopgui, i2psnark, i2ptunnel.war (UI), jetty-i2p.jar, jsonrpc, routerconsole (exceto news), SAM, susidns, susimail, systray.
- Autores de plugins podem requerer qualquer versão mínima de Java através do arquivo `plugin.config`.
- Converta explicitamente entre tipos primitivos e classes; não confie em autoboxing/unboxing.
- Não use `URL`. Use `URI`.
- Não capture `Exception`. Capture `RuntimeException` e exceções verificadas individualmente.
- Não use `String.getBytes()` sem um argumento de charset UTF-8. Você também pode usar `DataHelper.getUTF8()` ou `DataHelper.getASCII()`.
- Sempre especifique um charset UTF-8 ao ler ou escrever arquivos. Os utilitários `DataHelper` podem ser úteis.
- Sempre especifique um locale (por exemplo `Locale.US`) ao usar `String.toLowerCase()` ou `String.toUpperCase()`. Não use `String.equalsIgnoreCase()`, pois um locale não pode ser especificado.
- Não use `String.split()`. Use `DataHelper.split()`.
- Não adicione código para formatar datas e horas. Use `DataHelper.formatDate()` e `DataHelper.formatTime()`.
- Certifique-se de que `InputStream`s e `OutputStream`s sejam fechados em blocos finally.
- Use `{}` para todos os blocos `for` e `while`, mesmo que sejam de apenas uma linha. Se você usar `{}` para o bloco `if`, `else`, ou `if-else`, use para todos os blocos. Coloque `} else {` em uma única linha.
- Especifique campos como `final` sempre que possível.
- Não armazene `I2PAppContext`, `RouterContext`, `Log`, ou quaisquer outras referências a router ou itens de contexto em campos estáticos.
- Não inicie threads em construtores. Use `I2PAppThread` em vez de `Thread`.

### Registro de Logs

As seguintes diretrizes aplicam-se ao router, webapps e todos os plugins.

- Para quaisquer mensagens não exibidas no nível de log padrão (WARN, INFO e DEBUG), a menos que a mensagem seja uma string estática (sem concatenação), sempre use `log.shouldWarn()`, `log.shouldInfo()` ou `log.shouldDebug()` antes da chamada de log para evitar a criação desnecessária de objetos.
- Mensagens de log que podem ser exibidas no nível de log padrão (ERROR, CRIT e `logAlways()`) devem ser breves, claras e compreensíveis para um usuário não técnico. Isso inclui o texto de razão da exceção que também pode ser exibido. Considere traduzir se o erro provavelmente acontecerá (por exemplo, em erros de envio de formulário). Caso contrário, a tradução não é necessária, mas pode ser útil procurar e reutilizar uma string que já esteja marcada para tradução em outro lugar.
- Mensagens de log não exibidas no nível de log padrão (WARN, INFO e DEBUG) são destinadas ao uso do desenvolvedor e não têm os requisitos acima. No entanto, mensagens WARN estão disponíveis na aba de log do Android e podem ser úteis para usuários que estão depurando problemas, então use algum cuidado com mensagens WARN também.
- Mensagens de log INFO e DEBUG devem ser usadas com moderação, especialmente em caminhos de código frequentemente executados. Embora sejam úteis durante o desenvolvimento, considere removê-las ou comentá-las após a conclusão dos testes.
- Não registre logs em stdout ou stderr (wrapper log).

### Licenças

- Apenas faça commit de código que você mesmo escreveu. Antes de fazer commit de qualquer código ou JARs de bibliotecas de outras fontes, justifique por que é necessário, verifique se a licença é compatível e obtenha aprovação do gerente de lançamento.
- Se você obtiver aprovação para adicionar código externo ou JARs, e binários estiverem disponíveis em qualquer pacote Debian ou Ubuntu, você deve implementar opções de compilação e empacotamento para usar o pacote externo em vez disso. Lista de verificação de arquivos a modificar: `build.properties`, `build.xml`, `debian/control`, `debian/i2p-router.install`, `debian/i2p-router.links`, `debian/rules`, `sub-build.xml`.
- Para quaisquer imagens enviadas de fontes externas, é sua responsabilidade primeiro verificar se a licença é compatível. Inclua a licença e informações da fonte no comentário do commit.

### Bugs

- Gerenciar issues é trabalho de todos; por favor, ajude. Monitore o [GitLab](https://i2pgit.org/I2P_Developers/i2p.i2p/issues) para encontrar issues com as quais você pode ajudar. Comente, corrija e feche issues se puder.
- Novos desenvolvedores devem começar corrigindo issues. Quando tiver uma correção, anexe seu patch à issue e adicione a palavra-chave `review-needed`. Não feche a issue até que ela tenha sido revisada com sucesso e você tenha verificado suas alterações. Depois de fazer isso sem problemas para alguns tickets, você pode seguir o procedimento normal acima.
- Feche uma issue quando achar que a corrigiu. Não temos um departamento de testes para verificar e fechar tickets. Se não tiver certeza de que corrigiu, feche-a e adicione uma nota dizendo "Acho que corrigi, por favor teste e reabra se ainda estiver quebrado". Adicione um comentário com o número da dev build ou revisão e defina o milestone para o próximo lançamento.
