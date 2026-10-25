---
title: "ECIES-X25519-AEAD-Ratchet"
description: "Elliptic Curve Integrated Encryption Scheme für I2P Ende-zu-Ende-Verschlüsselung"
slug: "ecies"
aliases:
  - "/de/docs/specs/ecies-x25519-aead-ratchet"
  - "/de/docs/specs/ecies-x25519-aead-ratchet/"
category: "Protokolle"
lastUpdated: "2025-06"
accurateFor: "0.9.67"
---

## Hinweis

Netzwerk-Bereitstellung abgeschlossen. Unterliegt geringfügigen Revisionen. Siehe [Prop144](/proposals/144-ecies-x25519/) für den ursprünglichen Vorschlag, einschließlich Hintergrunddiskussion und zusätzlichen Informationen.

Die folgenden Funktionen sind seit Version 0.9.66 nicht implementiert:

- MessageNumbers-, Options- und Termination-Blöcke
- Protokollschicht-Antworten
- Null-statischer Schlüssel
- Multicast

Für die MLKEM PQ Hybrid-Version dieses Protokolls, siehe [ECIES-HYBRID](/docs/specs/ecies-hybrid/).

## Übersicht

Dies ist das neue Ende-zu-Ende-Verschlüsselungsprotokoll, das ElGamal/AES+SessionTags [ElG-AES](/docs/specs/elgamal-aes/) ersetzen soll.

Es basiert auf folgenden vorherigen Arbeiten:

- Common structures Spezifikation [Common](/docs/specs/common-structures/)
- [I2NP](/docs/specs/i2np/) Spezifikation einschließlich LS2
- ElGamal/AES+Session Tags [Elg-AES](/docs/specs/elgamal-aes/)
- <http://zzz.i2p/topics/1768> Übersicht über neue asymmetrische Kryptographie
- Low-Level-Krypto-Übersicht [CRYPTO-ELG](/docs/specs/cryptography/#elgamal)
- ECIES <http://zzz.i2p/topics/2418>
- [NTCP2](/docs/specs/ntcp2/) [Prop111](/proposals/111-ntcp2/)
- 123 Neue netDB Einträge
- 142 Neue Krypto-Vorlage
- [Noise](https://noiseprotocol.org/noise.html) Protokoll
- [Signal](https://signal.org/docs/specifications/doubleratchet/) Double-Ratchet-Algorithmus

Es unterstützt neue Verschlüsselung für End-zu-End-, Destination-zu-Destination-Kommunikation.

Das Design verwendet einen Noise-Handshake und eine Datenphase, die Signals Double Ratchet integriert.

Alle Verweise auf Signal und Noise in dieser Spezifikation dienen nur der Hintergrundinformation. Kenntnisse der Signal- und Noise-Protokolle sind nicht erforderlich, um diese Spezifikation zu verstehen oder zu implementieren.

Diese Spezifikation wird ab Version 0.9.46 unterstützt.

## Spezifikation

Das Design verwendet einen Noise-Handshake und eine Datenphase, die Signals Double Ratchet einbezieht.

### Zusammenfassung des kryptographischen Designs

Es gibt fünf Teile des Protokolls, die neu gestaltet werden müssen:

- 1\) Die neuen und bestehenden Session-Container-Formate werden durch
  neue Formate ersetzt.
- 2\) ElGamal (256 Byte öffentliche Schlüssel, 128 Byte private Schlüssel) wird
  durch ECIES-X25519 (32 Byte öffentliche und private Schlüssel) ersetzt
- 3\) AES wird durch AEAD_ChaCha20_Poly1305 (im Folgenden als
  ChaChaPoly abgekürzt) ersetzt
- 4\) SessionTags werden durch Ratchets ersetzt, welche im Wesentlichen ein
  kryptographischer, synchronisierter PRNG sind.
- 5\) Die AES-Payload, wie sie in der ElGamal/AES+SessionTags-
  Spezifikation definiert ist, wird durch ein Blockformat ähnlich dem in
  NTCP2 ersetzt.

Jede der fünf Änderungen hat ihren eigenen Abschnitt unten.

### Krypto-Typ

Der Krypto-Typ (verwendet im LS2) ist 4. Dies zeigt einen Little-Endian 32-Byte X25519 öffentlichen Schlüssel und das hier spezifizierte End-to-End-Protokoll an.

Kryptotyp 0 ist ElGamal. Kryptotypen 1-3 sind für ECIES-ECDH-AES-SessionTag reserviert, siehe Vorschlag 145 [Prop145](/proposals/145-ecies-ecdh-aes/).

### Noise Protocol Framework

