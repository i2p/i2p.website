---
title: "Datagramme"
description: "Authentifizierte, beantwortbare und rohe Nachrichtenformate über I2CP"
slug: "datagrams"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
toc: true
---

## Überblick

Datagrams bieten nachrichtenorientierte Kommunikation oberhalb von [I2CP](/docs/specs/i2cp/) und parallel zur Streaming-Bibliothek. Sie ermöglichen **beantwortbare**, **authentifizierte** oder **rohe** Pakete, ohne verbindungsorientierte Streams zu erfordern. Router kapseln Datagrams in I2NP-Nachrichten und Tunnel-Nachrichten ein, unabhängig davon, ob NTCP2 oder SSU2 den Verkehr überträgt.

Die zentrale Motivation besteht darin, Anwendungen (wie Tracker, DNS-Resolver oder Spiele) zu ermöglichen, eigenständige Pakete zu senden, die ihren Absender identifizieren.

> **Neu in 2025:** Das I2P-Projekt hat **Datagram2 (Protokoll 19)** und **Datagram3 (Protokoll 20)** genehmigt, die zum ersten Mal seit einem Jahrzehnt Replay-Schutz und Messaging mit geringerem Overhead und Antwortmöglichkeit hinzufügen.

---

## 1. Protokollkonstanten

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Value</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Introduced</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>PROTO_DATAGRAM</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">17</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Signed (repliable) datagram – “Datagram1”</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Original</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>PROTO_DATAGRAM_RAW</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unsigned (raw) datagram – no sender info</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Original</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>PROTO_DATAGRAM2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Signed + replay-protected datagram</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">API 0.9.66 (2025)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>PROTO_DATAGRAM3</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Repliable (no signature, hash only)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">API 0.9.66 (2025)</td>
    </tr>
  </tbody>
</table>
Die Protokolle 19 und 20 wurden in **Proposal 163 (April 2025)** formalisiert. Sie koexistieren mit Datagram1 / RAW zur Abwärtskompatibilität.

---

## 2. Datagramm-Typen

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Repliable</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Authenticated</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Replay Protection</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Min Overhead</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Raw</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Minimal size; spoofable.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Datagram1</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">17</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">≈ 427</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Full Destination + signature.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Datagram2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">≈ 457</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Replay prevention + offline signatures; PQ-ready.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Datagram3</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">≈ 34</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Sender hash only; low overhead.</td>
    </tr>
  </tbody>
</table>
### Typische Designmuster

- **Request → Response:** Senden Sie ein signiertes Datagram2 (Anfrage + Nonce), empfangen Sie eine Raw- oder Datagram3-Antwort (Echo-Nonce).  
- **Hochfrequenz/geringer Overhead:** Bevorzugen Sie Datagram3 oder RAW.  
- **Authentifizierte Kontrollnachrichten:** Datagram2.  
- **Legacy-Kompatibilität:** Datagram1 wird weiterhin vollständig unterstützt.

---

## 3. Datagram2 und Datagram3 Details (2025)

### Datagram2 (Protokoll 19)

Erweiterte Alternative zu Datagram1. Funktionen: - **Replay-Schutz:** 4-Byte Anti-Replay-Token. - **Unterstützung für Offline-Signaturen:** ermöglicht die Verwendung durch offline-signierte Destinations. - **Erweiterte Signaturabdeckung:** umfasst Destination-Hash, Flags, Optionen, Offline-Signaturblock, Payload. - **Post-Quanten-bereit:** kompatibel mit zukünftigen ML-KEM-Hybriden. - **Overhead:** ≈ 457 Bytes (X25519-Schlüssel).

### Datagram3 (Protokoll 20)

Überbrückt die Lücke zwischen rohen und signierten Typen. Funktionen: - **Ohne Signatur beantwortbar:** enthält 32-Byte-Hash des Absenders + 2-Byte-Flags. - **Minimaler Overhead:** ≈ 34 Bytes. - **Kein Replay-Schutz** — muss von der Anwendung implementiert werden.

Beide Protokolle sind API 0.9.66-Funktionen und seit Release 2.9.0 im Java-Router implementiert; noch keine i2pd- oder Go-Implementierungen (Oktober 2025).

---

## 4. Größen- und Fragmentierungslimits

