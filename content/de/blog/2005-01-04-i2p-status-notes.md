---
title: "I2P-Statusnotizen für 2005-01-04"
date: 2005-01-04
author: "jr"
description: "Erste wöchentliche Statusnotizen des Jahres 2005 über das Netzwerkwachstum bis auf 160 routers, die Funktionen von 0.4.2.6 und die Entwicklung von 0.5"
categories: ["status"]
---

Hallo zusammen, es ist Zeit für unsere ersten wöchentlichen Statusnotizen des Jahres 2005

* Index

1) Netzstatus 2) 0.4.2.6 3) 0.5 4) jabber @ chat.i2p 5) ???

* 1) Net status

In der letzten Woche ist es im Netz ziemlich interessant gewesen - zu Silvester wurden auf einer beliebten Website Kommentare gepostet, in denen über i2p-bt gesprochen wurde, und wir hatten einen kleinen Schub neuer Nutzer. Derzeit gibt es zwischen 120-150 routers im Netz, wobei der Höchststand vor ein paar Tagen bei 160 lag. Das Netzwerk hat sich jedoch bewährt, indem leistungsfähige Peers (Gegenstellen) die zusätzliche Last aufgefangen haben, ohne andere Peers groß zu beeinträchtigen. Einige Nutzer, die ohne Bandbreitenbegrenzung auf sehr schnellen Verbindungen laufen, haben Durchsatzraten von 2-300KBps gemeldet, während diejenigen mit geringerer Kapazität auf die üblichen niedrigen 1-5KBps kommen.

Ich meine mich zu erinnern, dass Connelly erwähnte, er habe im Verlauf einiger Tage nach Neujahr 300+ verschiedene Router gesehen, sodass es eine erhebliche Fluktuation gab. Andererseits haben wir jetzt stetig 120-150 Nutzer online, im Gegensatz zu den bisherigen 80-90, was eine angemessene Steigerung ist. Wir möchten jedoch immer noch *nicht*, dass es schon zu sehr wächst, da es bekannte Implementierungsprobleme gibt, die noch erledigt werden müssen. Konkret wollen wir bis zum Release 0.6 [1] unter 2-300 Peers bleiben, um die Anzahl der Threads auf einem vernünftigen Niveau zu halten. Wenn jedoch jemand beim Implementieren des UDP-Transports helfen möchte, können wir das viel schneller erreichen.

In der letzten Woche habe ich die von den i2p-bt-Trackern veröffentlichten Statistiken beobachtet, und es wurden Gigabytes großer Dateien übertragen, mit einigen Berichten über 80-120KBps. IRC hatte seitdem diese Kommentare auf jener Website gepostet wurden, mehr Aussetzer als üblich, aber es vergehen immer noch Stunden zwischen den Verbindungsabbrüchen. (Soweit ich das beurteilen kann, läuft der router, auf dem irc.duck.i2p läuft, ziemlich nahe an seinem Bandbreitenlimit, was die Sache erklären würde)

[1] http://www.i2p.net/roadmap#0.6

* 2) 0.4.2.6

Seit dem 0.4.2.5-Release wurden in CVS einige Fehlerbehebungen und neue Funktionen hinzugefügt, die wir bald bereitstellen möchten, darunter Zuverlässigkeitskorrekturen für die Streaming-Bibliothek, eine verbesserte Widerstandsfähigkeit gegenüber Änderungen der IP-Adresse und die Bündelung von ragnaroks Adressbuch-Implementierung.

Wenn Sie vom Adressbuch noch nichts gehört haben oder es noch nicht benutzt haben, kurz gesagt: Es aktualisiert Ihre hosts.txt-Datei automatisch, indem es in regelmäßigen Abständen Änderungen von einigen anonym gehosteten Quellen abruft und zusammenführt (Standard sind http://dev.i2p/i2p/hosts.txt und http://duck.i2p/hosts.txt). Sie müssen keine Dateien ändern, keine Konfiguration anpassen und keine zusätzlichen Anwendungen ausführen - es wird im I2P router als Standard-.war-Datei bereitgestellt.

Natürlich, wenn Sie sich *wirklich* intensiv mit dem Adressbuch beschäftigen möchten, nur zu - Details finden Sie auf Ragnaroks Website [2]. Wenn Sie das Adressbuch bereits in Ihrem router installiert haben, müssen Sie beim Upgrade auf 0.4.2.6 ein wenig basteln, aber es funktioniert mit allen Ihren alten Konfigurationseinstellungen.

[2] http://ragnarok.i2p/

* 3) 0.5

Zahlen, Zahlen, Zahlen! Nun, wie ich bereits sagte, wird das Release 0.5 überarbeiten, wie das Tunnel-Routing funktioniert, und es gibt Fortschritte in dieser Richtung. In den letzten Tagen habe ich den neuen Verschlüsselungs-Code (und Unit-Tests) implementiert, und sobald sie funktionieren, werde ich ein Dokument veröffentlichen, das meine aktuellen Überlegungen dazu beschreibt, wie, was und warum das neue Tunnel-Routing funktionieren soll. Ich implementiere die Verschlüsselung dafür jetzt statt später, damit die Leute konkret nachvollziehen können, was das bedeutet, sowie Problemstellen finden und Vorschläge zur Verbesserung machen können. Ich hoffe, den Code bis zum Ende der Woche lauffähig zu haben, also gibt es vielleicht dieses Wochenende weitere Dokumente. Keine Versprechen allerdings.

* 4) jabber @ chat.i2p

jdot hat einen neuen Jabber-Server aufgesetzt, und er scheint sowohl für Einzelgespräche als auch für Gruppenchat ziemlich gut zu funktionieren. Schau dir die Infos im Forum [3] an. Der I2P-Dev-Diskussionskanal bleibt weiterhin der IRC #i2p, aber es ist immer schön, Alternativen zu haben.

[3] http://forum.i2p.net/viewtopic.php?t=229

* 5) ???

Okay, das ist so ziemlich alles, was ich im Moment zu erwähnen habe – ich bin mir sicher, dass noch vieles mehr passiert, das andere ansprechen möchten, also schaut in 15 Minuten beim Treffen am üblichen Ort [4] vorbei und sagt uns, was los ist!

=jr
