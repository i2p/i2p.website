---
title: "Diskussion zur Netzwerkdatenbank"
description: "Historische Anmerkungen zu floodfill, Kademlia-Experimenten und künftigen Optimierungen der netDb"
slug: "netdb"
reviewStatus: "needs-review"
---

> **Hinweis:** Diese archivierte Diskussion umreißt historische Ansätze zur Netzwerkdatenbank (netDb). Siehe die [Hauptdokumentation zu netDb](/docs/specs/common-structures/) für Informationen zum aktuellen Verhalten und zu Leitlinien.

## Geschichte

Die netDb von I2P wird mithilfe eines einfachen floodfill-Algorithmus verteilt. Frühe Versionen behielten außerdem eine Implementierung von Kademlia-DHT (verteilte Hashtabelle) als Fallback bei; diese erwies sich jedoch als unzuverlässig und wurde in Version 0.6.1.20 vollständig deaktiviert. Das floodfill-Design leitet einen veröffentlichten Eintrag an einen teilnehmenden Router weiter, wartet auf eine Bestätigung und versucht es bei Bedarf mit anderen floodfill-Peers erneut. Floodfill-Peers verbreiten Stores (Speicher-Nachrichten) von Non-floodfill-Routern an alle anderen floodfill-Teilnehmer.

Ende 2009 wurden Kademlia-Abfragen teilweise wieder eingeführt, um die Speicherlast auf einzelnen floodfill-Routern zu verringern.

### Einführung in Floodfill

Floodfill erschien erstmals in Version 0.6.0.4, während Kademlia weiterhin als Fallback verfügbar blieb. Zu der Zeit erschwerten starker Paketverlust und eingeschränkte Routen es, Bestätigungen von den vier nächsten Peers zu erhalten, was häufig Dutzende redundanter store-Versuche (Speicheroperationen) erforderte. Der Wechsel zu einer floodfill-Teilmenge von außen erreichbaren routers bot eine pragmatische kurzfristige Lösung.

### Kademlia neu gedacht

Zu den in Erwägung gezogenen Alternativen gehörten:

- Betreiben der netDb als Kademlia DHT (verteilte Hashtabelle nach dem Kademlia-Verfahren), beschränkt auf erreichbare routers, die der Teilnahme zustimmen
- Beibehaltung des floodfill-Modells, jedoch Begrenzung der Teilnahme auf leistungsfähige routers und Überprüfung der Verteilung durch zufällige Stichproben

Der floodfill-Ansatz setzte sich durch, weil er einfacher zu implementieren war und die netDb nur Metadaten enthält, keine Nutzdaten der Benutzer. Die meisten Ziele veröffentlichen nie ein LeaseSet, da der Absender sein LeaseSet typischerweise in garlic messages (Garlic-Nachrichten) bündelt.

## Aktueller Stand (historische Perspektive)

Die netDb-Algorithmen sind auf die Bedürfnisse des Netzwerks optimiert und haben in der Vergangenheit problemlos einige hundert routers bewältigt. Frühe Schätzungen deuteten darauf hin, dass 3–5 floodfill routers ungefähr 10.000 Knoten unterstützen könnten.

### Aktualisierte Berechnungen (März 2008)

```
recvKBps = N * (L + 1) * (1 + F) * (1 + R) * S / T
```
Wo:

- `N`: Router im Netzwerk
- `L`: Durchschnittliche Anzahl der Client-Ziele pro Router (plus eins für die `RouterInfo`)
- `F`: Ausfallrate der Tunnel
- `R`: Zeitraum für den Neuaufbau von Tunneln als Anteil an der Lebensdauer eines Tunnels
- `S`: Durchschnittliche Größe eines netDb-Eintrags
- `T`: Lebensdauer eines Tunnels

Bei Verwendung von Werten aus dem Jahr 2008 (`N = 700`, `L = 0.5`, `F = 0.33`, `R = 0.5`, `S = 4 KB`, `T = 10 minutes`) ergibt sich:

