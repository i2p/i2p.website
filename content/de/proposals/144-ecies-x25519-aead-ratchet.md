---
title: "ECIES-X25519-AEAD-Ratchet"
number: "144"
author: "zzz, chisana, orignal"
created: "2018-11-22"
lastupdated: "2025-03-05"
status: "Closed"
thread: "http://zzz.i2p/topics/2639"
target: "0.9.46"
implementedin: "0.9.46"
---

## Hinweis
Netzwerkbereitstellung und -tests im Gange.
Unterliegt geringfügigen Überarbeitungen.
Siehe [SPEC]_ für die offizielle Spezifikation.

Die folgenden Funktionen sind ab Version 0.9.46 nicht implementiert:

- Nachrichtennummern, Optionen und Beendigungsblöcke
- Antworten auf Protokollebene
- Null-Static-Key
- Multicast

## Übersicht

Dies ist ein Vorschlag für den ersten neuen End-to-End-Verschlüsserungstyp
seit dem Beginn von I2P, um ElGamal/AES+SessionTags [Elg-AES]_ zu ersetzen.

Er basiert auf früheren Arbeiten wie folgt:

- Spezifikation der gemeinsamen Strukturen [Common]_
- [I2NP]_ Spezifikation einschließlich LS2
- ElGamal/AES+Session Tags [Elg-AES]_
- http://zzz.i2p/topics/1768 Neue Übersicht über asymmetrische Kryptografie
- Übersicht über kryptografische Grundlagen [CRYPTO-ELG]_
- ECIES http://zzz.i2p/topics/2418
- [NTCP2]_ [Prop111]_
- 123 Neue netDB-Einträge
- 142 Neues Krypto-Template
- [Noise]_ Protokoll
- [Signal]_ doppelter Ratschenschlüssel-Algorithmus

Ziel ist es, neue Verschlüsselung für die End-to-End-,
Ziel-zu-Ziel-Kommunikation zu unterstützen.

Das Design wird einen Noise-Handshake und eine Datenphase einbeziehen, die den doppelten Ratschenschlüssel von Signal integriert.

Alle in diesem Vorschlag erwähnten Verweise auf Signal und Noise dienen nur zur Hintergrundinformation.
Kenntnisse der Signal- und Noise-Protokolle sind nicht erforderlich,
um diesen Vorschlag zu verstehen oder zu implementieren.

### Aktuelle Verwendung von ElGamal

Als Rückblick:
ElGamal 256-Byte-öffentliche Schlüssel können in den folgenden Datenstrukturen gefunden werden.
Verweise siehe Spezifikation der gemeinsamen Strukturen.

- In einer Router-Identität
  Dies ist der Verschlüsselungsschlüssel des Routers.

- In einem Ziel
  Der öffentliche Schlüssel des Ziels wurde für die alte i2cp-zu-i2cp-Verschlüsselung verwendet, die in Version 0.6 deaktiviert wurde. Er wird derzeit nicht verwendet, außer für
  das IV für LeaseSet-Verschlüsselung, das veraltet ist.
  Stattdessen wird der öffentliche Schlüssel im LeaseSet verwendet.

- In einem LeaseSet
  Dies ist der Verschlüsselungsschlüssel des Ziels.

- In einer LS2
  Dies ist der Verschlüsselungsschlüssel des Ziels.

### EncTypes in Key-Zertifikaten

Als Rückblick:
Wir haben Unterstützung für Verschlüsselungstypen hinzugefügt, als wir Unterstützung für Signaturtypen hinzugefügt haben.
Das Verschlüsselungsfeld ist sowohl in Zielen als auch in RouterIdentities stets null.
Ob das jemals geändert werden soll, ist noch zu klären.
Verweise siehe Spezifikation der gemeinsamen Strukturen [Common]_.

### Verwendungen asymmetrischer Kryptografie

Als Rückblick: Wir verwenden ElGamal für:

1) Tunnelbau-Nachrichten (Schlüssel ist in RouterIdentity)
   Eine Ersetzung ist in diesem Vorschlag nicht enthalten.
   Siehe Vorschlag 152 [Prop152]_.

2) Router-zu-Router-Verschlüsselung von netdb und anderen I2NP-Nachrichten (Schlüssel ist in RouterIdentity)
   Hängt von diesem Vorschlag ab.
   Erfordert auch einen Vorschlag für 1) oder das Platzieren des Schlüssels in den RI-Optionen.

3) Client-End-to-End ElGamal+AES/SessionTag (Schlüssel ist im LeaseSet, der Zielschlüssel wird nicht verwendet)
   Ersetzung IST in diesem Vorschlag enthalten.

4) Ephemeral DH für NTCP1 und SSU
   Ersetzung ist in diesem Vorschlag nicht enthalten.
   Siehe Vorschlag 111 für NTCP2.
   Kein aktueller Vorschlag für SSU2.

### Ziele

- Rückwärtskompatibel
- Erfordert und baut auf LS2 (Vorschlag 123) auf
- Nutzung neuer Kryptografie oder primitiver Oberflächen für NTCP2 (Vorschlag 111)
- Keine neuen Kryptografien oder Primitiven erforderlich für die Unterstützung
- Entkopplung von Kryptografie und Signierung aufrechterhalten; Unterstützung aller aktuellen und zukünftigen Versionen
- Neue Kryptografie für Ziele aktivieren
- Neue Kryptografie für Router aktivieren, aber nur für Garlic-Nachrichten - Tunnelbau wäre
  ein separater Vorschlag
- Nichts brechen, das auf 32-Byte-binäre Ziel-Hashes angewiesen ist, z.B. Bittorrent
- 0-RTT-Nachrichtenübertragung mithilfe eines ephemeren-statischen DH beibehalten
- Keine Puffernachrichten auf dieser Protokollebene erforderlich;
  unbegrenzte Nachrichtenübermittlung in beide Richtungen ohne Wartezeit auf eine Antwort unterstützen
- Upgrade auf ephemeres-ephemeres DH nach 1 RTT
- Verarbeitung von Nachrichten außerhalb der Reihenfolge beibehalten
- 256-Bit-Sicherheit beibehalten
- Weiterleitungsgeheimnis hinzufügen
- Authentifizierung hinzufügen (AEAD)
- Viel CPU-effizienter als ElGamal
- Nicht auf Java jbigi angewiesen sein, um DH effizient zu machen
- Minimale DH-Operationen
- Viel bandbreiteneffizienter als ElGamal (514-Byte-ElGamal-Block)
- Unterstützung neuer und alter Kryptografie im gleichen Tunnel bei Bedarf
- Empfänger kann effizient neue und alte Kryptografie, die auf demselben Tunnel herunterkommen, unterscheiden
- Andere können neue und alte oder zukünftige Kryptografie nicht unterscheiden
- Neue vs. bestehende Sitzungs-Längeneinstufung beseitigen (Unterstützung von Padding)
- Keine neuen I2NP-Nachrichten erforderlich
- SHA-256-Prüfsumme im AES-Payload durch AEAD ersetzen
- Unterstützung der Bindung von Sende- und Empfangssitzungen, sodass
  Bestätigungen innerhalb des Protokolls erfolgen können, anstatt vollständig außerhalb.
  Dies wird auch ermöglichen, dass Antworten sofort vorwärts geheim sind.
- Ende-zu-Ende-Verschlüsselung bestimmter Nachrichten (RouterInfo-Speicher) ermöglichen,
  die wir derzeit aufgrund von CPU-Overhead nicht verwenden.
- Nicht das Format der I2NP-Garlic-Nachricht oder der Garlic-Nachrichtenlieferanweisungen ändern.
- Unbenutzte oder redundante Felder im Garlic Clove Set und im Clove-Format beseitigen.

Verschiedene Probleme mit Session-Tags beseitigen, einschließlich:

- Unfähigkeit, AES bis zur ersten Antwort zu verwenden
- Unzuverlässigkeit und Verzögerungen, wenn Tag-Übergabe angenommen wird
- Bandbreitenineffizient, insbesondere bei der ersten Lieferung
- Enorme Platzineffizienz beim Speichern von Tags
- Großer Bandbreitenoverhead bei der Bereitstellung von Tags
- Sehr komplex, schwer implementierbar
- Schwer an verschiedene Anwendungsfälle anzupassen (Streaming vs. Datagramme, Server vs. Client, hohe vs. niedrige Bandbreite)
- Schwachstellen bei der Speicherauslastung aufgrund von Tag-Übergaben

### Nichtziele / Ausschlussbereiche

- Änderungen am LS2-Format (Vorschlag 123 ist abgeschlossen)
- Neuer DHT-Rotationsalgorithmus oder gemeinsame zufällige Generierung
- Neue Verschlüsselung für den Tunnelaufbau.
  Siehe Vorschlag 152 [Prop152]_.
- Neue Verschlüsselung für die Tunnel-Layer-Verschlüsselung.
  Siehe Vorschlag 153 [Prop153]_.
