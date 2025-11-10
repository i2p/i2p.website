---
title: "Notas de status do I2P de 2005-03-15"
date: 2005-03-15
author: "jr"
description: "Notas semanais sobre o status do desenvolvimento do I2P, abrangendo análise de desempenho da rede, melhorias no cálculo de velocidade e desenvolvimento do Feedspace"
categories: ["status"]
---

Oi, pessoal, hora da atualização semanal

* Index

1) Estado da rede 2) Feedspace (espaço de feeds) 3) ???

* 1) Net status

Na última semana, grande parte do meu tempo foi dedicada a analisar o comportamento da rede, acompanhar estatísticas e tentar reproduzir vários eventos no simulador.  Embora parte do comportamento estranho da rede possa ser atribuída aos cerca de duas dúzias de routers ainda em versões antigas, o fator principal é que nossos cálculos de velocidade não estão nos fornecendo bons dados - não conseguimos identificar corretamente os pares que conseguem transferir dados rapidamente.  No passado, isso não era um grande problema, pois havia um bug que nos fazia usar os 8 pares de maior capacidade como o pool 'fast', em vez de construir níveis legítimos derivados da capacidade.  Nosso cálculo de velocidade atual é derivado de um teste periódico de latência (o RTT de um teste de tunnel, em particular), mas isso fornece dados insuficientes para termos confiança no valor.  O que precisamos é de uma forma melhor de coletar mais pontos de dados, ao mesmo tempo permitindo que pares de 'alta capacidade' sejam promovidos ao nível 'fast', conforme necessário.

To verify that this is the key problem we're facing, I cheated a bit and added functionality to manually select what peers should be used in a particular tunnel pool's selection.  With those explicitly chosen peers, I've had over two days on irc without disconnect and fairly reasonable performance w/ another service I control.  For the last two days or so, I've been trying out a new speed calculator using some new stats, and while it has improved selection, it still has some problems.  I've worked through a few alternatives this afternoon, but there's still work to be done to try 'em out on the net.

* 2) Feedspace

Frosk colocou no ar mais uma revisão da documentação do i2pcontent/fusenet, só que agora em um novo endereço com um novo nome: http://feedspace.i2p/ - veja o orion [1] ou meu blog [2] para o destino.  Isso parece realmente promissor, tanto sob a perspectiva de "ei, funcionalidade incrível" quanto de "ei, isso vai ajudar o anonimato do I2P".  Frosk e sua turma estão trabalhando a todo vapor, mas com certeza estão buscando feedback (e ajuda).  Talvez possamos pedir ao Frosk que nos dê uma atualização na reunião?

[1] http://orion.i2p/#feedspace.i2p [2] http://jrandom.dev.i2p/

* 3) ???

Ok, pode não parecer grande coisa, mas há muita coisa acontecendo, de verdade :) Tenho certeza de que também deixei algumas coisas de fora, então dê uma passada na reunião e veja o que está acontecendo.

=jr
