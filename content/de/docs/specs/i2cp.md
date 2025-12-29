---
title: "I2P-Client-Protokoll (I2CP)"
description: "Wie Anwendungen Sitzungen, tunnels und LeaseSets mit dem I2P router aushandeln."
slug: "i2cp"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Überblick

I2CP ist das Low-Level-Steuerprotokoll zwischen einem I2P router und jedem beliebigen Client-Prozess. Es definiert eine strikte Trennung der Verantwortlichkeiten:

- **Router**: Verwaltet Routing, Kryptografie, Lebenszyklen von tunnels und Netzwerkdatenbank-Operationen
- **Client**: Wählt Anonymitätseigenschaften aus, konfiguriert tunnels und übermittelt/empfängt Nachrichten

Die gesamte Kommunikation läuft über einen einzigen TCP-Socket (optional TLS-gekapselt), wodurch asynchroner Vollduplexbetrieb ermöglicht wird.

**Protokollversion**: I2CP verwendet ein Protokollversions-Byte `0x2A` (42 dezimal), das während des initialen Verbindungsaufbaus gesendet wird. Dieses Versions-Byte ist seit der Einführung des Protokolls unverändert geblieben.

**Aktueller Stand**: Diese Spezifikation gilt für router version 0.9.67 (API-Version 0.9.67), veröffentlicht 2025-09.

## Implementierungskontext

### Java-Implementierung

