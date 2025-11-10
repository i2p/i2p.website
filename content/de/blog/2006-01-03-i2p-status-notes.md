---
title: "I2P-Statusnotizen vom 2006-01-03"
date: 2006-01-03
author: "jr"
description: "Neujahrs-Update zur Stabilität der Version 0.6.1.8, Ergebnissen der Lasttests und Peer‑Profiling zur Durchsatzoptimierung sowie einem umfassenden Rückblick auf 2005 mit Vorschau auf die Roadmap 2006"
categories: ["status"]
---

Hallo zusammen, frohes neues Jahr! Lasst uns nach einer Woche Pause wieder in unsere wöchentlichen Statusnotizen einsteigen -

* Index

1) Netzwerkstatus und 0.6.1.8 2) Ergebnisse von Lasttests und Peer-Profiling 3) 2005-Rückblick / 2006-Vorschau / ???

* 1) Net status and 0.6.1.8

In der vergangenen Woche haben wir 0.6.1.8 veröffentlicht, und Berichte aus der Praxis besagen, dass die Änderungen von zzz spürbar geholfen haben und das Netz insgesamt recht stabil wirkt – selbst bei dem in letzter Zeit deutlich gestiegenen Netzwerkverkehr (laut stats.i2p hat sich der Durchschnitt im letzten Monat offenbar verdoppelt). I2PSnark scheint ebenfalls ziemlich gut zu funktionieren – auch wenn wir auf ein paar Stolpersteine gestoßen sind, haben wir die meisten davon in nachfolgenden Builds aufgespürt und behoben. Zum neuen Blog-Interface von Syndie gab es bislang nicht viel Feedback, aber der Syndie-Traffic ist etwas angestiegen (teilweise, weil protocol dusts rss/atom-Importer entdeckt hat :).

* 2) Load testing results and peer profiling

In den letzten Wochen habe ich versucht, unsere Durchsatz-Engstelle genau einzugrenzen. Die verschiedenen Softwarekomponenten sind alle in der Lage, Daten mit deutlich höheren Raten zu übertragen, als wir sie typischerweise bei Ende-zu-Ende-Kommunikation über I2P sehen, daher habe ich im Live-Netz mit eigenem Code Benchmark-Tests zum Stresstest durchgeführt. Die erste Testreihe, beim Aufbau eingehender 1-Hop tunnel durch alle router im Netzwerk und dem so schnellen wie möglichen (ASAP) Übertragen von Daten durch diesen tunnel, zeigte recht vielversprechende Ergebnisse: router verarbeiteten Raten, die ungefähr in dem Bereich lagen, den man von ihnen erwarten würde (z. B. die meisten nur mit einem Durchschnitt über die Betriebsdauer von 4-16KBps, andere jedoch mit 20-120KBps durch einen einzelnen tunnel). Dieser Test war eine gute Ausgangsbasis für weitere Untersuchungen und zeigte, dass die tunnel-Verarbeitung selbst in der Lage ist, weit mehr zu übertragen, als wir üblicherweise sehen.

Versuche, diese Ergebnisse durch live tunnels zu reproduzieren, waren nicht so erfolgreich. Oder vielleicht könnte man sagen, sie waren erfolgreicher, denn sie zeigten einen Durchsatz ähnlich dem, was wir derzeit sehen, was bedeutete, dass wir auf der richtigen Spur waren. Zurück zu den 1hop-Testergebnissen änderte ich den Code so, dass er Peers auswählt, die ich manuell als schnell identifiziert hatte, und ließ die Lasttests mit dieser „geschummelten“ Peer-Auswahl erneut durch live tunnels laufen, und auch wenn es nicht bis an die 120KBps-Marke herankam, zeigte sich doch eine spürbare Verbesserung.

Leider bringt es sowohl für die Anonymität als auch, nun ja, die Benutzerfreundlichkeit erhebliche Probleme mit sich, Menschen zu bitten, ihre Peers manuell auszuwählen, aber bewaffnet mit den Lasttest-Daten scheint es einen Ausweg zu geben. In den letzten Tagen habe ich eine neue Methode getestet, Peers nach ihrer Geschwindigkeit zu profilieren – im Wesentlichen ihren maximal nachhaltig aufrechterhaltenen Durchsatz zu überwachen, statt ihre jüngste Latenz zu betrachten. Naive Implementierungen waren ziemlich erfolgreich, und auch wenn sie nicht genau die Peers ausgewählt haben, die ich manuell gewählt hätte, haben sie einen ziemlich guten Job gemacht. Es gibt allerdings noch ein paar Kinderkrankheiten, zum Beispiel sicherzustellen, dass wir exploratory tunnels in die schnelle Ebene hochstufen können, aber dazu führe ich derzeit einige Experimente durch.

Insgesamt denke ich, dass wir uns dem Ende dieses Durchsatz-Exkurses nähern, da wir gegen den engsten Flaschenhals drücken und ihn aufweiten. Ich bin sicher, dass wir bald auf den nächsten stoßen werden, und das wird uns ganz bestimmt keine normalen Internetgeschwindigkeiten bringen, aber es sollte helfen.

* 3) 2005 review / 2006 preview / ???

Zu sagen, 2005 habe viel Neuland erschlossen, ist fast untertrieben – wir haben I2P auf zahlreiche Weisen in den 25 Veröffentlichungen des letzten Jahres verbessert, das Netzwerk auf das Fünffache vergrößert, mehrere neue Client-Anwendungen bereitgestellt (Syndie, I2Phex, I2PSnark, I2PRufus), sind zum neuen irc2p-IRC-Netzwerk von postman und cervantes migriert und haben einige nützliche eepsites(I2P Sites) aufblühen sehen (wie zzz's stats.i2p, orion's orion.i2p und tino's Proxy- und Monitoring-Dienste, um nur einige zu nennen). Die Community ist ebenfalls ein Stück gereift, nicht zuletzt dank der Unterstützungsarbeit von Complication und anderen im Forum und in den Kanälen, und Qualität sowie Vielfalt der Fehlerberichte aus allen Bereichen haben sich deutlich verbessert. Die anhaltende finanzielle Unterstützung aus der Community war beeindruckend, und auch wenn sie noch nicht das Niveau erreicht, das für eine vollständig nachhaltige Entwicklung erforderlich wäre, haben wir doch einen Puffer, der mich über den Winter bringt.

An alle, die im vergangenen Jahr mitgewirkt haben, sei es technisch, sozial oder finanziell: Vielen Dank für Ihre Hilfe!

2006 wird ein wichtiges Jahr für uns, mit 0.6.2, das diesen Winter erscheint, einer für den Frühling oder Sommer geplanten 1.0-Veröffentlichung und 2.0 im Herbst, wenn nicht früher. Dies ist das Jahr, in dem wir sehen werden, was wir leisten können, und die Arbeit in der Anwendungsschicht wird noch wichtiger sein als zuvor. Wenn du also ein paar Ideen hast, ist jetzt der richtige Zeitpunkt, loszulegen :)

Jedenfalls steht unser wöchentliches Status-Meeting in wenigen Minuten an, also falls du etwas weiter besprechen möchtest, komm einfach bei #i2p an den üblichen Orten [1] vorbei und sag Hallo!

=jr [1] http://forum.i2p.net/viewtopic.php?t=952
