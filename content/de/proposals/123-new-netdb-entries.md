---
title: "Neue netDB-Einträge"
number: "123"
author: "zzz, str4d, orignal"
created: "2016-01-16"
lastupdated: "2020-07-18"
status: "Öffnen"
thread: "http://zzz.i2p/topics/2051"
supercedes: "110, 120, 121, 122"
---

## Status

Teile dieses Vorschlags sind vollständig und in 0.9.38 und 0.9.39 implementiert. Die Common Structures, I2CP, I2NP und andere Spezifikationen sind nun aktualisiert, um die Änderungen zu reflektieren, die jetzt unterstützt werden.

Die fertiggestellten Teile unterliegen noch geringfügigen Überarbeitungen. Andere Teile dieses Vorschlags befinden sich noch in der Entwicklung und können erheblichen Änderungen unterworfen sein.

Service Lookup (Typen 9 und 11) haben niedrige Priorität und sind ungeplant und könnten in einen separaten Vorschlag ausgelagert werden.

## Überblick

Dies ist eine Aktualisierung und Zusammenfassung der folgenden 4 Vorschläge:

- 110 LS2
- 120 Meta LS2 für massives Multihoming
- 121 Verschlüsseltes LS2
- 122 Nicht authentifizierte Dienst-Suche (Anycasting)

Diese Vorschläge sind größtenteils unabhängig, aber der Vernunft halber definieren und verwenden wir ein gemeinsames Format für mehrere von ihnen.

Die folgenden Vorschläge stehen in gewissem Zusammenhang:

- 140 Invisible Multihoming (nicht kompatibel mit diesem Vorschlag)
- 142 New Crypto Template (für neue symmetrische Kryptographie)
- 144 ECIES-X25519-AEAD-Ratchet
- 145 ECIES-P256
- 146 Red25519
- 148 EdDSA-BLAKE2b-Ed25519
- 149 B32 for Encrypted LS2
- 150 Garlic Farm Protocol
- 151 ECDSA Blinding

## Vorschlag

Dieser Vorschlag definiert 5 neue DatabaseEntry-Typen und den Prozess für deren Speicherung in und Abruf aus der Netzwerkdatenbank, sowie die Methode für deren Signierung und Verifikation dieser Signaturen.

### Goals

- Rückwärtskompatibel
- LS2 verwendbar mit altem multihoming-Stil
- Keine neue Kryptografie oder Primitiven für die Unterstützung erforderlich
- Entkopplung von Kryptografie und Signierung beibehalten; alle aktuellen und zukünftigen Versionen unterstützen
- Optionale offline Signaturschlüssel ermöglichen
- Genauigkeit von Zeitstempeln reduzieren, um Fingerprinting zu verringern
- Neue Kryptografie für Ziele ermöglichen
- Massives multihoming ermöglichen
- Mehrere Probleme mit bestehenden verschlüsselten LS beheben
- Optionales blinding zur Reduzierung der Sichtbarkeit durch floodfills
- Verschlüsselt unterstützt sowohl Einzel-Schlüssel als auch mehrere widerrufbare Schlüssel
- Service-Lookup für einfachere Suche nach outproxies, Anwendungs-DHT-Bootstrap
  und andere Verwendungen
- Nichts kaputt machen, was auf 32-Byte-Binär-Destination-Hashes angewiesen ist, z.B. bittorrent
- Flexibilität zu leasesets über Eigenschaften hinzufügen, wie wir sie in routerinfos haben.
- Veröffentlichungszeitstempel und variable Ablaufzeit in Header setzen, damit es auch funktioniert,
  wenn Inhalte verschlüsselt sind (Zeitstempel nicht aus frühestem lease ableiten)
- Alle neuen Typen leben im selben DHT-Raum und an denselben Orten wie bestehende leasesets,
  damit Benutzer vom alten LS zu LS2 migrieren können,
  oder zwischen LS2, Meta und Encrypted wechseln können,
  ohne die Destination oder den Hash zu ändern.
- Eine bestehende Destination kann zur Verwendung von offline-Schlüsseln konvertiert werden,
  oder zurück zu online-Schlüsseln, ohne die Destination oder den Hash zu ändern.

### Non-Goals / Out-of-scope

- Neuer DHT-Rotationsalgorithmus oder gemeinsame Zufallszahlengenerierung
- Der spezifische neue Verschlüsselungstyp und das Ende-zu-Ende-Verschlüsselungsschema
  zur Verwendung dieses neuen Typs wären in einem separaten Vorschlag.
  Keine neue Kryptographie wird hier spezifiziert oder diskutiert.
- Neue Verschlüsselung für RIs oder tunnel building.
  Das wäre in einem separaten Vorschlag.
- Methoden der Verschlüsselung, Übertragung und des Empfangs von I2NP DLM / DSM / DSRM Nachrichten.
  Werden nicht geändert.
- Wie Meta generiert und unterstützt wird, einschließlich Backend-Kommunikation zwischen Routern, Verwaltung, Failover und Koordination.
  Unterstützung könnte zu I2CP oder i2pcontrol oder einem neuen Protokoll hinzugefügt werden.
  Dies kann standardisiert werden oder auch nicht.
- Wie länger laufende Tunnel tatsächlich implementiert und verwaltet werden, oder bestehende Tunnel abgebrochen werden.
  Das ist extrem schwierig, und ohne das kann man kein vernünftiges graceful shutdown haben.
- Änderungen am Bedrohungsmodell
- Offline-Speicherformat oder Methoden zum Speichern/Abrufen/Teilen der Daten.
- Implementierungsdetails werden hier nicht diskutiert und jedem Projekt überlassen.

### Justification

LS2 fügt Felder hinzu, um den Verschlüsselungstyp zu ändern und für zukünftige Protokolländerungen.

Encrypted LS2 behebt mehrere Sicherheitsprobleme mit dem bestehenden encrypted LS durch die Verwendung asymmetrischer Verschlüsselung des gesamten Lease-Sets.

Meta LS2 bietet flexibles, effizientes, wirksames und groß angelegtes Multihoming.

Service Record und Service List bieten Anycast-Dienste wie Namensauflösung und DHT-Bootstrapping.

### Ziele

Die Typnummern werden in den I2NP Database Lookup/Store Messages verwendet.

Die End-zu-End-Spalte bezieht sich darauf, ob Abfragen/Antworten an ein Destination in einer Garlic Message gesendet werden.

Vorhandene Typen:

| NetDB Data | Lookup Type | Store Type |
|------------|-------------|------------|
| any        | 0           | any        |
| LS         | 1           | 1          |
| RI         | 2           | 0          |
| exploratory| 3           | DSRM       |
Neue Typen:

| NetDB Data     | Lookup Type | Store Type | Std. LS2 Header? | Sent end-to-end? |
|----------------|-------------|------------|------------------|------------------|
| LS2            | 1           | 3          | yes              | yes              |
| Encrypted LS2  | 1           | 5          | no               | no               |
| Meta LS2       | 1           | 7          | yes              | no               |
| Service Record | n/a         | 9          | yes              | no               |
| Service List   | 4           | 11         | no               | no               |
### Nicht-Ziele / Außerhalb des Umfangs

- Lookup-Typen sind derzeit Bits 3-2 in der Database Lookup Message.
  Alle zusätzlichen Typen würden die Verwendung von Bit 4 erfordern.

- Alle Store-Typen sind ungerade, da die oberen Bits im Typfeld der Database Store Message
  von alten Routern ignoriert werden.
  Wir möchten lieber, dass das Parsen als LS fehlschlägt anstatt als komprimierte RI.

- Sollte der Typ explizit oder implizit oder keines von beidem in den von der Signatur abgedeckten Daten sein?

### Begründung

Die Typen 3, 5 und 7 können als Antwort auf eine Standard-leaseSet-Suche (Typ 1) zurückgegeben werden. Typ 9 wird niemals als Antwort auf eine Suche zurückgegeben. Typ 11 wird als Antwort auf einen neuen Service-Lookup-Typ (Typ 11) zurückgegeben.

Nur Typ 3 darf in einer Client-zu-Client Garlic-Nachricht gesendet werden.

### NetDB-Datentypen

Die Typen 3, 7 und 9 haben alle ein gemeinsames Format::

Standard LS2 Header   - wie unten definiert

Typenspezifischer Teil - wie unten in jedem Teil definiert

Standard LS2 Signatur:   - Länge wie durch Signaturtyp des Signaturschlüssels impliziert

Typ 5 (Verschlüsselt) beginnt nicht mit einem Destination und hat ein anderes Format. Siehe unten.

Typ 11 (Service List) ist eine Zusammenfassung mehrerer Service Records und hat ein anderes Format. Siehe unten.

### Hinweise

TBD

## Standard LS2 Header

Typen 3, 7 und 9 verwenden den Standard-LS2-Header, der unten spezifiziert ist:

### Lookup/Store-Prozess

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
### Format

- Unpublished/published: Zur Verwendung beim Ende-zu-Ende-Versenden eines Database Store
  kann der sendende router anzeigen wollen, dass dieses leaseSet nicht an
  andere weitergeleitet werden soll. Wir verwenden derzeit Heuristiken, um diesen Zustand aufrechtzuerhalten.

