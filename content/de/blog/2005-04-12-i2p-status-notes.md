---
title: "I2P-Statusnotizen für den 12.04.2005"
date: 2005-04-12
author: "jr"
description: "Wöchentliches Update zu netDb-Fehlerbehebungen in 0.5.0.6, Fortschritten beim SSU-UDP-Transport, Ergebnissen des bayesschen Peer-Profilings und der Q-Entwicklung"
categories: ["status"]
---

Hallo zusammen, wieder Zeit für ein Update

* Index

1) Netzstatus 2) SSU-Status 3) Bayessches Peer-Profiling 4) Q-Status 5) ???

* 1) Net status

Das Release 0.5.0.6 der letzten Woche scheint die netDb-Probleme, die wir beobachtet haben, behoben zu haben (juhu). Websites und Dienste sind deutlich zuverlässiger als unter 0.5.0.5, allerdings gab es einige Berichte über Probleme, bei denen eine Website oder ein Dienst nach einigen Tagen Betriebszeit nicht mehr erreichbar wurde.

* 2) SSU status

Es hat große Fortschritte am 0.6-UDP-Code gegeben; der erste Schwung Commits wurde bereits in CVS eingecheckt. Es ist noch nichts, was man tatsächlich verwenden könnte, aber die Grundlagen sind gelegt. Die Sitzungsaushandlung funktioniert gut und die teilzuverlässige Nachrichtenübermittlung verhält sich wie erwartet. Es gibt jedoch noch viel zu tun, Testfälle zu schreiben und Sonderfälle zu debuggen, aber es ist ein Fortschritt.

Wenn alles gut läuft, könnten wir nächste Woche mit einigen Alpha-Tests beginnen, zunächst nur für Personen, die ihre Firewalls/NATs explizit konfigurieren können. Ich möchte erst den allgemeinen Betrieb ausarbeiten, bevor ich den Relay-Handler hinzufüge, die netDb für schnellere routerInfo-Ablaufzeiten abstimme und Relays zum Veröffentlichen auswähle. Außerdem werde ich die Gelegenheit nutzen, eine ganze Reihe von Tests durchzuführen, da mehrere kritische Faktoren beim Queueing angegangen werden.

* 3) Bayesian peer profiling

bla hat fleißig daran gearbeitet, unsere Entscheidungskriterien dafür zu überarbeiten, über welche Peers (Gegenstellen) wir tunnel führen, und obwohl bla nicht am Treffen teilnehmen konnte, gibt es einige interessante Daten zu berichten:

<+bla> Ich habe direkte Knotengeschwindigkeiten gemessen: Ich habe        etwa 150 Knoten profiliert, indem ich OB tunnels mit Länge 0, IB tunnels mit        Länge 1 verwendet habe, batching-interval = 0ms
<+bla> Außerdem habe ich gerade eine _sehr_ grundlegende und        _vorläufige_ Geschwindigkeitsabschätzung mit naiver Bayes-Klassifikation        durchgeführt
<+bla> Letzteres wurde unter Verwendung der Standard-Längen der expl. tunnels durchgeführt
<+bla> Die Schnittmenge zwischen der Menge der Knoten, für die ich        „Ground Truth“ (Referenzwerte) habe, und der Menge der Knoten in den aktuellen        Messungen, beträgt 117 Knoten
<+bla> Die Ergebnisse sind nicht _so_ schlecht, aber auch nicht besonders beeindruckend
<+bla> Siehe http://theland.i2p/estspeed.png
<+bla> Die grundlegende Trennung sehr langsam/schnell ist ganz okay, aber die        feinere Unterscheidung unter den schnelleren Peers könnte deutlich besser sein
<+jrandom2p> hmm, wie wurden die tatsächlichen Werte berechnet - ist das              volles RTT oder RTT/Länge ?
<+bla> Mit den normalen expl. tunnels ist es so gut wie unmöglich,        Batching-Verzögerungen zu verhindern.
<+bla> Die tatsächlichen Werte sind die ground-truth-Werte: jene, die        mit OB=0 und IB=1 gewonnen wurden
<+bla> (und variance=0, und keine Batching-Verzögerung)
<+jrandom2p> die Ergebnisse sehen von hier aus allerdings ziemlich gut aus
<+bla> Die geschätzten Zeiten sind diejenigen, die mittels Bayesscher        Inferenz aus _tatsächlichen_ expl. tunnels mit Länge 2 +/- 1 gewonnen wurden
<+bla> Das stammt aus 3000 RTTs, aufgezeichnet über einen Zeitraum von        etwa 3 Stunden (das ist lang)
<+bla> Es setzt (vorerst) voraus, dass die Geschwindigkeit der Peers statisch ist.        Eine Gewichtung habe ich noch nicht implementiert
<+jrandom2p> klingt verdammt gut.  gute Arbeit, bla
<+jrandom2p> hmm, die Schätzung sollte also 1/4 des tatsächlichen Werts entsprechen
<+bla> jrandom: Nein: Alle gemessenen RTTs (mit den normalen expl.        tunnels) werden auf die Anzahl der Hops im        Round-Trip korrigiert
<+jrandom2p> ah ok
<+bla> Erst danach wird der Bayes-Klassifikator trainiert
<+bla> Vorerst teile ich die gemessenen Zeiten-pro-Hop in 10 Klassen ein:        50, 100, ..., 450 ms, und eine zusätzliche Klasse >500 ms
<+bla> Z. B. könnten kleine Verzögerungen pro Hop mit einem größeren        Faktor gewichtet werden, ebenso komplette Ausfälle (>60000 ms).
<+bla> Trotzdem.... 65% der geschätzten Zeiten liegen innerhalb von 0,5        Standardabweichungen von der tatsächlichen Knotenzeit
<+bla> Allerdings muss das neu gemacht werden, da die Standardabweichung        stark von den >60000 ms-Ausfällen beeinflusst wird

Nach weiterer Diskussion zeigte bla einen Vergleich gegenüber dem bestehenden Geschwindigkeitsrechner, veröffentlicht @ http://theland.i2p/oldspeed.png Spiegel dieser PNGs sind unter http://dev.i2p.net/~jrandom/estspeed.png und http://dev.i2p.net/~jrandom/oldspeed.png verfügbar

(zur Terminologie, IB=eingehende tunnel-Hops, OB=ausgehende tunnel-Hops, und nach einigen Klarstellungen wurden die "Ground Truth"-Messungen mit 1 Hop ausgehend und 0 Hops eingehend ermittelt, nicht umgekehrt)

* 4) Q status

Aum hat ebenfalls große Fortschritte bei Q gemacht und zuletzt an einer webbasierten Client-Oberfläche gearbeitet. Der nächste Q-Build wird nicht abwärtskompatibel sein, da er eine ganze Reihe neuer Funktionen enthält, aber ich bin sicher, dass wir von Aum mehr erfahren werden, sobald es mehr zu berichten gibt :)

* 5) ???

Das war’s fürs Erste (ich muss das hier noch vor dem Meeting zu Ende bringen). Oh, nur am Rande: Es sieht so aus, als würde ich früher umziehen als geplant, daher könnten sich einige der Termine in der Roadmap verschieben, während ich unterwegs bin, wohin auch immer ich am Ende lande. Wie auch immer, schaut in ein paar Minuten im Channel vorbei, um uns mit neuen Ideen zu nerven!

=jr
