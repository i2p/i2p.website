---
title: "SAM (rozhraní Simple Anonymous Messaging) v1"
description: "Zastaralý protokol Simple Anonymous Messaging (deprecated)"
slug: "sam"
lastUpdated: "2025-03"
accurateFor: "0.9.20"
reviewStatus: "needs-review"
---

> **Zastaralé:** SAM v1 je zachován pouze pro historické účely. Nové aplikace by měly používat [SAM v3](/docs/api/samv3/) nebo [BOB](/docs/legacy/bob/). Původní můstek podporuje pouze cíle DSA-SHA1 a omezenou sadu možností.

## Knihovny

Strom zdrojových kódů Java I2P stále obsahuje zastaralé vazby pro C, C#, Perl a Python. Už nejsou udržovány a jsou distribuovány převážně kvůli archivní kompatibilitě.

## Vyjednávání verze

Klienti se připojují přes TCP (výchozí `127.0.0.1:7656`) a vyměňují si:

```
Client → HELLO VERSION MIN=1 MAX=1
Bridge → HELLO REPLY RESULT=OK VERSION=1.0
```
Od verze Java I2P 0.9.14 je parametr `MIN` nepovinný a oba `MIN`/`MAX` přijímají jednociferné tvary (`"3"` apod.) pro aktualizované mosty.

## Vytvoření relace

```
SESSION CREATE STYLE={STREAM|DATAGRAM|RAW} DESTINATION={name|TRANSIENT} [DIRECTION={BOTH|RECEIVE|CREATE}] [option=value]*
```
- `DESTINATION=name` načte nebo vytvoří položku v `sam.keys`; `TRANSIENT` vždy vytvoří dočasnou destinaci.
- `STYLE` vybírá virtuální streamy (podobné TCP), podepsané datagramy nebo surové datagramy.
- `DIRECTION` se vztahuje pouze na streamové relace; výchozí hodnota je `BOTH`.
- Další páry klíč/hodnota jsou předány jako volby I2CP (například `tunnels.quantityInbound=3`).

Most odpovídá:

```
SESSION STATUS RESULT=OK DESTINATION=name
```
Chybové stavy vracejí `DUPLICATED_DEST`, `I2P_ERROR` nebo `INVALID_KEY` a volitelnou zprávu.

## Formáty zpráv

Zprávy SAM jsou jednořádkové ASCII s páry klíč/hodnota oddělenými mezerami. Klíče jsou v UTF‑8; hodnoty mohou být uzavřeny v uvozovkách, pokud obsahují mezery. Nejsou definovány žádné escape sekvence.

Typy komunikace:

- **Datové proudy** – proxyované přes I2P streaming library
- **Datagramy s možností odpovědi** – podepsaná užitečná data (Datagram1)
- **Surové datagramy** – nepodepsaná užitečná data (Datagram RAW)

## Možnosti přidané ve verzi 0.9.14

- `DEST GENERATE` přijímá `SIGNATURE_TYPE=...` (umožňuje použít Ed25519 apod.)
- `HELLO VERSION` považuje `MIN` za volitelné a přijímá jednociferné řetězce verzí

## Kdy použít SAM v1

Pouze kvůli interoperabilitě se zastaralým softwarem, který nelze aktualizovat. Pro veškerý nový vývoj používejte:

- [SAM v3](/docs/api/samv3/) pro funkčně kompletní přístup ke streamům/datagramům
- [BOB](/docs/legacy/bob/) pro správu destinací (stále omezený, ale podporuje modernější funkce)

## Reference

- [SAM v2](/docs/legacy/samv2/)
- [SAM v3](/docs/api/samv3/)
- [Specifikace datagramů](/docs/api/datagrams/)
- [Streamovací protokol](/docs/specs/streaming/)

SAM v1 položil základy pro vývoj aplikací nezávislý na routeru, ale ekosystém se posunul dál. Tento dokument berte spíše jako pomůcku pro kompatibilitu než jako výchozí bod.
