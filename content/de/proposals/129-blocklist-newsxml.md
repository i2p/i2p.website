---
title: "Blockliste im News Feed"
number: "129"
author: "zzz"
created: "2016-11-23"
lastupdated: "2016-12-02"
status: "Geschlossen"
thread: "http://zzz.i2p/topics/2191"
target: "0.9.28"
implementedin: "0.9.28"
---

## Überblick

Dieser Vorschlag sieht vor, Blocklisten-Updates in der News-Datei zu verteilen,
die in signiertem su3-Format verteilt wird.
Implementiert in 0.9.28.

## Motivation

Ohne dies wird die Blockliste nur in der Veröffentlichung aktualisiert.
Verwendet bestehendes News-Abonnement.
Dieses Format könnte in verschiedenen Router-Implementierungen verwendet werden, aber nur der Java-Router
verwendet derzeit das News-Abonnement.

## Design

Füge der Datei news.xml einen neuen Abschnitt hinzu.
Erlaube das Blockieren nach IP oder Router-Hash.
Der Abschnitt wird seinen eigenen Zeitstempel haben.
Ermögliche das Entsperren zuvor gesperrter Einträge.

Enthalten Sie eine Signatur des Abschnitts, die spezifiziert werden soll.
Die Signatur wird den Zeitstempel abdecken.
Die Signatur muss beim Import überprüft werden.
Der Unterzeichner wird spezifiziert und kann vom su3-Unterzeichner abweichen.
Router können eine andere Vertrauensliste für die Blockliste verwenden.

## Spezifikation

Jetzt auf der Spezifikationsseite für Router-Updates.

Einträge sind entweder eine wörtliche IPv4- oder IPv6-Adresse,
oder ein 44-stelliger Base64-codierter Router-Hash.
IPv6-Adressen können im abgekürzten Format (mit "::") sein.
Unterstützung für das Blockieren mit einer Netzmaske, z.B. x.y.0.0/16, ist optional.
Unterstützung für Hostnamen ist optional.

## Migration

Router, die dies nicht unterstützen, ignorieren den neuen XML-Abschnitt.

## Siehe auch

Vorschlag 130
