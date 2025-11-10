---
title: "Lista de Bloqueio no Feed de Notícias"
number: "129"
author: "zzz"
created: "2016-11-23"
lastupdated: "2016-12-02"
status: "Fechado"
thread: "http://zzz.i2p/topics/2191"
target: "0.9.28"
implementedin: "0.9.28"
---

## Visão Geral

Esta proposta é para distribuir atualizações da lista de bloqueio no arquivo de notícias,
que é distribuído em formato su3 assinado.
Implementado na versão 0.9.28.

## Motivação

Sem isso, a lista de bloqueio só é atualizada na versão de lançamento.
Utiliza a assinatura de notícias existente.
Este formato poderia ser usado em várias implementações de roteador, mas apenas o roteador Java
usa a assinatura de notícias atualmente.

## Design

Adicionar uma nova seção ao arquivo news.xml.
Permitir bloqueio por IP ou hash de roteador.
A seção terá seu próprio carimbo de data/hora.
Permitir o desbloqueio de entradas previamente bloqueadas.

Incluir uma assinatura da seção, a ser especificada.
A assinatura cobrirá o carimbo de data/hora.
A assinatura deve ser verificada na importação.
O signatário será especificado e pode ser diferente do signatário su3.
Roteadores podem usar uma lista de confiança diferente para a lista de bloqueio.

## Especificação

Agora na página de especificação de atualização do roteador.

Entradas são ou um endereço IPv4 ou IPv6 literal,
ou um hash de roteador codificado em base64 de 44 caracteres.
Endereços IPv6 podem estar em formato abreviado (contendo "::").
O suporte para bloqueio com uma máscara de rede, por exemplo, x.y.0.0/16, é opcional.
O suporte para nomes de host é opcional.

## Migração

Roteadores que não suportam isso irão ignorar a nova seção XML.

## Veja Também

Proposta 130
