---
title: "20 Jahre Privatsphäre: Eine kurze Geschichte von I2P"
date: 2021-08-28
slug: "20-years-of-privacy-a-brief-history-of-i2p"
author: "sadie"
description: "Eine Geschichte von I2P, so wie wir es kennen"
categories: ["general"]
API_Translate: wahr
---

## Unsichtbarkeit ist die beste Verteidigung: der Aufbau eines Internets innerhalb des Internets

> "Ich glaube, die meisten Menschen wollen diese Technologie, damit sie sich frei äußern können. Es ist ein beruhigendes Gefühl, wenn man weiß, dass man das tun kann. Gleichzeitig können wir einige der im Internet auftretenden Probleme überwinden, indem wir sowohl die Sichtweise auf Sicherheit und Privatsphäre als auch den Stellenwert, der ihnen beigemessen wird, ändern."

Im Oktober 2001 hatte 0x90 (Lance James) einen Traum. Es begann als ein "Wunsch nach sofortiger Kommunikation mit anderen Freenet-Benutzern, um über Freenet-Themen zu sprechen und Freenet-Schlüssel auszutauschen, während Anonymität, Privatsphäre und Sicherheit weiterhin gewahrt bleiben." Es hieß IIP — the Invisible IRC Project.

The Invisible IRC Project basierte auf einem Ideal und dem Rahmenwerk hinter The InvisibleNet. In einem Interview aus dem Jahr 2002 beschrieb 0x90 das Projekt als fokussiert auf "die Innovation intelligenter Netzwerktechnologie" mit dem Ziel, "die höchsten Standards in Sicherheit und Privatsphäre auf dem weit verbreiteten, jedoch notorisch unsicheren Internet bereitzustellen."

Bis 2003 hatten mehrere andere ähnliche Projekte begonnen, die größten waren Freenet, GNUNet und Tor. Alle diese Projekte verfolgten das weit gefasste Ziel, verschiedene Arten von Datenverkehr zu verschlüsseln und zu anonymisieren. Für IIP wurde klar, dass IRC allein kein ausreichend großes Ziel war. Benötigt wurde eine anonymisierende Schicht für alle Protokolle.

Anfang 2003 schloss sich ein neuer anonymer Entwickler, "jrandom", dem Projekt an. Sein ausdrückliches Ziel war es, den Auftrag von IIP zu erweitern. jrandom wollte die IIP-Codebasis in Java neu schreiben und die Protokolle auf Grundlage jüngerer Fachveröffentlichungen sowie der frühen Designentscheidungen, die Tor und Freenet trafen, neu entwerfen. Einige Konzepte wie "onion routing" (Zwiebel-Routing) wurden so angepasst, dass daraus "garlic routing" (Knoblauch-Routing) wurde.

Bis zum Spätsommer 2003 hatte jrandom die Kontrolle über das Projekt übernommen und es in Invisible Internet Project oder "I2P" umbenannt. Er veröffentlichte ein Dokument, das die Philosophie des Projekts skizzierte, und ordnete seine technischen Ziele und sein Design in den Kontext von Mix-Netzen und Anonymisierungsschichten ein. Außerdem veröffentlichte er die Spezifikation zweier Protokolle (I2CP und I2NP), die die Grundlage des Netzwerks bilden, das I2P heute verwendet.

Bis Herbst 2003 entwickelten sich I2P, Freenet und Tor rasant. jrandom veröffentlichte am 1. November 2003 I2P Version 0.2 und setzte in den folgenden drei Jahren die raschen Veröffentlichungen fort.

Im Februar 2005 installierte zzz zum ersten Mal I2P. Bis zum Sommer 2005 hatte zzz zzz.i2p und stats.i2p eingerichtet, die zu zentralen Ressourcen für die I2P-Entwicklung wurden. Im Juli 2005 veröffentlichte jrandom Version 0.6, einschließlich des innovativen SSU (Secure Semi-reliable UDP) Transportprotokolls zur IP-Ermittlung und Firewall-Traversal.

Von Ende 2006 bis ins Jahr 2007 hinein verlangsamte sich die I2P-Kernentwicklung dramatisch, da jrandom seinen Schwerpunkt auf Syndie verlagerte. Im November 2007 kam es zur Katastrophe, als jrandom eine kryptische Nachricht sandte, dass er sich für ein Jahr oder länger eine Auszeit nehmen müsse. Leider hörten sie nie wieder von jrandom.

