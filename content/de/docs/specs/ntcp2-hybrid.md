---
title: "PQ-Hybrid-NTCP2"
description: "Post-quanten-hybride Variante des NTCP2-Transportprotokolls unter Verwendung von ML-KEM"
slug: "ntcp2-hybrid"
lastupdated: "2026-10"
category: "Transports"
accurateFor: "0.9.71"
---

### Status

Beta Q1 2026, Veröffentlichung Q2 2026

## Übersicht

Dies ist die hybride post-quanten-sichere Variante des NTCP2-Transportprotokolls, wie sie in Vorschlag 169 entworfen wurde. Siehe diesen Vorschlag für zusätzlichen Hintergrund.

PQ Hybrid NTCP2 ist nur für dieselbe Adresse und denselben Port wie standardmäßiges NTCP2 definiert. Der Betrieb an einem anderen Port oder ohne Unterstützung für standardmäßiges NTCP2 ist nicht zulässig und wird dies mehrere Jahre lang auch nicht sein, bis standardmäßiges NTCP2 als veraltet gilt.

Diese Spezifikation beschreibt ausschließlich die Änderungen, die erforderlich sind, um NTCP2 um PQ-Hybrid zu erweitern. Für die Grundimplementierungsdetails siehe die NTCP2-Spezifikation.

## Design

Wir unterstützen die NIST FIPS 203- und 204-Standards [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf), die auf CRYSTALS-Kyber und CRYSTALS-Dilithium (Versionen 3.1, 3 und älter) basieren, aber NICHT kompatibel damit sind.

### Schlüsselaustausch

PQ KEM bietet nur temporäre Schlüssel und unterstützt keine statischen Schlüssel-Handshakes wie Noise XK und IK direkt. Die Verschlüsselungstypen sind identisch mit denen im PQ Hybrid Ratchet und werden im Dokument zu gemeinsamen Strukturen [/docs/specs/common-structures/](/docs/specs/common-structures/) definiert, wie in [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf). Hybride Typen sind nur in Kombination mit X25519 definiert.

Die Verschlüsselungstypen sind:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NTCP2 Version</th>
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
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
</tr>
</table>
### Zulässige Kombinationen

Die neuen Verschlüsselungstypen werden in den RouterAddresses angezeigt. Der Verschlüsselungstyp im Schlüsselzertifikat bleibt Typ 4.

## Spezifikation

### Handshake-Muster

