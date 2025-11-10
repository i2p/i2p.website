---
title: "Namensübersetzung für GarliCat"
number: "105"
author: "Bernhard R. Fischer"
created: "2009-12-04"
lastupdated: "2009-12-04"
status: "Gestorben"
thread: "http://zzz.i2p/topics/453"
---

## Überblick

Diese Vorschlag bezieht sich auf die Unterstützung von DNS-Rückwärtslookups für I2P.


## Aktueller Übersetzungsmechanismus

GarliCat (GC) führt die Namensübersetzung zur Einrichtung von Verbindungen zu anderen GC-Knoten durch. Diese Namensübersetzung ist lediglich eine Umkodierung der binären Darstellung einer Adresse in die Base32-codierte Form. Somit funktioniert die Übersetzung in beide Richtungen.

Diese Adressen sind auf eine Länge von 80 Bit gewählt. Das liegt daran, dass Tor 80 Bit lange Werte zur Adressierung seiner versteckten Dienste verwendet. Somit arbeitet OnionCat (das GC für Tor) ohne weiteren Eingriff mit Tor.

Unglücklicherweise (in Bezug auf dieses Adressschema) verwendet I2P 256 Bit lange Werte zur Adressierung seiner Dienste. Wie bereits erwähnt, transkodiert GC zwischen binärer und Base32-codierter Form. Aufgrund der Natur von GC als Layer-3-VPN sind die Adressen in ihrer binären Darstellung als IPv6-Adressen mit einer Gesamtlänge von 128 Bit definiert. Offensichtlich passen 256 Bit lange I2P-Adressen nicht hinein.

Daher wird ein zweiter Schritt der Namensübersetzung notwendig:
IPv6-Adresse (binär) -1a-> Base32-Adresse (80 Bit) -2a-> I2P-Adresse (256 Bit)
-1a- ... GC-Übersetzung
-2a- ... I2P hosts.txt Lookup

Die aktuelle Lösung besteht darin, den I2P-Router die Arbeit machen zu lassen. Dies wird erreicht, indem die 80 Bit Base32-Adresse und ihr Ziel (die I2P-Adresse) als Name/Wert-Paar in die hosts.txt oder privatehosts.txt-Datei des I2P-Routers eingefügt werden.

Dies funktioniert im Grunde, aber es hängt von einem Namensdienst ab, der sich (meiner Meinung nach) in einem Entwicklungsstadium befindet und nicht ausgereift genug ist (insbesondere in Bezug auf Namensverteilung).


## Eine skalierbare Lösung

Ich schlage vor, die Adressierungsstufen in Bezug auf I2P (und möglicherweise auch für Tor) so zu ändern, dass GC Rückwärtslookups auf den IPv6-Adressen unter Verwendung des regulären DNS-Protokolls durchführt. Die Rückwärtszone soll direkt die 256 Bit lange I2P-Adresse in ihrer Base32-codierten Form enthalten. Dies ändert den Lookup-Mechanismus zu einem einstufigen Verfahren und bringt weitere Vorteile.
IPv6-Adresse (binär) -1b-> I2P-Adresse (256 Bit)
-1b- ... DNS-Rückwärtslookup

DNS-Lookups innerhalb des Internets sind als Informationslecks in Bezug auf Anonymität bekannt. Daher müssen diese Lookups innerhalb von I2P durchgeführt werden. Dies impliziert, dass mehrere DNS-Dienste innerhalb von I2P vorhanden sein sollten. Da DNS-Abfragen üblicherweise über das UDP-Protokoll durchgeführt werden, wird GC selbst für den Datentransport benötigt, da es UDP-Pakete transportiert, was I2P nativ nicht tut.

Mit DNS sind weitere Vorteile verbunden:
1) Es ist ein wohlbekanntes Standardprotokoll, das kontinuierlich verbessert wird und für das viele Werkzeuge (Clients, Server, Bibliotheken,...) existieren.
2) Es ist ein verteiltes System. Es unterstützt standardmäßig den Namensraum, der parallel auf mehreren Servern gehostet wird.
3) Es unterstützt Kryptografie (DNSSEC), die die Authentifizierung von Ressourceneinträgen ermöglicht. Dies könnte direkt mit den Schlüsseln eines Ziels verknüpft werden.


## Zukünftige Möglichkeiten

Es könnte möglich sein, dass dieser Namensdienst auch für direkte Lookups verwendet werden kann. Dies bedeutet die Übersetzung von Hostnamen in I2P-Adressen und/oder IPv6-Adressen. Aber diese Art von Lookup benötigt weitere Untersuchungen, da diese Lookups üblicherweise durch die lokal installierte Resolver-Bibliothek durchgeführt werden, die reguläre Internet-Namensserver nutzt (z.B. wie in /etc/resolv.conf auf Unix-ähnlichen Systemen angegeben). Dies unterscheidet sich von den Rückwärtslookups von GC, die ich oben erklärt habe.
Eine weitere Möglichkeit könnte sein, dass die I2P-Adresse (Ziel) automatisch registriert wird, wenn ein GC-Inbound-Tunnel erstellt wird. Dies würde die Benutzerfreundlichkeit erheblich verbessern.
