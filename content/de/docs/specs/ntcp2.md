---
title: "NTCP2 Transport"
description: "Noise-basierter TCP-Transport für router-zu-router Verbindungen"
slug: "ntcp2"
category: "Transports"
lastUpdated: "2026-07"
accurateFor: "0.9.70"
---

## Übersicht

NTCP2 ist ein authentifiziertes Schlüsselvereinbarungsprotokoll, das die Widerstandsfähigkeit von [NTCP](/docs/transport/ntcp) gegen verschiedene Formen der automatisierten Identifizierung und Angriffe verbessert.

NTCP2 ist für Flexibilität und Koexistenz mit NTCP konzipiert. Es kann auf demselben Port wie NTCP unterstützt werden, oder auf einem anderen Port, oder ganz ohne gleichzeitige NTCP-Unterstützung. Details finden Sie im Abschnitt "Published Router Info" weiter unten.

Wie bei anderen I2P-Transporten ist NTCP2 ausschließlich für die Punkt-zu-Punkt-Übertragung (router-zu-router) von I2NP-Nachrichten definiert. Es ist keine allgemeine Datenleitung.

NTCP2 wird ab Version 0.9.36 unterstützt. Siehe [Prop111](/proposals/111-ntcp-2) für den ursprünglichen Vorschlag, einschließlich Hintergrunddiskussion und zusätzlichen Informationen.

## Noise Protocol Framework

NTCP2 verwendet das Noise Protocol Framework [NOISE](https://noiseprotocol.org/noise.html) (Revision 33, 2017-10-04). Noise hat ähnliche Eigenschaften wie das Station-To-Station-Protokoll [STS](#references), welches die Grundlage für das [SSU](/docs/transport/ssu)-Protokoll ist. In der Noise-Terminologie ist Alice der Initiator und Bob der Responder.

NTCP2 basiert auf dem Noise-Protokoll Noise_XK_25519_ChaChaPoly_SHA256. (Der tatsächliche Bezeichner für die anfängliche Schlüsselableitungsfunktion ist "Noise_XKaesobfse+hs2+hs3_25519_ChaChaPoly_SHA256" um I2P-Erweiterungen zu kennzeichnen - siehe KDF 1 Abschnitt unten) Dieses Noise-Protokoll verwendet die folgenden Primitive:

- Handshake Pattern: XK Alice übermittelt ihren Schlüssel an Bob (X) Alice kennt bereits Bobs statischen Schlüssel (K)
- DH Function: X25519 X25519 DH mit einer Schlüssellänge von 32 Bytes wie in [RFC-7748](https://tools.ietf.org/html/rfc7748) spezifiziert.
- Cipher Function: ChaChaPoly AEAD_CHACHA20_POLY1305 wie in [RFC-7539](https://tools.ietf.org/html/rfc7539) Abschnitt 2.8 spezifiziert. 12-Byte-Nonce, wobei die ersten 4 Bytes auf null gesetzt sind.
- Hash Function: SHA256 Standard 32-Byte-Hash, bereits umfangreich in I2P verwendet.

## Ergänzungen zum Framework

NTCP2 definiert die folgenden Erweiterungen zu Noise_XK_25519_ChaChaPoly_SHA256. Diese folgen im Allgemeinen den Richtlinien in [NOISE](https://noiseprotocol.org/noise.html) Abschnitt 13.

1) Klartext-Ephemeral-Schlüssel werden mit AES-Verschlüsselung unter Verwendung eines bekannten Schlüssels und IV verschleiert. 2) Zufälliges Klartext-Padding wird zu Nachrichten 1 und 2 hinzugefügt. Das Klartext-Padding ist in der Handshake-Hash (MixHash) Berechnung enthalten. Siehe die KDF-Abschnitte unten für Nachricht 2 und Nachricht 3 Teil 1. Zufälliges AEAD-Padding wird zu Nachricht 3 und Datenphase-Nachrichten hinzugefügt. 3) Ein zwei-Byte Frame-Längenfeld wird hinzugefügt, wie es für Noise über TCP erforderlich ist und wie in obfs4. Dies wird nur in den Datenphase-Nachrichten verwendet. Nachricht 1 und 2 AEAD-Frames haben eine feste Länge. Nachricht 3 Teil 1 AEAD-Frame hat eine feste Länge. Die Nachricht 3 Teil 2 AEAD-Frame-Länge wird in Nachricht 1 spezifiziert. 4) Das zwei-Byte Frame-Längenfeld wird mit SipHash-2-4 verschleiert, wie in obfs4. 5) Das Payload-Format wird für Nachrichten 1,2,3 und die Datenphase definiert. Natürlich sind diese nicht im Framework definiert.

## Nachrichten

Alle NTCP2-Nachrichten sind maximal 65537 Bytes lang. Das Nachrichtenformat basiert auf Noise-Nachrichten, mit Modifikationen für Framing und Ununterscheidbarkeit. Implementierungen, die Standard-Noise-Bibliotheken verwenden, müssen möglicherweise empfangene Nachrichten zum/vom Noise-Nachrichtenformat vorverarbeiten. Alle verschlüsselten Felder sind AEAD-Chiffretexte.

Die Verbindungsaufbau-Sequenz ist wie folgt:

