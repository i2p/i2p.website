---
title: "Notas de status do I2P de 2004-11-30"
date: 2004-11-30
author: "jr"
description: "Atualização semanal de status do I2P cobrindo os lançamentos 0.4.2 e 0.4.2.1, desenvolvimentos no mail.i2p, progresso do i2p-bt e discussões sobre segurança de eepsite"
categories: ["status"]
---

Oi, pessoal

## Índice

1. 0.4.2 and 0.4.2.1
2. mail.i2p
3. i2p-bt
4. eepsites(I2P Sites)
5. ???

## 1) 0.4.2 e 0.4.2.1

Desde que finalmente lançamos a versão 0.4.2, a confiabilidade e a taxa de transferência da rede dispararam por um tempo, até esbarrarmos nos bugs novinhos que nós mesmos criamos. Para a maioria das pessoas, as conexões de IRC estão durando horas a fio, embora, para alguns que enfrentaram parte dos problemas, tem sido um caminho acidentado. Ainda assim, houve uma série de correções e, mais tarde hoje à noite ou amanhã bem cedo, teremos uma nova versão 0.4.2.1 pronta para download.

## 2) mail.i2p

Hoje mais cedo recebi discretamente uma mensagem do postman dizendo que ele tinha algumas coisas que queria discutir - para mais informações, veja os logs da reunião (ou, se você estiver lendo isto antes da reunião, apareça por lá).

## 3) i2p-bt

Uma das desvantagens da nova versão é que estamos enfrentando alguns problemas com o porte do i2p-bt. Alguns dos problemas foram identificados e corrigidos na biblioteca de streaming, mas ainda é necessário mais trabalho para deixá-lo no estado em que precisamos que esteja.

## 4) eepsites(Sites do I2P)

Tem havido alguma discussão ao longo dos meses na lista, no canal e no fórum sobre alguns problemas com a forma como os eepsites(I2P Sites) e o eepproxy funcionam - recentemente, alguns mencionaram problemas com como e quais cabeçalhos são filtrados, outros apontaram os perigos de navegadores mal configurados, e há também a página do DrWoo que resume muitos dos riscos. Um evento particularmente digno de nota é o fato de que algumas pessoas estão trabalhando ativamente em applets que sequestrarão o computador do usuário se o usuário não desativar os applets. (PORTANTO, DESATIVE JAVA E JAVASCRIPT NO SEU NAVEGADOR)

Isso, claro, leva a uma discussão sobre como podemos proteger as coisas. Ouvi sugestões de criar nosso próprio navegador ou de distribuir um com configurações de segurança pré-configuradas, mas sejamos realistas - isso é muito mais trabalho do que qualquer pessoa aqui estaria disposta a encarar. No entanto, há três outras vertentes:

1. Use a fascist HTML filter and tie it in with the proxy
2. Use a fascist HTML filter as part of a script that fetches pages for you
3. Use a secure macro language

A primeira é praticamente o que temos hoje, exceto que filtramos o conteúdo renderizado por meio de algo como o muffin ou o filtro de anonimato do freenet. A desvantagem aqui é que isso ainda expõe os cabeçalhos HTTP, então teríamos que anonimizar também o lado HTTP.

A segunda é muito parecida com o que você pode ver em `http://duck.i2p/` com o CGIproxy, ou, alternativamente, como você pode ver no fproxy do Freenet. Isso também cuida da parte HTTP.

A terceira tem seus benefícios e desvantagens - ela nos permite usar interfaces muito mais atraentes (já que podemos usar com segurança algum javascript conhecido como seguro, etc), mas tem a desvantagem de incompatibilidade com versões anteriores. Talvez uma mescla disso com um filtro, permitindo que você incorpore as macros em html filtrado?

De qualquer forma, este é um esforço de desenvolvimento importante e aborda um dos usos mais atraentes do I2P - sites interativos seguros e anônimos. Talvez alguém tenha outras ideias ou informações sobre como poderíamos obter o que é necessário?

## 5) ???

Ok, estou atrasado para a reunião, então acho que devo assinar isso e enviá-lo adiante, né?

=jr [vamos ver se eu consigo fazer o gpg funcionar direito...]
