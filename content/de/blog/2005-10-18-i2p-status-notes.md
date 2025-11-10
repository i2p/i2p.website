---
title: "I2P-Statusnotizen vom 2005-10-18"
date: 2005-10-18
author: "jr"
description: "Wöchentliches Update mit dem Erfolg des Releases 0.6.1.3, einer Diskussion über die Zusammenarbeit mit Freenet, der Analyse von tunnel-Bootstrap-Angriffen, dem Fortschritt bei der Behebung des Upload-Fehlers in I2Phex und einer Prämie für symmetrisches NAT"
categories: ["status"]
---

Hi zusammen, es ist wieder Dienstag

* Index

1) 0.6.1.3 2) Freenet, I2P und Darknets (oh je) 3) Tunnel-Bootstrap-Angriffe 4) I2Phex 5) Syndie/Sucker 6) ??? [500+ Prämie für symmetrisches NAT]

* 1) 0.6.1.3

Letzten Freitag haben wir ein neues 0.6.1.3-Release veröffentlicht, und nachdem 70 % des Netzwerks aktualisiert wurden, sind die Rückmeldungen sehr positiv ausgefallen. Die neuen SSU-Verbesserungen scheinen unnötige erneute Übertragungen reduziert zu haben, wodurch bei höheren Raten ein effizienterer Durchsatz möglich ist, und meines Wissens gab es keine größeren Probleme mit dem IRC-Proxy oder den Syndie-Verbesserungen.

Bemerkenswert ist, dass Eol auf rentacoder[1] eine Prämie für die Unterstützung von symmetrischem NAT ausgelobt hat, sodass wir hoffentlich auf dieser Front Fortschritte machen!

[1] http://rentacoder.com/RentACoder/misc/BidRequests/ShowBidRequest.asp?lngBidRequestId=349320

* 2) Freenet, I2P, and darknets (oh my)

Wir haben diesen Thread mit über 100 Nachrichten nun endlich abgeschlossen und haben jetzt ein klareres Bild der beiden Netzwerke, wo sie einzuordnen sind und welchen Spielraum wir für eine weitere Zusammenarbeit haben. Ich gehe hier nicht näher darauf ein, für welche Topologien oder Bedrohungsmodelle sie am besten geeignet sind, aber Sie können die Listen durchforsten, wenn Sie mehr wissen wollen. Was die Zusammenarbeit angeht, habe ich toad Beispielcode geschickt, um unseren SSU transport wiederzuverwenden, was der Freenet-Community kurzfristig hilfreich sein könnte, und später könnten wir zusammenarbeiten, um premix routing (Vormisch-Routing) für Freenet-Nutzer in Umgebungen anzubieten, in denen I2P einsetzbar ist. Mit den Fortschritten bei Freenet könnten wir Freenet auch als Client-Anwendung auf I2P zum Laufen bringen, wodurch eine automatisierte Inhaltsverteilung unter den Nutzern möglich würde, die es betreiben (z. B. das Verteilen von Syndie-Archiven und -Beiträgen), aber zuerst werden wir sehen, wie Freenets geplante Last- und Inhaltsverteilungssysteme funktionieren.

* 3) Tunnel bootstrap attacks

Michael Rogers hat sich wegen einiger interessanter neuer Angriffe auf die Erstellung von I2P-tunnels gemeldet [2][3][4]. Der primäre Angriff (ein erfolgreich durchgeführter Vorgängerangriff während des gesamten Bootstrap-Prozesses) ist interessant, aber nicht wirklich praktikabel - die Erfolgswahrscheinlichkeit beträgt (c/n)^t, wobei c die Anzahl der Angreifer, n die Zahl der Peers im Netzwerk und t die vom Ziel aufgebauten tunnels (lifetime) bezeichnet - sie ist geringer als die Wahrscheinlichkeit, dass ein Angreifer alle h Hops in einem tunnel übernimmt (P(success) = (c/n)^h), nachdem der router h tunnels aufgebaut hat.

Michael hat auf der Liste einen weiteren Angriff veröffentlicht, den wir gerade durcharbeiten, sodass du ihn dort ebenfalls mitverfolgen kannst.

[2] http://dev.i2p.net/pipermail/i2p/2005-October/001005.html [3] http://dev.i2p.net/pipermail/i2p/2005-October/001008.html [4] http://dev.i2p.net/pipermail/i2p/2005-October/001006.html

* 4) I2Phex

Striker macht weitere Fortschritte beim Upload-Bug, und Berichten zufolge hat er das Problem lokalisiert. Hoffentlich wird es heute Nacht in CVS eingecheckt und kurz darauf als 0.1.1.33 veröffentlicht. Behalten Sie das Forum [5] für weitere Informationen im Auge.

[5] http://forum.i2p.net/viewforum.i2p?f=25

Man hört, dass redzara auch beim Wiederzusammenführen mit dem Phex-Hauptzweig recht gute Fortschritte macht, sodass wir hoffentlich mit Gregors Hilfe bald alles auf den neuesten Stand bringen!

* 5) Syndie/Sucker

dust hat ebenfalls fleißig mit Sucker gearbeitet und Code geschrieben, der mehr RSS/Atom-Daten in Syndie einspeist. Vielleicht können wir Sucker und die post CLI noch weiter in Syndie integrieren, vielleicht sogar eine webbasierte Steuerung, um Importe verschiedener RSS/Atom-Feeds in unterschiedliche Blogs zu planen. Mal sehen...

* 6) ???

Es gibt noch vieles über das oben Gesagte hinaus, aber das ist im Wesentlichen das, was mir bekannt ist. Wenn jemand Fragen oder Bedenken hat oder andere Dinge zur Sprache bringen möchte, schaut heute Abend um 20:00 UTC beim Meeting in #i2p vorbei!

=jr
