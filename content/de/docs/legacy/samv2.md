---
title: "SAM v2"
description: "Veraltetes Simple Anonymous Messaging-Protokoll"
slug: "samv2"
lastUpdated: "2025-03"
accurateFor: "0.9.20"
reviewStatus: "needs-review"
---

> **Veraltet:** SAM v2 wurde mit I2P 0.6.1.31 ausgeliefert und wird nicht mehr gepflegt. Verwenden Sie [SAM v3](/docs/api/samv3/) für neue Entwicklungen. Die einzige Verbesserung von v2 gegenüber v1 war die Unterstützung mehrerer Sockets, die über eine einzelne SAM-Verbindung multiplex übertragen werden.

## Versionshinweise

- Die gemeldete Versionszeichenfolge bleibt `"2.0"`.
- Seit 0.9.14 akzeptiert die Nachricht `HELLO VERSION` einstellige Werte für `MIN`/`MAX` und der Parameter `MIN` ist optional.
- `DEST GENERATE` unterstützt `SIGNATURE_TYPE`, sodass Ed25519-Destinations (Ziele) erstellt werden können.

## Grundlagen der Sitzung

```
SESSION CREATE STYLE={STREAM|DATAGRAM|RAW} DESTINATION={name|TRANSIENT} [DIRECTION={BOTH|RECEIVE|CREATE}] [option=value]
```
- Jede Destination (Zieladresse) darf nur eine aktive SAM-Session haben (Streams, Datagramme oder RAW).
- `STYLE` wählt virtuelle Streams, signierte Datagramme oder rohe Datagramme aus.
- Zusätzliche Optionen werden an I2CP übergeben (zum Beispiel `tunnels.quantityInbound=3`).
- Antworten entsprechen v1: `SESSION STATUS RESULT=OK|DUPLICATED_DEST|I2P_ERROR|INVALID_KEY`.

## Nachrichtenkodierung

Zeilenorientiertes ASCII mit durch Leerzeichen getrennten `key=value`-Paaren (Werte können in Anführungszeichen stehen). Kommunikationstypen sind dieselben wie in v1:

- Streams über die I2P-Streaming-Bibliothek
- Antwortfähige Datagramme (`PROTO_DATAGRAM`)
- Rohdatagramme (`PROTO_DATAGRAM_RAW`)

## Wann verwenden

Nur für Legacy-Clients, die nicht migrieren können. SAM v3 bietet:

- Übergabe einer binären Destination (Zieladresse) (`DEST GENERATE BASE64`)
- Subsessions (Untersitzungen) und DHT-Unterstützung (v3.3)
- Verbesserte Fehlermeldungen und Aushandlung von Optionen

Siehe:

- [SAM v1](/docs/legacy/sam/)
- [SAM v3](/docs/api/samv3/)
- [Datagramm-API](/docs/api/datagrams/)
- [Streaming-Protokoll](/docs/specs/streaming/)
