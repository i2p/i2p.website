---
title: "I2P-Statusnotizen vom 2004-10-19"
date: 2004-10-19
author: "jr"
description: "Wöchentliches I2P-Statusupdate mit Informationen zum Release 0.4.1.3, zu tunnel-Leistungsverbesserungen, zu Fortschritten bei der Streaming-Bibliothek und zur files.i2p-Suchmaschine"
categories: ["status"]
---

Hi zusammen, es ist wieder Dienstag

## Stichwortverzeichnis

1. 0.4.1.3
2. Tunnel test time, and send processing time
3. Streaming lib
4. files.i2p
5. ???

## 1) 0.4.1.3

Die Version 0.4.1.3 ist vor ein oder zwei Tagen erschienen, und es sieht so aus, als hätten die meisten Leute aktualisiert (danke!). Das Netz funktioniert ziemlich gut, aber es gibt noch keine revolutionäre Verbesserung der Zuverlässigkeit. Die Watchdog-Fehler aus 0.4.1.2 scheinen verschwunden zu sein (oder zumindest hat sie bisher niemand erwähnt). Mein Ziel ist, dass dieses 0.4.1.3-Release der letzte Patch vor 0.4.2 ist, aber natürlich werden wir, falls noch etwas Größeres auftaucht, das behoben werden muss, noch einen weiteren Patch veröffentlichen.

## 2) Tunnel-Testzeit und Sendeverarbeitungszeit

Die wichtigsten Änderungen im Release 0.4.1.3 betrafen das Testen der tunnel - statt einer festen (30 Sekunden!) Testperiode haben wir jetzt deutlich aggressivere Timeouts, die aus der gemessenen Performance abgeleitet werden. Das ist gut, denn wir markieren tunnels nun als fehlerhaft, wenn sie zu langsam sind, um irgendetwas Nützliches zu tun. Allerdings ist das auch schlecht, denn manchmal stauen sich tunnels vorübergehend, und wenn wir sie während dieses Zeitraums testen, stufen wir einen tunnel als fehlgeschlagen ein, der ansonsten funktionieren würde.

Ein aktuelles Diagramm dazu, wie lange ein tunnel-Test auf einem router dauert:

Das sind im Allgemeinen ok tunnel-Testzeiten - sie laufen über 4 entfernte Peers (mit 2 hop (Sprung) tunnels), was bei den meisten eine Zeit von ~1-200ms pro hop ergibt. Allerdings ist das nicht immer der Fall, wie man sieht - manchmal dauert es in der Größenordnung von Sekunden pro hop.

Hier setzt das nächste Diagramm an - die Warteschlangenzeit vom Zeitpunkt, an dem ein bestimmter router eine Nachricht senden wollte, bis zu dem Zeitpunkt, an dem diese Nachricht über einen Socket abgeschickt wurde:

Die oberen etwa 95 % liegen unter 50 ms, aber die Spitzen sind fatal.

Wir müssen diese Spitzen loswerden sowie Situationen umgehen, in denen mehr Peers ausfallen. Derzeit gilt: Wenn wir 'lernen', dass bei einem Peer unsere tunnels fehlschlagen, erfahren wir eigentlich nichts Spezifisches über dessen router - diese Spitzen können sogar Peers mit hoher Kapazität langsam erscheinen lassen, wenn wir sie ungünstig erwischen.

## 3) Streaming-Bibliothek

Der zweite Aspekt beim Umgang mit ausfallenden tunnels wird teilweise von der streaming lib (Streaming-Bibliothek) übernommen - was uns eine deutlich robustere Ende-zu-Ende-Streaming-Kommunikation verschafft. Diese Diskussion ist nichts Neues - die streaming lib wird all die ausgefeilten Funktionen liefern, über die wir schon eine Weile sprechen (und sie wird natürlich auch ihren Anteil an Bugs haben). In dieser Hinsicht gab es bereits große Fortschritte, und die Implementierung ist wahrscheinlich zu etwa 60% fertig.

Weitere Neuigkeiten, wenn es mehr davon gibt.

## 4) files.i2p

Ok, wir hatten in letzter Zeit viele neue eepsites(I2P Sites), was echt großartig ist. Ich möchte besonders auf diese hier hinweisen, denn sie hat eine ziemlich praktische Funktion für den Rest von uns. Wenn du noch nicht auf files.i2p warst: Es ist im Grunde eine Google-ähnliche Suchmaschine mit einem Cache der Seiten, die sie crawlt (sodass du sowohl suchen als auch stöbern kannst, wenn die eepsite(I2P Site) offline ist). Sehr cool.

## 5) ???

Die Statusnotizen dieser Woche sind ziemlich kurz, aber es ist eine Menge los - - ich habe einfach keine Zeit, vor dem Meeting noch mehr zu schreiben. Also schau in ein paar Minuten bei #i2p vorbei, dann können wir alles besprechen, was ich dummerweise übersehen habe.

=jr