- Methoden der Verschlüsselung, Übertragung und Empfang von I2NP DLM / DSM / DSRM-Nachrichten.
  Keine Änderung.
- Keine LS1-zu-LS2- oder ElGamal/AES-zu-diesem Vorschlags-Kommunikation wird unterstützt.
  Dieser Vorschlag ist ein bidirektionales Protokoll.
  Ziele können die Rückwärtskompatibilität verwalten, indem sie zwei LeaseSets veröffentlichen
  über die gleichen Tunnel, oder beide Verschlüsselungstypen in der LS2 platzieren.
- Änderungen am Bedrohungsmodell
- Implementierungsdetails werden hier nicht diskutiert und sind jedem Projekt überlassen.
- (Optimistisch) Erweiterungen oder Hooks hinzufügen, um Multicast zu unterstützen

### Begründung

ElGamal/AES+SessionTag war unser einziges End-to-End-Protokoll für etwa 15 Jahre,
im Wesentlichen ohne Änderungen am Protokoll.
Es gibt jetzt kryptografische Primitiven, die schneller sind.
Wir müssen die Sicherheit des Protokolls verbessern.
Wir haben auch heuristische Strategien und Workarounds entwickelt, um den
Speicher- und Bandbreiten-Overhead des Protokolls zu minimieren, aber diese Strategien
sind zerbrechlich, schwer zu optimieren, und machen das Protokoll sogar noch anfälliger
für Ausfälle, die zum Sitzungsabbruch führen.

Etwa im gleichen Zeitraum beschreibt die ElGamal/AES+SessionTag-Spezifikation und die zugehörige
Dokumentation, wie bandbreitenaufwendig es ist, Session-Tags zu liefern,
und hat vorgeschlagen, die Lieferung von Session-Tags durch einen "synchronisierten PRNG" zu ersetzen.
Ein synchronisierter PRNG generiert deterministisch die gleichen Tags an beiden Enden,
abgeleitet von einem gemeinsamen Seed.
Ein synchronisierter PRNG kann auch als "Ratsche" bezeichnet werden.
Dieser Vorschlag spezifiziert schließlich diesen Ratschenschlüsselmechanismus und eliminiert die Tag-Lieferung.

Durch die Verwendung eines Ratschenschlüssels (eines synchronisierten PRNG) zur Generierung der
Session-Tags beseitigen wir den Overhead des Sendens von Session-Tags
in der neuen Sitzung-Nachricht und nachfolgenden Nachrichten, wenn nötig.
Für ein typisches Tag-Set von 32 Tags sind dies 1 KB.
Dies beseitigt auch die Speicherung von Session-Tags auf der Sendeseite und halbiert damit die Speicheranforderungen.

Ein vollständiger bidirektionaler Handshake, ähnlich dem Noise IK-Muster, ist erforderlich, um Angriffe auf die Schlüsselkompromittierung zu vermeiden.
Siehe die Noise "Payload Security Properties"-Tabelle in [NOISE]_.
Weitere Informationen zu KCI finden Sie im Paper https://www.usenix.org/system/files/conference/woot15/woot15-paper-hlauschek.pdf

### Bedrohungsmodell

Das Bedrohungsmodell unterscheidet sich etwas von dem für NTCP2 (Vorschlag 111).
Die MitM-Knoten sind der OBEP und der IBGW und es wird angenommen, dass sie einen vollständigen Blick auf
das aktuelle oder historische globale NetDB haben, indem sie mit Floodfills zusammenarbeiten.

Ziel ist es, zu verhindern, dass diese MitMs den Verkehr als
neue und bestehende Sitzungsnachrichten oder als neue Kryptografie vs. alte Kryptografie klassifizieren.

## Detaillierter Vorschlag

Dieser Vorschlag definiert ein neues End-to-End-Protokoll, um ElGamal/AES+SessionTags zu ersetzen.
Das Design wird einen Noise-Handshake und eine Datenphase einbeziehen, die den doppelten Ratschenschlüssel von Signal integriert.

### Zusammenfassung der kryptografischen Gestaltung

Es gibt fünf Teile des Protokolls, die neu gestaltet werden sollen:

- 1) Die neuen und bestehenden Sitzungscontainerformate
  werden durch neue Formate ersetzt.
- 2) ElGamal (256-Byte-öffentliche Schlüssel, 128-Byte-private Schlüssel) wird ersetzt
  durch ECIES-X25519 (32-Byte-öffentliche und -private Schlüssel)
- 3) AES wird ersetzt durch
  AEAD_ChaCha20_Poly1305 (im Folgenden als ChaChaPoly abgekürzt)
- 4) SessionTags werden ersetzt durch Ratschenschlüssel,
  was im Wesentlichen ein kryptografischer, synchronisierter PRNG ist.
- 5) Der AES-Payload, wie er in der ElGamal/AES+SessionTags-Spezifikation definiert ist,
  wird durch ein Blockformat ersetzt, das dem in NTCP2 ähnlich ist.

Jede der fünf Änderungen hat ihren eigenen Abschnitt unten.

### Neue kryptografische Primitive für I2P

Bestehende I2P-Router-Implementierungen erfordern Implementierungen für
die folgenden standardmäßigen kryptografischen Primitive,
die für aktuelle I2P-Protokolle nicht erforderlich sind:

- ECIES (aber das ist im Wesentlichen X25519)
- Elligator2

Bestehende I2P-Router-Implementierungen, die noch nicht [NTCP2]_ ([Prop111]_) implementiert haben,
werden auch Implementierungen benötigen für:

- X25519-Schlüsselerzeugung und DH
- AEAD_ChaCha20_Poly1305 (im Folgenden als ChaChaPoly abgekürzt)
- HKDF

### Kryptotyp

Der Kryptotyp (verwendet in der LS2) ist 4.
Dies zeigt einen little-endian 32-Byte-X25519-öffentlichen Schlüssel an,
und das hier spezifizierte End-to-End-Protokoll.

Kryptotyp 0 ist ElGamal.
Kryptotypen 1-3 sind reserviert für ECIES-ECDH-AES-SessionTag, siehe Vorschlag 145 [Prop145]_.

### Noise-Protokoll-Framework

Dieser Vorschlag bietet die Anforderungen basierend auf dem Noise-Protokoll-Framework
[NOISE]_ (Revision 34, 2018-07-11).
Noise weist ähnliche Eigenschaften wie das Station-To-Station-Protokoll
[STS]_ auf, das die Grundlage für das [SSU]_ Protokoll ist. In Noise-Terminologie ist Alice
die Initiatorin und Bob der Responder.

Dieser Vorschlag basiert auf dem Noise-Protokoll Noise_IK_25519_ChaChaPoly_SHA256.
(Der tatsächliche Bezeichner für die anfängliche Schlüsselableitungsfunktion
ist "Noise_IKelg2_25519_ChaChaPoly_SHA256",
um auf I2P-Erweiterungen hinzuweisen - siehe Abschnitt KDF 1 unten).
Dieses Noise-Protokoll verwendet die folgenden Primitive:

- Interaktives Handshake-Muster: IK
  Alice überträgt sofort ihren statischen Schlüssel an Bob (I)
  Alice kennt bereits Bobs statischen Schlüssel (K)

- Einweg-Handshake-Muster: N
  Alice überträgt ihren statischen Schlüssel nicht an Bob (N)

- DH-Funktion: X25519
  X25519 DH mit einer Schlüssellänge von 32 Bytes, wie in [RFC-7748]_ spezifiziert.

- Chiffre-Funktion: ChaChaPoly
  AEAD_CHACHA20_POLY1305 wie in [RFC-7539]_ Abschnitt 2.8 spezifiziert.
  12-Byte-Nonce, wobei die ersten 4 Bytes auf Null gesetzt sind.
  Identisch mit dem in [NTCP2]_.

- Hash-Funktion: SHA256
  Standardmäßiger 32-Byte-Hash, der in I2P ausgiebig verwendet wird.

Ergänzungen zum Framework
``````````````````````````

Dieser Vorschlag definiert die folgenden Erweiterungen
Noise_IK_25519_ChaChaPoly_SHA256. Diese folgen im Allgemeinen den Richtlinien in
[NOISE]_ Abschnitt 13.

1) Klartext-ephemere Schlüssel werden mit [Elligator2]_ codiert.

2) Die Antwort wird mit einem Klartext-Tag versehen.

3) Das Payload-Format ist für die Nachrichten 1, 2 und die Datenphase definiert.
   Natürlich ist dies in Noise nicht definiert.

Alle Nachrichten enthalten einen [I2NP]_ Garlic-Nachrichtenheader.
Die Datenphase verwendet eine Verschlüsselung, die der in der Noise-Datenphase ähnlich ist, aber nicht kompatibel ist.

### Handshake-Muster

Handshakes verwenden [Noise]_ Handshake-Muster.

Das folgende Buchstabenmapping wird verwendet:

- e = einmaliger ephemerer Schlüssel
- s = statischer Schlüssel
- p = Nachrichten-Payload

