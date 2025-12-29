---
title: "SAM v2"
description: "Zastaralý protokol Simple Anonymous Messaging (jednoduché anonymní zasílání zpráv)"
slug: "samv2"
lastUpdated: "2025-03"
accurateFor: "0.9.20"
reviewStatus: "needs-review"
---

> **Zastaralé:** SAM v2 byl součástí I2P 0.6.1.31 a již není udržován. Pro nový vývoj použijte [SAM v3](/docs/api/samv3/). Jediným vylepšením v2 oproti v1 byla podpora více socketů multiplexovaných přes jedno připojení SAM.

## Poznámky k verzi

- Hlášený řetězec verze zůstává "2.0".
- Od verze 0.9.14 zpráva `HELLO VERSION` přijímá jednociferné hodnoty `MIN`/`MAX` a parametr `MIN` je volitelný.
- `DEST GENERATE` podporuje `SIGNATURE_TYPE`, takže lze vytvářet destinace Ed25519.

## Základy relace

```
SESSION CREATE STYLE={STREAM|DATAGRAM|RAW} DESTINATION={name|TRANSIENT} [DIRECTION={BOTH|RECEIVE|CREATE}] [option=value]
```
- Každá destinace může mít pouze jednu aktivní relaci SAM (streamy, datagramy nebo režim raw (surový)).
- `STYLE` volí virtuální streamy, podepsané datagramy nebo raw datagramy.
- Dodatečné volby se předávají do I2CP (například `tunnels.quantityInbound=3`).
- Odpovědi odpovídají v1: `SESSION STATUS RESULT=OK|DUPLICATED_DEST|I2P_ERROR|INVALID_KEY`.

## Kódování zpráv

Řádkově orientované ASCII s dvojicemi `key=value` oddělenými mezerami (hodnoty mohou být v uvozovkách). Typy komunikace jsou stejné jako ve verzi v1:

- Datové proudy přes streamovací knihovnu I2P
- Repliable datagrams (datagramy s možností odpovědi) (`PROTO_DATAGRAM`)
- Surové datagramy (`PROTO_DATAGRAM_RAW`)

## Kdy použít

Pouze pro starší klienty, které nelze migrovat. SAM v3 nabízí:

- Předání destinace v binární podobě (`DEST GENERATE BASE64`)
- Subsessions (podrelace) a podpora DHT (v3.3)
- Lepší hlášení chyb a vyjednávání parametrů

Viz:

- [SAM v1](/docs/legacy/sam/)
- [SAM v3](/docs/api/samv3/)
- [Datagramové API](/docs/api/datagrams/)
- [Streamovací protokol](/docs/specs/streaming/)
