---
title: "Hybride Verschlüsselung mit ECIES-X25519-AEAD-Ratchet"
description: "Post-Quanten-hybride Variante des Verschlüsselungsprotokolls ECIES (integriertes Verschlüsselungsverfahren mit elliptischen Kurven) unter Verwendung von ML-KEM (Modul-Gitter-basiertes Schlüsselkapselungsverfahren)"
slug: "ecies-hybrid"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Implementierungsstatus

**Aktuelle Bereitstellung:** - **i2pd (C++-Implementierung)**: Vollständig implementiert in Version 2.58.0 (September 2025) mit Unterstützung für ML-KEM-512, ML-KEM-768 und ML-KEM-1024. Post-Quanten-Ende-zu-Ende-Verschlüsselung ist standardmäßig aktiviert, wenn OpenSSL 3.5.0 oder neuer verfügbar ist. - **Java I2P**: Bis Version 0.9.67 / 2.10.0 (September 2025) noch nicht implementiert. Spezifikation genehmigt und Implementierung für zukünftige Versionen geplant.

Diese Spezifikation beschreibt freigegebene Funktionalität, die derzeit in i2pd eingesetzt ist und für Java I2P-Implementierungen geplant ist.

## Übersicht

Dies ist die Post-Quanten-Hybridvariante des Protokolls ECIES-X25519-AEAD-Ratchet [ECIES](/docs/specs/ecies/). Sie stellt die erste zu genehmigende Phase von Vorschlag 169 [Prop169](/proposals/169-pq-crypto/) dar. Siehe diesen Vorschlag für übergeordnete Ziele, Bedrohungsmodelle, Analysen, Alternativen und zusätzliche Informationen.

Status von Vorschlag 169: **Offen** (erste Phase für hybride ECIES (Elliptic Curve Integrated Encryption Scheme, integriertes Verschlüsselungsverfahren mit elliptischen Kurven)-Implementierung genehmigt).

Diese Spezifikation enthält nur die Unterschiede zum Standard [ECIES](/docs/specs/ecies/) und muss in Verbindung mit jener Spezifikation gelesen werden.

## Entwurf

