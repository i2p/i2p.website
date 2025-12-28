---
title: "SAM v1"
description: "Protocolo legado de Mensagens Anônimas Simples (obsoleto)"
slug: "sam"
lastUpdated: "2025-03"
accurateFor: "0.9.20"
reviewStatus: "needs-review"
---

> **Obsoleto:** SAM v1 é mantido apenas para referência histórica. Novas aplicações devem usar [SAM v3](/docs/api/samv3/) ou [BOB](/docs/legacy/bob/). A ponte original suporta apenas destinos DSA-SHA1 e um conjunto limitado de opções.

## Bibliotecas

A árvore de código-fonte do I2P em Java ainda inclui bindings (vinculações) legados para C, C#, Perl e Python. Eles não são mais mantidos e são distribuídos principalmente por motivos de compatibilidade de arquivamento.

## Negociação de Versão

Clientes conectam-se via TCP (padrão `127.0.0.1:7656`) e trocam:

```
Client → HELLO VERSION MIN=1 MAX=1
Bridge → HELLO REPLY RESULT=OK VERSION=1.0
```
A partir da versão 0.9.14 do Java I2P, o parâmetro `MIN` é opcional e ambos `MIN`/`MAX` aceitam formas de um único dígito (`"3"` etc.) para pontes atualizadas.

## Criação de sessão

```
SESSION CREATE STYLE={STREAM|DATAGRAM|RAW} DESTINATION={name|TRANSIENT} [DIRECTION={BOTH|RECEIVE|CREATE}] [option=value]*
```
- `DESTINATION=name` carrega ou cria uma entrada em `sam.keys`; `TRANSIENT` sempre cria um destino temporário.
- `STYLE` seleciona fluxos virtuais (semelhantes ao TCP), datagramas assinados ou datagramas brutos.
- `DIRECTION` aplica-se apenas a sessões de fluxo; o padrão é `BOTH`.
- Pares adicionais de chave/valor são encaminhados como opções de I2CP (por exemplo, `tunnels.quantityInbound=3`).

A ponte responde com:

```
SESSION STATUS RESULT=OK DESTINATION=name
```
Falhas retornam `DUPLICATED_DEST`, `I2P_ERROR` ou `INVALID_KEY`, além de uma mensagem opcional.

## Formatos de mensagens

As mensagens SAM são ASCII de linha única, com pares chave/valor separados por espaço. As chaves estão em UTF‑8; os valores podem ser colocados entre aspas se contiverem espaços. Não há mecanismo de escape definido.

Tipos de comunicação:

- **Fluxos** – encaminhados por proxy através da biblioteca de streaming do I2P
- **Datagramas com possibilidade de resposta** – cargas úteis assinadas (Datagram1)
- **Datagramas brutos** – cargas úteis sem assinatura (Datagram RAW)

## Opções adicionadas na versão 0.9.14

- `DEST GENERATE` aceita `SIGNATURE_TYPE=...` (permitindo Ed25519, etc.)
- `HELLO VERSION` trata `MIN` como opcional e aceita strings de versão de um dígito

## Quando usar o SAM v1

Apenas para interoperabilidade com software legado que não pode ser atualizado. Para todo novo desenvolvimento, use:

- [SAM v3](/docs/api/samv3/) para acesso a stream/datagram com todos os recursos
- [BOB](/docs/legacy/bob/) para gerenciamento de destino (ainda limitado, mas suporta recursos mais modernos)

## Referências

- [SAM v2](/docs/legacy/samv2/)
- [SAM v3](/docs/api/samv3/)
- [Especificação de Datagramas](/docs/api/datagrams/)
- [Protocolo de Streaming](/docs/specs/streaming/)

SAM v1 lançou as bases para o desenvolvimento de aplicações independente do router, mas o ecossistema já seguiu em frente. Trate este documento como um auxílio de compatibilidade, e não como um ponto de partida.
