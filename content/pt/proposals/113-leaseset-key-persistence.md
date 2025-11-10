---
title: "Persistência de Chave LeaseSet"
number: "113"
author: "zzz"
created: "2014-12-13"
lastupdated: "2016-12-02"
status: "Fechado"
thread: "http://zzz.i2p/topics/1770"
target: "0.9.18"
implementedin: "0.9.18"
---

## Visão Geral

Esta proposta trata da persistência de dados adicionais no LeaseSet que são atualmente efêmeros.
Implementado na versão 0.9.18.

## Motivação

Na versão 0.9.17, foi adicionada a persistência para a chave de corte do netDb, armazenada em
i2ptunnel.config. Isso ajuda a prevenir alguns ataques mantendo o mesmo corte após reiniciar, e também previne possíveis correlações com uma reinicialização do roteador.

Há duas outras coisas que são ainda mais fáceis de correlacionar com a reinicialização do roteador:
as chaves de criptografia e assinatura do leaseset. Estas não são atualmente persistidas.

## Alterações Propostas

As chaves privadas são armazenadas em i2ptunnel.config, como i2cp.leaseSetPrivateKey e i2cp.leaseSetSigningPrivateKey.
