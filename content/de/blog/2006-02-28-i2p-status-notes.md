---
title: "I2P Statusnotizen für 2006-02-28"
date: 2006-02-28
author: "jr"
description: "Netzwerkverbesserungen mit 0.6.1.12, Roadmap zu 0.6.2 mit neuen Strategien zur Peer-Auswahl und Möglichkeiten für Mini-Projekte"
categories: ["status"]
---

Hey zusammen, es ist wieder Zeit für unser Dienstags-Gemecker

* Index

1) Netzstatus und 0.6.1.12 2) Der Weg zu 0.6.2 3) Miniprojekte 4) ???

* 1) Net status and 0.6.1.12

In der vergangenen Woche gab es im Netz einige erhebliche Verbesserungen, zunächst durch die breite Verteilung von 0.6.1.11 am vergangenen Dienstag, gefolgt vom 0.6.1.12-Release am vergangenen Montag (das bislang auf 70% des Netzes ausgerollt wurde – danke!). Insgesamt ist die Lage im Vergleich zu 0.6.1.10 und früheren Releases deutlich besser – die Erfolgsraten beim Erstellen von tunnels sind ohne irgendwelche fallback tunnels um eine volle Größenordnung höher, die Latenz ist gesunken, die CPU-Auslastung ist gesunken und der Durchsatz ist gestiegen. Außerdem bleibt bei vollständig deaktiviertem TCP die Paket-Wiederübertragungsrate unter Kontrolle.

* 2) Road to 0.6.2

Es gibt noch Verbesserungsbedarf im Peer-Auswahlcode, da wir weiterhin 10-20% Ablehnungsraten bei client tunnels sehen und tunnels mit hohem Durchsatz (10+KBps) nicht so häufig sind, wie sie sein sollten. Andererseits, da die CPU-Last jetzt so stark gesunken ist, kann ich einen zusätzlichen router auf dev.i2p.net betreiben, ohne Probleme für meinen primären router zu verursachen (der squid.i2p, www.i2p, cvs.i2p, syndiemedia.i2p und andere ausliefert und dabei 2-300+KBps erreicht).

Außerdem probiere ich einige Verbesserungen für Nutzer in stark überlasteten Netzwerken aus (wie bitte, es gibt Leute, bei denen das nicht der Fall ist?). Es scheint in dieser Hinsicht einige Fortschritte zu geben, aber es werden weitere Tests nötig sein.  Das sollte, so hoffe ich, den 4 oder 5 Leuten auf irc2p helfen, die offenbar Schwierigkeiten haben, stabile Verbindungen aufrechtzuerhalten (und natürlich auch jenen helfen, die still unter denselben Symptomen leiden).

Nachdem das gut funktioniert, haben wir immer noch etwas Arbeit vor uns, bevor wir es 0.6.2 nennen können - wir benötigen die neuen Strategien zur Peer-Reihenfolge, zusätzlich zu diesen verbesserten Strategien zur Peer-Auswahl.  Als Ausgangsbasis hätte ich gern drei neue Strategien - = strikte Reihenfolge (Begrenzung des Vorgängers und Nachfolgers jedes Peers,   mit einer MTBF-Rotation (mittlere Zeit zwischen Ausfällen)) = feste Extreme (Verwendung eines festen Peers als eingehendes Gateway und   ausgehenden Endpunkt) = begrenzter Nachbar (Verwendung eines begrenzten Satzes von Peers als ersten Remote   Hop)

Es gibt noch andere interessante Strategien, die ausgearbeitet werden müssen, aber diese drei sind die wichtigsten. Sobald sie umgesetzt sind, werden wir für 0.6.2 funktional vollständig sein. Ungefähre ETA: März/April.

* 3) Miniprojects

Es gibt mehr nützliche Dinge zu tun, als ich aufzählen könnte, aber ich möchte eure Aufmerksamkeit auf einen Beitrag auf meinem Blog lenken, der fünf kleine Projekte beschreibt, die ein Coder ohne allzu großen Zeitaufwand umsetzen könnte [1]. Wenn jemand Interesse hat, an denen zu arbeiten, bin ich sicher, dass wir als Dank aus dem allgemeinen Fonds einige Ressourcen [2] bereitstellen würden, auch wenn mir klar ist, dass die meisten von euch eher vom Basteln als vom Geld motiviert sind ;)

[1] http://syndiemedia.i2p.net:8000/blog.jsp?     blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&     entry=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=/1140652800002 [2] http://www.i2p.net/halloffame

* 4) ???

Jedenfalls ist das ein kurzer Überblick darüber, was derzeit passiert, soweit ich weiß. Glückwunsch auch an cervantes zum 500. Forennutzer, übrigens :) Wie immer: Schaut in ein paar Minuten zum Meeting im Kanal #i2p vorbei!

=jr
