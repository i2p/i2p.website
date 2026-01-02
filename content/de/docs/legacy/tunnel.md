---
title: "Tunnel-Diskussion"
description: "Historische Untersuchung von tunnel-Padding, Fragmentierung und Aufbau-Strategien"
slug: "tunnel"
layout: "single"
lastUpdated: "2019-07"
accurateFor: "0.9.41"
reviewStatus: "needs-review"
---

> **Hinweis:** Dieses Archiv enthält spekulative Entwurfsarbeiten aus der Zeit vor I2P 0.9.41. Für die Implementierung für den Produktionseinsatz siehe die [tunnel-Dokumentation](/docs/specs/implementation/).

## Konfigurationsalternativen

Zu den in Betracht gezogenen Ideen für künftige tunnel-Stellschrauben gehörten:

- Ratenbegrenzungen für die Nachrichtenübermittlung
- Padding-Richtlinien (einschließlich chaff injection, Einbringen von Täuschdaten)
- Kontrollen der Tunnel-Lebensdauer
- Batch- und Warteschlangenstrategien für den Versand von Nutzlasten

Keine dieser Optionen wurde mit der Legacy-Implementierung ausgeliefert.

## Padding-Strategien

Besprochene potenzielle Padding-Ansätze:

- Kein Padding
- Padding mit zufälliger Länge
- Padding mit fester Länge
- Padding auf das nächste Kilobyte
- Padding auf Zweierpotenzen (`2^n` Bytes)

Frühe Messungen (Release 0.4) führten zur aktuellen, festen Größe von 1024 Byte für tunnel-Nachrichten. Höherstufige Garlic-Nachrichten können eigenes Padding hinzufügen.

## Fragmentierung

Um Tagging-Angriffe über die Nachrichtenlänge zu verhindern, haben tunnel-Nachrichten eine feste Größe von 1024 Bytes. Größere I2NP-Payloads werden vom Gateway fragmentiert; der Endpunkt setzt die Fragmente innerhalb eines kurzen Timeouts wieder zusammen. Router können Fragmente neu anordnen, um die Packeffizienz vor dem Senden zu maximieren.

## Zusätzliche Alternativen

### Tunnel-Verarbeitung zur Laufzeit anpassen

Drei Möglichkeiten wurden untersucht:

1. Erlauben, dass ein Zwischen-Hop einen tunnel vorübergehend beendet, indem ihm Zugriff auf entschlüsselte Nutzdaten gewährt wird.
2. Erlauben, dass teilnehmende router Nachrichten “remixen”, indem sie diese, bevor sie zum nächsten Hop fortfahren, durch einen ihrer eigenen ausgehenden tunnel senden.
3. Dem Ersteller des tunnel ermöglichen, den nächsten Hop eines Peers dynamisch neu festzulegen.

### Bidirektionale Tunnels

Die Verwendung separater eingehender und ausgehender tunnels begrenzt die Informationen, die eine einzelne Gruppe von Peers beobachten kann (z. B. eine GET-Anfrage gegenüber einer großen Antwort). Bidirektionale tunnels vereinfachen das Peer-Management, legen jedoch in beiden Richtungen gleichzeitig vollständige Verkehrsmuster offen. Unidirektionale tunnels blieben daher das bevorzugte Design.

### Rückkanäle und variable Größen

Die Zulassung variabler tunnel-Nachrichtengrößen würde verdeckte Kanäle zwischen kolludierenden Peers ermöglichen (z. B. durch Kodierung von Daten über ausgewählte Größen oder Häufigkeiten). Nachrichten fester Größe mindern dieses Risiko, allerdings zum Preis eines zusätzlichen Padding-Overheads.

## Alternativen für den Tunnel-Aufbau

Quelle: [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf)

### Veraltete „Parallele“ Build-Methode

Vor Version 0.6.1.10 wurden tunnel-Aufbauanfragen parallel an jeden Teilnehmer gesendet. Diese Methode ist auf der [alten tunnel-Seite](/docs/legacy/old-implementation/) dokumentiert.

### Teleskopischer Aufbau in einem Schritt (aktuelle Methode)

Der moderne Ansatz sendet build messages (Aufbau-Nachrichten) hop-by-hop durch den teilweise aufgebauten tunnel. Obwohl dies Tors telescoping (schrittweises Aufbauen) ähnelt, verringert das Weiterleiten der build messages durch exploratory tunnels (Erkundungstunnel) die Informationsleckage.

### „Interaktives“ Teleskopieren

Der Hop-für-Hop-Aufbau mit expliziten Round-Trips ermöglicht es Peers, Nachrichten zu zählen und ihre Position im tunnel abzuleiten, daher wurde dieser Ansatz verworfen.

### Nicht-exploratorische Management Tunnels

Ein Vorschlag war, einen separaten Pool von Management tunnels für Aufbauverkehr bereitzuhalten. Auch wenn dies partitionierten routers helfen könnte, wurde es bei ausreichender Netzwerkintegration als unnötig erachtet.

### Erkundungszustellung (veraltet)

Vor 0.6.1.10 wurden einzelne tunnel-Anfragen mit garlic encryption verschlüsselt und über Erkundungs-tunnel übermittelt; die Antworten kamen separat zurück. Diese Strategie wurde durch die aktuelle one-shot telescoping method (ein einmaliges, stufenweises Aufbauverfahren) ersetzt.

## Kernaussagen

- tunnel-Nachrichten fester Größe schützen trotz zusätzlichem Padding-Overhead vor größenbasierter Markierung und verdeckten Kanälen.
- Alternative Padding-, Fragmentierungs- und Aufbaustrategien wurden untersucht, aber angesichts der Anonymitätskompromisse nicht übernommen.
- Das tunnel-Design balanciert weiterhin Effizienz, Beobachtbarkeit und Widerstandsfähigkeit gegen Vorgänger- und Überlastungsangriffe.
