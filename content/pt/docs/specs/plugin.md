---
title: "Especificação de Plugin"
description: "Regras de empacotamento .xpi2p / .su3 para plugins I2P"
slug: "plugin"
aliases:
  - "/pt/plugin_spec"
  - "/pt/plugin_spec/"
lastUpdated: "2022-01"
accurateFor: "0.9.53"
type: docs
---

## Visão Geral

Este documento especifica um formato de arquivo .xpi2p (como o .xpi do Firefox), mas com um arquivo de descrição plugin.config simples em vez de um arquivo XML install.rdf. Este formato de arquivo é usado tanto para instalações iniciais de plugins quanto para atualizações de plugins.

Além disso, este documento fornece uma breve visão geral de como o router instala plugins, e políticas e diretrizes para desenvolvedores de plugins.

O formato básico do arquivo .xpi2p é o mesmo de um arquivo i2pupdate.sud (o formato usado para atualizações do router), mas o instalador permitirá que o usuário instale o addon mesmo que ainda não conheça a chave do signatário.

A partir da versão 0.9.15, o formato de arquivo SU3 é suportado e é preferido. Este formato permite chaves de assinatura mais fortes.

> **Nota:** Não recomendamos mais distribuir plugins no formato xpi2p. Use o formato su3.

A estrutura de diretórios padrão permitirá aos usuários instalar os seguintes tipos de addons:

- Aplicações web do console
- Novo eepsite com cgi-bin, aplicações web
- Temas do console
- Traduções do console
- Programas Java
- Programas Java numa JVM separada
- Qualquer script shell ou programa

