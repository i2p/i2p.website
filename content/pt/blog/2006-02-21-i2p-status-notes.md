---
title: "Notas de status do I2P de 2006-02-21"
date: 2006-02-21
author: "jr"
description: "Problemas de rede com a versão 0.6.1.10, lançamento subsequente rápido 0.6.1.11 e preocupações de segurança no IE"
categories: ["status"]
---

Oi, pessoal, é terça-feira de novo

* Index

1) Estado da rede 2) ???

* 1) Net status

A rede tem passado por alguma turbulência com o lançamento 0.6.1.10, devido em parte à incompatibilidade com versões anteriores, mas também a bugs inesperados. Nem a confiabilidade nem o tempo de atividade na 0.6.1.10 foram suficientes, então, nos últimos 5 dias, houve uma série de correções, culminando no novo lançamento 0.6.1.11 - http://dev.i2p.net/pipermail/i2p/2006-February/001263.html

A maioria dos bugs encontrados na 0.6.1.10 já estava presente desde o lançamento 0.6 em setembro passado, mas não eram prontamente aparentes enquanto havia transportes alternativos aos quais recorrer (TCP). Minha rede de teste local simula falhas de pacotes, mas de fato não cobria o router churn (alta rotatividade de router) e outras falhas persistentes de rede. A rede de teste _PRE também incluía um conjunto auto-selecionado de pares razoavelmente confiáveis, assim, havia situações significativas que não foram totalmente exploradas antes do lançamento completo. Isso é um problema, obviamente, e da próxima vez vamos garantir a inclusão de uma seleção mais ampla de cenários.

* 2) ???

Há várias coisas acontecendo no momento, mas a nova versão 0.6.1.11 pulou para o topo da fila. A rede continuará um pouco instável até que um grande número de pessoas esteja atualizado; depois disso, o trabalho continuará avançando. Vale mencionar que o cervantes está trabalhando em algum tipo de exploit de domínio de segurança relacionado ao IE e, embora eu não saiba se ele está pronto para explicar os detalhes, resultados preliminares sugerem que é viável; portanto, quem se preocupa com o anonimato deve evitar o IE por enquanto (mas você já sabia disso de qualquer forma ;). Talvez o cervantes possa nos dar um resumo na reunião?

Enfim, é tudo o que tenho para mencionar no momento - dá uma passada na reunião daqui a alguns minutos para dar um oi!

=jr
