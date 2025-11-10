---
title: "Mensagens I2NP Maiores"
number: "103"
author: "zzz"
created: "2009-04-05"
lastupdated: "2009-05-27"
status: "Dead"
thread: "http://zzz.i2p/topics/258"
---

## Visão Geral

Esta proposta é sobre aumentar o limite de tamanho das mensagens I2NP.

## Motivação

O uso de datagramas de 12KB pelo iMule expôs muitos problemas. O limite real hoje
é algo em torno de 10KB.

## Design

A fazer:

- Aumentar o limite NTCP - não é tão fácil?

- Mais ajustes na quantidade de tags de sessão. Pode prejudicar o tamanho máximo da janela? Há estatísticas
  para analisar? Tornar o número variável com base na quantidade que achamos que precisam? Podem
  pedir mais? pedir uma quantidade?

- Investigar o aumento do tamanho máximo de SSU (aumentando o MTU?)

- Muitos testes

- Finalmente aplicar as melhorias do fragmentador? - Precisamos fazer testes de comparação
  primeiro!
