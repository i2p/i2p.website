---
title: "I2P-Statusnotizen für 2006-01-31"
date: 2006-01-31
author: "jr"
description: "Herausforderungen bei der Netzwerkzuverlässigkeit, bevorstehende Version 0.6.1.10 mit neuer Kryptografie zur tunnel-Erstellung und rückwärtsinkompatible Änderungen"
categories: ["status"]
---

Hallo zusammen, es ist wieder Dienstag,

* Index

1) Netzstatus 2) 0.6.1.10-Status 3) ???

* 1) Net status

In der vergangenen Woche habe ich verschiedene Optimierungen ausprobiert, um die Zuverlässigkeit beim Aufbau von tunnel im Live-Netz zu erhöhen, aber ein Durchbruch ist bislang ausgeblieben. In CVS gab es allerdings einige substanzielle Änderungen, aber ich würde sie nicht gerade als ... stabil bezeichnen. Daher würde ich im Allgemeinen empfehlen, entweder das neueste Release (0.6.1.9, in CVS als i2p_0_6_1_9 getaggt) zu verwenden oder mit den neuesten Builds nicht mehr als 1 Hop tunnels zu nutzen. Andererseits...

* 2) 0.6.1.10 status

Anstatt mich endlos mit kleineren Anpassungen aufzuhalten, habe ich in meinem lokalen Testnetzwerk daran gearbeitet, auf die neue Kryptographie und den neuen Prozess [1] für die Erstellung von tunnel zu migrieren. Dies sollte einen großen Teil der Fehlerrate bei der Erstellung von tunnel reduzieren, danach können wir es bei Bedarf weiter optimieren.

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/                                tunnel-alt-creation.html?rev=HEAD

Ein unglücklicher Nebeneffekt ist, dass 0.6.1.10 nicht abwärtskompatibel sein wird. Wir hatten seit langem keine nicht abwärtskompatible Veröffentlichung, aber in den frühen Tagen haben wir das mehrfach getan, daher sollte es kein allzu großes Problem sein. Im Grunde werden wir, nachdem es in meinem lokalen Testnetzwerk hervorragend funktioniert, es parallel ein paar Wagemutigen für frühe Tests ausrollen, und wenn es bereit für die Veröffentlichung ist, stellen wir einfach die Seed-Referenzen auf die Seeds des neuen Netzwerks um und bringen es raus.

Ich habe noch keinen voraussichtlichen Termin für das 0.6.1.10-Release, aber im Moment sieht es ziemlich gut aus (die meisten tunnel-Längen funktionieren, aber es gibt ein paar Entwicklungszweige, die ich noch nicht unter Last getestet habe).  Weitere Neuigkeiten, sobald es welche gibt, natürlich.

* 3) ???

Das ist so ziemlich alles, was ich im Moment zu erwähnen habe, auch wenn ich weiß, dass andere an ein paar Sachen herumbasteln und ich noch ein paar Tricks für später im Ärmel habe; aber wir werden mehr erfahren, wenn die Zeit reif ist. Wie auch immer, bis in ein paar Minuten!

=jr
