---
title: "I2P Statusnotizen vom 2005-03-01"
date: 2005-03-01
author: "jr"
description: "Wöchentliche Statusnotizen zur I2P-Entwicklung zu Fehlern in 0.5.0.1 und zum bevorstehenden 0.5.0.2, Roadmap-Updates, Adressbuch-Editor und i2p-bt-Updates"
categories: ["status"]
---

Hallo zusammen, es ist Zeit für unser Status-Update.

* Index

1) 0.5.0.1 2) Roadmap 3) Adressbuch-Editor und Konfiguration 4) i2p-bt 5) ???

* 1) 0.5.0.1

Wie letzte Woche besprochen, haben wir wenige Stunden nach dem Treffen ein neues Release 0.5.0.1 herausgebracht, das die Fehler in 0.5 behob, die (unter anderem) dazu geführt hatten, dass eine massive Anzahl an tunnels aufgebaut wurde. Generell hat diese Revision die Lage verbessert, aber bei breiter angelegten Tests sind uns noch einige zusätzliche Fehler aufgefallen, die bei einigen Nutzern auftreten. Insbesondere kann die 0.5.0.1-Revision Unmengen an CPU fressen, wenn du eine langsame Maschine hast oder die tunnels deines routers massenhaft fehlschlagen, und einige langlebige I2PTunnel-Server können so viel RAM verschlingen, bis es zu einem OOM (Out-of-Memory) kommt. Außerdem gibt es einen schon lange bestehenden Fehler in der Streaming-Bibliothek, bei dem das Herstellen einer Verbindung scheitern kann, wenn genau die passenden Ausfälle zusammenkommen.

Die meisten davon (und weitere) wurden in cvs bereits behoben, aber einige sind noch offen. Sobald sie alle behoben sind, packen wir das Ganze zusammen und veröffentlichen es als 0.5.0.2-Release. Ich bin mir nicht genau sicher, wann das sein wird, hoffentlich diese Woche, aber wir werden sehen.

* 2) roadmap

Nach größeren Releases scheint die Roadmap [1]... angepasst zu werden. Das 0.5-Release bildete da keine Ausnahme. Diese Seite widerspiegelt, was ich für sinnvoll und angemessen für das weitere Vorgehen halte, aber natürlich kann sie angepasst werden, wenn mehr Leute einsteigen und mithelfen. Sie werden die deutliche Unterbrechung zwischen 0.6 und 0.6.1 feststellen, und auch wenn das viel Arbeit widerspiegelt, widerspiegelt es ebenso die Tatsache, dass ich umziehen werde (es ist wieder diese Jahreszeit).

[1] http://www.i2p.net/roadmap

* 3) addressbook editor and config

Detonate hat mit Arbeiten an einer webbasierten Oberfläche zur Verwaltung der Adressbucheinträge (hosts.txt) begonnen, und es sieht ziemlich vielversprechend aus.  Vielleicht können wir während des Meetings ein Update von detonate bekommen?

Außerdem hat smeghead an einer webbasierten Oberfläche zur Verwaltung der Adressbuch-Konfiguration (subscriptions.txt, config.txt) gearbeitet.  Vielleicht können wir während des Meetings ein Update von smeghead erhalten?

* 4) i2p-bt

Es hat einige Fortschritte im Bereich i2p-bt gegeben, mit einer neuen Version 0.1.8, die die azneti2p-Kompatibilitätsprobleme behebt, wie in der Sitzung letzte Woche besprochen. Vielleicht können wir während der Sitzung ein Update von duck oder smeghead erhalten?

Legion hat außerdem einen Fork von i2p-bt rev erstellt, weiteren Code integriert, einige Dinge korrigiert und stellt auf seiner eepsite(I2P Site) ein Windows-Binary bereit. Die Ankündigung [2] scheint anzudeuten, dass der Quellcode möglicherweise verfügbar gemacht wird, allerdings ist er derzeit nicht auf der eepsite(I2P Site) zu finden. Die I2P-Entwickler haben den Code dieses Clients nicht geprüft (ja, nicht einmal gesehen), daher sollten diejenigen, die Anonymität benötigen, zunächst eine Kopie des Codes beschaffen und ihn prüfen.

[2] http://forum.i2p.net/viewtopic.php?t=382

Es wird außerdem an einer Version 2 von Legions BT-Client gearbeitet, allerdings kenne ich den aktuellen Stand nicht.  Vielleicht können wir während des Meetings ein Update von Legion erhalten?

* 5) ???

Thats about all I have to say atm, lots and lots going on.  Anyone else working on things that perhaps we can get an update for during the meeting?

=jr
