---
title: "Tunnelbau-Nachrichtenoptionen"
number: "143"
author: "zzz"
created: "2018-01-14"
lastupdated: "2022-01-28"
status: "Abgelehnt"
thread: "http://zzz.i2p/topics/2500"
toc: true
---

## Hinweis
Dieser Vorschlag wurde nicht wie spezifiziert implementiert,
jedoch wurden die ECIES langen und kurzen Build-Nachrichten (Vorschläge 152 und 157)
mit erweiterbaren Optionsfeldern entworfen.
Siehe die [Tunnel Creation ECIES Spezifikation](/docs/specs/implementation/#tunnel-creation-ecies) für die offizielle Spezifikation.


## Übersicht

Fügen Sie einen flexiblen, erweiterbaren Mechanismus für Optionen in den I2NP Tunnel Build Records hinzu,
die in den Tunnel Build und Tunnel Build Reply-Nachrichten enthalten sind.


## Motivation

Es gibt einige vorläufige, undokumentierte Vorschläge zur Einstellung von Optionen oder Konfiguration in der Tunnel Build-Nachricht,
so dass der Ersteller des Tunnels einige Parameter an jeden Tunnelknoten weitergeben kann.

Es gibt 29 freie Bytes im TBM. Wir möchten die Flexibilität für zukünftige Erweiterungen bewahren, aber auch den Raum weise nutzen.
Die Verwendung der 'Mapping'-Konstruktion würde mindestens 6 Bytes pro Option verwenden ("1a=1b;").
Die rigide Definition weiterer Optionsfelder könnte später Probleme verursachen.

Dieses Dokument schlägt ein neues, flexibles Options-Mapping-Schema vor.


## Design

Wir benötigen eine Optionsdarstellung, die kompakt und dennoch flexibel ist, damit wir mehrere
Optionen unterschiedlicher Länge in 29 Bytes unterbringen können.
Diese Optionen sind noch nicht definiert und müssen derzeit nicht definiert werden.
Verwenden Sie nicht die "Mapping"-Struktur (die ein Java-Propertie-Objekt kodiert), sie ist zu verschwenderisch.
Verwenden Sie eine Nummer, um jede Option und Länge anzugeben, was zu einer kompakten und dennoch flexiblen Kodierung führt.
Optionen müssen in unseren Spezifikationen nach Nummer registriert werden, aber wir werden auch einen Bereich für experimentelle Optionen reservieren.


## Spezifikation

Vorläufig - mehrere Alternativen werden unten beschrieben.

Dies wäre nur vorhanden, wenn Bit 5 in den Flags (Byte 184) auf 1 gesetzt ist.

Jede Option ist eine zwei Byte lange Optionsnummer und -länge, gefolgt von der Länge der Optionswert-Bytes.

Optionen beginnen bei Byte 193 und setzen sich bis maximal zum letzten Byte 221 fort.

Optionsnummer/Länge:

Zwei Bytes. Bits 15-4 sind die 12-Bit-Optionsnummer, 1 - 4095.
Bits 3-0 sind die Anzahl der zu folgenden Optionswert-Bytes, 0 - 15.
Eine boolesche Option könnte null Wertbytes haben.
Wir werden ein Register der Optionsnummern in unseren Spezifikationen führen und auch einen Bereich für experimentelle Optionen definieren.

Der Optionswert ist 0 bis 15 Bytes, um von allem interpretiert zu werden, was diese Option benötigt. Unbekannte Optionsnummern sollten ignoriert werden.

Die Optionen werden abgeschlossen mit einer Optionsnummer/Länge von 0/0, das heißt zwei 0 Bytes.
Der verbleibende Platz der 29 Bytes, falls vorhanden, sollte wie gewohnt mit zufälliger Auffüllung gefüllt werden.

Diese Kodierung bietet uns Platz für 14 0-Byte-Optionen, 9 1-Byte-Optionen oder 7 2-Byte-Optionen.
Eine Alternative wäre, nur ein Byte für die Optionsnummer/Länge zu verwenden,
vielleicht mit 5 Bits für die Optionsnummer (maximal 32) und 3 Bits für die Länge (maximal 7).
Dies würde die Kapazität auf 28 0-Byte-Optionen, 14 1-Byte-Optionen oder 9 Zwei-Byte-Optionen erhöhen.
Wir könnten es auch variabel machen, wobei eine 5-Bit-Optionsnummer von 31 bedeutet, dass 8 weitere Bits für die Optionsnummer gelesen werden.

Wenn der Tunnelknoten Optionen an den Ersteller zurückgeben muss, können wir dasselbe Format in der Tunnel Build Reply-Nachricht verwenden,
vorangestellt von einer magischen Zahl mehrerer Bytes (da wir kein definiertes Flagbyte haben, um anzuzeigen, dass Optionen vorhanden sind).
Es gibt 495 freie Bytes im TBRM.


## Hinweise

Diese Änderungen betreffen die Tunnel Build Records und können daher in allen Anfragevarianten für Build-Nachrichten verwendet werden -
Tunnel Build Request, Variable Tunnel Build Request, Tunnel Build Reply und Variable Tunnel Build Reply.


## Migration

Der ungenutzte Platz in den Tunnel Build Records wird mit zufälligen Daten gefüllt und derzeit ignoriert.
Der Raum kann ohne Migrationsprobleme in Optionen umgewandelt werden.
In der Build-Nachricht wird das Vorhandensein von Optionen im Flags-Byte angezeigt.
In der Build-Antwort-Nachricht wird das Vorhandensein von Optionen durch eine mehrbyteige magische Zahl angezeigt.
