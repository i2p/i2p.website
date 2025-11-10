---
title: "I2P Entwicklungsplan"
description: "Aktuelle Entwicklungspläne und historische Meilensteine für das I2P-Netzwerk"
---

<div style="background: var(--color-bg-secondary); border-left: 4px solid var(--color-primary); padding: 1.5rem; margin-bottom: 2rem; border-radius: var(--radius-md);">

**I2P folgt einem inkrementellen Entwicklungsmodell** mit Veröffentlichungen etwa alle 13 Wochen. Dieser Entwicklungsplan umfasst Desktop- und Android-Java-Veröffentlichungen in einem einzigen, stabilen Veröffentlichungsweg.

**Zuletzt aktualisiert:** August 2025

</div>

## 🎯 Bevorstehende Veröffentlichungen

<div style="border-left: 3px solid var(--color-accent); padding-left: 1.5rem; margin-bottom: 2rem;">

### Version 2.11.0
<div style="display: inline-block; background: var(--color-accent); color: white; padding: 0.25rem 0.75rem; border-radius: var(--radius-md); font-size: 0.875rem; margin-bottom: 1rem;">
Ziel: Anfang Dezember 2025
</div>

- Hybrid PQ MLKEM Ratchet final, standardmäßig aktiviert (Prop. 169)
- Jetty 12, erfordert Java 17+
- Weiterarbeit an PQ (Transports) (Prop. 169)
- I2CP Lookups-Unterstützung für LS-Servicerecord-Parameter (Prop. 167)
- Per-Tunnel-Drosselung
- Prometheus-freundliches Statistik-Subsystem
- SAM-Unterstützung für Datagramm 2/3

</div>

---

## 📦 Kürzliche Veröffentlichungen

### Veröffentlichungen 2025

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-success);">

**Version 2.10.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— Veröffentlicht am 8. September 2025</span>

- i2psnark UDP-Tracker-Unterstützung (Prop. 160)
- I2CP LS Servicerecord-Parameter (teilweise) (Prop. 167)
- I2CP asynchrone Lookup-API
- Hybrid PQ MLKEM Ratchet Beta (Prop. 169)
- Weiterarbeit an PQ (Transports) (Prop. 169)
- Tunnelkonstruktions-Bandbreitenparameter (Prop. 168) Teil 2 (Bearbeitung)
- Weiterarbeit an der Per-Tunnel-Drosselung
- Entfernen von nicht genutztem ElGamal-Transportcode
- Entfernen von altem SSU2-"Active Throttle"-Code
- Entfernen alter Statistik-Logging-Unterstützung
- Bereinigung des Statistik-/Graph-Subsystems
- Verbesserungen und Fixes im versteckten Modus

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-success);">

**Version 2.9.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— Veröffentlicht am 2. Juni 2025</span>

- Netdb-Karte
- Implementierung von Datagramm2, Datagramm3 (Prop. 163)
- Beginn der Arbeit an LS Servicerecord-Parameter (Prop. 167)
- Beginn der Arbeit an PQ (Prop. 169)
- Weiterarbeit an der Per-Tunnel-Drosselung
- Tunnelkonstruktions-Bandbreitenparameter (Prop. 168) Teil 1 (Senden)
- Verwendung von /dev/random für PRNG standardmäßig unter Linux
- Entfernen von redundantem LS-Rendercode
- Anzeige des Changelogs in HTML
- Reduzierung der HTTP-Server-Thread-Nutzung
- Behebung der automatischen Floodfill-Registrierung
- Wrapper-Update auf 3.5.60

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-success);">

**Version 2.8.2** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— Veröffentlicht am 29. März 2025</span>

- Behebung des SHA256-Korruptionsfehlers

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-success);">

**Version 2.8.1** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— Veröffentlicht am 17. März 2025</span>

- Behebung der Installationsprobleme bei Java 21+
- Behebung des "Loopback"-Fehlers
- Behebung von Tunnel-Tests für ausgehende Client-Tunnel
- Behebung der Installation in Pfade mit Leerzeichen
- Aktualisierung veralteter Docker-Container und Container-Bibliotheken
- Konsolenbenachrichtigungsblasen
- SusiDNS-Sortierung nach neuesten Einträgen
- Verwendung des SHA256-Pools in Noise
- Verbesserungen und Fixes für das Dunkelthema der Konsole
- Unterstützung für .i2p.alt

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-success);">

**Version 2.8.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— Veröffentlicht am 3. Februar 2025</span>

