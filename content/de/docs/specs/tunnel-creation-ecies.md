---
title: "Spezifikation der Tunnel-Erstellung (ECIES-X25519)"
description: "Tunnel Build Nachrichten-Verschlüsselung mit ECIES-X25519 Krypto-Primitiven für Forward Secrecy."
slug: "tunnel-creation-ecies"
aliases:
  - "/de/docs/specs/tunnel-creation-ecies-spec"
  - "/de/docs/specs/tunnel-creation-ecies-spec/"
category: "Protokolle"
lastUpdated: "2025-06"
accurateFor: "0.9.66"
---

## Überblick

Dieses Dokument spezifiziert die Verschlüsselung von Tunnel Build-Nachrichten unter Verwendung kryptographischer Primitive, die durch [ECIES-X25519](/docs/specs/ecies/) eingeführt wurden. Es ist ein Teil des Gesamtvorschlags [Prop156](/proposals/156/) zur Umstellung von Routern von ElGamal- auf ECIES-X25519-Schlüssel.

Es sind zwei Versionen spezifiziert. Die erste verwendet die bestehenden Build-Nachrichten und Build-Record-Größe, für Kompatibilität mit ElGamal-Routern. Diese Spezifikation wurde ab Release 0.9.48 implementiert und ist nun veraltet. Die zweite verwendet zwei neue Build-Nachrichten und eine kleinere Build-Record-Größe und darf nur mit ECIES-Routern verwendet werden. Diese Spezifikation ist ab Release 0.9.51 implementiert.

Für die Zwecke der Umstellung des Netzwerks von ElGamal + AES256 auf ECIES + ChaCha20 sind tunnel mit gemischten ElGamal- und ECIES-Routern erforderlich. Spezifikationen für den Umgang mit gemischten Tunnel-Hops werden bereitgestellt. Es werden keine Änderungen am Format, der Verarbeitung oder der Verschlüsselung von ElGamal-Hops vorgenommen. Dieses Format behält die gleiche Größe für Tunnel-Build-Records bei, wie es für die Kompatibilität erforderlich ist.

ElGamal tunnel-Ersteller werden ephemerale X25519-Schlüsselpaare pro Hop generieren und dieser Spezifikation folgen, um tunnel mit ECIES-Hops zu erstellen.

Dieses Dokument spezifiziert ECIES-X25519 Tunnel Building. Für einen Überblick über alle Änderungen, die für ECIES router erforderlich sind, siehe Vorschlag 156 [Prop156](/proposals/156/). Für zusätzliche Hintergrundinformationen zur Entwicklung der Long-Record-Spezifikation siehe Vorschlag 152 [Prop152](/proposals/152/). Für zusätzliche Hintergrundinformationen zur Entwicklung der Short-Record-Spezifikation siehe Vorschlag 157 [Prop157](/proposals/157/).

### Kryptographische Grundbausteine

Die zur Implementierung dieser Spezifikation erforderlichen Grundbausteine sind:

