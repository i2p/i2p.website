---
title: "ECIES-X25519-AEAD-Ratchet"
number: "144"
author: "zzz, chisana, orignal"
created: "2018-11-22"
lastupdated: "2025-03-05"
status: "Geschlossen"
thread: "http://zzz.i2p/topics/2639"
target: "0.9.46"
implementedin: "0.9.46"
toc: true
---

## Hinweis

Netzwerk-Bereitstellung und Tests in Arbeit. Unterliegt kleineren Überarbeitungen. Siehe [SPEC](/docs/specs/ecies/) für die offizielle Spezifikation.

Die folgenden Funktionen sind ab Version 0.9.46 nicht implementiert:

- MessageNumbers, Options, und Termination Blocks
- Protocol-Layer-Antworten
- Zero Static Key
- Multicast

## Überblick

Dies ist ein Vorschlag für den ersten neuen End-to-End-Verschlüsselungstyp seit den Anfängen von I2P, um ElGamal/AES+SessionTags [Elg-AES](/docs/legacy/elgamal-aes/) zu ersetzen.

Es basiert auf folgenden Vorarbeiten:

- Common Structures Spezifikation [Common Structures](/docs/specs/common-structures/)
- [I2NP](/docs/specs/i2np/) Spezifikation einschließlich LS2
- ElGamal/AES+Session Tags [Elg-AES](/docs/legacy/elgamal-aes/)
- [http://zzz.i2p/topics/1768](http://zzz.i2p/topics/1768) Überblick über neue asymmetrische Kryptographie
- Low-Level-Kryptographie-Überblick [CRYPTO-ELG](/docs/specs/cryptography/)
- ECIES [http://zzz.i2p/topics/2418](http://zzz.i2p/topics/2418)
- [NTCP2](/docs/specs/ntcp2/) [Proposal 111](/proposals/111-ntcp-2/)
- 123 Neue netDB-Einträge
- 142 Neue Krypto-Vorlage
- [Noise](https://noiseprotocol.org/noise.html) Protokoll
- [Signal](https://signal.org/docs/) Double Ratchet Algorithmus

Das Ziel ist es, neue Verschlüsselung für End-to-End-, Destination-zu-Destination-Kommunikation zu unterstützen.

Das Design wird einen Noise-Handshake und eine Datenphase verwenden, die Signals Double Ratchet einbezieht.

Alle Verweise auf Signal und Noise in diesem Vorschlag dienen nur als Hintergrundinformation. Kenntnisse der Signal- und Noise-Protokolle sind nicht erforderlich, um diesen Vorschlag zu verstehen oder zu implementieren.

### Current ElGamal Uses

Zur Wiederholung: ElGamal 256-Byte öffentliche Schlüssel können in den folgenden Datenstrukturen gefunden werden. Siehe die Spezifikation der gemeinsamen Strukturen.

- In einer Router Identity
  Dies ist der Verschlüsselungsschlüssel des Routers.

- In einer Destination
  Der öffentliche Schlüssel der Destination wurde für die alte i2cp-zu-i2cp-Verschlüsselung verwendet,
  die in Version 0.6 deaktiviert wurde. Er wird derzeit nicht verwendet, außer für
  den IV für LeaseSet-Verschlüsselung, welche veraltet ist.
  Stattdessen wird der öffentliche Schlüssel im LeaseSet verwendet.

- In einem LeaseSet
  Dies ist der Verschlüsselungsschlüssel des Ziels.

- In einem LS2
  Das ist der Verschlüsselungsschlüssel des Ziels.

### EncTypes in Key Certs

Zur Wiederholung: Wir haben Unterstützung für Verschlüsselungstypen hinzugefügt, als wir Unterstützung für Signaturtypen hinzugefügt haben. Das Verschlüsselungstyp-Feld ist immer null, sowohl in Destinations als auch RouterIdentities. Ob das jemals geändert werden soll, ist noch zu bestimmen. Siehe die Spezifikation für gemeinsame Strukturen [Common Structures](/docs/specs/common-structures/).

### Aktuelle ElGamal-Anwendungen

Zur Wiederholung, wir verwenden ElGamal für:

1) Tunnel Build-Nachrichten (Schlüssel ist in RouterIdentity)    Der Ersatz ist in diesem Vorschlag nicht abgedeckt.    Siehe Vorschlag 152 [Proposal 152](/proposals/152-ecies-tunnels).

2) Router-zu-Router-Verschlüsselung von netDb und anderen I2NP-Nachrichten (Schlüssel ist in RouterIdentity)    Hängt von diesem Vorschlag ab.    Erfordert auch einen Vorschlag für 1) oder das Einfügen des Schlüssels in die RI-Optionen.

3) Client End-to-End ElGamal+AES/SessionTag (Schlüssel ist im LeaseSet, der Destination-Schlüssel wird nicht verwendet)    Ersetzung IST in diesem Vorschlag abgedeckt.

4) Ephemeral DH für NTCP1 und SSU    Ersatz wird in diesem Vorschlag nicht behandelt.    Siehe Vorschlag 111 für NTCP2.    Kein aktueller Vorschlag für SSU2.

### EncTypes in Key Certs

- Rückwärts kompatibel
- Erfordert und baut auf LS2 auf (Vorschlag 123)
- Nutzt neue Kryptografie oder Primitive, die für NTCP2 hinzugefügt wurden (Vorschlag 111)
- Keine neuen kryptografischen Verfahren oder Primitive für die Unterstützung erforderlich
- Beibehaltung der Entkopplung von Kryptografie und Signierung; Unterstützung aller aktuellen und zukünftigen Versionen
- Ermöglicht neue Kryptografie für Ziele
- Ermöglicht neue Kryptografie für router, aber nur für garlic-Nachrichten - Tunnel-Aufbau wäre ein separater Vorschlag
- Bricht nichts, was auf 32-Byte binäre Ziel-Hashes angewiesen ist, z.B. BitTorrent
- Beibehaltung der 0-RTT Nachrichtenzustellung mit ephemeral-static DH
- Erfordert kein Puffern/Einreihen von Nachrichten auf dieser Protokollebene;
  unterstützt weiterhin unbegrenzte Nachrichtenzustellung in beide Richtungen ohne Warten auf eine Antwort
- Upgrade auf ephemeral-ephemeral DH nach 1 RTT
- Beibehaltung der Behandlung von Nachrichten außerhalb der Reihenfolge
- Beibehaltung der 256-Bit-Sicherheit
- Hinzufügen von Forward Secrecy
- Hinzufügen von Authentifizierung (AEAD)
- Viel CPU-effizienter als ElGamal
- Keine Abhängigkeit von Java jbigi für effizientes DH
- Minimierung von DH-Operationen
- Viel bandbreiteneffizienter als ElGamal (514-Byte ElGamal-Block)
- Unterstützung neuer und alter Kryptografie im selben Tunnel falls gewünscht
- Empfänger kann neue von alter Kryptografie effizient unterscheiden, die
  über denselben Tunnel kommt
- Andere können neue von alter oder zukünftiger Kryptografie nicht unterscheiden
- Eliminierung der Klassifizierung der Länge neuer vs. bestehender Sitzungen (Unterstützung von Padding)
- Keine neuen I2NP-Nachrichten erforderlich
- Ersetzung der SHA-256-Prüfsumme in der AES-Payload durch AEAD
- Unterstützung der Bindung von Sende- und Empfangssitzungen, damit
  Bestätigungen innerhalb des Protokolls stattfinden können, anstatt ausschließlich out-of-band.
  Dies ermöglicht auch, dass Antworten sofort Forward Secrecy haben.
- Ermöglicht End-to-End-Verschlüsselung bestimmter Nachrichten (RouterInfo-Stores),
  die wir derzeit aufgrund des CPU-Overheads nicht verwenden.
- Ändert nicht das I2NP Garlic Message
  oder Garlic Message Delivery Instructions Format.
- Eliminierung ungenutzter oder redundanter Felder in den Garlic Clove Set und Clove Formaten.

Beseitigen Sie mehrere Probleme mit Session-Tags, einschließlich:

- Unfähigkeit, AES bis zur ersten Antwort zu verwenden
- Unzuverlässigkeit und Stillstände bei angenommener Tag-Zustellung
- Bandbreiteneffizient, besonders bei der ersten Zustellung
- Große Speicherineffizienz zur Tag-Speicherung
- Großer Bandbreiten-Overhead zur Tag-Zustellung
- Sehr komplex, schwierig zu implementieren
- Schwierig abzustimmen für verschiedene Anwendungsfälle
  (Streaming vs. Datagramme, Server vs. Client, hohe vs. niedrige Bandbreite)
- Speichererschöpfungsschwachstellen durch Tag-Zustellung

### Verwendung asymmetrischer Kryptographie

- LS2-Formatänderungen (Vorschlag 123 ist abgeschlossen)
- Neuer DHT-Rotationsalgorithmus oder gemeinsame Zufallszahlengenerierung
- Neue Verschlüsselung für den Tunnelbau.
  Siehe Vorschlag 152 [Proposal 152](/proposals/152-ecies-tunnels).
- Neue Verschlüsselung für die Tunnel-Layer-Verschlüsselung.
  Siehe Vorschlag 153 [Proposal 153](/proposals/153-chacha20-layer-encryption).
- Methoden zur Verschlüsselung, Übertragung und zum Empfang von I2NP DLM / DSM / DSRM-Nachrichten.
  Keine Änderung.
- Keine LS1-zu-LS2- oder ElGamal/AES-zu-diesem-Vorschlag-Kommunikation wird unterstützt.
  Dieser Vorschlag ist ein bidirektionales Protokoll.
  Destinations können Rückwärtskompatibilität handhaben, indem sie zwei leasesets
  mit denselben Tunneln veröffentlichen oder beide Verschlüsselungstypen in das LS2 einbinden.
- Änderungen am Bedrohungsmodell
- Implementierungsdetails werden hier nicht diskutiert und bleiben jedem Projekt überlassen.
- (Optimistisch) Erweiterungen oder Hooks hinzufügen, um Multicast zu unterstützen

### Ziele

ElGamal/AES+SessionTag war etwa 15 Jahre lang unser einziges Ende-zu-Ende-Protokoll, im Wesentlichen ohne Änderungen am Protokoll. Es gibt mittlerweile kryptographische Primitive, die schneller sind. Wir müssen die Sicherheit des Protokolls verbessern. Wir haben auch heuristische Strategien und Workarounds entwickelt, um den Speicher- und Bandbreiten-Overhead des Protokolls zu minimieren, aber diese Strategien sind fragil, schwer abzustimmen und machen das Protokoll noch anfälliger für Ausfälle, wodurch die Sitzung unterbrochen wird.

Für etwa denselben Zeitraum haben die ElGamal/AES+SessionTag-Spezifikation und die dazugehörige Dokumentation beschrieben, wie bandbreitenaufwändig die Übermittlung von Session Tags ist, und haben vorgeschlagen, die Session Tag-Übermittlung durch einen "synchronisierten PRNG" zu ersetzen. Ein synchronisierter PRNG erzeugt deterministisch dieselben Tags an beiden Enden, abgeleitet von einem gemeinsamen Seed. Ein synchronisierter PRNG kann auch als "Ratchet" bezeichnet werden. Dieser Vorschlag spezifiziert (endlich) diesen Ratchet-Mechanismus und eliminiert die Tag-Übermittlung.

Durch die Verwendung einer Ratsche (ein synchronisierter PRNG) zur Generierung der Session-Tags eliminieren wir den Overhead beim Versenden von Session-Tags in der New Session-Nachricht und nachfolgenden Nachrichten bei Bedarf. Für ein typisches Tag-Set von 32 Tags sind das 1KB. Dies eliminiert auch die Speicherung von Session-Tags auf der Senderseite und reduziert somit die Speicheranforderungen um die Hälfte.

Ein vollständiger bidirektionaler Handshake, ähnlich dem Noise IK-Muster, ist erforderlich, um Key Compromise Impersonation (KCI) Angriffe zu vermeiden. Siehe die Noise "Payload Security Properties" Tabelle in [NOISE](https://noiseprotocol.org/noise.html). Für weitere Informationen zu KCI siehe das Paper https://www.usenix.org/system/files/conference/woot15/woot15-paper-hlauschek.pdf

### Nicht-Ziele / Außerhalb des Anwendungsbereichs

Das Bedrohungsmodell unterscheidet sich etwas von dem für NTCP2 (Vorschlag 111). Die MitM-Knoten sind der OBEP und IBGW und es wird angenommen, dass sie durch Kollaboration mit floodfills eine vollständige Sicht auf die aktuelle oder historische globale NetDB haben.

Das Ziel ist es, diese MitMs daran zu hindern, den Traffic als neue und bestehende Session-Nachrichten oder als neue Krypto vs. alte Krypto zu klassifizieren.

## Detailed Proposal

Dieser Vorschlag definiert ein neues Ende-zu-Ende-Protokoll, das ElGamal/AES+SessionTags ersetzen soll. Das Design wird einen Noise-Handshake und eine Datenphase verwenden, die Signals Double Ratchet integriert.

### Begründung

Es gibt fünf Bereiche des Protokolls, die neu gestaltet werden müssen:

- 1) Die neuen und bestehenden Session-Container-Formate
  werden durch neue Formate ersetzt.
