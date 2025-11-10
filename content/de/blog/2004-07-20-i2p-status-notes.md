---
title: "I2P-Statushinweise für 2004-07-20"
date: 2004-07-20
author: "jr"
description: "Wöchentliches Status-Update zu Release 0.3.2.3, Kapazitätsänderungen, Website-Updates und Sicherheitsaspekten"
categories: ["status"]
---

**1) 0.3.2.3, 0.3.3, und die Roadmap**

Nach der Veröffentlichung von 0.3.2.3 in der letzten Woche habt ihr alle großartige Arbeit beim Aktualisieren geleistet - wir haben jetzt nur noch zwei Nachzügler (einer bei 0.3.2.2 und einer ganz weit zurück bei 0.3.1.4 :). In den letzten Tagen war das Netzwerk zuverlässiger als üblich - Leute bleiben stundenlang auf irc.duck.i2p, größere Dateidownloads gelingen von eepsites(I2P Sites), und die allgemeine Erreichbarkeit von eepsite(I2P Site) ist ziemlich gut. Da es gut läuft und ich euch auf Trab halten möchte, habe ich beschlossen, ein paar grundlegende Konzepte zu ändern, und wir werden sie in ein bis zwei Tagen mit einem 0.3.3-Release bereitstellen.

Da einige Leute sich zu unserem Zeitplan geäußert und sich gefragt haben, ob wir die veröffentlichten Termine einhalten werden, habe ich beschlossen, die Website zu aktualisieren, damit sie die Roadmap widerspiegelt, die ich auf meinem palmpilot habe – also habe ich das getan [1]. Die Termine haben sich verschoben und einige Punkte wurden neu angeordnet, aber der Plan ist immer noch derselbe wie der, der letzten Monat besprochen wurde [2].

0.4 wird die vier genannten Release-Kriterien erfüllen (funktional, sicher, anonym und skalierbar), allerdings werden vor 0.4.2 nur wenige Personen hinter NATs und Firewalls teilnehmen können, und vor 0.4.3 wird es aufgrund des Overheads durch die Aufrechterhaltung einer großen Anzahl von TCP-Verbindungen zu anderen routers eine effektive Obergrenze für die Größe des Netzwerks geben.

[1] http://www.i2p.net/redesign/roadmap [2] http://dev.i2p.net/pipermail/i2p/2004-June/000286.html

**2) s/reliability/capacity/g**

In der letzten Woche oder so haben die Leute auf #i2p mich gelegentlich darüber schimpfen hören, wie unsere Zuverlässigkeitsbewertungen völlig willkürlich sind (und welche Probleme das in den letzten paar Versionen verursacht hat). Also haben wir das Konzept der Zuverlässigkeit komplett abgeschafft und es durch eine Messung der Kapazität ersetzt - "Wie viel kann ein Peer für uns leisten?" Das hatte Folgewirkungen im gesamten Peer-Auswahl- und Peer-Profiling-Code (und natürlich auf der router-Konsole), aber abgesehen davon wurde nicht viel geändert.

Weitere Informationen zu dieser Änderung finden sich auf der überarbeiteten Seite zur Peer-Auswahl [3], und wenn 0.3.3 veröffentlicht wird, könnt ihr die Auswirkungen aus erster Hand sehen (ich habe in den letzten Tagen damit herumgespielt und dabei einige Einstellungen angepasst usw.).

[3] http://www.i2p.net/redesign/how_peerselection

**3) Website-Aktualisierungen**

In der vergangenen Woche haben wir beim Website-Redesign [4] große Fortschritte gemacht - die Navigation vereinfacht, einige wichtige Seiten bereinigt, alte Inhalte importiert und einige neue Einträge [5] verfasst. Wir sind fast so weit, die Website live zu schalten, aber es gibt noch ein paar Dinge, die erledigt werden müssen.

Heute hat duck die Website durchgesehen und eine Bestandsaufnahme der fehlenden Seiten erstellt, und nach den Updates heute Nachmittag gibt es noch ein paar offene Punkte, von denen ich hoffe, dass wir sie entweder angehen oder dass sich Freiwillige darum kümmern:

* **documentation**: hmm, do we need any content for this? or can we have it just sit as a header with no page behind it?
* **development**: I think this is in the same boat as "documentation" above
* **news**: perhaps we can remove the 'announcements' page and put that content here? or should we do as above and let news be a simple heading, with an announcements page below?
* **i2ptunnel_services, i2ptunnel_tuning, i2ptunnel_lan**: We need someone to rewrite the 'how to set up an eepsite(I2P Site)' page, as well as include answers to the two most frequently asked I2PTunnel questions (how to access it through a LAN and how to configure its tunnels - answers being: -e "listen_on 0.0.0.0" and -e 'clientoptions tunnels.numInbound=1 tunnels.depthInbound=1', respectively) Perhaps we can come up with some more comprehensive user level I2PTunnel documentation?
* **jvm**: er, I'm not sure about this page - is it 'how to tweak the JVM for optimal performance'? do we *know*?
* **config_tweaks**: other config parameters for the router (bandwidth limiting, etc). could someone go through the router.config and take a stab at what everything means? if anyone has any questions, please let me know.
* **more meeting logs**: mihi posted up an archive of some logs, perhaps a volunteer can sift through those and post them up?
* perhaps we can update the meetings.html to be date based and include a link to that week's status update along with any release announcements preceding it?

Abgesehen davon denke ich, dass die Website so gut wie bereit ist, live geschaltet zu werden. Hat jemand in dieser Hinsicht Vorschläge oder Bedenken?

[4] http://www.i2p.net/redesign/ [5] http://dev.i2p.net/pipermail/i2pwww/2004-July/thread.html

**4) Angriffe und Abwehrmaßnahmen**

Connelly hat sich ein paar neue Ansatzpunkte überlegt, um Schwachstellen in der Sicherheit und Anonymität des Netzwerks aufzudecken, und dabei ist er auf einige Möglichkeiten gestoßen, wie wir Verbesserungen vornehmen können. Auch wenn einige Aspekte der von ihm beschriebenen Techniken nicht wirklich zu I2P passen, seht ihr vielleicht Möglichkeiten, sie weiter auszubauen, um das Netzwerk noch stärker anzugreifen? Na los, probiert’s mal :)

**5) ???**

Das ist so ziemlich alles, woran ich mich vor der Sitzung heute Abend erinnern kann - bringt bitte alles zur Sprache, was ich übersehen habe. Wie auch immer, bis gleich in #i2p in ein paar Minuten.

=jr
