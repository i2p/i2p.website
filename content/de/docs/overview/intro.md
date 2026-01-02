---
title: "Einführung in I2P"
description: "Eine weniger technische Einführung in das anonyme I2P-Netzwerk"
slug: "intro"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "needs-review"
---

## Was ist I2P?

Das Invisible Internet Project (I2P) ist eine anonyme Netzwerkschicht, die zensurresistente Peer-to-Peer-Kommunikation ermöglicht. Anonyme Verbindungen werden durch Verschlüsselung des Nutzerverkehrs und dessen Weiterleitung über ein verteiltes Netzwerk erreicht, das von Freiwilligen weltweit betrieben wird.

## Hauptmerkmale

### Anonymity

I2P verbirgt sowohl Absender als auch Empfänger von Nachrichten. Anders als bei herkömmlichen Internetverbindungen, bei denen Ihre IP-Adresse für Websites und Dienste sichtbar ist, verwendet I2P mehrere Verschlüsselungs- und Routing-Ebenen, um Ihre Identität privat zu halten.

### Decentralization

Es gibt keine zentrale Autorität in I2P. Das Netzwerk wird von Freiwilligen betrieben, die Bandbreite und Rechenressourcen zur Verfügung stellen. Dies macht es resistent gegen Zensur und einzelne Fehlerquellen.

### Anonymität

Sämtlicher Datenverkehr innerhalb von I2P ist Ende-zu-Ende verschlüsselt. Nachrichten werden mehrfach verschlüsselt, während sie durch das Netzwerk geleitet werden, ähnlich wie bei Tor, jedoch mit wichtigen Unterschieden in der Implementierung.

## How It Works

### Dezentralisierung

I2P verwendet „Tunnels", um Datenverkehr zu routen. Wenn Sie Daten senden oder empfangen:

1. Dein Router erstellt einen ausgehenden Tunnel (zum Senden)
2. Dein Router erstellt einen eingehenden Tunnel (zum Empfangen)
3. Nachrichten werden verschlüsselt und über mehrere Router gesendet
4. Jeder Router kennt nur den vorherigen und nächsten Hop, nicht den vollständigen Pfad

### Ende-zu-Ende-Verschlüsselung

I2P verbessert das traditionelle Onion Routing durch "Garlic Routing":

- Mehrere Nachrichten können zusammengebündelt werden (wie Zehen in einer Knoblauchknolle)
- Dies bietet bessere Leistung und zusätzliche Anonymität
- Erschwert die Verkehrsanalyse

### Network Database

I2P verwaltet eine verteilte Netzwerkdatenbank, die Folgendes enthält:

- Router-Informationen
- Zieladressen (ähnlich wie .i2p-Websites)
- Verschlüsselte Routing-Daten

## Common Use Cases

### Tunnel

Hosten oder besuchen Sie Websites, die auf `.i2p` enden - diese sind nur innerhalb des I2P-Netzwerks zugänglich und bieten sowohl für Hosts als auch für Besucher starke Anonymitätsgarantien.

### Garlic Routing

Teilen Sie Dateien anonym über BitTorrent auf I2P. Viele Torrent-Anwendungen haben integrierte I2P-Unterstützung.

### Netzwerkdatenbank

Senden und empfangen Sie anonyme E-Mails mit I2P-Bote oder anderen E-Mail-Anwendungen, die für I2P entwickelt wurden.

### Messaging

Nutzen Sie IRC, Instant Messaging oder andere Kommunikationswerkzeuge privat über das I2P-Netzwerk.

## Getting Started

Bereit, I2P auszuprobieren? Besuchen Sie unsere [Download-Seite](/downloads), um I2P auf Ihrem System zu installieren.

Für weitere technische Details siehe die [Technische Einführung](/docs/overview/tech-intro) oder erkunde die vollständige [Dokumentation](/docs).

## Wie es funktioniert

- [Technische Einführung](/docs/overview/tech-intro) - Tiefergehende technische Konzepte
- [Bedrohungsmodell](/docs/overview/threat-model) - Das Sicherheitsmodell von I2P verstehen
- [Vergleich mit Tor](/docs/overview/comparison) - Wie sich I2P von Tor unterscheidet
- [Kryptographie](/docs/specs/cryptography) - Details zu den kryptographischen Algorithmen von I2P
