---
title: "I2P Statusnotizen für 2004-09-08"
date: 2004-09-08
author: "jr"
description: "Wöchentlicher I2P-Statusbericht zu Release 0.4, Kapazitätsproblemen im Netzwerk, Website-Updates und Verbesserungen an der I2PTunnel-Benutzeroberfläche"
categories: ["status"]
---

Hallo zusammen, entschuldigt die Verspätung...

## Stichwortverzeichnis:

1. 0.4
2. Capacity and overload
3. Website updates
4. I2PTunnel web interface
5. Roadmap and todo
6. ???

## 1) 0.4

Wie ihr sicher alle gesehen habt, ist das Release 0.4 neulich erschienen, und insgesamt läuft es ziemlich gut. Es ist kaum zu glauben, dass es schon 6 Monate her ist, seit 0.3 erschienen ist (und ein Jahr, seit das 1.0 SDK veröffentlicht wurde), aber wir haben einen langen Weg zurückgelegt, und eure harte Arbeit, euer Enthusiasmus und eure Geduld haben Wunder bewirkt. Glückwunsch und danke!

Wie bei jeder guten Veröffentlichung haben wir, kaum dass sie draußen war, einige Probleme gefunden, und in den letzten Tagen haben wir Fehlerberichte gesammelt und wie verrückt gepatcht (Sie können die Änderungen verfolgen, während wir die Probleme beheben). Wir haben noch ein paar weitere Fehler zu beseitigen, bevor wir die nächste Revision veröffentlichen, aber das sollte im Laufe des nächsten Tages oder so erledigt sein.

## 2) Kapazität und Überlastung

Wir haben in den letzten paar Releases einige ziemlich unausgewogene Zuweisungen von tunnels beobachtet, und obwohl einige davon fehlerbedingt sind (zwei davon seit 0.4 behoben), bleibt dennoch eine allgemeine Frage zum Algorithmus offen - wann sollte ein router aufhören, weitere tunnels zu akzeptieren?

Vor einigen Revisionen haben wir Code zur Drosselung hinzugefügt, um Anfragen zur Teilnahme an einem tunnel abzulehnen, wenn der router überlastet war (die lokale Nachrichtenverarbeitungszeit überschreitet 1s), und das hat erheblich geholfen. Allerdings gibt es zwei Aspekte dieses einfachen Algorithmus, die nicht berücksichtigt werden: - wenn unsere Bandbreite ausgelastet ist, kann unsere lokale Verarbeitungszeit trotzdem schnell sein, sodass wir weiterhin mehr tunnel-Anfragen akzeptieren würden - wenn ein einzelner Peer an „zu vielen“ tunnels teilnimmt, schadet es dem Netzwerk stärker, wenn diese ausfallen.

Das erste Problem lässt sich ziemlich einfach dadurch lösen, dass man den Bandbreitenbegrenzer aktiviert (da die Bandbreitenbegrenzung die Nachrichtenverarbeitungszeit entsprechend der Bandbreitenverzögerung verlangsamt). Das zweite ist komplizierter, und sowohl mehr Forschung als auch mehr Simulation sind notwendig. Ich denke an etwas in der Art, tunnel-Anfragen probabilistisch abzulehnen, basierend auf dem Verhältnis der tunnel, an denen wir teilnehmen, zu den vom Netzwerk angeforderten tunnel, einschließlich eines Basis-„Freundlichkeitsfaktors“, wobei P(reject) = 0 gesetzt wird, wenn unsere Teilnahme darunter liegt.

Aber wie gesagt, weitere Arbeit und Simulation sind erforderlich.

## 3) Website-Aktualisierungen

Jetzt, da wir die neue I2P-Weboberfläche haben, ist so gut wie unsere gesamte alte Endnutzer-Dokumentation veraltet. Wir brauchen Hilfe dabei, diese Seiten durchzugehen und sie so zu aktualisieren, dass sie den aktuellen Stand widerspiegeln. Wie von duck und anderen vorgeschlagen, brauchen wir einen neuen 'kickstart'-Leitfaden über das readme unter `http://localhost:7657/` hinaus - etwas, das Leute schnell an den Start bringt und ins System hineinführt.

Außerdem bietet unsere neue Weboberfläche reichlich Platz für die Integration kontextsensitiver Hilfe. Wie Sie in der mitgelieferten help.jsp sehen können, „Hmm. Wir sollten hier wahrscheinlich etwas Hilfetext hinzufügen.“

Es wäre wahrscheinlich großartig, wenn wir zu den verschiedenen Seiten Links zu 'Über' und/oder 'Fehlerbehebung' hinzufügen könnten, die erklären, was die einzelnen Elemente bedeuten und wie man sie verwendet.

## 4) I2PTunnel-Weboberfläche

Die neue `http://localhost:7657/i2ptunnel/`-Benutzeroberfläche als „spartanisch“ zu bezeichnen, wäre eine Untertreibung. Wir müssen noch viel Arbeit hineinstecken, um das näher an einen brauchbaren Zustand zu bringen – derzeit ist die Funktionalität zwar technisch vorhanden, aber man muss wirklich wissen, was hinter den Kulissen vor sich geht, um das zu verstehen. Ich denke, duck könnte dazu noch weitere Ideen haben, die duck im Meeting zur Sprache bringen möchte.

## 5) Roadmap und To-do-Liste

Ich war nachlässig dabei, die Roadmap aktuell zu halten, aber Tatsache ist, dass weitere Überarbeitungen vor uns liegen. Um zu erläutern, was ich als die „großen Probleme“ ansehe, habe ich eine neue Aufgabenliste zusammengestellt, die jedes davon etwas detaillierter beleuchtet. Ich denke, wir sollten an diesem Punkt ziemlich offen dafür sein, unsere Optionen zu prüfen und vielleicht die Roadmap zu überarbeiten.

Eine Sache, die ich auf dieser To-Do-Liste zu erwähnen vergessen habe, ist, dass wir beim Hinzufügen des leichtgewichtigen Verbindungsprotokolls die (optionale) automatische Erkennung der IP-Adresse einbauen können. Das mag 'gefährlich' sein (weshalb sie optional sein wird), aber es wird die Anzahl der Support-Anfragen, die wir erhalten, drastisch reduzieren :)

Jedenfalls sind die Punkte, die auf der To-Do-Liste stehen, solche, die wir für verschiedene Releases vorgesehen hatten, und sie werden ganz sicher nicht alle in 1.0 oder sogar 2.0 enthalten sein. Ich habe ein paar unterschiedliche mögliche Priorisierungen/Release-Planungen skizziert, aber darauf bin ich noch nicht festgelegt. Wenn Leute weitere große Themen identifizieren können, die auf dem Weg liegen, wäre das sehr willkommen, denn ein ungeplantes Thema ist immer ein echtes Ärgernis.

## 6) ???

Okay, das war’s für den Moment (ist auch gut so, denn das Meeting beginnt in ein paar Minuten). Schau um 21 Uhr GMT bei #i2p auf irc.freenode.net, www.invisiblechat.com oder irc.duck.i2p vorbei, um weiter zu chatten.
