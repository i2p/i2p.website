---
title: "Tutorial básico de I2P Tunnels com imagens"
date: 2019-06-02
author: "idk"
description: "Configuração básica do i2ptunnel"
categories: ["tutorial"]
---

Embora o router Java I2P venha pré-configurado com um servidor web estático, o jetty, para fornecer o primeiro eepSite do usuário, muitos precisam de funcionalidades mais sofisticadas do seu servidor web e preferem criar um eepSite com um servidor diferente. Isso é, claro, possível e, na verdade, é bem fácil depois que você o faz pela primeira vez.

Embora seja fácil de fazer, há algumas coisas que você deve considerar antes de fazê-lo. Você vai querer remover características identificáveis do seu servidor web, como cabeçalhos potencialmente identificadores e páginas de erro padrão que informam o tipo de servidor/distribuição. Para mais informações sobre ameaças ao anonimato causadas por aplicações configuradas de forma incorreta, consulte: [Riseup aqui](https://riseup.net/en/security/network-security/tor/onionservices-best-practices), [Whonix aqui](https://www.whonix.org/wiki/Onion_Services), [este artigo de blog sobre algumas falhas de opsec (segurança operacional)](https://blog.0day.rocks/securing-a-web-hidden-service-89d935ba1c1d), [e a página de aplicações do I2P aqui](https://geti2p.net/docs/applications/supported). Embora grande parte dessas informações seja voltada para os Onion Services do Tor, os mesmos procedimentos e princípios se aplicam à hospedagem de aplicações sobre I2P.

### Passo Um: Abra o Assistente do Tunnel

Vá à interface da web do I2P em 127.0.0.1:7657 e abra o [Gerenciador de Serviços Ocultos](http://127.0.0.1:7657/i2ptunnelmgr) (aponta para o localhost). Clique no botão que diz "Tunnel Wizard" para começar.

### Passo Dois: Selecione um Tunnel de Servidor

O assistente de tunnel (túnel) é muito simples. Como estamos configurando um *servidor* http, tudo o que precisamos fazer é selecionar um tunnel *servidor*.

### Passo Três: Selecione um HTTP Tunnel

Um HTTP tunnel é o tipo de tunnel otimizado para hospedar serviços HTTP. Ele tem recursos de filtragem e limitação de taxa habilitados, ajustados especificamente para esse propósito. Um tunnel padrão também pode funcionar, mas, se você selecionar um tunnel padrão, será necessário cuidar desses recursos de segurança por conta própria. Uma análise mais aprofundada da configuração do HTTP Tunnel está disponível no próximo tutorial.

### Etapa Quatro: Dê um nome e uma descrição

Para seu próprio benefício e para facilitar lembrar e diferenciar para que você está usando o tunnel, dê a ele um bom apelido e uma descrição. Se precisar voltar mais tarde para fazer mais gerenciamento, é assim que você identificará o tunnel no gerenciador de serviços ocultos.

### Passo Cinco: Configurar o Host e a Porta

Nesta etapa, você aponta o servidor web para a porta TCP na qual o seu servidor web está ouvindo. Como a maioria dos servidores web ouve na porta 80 ou 8080, o exemplo mostra isso. Se você utilizar portas alternativas ou máquinas virtuais ou contêineres para isolar seus serviços web, talvez seja necessário ajustar o host, a porta ou ambos.

### Etapa Seis: Decida se deseja iniciá-lo automaticamente

Não consigo pensar em uma forma de detalhar melhor esta etapa.

### Passo Sete: Revise suas configurações

Por fim, confira as configurações que você selecionou. Se estiver de acordo, salve-as. Se você não optou por iniciar o tunnel automaticamente, vá ao gerenciador de serviços ocultos e inicie-o manualmente quando quiser disponibilizar seu serviço.

### Apêndice: Opções de Personalização do Servidor HTTP

O I2P fornece um painel detalhado para configurar o tunnel (túnel) do servidor HTTP de maneiras personalizadas. Vou encerrar este tutorial passando por todas elas. Mais cedo ou mais tarde.
