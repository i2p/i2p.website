---
title: "Coleta de Estatísticas com Opt-in"
number: "117"
author: "zab"
created: "2015-11-04"
lastupdated: "2015-11-04"
status: "Rascunho"
thread: "http://zzz.i2p/topics/1981"
---

## Visão Geral

Esta proposta é sobre um sistema automatizado de relatório para coleta de estatísticas na rede, com consentimento do usuário.


## Motivação

Atualmente, existem vários parâmetros de rede que foram determinados por suposições fundamentadas. Suspeita-se que alguns deles possam ser ajustados para melhorar o desempenho geral da rede em termos de velocidade, confiabilidade, e assim por diante. No entanto, alterá-los sem pesquisa adequada é muito arriscado.


## Design

O roteador suporta uma vasta coleção de estatísticas que podem ser usadas para analisar propriedades da rede como um todo. O que precisamos é um sistema automatizado de relatório que colete essas estatísticas em um local centralizado. Naturalmente, isso seria opt-in, pois compromete fortemente o anonimato. (As estatísticas que respeitam a privacidade já são reportadas para stats.i2p) De modo geral, para uma rede de tamanho 30.000, uma amostra de 300 roteadores de relatório deve ser suficientemente representativa.