- Verbesserungen beim Veröffentlichen von RouterInfo
- Verbesserung der SSU2-ACK-Effizienz
- Verbesserung der SSU2-Behandlung von doppelten Relay-Nachrichten
- Schnellere / variable Lookup-Timeouts
- Verbesserungen der LS-Ablaufzeiten
- Änderung der symmetrischen NAT-Kapazität
- Durchsetzung von POST in mehr Formularen
- Verbesserungen des SusiDNS-Dunkelthemas
- Bereinigungen von Bandbreitentests
- Neue Gan-Chinesisch-Übersetzung
- Hinzufügen der kurdischen UI-Option
- Neuer Jammy-Build
- Izpack 5.2.3
- rrd4j 3.10

</div>

<div style="margin: 3rem 0; padding: 1rem 0; border-top: 2px solid var(--color-border); border-bottom: 2px solid var(--color-border);">
  <h3 style="margin: 0; color: var(--color-primary);">📅 Veröffentlichungen 2024</h3>
</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**Version 2.7.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 8. Oktober 2024</span>

- i2ptunnel-HTTP-Server reduziert Thread-Nutzung
- Generische UDP-Tunnel in I2PTunnel
- Browser-Proxy in I2PTunnel
- Website-Migration
- Behebung für Tunnel, die gelb werden
- Refaktorisierung der Konsole /netdb

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**Version 2.6.1** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 6. August 2024</span>

- Behebung von iframe-Größenproblemen in der Konsole
- Umwandlung von Grafiken in SVG
- Bündelungsübersetzungs-Statusbericht

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**Version 2.6.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 19. Juli 2024</span>

- Reduzierung des Netdb-Speicherverbrauchs
- Entfernen von SSU1-Code
- Behebung von i2psnark-Temp-Datei-Lecks und -Staus
- Effizienteres PEX in i2psnark
- JS-Aktualisierung der Konsolendiagramme
- Verbesserungen beim Rendering von Grafiken
- Susimail JS-Suche
- Effizientere Nachrichtenverarbeitung am OBEP
- Effizientere lokale Ziel-I2CP-Lookups
- Behebung von JS-Variablensichtbarkeitsproblemen

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**Version 2.5.2** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 15. Mai 2024</span>

- Behebung der HTTP-Kürzung
- Veröffentlichung der G-Fähigkeit, wenn symmetrisches NAT erkannt wird
- Update auf rrd4j 3.9.1-Vorschau

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**Version 2.5.1** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 6. Mai 2024</span>

- NetDB-DDoS-Minderungen
- Tor-Blockliste
- Susimail-Korrekturen und -Suche
- Weiteres Entfernen von SSU1-Code
- Update auf Tomcat 9.0.88

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**Version 2.5.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 8. April 2024</span>

- Verbesserungen des Konsolen-Iframes
- Neugestaltung des i2psnark-Bandbreitenbegrenzers
- JavaScript-Drag-and-Drop für i2psnark und susimail
- Verbesserungen beim SSL-Fehlerhandling von i2ptunnel
- Unterstützung persistenter HTTP-Verbindung für i2ptunnel
- Beginn des Entfernens von SSU1-Code
- Verbesserungen beim SSU2-Relay-Tag-Anforderungs-Handling
- Fixes für SSU2-Peer-Tests
- Verbesserungen bei Susimail (Laden, Markdown, HTML-E-Mail-Unterstützung)
- Anpassungen der Tunnel-Peer-Auswahl
- Update von RRD4J auf 3.9
- Update von gradlew auf 8.5

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**Version 2.4.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 18. Dezember 2023</span>

- NetDB-Kontext-Management/Segmentierte NetDB
- Behandlung von Überlastungskapazitäten durch Depriorisierung überlasteter Router
- Wiederbelebung der Android-Hilfsbibliothek
- Lokale Torrent-Dateiauswahl in i2psnark
- Fixes für NetDB-Lookup-Handler
- Deaktivierung von SSU1
- Ban von Routern, die in der Zukunft veröffentlichen
- SAM-Fixes
- Susimail-Fixes
- UPnP-Fixes

</div>

---

### Veröffentlichungen 2023-2022

<details>
<summary>Klicken Sie, um die Veröffentlichungen 2023-2022 anzuzeigen</summary>

**Version 2.3.0** — Veröffentlicht am 28. Juni 2023

- Verbesserungen bei der Tunnel-Peer-Auswahl
- Benutzerkonfigurierbare Blockliste-Ablauf
- Drosselung schneller Lookup-Schübe aus derselben Quelle
- Korrektur von Replay-Erkennungs-Informationsleck
- Fixes in der NetDB für multihomed LeaseSets
- Fixes in der NetDB für LeaseSets, die als Antwort empfangen werden, bevor sie als Store empfangen werden