Wir verwenden den NIST FIPS 203-Standard [FIPS203](https://csrc.nist.gov/pubs/fips/203/final), der zwar auf CRYSTALS-Kyber basiert, jedoch nicht damit kompatibel ist (Versionen 3.1, 3 und älter).

Hybride Handshakes kombinieren klassisches X25519-Diffie-Hellman mit Post-Quanten-Schlüsselkapselungsmechanismen (ML-KEM). Dieser Ansatz basiert auf Konzepten hybrider Vorwärtsgeheimhaltung, die in der PQNoise-Forschung dokumentiert sind, sowie auf ähnlichen Implementierungen in TLS 1.3, IKEv2 und WireGuard.

### Schlüsselaustausch

Wir definieren einen hybriden Schlüsselaustausch für Ratchet (kryptographisches Ratchet-Protokoll).
Ein Post-Quanten-Schlüsselkapselungsverfahren (KEM) liefert nur ephemere Schlüssel und unterstützt Handshakes mit statischen Schlüsseln wie Noise IK nicht direkt.

Wir definieren die drei ML-KEM-Varianten wie in [FIPS203](https://csrc.nist.gov/pubs/fips/203/final) spezifiziert, woraus sich insgesamt drei neue Verschlüsselungstypen ergeben. Hybridtypen sind nur in Kombination mit X25519 definiert.

Die neuen Verschlüsselungstypen sind:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Security Level</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">ML-KEM Variant</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NIST Category 1 (AES-128 equivalent)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ML-KEM-512</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NIST Category 3 (AES-192 equivalent)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ML-KEM-768 (Recommended)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NIST Category 5 (AES-256 equivalent)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ML-KEM-1024</td>
    </tr>
  </tbody>
</table>
**Hinweis:** MLKEM768_X25519 (Typ 6) ist die empfohlene Standardvariante, die starke Post-Quanten-Sicherheit bei angemessenem Mehraufwand bietet.

Der Overhead ist im Vergleich zur ausschließlich mit X25519 erfolgenden Verschlüsselung erheblich. Die typischen Größen der Nachrichten 1 und 2 (für IK pattern (Noise‑Protokollmuster IK)) liegen derzeit bei etwa 96-103 Bytes (vor zusätzlicher Nutzlast). Dies erhöht sich je nach Nachrichtentyp um etwa das 9- bis 12‑Fache für MLKEM512 (post‑quantenfähiges Schlüsselkapselungsverfahren), das 13- bis 16‑Fache für MLKEM768 und das 17- bis 23‑Fache für MLKEM1024.

### Neue Kryptografie erforderlich

- **ML-KEM** (früher CRYSTALS-Kyber) [FIPS203](https://csrc.nist.gov/pubs/fips/203/final) - Standard für modulgitterbasierte Key-Encapsulation Mechanisms (Schlüsselkapselungsmechanismen)
- **SHA3-256** (früher Keccak-512) [FIPS202](https://csrc.nist.gov/pubs/fips/202/final) - Teil des SHA-3-Standards
- **SHAKE128 und SHAKE256** (XOF-Erweiterungen für SHA3) [FIPS202](https://csrc.nist.gov/pubs/fips/202/final) - Erweiterbare Ausgabefunktionen

Testvektoren für SHA3-256, SHAKE128 und SHAKE256 sind im [NIST Cryptographic Algorithm Validation Program](https://csrc.nist.gov/Projects/cryptographic-algorithm-validation-program) verfügbar.

**Bibliotheksunterstützung:** - Java: Bouncycastle-Bibliothek Version 1.79 und höher unterstützt alle ML-KEM-Varianten und SHA3/SHAKE-Funktionen - C++: OpenSSL 3.5 und höher enthält vollständige ML-KEM-Unterstützung (veröffentlicht im April 2025) - Go: Mehrere Bibliotheken sind für die Implementierung von ML-KEM und SHA3 verfügbar

## Spezifikation

### Allgemeine Strukturen

Siehe die [Common Structures Specification](/docs/specs/common-structures/) für Schlüssellängen und Bezeichner.

### Handshake-Muster

Handshakes verwenden [Noise Protocol Framework](https://noiseprotocol.org/noise.html) Handshake-Muster mit I2P-spezifischen Anpassungen für hybride Post-Quanten-Sicherheit.

Die folgende Zuordnung der Buchstaben wird verwendet:

- **e** = einmaliger ephemerer Schlüssel (X25519)
- **s** = statischer Schlüssel
- **p** = Nutzlast der Nachricht
- **e1** = einmaliger ephemerer PQ-Schlüssel, von Alice an Bob gesendet (I2P-spezifisches Token)
- **ekem1** = das KEM-Chiffrat, von Bob an Alice gesendet (I2P-spezifisches Token)

**Wichtiger Hinweis:** Die Musternamen "IKhfs" und "IKhfselg2" sowie die Token "e1" und "ekem1" sind I2P-spezifische Anpassungen, die in der offiziellen Spezifikation des Noise Protocol Frameworks nicht dokumentiert sind. Diese stellen eigene Definitionen zur Integration von ML-KEM in das Noise-IK-Muster dar. Während der hybride Ansatz X25519 + ML-KEM in der Forschung zur Post-Quanten-Kryptografie und in anderen Protokollen weithin anerkannt ist, ist die hier verwendete spezifische Nomenklatur I2P-spezifisch.

Die folgenden Änderungen an IK für hybrides Vorwärtsgeheimnis werden angewendet:

```
Standard IK:              I2P IKhfs (Hybrid):
<- s                      <- s
...                       ...
-> e, es, s, ss, p        -> e, es, e1, s, ss, p
<- e, ee, se, p           <- e, ee, ekem1, se, p
<- p                      <- p
p ->                      p ->

Note: e1 and ekem1 are encrypted within ChaCha20-Poly1305 AEAD blocks.
Note: e1 (ML-KEM public key) and ekem1 (ML-KEM ciphertext) have different sizes.
```
Das **e1**-Muster ist wie folgt definiert:

```
For Alice (sender):
(encap_key, decap_key) = PQ_KEYGEN()

// EncryptAndHash(encap_key)
ciphertext = ENCRYPT(k, n, encap_key, ad)
n++
MixHash(ciphertext)

For Bob (receiver):
// DecryptAndHash(ciphertext)
encap_key = DECRYPT(k, n, ciphertext, ad)
n++
MixHash(ciphertext)
```
Das **ekem1**-Muster ist wie folgt definiert:

```
For Bob (receiver of encap_key):
(kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

// EncryptAndHash(kem_ciphertext)
ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)
MixHash(ciphertext)

// MixKey
MixKey(kem_shared_key)

For Alice (sender of encap_key):
// DecryptAndHash(ciphertext)
kem_ciphertext = DECRYPT(k, n, ciphertext, ad)
MixHash(ciphertext)

// MixKey
kem_shared_key = DECAPS(kem_ciphertext, decap_key)
MixKey(kem_shared_key)
```
### Definierte ML-KEM-Operationen

Wir definieren die folgenden Funktionen, die den kryptografischen Bausteinen entsprechen, wie in [FIPS203](https://csrc.nist.gov/pubs/fips/203/final) spezifiziert.

**(encap_key, decap_key) = PQ_KEYGEN()** : Alice generiert die Kapselungs- und Entkapselungsschlüssel. Der Kapselungsschlüssel wird in der NS-Nachricht übermittelt. Schlüsselgrößen:   - ML-KEM-512: encap_key = 800 Bytes, decap_key = 1632 Bytes   - ML-KEM-768: encap_key = 1184 Bytes, decap_key = 2400 Bytes   - ML-KEM-1024: encap_key = 1568 Bytes, decap_key = 3168 Bytes

**(ciphertext, kem_shared_key) = ENCAPS(encap_key)** : Bob berechnet das Chiffrat und den gemeinsamen Schlüssel unter Verwendung des in der NS-Nachricht empfangenen Kapselungsschlüssels. Das Chiffrat wird in der NSR-Nachricht gesendet. Chiffratgrößen:   - ML-KEM-512: 768 Bytes   - ML-KEM-768: 1088 Bytes   - ML-KEM-1024: 1568 Bytes

kem_shared_key ist bei allen drei Varianten immer **32 Byte** groß.

**kem_shared_key = DECAPS(ciphertext, decap_key)** : Alice berechnet den gemeinsamen Schlüssel mithilfe des in der NSR-Nachricht empfangenen Chiffrats. Der kem_shared_key ist immer **32 Bytes**.

**Wichtig:** Sowohl der encap_key als auch das Chiffrat sind innerhalb von ChaCha20-Poly1305-Blöcken in den Noise-Handshake-Nachrichten 1 und 2 verschlüsselt. Sie werden im Rahmen des Handshake-Prozesses entschlüsselt.

Der kem_shared_key wird mit MixKey() in den Verkettungsschlüssel eingemischt. Siehe unten für Details.

### KDF (Schlüsselableitungsfunktion) des Noise-Handshakes

#### Übersicht

Der hybride Handshake kombiniert klassisches X25519-ECDH mit Post-Quanten-ML-KEM. Die erste Nachricht, von Alice an Bob, enthält e1 (den ML-KEM-Kapselungsschlüssel) vor der Nutzlast der Nachricht. Dies wird als zusätzliches Schlüsselmaterial behandelt; führen Sie EncryptAndHash() darauf aus (als Alice) oder DecryptAndHash() (als Bob). Verarbeiten Sie anschließend die Nutzlast der Nachricht wie üblich.

Die zweite Nachricht, von Bob an Alice, enthält ekem1 (den ML-KEM-Chiffretext) vor dem Nachrichteninhalt. Dies wird als zusätzliches Schlüsselmaterial behandelt; rufe EncryptAndHash() darauf auf (als Bob) bzw. DecryptAndHash() (als Alice). Berechne dann den kem_shared_key und rufe MixKey(kem_shared_key) auf. Anschließend den Nachrichteninhalt wie üblich verarbeiten.

#### Noise (Protokoll-Framework)-Kennungen

Dies sind die Initialisierungs-Strings von Noise (Kryptografieprotokoll) (I2P-spezifisch):

- `Noise_IKhfselg2_25519+MLKEM512_ChaChaPoly_SHA256`
- `Noise_IKhfselg2_25519+MLKEM768_ChaChaPoly_SHA256`
- `Noise_IKhfselg2_25519+MLKEM1024_ChaChaPoly_SHA256`

#### Alice-KDF für NS-Nachricht

Fügen Sie nach dem Nachrichtenmuster 'es' und vor dem Nachrichtenmuster 's' Folgendes hinzu:

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
#### Bobs KDF für NS-Nachricht

Fügen Sie nach dem Nachrichtenmuster 'es' und vor dem Nachrichtenmuster 's' Folgendes hinzu:

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
#### Bob KDF (Schlüsselableitungsfunktion) für NSR-Nachricht

Fügen Sie nach dem Nachrichtenmuster 'ee' und vor dem Nachrichtenmuster 'se' hinzu:

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
#### Alice-KDF für NSR-Nachricht

Fügen Sie nach dem 'ee'-Nachrichtenmuster und vor dem 'ss'-Nachrichtenmuster Folgendes hinzu:

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
#### Schlüsselableitungsfunktion (KDF) für split()

Die Funktion split() entspricht unverändert der ECIES-Standardspezifikation (ECIES: Elliptic Curve Integrated Encryption Scheme, ein Verschlüsselungsverfahren auf Basis elliptischer Kurven). Nach Abschluss des Handshakes:

```
keydata = HKDF(chainKey, ZEROLEN, "", 64)
k_ab = keydata[0:31]
k_ba = keydata[32:63]
```
Dies sind die bidirektionalen Sitzungsschlüssel für die laufende Kommunikation.

### Nachrichtenformat

#### NS (Neue Sitzung) Format

**Änderungen:** Im aktuellen Ratchet (Schlüsselfortschaltung) befindet sich der statische Schlüssel im ersten ChaCha20-Poly1305-Abschnitt und die Nutzlast im zweiten Abschnitt. Mit ML-KEM gibt es nun drei Abschnitte. Der erste Abschnitt enthält den verschlüsselten öffentlichen ML-KEM-Schlüssel (encap_key). Der zweite Abschnitt enthält den statischen Schlüssel. Der dritte Abschnitt enthält die Nutzlast.

**Nachrichtengrößen:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">X25519 len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NS len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NS Enc len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NS Dec len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">PQ key len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">pl len</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">96+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">--</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">912+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">880+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">800+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">800</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1296+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1264+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1184+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1184</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1680+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1648+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1568+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1568</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
  </tbody>
</table>
**Hinweis:** Die Nutzlast muss einen DateTime-Block enthalten (mindestens 7 Bytes: 1-Byte-Typ, 2-Byte-Größe, 4-Byte-Zeitstempel). Die minimalen NS-Größen können entsprechend berechnet werden. Die minimale praktische NS-Größe beträgt daher 103 Bytes für X25519 und liegt bei hybriden Varianten zwischen 919 und 1687 Bytes.

Die Größenzunahmen um 816, 1200 und 1584 Byte bei den drei ML-KEM-Varianten gehen auf den öffentlichen Schlüssel von ML-KEM sowie einen 16-Byte-Poly1305-MAC für authentifizierte Verschlüsselung zurück.

#### NSR (Neue Sitzungsantwort) Format

**Änderungen:** Die aktuelle ratchet (Schlüssel-Update-Mechanismus) hat für den ersten ChaCha20-Poly1305-Abschnitt eine leere Nutzlast und die Nutzlast im zweiten Abschnitt. Mit ML-KEM gibt es nun drei Abschnitte. Der erste Abschnitt enthält das verschlüsselte ML-KEM-Chiffrat. Der zweite Abschnitt hat eine leere Nutzlast. Der dritte Abschnitt enthält die Nutzlast.

**Nachrichtengrößen:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">X25519 len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NSR len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NSR Enc len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NSR Dec len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">PQ ct len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">pl len</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">72+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">40+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">--</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">856+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">824+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">784+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">768</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1176+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1144+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1104+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1088</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1656+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1624+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1584+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1568</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
  </tbody>
</table>
Die Größenzunahmen um 784, 1104 und 1584 Byte bei den drei ML-KEM-Varianten ergeben sich aus dem ML-KEM-Chiffrat plus einem 16-Byte-Poly1305-MAC für authentifizierte Verschlüsselung.

## Overhead-Analyse

### Schlüsselaustausch

Der Overhead der Hybridverschlüsselung ist im Vergleich zu X25519 allein erheblich:

- **MLKEM512_X25519**: Ungefähr 9-12x Zunahme der Größe der Handshake-Nachrichten (NS: 9.5x, NSR: 11.9x)
- **MLKEM768_X25519**: Ungefähr 13-16x Zunahme der Größe der Handshake-Nachrichten (NS: 13.5x, NSR: 16.3x)
- **MLKEM1024_X25519**: Ungefähr 17-23x Zunahme der Größe der Handshake-Nachrichten (NS: 17.5x, NSR: 23x)

Dieser Overhead ist angesichts der zusätzlichen Post-Quanten-Sicherheitsvorteile akzeptabel. Die Multiplikatoren variieren je nach Nachrichtentyp, da sich die Basisgrößen der Nachrichten unterscheiden (NS mindestens 96 Byte, NSR mindestens 72 Byte).

### Überlegungen zur Bandbreite

Für einen typischen Sitzungsaufbau mit minimaler Nutzlast:
- Nur X25519: ~200 Bytes insgesamt (NS + NSR)
- MLKEM512_X25519: ~1,800 Bytes insgesamt (9-facher Anstieg)
- MLKEM768_X25519: ~2,500 Bytes insgesamt (12,5-facher Anstieg)
- MLKEM1024_X25519: ~3,400 Bytes insgesamt (17-facher Anstieg)

Nach dem Sitzungsaufbau verwendet die fortlaufende Nachrichtenverschlüsselung dasselbe Datenübertragungsformat wie reine X25519-Sitzungen, sodass für nachfolgende Nachrichten kein Overhead anfällt.

## Sicherheitsanalyse

### Handshakes

Der hybride Handshake bietet sowohl klassische Sicherheit (X25519) als auch Post-Quanten-Sicherheit (ML-KEM). Ein Angreifer muss **beide**, sowohl das klassische ECDH als auch das Post-Quanten-KEM, brechen, um die Sitzungsschlüssel zu kompromittieren.

Dies bietet: - **Aktuelle Sicherheit**: X25519 ECDH bietet Schutz gegen klassische Angreifer (Sicherheitsniveau von 128 Bit) - **Zukünftige Sicherheit**: ML-KEM (Post-Quanten-Schlüsselkapselungsmechanismus) bietet Schutz gegen Quantenangreifer (variiert je nach Parametersatz) - **Hybride Sicherheit**: Beide müssen gebrochen werden, um die Sitzung zu kompromittieren (Sicherheitsniveau = Maximum beider Komponenten)

### Sicherheitsstufen

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Variant</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NIST Category</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Classical Security</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">PQ Security</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Hybrid Security</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Category 1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit (X25519)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-128 equivalent</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Category 3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit (X25519)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-192 equivalent</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Category 5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit (X25519)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 equivalent</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit</td>
    </tr>
  </tbody>
</table>
**Hinweis:** Das hybride Sicherheitsniveau wird durch die schwächere der beiden Komponenten begrenzt. In allen Fällen bietet X25519 eine klassische Sicherheit von 128 Bit. Wenn ein kryptografisch relevanter Quantencomputer verfügbar wird, hängt das Sicherheitsniveau vom gewählten ML‑KEM (Modul‑Gitter‑basierter Schlüsselkapselungsmechanismus)‑Parametersatz ab.

### Vorwärtsgeheimnis

Der hybride Ansatz wahrt die Eigenschaften der Vorwärtsgeheimhaltung. Sitzungsschlüssel werden aus beiden ephemeren Schlüsselaustauschverfahren, X25519 und ML-KEM, abgeleitet. Wenn entweder die ephemeren X25519- oder ML-KEM-Privatschlüssel nach dem Handshake vernichtet werden, können frühere Sitzungen nicht entschlüsselt werden, selbst wenn langfristige statische Schlüssel kompromittiert sind.

Das IK pattern (IK-Muster) bietet vollständige Vorwärtsgeheimhaltung (Noise Confidentiality level 5), nachdem die zweite Nachricht (NSR) gesendet wurde.

## Typ-Einstellungen

Implementierungen sollten mehrere Hybridtypen unterstützen und die stärkste gegenseitig unterstützte Variante aushandeln. Die Präferenzreihenfolge sollte wie folgt sein:

1. **MLKEM768_X25519** (Typ 6) - Empfohlene Voreinstellung, bestes Gleichgewicht zwischen Sicherheit und Leistung
2. **MLKEM1024_X25519** (Typ 7) - Höchste Sicherheit für sensible Anwendungen
3. **MLKEM512_X25519** (Typ 5) - Grundlegende Post-Quanten-Sicherheit für ressourcenbeschränkte Szenarien
4. **X25519** (Typ 4) - Nur klassisch, Fallback für Kompatibilität

**Begründung:** MLKEM768_X25519 wird als Standard empfohlen, weil es Sicherheit der NIST-Kategorie 3 (entspricht AES-192) bietet, die als ausreichender Schutz gegen Quantencomputer gilt, und dabei angemessene Nachrichtengrößen beibehält. MLKEM1024_X25519 bietet eine höhere Sicherheit, verursacht jedoch einen erheblich höheren Overhead.

## Implementierungshinweise

### Bibliotheksunterstützung

- **Java**: Bouncycastle-Bibliothek Version 1.79 (August 2024) und neuer unterstützt alle erforderlichen ML-KEM-Varianten und SHA3/SHAKE-Funktionen. Verwenden Sie `org.bouncycastle.pqc.crypto.mlkem.MLKEMEngine` zur Einhaltung von FIPS 203.
- **C++**: OpenSSL 3.5 (April 2025) und neuer enthält Unterstützung für ML-KEM über die EVP_KEM-Schnittstelle. Dies ist eine Version mit Langzeitunterstützung (LTS), die bis April 2030 gepflegt wird.
- **Go**: Es sind mehrere Drittanbieterbibliotheken für ML-KEM und SHA3 verfügbar, darunter die CIRCL-Bibliothek von Cloudflare.

### Migrationsstrategie

Implementierungen sollten: 1. In der Übergangsphase sowohl X25519-only als auch hybride ML-KEM-Varianten unterstützen 2. Hybride Varianten bevorzugen, wenn beide Peers sie unterstützen 3. Ein Fallback auf X25519-only zur Abwärtskompatibilität beibehalten 4. Einschränkungen der Netzwerkbandbreite bei der Auswahl der Standardvariante berücksichtigen

### Gemeinsame Tunnels

Die erhöhten Nachrichtengrößen können die Nutzung gemeinsam genutzter tunnel beeinträchtigen. Implementierungen sollten Folgendes in Betracht ziehen: - Handshakes nach Möglichkeit bündeln, um den Overhead zu amortisieren - Kürzere Ablaufzeiten für hybride Sitzungen verwenden, um den gespeicherten Zustand zu verringern - Die Bandbreitennutzung überwachen und die Parameter entsprechend anpassen - Eine Überlastkontrolle für den Datenverkehr beim Sitzungsaufbau implementieren

### Überlegungen zur Größe neuer Sitzungen

Aufgrund der größeren Handshake-Nachrichten müssen Implementierungen möglicherweise Folgendes tun: - Die Puffergrößen für die Sitzungsaushandlung erhöhen (mindestens 4KB empfohlen) - Timeout-Werte für langsamere Verbindungen anpassen (~3-17x größere Nachrichten berücksichtigen) - Komprimierung für Nutzdaten in NS/NSR-Nachrichten in Erwägung ziehen - Fragmentierungsbehandlung implementieren, falls von der Transportschicht erforderlich

### Tests und Validierung

Implementierungen sollten überprüfen: - Korrekte ML-KEM-Schlüsselgenerierung, Kapselung und Entkapselung - Korrekte Integration von kem_shared_key in die Noise KDF - Berechnungen der Nachrichtengröße entsprechen der Spezifikation - Interoperabilität mit anderen I2P router-Implementierungen - Fallback-Verhalten, wenn ML-KEM nicht verfügbar ist

Testvektoren für ML-KEM-Operationen stehen im NIST [Cryptographic Algorithm Validation Program](https://csrc.nist.gov/Projects/cryptographic-algorithm-validation-program) zur Verfügung.

## Versionskompatibilität

**I2P-Versionsnummerierung:** I2P führt zwei parallele Versionsnummern: - **Router-Release-Version**: 2.x.x-Format (z. B. 2.10.0, veröffentlicht im September 2025) - **API/Protokoll-Version**: 0.9.x-Format (z. B. 0.9.67 entspricht router 2.10.0)

Diese Spezifikation verweist auf die Protokollversion 0.9.67, die dem router-Release 2.10.0 und neuer entspricht.

**Kompatibilitätsmatrix:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Implementation</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">ML-KEM Support</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2pd</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.58.0+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Full (512/768/1024)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deployed September 2025</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Java I2P</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67 / 2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Not yet</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Planned for future release</td>
    </tr>
  </tbody>
</table>
## Referenzen

- **[ECIES]**: [ECIES-X25519-AEAD-Ratchet-Spezifikation](/docs/specs/ecies/)
- **[Prop169]**: [Vorschlag 169: Post-Quanten-Kryptografie](/proposals/169-pq-crypto/)
- **[FIPS203]**: [NIST FIPS 203 - ML-KEM-Standard](https://csrc.nist.gov/pubs/fips/203/final)
- **[FIPS202]**: [NIST FIPS 202 - SHA-3-Standard](https://csrc.nist.gov/pubs/fips/202/final)
- **[Noise]**: [Noise-Protokoll-Framework](https://noiseprotocol.org/noise.html)
- **[COMMON]**: [Spezifikation gemeinsamer Strukturen](/docs/specs/common-structures/)
- **[RFC7539]**: [RFC 7539 - ChaCha20 und Poly1305](https://www.rfc-editor.org/rfc/rfc7539)
- **[RFC5869]**: [RFC 5869 - HKDF](https://www.rfc-editor.org/rfc/rfc5869)
- **[OpenSSL]**: [OpenSSL 3.5 ML-KEM-Dokumentation](https://docs.openssl.org/3.5/man7/EVP_KEM-ML-KEM/)
- **[Bouncycastle]**: [Bouncycastle Java-Kryptografie-Bibliothek](https://www.bouncycastle.org/)

---
