---
title: "Implementação antiga do Tunnel (Legado)"
description: "Descrição arquivada do projeto do tunnel utilizado antes do I2P 0.6.1.10."
slug: "old-implementation"
lastUpdated: "2005-06"
accurateFor: "0.6.1"
reviewStatus: "needs-review"
---

> **Status legado:** Este conteúdo é mantido apenas para referência histórica. Ele documenta o sistema de tunnels que foi distribuído antes do I2P&nbsp;0.6.1.10 e não deve ser usado para desenvolvimento moderno. Consulte a [implementação atual](/docs/specs/implementation/) para orientações de produção.

O subsistema de tunnel original também usava tunnels unidirecionais, mas diferia no formato das mensagens, na detecção de duplicados e na estratégia de construção. Muitas seções abaixo espelham a estrutura do documento descontinuado para facilitar a comparação.

## 1. Visão geral do Tunnel

- Os tunnels eram construídos como sequências ordenadas de pares selecionados pelo criador.
- Os comprimentos dos tunnels variavam de 0–7 saltos, com vários ajustes para padding (preenchimento), throttling (limitação de taxa) e geração de chaff (tráfego falso).
- Os tunnels de entrada entregavam mensagens de um gateway não confiável ao criador (ponto final); os tunnels de saída direcionavam os dados para longe do criador.
- A vida útil dos tunnels era de 10 minutos; depois disso, novos tunnels eram construídos (frequentemente usando os mesmos pares, mas IDs de tunnel diferentes).

## 2. Operação no Design Legado

### 2.1 Pré-processamento de mensagens

Os gateways acumularam ≤32&nbsp;KB de carga útil I2NP, selecionaram o preenchimento e produziram uma carga útil contendo:

- Um campo de comprimento de preenchimento de dois bytes e o mesmo número de bytes aleatórios
- Uma sequência de pares `{instructions, I2NP message}` descrevendo destinos de entrega, fragmentação e atrasos opcionais
- Mensagens I2NP completas preenchidas até um limite de 16 bytes

As instruções de entrega compactavam as informações de roteamento em campos de bits (tipo de entrega, flags de atraso, flags de fragmentação e extensões opcionais). Mensagens fragmentadas incluíam um ID de mensagem de 4 bytes, além de uma flag de índice/último fragmento.

### 2.2 Criptografia no Gateway

O design legado fixava o comprimento do tunnel em oito saltos para a fase de criptografia. Os gateways aplicavam camadas de AES-256/CBC mais blocos de soma de verificação, de modo que cada salto pudesse verificar a integridade sem reduzir a carga útil. A própria soma de verificação era um bloco derivado de SHA-256 incorporado na mensagem.

### 2.3 Comportamento dos Participantes

Os participantes rastreavam os IDs de tunnel de entrada, verificavam a integridade logo no início e descartavam duplicatas antes de encaminhar. Como o preenchimento e os blocos de verificação estavam incorporados, o tamanho da mensagem permanecia constante, independentemente do número de saltos.

### 2.4 Processamento do ponto de extremidade

Os pontos de extremidade descriptografaram os blocos em camadas sequencialmente, validaram as somas de verificação e separaram a carga útil novamente em instruções codificadas e mensagens I2NP para entrega posterior.

## 3. Criação de tunnel (processo obsoleto)

1. **Seleção de pares:** Os pares eram escolhidos a partir de perfis mantidos localmente (exploratório vs. cliente). O documento original já enfatizava a mitigação do [ataque do predecessor](https://en.wikipedia.org/wiki/Predecessor_attack) ao reutilizar listas ordenadas de pares por pool de tunnel.
2. **Entrega de solicitações:** As mensagens de construção eram encaminhadas salto a salto, com seções criptografadas para cada par. Ideias alternativas, como telescopic extension (extensão telescópica), midstream rerouting (reroteamento em meio ao fluxo) ou a remoção de blocos de checksum, foram discutidas como experimentos, mas nunca adotadas.
3. **Agrupamento:** Cada destino local mantinha pools separados de entrada e de saída. As configurações incluíam quantidade desejada, tunnels de reserva, variação de comprimento, limitação de taxa e políticas de padding (preenchimento).

## 4. Conceitos de Limitação e Mixagem

O texto antigo propôs várias estratégias que orientaram lançamentos posteriores:

- Descarte Antecipado Aleatório Ponderado (WRED) para controle de congestionamento
- Limitações de taxa por tunnel baseadas em médias móveis do uso recente
- Controles opcionais de chaff (tráfego de enchimento) e batching (agrupamento em lotes) (não totalmente implementados)

## 5. Alternativas Arquivadas

Seções do documento original exploravam ideias que nunca foram implementadas:

- Remover blocos de checksum para reduzir o processamento por salto
- Aplicar telescoping (construção incremental) de tunnels no meio do fluxo para alterar a composição dos pares
- Adotar tunnels bidirecionais (acabou sendo rejeitado)
- Usar hashes mais curtos ou diferentes regimes de padding

Essas ideias continuam sendo um contexto histórico valioso, mas não refletem a base de código moderna.

## Referências

- Arquivo original de documentos legados (pré-0.6.1.10)
- [Visão geral de Tunnel](/docs/overview/tunnel-routing/) para a terminologia atual
- [Perfilamento e seleção de pares](/docs/overview/tunnel-routing#peer-selection/) para heurísticas modernas