- **Tunnel-Nachrichtengröße:** 1 028 Bytes (4 B Tunnel-ID + 16 B IV + 1 008 B Nutzdaten).  
- **Erstes Fragment:** 956 B (typische TUNNEL-Zustellung).  
- **Folgefragment:** 996 B.  
- **Maximale Fragmente:** 63–64.  
- **Praktisches Limit:** ≈ 62 708 B (~61 KB).  
- **Empfohlenes Limit:** ≤ 10 KB für zuverlässige Zustellung (Paketverluste steigen darüber hinaus exponentiell an).

**Overhead-Zusammenfassung:** - Datagram1 ≈ 427 B (Minimum).   - Datagram2 ≈ 457 B.   - Datagram3 ≈ 34 B.   - Zusätzliche Schichten (I2CP gzip-Header, I2NP, Garlic, Tunnel): + ~5,5 KB im ungünstigsten Fall.

---

## 5. I2CP / I2NP Integration

Nachrichtenpfad: 1. Anwendung erstellt Datagramm (über I2P API oder SAM).   2. I2CP verpackt mit gzip-Header (`0x1F 0x8B 0x08`, RFC 1952) und CRC-32-Prüfsumme.   3. Protokoll + Portnummern werden in gzip-Header-Feldern gespeichert.   4. Router kapselt als I2NP-Nachricht → Garlic clove → 1 KB tunnel-Fragmente.   5. Fragmente durchqueren outbound → Netzwerk → inbound tunnel.   6. Zusammengesetztes Datagramm wird basierend auf Protokollnummer an Anwendungs-Handler übergeben.

**Integrität:** CRC-32 (von I2CP) + optionale kryptografische Signatur (Datagram1/2). Es gibt kein separates Prüfsummenfeld innerhalb des Datagramms selbst.

---

## 6. Programmierschnittstellen

### Java-API

Das Paket `net.i2p.client.datagram` enthält: - `I2PDatagramMaker` – erstellt signierte Datagramme.   - `I2PDatagramDissector` – überprüft und extrahiert Absenderinformationen.   - `I2PInvalidDatagramException` – wird bei Überprüfungsfehlern ausgelöst.

`I2PSessionMuxedImpl` (`net.i2p.client.impl.I2PSessionMuxedImpl`) verwaltet Protokoll- und Port-Multiplexing für Anwendungen, die sich eine Destination teilen.

