---
title: "Streaming-Protokoll"
description: "Zuverlässiger, TCP-ähnlicher Transport, der von den meisten I2P-Anwendungen verwendet wird"
slug: "streaming"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## Übersicht

Die I2P Streaming Library (Streaming-Bibliothek) bietet eine zuverlässige, geordnete und authentifizierte Datenübertragung aufbauend auf der unzuverlässigen Nachrichtenebene von I2P — analog zu TCP über IP. Sie wird von fast allen interaktiven I2P‑Anwendungen wie Web‑Browsing, IRC, E‑Mail und Dateifreigabe verwendet.

Es stellt zuverlässige Übertragung, Überlastkontrolle, Wiederübertragung und Flusssteuerung über die anonymen tunnels mit hoher Latenz von I2P sicher. Jeder Datenstrom ist zwischen Destinations (Zielen) vollständig Ende-zu-Ende verschlüsselt.

---

## Zentrale Designprinzipien

Die Streaming-Bibliothek implementiert einen **einphasigen Verbindungsaufbau**, bei dem SYN-, ACK- und FIN-Flags Nutzdaten in derselben Nachricht mitführen können. Dies minimiert Round-Trips in Umgebungen mit hoher Latenz — eine kleine HTTP-Transaktion kann in einem einzigen Round-Trip abgeschlossen werden.

Staukontrolle und Wiederübertragung sind an TCP angelehnt, jedoch für die Umgebung von I2P angepasst. Die Fenstergrößen sind nachrichtenbasiert statt bytebasiert und auf die tunnel-Latenz sowie den Overhead abgestimmt. Das Protokoll unterstützt langsamen Start, Stauvermeidung und exponentielles Backoff, ähnlich dem AIMD-Algorithmus von TCP.

---

## Architektur

Die Streaming-Bibliothek arbeitet zwischen Anwendungen und der I2CP-Schnittstelle.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Layer</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Responsibility</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Application</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Standard I2PSocket and I2PServerSocket usage</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Streaming Library</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connection setup, sequencing, retransmission, and flow control</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2CP</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel creation, routing, and message handling</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2NP / Router Layer</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Transport through tunnels</td>
    </tr>
  </tbody>
</table>
Die meisten Nutzer greifen über I2PSocketManager, I2PTunnel oder SAMv3 darauf zu. Die Bibliothek übernimmt transparent die Destination-Verwaltung (Adresse in I2P), die tunnel-Nutzung und erneute Übertragungen.

---

## Paketformat

```
+-----------------------------------------------+
| Send Stream ID (4B) | Receive Stream ID (4B) |
+-----------------------------------------------+
| Sequence Number (4B) | Ack Through (4B)      |
+-----------------------------------------------+
| NACK Count (1B) | optional NACK list (4B each)
+-----------------------------------------------+
| Flags (1B) | Option Size (1B) | Options ...   |
+-----------------------------------------------+
| Payload ...                                  |
```
### Details zum Header

- **Stream-IDs**: 32-Bit-Werte, die lokale und entfernte Streams eindeutig kennzeichnen.
- **Sequenznummer**: Beginnt bei 0 für SYN und erhöht sich pro Nachricht.
- **Ack Through (Bestätigt bis)**: Bestätigt alle Nachrichten bis N, mit Ausnahme derjenigen in der NACK-Liste.
- **Flags**: Bitmaske, die Zustand und Verhalten steuert.
- **Optionen**: Liste variabler Länge für RTT, MTU und Protokollverhandlung.

### Schlüssel-Flags

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Flag</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SYN</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connection initiation</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ACK</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Acknowledge received packets</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">FIN</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Graceful close</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RST</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reset connection</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">FROM_INCLUDED</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Sender’s destination included</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SIGNATURE_INCLUDED</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Message signed by sender</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECHO / ECHO_REPLY</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ping/Pong keepalive</td>
    </tr>
  </tbody>
</table>
---

## Flusskontrolle und Zuverlässigkeit

Streaming (I2P-Streaming-Protokoll) verwendet **nachrichtenbasierte Fenstersteuerung**, im Gegensatz zum bytebasierten Ansatz von TCP. Die Anzahl der unbestätigten Pakete, die gleichzeitig unterwegs sein dürfen, entspricht der aktuellen Fenstergröße (Standard: 128).

### Mechanismen

- **Staukontrolle:** Slow Start und AIMD-basierte Stauvermeidung (additive Erhöhung/multiplikative Verringerung).  
- **Choke/Unchoke (Drosseln/Freigeben):** Flusskontrollsignalisierung basierend auf Pufferbelegung.  
- **Wiederübertragung:** RFC 6298-basierte RTO-Berechnung mit exponentiellem Backoff.  
- **Duplikatfilterung:** Gewährleistet Zuverlässigkeit trotz potenziell umgeordneter Nachrichten.

