---
title: "I2P-Statusnotizen für 2006-03-21"
date: 2006-03-21
author: "jr"
description: "JRobin-Integration für Netzwerkstatistiken, die IRC-Bots biff und toopie sowie die Ankündigung eines neuen GPG-Schlüssels"
categories: ["status"]
---

Hi zusammen, es ist wieder Dienstag

* Index

1) Netzstatus 2) jrobin 3) biff und toopie 4) neuer Schlüssel 5) ???

* 1) Net status

Die vergangene Woche war ziemlich stabil, bisher ohne neue Veröffentlichung. Ich habe weiter an der Drosselung von tunnel und am Betrieb mit geringer Bandbreite gearbeitet, aber um diese Tests zu unterstützen, habe ich JRobin in die Web-Konsole und unser Statistik-Management-System integriert.

* 2) JRobin

JRobin [1] ist eine reine Java-Portierung von RRDtool [2], die es uns ermöglicht, ansprechende Grafiken zu erzeugen, wie die, die zzz in großer Zahl erzeugt, und das mit sehr geringem zusätzlichen Speicherbedarf.  Wir haben es so konfiguriert, dass es vollständig im Speicher arbeitet, sodass es keine Sperrkonflikte bei Dateien gibt, und die Zeit zum Aktualisieren der Datenbank ist praktisch nicht wahrnehmbar.  Es gibt eine ganze Reihe praktischer Funktionen, die JRobin beherrscht und die wir derzeit nicht nutzen; die nächste Version wird jedoch die grundlegende Funktionalität enthalten sowie eine Möglichkeit, die Daten in einem von RRDtool verstandenen Format zu exportieren.

[1] http://www.jrobin.org/ [2] http://people.ee.ethz.ch/~oetiker/webtools/rrdtool/

* 3) biff and toopie

Postman hat fleißig an ein paar nützlichen Bots gearbeitet, und ich freue mich berichten zu können, dass der liebenswerte biff zurück ist [3], der dich benachrichtigt, sobald (anonyme) Mail eingeht, während du auf irc2p bist. Außerdem hat postman einen ganz neuen Bot für uns entwickelt - toopie - der als Info-Bot für I2P/irc2p dient. Wir füttern toopie noch mit FAQs, aber er wird bald in den üblichen Kanälen auftauchen. Danke, postman!

[3] http://hq.postman.i2p/?page_id=15

* 4) new key

Den Aufmerksamen unter euch wird aufgefallen sein, dass mein GPG-Schlüssel in ein paar Tagen abläuft. Mein neuer Schlüssel unter http://dev.i2p.net/~jrandom hat den Fingerabdruck 0209 9706 442E C4A9 91FA  B765 CE08 BC25 33DC 8D49 und die Schlüssel-ID 33DC8D49. Dieser Beitrag ist mit meinem alten Schlüssel signiert, aber meine folgenden Beiträge (und Veröffentlichungen) im nächsten Jahr werden mit dem neuen Schlüssel signiert sein.

* 5) ???

Das war's fürs Erste - schaut in ein paar Minuten bei #i2p zu unserem wöchentlichen Treffen vorbei, um Hallo zu sagen!

=jr
