---
title: "Pesquisa de Serviço"
number: "122"
author: "zzz"
created: "2016-01-13"
lastupdated: "2016-01-13"
status: "Rejeitado"
thread: "http://zzz.i2p/topics/2048"
supercedes: "102"
supercededby: "123"
---

## Visão Geral

Esta é a proposta completa e bombástica de qualquer coisa no netdb. Também conhecida como
anycast. Este seria o 4º subtipo LS2 proposto.


## Motivação

Suponha que você quisesse anunciar seu destino como um outproxy, ou um nó GNS, ou um
gateway Tor, ou um Bittorrent DHT ou imule ou i2phex ou bootstrap do Seedless, etc.
Você poderia armazenar essa informação no netDB em vez de usar uma camada de bootstrap ou informação separada.

Não há ninguém no comando, então, ao contrário do multihoming massivo, você não pode ter uma lista assinada e autorizada. Então você simplesmente publicaria seu registro em um floodfill.
O floodfill agregaria esses dados e os enviaria como uma resposta para consultas.


## Exemplo

Suponha que seu serviço fosse "GNS". Você enviaria um armazenamento de banco de dados para o floodfill:

- Hash de "GNS"
- destino
- carimbo de data/hora de publicação
- expiração (0 para revogação)
- porta
- assinatura

Quando alguém fizesse uma busca, receberia de volta uma lista desses registros:

- Hash de "GNS"
- Hash do floodfill
- Carimbo de data/hora
- número de registros
- Lista de registros
- assinatura do floodfill

As expirações seriam relativamente longas, pelo menos algumas horas.


## Implicações de segurança

O lado negativo é que isso poderia se transformar no Bittorrent DHT ou pior. No
mínimo, os floodfills teriam que limitar severamente a taxa e a capacidade dos
armazenamentos e consultas. Poderíamos listar serviços aprovados para limites mais altos.
Também poderíamos proibir completamente serviços não autorizados.

Claro, até mesmo o netDB de hoje é aberto a abusos. Você pode armazenar dados arbitrários no
netDB, desde que se pareçam com um RI ou LS e a assinatura seja verificada. Mas
isso tornaria muito mais fácil.
