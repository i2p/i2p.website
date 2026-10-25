---
title: "I2P Client Protocol (I2CP)"
description: "Wie Anwendungen Sitzungen, tunnel und leaseSet mit dem I2P router aushandeln."
slug: "i2cp"
aliases:
  - "/de/docs/api/i2cp"
  - "/de/docs/api/i2cp/"
  - "/de/docs/specs/i2cp-spec"
  - "/de/docs/specs/i2cp-spec/"
category: "Protokolle"
lastUpdated: "2025-07"
accurateFor: "0.9.67"
---

## Überblick

Dies ist die Spezifikation des I2P Control Protocol (I2CP), der Low-Level-Schnittstelle zwischen Clients und dem router. Java-Clients werden die I2CP-Client-API verwenden, die dieses Protokoll implementiert.

Es gibt keine bekannten Implementierungen einer clientseitigen Bibliothek außerhalb von Java, die I2CP implementiert. Zusätzlich benötigen socket-orientierte (streaming) Anwendungen eine Implementierung des Streaming-Protokolls, aber es gibt auch dafür keine Bibliotheken außerhalb von Java. Daher sollten Nicht-Java-Clients stattdessen das höhere Protokoll SAM [SAMv3](/docs/api/samv3/) verwenden, für das Bibliotheken in mehreren Sprachen existieren.

Dies ist ein Low-Level-Protokoll, das sowohl intern als auch extern vom Java I2P router unterstützt wird. Das Protokoll wird nur serialisiert, wenn sich Client und router nicht in derselben JVM befinden; andernfalls werden I2CP-Nachrichten-Java-Objekte über eine interne JVM-Schnittstelle übertragen. I2CP wird auch extern vom C++ router i2pd unterstützt.

Weitere Informationen finden Sie auf der I2CP-Übersichtsseite [I2CP](/docs/specs/i2cp/).

## Sitzungen

