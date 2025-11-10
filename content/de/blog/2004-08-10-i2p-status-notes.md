---
title: "I2P-Statusnotizen vom 2004-08-10"
date: 2004-08-10
author: "jr"
description: "Wöchentliches I2P-Status-Update zur Leistung des Releases 0.3.4.1, outproxy-Lastverteilung und Aktualisierungen der Dokumentation"
categories: ["status"]
---

Hey zusammen, Zeit für das wöchentliche Update

## Stichwortverzeichnis:

1. 0.3.4.1 status
2. Updated docs
3. 0.4 progress
4. ???

## 1) 0.3.4.1 Status

Nun, wir haben neulich die Version 0.3.4.1 herausgebracht, und sie läuft ziemlich gut. Die Verbindungszeiten auf irc liegen durchgehend bei mehreren Stunden, und die Übertragungsraten sind ebenfalls ziemlich gut (ich habe neulich mit 3 parallelen Streams 25KBps von einer eepsite(I2P Site) erreicht).

Eine wirklich coole Funktion, die mit der Version 0.3.4.1 hinzugefügt wurde (die ich in der Release-Ankündigung zu erwähnen vergessen habe), war der Patch von mule, der es dem eepproxy ermöglicht, Nicht-I2P-Anfragen im Round-Robin-Verfahren über eine Reihe von outproxies (ausgehende Proxys) zu verteilen. Der Standard ist weiterhin einfach die Verwendung des squid.i2p outproxy, aber wenn Sie in Ihre router.config gehen und die clientApp Zeile so ändern, dass sie hat:

```
-e 'httpclient 4444 squid.i2p,www1.squid.i2p'
```
Es wird jede HTTP-Anfrage zufällig über einen der beiden aufgeführten outproxies routen (squid.i2p und www1.squid.i2p). Damit seid ihr, wenn noch ein paar mehr Leute outproxies betreiben, nicht mehr so abhängig von squid.i2p. Natürlich kennt ihr alle meine Bedenken hinsichtlich outproxies, aber diese Möglichkeit bietet den Leuten mehr Optionen.

Wir haben in den letzten Stunden etwas Instabilität beobachtet, aber mit Hilfe von duck und cervantes habe ich zwei üble Bugs identifiziert und teste derzeit Fehlerbehebungen. Die Fehlerbehebungen sind umfangreich, daher rechne ich damit, in ein bis zwei Tagen 0.3.4.2 zu veröffentlichen, nachdem ich die Ergebnisse verifiziert habe.

## 2) Aktualisierte Dokumentation

Wir waren in letzter Zeit etwas nachlässig, die Dokumentation auf der Website auf den neuesten Stand zu bringen, und obwohl es noch einige große Lücken gibt (z. B. die netDb- und i2ptunnel-Dokumentation), haben wir kürzlich ein paar davon aktualisiert (Netzwerkvergleiche und die FAQ). Da wir uns den Releases 0.4 und 1.0 nähern, würde ich es begrüßen, wenn Leute die Website durchsehen und prüfen könnten, was sich verbessern lässt.

Besonders erwähnenswert ist eine aktualisierte Hall of Fame – wir haben sie endlich auf den neuesten Stand gebracht, damit sie die großzügigen Spenden von euch allen widerspiegelt (danke!). Während wir voranschreiten, werden wir diese Mittel nutzen, um Coder und andere Mitwirkende zu vergüten sowie um angefallene Kosten auszugleichen (z. B. Hosting-Anbieter usw.).

## 3) 0.4 Fortschritt

Rückblickend auf die Notizen der letzten Woche haben wir für 0.4 noch ein paar Punkte offen, aber die Simulationen laufen ziemlich gut und die meisten kaffe-Probleme wurden gefunden. Großartig wäre es allerdings, wenn Leute verschiedene Aspekte am router oder an den Client-Anwendungen intensiv testen und alle dabei auftretenden Fehler melden könnten.

## 4) ???

Das ist alles, was ich im Moment ansprechen wollte – ich weiß die Zeit zu schätzen, die ihr euch nehmt, um uns voranzubringen, und ich denke, wir machen große Fortschritte. Natürlich: Falls jemand noch etwas hat, worüber er sprechen möchte, schaut einfach beim Meeting in #i2p vorbei ... äh ... jetzt :)

=jr
