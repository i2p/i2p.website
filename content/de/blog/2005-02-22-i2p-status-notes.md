---
title: "I2P-Statusnotizen vom 2005-02-22"
date: 2005-02-22
author: "jr"
description: "Wöchentliche Notizen zum Entwicklungsstatus von I2P mit Berichten über den Erfolg der Version 0.5, das bevorstehende Bugfix-Release 0.5.0.1, Peer-Reihenfolgestrategien für tunnel sowie azneti2p-Updates"
categories: ["status"]
---

Hallo zusammen, Zeit für das wöchentliche Update

* Index

1) 0.5 2) Nächste Schritte 3) azneti2p 4) ???

* 1) 0.5

Wie ihr sicher schon gehört habt, haben wir 0.5 endlich veröffentlicht, und größtenteils läuft es ziemlich gut. Ich weiß sehr zu schätzen, wie schnell die Leute aktualisiert haben – innerhalb des ersten Tages waren 50-75% des Netzes auf 0.5! Dank der schnellen Umstellung konnten wir die Auswirkungen der verschiedenen Änderungen schneller erkennen und haben dabei eine ganze Reihe von Fehlern gefunden. Auch wenn es noch einige offene Probleme gibt, werden wir später am Abend eine neue Version 0.5.0.1 herausgeben, um die wichtigsten zu beheben.

Als netter Nebeneffekt der Bugs war es ziemlich cool zu sehen, dass routers Tausende von tunnels bewältigen können ;)

* 2) Next steps

Nach dem Release 0.5.0.1 könnte es einen weiteren Build geben, um mit einigen Änderungen am exploratorischen tunnel-Aufbau zu experimentieren (z. B. nur ein oder zwei nicht-ausfallende Peers zu verwenden, der Rest mit hoher Kapazität, statt alle Peers als nicht-ausfallend zu wählen). Danach springen wir in Richtung 0.5.1, was den tunnel-Durchsatz verbessern wird (indem mehrere kleine Nachrichten zu einer einzigen tunnel-Nachricht zusammengefasst werden) und dem Benutzer mehr Kontrolle über seine Anfälligkeit für den predecessor attack (Vorgängerangriff) ermöglichen wird.

Diese Kontrollmechanismen werden die Form client-spezifischer Strategien zur Peer-Reihenfolge und -Auswahl annehmen, eine für den eingehenden Gateway und den ausgehenden Endpunkt und eine für den Rest des tunnel.  Aktuelle grobe Skizze der Strategien, die ich vorsehe:  = random (was wir derzeit haben)  = balanced (wir versuchen ausdrücklich, die Häufigkeit zu verringern, mit der wir jeden Peer verwenden)  = strict (wenn wir jemals A-->B-->C verwenden, bleiben sie in dieser Reihenfolge            während nachfolgender tunnels [zeitlich begrenzt])  = loose (erzeuge einen zufälligen Schlüssel für den Client, berechne das XOR (exklusives ODER)           aus diesem Schlüssel und jedem Peer und ordne die Peers stets           nach der Entfernung zu diesem Schlüssel [zeitlich begrenzt])  = fixed (immer dieselben Peers pro MBTF verwenden)

Jedenfalls ist das der Plan, aber ich bin mir nicht sicher, welche Strategien zuerst eingeführt werden. Vorschläge sind mehr als willkommen :)

* 3) azneti2p

Die Leute drüben bei azureus haben fleißig gearbeitet und eine ganze Reihe von Updates veröffentlicht, und ihr neuester b34-Snapshot [1] scheint einige I2P-bezogene Fehlerbehebungen zu enthalten.  Auch wenn ich seit dem letzten von mir angesprochenen Anonymitätsproblem keine Zeit hatte, den Quellcode zu prüfen, haben sie diesen speziellen Bug behoben, also wenn du dich abenteuerlustig fühlst, schnapp dir ihr Update und probier's mal aus!

[1] http://azureus.sourceforge.net/index_CVS.php

* 4) ???

Es ist eine Menge los, und ich bin mir sicher, dass ich noch längst nicht alles erwähnt habe. Komm in ein paar Minuten kurz beim Meeting vorbei und schau, was los ist!

=jr
