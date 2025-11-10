---
title: "I2P-Statusnotizen vom 2005-08-30"
date: 2005-08-30
author: "jr"
description: "Wöchentliches Update zum Netzwerkstatus der Version 0.6.0.3 mit NAT-Problemen, Bereitstellung der floodfill netDb und Fortschritten bei der Internationalisierung von Syndie"
categories: ["status"]
---

Hallo zusammen, es ist wieder soweit

* Index

1) Netzstatus 2) floodfill netDb 3) Syndie 4) ???

* 1) Net status

Nachdem 0.6.0.3 nun seit einer Woche veröffentlicht ist, sind die Rückmeldungen ziemlich gut, auch wenn die Protokollierung und die Anzeige für einige ziemlich verwirrend waren. Stand vor wenigen Minuten meldet I2P jedoch, dass eine beträchtliche Zahl von Nutzern ihre NATs oder Firewalls falsch konfiguriert hat – von 241 Peers haben 41 den Status auf ERR-Reject wechseln sehen, während 200 durchgehend OK waren (wenn sie einen expliziten Status erhalten können). Das ist nicht gut, hat aber geholfen, den Fokus noch etwas genauer darauf zu richten, was getan werden muss.

Since the release, there have been a few bugfixes for long standing error conditions, bringing the current CVS HEAD up to 0.6.0.3-4, which will likely be pushed out as 0.6.0.4 later this week.

* 2) floodfill netDb

Wie [1] in meinem Blog [2] besprochen, probieren wir eine neue abwärtskompatible netDb aus, die sowohl die von uns beobachtete Situation mit eingeschränkten Routen (20% der routers) angeht als auch die Dinge ein wenig vereinfacht. Die floodfill netDb wird als Teil von 0.6.0.3-4 ohne weitere Konfiguration bereitgestellt und funktioniert im Wesentlichen so, dass zunächst in der floodfill db abgefragt wird, bevor auf die bestehende kademlia db zurückgegriffen wird. Wenn ein paar Leute helfen möchten, es auszuprobieren, aktualisiert auf 0.6.0.3-4 und probiert es mal aus!

[1] http://syndiemedia.i2p.net/index.jsp?selector=entry://ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=/1125100800001 [2] http://syndiemedia.i2p.net/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=

* 3) Syndie

Die Entwicklung von Syndie schreitet sehr gut voran, wobei die vollständige remote syndication (Fern-Syndizierung) in Betrieb ist und für die Anforderungen von I2P optimiert wurde (die Anzahl der HTTP-Anfragen wird minimiert; stattdessen werden Ergebnisse und Uploads in multipart-HTTP-POSTs gebündelt). Die neue remote syndication bedeutet, dass Sie Ihre eigene lokale Syndie-Instanz betreiben, offline lesen und Beiträge verfassen können und diese später mit der Syndie eines anderen synchronisieren - neue Beiträge herunterladen und lokal erstellte Beiträge hochladen (entweder stapelweise, nach Blog oder nach Beitrag).

Eine öffentliche Syndie-Site ist syndiemedia.i2p (auch im Web unter http://syndiemedia.i2p.net/ erreichbar), deren öffentliche Archive unter http://syndiemedia.i2p/archive/archive.txt erreichbar sind (konfigurieren Sie Ihren Syndie-Knoten auf diese Adresse, um ihn zu synchronisieren). Die 'Startseite' auf dieser syndiemedia-Site wurde standardmäßig so gefiltert, dass nur mein Blog enthalten ist, aber Sie können über das Dropdown-Menü weiterhin auf die anderen Blogs zugreifen und Ihre Standardeinstellung entsprechend anpassen. (Mit der Zeit wird sich die Standardeinstellung von syndiemedia.i2p zu einer Sammlung von einführenden Beiträgen und Blogs ändern, was einen guten Einstieg in Syndie bietet.)

Eine der noch laufenden Arbeiten ist die Internationalisierung der Syndie-Codebasis. Ich habe meine lokale Kopie so angepasst, dass sie mit beliebigen Inhalten (beliebiger Zeichensatz / Gebietsschema / usw.) auf jedem Rechner (mit möglicherweise unterschiedlichen Zeichensätzen / Gebietsschemata / usw.) korrekt funktioniert und die Daten sauber ausliefert, sodass der Browser des Nutzers sie korrekt interpretieren kann. Allerdings bin ich auf Probleme mit einer Jetty-Komponente gestoßen, die Syndie verwendet, da deren Klasse zur Verarbeitung internationalisierter Multipart-Anfragen nicht zeichensatzsensitiv ist. Noch ;)

Wie auch immer, das bedeutet, dass, sobald der Internationalisierungs-Teil geklärt ist, Inhalte und Blogs über alle Sprachen hinweg darstellbar und bearbeitbar sein werden (aber natürlich noch nicht übersetzt). Bis dahin kann es allerdings passieren, dass erstellte Inhalte nach Abschluss der Internationalisierung zerschossen werden (da sich in den signierten Inhaltsbereichen UTF-8-Strings befinden). Aber trotzdem: Fühlt euch frei, ein bisschen herumzuhacken, und hoffentlich bekomme ich das heute Abend oder irgendwann morgen fertig.

Außerdem gehören zu den für SML [3] noch am Horizont stehenden Ideen ein [torrent attachment="1"]meine Datei[/torrent]-Tag, das eine Ein-Klick-Möglichkeit bieten würde, mit der Nutzer den angehängten Torrent in ihrem bevorzugten BT‑Client (susibt, i2p-bt, azneti2p oder sogar ein BT‑Client ohne I2P) starten können. Gibt es Nachfrage nach anderen Arten von Hooks (Einhängepunkte) (z. B. einem [ed2k]-Tag?), oder haben Leute völlig andere verrückte Ideen, um Inhalte in Syndie zu verbreiten?

[3] http://syndiemedia.i2p.net/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&entry=1124496000000

* 4) ???

Jedenfalls ist gerade jede Menge los, also schaut in 10 Minuten beim Treffen auf irc://irc.{postman,arcturus,freshcoffee}.i2p/#i2p oder freenode.net vorbei!

=jr
