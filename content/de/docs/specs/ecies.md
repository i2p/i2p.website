---
title: "Spezifikation der ECIES-X25519-AEAD-Ratchet-Verschlüsselung (Ratchet = Schlüsselwechsel-Mechanismus)"
description: "Elliptic Curve Integrated Encryption Scheme (integriertes Verschlüsselungsschema auf elliptischen Kurven) für I2P (X25519 + AEAD)"
slug: "ecies"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
toc: true
---

## Übersicht

### Zweck

ECIES-X25519-AEAD-Ratchet (ein Verfahren zur Ende-zu-Ende-Verschlüsselung) ist I2Ps modernes Ende-zu-Ende-Verschlüsselungsprotokoll und ersetzt das Legacy-System ElGamal/AES+SessionTags. Es bietet Vorwärtsgeheimnis, authentifizierte Verschlüsselung und deutliche Verbesserungen bei Leistung und Sicherheit.

### Wesentliche Verbesserungen gegenüber ElGamal/AES+SessionTags

- **Kleinere Schlüssel**: 32-Byte-Schlüssel gegenüber 256-Byte-ElGamal-öffentlichen Schlüsseln (87,5 % Verringerung)
- **Vorwärtsgeheimnis**: Erreicht durch DH-Ratcheting (schrittweise Schlüsselaktualisierung; im Legacy-Protokoll nicht verfügbar)
- **Moderne Kryptografie**: X25519 DH, ChaCha20-Poly1305 AEAD, SHA-256
- **Authentifizierte Verschlüsselung**: Integrierte Authentifizierung durch AEAD-Konstruktion
- **Bidirektionales Protokoll**: Gekoppelte eingehende/ausgehende Sitzungen gegenüber unidirektionalem Legacy-Protokoll
- **Effiziente Tags**: 8-Byte-Sitzungs-Tags gegenüber 32-Byte-Tags (75 % Verringerung)
- **Verschleierung des Datenverkehrs**: Elligator2-Codierung macht Handshakes ununterscheidbar vom Zufall

### Bereitstellungsstatus

- **Erstveröffentlichung**: Version 0.9.46 (25. Mai 2020)
- **Netzwerkbereitstellung**: Seit 2020 abgeschlossen
- **Aktueller Status**: Ausgereift, breit ausgerollt (seit über 5 Jahren im produktiven Einsatz)
- **Router-Unterstützung**: Version 0.9.46 oder höher erforderlich
- **Floodfill-Anforderungen**: Nahezu 100% Verbreitung für verschlüsselte Lookups

### Implementierungsstatus

**Vollständig implementiert:** - New Session (NS)-Nachrichten mit Bindung - New Session Reply (NSR)-Nachrichten - Existing Session (ES)-Nachrichten - DH-Ratchet-Mechanismus (Ratschenmechanismus) - Session-Tag- und symmetrische Schlüssel-Ratchets - DateTime-, NextKey-, ACK-, ACK Request-, Garlic Clove- und Padding-Blöcke

**Nicht implementiert (Stand: Version 0.9.50):** - MessageNumbers-Block (Typ 6) - Options-Block (Typ 5) - Termination-Block (Typ 4) - Automatische Antworten auf Protokollebene - Zero-Static-Key-Modus - Multicast-Sitzungen

**Hinweis**: Der Implementierungsstatus für die Versionen 1.5.0 bis 2.10.0 (2021-2025) erfordert eine Überprüfung, da möglicherweise einige Funktionen hinzugefügt wurden.

---

## Protokollgrundlagen

### Noise Protocol Framework (kryptografisches Protokoll-Framework)

