---
title: "Größere I2NP-Nachrichten"
number: "103"
author: "zzz"
created: "2009-04-05"
lastupdated: "2009-05-27"
status: "Tot"
thread: "http://zzz.i2p/topics/258"
---

## Übersicht

Dieser Vorschlag befasst sich mit der Erhöhung des Größenlimits für I2NP-Nachrichten.


## Motivation

Die Nutzung von 12KB-Datagrammen durch iMule hat viele Probleme offenbart. Das tatsächliche Limit liegt derzeit eher bei 10KB.


## Design

Zu tun:

- NTCP-Limit erhöhen - nicht so einfach?

- Anpassungen bei der Menge der Sitzungstags. Könnte die maximale Fenstergröße beeinträchtigen? Gibt es Statistiken, die untersucht werden sollten? Die Anzahl basierend darauf variabel gestalten, wie viele wir glauben, dass sie benötigen? Können sie nach mehr fragen? Nach einer Menge fragen?

- Untersuchen, ob die maximale SSU-Größe erhöht werden kann (durch Erhöhung des MTU?)

- Viel testen

- Schließlich die Verbesserungen beim Fragmentierer einchecken? - Vergleichstests sind zuerst erforderlich!