Die zweite Phase der Katastrophe ereignete sich am 13. Januar 2008, als der Hosting-Anbieter für fast alle i2p.net-Server von einem Stromausfall betroffen war und den Betrieb nicht vollständig wieder aufnahm. Complication, welterde und zzz trafen schnell Entscheidungen, um das Projekt wieder zum Laufen zu bringen, zogen zu i2p2.de um und wechselten bei der Versionsverwaltung von CVS zu monotone.

Das Projekt erkannte, dass es sich zu stark auf zentralisierte Ressourcen verlassen hatte. Die Arbeiten im gesamten Jahr 2008 dezentralisierten das Projekt und verteilten die Rollen auf mehrere Personen. Ab Release 0.7.6 am 31. Juli 2009 signierte zzz die nächsten 49 Releases.

Bis Mitte 2009 hatte zzz die Codebasis deutlich besser verstanden und zahlreiche Skalierbarkeitsprobleme identifiziert. Das Netzwerk verzeichnete Wachstum aufgrund seiner Fähigkeiten zur Anonymisierung und zur Zensurumgehung. Automatische Updates innerhalb des Netzwerks wurden verfügbar.

Im Herbst 2010 erklärte zzz ein Moratorium für die I2P-Entwicklung, bis die Website-Dokumentation vollständig und korrekt war. Es dauerte 3 Monate.

Ab 2010 nahmen zzz, ech, hottuna und weitere Mitwirkende jährlich am CCC (Chaos Communications Congress) teil, bis die COVID-bedingten Beschränkungen in Kraft traten. Das Projekt baute eine Gemeinschaft auf und feierte Veröffentlichungen gemeinsam.

Im Jahr 2013 wurde Anoncoin als die erste Kryptowährung mit eingebauter I2P-Unterstützung geschaffen, wobei Entwickler wie meeh Infrastruktur für das I2P-Netzwerk bereitstellten.

2014 begann str4d, zu I2PBote beizutragen, und bei Real World Crypto begannen Diskussionen über die Aktualisierung der I2P-Kryptographie. Bis Ende 2014 war der Großteil der neuen Signaturkryptographie abgeschlossen, darunter ECDSA und EdDSA.

Im Jahr 2015 fand die I2PCon in Toronto statt, mit Vorträgen, Unterstützung aus der Community und Teilnehmern aus Amerika und Europa. Im Jahr 2016 hielt str4d bei der Real World Crypto Stanford einen Vortrag über die Fortschritte bei der Umstellung der Kryptografie.

NTCP2 wurde 2018 (Release 0.9.36) implementiert und bietet Schutz vor DPI-Zensur, während schnellere, moderne Kryptografie die CPU-Last reduziert.

Im Jahr 2019 nahm das Team an weiteren Konferenzen teil, darunter DefCon und Monero Village, und suchte den Austausch mit Entwicklern und Forschenden. Die Forschung von Hoàng Nguyên Phong zur I2P-Zensur wurde für FOCI bei USENIX angenommen, was zur Erstellung von I2P Metrics führte.

Auf dem CCC 2019 wurde die Entscheidung getroffen, von Monotone zu GitLab zu migrieren. Am 10. Dezember 2020 stellte das Projekt offiziell von Monotone auf Git um und schloss sich damit der Welt der Entwickler an, die Git verwenden.

0.9.49 (2021) begann die Migration auf die neue, schnellere ECIES-X25519-Verschlüsselung für routers und schloss damit jahrelange Spezifikationsarbeit ab. Die Migration würde mehrere Releases in Anspruch nehmen.

## 1.5.0 — Das vorgezogene Jubiläums-Release

Nach 9 Jahren mit 0.9.x-Versionen wechselte das Projekt direkt von 0.9.50 auf 1.5.0 als Würdigung von fast 20 Jahren Arbeit, um Anonymität und Sicherheit zu bieten. Diese Version schloss die Implementierung kleinerer tunnel-Build-Nachrichten zur Reduzierung der Bandbreite ab und setzte die Umstellung auf X25519-Verschlüsselung fort.

**Herzlichen Glückwunsch, Team. Machen wir noch 20.**
