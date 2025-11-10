---
title: "Diretório de Serviços"
number: "102"
author: "zzz"
created: "2009-01-01"
lastupdated: "2009-01-06"
status: "Rejeitado"
thread: "http://zzz.i2p/topics/180"
supercededby: "122"
---

## Visão Geral

Esta proposta é para um protocolo que aplicativos poderiam usar para registrar e procurar serviços em um diretório.

## Motivação

A maneira mais simples de suportar onioncat é com um diretório de serviços.

Isto é semelhante a uma proposta que Sponge fez algum tempo atrás no IRC. Eu não acho que ele tenha escrito, mas a ideia dele era colocá-lo no netDb. Eu não sou a favor disso, mas a discussão sobre o melhor método de acessar o diretório (consultas netDb, DNS-over-i2p, HTTP, hosts.txt, etc.) deixarei para outro dia.

Eu provavelmente poderia improvisar isso rapidamente usando HTTP e a coleção de scripts perl que uso para o formulário de adição de chave.

## Especificação

Aqui está como um aplicativo interagiria com o diretório:

REGISTRAR
  - DestKey
  - Lista de pares de Protocolo/Serviço:

    - Protocolo (opcional, padrão: HTTP)
    - Serviço (opcional, padrão: website)
    - ID (opcional, padrão: nenhum)

  - Nome do host (opcional)
  - Expiração (padrão: 1 dia? 0 para excluir)
  - Assinatura (usando chave privada para dest)

  Retorna: sucesso ou falha

  Atualizações permitidas

CONSULTAR
  - Hash ou chave (opcional). UM dos:

    - hash parcial de 80 bits
    - hash completo de 256 bits
    - destkey completa

  - Par protocolo/serviço (opcional)

  Retorna: sucesso, falha, ou (para 80 bits) colisão.
  Se sucesso, retorna descritor assinado acima.
