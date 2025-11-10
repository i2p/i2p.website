---
title: "I2P Statusnotizen für 2005-04-26"
date: 2005-04-26
author: "jr"
description: "Kurzes wöchentliches Update zur Netzwerkstabilität von 0.5.0.7, den Fortschritten beim SSU-UDP-Transport mit Unterstützung für mehrere Netzwerke und der Finanzierung der Unit-Test-Prämie"
categories: ["status"]
---

Hallo zusammen, heute nur kurze wöchentliche Statusnotizen

* Index

1) Netzstatus 2) SSU-Status 3) Prämie für Unit-Tests 4) ???

* 1) Net status

Die meisten Nutzer haben recht schnell auf die Veröffentlichung 0.5.0.7 der letzten Woche aktualisiert (danke!), und insgesamt scheint das Ergebnis positiv zu sein. Das Netz scheint ziemlich zuverlässig zu sein und die vorherige tunnel-Drosselung wurde behoben. Es werden jedoch weiterhin von einigen Nutzern sporadische Probleme gemeldet, und wir gehen diesen nach.

* 2) SSU status

Die meiste Zeit verbringe ich derzeit mit dem 0.6-UDP-Code, und nein, es ist noch nicht bereit für eine Veröffentlichung, und ja, es gibt Fortschritte ;) Im Moment kann es mehrere Netzwerke handhaben und hält dabei einige Peers auf UDP und andere auf TCP, mit recht vernünftiger Performance. Der schwierige Teil besteht darin, all die Überlastungs- und Konkurrenzsituationen durchzuarbeiten, da das Live-Netz ständig unter Last stehen wird, aber in den letzten ein, zwei Tagen gab es dort eine Menge Fortschritte. Mehr Neuigkeiten, wenn es mehr Neuigkeiten gibt.

* 3) Unit test bounty

Wie duck auf der Liste erwähnt hat [1], hat zab eine Bounty (Prämie) ausgelobt, um I2P mit einer Reihe von Test-Updates zu unterstützen - etwas Geld für jeden, der die auf der Bounty-Seite [2] aufgeführten Aufgaben erledigen kann. Wir haben einige weitere Spenden für diese Bounty erhalten [3] - sie liegt derzeit bei $1000USD. Auch wenn die Bounties sicherlich keinen "marktüblichen Satz" bieten, sind sie ein kleiner Anreiz für Entwickler, die helfen möchten.

[1] http://dev.i2p.net/pipermail/i2p/2005-April/000721.html [2] http://www.i2p.net/bounty_unittests [3] http://www.i2p.net/halloffame

* 4) ???

Okay, ich bin schon wieder zu spät zur Besprechung... Ich sollte das wohl unterschreiben und rausschicken, oder? Schau einfach bei der Besprechung vorbei, dann können wir auch andere Punkte besprechen.

=jr
