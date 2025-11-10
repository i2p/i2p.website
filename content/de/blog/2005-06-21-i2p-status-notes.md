---
title: "I2P Statusnotizen für 2005-06-21"
date: 2005-06-21
author: "jr"
description: "Wöchentliches Update zur Rückkehr eines Entwicklers von einer Reise, zu Fortschritten beim SSU-Transport, zum Abschluss der Unit-Test-Prämie und zu einem Service-Ausfall"
categories: ["status"]
---

Hallo zusammen, es ist Zeit, unsere wöchentlichen Statusnotizen wieder aufzunehmen

* Index

1) Entwicklerstatus 2) Entwicklungsstatus 3) Prämie für Unit-Tests 4) Dienstunterbrechung 5) ???

* 1) Dev[eloper] status

Nach 4 Städten in 4 Ländern bin ich endlich angekommen und arbeite wieder kräftig am Code. Letzte Woche habe ich die letzten Teile für einen Laptop zusammenbekommen, ich ziehe nicht mehr von Couch zu Couch, und obwohl ich zu Hause keinen Internetzugang habe, gibt es in der Umgebung genug Internetcafés, sodass der Zugang zuverlässig ist (nur unregelmäßig und teuer).

Dieser letzte Punkt bedeutet, dass ich mich vorerst, zumindest bis zum Herbst, nicht mehr so oft auf irc herumtreiben werde wie bisher (ich habe eine Untermiete bis etwa August und werde mir einen Ort suchen, an dem ich 24/7 Netzzugang bekomme). Das heißt jedoch nicht, dass ich weniger machen werde - ich werde nur größtenteils in meinem eigenen Testnetz arbeiten, Builds für Tests im Live-Netz herausbringen (und, äh, oh ja, Releases). Es bedeutet allerdings, dass wir einige Diskussionen, die früher frei in #i2p liefen, auf die Liste [1] und/oder ins Forum [2] verlagern möchten (ich lese allerdings weiterhin den #i2p-Backlog). Ich habe noch keinen geeigneten Ort gefunden, zu dem ich für unsere Entwicklertreffen gehen kann, daher werde ich diese Woche nicht dabei sein, aber vielleicht habe ich bis nächste Woche einen gefunden.

Wie dem auch sei, genug über mich.

[1] http://dev.i2p.net/pipermail/i2p/ [2] http://forum.i2p.net/

* 2) Dev[elopment] status

Während meines Umzugs habe ich an zwei Hauptbereichen gearbeitet - der Dokumentation und dem SSU-Transport (Letzteres erst, seit ich den Laptop habe). Die Dokumentation ist noch in Arbeit, darunter eine große, ziemlich einschüchternde Übersicht sowie eine Reihe kleinerer Implementierungsdokumente (die Dinge wie Quellcode-Struktur, Komponenteninteraktion usw. abdecken).

Die Arbeiten an SSU kommen gut voran – die neuen ACK-Bitfelder sind implementiert, die Kommunikation geht effektiv mit (simulierten) Verlusten um, die Übertragungsraten sind für die verschiedenen Bedingungen angemessen, und ich habe einige der hässlicheren Fehler behoben, auf die ich zuvor gestoßen war. Ich teste diese Änderungen weiterhin, und sobald es sinnvoll ist, werden wir eine Reihe von Live-Netztests planen, für die wir einige Freiwillige zur Unterstützung benötigen. Weitere Neuigkeiten dazu, sobald sie verfügbar sind.

* 3) Unit test bounty

Ich freue mich, bekanntzugeben, dass Comwiz mit einer Reihe von Patches vorstellig geworden ist, um die erste Phase der Unit-Test-Prämie [3] für sich zu beanspruchen! Wir arbeiten noch an einigen kleineren Details der Patches, aber ich habe die Aktualisierungen erhalten und sowohl die junit- als auch die clover-Berichte wie erforderlich erstellt. Ich rechne damit, dass wir die Patches in Kürze in CVS haben werden, woraufhin wir Comwiz’ Testdokumentation veröffentlichen.

Da clover ein kommerzielles Produkt ist (für OSS-Entwickler kostenlos [4]), können nur diejenigen, die clover installiert haben und ihre clover-Lizenz erhalten haben, die clover-Berichte generieren. In jedem Fall werden wir die clover-Berichte in regelmäßigen Abständen im Web veröffentlichen, sodass diejenigen, die clover nicht installiert haben, trotzdem sehen können, wie gut unsere Test-Suite abschneidet.

[3] http://www.i2p.net/bounties_unittest [4] http://www.cenqua.com/clover/

* 4) Service outage

Wie viele wahrscheinlich schon bemerkt haben, ist (mindestens) einer der Outproxies offline (squid.i2p), ebenso www.i2p, dev.i2p, cvs.i2p und mein Blog. Das sind keine voneinander unabhängigen Ereignisse - der Rechner, der sie hostet, ist kaputt.

=jr
