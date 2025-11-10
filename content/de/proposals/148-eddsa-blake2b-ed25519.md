---
title: "RedDSA-BLAKE2b-Ed25519"
number: "148"
author: "zzz"
created: "2019-03-12"
lastupdated: "2019-04-11"
status: "Open"
thread: "http://zzz.i2p/topics/2689"
---

## Übersicht

Dieser Vorschlag fügt einen neuen Signaturtyp hinzu, der BLAKE2b-512 mit Personalisierungsstrings und Salzen verwendet, um SHA-512 zu ersetzen. Dies wird drei Klassen von möglichen Angriffen eliminieren.

## Motivation

Während der Diskussionen und des Designs von NTCP2 (Vorschlag 111) und LS2 (Vorschlag 123) haben wir kurz verschiedene mögliche Angriffe in Betracht gezogen und wie man sie verhindern kann. Drei dieser Angriffe sind Length Extension Attacks, Cross-Protocol Attacks und Duplicate Message Identification.

Für sowohl NTCP2 als auch LS2 entschieden wir, dass diese Angriffe nicht direkt relevant für die gegenwärtigen Vorschläge waren und jede Lösung im Widerspruch zur Minimierung neuer Primitiven stand. Außerdem stellten wir fest, dass die Geschwindigkeit der Hash-Funktionen in diesen Protokollen kein bedeutender Faktor bei unseren Entscheidungen war. Daher haben wir die Lösung größtenteils auf einen separaten Vorschlag vertagt. Während wir einige Personalisierungsfunktionen in die LS2-Spezifikation aufgenommen haben, verlangten wir keine neuen Hash-Funktionen.

Viele Projekte, wie ZCash [ZCASH]_, verwenden Hash-Funktionen und Signaturalgorithmen, die auf neueren Algorithmen basieren, die nicht anfällig für die folgenden Angriffe sind.

### Length Extension Attacks

SHA-256 und SHA-512 sind anfällig für Length Extension Attacks (LEA) [LEA]_. Dies ist der Fall, wenn tatsächliche Daten signiert werden, nicht der Hash der Daten. In den meisten I2P-Protokollen (Streaming, Datagramme, NetDB und andere) werden die tatsächlichen Daten signiert. Eine Ausnahme sind SU3-Dateien, bei denen der Hash signiert wird. Eine andere Ausnahme sind signierte Datagramme für DSA (Sig-Typ 0) nur, bei denen der Hash signiert wird. Für andere signierte Datagramm-Sig-Typen werden die Daten signiert.

### Cross-Protocol Attacks

Signierte Daten in I2P-Protokollen können aufgrund fehlender Domänentrennung anfällig für Cross-Protocol Attacks (CPA) sein. Dies ermöglicht es einem Angreifer, Daten, die in einem Kontext (wie ein signiertes Datagramm) empfangen wurden, als valide, signierte Daten in einem anderen Kontext (wie Streaming oder Netzwerkdatenbank) zu präsentieren. Während es unwahrscheinlich ist, dass die signierten Daten aus einem Kontext in einem anderen Kontext als gültige Daten interpretiert werden, ist es schwierig oder unmöglich, alle Situationen sicher zu analysieren. Darüber hinaus kann in einigen Kontexten ein Angreifer möglicherweise ein Opfer dazu bringen, speziell gestaltete Daten zu signieren, die gültige Daten in einem anderen Kontext sein könnten. Auch hier ist es schwierig oder unmöglich, alle Situationen sicher zu analysieren.

### Duplicate Message Identification

I2P-Protokolle können anfällig für Duplicate Message Identification (DMI) sein. Dies könnte es einem Angreifer ermöglichen, zu identifizieren, dass zwei signierte Nachrichten denselben Inhalt haben, selbst wenn diese Nachrichten und ihre Signaturen verschlüsselt sind. Obwohl es aufgrund der in I2P verwendeten Verschlüsselungsmethoden unwahrscheinlich ist, ist es schwierig oder unmöglich, alle Situationen sicher zu analysieren. Durch die Verwendung einer Hash-Funktion, die es ermöglicht, ein zufälliges Salz hinzuzufügen, werden alle Signaturen unterschiedlich sein, selbst wenn dieselben Daten signiert werden. Während Red25519, wie in Vorschlag 123 definiert, ein zufälliges Salz zur Hash-Funktion hinzufügt, löst dies das Problem bei unverschlüsselten Lease-Sets nicht.

### Geschwindigkeit

