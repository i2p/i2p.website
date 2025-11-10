---
title: "Notas de status do I2P de 2005-03-29"
date: 2005-03-29
author: "jr"
description: "Notas semanais sobre o status do desenvolvimento do I2P cobrindo o lançamento 0.5.0.5 com processamento em lotes (batching), protocolo de transporte UDP (SSU) e armazenamento distribuído Q"
categories: ["status"]
---

Oi pessoal, é hora das notas de status semanais

* Index

1) 0.5.0.5 2) UDP (SSU) 3) Q 4) ???

* 1) 0.5.0.5

Since y'all did such a great job at upgrading to 0.5.0.4 so quickly, we're going to have the new 0.5.0.5 release come out after the meeting.  As discussed last week, the big change is the inclusion of the batching code, bundling multiple small messages together, rather than giving them each their own full 1KB tunnel message.  While this alone won't be revolutionary, it should substantially reduce the number of messages passed, as well as the bandwidth used, especially for services like IRC.

Haverá mais informações no anúncio da versão, mas outras duas coisas importantes surgem com a revisão 0.5.0.5. Primeiro, estamos descontinuando o suporte para usuários em versões anteriores à 0.5.0.4 — há bem mais de 100 usuários na 0.5.0.4, e há problemas substanciais nas versões anteriores. Em segundo lugar, há uma correção importante de anonimato no novo build que, embora exigisse algum esforço de desenvolvimento para ser montada, não é implausível. A maior parte da mudança é na forma como gerimos o netDb — em vez de agir de forma descuidada e armazenar em cache entradas por toda parte, só responderemos a solicitações do netDb por elementos que nos tenham sido explicitamente fornecidos, independentemente de termos ou não os dados em questão.

Como sempre, há correções de bugs e alguns novos recursos, mas mais informações serão divulgadas no anúncio de lançamento.

* 2) UDP (SSU)

Como discutido de forma intermitente nos últimos 6-12 meses, vamos migrar para UDP para nossa comunicação entre routers assim que a versão 0.6 for lançada. Para avançarmos nesse caminho, temos um primeiro rascunho do protocolo de transporte disponível no CVS @ http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/udp.html?rev=HEAD

É um protocolo relativamente simples, com os objetivos descritos no documento, e explora as capacidades do I2P para tanto autenticar quanto proteger dados, bem como expor o mínimo possível de informações externas. Nem mesmo a primeira parte do handshake de conexão é identificável por alguém que não esteja executando o I2P. O comportamento do protocolo ainda não está totalmente definido na especificação, por exemplo, como os temporizadores disparam ou como os três diferentes indicadores de estado semiconfiáveis são usados, mas cobre o básico de criptografia, empacotamento e NAT hole punching (perfuração de NAT). Nada disso foi implementado ainda, mas será em breve, então feedback seria muito bem-vindo!

* 3) Q

Aum tem trabalhado intensamente no Q(uartermaster), um armazenamento distribuído, e o primeiro rascunho da documentação já está no ar [1]. Uma das ideias interessantes ali parece ser se afastar de uma DHT simples (tabela hash distribuída) em direção a um sistema ao estilo memcached [2], com cada usuário realizando quaisquer buscas inteiramente *localmente* e solicitando os dados propriamente ditos ao servidor Q "diretamente" (bem, através do I2P). De qualquer forma, há coisas interessantes; talvez, se o Aum estiver acordado [3], consigamos arrancar dele uma atualização?

[1] http://aum.i2p/q/ [2] http://www.danga.com/memcached/ [3] malditos fusos horários!

* 4) ???

Muita coisa acontecendo e, se faltasse mais do que apenas alguns minutos para a reunião, eu poderia continuar, mas é a vida. Dá uma passada por aqui

# i2p in a few to chat.

=jr
