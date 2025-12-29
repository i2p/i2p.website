---
title: "SAM v2"
description: "Protocolo Simple Anonymous Messaging legado"
slug: "samv2"
lastUpdated: "2025-03"
accurateFor: "0.9.20"
reviewStatus: "needs-review"
---

> **Obsoleto:** SAM v2 foi distribuído com o I2P 0.6.1.31 e não é mais mantido. Use [SAM v3](/docs/api/samv3/) para novos desenvolvimentos. A única melhoria do v2 em relação ao v1 foi o suporte a múltiplos sockets multiplexados sobre uma única conexão SAM.

## Notas da versão

- A string de versão informada permanece `"2.0"`.
- Desde a versão 0.9.14, a mensagem `HELLO VERSION` aceita valores de um dígito para `MIN`/`MAX` e o parâmetro `MIN` é opcional.
- `DEST GENERATE` suporta `SIGNATURE_TYPE`, assim destinos Ed25519 podem ser criados.

## Noções básicas de sessão

```
SESSION CREATE STYLE={STREAM|DATAGRAM|RAW} DESTINATION={name|TRANSIENT} [DIRECTION={BOTH|RECEIVE|CREATE}] [option=value]
```
- Cada destino pode ter apenas uma sessão SAM ativa (fluxos, datagramas ou raw (bruto)).
- `STYLE` seleciona fluxos virtuais, datagramas assinados ou datagramas brutos.
- Opções adicionais são passadas ao I2CP (por exemplo, `tunnels.quantityInbound=3`).
- As respostas refletem a v1: `SESSION STATUS RESULT=OK|DUPLICATED_DEST|I2P_ERROR|INVALID_KEY`.

## Codificação de Mensagens

ASCII orientado por linhas com pares `key=value` separados por espaços (os valores podem estar entre aspas). Os tipos de comunicação são os mesmos da v1:

- Fluxos via a biblioteca de streaming do I2P
- Datagramas respondíveis (`PROTO_DATAGRAM`)
- Datagramas brutos (`PROTO_DATAGRAM_RAW`)

## Quando usar

Apenas para clientes legados que não podem migrar. SAM v3 oferece:

- Transferência de destino binário (`DEST GENERATE BASE64`)
- Suporte a subsessões e a DHT (tabela de hash distribuída) (v3.3)
- Relato de erros aprimorado e negociação de opções

Consulte:

- [SAM v1](/docs/legacy/sam/)
- [SAM v3](/docs/api/samv3/)
- [API de Datagramas](/docs/api/datagrams/)
- [Protocolo de Streaming](/docs/specs/streaming/)