Um plugin instala todos os seus arquivos em `~/.i2p/plugins/name/` (`%APPDIR%\I2P\plugins\name\` no Windows). O instalador impedirá a instalação em qualquer outro local, embora o plugin possa acessar bibliotecas em outros lugares quando estiver em execução.

Isso deve ser visto apenas como uma forma de tornar a instalação, desinstalação e atualização mais fáceis, e de reduzir conflitos básicos entre plugins.

No entanto, essencialmente não há modelo de segurança uma vez que o plugin está em execução. O plugin executa na mesma JVM e com as mesmas permissões que o router, e tem acesso total ao sistema de arquivos, ao router, execução de programas externos, etc.

## Detalhes

foo.xpi2p é um arquivo de atualização assinada (sud) contendo o seguinte:

Cabeçalho .sud padrão anexado ao arquivo zip, contendo o seguinte:

```text
40-byte DSA signature
16-byte plugin version in UTF-8, padded with trailing zeroes if necessary
```
Arquivo zip contendo o seguinte:

### arquivo plugin.config

Este arquivo é obrigatório. É um arquivo de configuração padrão do I2P, contendo as seguintes propriedades:

#### Propriedades Obrigatórias

As quatro propriedades seguintes são obrigatórias. As três primeiras devem ser idênticas àquelas no plugin instalado para um plugin de atualização.

-   **name** - Será instalado neste nome de diretório. Para plugins nativos, você pode querer nomes separados em diferentes pacotes - foo-windows e foo-linux, por exemplo.
-   **key** - Chave pública DSA como 172 caracteres B64 terminando com '='. Omitir para formato SU3.
-   **signer** - yourname@mail.i2p recomendado
-   **version** - Deve estar em um formato que o VersionComparator possa analisar, ex. 1.2.3-4. 16 bytes máximo (deve coincidir com a versão sud). Separadores de número válidos são '.', '-', e '_'. Isto deve ser maior que aquele no plugin instalado para um plugin de atualização.

#### Propriedades de Exibição

Os valores para as seguintes propriedades são exibidos em /configplugins no console do router se presentes:

-   **date** - Horário Java - long int
-   **author** - `yourname@mail.i2p` recomendado
-   **websiteURL** - `http://foo.i2p/`
-   **updateURL** - `http://foo.i2p/foo.xpi2p` - O verificador de atualizações verificará os bytes 41-56 nesta URL para determinar se uma versão mais recente está disponível. A partir da versão 1.7.0 (0.9.53), é possível usar as variáveis `$OS` e `$ARCH` na URL. Não recomendado. Não use a menos que tenha distribuído plugins previamente no formato xpi2p.
-   **updateURL.su3** - `http://foo.i2p/foo.su3` - A localização do arquivo de atualização no formato su3, a partir da versão 0.9.15. A partir da versão 1.7.0 (0.9.53), é possível usar as variáveis `$OS` e `$ARCH` na URL.
-   **description** - em inglês
-   **description_xx** - para o idioma xx
-   **license** - A licença do plugin
-   **disableStop=true** - Padrão falso. Se verdadeiro, o botão parar não será exibido. Use isto se não houver webapps e nenhum cliente com stopargs.

#### Propriedades do Link da Barra de Resumo do Console

As seguintes propriedades são usadas para adicionar um link na barra de resumo do console:

-   **consoleLinkName** - será adicionado à barra de resumo
-   **consoleLinkName_xx** - para idioma xx
-   **consoleLinkURL** - /appname/index.jsp
-   **consoleLinkTooltip** - suportado a partir de 0.7.12-6
-   **consoleLinkTooltip_xx** - idioma xx a partir de 0.7.12-6

#### Propriedades do Ícone do Console

As seguintes propriedades opcionais podem ser usadas para adicionar um ícone personalizado no console:

-   **console-icon** - suportado a partir da versão 0.9.20. Apenas para webapps. Um caminho para uma imagem 32x32, ex. /icon.png. A partir da versão 1.7.0 (API 0.9.53), se consoleLinkURL for especificado, o caminho é relativo a essa URL. Caso contrário, é relativo ao nome da webapp. Aplica-se a todas as webapps no plugin.
-   **icon-code** - suportado a partir da versão 0.9.25. Fornece um ícone de console para plugins sem recursos web. Uma string B64 produzida chamando `net.i2p.data.Base64 encode FILE` em um arquivo de imagem png 32x32.

#### Propriedades do Instalador

As seguintes propriedades são usadas pelo instalador de plugins:

-   **type** - app/theme/locale/webapp/... (não implementado, provavelmente desnecessário)
-   **min-i2p-version** - A versão mínima do I2P que este plugin requer
-   **max-i2p-version** - A versão máxima do I2P em que este plugin irá executar
-   **min-java-version** - A versão mínima do Java que este plugin requer
-   **min-jetty-version** - suportado desde 0.8.13, use 6 para webapps Jetty 6
-   **max-jetty-version** - suportado desde 0.8.13, use 5.99999 para webapps Jetty 5
-   **required-platform-OS** - não implementado - talvez seja apenas exibido, não verificado
-   **other-requirements** - não implementado, ex: python x.y - não verificado pelo instalador, apenas exibido ao usuário
-   **dont-start-at-install=true** - Padrão falso. Não iniciará o plugin quando for instalado ou atualizado.
-   **router-restart-required=true** - Padrão falso. Isso não reinicia o router ou o plugin em uma atualização, apenas informa ao usuário que uma reinicialização é necessária.
-   **update-only=true** - Padrão falso. Se verdadeiro, falhará se uma instalação não existir.
-   **install-only=true** - Padrão falso. Se verdadeiro, falhará se uma instalação existir.
-   **min-installed-version** - para atualizar sobre, se uma instalação existir
-   **max-installed-version** - para atualizar sobre, se uma instalação existir
-   **depends=plugin1,plugin2,plugin3** - não implementado
-   **depends-version=0.3.4,,5.6.7** - não implementado

#### Propriedades de Tradução

-   **langs=xx,yy,Klingon,...** - (não implementado) (yy é a bandeira do país)

### Diretórios e Arquivos da Aplicação

Cada um dos seguintes diretórios ou arquivos é opcional, mas algo deve estar presente ou não funcionará:

**console/**

-   **locale/** - Apenas jars contendo novos pacotes de recursos (traduções) para aplicativos na instalação base do I2P. Pacotes para este plugin devem ir dentro de console/webapp/foo.war ou lib/foo.jar
-   **themes/** - Novos temas para o console do router. Coloque cada tema em um subdiretório.
-   **webapps/** - (Veja notas importantes abaixo sobre webapps) .wars - Estes serão executados no momento da instalação, a menos que desabilitados em webapps.config. O nome do war não precisa ser o mesmo que o nome do plugin. Não duplique nomes de war na instalação base do I2P.
-   **webapps.config** - Mesmo formato do webapps.config do router. Também usado para especificar jars adicionais em $PLUGIN/lib/ ou $I2P/lib para o classpath da webapp, com `webapps.warname.classpath=$PLUGIN/lib/foo.jar,$I2P/lib/bar.jar`

> **Nota:** Antes da versão 1.7.0 (API 0.9.53), a linha do classpath só era carregada se o warname fosse igual ao nome do plugin. A partir da API 0.9.53, a configuração do classpath funcionará para qualquer warname.

> **Nota:** Antes da versão do router 0.7.12-9, o router procurava por `plugin.warname.startOnLoad` em vez de `webapps.warname.startOnLoad`. Para compatibilidade com versões mais antigas do router, um plugin que deseje desativar um war deve incluir ambas as linhas.

**eepsite/**

(Veja as notas importantes abaixo sobre eepsites)

-   **cgi-bin/**
-   **docroot/**
-   **logs/**
-   **webapps/**
-   **jetty.xml** - O instalador terá que fazer substituição de variáveis aqui para definir o caminho. A localização e nome deste arquivo não importa muito, desde que esteja definido em clients.config - pode ser mais conveniente estar um nível acima daqui.

**lib/**

Coloque qualquer arquivo jar aqui e especifique-os em uma linha classpath em console/webapps.config e/ou clients.config

### arquivo clients.config

Este arquivo é opcional e especifica clientes que serão executados quando um plugin for iniciado. Ele usa o mesmo formato do arquivo clients.config do router. Veja a especificação do arquivo de configuração clients.config para mais informações sobre o formato e detalhes importantes sobre como os clientes são iniciados e parados.

-   **clientApp.0.stopargs=foo bar stop baz** - Se presente, a classe será chamada com estes argumentos para parar o cliente. Todas as tarefas de parada são chamadas com atraso zero. Nota: O router não pode determinar se seus clientes não gerenciados estão em execução ou não.
-   **clientApp.0.uninstallargs=foo bar uninstall baz** - Se presente, a classe será chamada com estes argumentos logo antes de deletar $PLUGIN. Todas as tarefas de desinstalação são chamadas com atraso zero.
-   **clientApp.0.classpath=$I2P/lib/foo.bar,$PLUGIN/lib/bar.jar** - O executor de plugin fará substituição de variáveis nas linhas args e stopargs da seguinte forma:
    -   `$I2P` - Diretório base de instalação do I2P
    -   `$CONFIG` - Diretório de configuração do I2P (tipicamente ~/.i2p)
    -   `$PLUGIN` - Diretório de instalação deste plugin (tipicamente ~/.i2p/plugins/appname)
    -   `$OS` - O sistema operacional host na forma `windows`, `linux`, `mac`
    -   `$ARCH` - A arquitetura host na forma `386`, `amd64`, `arm64`

(Veja as notas importantes abaixo sobre execução de shell scripts ou programas externos)

## Tarefas do Instalador de Plugin

Isto lista o que acontece quando um plugin é instalado pelo I2P.

1.  O arquivo .xpi2p é baixado.
2.  A assinatura .sud é verificada contra as chaves armazenadas. A partir da versão 0.9.14.1, se não houver uma chave correspondente, a instalação falha, a menos que uma propriedade avançada do router seja definida para permitir todas as chaves.
3.  Verificar a integridade do arquivo zip.
4.  Extrair o arquivo plugin.config.
5.  Verificar a versão do I2P, para garantir que o plugin funcionará.
6.  Verificar se os webapps não duplicam as aplicações $I2P existentes.
7.  Parar o plugin existente (se presente).
8.  Verificar se o diretório de instalação ainda não existe se update=false, ou perguntar para sobrescrever.
9.  Verificar se o diretório de instalação existe se update=true, ou perguntar para criar.
10. Descompactar o plugin em appDir/plugins/name/
11. Adicionar o plugin ao plugins.config

## Tarefas Iniciais de Plugin

Isto lista o que acontece quando os plugins são iniciados. Primeiro, plugins.config é verificado para ver quais plugins precisam ser iniciados. Para cada plugin:

1.  Verificar clients.config, e carregar e iniciar cada item (adicionar os jars configurados ao classpath).
2.  Verificar console/webapp e console/webapp.config. Carregar e iniciar os itens necessários (adicionar os jars configurados ao classpath).
3.  Adicionar console/locale/foo.jar ao classpath de tradução se presente.
4.  Adicionar console/theme ao caminho de busca de temas se presente.
5.  Adicionar o link da barra de resumo.

## Notas da Aplicação Web do Console

Webapps de console com tarefas em segundo plano devem implementar um ServletContextListener (veja seedless ou i2pbote para exemplos), ou sobrescrever destroy() no servlet, para que possam ser paradas. A partir da versão 0.7.12-3 do router, webapps de console sempre serão paradas antes de serem reiniciadas, então você não precisa se preocupar com múltiplas instâncias, desde que faça isso. Também a partir da versão 0.7.12-3 do router, webapps de console serão paradas no desligamento do router.

Não inclua os arquivos JAR de biblioteca no webapp; coloque-os em lib/ e defina um classpath em webapps.config. Assim você pode criar plugins de instalação e atualização separados, onde o plugin de atualização não contém os arquivos JAR de biblioteca.

Nunca inclua os JARs do Jetty, Tomcat ou servlet no seu plugin, pois podem entrar em conflito com a versão na instalação do I2P. Tenha cuidado para não incluir bibliotecas conflitantes.

Não inclua arquivos .java ou .jsp; caso contrário, o Jetty irá recompilá-los na instalação, o que aumentará o tempo de inicialização. Embora a maioria das instalações do I2P tenha um compilador Java e JSP funcionando no classpath, isso não é garantido e pode não funcionar em todos os casos.

Por enquanto, uma webapp que precise adicionar arquivos classpath em $PLUGIN deve ter o mesmo nome do plugin. Por exemplo, uma webapp no plugin foo deve ser nomeada foo.war.

Embora o I2P suporte Servlet 3.0 desde a versão 0.9.30 do I2P, ele NÃO suporta escaneamento de anotações para @WebContent (nenhum arquivo web.xml). Vários jars de tempo de execução adicionais seriam necessários, e nós não fornecemos esses em uma instalação padrão. Entre em contato com os desenvolvedores do I2P se você precisar de suporte para @WebContent.

## Notas sobre Eepsite

Não está claro como fazer um plugin instalar em um eepsite existente. O router não tem conexão com o eepsite, e ele pode ou não estar em execução, e pode haver mais de um. É melhor iniciar sua própria instância Jetty e instância I2PTunnel, para um eepsite completamente novo.

Pode instanciar um novo I2PTunnel (de forma semelhante ao que faz a CLI i2ptunnel), mas não aparecerá na interface gráfica do i2ptunnel, claro, essa é uma instância diferente. Mas tudo bem. Então você pode iniciar e parar o i2ptunnel e o jetty juntos.

Então não conte com o router para mesclar automaticamente isso com algum eepsite existente. Provavelmente não vai acontecer. Inicie um novo I2PTunnel e Jetty a partir de clients.config. Os melhores exemplos disso são os plugins zzzot e pebble.

Como obter substituição de caminho no jetty.xml? Veja os plugins zzzot e pebble como exemplos.

## Notas de Início/Parada do Cliente

A partir da versão 0.9.4, o router suporta clientes de plugin "gerenciados". Clientes de plugin gerenciados são instanciados e iniciados pelo `ClientAppManager`. O ClientAppManager mantém uma referência ao cliente e recebe atualizações sobre o estado do cliente. Clientes de plugin gerenciados são preferidos, pois é muito mais fácil implementar o rastreamento de estado e iniciar e parar um cliente. Também é muito mais fácil evitar referências estáticas no código do cliente que poderiam levar ao uso excessivo de memória após um cliente ser parado. Consulte a especificação do arquivo de configuração clients.config para obter mais informações sobre como escrever um cliente gerenciado.

Para clientes de plugin "não gerenciados", o router não tem como monitorar o estado dos clientes iniciados via clients.config. O autor do plugin deve lidar com múltiplas chamadas de início ou parada de forma elegante, se possível, mantendo uma tabela de estado estática, ou usando arquivos PID, etc. Evite logs ou exceções em múltiplos inícios ou paradas. Isso também vale para uma chamada de parada sem um início anterior. A partir da versão 0.7.12-3 do router, os plugins serão parados no desligamento do router, o que significa que todos os clientes com stopargs em clients.config serão chamados, independentemente de terem sido previamente iniciados ou não.

## Notas sobre Script Shell e Programa Externo

Para executar scripts shell ou outros programas externos, escreva uma pequena classe Java que verifica o tipo de SO, depois executa ShellCommand em um arquivo .bat ou .sh que você fornecer. Uma solução generalizada para isso foi adicionada no I2P 1.7.0/0.9.53, o "ShellService" que realiza rastreamento de estado para um único comando e se comunica com o ClientAppManager.

Programas externos não serão interrompidos quando o router parar, e uma segunda cópia será iniciada quando o router reiniciar. Isso geralmente pode ser mitigado usando um ShellService para realizar o rastreamento de estado. Se isso for inadequado para o seu caso de uso, você pode escrever uma classe wrapper ou script shell que faça o armazenamento usual do PID em um arquivo PID, e verificar por ele na inicialização.

## Outras Diretrizes de Plugin

-   Consulte o branch monotone i2p.scripts ou qualquer um dos plugins de exemplo na página do zzz para o script shell makeplugin.sh. Isso automatiza a maioria das tarefas para geração de chaves, criação de arquivo su3 do plugin e verificação. Você deve incorporar este script no seu processo de build do plugin.
-   Pack200 de jars e wars é fortemente recomendado para plugins, geralmente reduz os plugins em 60-65%. Consulte qualquer um dos plugins de exemplo na página do zzz para um exemplo. O desempacotamento Pack200 é suportado em routers 0.7.11-5 ou superior, que são essencialmente todos os routers que suportam plugins.
-   Plugins não devem tentar escrever em qualquer lugar em $I2P pois pode ser somente leitura, e isso não é uma boa política mesmo.
-   Plugins podem escrever em $CONFIG mas manter arquivos apenas em $PLUGIN é recomendado. Todos os arquivos em $PLUGIN serão excluídos na desinstalação.
-   $CWD pode estar em qualquer lugar; não assuma que está em um local específico, não tente ler ou escrever arquivos relativos a $CWD. Para um ShellService, é sempre o mesmo que $PLUGIN.
-   Programas Java devem descobrir onde estão com os getters de diretório em I2PAppContext.
-   O diretório do plugin é `I2PAppContext.getGlobalContext().getAppDir().getAbsolutePath() + "/plugins/" + appname`, ou coloque um argumento $PLUGIN na linha args em clients.config.
-   Todos os arquivos de configuração devem estar em UTF-8.
-   Para executar em uma JVM separada, use ShellCommand com `java -cp foo:bar:baz my.main.class arg1 arg2 arg3`.
-   Como alternativa ao stopargs em clients.config, um cliente Java pode registrar um hook de shutdown com `I2PAppContext.addShutdownTask()`. Mas isso não desligaria um plugin durante uma atualização, então stopargs é recomendado. Além disso, defina todas as threads criadas para modo daemon.
-   Não inclua classes duplicando aquelas na instalação padrão. Estenda as classes se necessário.
-   Cuidado com as diferentes definições de classpath em wrapper.config entre instalações antigas e novas.
-   Clientes rejeitarão chaves duplicadas com keynames diferentes, e keynames duplicados com chaves diferentes, e chaves ou keynames diferentes em pacotes de atualização. Proteja suas chaves. Gere-as apenas uma vez.
-   Não modifique o arquivo plugin.config em tempo de execução pois será sobrescrito na atualização. Use um arquivo de configuração diferente no diretório para armazenar configuração de tempo de execução.
-   Em geral, plugins não devem exigir acesso a $I2P/lib/router.jar. Não acesse classes do router, a menos que esteja fazendo algo especial.
-   Como cada versão deve ser maior que a anterior, você pode aprimorar seu script de build para adicionar um número de build ao final da versão.
-   Plugins nunca devem chamar `System.exit()`.
-   Por favor, respeite licenças atendendo aos requisitos de licença para qualquer software que você empacote.
-   O router define o fuso horário da JVM para UTC. Se um plugin precisar conhecer o fuso horário real do usuário, ele é armazenado pelo router na propriedade I2PAppContext `i2p.systemTimeZone`.

## Classpaths

Os seguintes jars em $I2P/lib podem ser assumidos como estando no classpath padrão para todas as instalações do I2P, independentemente de quão antiga ou nova seja a instalação original.

Todas as APIs públicas recentes nos jars do i2p têm o número da versão especificado no Javadocs. Se o seu plugin requer certas funcionalidades disponíveis apenas em versões recentes, certifique-se de definir as propriedades min-i2p-version, min-jetty-version, ou ambas, no arquivo plugin.config.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Jar</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contains</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">addressbook.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Subscription and blockfile support</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need; use the NamingService interface</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">commons-logging.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Apache Logging</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Empty since release 0.9.30</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">commons-el.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">JSP Expressions Language</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For plugins with JSPs that use EL. As of release 0.9.30 (Jetty 9), this contains the EL 3.0 API.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Core API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">All plugins will need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2ptunnel.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2PTunnel</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For plugins with HTTP or other servers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jasper-compiler.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">nothing</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Empty since Jetty 6 (release 0.9)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jasper-runtime.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Jasper Compiler and Runtime, and some Tomcat utils</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Needed for plugins with JSPs</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">javax.servlet.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Servlet API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Needed for plugins with JSPs. As of release 0.9.30 (Jetty 9), this contains the Servlet 3.1 and JSP 2.3 APIs.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jbigi.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Binaries</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jetty-i2p.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Support utilities</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Some plugins will need. As of release 0.9.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">mstreaming.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Streaming API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins will need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">org.mortbay.jetty.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Jetty Base</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Only plugins starting their own Jetty instance will need. Recommended way of starting Jetty is with <code>net.i2p.jetty.JettyStart</code> in jetty-i2p.jar.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">router.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Router</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Only plugins using router context will need; most will not</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">routerconsole.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Console libraries</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need, not a public API</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">sam.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SAM API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">streaming.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Streaming Implementation</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins will need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">systray.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">URL Launcher</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins should not need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">systray4j.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Systray</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need. As of 0.9.26, no longer present.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">wrapper.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Router</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need</td>
    </tr>
  </tbody>
</table>
Os seguintes arquivos jar em $I2P/lib podem ser considerados presentes em todas as instalações do I2P, independentemente de quão antiga ou nova seja a instalação original, mas não estão necessariamente no classpath:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Jar</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contains</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jstl.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Standard Taglib</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For plugins using JSP tags</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">standard.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Standard Taglib</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For plugins using JSP tags</td>
    </tr>
  </tbody>
</table>
Qualquer coisa não listada acima pode não estar presente no classpath de todos, mesmo que você tenha no classpath na SUA versão do i2p. Se você precisar de algum jar não listado acima, adicione $I2P/lib/foo.jar ao classpath especificado em clients.config ou webapps.config no seu plugin.

Anteriormente, uma entrada de classpath especificada em clients.config era adicionada ao classpath para toda a JVM. No entanto, a partir da versão 0.7.13-3, isso foi corrigido usando class loaders, e agora, como originalmente pretendido, o classpath especificado em clients.config é apenas para o thread específico. Portanto, especifique o classpath completo necessário para cada cliente.

## Notas da Versão Java

O I2P requer Java 7 desde a versão 0.9.24 (janeiro de 2016). O I2P requereu Java 6 desde a versão 0.9.12 (abril de 2014). Qualquer usuário do I2P na versão mais recente deve estar executando uma JVM 1.7 (7.0).

Se o seu plugin **não requer 1.7**:

-   Certifique-se de que todos os arquivos java e jsp sejam compilados com source="1.6" target="1.6".
-   Certifique-se de que todos os jars de biblioteca incluídos também sejam para 1.6 ou inferior.

Se o seu plugin **requer 1.7**:

-   Observe isso na sua página de download.
-   Adicione min-java-version=1.7 ao seu plugin.config

Em qualquer caso, você **deve** definir um bootclasspath ao compilar com Java 8 para evitar falhas em tempo de execução.

## Falhas da JVM ao Atualizar

Nota - isto já deve estar tudo corrigido agora.

A JVM tem tendência a travar ao atualizar jars em um plugin se esse plugin estava sendo executado desde que o I2P foi iniciado (mesmo que o plugin tenha sido posteriormente parado). Isso pode ter sido corrigido com a implementação do carregador de classes na versão 0.7.13-3, mas talvez não.

A forma mais segura é projetar seu plugin com o jar dentro do war (para uma webapp), ou exigir uma reinicialização após a atualização, ou não atualizar os jars em seu plugin.

Devido à forma como os class loaders funcionam dentro de uma webapp, _pode_ ser seguro ter jars externos se você especificar o classpath em webapps.config. Mais testes são necessários para verificar isso. Não especifique o classpath com um cliente 'falso' em clients.config se for necessário apenas para uma webapp - use webapps.config em vez disso.

O menos seguro, e aparentemente a fonte da maioria dos crashes, são clientes com plugin jars especificados no classpath em clients.config.

Nada disso deve ser um problema na instalação inicial - você nunca deve precisar de uma reinicialização para a instalação inicial de um plugin.

## Referências

-   [Especificação do Arquivo de Configuração](/docs/specs/configuration)
-   [Criptografia DSA](/docs/specs/cryptography#DSA)
-   [Especificação de Atualizações](/docs/specs/updates)
