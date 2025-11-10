---
title: "Preferir Roteadores Próximos no Espaço de Chaves"
number: "116"
author: "chisquare"
created: "2015-04-25"
lastupdated: "2015-04-25"
status: "Needs-Research"
thread: "http://zzz.i2p/topics/1874"
---

## Visão Geral

Esta é uma proposta para organizar pares de modo que eles prefiram conectar-se a outros
pares que estejam próximos a eles no espaço de chaves.

## Motivação

A ideia é melhorar o sucesso na construção de túneis, aumentando a probabilidade de que
um roteador já esteja conectado a outro.

## Design

### Mudanças Necessárias

Esta mudança exigiria:

1. Cada roteador deve preferir conexões próximas a eles no espaço de chaves.
2. Cada roteador deve estar ciente de que cada roteador prefere conexões próximas a eles
   no espaço de chaves.

### Vantagens para a Construção de Túneis

Se você construir um túnel::

    A -longo-> B -curto-> C -curto-> D

(passo longo/aleatório vs. passo curto no espaço de chaves), você pode adivinhar onde a construção do túnel provavelmente falhou e tentar outro par naquele ponto. Além disso, permitiria detectar partes mais densas no espaço de chaves e fazer com que os roteadores simplesmente não as usassem, já que pode ser alguém conspirando.

Se você construir um túnel::

    A -longo-> B -longo-> C -curto-> D

e ele falhar, você pode inferir que é mais provável que tenha falhado em C -> D e
pode escolher outro ponto D.

Você também pode construir túneis de modo que o OBEP esteja mais próximo do IBGW e usar aqueles
túneis com OBEP que estejam mais próximos do IBGW determinado em um LeaseSet.

## Implicações de Segurança

Se você randomizar a colocação de passos curtos vs. longos no espaço de chaves, um
atacante provavelmente não obterá muita vantagem.

A maior desvantagem, no entanto, é que pode tornar a enumeração de usuários um pouco mais fácil.
