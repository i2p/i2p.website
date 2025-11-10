---
title: "Aumentar o MTU IPv6"
number: "127"
author: "zzz"
created: "2016-08-23"
lastupdated: "2016-12-02"
status: "Fechado"
thread: "http://zzz.i2p/topics/2181"
target: "0.9.28"
implementedin: "0.9.28"
---

## Visão Geral

Esta proposta visa aumentar o MTU máximo SSU IPv6 de 1472 para 1488.
Implementada na versão 0.9.28.


## Motivação

O MTU IPv4 deve ser um múltiplo de 16, + 12. O MTU IPv6 deve ser um múltiplo de 16.


Quando o suporte a IPv6 foi adicionado pela primeira vez anos atrás, definimos o MTU máximo do IPv6 para 1472, menor que o
MTU do IPv4 de 1484. Isso era para manter as coisas simples e garantir que o MTU IPv6 fosse menor
que o MTU existente do IPv4. Agora que o suporte a IPv6 é estável, devemos ser capazes de
definir o MTU IPv6 mais alto que o MTU IPv4.

O MTU típico da interface é 1500, então podemos razoavelmente aumentar o MTU IPv6 em 16 para 1488.


## Design

Alterar o máximo de 1472 para 1488.


## Especificação

Nas seções "Endereço do Router" e "MTU" da visão geral do SSU,
alterar o MTU máximo IPv6 de 1472 para 1488.


## Migração

Esperamos que os routers definam o MTU de conexão como o mínimo do MTU local e remoto,
como de costume. Nenhuma verificação de versão deve ser necessária.

Caso determinemos que uma verificação de versão é necessária, definiremos um nível de versão mínima
de 0.9.28 para esta alteração.
