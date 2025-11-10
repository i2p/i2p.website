---
title: "I2P-Statusnotizen für 2005-11-08"
date: 2005-11-08
author: "jr"
description: "Wöchentliches Update zu Stabilität von 0.6.1.4, Roadmap zur Performance-Optimierung, Veröffentlichung von I2Phex 0.1.1.35, Entwicklung des I2P-Rufus-BT-Clients, Fortschritte bei I2PSnarkGUI und Überarbeitungen der Syndie UI"
categories: ["status"]
---

Hi Leute, schon wieder Dienstag

* Index

1) Netzstatus / kurzfristige Roadmap 2) I2Phex 3) I2P-Rufus 4) I2PSnarkGUI 5) Syndie 6) ???

* 1) Net status / short term roadmap

0.6.1.4 wirkt weiterhin ziemlich stabil, auch wenn es seitdem einige Fehlerbehebungen in CVS gegeben hat. Ich habe außerdem einige Optimierungen für SSU hinzugefügt, um Daten effizienter zu übertragen, von denen ich hoffe, dass sie spürbare Auswirkungen auf das Netzwerk haben werden, sobald sie breit ausgerollt sind. Ich halte 0.6.1.5 jedoch vorerst zurück, da es noch ein paar andere Dinge gibt, die ich in die nächste Veröffentlichung aufnehmen möchte. Der aktuelle Plan ist, es dieses Wochenende herauszubringen, also haltet die Ohren offen für die neuesten Nachrichten.

Das Release 0.6.2 wird viele großartige Dinge enthalten, um noch stärkeren Gegnern zu begegnen, aber eines wird es nicht beeinflussen: die Leistung. Auch wenn Anonymität sicherlich der ganze Sinn von I2P ist, werden wir bei schlechtem Durchsatz und hoher Latenz keine Nutzer haben. Daher ist mein Plan, die Leistung zunächst auf das erforderliche Niveau zu bringen, bevor wir zur Implementierung der 0.6.2-Strategien zur Sortierung der Peers und der neuen Techniken zur Erstellung von tunnel übergehen.

* 2) I2Phex

In letzter Zeit hat sich auch an der I2Phex-Front viel getan, mit einer neuen Version 0.1.1.35 [1]. Es gab außerdem weitere Änderungen in CVS (danke, Legion!), daher würde es mich nicht überraschen, wenn im Laufe dieser Woche die Version 0.1.1.36 erscheint.

Auch bei gwebcache gab es einige gute Fortschritte (siehe http://awup.i2p/), allerdings hat meines Wissens noch niemand damit begonnen, I2Phex so zu modifizieren, dass es einen I2P-fähigen gwebcache verwendet (Interessiert? Sag mir Bescheid!).

[1] http://forum.i2p.net/viewtopic.php?t=1157

* 3) I2P-Rufus

Wie man hört, haben defnax und Rawn am Rufus BT-Client gehackt und dabei etwas I2P-bezogenen Code aus I2P-BT integriert. Den aktuellen Stand der Portierung kenne ich nicht, aber es klingt, als kämen ein paar nette Funktionen hinzu. Ich bin sicher, wir werden mehr hören, sobald es mehr zu hören gibt.

* 4) I2PSnarkGUI

Ein weiteres Gerücht, das die Runde macht, ist, dass Markus an einer neuen C#-GUI herumwerkelt... Screenshots auf PlanetPeer sehen ziemlich cool aus [2]. Es gibt weiterhin Pläne für eine plattformunabhängige Weboberfläche, aber das hier sieht ziemlich gut aus. Ich bin sicher, dass wir von Markus noch mehr hören werden, während die GUI-Entwicklung voranschreitet.

[2] http://board.planetpeer.de/index.php?topic=1338

* 5) Syndie

Es gab außerdem einige Diskussionen zu Überarbeitungen der Syndie-UI [3], und ich erwarte, dass wir an dieser Front recht bald einige Fortschritte sehen werden. dust arbeitet außerdem intensiv an Sucker und fügt eine bessere Unterstützung für das Importieren weiterer RSS/Atom-Feeds in Syndie hinzu sowie einige Verbesserungen an SML selbst.

[3] http://syndiemedia.i2p.net:8000/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&entry=1131235200000&expand=true

* 6) ???

Wie immer ist eine Menge los. Schaut in ein paar Minuten bei #i2p zu unserem wöchentlichen Entwicklertreffen vorbei.

=jr