Die Referenzimplementierung ist in Java I2P: - Client-SDK: `i2p.jar`-Paket - Router-Implementierung: `router.jar`-Paket - [Javadocs](http://docs.i2p-projekt.de/javadoc/)

Wenn Client und router in derselben JVM laufen, werden I2CP-Nachrichten als Java-Objekte ohne Serialisierung übergeben. Externe Clients verwenden das serialisierte Protokoll über TCP.

### C++-Implementierung

i2pd (der C++ I2P router) stellt I2CP für Client-Verbindungen auch extern bereit.

### Nicht-Java-Clients

Es gibt **keine bekannten Nicht-Java-Implementierungen** einer vollständigen I2CP-Clientbibliothek. Nicht-Java-Anwendungen sollten stattdessen höherstufige Protokolle verwenden:

- **SAM (Simple Anonymous Messaging) v3**: Socket-basierte Schnittstelle mit Bibliotheken in mehreren Programmiersprachen
- **BOB (Basic Open Bridge)**: Einfachere Alternative zu SAM

Diese Protokolle höherer Ebene handhaben die I2CP-Komplexität intern und stellen außerdem die Streaming-Bibliothek (für TCP-ähnliche Verbindungen) und die Datagramm-Bibliothek (für UDP-ähnliche Verbindungen) bereit.

## Verbindungsaufbau

### 1. TCP-Verbindung

Stellen Sie eine Verbindung zum I2CP-Port des router her: - Standard: `127.0.0.1:7654` - Über die router-Einstellungen konfigurierbar - Optionaler TLS-Wrapper (für Remote-Verbindungen dringend empfohlen)

### 2. Protokoll-Handshake

**Schritt 1**: Sende das Protokollversions-Byte `0x2A`

**Schritt 2**: Zeitsynchronisation

```
Client → Router: GetDateMessage
Router → Client: SetDateMessage
```
Der router gibt seinen aktuellen Zeitstempel und den I2CP-API-Versionsstring zurück (seit 0.8.7).

**Schritt 3**: Authentifizierung (falls aktiviert)

Ab Version 0.9.11 kann die Authentifizierung in GetDateMessage über ein Mapping (Zuordnung) enthalten sein, das Folgendes enthält: - `i2cp.username` - `i2cp.password`

Seit 0.9.16 **muss**, wenn die Authentifizierung aktiviert ist, die Authentifizierung über GetDateMessage abgeschlossen werden, bevor andere Nachrichten gesendet werden.

**Schritt 4**: Sitzungserstellung

```
Client → Router: CreateSessionMessage (contains SessionConfig)
Router → Client: SessionStatusMessage (status=Created)
```
**Schritt 5**: Tunnel-Bereitsignal

```
Router → Client: RequestVariableLeaseSetMessage
```
Diese Nachricht zeigt an, dass eingehende tunnels aufgebaut wurden. Der router wird dies NICHT senden, bevor mindestens ein eingehender UND ein ausgehender tunnel existieren.

**Schritt 6**: LeaseSet-Veröffentlichung

```
Client → Router: CreateLeaseSet2Message
```
An diesem Punkt ist die Sitzung zum Senden und Empfangen von Nachrichten vollständig einsatzbereit.

## Muster des Nachrichtenflusses

### Ausgehende Nachricht (Client sendet an ein entferntes Ziel)

**Mit i2cp.messageReliability=none**:

```
Client → Router: SendMessageMessage (nonce=0)
[No acknowledgments]
```
**Mit i2cp.messageReliability=BestEffort**:

```
Client → Router: SendMessageMessage (nonce>0)
Router → Client: MessageStatusMessage (status=Accepted)
Router → Client: MessageStatusMessage (status=Success or Failure)
```
### Eingehende Nachricht (Router liefert an den Client)

**Mit i2cp.fastReceive=true** (Standard seit 0.9.4):

```
Router → Client: MessagePayloadMessage
[No acknowledgment required]
```
**Mit i2cp.fastReceive=false** (VERALTET):

```
Router → Client: MessageStatusMessage (status=Available)
Client → Router: ReceiveMessageBeginMessage
Router → Client: MessagePayloadMessage
Client → Router: ReceiveMessageEndMessage
```
Moderne Clients sollten immer den schnellen Empfangsmodus verwenden.

## Allgemeine Datenstrukturen

### I2CP-Nachrichten-Header

Alle I2CP-Nachrichten verwenden diesen gemeinsamen Header:

```
+----+----+----+----+----+----+----+----+
| Body Length (4 bytes)                 |
+----+----+----+----+----+----+----+----+
|Type|  Message Body (variable)        |
+----+----+----+----+----+----+----+----+
```
- **Länge des Nachrichtenkörpers**: 4-Byte-Integer, nur die Länge des Nachrichtenkörpers (ohne Header)
- **Typ**: 1-Byte-Integer, Kennung des Nachrichtentyps
- **Nachrichtenkörper**: 0+ Bytes, Format variiert je nach Nachrichtentyp

**Begrenzung der Nachrichtengröße**: Maximal etwa 64 KB.

### Sitzungs-ID

2-Byte-Ganzzahl, die eine Sitzung auf einem router eindeutig identifiziert.

**Sonderwert**: `0xFFFF` zeigt "keine Sitzung" an (verwendet für Hostname-Abfragen ohne bestehende Sitzung).

### Nachrichten-ID

Vom router erzeugter 4-Byte-Integer zur eindeutigen Identifizierung einer Nachricht innerhalb einer Sitzung.

**Wichtig**: Nachrichten-IDs sind **nicht** global eindeutig, sondern nur innerhalb einer Sitzung eindeutig. Sie unterscheiden sich außerdem von dem vom Client erzeugten nonce (Einmalwert).

### Nutzlastformat

Nachrichten-Nutzdaten werden mit einem standardmäßigen 10-Byte-gzip-Header gzip-komprimiert: - Beginnt mit: `0x1F 0x8B 0x08` (RFC 1952) - Seit 0.7.1: Unbenutzte Teile des gzip-Headers enthalten Informationen zu Protokoll, Quellport und Zielport - Dies ermöglicht Streaming und Datagramme auf derselben Destination (I2P-Zieladresse)

**Kompressionssteuerung**: Setzen Sie `i2cp.gzip=false`, um die Kompression zu deaktivieren (setzt den gzip-Aufwand auf 0). Der gzip-Header ist weiterhin enthalten, jedoch mit minimalem Kompressions-Overhead.

### SessionConfig-Struktur

Definiert die Konfiguration für eine Client-Sitzung:

```
+----------------------------------+
| Destination                      |
+----------------------------------+
| Mapping (configuration options)  |
+----------------------------------+
| Creation Date                    |
+----------------------------------+
| Signature                        |
+----------------------------------+
```
**Kritische Anforderungen**: 1. **Die Zuordnung muss nach Schlüssel sortiert sein** für die Signaturvalidierung 2. **Erstellungsdatum** muss innerhalb von ±30 Sekunden der aktuellen Zeit des router liegen 3. **Signatur** wird vom SigningPrivateKey der Destination erstellt

**Offline-Signaturen** (seit 0.9.38):

Bei Verwendung der Offline-Signierung muss das Mapping (Zuordnung) Folgendes enthalten: - `i2cp.leaseSetOfflineExpiration` - `i2cp.leaseSetTransientPublicKey` - `i2cp.leaseSetOfflineSignature`

Die Signatur wird anschließend vom flüchtigen SigningPrivateKey erzeugt.

## Optionen der Kernkonfiguration

### Tunnelkonfiguration

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Default</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>inbound.length</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Number of hops for inbound tunnels</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.length</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Number of hops for outbound tunnels</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>inbound.lengthVariance</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Random variance in hop count (since 0.7.6)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.lengthVariance</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Random variance in hop count (since 0.7.6)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>inbound.quantity</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Number of concurrent inbound tunnels</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.quantity</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Number of concurrent outbound tunnels</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>inbound.backupQuantity</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Standby inbound tunnels (hot spares)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.backupQuantity</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Standby outbound tunnels (hot spares)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>inbound.allowZeroHop</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">true</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Allow 0-hop tunnels (disable for full anonymity)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.allowZeroHop</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">true</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Allow 0-hop tunnels (disable for full anonymity)</td>
    </tr>
  </tbody>
</table>
**Hinweise**: - Werte für `quantity` > 6 erfordern Peers, die 0.9.0+ ausführen, und erhöhen die Ressourcennutzung erheblich - Setzen Sie `backupQuantity` auf 1-2 für hochverfügbare Dienste - Zero-hop tunnels opfern Anonymität zugunsten geringerer Latenz, sind jedoch für Tests nützlich

### Nachrichtenbehandlung

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Default</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>clientMessageTimeout</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">60000&nbsp;ms</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy timeout for message delivery</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.messageReliability</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">BestEffort</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>None</code>, <code>BestEffort</code>, or <code>Guaranteed</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.fastReceive</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">true</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Skip ReceiveMessageBegin/End handshake (default since 0.9.4)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.gzip</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">true</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Enable gzip compression of message payloads</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.priority</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Priority for outbound scheduling (-25 to +25)</td>
    </tr>
  </tbody>
</table>
**Nachrichtenzuverlässigkeit**: - `None`: Keine router-Bestätigungen (Standard der Streaming-Bibliothek seit 0.8.1) - `BestEffort`: router sendet Annahme- sowie Benachrichtigungen über Erfolg/Misserfolg - `Guaranteed`: Nicht implementiert (verhält sich derzeit wie BestEffort)

**Per-Nachricht-Überschreibung** (seit 0.9.14): - In einer Sitzung mit `messageReliability=none` fordert das Setzen eines Nonce (einmaliger Zufallswert) ungleich 0 eine Zustellbenachrichtigung speziell für diese Nachricht an - Das Setzen von nonce=0 in einer `BestEffort`-Sitzung deaktiviert Benachrichtigungen für diese Nachricht

### LeaseSet-Konfiguration

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Default</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.dontPublishLeaseSet</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">false</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Disable automatic LeaseSet publication (for client-only destinations)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetType</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet variant: 1 = standard, 3 = LS2, 5 = encrypted, 7 = meta</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetEncType</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Comma-separated encryption type codes (see below)</td>
    </tr>
  </tbody>
</table>
### Veraltete ElGamal/AES Session Tags (Sitzungs-Tags)

Diese Optionen sind nur für die veraltete ElGamal-Verschlüsselung relevant:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Default</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>crypto.lowTagThreshold</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">30</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Minimum session tags before replenishing</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>crypto.tagsToSend</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">40</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Number of tags to send in a batch</td>
    </tr>
  </tbody>
</table>
**Hinweis**: ECIES-X25519-Clients (Elliptic Curve Integrated Encryption Scheme über X25519) verwenden einen anderen Ratchet-Mechanismus und ignorieren diese Optionen.

## Verschlüsselungstypen

I2CP unterstützt mehrere Ende-zu-Ende-Verschlüsselungsverfahren über die Option `i2cp.leaseSetEncType`. Es können mehrere Typen angegeben werden (kommagetrennt), um sowohl moderne als auch ältere Peers zu unterstützen.

### Unterstützte Verschlüsselungstypen

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Algorithm</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal/AES+SessionTags</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2048-bit ElGamal</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1-3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unused</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-X25519-AEAD-Ratchet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32-byte X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.46</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current Standard</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-X25519-AEAD-Ratchet + ML-KEM-768 hybrid</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32&nbsp;+&nbsp;PQ</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-X25519-AEAD-Ratchet + ML-KEM-1024 hybrid</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32&nbsp;+&nbsp;PQ</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved (likely ML-KEM-512 hybrid)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32&nbsp;+&nbsp;PQ</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Future</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Planned</td>
    </tr>
  </tbody>
</table>
**Empfohlene Konfiguration**:

```
i2cp.leaseSetEncType=4,0
```
Dies stellt X25519 (bevorzugt) mit einer ElGamal-Rückfalllösung für die Kompatibilität bereit.

### Details zum Verschlüsselungstyp

**Typ 0 - ElGamal/AES+SessionTags**: - 2048-Bit öffentliche ElGamal-Schlüssel (256 Byte) - Symmetrische AES-256-Verschlüsselung - 32-Byte Session-Tags, stapelweise gesendet - Hoher CPU-, Bandbreiten- und Speicher-Overhead - Wird netzwerkweit schrittweise abgeschafft

**Typ 4 - ECIES-X25519-AEAD-Ratchet**: - X25519-Schlüsselaustausch (32-Byte-Schlüssel) - ChaCha20/Poly1305 AEAD - Signal-Style Double Ratchet (Schlüsselableitungsverfahren mit doppelter Ratsche) - 8-Byte-Session-Tags (im Vergleich zu 32-Byte bei ElGamal) - Tags werden über einen synchronisierten PRNG erzeugt (nicht im Voraus gesendet) - ~92% Overhead-Reduzierung gegenüber ElGamal - Standard für modernes I2P (die meisten routers verwenden dies)

**Typen 5-6 - Post-Quanten-Hybrid**: - Kombiniert X25519 mit ML-KEM (NIST FIPS 203) - Bietet quantenresistente Sicherheit - ML-KEM-768 für ein ausgewogenes Sicherheits-/Leistungsverhältnis - ML-KEM-1024 für maximale Sicherheit - Größere Nachrichtengrößen aufgrund von Post-Quanten-Schlüsselmaterial - Netzwerkunterstützung wird noch ausgerollt

### Migrationsstrategie

Das I2P-Netzwerk stellt aktiv von ElGamal (Typ 0) auf X25519 (Typ 4) um:
- NTCP → NTCP2 (abgeschlossen)
- SSU → SSU2 (abgeschlossen)
- ElGamal tunnels → X25519 tunnels (abgeschlossen)
- ElGamal Ende-zu-Ende → ECIES-X25519 (größtenteils abgeschlossen)

## LeaseSet2 und erweiterte Funktionen

### LeaseSet2-Optionen (seit 0.9.38)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetType</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Specifies LeaseSet variant (1, 3, 5, 7)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetEncType</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Encryption types supported (comma-separated)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetAuthType</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.41</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Per-client authentication: 0 = none, 1 = DH, 2 = PSK</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetPrivKey</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.41</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">X25519 private key for decrypting LS2 with auth</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetSecret</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Base64 secret for blinded addresses</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetTransientPublicKey</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Transient signing key for offline signatures</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetPrivateKey</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Persistent LeaseSet encryption keys (type:key pairs)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetOption.nnn</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Service records (proposal 167)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetClient.dh.nnn</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.41</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DH client auth material (indexed from 0)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetClient.psk.nnn</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.41</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">PSK client auth material (indexed from 0)</td>
    </tr>
  </tbody>
</table>
### Verblindete Adressen

Seit 0.9.39 können destinations (Ziele) "blinded" (verschleiert) Adressen (b33-Format) verwenden, die sich periodisch ändern: - Erfordert `i2cp.leaseSetSecret` für Passwortschutz - Optionale Authentifizierung pro Client - Siehe Proposals 123 und 149 für Details

### Diensteinträge (seit 0.9.66)

LeaseSet2 unterstützt Service-Record-Optionen (Vorschlag 167):

```
i2cp.leaseSetOption.0=_smtp._tcp=1 86400 0 0 25 mail.example.b32.i2p
```
Format folgt dem DNS-SRV-Record-Stil, ist jedoch für I2P angepasst.

## Mehrere Sitzungen (seit 0.9.21)

Eine einzelne I2CP-Verbindung kann mehrere Sitzungen verwalten:

**Primäre Sitzung**: Die erste auf einer Verbindung erstellte Sitzung **Untersitzungen**: Zusätzliche Sitzungen, die sich den tunnel pool (Tunnel-Pool) der primären Sitzung teilen

### Eigenschaften der Subsession (Teilsitzung)

1. **Gemeinsame Tunnels**: Verwenden dieselben eingehenden/ausgehenden tunnel-Pools wie die primäre Sitzung
2. **Gemeinsame Verschlüsselungsschlüssel**: Müssen identische LeaseSet-Verschlüsselungsschlüssel verwenden
3. **Unterschiedliche Signaturschlüssel**: Müssen unterschiedliche Destination-Signaturschlüssel (I2P-Zieladresse) verwenden
4. **Keine Anonymitätsgarantie**: Eindeutig mit der primären Sitzung verknüpft (gleicher router, gleiche tunnels)

### Anwendungsfall für Subsession (Teilsitzung)

Ermöglicht die Kommunikation mit Destinations (Ziele) unter Verwendung unterschiedlicher Signaturtypen: - Primär: EdDSA-Signatur (modern) - Subsession (Teilsitzung): DSA-Signatur (Abwärtskompatibilität)

### Lebenszyklus der Subsession (Teilsitzung)

**Erstellung**:

```
Client → Router: CreateSessionMessage
Router → Client: SessionStatusMessage (unique Session ID)
Router → Client: RequestVariableLeaseSetMessage (separate for each destination)
Client → Router: CreateLeaseSet2Message (separate for each destination)
```
**Beendigung**: - Das Beenden einer subsession (Unter-Sitzung): Lässt die primary session (primäre Sitzung) intakt - Das Beenden der primary session: Beendet alle subsessions und schließt die Verbindung - DisconnectMessage (Trennnachricht): Beendet alle Sitzungen

### Umgang mit der Sitzungs-ID

Die meisten I2CP-Nachrichten enthalten ein Session-ID-Feld. Ausnahmen: - DestLookup / DestReply (veraltet, verwenden Sie HostLookup / HostReply) - GetBandwidthLimits / BandwidthLimits (Antwort nicht sitzungsspezifisch)

**Wichtig**: Clients sollten nicht mehrere CreateSession-Nachrichten gleichzeitig offen haben, da Antworten nicht eindeutig den Anfragen zugeordnet werden können.

## Nachrichtenkatalog

### Übersicht der Nachrichtentypen

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Direction</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">CreateSession</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ReconfigureSession</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DestroySession</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">CreateLeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SendMessage</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ReceiveMessageBegin</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ReceiveMessageEnd</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">GetBandwidthLimits</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SessionStatus</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">21</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">RequestLeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">22</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">MessageStatus</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">23</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">BandwidthLimits</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">29</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ReportAbuse</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bidirectional</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unused</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">30</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Disconnect</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bidirectional</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">31</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">MessagePayload</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">GetDate</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">33</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SetDate</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">34</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DestLookup</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">35</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DestReply</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">36</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SendMessageExpires</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">37</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">RequestVariableLeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">38</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">HostLookup</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.11</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">39</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">HostReply</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.11</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">41</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">CreateLeaseSet2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">42</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">BlindingInfo</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.43</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
  </tbody>
</table>
**Legende**: C = Client, R = Router

### Details zur Schlüsselnachricht

#### CreateSessionMessage (Typ 1)

**Zweck**: Starten einer neuen I2CP-Sitzung

**Inhalt**: SessionConfig-Struktur

**Antwort**: SessionStatusMessage (status=Created oder Invalid)

**Anforderungen**: - Das Datum in SessionConfig muss innerhalb von ±30 Sekunden der router‑Zeit liegen - Das Mapping muss zur Signaturvalidierung nach Schlüssel sortiert sein - Destination (Zieladresse in I2P) darf nicht bereits eine aktive Sitzung haben

#### RequestVariableLeaseSetMessage (Typ 37)

**Zweck**: Router fordert eine Client-Autorisierung für eingehende tunnels an

**Inhalt**: - Sitzungs-ID - Anzahl der Leases (zeitlich befristete Verbindungs-Einträge) - Array von Lease-Strukturen (jede mit individueller Ablaufzeit)

**Antwort**: CreateLeaseSet2Message

**Bedeutung**: Dies ist das Signal, dass die Sitzung betriebsbereit ist. Der router sendet dies erst, nachdem: 1. Mindestens ein eingehender tunnel aufgebaut ist 2. Mindestens ein ausgehender tunnel aufgebaut ist

**Timeout-Empfehlung**: Clients sollten die Sitzung beenden, wenn diese Nachricht nicht innerhalb von 5+ Minuten nach Erstellung der Sitzung empfangen wird.

#### CreateLeaseSet2Message (Typ 41)

**Zweck**: Der Client veröffentlicht das LeaseSet in der Netzwerkdatenbank

**Inhalt**: - Sitzungs-ID - LeaseSet-Typ-Byte (1, 3, 5 oder 7) - LeaseSet oder LeaseSet2 oder EncryptedLeaseSet oder MetaLeaseSet - Anzahl der privaten Schlüssel - Liste privater Schlüssel (je ein privater Schlüssel pro öffentlichem Schlüssel in LeaseSet, gleiche Reihenfolge)

**Private Schlüssel**: Erforderlich zum Entschlüsseln eingehender Garlic-Nachrichten. Format:

```
Encryption type (2 bytes)
Key length (2 bytes)
Private key data (variable)
```
**Hinweis**: Ersetzt die veraltete CreateLeaseSetMessage (Typ 4), die Folgendes nicht unterstützt: - LeaseSet2-Varianten - Nicht-ElGamal-Verschlüsselung - Mehrere Verschlüsselungstypen - Verschlüsselte LeaseSets - Offline-Signaturschlüssel

#### SendMessageExpiresMessage (Typ 36)

**Zweck**: Nachricht mit Ablaufzeit und erweiterten Optionen an das Ziel senden

**Inhalt**: - Sitzungs-ID - Destination (Zieladresse) - Nutzlast (gzip-komprimiert) - Nonce (einmalig verwendete Zufallszahl) (4 Bytes) - Flags (2 Bytes) - siehe unten - Ablaufdatum (6 Bytes, von 8 gekürzt)

**Flags-Feld** (2 Bytes, Bitreihenfolge 15...0):

**Bits 15-11**: Unbenutzt, müssen 0 sein

**Bits 10-9**: Übersteuerung der Nachrichtenzuverlässigkeit (ungenutzt, stattdessen nonce (Einmalwert) verwenden)

**Bit 8**: LeaseSet nicht bündeln - 0: Router darf LeaseSet in garlic bündeln - 1: LeaseSet nicht bündeln

**Bits 7-4**: Unterer Tag-Schwellenwert (nur ElGamal, für ECIES ignoriert)

```
0000 = Use session settings
0001 = 2 tags
0010 = 3 tags
...
1111 = 192 tags
```
**Bits 3-0**: Tags, die bei Bedarf gesendet werden (nur für ElGamal, bei ECIES ignoriert)

```
0000 = Use session settings
0001 = 2 tags
0010 = 4 tags
...
1111 = 160 tags
```
#### MessageStatusMessage (Typ 22)

**Zweck**: Benachrichtigung des Clients über den Zustellstatus der Nachricht

**Inhalt**: - Sitzungs-ID - Nachrichten-ID (vom router generiert) - Statuscode (1 Byte) - Größe (4 Bytes, nur relevant für status=0) - Nonce (4 Bytes, entspricht der SendMessage-Nonce des Clients)

**Statuscodes** (Ausgehende Nachrichten):

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Meaning</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Result</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Accepted</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Router accepted message</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Success</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Best Effort Success</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Probable delivery</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Success</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Guaranteed Success</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Probable delivery</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Success</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Local Success</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Delivered to local client</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Success</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Best Effort Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Probable failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Guaranteed Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Generic failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Local Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Local delivery failed</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Router Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Router shutdown/error</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">9</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Network Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No network connectivity</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Session</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Invalid/closed session</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Message</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Invalid payload</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Options</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Invalid options/expiration</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">13</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Overflow Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Queue/buffer full</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">14</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Message Expired</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Expired before send</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">15</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Local LeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Local LeaseSet problem</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">16</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No Local Tunnels</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No tunnels available</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">17</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unsupported Encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Incompatible encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Invalid remote destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Leaseset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Invalid remote LeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Expired Leaseset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Remote LeaseSet expired</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">21</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No Leaseset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Remote LeaseSet not found</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">22</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Meta Leaseset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Cannot send to meta LS</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">23</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Loopback Denied</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Same source and destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
  </tbody>
</table>
**Erfolgscodes**: 1, 2, 4, 6 **Fehlercodes**: Alle anderen

**Statuscode 0** (VERALTET): Verfügbare Nachricht (eingehend, schneller Empfang deaktiviert)

#### HostLookupMessage (Typ 38)

**Zweck**: Destination (Zieladresse) anhand von Hostname oder Hash auflösen (ersetzt DestLookup)

**Inhalt**: - Sitzungs-ID (oder 0xFFFF für keine Sitzung) - Anfrage-ID (4 Bytes) - Timeout in Millisekunden (4 Bytes, empfohlener Mindestwert: 10000) - Anfragetyp (1 Byte) - Lookup-Schlüssel (Hash, Hostname-String oder Destination (I2P‑Zieladresse))

**Anfragetypen**:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Lookup Key</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Returns</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Hash</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Hostname String</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Hash</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination + Options</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Hostname String</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination + Options</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination + Options</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td>
    </tr>
  </tbody>
</table>
Typen 2-4 geben LeaseSet-Optionen (Vorschlag 167) zurück, falls verfügbar.

**Antwort**: HostReplyMessage

#### HostReplyMessage (Typ 39)

**Zweck**: Antwort auf HostLookupMessage (Nachricht zur Hostauflösung)

**Inhalt**: - Sitzungs-ID - Anfrage-ID - Ergebniscode (1 Byte) - Ziel (vorhanden bei Erfolg, manchmal bei bestimmten Fehlern) - Zuordnung (nur für Lookup-Typen 2-4, kann leer sein)

**Ergebniscodes**:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Meaning</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Success</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Lookup succeeded</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Generic failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Lookup Password Required</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded address requires password</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Private Key Required</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded address requires private key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Password and Key Required</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded address requires both</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet Decryption Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Cannot decrypt LeaseSet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet Lookup Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet not found in netdb</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Lookup Type Unsupported</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Router doesn't support this type</td>
    </tr>
  </tbody>
</table>
#### BlindingInfoMessage (Typ 42)

**Zweck**: Den router über die Authentifizierungsanforderungen für blinded destination (geblindete Destination) informieren (seit 0.9.43)

**Inhalt**: - Sitzungs-ID - Flags (1 Byte) - Endpunkttyp (1 Byte): 0=Hash, 1=hostname, 2=Destination, 3=SigType+Key - Typ der geblendeten Signatur (2 Bytes) - Ablaufzeit (4 Bytes, Sekunden seit der Unix-Epoche) - Endpunktdaten (abhängig vom Typ) - Privater Schlüssel (32 Bytes, nur wenn Flag-Bit 0 gesetzt ist) - Lookup-Passwort (String, nur wenn Flag-Bit 4 gesetzt ist)

**Flags** (Bitreihenfolge 76543210):

- **Bit 0**: 0=alle, 1=pro Client
- **Bits 3-1**: Authentifizierungsschema (wenn Bit 0=1): 000=DH, 001=PSK
- **Bit 4**: 1=Secret (gemeinsames Geheimnis) erforderlich
- **Bits 7-5**: Ungenutzt, auf 0 setzen

**Keine Antwort**: Router verarbeitet stillschweigend

**Anwendungsfall**: Bevor an eine blinded destination (verschleiertes Ziel; b33 address) gesendet wird, muss der Client entweder: 1. die b33 via HostLookup auflösen, ODER 2. eine BlindingInfo-Nachricht senden

Wenn das Ziel eine Authentifizierung erfordert, ist BlindingInfo (Verblindungsinformationen) obligatorisch.

#### ReconfigureSessionMessage (Nachricht zur Neukonfiguration einer Sitzung) (Typ 2)

**Zweck**: Sitzungskonfiguration nach der Erstellung aktualisieren

**Inhalt**: - Sitzungs-ID - SessionConfig (nur geänderte Optionen erforderlich)

**Antwort**: SessionStatusMessage (status=Updated oder Invalid)

**Hinweise**: - Der Router führt neue Konfiguration mit der bestehenden zusammen - Tunnel-Optionen (`inbound.*`, `outbound.*`) werden immer angewendet - Einige Optionen können nach der Erstellung der Sitzung unveränderlich sein - Das Datum muss innerhalb von ±30 Sekunden der Routerzeit liegen - Die Zuordnung muss nach Schlüssel sortiert sein

#### DestroySessionMessage (Typ 3)

**Zweck**: Eine Sitzung beenden

**Inhalt**: Sitzungs-ID

**Erwartete Antwort**: SessionStatusMessage (status=Destroyed)

**Tatsächliches Verhalten** (Java I2P bis einschließlich 0.9.66): - Router sendet nie SessionStatus(Destroyed) - Wenn keine Sitzungen verbleiben: sendet DisconnectMessage - Wenn subsessions (Untersitzungen) verbleiben: Keine Antwort

**Wichtig**: Das Verhalten von Java I2P weicht von der Spezifikation ab. Implementierungen sollten beim Zerstören einzelner Subsessions (Teilsitzungen) vorsichtig sein.

#### DisconnectMessage (Typ 30)

**Zweck**: Mitteilen, dass die Verbindung in Kürze beendet wird

**Inhalt**: Begründungstext

**Auswirkung**: Alle Sitzungen auf der Verbindung werden beendet, der Socket wird geschlossen

**Implementierung**: Hauptsächlich router → Client in Java I2P

## Versionshistorie des Protokolls

### Versionserkennung

Die I2CP-Protokollversion wird über Get/SetDate-Nachrichten ausgetauscht (seit 0.8.7). Für ältere routers sind keine Versionsinformationen verfügbar.

**Versions-String**: Gibt die "core"-API-Version an, nicht unbedingt die router-Version.

### Zeitlinie der Funktionen

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Features</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.67</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">PQ Hybrid ML-KEM (enc types 5-7) in LeaseSet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.66</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Host lookup/reply extensions (proposal 167), service records</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.62</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">MessageStatus loopback error code</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.46</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">X25519 (enc type 4) in LeaseSet, ECIES end-to-end</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.43</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">BlindingInfo message, extended HostReply failure codes</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.41</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet options, Meta LS error code</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.39</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">CreateLeaseSet2 message, RedDSA Ed25519 support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.38</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Preliminary LS2 support (format changed in 0.9.39)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.21</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Multiple sessions on single connection</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.20</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Additional SetDate messages for clock shifts</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.16</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Authentication required before other messages (when enabled)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.15</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA Ed25519 signature type</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.14</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Per-message reliability override with nonzero nonce</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.12</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA P-256/384/521 signature types, RSA support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.11</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">HostLookup/HostReply messages, auth in GetDate</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.7</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">RequestVariableLeaseSet message</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.5</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Additional MessageStatus codes</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.4</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Fast receive mode default, nonce=0 allowed</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SendMessageExpires flag tag bits</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">16 leases per LeaseSet (up from 6)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.8.7</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Version strings in Get/SetDate</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.8.4</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SendMessageExpires flag bits</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.8.3</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DestLookup in standard session, concurrent lookups</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.8.1</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>messageReliability=none</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.7.2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">GetBandwidthLimits, BandwidthLimits</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.7.1</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SendMessageExpires, ReconfigureSession, ports in gzip header</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.7</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DestLookup, DestReply</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.6.5-</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Original protocol features</td>
    </tr>
  </tbody>
</table>
## Sicherheitsaspekte

### Authentifizierung

**Standard**: Keine Authentifizierung erforderlich **Optional**: Authentifizierung mit Benutzername/Passwort (seit 0.9.11) **Erforderlich**: Wenn aktiviert, muss die Authentifizierung vor anderen Nachrichten abgeschlossen werden (seit 0.9.16)

**Remote-Verbindungen**: Verwenden Sie immer TLS (`i2cp.SSL=true`), um Anmeldedaten und private Schlüssel zu schützen.

### Uhrzeitabweichung

SessionConfig Date muss innerhalb von ±30 Sekunden von der router-Zeit liegen, andernfalls wird die Sitzung abgelehnt. Verwenden Sie Get/SetDate zur Synchronisierung.

### Umgang mit privaten Schlüsseln

CreateLeaseSet2Message enthält private Schlüssel zum Entschlüsseln eingehender Nachrichten. Diese Schlüssel müssen: - Sicher übertragen werden (TLS für Remote-Verbindungen) - Sicher vom router gespeichert werden - Rotiert werden, wenn sie kompromittiert sind

### Ablaufzeit von Nachrichten

Verwenden Sie immer SendMessageExpires (nicht SendMessage), um eine explizite Ablaufzeit festzulegen. Dadurch: - Verhindert, dass Nachrichten unbegrenzt in der Warteschlange verbleiben - Reduziert den Ressourcenverbrauch - Verbessert die Zuverlässigkeit

### Verwaltung von Session Tags (Sitzungs-Tags)

**ElGamal** (veraltet): - Tags (Markierungen) müssen in Batches übertragen werden - Verlorene Tags führen zu Entschlüsselungsfehlern - Hoher Speicheraufwand

**ECIES-X25519** (aktuell): - Tags (Kennungen), die mit einem synchronisierten Pseudozufallszahlengenerator erzeugt werden - Keine vorherige Übertragung erforderlich - Widerstandsfähig gegenüber Nachrichtenverlust - Deutlich geringerer Overhead

## Bewährte Verfahren

### Für Client-Entwickler

1. **Schnellen Empfangsmodus verwenden**: Setze immer `i2cp.fastReceive=true` (oder verwende die Voreinstellung)

2. **ECIES-X25519 (Elliptic Curve Integrated Encryption Scheme mit X25519) bevorzugen**: Konfigurieren Sie `i2cp.leaseSetEncType=4,0` für optimale Leistung bei gleichzeitiger Kompatibilität

3. **Explizites Ablaufdatum festlegen**: Verwenden Sie SendMessageExpires, nicht SendMessage

4. **Subsessions vorsichtig handhaben**: Beachten Sie, dass Subsessions (Untersitzungen) zwischen Destinations keine Anonymität bieten

5. **Zeitüberschreitung bei der Sitzungserstellung**: Sitzung verwerfen, wenn RequestVariableLeaseSet nicht innerhalb von 5 Minuten empfangen wird

6. **Konfigurations-Mappings sortieren**: Sortieren Sie die Mapping-Schlüssel immer, bevor Sie SessionConfig signieren

7. **Verwenden Sie eine angemessene Anzahl der Tunnel**: Setzen Sie `quantity` nicht > 6, es sei denn, es ist erforderlich

8. **SAM/BOB für Nicht-Java in Betracht ziehen**: Implementieren Sie SAM, anstatt I2CP direkt zu implementieren

### Für Router-Entwickler

1. **Datumsangaben validieren**: ±30‑Sekunden-Fenster für die SessionConfig-Datumsangaben erzwingen

2. **Nachrichtengröße begrenzen**: Maximale Nachrichtengröße von ~64 KB erzwingen

3. **Unterstützung mehrerer Sitzungen**: Subsession-Unterstützung gemäß Spezifikation 0.9.21 implementieren

4. **RequestVariableLeaseSet (Anforderung für ein variables leaseSet) umgehend senden**: Erst nachdem sowohl eingehende als auch ausgehende tunnels vorhanden sind

5. **Veraltete Nachrichten behandeln**: ReceiveMessageBegin/End akzeptieren, aber von ihrer Verwendung abraten

6. **ECIES-X25519 unterstützen**: Verschlüsselungstyp 4 für neue Bereitstellungen priorisieren

## Debugging und Fehlerbehebung

### Häufige Probleme

**Sitzung abgelehnt (ungültig)**: - Uhrzeitabweichung prüfen (muss innerhalb von ±30 Sekunden liegen) - Überprüfen, dass die Zuordnung nach Schlüssel sortiert ist - Sicherstellen, dass die Destination nicht bereits in Verwendung ist

**Kein RequestVariableLeaseSet**: - Router baut möglicherweise tunnels (Warten Sie bis zu 5 Minuten) - Prüfen Sie auf Probleme mit der Netzwerkverbindung - Überprüfen Sie, ob ausreichend Peer-Verbindungen bestehen

**Fehler bei der Nachrichtenübermittlung**: - MessageStatus-Codes auf den spezifischen Fehlergrund prüfen - Überprüfen, ob das entfernte LeaseSet veröffentlicht und aktuell ist - Kompatible Verschlüsselungstypen sicherstellen

**Subsession-Probleme (Teilsitzung)**: - Überprüfen, dass die primäre Sitzung zuerst erstellt wurde - Bestätigen, dass die gleichen Verschlüsselungsschlüssel verwendet werden - Prüfen, ob unterschiedliche Signaturschlüssel vorhanden sind

### Diagnosemeldungen

**GetBandwidthLimits**: router-Kapazität abfragen **HostLookup**: Namensauflösung und LeaseSet-Verfügbarkeit testen **MessageStatus**: Nachrichtenübermittlung Ende-zu-Ende nachverfolgen

## Verwandte Spezifikationen

- **Gemeinsame Strukturen**: /docs/specs/common-structures/
- **I2NP (Netzwerkprotokoll)**: /docs/specs/i2np/
- **ECIES-X25519**: /docs/specs/ecies/
- **Tunnel-Erstellung**: /docs/specs/implementation/
- **Streaming-Bibliothek**: /docs/specs/streaming/
- **Datagramm-Bibliothek**: /docs/api/datagrams/
- **SAM v3**: /docs/api/samv3/

## Referenzierte Vorschläge

- [Vorschlag 123](/proposals/123-new-netdb-entries/): Verschlüsselte LeaseSets und Authentifizierung
- [Vorschlag 144](/proposals/144-ecies-x25519-aead-ratchet/): ECIES-X25519-AEAD-Ratchet
- [Vorschlag 149](/proposals/149-b32-encrypted-ls2/): Geblendetes Adressformat (b33)
- [Vorschlag 152](/proposals/152-ecies-tunnels/): X25519 tunnel-Erstellung
- [Vorschlag 154](/proposals/154-ecies-lookups/): Datenbankabfragen von ECIES-Destinationen
- [Vorschlag 156](/proposals/156-ecies-routers/): Router-Migration auf ECIES-X25519
- [Vorschlag 161](/de/proposals/161-ri-dest-padding/): Komprimierung des Destination-Padding
- [Vorschlag 167](/proposals/167-service-records/): LeaseSet-Serviceeinträge
- [Vorschlag 169](/proposals/169-pq-crypto/): Post-quantische hybride Kryptografie (ML-KEM)

## Javadoc-Referenz

- [I2CP-Paket](http://docs.i2p-projekt.de/javadoc/net/i2p/data/i2cp/package-summary.html)
- [MessageStatusMessage](http://docs.i2p-projekt.de/javadoc/net/i2p/data/i2cp/MessageStatusMessage.html)
- [Client-API](http://docs.i2p-projekt.de/javadoc/net/i2p/client/package-summary.html)

## Abkündigungsübersicht

### Veraltete Nachrichten (nicht verwenden)

- **CreateLeaseSetMessage** (Typ 4): Verwende CreateLeaseSet2Message
- **RequestLeaseSetMessage** (Typ 21): Verwende RequestVariableLeaseSetMessage
- **ReceiveMessageBeginMessage** (Typ 6): Verwende schnellen Empfangsmodus
- **ReceiveMessageEndMessage** (Typ 7): Verwende schnellen Empfangsmodus
- **DestLookupMessage** (Typ 34): Verwende HostLookupMessage
- **DestReplyMessage** (Typ 35): Verwende HostReplyMessage
- **ReportAbuseMessage** (Typ 29): Nie implementiert

### Veraltete Optionen

- ElGamal-Verschlüsselung (Typ 0): Umstellung auf ECIES-X25519 (Typ 4)
- DSA-Signaturen: Umstellung auf EdDSA oder ECDSA
- `i2cp.fastReceive=false`: Immer den schnellen Empfangsmodus verwenden