ECIES-X25519-AEAD-Ratchet (Ratchet-Verfahren auf Basis von ECIES, X25519 und AEAD) basiert auf dem [Noise Protocol Framework](https://noiseprotocol.org/) (Protokollrahmen „Noise“, Revision 34, 2018-07-11), insbesondere auf dem **IK** (Interactive, Known remote static key – interaktiv, bekannter statischer Schlüssel der Gegenstelle) Handshake-Muster mit I2P-spezifischen Erweiterungen.

### Bezeichner des Noise-Protokolls

```
Noise_IKelg2+hs2_25519_ChaChaPoly_SHA256
```
**Bezeichner-Komponenten:** - `Noise` - Basis-Framework - `IK` - Interaktives Handshake-Muster mit bekanntem entfernten statischen Schlüssel - `elg2` - Elligator2-Codierung für ephemere Schlüssel (I2P extension) - `+hs2` - MixHash wird vor der zweiten Nachricht aufgerufen, um das Tag einzumischen (I2P extension) - `25519` - X25519-Diffie-Hellman-Funktion - `ChaChaPoly` - ChaCha20-Poly1305-AEAD-Chiffre - `SHA256` - SHA-256-Hashfunktion

### Noise Handshake-Muster

**IK-Musternotation:**

```
<- s                    (Bob's static key known to Alice)
...
-> e, es, s, ss         (Alice sends ephemeral, DH es, static key, DH ss)
<- e, ee, se            (Bob sends ephemeral, DH ee, DH se)
```
**Bedeutungen der Token:** - `e` - Übertragung eines ephemeren Schlüssels - `s` - Übertragung eines statischen Schlüssels - `es` - DH (Diffie-Hellman-Schlüsselaustausch) zwischen Alices ephemerem Schlüssel und Bobs statischem Schlüssel - `ss` - DH zwischen Alices statischem Schlüssel und Bobs statischem Schlüssel - `ee` - DH zwischen Alices ephemerem Schlüssel und Bobs ephemerem Schlüssel - `se` - DH zwischen Bobs statischem Schlüssel und Alices ephemerem Schlüssel

### Sicherheitseigenschaften von Noise

In der Terminologie von Noise bietet das IK pattern (IK-Muster):

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Message</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Authentication Level</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Confidentiality Level</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Message&nbsp;1 (NS)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;1 (sender auth, KCI vulnerable)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;2 (weak forward secrecy)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Message&nbsp;2 (NSR)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;2 (mutual auth)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;4 (weak forward secrecy)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Transport (ES)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;2 (mutual auth)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;5 (strong forward secrecy)</td>
    </tr>
  </tbody>
</table>
**Authentifizierungsstufen:** - **Stufe 1**: Die Nutzdaten sind authentifiziert und dem Inhaber des statischen Schlüssels des Senders zugeordnet, sind jedoch anfällig für Key Compromise Impersonation (KCI; Identitätsanmaßung bei kompromittiertem Schlüssel) - **Stufe 2**: Resistent gegen KCI-Angriffe nach NSR (Sitzungsneustart)

**Vertraulichkeitsstufen:** - **Stufe 2**: Vorwärtsgeheimnis, falls der statische Schlüssel des Absenders später kompromittiert wird - **Stufe 4**: Vorwärtsgeheimnis, falls der ephemere Schlüssel des Absenders später kompromittiert wird - **Stufe 5**: Vollständiges Vorwärtsgeheimnis, nachdem beide ephemeren Schlüssel gelöscht wurden

### Unterschiede zwischen IK und XK

Das IK-Muster unterscheidet sich von dem in NTCP2 und SSU2 verwendeten XK-Muster:

1. **Vier DH-Operationen**: IK verwendet 4 DH-Operationen (es, ss, ee, se) gegenüber 3 bei XK
2. **Sofortige Authentifizierung**: Alice wird in der ersten Nachricht authentifiziert (Authentifizierungsstufe 1)
3. **Schnellere Herstellung des Vorwärtsgeheimnisses**: Volles Vorwärtsgeheimnis (Stufe 5) wird nach der zweiten Nachricht erreicht (1-RTT)
4. **Kompromiss**: Die Nutzlast der ersten Nachricht ist nicht vorwärtsgeheim (im Gegensatz zu XK, wo alle Nutzlasten vorwärtsgeheim sind)

**Zusammenfassung**: IK ermöglicht die 1-RTT-Übermittlung von Bobs Antwort mit vollständigem Vorwärtsgeheimnis, auf Kosten dessen, dass die anfängliche Anfrage nicht vorwärtsgeheim ist.

### Konzepte der Signal-Double-Ratchet

ECIES (Elliptic Curve Integrated Encryption Scheme, integriertes Verschlüsselungsschema mit elliptischen Kurven) integriert Konzepte aus dem [Signal Double Ratchet-Algorithmus](https://signal.org/docs/specifications/doubleratchet/):

- **DH Ratchet** (Ratchet-Mechanismus auf Basis von Diffie-Hellman): Bietet Vorwärtsgeheimnis, indem periodisch neue DH-Schlüssel ausgetauscht werden
- **Symmetric Key Ratchet** (symmetrischer Ratchet-Mechanismus für Schlüssel): Leitet für jede Nachricht neue Sitzungsschlüssel ab
- **Session Tag Ratchet** (Ratchet-Mechanismus für Sitzungs-Tags): Erzeugt deterministisch Sitzungs-Tags zur einmaligen Verwendung

**Wesentliche Unterschiede zu Signal:** - **Selteneres Ratcheting (schrittweise Schlüsselaktualisierung)**: I2P führt Ratcheting nur bei Bedarf durch (bei nahezu erschöpften Tags oder per Richtlinie) - **Session-Tags statt Header-Verschlüsselung**: Verwendet deterministische Tags statt verschlüsselter Header - **Explizite ACKs (Empfangsbestätigungen)**: Verwendet In-Band-ACK-Blöcke, statt sich ausschließlich auf Rückverkehr zu verlassen - **Getrennte Tag- und Schlüssel-Ratchets**: Effizienter für den Empfänger (kann die Schlüsselberechnung aufschieben)

### I2P-Erweiterungen für Noise

1. **Elligator2-Codierung**: Ephemere Schlüssel werden so codiert, dass sie nicht von Zufallsdaten zu unterscheiden sind
2. **Tag vor NSR vorangestellt**: Session-Tag wird zur Korrelation vor die NSR-Nachricht gesetzt
3. **Definiertes Nutzlastformat**: Blockbasierte Nutzlaststruktur für alle Nachrichtentypen
4. **I2NP-Kapselung**: Alle Nachrichten werden in I2NP Garlic Message-Headern eingebettet
5. **Getrennte Datenphase**: Transportnachrichten (ES) weichen von der standardmäßigen Noise (Protokollrahmenwerk)-Datenphase ab

---

## Kryptografische Primitive

### X25519 Diffie-Hellman

**Spezifikation**: [RFC 7748](https://tools.ietf.org/html/rfc7748)

**Wesentliche Eigenschaften:** - **Größe des privaten Schlüssels**: 32 Bytes - **Größe des öffentlichen Schlüssels**: 32 Bytes - **Größe des gemeinsamen Geheimnisses**: 32 Bytes - **Byte-Reihenfolge (Endianness)**: Little-endian - **Kurve**: Curve25519

**Operationen:**

### X25519 GENERATE_PRIVATE()

Erzeugt einen zufälligen privaten Schlüssel mit 32 Byte:

```
privkey = CSRNG(32)
```
### X25519 DERIVE_PUBLIC(privkey)

Leitet den entsprechenden öffentlichen Schlüssel ab:

```
pubkey = curve25519_scalarmult_base(privkey)
```
Gibt einen 32 Byte großen, im Little-Endian-Format vorliegenden öffentlichen Schlüssel zurück.

### X25519 DH(privkey, pubkey)

Führt einen Diffie-Hellman-Schlüsselaustausch durch:

```
sharedSecret = curve25519_scalarmult(privkey, pubkey)
```
Gibt ein 32 Byte langes gemeinsames Geheimnis zurück.

**Sicherheitshinweis**: Implementierer müssen prüfen, dass das gemeinsame Geheimnis nicht nur aus Nullen besteht (schwacher Schlüssel). In diesem Fall ablehnen und den Handshake abbrechen.

### ChaCha20-Poly1305 AEAD (Authentifizierte Verschlüsselung mit assoziierten Daten)

**Spezifikation**: [RFC 7539](https://tools.ietf.org/html/rfc7539) Abschnitt 2.8

**Parameter:** - **Schlüsselgröße**: 32 Byte (256 Bit) - **Nonce-Größe**: 12 Byte (96 Bit) - **MAC-Größe**: 16 Byte (128 Bit) - **Blockgröße**: 64 Byte (intern)

**Nonce (Einmalwert)-Format:**

```
Byte 0-3:   0x00 0x00 0x00 0x00  (always zero)
Byte 4-11:  Little-endian counter (message number N)
```
**AEAD-Konstruktion:**

Das AEAD (authentifizierte Verschlüsselung mit zugeordneten Daten) kombiniert die Stromchiffre ChaCha20 mit dem Poly1305-MAC:

1. ChaCha20-Schlüsselstrom aus Schlüssel und Nonce erzeugen
2. Klartext per XOR mit dem Schlüsselstrom verschlüsseln
3. Poly1305-MAC über (assoziierte Daten || Geheimtext) berechnen
4. 16-Byte-MAC an den Geheimtext anhängen

### ChaCha20-Poly1305 ENCRYPT(k, n, plaintext, ad)

Verschlüsselt Klartext mit Authentifizierung:

```python
# Inputs
k = 32-byte cipher key
n = 12-byte nonce (first 4 bytes zero, last 8 bytes = message number)
plaintext = data to encrypt (0 to 65519 bytes)
ad = associated data (optional, used in MAC calculation)

# Output
ciphertext = chacha20_encrypt(k, n, plaintext)
mac = poly1305(ad || ciphertext, poly1305_key_gen(k, n))
return ciphertext || mac  # Total length = len(plaintext) + 16
```
**Eigenschaften:** - Der Geheimtext hat dieselbe Länge wie der Klartext (Stromchiffre) - Die Ausgabe ist plaintext_length + 16 Bytes (enthält MAC) - Die gesamte Ausgabe ist nicht von zufälligen Daten zu unterscheiden, wenn der Schlüssel geheim ist - Der MAC authentifiziert sowohl die assoziierten Daten als auch den Geheimtext

### ChaCha20-Poly1305 ENTSCHLÜSSELN(k, n, ciphertext, ad)

Entschlüsselt und überprüft die Authentifizierung:

```python
# Split ciphertext and MAC
ct_without_mac = ciphertext[0:-16]
received_mac = ciphertext[-16:]

# Verify MAC
expected_mac = poly1305(ad || ct_without_mac, poly1305_key_gen(k, n))
if not constant_time_compare(received_mac, expected_mac):
    raise AuthenticationError("MAC verification failed")

# Decrypt
plaintext = chacha20_decrypt(k, n, ct_without_mac)
return plaintext
```
**Kritische Sicherheitsanforderungen:** - Nonces (einmalige Werte) MÜSSEN für jede Nachricht mit demselben Schlüssel eindeutig sein - Nonces DÜRFEN NICHT wiederverwendet werden (katastrophales Versagen bei Wiederverwendung) - Die Verifikation des MAC (Nachrichten-Authentifizierungscode) MUSS einen zeitkonstanten Vergleich verwenden, um Timing-Angriffe zu verhindern - Eine fehlgeschlagene MAC-Verifikation MUSS zur vollständigen Ablehnung der Nachricht führen (keine teilweise Entschlüsselung)

### SHA-256-Hashfunktion

**Spezifikation**: NIST FIPS 180-4

**Eigenschaften:** - **Ausgabegröße**: 32 Byte (256 Bit) - **Blockgröße**: 64 Byte (512 Bit) - **Sicherheitsniveau**: 128 Bit (Kollisionsresistenz)

**Operationen:**

### SHA-256 H(p, d)

SHA-256-Hash mit Personalization String (Personalisierungszeichenkette):

```
H(p, d) := SHA256(p || d)
```
Wobei `||` die Verkettung bezeichnet, `p` für den Personalisierungsstring steht und `d` für die Daten.

### SHA-256 MixHash(d)

Aktualisiert den laufenden Hash mit neuen Daten:

```
h = SHA256(h || d)
```
Wird im gesamten Noise handshake (Aushandlung im Noise-Protokoll) verwendet, um den Transkript-Hash fortzuschreiben.

### HKDF-Schlüsselableitung

**Spezifikation**: [RFC 5869](https://tools.ietf.org/html/rfc5869)

**Beschreibung**: HMAC-basierte Schlüsselableitungsfunktion mit SHA-256

**Parameter:** - **Hashfunktion**: HMAC-SHA256 - **Salt-Länge**: Bis zu 32 Byte (SHA-256-Ausgabegröße) - **Ausgabelänge**: Variabel (bis zu 255 * 32 Byte)

**HKDF-Funktion:**

```python
def HKDF(salt, ikm, info, length):
    """
    Args:
        salt: Salt value (32 bytes max for SHA-256)
        ikm: Input key material (any length)
        info: Context-specific info string
        length: Desired output length in bytes
    
    Returns:
        output: Derived key material (length bytes)
    """
    # Extract phase
    prk = HMAC-SHA256(salt, ikm)
    
    # Expand phase
    n = ceil(length / 32)
    t = b''
    okm = b''
    for i in range(1, n + 1):
        t = HMAC-SHA256(prk, t || info || byte(i))
        okm = okm || t
    
    return okm[0:length]
```
**Häufige Nutzungsmuster:**

```python
# Generate two keys (64 bytes total)
keydata = HKDF(chainKey, sharedSecret, "KDFDHRatchetStep", 64)
nextRootKey = keydata[0:31]
chainKey = keydata[32:63]

# Generate session tag (8 bytes)
tagdata = HKDF(chainKey, CONSTANT, "SessionTagKeyGen", 64)
nextChainKey = tagdata[0:31]
sessionTag = tagdata[32:39]

# Generate symmetric key (32 bytes)
keydata = HKDF(chainKey, ZEROLEN, "SymmetricRatchet", 64)
nextChainKey = keydata[0:31]
sessionKey = keydata[32:63]
```
**In ECIES verwendete Info-Strings:** - `"KDFDHRatchetStep"` - Schlüsselableitung der DH-Ratchet (Schrittmechanismus zur Schlüsselaktualisierung) - `"TagAndKeyGenKeys"` - Initialisierung der Tag- und Schlüsselketten-Schlüssel - `"STInitialization"` - Initialisierung der Session-Tag-Ratchet - `"SessionTagKeyGen"` - Generierung von Session-Tags - `"SymmetricRatchet"` - Generierung symmetrischer Schlüssel - `"XDHRatchetTagSet"` - Tagset-Schlüssel der DH-Ratchet - `"SessionReplyTags"` - Generierung des NSR-Tagsets - `"AttachPayloadKDF"` - Schlüsselableitung für die NSR-Nutzlast

### Elligator2-Kodierung (kryptografisches Abbildungsverfahren)

**Zweck**: Öffentliche X25519-Schlüssel (ECDH-Verfahren auf Basis von Curve25519) so kodieren, dass sie von gleichverteilten zufälligen 32-Byte-Folgen nicht zu unterscheiden sind.

**Spezifikation**: [Elligator2 Paper](https://elligator.cr.yp.to/elligator-20130828.pdf)

**Problem**: Standardmäßige öffentliche X25519-Schlüssel haben eine erkennbare Struktur. Ein Beobachter kann Handshake-Nachrichten identifizieren, indem er diese Schlüssel erkennt, selbst wenn der Inhalt verschlüsselt ist.

**Lösung**: Elligator2 bietet eine bijektive Abbildung zwischen ~50% der gültigen X25519-öffentlichen Schlüssel und zufällig aussehenden 254-Bit-Zeichenfolgen.

**Schlüsselgenerierung mit Elligator2 (kryptografisches Verfahren zur Abbildung elliptischer Kurvenpunkte auf zufällig aussehende Bytes):**

### Elligator2 GENERATE_PRIVATE_ELG2()

Erzeugt einen privaten Schlüssel, der zu einem öffentlichen Schlüssel gehört, der mit Elligator2 (ein Kodierungsverfahren für elliptische Kurvenpunkte) kodierbar ist:

```python
while True:
    privkey = CSRNG(32)
    pubkey = DERIVE_PUBLIC(privkey)
    
    # Test if public key is Elligator2-encodable
    try:
        encoded = ENCODE_ELG2(pubkey)
        # Success - this key pair is suitable
        return privkey
    except NotEncodableError:
        # Try again with new random key
        continue
```
**Wichtig**: Etwa 50 % der zufällig erzeugten privaten Schlüssel führen zu nicht kodierbaren öffentlichen Schlüsseln. Diese müssen verworfen werden; anschließend ist eine Neugenerierung zu versuchen.

**Leistungsoptimierung**: Schlüssel vorab in einem Hintergrund-Thread generieren, um einen Pool geeigneter Schlüsselpaare bereitzuhalten und Verzögerungen während des Handshakes zu vermeiden.

### Elligator2 ENCODE_ELG2(pubkey)

Kodiert einen öffentlichen Schlüssel in 32 zufällig aussehende Bytes:

```python
def ENCODE_ELG2(pubkey):
    """
    Encodes X25519 public key using Elligator2.
    
    Args:
        pubkey: 32-byte X25519 public key (little-endian)
    
    Returns:
        encoded: 32-byte encoded key indistinguishable from random
    
    Raises:
        NotEncodableError: If pubkey cannot be encoded
    """
    # Perform Elligator2 representative calculation
    # Returns 254-bit value (31.75 bytes)
    encodedKey = elligator2_encode(pubkey)
    
    # Add 2 random bits to MSB to make full 32 bytes
    randomByte = CSRNG(1)
    encodedKey[31] |= (randomByte & 0xc0)
    
    return encodedKey
```
**Details zur Kodierung:** - Elligator2 liefert 254 Bit (nicht volle 256 Bit) - Die obersten 2 Bit von Byte 31 sind zufälliges Padding (Auffüllung) - Das Ergebnis ist gleichmäßig über den 32-Byte-Raum verteilt - Kodiert erfolgreich etwa 50 % der gültigen öffentlichen X25519-Schlüssel

### Elligator2 DECODE_ELG2(encodedKey)

Dekodiert zurück zum ursprünglichen öffentlichen Schlüssel:

```python
def DECODE_ELG2(encodedKey):
    """
    Decodes Elligator2-encoded key back to X25519 public key.
    
    Args:
        encodedKey: 32-byte encoded key
    
    Returns:
        pubkey: 32-byte X25519 public key (little-endian)
    """
    # Mask out 2 random padding bits from MSB
    encodedKey[31] &= 0x3f
    
    # Perform Elligator2 representative inversion
    pubkey = elligator2_decode(encodedKey)
    
    return pubkey
```
**Sicherheitseigenschaften:** - Kodierte Schlüssel sind rechnerisch nicht von zufälligen Bytes unterscheidbar - Keine statistischen Tests können Elligator2-kodierte Schlüssel zuverlässig erkennen - Das Dekodieren ist deterministisch (der gleiche kodierte Schlüssel erzeugt stets denselben öffentlichen Schlüssel) - Das Kodieren ist für die ~50% der Schlüssel in der kodierbaren Teilmenge bijektiv

**Implementierungshinweise:** - Kodierte Schlüssel in der Generierungsphase speichern, um eine erneute Kodierung während des Handshakes zu vermeiden - Ungeeignete Schlüssel aus der Elligator2-Generierung können für NTCP2 verwendet werden (das kein Elligator2 benötigt) - Die Schlüsselerzeugung im Hintergrund ist für die Leistung entscheidend - Die durchschnittliche Generierungszeit verdoppelt sich aufgrund einer Ablehnungsrate von 50 %

---

## Nachrichtenformate

### Übersicht

ECIES definiert drei Nachrichtentypen:

1. **Neue Sitzung (NS)**: Initiale Handshake-Nachricht von Alice an Bob
2. **Antwort auf neue Sitzung (NSR)**: Bobs Handshake-Antwort an Alice
3. **Bestehende Sitzung (ES)**: Alle nachfolgenden Nachrichten in beiden Richtungen

Alle Nachrichten werden im I2NP Garlic Message-Format (I2NP-Nachrichtenformat mit 'Garlic'-Struktur) mit zusätzlichen Verschlüsselungsschichten gekapselt.

### I2NP Garlic Message (Knoblauch-Nachricht) Container

Alle ECIES-Nachrichten werden in standardmäßige I2NP Garlic Message-Header eingekapselt:

```
+----+----+----+----+----+----+----+----+
|type|      msg_id       |  expiration   |
+----+----+----+----+----+----+----+----+
                         |  size   |chks|
+----+----+----+----+----+----+----+----+
|      length       |                   |
+----+----+----+----+                   +
|          encrypted data               |
~                                       ~
```
**Felder:** - `type`: 0x26 (Garlic-Nachricht) - `msg_id`: 4-Byte I2NP-Nachrichten-ID - `expiration`: 8-Byte-Unix-Zeitstempel (Millisekunden) - `size`: 2-Byte-Nutzlastgröße - `chks`: 1-Byte-Prüfsumme - `length`: 4-Byte-Länge der verschlüsselten Daten - `encrypted data`: ECIES-verschlüsselte Nutzlast

**Zweck**: Ermöglicht die Nachrichtenidentifizierung und das Routing auf der I2NP-Schicht. Das Feld `length` ermöglicht es den Empfängern, die gesamte Größe der verschlüsselten Nutzlast zu ermitteln.

### Neue Sitzung (NS)-Nachricht

Die New Session-Nachricht initiiert eine neue Sitzung von Alice zu Bob. Sie kommt in drei Varianten vor:

1. **Mit Bindung** (1b): Enthält Alices statischen Schlüssel für bidirektionale Kommunikation
2. **Ohne Bindung** (1c): Verzichtet auf den statischen Schlüssel für eindirektionale Kommunikation
3. **Einmal** (1d): Einzelnachrichtenmodus ohne Sitzungsaufbau

### NS-Nachricht mit Bindung (Typ 1b)

**Anwendungsfall**: Streaming, antwortfähige Datagramme, jedes Protokoll, das Antworten erfordert

**Gesamtlänge**: 96 + payload_length Bytes

**Format**:

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|   New Session Ephemeral Public Key    |
+             32 bytes                  +
|     Encoded with Elligator2           |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+         Static Key Section            +
|       ChaCha20 encrypted data         |
+            32 bytes                   +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+    (MAC) for Static Key Section       +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~          Variable length              ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
```
**Details zum Feld:**

**Ephemerer öffentlicher Schlüssel** (32 Byte, Klartext): - Alices einmaliger X25519-öffentlicher Schlüssel - Kodiert mit Elligator2 (nicht von Zufallsdaten zu unterscheiden) - Für jede NS-Nachricht neu erzeugt (niemals wiederverwendet) - Little-Endian-Format

**Abschnitt für statischen Schlüssel** (32 Bytes verschlüsselt, 48 Bytes mit MAC): - Enthält Alices statischen öffentlichen X25519-Schlüssel (32 Bytes) - Mit ChaCha20 verschlüsselt - Mit Poly1305-MAC authentifiziert (16 Bytes) - Von Bob verwendet, um die Sitzung an Alices Destination (Zieladresse) zu binden

**Nutzlastabschnitt** (mit variabler Länge verschlüsselt, +16 Bytes MAC): - Enthält garlic cloves (Einzelteile einer Garlic-Nachricht) und andere Blöcke - Muss den DateTime-Block als ersten Block enthalten - Enthält üblicherweise Garlic Clove-Blöcke mit Anwendungsdaten - Kann den NextKey-Block für immediate ratchet (sofortige Schlüsselfortschaltung) enthalten - Verschlüsselt mit ChaCha20 - Authentifiziert mit Poly1305 MAC (16 Bytes)

**Sicherheitseigenschaften:** - Ephemerer Schlüssel stellt die Vorwärtsgeheimnis-Komponente bereit - Statischer Schlüssel authentifiziert Alice (Bindung an das Ziel) - Beide Abschnitte haben separate MACs zur Domänentrennung - Der gesamte Handshake führt 2 DH-Operationen aus (es, ss)

### NS-Nachricht ohne Bindung (Typ 1c)

**Anwendungsfall**: Rohdatagramme, bei denen keine Antwort erwartet oder gewünscht ist

**Gesamtlänge**: 96 + payload_length Bytes

**Format**:

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|   New Session Ephemeral Public Key    |
+             32 bytes                  +
|     Encoded with Elligator2           |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+           Flags Section               +
|       ChaCha20 encrypted data         |
+            32 bytes                   +
|           All zeros                   |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for above section       +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~          Variable length              ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
```
**Wesentlicher Unterschied**: Der Flags-Abschnitt enthält 32 Bytes mit Nullen anstelle eines statischen Schlüssels.

**Erkennung**: Bob bestimmt den Nachrichtentyp, indem er den 32-Byte-Abschnitt entschlüsselt und prüft, ob alle Bytes Null sind: - Alle Bytes sind Null → Ungebundene Sitzung (Typ 1c) - Nicht alle Bytes sind Null → Gebundene Sitzung mit statischem Schlüssel (Typ 1b)

**Eigenschaften:** - Kein statischer Schlüssel bedeutet keine Bindung an Alices Zieladresse - Bob kann keine Antworten senden (keine Zieladresse bekannt) - Führt nur 1 DH-Operation aus - Folgt dem Noise (Kryptografie-Protokoll-Framework) "N"-Muster statt "IK" - Effizienter, wenn Antworten nie benötigt werden

**Flags-Abschnitt** (für zukünftige Verwendung reserviert): Derzeit nur Nullen. Kann in zukünftigen Versionen für die Aushandlung von Funktionen verwendet werden.

### NS Einmalnachricht (Typ 1d)

**Anwendungsfall**: Einzelne anonyme Nachricht ohne erwartete Sitzung oder Antwort

**Gesamtlänge**: 96 + payload_length Bytes

**Format**: Identisch mit NS ohne Bindung (Typ 1c)

**Unterscheidung**:  - Typ 1c kann mehrere Nachrichten in derselben Sitzung senden (ES-Nachrichten folgen) - Typ 1d sendet genau eine Nachricht ohne Sitzungsaufbau - In der Praxis könnten Implementierungen diese zunächst identisch behandeln

**Eigenschaften:** - Maximale Anonymität (kein statischer Schlüssel, keine Sitzung) - Von keiner der Parteien wird Sitzungszustand beibehalten - Folgt dem Noise "N"-Muster - Eine einzige DH-Operation (es)

### New Session Reply (NSR)-Nachricht

Bob sendet als Antwort auf Alices NS-Nachricht eine oder mehrere NSR-Nachrichten. NSR schließt den Noise IK handshake (Noise-Handshake nach dem IK-Muster) ab und stellt eine bidirektionale Sitzung her.

**Gesamtlänge**: 72 + payload_length Bytes

**Format**:

```
+----+----+----+----+----+----+----+----+
|       Session Tag   8 bytes           |
+----+----+----+----+----+----+----+----+
|                                       |
+        Ephemeral Public Key           +
|                                       |
+            32 bytes                   +
|     Encoded with Elligator2           |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+  (MAC) for Key Section (empty)        +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~          Variable length              ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
```
**Felddetails:**

**Session-Tag** (8 Bytes, Klartext): - Generiert aus dem NSR-Tagset (siehe KDF-Abschnitte) - Ordnet diese Antwort der NS-Nachricht von Alice zu - Ermöglicht Alice zu erkennen, auf welche NS diese NSR antwortet - Einmalige Verwendung (niemals wiederverwendet)

**Ephemerer öffentlicher Schlüssel** (32 Bytes, Klartext): - Bobs einmaliger öffentlicher X25519-Schlüssel - Mit Elligator2 kodiert - Für jede NSR-Nachricht neu erzeugt - Muss für jede gesendete NSR unterschiedlich sein

**MAC des Schlüsselabschnitts** (16 Bytes): - Authentifiziert leere Daten (ZEROLEN) - Teil des Noise-IK-Protokolls (se pattern; statisch-ephemeres Muster) - Verwendet das Hash-Transkript als assoziierte Daten - Kritisch für die Bindung von NSR an NS

**Nutzdatenabschnitt** (variable Länge): - Enthält garlic cloves (Einzelnachrichten im Garlic-Verfahren) und Blöcke - Enthält normalerweise Antworten auf Anwendungsebene - Kann leer sein (ACK-only NSR) - Maximale Größe: 65519 Bytes (65535 - 16 Byte MAC)

**Mehrere NSR-Nachrichten:**

Bob kann als Antwort auf eine NS (Nachrichtentyp) mehrere NSR-Nachrichten (Nachrichtentyp) senden: - Jede NSR-Nachricht hat einen eindeutigen ephemeren Schlüssel - Jede NSR-Nachricht hat einen eindeutigen Session-Tag - Alice verwendet die zuerst empfangene NSR-Nachricht, um den Handshake abzuschließen - Weitere NSR-Nachrichten dienen der Redundanz (für den Fall von Paketverlust)

**Kritisches Timing:** - Alice muss eine NSR empfangen, bevor sie ES-Nachrichten sendet - Bob muss eine ES-Nachricht empfangen, bevor er ES-Nachrichten sendet - NSR etabliert bidirektionale Sitzungsschlüssel über die split()-Operation

**Sicherheitseigenschaften:** - Schließt den Noise IK handshake (Handshake des Noise-IK-Protokolls) ab - Führt 2 zusätzliche DH-Operationen (ee, se) aus - Insgesamt 4 DH-Operationen über NS+NSR - Erreicht gegenseitige Authentifizierung (Stufe 2) - Bietet schwaches Vorwärtsgeheimnis (Stufe 4) für die NSR-Nutzlast

### Nachricht zur bestehenden Sitzung (ES)

Alle Nachrichten nach dem NS/NSR-Handshake verwenden das Existing Session-Format (Format für eine bestehende Sitzung). ES-Nachrichten werden bidirektional sowohl von Alice als auch von Bob verwendet.

**Gesamtlänge**: 8 + payload_length + 16 Bytes (mindestens 24 Bytes)

**Format**:

```
+----+----+----+----+----+----+----+----+
|       Session Tag   8 bytes           |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~          Variable length              ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+              (MAC)                    +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
```
**Details zum Feld:**

**Session-Tag** (8 Bytes, Klartext): - Generiert aus dem aktuellen ausgehenden Tagset (Menge von Tags) - Identifiziert die Sitzung und die Nachrichtennummer - Empfänger schlägt den Tag nach, um Sitzungsschlüssel und Nonce (Einmalwert) zu finden - Einmalige Verwendung (jeder Tag wird genau einmal verwendet) - Format: Erste 8 Bytes der HKDF-Ausgabe

**Nutzlastabschnitt** (variable Länge): - Enthält Garlic Cloves (Einzelelemente einer Garlic-Nachricht) und Blöcke - Keine erforderlichen Blöcke (kann leer sein) - Übliche Blöcke: Garlic Clove, NextKey, ACK, ACK Request, Padding - Maximale Größe: 65519 Bytes (65535 - 16-Byte-MAC)

**MAC** (16 Bytes): - Poly1305-Authentifizierungstag - Über die gesamte Nutzlast berechnet - Assoziierte Daten: das 8-Byte session tag (Sitzungs-Tag) - Muss korrekt verifiziert werden, sonst wird die Nachricht verworfen

**Ablauf der Tag-Abfrage:**

1. Empfänger extrahiert 8-Byte-Tag
2. Schlägt das Tag in allen aktuellen eingehenden Tagsets nach
3. Ruft den zugehörigen Sitzungsschlüssel und die Nachrichtennummer N ab
4. Erzeugt die Nonce: `[0x00, 0x00, 0x00, 0x00, N (8 bytes little-endian)]`
5. Entschlüsselt die Nutzlast mit AEAD (Authentifizierte Verschlüsselung mit zusätzlichen Daten), wobei das Tag als zugehörige Daten verwendet wird
6. Entfernt das Tag aus dem Tagset (Einmalverwendung)
7. Verarbeitet die entschlüsselten Blöcke

**Session Tag (Sitzungs-Tag) nicht gefunden:**

Wenn tag (Sitzungs-Tag) in keinem tagset (Satz von Sitzungs-Tags) gefunden wird: - Kann eine NS-Nachricht sein → NS-Entschlüsselung versuchen - Kann eine NSR-Nachricht sein → NSR-Entschlüsselung versuchen - Kann eine ES außer der Reihenfolge sein → kurz auf tagset-Aktualisierung warten - Kann ein Replay-Angriff sein → ablehnen - Kann beschädigte Daten sein → ablehnen

**Leere Nutzdaten:**

ES messages (ES-Nachrichten) können leere Nutzlasten (0 Bytes) haben: - Dient als explizites ACK, wenn eine ACK-Anforderung empfangen wurde - Liefert eine Antwort auf Protokollebene ohne Anwendungsdaten - Verbraucht dennoch einen session tag (Session-Tag, Kennzeichen einer Sitzung) - Nützlich, wenn die höhere Schicht keine sofort zu sendenden Daten hat

**Sicherheitsmerkmale:** - Vollständige Vorwärtsgeheimhaltung (Stufe 5) nach Empfang von NSR - Authentifizierte Verschlüsselung mit AEAD - Tag dient als zusätzliche assoziierte Daten - Maximal 65535 Nachrichten pro tagset (Tag-Satz), bevor ein Ratchet (Schlüsselfortschaltung) erforderlich ist

---

## Schlüsselableitungsfunktionen

Dieser Abschnitt dokumentiert alle in ECIES verwendeten KDF-Operationen und zeigt die vollständigen kryptografischen Ableitungen.

### Notation und Konstanten

**Konstanten:** - `ZEROLEN` - Byte-Array der Länge Null (leerer String) - `||` - Verkettungsoperator

**Variablen:** - `h` - Fortlaufendes Hash-Protokoll (32 Bytes) - `chainKey` - Kettenschlüssel für HKDF (32 Bytes) - `k` - Symmetrischer Chiffrierschlüssel (32 Bytes) - `n` - Nonce (Einmalwert) / Nachrichtennummer

**Schlüssel:** - `ask` / `apk` - Alices statischer privater/öffentlicher Schlüssel - `aesk` / `aepk` - Alices ephemerer privater/öffentlicher Schlüssel - `bsk` / `bpk` - Bobs statischer privater/öffentlicher Schlüssel - `besk` / `bepk` - Bobs ephemerer privater/öffentlicher Schlüssel

### KDFs für NS-Nachrichten

### KDF 1: Initialer Kettenschlüssel

Einmalig bei der Protokollinitialisierung ausgeführt (kann vorab berechnet werden):

```python
# Protocol name (40 bytes, ASCII, no null termination)
protocol_name = "Noise_IKelg2+hs2_25519_ChaChaPoly_SHA256"

# Initialize hash
h = SHA256(protocol_name)

# Initialize chaining key
chainKey = h

# MixHash with empty prologue
h = SHA256(h)

# State: chainKey and h initialized
# Can be precalculated for all outbound sessions
```
**Ergebnis:** - `chainKey` = anfänglicher Verkettungsschlüssel für alle nachfolgenden Schlüsselableitungsfunktionen (KDFs) - `h` = anfänglicher Transkript-Hash

### KDF 2: Bobs statische Schlüsselmischung

Bob führt dies einmalig aus (kann für alle eingehenden Sitzungen im Voraus berechnet werden):

```python
# Bob's static keys (published in LeaseSet)
bsk = GENERATE_PRIVATE()
bpk = DERIVE_PUBLIC(bsk)

# Mix Bob's public key into hash
h = SHA256(h || bpk)

# State: h updated with Bob's identity
# Can be precalculated by Bob for all inbound sessions
```
### KDF 3: Alices ephemere Schlüsselgenerierung

Alice erzeugt für jede NS‑Nachricht neue Schlüssel:

```python
# Generate ephemeral key pair suitable for Elligator2
aesk = GENERATE_PRIVATE_ELG2()
aepk = DERIVE_PUBLIC(aesk)

# Mix ephemeral public key into hash
h = SHA256(h || aepk)

# Elligator2 encode for transmission
elg2_aepk = ENCODE_ELG2(aepk)

# State: h updated with Alice's ephemeral key
# Send elg2_aepk as first 32 bytes of NS message
```
### KDF 4: NS-Abschnitt für statischen Schlüssel (es DH)

Leitet Schlüssel zur Verschlüsselung von Alices statischem Schlüssel ab:

```python
# Perform first DH (ephemeral-static)
sharedSecret = DH(aesk, bpk)  # Alice computes
# Equivalent: sharedSecret = DH(bsk, aepk)  # Bob computes

# Derive cipher key from shared secret
keydata = HKDF(chainKey, sharedSecret, "", 64)
chainKey = keydata[0:31]
k = keydata[32:63]

# AEAD encryption parameters
nonce = 0
associated_data = h  # Current hash transcript

# Encrypt static key section
if binding_requested:
    plaintext = apk  # Alice's static public key (32 bytes)
else:
    plaintext = bytes(32)  # All zeros for unbound

ciphertext = ENCRYPT(k, nonce, plaintext, associated_data)
# ciphertext = 32 bytes encrypted + 16 bytes MAC = 48 bytes

# Mix ciphertext into hash
h = SHA256(h || ciphertext)

# State: Static key section encrypted, h updated
# Send ciphertext (48 bytes) as next part of NS message
```
### KDF 5: NS-Nutzdatenabschnitt (ss DH, nur gebunden)

Für gebundene Sessions einen zweiten DH für die Nutzlastverschlüsselung durchführen:

```python
if binding_requested:
    # Alice's static keys
    ask = GENERATE_PRIVATE()  # Alice's long-term key
    apk = DERIVE_PUBLIC(ask)
    
    # Perform second DH (static-static)
    sharedSecret = DH(ask, bpk)  # Alice computes
    # Equivalent: sharedSecret = DH(bsk, apk)  # Bob computes
    
    # Derive cipher key
    keydata = HKDF(chainKey, sharedSecret, "", 64)
    chainKey = keydata[0:31]
    k = keydata[32:63]
    
    nonce = 0
    associated_data = h
else:
    # Unbound: reuse keys from static key section
    # chainKey and k unchanged
    nonce = 1  # Increment nonce (reusing same key)
    associated_data = h

# Encrypt payload
payload = build_payload()  # DateTime + Garlic Cloves + etc.
ciphertext = ENCRYPT(k, nonce, payload, associated_data)

# Mix ciphertext into hash
h = SHA256(h || ciphertext)

# State: Payload encrypted, h contains complete NS transcript
# Save chainKey and h for NSR processing
# Send ciphertext as final part of NS message
```
**Wichtige Hinweise:**

1. **Bound (gebunden) vs Unbound (ungebunden)**: 
   - Bound führt 2 DH-Operationen durch (es + ss)
   - Unbound führt 1 DH-Operation durch (nur es)
   - Unbound inkrementiert die Nonce, anstatt einen neuen Schlüssel abzuleiten

2. **Sicherheit vor Schlüsselwiederverwendung**:
   - Unterschiedliche Nonces (Einmalwerte) (0 vs 1) verhindern die Wiederverwendung desselben Schlüssel/Nonce-Paares
   - Unterschiedliche Associated Data (zusätzliche authentifizierte Daten) (h ist unterschiedlich) sorgen für Domänentrennung

3. **Hash-Transkript**:
   - `h` enthält jetzt: protocol_name, leerer Prolog, bpk, aepk, static_key_ciphertext, payload_ciphertext
   - Dieses Transkript verknüpft alle Teile der NS-Nachricht miteinander

### NSR Reply Tagset KDF (Schlüsselableitungsfunktion)

Bob generiert Tags für NSR-Nachrichten:

```python
# Chain key from NS payload section
# chainKey = final chainKey from NS KDF

# Generate tagset key
tagsetKey = HKDF(chainKey, ZEROLEN, "SessionReplyTags", 32)

# Initialize NSR tagset (see DH_INITIALIZE below)
tagset_nsr = DH_INITIALIZE(chainKey, tagsetKey)

# Get tag for this NSR
tagsetEntry = tagset_nsr.GET_NEXT_ENTRY()
tag = tagsetEntry.SESSION_TAG  # 8 bytes

# State: tag available for NSR message
# Send tag as first 8 bytes of NSR
```
### KDFs für NSR-Nachrichten (Schlüsselableitungsfunktionen)

### KDF 6: Ephemere Schlüsselerzeugung für NSR

Bob generiert für jede NSR einen frischen ephemeren Schlüssel:

```python
# Mix tag into hash (I2P extension to Noise)
h = SHA256(h || tag)

# Generate ephemeral key pair
besk = GENERATE_PRIVATE_ELG2()
bepk = DERIVE_PUBLIC(besk)

# Mix ephemeral public key into hash
h = SHA256(h || bepk)

# Elligator2 encode for transmission
elg2_bepk = ENCODE_ELG2(bepk)

# State: h updated with tag and Bob's ephemeral key
# Send elg2_bepk as bytes 9-40 of NSR message
```
### KDF 7: NSR-Schlüsselabschnitt (ee und se DH)

Leitet Schlüssel für den NSR-Schlüsselabschnitt ab:

```python
# Perform third DH (ephemeral-ephemeral)
sharedSecret_ee = DH(aesk, bepk)  # Alice computes
# Equivalent: sharedSecret_ee = DH(besk, aepk)  # Bob computes

# Mix ee into chain
keydata = HKDF(chainKey, sharedSecret_ee, "", 32)
chainKey = keydata[0:31]

# Perform fourth DH (static-ephemeral)
sharedSecret_se = DH(ask, bepk)  # Alice computes
# Equivalent: sharedSecret_se = DH(besk, apk)  # Bob computes

# Derive cipher key from se
keydata = HKDF(chainKey, sharedSecret_se, "", 64)
chainKey = keydata[0:31]
k = keydata[32:63]

# AEAD encryption of empty data (key section has no payload)
nonce = 0
associated_data = h
ciphertext = ENCRYPT(k, nonce, ZEROLEN, associated_data)
# ciphertext = 16 bytes (MAC only, no plaintext)

# Mix ciphertext into hash
h = SHA256(h || ciphertext)

# State: Key section encrypted, chainKey contains all 4 DH results
# Send ciphertext (16 bytes MAC) as bytes 41-56 of NSR
```
**Kritisch**: Dies vervollständigt den Noise IK handshake (Handshake des Noise-IK-Protokolls). `chainKey` enthält nun Beiträge aus allen 4 DH-Operationen (es, ss, ee, se).

### KDF 8: NSR-Nutzlastabschnitt

Leitet Schlüssel für die NSR-Nutzlastverschlüsselung ab:

```python
# Split chainKey into bidirectional keys
keydata = HKDF(chainKey, ZEROLEN, "", 64)
k_ab = keydata[0:31]   # Alice → Bob key
k_ba = keydata[32:63]  # Bob → Alice key

# Initialize ES tagsets for both directions
tagset_ab = DH_INITIALIZE(chainKey, k_ab)  # Alice → Bob
tagset_ba = DH_INITIALIZE(chainKey, k_ba)  # Bob → Alice

# Derive NSR payload key (Bob → Alice)
k_nsr = HKDF(k_ba, ZEROLEN, "AttachPayloadKDF", 32)

# Encrypt NSR payload
nonce = 0
associated_data = h  # Binds payload to entire NSR
payload = build_payload()  # Usually application reply
ciphertext = ENCRYPT(k_nsr, nonce, payload, associated_data)

# State: Bidirectional ES sessions established
# tagset_ab and tagset_ba ready for ES messages
# Send ciphertext as bytes 57+ of NSR message
```
**Wichtige Hinweise:**

1. **Split-Operation**: 
   - Erzeugt unabhängige Schlüssel für jede Richtung
   - Verhindert die Wiederverwendung von Schlüsseln zwischen Alice→Bob und Bob→Alice

2. **NSR-Nutzlastbindung**:
   - Verwendet `h` als assoziierte Daten, um die Nutzlast an den Handshake zu binden
   - Eine separate KDF ("AttachPayloadKDF") sorgt für Domänentrennung

3. **ES-Bereitschaft**:
   - Nach dem NSR können beide Parteien ES-Nachrichten senden
   - Alice muss NSR empfangen, bevor sie ES sendet
   - Bob muss ES empfangen, bevor er ES sendet

### Schlüsselableitungsfunktionen für ES-Nachrichten

ES-Nachrichten verwenden vorgenerierte Sitzungsschlüssel aus tagsets:

```python
# Sender gets next tag and key
tagsetEntry = outbound_tagset.GET_NEXT_ENTRY()
tag = tagsetEntry.SESSION_TAG     # 8 bytes
k = tagsetEntry.SESSION_KEY       # 32 bytes
N = tagsetEntry.INDEX             # Message number

# Construct nonce (12 bytes)
nonce = [0x00, 0x00, 0x00, 0x00] + little_endian_8_bytes(N)

# AEAD encryption
associated_data = tag  # Tag is associated data
payload = build_payload()
ciphertext = ENCRYPT(k, nonce, payload, associated_data)

# Send: tag || ciphertext (8 + len(ciphertext) bytes)
```
**Empfängerprozess:**

```python
# Extract tag
tag = message[0:8]

# Look up tag in inbound tagsets
tagsetEntry = inbound_tagset.GET_SESSION_KEY(tag)
if tagsetEntry is None:
    # Not an ES message, try NS/NSR decryption
    return try_handshake_decryption(message)

k = tagsetEntry.SESSION_KEY
N = tagsetEntry.INDEX

# Construct nonce
nonce = [0x00, 0x00, 0x00, 0x00] + little_endian_8_bytes(N)

# AEAD decryption
associated_data = tag
ciphertext = message[8:]
try:
    payload = DECRYPT(k, nonce, ciphertext, associated_data)
except AuthenticationError:
    # MAC verification failed, reject message
    return reject_message()

# Process payload blocks
process_payload(payload)

# Remove tag from tagset (one-time use)
inbound_tagset.remove(tag)
```
### DH_INITIALIZE-Funktion

Erstellt ein Tagset für eine Richtung:

```python
def DH_INITIALIZE(rootKey, k):
    """
    Initializes a tagset with session tag and symmetric key ratchets.
    
    Args:
        rootKey: Chain key from previous DH ratchet (32 bytes)
        k: Key material from split() or DH ratchet (32 bytes)
    
    Returns:
        tagset: Initialized tagset object
    """
    # Derive next root key and chain key
    keydata = HKDF(rootKey, k, "KDFDHRatchetStep", 64)
    nextRootKey = keydata[0:31]
    chainKey_tagset = keydata[32:63]
    
    # Derive separate chain keys for tags and keys
    keydata = HKDF(chainKey_tagset, ZEROLEN, "TagAndKeyGenKeys", 64)
    sessTag_ck = keydata[0:31]   # Session tag chain key
    symmKey_ck = keydata[32:63]  # Symmetric key chain key
    
    # Create tagset object
    tagset = Tagset()
    tagset.nextRootKey = nextRootKey
    tagset.sessTag_chainKey = sessTag_ck
    tagset.symmKey_chainKey = symmKey_ck
    tagset.lastIndex = -1
    
    return tagset
```
**Nutzungskontexte:**

1. **NSR-Tagset**: `DH_INITIALIZE(chainKey_from_NS, tagsetKey_NSR)`
2. **ES-Tagsets**: `DH_INITIALIZE(chainKey_from_NSR, k_ab or k_ba)`
3. **Ratcheted Tagsets (mit schrittweiser Schlüsselaktualisierung)**: `DH_INITIALIZE(nextRootKey_from_previous, tagsetKey_from_DH)`

---

## Ratchet-Mechanismen (kryptografisches Verfahren zur fortlaufenden, vorwärtssicheren Schlüsselaktualisierung)

ECIES verwendet drei synchronisierte Ratchet-Mechanismen (kryptografische Ratschenmechanismen), um Vorwärtsgeheimnis zu gewährleisten und ein effizientes Sitzungsmanagement zu ermöglichen.

### Ratchet-Übersicht

**Drei Ratchet-Typen (Kryptografie-Mechanismus zur fortlaufenden Schlüsselaktualisierung):**

1. **DH Ratchet**: Führt Diffie-Hellman-Schlüsselaustausch durch, um neue Root-Schlüssel zu erzeugen
2. **Session Tag Ratchet**: Leitet einmalig verwendbare Session Tags (Sitzungs-Tags) deterministisch ab
3. **Symmetric Key Ratchet**: Leitet Sitzungsschlüssel für die Nachrichtenverschlüsselung ab

**Beziehung:**

```
DH Ratchet (periodic)
    ↓
Creates new tagset
    ↓
Session Tag Ratchet (per message) ← synchronized → Symmetric Key Ratchet (per message)
    ↓                                                      ↓
Session Tags (8 bytes each)                      Session Keys (32 bytes each)
```
**Wesentliche Eigenschaften:**

- **Sender**: Erzeugt Tags und Schlüssel bei Bedarf (kein Speicher erforderlich)
- **Empfänger**: Erzeugt Tags für ein Lookahead-Fenster im Voraus (Speicher erforderlich)
- **Synchronisierung**: Der Tag-Index bestimmt den Schlüsselindex (N_tag = N_key)
- **Vorwärtsgeheimnis**: Erreicht durch periodische DH ratchet (Diffie-Hellman-Ratsche, ein periodischer Schlüsselerneuerungsmechanismus)
- **Effizienz**: Der Empfänger kann die Schlüsselberechnung bis zum Empfang des Tags aufschieben

### DH Ratchet (Diffie-Hellman-Ratsche)

Die DH ratchet (Diffie-Hellman-Ratsche) gewährleistet Vorwärtsgeheimnis, indem in regelmäßigen Abständen neue ephemere Schlüssel ausgetauscht werden.

### DH-Ratchet-Frequenz

**Erforderliche Ratchet-Bedingungen (kryptografischer Schlüssel-Mechanismus):** - Tag-Menge kurz vor Erschöpfung (Tag 65535 ist das Maximum) - Implementierungsspezifische Richtlinien:   - Schwellwert für die Anzahl der Nachrichten (z. B. alle 4096 Nachrichten)   - Zeitschwelle (z. B. alle 10 Minuten)   - Schwellwert für Datenvolumen (z. B. alle 100 MB)

**Empfohlene erste Ratchet (Schlüsselwechsel-Mechanismus)**: Etwa bei Tagnummer 4096, um das Erreichen des Grenzwerts zu vermeiden

**Maximale Werte:** - **Maximale tag set ID** (Tag-Menge): 65535 - **Maximale Schlüssel-ID**: 32767 - **Maximale Nachrichten pro tag set**: 65535 - **Theoretisch maximales Datenvolumen pro Sitzung**: ~6.9 TB (64K tag sets × 64K Nachrichten × 1730 Bytes im Durchschnitt)

### DH Ratchet (Diffie-Hellman-basierter Ratchet-Mechanismus) Tag- und Schlüssel-IDs

**Initiales Tag-Set** (nach dem Handshake): - Tag-Set-ID: 0 - Es wurden noch keine NextKey-Blöcke (Blöcke für den nächsten Schlüssel) gesendet - Keine Schlüssel-IDs zugewiesen

**Nach dem ersten Ratchet**: - Tag-Set-ID: 1 = (1 + Alices Schlüssel-ID + Bobs Schlüssel-ID) = (1 + 0 + 0) - Alice sendet NextKey (Nachfolgeschlüssel) mit Schlüssel-ID 0 - Bob antwortet mit NextKey mit Schlüssel-ID 0

**Nachfolgende Tag-Sets**: - Tag-Set-ID = 1 + Sender-Schlüssel-ID + Empfänger-Schlüssel-ID - Beispiel: Tag-Set 5 = (1 + sender_key_2 + receiver_key_2)

**Fortschrittstabelle für Tag-Sets:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Tag Set ID</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Sender Key ID</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Receiver Key ID</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">n/a</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">n/a</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Initial tag set (post-NSR)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">First ratchet (both generate new keys)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Sender generates new key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Receiver generates new key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Sender generates new key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Receiver generates new key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">...</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">...</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">...</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Pattern repeats</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">65534</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32767 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32766</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Second-to-last tag set</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">65535</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32767</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32767 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Final tag set</td>
    </tr>
  </tbody>
</table>
\* = Neuer Schlüssel in diesem ratchet (Mechanismus zur Schlüsselaktualisierung) erzeugt

**Schlüssel-ID-Regeln:** - IDs sind fortlaufend und beginnen bei 0 - IDs erhöhen sich nur, wenn ein neuer Schlüssel erzeugt wird - Maximale Schlüssel-ID ist 32767 (15 Bit) - Nach der Schlüssel-ID 32767 ist eine neue Sitzung erforderlich

### Nachrichtenfluss der DH Ratchet (Diffie-Hellman-basiertes Schlüsselerneuerungsverfahren)

**Rollen:** - **Tag-Sender**: Besitzt das ausgehende Tag-Set, sendet Nachrichten - **Tag-Empfänger**: Besitzt das eingehende Tag-Set, empfängt Nachrichten

**Muster:** Der Tag-Sender initiiert das ratchet (Schlüsselwechselmechanismus), wenn die Tag-Menge fast erschöpft ist.

**Nachrichtenflussdiagramm:**

```
Tag Sender                         Tag Receiver

       ... using tag set #0 ...

(Tag set #0 approaching exhaustion)
(Generate new key #0)

NextKey forward, request reverse, with key #0  -------->
(Repeat until NextKey ACK received)
                                   (Generate new key #0)
                                   (Perform DH: sender_key_0 × receiver_key_0)
                                   (Create inbound tag set #1)

        <---------------           NextKey reverse, with key #0
                                   (Repeat until tag from tag set #1 received)

(Receive NextKey with key #0)
(Perform DH: sender_key_0 × receiver_key_0)
(Create outbound tag set #1)


       ... using tag set #1 ...


(Tag set #1 approaching exhaustion)
(Generate new key #1)

NextKey forward, with key #1        -------->
(Repeat until NextKey ACK received)
                                   (Reuse existing key #0)
                                   (Perform DH: sender_key_1 × receiver_key_0)
                                   (Create inbound tag set #2)

        <--------------            NextKey reverse, id 0 (ACK)
                                   (Repeat until tag from tag set #2 received)

(Receive NextKey with id 0)
(Perform DH: sender_key_1 × receiver_key_0)
(Create outbound tag set #2)


       ... using tag set #2 ...


(Tag set #2 approaching exhaustion)
(Reuse existing key #1)

NextKey forward, request reverse, id 1  -------->
(Repeat until NextKey received)
                                   (Generate new key #1)
                                   (Perform DH: sender_key_1 × receiver_key_1)
                                   (Create inbound tag set #3)

        <--------------            NextKey reverse, with key #1

(Receive NextKey with key #1)
(Perform DH: sender_key_1 × receiver_key_1)
(Create outbound tag set #3)


       ... using tag set #3 ...

       (Pattern repeats: even-numbered tag sets
        use forward key, odd-numbered use reverse key)
```
**Ratchet-Patterns (Mechanismen zur schrittweisen Schlüsselaktualisierung):**

**Erstellen von Tag Sets (Tag-Sets) mit geraden Nummern** (2, 4, 6, ...): 1. Der Sender erzeugt einen neuen Schlüssel 2. Der Sender sendet NextKey block (NextKey-Block) mit neuem Schlüssel 3. Der Empfänger sendet NextKey block mit der alten Schlüssel-ID (ACK) 4. Beide führen DH (Diffie-Hellman) mit (neuem Sender-Schlüssel × altem Empfänger-Schlüssel) durch

**Erstellen von Tag-Sets mit ungeraden Nummern** (3, 5, 7, ...): 1. Absender fordert reverse key (Schlüssel für die Gegenrichtung) an (sendet NextKey mit Request-Flag) 2. Empfänger erzeugt neuen Schlüssel 3. Empfänger sendet NextKey-Block mit neuem Schlüssel 4. Beide führen DH mit (altem Absender-Schlüssel × neuem Empfänger-Schlüssel) aus

### NextKey-Block-Format

Siehe den Abschnitt zum Payload-Format für eine detaillierte Spezifikation des NextKey-Blocks.

**Zentrale Elemente:** - **Flags-Byte**:   - Bit 0: Schlüssel vorhanden (1) oder nur ID (0)   - Bit 1: Rückwärtsschlüssel (1) oder Vorwärtsschlüssel (0)   - Bit 2: Rückwärtsschlüssel anfordern (1) oder keine Anforderung (0) - **Schlüssel-ID**: 2 Bytes, Big-Endian (0-32767) - **Öffentlicher Schlüssel**: 32 Bytes X25519 (wenn Bit 0 = 1)

**Beispiele für NextKey Blocks (NextKey-Blöcke):**

```python
# Sender initiates ratchet with new key (key ID 0, tag set 1)
NextKey(flags=0x01, key_id=0, pubkey=sender_key_0)

# Receiver replies with new key (key ID 0, tag set 1)
NextKey(flags=0x03, key_id=0, pubkey=receiver_key_0)

# Sender ratchets again with new key (key ID 1, tag set 2)
NextKey(flags=0x01, key_id=1, pubkey=sender_key_1)

# Receiver ACKs with old key ID (tag set 2)
NextKey(flags=0x02, key_id=0)

# Sender requests reverse key (tag set 3)
NextKey(flags=0x04, key_id=1)

# Receiver sends new reverse key (key ID 1, tag set 3)
NextKey(flags=0x03, key_id=1, pubkey=receiver_key_1)
```
### KDF der DH-Ratsche

Wenn neue Schlüssel ausgetauscht werden:

```python
# Tag sender generates or reuses key
if generating_new:
    sender_sk = GENERATE_PRIVATE()
    sender_pk = DERIVE_PUBLIC(sender_sk)
else:
    # Reuse existing key pair
    sender_pk = existing_sender_pk

# Tag receiver generates or reuses key
if generating_new:
    receiver_sk = GENERATE_PRIVATE()
    receiver_pk = DERIVE_PUBLIC(receiver_sk)
else:
    # Reuse existing key pair
    receiver_pk = existing_receiver_pk

# Both parties perform DH
sharedSecret = DH(sender_sk, receiver_pk)

# Derive tagset key
tagsetKey = HKDF(sharedSecret, ZEROLEN, "XDHRatchetTagSet", 32)

# Get next root key from previous tagset
rootKey = previous_tagset.nextRootKey

# Initialize new tagset
new_tagset = DH_INITIALIZE(rootKey, tagsetKey)

# Tag sender: outbound tagset
# Tag receiver: inbound tagset
```
**Kritisches Timing:**

**Tag-Sender:** - Erstellt sofort ein neues ausgehendes Tag-Set - Beginnt sofort, neue Tags zu verwenden - Löscht das alte ausgehende Tag-Set

**Tag-Empfänger:** - erstellt einen neuen eingehenden Tag-Satz - behält den alten eingehenden Tag-Satz während einer Schonfrist (3 Minuten) bei - akzeptiert Tags sowohl aus dem alten als auch aus dem neuen Tag-Satz während der Schonfrist - löscht den alten eingehenden Tag-Satz nach Ablauf der Schonfrist

### Verwaltung des DH-Ratchet-Zustands (Diffie-Hellman-Ratchet, Schlüsselfortschrittsmechanismus)

**Senderzustand:** - Aktueller ausgehender Tag-Satz - Tag-Satz-ID und Schlüssel-IDs - Nächster Root-Schlüssel (für die nächste ratchet; Kryptographie-Ratchet-Mechanismus) - Anzahl der Nachrichten im aktuellen Tag-Satz

**Empfängerstatus:** - Aktuelle eingehende Tag-Menge(n) (kann während der Übergangsphase 2 haben) - Vorherige Nachrichtennummern (PN) zur Lückenerkennung - Vorausschaufenster vorab erzeugter Tags - Nächster Root-Schlüssel (für die nächste ratchet (Schlüssel-Fortschrittsmechanismus))

**Zustandsübergangsregeln:**

1. **Vor dem ersten Ratchet (Schlüsselaktualisierungsmechanismus)**:
   - Verwendung von Tag-Set 0 (aus NSR)
   - Keine Schlüssel-IDs zugewiesen

2. **Ratchet (kryptografischer Ratschenmechanismus) initialisieren**:
   - Neuen Schlüssel generieren (falls der Absender in dieser Runde an der Reihe ist)
   - NextKey-Block in ES-Nachricht senden
   - Vor dem Erstellen eines neuen ausgehenden Tag-Sets auf die NextKey-Antwort warten

3. **Empfangen einer Ratchet-Anfrage (kryptografischer Fortschalt-Mechanismus)**:
   - Neuen Schlüssel erzeugen (falls der Empfänger in dieser Runde generiert)
   - Diffie-Hellman (DH) mit dem empfangenen Schlüssel durchführen
   - Neues eingehendes tag set (Satz von Session-Tags) erstellen
   - NextKey-Antwort senden
   - Altes eingehendes tag set für eine Schonfrist beibehalten

4. **Ratchet (Schlüsselwechselmechanismus) abschließen**:
   - NextKey-Antwort empfangen
   - DH durchführen
   - Neues ausgehendes Tagset erstellen
   - Neue Tags verwenden

### Session Tag Ratchet (kryptografischer Erneuerungsmechanismus für Session-Tags)

Das session tag ratchet (Ratschenmechanismus für session tags) erzeugt deterministisch 8-Byte session tags zur einmaligen Verwendung.

### Zweck der Session Tag Ratchet

- Ersetzt die explizite Tag-Übertragung (ElGamal sendete 32-Byte-Tags)
- Ermöglicht dem Empfänger, Tags vorab für ein Look-ahead-Fenster (Vorausschaufenster) zu generieren
- Der Sender generiert bei Bedarf (keine Speicherung erforderlich)
- Synchronisiert sich über einen Index mit dem symmetric key ratchet (symmetrisches Schlüssel-Ratchet)

### Session-Tag-Ratchet-Formel (Kryptografie-Mechanismus für schrittweise Schlüsselaktualisierung)

**Initialisierung:**

```python
# From DH_INITIALIZE
sessTag_ck = initial_chain_key  # 32 bytes

# Initialize session tag ratchet
keydata = HKDF(sessTag_ck, ZEROLEN, "STInitialization", 64)
sessTag_chainKey = keydata[0:31]    # First chain key
SESSTAG_CONSTANT = keydata[32:63]   # Constant for all tags in this tagset
```
**Tag-Generierung (für Tag N):**

```python
# Generate tag N
keydata = HKDF(sessTag_chainKey_(N-1), SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
sessTag_chainKey_N = keydata[0:31]  # Chain key for next tag
tag_N = keydata[32:39]              # Session tag (8 bytes)

# Chain continues for each tag
# tag_0, tag_1, tag_2, ..., tag_65535
```
**Vollständige Sequenz:**

```python
# Tag 0
keydata_0 = HKDF(sessTag_chainKey, SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
sessTag_chainKey_0 = keydata_0[0:31]
tag_0 = keydata_0[32:39]

# Tag 1
keydata_1 = HKDF(sessTag_chainKey_0, SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
sessTag_chainKey_1 = keydata_1[0:31]
tag_1 = keydata_1[32:39]

# Tag N
keydata_N = HKDF(sessTag_chainKey_(N-1), SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
sessTag_chainKey_N = keydata_N[0:31]
tag_N = keydata_N[32:39]
```
### Implementierung des Session Tag Ratchet-Senders (Ratschenmechanismus für Session-Tags)

```python
class OutboundTagset:
    def __init__(self, sessTag_ck):
        # Initialize
        keydata = HKDF(sessTag_ck, ZEROLEN, "STInitialization", 64)
        self.chainKey = keydata[0:31]
        self.constant = keydata[32:63]
        self.index = -1
    
    def get_next_tag(self):
        # Increment index
        self.index += 1
        
        if self.index > 65535:
            raise TagsetExhausted("Ratchet required")
        
        # Generate tag
        keydata = HKDF(self.chainKey, self.constant, "SessionTagKeyGen", 64)
        self.chainKey = keydata[0:31]
        tag = keydata[32:39]
        
        return (tag, self.index)
```
**Senderprozess:** 1. Rufen Sie `get_next_tag()` für jede Nachricht auf 2. Verwenden Sie den zurückgegebenen tag (Markierung) in der ES-Nachricht 3. Speichern Sie den Index N für eine mögliche Nachverfolgung von ACK (Bestätigung) 4. Keine tag-Speicherung erforderlich (wird bei Bedarf erzeugt)

### Implementierung des Empfängers für das Session Tag Ratchet (Mechanismus zur schrittweisen Aktualisierung der Session Tags)

```python
class InboundTagset:
    def __init__(self, sessTag_ck, look_ahead=32):
        # Initialize
        keydata = HKDF(sessTag_ck, ZEROLEN, "STInitialization", 64)
        self.chainKey = keydata[0:31]
        self.constant = keydata[32:63]
        self.index = -1
        self.look_ahead = look_ahead
        self.tags = {}  # Dictionary: tag -> index
        
        # Pre-generate initial tags
        self.extend(look_ahead)
    
    def extend(self, count):
        """Generate 'count' more tags"""
        for _ in range(count):
            self.index += 1
            
            if self.index > 65535:
                return  # Cannot exceed maximum
            
            # Generate tag
            keydata = HKDF(self.chainKey, self.constant, "SessionTagKeyGen", 64)
            self.chainKey = keydata[0:31]
            tag = keydata[32:39]
            
            # Store tag
            self.tags[tag] = self.index
    
    def lookup_tag(self, tag):
        """Look up tag and return index"""
        if tag in self.tags:
            index = self.tags[tag]
            # Remove tag (one-time use)
            del self.tags[tag]
            return index
        return None
    
    def check_and_extend(self):
        """Extend if tag count is low"""
        current_count = len(self.tags)
        if current_count < self.look_ahead // 2:
            # Extend to restore window
            self.extend(self.look_ahead - current_count)
```
**Empfängerprozess:** 1. Tags (Sitzungskennzeichen) für das Lookahead-Fenster vorab generieren (z. B. 32 Tags) 2. Tags in einer Hashtabelle oder einem Dictionary speichern 3. Bei Nachrichteneingang den Tag nachschlagen, um Index N zu erhalten 4. Tag aus dem Speicher entfernen (Einmalverwendung) 5. Fenster erweitern, wenn die Tag-Anzahl unter den Schwellenwert fällt

### Vorausschau-Strategie für Session Tags (Sitzungs-Tags)

**Zweck**: Abwägen zwischen Speicherverbrauch und der Verarbeitung von Nachrichten, die nicht in der richtigen Reihenfolge eintreffen

**Empfohlene Vorausschau-Größen:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Tagset Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Initial Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Maximum Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR tagset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Short-lived</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ES tagset 0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">24</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">160</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Initial ES tagset</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ES tagset 1+</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">160</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">160</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Ratcheted tagsets</td>
    </tr>
  </tbody>
</table>
**Adaptive Vorausschau:**

```python
# Dynamic look-ahead based on highest tag received
look_ahead = min(tsmax, tsmin + N // 4)

# Example:
# tsmin = 24, tsmax = 160
# N = 0:   look_ahead = min(160, 24 + 0/4) = 24
# N = 100: look_ahead = min(160, 24 + 100/4) = 49
# N = 500: look_ahead = min(160, 24 + 500/4) = 149
# N = 544: look_ahead = min(160, 24 + 544/4) = 160
```
**Am Ende kürzen:**

```python
# Trim tags far behind highest received
trim_behind = look_ahead // 2

# If highest received tag is N=100, trim tags below N=50
```
**Speicherberechnung:**

```python
# Per tag: 8 bytes (tag) + 2 bytes (index) + overhead ≈ 16 bytes
# Look-ahead of 160 tags ≈ 2.5 KB per inbound tagset

# With multiple sessions:
# 100 inbound sessions × 2.5 KB = 250 KB total
```
### Behandlung von Session-Tags außerhalb der Reihenfolge

**Szenario**: Nachrichten kommen in falscher Reihenfolge an

```
Expected: tag_5, tag_6, tag_7, tag_8
Received: tag_5, tag_7, tag_6, tag_8
```
**Empfängerverhalten:**

1. Empfange tag_5:
   - Nachschlagen: bei Index 5 gefunden
   - Nachricht verarbeiten
   - tag_5 entfernen
   - Bisher höchstes empfangenes: 5

2. Empfang von tag_7 (außerhalb der Reihenfolge):
   - Nachschlagen: bei Index 7 gefunden
   - Nachricht verarbeiten
   - tag_7 entfernen
   - Bisher höchster empfangener Wert: 7
   - Hinweis: tag_6 noch im Speicher (noch nicht empfangen)

3. Empfange tag_6 (verzögert):
   - Nachsehen: bei Index 6 gefunden
   - Nachricht verarbeiten
   - tag_6 entfernen
   - Höchster empfangener Wert: 7 (unverändert)

4. tag_8 empfangen:
   - Nachschlagen: bei Index 8 gefunden
   - Nachricht verarbeiten
   - tag_8 entfernen
   - Höchster Empfang: 8

**Fensterverwaltung:** - Den höchsten empfangenen Index nachverfolgen - Liste fehlender Indizes (Lücken) führen - Fenster basierend auf dem höchsten Index erweitern - Optional: Alte Lücken nach einem Timeout verwerfen

### Symmetric Key Ratchet (symmetrisches Schlüssel-Ratschenverfahren)

Das symmetric key ratchet (symmetrischer Mechanismus zur fortlaufenden Schlüsselerneuerung) erzeugt 32-Byte-Verschlüsselungsschlüssel, die mit den session tags (Sitzungs-Tags) synchronisiert sind.

### Zweck der Symmetric Key Ratchet (symmetrische KDF-Kette)

- Stellt für jede Nachricht einen eindeutigen Verschlüsselungsschlüssel bereit
- Synchronisiert mit session tag ratchet (Ratchet-Mechanismus für Sitzungstags; gleicher Index)
- Absender kann bei Bedarf generieren
- Empfänger kann die Generierung aufschieben, bis der Tag empfangen wurde

### Formel für die Symmetric Key Ratchet (Schlüsselfortschrittsmechanismus)

**Initialisierung:**

```python
# From DH_INITIALIZE
symmKey_ck = initial_chain_key  # 32 bytes

# No additional initialization needed
# Unlike session tag ratchet, no constant is derived
```
**Schlüsselgenerierung (für Schlüssel N):**

```python
# Generate key N
SYMMKEY_CONSTANT = ZEROLEN  # Empty string
keydata = HKDF(symmKey_chainKey_(N-1), SYMMKEY_CONSTANT, "SymmetricRatchet", 64)
symmKey_chainKey_N = keydata[0:31]  # Chain key for next key
key_N = keydata[32:63]              # Session key (32 bytes)
```
**Vollständige Abfolge:**

```python
# Key 0
keydata_0 = HKDF(symmKey_ck, ZEROLEN, "SymmetricRatchet", 64)
symmKey_chainKey_0 = keydata_0[0:31]
key_0 = keydata_0[32:63]

# Key 1
keydata_1 = HKDF(symmKey_chainKey_0, ZEROLEN, "SymmetricRatchet", 64)
symmKey_chainKey_1 = keydata_1[0:31]
key_1 = keydata_1[32:63]

# Key N
keydata_N = HKDF(symmKey_chainKey_(N-1), ZEROLEN, "SymmetricRatchet", 64)
symmKey_chainKey_N = keydata_N[0:31]
key_N = keydata_N[32:63]
```
### Implementierung des Symmetric Key Ratchet Senders (symmetrischer Schlüssel-Ratschenmechanismus)

```python
class OutboundKeyRatchet:
    def __init__(self, symmKey_ck):
        self.chainKey = symmKey_ck
        self.index = -1
    
    def get_key(self, index):
        """Generate key for specific index"""
        # Fast-forward to desired index if needed
        while self.index < index:
            self.index += 1
            keydata = HKDF(self.chainKey, ZEROLEN, "SymmetricRatchet", 64)
            self.chainKey = keydata[0:31]
            if self.index == index:
                return keydata[32:63]
        
        # Should not reach here if called correctly
        raise ValueError("Key already generated")
```
**Sendeprozess:** 1. Ermittle den nächsten Tag (Kennzeichen) und dessen Index N 2. Erzeuge einen Schlüssel für Index N 3. Verwende den Schlüssel, um die Nachricht zu verschlüsseln 4. Keine Schlüsselspeicherung erforderlich

### Implementierung des Empfängers für die Symmetric Key Ratchet (symmetrischer Schlüssel-Ratschenmechanismus)

**Strategie 1: Verzögerte Generierung (Empfohlen)**

```python
class InboundKeyRatchet:
    def __init__(self, symmKey_ck):
        self.chainKey = symmKey_ck
        self.index = -1
        self.cache = {}  # Optional: cache recently used keys
    
    def get_key(self, index):
        """Generate key for specific index"""
        # Check cache first (optional optimization)
        if index in self.cache:
            key = self.cache[index]
            del self.cache[index]
            return key
        
        # Fast-forward to desired index
        while self.index < index:
            self.index += 1
            keydata = HKDF(self.chainKey, ZEROLEN, "SymmetricRatchet", 64)
            self.chainKey = keydata[0:31]
            
            if self.index == index:
                return keydata[32:63]
        
        raise ValueError("Index already passed")
```
**Aufgeschobener Generierungsprozess:** 1. ES-Nachricht mit Tag empfangen 2. Tag nachschlagen, um den Index N zu erhalten 3. Schlüssel 0 bis N erzeugen (falls noch nicht erzeugt) 4. Schlüssel N verwenden, um die Nachricht zu entschlüsseln 5. Chain key (Kettenschlüssel) ist jetzt am Index N positioniert

**Vorteile:** - Minimaler Speicherverbrauch - Schlüssel werden nur bei Bedarf erzeugt - Einfache Implementierung

**Nachteile:** - Muss bei der ersten Verwendung alle Schlüssel von 0 bis N erzeugen - Kann Nachrichten, die nicht in der richtigen Reihenfolge eintreffen, ohne Zwischenspeicherung nicht verarbeiten

**Strategie 2: Vorgenerierung mit Tag Window (Tag-Fenster) (Alternative)**

```python
class InboundKeyRatchet:
    def __init__(self, symmKey_ck):
        self.chainKey = symmKey_ck
        self.index = -1
        self.keys = {}  # Dictionary: index -> key
    
    def extend(self, count):
        """Pre-generate 'count' more keys"""
        for _ in range(count):
            self.index += 1
            keydata = HKDF(self.chainKey, ZEROLEN, "SymmetricRatchet", 64)
            self.chainKey = keydata[0:31]
            key = keydata[32:63]
            self.keys[self.index] = key
    
    def get_key(self, index):
        """Retrieve pre-generated key"""
        if index in self.keys:
            key = self.keys[index]
            del self.keys[index]
            return key
        return None
```
**Vorgenerierungsprozess:** 1. Schlüssel vorgenerieren, entsprechend dem tag window (Fenster für Tags) (z. B. 32 Schlüssel) 2. Schlüssel speichern, indexiert nach der Nachrichtennummer 3. Wenn ein tag empfangen wird, den entsprechenden Schlüssel nachschlagen 4. Fenster erweitern, wenn tags verwendet werden

**Vorteile:** - Kommt von Haus aus mit nicht in der richtigen Reihenfolge eintreffenden Nachrichten zurecht - Schneller Schlüsselabruf (keine Generierungsverzögerung)

**Nachteile:** - Höherer Speicherverbrauch (32 Bytes pro Schlüssel gegenüber 8 Bytes pro tag (Markierung)) - Schlüssel müssen mit tags synchron gehalten werden

**Speichervergleich:**

```python
# Look-ahead of 160:
# Tags only:  160 × 16 bytes = 2.5 KB
# Tags+Keys:  160 × (16 + 32) bytes = 7.5 KB
# 
# For 100 sessions:
# Tags only:  250 KB
# Tags+Keys:  750 KB
```
### Synchronisierung von Symmetric Ratchet (symmetrischer Ratchet-Mechanismus) mit Session-Tags

**Kritische Anforderung**: Der Session-Tag-Index (Index des Sitzungs-Tags) MUSS dem Index des symmetrischen Schlüssels gleich sein

```python
# Sender
tag, index = outbound_tagset.get_next_tag()
key = outbound_keyratchet.get_key(index)  # Same index
nonce = construct_nonce(index)
ciphertext = ENCRYPT(key, nonce, payload, tag)

# Receiver
index = inbound_tagset.lookup_tag(tag)
key = inbound_keyratchet.get_key(index)  # Same index
nonce = construct_nonce(index)
plaintext = DECRYPT(key, nonce, ciphertext, tag)
```
**Fehlermodi:**

Wenn die Synchronisierung abbricht: - Falscher Schlüssel für die Entschlüsselung verwendet - MAC-Überprüfung schlägt fehl - Nachricht abgelehnt

**Prävention:** - Verwenden Sie immer denselben Index für Tag und Schlüssel - Überspringen Sie in keinem der beiden Ratchets (kryptografischer Ratchet-Mechanismus) Indizes - Gehen Sie mit außer der Reihenfolge eingehenden Nachrichten sorgfältig um

### Konstruktion der Nonce (Einmalwert) im symmetrischen Ratchet (Ratschenmechanismus)

Die Nonce (Einmalwert) wird aus der Nachrichtennummer abgeleitet:

```python
def construct_nonce(index):
    """
    Construct 12-byte nonce for ChaCha20-Poly1305
    
    Args:
        index: Message number (0-65535)
    
    Returns:
        nonce: 12-byte nonce
    """
    # First 4 bytes are always zero
    nonce = bytearray(12)
    nonce[0:4] = b'\x00\x00\x00\x00'
    
    # Last 8 bytes are little-endian message number
    nonce[4:12] = index.to_bytes(8, byteorder='little')
    
    return bytes(nonce)
```
**Beispiele:**

```python
index = 0:     nonce = 0x00000000 0000000000000000
index = 1:     nonce = 0x00000000 0100000000000000
index = 255:   nonce = 0x00000000 FF00000000000000
index = 256:   nonce = 0x00000000 0001000000000000
index = 65535: nonce = 0x00000000 FFFF000000000000
```
**Wichtige Eigenschaften:** - Nonces sind für jede Nachricht in einem tagset (Satz von Tags) eindeutig - Nonces wiederholen sich niemals (Tags zur einmaligen Verwendung stellen dies sicher) - 8-Byte-Zähler ermöglicht 2^64 Nachrichten (wir verwenden nur 2^16) - Das Nonce-Format entspricht der zählerbasierten Konstruktion nach RFC 7539

---

## Sitzungsverwaltung

### Sitzungskontext

Alle eingehenden und ausgehenden Sitzungen müssen zu einem bestimmten Kontext gehören:

1. **Router-Kontext**: Sitzungen für den Router selbst
2. **Ziel-Kontext**: Sitzungen für ein spezifisches lokales Ziel (Client-Anwendung)

**Kritische Regel**: Sitzungen dürfen NICHT zwischen Kontexten geteilt werden, um Korrelationsangriffe zu verhindern.

**Implementierung:**

```python
class SessionKeyManager:
    """Context for managing sessions (router or destination)"""
    def __init__(self, context_id):
        self.context_id = context_id
        self.inbound_sessions = {}   # far_end_dest -> [sessions]
        self.outbound_sessions = {}  # far_end_dest -> session
        self.static_keypair = generate_keypair()  # Context's identity
    
    def get_outbound_session(self, destination):
        """Get or create outbound session to destination"""
        if destination not in self.outbound_sessions:
            self.outbound_sessions[destination] = create_outbound_session(destination)
        return self.outbound_sessions[destination]
    
    def add_inbound_session(self, session, destination=None):
        """Add inbound session, optionally bound to destination"""
        if destination:
            if destination not in self.inbound_sessions:
                self.inbound_sessions[destination] = []
            self.inbound_sessions[destination].append(session)
        else:
            # Unbound session
            self.inbound_sessions[None].append(session)
```
**Java-I2P-Implementierung:**

In Java I2P stellt die Klasse `SessionKeyManager` folgende Funktionalität bereit: - Ein `SessionKeyManager` pro router - Ein `SessionKeyManager` pro lokaler Destination (Zieladresse) - Getrennte Verwaltung der ECIES- und ElGamal-Sitzungen innerhalb jedes Kontexts

### Sitzungsbindung

**Bindung** verknüpft eine Sitzung mit einer bestimmten Destination (Zielkennung) der Gegenstelle.

### Gebundene Sitzungen

**Eigenschaften:** - Enthält den statischen Schlüssel des Senders in der NS-Nachricht - Empfänger kann die destination (I2P-Zieladresse) des Senders identifizieren - Ermöglicht bidirektionale Kommunikation - Eine ausgehende Sitzung pro destination - Kann mehrere eingehende Sitzungen haben (während Übergangsphasen)

**Anwendungsfälle:** - Streaming-Verbindungen (TCP-ähnlich) - Beantwortbare Datagramme - Jedes Protokoll, das Anfrage/Antwort erfordert

**Bindevorgang:**

```python
# Alice creates bound outbound session
outbound_session = OutboundSession(
    destination=bob_destination,
    static_key=alice_static_key,
    bound=True
)

# Alice sends NS with static key
ns_message = build_ns_message(
    ephemeral_key=alice_ephemeral_key,
    static_key=alice_static_key,  # Included for binding
    payload=data
)

# Bob receives NS
bob_receives_ns(ns_message)
# Bob extracts Alice's static key
alice_static_key = decrypt_static_key_section(ns_message)

# Bob looks up Alice's destination (from bundled LeaseSet)
alice_destination = lookup_destination_by_static_key(alice_static_key)

# Bob creates bound inbound session
inbound_session = InboundSession(
    destination=alice_destination,
    bound=True
)

# Bob pairs with outbound session
outbound_session = OutboundSession(
    destination=alice_destination,
    bound=True
)
```
**Vorteile:** 1. **Ephemeral-Ephemeral DH**: Die Antwort verwendet ee DH (perfekte Vorwärtsgeheimhaltung) 2. **Sitzungskontinuität**: Ratchets (zustandsbehaftete Schlüsselerneuerungen) halten die Bindung zum selben Ziel aufrecht 3. **Sicherheit**: Verhindert Sitzungsübernahmen (authentifiziert durch statischen Schlüssel) 4. **Effizienz**: Eine einzelne Sitzung pro Ziel (keine Duplizierung)

### Ungebundene Sitzungen

**Eigenschaften:** - Kein statischer Schlüssel in der NS-Nachricht (Flags-Abschnitt besteht ausschließlich aus Nullen) - Empfänger kann den Absender nicht identifizieren - Nur unidirektionale Kommunikation - Mehrere Sitzungen zur gleichen Destination (Zieladresse) erlaubt

**Anwendungsfälle:** - Rohe Datagramme (fire-and-forget, ohne Bestätigung) - Anonymes Publizieren - Broadcast-ähnliche Nachrichtenübermittlung

**Eigenschaften:** - Anonymer (keine Absenderidentifikation) - Effizienter (1 DH vs 2 DH im Handshake) - Keine Antworten möglich (der Empfänger weiß nicht, wohin er antworten soll) - Kein session ratcheting (einmalige oder begrenzte Nutzung)

### Sitzungskopplung

**Kopplung** verbindet eine eingehende Sitzung mit einer ausgehenden Sitzung für die bidirektionale Kommunikation.

### Erstellen gekoppelter Sitzungen

**Alices Perspektive (Initiatorin):**

```python
# Create outbound session to Bob
outbound_session = create_outbound_session(bob_destination)

# Create paired inbound session
inbound_session = create_inbound_session(
    paired_with=outbound_session,
    bound_to=bob_destination
)

# Link them
outbound_session.paired_inbound = inbound_session
inbound_session.paired_outbound = outbound_session

# Send NS message
send_ns_message(outbound_session, payload)
```
**Bobs Perspektive (Antwortender):**

```python
# Receive NS message
ns_message = receive_ns_message()

# Create inbound session
inbound_session = create_inbound_session_from_ns(ns_message)

# If NS contains static key (bound):
if ns_message.has_static_key():
    alice_destination = extract_destination(ns_message)
    inbound_session.bind_to(alice_destination)
    
    # Create paired outbound session
    outbound_session = create_outbound_session(alice_destination)
    
    # Link them
    outbound_session.paired_inbound = inbound_session
    inbound_session.paired_outbound = outbound_session

# Send NSR
send_nsr_message(inbound_session, outbound_session, payload)
```
### Vorteile der Sitzungskopplung

1. **In-Band-ACKs**: Können Nachrichten ohne separate clove (Teilnachricht im 'garlic'-Nachrichtenformat) bestätigen
2. **Effizientes Ratcheting**: Beide Richtungen führen den Ratchet (schrittweisen Schlüsselwechsel) synchron aus
3. **Flusskontrolle**: Kann Backpressure (Gegendruck) über gepaarte Sitzungen hinweg implementieren
4. **Zustandskonsistenz**: Einfacher, einen synchronisierten Zustand beizubehalten

### Regeln zur Sitzungszuordnung

- Ausgehende Sitzung kann ungepaart sein (ungebundenes NS)
- Eingehende Sitzung für gebundenes NS sollte gepaart sein
- Die Paarung erfolgt bei der Sitzungserstellung, nicht danach
- Gepaarte Sitzungen haben dieselbe Zielbindung
- Ratchets (Kryptographie-Ratchets) erfolgen unabhängig voneinander, sind jedoch koordiniert

### Lebenszyklus einer Sitzung

### Sitzungslebenszyklus: Erstellungsphase

**Ausgehender Sitzungsaufbau (Alice):**

```python
def create_outbound_session(destination, bound=True):
    session = OutboundSession()
    session.destination = destination
    session.bound = bound
    session.state = SessionState.NEW
    session.created_time = now()
    
    # Generate keys for NS message
    session.ephemeral_keypair = generate_elg2_keypair()
    if bound:
        session.static_key = context.static_keypair.public_key
    
    # Will be populated after NSR received
    session.outbound_tagset = None
    session.inbound_tagset = None
    
    return session
```
**Erstellung einer eingehenden Sitzung (Bob):**

```python
def create_inbound_session_from_ns(ns_message):
    session = InboundSession()
    session.state = SessionState.ESTABLISHED
    session.created_time = now()
    
    # Extract from NS
    session.remote_ephemeral_key = ns_message.ephemeral_key
    session.remote_static_key = ns_message.static_key
    
    if session.remote_static_key:
        session.bound = True
        session.destination = lookup_destination(session.remote_static_key)
    else:
        session.bound = False
        session.destination = None
    
    # Generate keys for NSR
    session.ephemeral_keypair = generate_elg2_keypair()
    
    # Create tagsets from KDF
    session.inbound_tagset = create_tagset_from_nsr()
    session.outbound_tagset = create_tagset_from_nsr()
    
    return session
```
### Sitzungslebenszyklus: Aktive Phase

**Zustandsübergänge:**

```
NEW (outbound only)
  ↓
  NS sent
  ↓
PENDING_REPLY (outbound only)
  ↓
  NSR received
  ↓
ESTABLISHED
  ↓
  ES messages exchanged
  ↓
ESTABLISHED (ongoing)
  ↓
  (optional) RATCHETING
  ↓
ESTABLISHED
```
**Aktive Sitzungsaufrechterhaltung:**

```python
def maintain_active_session(session):
    # Update last activity time
    session.last_activity = now()
    
    # Check for ratchet needed
    if session.outbound_tagset.needs_ratchet():
        initiate_ratchet(session)
    
    # Check for incoming ratchet
    if received_nextkey_block():
        process_ratchet(session)
    
    # Trim old tags from inbound tagset
    session.inbound_tagset.expire_old_tags()
    
    # Check session health
    if session.idle_time() > SESSION_TIMEOUT:
        mark_session_idle(session)
```
### Sitzungslebenszyklus: Ablaufphase

**Sitzungs-Timeout-Werte:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Session Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Sender Timeout</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Receiver Timeout</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR tagset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">N/A</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Short-lived</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ES tagset 0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Initial</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ES tagset 1+</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Ratcheted</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Old tagset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">N/A</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">After ratchet</td>
    </tr>
  </tbody>
</table>
**Ablauflogik:**

```python
def check_session_expiration():
    for session in active_sessions:
        # Outbound session expiration (sender)
        if session.is_outbound():
            if session.idle_time() > 8 * 60:  # 8 minutes
                expire_outbound_session(session)
        
        # Inbound session expiration (receiver)
        else:
            if session.idle_time() > 10 * 60:  # 10 minutes
                expire_inbound_session(session)
    
    # Old tagsets (after ratchet)
    for tagset in old_tagsets:
        if tagset.age() > 3 * 60:  # 3 minutes
            delete_tagset(tagset)
```
**Kritische Regel**: Ausgehende Sitzungen MÜSSEN vor eingehenden Sitzungen ablaufen, um eine Desynchronisierung zu verhindern.

**Geordnete Beendigung:**

```python
def terminate_session(session, reason=0):
    # Send Termination block (if implemented)
    send_termination_block(session, reason)
    
    # Mark session for deletion
    session.state = SessionState.TERMINATED
    
    # Keep session briefly for final messages
    schedule_deletion(session, delay=30)  # 30 seconds
    
    # Notify paired session
    if session.paired_session:
        session.paired_session.mark_remote_terminated()
```
### Mehrere NS-Nachrichten

**Szenario**: Alices NS-Nachricht oder die NSR-Antwort geht verloren.

**Alices Verhalten:**

```python
class OutboundSession:
    def __init__(self):
        self.ns_messages_sent = []
        self.ns_timer = None
        self.max_ns_attempts = 5
    
    def send_ns_message(self, payload):
        # Generate new ephemeral key for each NS
        ephemeral_key = generate_elg2_keypair()
        
        ns_message = build_ns_message(
            ephemeral_key=ephemeral_key,
            static_key=self.static_key,
            payload=payload
        )
        
        # Store state for this NS
        ns_state = {
            'ephemeral_key': ephemeral_key,
            'chainkey': compute_chainkey(ns_message),
            'hash': compute_hash(ns_message),
            'tagset': derive_nsr_tagset(ns_message),
            'sent_time': now()
        }
        self.ns_messages_sent.append(ns_state)
        
        # Send message
        send_message(ns_message)
        
        # Set timer for retry
        if not self.ns_timer:
            self.ns_timer = set_timer(1.0, self.on_ns_timeout)
    
    def on_ns_timeout(self):
        if len(self.ns_messages_sent) >= self.max_ns_attempts:
            # Give up
            fail_session("No NSR received after {self.max_ns_attempts} attempts")
            return
        
        # Retry with new NS message
        send_ns_message(self.payload)
    
    def on_nsr_received(self, nsr_message):
        # Cancel timer
        cancel_timer(self.ns_timer)
        
        # Find which NS this NSR responds to
        tag = nsr_message.tag
        for ns_state in self.ns_messages_sent:
            if tag in ns_state['tagset']:
                # This NSR corresponds to this NS
                self.active_ns_state = ns_state
                break
        
        # Process NSR and complete handshake
        complete_handshake(nsr_message, self.active_ns_state)
        
        # Discard other NS states
        self.ns_messages_sent = []
```
**Wichtige Eigenschaften:**

1. **Eindeutige ephemere Schlüssel**: Jede NS verwendet einen anderen ephemeren Schlüssel
2. **Unabhängige Handshakes**: Jede NS erzeugt einen separaten Handshake-Zustand
3. **NSR-Korrelation**: Das NSR-Tag identifiziert, auf welche NS es antwortet
4. **Zustandsbereinigung**: Nicht verwendete NS-Zustände werden nach erfolgreicher NSR verworfen

**Angriffsprävention:**

Um Ressourcenerschöpfung zu verhindern:

```python
# Limit NS sending rate
max_ns_rate = 5 per 10 seconds per destination

# Limit total NS attempts
max_ns_attempts = 5

# Limit total pending NS states
max_pending_ns = 10 per context
```
### Mehrere NSR-Nachrichten

**Szenario**: Bob sendet mehrere NSRs (engl. Akronym; hier: einzelne Antwortnachrichten; z. B. auf mehrere Nachrichten aufgeteilte Antwortdaten).

**Bobs Verhalten:**

```python
class InboundSession:
    def send_nsr_replies(self, payload_chunks):
        # One NS received, multiple NSRs to send
        for chunk in payload_chunks:
            # Generate new ephemeral key for each NSR
            ephemeral_key = generate_elg2_keypair()
            
            # Get next tag from NSR tagset
            tag = self.nsr_tagset.get_next_tag()
            
            nsr_message = build_nsr_message(
                tag=tag,
                ephemeral_key=ephemeral_key,
                payload=chunk
            )
            
            send_message(nsr_message)
        
        # Wait for ES message from Alice
        self.state = SessionState.AWAITING_ES
```
**Alices Verhalten:**

```python
class OutboundSession:
    def on_nsr_received(self, nsr_message):
        if self.state == SessionState.PENDING_REPLY:
            # First NSR received
            complete_handshake(nsr_message)
            self.state = SessionState.ESTABLISHED
            
            # Create ES sessions
            self.es_outbound_tagset = derive_es_outbound_tagset()
            self.es_inbound_tagset = derive_es_inbound_tagset()
            
            # Send ES message (ACK)
            send_es_message(empty_payload)
        
        elif self.state == SessionState.ESTABLISHED:
            # Additional NSR received
            # Decrypt and process payload
            payload = decrypt_nsr_payload(nsr_message)
            process_payload(payload)
            
            # These NSRs are from other NS attempts, ignore handshake
```
**Bobs Aufräumarbeiten:**

```python
class InboundSession:
    def on_es_received(self, es_message):
        # First ES received from Alice
        # This confirms which NSR Alice used
        
        # Clean up other handshake states
        for other_ns_state in self.pending_ns_states:
            if other_ns_state != self.active_ns_state:
                delete_ns_state(other_ns_state)
        
        # Delete unused NSR tagsets
        for tagset in self.nsr_tagsets:
            if tagset != self.active_nsr_tagset:
                delete_tagset(tagset)
        
        self.state = SessionState.ESTABLISHED
```
**Wichtige Eigenschaften:**

1. **Mehrere NSRs erlaubt**: Bob kann pro NS mehrere NSRs senden
2. **Verschiedene ephemere Schlüssel**: Jede NSR sollte einen eindeutigen ephemeren Schlüssel verwenden
3. **Gleiches NSR-Tagset**: Alle NSRs für einen NS verwenden dasselbe Tagset
4. **Erstes ES gewinnt**: Alices erstes ES entscheidet, welche NSR erfolgreich war
5. **Aufräumen nach ES**: Bob verwirft ungenutzte Zustände nach Erhalt des ES

### Zustandsautomat der Sitzung

**Vollständiges Zustandsdiagramm:**

```
                    Outbound Session                    Inbound Session

                         NEW
                          |
                     send NS
                          |
                   PENDING_REPLY -------------------- receive NS ---> ESTABLISHED
                          |                                                |
                   receive NSR                                        send NSR
                          |                                                |
                    ESTABLISHED <---------- receive ES ------------- AWAITING_ES
                          |                     |                          |
                    ┌─────┴─────┐               |                    receive ES
                    |           |               |                          |
              send ES      receive ES           |                    ESTABLISHED
                    |           |               |                          |
                    └─────┬─────┘               |                ┌─────────┴─────────┐
                          |                     |                |                   |
                          |                     |          send ES              receive ES
                          |                     |                |                   |
                          |                     |                └─────────┬─────────┘
                          |                     |                          |
                          └─────────────────────┴──────────────────────────┘
                                              ACTIVE
                                                |
                                         idle timeout
                                                |
                                             EXPIRED
```
**Statusbeschreibungen:**

- **NEW**: Ausgehende Sitzung erstellt, bisher noch kein NS gesendet
- **PENDING_REPLY**: NS gesendet, wartet auf NSR
- **AWAITING_ES**: NSR gesendet, wartet auf das erste ES von Alice
- **ESTABLISHED**: Handshake abgeschlossen, kann ES senden/empfangen
- **ACTIVE**: Aktiver Austausch von ES-Nachrichten
- **RATCHETING**: DH ratchet (Diffie-Hellman-Ratchet, kryptografischer Fortschaltmechanismus) läuft (Teilmenge von ACTIVE)
- **EXPIRED**: Sitzung abgelaufen, zur Löschung ausstehend
- **TERMINATED**: Sitzung explizit beendet

---

## Nutzlastformat

Der Nutzlastabschnitt aller ECIES-Nachrichten (NS, NSR, ES) verwendet ein blockbasiertes Format, ähnlich wie NTCP2.

### Blockstruktur

**Allgemeines Format:**

```
+----+----+----+----+----+----+----+----+
|blk |  size   |       data             |
+----+----+----+                        +
|                                       |
~               ...                     ~
|                                       |
+----+----+----+----+----+----+----+----+
|blk |  size   |       data             |
+----+----+----+                        +
|                                       |
~               ...                     ~
|                                       |
+----+----+----+----+----+----+----+----+
```
**Felder:**

- `blk`: 1 Byte - Nummer des Blocktyps
- `size`: 2 Bytes - Big-Endian-Größe des Datenfelds (0-65516)
- `data`: Variable Länge - blockspezifische Daten

**Einschränkungen:**

- Maximale ChaChaPoly-Frame-Größe: 65535 Bytes
- Poly1305-MAC: 16 Bytes
- Maximale Gesamtblockgröße: 65519 Bytes (65535 - 16)
- Maximaler Einzelblock: 65519 Bytes (einschließlich 3-Byte-Header)
- Maximale Nutzdaten eines Einzelblocks: 65516 Bytes

### Blocktypen

**Definierte Blocktypen:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DateTime</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">7 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Required in NS</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1-3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Future use</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Termination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">9+ bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unimplemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Session termination</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Options</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">21+ bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unimplemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Session options</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">MessageNumbers</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">5 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unimplemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">PN value</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NextKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">3 or 35 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DH ratchet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ACK</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">4+ bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Message acknowledgment</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">9</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ACK Request</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">3 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Request ACK</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Future use</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Garlic Clove</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Variable</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Application data</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12-223</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Future use</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">224-253</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Variable</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Testing features</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">254</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Padding</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Variable</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Traffic shaping</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">255</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Future extension</td>
    </tr>
  </tbody>
</table>
**Behandlung unbekannter Blöcke:**

Implementierungen MÜSSEN Blöcke mit unbekannten Typnummern ignorieren und sie als Padding (Auffüllung) behandeln. Dies gewährleistet die Vorwärtskompatibilität.

### Regeln für die Blockreihenfolge

### NS-Nachrichtenreihenfolge

**Erforderlich:** - Der DateTime-Block MUSS zuerst stehen

**Zulässig:** - Garlic Clove (Teil von garlic encryption; Typ 11) - Optionen (Typ 5) - falls implementiert - Padding (Typ 254)

**Unzulässig:** - NextKey, ACK, ACK Request, Termination, MessageNumbers

**Beispiel für eine gültige NS-Nutzlast:**

```
DateTime (0) | Garlic Clove (11) | Garlic Clove (11) | Padding (254)
```
### Reihenfolge von NSR-Nachrichten

**Erforderlich:** - Keine (Nutzlast kann leer sein)

**Zulässig:** - Garlic Clove (type 11) - Optionen (type 5) - falls implementiert - Padding (type 254)

**Verboten:** - DateTime, NextKey, ACK, ACK Request, Termination, MessageNumbers

**Beispiel für eine gültige NSR-Nutzlast:**

```
Garlic Clove (11) | Garlic Clove (11) | Padding (254)
```
oder

```
(empty - ACK only)
```
### ES-Nachrichtenreihenfolge

**Erforderlich:** - Keine (die Nutzlast kann leer sein)

**Zulässig (beliebige Reihenfolge):** - Garlic Clove (Einzelnachricht in einem Garlic-Message-Bündel; Typ 11) - NextKey (Typ 7) - ACK (Typ 8) - ACK Request (Typ 9) - Termination (Typ 4) - falls implementiert - MessageNumbers (Typ 6) - falls implementiert - Options (Typ 5) - falls implementiert - Padding (Typ 254)

**Sonderregeln:** - Termination (Abschlussblock) MUSS der letzte Block sein (außer Padding (Auffüllungsblock)) - Padding MUSS der letzte Block sein - Mehrere Garlic Cloves (Clove-Teilnachrichten) sind erlaubt - Bis zu 2 NextKey blocks (Block für nächsten Schlüssel) sind erlaubt (vorwärts und rückwärts) - Mehrere Padding blocks sind NICHT erlaubt

**Beispiele für gültige ES-Nutzdaten:**

```
Garlic Clove (11) | ACK (8) | Padding (254)
```
```
NextKey (7) | Garlic Clove (11) | Garlic Clove (11)
```
```
NextKey (7) forward | NextKey (7) reverse | Garlic Clove (11)
```
```
ACK Request (9) | Garlic Clove (11) | Termination (4) | Padding (254)
```
### Datum/Uhrzeit-Block (Typ 0)

**Zweck**: Zeitstempel zur Verhinderung von Replay-Angriffen und zur Prüfung der Uhrzeitabweichung

**Größe**: 7 Byte (3 Byte Header + 4 Byte Daten)

**Format:**

```
+----+----+----+----+----+----+----+
| 0  |    4    |     timestamp     |
+----+----+----+----+----+----+----+
```
**Felder:**

- `blk`: 0
- `size`: 4 (Big-Endian)
- `timestamp`: 4 Bytes - Unix-Zeitstempel in Sekunden (ohne Vorzeichen, Big-Endian)

**Zeitstempelformat:**

```python
timestamp = int(time.time())  # Seconds since 1970-01-01 00:00:00 UTC
# Wraps around in year 2106 (4-byte unsigned maximum)
```
**Validierungsregeln:**

```python
MAX_CLOCK_SKEW_PAST = 5 * 60      # 5 minutes
MAX_CLOCK_SKEW_FUTURE = 2 * 60    # 2 minutes

def validate_datetime(timestamp):
    now = int(time.time())
    age = now - timestamp
    
    if age < -MAX_CLOCK_SKEW_FUTURE:
        return False  # Too far in future
    
    if age > MAX_CLOCK_SKEW_PAST:
        return False  # Too old
    
    return True
```
**Schutz vor Replay-Angriffen:**

```python
class ReplayFilter:
    def __init__(self, duration=5*60):
        self.duration = duration  # 5 minutes
        self.seen_messages = BloomFilter(size=100000, false_positive_rate=0.001)
        self.cleanup_timer = RepeatTimer(60, self.cleanup)
    
    def check_replay(self, ephemeral_key, timestamp):
        # Check timestamp validity
        if not validate_datetime(timestamp):
            return False
        
        # Check if ephemeral key seen recently
        if ephemeral_key in self.seen_messages:
            return False  # Replay attack
        
        # Add to seen messages
        self.seen_messages.add(ephemeral_key)
        return True
    
    def cleanup(self):
        # Expire old entries (Bloom filter automatically ages out)
        pass
```
**Implementierungshinweise:**

1. **NS-Nachrichten**: DateTime MUSS der erste Block sein
2. **NSR/ES-Nachrichten**: DateTime ist typischerweise nicht enthalten
3. **Replay-Fenster**: 5 Minuten sind das empfohlene Minimum
4. **Bloom-Filter**: Empfohlen für effiziente Replay-Erkennung
5. **Uhrabweichung**: 5 Minuten in der Vergangenheit, 2 Minuten in der Zukunft erlauben

### Garlic Clove Block (Datenblock einer Clove bei garlic encryption) (Typ 11)

**Zweck**: Kapselt I2NP-Nachrichten zur Zustellung ein

**Format:**

```
+----+----+----+----+----+----+----+----+
| 11 |  size   |                        |
+----+----+----+                        +
|      Delivery Instructions            |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|type|  Message_ID       | Expiration  |
+----+----+----+----+----+----+----+----+
     |      I2NP Message body           |
+----+                                  +
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
```
**Felder:**

- `blk`: 11
- `size`: Gesamtgröße der clove (Teilkomponente einer Garlic-Nachricht) (variabel)
- `Delivery Instructions`: Wie in der I2NP-Spezifikation angegeben
- `type`: I2NP-Nachrichtentyp (1 Byte)
- `Message_ID`: I2NP-Nachrichten-ID (4 Byte)
- `Expiration`: Unix-Zeitstempel in Sekunden (4 Byte)
- `I2NP Message body`: Nachrichtendaten variabler Länge

**Formate der Zustellhinweise:**

**Lokale Zustellung** (1 Byte):

```
+----+
|0x00|
+----+
```
**Zustellung an die Zieladresse** (33 Bytes):

```
+----+----+----+----+----+----+----+----+
|0x01|                                  |
+----+        Destination Hash         +
|              32 bytes                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
**Router-Zustellung** (33 Bytes):

```
+----+----+----+----+----+----+----+----+
|0x02|                                  |
+----+         Router Hash              +
|              32 bytes                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
**Tunnel-Zustellung** (37 Bytes):

```
+----+----+----+----+----+----+----+----+
|0x03|         Tunnel ID                |
+----+----+----+----+----+              +
|           Router Hash                 |
+              32 bytes                 +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
**I2NP Message Header** (insgesamt 9 Bytes):

```
+----+----+----+----+----+----+----+----+
|type|      msg_id       |  expiration   |
+----+----+----+----+----+----+----+----+
     |                                   |
```
- `type`: I2NP-Nachrichtentyp (Database Store, Database Lookup, Data, etc.)
- `msg_id`: 4-Byte-Nachrichtenkennung
- `expiration`: 4-Byte-Unix-Zeitstempel (Sekunden)

**Wichtige Unterschiede gegenüber dem ElGamal-Clove-Format:**

1. **Kein Zertifikat**: Zertifikatsfeld weggelassen (in ElGamal unbenutzt)
2. **Keine Clove-ID** (Teilnachricht in I2P): Clove-ID weggelassen (war immer 0)
3. **Keine Clove-Ablaufzeit**: Verwendet stattdessen die Ablaufzeit der I2NP-Nachricht
4. **Kompakter Header**: 9-Byte-I2NP-Header im Vergleich zum größeren ElGamal-Format
5. **Jede Clove ist ein separater Block**: Keine CloveSet-Struktur

**Mehrere Cloves (Teilnachrichten innerhalb einer Garlic-Nachricht):**

```python
# Multiple Garlic Cloves in one message
payload = [
    build_datetime_block(),
    build_garlic_clove(i2np_message_1),
    build_garlic_clove(i2np_message_2),
    build_garlic_clove(i2np_message_3),
    build_padding_block()
]
```
**Gängige I2NP-Nachrichtentypen in Cloves (Teilbotschaften innerhalb von garlic encryption):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseStore</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Publishing LeaseSet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseLookup</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Requesting LeaseSet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DeliveryStatus</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ACK (legacy, avoid in ECIES)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Streaming data</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">21</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Garlic</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Nested garlic messages</td>
    </tr>
  </tbody>
</table>
**Clove-Verarbeitung:**

```python
def process_garlic_clove(clove_data):
    # Parse delivery instructions
    delivery_type = clove_data[0]
    
    if delivery_type == 0x00:
        # Local delivery
        offset = 1
    elif delivery_type == 0x01:
        # Destination delivery
        dest_hash = clove_data[1:33]
        offset = 33
    elif delivery_type == 0x02:
        # Router delivery
        router_hash = clove_data[1:33]
        offset = 33
    elif delivery_type == 0x03:
        # Tunnel delivery
        tunnel_id = struct.unpack('>I', clove_data[1:5])[0]
        router_hash = clove_data[5:37]
        offset = 37
    
    # Parse I2NP header
    i2np_type = clove_data[offset]
    msg_id = struct.unpack('>I', clove_data[offset+1:offset+5])[0]
    expiration = struct.unpack('>I', clove_data[offset+5:offset+9])[0]
    
    # Extract I2NP body
    i2np_body = clove_data[offset+9:]
    
    # Process message
    process_i2np_message(i2np_type, msg_id, expiration, i2np_body)
```
### NextKey-Block (Typ 7)

**Zweck**: Schlüsselaustausch mittels DH ratchet (DH-Ratschenmechanismus)

**Format (Schlüssel vorhanden - 38 Bytes):**

```
+----+----+----+----+----+----+----+----+
| 7  |   35    |flag|  key ID |         |
+----+----+----+----+----+----+         +
|                                       |
+     Next DH Ratchet Public Key        +
|              32 bytes                 |
+                                       +
|                                       |
+                             +----+----+
|                             |
+----+----+----+----+----+----+
```
**Format (nur Schlüssel-ID - 6 Bytes):**

```
+----+----+----+----+----+----+
| 7  |    3    |flag|  key ID |
+----+----+----+----+----+----+
```
**Felder:**

- `blk`: 7
- `size`: 3 (nur ID) oder 35 (mit Schlüssel)
- `flag`: 1 Byte - Flag-Bits
- `key ID`: 2 Byte - Big-Endian-Schlüsselkennung (0-32767)
- `Public Key`: 32 Byte - öffentlicher X25519-Schlüssel (Little-Endian), falls Flag-Bit 0 = 1

**Flag-Bits:**

```
Bit 7 6 5 4 3 2 1 0
    | | | | | | | |
    | | | | | | | +-- Bit 0: Key present (1) or ID only (0)
    | | | | | | +---- Bit 1: Reverse key (1) or forward key (0)
    | | | | | +------ Bit 2: Request reverse key (1) or no request (0)
    | | | | |
    +-+-+-+-+-------- Bits 3-7: Reserved (set to 0)
```
**Beispiel-Flags:**

```python
# Forward key present
flags = 0x01  # Binary: 00000001

# Reverse key present
flags = 0x03  # Binary: 00000011

# Forward key ID only (ACK)
flags = 0x00  # Binary: 00000000

# Reverse key ID only (ACK)
flags = 0x02  # Binary: 00000010

# Forward key ID with reverse request
flags = 0x04  # Binary: 00000100
```
**Schlüssel-ID-Regeln:**

- IDs sind fortlaufend: 0, 1, 2, ..., 32767
- Die ID wird nur erhöht, wenn ein neuer Schlüssel generiert wird
- Dieselbe ID wird für mehrere Nachrichten verwendet, bis zum nächsten Ratchet (Kryptographie-Ratchet-Mechanismus)
- Die maximale ID ist 32767 (danach muss eine neue Sitzung gestartet werden)

**Anwendungsbeispiele:**

```python
# Initiating ratchet (sender generates new key)
nextkey = NextKeyBlock(
    flags=0x01,           # Key present, forward
    key_id=0,
    public_key=sender_new_pk
)

# Replying to ratchet (receiver generates new key)
nextkey = NextKeyBlock(
    flags=0x03,           # Key present, reverse
    key_id=0,
    public_key=receiver_new_pk
)

# Acknowledging ratchet (no new key from sender)
nextkey = NextKeyBlock(
    flags=0x02,           # ID only, reverse
    key_id=0
)

# Requesting reverse ratchet
nextkey = NextKeyBlock(
    flags=0x04,           # Request reverse, forward ID
    key_id=1
)
```
**Verarbeitungslogik:**

```python
def process_nextkey_block(block):
    flags = block.flags
    key_id = block.key_id
    
    key_present = (flags & 0x01) != 0
    is_reverse = (flags & 0x02) != 0
    request_reverse = (flags & 0x04) != 0
    
    if key_present:
        public_key = block.public_key
        
        if is_reverse:
            # Reverse key received
            perform_dh_ratchet(receiver_key=public_key, key_id=key_id)
            # Sender should ACK with own key ID
        else:
            # Forward key received
            perform_dh_ratchet(sender_key=public_key, key_id=key_id)
            # Receiver should reply with reverse key
            send_reverse_key(generate_new_key())
    
    else:
        # Key ID only (ACK)
        if is_reverse:
            # Reverse key ACK
            confirm_reverse_ratchet(key_id)
        else:
            # Forward key ACK
            confirm_forward_ratchet(key_id)
    
    if request_reverse:
        # Sender requests receiver to generate new key
        send_reverse_key(generate_new_key())
```
**Mehrere NextKey-Blöcke:**

Eine einzelne ES-Nachricht kann bis zu 2 NextKey-Blöcke enthalten, wenn beide Richtungen gleichzeitig ratcheting (Schlüsselfortschaltung) durchführen:

```python
# Both directions ratcheting
payload = [
    NextKeyBlock(flags=0x01, key_id=2, public_key=forward_key),  # Forward
    NextKeyBlock(flags=0x03, key_id=1, public_key=reverse_key),  # Reverse
    build_garlic_clove(data)
]
```
### ACK-Block (Typ 8)

**Zweck**: Empfangene Nachrichten In-Band bestätigen

**Format (Einzelnes ACK - 7 Byte):**

```
+----+----+----+----+----+----+----+
| 8  |    4    |tagsetid |   N     |
+----+----+----+----+----+----+----+
```
**Format (Mehrere ACKs):**

```
+----+----+----+----+----+----+----+----+
| 8  |  size   |tagsetid |   N     |    |
+----+----+----+----+----+----+----+    +
|            more ACKs                  |
~               ...                     ~
|                                       |
+----+----+----+----+----+----+----+----+
```
**Felder:**

- `blk`: 8
- `size`: 4 * Anzahl der ACKs (Bestätigungen) (mindestens 4)
- Für jedes ACK:
  - `tagsetid`: 2 Bytes - Big-Endian-Tag-Set-ID (0-65535)
  - `N`: 2 Bytes - Big-Endian-Nachrichtennummer (0-65535)

**Bestimmung der Tag-Set-ID:**

```python
# Tag set 0 (initial, after NSR)
tagset_id = 0

# After first ratchet (tag set 1)
# Both Alice and Bob sent key ID 0
tagset_id = 1 + 0 + 0 = 1

# After second ratchet (tag set 2)
# Alice sent key ID 1, Bob still using key ID 0
tagset_id = 1 + 1 + 0 = 2

# After third ratchet (tag set 3)
# Alice still using key ID 1, Bob sent key ID 1
tagset_id = 1 + 1 + 1 = 3
```
**Beispiel für ein einzelnes ACK:**

```python
# ACK message from tag set 5, message number 127
ack_block = ACKBlock(
    tagset_id=5,
    message_number=127
)

# Wire format (7 bytes):
# 08 00 04 00 05 00 7F
# |  |  |  |  |  |  |
# |  |  |  |  |  |  +-- N (127)
# |  |  |  |  +--------- N high byte
# |  |  |  +------------ tagset_id (5)
# |  |  +--------------- tagset_id high byte
# |  +------------------ size (4)
# +--------------------- type (8)
```
**Beispiel mit mehreren ACKs (Bestätigungen):**

```python
# ACK three messages
ack_block = ACKBlock([
    (tagset_id=3, N=42),
    (tagset_id=3, N=43),
    (tagset_id=4, N=0)
])

# Wire format (15 bytes):
# 08 00 0C 00 03 00 2A 00 03 00 2B 00 04 00 00
#                (ts=3, N=42) (ts=3, N=43) (ts=4, N=0)
```
**Verarbeitung:**

```python
def process_ack_block(block):
    num_acks = block.size // 4
    
    for i in range(num_acks):
        offset = i * 4
        tagset_id = struct.unpack('>H', block.data[offset:offset+2])[0]
        message_num = struct.unpack('>H', block.data[offset+2:offset+4])[0]
        
        # Mark message as acknowledged
        mark_acked(tagset_id, message_num)
        
        # May trigger retransmission timeout cancellation
        cancel_retransmit_timer(tagset_id, message_num)
```
**Wann ACKs zu senden sind:**

1. **Explizite ACK-Anforderung**: Immer auf den ACK-Anforderungsblock antworten
2. **LeaseSet-Zustellung**: Wenn der Absender ein LeaseSet in die Nachricht einfügt
3. **Sitzungsaufbau**: Darf NS/NSR bestätigen (obwohl das Protokoll eine implizite Bestätigung über ES bevorzugt)
4. **Ratchet-Bestätigung**: Darf den Empfang von NextKey bestätigen
5. **Anwendungsschicht**: Wie vom Protokoll der höheren Schicht gefordert (z. B. Streaming)

**ACK-Timing:**

```python
class ACKManager:
    def __init__(self):
        self.pending_acks = []
        self.ack_timer = None
    
    def request_ack(self, tagset_id, message_num):
        self.pending_acks.append((tagset_id, message_num))
        
        if not self.ack_timer:
            # Delay ACK briefly to allow higher layer to respond
            self.ack_timer = set_timer(0.1, self.send_acks)  # 100ms
    
    def send_acks(self):
        if self.pending_acks and not has_outbound_data():
            # No higher layer data, send explicit ACK
            send_es_message(build_ack_block(self.pending_acks))
        
        # Otherwise, ACK will piggyback on next ES message
        self.pending_acks = []
        self.ack_timer = None
```
### ACK-Anforderungsblock (Typ 9)

**Zweck**: Anfordern einer In-Band-Bestätigung der aktuellen Nachricht

**Format:**

```
+----+----+----+----+
| 9  |    1    |flg |
+----+----+----+----+
```
**Felder:**

- `blk`: 9
- `size`: 1
- `flg`: 1 Byte - Flags (alle Bits derzeit unbenutzt, auf 0 gesetzt)

**Verwendung:**

```python
# Request ACK for this message
payload = [
    build_ack_request_block(),
    build_garlic_clove(important_data)
]
```
**Antwort des Empfängers:**

Wenn eine ACK-Anforderung empfangen wird:

1. **Mit Sofortdaten**: ACK-Block in die Sofortantwort aufnehmen
2. **Ohne Sofortdaten**: Timer starten (z. B. 100 ms) und leeres ES mit ACK senden, wenn der Timer abläuft
3. **Tagset-ID**: Aktuelle eingehende Tagset-ID verwenden
4. **Nachrichtennummer**: Nachrichtennummer verwenden, die dem empfangenen Sitzungs-Tag zugeordnet ist

**Verarbeitung:**

```python
def process_ack_request(message):
    # Extract message identification
    tagset_id = message.tagset_id
    message_num = message.message_num
    
    # Schedule ACK
    schedule_ack(tagset_id, message_num)
    
    # If no data to send immediately, start timer
    if not has_pending_data():
        set_timer(0.1, lambda: send_ack_only(tagset_id, message_num))
```
**Wann die ACK-Anforderung verwendet werden sollte:**

1. **Kritische Nachrichten**: Nachrichten, die bestätigt werden müssen
2. **LeaseSet-Zustellung**: Beim Bündeln eines LeaseSet
3. **Session Ratchet** (Schlüsselkettensystem für Sitzungen): Nach dem Senden des NextKey block (Block mit dem nächsten Schlüssel)
4. **Ende der Übertragung**: Wenn der Sender keine weiteren Daten zu senden hat, aber eine Bestätigung wünscht

**Wann NICHT verwenden:**

1. **Streaming-Protokoll**: Die Streaming-Schicht verarbeitet ACKs (Bestätigungen)
2. **Häufige Nachrichten**: Vermeiden Sie eine ACK-Anforderung bei jeder Nachricht (Overhead)
3. **Unwichtige Datagramme**: Raw datagrams (rohe Datagramme) benötigen normalerweise keine ACKs

### Terminierungsblock (Typ 4)

**Status**: NICHT IMPLEMENTIERT

**Zweck**: Sitzung geordnet beenden

**Format:**

```
+----+----+----+----+----+----+----+----+
| 4  |  size   | rsn|     addl data     |
+----+----+----+----+                   +
~               ...                     ~
+----+----+----+----+----+----+----+----+
```
**Felder:**

- `blk`: 4
- `size`: 1 oder mehr Bytes
- `rsn`: 1 Byte - Grundcode
- `addl data`: Optionale zusätzliche Daten (Format hängt vom Grund ab)

**Ursachen-Codes:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Meaning</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Additional Data</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Normal close / unspecified</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">None</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Termination received</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">None</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Idle timeout</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">None (implementation-specific)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Resource exhaustion</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">None (implementation-specific)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4+</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implementation-specific</td>
    </tr>
  </tbody>
</table>
**Verwendung (sobald implementiert):**

```python
# Normal session close
termination = TerminationBlock(
    reason=0,
    additional_data=b''
)

# Session termination due to received termination
termination = TerminationBlock(
    reason=1,
    additional_data=b''
)
```
**Regeln:**

- MUSS der letzte Block sein (mit Ausnahme von Padding)
- Padding MUSS auf Termination folgen, falls vorhanden
- In NS- oder NSR-Nachrichten nicht erlaubt
- Nur in ES-Nachrichten erlaubt

### Optionsblock (Typ 5)

**Status**: NICHT IMPLEMENTIERT

**Zweck**: Aushandeln von Sitzungsparametern

**Format:**

```
+----+----+----+----+----+----+----+----+
| 5  |  size   |ver |flg |STL |STimeout |
+----+----+----+----+----+----+----+----+
|  SOTW   |  RITW   |tmin|tmax|rmin|rmax|
+----+----+----+----+----+----+----+----+
|  tdmy   |  rdmy   |  tdelay |  rdelay |
+----+----+----+----+----+----+----+----+
|              more_options             |
~               ...                     ~
|                                       |
+----+----+----+----+----+----+----+----+
```
**Felder:**

- `blk`: 5
- `size`: 21 oder mehr Bytes
- `ver`: 1 Byte - Protokollversion (muss 0 sein)
- `flg`: 1 Byte - Flags (derzeit sind alle Bits ungenutzt)
- `STL`: 1 Byte - Länge des Session-Tags (muss 8 sein)
- `STimeout`: 2 Bytes - Leerlauf-Timeout der Session in Sekunden (Big-Endian)
- `SOTW`: 2 Bytes - Sender Outbound Tag Window (Fenster für ausgehende Tags des Senders, Big-Endian)
- `RITW`: 2 Bytes - Receiver Inbound Tag Window (Fenster für eingehende Tags des Empfängers, Big-Endian)
- `tmin`, `tmax`, `rmin`, `rmax`: je 1 Byte - Padding-Parameter (4.4-Festkomma)
- `tdmy`: 2 Bytes - Maximaler Füllverkehr, zu dessen Sendung man bereit ist (Bytes/s, Big-Endian)
- `rdmy`: 2 Bytes - Angeforderter Füllverkehr (Bytes/s, Big-Endian)
- `tdelay`: 2 Bytes - Maximale intra-Nachrichten-Verzögerung, die man einzufügen bereit ist (Millisekunden, Big-Endian)
- `rdelay`: 2 Bytes - Angeforderte intra-Nachrichten-Verzögerung (Millisekunden, Big-Endian)
- `more_options`: Variabel - zukünftige Erweiterungen

**Padding-Parameter (4.4-Festkomma):**

```python
def encode_padding_ratio(ratio):
    """
    Encode padding ratio as 4.4 fixed-point
    
    ratio: 0.0 to 15.9375
    returns: 0x00 to 0xFF
    """
    return int(ratio * 16)

def decode_padding_ratio(encoded):
    """
    Decode 4.4 fixed-point to ratio
    
    encoded: 0x00 to 0xFF
    returns: 0.0 to 15.9375
    """
    return encoded / 16.0

# Examples:
# 0x00 = 0.0 (no padding)
# 0x01 = 0.0625 (6.25% padding)
# 0x10 = 1.0 (100% padding - double traffic)
# 0x80 = 8.0 (800% padding - 9x traffic)
# 0xFF = 15.9375 (1593.75% padding)
```
**Tag Window Negotiation (Aushandlung des Tag-Fensters):**

```python
# SOTW: Sender's recommendation for receiver's inbound window
# RITW: Sender's declaration of own inbound window

# Receiver calculates actual inbound window:
inbound_window = calculate_window(
    sender_suggestion=SOTW,
    own_constraints=MAX_INBOUND_TAGS,
    own_resources=available_memory()
)

# Sender uses:
# - RITW to know how far ahead receiver will accept
# - Own SOTW to hint optimal window size
```
**Standardwerte (wenn Optionen nicht ausgehandelt wurden):**

```python
DEFAULT_OPTIONS = {
    'version': 0,
    'session_tag_length': 8,
    'session_timeout': 600,  # 10 minutes
    'sender_outbound_tag_window': 160,
    'receiver_inbound_tag_window': 160,
    'tmin': 0x00,  # No minimum padding
    'tmax': 0x10,  # Up to 100% padding
    'rmin': 0x00,  # No minimum requested
    'rmax': 0x10,  # Up to 100% requested
    'tdmy': 0,     # No dummy traffic
    'rdmy': 0,     # No dummy traffic requested
    'tdelay': 0,   # No delay
    'rdelay': 0    # No delay requested
}
```
### MessageNumbers-Block (Typ 6)

**Status**: NICHT IMPLEMENTIERT

**Zweck**: Gibt die letzte im vorherigen Tag-Satz gesendete Nachricht an (ermöglicht Lückenerkennung)

**Format:**

```
+----+----+----+----+----+
| 6  |    2    |  PN    |
+----+----+----+----+----+
```
**Felder:**

- `blk`: 6
- `size`: 2
- `PN`: 2 Bytes - Letzte Nachrichtennummer des vorherigen Tag-Sets (Big-Endian, 0-65535)

**PN (Previous Number, vorherige Nummer) Definition:**

PN ist der Index des letzten Tags, der im vorherigen Satz von Tags gesendet wurde.

**Verwendung (sobald implementiert):**

```python
# After ratcheting to new tag set
# Old tag set: sent messages 0-4095
# New tag set: sending first message

payload = [
    MessageNumbersBlock(PN=4095),
    build_garlic_clove(data)
]
```
**Vorteile für Empfänger:**

```python
def process_message_numbers(pn_value):
    # Receiver can now:
    
    # 1. Determine if any messages were skipped
    highest_received_in_old_tagset = 4090
    if pn_value > highest_received_in_old_tagset:
        missing_count = pn_value - highest_received_in_old_tagset
        # 5 messages were never received
    
    # 2. Delete tags higher than PN from old tagset
    for tag_index in range(pn_value + 1, MAX_TAG_INDEX):
        delete_tag(old_tagset, tag_index)
    
    # 3. Expire tags ≤ PN after grace period (e.g., 2 minutes)
    schedule_deletion(old_tagset, delay=120)
```
**Regeln:**

- DARF NICHT in tag set (Satz von Tags) 0 gesendet werden (kein vorheriges tag set)
- Wird nur in ES messages (ES-Nachrichten) gesendet
- Wird nur in der ersten Nachricht(en) eines neuen tag set gesendet
- PN value (PN-Wert) ist aus Sicht des Senders (letztes Tag, das der Sender gesendet hat)

**Beziehung zu Signal:**

Im Signal Double Ratchet (Double‑Ratchet‑Algorithmus von Signal) steht PN im Nachrichtenheader. In ECIES (Elliptic Curve Integrated Encryption Scheme, integriertes Verschlüsselungsverfahren auf elliptischen Kurven) befindet es sich in den verschlüsselten Nutzdaten und ist optional.

### Padding-Block (Typ 254)

**Zweck**: Widerstandsfähigkeit gegen Verkehrsanalyse und Verschleierung der Nachrichtengröße

**Format:**

```
+----+----+----+----+----+----+----+----+
|254 |  size   |      padding           |
+----+----+----+                        +
|                                       |
~               ...                     ~
|                                       |
+----+----+----+----+----+----+----+----+
```
**Felder:**

- `blk`: 254
- `size`: 0-65516 Bytes (big-endian, höchstwertiges Byte zuerst)
- `padding`: Zufällige oder aus Nullen bestehende Daten

**Regeln:**

- MUSS der letzte Block in der Nachricht sein
- Mehrere Padding-Blöcke (Auffüllung) sind NICHT erlaubt
- Darf eine Länge von Null haben (nur 3-Byte-Header)
- Padding-Daten dürfen Nullen oder zufällige Bytes sein

**Standard-Padding:**

```python
DEFAULT_PADDING_MIN = 0
DEFAULT_PADDING_MAX = 15

def generate_default_padding():
    size = random.randint(DEFAULT_PADDING_MIN, DEFAULT_PADDING_MAX)
    data = random.bytes(size)  # or zeros
    return PaddingBlock(size, data)
```
**Strategien zur Erschwerung der Verkehrsanalyse:**

**Strategie 1: Zufällige Größe (Standard)**

```python
# Add 0-15 bytes random padding to each message
padding_size = random.randint(0, 15)
padding_block = PaddingBlock(padding_size, random.bytes(padding_size))
```
**Strategie 2: Auf ein Vielfaches runden**

```python
# Round total message size to next multiple of 64
target_size = ((message_size + 63) // 64) * 64
padding_size = target_size - message_size - 3  # -3 for block header
padding_block = PaddingBlock(padding_size, random.bytes(padding_size))
```
**Strategie 3: Feste Nachrichtengrößen**

```python
# Always send 1KB messages
TARGET_MESSAGE_SIZE = 1024
padding_size = TARGET_MESSAGE_SIZE - message_size - 3
padding_block = PaddingBlock(padding_size, random.bytes(padding_size))
```
**Strategie 4: Ausgehandeltes Padding (Options-Block)**

```python
# Calculate padding based on negotiated parameters
# tmin, tmax from Options block
min_padding = int(payload_size * tmin_ratio)
max_padding = int(payload_size * tmax_ratio)
padding_size = random.randint(min_padding, max_padding)
padding_block = PaddingBlock(padding_size, random.bytes(padding_size))
```
**Nur-Padding-Nachrichten:**

Nachrichten können vollständig aus Padding bestehen (keine Anwendungsdaten):

```python
# Dummy traffic message
payload = [
    PaddingBlock(random.randint(100, 500), random.bytes(...))
]
```
**Hinweise zur Implementierung:**

1. **All-Nullen-Padding**: Zulässig (wird von ChaCha20 verschlüsselt)
2. **Zufälliges Padding**: Bietet nach der Verschlüsselung keine zusätzliche Sicherheit, verbraucht jedoch mehr Entropie
3. **Leistung**: Die Erzeugung zufälligen Paddings kann rechenaufwendig sein; erwägen Sie die Verwendung von Nullen
4. **Speicher**: Große Padding-Blöcke verbrauchen Bandbreite; achten Sie auf die maximale Größe

---

## Implementierungsleitfaden

### Voraussetzungen

**Kryptografische Bibliotheken:**

- **X25519**: libsodium, NaCl oder Bouncy Castle
- **ChaCha20-Poly1305**: libsodium, OpenSSL 1.1.0+ oder Bouncy Castle
- **SHA-256**: OpenSSL, Bouncy Castle oder integrierte Unterstützung in der Programmiersprache
- **Elligator2**: Eingeschränkte Unterstützung durch Bibliotheken; möglicherweise ist eine eigene Implementierung erforderlich

**Implementierung von Elligator2 (Verfahren zur Tarnung elliptischer Kurvenpunkte):**

Elligator2 (ein Verfahren zur Tarnung elliptischer Kurvenpunkte) ist nicht weit verbreitet implementiert. Optionen:

1. **OBFS4**: Tors obfs4-Pluggable-Transport (austauschbares Transportprotokoll) enthält eine Elligator2-Implementierung
2. **Eigene Implementierung**: Basiert auf dem [Elligator2-Fachartikel](https://elligator.cr.yp.to/elligator-20130828.pdf)
3. **kleshni/Elligator**: Referenzimplementierung auf GitHub

**Java I2P-Hinweis:** Java I2P verwendet die Bibliothek net.i2p.crypto.eddsa mit benutzerdefinierten Elligator2-Erweiterungen (Kryptoverfahren zur Tarnung von Punkten auf elliptischen Kurven).

### Empfohlene Implementierungsreihenfolge

**Phase 1: Kernkryptografie** 1. X25519-DH-Schlüsselgenerierung und -austausch 2. ChaCha20-Poly1305-AEAD-Verschlüsselung/Entschlüsselung 3. SHA-256-Hashing und MixHash 4. HKDF-Schlüsselableitung 5. Elligator2-Kodierung/Dekodierung (anfangs können Testvektoren verwendet werden)

**Phase 2: Nachrichtenformate** 1. NS-Nachricht (ungebunden) - einfachstes Format 2. NS-Nachricht (gebunden) - fügt statischen Schlüssel hinzu 3. NSR-Nachricht 4. ES-Nachricht 5. Block-Parsing und -Generierung

**Phase 3: Sitzungsverwaltung** 1. Sitzungserstellung und -speicherung 2. Tag-Set-Verwaltung (Kennzeichen) (Sender und Empfänger) 3. Sitzungs-Tag ratchet (Ratschenmechanismus) 4. Ratchet für symmetrische Schlüssel 5. Tag-Suche und Fensterverwaltung

**Phase 4: DH Ratcheting (DH-Ratschenmechanismus)** 1. Verarbeitung des NextKey-Blocks 2. DH-Ratchet-KDF 3. Erstellung des Tag-Sets nach dem Ratchet 4. Verwaltung mehrerer Tag-Sets

**Phase 5: Protokoll-Logik** 1. NS/NSR/ES-Zustandsautomat 2. Replay-Schutz (DateTime, Bloom-Filter) 3. Wiederübertragungslogik (mehrere NS/NSR) 4. ACK-Verarbeitung

**Phase 6: Integration** 1. Verarbeitung von I2NP Garlic Clove (Teilnachricht) 2. LeaseSet-Bündelung 3. Integration des Streaming-Protokolls 4. Integration des Datagramm-Protokolls

### Implementierung des Senders

**Lebenszyklus einer ausgehenden Sitzung:**

```python
class OutboundSession:
    def __init__(self, destination, bound=True):
        self.destination = destination
        self.bound = bound
        self.state = SessionState.NEW
        
        # Keys for NS message
        self.ephemeral_keypair = generate_elg2_keypair()
        if bound:
            self.static_key = context.static_keypair
        
        # Will be populated after NSR
        self.outbound_tagset = None
        self.outbound_keyratchet = None
        self.inbound_tagset = None
        self.inbound_keyratchet = None
        
        # Timing
        self.created_time = now()
        self.last_activity = now()
        
        # Retransmission
        self.ns_attempts = []
        self.ns_timer = None
    
    def send_initial_message(self, payload):
        """Send NS message"""
        # Build NS message
        ns_message = self.build_ns_message(payload)
        
        # Send
        send_to_network(self.destination, ns_message)
        
        # Track for retransmission
        self.ns_attempts.append({
            'message': ns_message,
            'time': now(),
            'ephemeral_key': self.ephemeral_keypair,
            'kdf_state': self.save_kdf_state()
        })
        
        # Start timer
        self.ns_timer = set_timer(1.0, self.on_ns_timeout)
        self.state = SessionState.PENDING_REPLY
    
    def build_ns_message(self, payload):
        """Construct NS message"""
        # KDF initialization
        chainKey, h = self.initialize_kdf()
        
        # Ephemeral key section
        elg2_ephemeral = ENCODE_ELG2(self.ephemeral_keypair.public_key)
        h = SHA256(h || self.destination.static_key)
        h = SHA256(h || self.ephemeral_keypair.public_key)
        
        # es DH
        es_shared = DH(self.ephemeral_keypair.private_key, 
                       self.destination.static_key)
        keydata = HKDF(chainKey, es_shared, "", 64)
        chainKey = keydata[0:31]
        k_static = keydata[32:63]
        
        # Encrypt static key section
        if self.bound:
            static_section = self.static_key.public_key
        else:
            static_section = bytes(32)
        
        static_ciphertext = ENCRYPT(k_static, 0, static_section, h)
        h = SHA256(h || static_ciphertext)
        
        # ss DH (if bound)
        if self.bound:
            ss_shared = DH(self.static_key.private_key, 
                          self.destination.static_key)
            keydata = HKDF(chainKey, ss_shared, "", 64)
            chainKey = keydata[0:31]
            k_payload = keydata[32:63]
            nonce = 0
        else:
            k_payload = k_static
            nonce = 1
        
        # Build payload blocks
        payload_data = self.build_ns_payload(payload)
        
        # Encrypt payload
        payload_ciphertext = ENCRYPT(k_payload, nonce, payload_data, h)
        h = SHA256(h || payload_ciphertext)
        
        # Save KDF state for NSR processing
        self.ns_chainkey = chainKey
        self.ns_hash = h
        
        # Assemble message
        return elg2_ephemeral + static_ciphertext + payload_ciphertext
    
    def build_ns_payload(self, application_data):
        """Build NS payload blocks"""
        blocks = []
        
        # DateTime block (required, first)
        blocks.append(build_datetime_block())
        
        # Garlic Clove(s) with application data
        blocks.append(build_garlic_clove(application_data))
        
        # Optionally bundle LeaseSet
        if should_send_leaseset():
            blocks.append(build_garlic_clove(build_leaseset_store()))
        
        # Padding
        blocks.append(build_padding_block(random.randint(0, 15)))
        
        return encode_blocks(blocks)
    
    def on_nsr_received(self, nsr_message):
        """Process NSR and establish ES session"""
        # Cancel retransmission timer
        cancel_timer(self.ns_timer)
        
        # Parse NSR
        tag = nsr_message[0:8]
        elg2_bob_ephemeral = nsr_message[8:40]
        key_section_mac = nsr_message[40:56]
        payload_ciphertext = nsr_message[56:]
        
        # Find corresponding NS attempt
        ns_state = self.find_ns_by_tag(tag)
        if not ns_state:
            raise ValueError("NSR tag doesn't match any NS")
        
        # Restore KDF state
        chainKey = ns_state['chainkey']
        h = ns_state['hash']
        
        # Decode Bob's ephemeral key
        bob_ephemeral = DECODE_ELG2(elg2_bob_ephemeral)
        
        # Mix tag and Bob's ephemeral into hash
        h = SHA256(h || tag)
        h = SHA256(h || bob_ephemeral)
        
        # ee DH
        ee_shared = DH(self.ephemeral_keypair.private_key, bob_ephemeral)
        keydata = HKDF(chainKey, ee_shared, "", 32)
        chainKey = keydata[0:31]
        
        # se DH
        se_shared = DH(self.static_key.private_key, bob_ephemeral)
        keydata = HKDF(chainKey, se_shared, "", 64)
        chainKey = keydata[0:31]
        k_key_section = keydata[32:63]
        
        # Verify key section MAC
        try:
            DECRYPT(k_key_section, 0, key_section_mac, h)
        except AuthenticationError:
            raise ValueError("NSR key section MAC verification failed")
        
        h = SHA256(h || key_section_mac)
        
        # Split for bidirectional ES
        keydata = HKDF(chainKey, ZEROLEN, "", 64)
        k_ab = keydata[0:31]  # Alice → Bob
        k_ba = keydata[32:63]  # Bob → Alice
        
        # Initialize ES tagsets
        self.outbound_tagset = DH_INITIALIZE(chainKey, k_ab)
        self.inbound_tagset = DH_INITIALIZE(chainKey, k_ba)
        
        # Decrypt NSR payload
        k_nsr = HKDF(k_ba, ZEROLEN, "AttachPayloadKDF", 32)
        try:
            payload = DECRYPT(k_nsr, 0, payload_ciphertext, h)
        except AuthenticationError:
            raise ValueError("NSR payload MAC verification failed")
        
        # Process NSR payload blocks
        self.process_payload_blocks(payload)
        
        # Session established
        self.state = SessionState.ESTABLISHED
        self.last_activity = now()
        
        # Send ES message (implicit ACK)
        self.send_es_ack()
    
    def send_es_message(self, payload):
        """Send ES message"""
        if self.state != SessionState.ESTABLISHED:
            raise ValueError("Session not established")
        
        # Get next tag and key
        tag, index = self.outbound_tagset.get_next_tag()
        key = self.outbound_keyratchet.get_key(index)
        
        # Construct nonce
        nonce = construct_nonce(index)
        
        # Build payload blocks
        payload_data = self.build_es_payload(payload)
        
        # AEAD encryption
        ciphertext = ENCRYPT(key, nonce, payload_data, tag)
        
        # Assemble message
        es_message = tag + ciphertext
        
        # Send
        send_to_network(self.destination, es_message)
        
        # Update activity
        self.last_activity = now()
        
        # Check if ratchet needed
        if self.outbound_tagset.should_ratchet():
            self.initiate_ratchet()
```
### Implementierung des Empfängers

**Lebenszyklus der eingehenden Sitzung:**

```python
class InboundSession:
    def __init__(self):
        self.state = None
        self.bound = False
        self.destination = None
        
        # Keys
        self.remote_ephemeral_key = None
        self.remote_static_key = None
        self.ephemeral_keypair = None
        
        # Tagsets
        self.inbound_tagset = None
        self.outbound_tagset = None
        
        # Timing
        self.created_time = None
        self.last_activity = None
        
        # Paired session
        self.paired_outbound = None
    
    @staticmethod
    def try_decrypt_ns(message):
        """Attempt to decrypt as NS message"""
        # Parse NS structure
        elg2_ephemeral = message[0:32]
        static_ciphertext = message[32:80]  # 32 + 16
        payload_ciphertext = message[80:]
        
        # Decode ephemeral key
        try:
            alice_ephemeral = DECODE_ELG2(elg2_ephemeral)
        except:
            return None  # Not a valid Elligator2 encoding
        
        # Check replay
        if is_replay(alice_ephemeral):
            return None
        
        # KDF initialization
        chainKey, h = initialize_kdf()
        
        # Mix keys
        h = SHA256(h || context.static_keypair.public_key)
        h = SHA256(h || alice_ephemeral)
        
        # es DH
        es_shared = DH(context.static_keypair.private_key, alice_ephemeral)
        keydata = HKDF(chainKey, es_shared, "", 64)
        chainKey = keydata[0:31]
        k_static = keydata[32:63]
        
        # Decrypt static key section
        try:
            static_data = DECRYPT(k_static, 0, static_ciphertext, h)
        except AuthenticationError:
            return None  # Not a valid NS message
        
        h = SHA256(h || static_ciphertext)
        
        # Check if bound or unbound
        if static_data == bytes(32):
            # Unbound
            alice_static_key = None
            k_payload = k_static
            nonce = 1
        else:
            # Bound - perform ss DH
            alice_static_key = static_data
            ss_shared = DH(context.static_keypair.private_key, alice_static_key)
            keydata = HKDF(chainKey, ss_shared, "", 64)
            chainKey = keydata[0:31]
            k_payload = keydata[32:63]
            nonce = 0
        
        # Decrypt payload
        try:
            payload = DECRYPT(k_payload, nonce, payload_ciphertext, h)
        except AuthenticationError:
            return None
        
        h = SHA256(h || payload_ciphertext)
        
        # Create session
        session = InboundSession()
        session.state = SessionState.ESTABLISHED
        session.created_time = now()
        session.last_activity = now()
        session.remote_ephemeral_key = alice_ephemeral
        session.remote_static_key = alice_static_key
        session.bound = (alice_static_key is not None)
        session.ns_chainkey = chainKey
        session.ns_hash = h
        
        # Extract destination if bound
        if session.bound:
            session.destination = extract_destination_from_payload(payload)
        
        # Process payload
        session.process_payload_blocks(payload)
        
        return session
    
    def send_nsr_reply(self, reply_payload):
        """Send NSR message"""
        # Generate NSR tagset
        tagsetKey = HKDF(self.ns_chainkey, ZEROLEN, "SessionReplyTags", 32)
        nsr_tagset = DH_INITIALIZE(self.ns_chainkey, tagsetKey)
        
        # Get tag
        tag, _ = nsr_tagset.get_next_tag()
        
        # Mix tag into hash
        h = SHA256(self.ns_hash || tag)
        
        # Generate ephemeral key
        self.ephemeral_keypair = generate_elg2_keypair()
        bob_ephemeral = self.ephemeral_keypair.public_key
        elg2_bob_ephemeral = ENCODE_ELG2(bob_ephemeral)
        
        # Mix ephemeral key
        h = SHA256(h || bob_ephemeral)
        
        chainKey = self.ns_chainkey
        
        # ee DH
        ee_shared = DH(self.ephemeral_keypair.private_key, 
                      self.remote_ephemeral_key)
        keydata = HKDF(chainKey, ee_shared, "", 32)
        chainKey = keydata[0:31]
        
        # se DH
        se_shared = DH(context.static_keypair.private_key, 
                      self.remote_ephemeral_key)
        keydata = HKDF(chainKey, se_shared, "", 64)
        chainKey = keydata[0:31]
        k_key_section = keydata[32:63]
        
        # Encrypt key section (empty)
        key_section_ciphertext = ENCRYPT(k_key_section, 0, ZEROLEN, h)
        h = SHA256(h || key_section_ciphertext)
        
        # Split for bidirectional ES
        keydata = HKDF(chainKey, ZEROLEN, "", 64)
        k_ab = keydata[0:31]  # Alice → Bob
        k_ba = keydata[32:63]  # Bob → Alice
        
        # Initialize ES tagsets
        self.inbound_tagset = DH_INITIALIZE(chainKey, k_ab)
        self.outbound_tagset = DH_INITIALIZE(chainKey, k_ba)
        
        # Build reply payload
        payload_data = build_payload_blocks(reply_payload)
        
        # Encrypt payload
        k_nsr = HKDF(k_ba, ZEROLEN, "AttachPayloadKDF", 32)
        payload_ciphertext = ENCRYPT(k_nsr, 0, payload_data, h)
        
        # Assemble NSR
        nsr_message = tag + elg2_bob_ephemeral + key_section_ciphertext + payload_ciphertext
        
        # Send
        send_to_network(self.destination, nsr_message)
        
        # Wait for ES
        self.state = SessionState.AWAITING_ES
        self.last_activity = now()
    
    def on_es_received(self, es_message):
        """Process first ES message"""
        if self.state == SessionState.AWAITING_ES:
            # First ES received, confirms session
            self.state = SessionState.ESTABLISHED
        
        # Process ES message
        self.process_es_message(es_message)
    
    def process_es_message(self, es_message):
        """Decrypt and process ES message"""
        # Extract tag
        tag = es_message[0:8]
        ciphertext = es_message[8:]
        
        # Look up tag
        index = self.inbound_tagset.lookup_tag(tag)
        if index is None:
            raise ValueError("Tag not found")
        
        # Get key
        key = self.inbound_keyratchet.get_key(index)
        
        # Construct nonce
        nonce = construct_nonce(index)
        
        # Decrypt
        try:
            payload = DECRYPT(key, nonce, ciphertext, tag)
        except AuthenticationError:
            raise ValueError("ES MAC verification failed")
        
        # Process blocks
        self.process_payload_blocks(payload)
        
        # Update activity
        self.last_activity = now()
```
### Nachrichtenklassifizierung

**Unterscheidung von Nachrichtentypen:**

```python
def classify_message(message):
    """Determine message type"""
    
    # Minimum lengths
    if len(message) < 24:
        return None  # Too short
    
    # Check for session tag (8 bytes)
    tag = message[0:8]
    
    # Try ES decryption first (most common)
    session = lookup_session_by_tag(tag)
    if session:
        return ('ES', session)
    
    # Try NSR decryption (tag + Elligator2 key)
    if len(message) >= 72:
        # Check if bytes 8-40 are valid Elligator2
        try:
            nsr_ephemeral = DECODE_ELG2(message[8:40])
            nsr_session = find_pending_nsr_by_tag(tag)
            if nsr_session:
                return ('NSR', nsr_session)
        except:
            pass
    
    # Try NS decryption (starts with Elligator2 key)
    if len(message) >= 96:
        try:
            ns_ephemeral = DECODE_ELG2(message[0:32])
            ns_session = InboundSession.try_decrypt_ns(message)
            if ns_session:
                return ('NS', ns_session)
        except:
            pass
    
    # Check ElGamal/AES (for dual-key compatibility)
    if len(message) >= 514:
        if (len(message) - 2) % 16 == 0:
            # Might be ElGamal NS
            return ('ELGAMAL_NS', None)
        elif len(message) % 16 == 0:
            # Might be ElGamal ES
            return ('ELGAMAL_ES', None)
    
    return None  # Unknown message type
```
### Bewährte Verfahren für das Sitzungsmanagement

**Sitzungsspeicher:**

```python
class SessionKeyManager:
    def __init__(self):
        # Outbound sessions (one per destination)
        self.outbound_sessions = {}  # destination -> OutboundSession
        
        # Inbound sessions (multiple per destination during transition)
        self.inbound_sessions = []  # [InboundSession]
        
        # Session tag lookup (fast path for ES messages)
        self.tag_to_session = {}  # tag -> InboundSession
        
        # Limits
        self.max_inbound_sessions = 1000
        self.max_tags_per_session = 160
    
    def get_outbound_session(self, destination):
        """Get or create outbound session"""
        if destination not in self.outbound_sessions:
            session = OutboundSession(destination)
            self.outbound_sessions[destination] = session
        return self.outbound_sessions[destination]
    
    def add_inbound_session(self, session):
        """Add new inbound session"""
        # Check limits
        if len(self.inbound_sessions) >= self.max_inbound_sessions:
            self.expire_oldest_session()
        
        self.inbound_sessions.append(session)
        
        # Add tags to lookup table
        self.register_session_tags(session)
    
    def register_session_tags(self, session):
        """Register session's tags in lookup table"""
        for tag in session.inbound_tagset.get_all_tags():
            self.tag_to_session[tag] = session
    
    def lookup_tag(self, tag):
        """Fast tag lookup"""
        return self.tag_to_session.get(tag)
    
    def expire_sessions(self):
        """Periodic session expiration"""
        now_time = now()
        
        # Expire outbound sessions
        for dest, session in list(self.outbound_sessions.items()):
            if session.idle_time(now_time) > 8 * 60:
                del self.outbound_sessions[dest]
        
        # Expire inbound sessions
        expired = []
        for session in self.inbound_sessions:
            if session.idle_time(now_time) > 10 * 60:
                expired.append(session)
        
        for session in expired:
            self.remove_inbound_session(session)
    
    def remove_inbound_session(self, session):
        """Remove inbound session and clean up tags"""
        self.inbound_sessions.remove(session)
        
        # Remove tags from lookup
        for tag in session.inbound_tagset.get_all_tags():
            if tag in self.tag_to_session:
                del self.tag_to_session[tag]
```
**Speicherverwaltung:**

```python
class TagMemoryManager:
    def __init__(self, max_memory_kb=10240):  # 10 MB default
        self.max_memory = max_memory_kb * 1024
        self.current_memory = 0
        self.max_tags_per_session = 160
        self.min_tags_per_session = 32
    
    def calculate_tag_memory(self, session):
        """Calculate memory used by session tags"""
        tag_count = len(session.inbound_tagset.tags)
        # Each tag: 8 bytes (tag) + 2 bytes (index) + 32 bytes (key, optional)
        # + overhead
        bytes_per_tag = 16 if session.defer_keys else 48
        return tag_count * bytes_per_tag
    
    def check_pressure(self):
        """Check if under memory pressure"""
        return self.current_memory > (self.max_memory * 0.9)
    
    def handle_pressure(self):
        """Reduce memory usage when under pressure"""
        if not self.check_pressure():
            return
        
        # Strategy 1: Reduce look-ahead windows
        for session in all_sessions:
            if session.look_ahead > self.min_tags_per_session:
                session.reduce_look_ahead(self.min_tags_per_session)
        
        # Strategy 2: Trim old tags aggressively
        for session in all_sessions:
            session.inbound_tagset.trim_behind(aggressive=True)
        
        # Strategy 3: Refuse new ratchets
        for session in all_sessions:
            if session.outbound_tagset.should_ratchet():
                session.defer_ratchet = True
        
        # Strategy 4: Expire idle sessions early
        expire_idle_sessions(threshold=5*60)  # 5 min instead of 10
```
### Teststrategien

**Unit-Tests:**

```python
def test_x25519_dh():
    """Test X25519 key exchange"""
    alice_sk = GENERATE_PRIVATE()
    alice_pk = DERIVE_PUBLIC(alice_sk)
    
    bob_sk = GENERATE_PRIVATE()
    bob_pk = DERIVE_PUBLIC(bob_sk)
    
    # Both sides compute same shared secret
    alice_shared = DH(alice_sk, bob_pk)
    bob_shared = DH(bob_sk, alice_pk)
    
    assert alice_shared == bob_shared

def test_elligator2_encode_decode():
    """Test Elligator2 roundtrip"""
    sk = GENERATE_PRIVATE_ELG2()
    pk = DERIVE_PUBLIC(sk)
    
    encoded = ENCODE_ELG2(pk)
    decoded = DECODE_ELG2(encoded)
    
    assert decoded == pk

def test_chacha_poly_encrypt_decrypt():
    """Test ChaCha20-Poly1305 AEAD"""
    key = CSRNG(32)
    nonce = construct_nonce(42)
    plaintext = b"Hello, I2P!"
    ad = b"associated_data"
    
    ciphertext = ENCRYPT(key, nonce, plaintext, ad)
    decrypted = DECRYPT(key, nonce, ciphertext, ad)
    
    assert decrypted == plaintext

def test_session_tag_ratchet():
    """Test session tag generation"""
    sessTag_ck = CSRNG(32)
    tagset = SessionTagRatchet(sessTag_ck)
    
    # Generate 100 tags
    tags = [tagset.get_next_tag() for _ in range(100)]
    
    # All tags should be unique
    assert len(set(tags)) == 100
    
    # Each tag should be 8 bytes
    for tag in tags:
        assert len(tag) == 8
```
**Integrationstests:**

```python
def test_ns_nsr_handshake():
    """Test NS/NSR handshake"""
    # Alice creates outbound session
    alice_session = OutboundSession(bob_destination, bound=True)
    
    # Alice sends NS
    ns_message = alice_session.build_ns_message(b"Hello Bob")
    
    # Bob receives NS
    bob_session = InboundSession.try_decrypt_ns(ns_message)
    assert bob_session is not None
    assert bob_session.bound == True
    
    # Bob sends NSR
    nsr_message = bob_session.build_nsr_message(b"Hello Alice")
    
    # Alice receives NSR
    alice_session.on_nsr_received(nsr_message)
    assert alice_session.state == SessionState.ESTABLISHED
    
    # Both should have matching ES tagsets
    # (Cannot directly compare, but can test by sending ES messages)

def test_es_bidirectional():
    """Test ES messages in both directions"""
    # (After NS/NSR handshake)
    
    # Alice sends ES to Bob
    es_alice_to_bob = alice_session.send_es_message(b"Data from Alice")
    
    # Bob receives ES
    bob_session.process_es_message(es_alice_to_bob)
    
    # Bob sends ES to Alice
    es_bob_to_alice = bob_session.send_es_message(b"Data from Bob")
    
    # Alice receives ES
    alice_session.process_es_message(es_bob_to_alice)

def test_dh_ratchet():
    """Test DH ratchet"""
    # (After established session)
    
    # Alice initiates ratchet
    alice_session.initiate_ratchet()
    nextkey_alice = build_nextkey_block(
        flags=0x01,
        key_id=0,
        public_key=alice_new_key
    )
    
    # Send to Bob
    bob_session.process_nextkey_block(nextkey_alice)
    
    # Bob replies
    nextkey_bob = build_nextkey_block(
        flags=0x03,
        key_id=0,
        public_key=bob_new_key
    )
    
    # Send to Alice
    alice_session.process_nextkey_block(nextkey_bob)
    
    # Both should now be using new tagsets
    assert alice_session.outbound_tagset.id == 1
    assert bob_session.inbound_tagset.id == 1
```
**Testvektoren:**

Implementiere Testvektoren aus der Spezifikation:

1. **Noise IK Handshake**: Verwenden Sie die Standard-Testvektoren von Noise
2. **HKDF**: Verwenden Sie die Testvektoren aus RFC 5869
3. **ChaCha20-Poly1305**: Verwenden Sie die Testvektoren aus RFC 7539
4. **Elligator2**: Verwenden Sie die Testvektoren aus dem Elligator2-Paper oder aus OBFS4

**Interoperabilitätstests:**

1. **Java I2P**: Gegen die Referenzimplementierung von Java I2P testen
2. **i2pd**: Gegen die C++-Implementierung i2pd testen
3. **Paketmitschnitte**: Wireshark-Dissektor (falls verfügbar) verwenden, um Nachrichtenformate zu überprüfen
4. **Implementationsübergreifend**: Ein Test-Harness (Testgerüst) erstellen, das zwischen Implementierungen senden und empfangen kann

### Leistungsaspekte

**Schlüsselerzeugung:**

Die Elligator2-Schlüsselgenerierung ist rechenintensiv (50% Verwerfungsrate):

```python
class KeyPool:
    """Pre-generate keys in background thread"""
    def __init__(self, pool_size=10):
        self.pool = Queue(maxsize=pool_size)
        self.generator_thread = Thread(target=self.generate_keys, daemon=True)
        self.generator_thread.start()
    
    def generate_keys(self):
        while True:
            if not self.pool.full():
                keypair = generate_elg2_keypair()
                # Also compute encoded form
                encoded = ENCODE_ELG2(keypair.public_key)
                self.pool.put((keypair, encoded))
            else:
                sleep(0.1)
    
    def get_keypair(self):
        try:
            return self.pool.get(timeout=1.0)
        except Empty:
            # Pool exhausted, generate inline
            return generate_elg2_keypair()
```
**Tag-Abfrage:**

Verwenden Sie Hashtabellen für O(1)-Tag-Lookups:

```python
class FastTagLookup:
    def __init__(self):
        self.tag_to_session = {}  # Python dict is hash table
    
    def add_tag(self, tag, session, index):
        # 8-byte tag as bytes is hashable
        self.tag_to_session[tag] = (session, index)
    
    def lookup_tag(self, tag):
        return self.tag_to_session.get(tag)
```
**Speicheroptimierung:**

Symmetrische Schlüsselgenerierung verschieben:

```python
class DeferredKeyRatchet:
    """Only generate keys when needed"""
    def __init__(self, symmKey_ck):
        self.chainKey = symmKey_ck
        self.index = -1
        self.cache = LRUCache(maxsize=32)  # Cache recent keys
    
    def get_key(self, index):
        # Check cache first
        if index in self.cache:
            return self.cache[index]
        
        # Generate keys up to index
        while self.index < index:
            self.index += 1
            keydata = HKDF(self.chainKey, ZEROLEN, "SymmetricRatchet", 64)
            self.chainKey = keydata[0:31]
            
            if self.index == index:
                key = keydata[32:63]
                self.cache[index] = key
                return key
```
**Stapelverarbeitung:**

Mehrere Nachrichten stapelweise verarbeiten:

```python
def process_message_batch(messages):
    """Process multiple messages efficiently"""
    results = []
    
    # Group by type
    ns_messages = []
    nsr_messages = []
    es_messages = []
    
    for msg in messages:
        msg_type = classify_message(msg)
        if msg_type[0] == 'NS':
            ns_messages.append(msg)
        elif msg_type[0] == 'NSR':
            nsr_messages.append(msg)
        elif msg_type[0] == 'ES':
            es_messages.append(msg)
    
    # Process in batches
    # ES messages are most common, process first
    for msg in es_messages:
        results.append(process_es_message(msg))
    
    for msg in nsr_messages:
        results.append(process_nsr_message(msg))
    
    for msg in ns_messages:
        results.append(process_ns_message(msg))
    
    return results
```
---

## Sicherheitsüberlegungen

### Bedrohungsmodell

**Gegnerische Fähigkeiten:**

1. **Passiver Beobachter**: Kann den gesamten Netzwerkverkehr beobachten
2. **Aktiver Angreifer**: Kann Nachrichten einschleusen, modifizieren, verwerfen, erneut abspielen
3. **Kompromittierter Knoten**: Kann einen router oder ein Ziel kompromittieren
4. **Verkehrsanalyse**: Kann statistische Analysen von Verkehrsmustern durchführen

**Sicherheitsziele:**

1. **Vertraulichkeit**: Nachrichteninhalte vor Beobachtern verborgen
2. **Authentifizierung**: Absenderidentität verifiziert (für gebundene Sitzungen)
3. **Vorwärtsgeheimnis**: Frühere Nachrichten bleiben geheim, selbst wenn Schlüssel kompromittiert sind
4. **Schutz vor Wiederholungsangriffen**: Alte Nachrichten können nicht erneut verwendet werden
5. **Verschleierung des Datenverkehrs**: Handshakes sind nicht von Zufallsdaten zu unterscheiden

### Kryptografische Annahmen

**Härteannahmen:**

1. **X25519 CDH**: Das Computational-Diffie-Hellman-Problem ist auf Curve25519 hart
2. **ChaCha20 PRF**: ChaCha20 ist eine pseudozufällige Funktion
3. **Poly1305 MAC**: Poly1305 ist unter gewähltem Nachrichtenangriff unfälschbar
4. **SHA-256 CR**: SHA-256 ist kollisionsresistent
5. **HKDF Security**: HKDF extrahiert und erweitert gleichmäßig verteilte Schlüssel

**Sicherheitsstufen:**

- **X25519**: ~128-Bit-Sicherheitsniveau (Ordnung der Kurve 2^252)
- **ChaCha20**: 256-Bit-Schlüssel, 256-Bit-Sicherheitsniveau
- **Poly1305**: 128-Bit-Sicherheitsniveau (Kollisionswahrscheinlichkeit)
- **SHA-256**: 128-Bit-Kollisionsresistenz, 256-Bit-Urbildresistenz

### Schlüsselverwaltung

**Schlüsselerzeugung:**

```python
# CRITICAL: Use cryptographically secure RNG
def CSRNG(length):
    # GOOD: os.urandom, secrets.token_bytes (Python)
    # GOOD: /dev/urandom (Linux)
    # GOOD: BCryptGenRandom (Windows)
    # BAD: random.random(), Math.random() (NOT cryptographically secure)
    return os.urandom(length)

# CRITICAL: Validate keys
def validate_x25519_key(pubkey):
    # Check for weak keys (all zeros, small order points)
    if pubkey == bytes(32):
        raise WeakKeyError("All-zero public key")
    
    # Perform DH to check for weak shared secrets
    test_shared = DH(test_private_key, pubkey)
    if test_shared == bytes(32):
        raise WeakKeyError("Results in zero shared secret")
```
**Schlüsselspeicherung:**

```python
# CRITICAL: Protect private keys
class SecureKeyStorage:
    def __init__(self):
        # Store in memory with protection
        self.keys = {}
        
        # Option 1: Memory locking (prevent swapping to disk)
        # mlock(self.keys)
        
        # Option 2: Encrypted storage
        # self.encryption_key = derive_from_password()
    
    def store_key(self, key_id, private_key):
        # Option: Encrypt before storage
        # encrypted = encrypt(private_key, self.encryption_key)
        # self.keys[key_id] = encrypted
        self.keys[key_id] = private_key
    
    def delete_key(self, key_id):
        # Securely wipe memory
        if key_id in self.keys:
            key = self.keys[key_id]
            # Overwrite with zeros before deletion
            for i in range(len(key)):
                key[i] = 0
            del self.keys[key_id]
```
**Schlüsselrotation:**

```python
# CRITICAL: Rotate keys regularly
class KeyRotationPolicy:
    def __init__(self):
        self.max_messages_per_tagset = 4096  # Ratchet before 65535
        self.max_tagset_age = 10 * 60       # 10 minutes
        self.max_session_age = 60 * 60      # 1 hour
    
    def should_ratchet(self, tagset):
        return (tagset.messages_sent >= self.max_messages_per_tagset or
                tagset.age() >= self.max_tagset_age)
    
    def should_replace_session(self, session):
        return session.age() >= self.max_session_age
```
### Abwehrmaßnahmen gegen Angriffe

### Gegenmaßnahmen gegen Replay-Angriffe

**Validierung von Datum und Uhrzeit:**

```python
MAX_CLOCK_SKEW_PAST = 5 * 60
MAX_CLOCK_SKEW_FUTURE = 2 * 60

def validate_datetime(timestamp):
    now = int(time.time())
    age = now - timestamp
    
    if age < -MAX_CLOCK_SKEW_FUTURE:
        raise ReplayError("Timestamp too far in future")
    
    if age > MAX_CLOCK_SKEW_PAST:
        raise ReplayError("Timestamp too old")
    
    return True
```
**Bloom-Filter für NS-Nachrichten:**

```python
class ReplayFilter:
    def __init__(self, capacity=100000, error_rate=0.001, duration=5*60):
        self.bloom = BloomFilter(capacity=capacity, error_rate=error_rate)
        self.duration = duration
        self.entries = []  # (timestamp, ephemeral_key)
    
    def check_replay(self, ephemeral_key, timestamp):
        # Validate timestamp
        if not validate_datetime(timestamp):
            return False
        
        # Check Bloom filter
        if ephemeral_key in self.bloom:
            # Potential replay (or false positive)
            # Check exact match in entries
            for ts, key in self.entries:
                if key == ephemeral_key:
                    return False  # Definite replay
        
        # Add to filter
        self.bloom.add(ephemeral_key)
        self.entries.append((timestamp, ephemeral_key))
        
        # Expire old entries
        self.expire_old_entries()
        
        return True
    
    def expire_old_entries(self):
        now = int(time.time())
        self.entries = [(ts, key) for ts, key in self.entries
                       if now - ts < self.duration]
```
**Einmalige Verwendung von Session-Tags:**

```python
def process_session_tag(tag):
    # Look up tag
    entry = tagset.lookup_tag(tag)
    if entry is None:
        raise ValueError("Invalid session tag")
    
    # CRITICAL: Remove tag immediately (one-time use)
    tagset.remove_tag(tag)
    
    # Use associated key
    return entry.key, entry.index
```
### Gegenmaßnahmen gegen Key Compromise Impersonation (KCI, Identitätsanmaßung nach Schlüsselkompromittierung)

**Problem**: NS-Nachrichtenauthentifizierung ist anfällig für KCI (Key Compromise Impersonation, Identitätsanmaßung nach Schlüsselkompromittierung) (Authentifizierungsstufe 1)

**Gegenmaßnahme**:

1. Stellen Sie so schnell wie möglich auf NSR (Authentifizierungsstufe 2) um
2. Verlassen Sie sich für sicherheitskritische Vorgänge nicht auf die NS-Payload
3. Warten Sie auf die NSR-Bestätigung, bevor Sie unumkehrbare Aktionen durchführen

```python
def process_ns_message(ns_message):
    # NS authenticated at Level 1 (KCI vulnerable)
    # Do NOT perform security-critical operations yet
    
    # Extract sender's static key
    sender_key = ns_message.static_key
    
    # Mark session as pending Level 2 authentication
    session.auth_level = 1
    session.sender_key = sender_key
    
    # Send NSR
    send_nsr_reply(session)

def process_first_es_message(es_message):
    # Now we have Level 2 authentication (KCI resistant)
    session.auth_level = 2
    
    # Safe to perform security-critical operations
    process_security_critical_operation(es_message)
```
### Gegenmaßnahmen gegen Denial-of-Service

**NS-Flood-Schutz:**

```python
class NSFloodProtection:
    def __init__(self):
        self.ns_count = defaultdict(int)  # source -> count
        self.ns_timestamps = defaultdict(list)  # source -> [timestamps]
        
        self.max_ns_per_source = 5
        self.rate_window = 10  # seconds
        self.max_concurrent_ns = 100
    
    def check_ns_allowed(self, source):
        # Global limit
        total_pending = sum(self.ns_count.values())
        if total_pending >= self.max_concurrent_ns:
            return False
        
        # Per-source rate limit
        now = time.time()
        timestamps = self.ns_timestamps[source]
        
        # Remove old timestamps
        timestamps = [ts for ts in timestamps if now - ts < self.rate_window]
        self.ns_timestamps[source] = timestamps
        
        # Check rate
        if len(timestamps) >= self.max_ns_per_source:
            return False
        
        # Allow NS
        timestamps.append(now)
        self.ns_count[source] += 1
        return True
    
    def on_session_established(self, source):
        # Decrease pending count
        if self.ns_count[source] > 0:
            self.ns_count[source] -= 1
```
**Speichergrenzen für Tags:**

```python
class TagStorageLimit:
    def __init__(self, max_tags=1000000):
        self.max_tags = max_tags
        self.current_tags = 0
    
    def can_create_session(self, look_ahead):
        if self.current_tags + look_ahead > self.max_tags:
            return False
        return True
    
    def add_tags(self, count):
        self.current_tags += count
    
    def remove_tags(self, count):
        self.current_tags -= count
```
**Adaptives Ressourcenmanagement:**

```python
class AdaptiveResourceManager:
    def __init__(self):
        self.load_level = 0  # 0 = low, 1 = medium, 2 = high, 3 = critical
    
    def adjust_parameters(self):
        if self.load_level == 0:
            # Normal operation
            return {
                'max_look_ahead': 160,
                'max_sessions': 1000,
                'session_timeout': 10 * 60
            }
        
        elif self.load_level == 1:
            # Moderate load
            return {
                'max_look_ahead': 80,
                'max_sessions': 800,
                'session_timeout': 8 * 60
            }
        
        elif self.load_level == 2:
            # High load
            return {
                'max_look_ahead': 32,
                'max_sessions': 500,
                'session_timeout': 5 * 60
            }
        
        else:  # load_level == 3
            # Critical load
            return {
                'max_look_ahead': 16,
                'max_sessions': 200,
                'session_timeout': 3 * 60
            }
```
### Widerstandsfähigkeit gegen Datenverkehrsanalyse

**Elligator2-Kodierung:**

Stellt sicher, dass Handshake-Nachrichten nicht von Zufallsdaten zu unterscheiden sind:

```python
# NS and NSR start with Elligator2-encoded ephemeral keys
# Observer cannot distinguish from random 32-byte string
```
**Padding-Strategien:**

```python
# Resist message size fingerprinting
def add_padding(payload, strategy='random'):
    if strategy == 'random':
        # Random padding 0-15 bytes
        size = random.randint(0, 15)
    
    elif strategy == 'round':
        # Round to next 64-byte boundary
        target = ((len(payload) + 63) // 64) * 64
        size = target - len(payload) - 3  # -3 for block header
    
    elif strategy == 'fixed':
        # Always 1KB messages
        size = 1024 - len(payload) - 3
    
    return build_padding_block(size)
```
**Timing-Angriffe:**

```python
# CRITICAL: Use constant-time operations
def constant_time_compare(a, b):
    """Constant-time byte string comparison"""
    if len(a) != len(b):
        return False
    
    result = 0
    for x, y in zip(a, b):
        result |= x ^ y
    
    return result == 0

# CRITICAL: Constant-time MAC verification
def verify_mac(computed_mac, received_mac):
    if not constant_time_compare(computed_mac, received_mac):
        # Always take same time regardless of where comparison fails
        raise AuthenticationError("MAC verification failed")
```
### Fallstricke bei der Implementierung

**Häufige Fehler:**

1. **Nonce-Wiederverwendung** (Einmalwert): NIEMALS (Schlüssel, Nonce)-Paare wiederverwenden
   ```python
   # BAD: Reusing nonce with same key
   ciphertext1 = ENCRYPT(key, nonce, plaintext1, ad1)
   ciphertext2 = ENCRYPT(key, nonce, plaintext2, ad2)  # CATASTROPHIC

# GUT: Eindeutiger nonce (einmaliger Zufallswert) für jede Nachricht    ciphertext1 = ENCRYPT(key, nonce1, plaintext1, ad1)    ciphertext2 = ENCRYPT(key, nonce2, plaintext2, ad2)

   ```

2. **Ephemeral Key Reuse**: Generate fresh ephemeral key for each NS/NSR
   ```python
# FALSCH: Wiederverwendung eines ephemeren Schlüssels    ephemeral_key = generate_elg2_keypair()    send_ns_message(ephemeral_key)    send_ns_message(ephemeral_key)  # FALSCH

# GUT: Neuer Schlüssel für jede Nachricht    send_ns_message(generate_elg2_keypair())    send_ns_message(generate_elg2_keypair())

   ```

3. **Weak RNG**: Use cryptographically secure random number generator
   ```python
# SCHLECHT: Nicht-kryptografischer Zufallszahlengenerator (RNG)    import random    key = bytes([random.randint(0, 255) for _ in range(32)])  # UNSICHER

# GUT: Kryptografisch sicherer Zufallszahlengenerator    import os    key = os.urandom(32)

   ```

4. **Timing Attacks**: Use constant-time comparisons
   ```python
# SCHLECHT: Vergleich mit frühem Abbruch    if computed_mac == received_mac:  # Timing-Leak

       pass
   
# GUT: Zeitkonstanter Vergleich    if constant_time_compare(computed_mac, received_mac):

       pass
   ```

5. **Incomplete MAC Verification**: Always verify before using data
   ```python
# SCHLECHT: Entschlüsselung vor der Überprüfung    plaintext = chacha20_decrypt(key, nonce, ciphertext)    mac_ok = verify_mac(mac, plaintext)  # ZU SPÄT    if not mac_ok:

       return error
   
# GUT: AEAD verifiziert vor dem Entschlüsseln    try:

       plaintext = DECRYPT(key, nonce, ciphertext, ad)  # Verifies MAC first
except AuthenticationError:

       return error
   ```

6. **Key Deletion**: Securely wipe keys from memory
   ```python
# SCHLECHT: Einfaches Löschen    del private_key  # Noch im Speicher

# GUT: Vor dem Löschen überschreiben    for i in range(len(private_key)):

       private_key[i] = 0
del private_key

   ```

### Security Audits

**Recommended Audits:**

1. **Cryptographic Review**: Expert review of KDF chains and DH operations
2. **Implementation Audit**: Code review for timing attacks, key management, RNG usage
3. **Protocol Analysis**: Formal verification of handshake security properties
4. **Side-Channel Analysis**: Timing, power, and cache attacks
5. **Fuzzing**: Random input testing for parser robustness

**Test Cases:**

```python
# Sicherheitskritische Testfälle

def test_nonce_uniqueness():

    """Ensure nonces are never reused"""
    nonces = set()
    for i in range(10000):
        nonce = construct_nonce(i)
        assert nonce not in nonces
        nonces.add(nonce)

def test_key_isolation():

    """Ensure sessions don't share keys"""
    session1 = create_session(destination1)
    session2 = create_session(destination2)
    
    assert session1.key != session2.key

def test_replay_prevention():

    """Ensure replay attacks are detected"""
    ns_message = create_ns_message()
    
    # First delivery succeeds
    assert process_ns_message(ns_message) == True
    
    # Replay fails
    assert process_ns_message(ns_message) == False

def test_mac_verification():

    """Ensure MAC verification is enforced"""
    key = CSRNG(32)
    nonce = construct_nonce(0)
    plaintext = b"test"
    ad = b"test_ad"
    
    ciphertext = ENCRYPT(key, nonce, plaintext, ad)
    
    # Correct MAC verifies
    assert DECRYPT(key, nonce, ciphertext, ad) == plaintext
    
    # Corrupted MAC fails
    corrupted = ciphertext[:-1] + bytes([ciphertext[-1] ^ 0xFF])
    with pytest.raises(AuthenticationError):
        DECRYPT(key, nonce, corrupted, ad)
```

---

## Configuration and Deployment

### I2CP Configuration

**Enable ECIES Encryption:**

```properties
# Nur ECIES (Elliptic Curve Integrated Encryption Scheme, integriertes Verschlüsselungsschema auf elliptischen Kurven) (für neue Bereitstellungen empfohlen)

i2cp.leaseSetEncType=4

# Doppelschlüssel (ECIES + ElGamal zur Kompatibilität)

i2cp.leaseSetEncType=4,0

# Nur ElGamal (veraltet, nicht empfohlen)

i2cp.leaseSetEncType=0

```

**LeaseSet Type:**

```properties
# Standard LS2 (am häufigsten)

i2cp.leaseSetType=3

# Verschlüsseltes LS2 (blinded destinations, verblindete Destinationen)

i2cp.leaseSetType=5

# Meta LS2 (erweiterter LeaseSet2-Typ; mehrere Ziele)

i2cp.leaseSetType=7

```

**Additional Options:**

```properties
# Statischer Schlüssel für ECIES (Elliptic Curve Integrated Encryption Scheme, Verschlüsselungsschema mit elliptischen Kurven; optional, wird automatisch generiert, wenn nicht angegeben)

# Öffentlicher X25519-Schlüssel mit 32 Byte, Base64-kodiert

i2cp.leaseSetPrivateKey=<base64-encoded-key>

# Signaturtyp (für LeaseSet)

i2cp.leaseSetSigningPrivateKey=<base64-encoded-key> i2cp.leaseSetSigningType=7  # Ed25519

```

### Java I2P Configuration

**router.config:**

```properties
# Router-zu-Router ECIES

i2p.router.useECIES=true

```

**Build Properties:**

```java
// Für I2CP-Clients (Java) Properties props = new Properties(); props.setProperty("i2cp.leaseSetEncType", "4"); props.setProperty("i2cp.leaseSetType", "3");

I2PSession session = i2pClient.createSession(props);

```

### i2pd Configuration

**i2pd.conf:**

```ini
[limits]

# Speicherlimit für ECIES-Sitzungen

ecies.memory = 128M

[ecies]

# ECIES aktivieren (integriertes Verschlüsselungsschema mit elliptischen Kurven)

enabled = true

# Nur ECIES (integriertes Verschlüsselungsverfahren mit elliptischen Kurven) oder Dual-Schlüssel

compatibility = true  # true = dual-key (Zweischlüsselmodus), false = nur ECIES

```

**Tunnels Configuration:**

```ini
[my-service] type = http host = 127.0.0.1 port = 8080 keys = my-service-keys.dat

# Nur ECIES (integriertes Verschlüsselungsverfahren mit elliptischen Kurven)

ecies = true

```

### Compatibility Matrix

**Router Version Support:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">ECIES Support</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">LS2 Support</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Dual-Key</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">&lt; 0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">❌ No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">❌ No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">N/A</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy only</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.38-0.9.45</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">❌ No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">N/A</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LS2 only</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.46-0.9.50</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Initial ECIES</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.5.0+</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.0.0+</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
  </tbody>
</table>

**Destination Compatibility:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Destination Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Can Connect To</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-only</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-only, Dual-key</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Requires 0.9.46+ routers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Dual-key</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Maximum compatibility</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal-only</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal-only, Dual-key</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy</td>
    </tr>
  </tbody>
</table>

**FloodFill Requirements:**

- **ECIES-only destinations**: Require majority of floodfills on 0.9.46+ for encrypted lookups
- **Dual-key destinations**: Work with any floodfill version
- **Current status**: Near 100% floodfill adoption as of 2025

### Migration Guide

**Migrating from ElGamal to ECIES:**

**Step 1: Enable Dual-Key Mode**

```properties
# ECIES (Elliptic Curve Integrated Encryption Scheme, integriertes Verschlüsselungsschema auf elliptischen Kurven) hinzufügen und dabei ElGamal (asymmetrisches Verschlüsselungsverfahren) beibehalten

i2cp.leaseSetEncType=4,0

```

**Step 2: Monitor Connections**

```bash
# Verbindungstypen prüfen

i2prouter.exe status

# oder

http://127.0.0.1:7657/peers

```

**Step 3: Switch to ECIES-Only (after testing)**

```properties
# ElGamal entfernen

i2cp.leaseSetEncType=4

```

**Step 4: Restart Application**

```bash
# I2P router oder Anwendung neu starten

systemctl restart i2p

# oder

i2prouter.exe restart

```

**Rollback Plan:**

```properties
# Bei Problemen auf nur ElGamal zurückfallen

i2cp.leaseSetEncType=0

```

### Performance Tuning

**Session Limits:**

```properties
# Maximale Anzahl eingehender Sitzungen

i2p.router.maxInboundSessions=1000

# Maximale Anzahl ausgehender Sitzungen

i2p.router.maxOutboundSessions=1000

# Sitzungs-Timeout (Sekunden)

i2p.router.sessionTimeout=600

```

**Memory Limits:**

```properties
# Speicherlimit für Tags (KB)

i2p.ecies.maxTagMemory=10240  # 10 MB

# Vorausschaufenster

i2p.ecies.tagLookAhead=160 i2p.ecies.tagLookAheadMin=32

```

**Ratchet Policy:**

```properties
# Nachrichten vor dem Ratchet (kryptografischer Ratschen-Mechanismus)

i2p.ecies.ratchetThreshold=4096

# Zeit vor dem ratchet (kryptografischer Schlüsselfortschrittsmechanismus) (Sekunden)

i2p.ecies.ratchetTimeout=600  # 10 Minuten

```

### Monitoring and Debugging

**Logging:**

```properties
# Debug-Protokollierung für ECIES (integriertes Verschlüsselungsverfahren mit elliptischen Kurven) aktivieren

logger.i2p.router.transport.ecies=DEBUG

```

**Metrics:**

Monitor these metrics:

1. **NS Success Rate**: Percentage of NS messages receiving NSR
2. **Session Establishment Time**: Time from NS to first ES
3. **Tag Storage Usage**: Current memory usage for tags
4. **Ratchet Frequency**: How often sessions ratchet
5. **Session Lifetime**: Average session duration

**Common Issues:**

1. **NS Timeout**: No NSR received
   - Check destination is online
   - Check floodfill availability
   - Verify LeaseSet published correctly

2. **High Memory Usage**: Too many tags stored
   - Reduce look-ahead window
   - Decrease session timeout
   - Implement aggressive expiration

3. **Frequent Ratchets**: Sessions ratcheting too often
   - Increase ratchet threshold
   - Check for retransmissions

4. **Session Failures**: ES messages failing to decrypt
   - Verify tag synchronization
   - Check for replay attacks
   - Validate nonce construction

---

## References

### Specifications

1. **ECIES Proposal**: [Proposal 144](/proposals/144-ecies-x25519-aead-ratchet/)
2. **I2NP**: [I2NP Specification](/docs/specs/i2np/)
3. **Common Structures**: [Common Structures Specification](/docs/specs/common-structures/)
4. **NTCP2**: [NTCP2 Specification](/docs/specs/ntcp2/)
5. **SSU2**: [SSU2 Specification](/docs/specs/ssu2/)
6. **I2CP**: [I2CP Specification](/docs/specs/i2cp/)
7. **ElGamal/AES+SessionTags**: [ElGamal/AES Specification](/docs/legacy/elgamal-aes/)

### Cryptographic Standards

1. **Noise Protocol Framework**: [Noise Specification](https://noiseprotocol.org/noise.html) (Revision 34, 2018-07-11)
2. **Signal Double Ratchet**: [Signal Specification](https://signal.org/docs/specifications/doubleratchet/)
3. **RFC 7748**: [Elliptic Curves for Security (X25519)](https://tools.ietf.org/html/rfc7748)
4. **RFC 7539**: [ChaCha20 and Poly1305 for IETF Protocols](https://tools.ietf.org/html/rfc7539)
5. **RFC 5869**: [HKDF (HMAC-based Key Derivation Function)](https://tools.ietf.org/html/rfc5869)
6. **RFC 2104**: [HMAC: Keyed-Hashing for Message Authentication](https://tools.ietf.org/html/rfc2104)
7. **Elligator2**: [Elligator Paper](https://elligator.cr.yp.to/elligator-20130828.pdf)

### Implementation Resources

1. **Java I2P**: [i2p.i2p Repository](https://github.com/i2p/i2p.i2p)
2. **i2pd (C++)**: [i2pd Repository](https://github.com/PurpleI2P/i2pd)
3. **OBFS4 (Elligator2)**: [obfs4proxy Repository](https://gitlab.com/yawning/obfs4)

### Additional Information

1. **I2P Website**: [/](/)
2. **I2P Forum**: [https://i2pforum.net](https://i2pforum.net)
3. **I2P Wiki**: [https://wiki.i2p-projekt.de](https://wiki.i2p-projekt.de)

---

## Appendix A: KDF Summary

**All KDF Operations in ECIES:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Input</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Info String</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Output</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NS Initial ChainKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">protocol_name</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">(none - SHA256)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">h, chainKey</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NS Static Key Section</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, es_shared</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">""</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, k</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NS Payload Section (bound)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, ss_shared</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">""</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, k</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR Tagset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"SessionReplyTags"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">tagsetKey</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR ee DH</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, ee_shared</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">""</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR se DH</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, se_shared</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">""</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, k</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR Split</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">""</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">k_ab, k_ba</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR Payload</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">k_ba</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"AttachPayloadKDF"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">k_nsr</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DH Initialize</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">rootKey, k</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"KDFDHRatchetStep"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">nextRootKey, chainKey</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Tag and Key Chain Keys</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"TagAndKeyGenKeys"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">sessTag_ck, symmKey_ck</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Session Tag Init</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">sessTag_ck</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"STInitialization"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, CONSTANT</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Session Tag Gen</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, CONSTANT</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"SessionTagKeyGen"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, tag</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Symmetric Key Gen</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"SymmetricRatchet"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DH Ratchet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">sharedSecret</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"XDHRatchetTagSet"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">tagsetKey</td>
    </tr>
  </tbody>
</table>

---

## Appendix B: Message Size Calculator

**Calculate message sizes for capacity planning:**

```python
def calculate_ns_size(payload_size, bound=True):

    """Calculate New Session message size"""
    ephemeral_key = 32
    static_section = 32 + 16  # encrypted + MAC
    payload_encrypted = payload_size + 16  # + MAC
    
    return ephemeral_key + static_section + payload_encrypted

def calculate_nsr_size(payload_size):

    """Calculate New Session Reply message size"""
    tag = 8
    ephemeral_key = 32
    key_section_mac = 16
    payload_encrypted = payload_size + 16  # + MAC
    
    return tag + ephemeral_key + key_section_mac + payload_encrypted

def calculate_es_size(payload_size):

    """Calculate Existing Session message size"""
    tag = 8
    payload_encrypted = payload_size + 16  # + MAC
    
    return tag + payload_encrypted

# Beispiele

print("NS (gebunden, 1 KB Nutzlast):", calculate_ns_size(1024, bound=True), "Bytes")

# Ausgabe: 1120 Bytes

print("NSR (1KB payload):", calculate_nsr_size(1024), "bytes")

# Ausgabe: 1096 Bytes

print("ES (1KB Nutzlast):", calculate_es_size(1024), "Bytes")

# Ausgabe: 1048 Bytes

```

---

## Appendix C: Glossary

**AEAD**: Authenticated Encryption with Associated Data - encryption mode that provides both confidentiality and authenticity

**Authentication Level**: Noise protocol security property indicating strength of sender identity verification

**Binding**: Association of a session with a specific far-end destination

**ChaCha20**: Stream cipher designed by Daniel J. Bernstein

**ChainKey**: Cryptographic key used in HKDF chains to derive subsequent keys

**Confidentiality Level**: Noise protocol security property indicating strength of forward secrecy

**DH**: Diffie-Hellman key agreement protocol

**Elligator2**: Encoding technique to make elliptic curve points indistinguishable from random

**Ephemeral Key**: Short-lived key used only for a single handshake

**ES**: Existing Session message (used after handshake completion)

**Forward Secrecy**: Property ensuring past communications remain secure if keys are compromised

**Garlic Clove**: I2NP message container for end-to-end delivery

**HKDF**: HMAC-based Key Derivation Function

**IK Pattern**: Noise handshake pattern where initiator sends static key immediately

**KCI**: Key Compromise Impersonation attack

**KDF**: Key Derivation Function - cryptographic function for generating keys from other keys

**LeaseSet**: I2P structure containing a destination's public keys and tunnel information

**LS2**: LeaseSet version 2 with encryption type support

**MAC**: Message Authentication Code - cryptographic checksum proving authenticity

**MixHash**: Noise protocol function for maintaining running hash transcript

**NS**: New Session message (initiates new session)

**NSR**: New Session Reply message (response to NS)

**Nonce**: Number used once - ensures unique encryption even with same key

**Pairing**: Linking an inbound session with an outbound session for bidirectional communication

**Poly1305**: Message authentication code designed by Daniel J. Bernstein

**Ratchet**: Cryptographic mechanism for deriving sequential keys

**Session Tag**: 8-byte one-time identifier for existing session messages

**Static Key**: Long-term key associated with a destination's identity

**Tag Set**: Collection of session tags derived from a common root

**X25519**: Elliptic curve Diffie-Hellman key agreement using Curve25519

---