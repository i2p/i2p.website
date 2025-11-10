---
title: "Notas de status do I2P de 2006-02-28"
date: 2006-02-28
author: "jr"
description: "Melhorias na rede com a versão 0.6.1.12, roteiro para a versão 0.6.2 com novas estratégias de seleção de pares e oportunidades de miniprojetos"
categories: ["status"]
---

Ei, pessoal, hora de mais um dos nossos desabafos de terça-feira

* Index

1) Estado da rede e 0.6.1.12 2) Caminho para 0.6.2 3) Miniprojetos 4) ???

* 1) Net status and 0.6.1.12

Na semana passada houve melhorias substanciais na rede, primeiro com a ampla implantação da 0.6.1.11 na terça-feira passada, seguida pelo lançamento da 0.6.1.12 na segunda-feira passada (que já foi distribuída para 70% da rede até agora - obrigado!)  No geral, as coisas estão muito melhores do que na 0.6.1.10 e em versões anteriores — as taxas de sucesso na construção de tunnels estão uma ordem de grandeza mais altas, sem nenhum daqueles tunnels de contingência, a latência caiu, o uso de CPU caiu e a taxa de transferência aumentou. Além disso, com o TCP totalmente desativado, a taxa de retransmissão de pacotes está sob controle.

* 2) Road to 0.6.2

Ainda há melhorias a serem feitas no código de seleção de pares, pois ainda estamos vendo taxas de rejeição de client tunnel de 10-20%, e tunnels (túneis) de alta taxa de transferência (10+KBps) não são tão comuns quanto deveriam.  Por outro lado, agora que a carga de CPU caiu bastante, posso executar um router (roteador) adicional em dev.i2p.net sem causar problemas para meu router principal (que disponibiliza squid.i2p, www.i2p, cvs.i2p, syndiemedia.i2p e outros, atingindo 2-300+KBps).

Além disso, estou testando algumas melhorias para pessoas em redes altamente congestionadas (como assim, há pessoas que não estão?). Parece haver algum progresso nessa frente, mas serão necessários mais testes.  Isso deve, espero, ajudar as 4 ou 5 pessoas no irc2p que parecem ter dificuldade em manter conexões confiáveis (e, claro, ajudar também aqueles que sofrem em silêncio com os mesmos sintomas).

Depois que isso estiver funcionando bem, ainda temos um pouco de trabalho a fazer antes de podermos chamá-lo de 0.6.2 - precisamos das novas estratégias de ordenação de pares, além dessas estratégias aprimoradas de seleção de pares.  Como base, eu gostaria de obter três novas estratégias - = ordenação estrita (limitando o predecessor e o sucessor de cada par,
   com uma rotação baseada no MTBF) = extremos fixos (usando um par fixo como o gateway de entrada e
   a extremidade de saída) = vizinho limitado (usando um conjunto limitado de pares como o primeiro
   salto remoto)

Há outras estratégias interessantes a serem exploradas, mas essas três são as mais relevantes.  Uma vez implementadas, estaremos funcionalmente completos para a 0.6.2.  Estimativa vaga para março/abril.

* 3) Miniprojects

Há mais coisas úteis para fazer do que consigo contar, mas só quero chamar sua atenção para um post no meu blog descrevendo cinco pequenos projetos que um programador poderia implementar rapidamente sem investir muito tempo [1]. Se alguém se interessar em abraçar esses projetos, tenho certeza de que alocaríamos alguns recursos [2] do fundo geral como forma de agradecimento, embora eu saiba que a maioria de vocês é movida pelo desafio e não pelo dinheiro ;)

[1] http://syndiemedia.i2p.net:8000/blog.jsp?     blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&     entry=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=/1140652800002 [2] http://www.i2p.net/halloffame

* 4) ???

Enfim, isso é um breve resumo do que está acontecendo, até onde eu sei. Parabéns ao cervantes também pelo 500º usuário do fórum, a propósito :) Como sempre, dê uma passada no #i2p para a reunião daqui a alguns minutos!

=jr
