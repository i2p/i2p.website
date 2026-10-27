---
title: "ECIES-Tunnel"
aliases:
  - "/de/proposals/152-ecies-config"
  - "/de/proposals/152-ecies-config/"
  - "/de/proposals/152"
  - "/de/proposals/152/"
number: "152"
author: "chisana, zzz, orignal"
created: "2019-07-04"
lastupdated: "2025-03-05"
status: "Geschlossen"
thread: "http://zzz.i2p/topics/2737"
target: "0.9.48"
implementedin: "0.9.48"
toc: true
---

## Hinweis

Netzwerk-Deployment und Tests laufen. Geringfügige Überarbeitungen vorbehalten. Siehe [SPEC](/docs/specs/tunnel-implementation/) für die offizielle Spezifikation.

## Überblick

Dieses Dokument schlägt Änderungen an der Tunnel Build-Nachrichtenverschlüsselung unter Verwendung kryptographischer Primitive vor, die von [ECIES-X25519](/docs/specs/ecies/) eingeführt wurden. Es ist ein Teil des Gesamtvorschlags [Proposal 156](/proposals/156-ecies-routers) zur Umstellung von Routern von ElGamal auf ECIES-X25519-Schlüssel.

Für die Zwecke der Netzwerkumstellung von ElGamal + AES256 zu ECIES + ChaCha20 sind tunnel mit gemischten ElGamal- und ECIES-routern erforderlich. Spezifikationen für die Behandlung gemischter Tunnel-Hops werden bereitgestellt. Es werden keine Änderungen am Format, der Verarbeitung oder der Verschlüsselung von ElGamal-Hops vorgenommen.

ElGamal-Tunnel-Ersteller müssen ephemere X25519-Schlüsselpaare pro Hop erstellen und dieser Spezifikation für die Erstellung von Tunneln mit ECIES-Hops folgen.

Dieser Vorschlag spezifiziert die Änderungen, die für ECIES-X25519 Tunnel Building benötigt werden. Für eine Übersicht aller erforderlichen Änderungen für ECIES router, siehe Vorschlag 156 [Proposal 156](/proposals/156-ecies-routers).

Dieser Vorschlag behält die gleiche Größe für tunnel build records bei, wie es für die Kompatibilität erforderlich ist. Kleinere build records und Nachrichten werden später implementiert - siehe [Proposal 157](/proposals/157-new-tbm).

### Cryptographic Primitives

Es werden keine neuen kryptographischen Primitive eingeführt. Die zur Implementierung dieses Vorschlags erforderlichen Primitive sind:

