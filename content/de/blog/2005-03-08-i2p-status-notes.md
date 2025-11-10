---
title: "I2P Statusnotizen für 2005-03-08"
date: 2005-03-08
author: "jr"
description: "Wöchentliche Notizen zum Entwicklungsstatus von I2P mit Informationen zu Verbesserungen in der Version 0.5.0.2, einem Schwerpunkt auf der Zuverlässigkeit des Netzwerks und Aktualisierungen der Mail- und BitTorrent-Dienste"
categories: ["status"]
---

Hi zusammen, Zeit für das wöchentliche Update

* Index

1) 0.5.0.2 2) mail.i2p Updates 3) i2p-bt Updates 4) ???

* 1) 0.5.0.2

Neulich haben wir die Version 0.5.0.2 veröffentlicht, und ein guter Teil des Netzwerks hat aktualisiert (juhu!). Es gehen Berichte ein, dass die schlimmsten Übeltäter aus 0.5.0.1 beseitigt wurden, und insgesamt scheint alles gut zu funktionieren. Es gibt zwar noch einige Zuverlässigkeitsprobleme, aber die Streaming Library (Streaming-Bibliothek) hat das bislang gut abgefangen (IRC-Verbindungen, die 12–24+ Stunden halten, scheinen die Norm zu sein). Ich versuche, einige der verbleibenden Probleme aufzuspüren, aber es wäre wirklich, wirklich gut, wenn alle so schnell wie möglich auf den neuesten Stand kommen würden.

Fürs Weiterkommen gilt derzeit: Zuverlässigkeit steht an erster Stelle. Erst wenn eine überwältigende Mehrheit der Nachrichten, die gelingen sollten, auch tatsächlich gelingt, werden wir an der Verbesserung des Durchsatzes arbeiten. Über den Batching-Tunnel-Preprocessor hinaus könnten wir als weitere Dimension untersuchen, mehr Latenzdaten in die Profile einfließen zu lassen. Derzeit verwenden wir nur Test- und tunnel-Management-Nachrichten, um das „Geschwindigkeits“-Ranking jedes Peers zu ermitteln, aber vermutlich sollten wir alle messbaren RTTs (Round-Trip-Zeiten) auch bei anderen Vorgängen erfassen, etwa bei netDb und sogar bei End-to-End-Client-Nachrichten. Andererseits müssen wir sie entsprechend gewichten, da wir bei einer End-to-End-Client-Nachricht die vier Anteile der messbaren RTT (unser outbound, deren inbound, deren outbound, unser inbound) nicht voneinander trennen können. Vielleicht können wir mit ein paar Garlic-Tricks eine Nachricht, die auf einen unserer inbound tunnels adressiert ist, zusammen mit einigen outbound-Nachrichten bündeln, sodass die tunnels der Gegenseite aus der Messschleife herausfallen.

* 2) mail.i2p updates

Okay, ich weiß nicht, welche Updates postman für uns bereithält, aber es wird während des Meetings ein Update geben. Sieh dir die Logs an, um es herauszufinden!

* 3) i2p-bt update

Ich weiß nicht, welche Updates duck & Co. für uns haben, aber ich habe ein bisschen Gemunkel über Fortschritte im Channel gehört. Vielleicht können wir ihm ein Update entlocken.

* 4) ???

Es ist gerade eine ganze Menge los, aber wenn ihr etwas Bestimmtes ansprechen und diskutieren wollt, schaut in ein paar Minuten beim Meeting vorbei. Oh, und nur zur Erinnerung: Wenn ihr noch nicht aktualisiert habt, holt das bitte so schnell wie möglich nach (Aktualisieren ist kinderleicht - eine Datei herunterladen, auf einen Button klicken)

=jr