```
recvKBps ≈ 700 * (0.5 + 1) * (1 + 0.33) * (1 + 0.5) * 4 KB / 10m ≈ 28 KBps
```
### Wird Kademlia (ein verteiltes Hash-Table-Protokoll) zurückkehren?

Entwickler diskutierten Anfang 2007 die Wiedereinführung von Kademlia. Der Konsens war, dass die floodfill-Kapazität bei Bedarf schrittweise ausgebaut werden könne, während Kademlia für die Basispopulation der router erhebliche zusätzliche Komplexität verursachte und den Ressourcenbedarf erhöhte. Der Fallback bleibt inaktiv, sofern die floodfill-Kapazität nicht mehr ausreicht.

### Floodfill-Kapazitätsplanung

Die automatische Aufnahme von routers der Bandbreitenklasse `O` in floodfill ist zwar verlockend, birgt jedoch das Risiko von Denial-of-Service-Szenarien, wenn böswillige Knoten sich dafür entscheiden, teilzunehmen. Historische Analysen deuteten darauf hin, dass die Begrenzung des floodfill-Pools (zum Beispiel 3–5 Peers, die ~10K routers verwalten) sicherer war. Vertrauenswürdige Betreiber oder automatische Heuristiken wurden eingesetzt, um eine ausreichende, zugleich kontrollierte floodfill-Menge aufrechtzuerhalten.

## Floodfill TODO (Historisch)

> Dieser Abschnitt wird für die Nachwelt beibehalten. Die netDb-Hauptseite verfolgt die aktuelle Roadmap und die Designüberlegungen.

Betriebsstörungen, wie etwa ein Zeitraum am 13. März 2008, in dem nur ein floodfill router verfügbar war, führten zu mehreren Verbesserungen, die in den Versionen 0.6.1.33 bis 0.7.x veröffentlicht wurden, darunter:

- Zufallsbasierte floodfill-Auswahl bei Suchen und Bevorzugung reaktionsschneller Peers
- Anzeige zusätzlicher floodfill-Metriken auf der router-Konsole auf der Seite "Profiles"
- Schrittweise Verringerungen der netDb-Eintragsgröße, um die floodfill-Bandbreitennutzung zu senken
- Automatisches opt-in (aktive Zustimmung) für eine Teilmenge von routers der Klasse `O`, basierend auf Leistung, die über Profildaten erfasst wurde
- Verbessertes Blocklisting, floodfill-Peer-Auswahl und Explorationsheuristiken

Weitere Ideen aus jener Zeit umfassten:

- Verwendung von `dbHistory`-Statistiken, um floodfill-Peers besser zu bewerten und auszuwählen
- Verbesserung des Retry-Verhaltens, um zu vermeiden, dass ausfallende Peers wiederholt kontaktiert werden
- Nutzung von Latenzmetriken und Integrations-Scores bei der Auswahl
- Schnelleres Erkennen und Reagieren auf ausfallende floodfill-Router
- Weitere Reduzierung des Ressourcenbedarfs bei Knoten mit hoher Bandbreite und floodfill-Knoten

Schon zum Zeitpunkt dieser Notizen galt das Netzwerk als widerstandsfähig und verfügte über eine Infrastruktur, um schnell auf feindliche floodfills oder gezielte Denial-of-Service-Angriffe gegen floodfill zu reagieren.

## Zusätzliche Hinweise

- Die router-Konsole legt seit Langem erweiterte Profildaten offen, um die Analyse der floodfill-Zuverlässigkeit zu unterstützen.
- Während frühere Kommentare über Kademlia oder alternative DHT-Schemata spekulierten, ist floodfill der primäre Algorithmus für Produktionsnetzwerke geblieben.
- Vorausschauende Forschung konzentrierte sich darauf, die Aufnahme in floodfill adaptiv zu gestalten und gleichzeitig Missbrauchsmöglichkeiten zu begrenzen.
