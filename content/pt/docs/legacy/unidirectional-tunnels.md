---
title: "Tunnels Unidirecionais"
description: "Resumo histórico do projeto de tunnel unidirecional do I2P."
slug: "unidirectional"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

> **Aviso histórico:** Esta página preserva a discussão legada sobre “Unidirectional Tunnels” (túneis unidirecionais) para referência. Consulte a [documentação de implementação de tunnel](/docs/specs/implementation/) ativa para o comportamento atual.

## Visão geral

O I2P constrói **tunnels unidirecionais**: um tunnel transporta o tráfego de saída e outro tunnel separado transporta as respostas de entrada. Essa estrutura remonta aos primeiros projetos de rede e continua sendo um importante diferencial em relação a sistemas de circuito bidirecional como o Tor. Para terminologia e detalhes de implementação, consulte a [visão geral de tunnel](/docs/overview/tunnel-routing/) e a [especificação de tunnel](/docs/specs/implementation/).

## Revisão

- Tunnels unidirecionais mantêm separados os tráfegos de requisição e de resposta, de modo que um único grupo de pares em conluio observa apenas metade de um trajeto de ida e volta.
- Ataques de temporização precisam cruzar dois pools de tunnels (saída e entrada) em vez de analisar um único circuito, elevando a dificuldade de correlação.
- Pools independentes de entrada e de saída permitem que routers ajustem latência, capacidade e características de tratamento de falhas por direção.
- Desvantagens incluem maior complexidade no gerenciamento de pares e a necessidade de manter múltiplos conjuntos de tunnels para uma entrega de serviço confiável.

## Anonimato

O artigo de Hermann e Grothoff, [*I2P is Slow… and What to Do About It*](http://grothoff.org/christian/i2p.pdf), analisa ataques de predecessor contra tunnels unidirecionais, sugerindo que adversários determinados podem, eventualmente, confirmar pares de longa duração. O feedback da comunidade observa que o estudo se baseia em suposições específicas sobre a paciência e os poderes legais do adversário e não compara a abordagem com ataques de temporização (timing attacks) que afetam projetos bidirecionais. Pesquisas contínuas e a experiência prática seguem reforçando os tunnels unidirecionais como uma escolha deliberada de anonimato, e não um descuido.