**Javadoc-Zugriff:** - [idk.i2p Javadoc](http://idk.i2p/javadoc-i2p/) (nur I2P-Netzwerk) - [Javadoc Mirror](https://eyedeekay.github.io/javadoc-i2p/) (Clearnet-Spiegel) - [Offizielle Javadocs](http://docs.i2p-projekt.de/javadoc/) (offizielle Dokumentation)

### SAM v3 Unterstützung

- SAM 3.2 (2016): PORT- und PROTOCOL-Parameter hinzugefügt.  
- SAM 3.3 (2016): PRIMARY/Subsession-Modell eingeführt; ermöglicht Streams + Datagrams auf einer Destination.  
- Unterstützung für Datagram2 / 3 Session-Stile zur Spezifikation 2025 hinzugefügt (Implementierung ausstehend).  
- Offizielle Spezifikation: [SAM v3 Specification](/docs/api/samv3/)

### i2ptunnel-Module

- **udpTunnel:** Voll funktionsfähige Basis für I2P-UDP-Anwendungen (`net.i2p.i2ptunnel.udpTunnel`).  
- **streamr:** Betriebsbereit für A/V-Streaming (`net.i2p.i2ptunnel.streamr`).  
- **SOCKS UDP:** **Nicht funktionsfähig** ab Version 2.10.0 (nur UDP-Stub).

> Für allgemeine UDP-Zwecke verwenden Sie die Datagram-API oder udpTunnel direkt – verlassen Sie sich nicht auf SOCKS UDP.

---

## 7. Ökosystem und Sprachunterstützung (2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Language</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Library / Package</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">SAM Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Java</td><td style="border:1px solid var(--color-border); padding:0.5rem;">core API (net.i2p.client.datagram)</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✓ full support</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">C++</td><td style="border:1px solid var(--color-border); padding:0.5rem;">i2pd / libsam3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2 partial</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Limited</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Go</td><td style="border:1px solid var(--color-border); padding:0.5rem;">go-i2p / sam3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1–3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td><td style="border:1px solid var(--color-border); padding:0.5rem;">i2plib, i2p.socket, txi2p</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Rust</td><td style="border:1px solid var(--color-border); padding:0.5rem;">i2p-rs, i2p_client</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">C#</td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2PSharp</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">JS/TS</td><td style="border:1px solid var(--color-border); padding:0.5rem;">node-i2p, i2p-sam</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Haskell</td><td style="border:1px solid var(--color-border); padding:0.5rem;">network-anonymous-i2p</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Lua</td><td style="border:1px solid var(--color-border); padding:0.5rem;">mooni2p</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental</td></tr>
  </tbody>
</table>
Java I2P ist derzeit der einzige Router, der vollständige SAM 3.3 Subsessions und die Datagram2 API unterstützt.

---

## 8. Beispielanwendung – UDP-Tracker (I2PSnark 2.10.0)

Erste reale Anwendung von Datagram2/3:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Datagram Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Announce Request</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Datagram3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Repliable but low-overhead update</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Response</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Raw Datagram</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimal payload return</td></tr>
  </tbody>
</table>
Das Muster demonstriert die gemischte Verwendung von authentifizierten und leichtgewichtigen Datagrammen, um Sicherheit und Leistung auszubalancieren.

---

## 9. Sicherheit und Best Practices

- Verwenden Sie Datagram2 für jeden authentifizierten Austausch oder wenn Replay-Angriffe relevant sind.
- Bevorzugen Sie Datagram3 für schnelle beantwortbare Antworten mit moderatem Vertrauen.
- Verwenden Sie RAW für öffentliche Broadcasts oder anonyme Daten.
- Halten Sie Payloads ≤ 10 KB für zuverlässige Zustellung.
- Beachten Sie, dass SOCKS UDP weiterhin nicht funktionsfähig ist.
- Überprüfen Sie immer gzip CRC und digitale Signaturen beim Empfang.

---

## 10. Technische Spezifikation

Dieser Abschnitt behandelt die Low-Level-Datagramm-Formate, Kapselung und Protokolldetails.

### 10.1 Protokollidentifikation

Datagramm-Formate teilen **keinen** gemeinsamen Header. Router können den Typ nicht allein anhand der Payload-Bytes ableiten.

Beim Mischen mehrerer Datagramm-Typen – oder beim Kombinieren von Datagrammen mit Streaming – explizit festlegen: - Die **Protokollnummer** (über I2CP oder SAM) - Optional die **Portnummer**, wenn Ihre Anwendung mehrere Dienste multiplext

Das Protokoll nicht festzulegen (`0` oder `PROTO_ANY`) wird nicht empfohlen und kann zu Routing- oder Zustellfehlern führen.

### 10.2 Raw Datagrams

Nicht beantwortbare Datagramme enthalten keine Absender- oder Authentifizierungsdaten. Sie sind opake Nutzdaten, die außerhalb der höherstufigen Datagramm-API verarbeitet werden, aber über SAM und I2PTunnel unterstützt werden.

**Protokoll:** `18` (`PROTO_DATAGRAM_RAW`)

**Format:**

```
+----+----+----+----+----//
|     payload...
+----+----+----+----+----//
```
Die Payload-Länge ist durch Transportlimits beschränkt (≈32 KB praktisches Maximum, oft deutlich weniger).

### 10.3 Datagram1 (Beantwortbare Datagramme)

Bettet die **Destination** des Absenders und eine **Signature** zur Authentifizierung und Antwortadressierung ein.

**Protokoll:** `17` (`PROTO_DATAGRAM`)

**Overhead:** ≥427 Bytes **Payload:** bis zu ~31,5 KB (begrenzt durch Transport)

**Format:**

```
+----+----+----+----+----+----+----+----+
|               from                    |
+                                       +
|                                       |
~             Destination bytes         ~
|                                       |
+----+----+----+----+----+----+----+----+
|             signature                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|     payload...
+----+----+----+----//
```
- `from`: ein Destination (387+ Bytes)
- `signature`: eine Signature, die dem Schlüsseltyp entspricht
  - Für DSA_SHA1: Signature des SHA-256-Hashs der Payload
  - Für andere Schlüsseltypen: Signature direkt über die Payload

**Hinweise:** - Signaturen für Nicht-DSA-Typen wurden in I2P 0.9.14 standardisiert. - LS2 (Proposal 123) Offline-Signaturen werden derzeit in Datagram1 nicht unterstützt.

### 10.4 Datagram2-Format

Ein verbessertes beantwortbares Datagramm, das **Replay-Resistenz** hinzufügt, wie in [Proposal 163](/proposals/163-datagram2/) definiert.

**Protokoll:** `19` (`PROTO_DATAGRAM2`)

Die Implementierung ist im Gange. Anwendungen sollten Nonce- oder Zeitstempel-Prüfungen zur Redundanz enthalten.

### 10.5 Datagram3-Format

Bietet **beantwortbare, aber nicht authentifizierte** Datagramme. Basiert auf der vom Router verwalteten Sitzungsauthentifizierung anstatt auf eingebetteter Zieladresse und Signatur.

**Protokoll:** `20` (`PROTO_DATAGRAM3`) **Status:** In Entwicklung seit 0.9.66

Nützlich, wenn: - Ziele groß sind (z. B. Post-Quantum-Schlüssel) - Authentifizierung auf einer anderen Ebene erfolgt - Bandbreiteneffizienz kritisch ist

### 10.6 Datenintegrität

Die Integrität des Datagramms wird durch die **gzip CRC-32-Prüfsumme** in der I2CP-Schicht geschützt. Es existiert kein explizites Prüfsummenfeld innerhalb des Datagramm-Payload-Formats selbst.

### 10.7 Paket-Kapselung

Jedes Datagramm wird als einzelne I2NP-Nachricht oder als einzelne Clove in einer **Garlic Message** gekapselt. I2CP-, I2NP- und Tunnel-Schichten handhaben Länge und Rahmenbildung — es gibt kein internes Trennzeichen oder Längenfeld im Datagramm-Protokoll.

### 10.8 Post-Quantum (PQ) Überlegungen

Wenn **Proposal 169** (ML-DSA-Signaturen) implementiert wird, werden die Signatur- und Zielgrößen dramatisch ansteigen – von ~455 Bytes auf **≥3739 Bytes**. Diese Änderung wird den Datagram-Overhead erheblich erhöhen und die effektive Nutzlastkapazität reduzieren.

**Datagram3**, das auf Authentifizierung auf Sitzungsebene (nicht eingebettete Signaturen) setzt, wird wahrscheinlich das bevorzugte Design in Post-Quanten-I2P-Umgebungen werden.

---

## 11. Referenzen

- [Proposal 163 – Datagram2 und Datagram3](/proposals/163-datagram2/)
- [Proposal 160 – UDP Tracker Integration](/proposals/160-udp-trackers/)
- [Proposal 144 – Streaming MTU Berechnungen](/proposals/144-ecies-x25519-aead-ratchet/)
- [Proposal 169 – Post-Quantum Signaturen](/proposals/169-pq-crypto/)
- [I2CP Spezifikation](/docs/specs/i2cp/)
- [I2NP Spezifikation](/docs/specs/i2np/)
- [Tunnel Message Spezifikation](/docs/specs/implementation/)
- [SAM v3 Spezifikation](/docs/api/samv3/)
- [i2ptunnel Dokumentation](/docs/api/i2ptunnel/)

## 12. Wichtigste Änderungen im Changelog (2019 – 2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Year</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Release</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Change</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2019</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.43</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Datagram API stabilization</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2021</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.50</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Protocol port handling reworked</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2022</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2.0.0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 adoption completed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2024</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2.6.0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy transport removal simplified UDP code</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2025</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2.9.0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Datagram2/3 support added (Java API)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2025</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2.10.0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">UDP Tracker implementation released</td></tr>
  </tbody>
</table>
---

## 13. Zusammenfassung

Das Datagram-Subsystem unterstützt jetzt vier Protokollvarianten, die ein Spektrum von vollständig authentifiziert bis hin zu leichtgewichtiger Rohübertragung bieten. Entwickler sollten für sicherheitskritische Anwendungsfälle zu **Datagram2** und für effizienten beantwortbaren Datenverkehr zu **Datagram3** migrieren. Alle älteren Typen bleiben kompatibel, um langfristige Interoperabilität zu gewährleisten.