Einmalige und ungebundene Sitzungen sind dem Noise-N-Muster ähnlich.

.. raw:: html

  {% highlight lang='dataspec' %}
<- s
  ...
  e es p ->

{% endhighlight %}

Gebundene Sitzungen sind dem Noise-IK-Muster ähnlich.

.. raw:: html

  {% highlight lang='dataspec' %}
<- s
  ...
  e es s ss p ->
  <- tag e ee se
  <- p
  p ->

{% endhighlight %}

### Sitzungen

Das aktuelle ElGamal/AES+SessionTag-Protokoll ist unidirektional.
Auf dieser Ebene weiß der Empfänger nicht, woher eine Nachricht kommt.
Aus- und eingehende Sitzungen sind nicht verbunden.
Bestätigungen erfolgen out-of-band mit einer DeliveryStatusMessage
(in einer GarlicMessage) im Clove.

Es gibt erhebliche Unwirklichkeit in einem unidirektionalen Protokoll.
Jede Antwort muss ebenfalls eine teure "Neue Sitzung"-Nachricht verwenden.
Dies führt zu höherer Bandbreiten-, CPU- und Speichernutzung.

Es gibt auch Sicherheitslücken in einem unidirektionalen Protokoll.
Alle Sitzungen basieren auf ephemeral-static DH.
Ohne Rückweg gibt es keine Möglichkeit für Bob, seinen statischen Schlüssel
auf einen ephemeren Schlüssel zu "ratschen".
Ohne zu wissen, woher eine Nachricht kommt, gibt es keine Möglichkeit, 
den empfangenen ephemeren Schlüssel für ausgehende Nachrichten zu nutzen,
sodass die erste Antwort ebenfalls ephemeral-static DH verwendet.

Für diesen Vorschlag definieren wir zwei Mechanismen, um ein bidirektionales Protokoll zu erstellen -
"Pairing" und "Binding".
Diese Mechanismen bieten erhöhte Effizienz und Sicherheit.

Sitzungskontext
```````````````

Wie bei ElGamal/AES+SessionTags, müssen alle aus- und eingehenden Sitzungen
in einem bestimmten Kontext, entweder im Router-Kontext oder
im Kontext eines bestimmten lokalen Ziels, stattfinden.
In Java I2P wird dieser Kontext als Session Key Manager bezeichnet.

Sitzungen dürfen nicht zwischen Kontexte geteilt werden, da dies
eine Korrelation zwischen den verschiedenen lokalen Zielen
oder zwischen einem lokalen Ziel und einem Router ermöglichen würde.

Wenn ein bestimmtes Ziel sowohl ElGamal/AES+SessionTags
als auch diesen Vorschlag unterstützt, können beide Arten von Sitzungen einen Kontext gemeinsam nutzen.
Siehe Abschnitt 1c) unten.

Paarung von eingehenden und ausgehenden Sitzungen
``````````````````````````````````````````````````

Wenn eine ausgehende Sitzung bei der Initiatorin (Alice) erstellt wird,
wird eine neue eingehende Sitzung erstellt und mit der ausgehenden Sitzung gekoppelt,
es sei denn, es wird keine Antwort erwartet (z.B. rohes Datagramm).

Wenn eine neue eingehende Sitzung erstellt wird, wird sie immer mit einer neuen ausgehenden Sitzung gekoppelt,
es sei denn, es wird keine Antwort angefordert (z.B. rohes Datagramm).

Wenn eine Antwort angefordert und an ein Ziel oder einen Router gebunden wird,
wird diese neue ausgehende Sitzung an dieses Ziel oder diesen Router gebunden
und ersetzt alle vorherigen ausgehenden Sitzungen zu diesem Ziel oder Router.

Durch die Paarung von eingehenden und ausgehenden Sitzungen können wir ein bidirektionales Protokoll erstellen
mit der Fähigkeit, die DH-Schlüssel zu ratschen.

Binding von Sitzungen und Zielen
````````````````````````````````

Es gibt nur eine ausgehende Sitzung zu einem bestimmten Ziel oder Router.
Es können mehrere aktuelle eingehende Sitzungen von einem bestimmten Ziel oder Router vorhanden sein.
Wenn eine neue eingehende Sitzung erstellt wird und Verkehr auf dieser Sitzung empfangen wird
(was als ACK dient), werden alle anderen relativ schnell markiert, um nach etwa einer Minute abzulaufen.
Der Wert der vorherigen Nachrichten, die gesendet wurden (PN), wird überprüft, und wenn es keine
nicht empfangenen Nachrichten (innerhalb des Fensters) in der vorherigen eingehenden Sitzung gibt,
kann die vorherige Sitzung sofort gelöscht werden.

Wenn eine ausgehende Sitzung bei der Initiatorin (Alice) erstellt wird,
wird sie an das entfernteste Ziel (Bob) gebunden,
und alle gekoppelten eingehenden Sitzungen werden ebenfalls an das entfernteste Ziel gebunden.
Wenn die Sitzungen sich ratcheln, bleiben sie an das entfernteste Ziel gebunden.

Wenn eine eingehende Sitzung beim Empfänger (Bob) erstellt wird,
kann sie an das entfernteste Ziel (Alice) gebunden werden, optional von Alice.
Wenn Alice Bindungsinformationen (ihren statischen Schlüssel) in der "Neue Sitzung"-Nachricht einfügt,
wird die Sitzung an dieses Ziel gebunden,
und eine ausgehende Sitzung wird erstellt und an dasselbe Ziel gebunden.
Wenn sich die Sitzungen ratcheln, bleiben sie an das entfernteste Ziel gebunden.

Vorteile des Bindens und Paarens
````````````````````````````````

Für den häufigen Fall von Streaming erwarten wir, dass Alice und Bob das Protokoll folgendermaßen verwenden:

- Alice paart ihre neue ausgehende Sitzung mit einer neuen eingehenden Sitzung, die beide an das entfernteste Ziel (Bob) gebunden sind.
- Alice fügt die Bindungsinformationen und die Signatur sowie eine Antwortenanforderung in die "Neue Sitzung"-Nachricht ein, die sie an Bob sendet.
- Bob paart seine neue eingehende Sitzung mit einer neuen ausgehenden Sitzung, die beide an das entfernteste Ziel (Alice) gebunden sind.
- Bob sendet eine Antwort (Ack) an Alice in der gepaarten Sitzung mit einem Ratchet auf einen neuen DH-Schlüssel.
- Alice ratchelt zu einer neuen ausgehenden Sitzung mit Bobs neuem Schlüssel, gepaart mit der bestehenden eingehenden Sitzung.

Indem eine eingehende Sitzung an ein entferntes Ziel gebunden wird und die eingehende Sitzung
mit einer ausgehenden Sitzung gepaart wird, die an dasselbe Ziel gebunden ist, erzielen wir zwei wesentliche Vorteile:

1) Die anfängliche Antwort von Bob an Alice verwendet ephemeres-ephemeres DH

2) Nachdem Alice Bobs Antwort erhalten und geratscht hat, verwenden alle nachfolgenden Nachrichten
von Alice an Bob ephemeres-ephemeres DH.

Nachrichtliche ACKs
```````````````````

In ElGamal/AES+SessionTags, wenn ein LeaseSet als ein Garlic Clove gebündelt wird
oder Tags geliefert werden, fordert der sendende Router ein ACK an.
Dies ist eine separate Garlic Clove, die eine DeliveryStatus-Nachricht enthält.
Für zusätzliche Sicherheit wird die DeliveryStatus-Nachricht in eine Garlic-Nachricht eingewickelt.
Dieser Mechanismus ist aus Sicht des Protokolls out-of-band.

Im neuen Protokoll, da die eingehenden und ausgehenden Sitzungen gepaart sind,
können ACKs in-band erfolgen. Keine separate Clove ist erforderlich.

Ein explizites ACK ist einfach eine bestehende Sitzungsnachricht ohne I2NP-Block.
In den meisten Fällen kann jedoch auf ein explizites ACK verzichtet werden, da es Rückverkehr gibt.
Es kann wünschenswert sein, dass Implementierungen eine kurze Zeit (vielleicht hundert ms) warten,
bevor sie ein explizites ACK senden, um dem Streaming- oder Anwendungsschicht Zeit zu geben zu antworten.

Implementierungen müssen auch das Senden von ACKs aufschieben, bis nach dem
I2NP-Block verarbeitet wurde, da die Garlic Message eine Database Store-Nachricht
mit einem LeaseSet enthalten kann. Ein aktuelles LeaseSet wird notwendig sein, um das ACK zu routen,
und das externe Ziel (im LeaseSet enthalten) wird notwendig sein, um den bindenden statischen Schlüssel zu überprüfen.

