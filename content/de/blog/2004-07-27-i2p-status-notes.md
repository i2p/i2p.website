---
title: "I2P-Statusnotizen für 2004-07-27"
date: 2004-07-27
author: "jr"
description: "Wöchentliches I2P-Status-Update zu Leistungsproblemen der Version 0.3.3 und bevorstehenden Optimierungen"
categories: ["status"]
---

Hallo zusammen, Zeit für die wöchentliche Meckerrunde

## Inhaltsverzeichnis:

1. 0.3.3 & current updates
2. NativeBigInteger
3. ???

## 1) 0.3.3

Wir haben die Version 0.3.3 am vergangenen Freitag veröffentlicht, und nach ein oder zwei ziemlich holprigen Tagen scheint es ganz gut zu laufen. Nicht so gut wie 0.3.2.3, aber ich konnte in der Regel für 2–7 Stunden am Stück auf irc.duck.i2p verbunden bleiben. Da jedoch viele Leute Probleme hatten, habe ich den Logger gestartet und im Detail beobachtet, was los war. Kurz gesagt haben wir einfach mehr Bandbreite genutzt, als nötig, was zu Überlastung und Ausfällen der tunnel führte (aufgrund von Zeitüberschreitungen bei Testnachrichten usw.).

Ich habe die letzten paar Tage wieder im Simulator verbracht, eine Reihe von Heartbeat-Signalen durch ein Netzwerk laufen lassen, um zu sehen, was wir verbessern können, und darauf basierend steht uns eine ganze Reihe an Updates bevor:

### netDb update to operate more efficiently

Die bestehenden netDb-Abfrage-Nachrichten sind bis zu 10+KB groß, und obwohl erfolgreiche Antworten häufig sind, können fehlgeschlagene Antworten bis zu 30+KB groß sein (da beide vollständige RouterInfo-Strukturen enthalten). Die neue netDb ersetzt diese vollständigen RouterInfo-Strukturen durch den router-Hash - wodurch 10KB- und 30KB-Nachrichten zu ~100-Byte-Nachrichten werden.

### throw out the SourceRouteBlock and SourceRouteReplyMessage

Diese Strukturen waren ein Überbleibsel einer alten Idee, tragen jedoch nichts zur Anonymität oder Sicherheit des Systems bei. Indem wir sie zugunsten eines einfacheren Satzes von Antwortdatenpunkten verwerfen, reduzieren wir die Größe der Verwaltungsnachrichten für tunnel drastisch und halbieren die Zeit für die garlic encryption (Knoblauch-Verschlüsselung).

### netDb-Update für effizienteren Betrieb

Der Code war während der tunnel-Erstellung etwas 'geschwätzig', daher wurden die unnötigen Meldungen entfernt.

### Verwerfen Sie den SourceRouteBlock und die SourceRouteReplyMessage

Ein Teil des Krypto-Codes für das garlic routing (I2P-Routing-Verfahren) verwendete festes Padding, basierend auf einigen garlic routing-Techniken, die wir nicht verwenden (als ich es im September und Oktober schrieb, dachte ich, wir würden multi-hop garlic routing statt tunnels einsetzen).

Ich arbeite außerdem daran herauszufinden, ob ich das umfassende Update des tunnel-Routings umsetzen kann, um die per-Hop tunnel-IDs hinzuzufügen.

Wie aus der Roadmap ersichtlich ist, umfasst dies einen Großteil des 0.4.1-Releases, aber da die Änderung an der netDb den Verlust der Abwärtskompatibilität zur Folge hatte, können wir gleich eine ganze Reihe weiterer nicht abwärtskompatibler Änderungen auf einmal erledigen.

Ich lasse immer noch Tests im Simulator laufen und muss sehen, ob ich die Sache mit der per-Hop tunnel id fertigbekomme, aber ich hoffe, in ein oder zwei Tagen ein neues Patch-Release herauszubringen. Es wird nicht abwärtskompatibel sein, daher wird das Upgrade holprig, aber es sollte sich lohnen.

## 2) NativeBigInteger

Iakin hat für das Freenet-Team einige Aktualisierungen am NativeBigInteger-Code vorgenommen, wobei er zwar Dinge optimiert, die wir nicht verwenden, aber auch einen CPU-Erkennungscode erstellt, den wir nutzen können, um automatisch die richtige native Bibliothek auszuwählen. Das bedeutet, dass wir jbigi mit der Standardinstallation als einzelne Bibliothek ausliefern können und dabei automatisch die passende ausgewählt wird, ohne den Benutzer nach irgendetwas fragen zu müssen. Er hat außerdem zugestimmt, seine Änderungen und den neuen CPU-Erkennungscode freizugeben, damit wir sie in unseren Quellcode einbinden können (juhu, Iakin!). Ich bin mir nicht sicher, wann das ausgerollt wird, aber ich werde Bescheid geben, sobald es so weit ist, da diejenigen mit vorhandenen jbigi-Bibliotheken voraussichtlich eine neue benötigen werden.

## 3) ???

Nun, die letzte Woche war vor allem von intensivem Coden geprägt, daher gibt es nicht allzu viele Updates. Hat sonst noch jemand etwas anzusprechen? Wenn ja, schaut heute Abend um 21 Uhr GMT beim Treffen in #i2p vorbei.

=jr
