---
title: "Transportschicht"
description: "Die I2P-Transportschicht verstehen - Punkt-zu-Punkt-Kommunikationsmethoden zwischen routers, einschließlich NTCP2 und SSU2"
slug: "transport"
lastUpdated: "2025-03"
accurateFor: "2.10.0"
---

---

## 1. Übersicht

Ein **Transport** in I2P ist eine Methode für die direkte Punkt-zu-Punkt-Kommunikation zwischen routers. Diese Mechanismen gewährleisten Vertraulichkeit und Integrität und überprüfen dabei die router-Authentifizierung.

Jeder Transport arbeitet unter Verwendung von Verbindungsparadigmen mit Authentifizierung, Flusskontrolle, Bestätigungen und Wiederübertragungsfunktionen.

---

## 2. Aktuelle Transportprotokolle

I2P unterstützt derzeit zwei primäre Transportprotokolle:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Transport</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NTCP2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TCP</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise-based TCP transport with modern encryption (as of 0.9.36)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UDP</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Secure Semireliable UDP with modern encryption (as of 0.9.56)</td>
    </tr>
  </tbody>
</table>
### 2.1 Veraltete Transportprotokolle (abgekündigt)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Transport</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NTCP</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TCP</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Replaced by NTCP2; removed in 0.9.62</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UDP</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Replaced by SSU2; removed in 0.9.62</td>
    </tr>
  </tbody>
</table>
---

## 3. Transportdienste

Das Transport-Subsystem stellt die folgenden Dienste bereit:

### 3.1 Nachrichtenübermittlung

- Zuverlässige [I2NP](/docs/specs/i2np/) Nachrichtenübermittlung (Transportprotokolle übernehmen ausschließlich den I2NP‑Nachrichtenverkehr)
- In-Order-Zustellung ist **NICHT garantiert** universell
- Prioritätsbasierte Nachrichtenwarteschlangen

### 3.2 Verbindungsverwaltung

- Aufbau und Schließung von Verbindungen
- Verwaltung von Verbindungsobergrenzen mit Durchsetzung von Schwellenwerten
- Statusverfolgung pro Peer
- Automatisierte und manuelle Durchsetzung der Peer-Sperrliste

### 3.3 Netzwerkkonfiguration

- Mehrere router-Adressen pro Transport (IPv4- und IPv6-Unterstützung seit v0.9.8)
- Öffnen von UPnP-Firewall-Ports
- Unterstützung für NAT/Firewall-Traversal
- Lokale IP-Erkennung über mehrere Methoden

### 3.4 Sicherheit

- Verschlüsselung für Punkt-zu-Punkt-Kommunikation
- Validierung von IP-Adressen gemäß lokalen Regeln
- Bestimmung des Zeitkonsenses (NTP-Backup)

### 3.5 Bandbreitenverwaltung

- Eingehende und ausgehende Bandbreitenlimits
- Optimale Transportauswahl für ausgehende Nachrichten

---

## 4. Transportadressen

Das Subsystem verwaltet eine Liste der Router-Kontaktpunkte:

- Transportmethode (NTCP2, SSU2)
- IP-Adresse
- Portnummer
- Optionale Parameter

Mehrere Adressen pro Transportmethode sind möglich.

### 4.1 Häufige Adresskonfigurationen

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Configuration</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Hidden</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Routers with no published addresses</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Firewalled</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Routers publishing SSU2 addresses with "introducer" peer lists for NAT traversal</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Unrestricted</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Routers advertising both NTCP2 and SSU2 addresses on IPv4 and/or IPv6</td>
    </tr>
  </tbody>
</table>
---

## 5. Auswahl des Transports

Das System wählt Transporte für [I2NP messages](/docs/specs/i2np/) unabhängig von Protokollen höherer Schichten aus. Die Auswahl verwendet ein **Bietsystem**, bei dem jeder Transport Gebote abgibt, wobei der niedrigste Wert gewinnt.

### 5.1 Faktoren zur Gebotsbestimmung

- Einstellungen für Transportpräferenzen
- Bestehende Peer-Verbindungen
- Aktuelle gegenüber Schwellenwerten für die Anzahl der Verbindungen
- Verlauf der jüngsten Verbindungsversuche
- Beschränkungen der Nachrichtengröße
- Transportfähigkeiten der RouterInfo des Peers
- Direktheit der Verbindung (direkt versus introducer-abhängig)
- Vom Peer veröffentlichte Transportpräferenzen

In der Regel unterhalten zwei routers gleichzeitig Verbindungen über genau ein Transportprotokoll; gleichzeitige Verbindungen über mehrere Transportprotokolle sind jedoch möglich.

---

## 6. NTCP2

**NTCP2** (Neues Transportprotokoll 2) ist der moderne, TCP-basierte Transport für I2P, der in Version 0.9.36 eingeführt wurde.

### 6.1 Hauptfunktionen

- Basiert auf dem **Noise Protocol Framework** (Noise_XK-Pattern)
- Verwendet **X25519** für den Schlüsselaustausch
- Verwendet **ChaCha20/Poly1305** für authentifizierte Verschlüsselung
- Verwendet **BLAKE2s** für das Hashing
- Protokollverschleierung zur Abwehr von DPI (Deep Packet Inspection)
- Optionales Padding zur Abwehr von Verkehrsanalysen