Sitzungs-Timeouts
`````````````````

Ausgehende Sitzungen sollten immer vor eingehenden Sitzungen ablaufen.
Sobald eine ausgehende Sitzung abgelaufen ist und eine neue erstellt wird, wird auch eine neue gekoppelte eingehende
Sitzung erstellt. Wenn es eine alte eingehende Sitzung gab,
darf sie ablaufen.

### Multicast

TBD

### Definitionen
Wir definieren die folgenden Funktionen, die den kryptografischen Bausteinen entsprechen, die verwendet werden.

ZEROLEN
    Null-Längen-Byte-Array

CSRNG(n)
    n-Byte-Ausgabe von einem kryptografisch sicheren Zufallszahlengenerator.

H(p, d)
    SHA-256-Hash-Funktion, die eine Personalisierungszeichenkette p und Daten d übernimmt und
    eine Ausgabe von 32 Byte Länge produziert.
    Wie in [NOISE]_ definiert.
    || unten bedeutet Anhängen.

    Verwenden Sie SHA-256 wie folgt::

        H(p, d) := SHA-256(p || d)

MixHash(d)
    SHA-256-Hash-Funktion, die einen vorherigen Hash h und neue Daten d übernimmt und
    eine Ausgabe von 32 Byte Länge erzeugt.
    || unten bedeutet Anhängen.

    Verwenden Sie SHA-256 wie folgt::

        MixHash(d) := h = SHA-256(h || d)

STREAM
    Der ChaCha20/Poly1305 AEAD wie in [RFC-7539]_ spezifiziert.
    S_KEY_LEN = 32 und S_IV_LEN = 12.

    ENCRYPT(k, n, Klartext, ad)
        Verschlüsselt den Klartext mit dem Chiffre-Schlüssel k und Nonce n, das für
        den Schlüssel k eindeutig sein MUSS.
        Assoziierte Daten ad sind optional.
        Gibt einen Chiffretext zurück, der die Größe des Klartextes plus 16 Byte für das HMAC ist.

        Der gesamte Chiffretext muss von Zufallszahlen nicht zu unterscheiden sein, wenn der Schlüssel geheim ist.

    DECRYPT(k, n, Chiffretext, ad)
        Entschlüsselt den Chiffretext mit dem Chiffre-Schlüssel k und Nonce n.
        Assoziierte Daten ad sind optional.
        Gibt den Klartext zurück.

DH
    X25519 öffentliches Schlüsselaustauschsystem. Private Schlüssel von 32 Bytes, öffentliche Schlüssel von 32
    Bytes, produziert Ausgaben von 32 Bytes. Es hat die folgenden
    Funktionen:

    GENERATE_PRIVATE()
        Generiert einen neuen privaten Schlüssel.

    DERIVE_PUBLIC(privkey)
        Gibt den öffentlichen Schlüssel zurück, der dem gegebenen privaten Schlüssel entspricht.

    GENERATE_PRIVATE_ELG2()
        Generiert einen neuen privaten Schlüssel, der zu einem öffentlichen Schlüssel führt, der für die Elligator2-Codierung geeignet ist.
        Beachten Sie, dass die Hälfte der zufällig generierten privaten Schlüssel nicht geeignet sind und verworfen werden müssen.

    ENCODE_ELG2(pubkey)
        Gibt den Elligator2-kodierten öffentlichen Schlüssel zurück, der dem gegebenen öffentlichen Schlüssel entspricht (inverse Abbildung).
        Kodierte Schlüssel sind little endian.
        Der codierte Schlüssel muss 256 Bits sein, die von zufälligen Daten nicht zu unterscheiden sind.
        Siehe Elligator2-Abschnitt unten für die Spezifikation.

    DECODE_ELG2(pubkey)
        Gibt den öffentlichen Schlüssel zurück, der dem gegebenen Elligator2-kodierten öffentlichen Schlüssel entspricht.
        Siehe Elligator2-Abschnitt unten für die Spezifikation.

    DH(privkey, pubkey)
        Generiert ein gemeinsames Geheimnis aus den gegebenen privaten und öffentlichen Schlüsseln.

HKDF(salt, ikm, info, n)
    Eine kryptografische Schlüsselderivationsfunktion, die einige Eingabeschlüsselmaterial ikm (das
    gute Entropie haben sollte, aber nicht erforderlich ist, ein gleichmäßig zufälliger String zu sein), ein Salt
    mit einer Länge von 32 Bytes, und einen kontextspezifischen 'info'-Wert übernimmt und eine Ausgabe
    von n Bytes erzeugt, die sich als Schlüsselmaterieal eignet.

    Verwenden Sie HKDF wie in [RFC-5869]_ spezifiziert, mit der HMAC-Hash-Funktion SHA-256
    wie in [RFC-2104]_ spezifiziert. Das bedeutet, dass SALT_LEN maximal 32 Bytes ist.

MixKey(d)
    Verwenden Sie HKDF() mit einem vorherigen chainKey und neuen Daten d und
    legt den neuen chainKey und k fest.
    Wie in [NOISE]_ definiert.

    Verwenden Sie HKDF wie folgt::

        MixKey(d) := Ausgabe = HKDF(chainKey, d, "", 64)
                     chainKey = Ausgabewert[0:31]
                     k = Ausgabewert[32:63]

### 1) Nachrichtenformat

Übersicht des aktuellen Nachrichtenformats
````````````````````````````````````````````

Die Garlic-Nachricht, wie in [I2NP]_ spezifiziert, ist wie folgt.
Da ein Designziel darin besteht, dass Zwischenhops neue von alten Krypto nicht unterscheiden können,
kann sich dieses Format nicht ändern, obwohl das Längenfeld redundant ist.
Das Format wird mit dem vollständigen 16-Byte-Header angezeigt, obwohl der
tatsächliche Header in einem anderen Format vorliegen kann, abhängig vom verwendeten Transport.

Wenn die Daten entschlüsselt werden, enthalten sie eine Serie von Garlic-Cloves und zusätzliche Daten, auch bekannt als Clove-Set.

Siehe [I2NP]_ für Details und eine vollständige Spezifikation.

.. raw:: html

  {% highlight lang='dataspec' %}
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

{% endhighlight %}

Übersicht des verschlüsselten Datenformats
````````````````````````````````````````````

Das aktuelle Nachrichtenformat, das seit über 15 Jahren verwendet wird,
ist ElGamal/AES+SessionTags.
In ElGamal/AES+SessionTags gibt es zwei Nachrichtenformate:

1) Neue Sitzung:
- 514-Byte-ElGamal-Block
- AES-Block (mindestens 128 Bytes, Vielfaches von 16)

2) Bestehende Sitzung:
- 32-Byte-Session-Tag
- AES-Block (mindestens 128 Bytes, Vielfaches von 16)

Das Mindest-Padding auf 128 wird in Java I2P implementiert, ist jedoch beim Empfang nicht erforderlich.

Diese Nachrichten werden in einer I2NP-Garlic-Nachricht, die ein Längenfeld enthält, eingekapselt, sodass die Länge bekannt ist.

Hinweis: Es gibt kein definiertes Padding auf eine ungerade Vielfaches von 16,
sodass die neue Sitzung immer (mod 16 == 2) ist,
und eine bestehende Sitzung immer (mod 16 == 0) ist.
Wir müssen dies beheben.

Der Empfänger versucht zunächst, die ersten 32 Bytes als Session-Tag zu finden.
Wenn gefunden, entschlüsselt er den AES-Block.
Wenn nicht gefunden und die Daten sind mindestens (514+16) lang, versucht er, den ElGamal-Block zu entschlüsseln,
und wenn erfolgreich, entschlüsselt er den AES-Block.

Neue Sitzungstags und Vergleich mit Signal
```````````````````````````````````````````

In Signal Double Ratchet enthält der Header:

- DH: Aktueller Ratschenschlüssel
- PN: Vorherige Kettennachrichtlänge
- N: Nachrichtenummer

Signals "Sendeketten" sind grob vergleichbar mit unseren Sets.
Durch die Verwendung eines Session-Tags können wir die meisten davon eliminieren.

In New Session setzen wir nur den öffentlichen Schlüssel in den unverschlüsselten Header.

In Existing Session verwenden wir ein Session-Tag für den Header.
Das Session-Tag ist mit dem aktuellen Ratschenschlüssel und
der Nachrichtenummer assoziiert.

In New Session und Existing Session sind PN und N im verschlüsselten Körper.

In Signal werden die Dinge ständig geratscht. Ein neuer DH öffentlicher Schlüssel erfordert, dass
der Empfänger ratchelt und einen neuen öffentlichen Schlüssel zurücksendet, was auch
als Bestätigung für den empfangenen öffentlichen Schlüssel dient.
Dies wären viel zu viele DH-Operationen für uns.
Daher trennen wir die Bestätigung des empfangenen Schlüssels und die Übertragung eines neuen Schlüssels.
Jede Nachricht, die ein vom neuen DH-Schlüssel generiertes Session-Tag verwendet, stellt ein ACK dar.
Wir übertragen nur einen neuen öffentlichen Schlüssel, wenn wir einen neuen Schlüssel wollen.

