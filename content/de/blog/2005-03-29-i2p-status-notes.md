---
title: "I2P-Statusnotizen für 2005-03-29"
date: 2005-03-29
author: "jr"
description: "Wöchentliche Statusnotizen zur I2P-Entwicklung, die das Release 0.5.0.5 mit Batching (Batch-Verarbeitung), dem UDP (SSU)-Transportprotokoll und dem verteilten Speicher Q behandeln."
categories: ["status"]
---

Hallo zusammen, Zeit für die wöchentlichen Statusnotizen

* Index

1) 0.5.0.5 2) UDP (SSU) 3) Q 4) ???

* 1) 0.5.0.5

Da ihr alle so großartige Arbeit beim schnellen Aktualisieren auf 0.5.0.4 geleistet habt, werden wir die neue Version 0.5.0.5 nach dem Meeting veröffentlichen.  Wie letzte Woche besprochen, besteht die große Änderung in der Einbindung des Batching-Codes, der mehrere kleine Nachrichten zusammenfasst, statt ihnen jeweils eine eigene vollständige 1KB tunnel-Nachricht zu geben.  Zwar ist das für sich genommen nicht revolutionär, aber es sollte die Anzahl der übermittelten Nachrichten sowie die genutzte Bandbreite deutlich reduzieren, insbesondere bei Diensten wie IRC.

Es wird in der Release-Ankündigung weitere Infos geben, aber mit der Revision 0.5.0.5 kommen zwei weitere wichtige Punkte hinzu. Erstens stellen wir den Support für Nutzer auf Versionen vor 0.5.0.4 ein – es gibt weit über 100 Nutzer auf 0.5.0.4, und frühere Releases haben erhebliche Probleme. Zweitens enthält der neue Build einen wichtigen Fix für die Anonymität gegen einen Angriff, der zwar Entwicklungsaufwand erfordern würde, aber nicht unrealistisch ist. Der Hauptteil der Änderung betrifft den Umgang mit der netDb – statt es locker zu handhaben und Einträge überall zu zwischenspeichern, beantworten wir nur noch netDb-Anfragen zu Elementen, die uns ausdrücklich übergeben wurden, unabhängig davon, ob wir die betreffenden Daten vorliegen haben oder nicht.

Wie immer gibt es Fehlerbehebungen und einige neue Funktionen, aber weitere Informationen folgen in der Release-Ankündigung.

* 2) UDP (SSU)

Wie in den letzten 6–12 Monaten immer wieder diskutiert, werden wir für unsere Inter-Router-Kommunikation auf UDP umstellen, sobald die Version 0.6 veröffentlicht ist.  Um auf diesem Weg voranzukommen, haben wir einen ersten Entwurf des Transportprotokolls im CVS bereitgestellt @ http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/udp.html?rev=HEAD

Es ist ein recht einfaches Protokoll mit den in dem Dokument skizzierten Zielen und macht sich die Fähigkeiten von I2P zunutze, um Daten sowohl zu authentifizieren als auch zu sichern und dabei so wenige externe Informationen wie möglich preiszugeben. Nicht einmal der erste Teil eines Verbindungs-Handshakes ist für jemanden identifizierbar, der I2P nicht verwendet. Das Verhalten des Protokolls ist in der Spezifikation noch nicht vollständig definiert, etwa wie die Timer ausgelöst werden oder wie die drei verschiedenen halbzuverlässigen Statusindikatoren verwendet werden, aber sie deckt die Grundlagen der Verschlüsselung, Paketisierung und des NAT-Hole-Punching (Durchdringen von NAT-Barrieren) ab. Noch ist nichts davon implementiert, aber es wird bald soweit sein, daher wäre Feedback sehr willkommen!

* 3) Q

Aum hat unermüdlich an Q(uartermaster), einem verteilten Store (verteiltes Speichersystem), gearbeitet, und die erste Fassung der Dokumentation ist online [1]. Eine der interessanten Ideen darin scheint eine Abkehr von einer reinen DHT hin zu einem System im Stil von memcached [2] zu sein, wobei jede Nutzerin/jeder Nutzer sämtliche Suchvorgänge vollständig *lokal* ausführt und die eigentlichen Daten "direkt" (nun ja, über I2P) beim Q-Server anfordert. Jedenfalls, ein paar coole Sachen; vielleicht können wir, falls Aum wach ist [3], ihm ein Update entlocken?

[1] http://aum.i2p/q/ [2] http://www.danga.com/memcached/ [3] Verdammte Zeitzonen!

* 4) ???

Es passiert noch eine ganze Menge, und wenn bis zur Besprechung mehr als nur ein paar Minuten übrig wären, könnte ich weiter darauf eingehen, aber so ist das Leben. Schau einfach vorbei.

# i2p in Kürze zum Chatten.

=jr
