---
title: "Suporte a Floodfill para Tipos de Assinatura Opcionais"
number: "137"
author: "zzz"
created: "2017-03-31"
lastupdated: "2017-11-12"
status: "Open"
thread: "http://zzz.i2p/topics/2280"
toc: true
---

## Visão Geral

Adicione uma maneira para os floodfills anunciarem suporte a tipos de assinaturas opcionais.
Isso fornecerá um meio de suportar novos tipos de assinaturas a longo prazo,
mesmo que nem todas as implementações os suportem.


## Motivação

A proposta GOST 134 revelou vários problemas com a faixa de tipos de assinatura experimental anteriormente não utilizada.

Primeiro, como os tipos de assinatura na faixa experimental não podem ser reservados, eles podem ser usados para
múltiplos tipos de assinatura ao mesmo tempo.

Segundo, a menos que uma informação do roteador ou um conjunto de locações com um tipo de assinatura experimental possa ser armazenado em um floodfill,
o novo tipo de assinatura é difícil de testar ou usar completamente em uma fase de teste.

Terceiro, se a proposta 136 for implementada, isso não é seguro, já que qualquer pessoa pode sobrescrever uma entrada.

Quarto, implementar um novo tipo de assinatura pode ser um grande esforço de desenvolvimento.
Pode ser difícil convencer os desenvolvedores de todas as implementações de roteadores a adicionar suporte a um novo
tipo de assinatura a tempo para qualquer lançamento específico. O tempo e a motivação dos desenvolvedores podem variar.

Quinto, se GOST usar um tipo de assinatura na faixa padrão, ainda não há como saber se um determinado
floodfill suporta GOST.


## Design

Todos os floodfills devem suportar os tipos de assinaturas DSA (0), ECDSA (1-3) e EdDSA (7).

Para qualquer outro tipo de assinatura na faixa padrão (não experimental), um floodfill pode
anunciar suporte em suas propriedades de informação do roteador.


## Especificação


Um roteador que suporta um tipo de assinatura opcional deve adicionar a propriedade "sigTypes"
à sua informação de roteador publicada, com números de tipos de assinatura separados por vírgula.
Os tipos de assinatura estarão em ordem numérica ordenada.
Os tipos de assinatura obrigatórios (0-4,7) não devem ser incluídos.

Por exemplo: sigTypes=9,10

Roteadores que suportam tipos de assinatura opcionais devem somente armazenar, pesquisar ou inundar,
para floodfills que anunciem suporte para esse tipo de assinatura.


## Migração

Não aplicável.
Apenas roteadores que suportam um tipo de assinatura opcional devem implementar.


## Problemas

Se não houver muitos floodfills suportando o tipo de assinatura, eles podem ser difíceis de encontrar.

Pode não ser necessário exigir ECDSA 384 e 521 (tipos de assinaturas 2 e 3) para todos os floodfills.
Esses tipos não são amplamente utilizados.

Questões semelhantes precisarão ser abordadas com tipos de criptografia não-zero,
o que ainda não foi formalmente proposto.


## Notas

Armazenamentos NetDB de tipos de assinatura desconhecidos que não estão na faixa experimental continuarão
sendo rejeitados por floodfills, pois a assinatura não pode ser verificada.