Die maximale Anzahl von Nachrichten, bevor das DH ratschern muss, beträgt 65535.

Beim Liefern eines Session-Schlüssels leiten wir den "Tag Set" daraus ab,
anstatt auch Session-Tags liefern zu müssen.
Ein Tag Set kann bis zu 65536 Tags enthalten.
Empfänger sollten jedoch eine "Look-ahead"-Strategie implementieren, anstatt alle möglichen Tags auf einmal zu generieren.
Nur maximal N Tags nach dem letzten guten Tag generieren.
N könnte maximal 128 sein, aber 32 oder sogar weniger könnte die bessere Wahl sein.

### 1a) Neues Sitzungsformat

Neuer Sitzungseinmaliger öffentlicher Schlüssel (32 Bytes) Verschlüsselte Daten und MAC (verbleibende Bytes)

Die New Session-Nachricht kann den statischen öffentlichen Schlüssel des Senders enthalten oder nicht.
Wenn er enthalten ist, wird die umgekehrte Sitzung an diesen Schlüssel gebunden.
Der statische Schlüssel sollte enthalten sein, wenn Antworten erwartet werden,
d.h. für Streaming und replizierbare Datagramme.
Er sollte nicht für rohe Datagramme enthalten sein.

Die New Session-Nachricht ist dem Einweg-Noise-[NOISE]-Muster "N" (wenn der statische Schlüssel nicht gesendet wird) oder dem Zweiweg-Muster "IK" (wenn der statische Schlüssel gesendet wird) ähnlich.

### 1b) Neues Sitzungsformat (mit Binding)

Die Länge beträgt 96 + Payload-Länge.
Verschlüsseltes Format:

.. raw:: html

  {% highlight lang='dataspec' %}
+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   Neuer Sitzung-Ephemerer öffentlicher Schlüssel  |
  +             32 Bytes                   +
  |     Codiert mit Elligator2             |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +         Statischer Schlüssel                     +
  |       ChaCha20 verschlüsselte Daten               +
  +            32 Bytes                   +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +    (MAC) für den statischen Schlüssel Bereich       +
  |             16 Bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload-Bereich            +
  |       ChaCha20 verschlüsselte Daten   |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) für Payload-Bereich     +
  |             16 Bytes                  |
  +----+----+----+----+----+----+----+----+

  Öffentlicher Schlüssel :: 32 Bytes, little endian, Elligator2, Klartext

  Statischer Schlüssel verschlüsselte Daten :: 32 Bytes

  Payload-Bereich verschlüsselte Daten :: restliche Daten minus 16 Bytes

  MAC :: Poly1305-Nachrichtenauthentifizierungscode, 16 Bytes

{% endhighlight %}

Neuer Sitzung-ephemerer Schlüssel
```````````````````````````

Der ephemere Schlüssel ist 32 Bytes, codiert mit Elligator2.
Dieser Schlüssel wird nie wiederverwendet; ein neuer Schlüssel wird mit
jeder Nachricht generiert, einschließlich erneuter Übertragungen.

Statischer Schlüssel
`````````````````

Bei Entschlüsselung: Alices X25519-statischer Schlüssel, 32 Bytes.

Payload
```````

Verschlüsselte Länge ist der Rest der Daten.
Entschlüsselte Länge ist 16 weniger als die verschlüsselte Länge.
Der Payload muss einen DateTime-Block enthalten und enthält in der Regel einen oder mehrere Garlic-Clove-Blöcke.
Siehe den Payload-Abschnitt unten für das Format und zusätzliche Anforderungen.

### 1c) Neues Sitzungsformat (ohne Binding)

Wenn keine Antwort erforderlich ist, wird kein statischer Schlüssel gesendet.

Die Länge beträgt 96 + Payload-Länge.
Verschlüsseltes Format:

.. raw:: html

  {% highlight lang='dataspec' %}
+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   Neuer Sitzung-Ephemerer öffentlicher Schlüssel  |
  +             32 Bytes                   +
  |     Codiert mit Elligator2             |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +           Flag-Bereich                 +
  |       ChaCha20 verschlüsselte Daten   |
  +            32 Bytes                   +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) für oberen Bereich       +
  |             16 Bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload-Bereich            +
  |       ChaCha20 verschlüsselte Daten   |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) für Payload-Bereich     +
  |             16 Bytes                  |
  +----+----+----+----+----+----+----+----+

  Öffentlicher Schlüssel :: 32 Bytes, little endian, Elligator2, Klartext

  Flag-Bereich verschlüsselte Daten :: 32 Bytes

  Payload-Bereich verschlüsselte Daten :: restliche Daten minus 16 Bytes

  MAC :: Poly1305-Nachrichtenauthentifizierungscode, 16 Bytes

{% endhighlight %}

Neuer Sitzung-ephemerer Schlüssel
```````````````````````````

Alices ephemerer Schlüssel.
Der ephemere Schlüssel ist 32 Bytes, codiert mit Elligator2, little endian.
Dieser Schlüssel wird nie wiederverwendet; ein neuer Schlüssel wird mit
jeder Nachricht generiert, einschließlich erneuter Übertragungen.

Entschlüsselte Daten des Flag-Bereichs
``````````````````````````````````````

Der Flag-Bereich enthält nichts.
Er ist immer 32 Bytes groß, da er dieselbe Länge haben muss
wie der statische Schlüssel für New Session-Nachrichten mit Binding.
Bob bestimmt, ob es sich um einen statischen Schlüssel oder einen Flag-Bereich
handelt, indem er prüft, ob die 32 Bytes alle Null sind.

TODO: Irgendwelche Flags hier benötigt?

Payload
```````

Verschlüsselte Länge ist der Rest der Daten.
Entschlüsselte Länge ist 16 weniger als die verschlüsselte Länge.
Payload muss einen DateTime-Block enthalten und enthält in der Regel einen oder mehrere Garlic-Clove-Blöcke.
Siehe den Payload-Abschnitt unten für das Format und zusätzliche Anforderungen.

### 1d) Einmaliges Format (ohne Binding oder Sitzung)

Wenn nur eine einzelne Nachricht erwartet wird,
ist kein Sitzungs-Setup oder statischer Schlüssel erforderlich.

Die Länge beträgt 96 + Payload-Länge.
Verschlüsseltes Format:

.. raw:: html

  {% highlight lang='dataspec' %}
+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |       Ephemerer öffentlicher Schlüssel          |
  +             32 Bytes                   +
  |     Codiert mit Elligator2             |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +           Flag-Bereich                 +
  |       ChaCha20 verschlüsselte Daten   |
  +            32 Bytes                   +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) für oberen Bereich       +
  |             16 Bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload-Bereich            +
  |       ChaCha20 verschlüsselte Daten   |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) für Payload-Bereich     +
  |             16 Bytes                  |
  +----+----+----+----+----+----+----+----+

  Öffentlicher Schlüssel :: 32 Bytes, little endian, Elligator2, Klartext

  Flag-Bereich verschlüsselte Daten :: 32 Bytes

  Payload-Bereich verschlüsselte Daten :: restliche Daten minus 16 Bytes

  MAC :: Poly1305-Nachrichtenauthentifizierungscode, 16 Bytes

{% endhighlight %}

Neuer Sitzungseinmaliger Schlüssel
````````````````````````````````

Der einmalige Schlüssel ist 32 Bytes, codiert mit Elligator2, little endian.
Dieser Schlüssel wird nie wiederverwendet; ein neuer Schlüssel wird mit
jeder Nachricht generiert, einschließlich erneuter Übertragungen.

Entschlüsselte Daten des Flag-Bereichs
````````````````````````````````````

Der Flag-Bereich enthält nichts.
Er ist immer 32 Bytes groß, da er dieselbe Länge haben muss
wie der statische Schlüssel für New Session-Nachrichten mit Binding.
Bob bestimmt, ob es sich um einen statischen Schlüssel oder einen Flag-Bereich
handelt, indem er prüft, ob die 32 Bytes alle Null sind.

TODO: Irgendwelche Flags hier benötigt?

.. raw:: html

  {% highlight lang='dataspec' %}
+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                                       |
  +             Alles Null                +
  |              32 Bytes                 |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+

  Nullen:: Alles Null, 32 Bytes.

{% endhighlight %}

Payload
```````

Verschlüsselte Länge ist der Rest der Daten.
Entschlüsselte Länge ist 16 weniger als die verschlüsselte Länge.
Payload muss einen DateTime-Block enthalten und enthält in der Regel einen oder mehrere Garlic-Clove-Blöcke.
Siehe den Payload-Abschnitt unten für das Format und zusätzliche Anforderungen.

### 1f) KDFs für New Session Message

KDF für den Initial-ChainKey
``````````````````````````

Dies ist standardmäßiges [NOISE]_ für IK mit einem modifizierten Protokollnamen.
Beachten Sie, dass wir denselben Initialisierer sowohl für das IK-Muster (gebundene Sitzungen) als auch für das N-Muster (ungebundene Sitzungen) verwenden.

