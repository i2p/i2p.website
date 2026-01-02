---
title: "I2PTunnel"
description: "Werkzeug zur Schnittstelle und Bereitstellung von Diensten auf I2P"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Übersicht

I2PTunnel ist eine zentrale I2P-Komponente für die Kommunikation mit dem I2P-Netzwerk und die Bereitstellung von Diensten darauf. Es ermöglicht TCP-basierten und Media-Streaming-Anwendungen, anonym durch Tunnel-Abstraktion zu arbeiten. Das Ziel eines tunnels kann durch einen [Hostnamen](/docs/overview/naming), [Base32](/docs/overview/naming#base32) oder einen vollständigen Zielschlüssel (destination key) definiert werden.

Jeder eingerichtete tunnel lauscht lokal (z.B. `localhost:port`) und verbindet sich intern mit I2P-Zielen. Um einen Dienst bereitzustellen, erstellen Sie einen tunnel, der auf die gewünschte IP und den gewünschten Port verweist. Ein entsprechender I2P-Zielschlüssel wird generiert, wodurch der Dienst im I2P-Netzwerk global erreichbar wird. Die I2PTunnel-Weboberfläche ist verfügbar unter [I2P Router Tunnel Manager](http://localhost:7657/i2ptunnel/).

---

## Standarddienste

### Server-Tunnel

- **I2P Webserver** – Ein Tunnel zu einem Jetty-Webserver unter [localhost:7658](http://localhost:7658) für einfaches Hosting auf I2P.  
  - **Unix:** `$HOME/.i2p/eepsite/docroot`  
  - **Windows:** `%LOCALAPPDATA%\I2P\I2P Site\docroot` → `C:\Users\<username>\AppData\Local\I2P\I2P Site\docroot`

### Client-Tunnel

- **I2P HTTP Proxy** – `localhost:4444` – Wird zum Durchsuchen von I2P und dem Internet über Outproxies verwendet.  
- **I2P HTTPS Proxy** – `localhost:4445` – Sichere Variante des HTTP-Proxys.  
- **Irc2P** – `localhost:6668` – Standard-tunnel für das anonyme IRC-Netzwerk.  
- **Git SSH (gitssh.idk.i2p)** – `localhost:7670` – Client-tunnel für SSH-Zugriff auf Repositorys.  
- **Postman SMTP** – `localhost:7659` – Client-tunnel für ausgehende E-Mails.  
- **Postman POP3** – `localhost:7660` – Client-tunnel für eingehende E-Mails.

> Hinweis: Nur der I2P-Webserver ist ein standardmäßiger **server tunnel**; alle anderen sind Client-Tunnel, die sich mit externen I2P-Diensten verbinden.

---

## Konfiguration

Die I2PTunnel-Konfigurationsspezifikation ist unter [/spec/configuration](/docs/specs/configuration/) dokumentiert.

---

## Client-Modi

### Standard

Öffnet einen lokalen TCP-Port, der sich mit einem Dienst auf einer I2P-Destination verbindet. Unterstützt mehrere durch Kommas getrennte Destination-Einträge für Redundanz.

### HTTP

Ein Proxy-Tunnel für HTTP/HTTPS-Anfragen. Unterstützt lokale und entfernte Outproxies, Header-Entfernung, Caching, Authentifizierung und transparente Kompression.

**Datenschutzmaßnahmen:**   - Entfernt Header: `Accept-*`, `Referer`, `Via`, `From`   - Ersetzt Host-Header durch Base32-Zieladressen   - Erzwingt RFC-konformes Hop-by-Hop-Stripping   - Fügt Unterstützung für transparente Dekomprimierung hinzu   - Bietet interne Fehlerseiten und lokalisierte Antworten

**Komprimierungsverhalten:**   - Anfragen können den benutzerdefinierten Header `X-Accept-Encoding: x-i2p-gzip` verwenden   - Antworten mit `Content-Encoding: x-i2p-gzip` werden transparent dekomprimiert   - Komprimierung wird anhand von MIME-Typ und Antwortlänge für Effizienz bewertet

**Persistenz (neu seit 2.5.0):** HTTP Keepalive und persistente Verbindungen werden jetzt für I2P-gehostete Dienste über den Hidden Services Manager unterstützt. Dies reduziert die Latenz und den Verbindungsoverhead, ermöglicht aber noch keine vollständige RFC 2616-konforme persistente Sockets über alle Hops hinweg.

**Pipelining:**   Bleibt nicht unterstützt und unnötig; moderne Browser haben es als veraltet markiert.

**User-Agent-Verhalten:**   - **Outproxy:** Verwendet einen aktuellen Firefox ESR User-Agent.   - **Intern:** `MYOB/6.66 (AN/ON)` für konsistente Anonymität.

### IRC-Client

Verbindet sich mit I2P-basierten IRC-Servern. Erlaubt eine sichere Teilmenge von Befehlen und filtert Identifikatoren zum Schutz der Privatsphäre.

### SOCKS 4/4a/5

Bietet SOCKS-Proxy-Funktionalität für TCP-Verbindungen. UDP ist in Java I2P nicht implementiert (nur in i2pd).

### CONNECT

Implementiert HTTP-`CONNECT`-Tunneling für SSL/TLS-Verbindungen.

### Streamr

Ermöglicht UDP-ähnliches Streaming über TCP-basierte Kapselung. Unterstützt Media-Streaming, wenn es mit einem entsprechenden Streamr-Server-Tunnel kombiniert wird.

![I2PTunnel Streamr Diagramm](/images/I2PTunnel-streamr.png)

---

## Server-Modi

### Standard-Server

Erstellt ein TCP-Ziel, das einer lokalen IP:Port zugeordnet ist.

### HTTP-Server

Erstellt eine Destination, die mit einem lokalen Webserver kommuniziert. Unterstützt Komprimierung (`x-i2p-gzip`), Header-Entfernung und DDoS-Schutz. Profitiert nun von **Unterstützung für persistente Verbindungen** (v2.5.0+) und **Thread-Pool-Optimierung** (v2.7.0–2.9.0).

### HTTP Bidirektional

**Veraltet** – Noch funktionsfähig, aber nicht empfohlen. Fungiert sowohl als HTTP-Server als auch als Client ohne Outproxying. Wird hauptsächlich für diagnostische Loopback-Tests verwendet.

### IRC-Server

Erstellt eine gefilterte Destination für IRC-Dienste, die Client-Destination-Schlüssel als Hostnamen übergibt.

### Streamr-Server

Kombiniert mit einem Streamr-Client-Tunnel zur Verarbeitung von UDP-ähnlichen Datenströmen über I2P.

---

## Neue Funktionen (2.4.0–2.10.0)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Introduced</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Summary</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Keepalive/Persistent Connections</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.5.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HTTP tunnels now support persistent sockets for I2P-hosted services, improving performance.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Thread Pooling Optimization</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.7.0-2.9.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reduced CPU overhead and latency by improving thread management.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Post-Quantum Encryption (ML-KEM)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Optional hybrid X25519+ML-KEM encryption to resist future quantum attacks.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NetDB Segmentation</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.4.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Isolates I2PTunnel contexts for improved security and privacy.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU1 Removal / SSU2 Adoption</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.4.0-2.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Upgraded transport layer; transparent to users.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2P-over-Tor Blocking</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Prevents inefficient and unstable I2P-over-Tor routing.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Browser Proxy (Proposal 166)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.7.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Introduced identity-aware proxy mode; details pending confirmation.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Java 17 Requirement (upcoming)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.11.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Future release will require Java 17+.</td>
    </tr>
  </tbody>
</table>
---

## Sicherheitsfunktionen

- **Header-Entfernung** für Anonymität (Accept, Referer, From, Via)
- **User-Agent-Randomisierung** abhängig von in/outproxy
- **POST-Ratenbegrenzung** und **Slowloris-Schutz**
- **Verbindungsdrosselung** in Streaming-Subsystemen
- **Behandlung von Netzwerküberlastung** auf Tunnel-Ebene
- **NetDB-Isolierung** zur Verhinderung anwendungsübergreifender Lecks

---

## Technische Details

- Standard-Zielschlüsselgröße: 516 Bytes (kann bei erweiterten LS2-Zertifikaten überschritten werden)
- Base32-Adressen: `{52–56+ Zeichen}.b32.i2p`
- Server-Tunnel bleiben kompatibel mit sowohl Java I2P als auch i2pd
- Veraltete Funktion: nur `httpbidirserver`; keine Entfernungen seit 0.9.59
- Verifizierte korrekte Standard-Ports und Dokumentenstammverzeichnisse für alle Plattformen

---

## Zusammenfassung

I2PTunnel bleibt das Rückgrat der Anwendungsintegration mit I2P. Zwischen Version 0.9.59 und 2.10.0 erhielt es Unterstützung für persistente Verbindungen, Post-Quanten-Verschlüsselung und umfangreiche Threading-Verbesserungen. Die meisten Konfigurationen bleiben kompatibel, aber Entwickler sollten ihre Setups überprüfen, um die Einhaltung moderner Transport- und Sicherheitsstandards sicherzustellen.
