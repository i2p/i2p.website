---
title: "I2P-Statusnotizen für 2006-02-21"
date: 2006-02-21
author: "jr"
description: "Netzwerkprobleme mit dem Release 0.6.1.10, schnelles Folge-Release 0.6.1.11, und IE-Sicherheitsbedenken"
categories: ["status"]
---

Hi zusammen, es ist wieder Dienstag

* Index

1) Netzstatus 2) ???

* 1) Net status

Das Netzwerk hat mit der Veröffentlichung 0.6.1.10 eine etwas raue Phase durchgemacht, teilweise aufgrund der fehlenden Abwärtskompatibilität, aber auch wegen unerwarteter Fehler.  Weder Zuverlässigkeit noch Betriebszeit (Uptime) unter 0.6.1.10 waren ausreichend, sodass es in den letzten 5 Tagen eine ganze Reihe von Patches gab, die im neuen Release 0.6.1.11 gipfelte - http://dev.i2p.net/pipermail/i2p/2006-February/001263.html

Die meisten der in 0.6.1.10 gefundenen Fehler sind bereits seit dem 0.6-Release im vergangenen September vorhanden, waren jedoch nicht ohne Weiteres erkennbar, solange es alternative Transportverfahren (TCP) gab, auf die man ausweichen konnte. Mein lokales Testnetzwerk simuliert Paketverluste, deckte jedoch router churn (Fluktuation) und andere persistente Netzwerkfehler nicht wirklich ab. Auch das _PRE test network umfasste eine selbst ausgewählte Gruppe recht zuverlässiger Peers, sodass wesentliche Szenarien vor dem vollständigen Release nicht vollständig untersucht wurden. Das ist offensichtlich ein Problem, und beim nächsten Mal werden wir darauf achten, eine breitere Auswahl an Szenarien abzudecken.

* 2) ???

There's a bunch of things going on at the moment, but the new 0.6.1.11 release jumped to the head of the queue.  The network will continue to be a bit bumpy until a large number of people are up to date, after which work will continue moving forward.  One thing worth mentioning is that cervantes is working through some sort of IE-related security domain exploit, and while I'm not sure if he is ready to explain the details, preliminary results suggest its viable, so the anonymity-minded out there should avoid IE in the meantime (but you knew that anyway ;).  Perhaps cervantes can give us a summary in the meeting?

Jedenfalls, das ist alles, was ich im Moment zu erwähnen habe - komm in ein paar Minuten kurz beim Meeting vorbei, um Hallo zu sagen!

=jr