- Published: Ersetzt die komplexe Logik, die erforderlich ist, um die 'Version' des
  leaseSet zu bestimmen. Derzeit ist die Version das Ablaufdatum des zuletzt ablaufenden Lease,
  und ein veröffentlichender Router muss dieses Ablaufdatum um mindestens 1ms erhöhen, wenn
  er ein leaseSet veröffentlicht, das nur einen älteren Lease entfernt.

- Expires: Ermöglicht, dass ein netDb-Eintrag früher abläuft als sein am spätesten ablaufendes leaseSet. Möglicherweise nicht nützlich für LS2, wo leasesets erwartungsgemäß bei einer maximalen Ablaufzeit von 11 Minuten bleiben, aber für andere neue Typen ist es notwendig (siehe Meta LS und Service Record unten).

- Offline-Schlüssel sind optional, um die anfängliche/erforderliche Implementierungskomplexität zu reduzieren.

### Datenschutz-/Sicherheitsüberlegungen

- Könnte die Timestamp-Genauigkeit noch weiter reduzieren (10 Minuten?), müsste aber
  eine Versionsnummer hinzufügen. Dies könnte Multihoming beeinträchtigen, es sei denn, wir haben
  ordnungserhaltende Verschlüsselung? Wahrscheinlich geht es nicht ganz ohne Timestamps.

- Alternative: 3 Byte Zeitstempel (Epoche / 10 Minuten), 1-Byte Version, 2-Byte läuft ab

- Ist der Typ explizit oder implizit in Daten / Signatur? "Domain"-Konstanten für Signatur?

### Notes

- Router sollten nicht öfter als einmal pro Sekunde eine LS veröffentlichen.
  Falls doch, müssen sie den veröffentlichten Zeitstempel künstlich um 1 über die zuvor veröffentlichte LS erhöhen.

- Router-Implementierungen könnten die transienten Schlüssel und Signaturen zwischenspeichern, um die Verifikation bei jedem Mal zu vermeiden. Insbesondere floodfills und Router an beiden Enden langlebiger Verbindungen könnten davon profitieren.

- Offline-Schlüssel und -Signaturen sind nur für langlebige Ziele geeignet,
  d.h. Server, nicht Clients.

## New DatabaseEntry types

### Format

Änderungen gegenüber dem bestehenden LeaseSet:

- Veröffentlichungszeitstempel, Ablaufzeitstempel, Flags und Eigenschaften hinzufügen
- Verschlüsselungstyp hinzufügen
- Widerrufschlüssel entfernen

Suche mit     Standard LS Flag (1) Speicherung mit     Standard LS2 Typ (3) Speicherung bei     Hash des Ziels     Dieser Hash wird dann verwendet, um den täglichen "routing key" zu generieren, wie bei LS1 Typische Ablaufzeit     10 Minuten, wie bei einem regulären LS. Veröffentlicht von     Ziel

    Standard LS flag (1)
Dieser Vorschlag verwendet weiterhin den öffentlichen Schlüssel im leaseset für den Ende-zu-Ende-Verschlüsselungsschlüssel und lässt das Feld für den öffentlichen Schlüssel in der Destination ungenutzt, wie es derzeit der Fall ist. Der Verschlüsselungstyp wird nicht im Destination-Schlüsselzertifikat angegeben, er bleibt bei 0.

    Standard LS2 type (3)
Eine verworfene Alternative ist es, den Verschlüsselungstyp im Destination-Schlüsselzertifikat anzugeben, den öffentlichen Schlüssel in der Destination zu verwenden und den öffentlichen Schlüssel im LeaseSet nicht zu verwenden. Wir planen nicht, dies zu tun.

    Hash of destination
    This hash is then used to generate the daily "routing key", as in LS1
Vorteile von LS2:

    10 minutes, as in a regular LS.
Nachteile von LS2:

    Destination

### Begründung

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
### Probleme

- Properties: Zukünftige Erweiterung und Flexibilität.
  Zuerst platziert für den Fall, dass es für das Parsen der verbleibenden Daten notwendig ist.

- Mehrere Verschlüsselungstyp/öffentliche Schlüssel-Paare dienen
  dazu, den Übergang zu neuen Verschlüsselungstypen zu erleichtern. Die andere Möglichkeit
  ist es, mehrere leasesets zu veröffentlichen, möglicherweise unter Verwendung derselben tunnels,
  wie wir es jetzt für DSA- und EdDSA-Ziele tun.
  Die Identifikation des eingehenden Verschlüsselungstyps auf einem tunnel
  kann mit dem bestehenden Session-Tag-Mechanismus erfolgen,
  und/oder durch Probe-Entschlüsselung mit jedem Schlüssel. Die Längen der eingehenden
  Nachrichten können ebenfalls einen Hinweis liefern.

### Hinweise

Einiges davon liegt außerhalb des Umfangs dieses Vorschlags, aber wir notieren es hier vorerst, da wir noch keinen separaten Verschlüsselungsvorschlag haben. Siehe auch die ECIES-Vorschläge 144 und 145.

Ziele:

Verschlüsselte LS2 werden niemals in einer End-to-End-Garlic-Nachricht gesendet. Verwenden Sie die Standard-LS2 wie oben beschrieben.

- Der Standort des tatsächlichen öffentlichen Schlüssels ändert sich nicht.
- Verschlüsselungstyp oder öffentlicher Schlüssel können sich ändern, ohne dass sich die Destination ändert.
- Entfernt ungenutztes Widerrufsfeld
- Grundlegende Kompatibilität mit anderen DatabaseEntry-Typen in diesem Vorschlag
- Erlaubt mehrere Verschlüsselungstypen

Änderungen gegenüber bestehenden verschlüsselten LeaseSet:

- Position des öffentlichen Schlüssels und Verschlüsselungstyp unterscheidet sich von RouterInfo
- Behält ungenutzten öffentlichen Schlüssel im leaseSet bei
- Erfordert netzweite Implementierung; alternativ können experimentelle
  Verschlüsselungstypen verwendet werden, falls von floodfills erlaubt
  (siehe aber auch die verwandten Vorschläge 136 und 137 bezüglich Unterstützung für experimentelle Signaturtypen).
  Der alternative Vorschlag könnte einfacher zu implementieren und für experimentelle Verschlüsselungstypen zu testen sein.

### New Encryption Issues

Lookup mit     Standard LS Flag (1) Speichern mit     Verschlüsselter LS2 Typ (5) Speichern unter     Hash des geblindeten Sig-Typs und geblindeten öffentlichen Schlüssels     Zwei-Byte Sig-Typ (Big Endian, z.B. 0x000b) || geblindeter öffentlicher Schlüssel     Dieser Hash wird dann verwendet, um den täglichen "Routing-Schlüssel" zu generieren, wie in LS1 Typische Ablaufzeit     10 Minuten, wie in einem regulären LS, oder Stunden, wie in einem Meta-LS. Veröffentlicht von     Destination

- Der Verschlüsselungstyp repräsentiert die Kombination
  aus Kurve, Schlüssellänge und End-to-End-Schema,
  einschließlich KDF und MAC, falls vorhanden.

- Wir haben ein Schlüssellängenfeld eingefügt, damit das LS2 vom floodfill geparst und verifiziert werden kann, auch bei unbekannten Verschlüsselungstypen.

- Der erste neue Verschlüsselungstyp, der vorgeschlagen wird,
  wird wahrscheinlich ECIES/X25519 sein. Wie er Ende-zu-Ende
  verwendet wird (entweder eine leicht modifizierte Version von ElGamal/AES+SessionTag
  oder etwas völlig Neues, z.B. ChaCha/Poly) wird in einem
  oder mehreren separaten Vorschlägen spezifiziert werden.
  Siehe auch die ECIES-Vorschläge 144 und 145.

### LeaseSet 2

- 8-Byte-Ablaufzeit in Leases auf 4 Bytes geändert.

- Falls wir jemals eine Sperrung implementieren, können wir dies mit einem expires-Feld von null,
  oder null leases, oder beidem tun. Kein Bedarf für einen separaten Sperrschlüssel.

- Verschlüsselungsschlüssel sind in der Reihenfolge der Serverpräferenz angeordnet, der bevorzugteste zuerst.
  Das Standard-Client-Verhalten ist es, den ersten Schlüssel mit
  einem unterstützten Verschlüsselungstyp auszuwählen. Clients können andere Auswahlalgorithmen
  basierend auf Verschlüsselungsunterstützung, relativer Leistung und anderen Faktoren verwenden.

### Format

Wir definieren die folgenden Funktionen, die den kryptographischen Bausteinen entsprechen, die für verschlüsselte LS2 verwendet werden:

- Blinding hinzufügen
- Mehrere Signaturtypen erlauben
- Keine neuen kryptographischen Primitive erforderlich
- Optional Verschlüsselung für jeden Empfänger, widerrufbar
- Unterstützung der Verschlüsselung nur für Standard LS2 und Meta LS2

