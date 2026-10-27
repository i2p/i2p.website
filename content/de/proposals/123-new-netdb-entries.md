---
title: "Neue netDB-Einträge"
number: "123"
author: "zzz, str4d, orignal"
created: "2016-01-16"
lastupdated: "2020-07-18"
status: "Öffnen"
thread: "http://zzz.i2p/topics/2051"
supercedes: "110, 120, 121, 122"
toc: true
---

## Status

Teile dieses Vorschlags sind abgeschlossen und in Version 0.9.38 und 0.9.39 implementiert.   Die Spezifikationen für gemeinsame Strukturen, I2CP, I2NP und andere   sind nun aktualisiert, um die jetzt unterstützten Änderungen widerzuspiegeln.

Die abgeschlossenen Teile unterliegen weiterhin geringfügigen Überarbeitungen.   Andere Teile dieses Vorschlags befinden sich noch in Entwicklung   und unterliegen erheblichen Änderungen.

Die Dienstsuche (Typen 9 und 11) hat niedrige Priorität,   ist nicht terminiert und könnte in einen separaten Vorschlag ausgelagert werden.

## Übersicht

Dies ist eine Aktualisierung und Zusammenfassung der folgenden 4 Vorschläge:

- 110 LS2
- 120 Meta LS2 für massives Multihoming
- 121 Verschlüsseltes LS2
- 122 Unauthentifizierte Dienstsuche (Anycasting)

Diese Vorschläge sind größtenteils unabhängig, aber aus Gründen der Konsistenz definieren wir und verwenden ein gemeinsames Format für mehrere davon.

Die folgenden Vorschläge sind teilweise verwandt:

- 140 Unsichtbares Multihoming (inkompatibel mit diesem Vorschlag)
- 142 Neues Kryptovorlage (für neue symmetrische Kryptografie)
- 144 ECIES-X25519-AEAD-Ratchet
- 145 ECIES-P256
- 146 Red25519
- 148 EdDSA-BLAKE2b-Ed25519
- 149 B32 für verschlüsseltes LS2
- 150 Garlic-Farm-Protokoll
- 151 ECDSA-Blinding

## Vorschlag

Dieser Vorschlag definiert 5 neue DatabaseEntry-Typen und den Prozess zum   Speichern und Abrufen aus der Netzwerkdatenbank,   sowie die Methode zum Signieren und Verifizieren dieser Signaturen.

### Ziele

- Rückwärtskompatibel
- LS2 verwendbar mit altem Multihoming
- Keine neuen Kryptoverfahren oder Primitiva erforderlich
- Beibehaltung der Entkopplung von Kryptografie und Signatur; Unterstützung aller aktuellen und zukünftigen Versionen
- Unterstützung optionaler Offline-Signaturschlüssel
- Reduzierung der Zeitstempelgenauigkeit zur Verringerung von Fingerprinting
- Aktivierung neuer Kryptoverfahren für Ziele
- Massive Multihoming-Fähigkeit
- Behebung mehrerer Probleme mit bestehenden verschlüsselten LS
- Optionales Blinding zur Verringerung der Sichtbarkeit durch Floodfills
- Verschlüsselung unterstützt sowohl Einzelschlüssel als auch mehrere widerrufbare Schlüssel
- Dienstsuche für einfachere Suche nach Outproxies, Anwendung-DHT-Bootstrap und andere Anwendungen
- Nichts brechen, was auf 32-Byte-binären Ziel-Hashes basiert, z. B. BitTorrent
- Flexibilität in Leasesets durch Eigenschaften, wie wir sie in Routerinfos haben
- Veröffentlichungszeitstempel und variable Ablaufzeit im Header, damit es auch funktioniert, wenn Inhalte verschlüsselt sind (nicht Zeitstempel aus frühester Lease ableiten)
- Alle neuen Typen befinden sich im selben DHT-Bereich und an denselben Orten wie bestehende Leasesets, sodass Benutzer vom alten LS zu LS2 migrieren oder zwischen LS2, Meta und Verschlüsselt wechseln können, ohne Ziel oder Hash zu ändern
- Ein vorhandenes Ziel kann zur Verwendung von Offline-Schlüsseln konvertiert werden oder zurück zu Online-Schlüsseln, ohne Ziel oder Hash zu ändern

### Nicht-Ziele / Außerhalb des Umfangs

- Neuer DHT-Rotationsalgorithmus oder gemeinsame Zufallszahlengenerierung
- Der spezifische neue Verschlüsselungstyp und das Ende-zu-Ende-Verschlüsselungsschema, um diesen neuen Typ zu verwenden, wären Gegenstand eines separaten Vorschlags. Hier wird keine neue Kryptografie spezifiziert oder diskutiert.
- Neue Verschlüsselung für RIs oder Tunnelaufbau. Das wäre Gegenstand eines separaten Vorschlags.
- Methoden zur Verschlüsselung, Übertragung und Empfang von I2NP DLM / DSM / DSRM-Nachrichten. Bleibt unverändert.
- Wie Meta generiert und unterstützt wird, einschließlich Backend-Inter-Router-Kommunikation, Management, Failover und Koordination. Unterstützung könnte I2CP, i2pcontrol oder ein neues Protokoll hinzugefügt werden. Dies könnte standardisiert werden oder auch nicht.
- Wie tatsächlich länger laufende Tunnel implementiert und verwaltet oder bestehende Tunnel abgebrochen werden. Das ist extrem schwierig, und ohne dies kann kein vernünftiger, sanfter Herunterfahren erfolgen.
- Änderungen am Bedrohungsmodell
- Offline-Speicherformat oder Methoden zum Speichern/Abrufen/Teilen der Daten
- Implementierungsdetails werden hier nicht diskutiert und bleiben jedem Projekt überlassen

### Begründung

LS2 fügt Felder für die Änderung des Verschlüsselungstyps und zukünftige Protokolländerungen hinzu.

Verschlüsseltes LS2 behebt mehrere Sicherheitsprobleme mit dem bestehenden verschlüsselten LS, indem die gesamte Menge von Leases asymmetrisch verschlüsselt wird.

Meta LS2 bietet flexibles, effizientes, effektives und großskaliges Multihoming.

Dienst-Eintrag und Dienst-Liste bieten Anycast-Dienste wie Namenssuche und DHT-Bootstrap.

### NetDB-Datentypen

Die Typnummern werden in den I2NP Database Lookup/Store-Nachrichten verwendet.

Die Spalte „Ende-zu-Ende“ bezieht sich darauf, ob Abfragen/Antworten an ein Ziel in einer Garlic-Nachricht gesendet werden.

Bestehende Typen:

| NetDB-Daten | Lookup-Typ | Store-Typ |
|------------|-------------|------------|
| beliebig   | 0           | beliebig   |
| LS         | 1           | 1          |
| RI         | 2           | 0          |
| explorativ | 3           | DSRM       |
Neue Typen:

| NetDB-Daten     | Lookup-Typ | Store-Typ | Standard-LS2-Header? | Ende-zu-Ende gesendet? |
|----------------|-------------|------------|------------------|------------------|
| LS2            | 1           | 3          | ja               | ja               |
| Verschlüsseltes LS2  | 1           | 5          | nein             | nein             |
| Meta LS2       | 1           | 7          | ja               | nein             |
| Dienst-Eintrag | n/a         | 9          | ja               | nein             |
| Dienst-Liste   | 4           | 11         | nein             | nein             |
### Hinweise

- Lookup-Typen verwenden derzeit die Bits 3-2 in der Database Lookup-Nachricht.  
  Zusätzliche Typen würden die Verwendung von Bit 4 erfordern.

- Alle Store-Typen sind ungerade, da die oberen Bits im Typfeld der Database Store-Nachricht von alten Routern ignoriert werden.  
  Wir bevorzugen, dass das Parsen als LS fehlschlägt, nicht als komprimiertes RI.

- Sollte der Typ explizit, implizit oder gar nicht in den durch die Signatur abgedeckten Daten sein?

### Lookup/Store-Prozess

Typen 3, 5 und 7 können als Antwort auf eine Standard-Leaseset-Abfrage (Typ 1) zurückgegeben werden.   Typ 9 wird niemals als Antwort auf eine Abfrage zurückgegeben.   Typ 11 wird als Antwort auf einen neuen Dienstsuchtyp (Typ 11) zurückgegeben.

Nur Typ 3 kann in einer Garlic-Nachricht von Client zu Client gesendet werden.

### Format

Typen 3, 7 und 9 haben ein gemeinsames Format::

```text
Standard LS2 Header
- as defined below

Type-Specific Part
- as defined below in each part

Standard LS2 Signature:
- Length as implied by sig type of signing key
```
Standard-LS2-Header

Typspezifischer Teil

### Datenschutz-/Sicherheitsüberlegungen

Standard-LS2-Signatur:

## Standard-LS2-Header

Typ 5 (verschlüsselt) beginnt nicht mit einem Ziel und hat ein anderes Format. Siehe unten.

### Format

```
Standard LS2 Header:
  - Type (1 byte)
    Not actually in header, but part of data covered by signature.
    Take from field in Database Store Message.
  - Destination (387+ bytes)
  - Published timestamp (4 bytes, big endian, seconds since epoch, rolls over in 2106)
  - Expires (2 bytes, big endian) (offset from published timestamp in seconds, 18.2 hours max)
  - Flags (2 bytes)
    Bit order: 15 14 ... 3 2 1 0
    Bit 0: If 0, no offline keys; if 1, offline keys
    Bit 1: If 0, a standard published leaseset.
           If 1, an unpublished leaseset. Should not be flooded, published, or
           sent in response to a query. If this leaseset expires, do not query the
           netdb for a new one, unless bit 2 is set.
    Bit 2: If 0, a standard published leaseset.
           If 1, this unencrypted leaseset will be blinded and encrypted when published.
           If this leaseset expires, query the blinded location in the netdb for a new one.
           If this bit is set to 1, set bit 1 to 1 also.
           As of release 0.9.42.
    Bits 3-15: set to 0 for compatibility with future uses
  - If flag indicates offline keys, the offline signature section:
    Expires timestamp (4 bytes, big endian, seconds since epoch, rolls over in 2106)
    Transient sig type (2 bytes, big endian)
    Transient signing public key (length as implied by sig type)
    Signature of expires timestamp, transient sig type, and public key,
    by the destination public key,
    length as implied by destination public key sig type.
    This section can, and should, be generated offline.
```
### Begründung

  - wie unten definiert

  - wie unten in jedem Teil definiert

  - Länge wie durch Sig-Typ des Signaturschlüssels impliziert