- AES-256-CBC wie in [Cryptography](/docs/specs/cryptography/)
- STREAM ChaCha20 Funktionen: ENCRYPT(k, iv, plaintext) und DECRYPT(k, iv, ciphertext) - wie in [EncryptedLeaseSet](/docs/specs/encryptedleaseset/) und [RFC-7539](https://tools.ietf.org/html/rfc7539)
- STREAM ChaCha20/Poly1305 Funktionen: ENCRYPT(k, n, plaintext, ad) und DECRYPT(k, n, ciphertext, ad) - wie in [NTCP2](/docs/specs/ntcp2/), [ECIES-X25519](/docs/specs/ecies/) und [RFC-7539](https://tools.ietf.org/html/rfc7539)
- X25519 DH Funktionen - wie in [NTCP2](/docs/specs/ntcp2/) und [ECIES-X25519](/docs/specs/ecies/)
- HKDF(salt, ikm, info, n) - wie in [NTCP2](/docs/specs/ntcp2/) und [ECIES-X25519](/docs/specs/ecies/)

Andere Noise-Funktionen, die andernorts definiert sind:

- MixHash(d) - wie in [NTCP2](/docs/specs/ntcp2/) und [ECIES-X25519](/docs/specs/ecies/)
- MixKey(d) - wie in [NTCP2](/docs/specs/ntcp2/) und [ECIES-X25519](/docs/specs/ecies/)

## Design

### Noise Protocol Framework

Diese Spezifikation stellt die Anforderungen basierend auf dem Noise Protocol Framework [NOISE](https://noiseprotocol.org/noise.html) (Revision 34, 2018-07-11) bereit. In der Noise-Terminologie ist Alice die Initiatorin und Bob der Responder.

Es basiert auf dem Noise-Protokoll Noise_N_25519_ChaChaPoly_SHA256. Dieses Noise-Protokoll verwendet die folgenden Primitive:

- One-Way Handshake Pattern: N - Alice übermittelt ihren statischen Schlüssel nicht an Bob (N)
- DH Function: X25519 - X25519 DH mit einer Schlüssellänge von 32 Bytes wie in [RFC-7748](https://tools.ietf.org/html/rfc7748) spezifiziert
- Cipher Function: ChaChaPoly - AEAD_CHACHA20_POLY1305 wie in [RFC-7539](https://tools.ietf.org/html/rfc7539) Abschnitt 2.8 spezifiziert. 12-Byte-Nonce, wobei die ersten 4 Bytes auf null gesetzt sind. Identisch zu dem in [NTCP2](/docs/specs/ntcp2/)
- Hash Function: SHA256 - Standard 32-Byte-Hash, bereits umfangreich in I2P verwendet

### Handshake-Muster

Handshakes verwenden [Noise](https://noiseprotocol.org/noise.html) Handshake-Muster.

Die folgende Buchstabenzuordnung wird verwendet:

- e = einmaliger ephemerer Schlüssel
- s = statischer Schlüssel
- p = Nachrichten-Payload

Die Build-Anfrage ist identisch zum Noise N-Pattern. Dies ist auch identisch zur ersten (Session Request) Nachricht im XK-Pattern, das in [NTCP2](/docs/specs/ntcp2/) verwendet wird.

```
<- s
  ...
  e es p ->
```
### Anfragenverschlüsselung

Build-Request-Datensätze werden vom tunnel creator erstellt und asymmetrisch für den jeweiligen Hop verschlüsselt. Diese asymmetrische Verschlüsselung der Request-Datensätze ist derzeit ElGamal, wie in [Cryptography](/docs/specs/cryptography/) definiert, und enthält eine SHA-256-Prüfsumme. Dieses Design bietet keine Forward Secrecy.

Das ECIES-Design verwendet das Einweg-Noise-Muster "N" mit ECIES-X25519 ephemeral-static DH, mit einem HKDF und ChaCha20/Poly1305 AEAD für Forward Secrecy, Integrität und Authentifizierung. Alice ist der tunnel Build-Anforderer. Jeder Hop im tunnel ist ein Bob.

### Antwort-Verschlüsselung

Build-Antwort-Datensätze werden vom Hop-Ersteller erstellt und symmetrisch an den Ersteller verschlüsselt. Diese symmetrische Verschlüsselung von ElGamal-Antwort-Datensätzen ist AES mit einer vorangestellten SHA-256-Prüfsumme. Dieses Design ist nicht forward-secret.

ECIES-Antworten verwenden ChaCha20/Poly1305 AEAD für Integrität und Authentifizierung.

## Long Record Spezifikation

HINWEIS: Veraltet, obsolet. Verwenden Sie das unten spezifizierte Short Record Format.

### Build Request Records

Verschlüsselte BuildRequestRecords sind sowohl für ElGamal als auch für ECIES 528 Bytes groß, aus Kompatibilitätsgründen.

#### Anfragedatensatz unverschlüsselt

Dies ist die Spezifikation des tunnel BuildRequestRecord für ECIES-X25519 router. Zusammenfassung der Änderungen:

- Entfernen Sie ungenutzten 32-Byte-router-Hash
- Ändern Sie die Anfragezeit von Stunden zu Minuten
- Fügen Sie ein Ablauffeld für zukünftige variable tunnel-Zeit hinzu
- Fügen Sie mehr Platz für Flags hinzu
- Fügen Sie Mapping für zusätzliche Build-Optionen hinzu
- AES-256-Antwortschlüssel und IV werden nicht für den eigenen Antwortdatensatz des Hops verwendet
- Unverschlüsselter Datensatz ist länger, da weniger Verschlüsselungsaufwand besteht

Der Anfrage-Datensatz enthält keine ChaCha-Antwortschlüssel. Diese Schlüssel werden von einer KDF abgeleitet. Siehe unten.

Alle Felder sind im Big-Endian-Format.

Unverschlüsselte Größe: 464 Bytes

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-3</td><td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel ID to receive messages as, nonzero</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">4-7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next tunnel ID, nonzero</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">8-39</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next router identity hash</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">40-71</td><td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 tunnel layer key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">72-103</td><td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 tunnel IV key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">104-135</td><td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 reply key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">136-151</td><td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 reply IV</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">152</td><td style="border:1px solid var(--color-border); padding:0.6rem;">flags</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">153-155</td><td style="border:1px solid var(--color-border); padding:0.6rem;">more flags, unused, set to 0 for compatibility</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">156-159</td><td style="border:1px solid var(--color-border); padding:0.6rem;">request time (in minutes since the epoch, rounded down)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">160-163</td><td style="border:1px solid var(--color-border); padding:0.6rem;">request expiration (in seconds since creation)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">164-167</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next message ID</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">168-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel build options (Mapping)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">other data as implied by flags or options</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-463</td><td style="border:1px solid var(--color-border); padding:0.6rem;">random padding</td></tr>
</tbody>
</table>
Das Flags-Feld ist dasselbe wie in [Tunnel-Creation](/docs/specs/tunnel-creation/) definiert und enthält folgendes:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bit</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;" colspan="2"><em>Bit order: 76543210 (bit 7 is MSB)</em></td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">if set, allow messages from anyone</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">6</td><td style="border:1px solid var(--color-border); padding:0.6rem;">if set, allow messages to anyone, and send the reply to the specified next hop in a Tunnel Build Reply Message</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">5-0</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Undefined, must set to 0 for compatibility with future options</td></tr>
</tbody>
</table>
Bit 7 zeigt an, dass der Hop ein eingehender gateway (IBGW) sein wird. Bit 6 zeigt an, dass der Hop ein ausgehender Endpunkt (OBEP) sein wird. Wenn keines der beiden Bits gesetzt ist, wird der Hop ein Zwischenteilnehmer sein. Beide können nicht gleichzeitig gesetzt werden.

Die Anfrage-Ablaufzeit ist für zukünftige variable tunnel-Dauer gedacht. Derzeit ist der einzige unterstützte Wert 600 (10 Minuten).

Die tunnel build options sind eine Mapping-Struktur wie in [Common](/docs/specs/common-structures/) definiert. Die einzigen derzeit definierten Optionen sind für Bandbreitenparameter, ab API 0.9.65, siehe unten für Details. Wenn die Mapping-Struktur leer ist, sind dies zwei Bytes 0x00 0x00. Die maximale Größe des Mappings (einschließlich des Längenfelds) beträgt 296 Bytes, und der maximale Wert des Mapping-Längenfelds beträgt 294.

#### Request Record verschlüsselt

Alle Felder sind Big-Endian, außer dem ephemeren öffentlichen Schlüssel, der Little-Endian ist.

Verschlüsselte Größe: 528 Bytes

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-15</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Hop's truncated identity hash</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">16-47</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Sender's ephemeral X25519 public key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">48-511</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20 encrypted BuildRequestRecord</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">512-527</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Poly1305 MAC</td></tr>
</tbody>
</table>
### Reply Records erstellen

Verschlüsselte BuildReplyRecords sind 528 Bytes sowohl für ElGamal als auch für ECIES, aus Kompatibilitätsgründen.

#### Reply Record Unverschlüsselt

Dies ist die Spezifikation des tunnel BuildReplyRecord für ECIES-X25519 router. Zusammenfassung der Änderungen:

- Zuordnung für Build-Reply-Optionen hinzufügen
- Unverschlüsselter Datensatz ist länger, da weniger Verschlüsselungsoverhead vorhanden ist

ECIES-Antworten werden mit ChaCha20/Poly1305 verschlüsselt.

Alle Felder sind im Big-Endian-Format.

Unverschlüsselte Größe: 512 Bytes

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel Build Reply Options (Mapping)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">other data as implied by options</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-510</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Random padding</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">511</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Reply byte</td></tr>
</tbody>
</table>
Die tunnel build reply Optionen sind eine Mapping-Struktur, wie in [Common](/docs/specs/common-structures/) definiert. Die einzigen derzeit definierten Optionen sind für Bandbreitenparameter, ab API 0.9.65, siehe unten für Details. Wenn die Mapping-Struktur leer ist, sind dies zwei Bytes 0x00 0x00. Die maximale Größe des Mapping (einschließlich des Längenfelds) beträgt 511 Bytes, und der maximale Wert des Mapping-Längenfelds ist 509.

Das Antwort-Byte ist einer der folgenden Werte, wie in [Tunnel-Creation](/docs/specs/tunnel-creation/) definiert, um Fingerprinting zu vermeiden:

- 0x00 (akzeptieren)
- 30 (TUNNEL_REJECT_BANDWIDTH)

#### Antwort-Datensatz verschlüsselt

Verschlüsselte Größe: 528 Bytes

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-511</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20 encrypted BuildReplyRecord</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">512-527</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Poly1305 MAC</td></tr>
</tbody>
</table>
Nach der vollständigen Umstellung auf ECIES-Datensätze sind die Regeln für bereichsbasierte Auffüllung dieselben wie für Anfrage-Datensätze.

### Symmetrische Verschlüsselung von Datensätzen

Gemischte Tunnel sind erlaubt und notwendig für den Übergang von ElGamal zu ECIES. Während der Übergangszeit wird eine zunehmende Anzahl von Routern unter ECIES-Schlüsseln verschlüsselt sein.

Die Vorverarbeitung der symmetrischen Kryptographie läuft auf die gleiche Weise ab:

- "encryption":
  - Cipher läuft im Entschlüsselungsmodus
  - Anfrage-Datensätze werden präventiv in der Vorverarbeitung entschlüsselt (verbirgt verschlüsselte Anfrage-Datensätze)
- "decryption":
  - Cipher läuft im Verschlüsselungsmodus
  - Anfrage-Datensätze werden von den Teilnehmer-Hops verschlüsselt (enthüllt den nächsten Klartext-Anfrage-Datensatz)
- ChaCha20 hat keine "Modi", daher wird es einfach dreimal ausgeführt:
  - einmal in der Vorverarbeitung
  - einmal vom Hop
  - einmal bei der finalen Antwortverarbeitung

Wenn gemischte Tunnel verwendet werden, müssen Tunnel-Ersteller die symmetrische Verschlüsselung des BuildRequestRecord auf dem Verschlüsselungstyp des aktuellen und vorherigen Hops basieren.

Jeder Hop wird seinen eigenen Verschlüsselungstyp zum Verschlüsseln der BuildReplyRecords und der anderen Records in der VariableTunnelBuildMessage (VTBM) verwenden.

Auf dem Antwortpfad muss der Endpunkt (Sender) die [Multiple-Encryption](https://en.wikipedia.org/wiki/Multiple_encryption) rückgängig machen, indem er den Antwortschlüssel jedes Hops verwendet.

Als verdeutlichendes Beispiel schauen wir uns einen ausgehenden Tunnel mit ECIES betrachten, der von ElGamal umgeben ist:

- Absender (OBGW) -> ElGamal (H1) -> ECIES (H2) -> ElGamal (H3)

Alle BuildRequestRecords befinden sich in ihrem verschlüsselten Zustand (mit ElGamal oder ECIES).

Die AES256/CBC-Verschlüsselung wird, wenn sie verwendet wird, weiterhin für jeden Datensatz einzeln eingesetzt, ohne Verkettung über mehrere Datensätze hinweg.

Ebenso wird ChaCha20 verwendet, um jeden Datensatz zu verschlüsseln, nicht um über das gesamte VTBM zu streamen.

Die Anfrage-Datensätze werden vom Sender (OBGW) vorverarbeitet:

- H3's Datensatz wird "verschlüsselt" mit:
  - H2's reply key (ChaCha20)
  - H1's reply key (AES256/CBC)
- H2's Datensatz wird "verschlüsselt" mit:
  - H1's reply key (AES256/CBC)
- H1's Datensatz wird ohne symmetrische Verschlüsselung gesendet

Nur H2 überprüft das Reply-Verschlüsselungs-Flag und sieht, dass darauf AES256/CBC folgt.

Nachdem sie von jedem Hop verarbeitet wurden, befinden sich die Datensätze in einem "entschlüsselten" Zustand:

- H3's Datensatz wird "entschlüsselt" mit:
  - H3's reply key (AES256/CBC)
- H2's Datensatz wird "entschlüsselt" mit:
  - H3's reply key (AES256/CBC)
  - H2's reply key (ChaCha20-Poly1305)
- H1's Datensatz wird "entschlüsselt" mit:
  - H3's reply key (AES256/CBC)
  - H2's reply key (ChaCha20)
  - H1's reply key (AES256/CBC)

Der tunnel-Ersteller, auch bekannt als Inbound Endpoint (IBEP), nachbearbeitet die Antwort:

- H3's Datensatz wird "verschlüsselt" mit:
  - H3's Antwortschlüssel (AES256/CBC)
- H2's Datensatz wird "verschlüsselt" mit:
  - H3's Antwortschlüssel (AES256/CBC)
  - H2's Antwortschlüssel (ChaCha20-Poly1305)
- H1's Datensatz wird "verschlüsselt" mit:
  - H3's Antwortschlüssel (AES256/CBC)
  - H2's Antwortschlüssel (ChaCha20)
  - H1's Antwortschlüssel (AES256/CBC)

### Request Record Schlüssel

Diese Schlüssel sind explizit in ElGamal BuildRequestRecords enthalten. Für ECIES BuildRequestRecords sind die tunnel-Schlüssel und AES-Antwortschlüssel enthalten, aber die ChaCha-Antwortschlüssel werden aus dem DH-Austausch abgeleitet. Siehe [Prop156](/proposals/156/) für Details zu den statischen ECIES-Schlüsseln des routers.

Nachfolgend wird beschrieben, wie die Schlüssel abgeleitet werden, die zuvor in Anfragedatensätzen übertragen wurden.

#### KDF für anfängliches ck und h

Dies ist Standard-[NOISE](https://noiseprotocol.org/noise.html) für Muster "N" mit einem Standard-Protokollnamen.

```
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
#### KDF für Request Record

ElGamal tunnel-Ersteller generieren ein ephemeres X25519-Schlüsselpaar für jeden ECIES-Hop im tunnel und verwenden das obige Schema zur Verschlüsselung ihres BuildRequestRecord. ElGamal tunnel-Ersteller werden das Schema vor dieser Spezifikation zur Verschlüsselung an ElGamal-Hops verwenden.

ECIES tunnel-Ersteller müssen für jeden der ElGamal-Hops mit dem öffentlichen Schlüssel unter Verwendung des in [Tunnel-Creation](/docs/specs/tunnel-creation/) definierten Schemas verschlüsseln. ECIES tunnel-Ersteller werden das oben genannte Schema für die Verschlüsselung zu ECIES-Hops verwenden.

Das bedeutet, dass tunnel-Hops nur verschlüsselte Datensätze von ihrem gleichen Verschlüsselungstyp sehen werden.

Für ElGamal- und ECIES-Tunnel-Ersteller werden sie eindeutige ephemerale X25519-Schlüsselpaare pro Hop generieren, um an ECIES-Hops zu verschlüsseln.

**WICHTIG**: Ephemere Schlüssel müssen für jeden ECIES-Hop und für jeden Build-Record eindeutig sein. Die Verwendung nicht-eindeutiger Schlüssel eröffnet einen Angriffsvektor für kollaborierenden Hops, um zu bestätigen, dass sie sich im selben tunnel befinden.

```
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
`replyKey`, `layerKey` und `layerIV` müssen weiterhin in ElGamal-Datensätzen enthalten sein und können zufällig generiert werden.

### Reply Record Verschlüsselung

Der Antwortdatensatz ist ChaCha20/Poly1305 verschlüsselt.

```
// AEAD parameters
k = chainkey from build request
n = 0
plaintext = 512 byte build reply record
ad = h from build request

ciphertext = ENCRYPT(k, n, plaintext, ad)
```
## Short Record Spezifikation

Diese Spezifikation verwendet zwei neue I2NP tunnel build messages, Short Tunnel Build Message (Typ 25) und Outbound Tunnel Build Reply Message (Typ 26).

Der tunnel-Ersteller und alle Hops im erstellten tunnel müssen ECIES-X25519 unterstützen und mindestens Version 0.9.51 haben. Die Hops im Antwort-tunnel (für einen ausgehenden Build) oder im ausgehenden tunnel (für einen eingehenden Build) haben keine Anforderungen.

Verschlüsselte Anfrage- und Antwort-Datensätze werden 218 Bytes groß sein, verglichen mit 528 Bytes für alle anderen Build-Nachrichten.

Die Klartext-Anfrage-Datensätze werden 154 Bytes groß sein, verglichen mit 222 Bytes für ElGamal-Datensätze und 464 Bytes für ECIES-Datensätze wie oben definiert.

Die Klartext-Antwortdatensätze werden 202 Bytes groß sein, verglichen mit 496 Bytes für ElGamal-Datensätze und 512 Bytes für ECIES-Datensätze wie oben definiert.

Die Antwort-Verschlüsselung wird ChaCha20/Poly1305 für den eigenen Datensatz des Hops und ChaCha20 (NICHT ChaCha20/Poly1305) für die anderen Datensätze in der Build-Nachricht sein.

Request-Datensätze werden durch die Verwendung von HKDF zur Erstellung der Layer- und Antwortschlüssel kleiner gemacht, sodass sie nicht explizit in die Anfrage einbezogen werden.

### Nachrichtenfluss

```
STBM: Short tunnel build message (type 25)
OTBRM: Outbound tunnel build reply message (type 26)

Outbound Build A-B-C
Reply through existing inbound D-E-F


                New Tunnel
         STBM      STBM      STBM
Creator ------> A ------> B ------> C ---\
                                   OBEP   \
                                          | Garlic wrapped (optional)
                                          | OTBRM
                                          | (TUNNEL delivery)
                                          | from OBEP to
                                          | creator
              Existing Tunnel             /
Creator <-------F---------E-------- D <--/
                                   IBGW



Inbound Build D-E-F
Sent through existing outbound A-B-C


              Existing Tunnel
Creator ------> A ------> B ------> C ---\
                                  OBEP    \
                                          | Garlic wrapped (optional)
                                          | STBM
                                          | (ROUTER delivery)
                                          | from creator
                New Tunnel                | to IBGW
          STBM      STBM      STBM        /
Creator <------ F <------ E <------ D <--/
                                   IBGW
```
#### Notizen

Die Garlic-Verschlüsselung der Nachrichten verbirgt sie vor dem OBEP (bei einem eingehenden Build) oder dem IBGW (bei einem ausgehenden Build). Dies wird empfohlen, ist aber nicht erforderlich. Wenn OBEP und IBGW derselbe Router sind, ist es nicht notwendig.

### Kurze Build Request Records

Kurze verschlüsselte BuildRequestRecords sind 218 Bytes groß.

#### Kurzer Anfrage-Datensatz Unverschlüsselt

Zusammenfassung der Änderungen aus langen Datensätzen:

- Änderung der unverschlüsselten Länge von 464 auf 154 Bytes
- Änderung der verschlüsselten Länge von 528 auf 218 Bytes
- Entfernung der Layer- und Antwortschlüssel sowie IVs, sie werden aus einer KDF generiert

Der Request-Datensatz enthält keine ChaCha-Antwortschlüssel. Diese Schlüssel werden aus einer KDF abgeleitet. Siehe unten.

Alle Felder sind in Big-Endian-Format.

Unverschlüsselte Größe: 154 Bytes.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-3</td><td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel ID to receive messages as, nonzero</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">4-7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next tunnel ID, nonzero</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">8-39</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next router identity hash</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">40</td><td style="border:1px solid var(--color-border); padding:0.6rem;">flags</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">41-42</td><td style="border:1px solid var(--color-border); padding:0.6rem;">more flags, unused, set to 0 for compatibility</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">43</td><td style="border:1px solid var(--color-border); padding:0.6rem;">layer encryption type</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">44-47</td><td style="border:1px solid var(--color-border); padding:0.6rem;">request time (in minutes since the epoch, rounded down)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">48-51</td><td style="border:1px solid var(--color-border); padding:0.6rem;">request expiration (in seconds since creation)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">52-55</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next message ID</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">56-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel build options (Mapping)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">other data as implied by flags or options</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-153</td><td style="border:1px solid var(--color-border); padding:0.6rem;">random padding (see below)</td></tr>
</tbody>
</table>
Das Flags-Feld ist dasselbe wie in [Tunnel-Creation](/docs/specs/tunnel-creation/) definiert und enthält folgendes:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bit</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;" colspan="2"><em>Bit order: 76543210 (bit 7 is MSB)</em></td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">if set, allow messages from anyone</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">6</td><td style="border:1px solid var(--color-border); padding:0.6rem;">if set, allow messages to anyone, and send the reply to the specified next hop in a Tunnel Build Reply Message</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">5-0</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Undefined, must set to 0 for compatibility with future options</td></tr>
</tbody>
</table>
Bit 7 zeigt an, dass der Hop ein eingehender Gateway (IBGW) sein wird. Bit 6 zeigt an, dass der Hop ein ausgehender Endpunkt (OBEP) sein wird. Wenn keines der Bits gesetzt ist, wird der Hop ein zwischenliegender Teilnehmer sein. Beide können nicht gleichzeitig gesetzt sein.

Layer-Verschlüsselungstyp: 0 für AES (wie in aktuellen Tunneln); 1 für zukünftig (ChaCha?)

Das Anfrage-Ablaufdatum ist für zukünftige variable tunnel-Dauer vorgesehen. Derzeit ist der einzige unterstützte Wert 600 (10 Minuten).

Der ephemere öffentliche Schlüssel des Erstellers ist ein ECIES-Schlüssel, Big-Endian. Er wird für die KDF für die IBGW-Schicht und Antwortschlüssel und IVs verwendet. Dies ist nur im Klartext-Datensatz in einer Inbound Tunnel Build-Nachricht enthalten. Es ist erforderlich, da es auf dieser Schicht keinen DH für den Build-Datensatz gibt.

Die tunnel build Optionen sind eine Mapping-Struktur wie in [Common](/docs/specs/common-structures/) definiert. Die einzigen derzeit definierten Optionen sind für Bandbreitenparameter, ab API 0.9.65, siehe unten für Details. Wenn die Mapping-Struktur leer ist, sind dies zwei Bytes 0x00 0x00. Die maximale Größe des Mapping (einschließlich des Längenfelds) beträgt 98 Bytes, und der Maximalwert des Mapping-Längenfelds ist 96.

#### Kurzer Anfrage-Datensatz Verschlüsselt

Alle Felder sind im Big-Endian-Format, außer dem ephemeral public key, der im Little-Endian-Format ist.

Verschlüsselte Größe: 218 Bytes

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-15</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Hop's truncated identity hash</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">16-47</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Sender's ephemeral X25519 public key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">48-201</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20 encrypted ShortBuildRequestRecord</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">202-217</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Poly1305 MAC</td></tr>
</tbody>
</table>
### Kurze Build Reply Records

Kurze verschlüsselte BuildReplyRecords sind 218 Bytes lang.

#### Kurzer Antwortdatensatz Unverschlüsselt

Zusammenfassung der Änderungen aus langen Datensätzen:

- Unverschlüsselte Länge von 512 auf 202 Bytes ändern
- Verschlüsselte Länge von 528 auf 218 Bytes ändern

ECIES-Antworten werden mit ChaCha20/Poly1305 verschlüsselt.

Alle Felder sind big-endian.

Unverschlüsselte Größe: 202 Bytes.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel Build Reply Options (Mapping)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">other data as implied by options</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-200</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Random padding (see below)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">201</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Reply byte</td></tr>
</tbody>
</table>
Die tunnel build reply Optionen sind eine Mapping-Struktur, wie in [Common](/docs/specs/common-structures/) definiert. Die einzigen derzeit definierten Optionen sind für Bandbreitenparameter, seit API 0.9.65, siehe unten für Details. Wenn die Mapping-Struktur leer ist, sind dies zwei Bytes 0x00 0x00. Die maximale Größe des Mappings (einschließlich des Längenfelds) beträgt 201 Bytes, und der maximale Wert des Mapping-Längenfelds ist 199.

Das Antwort-Byte ist einer der folgenden Werte, wie in [Tunnel-Creation](/docs/specs/tunnel-creation/) definiert, um Fingerprinting zu vermeiden:

- 0x00 (akzeptieren)
- 30 (TUNNEL_REJECT_BANDWIDTH)

Ein zusätzlicher Antwortwert kann in Zukunft definiert werden, um die Ablehnung für nicht unterstützte Optionen zu repräsentieren.

#### Kurzer Antwort-Datensatz verschlüsselt

Verschlüsselte Größe: 218 Bytes

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-201</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20 encrypted ShortBuildReplyRecord</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">202-217</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Poly1305 MAC</td></tr>
</tbody>
</table>
### KDF

Wir verwenden den chaining key (ck) aus dem Noise-Zustand nach der Verschlüsselung/Entschlüsselung des tunnel build record, um folgende Schlüssel abzuleiten: reply key, AES layer key, AES IV key und garlic reply key/tag für den OBEP.

Reply keys: Beachten Sie, dass die KDF für die OBEP- und Nicht-OBEP-Hops leicht unterschiedlich ist. Im Gegensatz zu langen Datensätzen können wir den linken Teil von ck nicht für den Reply-Schlüssel verwenden, da er nicht der letzte ist und später verwendet wird. Der Reply-Schlüssel wird verwendet, um die Antwort für diesen Datensatz mit AEAD/ChaCha20/Poly1305 zu verschlüsseln und ChaCha20 für die Antwort auf andere Datensätze. Beide verwenden denselben Schlüssel. Die Nonce ist die Position des Datensatzes in der Nachricht, beginnend bei 0. Siehe unten für Details.

```
keydata = HKDF(ck, ZEROLEN, "SMTunnelReplyKey", 64)
replyKey = keydata[32:63]
ck = keydata[0:31]

AES Layer key:
keydata = HKDF(ck, ZEROLEN, "SMTunnelLayerKey", 64)
layerKey = keydata[32:63]

IV key for non-OBEP record:
ivKey = keydata[0:31]
because it's last

IV key for OBEP record:
ck = keydata[0:31]
keydata = HKDF(ck, ZEROLEN, "TunnelLayerIVKey", 64)
ivKey = keydata[32:63]
ck = keydata[0:31]

OBEP garlic reply key/tag:
keydata = HKDF(ck, ZEROLEN, "RGarlicKeyAndTag", 64)
garlicReplyKey = keydata[32:63]
garlicReplyTag = keydata[0:7]
```
Hinweis: Die KDF für den IV-Schlüssel am OBEP unterscheidet sich von der für die anderen Hops, auch wenn die Antwort nicht mit garlic encryption verschlüsselt ist.

#### Datensatz-Verschlüsselung

Der eigene Antwortdatensatz des Hops wird mit ChaCha20/Poly1305 verschlüsselt. Dies ist dasselbe wie bei der oben genannten langen Datensatzspezifikation, AUSSER dass 'n' die Datensatznummer 0-7 ist, anstatt immer 0 zu sein. Siehe [RFC-7539](https://tools.ietf.org/html/rfc7539).

```
// AEAD parameters
k = replyKey from KDF above
n = record number 0-7
plaintext = 202 byte build reply record
ad = h from build request

ciphertext = ENCRYPT(k, n, plaintext, ad)
```
Die anderen Records werden iterativ und symmetrisch an jedem Hop mit ChaCha20 verschlüsselt (NICHT ChaCha20/Poly1305). Dies unterscheidet sich von der oben beschriebenen Long-Record-Spezifikation, die AES verwendet und nicht die Record-Nummer nutzt.

Die Datensatznummer wird im IV an Byte 4 eingefügt, da ChaCha20 einen 12-Byte-IV mit einer Little-Endian-Nonce an den Bytes 4-11 verwendet. Siehe [RFC-7539](https://tools.ietf.org/html/rfc7539).

```
// Parameters
k = replyKey from KDF above
n = record number 0-7
iv = 12 bytes, all zeros except iv[4] = n
plaintext = 218 byte encrypted record

ciphertext = ENCRYPT(k, iv, plaintext)
```
#### Garlic Encryption

Die Garlic-Verpackung der Nachrichten verbirgt sie vor dem OBEP (bei einem eingehenden Build) oder dem IBGW (bei einem ausgehenden Build). Dies wird empfohlen, ist aber nicht erforderlich. Wenn OBEP und IBGW derselbe Router sind, ist es nicht notwendig.

Garlic encryption einer eingehenden Short Tunnel Build Message durch den Ersteller, verschlüsselt an das ECIES IBGW, verwendet Noise 'N' Verschlüsselung, wie in [ECIES-ROUTERS](/docs/specs/ecies-routers/) definiert.

Garlic encryption einer Outbound Tunnel Build Reply Message durch den OBEP, verschlüsselt für den Ersteller, verwendet Existing Session Nachrichten mit dem 32-Byte garlic reply key und 8-Byte garlic reply tag aus der oben genannten KDF. Das Format ist wie für Antworten auf Database Lookups in [I2NP](/docs/specs/i2np/), [ECIES-ROUTERS](/docs/specs/ecies-routers/) und [ECIES-X25519](/docs/specs/ecies/) spezifiziert.

#### Schichtverschlüsselung

Diese Spezifikation enthält ein Feld für den Layer-Verschlüsselungstyp im Build-Request-Record. Die einzige derzeit unterstützte Layer-Verschlüsselung ist Typ 0, welches AES ist. Dies ist unverändert gegenüber vorherigen Spezifikationen, außer dass der Layer-Key und IV-Key aus der oben genannten KDF abgeleitet werden, anstatt im Build-Request-Record enthalten zu sein.

Das Hinzufügen neuer Layer-Verschlüsselungstypen, beispielsweise ChaCha20, ist ein Thema für weitere Forschung und ist derzeit nicht Teil dieser Spezifikation.

## Implementierungshinweise

- Ältere router überprüfen nicht den Verschlüsselungstyp des Hops und senden ElGamal-verschlüsselte Datensätze. Einige neuere router sind fehlerhaft und senden verschiedene Arten von fehlerhaften Datensätzen. Implementierer sollten diese Datensätze vor der DH-Operation erkennen und ablehnen, wenn möglich, um die CPU-Nutzung zu reduzieren.

### Build-Datensätze

Die Reihenfolge der Build-Records muss randomisiert werden, damit mittlere Hops ihre Position innerhalb des tunnels nicht kennen.

Die empfohlene Mindestanzahl von Build-Records ist 4. Wenn es mehr Build-Records als Hops gibt, müssen "gefälschte" Records hinzugefügt werden, die zufällige oder implementierungsspezifische Daten enthalten. Für eingehende Tunnel-Builds muss immer ein "gefälschter" Record für den ursprünglichen Router vorhanden sein, mit dem korrekten 16-Byte-Hash-Präfix und einem echten X25519-Ephemeral-Key, andernfalls wird der nächstliegende Hop wissen, dass der nächste Hop der Originator ist.

Der Rest des "gefälschten" Eintrags kann zufällige Daten enthalten oder in einem beliebigen Format verschlüsselt sein, damit der Urheber Daten über den Build an sich selbst senden kann, möglicherweise um die Speicheranforderungen für ausstehende Builds zu reduzieren.

Urheber von eingehenden Tunneln müssen eine Methode verwenden, um zu validieren, dass ihr "gefälschter" Datensatz nicht vom vorherigen Hop modifiziert wurde, da dies auch zur Deanonymisierung verwendet werden könnte. Der Urheber kann eine Prüfsumme des Datensatzes speichern und verifizieren, oder die Prüfsumme in den Datensatz einschließen, oder eine AEAD-Verschlüsselungs-/Entschlüsselungsfunktion verwenden, implementierungsabhängig. Wenn das 16-Byte-Hash-Präfix oder andere Build-Datensatzinhalte modifiziert wurden, muss der Router den Tunnel verwerfen.

Gefälschte Datensätze für ausgehende tunnel und zusätzliche gefälschte Datensätze für eingehende tunnel haben diese Anforderungen nicht und können völlig zufällige Daten sein, da sie niemals für irgendeinen Hop sichtbar sein werden. Es kann dennoch wünschenswert sein, dass der Urheber validiert, dass sie nicht modifiziert wurden.

## Tunnel-Bandbreiten-Parameter

### Übersicht

Da wir die Leistung des Netzwerks in den letzten Jahren durch neue Protokolle, Verschlüsselungstypen und Verbesserungen der Staukontrolle erhöht haben, werden schnellere Anwendungen wie Video-Streaming möglich. Diese Anwendungen benötigen hohe Bandbreite bei jedem Hop in ihren Client-tunnels.

Teilnehmende router haben jedoch keine Informationen darüber, wie viel Bandbreite ein tunnel verwenden wird, wenn sie eine Tunnel-Build-Nachricht erhalten. Sie können einen tunnel nur basierend auf der aktuell genutzten Gesamtbandbreite aller teilnehmenden tunnel und dem Gesamtbandbreitenlimit für teilnehmende tunnel akzeptieren oder ablehnen.

Anfragende Router haben auch keine Informationen darüber, wie viel Bandbreite an jedem Hop verfügbar ist.

Außerdem haben router derzeit keine Möglichkeit, eingehenden Verkehr in einem tunnel zu begrenzen. Dies wäre sehr nützlich bei Überlastung oder DDoS-Angriffen auf einen Dienst.

Tunnel-Bandbreitenparameter in den Tunnel-Build-Request- und -Reply-Nachrichten fügen Unterstützung für diese Funktionen hinzu. Siehe [Prop168](/proposals/168/) für zusätzliche Hintergrundinformationen. Diese Parameter sind ab API 0.9.65 definiert, aber die Unterstützung kann je nach Implementierung variieren. Sie werden sowohl für lange als auch kurze ECIES Build Records unterstützt.

### Build-Request-Optionen

Die folgenden drei Optionen können im Tunnel-Build-Optionen-Mapping-Feld des Datensatzes gesetzt werden: Ein anfragender Router kann beliebige, alle oder keine davon einschließen.

- m := erforderliche Mindestbandbreite für diesen tunnel (KBps positive Ganzzahl als String)
- r := angeforderte Bandbreite für diesen tunnel (KBps positive Ganzzahl als String)
- l := Bandbreitenlimit für diesen tunnel; nur an IBGW gesendet (KBps positive Ganzzahl als String)

Bedingung: m <= r <= l

Der teilnehmende Router sollte den tunnel ablehnen, wenn "m" angegeben ist und er nicht mindestens diese Bandbreite bereitstellen kann.

Anfrage-Optionen werden an jeden Teilnehmer im entsprechenden verschlüsselten Build-Request-Datensatz gesendet und sind für andere Teilnehmer nicht sichtbar.

### Build Reply Option

Die folgende Option kann im Optionsfeld der tunnel build reply des Datensatzes gesetzt werden, wenn die Antwort ACCEPTED ist:

- b := für diesen tunnel verfügbare Bandbreite (KBps positive Ganzzahl als String)

Einschränkung: b >= m

Der teilnehmende Router sollte dies einschließen, wenn entweder "m" oder "r" in der Build-Anfrage angegeben wurde. Der Wert sollte mindestens dem "m"-Wert entsprechen, falls angegeben, kann aber kleiner oder größer als der "r"-Wert sein, falls angegeben.

Der teilnehmende Router sollte versuchen, mindestens diese Bandbreite für den Tunnel zu reservieren und bereitzustellen, jedoch ist dies nicht garantiert. Router können die Bedingungen 10 Minuten in die Zukunft nicht vorhersagen, und der Durchgangsverkehr hat eine niedrigere Priorität als der eigene Verkehr und die eigenen Tunnel des Routers.

Router können bei Bedarf auch die verfügbare Bandbreite überbuchen, und dies ist wahrscheinlich wünschenswert, da andere Sprungstellen im tunnel diese ablehnen könnten.

Aus diesen Gründen sollte die Antwort des teilnehmenden routers als bestmögliche Zusage behandelt werden, aber nicht als Garantie.

Antwortoptionen werden an den anfragenden Router im entsprechenden verschlüsselten Build-Reply-Record gesendet und sind für andere Teilnehmer nicht sichtbar.

### Implementierungshinweise

Bandbreitenparameter werden wie an den teilnehmenden Routern auf der Tunnel-Ebene gesehen, d.h. die Anzahl der Tunnel-Nachrichten mit fester Größe von 1 KB pro Sekunde. Transport-Overhead (NTCP2 oder SSU2) ist nicht enthalten.

Diese Bandbreite kann viel höher oder niedriger sein als die beim Client sichtbare Bandbreite. Tunnel-Nachrichten enthalten erheblichen Overhead, einschließlich Overhead von höheren Schichten wie ratchet und streaming. Sporadische kleine Nachrichten wie streaming acks werden jeweils auf 1 KB erweitert. Allerdings kann gzip-Komprimierung auf der I2CP-Schicht die Bandbreite erheblich reduzieren.

Die einfachste Implementierung am anfragenden router ist es, die durchschnittlichen, minimalen und/oder maximalen Bandbreiten der aktuellen tunnel im Pool zu verwenden, um die Werte für die Anfrage zu berechnen. Komplexere Algorithmen sind möglich und liegen im Ermessen des Implementierers.

Es gibt derzeit keine I2CP- oder SAM-Optionen definiert, mit denen der Client dem Router mitteilen kann, welche Bandbreite erforderlich ist, und es werden hier auch keine neuen Optionen vorgeschlagen. Optionen können zu einem späteren Zeitpunkt definiert werden, falls erforderlich.

Implementierungen können verfügbare Bandbreite oder andere Daten, Algorithmen, lokale Richtlinien oder lokale Konfigurationen verwenden, um den Bandbreitenwert zu berechnen, der in der Build-Antwort zurückgegeben wird.

## Referenzen

- [Gemeinsame Strukturen](/docs/specs/common-structures/)
- [Kryptographie](/docs/specs/cryptography/)
- [ECIES-ROUTERS](/docs/specs/ecies-routers/)
- [ECIES-X25519](/docs/specs/ecies/)
- [EncryptedLeaseSet](/docs/specs/encryptedleaseset/)
- [I2NP](/docs/specs/i2np/)
- [Multiple-Encryption](https://en.wikipedia.org/wiki/Multiple_encryption)
- [NOISE](https://noiseprotocol.org/noise.html)
- [NTCP2](/docs/specs/ntcp2/)
- [Prop119](/proposals/119/)
- [Prop143](/proposals/143/)
- [Prop152](/proposals/152/)
- [Prop153](/proposals/153/)
- [Prop156](/proposals/156/)
- [Prop157](/proposals/157/)
- [Prop168](/proposals/168/)
- [RFC-7539](https://tools.ietf.org/html/rfc7539)
- [RFC-7748](https://tools.ietf.org/html/rfc7748)
- [Tunnel-Erstellung](/docs/specs/tunnel-creation/)
