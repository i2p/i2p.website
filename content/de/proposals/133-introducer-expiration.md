---
title: "Introducer-Verfall"
number: "133"
author: "zzz"
created: "2017-02-05"
lastupdated: "2017-08-09"
status: "Geschlossen"
thread: "http://zzz.i2p/topics/2230"
target: "0.9.30"
implementedin: "0.9.30"
---

## Übersicht

Dieser Vorschlag bezieht sich auf die Verbesserung der Erfolgsrate bei Einführungen.


## Motivation

Einführer verfallen nach einer bestimmten Zeit, aber diese Info wird nicht in der
RouterInfo veröffentlicht. Router müssen derzeit Heuristiken verwenden, um zu schätzen, wann ein
Einführer nicht mehr gültig ist.


## Design

In einer SSU RouterAddress, die Einführer enthält, kann der Herausgeber optional
Ablaufzeiten für jeden Einführer angeben.


## Spezifikation

```
iexp{X}={nnnnnnnnnn}

X :: Die Einführer-Nummer (0-2)

nnnnnnnnnn :: Die Zeit in Sekunden (nicht ms) seit der Epoche.
```

### Hinweise
* Jeder Ablauf muss größer sein als das Veröffentlichungsdatum der RouterInfo
  und weniger als 6 Stunden nach dem Veröffentlichungsdatum der RouterInfo.

* Herausgeber von Routern und Einführern sollten versuchen, den Einführer bis zum Ablauf gültig zu halten,
  können dies jedoch nicht garantieren.

* Router sollten einen veröffentlichten Einführer nach dessen Ablauf nicht mehr verwenden.

* Die Einführerabläufe befinden sich in der RouterAddress Zuordnung.
  Sie sind nicht das (derzeit ungenutzte) 8-Byte-Ablauf-Feld in der RouterAddress.

**Beispiel:** `iexp0=1486309470`


## Migration

Keine Probleme. Die Implementierung ist optional.
Abwärtskompatibilität ist sichergestellt, da ältere Router unbekannte Parameter ignorieren.
