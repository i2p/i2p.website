---
title: "Roteiro de alto nível para 2018"
date: 2018-02-11
slug: "high-level-roadmap-for-2018"
author: "str4d"
description: "2018 será o ano de novos protocolos, novas colaborações e um foco mais apurado"
categories: ["roadmap"]
---

Uma das muitas coisas que discutimos no 34C3 foi em que deveríamos nos concentrar para o próximo ano. Em particular, queríamos um roadmap (plano de ação) que fosse claro sobre o que queremos garantir que faremos, versus o que seria realmente bom ter, e que também nos permitisse ajudar a integrar os recém-chegados em qualquer uma das categorias. Aqui está o que elaboramos:

## Prioridade: Nova cripto(grafia!)

Muitas das primitivas e protocolos atuais ainda mantêm seus projetos originais de por volta de 2005 e precisam de melhorias. Temos tido várias propostas abertas há vários anos com ideias, mas o progresso tem sido lento. Todos concordamos que isso precisa ser nossa principal prioridade para 2018. Os componentes centrais são:

- New transport protocols (to replace NTCP and SSU). See [Prop111](https://geti2p.net/spec/proposals/111).
- New onion-encryption protocol for building and using tunnels.
- New NetDB datatypes to enable enhanced Destinations. See [Prop123](https://geti2p.net/spec/proposals/123).
- Upgraded end-to-end protocol (replacing ElGamal).

O trabalho nesta prioridade se divide em várias áreas:

- Writing proposals.
- Writing working implementations of them that we can test.
- Reviewing proposals.

Não podemos lançar novas especificações de protocolo em toda a rede sem trabalhar em todas essas áreas.

## Desejável: Reutilização de código

Um dos benefícios de iniciar o trabalho mencionado acima agora é que, nos últimos anos, houve esforços independentes para criar protocolos simples e frameworks de protocolo que atendem a muitos dos objetivos que temos para nossos próprios protocolos, e que ganharam adoção na comunidade mais ampla. Ao aproveitar esse trabalho, obtemos um efeito de "multiplicador de força":

- We benefit from protocol designs, security proofs, and code written by others, reducing the amount of work we need to do for the same level of feature-completeness and security assurances.

- Work we do can be leveraged by other communities, increasing their interest in collaborating with us, and thinking about I2P as a whole.

As minhas propostas, em particular, irão utilizar o [Noise Protocol Framework](https://noiseprotocol.org/) e o [formato de pacote SPHINX](https://katzenpost.mixnetworks.org/docs/specs/sphinx.html). Tenho colaborações já combinadas com várias pessoas fora do I2P para estas!

## Prioridade: Colaboração com a Clearnet (internet aberta)

A esse respeito, temos aumentado o interesse aos poucos nos últimos seis meses, aproximadamente. Durante PETS2017, 34C3 e RWC2018, tive discussões muito boas sobre maneiras de melhorar a colaboração com a comunidade mais ampla. Isso é realmente importante para garantir que possamos obter o máximo de revisão possível para novos protocolos. O principal entrave que tenho observado é o fato de que a maior parte da colaboração no desenvolvimento de I2P atualmente acontece dentro do próprio I2P, o que aumenta significativamente o esforço necessário para contribuir.

As duas prioridades nesta área são:

- Set up a project-run development forum that is accessible both inside and outside I2P.

- Set up mailing lists for review and discussion of proposals (possibly connected to the above forum).

Outros objetivos classificados como desejáveis:

- Set up a usable git-to-mtn pathway, to enable us to effectively solicit clearnet contributions on GitHub while keeping the canonical dev environment on Monotone.

- Write a "position paper" that accurately explains I2P to academic audiences, and puts it in context with existing literature.

Espero que as colaborações com pessoas de fora do I2P sejam feitas inteiramente no GitHub, para minimizar o atrito.

## Prioridade: Preparação para versões de longa duração

O I2P agora está no Debian Sid (o repositório instável deles), que se estabilizará em cerca de um ano e meio, e também foi incorporado ao repositório do Ubuntu para inclusão na próxima versão LTS em abril. Vamos começar a ter versões do I2P que acabarão permanecendo por anos, e precisamos garantir que podemos lidar com a presença delas na rede.

O objetivo principal aqui é implementar, no próximo ano, o máximo possível dos novos protocolos, para entrar na próxima versão estável do Debian. Para aqueles que exigirem implantações plurianuais, devemos incorporar as alterações de compatibilidade futura o mais cedo possível.

## Prioridade: Transformação dos aplicativos atuais em plugins

O modelo do Debian incentiva o uso de pacotes separados para componentes distintos. Concordamos que desacoplar as aplicações Java atualmente incluídas do router Java principal seria benéfico por várias razões:

- It codifies the boundary between the applications and the router.

- It should make it easier to get these apps running with non-Java routers.

- It would enable third parties to create "I2P bundles" containing just the applications they want.

Em combinação com as prioridades anteriores, isso orienta o projeto principal do I2P mais na direção, por exemplo, do kernel do Linux. Vamos dedicar mais tempo a focar na própria rede, deixando que os desenvolvedores de terceiros se concentrem em aplicações que usam a rede (algo que é significativamente mais fácil de fazer depois do nosso trabalho nos últimos anos em APIs e bibliotecas).

## Desejável: Melhorias no aplicativo

Há várias melhorias em nível de aplicativo nas quais queremos trabalhar, mas, no momento, não temos tempo de desenvolvimento para isso, dadas nossas outras prioridades. Esta é uma área na qual adoraríamos ver novos colaboradores! Assim que o desacoplamento acima estiver concluído, será significativamente mais fácil para alguém trabalhar em um aplicativo específico de forma independente do router Java principal.

Um desses aplicativos para o qual adoraríamos receber ajuda é o I2P Android. Nós o manteremos atualizado com os lançamentos do núcleo do I2P e corrigiremos bugs na medida do possível, mas há muito que pode ser feito para melhorar o código subjacente, bem como a usabilidade.

## Prioridade: estabilização do Susimail e do I2P-Bote

Dito isso, queremos de fato trabalhar especificamente em correções para o Susimail e o I2P-Bote no curto prazo (algumas das quais já foram incluídas na 0.9.33). Esses projetos receberam menos atenção nos últimos anos do que outros aplicativos do I2P e, por isso, queremos dedicar algum tempo a colocar suas bases de código em dia e torná-los mais fáceis para que novos contribuidores comecem a se envolver!

## Desejável: Triagem de tickets

Temos um grande acúmulo de tickets em vários subsistemas e aplicativos do I2P. Como parte do esforço de estabilização acima, gostaríamos muito de resolver e encerrar alguns dos nossos problemas mais antigos e de longa data. Mais importante ainda, queremos garantir que os nossos tickets estejam corretamente organizados, para que novos contribuidores possam encontrar bons tickets em que trabalhar.

## Prioridade: Suporte ao usuário

One aspect of the above we will be focusing on is keeping in touch with users who take the time to report issues. Thank you! The smaller we can make the feedback loop, the quicker we can resolve problems that new users face, and the more likely it is that they keep participating in the community.

## Adoraríamos a sua ajuda!


Isso tudo parece muito ambicioso, e é! Mas muitos dos itens acima se sobrepõem e, com um planejamento cuidadoso, podemos fazer um progresso significativo neles.

Se você estiver interessado em ajudar com qualquer um dos objetivos acima, venha conversar conosco! Você pode nos encontrar na OFTC e na Freenode (#i2p-dev), e no Twitter (@GetI2P).