Der Protokollname wird aus zwei Gründen modifiziert.
Erstens, um anzuzeigen, dass die ephemeren Schlüssel mit Elligator2 codiert sind,
und zweitens, um anzuzeigen, dass MixHash() vor der zweiten Nachricht aufgerufen wird,
um den Tag-Wert zu vermischen.

.. raw:: html

  {% highlight lang='text' %}
Dies ist das "e"-Muster:

  // Protokollname definieren.
  Set protocol_name = "Noise_IKelg2+hs2_25519_ChaChaPoly_SHA256"
   (40 Bytes, US-ASCII-kodiert, keine NULL-Termination).

  // Definieren Sie Hash h = 32 Bytes
  h = SHA256(protocol_name);

  // Definieren Sie ck = 32-Byte-Kettenwert. Kopieren Sie die h-Daten nach ck.
  Set chainKey = h

  // MixHash(null Prologue)
  h = SHA256(h);

  // bis hierhin, kann alles von Alice im Voraus berechnet werden für alle ausgehenden Verbindungen

{% endhighlight %}

KDF für Flag-/Statischer Schlüsselbereich verschlüsselte Inhalte
`````````````````````````````````````````````````

.. raw:: html

  {% highlight lang='text' %}
Dies ist das "e"-Muster:

  // Bobs X25519 static keys
  // bpk wird im Leaseset veröffentlicht
  bsk = GENERATE_PRIVATE()
  bpk = DERIVE_PUBLIC(bsk)

  // Bob Static Pinciple Kiy
  // MixHash(bpk)
  // || unten bedeutet Anhängen
  h = SHA256(h || bpk);

  // bis hierhin, kann alles von Bob im Voraus berechnet werden für alle eingehenden Verbindungen

  // Alices X25519 ephemeral keys
  aesk = GENERATE_PRIVATE_ELG2()
  aepk = DERIVE_PUBLIC(aesk)

  // Alices ephemerer öffentlicher Schlüssel
  // MixHash(aepk)
  // || unten bedeutet Anhängen
  h = SHA256(h || aepk);

  // h wird als assoziiertes Datensatz für das AEAD in der New Session Message
  // aufbewahrt für die New Session Reply KDF
  // eapk wird Klartext in der
  // Beginn der New Session Message
  elg2_aepk = ENCODE_ELG2(aepk)
  // Wie Bob decodiert
  aepk = DECODE_ELG2(elg2_aepk)

  Ende des "e"-Muster.

  Dies ist das "es"-Muster:

  // Noise es
  sharedSecret = DH(aesk, bpk) = DH(bsk, aepk)

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // ChaChaPoly-Parameter zur Verschlüsselung/Entschlüsselung
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  chainKey = keydata[0:31]

  // AEAD-Parameter
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, flag/static key section, ad)

  Ende des "es"-Muster.

  Dies ist das "s"-Muster:

  // MixHash(ciphertext)
  // Gespeichert für die Payload-Bereich KDF
  h = SHA256(h || ciphertext)

  // Alices X25519 static keys
  ask = GENERATE_PRIVATE()
  apk = DERIVE_PUBLIC(ask)

  Ende des "s"-Muster.

{% endhighlight %}

KDF für den Payload-Bereich (mit Alices statischem Schlüssel)
`````````````````````````````````````````````````

.. raw:: html

  {% highlight lang='text' %}
Dies ist das "ss"-Muster:

  // Noise ss
  sharedSecret = DH(ask, bpk) = DH(bsk, apk)

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // ChaChaPoly-Parameter zur Verschlüsselung/Entschlüsselung
  // chainKey aus Statischer Schlüsselbereich
  Set sharedSecret = X25519 DH Ergebnis
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  chainKey = keydata[0:31]

  // AEAD-Parameter
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, payload, ad)

  Ende des "ss"-Muster.

  // MixHash(ciphertext)
  // Gespeichert für die New Session Reply KDF
  h = SHA256(h || ciphertext)

{% endhighlight %}

KDF für den Payload-Bereich (ohne Alices statischen Schlüssel)
`````````````````````````````````````````````````

Beachten Sie, dass dies ein Noise "N"-Muster ist, aber wir verwenden denselben "IK"-Initialisierer
wie für gebundene Sitzungen.

Neue Sitzungsnachrichten können nicht identifiziert werden, ob sie Alices statischen Schlüssel enthalten oder nicht, 
bis der statische Schlüssel entschlüsselt und inspiziert wird, ob er alle Null enthält. 
Daher muss der Empfänger die "IK"-Zustandsmaschine für alle
neuen Sitzungsnachrichten verwenden.
Wenn der statische Schlüssel alle Nullen enthält, muss das "ss"-Muster übersprungen werden.

.. raw:: html

  {% highlight lang='text' %}
chainKey = from Flag-/Statischer Schlüsselbereich
  k = from Flag-/Statischer Schlüsselbereich
  n = 1
  ad = h from Flag-/Statischer Schlüsselbereich
  ciphertext = ENCRYPT(k, n, payload, ad)

{% endhighlight %}

### 1g) Neues Sitzungsantwortformat

Eine oder mehrere neue Sitzungsantworten können als Antwort auf eine einzelne neue Sitzung-Nachricht gesendet werden.
Jede Antwort wird mit einem Tag versehen, das aus einem TagSet für die Sitzung generiert wird.

Die Neue Sitzung Antwort besteht aus zwei Teilen.
Der erste Teil ist der Abschluss des Noise IK-Handshake mit einem vorangestellten Tag.
Die Länge des ersten Teils beträgt 56 Bytes.
Der zweite Teil ist der Datenphasen-Payload.
Die Länge des zweiten Teils beträgt 16 + Payload-Länge.

Gesamtlänge ist 72 + Payload-Länge.
Verschlüsseltes Format:

.. raw:: html

  {% highlight lang='dataspec' %}
+----+----+----+----+----+----+----+----+
  |       Session Tag   8 Bytes           |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Ephemerer öffentlicher Schlüssel           +
  |                                       |
  +            32 Bytes                   +
  |     Codiert mit Elligator2             +
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +  (MAC) für den Schlüsselbereich (keine Daten)  +
  |             16 Bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload-Bereich            +
  |       ChaCha20 verschlüsselte Daten   |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) für den Payload-Bereich +
  |             16 Bytes                  |
  +----+----+----+----+----+----+----+----+

  Tag :: 8 Bytes, Klartext

  Öffentlicher Schlüssel :: 32 Bytes, little endian, Elligator2, Klartext

  MAC :: Poly1305-Nachrichtenauthentifizierungscode, 16 Bytes
         Hinweis: Der ChaCha20-Klartext-Datensatz ist leer (ZEROLEN)

  Payload-Bereich verschlüsselte Daten :: restliche Daten minus 16 Bytes

  MAC :: Poly1305-Nachrichtenauthentifizierungscode, 16 Bytes

{% endhighlight %}

Sitzungstag
```````````

Das Tag wird im Session Tags KDF generiert, wie in
der DH-Initialisierungs-KDF unten gezeigt.
Dies korreliert die Antwort mit der Sitzung.
Der Sitzungsschlüssel aus der DH-Initialisierung wird nicht verwendet.

Neues Sitzungs Antwort Ephemer-Schlüssel
````````````````````````````````

Bobs ephemerer Schlüssel.
Der ephemere Schlüssel ist 32 Bytes, codiert mit Elligator2, little endian.
Dieser Schlüssel wird nie wiederverwendet; ein neuer Schlüssel wird mit
jeder Nachricht generiert, einschließlich erneuter Übertragungen.

Payload
```````
Verschlüsselte Länge ist die Restdatenfläche.
Entschlüsselte Länge ist 16 weniger als die verschlüsselte Länge.
Der Payload-Bereich enthält in der Regel einen oder mehrere Garlic-Clove-Blöcke.
Siehe den Payload-Abschnitt unten für das Format und zusätzliche Anforderungen.

KDF für Reply TagSet
`````````````````````

Eines oder mehrere Tags werden aus dem TagSet generiert, das mit dem
KDF unten initialisiert wird, das den chainKey aus der neuen Sitzung verwendet.

.. raw:: html

  {% highlight lang='text' %}
// Tagset generieren
  tagsetKey = HKDF(chainKey, ZEROLEN, "SessionReplyTags", 32)
  tagset_nsr = DH_INITIALIZE(chainKey, tagsetKey)

{% endhighlight %}

KDF für Reply Key-Bereich verschlüsselte Inhalte
``````````````````````````````````````````````

.. raw:: html

  {% highlight lang='text' %}