- AES-256-CBC wie in [Cryptography](/docs/specs/cryptography/)
- STREAM ChaCha20/Poly1305 Funktionen:
  ENCRYPT(k, n, plaintext, ad) und DECRYPT(k, n, ciphertext, ad) - wie in [NTCP2](/docs/specs/ntcp2/) [ECIES-X25519](/docs/specs/ecies/) und [RFC-7539](https://tools.ietf.org/html/rfc7539)
- X25519 DH Funktionen - wie in [NTCP2](/docs/specs/ntcp2/) und [ECIES-X25519](/docs/specs/ecies/)
- HKDF(salt, ikm, info, n) - wie in [NTCP2](/docs/specs/ntcp2/) und [ECIES-X25519](/docs/specs/ecies/)

Andere Noise-Funktionen, die anderweitig definiert sind:

- MixHash(d) - wie in [NTCP2](/docs/specs/ntcp2/) und [ECIES-X25519](/docs/specs/ecies/)
- MixKey(d) - wie in [NTCP2](/docs/specs/ntcp2/) und [ECIES-X25519](/docs/specs/ecies/)

### Goals

- Geschwindigkeit von Krypto-Operationen erhöhen
- ElGamal + AES256/CBC durch ECIES-Primitive für Tunnel BuildRequestRecords und BuildReplyRecords ersetzen
- Keine Änderung der Größe verschlüsselter BuildRequestRecords und BuildReplyRecords (528 Bytes) für Kompatibilität
- Keine neuen I2NP-Nachrichten
- Verschlüsselte Build-Record-Größe für Kompatibilität beibehalten
- Forward Secrecy für Tunnel Build Messages hinzufügen
- Authentifizierte Verschlüsselung hinzufügen
- Neuordnung von BuildRequestRecords durch Hops erkennen
- Auflösung des Zeitstempels erhöhen, damit die Bloom-Filter-Größe reduziert werden kann
- Feld für Tunnel-Ablauf hinzufügen, damit variable Tunnel-Lebensdauern möglich werden (nur All-ECIES-Tunnel)
- Erweiterbares Optionsfeld für zukünftige Features hinzufügen
- Bestehende kryptographische Primitive wiederverwenden
- Sicherheit von Tunnel-Build-Messages verbessern, wo möglich, unter Beibehaltung der Kompatibilität
- Tunnel mit gemischten ElGamal/ECIES-Peers unterstützen
- Schutz gegen "Tagging"-Angriffe auf Build-Messages verbessern
- Hops müssen den Verschlüsselungstyp des nächsten Hops nicht vor der Verarbeitung der Build-Message kennen,
  da sie möglicherweise die RI des nächsten Hops zu diesem Zeitpunkt nicht haben
- Kompatibilität mit aktuellem Netzwerk maximieren
- Keine Änderung der Tunnel-Build-AES-Request/Reply-Verschlüsselung für ElGamal-Router
- Keine Änderung der Tunnel-AES-"Layer"-Verschlüsselung, siehe dafür [Proposal 153](/proposals/153-chacha20-layer-encryption)
- Unterstützung sowohl für 8-Record TBM/TBRM als auch variable Größe VTBM/VTBRM fortsetzen
- Kein "Flag Day"-Upgrade des gesamten Netzwerks erforderlich

### Kryptographische Grundbausteine

- Komplette Neugestaltung der Tunnel-Build-Nachrichten, die einen "Flag Day" erfordert.
- Verkleinerung der Tunnel-Build-Nachrichten (erfordert ausschließlich ECIES-Hops und einen neuen Vorschlag)
- Verwendung von Tunnel-Build-Optionen wie in [Proposal 143](/proposals/143-build-message-options) definiert, nur für kleine Nachrichten erforderlich
- Bidirektionale Tunnel - siehe dazu [Proposal 119](/proposals/119-bidirectional-tunnels)
- Kleinere Tunnel-Build-Nachrichten - siehe dazu [Proposal 157](/proposals/157-new-tbm)

## Threat Model

### Ziele

- Keine Hops sind in der Lage, den Ursprung des Tunnels zu bestimmen.

- Zwischenhops dürfen nicht in der Lage sein, die Richtung des tunnels
  oder ihre Position im tunnel zu bestimmen.

- Kein Hop kann Inhalte anderer Anfrage- oder Antwort-Datensätze lesen, außer
  dem gekürzten Router-Hash und dem ephemeren Schlüssel für den nächsten Hop

- Kein Mitglied des Antwort-Tunnels für ausgehende Builds kann Antwort-Datensätze lesen.

- Kein Mitglied des Outbound-Tunnels für den Inbound-Build kann Anfrage-Datensätze lesen,
  außer dass OBEP den gekürzten Router-Hash und den ephemeren Schlüssel für IBGW sehen kann

### Nicht-Ziele

Ein Hauptziel des Tunnel-Building-Designs ist es, es für kollaborierende router X und Y schwieriger zu machen zu wissen, dass sie sich in einem einzigen Tunnel befinden. Wenn router X bei Hop m und router Y bei Hop m+1 ist, werden sie es offensichtlich wissen. Aber wenn router X bei Hop m und router Y bei Hop m+n für n>1 ist, sollte dies viel schwieriger sein.

Tagging-Angriffe sind Angriffe, bei denen der Zwischenhop-router X die Tunnel-Build-Nachricht so verändert, dass router Y die Veränderung erkennen kann, wenn die Build-Nachricht dort ankommt. Das Ziel ist, dass jede veränderte Nachricht von einem router zwischen X und Y verworfen wird, bevor sie router Y erreicht. Für Änderungen, die nicht vor router Y verworfen werden, sollte der Tunnel-Ersteller die Verfälschung in der Antwort erkennen und den Tunnel verwerfen.

Mögliche Angriffe:

- Einen Build-Datensatz ändern
- Einen Build-Datensatz ersetzen
- Einen Build-Datensatz hinzufügen oder entfernen
- Die Build-Datensätze neu anordnen

TODO: Verhindert das aktuelle Design all diese Angriffe?

## Design

### Noise Protocol Framework

Dieser Vorschlag stellt die Anforderungen basierend auf dem Noise Protocol Framework [NOISE](https://noiseprotocol.org/noise.html) (Revision 34, 2018-07-11) bereit. In der Noise-Terminologie ist Alice die Initiatorin und Bob der Responder.

Dieser Vorschlag basiert auf dem Noise-Protokoll Noise_N_25519_ChaChaPoly_SHA256. Dieses Noise-Protokoll verwendet die folgenden Primitive:

- One-Way Handshake Pattern: N
  Alice übermittelt ihren statischen Schlüssel nicht an Bob (N)

- DH Function: X25519
  X25519 DH mit einer Schlüssellänge von 32 Bytes wie in [RFC-7748](https://tools.ietf.org/html/rfc7748) spezifiziert.

- Cipher Function: ChaChaPoly
  AEAD_CHACHA20_POLY1305 wie spezifiziert in [RFC-7539](https://tools.ietf.org/html/rfc7539) Abschnitt 2.8.
  12 Byte Nonce, wobei die ersten 4 Bytes auf null gesetzt sind.
  Identisch zu dem in [NTCP2](/docs/specs/ntcp2/).

- Hash Function: SHA256
  Standard 32-Byte-Hash, bereits umfangreich in I2P verwendet.

#### Additions to the Framework

Keine.

### Designziele

Handshakes verwenden [Noise](https://noiseprotocol.org/noise.html) Handshake-Muster.

Die folgende Buchstabenzuordnung wird verwendet:

- e = einmaliger ephemerer Schlüssel
- s = statischer Schlüssel
- p = Nachrichten-Payload

Die Build-Anfrage ist identisch zum Noise N-Muster. Dies ist auch identisch zur ersten (Session Request) Nachricht im XK-Muster, das in [NTCP2](/docs/specs/ntcp2/) verwendet wird.

```text
<- s
  ...
  e es p ->
```
### Tagging-Angriffe

Build-Request-Datensätze werden vom tunnel-Ersteller erstellt und asymmetrisch zu dem jeweiligen Hop verschlüsselt. Diese asymmetrische Verschlüsselung von Request-Datensätzen ist derzeit ElGamal, wie in [Cryptography](/docs/specs/cryptography/) definiert, und enthält eine SHA-256-Prüfsumme. Dieses Design ist nicht forward-secret.

Das neue Design wird das einseitige Noise-Pattern "N" mit ECIES-X25519 ephemeral-static DH, mit einem HKDF und ChaCha20/Poly1305 AEAD für Forward Secrecy, Integrität und Authentifizierung verwenden. Alice ist der Tunnel-Build-Anforderer. Jeder Hop im Tunnel ist ein Bob.

(Payload-Sicherheitseigenschaften)

```text
N:                      Authentication   Confidentiality
    -> e, es                  0                2

    Authentication: None (0).
    This payload may have been sent by any party, including an active attacker.

    Confidentiality: 2.
    Encryption to a known recipient, forward secrecy for sender compromise
    only, vulnerable to replay.  This payload is encrypted based only on DHs
    involving the recipient's static key pair.  If the recipient's static
    private key is compromised, even at a later date, this payload can be
    decrypted.  This message can also be replayed, since there's no ephemeral
    contribution from the recipient.

    "e": Alice generates a new ephemeral key pair and stores it in the e
         variable, writes the ephemeral public key as cleartext into the
         message buffer, and hashes the public key along with the old h to
         derive a new h.

    "es": A DH is performed between the Alice's ephemeral key pair and the
          Bob's static key pair.  The result is hashed along with the old ck to
          derive a new ck and k, and n is set to zero.
```
### Reply encryption

Build-Reply-Datensätze werden vom Hop-Ersteller erstellt und symmetrisch zum Ersteller verschlüsselt. Diese symmetrische Verschlüsselung der Reply-Datensätze erfolgt derzeit mit AES und einer vorangestellten SHA-256-Prüfsumme. und enthält eine SHA-256-Prüfsumme. Dieses Design ist nicht forward-secret.

Das neue Design wird ChaCha20/Poly1305 AEAD für Integrität und Authentifizierung verwenden.

### Noise Protocol Framework

Der ephemerale öffentliche Schlüssel in der Anfrage muss nicht mit AES oder Elligator2 verschleiert werden. Der vorherige Hop ist der einzige, der ihn sehen kann, und dieser Hop weiß, dass der nächste Hop ECIES ist.

Antwort-Datensätze benötigen keine vollständige asymmetrische Verschlüsselung mit einem weiteren DH.

## Specification

### Build Request Records

Verschlüsselte BuildRequestRecords sind 528 Bytes sowohl für ElGamal als auch für ECIES, aus Kompatibilitätsgründen.

#### Request Record Unencrypted (ElGamal)

Als Referenz ist dies die aktuelle Spezifikation des tunnel BuildRequestRecord für ElGamal router, entnommen aus [I2NP](/docs/specs/i2np/). Die unverschlüsselten Daten werden mit einem Byte ungleich null und dem SHA-256-Hash der Daten vor der Verschlüsselung vorangestellt, wie in [Cryptography](/docs/specs/cryptography/) definiert.

Alle Felder sind Big-Endian.

Unverschlüsselte Größe: 222 Bytes

```text
bytes     0-3: tunnel ID to receive messages as, nonzero
  bytes    4-35: local router identity hash
  bytes   36-39: next tunnel ID, nonzero
  bytes   40-71: next router identity hash
  bytes  72-103: AES-256 tunnel layer key
  bytes 104-135: AES-256 tunnel IV key
  bytes 136-167: AES-256 reply key
  bytes 168-183: AES-256 reply IV
  byte      184: flags
  bytes 185-188: request time (in hours since the epoch, rounded down)
  bytes 189-192: next message ID
  bytes 193-221: uninterpreted / random padding
```
#### Request Record Encrypted (ElGamal)

Zur Referenz ist hier die aktuelle Spezifikation des tunnel BuildRequestRecord für ElGamal router, entnommen aus [I2NP](/docs/specs/i2np/).

Verschlüsselte Größe: 528 Bytes

```text
bytes    0-15: Hop's truncated identity hash
  bytes  16-528: ElGamal encrypted BuildRequestRecord
```
#### Request Record Unencrypted (ECIES)

Dies ist die vorgeschlagene Spezifikation des tunnel BuildRequestRecord für ECIES-X25519 router. Zusammenfassung der Änderungen:

- Entferne ungenutzte 32-Byte router hash
- Ändere Anfrage-Zeit von Stunden zu Minuten
- Füge Ablauffeld für zukünftige variable tunnel-Zeit hinzu
- Füge mehr Platz für Flags hinzu
- Füge Mapping für zusätzliche Build-Optionen hinzu
- AES-256 Antwortschlüssel und IV werden nicht für den eigenen Antwort-Record des Hops verwendet
- Unverschlüsselter Record ist länger, da weniger Verschlüsselungs-Overhead vorhanden ist

Der Request-Datensatz enthält keine ChaCha-Antwortschlüssel. Diese Schlüssel werden von einer KDF abgeleitet. Siehe unten.

Alle Felder sind Big-Endian.

Unverschlüsselte Größe: 464 Bytes

```text
bytes     0-3: tunnel ID to receive messages as, nonzero
  bytes     4-7: next tunnel ID, nonzero
  bytes    8-39: next router identity hash
  bytes   40-71: AES-256 tunnel layer key
  bytes  72-103: AES-256 tunnel IV key
  bytes 104-135: AES-256 reply key
  bytes 136-151: AES-256 reply IV
  byte      152: flags
  bytes 153-155: more flags, unused, set to 0 for compatibility
  bytes 156-159: request time (in minutes since the epoch, rounded down)
  bytes 160-163: request expiration (in seconds since creation)
  bytes 164-167: next message ID
  bytes   168-x: tunnel build options (Mapping)
  bytes     x-x: other data as implied by flags or options
  bytes   x-463: random padding
```
Das flags-Feld ist dasselbe wie in [Tunnel Creation](/docs/specs/tunnel-implementation/) definiert und enthält folgendes::

```text
Bit order: 76543210 (bit 7 is MSB)
bit 7: if set, allow messages from anyone
bit 6: if set, allow messages to anyone, and send the reply to the
       specified next hop in a Tunnel Build Reply Message
bits 5-0: Undefined, must set to 0 for compatibility with future options
```
Bit-Reihenfolge: 76543210 (Bit 7 ist MSB)  Bit 7: falls gesetzt, erlaube Nachrichten von jedem  Bit 6: falls gesetzt, erlaube Nachrichten an jeden und sende die Antwort an das

Bits 5-0: Undefiniert, muss für Kompatibilität mit zukünftigen Optionen auf 0 gesetzt werden

Bit 7 zeigt an, dass der Hop ein eingehender Gateway (IBGW) sein wird. Bit 6 zeigt an, dass der Hop ein ausgehender Endpunkt (OBEP) sein wird. Wenn keines der Bits gesetzt ist, wird der Hop ein zwischenliegender Teilnehmer sein. Beide können nicht gleichzeitig gesetzt werden.

#### Request Record Encrypted (ECIES)

Die Anfrage-Ablaufzeit ist für zukünftige variable Tunneldauer vorgesehen. Derzeit ist der einzige unterstützte Wert 600 (10 Minuten).

Die tunnel build options sind eine Mapping-Struktur, wie sie in [Common Structures](/docs/specs/common-structures/) definiert ist. Dies ist für zukünftige Verwendung vorgesehen. Derzeit sind keine Optionen definiert. Wenn die Mapping-Struktur leer ist, sind dies zwei Bytes 0x00 0x00. Die maximale Größe des Mappings (einschließlich des Längenfelds) beträgt 296 Bytes, und der maximale Wert des Mapping-Längenfelds beträgt 294.

```text
bytes    0-15: Hop's truncated identity hash
  bytes   16-47: Sender's ephemeral X25519 public key
  bytes  48-511: ChaCha20 encrypted BuildRequestRecord
  bytes 512-527: Poly1305 MAC
```
### Handshake-Muster

Alle Felder sind big-endian, außer dem ephemeral public key, welcher little-endian ist.

#### Reply Record Unencrypted (ElGamal)

Verschlüsselte Größe: 528 Bytes

Verschlüsselte BuildReplyRecords sind 528 Bytes sowohl für ElGamal als auch ECIES, aus Kompatibilitätsgründen.

ElGamal-Antworten werden mit AES verschlüsselt.

```text
bytes   0-31: SHA-256 Hash of bytes 32-527
  bytes 32-526: random data
  byte     527: reply

  total length: 528
```
#### Reply Record Unencrypted (ECIES)

Alle Felder sind big-endian.

- Zuordnung für Build-Reply-Optionen hinzufügen
- Unverschlüsselter Datensatz ist länger, da weniger Verschlüsselungsoverhead vorhanden ist

Unverschlüsselte Größe: 528 Bytes

Dies ist die vorgeschlagene Spezifikation des tunnel BuildReplyRecord für ECIES-X25519 router. Zusammenfassung der Änderungen:

ECIES-Antworten werden mit ChaCha20/Poly1305 verschlüsselt.

```text
bytes    0-x: Tunnel Build Reply Options (Mapping)
  bytes    x-x: other data as implied by options
  bytes  x-510: Random padding
  byte     511: Reply byte
```
Alle Felder sind big-endian.

Unverschlüsselte Größe: 512 Bytes

- 0x00 (akzeptieren)
- 30 (TUNNEL_REJECT_BANDWIDTH)

#### Reply Record Encrypted (ECIES)

Die tunnel build reply Optionen sind eine Mapping-Struktur, wie in [Common Structures](/docs/specs/common-structures/) definiert. Diese ist für zukünftige Verwendung vorgesehen. Derzeit sind keine Optionen definiert. Wenn die Mapping-Struktur leer ist, sind dies zwei Bytes 0x00 0x00. Die maximale Größe des Mappings (einschließlich des Längenfelds) beträgt 511 Bytes, und der maximale Wert des Mapping-Längenfelds beträgt 509.

```text
bytes   0-511: ChaCha20 encrypted BuildReplyRecord
  bytes 512-527: Poly1305 MAC
```
Das Antwort-Byte ist einer der folgenden Werte, wie in [Tunnel Creation](/docs/specs/tunnel-implementation/) definiert, um Fingerprinting zu vermeiden:

### Anfrage-Verschlüsselung

Verschlüsselte Größe: 528 Bytes

Nach dem vollständigen Übergang zu ECIES-Datensätzen sind die Regeln für bereichsbasierte Auffüllung dieselben wie für Anfrage-Datensätze.

- "Verschlüsselung":

- Verschlüsselung im Entschlüsselungsmodus ausgeführt
- Anfragedatensätze präventiv in der Vorverarbeitung entschlüsselt (Verbergung verschlüsselter Anfragedatensätze)

- "Entschlüsselung":

- Verschlüsselung läuft im Verschlüsselungsmodus
- Anfrage-Datensätze verschlüsselt (enthüllen nächsten Klartext-Anfrage-Datensatz) durch Teilnehmer-Hops

- ChaCha20 hat keine "Modi", daher wird es einfach dreimal ausgeführt:

- einmal in der Vorverarbeitung
- einmal durch den Hop
- einmal bei der finalen Antwortverarbeitung

Gemischte Tunnel sind erlaubt und notwendig für den Übergang von ElGamal zu ECIES. Während der Übergangszeit wird eine steigende Anzahl von Routern unter ECIES-Schlüsseln betrieben werden.

Die Vorverarbeitung der symmetrischen Kryptographie wird auf die gleiche Weise ablaufen:

Wenn gemischte Tunnel verwendet werden, müssen Tunnel-Ersteller die symmetrische Verschlüsselung des BuildRequestRecord auf dem Verschlüsselungstyp des aktuellen und vorherigen Hops basieren.

Jeder Hop wird seinen eigenen Verschlüsselungstyp zum Verschlüsseln der BuildReplyRecords und der anderen Records in der VariableTunnelBuildMessage (VTBM) verwenden.

- Absender (OBGW) -> ElGamal (H1) -> ECIES (H2) -> ElGamal (H3)

Auf dem Antwortpfad muss der Endpunkt (Sender) die [Multiple Encryption](https://en.wikipedia.org/wiki/Multiple_encryption) rückgängig machen, indem er den Antwortschlüssel jedes Hops verwendet.

Als verdeutlichendes Beispiel betrachten wir einen ausgehenden Tunnel mit ECIES, umgeben von ElGamal:

Alle BuildRequestRecords befinden sich in ihrem verschlüsselten Zustand (unter Verwendung von ElGamal oder ECIES).

AES256/CBC-Verschlüsselung wird, wenn verwendet, weiterhin für jeden Datensatz verwendet, ohne Verkettung über mehrere Datensätze hinweg.

- H3s Datensatz wird "verschlüsselt" mit:

- H2's Antwortschlüssel (ChaCha20)
- H1's Antwortschlüssel (AES256/CBC)

- H2's Datensatz wird "verschlüsselt" mit:

- H1's Antwortschlüssel (AES256/CBC)

- H1s Datensatz wird ohne symmetrische Verschlüsselung gesendet

Ebenso wird ChaCha20 verwendet, um jeden Datensatz zu verschlüsseln, nicht streaming über die gesamte VTBM.

Die Anfrage-Datensätze werden vom Sender (OBGW) vorverarbeitet:

- Der Datensatz von H3 wird "entschlüsselt" mit:

- H3's Antwortschlüssel (AES256/CBC)

- H2's Datensatz wird "entschlüsselt" mit:

- H3's Antwortschlüssel (AES256/CBC)
- H2's Antwortschlüssel (ChaCha20-Poly1305)

- H1s Datensatz wird "entschlüsselt" mit:

- Antwortschlüssel von H3 (AES256/CBC)
- Antwortschlüssel von H2 (ChaCha20)
- Antwortschlüssel von H1 (AES256/CBC)

Nur H2 überprüft das Reply-Verschlüsselungs-Flag und sieht, dass es von AES256/CBC gefolgt wird.

- H3s Datensatz ist "verschlüsselt" unter Verwendung von:

- H3's Antwortschlüssel (AES256/CBC)

- H2's record ist "verschlüsselt" mit:

- H3's Antwortschlüssel (AES256/CBC)
- H2's Antwortschlüssel (ChaCha20-Poly1305)

- Der Datensatz von H1 ist „verschlüsselt" mit:

- H3's Antwortschlüssel (AES256/CBC)
- H2's Antwortschlüssel (ChaCha20)
- H1's Antwortschlüssel (AES256/CBC)

### Antwort-Verschlüsselung

Nachdem sie von jedem Hop verarbeitet wurden, befinden sich die Datensätze in einem "entschlüsselten" Zustand:

Der Tunnel-Ersteller, auch bekannt als Inbound Endpoint (IBEP), nachbearbeitet die Antwort:

#### KDF for Initial ck and h

Diese Schlüssel sind explizit in ElGamal BuildRequestRecords enthalten. Für ECIES BuildRequestRecords sind die tunnel keys und AES reply keys enthalten, aber die ChaCha reply keys werden aus dem DH-Austausch abgeleitet. Siehe [Proposal 156](/proposals/156-ecies-routers) für Details der statischen ECIES-Schlüssel des routers.

```text
This is the "e" message pattern:

  // Define protocol_name.
  Set protocol_name = "Noise_N_25519_ChaChaPoly_SHA256"
  (31 bytes, US-ASCII encoded, no NULL termination).

  // Define Hash h = 32 bytes
  // Pad to 32 bytes. Do NOT hash it, because it is not more than 32 bytes.
  h = protocol_name || 0

  Define ck = 32 byte chaining key. Copy the h data to ck.
  Set chainKey = h

  // MixHash(null prologue)
  h = SHA256(h);

  // up until here, can all be precalculated by all routers.
```
#### KDF for Request Record

Nachfolgend ist eine Beschreibung, wie die Schlüssel abgeleitet werden, die zuvor in Anfrage-Datensätzen übertragen wurden.

Dies ist standardmäßiges [NOISE](https://noiseprotocol.org/noise.html) für Muster "N" mit einem Standard-Protokollnamen.

ElGamal tunnel creators generieren ein ephemeres X25519-Schlüsselpaar für jeden ECIES-Hop im tunnel und verwenden das obige Schema zur Verschlüsselung ihres BuildRequestRecord. ElGamal tunnel creators werden das Schema vor dieser Spezifikation für die Verschlüsselung zu ElGamal-Hops verwenden.

ECIES tunnel creators müssen für jeden der ElGamal-Hops mit dessen öffentlichem Schlüssel verschlüsseln, unter Verwendung des in [Tunnel Creation](/docs/specs/tunnel-implementation/) definierten Schemas. ECIES tunnel creators werden das oben genannte Schema für die Verschlüsselung zu ECIES-Hops verwenden.

Das bedeutet, dass tunnel hops nur verschlüsselte Datensätze von ihrem gleichen Verschlüsselungstyp sehen werden.

```text
// Each hop's X25519 static keypair (hesk, hepk) from the Router Identity
  hesk = GENERATE_PRIVATE()
  hepk = DERIVE_PUBLIC(hesk)

  // MixHash(hepk)
  // || below means append
  h = SHA256(h || hepk);

  // up until here, can all be precalculated by each router
  // for all incoming build requests

  // Sender generates an X25519 ephemeral keypair per ECIES hop in the VTBM (sesk, sepk)
  sesk = GENERATE_PRIVATE()
  sepk = DERIVE_PUBLIC(sesk)

  // MixHash(sepk)
  h = SHA256(h || sepk);

  End of "e" message pattern.

  This is the "es" message pattern:

  // Noise es
  // Sender performs an X25519 DH with Hop's static public key.
  // Each Hop, finds the record w/ their truncated identity hash,
  // and extracts the Sender's ephemeral key preceding the encrypted record.
  sharedSecret = DH(sesk, hepk) = DH(hesk, sepk)

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // ChaChaPoly parameters to encrypt/decrypt
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  // Save for Reply Record KDF
  chainKey = keydata[0:31]

  // AEAD parameters
  k = keydata[32:63]
  n = 0
  plaintext = 464 byte build request record
  ad = h
  ciphertext = ENCRYPT(k, n, plaintext, ad)

  End of "es" message pattern.

  // MixHash(ciphertext)
  // Save for Reply Record KDF
  h = SHA256(h || ciphertext)
```
Für ElGamal- und ECIES-Tunnel-Ersteller werden sie einzigartige ephemerale X25519-Schlüsselpaare pro Hop generieren, um zu ECIES-Hops zu verschlüsseln.

### Begründung

**WICHTIG**: Ephemeral Keys müssen eindeutig pro ECIES-Hop und pro Build Record sein. Die Verwendung nicht eindeutiger Keys eröffnet einen Angriffsvektor für kollaborierende Hops, um zu bestätigen, dass sie sich im selben Tunnel befinden.

### Reply Record Encryption (ECIES)

``replyKey``, ``layerKey`` und ``layerIV`` müssen weiterhin in ElGamal-Records enthalten sein und können zufällig generiert werden.

```text
// AEAD parameters
  k = chainkey from build request
  n = 0
  plaintext = 512 byte build reply record
  ad = h from build request

  ciphertext = ENCRYPT(k, n, plaintext, ad)
```
### Build-Request-Datensätze

Wie in [Tunnel Creation](/docs/specs/tunnel-implementation/) definiert. Es gibt keine Änderungen bei der Verschlüsselung für ElGamal-Hops.

### Security Analysis

Der Antwortdatensatz ist mit ChaCha20/Poly1305 verschlüsselt.

Wie in [Tunnel Creation](/docs/specs/tunnel-implementation/) definiert. Es gibt keine Änderungen bei der Verschlüsselung für ElGamal-Hops.

ElGamal bietet keine Forward Secrecy für Tunnel Build Messages.

AES256/CBC steht etwas besser da und ist nur anfällig für eine theoretische Schwächung durch einen bekannten Klartext-`biclique`-Angriff.

Der einzige bekannte praktische Angriff gegen AES256/CBC ist ein Padding-Oracle-Angriff, wenn der IV dem Angreifer bekannt ist.

Ein Angreifer müsste die ElGamal-Verschlüsselung des nächsten Hops brechen, um an die AES256/CBC-Schlüsselinformationen (Antwortschlüssel und IV) zu gelangen.

ElGamal ist deutlich CPU-intensiver als ECIES, was zu potentieller Ressourcenerschöpfung führt.

## Bedrohungsmodell

ECIES, verwendet mit neuen ephemeren Schlüsseln pro BuildRequestRecord oder VariableTunnelBuildMessage, bietet Forward-Secrecy.

## Implementation Notes

* Ältere Router prüfen nicht den Verschlüsselungstyp des Hops und senden ElGamal-verschlüsselte
  Datensätze. Einige neuere Router sind fehlerhaft und senden verschiedene Arten von fehlerhaften Datensätzen.
  Implementierer sollten diese Datensätze vor der DH-Operation erkennen und ablehnen,
  falls möglich, um die CPU-Nutzung zu reduzieren.

## Issues

## Design

ChaCha20Poly1305 bietet AEAD-Verschlüsselung, wodurch der Empfänger die Nachrichtenintegrität vor dem Entschlüsselungsversuch überprüfen kann.

## Referenzen

* [Common](/docs/specs/common-structures/)
* [Cryptography](/docs/specs/cryptography/)
* [ECIES-X25519](/docs/specs/ecies/)
* [I2NP](/docs/specs/i2np/)
* [NOISE](https://noiseprotocol.org/noise.html)
* [NTCP2](/docs/specs/ntcp2/)
* [Prop119](/proposals/119-bidirectional-tunnels/)
* [Prop143](/proposals/143-build-message-options/)
* [Prop153](/proposals/153-chacha20-layer-encryption/)
* [Prop156](/proposals/156-ecies-routers/)
* [Prop157](/proposals/157-new-tbm/)
* [SPEC](/docs/specs/tunnel-implementation/#tunnel-creation-ecies)
* [Tunnel-Creation](/docs/specs/tunnel-implementation/#tunnel-creation-ecies)
* [Mehrfachverschlüsselung](https://en.wikipedia.org/wiki/Multiple_encryption)
* [RFC-7539](https://tools.ietf.org/html/rfc7539)
* [RFC-7748](https://tools.ietf.org/html/rfc7748)
