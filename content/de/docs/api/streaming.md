---
title: "Streaming-Protokoll"
description: "TCP-ähnlicher Transport, der von den meisten I2P-Anwendungen verwendet wird"
slug: "streaming"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Überblick

Die **I2P Streaming Library** bietet zuverlässigen, geordneten und authentifizierten Transport über die Nachrichtenschicht von I2P, ähnlich wie **TCP über IP**. Sie befindet sich oberhalb des [I2CP-Protokolls](/docs/specs/i2cp/) und wird von nahezu allen interaktiven I2P-Anwendungen verwendet, einschließlich HTTP-Proxys, IRC, BitTorrent und E-Mail.

### Kernmerkmale

- Einstufiger Verbindungsaufbau mit **SYN**-, **ACK**- und **FIN**-Flags, die mit Nutzdaten gebündelt werden können, um Round-Trips zu reduzieren.
- **Sliding-Window-Staukontrolle** mit Slow Start und Congestion Avoidance, optimiert für die Hochlatenz-Umgebung von I2P.
- Paketkomprimierung (standardmäßig 4KB komprimierte Segmente), die Kosten für erneute Übertragung und Fragmentierungslatenz ausbalanciert.
- Vollständig **authentifizierte, verschlüsselte** und **zuverlässige** Kanal-Abstraktion zwischen I2P-Destinations.

Dieses Design ermöglicht es, dass kleine HTTP-Anfragen und -Antworten in einem einzigen Round-Trip abgeschlossen werden. Ein SYN-Paket kann die Anfrage-Nutzdaten enthalten, während das SYN/ACK/FIN des Antwortenden den vollständigen Antwortinhalt enthalten kann.

---

## API-Grundlagen

Die Java-Streaming-API entspricht der Standard-Java-Socket-Programmierung:

```java
I2PSocketManager mgr = I2PSocketManagerFactory.createManager(host, port, options);
I2PSocket socket       = mgr.connect(destination);
I2PServerSocket server = mgr.getServerSocket();
```
- `I2PSocketManagerFactory` verhandelt oder verwendet eine Router-Sitzung über I2CP wieder.
- Falls kein Schlüssel bereitgestellt wird, wird automatisch ein neues Ziel generiert.
- Entwickler können I2CP-Optionen (z. B. Tunnellängen, Verschlüsselungstypen oder Verbindungseinstellungen) über die `options`-Map übergeben.
- `I2PSocket` und `I2PServerSocket` spiegeln die Standard-Java-`Socket`-Schnittstellen wider, was die Migration unkompliziert macht.

Vollständige Javadocs sind über die I2P Router-Konsole oder [hier](/docs/specs/streaming/) verfügbar.

---

## Konfiguration und Optimierung

Sie können Konfigurationseigenschaften beim Erstellen eines Socket-Managers übergeben über:

```java
I2PSocketManagerFactory.createManager(host, port, properties);
```
### Schlüsseloptionen

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Default</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.maxWindowSize</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Maximum send window (bytes)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128 KB</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.initialRTO</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Initial retransmission timeout</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">9s</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.inactivityTimeout</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Timeout before connection close</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">90s</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.enforceProtocol</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Enforce protocol ID (prevents confusion)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">true</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.congestionAlgorithm</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Congestion control method</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default (AIMD TCP-like)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.disableRejectLogging</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Disable logging rejected packets</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">false</td>
    </tr>
  </tbody>
</table>
### Verhalten nach Arbeitslast

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Workload</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended Settings</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>HTTP-like</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default parameters are ideal.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Bulk Transfer</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Increase window size to 256 KB or 512 KB; lengthen timeouts.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Real-time Streaming</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Lower tunnel length to 1-2 hops; adjust RTO downwards.</td>
    </tr>
  </tbody>
</table>
Neuere Funktionen seit Version 0.9.4 umfassen die Unterdrückung von Ablehnungsprotokollen, DSA-Listenunterstützung (0.9.21) und die obligatorische Protokolldurchsetzung (0.9.36). Router seit 2.10.0 enthalten Post-Quanten-Hybridverschlüsselung (ML-KEM + X25519) auf der Transportschicht.

---

## Protokolldetails

Jeder Stream wird durch eine **Stream ID** identifiziert. Pakete tragen Steuerungsflags ähnlich wie TCP: `SYNCHRONIZE`, `ACK`, `FIN` und `RESET`. Pakete können gleichzeitig sowohl Daten als auch Steuerungsflags enthalten, was die Effizienz für kurzlebige Verbindungen verbessert.

### Verbindungslebenszyklus

1. **SYN gesendet** — Initiator enthält optionale Daten.  
2. **SYN/ACK-Antwort** — Responder enthält optionale Daten.  
3. **ACK-Finalisierung** — stellt Zuverlässigkeit und Sitzungsstatus her.  
4. **FIN/RESET** — wird für ordnungsgemäßes Schließen oder abrupten Abbruch verwendet.