- 2) ElGamal (256 Byte öffentliche Schlüssel, 128 Byte private Schlüssel) wird
  durch ECIES-X25519 (32 Byte öffentliche und private Schlüssel) ersetzt
- 3) AES wird durch
  AEAD_ChaCha20_Poly1305 (nachfolgend als ChaChaPoly abgekürzt) ersetzt
- 4) SessionTags werden durch ratchets ersetzt,
  welches im Wesentlichen ein kryptographischer, synchronisierter PRNG ist.
- 5) Die AES-Payload, wie in der ElGamal/AES+SessionTags-Spezifikation definiert,
  wird durch ein Blockformat ähnlich dem in NTCP2 ersetzt.

Jede der fünf Änderungen hat ihren eigenen Abschnitt unten.

### Bedrohungsmodell

Bestehende I2P-Router-Implementierungen werden Implementierungen für die folgenden standardmäßigen kryptographischen Primitive benötigen, die für aktuelle I2P-Protokolle nicht erforderlich sind:

- ECIES (aber das ist im Wesentlichen X25519)
- Elligator2

Bestehende I2P-Router-Implementierungen, die [NTCP2](/docs/specs/ntcp2/) ([Proposal 111](/proposals/111-ntcp-2/)) noch nicht implementiert haben, benötigen ebenfalls Implementierungen für:

- X25519 Schlüsselerzeugung und DH
- AEAD_ChaCha20_Poly1305 (unten als ChaChaPoly abgekürzt)
- HKDF

### Crypto Type

Der Krypto-Typ (verwendet im LS2) ist 4. Dies zeigt einen Little-Endian 32-Byte X25519 öffentlichen Schlüssel an und das hier spezifizierte Ende-zu-Ende-Protokoll.

Crypto-Typ 0 ist ElGamal. Crypto-Typen 1-3 sind reserviert für ECIES-ECDH-AES-SessionTag, siehe Proposal 145 [Proposal 145](/proposals/145-ecies).

### Zusammenfassung des kryptografischen Designs

Dieser Vorschlag stellt die Anforderungen basierend auf dem Noise Protocol Framework [NOISE](https://noiseprotocol.org/noise.html) (Revision 34, 2018-07-11) bereit. Noise hat ähnliche Eigenschaften wie das Station-To-Station-Protokoll [STS](https://en.wikipedia.org/wiki/Station-to-Station_protocol), welches die Grundlage für das [SSU](/docs/legacy/ssu/)-Protokoll bildet. In der Noise-Terminologie ist Alice die Initiatorin und Bob der Responder.

Dieser Vorschlag basiert auf dem Noise-Protokoll Noise_IK_25519_ChaChaPoly_SHA256. (Der tatsächliche Bezeichner für die anfängliche Schlüsselableitungsfunktion ist "Noise_IKelg2_25519_ChaChaPoly_SHA256", um I2P-Erweiterungen anzuzeigen - siehe Abschnitt KDF 1 unten) Dieses Noise-Protokoll verwendet die folgenden Primitive:

- Interactive Handshake Pattern: IK
  Alice übermittelt sofort ihren statischen Schlüssel an Bob (I)
  Alice kennt Bobs statischen Schlüssel bereits (K)

- One-Way Handshake Pattern: N
  Alice übermittelt ihren statischen Schlüssel nicht an Bob (N)

- DH Function: X25519
  X25519 DH mit einer Schlüssellänge von 32 Bytes wie spezifiziert in [RFC-7748](https://tools.ietf.org/html/rfc7748).

- Cipher Function: ChaChaPoly
  AEAD_CHACHA20_POLY1305 wie in [RFC-7539](https://tools.ietf.org/html/rfc7539) Abschnitt 2.8 spezifiziert.
  12 Byte Nonce, wobei die ersten 4 Bytes auf Null gesetzt sind.
  Identisch zu der in [NTCP2](/docs/specs/ntcp2/).

- Hash Function: SHA256
  Standard 32-Byte-Hash, bereits umfassend in I2P verwendet.

### Neue kryptographische Primitive für I2P

Dieser Vorschlag definiert die folgenden Erweiterungen für Noise_IK_25519_ChaChaPoly_SHA256. Diese folgen im Allgemeinen den Richtlinien in [NOISE](https://noiseprotocol.org/noise.html) Abschnitt 13.

1) Klartext-Ephemeralschlüssel werden mit [Elligator2](https://elligator.cr.yp.to/) kodiert.

2) Die Antwort wird mit einem Klartext-Tag vorangestellt.

3) Das Payload-Format ist für Nachrichten 1, 2 und die Datenphase definiert. Natürlich ist dies nicht in Noise definiert.

Alle Nachrichten enthalten einen [I2NP](/docs/specs/i2np/) Garlic Message Header. Die Datenphase verwendet eine Verschlüsselung, die ähnlich, aber nicht kompatibel mit der Noise-Datenphase ist.

### Krypto-Typ

Handshakes verwenden [Noise](https://noiseprotocol.org/noise.html) Handshake-Muster.

Die folgende Buchstabenzuordnung wird verwendet:

- e = einmaliger ephemerer Schlüssel
- s = statischer Schlüssel
- p = Nachrichten-Payload

One-time und Unbound Sessions sind ähnlich dem Noise N Pattern.

```

<- s
  ...
  e es p ->

```
Bound Sessions ähneln dem Noise IK Pattern.

```

<- s
  ...
  e es s ss p ->
  <- tag e ee se
  <- p
  p ->

```
### Noise Protocol Framework

Das aktuelle ElGamal/AES+SessionTag-Protokoll ist unidirektional. Auf dieser Ebene weiß der Empfänger nicht, woher eine Nachricht stammt. Ausgehende und eingehende Sitzungen sind nicht miteinander verknüpft. Bestätigungen erfolgen out-of-band mittels einer DeliveryStatusMessage (eingehüllt in eine GarlicMessage) im Clove.

Es gibt erhebliche Ineffizienz in einem unidirektionalen Protokoll. Jede Antwort muss ebenfalls eine teure 'New Session'-Nachricht verwenden. Dies führt zu höherem Bandbreiten-, CPU- und Speicherverbrauch.

Es gibt auch Sicherheitsschwächen in einem unidirektionalen Protokoll. Alle Sitzungen basieren auf ephemeral-static DH. Ohne einen Rückpfad gibt es keine Möglichkeit für Bob, seinen statischen Schlüssel zu einem ephemeren Schlüssel zu "ratcheten". Ohne zu wissen, woher eine Nachricht kommt, gibt es keine Möglichkeit, den empfangenen ephemeren Schlüssel für ausgehende Nachrichten zu verwenden, daher verwendet auch die erste Antwort ephemeral-static DH.

Für diesen Vorschlag definieren wir zwei Mechanismen zur Erstellung eines bidirektionalen Protokolls - "Pairing" und "Binding". Diese Mechanismen bieten erhöhte Effizienz und Sicherheit.

### Ergänzungen zum Framework

Wie bei ElGamal/AES+SessionTags müssen alle eingehenden und ausgehenden Sitzungen in einem bestimmten Kontext stehen, entweder im Kontext des routers oder im Kontext für ein bestimmtes lokales Ziel. In Java I2P wird dieser Kontext Session Key Manager genannt.

Sessions dürfen nicht zwischen Kontexten geteilt werden, da dies eine Korrelation zwischen den verschiedenen lokalen Zielen oder zwischen einem lokalen Ziel und einem Router ermöglichen würde.

Wenn ein bestimmtes Ziel sowohl ElGamal/AES+SessionTags als auch diesen Vorschlag unterstützt, können beide Sitzungstypen einen Kontext teilen. Siehe Abschnitt 1c) unten.

### Handshake-Muster

Wenn eine ausgehende Sitzung beim Ursprung (Alice) erstellt wird, wird eine neue eingehende Sitzung erstellt und mit der ausgehenden Sitzung gepaart, es sei denn, es wird keine Antwort erwartet (z.B. rohe Datagramme).

Eine neue eingehende Sitzung wird immer mit einer neuen ausgehenden Sitzung gekoppelt, es sei denn, es wird keine Antwort angefordert (z. B. rohe Datagramme).

Wenn eine Antwort angefordert wird und an ein entferntes Ziel oder einen Router gebunden ist, wird diese neue ausgehende Session an dieses Ziel oder diesen Router gebunden und ersetzt jede vorherige ausgehende Session zu diesem Ziel oder Router.

Die Paarung von eingehenden und ausgehenden Sitzungen bietet ein bidirektionales Protokoll mit der Fähigkeit, die DH-Schlüssel zu ratcheten.

### Sitzungen

Es gibt nur eine ausgehende Sitzung zu einem bestimmten Ziel oder router. Es kann mehrere aktuelle eingehende Sitzungen von einem bestimmten Ziel oder router geben. Im Allgemeinen wird, wenn eine neue eingehende Sitzung erstellt wird und Datenverkehr auf dieser Sitzung empfangen wird (was als ACK dient), jede andere relativ schnell zum Ablaufen markiert, innerhalb von etwa einer Minute. Der Wert der zuvor gesendeten Nachrichten (PN) wird überprüft, und falls es keine unempfangenen Nachrichten (innerhalb der Fenstergröße) in der vorherigen eingehenden Sitzung gibt, kann die vorherige Sitzung sofort gelöscht werden.

Wenn eine ausgehende Sitzung beim Ursprung (Alice) erstellt wird, wird sie an die entfernte Destination (Bob) gebunden, und jede gepaarte eingehende Sitzung wird ebenfalls an die entfernte Destination gebunden. Während die Sitzungen fortschreiten, bleiben sie weiterhin an die entfernte Destination gebunden.

Wenn eine eingehende Session beim Empfänger (Bob) erstellt wird, kann sie optional an die entfernte Destination (Alice) gebunden werden. Wenn Alice Binding-Informationen (ihren statischen Schlüssel) in die New Session-Nachricht einschließt, wird die Session an diese Destination gebunden, und eine ausgehende Session wird erstellt und an dieselbe Destination gebunden. Während die Sessions ratcheten, bleiben sie weiterhin an die entfernte Destination gebunden.

### Sitzungskontext

Für den häufigen, Streaming-Fall erwarten wir, dass Alice und Bob das Protokoll wie folgt verwenden:

- Alice paart ihre neue ausgehende Session mit einer neuen eingehenden Session, beide gebunden an das entfernte Ziel (Bob).
- Alice fügt die Bindungsinformationen und Signatur sowie eine Antwortanfrage in die
  New Session-Nachricht ein, die an Bob gesendet wird.
- Bob paart seine neue eingehende Session mit einer neuen ausgehenden Session, beide gebunden an das entfernte Ziel (Alice).
- Bob sendet eine Antwort (ack) an Alice in der gepaarten Session, mit einem Ratchet zu einem neuen DH-Schlüssel.
- Alice führt einen Ratchet zu einer neuen ausgehenden Session mit Bobs neuem Schlüssel durch, gepaart mit der bestehenden eingehenden Session.

Durch die Bindung einer eingehenden Session an eine entfernte Destination und die Kopplung der eingehenden Session mit einer ausgehenden Session, die an dieselbe Destination gebunden ist, erreichen wir zwei wesentliche Vorteile:

1) Die erste Antwort von Bob an Alice verwendet ephemeral-ephemeral DH

2) Nachdem Alice Bobs Antwort erhalten und geratchet hat, verwenden alle nachfolgenden Nachrichten von Alice an Bob ephemeral-ephemeral DH.

### Kopplung von Eingehenden und Ausgehenden Sessions

In ElGamal/AES+SessionTags fordert der sendende Router eine ACK an, wenn ein LeaseSet als garlic clove gebündelt wird oder Tags übermittelt werden. Dies ist ein separater garlic clove, der eine DeliveryStatus-Nachricht enthält. Für zusätzliche Sicherheit wird die DeliveryStatus-Nachricht in eine Garlic-Nachricht eingeschlossen. Dieser Mechanismus ist aus Sicht des Protokolls out-of-band.

Im neuen Protokoll können wir, da die eingehenden und ausgehenden Sessions gepaart sind, ACKs in-band haben. Es ist keine separate Clove erforderlich.

Ein explizites ACK ist einfach eine Existing Session-Nachricht ohne I2NP-Block. In den meisten Fällen kann jedoch ein explizites ACK vermieden werden, da es Rückverkehr gibt. Es kann für Implementierungen wünschenswert sein, eine kurze Zeit (vielleicht hundert ms) zu warten, bevor ein explizites ACK gesendet wird, um der Streaming- oder Anwendungsschicht Zeit zu geben, zu antworten.

