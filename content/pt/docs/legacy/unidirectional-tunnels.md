---
title: "Tunnels Unidirecionais"
description: "Resumo histórico do design de tunnel unidirecional do I2P"
slug: "unidirectional"
aliases:
  - "/pt/unidirectional-tunnels"
  - "/pt/unidirectional-tunnels/"
lastUpdated: "2016-11"
accurateFor: "0.9.27"
---

## Visão Geral

Esta página descreve as origens e design dos tunnels unidirecionais do I2P. Para mais informações consulte:

- [Página de visão geral do tunnel](/docs/overview/tunnel-routing)
- [Especificação do tunnel](/docs/specs/tunnel-implementation)
- [Especificação de criação do tunnel](/docs/specs/tunnel-creation)
- [Discussão sobre design do tunnel](/docs/discussions/tunnel)
- [Seleção de pares](/docs/overview/peer-selection)

## Revisão

Embora não tenhamos conhecimento de qualquer pesquisa publicada sobre as vantagens dos tunnels unidirecionais, eles parecem tornar mais difícil detectar um padrão de solicitação/resposta, que é bastante possível de detectar em um tunnel bidirecional. Várias aplicações e protocolos, notavelmente HTTP, transferem dados dessa maneira. Ter o tráfego seguindo a mesma rota até seu destino e de volta poderia facilitar para um atacante que possui apenas dados de temporização e volume de tráfego inferir o caminho que um tunnel está tomando. Ter a resposta voltando por um caminho diferente possivelmente torna isso mais difícil.

Ao lidar com um adversário interno ou a maioria dos adversários externos, os tunnels unidirecionais do I2P expõem metade dos dados de tráfego que seriam expostos com circuitos bidirecionais simplesmente ao observar os fluxos em si - uma requisição e resposta HTTP seguiriam o mesmo caminho no Tor, enquanto no I2P os pacotes que compõem a requisição sairiam através de um ou mais tunnels de saída e os pacotes que compõem a resposta voltariam através de um ou mais tunnels de entrada diferentes.

A estratégia de usar dois tunnels separados para comunicação de entrada e saída não é a única técnica disponível, e ela tem implicações de anonimato. Do lado positivo, ao usar tunnels separados, reduz-se os dados de tráfego expostos para análise aos participantes em um tunnel - por exemplo, peers em um tunnel de saída de um navegador web veriam apenas o tráfego de um HTTP GET, enquanto os peers em um tunnel de entrada veriam a carga útil entregue através do tunnel. Com tunnels bidirecionais, todos os participantes teriam acesso ao fato de que, por exemplo, 1KB foi enviado em uma direção, depois 100KB na outra. Do lado negativo, usar tunnels unidirecionais significa que há dois conjuntos de peers que precisam ser perfilados e contabilizados, e cuidado adicional deve ser tomado para abordar a velocidade aumentada de ataques predecessor. O processo de agrupamento e construção de tunnel (estratégias de seleção e ordenação de peers) deve minimizar as preocupações do ataque predecessor.

## Anonimato

Um [artigo de Hermann e Grothoff](http://grothoff.org/christian/i2p.pdf) declarou que os tunnels unidirecionais do I2P "parecem ser uma decisão de design ruim".

O ponto principal do artigo é que as desanonimizações em tunnels unidirecionais levam mais tempo, o que é uma vantagem, mas que um atacante pode ter mais certeza no caso unidirecional. Portanto, o artigo afirma que isso não é uma vantagem de forma alguma, mas uma desvantagem, pelo menos com I2P Sites de longa duração.

Esta conclusão não é totalmente suportada pelo artigo. Os tunnels unidirecionais claramente mitigam outros ataques e não está claro como balancear o risco do ataque no artigo com ataques em uma arquitetura de tunnel bidirecional.

Esta conclusão é baseada em uma ponderação (tradeoff) arbitrária entre certeza vs. tempo que pode não ser aplicável em todos os casos. Por exemplo, alguém poderia fazer uma lista de IPs possíveis e então emitir intimações para cada um. Ou o atacante poderia realizar DDoS em cada um por vez e, através de um simples ataque de interseção, ver se o I2P Site fica fora do ar ou é ralentizado. Então "próximo" pode ser suficiente, ou o tempo pode ser mais importante.

A conclusão baseia-se numa ponderação específica da importância da certeza versus tempo, e essa ponderação pode estar errada, e é definitivamente discutível, especialmente num mundo real com intimações, mandados de busca e outros métodos disponíveis para confirmação final.

Uma análise completa das compensações entre tunnels unidirecionais vs. bidirecionais está claramente fora do escopo do artigo, e não foi feita em outro lugar. Por exemplo, como este ataque se compara aos numerosos ataques de temporização possíveis publicados sobre redes com roteamento onion? Claramente os autores não fizeram essa análise, se é que é possível fazê-la de forma eficaz.

O Tor usa tunnels bidirecionais e teve muito revisão acadêmica. O I2P usa tunnels unidirecionais e teve muito pouca revisão. A falta de um artigo de pesquisa defendendo tunnels unidirecionais significa que é uma escolha de design ruim, ou apenas que precisa de mais estudo? Ataques de temporização e ataques distribuídos são difíceis de defender tanto no I2P quanto no Tor. A intenção do design (veja referências acima) era que tunnels unidirecionais são mais resistentes a ataques de temporização. No entanto, o artigo apresenta um tipo um pouco diferente de ataque de temporização. Este ataque, por mais inovador que seja, é suficiente para rotular a arquitetura de tunnel do I2P (e assim o I2P como um todo) como um "design ruim", e por implicação claramente inferior ao Tor, ou é apenas uma alternativa de design que claramente precisa de mais investigação e análise? Há várias outras razões para considerar o I2P atualmente inferior ao Tor e outros projetos (tamanho pequeno da rede, falta de financiamento, falta de revisão), mas tunnels unidirecionais são realmente uma razão?

Em resumo, "decisão de design ruim" é aparentemente (já que o artigo não rotula tunnels bidirecionais como "ruins") uma forma abreviada de dizer que "tunnels unidirecionais são inequivocamente inferiores aos tunnels bidirecionais", mas essa conclusão não é apoiada pelo artigo.