Die Handshakes verwenden [Noise Protocol](https://noiseprotocol.org/noise.html) Handshake-Muster.

Die folgende Buchstabenzuordnung wird verwendet:

- e = einmaliger temporärer Schlüssel
- s = statischer Schlüssel
- p = Nachrichtennutzlast
- e1 = einmaliger temporärer PQ-Schlüssel, gesendet von Alice an Bob
- ekem1 = der KEM-Chiffretext, gesendet von Bob an Alice

Die folgenden Änderungen an XK und IK für die hybride Vorwärtsgeheimhaltung (hfs) entsprechen den Vorgaben aus Abschnitt 5 der [Noise HFS-Spezifikation](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf):

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
Das e1-Muster ist wie folgt definiert, wie in Abschnitt 4 der [Noise HFS-Spezifikation](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) festgelegt:

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
Das ekem1-Muster ist wie folgt definiert, wie in Abschnitt 4 der [Noise HFS-Spezifikation](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) spezifiziert:

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
### Noise-Handshake-KDF

#### Übersicht

Der Hybrid-Handshake ist in der [Noise HFS-Spezifikation](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) definiert. Die erste Nachricht, von Alice an Bob, enthält e1, den Kapselungsschlüssel, vor dem Nachrichtennutzdaten. Dieser wird als zusätzlicher statischer Schlüssel behandelt; rufe EncryptAndHash() darauf auf (als Alice) oder DecryptAndHash() (als Bob). Danach werden die Nachrichtennutzdaten wie üblich verarbeitet.

Die zweite Nachricht von Bob an Alice enthält ekem1, den Chiffretext, vor der Nutzlast der Nachricht. Dies wird als zusätzlicher statischer Schlüssel behandelt; rufe EncryptAndHash() darauf auf (als Bob) bzw. DecryptAndHash() (als Alice). Danach wird der kem_shared_key berechnet und MixKey(kem_shared_key) aufgerufen. Anschließend wird die Nachrichtennutzlast wie üblich verarbeitet.

#### Definierte ML-KEM-Operationen

Wir definieren die folgenden Funktionen, die den verwendeten kryptografischen Bausteinen entsprechen, wie in [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) festgelegt.

(encap_key, decap_key) = PQ_KEYGEN()

    Alice creates the encapsulation and decapsulation keys
    The encapsulation key is sent in message 1.
    encap_key and decap_key sizes vary based on ML-KEM variant.

(Chiffrat, kem_shared_key) = ENCAPS(encap_key)

    Bob calculates the ciphertext and shared key,
    using the ciphertext received in message 1.
    The ciphertext is sent in message 2.
    ciphertext size varies based on ML-KEM variant.
    The kem_shared_key is always 32 bytes.

kem_shared_key = DECAPS(Ziffertext, decap_key)

    Alice calculates the shared key,
    using the ciphertext received in message 2.
    The kem_shared_key is always 32 bytes.

Beachten Sie, dass sowohl der encap_key als auch der Ciphertext innerhalb der ChaCha/Poly-Blöcke in den Noise-Handshake-Nachrichten 1 und 2 verschlüsselt sind. Sie werden im Rahmen des Handshake-Prozesses entschlüsselt.

Der kem_shared_key wird mit MixHash() in den Verkettungsschlüssel eingemischt. Siehe unten für Details.

#### Alice-KDF für Nachricht 1

Nach dem 'es'-Nachrichtenmuster und vor der Nutzlast hinzufügen:

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

Nach dem 'es'-Nachrichtenmuster und vor der Nutzlast hinzufügen:

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
#### Bob-KDF für Nachricht 2

Für XK: Fügen Sie nach dem 'ee'-Nachrichtenmuster und vor der Nutzlast Folgendes hinzu:

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
#### Alice-KDF für Nachricht 2

Fügen Sie nach dem Muster der Nachricht „ee“ Folgendes hinzu:

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
#### KDF für Nachricht 3 (nur XK)

unchanged

#### KDF für split()

unchanged

### Handshake-Details

#### Noise-Identifikatoren

- „Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256“
- „Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256“
- „Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM1024_ChaChaPoly_SHA256“

#### 1) SessionRequest

Änderungen: Das aktuelle NTCP2 enthält nur die Optionen in einem einzigen ChaCha-Abschnitt. Mit ML-KEM wird es einen neuen ChaCha-Abschnitt vor den Optionen geben, der den verschlüsselten Öffentlichen PQ-Schlüssel enthält.

Damit PQ- und Nicht-PQ-NTCP2-Verbindungen auf derselben Routeradresse und demselben Port unterstützt werden können, verwenden wir das höchstwertige Bit des X-Werts (X25519 ephemeraler öffentlicher Schlüssel), um anzugeben, dass es sich um eine PQ-Verbindung handelt. Dieses Bit ist für Nicht-PQ-Verbindungen immer deaktiviert.

Für Alice, nachdem die Nachricht durch Noise verschlüsselt wurde, aber vor der AES-Verfälschung von X, setze X[31] |= 0x7f.

Für Bob, nach der AES-Deobfuskation von X, teste X[31] & 0x80. Wenn das Bit gesetzt ist, lösche es mit X[31] &= 0x7f und entschlüssele via Noise als PQ-Verbindung. Wenn das Bit nicht gesetzt ist, entschlüssele via Noise wie üblich als Nicht-PQ-Verbindung.

Für PQ NTCP2, das auf einer anderen Routeradresse und einem anderen Port angeboten wird, ist dies nicht erforderlich.

Weitere Informationen finden Sie im Abschnitt „Veröffentlichte Adressen“ weiter unten.

Rohinhalte:

```
  +----+----+----+----+----+----+----+----+
  |        MS bit set to 1 and then       |
  +        obfuscated with RH_B           +
  |       AES-CBC-256 encrypted X         |
  +             (32 bytes)                +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaChaPoly encrypted data (MLKEM)   |
  +      (see table below for length)     +
  |   k defined in KDF for message 1      |
  +   n = 0                               +
  |   see KDF for associated data         |
  ~                                       ~
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (options)   |
  +         16 bytes                      +
  |   k defined in KDF for message 1      |
  +   n = 1                               +
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

  Same as current specification except add a second ChaChaPoly frame
```
Unverschlüsselte Daten (Poly1305-Authentifizierungstag nicht angezeigt):

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
  |           ML-KEM encap_key            |
  +      (see table below for length)     +
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
```
Hinweis: Das Versionsfeld im Optionsblock der Nachricht 1 muss auch für PQ-Verbindungen auf 2 gesetzt werden.

Größen:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">X len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Msg 1 len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Msg 1 Enc len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Msg 1 Dec len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">PQ key len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">opt len</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">64+pad</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">--</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">880+pad</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">848</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">816</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">800</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1264+pad</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1232</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1200</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1184</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1648+pad</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1616</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1584</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1568</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
</tr>
</table>
Hinweis: Typ-Codes sind nur für den internen Gebrauch. Router behalten den Typ 4, und die Unterstützung wird in den Router-Adressen angegeben.

#### 2) SessionCreated

Änderungen: Das aktuelle NTCP2 enthält nur die Optionen in einem einzelnen ChaCha-Abschnitt. Mit ML-KEM wird ein neuer ChaCha-Abschnitt vor den Optionen hinzugefügt, der den verschlüsselten PQ-Ciphertext enthält.

Rohinhalte:

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
  |   ChaCha20 encrypted data (MLKEM)     |
  -      (see table below for length)     -
  +   k defined in KDF for message 2      +
  |  (before mixKey)                      |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 encrypted data (options)   |
  -           16 bytes                    -
  +   k defined in KDF for message 2      +
  |  (after mixKey)                       |
  +  n = 0; see KDF for associated data   +
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

  Same as current specification except add a second ChaChaPoly frame
```
Unverschlüsselte Daten (Poly1305-Authentifizierungstag nicht angezeigt):

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
  |           ML-KEM Ciphertext           |
  +      (see table below for length)     +
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
```
Größen:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Y len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Msg 2 len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Msg 2 Enc len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Msg 2 Dec len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">PQ CT len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">opt len</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">64+pad</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">--</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">848+pad</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">816</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">784</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">768</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1168+pad</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1136</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1104</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1088</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1648+pad</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1616</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1584</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1568</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
</tr>
</table>
Hinweis: Typ-Codes sind nur für den internen Gebrauch. Router behalten den Typ 4, und die Unterstützung wird in den Router-Adressen angegeben.

#### 3) SessionConfirmed

Unverändert

#### Schlüsselableitungsfunktion (KDF) (für die Datenphase)

Unverändert

#### Veröffentlichte Adressen

Verwenden Sie in allen Fällen den NTCP2-Transportnamen wie gewohnt.

Verwenden Sie dieselbe Adresse/denselben Port wie bei nicht-PQ, nicht-firewalled. Nur eine PQ-Variante wird unterstützt. In der Router-Adresse veröffentlichen Sie v=2 (wie üblich) und den neuen Parameter pq=[3|4|5], um MLKEM 512/768/1024 anzugeben. Alice setzt das MSB des temporären Schlüssels (key[31] & 0x80) in der Sitzungsanfrage, um anzugeben, dass es sich um eine hybride Verbindung handelt. Siehe oben. Ältere Router werden den pq-Parameter ignorieren und wie gewohnt nicht-pq verbinden.

Unterschiedliche Adressen/Ports für nicht-PQ, oder nur PQ, nicht hinter einer Firewall, werden NICHT unterstützt. Dies wird nicht implementiert, bis nicht-PQ NTCP2 deaktiviert ist, was erst in mehreren Jahren der Fall sein wird. Wenn nicht-PQ deaktiviert ist, könnten mehrere PQ-Varianten unterstützt werden, jedoch nur eine pro Adresse. Sobald dies unterstützt wird, muss in der Routeradresse v=[3|4|5] veröffentlicht werden, um MLKEM 512/768/1024 anzugeben. Alice setzt das MSB des ephemeren Schlüssels nicht. Ältere Router prüfen den v-Parameter und überspringen diese Adresse als nicht unterstützte Variante.

Gefeuwalled-Adressen (keine IP veröffentlicht): In der Routeradresse v=2 veröffentlichen (wie üblich). Es ist nicht notwendig, einen pq-Parameter zu veröffentlichen.

Alice kann sich mit einem PQ-Bob über die PQ-Variante verbinden, die Bob veröffentlicht, unabhängig davon, ob Alice PQ-Unterstützung in ihren Router-Infos annonciert oder ob sie dieselbe Variante annonciert.

#### Maximale Auffüllung

In der aktuellen Spezifikation ist für die Nachrichten 1 und 2 eine „angemessene“ Menge an Auffüllung (Padding) vorgesehen, wobei ein Bereich von 0–31 Bytes empfohlen wird, ohne dass ein Maximum festgelegt ist.

Bis API 0.9.68 (Release 2.11.0) implementierte Java I2P eine maximale Auffüllung von 256 Bytes für Nicht-PQ-Verbindungen, was jedoch zuvor nicht dokumentiert war. Ab API 0.9.69 (Release 2.12.0) implementiert Java I2P dieselbe maximale Auffüllung für Nicht-PQ-Verbindungen wie für MLKEM-512. Siehe Tabelle unten.

Verwenden Sie die definierte Nachrichtengröße als maximale Auffüllung, das heißt, die maximale Auffüllung verdoppelt die Nachrichtengröße für PQ-Verbindungen, wie folgt:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Message Max Padding</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">non-PQ (thru 0.9.68)</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">non-PQ (as of 0.9.69)</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">MLKEM-512</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">MLKEM-768</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">MLKEM-1024</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Session Request</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">256</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">880</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">880</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1264</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1648</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Session Created</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">256</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">848</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">848</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1168</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1648</td>
</tr>
</table>
## Analyse der Overhead-Kosten

### Schlüsselaustausch

Größenanstieg (Bytes):

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
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+1584</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+1584</td>
</tr>
</table>
## Sicherheitsanalyse

Die NIST-Sicherheitskategorien sind in [NIST-Präsentation](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf), Folie 10, zusammengefasst. Vorläufige Kriterien: Unsere minimale NIST-Sicherheitskategorie sollte bei Hybridprotokollen 2 und bei reinen PQ-Protokollen 3 betragen.

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
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
</tr>
</table>
## Implementierungshinweise

### Bibliotheksunterstützung

Die Bibliotheken Bouncycastle, BoringSSL und WolfSSL unterstützen jetzt MLKEM und MLDSA. Die Unterstützung durch OpenSSL wird im Release 3.5 am 8. April 2025 erfolgen [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

### Identifizierung eingehenden Datenverkehrs

Wir setzen das MSB des temporären Schlüssels (key[31] & 0x80) im Sitzungsanfragepaket, um anzugeben, dass es sich um eine hybride Verbindung handelt. Dies ermöglicht es uns, sowohl standardmäßiges NTCP als auch hybrides NTCP am selben Port zu betreiben. Für eingehende Verbindungen wird nur eine hybride Variante unterstützt und in der Routeradresse angekündigt. Zum Beispiel pq=3 oder pq=4.

#### Verschleierung

Als Alice, für eine PQ-Verbindung, vor der Verschleierung, setze X[31] |= 0x80. Dadurch wird X ein ungültiger X25519-Öffentlicher Schlüssel. Nach der Verschleierung wird AES-CBC diesen Wert randomisieren. Das MSB von X wird nach der Verschleierung zufällig sein.

Als Bob testen, ob (X[31] & 0x80) != 0 nach der De-Verfälschung gilt. Wenn ja, handelt es sich um eine PQ-Verbindung.

Die minimale Router-Version, die für NTCP2-PQ erforderlich ist, steht noch aus (TBD).

Hinweis: Typ-Codes sind nur für den internen Gebrauch. Router behalten den Typ 4, und die Unterstützung wird in den Router-Adressen angegeben.

## Router-Kompatibilität

### Transportnamen

Verwenden Sie in allen Fällen wie gewohnt den NTCP2-Transportnamen. Ältere Router werden den pq-Parameter ignorieren und wie üblich mit standardmäßigem NTCP2 eine Verbindung herstellen.

## Referenzen

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
