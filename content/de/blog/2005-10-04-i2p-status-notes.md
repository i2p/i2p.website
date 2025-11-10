---
title: "I2P Statusnotizen für 2005-10-04"
date: 2005-10-04
author: "jr"
description: "Wöchentliches Update zum Erfolg des Releases 0.6.1.1 mit 3-400 Peers, zu den Bemühungen zur Zusammenführung des i2phex-Forks und zu Fortschritten bei der Syndie-Automatisierung mit Petnames (vom Nutzer vergebene eindeutige Namen) und zeitgesteuerten Abrufen"
categories: ["status"]
---

Hallo zusammen, es ist Zeit für unsere wöchentlichen Statusnotizen (Jubel einfügen)

* Index

1) 0.6.1.1 2) i2phex 3) syndie 4) ???

* 1) 0.6.1.1

As announced on the usual places, 0.6.1.1 came out the other day, and so far, reports have been positive. The network has grown to a steady 3-400 known peers, and performance has been pretty good, though cpu usage has increased a bit. This is probably be due to a long standing bugs which incorrectly allows invalid IP addresses to get accepted, which in turn causes a higher than necessary churn. There have been fixes to this and other things in CVS builds since 0.6.1.1, so we'll probably have a 0.6.1.2 later this week.

* 2) i2phex

Während einige möglicherweise die Diskussion in verschiedenen Foren über i2phex und den Fork von legion bemerkt haben, gab es weiteren Austausch zwischen mir und legion, und wir arbeiten daran, die beiden wieder zusammenzuführen. Weitere Informationen dazu, sobald sie verfügbar sind.

Außerdem arbeitet redzara eifrig daran, i2phex mit dem aktuellen phex-Release zusammenzuführen, und striker hat einige weitere Verbesserungen erarbeitet, sodass in Kürze spannende Neuerungen zu erwarten sind.

* 3) syndie

Ragnarok hat in den letzten Tagen fleißig an syndie gearbeitet, indem er syndies Pet-Name-Datenbank mit der Pet-Name-Datenbank des router integriert und die Syndizierung mit zeitgesteuerten Abrufen aus ausgewählten entfernten Archiven automatisiert hat. Der Automatisierungsteil ist abgeschlossen, und obwohl noch etwas Arbeit an der UI (Benutzeroberfläche) übrig ist, ist das Ganze schon in ziemlich gutem Zustand!

* 4) ???

Zurzeit passiert auch sonst eine Menge, unter anderem Arbeiten an den neuen technischen Einführungsdokumenten, an der IRC-Migration und an der Überarbeitung der Website. Wenn jemand etwas ansprechen möchte, kommt in ein paar Minuten einfach beim Meeting vorbei und sagt Hallo!

=jr