Dieses Protokoll stellt die Anforderungen basierend auf dem Noise Protocol Framework [NOISE](https://noiseprotocol.org/noise.html) (Revision 34, 2018-07-11) bereit. Noise hat ähnliche Eigenschaften wie das Station-To-Station-Protokoll [STS](https://en.wikipedia.org/wiki/Station-to-Station_protocol), welches die Grundlage für das [SSU](/docs/transport/ssu/)-Protokoll ist. In der Noise-Terminologie ist Alice der Initiator und Bob der Responder.

Diese Spezifikation basiert auf dem Noise-Protokoll Noise_IK_25519_ChaChaPoly_SHA256. (Der tatsächliche Bezeichner für die anfängliche Schlüsselableitungsfunktion ist "Noise_IKelg2_25519_ChaChaPoly_SHA256", um I2P-Erweiterungen anzuzeigen - siehe Abschnitt KDF 1 unten) Dieses Noise-Protokoll verwendet die folgenden Primitive:

- Interactive Handshake Pattern: IK Alice überträgt sofort ihren
  statischen Schlüssel an Bob (I) Alice kennt bereits Bobs statischen Schlüssel (K)
- One-Way Handshake Pattern: N Alice überträgt ihren statischen Schlüssel nicht an
  Bob (N)
- DH-Funktion: X25519 X25519 DH mit einer Schlüssellänge von 32 Bytes wie
  spezifiziert in [RFC-7748](https://tools.ietf.org/html/rfc7748).
- Cipher-Funktion: ChaChaPoly AEAD_CHACHA20_POLY1305 wie spezifiziert in
  [RFC-7539](https://tools.ietf.org/html/rfc7539) Abschnitt 2.8. 12-Byte-Nonce, mit
  den ersten 4 Bytes auf null gesetzt. Identisch zu dem in
  [NTCP2](/docs/specs/ntcp2/).
- Hash-Funktion: SHA256 Standard 32-Byte-Hash, bereits umfassend
  in I2P verwendet.

#### Ergänzungen zum Framework

Diese Spezifikation definiert die folgenden Erweiterungen für Noise_IK_25519_ChaChaPoly_SHA256. Diese folgen im Allgemeinen den Richtlinien in [NOISE](https://noiseprotocol.org/noise.html) Abschnitt 13.

1)  Klartext-Ephemeralschlüssel werden kodiert mit

    [Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf).
2) Die Antwort wird mit einem Klartext-Tag vorangestellt. 3) Das Payload-Format ist für die Nachrichten 1, 2 und die Datenphase definiert.

    Of course, this is not defined in Noise.

Alle Nachrichten enthalten einen [I2NP](/docs/specs/i2np/) Garlic Message Header. Die Datenphase verwendet eine Verschlüsselung, die ähnlich, aber nicht kompatibel mit der Noise-Datenphase ist.

### Handshake-Muster

Handshakes verwenden [Noise](https://noiseprotocol.org/noise.html) Handshake-Muster.

Die folgende Buchstabenzuordnung wird verwendet:

- e = einmaliger ephemerer Schlüssel
- s = statischer Schlüssel
- p = Nachrichtennutzlast

Einmalige und Unbound-Sitzungen sind ähnlich dem Noise N-Muster.

```
<- s
...
e es p ->
```
Bound sessions sind ähnlich dem Noise IK-Muster.

```
<- s
...
e es s ss p ->
<- tag e ee se
<- p
p ->
```
#### Sicherheitseigenschaften

Mit der Noise-Terminologie ist die Etablierungs- und Datensequenz wie folgt: (Payload Security Properties von [Noise](https://noiseprotocol.org/noise.html))

```
IK(s, rs):           Authentication   Confidentiality
  <- s
  ...
  -> e, es, s, ss           1                2
  <- e, ee, se              2                4
  ->                        2                5
  <-                        2                5
```
#### Unterschiede zu XK

IK-Handshakes haben mehrere Unterschiede zu XK-Handshakes, die in [NTCP2](/docs/specs/ntcp2/) und [SSU2](/docs/specs/ssu2/) verwendet werden.

- Vier DH-Operationen insgesamt im Vergleich zu drei bei XK
- Sender-Authentifizierung in der ersten Nachricht: Die Nutzdaten werden als zugehörig zum Besitzer des öffentlichen Schlüssels des Senders authentifiziert, obwohl der Schlüssel kompromittiert worden sein könnte (Authentication 1). XK erfordert eine weitere Roundtrip-Zeit, bevor Alice authentifiziert ist.
- Vollständige Forward Secrecy (Confidentiality 5) nach der zweiten Nachricht. Bob kann unmittelbar nach der zweiten Nachricht eine Nutzdatenlast mit vollständiger Forward Secrecy senden. XK erfordert eine weitere Roundtrip-Zeit für vollständige Forward Secrecy.

Zusammenfassend ermöglicht IK eine 1-RTT-Übertragung der Antwort-Payload von Bob an Alice mit vollständiger Forward Secrecy, jedoch ist die Anfrage-Payload nicht forward-secret.

### Sitzungen

Das ElGamal/AES+SessionTag-Protokoll ist unidirektional. Auf dieser Ebene weiß der Empfänger nicht, woher eine Nachricht stammt. Ausgehende und eingehende Sitzungen sind nicht miteinander verknüpft. Bestätigungen erfolgen außerhalb des Bands mittels einer DeliveryStatusMessage (verpackt in einer GarlicMessage) im Clove.

Für diese Spezifikation definieren wir zwei Mechanismen zur Erstellung eines bidirektionalen Protokolls - "Pairing" und "Binding". Diese Mechanismen bieten erhöhte Effizienz und Sicherheit.

#### Sitzungskontext

Wie bei ElGamal/AES+SessionTags müssen alle eingehenden und ausgehenden Sitzungen in einem bestimmten Kontext stehen, entweder im Kontext des routers oder im Kontext für ein bestimmtes lokales Ziel. In Java I2P wird dieser Kontext Session Key Manager genannt.

Sessions dürfen nicht zwischen Kontexten geteilt werden, da dies eine Korrelation zwischen den verschiedenen lokalen Zielen oder zwischen einem lokalen Ziel und einem router ermöglichen würde.

Wenn ein bestimmtes Ziel sowohl ElGamal/AES+SessionTags als auch diese Spezifikation unterstützt, können beide Arten von Sitzungen einen Kontext teilen. Siehe Abschnitt 1c) unten.

#### Koppeln von eingehenden und ausgehenden Sitzungen

Wenn eine ausgehende Sitzung beim Ursprung (Alice) erstellt wird, wird eine neue eingehende Sitzung erstellt und mit der ausgehenden Sitzung gepaart, es sei denn, es wird keine Antwort erwartet (z.B. rohe Datagramme).

Eine neue eingehende Session wird immer mit einer neuen ausgehenden Session gepaart, es sei denn, es wird keine Antwort angefordert (z.B. bei rohen Datagrammen).

Wenn eine Antwort angefordert und an ein entferntes Ziel oder einen router gebunden wird, wird diese neue ausgehende Sitzung an dieses Ziel oder diesen router gebunden und ersetzt jede vorherige ausgehende Sitzung zu diesem Ziel oder router.

Das Paaren von eingehenden und ausgehenden Sitzungen bietet ein bidirektionales Protokoll mit der Fähigkeit, die DH-Schlüssel zu rotieren.

#### Sitzungen und Ziele verbinden

Es gibt nur eine ausgehende Session zu einem bestimmten Ziel oder router. Es kann mehrere aktuelle eingehende Sessions von einem bestimmten Ziel oder router geben. Wenn eine neue eingehende Session erstellt wird und Datenverkehr auf dieser Session empfangen wird (was als ACK dient), werden alle anderen normalerweise markiert, um relativ schnell zu verfallen, innerhalb einer Minute oder so. Der Wert der zuvor gesendeten Nachrichten (PN) wird überprüft, und wenn es keine unempfangenen Nachrichten (innerhalb der Fenstergröße) in der vorherigen eingehenden Session gibt, kann die vorherige Session sofort gelöscht werden.

Wenn eine ausgehende Session beim Urheber (Alice) erstellt wird, ist sie an das entfernte Destination (Bob) gebunden, und jede gepaarte eingehende Session wird ebenfalls an das entfernte Destination gebunden. Während die Sessions ratchet, bleiben sie weiterhin an das entfernte Destination gebunden.

Wenn eine eingehende Session beim Empfänger (Bob) erstellt wird, kann sie an das entfernte Destination (Alice) gebunden werden, nach Alices Wahl. Wenn Alice Bindungsinformationen (ihren statischen Schlüssel) in der New Session-Nachricht einschließt, wird die Session an dieses Destination gebunden, und eine ausgehende Session wird erstellt und an dasselbe Destination gebunden. Während die Sessions sich weiterentwickeln (ratchet), bleiben sie weiterhin an das entfernte Destination gebunden.

#### Vorteile von Binding und Pairing

Für den üblichen Streaming-Fall erwarten wir, dass Alice und Bob das Protokoll wie folgt verwenden:

- Alice verbindet ihre neue ausgehende Session mit einer neuen eingehenden Session, beide
  gebunden an das entfernte Ziel (Bob).
- Alice fügt die Bindungsinformationen und Signatur sowie eine Antwortanfrage
  in die New Session-Nachricht ein, die an Bob gesendet wird.
- Bob verbindet seine neue eingehende Session mit einer neuen ausgehenden Session, beide
  gebunden an das entfernte Ziel (Alice).
- Bob sendet eine Antwort (ack) an Alice in der verbundenen Session, mit einem ratchet
  zu einem neuen DH-Schlüssel.
- Alice führt ein ratchet zu einer neuen ausgehenden Session mit Bobs neuem Schlüssel durch, verbunden
  mit der bestehenden eingehenden Session.

Durch die Bindung einer eingehenden Sitzung an eine entfernte Destination und die Kopplung der eingehenden Sitzung mit einer ausgehenden Sitzung, die an dieselbe Destination gebunden ist, erzielen wir zwei wesentliche Vorteile:

1) Die erste Antwort von Bob an Alice verwendet ephemeral-ephemeral DH

2\) Nachdem Alice Bobs Antwort erhalten und die Ratchets aktualisiert hat, verwenden alle nachfolgenden Nachrichten von Alice an Bob ephemeral-ephemeral DH.

#### Nachrichten-ACKs

In ElGamal/AES+SessionTags wird, wenn ein LeaseSet als garlic clove gebündelt wird oder Tags übertragen werden, vom sendenden Router eine Bestätigung (ACK) angefordert. Dies ist ein separater garlic clove, der eine DeliveryStatus-Nachricht enthält. Für zusätzliche Sicherheit wird die DeliveryStatus-Nachricht in eine Garlic-Nachricht eingehüllt. Dieser Mechanismus ist aus Sicht des Protokolls out-of-band.

Im neuen Protokoll können wir, da die eingehenden und ausgehenden Sitzungen gekoppelt sind, ACKs bandintern haben. Es ist keine separate Clove erforderlich.

Ein explizites ACK ist einfach eine Existing Session-Nachricht ohne I2NP-Block. In den meisten Fällen kann jedoch ein explizites ACK vermieden werden, da es Gegenverkehr gibt. Es kann für Implementierungen wünschenswert sein, eine kurze Zeit (vielleicht hundert ms) zu warten, bevor ein explizites ACK gesendet wird, um der Streaming- oder Anwendungsschicht Zeit zu geben zu antworten.

Implementierungen müssen auch das Senden von ACKs aufschieben, bis der I2NP-Block verarbeitet wurde, da die Garlic Message möglicherweise eine Database Store Message mit einem leaseSet enthält. Ein aktuelles leaseSet wird notwendig sein, um das ACK zu routen, und das entfernte Ziel (im leaseSet enthalten) wird erforderlich sein, um den bindenden statischen Schlüssel zu verifizieren.

#### Session-Timeouts

Outbound-Sessions sollten immer vor Inbound-Sessions ablaufen. Sobald eine Outbound-Session abläuft und eine neue erstellt wird, wird auch eine neue gekoppelte Inbound-Session erstellt. Falls es eine alte Inbound-Session gab, wird diese ablaufen gelassen.

### Multicast

Noch zu bestimmen

### Definitionen

Wir definieren die folgenden Funktionen, die den verwendeten kryptographischen Bausteinen entsprechen.

ZEROLEN

Byte-Array der Länge Null

CSRNG(n)

n-Byte-Ausgabe von einem kryptographisch sicheren Zufallszahlengenerator

    generator.

H(p, d)

SHA-256 Hash-Funktion, die einen Personalisierungsstring p und Daten entgegennimmt

    d, and produces an output of length 32 bytes. As defined in
    [NOISE](https://noiseprotocol.org/noise.html). || below means append.

    Use SHA-256 as follows:

        H(p, d) := SHA-256(p || d)

MixHash(d)

SHA-256 Hash-Funktion, die einen vorherigen Hash h und neue Daten d nimmt,

    and produces an output of length 32 bytes. || below means append.

    Use SHA-256 as follows:

        MixHash(d) := h = SHA-256(h || d)

STREAM

Die ChaCha20/Poly1305 AEAD wie spezifiziert in

    [RFC-7539](https://tools.ietf.org/html/rfc7539). S_KEY_LEN = 32 and S_IV_LEN =
    12.

    ENCRYPT(k, n, plaintext, ad)

    :   Encrypts plaintext using the cipher key k, and nonce n which
        MUST be unique for the key k. Associated data ad is optional.
        Returns a ciphertext that is the size of the plaintext + 16
        bytes for the HMAC.

        The entire ciphertext must be indistinguishable from random if
        the key is secret.

    DECRYPT(k, n, ciphertext, ad)

    :   Decrypts ciphertext using the cipher key k, and nonce n.
        Associated data ad is optional. Returns the plaintext.

DH

X25519 öffentliches Schlüsselaustauschsystem. Private Schlüssel mit 32 Bytes, öffentliche

    keys of 32 bytes, produces outputs of 32 bytes. It has the following
    functions:

    GENERATE_PRIVATE()

    :   Generates a new private key.

    DERIVE_PUBLIC(privkey)

    :   Returns the public key corresponding to the given private key.

    GENERATE_PRIVATE_ELG2()

    :   Generates a new private key that maps to a public key suitable
        for Elligator2 encoding. Note that half of the
        randomly-generated private keys will not be suitable and must be
        discarded.

    ENCODE_ELG2(pubkey)

    :   Returns the Elligator2-encoded public key corresponding to the
        given public key (inverse mapping). Encoded keys are little
        endian. Encoded key must be 256 bits indistinguishable from
        random data. See Elligator2 section below for specification.

    DECODE_ELG2(pubkey)

    :   Returns the public key corresponding to the given
        Elligator2-encoded public key. See Elligator2 section below for
        specification.

    DH(privkey, pubkey)

    :   Generates a shared secret from the given private and public
        keys.

HKDF(salt, ikm, info, n)

Eine kryptographische Schlüsselableitungsfunktion, die einen Eingabeschlüssel nimmt

    material ikm (which should have good entropy but is not required to
    be a uniformly random string), a salt of length 32 bytes, and a
    context-specific 'info' value, and produces an output of n bytes
    suitable for use as key material.

    Use HKDF as specified in [RFC-5869](https://tools.ietf.org/html/rfc5869), using
    the HMAC hash function SHA-256 as specified in
    [RFC-2104](https://tools.ietf.org/html/rfc2104). This means that SALT_LEN is 32
    bytes max.

MixKey(d)

Verwende HKDF() mit einem vorherigen chainKey und neuen Daten d, und setzt den neuen

    chainKey and k. As defined in [NOISE](https://noiseprotocol.org/noise.html).

    Use HKDF as follows:

        MixKey(d) := output = HKDF(chainKey, d, "", 64)
                     chainKey = output[0:31]
                     k = output[32:63]

### 1) Nachrichtenformat

#### Überprüfung des aktuellen Nachrichtenformats

Die Garlic Message, wie in [I2NP](/docs/specs/i2np/) spezifiziert, ist wie folgt. Da ein Entwurfsziel ist, dass Zwischenstationen neue von alter Kryptographie nicht unterscheiden können, kann dieses Format nicht geändert werden, obwohl das Längenfeld redundant ist. Das Format wird mit dem vollständigen 16-Byte-Header gezeigt, obwohl der tatsächliche Header je nach verwendetem Transport in einem anderen Format vorliegen kann.

Wenn entschlüsselt, enthält die Daten eine Reihe von Garlic Cloves und zusätzliche Daten, auch bekannt als Clove Set.

Siehe [I2NP](/docs/specs/i2np/) für Details und eine vollständige Spezifikation.

```
+----+----+----+----+----+----+----+----+
|type|      msg_id       |  expiration
+----+----+----+----+----+----+----+----+
                         |  size   |chks|
+----+----+----+----+----+----+----+----+
|      length       |                   |
+----+----+----+----+                   +
|          encrypted data               |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
```
#### Überprüfung des verschlüsselten Datenformats

In ElGamal/AES+SessionTags gibt es zwei Nachrichtenformate:

1\) Neue Sitzung: - 514 Byte ElGamal-Block - AES-Block (mindestens 128 Bytes, Vielfaches von 16)

2\) Bestehende Sitzung: - 32 Byte Session Tag - AES-Block (128 Bytes minimum, Vielfaches von 16)

Diese Nachrichten sind in einer I2NP garlic message eingekapselt, die ein Längenfeld enthält, sodass die Länge bekannt ist.

Der Empfänger versucht zunächst, die ersten 32 Bytes als Session Tag nachzuschlagen. Falls gefunden, entschlüsselt er den AES-Block. Falls nicht gefunden und die Daten mindestens (514+16) lang sind, versucht er den ElGamal-Block zu entschlüsseln, und bei Erfolg entschlüsselt er den AES-Block.

#### Neue Session Tags und Vergleich zu Signal

In Signal Double Ratchet enthält der Header:

- DH: Aktueller ratchet öffentlicher Schlüssel
- PN: Vorherige Kettennachrichtenlänge
- N: Nachrichtennummer

Signals "Sendeketten" entsprechen ungefähr unseren Tag-Sets. Durch die Verwendung eines Session-Tags können wir den Großteil davon eliminieren.

In New Session setzen wir nur den öffentlichen Schlüssel in den unverschlüsselten Header.

In einer bestehenden Session verwenden wir ein Session-Tag für den Header. Das Session-Tag ist mit dem aktuellen Ratchet Public Key und der Nachrichtennummer verknüpft.

Bei sowohl neuen als auch bestehenden Sessions befinden sich PN und N im verschlüsselten Körper.

In Signal werden die Schlüssel ständig rotiert. Ein neuer DH-Public-Key erfordert, dass der Empfänger die Rotation durchführt und einen neuen Public Key zurücksendet, was gleichzeitig als Bestätigung für den empfangenen Public Key dient. Das wären viel zu viele DH-Operationen für uns. Daher trennen wir die Bestätigung des empfangenen Schlüssels von der Übertragung eines neuen Public Keys. Jede Nachricht, die ein Session-Tag verwendet, das vom neuen DH-Public-Key generiert wurde, stellt eine Bestätigung dar. Wir übertragen nur dann einen neuen Public Key, wenn wir eine Schlüssel-Neugenerierung durchführen möchten.

Die maximale Anzahl von Nachrichten, bevor der DH ratchet muss, beträgt 65535.

Bei der Übermittlung eines Session-Schlüssels leiten wir das "Tag Set" davon ab, anstatt zusätzlich Session-Tags übertragen zu müssen. Ein Tag Set kann bis zu 65536 Tags enthalten. Empfänger sollten jedoch eine "Look-ahead"-Strategie implementieren, anstatt alle möglichen Tags auf einmal zu generieren. Generiere höchstens N Tags nach dem letzten korrekt empfangenen Tag. N könnte höchstens 128 betragen, aber 32 oder sogar weniger könnte eine bessere Wahl sein.

### 1a) Neues Session-Format

New Session One Time Public key (32 Bytes) Verschlüsselte Daten und MAC (verbleibende Bytes)

Die New Session-Nachricht kann den statischen öffentlichen Schlüssel des Absenders enthalten oder auch nicht. Wenn er enthalten ist, wird die Rücksitzung an diesen Schlüssel gebunden. Der statische Schlüssel sollte enthalten sein, wenn Antworten erwartet werden, d.h. für Streaming und beantwortbare Datagramme. Er sollte nicht für rohe Datagramme enthalten sein.

Die New Session-Nachricht ähnelt dem einseitigen Noise [NOISE](https://noiseprotocol.org/noise.html) Pattern "N" (falls der statische Schlüssel nicht gesendet wird) oder dem zweiseitigen Pattern "IK" (falls der statische Schlüssel gesendet wird).

### 1b) Neues Sitzungsformat (mit Bindung)

Die Länge beträgt 96 + Payload-Länge. Verschlüsseltes Format:

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
+         Static Key                    +
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
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Public Key :: 32 bytes, little endian, Elligator2, cleartext

Static Key encrypted data :: 32 bytes

Payload Section encrypted data :: remaining data minus 16 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
#### Neuer temporärer Session-Schlüssel

Der ephemere Schlüssel ist 32 Bytes groß und mit Elligator2 codiert. Dieser Schlüssel wird niemals wiederverwendet; ein neuer Schlüssel wird für jede Nachricht generiert, einschließlich Neuübertragungen.

#### Statischer Schlüssel

Nach der Entschlüsselung, Alices statischer X25519-Schlüssel, 32 Bytes.

#### Nutzdaten

Die verschlüsselte Länge ist der Rest der Daten. Die entschlüsselte Länge ist 16 weniger als die verschlüsselte Länge. Die Nutzlast muss einen DateTime-Block enthalten und wird normalerweise einen oder mehrere Garlic Clove-Blöcke enthalten. Siehe den Nutzlast-Abschnitt unten für Format und zusätzliche Anforderungen.

### 1c) Neues Sitzungsformat (ohne Bindung)

Wenn keine Antwort erforderlich ist, wird kein statischer Schlüssel gesendet.

Die Länge beträgt 96 + Nutzlastlänge. Verschlüsseltes Format:

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
|                                       |
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
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Public Key :: 32 bytes, little endian, Elligator2, cleartext

Flags Section encrypted data :: 32 bytes

Payload Section encrypted data :: remaining data minus 16 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
#### Neuer Session Ephemeral Key

Alices ephemeral key. Der ephemeral key ist 32 Bytes groß, kodiert mit Elligator2, little endian. Dieser Schlüssel wird niemals wiederverwendet; ein neuer Schlüssel wird mit jeder Nachricht generiert, einschließlich Neuübertragungen.

#### Flags-Sektion Entschlüsselte Daten

Der Flags-Abschnitt enthält nichts. Er ist immer 32 Bytes lang, da er die gleiche Länge wie der statische Schlüssel für New Session-Nachrichten mit Binding haben muss. Bob bestimmt, ob es sich um einen statischen Schlüssel oder einen Flags-Abschnitt handelt, indem er prüft, ob die 32 Bytes alle Nullen sind.

TODO sind hier irgendwelche Flags erforderlich?

#### Nutzlast

Die verschlüsselte Länge ist der Rest der Daten. Die entschlüsselte Länge ist 16 weniger als die verschlüsselte Länge. Die Nutzlast muss einen DateTime-Block enthalten und wird normalerweise einen oder mehrere Garlic Clove-Blöcke enthalten. Siehe den Nutzlast-Abschnitt unten für Format und zusätzliche Anforderungen.

### 1d) Einmaliges Format (keine Bindung oder Sitzung)

Wenn nur eine einzige Nachricht gesendet werden soll, ist keine Session-Einrichtung oder ein statischer Schlüssel erforderlich.

Die Länge beträgt 96 + Nutzdatenlänge. Verschlüsseltes Format:

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|       Ephemeral Public Key            |
+             32 bytes                  +
|     Encoded with Elligator2           |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+           Flags Section               +
|       ChaCha20 encrypted data         |
+            32 bytes                   +
|                                       |
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
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Public Key :: 32 bytes, little endian, Elligator2, cleartext

Flags Section encrypted data :: 32 bytes

Payload Section encrypted data :: remaining data minus 16 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
#### Neuer Session-Einmalschlüssel

Der Einmalschlüssel ist 32 Bytes groß, mit Elligator2 kodiert, little endian. Dieser Schlüssel wird niemals wiederverwendet; ein neuer Schlüssel wird für jede Nachricht generiert, einschließlich Neuübertragungen.

#### Flags-Bereich Entschlüsselte Daten

Die Flags-Sektion enthält nichts. Sie ist immer 32 Bytes lang, weil sie die gleiche Länge wie der statische Schlüssel für New Session-Nachrichten mit Binding haben muss. Bob bestimmt, ob es sich um einen statischen Schlüssel oder eine Flags-Sektion handelt, indem er testet, ob die 32 Bytes alle Nullen sind.

TODO sind hier irgendwelche Flags erforderlich?

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|                                       |
+             All zeros                 +
|              32 bytes                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

zeros:: All zeros, 32 bytes.
```
#### Nutzlast

Die verschlüsselte Länge ist der Rest der Daten. Die entschlüsselte Länge ist 16 weniger als die verschlüsselte Länge. Die Nutzlast muss einen DateTime-Block enthalten und wird normalerweise einen oder mehrere Garlic Clove-Blöcke enthalten. Siehe den Nutzlast-Abschnitt unten für Format und zusätzliche Anforderungen.

### 1f) KDFs für New Session Message

#### KDF für Initial ChainKey

Dies ist standardmäßiges [NOISE](https://noiseprotocol.org/noise.html) für IK mit einem modifizierten Protokollnamen. Beachten Sie, dass wir denselben Initialisierer sowohl für das IK-Muster (gebundene Sitzungen) als auch für das N-Muster (ungebundene Sitzungen) verwenden.

Der Protokollname wird aus zwei Gründen geändert. Erstens, um anzuzeigen, dass die ephemeren Schlüssel mit Elligator2 kodiert sind, und zweitens, um anzuzeigen, dass MixHash() vor der zweiten Nachricht aufgerufen wird, um den Tag-Wert einzumischen.

```
This is the "e" message pattern:

// Define protocol_name.
Set protocol_name = "Noise_IKelg2+hs2_25519_ChaChaPoly_SHA256"
 (40 bytes, US-ASCII encoded, no NULL termination).

// Define Hash h = 32 bytes
h = SHA256(protocol_name);

Define ck = 32 byte chaining key. Copy the h data to ck.
Set chainKey = h

// MixHash(null prologue)
h = SHA256(h);

// up until here, can all be precalculated by Alice for all outgoing connections
```
#### KDF für Flags/Static Key Section verschlüsselte Inhalte

```
This is the "e" message pattern:

// Bob's X25519 static keys
// bpk is published in leaseset
bsk = GENERATE_PRIVATE()
bpk = DERIVE_PUBLIC(bsk)

// Bob static public key
// MixHash(bpk)
// || below means append
h = SHA256(h || bpk);

// up until here, can all be precalculated by Bob for all incoming connections

// Alice's X25519 ephemeral keys
aesk = GENERATE_PRIVATE_ELG2()
aepk = DERIVE_PUBLIC(aesk)

// Alice ephemeral public key
// MixHash(aepk)
// || below means append
h = SHA256(h || aepk);

// h is used as the associated data for the AEAD in the New Session Message
// Retain the Hash h for the New Session Reply KDF
// eapk is sent in cleartext in the
// beginning of the New Session message
elg2_aepk = ENCODE_ELG2(aepk)
// As decoded by Bob
aepk = DECODE_ELG2(elg2_aepk)

End of "e" message pattern.

This is the "es" message pattern:

// Noise es
sharedSecret = DH(aesk, bpk) = DH(bsk, aepk)

// MixKey(DH())
//[chainKey, k] = MixKey(sharedSecret)
// ChaChaPoly parameters to encrypt/decrypt
keydata = HKDF(chainKey, sharedSecret, "", 64)
chainKey = keydata[0:31]

// AEAD parameters
k = keydata[32:63]
n = 0
ad = h
ciphertext = ENCRYPT(k, n, flags/static key section, ad)

End of "es" message pattern.

This is the "s" message pattern:

// MixHash(ciphertext)
// Save for Payload section KDF
h = SHA256(h || ciphertext)

// Alice's X25519 static keys
ask = GENERATE_PRIVATE()
apk = DERIVE_PUBLIC(ask)

End of "s" message pattern.
```
#### KDF für Payload-Sektion (mit Alice static key)

```
This is the "ss" message pattern:

// Noise ss
sharedSecret = DH(ask, bpk) = DH(bsk, apk)

// MixKey(DH())
//[chainKey, k] = MixKey(sharedSecret)
// ChaChaPoly parameters to encrypt/decrypt
// chainKey from Static Key Section
Set sharedSecret = X25519 DH result
keydata = HKDF(chainKey, sharedSecret, "", 64)
chainKey = keydata[0:31]

// AEAD parameters
k = keydata[32:63]
n = 0
ad = h
ciphertext = ENCRYPT(k, n, payload, ad)

End of "ss" message pattern.

// MixHash(ciphertext)
// Save for New Session Reply KDF
h = SHA256(h || ciphertext)
```
#### KDF für Payload-Sektion (ohne Alice statischen Schlüssel)

Beachten Sie, dass dies ein Noise "N"-Muster ist, aber wir verwenden den gleichen "IK"-Initialisierer wie für gebundene Sitzungen.

New Session-Nachrichten können nicht als Alices statischen Schlüssel enthaltend oder nicht enthaltend identifiziert werden, bis der statische Schlüssel entschlüsselt und überprüft wurde, um festzustellen, ob er nur Nullen enthält. Daher muss der Empfänger die "IK"-Zustandsmaschine für alle New Session-Nachrichten verwenden. Wenn der statische Schlüssel nur Nullen enthält, muss das "ss"-Nachrichtenmuster übersprungen werden.

```
chainKey = from Flags/Static key section
k = from Flags/Static key section
n = 1
ad = h from Flags/Static key section
ciphertext = ENCRYPT(k, n, payload, ad)
```
### 1g) Format der New Session Reply

Eine oder mehrere New Session Replies können als Antwort auf eine einzelne New Session-Nachricht gesendet werden. Jeder Antwort wird ein Tag vorangestellt, das aus einem TagSet für die Sitzung generiert wird.

Die New Session Reply besteht aus zwei Teilen. Der erste Teil ist die Vervollständigung des Noise IK-Handshakes mit einem vorangestellten Tag. Die Länge des ersten Teils beträgt 56 Bytes. Der zweite Teil ist die Nutzdaten der Datenphase. Die Länge des zweiten Teils beträgt 16 + Nutzdatenlänge.

Die Gesamtlänge beträgt 72 + Payload-Länge. Verschlüsseltes Format:

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
+  (MAC) for Key Section (no data)      +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Tag :: 8 bytes, cleartext

Public Key :: 32 bytes, little endian, Elligator2, cleartext

MAC :: Poly1305 message authentication code, 16 bytes
       Note: The ChaCha20 plaintext data is empty (ZEROLEN)

Payload Section encrypted data :: remaining data minus 16 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
#### Session Tag

Der Tag wird in der Session Tags KDF generiert, wie in der DH Initialization KDF unten initialisiert. Dies korreliert die Antwort mit der Session. Der Session Key aus der DH Initialization wird nicht verwendet.

#### New Session Reply Ephemeral Key

Bobs ephemerer Schlüssel. Der ephemere Schlüssel ist 32 Bytes lang, kodiert mit Elligator2, little endian. Dieser Schlüssel wird niemals wiederverwendet; ein neuer Schlüssel wird mit jeder Nachricht generiert, einschließlich Neuübertragungen.

#### Nutzlast

Die verschlüsselte Länge ist der Rest der Daten. Die entschlüsselte Länge ist 16 weniger als die verschlüsselte Länge. Die Nutzlast enthält normalerweise einen oder mehrere Garlic Clove Blöcke. Siehe den Nutzlast-Abschnitt unten für Format und zusätzliche Anforderungen.

#### KDF für Reply TagSet

Ein oder mehrere Tags werden aus dem TagSet erstellt, das mit der unten beschriebenen KDF initialisiert wird, unter Verwendung des chainKey aus der New Session-Nachricht.

```
// Generate tagset

tagsetKey = HKDF(chainKey, ZEROLEN, "SessionReplyTags", 32)
    tagset_nsr = DH_INITIALIZE(chainKey, tagsetKey)

```
#### KDF für verschlüsselte Inhalte des Reply Key Abschnitts

```
// Keys from the New Session message
// Alice's X25519 keys
// apk and aepk are sent in original New Session message
// ask = Alice private static key
// apk = Alice public static key
// aesk = Alice ephemeral private key
// aepk = Alice ephemeral public key
// Bob's X25519 static keys
// bsk = Bob private static key
// bpk = Bob public static key

// Generate the tag
tagsetEntry = tagset_nsr.GET_NEXT_ENTRY()
tag = tagsetEntry.SESSION_TAG

// MixHash(tag)
h = SHA256(h || tag)

This is the "e" message pattern:

// Bob's X25519 ephemeral keys
besk = GENERATE_PRIVATE_ELG2()
bepk = DERIVE_PUBLIC(besk)

// Bob's ephemeral public key
// MixHash(bepk)
// || below means append
h = SHA256(h || bepk);

// elg2_bepk is sent in cleartext in the
// beginning of the New Session message
elg2_bepk = ENCODE_ELG2(bepk)
// As decoded by Bob
bepk = DECODE_ELG2(elg2_bepk)

End of "e" message pattern.

This is the "ee" message pattern:

// MixKey(DH())
//[chainKey, k] = MixKey(sharedSecret)
// ChaChaPoly parameters to encrypt/decrypt
// chainKey from original New Session Payload Section
sharedSecret = DH(aesk, bepk) = DH(besk, aepk)
keydata = HKDF(chainKey, sharedSecret, "", 32)
chainKey = keydata[0:31]

End of "ee" message pattern.

This is the "se" message pattern:

// MixKey(DH())
//[chainKey, k] = MixKey(sharedSecret)
sharedSecret = DH(ask, bepk) = DH(besk, apk)
keydata = HKDF(chainKey, sharedSecret, "", 64)
chainKey = keydata[0:31]

// AEAD parameters
k = keydata[32:63]
n = 0
ad = h
ciphertext = ENCRYPT(k, n, ZEROLEN, ad)

End of "se" message pattern.

// MixHash(ciphertext)
h = SHA256(h || ciphertext)

chainKey is used in the ratchet below.
```
#### KDF für verschlüsselte Inhalte der Payload-Sektion

Dies ist wie die erste Existing Session-Nachricht nach der Aufteilung, aber ohne einen separaten Tag. Zusätzlich verwenden wir den Hash von oben, um die Nutzlast an die NSR-Nachricht zu binden.

```
This is the "ss" message pattern:

// Noise ss
sharedSecret = DH(ask, bpk) = DH(bsk, apk)

// MixKey(DH())
//[chainKey, k] = MixKey(sharedSecret)
// ChaChaPoly parameters to encrypt/decrypt
// chainKey from Static Key Section
Set sharedSecret = X25519 DH result
keydata = HKDF(chainKey, sharedSecret, "", 64)
chainKey = keydata[0:31]

// AEAD parameters
k = keydata[32:63]
n = 0
ad = h
ciphertext = ENCRYPT(k, n, payload, ad)

End of "ss" message pattern.

// MixHash(ciphertext)
// Save for New Session Reply KDF
h = SHA256(h || ciphertext)
```
### Notizen

Mehrere NSR-Nachrichten können als Antwort gesendet werden, jede mit eindeutigen ephemeren Schlüsseln, abhängig von der Größe der Antwort.

Alice und Bob müssen für jede NS- und NSR-Nachricht neue ephemere Schlüssel verwenden.

Alice muss eine von Bobs NSR-Nachrichten erhalten, bevor sie Existing Session (ES)-Nachrichten senden kann, und Bob muss eine ES-Nachricht von Alice erhalten, bevor er ES-Nachrichten senden kann.

Der `chainKey` und `k` aus Bobs NSR Payload Section werden als Eingaben für die anfänglichen ES DH Ratchets (beide Richtungen, siehe DH Ratchet KDF) verwendet.

Bob darf nur bestehende Sessions für die ES-Nachrichten behalten, die von Alice empfangen wurden. Alle anderen erstellten eingehenden und ausgehenden Sessions (für mehrere NSRs) sollten sofort nach dem Empfang von Alices erster ES-Nachricht für eine gegebene Session zerstört werden.

### 1h) Format bestehender Sitzung

Session-Tag (8 Bytes) Verschlüsselte Daten und MAC (siehe Abschnitt 3 unten)

#### Format

Verschlüsselt:

```
+----+----+----+----+----+----+----+----+
|       Session Tag                     |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+              (MAC)                    +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Session Tag :: 8 bytes, cleartext

Payload Section encrypted data :: remaining data minus 16 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
#### Nutzlast

Die verschlüsselte Länge ist der Rest der Daten. Die entschlüsselte Länge ist 16 weniger als die verschlüsselte Länge. Siehe den Payload-Bereich unten für Format und Anforderungen.

#### KDF

```
See AEAD section below.

// AEAD parameters for Existing Session payload
k = The 32-byte session key associated with this session tag
n = The message number N in the current chain, as retrieved from the associated Session Tag.
ad = The session tag, 8 bytes
ciphertext = ENCRYPT(k, n, payload, ad)
```
### 2) ECIES-X25519

Format: 32-Byte öffentliche und private Schlüssel, Little-Endian.

### 2a) Elligator2

Bei Standard-Noise-Handshakes beginnen die anfänglichen Handshake-Nachrichten in jede Richtung mit ephemeren Schlüsseln, die im Klartext übertragen werden. Da gültige X25519-Schlüssel von zufälligen Daten unterscheidbar sind, kann ein Man-in-the-Middle diese Nachrichten von Existing Session-Nachrichten unterscheiden, die mit zufälligen Session-Tags beginnen. In [NTCP2](/docs/specs/ntcp2/) ([Prop111](/proposals/111-ntcp2/)) haben wir eine ressourcenschonende XOR-Funktion mit dem out-of-band static key verwendet, um den Schlüssel zu verschleiern. Das Bedrohungsmodell ist hier jedoch anders; wir möchten nicht zulassen, dass ein MitM (Man-in-the-Middle) irgendwelche Mittel verwenden kann, um das Ziel des Traffics zu bestätigen oder um die anfänglichen Handshake-Nachrichten von Existing Session-Nachrichten zu unterscheiden.

Daher wird [Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf) verwendet, um die ephemeren Schlüssel in den New Session und New Session Reply Nachrichten zu transformieren, sodass sie nicht von gleichmäßig zufälligen Strings unterscheidbar sind.

#### Format

32-Byte öffentliche und private Schlüssel. Kodierte Schlüssel sind Little-Endian.

Wie in [Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf) definiert, sind die kodierten Schlüssel nicht von 254 zufälligen Bits zu unterscheiden. Wir benötigen 256 zufällige Bits (32 Bytes). Daher sind die Kodierung und Dekodierung wie folgt definiert:

Kodierung:

```
ENCODE_ELG2() Definition

// Encode as defined in Elligator2 specification
encodedKey = encode(pubkey)
// OR in 2 random bits to MSB
randomByte = CSRNG(1)
encodedKey[31] |= (randomByte & 0xc0)
```
Dekodierung:

```
DECODE_ELG2() Definition

// Mask out 2 random bits from MSB
encodedKey[31] &= 0x3f
// Decode as defined in Elligator2 specification
pubkey = decode(encodedKey)
```
#### Notizen

Elligator2 verdoppelt im Durchschnitt die Schlüsselerzeugungszeit, da die Hälfte der privaten Schlüssel zu öffentlichen Schlüsseln führt, die für die Kodierung mit Elligator2 ungeeignet sind. Außerdem ist die Schlüsselerzeugungszeit unbegrenzt mit einer exponentiellen Verteilung, da der Generator so lange weiterversuchen muss, bis ein geeignetes Schlüsselpaar gefunden wird.

Dieser Overhead kann verwaltet werden, indem die Schlüsselerzeugung im Voraus in einem separaten Thread durchgeführt wird, um einen Pool geeigneter Schlüssel bereitzuhalten.

Der Generator führt die ENCODE_ELG2()-Funktion aus, um die Eignung zu bestimmen. Daher sollte der Generator das Ergebnis von ENCODE_ELG2() speichern, damit es nicht erneut berechnet werden muss.

Zusätzlich können die ungeeigneten Schlüssel dem Pool von Schlüsseln hinzugefügt werden, die für [NTCP2](/docs/specs/ntcp2/) verwendet werden, wo Elligator2 nicht verwendet wird. Die Sicherheitsprobleme dabei sind noch zu klären.

### 3) AEAD (ChaChaPoly)

AEAD mit ChaCha20 und Poly1305, wie in [NTCP2](/docs/specs/ntcp2/). Dies entspricht [RFC-7539](https://tools.ietf.org/html/rfc7539), welches auch ähnlich in TLS [RFC-7905](https://tools.ietf.org/html/rfc7905) verwendet wird.

#### Neue Sitzung und Neue Sitzungsantwort-Eingaben

Eingaben für die Verschlüsselungs-/Entschlüsselungsfunktionen für einen AEAD-Block in einer New Session-Nachricht:

```
k :: 32 byte cipher key
     See New Session and New Session Reply KDFs above.

n :: Counter-based nonce, 12 bytes.
     n = 0

ad :: Associated data, 32 bytes.
      The SHA256 hash of the preceding data, as output from mixHash()

data :: Plaintext data, 0 or more bytes
```
#### Bestehende Session-Eingaben

Eingaben für die Verschlüsselungs-/Entschlüsselungsfunktionen für einen AEAD-Block in einer Existing Session-Nachricht:

```
k :: 32 byte session key
     As looked up from the accompanying session tag.

n :: Counter-based nonce, 12 bytes.
     Starts at 0 and incremented for each message when transmitting.
     For the receiver, the value
     as looked up from the accompanying session tag.
     First four bytes are always zero.
     Last eight bytes are the message number (n), little-endian encoded.
     Maximum value is 65535.
     Session must be ratcheted when N reaches that value.
     Higher values must never be used.

ad :: Associated data
      The session tag

data :: Plaintext data, 0 or more bytes
```
#### Verschlüsseltes Format

Ausgabe der Verschlüsselungsfunktion, Eingabe der Entschlüsselungsfunktion:

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|       ChaCha20 encrypted data         |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+              (MAC)                    +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

encrypted data :: Same size as plaintext data, 0 - 65519 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
#### Notizen

- Da ChaCha20 eine Stromchiffre ist, müssen Klartexte nicht aufgefüllt werden.
  Zusätzliche Keystream-Bytes werden verworfen.
- Der Schlüssel für die Chiffre (256 Bit) wird mittels der
  SHA256 KDF vereinbart. Die Details der KDF für jede Nachricht stehen in separaten
  Abschnitten unten.
- ChaChaPoly-Frames haben eine bekannte Größe, da sie in der
  I2NP-Datennachricht gekapselt sind.
- Bei allen Nachrichten befindet sich das Padding innerhalb des authentifizierten Datenframes.

#### AEAD Fehlerbehandlung

Alle empfangenen Daten, die die AEAD-Verifikation nicht bestehen, müssen verworfen werden. Es wird keine Antwort zurückgegeben.

### 4) Ratchets

Wir verwenden weiterhin Session Tags wie zuvor, aber wir nutzen Ratchets, um sie zu generieren. Session Tags hatten auch eine Rekey-Option, die wir nie implementiert haben. Es ist also wie ein Double Ratchet, aber wir haben den zweiten nie gemacht.

Hier definieren wir etwas ähnliches wie Signals Double Ratchet. Die Session-Tags werden deterministisch und identisch auf der Empfänger- und Senderseite generiert.

Durch die Verwendung eines symmetrischen Schlüssel-/Tag-Ratchets eliminieren wir den Speicherverbrauch zur Speicherung von Session-Tags auf der Senderseite. Wir eliminieren auch den Bandbreitenverbrauch beim Senden von Tag-Sets. Der Verbrauch auf der Empfängerseite ist immer noch erheblich, aber wir können ihn weiter reduzieren, da wir den Session-Tag von 32 Bytes auf 8 Bytes verkleinern werden.

Wir verwenden keine Header-Verschlüsselung wie in Signal spezifiziert (und optional), sondern verwenden stattdessen Session-Tags.

Durch die Verwendung eines DH-Ratchets erreichen wir Forward Secrecy, was bei ElGamal/AES+SessionTags nie implementiert wurde.

Hinweis: Der öffentliche Einmalschlüssel der neuen Sitzung ist nicht Teil des Ratchet, seine einzige Funktion besteht darin, Alices anfänglichen DH-Ratchet-Schlüssel zu verschlüsseln.

#### Nachrichtennummern

Der Double Ratchet behandelt verlorene oder nicht in der richtigen Reihenfolge ankommende Nachrichten, indem er in jeden Nachrichten-Header ein Tag einfügt. Der Empfänger schlägt den Index des Tags nach, dies ist die Nachrichtennummer N. Wenn die Nachricht einen Message Number Block mit einem PN-Wert enthält, kann der Empfänger alle Tags löschen, die höher als dieser Wert im vorherigen Tag-Set sind, während übersprungene Tags aus dem vorherigen Tag-Set beibehalten werden, falls die übersprungenen Nachrichten später ankommen.

#### Beispielimplementierung

Wir definieren die folgenden Datenstrukturen und Funktionen, um diese Ratchets zu implementieren.

TAGSET_ENTRY

Ein einzelner Eintrag in einem TAGSET.

    INDEX

    :   An integer index, starting with 0

    SESSION_TAG

    :   An identifier to go out on the wire, 8 bytes

    SESSION_KEY

    :   A symmetric key, never goes on the wire, 32 bytes

TAGSET

Eine Sammlung von TAGSET_ENTRIES.

    CREATE(key, n)

    :   Generate a new TAGSET using initial cryptographic key material
        of 32 bytes. The associated session identifier is provided. The
        initial number of of tags to create is specified; this is
        generally 0 or 1 for an outgoing session. LAST_INDEX = -1
        EXTEND(n) is called.

    EXTEND(n)

    :   Generate n more TAGSET_ENTRIES by calling EXTEND() n times.

    EXTEND()

    :   Generate one more TAGSET_ENTRY, unless the maximum number
        SESSION_TAGS have already been generated. If LAST_INDEX is
        greater than or equal to 65535, return. ++ LAST_INDEX Create a
        new TAGSET_ENTRY with the LAST_INDEX value and the calculated
        SESSION_TAG. Calls RATCHET_TAG() and (optionally) RATCHET_KEY().
        For inbound sessions, the calculation of the SESSION_KEY may be
        deferred and calculated in GET_SESSION_KEY(). Calls EXPIRE()

    EXPIRE()

    :   Remove tags and keys that are too old, or if the TAGSET size
        exceeds some limit.

    RATCHET_TAG()

    :   Calculates the next SESSION_TAG based on the last SESSION_TAG.

    RATCHET_KEY()

    :   Calculates the next SESSION_KEY based on the last SESSION_KEY.

    SESSION

    :   The associated session.

    CREATION_TIME

    :   When the TAGSET was created.

    LAST_INDEX

    :   The last TAGSET_ENTRY INDEX generated by EXTEND().

    GET_NEXT_ENTRY()

    :   Used for outgoing sessions only. EXTEND(1) is called if there
        are no remaining TAGSET_ENTRIES. If EXTEND(1) did nothing, the
        max of 65535 TAGSETS have been used, and return an error.
        Returns the next unused TAGSET_ENTRY.

    GET_SESSION_KEY(sessionTag)

    :   Used for incoming sessions only. Returns the TAGSET_ENTRY
        containing the sessionTag. If found, the TAGSET_ENTRY is
        removed. If the SESSION_KEY calculation was deferred, it is
        calculated now. If there are few TAGSET_ENTRIES remaining,
        EXTEND(n) is called.

#### 4a) DH Ratchet

Ratchets, aber nicht annähernd so schnell wie Signal es tut. Wir trennen die Bestätigung des empfangenen Schlüssels von der Generierung des neuen Schlüssels. Bei typischer Nutzung werden Alice und Bob jeweils (zweimal) sofort in einer New Session einen Ratchet durchführen, aber danach nicht mehr ratcheten.

Beachten Sie, dass ein Ratchet für eine einzelne Richtung ist und eine New Session Tag / Nachrichtenschlüssel-Ratchet-Kette für diese Richtung generiert. Um Schlüssel für beide Richtungen zu generieren, müssen Sie zweimal ratcheten.

Du führst ein Ratcheting durch, jedes Mal wenn du einen neuen Schlüssel generierst und sendest. Du führst ein Ratcheting durch, jedes Mal wenn du einen neuen Schlüssel empfängst.

Alice führt ein Ratcheting durch, wenn sie eine ungebundene ausgehende Sitzung erstellt, sie erstellt keine eingehende Sitzung (ungebunden bedeutet nicht antwortfähig).

Bob führt einmal ein Ratcheting durch, wenn er eine ungebundene eingehende Sitzung erstellt, und erstellt keine entsprechende ausgehende Sitzung (ungebunden bedeutet nicht antwortbar).

Alice sendet weiterhin New Session (NS) Nachrichten an Bob, bis sie eine von Bobs New Session Reply (NSR) Nachrichten erhält. Sie verwendet dann die KDF-Ergebnisse der Payload Section der NSR als Eingaben für die Session-Ratchets (siehe DH Ratchet KDF) und beginnt mit dem Senden von Existing Session (ES) Nachrichten.

Für jede empfangene NS-Nachricht erstellt Bob eine neue eingehende Sitzung und verwendet die KDF-Ergebnisse des Antwort-Payload-Abschnitts als Eingaben für die neue eingehende und ausgehende ES DH Ratchet.

Für jede erforderliche Antwort sendet Bob Alice eine NSR-Nachricht mit der Antwort in der Nutzdaten. Es ist erforderlich, dass Bob neue ephemerale Schlüssel für jede NSR verwendet.

Bob muss eine ES-Nachricht von Alice auf einer der eingehenden Sitzungen erhalten, bevor er ES-Nachrichten auf der entsprechenden ausgehenden Sitzung erstellt und sendet.

Alice sollte einen Timer für den Empfang einer NSR-Nachricht von Bob verwenden. Wenn der Timer abläuft, sollte die Session entfernt werden.

Um einen KCI- und/oder Ressourcenerschöpfungsangriff zu vermeiden, bei dem ein Angreifer Bobs NSR-Antworten verwirft, um Alice dazu zu bringen, weiterhin NS-Nachrichten zu senden, sollte Alice vermeiden, neue Sitzungen zu Bob zu starten, nachdem eine bestimmte Anzahl von Wiederholungsversuchen aufgrund von Timer-Ablauf aufgetreten ist.

Alice und Bob führen jeweils ein DH-Ratchet für jeden empfangenen NextKey-Block durch.

Alice und Bob generieren jeweils neue Tag-Ratchets und zwei symmetrische Schlüssel-Ratchets nach jedem DH-Ratchet. Für jede neue ES-Nachricht in einer gegebenen Richtung rücken Alice und Bob die Session-Tag- und symmetrischen Schlüssel-Ratchets vor.

Die Häufigkeit der DH-Ratchets nach dem ersten Handshake ist implementierungsabhängig. Obwohl das Protokoll eine Grenze von 65535 Nachrichten vor einem erforderlichen Ratchet festlegt, kann häufigeres Ratcheting (basierend auf der Nachrichtenanzahl, verstrichener Zeit oder beidem) zusätzliche Sicherheit bieten.

Nach der finalen Handshake-KDF bei gebundenen Sitzungen müssen Bob und Alice die Noise Split()-Funktion auf den resultierenden CipherState ausführen, um unabhängige symmetrische und Tag-Chain-Schlüssel für eingehende und ausgehende Sitzungen zu erstellen.

##### SCHLÜSSEL- UND TAG-SET-IDS

Schlüssel- und Tag-Set-ID-Nummern werden verwendet, um Schlüssel und Tag-Sets zu identifizieren. Schlüssel-IDs werden in NextKey-Blöcken verwendet, um den gesendeten oder verwendeten Schlüssel zu identifizieren. Tag-Set-IDs werden (zusammen mit der Nachrichtennummer) in ACK-Blöcken verwendet, um die bestätigte Nachricht zu identifizieren. Sowohl Schlüssel- als auch Tag-Set-IDs gelten für die Tag-Sets einer einzelnen Richtung. Schlüssel- und Tag-Set-ID-Nummern müssen sequenziell sein.

In den ersten Tag-Sets, die für eine Session in jede Richtung verwendet werden, ist die Tag-Set-ID 0. Es wurden keine NextKey-Blöcke gesendet, daher gibt es keine Schlüssel-IDs.

Um ein DH ratchet zu beginnen, überträgt der Sender einen neuen NextKey-Block mit einer Schlüssel-ID von 0. Der Empfänger antwortet mit einem neuen NextKey-Block mit einer Schlüssel-ID von 0. Der Sender beginnt dann mit der Verwendung eines neuen Tag-Sets mit einer Tag-Set-ID von 1.

Nachfolgende Tag-Sets werden ähnlich generiert. Für alle Tag-Sets, die nach NextKey-Austauschvorgängen verwendet werden, ist die Tag-Set-Nummer (1 + Alices Schlüssel-ID + Bobs Schlüssel-ID).

Schlüssel- und Tag-Set-IDs beginnen bei 0 und werden sequenziell erhöht. Die maximale Tag-Set-ID ist 65535. Die maximale Schlüssel-ID ist 32767. Wenn ein Tag-Set fast erschöpft ist, muss der Tag-Set-Sender einen NextKey-Austausch initiieren. Wenn Tag-Set 65535 fast erschöpft ist, muss der Tag-Set-Sender eine neue Sitzung initiieren, indem er eine New Session-Nachricht sendet.

Mit einer Streaming-Maximalnachrichtengröße von 1730 und unter der Annahme keiner Neuübertragungen beträgt die theoretische maximale Datenübertragung unter Verwendung eines einzigen Tag-Sets 1730 * 65536 ~= 108 MB. Das tatsächliche Maximum wird aufgrund von Neuübertragungen niedriger sein.

Der theoretische maximale Datentransfer mit allen 65536 verfügbaren Tag-Sets, bevor die Sitzung verworfen und ersetzt werden müsste, beträgt 64K * 108 MB ~= 6,9 TB.

##### DH RATCHET NACHRICHTENFLUSS

Der nächste Schlüsselaustausch für einen Tag-Satz muss vom Sender dieser Tags (dem Eigentümer des ausgehenden Tag-Satzes) initiiert werden. Der Empfänger (Eigentümer des eingehenden Tag-Satzes) wird antworten. Bei typischem HTTP GET-Verkehr auf der Anwendungsebene wird Bob mehr Nachrichten senden und wird zuerst ratcheten, indem er den Schlüsselaustausch initiiert; das untenstehende Diagramm zeigt dies. Wenn Alice ratchetet, passiert dasselbe in umgekehrter Richtung.

Der erste Tag-Satz, der nach dem NS/NSR-Handshake verwendet wird, ist Tag-Satz 0. Wenn Tag-Satz 0 fast erschöpft ist, müssen neue Schlüssel in beide Richtungen ausgetauscht werden, um Tag-Satz 1 zu erstellen. Danach wird ein neuer Schlüssel nur in eine Richtung gesendet.

Um Tag-Set 2 zu erstellen, sendet der Tag-Sender einen neuen Schlüssel und der Tag-Empfänger sendet die ID seines alten Schlüssels als Bestätigung. Beide Seiten führen einen DH durch.

Um Tag-Set 3 zu erstellen, sendet der Tag-Sender die ID seines alten Schlüssels und fordert einen neuen Schlüssel vom Tag-Empfänger an. Beide Seiten führen einen DH durch.

Nachfolgende Tag-Sets werden wie für Tag-Sets 2 und 3 generiert. Die Tag-Set-Nummer ist (1 + Sender-Schlüssel-ID + Empfänger-Schlüssel-ID).

```
Tag Sender                    Tag Receiver

                 ... use tag set #0 ...


(Tagset #0 almost empty)
(generate new key #0)

Next Key, forward, request reverse, with key #0  -------->
(repeat until next key received)

                            (generate new key #0, do DH, create IB Tagset #1)

        <-------------      Next Key, reverse, with key #0
                            (repeat until tag received on new tagset)

(do DH, create OB Tagset #1)


                 ... use tag set #1 ...


(Tagset #1 almost empty)
(generate new key #1)

Next Key, forward, with key #1        -------->
(repeat until next key received)

                            (reuse key #0, do DH, create IB Tagset #2)

        <--------------     Next Key, reverse, id 0
                            (repeat until tag received on new tagset)

(do DH, create OB Tagset #2)


                 ... use tag set #2 ...


(Tagset #2 almost empty)
(reuse key #1)

Next Key, forward, request reverse, id 1  -------->
(repeat until next key received)

                            (generate new key #1, do DH, create IB Tagset #3)

        <--------------     Next Key, reverse, with key #1

(do DH, create OB Tagset #3)
(reuse key #1, do DH, create IB Tagset #3)



                 ... use tag set #3 ...



     After tag set 3, repeat the above
     patterns as shown for tag sets 2 and 3.

     To create a new even-numbered tag set, the sender sends a new key
     to the receiver. The receiver sends his old key ID
     back as an acknowledgement.

     To create a new odd-numbered tag set, the sender sends a reverse request
     to the receiver. The receiver sends a new reverse key to the sender.
```
Nachdem das DH-Ratchet für ein ausgehendes Tagset abgeschlossen ist und ein neues ausgehendes Tagset erstellt wurde, sollte es sofort verwendet werden, und das alte ausgehende Tagset kann gelöscht werden.

Nachdem der DH-Ratchet für ein eingehendes Tagset abgeschlossen ist und ein neues eingehendes Tagset erstellt wurde, sollte der Empfänger auf Tags in beiden Tagsets lauschen und das alte Tagset nach kurzer Zeit, etwa 3 Minuten, löschen.

Eine Zusammenfassung der Tag-Set- und Schlüssel-ID-Progression ist in der nachfolgenden Tabelle dargestellt. * zeigt an, dass ein neuer Schlüssel generiert wird.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">New Tag Set ID</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Sender key ID</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Rcvr key ID</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">n/a</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">n/a</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 *</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 *</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 *</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 *</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2 *</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2 *</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">...</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">...</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">...</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">65534</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32767 *</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32766</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">65535</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32767</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32767 *</td>
</tr>
</table>
Schlüssel- und Tag-Set-ID-Nummern müssen sequenziell sein.

##### DH INITIALIZATION KDF

Das ist die Definition von DH_INITIALIZE(rootKey, k) für eine einzelne Richtung. Es erstellt ein Tagset und einen "nächsten Root-Schlüssel", der bei Bedarf für einen nachfolgenden DH-Ratchet verwendet wird.

Wir verwenden DH-Initialisierung an drei Stellen. Erstens verwenden wir sie zur Generierung eines Tag-Sets für die New Session Replies. Zweitens verwenden wir sie zur Generierung von zwei Tag-Sets, eines für jede Richtung, zur Verwendung in Existing Session-Nachrichten. Schließlich verwenden wir sie nach einem DH Ratchet zur Generierung eines neuen Tag-Sets in eine einzige Richtung für zusätzliche Existing Session-Nachrichten.

```
Inputs:
1) rootKey = chainKey from Payload Section
2) k from the New Session KDF or split()

// KDF_RK(rk, dh_out)
keydata = HKDF(rootKey, k, "KDFDHRatchetStep", 64)

// Output 1: The next Root Key (KDF input for the next DH ratchet)
nextRootKey = keydata[0:31]
// Output 2: The chain key to initialize the new
// session tag and symmetric key ratchets
// for the tag set
ck = keydata[32:63]

// session tag and symmetric key chain keys
keydata = HKDF(ck, ZEROLEN, "TagAndKeyGenKeys", 64)
sessTag_ck = keydata[0:31]
symmKey_ck = keydata[32:63]
```
##### DH RATCHET KDF

Dies wird verwendet, nachdem neue DH-Schlüssel in NextKey-Blöcken ausgetauscht wurden, bevor ein Tagset erschöpft ist.

```
// Tag sender generates new X25519 ephemeral keys
// and sends rapk to tag receiver in a NextKey block
rask = GENERATE_PRIVATE()
rapk = DERIVE_PUBLIC(rask)

// Tag receiver generates new X25519 ephemeral keys
// and sends rbpk to Tag sender in a NextKey block
rbsk = GENERATE_PRIVATE()
rbpk = DERIVE_PUBLIC(rbsk)

sharedSecret = DH(rask, rbpk) = DH(rbsk, rapk)
tagsetKey = HKDF(sharedSecret, ZEROLEN, "XDHRatchetTagSet", 32)
rootKey = nextRootKey // from previous tagset in this direction
newTagSet = DH_INITIALIZE(rootKey, tagsetKey)
```
#### 4b) Session Tag Ratchet

Ratchets für jede Nachricht, wie in Signal. Der Session-Tag-Ratchet ist mit dem symmetrischen Schlüssel-Ratchet synchronisiert, aber der Empfänger-Schlüssel-Ratchet kann "zurückliegen", um Speicher zu sparen.

Der Sender ratchet einmal für jede übertragene Nachricht. Es müssen keine zusätzlichen Tags gespeichert werden. Der Sender muss auch einen Zähler für 'N' führen, die Nachrichtennummer der Nachricht in der aktuellen Kette. Der 'N'-Wert ist in der gesendeten Nachricht enthalten. Siehe die Definition des Message Number-Blocks.

Der Empfänger muss um die maximale Fenstergröße vorwärts ratchet und die Tags in einem "Tag-Set" speichern, das mit der Sitzung verknüpft ist. Nach dem Empfang kann der gespeicherte Tag verworfen werden, und wenn keine vorherigen nicht empfangenen Tags vorhanden sind, kann das Fenster vorgeschoben werden. Der Empfänger sollte den 'N'-Wert für jeden Sitzungs-Tag speichern und prüfen, dass die Nummer in der gesendeten Nachricht mit diesem Wert übereinstimmt. Siehe die Definition des Message Number-Blocks.

##### KDF

Das ist die Definition von RATCHET_TAG().

```
Inputs:
1) Session Tag Chain key sessTag_ck
   First time: output from DH ratchet
   Subsequent times: output from previous session tag ratchet

Generated:
2) input_key_material = SESSTAG_CONSTANT
   Must be unique for this tag set (generated from chain key),
   so that the sequence isn't predictable, since session tags
   go out on the wire in plaintext.

Outputs:
1) N (the current session tag number)
2) the session tag (and symmetric key, probably)
3) the next Session Tag Chain Key (KDF input for the next session tag ratchet)

Initialization:
keydata = HKDF(sessTag_ck, ZEROLEN, "STInitialization", 64)
// Output 1: Next chain key
sessTag_chainKey = keydata[0:31]
// Output 2: The constant
SESSTAG_CONSTANT = keydata[32:63]

// KDF_ST(ck, constant)
keydata_0 = HKDF(sessTag_chainkey, SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
// Output 1: Next chain key
sessTag_chainKey_0 = keydata_0[0:31]
// Output 2: The session tag
// or more if tag is longer than 8 bytes
tag_0 = keydata_0[32:39]

// repeat as necessary to get to tag_n
keydata_n = HKDF(sessTag_chainKey_(n-1), SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
// Output 1: Next chain key
sessTag_chainKey_n = keydata_n[0:31]
// Output 2: The session tag
// or more if tag is longer than 8 bytes
tag_n = keydata_n[32:39]
```
#### 4c) Symmetrischer Schlüssel-Ratchet

Ratchets für jede Nachricht, wie in Signal. Jeder symmetrische Schlüssel hat eine zugehörige Nachrichtennummer und Session-Tag. Der Session-Key-Ratchet ist mit dem symmetrischen Tag-Ratchet synchronisiert, aber der Empfänger-Key-Ratchet kann „zurückbleiben", um Speicher zu sparen.

Der Transmitter ratchet wird für jede übertragene Nachricht einmal ausgeführt. Es müssen keine zusätzlichen Schlüssel gespeichert werden.

Wenn der Empfänger einen session tag erhält und noch nicht den symmetrischen Schlüssel-Ratchet zum zugehörigen Schlüssel vorgerückt hat, muss er zum zugehörigen Schlüssel "aufholen". Der Empfänger wird wahrscheinlich die Schlüssel für alle vorherigen Tags zwischenspeichern, die noch nicht empfangen wurden. Nach dem Empfang kann der gespeicherte Schlüssel verworfen werden, und wenn es keine vorherigen unempfangenen Tags gibt, kann das Fenster vorgerückt werden.

Aus Effizienzgründen sind die session tag und symmetric key ratchets getrennt, sodass der session tag ratchet dem symmetric key ratchet vorauslaufen kann. Dies bietet auch zusätzliche Sicherheit, da die session tags über die Leitung übertragen werden.

##### KDF

Dies ist die Definition von RATCHET_KEY().

```
Inputs:
1) Symmetric Key Chain key symmKey_ck
   First time: output from DH ratchet
   Subsequent times: output from previous symmetric key ratchet

Generated:
2) input_key_material = SYMMKEY_CONSTANT = ZEROLEN
   No need for uniqueness. Symmetric keys never go out on the wire.
   TODO: Set a constant anyway?

Outputs:
1) N (the current session key number)
2) the session key
3) the next Symmetric Key Chain Key (KDF input for the next symmetric key ratchet)

// KDF_CK(ck, constant)
SYMMKEY_CONSTANT = ZEROLEN
// Output 1: Next chain key
keydata_0 = HKDF(symmKey_ck, SYMMKEY_CONSTANT, "SymmetricRatchet", 64)
symmKey_chainKey_0 = keydata_0[0:31]
// Output 2: The symmetric key
k_0 = keydata_0[32:63]

// repeat as necessary to get to k[n]
keydata_n = HKDF(symmKey_chainKey_(n-1), SYMMKEY_CONSTANT, "SymmetricRatchet", 64)
// Output 1: Next chain key
symmKey_chainKey_n = keydata_n[0:31]
// Output 2: The symmetric key
k_n = keydata_n[32:63]
```
### 5) Nutzlast

Dies ersetzt das AES-Abschnittsformat, das in der ElGamal/AES+SessionTags-Spezifikation definiert ist.

Dies verwendet dasselbe Blockformat wie in der [NTCP2](/docs/specs/ntcp2/)-Spezifikation definiert. Einzelne Blocktypen sind unterschiedlich definiert.

Es gibt Bedenken, dass die Ermutigung von Implementierern, Code zu teilen, zu Parsing-Problemen führen könnte. Implementierer sollten sorgfältig die Vorteile und Risiken des Code-Teilens abwägen und sicherstellen, dass die Reihenfolge- und gültigen Block-Regeln für die beiden Kontexte unterschiedlich sind.

#### Payload-Abschnitt Entschlüsselte Daten

Die verschlüsselte Länge entspricht dem verbleibenden Teil der Daten. Die entschlüsselte Länge ist 16 weniger als die verschlüsselte Länge. Alle Blocktypen werden unterstützt. Typische Inhalte umfassen die folgenden Blöcke:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Payload Block Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type Number</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Block Length</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">DateTime</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Termination (TBD)</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">9 typ.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Options (TBD)</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">21+</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Message Number (TBD)</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">TBD</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Next Key</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3 or 35</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">ACK</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4 typ.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">ACK Request</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">9</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Garlic Clove</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">varies</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Padding</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">254</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">varies</td>
</tr>
</table>
#### Unverschlüsselte Daten

Es gibt null oder mehr Blöcke im verschlüsselten Frame. Jeder Block enthält eine Ein-Byte-Kennung, eine Zwei-Byte-Länge und null oder mehr Datenbytes.

Für die Erweiterbarkeit MÜSSEN Empfänger Blöcke mit unbekannten Typnummern ignorieren und sie als Padding behandeln.

Verschlüsselte Daten haben eine maximale Größe von 65535 Bytes, einschließlich eines 16-Byte-Authentifizierungs-Headers, sodass die maximale unverschlüsselte Datenmenge 65519 Bytes beträgt.

(Poly1305-Auth-Tag nicht angezeigt):

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
       0 datetime
       1-3 reserved
       4 termination
       5 options
       6 previous message number
       7 next session key
       8 ack
       9 ack request
       10 reserved
       11 Garlic Clove
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
#### Reihenfolge-Regeln für Blöcke

In der New Session-Nachricht ist der DateTime-Block erforderlich und muss der erste Block sein.

Andere erlaubte Blöcke:

- Garlic Clove (Typ 11)
- Optionen (Typ 5)
- Padding (Typ 254)

In der New Session Reply-Nachricht sind keine Blöcke erforderlich.

Andere erlaubte Blöcke:

- Garlic Clove (Typ 11)
- Optionen (Typ 5)
- Padding (Typ 254)

Keine anderen Blöcke sind erlaubt. Padding, falls vorhanden, muss der letzte Block sein.

In der Existing Session Nachricht sind keine Blöcke erforderlich und die Reihenfolge ist nicht spezifiziert, außer für die folgenden Anforderungen:

Termination, falls vorhanden, muss der letzte Block außer Padding sein. Padding, falls vorhanden, muss der letzte Block sein.

Es können mehrere Garlic Clove-Blöcke in einem einzigen Frame vorhanden sein. Es können bis zu zwei Next Key-Blöcke in einem einzigen Frame vorhanden sein. Mehrere Padding-Blöcke sind in einem einzigen Frame nicht erlaubt. Andere Blocktypen werden wahrscheinlich nicht mehrere Blöcke in einem einzigen Frame haben, aber es ist nicht verboten.

#### DateTime

Ein Ablaufzeitpunkt. Unterstützt die Verhinderung von Replay-Angriffen. Bob muss validieren, dass die Nachricht aktuell ist, unter Verwendung dieses Zeitstempels. Bob muss einen Bloom-Filter oder einen anderen Mechanismus implementieren, um Replay-Angriffe zu verhindern, falls die Zeit gültig ist. Bob kann auch eine frühere Replay-Erkennungsprüfung für einen doppelten ephemeren Schlüssel (entweder vor oder nach der Elligator2-Dekodierung) verwenden, um kürzlich doppelte NS-Nachrichten vor der Entschlüsselung zu erkennen und zu verwerfen. Normalerweise nur in New Session-Nachrichten enthalten.

```
+----+----+----+----+----+----+----+
| 0  |    4    |     timestamp     |
+----+----+----+----+----+----+----+

blk :: 0
size :: 2 bytes, big endian, value = 4
timestamp :: Unix timestamp, unsigned seconds.
             Wraps around in 2106
```
#### Garlic Clove

Eine einzelne entschlüsselte Garlic Clove wie in [I2NP](/docs/specs/i2np/) spezifiziert, mit Änderungen zur Entfernung von Feldern, die ungenutzt oder redundant sind. Warnung: Dieses Format unterscheidet sich erheblich von dem für ElGamal/AES. Jede Clove ist ein separater Payload-Block. Garlic Cloves dürfen nicht über Blöcke oder über ChaChaPoly-Frames fragmentiert werden.

```
+----+----+----+----+----+----+----+----+
| 11 |  size   |                        |
+----+----+----+                        +
|      Delivery Instructions            |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|type|  Message_ID       | Expiration   
+----+----+----+----+----+----+----+----+
     |      I2NP Message body           |
+----+                                  +
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

size :: size of all data to follow

Delivery Instructions :: As specified in
       the Garlic Clove section of [I2NP]_.
       Length varies but is typically 1, 33, or 37 bytes

type :: I2NP message type

Message_ID :: 4 byte `Integer` I2NP message ID

Expiration :: 4 bytes, seconds since the epoch
```
Hinweise:

- Implementierer müssen sicherstellen, dass beim Lesen eines Blocks fehlerhafte oder
  bösartige Daten nicht dazu führen, dass Lesevorgänge in den nächsten Block überlaufen.
- Das in [I2NP](/docs/specs/i2np/) spezifizierte Clove Set Format wird nicht
  verwendet. Jeder Clove ist in seinem eigenen Block enthalten.
- Der I2NP Message Header ist 9 Bytes groß und hat ein identisches Format zu dem,
  das in [NTCP2](/docs/specs/ntcp2/) verwendet wird.
- Das Certificate, die Message ID und die Expiration aus der Garlic Message
  Definition in [I2NP](/docs/specs/i2np/) sind nicht enthalten.
- Das Certificate, die Clove ID und die Expiration aus der Garlic Clove
  Definition in [I2NP](/docs/specs/i2np/) sind nicht enthalten.

#### Beendigung

Implementation ist optional. Beende die Sitzung. Dies muss der letzte Nicht-Padding-Block im Frame sein. In dieser Sitzung werden keine weiteren Nachrichten gesendet.

Nicht erlaubt in NS oder NSR. Nur in Existing Session-Nachrichten enthalten.

```
+----+----+----+----+----+----+----+----+
| 4  |  size   | rsn|     addl data     |
+----+----+----+----+                   +
~               .   .   .               ~
+----+----+----+----+----+----+----+----+

blk :: 4
size :: 2 bytes, big endian, value = 1 or more
rsn :: reason, 1 byte:
       0: normal close or unspecified
       1: termination received
       others: optional, impementation-specific
addl data :: optional, 0 or more bytes, for future expansion, debugging,
             or reason text.
             Format unspecified and may vary based on reason code.
```
#### Optionen

NICHT IMPLEMENTIERT, zur weiteren Untersuchung. Übergabe aktualisierter Optionen. Die Optionen umfassen verschiedene Parameter für die Sitzung. Siehe den Abschnitt "Session Tag Length Analysis" unten für weitere Informationen.

Der Optionsblock kann eine variable Länge haben, da more_options vorhanden sein können.

```
+----+----+----+----+----+----+----+----+
| 5  |  size   |ver |flg |STL |STimeout |
+----+----+----+----+----+----+----+----+
|  SOTW   |  RITW   |tmin|tmax|rmin|rmax|
+----+----+----+----+----+----+----+----+
|  tdmy   |  rdmy   |  tdelay |  rdelay |
+----+----+----+----+----+----+----+----+
|              more_options             |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 5
size :: 2 bytes, big endian, size of options to follow, 21 bytes minimum
ver :: Protocol version, must be 0
flg :: 1 byte flags
       bits 7-0: Unused, set to 0 for future compatibility
STL :: Session tag length (must be 8), other values unimplemented
STimeout :: Session idle timeout (seconds), big endian
SOTW :: Sender Outbound Tag Window, 2 bytes big endian
RITW :: Receiver Inbound Tag Window 2 bytes big endian

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

more_options :: Format undefined, for future use
```
SOTW ist die Empfehlung des Senders an den Empfänger für das eingehende Tag-Fenster des Empfängers (der maximale Lookahead). RITW ist die Erklärung des Senders über das eingehende Tag-Fenster (maximaler Lookahead), das er zu verwenden plant. Jede Seite setzt oder justiert dann den Lookahead basierend auf einem Minimum oder Maximum oder einer anderen Berechnung.

Hinweise:

- Unterstützung für nicht-standardmäßige Session-Tag-Längen wird hoffentlich niemals
  erforderlich sein.
- Das Tag-Fenster ist MAX_SKIP in der Signal-Dokumentation.

Probleme:

- Options-Verhandlung ist noch zu bestimmen.
- Standardwerte sind noch zu bestimmen.
- Padding- und Verzögerungsoptionen werden von NTCP2 übernommen, aber diese Optionen
  wurden dort noch nicht vollständig implementiert oder untersucht.

#### Nachrichtennummern

Die Implementierung ist optional. Die Länge (Anzahl der gesendeten Nachrichten) im vorherigen Tag-Set (PN). Der Empfänger kann Tags höher als PN aus dem vorherigen Tag-Set sofort löschen. Der Empfänger kann Tags kleiner oder gleich PN aus dem vorherigen Tag-Set nach kurzer Zeit (z.B. 2 Minuten) verfallen lassen.

```
+----+----+----+----+----+
| 6  |  size   |  PN    |
+----+----+----+----+----+

blk :: 6
size :: 2
PN :: 2 bytes big endian. The index of the last tag sent in the previous tag set.
```
Hinweise:

- Maximale PN ist 65535.
- Die Definitionen von PN entsprechen der Definition von Signal, minus eins.
  Dies ist ähnlich dem, was Signal macht, aber in Signal sind PN und N im
  Header. Hier sind sie im verschlüsselten Nachrichtentext.
- Senden Sie diesen Block nicht in Tag-Set 0, da es kein vorheriges Tag-
  Set gab.

#### Nächster DH Ratchet Public Key

Der nächste DH ratchet key befindet sich in der Payload und ist optional. Wir führen nicht jedes Mal ein ratchet durch. (Dies unterscheidet sich von Signal, wo er sich im Header befindet und jedes Mal gesendet wird)

Für den ersten Ratchet ist Key ID = 0.

Nicht erlaubt in NS oder NSR. Nur in Existing Session-Nachrichten enthalten.

```
+----+----+----+----+----+----+----+----+
| 7  |  size   |flag|  key ID |         |
+----+----+----+----+----+----+         +
|                                       |
+                                       +
|     Next DH Ratchet Public Key        |
+                                       +
|                                       |
+                             +----+----+
|                             |
+----+----+----+----+----+----+

blk :: 7
size :: 3 or 35
flag :: 1 byte flags
        bit order: 76543210
        bit 0: 1 for key present, 0 for no key present
        bit 1: 1 for reverse key, 0 for forward key
        bit 2: 1 to request reverse key, 0 for no request
               only set if bit 1 is 0
        bits 7-2: Unused, set to 0 for future compatibility
key ID :: The key ID of this key. 2 bytes, big endian
          0 - 32767
Public Key :: The next X25519 public key, 32 bytes, little endian
              Only if bit 0 is 1
```
Hinweise:

- Die Key ID ist ein inkrementierender Zähler für den lokalen Schlüssel, der für diesen Tag-Satz verwendet wird, beginnend bei 0.
- Die ID darf sich nicht ändern, es sei denn, der Schlüssel ändert sich.
- Es ist möglicherweise nicht unbedingt erforderlich, aber nützlich für die Fehlersuche.
  Signal verwendet keine Key ID.
- Die maximale Key ID ist 32767.
- In dem seltenen Fall, dass die Tag-Sätze in beide Richtungen gleichzeitig ratcheting durchführen, enthält ein Frame zwei Next Key-Blöcke, einen für den Forward-Schlüssel und einen für den Reverse-Schlüssel.
- Schlüssel- und Tag-Satz-ID-Nummern müssen sequenziell sein.
- Siehe den DH Ratchet-Abschnitt oben für Details.

#### Bestätigung

Dies wird nur gesendet, wenn ein Bestätigungsanfrage-Block empfangen wurde. Mehrere Bestätigungen können vorhanden sein, um mehrere Nachrichten zu bestätigen.

Nicht erlaubt in NS oder NSR. Nur in Existing Session-Nachrichten enthalten.

```
+----+----+----+----+----+----+----+----+
| 8  |  size   |tagsetid |   N     |    |
+----+----+----+----+----+----+----+    +
|             more acks                 |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 8
size :: 4 * number of acks to follow, minimum 1 ack
for each ack:
tagsetid :: 2 bytes, big endian, from the message being acked
N :: 2 bytes, big endian, from the message being acked
```
Hinweise:

- Die Tag-Set-ID und N identifizieren eindeutig die Nachricht, die bestätigt wird.
- In den ersten Tag-Sets, die für eine Sitzung in jede Richtung verwendet werden, ist die Tag-Set-ID 0.
- Es wurden keine NextKey-Blöcke gesendet, daher gibt es keine Schlüssel-IDs.
- Für alle Tag-Sets, die nach NextKey-Austauschen verwendet werden, ist die Tag-Set-Nummer (1 + Alices Schlüssel-ID + Bobs Schlüssel-ID).

#### Ack-Anfrage

Eine In-Band-Bestätigung anfordern. Um die Out-of-Band DeliveryStatus Message in der Garlic Clove zu ersetzen.

Wenn eine explizite Bestätigung angefordert wird, werden die aktuelle Tagset-ID und Nachrichtennummer (N) in einem Bestätigungsblock zurückgegeben.

Nicht erlaubt in NS oder NSR. Nur in Existing Session-Nachrichten enthalten.

```
+----+----+----+----+
|  9 |  size   |flg |
+----+----+----+----+

blk :: 9
size :: 1
flg :: 1 byte flags
       bits 7-0: Unused, set to 0 for future compatibility
```
#### Padding

Alle Padding-Daten befinden sich innerhalb von AEAD-Frames. TODO Padding innerhalb von AEAD sollte ungefähr den ausgehandelten Parametern entsprechen. TODO Alice hat ihre gewünschten tx/rx min/max Parameter in der NS-Nachricht gesendet. TODO Bob hat seine gewünschten tx/rx min/max Parameter in der NSR-Nachricht gesendet. Aktualisierte Optionen können während der Datenphase gesendet werden. Siehe Informationen zum Optionsblock oben.

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
size :: 2 bytes, big endian, 0-65516
padding :: zeros or random data
```
Hinweise:

- Nullen-Padding ist in Ordnung, da es verschlüsselt wird.
- Padding-Strategien sind noch festzulegen.
- Reine Padding-Frames sind erlaubt.
- Standard-Padding beträgt 0-15 Bytes.
- Siehe Optionsblock für Padding-Parameter-Verhandlung
- Siehe Optionsblock für min/max Padding-Parameter
- Die router-Antwort bei Verletzung der verhandelten Padding-Parameter ist
  implementierungsabhängig.

#### Andere Blocktypen

Implementierungen sollten unbekannte Blocktypen ignorieren, um Vorwärtskompatibilität zu gewährleisten.

#### Zukünftige Arbeiten

- Die Padding-Länge soll entweder nachrichtenweise entschieden werden basierend auf Schätzungen der Längenverteilung, oder es sollen zufällige Verzögerungen hinzugefügt werden. Diese Gegenmaßnahmen sind zu implementieren, um DPI zu widerstehen, da Nachrichtengrößen andernfalls preisgeben würden, dass I2P-Traffic über das Transportprotokoll übertragen wird. Das genaue Padding-Schema ist ein Bereich zukünftiger Arbeit, Anhang A bietet weitere Informationen zu diesem Thema.

## Typische Verwendungsmuster

### HTTP GET

Dies ist der typischste Anwendungsfall, und die meisten Nicht-HTTP-Streaming-Anwendungsfälle werden ebenfalls identisch zu diesem Anwendungsfall sein. Eine kleine anfängliche Nachricht wird gesendet, eine Antwort folgt, und zusätzliche Nachrichten werden in beide Richtungen gesendet.

Ein HTTP GET passt normalerweise in eine einzelne I2NP-Nachricht. Alice sendet eine kleine Anfrage mit einer einzigen neuen Session-Nachricht und bündelt ein Antwort-leaseSet. Alice schließt sofortiges Ratcheting zu einem neuen Schlüssel ein. Enthält Signatur zur Bindung an das Ziel. Keine Bestätigung angefordert.

Bob führt sofort ein Ratcheting durch.

Alice führt sofort ein Ratcheting durch.

Setzt mit diesen Sessions fort.

```
Alice                           Bob

  New Session (1b)     ------------------->
  with ephemeral key 1
  with static key for binding
  with next key
  with bundled HTTP GET
  with bundled LS
  without bundled Delivery Status Message

  any retransmissions, same as above

  following messages may arrive in any order:

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 1
                      with bundled HTTP reply part 1

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 2
                      with bundled HTTP reply part 2

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 3
                      with bundled HTTP reply part 3

  After reception of any of these messages,
  Alice switches to use Existing Session messages,
  creates a new inbound + outbound session pair,
  and ratchets.


  Existing Session     ------------------->
  with bundled streaming ack


  Existing Session     ------------------->
  with bundled streaming ack


  After reception of any of these messages,
  Bob switches to use Existing Session messages.


  <--------------     Existing Session
                      with bundled HTTP reply part 4


  Existing Session     ------------------->
  with bundled streaming ack

  <--------------     Existing Session
                      with bundled HTTP reply part 5
```
### HTTP POST

Alice hat drei Optionen:

1)  Sende nur die erste Nachricht (Fenstergröße = 1), wie bei HTTP GET. Nicht

    recommended.
2)  Sende bis zum Streaming-Fenster, aber verwende dasselbe Elligator2-kodierte

    cleartext public key. All messages contain same next public key
    (ratchet). This will be visible to OBGW/IBEP because they all start
    with the same cleartext. Things proceed as in 1). Not recommended.
3)  Empfohlene Implementierung. Sende bis zum Streaming-Fenster, aber verwende ein

    different Elligator2-encoded cleartext public key (session) for
    each. All messages contain same next public key (ratchet). This will
    not be visible to OBGW/IBEP because they all start with different
    cleartext. Bob must recognize that they all contain the same next
    public key, and respond to all with the same ratchet. Alice uses
    that next public key and continues.

Option 3 Nachrichtenfluss:

```
Alice                           Bob

  New Session (1b)     ------------------->
  with ephemeral key 1
  with static key for binding
  with bundled HTTP POST part 1
  with bundled LS
  without bundled Delivery Status Message


  New Session (1b)     ------------------->
  with ephemeral key 2
  with static key for binding
  with bundled HTTP POST part 2
  with bundled LS
  without bundled Delivery Status Message


  New Session (1b)     ------------------->
  with ephemeral key 3
  with static key for binding
  with bundled HTTP POST part 3
  with bundled LS
  without bundled Delivery Status Message


  following messages can arrive in any order:

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 1
                      with bundled streaming ack

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 2
                      with bundled streaming ack

  After reception of any of these messages,
  Alice switches to use Existing Session messages,
  creates a new inbound + outbound session pair,
  and ratchets.


  following messages can arrive in any order:


  Existing Session     ------------------->
  with bundled HTTP POST part 4

  Existing Session     ------------------->
  with next key
  with bundled HTTP POST part 5


  After reception of any of these messages,
  Bob switches to use Existing Session messages.


  <--------------     Existing Session
                      with bundled streaming ack

  After reception of any of this message,
  Alice switches to use Existing Session messages,
  and Alice ratchets.


  Existing Session     ------------------->
  with next key
  with bundled HTTP POST part 4

  after reception of this message, Bob ratchets

  Existing Session     ------------------->
  with next key
  with bundled HTTP POST part 5

  <--------------     Existing Session
                      with bundled streaming ack
```
### Replizierbares Datagramm

Eine einzelne Nachricht, mit einer einzelnen erwarteten Antwort. Zusätzliche Nachrichten oder Antworten können gesendet werden.

Ähnlich wie HTTP GET, aber mit kleineren Optionen für die Session-Tag-Fenstergröße und Lebensdauer. Möglicherweise sollte kein ratchet angefordert werden.

```
Alice                           Bob

  New Session (1b)     ------------------->
  with static key for binding
  with next key
  with bundled repliable datagram
  with bundled LS
  without bundled Delivery Status Message


  <--------------     New Session Reply (1g)
                      with Bob ephemeral key
                      with bundled reply part 1

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key
                      with bundled reply part 2

  After reception of either message,
  Alice switches to use Existing Session messages,
  and ratchets.

  If the Existing Session message arrives first,
  Alice ratchets on the existing inbound and outbound
  sessions.

  When the New Session Reply arrives, Alice
  sets the existing inbound session to expire,
  creates a new inbound and outbound session,
  and sends Existing Session messages on
  the new outbound session.

  Alice keeps the expiring inbound session
  around for a while to process the Existing Session
  message sent to Alice.
  If all expected original Existing Session message replies
  have been processed, Alice can expire the original
  inbound session immediately.

  if there are any other messages:

  Existing Session     ------------------->
  with bundled message

  Existing Session     ------------------->
  with bundled streaming ack

  <--------------     Existing Session
                      with bundled message
```
### Mehrere Raw-Datagramme

Mehrere anonyme Nachrichten, ohne erwartete Antworten.

In diesem Szenario fordert Alice eine Session an, aber ohne Bindung. Eine neue Session-Nachricht wird gesendet. Keine Antwort-LS wird gebündelt. Eine Antwort-DSM wird gebündelt (dies ist der einzige Anwendungsfall, der gebündelte DSMs erfordert). Kein nächster Schlüssel ist enthalten. Keine Antwort oder ratchet wird angefordert. Kein ratchet wird gesendet. Die Optionen setzen das Session-Tags-Fenster auf null.

```
Alice                           Bob

  New Session (1c)     ------------------->
  with bundled message
  without bundled LS
  with bundled Delivery Status Message 1

  New Session (1c)     ------------------->
  with bundled message
  without bundled LS
  with bundled Delivery Status Message 2

  New Session (1c)     ------------------->
  with bundled message
  without bundled LS
  with bundled Delivery Status Message 3
 
  following messages can arrive in any order:

  <--------------     Delivery Status Message 1

  <--------------     Delivery Status Message 2

  <--------------     Delivery Status Message 3

  After reception of any of these messages,
  Alice switches to use Existing Session messages.

  Existing Session     ------------------->

  Existing Session     ------------------->

  Existing Session     ------------------->
```
### Einzelnes Raw-Datagramm

Eine einzelne anonyme Nachricht, ohne erwartete Antwort.

Einmalige Nachricht wird gesendet. Keine Antwort-LS oder DSM sind gebündelt. Kein nächster Schlüssel ist enthalten. Keine Antwort oder Ratsche wird angefordert. Keine Ratsche wird gesendet. Optionen setzen das Session-Tags-Fenster auf null.

```
Alice                           Bob

  One-Time Message (1d)   ------------------->
  with bundled message
  without bundled LS
  without bundled Delivery Status Message
```
### Langlebige Sitzungen

Langlebige Sitzungen können jederzeit ein Ratcheting durchführen oder anfordern, um die Forward Secrecy ab diesem Zeitpunkt aufrechtzuerhalten. Sitzungen müssen ein Ratcheting durchführen, wenn sie sich dem Limit gesendeter Nachrichten pro Sitzung (65535) nähern.

## Implementierungsüberlegungen

### Verteidigung

Wie bei dem bestehenden ElGamal/AES+SessionTag-Protokoll müssen Implementierungen die Speicherung von Session-Tags begrenzen und sich vor Angriffen zum Erschöpfen des Arbeitsspeichers schützen.

Einige empfohlene Strategien umfassen:

- Harte Begrenzung der Anzahl gespeicherter Session-Tags
- Aggressive Ablaufzeiten für inaktive eingehende Sessions bei 
  Speicherdruck
- Begrenzung der Anzahl eingehender Sessions, die an ein einzelnes 
  entferntes Ziel gebunden sind
- Adaptive Reduzierung des Session-Tag-Fensters und Löschung alter 
  ungenutzter Tags bei Speicherdruck
- Verweigerung des Ratcheting auf Anfrage bei Speicherdruck

### Parameter

Empfohlene Parameter und Timeouts:

- NSR tagset Größe: 12 tsmin und tsmax
- ES tagset 0 Größe: tsmin 24, tsmax 160
- ES tagset (1+) Größe: 160 tsmin und tsmax
- NSR tagset Timeout: 3 Minuten für Empfänger
- ES tagset Timeout: 8 Minuten für Sender, 10 Minuten für Empfänger
- Vorheriges ES tagset entfernen nach: 3 Minuten
- Tagset Look-ahead von Tag N: min(tsmax, tsmin + N/4)
- Tagset Trim hinter Tag N: min(tsmax, tsmin + N/4) / 2
- Nächsten Schlüssel senden bei Tag: 4096
- Nächsten Schlüssel senden nach tagset Lebensdauer: TBD
- Session ersetzen wenn NS empfangen nach: 3 Minuten
- Max Uhrabweichung: -5 Minuten bis +2 Minuten
- NS Replay-Filter Dauer: 5 Minuten
- Padding Größe: 0-15 Bytes (andere Strategien TBD)

### Klassifikation

Im Folgenden finden Sie Empfehlungen für die Klassifizierung eingehender Nachrichten.

#### Nur X25519

Bei einem tunnel, der ausschließlich mit diesem Protokoll verwendet wird, führe die Identifikation wie derzeit mit ElGamal/AES+SessionTags durch:

Zuerst behandeln Sie die Anfangsdaten als Session-Tag und schlagen das Session-Tag nach. Falls gefunden, entschlüsseln Sie mit den gespeicherten Daten, die mit diesem Session-Tag verknüpft sind.

Falls nicht gefunden, behandeln Sie die anfänglichen Daten als DH öffentlichen Schlüssel und Nonce. Führen Sie eine DH-Operation und die angegebene KDF durch und versuchen Sie, die verbleibenden Daten zu entschlüsseln.

#### X25519 geteilt mit ElGamal/AES+SessionTags

Auf einem tunnel, der sowohl dieses Protokoll als auch ElGamal/AES+SessionTags unterstützt, klassifiziere eingehende Nachrichten wie folgt:

Aufgrund eines Fehlers in der ElGamal/AES+SessionTags-Spezifikation wird der AES-Block nicht auf eine zufällige Länge aufgefüllt, die nicht durch 16 teilbar ist. Daher ist die Länge von Existing Session-Nachrichten modulo 16 immer 0, und die Länge von New Session-Nachrichten modulo 16 ist immer 2 (da der ElGamal-Block 514 Bytes lang ist).

Wenn die Länge mod 16 nicht 0 oder 2 ist, behandle die anfänglichen Daten als session tag und suche nach dem session tag. Falls gefunden, entschlüssele mit den gespeicherten Daten, die mit diesem session tag verknüpft sind.

Wenn nicht gefunden und die Länge modulo 16 nicht 0 oder 2 ist, behandeln Sie die anfänglichen Daten als DH-Public-Key und Nonce. Führen Sie eine DH-Operation und die angegebene KDF durch und versuchen Sie, die verbleibenden Daten zu entschlüsseln. (basierend auf der relativen Verkehrsmischung und den relativen Kosten von X25519- und ElGamal-DH-Operationen kann dieser Schritt stattdessen zuletzt durchgeführt werden)

Andernfalls, wenn die Länge mod 16 gleich 0 ist, behandeln Sie die ursprünglichen Daten als ElGamal/AES session tag und suchen Sie den session tag auf. Falls gefunden, entschlüsseln Sie mit den gespeicherten Daten, die mit diesem session tag verknüpft sind.

Wenn nicht gefunden, und die Daten mindestens 642 (514 + 128) Bytes lang sind, und die Länge modulo 16 gleich 2 ist, behandle die anfänglichen Daten als ElGamal-Block. Versuche, die verbleibenden Daten zu entschlüsseln.

Beachte, dass wenn die ElGamal/AES+SessionTag Spezifikation aktualisiert wird, um nicht-mod-16 Padding zu erlauben, die Dinge anders gemacht werden müssen.

### Neuübertragungen und Zustandsübergänge

Die ratchet-Schicht führt keine Neuübertragungen durch und verwendet mit zwei Ausnahmen keine Timer für Übertragungen. Timer sind auch für das tagset-Timeout erforderlich.

Übertragungstimer werden nur zum Senden von NSR und zum Antworten mit einer ES verwendet, wenn eine empfangene ES eine ACK-Anfrage enthält. Die empfohlene Zeitüberschreitung beträgt eine Sekunde. In fast allen Fällen wird die höhere Schicht (Datagramm oder Streaming) antworten, was eine NSR oder ES erzwingt, und der Timer kann abgebrochen werden. Wenn der Timer dennoch ausgelöst wird, sende eine leere Nutzlast mit der NSR oder ES.

#### Ratchet-Layer-Antworten

Erste Implementierungen basieren auf bidirektionalem Verkehr in den höheren Schichten. Das heißt, die Implementierungen gehen davon aus, dass bald Verkehr in die entgegengesetzte Richtung übertragen wird, was eine erforderliche Antwort auf der ECIES-Schicht erzwingen wird.

Bestimmter Datenverkehr kann jedoch unidirektional oder mit sehr geringer Bandbreite sein, sodass kein höherschichtiger Datenverkehr vorhanden ist, um eine rechtzeitige Antwort zu generieren.

Der Empfang von NS- und NSR-Nachrichten erfordert eine Antwort; der Empfang von ACK Request- und Next Key-Blöcken erfordert ebenfalls eine Antwort.

Implementierungen sollten einen Timer starten, wenn eine dieser Nachrichten empfangen wird, die eine Antwort erfordert, und eine "leere" Antwort (ohne Garlic Clove Block) auf der ECIES-Ebene generieren, falls kein Rückverkehr in einem kurzen Zeitraum gesendet wird (z.B. 1 Sekunde).

Es könnte auch angemessen sein, eine noch kürzere Zeitüberschreitung für Antworten auf NS- und NSR-Nachrichten zu verwenden, um den Verkehr so schnell wie möglich zu den effizienten ES-Nachrichten zu verlagern.

#### NS-Bindung für NSR

Auf der Ratchet-Ebene ist Alice für Bob nur durch den statischen Schlüssel bekannt. Die NS-Nachricht ist authentifiziert ([Noise](https://noiseprotocol.org/noise.html) IK Sender-Authentifizierung 1). Dies reicht jedoch nicht aus, damit die Ratchet-Ebene etwas an Alice senden kann, da das Netzwerk-Routing eine vollständige Destination erfordert.

Bevor die NSR gesendet werden kann, muss Alices vollständige Destination entweder durch die Ratchet-Schicht oder ein höherschichtiges antwortfähiges Protokoll entdeckt werden, entweder antwortfähige [Datagrams](/docs/specs/datagrams/) oder [Streaming](/docs/specs/streaming/). Nach dem Auffinden des LeaseSet für diese Destination wird dieses LeaseSet denselben statischen Schlüssel enthalten, der auch in der NS enthalten ist.

Typischerweise wird die höhere Schicht antworten und eine Netzwerkdatenbank-Suche nach Alices Leaseset anhand von Alices Destination Hash erzwingen. Dieses Leaseset wird fast immer lokal gefunden, da die NS einen Garlic Clove Block enthielt, der eine Database Store Nachricht enthielt, die Alices Leaseset beinhaltete.

Damit Bob bereit ist, eine ratchet-layer NSR zu senden und die ausstehende Sitzung an Alices Destination zu binden, sollte Bob die Destination während der Verarbeitung der NS-Nutzlast "erfassen". Wenn eine Database Store-Nachricht gefunden wird, die ein Leaseset mit einem Schlüssel enthält, der dem statischen Schlüssel in der NS entspricht, ist die ausstehende Sitzung nun an diese Destination gebunden, und Bob weiß, wohin er eine NSR senden soll, falls der Antwort-Timer abläuft. Dies ist die empfohlene Implementierung.

Ein alternativer Ansatz besteht darin, einen Cache oder eine Datenbank zu führen, in der der statische Schlüssel einer Destination zugeordnet wird. Die Sicherheit und Praktikabilität dieses Ansatzes ist ein Thema für weitere Untersuchungen.

Weder diese Spezifikation noch andere verlangen strikt, dass jede NS Alices Leaseset enthält. In der Praxis sollte sie es jedoch tun. Das empfohlene ES-Tagset-Sender-Timeout (8 Minuten) ist kürzer als das maximale Leaseset-Timeout (10 Minuten), sodass es ein kleines Zeitfenster geben könnte, in dem die vorherige Sitzung abgelaufen ist, Alice denkt, dass Bob noch ihr gültiges Leaseset hat, und kein neues Leaseset mit der neuen NS sendet. Dies ist ein Thema für weitere Untersuchungen.

#### Mehrere NS-Nachrichten

Wenn keine NSR-Antwort empfangen wird, bevor die höhere Schicht (Datagramm oder Streaming) weitere Daten sendet, möglicherweise als Neuübertragung, muss Alice eine neue NS erstellen und dabei einen neuen ephemeren Schlüssel verwenden. Der ephemere Schlüssel von einer vorherigen NS darf nicht wiederverwendet werden. Alice muss den zusätzlichen Handshake-Zustand und das abgeleitete Empfangs-Tagset beibehalten, um NSR-Nachrichten als Antwort auf jede gesendete NSR zu empfangen.

Implementierungen können die Gesamtzahl der gesendeten NS-Nachrichten oder die Rate des NS-Nachrichtenversands begrenzen, entweder durch Warteschlangen oder durch das Verwerfen von Nachrichten höherer Schichten, bevor sie gesendet werden.

In bestimmten Situationen, bei hoher Belastung oder unter bestimmten Angriffsszenarien kann es für Bob angemessen sein, scheinbare NS-Nachrichten in die Warteschlange einzureihen, zu verwerfen oder zu begrenzen, ohne zu versuchen sie zu entschlüsseln, um einen Ressourcenerschöpfungsangriff zu vermeiden.

Für jede empfangene NS generiert Bob ein NSR outbound tagset, sendet eine NSR, führt ein split() aus und generiert die inbound und outbound ES tagsets. Bob sendet jedoch keine ES-Nachrichten, bis die erste ES-Nachricht auf dem entsprechenden inbound tagset empfangen wird. Danach kann Bob alle handshake-Zustände und tagsets für alle anderen empfangenen NS oder gesendeten NSR verwerfen oder sie kurz darauf ablaufen lassen. Verwenden Sie NSR tagsets nicht für ES-Nachrichten.

Es ist ein Thema für weitere Untersuchungen, ob Bob spekulativ ES-Nachrichten unmittelbar nach der NSR senden kann, noch bevor er die erste ES von Alice erhält. In bestimmten Szenarien und Verkehrsmustern könnte dies erhebliche Bandbreite und CPU-Leistung sparen. Diese Strategie könnte auf Heuristiken basieren, wie z.B. Verkehrsmustern, dem Prozentsatz der auf dem Tagset der ersten Sitzung empfangenen ESs oder anderen Daten.

#### Mehrere NSR-Nachrichten

Für jede empfangene NS-Nachricht muss Bob mit einer neuen NSR antworten, bis eine ES-Nachricht empfangen wird, entweder aufgrund von Traffic höherer Schichten oder durch Ablauf des NSR-Sendetimers.

Jede NSR verwendet den Handshake-Status und Tagset, der der eingehenden NS entspricht. Bob muss den Handshake-Status und Tagset für alle empfangenen NS-Nachrichten aufrechterhalten, bis eine ES-Nachricht empfangen wird.

Implementierungen können die Gesamtanzahl der gesendeten NSR-Nachrichten oder die Senderate von NSR-Nachrichten begrenzen, entweder durch Warteschlangen oder durch Verwerfen von Nachrichten höherer Schichten, bevor sie gesendet werden. Diese können sowohl bei eingehenden NS-Nachrichten als auch bei zusätzlichem ausgehenden Verkehr höherer Schichten begrenzt werden.

In bestimmten Situationen, bei hoher Last oder unter bestimmten Angriffsszenarien kann es für Alice angebracht sein, NSR-Nachrichten in die Warteschlange einzureihen, zu verwerfen oder zu begrenzen, ohne zu versuchen sie zu entschlüsseln, um einen Angriff auf die Ressourcenerschöpfung zu vermeiden. Diese Grenzen können entweder insgesamt über alle Sitzungen hinweg, pro Sitzung oder beides gelten.

Sobald Alice eine NSR erhält, führt Alice eine split()-Operation durch, um die ES-Sitzungsschlüssel abzuleiten. Alice sollte einen Timer setzen und eine leere ES-Nachricht senden, falls die höhere Schicht keinen Datenverkehr sendet, typischerweise innerhalb einer Sekunde.

Die anderen eingehenden NSR-Tagsets können bald entfernt werden oder ablaufen, aber Alice sollte sie für eine kurze Zeit behalten, um alle anderen NSR-Nachrichten zu entschlüsseln, die empfangen werden.

### Schutz vor Wiederholungsangriffen

Bob muss einen Bloom-Filter oder anderen Mechanismus implementieren, um NS-Replay-Angriffe zu verhindern, wenn die enthaltene DateTime aktuell ist, und NS-Nachrichten ablehnen, bei denen die DateTime zu alt ist. Bob kann auch eine frühere Replay-Erkennungsprüfung für einen doppelten ephemeren Schlüssel (entweder vor oder nach der Elligator2-Dekodierung) verwenden, um kürzlich doppelte NS-Nachrichten vor der Entschlüsselung zu erkennen und zu verwerfen.

NSR- und ES-Nachrichten haben einen inhärenten Schutz vor Replay-Angriffen, da der Session-Tag nur einmal verwendet werden kann.

Garlic-Nachrichten haben auch einen Schutz vor Replay-Angriffen, wenn der Router einen router-weiten Bloom-Filter basierend auf der I2NP-Nachrichten-ID implementiert.

## Verwandte Änderungen

Datenbankabfragen von ECIES-Zielen: Siehe [Prop154](/proposals/154-ratchet/), jetzt eingearbeitet in [I2NP](/docs/specs/i2np/) für Version 0.9.46.

Diese Spezifikation erfordert LS2-Unterstützung, um den X25519 öffentlichen Schlüssel mit dem leaseSet zu veröffentlichen. Es sind keine Änderungen an den LS2-Spezifikationen in [I2NP](/docs/specs/i2np/) erforderlich. Die gesamte Unterstützung wurde in [Prop123](/proposals/123-new-netdb-entries/) entworfen, spezifiziert und implementiert, welches in Version 0.9.38 umgesetzt wurde.

Diese Spezifikation erfordert, dass eine Eigenschaft in den I2CP-Optionen gesetzt wird, um aktiviert zu werden. Alle Unterstützung wurde entworfen, spezifiziert und implementiert in [Prop123](/proposals/123-new-netdb-entries/), umgesetzt in 0.9.38.

Die Option, die zum Aktivieren von ECIES erforderlich ist, ist eine einzelne I2CP-Eigenschaft für I2CP, BOB, SAM oder i2ptunnel.

Typische Werte sind i2cp.leaseSetEncType=4 für nur ECIES, oder i2cp.leaseSetEncType=4,0 für ECIES und ElGamal Dual-Schlüssel.

## Kompatibilität

Jeder router, der LS2 mit dualen Schlüsseln unterstützt (0.9.38 oder höher), sollte Verbindungen zu Zielen mit dualen Schlüsseln unterstützen.

ECIES-only-Ziele erfordern, dass eine Mehrheit der floodfills auf 0.9.46 aktualisiert wird, um verschlüsselte Lookup-Antworten zu erhalten. Siehe [Prop154](/proposals/154-ratchet/).

ECIES-only Ziele können sich nur mit anderen Zielen verbinden, die entweder ebenfalls ECIES-only oder dual-key sind.

## Referenzen

- [Common](/docs/specs/common-structures/)
- [CRYPTO-ELG](/docs/specs/cryptography/#elgamal)
- [Datagrams](/docs/specs/datagrams/)
- [ECIES-HYBRID](/docs/specs/ecies-hybrid/)
- [ElG-AES](/docs/specs/elgamal-aes/)
- [Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf) - Siehe auch [Elligator-Artikel](https://www.imperialviolet.org/2013/12/25/elligator.html) und OBFS4-Code
- [GARLICSPEC](/docs/overview/garlic-routing/)
- [I2CP](/docs/specs/i2cp/)
- [I2NP](/docs/specs/i2np/)
- [NOISE](https://noiseprotocol.org/noise.html)
- [NTCP2](/docs/specs/ntcp2/)
- [Prop111](/proposals/111-ntcp2/)
- [Prop123](/proposals/123-new-netdb-entries/)
- [Prop142](/proposals/142-ecies-template/)
- [Prop144](/proposals/144-ecies-x25519/)
- [Prop145](/proposals/145-ecies-ecdh-aes/)
- [Prop152](/proposals/152-ecies-config/)
- [Prop153](/proposals/153-chacha20-layer/)
- [Prop154](/proposals/154-ratchet/)
- [RFC-2104](https://tools.ietf.org/html/rfc2104)
- [RFC-4880-S5.1](https://tools.ietf.org/html/rfc4880#section-5.1)
- [RFC-5869](https://tools.ietf.org/html/rfc5869)
- [RFC-7539](https://tools.ietf.org/html/rfc7539)
- [RFC-7748](https://tools.ietf.org/html/rfc7748)
- [RFC-7905](https://tools.ietf.org/html/rfc7905)
- [Signal](https://signal.org/docs/specifications/doubleratchet/)
- [SSU](/docs/transport/ssu/)
- [SSU2](/docs/specs/ssu2/)
- [STS](https://en.wikipedia.org/wiki/Station-to-Station_protocol) - Diffie, W.; van Oorschot P. C.; Wiener M. J., Authentication and Authenticated Key Exchanges
- [Streaming](/docs/specs/streaming/)
