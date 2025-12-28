---
title: "Transporte SSU (Obsoleto)"
description: "Transporte UDP original utilizado antes do SSU2"
slug: "ssu"
lastUpdated: "2024-01"
accurateFor: "0.9.61"
type: docs
reviewStatus: "needs-review"
---

> **Obsoleto:** SSU (UDP seguro semi-confiável) foi substituído por [SSU2](/docs/specs/ssu2/). O Java I2P removeu o SSU na versão 2.4.0 (API 0.9.61) e o i2pd o removeu na 2.44.0 (API 0.9.56). Este documento é mantido apenas para referência histórica.

## Destaques

- Transporte UDP que fornece entrega ponto a ponto criptografada e autenticada de mensagens I2NP.
- Baseava-se em uma negociação Diffie–Hellman de 2048 bits (mesmo primo que o ElGamal).
- Cada datagrama continha um HMAC-MD5 de 16 bytes (variante truncada não padrão) + IV (vetor de inicialização) de 16 bytes, seguido por uma carga útil criptografada com AES-256-CBC.
- A prevenção de repetição (replay) e o estado da sessão eram rastreados dentro da carga útil criptografada.

## Cabeçalho da mensagem

```
[16-byte MAC][16-byte IV][encrypted payload]
```
Cálculo de MAC utilizado: `HMAC-MD5(ciphertext || IV || (len ^ version ^ ((netid-2)<<8)))` com uma chave MAC de 32 bytes. O tamanho da carga útil (payload) era um valor de 16 bits em big-endian, acrescentado aos dados considerados no cálculo do MAC. Por padrão, a versão do protocolo era `0`; o netId era `2` (rede principal).

## Chaves de Sessão e MAC

Derivado do segredo compartilhado de Diffie-Hellman:

1. Converta o valor compartilhado em um array de bytes big-endian (prefixe `0x00` se o bit mais significativo estiver definido).
2. Chave de sessão: primeiros 32 bytes (preencha com zeros se for mais curto).
3. Chave MAC: bytes 33–64; se insuficiente, recorra ao hash SHA-256 do valor compartilhado.

## Estado

Routers não anunciam mais endereços SSU. Os clientes devem migrar para os transportes SSU2 ou NTCP2. Implementações históricas podem ser encontradas em versões mais antigas:

- Código-fonte Java anterior à versão 2.4.0 em `router/transport/udp`
- Código-fonte do i2pd anterior à versão 2.44.0

Para o comportamento atual do transporte UDP, consulte a [especificação do SSU2](/docs/specs/ssu2/).