Obwohl dies keine Hauptmotivation für diesen Vorschlag ist, ist SHA-512 relativ langsam, und schnellere Hash-Funktionen sind verfügbar.

## Ziele

- Verhinderung oben genannter Angriffe
- Minimierung der Nutzung neuer Kryptoprimitive
- Verwendung bewährter, standardmäßiger Kryptoprimitive
- Nutzung standardmäßiger Kurven
- Verwendung schnellerer Primitive, wenn verfügbar

## Design

Modifizieren Sie den bestehenden RedDSA_SHA512_Ed25519-Signaturtyp, um BLAKE2b-512 anstelle von SHA-512 zu verwenden. Fügen Sie einzigartige Personalisierungsstrings für jeden Anwendungsfall hinzu. Der neue Signaturtyp kann für sowohl verblendete als auch unverblendete Lease-Sets verwendet werden.

## Rechtfertigung

- BLAKE2b ist nicht anfällig für LEA [BLAKE2]_.
- BLAKE2b bietet eine standardisierte Möglichkeit, Personalisierungsstrings zur Domänentrennung hinzuzufügen.
- BLAKE2b bietet eine standardisierte Möglichkeit, ein zufälliges Salz hinzuzufügen, um DMI zu verhindern.
- BLAKE2b ist auf moderner Hardware schneller als SHA-256 und SHA-512 (und MD5), laut [BLAKE2]_.
- Ed25519 ist immer noch unser schnellster Signaturtyp, viel schneller als ECDSA, zumindest in Java.
- Ed25519 [ED25519-REFS]_ erfordert eine 512-Bit-kryptographische Hash-Funktion. Es spezifiziert nicht SHA-512. BLAKE2b ist genauso geeignet für die Hash-Funktion.
- BLAKE2b ist in Bibliotheken für viele Programmiersprachen weit verbreitet, wie zum Beispiel Noise.

## Spezifikation

Verwenden Sie unkeyed BLAKE2b-512 wie in [BLAKE2]_ mit Salz und Personalisierung. Alle Verwendungen von BLAKE2b-Signaturen werden einen 16-Zeichen-Personalisierungsstring verwenden.

Bei der Verwendung im RedDSA_BLAKE2b_Ed25519-Signieren ist ein zufälliges Salz erlaubt, aber nicht notwendig, da der Signaturalgorithmus 80 Bytes zufällige Daten hinzufügt (siehe Vorschlag 123). Falls gewünscht, beim Hashing der Daten zur Berechnung von r, setzen Sie ein neues 16-Byte zufälliges BLAKE2b-Salz für jede Signatur. Beim Berechnen von S setzen Sie das Salz zurück auf den Standard, nämlich alle Nullen.

Bei der Verwendung im RedDSA_BLAKE2b_Ed25519-Verifizieren verwenden Sie kein zufälliges Salz, verwenden Sie den Standard von allen Nullen.

Die Salz- und Personalisierungsfunktionen sind nicht in [RFC-7693]_ spezifiziert; verwenden Sie diese Funktionen wie in [BLAKE2]_ angegeben.

### Signaturtyp

Für RedDSA_BLAKE2b_Ed25519 ersetzen Sie die SHA-512 Hash-Funktion in RedDSA_SHA512_Ed25519 (Signaturtyp 11, wie in Vorschlag 123 definiert) durch BLAKE2b-512. Keine weiteren Änderungen.

Wir benötigen keinen Ersatz für EdDSA_SHA512_Ed25519ph (Signaturtyp 8) für su3-Dateien, da die vorgehashte Version von EdDSA nicht anfällig für LEA ist. EdDSA_SHA512_Ed25519 (Signaturtyp 7) wird für su3-Dateien nicht unterstützt.

=======================  ===========  ======  =====
        Typ              Typcode      Seit    Nutzung
=======================  ===========  ======  =====
RedDSA_BLAKE2b_Ed25519       12        TBD    Nur für Router-Identitäten, Destinations und verschlüsselte Lease-Sets; wird niemals für Router-Identitäten verwendet
=======================  ===========  ======  =====

### Allgemeine Strukturdatenlängen

Das Folgende gilt für den neuen Signaturtyp.

==================================  =============
            Datentyp                 Länge    
==================================  =============
Hash                                     64      
Privater Schlüssel                       32      
Öffentlicher Schlüssel                   32      
Signatur                                64      
==================================  =============

### Personalisierungen

Um Domänentrennung für die verschiedenen Anwendungen von Signaturen zu bieten, werden wir die BLAKE2b-Personalisierungsfunktion verwenden.

