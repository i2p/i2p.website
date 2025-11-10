---
title: "I2P-Statusnotizen für 2004-10-26"
date: 2004-10-26
author: "jr"
description: "Wöchentliches I2P-Status-Update zu Netzwerkstabilität, Entwicklung der Streaming-Bibliothek sowie Fortschritten bei mail.i2p und BitTorrent"
categories: ["status"]
---

Hallo zusammen, Zeit für das wöchentliche Update

## Stichwortverzeichnis

1. Net status
2. Streaming lib
3. mail.i2p progress
4. ???

## 1) Netzstatus

Ich will es nicht verschreien, aber in der letzten Woche war das Netzwerk im Großen und Ganzen wie zuvor - für irc ziemlich stabil, eepsites(I2P Sites) laden zuverlässig, obwohl große Dateien oft weiterhin das Fortsetzen des Downloads erfordern. Im Grunde gibt es nichts Neues zu berichten, abgesehen von der Tatsache, dass es nichts Neues zu berichten gibt.

Oh, eine Sache, die wir herausgefunden haben, ist, dass Jetty zwar HTTP resume (Fortsetzen von HTTP-Downloads) unterstützt, aber nur für HTTP 1.1. Das ist für die meisten Browser und Download-Tools in Ordnung, *außer* wget - wget sendet die Fortsetzungsanfrage als HTTP 1.0. Also verwendet zum Herunterladen großer Dateien curl oder ein anderes Tool, das Resume über HTTP 1.1 unterstützt (Danke an duck und ardvark fürs Recherchieren und Finden einer Lösung!)

## 2) Streaming-Bibliothek

Da das Netzwerk in letzter Zeit ziemlich stabil war, habe ich fast meine gesamte Zeit damit verbracht, an der neuen Streaming-Bibliothek zu arbeiten. Auch wenn sie noch nicht fertig ist, gab es große Fortschritte – die grundlegenden Szenarien funktionieren alle einwandfrei, die Gleitfenster sorgen zuverlässig für die Selbsttaktung, und aus Sicht des Clients funktioniert die neue Bibliothek als unmittelbarer Ersatz ohne Anpassungen (Drop-in-Replacement) für die alte. Die beiden Streaming-Bibliotheken können allerdings nicht miteinander kommunizieren.

In den letzten Tagen habe ich einige weitere interessante Szenarien durchgearbeitet. Das wichtigste ist das latenzbehaftete Netzwerk, das wir simulieren, indem wir bei empfangenen Nachrichten Verzögerungen einfügen – entweder eine einfache zufällige Verzögerung von 0–30 s oder eine gestaffelte Verzögerung (in 80 % der Fälle 0–10 s Latenz, in 10 % 10–20 s, 5 % 20–30 s, 3 % 30–40 s, 4 % 40–50 s). Ein weiterer wichtiger Test war das zufällige Verwerfen von Nachrichten – das sollte im I2P-Netzwerk nicht häufig vorkommen, aber wir sollten damit umgehen können.

Die Gesamtleistung war bisher ziemlich gut, aber es gibt noch viel zu tun, bevor wir das im Live-Netz bereitstellen können. Dieses Update wird 'gefährlich' sein, insofern es enorm leistungsstark ist - wenn wir es katastrophal falsch machen, können wir uns im Handumdrehen selbst mit einem DDoS lahmlegen, aber wenn wir es richtig machen, nun, sagen wir einfach, dass darin erhebliches Potenzial steckt (weniger versprechen und mehr liefern).

Damit gesagt und da sich das Netzwerk weitgehend im 'steady state' befindet, habe ich es nicht eilig, etwas herauszubringen, das nicht ausreichend getestet ist. Weitere Neuigkeiten, sobald es welche gibt.

## 3) Fortschritt bei mail.i2p

postman und seine Crew haben intensiv an E-Mail über I2P gearbeitet (siehe www.postman.i2p), und es stehen einige spannende Neuerungen in der Pipeline - vielleicht hat postman ein Update für uns?

Nebenbei bemerkt, ich verstehe die Forderungen nach einer Webmail-Oberfläche gut und kann sie nachvollziehen, aber postman ist stark ausgelastet mit einigen interessanten Arbeiten am Backend des Mail-Systems. Eine Alternative ist jedoch, eine Webmail-Oberfläche *lokal* auf Ihrem eigenen Webserver zu installieren - es gibt Webmail-JSP/Servlet-Lösungen. Damit könnten Sie Ihre eigene lokale Webmail-Oberfläche z. B. unter `http://localhost:7657/mail/` betreiben.

Ich weiß, dass es da draußen einige Open-Source-Skripte für den Zugriff auf pop3-Konten gibt, damit sind wir schon auf halbem Weg - vielleicht könnte jemand mal schauen, ob es welche gibt, die pop3 und authentifiziertes SMTP unterstützen? Komm schon, du weißt, dass du es willst!

## 4) ???

Ok, das ist alles, was ich im Moment zu sagen habe - schaut in ein paar Minuten beim Meeting vorbei und lasst uns wissen, was los ist.

=jr
