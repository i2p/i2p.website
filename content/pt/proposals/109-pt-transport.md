---
title: "PT Transport"
number: "109"
author: "zzz"
created: "2014-01-09"
lastupdated: "2014-09-28"
status: "Open"
thread: "http://zzz.i2p/topics/1551"
---

## Visão Geral

Esta proposta é para criar um transporte I2P que se conecta a outros roteadores
através de Transportes Plugáveis.


## Motivação

Os Transportes Plugáveis (PTs) foram desenvolvidos pelo Tor como uma forma de adicionar transportes de ofuscação às pontes Tor de maneira modular.

O I2P já possui um sistema de transporte modular que diminui a barreira para adicionar transportes alternativos. Adicionar suporte para PTs proporcionaria ao I2P uma maneira fácil de experimentar com protocolos alternativos e se preparar para resistência a bloqueios.


## Design

Existem algumas camadas potenciais de implementação:

1. Um PT genérico que implementa SOCKS e ExtORPort e configura e faz fork dos
   processos de entrada e saída, e registra-se com o sistema de comunicação. Esta camada não sabe nada sobre NTCP, e pode ou não usar NTCP. Bom para testes.

2. Construindo sobre 1), um PT NTCP genérico que se baseia no código NTCP e canaliza
   NTCP para 1).

3. Construindo sobre 2), um PT NTCP-xxxx específico configurado para executar um determinado processo externo de entrada e saída.
