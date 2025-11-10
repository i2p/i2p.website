---
title: "I2P Statusnotizen für 2005-11-01"
date: 2005-11-01
author: "jr"
description: "Wöchentliches Update: Erfolg des 0.6.1.4-Releases, Analyse von Bootstrap-Angriffen, Sicherheitskorrekturen in I2Phex 0.1.1.34, Entwicklung der Sprach-App voi2p und Integration des Syndie-RSS-Feeds"
categories: ["status"]
---

Hallo zusammen, es ist wieder so weit

* Index

1) 0.6.1.4 und Netzstatus 2) Bootstraps, Vorgänger, globale passive Angreifer und CBR 3) i2phex 0.1.1.34 4) voi2p-App 5) syndie und sucker 6) ???

* 1) 0.6.1.4 and net status

Die Veröffentlichung 0.6.1.4 vom letzten Samstag scheint ziemlich reibungslos verlaufen zu sein - 75% des Netzwerks haben bereits aktualisiert (danke!), und die meisten der übrigen sind ohnehin auf 0.6.1.3. Alles scheint recht gut zu funktionieren, und obwohl ich bisher nicht viel Feedback dazu gehört habe - weder positives noch negatives, gehe ich davon aus, dass ihr euch lautstark beschweren würdet, wenn es schlecht wäre :)

Insbesondere wäre ich an Rückmeldungen von Personen interessiert, die Einwahlverbindungen über Modem nutzen, da die von mir durchgeführten Tests lediglich eine grundlegende Simulation dieser Art von Verbindung darstellen.

* 2) boostraps, predecessors, global passive adversaries, and CBR

Es hat auf der Liste viele weitere Diskussionen zu einigen Ideen gegeben, mit einer online verfügbaren Zusammenfassung der Bootstrap-Angriffe [1]. Ich habe einige Fortschritte beim Ausarbeiten der Kryptographie für Option 3 gemacht, und obwohl noch nichts veröffentlicht wurde, ist es ziemlich unkompliziert.

[1] http://dev.i2p.net/pipermail/i2p/2005-October/001146.html

Es gab weitere Diskussionen darüber, wie sich mittels tunnels mit konstanter Bitrate (CBR) die Widerstandsfähigkeit gegenüber mächtigen Gegnern verbessern lässt, und obwohl wir die Möglichkeit haben, diesen Weg zu erforschen, ist er derzeit für I2P 3.0 vorgesehen, da seine korrekte Nutzung erhebliche Ressourcen erfordert und voraussichtlich messbare Auswirkungen darauf hätte, wer I2P bei einem solchen Overhead nutzen würde sowie welche Gruppen dazu überhaupt in der Lage wären oder nicht.

* 3) I2Phex 0.1.1.34

Letzten Samstag gab es außerdem ein neues I2Phex-Release [2], das ein Leck bei Dateideskriptoren behob, das schließlich zum Ausfall von I2Phex führen konnte (danke, Complication!), und Code entfernte, der es Personen ermöglicht hätte, Ihrer I2Phex-Instanz aus der Ferne anzuweisen, bestimmte Dateien herunterzuladen (danke, GregorK!). Ein Update wird dringend empfohlen.

Es gab außerdem ein Update der CVS-Version (noch nicht veröffentlicht), das einige Synchronisationsprobleme behebt - Phex geht davon aus, dass einige Netzwerkoperationen sofort verarbeitet werden, während I2P sich manchmal eine Weile Zeit lässt, Dinge zu erledigen :) Das äußert sich dadurch, dass die GUI eine Weile hängt, Downloads oder Uploads ins Stocken geraten oder Verbindungen abgelehnt werden (und vielleicht noch auf ein paar andere Arten). Es wurde bisher noch nicht viel getestet, wird aber wahrscheinlich diese Woche in 0.1.1.35 ausgeliefert. Ich bin sicher, dass im Forum weitere Neuigkeiten veröffentlicht werden, sobald es mehr zu berichten gibt.

[2] http://forum.i2p.net/viewtopic.php?t=1143

* 4) voi2p app

Aum arbeitet intensiv an seiner neuen App für Sprache (und Text) über I2P, und auch wenn ich sie noch nicht gesehen habe, klingt das vielversprechend. Vielleicht kann uns Aum im Meeting ein Update geben, oder wir warten einfach geduldig auf die erste Alpha-Version :)

* 5) syndie and sucker

dust hat fleißig an Syndie und Sucker gearbeitet, und der neueste CVS-Build von I2P ermöglicht es dir jetzt, Inhalte automatisch aus RSS- und Atom-Feeds zu beziehen und sie in deinem Syndie-Blog zu veröffentlichen. Im Moment musst du lib/rome-0.7.jar und lib/jdom.jar explizit zu deiner wrapper.config (wrapper.java.classpath.20 und 21) hinzufügen, aber wir werden das bündeln, sodass das später nicht mehr erforderlich ist. Es ist noch in Arbeit, und Rome 0.8 (noch nicht veröffentlicht) scheint ein paar wirklich coole Dinge zu bieten, etwa die Möglichkeit, die Enclosures (Anhänge) aus einem Feed abzugreifen, die Sucker dann als Anhang zu einem Syndie-Beitrag importieren kann (schon jetzt verarbeitet Sucker allerdings auch Bilder und Links!).

Wie bei allen RSS-Feeds scheint es einige Unstimmigkeiten dabei zu geben, wie die Inhalte eingebunden werden, daher lassen sich manche Feeds reibungsloser einbinden als andere. Ich denke, wenn Leute helfen würden, das mit verschiedenen Feeds zu testen und dust über alle Probleme informieren, bei denen es aussteigt, könnte das nützlich sein. Auf jeden Fall sieht das ziemlich spannend aus, gute Arbeit, dust!

* 6) ???

Das war's fürs Erste, aber wenn jemand Fragen hat oder einige Dinge weiter besprechen möchte, schaut einfach beim Meeting um 20:00 Uhr GMT vorbei (denkt an die Sommerzeit!).

=jr
