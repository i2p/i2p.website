---
title: "I2P-Statusnotizen für 2005-10-11"
date: 2005-10-11
author: "jr"
description: "Wöchentliche Aktualisierung über den Erfolg der Veröffentlichung 0.6.1.2, den neuen I2PTunnelIRCClient-Proxy zum Filtern unsicherer IRC-Nachrichten, die Syndie CLI und RSS-zu-SML-Konvertierung sowie Pläne zur I2Phex-Integration"
categories: ["status"]
---

Hi zusammen, es ist wieder Dienstag

* Index

1) 0.6.1.2 2) I2PTunnelIRCClient 3) Syndie 4) I2Phex 5) Steganographie und Darknets (bzgl. Flamewar) 6) ???

* 1) 0.6.1.2

Das Release 0.6.1.2 von letzter Woche ist bisher ziemlich gut verlaufen – 75 % des Netzwerks haben ein Upgrade durchgeführt, HTTP POST funktioniert einwandfrei, und die streaming lib (Streaming-Bibliothek) überträgt Daten recht effizient (die vollständige Antwort auf eine HTTP-Anfrage wird oft in einem einzigen Ende-zu-Ende-Roundtrip empfangen). Das Netzwerk ist auch ein wenig gewachsen – stabil liegt die Zahl bei etwa 400 Peers, allerdings stieg sie während des Höhepunkts der digg/gotroot [1]-Erwähnung am Wochenende mit Churn (Knotenfluktuation) auf 600–700 an.

[1] http://gotroot.com/tiki-read_article.php?articleId=195     (ja, wirklich ein alter Artikel, ich weiß, aber jemand hat ihn wiederentdeckt)

Seit 0.6.1.2 veröffentlicht wurde, ist noch mehr Gutes hinzugekommen – die Ursache der jüngsten irc2p-Netsplits wurde gefunden (und behoben), ebenso wurden ziemlich umfangreiche Verbesserungen an der Paketübertragung von SSU vorgenommen (wodurch über 5 % der Pakete eingespart werden). Ich weiß nicht genau, wann 0.6.1.3 herauskommen wird, aber vielleicht später in dieser Woche. Wir werden sehen.

* 2) I2PTunnelIRCClient

Neulich, nach einigen Diskussionen, hat dust schnell eine neue Erweiterung für I2PTunnel entwickelt - der "ircclient"-Proxy. Er funktioniert, indem er die über I2P zwischen Client und Server gesendeten und empfangenen Inhalte filtert, unsichere IRC-Nachrichten entfernt und solche umschreibt, die angepasst werden sollten. Nach einigen Tests sieht es ziemlich gut aus, und dust hat es zu I2PTunnel beigetragen und es wird nun den Nutzern über die Weboberfläche angeboten. Es ist großartig, dass die irc2p-Leute ihre IRC-Server so gepatcht haben, dass unsichere Nachrichten verworfen werden, aber jetzt müssen wir uns nicht mehr darauf verlassen, dass sie das tun - der lokale Benutzer hat die Kontrolle über die eigene Filterung.

Die Verwendung ist ziemlich einfach - anstatt wie bisher einen "Client proxy" für IRC zu erstellen, erstellen Sie einfach einen "IRC proxy". Wenn Sie Ihren vorhandenen "Client proxy" in einen "IRC proxy" umwandeln möchten, können Sie (peinlich) die Datei i2ptunnel.config bearbeiten und "tunnel.1.type=client" in "tunnel.1.ircclient" ändern (oder welche Nummer auch immer für Ihren Proxy passend ist).

Wenn alles gut geht, wird dies in der nächsten Version zum Standard-I2PTunnel-Proxytyp für IRC-Verbindungen.

Gute Arbeit, dust, danke!

* 3) Syndie

Ragnaroks zeitgesteuerte Syndizierungsfunktion scheint gut zu laufen, und seit 0.6.1.2 erschienen ist, sind zwei neue Funktionen hinzugekommen - ich habe eine neue, vereinfachte CLI (Kommandozeilenschnittstelle) hinzugefügt, um in Syndie [2] zu posten, und dust (juhu, dust!) hat schnell etwas Code geschrieben, um Inhalte aus einem RSS/Atom-Feed zu extrahieren, darin referenzierte Enclosures (Anhänge) oder Bilder einzubinden und die RSS-Inhalte in SML (!!!) [3][4] zu konvertieren.

Die Auswirkungen der beiden in Kombination sollten klar sein. Weitere Neuigkeiten, sobald es welche gibt.

[2] http://syndiemedia.i2p/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&entry=1128816000000&expand=true [3] http://syndiemedia.i2p/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&entry=1128816000001&expand=true [4] http://dust.i2p/Sucker.java     (wir werden es in Kürze in CVS integrieren)

* 4) I2Phex

Es heißt, dass I2Phex ziemlich gut funktioniert, dass aber im Laufe der Zeit weiterhin Probleme bestehen. Im Forum [5] gab es einige Diskussionen darüber, wie es weitergehen soll, und GregorK, der leitende Phex-Entwickler, hat sich sogar zu Wort gemeldet und Unterstützung dafür bekundet, die I2Phex-Funktionalität wieder in Phex zu integrieren (oder zumindest die Hauptversion von Phex eine einfache Plugin-Schnittstelle für die Transportschicht anbieten zu lassen).

Das wäre richtig genial, denn es würde bedeuten, dass viel weniger Code zu warten ist, und außerdem würden wir von der Arbeit des Phex-Teams zur Verbesserung der Codebasis profitieren. Damit das funktioniert, brauchen wir jedoch ein paar Hacker, die sich melden und die Migration in die Hand nehmen. Der I2Phex-Code macht ziemlich klar, wo sirup Änderungen vorgenommen hat, daher sollte es nicht allzu schwer sein, aber wahrscheinlich auch nicht ganz trivial ;)

Ich habe im Moment nicht wirklich Zeit, mich darum zu kümmern, aber schau im Forum vorbei, wenn du helfen möchtest.

[5] http://forum.i2p.net/viewforum.php?f=25

* 5) Stego and darknets (re: flamewar)

Die Mailingliste [6] war in letzter Zeit aufgrund der Diskussion über Steganographie und Darknets ziemlich aktiv. Das Thema hat sich weitgehend auf die Freenet-Tech-Liste [7] unter dem Betreff "I2P conspiracy theories flamewar" verlagert, ist aber noch im Gange.

Ich bin mir nicht sicher, ob ich viel hinzufügen kann, was nicht ohnehin schon Teil der Beiträge selbst ist, aber einige Leute haben erwähnt, dass die Diskussion ihnen beim Verständnis von I2P und Freenet geholfen hat, also könnte es sich lohnen, mal reinzuschauen. Oder auch nicht ;)

[6] http://dev.i2p.net/pipermail/i2p/2005-October/thread.html [7] nttp://news.gmane.org/gmane.network.freenet.technical

* 6) ???

Wie ihr seht, passiert gerade eine Menge Spannendes, und ich bin mir sicher, dass ich einiges übersehen habe. Schaut in ein paar Minuten bei #i2p vorbei zu unserem wöchentlichen Meeting und sagt Hallo!

=jr