Typische Konfigurationswerte:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Parameter</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Default</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>maxWindowSize</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Max unacknowledged messages</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>maxMessageSize</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1730</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Maximum payload bytes per message</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>initialRTO</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">9000 ms</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Initial retransmission timeout</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>inactivityTimeout</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">90000 ms</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Idle connection timeout</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>connectTimeout</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">300000 ms</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connection establishment timeout</td>
    </tr>
  </tbody>
</table>
---

## Verbindungsaufbau

1. **Initiator** sendet ein SYN (optional mit Nutzdaten und FROM_INCLUDED).  
2. **Antwortender** antwortet mit SYN+ACK (kann Nutzdaten enthalten).  
3. **Initiator** sendet das abschließende ACK und bestätigt damit den Verbindungsaufbau.

Optionale anfängliche Nutzdaten ermöglichen die Datenübertragung, bevor der vollständige Handshake abgeschlossen ist.

---

## Implementierungsdetails

### Wiederübertragung und Zeitüberschreitung

Der Wiederübertragungsalgorithmus folgt **RFC 6298**.   - **Initiales RTO:** 9s   - **Minimales RTO:** 100ms   - **Maximales RTO:** 45s   - **Alpha:** 0.125   - **Beta:** 0.25

### Gemeinsame Nutzung von Steuerblöcken

Jüngste Verbindungen zum selben Peer nutzen vorherige RTT (Round-Trip Time, Hin- und Rücklaufzeit) und Fensterdaten erneut, um den Hochlauf zu beschleunigen und „Kaltstart“-Latenz zu vermeiden. Kontrollblöcke verfallen nach einigen Minuten.

### MTU und Fragmentierung

- Standard-MTU: **1730 Bytes** (fasst zwei I2NP-Nachrichten).  
- ECIES-Ziele: **1812 Bytes** (verringerter Overhead).  
- Minimale unterstützte MTU: 512 Bytes.

Die Nutzlastgröße umfasst den Streaming-Header mit einer Mindestgröße von 22 Byte nicht.

---

## Versionsverlauf

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Router Version</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.7.1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Protocol numbers defined in I2CP</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.11</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Variable-length signatures</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA signature support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ed25519 signature support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.18</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ping/Pong payloads</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.20</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">FROM_INCLUDED not required in RESET</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.36</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Protocol enforcement enabled by default</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.39</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">OFFLINE_SIGNATURE support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.58</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Bob’s hash added to NACK field in SYN</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Post-Quantum hybrid encryption (experimental)</td>
    </tr>
  </tbody>
</table>
---

## Nutzung auf Anwendungsebene

### Java-Beispiel

```java
Properties props = new Properties();
props.setProperty("i2p.streaming.maxWindowSize", "512");
I2PSocketManager mgr = I2PSocketManagerFactory.createManager(props);

I2PSocket socket = mgr.connect(destination);
InputStream in = socket.getInputStream();
OutputStream out = socket.getOutputStream();
```
### Unterstützung für SAMv3 und i2pd

- **SAMv3**: Bietet STREAM- und DATAGRAM-Modi für Nicht-Java-Clients.  
- **i2pd**: Stellt identische Streaming-Parameter über Optionen der Konfigurationsdatei bereit (z. B. `i2p.streaming.maxWindowSize`, `profile`, usw.).

---

## Die Wahl zwischen Streaming und Datagrammen

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Use Case</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended Transport</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Reason</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HTTP, IRC, Email</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Streaming</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Requires reliability</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DNS</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Repliable Datagram</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Single request/response</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Telemetry, Logging</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Raw Datagram</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Best-effort acceptable</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P2P DHT</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Datagram</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">High connection churn</td>
    </tr>
  </tbody>
</table>
---

## Sicherheit und Post-Quanten-Zukunft

Streaming-Sitzungen sind auf der I2CP-Ebene Ende-zu-Ende-verschlüsselt.   Post-Quanten-Hybridverschlüsselung (ML-KEM + X25519) wird in 2.10.0 experimentell unterstützt, ist jedoch standardmäßig deaktiviert.

---

## Referenzen

- [Streaming-API-Übersicht](/docs/specs/streaming/)  
- [Spezifikation des Streaming-Protokolls](/docs/specs/streaming/)  
- [I2CP-Spezifikation](/docs/specs/i2cp/)  
- [Vorschlag 144: Streaming-MTU-Berechnungen](/proposals/144-ecies-x25519-aead-ratchet/)  
- [I2P 2.10.0 Versionshinweise](/de/blog/2025/09/08/i2p-2.10.0-release/)
