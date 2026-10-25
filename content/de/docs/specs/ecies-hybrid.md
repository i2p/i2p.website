---
title: "PQ Hybrid ECIES-X25519-AEAD-Ratchet"
description: "Post-Quanten-Hybrid-Variante des ECIES-Verschlüsselungsprotokolls mit ML-KEM"
slug: "ecies-hybrid"
category: "Protokolle"
lastUpdated: "2026-04"
accurateFor: "0.9.69"
---

## Hinweis

Implementierung, Tests und Einführung sind in den verschiedenen router-Implementierungen im Gange. Überprüfen Sie die Dokumentation dieser Implementierungen für den aktuellen Status.

## Übersicht

Dies ist die PQ-Hybrid-Variante des ECIES-X25519-AEAD-Ratchet-Protokolls [ECIES](/docs/specs/ecies/). Es ist die erste Phase des gesamten PQ-Vorschlags [Prop169](/proposals/169-pq-crypto/), die genehmigt wurde. Siehe diesen Vorschlag für übergeordnete Ziele, Bedrohungsmodelle, Analysen, Alternativen und zusätzliche Informationen.

Diese Spezifikation enthält nur die Unterschiede zum Standard-[ECIES](/docs/specs/ecies/) und muss in Verbindung mit dieser Spezifikation gelesen werden.

## Design

Wir unterstützen den NIST FIPS 203-Standard [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf), der auf CRYSTALS-Kyber basiert, aber NICHT damit kompatibel ist.

Hybrid-Handshakes sind wie in [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) spezifiziert.

### Schlüsselaustausch

Wir definieren einen hybriden Schlüsselaustausch für Ratchet. PQ KEM stellt nur ephemere Schlüssel bereit und unterstützt nicht direkt statische Schlüssel-Handshakes wie Noise IK.

Wir definieren die drei ML-KEM-Varianten wie in [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf), für insgesamt 3 neue Verschlüsselungstypen. Hybride Typen sind nur in Kombination mit X25519 definiert.

Die neuen Verschlüsselungsarten sind:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Code</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
</tr>
</table>
Der Overhead wird erheblich sein. Typische Nachrichten-1- und -2-Größen (für IK) betragen derzeit etwa 100 Bytes (vor zusätzlicher Nutzlast). Dies wird sich je nach Algorithmus um das 8- bis 15-fache erhöhen.

### Neue Kryptographie erforderlich

