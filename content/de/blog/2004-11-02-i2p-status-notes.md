---
title: "I2P-Statusnotizen für 2004-11-02"
date: 2004-11-02
author: "jr"
description: "Wöchentliches I2P-Status-Update zu Netzwerkstatus, Speicheroptimierungen im Kern, Sicherheitskorrekturen im Routing der tunnel, Fortschritten bei der Streaming-Bibliothek und Entwicklungen bei E‑Mail/BitTorrent"
categories: ["status"]
---

Hi zusammen, Zeit für das wöchentliche Update

## Stichwortverzeichnis:

1. Net status
2. Core updates
3. Streaming lib
4. mail.i2p progress
5. BT progress
6. ???

## 1) Netzstatus

Im Großen und Ganzen wie zuvor - eine konstante Anzahl von Peers, eepsites(I2P Sites) weitgehend erreichbar und irc stundenlang am Stück. Sie können sich einen Eindruck von der Erreichbarkeit verschiedener eepsites(I2P Sites) auf einigen verschiedenen Seiten verschaffen: - `http://gott.i2p/sites.html` - `http://www.baffled.i2p/links.html` - `http://thetower.i2p/pings.txt`

## 2) Kern-Updates

Wer im Channel (IRC-Kanal) abhängt (oder die CVS-Logs liest), hat gesehen, dass viel los war, obwohl die letzte Veröffentlichung schon eine Weile zurückliegt. Eine vollständige Liste der Änderungen seit dem 0.4.1.3-Release ist online verfügbar, aber es gibt zwei wesentliche Änderungen, eine gute und eine schlechte:

Das Gute daran ist, dass wir die durch das irrwitzige Anlegen aller möglichen temporären Objekte verursachte Speicherbelastung drastisch reduziert haben. Irgendwann hatte ich es satt, dem GC (Garbage Collector) dabei zuzusehen, wie er beim Debuggen der neuen Streaming-Bibliothek durchdrehte, also sind nach ein paar Tagen Profiling, Feintuning und Optimierung die hässlichsten Stellen bereinigt.

Der problematische ist ein Bugfix für die Art und Weise, wie einige tunnel-geroutete Nachrichten gehandhabt werden - es gab einige Situationen, in denen eine Nachricht direkt an den anvisierten router gesendet wurde, statt vor der Zustellung durch einen tunnel geroutet zu werden, was von einem Angreifer, der ein wenig programmieren kann, ausgenutzt werden könnte. Im Zweifel routen wir jetzt ordnungsgemäß durch einen tunnel.

Das mag gut klingen, aber der 'schlechte' Teil ist, dass es aufgrund der zusätzlichen Hops zu einer erhöhten Latenz kommt, obwohl es sich um Hops handelt, die ohnehin verwendet werden mussten.

Es laufen im Kern auch noch weitere Debugging-Aktivitäten, daher gab es noch kein offizielles Release - CVS HEAD ist 0.4.1.3-8. In den nächsten Tagen werden wir wahrscheinlich ein 0.4.1.4-Release herausbringen, nur um das alles zu bereinigen. Die neue Streaming-Bibliothek wird es natürlich nicht enthalten.

## 3) Streaming-Bibliothek

Was die Streaming-Bibliothek betrifft, hat es hier große Fortschritte gegeben, und der direkte Vergleich der alten und der neuen Bibliothek macht einen guten Eindruck. Es bleibt jedoch noch Arbeit zu tun, und wie ich beim letzten Mal gesagt habe, werden wir es nicht überhastet herausbringen. Das bedeutet, dass sich die Roadmap verschoben hat, voraussichtlich um etwa 2–3 Wochen. Weitere Details, sobald sie verfügbar sind.

## 4) mail.i2p Fortschritt

Diese Woche gibt es viel Neues - funktionierende eingehende und ausgehende Proxys! Weitere Informationen finden Sie unter www.postman.i2p.

## 5) BT-Fortschritt

In letzter Zeit gab es rege Aktivitäten rund um das Portieren eines BitTorrent-Clients sowie das Aktualisieren einiger Tracker-Einstellungen. Vielleicht können wir während des Treffens von den Beteiligten ein Update erhalten.

## 6) ???

Das war's von mir. Sorry für die Verspätung, ich habe die ganze Geschichte mit der Zeitumstellung vergessen. Wie dem auch sei, wir sehen uns in Kürze.

=jr