- Nicht veröffentlicht/veröffentlicht: Zur Verwendung beim Senden einer Datenbank-Speicherung Ende-zu-Ende,
  kann der sendende Router angeben, dass dieses Leaseset nicht an andere gesendet werden soll. Derzeit verwenden wir Heuristiken, um diesen Zustand beizubehalten.

### Probleme

- Veröffentlicht: Ersetzt die komplexe Logik zur Bestimmung der „Version“ des Leasesets. Derzeit ist die Version das Ablaufdatum der am längsten laufenden Lease, und ein Router, der ein Leaseset veröffentlicht, das nur eine ältere Lease entfernt, muss dieses Ablaufdatum um mindestens 1 ms erhöhen.

- Ablauf: Ermöglicht, dass das Ablaufdatum eines NetDB-Eintrags früher ist als das der am längsten laufenden Leaseset. Für LS2 möglicherweise nicht nützlich, wo Leasesets mit maximal 11 Minuten Ablauf erwartet werden, aber für andere neue Typen notwendig (siehe Meta LS und Dienst-Eintrag unten).

- Offline-Schlüssel sind optional, um die anfängliche/erforderliche Implementierungskomplexität zu reduzieren.

### Hinweise

- Die Zeitstempelgenauigkeit könnte noch weiter reduziert werden (10 Minuten?), aber dann müsste eine Versionsnummer hinzugefügt werden. Dies könnte Multihoming brechen, es sei denn, wir haben ordnungserhaltende Verschlüsselung? Ohne Zeitstempel wahrscheinlich nicht machbar.

- Alternative: 3-Byte-Zeitstempel (Epoche / 10 Minuten), 1-Byte-Version, 2-Byte-Ablauf

- Ist der Typ explizit oder implizit in Daten/Signatur? „Domain“-Konstanten für Signatur?

## Neue DatabaseEntry-Typen

### LeaseSet 2

Typ 11 (Dienst-Liste) ist eine Aggregation mehrerer Dienst-Einträge und hat ein anderes Format. Siehe unten.

- Router sollten ein LS nicht öfter als einmal pro Sekunde veröffentlichen.  
  Wenn doch, müssen sie den Veröffentlichungszeitstempel künstlich um 1 gegenüber dem zuvor veröffentlichten LS erhöhen.

TBD

    Standard LS flag (1)
Typen 3, 7 und 9 verwenden den Standard-LS2-Header, wie unten spezifiziert:

    Standard LS2 type (3)
Änderungen gegenüber bestehendem LeaseSet:

    Hash of destination
    This hash is then used to generate the daily "routing key", as in LS1
Abfrage mit

    10 minutes, as in a regular LS.
Speichern mit

    Destination

### Format

```
Standard LS2 Header as specified above

  Standard LS2 Type-Specific Part
  - Properties (Mapping as specified in common structures spec, 2 zero bytes if none)
  - Number of key sections to follow (1 byte, max TBD)
  - Key sections:
    - Encryption type (2 bytes, big endian)
    - Encryption key length (2 bytes, big endian)
      This is explicit, so floodfills can parse LS2 with unknown encryption types.
    - Encryption key (number of bytes specified)
  - Number of lease2s (1 byte)
  - Lease2s (40 bytes each)
    These are leases, but with a 4-byte instead of an 8-byte expiration,
    seconds since the epoch (rolls over in 2106)

  Standard LS2 Signature:
  - Signature
    If flag indicates offline keys, this is signed by the transient pubkey,
    otherwise, by the destination pubkey
    Length as implied by sig type of signing key
    The signature is of everything above.
```
### Begründung

- Router-Implementierungen könnten die transienten Schlüssel und Signaturen zwischenspeichern,  
  um die Verifizierung bei jedem Zugriff zu vermeiden. Insbesondere Floodfills und Router an beiden Enden langlebiger Verbindungen könnten davon profitieren.

- Offline-Schlüssel und -signatur sind nur für langlebige Ziele geeignet,  
  d. h. Server, nicht Clients.

### Diskussion

Speichern unter

Typischer Ablauf

Veröffentlicht von

- Hinzufügen von Veröffentlichungszeitstempel, Ablaufzeitstempel, Flags und Eigenschaften
- Hinzufügen des Verschlüsselungstyps
- Entfernen des Widerrufschlüssels

Dieser Vorschlag verwendet weiterhin den öffentlichen Schlüssel im Leaseset als Ende-zu-Ende-Verschlüsselungsschlüssel und lässt das öffentliche Schlüsselfeld im Ziel ungenutzt, wie es derzeit ist. Der Verschlüsselungstyp ist nicht im Zertifikat des Ziel-Schlüssels angegeben, bleibt 0.

- Eigenschaften: Zukünftige Erweiterbarkeit und Flexibilität.  
  Zuerst platziert, falls zur Analyse der restlichen Daten erforderlich.

### Neue Verschlüsselungsprobleme

Eine abgelehnte Alternative ist, den Verschlüsselungstyp im Zertifikat des Ziel-Schlüssels anzugeben, den öffentlichen Schlüssel im Ziel zu verwenden und den öffentlichen Schlüssel im Leaseset nicht zu verwenden. Dies ist nicht geplant.

- Mehrere Verschlüsselungstyp-/öffentliche Schlüsselpaare  
  erleichtern den Übergang zu neuen Verschlüsselungstypen. Die andere Möglichkeit ist,  
  mehrere Leasesets zu veröffentlichen, möglicherweise mit denselben Tunneln,  
  wie wir es derzeit für DSA- und EdDSA-Ziele tun.  
  Die Identifizierung des eingehenden Verschlüsselungstyps auf einem Tunnel  
  kann mit dem bestehenden Session-Tag-Mechanismus erfolgen  
  und/oder durch Testentschlüsselung mit jedem Schlüssel. Die Länge der eingehenden  
  Nachrichten kann ebenfalls Hinweise geben.

- Der Ort des tatsächlichen öffentlichen Schlüssels ändert sich nicht.
- Verschlüsselungstyp oder öffentlicher Schlüssel können sich ändern, ohne das Ziel zu ändern.
- Entfernt das ungenutzte Widerruffeld
- Grundlegende Kompatibilität mit anderen DatabaseEntry-Typen in diesem Vorschlag
- Erlaubt mehrere Verschlüsselungstypen

- Der Ort des öffentlichen Schlüssels und des Verschlüsselungstyps unterscheidet sich von RouterInfo
- Behält den ungenutzten öffentlichen Schlüssel im Leaseset bei
- Erfordert Implementierung im gesamten Netzwerk; alternativ könnten experimentelle Verschlüsselungstypen verwendet werden, wenn von Floodfills erlaubt (siehe aber verwandte Vorschläge 136 und 137 zur Unterstützung experimenteller Sig-Typen). Der alternative Vorschlag könnte einfacher zu implementieren und testen sein für experimentelle Verschlüsselungstypen.

### Hinweise

- Der Verschlüsselungstyp repräsentiert die Kombination  
  aus Kurve, Schlüssellänge und Ende-zu-Ende-Schema,  
  einschließlich KDF und MAC, falls vorhanden.

- Wir haben ein Schlüssellängenfeld eingefügt, damit das LS2  
  vom Floodfill auch für unbekannte Verschlüsselungstypen  
  analysierbar und verifizierbar ist.

- Der erste neue Verschlüsselungstyp, der vorgeschlagen wird, wird  
  wahrscheinlich ECIES/X25519 sein. Wie es Ende-zu-Ende verwendet wird  
  (entweder eine leicht modifizierte Version von ElGamal/AES+SessionTag  
  oder etwas völlig Neues, z. B. ChaCha/Poly) wird in einem oder mehreren separaten Vorschlägen spezifiziert.  
  Siehe auch die ECIES-Vorschläge 144 und 145.

### Verschlüsseltes LS2

Vorteile von LS2:

- 8-Byte-Ablauf in Leases geändert zu 4 Bytes.

Nachteile von LS2:

Einiges davon ist für diesen Vorschlag außerhalb des Umfangs,   aber hier werden vorläufige Notizen gesammelt, da wir noch   keinen separaten Verschlüsselungsvorschlag haben.   Siehe auch die ECIES-Vorschläge 144 und 145.

- Falls wir jemals Widerruf implementieren, können wir dies mit einem Ablaufwert von Null tun, oder mit Null Leases, oder beidem. Kein separater Widerrufschlüssel erforderlich.

Ziele:

    Standard LS flag (1)
Verschlüsseltes LS2 wird niemals in einer Ende-zu-Ende-Garlic-Nachricht gesendet.   Verwenden Sie stattdessen das Standard-LS2 wie oben.

    Encrypted LS2 type (5)
Änderungen gegenüber bestehendem verschlüsseltem LeaseSet:

    Hash of blinded sig type and blinded public key
    Two byte sig type (big endian, e.g. 0x000b) || blinded public key
    This hash is then used to generate the daily "routing key", as in LS1
Abfrage mit

    10 minutes, as in a regular LS, or hours, as in a meta LS.
Speichern mit

    Destination


### Definitionen

Speichern unter

