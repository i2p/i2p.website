---
title: "Meta-LeaseSet para Multihoming"
number: "120"
author: "zzz"
created: "2016-01-09"
lastupdated: "2016-01-11"
status: "Rejected"
thread: "http://zzz.i2p/topics/2045"
supercededby: "123"
---

## Visão Geral

Esta proposta trata da implementação de suporte adequado a multihoming no I2P que possa escalar para sites grandes.


## Motivação

O multihoming é um improviso e presumivelmente não funcionará, por exemplo, para facebook.i2p em larga escala. Digamos que tivéssemos 100 multihomes, cada um com 16 túneis, isso seria 1600 publicações de LS a cada 10 minutos, ou quase 3 por segundo. Os floodfills ficariam sobrecarregados e os limitadores entrariam em ação. E isso antes mesmo de mencionarmos o tráfego de pesquisa.

Precisamos de algum tipo de meta-LS, onde o LS liste os 100 hashes reais de LS. Isso seria de longa duração, muito mais longo que 10 minutos. Então é uma pesquisa em duas etapas para o LS, mas a primeira etapa poderia ser armazenada em cache por horas.


## Especificação

O meta-LeaseSet teria o seguinte formato::

  - Destino
  - Carimbo de Tempo de Publicação
  - Expiração
  - Flags
  - Propriedades
  - Número de entradas
  - Número de revogações

  - Entradas. Cada entrada contém:
    - Hash
    - Flags
    - Expiração
    - Custo (prioridade)
    - Propriedades

  - Revogações. Cada revogação contém:
    - Hash
    - Flags
    - Expiração

  - Assinatura

Flags e propriedades são incluídos para flexibilidade máxima.


## Comentários

Isso então poderia ser generalizado para ser uma pesquisa de serviço de qualquer tipo. O identificador do serviço é um hash SHA256.

Para ainda mais escalabilidade massiva, poderíamos ter múltiplos níveis, ou seja, um meta-LS poderia apontar para outros meta-LSes.
