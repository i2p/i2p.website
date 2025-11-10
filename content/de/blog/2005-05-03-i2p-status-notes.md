---
title: "I2P-Statusnotizen für 2005-05-03"
date: 2005-05-03
author: "jr"
description: "Wöchentliche Aktualisierung zu Netzwerkstabilität, erfolgreichen Live-Tests des SSU-UDP-Transports, Fortschritten beim i2phex-Dateiaustausch und einer bevorstehenden 3–4‑wöchigen Abwesenheit"
categories: ["status"]
---

Hallo zusammen, diese Woche steht eine Menge auf der Agenda

* Index

1) Netzwerkstatus 2) SSU Status 3) i2phex 4) unerlaubt abwesend 5) ???

* 1) Net status

Keine großen Veränderungen beim Gesamtzustand des Netzwerks - alles scheint ziemlich stabil zu sein, und obwohl wir gelegentliche Aussetzer haben, scheinen die Dienste gut zu laufen. Seit dem letzten Release gab es viele Updates im CVS, aber keine Showstopper-Bugfixes. Möglicherweise gibt es vor meinem Umzug noch ein weiteres Release, einfach um den neuesten Stand aus dem CVS weiter zu verbreiten, aber ich bin mir noch nicht sicher.

* 2) SSU status

Habt ihr es satt, mich immer wieder sagen zu hören, dass es beim UDP-Transport viele Fortschritte gibt? Tja, Pech gehabt - es gab wieder viele Fortschritte beim UDP-Transport. Am Wochenende sind wir von Tests im privaten Netzwerk ins Live-Netz gewechselt, und etwa ein Dutzend router haben ein Upgrade durchgeführt und ihre SSU-Adresse veröffentlicht - dadurch sind sie für die meisten Nutzer über den TCP-Transport erreichbar, während SSU-fähige router über UDP miteinander kommunizieren können.

Die Tests sind noch in einem sehr frühen Stadium, aber sie verliefen deutlich besser, als ich erwartet hatte. Die Congestion Control (Überlaststeuerung) verhielt sich sehr gut, und sowohl Durchsatz als auch Latenz waren durchaus ausreichend - sie konnte reale Bandbreitengrenzen korrekt erkennen und die Verbindung effektiv mit konkurrierenden TCP-Streams teilen.

Mit den von den hilfreichen Freiwilligen gesammelten Statistiken wurde deutlich, wie wichtig der Code für selektive Bestätigungen (SACK) für den ordnungsgemäßen Betrieb in stark überlasteten Netzwerken ist. Ich habe die letzten paar Tage damit verbracht, diesen Code zu implementieren und zu testen, und habe die SSU-Spezifikation [1] aktualisiert, um eine neue, effiziente SACK-Technik aufzunehmen. Sie wird nicht abwärtskompatibel mit dem früheren SSU-Code sein, daher sollten Personen, die beim Testen geholfen haben, den SSU-Transport deaktivieren, bis ein neuer Build zum Testen bereitsteht (hoffentlich in den nächsten ein bis zwei Tagen).

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/udp.html?rev=HEAD

* 3) i2phex

sirup arbeitet unermüdlich an einer Portierung von phex auf i2p, und obwohl noch viel Arbeit nötig ist, bevor es für Otto Normalverbraucher bereit ist, konnte ich es heute Abend starten, sirups freigegebene Dateien durchsuchen, einige Daten herunterladen und seine *hust* "instant"-Chat-Oberfläche verwenden.

Es gibt viel mehr Informationen auf sirups eepsite(I2P Site) [2], und Hilfe beim Testen durch Leute, die bereits in der i2p-Community sind, wäre großartig (aber bitte, bis sirup es als öffentliche Freigabe absegnet und i2p mindestens 0.6, wenn nicht 1.0, ist, lassen wir es innerhalb der i2p-Community). Ich glaube, sirup wird beim Treffen dieser Woche dabei sein, also können wir dann vielleicht noch mehr Informationen bekommen!

[2] http://sirup.i2p/

* 4) awol

Apropos Anwesenheit: Ich werde bei der Sitzung nächste Woche wahrscheinlich nicht dabei sein und bin anschließend für 3-4 Wochen offline. Auch wenn das wohl bedeutet, dass es keine neuen Releases geben wird, gibt es dennoch eine Menge wirklich interessanter Dinge, an denen Leute hacken können:
  = Anwendungen wie feedspace, i2p-bt/ducktorrent, i2phex, fire2pe,
     das addressbook, susimail, q oder etwas völlig Neues.
  = der eepproxy - es wäre großartig, Filterung, Unterstützung für
     persistente HTTP-Verbindungen, 'listen on' ACLs, und vielleicht ein
     exponentielles Backoff zu bekommen, um mit outproxy-Timeouts umzugehen (statt
     einfachem Round-Robin)
  = der PRNG (wie auf der Liste besprochen)
  = eine PMTU-Bibliothek (entweder in Java oder in C mit JNI)
  = die Unit-Test-Prämie und die GCJ-Prämie
  = Speicherprofiling und -Tuning des router
  = und noch vieles mehr.

Wenn du dich langweilst und helfen möchtest, dir aber die Inspiration fehlt, könnte dich vielleicht einer der oben genannten Vorschläge auf Ideen bringen. Ich werde wahrscheinlich hin und wieder in einem Internetcafé vorbeischauen, daher bin ich per E-Mail erreichbar, aber die Antwortzeit wird in der Größenordnung von Tagen liegen.

* 5) ???

Okay, das ist fürs Erste so ziemlich alles, was ich ansprechen wollte. Für diejenigen, die in der kommenden Woche bei den SSU-Tests helfen möchten, haltet auf meinem Blog [3] nach Informationen Ausschau. Für den Rest von euch: Wir sehen uns im Meeting!

=jr [3] http://jrandom.dev.i2p/