Implementierungen müssen auch das Senden von ACKs aufschieben, bis der I2NP-Block verarbeitet wurde, da die Garlic Message eine Database Store Message mit einem leaseSet enthalten kann. Ein aktuelles leaseSet ist erforderlich, um das ACK zu routen, und das entfernte Ziel (im leaseSet enthalten) ist notwendig, um den bindenden statischen Schlüssel zu verifizieren.

### Binding von Sessions und Destinations

Ausgehende Sessions sollten immer vor eingehenden Sessions ablaufen. Sobald eine ausgehende Session abläuft und eine neue erstellt wird, wird ebenfalls eine neue gepaarte eingehende Session erstellt. Falls eine alte eingehende Session vorhanden war, wird sie ablaufen gelassen.

### Vorteile von Binding und Pairing

TBD

### Message ACKs

Wir definieren die folgenden Funktionen, die den verwendeten kryptografischen Bausteinen entsprechen.

ZEROLEN

    zero-length byte array

CSRNG(n)

    n-byte output from a cryptographically-secure random number generator.

H(p, d)

    SHA-256 hash function that takes a personalization string p and data d, and
    produces an output of length 32 bytes.
    As defined in [NOISE](https://noiseprotocol.org/noise.html).
    || below means append.

    Use SHA-256 as follows::

        H(p, d) := SHA-256(p || d)

MixHash(d)

    SHA-256 hash function that takes a previous hash h and new data d,
    and produces an output of length 32 bytes.
    || below means append.

    Use SHA-256 as follows::

        MixHash(d) := h = SHA-256(h || d)

STREAM

    The ChaCha20/Poly1305 AEAD as specified in [RFC-7539](https://tools.ietf.org/html/rfc7539).
    S_KEY_LEN = 32 and S_IV_LEN = 12.

    ENCRYPT(k, n, plaintext, ad)
        Encrypts plaintext using the cipher key k, and nonce n which MUST be unique for
        the key k.
        Associated data ad is optional.
        Returns a ciphertext that is the size of the plaintext + 16 bytes for the HMAC.

        The entire ciphertext must be indistinguishable from random if the key is secret.

    DECRYPT(k, n, ciphertext, ad)
        Decrypts ciphertext using the cipher key k, and nonce n.
        Associated data ad is optional.
        Returns the plaintext.

DH

    X25519 public key agreement system. Private keys of 32 bytes, public keys of 32
    bytes, produces outputs of 32 bytes. It has the following
    functions:

    GENERATE_PRIVATE()
        Generates a new private key.

    DERIVE_PUBLIC(privkey)
        Returns the public key corresponding to the given private key.

    GENERATE_PRIVATE_ELG2()
        Generates a new private key that maps to a public key suitable for Elligator2 encoding.
        Note that half of the randomly-generated private keys will not be suitable and must be discarded.

    ENCODE_ELG2(pubkey)
        Returns the Elligator2-encoded public key corresponding to the given public key (inverse mapping).
        Encoded keys are little endian.
        Encoded key must be 256 bits indistinguishable from random data.
        See Elligator2 section below for specification.

    DECODE_ELG2(pubkey)
        Returns the public key corresponding to the given Elligator2-encoded public key.
        See Elligator2 section below for specification.

    DH(privkey, pubkey)
        Generates a shared secret from the given private and public keys.

HKDF(salt, ikm, info, n)

    A cryptographic key derivation function which takes some input key material ikm (which
    should have good entropy but is not required to be a uniformly random string), a salt
    of length 32 bytes, and a context-specific 'info' value, and produces an output
    of n bytes suitable for use as key material.

    Use HKDF as specified in [RFC-5869](https://tools.ietf.org/html/rfc5869), using the HMAC hash function SHA-256
    as specified in [RFC-2104](https://tools.ietf.org/html/rfc2104). This means that SALT_LEN is 32 bytes max.

MixKey(d)

    Use HKDF() with a previous chainKey and new data d, and
    sets the new chainKey and k.
    As defined in [NOISE](https://noiseprotocol.org/noise.html).

    Use HKDF as follows::

        MixKey(d) := output = HKDF(chainKey, d, "", 64)
                     chainKey = output[0:31]
                     k = output[32:63]


### Sitzungs-Timeouts

### Multicast

Die Garlic Message, wie in [I2NP](/docs/specs/i2np/) spezifiziert, ist wie folgt. Da ein Designziel ist, dass Zwischenhops nicht zwischen neuer und alter Kryptografie unterscheiden können, kann dieses Format nicht geändert werden, obwohl das Längenfeld redundant ist. Das Format wird mit dem vollständigen 16-Byte-Header gezeigt, obwohl der tatsächliche Header je nach verwendetem Transport in einem anderen Format vorliegen kann.

Wenn entschlüsselt, enthält die Datenstruktur eine Reihe von Garlic Cloves und zusätzliche Daten, auch bekannt als Clove Set.

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
### Definitionen

Das aktuelle Nachrichtenformat, das seit über 15 Jahren verwendet wird, ist ElGamal/AES+SessionTags. In ElGamal/AES+SessionTags gibt es zwei Nachrichtenformate:

1) Neue Session: - 514 Byte ElGamal-Block - AES-Block (128 Bytes Minimum, Vielfaches von 16)

2) Bestehende Session: - 32 Byte Session Tag - AES-Block (128 Bytes Minimum, Vielfaches von 16)

Das minimale Padding auf 128 ist wie in Java I2P implementiert, wird aber beim Empfang nicht durchgesetzt.

Diese Nachrichten sind in einer I2NP garlic message gekapselt, die ein Längenfeld enthält, sodass die Länge bekannt ist.

Beachte, dass kein Padding zu einer Länge definiert ist, die nicht mod-16 entspricht, daher ist die New Session immer (mod 16 == 2) und eine Existing Session ist immer (mod 16 == 0). Wir müssen das beheben.

Der Empfänger versucht zunächst, die ersten 32 Bytes als Session Tag nachzuschlagen. Wenn gefunden, entschlüsselt er den AES-Block. Wenn nicht gefunden und die Daten mindestens (514+16) lang sind, versucht er den ElGamal-Block zu entschlüsseln, und bei Erfolg entschlüsselt er den AES-Block.

### 1) Nachrichtenformat

Im Signal Double Ratchet enthält der Header:

- DH: Aktueller Ratchet-Public-Key
- PN: Vorherige Chain-Nachrichtenlänge
- N: Nachrichtennummer

Signals „Sending Chains" entsprechen in etwa unseren Tag-Sets. Durch die Verwendung eines Session-Tags können wir den Großteil davon eliminieren.

In New Session setzen wir nur den öffentlichen Schlüssel in den unverschlüsselten Header.

In Existing Session verwenden wir ein Session-Tag für den Header. Das Session-Tag ist mit dem aktuellen Ratchet-Public-Key und der Nachrichtennummer verknüpft.

In sowohl neuen als auch bestehenden Sessions befinden sich PN und N im verschlüsselten Körper.

In Signal wird ständig geratchet. Ein neuer DH-Public-Key erfordert, dass der Empfänger ratchet und einen neuen Public Key zurücksendet, was gleichzeitig als Bestätigung für den empfangenen Public Key dient. Das wären viel zu viele DH-Operationen für uns. Daher trennen wir die Bestätigung des empfangenen Keys von der Übertragung eines neuen Public Keys. Jede Nachricht, die ein Session-Tag verwendet, das aus dem neuen DH-Public-Key generiert wurde, stellt eine Bestätigung dar. Wir übertragen nur dann einen neuen Public Key, wenn wir den Key erneuern möchten.

Die maximale Anzahl von Nachrichten, bevor der DH ratcheten muss, beträgt 65535.

Beim Übermitteln eines Session-Schlüssels leiten wir das "Tag Set" davon ab, anstatt auch Session-Tags übermitteln zu müssen. Ein Tag Set kann bis zu 65536 Tags enthalten. Empfänger sollten jedoch eine "Look-ahead"-Strategie implementieren, anstatt alle möglichen Tags auf einmal zu generieren. Generieren Sie höchstens N Tags nach dem letzten erfolgreich empfangenen Tag. N könnte höchstens 128 betragen, aber 32 oder sogar weniger könnte eine bessere Wahl sein.

### Überprüfung des aktuellen Nachrichtenformats

New Session One Time Public Key (32 Bytes) Verschlüsselte Daten und MAC (verbleibende Bytes)

Die New Session-Nachricht kann den statischen öffentlichen Schlüssel des Absenders enthalten oder auch nicht. Wenn er enthalten ist, wird die Rücksitzung an diesen Schlüssel gebunden. Der statische Schlüssel sollte enthalten sein, wenn Antworten erwartet werden, d.h. für Streaming und beantwortbare Datagramme. Er sollte nicht für Raw-Datagramme enthalten sein.

Die New Session Nachricht ähnelt dem einseitigen Noise [NOISE](https://noiseprotocol.org/noise.html) Muster "N" (falls der statische Schlüssel nicht gesendet wird), oder dem zweiseitigen Muster "IK" (falls der statische Schlüssel gesendet wird).

### Überprüfung des verschlüsselten Datenformats

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
### Neue Session Tags und Vergleich mit Signal

Der ephemere Schlüssel ist 32 Bytes groß und wird mit Elligator2 kodiert. Dieser Schlüssel wird niemals wiederverwendet; für jede Nachricht wird ein neuer Schlüssel generiert, einschließlich Wiederübertragungen.

### 1a) Neues Session-Format

Wenn entschlüsselt, Alices statischer X25519-Schlüssel, 32 Bytes.

### 1b) Neues Session-Format (mit Binding)

Die verschlüsselte Länge ist der Rest der Daten. Die entschlüsselte Länge ist 16 weniger als die verschlüsselte Länge. Die Payload muss einen DateTime-Block enthalten und wird normalerweise einen oder mehrere Garlic Clove-Blöcke enthalten. Siehe den Payload-Abschnitt unten für Format und zusätzliche Anforderungen.

### Neuer Session Ephemeral Key

Wenn keine Antwort erforderlich ist, wird kein statischer Schlüssel gesendet.

Länge ist 96 + Payload-Länge. Verschlüsseltes Format:

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
### Statischer Schlüssel

Alices ephemeral key. Der ephemeral key ist 32 Bytes lang, kodiert mit Elligator2, little endian. Dieser Schlüssel wird niemals wiederverwendet; ein neuer Schlüssel wird für jede Nachricht generiert, einschließlich Neuübertragungen.

### Nutzlast

Der Flags-Abschnitt enthält nichts. Er ist immer 32 Bytes lang, da er die gleiche Länge wie der statische Schlüssel für New Session-Nachrichten mit Binding haben muss. Bob bestimmt, ob es sich um einen statischen Schlüssel oder einen Flags-Abschnitt handelt, indem er prüft, ob alle 32 Bytes Nullen sind.

TODO sind hier irgendwelche Flags erforderlich?

### 1c) Neues Session-Format (ohne Bindung)

Die verschlüsselte Länge ist der Rest der Daten. Die entschlüsselte Länge ist 16 weniger als die verschlüsselte Länge. Die Nutzdaten müssen einen DateTime-Block enthalten und werden normalerweise einen oder mehrere Garlic Clove-Blöcke enthalten. Siehe den Nutzdatenbereich unten für Format und zusätzliche Anforderungen.

### Neuer Session Ephemeral Key

Wenn nur eine einzige Nachricht gesendet werden soll, ist keine Session-Einrichtung oder statischer Schlüssel erforderlich.

Die Länge beträgt 96 + Payload-Länge. Verschlüsseltes Format:

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
### Flags-Abschnitt Entschlüsselte Daten

Der Einmalschlüssel ist 32 Bytes lang, mit Elligator2 kodiert, Little Endian. Dieser Schlüssel wird niemals wiederverwendet; ein neuer Schlüssel wird mit jeder Nachricht generiert, einschließlich Neuübertragungen.

### Nutzlast

Der Flags-Abschnitt enthält nichts. Er ist immer 32 Bytes lang, da er die gleiche Länge wie der statische Schlüssel für New Session-Nachrichten mit Binding haben muss. Bob bestimmt, ob es sich um einen statischen Schlüssel oder einen Flags-Abschnitt handelt, indem er prüft, ob die 32 Bytes alle Nullen sind.

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
### 1d) Einmaliges Format (keine Bindung oder Sitzung)

Die verschlüsselte Länge ist der Rest der Daten. Die entschlüsselte Länge ist 16 weniger als die verschlüsselte Länge. Die Nutzlast muss einen DateTime-Block enthalten und wird normalerweise einen oder mehrere Garlic Clove-Blöcke enthalten. Siehe den Nutzlast-Abschnitt unten für das Format und zusätzliche Anforderungen.

### Neuer Sitzungs-Einmalschlüssel

### Flags Sektion Entschlüsselte Daten

Das ist standardmäßiges [NOISE](https://noiseprotocol.org/noise.html) für IK mit einem modifizierten Protokollnamen. Beachten Sie, dass wir denselben Initializer sowohl für das IK-Muster (gebundene Sitzungen) als auch für das N-Muster (ungebundene Sitzungen) verwenden.

Der Protokollname wird aus zwei Gründen modifiziert. Erstens, um anzuzeigen, dass die ephemeren Schlüssel mit Elligator2 kodiert sind, und zweitens, um anzuzeigen, dass MixHash() vor der zweiten Nachricht aufgerufen wird, um den Tag-Wert einzumischen.

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
### Nutzlast

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
### 1f) KDFs für New Session Message

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
### KDF für initialen ChainKey

Beachten Sie, dass dies ein Noise "N" Pattern ist, aber wir verwenden den gleichen "IK" Initializer wie für gebundene Sitzungen.

New Session-Nachrichten können nicht als Alice's statischen Schlüssel enthaltend oder nicht enthaltend identifiziert werden, bis der statische Schlüssel entschlüsselt und überprüft wird, um festzustellen, ob er nur Nullen enthält. Daher muss der Empfänger die "IK"-Zustandsmaschine für alle New Session-Nachrichten verwenden. Wenn der statische Schlüssel nur Nullen enthält, muss das "ss"-Nachrichtenmuster übersprungen werden.

```

chainKey = from Flags/Static key section
  k = from Flags/Static key section
  n = 1
  ad = h from Flags/Static key section
  ciphertext = ENCRYPT(k, n, payload, ad)

```
### KDF für Flags/Static Key Section verschlüsselte Inhalte

Eine oder mehrere New Session Replies können als Antwort auf eine einzelne New Session-Nachricht gesendet werden. Jeder Reply wird mit einem Tag vorangestellt, der aus einem TagSet für die Session generiert wird.

Die New Session Reply besteht aus zwei Teilen. Der erste Teil ist die Vervollständigung des Noise IK Handshakes mit einem vorangestellten Tag. Die Länge des ersten Teils beträgt 56 Bytes. Der zweite Teil ist die Nutzlast der Datenphase. Die Länge des zweiten Teils beträgt 16 + Nutzlastlänge.

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
### KDF für Payload-Sektion (mit Alice statischem Schlüssel)

Der Tag wird in der Session Tags KDF generiert, wie sie in der DH Initialization KDF unten initialisiert wird. Dies korreliert die Antwort mit der Session. Der Session Key aus der DH Initialization wird nicht verwendet.

### KDF für Payload-Sektion (ohne Alice statischen Schlüssel)

Bobs kurzlebiger Schlüssel. Der kurzlebige Schlüssel ist 32 Bytes lang, kodiert mit Elligator2, Little-Endian. Dieser Schlüssel wird niemals wiederverwendet; ein neuer Schlüssel wird mit jeder Nachricht generiert, einschließlich Neuübertragungen.

### 1g) Neues Session Reply Format

Die verschlüsselte Länge ist der verbleibende Teil der Daten. Die entschlüsselte Länge ist 16 weniger als die verschlüsselte Länge. Die Nutzdaten enthalten normalerweise einen oder mehrere Garlic Clove-Blöcke. Siehe den Nutzdaten-Abschnitt unten für Format und zusätzliche Anforderungen.

### Session Tag

Ein oder mehrere Tags werden aus dem TagSet erstellt, das mit der unten beschriebenen KDF initialisiert wird, unter Verwendung des chainKey aus der New Session-Nachricht.

```

// Generate tagset
  tagsetKey = HKDF(chainKey, ZEROLEN, "SessionReplyTags", 32)
  tagset_nsr = DH_INITIALIZE(chainKey, tagsetKey)

```
### New Session Reply Ephemeral Key

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
### Nutzlast

Dies ist wie die erste Existing Session-Nachricht nach der Aufspaltung, aber ohne separaten Tag. Zusätzlich verwenden wir den Hash von oben, um die Nutzdaten an die NSR-Nachricht zu binden.

```

// split()
  keydata = HKDF(chainKey, ZEROLEN, "", 64)
  k_ab = keydata[0:31]
  k_ba = keydata[32:63]
  tagset_ab = DH_INITIALIZE(chainKey, k_ab)
  tagset_ba = DH_INITIALIZE(chainKey, k_ba)

  // AEAD parameters for New Session Reply payload
  k = HKDF(k_ba, ZEROLEN, "AttachPayloadKDF", 32)
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, payload, ad)
```
### KDF für Reply TagSet

Mehrere NSR-Nachrichten können als Antwort gesendet werden, jede mit einzigartigen ephemeral keys, abhängig von der Größe der Antwort.

Alice und Bob müssen neue ephemere Schlüssel für jede NS- und NSR-Nachricht verwenden.

Alice muss eine von Bobs NSR-Nachrichten erhalten, bevor sie Existing Session (ES)-Nachrichten sendet, und Bob muss eine ES-Nachricht von Alice erhalten, bevor er ES-Nachrichten sendet.

Der ``chainKey`` und ``k`` aus Bobs NSR Payload Section werden als Eingaben für die initialen ES DH Ratchets (beide Richtungen, siehe DH Ratchet KDF) verwendet.

Bob muss nur bestehende Sessions für die von Alice empfangenen ES-Nachrichten beibehalten. Alle anderen erstellten eingehenden und ausgehenden Sessions (für mehrere NSRs) sollten sofort nach dem Empfang von Alices erster ES-Nachricht für eine bestimmte Session zerstört werden.

### KDF für Reply Key Section verschlüsselte Inhalte

Session-Tag (8 Bytes) Verschlüsselte Daten und MAC (siehe Abschnitt 3 unten)

### KDF für verschlüsselte Inhalte des Payload-Abschnitts

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
### Hinweise

Die verschlüsselte Länge ist der verbleibende Teil der Daten. Die entschlüsselte Länge ist 16 weniger als die verschlüsselte Länge. Siehe den Payload-Abschnitt unten für Format und Anforderungen.

KDF

```
See AEAD section below.

  // AEAD parameters for Existing Session payload
  k = The 32-byte session key associated with this session tag
  n = The message number N in the current chain, as retrieved from the associated Session Tag.
  ad = The session tag, 8 bytes
  ciphertext = ENCRYPT(k, n, payload, ad)
```
### 1h) Bestehendes Session-Format

Format: 32-Byte öffentliche und private Schlüssel, Little-Endian.

Begründung: Verwendet in [NTCP2](/docs/specs/ntcp2/).

### Format

Bei Standard-Noise-Handshakes beginnen die anfänglichen Handshake-Nachrichten in jede Richtung mit ephemeren Schlüsseln, die im Klartext übertragen werden. Da gültige X25519-Schlüssel von zufälligen Daten unterscheidbar sind, kann ein Man-in-the-Middle diese Nachrichten von Existing Session-Nachrichten unterscheiden, die mit zufälligen Session-Tags beginnen. In [NTCP2](/docs/specs/ntcp2/) ([Proposal 111](/proposals/111-ntcp-2/)) verwendeten wir eine ressourcenschonende XOR-Funktion mit dem Out-of-Band-Static-Key, um den Schlüssel zu verschleiern. Das Bedrohungsmodell hier ist jedoch anders; wir wollen nicht zulassen, dass ein MitM irgendwelche Mittel verwenden kann, um das Ziel des Traffics zu bestätigen oder um die anfänglichen Handshake-Nachrichten von Existing Session-Nachrichten zu unterscheiden.

Daher wird [Elligator2](https://elligator.cr.yp.to/) verwendet, um die ephemeren Schlüssel in den New Session und New Session Reply Nachrichten so zu transformieren, dass sie von gleichmäßig zufälligen Zeichenketten nicht zu unterscheiden sind.

### Nutzlast

32-Byte öffentliche und private Schlüssel. Kodierte Schlüssel sind Little-Endian.

Wie in [Elligator2](https://elligator.cr.yp.to/) definiert, sind die kodierten Schlüssel von 254 zufälligen Bits nicht zu unterscheiden. Wir benötigen 256 zufällige Bits (32 Bytes). Daher sind die Kodierung und Dekodierung wie folgt definiert:

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
### 2) ECIES-X25519

Erforderlich, um zu verhindern, dass der OBEP und IBGW den Datenverkehr klassifizieren.

### 2a) Elligator2

Elligator2 verdoppelt im Durchschnitt die Schlüsselerzeugungszeit, da die Hälfte der privaten Schlüssel zu öffentlichen Schlüsseln führt, die für die Codierung mit Elligator2 ungeeignet sind. Außerdem ist die Schlüsselerzeugungszeit unbegrenzt mit einer exponentiellen Verteilung, da der Generator solange wiederholen muss, bis ein geeignetes Schlüsselpaar gefunden wird.

Dieser Overhead kann verwaltet werden, indem die Schlüsselerzeugung im Voraus in einem separaten Thread durchgeführt wird, um einen Pool geeigneter Schlüssel bereitzuhalten.

Der Generator führt die ENCODE_ELG2()-Funktion aus, um die Eignung zu bestimmen. Daher sollte der Generator das Ergebnis von ENCODE_ELG2() speichern, damit es nicht erneut berechnet werden muss.

Zusätzlich können die ungeeigneten Schlüssel zum Pool der Schlüssel hinzugefügt werden, die für [NTCP2](/docs/specs/ntcp2/) verwendet werden, wo Elligator2 nicht verwendet wird. Die Sicherheitsprobleme dabei sind noch zu bestimmen.

### Format

AEAD mit ChaCha20 und Poly1305, wie auch in [NTCP2](/docs/specs/ntcp2/). Dies entspricht [RFC-7539](https://tools.ietf.org/html/rfc7539), welches auch ähnlich in TLS [RFC-7905](https://tools.ietf.org/html/rfc7905) verwendet wird.

### Begründung

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
### Hinweise

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
### 3) AEAD (ChaChaPoly)

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
### Neue Session und Neue Session Reply Eingaben

- Da ChaCha20 eine Stromchiffre ist, müssen Klartexte nicht aufgefüllt werden.
  Zusätzliche Keystream-Bytes werden verworfen.

- Der Schlüssel für die Verschlüsselung (256 Bits) wird mittels der SHA256 KDF vereinbart.
  Die Details der KDF für jede Nachricht befinden sich in separaten Abschnitten unten.

- ChaChaPoly-Frames haben eine bekannte Größe, da sie in der I2NP-Datennachricht eingekapselt sind.

- Für alle Nachrichten
  befindet sich die Polsterung innerhalb des
  authentifizierten Datenrahmens.

### Vorhandene Session-Eingaben

Alle empfangenen Daten, die die AEAD-Verifikation nicht bestehen, müssen verworfen werden. Es wird keine Antwort zurückgegeben.

### Verschlüsseltes Format

Verwendet in [NTCP2](/docs/specs/ntcp2/).

### Notizen

Wir verwenden immer noch Session Tags wie zuvor, aber wir nutzen Ratchets, um sie zu generieren. Session Tags hatten auch eine Rekey-Option, die wir nie implementiert haben. Es ist also wie ein Double Ratchet, aber wir haben den zweiten nie gemacht.

Hier definieren wir etwas Ähnliches wie Signals Double Ratchet. Die Session-Tags werden deterministisch und identisch auf der Empfänger- und Senderseite generiert.

Durch die Verwendung eines symmetrischen Schlüssel/Tag-Ratchets eliminieren wir den Speicherverbrauch für die Speicherung von Session Tags auf der Senderseite. Wir eliminieren auch den Bandbreitenverbrauch für das Senden von Tag-Sets. Der Verbrauch auf der Empfängerseite ist immer noch erheblich, aber wir können ihn weiter reduzieren, da wir den Session Tag von 32 Bytes auf 8 Bytes verkleinern werden.

Wir verwenden keine Header-Verschlüsselung wie in Signal spezifiziert (und optional), sondern nutzen stattdessen Session-Tags.

Durch die Verwendung eines DH-Ratchets erreichen wir Forward Secrecy, was in ElGamal/AES+SessionTags nie implementiert wurde.

Hinweis: Der New Session einmalige öffentliche Schlüssel ist nicht Teil des Ratchet, seine einzige Funktion besteht darin, Alices initialen DH-Ratchet-Schlüssel zu verschlüsseln.

### AEAD-Fehlerbehandlung

Der Double Ratchet behandelt verlorene oder nicht in der richtigen Reihenfolge eingehende Nachrichten, indem in jedem Nachrichten-Header ein Tag enthalten ist. Der Empfänger schlägt den Index des Tags nach, dies ist die Nachrichtennummer N. Wenn die Nachricht einen Message Number Block mit einem PN-Wert enthält, kann der Empfänger alle Tags löschen, die höher als dieser Wert im vorherigen Tag-Set sind, während übersprungene Tags aus dem vorherigen Tag-Set beibehalten werden, falls die übersprungenen Nachrichten später eintreffen.

### Begründung

Wir definieren die folgenden Datenstrukturen und Funktionen zur Implementierung dieser Ratchets.

TAGSET_ENTRY

    A single entry in a TAGSET.

    INDEX
        An integer index, starting with 0

    SESSION_TAG
        An identifier to go out on the wire, 8 bytes

    SESSION_KEY
        A symmetric key, never goes on the wire, 32 bytes

TAGSET

    A collection of TAGSET_ENTRIES.

    CREATE(key, n)
        Generate a new TAGSET using initial cryptographic key material of 32 bytes.
        The associated session identifier is provided.
        The initial number of of tags to create is specified; this is generally 0 or 1
        for an outgoing session.
        LAST_INDEX = -1
        EXTEND(n) is called.

    EXTEND(n)
        Generate n more TAGSET_ENTRIES by calling EXTEND() n times.

    EXTEND()
        Generate one more TAGSET_ENTRY, unless the maximum number SESSION_TAGS have
        already been generated.
        If LAST_INDEX is greater than or equal to 65535, return.
        ++ LAST_INDEX
        Create a new TAGSET_ENTRY with the LAST_INDEX value and the calculated SESSION_TAG.
        Calls RATCHET_TAG() and (optionally) RATCHET_KEY().
        For inbound sessions, the calculation of the SESSION_KEY may
        be deferred and calculated in GET_SESSION_KEY().
        Calls EXPIRE()

    EXPIRE()
        Remove tags and keys that are too old, or if the TAGSET size exceeds some limit.

    RATCHET_TAG()
        Calculates the next SESSION_TAG based on the last SESSION_TAG.

    RATCHET_KEY()
        Calculates the next SESSION_KEY based on the last SESSION_KEY.

    SESSION
        The associated session.

    CREATION_TIME
        When the TAGSET was created.

    LAST_INDEX
        The last TAGSET_ENTRY INDEX generated by EXTEND().

    GET_NEXT_ENTRY()
        Used for outgoing sessions only.
        EXTEND(1) is called if there are no remaining TAGSET_ENTRIES.
        If EXTEND(1) did nothing, the max of 65535 TAGSETS have been used,
        and return an error.
        Returns the next unused TAGSET_ENTRY.

    GET_SESSION_KEY(sessionTag)
        Used for incoming sessions only.
        Returns the TAGSET_ENTRY containing the sessionTag.
        If found, the TAGSET_ENTRY is removed.
        If the SESSION_KEY calculation was deferred, it is calculated now.
        If there are few TAGSET_ENTRIES remaining, EXTEND(n) is called.


### 4) Ratchets

Ratchets, aber bei weitem nicht so schnell wie Signal es macht. Wir trennen die Bestätigung des empfangenen Schlüssels von der Generierung des neuen Schlüssels. Bei typischer Nutzung werden Alice und Bob jeweils (zweimal) sofort in einer New Session ratcheten, aber danach nicht mehr ratcheten.

Beachten Sie, dass ein Ratchet für eine einzelne Richtung gilt und eine New Session Tag / Message Key Ratchet-Kette für diese Richtung generiert. Um Schlüssel für beide Richtungen zu generieren, müssen Sie zweimal ratcheten.

Sie ratchet jedes Mal, wenn Sie einen neuen Schlüssel generieren und senden. Sie ratchet jedes Mal, wenn Sie einen neuen Schlüssel empfangen.

Alice führt einmal ein Ratcheting durch, wenn sie eine ungebundene ausgehende Sitzung erstellt, sie erstellt keine eingehende Sitzung (ungebunden bedeutet nicht antwortfähig).

Bob führt einmal ein Ratcheting durch, wenn er eine ungebundene eingehende Sitzung erstellt, und erstellt keine entsprechende ausgehende Sitzung (ungebunden bedeutet nicht antwortbar).

Alice sendet weiterhin New Session (NS) Nachrichten an Bob, bis sie eine von Bobs New Session Reply (NSR) Nachrichten erhält. Sie verwendet dann die KDF-Ergebnisse des NSR-Payload-Abschnitts als Eingaben für die Session-Ratchets (siehe DH Ratchet KDF) und beginnt mit dem Senden von Existing Session (ES) Nachrichten.

Für jede empfangene NS-Nachricht erstellt Bob eine neue eingehende Sitzung und verwendet die KDF-Ergebnisse des Antwort-Payload-Abschnitts als Eingaben für die neue eingehende und ausgehende ES DH Ratchet.

Für jede erforderliche Antwort sendet Bob Alice eine NSR-Nachricht mit der Antwort in der Payload. Es ist erforderlich, dass Bob für jede NSR neue ephemerale Schlüssel verwendet.

Bob muss eine ES-Nachricht von Alice auf einer der eingehenden Sessions erhalten, bevor er ES-Nachrichten auf der entsprechenden ausgehenden Session erstellt und sendet.

Alice sollte einen Timer für den Empfang einer NSR-Nachricht von Bob verwenden. Wenn der Timer abläuft, sollte die Sitzung entfernt werden.

Um einen KCI- und/oder Ressourcenerschöpfungsangriff zu vermeiden, bei dem ein Angreifer Bobs NSR-Antworten verwirft, um Alice dazu zu bringen, weiterhin NS-Nachrichten zu senden, sollte Alice vermeiden, neue Sitzungen zu Bob zu starten, nachdem eine bestimmte Anzahl von Wiederholungsversuchen aufgrund von Timer-Ablauf aufgetreten ist.

Alice und Bob führen jeweils ein DH ratchet für jeden empfangenen NextKey-Block durch.

Alice und Bob generieren jeweils neue Tag-Ratchets und zwei symmetrische Schlüssel-Ratchets nach jedem DH-Ratchet. Für jede neue ES-Nachricht in einer bestimmten Richtung rücken Alice und Bob die Session-Tag- und symmetrischen Schlüssel-Ratchets vor.

Die Häufigkeit von DH-Ratchets nach dem anfänglichen Handshake ist implementierungsabhängig. Während das Protokoll eine Grenze von 65535 Nachrichten festlegt, bevor ein Ratchet erforderlich ist, kann häufigeres Ratcheting (basierend auf der Nachrichtenanzahl, der verstrichenen Zeit oder beidem) zusätzliche Sicherheit bieten.

Nach dem finalen Handshake KDF bei gebundenen Sessions müssen Bob und Alice die Noise Split()-Funktion auf dem resultierenden CipherState ausführen, um unabhängige symmetrische und Tag-Chain-Schlüssel für eingehende und ausgehende Sessions zu erstellen.

#### KEY AND TAG SET IDS

Schlüssel- und Tag-Set-ID-Nummern werden verwendet, um Schlüssel und Tag-Sets zu identifizieren. Schlüssel-IDs werden in NextKey-Blöcken verwendet, um den gesendeten oder verwendeten Schlüssel zu identifizieren. Tag-Set-IDs werden (zusammen mit der Nachrichtennummer) in ACK-Blöcken verwendet, um die bestätigte Nachricht zu identifizieren. Sowohl Schlüssel- als auch Tag-Set-IDs gelten für die Tag-Sets einer einzelnen Richtung. Schlüssel- und Tag-Set-ID-Nummern müssen sequenziell sein.

In den ersten Tag-Sets, die für eine Session in jede Richtung verwendet werden, ist die Tag-Set-ID 0. Es wurden keine NextKey-Blöcke gesendet, daher gibt es keine Key-IDs.

Um einen DH-Ratchet zu beginnen, überträgt der Sender einen neuen NextKey-Block mit einer Schlüssel-ID von 0. Der Empfänger antwortet mit einem neuen NextKey-Block mit einer Schlüssel-ID von 0. Der Sender beginnt dann mit der Verwendung eines neuen Tag-Sets mit einer Tag-Set-ID von 1.

Nachfolgende Tag-Sets werden ähnlich generiert. Für alle Tag-Sets, die nach NextKey-Austauschen verwendet werden, ist die Tag-Set-Nummer (1 + Alices Key-ID + Bobs Key-ID).

Schlüssel- und Tag-Set-IDs beginnen bei 0 und werden sequenziell erhöht. Die maximale Tag-Set-ID ist 65535. Die maximale Schlüssel-ID ist 32767. Wenn ein Tag-Set fast erschöpft ist, muss der Tag-Set-Sender einen NextKey-Austausch initiieren. Wenn Tag-Set 65535 fast erschöpft ist, muss der Tag-Set-Sender eine neue Session initiieren, indem er eine New Session-Nachricht sendet.

Mit einer Streaming-Maximalnachrichtengröße von 1730 und unter der Annahme, dass keine Neuübertragungen stattfinden, beträgt die theoretische maximale Datenübertragung mit einem einzigen Tag-Set 1730 * 65536 ~= 108 MB. Das tatsächliche Maximum wird aufgrund von Neuübertragungen niedriger sein.

Das theoretische Maximum der Datenübertragung mit allen 65536 verfügbaren Tag-Sets, bevor die Sitzung verworfen und ersetzt werden müsste, beträgt 64K * 108 MB ~= 6,9 TB.

#### DH RATCHET MESSAGE FLOW

Der nächste Schlüsselaustausch für einen Tag-Satz muss vom Sender dieser Tags (dem Besitzer des ausgehenden Tag-Satzes) initiiert werden. Der Empfänger (Besitzer des eingehenden Tag-Satzes) wird antworten. Bei typischem HTTP GET-Traffic auf der Anwendungsschicht wird Bob mehr Nachrichten senden und wird zuerst ratchet, indem er den Schlüsselaustausch initiiert; das untenstehende Diagramm zeigt dies. Wenn Alice ratchet, passiert dasselbe in umgekehrter Richtung.

Das erste nach dem NS/NSR-Handshake verwendete Tag-Set ist Tag-Set 0. Wenn Tag-Set 0 fast erschöpft ist, müssen neue Schlüssel in beide Richtungen ausgetauscht werden, um Tag-Set 1 zu erstellen. Danach wird ein neuer Schlüssel nur noch in eine Richtung gesendet.

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
Nachdem der DH ratchet für ein ausgehendes Tagset abgeschlossen ist und ein neues ausgehendes Tagset erstellt wurde, sollte es sofort verwendet werden, und das alte ausgehende Tagset kann gelöscht werden.

Nachdem der DH ratchet für ein eingehendes tagset abgeschlossen ist und ein neues eingehendes tagset erstellt wurde, sollte der Empfänger auf Tags in beiden tagsets hören und das alte tagset nach kurzer Zeit löschen, etwa 3 Minuten.

Zusammenfassung der Tag-Set- und Schlüssel-ID-Progression ist in der untenstehenden Tabelle. * zeigt an, dass ein neuer Schlüssel generiert wird.

| New Tag Set ID | Sender key ID | Rcvr key ID |
|----------------|---------------|-------------|
| 0              | n/a           | n/a         |
| 1              | 0 *           | 0 *         |
| 2              | 1 *           | 0           |
| 3              | 1             | 1 *         |
| 4              | 2 *           | 1           |
| 5              | 2             | 2 *         |
| ...            | ...           | ...         |
| 65534          | 32767 *       | 32766       |
| 65535          | 32767         | 32767 *     |
Schlüssel- und Tag-Set-ID-Nummern müssen aufeinanderfolgend sein.

#### DH INITIALIZATION KDF

Dies ist die Definition von DH_INITIALIZE(rootKey, k) für eine einzelne Richtung. Sie erstellt ein Tagset und einen "nächsten Root-Key", der bei Bedarf für einen nachfolgenden DH-Ratchet verwendet wird.

Wir verwenden DH-Initialisierung an drei Stellen. Erstens verwenden wir sie, um einen Tag-Satz für die New Session Replies zu generieren. Zweitens verwenden wir sie, um zwei Tag-Sätze zu generieren, einen für jede Richtung, zur Verwendung in Existing Session-Nachrichten. Schließlich verwenden wir sie nach einem DH Ratchet, um einen neuen Tag-Satz in eine einzige Richtung für zusätzliche Existing Session-Nachrichten zu generieren.

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
#### DH RATCHET KDF

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
### Nachrichtennummern

Ratchets für jede Nachricht, wie bei Signal. Der Session-Tag-Ratchet ist mit dem symmetrischen Schlüssel-Ratchet synchronisiert, aber der Empfänger-Schlüssel-Ratchet kann "zurückbleiben", um Speicher zu sparen.

Der Transmitter ratchetet einmal für jede übertragene Nachricht. Es müssen keine zusätzlichen Tags gespeichert werden. Der Transmitter muss auch einen Zähler für 'N' führen, die Nachrichtennummer der Nachricht in der aktuellen Kette. Der 'N'-Wert ist in der gesendeten Nachricht enthalten. Siehe die Definition des Message Number-Blocks.

Der Empfänger muss um die maximale Fenstergröße vorspringen und die Tags in einem "Tag-Set" speichern, das mit der Sitzung verknüpft ist. Nach dem Empfang kann der gespeicherte Tag verworfen werden, und wenn keine vorherigen nicht empfangenen Tags vorhanden sind, kann das Fenster vorgerückt werden. Der Empfänger sollte den 'N'-Wert, der jedem Sitzungs-Tag zugeordnet ist, beibehalten und prüfen, dass die Nummer in der gesendeten Nachricht diesem Wert entspricht. Siehe die Definition des Message Number-Blocks.

#### KDF

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
### Beispielhafte Implementierung

Ratchets für jede Nachricht, wie in Signal. Jeder symmetrische Schlüssel hat eine zugehörige Nachrichtennummer und ein Session-Tag. Der Session Key Ratchet ist mit dem symmetrischen Tag Ratchet synchronisiert, aber der Receiver Key Ratchet kann "hinterherhinken", um Speicher zu sparen.

Transmitter ratchets einmal für jede übertragene Nachricht. Es müssen keine zusätzlichen Schlüssel gespeichert werden.

Wenn der Empfänger einen Session-Tag erhält und noch nicht den symmetrischen Schlüssel-Ratchet zum zugehörigen Schlüssel vorgerückt hat, muss er zum zugehörigen Schlüssel "aufholen". Der Empfänger wird wahrscheinlich die Schlüssel für alle vorherigen Tags zwischenspeichern, die noch nicht empfangen wurden. Nach dem Empfang kann der gespeicherte Schlüssel verworfen werden, und falls keine vorherigen nicht empfangenen Tags vorhanden sind, kann das Fenster weitergeschoben werden.

Für die Effizienz sind die session tag und symmetric key ratchets getrennt, sodass das session tag ratchet dem symmetric key ratchet vorauslaufen kann. Dies bietet auch zusätzliche Sicherheit, da die session tags über die Leitung übertragen werden.

#### KDF

Das ist die Definition von RATCHET_KEY().

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
### 4a) DH Ratchet

Dies ersetzt das AES-Abschnittsformat, das in der ElGamal/AES+SessionTags-Spezifikation definiert ist.

Dies verwendet das gleiche Blockformat wie in der [NTCP2](/docs/specs/ntcp2/)-Spezifikation definiert. Einzelne Blocktypen werden unterschiedlich definiert.

Es gibt Bedenken, dass die Ermutigung von Implementierern, Code zu teilen, zu Parsing-Problemen führen könnte. Implementierer sollten die Vor- und Nachteile des Code-Teilens sorgfältig abwägen und sicherstellen, dass die Reihenfolge- und gültigen Block-Regeln für beide Kontexte unterschiedlich sind.

### Payload Section Decrypted data

Die verschlüsselte Länge ist der Rest der Daten. Die entschlüsselte Länge ist 16 weniger als die verschlüsselte Länge. Alle Blocktypen werden unterstützt. Typische Inhalte umfassen die folgenden Blöcke:

| Payload Block Type | Type Number | Block Length |
|--------------------|-------------|--------------|
| DateTime           | 0           | 7            |
| Termination (TBD)  | 4           | 9 typ.       |
| Options (TBD)      | 5           | 21+          |
| Message Number (TBD) | 6           | TBD          |
| Next Key           | 7           | 3 or 35      |
| ACK                | 8           | 4 typ.       |
| ACK Request        | 9           | 3            |
| Garlic Clove       | 11          | varies       |
| Padding            | 254         | varies       |
### Unencrypted data

Es gibt null oder mehr Blöcke im verschlüsselten Frame. Jeder Block enthält eine Ein-Byte-Kennung, eine Zwei-Byte-Längenangabe und null oder mehr Datenbytes.

Für die Erweiterbarkeit MÜSSEN Empfänger Blöcke mit unbekannten Typnummern ignorieren und sie als Padding behandeln.

Verschlüsselte Daten sind maximal 65535 Bytes groß, einschließlich eines 16-Byte-Authentifizierungsheaders, sodass die maximalen unverschlüsselten Daten 65519 Bytes betragen.

(Poly1305 Authentifizierungs-Tag nicht gezeigt):

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
### Block Ordering Rules

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

In der Existing Session Nachricht sind keine Blöcke erforderlich, und die Reihenfolge ist nicht spezifiziert, außer für die folgenden Anforderungen:

Termination, falls vorhanden, muss der letzte Block außer Padding sein. Padding, falls vorhanden, muss der letzte Block sein.

Es können mehrere Garlic Clove-Blöcke in einem einzigen Frame vorhanden sein. Es können bis zu zwei Next Key-Blöcke in einem einzigen Frame vorhanden sein. Mehrere Padding-Blöcke sind in einem einzigen Frame nicht erlaubt. Andere Blocktypen werden wahrscheinlich keine mehrfachen Blöcke in einem einzigen Frame haben, aber es ist nicht verboten.

### DateTime

Eine Ablaufzeit. Hilft bei der Verhinderung von Antworten. Bob muss validieren, dass die Nachricht aktuell ist, unter Verwendung dieses Zeitstempels. Bob muss einen Bloom-Filter oder anderen Mechanismus implementieren, um Replay-Angriffe zu verhindern, falls die Zeit gültig ist. Normalerweise nur in New Session-Nachrichten enthalten.

```

+----+----+----+----+----+----+----+
  | 0  |    4    |     timestamp     |
  +----+----+----+----+----+----+----+

  blk :: 0
  size :: 2 bytes, big endian, value = 4
  timestamp :: Unix timestamp, unsigned seconds.
               Wraps around in 2106

```
### 4b) Session Tag Ratchet

Eine einzelne entschlüsselte Garlic Clove wie in [I2NP](/docs/specs/i2np/) spezifiziert, mit Änderungen zur Entfernung von Feldern, die unbenutzt oder redundant sind. Warnung: Dieses Format unterscheidet sich erheblich von dem für ElGamal/AES. Jede Clove ist ein separater Payload-Block. Garlic Cloves dürfen nicht über Blöcke oder über ChaChaPoly-Frames hinweg fragmentiert werden.

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
         the Garlic Clove section of [I2NP](/docs/specs/i2np/).
         Length varies but is typically 1, 33, or 37 bytes

  type :: I2NP message type

  Message_ID :: 4 byte `Integer` I2NP message ID

  Expiration :: 4 bytes, seconds since the epoch

```
Hinweise:

- Implementierer müssen sicherstellen, dass beim Lesen eines Blocks
  fehlerhafte oder bösartige Daten nicht dazu führen, dass
  Lesevorgänge in den nächsten Block überlaufen.

- Das in [I2NP](/docs/specs/i2np/) spezifizierte Clove Set Format wird nicht verwendet.
  Jeder Clove ist in seinem eigenen Block enthalten.

- Der I2NP-Message-Header ist 9 Bytes groß und hat ein identisches Format
  zu dem, das in [NTCP2](/docs/specs/ntcp2/) verwendet wird.

- Das Certificate, die Message ID und die Expiration aus der
  Garlic Message Definition in [I2NP](/docs/specs/i2np/) sind nicht enthalten.

- Das Certificate, die Clove ID und die Expiration aus der
  Garlic Clove Definition in [I2NP](/docs/specs/i2np/) sind nicht enthalten.

Begründung:

- Die Zertifikate wurden nie verwendet.
- Die separaten Nachrichten-ID und Clove-IDs wurden nie verwendet.
- Die separaten Ablaufzeiten wurden nie verwendet.
- Die Gesamteinsparung im Vergleich zu den alten Clove Set- und Clove-Formaten
  beträgt etwa 35 Bytes für 1 Clove, 54 Bytes für 2 Cloves
  und 73 Bytes für 3 Cloves.
- Das Blockformat ist erweiterbar und neue Felder können
  als neue Blocktypen hinzugefügt werden.

### Termination

Die Implementierung ist optional. Beende die Session. Dies muss der letzte Nicht-Padding-Block im Frame sein. Es werden keine weiteren Nachrichten in dieser Session gesendet.

Nicht erlaubt in NS oder NSR. Nur in Existing Session Nachrichten enthalten.

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
### 4c) Symmetric Key Ratchet

NICHT IMPLEMENTIERT, für weitere Untersuchungen. Aktualisierte Optionen übergeben. Die Optionen umfassen verschiedene Parameter für die Session. Siehe den Abschnitt Session Tag Length Analysis weiter unten für weitere Informationen.

Der Options-Block kann eine variable Länge haben, da more_options vorhanden sein können.

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
SOTW ist die Empfehlung des Senders an den Empfänger für das eingehende Tag-Fenster des Empfängers (der maximale Lookahead). RITW ist die Erklärung des Senders über das eingehende Tag-Fenster (maximaler Lookahead), das er zu verwenden plant. Jede Seite setzt dann den Lookahead basierend auf einem Minimum oder Maximum oder einer anderen Berechnung fest oder passt ihn an.

Hinweise:

- Die Unterstützung für nicht-standardmäßige Session-Tag-Längen wird hoffentlich
  niemals erforderlich sein.
- Das Tag-Fenster ist MAX_SKIP in der Signal-Dokumentation.

Probleme:

- Die Optionsverhandlung ist noch zu bestimmen.
- Standardwerte sind noch zu bestimmen.
- Padding- und Verzögerungsoptionen werden von NTCP2 übernommen,
  aber diese Optionen wurden dort noch nicht vollständig implementiert oder untersucht.

### Message Numbers

Die Implementierung ist optional. Die Länge (Anzahl der gesendeten Nachrichten) im vorherigen Tag-Set (PN). Der Empfänger kann Tags, die höher als PN sind, sofort aus dem vorherigen Tag-Set löschen. Der Empfänger kann Tags, die kleiner oder gleich PN sind, aus dem vorherigen Tag-Set nach kurzer Zeit (z.B. 2 Minuten) verfallen lassen.

```

+----+----+----+----+----+
  | 6  |  size   |  PN    |
 +----+----+----+----+----+

  blk :: 6
  size :: 2
  PN :: 2 bytes big endian. The index of the last tag sent in the previous tag set.

```
Hinweise:

- Die maximale PN ist 65535.
- Die Definition von PN ist gleich der Definition von Signal, minus eins.
  Dies ist ähnlich zu dem, was Signal macht, aber in Signal sind PN und N im Header.
  Hier befinden sie sich im verschlüsselten Nachrichteninhalt.
- Sende diesen Block nicht in Tag-Set 0, da es kein vorheriges Tag-Set gab.

### 5) Payload

Der nächste DH ratchet key befindet sich in der Payload und ist optional. Wir führen nicht jedes Mal ein ratchet durch. (Das unterscheidet sich von Signal, wo er sich im Header befindet und jedes Mal gesendet wird)

Für das erste Ratchet ist Key ID = 0.

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
- Es ist möglicherweise nicht unbedingt notwendig, aber es ist nützlich für das Debugging.
  Signal verwendet keine Key ID.
- Die maximale Key ID ist 32767.
- In dem seltenen Fall, dass die Tag-Sätze in beide Richtungen gleichzeitig ratcheting betreiben, enthält ein Frame zwei Next Key-Blöcke, einen für den Forward-Schlüssel und einen für den Reverse-Schlüssel.
- Schlüssel- und Tag-Satz-ID-Nummern müssen sequenziell sein.
- Siehe den DH Ratchet-Abschnitt oben für Details.

### Payload-Sektion Entschlüsselte Daten

Dies wird nur gesendet, wenn ein Ack-Request-Block empfangen wurde. Mehrere Acks können vorhanden sein, um mehrere Nachrichten zu bestätigen.

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
- In den ersten Tag-Sets, die für eine Sitzung in jeder Richtung verwendet werden, ist die Tag-Set-ID 0.
- Es wurden keine NextKey-Blöcke gesendet, daher gibt es keine Schlüssel-IDs.
- Für alle Tag-Sets, die nach NextKey-Austauschen verwendet werden, ist die Tag-Set-Nummer (1 + Alices Schlüssel-ID + Bobs Schlüssel-ID).

### Unverschlüsselte Daten

Fordere eine in-band Bestätigung an. Um die out-of-band DeliveryStatus Message in der Garlic Clove zu ersetzen.

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
### Regeln für die Blockreihenfolge

Alles Padding befindet sich innerhalb von AEAD-Frames. TODO Padding innerhalb von AEAD sollte grob den ausgehandelten Parametern entsprechen. TODO Alice hat ihre angeforderten tx/rx min/max-Parameter in der NS-Nachricht gesendet. TODO Bob hat seine angeforderten tx/rx min/max-Parameter in der NSR-Nachricht gesendet. Aktualisierte Optionen können während der Datenphase gesendet werden. Siehe Optionsblock-Informationen oben.

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

- All-Zero-Padding ist in Ordnung, da es verschlüsselt wird.
- Padding-Strategien sind noch zu bestimmen.
- Reine Padding-Frames sind erlaubt.
- Der Padding-Standard beträgt 0-15 Bytes.
- Siehe Optionsblock für die Aushandlung von Padding-Parametern
- Siehe Optionsblock für Min/Max-Padding-Parameter
- Die Router-Reaktion bei Verletzung ausgehandelter Padding-Parameter ist implementierungsabhängig.

### DateTime

Implementierungen sollten unbekannte Block-Typen für Vorwärtskompatibilität ignorieren.

### Garlic Clove

- Die Padding-Länge soll entweder nachrichtenbasiert unter Berücksichtigung von Schätzungen der Längenverteilung festgelegt werden, oder es sollten zufällige Verzögerungen hinzugefügt werden. Diese Gegenmaßnahmen sind zu implementieren, um DPI zu widerstehen, da Nachrichtengrößen andernfalls preisgeben würden, dass I2P-Traffic über das Transportprotokoll übertragen wird. Das genaue Padding-Schema ist ein Bereich für zukünftige Arbeiten, Anhang A liefert weitere Informationen zu diesem Thema.

## Typical Usage Patterns

### Beendigung

Dies ist der typischste Anwendungsfall, und die meisten nicht-HTTP-Streaming-Anwendungsfälle werden ebenfalls identisch zu diesem Anwendungsfall sein. Eine kleine anfängliche Nachricht wird gesendet, eine Antwort folgt, und zusätzliche Nachrichten werden in beide Richtungen gesendet.

Ein HTTP GET passt normalerweise in eine einzige I2NP-Nachricht. Alice sendet eine kleine Anfrage mit einer einzigen neuen Session-Nachricht und bündelt ein Antwort-leaseSet. Alice schließt sofortiges Ratchet zu einem neuen Schlüssel ein. Enthält Signatur zur Bindung an das Ziel. Keine Bestätigung angefordert.

Bob ratchet sofort.

Alice führt das Ratcheting sofort durch.

Setzt mit diesen Sitzungen fort.

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
### Optionen

Alice hat drei Optionen:

1) Sende nur die erste Nachricht (Fenstergröße = 1), wie bei HTTP GET. Nicht empfohlen.

2) Senden bis zum Streaming-Fenster, aber mit demselben Elligator2-kodierten Klartext-Public-Key. Alle Nachrichten enthalten denselben nächsten Public Key (ratchet). Dies wird für OBGW/IBEP sichtbar sein, da sie alle mit demselben Klartext beginnen. Der Ablauf erfolgt wie in 1). Nicht empfohlen.

3) Empfohlene Implementierung. Sende bis zu streaming window, aber verwende einen anderen Elligator2-kodierten Klartext-öffentlichen Schlüssel (Session) für jeden. Alle Nachrichten enthalten denselben nächsten öffentlichen Schlüssel (ratchet). Dies wird für OBGW/IBEP nicht sichtbar sein, da sie alle mit unterschiedlichem Klartext beginnen. Bob muss erkennen, dass sie alle denselben nächsten öffentlichen Schlüssel enthalten, und auf alle mit demselben ratchet antworten. Alice verwendet diesen nächsten öffentlichen Schlüssel und setzt fort.

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
### Nachrichtennummern

Eine einzelne Nachricht, mit einer einzelnen erwarteten Antwort. Zusätzliche Nachrichten oder Antworten können gesendet werden.

Ähnlich wie HTTP GET, aber mit kleineren Optionen für die Fenstergröße und Lebensdauer der Sitzungs-Tags. Möglicherweise sollte kein Ratchet angefordert werden.

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
### Nächster DH Ratchet Public Key

Mehrere anonyme Nachrichten, ohne erwartete Antworten.

In diesem Szenario fordert Alice eine Sitzung an, aber ohne Bindung. Eine neue Sitzungsnachricht wird gesendet. Keine Antwort-LS wird gebündelt. Eine Antwort-DSM wird gebündelt (dies ist der einzige Anwendungsfall, der gebündelte DSMs erfordert). Kein nächster Schlüssel ist enthalten. Keine Antwort oder Ratchet wird angefordert. Kein Ratchet wird gesendet. Optionen setzen das Session-Tags-Fenster auf null.

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
### Bestätigung

Eine einzelne anonyme Nachricht, ohne erwartete Antwort.

Eine einmalige Nachricht wird gesendet. Keine Antwort-LS oder DSM sind gebündelt. Kein nächster Schlüssel ist enthalten. Keine Antwort oder Ratchet wird angefordert. Kein Ratchet wird gesendet. Optionen setzen das Session-Tags-Fenster auf null.

```

Alice                           Bob

  One-Time Message (1d)   ------------------->
  with bundled message
  without bundled LS
  without bundled Delivery Status Message

```
### Ack-Anfrage

Langlebige Sitzungen können jederzeit ein Ratcheting durchführen oder anfordern, um die Forward Secrecy ab diesem Zeitpunkt aufrechtzuerhalten. Sitzungen müssen ein Ratcheting durchführen, wenn sie sich dem Limit gesendeter Nachrichten pro Sitzung nähern (65535).

## Implementation Considerations

### Padding

Wie beim bestehenden ElGamal/AES+SessionTag-Protokoll müssen Implementierungen die Session-Tag-Speicherung begrenzen und sich gegen Speichererschöpfungsangriffe schützen.

Einige empfohlene Strategien umfassen:

- Harte Begrenzung der Anzahl gespeicherter Session-Tags
- Aggressives Ablaufen von inaktiven eingehenden Sessions bei Speicherdruck
- Begrenzung der Anzahl eingehender Sessions, die an ein einzelnes entferntes Ziel gebunden sind
- Adaptive Reduzierung des Session-Tag-Fensters und Löschung alter ungenutzter Tags
  bei Speicherdruck
- Verweigerung des Ratcheting auf Anfrage bei Speicherdruck

### Andere Blocktypen

Empfohlene Parameter und Timeouts:

- NSR tagset Größe: 12 tsmin und tsmax
- ES tagset 0 Größe: tsmin 24, tsmax 160
- ES tagset (1+) Größe: 160 tsmin und tsmax
- NSR tagset Timeout: 3 Minuten für Empfänger
- ES tagset Timeout: 8 Minuten für Sender, 10 Minuten für Empfänger
- Vorheriges ES tagset entfernen nach: 3 Minuten
- Tagset Look-ahead von Tag N: min(tsmax, tsmin + N/4)
- Tagset Trim hinter Tag N: min(tsmax, tsmin + N/4) / 2
- Nächsten Schlüssel senden bei Tag: TBD
- Nächsten Schlüssel senden nach tagset Lebensdauer: TBD
- Sitzung ersetzen wenn NS empfangen nach: 3 Minuten
- Max. Uhrenabweichung: -5 Minuten bis +2 Minuten
- NS Replay-Filter Dauer: 5 Minuten
- Padding-Größe: 0-15 Bytes (andere Strategien TBD)

### Zukünftige Arbeiten

Im Folgenden finden Sie Empfehlungen zur Klassifizierung eingehender Nachrichten.

### X25519 Only

Bei einem tunnel, der ausschließlich mit diesem Protokoll verwendet wird, führe die Identifikation so durch, wie es derzeit mit ElGamal/AES+SessionTags gemacht wird:

Behandeln Sie zunächst die Anfangsdaten als Session-Tag und schlagen Sie das Session-Tag nach. Falls gefunden, entschlüsseln Sie mit den gespeicherten Daten, die diesem Session-Tag zugeordnet sind.

Falls nicht gefunden, behandeln Sie die anfänglichen Daten als DH public key und Nonce. Führen Sie eine DH-Operation und die angegebene KDF durch und versuchen Sie, die verbleibenden Daten zu entschlüsseln.

### HTTP GET

Bei einem Tunnel, der sowohl dieses Protokoll als auch ElGamal/AES+SessionTags unterstützt, klassifiziere eingehende Nachrichten wie folgt:

Aufgrund eines Fehlers in der ElGamal/AES+SessionTags-Spezifikation wird der AES-Block nicht auf eine zufällige Länge aufgefüllt, die nicht durch 16 teilbar ist. Daher ist die Länge von Existing Session-Nachrichten modulo 16 immer 0, und die Länge von New Session-Nachrichten modulo 16 ist immer 2 (da der ElGamal-Block 514 Bytes lang ist).

Wenn die Länge mod 16 nicht 0 oder 2 ist, behandeln Sie die ursprünglichen Daten als session tag und schlagen Sie den session tag nach. Falls gefunden, entschlüsseln Sie mit den gespeicherten Daten, die mit diesem session tag verknüpft sind.

Wenn nicht gefunden und die Länge modulo 16 nicht 0 oder 2 ist, behandeln Sie die ursprünglichen Daten als DH-Public-Key und Nonce. Führen Sie eine DH-Operation und die angegebene KDF durch und versuchen Sie, die verbleibenden Daten zu entschlüsseln. (basierend auf der relativen Traffic-Mischung und den relativen Kosten von X25519- und ElGamal-DH-Operationen kann dieser Schritt stattdessen zuletzt durchgeführt werden)

Andernfalls, wenn die Länge Modulo 16 gleich 0 ist, behandeln Sie die Anfangsdaten als ElGamal/AES session tag und suchen Sie nach dem session tag. Falls gefunden, entschlüsseln Sie mit den gespeicherten Daten, die mit diesem session tag verknüpft sind.

Falls nicht gefunden und die Daten mindestens 642 (514 + 128) Bytes lang sind und die Länge mod 16 gleich 2 ist, behandle die anfänglichen Daten als ElGamal-Block. Versuche, die verbleibenden Daten zu entschlüsseln.

Beachten Sie, dass wenn die ElGamal/AES+SessionTag-Spezifikation aktualisiert wird, um non-mod-16 padding zu erlauben, die Dinge anders gemacht werden müssen.

### HTTP POST

Erste Implementierungen basieren auf bidirektionalem Verkehr in den höheren Schichten. Das bedeutet, die Implementierungen nehmen an, dass Verkehr in die entgegengesetzte Richtung bald übertragen wird, was jede erforderliche Antwort auf der ECIES-Schicht erzwingt.

Allerdings kann bestimmter Datenverkehr unidirektional oder sehr bandbreitenschonend sein, sodass kein höherschichtiger Datenverkehr vorhanden ist, um eine zeitnahe Antwort zu generieren.

Der Empfang von NS- und NSR-Nachrichten erfordert eine Antwort; der Empfang von ACK Request- und Next Key-Blöcken erfordert ebenfalls eine Antwort.

Eine ausgereifte Implementierung kann einen Timer starten, wenn eine dieser Nachrichten empfangen wird, die eine Antwort erfordert, und eine "leere" Antwort (ohne Garlic Clove Block) auf der ECIES-Ebene generieren, falls kein Rückverkehr in einem kurzen Zeitraum gesendet wird (z.B. 1 Sekunde).

Es kann auch angemessen sein, ein noch kürzeres Timeout für Antworten auf NS- und NSR-Nachrichten zu verwenden, um den Traffic so schnell wie möglich zu den effizienten ES-Nachrichten zu verlagern.

## Analysis

### Repliable Datagram

Der Message-Overhead für die ersten beiden Nachrichten in jede Richtung ist wie folgt. Dies setzt voraus, dass nur eine Nachricht in jede Richtung vor der ACK gesendet wird, oder dass alle zusätzlichen Nachrichten spekulativ als Existing Session-Nachrichten gesendet werden. Wenn es keine spekulativen ACKs von zugestellten Session-Tags gibt, ist der Overhead des alten Protokolls viel höher.

Es wird keine Auffüllung für die Analyse des neuen Protokolls angenommen. Kein gebündeltes leaseSet wird angenommen.

### Mehrere Raw Datagrams

Neue Session-Nachricht, gleich in jede Richtung:

```

ElGamal block:
  514 bytes

  AES block:
  - 2 byte tag count
  - 1024 bytes of tags (32 typical)
  - 4 byte payload size
  - 32 byte hash of payload
  - 1 byte flags
  - 1 byte clove count
  - 33 byte Garlic deliv. inst.
  - 16 byte I2NP header
  - 15 byte clove cert, id, exp.
  - 15 byte msg cert, id, exp.
  - 0 byte padding assuming 1936 byte message
  1143 total

  Total:
  1657 bytes
```
Bestehende Sitzungsnachrichten, jeweils gleich in jede Richtung:

```

AES block:
  - 32 byte session tag
  - 2 byte tag count
  - 4 byte payload size
  - 32 byte hash of payload
  - 1 byte flags
  - 1 byte clove count
  - 33 byte Garlic deliv. inst.
  - 16 byte I2NP header
  - 15 byte msg cert, id, exp.
  - 15 byte clove cert, id, exp.
  - 0 byte padding assuming 1936 byte message
  151 total
```
```
Four message total (two each direction)
  3616 bytes overhead
```
### Einzelnes Raw-Datagramm

Alice-zu-Bob New Session Nachricht:

```

- 32 byte ephemeral public key
  - 32 byte static public key
  - 16 byte Poly1305 MAC
  - 7 byte DateTime block
  - 3 byte Garlic block overhead
  - 9 byte I2NP header
  - 33 byte Garlic deliv. inst.
  - 16 byte Poly1305 MAC

  Total:
  148 bytes overhead
```
Bob-zu-Alice New Session Reply Nachricht:

```

- 8 byte session tag
  - 32 byte ephemeral public key
  - 16 byte Poly1305 MAC
  - 3 byte Garlic block overhead
  - 9 byte I2NP header
  - 33 byte Garlic deliv. inst.
  - 16 byte Poly1305 MAC

  Total:
  117 bytes overhead
```
Bestehende Sitzungsnachrichten, jeweils gleich in jede Richtung:

```

- 8 byte session tag
  - 3 byte Garlic block overhead
  - 9 byte I2NP header
  - 33 byte Garlic deliv. inst.
  - 16 byte Poly1305 MAC

  Total:
  69 bytes
```
### Langlebige Sitzungen

Insgesamt vier Nachrichten (jeweils zwei in jede Richtung):

```

372 bytes
  90% (approx. 10x) reduction compared to ElGamal/AES+SessionTags
```
Nur Handshake:

```

ElGamal: 1657 + 1657 = 3314 bytes
  Ratchet: 148 _ 117 = 265 bytes
  92% (approx. 12x) reduction compared to ElGamal/AES+SessionTags
```
Langfristige Gesamtmenge (ohne Handshakes):

```
ElGamal: 151 + 32 byte tag sent previously = 183 bytes
  Ratchet: 69 bytes
  64% (approx. 3x) reduction compared to ElGamal/AES+SessionTags
```
### CPU

TODO Diesen Abschnitt aktualisieren, nachdem der Vorschlag stabil ist.

Die folgenden kryptografischen Operationen sind von jeder Partei erforderlich, um New Session und New Session Reply Nachrichten auszutauschen:

- HMAC-SHA256: 3 pro HKDF, gesamt noch festzulegen
- ChaChaPoly: je 2
- X25519 Schlüsselerzeugung: 2 Alice, 1 Bob
- X25519 DH: je 3
- Signaturverifikation: 1 (Bob)

Alice berechnet 5 ECDHs pro gebundener Sitzung (Minimum), 2 für jede NS-Nachricht an Bob und 3 für jede von Bobs NSR-Nachrichten.

Bob berechnet außerdem 6 ECDHs pro gebundene Sitzung, 3 für jede von Alices NS-Nachrichten und 3 für jede seiner NSR-Nachrichten.

Die folgenden kryptographischen Operationen sind für jede Partei bei jeder Existing Session-Nachricht erforderlich:

- HKDF: 2
- ChaChaPoly: 1

### Verteidigung

Die aktuelle Session-Tag-Länge beträgt 32 Bytes. Wir haben noch keine Rechtfertigung für diese Länge gefunden, aber wir forschen weiterhin in den Archiven. Der obige Vorschlag definiert die neue Tag-Länge als 8 Bytes. Die Analyse, die ein 8-Byte-Tag rechtfertigt, ist wie folgt:

Der Session-Tag-Ratchet wird angenommen, zufällige, gleichmäßig verteilte Tags zu generieren. Es gibt keinen kryptographischen Grund für eine bestimmte Session-Tag-Länge. Der Session-Tag-Ratchet ist mit dem symmetrischen Schlüssel-Ratchet synchronisiert, erzeugt aber eine unabhängige Ausgabe davon. Die Ausgaben der beiden Ratchets können unterschiedliche Längen haben.

Daher ist die einzige Sorge eine Session-Tag-Kollision. Es wird angenommen, dass Implementierungen nicht versuchen werden, Kollisionen zu handhaben, indem sie versuchen, mit beiden Sessions zu entschlüsseln; Implementierungen werden den Tag einfach entweder der vorherigen oder der neuen Session zuordnen, und jede Nachricht, die mit diesem Tag in der anderen Session empfangen wird, wird nach dem Fehlschlagen der Entschlüsselung verworfen.

Das Ziel ist es, eine Session-Tag-Länge zu wählen, die groß genug ist, um das Risiko von Kollisionen zu minimieren, aber klein genug, um den Speicherverbrauch zu minimieren.

Dies setzt voraus, dass Implementierungen die Speicherung von Session-Tags begrenzen, um Speichererschöpfungsangriffe zu verhindern. Dies wird auch die Wahrscheinlichkeit erheblich reduzieren, dass ein Angreifer Kollisionen erzeugen kann. Siehe den Abschnitt Implementierungsüberlegungen unten.

Für den schlimmsten Fall nehmen wir einen stark ausgelasteten Server mit 64 neuen eingehenden Sessions pro Sekunde an. Nehmen wir eine Lebensdauer von 15 Minuten für eingehende Session-Tags an (wie derzeit, sollte wahrscheinlich reduziert werden). Nehmen wir ein eingehendes Session-Tag-Fenster von 32 an. 64 * 15 * 60 * 32 = 1.843.200 Tags. Das aktuelle Java I2P Maximum für eingehende Tags liegt bei 750.000 und wurde unseres Wissens nach nie erreicht.

Ein Ziel von 1 zu einer Million (1e-6) Session-Tag-Kollisionen ist wahrscheinlich ausreichend. Die Wahrscheinlichkeit, eine Nachricht unterwegs aufgrund von Überlastung zu verlieren, ist weitaus höher.

Ref: https://en.wikipedia.org/wiki/Birthday_paradox Abschnitt Wahrscheinlichkeitstabelle.

Mit 32-Byte-Session-Tags (256 Bits) beträgt der Session-Tag-Raum 1,2e77. Die Wahrscheinlichkeit einer Kollision mit einer Wahrscheinlichkeit von 1e-18 erfordert 4,8e29 Einträge. Die Wahrscheinlichkeit einer Kollision mit einer Wahrscheinlichkeit von 1e-6 erfordert 4,8e35 Einträge. 1,8 Millionen Tags à 32 Bytes entsprechen insgesamt etwa 59 MB.

Mit 16-Byte-Session-Tags (128 Bits) beträgt der Session-Tag-Bereich 3,4e38. Die Wahrscheinlichkeit einer Kollision mit einer Wahrscheinlichkeit von 1e-18 erfordert 2,6e10 Einträge. Die Wahrscheinlichkeit einer Kollision mit einer Wahrscheinlichkeit von 1e-6 erfordert 2,6e16 Einträge. 1,8 Millionen Tags zu je 16 Bytes ergeben insgesamt etwa 30 MB.

Mit 8-Byte-Session-Tags (64 Bits) beträgt der Session-Tag-Raum 1,8e19. Die Wahrscheinlichkeit einer Kollision mit Wahrscheinlichkeit 1e-18 erfordert 6,1 Einträge. Die Wahrscheinlichkeit einer Kollision mit Wahrscheinlichkeit 1e-6 erfordert 6,1e6 (6.100.000) Einträge. 1,8 Millionen Tags zu je 8 Bytes ergeben insgesamt etwa 15 MB.

6,1 Millionen aktive Tags sind über 3x mehr als unsere Worst-Case-Schätzung von 1,8 Millionen Tags. Die Wahrscheinlichkeit einer Kollision wäre daher geringer als eins zu einer Million. Wir schlussfolgern daher, dass 8-Byte-Session-Tags ausreichend sind. Dies führt zu einer 4x-Reduzierung des Speicherplatzes, zusätzlich zur 2x-Reduzierung, da Übertragungstags nicht gespeichert werden. Somit haben wir eine 8x-Reduzierung des Session-Tag-Speicherverbrauchs im Vergleich zu ElGamal/AES+SessionTags.

Um Flexibilität zu wahren, falls diese Annahmen falsch sein sollten, werden wir ein Feld für die session tag-Länge in den Optionen einfügen, sodass die Standardlänge pro Session überschrieben werden kann. Wir erwarten nicht, dass wir eine dynamische tag-Längen-Verhandlung implementieren müssen, es sei denn, es ist absolut notwendig.

Implementierungen sollten zumindest Session-Tag-Kollisionen erkennen, sie elegant behandeln und die Anzahl der Kollisionen protokollieren oder zählen. Obwohl sie immer noch extrem unwahrscheinlich sind, werden sie viel wahrscheinlicher sein als bei ElGamal/AES+SessionTags und könnten tatsächlich auftreten.

### Parameter

Bei doppelter Anzahl von Sessions pro Sekunde (128) und doppeltem Tag-Fenster (64) haben wir 4-mal so viele Tags (7,4 Millionen). Das Maximum für eine Kollisionswahrscheinlichkeit von eins zu einer Million liegt bei 6,1 Millionen Tags. 12-Byte- (oder sogar 10-Byte-) Tags würden eine enorme Sicherheitsmarge bieten.

Ist jedoch die Chance einer Kollision von eins zu einer Million ein gutes Ziel? Viel größer als die Chance, unterwegs verworfen zu werden, ist nicht sehr nützlich. Das Falsch-Positiv-Ziel für Javas DecayingBloomFilter liegt bei ungefähr 1 zu 10.000, aber selbst 1 zu 1000 ist nicht von schwerwiegender Bedeutung. Durch die Reduzierung des Ziels auf 1 zu 10.000 gibt es ausreichend Spielraum mit 8-Byte-Tags.

### Klassifizierung

Der Sender generiert Tags und Schlüssel dynamisch, sodass keine Speicherung erforderlich ist. Dies halbiert die gesamten Speicheranforderungen im Vergleich zu ElGamal/AES. ECIES-Tags sind 8 Bytes statt 32 für ElGamal/AES. Dies reduziert die gesamten Speicheranforderungen um einen weiteren Faktor 4. Pro-Tag-Sitzungsschlüssel werden beim Empfänger nicht gespeichert, außer bei "Lücken", die bei angemessenen Verlustraten minimal sind.

Die 33%ige Reduzierung der Tag-Ablaufzeit schafft weitere 33% Einsparungen, unter der Annahme kurzer Sitzungszeiten.

Daher beträgt die gesamte Platzersparnis gegenüber ElGamal/AES einen Faktor von 10,7 oder 92%.

## Related Changes

### Nur X25519

Datenbank-Lookups von ECIES-Zielen: Siehe [Proposal 154](/proposals/154-ecies-lookups), jetzt integriert in [I2NP](/docs/specs/i2np/) für Release 0.9.46.

Dieser Vorschlag erfordert LS2-Unterstützung, um den X25519 public key mit dem leaseset zu veröffentlichen. Keine Änderungen sind an den LS2-Spezifikationen in [I2NP](/docs/specs/i2np/) erforderlich. Alle Unterstützung wurde entworfen, spezifiziert und implementiert in [Proposal 123](/proposals/123-new-netdb-entries), das in 0.9.38 implementiert wurde.

### X25519 Shared mit ElGamal/AES+SessionTags

Keine. Dieser Vorschlag erfordert LS2-Unterstützung und eine Eigenschaft, die in den I2CP-Optionen gesetzt werden muss, um aktiviert zu werden. Es sind keine Änderungen an den [I2CP](/docs/specs/i2cp/)-Spezifikationen erforderlich. Alle Unterstützung wurde in [Proposal 123](/proposals/123-new-netdb-entries) entworfen, spezifiziert und implementiert, welcher in 0.9.38 umgesetzt wurde.

Die Option, die zur Aktivierung von ECIES erforderlich ist, ist eine einzelne I2CP-Eigenschaft für I2CP, BOB, SAM oder i2ptunnel.

Typische Werte sind i2cp.leaseSetEncType=4 für nur ECIES, oder i2cp.leaseSetEncType=4,0 für ECIES und ElGamal Dual-Schlüssel.

### Protokollschicht-Antworten

Dieser Abschnitt ist aus [Proposal 123](/proposals/123-new-netdb-entries) kopiert.

Option in SessionConfig Mapping:

```
  i2cp.leaseSetEncType=nnn[,nnn]  The encryption types to be used.
                                  0: ElGamal
                                  1-3: See proposal 145
                                  4: This proposal.
```
### Create Leaseset2 Message

Dieser Vorschlag erfordert LS2, das ab Release 0.9.38 unterstützt wird. Es sind keine Änderungen an den [I2CP](/docs/specs/i2cp/)-Spezifikationen erforderlich. Die gesamte Unterstützung wurde in [Proposal 123](/proposals/123-new-netdb-entries) entworfen, spezifiziert und implementiert, das in 0.9.38 umgesetzt wurde.

### Overhead

Jeder Router, der LS2 mit dualen Schlüsseln unterstützt (0.9.38 oder höher), sollte Verbindungen zu Zielen mit dualen Schlüsseln unterstützen.

ECIES-only Ziele erfordern, dass eine Mehrheit der floodfills auf 0.9.46 aktualisiert wird, um verschlüsselte Lookup-Antworten zu erhalten. Siehe [Proposal 154](/proposals/154-ecies-lookups).

ECIES-only Ziele können nur mit anderen Zielen verbinden, die entweder ECIES-only oder dual-key sind.
