---
title: "I2P-Statusnotizen für 2005-02-15"
date: 2005-02-15
author: "jr"
description: "Wöchentliche Notizen zum I2P-Entwicklungsstatus, die das Netzwachstum auf 211 routers, die Vorbereitungen für das Release 0.5 und i2p-bt 0.1.7 abdecken"
categories: ["status"]
---

Hallo, es ist wieder diese Zeit der Woche,

* Index

1) Netzstatus
2) 0.5 Status
3) i2p-bt 0.1.7
4) ???

* 1) Net status

Auch wenn keine neuen Fehler im Netzwerk aufgetaucht sind, haben wir letzte Woche auf einer beliebten französischen P2P-Website etwas Aufmerksamkeit bekommen, was sowohl zu einem Anstieg der Nutzerzahl als auch der BitTorrent-Aktivität geführt hat. Auf dem Höhepunkt erreichten wir 211 routers im Netz, auch wenn es sich zuletzt zwischen 150 und 180 eingependelt hat. Die gemeldete Bandbreitennutzung ist ebenfalls gestiegen, allerdings hat sich leider die IRC-Zuverlässigkeit verschlechtert, wobei einer der Server aufgrund der Last seine Bandbreitenlimits gesenkt hat. Es gab eine Reihe von Verbesserungen an der Streaming-Bibliothek, um dem entgegenzuwirken, aber sie befinden sich im 0.5-pre-Branch, sodass sie im Live-Netz noch nicht verfügbar sind.

Ein weiteres vorübergehendes Problem war der Ausfall eines der HTTP-Outproxies (www1.squid.i2p), wodurch 50 % der Outproxy-Anfragen fehlschlugen.  Sie können diesen Outproxy vorübergehend entfernen, indem Sie Ihre I2PTunnel config [1] öffnen, den eepProxy bearbeiten und die Zeile "Outproxies:" so ändern, dass sie nur "squid.i2p" enthält.  Hoffentlich bekommen wir den anderen bald wieder online, um die Redundanz zu erhöhen.

[1] http://localhost:7657/i2ptunnel/index.jsp

* 2) 0.5 status

In der vergangenen Woche gab es an Version 0.5 große Fortschritte (ich wette, ihr könnt es schon nicht mehr hören, oder?). Dank der Hilfe von postman, cervantes, duck, spaetz und einer ungenannten Person haben wir seit fast einer Woche ein Testnetz mit dem neuen Code betrieben und eine ganze Reihe von Bugs behoben, die mir in meinem lokalen Testnetz nicht aufgefallen waren.

Seit etwa einem Tag sind die Änderungen geringfügig, und ich rechne nicht damit, dass noch wesentlicher Code übrig ist, bevor die 0.5-Version herausgeht. Es bleibt noch etwas zusätzliche Bereinigung, Dokumentation und Zusammenstellung, und es schadet nicht, das 0.5-Testnetz weiterlaufen zu lassen, falls mit der Zeit weitere Fehler zutage treten. Da dies eine NICHT ABWÄRTSKOMPATIBLE VERÖFFENTLICHUNG sein wird, damit Sie Zeit haben, das Update zu planen, lege ich als einfache Frist DIESEN FREITAG für die Veröffentlichung von 0.5 fest.

Wie bla auf irc erwähnte, könnten Betreiber von eepsite(I2P Site) in Erwägung ziehen, ihre Seite am Donnerstag oder Freitag vom Netz zu nehmen und sie bis Samstag offline zu lassen, wenn viele Nutzer das Upgrade durchgeführt haben. Dies hilft, die Auswirkungen eines Schnittmengenangriffs zu verringern (z. B. wenn 90 % des Netzwerks auf 0.5 migriert sind und du noch auf 0.4 bist, weiß jemand, der deine eepsite(I2P Site) erreicht, dass du zu den 10 % der router gehörst, die noch im Netzwerk sind).

Ich könnte anfangen zu erklären, was in 0.5 aktualisiert wurde, aber am Ende würde ich Seiten über Seiten schreiben, also warte ich vielleicht lieber und packe das in die Dokumentation, die ich noch schreiben sollte :)

* 3) i2p-bt 0.1.7

duck hat ein Bugfix-Release für das 0.1.6-Update der letzten Woche zusammengestellt, und wie man hört, ist es der Hammer (vielleicht sogar /zu/ heftig, angesichts der gestiegenen Netzwerkauslastung ;)  Mehr Infos @ dem i2p-bt-Forum [2]

[2] http://forum.i2p.net/viewtopic.php?t=300

* 4) ???

Es tut sich noch vieles in den IRC-Diskussionen und im Forum [3], zu viel, um es kurz zusammenzufassen. Vielleicht können die Interessierten beim Treffen vorbeischauen und uns Updates und Gedanken geben? Wie dem auch sei, bis gleich

=jr
