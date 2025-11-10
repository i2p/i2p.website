---
title: "Notas de status do I2P de 2005-06-28"
date: 2005-06-28
author: "jr"
description: "Atualização semanal abordando planos de implantação do transporte SSU, conclusão da recompensa por testes unitários e considerações de licenciamento, e status do Kaffe Java"
categories: ["status"]
---

Olá, pessoal, é hora da atualização semanal de novo

* Index

1) Estado do SSU 2) Estado dos testes unitários 3) Estado do Kaffe 4) ???

* 1) SSU status

There has been some more progress on the SSU transport, and my current thinking will be that after some more live net testing, we'll be able to deploy as 0.6 without much delay. The first SSU release will not include support for people who cannot poke a hole in their firewall or adjust their NAT, but that will be rolled out in 0.6.1. After 0.6.1 is out, tested, and kicking ass (aka 0.6.1.42), we'll move on over to 1.0.

Minha inclinação pessoal é abandonar completamente o transporte TCP à medida que o transporte SSU é implantado, para que as pessoas não precisem manter ambos habilitados (encaminhando portas TCP e UDP) e para que os desenvolvedores não precisem manter código que não é necessário. Alguém tem alguma opinião forte sobre isso?

* 2) Unit test status

Como mencionado na semana passada, Comwiz se apresentou para reivindicar a primeira fase da recompensa por testes unitários (viva, Comwiz!  obrigado ao duck & ao zab por financiarem a recompensa também!). O código foi submetido ao CVS e, dependendo da sua configuração local, você talvez consiga gerar os relatórios do junit e do clover entrando no diretório i2p/core/java e executando "ant test junit.report" (espere cerca de uma hora...) e depois ver i2p/reports/core/html/junit/index.html. Por outro lado, você pode executar "ant useclover test junit.report clover.report" e ver i2p/reports/core/html/clover/index.html.

A desvantagem de ambos os conjuntos de testes tem a ver com aquele conceito tolo que a classe dominante chama de "lei de direitos autorais". Clover é um produto comercial, embora o pessoal da cenqua permita seu uso gratuito por desenvolvedores de código aberto (e eles gentilmente concordaram em nos conceder uma licença). Para gerar os relatórios do clover, você precisa ter o clover instalado localmente - eu tenho o clover.jar em ~/.ant/lib/, ao lado do meu arquivo de licença. A maioria das pessoas não vai precisar do clover e, como publicaremos os relatórios na web, não há perda de funcionalidade por não instalá-lo.

Por outro lado, acabamos sendo prejudicados pelo outro lado da lei de direitos autorais quando levamos em consideração o próprio framework de testes unitários - o junit é distribuído sob a IBM Common Public License 1.0, que, de acordo com a FSF [1], não é compatível com a GPL. Agora, embora não tenhamos nenhum código GPL (pelo menos não no núcleo ou no router), ao olharmos para nossa política de licenciamento [2], nosso objetivo, nos detalhes de como licenciamos as coisas, é permitir que o maior número possível de pessoas use o que está sendo criado, pois o anonimato adora companhia.

[1] http://www.fsf.org/licensing/licenses/index_html#GPLIncompatibleLicenses [2] http://www.i2p.net/licenses

Como algumas pessoas inexplicavelmente distribuem software sob a GPL, faz sentido que nos esforcemos para permitir que elas usem o I2P sem restrições. No mínimo, isso significa que não podemos permitir que a funcionalidade efetiva que expomos dependa de código licenciado sob a CPL (por exemplo, junit.framework.*). Eu gostaria de estender isso para incluir também os testes unitários, mas o junit parece ser a língua franca dos frameworks de teste (e não acho que seria nem de longe sensato dizer "ei, vamos criar nosso próprio framework de teste unitário de domínio público!", considerando nossos recursos).

Dado tudo isso, eis o que estou pensando. Vamos incluir o junit.jar no CVS e usá-lo quando os testes unitários forem executados, mas os próprios testes unitários não serão incluídos em i2p.jar ou router.jar, e não serão distribuídos nos lançamentos. Podemos disponibilizar um conjunto adicional de JARs (i2p-test.jar e router-test.jar), se necessário, mas esses não seriam utilizáveis por aplicações licenciadas sob a GPL (já que dependem de junit).

=jr
