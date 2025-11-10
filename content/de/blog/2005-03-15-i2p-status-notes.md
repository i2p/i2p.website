---
title: "I2P Statusnotizen für 2005-03-15"
date: 2005-03-15
author: "jr"
description: "Wöchentliche Statusnotizen zur I2P-Entwicklung, die Analysen der Netzwerkleistung, Verbesserungen der Geschwindigkeitsberechnung und die Entwicklung von Feedspace behandeln"
categories: ["status"]
---

Hallo zusammen, es ist Zeit für das wöchentliche Update.

* Index

1) Netzstatus 2) Feedspace 3) ???

* 1) Net status

In der letzten Woche habe ich einen Großteil meiner Zeit damit verbracht, das Verhalten des Netzwerks zu analysieren, Statistiken nachzuverfolgen und zu versuchen, verschiedene Ereignisse im Simulator zu reproduzieren. Während sich ein Teil des merkwürdigen Netzwerkverhaltens auf die rund zwei Dutzend routers zurückführen lässt, die noch ältere Versionen verwenden, ist der entscheidende Faktor, dass unsere Geschwindigkeitsberechnungen uns keine guten Daten liefern – wir sind nicht in der Lage, Peers, die Daten schnell übertragen können, zuverlässig zu identifizieren. In der Vergangenheit war das kein großes Problem, da es einen Bug gab, der dazu führte, dass wir die 8 Peers mit der höchsten Kapazität als den 'fast'-Pool verwendeten, anstatt korrekt aus der Kapazität abgeleitete Ebenen zu bilden. Unsere aktuelle Geschwindigkeitsberechnung leitet sich von einem periodischen Latenztest ab (insbesondere der RTT eines tunnel-Tests), aber das liefert zu wenige Daten, um Vertrauen in den Wert zu haben. Was wir brauchen, ist eine bessere Möglichkeit, mehr Datenpunkte zu sammeln und dennoch zuzulassen, dass 'high capacity'-Peers bei Bedarf in die 'fast'-Ebene aufsteigen.

Um zu überprüfen, dass dies das Hauptproblem ist, mit dem wir es zu tun haben, habe ich ein wenig getrickst und eine Funktion hinzugefügt, um manuell auszuwählen, welche Peers bei der Auswahl eines bestimmten tunnel pool verwendet werden sollen. Mit diesen explizit ausgewählten Peers war ich über zwei Tage auf irc ohne Verbindungsabbruch und hatte eine recht ordentliche Leistung mit einem weiteren Dienst, den ich betreibe. Seit ungefähr zwei Tagen probiere ich einen neuen Geschwindigkeitsrechner aus, der einige neue Statistiken verwendet, und obwohl er die Auswahl verbessert hat, gibt es noch einige Probleme. Ich habe heute Nachmittag ein paar Alternativen durchgearbeitet, aber es bleibt noch Arbeit, um sie im Netz auszuprobieren.

* 2) Feedspace

Frosk hat eine weitere Revision der i2pcontent/fusenet docs veröffentlicht, nur jetzt an neuer Adresse und unter neuem Namen: http://feedspace.i2p/ - siehe entweder orion [1] oder meinen Blog [2] für die Destination (Zieladresse). Das sieht wirklich vielversprechend aus, sowohl aus der Perspektive von "hey, richtig starke Funktionalität" als auch von "hey, das wird I2Ps Anonymität zugutekommen". Frosk und sein Team arbeiten fleißig weiter, aber sie suchen ganz sicher nach Input (und Hilfe). Vielleicht können wir Frosk dazu bringen, uns im Meeting ein Update zu geben?

[1] http://orion.i2p/#feedspace.i2p [2] http://jrandom.dev.i2p/

* 3) ???

Okay, es sieht vielleicht nicht nach viel aus, aber es passiert wirklich eine Menge :) Ich bin sicher, dass ich auch einiges übersehen habe, also schau beim Meeting vorbei und sieh, was los ist.

=jr
