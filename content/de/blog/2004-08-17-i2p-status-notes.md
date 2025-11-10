---
title: "I2P Statusnotizen vom 17.08.2004"
date: 2004-08-17
author: "jr"
description: "Wöchentliches I2P-Status-Update zu Netzwerkleistungsproblemen, DoS-Angriffen und der Entwicklung der Stasher DHT"
categories: ["status"]
---

Hallo zusammen, Zeit für ein Update

## Stichwortverzeichnis:

1. Network status and 0.3.4.3
2. Stasher
3. ???

## 1) Netzwerkstatus und 0.3.4.3

Obwohl das Netzwerk in der letzten Woche funktionsfähig war, gab es zeitweise eine Menge Schwierigkeiten, was zu einem drastischen Rückgang der Zuverlässigkeit führte. Die Version 0.3.4.2 hat erheblich dabei geholfen, einen DoS zu beheben, der durch einige Inkompatibilitäts- und Zeitsynchronisationsprobleme verursacht wurde – siehe das Diagramm der Netzwerkdatenbank-Anfragen, das den DoS zeigt (Spitzen außerhalb der Skala), der durch die Einführung von 0.3.4.2 gestoppt wurde. Unglücklicherweise brachte diese Version wiederum ihre eigenen Probleme mit sich, sodass eine erhebliche Zahl von Nachrichten erneut übertragen werden musste, wie im Bandbreiten-Diagramm zu sehen ist. Die erhöhte Last dort war außerdem auf einen tatsächlichen Anstieg der Nutzeraktivität zurückzuführen, also ist es nicht /so/ verrückt ;) Aber dennoch war es ein Problem.

In den letzten Tagen war ich ziemlich egoistisch. Wir haben eine Reihe von Bugfixes getestet und auf ein paar routers ausgerollt, aber ich habe sie noch nicht veröffentlicht, da ich selten die Wechselwirkungen von Inkompatibilitäten in der Software testen kann, wenn ich meine Simulationen laufen lasse. Also wart ihr einem äußerst beschissenen Netzwerkbetrieb ausgesetzt, während ich an Dingen herumgeschraubt habe, um Wege zu finden, wie routers gut funktionieren können, wenn viele routers grottig sind. Wir machen an dieser Front Fortschritte – Profiling und das Meiden von Peers, die die netDb (Network Database) ausnutzen, eine effizientere Verwaltung der Anfragewarteschlangen der netDb und die stärkere Durchsetzung der tunnel-Diversifizierung.

So weit sind wir noch nicht, aber ich bin zuversichtlich. Derzeit werden Tests im Live-Netz durchgeführt, und wenn alles bereit ist, wird es ein 0.3.4.3-Release geben, das die Ergebnisse ausrollt.

## 2) Stasher

Aum hat an seiner DHT (verteilte Hashtabelle) ziemlich beeindruckende Arbeit geleistet, und obwohl sie derzeit einige erhebliche Einschränkungen hat, wirkt sie vielversprechend. Sie ist definitiv noch nicht für den allgemeinen Einsatz bereit, aber wenn du Lust hast, ihn beim Testen (oder Programmieren :) zu unterstützen, schau dir die Website an und starte einen Knoten.

## 3) ???

Das war's erst mal. Da das Meeting schon vor einer Minute hätte anfangen sollen, sollte ich das hier wohl beenden. Wir sehen uns in #i2p!

=jr
