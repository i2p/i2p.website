---
title: "I2P-Statusnotizen für 2005-01-11"
date: 2005-01-11
author: "jr"
description: "Wöchentliche Statusnotizen zur I2P-Entwicklung zu Netzwerkstatus, 0.5‑Fortschritt, 0.6‑Status, azneti2p, FreeBSD‑Port und hosts.txt als Web of Trust (Vertrauensnetz)"
categories: ["status"]
---

Hallo zusammen, es ist Zeit für das wöchentliche Update.

* Index

1) Netzstatus 2) 0.5 Fortschritt 3) 0.6 Status 4) azneti2p 5) fbsd 6) hosts.txt als WoT 7) ???

* 1) Net status

Insgesamt läuft das Netz gut, auch wenn wir einige Probleme hatten, weil einer der IRC-Server offline war und mein outproxy (Ausgangsproxy ins offene Internet) herumzickte. Der andere IRC-Server war (und ist) jedoch erreichbar (auch wenn CTCP derzeit nicht deaktiviert ist - siehe [1]), sodass wir unseren Bedarf an IRC stillen konnten :)

[1] http://ugha.i2p/HowTo/IrcAnonymityGuide

* 2) 0.5 progress

Es geht voran, immer weiter! Okay, ich sollte wohl etwas mehr ins Detail gehen. Ich habe endlich die neue tunnel-Routing-Kryptografie implementiert und getestet (yay!), aber in einigen Diskussionen haben wir eine Stelle gefunden, an der es zu einem Anonymitätsleck auf einer Ebene kommen könnte, deshalb wird das überarbeitet (der erste Hop hätte gewusst, dass er der erste Hop ist, was schlecht ist. aber wirklich, wirklich leicht zu beheben). Wie auch immer, ich hoffe, die Dokumentation und den Code dazu bald zu aktualisieren und zu veröffentlichen und die Dokumentation zum Rest des 0.5 tunnel-Betriebs / Pooling / usw. später zu veröffentlichen. Mehr Neuigkeiten, wenn es mehr Neuigkeiten gibt.

* 3) 0.6 status

(Was!?)

Mule hat mit Untersuchungen zum UDP-Transport begonnen, und wir schöpfen aus zabs Erfahrungen mit LimeWires UDP-Code. Das ist alles sehr vielversprechend, aber es gibt noch viel zu tun (und auf der Roadmap [2] liegt das noch mehrere Monate in der Zukunft). Hast du Ideen oder Vorschläge? Mach mit und hilf, die Arbeit auf das zu fokussieren, was getan werden muss!

[2] http://www.i2p.net/roadmap#0.6

* 4) azneti2p

Ich hab mir fast in die Hose gemacht, als ich die Info bekommen habe, aber es sieht so aus, als hätten die Leute bei azureus ein I2P-Plugin geschrieben, das sowohl anonyme Tracker-Nutzung als auch anonyme Datenkommunikation ermöglicht! Mehrere Torrents funktionieren auch innerhalb eines einzigen I2P destination (I2P‑Zieladresse), und es verwendet die I2PSocket direkt, was eine enge Integration mit der streaming lib (Streaming‑Bibliothek) ermöglicht. Das azneti2p-Plugin befindet sich mit dieser 0.1-Version noch in einem frühen Stadium, und es sind viele Optimierungen und Verbesserungen der Benutzerfreundlichkeit in der Pipeline, aber wenn du Lust hast, dir die Hände schmutzig zu machen, schau bei i2p-bt in den I2P-IRC-Netzwerken vorbei und mach mit :)

Für Experimentierfreudige: Laden Sie die neueste Version von Azureus [3] herunter, sehen Sie sich deren I2P-Anleitung [4] an und schnappen Sie sich das Plugin [5].

[3] http://azureus.sourceforge.net/index_CVS.php [4] http://azureus.sourceforge.net/doc/AnonBT/i2p/I2P_howto.htm [5] http://azureus.sourceforge.net/plugin_details.php?plugin=azneti2p

duck hat außerordentliche Anstrengungen unternommen, um die Kompatibilität mit i2p-bt aufrechtzuerhalten, und in #i2p-bt wird gerade fieberhaft gehackt, während ich dies schreibe, also haltet die Augen nach einer neuen i2p-bt-Veröffentlichung offen, die sehr bald erscheinen dürfte.

* 5) fbsd

Dank der Arbeit von lioux gibt es jetzt einen FreeBSD-Ports-Eintrag für i2p [6]. Auch wenn wir nicht unbedingt viele distributionsspezifische Installationen anstreben, verspricht er, ihn aktuell zu halten, sofern wir neue Releases mit ausreichendem Vorlauf ankündigen. Das dürfte für fbsd-current-Nutzer hilfreich sein – danke, lioux!

[6] http://www.freshports.org/net/i2p/

* 6) hosts.txt as WoT

Da die Version 0.4.2.6 nun Ragnaroks Adressbuch mitliefert, liegt der Vorgang, Ihre hosts.txt mit neuen Einträgen aktuell zu halten, unter der Kontrolle jedes Nutzers. Nicht nur das: Sie können die Adressbuch-Abonnements auch als eine einfache Variante eines Web-of-Trust (Netz des Vertrauens) betrachten – Sie importieren neue Einträge von einer Website, der Sie vertrauen, die Ihnen neue Destinations (Zieladressen) vorstellt (standardmäßig dev.i2p und duck.i2p).

Mit dieser Möglichkeit geht eine völlig neue Dimension einher – nämlich die Möglichkeit für Nutzer, auszuwählen, welche Seiten sie in ihrer hosts.txt eintragen und welche nicht. Zwar hat auch der offene Wildwuchs, der in der Vergangenheit stattgefunden hat, seinen Platz, doch jetzt, da das Namenssystem nicht nur theoretisch, sondern in der Praxis vollständig verteilt ist, müssen Nutzer eigene Richtlinien dafür festlegen, wie sie fremde Destinations (I2P‑Adressen) veröffentlichen.

Der wichtige Punkt hinter den Kulissen ist hier, dass dies eine Lerngelegenheit für die I2P-Gemeinschaft ist. Zuvor versuchten sowohl gott als auch ich, das Namensproblem voranzubringen, indem wir gotts Site unter jrandom.i2p veröffentlichten (er hat diese Site zuerst beantragt - ich nicht, und ich habe keinerlei Kontrolle über die Inhalte dieser URL). Jetzt können wir damit beginnen zu erkunden, wie wir mit Sites umgehen, die nicht in der http://dev.i2p.net/i2p/hosts.txt oder auf forum.i2p aufgeführt sind. Dass sie an diesen Stellen nicht veröffentlicht sind, hindert eine Site in keiner Weise am Betrieb - Ihre hosts.txt ist lediglich Ihr lokales Adressbuch.

Wie dem auch sei, genug Gerede, ich wollte die Leute nur in Kenntnis setzen, damit wir alle sehen können, was zu tun ist.

* 7) ???

Wow, das ist eine Menge Zeug. Viel los diese Woche, und ich rechne nicht damit, dass es in nächster Zeit ruhiger wird. Also schau in ein paar Minuten kurz beim Meeting vorbei, dann können wir darüber reden.

=jr
