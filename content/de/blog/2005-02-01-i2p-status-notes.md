---
title: "I2P-Statushinweise vom 2005-02-01"
date: 2005-02-01
author: "jr"
description: "Wöchentliche Notizen zum I2P-Entwicklungsstatus, die den Fortschritt bei der tunnel-Verschlüsselung 0.5, einen neuen NNTP-Server und technische Vorschläge abdecken"
categories: ["status"]
---

Hi zusammen, Zeit für das wöchentliche Status-Update

* Index

1) 0.5 Status 2) nntp 3) technische Vorschläge 4) ???

* 1) 0.5 status

Es gab in Bezug auf Version 0.5 viele Fortschritte, mit einer großen Anzahl von Commits gestern. Der Großteil des router verwendet jetzt die neue tunnel encryption und tunnel pooling [1], und es hat im Testnetz gut funktioniert. Es sind noch einige zentrale Teile zu integrieren, und der Code ist offensichtlich nicht abwärtskompatibel, aber ich hoffe, dass wir irgendwann nächste Woche eine Bereitstellung in größerem Umfang vornehmen können.

Wie bereits erwähnt, wird die anfängliche Version 0.5 die Grundlage schaffen, auf der verschiedene Auswahl- und Reihenfolgestrategien für tunnel-Peers zum Einsatz kommen können. Wir beginnen mit einem grundlegenden Satz konfigurierbarer Parameter für die Erkundungs- und Client-Pools, aber spätere Versionen werden voraussichtlich weitere Optionen für unterschiedliche Nutzerprofile enthalten.

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/tunnel-alt.html?rev=HEAD

* 2) nntp

Wie auf LazyGuys Seite [2] und meinem Blog [3] erwähnt, haben wir einen neuen NNTP-Server im Netzwerk in Betrieb, erreichbar unter nntp.fr.i2p. Während LazyGuy einige suck [4] Skripte gestartet hat, um ein paar Listen von gmane einzulesen, sind die Inhalte im Wesentlichen von, für und durch I2P-Nutzer.  jdot, LazyGuy und ich haben untersucht, welche Newsreader sich sicher verwenden lassen, und es scheint einige recht einfache Lösungen zu geben.  Siehe meinen Blog für Anleitungen zum Einsatz von slrn [5] für anonymes Lesen und Posten.

[2] http://fr.i2p/ [3] http://jrandom.dev.i2p/ [4] http://freshmeat.net/projects/suck/ [5] http://freshmeat.net/projects/slrn/

* 3) tech proposals

Orion und andere haben auf ughas Wiki [6] eine Reihe von RFCs zu verschiedenen technischen Themen eingestellt, um einige der schwierigeren Probleme auf Client- und App-Ebene weiter auszuarbeiten. Bitte verwenden Sie das als Ort, um Namensfragen, Updates zu SAM, Swarming-Ideen und Ähnliches zu diskutieren – wenn Sie dort etwas posten, können wir alle jeweils von unserem Ort aus zusammenarbeiten, um ein besseres Ergebnis zu erzielen.

[6] http://ugha.i2p/I2pRfc

* 4) ???

Das ist alles, was ich im Moment habe (was auch gut ist, denn das Meeting beginnt gleich).  Wie immer, postet eure Gedanken, wann und wo auch immer :)

=jr
