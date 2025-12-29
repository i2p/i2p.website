---
title: "SAM v1"
description: "Älteres Simple Anonymous Messaging (einfaches anonymes Messaging)-Protokoll (veraltet)"
slug: "sam"
lastUpdated: "2025-03"
accurateFor: "0.9.20"
reviewStatus: "needs-review"
---

> **Veraltet:** SAM v1 wird nur aus historischen Gründen beibehalten. Neue Anwendungen sollten [SAM v3](/docs/api/samv3/) oder [BOB](/docs/legacy/bob/) verwenden. Die ursprüngliche Bridge unterstützt nur DSA-SHA1-Ziele und einen eingeschränkten Optionssatz.

## Bibliotheken

Der Java-I2P-Quellbaum enthält weiterhin veraltete Bindings für C, C#, Perl und Python. Sie werden nicht mehr gepflegt und hauptsächlich aus Gründen der Archivkompatibilität mitgeliefert.

## Versionsaushandlung

Clients verbinden sich über TCP (standardmäßig `127.0.0.1:7656`) und tauschen Folgendes aus:

```
Client → HELLO VERSION MIN=1 MAX=1
Bridge → HELLO REPLY RESULT=OK VERSION=1.0
```
Seit Java I2P 0.9.14 ist der Parameter `MIN` optional und sowohl `MIN`/`MAX` akzeptieren bei aktualisierten Brücken einstellige Formen (`"3"` usw.).

## Sitzungserstellung

```
SESSION CREATE STYLE={STREAM|DATAGRAM|RAW} DESTINATION={name|TRANSIENT} [DIRECTION={BOTH|RECEIVE|CREATE}] [option=value]*
```
- `DESTINATION=name` lädt oder erstellt einen Eintrag in `sam.keys`; `TRANSIENT` erstellt immer eine temporäre Destination (Zieladresse).
- `STYLE` wählt virtuelle Streams (TCP-ähnlich), signierte Datagramme oder rohe Datagramme aus.
- `DIRECTION` gilt nur für Stream-Sitzungen; standardmäßig `BOTH`.
- Zusätzliche Schlüssel-Wert-Paare werden als I2CP-Optionen weitergereicht (zum Beispiel `tunnels.quantityInbound=3`).

Die Bridge antwortet mit:

```
SESSION STATUS RESULT=OK DESTINATION=name
```
Bei Fehlern werden `DUPLICATED_DEST`, `I2P_ERROR` oder `INVALID_KEY` zurückgegeben, zusammen mit einer optionalen Nachricht.

## Nachrichtenformate

SAM-Nachrichten sind einzeilige ASCII-Nachrichten mit durch Leerzeichen getrennten Schlüssel/Wert-Paaren. Schlüssel sind UTF‑8; Werte dürfen in Anführungszeichen stehen, wenn sie Leerzeichen enthalten. Es ist kein Escaping (Maskierung) definiert.

Kommunikationstypen:

- **Streams** – über die I2P-Streaming-Bibliothek weitergeleitet
- **Antwortfähige Datagramme** – signierte Nutzlasten (Datagram1)
- **Rohe Datagramme** – unsignierte Nutzlasten (Datagram RAW)

## In 0.9.14 hinzugefügte Optionen

- `DEST GENERATE` akzeptiert `SIGNATURE_TYPE=...` (ermöglicht Ed25519 usw.)
- `HELLO VERSION` behandelt `MIN` als optional und akzeptiert einstellige Versionsstrings

## Wann SAM v1 verwenden

Nur zur Interoperabilität mit Legacy-Software, die nicht aktualisiert werden kann. Für alle neuen Entwicklungen verwenden Sie:

- [SAM v3](/docs/api/samv3/) für funktionsvollständigen Stream-/Datagrammzugriff
- [BOB](/docs/legacy/bob/) für die Verwaltung von Destinations (noch eingeschränkt, unterstützt aber modernere Funktionen)

## Referenzen

- [SAM v2](/docs/legacy/samv2/)
- [SAM v3](/docs/api/samv3/)
- [Datagramm-Spezifikation](/docs/api/datagrams/)
- [Streaming-Protokoll](/docs/specs/streaming/)

SAM v1 (SAM-API in Version 1) legte die Grundlage für eine router-agnostische Anwendungsentwicklung, aber das Ökosystem hat sich weiterentwickelt. Betrachten Sie dieses Dokument eher als Kompatibilitätshilfe denn als Ausgangspunkt.