**Version 2.2.1** — Veröffentlicht am 12. April 2023

- Verpackungs-Fixes

**Version 2.2.0** — Veröffentlicht am 13. März 2023

- Verbesserungen bei der Tunnel-Peer-Auswahl
- Behebung des Streaming-Replay-Fehlers

**Version 2.1.0** — Veröffentlicht am 10. Januar 2023

- SSU2-Fixes
- Tunnel-Konstruktions-Überlastungs-Fixes
- Fixes bei der Erkennung von SSU-Peer-Tests und symmetrischem NAT
- Behebung von fehlerhaften LS2-verschlüsselten LeaseSets
- Option zur Deaktivierung von SSU 1 (vorläufig)
- Komprimierbares Padding (Vorschlag 161)
- Neuer Status-Tab für Konsolen-Peers
- Hinzufügen von Torsocks-Unterstützung zum SOCKS-Proxy und anderen SOCKS-Verbesserungen und -Fixes

**Version 2.0.0** — Veröffentlicht am 21. November 2022

- Migration von SSU2-Verbindungen
- Sofortige ACKs bei SSU2
- Standardmäßige Aktivierung von SSU2
- SHA-256-Digest-Proxy-Authentifizierung in i2ptunnel
- Aktualisieren des Android-Build-Prozesses für moderne AGP
- Unterstützung für die automatische Konfiguration des I2P-Browsers auf verschiedenen Plattformen (Desktop)

**Version 1.9.0** — Veröffentlicht am 22. August 2022

- Implementierung von SSU2-Peer-Test und Relay
- SSU2-Fixes
- Verbesserungen bei SSU-MTU/PMTU
- Aktivierung von SSU2 für einen kleinen Teil der Router
- Hinzufügen eines Deadlock-Detektors
- Weitere Fixes für Zertifikatimport
- Behebung des Neustarts von i2psnark DHT nach Router-Neustart

**Version 1.8.0** — Veröffentlicht am 23. Mai 2022

- Fixes und Verbesserungen bei Router-Familien
- Fixes beim Soft-Restart
- Fixes und Leistungsverbesserungen bei SSU
- Eigenständige Fixes und Verbesserungen bei I2PSnark
- Vermeidung von Sybil-Bestrafungen für vertrauenswürdige Familien
- Reduzierung des Tunnel-Konstruktions-Antwort-Timeouts
- UPnP-Fixes
- Entfernen von BOB-Source
- Zertifikatimport-Fixes
- Tomcat 9.0.62
- Refactoring zur Unterstützung von SSU2 (Vorschlag 159)
- Erste Implementierung des SSU2-Basisprotokolls (Vorschlag 159)
- SAM-Autorisierungs-Popup für Android-Apps
- Verbesserung der Unterstützung für benutzerdefinierte Verzeichnis-Installationen in i2p.firefox

**Version 1.7.0** — Veröffentlicht am 21. Februar 2022

- Entfernen von BOB
- Neuer i2psnark-Torrent-Editor
- Eigenständige Fixes und Verbesserungen bei i2psnark
- Verbesserungen bei der NetDB-Zuverlässigkeit
- Hinzufügen von Popup-Nachrichten im System-Tray
- Verbesserungen der NTCP2-Leistung
- Entfernen des ausgehenden Tunnels, wenn der erste Hop fehlschlägt
- Fallback auf Exploratory für Tunnel-Konstruktions-Antwort nach wiederholtem Scheitern von Client-Tunneln
- Wiederherstellen von Tunnel-selben-IP-Einschränkungen
- Refaktorisierung der i2ptunnel-UDP-Unterstützung für I2CP-Ports
- Weitere Arbeiten an SSU2, Start der Implementierung (Vorschlag 159)
- Erstellung eines Debian/Ubuntu-Pakets des I2P-Browser-Profils
- Erstellung eines Plugins des I2P-Browser-Profils
- Dokumentation von I2P für Android-Anwendungen
- Verbesserungen bei i2pcontrol
- Verbesserungen der Plugin-Unterstützung
- Neues lokales Outproxy-Plugin
- Unterstützung von IRCv3-Nachrichtentags

</details>

---

### Veröffentlichungen 2021

<details>
<summary>Klicken Sie, um die Veröffentlichungen 2021 anzuzeigen</summary>

**Version 1.6.1** — Veröffentlicht am 29. November 2021

- Beschleunigung der Rekeying-Router zu ECIES
- Verbesserungen der SSU-Leistung
- Verbesserung der SSU-Peer-Test-Sicherheit
- Hinzufügen der
