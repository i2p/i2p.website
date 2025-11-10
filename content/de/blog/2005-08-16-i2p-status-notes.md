---
title: "I2P-Statusnotizen für 2005-08-16"
date: 2005-08-16
author: "jr"
description: "Kurzes Update zu PeerTest-Status, Irc2P-Netzwerk-Umstellung, Fortschritt der Feedspace-GUI und zur Änderung der Meeting-Zeit auf 20:00 GMT"
categories: ["status"]
---

Hallo zusammen, heute nur kurze Notizen

* Index:

1) PeerTest-Status 2) Irc2P 3) Feedspace 4) Meta 5) ???

* 1) PeerTest status

Wie bereits erwähnt, wird das kommende 0.6.1-Release eine Reihe von Tests enthalten, um den router sorgfältiger zu konfigurieren und die Erreichbarkeit zu verifizieren (oder darauf hinzuweisen, was getan werden muss), und obwohl wir seit zwei Builds bereits Code in CVS haben, sind noch einige Verfeinerungen nötig, bevor das so reibungslos funktioniert, wie erforderlich. Derzeit nehme ich einige kleine Änderungen am dokumentierten [1] Testablauf vor, indem ich ein zusätzliches Paket hinzufüge, um Charlies Erreichbarkeit zu verifizieren, und Bobs Antwort an Alice verzögere, bis Charlie geantwortet hat. Dies sollte die Anzahl unnötiger "ERR-Reject"-Statuswerte verringern, die Leute sehen, da Bob Alice erst antwortet, wenn er einen Charlie hat, der für Tests verfügbar ist (und wenn Bob nicht antwortet, sieht Alice "Unknown" als Status).

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/udp.html#peerTesting

Wie auch immer, ja, so viel dazu - morgen sollte die Version 0.6.0.2-3 erscheinen; als Release wird sie freigegeben, sobald sie gründlich getestet ist.

* 2) Irc2P

Wie im Forum [2] erwähnt, müssen I2P-Nutzerinnen und -Nutzer, die IRC verwenden, ihre Konfiguration aktualisieren, um auf das neue IRC-Netzwerk umzusteigen. Duck wird vorübergehend offline gehen, um [redacted], und anstatt darauf zu hoffen, dass der Server in dieser Zeit keine Probleme hat, sind postman und smeghead eingesprungen und haben ein neues IRC-Netzwerk für Ihre Nutzung aufgebaut. Postman hat außerdem den Tracker von Duck und die i2p-bt‑Site unter [3] gespiegelt, und ich meine, ich hätte im neuen IRC‑Netzwerk etwas darüber gesehen, dass susi eine neue IdleRPG‑Instanz startet (siehe die Channel‑Liste für weitere Informationen).

Mein Dank gilt den Verantwortlichen für das alte i2pirc-Netzwerk (duck, baffled, die metropipe-Crew, postman) und den Verantwortlichen für das neue irc2p-Netzwerk (postman, arcturus)! Interessante Dienste und Inhalte machen I2P lohnenswert, und es liegt an euch, sie zu schaffen!

[2] http://forum.i2p.net/viewtopic.php?t=898 [3] http://hq.postman.i2p/

* 3) Feedspace

Apropos: Neulich habe ich frosks Blog gelesen, und es scheint, dass es bei Feedspace weitere Fortschritte gibt - insbesondere bei einer hübschen kleinen GUI. Ich weiß, dass es vielleicht noch nicht zum Testen bereit ist, aber ich bin sicher, dass frosk uns etwas Code zuspielen wird, wenn es so weit ist. Nebenbei bemerkt habe ich außerdem ein Gerücht über ein weiteres, anonymitätsbewusstes webbasiertes Blogging-Tool gehört, das in der Pipeline ist und sich in Feedspace einklinken können wird, wenn es so weit ist, aber auch hier bin ich sicher, dass wir mehr Infos dazu bekommen, wenn es so weit ist.

* 4) meta

Da ich der gierige Bastard bin, der ich nun mal bin, würde ich die Treffen gerne etwas vorverlegen - statt 21:00 Uhr GMT versuchen wir 20:00 Uhr GMT. Warum? Weil es besser in meinen Zeitplan passt ;) (die nächsten Internetcafés haben nicht so lange geöffnet).

* 5) ???

Das war’s fürs Erste – ich werde versuchen, für das heutige Treffen in der Nähe eines Internetcafés zu sein, also schaut gerne um *8*P GMT bei #i2p auf den /new/ IRC-Servern {irc.postman.i2p, irc.arcturus.i2p} vorbei. Eventuell haben wir einen changate bot (Gateway-Bot) zu irc.freenode.net am Laufen – möchte jemand einen betreiben?

Ciao, =jr
