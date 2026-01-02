---
title: "Suporte de Floodfill para Tipos de Assinatura Experimentais"
number: "136"
author: "zzz"
created: "2017-03-31"
lastupdated: "2017-11-12"
status: "Aberto"
thread: "http://zzz.i2p/topics/2279"
toc: true
---

## Visão Geral

Para tipos de assinatura na faixa experimental (65280-65534),
os floodfills devem aceitar armazenamentos de netdb sem verificar a assinatura.

Isso apoiará o teste de novos tipos de assinatura.


## Motivação

A proposta GOST 134 revelou duas questões com a faixa de tipo de assinatura experimental anteriormente não utilizada.

Primeiro, como os tipos de assinatura na faixa experimental não podem ser reservados, eles podem ser usados para múltiplos tipos de assinatura ao mesmo tempo.

Segundo, a menos que uma info de roteador ou conjunto de arrendamento com um tipo de assinatura experimental possa ser armazenado em um floodfill,
o novo tipo de assinatura é difícil de testar completamente ou usar em uma base experimental.


## Design

Os floodfills devem aceitar, e propagar, armazenamentos de LS com tipos de assinatura na faixa experimental,
sem verificar a assinatura. O suporte para armazenamentos RI está em definição e pode ter mais implicações de segurança.


## Especificação


Para tipos de assinatura na faixa experimental, um floodfill deve aceitar e propagar armazenamentos de netdb
sem verificar a assinatura.

Para evitar falsificação de roteadores e destinos não experimentais, um floodfill
nunca deve aceitar um armazenamento de um tipo de assinatura experimental que tenha uma colisão de hash
com uma entrada existente do netdb de um tipo de assinatura diferente.
Isso previne o sequestro de uma entrada anterior do netdb.

Adicionalmente, um floodfill deve sobrescrever uma entrada netdb experimental
com um armazenamento de um tipo de assinatura não experimental que é uma colisão de hash,
para evitar o sequestro de um hash previamente ausente.

Floodfills devem assumir que o comprimento da chave pública de assinatura é 128, ou derivá-lo do
comprimento do certificado de chave, se for maior. Algumas implementações podem
não suportar comprimentos maiores a menos que o tipo de assinatura seja informalmente reservado.


## Migração

Uma vez que esse recurso seja suportado, em uma versão conhecida do roteador,
entradas netdb de tipo de assinatura experimental podem ser armazenadas em floodfills dessa versão ou superior.

Se algumas implementações de roteadores não suportarem esse recurso, o armazenamento do netdb
falhará, mas isso é igual ao que acontece atualmente.


## Questões

Podem haver implicações adicionais de segurança, a serem pesquisadas (ver proposta 137)

Algumas implementações podem não suportar comprimentos de chave maiores que 128,
como descrito acima. Adicionalmente, pode ser necessário impor um máximo de 128
(em outras palavras, não há dados de chave excessivos no certificado de chave),
para reduzir a capacidade de atacantes gerarem colisões de hash.

Questões semelhantes precisarão ser abordadas com tipos de criptografia não nulos,
que ainda não foram formalmente propostos.


## Notas

Armazenamentos de NetDB de tipos de assinatura desconhecidos que não estão na faixa experimental continuarão
a ser rejeitados pelos floodfills, pois a assinatura não pode ser verificada.


