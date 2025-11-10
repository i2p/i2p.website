---
title: "Mensagem de Redefinição para ElGamal/AES+SessionTags"
number: "124"
author: "orignal"
created: "2016-01-24"
lastupdated: "2016-01-26"
status: "Aberta"
thread: "http://zzz.i2p/topics/2056"
---

## Visão Geral

Esta proposta é para uma mensagem I2NP que pode ser usada para redefinir as etiquetas de sessão entre duas Destinações.

## Motivação

Imagine que alguma destinação tenha um monte de etiquetas confirmadas para outra destinação. Mas essa destinação foi reiniciada ou perdeu essas etiquetas de alguma outra forma. A primeira destinação continua enviando mensagens com etiquetas e a segunda destinação não consegue descriptografar. A segunda destinação deveria ter uma maneira de informar à primeira destinação para redefinir (começar do zero) através de um glóbulo de alho adicional da mesma forma que envia LeaseSet atualizado.

## Design

### Mensagem Proposta

Este novo glóbulo deve conter o tipo de entrega "destinação" com uma nova mensagem I2NP chamada algo como "Redefinição de Etiquetas" e contendo o hash de identidade do remetente. Deve incluir timestamp e assinatura.

Pode ser enviada a qualquer momento se uma destinação não puder descriptografar mensagens.

### Uso

Se eu reiniciar meu roteador e tentar conectar a outra destinação, envio um glóbulo com meu novo LeaseSet, e enviaria um glóbulo adicional com esta mensagem contendo meu endereço. Uma destinação remota recebe esta mensagem, deleta todas as etiquetas de saída para mim e começa do ElGamal.

É um caso muito comum que uma destinação esteja em comunicação apenas com uma destinação remota. Em caso de reinicialização, ela deve enviar esta mensagem para todos junto com a primeira mensagem de streaming ou datagrama.
