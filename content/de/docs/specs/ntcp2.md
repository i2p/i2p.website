---
title: "NTCP2 Transport"
description: "Noise-basierter TCP-Transport für router-zu-router-Verbindungen"
slug: "ntcp2"
lastUpdated: "2025-10"
accurateFor: "0.9.66"
type: docs
---

## Übersicht

NTCP2 ersetzt den veralteten NTCP-Transport durch einen auf dem Noise-Protokoll basierenden Handshake, der gegen Traffic-Fingerprinting resistent ist, Längenfelder verschlüsselt und moderne Cipher-Suites unterstützt. Router können NTCP2 parallel zu SSU2 als die beiden obligatorischen Transportprotokolle im I2P-Netzwerk betreiben. NTCP (Version 1) wurde in 0.9.40 (Mai 2019) als veraltet markiert und in 0.9.50 (Mai 2021) vollständig entfernt.

## Noise Protocol Framework (kryptografisches Protokoll-Framework „Noise“)

NTCP2 verwendet das Noise Protocol Framework [Revision 33, 2017-10-04](https://noiseprotocol.org/noise.html) mit I2P-spezifischen Erweiterungen:

- **Muster**: `Noise_XK_25519_ChaChaPoly_SHA256`
- **Erweiterter Bezeichner**: `Noise_XKaesobfse+hs2+hs3_25519_ChaChaPoly_SHA256` (für KDF-Initialisierung)
- **DH-Funktion**: X25519 (RFC 7748) - 32-Byte-Schlüssel, Little-Endian-Codierung
- **Chiffre**: AEAD_CHACHA20_POLY1305 (RFC 7539/RFC 8439)
  - 12-Byte-Nonce: erste 4 Bytes sind Null, die letzten 8 Bytes sind ein Zähler (Little-Endian)
  - Maximaler Nonce-Wert: 2^64 - 2 (die Verbindung muss beendet werden, bevor 2^64 - 1 erreicht wird)
- **Hash-Funktion**: SHA-256 (32-Byte-Ausgabe)
- **MAC**: Poly1305 (16-Byte-Authentifizierungstag)

### I2P-spezifische Erweiterungen

1. **AES-Verschleierung**: Ephemere Schlüssel, mit AES-256-CBC unter Verwendung von Bobs Router-Hash und veröffentlichtem IV verschlüsselt
2. **Zufälliges Padding**: Klartext-Padding in den Nachrichten 1–2 (authentifiziert), AEAD-Padding ab Nachricht 3 (verschlüsselt)
3. **SipHash-2-4-Längenverschleierung**: Zweibyte-Frame-Längen werden mit der SipHash-Ausgabe XOR-verknüpft
4. **Frame-Struktur**: Längenpräfixierte Frames für die Datenphase (TCP-Streaming-Kompatibilität)
5. **Blockbasierte Nutzlasten**: Strukturiertes Datenformat mit typisierten Blöcken

## Ablauf des Handshakes

```
Alice (Initiator)             Bob (Responder)
SessionRequest  ──────────────────────►
                ◄────────────────────── SessionCreated
SessionConfirmed ──────────────────────►
```
### Drei-Nachrichten-Handshake

1. **SessionRequest** - Alices verschleierter ephemerer Schlüssel, Optionen, Padding-Hinweise
2. **SessionCreated** - Bobs verschleierter ephemerer Schlüssel, verschlüsselte Optionen, Padding
3. **SessionConfirmed** - Alices verschlüsselter statischer Schlüssel und RouterInfo (zwei AEAD-Frames)

### Noise-Nachrichtenmuster

```
XK(s, rs):           Authentication   Confidentiality
  <- s               (Bob's static key known in advance)
  -> e, es                  0                2
  <- e, ee                  2                1
  -> s, se                  2                5
  <-                        2                5
```
**Authentifizierungsstufen:** - 0: Keine Authentifizierung (jede Partei könnte es gesendet haben) - 2: Absenderauthentifizierung, resistent gegen key-compromise impersonation (KCI, Identitätsanmaßung bei Schlüsselkompromittierung)

**Vertraulichkeitsstufen:** - 1: Ephemerer Empfänger (Vorwärtsgeheimnis, keine Empfänger-Authentifizierung) - 2: Bekannter Empfänger, Vorwärtsgeheimnis nur bei Kompromittierung des Senders - 5: Starkes Vorwärtsgeheimnis (ephemeral-ephemeral + ephemeral-static DH (Diffie-Hellman))

## Nachrichtenspezifikationen

### Schlüsselnotation

- `RH_A` = Router Hash für Alice (32 Byte, SHA-256)
- `RH_B` = Router Hash für Bob (32 Byte, SHA-256)
- `||` = Verkettungsoperator
- `byte(n)` = Einzelnes Byte mit dem Wert n
- Alle Mehrbyte-Ganzzahlen sind **big-endian**, sofern nicht anders angegeben
- X25519-Schlüssel sind **little-endian** (32 Byte)

### Authentifizierte Verschlüsselung (ChaCha20-Poly1305)

**Verschlüsselungsfunktion:**

```
AEAD_ChaCha20_Poly1305(key, nonce, associatedData, plaintext)
  → (ciphertext || MAC)
```
**Parameter:** - `key`: 32-Byte-Chiffrierschlüssel aus KDF (Schlüsselableitungsfunktion) - `nonce`: 12 Byte (4 Nullbytes + 8-Byte-Zähler, Little-Endian) - `associatedData`: 32-Byte-Hash in der Handshake-Phase; Länge 0 in der Datenphase - `plaintext`: Zu verschlüsselnde Daten (0+ Byte)

**Ausgabe:** - Geheimtext: gleiche Länge wie der Klartext - MAC: 16 Bytes (Poly1305-Authentifizierungstag)

**Nonce-Verwaltung (einmalig verwendeter Wert):** - Der Zähler beginnt bei 0 für jede Verschlüsselungsinstanz - Erhöht sich bei jeder AEAD-Operation in dieser Richtung - Separate Zähler für Alice→Bob und Bob→Alice in der Datenphase - Die Verbindung muss beendet werden, bevor der Zähler den Wert 2^64 - 1 erreicht

## Nachricht 1: SessionRequest (Sitzungsanfrage)

Alice stellt eine Verbindung zu Bob her.

**Noise-Operationen**: `e, es` (Erzeugung und Austausch ephemerer Schlüssel)

### Rohformat

```
+----+----+----+----+----+----+----+----+
|                                       |
+    AES-256-CBC Encrypted X (32B)      +
|    Key: RH_B, IV: Bob's published IV  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+    ChaChaPoly Frame (48 bytes)        +
|    Plaintext: 32B (X + options)       |
+    k from KDF-1, n=0, ad=h            +
|                                       |
+----+----+----+----+----+----+----+----+
|    Cleartext Padding (optional)       |
+    Length specified in options         +
|    0 to 65535 - 80 bytes              |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
**Größenbeschränkungen:** - Minimum: 80 Bytes (32 AES + 48 AEAD) - Maximum: 65535 Bytes insgesamt - **Sonderfall**: Max. 287 Bytes beim Verbindungsaufbau zu "NTCP"-Adressen (Versionserkennung)

### Entschlüsselter Inhalt

```
+----+----+----+----+----+----+----+----+
|                                       |
+    X (Alice ephemeral public key)     +
|    32 bytes, X25519, little-endian    |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|           Options Block               |
+             (16 bytes)                +
|                                       |
+----+----+----+----+----+----+----+----+
|    Cleartext Padding (optional)       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
### Optionsblock (16 Byte, Big-Endian)

```
+----+----+----+----+----+----+----+----+
| id | ver|  padLen | m3p2len | Rsvd(0) |
+----+----+----+----+----+----+----+----+
|        tsA        |   Reserved (0)    |
+----+----+----+----+----+----+----+----+

id      : 1 byte  - Network ID (2 for mainnet, 16-254 for testnets)
ver     : 1 byte  - Protocol version (currently 2)
padLen  : 2 bytes - Padding length in this message (0-65455)
m3p2len : 2 bytes - Length of SessionConfirmed part 2 frame
Rsvd    : 2 bytes - Reserved, set to 0
tsA     : 4 bytes - Unix timestamp (seconds since epoch)
Reserved: 4 bytes - Reserved, set to 0
```
**Kritische Felder:** - **Network ID** (seit 0.9.42): Schnelle Zurückweisung netzwerkübergreifender Verbindungen - **m3p2len**: Exakte Größe von Nachricht 3, Teil 2 (muss beim Senden übereinstimmen)

### Schlüsselableitungsfunktion (KDF-1)

**Protokoll initialisieren:**

```
protocol_name = "Noise_XKaesobfse+hs2+hs3_25519_ChaChaPoly_SHA256"
h = SHA256(protocol_name)
ck = h  // Chaining key initialized to hash
```
**MixHash-Operationen:**

```
h = SHA256(h)                    // Null prologue
h = SHA256(h || rs)              // Bob's static key (known)
h = SHA256(h || e.pubkey)        // Alice's ephemeral key X
// h is now the associated data for message 1 AEAD
```
**MixKey-Operation (es-Pattern):**

```
dh_result = X25519(Alice.ephemeral_private, Bob.static_public)
temp_key = HMAC-SHA256(ck, dh_result)
ck = HMAC-SHA256(temp_key, byte(0x01))
k = HMAC-SHA256(temp_key, ck || byte(0x02))
// k is the cipher key for message 1
// ck is retained for message 2 KDF
```
### Implementierungshinweise

1. **AES-Verschleierung**: Wird nur zur DPI-Resistenz verwendet (DPI: Deep Packet Inspection, Analyse von Datenpaketen); jeder, der Bobs Router-Hash und IV (Initialisierungsvektor) besitzt, kann X entschlüsseln
2. **Replay-Schutz (Schutz vor Wiederholungsangriffen)**: Bob muss X-Werte (oder verschlüsselte Entsprechungen) für mindestens 2*D Sekunden zwischenspeichern (D = maximale Uhrenabweichung)
3. **Zeitstempel-Validierung**: Bob muss Verbindungen mit |tsA - current_time| > D ablehnen (typischerweise D = 60 Sekunden)
4. **Kurvenvalidierung**: Bob muss prüfen, dass X ein gültiger Punkt auf X25519 (elliptische Kurve) ist
5. **Schnelle Ablehnung**: Bob darf X[31] & 0x80 == 0 vor der Entschlüsselung prüfen (gültige X25519-Schlüssel haben das MSB (Most Significant Bit, höchstwertiges Bit) nicht gesetzt)
6. **Fehlerbehandlung**: Bei jedem Fehler schließt Bob mit TCP RST (TCP-Reset) nach einer zufälligen Wartezeit und dem Lesen einer zufälligen Anzahl von Bytes
7. **Pufferung**: Alice muss die gesamte Nachricht (einschließlich Padding (Auffüllung)) aus Effizienzgründen in einem Stück übertragen

## Nachricht 2: SessionCreated (Sitzung erstellt)

Bob antwortet Alice.

**Noise-Operationen**: `e, ee` (ephemeral-ephemeral DH, Diffie-Hellman zwischen zwei ephemeren (kurzlebigen) Schlüsseln)

### Rohformat

```
+----+----+----+----+----+----+----+----+
|                                       |
+    AES-256-CBC Encrypted Y (32B)      +
|    Key: RH_B, IV: AES state from msg1 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+    ChaChaPoly Frame (48 bytes)        +
|    Plaintext: 32B (Y + options)       |
+    k from KDF-2, n=0, ad=h            +
|                                       |
+----+----+----+----+----+----+----+----+
|    Cleartext Padding (optional)       |
+    Length specified in options         +
|    0 to 65535 - 80 bytes              |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
### Entschlüsselter Inhalt

```
+----+----+----+----+----+----+----+----+
|                                       |
+    Y (Bob ephemeral public key)       +
|    32 bytes, X25519, little-endian    |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|           Options Block               |
+             (16 bytes)                +
|                                       |
+----+----+----+----+----+----+----+----+
|    Cleartext Padding (optional)       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
### Optionsblock (16 Bytes, big-endian (höherwertiges Byte zuerst))

```
+----+----+----+----+----+----+----+----+
| Rsvd(0) | padLen  |   Reserved (0)    |
+----+----+----+----+----+----+----+----+
|        tsB        |   Reserved (0)    |
+----+----+----+----+----+----+----+----+

Rsvd    : 2 bytes - Reserved, set to 0
padLen  : 2 bytes - Padding length in this message
Reserved: 10 bytes - Reserved, set to 0
tsB     : 4 bytes - Unix timestamp (seconds since epoch)
```
### Schlüsselableitungsfunktion (KDF-2)

**MixHash-Operationen:**

```
h = SHA256(h || encrypted_payload_msg1)  // 32-byte ciphertext
if (msg1_padding_length > 0):
    h = SHA256(h || padding_from_msg1)
h = SHA256(h || e.pubkey)                // Bob's ephemeral key Y
// h is now the associated data for message 2 AEAD
```
**MixKey-Operation (ee pattern, ee-Muster):**

```
dh_result = X25519(Bob.ephemeral_private, Alice.ephemeral_public)
temp_key = HMAC-SHA256(ck, dh_result)
ck = HMAC-SHA256(temp_key, byte(0x01))
k = HMAC-SHA256(temp_key, ck || byte(0x02))
// k is the cipher key for message 2
// ck is retained for message 3 KDF
```
**Speicherbereinigung:**

```
// Overwrite ephemeral keys after ee DH
Alice.ephemeral_public = zeros(32)
Alice.ephemeral_private = zeros(32)  // Bob side
Bob.received_ephemeral = zeros(32)    // Bob side
```
### Implementierungshinweise

1. **AES-Verkettung**: Die Verschlüsselung von Y verwendet den AES-CBC-Zustand aus Nachricht 1 (nicht zurückgesetzt)
2. **Schutz vor Wiederholungsangriffen**: Alice muss Y-Werte mindestens 2*D Sekunden zwischenspeichern
3. **Zeitstempelprüfung**: Alice muss |tsB - current_time| > D zurückweisen
4. **Kurvenvalidierung**: Alice muss prüfen, dass Y ein gültiger X25519-Punkt ist
5. **Fehlerbehandlung**: Alice schließt bei jedem Fehler mit TCP RST
6. **Pufferung**: Bob muss die gesamte Nachricht auf einmal senden

## Nachricht 3: SessionConfirmed (Sitzung bestätigt)

Alice bestätigt die Sitzung und sendet die RouterInfo.

**Noise-Operationen**: `s, se` (Offenlegung des statischen Schlüssels und statisch-ephemerer Diffie-Hellman (DH))

### Zweiteilige Struktur

Nachricht 3 besteht aus **zwei separaten AEAD frames** (AEAD, authentifizierte Verschlüsselung mit zusätzlichen Daten):

1. **Teil 1**: Fester 48-Byte-Frame mit Alices verschlüsseltem statischen Schlüssel
2. **Teil 2**: Frame variabler Länge mit RouterInfo, Optionen und Padding

### Rohformat

```
+----+----+----+----+----+----+----+----+
|    ChaChaPoly Frame 1 (48 bytes)      |
+    Plaintext: Alice static key (32B)  +
|    k from KDF-2, n=1, ad=h            |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+    ChaChaPoly Frame 2 (variable)      +
|    Length specified in msg1.m3p2len   |
+    k from KDF-3, n=0, ad=h            +
|    Plaintext: RouterInfo + padding    |
+                                       +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
**Größenbeschränkungen:** - Teil 1: Genau 48 Bytes (32 Klartext + 16 MAC) - Teil 2: Länge, in Nachricht 1 festgelegt (Feld m3p2len) - Maximalgröße insgesamt: 65535 Bytes (Teil 1 max 48, daher Teil 2 max 65487)

### Entschlüsselter Inhalt

**Teil 1:**

```
+----+----+----+----+----+----+----+----+
|                                       |
+    S (Alice static public key)        +
|    32 bytes, X25519, little-endian    |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
**Teil 2:**

```
+----+----+----+----+----+----+----+----+
|    Block: RouterInfo (required)       |
+    Type=2, contains Alice's RI         +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
|    Block: Options (optional)          |
+    Type=1, padding parameters          +
|                                       |
+----+----+----+----+----+----+----+----+
|    Block: Padding (optional)          |
+    Type=254, random data               +
|    MUST be last block if present      |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
### Schlüsselableitungsfunktion (KDF-3)

**Teil 1 (s-Muster):**

```
h = SHA256(h || encrypted_payload_msg2)  // 32-byte ciphertext
if (msg2_padding_length > 0):
    h = SHA256(h || padding_from_msg2)

// Encrypt static key with message 2 cipher key
ciphertext = AEAD_ChaCha20_Poly1305(k_msg2, n=1, h, Alice.static_public)
h = SHA256(h || ciphertext)  // 48 bytes (32 + 16)
// h is now the associated data for message 3 part 2
```
**Teil 2 (siehe Muster):**

```
dh_result = X25519(Alice.static_private, Bob.ephemeral_public)
temp_key = HMAC-SHA256(ck, dh_result)
ck = HMAC-SHA256(temp_key, byte(0x01))
k = HMAC-SHA256(temp_key, ck || byte(0x02))
// k is the cipher key for message 3 part 2
// ck is retained for data phase KDF

ciphertext = AEAD_ChaCha20_Poly1305(k, n=0, h, payload)
h = SHA256(h || ciphertext)
// h is retained for SipHash KDF
```
**Speicherbereinigung:**

```
// Overwrite Bob's ephemeral key after se DH
Alice.received_ephemeral = zeros(32)  // Alice side
Bob.ephemeral_public = zeros(32)       // Bob side
Bob.ephemeral_private = zeros(32)      // Bob side
```
### Hinweise zur Implementierung

1. **RouterInfo-Validierung**: Bob muss Signatur, Zeitstempel und Schlüsselkonsistenz prüfen
2. **Schlüsselabgleich**: Bob muss prüfen, dass Alices statischer Schlüssel in Teil 1 mit dem Schlüssel in der RouterInfo übereinstimmt
3. **Position des statischen Schlüssels**: In der NTCP oder NTCP2 RouterAddress nach einem passenden "s"-Parameter suchen
4. **Blockreihenfolge**: RouterInfo muss zuerst kommen, Options als Zweites (falls vorhanden), Padding zuletzt (falls vorhanden)
5. **Längenplanung**: Alice muss sicherstellen, dass m3p2len in Nachricht 1 exakt der Länge von Teil 2 entspricht
6. **Pufferung**: Alice muss beide Teile zusammen als einen einzigen TCP-Sendevorgang absetzen
7. **Optionale Verkettung**: Alice kann aus Effizienzgründen unmittelbar einen data phase frame (Frame der Datenphase) anhängen

## Datenphase

Nach Abschluss des Handshakes verwenden alle Nachrichten AEAD-Frames variabler Länge mit verschleierten Längenfeldern.

### Schlüsselableitungsfunktion (Datenphase)

**Split-Funktion (Noise):**

```
// Generate transmit and receive keys
zerolen = ""  // Zero-length byte array
temp_key = HMAC-SHA256(ck, zerolen)

// Alice transmits to Bob
k_ab = HMAC-SHA256(temp_key, byte(0x01))

// Bob transmits to Alice  
k_ba = HMAC-SHA256(temp_key, k_ab || byte(0x02))

// Cleanup
ck = zeros(32)
temp_key = zeros(32)
```
**SipHash-Schlüsselableitung:**

```
// Generate additional symmetric key for SipHash
ask_master = HMAC-SHA256(temp_key, "ask" || byte(0x01))

// "siphash" is 7 bytes US-ASCII
temp_key2 = HMAC-SHA256(ask_master, h || "siphash")
sip_master = HMAC-SHA256(temp_key2, byte(0x01))

// Alice to Bob SipHash keys
temp_key3 = HMAC-SHA256(sip_master, zerolen)
sipkeys_ab = HMAC-SHA256(temp_key3, byte(0x01))
sipk1_ab = sipkeys_ab[0:7]   // 8 bytes, little-endian
sipk2_ab = sipkeys_ab[8:15]  // 8 bytes, little-endian
sipiv_ab = sipkeys_ab[16:23] // 8 bytes, IV

// Bob to Alice SipHash keys
sipkeys_ba = HMAC-SHA256(temp_key3, sipkeys_ab || byte(0x02))
sipk1_ba = sipkeys_ba[0:7]   // 8 bytes, little-endian
sipk2_ba = sipkeys_ba[8:15]  // 8 bytes, little-endian
sipiv_ba = sipkeys_ba[16:23] // 8 bytes, IV
```
### Rahmenstruktur

```
+----+----+----+----+----+----+----+----+
|Obfs Len |                             |
+----+----+    ChaChaPoly Frame         +
|    Encrypted Block Data               |
+    k_ab (Alice→Bob) or k_ba (Bob→Alice)|
|    Nonce starts at 0, increments      |
+    No associated data (empty string)  +
|                                       |
~           .   .   .                   ~
|                                       |
+----+----+----+----+----+----+----+----+
|    Poly1305 MAC (16 bytes)            |
+----+----+----+----+----+----+----+----+
```
**Frame-Beschränkungen:** - Minimum: 18 Bytes (2 verschleierte Länge + 0 Klartext + 16 MAC) - Maximum: 65537 Bytes (2 verschleierte Länge + 65535 Frame) - Empfohlen: Wenige KB pro Frame (Empfängerlatenz minimieren)

### SipHash-Längenverschleierung

**Zweck**: Verhindern, dass DPI (tiefgehende Paketinspektion) die Frame-Grenzen erkennt

**Algorithmus:**

```
// Initialization (per direction)
IV[0] = sipiv  // From KDF

// For each frame:
IV[n] = SipHash-2-4(sipk1, sipk2, IV[n-1])
Mask[n] = IV[n][0:1]  // First 2 bytes of IV
ObfuscatedLength = ActualLength XOR Mask[n]

// Send 2-byte ObfuscatedLength, then ActualLength bytes
```
**Dekodierung:**

```
// Receiver maintains identical IV chain
IV[n] = SipHash-2-4(sipk1, sipk2, IV[n-1])
Mask[n] = IV[n][0:1]
ActualLength = ObfuscatedLength XOR Mask[n]
// Read ActualLength bytes (includes 16-byte MAC)
```
**Hinweise:** - Getrennte IV-Ketten für jede Richtung (Alice→Bob und Bob→Alice) - Wenn SipHash uint64 zurückgibt, die beiden niederwertigsten Bytes als Maske verwenden - uint64 als Little-Endian-Bytes in den nächsten IV umwandeln

### Blockformat

Jeder Frame enthält null oder mehr Blöcke:

```
+----+----+----+----+----+----+----+----+
|Type| Length  |       Data              |
+----+----+----+                        +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type  : 1 byte  - Block type identifier
Length: 2 bytes - Big-endian, data size (0-65516)
Data  : Variable length payload
```
**Größenlimits:** - Maximaler Frame: 65535 Bytes (einschließlich MAC) - Maximaler Blockbereich: 65519 Bytes (Frame - 16-Byte-MAC) - Maximaler Einzelblock: 65519 Bytes (3-Byte-Header + 65516 Daten)

### Blocktypen

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DateTime</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Time synchronization (4-byte timestamp)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Options</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Padding parameters, dummy traffic</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo delivery/flooding</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2NP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2NP message with shortened header</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Termination</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Explicit connection close</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">224-253</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental features</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">254</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Padding</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Random padding (must be last)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">255</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Future extensions</td></tr>
  </tbody>
</table>
**Regeln zur Blockreihenfolge:** - **Nachricht 3, Teil 2**: RouterInfo, Optionen (optional), Padding (Auffüllung; optional) - KEINE anderen Typen - **Datenphase**: Beliebige Reihenfolge, außer:   - Padding MUSS der letzte Block sein, falls vorhanden   - Termination (Beendigung) MUSS der letzte Block sein (außer Padding), falls vorhanden - Mehrere I2NP-Blöcke pro Frame erlaubt - Mehrere Padding-Blöcke pro Frame NICHT erlaubt

### Blocktyp 0: Datum/Uhrzeit

Zeitsynchronisierung zur Erkennung von Uhrzeitabweichungen.

```
+----+----+----+----+----+----+----+
| 0  |    4    |     timestamp     |
+----+----+----+----+----+----+----+

Type     : 0
Length   : 4 (big-endian)
Timestamp: 4 bytes, Unix seconds (big-endian)
```
**Implementierung**: Zur nächstgelegenen Sekunde runden, um die Akkumulation von Uhrversatz zu verhindern.

### Blocktyp 1: Optionen

Parameter für Padding (Auffüllung) und Traffic Shaping (Datenverkehrsformung).

```
+----+----+----+----+----+----+----+----+
| 1  |  size   |tmin|tmax|rmin|rmax|tdmy|
+----+----+----+----+----+----+----+----+
|tdmy|  rdmy   |  tdelay |  rdelay |    |
+----+----+----+----+----+----+----+    +
|         more_options (TBD)            |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type  : 1
Length: 12+ bytes (big-endian)
```
**Padding-Verhältnisse** (4.4-Festkommaformat, Wert/16.0): - `tmin`: Minimales Padding-Verhältnis beim Senden (0.0 - 15.9375) - `tmax`: Maximales Padding-Verhältnis beim Senden (0.0 - 15.9375) - `rmin`: Minimales Padding-Verhältnis beim Empfangen (0.0 - 15.9375) - `rmax`: Maximales Padding-Verhältnis beim Empfangen (0.0 - 15.9375)

**Beispiele:** - 0x00 = 0% Padding - 0x01 = 6,25% Padding - 0x10 = 100% Padding (1:1-Verhältnis) - 0x80 = 800% Padding (8:1-Verhältnis)

**Dummy-Datenverkehr:** - `tdmy`: Maximal bereit zu senden (2 Bytes, Durchschnitt in Bytes/Sekunde) - `rdmy`: Angeforderter Empfang (2 Bytes, Durchschnitt in Bytes/Sekunde)

**Einfügen von Verzögerungen:** - `tdelay`: Maximal einzufügende Verzögerung (2 Bytes, Durchschnitt in Millisekunden) - `rdelay`: Angeforderte Verzögerung (2 Bytes, Durchschnitt in Millisekunden)

**Leitlinien:** - Min-Werte geben die angestrebte Widerstandsfähigkeit gegen Traffic-Analyse an - Max-Werte geben Bandbreitenbeschränkungen an - Der Sender sollte das Maximum des Empfängers einhalten - Der Sender kann das Minimum des Empfängers innerhalb der Beschränkungen berücksichtigen - Kein Durchsetzungsmechanismus; Implementierungen können variieren

### Blocktyp 2: RouterInfo

RouterInfo-Übermittlung zur netdb-Befüllung und zum Flooding (flutartige Verteilung).

```
+----+----+----+----+----+----+----+----+
| 2  |  size   |flg |    RouterInfo     |
+----+----+----+----+                   +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type : 2
Length: Flag (1 byte) + RouterInfo size
Flag : Bit 0 = flood request (1) or local store (0)
       Bits 1-7 = Reserved, set to 0
```
**Verwendung:**

**In Nachricht 3 Teil 2** (Handshake): - Alice sendet ihre RouterInfo (Router-Informationsobjekt) an Bob - Flood bit (Steuerbit für Weiterverteilung) typischerweise 0 (lokale Speicherung) - RouterInfo NICHT gzip-komprimiert

**In der Datenphase:** - Jede Seite darf ihre aktualisierte RouterInfo (Router-Informationen) senden - Flood bit = 1: Anforderung der floodfill-Verteilung (wenn der Empfänger floodfill ist) - Flood bit = 0: Nur lokale netdb-Speicherung

**Validierungsanforderungen:** 1. Prüfen, ob der Signaturtyp unterstützt wird 2. RouterInfo-Signatur prüfen 3. Prüfen, ob der Zeitstempel innerhalb akzeptabler Grenzen liegt 4. Für den Handshake: Prüfen, ob der statische Schlüssel dem NTCP2-Adressparameter "s" entspricht 5. Für die Datenphase: Prüfen, ob der router-Hash zum Sitzungspartner passt 6. Nur RouterInfos mit veröffentlichten Adressen weiterverbreiten

**Hinweise:** - Kein ACK-Mechanismus (verwenden Sie I2NP DatabaseStore mit reply token (Antwort-Token), falls nötig) - Kann RouterInfos Dritter enthalten (floodfill-Nutzung) - NICHT gzip-komprimiert (im Gegensatz zu I2NP DatabaseStore)

### Blocktyp 3: I2NP-Nachricht

I2NP-Nachricht mit verkürztem 9-Byte-Header.

```
+----+----+----+----+----+----+----+----+
| 3  |  size   |type|    msg_id         |
+----+----+----+----+----+----+----+----+
|   expiration  |     I2NP payload      |
+----+----+----+                        +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type      : 3
Length    : 9 + payload_size (big-endian)
Type      : 1 byte, I2NP message type
Msg_ID    : 4 bytes, big-endian, I2NP message ID
Expiration: 4 bytes, big-endian, Unix timestamp (seconds)
Payload   : I2NP message body (length = size - 9)
```
**Unterschiede gegenüber NTCP1:** - Ablaufzeit: 4 Bytes (Sekunden) vs 8 Bytes (Millisekunden) - Länge: weggelassen (aus der Blocklänge ableitbar) - Prüfsumme: weggelassen (AEAD bietet Integrität) - Header: 9 Bytes vs 16 Bytes (44% Reduktion)

**Fragmentierung:** - I2NP-Nachrichten DÜRFEN NICHT über Blöcke hinweg fragmentiert werden - I2NP-Nachrichten DÜRFEN NICHT über Frames hinweg fragmentiert werden - Mehrere I2NP-Blöcke pro Frame sind zulässig

### Blocktyp 4: Beendigung

Explizites Schließen der Verbindung mit Beendigungsgrundcode.

```
+----+----+----+----+----+----+----+----+
| 4  |  size   |  valid_frames_recv    |
+----+----+----+----+----+----+----+----+
| (continued) |rsn |   additional_data   |
+----+----+----+----+                   +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type            : 4
Length          : 9+ bytes (big-endian)
Valid_Frames_Recv: 8 bytes, big-endian (receive nonce value)
                  0 if error in handshake phase
Reason          : 1 byte (see table below)
Additional_Data : Optional (format unspecified, for debugging)
```
**Begründungscodes:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Reason</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Phase</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Normal close / unspecified</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Termination received</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Idle timeout</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Router shutdown</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data phase AEAD failure</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Incompatible options</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Incompatible signature type</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Clock skew</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Padding violation</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">9</td><td style="border:1px solid var(--color-border); padding:0.5rem;">AEAD framing error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Payload format error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Message 1 error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Message 2 error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">13</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Message 3 error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">14</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Intra-frame read timeout</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo signature verification fail</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">16</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Static key parameter mismatch</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">17</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Banned</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td></tr>
  </tbody>
</table>
**Regeln:** - Die Terminierung MUSS der letzte Nicht-Padding-Block im Frame sein - Maximal ein Terminierungsblock pro Frame - Der Sender sollte die Verbindung nach dem Senden schließen - Der Empfänger sollte die Verbindung nach dem Empfangen schließen

**Fehlerbehandlung:** - Handshake-Fehler: In der Regel mit TCP RST schließen (kein Termination-Block) - AEAD-Fehler in der Datenphase: Zufälliges Timeout + zufälliges Lesen, dann Termination (Beendigung) senden - Siehe Abschnitt "AEAD Error Handling" für Sicherheitsverfahren

### Blocktyp 254: Auffüllung

Zufälliges Padding zur Erhöhung der Widerstandsfähigkeit gegen Verkehrsanalyse.

```
+----+----+----+----+----+----+----+----+
|254 |  size   |     random_data       |
+----+----+----+                        +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type: 254
Length: 0-65516 bytes (big-endian)
Data: Cryptographically random bytes
```
**Regeln:** - Padding MUSS der letzte Block im Frame sein, falls vorhanden - Padding mit Länge Null ist zulässig - Pro Frame ist nur ein Padding-Block zulässig - Nur aus Padding bestehende Frames sind zulässig - Sollte den ausgehandelten Parametern aus dem Options-Block entsprechen

**Padding in den Nachrichten 1-2:** - Außerhalb des AEAD (Authentifizierte Verschlüsselung mit zusätzlichen Daten)-Rahmens (Klartext) - In die Hash-Kette der nächsten Nachricht einbezogen (authentifiziert) - Manipulation wird erkannt, wenn die AEAD der nächsten Nachricht fehlschlägt

**Padding in Nachricht 3+ und Datenphase:** - Innerhalb des AEAD-Frames (verschlüsselt und authentifiziert) - Wird für Traffic Shaping und Größenverschleierung verwendet

## AEAD-Fehlerbehandlung

**Kritische Sicherheitsanforderungen:**

### Handshake-Phase (Nachrichten 1-3)

**Bekannte Nachrichtengröße:** - Nachrichtengrößen sind vorgegeben oder im Voraus spezifiziert - AEAD-Authentifizierungsfehler ist eindeutig

**Bobs Reaktion auf Fehler bei Nachricht 1:** 1. Zufälliges Timeout setzen (Bereich implementierungsabhängig, Vorschlag: 100-500ms) 2. Zufällige Anzahl von Bytes lesen (Bereich implementierungsabhängig, Vorschlag: 1KB-64KB) 3. Verbindung mit TCP RST schließen (keine Antwort) 4. Quell-IP vorübergehend sperren 5. Wiederholte Fehlschläge nachverfolgen, um langfristige Sperren zu verhängen

**Alices Reaktion auf Fehler bei Nachricht 2:** 1. Verbindung sofort mit TCP RST schließen 2. Keine Antwort an Bob

**Bobs Reaktion auf den Fehler bei Nachricht 3:** 1. Verbindung sofort mit TCP RST schließen 2. Keine Antwort an Alice

### Datenphase

**Verschleierte Nachrichtengröße:** - Das Längenfeld ist durch SipHash (Hash-Funktion) verschleiert - Ungültige Länge oder AEAD (authentifizierte Verschlüsselung mit assoziierten Daten)-Fehler könnte darauf hindeuten:   - Sondierung durch einen Angreifer   - Beschädigung im Netzwerk   - Desynchronisierter SipHash-IV (Initialisierungsvektor)   - Böswillige Gegenstelle

**Antwort auf AEAD- oder Längenfehler:** 1. Zufälliges Timeout setzen (empfohlen 100-500ms) 2. Zufällige Anzahl von Bytes lesen (empfohlen 1KB-64KB) 3. Beendigungsblock mit Reason-Code 4 (AEAD-Fehler) oder 9 (Framing-Fehler) senden 4. Verbindung schließen

**Vermeidung von Entschlüsselungsorakeln:** - Den Fehlertyp der Gegenstelle niemals vor Ablauf einer zufälligen Wartezeit offenlegen - Niemals auf die Längenvalidierung vor der AEAD-Prüfung verzichten - Ungültige Länge genauso behandeln wie einen AEAD-Fehler - Für beide Fehler denselben Fehlerbehandlungspfad verwenden

**Überlegungen zur Implementierung:** - Einige Implementierungen können nach Fehlern bei AEAD (authentifizierte Verschlüsselung mit zugehörigen Daten) fortfahren, sofern sie selten auftreten - Nach wiederholten Fehlern beenden (empfohlener Schwellenwert: 3–5 Fehler pro Stunde) - Abwägung zwischen Fehlerwiederherstellung und Sicherheit

## Veröffentlichte RouterInfo

### Format der Router-Adresse

Die NTCP2-Unterstützung wird über veröffentlichte RouterAddress-Einträge mit bestimmten Optionen bekanntgegeben.

**Transportstil:** - `"NTCP2"` - NTCP2 nur auf diesem Port - `"NTCP"` - Sowohl NTCP als auch NTCP2 auf diesem Port (automatische Erkennung)   - **Hinweis**: Unterstützung für NTCP (v1) wurde in 0.9.50 entfernt (Mai 2021)   - "NTCP"-Stil ist jetzt veraltet; verwenden Sie "NTCP2"

### Erforderliche Optionen

**Alle veröffentlichten NTCP2-Adressen:**

1. **`host`** - IP-Adresse (IPv4 oder IPv6) oder Hostname
   - Format: Standard-IP-Notation oder Domainname
   - Kann bei nur ausgehenden oder versteckten routers weggelassen werden

2. **`port`** - TCP-Portnummer
   - Format: Ganzzahl, 1-65535
   - Kann bei nur ausgehenden oder versteckten router weggelassen werden

3. **`s`** - Statischer öffentlicher Schlüssel (X25519)
   - Format: Base64-kodiert, 44 Zeichen
   - Kodierung: I2P-Base64-Alphabet
   - Quelle: öffentlicher X25519-Schlüssel (32 Byte), Little-Endian

4. **`i`** - Initialisierungsvektor für AES
   - Format: Base64-kodiert, 24 Zeichen
   - Kodierung: I2P-Base64-Alphabet
   - Quelle: 16-Byte-IV, Big-Endian

5. **`v`** - Protokollversion
   - Format: Ganzzahl oder durch Kommas getrennte Ganzzahlen
   - Aktuell: `"2"`
   - Zukünftig: `"2,3"` (muss in numerischer Reihenfolge sein)

**Optionale Einstellungen:**

6. **`caps`** - Fähigkeiten (seit 0.9.50)
   - Format: Zeichenkette aus Fähigkeitszeichen
   - Werte:
     - `"4"` - IPv4-Fähigkeit für ausgehende Verbindungen
     - `"6"` - IPv6-Fähigkeit für ausgehende Verbindungen
     - `"46"` - Sowohl IPv4 als auch IPv6 (empfohlene Reihenfolge)
   - Nicht erforderlich, wenn `host` veröffentlicht ist
   - Nützlich für versteckte bzw. hinter einer Firewall befindliche routers

7. **`cost`** - Adresspriorität
   - Format: Ganzzahl, 0-255
   - Niedrigere Werte = höhere Priorität
   - Empfohlen: 5-10 für normale Adressen
   - Empfohlen: 14 für unveröffentlichte Adressen

### Beispielhafte RouterAddress-Einträge

**Veröffentlichte IPv4-Adresse:**

```
<Address cost="5">
  <transport_style>NTCP2</transport_style>
  <options>
    <host>192.0.2.1</host>
    <port>8887</port>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <i>MDEyMzQ1Njc4OUFCQ0RFRg==</i>
    <v>2</v>
  </options>
</Address>
```
**Verborgener Router (nur ausgehend):**

```
<Address cost="14">
  <transport_style>NTCP2</transport_style>
  <options>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <v>2</v>
    <caps>4</caps>
  </options>
</Address>
```
**Dual-Stack-Router:**

```
<!-- IPv4 Address -->
<Address cost="5">
  <transport_style>NTCP2</transport_style>
  <options>
    <host>192.0.2.1</host>
    <port>8887</port>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <i>MDEyMzQ1Njc4OUFCQ0RFRg==</i>
    <v>2</v>
  </options>
</Address>

<!-- IPv6 Address (same keys, same port) -->
<Address cost="5">
  <transport_style>NTCP2</transport_style>
  <options>
    <host>2001:db8::1</host>
    <port>8887</port>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <i>MDEyMzQ1Njc4OUFCQ0RFRg==</i>
    <v>2</v>
  </options>
</Address>
```
**Wichtige Regeln:** - Mehrere NTCP2-Adressen mit **demselben Port** MÜSSEN **identische** `s`-, `i`- und `v`-Werte verwenden - Verschiedene Ports dürfen unterschiedliche Schlüssel verwenden - Dual-Stack routers sollten getrennte IPv4- und IPv6-Adressen veröffentlichen

### Unveröffentlichte NTCP2-Adresse

**Für ausschließlich ausgehende Router:**

Wenn ein router keine eingehenden NTCP2-Verbindungen akzeptiert, aber ausgehende Verbindungen initiiert, MUSS er dennoch eine RouterAddress mit Folgendem veröffentlichen:

```xml
<Address cost="14">
  <transport_style>NTCP2</transport_style>
  <options>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <v>2</v>
  </options>
</Address>
```
**Zweck:** - Ermöglicht es Bob, Alices statischen Schlüssel während des Handshakes zu verifizieren - Erforderlich für die Verifizierung der RouterInfo in Nachricht 3, Teil 2 - Keine `i`, `host` oder `port` erforderlich (nur ausgehend)

**Alternative:** - Füge `s` und `v` zur bereits veröffentlichten "NTCP"- oder SSU-Adresse hinzu

### Rotation von öffentlichem Schlüssel und IV (Initialisierungsvektor)

**Kritische Sicherheitsrichtlinie:**

**Allgemeine Regeln:** 1. **Niemals rotieren, während der router läuft** 2. **Schlüssel und IV (Initialisierungsvektor) dauerhaft speichern** über Neustarts hinweg 3. **Vorherige Ausfallzeit nachverfolgen**, um festzustellen, ob eine Rotation in Frage kommt

**Mindest-Ausfallzeit vor der Rotation:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Router Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Min Downtime</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Reason</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Published NTCP2 address</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>1 month</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Many routers cache RouterInfo</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Published SSU only (no NTCP2)</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>1 day</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Moderate caching</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">No published addresses (hidden)</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>2 hours</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimal impact</td></tr>
  </tbody>
</table>
**Zusätzliche Auslöser:** - Änderung der lokalen IP-Adresse: Kann unabhängig von Ausfallzeiten rotieren - Router "rekey" (new Router Hash): Neue Schlüssel erzeugen

**Begründung:** - Verhindert das Offenlegen von Neustartzeiten durch Schlüsseländerungen - Ermöglicht, dass zwischengespeicherte RouterInfos natürlich ablaufen - Wahrung der Netzwerkstabilität - Verringert fehlgeschlagene Verbindungsversuche

**Implementierung:** 1. Schlüssel, IV (Initialisierungsvektor) und Zeitstempel des letzten Herunterfahrens dauerhaft speichern 2. Beim Start die Ausfallzeit berechnen: downtime = current_time - last_shutdown 3. Wenn downtime > Minimum für den router-Typ, kann rotiert werden 4. Wenn sich die IP geändert hat oder eine Schlüsselerneuerung stattfindet, kann rotiert werden 5. Andernfalls den vorherigen Schlüssel und die IV wiederverwenden

**IV Rotation:** - Unterliegt denselben Regeln wie die Schlüsselrotation - Nur in veröffentlichten Adressen vorhanden (nicht in versteckten routers) - Es wird empfohlen, den IV zu ändern, sobald sich der Schlüssel ändert

## Versionserkennung

**Kontext:** Wenn `transportStyle="NTCP"` (veraltet) ist, unterstützt Bob sowohl NTCP v1 als auch v2 auf demselben Port und muss die Protokollversion automatisch erkennen.

**Erkennungsalgorithmus:**

```
1. Wait for at least 64 bytes (minimum NTCP2 message 1 size)

2. If received ≥ 288 bytes:
   → Connection is NTCP version 1 (NTCP1 message 1 is 288 bytes)

3. If received < 288 bytes:
   
   Option A (conservative, pre-NTCP2 majority):
   a. Wait additional short time (e.g., 100-500ms)
   b. If total received ≥ 288 bytes → NTCP1
   c. Otherwise → Attempt NTCP2 decode
   
   Option B (aggressive, post-NTCP2 majority):
   a. Attempt NTCP2 decode immediately:
      - Decrypt first 32 bytes (X key) with AES-256-CBC
      - Verify valid X25519 point (X[31] & 0x80 == 0)
      - Verify AEAD frame
   b. If decode succeeds → NTCP2
   c. If decode fails → Wait for more data or NTCP1
```
**Schnelle MSB-Prüfung (höchstwertiges Bit):** - Vor der AES-Entschlüsselung prüfen: `encrypted_X[31] & 0x80 == 0` - Gültige X25519-Schlüssel haben das höchstwertige Bit nicht gesetzt - Ein Fehlschlag weist wahrscheinlich auf NTCP1 (oder einen Angriff) hin - Bei Fehlschlag Sondierungsresistenz implementieren (zufälliges Timeout + read)

**Anforderungen an die Implementierung:**

1. **Alices Verantwortung:**
   - Begrenze Nachricht 1 beim Verbindungsaufbau zu einer "NTCP"-Adresse auf maximal 287 Bytes
   - Puffere die gesamte Nachricht 1 und sende sie anschließend auf einmal
   - Erhöht die Wahrscheinlichkeit der Zustellung in einem einzigen TCP-Paket

2. **Bobs Verantwortung:**
   - Empfangene Daten puffern, bevor die Version bestimmt wird
   - Ordnungsgemäße Timeout-Behandlung implementieren
   - TCP_NODELAY für eine schnelle Versionserkennung verwenden
   - Nach Erkennung der Version die gesamte Nachricht 2 auf einmal puffern und einen flush durchführen (Puffer leeren)

**Sicherheitsaspekte:** - Segmentierungsangriffe: Bob sollte gegenüber TCP-Segmentierung robust sein - Sondierungsangriffe: Zufällige Verzögerungen und Byte-Lesevorgänge bei Fehlern implementieren - DoS-Prävention: Gleichzeitig ausstehende Verbindungen begrenzen - Lese-Timeouts: Sowohl pro Lesevorgang als auch insgesamt ("slowloris"-Schutz)

## Richtlinien zur Uhrzeitabweichung

**Zeitstempel-Felder:** - Nachricht 1: `tsA` (Zeitstempel von Alice) - Nachricht 2: `tsB` (Zeitstempel von Bob) - Nachricht 3+: Optionale DateTime-Blöcke (Datum/Uhrzeit)

**Maximale Zeitabweichung (D):** - Typisch: **±60 Sekunden** - Pro Implementierung konfigurierbar - Zeitabweichung > D ist in der Regel fatal

### Bobs Verarbeitung (Nachricht 1)

```
1. Receive tsA from Alice
2. skew = tsA - current_time
3. If |skew| > D:
   a. Still send message 2 (allows Alice to calculate skew)
   b. Include tsB in message 2
   c. Do NOT initiate handshake completion
   d. Optionally: Temporary ban Alice's IP
   e. After message 2 sent, close connection

4. If |skew| ≤ D:
   a. Continue handshake normally
```
**Begründung:** Das Senden von Nachricht 2 selbst bei Zeitabweichung ermöglicht es Alice, Probleme mit der Systemuhr zu diagnostizieren.

### Alices Verarbeitung (Nachricht 2)

```
1. Receive tsB from Bob
2. RTT = (current_time_now - tsA_sent)
3. adjusted_skew = (tsB - current_time_now) - (RTT / 2)
4. If |adjusted_skew| > D:
   a. Close connection immediately
   b. If local clock suspect: Adjust clock or use external time source
   c. If Bob's clock suspect: Temporary ban Bob
   d. Log for operator review
5. If |adjusted_skew| ≤ D:
   a. Continue handshake normally
   b. Optionally: Track skew for time synchronization
```
**RTT-Anpassung:** - Ziehe die halbe RTT von der berechneten Uhrabweichung ab - Berücksichtigt die Ausbreitungsverzögerung im Netzwerk - Genauere Schätzung der Uhrabweichung

### Bobs Verarbeitung (Nachricht 3)

```
1. If message 3 received (unlikely if skew exceeded in message 1)
2. Recalculate skew = tsA_received - current_time
3. If |adjusted_skew| > D:
   a. Send termination block (reason code 7: clock skew)
   b. Close connection
   c. Ban Alice for period (e.g., 1-24 hours)
```
### Zeitsynchronisierung

**DateTime-Blöcke (Datenphase):** - DateTime-Block (Typ 0) regelmäßig senden - Empfänger kann ihn zum Uhrabgleich verwenden - Zeitstempel auf die nächste ganze Sekunde runden (Verzerrungen vermeiden)

**Externe Zeitquellen:** - NTP (Network Time Protocol) - Synchronisierung der Systemuhr - konsensbasierte Zeit des I2P-Netzwerks

**Strategien zur Uhrzeitkorrektur:** - Wenn die lokale Systemuhr falsch ist: Systemzeit anpassen oder einen Offset verwenden - Wenn die Uhren der Peers dauerhaft falsch sind: Peer-Problem kennzeichnen - Abweichungsstatistiken für die Überwachung der Netzwerkgesundheit nachverfolgen

## Sicherheitseigenschaften

### Vorwärtsgeheimnis

**Erreicht durch:** - Ephemerer Diffie-Hellman-Schlüsselaustausch (X25519) - Drei DH-Operationen: es, ee, se (Noise-XK-Muster) - Ephemere Schlüssel werden nach Abschluss des Handshakes vernichtet

**Vertraulichkeitsfortschritt:** - Nachricht 1: Stufe 2 (Vorwärtsgeheimnis bei Kompromittierung des Senders) - Nachricht 2: Stufe 1 (ephemerer Empfänger) - Nachricht 3+: Stufe 5 (starkes Vorwärtsgeheimnis)

**Perfect Forward Secrecy (Vorwärtsgeheimnis):** - Kompromittierung langfristiger statischer Schlüssel offenbart NICHT frühere Sitzungsschlüssel - Jede Sitzung verwendet eindeutige ephemere Schlüssel - Ephemere private Schlüssel werden niemals wiederverwendet - Speicherbereinigung nach der Schlüsselaushandlung

**Einschränkungen:** - Nachricht 1 ist verwundbar, wenn Bobs statischer Schlüssel kompromittiert ist (aber Vorwärtsgeheimnis bei einer Kompromittierung von Alice) - Wiederholungsangriffe auf Nachricht 1 sind möglich (abgemildert durch Zeitstempel und Replay-Cache)

### Authentifizierung

**Gegenseitige Authentifizierung:** - Alice wird in Nachricht 3 mittels eines statischen Schlüssels authentifiziert - Bob wird durch Besitz des statischen privaten Schlüssels authentifiziert (implizit durch einen erfolgreichen Handshake)

**Key Compromise Impersonation (KCI) Resistance (Widerstand gegen Identitätsanmaßung bei kompromittiertem Schlüssel):** - Authentifizierungsstufe 2 (resistent gegen KCI) - Ein Angreifer kann sich nicht als Alice ausgeben, selbst mit Alices statischem privaten Schlüssel (ohne Alices ephemeren Schlüssel) - Ein Angreifer kann sich nicht als Bob ausgeben, selbst mit Bobs statischem privaten Schlüssel (ohne Bobs ephemeren Schlüssel)

**Verifizierung statischer Schlüssel:** - Alice kennt Bobs statischen Schlüssel im Voraus (aus der RouterInfo (Router-Informationen)) - Bob verifiziert in Nachricht 3, dass Alices statischer Schlüssel mit der RouterInfo übereinstimmt - Verhindert Man-in-the-Middle-Angriffe

### Widerstand gegen Verkehrsanalyse

**DPI (Deep Packet Inspection)-Gegenmaßnahmen:** 1. **AES-Verschleierung:** Ephemere Schlüssel verschlüsselt, zufälliges Erscheinungsbild 2. **SipHash-Längenverschleierung:** Frame-Längen nicht im Klartext 3. **Zufälliges Padding (Auffüllung):** Variable Nachrichtengrößen, keine festen Muster 4. **Verschlüsselte Frames:** Gesamte Nutzlast mit ChaCha20 verschlüsselt

**Schutz vor Replay-Angriffen:** - Zeitstempelvalidierung (±60 Sekunden) - Replay-Cache für ephemere Schlüssel (Lebensdauer 2*D) - Inkremente der Nonce (Einmalwert) verhindern das Wiederholen von Paketen innerhalb einer Sitzung

**Widerstandsfähigkeit gegen Sondierungen:** - Zufällige Timeouts bei AEAD (Authentifizierte Verschlüsselung mit zusätzlichen Daten)-Fehlern - Zufälliges Lesen von Bytes vor dem Schließen der Verbindung - Keine Antworten bei Handshake-Fehlern - IP-Blockliste bei wiederholten Fehlern

**Richtlinien für Padding:** - Nachrichten 1-2: Klartext-Padding (authentifiziert) - Ab Nachricht 3: Verschlüsseltes Padding innerhalb von AEAD frames (Authenticated Encryption with Associated Data; authentifizierte Verschlüsselung mit zugeordneten Daten) - Ausgehandelte Padding-Parameter (Options-Block) - Nur-Padding-Frames zulässig

### Abwehr von Denial-of-Service-Angriffen

**Verbindungsbeschränkungen:** - Maximale Anzahl aktiver Verbindungen (implementierungsabhängig) - Maximale Anzahl ausstehender Handshakes (z. B. 100-1000) - Verbindungsbeschränkungen pro IP (z. B. 3-10 gleichzeitig)

**Ressourcenschutz:** - DH-Operationen ratenbegrenzt (rechenaufwendig) - Lese-Timeouts pro Socket und insgesamt - "Slowloris"-Schutz (Gesamtzeitlimits) - IP-Blacklisting bei Missbrauch

**Schnelle Zurückweisung:** - Netzwerk-ID stimmt nicht überein → sofortige Schließung - Ungültiger X25519-Punkt → schnelle MSB-Prüfung vor der Entschlüsselung - Zeitstempel außerhalb des zulässigen Bereichs → Schließen ohne Berechnung - AEAD-Fehler → keine Antwort, zufällige Verzögerung

**Sondierungsresistenz:** - Zufälliges Timeout: 100-500ms (implementierungsabhängig) - Zufälliges Lesen: 1KB-64KB (implementierungsabhängig) - Keine Fehlerinformationen an den Angreifer - Mit TCP RST schließen (kein FIN-Handshake)

### Kryptografische Sicherheit

**Algorithmen:** - **X25519**: 128-Bit-Sicherheit, Diffie-Hellman über elliptische Kurven (Curve25519) - **ChaCha20**: Stromchiffre mit 256-Bit-Schlüssel - **Poly1305**: informationstheoretisch sichere MAC (Message Authentication Code) - **SHA-256**: 128-Bit-Kollisionsresistenz, 256-Bit-Urbildresistenz - **HMAC-SHA256**: PRF (pseudorandom function, pseudozufällige Funktion) für die Schlüsselableitung

**Schlüsselgrößen:** - Statische Schlüssel: 32 Bytes (256 Bit) - Ephemere Schlüssel: 32 Bytes (256 Bit) - Chiffrierschlüssel: 32 Bytes (256 Bit) - MAC: 16 Bytes (128 Bit)

**Bekannte Probleme:** - Wiederverwendung von ChaCha20-Nonces (einmalige Werte) ist katastrophal (verhindert durch Zählerinkrement) - X25519 hat Probleme mit kleinen Untergruppen (abgemildert durch Kurvenvalidierung) - SHA-256 ist theoretisch anfällig für Längenerweiterung (in HMAC nicht ausnutzbar)

**Keine bekannten Schwachstellen (Stand Oktober 2025):** - Noise Protocol Framework (Kryptografie-Rahmenwerk für Handshake-Protokolle) umfassend analysiert - ChaCha20-Poly1305 (AEAD-Algorithmus) in TLS 1.3 eingesetzt - X25519 (Schlüsselaustausch auf Basis elliptischer Kurven) Standard in modernen Protokollen - Keine praktischen Angriffe auf die Konstruktion

## Referenzen

### Primäre Spezifikationen

- **[NTCP2-Spezifikation](/docs/specs/ntcp2/)** - Offizielle I2P-Spezifikation
- **[Vorschlag 111](/proposals/111-ntcp-2/)** - Ursprüngliches Entwurfsdokument mit Begründung
- **[Noise Protocol Framework](https://noiseprotocol.org/noise.html)** - Revision 33 (2017-10-04)

### Kryptografische Standards

- **[RFC 7748](https://www.rfc-editor.org/rfc/rfc7748)** - Elliptische Kurven für Sicherheitszwecke (X25519)
- **[RFC 7539](https://www.rfc-editor.org/rfc/rfc7539)** - ChaCha20 und Poly1305 für IETF-Protokolle
- **[RFC 8439](https://www.rfc-editor.org/rfc/rfc8439)** - ChaCha20-Poly1305 (ersetzt RFC 7539)
- **[RFC 2104](https://www.rfc-editor.org/rfc/rfc2104)** - HMAC: Schlüsselbasiertes Hashing zur Nachrichtenauthentifizierung
- **[SipHash](https://www.131002.net/siphash/)** - SipHash-2-4 für Anwendungen von Hashfunktionen

### Verwandte I2P-Spezifikationen

- **[I2NP-Spezifikation](/docs/specs/i2np/)** - Nachrichtenformat des I2P-Netzwerkprotokolls
- **[Gemeinsame Strukturen](/docs/specs/common-structures/)** - Formate von RouterInfo und RouterAddress
- **[SSU-Transport](/docs/legacy/ssu/)** - UDP-Transport (ursprünglich, jetzt SSU2)
- **[Vorschlag 147](/proposals/147-transport-network-id-check/)** - Prüfung der Transport-Netzwerk-ID (0.9.42)

### Referenzen zur Implementierung

- **[I2P Java](https://github.com/i2p/i2p.i2p)** - Referenzimplementierung (Java)
- **[i2pd](https://github.com/PurpleI2P/i2pd)** - C++-Implementierung
- **[I2P Versionshinweise](/blog/)** - Versionsverlauf und Aktualisierungen

### Historischer Kontext

- **[Station-To-Station Protocol (STS)](https://en.wikipedia.org/wiki/Station-to-Station_protocol)** - Inspiration für das Noise-Framework
- **[obfs4](https://gitlab.com/yawning/obfs4)** - Pluggable transport (austauschbares Transportprotokoll; SipHash-Längenverschleierung als Präzedenzfall)

## Implementierungsrichtlinien

### Verbindliche Anforderungen

**Zur Einhaltung:**

1. **Vollständigen Handshake implementieren:**
   - Alle drei Nachrichten mit korrekten KDF-Ketten (Schlüsselableitungsfunktionen) unterstützen
   - Alle AEAD-Tags (Authentifizierte Verschlüsselung mit zusätzlichen Daten) validieren
   - Überprüfen, dass X25519-Punkte gültig sind

2. **Datenphase implementieren:**
   - SipHash-Längenverschleierung (in beiden Richtungen)
   - Alle Blocktypen: 0 (DateTime), 1 (Options), 2 (RouterInfo), 3 (I2NP), 4 (Termination), 254 (Padding)
   - Korrektes Nonce (Einmalwert)-Management (separate Zähler)

3. **Sicherheitsfunktionen:**
   - Replay-Schutz (ephemere Schlüssel für 2*D zwischenspeichern)
   - Zeitstempel-Validierung (Standard: ±60 Sekunden)
   - Zufälliges Padding in Nachrichten 1-2
   - AEAD (authentifizierte Verschlüsselung mit zusätzlichen Daten)-Fehlerbehandlung mit zufälligen Timeouts

4. **Veröffentlichung von RouterInfo:**
   - Veröffentliche statischen Schlüssel ("s"), IV ("i") und Version ("v")
   - Rotiere Schlüssel gemäß Richtlinie
   - Unterstütze das Feld für Fähigkeiten ("caps") für versteckte router

5. **Netzwerkkompatibilität:**
   - Unterstützung des Netzwerk-ID-Felds (derzeit 2 für mainnet (Hauptnetz))
   - Interoperabilität mit bestehenden Java- und i2pd-Implementierungen
   - Unterstützung von IPv4 und IPv6

### Empfohlene Vorgehensweisen

**Leistungsoptimierung:**

1. **Pufferstrategie:**
   - Gesamte Nachrichten auf einmal senden (Nachrichten 1, 2, 3)
   - TCP_NODELAY (TCP-Option, die den Nagle-Algorithmus deaktiviert) für Handshake-Nachrichten verwenden
   - Mehrere Datenblöcke zu einem einzelnen Frame puffern
   - Frame-Größe auf wenige KB begrenzen (Latenz beim Empfänger minimieren)

2. **Verbindungsverwaltung:**
   - Verbindungen nach Möglichkeit wiederverwenden
   - Verbindungspooling implementieren
   - Verbindungsgesundheit überwachen (DateTime blocks – zeitbezogene Blöcke)

3. **Speicherverwaltung:**
   - Sensible Daten nach der Verwendung auf Null setzen (ephemere Schlüssel, DH-Ergebnisse (Diffie-Hellman))
   - Gleichzeitige Handshakes begrenzen (DoS-Prävention)
   - Speicherpools für häufige Zuweisungen verwenden

**Sicherheitshärtung:**

1. **Abwehr von Sondierungsversuchen:**
   - Zufällige Timeouts: 100-500ms
   - Zufällige Byte-Lesevorgänge: 1KB-64KB
   - IP-Blacklisting bei wiederholten Fehlschlägen
   - Keine Fehlerdetails an Peers

2. **Ressourcengrenzen:**
   - Maximale Verbindungen pro IP: 3-10
   - Maximale ausstehende Handshakes: 100-1000
   - Lese-Timeouts: 30-60 Sekunden pro Vorgang
   - Gesamtes Verbindungs-Timeout: 5 Minuten für den Handshake

3. **Schlüsselverwaltung:**
   - Persistente Speicherung von statischem Schlüssel und IV (Initialisierungsvektor)
   - Sichere Zufallszahlengenerierung (kryptografischer RNG)
   - Rotationsrichtlinien strikt einhalten
   - Ephemere Schlüssel niemals wiederverwenden

**Überwachung und Diagnose:**

1. **Metriken:**
   - Erfolgs-/Fehlerraten beim Handshake
   - AEAD-Fehlerraten
   - Verteilung der Uhrenabweichungen
   - Statistiken zur Verbindungsdauer

2. **Protokollierung:**
   - Handshake-Fehler mit Reason-Codes (Begründungscodes) protokollieren
   - Clock-Skew-Ereignisse (Abweichungen der Systemuhren) protokollieren
   - Gesperrte IP-Adressen protokollieren
   - Niemals sensibles Schlüsselmaterial protokollieren

3. **Tests:**
   - Unit-Tests für KDF-Ketten
   - Integrationstests mit anderen Implementierungen
   - Fuzzing für Paketverarbeitung
   - Lasttests zur Widerstandsfähigkeit gegen DoS

### Häufige Fallstricke

**Kritische Fehler, die zu vermeiden sind:**

1. **Wiederverwendung von Nonces (Nonce = Einmalwert):**
   - Den Nonce-Zähler niemals während einer Sitzung zurücksetzen
   - Für jede Richtung separate Zähler verwenden
   - Vor Erreichen von 2^64 - 1 beenden

2. **Schlüsselrotation:**
   - Niemals Schlüssel rotieren, während der router läuft
   - Ephemere Schlüssel niemals über Sitzungen hinweg wiederverwenden
   - Regeln für minimale Ausfallzeit befolgen

3. **Zeitstempel-Verarbeitung:**
   - Niemals abgelaufene Zeitstempel akzeptieren
   - Bei der Berechnung der Abweichung stets die RTT (Round-Trip Time) berücksichtigen
   - DateTime-Zeitstempel auf Sekunden runden

4. **AEAD-Fehler:**
   - Fehlertyp niemals gegenüber dem Angreifer offenlegen
   - Vor dem Schließen stets einen zufälligen Timeout verwenden
   - Ungültige Länge genauso behandeln wie einen AEAD-Fehler

5. **Padding:**
   - Niemals Padding außerhalb der vereinbarten Grenzen senden
   - Den Padding-Block immer zuletzt platzieren
   - Niemals mehrere Padding-Blöcke pro Frame

6. **RouterInfo:**
   - Immer überprüfen, dass der statische Schlüssel mit der RouterInfo übereinstimmt
   - Niemals RouterInfos ohne veröffentlichte Adressen flooden (über floodfill verbreiten)
   - Immer Signaturen verifizieren

### Testmethodik

**Unit-Tests:**

1. **Kryptographische Primitive:**
   - Testvektoren für X25519, ChaCha20, Poly1305, SHA-256
   - Testvektoren für HMAC-SHA256
   - Testvektoren für SipHash-2-4

2. **KDF-Ketten:**
   - Known-Answer-Tests für alle drei Nachrichten
   - Weitergabe des Chaining Keys (Verkettungsschlüssel) überprüfen
   - SipHash-IV-Erzeugung testen

3. **Nachrichten-Parsing:**
   - Dekodierung gültiger Nachrichten
   - Ablehnung ungültiger Nachrichten
   - Randbedingungen (leer, maximale Größe)

**Integrationstests:**

1. **Handshake:**
   - Erfolgreicher Austausch von drei Nachrichten
   - Zurückweisung bei Uhrversatz
   - Erkennung von Replay-Angriffen
   - Zurückweisung ungültiger Schlüssel

2. **Datenphase:**
   - I2NP-Nachrichtenübertragung
   - RouterInfo-Austausch
   - Verarbeitung von Padding (Auffüllung)
   - Beendigungsnachrichten

3. **Interoperabilität:**
   - Gegen Java I2P testen
   - Gegen i2pd testen
   - IPv4 und IPv6 testen
   - Veröffentlichte und versteckte routers testen

**Sicherheitstests:**

1. **Negativtests:**
   - Ungültige AEAD-Tags
   - Erneut gesendete Nachrichten
   - Angriffe durch Zeitdrift (Clock Skew)
   - Fehlerhaft formatierte Frames

2. **DoS-Tests:**
   - Verbindungsflutung
   - Slowloris-Angriffe (Angriff durch langsame, unvollständige HTTP-Anfragen)
   - CPU-Erschöpfung (exzessives DH (Diffie-Hellman))
   - Speichererschöpfung

3. **Fuzzing:**
   - Zufällige Handshake-Nachrichten
   - Zufällige Frames der Datenphase
   - Zufällige Blocktypen und -größen
   - Ungültige kryptografische Werte

### Migration von NTCP

**Für Legacy-NTCP-Unterstützung (inzwischen entfernt):**

NTCP (Version 1) wurde in I2P 0.9.50 (Mai 2021) entfernt. Alle aktuellen Implementierungen müssen NTCP2 unterstützen. Historische Anmerkungen:

1. **Übergangsphase (2018-2021):**
   - 0.9.36: NTCP2 eingeführt (standardmäßig deaktiviert)
   - 0.9.37: NTCP2 standardmäßig aktiviert
   - 0.9.40: NTCP als veraltet markiert
   - 0.9.50: NTCP entfernt

2. **Versionserkennung:**
   - "NTCP" transportStyle gab an, dass beide Versionen unterstützt werden
   - "NTCP2" transportStyle gab an, dass nur NTCP2 unterstützt wird
   - Automatische Erkennung anhand der Nachrichtengröße (287 vs 288 Bytes)

3. **Aktueller Status:**
   - Alle Router müssen NTCP2 unterstützen
   - "NTCP" transportStyle ist veraltet
   - Ausschließlich den "NTCP2" transportStyle verwenden

## Anhang A: Noise-XK-Muster

**Standard Noise XK Pattern (standardmäßiges XK-Muster des Noise-Protokolls):**

```
XK(s, rs):
  <- s
  ...
  -> e, es
  <- e, ee
  -> s, se
```
**Interpretation:**

- `<-` : Nachricht vom Responder (Bob) an den Initiator (Alice)
- `->` : Nachricht vom Initiator (Alice) an den Responder (Bob)
- `s` : Statischer Schlüssel (Langzeit-Identitätsschlüssel)
- `rs` : Entfernter statischer Schlüssel (statischer Schlüssel der Gegenstelle, vorab bekannt)
- `e` : Ephemerer Schlüssel (sitzungsspezifisch, bei Bedarf erzeugt)
- `es` : Ephemer-Statisch DH (Diffie-Hellman-Schlüsselaustausch; Alice ephemerer × Bob statischer)
- `ee` : Ephemer-Ephemer DH (Alice ephemerer × Bob ephemerer)
- `se` : Statisch-Ephemer DH (Alice statischer × Bob ephemerer)

**Ablauf der Schlüsselvereinbarung:**

1. **Vorabnachricht:** Alice kennt Bobs statischen öffentlichen Schlüssel (aus RouterInfo)
2. **Nachricht 1:** Alice sendet einen ephemeren Schlüssel, führt es DH aus
3. **Nachricht 2:** Bob sendet einen ephemeren Schlüssel, führt ee DH aus
4. **Nachricht 3:** Alice gibt den statischen Schlüssel preis, führt se DH aus

**Sicherheitseigenschaften:**

- Alice authentifiziert: Ja (durch Nachricht 3)
- Bob authentifiziert: Ja (durch Besitz des statischen privaten Schlüssels)
- Vorwärtsgeheimnis: Ja (ephemere Schlüssel vernichtet)
- KCI resistance (Widerstandsfähigkeit gegen Key-Compromise-Impersonation): Ja (Authentifizierungsstufe 2)

## Anhang B: Base64-Kodierung

**I2P-Base64-Alphabet:**

```
ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-~
```
**Unterschiede zu Standard-Base64:** - Zeichen 62-63: `-~` statt `+/` - Padding: gleich (`=`) oder je nach Kontext weggelassen

**Verwendung in NTCP2:** - Statischer Schlüssel ("s"): 32 Bytes → 44 Zeichen (kein Padding) - IV ("i"): 16 Bytes → 24 Zeichen (kein Padding)

**Kodierungsbeispiel:**

```python
# 32-byte static key (hex): 
# f4489e1bb0597b39ca6cbf5ad9f5f1f09043e02d96cb9aa6a63742b3462429aa

# I2P Base64 encoded:
# 9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=
```
## Anhang C: Analyse von Paketmitschnitten

**Erkennung von NTCP2-Verkehr:**

1. **TCP-Handshake:**
   - Standard-TCP SYN, SYN-ACK, ACK
   - Zielport typischerweise 8887 oder ähnlich

2. **Nachricht 1 (SessionRequest – Sitzungsanforderung):**
   - Erste Anwendungsdaten von Alice
   - 80-65535 Bytes (typischerweise ein paar Hundert)
   - Erscheint zufällig (AES-verschlüsselter ephemerer Schlüssel)
   - Maximal 287 Bytes bei Verbindung zu einer "NTCP"-Adresse

3. **Nachricht 2 (SessionCreated):**
   - Antwort von Bob
   - 80-65535 Bytes (typischerweise einige Hundert)
   - Erscheint ebenfalls zufällig

4. **Nachricht 3 (SessionConfirmed, Sitzung bestätigt):**
   - Von Alice
   - 48 Byte + variabler Anteil (RouterInfo-Größe + Padding)
   - Typischerweise 1–4 KB

5. **Datenphase:**
   - Frames variabler Länge
   - Längenfeld verschleiert (erscheint zufällig)
   - Verschlüsselte Nutzlast
   - Padding macht die Größe unvorhersehbar

**DPI-Umgehung:** - Keine Klartext-Header - Keine festen Muster - Längenfelder verschleiert - Zufälliges Padding durchbricht größenbasierte Heuristiken

**Vergleich mit NTCP:** - NTCP Nachricht 1 ist immer 288 Byte groß (identifizierbar) - Bei NTCP2 variiert die Größe von Nachricht 1 (nicht identifizierbar) - NTCP hatte erkennbare Muster - NTCP2 wurde so entworfen, dass es DPI widersteht

## Anhang D: Versionsverlauf

**Wichtige Meilensteine:**

- **0.9.36** (23. August 2018): NTCP2 eingeführt, standardmäßig deaktiviert
- **0.9.37** (4. Oktober 2018): NTCP2 standardmäßig aktiviert
- **0.9.40** (20. Mai 2019): NTCP als veraltet markiert
- **0.9.42** (27. August 2019): Netzwerk-ID-Feld hinzugefügt (Proposal 147)
- **0.9.50** (17. Mai 2021): NTCP entfernt, Unterstützung für Fähigkeiten hinzugefügt
- **2.10.0** (9. September 2025): Neueste stabile Version

**Protokollstabilität:** - Keine inkompatiblen Änderungen seit 0.9.50 - Laufende Verbesserungen der Widerstandsfähigkeit gegen Sondierungsangriffe - Fokus auf Leistung und Zuverlässigkeit - Post-Quanten-Kryptografie in Entwicklung (standardmäßig nicht aktiviert)

**Aktueller Transportstatus:** - NTCP2: Obligatorischer TCP-Transport - SSU2: Obligatorischer UDP-Transport - NTCP (v1): Entfernt - SSU (v1): Entfernt
