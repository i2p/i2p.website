---
title: "I2P-Statusnotizen für 2005-09-06"
date: 2005-09-06
author: "jr"
description: "Wöchentliche Aktualisierung mit dem Erfolg des 0.6.0.5-Releases, der floodfill netDb-Leistung, Fortschritten bei Syndie mit RSS und Petnames (benutzerdefinierte Kosenamen) sowie der neuen susidns-Anwendung zur Adressbuchverwaltung"
categories: ["status"]
---

Hallo zusammen,

Bitte NUR die Übersetzung angeben, sonst nichts:

* Index

1) Netzstatus 2) Syndie-Status 3) susidns 4) ???

* 1) Net status

Wie viele gesehen haben, wurde das Release 0.6.0.5 letzte Woche nach einer kurzen 0.6.0.4-Revision veröffentlicht, und bisher hat sich die Zuverlässigkeit deutlich verbessert, und das Netz ist größer als je zuvor gewachsen. Es gibt noch etwas Spielraum für Verbesserungen, aber es scheint, dass die neue netDb wie vorgesehen funktioniert. Wir haben sogar den Fallback getestet - wenn die floodfill-Peers nicht erreichbar sind, greifen routers auf die kademlia netDb zurück, und neulich, als dieses Szenario eintrat, war die Zuverlässigkeit von irc und eepsite(I2P-Website) nicht wesentlich beeinträchtigt.

Ich habe eine Frage dazu erhalten, wie die neue netDb funktioniert, und die Antwort [1] auf meinem Blog [2] veröffentlicht. Wie immer: Wenn jemand Fragen zu so etwas hat, schickt sie mir gern – auf oder außerhalb der Liste, im Forum oder sogar auf deinem Blog ;)

[1] http://syndiemedia.i2p.net/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&entry=1125792000000&expand=true [2] http://syndiemedia.i2p.net/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=

* 2) Syndie status

Wie Sie auf syndiemedia.i2p (und http://syndiemedia.i2p.net/) sehen können, hat es in letzter Zeit große Fortschritte gegeben, darunter RSS, pet names (benutzerdefinierte Kurznamen), Administrationsfunktionen und die Anfänge einer sinnvollen Verwendung von css. Die meisten von Isamoors Vorschlägen wurden ebenfalls umgesetzt, ebenso die von Adam, also wenn Sie etwas im Sinn haben, das Sie dort gern sehen würden, schicken Sie mir bitte eine kurze Nachricht!

Syndie ist jetzt ziemlich nahe an der Beta, woraufhin es als eine der standardmäßigen I2P-Anwendungen ausgeliefert sowie auch als eigenständiges Paket bereitgestellt wird, daher wäre jede Hilfe sehr willkommen. Mit den neuesten Ergänzungen von heute (in cvs) ist das Skinnen von Syndie ebenfalls ein Kinderspiel – Sie können einfach eine neue Datei syndie_standard.css in Ihrem Verzeichnis i2p/docs/ anlegen, und die angegebenen Stile überschreiben Syndies Standardvorgaben. Weitere Informationen dazu finden Sie in meinem Blog [2].

* 3) susidns

Susi hat noch eine weitere Webanwendung für uns aus dem Ärmel geschüttelt - susidns [3]. Diese dient als einfache Oberfläche zur Verwaltung der Adressbuch-App - ihrer Einträge, Abonnements usw. Sie sieht ziemlich gut aus, sodass wir sie hoffentlich bald als eine der Standard-Apps ausliefern können, aber vorerst ist es ein Leichtes, sie von ihrer eepsite(I2P Site) zu holen, sie in deinem webapps-Verzeichnis zu speichern, deinen router neu zu starten, und schon bist du startklar.

[3] http://susi.i2p/?page_id=13

* 4) ???

Auch wenn wir uns in letzter Zeit eindeutig auf die Client-App-Seite konzentriert haben (und das auch weiterhin tun werden), verwende ich weiterhin einen großen Teil meiner Zeit auf den Kernbetrieb des Netzwerks, und es steht einiges Spannendes in der Pipeline – Firewall- und NAT-Hopping mittels introductions (Vermittlungen), verbesserte SSU-Autokonfiguration, fortgeschrittene Sortierung und Auswahl von Peers und sogar eine einfache Verarbeitung eingeschränkter Routen. Was die Website betrifft, hat HalfEmpty einige Verbesserungen an unseren Stylesheets vorgenommen (yay!).

Wie auch immer, es ist eine Menge los, aber mehr Zeit habe ich im Moment nicht, um das zu erwähnen, also schaut einfach um 20 Uhr UTC beim Meeting vorbei und sagt Hi :)

=jr
