---
title: "I2P Statusnotizen für 2005-08-23"
date: 2005-08-23
author: "jr"
description: "Wöchentliches Update zu Verbesserungen im Release 0.6.0.3, dem Netzwerkstatus von Irc2P, dem susibt Web-Frontend für i2p-bt und sicherem Bloggen mit Syndie"
categories: ["status"]
---

Hi zusammen, es ist wieder Zeit für die wöchentlichen Statusnotizen

* Index

1) 0.6.0.3 Status 2) IRC Status 3) susibt 4) Syndie 5) ???

* 1) 0.6.0.3 status

Wie neulich erwähnt [1], haben wir eine neue 0.6.0.3-Version veröffentlicht, die bereitsteht. Sie ist eine große Verbesserung gegenüber der 0.6.0.2-Version (es ist nicht ungewöhnlich, mehrere Tage ohne Disconnect auf irc zu haben - ich hatte 5 Tage Uptime, die erst durch ein Upgrade beendet wurden), aber es gibt ein paar Dinge, die man beachten sollte. Trotzdem ist es nicht immer so - Menschen mit langsamen Netzverbindungen stoßen auf Probleme, aber es ist ein Fortschritt.

Eine (sehr) häufige Frage ist zum Peer-Test-Code aufgekommen – "Warum steht dort Status: Unknown?" Unknown ist *völlig in Ordnung* – es ist KEIN Hinweis auf ein Problem. Außerdem, wenn du siehst, dass es manchmal zwischen "OK" und "ERR-Reject" wechselt, bedeutet das NICHT, dass alles in Ordnung ist – wenn du jemals ERR-Reject siehst, heißt das sehr wahrscheinlich, dass du ein NAT- oder Firewall-Problem hast. Ich weiß, das ist verwirrend, und es wird später ein Release mit einer klareren Statusanzeige (und, wenn möglich, automatischer Behebung) geben, aber fürs Erste wundere dich nicht, wenn ich dich ignoriere, wenn du sagst "omg es ist kaputt!!!11 der Status ist Unknown!" ;)

(Der Grund für die übermäßigen Unknown-Statuswerte ist, dass wir Peer-Tests ignorieren, bei denen "Charlie" [2] jemand ist, mit dem wir bereits eine SSU-Sitzung haben, da dies impliziert, dass er durch unser NAT kommen könnte, selbst wenn unser NAT fehlerhaft ist)

[1] http://dev.i2p.net/pipermail/i2p/2005-August/000844.html [2] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/udp.html?rev=HEAD#peerTesting

* 2) IRC status

Wie oben erwähnt, haben die Irc2P-Betreiber großartige Arbeit mit ihrem Netzwerk geleistet, da die Latenz deutlich gesunken und die Zuverlässigkeit deutlich gestiegen ist – ich habe seit Tagen keinen Netsplit gesehen. Es gibt dort außerdem einen neuen IRC-Server, womit wir jetzt 3 haben - irc.postman.i2p, irc.arcturus.i2p und irc.freshcoffee.i2p. Vielleicht kann uns jemand von Irc2P während des Treffens ein Update zu ihrem Fortschritt geben?

* 3) susibt

susi23 (bekannt durch susimail) ist zurück mit zwei bt-bezogenen Tools - susibt [3] und einem neuen Tracker-Bot [4]. susibt ist eine Webanwendung (die sich mit minimalem Aufwand in Ihrer i2p-Jetty-Instanz bereitstellen lässt) zur Verwaltung des Betriebs von i2p-bt. Wie es auf ihrer Website heißt:

SusiBT ist ein Web-Frontend für i2p-bt. Es integriert sich in Ihren i2p   router und ermöglicht automatische Uploads und Downloads, setzt nach   einem Neustart fort und bietet einige Verwaltungsfunktionen wie Datei-Upload und   -Download. Spätere Versionen der Anwendung werden die automatische   Erstellung und das Hochladen von Torrent-Dateien unterstützen.

[3] http://susi.i2p/?page_id=31 [4] http://susi.i2p/?p=33

Kann ich ein "w00t" hören?

* 4) Syndie

Wie auf der Liste und im Channel erwähnt, haben wir eine neue Client-App für sicheres und authentifiziertes Blogging / Content-Distribution. Mit Syndie erübrigt sich die Frage "Ist deine eepsite(I2P Site) online", da du die Inhalte lesen kannst, selbst wenn die Site offline ist, aber Syndie vermeidet all die unschönen Probleme, die Content-Distribution-Netzwerken innewohnen, indem es sich auf das Frontend konzentriert. Wie auch immer, es ist noch deutlich in Arbeit, aber wenn du einsteigen und es ausprobieren möchtest, gibt es einen öffentlichen Syndie-Knoten unter http://syndiemedia.i2p/ (auch über das Web erreichbar unter http://66.111.51.110:8000/). Geh ruhig rein und erstelle einen Blog, oder wenn du abenteuerlustig bist, poste ein paar Kommentare/Vorschläge/Bedenken! Natürlich sind Patches willkommen, ebenso wie Funktionsvorschläge, also leg los.

* 5) ???

Zu sagen, dass viel los ist, ist eine ziemliche Untertreibung ... abgesehen vom oben Genannten, hacke ich an ein paar Verbesserungen an der Kongestionskontrolle von SSU (-1 ist bereits in cvs), an unserem Bandbreitenbegrenzer und an der netDb (für die gelegentliche Nichterreichbarkeit von Sites), sowie debugge ich das im Forum gemeldete CPU-Problem. Ich bin sicher, dass andere ebenfalls an ein paar coolen Dingen hacken, über die sie berichten können, also schauen sie hoffentlich heute Abend beim Meeting vorbei, um sich auszulassen :)

Also, wir sehen uns heute Abend um 20:00 Uhr GMT in #i2p auf den üblichen Servern!

=jr
