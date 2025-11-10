---
title: "Meta-LeaseSet für Multihoming"
number: "120"
author: "zzz"
created: "2016-01-09"
lastupdated: "2016-01-11"
status: "Abgelehnt"
thread: "http://zzz.i2p/topics/2045"
supercededby: "123"
---

## Überblick

Dieser Vorschlag betrifft die Implementierung einer ordnungsgemäßen Multihoming-Unterstützung in I2P, die auf große Websites skalierbar ist.

## Motivation

Multihoming ist ein Hack und wird vermutlich bei z.B. facebook.i2p im großen Maßstab nicht funktionieren. Angenommen, wir hätten 100 Multihomes, jeweils mit 16 Tunneln, das wären 1600 LS-Veröffentlichungen alle 10 Minuten oder fast 3 pro Sekunde. Die Floodfills würden überfordert und Drosselungen würden einsetzen. Und das, bevor wir überhaupt den Abfrageverkehr erwähnen.

Wir brauchen eine Art von Meta-LS, bei der die LS die 100 echten LS-Hashes auflisten. Diese wäre langlebig, deutlich länger als 10 Minuten. Es handelt sich also um einen zweistufigen Look-up für die LS, aber die erste Stufe könnte für Stunden zwischengespeichert werden.

## Spezifikation

Das Meta-LeaseSet hätte folgendes Format::

- Destination
- Veröffentlichtes Zeitstempel
- Ablauf
- Flags
- Eigenschaften
- Anzahl der Einträge
- Anzahl der Widerrufe

- Einträge. Jeder Eintrag enthält:
  - Hash
  - Flags
  - Ablauf
  - Kosten (Priorität)
  - Eigenschaften

- Widerrufe. Jeder Widerruf enthält:
  - Hash
  - Flags
  - Ablauf

- Signatur

Flags und Eigenschaften sind für maximale Flexibilität enthalten.

## Kommentare

Dies könnte dann verallgemeinert werden, um eine Dienstabfrage jeglicher Art zu sein. Der Dienst-Identifikator ist ein SHA256-Hash.

Für noch massivere Skalierbarkeit könnten wir mehrere Ebenen haben, d.h. ein Meta-LS könnte auf andere Meta-LSes verweisen.
