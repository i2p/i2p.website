---
title: "Notas de status do I2P de 2006-04-18"
date: 2006-04-18
author: "jr"
description: "Melhorias de rede 0.6.1.16, análise do colapso por congestionamento na criação de tunnel, e atualizações do desenvolvimento do Feedspace"
categories: ["status"]
---

Olá, pessoal, chega mais uma terça-feira para nossas notas semanais de status

* Index

1) Estado da rede e 0.6.1.16 2) Criação de Tunnel e congestionamento 3) Feedspace 4) ???

* 1) Net status and 0.6.1.16

Com 70% da rede atualizada para 0.6.1.16, parece que estamos observando uma melhoria em relação a versões anteriores e, com os problemas corrigidos nessa versão, temos uma visão mais clara do nosso próximo gargalo.  Para aqueles que ainda não estão na 0.6.1.16, por favor, atualizem o quanto antes, pois versões anteriores rejeitarão solicitações de criação de tunnel de forma arbitrária (mesmo que o router tenha recursos suficientes para participar de mais tunnels).

* 2) Tunnel creation and congestion

No momento, parece que estamos enfrentando o que provavelmente é melhor descrito como colapso por congestionamento - solicitações de criação de tunnel estão sendo rejeitadas porque os routers estão com pouca largura de banda, então mais solicitações de criação de tunnel são enviadas na esperança de encontrar outros routers com recursos disponíveis, apenas para aumentar a largura de banda utilizada. Esse problema existe desde que migramos para a nova criptografia de criação de tunnel na versão 0.6.1.10 e pode ser substancialmente atribuído ao fato de que não recebemos feedback de aceitação/rejeição por salto (per-hop) até que (ou mais precisamente, *a menos que*) a solicitação e a resposta tenham percorrido o comprimento de dois tunnels. Se qualquer um desses pares falhar em encaminhar a mensagem, não saberemos qual par falhou, quais pares aceitaram e quais pares a rejeitaram explicitamente.

Já limitamos o número de solicitações concorrentes de criação de tunnel em andamento (e os testes mostram que aumentar o timeout não ajuda), então a solução tradicional de Nagle não é suficiente.  Estou experimentando alguns ajustes no nosso código de processamento de solicitações agora, para reduzir a frequência de descartes silenciosos de solicitações (em oposição a rejeições explícitas), e no nosso código de geração de solicitações para reduzir a concorrência sob carga.  Também estou testando outras melhorias que estão alcançando taxas de sucesso de construção de tunnel substancialmente maiores, embora ainda não estejam prontas para uso seguro.

Há luz no fim do tunnel, e agradeço a sua paciência em continuar connosco enquanto avançamos.  Espero que ainda esta semana tenhamos outra versão para disponibilizar algumas das melhorias; depois disso, reavaliaremos o estado da rede para verificar se o colapso por congestionamento está resolvido.

* 3) Feedspace

Frosk tem trabalhado intensamente no Feedspace e atualizou algumas páginas no site do Trac, incluindo um novo documento de visão geral, um conjunto de tarefas em aberto, alguns detalhes do banco de dados e mais. Dê uma passada em http://feedspace.i2p/ para ficar por dentro das mudanças mais recentes e, quem sabe, bombardear o Frosk com perguntas assim que for conveniente :)

* 4) ???

Isso é praticamente tudo o que estou pronto para discutir no momento, mas por favor, dê uma passada no #i2p para a nossa reunião mais tarde esta noite (8pm UTC) para conversarmos mais!

=jr
