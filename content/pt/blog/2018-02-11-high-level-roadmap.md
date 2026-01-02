---
title: "Roteiro de alto nível para 2018"
date: 2018-02-11
slug: "high-level-roadmap-for-2018"
author: "str4d"
description: "2018 será o ano de novos protocolos, novas colaborações e um foco mais refinado."
categories: ["roadmap"]
---

Uma das muitas coisas que discutimos no 34C3 foi em que deveríamos concentrar nossos esforços no próximo ano. Em particular, queríamos um roteiro que deixasse claro o que queremos garantir que será concluído, em contraste com o que seria muito bom ter, e que também nos ajudasse a integrar recém-chegados em qualquer uma das categorias. Eis o que definimos:

## Prioridade: Nova cripto(grafia!)

Muitas das primitivas e dos protocolos atuais ainda conservam seus projetos originais de por volta de 2005 e precisam de melhorias. Há vários anos temos diversas propostas abertas com ideias, mas o progresso tem sido lento. Todos concordamos que isso precisa ser a nossa prioridade máxima para 2018. Os componentes centrais são:

- New transport protocols (to replace NTCP and SSU). See Prop111.
- New onion-encryption protocol for building and using tunnels.
- New NetDB datatypes to enable enhanced Destinations. See Prop123.
- Upgraded end-to-end protocol (replacing ElGamal).

O trabalho nesta prioridade abrange várias áreas:

- Writing proposals.
- Writing working implementations of them that we can test.
- Reviewing proposals.

We cannot release new protocol specifications across the entire network without work on all of these areas.

## Desejável: Reutilização de código

Uma das vantagens de começar agora o trabalho mencionado acima é que, nos últimos anos, houve esforços independentes para criar protocolos simples e frameworks de protocolos que alcançam muitos dos objetivos que temos para os nossos próprios protocolos e ganharam adoção na comunidade mais ampla. Ao aproveitar esse trabalho, obtemos um "efeito multiplicador":

- We benefit from protocol designs, security proofs, and code written by others, reducing the amount of work we need to do for the same level of feature-completeness and security assurances.

- Work we do can be leveraged by other communities, increasing their interest in collaborating with us, and thinking about I2P as a whole.

As minhas propostas, em particular, irão tirar proveito do [Noise Protocol Framework](https://noiseprotocol.org/) e do [SPHINX packet format](https://katzenpost.mixnetworks.org/docs/specs/sphinx.html). Tenho colaborações combinadas com várias pessoas fora do I2P para isso!

## Prioridade: colaboração com a Clearnet (internet aberta)

Sobre esse assunto, temos aumentado o interesse gradualmente ao longo dos últimos seis meses, aproximadamente. Durante o PETS2017, o 34C3 e o RWC2018, tive discussões muito boas sobre maneiras de melhorar a colaboração com a comunidade mais ampla. Isso é muito importante para garantir que possamos obter o máximo de revisão possível para novos protocolos. O maior obstáculo que tenho visto é o fato de que a maior parte da colaboração no desenvolvimento de I2P atualmente acontece dentro do próprio I2P, o que aumenta significativamente o esforço necessário para contribuir.

As duas prioridades nesta área são:

- Set up a project-run development forum that is accessible both inside and outside I2P.

- Set up mailing lists for review and discussion of proposals (possibly connected to the above forum).

Outros objetivos considerados desejáveis (mas não essenciais):

- Set up a usable git-to-mtn pathway, to enable us to effectively solicit clearnet contributions on GitHub while keeping the canonical dev environment on Monotone.

- Write a "position paper" that accurately explains I2P to academic audiences, and puts it in context with existing literature.

Espero que as colaborações com pessoas fora do I2P sejam realizadas inteiramente no GitHub, com o mínimo de atrito.

## Prioridade: Preparação para versões de longa duração

O I2P agora está no Debian Sid (o repositório instável do Debian), que deverá se estabilizar em cerca de um ano e meio, e também foi incorporado ao repositório do Ubuntu para inclusão na próxima versão LTS em abril. Vamos começar a ter versões do I2P que acabarão permanecendo por anos, e precisamos garantir que possamos lidar com sua presença na rede.

O objetivo principal aqui é implantar, ao longo do próximo ano, o maior número possível de novos protocolos, tanto quanto for viável, para coincidir com a próxima versão estável do Debian. Para aqueles que exigirem implantações plurianuais, devemos incorporar as alterações de compatibilidade futura o mais cedo possível.

## Prioridade: Transformação dos aplicativos atuais em plugins

O modelo do Debian incentiva a existência de pacotes separados para componentes distintos. Concordamos que desacoplar os aplicativos Java atualmente empacotados do router Java principal seria benéfico por várias razões:

- It codifies the boundary between the applications and the router.

- It should make it easier to get these apps running with non-Java routers.

- It would enable third parties to create "I2P bundles" containing just the applications they want.

Em combinação com as prioridades anteriores, isso move o projeto principal do I2P mais na direção, por exemplo, do kernel do Linux. Dedicaremos mais tempo a nos concentrar na própria rede, deixando que desenvolvedores de terceiros se concentrem em aplicações que utilizam a rede (algo que é significativamente mais fácil de fazer após nosso trabalho nos últimos anos em APIs e bibliotecas).

## Desejável: melhorias no aplicativo

Há uma série de melhorias no nível de aplicativo nas quais queremos trabalhar, mas, considerando nossas outras prioridades, no momento não temos recursos de desenvolvimento para isso. Esta é uma área na qual adoraríamos ver novos colaboradores! Assim que o desacoplamento mencionado acima estiver concluído, será significativamente mais fácil para alguém trabalhar em um aplicativo específico de forma independente do router Java principal.

Um desses aplicativos com o qual adoraríamos receber ajuda é o I2P Android. Nós o manteremos atualizado com as versões do núcleo do I2P e corrigiremos bugs na medida do possível, mas há muito que pode ser feito para melhorar tanto o código subjacente quanto a usabilidade.

## Prioridade: estabilização do Susimail e do I2P-Bote

Dito isso, queremos trabalhar especificamente em correções para o Susimail e o I2P-Bote no curto prazo (algumas das quais já foram incluídas na versão 0.9.33). Eles tiveram menos desenvolvimento nos últimos anos do que outros aplicativos do I2P e, por isso, queremos dedicar algum tempo para colocar suas bases de código em dia e torná-los mais acessíveis para novos contribuidores!

## Desejável: triagem de tíquetes

Temos um grande volume de tickets pendentes em vários subsistemas e aplicativos do I2P. Como parte do esforço de estabilização descrito acima, gostaríamos de resolver alguns dos nossos problemas mais antigos, de longa data. Mais importante ainda, queremos garantir que nossos tickets estejam corretamente organizados, para que novos colaboradores possam encontrar bons tickets em que trabalhar.

## Prioridade: Suporte ao usuário

Um dos aspectos acima nos quais vamos nos concentrar é manter contato com os usuários que dedicam tempo para relatar problemas. Obrigado! Quanto menor conseguirmos tornar o ciclo de feedback, mais rapidamente poderemos resolver os problemas que novos usuários enfrentam, e maior a probabilidade de que continuem participando da comunidade.

## Gostaríamos muito da sua ajuda!

Isso tudo parece muito ambicioso, e é! Mas muitos dos itens acima se sobrepõem e, com um planejamento cuidadoso, podemos fazer um progresso significativo neles.

Se você tiver interesse em ajudar com quaisquer dos objetivos acima, venha conversar conosco! Você pode nos encontrar no OFTC e no Freenode (#i2p-dev) e no Twitter (@GetI2P).