// Schlüssel aus der neuen Sitzung Nachricht
  // Alices X25519-Schlüssel
  // apk und aepk werden in der ursprünglichen neuen Sitzung Nachricht gesendet
  // ask = Alices privater statischer Schlüssel
  // apk = Alices öffentlicher statischer Schlüssel
  // aesk = Alices ephemerer privater Schlüssel
  // aepk = Alices ephemerer öffentlicher Schlüssel
  // Bobs X25519-Static-Schlüssel
  // bsk = Bobs privater statischer Schlüssel
  // bpk = Bobs öffentlicher statischer Schlüssel

  // Tag generieren
  tagsetEntry = tagset_nsr.GET_NEXT_ENTRY()
  tag = tagsetEntry.SESSION_TAG

  // MixHash(tag)
  h = SHA256(h || tag)

  Dies ist das "e"-Muster:

  // Bobs X25519 ephemerer Schlüssel
  besk = GENERATE_PRIVATE_ELG2()
  bepk = DERIVE_PUBLIC(besk)

  // Bobs ephemerer öffentlicher Schlüssel
  // MixHash(bepk)
  // || unten bedeutet Anhängen
  h = SHA256(h || bepk);

  // elg2_bepk wird als Klartext in der
  // Beginn der neuen Sitzung Nachricht gesendet
  elg2_bepk = ENCODE_ELG2(bepk)
  // Wie von Bob decodiert
  bepk = DECODE_ELG2(elg2_bepk)

  Ende des "e"-Muster.

  Dies ist das "ee"-Muster:

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // ChaChaPoly-Parameter zur Verschlüsselung/Entschlüsselung
  // chainKey aus der ursprünglichen neuen Sitzung Payload-Bereich
  sharedSecret = DH(aesk, bepk) = DH(besk, aepk)
  keydata = HKDF(chainKey, sharedSecret, "", 32)
  chainKey = keydata[0:31]

  Ende des "ee"-Muster.

  Dies ist das "se"-Muster:

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  sharedSecret = DH(ask, bepk) = DH(besk, apk)
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  chainKey = keydata[0:31]

  // AEAD-Parameter
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, ZEROLEN, ad)

  Ende des "se"-Muster.

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)

  chainKey wird in der Ratchet unten verwendet.

{% endhighlight %}

KDF für Payload-Bereich verschlüsselte Inhalte
``````````````````````````````````````

Dies ist wie die erste bestehende Sitzung-Nachricht,
nach dem Split, jedoch ohne ein separates Tag.
Zusätzlich verwenden wir den Hash von oben, um
den Payload an die NSR-Nachricht zu binden.

.. raw:: html

  {% highlight lang='text' %}

// split()
  keydata = HKDF(chainKey, ZEROLEN, "", 64)
  k_ab = keydata[0:31]
  k_ba = keydata[32:63]
  tagset_ab = DH_INITIALIZE(chainKey, k_ab)
  tagset_ba = DH_INITIALIZE(chainKey, k_ba)

  // AEAD-Parameter für New Session Reply-Payload
  k = HKDF(k_ba, ZEROLEN, "AttachPayloadKDF", 32)
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, payload, ad)
{% endhighlight %}

### Hinweise

Mehrere NSR Nachrichten können als Antwort gesendet werden, jede mit eindeutigen ephemeren Schlüsseln, abhängig von der Größe der Antwort.

Alice und Bob sind verpflichtet, neue ephemere Schlüssel für jede NS und NSR Nachricht zu verwenden.

Alice muss eine von Bobs NSR-Nachrichten empfangen, bevor sie bestehende Sitzung-Nachrichten sendet,
und Bob muss eine bestehende Sitzung-Nachricht von Alice empfangen haben, bevor er bestehende Sitzung-Nachrichten sendet.

Der ``chainKey`` und ``k`` aus Bobs NSR-Payload-Bereich werden als Eingaben für die initialen ES DH Ratchets (in beiden Richtungen, siehe DH Ratchet KDF) verwendet.

Bob muss nur bestehende Sitzungen für die ES Nachrichten beibehalten, die er von Alice erhalten hat.
Alle anderen erstellten ein- und ausgehenden Sitzungen (für mehrere NSRs) sollten
unmittelbar nach Empfang von Alices erster ES Nachricht für eine gegebene Sitzung gelöscht werden.

### 1h) Bestehendes Sitzungsformat

Session-Tag (8 Bytes) Verschlüsselte Daten und MAC (siehe Abschnitt 3 unten)

Format
``````
Verschlüsselt:

.. raw:: html

  {% highlight lang='dataspec' %}
+----+----+----+----+----+----+----+----+
  |       Session Tag                     |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload-Bereich            +
  |       ChaCha20 verschlüsselte Daten   |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +              (MAC)                    +
  |             16 Bytes                  |
  +----+----+----+----+----+----+----+----+

  Session Tag :: 8 Bytes, Klartext

  Payload-Bereich verschlüsselte Daten :: restliche Daten minus 16 Bytes

  MAC :: Poly1305-Nachrichtenauthentifizierungscode, 16 Bytes

{% endhighlight %}

Payload
```````
Verschlüsselte Länge ist die Restdatenfläche.
Entschlüsselte Länge ist 16 weniger als die verschlüsselte Länge.
Siehe den Payload-Abschnitt unten für Format und Anforderungen.

KDF
```

.. raw:: html

  {% highlight lang='text' %}
Siehe AEAD-Abschnitt unten.

  // AEAD-Parameter für bestehenden Sitzung-Payload
  k = Der 32-Byte Session-Schlüssel, der mit diesem Session-Tag assoziiert ist
  n = Die Nachrichtenummer N in der aktuellen Kette, wie sie aus dem zugehörigen Session-Tag abgerufen wird.
  ad = Das Session-Tag, 8 Bytes
  ciphertext = ENCRYPT(k, n, payload, ad)
{% endhighlight %}

### 2) ECIES-X25519

Format: 32-Byte öffentliche und private Schlüssel, little-endian.

Rechtfertigung: Wird in [NTCP2]_.

### 2a) Elligator2

In standardmäßigen Noise-Handshakes beginnen die anfänglichen Handshake-Nachrichten in jeder Richtung mit
ephemeren Schlüsseln, die Klartext übertragen werden.
Da gültige X25519-Schlüssel von Zufall zu unterscheiden sind, könnte ein Man-in-the-Middle den Unterschied zwischen diesen Nachrichten machen
und bestehenden Sitzungsnachrichten erkennen, die mit zufälligen Session-Tags beginnen.
In [NTCP2]_ ([Prop111]_) haben wir eine mit geringem Aufwand XOR-Funktion verwendet, die den out-of-band Static-Schlüssel benutzt, um
den Schlüssel zu verschleiern.
Doch da das Bedrohungsmodell hier anders ist; wollen wir keiner MitM die Möglichkeit geben
irgendeine Methode zu verwenden, um das Ziel des Verkehrs zu bestätigen oder um zu unterscheiden,
ob die anfänglichen Handshake-Nachrichten von bestehenden Sitzungsnachrichten kommen.

Daher wird [Elligator2]_ verwendet, um die ephemeren Schlüssel in den New Session und New Session Reply Nachrichten
so zu transformieren, dass sie von einheitlichen Zufallstrings nicht zu unterscheiden sind.

Format
``````

32-Byte öffentliche und private Schlüssel.
Kodierte Schlüssel sind little endian.

Wie in [Elligator2]_ definiert, sind die kodierten Schlüssel von 254 Zufallsbits nicht zu unterscheiden.
Wir benötigen 256 Zufallsbits (32 Bytes). Daher sind die Kodierung und Dekodierung definiert wie folgt:

Kodierung:

.. raw:: html

  {% highlight lang='text' %}
ENCODE_ELG2() Definition

  // Kodieren wie in der Elligator2-Spezifikation definiert
  encodedKey = kodieren(pubkey)
  // XOR mit 2 zufälligen Bits zur MSB
  randomByte = CSRNG(1)
  encodedKey[31] |= (randomByte & 0xc0)
{% endhighlight %}

Dekodierung:

.. raw:: html

  {% highlight lang='text' %}
DECODE_ELG2() Definition

  // Entmaskieren von 2 zufälligen Bits aus der MSB
  encodedKey[31] &= 0x3f
  // Kodieren wie in der Elligator2-Spezifikation definiert
  pubkey = dekodieren(encodedKey)
{% endhighlight %}

Rechtfertigung
``````````````

Erforderlich, um zu verhindern, dass OBEP und IBGW den Verkehr klassifizieren.

Hinweise
````````

Elligator2 verdoppelt die durchschnittliche Generierungszeit des Schlüssels, da die Hälfte der privaten Schlüssel
zu öffentlichen Schlüsseln führen, die für die Kodierung mit Elligator2 ungeeignet sind.
Darüber hinaus ist die Generierungszeit des Schlüssels unbounded mit einer exponentiellen Verteilung,
da der Generator muss nach abgelehnten Schlüsselpaaren weiter versuchen.

Dieser Overhead kann verwaltet werden, indem Schlüsselgenerierung im Voraus durchgeführt wird,
in einem separaten Thread, um einen Pool geeigneter Schlüssel zu pflegen.