Alle Verwendungen von BLAKE2b-Signaturen werden einen 16-Zeichen-Personalisierungsstring verwenden. Alle neuen Verwendungen müssen hier der Tabelle mit einem einzigartigen Personalisierungsstring hinzugefügt werden.

Die unten genannten NTCP1 und SSU-Handschläge sind für die signierten Daten definiert, die im Handschlag selbst definiert sind. Signierte RouterInfos in DatabaseStore-Nachrichten verwenden die Netzwerk-Datenbank-Personalisierung, so als ob sie im NetDB gespeichert wären.

==================================  ==========================
         Nutzung                     16 Zeichen Personalisierung
==================================  ==========================
I2CP SessionConfig                   "I2CP_SessionConf"
NetDB-Einträge (RI, LS, LS2)         "network_database"
NTCP 1 Handshake                     "NTCP_1_handshake"
Signierte Datagramme                 "sign_datagramI2P"
Streaming                            "streaming_i2psig"
SSU Handshake                        "SSUHandshakeSign"
SU3-Dateien                          n/a, nicht unterstützt
Unit-Tests                           "test1234test5678"
==================================  ==========================

## Anmerkungen

## Probleme

- Alternative 1: Vorschlag 146;
  Bietet LEA-Resistenz
- Alternative 2: Ed25519ctx in RFC 8032;
  Bietet LEA-Resistenz und Personalisierung. Standardisiert, aber benutzt es überhaupt jemand? Siehe [RFC-8032]_ und [ED25519CTX]_.
- Ist "keyed" Hashing für uns nützlich?

## Migration

Gleich wie beim Rollout vorheriger Signaturtypen.

Wir planen, neue Router vom Typ 7 auf Typ 12 als Standard umzustellen. Wir planen, bestehende Router schließlich vom Typ 7 auf Typ 12 zu migrieren, indem wir den "Rekeying"-Prozess nutzen, der nach der Einführung von Typ 7 verwendet wurde. Wir planen, neue Destinationen vom Typ 7 auf Typ 12 als Standard umzustellen. Wir planen, neue verschlüsselte Destinationen vom Typ 11 auf Typ 13 als Standard umzustellen.

Wir werden das Blinden von Typen 7, 11 und 12 auf Typ 12 unterstützen. Wir werden das Blinden von Typ 12 auf Typ 11 nicht unterstützen.

Neue Router könnten beginnen, den neuen Sig-Typ standardmäßig zu verwenden, nachdem einige Monate vergangen sind. Neue Destinationen könnten beginnen, den neuen Sig-Typ standardmäßig zu verwenden, vielleicht ein Jahr später.

Für die minimale Routerversion 0.9.TBD müssen Router sicherstellen:

- Speichern (oder verbreiten) Sie keine RI oder LS mit dem neuen Sig-Typ zu Routern unter Version 0.9.TBD.
- Beim Überprüfen eines netdb stores lesen Sie keine RI oder LS mit dem neuen Sig-Typ von Routern unter Version 0.9.TBD.
- Router mit einem neuen Sig-Typ in ihrer RI dürfen keine Verbindung zu Routern unter Version 0.9.TBD herstellen, weder mit NTCP, NTCP2 noch SSU.
- Streaming-Verbindungen und signierte Datagramme funktionieren nicht bei Routern unter Version 0.9.TBD, aber es gibt keine Möglichkeit, dies zu wissen, daher sollte der neue Sig-Typ nicht standardmäßig für einen Zeitraum von Monaten oder Jahren nach Freigabe von 0.9.TBD verwendet werden.

## Referenzen

.. [BLAKE2]
   https://blake2.net/blake2.pdf

.. [ED25519CTX]
   https://moderncrypto.org/mail-archive/curves/2017/000925.html

.. [ED25519-REFS]
    "High-speed high-security signatures" von Daniel
    J. Bernstein, Niels Duif, Tanja Lange, Peter Schwabe, und
    Bo-Yin Yang. http://cr.yp.to/papers.html#ed25519

.. [EDDSA-FAULTS]
   https://news.ycombinator.com/item?id=15414760

.. [LEA]
   https://de.wikipedia.org/wiki/Länge_Erweiterungsangriff

.. [RFC-7693]
   https://tools.ietf.org/html/rfc7693

.. [RFC-8032]
   https://tools.ietf.org/html/rfc8032

.. [ZCASH]
   https://github.com/zcash/zips/tree/master/protocol/protocol.pdf