### 6.2 Verbindungsaufbau

1. **Sitzungsanfrage** (Alice → Bob): Ephemerer X25519-Schlüssel + verschlüsselte Nutzlast
2. **Sitzung erstellt** (Bob → Alice): Ephemerer Schlüssel + verschlüsselte Bestätigung
3. **Sitzung bestätigt** (Alice → Bob): Abschließender Handshake mit RouterInfo

Alle nachfolgenden Daten werden mit Sitzungsschlüsseln verschlüsselt, die aus dem Handshake abgeleitet werden.

Ausführliche Informationen finden Sie in der [NTCP2-Spezifikation](/docs/specs/ntcp2/).

---

## 7. SSU2

**SSU2** (Secure Semireliable UDP 2) ist das moderne, UDP-basierte Transportprotokoll für I2P und wurde in Version 0.9.56 eingeführt.

### 7.1 Hauptfunktionen

- Basiert auf dem **Noise Protocol Framework** (Noise_XK-Muster)
- Verwendet **X25519** für den Schlüsselaustausch
- Verwendet **ChaCha20/Poly1305** für authentifizierte Verschlüsselung
- Semizuverlässige Übertragung mit selektiven Bestätigungen
- NAT-Traversal über Hole Punching und Relay/Einführung
- Unterstützung für Verbindungsmigration
- Path-MTU-Erkennung

### 7.2 Vorteile gegenüber SSU (veraltet)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">SSU (Legacy)</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">SSU2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ElGamal + AES</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519 + ChaCha20/Poly1305</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Header encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Partial</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Full (ChaCha20)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connection ID</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fixed</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypted, rotatable</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NAT traversal</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Basic introduction</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Enhanced hole punching + relay</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Obfuscation</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Minimal</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Improved (variable padding)</td>
    </tr>
  </tbody>
</table>
Alle Einzelheiten finden Sie in der [SSU2-Spezifikation](/docs/specs/ssu2/).

---

## 8. NAT-Traversal

Beide Transportprotokolle unterstützen NAT-Traversal, damit routers hinter einer Firewall am Netzwerk teilnehmen können.

### 8.1 SSU2 Einführung

Wenn ein router eingehende Verbindungen nicht direkt empfangen kann:

1. Router veröffentlicht **introducer**-Adressen (Vermittler) in seiner RouterInfo
2. Der sich verbindende Peer sendet eine Einführungsanfrage an den introducer
3. Der introducer leitet Verbindungsinformationen an den durch eine Firewall geschützten Router weiter
4. Der durch eine Firewall geschützte Router initiiert eine ausgehende Verbindung (hole punch; NAT-Lochstanzen)
5. Direkte Kommunikation hergestellt

### 8.2 NTCP2 und Firewalls

NTCP2 erfordert eingehende TCP-Konnektivität. Router hinter NAT können:

- UPnP verwenden, um Ports automatisch zu öffnen
- Portweiterleitung manuell konfigurieren
- Für eingehende Verbindungen SSU2 verwenden und für ausgehende NTCP2

---

## 9. Protokollverschleierung

Beide modernen Transportprotokolle integrieren Verschleierungsfunktionen:

- **Zufälliges Padding** in Handshake-Nachrichten
- **Verschlüsselte Header**, die keine Protokollsignaturen preisgeben
- **Nachrichten variabler Länge** zur Abwehr von Traffic-Analyse
- **Keine festen Muster** beim Verbindungsaufbau

> **Hinweis**: Verschleierung auf der Transportschicht ergänzt, ersetzt aber nicht die durch die tunnel-Architektur von I2P bereitgestellte Anonymität.

---

## 10. Zukünftige Entwicklungen

Geplante Forschungsarbeiten und Verbesserungen umfassen:

- **Pluggable Transports (austauschbare Verschleierungsprotokolle)** – Tor-kompatible Verschleierungs-Plugins
- **QUIC-basierter Transport** – Untersuchung der Vorteile des QUIC-Protokolls
- **Optimierung der Verbindungsgrenzen** – Forschung zu optimalen Grenzen für Peer-Verbindungen
- **Erweiterte Padding-Strategien** – Verbesserte Widerstandsfähigkeit gegen Verkehrsanalyse

---

## 11. Referenzen

- [NTCP2-Spezifikation](/docs/specs/ntcp2/) – Noise-basiertes TCP-Transportprotokoll
- [SSU2-Spezifikation](/docs/specs/ssu2/) – Sicheres halbzuverlässiges UDP 2
- [I2NP-Spezifikation](/docs/specs/i2np/) – Nachrichten des I2P Network Protocol
- [Gemeinsame Strukturen](/docs/specs/common-structures/) – RouterInfo- und Adressstrukturen
- [Historische NTCP-Diskussion](/docs/ntcp/) – Entwicklungsgeschichte des Legacy-Transports
- [Legacy-SSU-Dokumentation](/docs/legacy/ssu/) – Ursprüngliche SSU-Spezifikation (veraltet)