```
Alice                           Bob

SessionRequest ------------------->
<------------------- SessionCreated
SessionConfirmed ----------------->
```
Mit der Noise-Terminologie ist die Etablierungs- und Datensequenz wie folgt: (Payload Security Properties von [Noise](https://noiseprotocol.org/noise.html) )

```
XK(s, rs):           Authentication   Confidentiality
  <- s
  ...
  -> e, es                  0                2
  <- e, ee                  2                1
  -> s, se                  2                5
  <-                        2                5
```
Sobald eine Sitzung hergestellt wurde, können Alice und Bob Data-Nachrichten austauschen.

Alle Nachrichtentypen (SessionRequest, SessionCreated, SessionConfirmed, Data und TimeSync) sind in diesem Abschnitt spezifiziert.

Einige Notationen:

    - RH_A = Router Hash for Alice (32 bytes)
    - RH_B = Router Hash for Bob (32 bytes)

### Authentifizierte Verschlüsselung

Es gibt drei separate authentifizierte Verschlüsselungsinstanzen (CipherStates). Eine während der Handshake-Phase und zwei (Senden und Empfangen) für die Datenphase. Jede hat ihren eigenen Schlüssel aus einer KDF.

Verschlüsselte/authentifizierte Daten werden dargestellt als

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|   Encrypted and authenticated data    |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
```
#### ChaCha20/Poly1305

Verschlüsseltes und authentifiziertes Datenformat.

Eingaben für die Verschlüsselungs-/Entschlüsselungsfunktionen:

```
k :: 32 byte cipher key, as generated from KDF

nonce :: Counter-based nonce, 12 bytes.
         Starts at 0 and incremented for each message.
         First four bytes are always zero.
         Last eight bytes are the counter, little-endian encoded.
         Maximum value is 2**64 - 2.
         Connection must be dropped and restarted after
         it reaches that value.
         The value 2**64 - 1 must never be sent.

ad :: In handshake phase:
      Associated data, 32 bytes.
      The SHA256 hash of all preceding data.
      In data phase:
      Zero bytes

data :: Plaintext data, 0 or more bytes
```
Ausgabe der Verschlüsselungsfunktion, Eingabe in die Entschlüsselungsfunktion:

```
+----+----+----+----+----+----+----+----+
|Obfs Len |                             |
+----+----+                             +
|       ChaCha20 encrypted data         |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+              (MAC)                    +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Obfs Len :: Length of (encrypted data + MAC) to follow, 16 - 65535
            Obfuscation using SipHash (see below)
            Not used in message 1 or 2, or message 3 part 1, where the length is fixed
            Not used in message 3 part 1, as the length is specified in message 1

encrypted data :: Same size as plaintext data, 0 - 65519 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
Für ChaCha20 entspricht das hier Beschriebene [RFC-7539](https://tools.ietf.org/html/rfc7539), welches auch ähnlich in TLS [RFC-7905](https://tools.ietf.org/html/rfc7905) verwendet wird.

#### Notizen

- Da ChaCha20 eine Stromchiffre ist, müssen Klartexte nicht gepaddet werden. Zusätzliche Keystream-Bytes werden verworfen.
- Der Schlüssel für die Chiffre (256 Bits) wird mittels der SHA256 KDF vereinbart. Die Details der KDF für jede Nachricht sind in separaten Abschnitten unten aufgeführt.
- ChaChaPoly-Frames für Nachrichten 1, 2 und den ersten Teil von Nachricht 3 haben eine bekannte Größe. Ab dem zweiten Teil von Nachricht 3 haben Frames eine variable Größe. Die Größe von Nachricht 3 Teil 1 wird in Nachricht 1 spezifiziert. Ab der Datenphase werden Frames mit einer zwei-Byte-Länge vorangestellt, die mit SipHash wie in obfs4 verschleiert wird.
- Padding liegt außerhalb des authentifizierten Datenframes für Nachrichten 1 und 2. Das Padding wird in der KDF für die nächste Nachricht verwendet, sodass Manipulationen erkannt werden. Ab Nachricht 3 befindet sich das Padding innerhalb des authentifizierten Datenframes.

#### AEAD-Fehlerbehandlung

- In Nachrichten 1, 2 und Nachricht 3 Teile 1 und 2 ist die AEAD-Nachrichtengröße im Voraus bekannt. Bei einem AEAD-Authentifizierungsfehler muss der Empfänger die weitere Nachrichtenverarbeitung stoppen und die Verbindung ohne Antwort schließen. Dies sollte ein abnormales Schließen sein (TCP RST).
- Für Probing-Resistenz sollte Bob in Nachricht 1 nach einem AEAD-Fehler einen zufälligen Timeout (Bereich TBD) setzen und dann eine zufällige Anzahl von Bytes (Bereich TBD) lesen, bevor er den Socket schließt. Bob sollte eine Blacklist von IPs mit wiederholten Fehlern führen.
- In der Datenphase ist die AEAD-Nachrichtengröße mit SipHash "verschlüsselt" (verschleiert). Es muss darauf geachtet werden, kein Entschlüsselungsorakel zu erstellen. Bei einem AEAD-Authentifizierungsfehler in der Datenphase sollte der Empfänger einen zufälligen Timeout (Bereich TBD) setzen und dann eine zufällige Anzahl von Bytes (Bereich TBD) lesen. Nach dem Lesen oder bei Lese-Timeout sollte der Empfänger eine Payload mit einem Terminierungsblock senden, der einen "AEAD-Fehler"-Grund-Code enthält, und die Verbindung schließen.
- Die gleiche Fehleraktion für einen ungültigen Längenfeldwert in der Datenphase durchführen.

### Schlüsselableitungsfunktion (KDF) (für Handshake-Nachricht 1)

Die KDF generiert einen Handshake-Phasen-Chiffrierschlüssel k aus dem DH-Ergebnis, unter Verwendung von HMAC-SHA256(key, data) wie in [RFC-2104](https://tools.ietf.org/html/rfc2104) definiert. Dies sind die Funktionen InitializeSymmetric(), MixHash() und MixKey(), genau wie in der Noise-Spezifikation definiert.

```
This is the "e" message pattern:

// Define protocol_name.
Set protocol_name = "Noise_XKaesobfse+hs2+hs3_25519_ChaChaPoly_SHA256"
 (48 bytes, US-ASCII encoded, no NULL termination).

// Define Hash h = 32 bytes
h = SHA256(protocol_name);

Define ck = 32 byte chaining key. Copy the h data to ck.
Set ck = h

Define rs = Bob's 32-byte static key as published in the RouterInfo

// MixHash(null prologue)
h = SHA256(h);

// up until here, can all be precalculated by Alice for all outgoing connections

// Alice must validate that Bob's static key is a valid point on the curve here.

// Bob static key
// MixHash(rs)
// || below means append
h = SHA256(h || rs);

// up until here, can all be precalculated by Bob for all incoming connections

This is the "e" message pattern:

Alice generates her ephemeral DH key pair e.

// Alice ephemeral key X
// MixHash(e.pubkey)
// || below means append
h = SHA256(h || e.pubkey);

// h is used as the associated data for the AEAD in message 1
// Retain the Hash h for the message 2 KDF


End of "e" message pattern.

This is the "es" message pattern:

// DH(e, rs) == DH(s, re)
Define input_key_material = 32 byte DH result of Alice's ephemeral key and Bob's static key
Set input_key_material = X25519 DH result

// MixKey(DH())

Define temp_key = 32 bytes
Define HMAC-SHA256(key, data) as in [RFC-2104]_
// Generate a temp key from the chaining key and DH result
// ck is the chaining key, defined above
temp_key = HMAC-SHA256(ck, input_key_material)
// overwrite the DH result in memory, no longer needed
input_key_material = (all zeros)

// Output 1
// Set a new chaining key from the temp key
// byte() below means a single byte
ck =       HMAC-SHA256(temp_key, byte(0x01)).

// Output 2
// Generate the cipher key k
Define k = 32 bytes
// || below means append
// byte() below means a single byte
k =        HMAC-SHA256(temp_key, ck || byte(0x02)).
// overwrite the temp_key in memory, no longer needed
temp_key = (all zeros)

// retain the chaining key ck for message 2 KDF


End of "es" message pattern.
```
### 1) SessionRequest

Alice sendet an Bob.

Noise-Inhalt: Alices ephemerer Schlüssel X Noise-Nutzlast: 16-Byte-Optionsblock Nicht-Noise-Nutzlast: Zufälliges Padding

(Payload-Sicherheitseigenschaften aus [Noise](https://noiseprotocol.org/noise.html) )

```
XK(s, rs):           Authentication   Confidentiality
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
Der X-Wert wird verschlüsselt, um die Ununterscheidbarkeit und Eindeutigkeit der Nutzdaten zu gewährleisten, was notwendige DPI-Gegenmaßnahmen sind. Wir verwenden AES-Verschlüsselung, um dies zu erreichen, anstatt komplexere und langsamere Alternativen wie elligator2. Asymmetrische Verschlüsselung mit Bobs router-öffentlichem Schlüssel wäre viel zu langsam. Die AES-Verschlüsselung verwendet Bobs router-Hash als Schlüssel und Bobs IV, wie er in der netDb veröffentlicht ist.

AES-Verschlüsselung dient nur der DPI-Resistenz. Jede Partei, die Bobs router hash und IV kennt, welche in der Netzwerkdatenbank veröffentlicht sind, kann den X-Wert in dieser Nachricht entschlüsseln.

Das Padding wird nicht von Alice verschlüsselt. Es kann notwendig sein, dass Bob das Padding entschlüsselt, um Timing-Angriffe zu verhindern.

Rohe Inhalte:

```
+----+----+----+----+----+----+----+----+
|                                       |
+        obfuscated with RH_B           +
|       AES-CBC-256 encrypted X         |
+             (32 bytes)                +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|   ChaChaPoly encrypted data           |
+             (16 bytes)                +
|   k defined in KDF for message 1      |
+   n = 0                               +
|   see KDF for associated data         |
+----+----+----+----+----+----+----+----+
|                                       |
+        Poly1305 MAC (16 bytes)        +
|                                       |
+----+----+----+----+----+----+----+----+
|     unencrypted authenticated         |
~         padding (optional)            ~
|     length defined in options block   |
+----+----+----+----+----+----+----+----+

X :: 32 bytes, AES-256-CBC encrypted X25519 ephemeral key, little endian
        key: RH_B
        iv: As published in Bobs network database entry

padding :: Random data, 0 or more bytes.
           Total message length must be 65535 bytes or less.
           Total message length must be 287 bytes or less if
           Bob is publishing his address as NTCP
           (see Version Detection section below).
           Alice and Bob will use the padding data in the KDF for message 2.
           It is authenticated so that any tampering will cause the
           next message to fail.
```
Unverschlüsselte Daten (Poly1305-Authentifizierungs-Tag nicht gezeigt):

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|                   X                   |
+              (32 bytes)               +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|               options                 |
+              (16 bytes)               +
|                                       |
+----+----+----+----+----+----+----+----+
|     unencrypted authenticated         |
+         padding (optional)            +
|     length defined in options block   |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

X :: 32 bytes, X25519 ephemeral key, little endian

options :: options block, 16 bytes, see below

padding :: Random data, 0 or more bytes.
           Total message length must be 65535 bytes or less.
           Total message length must be 287 bytes or less if
           Bob is publishing his address as "NTCP"
           (see Version Detection section below)
           Alice and Bob will use the padding data in the KDF for message 2.
           It is authenticated so that any tampering will cause the
           next message to fail.
```
Options-Block: Hinweis: Alle Felder sind big-endian.

```
+----+----+----+----+----+----+----+----+
| id | ver|  padLen | m3p2len | Rsvd(0) |
+----+----+----+----+----+----+----+----+
|        tsA        |   Reserved (0)    |
+----+----+----+----+----+----+----+----+

id :: 1 byte, the network ID (currently 2, except for test networks)
      As of 0.9.42. See proposal 147.

ver :: 1 byte, protocol version (currently 2)

padLen :: 2 bytes, length of the padding, 0 or more
          See below for max guidelines. Random size from 0 to 64 bytes minimum is recommended.
          (Distribution is implementation-dependent)

m3p2Len :: 2 bytes, length of the the second AEAD frame in SessionConfirmed
           (message 3 part 2) See notes below

Rsvd :: 2 bytes, set to 0 for compatibility with future options

tsA :: 4 bytes, Unix timestamp, unsigned seconds.
       Wraps around in 2106

Reserved :: 4 bytes, set to 0 for compatibility with future options
```
#### Notizen

- Wenn die veröffentlichte Adresse "NTCP" ist, unterstützt Bob sowohl NTCP als auch NTCP2 auf demselben Port. Aus Kompatibilitätsgründen muss Alice beim Initiieren einer Verbindung zu einer als "NTCP" veröffentlichten Adresse die maximale Größe dieser Nachricht, einschließlich Padding, auf 287 Bytes oder weniger begrenzen. Dies ermöglicht Bob die automatische Protokollidentifikation. Wenn als "NTCP2" veröffentlicht, gibt es keine Größenbeschränkung. Siehe die Abschnitte Veröffentlichte Adressen und Versionserkennung unten.

- Der eindeutige X-Wert im initialen AES-Block stellt sicher, dass der Chiffretext für jede Sitzung unterschiedlich ist.

- Bob muss Verbindungen ablehnen, bei denen der Zeitstempelwert zu weit von der aktuellen Zeit abweicht. Nennen wir die maximale Zeitdifferenz "D". Bob muss einen lokalen Cache von zuvor verwendeten Handshake-Werten pflegen und Duplikate ablehnen, um Replay-Angriffe zu verhindern. Werte im Cache müssen eine Lebensdauer von mindestens 2*D haben. Die Cache-Werte sind implementierungsabhängig, jedoch kann der 32-Byte-X-Wert (oder sein verschlüsseltes Äquivalent) verwendet werden.

- Diffie-Hellman-Ephemeralschlüssel dürfen niemals wiederverwendet werden, um kryptografische Angriffe zu verhindern, und eine Wiederverwendung wird als Replay-Angriff abgelehnt.

- Die "KE"- und "auth"-Optionen müssen kompatibel sein, d.h. das gemeinsame Geheimnis K muss die entsprechende Größe haben. Wenn weitere "auth"-Optionen hinzugefügt werden, könnte dies implizit die Bedeutung des "KE"-Flags ändern, um eine andere KDF oder eine andere Verkürzungsgröße zu verwenden.

- Bob muss hier validieren, dass Alices ephemerer Schlüssel ein gültiger Punkt auf der Kurve ist.

- Padding sollte auf eine angemessene Menge begrenzt werden. Bob kann Verbindungen mit übermäßigem Padding ablehnen. Bob wird seine Padding-Optionen in Nachricht 2 angeben. Min/Max-Richtlinien noch zu bestimmen. Zufällige Größe von 0 bis mindestens 31 Bytes? (Verteilung ist implementierungsabhängig) Java-Implementierungen begrenzen Padding derzeit auf maximal 256 Bytes.

- Bei jedem Fehler, einschließlich AEAD, DH, Zeitstempel, offensichtlicher Wiederholung oder Schlüsselvalidierungsfehler, muss Bob die weitere Nachrichtenverarbeitung stoppen und die Verbindung ohne Antwort schließen. Dies sollte ein abnormales Schließen sein (TCP RST). Für Widerstand gegen Probing sollte Bob nach einem AEAD-Fehler ein zufälliges Timeout (Bereich TBD) setzen und dann eine zufällige Anzahl von Bytes (Bereich TBD) lesen, bevor er den Socket schließt.

- Bob kann eine schnelle MSB-Prüfung für einen gültigen Schlüssel (X[31] & 0x80 == 0) durchführen, bevor er eine Entschlüsselung versucht. Falls das höchste Bit gesetzt ist, implementiere Sondierungsresistenz wie bei AEAD-Fehlern.

- DoS-Abwehr: DH ist eine relativ kostenintensive Operation. Wie beim vorherigen NTCP-Protokoll sollten Router alle notwendigen Maßnahmen ergreifen, um CPU- oder Verbindungserschöpfung zu verhindern. Setzen Sie Grenzen für maximale aktive Verbindungen und maximale laufende Verbindungsaufbauten fest. Erzwingen Sie Lesetimeouts (sowohl pro Lesevorgang als auch insgesamt für "slowloris"). Begrenzen Sie wiederholte oder gleichzeitige Verbindungen von derselben Quelle. Führen Sie Blacklists für Quellen, die wiederholt fehlschlagen. Antworten Sie nicht auf AEAD-Fehler.

- Um eine schnelle Versionserkennung und Handshake zu ermöglichen, müssen Implementierungen sicherstellen, dass Alice den gesamten Inhalt der ersten Nachricht puffert und dann auf einmal überträgt, einschließlich des Paddings. Dies erhöht die Wahrscheinlichkeit, dass die Daten in einem einzigen TCP-Paket enthalten sind (es sei denn, sie werden vom Betriebssystem oder Middleboxes segmentiert) und von Bob auf einmal empfangen werden. Zusätzlich müssen Implementierungen sicherstellen, dass Bob den gesamten Inhalt der zweiten Nachricht puffert und dann auf einmal überträgt, einschließlich des Paddings, und dass Bob den gesamten Inhalt der dritten Nachricht puffert und dann auf einmal überträgt. Dies dient auch der Effizienz und um die Wirksamkeit des zufälligen Paddings sicherzustellen.

- "ver"-Feld: Das gesamte Noise-Protokoll, Erweiterungen und NTCP-Protokoll einschließlich Payload-Spezifikationen, das NTCP2 anzeigt. Dieses Feld kann verwendet werden, um die Unterstützung für zukünftige Änderungen anzuzeigen.

- Message 3 Teil 2 Länge: Dies ist die Größe des zweiten AEAD-Frames (einschließlich 16-Byte-MAC), der Alices Router Info und optionale Polsterung enthält, die in der SessionConfirmed-Nachricht gesendet wird. Da Router ihre Router Info regelmäßig regenerieren und erneut veröffentlichen, kann sich die Größe der aktuellen Router Info ändern, bevor Nachricht 3 gesendet wird. Implementierungen müssen eine von zwei Strategien wählen:

a\) die aktuelle Router-Info speichern, die in Nachricht 3 gesendet werden soll, damit die Größe bekannt ist, und optional Platz für Padding hinzufügen;

b\) die angegebene Größe ausreichend erhöhen, um eine mögliche Vergrößerung der Router Info-Größe zu berücksichtigen, und beim tatsächlichen Senden von Nachricht 3 immer Padding hinzufügen. In beiden Fällen muss die in Nachricht 1 enthaltene "m3p2len"-Länge genau der Größe dieses Frames entsprechen, wenn er in Nachricht 3 gesendet wird.

- Bob muss die Verbindung fehlschlagen lassen, wenn nach der Validierung von Nachricht 1 und dem Einlesen des Paddings noch eingehende Daten verbleiben. Es sollten keine zusätzlichen Daten von Alice vorhanden sein, da Bob noch nicht mit Nachricht 2 geantwortet hat.

- Das Netzwerk-ID-Feld wird verwendet, um netzwerkübergreifende Verbindungen schnell zu identifizieren. Wenn dieses Feld nicht null ist und nicht mit Bobs Netzwerk-ID übereinstimmt, sollte Bob die Verbindung trennen und zukünftige Verbindungen blockieren. Alle Verbindungen von Testnetzwerken sollten eine andere ID haben und werden den Test nicht bestehen. Seit Version 0.9.42. Siehe Vorschlag 147 für weitere Informationen.

- Bis API 0.9.68 (Release 2.11.0) implementierte Java I2P ein Maximum von 256 Bytes Padding für Nicht-PQ-Verbindungen, jedoch war dies zuvor nicht dokumentiert.
  Ab API 0.9.69 (Release 2.12.0) implementiert Java I2P das gleiche maximale Padding für Nicht-PQ-Verbindungen
  wie für MLKEM-512. Das maximale Padding beträgt 880 Bytes.

### Schlüsselableitungsfunktion (KDF) (für Handshake-Nachricht 2 und Nachricht 3 Teil 1)

```
// take h saved from message 1 KDF
// MixHash(ciphertext)
h = SHA256(h || 32 byte encrypted payload from message 1)

// MixHash(padding)
// Only if padding length is nonzero
h = SHA256(h || random padding from message 1)

This is the "e" message pattern:

Bob generates his ephemeral DH key pair e.

// h is from KDF for handshake message 1
// Bob ephemeral key Y
// MixHash(e.pubkey)
// || below means append
h = SHA256(h || e.pubkey);

// h is used as the associated data for the AEAD in message 2
// Retain the Hash h for the message 3 KDF

End of "e" message pattern.

This is the "ee" message pattern:

// DH(e, re)
Define input_key_material = 32 byte DH result of Alice's ephemeral key and Bob's ephemeral key
Set input_key_material = X25519 DH result
// overwrite Alice's ephemeral key in memory, no longer needed
// Alice:
e(public and private) = (all zeros)
// Bob:
re = (all zeros)

// MixKey(DH())

Define temp_key = 32 bytes
Define HMAC-SHA256(key, data) as in [RFC-2104]_
// Generate a temp key from the chaining key and DH result
// ck is the chaining key, from the KDF for handshake message 1
temp_key = HMAC-SHA256(ck, input_key_material)
// overwrite the DH result in memory, no longer needed
input_key_material = (all zeros)

// Output 1
// Set a new chaining key from the temp key
// byte() below means a single byte
ck =       HMAC-SHA256(temp_key, byte(0x01)).

// Output 2
// Generate the cipher key k
Define k = 32 bytes
// || below means append
// byte() below means a single byte
k =        HMAC-SHA256(temp_key, ck || byte(0x02)).
// overwrite the temp_key in memory, no longer needed
temp_key = (all zeros)

// retain the chaining key ck for message 3 KDF

End of "ee" message pattern.
```
### 2) SessionCreated

Bob sendet an Alice.

Noise-Inhalt: Bobs ephemerer Schlüssel Y Noise-Nutzlast: 16-Byte-Optionsblock Nicht-Noise-Nutzlast: Zufällige Auffüllung

(Payload-Sicherheitseigenschaften von [Noise](https://noiseprotocol.org/noise.html) )

```
XK(s, rs):           Authentication   Confidentiality
  <- e, ee                  2                1

  Authentication: 2.
  Sender authentication resistant to key-compromise impersonation (KCI).
  The sender authentication is based on an ephemeral-static DH ("es" or "se")
  between the sender's static key pair and the recipient's ephemeral key pair.
  Assuming the corresponding private keys are secure, this authentication cannot be forged.

  Confidentiality: 1.
  Encryption to an ephemeral recipient.
  This payload has forward secrecy, since encryption involves an ephemeral-ephemeral DH ("ee").
  However, the sender has not authenticated the recipient,
  so this payload might be sent to any party, including an active attacker.


  "e": Bob generates a new ephemeral key pair and stores it in the e variable,
  writes the ephemeral public key as cleartext into the message buffer,
  and hashes the public key along with the old h to derive a new h.

  "ee": A DH is performed between the Bob's ephemeral key pair and the Alice's ephemeral key pair.
  The result is hashed along with the old ck to derive a new ck and k, and n is set to zero.
```
Der Y-Wert wird verschlüsselt, um die Ununterscheidbarkeit und Eindeutigkeit der Nutzlast zu gewährleisten, welche notwendige DPI-Gegenmaßnahmen darstellen. Wir verwenden AES-Verschlüsselung, um dies zu erreichen, anstatt komplexerer und langsamerer Alternativen wie elligator2. Asymmetrische Verschlüsselung mit Alices router public key wäre viel zu langsam. Die AES-Verschlüsselung verwendet Bobs router hash als Schlüssel und den AES-Zustand aus Nachricht 1 (der mit Bobs IV initialisiert wurde, wie in der netDb veröffentlicht).

Die AES-Verschlüsselung dient nur der DPI-Resistenz. Jede Partei, die Bobs router hash und IV kennt, welche in der Netzwerkdatenbank veröffentlicht sind, und die ersten 32 Bytes von Nachricht 1 abgefangen hat, kann den Y-Wert in dieser Nachricht entschlüsseln.

Rohe Inhalte:

```
+----+----+----+----+----+----+----+----+
|                                       |
+        obfuscated with RH_B           +
|       AES-CBC-256 encrypted Y         |
+              (32 bytes)               +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|   ChaChaPoly encrypted data (options) |
+   16 bytes                            +
|   k defined in KDF for message 2      |
+   n = 0; see KDF for associated data  +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+        Poly1305 MAC (16 bytes)        +
|                                       |
+----+----+----+----+----+----+----+----+
|     unencrypted authenticated         |
+         padding (optional)            +
|     length defined in options block   |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

Y :: 32 bytes, AES-256-CBC encrypted X25519 ephemeral key, little endian
        key: RH_B
        iv: Using AES state from message 1
```
Unverschlüsselte Daten (Poly1305 Auth-Tag nicht angezeigt):

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|                  Y                    |
+              (32 bytes)               +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|               options                 |
+              (16 bytes)               +
|                                       |
+----+----+----+----+----+----+----+----+
|     unencrypted authenticated         |
+         padding (optional)            +
|     length defined in options block   |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

Y :: 32 bytes, X25519 ephemeral key, little endian

options :: options block, 16 bytes, see below

padding :: Random data, 0 or more bytes.
           Total message length must be 65535 bytes or less.
           Alice and Bob will use the padding data in the KDF for message 3 part 1.
           It is authenticated so that any tampering will cause the
           next message to fail.
```
#### Notizen

- Alice muss hier validieren, dass Bobs ephemeral key ein gültiger Punkt auf der Kurve ist.
- Padding sollte auf ein vernünftiges Maß begrenzt werden. Alice kann Verbindungen mit übermäßigem Padding ablehnen. Alice wird ihre Padding-Optionen in Nachricht 3 spezifizieren. Min/Max-Richtlinien noch zu bestimmen. Zufällige Größe von 0 bis 31 Bytes minimum? (Verteilung ist implementierungsabhängig)
- Bei jedem Fehler, einschließlich AEAD-, DH-, Zeitstempel-, offensichtlicher Replay- oder Schlüsselvalidierungsfehlern, muss Alice die weitere Nachrichtenverarbeitung stoppen und die Verbindung ohne Antwort schließen. Dies sollte ein abnormaler Schluss sein (TCP RST).
- Um einen schnellen Handshake zu ermöglichen, müssen Implementierungen sicherstellen, dass Bob den gesamten Inhalt der ersten Nachricht puffert und dann auf einmal sendet, einschließlich des Paddings. Dies erhöht die Wahrscheinlichkeit, dass die Daten in einem einzigen TCP-Paket enthalten sind (außer bei Segmentierung durch das OS oder Middleboxes) und von Alice auf einmal empfangen werden. Dies dient auch der Effizienz und soll die Wirksamkeit des zufälligen Paddings gewährleisten.
- Alice muss die Verbindung fehlschlagen lassen, wenn nach der Validierung von Nachricht 2 und dem Einlesen des Paddings noch eingehende Daten verbleiben. Es sollten keine zusätzlichen Daten von Bob vorhanden sein, da Alice noch nicht mit Nachricht 3 geantwortet hat.

Options-Block: Hinweis: Alle Felder sind im Big-Endian-Format.

```
+----+----+----+----+----+----+----+----+
| Rsvd(0) | padLen  |   Reserved (0)    |
+----+----+----+----+----+----+----+----+
|        tsB        |   Reserved (0)    |
+----+----+----+----+----+----+----+----+

Reserved :: 10 bytes total, set to 0 for compatibility with future options

padLen :: 2 bytes, big endian, length of the padding, 0 or more
          See below for max guidelines. Random size from 0 to 64 bytes minimum is recommended.
          (Distribution is implementation-dependent)

tsB :: 4 bytes, big endian, Unix timestamp, unsigned seconds.
       Wraps around in 2106
```
#### Hinweise

- Alice muss Verbindungen ablehnen, bei denen der Zeitstempelwert zu weit von der aktuellen Zeit abweicht. Nennen wir das maximale Delta "D". Alice muss einen lokalen Cache von zuvor verwendeten Handshake-Werten führen und Duplikate ablehnen, um Replay-Angriffe zu verhindern. Werte im Cache müssen eine Lebensdauer von mindestens 2*D haben. Die Cache-Werte sind implementierungsabhängig, jedoch kann der 32-Byte-Y-Wert (oder sein verschlüsseltes Äquivalent) verwendet werden.

- Bis API 0.9.68 (Release 2.11.0) implementierte Java I2P maximal 256 Bytes Padding für Nicht-PQ-Verbindungen, dies war jedoch zuvor nicht dokumentiert.
  Ab API 0.9.69 (Release 2.12.0) implementiert Java I2P das gleiche maximale Padding für Nicht-PQ-Verbindungen
  wie für MLKEM-512. Das maximale Padding beträgt 848 Bytes.

#### Probleme

- Min/Max-Padding-Optionen hier einschließen?

### Verschlüsselung für Handshake-Nachricht 3 Teil 1, unter Verwendung von Nachricht 2 KDF)

```
// take h saved from message 2 KDF
// MixHash(ciphertext)
h = SHA256(h || 24 byte encrypted payload from message 2)

// MixHash(padding)
// Only if padding length is nonzero
h = SHA256(h || random padding from message 2)
// h is used as the associated data for the AEAD in message 3 part 1, below

This is the "s" message pattern:

Define s = Alice's static public key, 32 bytes

// EncryptAndHash(s.publickey)
// EncryptWithAd(h, s.publickey)
// AEAD_ChaCha20_Poly1305(key, nonce, associatedData, data)
// k is from handshake message 1
// n is 1
ciphertext = AEAD_ChaCha20_Poly1305(k, n++, h, s.publickey)
// MixHash(ciphertext)
// || below means append
h = SHA256(h || ciphertext);

// h is used as the associated data for the AEAD in message 3 part 2

End of "s" message pattern.
```
### Key Derivation Function (KDF) (für Handshake-Nachricht 3 Teil 2)

```
This is the "se" message pattern:

// DH(s, re) == DH(e, rs)
Define input_key_material = 32 byte DH result of Alice's static key and Bob's ephemeral key
Set input_key_material = X25519 DH result
// overwrite Bob's ephemeral key in memory, no longer needed
// Alice:
re = (all zeros)
// Bob:
e(public and private) = (all zeros)

// MixKey(DH())

Define temp_key = 32 bytes
Define HMAC-SHA256(key, data) as in [RFC-2104]_
// Generate a temp key from the chaining key and DH result
// ck is the chaining key, from the KDF for handshake message 1
temp_key = HMAC-SHA256(ck, input_key_material)
// overwrite the DH result in memory, no longer needed
input_key_material = (all zeros)

// Output 1
// Set a new chaining key from the temp key
// byte() below means a single byte
ck =       HMAC-SHA256(temp_key, byte(0x01)).

// Output 2
// Generate the cipher key k
Define k = 32 bytes
// || below means append
// byte() below means a single byte
k =        HMAC-SHA256(temp_key, ck || byte(0x02)).

// h from message 3 part 1 is used as the associated data for the AEAD in message 3 part 2

// EncryptAndHash(payload)
// EncryptWithAd(h, payload)
// AEAD_ChaCha20_Poly1305(key, nonce, associatedData, data)
// n is 0
ciphertext = AEAD_ChaCha20_Poly1305(k, n++, h, payload)
// MixHash(ciphertext)
// || below means append
h = SHA256(h || ciphertext);

// retain the chaining key ck for the data phase KDF
// retain the hash h for the data phase Additional Symmetric Key (SipHash) KDF

End of "se" message pattern.

// overwrite the temp_key in memory, no longer needed
temp_key = (all zeros)
```
### 3) SessionConfirmed

Alice sendet an Bob.

Noise-Inhalt: Alices statischer Schlüssel Noise-Nutzlast: Alices RouterInfo und zufällige Auffüllung Nicht-Noise-Nutzlast: keine

(Payload-Sicherheitseigenschaften von [Noise](https://noiseprotocol.org/noise.html) )

```
XK(s, rs):           Authentication   Confidentiality
  -> s, se                  2                5

  Authentication: 2.
  Sender authentication resistant to key-compromise impersonation (KCI).  The
  sender authentication is based on an ephemeral-static DH ("es" or "se")
  between the sender's static key pair and the recipient's ephemeral key
  pair.  Assuming the corresponding private keys are secure, this
  authentication cannot be forged.

  Confidentiality: 5.
  Encryption to a known recipient, strong forward secrecy.  This payload is
  encrypted based on an ephemeral-ephemeral DH as well as an ephemeral-static
  DH with the recipient's static key pair.  Assuming the ephemeral private
  keys are secure, and the recipient is not being actively impersonated by an
  attacker that has stolen its static private key, this payload cannot be
  decrypted.

  "s": Alice writes her static public key from the s variable into the
  message buffer, encrypting it, and hashes the output along with the old h
  to derive a new h.

  "se": A DH is performed between the Alice's static key pair and the Bob's
  ephemeral key pair.  The result is hashed along with the old ck to derive a
  new ck and k, and n is set to zero.
```
Dies enthält zwei ChaChaPoly-Frames. Der erste ist Alices verschlüsselter statischer öffentlicher Schlüssel. Der zweite ist die Noise-Payload: Alices verschlüsselte RouterInfo, optionale Optionen und optionales Padding. Sie verwenden unterschiedliche Schlüssel, da die MixKey()-Funktion dazwischen aufgerufen wird.

Roher Inhalt:

```
+----+----+----+----+----+----+----+----+
|                                       |
+   ChaCha20 encrypted data (32 bytes)  +
|   Alice static key S                  |
+     k defined in KDF for message 2    +
|   n = 1 see KDF for associated data   |
+----+----+----+----+----+----+----+----+
|                                       |
+        Poly1305 MAC (16 bytes)        +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+   ChaCha20 encrypted data             +
|     Length specified in message 1     |
+     (including 16 byte MAC to follow) +
|                                       |
+       Alice RouterInfo                +
|       using block format 2            |
+       Alice Options (optional)        +
|       using block format 1            |
+       Arbitrary padding               +
|       using block format 254          |
+                                       +
| k defined in KDF for message 3 part 2 |
+     n = 0                             +
|     see KDF for associated data       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+        Poly1305 MAC (16 bytes)        +
|                                       |
+----+----+----+----+----+----+----+----+

S :: 32 bytes, ChaChaPoly encrypted Alice's X25519 static key, little endian
     inside 48 byte ChaChaPoly frame
```
Unverschlüsselte Daten (Poly1305 Auth-Tags nicht gezeigt):

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|              S                        |
+       Alice static key                +
|          (32 bytes)                   |
+                                       +
|                                       |
+                                       +
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|                                       |
+                                       +
|       Alice RouterInfo block          |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+       Optional Options block          +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+       Optional Padding block          +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

S :: 32 bytes, Alice's X25519 static key, little endian
```
#### Hinweise

- Bob muss die übliche Router Info-Validierung durchführen. Stellen Sie sicher, dass der Signaturtyp unterstützt wird, überprüfen Sie die Signatur, überprüfen Sie, dass der Zeitstempel innerhalb der Grenzen liegt, und führen Sie alle anderen notwendigen Prüfungen durch.

- Bob muss überprüfen, dass Alices statischer Schlüssel, der im ersten Frame empfangen wurde, mit dem statischen Schlüssel in der Router Info übereinstimmt. Bob muss zuerst die Router Info nach einer NTCP- oder NTCP2-Router-Adresse mit einer passenden Versions-(v)-Option durchsuchen. Siehe die Abschnitte "Veröffentlichte Router Info" und "Unveröffentlichte Router Info" weiter unten.

- Wenn Bob eine ältere Version von Alices RouterInfo in seiner netdb hat, überprüfe, dass der statische Schlüssel in den router info in beiden gleich ist, falls vorhanden, und wenn die ältere Version weniger als XXX alt ist (siehe Schlüsselrotationszeit unten)

- Bob muss hier validieren, dass Alices statischer Schlüssel ein gültiger Punkt auf der Kurve ist.

- Optionen sollten enthalten sein, um Padding-Parameter zu spezifizieren.

- Bei jedem Fehler, einschließlich AEAD-, RI-, DH-, Zeitstempel- oder Schlüsselvalidierungsfehlern, muss Bob die weitere Nachrichtenverarbeitung stoppen und die Verbindung ohne Antwort schließen. Dies sollte ein abnormaler Verbindungsabbruch (TCP RST) sein.

- Um einen schnellen Handshake zu ermöglichen, müssen Implementierungen sicherstellen, dass Alice den gesamten Inhalt der dritten Nachricht puffert und dann auf einmal überträgt, einschließlich beider AEAD-Frames. Dies erhöht die Wahrscheinlichkeit, dass die Daten in einem einzigen TCP-Paket enthalten sind (es sei denn, sie werden vom Betriebssystem oder Middleboxes segmentiert) und von Bob auf einmal empfangen werden. Dies dient auch der Effizienz und gewährleistet die Wirksamkeit der zufälligen Polsterung.

- Message 3 Teil 2 Frame-Länge: Die Länge dieses Frames (einschließlich MAC) wird von Alice in Message 1 gesendet. Siehe diese Message für wichtige Hinweise zur ausreichenden Berücksichtigung von Platz für Padding.

- Nachricht 3 Teil 2 Frame-Inhalt: Das Format dieses Frames ist dasselbe wie das Format der Datenphasen-Frames, außer dass die Länge des Frames von Alice in Nachricht 1 gesendet wird. Siehe unten für das Datenphasen-Frame-Format. Der Frame muss 1 bis 3 Blöcke in der folgenden Reihenfolge enthalten:

1)  Alice's Router Info Block (erforderlich)   2)  Options Block (optional)

3\) Padding-Block (optional) Dieser Frame darf niemals einen anderen Block-Typ enthalten.

- Message 3 Teil 2 Padding ist nicht erforderlich, wenn Alice einen Data-Phase-Frame (der optional Padding enthalten kann) an das Ende von Message 3 anhängt und beide auf einmal sendet, da dies für einen Beobachter wie ein großer zusammenhängender Datenstrom aussieht. Da Alice im Allgemeinen, aber nicht immer, eine I2NP-Nachricht an Bob zu senden hat (deshalb hat sie sich mit ihm verbunden), ist dies die empfohlene Implementierung, sowohl aus Effizienzgründen als auch um die Wirksamkeit des zufälligen Paddings zu gewährleisten.

- Die theoretische maximale Gesamtlänge beider AEAD-Frames der Nachricht 3 (Teile 1 und 2) beträgt 65535 Bytes; Teil 1 umfasst 48 Bytes, daher beträgt die maximale Länge für Teil 2 65487 Bytes; die maximale Klartextlänge für Teil 2 ohne MAC beträgt 65471 Bytes.
  WARNUNG: Einige Implementierungen setzen deutlich kleinere Längen voraus. Java I2P begrenzt derzeit die Gesamtlänge auf 4096 Bytes. Fügen Sie keine übermäßige Auffüllung hinzu.

### Schlüsselableitungsfunktion (KDF) (für Datenphase)

Die Datenphase verwendet eine Eingabe für assoziierte Daten mit null Länge.

Die KDF generiert zwei Chiffrierschlüssel k_ab und k_ba aus dem Verkettungsschlüssel ck, wobei HMAC-SHA256(key, data) wie in [RFC-2104](https://tools.ietf.org/html/rfc2104) definiert verwendet wird. Dies ist die Split()-Funktion, genau wie in der Noise-Spezifikation definiert.

```
ck = from handshake phase

// k_ab, k_ba = HKDF(ck, zerolen)
// ask_master = HKDF(ck, zerolen, info="ask")

// zerolen is a zero-length byte array
temp_key = HMAC-SHA256(ck, zerolen)
// overwrite the chaining key in memory, no longer needed
ck = (all zeros)

// Output 1
// cipher key, for Alice transmits to Bob (Noise doesn't make clear which is which, but Java code does)
k_ab =   HMAC-SHA256(temp_key, byte(0x01)).

// Output 2
// cipher key, for Bob transmits to Alice (Noise doesn't make clear which is which, but Java code does)
k_ba =   HMAC-SHA256(temp_key, k_ab || byte(0x02)).


KDF for SipHash for length field:
Generate an Additional Symmetric Key (ask) for SipHash
SipHash uses two 8-byte keys (big endian) and 8 byte IV for first data.

// "ask" is 3 bytes, US-ASCII, no null termination
ask_master = HMAC-SHA256(temp_key, "ask" || byte(0x01))
// sip_master = HKDF(ask_master, h || "siphash")
// "siphash" is 7 bytes, US-ASCII, no null termination
// overwrite previous temp_key in memory
// h is from KDF for message 3 part 2
temp_key = HMAC-SHA256(ask_master, h || "siphash")
// overwrite ask_master in memory, no longer needed
ask_master = (all zeros)
sip_master = HMAC-SHA256(temp_key, byte(0x01))

Alice to Bob SipHash k1, k2, IV:
// sipkeys_ab, sipkeys_ba = HKDF(sip_master, zerolen)
// overwrite previous temp_key in memory
temp_key = HMAC-SHA256(sip_master, zerolen)
// overwrite sip_master in memory, no longer needed
sip_master = (all zeros)

sipkeys_ab = HMAC-SHA256(temp_key, byte(0x01)).
sipk1_ab = sipkeys_ab[0:7], little endian
sipk2_ab = sipkeys_ab[8:15], little endian
sipiv_ab = sipkeys_ab[16:23]

Bob to Alice SipHash k1, k2, IV:

sipkeys_ba = HMAC-SHA256(temp_key, sipkeys_ab || byte(0x02)).
sipk1_ba = sipkeys_ba[0:7], little endian
sipk2_ba = sipkeys_ba[8:15], little endian
sipiv_ba = sipkeys_ba[16:23]

// overwrite the temp_key in memory, no longer needed
temp_key = (all zeros)
```
### 4) Datenphase

Noise-Nutzlast: Wie unten definiert, einschließlich zufälliger Auffüllung Nicht-Noise-Nutzlast: keine

Ab dem 2. Teil der Nachricht 3 befinden sich alle Nachrichten innerhalb eines authentifizierten und verschlüsselten ChaChaPoly-"Rahmens" mit einer vorangestellten zweistelligen verschleierten Längenangabe. Alle Auffülldaten befinden sich innerhalb des Rahmens. Innerhalb des Rahmens befindet sich ein Standardformat mit null oder mehreren "Blöcken". Jeder Block hat einen Ein-Byte-Typ und eine Zwei-Byte-Länge. Typen umfassen Datum/Uhrzeit, I2NP-Nachricht, Optionen, Beendigung und Auffüllung.

Hinweis: Bob kann, ist aber nicht verpflichtet, seine RouterInfo als erste Nachricht an Alice in der Datenphase zu senden.

(Payload-Sicherheitseigenschaften von [Noise](https://noiseprotocol.org/noise.html) )

```
XK(s, rs):           Authentication   Confidentiality
  <-                        2                5
  ->                        2                5

  Authentication: 2.
  Sender authentication resistant to key-compromise impersonation (KCI).
  The sender authentication is based on an ephemeral-static DH ("es" or "se")
  between the sender's static key pair and the recipient's ephemeral key pair.
  Assuming the corresponding private keys are secure, this authentication cannot be forged.

  Confidentiality: 5.
  Encryption to a known recipient, strong forward secrecy.
  This payload is encrypted based on an ephemeral-ephemeral DH as well as
  an ephemeral-static DH with the recipient's static key pair.
  Assuming the ephemeral private keys are secure, and the recipient is not being actively impersonated
  by an attacker that has stolen its static private key, this payload cannot be decrypted.
```
#### Hinweise

- Für Effizienz und um die Identifizierung des Längenfelds zu minimieren, müssen Implementierungen sicherstellen, dass der Sender den gesamten Inhalt von Datennachrichten auf einmal puffert und dann überträgt, einschließlich des Längenfelds und des AEAD-Frames. Dies erhöht die Wahrscheinlichkeit, dass die Daten in einem einzigen TCP-Paket enthalten sind (es sei denn, sie werden vom Betriebssystem oder Middleboxen segmentiert) und von der anderen Partei auf einmal empfangen werden. Dies dient ebenfalls der Effizienz und stellt die Wirksamkeit der zufälligen Auffüllung sicher.
- Der router kann wählen, die Sitzung bei einem AEAD-Fehler zu beenden oder kann weiterhin Kommunikationsversuche unternehmen. Falls fortgesetzt wird, sollte der router nach wiederholten Fehlern beenden.

#### SipHash verschleierte Länge

Referenz: [SipHash](https://www.131002.net/siphash/)

Sobald beide Seiten den Handshake abgeschlossen haben, übertragen sie Nutzdaten, die dann in ChaChaPoly-"Frames" verschlüsselt und authentifiziert werden.

Jedem Frame geht eine zweibyte Längenangabe in Big-Endian-Format voraus. Diese Länge gibt die Anzahl der verschlüsselten Frame-Bytes an, die folgen, einschließlich des MAC. Um die Übertragung identifizierbarer Längenfelder im Stream zu vermeiden, wird die Frame-Länge durch XOR-Verknüpfung mit einer aus SipHash abgeleiteten Maske verschleiert, wie sie aus der Datenphase-KDF initialisiert wurde. Beachten Sie, dass die beiden Richtungen eindeutige SipHash-Schlüssel und IVs aus der KDF haben.

```
    sipk1, sipk2 = The SipHash keys from the KDF.  (two 8-byte long integers)
    IV[0] = sipiv = The SipHash IV from the KDF. (8 bytes)
    length is big endian.
    For each frame:
      IV[n] = SipHash-2-4(sipk1, sipk2, IV[n-1])
      Mask[n] = First 2 bytes of IV[n]
      obfuscatedLength = length ^ Mask[n]

    The first length output will be XORed with with IV[1].
```
Der Empfänger verfügt über die identischen SipHash-Schlüssel und IV. Die Dekodierung der Länge erfolgt durch Ableitung der Maske, die zur Verschleierung der Länge verwendet wird, und XOR-Verknüpfung des verkürzten Digest, um die Länge des Frames zu erhalten. Die Frame-Länge ist die Gesamtlänge des verschlüsselten Frames einschließlich des MAC.

#### Hinweise

- Wenn Sie eine SipHash-Bibliotheksfunktion verwenden, die eine vorzeichenlose lange Ganzzahl zurückgibt, verwenden Sie die beiden niedrigstwertigen Bytes als Maske. Konvertieren Sie die lange Ganzzahl als Little Endian zum nächsten IV.

#### Roher Inhalt

```
+----+----+----+----+----+----+----+----+
|obf size |                             |
+----+----+                             +
|                                       |
+   ChaChaPoly frame                    +
|   Encrypted and authenticated         |
+   key is k_ab for Alice to Bob        +
|   key is k_ba for Bob to Alice        |
+   as defined in KDF for data phase    +
|   n starts at 0 and increments        |
+   for each frame in that direction    +
|   no associated data                  |
+   16 bytes minimum                    +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

obf size :: 2 bytes length obfuscated with SipHash
            when de-obfuscated: 16 - 65535

Minimum size including length field is 18 bytes.
Maximum size including length field is 65537 bytes.
Obfuscated length is 2 bytes.
Maximum ChaChaPoly frame is 65535 bytes.
```
#### Notizen

- Da der Empfänger den gesamten Frame erhalten muss, um den MAC zu überprüfen, wird empfohlen, dass der Sender Frames auf wenige KB begrenzt, anstatt die Frame-Größe zu maximieren. Dies minimiert die Latenz beim Empfänger.

#### Unverschlüsselte Daten

Es gibt null oder mehr Blöcke im verschlüsselten Frame. Jeder Block enthält eine Ein-Byte-Kennung, eine Zwei-Byte-Länge und null oder mehr Bytes an Daten.

Für die Erweiterbarkeit müssen Empfänger Blöcke mit unbekannten Kennungen ignorieren und sie als Padding behandeln.

Verschlüsselte Daten haben eine maximale Größe von 65535 Bytes, einschließlich eines 16-Byte-Authentifizierungsheaders, daher beträgt die maximale Größe unverschlüsselter Daten 65519 Bytes.

(Poly1305-Authentifizierungs-Tag nicht angezeigt):

```
+----+----+----+----+----+----+----+----+
|blk |  size   |       data             |
+----+----+----+                        +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
|blk |  size   |       data             |
+----+----+----+                        +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
~               .   .   .               ~

blk :: 1 byte
       0 for datetime
       1 for options
       2 for RouterInfo
       3 for I2NP message
       4 for termination
       224-253 reserved for experimental features
       254 for padding
       255 reserved for future extension
size :: 2 bytes, big endian, size of data to follow, 0 - 65516
data :: the data

Maximum ChaChaPoly frame is 65535 bytes.
Poly1305 tag is 16 bytes
Maximum total block size is 65519 bytes
Maximum single block size is 65519 bytes
Block type is 1 byte
Block length is 2 bytes
Maximum single block data size is 65516 bytes.
```
#### Regeln für die Blockreihenfolge

In der Handshake-Nachricht 3 Teil 2 muss die Reihenfolge sein: RouterInfo, gefolgt von Options falls vorhanden, gefolgt von Padding falls vorhanden. Keine anderen Blöcke sind erlaubt.

In der Datenphase ist die Reihenfolge nicht spezifiziert, außer für die folgenden Anforderungen: Padding, falls vorhanden, muss der letzte Block sein. Termination, falls vorhanden, muss der letzte Block außer Padding sein.

Es können mehrere I2NP-Blöcke in einem einzigen Frame vorhanden sein. Mehrere Padding-Blöcke sind in einem einzigen Frame nicht erlaubt. Andere Blocktypen werden wahrscheinlich nicht mehrere Blöcke in einem einzigen Frame haben, aber es ist nicht verboten.

#### DatumZeit

Sonderfall für Zeitsynchronisation:

```
+----+----+----+----+----+----+----+
| 0  |    4    |     timestamp     |
+----+----+----+----+----+----+----+

blk :: 0
size :: 2 bytes, big endian, value = 4
timestamp :: Unix timestamp, unsigned seconds.
             Wraps around in 2106
```
HINWEIS: Implementierungen müssen auf die nächste Sekunde runden, um Uhrzeitabweichungen im Netzwerk zu verhindern.

#### Optionen

Aktualisierte Optionen übergeben. Optionen umfassen: Minimale und maximale Polsterung.

Der Options-Block wird eine variable Länge haben.

```
+----+----+----+----+----+----+----+----+
| 1  |  size   |tmin|tmax|rmin|rmax|tdmy|
+----+----+----+----+----+----+----+----+
|tdmy|  rdmy   |  tdelay |  rdelay |    |
~----+----+----+----+----+----+----+    ~
|              more_options             |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 1
size :: 2 bytes, big endian, size of options to follow, 12 bytes minimum

tmin, tmax, rmin, rmax :: requested padding limits
    tmin and rmin are for desired resistance to traffic analysis.
    tmax and rmax are for bandwidth limits.
    tmin and tmax are the transmit limits for the router sending this options block.
    rmin and rmax are the receive limits for the router sending this options block.
    Each is a 4.4 fixed-point float representing 0 to 15.9375
    (or think of it as an unsigned 8-bit integer divided by 16.0).
    This is the ratio of padding to data. Examples:
    Value of 0x00 means no padding
    Value of 0x01 means add 6 percent padding
    Value of 0x10 means add 100 percent padding
    Value of 0x80 means add 800 percent (8x) padding
    Alice and Bob will negotiate the minimum and maximum in each direction.
    These are guidelines, there is no enforcement.
    Sender should honor receiver's maximum.
    Sender may or may not honor receiver's minimum, within bandwidth constraints.

tdmy: Max dummy traffic willing to send, 2 bytes big endian, bytes/sec average
rdmy: Requested dummy traffic, 2 bytes big endian, bytes/sec average
tdelay: Max intra-message delay willing to insert, 2 bytes big endian, msec average
rdelay: Requested intra-message delay, 2 bytes big endian, msec average

Padding distribution specified as additional parameters?
Random delay specified as additional parameters?

more_options :: Format TBD
```
#### Optionsprobleme

- Das Optionsformat ist noch zu bestimmen.
- Die Optionsverhandlung ist noch zu bestimmen.

#### RouterInfo

Übergebe Alice's RouterInfo an Bob. Wird in Handshake-Nachricht 3 Teil 2 verwendet. Übergebe Alice's RouterInfo an Bob oder Bob's an Alice. Wird optional in der Datenphase verwendet.

```
+----+----+----+----+----+----+----+----+
| 2  |  size   |flg |    RouterInfo     |
+----+----+----+----+                   +
| (Alice RI in handshake msg 3 part 2)  |
~ (Alice, Bob, or third-party           ~
|  RI in data phase)                    |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 2
size :: 2 bytes, big endian, size of flag + router info to follow
flg :: 1 byte flags
       bit order: 76543210
       bit 0: 0 for local store, 1 for flood request
       bits 7-1: Unused, set to 0 for future compatibility
routerinfo :: Alice's or Bob's RouterInfo
```
#### Notizen

- Wenn in der Datenphase verwendet, soll der Empfänger (Alice oder Bob) validieren, dass es derselbe Router Hash ist wie ursprünglich gesendet (für Alice) oder gesendet an (für Bob). Dann als lokale I2NP DatabaseStore Message behandeln. Signatur validieren, neueren Zeitstempel validieren und in der lokalen netDb speichern. Wenn das Flag-Bit 0 gleich 1 ist und die empfangende Partei floodfill ist, als DatabaseStore Message mit einem Token ungleich null behandeln und an die nächsten floodfills weiterleiten.
- Die Router Info ist NICHT mit gzip komprimiert (im Gegensatz zu einer DatabaseStore Message, wo sie es ist)
- Flooding darf nur angefordert werden, wenn veröffentlichte RouterAddresses in der RouterInfo vorhanden sind. Der empfangende Router darf die RouterInfo nur dann weiterleiten, wenn veröffentlichte RouterAddresses darin enthalten sind.
- Implementierer müssen sicherstellen, dass beim Lesen eines Blocks fehlerhafte oder bösartige Daten nicht dazu führen, dass Lesevorgänge in den nächsten Block überlaufen.
- Dieses Protokoll bietet keine Bestätigung, dass die RouterInfo empfangen, gespeichert oder weitergeleitet wurde (weder in der Handshake- noch in der Datenphase). Wenn eine Bestätigung gewünscht wird und der Empfänger floodfill ist, sollte der Sender stattdessen eine Standard-I2NP DatabaseStoreMessage mit einem Reply-Token senden.

#### Probleme

- Könnte auch in der Datenphase verwendet werden, anstelle einer I2NP DatabaseStoreMessage. Zum Beispiel könnte Bob es verwenden, um die Datenphase zu starten.
- Ist es erlaubt, dass dies die RI für andere router als den Urheber enthält, als allgemeiner Ersatz für DatabaseStoreMessages, z.B. für das Flooding durch floodfills?

#### I2NP Message

Eine einzelne I2NP-Nachricht mit einem modifizierten Header. I2NP-Nachrichten dürfen nicht über Blöcke oder über ChaChaPoly-Frames fragmentiert werden.

Dies verwendet die ersten 9 Bytes aus dem Standard-NTCP I2NP-Header und entfernt die letzten 7 Bytes des Headers wie folgt: verkürzt die Gültigkeitsdauer von 8 auf 4 Bytes (Sekunden statt Millisekunden, genau wie bei SSU), entfernt die 2-Byte-Längenangabe (verwendet die Blockgröße - 9) und entfernt die Ein-Byte-SHA256-Prüfsumme.

```
+----+----+----+----+----+----+----+----+
| 3  |  size   |type|    msg id         |
+----+----+----+----+----+----+----+----+
|   short exp       |     message       |
+----+----+----+----+                   +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 3
size :: 2 bytes, big endian, size of type + msg id + exp + message to follow
        I2NP message body size is (size - 9).
type :: 1 byte, I2NP msg type, see I2NP spec
msg id :: 4 bytes, big endian, I2NP message ID
short exp :: 4 bytes, big endian, I2NP message expiration, Unix timestamp, unsigned seconds.
             Wraps around in 2106
message :: I2NP message body
```
#### Hinweise

- Implementierer müssen sicherstellen, dass beim Lesen eines Blocks fehlerhafte oder bösartige Daten nicht dazu führen, dass Lesevorgänge in den nächsten Block überlaufen.

#### Beendigung

Noise empfiehlt eine explizite Beendigungsnachricht. Das ursprüngliche NTCP hat keine. Verbindung trennen. Dies muss der letzte Nicht-Padding-Block im Frame sein.

```
+----+----+----+----+----+----+----+----+
| 4  |  size   |    valid data frames   |
+----+----+----+----+----+----+----+----+
    received   | rsn|     addl data     |
+----+----+----+----+                   +
~               .   .   .               ~
+----+----+----+----+----+----+----+----+

blk :: 4
size :: 2 bytes, big endian, value = 9 or more
valid data frames received :: The number of valid AEAD data phase frames received
                              (current receive nonce value)
                              0 if error occurs in handshake phase
                              8 bytes, big endian
rsn :: reason, 1 byte:
       0: normal close or unspecified
       1: termination received
       2: idle timeout
       3: router shutdown
       4: data phase AEAD failure
       5: incompatible options
       6: incompatible signature type
       7: clock skew
       8: padding violation
       9: AEAD framing error
       10: payload format error
       11: message 1 error
       12: message 2 error
       13: message 3 error
       14: intra-frame read timeout
       15: RI signature verification fail
       16: s parameter missing, invalid, or mismatched in RouterInfo
       17: banned
addl data :: optional, 0 or more bytes, for future expansion, debugging,
             or reason text.
             Format unspecified and may vary based on reason code.
```
#### Anmerkungen

Nicht alle Gründe werden möglicherweise tatsächlich verwendet, dies ist implementierungsabhängig. Handshake-Fehler führen im Allgemeinen zu einem Schließen mit TCP RST stattdessen. Siehe Hinweise in den Handshake-Nachrichtensektionen oben. Zusätzliche aufgeführte Gründe dienen der Konsistenz, Protokollierung, Fehlerbehebung oder falls sich die Richtlinien ändern.

#### Padding

Dies ist für das Padding innerhalb von AEAD-Frames. Padding für Nachrichten 1 und 2 befinden sich außerhalb der AEAD-Frames. Sämtliches Padding für Nachricht 3 und die Datenphase befinden sich innerhalb der AEAD-Frames.

Padding innerhalb von AEAD sollte ungefähr den ausgehandelten Parametern entsprechen. Bob hat seine angeforderten tx/rx min/max Parameter in Nachricht 2 gesendet. Alice hat ihre angeforderten tx/rx min/max Parameter in Nachricht 3 gesendet. Aktualisierte Optionen können während der Datenphase gesendet werden. Siehe Optionsblock-Informationen oben.

Falls vorhanden, muss dies der letzte Block im Frame sein.

```
+----+----+----+----+----+----+----+----+
|254 |  size   |      padding           |
+----+----+----+                        +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 254
size :: 2 bytes, big endian, size of padding to follow
padding :: random data
```
#### Notizen

- Größe = 0 ist erlaubt.
- Padding-Strategien noch zu bestimmen.
- Minimales Padding noch zu bestimmen.
- Frames die nur aus Padding bestehen sind erlaubt.
- Padding-Standards noch zu bestimmen.
- Siehe Optionsblock für Padding-Parameter-Verhandlung
- Siehe Optionsblock für Min/Max-Padding-Parameter
- Noise begrenzt Nachrichten auf 64KB. Wenn mehr Padding notwendig ist, sende mehrere Frames.
- Router-Antwort bei Verletzung des ausgehandelten Paddings ist implementierungsabhängig.

#### Andere Blocktypen

Implementierungen sollten unbekannte Blocktypen für Vorwärtskompatibilität ignorieren, außer in Nachricht 3 Teil 2, wo unbekannte Blöcke nicht erlaubt sind.

#### Zukünftige Arbeiten

- Die Padding-Länge sollte entweder nachrichtenbasiert unter Berücksichtigung von Schätzungen der Längenverteilung bestimmt werden, oder es sollten zufällige Verzögerungen hinzugefügt werden. Diese Gegenmaßnahmen sind zu implementieren, um DPI zu widerstehen, da die Nachrichtengrößen andernfalls verraten würden, dass I2P-Verkehr über das Transportprotokoll übertragen wird. Das genaue Padding-Schema ist ein Bereich zukünftiger Arbeit.

### 5) Beendigung

Verbindungen können durch normales oder abnormales Schließen des TCP-Sockets beendet werden, oder, wie Noise empfiehlt, durch eine explizite Beendigungsnachricht. Die explizite Beendigungsnachricht ist in der oben beschriebenen Datenphase definiert.

Bei jeder normalen oder abnormalen Beendigung sollten router alle im Speicher befindlichen temporären Daten auf null setzen, einschließlich temporärer Handshake-Schlüssel, symmetrischer Kryptoschlüssel und zugehöriger Informationen.

## Veröffentlichte Router-Informationen

### Funktionen

Ab Release 0.9.50 wird die "caps"-Option in NTCP2-Adressen unterstützt, ähnlich wie bei SSU. Eine oder mehrere Fähigkeiten können in der "caps"-Option veröffentlicht werden. Fähigkeiten können in beliebiger Reihenfolge stehen, aber "46" ist die empfohlene Reihenfolge, um Konsistenz zwischen den Implementierungen zu gewährleisten. Es sind zwei Fähigkeiten definiert:

4: Zeigt ausgehende IPv4-Fähigkeit an. Wenn eine IP im Host-Feld veröffentlicht ist, ist diese Fähigkeit nicht erforderlich. Wenn der router versteckt ist oder NTCP2 nur ausgehend ist, können '4' und '6' in einer einzigen Adresse kombiniert werden.

6: Zeigt ausgehende IPv6-Fähigkeit an. Wenn eine IP im Host-Feld veröffentlicht wird, ist diese Fähigkeit nicht erforderlich. Wenn der router versteckt ist oder NTCP2 nur ausgehend ist, können '4' und '6' in einer einzigen Adresse kombiniert werden.

### Veröffentlichte Adressen

Die veröffentlichte RouterAddress (Teil der RouterInfo) wird eine Protokoll-Kennung von entweder "NTCP" oder "NTCP2" haben.

Die RouterAddress muss "host"- und "port"-Optionen enthalten, wie im aktuellen NTCP-Protokoll.

Die RouterAddress muss drei Optionen enthalten, um NTCP2-Unterstützung anzuzeigen:

- s=(Base64-Schlüssel) Der aktuelle statische öffentliche Noise-Schlüssel (s) für diese RouterAddress. Base64-kodiert unter Verwendung des Standard-I2P-Base64-Alphabets. 32 Bytes binär, 44 Bytes als Base64-kodiert, Little-Endian X25519 öffentlicher Schlüssel.
- i=(Base64-IV) Der aktuelle IV zum Verschlüsseln des X-Wertes in Nachricht 1 für diese RouterAddress. Base64-kodiert unter Verwendung des Standard-I2P-Base64-Alphabets. 16 Bytes binär, 24 Bytes als Base64-kodiert, Big-Endian.
- v=2 Die aktuelle Version (2). Wenn als "NTCP" veröffentlicht, ist zusätzliche Unterstützung für Version 1 impliziert. Unterstützung für zukünftige Versionen erfolgt mit kommagetrennten Werten, z.B. v=2,3. Die Implementierung sollte die Kompatibilität überprüfen, einschließlich mehrerer Versionen, falls ein Komma vorhanden ist. Kommagetrennte Versionen müssen in numerischer Reihenfolge stehen.

Alice muss überprüfen, dass alle drei Optionen vorhanden und gültig sind, bevor sie sich über das NTCP2-Protokoll verbindet.

Wenn als "NTCP" mit den Optionen "s", "i" und "v" veröffentlicht, muss der router eingehende Verbindungen auf diesem Host und Port für sowohl NTCP- als auch NTCP2-Protokolle akzeptieren und die Protokollversion automatisch erkennen.

Wenn als "NTCP2" mit den Optionen "s", "i" und "v" veröffentlicht, akzeptiert der router eingehende Verbindungen auf diesem Host und Port nur für das NTCP2-Protokoll.

Wenn ein router sowohl NTCP1- als auch NTCP2-Verbindungen unterstützt, aber keine automatische Versionserkennung für eingehende Verbindungen implementiert, muss er sowohl "NTCP"- als auch "NTCP2"-Adressen bekanntgeben und die NTCP2-Optionen nur in der "NTCP2"-Adresse einschließen. Der router sollte einen niedrigeren Kostenwert (höhere Priorität) in der "NTCP2"-Adresse als in der "NTCP"-Adresse setzen, damit NTCP2 bevorzugt wird.

Wenn mehrere NTCP2 RouterAddresses (entweder als "NTCP" oder "NTCP2") in derselben RouterInfo veröffentlicht werden (für zusätzliche IP-Adressen oder Ports), müssen alle Adressen, die denselben Port angeben, identische NTCP2-Optionen und -Werte enthalten. Insbesondere müssen alle denselben statischen Schlüssel und iv enthalten.

### Unveröffentlichte NTCP2-Adresse

Wenn Alice ihre NTCP2-Adresse nicht für eingehende Verbindungen veröffentlicht (als "NTCP" oder "NTCP2"), muss sie eine "NTCP2" router-Adresse veröffentlichen, die nur ihren statischen Schlüssel und die NTCP2-Version enthält, damit Bob den Schlüssel validieren kann, nachdem er Alices RouterInfo in Nachricht 3 Teil 2 erhalten hat.

- s=(Base64 key) Wie oben für veröffentlichte Adressen definiert.
- v=2 Wie oben für veröffentlichte Adressen definiert.

Diese Router-Adresse wird keine "i"-, "host"- oder "port"-Optionen enthalten, da diese für ausgehende NTCP2-Verbindungen nicht erforderlich sind. Die veröffentlichten Kosten für diese Adresse sind nicht von entscheidender Bedeutung, da sie nur für eingehende Verbindungen verwendet wird; es kann jedoch für andere Router hilfreich sein, wenn die Kosten höher (niedrigere Priorität) als bei anderen Adressen gesetzt werden. Der empfohlene Wert ist 14.

Alice kann auch einfach die Optionen "s" und "v" zu einer bestehenden veröffentlichten "NTCP"-Adresse hinzufügen.

### Public Key und IV-Rotation

Aufgrund der Zwischenspeicherung von RouterInfos dürfen Router den statischen öffentlichen Schlüssel oder IV nicht rotieren, während der Router läuft, unabhängig davon, ob er in einer veröffentlichten Adresse steht oder nicht. Router müssen diesen Schlüssel und IV dauerhaft speichern, um sie nach einem sofortigen Neustart wiederzuverwenden, damit eingehende Verbindungen weiterhin funktionieren und Neustartzeiten nicht preisgegeben werden. Router müssen die Zeit des letzten Herunterfahrens dauerhaft speichern oder anderweitig bestimmen, damit die vorherige Ausfallzeit beim Start berechnet werden kann.

Aufgrund von Bedenken bezüglich der Preisgabe von Neustartzeiten können router diesen Schlüssel oder IV beim Start rotieren, wenn der router zuvor für einige Zeit heruntergefahren war (mindestens ein paar Stunden).

Wenn der router veröffentlichte NTCP2 RouterAddresses hat (als NTCP oder NTCP2), sollte die minimale Ausfallzeit vor der Rotation viel länger sein, zum Beispiel einen Monat, es sei denn, die lokale IP-Adresse hat sich geändert oder der router führt ein "rekeys" durch.

Wenn der router veröffentlichte SSU RouterAddresses hat, aber kein NTCP2 (weder als NTCP noch als NTCP2), sollte die minimale Ausfallzeit vor der Rotation länger sein, zum Beispiel einen Tag, es sei denn, die lokale IP-Adresse hat sich geändert oder der router führt ein "rekeys" durch. Dies gilt auch dann, wenn die veröffentlichte SSU-Adresse introducers hat.

Wenn der router keine veröffentlichten RouterAddresses (NTCP, NTCP2 oder SSU) hat, kann die minimale Ausfallzeit vor der Rotation so kurz wie zwei Stunden sein, auch wenn sich die IP-Adresse ändert, es sei denn, der router führt ein "rekeys" durch.

Wenn der router auf einen anderen Router Hash "rekeys", sollte er auch einen neuen noise key und IV generieren.

Implementierungen müssen sich bewusst sein, dass eine Änderung des statischen öffentlichen Schlüssels oder IV eingehende NTCP2-Verbindungen von routern verhindert, die eine ältere RouterInfo zwischengespeichert haben. RouterInfo-Veröffentlichung, tunnel-Peer-Auswahl (einschließlich sowohl OBGW als auch IB nächster Hop), Zero-Hop-tunnel-Auswahl, Transport-Auswahl und andere Implementierungsstrategien müssen dies berücksichtigen.

Die IV-Rotation unterliegt denselben Regeln wie die Schlüsselrotation, außer dass IVs nur in veröffentlichten RouterAddresses vorhanden sind, sodass es keine IV für versteckte oder durch Firewalls geschützte Router gibt. Wenn sich etwas ändert (Version, Schlüssel, Optionen?), wird empfohlen, dass sich auch die IV ändert.

Hinweis: Die minimale Ausfallzeit vor dem Rekeying kann angepasst werden, um die Netzwerkgesundheit zu gewährleisten und zu verhindern, dass ein router, der für eine moderate Zeit ausgefallen ist, ein Reseeding durchführt.

## Versionserkennung

Wenn als "NTCP" veröffentlicht, muss der router automatisch die Protokollversion für eingehende Verbindungen erkennen.

Diese Erkennung ist implementierungsabhängig, aber hier ist eine allgemeine Anleitung.

Um die Version einer eingehenden NTCP-Verbindung zu erkennen, geht Bob wie folgt vor:

- Warten auf mindestens 64 Bytes (minimale NTCP2 Nachricht 1 Größe)

- Wenn die initial empfangenen Daten 288 oder mehr Bytes betragen, ist die eingehende Verbindung Version 1.

- Falls weniger als 288 Bytes, entweder

> - Warte eine kurze Zeit auf weitere Daten (gute Strategie vor der weitverbreiteten NTCP2-Einführung), wenn mindestens 288 insgesamt empfangen wurden, ist es NTCP 1.   >   > - Versuche die ersten Stufen der Dekodierung als Version 2, wenn es fehlschlägt, warte eine kurze Zeit auf weitere Daten (gute Strategie nach der weitverbreiteten NTCP2-Einführung)   >   >   > - Entschlüssele die ersten 32 Bytes (der X-Schlüssel) des SessionRequest-Pakets mit AES-256 mit Schlüssel RH_B.   >   > - Überprüfe einen gültigen Punkt auf der Kurve. Wenn es fehlschlägt, warte eine kurze Zeit auf weitere Daten für NTCP 1   >   > - Überprüfe den AEAD-Frame. Wenn es fehlschlägt, warte eine kurze Zeit auf weitere Daten für NTCP 1

Beachten Sie, dass Änderungen oder zusätzliche Strategien empfohlen werden können, wenn wir aktive TCP-Segmentierungsangriffe auf NTCP 1 erkennen.

Um eine schnelle Versionserkennung und den Handshake zu erleichtern, müssen Implementierungen sicherstellen, dass Alice den gesamten Inhalt der ersten Nachricht puffert und dann auf einmal überträgt, einschließlich des Paddings. Dies erhöht die Wahrscheinlichkeit, dass die Daten in einem einzigen TCP-Paket enthalten sind (außer bei Segmentierung durch das Betriebssystem oder Middleboxes) und von Bob auf einmal empfangen werden. Dies dient auch der Effizienz und um die Wirksamkeit des zufälligen Paddings sicherzustellen. Dies gilt sowohl für NTCP- als auch für NTCP2-Handshakes.

## Varianten, Fallbacks und allgemeine Probleme

- Wenn Alice und Bob beide NTCP2 unterstützen, sollte Alice sich mit NTCP2 verbinden.
- Wenn Alice aus irgendeinem Grund nicht mit NTCP2 zu Bob verbinden kann, schlägt die Verbindung fehl. Alice darf es nicht mit NTCP 1 erneut versuchen.

## Richtlinien zur Uhrzeitabweichung

Peer-Zeitstempel sind in den ersten beiden Handshake-Nachrichten enthalten: Session Request und Session Created. Eine Zeitabweichung zwischen zwei Peers von mehr als +/- 60 Sekunden ist in der Regel fatal. Wenn Bob denkt, dass seine lokale Uhr falsch geht, kann er seine Uhr mit der berechneten Abweichung oder einer externen Quelle korrigieren. Andernfalls sollte Bob mit einer Session Created antworten, auch wenn die maximale Abweichung überschritten wird, anstatt die Verbindung einfach zu schließen. Dies ermöglicht es Alice, Bobs Zeitstempel zu erhalten und die Abweichung zu berechnen, und bei Bedarf Maßnahmen zu ergreifen. Bob hat zu diesem Zeitpunkt nicht Alices router-Identität, aber um Ressourcen zu schonen, kann es wünschenswert sein, dass Bob eingehende Verbindungen von Alices IP für eine gewisse Zeit sperrt, oder nach wiederholten Verbindungsversuchen mit einer übermäßigen Abweichung.

Alice sollte die berechnete Uhrenabweichung anpassen, indem sie die Hälfte der RTT abzieht. Wenn Alice denkt, dass ihre lokale Uhr fehlerhaft ist, kann sie ihre Uhr mit der berechneten Abweichung oder einer externen Quelle anpassen. Wenn Alice denkt, dass Bobs Uhr fehlerhaft ist, kann sie Bob für eine bestimmte Zeit sperren. In beiden Fällen sollte Alice die Verbindung schließen.

Wenn Alice mit Session Confirmed antwortet (wahrscheinlich weil die Zeitabweichung sehr nahe am 60s-Limit liegt und die Berechnungen von Alice und Bob aufgrund der RTT nicht exakt gleich sind), sollte Bob die berechnete Uhrzeitabweichung anpassen, indem er die Hälfte der RTT abzieht. Wenn die angepasste Uhrzeitabweichung das Maximum überschreitet, sollte Bob dann mit einer Disconnect-Nachricht antworten, die einen Uhrzeitabweichungs-Grund-Code enthält, und die Verbindung schließen. An diesem Punkt hat Bob Alices Router-Identität und kann Alice für eine bestimmte Zeit sperren.

## Referenzen

- [Gemeinsame Strukturen](/docs/specs/common-structures)
- [I2NP](/docs/specs/i2np)
- [Network Database](/docs/overview/network-database)
- [NOISE - Noise Protocol Framework](https://noiseprotocol.org/noise.html)
- [NTCP](/docs/transport/ntcp)
- [Prop104](/proposals/104-tls-transport)
- [Prop109](/proposals/109-pt-transport)
- [Prop111](/proposals/111-ntcp-2)
- [RFC-2104 - HMAC](https://tools.ietf.org/html/rfc2104)
- [RFC-3526 - DH Groups](https://tools.ietf.org/html/rfc3526)
- [RFC-6151](https://tools.ietf.org/html/rfc6151)
- [RFC-7539 - ChaCha20-Poly1305](https://tools.ietf.org/html/rfc7539)
- [RFC-7748 - X25519](https://tools.ietf.org/html/rfc7748)
- [RFC-7905](https://tools.ietf.org/html/rfc7905)
- [SipHash](https://www.131002.net/siphash/)
- [SSU](/docs/transport/ssu)
- **[STS]** Diffie, W.; van Oorschot P. C.; Wiener M. J., Authentifizierung und authentifizierte Schlüsselaustauschverfahren
