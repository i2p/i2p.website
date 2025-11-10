---
title: "LeaseSet 2"
number: "110"
author: "zzz"
created: "2014-01-22"
lastupdated: "2016-04-04"
status: "Rejeitado"
thread: "http://zzz.i2p/topics/1560"
supercededby: "123"
---

## Visão Geral

Esta proposta trata de um novo formato de LeaseSet com suporte para novos tipos de encriptação.

## Motivação

A criptografia de ponta-a-ponta usada através dos túneis I2P possui chaves de encriptação e de assinatura separadas. As chaves de assinatura estão na Destinação do túnel, que já foi estendida com Certificados de Chave para suportar novos tipos de assinatura. No entanto, as chaves de encriptação são parte do LeaseSet, que não contém nenhum Certificado. Portanto, é necessário implementar um novo formato de LeaseSet e adicionar suporte para armazená-lo no netDb.

Um ponto positivo é que, uma vez que o LS2 seja implementado, todas as Destinações existentes poderão usar tipos de encriptação mais modernos; roteadores que podem buscar e ler um LS2 terão garantido suporte para quaisquer tipos de encriptação introduzidos juntamente com ele.

## Especificação

O formato básico do LS2 seria assim:

- dest
- carimbo de data/hora de publicação (8 bytes)
- expira (8 bytes)
- subtipo (1 byte) (regular, criptografado, meta ou serviço)
- flags (2 bytes)

- parte específica do subtipo:
  - tipo de encriptação, chave de encriptação e leases para o regular
  - blob para o criptografado
  - propriedades, hashes, portas, revogações, etc. para o serviço

- assinatura
