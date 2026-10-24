---
title: "PQ Hybrid SSU2"
description: "Post-Quanten-Hybridvariante des SSU2-Transportprotokolls mit ML-KEM"
slug: "ssu2-hybrid"
lastupdated: "2026-10"
category: "Transports"
accurateFor: "0.9.71"
---

### Status

Beta Q2 2026, Veröffentlichung Q3 2026

## Übersicht

Dies ist die hybride post-quantengesicherte Variante des SSU2-Transportprotokolls, wie sie in Proposal 169 entworfen wurde. Weitere Hintergrundinformationen sind in diesem Proposal zu finden.

PQ Hybrid SSU2 ist nur auf derselben Adresse und demselben Port wie Standard-SSU2 definiert. Der Betrieb auf einem anderen Port oder ohne Standard-SSU2-Unterstützung ist nicht zulässig und wird es auch für mehrere Jahre nicht sein, bis Standard-SSU2 abgekündigt wird.

Diese Spezifikation dokumentiert ausschließlich die Änderungen, die am Standard-SSU2 erforderlich sind, um PQ Hybrid zu unterstützen. Die grundlegenden Implementierungsdetails sind der SSU2-Spezifikation zu entnehmen.

## Design

Wir unterstützen die NIST FIPS 203 und 204 Standards [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf), die auf CRYSTALS-Kyber und CRYSTALS-Dilithium (Versionen 3.1, 3 und älter) basieren, jedoch NICHT mit diesen kompatibel sind.

### Schlüsselaustausch

PQ KEM bietet ausschließlich ephemere Schlüssel und unterstützt keine statischen Schlüssel-Handshakes wie Noise XK und IK. Die Verschlüsselungstypen sind dieselben wie im PQ Hybrid Ratchet und werden im Dokument für gemeinsame Strukturen [/docs/specs/common-structures/](/docs/specs/common-structures/) definiert; wie in [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) sind Hybrid-Typen nur in Kombination mit X25519 definiert.

Die Verschlüsselungstypen sind:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">SSU2 Version</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
</tr>
</table>
### Zulässige Kombinationen

Die neuen Verschlüsselungstypen werden in den RouterAddresses angegeben. Der Verschlüsselungstyp im Key-Zertifikat bleibt weiterhin Typ 4.

## Spezifikation

### Handshake-Muster

