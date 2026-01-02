---
title: "Blockliste im SU3-Format"
number: "130"
author: "psi, zzz"
created: "2016-11-23"
lastupdated: "2016-11-23"
status: "Offen"
thread: "http://zzz.i2p/topics/2192"
toc: true
---

## Übersicht

Dieser Vorschlag zielt darauf ab, Aktualisierungen der Blockliste in einer separaten su3-Datei zu verteilen.


## Motivation

Ohne diese Methode wird die Blockliste nur im Release aktualisiert.
Dieses Format könnte in verschiedenen Router-Implementierungen verwendet werden.


## Design

Definieren Sie das Format, das in einer su3-Datei eingebettet wird.
Ermöglichen Sie das Blockieren nach IP oder Router-Hash.
Router dürfen sich bei einer URL anmelden oder eine Datei importieren, die auf andere Weise bezogen wurde.
Die su3-Datei enthält eine Signatur, die beim Import verifiziert werden muss.


## Spezifikation

Soll der Aktualisierungsspezifikationsseite des Routers hinzugefügt werden.

Neuen Inhaltstyp BLOCKLIST (5) definieren.
Neuen Dateityp TXT_GZ (4) (.txt.gz-Format) definieren.
Einträge sind jeweils pro Zeile, entweder eine wörtliche IPv4- oder IPv6-Adresse,
oder ein 44-zeichenlang kodierter Router-Hash in Base64.
Unterstützung für das Blockieren mit einer Netzmaske, z.B. x.y.0.0/16, ist optional.
Um einen Eintrag zu entsperren, gehen Sie mit einem '!' voran.
Kommentare beginnen mit einem '#'.

## Migration

n/a


