---
title: "I2P Statusnotizen für 2005-01-18"
date: 2005-01-18
author: "jr"
description: "Wöchentliche Statusnotizen zur I2P-Entwicklung zu Netzwerkstatus, Design des tunnel-Routings in Version 0.5, i2pmail.v2 und Sicherheitsfix für azneti2p_0.2"
categories: ["status"]
---

Hi zusammen, Zeit für das wöchentliche Update

* Index

1) Netzstatus 2) 0.5 3) i2pmail.v2 4) azneti2p_0.2 5) ???

* 1) Net status

Hmm, hier gibt es nicht viel zu berichten - alles funktioniert immer noch so wie letzte Woche, die Größe des Netzes ist weiterhin ziemlich ähnlich, vielleicht ein wenig größer. Einige nette neue Sites tauchen auf - siehe das Forum [1] und orion [2] für Details.

[1] http://forum.i2p.net/viewforum.php?f=16 [2] http://orion.i2p/

* 2) 0.5

Dank der Hilfe von postman, dox, frosk und cervantes (und allen, die Daten durch ihre routers getunnelt haben ;)) haben wir Statistiken zur Nachrichtengröße für einen ganzen Tag gesammelt [3].  Es gibt dort zwei Gruppen von Statistiken - Höhe und Breite des Zooms.  Dies wurde durch den Wunsch angetrieben, die Auswirkungen verschiedener Strategien für message padding (Auffüllung von Nachrichten) auf die Netzwerklast zu untersuchen, wie [4] in einem der Entwürfe für das 0.5 tunnel routing erläutert.  (ooOOoo hübsche Bilder).

Das Beunruhigende an dem, was ich beim Durchforsten dieser Daten gefunden habe, war, dass man selbst mit ein paar ziemlich einfachen, manuell abgestimmten Padding-Schwellwerten durch das Padding auf diese festen Größen immer noch bei über 25 % verschwendeter Bandbreite landen würde. Schon klar, das werden wir nicht tun. Vielleicht fällt euch beim Durchforsten dieser Rohdaten etwas Besseres ein.

[3] http://dev.i2p.net/~jrandom/messageSizes/ [4] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/                                  tunnel.html?rev=HEAD#tunnel.padding

Eigentlich führt uns dieser Link [4] zum Stand der 0.5-Pläne für das tunnel-Routing. Wie Connelly [5] schrieb, gab es in letzter Zeit im IRC viel Diskussion über einige der Entwürfe; polecat, bla, duck, nickster, detonate und andere steuerten Vorschläge und bohrende Fragen bei (okay, und sarkastische Kommentare ;). Nach etwas mehr als einer Woche sind wir bei [4] auf eine potenzielle Schwachstelle gestoßen, die einen Gegner betrifft, der es irgendwie schaffte, das Gateway des eingehenden tunnel zu übernehmen und außerdem einen der anderen Peers weiter hinten in diesem tunnel kontrollierte. Auch wenn dies für sich genommen in den meisten Fällen den Endpunkt nicht offenlegen würde und mit wachsendem Netzwerk probabilistisch schwer zu bewerkstelligen wäre, ist es trotzdem Mist (tm).

Also kommt [6] zum Einsatz. Damit wird dieses Problem beseitigt, ermöglicht uns tunnels beliebiger Länge und löst den Welthunger [7]. Es eröffnet allerdings ein weiteres Problem, bei dem ein Angreifer Schleifen im tunnel konstruieren könnte, aber basierend auf einem Vorschlag [8], den Taral letztes Jahr zu den bei ElGamal/AES verwendeten session tags (Sitzungs-Tags) gemacht hat, können wir den angerichteten Schaden minimieren, indem wir eine Reihe synchronisierter Pseudozufallszahlgeneratoren [9] verwenden.

[5] http://dev.i2p.net/pipermail/i2p/2005-January/000557.html [6] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/                                             tunnel-alt.html?rev=HEAD [7] Raten Sie, welche Aussage falsch ist? [8] http://www.i2p.net/todo#sessionTag [9] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/                                 tunnel-alt.html?rev=HEAD#tunnel.prng

Keine Sorge, wenn das Obige verwirrend klingt - du bekommst die inneren Details einiger ziemlich kniffliger Designprobleme zu sehen, die gerade offen ausgetragen werden. Wenn das Obige *nicht* verwirrend klingt, melde dich bitte bei uns, denn wir sind immer auf der Suche nach weiteren Köpfen, mit denen wir das durchkauen können :)

Jedenfalls, wie ich auf der Liste [10] erwähnt habe, möchte ich als Nächstes die zweite Strategie [6] implementieren, um die verbleibenden Details auszuarbeiten. Der Plan für 0.5 ist derzeit, alle nicht abwärtskompatiblen Änderungen zusammenzuführen – die neue tunnel crypto usw. – und das als 0.5.0 zu veröffentlichen; sobald sich das im Netz eingespielt hat, gehen wir zu den anderen Teilen von 0.5 [11] über, etwa der Anpassung der Pooling-Strategie wie in den Vorschlägen beschrieben, und veröffentlichen das als 0.5.1. Ich hoffe, dass wir 0.5.0 bis Ende des Monats noch erreichen, aber wir werden sehen.

[10] http://dev.i2p.net/pipermail/i2p/2005-January/000558.html [11] http://www.i2p.net/roadmap#0.5

* 3) i2pmail.v2

Neulich hat postman einen Entwurf eines Aktionsplans für die E-Mail-Infrastruktur der nächsten Generation veröffentlicht [12], und der sieht verdammt cool aus. Natürlich kann man sich immer noch mehr Schnickschnack ausdenken, aber das Ganze hat in vielerlei Hinsicht eine ziemlich gute Architektur. Schau dir an, was bisher dokumentiert wurde [13], und melde dich mit deinem Feedback bei postman!

[12] http://forum.i2p.net/viewtopic.php?t=259 [13] http://www.postman.i2p/mailv2.html

* 4) azneti2p_0.2

As I posted to the list [14], the original azneti2p plugin for azureus had a serious anonymity bug.  The problem was that mixed torrents where some users are anonymous and others are not, the anonymous users would contact the non-anonymous users /directly/ rather than through I2P.  Paul Gardner and the rest of the azureus devs were quite responsive and put out a patch right away.  The issue I saw is no longer present in azureus v. 2203-b12 + azneti2p_0.2.

Wir haben den Code allerdings nicht durchgearbeitet und geprüft, um mögliche Anonymitätsprobleme zu bewerten, daher gilt: "Benutzung auf eigene Gefahr" (andererseits sagen wir dasselbe auch über I2P, vor der 1.0-Veröffentlichung). Wenn du dazu bereit bist, weiß ich, dass die Azureus-Entwickler weiteres Feedback und Fehlermeldungen zum Plugin begrüßen würden. Wir werden die Leute natürlich informieren, falls wir von weiteren Problemen erfahren.

[14] http://dev.i2p.net/pipermail/i2p/2005-January/000553.html

* 5) ???

Wie Sie sehen, ist eine Menge los.  Ich glaube, das ist so ziemlich alles, was ich ansprechen wollte, aber schauen Sie bitte in 40 Minuten beim Treffen vorbei, wenn es noch etwas gibt, das Sie besprechen möchten (oder wenn Sie sich einfach über das oben Genannte auslassen möchten)

=jr