CSRNG(n)     n-Byte-Ausgabe eines kryptographisch sicheren Zufallszahlengenerators.

Zusätzlich zur Anforderung, dass CSRNG kryptographisch sicher sein muss (und somit zur Generierung von Schlüsselmaterial geeignet ist), MUSS es sicher sein, dass eine n-Byte-Ausgabe für Schlüsselmaterial verwendet werden kann, wenn die unmittelbar davor und danach liegenden Byte-Sequenzen im Netzwerk preisgegeben werden (wie beispielsweise in einem Salt oder verschlüsseltem Padding). Implementierungen, die sich auf eine möglicherweise nicht vertrauenswürdige Quelle stützen, sollten jede Ausgabe hashen, die im Netzwerk preisgegeben werden soll. Siehe [PRNG references](http://projectbullrun.org/dual-ec/ext-rand.html) und [Tor dev discussion](https://lists.torproject.org/pipermail/tor-dev/2015-November/009954.html).

- Das Ganze zur Sicherheit verschlüsseln
- Sicher verschlüsseln, nicht nur mit AES.
- Für jeden Empfänger verschlüsseln

H(p, d)     SHA-256 Hash-Funktion, die eine Personalisierungszeichenkette p und Daten d nimmt und eine Ausgabe von 32 Bytes Länge erzeugt.

    Standard LS flag (1)
Verwende SHA-256 wie folgt::

    Encrypted LS2 type (5)
H(p, d) := SHA-256(p || d)

    Hash of blinded sig type and blinded public key
    Two byte sig type (big endian, e.g. 0x000b) || blinded public key
    This hash is then used to generate the daily "routing key", as in LS1
STREAM     Die ChaCha20 Stream-Verschlüsselung wie spezifiziert in [RFC 7539 Section 2.4](https://tools.ietf.org/html/rfc7539#section-2.4), mit dem initialen Zähler     auf 1 gesetzt. S_KEY_LEN = 32 und S_IV_LEN = 12.

    10 minutes, as in a regular LS, or hours, as in a meta LS.
ENCRYPT(k, iv, plaintext)         Verschlüsselt den Klartext mit dem Chiffrierschlüssel k und der Nonce iv, die für den Schlüssel k eindeutig sein MUSS. Gibt einen Geheimtext zurück, der die gleiche Größe wie der Klartext hat.

    Destination


### Begründung

Der gesamte Chiffretext muss von zufälligen Daten nicht unterscheidbar sein, wenn der Schlüssel geheim ist.

DECRYPT(k, iv, ciphertext)         Entschlüsselt den Chiffretext mit dem Chiffrierschlüssel k und der Nonce iv. Gibt den Klartext zurück.

    n-byte output from a cryptographically-secure random number generator.

    In addition to the requirement of CSRNG being cryptographically-secure (and thus
    suitable for generating key material), it MUST be safe
    for some n-byte output to be used for key material when the byte sequences immediately
    preceding and following it are exposed on the network (such as in a salt, or encrypted
    padding). Implementations that rely on a potentially-untrustworthy source should hash
    any output that is to be exposed on the network. See [PRNG references](http://projectbullrun.org/dual-ec/ext-rand.html) and [Tor dev discussion](https://lists.torproject.org/pipermail/tor-dev/2015-November/009954.html).

SIG     Das RedDSA-Signaturschema (entsprechend SigType 11) mit Key Blinding.     Es hat die folgenden Funktionen:

    SHA-256 hash function that takes a personalization string p and data d, and
    produces an output of length 32 bytes.

    Use SHA-256 as follows::

        H(p, d) := SHA-256(p || d)

DERIVE_PUBLIC(privkey)         Gibt den öffentlichen Schlüssel zurück, der dem angegebenen privaten Schlüssel entspricht.

    The ChaCha20 stream cipher as specified in [RFC 7539 Section 2.4](https://tools.ietf.org/html/rfc7539#section-2.4), with the initial counter
    set to 1. S_KEY_LEN = 32 and S_IV_LEN = 12.

    ENCRYPT(k, iv, plaintext)
        Encrypts plaintext using the cipher key k, and nonce iv which MUST be unique for
        the key k. Returns a ciphertext that is the same size as the plaintext.

        The entire ciphertext must be indistinguishable from random if the key is secret.

    DECRYPT(k, iv, ciphertext)
        Decrypts ciphertext using the cipher key k, and nonce iv. Returns the plaintext.


SIGN(privkey, m)         Gibt eine Signatur mit dem privaten Schlüssel privkey über die gegebene Nachricht m zurück.

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

VERIFY(pubkey, m, sig)         Überprüft die Signatur sig gegen den öffentlichen Schlüssel pubkey und die Nachricht m. Gibt         true zurück, wenn die Signatur gültig ist, andernfalls false.

    X25519 public key agreement system. Private keys of 32 bytes, public keys of 32
    bytes, produces outputs of 32 bytes. It has the following
    functions:

    GENERATE_PRIVATE()
        Generates a new private key.

    DERIVE_PUBLIC(privkey)
        Returns the public key corresponding to the given private key.

    DH(privkey, pubkey)
        Generates a shared secret from the given private and public keys.

Es muss auch die folgenden Key Blinding-Operationen unterstützen:

    A cryptographic key derivation function which takes some input key material ikm (which
    should have good entropy but is not required to be a uniformly random string), a salt
    of length 32 bytes, and a context-specific 'info' value, and produces an output
    of n bytes suitable for use as key material.

    Use HKDF as specified in [RFC 5869](https://tools.ietf.org/html/rfc5869), using the HMAC hash function SHA-256
    as specified in [RFC 2104](https://tools.ietf.org/html/rfc2104). This means that SALT_LEN is 32 bytes max.


### Diskussion

GENERATE_ALPHA(data, secret)         Generiere Alpha für diejenigen, die die Daten und ein optionales Geheimnis kennen.         Das Ergebnis muss identisch verteilt sein wie die privaten Schlüssel.

- Eine äußere Schicht, die die notwendigen Klartextinformationen für Speicherung und Abruf enthält.
- Eine mittlere Schicht, die die Client-Authentifizierung verwaltet.
- Eine innere Schicht, die die tatsächlichen LS2-Daten enthält.

BLIND_PRIVKEY(privkey, alpha)         Blendet einen privaten Schlüssel mit einem geheimen Alpha-Wert.

    Layer 0 data + Enc(layer 1 data + Enc(layer 2 data)) + Signature

BLIND_PUBKEY(pubkey, alpha)         Blendet einen öffentlichen Schlüssel mit einem geheimen Alpha.         Für ein gegebenes Schlüsselpaar (privkey, pubkey) gilt folgende Beziehung::

BLIND_PUBKEY(pubkey, alpha) ==             DERIVE_PUBLIC(BLIND_PRIVKEY(privkey, alpha))

#### Layer 0 (outer)

DH     X25519 Public-Key-Vereinbarungssystem. Private Schlüssel von 32 Bytes, öffentliche Schlüssel von 32     Bytes, erzeugt Ausgaben von 32 Bytes. Es hat die folgenden     Funktionen:

    1 byte

    Not actually in header, but part of data covered by signature.
    Take from field in Database Store Message.

GENERATE_PRIVATE()         Generiert einen neuen privaten Schlüssel.

    2 bytes, big endian
    This will always be type 11, identifying a Red25519 blinded key.

DERIVE_PUBLIC(privkey)         Gibt den öffentlichen Schlüssel zurück, der dem angegebenen privaten Schlüssel entspricht.

    Length as implied by sig type

DH(privkey, pubkey)         Generiert ein gemeinsames Geheimnis aus den gegebenen privaten und öffentlichen Schlüsseln.

    4 bytes, big endian

    Seconds since epoch, rolls over in 2106

HKDF(salt, ikm, info, n)     Eine kryptographische Schlüsselableitungsfunktion, die Eingabeschlüsselmaterial ikm (welches gute Entropie haben sollte, aber nicht zwingend eine gleichmäßig zufällige Zeichenkette sein muss), ein salt mit einer Länge von 32 Bytes und einen kontextspezifischen 'info'-Wert entgegennimmt und eine Ausgabe von n Bytes produziert, die als Schlüsselmaterial geeignet ist.

    2 bytes, big endian

    Offset from published timestamp in seconds, 18.2 hours max

Verwende HKDF wie in [RFC 5869](https://tools.ietf.org/html/rfc5869) spezifiziert, unter Verwendung der HMAC-Hash-Funktion SHA-256 wie in [RFC 2104](https://tools.ietf.org/html/rfc2104) spezifiziert. Das bedeutet, dass SALT_LEN maximal 32 Bytes beträgt.

    2 bytes

    Bit order: 15 14 ... 3 2 1 0

    Bit 0: If 0, no offline keys; if 1, offline keys

    Other bits: set to 0 for compatibility with future uses

Das verschlüsselte LS2-Format besteht aus drei verschachtelten Ebenen:

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

Das allgemeine Format sieht folgendermaßen aus::

    2 bytes, big endian

Layer 0 Daten + Enc(Layer 1 Daten + Enc(Layer 2 Daten)) + Signatur

    lenOuterCiphertext bytes

    Encrypted layer 1 data. See below for key derivation and encryption algorithms.

Beachten Sie, dass verschlüsseltes LS2 geblendet ist. Das Destination ist nicht im Header enthalten. Der DHT-Speicherort ist SHA-256(sig type || blinded public key) und wird täglich rotiert.

    Length as implied by sig type of the signing key used

    The signature is of everything above.

    If the flag indicates offline keys, the signature is verified with the transient
    public key. Otherwise, the signature is verified with the blinded public key.


#### Layer 1 (middle)

Verwendet NICHT den oben spezifizierten Standard-LS2-Header.

    1 byte
    
    Bit order: 76543210

    Bit 0: 0 for everybody, 1 for per-client, auth section to follow

    Bits 3-1: Authentication scheme, only if bit 0 is set to 1 for per-client, otherwise 000
              000: DH client authentication (or no per-client authentication)
              001: PSK client authentication

    Bits 7-4: Unused, set to 0 for future compatibility

Typ     1 Byte

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

Nicht tatsächlich im Header, aber Teil der Daten, die von der Signatur abgedeckt werden. Aus dem Feld in der Database Store Message nehmen.

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


Blinded Public Key Sig Type     2 Bytes, Big Endian     Dies wird immer Typ 11 sein und einen Red25519 blinded Key identifizieren.

    Length implied by lenOuterCiphertext (whatever data remains)

    Encrypted layer 2 data. See below for key derivation and encryption algorithms.


#### Layer 2 (inner)

Blinded Public Key     Länge wie vom Signaturtyp impliziert

    1 byte

    Either 3 (LS2) or 7 (Meta LS2)

Published timestamp     4 Bytes, Big Endian

    LeaseSet2 data for the given type.

    Includes the header and signature.


### Neue Verschlüsselungsprobleme

Sekunden seit der Epoche, läuft 2106 über

Expires     2 Bytes, Big-Endian

#### Goals

- Signing Public Key in unblinded destination muss
  Ed25519 (sig type 7) oder Red25519 (sig type 11) sein;
  keine anderen sig types werden unterstützt
- Wenn der Signing Public Key offline ist, muss der transient Signing Public Key ebenfalls Ed25519 sein
- Blinding ist rechnerisch einfach
- Verwendet vorhandene kryptographische Primitive
- Blinded Public Keys können nicht entblindet werden
- Blinded Public Keys müssen auf der Ed25519-Kurve und der prime-order Untergruppe liegen
- Muss den Signing Public Key des destination kennen
  (vollständiges destination nicht erforderlich) um den blinded Public Key abzuleiten
- Bietet optional ein zusätzliches Geheimnis, das zur Ableitung des blinded Public Key erforderlich ist

#### Security

Abweichung vom veröffentlichten Zeitstempel in Sekunden, maximal 18,2 Stunden

#### Definitions

Flags     2 Bytes

    The Ed25519 base point (generator) 2^255 - 19 as in [Ed25519](http://cr.yp.to/papers.html#ed25519)

Bit-Reihenfolge: 15 14 ... 3 2 1 0

    The Ed25519 order 2^252 + 27742317777372353535851937790883648493
    as in [Ed25519](http://cr.yp.to/papers.html#ed25519)

Bit 0: Wenn 0, keine Offline-Schlüssel; wenn 1, Offline-Schlüssel

    Convert a private key to public, as in Ed25519 (mulitply by G)

Andere Bits: auf 0 setzen für Kompatibilität mit zukünftigen Verwendungen

    A 32-byte random number known to those who know the destination.

Transiente Schlüsseldaten     Vorhanden, wenn Flag Offline-Schlüssel anzeigt

    Generate alpha for the current date, for those who know the destination and the secret.
    The result must be identically distributed as Ed25519 private keys.

Expires-Zeitstempel         4 Bytes, Big Endian

    The unblinded 32-byte EdDSA or RedDSA signing private key used to sign the destination

Sekunden seit der Epoche, läuft 2106 über

    The unblinded 32-byte EdDSA or RedDSA signing public key in the destination,
    = DERIVE_PUBLIC(a), as in Ed25519

Transienter Signatur-Typ         2 Bytes, Big Endian

    The blinded 32-byte EdDSA signing private key used to sign the encrypted leaseset
    This is a valid EdDSA private key.

Transiente Signatur-Public-Key         Länge wie durch Signaturtyp impliziert

    The blinded 32-byte EdDSA signing public key in the Destination,
    may be generated with DERIVE_PUBLIC(a'), or from A and alpha.
    This is a valid EdDSA public key, on the curve and on the prime-order subgroup.

Signatur         Länge wie durch den Signature-Typ des blinded public key impliziert

    Flip the order of the input bytes to little-endian

Über Ablaufzeitstempel, transiente Signaturtyp und transienten öffentlichen Schlüssel.

    32 bytes = (LEOS2IP(SHA512(x))) mod B, same as in Ed25519 hash-and-reduce


#### Blinding Calculations

Verifiziert mit dem verblindeten öffentlichen Schlüssel.

lenOuterCiphertext     2 Bytes, Big Endian

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
outerCiphertext     lenOuterCiphertext bytes

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
Verschlüsselte Layer-1-Daten. Siehe unten für Schlüsselableitung und Verschlüsselungsalgorithmen.

```text
// BLIND_PUBKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  A = destination's signing public key
  // Addition using group elements (points on the curve)
  blinded public key = A' = BLIND_PUBKEY(A, alpha) = A + DERIVE_PUBLIC(alpha)
```
Signatur     Länge wie durch den Signaturtyp des verwendeten Signaturschlüssels impliziert

#### Signing

Die Signatur bezieht sich auf alles oben Stehende.

Wenn das Flag Offline-Schlüssel anzeigt, wird die Signatur mit dem temporären öffentlichen Schlüssel verifiziert. Andernfalls wird die Signatur mit dem geblendeten öffentlichen Schlüssel verifiziert.

Flags     1 Byte

Bit-Reihenfolge: 76543210

#### Sign/Verify Calculations

Bit 0: 0 für alle, 1 für pro-Client, Auth-Sektion folgt

Bits 3-1: Authentifizierungsschema, nur wenn Bit 0 auf 1 für pro-Client gesetzt ist, andernfalls 000               000: DH Client-Authentifizierung (oder keine pro-Client-Authentifizierung)               001: PSK Client-Authentifizierung

Bits 7-4: Unbenutzt, auf 0 setzen für zukünftige Kompatibilität

DH-Client-Auth-Daten     Vorhanden, wenn Flag-Bit 0 auf 1 gesetzt ist und Flag-Bits 3-1 auf 000 gesetzt sind.

ephemeralPublicKey         32 Bytes

```text
T = 80 random bytes
  r = H*(T || publickey || message)
  // rest is the same as in Ed25519
```
clients         2 Bytes, Big Endian

```text
// same as in Ed25519
```
### Hinweise

#### Derivation of subcredentials

Anzahl der zu folgenden authClient-Einträge, jeweils 40 Bytes

```text
A = destination's signing public key
  stA = signature type of A, 2 bytes big endian (0x0007 or 0x000b)
  stA' = signature type of A', 2 bytes big endian (0x000b)
  keydata = A || stA || stA'
  credential = H("credential", keydata)
```
authClient         Autorisierungsdaten für einen einzelnen Client.         Siehe unten für den clientspezifischen Autorisierungsalgorithmus.

clientID_i             8 bytes

```text
subcredential = H("subcredential", credential || blindedPublicKey)
```
clientCookie_i             32 Bytes

#### Layer 1 encryption

PSK Client-Auth-Daten     Vorhanden wenn Flag-Bit 0 auf 1 gesetzt ist und Flag-Bits 3-1 auf 001 gesetzt sind.

```text
outerInput = subcredential || publishedTimestamp
```
authSalt         32 Bytes

```text
outerSalt = CSRNG(32)
```
clients         2 Bytes, Big Endian

```text
keys = HKDF(outerSalt, outerInput, "ELS2_L1K", 44)
  outerKey = keys[0:31]
  outerIV = keys[32:43]
```
Anzahl der zu folgenden authClient-Einträge, jeweils 40 Bytes

```text
outerCiphertext = outerSalt || ENCRYPT(outerKey, outerIV, outerPlaintext)
```
#### Layer 1 decryption

authClient         Autorisierungsdaten für einen einzelnen Client.         Siehe unten für den clientspezifischen Autorisierungsalgorithmus.

```text
outerSalt = outerCiphertext[0:31]
```
clientID_i             8 Bytes

```text
outerInput = subcredential || publishedTimestamp
  keys = HKDF(outerSalt, outerInput, "ELS2_L1K", 44)
  outerKey = keys[0:31]
  outerIV = keys[32:43]
```
clientCookie_i             32 Bytes

```text
outerPlaintext = DECRYPT(outerKey, outerIV, outerCiphertext[32:end])
```
#### Layer 2 encryption

innerCiphertext     Länge impliziert durch lenOuterCiphertext (alle verbleibenden Daten)

Verschlüsselte Layer-2-Daten. Siehe unten für Schlüsselableitung und Verschlüsselungsalgorithmen.

```text
innerInput = authCookie || subcredential || publishedTimestamp
  innerSalt = CSRNG(32)
  keys = HKDF(innerSalt, innerInput, "ELS2_L2K", 44)
  innerKey = keys[0:31]
  innerIV = keys[32:43]
  innerCiphertext = innerSalt || ENCRYPT(innerKey, innerIV, innerPlaintext)
```
#### Layer 2 decryption

Typ     1 Byte

Entweder 3 (LS2) oder 7 (Meta LS2)

```text
innerInput = authCookie || subcredential || publishedTimestamp
  innerSalt = innerCiphertext[0:31]
  keys = HKDF(innerSalt, innerInput, "ELS2_L2K", 44)
  innerKey = keys[0:31]
  innerIV = keys[32:43]
  innerPlaintext = DECRYPT(innerKey, innerIV, innerCiphertext[32:end])
```
### Verschlüsselte LS2

Daten     LeaseSet2-Daten für den angegebenen Typ.

Enthält den Header und die Signatur.

#### DH client authorization

Wir verwenden das folgende Schema für Key Blinding, basierend auf Ed25519 und [ZCash RedDSA](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf). Die Re25519-Signaturen erfolgen über die Ed25519-Kurve und verwenden SHA-512 für den Hash.

Wir verwenden nicht [Tor's rend-spec-v3.txt appendix A.2](https://spec.torproject.org/rend-spec-v3), das ähnliche Designziele hat, da dessen geblendete öffentliche Schlüssel möglicherweise außerhalb der Untergruppe mit Primordnung liegen, mit unbekannten Sicherheitsimplikationen.

```text
authCookie = CSRNG(32)
  esk = GENERATE_PRIVATE()
  epk = DERIVE_PUBLIC(esk)
```
Die Sicherheit eines Blinding-Schemas erfordert, dass die Verteilung von Alpha die gleiche ist wie bei den ungeblindeten privaten Schlüsseln. Wenn wir jedoch einen Ed25519 privaten Schlüssel (sig type 7) zu einem Red25519 privaten Schlüssel (sig type 11) blinden, ist die Verteilung unterschiedlich. Um die Anforderungen von [zcash section 4.1.6.1](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf) zu erfüllen, sollte Red25519 (sig type 11) auch für die ungeblindeten Schlüssel verwendet werden, damit "die Kombination aus einem re-randomisierten öffentlichen Schlüssel und Signatur(en) unter diesem Schlüssel nicht den Schlüssel preisgeben, von dem er re-randomisiert wurde." Wir erlauben Typ 7 für bestehende Ziele, empfehlen aber Typ 11 für neue Ziele, die verschlüsselt werden sollen.

```text
sharedSecret = DH(esk, cpk_i)
  authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
  okm = HKDF(epk, authInput, "ELS2_XCA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
  clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
```
B     Der Ed25519 Basispunkt (Generator) 2^255 - 19 wie in [Ed25519](http://cr.yp.to/papers.html#ed25519)

L     Die Ed25519-Ordnung 2^252 + 27742317777372353535851937790883648493     wie in [Ed25519](http://cr.yp.to/papers.html#ed25519)

```text
sharedSecret = DH(csk_i, epk)
  authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
  okm = HKDF(epk, authInput, "ELS2_XCA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
```
DERIVE_PUBLIC(a)     Konvertiert einen privaten Schlüssel in einen öffentlichen, wie bei Ed25519 (Multiplikation mit G)

```text
authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie_i)
```
#### Pre-shared key client authorization

alpha     Eine 32-Byte-Zufallszahl, die denjenigen bekannt ist, die das Ziel kennen.

GENERATE_ALPHA(destination, date, secret)     Generiert Alpha für das aktuelle Datum, für diejenigen, die das Ziel und das Geheimnis kennen.     Das Ergebnis muss identisch verteilt sein wie Ed25519 private keys.

```text
authCookie = CSRNG(32)
  authSalt = CSRNG(32)
```
a     Der ungeblindete 32-Byte EdDSA- oder RedDSA-Signatur-Private-Key, der zur Signierung des Ziels verwendet wird

```text
authInput = psk_i || subcredential || publishedTimestamp
  okm = HKDF(authSalt, authInput, "ELS2PSKA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
  clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
```
A     Der ungeblendete 32-Byte EdDSA oder RedDSA Signatur-Public-Key im Ziel,     = DERIVE_PUBLIC(a), wie in Ed25519

a'     Der geblendete 32-Byte-EdDSA-Signier-Private-Key, der zum Signieren des verschlüsselten leaseSets verwendet wird     Dies ist ein gültiger EdDSA-Private-Key.

```text
authInput = psk_i || subcredential || publishedTimestamp
  okm = HKDF(authSalt, authInput, "ELS2PSKA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
```
A'     Der geblendete 32-Byte EdDSA-Signatur-Public-Key in der Destination,     kann mit DERIVE_PUBLIC(a') generiert werden, oder aus A und alpha.     Dies ist ein gültiger EdDSA-Public-Key, auf der Kurve und in der Primordnung-Untergruppe.

```text
authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie_i)
```
#### Security considerations

LEOS2IP(x)     Kehrt die Reihenfolge der Eingabebytes zu Little-Endian um

H*(x)     32 Bytes = (LEOS2IP(SHA512(x))) mod B, wie in Ed25519 Hash-and-Reduce

Neue geheime Alpha- und Blinded-Keys müssen jeden Tag (UTC) generiert werden. Der geheime Alpha und die Blinded-Keys werden wie folgt berechnet.

GENERATE_ALPHA(destination, date, secret), für alle Parteien:

BLIND_PRIVKEY(), für den Eigentümer, der das LeaseSet veröffentlicht:

BLIND_PUBKEY(), für die Clients, die das leaseSet abrufen:

Beide Methoden zur Berechnung von A' liefern das gleiche Ergebnis, wie erforderlich.

### Definitionen

Das unblinded Leaseset wird mit dem unblinded Ed25519 oder Red25519 Signatur-Privatschlüssel signiert und wie üblich mit dem unblinded Ed25519 oder Red25519 Signatur-Öffentlichschlüssel (Signaturtypen 7 oder 11) verifiziert.

Wenn der öffentliche Signaturschlüssel offline ist, wird das ungeblindete leaseset vom ungeblindeten transienten Ed25519 oder Red25519 privaten Signaturschlüssel signiert und mit dem ungeblindeten Ed25519 oder Red25519 transienten öffentlichen Signaturschlüssel (sig types 7 oder 11) wie üblich verifiziert. Siehe unten für zusätzliche Hinweise zu offline-Schlüsseln für verschlüsselte leasesets.

### Format

Für die Signierung des verschlüsselten leaseSet verwenden wir Red25519, basierend auf [RedDSA](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf), um mit verblindeten Schlüsseln zu signieren und zu verifizieren. Die Red25519-Signaturen basieren auf der Ed25519-Kurve und verwenden SHA-512 für den Hash.

Red25519 ist identisch zu Standard Ed25519, außer wie unten spezifiziert.

Der äußere Teil des verschlüsselten leaseSets verwendet Red25519-Schlüssel und -Signaturen.

### Notes

- Ein Service, der verschlüsselte leaseSets verwendet, würde die verschlüsselte Version an die floodfills veröffentlichen. Jedoch würde er aus Effizienzgründen unverschlüsselte leaseSets an Clients in der umhüllten garlic-Nachricht senden, sobald diese authentifiziert sind (z.B. über eine Whitelist).

- Floodfills können die maximale Größe auf einen angemessenen Wert begrenzen, um Missbrauch zu verhindern.

- Nach der Entschlüsselung sollten mehrere Überprüfungen durchgeführt werden, einschließlich der Kontrolle, dass
  der innere Zeitstempel und das Ablaufdatum mit denen auf der obersten Ebene übereinstimmen.

- ChaCha20 wurde anstelle von AES gewählt. Während die Geschwindigkeiten ähnlich sind, wenn AES-Hardware-Unterstützung verfügbar ist, ist ChaCha20 2,5-3x schneller, wenn keine AES-Hardware-Unterstützung verfügbar ist, wie beispielsweise bei günstigeren ARM-Geräten.

- Uns ist die Geschwindigkeit nicht wichtig genug, um keyed BLAKE2b zu verwenden. Es hat eine Ausgabegröße, die groß genug ist, um das größte n zu unterstützen, das wir benötigen (oder wir können es einmal pro gewünschtem Schlüssel mit einem Zählerargument aufrufen). BLAKE2b ist viel schneller als SHA-256, und keyed-BLAKE2b würde die Gesamtzahl der Hash-Funktionsaufrufe reduzieren.
  Siehe jedoch Proposal 148, wo vorgeschlagen wird, dass wir aus anderen Gründen zu BLAKE2b wechseln.
  Siehe [Secure key derivation performance](https://www.lvh.io/posts/secure-key-derivation-performance.html).

### Meta LS2

Red25519 ist fast identisch mit Ed25519. Es gibt zwei Unterschiede:

Red25519 private keys werden aus Zufallszahlen generiert und müssen dann mod L reduziert werden, wobei L oben definiert ist. Ed25519 private keys werden aus Zufallszahlen generiert und dann mit bitweiser Maskierung auf die Bytes 0 und 31 "geklammert". Dies wird bei Red25519 nicht gemacht. Die oben definierten Funktionen GENERATE_ALPHA() und BLIND_PRIVKEY() generieren ordnungsgemäße Red25519 private keys unter Verwendung von mod L.

In Red25519 verwendet die Berechnung von r für das Signieren zusätzliche Zufallsdaten und nutzt den öffentlichen Schlüsselwert anstelle des Hashs des privaten Schlüssels. Aufgrund der Zufallsdaten ist jede Red25519-Signatur unterschiedlich, selbst beim Signieren derselben Daten mit demselben Schlüssel.

Signierung:

Verifikation:

Als Teil des Blinding-Prozesses müssen wir sicherstellen, dass ein verschlüsseltes LS2 nur von jemandem entschlüsselt werden kann, der den entsprechenden öffentlichen Signaturschlüssel der Destination kennt. Die vollständige Destination ist nicht erforderlich. Um dies zu erreichen, leiten wir eine Berechtigung vom öffentlichen Signaturschlüssel ab:

Der Personalisierungsstring stellt sicher, dass die Zugangsdaten nicht mit einem Hash kollidieren, der als DHT-Lookup-Schlüssel verwendet wird, wie beispielsweise dem einfachen Destination-Hash.

Für einen gegebenen blinded key können wir dann eine subcredential ableiten:

Der Subcredential wird in die unten beschriebenen Schlüsselableitungsprozesse einbezogen, wodurch diese Schlüssel an die Kenntnis des öffentlichen Signaturschlüssels des Destination gebunden werden.

Zuerst wird die Eingabe für den Schlüsselableitungsprozess vorbereitet:

    Standard LS flag (1)
Als Nächstes wird ein zufälliges Salt generiert:

    Meta LS2 type (7)
Dann wird der Schlüssel abgeleitet, der zur Verschlüsselung von Schicht 1 verwendet wird:

    Hash of destination
    This hash is then used to generate the daily "routing key", as in LS1
Schließlich wird der Layer 1 Klartext verschlüsselt und serialisiert:

    Hours. Max 18.2 hours (65535 seconds)
Das Salt wird aus dem Layer-1-Chiffretext geparst:

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
Dann wird der Schlüssel zur Verschlüsselung von Schicht 1 abgeleitet:

### Ableitung des Blinding-Schlüssels

- Ein verteilter Dienst, der dies verwendet, hätte einen oder mehrere "Master" mit dem privaten Schlüssel der Dienst-Destination. Diese würden (außerhalb des Bands) die aktuelle Liste der aktiven Destinations bestimmen und das Meta LS2 veröffentlichen. Für Redundanz könnten mehrere Master das Meta LS2 multihomen (d.h. gleichzeitig veröffentlichen).

- Ein verteilter Dienst könnte mit einem einzigen Destination beginnen oder altes Multihoming verwenden, dann zu einem Meta LS2 übergehn. Eine Standard-LS-Suche könnte eine LS, LS2 oder Meta LS2 zurückgeben.

- Wenn ein Service eine Meta LS2 verwendet, hat er keine Tunnel (leases).

### Service Record

Schließlich wird der Layer-1-Chiffretext entschlüsselt:

Wenn Client-Autorisierung aktiviert ist, wird ``authCookie`` wie unten beschrieben berechnet. Wenn Client-Autorisierung deaktiviert ist, ist ``authCookie`` das Byte-Array mit der Länge null.

Die Verschlüsselung läuft ähnlich wie bei Schicht 1 ab:

    n/a, see Service List
Wenn Client-Autorisierung aktiviert ist, wird ``authCookie`` wie unten beschrieben berechnet. Wenn Client-Autorisierung deaktiviert ist, ist ``authCookie`` das Byte-Array mit der Länge Null.

    Service Record type (9)
Die Entschlüsselung läuft ähnlich wie bei Schicht 1 ab:

    Hash of service name
    This hash is then used to generate the daily "routing key", as in LS1
Wenn Client-Autorisierung für eine Destination aktiviert ist, verwaltet der Server eine Liste von Clients, die er berechtigt, die verschlüsselten LS2-Daten zu entschlüsseln. Die pro Client gespeicherten Daten hängen vom Autorisierungsmechanismus ab und umfassen eine Form von Schlüsselmaterial, das jeder Client generiert und über einen sicheren Out-of-Band-Mechanismus an den Server sendet.

    Hours. Max 18.2 hours (65535 seconds)
Es gibt zwei Alternativen für die Implementierung einer clientspezifischen Autorisierung:

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
### Notes

- Wenn expires nur Nullen enthält, sollte der floodfill den Datensatz widerrufen und ihn nicht mehr in die Serviceliste einbeziehen.

- Speicherung: Der Floodfill kann die Speicherung dieser Datensätze streng drosseln und
  die Anzahl der pro Hash gespeicherten Datensätze sowie deren Ablaufzeit begrenzen. Eine Whitelist
  von Hashes kann ebenfalls verwendet werden.

- Jeder andere netDb-Typ mit demselben Hash hat Vorrang, daher kann ein Service-Datensatz niemals ein LS/RI überschreiben, aber ein LS/RI wird alle Service-Datensätze mit diesem Hash überschreiben.

### Service List

Jeder Client generiert ein DH-Schlüsselpaar ``[csk_i, cpk_i]`` und sendet den öffentlichen Schlüssel ``cpk_i`` an den Server.

Serververarbeitung
^^^^^^^^^^^^^^^^^

Der Server generiert ein neues ``authCookie`` und ein ephemeres DH-Schlüsselpaar:

Dann verschlüsselt der Server für jeden autorisierten Client das ``authCookie`` mit dessen öffentlichem Schlüssel:

Der Server platziert jedes ``[clientID_i, clientCookie_i]`` Tupel in Schicht 1 des verschlüsselten LS2, zusammen mit ``epk``.

Client-Verarbeitung
^^^^^^^^^^^^^^^^^

Der Client verwendet seinen privaten Schlüssel, um seine erwartete Client-Kennung ``clientID_i``, den Verschlüsselungsschlüssel ``clientKey_i`` und den Verschlüsselungs-IV ``clientIV_i`` abzuleiten:

Dann durchsucht der Client die Autorisierungsdaten der Schicht 1 nach einem Eintrag, der ``clientID_i`` enthält. Falls ein passender Eintrag existiert, entschlüsselt der Client diesen, um ``authCookie`` zu erhalten:

    Service List lookup type (11)
Jeder Client generiert einen geheimen 32-Byte-Schlüssel ``psk_i`` und sendet ihn an den Server. Alternativ kann der Server den geheimen Schlüssel generieren und an einen oder mehrere Clients senden.

    Service List type (11)
Serververarbeitung
^^^^^^^^^^^^^^^^^

Der Server generiert einen neuen ``authCookie`` und Salt:

    Hash of service name
    This hash is then used to generate the daily "routing key", as in LS1
Dann verschlüsselt der Server für jeden autorisierten Client das ``authCookie`` mit dessen vorgeteiltem Schlüssel:

    Hours, not specified in the list itself, up to local policy
Der Server platziert jedes ``[clientID_i, clientCookie_i]``-Tupel in Schicht 1 der verschlüsselten LS2, zusammen mit ``authSalt``.

    Nobody, never sent to floodfill, never flooded.

### Format

Client-Verarbeitung
^^^^^^^^^^^^^^^^^

Der Client verwendet seinen Pre-Shared-Key, um seine erwartete Client-Kennung ``clientID_i``, Verschlüsselungsschlüssel ``clientKey_i`` und Verschlüsselungs-IV ``clientIV_i`` abzuleiten:

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
Dann durchsucht der Client die Layer-1-Autorisierungsdaten nach einem Eintrag, der ``clientID_i`` enthält. Falls ein passender Eintrag existiert, entschlüsselt der Client diesen, um ``authCookie`` zu erhalten:

- den Hash des Servicenamens voranstellen
- den Hash des Erstellers entfernen
- Signatur des geänderten Inhalts überprüfen

Beide oben genannten Client-Autorisierungsmechanismen bieten Privatsphäre für die Client-Mitgliedschaft. Eine Entität, die nur die Destination kennt, kann sehen, wie viele Clients zu einem beliebigen Zeitpunkt abonniert sind, kann aber nicht verfolgen, welche Clients hinzugefügt oder widerrufen werden.

- Destination abrufen
- Signatur prüfen von (veröffentlichter Zeitstempel + läuft ab + Flags + Port + Hash des
  Service-Namens)

Server SOLLTEN die Reihenfolge der Clients jedes Mal randomisieren, wenn sie ein verschlüsseltes LS2 generieren, um zu verhindern, dass Clients ihre Position in der Liste erfahren und daraus schließen können, wann andere Clients hinzugefügt oder widerrufen wurden.

- Destination abrufen
- Signatur prüfen von (veröffentlichter Zeitstempel + 4 Null-Bytes + Flags + Port + Hash
  des Dienstnamens)

### Notes

- Wir verwenden die Signaturlänge anstelle des Signaturtyps, damit wir unbekannte Signaturtypen unterstützen können.

- Es gibt kein Ablaufdatum für eine Service-Liste, Empfänger können ihre eigene
  Entscheidung basierend auf der Richtlinie oder dem Ablauf der einzelnen Einträge treffen.

- Service Lists werden nicht geflutet, nur einzelne Service Records. Jeder
  floodfill erstellt, signiert und speichert eine Service List zwischen. Der floodfill nutzt seine
  eigene Richtlinie für die Cache-Zeit und die maximale Anzahl von Service- und Widerruf-Records.

## Common Structures Spec Changes Required

### Verschlüsselung und Verarbeitung

Ein Server KANN wählen, die Anzahl der abonnierten Clients zu verbergen, indem er zufällige Einträge in die Liste der Autorisierungsdaten einfügt.

### New Intermediate Structures

Vorteile der DH-Client-Autorisierung
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Die Sicherheit des Schemas hängt nicht ausschließlich vom Out-of-Band-Austausch des Client-Schlüsselmaterials ab. Der private Schlüssel des Clients muss niemals sein Gerät verlassen, sodass ein Angreifer, der den Out-of-Band-Austausch abfangen kann, aber den DH-Algorithmus nicht brechen kann, weder das verschlüsselte LS2 entschlüsseln noch bestimmen kann, wie lange dem Client Zugang gewährt wird.

### New NetDB Types

Nachteile der DH-Client-Autorisierung
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Erfordert N + 1 DH-Operationen auf der Serverseite für N Clients.
- Erfordert eine DH-Operation auf der Clientseite.
- Erfordert, dass der Client den geheimen Schlüssel generiert.

### New Signature Type

Vorteile der PSK-Client-Autorisierung
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Erfordert keine DH-Operationen.
- Ermöglicht es dem Server, den geheimen Schlüssel zu generieren.
- Ermöglicht es dem Server, denselben Schlüssel mit mehreren Clients zu teilen, falls gewünscht.

## Encryption Spec Changes Required

Nachteile der PSK-Client-Autorisierung
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Die Sicherheit des Schemas hängt kritisch vom Out-of-Band-Austausch des Client-Schlüsselmaterials ab. Ein Angreifer, der den Austausch für einen bestimmten Client abfängt, kann alle nachfolgenden verschlüsselten LS2 entschlüsseln, für die dieser Client autorisiert ist, sowie feststellen, wann der Zugang des Clients widerrufen wird.

## I2NP Changes Required

Siehe Vorschlag 149.

### Database Lookup Message

Sie können ein verschlüsseltes LS2 nicht für BitTorrent verwenden, da die kompakten Announce-Antworten 32 Bytes groß sind. Die 32 Bytes enthalten nur den Hash. Es gibt keinen Platz für einen Hinweis, dass das leaseSet verschlüsselt ist, oder für die Signaturtypen.

### Changes

```
Flags byte: Lookup type field, currently bits 3-2, expands to bits 4-2.
  Lookup type 0x04 is defined as the service list lookup.

  Add note: Service list loookup may only be sent to floodfills with a minimum version.
  Minimum version is 0.9.38.
```
### Pro-Client-Autorisierung

Für verschlüsselte LeaseSets mit Offline-Schlüsseln müssen die geblendeten privaten Schlüssel ebenfalls offline generiert werden, einer für jeden Tag.

### Changes

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
## I2CP Changes Required

### I2CP Options

Da der optionale Offline-Signaturblock im Klartext-Teil des verschlüsselten leaseSets steht, könnte jeder, der die floodfills durchsucht, dies nutzen, um das leaseSet (aber nicht entschlüsseln) über mehrere Tage zu verfolgen. Um dies zu verhindern, sollte der Besitzer der Schlüssel auch täglich neue transiente Schlüssel generieren. Sowohl die transienten als auch die geblendeten Schlüssel können im Voraus generiert und dem Router in einem Stapel übermittelt werden.

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
Es ist kein Dateiformat in diesem Vorschlag definiert, um mehrere transiente und geblendete Schlüssel zu verpacken und sie dem Client oder Router zur Verfügung zu stellen. Es ist keine I2CP-Protokollerweiterung in diesem Vorschlag definiert, um verschlüsselte leaseSets mit Offline-Schlüsseln zu unterstützen.

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
### Session Config

Dies wird verwendet, um Multihoming zu ersetzen. Wie jedes leaseSet wird dies vom Ersteller signiert. Dies ist eine authentifizierte Liste von Ziel-Hashes.

### Verschlüsselte LS mit Base 32 Adressen

Das Meta LS2 ist die Spitze und möglicherweise Zwischenknoten einer Baumstruktur. Es enthält eine Anzahl von Einträgen, die jeweils auf ein LS, LS2 oder ein anderes Meta LS2 zeigen, um massives Multihoming zu unterstützen. Ein Meta LS2 kann eine Mischung aus LS-, LS2- und Meta LS2-Einträgen enthalten. Die Blätter des Baums sind immer ein LS oder LS2. Der Baum ist ein DAG (gerichteter azyklischer Graph); Schleifen sind verboten; Clients, die Lookups durchführen, müssen Schleifen erkennen und sich weigern, diesen zu folgen.

### Verschlüsselte LS mit Offline-Schlüsseln

Eine Meta LS2 kann eine deutlich längere Ablaufzeit haben als ein Standard LS oder LS2. Die oberste Ebene kann eine Ablaufzeit haben, die mehrere Stunden nach dem Veröffentlichungsdatum liegt. Die maximale Ablaufzeit wird von floodfills und Clients durchgesetzt und ist noch zu bestimmen.

### Anmerkungen

Der Anwendungsfall für Meta LS2 ist massives Multihoming, aber ohne mehr Schutz vor Korrelation von Routern zu LeaseSets (zum Zeitpunkt des Router-Neustarts) als derzeit mit LS oder LS2 bereitgestellt wird. Dies entspricht dem "Facebook"-Anwendungsfall, der wahrscheinlich keinen Korrelationsschutz benötigt. Dieser Anwendungsfall benötigt wahrscheinlich Offline-Schlüssel, die im Standard-Header an jedem Knoten des Baums bereitgestellt werden.

### Meta LS2

- Damit der Router den Store-Typ parsen kann, muss der Typ in der Nachricht enthalten sein,
  es sei denn, er wird dem Router vorab in der Session-Konfiguration übergeben.
  Für gemeinsamen Parsing-Code ist es einfacher, ihn in der Nachricht selbst zu haben.

- Damit der Router den Typ und die Länge des privaten Schlüssels kennt,
  muss er nach dem Lease Set stehen, es sei denn, der Parser kennt den Typ bereits
  in der Session-Konfiguration.
  Für gemeinsamen Parsing-Code ist es einfacher, ihn aus der Nachricht selbst zu kennen.

- Der private Signaturschlüssel, der zuvor für Widerruf definiert und ungenutzt war,
  ist in LS2 nicht vorhanden.

### Format

Das Backend-Protokoll für die Koordination zwischen den Leaf-Routern, Zwischen- und Master-Meta-LS-Signierern ist hier nicht spezifiziert. Die Anforderungen sind extrem einfach - nur überprüfen, dass der Peer erreichbar ist, und alle paar Stunden ein neues LS veröffentlichen. Die einzige Komplexität besteht darin, neue Publisher für die Top-Level- oder Intermediate-Level-Meta-LSes bei Ausfällen auszuwählen.

### Hinweise

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
### Service-Datensatz

- Die minimale Router-Version ist 0.9.39.
- Eine vorläufige Version mit Nachrichtentyp 40 war in 0.9.38 verfügbar, aber das Format wurde geändert.
  Typ 40 ist aufgegeben und wird nicht unterstützt.

### Format

- Weitere Änderungen sind erforderlich, um verschlüsselte und Meta-LS zu unterstützen.

### Hinweise

Mix-and-match leasesets, bei denen Leases von mehreren Routern kombiniert, signiert und in einem einzigen leaseset veröffentlicht werden, sind in Vorschlag 140, "invisible multihoming", dokumentiert. Dieser Vorschlag ist in seiner jetzigen Form nicht umsetzbar, da Streaming-Verbindungen nicht an einen einzigen Router "gebunden" wären, siehe http://zzz.i2p/topics/2335 .

### Dienstliste

- Der Router muss wissen, ob ein Ziel geblendet ist.
  Falls es geblendet ist und eine geheime oder pro-Client-Authentifizierung verwendet,
  benötigt er diese Informationen ebenfalls.

- Ein Host Lookup einer neuen b32-Adresse im Format ("b33")
  teilt dem router mit, dass die Adresse geblindet ist, aber es gibt keinen Mechanismus,
  um den geheimen oder privaten Schlüssel an den router in der Host Lookup-Nachricht zu übertragen.
  Obwohl wir die Host Lookup-Nachricht erweitern könnten, um diese Informationen hinzuzufügen,
  ist es sauberer, eine neue Nachricht zu definieren.

- Wir benötigen eine programmatische Möglichkeit für den Client, es dem Router mitzuteilen.
  Andernfalls müsste der Benutzer jedes Ziel manuell konfigurieren.

### Format

Das Backend-Protokoll und die Interaktion mit Router- und Client-Interna wären für unsichtbares Multihoming recht komplex.

Um eine Überlastung des floodfill für das Top-Level Meta LS zu vermeiden, sollte die Ablaufzeit mindestens mehrere Stunden betragen. Clients müssen das Top-Level Meta LS zwischenspeichern und es bei Neustarts persistent halten, falls es noch nicht abgelaufen ist.

### Notizen

Wir müssen einen Algorithmus für Clients definieren, um den Baum zu durchlaufen, einschließlich Fallbacks, damit die Nutzung verteilt wird. Eine Funktion aus Hash-Distanz, Kosten und Zufälligkeit. Wenn ein Knoten sowohl LS oder LS2 als auch Meta LS hat, müssen wir wissen, wann es erlaubt ist, diese leasesets zu verwenden und wann der Baum weiter durchlaufen werden soll.

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
### Schlüsselzertifikate

- Mindest-Router-Version ist 0.9.43

### Neue Zwischenstrukturen

### Neue NetDB-Typen

Nachschlagen mit     Standard LS Flag (1) Speichern mit     Meta LS2 Typ (7) Speichern bei     Hash des Ziels     Dieser Hash wird dann verwendet, um den täglichen "routing key" zu generieren, wie bei LS1 Typische Ablaufzeit     Stunden. Max 18,2 Stunden (65535 Sekunden) Veröffentlicht von     "Master" Destination oder Koordinator, oder Zwischenkoordinatoren

```
2: Lookup password required
   3: Private key required
   4: Lookup password and private key required
   5: Leaseset decryption failure
```
Flags und Eigenschaften: für zukünftige Verwendung

### Neuer Signatur-Typ

Dies ist ein individueller Datensatz, der besagt, dass eine Destination an einem Service teilnimmt. Er wird vom Teilnehmer an den floodfill gesendet. Er wird niemals einzeln von einem floodfill gesendet, sondern nur als Teil einer Service List. Der Service Record wird auch verwendet, um die Teilnahme an einem Service zu widerrufen, indem die Ablaufzeit auf null gesetzt wird.

### Justification

Dies ist kein LS2, aber es verwendet das Standard-LS2-Header- und Signaturformat.

Lookup with     n/a, siehe Service List Store with     Service Record type (9) Store at     Hash des Servicenamen     Dieser Hash wird dann verwendet, um den täglichen "routing key" zu generieren, wie in LS1 Typical expiration     Stunden. Max 18,2 Stunden (65535 Sekunden) Published by     Destination

### Usage

Das ist nichts wie ein LS2 und verwendet ein anderes Format.

Die Serviceliste wird vom Floodfill erstellt und signiert. Sie ist nicht authentifiziert, da jeder einem Service beitreten kann, indem er einen Service Record an einen Floodfill veröffentlicht.

Eine Service-Liste enthält kurze Service-Datensätze, keine vollständigen Service-Datensätze. Diese enthalten Signaturen, aber nur Hashes, keine vollständigen Ziele, daher können sie ohne das vollständige Ziel nicht verifiziert werden.

### Database Lookup Nachricht

Die Sicherheit, falls vorhanden, und Wünschbarkeit von Service-Listen ist noch zu bestimmen. Floodfills könnten Veröffentlichungen und Lookups auf eine Whitelist von Services beschränken, aber diese Whitelist kann je nach Implementierung oder Betreiber-Präferenz variieren. Es ist möglicherweise nicht möglich, einen Konsens über eine gemeinsame, grundlegende Whitelist zwischen verschiedenen Implementierungen zu erreichen.

### Änderungen

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
### Database Store Message

Wenn der Servicename im obigen Service-Datensatz enthalten ist, können floodfill-Betreiber Einwände erheben; wenn nur der Hash enthalten ist, gibt es keine Verifizierung, und ein Service-Datensatz könnte sich vor jedem anderen netDb-Typ „einschleichen" und im floodfill gespeichert werden.

### Änderungen

Nachschlagen mit     Service List Nachschlageart (11) Speichern mit     Service List Typ (11) Speichern bei     Hash des Servicenamens     Dieser Hash wird dann verwendet, um den täglichen "Routing-Schlüssel" zu generieren, wie in LS1 Typische Ablaufzeit     Stunden, nicht in der Liste selbst angegeben, abhängig von lokaler Richtlinie Veröffentlicht von     Niemand, nie an floodfill gesendet, nie geflutet.

## Private Key File Changes Required

Verwendet NICHT den oben spezifizierten Standard-LS2-Header.

Um die Signatur der Service-Liste zu verifizieren:

### Changes

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
### I2CP-Optionen

Um die Signatur jedes Short Service Records zu verifizieren:

```
-d days              (specify expiration in days of offline sig, default 365)
      -o offlinedestfile   (generate the online key file,
                            using the offline key file specified)
      -r sigtype           (specify sig type of transient key, default Ed25519)
```
## Streaming Changes Required

Um die Signatur jedes Revocation Records zu verifizieren:

### Session-Konfiguration

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
### Request Leaseset Message

- Alternative ist, einfach ein Flag hinzuzufügen und den transient public key über I2CP abzurufen
  (Siehe Host Lookup / Host Reply Message Abschnitte oben)

## Standard LS2 Header

Außerhalb des Geltungsbereichs dieses Vorschlags. Zu den ECIES-Vorschlägen 144 und 145 hinzufügen.

### Request Variable Leaseset Nachricht

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
### Leaseset2-Nachricht erstellen

- Alternative ist es, nur ein Flag hinzuzufügen und den transienten öffentlichen Schlüssel über I2CP abzurufen
  (Siehe Host Lookup / Host Reply Message Abschnitte oben)
- Welche anderen Optionen sollten wir jetzt hinzufügen, da wir Flag-Bytes haben?

## SAM V3 Changes Required

Neue Strukturen für Lease2, MetaLease, LeaseSet2Header und OfflineSignature hinzufügen. Wirksam ab Version 0.9.38.

### Begründung

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
Fügen Sie Strukturen für jeden neuen Leaseset-Typ hinzu, die von oben übernommen wurden. Für LeaseSet2, EncryptedLeaseSet und MetaLeaseSet, gültig ab Version 0.9.38. Für Service Record und Service List, vorläufig und nicht terminiert.

Füge RedDSA_SHA512_Ed25519 Typ 11 hinzu. Öffentlicher Schlüssel ist 32 Bytes; privater Schlüssel ist 32 Bytes; Hash ist 64 Bytes; Signatur ist 64 Bytes.

Außerhalb des Geltungsbereichs dieses Vorschlags. Siehe Vorschläge 144 und 145.

### Nachrichtentyp

Hinweis hinzufügen: LS2 kann nur an floodfills mit einer Mindestversion veröffentlicht werden.

Fügen Sie den Service-Listen-Lookup-Typ hinzu.

## BOB Changes Required

Fügen Sie alle neuen Store-Typen hinzu.

## Publishing, Migration, Compatibility

Neue Optionen, die routerseitig interpretiert werden, gesendet in SessionConfig Mapping:

Neue clientseitig interpretierte Optionen:

Beachten Sie, dass für Offline-Signaturen die Optionen i2cp.leaseSetOfflineExpiration, i2cp.leaseSetTransientPublicKey und i2cp.leaseSetOfflineSignature erforderlich sind, und die Signatur erfolgt durch den temporären privaten Signaturschlüssel.

Router zum Client. Keine Änderungen. Die leases werden mit 8-Byte-Zeitstempeln gesendet, auch wenn das zurückgegebene leaseset ein LS2 mit 4-Byte-Zeitstempeln sein wird. Beachten Sie, dass die Antwort eine Create Leaseset oder Create Leaseset2 Message sein kann.

Router zu Client. Keine Änderungen. Die Leases werden mit 8-Byte-Zeitstempeln gesendet, auch wenn das zurückgegebene leaseSet ein LS2 mit 4-Byte-Zeitstempeln ist. Beachten Sie, dass die Antwort eine Create Leaseset- oder Create Leaseset2-Nachricht sein kann.

## Rollout

Client zu Router. Neue Nachricht, die anstelle der Create Leaseset Message verwendet werden soll.

Der Nachrichtentyp für die Create Leaseset2 Message ist 41.

Client zu Router. Neue Nachricht.

## Neue DatabaseEntry-Typen

Bevor ein Client eine Nachricht an ein blinded destination sendet, muss er entweder die "b33" in einer Host Lookup-Nachricht nachschlagen oder eine Blinding Info-Nachricht senden. Wenn das blinded destination ein Geheimnis oder eine clientspezifische Authentifizierung erfordert, muss der Client eine Blinding Info-Nachricht senden.
