---
title: "I2P-Statushinweise vom 2005-01-25"
date: 2005-01-25
author: "jr"
description: "Wöchentliche I2P-Entwicklungsstatus-Notizen zu Fortschritten beim tunnel-Routing in 0.5, der SAM-.NET-Portierung, der GCJ-Kompilierung und Diskussionen zum UDP-Transport"
categories: ["status"]
---

Hallo zusammen, kurzes wöchentliches Status-Update

* Index

1) 0.5 Status 2) sam.net 3) gcj Fortschritt 4) udp 5) ???

* 1) 0.5 status

In der vergangenen Woche sind wir auf der 0.5-Seite deutlich vorangekommen. Die zuvor diskutierten Probleme sind behoben, was die Kryptografie drastisch vereinfacht und das Tunnel-Looping-Problem beseitigt. Die neue Technik [1] ist implementiert, und die Unit-Tests sind vorhanden. Als Nächstes füge ich mehr Code zusammen, um diese Tunnel in den Haupt-router zu integrieren, und baue anschließend die Tunnel-Management- und Pooling-Infrastruktur auf. Sobald das steht, lassen wir es durch den sim (Simulator) laufen und anschließend auf einem parallelen Netz laufen, um es ausgiebig zu testen, bevor wir das Ganze abrunden und es 0.5 nennen.

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/tunnel-alt.html?rev=HEAD

* 2) sam.net

smeghead hat eine neue Portierung des SAM-Protokolls auf .net zusammengestellt - c#, mono/gnu.NET kompatibel (yay smeghead!). Das befindet sich in cvs unter i2p/apps/sam/csharp/ mit nant und weiteren Hilfsprogrammen - jetzt können alle .net-Devs mit i2p loslegen und hacken :)

* 3) gcj progress

smeghead ist definitiv richtig in Fahrt – nach letztem Stand lässt sich der router mit einigen Modifikationen unter dem neuesten gcj [2] build kompilieren (w00t!). Es funktioniert allerdings noch nicht, aber die Modifikationen, um die gcj-Verwirrung bei einigen Konstrukten innerer Klassen zu umgehen, sind definitiv ein Fortschritt. Vielleicht kann smeghead uns ein Update geben?

[2] http://gcc.gnu.org/java/

* 4) udp

Hier gibt es nicht viel zu sagen, allerdings hat Nightblade im Forum eine interessante Reihe von Bedenken [3] geäußert und gefragt, warum wir auf UDP setzen. Wenn du ähnliche Bedenken hast oder andere Vorschläge, wie wir die Punkte angehen können, auf die ich in meiner Antwort eingegangen bin, dann melde dich bitte zu Wort!

[3] http://forum.i2p.net/viewtopic.php?t=280

* 5) ???

Ja, okay, ich bin schon wieder spät dran mit den Notizen, zieht’s von meinem Gehalt ab ;) Wie auch immer, es ist viel los, also schaut entweder für die Besprechung im Channel vorbei, schaut euch hinterher die geposteten Logs an, oder postet in der Mailingliste, wenn ihr etwas zu sagen habt. Ach ja, nebenbei: Ich habe nachgegeben und innerhalb von i2p [4] einen Blog gestartet.

=jr [4] http://jrandom.dev.i2p/ (Schlüssel in http://dev.i2p.net/i2p/hosts.txt)
