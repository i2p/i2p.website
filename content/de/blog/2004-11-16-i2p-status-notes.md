---
title: "I2P-Statusnotizen für 2004-11-16"
date: 2004-11-16
author: "jr"
description: "Wöchentliches I2P-Status-Update zu Netzwerküberlastung, Fortschritten bei der Streaming-Bibliothek, BitTorrent-Entwicklungen und anstehenden Veröffentlichungsplänen"
categories: ["status"]
---

Hallo zusammen, es ist wieder Dienstag

## Stichwortverzeichnis

1. Congestion
2. Streaming
3. BT
4. ???

## 1) Überlastung

Ich weiß, ich durchbreche die Gewohnheit, Punkt 1 "Netzstatus" zu nennen, aber diese Woche erscheint "Überlastung" passend. Das Netzwerk selbst lief insgesamt ziemlich gut, aber mit der steigenden Nutzung von BitTorrent wurde das Netz immer stärker überlastet, was im Wesentlichen zu einem Überlastungskollaps führte.

Das war zu erwarten und bestärkt nur unseren Plan - die neue Streaming-Bibliothek herauszubringen und unser tunnel-Management zu überarbeiten, damit wir über ausreichende Daten zu Peers verfügen, die wir nutzen können, wenn unsere schnellen Peers ausfallen. Es gab bei den jüngsten Netzwerkproblemen noch einige andere Faktoren, aber der Großteil lässt sich auf den Anstieg der Überlastung und die daraus resultierenden tunnel-Ausfälle zurückführen (die ihrerseits zu allerlei wilder Peer-Auswahl führten).

## 2) Streaming

Es gab eine Menge Fortschritte bei der streaming lib (Streaming‑Bibliothek), und ich habe einen Squid‑Proxy darüber im Live‑Netz angebunden, den ich häufig für mein normales Web‑Browsing nutze. Mit mules Hilfe haben wir die Streams auch ziemlich hart belastet, indem wir frost und FUQID durchs Netzwerk geleitet haben (mein Gott, mir war vorher nie klar, wie aggressiv frost ist!). Auf diese Weise konnten einige bedeutende, seit Langem bestehende Fehler aufgespürt werden, und es wurden Anpassungen hinzugefügt, um sehr große Zahlen von Verbindungen besser zu kontrollieren.

Bulk-Streams funktionieren ebenfalls hervorragend, sowohl mit Slow Start als auch mit Congestion Avoidance, und die schnellen Sende-/Antwort-Verbindungen (à la HTTP get+response) tun genau das, was sie sollen.

Ich rechne damit, dass wir in den nächsten Tagen einige Freiwillige rekrutieren, um es weiter auszurollen, und hoffentlich kommen wir damit bald auf Version 0.4.2. Ich möchte nicht behaupten, es sei so gut, dass es dir den Abwasch macht, und ich bin sicher, dass uns ein paar Bugs durchrutschen werden, aber es wirkt vielversprechend.

## 3) BT

Abgesehen von den jüngsten Netzwerkproblemen macht die i2p-bt-Portierung große Fortschritte. Ich weiß, dass ein paar Leute darüber mehr als ein GB Daten heruntergeladen haben, und die Performance war wie erwartet (aufgrund der alten Streaming-Bibliothek, ~4 KB/s pro Peer im Schwarm). Ich versuche, bei der im #i2p-bt-Channel besprochenen Arbeit mitzuhören – vielleicht könnte duck uns im Meeting eine Zusammenfassung geben?

## 4) ???

Das war’s erstmal von mir. Wir sehen uns alle in ein paar Minuten im Meeting.

=jr
