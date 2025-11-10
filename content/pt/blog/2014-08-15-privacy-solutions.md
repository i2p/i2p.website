---
title: "O surgimento da Privacy Solutions"
date: 2014-08-15
author: "Meeh"
description: "Lançamento da organização"
categories: ["press"]
---

Olá a todos!

Hoje anunciamos o projeto Privacy Solutions, uma nova organização que desenvolve e mantém software I2P. A Privacy Solutions inclui vários novos esforços de desenvolvimento projetados para aprimorar a privacidade, a segurança e o anonimato dos usuários, com base nos protocolos e na tecnologia I2P.

Esses esforços incluem:

1. The Abscond browser bundle.
2. The i2pd C++ router project.
3. The "BigBrother" I2P network monitoring project.
4. The Anoncoin crypto-coin project.
5. The Monero crypto-coin project.

O financiamento inicial da Privacy Solutions foi fornecido pelos apoiadores dos projetos Anoncoin e Monero. A Privacy Solutions é um tipo de organização sem fins lucrativos sediada na Noruega, registrada nos registros do governo norueguês. (Algo como uma 501(c)3 dos EUA.)

A Privacy Solutions pretende solicitar financiamento ao governo norueguês para pesquisa em redes, por causa do BigBrother (voltaremos a explicar o que é) e das moedas que estão previstas para usar redes de baixa latência como camada de transporte principal. A nossa pesquisa apoiará avanços em tecnologia de software para anonimato, segurança e privacidade.

Primeiro, um pouco sobre o Abscond Browser Bundle. Inicialmente foi um projeto de uma pessoa só, criado pelo Meeh, mas depois amigos começaram a enviar patches (correções); o projeto agora está tentando criar o mesmo acesso fácil ao I2P que o Tor tem com seu pacote de navegador. Nosso primeiro lançamento não está longe; restam apenas algumas tarefas de scripts do Gitian, incluindo a configuração da Apple toolchain (cadeia de ferramentas). Mas, novamente, adicionaremos monitoramento com PROCESS_INFORMATION (uma struct em C que mantém informações vitais sobre um processo) a partir da instância Java para verificar o I2P antes de o declararmos estável. O I2pd também substituirá a versão em Java assim que estiver pronto, e não faz mais sentido incluir um JRE no pacote. Você pode ler mais sobre o Abscond Browser Bundle em https://hideme.today/dev

Também gostaríamos de informar o estado atual do i2pd. O i2pd agora oferece suporte a streaming bidirecional, o que permite usar não apenas HTTP, mas também canais de comunicação de longa duração. Já foi adicionado suporte a IRC. Os usuários do i2pd podem usá-lo da mesma forma que o Java I2P para acessar a rede de IRC do I2P. I2PTunnel é um dos recursos-chave da rede I2P, permitindo que aplicações não-I2P se comuniquem de forma transparente. É por isso que é um recurso vital para o i2pd e um dos marcos principais.

Por fim, se você está familiarizado com o I2P, provavelmente conhece o Bigbrother.i2p, que é um sistema de métricas que o Meeh criou há mais de um ano. Recentemente notamos que o Meeh na verdade tem 100Gb de dados não duplicados de nós que vêm reportando desde o lançamento inicial. Isso também será movido para a Privacy Solutions e reescrito com um back-end NSPOF (sem ponto único de falha). Com isso, também começaremos a usar o Graphite (http://graphite.wikidot.com/screen-shots). Isso nos dará uma ótima visão geral da rede sem problemas de privacidade para nossos usuários finais. Os clientes filtram todos os dados, exceto país, router hash e taxa de sucesso na construção de tunnel. O nome desse serviço é, como sempre, uma pequena piada do Meeh.

We have shorted down a bit of the news here, if you're interested in more information please visit https://blog.privacysolutions.no/ We're still under construction and more content will come!

Para mais informações, contacte: press@privacysolutions.no

Atenciosamente,

Mikal "Meeh" Villa
