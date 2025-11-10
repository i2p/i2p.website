---
title: "LeaseSet Criptografado"
number: "121"
author: "zzz"
created: "2016-01-11"
lastupdated: "2016-01-12"
status: "Rejeitado"
thread: "http://zzz.i2p/topics/2047"
supercededby: "123"
---

## Visão Geral

Esta proposta é sobre redesenhar o mecanismo para criptografar LeaseSets.


## Motivação

O LS criptografado atual é horrível e inseguro. Posso dizer isso, eu projetei e
implementei.

Razões:

- Criptografia AES CBC
- Chave AES única para todos
- Expirações de Lease ainda expostas
- Chave pública de criptografia ainda exposta


## Design

### Objetivos

- Tornar tudo opaco
- Chaves para cada destinatário


### Estratégia

Fazer como o GPG/OpenPGP faz. Criptografe assimetricamente uma chave simétrica para cada
destinatário. Os dados são descriptografados com essa chave assimétrica. Veja por exemplo [RFC-4880-S5.1]
SE conseguirmos encontrar um algoritmo que seja pequeno e rápido.

O truque é encontrar uma criptografia assimétrica que seja pequena e rápida. ElGamal com 514
bytes é um pouco doloroso aqui. Podemos fazer melhor.

Veja por exemplo http://security.stackexchange.com/questions/824...

Isso funciona para números pequenos de destinatários (ou, na verdade, chaves; você ainda pode
distribuir chaves para várias pessoas, se quiser).


## Especificação

- Destino
- Marca temporal publicada
- Expiração
- Bandeiras
- Comprimento dos dados
- Dados criptografados
- Assinatura

Os dados criptografados poderiam ser prefixados com algum especificador de tipo de criptografia, ou não.


## Referências

.. [RFC-4880-S5.1]
    https://tools.ietf.org/html/rfc4880#section-5.1
