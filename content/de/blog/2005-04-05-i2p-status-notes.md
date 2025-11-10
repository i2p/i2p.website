---
title: "I2P-Statusnotizen vom 2005-04-05"
date: 2005-04-05
author: "jr"
description: "Wöchentliches Update zu Problemen beim Release 0.5.0.5, zur Forschung zur bayesschen Peer-Profilierung und zu den Fortschritten der Q-Anwendung"
categories: ["status"]
---

Hallo zusammen, es ist Zeit für das wöchentliche Update

* Index

1) 0.5.0.5 2) Bayes'sches Peer-Profiling 3) Q 4) ???

* 1) 0.5.0.5

Die Veröffentlichung 0.5.0.5 der vergangenen Woche hatte ihre Höhen und Tiefen - die größere Änderung zur Abwehr einiger Angriffe auf die netDb scheint wie erwartet zu funktionieren, hat jedoch einige lange übersehene Fehler im Betrieb der netDb aufgedeckt. Dies hat zu erheblichen Zuverlässigkeitsproblemen geführt, insbesondere für eepsites(I2P Sites). Die Fehler wurden jedoch in CVS identifiziert und behoben, und diese Korrekturen, zusammen mit einigen weiteren, werden innerhalb des nächsten Tages als 0.5.0.6-Release bereitgestellt.

* 2) Bayesian peer profiling

bla hat einige Untersuchungen dazu durchgeführt, wie wir unser Peer-Profiling verbessern können, indem wir auf Basis der gesammelten Statistiken [1] eine einfache Bayes-Filterung einsetzen. Das sieht ziemlich vielversprechend aus, allerdings bin ich mir derzeit nicht sicher, wie der aktuelle Stand ist – vielleicht können wir während des Meetings ein Update von bla erhalten?

[1] http://forum.i2p.net/viewtopic.php?t=598     http://theland.i2p/nodemon.html

* 3) Q

Bei der Q-App von aum geht viel voran, sowohl bei der Kernfunktionalität als auch bei den von einigen Leuten entwickelten xmlrpc-Frontends. Gerüchten zufolge könnten wir an diesem Wochenende einen weiteren Q-Build sehen, mit einer ganzen Reihe von Neuerungen, die auf http://aum.i2p/q/ beschrieben sind.

* 4) ???

Ok, ja, sehr kurze Statusnotizen, da ich die Zeitzonen *schon wieder* durcheinandergebracht habe (eigentlich habe ich auch die Tage verwechselt; bis vor ein paar Stunden dachte ich, es sei Montag). Wie auch immer, es passiert eine Menge, die oben nicht erwähnt ist, also schau beim Meeting vorbei und sieh dir an, was so los ist!

=jr