Handshakes verwenden [Noise Protocol](https://noiseprotocol.org/noise.html)-Handshake-Muster.

Die folgende Buchstabenzuordnung wird verwendet:

- e = einmaliger ephemerer Schlüssel
- s = statischer Schlüssel
- p = Nachrichtennutzlast
- e1 = einmaliger ephemerer PQ-Schlüssel, von Alice an Bob gesendet
- ekem1 = der KEM-Chiffretext, von Bob an Alice gesendet

Die folgenden Modifikationen an XK und IK für hybride Vorwärtsgeheimhaltung (hfs) sind wie in [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) Abschnitt 5 spezifiziert:

```
XK:                       XKhfs:
  <- s                      <- s
  ...                       ...
  -> e, es, p               -> e, es, e1, p
  <- e, ee, p               <- e, ee, ekem1, p
  -> s, se                  -> s, se
  <- p                      <- p
  p ->                      p ->


  e1 and ekem1 are encrypted. See pattern definitions below.
  NOTE: e1 and ekem1 are different sizes (unlike X25519)
```
Das e1-Muster ist wie folgt definiert, wie in [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) Abschnitt 4 angegeben:

```
For Alice:
  (encap_key, decap_key) = PQ_KEYGEN()

  // EncryptAndHash(encap_key)
  ciphertext = ENCRYPT(k, n, encap_key, ad)
  n++
  MixHash(ciphertext)

  For Bob:

  // DecryptAndHash(ciphertext)
  encap_key = DECRYPT(k, n, ciphertext, ad)
  n++
  MixHash(ciphertext)
```
Das ekem1-Muster ist wie folgt definiert, wie in [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) Abschnitt 4 angegeben:

```
For Bob:

  (kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

  // EncryptAndHash(kem_ciphertext)
  ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)
  MixHash(ciphertext)

  // MixKey
  MixKey(kem_shared_key)


  For Alice:

  // DecryptAndHash(ciphertext)
  kem_ciphertext = DECRYPT(k, n, ciphertext, ad)
  MixHash(ciphertext)

  // MixKey
  kem_shared_key = DECAPS(kem_ciphertext, decap_key)
  MixKey(kem_shared_key)
```
### Noise Handshake KDF

#### Übersicht

Der hybride Handshake ist in der [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) definiert. Die erste Nachricht von Alice an Bob enthält e1, den Kapselungsschlüssel (encapsulation key), vor der Nachrichtennutzlast. Dieser wird als zusätzlicher statischer Schlüssel behandelt; rufe darauf `EncryptAndHash()` (als Alice) bzw. `DecryptAndHash()` (als Bob) auf. Anschließend wird die Nachrichtennutzlast wie gewohnt verarbeitet.

Die zweite Nachricht, von Bob an Alice, enthält ekem1, den Chiffretext, vor der Nachrichtennutzlast. Dieser wird als zusätzlicher statischer Schlüssel behandelt; rufen Sie darauf EncryptAndHash() (als Bob) oder DecryptAndHash() (als Alice) auf. Berechnen Sie dann den kem_shared_key und rufen Sie MixKey(kem_shared_key) auf. Anschließend wird die Nachrichtennutzlast wie gewohnt verarbeitet.

#### Definierte ML-KEM-Operationen

Wir definieren die folgenden Funktionen, die den kryptografischen Bausteinen entsprechen, wie sie in [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) festgelegt sind.

(encap_key, decap_key) = PQ_KEYGEN()

    Alice creates the encapsulation and decapsulation keys
    The encapsulation key is sent in message 1.
    encap_key and decap_key sizes vary based on ML-KEM variant.

(ciphertext, kem_shared_key) = ENCAPS(encap_key)

    Bob calculates the ciphertext and shared key,
    using the ciphertext received in message 1.
    The ciphertext is sent in message 2.
    ciphertext size varies based on ML-KEM variant.
    The kem_shared_key is always 32 bytes.

kem_shared_key = DECAPS(ciphertext, decap_key)

    Alice calculates the shared key,
    using the ciphertext received in message 2.
    The kem_shared_key is always 32 bytes.

Beachten Sie, dass sowohl der encap_key als auch der Ciphertext in ChaCha/Poly-Blöcken innerhalb der Noise-Handshake-Nachrichten 1 und 2 verschlüsselt sind. Sie werden im Rahmen des Handshake-Prozesses entschlüsselt.

Der kem_shared_key wird mit MixHash() in den Verkettungsschlüssel eingemischt. Weitere Details siehe unten.

#### Alice KDF für Nachricht 1

Nach dem 'es'-Nachrichtenmuster und vor der Nutzlast einfügen:

```
This is the "e1" message pattern:
  (encap_key, decap_key) = PQ_KEYGEN()

  // EncryptAndHash(encap_key)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, encap_key, ad)
  n++

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)


  End of "e1" message pattern.

  NOTE: For the next section (payload for XK or static key for IK),
  the keydata and chain key remain the same,
  and n now equals 1 (instead of 0 for non-hybrid).
```
#### Bob KDF für Nachricht 1

Nach dem 'es'-Nachrichtenmuster und vor der Nutzlast einfügen:

```
This is the "e1" message pattern:

  // DecryptAndHash(encap_key_section)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  encap_key = DECRYPT(k, n, encap_key_section, ad)
  n++

  // MixHash(encap_key_section)
  h = SHA256(h || encap_key_section)

  End of "e1" message pattern.

  NOTE: For the next section (payload for XK or static key for IK),
  the keydata and chain key remain the same,
  and n now equals 1 (instead of 0 for non-hybrid).
```
#### Bob KDF für Nachricht 2

Für XK: Nach dem 'ee' Nachrichtenmuster und vor der Nutzlast, füge hinzu:

```
This is the "ekem1" message pattern:

  (kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

  // EncryptAndHash(kem_ciphertext)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)

  // MixKey(kem_shared_key)
  keydata = HKDF(chainKey, kem_shared_key, "", 64)
  chainKey = keydata[0:31]

  End of "ekem1" message pattern.

  // AEAD parameters for payload section
  ... as in standard SSU2 ...
  k = keydata[32:63]
  ...

```
#### Alice KDF für Nachricht 2

Nach dem 'ee'-Nachrichtenmuster hinzufügen:

```
This is the "ekem1" message pattern:

  // DecryptAndHash(kem_ciphertext_section)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  kem_ciphertext = DECRYPT(k, n, kem_ciphertext_section, ad)

  // MixHash(kem_ciphertext_section)
  h = SHA256(h || kem_ciphertext_section)

  // MixKey(kem_shared_key)
  kem_shared_key = DECAPS(kem_ciphertext, decap_key)
  keydata = HKDF(chainKey, kem_shared_key, "", 64)
  chainKey = keydata[0:31]

  End of "ekem1" message pattern.

  // AEAD parameters for payload section
  ... as in standard SSU2 ...
  k = keydata[32:63]
  ...

```
#### KDF für Nachricht 3

unverändert

#### KDF für split()

unverändert

### Handshake-Details

#### Noise-Bezeichner

- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"

Beachten Sie, dass MLKEM-1024 für SSU2 NICHT unterstützt wird, da die Schlüssel zu groß sind, um in ein Standard-1500-Byte-Datagramm zu passen.

#### Langer Header

Der lange Header ist 32 Byte groß. Er wird verwendet, bevor eine Session erstellt wurde, für Token Request, SessionRequest, SessionCreated und Retry. Er wird außerdem für Peer Test- und Hole Punch-Nachrichten außerhalb einer Session verwendet.

Setzen Sie in den folgenden Nachrichten das Feld ver (Version) im langen Header auf 3 oder 4, um MLKEM-512 bzw. MLKEM-768 anzugeben.

- (0) Sitzungsanfrage
- (1) Sitzung erstellt
- (9) Wiederholen
- (10) Token-Anfrage
- (11) Hole Punch

In den folgenden Nachrichten ist das ver-Feld (Version) im langen Header wie üblich auf 2 zu setzen, auch wenn MLKEM-512 oder MLKEM-768 unterstützt wird. Implementierungen können den Wert auch auf 3 oder 4 setzen, wenn die Gegenseite dies unterstützt, jedoch ist dies nicht zwingend erforderlich. Implementierungen sollten jeden Wert von 2 bis 4 akzeptieren.

- (7) Peer Test (Nachrichten außerhalb der Sitzung 5–7)

Diskussion: Das Setzen des Versionsfelds auf 3 oder 4 ist möglicherweise nicht für alle Nachrichtentypen zwingend erforderlich, erleichtert jedoch die frühere Fehlererkennung bei nicht unterstützten Post-Quantum-Verbindungen. Token Request und Retry (Typen 9 und 10) sollten aus Konsistenzgründen die Versionen 3/4 verwenden. Hole Punch-Nachrichten (Typ 11) erfordern diese Behandlung möglicherweise nicht, wir werden jedoch zur Einheitlichkeit dasselbe Muster befolgen. Peer Test-Nachrichten (Typ 7) befinden sich außerhalb einer Sitzung und signalisieren keine Absicht, eine Sitzung einzuleiten.

- Relay Request
- Relay Response
- Relay Intro
- Peer Test

Vor der Header-Verschlüsselung:

Vor der Header-Verschlüsselung:

```

  +----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+

  Destination Connection ID :: 8 bytes, unsigned big endian integer

  Packet Number :: 4 bytes, unsigned big endian integer

  type :: The message type = 0, 1, 7, 9, 10, or 11

  ver :: The protocol version = 2, 3, or 4 for non-PQ, MLKEM512, MLKEM768

  id :: 1 byte, the network ID (currently 2, except for test networks)

  flag :: 1 byte, unused, set to 0 for future compatibility

  Source Connection ID :: 8 bytes, unsigned big endian integer

  Token :: 8 bytes, unsigned big endian integer

```
#### Kurzer Header

unverändert

#### SessionRequest (Typ 0)

Änderungen: Das aktuelle SSU2 enthält im ChaCha-Abschnitt nur die Block-Daten. Mit ML-KEM wird der ChaCha-Abschnitt zusätzlich den verschlüsselten öffentlichen PQ-Schlüssel enthalten.

KDF-Änderung zum Schutz vor Spoofing: Um die in Proposal 165 [Prop165]_ aufgeworfenen Probleme zu lösen, jedoch mit einem anderen Ansatz, modifizieren wir die KDF für Session Request. Dies gilt ausschließlich für PQ-Sessions. Die KDF für Nicht-PQ-Sessions bleibt unverändert.

```

// End of KDF for initial chain key (unchanged)
  // Bob static key
  // MixHash(bpk)
  h = SHA256(h || bpk);

  // Start of KDF for session request
  // NEW for PQ only
  // bhash = Bob router hash (32 bytes)
  // MixHash(bhash)
  h = SHA256(h || bhash);

  // Rest of KDF for session request, unchanged, as in SSU2 spec
  // MixHash(header)
  h = SHA256(h || header)

  ...

```
Roher Inhalt:

```
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 0-15, ChaCha20     |
  +  encrypted with Bob intro key         +
  |    See Header Encryption KDF          |
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 16-31, ChaCha20    |
  +  encrypted with Bob intro key n=0     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +       X, ChaCha20 encrypted           +
  |       with Bob intro key n=0          |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (MLKEM)     |
  +          (length varies)              +
  |  k defined in KDF for Session Request |
  +  n = 0                                +
  |  see KDF for associated data          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (payload)   |
  +          (length varies)              +
  |  k defined in KDF for Session Request |
  +  n = 1                                +
  |  see KDF for associated data          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
Unverschlüsselte Daten (Poly1305-Authentifizierungs-Tag nicht dargestellt):

```
  +----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                   X                   |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM encap_key            |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     Noise payload (block data)        |
  +          (length varies)              +
  |     see below for allowed blocks      |
  +----+----+----+----+----+----+----+----+
```
Größen, ohne IP-Overhead:

| Typ | Typ-Code | X Länge | Nachricht 1 Länge | Nachricht 1 Verschlüsselte Länge | Nachricht 1 Entschlüsselte Länge | PQ-Schlüssellänge | pl Länge |
|------|-----------|-------|-----------|---------------|---------------|------------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 896+pl | 832+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1280+pl | 1216+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | n/a | zu groß | | | | |
Hinweis: Typ-Codes sind nur für den internen Gebrauch bestimmt. Router bleiben vom Typ 4, und die Unterstützung wird in den Router-Adressen angegeben.

Minimale MTU für MLKEM768_X25519: 1318 für IPv4 und 1338 für IPv6. Siehe unten.

Änderungen: Das aktuelle SSU2 enthält nur die Nutzlast in einem einzigen ChaCha-Abschnitt. Mit ML-KEM wird ein neuer ChaCha-Abschnitt vor der Nutzlast hinzugefügt, der den verschlüsselten PQ-Ciphertext enthält.

#### SessionCreated (Typ 1)

Änderungen: Das aktuelle SSU2 enthält nur die Nutzlast in einem einzigen ChaCha-Abschnitt. Mit ML-KEM wird ein neuer ChaCha-Abschnitt vor der Nutzlast hinzugefügt, der den verschlüsselten PQ-Ciphertext enthält.

Roher Inhalt:

```
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 0-15, ChaCha20     |
  +  encrypted with Bob intro key and     +
  | derived key, see Header Encryption KDF|
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 16-31, ChaCha20    |
  +  encrypted with derived key n=0       +
  |  See Header Encryption KDF            |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +       Y, ChaCha20 encrypted           +
  |       with derived key n=0            |
  +              (32 bytes)               +
  |       See Header Encryption KDF       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 data (MLKEM)               |
  +   Encrypted and authenticated data    +
  |  length varies                        |
  +  k defined in KDF for Session Created +
  |  (before mixKey)                      |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 data (payload)             |
  +   Encrypted and authenticated data    +
  |  length varies                        |
  +  k defined in KDF for Session Created +
  |  (after mixKey)                       |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
Unverschlüsselte Daten (Poly1305-Authentifizierungs-Tag nicht angezeigt):

```
  +----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                  Y                    |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM Ciphertext           |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     Noise payload (block data)        |
  +          (length varies)              +
  |      see below for allowed blocks     |
  +----+----+----+----+----+----+----+----+
```
Größen, ohne IP-Overhead:

| Typ | Typcode | Y-Länge | Nachricht-2-Länge | Nachricht-2-Enc-Länge | Nachricht-2-Dec-Länge | PQ-CT-Länge | pl-Länge |
|------|-----------|-------|-----------|---------------|---------------|-----------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 864+pl | 800+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1184+pl | 1120+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | k. A. | zu groß | | | | |
Hinweis: Typ-Codes sind nur für den internen Gebrauch bestimmt. Router bleiben vom Typ 4, und die Unterstützung wird in den Router-Adressen angegeben.

Minimale MTU für MLKEM768_X25519: 1318 für IPv4 und 1338 für IPv6. Siehe unten.

Maximale Größe: Alice besitzt noch nicht Bobs RouterInfo und kennt daher seine veröffentlichte MTU nicht. Verwenden Sie für diese Nachricht eine temporäre MTU wie folgt. Bei MLKEM512_X25519 verwenden Sie das Maximum aus 1280 oder der empfangenen SessionRequest-Größe als MTU. Bei MLKEM768_X25519 verwenden Sie das Maximum aus (1318 für IPv4 oder 1338 für IPv6) oder der empfangenen SessionRequest-Größe als MTU. Der Overhead von SessionCreated ist geringer als der von SessionRequest, da der MLKEM-Chiffrat kleiner ist als der MLKEM-Öffentliche-Schlüssel. Dies ermöglicht eine Bandbreite an Auffüllgrößen in SessionCreated, selbst wenn im SessionRequest wenig oder keine Auffüllung vorhanden war.

#### SessionConfirmed (Typ 2)

unverändert

#### KDF für die Datenphase

unverändert

#### Relay und Peer-Test

Die folgenden Blöcke enthalten Versionsfelder. Sie bleiben bei Version 2 (zur Kompatibilität mit einem Nicht-PQ-Bob) und werden für PQ nicht auf Version 3/4 geändert.

* [CABFORUM](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/)
* [Choosing-Hash](https://kerkour.com/fast-secure-hash-function-sha256-sha512-sha3-blake3)
* [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/)
* [COMMON](/docs/specs/common-structures/)
* [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/)
* [ECIES](/docs/specs/ecies/)
* [FORUM](http://zzz.i2p/topics/3294)
* [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
* [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
* [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)
* [FIPS205](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.205.pdf)
* [MLDSA-OIDS](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/)
* [NIST-PQ](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards)
* [NIST-PQ-UPDATE](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf)
* [NIST-PQ-END](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf)
* [NIST-VECTORS](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values)
* [Noise](https://noiseprotocol.org/noise.html)
* [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf)
* [NSA-PQ](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF)
* [NTCP2](/docs/specs/ntcp2/)
* [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)
* [Prop165](/docs/proposals/165/)
* [PQ-WIREGUARD](https://eprint.iacr.org/2020/379.pdf)
* [RFC-2104](https://tools.ietf.org/html/rfc2104)
* [Rosenpass](https://rosenpass.eu/)
* [Rosenpass-Whitepaper](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf)
* [SSH-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-sshm-mlkem-hybrid-kex/)
* [SSU2](/docs/specs/ssu2/)
* [TLS-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-tls-hybrid-design/)

#### Veröffentlichte Adressen

Verwenden Sie in allen Fällen den SSU2-Transportnamen wie gewohnt. MLKEM-1024 wird nicht unterstützt.

Verwende dieselbe Adresse/denselben Port wie bei nicht-PQ, nicht-firewalled. Eine oder beide PQ-Varianten werden unterstützt. Veröffentliche in der Router-Adresse v=2 (wie üblich) sowie den neuen Parameter pq=[3|4|3,4|4,3], um MLKEM 512/768/beide anzugeben. Router mit einer MTU unterhalb des unten angegebenen Minimums dürfen keinen „pq"-Parameter veröffentlichen, der „4" enthält. Veröffentliche 4,3, um eine Präferenz für MLKEM-768 anzugeben, oder 3,4 für eine Präferenz für MLKEM-512. Die tatsächlich verwendete Version liegt im Ermessen des Initiators, und die angegebene Präferenz wird möglicherweise nicht berücksichtigt. Router mit einer MTU unterhalb des unten angegebenen Minimums dürfen keine Verbindung über MLKEM768 herstellen. Ältere Router ignorieren den pq-Parameter und verbinden sich wie gewohnt ohne PQ.

Verschiedene Adressen/Ports wie bei Nicht-PQ, oder PQ-only ohne Firewall werden NICHT unterstützt. Dies wird nicht implementiert, bis nicht-PQ SSU2 deaktiviert wird, was noch mehrere Jahre dauern wird. Wenn nicht-PQ deaktiviert ist, werden eine oder beide PQ-Varianten unterstützt. Veröffentlichen Sie in der router-Adresse v=[3|4|3,4|4,3], um MLKEM 512/768/beides anzugeben. Ältere router werden den v-Parameter prüfen und diese Adresse als nicht unterstützt überspringen.

Firewalled-Adressen (keine IP veröffentlicht): Veröffentlichen Sie in der Router-Adresse v=2 (wie gewohnt). Der pq-Parameter MUSS in Firewalled-Adressen veröffentlicht werden, um Relay zu unterstützen.

Alice kann sich mit einem PQ-fähigen Bob über die von Bob veröffentlichte PQ-Variante verbinden, unabhängig davon, ob Alice in ihren Router-Informationen PQ-Unterstützung ankündigt oder ob sie dieselbe Variante bewirbt.

#### MTU

Achten Sie darauf, die MTU bei MLKEM768 nicht zu überschreiten. Die minimale MTU für MLKEM768_X25519 beträgt 1318 für IPv4 und 1338 für IPv6 (ausgehend von einer minimalen Nutzlast von 10 Bytes mit einem DateTime- und einem Padding- oder RelayTagRequest-Block). Die minimale MTU für SSU2 im Allgemeinen beträgt 1280, daher können nicht alle Peers MLKEM768 verwenden. Veröffentlichen oder verwenden Sie MLKEM768 nicht, wenn die tatsächliche MTU geringer als das Minimum ist – weder lokal noch gemäß der vom Peer angegebenen MTU. Achten Sie darauf, die Padding-Größe nicht so zu wählen, dass Nachricht 1 oder 2 die lokale oder entfernte MTU überschreiten würde.

## Overhead-Analyse

### Schlüsselaustausch

Größenzunahme (Bytes):

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Pubkey (Msg 1)</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Ciphertext (Msg 2)</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+816</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+784</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+1200</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+1104</td>
</tr>
</table>
## Sicherheitsanalyse

Die NIST-Sicherheitskategorien sind in [NIST-Präsentation](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf) Folie 10 zusammengefasst. Vorläufige Kriterien: Unsere minimale NIST-Sicherheitskategorie sollte 2 für hybride Protokolle und 3 für reine Post-Quanten-Protokolle (PQ-only) sein.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Category</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">As Secure As</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES128</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">SHA256</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES192</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">SHA384</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES256</td>
</tr>
</table>
### Handshakes

Dies sind alles hybride Protokolle. Implementierungen sollten MLKEM768 bevorzugen; MLKEM512 ist nicht sicher genug.

NIST-Sicherheitskategorien [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf):

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Algorithm</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Security Category</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
</tr>
</table>
## Implementierungshinweise

### Bibliotheksunterstützung

Die Bibliotheken Bouncycastle, BoringSSL und WolfSSL unterstützen MLKEM und MLDSA bereits jetzt. OpenSSL-Unterstützung ist für deren Version 3.5 am 8. April 2025 geplant [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

### Identifizierung des eingehenden Datenverkehrs

Wir setzen das MSB (Most Significant Bit) des ephemeren Schlüssels (key[31] & 0x80) in der Session-Request, um anzuzeigen, dass es sich um eine Hybrid-Verbindung handelt. Dies ermöglicht es uns, sowohl Standard-NTCP als auch Hybrid-NTCP auf demselben Port zu betreiben. Für eingehende Verbindungen wird nur eine Hybrid-Variante unterstützt und in der router-Adresse bekanntgegeben. Zum Beispiel pq=3 oder pq=4.

## Router-Kompatibilität

### Transportbezeichnungen

Als Alice, für eine PQ-Verbindung, vor der Verschleierung, setze X[31] |= 0x80. Dies macht X zu einem ungültigen X25519-Public-Key. Nach der Verschleierung wird AES-CBC ihn randomisieren. Das MSB von X wird nach der Verschleierung zufällig sein.

## Referenzen

* [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/)
* [COMMON](/docs/specs/common-structures/)
* [ECIES](/docs/specs/ecies/)
* [FORUM](http://zzz.i2p/topics/3294)
* [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
* [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
* [NIST-PQ](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards)
* [NIST-PQ-UPDATE](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf)
* [NIST-PQ-END](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf)
* [NIST-VECTORS](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values)
* [Noise](https://noiseprotocol.org/noise.html)
* [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf)
* [NSA-PQ](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF)
* [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)
* [Prop165](/docs/proposals/165/)
* [PQ-WIREGUARD](https://eprint.iacr.org/2020/379.pdf)
* [RFC-2104](https://tools.ietf.org/html/rfc2104)
* [Rosenpass](https://rosenpass.eu/)
* [Rosenpass-Whitepaper](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf)
* [SSH-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-sshm-mlkem-hybrid-kex/)
* [SSU2](/docs/specs/ssu2/)
* [TLS-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-tls-hybrid-design/)