Typischer Ablauf

    n-byte output from a cryptographically-secure random number generator.

    In addition to the requirement of CSRNG being cryptographically-secure (and thus
    suitable for generating key material), it MUST be safe
    for some n-byte output to be used for key material when the byte sequences immediately
    preceding and following it are exposed on the network (such as in a salt, or encrypted
    padding). Implementations that rely on a potentially-untrustworthy source should hash
    any output that is to be exposed on the network. See [PRNG references](http://projectbullrun.org/dual-ec/ext-rand.html) and [Tor dev discussion](https://lists.torproject.org/pipermail/tor-dev/2015-November/009954.html).

Veröffentlicht von

    SHA-256 hash function that takes a personalization string p and data d, and
    produces an output of length 32 bytes.

    Use SHA-256 as follows::

        H(p, d) := SHA-256(p || d)

Wir definieren die folgenden Funktionen entsprechend den kryptografischen Bausteinen, die für verschlüsseltes LS2 verwendet werden:

    The ChaCha20 stream cipher as specified in [RFC 7539 Section 2.4](https://tools.ietf.org/html/rfc7539#section-2.4), with the initial counter
    set to 1. S_KEY_LEN = 32 and S_IV_LEN = 12.

    ENCRYPT(k, iv, plaintext)
        Encrypts plaintext using the cipher key k, and nonce iv which MUST be unique for
        the key k. Returns a ciphertext that is the same size as the plaintext.

        The entire ciphertext must be indistinguishable from random if the key is secret.

    DECRYPT(k, iv, ciphertext)
        Decrypts ciphertext using the cipher key k, and nonce iv. Returns the plaintext.


CSRNG(n)

    The RedDSA signature scheme (corresponding to SigType 11) with key blinding.
    It has the following functions:

    DERIVE_PUBLIC(privkey)
        Returns the public key corresponding to the given private key.

    SIGN(privkey, m)
        Returns a signature by the private key privkey over the given message m.

    VERIFY(pubkey, m, sig)
        Verifies the signature sig against the public key pubkey and message m. Returns
        true if the signature is valid, false otherwise.

    It must also support the following key blinding operations:

    GENERATE_ALPHA(data, secret)
        Generate alpha for those who know the data and an optional secret.
        The result must be identically distributed as the private keys.

    BLIND_PRIVKEY(privkey, alpha)
        Blinds a private key, using a secret alpha.

    BLIND_PUBKEY(pubkey, alpha)
        Blinds a public key, using a secret alpha.
        For a given keypair (privkey, pubkey) the following relationship holds::

            BLIND_PUBKEY(pubkey, alpha) ==
            DERIVE_PUBLIC(BLIND_PRIVKEY(privkey, alpha))

H(p, d)

    X25519 public key agreement system. Private keys of 32 bytes, public keys of 32
    bytes, produces outputs of 32 bytes. It has the following
    functions:

    GENERATE_PRIVATE()
        Generates a new private key.

    DERIVE_PUBLIC(privkey)
        Returns the public key corresponding to the given private key.

    DH(privkey, pubkey)
        Generates a shared secret from the given private and public keys.

STREAM

    A cryptographic key derivation function which takes some input key material ikm (which
    should have good entropy but is not required to be a uniformly random string), a salt
    of length 32 bytes, and a context-specific 'info' value, and produces an output
    of n bytes suitable for use as key material.

    Use HKDF as specified in [RFC 5869](https://tools.ietf.org/html/rfc5869), using the HMAC hash function SHA-256
    as specified in [RFC 2104](https://tools.ietf.org/html/rfc2104). This means that SALT_LEN is 32 bytes max.


### Format

SIG

- Verschlüsselungsschlüssel sind in der Reihenfolge der Serverpräferenz, am liebsten zuerst.  
  Standardverhalten des Clients ist, den ersten Schlüssel mit unterstütztem Verschlüsselungstyp auszuwählen.  
  Clients können andere Auswahlalgorithmen basierend auf Verschlüsselungsunterstützung, relativer Leistung und anderen Faktoren verwenden.

DH

    Layer 0 data + Enc(layer 1 data + Enc(layer 2 data)) + Signature

HKDF(salt, ikm, info, n)

Das verschlüsselte LS2-Format besteht aus drei verschachtelten Schichten:

#### Schicht 0 (äußerste)

Das Gesamtformat sieht wie folgt aus::

    1 byte

    Not actually in header, but part of data covered by signature.
    Take from field in Database Store Message.

Beachten Sie, dass verschlüsseltes LS2 verblendet ist. Das Ziel ist nicht im Header enthalten.   Der DHT-Speicherort ist SHA-256(Sig-Typ || verblendeter öffentlicher Schlüssel) und wird täglich rotiert.

    2 bytes, big endian
    This will always be type 11, identifying a Red25519 blinded key.

Verwendet NICHT den oben spezifizierten Standard-LS2-Header.

    Length as implied by sig type

Typ

    4 bytes, big endian

    Seconds since epoch, rolls over in 2106

Verblendeter öffentlicher Schlüssel-Sig-Typ

    2 bytes, big endian

    Offset from published timestamp in seconds, 18.2 hours max

Verblendeter öffentlicher Schlüssel

    2 bytes

    Bit order: 15 14 ... 3 2 1 0

    Bit 0: If 0, no offline keys; if 1, offline keys

    Other bits: set to 0 for compatibility with future uses

Veröffentlichungszeitstempel

    Present if flag indicates offline keys

    Expires timestamp
        4 bytes, big endian

        Seconds since epoch, rolls over in 2106

    Transient sig type
        2 bytes, big endian

    Transient signing public key
        Length as implied by sig type

    Signature
        Length as implied by blinded public key sig type

        Over expires timestamp, transient sig type, and transient public key.

        Verified with the blinded public key.

Ablauf

    2 bytes, big endian

Flags

    lenOuterCiphertext bytes

    Encrypted layer 1 data. See below for key derivation and encryption algorithms.

Transienter Schlüsseldaten

    Length as implied by sig type of the signing key used

    The signature is of everything above.

    If the flag indicates offline keys, the signature is verified with the transient
    public key. Otherwise, the signature is verified with the blinded public key.


#### Schicht 1 (mittlere)

lenOuterCiphertext

    1 byte
    
    Bit order: 76543210

    Bit 0: 0 for everybody, 1 for per-client, auth section to follow

    Bits 3-1: Authentication scheme, only if bit 0 is set to 1 for per-client, otherwise 000
              000: DH client authentication (or no per-client authentication)
              001: PSK client authentication

    Bits 7-4: Unused, set to 0 for future compatibility

outerCiphertext

    Present if flag bit 0 is set to 1 and flag bits 3-1 are set to 000.

    ephemeralPublicKey
        32 bytes

    clients
        2 bytes, big endian

        Number of authClient entries to follow, 40 bytes each

    authClient
        Authorization data for a single client.
        See below for the per-client authorization algorithm.

        clientID_i
            8 bytes

        clientCookie_i
            32 bytes

Signatur

    Present if flag bit 0 is set to 1 and flag bits 3-1 are set to 001.

    authSalt
        32 bytes

    clients
        2 bytes, big endian

        Number of authClient entries to follow, 40 bytes each

    authClient
        Authorization data for a single client.
        See below for the per-client authorization algorithm.

        clientID_i
            8 bytes

        clientCookie_i
            32 bytes


Flags

    Length implied by lenOuterCiphertext (whatever data remains)

    Encrypted layer 2 data. See below for key derivation and encryption algorithms.


#### Schicht 2 (innere)

DH-Client-Auth-Daten

    1 byte

    Either 3 (LS2) or 7 (Meta LS2)

PSK-Client-Auth-Daten

    LeaseSet2 data for the given type.

    Includes the header and signature.


### Blinding-Schlüsselableitung

innerCiphertext

Typ

#### Ziele

- Hinzufügen von Blinding
- Erlauben mehrerer Sig-Typen
- Keine neuen Kryptoprimitiva erforderlich
- Optional an jeden Empfänger verschlüsseln, widerrufbar
- Unterstützung der Verschlüsselung von Standard-LS2 und Meta-LS2 nur

#### Sicherheit

Daten

#### Definitionen

Wir verwenden das folgende Schema für die Schlüsselverblendung,   basierend auf Ed25519 und [ZCash RedDSA](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf).   Die Re25519-Signaturen erfolgen über die Ed25519-Kurve, unter Verwendung von SHA-512 für den Hash.

    The Ed25519 base point (generator) 2^255 - 19 as in [Ed25519](http://cr.yp.to/papers.html#ed25519)

Wir verwenden NICHT [Tor's rend-spec-v3.txt Anhang A.2](https://spec.torproject.org/rend-spec-v3),   das ähnliche Designziele hat, weil seine verblendeten öffentlichen Schlüssel   außerhalb der prim-Ordnungs-Untergruppe liegen könnten, mit unbekannten Sicherheitsimplikationen.

    The Ed25519 order 2^252 + 27742317777372353535851937790883648493
    as in [Ed25519](http://cr.yp.to/papers.html#ed25519)

Die Sicherheit eines Verblendungsschemas erfordert, dass die   Verteilung von alpha identisch mit der der unverblendeten privaten Schlüssel ist.   Wenn wir jedoch einen Ed25519-privaten Schlüssel (Sig-Typ 7)   zu einem Red25519-privaten Schlüssel (Sig-Typ 11) verblenden,   ist die Verteilung unterschiedlich. Um die Anforderungen von [zcash Abschnitt 4.1.6.1](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf) zu erfüllen,   sollte Red25519 (Sig-Typ 11) auch für die unverblendeten Schlüssel verwendet werden,   damit „die Kombination aus einem neu randomisierten öffentlichen Schlüssel und Signatur(en)   unter diesem Schlüssel den Schlüssel, von dem er neu randomisiert wurde, nicht offenbart“.   Wir erlauben Typ 7 für bestehende Ziele, empfehlen aber   Typ 11 für neue Ziele, die verschlüsselt werden sollen.

    Convert a private key to public, as in Ed25519 (mulitply by G)

B

    A 32-byte random number known to those who know the destination.

L

    Generate alpha for the current date, for those who know the destination and the secret.
    The result must be identically distributed as Ed25519 private keys.

DERIVE_PUBLIC(a)

    The unblinded 32-byte EdDSA or RedDSA signing private key used to sign the destination

alpha

    The unblinded 32-byte EdDSA or RedDSA signing public key in the destination,
    = DERIVE_PUBLIC(a), as in Ed25519

GENERATE_ALPHA(destination, date, secret)

    The blinded 32-byte EdDSA signing private key used to sign the encrypted leaseset
    This is a valid EdDSA private key.

a

    The blinded 32-byte EdDSA signing public key in the Destination,
    may be generated with DERIVE_PUBLIC(a'), or from A and alpha.
    This is a valid EdDSA public key, on the curve and on the prime-order subgroup.

A

    Flip the order of the input bytes to little-endian

a'

    32 bytes = (LEOS2IP(SHA512(x))) mod B, same as in Ed25519 hash-and-reduce


#### Verblendungsberechnungen

A'

LEOS2IP(x)

```text
// GENERATE_ALPHA(destination, date, secret)

  // secret is optional, else zero-length
  A = destination's signing public key
  stA = signature type of A, 2 bytes big endian (0x0007 or 0x000b)
  stA' = signature type of blinded public key A', 2 bytes big endian (0x000b)
  keydata = A || stA || stA'
  datestring = 8 bytes ASCII YYYYMMDD from the current date UTC
  secret = UTF-8 encoded string
  seed = HKDF(H("I2PGenerateAlpha", keydata), datestring || secret, "i2pblinding1", 64)
  // treat seed as a 64 byte little-endian value
  alpha = seed mod L
```
H*(x)

```text
// BLIND_PRIVKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  // If for a Ed25519 private key (type 7)
  seed = destination's signing private key
  a = left half of SHA512(seed) and clamped as usual for Ed25519
  // else, for a Red25519 private key (type 11)
  a = destination's signing private key
  // Addition using scalar arithmentic
  blinded signing private key = a' = BLIND_PRIVKEY(a, alpha) = (a + alpha) mod L
  blinded signing public key = A' = DERIVE_PUBLIC(a')
```
Ein neues Geheimnis alpha und verblendete Schlüssel müssen täglich (UTC) neu generiert werden.   Das Geheimnis alpha und die verblendeten Schlüssel werden wie folgt berechnet.

```text
// BLIND_PUBKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  A = destination's signing public key
  // Addition using group elements (points on the curve)
  blinded public key = A' = BLIND_PUBKEY(A, alpha) = A + DERIVE_PUBLIC(alpha)
```
GENERATE_ALPHA(destination, date, secret), für alle Parteien:

#### Signieren

BLIND_PRIVKEY(), für den Eigentümer, der das Leaseset veröffentlicht:

BLIND_PUBKEY(), für die Clients, die das Leaseset abrufen:

Beide Methoden zur Berechnung von A' liefern das gleiche Ergebnis, wie erforderlich.

Das unverblendete Leaseset wird vom unverblendeten Ed25519- oder Red25519-Signatur-privaten Schlüssel signiert und mit dem unverblendeten Ed25519- oder Red25519-Signatur-öffentlichen Schlüssel (Sig-Typen 7 oder 11) wie üblich verifiziert.

#### Signier-/Verifizierungsberechnungen

Wenn der Signatur-öffentliche Schlüssel offline ist,   wird das unverblendete Leaseset vom unverblendeten transienten Ed25519- oder Red25519-Signatur-privaten Schlüssel signiert   und mit dem unverblendeten Ed25519- oder Red25519-transienten öffentlichen Signaturschlüssel (Sig-Typen 7 oder 11) wie üblich verifiziert.   Siehe unten für zusätzliche Hinweise zu Offline-Schlüsseln für verschlüsselte Leasesets.

Zum Signieren des verschlüsselten Leasesets verwenden wir Red25519, basierend auf [RedDSA](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf),   um mit verblendeten Schlüsseln zu signieren und zu verifizieren.   Die Red25519-Signaturen erfolgen über die Ed25519-Kurve, unter Verwendung von SHA-512 für den Hash.

Red25519 ist identisch mit Standard-Ed25519, außer wie unten spezifiziert.

Der äußere Teil des verschlüsselten Leasesets verwendet Red25519-Schlüssel und -Signaturen.

Red25519 ist fast identisch mit Ed25519. Es gibt zwei Unterschiede:

```text
T = 80 random bytes
  r = H*(T || publickey || message)
  // rest is the same as in Ed25519
```
Red25519-privatschlüssel werden aus Zufallszahlen generiert und müssen dann mod L reduziert werden, wobei L wie oben definiert ist.   Ed25519-privatschlüssel werden aus Zufallszahlen generiert und dann „geklemmt“ unter Verwendung von   bitweiser Maskierung für Bytes 0 und 31. Dies wird für Red25519 nicht gemacht.   Die Funktionen GENERATE_ALPHA() und BLIND_PRIVKEY() oben generieren korrekte   Red25519-privatschlüssel unter Verwendung von mod L.

```text
// same as in Ed25519
```
### Verschlüsselung und Verarbeitung

#### Ableitung von Subcredentials

In Red25519 verwendet die Berechnung von r für die Signatur zusätzliche Zufallsdaten   und verwendet den öffentlichen Schlüsselwert statt des Hashes des privaten Schlüssels.   Aufgrund der Zufallsdaten ist jede Red25519-Signatur unterschiedlich, selbst   wenn dieselben Daten mit demselben Schlüssel signiert werden.

```text
A = destination's signing public key
  stA = signature type of A, 2 bytes big endian (0x0007 or 0x000b)
  stA' = signature type of A', 2 bytes big endian (0x000b)
  keydata = A || stA || stA'
  credential = H("credential", keydata)
```
Signieren:

Verifizieren:

```text
subcredential = H("subcredential", credential || blindedPublicKey)
```
Als Teil des Verblendungsprozesses müssen wir sicherstellen, dass ein verschlüsseltes LS2 nur von jemandem entschlüsselt werden kann, der den entsprechenden Signatur-öffentlichen Schlüssel des Ziels kennt. Das vollständige Ziel ist nicht erforderlich.   Um dies zu erreichen, leiten wir ein Credential vom Signatur-öffentlichen Schlüssel ab:

#### Verschlüsselung der Schicht 1

Die Personalisierungszeichenfolge stellt sicher, dass das Credential nicht mit einem Hash kollidiert, der als DHT-Suchschlüssel verwendet wird, wie z. B. der reine Ziel-Hash.

```text
outerInput = subcredential || publishedTimestamp
```
Für einen gegebenen verblendeten Schlüssel können wir dann ein Subcredential ableiten:

```text
outerSalt = CSRNG(32)
```
Das Subcredential ist in den unten beschriebenen Schlüsselableitungsprozessen enthalten, was diese Schlüssel an das Wissen des Signatur-öffentlichen Schlüssels des Ziels bindet.

```text
keys = HKDF(outerSalt, outerInput, "ELS2_L1K", 44)
  outerKey = keys[0:31]
  outerIV = keys[32:43]
```
Zuerst wird die Eingabe für den Schlüsselableitungsprozess vorbereitet:

```text
outerCiphertext = outerSalt || ENCRYPT(outerKey, outerIV, outerPlaintext)
```
#### Entschlüsselung der Schicht 1

Als Nächstes wird ein zufälliger Salt generiert:

```text
outerSalt = outerCiphertext[0:31]
```
Dann wird der Schlüssel abgeleitet, der zum Verschlüsseln der Schicht 1 verwendet wird:

```text
outerInput = subcredential || publishedTimestamp
  keys = HKDF(outerSalt, outerInput, "ELS2_L1K", 44)
  outerKey = keys[0:31]
  outerIV = keys[32:43]
```
Schließlich wird der Klartext der Schicht 1 verschlüsselt und serialisiert:

```text
outerPlaintext = DECRYPT(outerKey, outerIV, outerCiphertext[32:end])
```
#### Verschlüsselung der Schicht 2

Der Salt wird aus dem Geheimtext der Schicht 1 geparst:

Dann wird der Schlüssel abgeleitet, der zum Verschlüsseln der Schicht 1 verwendet wurde:

```text
innerInput = authCookie || subcredential || publishedTimestamp
  innerSalt = CSRNG(32)
  keys = HKDF(innerSalt, innerInput, "ELS2_L2K", 44)
  innerKey = keys[0:31]
  innerIV = keys[32:43]
  innerCiphertext = innerSalt || ENCRYPT(innerKey, innerIV, innerPlaintext)
```
#### Entschlüsselung der Schicht 2

Schließlich wird der Geheimtext der Schicht 1 entschlüsselt:

Wenn Client-Autorisierung aktiviert ist, wird ``authCookie`` wie unten beschrieben berechnet.   Wenn Client-Autorisierung deaktiviert ist, ist ``authCookie`` das null-längige Byte-Array.

```text
innerInput = authCookie || subcredential || publishedTimestamp
  innerSalt = innerCiphertext[0:31]
  keys = HKDF(innerSalt, innerInput, "ELS2_L2K", 44)
  innerKey = keys[0:31]
  innerIV = keys[32:43]
  innerPlaintext = DECRYPT(innerKey, innerIV, innerCiphertext[32:end])
```
### Pro-Client-Autorisierung

Die Verschlüsselung erfolgt ähnlich wie bei Schicht 1:

Wenn Client-Autorisierung aktiviert ist, wird ``authCookie`` wie unten beschrieben berechnet.   Wenn Client-Autorisierung deaktiviert ist, ist ``authCookie`` das null-längige Byte-Array.

#### DH-Client-Autorisierung

Die Entschlüsselung erfolgt ähnlich wie bei Schicht 1:

Wenn Client-Autorisierung für ein Ziel aktiviert ist, verwaltet der Server eine Liste von Clients, die autorisiert sind, die verschlüsselten LS2-Daten zu entschlüsseln. Die pro Client gespeicherten Daten hängen vom Autorisierungsmechanismus ab und enthalten eine Form von Schlüsselmaterial, das jeder Client generiert und über einen sicheren Out-of-Band-Mechanismus an den Server sendet.

```text
authCookie = CSRNG(32)
  esk = GENERATE_PRIVATE()
  epk = DERIVE_PUBLIC(esk)
```
Es gibt zwei Alternativen zur Implementierung der pro-Client-Autorisierung:

```text
sharedSecret = DH(esk, cpk_i)
  authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
  okm = HKDF(epk, authInput, "ELS2_XCA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
  clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
```
Jeder Client generiert ein DH-Schlüsselpaar ``[csk_i, cpk_i]`` und sendet den öffentlichen Schlüssel ``cpk_i`` an den Server.

Serververarbeitung ^^^^^^^^^^^^^^^^^ Der Server generiert ein neues ``authCookie`` und ein temporäres DH-Schlüsselpaar:

```text
sharedSecret = DH(csk_i, epk)
  authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
  okm = HKDF(epk, authInput, "ELS2_XCA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
```
Dann verschlüsselt der Server für jeden autorisierten Client das ``authCookie`` mit dessen öffentlichem Schlüssel:

```text
authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie_i)
```
#### Vorabgeteilter-Schlüssel-Client-Autorisierung

Der Server platziert jedes ``[clientID_i, clientCookie_i]``-Tupel in Schicht 1 des verschlüsselten LS2 zusammen mit ``epk``.

Clientverarbeitung ^^^^^^^^^^^^^^^^^ Der Client verwendet seinen privaten Schlüssel, um seinen erwarteten Client-Bezeichner ``clientID_i``, Verschlüsselungsschlüssel ``clientKey_i`` und Verschlüsselungs-IV ``clientIV_i`` abzuleiten:

```text
authCookie = CSRNG(32)
  authSalt = CSRNG(32)
```
Dann sucht der Client in den Autorisierungsdaten der Schicht 1 nach einem Eintrag, der ``clientID_i`` enthält. Wenn ein passender Eintrag existiert, entschlüsselt der Client ihn, um ``authCookie`` zu erhalten:

```text
authInput = psk_i || subcredential || publishedTimestamp
  okm = HKDF(authSalt, authInput, "ELS2PSKA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
  clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
```
Jeder Client generiert einen geheimen 32-Byte-Schlüssel ``psk_i`` und sendet ihn an den Server. Alternativ kann der Server den geheimen Schlüssel generieren und an einen oder mehrere Clients senden.

Serververarbeitung ^^^^^^^^^^^^^^^^^ Der Server generiert ein neues ``authCookie`` und einen Salt:

```text
authInput = psk_i || subcredential || publishedTimestamp
  okm = HKDF(authSalt, authInput, "ELS2PSKA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
```
Dann verschlüsselt der Server für jeden autorisierten Client das ``authCookie`` mit dessen vorabgeteiltem Schlüssel:

```text
authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie_i)
```
#### Sicherheitsüberlegungen

Der Server platziert jedes ``[clientID_i, clientCookie_i]``-Tupel in Schicht 1 des verschlüsselten LS2 zusammen mit ``authSalt``.

Clientverarbeitung ^^^^^^^^^^^^^^^^^ Der Client verwendet seinen vorabgeteilten Schlüssel, um seinen erwarteten Client-Bezeichner ``clientID_i``, Verschlüsselungsschlüssel ``clientKey_i`` und Verschlüsselungs-IV ``clientIV_i`` abzuleiten:

Dann sucht der Client in den Autorisierungsdaten der Schicht 1 nach einem Eintrag, der ``clientID_i`` enthält. Wenn ein passender Eintrag existiert, entschlüsselt der Client ihn, um ``authCookie`` zu erhalten:

Beide oben genannten Client-Autorisierungsmechanismen bieten Privatsphäre für die Client-Mitgliedschaft. Eine Entität, die nur das Ziel kennt, kann sehen, wie viele Clients zu einem Zeitpunkt abonniert sind, kann aber nicht verfolgen, welche Clients hinzugefügt oder widerrufen werden.

- Alles aus Sicherheitsgründen verschlüsseln
- Sicher verschlüsseln, nicht nur mit AES
- An jeden Empfänger verschlüsseln

Server SOLLTEN die Reihenfolge der Clients bei jeder Generierung eines verschlüsselten LS2 zufällig machen, um zu verhindern, dass Clients ihre Position in der Liste erfahren und ableiten, wann andere Clients hinzugefügt oder widerrufen wurden.

- Eine äußere Schicht, die die notwendigen Klartextinformationen für Speicherung und Abruf enthält.
- Eine mittlere Schicht, die die Client-Authentifizierung behandelt.
- Eine innere Schicht, die die eigentlichen LS2-Daten enthält.

Ein Server KANN wählen, die Anzahl der abonnierten Clients zu verbergen, indem er zufällige Einträge in die Liste der Autorisierungsdaten einfügt.

- Der Signierungs-öffentliche Schlüssel im unverblendeten Ziel muss  
  Ed25519 (Sig-Typ 7) oder Red25519 (Sig-Typ 11) sein;  
  keine anderen Sig-Typen werden unterstützt
- Wenn der Signierungs-öffentliche Schlüssel offline ist, muss auch der transiente öffentliche Signaturschlüssel Ed25519 sein
- Verblendung ist rechnerisch einfach
- Verwendung bestehender kryptografischer Primitiva
- Verblendete öffentliche Schlüssel können nicht entblendet werden
- Verblendete öffentliche Schlüssel müssen auf der Ed25519-Kurve und der prim-Ordnungs-Untergruppe liegen
- Es muss der Signierungs-öffentliche Schlüssel des Ziels bekannt sein  
  (vollständiges Ziel nicht erforderlich), um den verblendeten öffentlichen Schlüssel abzuleiten
- Optional kann ein zusätzliches Geheimnis bereitgestellt werden, das zum Ableiten des verblendeten öffentlichen Schlüssels erforderlich ist

Vorteile der DH-Client-Autorisierung ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Die Sicherheit des Schemas hängt nicht ausschließlich vom Out-of-Band-Austausch des Client-Schlüsselmaterials ab. Der private Schlüssel des Clients muss niemals sein Gerät verlassen, und daher kann ein Angreifer, der den Out-of-Band-Austausch abfangen kann, aber den DH-Algorithmus nicht brechen kann, das verschlüsselte LS2 nicht entschlüsseln oder bestimmen, wie lange dem Client Zugriff gewährt wird.

### Verschlüsseltes LS mit Base 32-Adressen

Nachteile der DH-Client-Autorisierung ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Vorteile der PSK-Client-Autorisierung ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

### Verschlüsseltes LS mit Offline-Schlüsseln

Nachteile der PSK-Client-Autorisierung ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Siehe Vorschlag 149.

Sie können kein verschlüsseltes LS2 für BitTorrent verwenden, wegen der kompakten Ankündigung-Antworten, die 32 Bytes sind.   Die 32 Bytes enthalten nur den Hash. Es ist kein Platz für eine Angabe, dass das Leaseset verschlüsselt ist, oder für die Signaturtypen.

### Hinweise

- Erfordert N + 1 DH-Operationen auf der Serverseite für N Clients.
- Erfordert eine DH-Operation auf der Clientseite.
- Erfordert, dass der Client den geheimen Schlüssel generiert.

- Erfordert keine DH-Operationen.
- Ermöglicht dem Server, den geheimen Schlüssel zu generieren.
- Ermöglicht dem Server, denselben Schlüssel mit mehreren Clients zu teilen, wenn gewünscht.

- Die Sicherheit des Schemas hängt kritisch vom Out-of-Band-Austausch des Client-Schlüsselmaterials ab. Ein Angreifer, der den Austausch für einen bestimmten Client abfängt, kann jedes nachfolgende verschlüsselte LS2 entschlüsseln, für das dieser Client autorisiert ist, sowie bestimmen, wann der Zugriff des Clients widerrufen wird.

- Ein Dienst, der verschlüsselte Leasesets verwendet, würde die verschlüsselte Version an die Floodfills veröffentlichen. Aus Effizienzgründen würde er jedoch unverschlüsselte Leasesets an Clients in der umhüllten Garlic-Nachricht senden, sobald authentifiziert (z. B. über eine Whitelist).

- Floodfills können die maximale Größe auf einen vernünftigen Wert begrenzen, um Missbrauch zu verhindern.

### Meta LS2

Für verschlüsselte Leasesets mit Offline-Schlüsseln müssen auch die verblendeten privaten Schlüssel offline generiert werden, einer für jeden Tag.

Da der optionale Offline-Signaturblock im Klartextteil des verschlüsselten Leasesets ist, könnte jemand, der Floodfills durchsucht, dies verwenden, um das Leaseset (aber nicht zu entschlüsseln) über mehrere Tage zu verfolgen.   Um dies zu verhindern, sollte der Eigentümer der Schlüssel auch neue transiente Schlüssel für jeden Tag generieren.   Sowohl die transienten als auch die verblendeten Schlüssel können im Voraus generiert und dem Router in einem Batch zur Verfügung gestellt werden.

Es ist in diesem Vorschlag kein Dateiformat definiert, um mehrere transiente und verblendete Schlüssel zu verpacken und dem Client oder Router zur Verfügung zu stellen.   Es ist in diesem Vorschlag keine I2CP-Protokollerweiterung definiert, um verschlüsselte Leasesets mit Offline-Schlüsseln zu unterstützen.

Dies wird verwendet, um Multihoming zu ersetzen. Wie jedes Leaseset wird dies vom Ersteller signiert. Dies ist eine authentifizierte Liste von Ziel-Hashes.

Das Meta LS2 ist die Spitze und möglicherweise Zwischenknoten einer Baumstruktur.   Es enthält eine Anzahl von Einträgen, die jeweils auf ein LS, LS2 oder ein anderes Meta LS2 verweisen, um massives Multihoming zu unterstützen.   Ein Meta LS2 kann eine Mischung aus LS-, LS2- und Meta-LS2-Einträgen enthalten.   Die Blätter des Baums sind immer ein LS oder LS2.   Der Baum ist ein DAG; Schleifen sind verboten; Clients, die Suchen durchführen, müssen Schleifen erkennen und deren Folge verweigern.

Ein Meta LS2 kann eine viel längere Ablaufzeit als ein Standard-LS oder LS2 haben.   Die oberste Ebene kann eine Ablaufzeit mehrere Stunden nach dem Veröffentlichungsdatum haben.   Die maximale Ablaufzeit wird von Floodfills und Clients durchgesetzt und ist TBD.

Der Anwendungsfall für Meta LS2 ist massives Multihoming, aber ohne mehr Schutz vor Korrelation von Routern zu Leasesets (beim Neustart des Routers) als derzeit mit LS oder LS2 bereitgestellt wird.   Dies entspricht dem „Facebook“-Anwendungsfall, der wahrscheinlich keinen Korrelationsschutz benötigt. Dieser Anwendungsfall benötigt wahrscheinlich Offline-Schlüssel, die im Standard-Header an jedem Knoten des Baums bereitgestellt werden.

Das Backend-Protokoll zur Koordination zwischen den Blattroutern, Zwischen- und Master-Meta-LS-Unterzeichnern ist hier nicht spezifiziert. Die Anforderungen sind extrem einfach – nur prüfen, ob der Peer online ist, und alle paar Stunden ein neues LS veröffentlichen. Die einzige Komplexität besteht darin, neue Publisher für die Meta-LS auf oberster oder Zwischenebene bei Ausfall auszuwählen.

Misch-und-Match-Leasesets, bei denen Leases von mehreren Routern kombiniert, signiert und in einem einzigen Leaseset veröffentlicht werden, sind im Vorschlag 140, „unsichtbares Multihoming“, dokumentiert.   Dieser Vorschlag ist so, wie er geschrieben ist, nicht durchführbar, weil Streaming-Verbindungen nicht „sticky“ zu einem einzelnen Router wären, siehe http://zzz.i2p/topics/2335 .

Das Backend-Protokoll und die Interaktion mit Router- und Client-Internas wäre für unsichtbares Multihoming sehr komplex.

    Standard LS flag (1)
Um Überlastung des Floodfills für das Meta-LS auf oberster Ebene zu vermeiden, sollte die Ablaufzeit mindestens mehrere Stunden betragen. Clients müssen das Meta-LS auf oberster Ebene zwischenspeichern und es bei Nichtablauf über Neustarts hinweg beibehalten.

    Meta LS2 type (7)
Wir müssen einen Algorithmus definieren, damit Clients den Baum durchlaufen, einschließlich Fallbacks, damit die Nutzung verteilt ist. Eine Funktion von Hash-Abstand, Kosten und Zufälligkeit. Wenn ein Knoten sowohl LS oder LS2 als auch Meta LS hat, müssen wir wissen, wann diese Leasesets verwendet werden dürfen und wann der Baum weiter durchlaufen werden muss.

    Hash of destination
    This hash is then used to generate the daily "routing key", as in LS1
Abfrage mit

    Hours. Max 18.2 hours (65535 seconds)
Speichern mit

    "master" Destination or coordinator, or intermediate coordinators

### Format

```
Standard LS2 Header as specified above

  Meta LS2 Type-Specific Part
  - Properties (Mapping as specified in common structures spec, 2 zero bytes if none)
  - Number of entries (1 byte) Maximum TBD
  - Entries. Each entry contains: (40 bytes)
    - Hash (32 bytes)
    - Flags (2 bytes)
      TBD. Set all to zero for compatibility with future uses.
    - Type (1 byte) The type of LS it is referencing;
      1 for LS, 3 for LS2, 5 for encrypted, 7 for meta, 0 for unknown.
    - Cost (priority) (1 byte)
    - Expires (4 bytes) (4 bytes, big endian, seconds since epoch, rolls over in 2106)
  - Number of revocations (1 byte) Maximum TBD
  - Revocations: Each revocation contains: (32 bytes)
    - Hash (32 bytes)

  Standard LS2 Signature:
  - Signature (40+ bytes)
    The signature is of everything above.
```
Speichern unter

### Hinweise

- Nach der Entschlüsselung sollten mehrere Prüfungen durchgeführt werden, einschließlich, dass der innere Zeitstempel und Ablauf mit denen auf der obersten Ebene übereinstimmen.

- ChaCha20 wurde gegenüber AES ausgewählt. Während die Geschwindigkeiten ähnlich sind, wenn AES-Hardwareunterstützung verfügbar ist, ist ChaCha20 2,5-3x schneller, wenn keine AES-Hardwareunterstützung verfügbar ist, wie z. B. auf Low-End-ARM-Geräten.

- Wir kümmern uns nicht genug um Geschwindigkeit, um BLAKE2b mit Schlüssel zu verwenden. Es hat eine Ausgabegröße, die groß genug ist, um die größte n zu akkommodieren, die wir benötigen (oder wir können es einmal pro gewünschten Schlüssel mit einem Zählerargument aufrufen). BLAKE2b ist viel schneller als SHA-256, und BLAKE2b mit Schlüssel würde die Gesamtanzahl der Hashfunktionsaufrufe reduzieren. Allerdings siehe Vorschlag 148, wo vorgeschlagen wird, dass wir aus anderen Gründen zu BLAKE2b wechseln. Siehe [Secure key derivation performance](https://www.lvh.io/posts/secure-key-derivation-performance.html).

### Dienst-Eintrag

Typischer Ablauf

Veröffentlicht von

Flags und Eigenschaften: für zukünftige Verwendung

    n/a, see Service List
Dies ist ein einzelner Eintrag, der besagt, dass ein Ziel an einem Dienst teilnimmt. Er wird vom Teilnehmer an den Floodfill gesendet. Er wird niemals einzeln von einem Floodfill gesendet, sondern nur als Teil einer Dienst-Liste. Der Dienst-Eintrag wird auch verwendet, um die Teilnahme an einem Dienst zu widerrufen, indem der Ablauf auf Null gesetzt wird.

    Service Record type (9)
Dies ist kein LS2, aber es verwendet das Standard-LS2-Header- und Signaturformat.

    Hash of service name
    This hash is then used to generate the daily "routing key", as in LS1
Abfrage mit

    Hours. Max 18.2 hours (65535 seconds)
Speichern mit

    Destination

### Format

```
Standard LS2 Header as specified above

  Service Record Type-Specific Part
  - Port (2 bytes, big endian) (0 if unspecified)
  - Hash of service name (32 bytes)

  Standard LS2 Signature:
  - Signature (40+ bytes)
    The signature is of everything above.
```
### Hinweise

- Ein verteilter Dienst, der dies verwendet, hätte einen oder mehrere „Master“ mit dem privaten Schlüssel des Dienstziels. Sie würden (außerhalb des Bandes) die aktuelle Liste der aktiven Ziele bestimmen und das Meta LS2 veröffentlichen. Zur Redundanz könnten mehrere Master das Meta LS2 multihomen (d. h. gleichzeitig veröffentlichen).

- Ein verteilter Dienst könnte mit einem einzelnen Ziel beginnen oder altes Multihoming verwenden und dann zu einem Meta LS2 übergehen. Eine Standard-LS-Abfrage könnte jedes der LS, LS2 oder Meta LS2 zurückgeben.

- Wenn ein Dienst ein Meta LS2 verwendet, hat er keine Tunnel (Leases).

### Dienst-Liste

Speichern unter

Typischer Ablauf

Veröffentlicht von

Dies ähnelt keinem LS2 und verwendet ein anderes Format.

Die Dienst-Liste wird vom Floodfill erstellt und signiert. Sie ist nicht authentifiziert, da jeder durch Veröffentlichung eines Dienst-Eintr

TBD

    Service List lookup type (11)
Typen 3, 7 und 9 verwenden den Standard-LS2-Header, wie unten spezifiziert:

    Service List type (11)
Änderungen gegenüber bestehendem LeaseSet:

    Hash of service name
    This hash is then used to generate the daily "routing key", as in LS1
Abfrage mit

    Hours, not specified in the list itself, up to local policy
Speichern mit

    Nobody, never sent to floodfill, never flooded.

### Format

Das verschlüsselte LS2-Format besteht aus drei verschachtelten Schichten:

```
- Type (1 byte)
    Not actually in header, but part of data covered by signature.
    Take from field in Database Store Message.
  - Hash of the service name (implicit, in the Database Store message)
  - Hash of the Creator (floodfill) (32 bytes)
  - Published timestamp (8 bytes, big endian)

  - Number of Short Service Records (1 byte)
  - List of Short Service Records:
    Each Short Service Record contains (90+ bytes)
    - Dest hash (32 bytes)
    - Published timestamp (8 bytes, big endian)
    - Expires (4 bytes, big endian) (offset from published in ms)
    - Flags (2 bytes)
    - Port (2 bytes, big endian)
    - Sig length (2 bytes, big endian)
    - Signature of dest (40+ bytes)

  - Number of Revocation Records (1 byte)
  - List of Revocation Records:
    Each Revocation Record contains (86+ bytes)
    - Dest hash (32 bytes)
    - Published timestamp (8 bytes, big endian)
    - Flags (2 bytes)
    - Port (2 bytes, big endian)
    - Sig length (2 bytes, big endian)
    - Signature of dest (40+ bytes)

  - Signature of floodfill (40+ bytes)
    The signature is of everything above.
```
Zum Verifizieren der Signatur der Service List:

- Wenn Ablauf alle Nullen ist, sollte der Floodfill den Eintrag widerrufen und ihn nicht länger in der Dienst-Liste enthalten.

Um die Signatur jedes Short Service Record zu überprüfen:

- Speicherung: Der Floodfill kann die Speicherung dieser Einträge streng drosseln und die Anzahl der gespeicherten Einträge pro Hash und deren Ablauf begrenzen. Eine Whitelist von Hashes kann ebenfalls verwendet werden.

Um die Signatur jedes Revocation Record zu verifizieren:

- Jeder andere NetDB-Typ am selben Hash hat Priorität, daher kann ein Dienst-Eintrag niemals ein LS/RI überschreiben, aber ein LS/RI wird alle Dienst-Einträge an diesem Hash überschreiben.

### Hinweise

- Wir verwenden die Signaturlänge anstelle des Signaturtyps, damit wir unbekannte Signaturtypen unterstützen können.

- Für eine Dienstliste gibt es kein Ablaufdatum; Empfänger können anhand ihrer Richtlinien oder des Ablaufs der einzelnen Einträge selbst entscheiden.

- Service Lists werden nicht geflutet, sondern nur einzelne Service Records. Jeder floodfill erstellt, signiert und cached eine Service List. Der floodfill verwendet seine eigene Policy für die Cache-Zeit und die maximale Anzahl an Service- und Revocation Records.

## Erforderliche Änderungen an der Common-Structures-Spezifikation

### Schlüsselzertifikate

Nicht Bestandteil dieses Vorschlags. Zu den ECIES-Vorschlägen 144 und 145 hinzufügen.

### Neue Zwischenstrukturen

Neue Strukturen für Lease2, MetaLease, LeaseSet2Header und OfflineSignature hinzufügen. Wirksam ab Version 0.9.38.

### Neue NetDB-Typen

Strukturen für jeden neuen leaseset-Typ hinzufügen, übernommen aus dem Obigen. Für LeaseSet2, EncryptedLeaseSet und MetaLeaseSet gilt dies ab Release 0.9.38. Service Record und Service List sind vorläufig und ohne festen Termin.

### Neuer Signaturtyp

RedDSA_SHA512_Ed25519 Typ 11 hinzufügen. Der öffentliche Schlüssel ist 32 Bytes; der private Schlüssel ist 32 Bytes; der Hash ist 64 Bytes; die Signatur ist 64 Bytes.

## Erforderliche Änderungen an der Verschlüsselungsspezifikation

Nicht Gegenstand dieses Vorschlags. Siehe Vorschläge 144 und 145.

## Erforderliche I2NP-Änderungen

Hinweis hinzufügen: LS2 kann nur auf floodfills mit einer Mindestversion veröffentlicht werden.

### Datenbank-Lookup-Nachricht

Fügen Sie den Lookup-Typ für die Dienstliste hinzu.

### Änderungen

```
Flags byte: Lookup type field, currently bits 3-2, expands to bits 4-2.
  Lookup type 0x04 is defined as the service list lookup.

  Add note: Service list loookup may only be sent to floodfills with a minimum version.
  Minimum version is 0.9.38.
```
### Datenbank-Speichernachricht

Fügen Sie alle neuen Store-Typen hinzu.

### Änderungen

```
Type byte: Type field, currently bit 0, expands to bits 3-0.
  Type 3 is defined as a LS2 store.
  Type 5 is defined as a encrypted LS2 store.
  Type 7 is defined as a meta LS2 store.
  Type 9 is defined as a service record store.
  Type 11 is defined as a service list store.
  Other types are undefined and invalid.

  Add note: All new types may only be published to floodfills with a minimum version.
  Minimum version is 0.9.38.
```
## Erforderliche I2CP-Änderungen

### I2CP-Optionen

Neue Optionen, router-seitig interpretiert, im SessionConfig-Mapping gesendet:

```

  i2cp.leaseSetType=nnn       The type of leaseset to be sent in the Create Leaseset Message
                              Value is the same as the netdb store type in the table above.
                              Interpreted client-side, but also passed to the router in the
                              SessionConfig, to declare intent and check support.

  i2cp.leaseSetEncType=nnn[,nnn]  The encryption types to be used.
                                  Interpreted client-side, but also passed to the router in
                                  the SessionConfig, to declare intent and check support.
                                  See proposals 144 and 145.

  i2cp.leaseSetOfflineExpiration=nnn  The expiration of the offline signature, ASCII,
                                      seconds since the epoch.

  i2cp.leaseSetTransientPublicKey=[type:]b64  The base 64 of the transient private key,
                                              prefixed by an optional sig type number
                                              or name, default DSA_SHA1.
                                              Length as inferred from the sig type

  i2cp.leaseSetOfflineSignature=b64   The base 64 of the offline signature.
                                      Length as inferred from the destination
                                      signing public key type

  i2cp.leaseSetSecret=b64     The base 64 of a secret used to blind the
                              address of the leaseset, default ""

  i2cp.leaseSetAuthType=nnn   The type of authentication for encrypted LS2.
                              0 for no per-client authentication (the default)
                              1 for DH per-client authentication
                              2 for PSK per-client authentication

  i2cp.leaseSetPrivKey=b64    A base 64 private key for the router to use to
                              decrypt the encrypted LS2,
                              only if per-client authentication is enabled
```
Neue Optionen, die clientseitig interpretiert werden:

```

  i2cp.leaseSetType=nnn     The type of leaseset to be sent in the Create Leaseset Message
                            Value is the same as the netdb store type in the table above.
                            Interpreted client-side, but also passed to the router in the
                            SessionConfig, to declare intent and check support.

  i2cp.leaseSetEncType=nnn[,nnn]  The encryption types to be used.
                                  Interpreted client-side, but also passed to the router in
                                  the SessionConfig, to declare intent and check support.
                                  See proposals 144 and 145.

  i2cp.leaseSetSecret=b64     The base 64 of a secret used to blind the
                              address of the leaseset, default ""

  i2cp.leaseSetAuthType=nnn       The type of authentication for encrypted LS2.
                                  0 for no per-client authentication (the default)
                                  1 for DH per-client authentication
                                  2 for PSK per-client authentication

  i2cp.leaseSetBlindedType=nnn   The sig type of the blinded key for encrypted LS2.
                                 Default depends on the destination sig type.

  i2cp.leaseSetClient.dh.nnn=b64name:b64pubkey   The base 64 of the client name (ignored, UI use only),
                                                 followed by a ':', followed by the base 64 of the public
                                                 key to use for DH per-client auth. nnn starts with 0

  i2cp.leaseSetClient.psk.nnn=b64name:b64privkey   The base 64 of the client name (ignored, UI use only),
                                                   followed by a ':', followed by the base 64 of the private
                                                   key to use for PSK per-client auth. nnn starts with 0
```
### Session-Konfiguration

Beachten Sie, dass für Offline-Signaturen die Optionen i2cp.leaseSetOfflineExpiration, i2cp.leaseSetTransientPublicKey und i2cp.leaseSetOfflineSignature erforderlich sind und die Signatur mit dem transienten privaten Signaturschlüssel erfolgt.

### LeaseSet-Anfrage-Nachricht

Router zu Client. Keine Änderungen. Die Leases werden mit 8-Byte-Zeitstempeln gesendet, auch wenn das zurückgegebene LeaseSet ein LS2 mit 4-Byte-Zeitstempeln sein wird. Beachten Sie, dass die Antwort eine Create Leaseset- oder Create Leaseset2-Message sein kann.

### Nachricht zur Anforderung eines variablen LeaseSet

Router zu Client. Keine Änderungen. Die Leases werden mit 8-Byte-Zeitstempeln gesendet, auch wenn das zurückgegebene LeaseSet ein LS2 mit 4-Byte-Zeitstempeln sein wird. Beachten Sie, dass die Antwort eine Create Leaseset- oder Create Leaseset2-Message sein kann.

### Leaseset2-Nachricht erstellen

Client zu Router. Neue Nachricht, die anstelle der Create Leaseset Message verwendet wird.

### Begründung

- Damit der Router den Store-Typ parsen kann, muss der Typ in der Nachricht enthalten sein,
  es sei denn, er wird dem Router vorab in der Session-Konfiguration übergeben.
  Für allgemeinen Parsing-Code ist es einfacher, ihn in der Nachricht selbst zu haben.

- Damit der router Typ und Länge des privaten Schlüssels kennt,
  muss er hinter dem leaseSet stehen, es sei denn, der Parser kennt den Typ vorab
  in der Session-Konfiguration.
  Für allgemeinen Parsing-Code ist es einfacher, ihn aus der Nachricht selbst zu entnehmen.

- Der Signaturschlüssel (private key), der zuvor für den Widerruf definiert und ungenutzt war,
  ist in LS2 nicht enthalten.

### Nachrichtentyp

Der Nachrichtentyp für die Create Leaseset2 Message ist 41.

### Format

```
Session ID
  Type byte: Type of lease set to follow
             Type 1 is a LS
             Type 3 is a LS2
             Type 5 is a encrypted LS2
             Type 7 is a meta LS2
  LeaseSet: type specified above
  Number of private keys to follow (1 byte)
  Encryption Private Keys: For each public key in the lease set,
                           in the same order
                           (Not present for Meta LS2)
                           - Encryption type (2 bytes, big endian)
                           - Encryption key length (2 bytes, big endian)
                           - Encryption key (number of bytes specified)
```
### Hinweise

- Die minimale Router-Version ist 0.9.39.
- Eine vorläufige Version mit Nachrichtentyp 40 gab es in 0.9.38, aber das Format wurde geändert.
  Typ 40 wurde verworfen und wird nicht unterstützt.

### Probleme

- Es sind weitere Änderungen erforderlich, um verschlüsselte und Meta-LS zu unterstützen.

### Blinding-Info-Nachricht

Client zum Router. Neue Nachricht.

### Begründung

- Der router muss wissen, ob ein Ziel geblindet ist.
  Wenn es geblindet ist und eine geheime oder per-Client-Authentifizierung verwendet,
  müssen ihm auch diese Informationen vorliegen.

- Ein Host-Lookup einer b32-Adresse im neuen Format („b33“)
  teilt dem Router mit, dass die Adresse blinded ist, aber es gibt keinen Mechanismus,
  um den Secret Key oder Private Key in der Host-Lookup-Nachricht an den Router zu übergeben.
  Wir könnten die Host-Lookup-Nachricht zwar erweitern, um diese Information hinzuzufügen,
  aber es ist sauberer, eine neue Nachricht zu definieren.

- Wir benötigen eine programmatische Möglichkeit für den Client, dem Router dies mitzuteilen.
  Andernfalls müsste der Benutzer jede Destination manuell konfigurieren.

### Verwendung

Bevor ein Client eine Nachricht an ein geblindetes Ziel sendet, muss er entweder die "b33" in einer Host-Lookup-Nachricht nachschlagen oder eine Blinding-Info-Nachricht senden. Wenn das geblindete Ziel ein Secret oder eine per-Client-Authentifizierung erfordert, muss der Client eine Blinding-Info-Nachricht senden.

Der Router sendet keine Antwort auf diese Nachricht.

### Nachrichtentyp

Der Nachrichtentyp für die Blinding Info Message ist 42.

### Format

```
Session ID
  Flags:       1 byte
               Bit order: 76543210
               Bit 0: 0 for everybody, 1 for per-client
               Bits 3-1: Authentication scheme, if bit 0 is set to 1 for per-client, otherwise 000
                         000: DH client authentication (or no per-client authentication)
                         001: PSK client authentication
               Bit 4: 1 if secret required, 0 if no secret required
               Bits 7-5: Unused, set to 0 for future compatibility
  Type byte:   Endpoint type to follow
               Type 0 is a Hash
               Type 1 is a host name String
               Type 2 is a Destination
               Type 3 is a Sig Type and Signing Public Key
  Blind Type:  2 byte blinded sig type (big endian)
  Expiration:  4 bytes, big endian, seconds since epoch
  Endpoint:    Data as specified above
               For type 0: 32 byte binary hash
               For type 1: host name String
               For type 2: binary Destination
               For type 3: 2 byte sig type (big endian)
                           Signing Public Key (length as implied by sig type)
  Private Key: Only if flag bit 0 is set to 1
               A 32-byte ECIES_X25519 private key
  Secret:      Only if flag bit 4 is set to 1
               A secret String
```
### Hinweise

- Die minimale router-Version ist 0.9.43

### Probleme

### Host-Antwortnachricht (verschlüsselt)

Um Lookups von „b33“-Hostnamen zu unterstützen und einen Hinweis zurückzugeben, wenn der Router nicht über die erforderlichen Informationen verfügt, definieren wir zusätzliche Ergebniscodes für die Host Reply Message wie folgt:

```
2: Lookup password required
   3: Private key required
   4: Lookup password and private key required
   5: Leaseset decryption failure
```
Werte 1-255 sind bereits als Fehler definiert, daher gibt es kein Problem mit der Rückwärtskompatibilität.

### Meta-Weiterleitungsnachricht

Router zum Client. Neue Nachricht.

### Begründung

Ein Client weiß a priori nicht, dass ein gegebener Hash zu einem Meta LS aufgelöst wird.

Wenn eine leaseset-Suche für ein Destination ein Meta LS zurückgibt, führt der router die rekursive Auflösung durch. Bei Datagrammen muss die Client-Seite nichts davon wissen; beim Streaming jedoch, wo das Protokoll das Ziel im SYN ACK prüft, muss sie wissen, was das „echte“ Destination ist. Daher benötigen wir eine neue Nachricht.

### Verwendung

Der router unterhält einen Cache für das tatsächliche Ziel, das aus einem Meta-LS verwendet wird. Wenn der Client eine Nachricht an ein Ziel sendet, das sich auf ein Meta-LS auflöst, prüft der router den Cache auf das zuletzt verwendete tatsächliche Ziel. Ist der Cache leer, wählt der router ein Ziel aus dem Meta-LS aus und schlägt das leaseset nach. Ist die leaseset-Suche erfolgreich, fügt der router dieses Ziel dem Cache hinzu und sendet dem Client eine Meta Redirect Message. Dies geschieht nur einmal, es sei denn, das Ziel läuft ab und muss geändert werden. Der Client muss die Informationen bei Bedarf ebenfalls zwischenspeichern. Die Meta Redirect Message wird NICHT als Antwort auf jede SendMessage gesendet.

Der Router sendet diese Nachricht nur an Clients mit Version 0.9.47 oder höher.

Der Client sendet keine Antwort auf diese Nachricht.

### Nachrichtentyp

Der Nachrichtentyp für die Meta Redirect Message ist 43.

### Format

```
Session ID (2 bytes) The value from the Send Message.
  Message ID generated by the router (4 bytes)
  4 byte nonce previously generated by the client
               (the value from the Send Message, may be zero)
  Flags:       2 bytes, bit order 15...0
               Unused, set to 0 for future compatibility
               Bit 0: 0 - the destination is no longer meta
                      1 - the destination is now meta
               Bits 15-1: Unused, set to 0 for future compatibility
  Original Destination (387+ bytes)
  (following fields only present if flags bit 0 is 1)
  MFlags:      2 bytes
               Unused, set to 0 for future compatibility
               From the Meta Lease for the actual Destination
  Expiration:  4 bytes, big endian, seconds since epoch
               From the Meta Lease for the actual Destination
  Cost (priority) 1 byte
               From the Meta Lease for the actual Destination
  Actual (real) Destination (387+ bytes)
```
### Änderungen zur Unterstützung von Meta

Wie Meta erzeugt und unterstützt wird, einschließlich Inter-Router-Kommunikation und -Koordination, ist nicht Gegenstand dieses Vorschlags. Siehe zugehörigen Vorschlag 150.

### Änderungen zur Unterstützung von Offline-Schlüsseln

Offline-Signaturen können in Streaming- oder repliable Datagrams nicht verifiziert werden. Siehe die Abschnitte unten.

## Erforderliche Änderungen an der Private-Key-Datei

Das Format der Datei mit dem privaten Schlüssel (eepPriv.dat) ist kein offizieller Teil unserer Spezifikationen, aber es ist in den [Java I2P javadocs](http://idk.i2p/javadoc-i2p/net/i2p/data/PrivateKeyFile.html) dokumentiert, und andere Implementierungen unterstützen es. Dies ermöglicht die Portabilität privater Schlüssel zwischen verschiedenen Implementierungen.

Änderungen sind erforderlich, um den ephemeren öffentlichen Schlüssel und die Informationen für die Offline-Signatur zu speichern.

### Änderungen

```
If the signing private key is all zeros, the offline information section follows:

  - Expires timestamp
    (4 bytes, big endian, seconds since epoch, rolls over in 2106)
  - Sig type of transient Signing Public Key (2 bytes, big endian)
  - Transient Signing Public key
    (length as specified by transient sig type)
  - Signature of above three fields by offline key
    (length as specified by destination sig type)
  - Transient Signing Private key
    (length as specified by transient sig type)
```
### Erforderliche Änderungen an der CLI der Private-Key-Datei

Unterstützung für die folgenden Optionen hinzufügen:

```
-d days              (specify expiration in days of offline sig, default 365)
      -o offlinedestfile   (generate the online key file,
                            using the offline key file specified)
      -r sigtype           (specify sig type of transient key, default Ed25519)
```
## Erforderliche Streaming-Änderungen

Offline-Signaturen können derzeit im Streaming nicht verifiziert werden. Die untenstehende Änderung fügt den Offline-Signaturblock den Optionen hinzu. Dadurch muss diese Information nicht über I2CP abgerufen werden.

### Änderungen

```
Add new option:
  Bit:          11
  Flag:         OFFLINE_SIGNATURE
  Option order: 4
  Option data:  Variable bytes
  Function:     Contains the offline signature section from LS2.
                FROM_INCLUDED must also be set.
                Expires timestamp
                (4 bytes, big endian, seconds since epoch, rolls over in 2106)
                Transient sig type (2 bytes, big endian)
                Transient signing public key (length as implied by sig type)
                Signature of expires timestamp, transient sig type,
                and public key, by the destination public key,
                length as implied by destination public key sig type.

  Change option:
  Bit:          3
  Flag:         SIGNATURE_INCLUDED
  Option order: Change from 4 to 5

  Add information about transient keys to the
  Variable Length Signature Notes section:
  The offline signature option does not needed to be added for a CLOSE packet if
  a SYN packet containing the option was previously acked.
  More info TODO
```
### Hinweise

- Alternative ist, einfach ein Flag hinzuzufügen und den transienten öffentlichen Schlüssel über I2CP abzurufen
  (Siehe Abschnitte Host Lookup / Host Reply Message oben)

## Erforderliche Änderungen für beantwortbare Datagramme

Offline-Signaturen können bei der Verarbeitung von repliable Datagrammen nicht verifiziert werden. Es wird ein Flag benötigt, das offline signiert anzeigt, aber es gibt keinen Platz, um ein Flag unterzubringen. Dies erfordert eine vollständig neue Protokollnummer und ein neues Format.

### Änderungen

```
Define new protocol 19 - Repliable datagram with options?
  - Destination (387+ bytes)
  - Flags (2 bytes)
    Bit order: 15 14 ... 3 2 1 0
    Bit 0: If 0, no offline keys; if 1, offline keys
    Bits 1-15: set to 0 for compatibility with future uses
  - If flag indicates offline keys, the offline signature section:
    Expires timestamp
    (4 bytes, big endian, seconds since epoch, rolls over in 2106)
    Transient sig type (2 bytes, big endian)
    Transient signing public key (length as implied by sig type)
    Signature of expires timestamp, transient sig type,
    and public key, by the destination public key,
    length as implied by destination public key sig type.
    This section can, and should, be generated offline.
  - Data
```
### Hinweise

- Alternative ist, einfach ein Flag hinzuzufügen und den transienten öffentlichen Schlüssel über I2CP abzurufen
  (Siehe Abschnitte Host Lookup / Host Reply Message oben)
- Gibt es weitere Optionen, die wir jetzt hinzufügen sollten, da wir Flag-Bytes haben?

## Erforderliche Änderungen an SAM V3

SAM muss erweitert werden, um Offline-Signaturen in der DESTINATION-Base64 zu unterstützen.

### Änderungen

```
Note that in the SESSION CREATE DESTINATION=$privkey,
  the $privkey raw data (before base64 conversion)
  may be optionally followed by the Offline Signature as specified in the
  Common Structures Specification.

  If the signing private key is all zeros, the offline information section follows:

  - Expires timestamp
    (4 bytes, big endian, seconds since epoch, rolls over in 2106)
  - Sig type of transient Signing Public Key (2 bytes, big endian)
  - Transient Signing Public key
    (length as specified by transient sig type)
  - Signature of above three fields by offline key
    (length as specified by destination sig type)
  - Transient Signing Private key (length as specified by transient sig type)
```
Beachten Sie, dass Offline-Signaturen nur für STREAM und RAW unterstützt werden, nicht für DATAGRAM (bis wir ein neues DATAGRAM-Protokoll definieren).

Beachten Sie, dass SESSION STATUS einen Signing Private Key aus lauter Nullen sowie die Offline Signature-Daten genau so zurückgibt, wie sie im SESSION CREATE übergeben wurden.

Beachten Sie, dass DEST GENERATE und SESSION CREATE DESTINATION=TRANSIENT nicht verwendet werden können, um ein offline signiertes Destination zu erstellen.

### Probleme

Die Version auf 3.4 anheben oder bei 3.1/3.2/3.3 belassen, damit sie hinzugefügt werden kann, ohne dass all das aus 3.2/3.3 erforderlich ist?

Weitere Änderungen noch offen. Siehe Abschnitt „I2CP Host Reply Message“ oben.

## BOB Änderungen erforderlich

BOB müsste erweitert werden, um Offline-Signaturen und/oder Meta LS zu unterstützen. Dies hat niedrige Priorität und wird wahrscheinlich nie spezifiziert oder implementiert werden. SAM V3 ist die bevorzugte Schnittstelle.

## Veröffentlichung, Migration, Kompatibilität

LS2 (außer verschlüsseltes LS2) wird am selben DHT-Ort wie LS1 veröffentlicht. Es gibt keine Möglichkeit, sowohl ein LS1 als auch ein LS2 zu veröffentlichen, es sei denn, LS2 befände sich an einem anderen Ort.

Encrypted LS2 wird unter dem Hash aus Blinded-Key-Typ und Key-Daten veröffentlicht. Dieser Hash wird dann verwendet, um den täglichen „Routing-Key“ zu erzeugen, wie bei LS1.

LS2 würde nur verwendet, wenn neue Funktionen erforderlich sind (neue Krypto, verschlüsselte LS, Meta usw.). LS2 kann nur bei Floodfills einer bestimmten Version oder höher veröffentlicht werden.

Server, die LS2 veröffentlichen, wüssten, dass alle sich verbindenden Clients LS2 unterstützen. Sie könnten LS2 im Garlic senden.

Clients würden LS2 nur dann in Garlics senden, wenn sie neue Krypto verwenden. Würden Shared Clients LS1 auf unbestimmte Zeit verwenden? TODO: Wie kann man einen Shared Client haben, der sowohl alte als auch neue Krypto unterstützt?

## Ausroll

0.9.38 enthält floodfill-Unterstützung für Standard-LS2, einschließlich Offline-Keys.

0.9.39 enthält I2CP-Unterstützung für LS2 und Encrypted LS2, Signieren/Verifizieren mit Sig-Typ 11, Floodfill-Unterstützung für Encrypted LS2 (Sig-Typen 7 und 11, ohne Offline-Schlüssel) sowie Ver- und Entschlüsselung von LS2 (ohne per-Client-Autorisierung).

0.9.40 soll Unterstützung für die Ver- und Entschlüsselung von LS2 mit Autorisierung pro Client, Floodfill- und I2CP-Unterstützung für Meta LS2, Unterstützung für verschlüsselte LS2 mit Offline-Schlüsseln sowie b32-Unterstützung für verschlüsselte LS2 enthalten.

## Danksagungen

Das Design der verschlüsselten LS2 ist stark von [Tors v3 Hidden-Service-Deskriptoren](https://spec.torproject.org/rend-spec-v3) beeinflusst, die ähnliche Designziele verfolgten.

## Referenzen

* ["High-speed high-security signatures" von Daniel J. Bernstein, Niels Duif, Tanja Lange, Peter Schwabe und Bo-Yin Yang](https://ed25519.cr.yp.to/)
* [KEYBLIND-PROOF](https://lists.torproject.org/pipermail/tor-dev/2013-December/005943.html)
* [KEYBLIND-REFS](https://gitlab.torproject.org/tpo/core/tor/-/issues/8106)
* [PRNG-REFS](http://projectbullrun.org/dual-ec/ext-rand.html)
* [RFC-2104](https://tools.ietf.org/html/rfc2104)
* [RFC-4880-S5.1](https://tools.ietf.org/html/rfc4880#section-5.1)
* [RFC-5869](https://tools.ietf.org/html/rfc5869)
* [RFC-7539-S2.4](https://tools.ietf.org/html/rfc7539#section-2.4)
* [TOR-REND-SPEC-V3](https://spec.torproject.org/rend-spec-v3)
* [UNSCIENTIFIC-KDF-SPEEDS](https://www.lvh.io/posts/secure-key-derivation-performance.html)
* [ZCASH](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf)