- ML-KEM (früher CRYSTALS-Kyber) [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
- SHA3-128 (früher Keccak-256) [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf) Nur für SHAKE128 verwendet
- SHA3-256 (früher Keccak-512) [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
- SHAKE128 und SHAKE256 (XOF-Erweiterungen zu SHA3-128 und SHA3-256)
  [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)

Testvektoren für SHA3-256, SHAKE128 und SHAKE256 finden Sie unter [NIST-VECTORS](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values).

Beachten Sie, dass die Java bouncycastle-Bibliothek alle oben genannten unterstützt. C++-Bibliotheksunterstützung ist in OpenSSL 3.5 [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/) verfügbar.

## Spezifikation

### Allgemeine Strukturen

Siehe die Spezifikation für gemeinsame Strukturen [COMMON](/docs/specs/common-structures/) für Schlüssellängen und Identifikatoren.

### Handshake-Muster

Handshakes verwenden [Noise](https://noiseprotocol.org/noise.html) Handshake-Muster.

Die folgende Buchstabenzuordnung wird verwendet:

- e = einmaliger ephemerer Schlüssel
- s = statischer Schlüssel
- p = Nachrichtennutzlast
- e1 = einmaliger ephemerer PQ-Schlüssel, von Alice an Bob gesendet
- ekem1 = der KEM-Chiffretext, von Bob an Alice gesendet

Die folgenden Modifikationen von XK und IK für hybride Vorwärtssicherheit (hfs) sind wie in [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) Abschnitt 5 spezifiziert:

```
IK:                         IKhfs:
<- s                        <- s
...                         ...
-> e, es, s, ss, p          -> e, es, e1, s, ss, p
<- tag, e, ee, se, p        <- tag, e, ee, ekem1, se, p
<- p                        <- p
p ->                        p ->

e1 and ekem1 are encrypted. See pattern definitions below.
NOTE: e1 and ekem1 are different sizes (unlike X25519)
```
Das e1-Muster ist wie folgt definiert, wie in [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) Abschnitt 4 spezifiziert:

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
Das ekem1-Muster ist wie folgt definiert, wie in [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) Abschnitt 4 spezifiziert:

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
### Definierte ML-KEM-Operationen

Wir definieren die folgenden Funktionen, die den kryptographischen Bausteinen entsprechen, die wie in [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) definiert verwendet werden.

**(encap_key, decap_key) = PQ_KEYGEN()**

Alice erstellt die Verkapselungs- und Entkapselungsschlüssel. Der Verkapselungsschlüssel wird in der NS-Nachricht gesendet. Die Größen von encap_key und decap_key variieren je nach ML-KEM-Variante.

**(ciphertext, kem_shared_key) = ENCAPS(encap_key)**

Bob berechnet den Chiffretext und den gemeinsamen Schlüssel, wobei er den in der NS-Nachricht empfangenen Chiffretext verwendet. Der Chiffretext wird in der NSR-Nachricht gesendet. Die Chiffretext-Größe variiert je nach ML-KEM-Variante. Der kem_shared_key ist immer 32 Bytes.

**kem_shared_key = DECAPS(ciphertext, decap_key)**

Alice berechnet den geteilten Schlüssel unter Verwendung des Chiffretexts, der in der NSR-Nachricht empfangen wurde. Der kem_shared_key ist immer 32 Bytes lang.

Beachten Sie, dass sowohl der encap_key als auch der ciphertext innerhalb von ChaCha/Poly-Blöcken in den Noise-Handshake-Nachrichten 1 und 2 verschlüsselt sind. Sie werden als Teil des Handshake-Prozesses entschlüsselt.

Der kem_shared_key wird mit MixHash() in den Verkettungsschlüssel eingemischt. Siehe unten für Details.

### Noise Handshake KDF

#### Übersicht

Der Hybrid-Handshake ist in [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) definiert. Die erste Nachricht von Alice an Bob enthält e1, den Verkapselungsschlüssel, vor der Nachrichtnutzlast. Dieser wird als zusätzlicher statischer Schlüssel behandelt; rufen Sie EncryptAndHash() darauf auf (als Alice) oder DecryptAndHash() (als Bob). Verarbeiten Sie dann die Nachrichtnutzlast wie gewohnt.

Die zweite Nachricht von Bob an Alice enthält ekem1, den Chiffretext, vor der Nachrichtennutzlast. Dies wird als zusätzlicher statischer Schlüssel behandelt; rufe EncryptAndHash() darauf auf (als Bob) oder DecryptAndHash() (als Alice). Berechne dann den kem_shared_key und rufe MixKey(kem_shared_key) auf. Verarbeite dann die Nachrichtennutzlast wie gewohnt.

#### Noise-Kennungen

Dies sind die Noise-Initialisierungsstrings:

- "Noise_IKhfselg2_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM1024_ChaChaPoly_SHA256"

#### Alice KDF für NS-Nachricht

Nach dem 'es' Nachrichtenmuster und vor dem 's' Nachrichtenmuster hinzufügen:

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

NOTE: For the next section (static key for IK),
the keydata and chain key remain the same, and n now equals 1
(instead of 0 for non-hybrid).
```
#### Bob KDF für NS-Nachricht

Nach dem 'es' Nachrichtenmuster und vor dem 's' Nachrichtenmuster, fügen Sie hinzu:

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

NOTE: For the next section (static key for IK),
the keydata and chain key remain the same, and n now equals 1
(instead of 0 for non-hybrid).
```
#### Bob KDF für NSR-Nachricht

Nach dem 'ee' Nachrichtenmuster und vor dem 'se' Nachrichtenmuster hinzufügen:

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
```
#### Alice KDF für NSR-Nachricht

Nach dem 'ee' Nachrichtenmuster und vor dem 'ss' Nachrichtenmuster hinzufügen:

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
```
#### KDF für split()

unverändert

### Nachrichtenformat

#### NS-Format

Änderungen: Der aktuelle ratchet enthielt den statischen Schlüssel im ersten ChaCha-Abschnitt und die Nutzlast im zweiten Abschnitt. Mit ML-KEM gibt es nun drei Abschnitte. Der erste Abschnitt enthält den verschlüsselten PQ-Public-Key. Der zweite Abschnitt enthält den statischen Schlüssel. Der dritte Abschnitt enthält die Nutzlast.

Verschlüsseltes Format:

```
+----+----+----+----+----+----+----+----+
|                                       |
+         New Session Ephemeral         +
|            Public Key                 |
+            32 bytes                   +
|      Encoded with Elligator2          |
+----+----+----+----+----+----+----+----+
|                                       |
+         ML-KEM encap_key              +
|       ChaCha20 encrypted data         |
+   (see table below for length)        +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+      (MAC) for encap_key Section      +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
|                                       |
+         X25519 Static Key             +
|       ChaCha20 encrypted data         |
+            32 bytes                   +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+     (MAC) for Static Key Section      +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
|                                       |
+          Payload Section              +
|       ChaCha20 encrypted data         |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+      (MAC) for Payload Section        +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
```
Entschlüsseltes Format:

```
Payload Part 1:

+----+----+----+----+----+----+----+----+
|                                       |
+         ML-KEM encap_key              +
|                                       |
+   (see table below for length)        +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

Payload Part 2:

+----+----+----+----+----+----+----+----+
|                                       |
+         X25519 Static Key             +
|            (32 bytes)                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

Payload Part 3:

+----+----+----+----+----+----+----+----+
|                                       |
+          Payload Section              +
|                                       |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
Größen:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">X len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NS len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NS Enc len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NS Dec len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">PQ key len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">pl len</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">96+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">64+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">--</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">912+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">880+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">800+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">800</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1296+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1360+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1184+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1184</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1680+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1648+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1568+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1568</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
</table>
Beachte, dass die Nutzlast einen DateTime-Block enthalten muss, sodass die minimale Nutzlastgröße 7 beträgt. Die minimalen NS-Größen können entsprechend berechnet werden.

#### NSR-Format

Änderungen: Der aktuelle ratchet hat eine leere Nutzlast für den ersten ChaCha-Abschnitt und die Nutzlast im zweiten Abschnitt. Mit ML-KEM gibt es nun drei Abschnitte. Der erste Abschnitt enthält den verschlüsselten PQ-Geheimtext. Der zweite Abschnitt hat eine leere Nutzlast. Der dritte Abschnitt enthält die Nutzlast.

Verschlüsseltes Format:

```
+----+----+----+----+----+----+----+----+
|       Session Tag 8 bytes             |
+----+----+----+----+----+----+----+----+
|                                       |
+       Ephemeral Public Key            +
|            32 bytes                   |
+      Encoded with Elligator2          +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+         ML-KEM ciphertext             +
|       ChaCha20 encrypted data         |
+   (see table below for length)        +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+     (MAC) for ciphertext Section      +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+   (MAC) for key Section (no data)     +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
|                                       |
+          Payload Section              +
|       ChaCha20 encrypted data         |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+      (MAC) for Payload Section        +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
```
Entschlüsseltes Format:

```
Payload Part 1:

+----+----+----+----+----+----+----+----+
|                                       |
+         ML-KEM ciphertext             +
|                                       |
+   (see table below for length)        +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

Payload Part 2:

empty

Payload Part 3:

+----+----+----+----+----+----+----+----+
|                                       |
+          Payload Section              +
|                                       |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
Größen:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Y len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NSR len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NSR Enc len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NSR Dec len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">PQ CT len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">opt len</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">72+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">--</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">856+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">816+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">768+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">768</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1176+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1136+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1088+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1088</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1656+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1616+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1568+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1568</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
</table>
Beachte, dass NSR normalerweise eine Nutzlast ungleich null haben wird, die Ratchet-Spezifikation [ECIES](/docs/specs/ecies/) erfordert dies jedoch nicht, daher beträgt die minimale Nutzlastgröße 0. Die minimalen NSR-Größen können entsprechend berechnet werden.

## Overhead-Analyse

### Schlüsselaustausch

Größenzunahme (Bytes):

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Pubkey (NS)</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Ciphertext (NSR)</th>
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
Geschwindigkeit:

Geschwindigkeiten wie von [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/) berichtet:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Relative speed</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">X25519 DH/keygen</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">baseline</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2.25x faster</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1.5x faster</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1x (same)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">XK</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4x DH (keygen + 3 DH)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4x DH + 2x PQ (keygen + enc/dec) = 4.9x DH = 22% slower</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4x DH + 2x PQ (keygen + enc/dec) = 5.3x DH = 32% slower</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4x DH + 2x PQ (keygen + enc/dec) = 6x DH = 50% slower</td>
</tr>
</table>
## Sicherheitsanalyse

NIST-Sicherheitskategorien sind in [NIST-PQ-END](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf) Folie 10 zusammengefasst. Vorläufige Kriterien: Unsere minimale NIST-Sicherheitskategorie sollte 2 für Hybridprotokolle und 3 für reine PQ-Protokolle sein.

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

Das sind alles Hybridprotokolle. Wahrscheinlich sollte MLKEM768 bevorzugt werden; MLKEM512 ist nicht sicher genug.

NIST-Sicherheitskategorien [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf):

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
## Typ-Einstellungen

Der empfohlene Typ für die anfängliche Unterstützung, basierend auf Sicherheitskategorie und Schlüssellänge, ist:

MLKEM768_X25519 (Typ 6)

## Implementierungshinweise

### Bibliotheksunterstützung

Bouncycastle, BoringSSL und WolfSSL-Bibliotheken unterstützen jetzt MLKEM. OpenSSL-Unterstützung ist in ihrer Version 3.5 vom 8. April 2025 [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

### Geteilte Tunnels

Die automatische Klassifizierung/Erkennung mehrerer Protokolle in denselben tunnels sollte basierend auf einer Längenprüfung von Nachricht 1 (New Session Message) möglich sein. Am Beispiel von MLKEM512_X25519 ist Nachricht 1 um 816 Bytes größer als beim aktuellen ratchet-Protokoll, und die minimale Größe von Nachricht 1 (mit nur einer DateTime-Payload) beträgt 919 Bytes. Die meisten Nachricht-1-Größen beim aktuellen ratchet haben eine Payload von weniger als 816 Bytes, sodass sie als nicht-hybrid ratchet klassifiziert werden können. Große Nachrichten sind wahrscheinlich POSTs, die selten vorkommen.

Die empfohlene Strategie ist daher:

- Wenn Nachricht 1 weniger als 919 Bytes hat, ist es das aktuelle ratchet
  Protokoll.
- Wenn Nachricht 1 größer oder gleich 919 Bytes ist, ist es wahrscheinlich
  MLKEM512_X25519. Versuche zuerst MLKEM512_X25519, und wenn es fehlschlägt, versuche das
  aktuelle ratchet Protokoll.

Dies sollte es uns ermöglichen, Standard-Ratchet und Hybrid-Ratchet effizient auf derselben Destination zu unterstützen, genau wie wir zuvor ElGamal und Ratchet auf derselben Destination unterstützt haben. Daher können wir viel schneller zum MLKEM-Hybrid-Protokoll migrieren, als wenn wir keine Dual-Protokolle für dieselbe Destination unterstützen könnten, weil wir MLKEM-Unterstützung zu bestehenden Destinations hinzufügen können.

Die erforderlichen unterstützten Kombinationen sind:

- X25519 + MLKEM512
- X25519 + MLKEM768
- X25519 + MLKEM1024

Die folgenden Kombinationen können komplex sein und müssen NICHT unterstützt werden, können aber implementierungsabhängig unterstützt werden:

- Mehr als ein MLKEM
- ElG + ein oder mehrere MLKEM
- X25519 + ein oder mehrere MLKEM
- ElG + X25519 + ein oder mehrere MLKEM

Es ist nicht erforderlich, mehrere MLKEM-Algorithmen (zum Beispiel MLKEM512_X25519 und MLKEM_768_X25519) auf demselben Ziel zu unterstützen. Wählen Sie nur einen aus. Implementierungsabhängig.

Es ist nicht erforderlich, drei Algorithmen (zum Beispiel X25519, MLKEM512_X25519 und MLKEM769_X25519) auf derselben Destination zu unterstützen. Die Klassifizierung und Wiederholungsstrategie könnte zu komplex werden. Die Konfiguration und Konfigurationsoberfläche könnte zu komplex werden. Implementierungsabhängig.

Es ist nicht erforderlich, ElGamal- und Hybrid-Algorithmen auf demselben Ziel zu unterstützen. ElGamal ist veraltet, und ElGamal + Hybrid allein (ohne X25519) ergibt nicht viel Sinn. Außerdem sind sowohl ElGamal- als auch Hybrid New Session Messages groß, sodass Klassifizierungsstrategien oft beide Entschlüsselungen versuchen müssten, was ineffizient wäre. Implementierungsabhängig.

Clients können dieselben oder unterschiedliche statische X25519-Schlüssel für die X25519- und Hybrid-Protokolle auf denselben Tunneln verwenden, implementierungsabhängig.

### Forward Secrecy

Die ECIES-Spezifikation erlaubt Garlic Messages im New Session Message Payload, was die 0-RTT-Übertragung des ersten Streaming-Pakets, normalerweise eines HTTP GET, zusammen mit dem leaseSet des Clients ermöglicht. Allerdings hat der New Session Message Payload keine Forward Secrecy. Da dieser Vorschlag die verbesserte Forward Secrecy für Ratchet betont, können oder sollten Implementierungen die Einbeziehung des Streaming-Payloads oder der vollständigen Streaming-Nachricht bis zur ersten Existing Session Message zurückstellen. Dies würde auf Kosten der 0-RTT-Übertragung gehen. Strategien können auch vom Verkehrstyp oder tunnel-Typ abhängen, oder zum Beispiel von GET vs. POST. Implementierungsabhängig.

### Neue Sitzungsgröße

MLKEM wird die Größe der New Session Message dramatisch erhöhen, wie oben beschrieben. Dies kann die Zuverlässigkeit der Zustellung von New Session Messages durch tunnel erheblich verringern, wo sie in mehrere 1024-Byte-tunnel-Nachrichten fragmentiert werden müssen. Der Zustellungserfolg ist proportional zur exponentiellen Anzahl der Fragmente. Implementierungen können verschiedene Strategien verwenden, um die Größe der Nachricht zu begrenzen, auf Kosten der 0-RTT-Zustellung. Implementierungsabhängig.

## Referenzen

- [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/)
- [COMMON](/docs/specs/common-structures/)
- [ECIES](/docs/specs/ecies/)
- [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
- [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
- [FORUM](http://zzz.i2p/topics/3294)
- [NIST-PQ-END](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf)
- [NIST-VECTORS](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values)
- [Noise](https://noiseprotocol.org/noise.html)
- [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf)
- [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)
- [PQ-WIREGUARD](https://eprint.iacr.org/2020/379.pdf)
- [Prop169](/proposals/169-pq-crypto/)