Das Protokoll wurde entwickelt, um mehrere "Sessions" mit jeweils einer 2-Byte Session-ID über eine einzelne TCP-Verbindung zu verwalten. Allerdings wurden mehrere Sessions erst ab Version 0.9.21 implementiert. Siehe den [Multisession-Abschnitt unten](#multisession). Versuchen Sie nicht, mehrere Sessions auf einer einzelnen I2CP-Verbindung mit Routern zu verwenden, die älter als Version 0.9.21 sind.

Es scheint auch, dass es einige Vorkehrungen dafür gibt, dass ein einzelner Client über separate Verbindungen mit mehreren Routern kommunizieren kann. Dies ist ebenfalls ungetestet und wahrscheinlich nicht nützlich.

Es gibt keine Möglichkeit, eine Session nach einer Trennung aufrechtzuerhalten oder sie über eine andere I2CP-Verbindung wiederherzustellen. Wenn der Socket geschlossen wird, wird die Session zerstört.

## Beispiel-Nachrichtensequenzen

Hinweis: Die folgenden Beispiele zeigen nicht das Protokoll-Byte (0x2a), das vom Client an den router gesendet werden muss, wenn zum ersten Mal eine Verbindung hergestellt wird. Weitere Informationen zur Verbindungsinitialisierung finden Sie auf der I2CP-Übersichtsseite [I2CP](/docs/specs/i2cp/).

### Standard-Sitzungsaufbau

```
  Client                                           Router

                           --------------------->  Get Date Message
        Set Date Message  <---------------------
                           --------------------->  Create Session Message
  Session Status Message  <---------------------
Request LeaseSet Message  <---------------------
                           --------------------->  Create LeaseSet Message

```
### Bandbreitenlimits abrufen (Einfache Sitzung)

```
  Client                                           Router

                           --------------------->  Get Bandwidth Limits Message
Bandwidth Limits Message  <---------------------

```
### Ziel-Lookup (Einfache Sitzung)

```
  Client                                           Router

                           --------------------->  Dest Lookup Message
      Dest Reply Message  <---------------------

```
### Ausgehende Nachricht

Bestehende Sitzung, mit i2cp.messageReliability=none

```
  Client                                           Router

                           --------------------->  Send Message Message

```
Bestehende Sitzung, mit i2cp.messageReliability=none und von Null verschiedener Nonce

```
  Client                                           Router

                           --------------------->  Send Message Message
  Message Status Message  <---------------------
  (succeeded)

```
Bestehende Sitzung, mit i2cp.messageReliability=BestEffort

```
  Client                                           Router

                           --------------------->  Send Message Message
  Message Status Message  <---------------------
  (accepted)
  Message Status Message  <---------------------
  (succeeded)

```
### Eingehende Nachricht

Bestehende Sitzung, mit i2cp.fastReceive=true (ab 0.9.4)

```
  Client                                           Router

 Message Payload Message  <---------------------

```
Bestehende Sitzung, mit i2cp.fastReceive=false (VERALTET)

```
  Client                                           Router

  Message Status Message  <---------------------
  (available)
                           --------------------->  Receive Message Begin Message
 Message Payload Message  <---------------------
                           --------------------->  Receive Message End Message

```
### Multisession-Hinweise {#multisession}

Mehrere Sessions auf einer einzelnen I2CP-Verbindung werden ab router Version 0.9.21 unterstützt. Die erste Session, die erstellt wird, ist die "primäre Session". Zusätzliche Sessions sind "Subsessions". Subsessions werden verwendet, um mehrere Ziele zu unterstützen, die sich einen gemeinsamen Satz von tunnels teilen. Die ursprüngliche Anwendung ist, dass die primäre Session ECDSA-Signaturschlüssel verwendet, während die Subsession DSA-Signaturschlüssel für die Kommunikation mit alten eepsites nutzt.

Subsessions teilen sich die gleichen eingehenden und ausgehenden tunnel-Pools wie die primäre Session. Subsessions müssen die gleichen Verschlüsselungsschlüssel wie die primäre Session verwenden. Dies gilt sowohl für die leaseSet-Verschlüsselungsschlüssel als auch für die (nicht verwendeten) Destination-Verschlüsselungsschlüssel. Subsessions müssen unterschiedliche Signierschlüssel im Destination verwenden, sodass sich der Destination-Hash von der primären Session unterscheidet. Da Subsessions die gleichen Verschlüsselungsschlüssel und tunnel wie die primäre Session verwenden, ist für alle ersichtlich, dass die Destinations auf demselben router laufen, weshalb die üblichen Anti-Korrelations-Anonymitätsgarantien nicht gelten.

Subsessions werden durch das Senden einer CreateSession-Nachricht und den Empfang einer SessionStatus-Nachricht als Antwort erstellt, wie üblich. Subsessions müssen nach der Erstellung der primären Session erstellt werden. Die SessionStatus-Antwort wird bei Erfolg eine eindeutige Session-ID enthalten, die sich von der ID der primären Session unterscheidet. Obwohl CreateSession-Nachrichten in der richtigen Reihenfolge verarbeitet werden sollten, gibt es keine sichere Möglichkeit, eine CreateSession-Nachricht mit der Antwort zu korrelieren, daher sollte ein Client nicht mehrere CreateSession-Nachrichten gleichzeitig ausstehend haben. SessionConfig-Optionen für die Subsession werden möglicherweise nicht berücksichtigt, wenn sie sich von der primären Session unterscheiden. Insbesondere können tunnel-Optionen ignoriert werden, da Subsessions denselben tunnel-Pool wie die primäre Session verwenden.

Der router wird separate RequestVariableLeaseSet-Nachrichten für jedes Destination an den Client senden, und der Client muss mit einer CreateLeaseSet-Nachricht für jedes antworten. Die leases für die beiden Destinations werden nicht unbedingt identisch sein, obwohl sie aus demselben tunnel pool ausgewählt werden.

Eine Untersitzung kann wie üblich mit der DestroySession-Nachricht zerstört werden. Dies zerstört nicht die primäre Sitzung und stoppt nicht die I2CP-Verbindung. Das Zerstören der primären Sitzung wird jedoch alle Untersitzungen zerstören und die I2CP-Verbindung stoppen. Eine Disconnect-Nachricht zerstört alle Sitzungen.

Beachte, dass die meisten, aber nicht alle, I2CP-Nachrichten eine Session ID enthalten. Für diejenigen, die keine enthalten, benötigen Clients möglicherweise zusätzliche Logik, um Router-Antworten ordnungsgemäß zu verarbeiten. DestLookup und DestReply enthalten keine Session IDs; verwende stattdessen die neueren HostLookup und HostReply. GetBandwidthLimts und BandwidthLimits enthalten keine Session IDs, jedoch ist die Antwort nicht session-spezifisch.

### Versionshinweise {#notes}

Das anfängliche Protokollversionsbyte (0x2a), das vom Client gesendet wird, wird voraussichtlich nicht geändert. Vor der Version 0.8.7 waren die Versionsinformationen des routers für den Client nicht verfügbar, was verhinderte, dass neue Clients mit alten routern funktionieren. Ab Version 0.8.7 werden die Protokollversionszeichenketten beider Parteien in den Get/Set Date Messages ausgetauscht. In Zukunft können Clients diese Informationen nutzen, um korrekt mit alten routern zu kommunizieren. Clients und router sollten keine Nachrichten senden, die von der anderen Seite nicht unterstützt werden, da sie die Sitzung beim Empfang einer nicht unterstützten Nachricht normalerweise trennen.

Die ausgetauschten Versionsinformationen sind die "Kern"-API-Version oder I2CP-Protokollversion und entsprechen nicht zwangsläufig der Router-Version.

Eine grundlegende Zusammenfassung der I2CP-Protokollversionen ist wie folgt. Für Details siehe unten.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Version</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Required I2CP Features</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.67</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">PQ Hybrid ML-KEM (enc types 5-7) supported in LS</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Host lookup/reply extensions (see proposal 167)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.62</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">MessageStatus message Loopback error code</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.46</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">X25519 (enc type 4) supported in LS</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.43</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">BlindingInfo message supported; Additional HostReply message failure codes</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">EncryptedLeaseSet options; MessageStatus message Meta LS error code</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.39</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">CreateLeaseSet2 message and options supported; Dest/LS key certs w/ RedDSA Ed25519 sig type supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Preliminary CreateLeaseSet2 message supported (abandoned)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.21</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Multiple sessions on a single I2CP connection supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.20</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Additional SetDate messages may be sent to the client at any time</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.16</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Authentication, if enabled, is required via GetDate before all other messages</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.15</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest/LS key certs w/ EdDSA Ed25519 sig type supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.14</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Per-message override of messageReliability=none with nonzero nonce</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest/LS key certs w/ ECDSA P-256, P-384, and P-521 sig types supported; RSA sig types also supported but currently unused</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Host Lookup and Host Reply messages supported; Authentication mapping in Get Date message supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Request Variable Lease Set message supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Additional Message Status codes defined</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Send Message nonce=0 allowed; Fast receive mode is the default</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Send Message Expires flag tag bits supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Supports up to 16 leases in a lease set (6 previously)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Get Date and Set Date version strings included. If not present, the client or router is version 0.8.6 or older.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Send Message Expires flag bits supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest Lookup and Get Bandwidth messages supported in standard session; Concurrent Dest Lookup messages supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.messageReliability=none supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Get Bandwidth Limits and Bandwidth Limits messages supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Send Message Expires message supported; Reconfigure Session message supported; Ports and protocol numbers in gzip header</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest Lookup and Dest Reply messages supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.6.5 or lower</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">All messages and features not listed above</td>
</tr>
</table>
## Gemeinsame Strukturen {#structures}

### I2CP Nachrichtenkopf {#struct-I2CPMessageHeader}

#### Beschreibung

Gemeinsamer Header für alle I2CP-Nachrichten, der die Nachrichtenlänge und den Nachrichtentyp enthält.

#### Inhaltsverzeichnis

1.  4 Byte [Integer](/docs/specs/common-structures/#integer), der die Länge des
    Nachrichtenkörpers angibt
2.  1 Byte [Integer](/docs/specs/common-structures/#integer), der den Nachrichtentyp
    angibt.
3.  Der I2CP Nachrichtenkörper, 0 oder mehr Bytes

#### Notizen

Die tatsächliche Nachrichtenlängenbegrenzung liegt bei etwa 64 KB.

### Message ID {#struct-MessageId}

#### Beschreibung

Identifiziert eindeutig eine Nachricht, die zu einem bestimmten Zeitpunkt auf einem bestimmten router wartet. Diese wird immer vom router generiert und ist NICHT dieselbe wie die vom Client generierte Nonce.

#### Inhaltsverzeichnis

1.  4 Byte [Integer](/docs/specs/common-structures/#integer)

#### Hinweise

Nachrichten-IDs sind nur innerhalb einer Sitzung eindeutig; sie sind nicht global eindeutig.

### Payload {#struct-Payload}

#### Beschreibung

Diese Struktur ist der Inhalt einer Nachricht, die von einer Destination zu einer anderen übermittelt wird.

#### Inhalt

1.  4 Byte [Integer](/docs/specs/common-structures/#integer) Länge
2.  So viele Bytes

#### Notizen

Die Nutzdaten sind im gzip-Format wie auf der I2CP-Übersichtsseite [I2CP-FORMAT](/docs/specs/i2cp/#format) spezifiziert.

Die tatsächliche Nachrichtenlängenbegrenzung liegt bei etwa 64 KB.

### Session-Konfiguration {#struct-SessionConfig}

#### Beschreibung

Definiert die Konfigurationsoptionen für eine bestimmte Client-Sitzung.

#### Inhalt

1.  [Destination](/docs/specs/common-structures/#destination)
2.  [Mapping](/docs/specs/common-structures/#mapping) der Optionen
3.  Erstellungs-[Date](/docs/specs/common-structures/#date)
4.  [Signature](/docs/specs/common-structures/#signature) der vorherigen 3 Felder,
    signiert durch den [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey)

#### Notizen

- Die Optionen sind auf der I2CP-Übersichtsseite
  [I2CP-OPTIONS](/docs/specs/i2cp/#options) angegeben.
- Das [Mapping](/docs/specs/common-structures/#mapping) muss nach Schlüssel sortiert sein, damit
  die Signatur im router korrekt validiert wird.
- Das Erstellungsdatum muss innerhalb von +/- 30 Sekunden der aktuellen Zeit
  liegen, wenn es vom router verarbeitet wird, andernfalls wird die Konfiguration abgelehnt.

#### Offline-Signaturen

- Wenn die [Destination](/docs/specs/common-structures/#destination) offline signiert ist,
  muss das [Mapping](/docs/specs/common-structures/#mapping) die drei Optionen
  i2cp.leaseSetOfflineExpiration, i2cp.leaseSetTransientPublicKey und
  i2cp.leaseSetOfflineSignature enthalten. Die
  [Signature](/docs/specs/common-structures/#signature) wird dann vom
  temporären [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey) generiert und
  mit dem [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) verifiziert, der in
  i2cp.leaseSetTransientPublicKey angegeben ist. Siehe
  [I2CP-OPTIONS](/docs/specs/i2cp/#options) für Details.

### Session ID {#struct-SessionId}

#### Beschreibung

Identifiziert eindeutig eine Sitzung auf einem bestimmten Router zu einem bestimmten Zeitpunkt.

#### Inhalt

1.  2 Byte [Integer](/docs/specs/common-structures/#integer)

#### Hinweise

Session ID 0xffff wird verwendet, um "keine Session" anzuzeigen, beispielsweise für Hostname-Lookups.

## Nachrichten

Siehe auch die [I2CP Javadocs](http://javadoc.i2p.net/net/i2p/data/i2cp/package-summary.html).

### Nachrichtentypen {#types}

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Message</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Direction</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Since</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#BandwidthLimitsMessage">BandwidthLimitsMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">23</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.2</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#BlindingInfoMessage">BlindingInfoMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">42</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.43</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#CreateLeaseSetMessage">CreateLeaseSetMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#CreateLeaseSet2Message">CreateLeaseSet2Message</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.39</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#CreateSessionMessage">CreateSessionMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#DestLookupMessage">DestLookupMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">34</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#DestReplyMessage">DestReplyMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">35</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#DestroySessionMessage">DestroySessionMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#DisconnectMessage">DisconnectMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">bidir.</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">30</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#GetBandwidthLimitsMessage">GetBandwidthLimitsMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.2</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#GetDateMessage">GetDateMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#HostLookupMessage">HostLookupMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.11</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#HostReplyMessage">HostReplyMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">39</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.11</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#MessagePayloadMessage">MessagePayloadMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">31</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#MessageStatusMessage">MessageStatusMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">22</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#ReceiveMessageBeginMessage">ReceiveMessageBeginMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#ReceiveMessageEndMessage">ReceiveMessageEndMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#ReconfigureSessionMessage">ReconfigureSessionMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#ReportAbuseMessage">ReportAbuseMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">bidir.</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">29</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#RequestLeaseSetMessage">RequestLeaseSetMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">21</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#RequestVariableLeaseSetMessage">RequestVariableLeaseSetMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">37</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#SendMessageMessage">SendMessageMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#SendMessageExpiresMessage">SendMessageExpiresMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">36</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#SessionStatusMessage">SessionStatusMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">20</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#SetDateMessage">SetDateMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">33</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
</table>
### BandwidthLimitsMessage {#BandwidthLimitsMessage}

#### Beschreibung

Teile dem Client die Bandbreitenbeschränkungen mit.

Vom Router an den Client als Antwort auf eine [GetBandwidthLimitsMessage](#GetBandwidthLimitsMessage) gesendet.

#### Inhalt

1.  4 Byte [Integer](/docs/specs/common-structures/#integer) Client eingehend Limit
    (KBps)
2.  4 Byte [Integer](/docs/specs/common-structures/#integer) Client ausgehend Limit
    (KBps)
3.  4 Byte [Integer](/docs/specs/common-structures/#integer) Router eingehend Limit
    (KBps)
4.  4 Byte [Integer](/docs/specs/common-structures/#integer) Router eingehend Burst-Limit
    (KBps)
5.  4 Byte [Integer](/docs/specs/common-structures/#integer) Router ausgehend Limit
    (KBps)
6.  4 Byte [Integer](/docs/specs/common-structures/#integer) Router ausgehend Burst-
    Limit (KBps)
7.  4 Byte [Integer](/docs/specs/common-structures/#integer) Router Burst-Zeit
    (Sekunden)
8.  Neun 4-Byte [Integer](/docs/specs/common-structures/#integer) (undefiniert)

#### Hinweise

Die Client-Limits können die einzigen gesetzten Werte sein und können die tatsächlichen router-Limits, oder ein Prozentsatz der router-Limits, oder spezifisch für den jeweiligen Client sein, implementierungsabhängig. Alle Werte, die als router-Limits bezeichnet sind, können 0 sein, implementierungsabhängig. Ab Release 0.7.2.

### BlindingInfoMessage {#BlindingInfoMessage}

#### Beschreibung

Teilt dem router mit, dass eine Destination geblendet ist, mit optionalem Lookup-Passwort und optionalem privaten Schlüssel für die Entschlüsselung. Siehe Vorschläge 123 und 149 für Details.

Der router muss wissen, ob ein Ziel geblendet ist. Wenn es geblendet ist und eine geheime oder pro-Client-Authentifizierung verwendet, muss er diese Informationen ebenfalls haben.

Ein Host Lookup einer neuen b32-Adresse im Format ("b33") teilt dem Router mit, dass die Adresse geblendet ist, aber es gibt keinen Mechanismus, um das Geheimnis oder den privaten Schlüssel in der Host Lookup-Nachricht an den Router zu übermitteln. Obwohl wir die Host Lookup-Nachricht erweitern könnten, um diese Informationen hinzuzufügen, ist es sauberer, eine neue Nachricht zu definieren.

Diese Nachricht bietet dem Client eine programmgesteuerte Möglichkeit, es dem Router mitzuteilen. Andernfalls müsste der Benutzer jedes Ziel manuell konfigurieren.

#### Verwendung

Bevor ein Client eine Nachricht an ein geblindetes Ziel sendet, muss er entweder das "b33" in einer Host Lookup-Nachricht nachschlagen oder eine Blinding Info-Nachricht senden. Wenn das geblindete Ziel ein Geheimnis oder eine clientspezifische Authentifizierung erfordert, muss der Client eine Blinding Info-Nachricht senden.

Der router sendet keine Antwort auf diese Nachricht. Gesendet vom Client zum Router.

#### Inhalt

1.  [Session ID](#struct-sessionid)
2.  1 Byte [Integer](/docs/specs/common-structures/#integer) Flags

> - Bit-Reihenfolge: 76543210 > - Bit 0: 0 für alle, 1 für pro-Client > - Bits 3-1: Authentifizierungsschema, falls Bit 0 auf 1 für >   pro-Client gesetzt ist, andernfalls 000 >   - 000: DH Client-Authentifizierung (oder keine pro-Client-Authentifizierung) >   - 001: PSK Client-Authentifizierung > - Bit 4: 1 falls Geheimnis erforderlich, 0 falls kein Geheimnis erforderlich > - Bits 7-5: Unbenutzt, für zukünftige Kompatibilität auf 0 setzen

3.  1 Byte [Integer](/docs/specs/common-structures/#integer) Endpunkt-Typ

> - Typ 0 ist ein [Hash](/docs/specs/common-structures/#hash) > - Typ 1 ist ein Hostname [String](/docs/specs/common-structures/#string) > - Typ 2 ist eine [Destination](/docs/specs/common-structures/#destination) > - Typ 3 ist ein Sig Type und >   [SigningPublicKey](/docs/specs/common-structures/#signingpublickey)

4.  2 Byte [Integer](/docs/specs/common-structures/#integer) Blinded Signature Type
5.  4 Byte [Integer](/docs/specs/common-structures/#integer) Ablaufzeit in Sekunden seit
    Epoche
6.  Endpunkt: Daten wie spezifiziert, einer von

> - Typ 0: 32 Byte [Hash](/docs/specs/common-structures/#hash) > > - Typ 1: Hostname [String](/docs/specs/common-structures/#string) > > - Typ 2: binäre [Destination](/docs/specs/common-structures/#destination) > >  > >  - Typ 3: 2 Byte [Integer](/docs/specs/common-structures/#integer) Signaturtyp, gefolgt von > >  -   [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) (Länge wie >       durch Signaturtyp impliziert)

7.  [PrivateKey](/docs/specs/common-structures/#privatekey) Entschlüsselungsschlüssel Nur vorhanden,
    wenn Flag-Bit 0 auf 1 gesetzt ist. Ein 32-Byte ECIES_X25519 privater Schlüssel,
    little-endian
8.  [String](/docs/specs/common-structures/#string) Lookup-Passwort Nur vorhanden, wenn
    Flag-Bit 4 auf 1 gesetzt ist.

#### Hinweise

- Ab Release 0.9.43.
- Der Hash-Endpunkt-Typ ist wahrscheinlich nicht nützlich, es sei denn, der router kann eine Rückwärtssuche im Adressbuch durchführen, um das Destination zu erhalten.
- Der Hostname-Endpunkt-Typ ist wahrscheinlich nicht nützlich, es sei denn, der router kann eine Suche im Adressbuch durchführen, um das Destination zu erhalten.

### CreateLeaseSetMessage {#CreateLeaseSetMessage}

VERALTET. Kann nicht für LeaseSet2, Offline-Schlüssel, Nicht-ElGamal-Verschlüsselungstypen, mehrere Verschlüsselungstypen oder verschlüsselte LeaseSets verwendet werden. Verwenden Sie CreateLeaseSet2Message mit allen Routern 0.9.39 oder höher.

#### Beschreibung

Diese Nachricht wird als Antwort auf eine [RequestLeaseSetMessage](#RequestLeaseSetMessage) oder [RequestVariableLeaseSetMessage](#RequestVariableLeaseSetMessage) gesendet und enthält alle [Lease](/docs/specs/common-structures/#lease)-Strukturen, die in der I2NP Network Database veröffentlicht werden sollen.

Vom Client zum Router gesendet.

#### Inhaltsverzeichnis

1.  [Session ID](#struct-sessionid)
2.  DSA [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey) oder 20
    Bytes ignoriert
3.  [PrivateKey](/docs/specs/common-structures/#privatekey)
4.  [LeaseSet](/docs/specs/common-structures/#leaseset)

#### Notizen

Der SigningPrivateKey entspricht dem [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) aus dem LeaseSet nur dann, wenn der Signaturschlüsseltyp DSA ist. Dies dient der LeaseSet-Widerrufung, die nicht implementiert ist und wahrscheinlich niemals implementiert werden wird. Wenn der Signaturschlüsseltyp nicht DSA ist, enthält dieses Feld 20 Bytes zufälliger Daten. Die Länge dieses Feldes beträgt immer 20 Bytes, sie entspricht niemals der Länge eines privaten Signaturschlüssels, der nicht DSA ist.

Der PrivateKey entspricht dem [PublicKey](/docs/specs/common-structures/#publickey) aus dem LeaseSet. Der PrivateKey ist erforderlich für die Entschlüsselung von garlic routed Nachrichten.

Widerruf ist nicht implementiert. Die Verbindung zu mehreren Routern ist in keiner Client-Bibliothek implementiert.

### CreateLeaseSet2Message {#CreateLeaseSet2Message}

#### Beschreibung

Diese Nachricht wird als Antwort auf eine [RequestLeaseSetMessage](#RequestLeaseSetMessage) oder [RequestVariableLeaseSetMessage](#RequestVariableLeaseSetMessage) gesendet und enthält alle [Lease](/docs/specs/common-structures/#lease)-Strukturen, die in der I2NP Network Database veröffentlicht werden sollen.

Vom Client zum Router gesendet. Seit Version 0.9.39. Client-spezifische Authentifizierung für EncryptedLeaseSet wird seit 0.9.41 unterstützt. MetaLeaseSet wird noch nicht über I2CP unterstützt. Siehe Vorschlag 123 für weitere Informationen.

#### Inhaltsverzeichnis

1.  [Session ID](#struct-sessionid)
2.  Ein Byte Typ des zu folgenden leaseSet.

> - Typ 1 ist ein [LeaseSet](/docs/specs/common-structures/#leaseset) (veraltet) > - Typ 3 ist ein [LeaseSet2](/docs/specs/common-structures/#leaseset2) > - Typ 5 ist ein [EncryptedLeaseSet](/docs/specs/common-structures/#leaseset2) > - Typ 7 ist ein [MetaLeaseSet](/docs/specs/common-structures/#leaseset2)

3.  [LeaseSet](/docs/specs/common-structures/#leaseset) oder
    [LeaseSet2](/docs/specs/common-structures/#leaseset2) oder
    [EncryptedLeaseSet](/docs/specs/common-structures/#leaseset2) oder
    [MetaLeaseSet](/docs/specs/common-structures/#leaseset2)
4.  Ein Byte mit der Anzahl der folgenden privaten Schlüssel.
5.  [PrivateKey](/docs/specs/common-structures/#privatekey)-Liste. Einer für jeden öffentlichen
    Schlüssel im leaseSet, in derselben Reihenfolge. (Nicht vorhanden für Meta LS2)

> - Verschlüsselungstyp (2 Byte [Integer](/docs/specs/common-structures/#integer)) > - Verschlüsselungsschlüssel-Länge (2 Byte [Integer](/docs/specs/common-structures/#integer)) > - Verschlüsselung [PrivateKey](/docs/specs/common-structures/#privatekey) (Anzahl der >   angegebenen Bytes)

#### Notizen

Die PrivateKeys entsprechen jedem der [PublicKey](/docs/specs/common-structures/#publickey) aus dem LeaseSet. Die PrivateKeys sind notwendig für die Entschlüsselung von garlic-gerouteten Nachrichten.

Siehe Vorschlag 123 für weitere Informationen zu verschlüsselten LeaseSets.

Der Inhalt und das Format für MetaLeaseSet sind vorläufig und können sich ändern. Es ist kein Protokoll für die Verwaltung mehrerer router spezifiziert. Siehe Vorschlag 123 für weitere Informationen.

Der private Signaturschlüssel, der zuvor für den Widerruf definiert und nicht verwendet wurde, ist in LS2 nicht vorhanden.

Die vorläufige Version mit Nachrichtentyp 40 war in 0.9.38 enthalten, aber das Format wurde geändert. Typ 40 ist aufgegeben und wird nicht unterstützt. Typ 41 ist erst ab 0.9.39 gültig.

### CreateSessionMessage {#CreateSessionMessage}

#### Beschreibung

Diese Nachricht wird von einem Client gesendet, um eine Session zu initiieren, wobei eine Session als die Verbindung einer einzelnen Destination zum Netzwerk definiert ist, über die alle Nachrichten für diese Destination zugestellt werden und über die alle Nachrichten gesendet werden, die diese Destination an jede andere Destination sendet.

Vom Client an Router gesendet. Der Router antwortet mit einer [SessionStatusMessage](#SessionStatusMessage).

#### Inhaltsverzeichnis

1.  [Session-Konfiguration](#struct-sessionconfig)

#### Notizen

- Dies ist die zweite Nachricht, die vom Client gesendet wird. Zuvor hat der Client
  eine [GetDateMessage](#GetDateMessage) gesendet und eine
  [SetDateMessage](#SetDateMessage) Antwort erhalten.
- Wenn das Datum in der Session Config zu weit (mehr als +/- 30
  Sekunden) von der aktuellen Zeit des routers abweicht, wird die Session
  abgelehnt.
- Wenn bereits eine Session auf dem router für diese Destination existiert, wird die
  Session abgelehnt.
- Das [Mapping](/docs/specs/common-structures/#mapping) in der Session Config muss
  nach Schlüssel sortiert sein, damit die Signatur im
  router korrekt validiert wird.

### DestLookupMessage {#DestLookupMessage}

#### Beschreibung

Gesendet vom Client zum Router. Der Router antwortet mit einer [DestReplyMessage](#DestReplyMessage).

#### Inhaltsverzeichnis

1.  SHA-256 [Hash](/docs/specs/common-structures/#hash)

#### Notizen

Ab Release 0.7.

Ab Release 0.8.3 werden mehrere ausstehende Lookups unterstützt, und Lookups werden sowohl in I2PSimpleSession als auch in Standard-Sessions unterstützt.

[HostLookupMessage](#HostLookupMessage) wird seit Version 0.9.11 bevorzugt.

### DestReplyMessage {#DestReplyMessage}

#### Beschreibung

Vom Router an den Client als Antwort auf eine [DestLookupMessage](#DestLookupMessage) gesendet.

#### Inhalte

1.  [Destination](/docs/specs/common-structures/#destination) bei Erfolg, oder
    [Hash](/docs/specs/common-structures/#hash) bei Fehler

#### Notizen

Ab Version 0.7.

Ab Version 0.8.3 wird der angeforderte Hash zurückgegeben, wenn die Suche fehlgeschlagen ist, damit der Client mehrere ausstehende Suchen haben und die Antworten mit den Suchen korrelieren kann. Um eine Destination-Antwort mit einer Anfrage zu korrelieren, nehmen Sie den Hash der Destination. Vor Version 0.8.3 war die Antwort bei einem Fehlschlag leer.

### DestroySessionMessage {#DestroySessionMessage}

#### Beschreibung

Diese Nachricht wird von einem Client gesendet, um eine Sitzung zu beenden.

Gesendet vom Client zum Router. Der Router sollte mit einer [SessionStatusMessage](#SessionStatusMessage) (Destroyed) antworten. Siehe jedoch wichtige Hinweise unten.

#### Inhaltsverzeichnis

1.  [Session ID](#struct-sessionid)

#### Notizen

Der router sollte zu diesem Zeitpunkt alle mit der Sitzung verbundenen Ressourcen freigeben.

Bis zur API 0.9.66 weichen die Java I2P router- und Client-Bibliotheken erheblich von dieser Spezifikation ab. Der router sendet niemals eine SessionStatus(Destroyed)-Antwort. Wenn keine Sessions mehr vorhanden sind, sendet er eine [DisconnectMessage](#DisconnectMessage). Wenn Subsessions vorhanden sind oder die primäre Session bestehen bleibt, antwortet er nicht.

Die Java-Client-Bibliothek reagiert auf eine SessionStatus-Nachricht, indem sie alle Sitzungen zerstört und die Verbindung wiederherstellt.

Das Zerstören einzelner Untersitzungen bei einer Verbindung mit mehreren Sitzungen ist möglicherweise nicht vollständig getestet oder funktioniert nicht bei verschiedenen Router- und Client-Implementierungen. Vorsicht ist geboten.

Implementierungen sollten eine Zerstörung einer primären Session als Zerstörung aller Subsessions behandeln, aber eine Zerstörung für eine einzelne Subsession erlauben und die Verbindung offen halten, aber Java I2P macht das derzeit nicht. Falls das Verhalten von Java I2P in zukünftigen Versionen geändert wird, wird es hier dokumentiert.

### DisconnectMessage {#DisconnectMessage}

#### Beschreibung

Teile der anderen Partei mit, dass es Probleme gibt und die aktuelle Verbindung kurz vor der Zerstörung steht. Dies beendet alle Sitzungen auf dieser Verbindung. Der Socket wird in Kürze geschlossen. Wird entweder vom Router zum Client oder vom Client zum Router gesendet.

#### Inhalt

1.  Grund [String](/docs/specs/common-structures/#string)

#### Notizen

Nur in Router-zu-Client-Richtung implementiert, zumindest in Java I2P.

### GetBandwidthLimitsMessage {#GetBandwidthLimitsMessage}

#### Beschreibung

Fordere an, dass der Router seine aktuellen Bandbreitenbegrenzungen mitteilt.

Vom Client an den Router gesendet. Der Router antwortet mit einer [BandwidthLimitsMessage](#BandwidthLimitsMessage).

#### Inhaltsverzeichnis

*Keine*

#### Notizen

Stand Release 0.7.2.

Ab Release 0.8.3 wird dies sowohl in I2PSimpleSession als auch in Standard-Sessions unterstützt.

### GetDateMessage {#GetDateMessage}

#### Beschreibung

Vom Client an den Router gesendet. Der Router antwortet mit einer [SetDateMessage](#SetDateMessage).

#### Inhaltsverzeichnis

1.  I2CP API Version [String](/docs/specs/common-structures/#string)
2.  Authentifizierung [Mapping](/docs/specs/common-structures/#mapping) (optional, seit
    Release 0.9.11)

#### Notizen

- Normalerweise die erste Nachricht, die vom Client nach dem Senden des
  Protokoll-Versions-Bytes gesendet wird.
- Der Versions-String ist ab Release 0.8.7 enthalten. Dies ist nur
  nützlich, wenn sich Client und router nicht in derselben JVM befinden. Wenn er nicht
  vorhanden ist, ist der Client Version 0.8.6 oder früher.
- Ab Release 0.9.11 kann das Authentifizierungs-
  [Mapping](/docs/specs/common-structures/#mapping) enthalten sein, mit den Schlüsseln
  i2cp.username und i2cp.password. Das Mapping muss nicht sortiert sein, da
  diese Nachricht nicht signiert ist. Vor und einschließlich 0.9.10
  ist die Authentifizierung im [Session Config](#struct-sessionconfig)
  Mapping enthalten, und keine Authentifizierung wird für
  [GetDateMessage](#GetDateMessage),
  [GetBandwidthLimitsMessage](#GetBandwidthLimitsMessage), oder
  [DestLookupMessage](#DestLookupMessage) durchgesetzt. Wenn aktiviert, ist die Authentifizierung
  über [GetDateMessage](#GetDateMessage) vor allen anderen
  Nachrichten ab Release 0.9.16 erforderlich. Dies ist nur außerhalb des router-
  Kontexts nützlich. Dies ist eine inkompatible Änderung, wird aber nur Sessions
  außerhalb des router-Kontexts mit Authentifizierung betreffen, was selten sein sollte.

### HostLookupMessage {#HostLookupMessage}

#### Beschreibung

Gesendet vom Client an den Router. Der Router antwortet mit einer [HostReplyMessage](#HostReplyMessage).

Dies ersetzt die [DestLookupMessage](#DestLookupMessage) und fügt eine Anfrage-ID, ein Timeout und Unterstützung für Hostnamen-Lookups hinzu. Da es auch Hash-Lookups unterstützt, kann es für alle Lookups verwendet werden, wenn der router es unterstützt. Für Hostnamen-Lookups fragt der router den Naming Service seines Kontexts ab. Dies ist nur nützlich, wenn sich der Client außerhalb des router-Kontexts befindet. Innerhalb des router-Kontexts sollte der Client den Naming Service selbst abfragen, was viel effizienter ist.

#### Inhaltsverzeichnis

1.  [Session ID](#struct-sessionid)
2.  4 Byte [Integer](/docs/specs/common-structures/#integer) Anfrage-ID
3.  4 Byte [Integer](/docs/specs/common-structures/#integer) Timeout (ms)
4.  1 Byte [Integer](/docs/specs/common-structures/#integer) Anfragetyp
5.  SHA-256 [Hash](/docs/specs/common-structures/#hash) oder Hostname
    [String](/docs/specs/common-structures/#string) oder
    [Destination](/docs/specs/common-structures/#destination)

Anfrage-Typen:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Lookup key (item 5)</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">As of</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Hash</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">host name String</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Hash</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">host name String</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Destination</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
</tr>
</table>
Typen 2-4 fordern, dass das Options-Mapping aus dem LeaseSet in der HostReply-Nachricht zurückgegeben wird. Siehe Vorschlag 167.

#### Notizen

- Ab Release 0.9.11. Verwenden Sie [DestLookupMessage](#DestLookupMessage) für
  ältere router.
- Die Session-ID und Anfrage-ID werden in der
  [HostReplyMessage](#HostReplyMessage) zurückgegeben. Verwenden Sie 0xFFFF für die Session-ID,
  wenn keine Session vorhanden ist.
- Timeout ist nützlich für Hash-Lookups. Empfohlenes Minimum 10.000 (10
  Sek.). In Zukunft könnte es auch für Remote-Naming-Service-
  Lookups nützlich sein. Der Wert wird möglicherweise nicht für lokale Hostnamen-Lookups berücksichtigt,
  die schnell sein sollten.
- Base-32-Hostnamen-Lookup wird unterstützt, aber es ist bevorzugt, ihn
  zuerst in einen Hash zu konvertieren.

### HostReplyMessage {#HostReplyMessage}

#### Beschreibung

Vom Router zum Client als Antwort auf eine [HostLookupMessage](#HostLookupMessage) gesendet.

#### Inhalt

1.  [Session ID](#struct-sessionid)
2.  4 Byte [Integer](/docs/specs/common-structures/#integer) Anfrage-ID
3.  1 Byte [Integer](/docs/specs/common-structures/#integer) Ergebniscode

> - 0: Erfolg > - 1: Fehler > - 2: Lookup-Passwort erforderlich (ab 0.9.43) > - 3: Privater Schlüssel erforderlich (ab 0.9.43) > - 4: Lookup-Passwort und privater Schlüssel erforderlich (ab 0.9.43) > - 5: leaseSet-Entschlüsselungsfehler (ab 0.9.43) > - 6: leaseSet-Lookup-Fehler (ab 0.9.66) > - 7: Lookup-Typ nicht unterstützt (ab 0.9.66)

4.  [Destination](/docs/specs/common-structures/#destination), nur vorhanden wenn der Ergebniscode null ist, außer kann auch für Nachschlagetypen 2-4 zurückgegeben werden. Siehe unten.
5.  [Mapping](/docs/specs/common-structures/#mapping), nur vorhanden wenn der Ergebniscode null ist, nur für Nachschlagetypen 2-4 zurückgegeben. Ab 0.9.66. Siehe unten.

#### Antworten für Lookup-Typen 2-4

Proposal 167 definiert zusätzliche Lookup-Typen, die alle Optionen aus dem leaseSet zurückgeben, falls vorhanden. Für Lookup-Typen 2-4 muss der router das leaseSet abrufen, auch wenn der Lookup-Schlüssel im Adressbuch vorhanden ist.

Falls erfolgreich, enthält die HostReply die Options-Mapping aus dem leaseSet und schließt diese als Element 5 nach dem Ziel ein. Falls es keine Optionen im Mapping gibt, oder das leaseSet Version 1 war, wird es trotzdem als leeres Mapping eingeschlossen (zwei Bytes: 0 0). Alle Optionen aus dem leaseSet werden eingeschlossen, nicht nur Service-Record-Optionen. Zum Beispiel können Optionen für in der Zukunft definierte Parameter vorhanden sein. Das zurückgegebene Mapping kann sortiert sein oder auch nicht, implementierungsabhängig.

Bei einem leaseSet-Nachschlagefehler enthält die Antwort einen neuen Fehlercode 6 (leaseSet-Nachschlagefehler) und wird keine Zuordnung enthalten. Wenn Fehlercode 6 zurückgegeben wird, kann das Destination-Feld vorhanden sein oder nicht. Es wird vorhanden sein, wenn eine Hostname-Suche im Adressbuch erfolgreich war, oder wenn eine vorherige Suche erfolgreich war und das Ergebnis zwischengespeichert wurde, oder wenn die Destination in der Nachschlagenachricht vorhanden war (Nachschlagetyp 4).

Falls ein Lookup-Typ nicht unterstützt wird, enthält die Antwort einen neuen Fehlercode 7 (Lookup-Typ nicht unterstützt).

#### Notizen

- Ab Release 0.9.11. Siehe [HostLookupMessage](#HostLookupMessage)
  Hinweise.
- Die Session-ID und Request-ID sind die aus der
  [HostLookupMessage](#HostLookupMessage).
- Der Result-Code ist 0 für Erfolg, 1-255 für Fehler. 1 zeigt einen
  generischen Fehler an. Ab 0.9.43 wurden die zusätzlichen Fehlercodes 2-5
  definiert, um erweiterte Fehler für "b33"-Lookups zu unterstützen. Siehe Proposals
  123 und 149 für zusätzliche Informationen. Ab 0.9.66 wurden die zusätzlichen
  Fehlercodes 6-7 definiert, um erweiterte Fehler für Typ 2-4
  Lookups zu unterstützen. Siehe Proposal 167 für zusätzliche Informationen.

### MessagePayloadMessage {#MessagePayloadMessage}

#### Beschreibung

Liefere die Nutzlast einer Nachricht an den Client.

Vom Router an den Client gesendet. Falls i2cp.fastReceive=true, was nicht die Standardeinstellung ist, antwortet der Client mit einer [ReceiveMessageEndMessage](#ReceiveMessageEndMessage).

#### Inhaltsverzeichnis

1.  [Sitzungs-ID](#struct-sessionid)
2.  [Nachrichten-ID](#struct-messageid)
3.  [Nutzdaten](#struct-payload)

#### Notizen

### MessageStatusMessage {#MessageStatusMessage}

#### Beschreibung

Benachrichtigt den Client über den Zustellstatus einer eingehenden oder ausgehenden Nachricht. Wird vom Router an den Client gesendet. Wenn diese Nachricht anzeigt, dass eine eingehende Nachricht verfügbar ist, antwortet der Client mit einer [ReceiveMessageBeginMessage](#ReceiveMessageBeginMessage). Für eine ausgehende Nachricht ist dies eine Antwort auf eine [SendMessageMessage](#SendMessageMessage) oder [SendMessageExpiresMessage](#SendMessageExpiresMessage).

#### Inhaltsverzeichnis

1.  [Session ID](#struct-sessionid)
2.  [Message ID](#struct-messageid) generiert vom router
3.  1 Byte [Integer](/docs/specs/common-structures/#integer) Status
4.  4 Byte [Integer](/docs/specs/common-structures/#integer) Größe
5.  4 Byte [Integer](/docs/specs/common-structures/#integer) Nonce zuvor generiert
    vom Client

#### Notizen

Bis Version 0.9.4 sind die bekannten Status-Werte 0 für Nachricht ist verfügbar, 1 für akzeptiert, 2 für best effort erfolgreich, 3 für best effort fehlgeschlagen, 4 für guaranteed erfolgreich, 5 für guaranteed fehlgeschlagen. Der size Integer gibt die Größe der verfügbaren Nachricht an und ist nur für status = 0 relevant. Obwohl guaranteed nicht implementiert ist (best effort ist der einzige Service), verwendet die aktuelle router-Implementierung die guaranteed Status-Codes, nicht die best effort Codes.

Ab Router-Version 0.9.5 sind zusätzliche Statuscodes definiert, diese sind jedoch nicht unbedingt implementiert. Siehe [MessageStatusMessage Javadocs](http://javadoc.i2p.net/net/i2p/data/i2cp/MessageStatusMessage.html) für Details. Für ausgehende Nachrichten zeigen die Codes 1, 2, 4 und 6 Erfolg an; alle anderen sind Fehlschläge. Zurückgegebene Fehlercodes können variieren und sind implementierungsspezifisch.

Alle Statuscodes:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Status Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">As Of Release</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Name</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Description</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Available</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">DEPRECATED. For incoming messages only. All other status codes below are for outgoing messages. The included size is the size in bytes of the available message. This is unused in "fast receive" mode, which is the default as of release 0.9.4.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Accepted</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Outgoing message accepted by the local router for delivery. The included nonce matches the nonce in the <a href="#SendMessageMessage">SendMessageMessage</a>, and the included Message ID will be used for subsequent success or failure notification.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Best Effort Success</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Probable success (unused)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Best Effort Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Probable failure</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Guaranteed Success</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Probable success</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Guaranteed Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Generic failure, specific cause unknown. May not really be a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local Success</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local delivery successful. The destination was another client on the same router.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local delivery failure. The destination was another client on the same router.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Router Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The local router is not ready, has shut down, or has major problems. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">9</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Network Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The local computer apparently has no network connectivity at all. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Session</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The I2CP session is invalid or closed. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Message</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The message payload is invalid or zero-length or too big. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Options</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Something is invalid in the message options, or the expiration is in the past or too far in the future. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">13</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Overflow Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Some queue or buffer in the router is full and the message was dropped. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">14</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Message Expired</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The message expired before it could be sent. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">15</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Local Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The client has not yet signed a <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a>, or the local keys are invalid, or it has expired, or it does not have any tunnels in it. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">No Local Tunnels</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local problems. No outbound tunnel to send through, or no inbound tunnel if a reply is required. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">17</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Unsupported Encryption</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The certs or options in the <a href="/docs/specs/common-structures/#destination">Destination</a> or its <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a> indicate that it uses an encryption format that we don't support, so we can't talk to it. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">18</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Destination</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Something is wrong with the far-end <a href="/docs/specs/common-structures/#destination">Destination</a>. Bad format, unsupported options, certificates, etc. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">19</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">We got the far-end <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a> but something strange is wrong with it. Unsupported options or certificates, no tunnels, etc. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">20</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Expired Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">We got the far-end <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a> but it's expired and we can't get a new one. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">21</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">No Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Could not find the far-end <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a>. This is a common failure, equivalent to a DNS lookup failure. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">22</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Meta Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The far-end destination's lease set was a meta lease set, and cannot be sent to. The client should request the meta lease set's contents with a HostLookupMessage, and select one of the hashes contained within to look up and send to. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">23</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.62</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Loopback Denied</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The message was attempted to be sent from and to the same destination or session. This is a guaranteed failure.</td>
</tr>
</table>
Wenn status = 1 (akzeptiert), stimmt die nonce mit der nonce in der [SendMessageMessage](#SendMessageMessage) überein, und die enthaltene Message ID wird für nachfolgende Erfolgs- oder Fehlschlagbenachrichtigungen verwendet. Andernfalls kann die nonce ignoriert werden.

### ReceiveMessageBeginMessage {#ReceiveMessageBeginMessage}

VERALTET. Nicht von i2pd unterstützt.

#### Beschreibung

Fordert den router auf, eine Nachricht zu übermitteln, über die er zuvor benachrichtigt wurde. Wird vom Client an den router gesendet. Der router antwortet mit einer [MessagePayloadMessage](#MessagePayloadMessage).

#### Inhaltsverzeichnis

1.  [Sitzungs-ID](#struct-sessionid)
2.  [Nachrichten-ID](#struct-messageid)

#### Hinweise

Die [ReceiveMessageBeginMessage](#ReceiveMessageBeginMessage) wird als Antwort auf eine [MessageStatusMessage](#MessageStatusMessage) gesendet, die angibt, dass eine neue Nachricht zur Abholung bereitsteht. Wenn die in der [ReceiveMessageBeginMessage](#ReceiveMessageBeginMessage) angegebene Nachrichten-ID ungültig oder falsch ist, kann der router einfach nicht antworten oder eine [DisconnectMessage](#DisconnectMessage) zurücksenden.

Dies wird im "Fast Receive"-Modus nicht verwendet, der seit Version 0.9.4 standardmäßig aktiviert ist.

### ReceiveMessageEndMessage {#ReceiveMessageEndMessage}

VERALTET. Wird von i2pd nicht unterstützt.

#### Beschreibung

Teile dem router mit, dass die Zustellung einer Nachricht erfolgreich abgeschlossen wurde und dass der router die Nachricht verwerfen kann.

Vom Client an den Router gesendet.

#### Inhaltsverzeichnis

1.  [Session ID](#struct-sessionid)
2.  [Nachrichten-ID](#struct-messageid)

#### Hinweise

Die [ReceiveMessageEndMessage](#ReceiveMessageEndMessage) wird gesendet, nachdem eine [MessagePayloadMessage](#MessagePayloadMessage) die Nutzlast einer Nachricht vollständig übertragen hat.

Dies wird im "schnellen Empfangsmodus" nicht verwendet, welcher seit Version 0.9.4 die Standardeinstellung ist.

### ReconfigureSessionMessage {#ReconfigureSessionMessage}

#### Beschreibung

Vom Client an den Router gesendet, um die Sitzungskonfiguration zu aktualisieren. Der Router antwortet mit einer [SessionStatusMessage](#SessionStatusMessage).

#### Inhalt

1.  [Sitzungs-ID](#struct-sessionid)
2.  [Sitzungskonfiguration](#struct-sessionconfig)

#### Notizen

- Ab Release 0.7.1.
- Wenn das Datum in der Session Config zu weit (mehr als +/- 30
  Sekunden) von der aktuellen Zeit des routers abweicht, wird die Session
  abgelehnt.
- Das [Mapping](/docs/specs/common-structures/#mapping) in der Session Config muss
  nach Schlüssel sortiert sein, damit die Signatur im
  router korrekt validiert wird.
- Einige Konfigurationsoptionen können nur in der
  [CreateSessionMessage](#CreateSessionMessage) gesetzt werden, und Änderungen hier werden
  vom router nicht erkannt. Änderungen an tunnel-Optionen inbound.\*
  und outbound.\* werden immer erkannt.
- Im Allgemeinen sollte der router die aktualisierte Konfiguration mit der
  aktuellen Konfiguration zusammenführen, sodass die aktualisierte Konfiguration nur die neuen oder
  geänderten Optionen enthalten muss. Aufgrund der Zusammenführung können Optionen jedoch nicht auf
  diese Weise entfernt werden; sie müssen explizit auf den gewünschten
  Standardwert gesetzt werden.

### ReportAbuseMessage {#ReportAbuseMessage}

VERALTET, UNGENUTZT, NICHT UNTERSTÜTZT

#### Beschreibung

Teile der anderen Partei (client oder router) mit, dass sie unter Angriff steht, möglicherweise mit Verweis auf eine bestimmte MessageId. Wenn der router unter Angriff steht, kann der client entscheiden, zu einem anderen router zu migrieren, und wenn ein client unter Angriff steht, kann der router seine router neu aufbauen oder einige der Peers auf die Bannliste setzen, die ihm Nachrichten mit dem Angriff zugestellt haben.

Wird entweder vom router zum Client oder vom Client zum router gesendet.

#### Inhaltsverzeichnis

1.  [Session ID](#struct-sessionid)
2.  1 Byte [Integer](/docs/specs/common-structures/#integer) Missbrauchsschweregrad (0 ist minimal missbräuchlich, 255 ist extrem missbräuchlich)
3.  Grund [String](/docs/specs/common-structures/#string)
4.  [Message ID](#struct-messageid)

#### Notizen

Nicht verwendet. Nicht vollständig implementiert. Sowohl der router als auch der Client können eine [ReportAbuseMessage](#ReportAbuseMessage) generieren, aber keiner von beiden hat einen Handler für die Nachricht, wenn sie empfangen wird.

### RequestLeaseSetMessage {#RequestLeaseSetMessage}

VERALTET. Wird von i2pd nicht unterstützt. Wird von Java I2P nicht an Clients der Version 0.9.7 oder höher gesendet (2013-07). Verwenden Sie RequestVariableLeaseSetMessage.

#### Beschreibung

Anfrage, dass ein Client die Einbeziehung eines bestimmten Satzes von eingehenden tunnels autorisiert. Gesendet vom Router zum Client. Der Client antwortet mit einer [CreateLeaseSetMessage](#CreateLeaseSetMessage).

Die erste dieser Nachrichten, die in einer Sitzung gesendet wird, ist ein Signal an den Client, dass tunnel erstellt und für den Verkehr bereit sind. Der router darf die erste dieser Nachrichten nicht senden, bis mindestens ein eingehender UND ein ausgehender tunnel erstellt wurde. Clients sollten die Sitzung mit einem Timeout beenden und zerstören, wenn die erste dieser Nachrichten nach einiger Zeit nicht empfangen wird (empfohlen: 5 Minuten oder mehr).

#### Inhalt

1.  [Session ID](#struct-sessionid)
2.  1 Byte [Integer](/docs/specs/common-structures/#integer) Anzahl der Tunnel
3.  So viele Paare von:
    1.  [Hash](/docs/specs/common-structures/#hash)
    2.  [TunnelId](/docs/specs/common-structures/#tunnelid)
4.  End [Date](/docs/specs/common-structures/#date)

#### Hinweise

Dies fordert ein [LeaseSet](/docs/specs/common-structures/#leaseset) an, bei dem alle [Lease](/docs/specs/common-structures/#lease)-Einträge so gesetzt sind, dass sie zur gleichen Zeit ablaufen. Für Client-Versionen 0.9.7 oder höher wird [RequestVariableLeaseSetMessage](#RequestVariableLeaseSetMessage) verwendet.

### RequestVariableLeaseSetMessage {#RequestVariableLeaseSetMessage}

#### Beschreibung

Anfrage, dass ein Client die Einbeziehung einer bestimmten Gruppe von eingehenden tunnels autorisiert.

Gesendet vom Router zum Client. Der Client antwortet mit einer [CreateLeaseSetMessage](#CreateLeaseSetMessage) oder [CreateLeaseSet2Message](#CreateLeaseSet2Message).

Die erste dieser Nachrichten, die in einer Sitzung gesendet wird, ist ein Signal an den Client, dass tunnel erstellt und bereit für den Datenverkehr sind. Der router darf die erste dieser Nachrichten nicht senden, bis mindestens ein eingehender UND ein ausgehender tunnel erstellt wurden. Clients sollten eine Zeitüberschreitung einleiten und die Sitzung beenden, wenn die erste dieser Nachrichten nach einiger Zeit nicht empfangen wird (empfohlen: 5 Minuten oder mehr).

#### Inhalt

1.  [Session ID](#struct-sessionid)
2.  1 Byte [Integer](/docs/specs/common-structures/#integer) Anzahl der tunnel
3.  Entsprechend viele [Lease](/docs/specs/common-structures/#lease) Einträge

#### Notizen

Dies fordert ein [LeaseSet](/docs/specs/common-structures/#leaseset) mit einer individuellen Ablaufzeit für jede [Lease](/docs/specs/common-structures/#lease) an.

Ab Release 0.9.7. Für Clients vor diesem Release verwenden Sie [RequestLeaseSetMessage](#RequestLeaseSetMessage).

### SendMessageMessage {#SendMessageMessage}

#### Beschreibung

So sendet ein Client eine Nachricht (die Nutzdaten) an die [Destination](/docs/specs/common-structures/#destination). Der Router verwendet eine Standard-Ablaufzeit.

Vom Client zum Router gesendet. Der Router antwortet mit einer [MessageStatusMessage](#MessageStatusMessage).

#### Inhaltsverzeichnis

1.  [Session ID](#struct-sessionid)
2.  [Destination](/docs/specs/common-structures/#destination)
3.  [Payload](#struct-payload)
4.  4 Byte [Integer](/docs/specs/common-structures/#integer) Nonce

#### Hinweise

Sobald die [SendMessageMessage](#SendMessageMessage) vollständig unversehrt ankommt, sollte der router eine [MessageStatusMessage](#MessageStatusMessage) zurücksenden, die besagt, dass sie zur Zustellung angenommen wurde. Diese Nachricht wird dieselbe hier gesendete Nonce enthalten. Später, basierend auf den Zustellungsgarantien der Sitzungskonfiguration, kann der router zusätzlich eine weitere [MessageStatusMessage](#MessageStatusMessage) zurücksenden, die den Status aktualisiert.

Seit Version 0.8.1 sendet der router keine [MessageStatusMessage](#MessageStatusMessage) wenn i2cp.messageReliability=none.

Vor Release 0.9.4 war ein nonce-Wert von 0 nicht erlaubt. Ab Release 0.9.4 ist ein nonce-Wert von 0 erlaubt und teilt dem router mit, dass er keine [MessageStatusMessage](#MessageStatusMessage) senden soll, d.h. es verhält sich so, als ob i2cp.messageReliability=none nur für diese Nachricht gilt.

Vor der Veröffentlichung 0.9.14 konnte eine Session mit i2cp.messageReliability=none nicht auf Nachrichten-Basis überschrieben werden. Ab der Veröffentlichung 0.9.14 kann der Client in einer Session mit i2cp.messageReliability=none die Zustellung einer [MessageStatusMessage](#MessageStatusMessage) mit dem Zustellungserfolg oder -fehler anfordern, indem die Nonce auf einen Wert ungleich Null gesetzt wird. Der Router wird die "accepted" [MessageStatusMessage](#MessageStatusMessage) nicht senden, aber später eine [MessageStatusMessage](#MessageStatusMessage) mit derselben Nonce und einem Erfolgs- oder Fehlschlagwert an den Client senden.

### SendMessageExpiresMessage {#SendMessageExpiresMessage}

#### Beschreibung

Vom Client an den Router gesendet. Wie [SendMessageMessage](#SendMessageMessage), jedoch mit Ablaufzeit und Optionen.

#### Inhalt

1.  [Session ID](#struct-sessionid)
2.  [Destination](/docs/specs/common-structures/#destination)
3.  [Payload](#struct-payload)
4.  4 Byte [Integer](/docs/specs/common-structures/#integer) Nonce
5.  2 Bytes Flags (Optionen)
6.  Ablauf-[Date](/docs/specs/common-structures/#date) von 8 Bytes auf 6 Bytes
    gekürzt

#### Notizen

Ab Release 0.7.1.

Im "best effort"-Modus sollte der router, sobald die SendMessageExpiresMessage vollständig intakt ankommt, eine MessageStatusMessage zurücksenden, die besagt, dass sie zur Zustellung angenommen wurde. Diese Nachricht wird dieselbe hier gesendete Nonce enthalten. Später kann der router basierend auf den Zustellungsgarantien der Sitzungskonfiguration zusätzlich eine weitere MessageStatusMessage zurücksenden, die den Status aktualisiert.

Seit Release 0.8.1 sendet der router keine Message Status Message, wenn i2cp.messageReliability=none ist.

Vor Version 0.9.4 war ein nonce-Wert von 0 nicht erlaubt. Ab Version 0.9.4 ist ein nonce-Wert von 0 erlaubt und teilt dem router mit, dass er keine Message Status Message senden soll, d.h. es verhält sich so, als ob i2cp.messageReliability=none nur für diese Nachricht gesetzt wäre.

Vor Version 0.9.14 konnte eine Sitzung mit i2cp.messageReliability=none nicht auf Basis einzelner Nachrichten überschrieben werden. Ab Version 0.9.14 kann der Client in einer Sitzung mit i2cp.messageReliability=none die Zustellung einer Message Status Message mit dem Erfolg oder Fehlschlag der Zustellung anfordern, indem er die nonce auf einen Wert ungleich null setzt. Der router wird die "accepted" Message Status Message nicht senden, aber später dem Client eine Message Status Message mit derselben nonce und einem Erfolgs- oder Fehlschlagswert senden.

#### Flags-Feld

Ab Release 0.8.4 sind die oberen zwei Bytes des Date-Feldes neu definiert, um Flags zu enthalten. Die Flags müssen standardmäßig auf alle Nullen gesetzt sein, um Rückwärtskompatibilität zu gewährleisten. Das Date-Feld wird das Flags-Feld nicht beeinträchtigen bis zum Jahr 10889. Die Flags können von der Anwendung verwendet werden, um dem Router Hinweise zu geben, ob ein LeaseSet und/oder ElGamal/AES Session Tags mit der Nachricht übermittelt werden sollen. Die Einstellungen beeinflussen erheblich die Menge an Protokoll-Overhead und die Zuverlässigkeit der Nachrichtenübermittlung. Die einzelnen Flag-Bits sind wie folgt definiert, ab Release 0.9.2. Die Definitionen können sich ändern. Verwenden Sie die SendMessageOptions-Klasse, um die Flags zu konstruieren.

Bit-Reihenfolge: 15...0

Bits 15-11

:   Ungenutzt, muss null sein

Bits 10-9

:   Message Reliability Override (Nicht implementiert, wird entfernt).

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Field value</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Description</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">00</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Use session setting i2cp.messageReliability (default)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">01</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Use "best effort" message reliability for this message, overriding the session setting. The router will send one or more MessageStatusMessages in response. Unused. Use a nonzero nonce value to override a session setting of "none".</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Use "guaranteed" message reliability for this message, overriding the session setting. The router will send one or more MessageStatusMessages in response. Unused. Use a nonzero nonce value to override a session setting of "none".</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Unused. Use a nonce value of 0 to force "none" and override a session setting of "best effort" or "guaranteed".</td>
</tr>
</table>
Bit 8

:   Wenn 1, kein leaseSet im garlic mit dieser Nachricht bündeln. Wenn

    0, the router may bundle a lease set at its discretion.

Bits 7-4

:   Niedrige Tag-Schwelle. Wenn weniger als diese Anzahl von Tags verfügbar sind,

    send more. This is advisory and does not force tags to be delivered.
    For ElGamal only. Ignored for ECIES-Ratchet.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Field value</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Tag threshold</th>
</tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0000</td><td style="border: 1px solid var(--color-border); padding: 8px;">Use session key manager settings</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0001</td><td style="border: 1px solid var(--color-border); padding: 8px;">2</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0010</td><td style="border: 1px solid var(--color-border); padding: 8px;">3</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0011</td><td style="border: 1px solid var(--color-border); padding: 8px;">6</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0100</td><td style="border: 1px solid var(--color-border); padding: 8px;">9</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0101</td><td style="border: 1px solid var(--color-border); padding: 8px;">14</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0110</td><td style="border: 1px solid var(--color-border); padding: 8px;">20</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0111</td><td style="border: 1px solid var(--color-border); padding: 8px;">27</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1000</td><td style="border: 1px solid var(--color-border); padding: 8px;">35</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1001</td><td style="border: 1px solid var(--color-border); padding: 8px;">45</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1010</td><td style="border: 1px solid var(--color-border); padding: 8px;">57</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1011</td><td style="border: 1px solid var(--color-border); padding: 8px;">72</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1100</td><td style="border: 1px solid var(--color-border); padding: 8px;">92</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1101</td><td style="border: 1px solid var(--color-border); padding: 8px;">117</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1110</td><td style="border: 1px solid var(--color-border); padding: 8px;">147</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1111</td><td style="border: 1px solid var(--color-border); padding: 8px;">192</td></tr>
</table>
Bits 3-0

:   Anzahl der zu sendenden Tags, falls erforderlich. Dies ist ein Richtwert und ist nicht

    force tags to be delivered. For ElGamal only. Ignored for
    ECIES-Ratchet.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Field value</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Tags to send</th>
</tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0000</td><td style="border: 1px solid var(--color-border); padding: 8px;">Use session key manager settings</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0001</td><td style="border: 1px solid var(--color-border); padding: 8px;">2</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0010</td><td style="border: 1px solid var(--color-border); padding: 8px;">4</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0011</td><td style="border: 1px solid var(--color-border); padding: 8px;">6</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0100</td><td style="border: 1px solid var(--color-border); padding: 8px;">8</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0101</td><td style="border: 1px solid var(--color-border); padding: 8px;">12</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0110</td><td style="border: 1px solid var(--color-border); padding: 8px;">16</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0111</td><td style="border: 1px solid var(--color-border); padding: 8px;">24</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1000</td><td style="border: 1px solid var(--color-border); padding: 8px;">32</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1001</td><td style="border: 1px solid var(--color-border); padding: 8px;">40</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1010</td><td style="border: 1px solid var(--color-border); padding: 8px;">51</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1011</td><td style="border: 1px solid var(--color-border); padding: 8px;">64</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1100</td><td style="border: 1px solid var(--color-border); padding: 8px;">80</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1101</td><td style="border: 1px solid var(--color-border); padding: 8px;">100</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1110</td><td style="border: 1px solid var(--color-border); padding: 8px;">125</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1111</td><td style="border: 1px solid var(--color-border); padding: 8px;">160</td></tr>
</table>
### SessionStatusMessage {#SessionStatusMessage}

#### Beschreibung

Den Client über den Status seiner Sitzung informieren.

Vom Router an den Client gesendet, als Antwort auf eine [CreateSessionMessage](#CreateSessionMessage), [ReconfigureSessionMessage](#ReconfigureSessionMessage) oder [DestroySessionMessage](#DestroySessionMessage). In allen Fällen, einschließlich als Antwort auf eine [CreateSessionMessage](#CreateSessionMessage), sollte der Router sofort antworten (nicht warten, bis tunnel erstellt sind).

#### Inhalt

1.  [Session ID](#struct-sessionid)
2.  1 Byte [Integer](/docs/specs/common-structures/#integer) Status

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Status</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Since</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Name</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Definition</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Destroyed</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The session with the given ID is terminated. May be a response to a <a href="#DestroySessionMessage">DestroySessionMessage</a>.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Created</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">In response to a <a href="#CreateSessionMessage">CreateSessionMessage</a>, a new session with the given ID is now active.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Updated</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">In response to a <a href="#ReconfigureSessionMessage">ReconfigureSessionMessage</a>, an existing session with the given ID has been reconfigured.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Invalid</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">In response to a <a href="#CreateSessionMessage">CreateSessionMessage</a>, the configuration is invalid. The included session ID should be ignored. In response to a <a href="#ReconfigureSessionMessage">ReconfigureSessionMessage</a>, the new configuration is invalid for the session with the given ID.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Refused</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">In response to a <a href="#CreateSessionMessage">CreateSessionMessage</a>, the router was unable to create the session, perhaps due to limits being exceeded. The included session ID should be ignored.</td>
</tr>
</table>
#### Notizen

Statuswerte sind oben definiert. Wenn der Status Created ist, ist die Session ID der Identifikator, der für den Rest der Sitzung verwendet werden soll.

### SetDateMessage {#SetDateMessage}

#### Beschreibung

Das aktuelle Datum und die Uhrzeit. Wird vom Router an den Client als Teil des initialen Handshakes gesendet. Ab Release 0.9.20 kann es auch jederzeit nach dem Handshake gesendet werden, um den Client über eine Uhrzeitverschiebung zu informieren.

#### Inhalt

1.  [Datum](/docs/specs/common-structures/#date)
2.  I2CP API-Version [String](/docs/specs/common-structures/#string)

#### Hinweise

Dies ist im Allgemeinen die erste Nachricht, die vom router gesendet wird. Der Versionsstring ist ab Release 0.8.7 enthalten. Dies ist nur nützlich, wenn sich Client und router nicht in derselben JVM befinden. Wenn er nicht vorhanden ist, handelt es sich um router Version 0.8.6 oder früher.

Zusätzliche SetDate-Nachrichten werden nicht an Clients in derselben JVM gesendet.

## Referenzen

- [Date](/docs/specs/common-structures/#date)
- [Destination](/docs/specs/common-structures/#destination)
- [EncryptedLeaseSet](/docs/specs/common-structures/#leaseset2)
- [Hash](/docs/specs/common-structures/#hash)
- [I2CP Überblick](/docs/specs/i2cp/)
- [I2CP Javadocs](http://javadoc.i2p.net/net/i2p/data/i2cp/package-summary.html)
- [Integer](/docs/specs/common-structures/#integer)
- [Lease](/docs/specs/common-structures/#lease)
- [LeaseSet](/docs/specs/common-structures/#leaseset)
- [LeaseSet2](/docs/specs/common-structures/#leaseset2)
- [Mapping](/docs/specs/common-structures/#mapping)
- [MetaLeaseSet](/docs/specs/common-structures/#leaseset2)
- [MessageStatusMessage Javadocs](http://javadoc.i2p.net/net/i2p/data/i2cp/MessageStatusMessage.html)
- [PrivateKey](/docs/specs/common-structures/#privatekey)
- [PublicKey](/docs/specs/common-structures/#publickey)
- [RouterIdentity](/docs/specs/common-structures/#routeridentity)
- [SAMv3](/docs/api/samv3/)
- [Signature](/docs/specs/common-structures/#signature)
- [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey)
- [SigningPublicKey](/docs/specs/common-structures/#signingpublickey)
- [String](/docs/specs/common-structures/#string)
- [TunnelId](/docs/specs/common-structures/#tunnelid)