### Fragmentierung und Neuordnung

Da I2P-Tunnel Latenz und Nachrichten-Umordnung verursachen, puffert die Bibliothek Pakete von unbekannten oder vorzeitig eintreffenden Streams. Gepufferte Nachrichten werden gespeichert, bis die Synchronisierung abgeschlossen ist, wodurch eine vollständige, geordnete Zustellung gewährleistet wird.

### Protokolldurchsetzung

Die Option `i2p.streaming.enforceProtocol=true` (Standard seit 0.9.36) stellt sicher, dass Verbindungen die korrekte I2CP-Protokollnummer verwenden, wodurch Konflikte zwischen mehreren Subsystemen verhindert werden, die ein destination gemeinsam nutzen.

---

## Interoperabilität und Best Practices

Das Streaming-Protokoll existiert parallel zur **Datagram API** und gibt Entwicklern die Wahl zwischen verbindungsorientierten und verbindungslosen Transportmechanismen.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Use Case</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended Transport</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reliable, ordered data (HTTP, IRC, FTP)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Streaming</strong></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connectionless or lossy data (DNS, telemetry)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Datagram</strong></td>
    </tr>
  </tbody>
</table>
### Gemeinsame Clients

Anwendungen können bestehende Tunnel wiederverwenden, indem sie als **Shared Clients** laufen, wodurch mehrere Dienste dieselbe Destination gemeinsam nutzen können. Dies reduziert zwar den Overhead, erhöht aber das Risiko der dienstübergreifenden Korrelation – mit Vorsicht verwenden.

### Überlastungssteuerung

- Die Streaming-Ebene passt sich kontinuierlich an Netzwerklatenz und Durchsatz über RTT-basiertes Feedback an.
- Anwendungen funktionieren am besten, wenn Router beitragende Peers sind (teilnehmende Tunnel aktiviert).
- TCP-ähnliche Überlastungskontrollmechanismen verhindern die Überlastung langsamer Peers und helfen, die Bandbreitennutzung über Tunnel hinweg auszugleichen.

### Latenzüberlegungen

Da I2P mehrere hundert Millisekunden Basislatenz hinzufügt, sollten Anwendungen Round-Trips minimieren. Bündeln Sie Daten mit dem Verbindungsaufbau, wo möglich (z.B. HTTP-Anfragen in SYN). Vermeiden Sie Designs, die auf vielen kleinen sequenziellen Austauschen basieren.

---

## Testen und Kompatibilität

- Testen Sie immer gegen sowohl **Java I2P** als auch **i2pd**, um vollständige Kompatibilität sicherzustellen.
- Obwohl das Protokoll standardisiert ist, können geringfügige Implementierungsunterschiede bestehen.
- Gehen Sie mit älteren Routern behutsam um – viele Peers verwenden noch Versionen vor 2.0.
- Überwachen Sie Verbindungsstatistiken mit `I2PSocket.getOptions()` und `getSession()`, um RTT- und Retransmission-Metriken auszulesen.

Die Leistung hängt stark von der Tunnel-Konfiguration ab:   - **Kurze Tunnel (1–2 Hops)** → geringere Latenz, reduzierte Anonymität.   - **Lange Tunnel (3+ Hops)** → höhere Anonymität, erhöhte RTT.

---

## Wichtige Verbesserungen (2.0.0–2.10.0)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Introduced</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Persistent ACK Bundling</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.0.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Optimized round-trip reduction for HTTP workloads.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Adaptive Window Scaling</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.3.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Improved large file transfer stability.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Thread Pooling and Socket Reuse</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.5.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reduced per-connection overhead.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Protocol Enforcement Default</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.36</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ensures correct stream usage.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Hybrid ML-KEM Ratchet</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Adds post-quantum hybrid encryption layer.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>i2pd Streaming API Compatibility Fixes</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.9.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Full parity with Java I2P library behavior.</td>
    </tr>
  </tbody>
</table>
---

## Zusammenfassung

Die **I2P Streaming Library** ist das Rückgrat jeglicher zuverlässiger Kommunikation innerhalb von I2P. Sie gewährleistet die geordnete, authentifizierte und verschlüsselte Nachrichtenzustellung und bietet einen nahezu vollständigen Ersatz für TCP in anonymen Umgebungen.

Um optimale Leistung zu erzielen: - Minimieren Sie Round-Trips durch SYN+Payload-Bündelung.   - Passen Sie Fenster- und Timeout-Parameter für Ihre Arbeitslast an.   - Bevorzugen Sie kürzere Tunnel für latenzempfindliche Anwendungen.   - Verwenden Sie überlastungsfreundliche Designs, um Peers nicht zu überlasten.
