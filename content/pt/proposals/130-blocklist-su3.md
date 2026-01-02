---
title: "Lista de Bloqueios em Formato SU3"
number: "130"
author: "psi, zzz"
created: "2016-11-23"
lastupdated: "2016-11-23"
status: "Open"
thread: "http://zzz.i2p/topics/2192"
toc: true
---

## Visão Geral

Esta proposta é para distribuir atualizações da lista de bloqueios em um arquivo su3 separado.


## Motivação

Sem isto, a lista de bloqueios é atualizada apenas na versão de lançamento.
Este formato poderia ser usado em várias implementações de roteadores.


## Design

Defina o formato para ser encapsulado em um arquivo su3.
Permitir bloqueio por IP ou hash de roteador.
Roteadores podem se inscrever em uma URL ou importar um arquivo obtido por outros meios.
O arquivo su3 contém uma assinatura que deve ser verificada na importação.


## Especificação

A ser adicionado à página de especificação de atualização do roteador.

Definir novo tipo de conteúdo BLOCKLIST (5).
Definir novo tipo de arquivo TXT_GZ (4) (formato .txt.gz).
Entradas são uma por linha, seja um endereço literal IPv4 ou IPv6,
ou um hash de roteador codificado em base64 de 44 caracteres.
Suporte para bloqueio com uma máscara de rede, e.g. x.y.0.0/16, é opcional.
Para desbloquear uma entrada, preceda-a com um '!'.
Comentários começam com um '#'.


## Migração

n/a