Der Generator führt die Funktion ENCODE_ELG2() aus, um Eignung zu bestimmen.
Der Generator sollte daher das Ergebnis der ENCODE_ELG2()
speichern, damit es nicht erneut berechnet werden muss.

Zusätzlich können die ungeeigneten Schlüssel dem Pool von Schlüsseln
hinzugefügt werden, die für [NTCP2]_ verwendet werden, wo Elligator2 nicht verwendet wird.
Die Sicherheitsprobleme die damit verbunden sind, sind TBD.

### 3) AEAD (ChaChaPoly)

AEAD mit ChaCha20 und Poly1305, identisch mit in [NTCP2]_.
Dies entspricht [RFC-7539]_, das auch
ähnlich in TLS [RFC-7905]_ verwendet wird.

Neue Sitzungs- und neue Sitzungsantwort-Eingaben
````````````````````````````````````````````````````````

Eingaben in die Verschlüsselungs-/Entschlüsselungsfunktionen
für einen AEAD-Block in einer neuen Sitzung Nachricht:

.. raw:: html

  {% highlight lang='dataspec' %}
k :: 32 Byte Chiffre-Schlüssel
       Siehe New Session und New Session Reply KDFs oben.

  n :: Zählerbasiertes Nonce, 12 Bytes.
       n = 0

  ad :: Assoziertes Daten, 32 Bytes.
        Der SHA256-Hash der vorherigen Daten aus mixHash()

  data :: Klartext-Daten, 0 oder mehr Bytes

{% endhighlight %}

Bestehende Sitzungseingaben
```````````````````````````

Eingaben in die Verschlüsselungs-/Entschlüsselungsfunktionen
für einen AEAD-Block in einer bestehenden Sitzung-Nachricht:

.. raw:: html

  {% highlight lang='dataspec' %}
k :: 32 Byte Session-Schlüssel
       Wie beim zugehörigen Sitzungstag nachgeschlagen.

  n :: Zählerbasiertes Nonce, 12 Bytes.
       Beginnt bei 0 und wird für jede Nachricht beim Senden inkrementiert.
       Für den Empfänger, der Wert
       wie beim zugehörigen Sitzungstag nachgeschlagen.
       Erste vier Bytes sind immer null.
       Letzte acht Bytes sind die Nachrichtenummer (n), little-endian kodiert.
       Maximalwert ist 65535.
       Sitzung muss geratscht werden, wenn N diesen Wert erreicht.
       Höhere Werte dürfen niemals verwendet werden.

  ad :: Assoziierte Daten
        Das Sitzungstag

  data :: Klartext-Daten, 0 oder mehr Bytes
{% endhighlight %}

Verschlüsseltes Format
``````````````````````

Ausgabe der Verschlüssungsfunktion, Eingabe in die Entschlüsselungsfunktion:

.. raw:: html

  {% highlight lang='dataspec' %}
+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |       ChaCha20 Verschlüsselte Daten    |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +              (MAC)                    +
  |             16 Bytes                  |
  +----+----+----+----+----+----+----+----+

  Verschlüsselte Daten :: Gleich groß wie Klartext-Daten, 0 - 65519 Bytes

  MAC :: Poly1305-Nachrichtenauthentifizierungscode, 16 Bytes

{% endhighlight %}

Hinweise
````````

- Da ChaCha20 ein Stream-Chiffre ist, müssen Klartexte nicht gepadded werden.
  Zusätzliche Keystream-Bytes werden verworfen.

- Der Schlüssel für den Chiffre (256 Bits) wird mit der SHA256-KDF vereinbart.
  Die Details der KDF für jede Nachricht befinden sich in den separaten Abschnitten unten.

- ChaChaPoly-Rahmen sind von bekannter Größe, da sie im I2NP-Datensatz eingekapselt sind.

- Für alle Nachrichten,
  Padding ist innerhalb der authentifizierten
  Datenaufzeichnung.

AEAD-Fehlerbehandlung
```````````````````````````

Alle empfangenen Daten, die die AEAD-Verifizierung nicht bestehen, müssen verworfen werden.
Es wird keine Antwort zurückgegeben.

Justification
``````````````

In [NTCP2]_ verwendet.

### 4) Ratschenschlüssel

Wir verwenden immer noch Session-Tags wie zuvor, aber wir verwenden Ratschenschlüssel, um sie zu generieren.
Session-Tags hatten auch eine Option zum Neuschlüsseln, die wir nie implementiert haben.
Es ist also wie eine doppelte Ratschenschlüssel, aber wir haben die zweite nie gemacht.

Wir definieren hier etwas, das ähnlich wie Signals Double Ratchet ist.
Die Session-Tags werden deterministisch und identisch auf
der Empfänger- und Senderseite generiert.

Durch die Verwendung eines symmetrischen Schlüssel-/Tag-Ratschenschlüssels eliminieren wir den Speicherverbrauch, um Session-Tags auf der Senderseite zu speichern.
Wir eliminieren auch den Bandbreitenverbrauch des Sendens von Tag-Sets.
Der Speicherverbrauch auf der Empfängerseite ist immer noch erheblich, aber wir können ihn weiter reduzieren,
da wir das Session-Tag von 32 Bytes auf 8 Bytes verkleinern werden.

Wir verschlüsseln den Header nicht optional, wie es in Signal spezifiziert ist,
wir verwenden Session-Tags stattdessen.

Durch die Verwendung eines DH-Ratschenschlüssels erreichen wir vorwärts Geheimnis, das nie im ElGamal/AES+SessionTags implementiert wurde.

Hinweis: Der New Session einmalige öffentliche Schlüssel ist kein Teil des Ratschenschlüssels, seine einzige Funktion
ist es, Alices ersten DH-Ratschenschlüssel zu verschlüsseln.

Nachrichtennummern
``````````````````````````

Der Double Ratchet behandelt verlorene oder aus der Ordnung geratene Nachrichten, indem er in jedem Nachrichtenheader
ein Tag enthält. Der Empfänger sucht den Index des Tags, dies ist die Nachrichtenummer N.
Wenn die Nachricht einen Nachrichtenblock mit einer PN enthält,
kann der Empfänger alle Tags höher als dieser Wert aus dem vorherigen Tag-Set löschen,
während er Tags aus dem vorherigen Tag-Set beibehält,
falls die fehlenden Nachrichten später ankommen.

Beispiel-Implementierung
`````````````````````````````````

Wir definieren die folgenden Datenstrukturen und Funktionen, um diese Ratschenschlüssel zu implementieren.

TAGSET_ENTRY
    Ein einzelner Eintrag in einem TAGSET.

    INDEX
        Ein ganzer Index, beginnend bei 0

    SESSION_TAG
        Ein Identifier, der auf dem Draht gesendet wird, 8 Bytes

    SESSION_KEY
        Ein symmetrischer Schlüssel, der nie auf den Draht geht, 32 Bytes

TAGSET
    Eine Sammlung von TAGSET_ENTRY.

    CREATE(key, n)
        Generiert ein neues TAGSET mit initialem kryptografischen Schlüsselmaterial von 32 Bytes.
        Der zugeordnete Sitzungs-Identifier wird bereitgestellt.
        Die anfängliche Anzahl von Tags, die erstellt werden sollen, wird angegeben; dies ist in der Regel 0 oder 1
        für eine ausgehende Sitzung.
        LAST_INDEX = -1
        EXTEND(n) wird aufgerufen.

    EXTEND(n)
        Generiert n weitere TAGSET_ENTRY, indem EXTEND() n-mal aufgerufen wird.

    EXTEND()
        Generiert einen weiteren TAGSET_ENTRY, es sei denn, die maximale Anzahl von SESSION_TAGS wurde
        bereits generiert.
        Wenn LAST_INDEX größer oder gleich 65535 ist, beenden.
        ++ LAST_INDEX
        Erstellen Sie einen neuen TAGSET_ENTRY mit dem LAST_INDEX-Wert und dem berechneten SESSION_TAG.
        Ruft RATCHET_TAG() und (optional) RATCHET_KEY() auf.
        Für eingehende Sitzungen kann die Berechnung des SESSION_KEY zurückgestellt werden und im GET_SESSION_KEY() berechnet werden.

    EXPIRE()
        Entfernt Tags und Schlüssel, die zu alt sind oder wenn die TAGSET-Größe einige Limits überschreitet.

    RATCHET_TAG()
        Berechnet das nächste SESSION_TAG basierend auf dem letzten SESSION_TAG.

    RATCHET_KEY()
        Berechnet das nächste SESSION_KEY basierend auf dem letzten SESSION_KEY.

    SESSION
        Die zugeordnete Sitzung.

    CREATION_TIME
        Zeitpunkterstellung des TAGSET.

    LAST_INDEX
        Der letzte TAGSET_ENTRY-INDEX, der von EXTEND() generiert wurde.

    GET_NEXT_ENTRY()
        Nur für ausgehende Sitzungen verwendbar.
        EXTEND(1) wird aufgerufen, wenn keine verbleibenden TAGSET_ENTRY vorhanden sind.
        Wenn
