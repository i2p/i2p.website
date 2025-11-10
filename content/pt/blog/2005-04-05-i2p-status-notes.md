---
title: "Notas de status do I2P para 2005-04-05"
date: 2005-04-05
author: "jr"
description: "Atualização semanal abordando problemas da versão 0.5.0.5, pesquisa sobre perfilamento bayesiano de pares e progresso da aplicação Q"
categories: ["status"]
---

Olá, pessoal, é hora da atualização semanal

* Index

1) 0.5.0.5 2) Perfilamento Bayesiano de pares 3) Q 4) ???

* 1) 0.5.0.5

A versão 0.5.0.5 da semana passada teve seus altos e baixos - a mudança principal para mitigar alguns ataques no netDb parece estar funcionando como esperado, mas expôs alguns bugs há muito tempo negligenciados na operação do netDb. Isso causou problemas de confiabilidade substanciais, especialmente para eepsites(Sites I2P). No entanto, os bugs foram identificados e tratados no CVS, e essas correções, entre algumas outras, serão lançadas como a versão 0.5.0.6 nas próximas 24 horas.

* 2) Bayesian peer profiling

bla vem pesquisando maneiras de melhorar nosso perfilamento de pares ao aproveitar uma filtragem bayesiana simples com base nas estatísticas coletadas [1]. Parece bastante promissor, embora eu não saiba em que ponto está no momento – talvez possamos obter uma atualização de bla durante a reunião?

[1] http://forum.i2p.net/viewtopic.php?t=598     http://theland.i2p/nodemon.html

* 3) Q

Há muito progresso em andamento com o aplicativo Q do aum, tanto na funcionalidade principal quanto com algumas pessoas desenvolvendo várias interfaces front-end xmlrpc. Há rumores de que poderemos ver outra build do Q neste fim de semana, com um monte de novidades descritas em http://aum.i2p/q/

* 4) ???

Ok, yeah, very brief status notes, as I got the timezones mixed up *again* (actually, I got the days mixed up too, thought it was Monday until a few hours ago). Anyway, there is lots of stuff going on not mentioned above, so swing on by the meeting and see whats up!

=jr
