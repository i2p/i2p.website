---
title: "Dienstsuche"
number: "122"
author: "zzz"
created: "2016-01-13"
lastupdated: "2016-01-13"
status: "Abgelehnt"
thread: "http://zzz.i2p/topics/2048"
supercedes: "102"
supercededby: "123"
---

## Überblick

Dies ist der vollständige bombastische Alles-geht-im-netdb-Vorschlag, auch bekannt als
anycast. Dies wäre der 4. vorgeschlagene LS2-Subtyp.

## Motivation

Angenommen, Sie möchten Ihr Ziel als Outproxy, oder einen GNS-Knoten, oder ein
Tor-Gateway, oder ein Bittorrent-DHT oder imule oder i2phex oder Seedless-Bootstrap usw. bewerben.
Sie könnten diese Informationen in der netDB speichern, anstatt eine separate
Bootstrapping- oder Informationsschicht zu verwenden.

Da niemand verantwortlich ist, können Sie im Gegensatz zu massivem Multihoming keine
signierte autoritative Liste haben. Sie würden einfach Ihr Verzeichnis an ein Floodfill
veröffentlichen. Das Floodfill würde diese aggregieren und als Antwort auf Anfragen senden.

## Beispiel

Angenommen, Ihr Dienst war "GNS". Sie würden einen Datenbankeintrag an das Floodfill senden:

- Hash von "GNS"
- Ziel
- Veröffentlichungszeitstempel
- Ablaufdatum (0 für Widerruf)
- Port
- Signatur

Wenn jemand eine Abfrage durchführte, erhielte er eine Liste dieser Verzeichnisse:

- Hash von "GNS"
- Hash des Floodfills
- Zeitstempel
- Anzahl der Verzeichnisse
- Liste der Verzeichnisse
- Signatur des Floodfills

Die Gültigkeitsdauer wäre relativ lang, mindestens Stunden.

## Sicherheitsimplikationen

Der Nachteil ist, dass dies sich in das Bittorrent-DHT oder schlimmeres verwandeln könnte. Mindestens müssten die Floodfills die Speicherung und Anfragen stark drosseln und kapazitätsbegrenzen. Wir könnten genehmigte Dienstnamen für höhere Limits auf die Whitelist setzen.
Wir könnten auch nicht aufgelistete Dienste komplett verbieten.

Natürlich ist selbst die heutige netDB anfällig für Missbrauch. Sie können beliebige Daten in der netDB speichern, solange sie wie ein RI oder LS aussehen und die Signatur bestätigt wird. Aber dies würde es viel einfacher machen.
