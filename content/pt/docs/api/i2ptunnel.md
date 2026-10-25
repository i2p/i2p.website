---
title: "I2PTunnel"
description: "Ferramenta para interagir e fornecer serviços no I2P"
slug: "i2ptunnel"
aliases:
  - "/pt/i2ptunnel"
  - "/pt/i2ptunnel/"
  - "/pt/i2ptunnel_migration"
  - "/pt/i2ptunnel_migration/"
  - "/pt/i2ptunnel_services"
  - "/pt/i2ptunnel_services/"
lastUpdated: "2023-10"
accurateFor: "0.9.59"
---

## Visão Geral {#overview}

I2PTunnel é uma ferramenta para interfacear com e fornecer serviços no I2P. O destino de um I2PTunnel pode ser definido usando um [hostname](/docs/overview/naming), [Base32](/docs/overview/naming#base32), ou uma chave de destino completa de 516 bytes. Um I2PTunnel estabelecido estará disponível na sua máquina cliente como localhost:port. Se você deseja fornecer um serviço na rede I2P, você simplesmente cria um I2PTunnel para o ip_address:port apropriado. Uma chave de destino correspondente de 516 bytes será gerada para o serviço e ele se tornará disponível em todo o I2P. Uma interface web para gerenciamento do I2PTunnel está disponível em [localhost:7657/i2ptunnel/](http://localhost:7657/i2ptunnel/).

## Serviços Padrão {#default-services}

### Túneis de Servidor {#default-server-tunnels}

- **I2P Webserver** - Um tunnel apontado para um webserver Jetty executado em [localhost:7658](http://localhost:7658) para hospedagem conveniente e rápida no I2P.
  A raiz do documento é:
  - **Unix** - `$HOME/.i2p/eepsite/docroot`
  - **Windows** - `%LOCALAPPDATA%\I2P\I2P Site\docroot`, que se expande para: `C:\Users\**nome_do_usuário**\AppData\Local\I2P\I2P Site\docroot`

### Tunnels de Cliente {#default-client-tunnels}

- **I2P HTTP Proxy** - *localhost:4444* - Um proxy HTTP usado para navegar no I2P e na internet regular de forma anônima através do I2P. Navegar na internet através do I2P usa um proxy aleatório especificado pela opção "Outproxies:".
- **Irc2P** - *localhost:6668* - Um tunnel IRC para a rede IRC anônima padrão, Irc2P.
- **gitssh.idk.i2p** - *localhost:7670* - Acesso SSH ao repositório Git do projeto
- **smtp.postman.i2p** - *localhost:7659* - Um serviço SMTP fornecido pelo postman em hq.postman.i2p
- **pop3.postman.i2p** - *localhost:7660* - O serviço POP3 complementar do postman em hq.postman.i2p

## Configuração {#configuration}

[Configuração do I2PTunnel](/docs/specs/configuration)

## Modos de Cliente {#client-modes}

### Padrão {#client-modes-standard}

Abre uma porta TCP local que se conecta a um serviço (como HTTP, FTP ou SMTP) em um destino dentro do I2P. O tunnel é direcionado para um host aleatório da lista de destinos separados por vírgula (", ").

### HTTP {#client-mode-http}

Um túnel de cliente HTTP. O túnel conecta-se ao destino especificado pela URL numa solicitação HTTP. Suporta proxy para a internet se um outproxy for fornecido. Remove das conexões HTTP os seguintes cabeçalhos:

- **Accept\*:** (não incluindo "Accept" e "Accept-Encoding") pois variam muito entre navegadores e podem ser usados como identificador.
- **Referer:**
- **Via:**
- **From:**

O proxy cliente HTTP fornece uma série de serviços para proteger o usuário e proporcionar uma melhor experiência do usuário.

**Processamento de cabeçalhos de solicitação:** - Remove cabeçalhos problemáticos para privacidade - Roteamento para outproxy local ou remoto - Seleção, cache e rastreamento de acessibilidade de outproxy - Pesquisas de nome de host para destino - Substituição do cabeçalho host para b32 - Adiciona cabeçalho para indicar suporte a descompressão transparente - Força connection: close - Suporte a proxy compatível com RFC - Processamento e remoção de cabeçalhos hop-by-hop compatível com RFC - Autenticação opcional digest e básica com nome de usuário/senha - Autenticação opcional de outproxy digest e básica com nome de usuário/senha - Buffer de todos os cabeçalhos antes de passar adiante para eficiência - Links de servidor jump - Processamento de resposta jump e formulários (assistente de endereço) - Processamento de b32 blinded e formulários de credenciais - Suporta solicitações HTTP e HTTPS (CONNECT) padrão

**Processamento de cabeçalho de resposta:** - Verificar se deve descomprimir a resposta - Forçar conexão: fechar - Processamento e remoção de cabeçalhos hop-by-hop conforme RFC - Buffer de todos os cabeçalhos antes de passar adiante para eficiência

**Respostas de erro HTTP:** - Para muitos erros comuns e não tão comuns, para que o usuário saiba o que aconteceu - Mais de 20 páginas de erro únicas traduzidas, estilizadas e formatadas para vários erros - Servidor web interno para servir formulários, CSS, imagens e erros

#### Compressão de Resposta Transparente {#transparent-response-compression}

A compressão de resposta do i2ptunnel é solicitada com o cabeçalho HTTP:

- **X-Accept-Encoding:** x-i2p-gzip;q=1.0, identity;q=0.5, deflate;q=0, gzip;q=0, *;q=0

O lado do servidor remove este cabeçalho hop-by-hop antes de enviar a solicitação para o servidor web. O cabeçalho elaborado com todos os valores q não é necessário; os servidores devem apenas procurar por "x-i2p-gzip" em qualquer lugar no cabeçalho.

O lado do servidor determina se deve comprimir a resposta com base nos cabeçalhos recebidos do servidor web, incluindo Content-Type, Content-Length e Content-Encoding, para avaliar se a resposta é comprimível e se vale a pena o CPU adicional necessário. Se o lado do servidor comprimir a resposta, ele adiciona o seguinte cabeçalho HTTP:

- **Content-Encoding:** x-i2p-gzip

Se este cabeçalho estiver presente na resposta, o proxy cliente HTTP descomprime-o de forma transparente. O lado cliente remove este cabeçalho e executa gunzip antes de enviar a resposta ao navegador. Note que ainda temos a compressão gzip subjacente na camada I2CP, que ainda é eficaz se a resposta não estiver comprimida na camada HTTP.

Este design e a implementação atual violam a RFC 2616 de várias maneiras:

- X-Accept-Encoding não é um cabeçalho padrão
- Não desfragmenta/fragmenta por salto; passa a fragmentação de ponta a ponta
- Passa o cabeçalho Transfer-Encoding de ponta a ponta
- Usa Content-Encoding, não Transfer-Encoding, para especificar a codificação por salto
- Proíbe compressão gzip x-i2p quando Content-Encoding está definido (mas provavelmente não queremos fazer isso mesmo)
- O lado do servidor comprime com gzip a fragmentação enviada pelo servidor, em vez de fazer desfragmentar-gzip-refragmentar e desfragmentar-gunzip-refragmentar
- O conteúdo comprimido com gzip não é fragmentado depois. RFC 2616 requer que toda Transfer-Encoding que não seja "identity" seja fragmentada.
- Como não há fragmentação externa (após) o gzip, é mais difícil encontrar o fim dos dados, tornando qualquer implementação de keepalive mais difícil.
- RFC 2616 diz que Content-Length não deve ser enviado se Transfer-Encoding estiver presente, mas nós enviamos. A especificação diz para ignorar Content-Length se Transfer-Encoding estiver presente, o que os navegadores fazem, então funciona para nós.

Alterações para implementar uma compressão hop-by-hop compatível com padrões de forma retrocompatível são um tópico para estudos futuros. Qualquer mudança no dechunk-gzip-rechunk exigiria um novo tipo de codificação, talvez x-i2p-gzchunked. Isso seria idêntico ao Transfer-Encoding: gzip, mas teria que ser sinalizado de forma diferente por razões de compatibilidade. Qualquer mudança exigiria uma proposta formal.

#### Compressão Transparente de Requisições {#transparent-request-compression}

Não suportado, embora POST se beneficiaria. Note que ainda temos a compressão gzip subjacente na camada I2CP.

#### Persistência {#persistence}

Os proxies cliente e servidor atualmente não suportam sockets HTTP persistentes RFC 2616 em nenhum dos três saltos (socket do navegador, socket I2P, socket do servidor). Cabeçalhos Connection: close são injetados em cada salto. Mudanças para implementar persistência estão sendo investigadas. Essas mudanças devem estar em conformidade com os padrões e ser compatíveis com versões anteriores, e não exigiriam uma proposta formal.

#### Pipelining {#pipelining}

Os proxies cliente e servidor atualmente não suportam pipelining HTTP RFC 2616 e não há planos para fazê-lo. Os navegadores modernos não suportam pipelining através de proxies porque a maioria dos proxies não consegue implementá-lo corretamente.

#### Compatibilidade {#compatibility}

As implementações de proxy devem funcionar corretamente com outras implementações do outro lado. Os proxies de cliente devem funcionar sem um proxy de servidor com suporte HTTP (ou seja, um tunnel padrão) no lado do servidor. Nem todas as implementações suportam x-i2p-gzip.

#### Agente do Usuário {#user-agent}

Dependendo de se o tunnel está usando um outproxy ou não, ele anexará o seguinte User-Agent:

- *Outproxy:* **User-Agent:** Usa o user agent de uma versão recente do Firefox no Windows
- *Uso interno do I2P:* **User-Agent:** MYOB/6.66 (AN/ON)

### Cliente IRC {#client-mode-irc}

Cria uma conexão para um servidor IRC aleatório especificado pela lista de destinos separados por vírgula (", "). Apenas um subconjunto de comandos IRC em lista branca são permitidos devido a preocupações de anonimato.

A seguinte lista de permissões é para comandos de entrada do servidor IRC para o cliente IRC.

**Lista de permitidos:** - AUTHENTICATE - CAP - ERROR - H - JOIN - KICK - MODE - NICK - PART - PING - PROTOCTL - QUIT - TOPIC - WALLOPS

Existe também uma lista de permissões para comandos enviados do cliente IRC para o servidor IRC. É bastante extensa devido ao número de comandos administrativos do IRC. Consulte o código-fonte IRCFilter.java para detalhes.

O filtro de saída também modifica os seguintes comandos para remover informações identificadoras: - NOTICE - PART - PING - PRIVMSG - QUIT - USER

### SOCKS 4/4a/5 {#client-mode-socks}

Permite usar o router I2P como um proxy SOCKS.

### SOCKS IRC {#client-mode-socks-irc}

Permite usar o router I2P como um proxy SOCKS com a lista branca de comandos especificada pelo modo cliente [IRC](#client-mode-irc).

### CONNECT {#client-mode-connect}

Cria um tunnel HTTP e usa o método de requisição HTTP "CONNECT" para construir um tunnel TCP que geralmente é usado para SSL e HTTPS.

### Streamr {#client-mode-streamr}

Cria um servidor UDP anexado a um cliente Streamr I2PTunnel. O tunnel cliente streamr irá se inscrever em um tunnel servidor streamr.

![Diagrama Streamr](/images/I2PTunnel-streamr.png)

## Modos de Servidor {#server-modes}

### Padrão {#server-mode-standard}

Cria um destino para um ip:porta local com uma porta TCP aberta.

### HTTP {#server-mode-http}

Cria um destino para um servidor HTTP local ip:port. Suporta gzip para solicitações com Accept-encoding: x-i2p-gzip, responde com Content-encoding: x-i2p-gzip em tal solicitação.

O proxy do servidor HTTP fornece uma série de serviços para tornar a hospedagem de um site mais fácil e segura, e para proporcionar uma melhor experiência do usuário no lado do cliente.

**Processamento de cabeçalho de requisição:** - Validação de cabeçalho - Proteção contra falsificação de cabeçalho - Verificações de tamanho de cabeçalho - Rejeição opcional de inproxy e user-agent - Adicionar cabeçalhos X-I2P para que o servidor web saiba de onde veio a requisição - Substituição do cabeçalho Host para facilitar vhosts do servidor web - Forçar connection: close - Processamento e remoção de cabeçalhos hop-by-hop em conformidade com RFC - Buffer de todos os cabeçalhos antes de passar adiante para eficiência

**Proteção DDoS:** - Limitação de POST - Timeouts e proteção contra slowloris - Limitação adicional ocorre no streaming para todos os tipos de tunnel

**Processamento de cabeçalhos de resposta:** - Remoção de alguns cabeçalhos problemáticos para a privacidade - Verificação do tipo MIME e outros cabeçalhos para determinar se deve comprimir a resposta - Forçar connection: close - Processamento e remoção de cabeçalhos hop-by-hop em conformidade com RFC - Buffer de todos os cabeçalhos antes de repassar para eficiência

**Respostas de erro HTTP:** - Para muitos erros comuns e não tão comuns e sobre limitação de taxa, para que o usuário do lado cliente saiba o que aconteceu

**Compressão transparente de resposta:** - O servidor web e/ou a camada I2CP podem comprimir, mas o servidor web frequentemente não o faz, e é mais eficiente comprimir em uma camada alta, mesmo que o I2CP também comprima. O proxy do servidor HTTP trabalha de forma cooperativa com o proxy do lado do cliente para comprimir transparentemente as respostas.

### HTTP Bidirecional {#server-mode-http-bidir}

*Obsoleto*

Funciona tanto como um I2PTunnel HTTP Server quanto como um I2PTunnel HTTP client sem capacidades de outproxy. Uma aplicação de exemplo seria uma aplicação web que faz solicitações do tipo cliente, ou teste de loopback de um Site I2P como ferramenta de diagnóstico.

### Servidor IRC {#server-mode-irc}

Cria um destino que filtra a sequência de registro de um cliente e passa a chave de destino do cliente como um nome de host para o servidor IRC.

### Streamr {#server-mode-streamr}

Um cliente UDP que se conecta a um servidor de mídia é criado. O Cliente UDP é acoplado com um servidor Streamr I2PTunnel.
