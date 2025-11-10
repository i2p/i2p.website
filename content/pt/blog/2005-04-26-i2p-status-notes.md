---
title: "Notas de status do I2P de 2005-04-26"
date: 2005-04-26
author: "jr"
description: "Atualização semanal breve abordando a estabilidade da rede 0.5.0.7, avanços no transporte UDP SSU com suporte a múltiplas redes e o financiamento da recompensa por testes unitários"
categories: ["status"]
---

Olá pessoal, breves notas semanais de status hoje

* Index

1) Estado da rede 2) Estado do SSU 3) Recompensa por teste unitário 4) ???

* 1) Net status

A maioria das pessoas atualizou para a versão 0.5.0.7 da semana passada bem rapidamente (obrigado!), e o resultado geral parece positivo. A rede parece bastante confiável e a limitação de tunnel que havia anteriormente foi resolvida. Ainda há problemas intermitentes relatados por alguns usuários, e estamos investigando as causas.

* 2) SSU status

Passo a maior parte do meu tempo focado no código UDP da versão 0.6, e não, ainda não está pronto para lançamento, e sim, há progresso ;) Neste momento, ele consegue lidar com várias redes, mantendo alguns pares em UDP e outros em TCP, com um desempenho bastante razoável. A parte difícil é tratar todos os casos de congestionamento/contenção, já que a rede em produção estará sob carga constante, mas houve bastante progresso nisso no último dia, mais ou menos. Mais novidades quando houver mais novidades.

* 3) Unit test bounty

Como duck mencionou na lista [1], zab aportou fundos iniciais para uma recompensa para ajudar o I2P com uma série de atualizações de testes - uma quantia para quem puder completar as tarefas listadas na página da recompensa [2]. Recebemos mais algumas doações para essa recompensa [3] - atualmente está em $1000USD. Embora as recompensas certamente não ofereçam "preço de mercado", elas são um pequeno incentivo para desenvolvedores que queiram ajudar.

[1] http://dev.i2p.net/pipermail/i2p/2005-April/000721.html [2] http://www.i2p.net/bounty_unittests [3] http://www.i2p.net/halloffame

* 4) ???

Ok, estou atrasado para a reunião de novo... Eu provavelmente deveria assinar e enviar isso, né? Dá uma passada na reunião e podemos discutir outras questões também.

=jr
