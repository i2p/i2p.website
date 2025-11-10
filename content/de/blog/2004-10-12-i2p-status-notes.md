---
title: "I2P-Statusnotizen für 2004-10-12"
date: 2004-10-12
author: "jr"
description: "Wöchentliches I2P-Status-Update mit den Themen 0.4.1.2-Release, Experimente zur dynamischen Drosselung, Entwicklung der Streaming-Bibliothek für 0.4.2 und E-Mail-Diskussionen"
categories: ["status"]
---

Hallo zusammen, es ist Zeit für unser wöchentliches Update

## Stichwortverzeichnis:

1. 0.4.1.2
2. 0.4.1.3
3. 0.4.2
4. mail discussions
5. ???

## 1) 0.4.1.2

Die neue Version 0.4.1.2 ist seit ein paar Tagen verfügbar und im Großen und Ganzen läuft alles wie erwartet - es gab allerdings ein paar Probleme mit der neuen Watchdog-Komponente, wodurch sie Ihren router beendet, wenn die Dinge Bad sind, statt ihn neu zu starten. Wie ich heute bereits erwähnt habe, suche ich nach Leuten, die das neue Stats-Logging-Tool verwenden, um mir einige Daten zu senden, daher wäre Ihre Hilfe dort sehr willkommen.

## 2) 0.4.1.3

Es wird noch ein weiteres Release geben, bevor 0.4.2 erscheint, weil ich möchte, dass das Netzwerk so stabil wie möglich ist, bevor ich weitermache. Woran ich derzeit arbeite, ist eine dynamische Drosselung der tunnel-Teilnahme – routers anweisen, Anfragen probabilistisch abzulehnen, wenn sie überlastet sind oder ihre tunnels langsamer als üblich sind. Diese Wahrscheinlichkeiten und Schwellenwerte werden dynamisch aus den erhobenen Statistiken berechnet – wenn deine 10‑Minuten tunnel test time größer ist als deine 60‑Minuten tunnel test time, akzeptiere die tunnel-Anfrage mit einer Wahrscheinlichkeit von 60minRate/10minRate (und wenn deine aktuelle Anzahl von tunnels größer ist als dein 60‑Minuten‑Durchschnitt an tunnels, akzeptiere sie mit p=60mRate/curTunnels).

Eine weitere mögliche Drosselung besteht darin, die Bandbreite in diesem Sinne zu glätten - tunnels probabilistisch abzulehnen, wenn unsere Bandbreitennutzung sprunghaft ansteigt. Jedenfalls ist die Absicht des Ganzen, die Netzwerknutzung zu entzerren und die tunnels auf mehr Teilnehmer zu verteilen. Das Hauptproblem, das wir mit der Lastverteilung hatten, war ein überwältigender *Überschuss* an Kapazität, und daher wurde keiner unserer "verdammt, wir sind langsam, wir lehnen ab"-Trigger ausgelöst. Diese neuen probabilistischen Drosselungen sollten hoffentlich schnelle Veränderungen im Zaum halten.

Ich habe keinen konkreten Plan, wann das Release 0.4.1.3 herauskommen wird - vielleicht am Wochenende. Die Daten, die Leute einsenden (siehe oben), sollten dabei helfen festzustellen, ob sich das lohnen wird oder ob es andere, lohnendere Ansätze gibt.

## 3) 0.4.2

Wie in der Besprechung letzte Woche besprochen, haben wir die Releases 0.4.2 und 0.4.3 vertauscht - 0.4.2 wird die neue Streaming-Bibliothek sein, und 0.4.3 wird das tunnel-Update sein.

Ich habe die Literatur zur Streaming-Funktionalität von TCP erneut überprüft, und es gibt einige interessante Aspekte, die für I2P relevant sind. Insbesondere spricht unsere hohe Round-Trip-Zeit (RTT) für etwas wie XCP, und wir sollten wahrscheinlich ziemlich aggressiv verschiedene Formen von Explicit Congestion Notification (ECN) einsetzen, obwohl wir von etwas wie der Timestamp-Option keinen Gebrauch machen können, da unsere Uhren um bis zu eine Minute abweichen können.

Außerdem wollen wir sicherstellen, dass wir die Streaming-Bibliothek optimieren können, um kurzlebige Verbindungen zu handhaben (worin reines TCP ziemlich schlecht ist) - zum Beispiel möchte ich in der Lage sein, kleine (<32KB) HTTP-GET-Anfragen und kleine (<32KB) Antworten in buchstäblich drei Nachrichten senden zu können:

```
Alice-->Bob: syn+data+close
Bob-->Alice: ack+data+close (the browser gets the response now)
Alice-->Bob: ack (so he doesn't resend the payload)
```
Jedenfalls ist hierfür bisher noch nicht viel Code geschrieben worden; die Protokollseite wirkt weitgehend TCP-ähnlich, und die Pakete entsprechen in etwa einer Zusammenführung von human's Vorschlag und dem alten Vorschlag. Wenn jemand Vorschläge oder Ideen hat oder bei der Implementierung helfen möchte, melden Sie sich bitte.

## 4) E-Mail-Diskussion

Es gab einige interessante Diskussionen über E‑Mail innerhalb (und außerhalb) von I2P – postman hat eine Reihe von Ideen online gestellt und sucht nach Vorschlägen. Es gab außerdem diesbezügliche Diskussionen auf #mail.i2p. Vielleicht können wir postman dazu bringen, uns ein Update zu geben?

## 5) ???

Das war's fürs Erste. Schau in ein paar Minuten einfach beim Meeting vorbei und bring deine Kommentare mit :)

=jr
