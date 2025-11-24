---
title: "Neue netDB-Einträge"
number: "123"
author: "zzz, str4d, orignal"
created: "2016-01-16"
lastupdated: "2020-07-18"
status: "Offen"
thread: "http://zzz.i2p/topics/2051"
supercedes: "110, 120, 121, 122"
---

## Status

Teile dieses Vorschlags sind abgeschlossen und in 0.9.38 und 0.9.39 implementiert.
Die Common Structures, I2CP, I2NP und andere Spezifikationen
sind nun aktualisiert, um die Änderungen widerzuspiegeln, die jetzt unterstützt werden.

Die abgeschlossenen Teile unterliegen weiterhin geringfügigen Überarbeitungen.
Andere Teile dieses Vorschlags sind noch in Entwicklung
und unterliegen wesentlichen Überarbeitungen.

Service Lookup (Typen 9 und 11) haben niedrige Priorität und
sind nicht geplant und können in einen separaten Vorschlag aufgeteilt werden.


## Überblick

Dies ist eine Aktualisierung und Aggregation der folgenden 4 Vorschläge:

- 110 LS2
- 120 Meta LS2 für massives Multihoming
- 121 Verschlüsseltes LS2
- 122 Nicht authentifizierte Dienstsuche (Anycasting)

Diese Vorschläge sind größtenteils unabhängig, aber der Übersicht halber definieren und nutzen wir ein
gemeinsames Format für mehrere davon.

Die folgenden Vorschläge sind etwas verwandt:

- 140 Unsichtbares Multihoming (nicht kompatibel mit diesem Vorschlag)
- 142 Neue Kryptovorlage (für neue symmetrische Kryptografie)
- 144 ECIES-X25519-AEAD-Ratchet
- 145 ECIES-P256
- 146 Red25519
- 148 EdDSA-BLAKE2b-Ed25519
- 149 B32 für Verschlüsseltes LS2
- 150 Garlic Farm Protocol
- 151 ECDSA Blinding


## Vorschlag

Dieser Vorschlag definiert 5 neue DatabaseEntry-Typen und den Prozess für
das Speichern und Abrufen dieser aus der Netzwerkdatenbank,
sowie die Methode, sie zu signieren und diese Signaturen zu verifizieren.

### Ziele

- Abwärtskompatibel
- LS2 nutzbar mit altem Multihoming
- Keine neue Krypto oder Primitiven erforderlich für Unterstützung
- Entkopplung von Krypto und Signierung beibehalten; Unterstützung aller aktuellen und zukünftigen Versionen
- Optionale Offline-Signierschlüssel ermöglichen
- Genauigkeit von Zeitstempeln verringern, um Fingerabdrücke zu reduzieren
- Neue Krypto für Ziele ermöglichen
- Massives Multihoming ermöglichen
- Mehrere Probleme mit bestehenden verschlüsselten LS beheben
- Optionale Verschleierung zur Reduzierung der Sichtbarkeit durch Floodfills
- Verschlüsselung unterstützt sowohl Einzelschlüssel als auch mehrere widerrufbare Schlüssel
- Dienstsuche für einfachere Suche von Outproxies, DHT-Bootstrap-Anwendungen
  und andere Anwendungen
- Nichts brechen, was sich auf 32-Byte-binäre Ziel-Hashes verlässt, z.B. Bittorrent
- Flexibilität für Leasesets durch Eigenschaften hinzufügen, wie wir sie in Routerinfos haben
- Veröffentlichungstimestamp und variable Ablaufzeit im Header platzieren, damit er auch funktioniert
  wenn Inhalte verschlüsselt sind (nicht den Timestamp aus dem frühesten Lease ableiten)
- Alle neuen Typen leben im gleichen DHT-Bereich und an gleichen Stellen wie bestehende Leasesets,
  damit Benutzer von alten LS auf LS2 migrieren können,
  oder zwischen LS2, Meta und Verschlüsselt wechseln können,
  ohne das Ziel oder den Hash zu ändern.
- Ein bestehendes Ziel kann zur Verwendung von Offline-Schlüsseln konvertiert werden,
  oder zurück zu Online-Schlüsseln, ohne das Ziel oder den Hash zu ändern.


### Nicht-Ziele / Außerhalb des Geltungsbereichs

- Neuer DHT-Rotationsalgorithmus oder gemeinsame Zufallsgenerierung
- Der spezifische neue Verschlüsselungstyp und das End-to-End-Verschlüsselungsschema
  zur Verwendung dieses neuen Typs würden in einem separaten Vorschlag behandelt.
  Keine neue Krypto ist hier spezifiziert oder diskutiert.
- Neue Verschlüsselung für RIs oder Tunnelaufbau.
  Dies wäre in einem separaten Vorschlag enthalten.
- Methoden zur Verschlüsselung, Übertragung und Empfang von I2NP DLM / DSM / DSRM-Nachrichten.
  Keine Änderung.
- Wie man Meta generiert und unterstützt, einschließlich Backend-Kommunikation zwischen Routern, Management, Failover und Koordination.
  Unterstützung kann zu I2CP oder i2pcontrol oder einem neuen Protokoll hinzugefügt werden.
  Dies kann standardisiert werden oder auch nicht.
- Wie man längere Tunnel implementiert und verwaltet oder bestehende Tunnel kündigt.
  Das ist extrem schwierig, und ohne es kann man keinen vernünftigen sanften Shutdown haben.
- Änderungen am Bedrohungsmodell
- Offline-Speicherformat oder Methoden zum Speichern/Abrufen/Teilen der Daten.
- Implementierungsdetails sind hier nicht diskutiert und werden jedem Projekt selbst überlassen.



### Begründung

LS2 fügt Felder hinzu, um den Verschlüsselungstyp zu ändern und zukünftige Protokolländerungen zu ermöglichen.

Verschlüsseltes LS2 behebt mehrere Sicherheitsprobleme mit dem bestehenden verschlüsselten LS durch
asymmetrische Verschlüsselung des gesamten Lease-Sets.

Meta LS2 bietet flexibles, effizientes, effektives und großmaßstäbliches Multihoming.

Service Record und Service List bieten Anycast-Dienste wie Namenssuche
und DHT-Bootstrapping.


### NetDB-Datentypen

Die Typnummern werden in den I2NP-Datenbank-Such-/Speichermeldungen verwendet.

Die End-to-End-Spalte bezieht sich darauf, ob Abfragen/Antworten an ein Ziel in einer Garlic-Nachricht gesendet werden.


Bestehende Typen:

            NetDB-Daten               Suche Typ    Speicher Typ 
beliebig                                0           beliebig  
LS                                       1            1      
RI                                       2            0      
erkundend                                3           DSRM    

Neue Typen:

            NetDB-Daten               Suche Typ    Speicher Typ   Std. LS2 Header?   End-to-End versendet?
LS2                                      1            3             ja                  ja
Verschlüsseltes LS2                      1            5             nein                 nein
Meta LS2                                 1            7             ja                  nein
Service Record                          n/a           9             ja                  nein
Service List                             4           11             nein                 nein



Anmerkungen
`````
- Suchtypen sind derzeit Bits 3-2 in der Database Lookup Message.
  Jeder zusätzliche Typ würde die Verwendung von Bit 4 erfordern.

- Alle Speichertypen sind ungerade, da höhere Bits im Typfeld der Speicherung von alten Routern ignoriert werden.
  Wir würden lieber das Parsing als LS fehlschlagen lassen als als komprimiertes RI.

- Sollte der Typ explizit oder implizit oder weder noch in den Daten sein, die durch die Signatur abgedeckt sind?



### Such-/Speicherprozess

Typen 3, 5 und 7 können als Antwort auf eine Standard-Leaseset-Suche (Typ 1) zurückgegeben werden.
Typ 9 wird nie als Antwort auf eine Suche zurückgegeben.
Typen 11 werden als Antwort auf einen neuen Dienstsuche-Typ (Typ 11) zurückgegeben.

Nur Typ 3 kann in einer Client-zu-Client-Garlic-Nachricht gesendet werden.



### Format

Typen 3, 7 und 9 haben alle ein gemeinsames Format::

  Standard LS2-Header
  - wie unten definiert

  Typspezifischer Teil
  - wie unten in jedem Teil definiert

  Standard LS2 Signatur:
  - Länge wie durch den Signaturtyp des Signaturschlüssels impliziert

Typ 5 (Verschlüsselt) beginnt nicht mit einem Ziel und hat ein
anderes Format. Siehe unten.

Typ 11 (Service List) ist eine Aggregation mehrerer Service Records und hat ein
anderes Format. Siehe unten.


### Datenschutz-/Sicherheitsüberlegungen

Wird noch festgelegt



## Standard-LS2-Header

Typen 3, 7 und 9 verwenden den Standard-LS2-Header, unten spezifiziert:


### Format
::

  Standard LS2-Header:
  - Typ (1 Byte)
    Tatsächlich nicht in der Überschrift, sondern Teil der durch die Signatur abgedeckten Daten.
    Nehmen Sie aus dem Datenbank-Speichermeldungsfeld.
  - Ziel (387+ Bytes)
  - Veröffentlicht-Zeitstempel (4 Bytes, Big Endian, Sekunden seit der Epoche, Roll-over in 2106)
  - Ablaufen (2 Bytes, Big Endian) (Offset von Veröffentlicht-Zeitstempel in Sekunden, max. 18,2 Stunden)
  - Flags (2 Bytes)
    Bit-Reihenfolge: 15 14 ... 3 2 1 0
    Bit 0: Wenn 0, keine Offline-Schlüssel; wenn 1, Offline-Schlüssel
    Bit 1: Wenn 0, ein veröffentlichtes Standard-Leaseset.
           Wenn 1, ein unveröffentlichtes Leaseset. Sollte nicht geflutet, veröffentlicht oder
           als Antwort auf eine Abfrage gesendet werden. Wenn dieses Leaseset abläuft, nicht im NetDB nach einem neuen suchen, es sei denn, Bit 2 ist gesetzt.
    Bit 2: Wenn 0, ein veröffentlichtes Standard-Leaseset.
           Wenn 1, wird dieses unverschlüsselte Leaseset bei der Veröffentlichung verschleiert und verschlüsselt.
           Wenn dieses Leaseset abläuft, fragen Sie den verschleierten Standort im NetDB nach einem neuen.
           Wenn dieses Bit auf 1 gesetzt ist, setzen Sie auch Bit 1 auf 1.
           Ab Veröffentlichung 0.9.42.
    Bits 3-15: auf 0 setzen für Kompatibilität mit zukünftigen Anwendungen
  - Wenn die Flagge Offline-Schlüssel anzeigt, der Offline-Signaturabschnitt:
    Läuft ab Zeitstempel (4 Bytes, Big Endian, Sekunden seit der Epoche, Roll-over in 2106)
    Transiente Signaturtyp (2 Bytes, Big Endian)
    Transienter öffentlicher Signaturschlüssel (Länge wie durch Signaturtyp impliziert)
    Signatur des Ablaufzeitpunkts, des transienten Signaturtyps und des öffentlichen Schlüssels,
    durch den öffentlichen Schlüssel des Ziels,
    Länge wie durch den Signaturtyp des Ziel-Signaturschlüssels impliziert.
    Dieser Abschnitt kann und sollte offline erstellt werden.


Begründung
`````````````

- Unveröffentlicht/veröffentlicht: Zur Verwendung, wenn ein Datenbank-Speicher-Ende-zu-Ende gesendet wird,
  möchte der sendende Router möglicherweise darauf hinweisen, dass dieses Leaseset nicht
  anderen gesendet werden soll. Wir verwenden derzeit Heuristiken, um diesen Zustand aufrechtzuerhalten.

- Veröffentlicht: Ersetzt die komplexe Logik, die erforderlich ist, um die 'Version' des
  Leasesets zu bestimmen. Derzeit ist die Version das Ablaufdatum des zuletzt ablaufenden Lease
  und ein veröffentlichender Router muss dieses Ablaufdatum um mindestens 1 ms erhöhen, wenn
  er ein Leaseset veröffentlicht, das nur ein älteres Lease entfernt.

- Ablaufen: Ermöglicht es einem NetDB-Eintrag, früher abzulaufen als das
  zuletzt ablaufende Leaseset. Für LS2, wo Leasesets mit einer maximalen Laufzeit von 11 Minuten
  verbleiben sollen, möglicherweise nicht nützlich, aber für andere neue Typen, ist es notwendig (siehe Meta LS und Service Record unten).

- Offline-Schlüssel sind optional, um die anfängliche/erforderte Implementierungskomplexität zu reduzieren.


### Probleme

- Könnte die Zeitstempelgenauigkeit noch weiter reduzieren (10 Minuten?), müsste aber eine
  Versionsnummer hinzufügen. Das könnte Multihoming brechen, es sei denn, wir haben
  ordnungserhaltende Verschlüsselung? Wahrscheinlich können wir gar nicht ohne Zeitstempel auskommen.

- Alternative: 3-Byte-Zeitstempel (Epoche / 10 Minuten), 1-Byte-Version, 2-Byte-Ablaufen

- Ist der Typ explizit oder implizit in den Daten / der Signatur? "Domain"-Konstanten für die Signatur?


Anmerkungen
`````

- Router sollten ein LS nicht mehr als einmal pro Sekunde veröffentlichen.
  Wenn sie das tun, müssen sie den veröffentlichten Zeitstempel künstlich um 1 über
  dem zuvor veröffentlichten LS erhöhen.

- Router-Implementierungen könnten die transienten Schlüssel und die Signatur zwischenspeichern, um das Verifizieren jedes Mal zu vermeiden. Insbesondere Floodfills und Router an beiden Enden von lang lebenden Verbindungen könnten davon profitieren.

- Offline-Schlüssel und Signatur sind nur für Langzeitziele geeignet, d.h. für Server, nicht für Clients.



## Neue DatabaseEntry-Typen


### LeaseSet 2

Änderungen vom bestehenden Leaseset:

- Hinzufügen von veröffentlichtem Zeitstempel, Ablaufzeitstempel, Flags und Eigenschaften
- Verschlüsselungstyp hinzufügen
- Widerrufsschlüssel entfernen

Abfragen mit
    Standard-LS-Flag (1)
Speichern mit
    Standard-LS2-Typ (3)
Speichern bei
    Hash des Ziels
    Dieser Hash wird dann verwendet, um den täglichen "Routing-Schlüssel" zu generieren, wie bei LS1
Typische Laufzeit
    10 Minuten, wie in einem regulären LS.
Veröffentlicht von
    Ziel

Format
``````
::

  Standard-LS2-Header wie oben spezifiziert

  Standard LS2 Typspezifischer Teil
  - Eigenschaften (Mapping wie in der Spezifikation der gemeinsamen Strukturen angegeben, 2 Null-Bytes, wenn keine vorhanden sind)
  - Anzahl der zu folgenden Schlüsselteile (1 Byte, max. TBD)
  - Schlüsselteile:
    - Verschlüsselungstyp (2 Bytes, Big Endian)
    - Verschlüsselungsschlüssellänge (2 Bytes, Big Endian)
      Dies ist explizit, sodass Floodfills ein LS2 mit unbekannten Verschlüsselungstypen analysieren können.
    - Verschlüsselungsschlüssel (angegebene Byteanzahl)
  - Anzahl der lease2s (1 Byte)
  - Lease2s (jeweils 40 Bytes)
    Dies sind Leases, jedoch mit einem 4-Byte statt einem 8-Byte-Ablauf
    Sekunden seit der Epoche (rollt im Jahr 2106 über)

  Standard LS2 Signatur:
  - Signatur
    Wenn die Flagge Offline-Schlüssel anzeigt, wird dies vom transienten Pubkey signiert,
    andernfalls vom Ziel-Pubkey
    Länge wie durch den Signaturtyp des Signaturschlüssels impliziert
    Die Signatur umfasst alles oben genannte.




Begründung
`````````````

- Eigenschaften: Zukünftige Erweiterung und Flexibilität.
  An erster Stelle platziert, falls nötig zum Parsen der verbleibenden Daten.

- Mehrere Verschlüsselungstyp-/Öffentlicher Schlüssel-Paare sind
  zur Erleichterung des Übergangs zu neuen Verschlüsselungstypen.
  Der andere Weg wäre es, mehrere Leasesets zu veröffentlichen, möglicherweise unter Verwendung derselben Tunnel,
  wie wir es jetzt für DSA- und EdDSA-Ziele tun.
  Die Identifikation des eingehenden Verschlüsselungstyps auf einem Tunnel
  kann mit dem bestehenden Sitzungs-Tag-Mechanismus durchgeführt werden,
  und/oder mit Versuch-Entschlüsselung mit jedem Schlüssel. Längen der eingehenden
  Nachrichten könnten auch einen Hinweis bieten.

Diskussion
``````````

Dieser Vorschlag verwendet weiterhin den öffentlichen Schlüssel im Leaseset für den
Ende-zu-Ende-Verschlüsselungsschlüssel und lässt das öffentliche Schlüsselfeld im
Ziel unbenutzt, wie es derzeit ist. Der Verschlüsselungstyp wird nicht im Zertifikat des Zielschlüssels angegeben, er bleibt 0.

Eine abgelehnte Alternative wäre es gewesen, den Verschlüsselungstyp im Zertifikat des Zielschlüssels anzugeben,
den öffentlichen Schlüssel im Ziel zu verwenden und den öffentlichen Schlüssel
im Leaseset nicht zu verwenden. Wir planen nicht, dies zu tun.

Vorteile von LS2:

- Der Standort des tatsächlichen öffentlichen Schlüssels ändert sich nicht.
- Verschlüsselungstyp oder öffentlicher Schlüssel können geändert werden, ohne das Ziel zu ändern.
- Entfernt ungenutztes Widerrufsfeld
- Grundlegende Kompatibilität mit anderen DatabaseEntry-Typen in diesem Vorschlag
- Erlaubt mehrere Verschlüsselungstypen

Nachteile von LS2:

- Standort des öffentlichen Schlüssels und Verschlüsselungstyp unterscheidet sich von RouterInfo
- Beibehaltung ungenutzter öffentlicher Schlüssel im Leaseset
- Erfordert Implementierung im gesamten Netzwerk; in der Alternative könnten experimentelle
  Verschlüsselungstypen verwendet werden, wenn sie von Floodfills zugelassen werden
  (siehe jedoch verwandte Vorschläge 136 und 137 zur Unterstützung experimenteller Signaturtypen).
  Der alternative Vorschlag könnte einfacher zu implementieren und für experimentelle Verschlüsselungstypen
  zu testen sein.


Neue Verschlüsselungsfragen
````````````````````
Einige davon liegen außerhalb des Geltungsbereichs dieses Vorschlags,
aber wir notieren hier vorläufige Anmerkungen, da es noch
keinen separaten Verschlüsselungsvorschlag gibt.
Siehe auch die ECIES-Vorschläge 144 und 145.

- Der Verschlüsselungstyp repräsentiert die Kombination von
  Kurve, Schlüssellänge und Ende-zu-Ende-Schema,
  einschließlich KDF und MAC, falls vorhanden.

- Wir haben ein Schlüssellängenfeld hinzugefügt, damit das LS2
  analysierbar und überprüfbar ist, selbst für unbekannte Verschlüsselungstypen.

- Der erste neue Verschlüsselungstyp, der vorgeschlagen wird, ist wahrscheinlich ECIES/X25519. Wie er
  Ende-zu-Ende verwendet wird (entweder eine leicht modifizierte Version von ElGamal/AES+SessionTag
  oder etwas komplett Neues, z.B. ChaCha/Poly) wird
  in einem oder mehreren separaten Vorschlägen spezifiziert.
  Siehe auch die ECIES-Vorschläge 144 und 145.


Anmerkungen
`````
- 8-Byte-Ablauf in Leases auf 4 Bytes geändert.

- Sollte es jemals eine Implementierung für Widerruf geben, könnten wir es mit einem Ablauf-Feld von null,
  oder null Leases, oder beidem machen. Kein separater Widerrufsschlüssel nötig.

- Verschlüsselungsschlüssel sind in der Reihenfolge der Server-Präferenz, die am meisten bevorzugt werden zuerst.
  Standard-Client-Verhalten ist die Auswahl des ersten Schlüssels mit
  einem unterstützten Verschlüsselungstyp. Clients können andere Auswahlalgorithmen basierend
  auf Verschlüsselungsunterstützung, relativer Leistung und anderen Faktoren verwenden.


### Verschlüsseltes LS2

Ziele:

- Verschleierung hinzufügen
- Mehrfach-Signaturtypen ermöglichen
- Keine neuen Krypto-Primitiven erfordern
- Optional für jeden Empfänger verschlüsseln, widerrufbar
- Unterstützung für Verschlüsselung nur für Standard-LS2 und Meta-LS2

Verschlüsseltes LS2 wird niemals in einer Ende-zu-Ende-Garlic-Nachricht gesendet.
Verwenden Sie das Standard-LS2 wie oben.


Änderungen von bestehendem verschlüsseltem Leaseset:

- Alles verschlüsseln für Sicherheit
- Sicher verschlüsseln, nicht nur mit AES.
- An jeden Empfänger verschlüsseln

Abfragen mit
    Standard-LS-Flag (1)
Speichern mit
    Verschlüsselter LS2-Typ (5)
Speichern bei
    Hash des verschleierten Signaturtyps und des verschleierten öffentlichen Schlüssels
    Zwei-Byte-Signaturtyp (big endian, z.B. 0x000b) || verschleierter öffentlicher Schlüssel
    Dieser Hash wird dann verwendet, um den täglichen "Routing-Schlüssel" zu generieren, wie bei LS1
Typische Laufzeit
    10 Minuten, wie in einem regulären LS, oder Stunden, wie in einem Meta-LS.
Veröffentlicht von
    Ziel


Definitionen
```````````
Wir definieren die folgenden Funktionen, die den kryptografischen Bausteinen entsprechen, die für verschlüsseltes LS2 verwendet werden:

CSRNG(n)
    n-Byte-Ausgabe von einem kryptografisch sicheren Zufallszahlengenerator.

    Neben der Anforderung, dass CSRNG kryptografisch sicher ist (und somit
    geeignet für die Generierung von Schlüsselmaterial), MUSS es sicher sein, dass
    einige n-Byte-Ausgabe als Schlüsselmaterial verwendet wird, wenn die Byte-Sequenzen unmittelbar
    davor und danach im Netzwerk offen gelegt werden (wie in einem Salt oder verschlüsseltem
    Padding). Implementierungen, die sich auf eine möglicherweise unzuverlässige Quelle verlassen, sollten irgendwelche ausgegebenen Daten, die im Netzwerk offen gelegt werden, hashen. See [PRNG references](http://projectbullrun.org/dual-ec/ext-rand.html) and [Tor dev discussion](https://lists.torproject.org/pipermail/tor-dev/2015-November/009954.html).

H(p, d)
    SHA-256 Hash-Funktion, die einen Personaliserungs-String p und Daten d aufnimmt und eine
    Ausgabe von 32 Byte erzeugt.

    Verwende SHA-256 wie folgt::

        H(p, d) := SHA-256(p || d)

STREAM
    Der ChaCha20 Stromchiffre wie in [RFC 7539 Section 2.4](https://tools.ietf.org/html/rfc7539#section-2.4) beschrieben, mit dem Anfangszähler
    auf 1 gesetzt. S_KEY_LEN = 32 und S_IV_LEN = 12.

    ENCRYPT(k, iv, plaintext)
        Verschlüsselt den Klartext unter Verwendung des Chiffreschlüssels k und der Nonce iv, die
        für den Schlüssel k eindeutig sein MUSS. Gibt einen Chiffretext zurück, der
        die gleiche Größe wie der Klartext hat.

        Der gesamte Chiffretext muss ununterscheidbar von Zufall sein, wenn der Schlüssel geheim ist.

    DECRYPT(k, iv, ciphertext)
        Entschlüsselt den Chiffretext unter Verwendung des Chiffreschlüssels k und der Nonce iv. Gibt den Klartext zurück.


SIG
    Das RedDSA-Signaturschema (entspricht Signaturtyp 11) mit Schlüsselverschleierung.
    Es hat die folgenden Funktionen:

    DERIVE_PUBLIC(privkey)
        Gibt den öffentlichen Schlüssel zurück, der dem angegebenen privaten Schlüssel entspricht.

    SIGN(privkey, m)
        Gibt eine Signatur des privaten Schlüssels privkey über die gegebene Nachricht m zurück.

    VERIFY(pubkey, m, sig)
        Verifiziert die Signatur sig gegen den öffentlichen Schlüssel pubkey und die Nachricht m. Gibt
        true zurück, wenn die Signatur gültig ist, andernfalls false.

    Es muss auch die folgenden Schlüsselverschleierungsoperationen unterstützen:

    GENERATE_ALPHA(data, secret)
        Generiere Alpha für diejenigen, die die Daten und ein optionales Geheimnis kennen.
        Das Ergebnis muss identisch mit den privaten Schlüsseln verteilt sein.

    BLIND_PRIVKEY(privkey, alpha)
        Verschleiert einen privaten Schlüssel mithilfe eines geheimen Alpha.

    BLIND_PUBKEY(pubkey, alpha)
        Verschleiert einen öffentlichen Schlüssel mithilfe eines geheimen Alpha.
        Für ein gegebenes Schlüsselpaar (privkey, pubkey) gilt die folgende Beziehung::

            BLIND_PUBKEY(pubkey, alpha) ==
            DERIVE_PUBLIC(BLIND_PRIVKEY(privkey, alpha))

DH
    X25519 öffentliches Schlüsselaustauschsystem. Private Schlüssel von 32 Byte, öffentliche Schlüssel von 32
    Byte, erzeugt Ausgaben von 32 Byte. Es hat die folgenden
    Funktionen:

    GENERATE_PRIVATE()
        Generiert einen neuen privaten Schlüssel.

    DERIVE_PUBLIC(privkey)
        Gibt den öffentlichen Schlüssel zurück, der dem angegebenen privaten Schlüssel entspricht.

    DH(privkey, pubkey)
        Generiert ein gemeinsames Geheimnis aus den angegebenen privaten und öffentlichen Schlüsseln.

HKDF(salt, ikm, info, n)
    Ein kryptografischer Schlüsselableitungsalgorithmus, der einige Eingabeschlüsselmaterial ikm aufnimmt (das
    gute Entropie haben muss, aber nicht zwingend ein gleichmäßig zufälliger String sein muss), ein Salt
    von 32 Byte Länge und einen kontextspezifischen 'Info'-Wert und ein Ausgabe von n Bytes produziert, das
    geeignet ist, als Schlüsselmaterial verwendet zu werden.

    Verwende HKDF wie in [RFC 5869](https://tools.ietf.org/html/rfc5869) beschrieben, unter Verwendung der HMAC-Hash-Funktion SHA-256
    wie in [RFC 2104](https://tools.ietf.org/html/rfc2104). Das bedeutet, dass SALT_LEN maximal 32 Byte beträgt.




Format
``````
Das verschlüsselte LS2-Format besteht aus drei verschachtelten Schichten:

- Eine äußere Schicht, die die notwendigen Klartextinformationen für die Speicherung und das Abrufen enthält.
- Eine mittlere Schicht, die die Client-Authentifizierung behandelt.
- Eine innere Schicht, die die tatsächlichen LS2-Daten enthält.

Das Gesamtformat sieht folgendermaßen aus::

    Schicht 0-Daten + Enc(Schicht 1-Daten + Enc(Schicht 2-Daten)) + Signatur

Beachten Sie, dass verschlüsseltes LS2 verschleiert ist. Das Ziel ist nicht im Header.
DHT-Speicherort ist SHA-256(Signaturtyp || verschleierter öffentlicher Schlüssel) und rotiert täglich.

Verwendet NICHT den oben spezifizierten Standard-LS2-Header.

#### Schicht 0 (äußere)
Typ
    1 Byte

    Tatsächlich nicht in der Überschrift, sondern Teil der durch die Signatur abgedeckten Daten.
    Nehmen Sie aus dem Datenbank-Speichermeldungsfeld.

Verschleierter öffentlicher Schlüssel Signaturtyp
    2 Bytes, Big Endian
    Dies wird immer Typ 11 sein, was einen Red25519 verschleierten Schlüssel identifiziert.

Verschleierter öffentlicher Schlüssel
    Länge wie durch Signaturtyp impliziert

Veröffentlicht-Zeitstempel
    4 Bytes, Big Endian

    Sekunden seit der Epoche, rollt über in 2106

Ablaufen
    2 Bytes, Big Endian

    Offset vom Veröffentlicht-Zeitstempel in Sekunden, max. 18,2 Stunden

Flags
    2 Bytes

    Bit-Reihenfolge: 15 14 ... 3 2 1 0

    Bit 0: Wenn 0, keine Offline-Schlüssel; wenn 1, Offline-Schlüssel

    Andere Bits: auf 0 setzen für Kompatibilität mit zukünftigen Anwendungen

Transiente Schlüsseldaten
    Vorhanden, wenn Flagge Offline-Schlüssel anzeigt

    Ablaufen-Zeitstempel
        4 Bytes, Big Endian

        Sekunden seit der Epoche, rollt über in 2106

    Transienter Signaturtyp
        2 Bytes, Big Endian

    Transienter öffentlicher Signaturschlüssel
        Länge wie durch Signaturtyp impliziert

    Signatur
        Länge wie durch verschleierten öffentlichen Signaturtyp impliziert

        Über Ablauf-Zeitstempel, transienten Signaturtyp und öffentlichen Schlüssel.

lenOuterCiphertext
    2 Bytes, Big Endian

outerCiphertext
    lenOuterCiphertext Bytes

    Verschlüsselte Schicht 1-Daten. Siehe unten für die Ableitungs- und Verschlüsselungsalgorithmen.

Signatur
    Länge wie durch den Signaturtyp des verwendeten Signaturschlüssels impliziert

    Die Signatur ist über alles oben genannte.

    Wenn das Flagge Offline-Schlüssel anzeigt, wird die Signatur mit dem transienten
    öffentlichen Schlüssel verifiziert. Andernfalls wird die Signatur mit dem verschleierten öffentlichen Schlüssel verifiziert.


#### Schicht 1 (mittlere)
Flags
    1 Byte
    
    Bit-Reihenfolge: 76543210

    Bit 0: 0 für jeden, 1 für jeden Client, Auth-Abschnitt folgt

    Bits 3-1: Authentifizierungsschema, nur wenn Bit 0 auf 1 gesetzt ist für jeden Client, andernfalls 000
              000: DH-Client-Authentifizierung (oder keine Client-Authentifizierung)
              001: PSK-Client-Authentifizierung

    Bits 7-4: Ungenutzt, setze auf 0 für zukünftige Kompatibilität

DH-Client-Auth-Daten
    Vorhanden, wenn Flagge Bit 0 auf 1 gesetzt ist und Flagge Bits 3-1 auf 000 gesetzt sind.

    ephemeralPublicKey
        32 Bytes

    clients
        2 Bytes, Big Endian

        Anzahl der folgenden authClient-Einträge, jeweils 40 Bytes

    authClient
        Autorisierungsdaten für einen einzelnen Client.
        Siehe unten für den Per-Client-Autorisierungsalgorithmus.

        clientID_i
            8 Bytes

        clientCookie_i
            32 Bytes

PSK-Client-Auth-Daten
    Vorhanden, wenn Flagge Bit 0 auf 1 gesetzt ist und Flagge Bits 3-1 auf 001 gesetzt sind.

    authSalt
        32 Bytes

    clients
        2 Bytes, Big Endian

        Anzahl der folgenden authClient-Einträge, jeweils 40 Bytes

    authClient
        Autorisierungsdaten für einen einzelnen Client.
        Siehe unten für den Per-Client-Autorisierungsalgorithmus.

        clientID_i
            8 Bytes

        clientCookie_i
            32 Bytes


innerCiphertext
    Länge impliziert durch lenOuterCiphertext (was auch immer an Daten übrig bleibt)

    Verschlüsselte Schicht 2-Daten. Siehe unten für die Ableitungs- und Verschlüsselungsalgorithmen.


#### Schicht 2 (inner)
Typ
    1 Byte

    Entweder 3 (LS2) oder 7 (Meta LS2)

Daten
    LeaseSet2-Daten für den gegebenen Typ.

    Enthält den Header und die Signatur.


Schlüsseldaten für die Verschleierung
`````````````````````````````````````

Wir verwenden das folgende Schema für die Verschleierung von Schlüsseln
basierend auf Ed25519 und [ZCash RedDSA](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf).
Die Red25519-Signaturen sind über die Ed25519-Kurve unter Verwendung von SHA-512 für den Hash.

Wir verwenden nicht [Tor's rend-spec-v3.txt appendix A.2](https://spec.torproject.org/rend-spec-v3),
der ähnliche Designziele hat, weil seine verschleierten öffentlichen Schlüssel
nicht auf der Primordnser-Untergruppe sein können, mit unbekannten Sicherheitsimplikationen.


#### Ziele

- Der öffentliche Signierungsschlüssel im nicht verschleierten Ziel muss
  Ed25519 (Typ 7) oder Red25519 (Typ 11) sein;
  keine anderen Signaturtypen werden unterstützt
- Wenn der öffentliche Signierungsschlüssel offline ist, muss auch der transiente öffentliche Signierungsschlüssel Ed25519 sein.
- Die Verschleierung ist rechentechnisch einfach
- Verwendung bestehender kryptografischer Primitiven
- Verschleierte öffentliche Schlüssel können nicht enthüllt werden
- Verschleierte öffentliche Schlüssel müssen auf der Ed25519-Kurve und der Primordnser-Untergruppe sein
- Zum Ableiten des verschleierten öffentlichen Schlüssels muss der Signierungsschlüssel des Ziels bekannt sein
  (vollständiges Ziel nicht erforderlich)
- Optional zusätzliche Geheimnisse bereitstellen, die zur Ableitung des verschleierten öffentlichen Schlüssels erforderlich sind.


#### Sicherheit

Die Sicherheit eines Verschleierungsschemas erfordert, dass die
Verteilung von Alpha dieselbe ist wie die unverschleierten privaten Schlüssel.
Wenn wir jedoch einen Ed25519 privaten Schlüssel (Typ 7)
auf einen Red25519 privaten Schlüssel (Typ 11) verschleiern, ist die Verteilung anders.
Um die Anforderungen des [Zcash section 4.1.6.1](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf)
zu erfüllen, sollte Red25519 (Typ 11) auch für unverschleierte Schlüssel verwendet werden, damit
"die Kombination aus einem neu randomisierten öffentlichen Schlüssel und Signaturen unter diesem Schlüssel den Schlüssel, aus dem er neu randomisiert wurde, nicht offenbart."
Wir erlauben Typ 7 für bestehende Ziele, empfehlen aber
Typ 11 für neue Ziele, die verschlüsselt werden sollen.



#### Definitionen

B
    Der Ed25519-Basispunkt (Generator) 2^255 - 19 wie in [Ed25519](http://cr.yp.to/papers.html#ed25519)

L
    Die Ed25519-Ordnungsgröße 2^252 + 27742317777372353535851937790883648493
    wie in [Ed25519](http://cr.yp.to/papers.html#ed25519)

DERIVE_PUBLIC(a)
    Konvertiere einen privaten Schlüssel zu einem öffentlichen, wie in Ed25519 (mit G multiplizieren)

alpha
    Eine 32-Byte-Zufallszahl, die denen bekannt ist, die das Ziel kennen.

GENERATE_ALPHA(destination, date, secret)
    Generiere Alpha für das aktuelle Datum für diejenigen, die das Ziel und das Geheimnis kennen.
    Das Ergebnis muss identisch mit den Ed25519 privaten Schlüsseln verteilt sein.

a
    Der unverschleierte 32-Byte-EdDSA oder RedDSA Signierungsschlüssel, der zum Signieren des Ziels verwendet wird

A
    Der unverschleierte 32-Byte-EdDSA oder RedDSA Signierungsköffentlichen Schlüssel im Ziel,
    = DERIVE_PUBLIC(a), wie in Ed25519

a'
    Der verschleierte 32-Byte-EdDSA Signierungsschlüssel, der zum Signieren des verschlüsselten Leasesets verwendet wird
    Dies ist ein gültiger EdDSA privater Schlüssel.

A'
    Der verschleierte 32-Byte-EdDSA Signierungsköffentlichen Schlüssel im Ziel,
    kann mit DERIVE_PUBLIC(a') generiert werden, oder von A und Alpha.
    Dies ist ein gültiger EdDSA öffentlicher Schlüssel, auf der Kurve und in der Primordnser-Untergruppe.

LEOS2IP(x)
    Drehe die Reihenfolge der Eingabebytes in Little-Endian um

H*(x)
    32 Bytes = (LEOS2IP(SHA512(x))) mod B, gleich wie in Ed25519 Hash- und Reduktionsvorgang


#### Verschleierung Berechnungen

Ein neues geheimes Alpha und verschleierte Schlüssel müssen jeden Tag (UTC) generiert werden.
Das geheime Alpha und die verschleierten Schlüssel werden wie folgt berechnet.

GENERATE_ALPHA(destination, date, secret), für alle Parteien:

  ```text
// GENERATE_ALPHA(destination, date, secret)

  // secret ist optional, sonst null-Länge
  A = öffentlicher Signierungsschlüssel des Ziels
  stA = Signaturtyp von A, 2 Bytes Big Endian (0x0007 oder 0x000b)
  stA' = Signaturtyp des verschleierten öffentlichen Schlüssels A', 2 Bytes Big Endian (0x000b)
  keydata = A || stA || stA'
  datenstring = 8 Bytes ASCII YYYYMMDD vom aktuellen Datum UTC
  secret = UTF-8 codierter String
  seed = HKDF(H("I2PGenerateAlpha", keydata), datenstring || secret, "i2pblinding1", 64)
  // behandel Seed als ein 64-Byte-Little-Endian Wert
  alpha = seed mod L
```

BLIND_PRIVKEY(), für den Eigentümer, der das Leaseset veröffentlicht:

  ```text
// BLIND_PRIVKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  // Wenn für einen Ed25519 privaten Schlüssel (Typ 7)
  seed = private Signierungsschlüssel des Ziels
  a = linke Hälfte von SHA512(seed) und wie üblich für Ed25519 geclamped
  // sonst, für einen Red25519 privaten Schlüssel (Typ 11)
  a = private Signierungsschlüssel des Ziels
  // Addition durch Skalararithmetik
  verschleierter privater Signierungsschlüssel = a' = BLIND_PRIVKEY(a, alpha) = (a + alpha) mod L
  verschleierter öffentlicher Signierungsschlüssel = A' = DERIVE_PUBLIC(a')
```

BLIND_PUBKEY(), für die Clients, die das Leaseset abrufen:

  ```text
// BLIND_PUBKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  A = öffentlicher Signierungsschlüssel des Ziels
  // Addition durch Gruppenelemente (Punkte auf der Kurve)
  verschleierter öffentlicher Schlüssel = A' = BLIND_PUBKEY(A, alpha) = A + DERIVE_PUBLIC(alpha)
```

Beide Methoden zur Berechnung von A' ergeben dasselbe Ergebnis, wie erforderlich.



#### Signieren

Das unverschleierte Leaseset wird vom unverschleierten Ed25519 oder Red25519 privaten Signierungsschlüssel
und überprüft mit dem unverschleierten Ed25519 oder Red25519 öffentlichen Signierungsschlüssel (Signaturtypen 7 oder 11) wie gewohnt.

Wenn der öffentliche Signierungsschlüssel offline ist,
wird das unverschleierte Leaseset vom unverschleierten transienten Ed25519 oder Red25519 privaten Signierungsschlüssel signiert
und überprüft mit dem unverschleierten Ed25519 oder Red25519 transienten öffentlichen Signierungsschlüssel (Signaturtypen 7 oder 11) wie gewohnt.
Siehe unten für zusätzliche Anmerkungen zu Offline-Schlüsseln für verschlüsselte Leasesets.

Zur Unterzeichnung des verschlüsselten Leasesets verwenden wir Red25519, basierend auf [RedDSA](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf)
zum Signieren und Verifizieren mit verschleierten Schlüsseln.
Die Red25519-Signaturen sind über die Ed25519-Kurve, unter Verwendung von SHA-512 für den Hash, erstellt.

Red25519 ist identisch mit dem Standard Ed25519, außer wie unten spezifiziert.


#### Signieren/Verifizieren Berechnungen

Der äußere Teil des verschlüsselten Leasesets verwendet Red25519-Schlüssel und Signaturen.

Red25519 ist fast identisch mit Ed25519. Es gibt zwei Unterschiede:

Red25519-Private-Schlüssel werden aus Zufallszahlen generiert und dann mod L reduziert, wobei L oben definiert ist. Ed25519-Private-Schlüssel werden aus Zufallszahlen generiert und dann durch Bitmaskierung auf die Bytes 0 und 31 "geklammert". Dies wird bei Red25519 nicht durchgeführt. Die Funktionen GENERATE_ALPHA() und BLIND_PRIVKEY() definieren oben generieren ordnungsgemäße Red25519-Private-Schlüssel, indem sie mod L verwenden.

In Red25519 verwendet die Berechnung von r für das Signieren zusätzliche Zufallsdaten und verwendet den öffentlichen Schlüsselwert anstelle des Hashs des privaten Schlüssels. Aufgrund der Zufallsdaten ist jede Red25519-Signatur unterschiedlich, selbst wenn dieselben Daten mit demselben Schlüssel signiert werden.

Unterzeichnung:

  ```text
T = 80 Zufallsbytes
  r = H*(T || öffentlicher Schlüssel || Nachricht)
  // der Rest ist derselbe wie in Ed25519
```

Überprüfung:

  ```text
// gleich wie in Ed25519
```



Verschlüsselung und Bearbeitung
```````````````````````````````
#### Ableitung der Subcreditentials
Im Rahmen des Verschleierungsvorgangs müssen wir sicherstellen, dass ein verschlüsseltes LS2 nur von jemandem entschlüsselt werden kann, der den entsprechenden öffentlichen Signierungsschlüssel des Ziels kennt. Das vollständige Ziel ist nicht erforderlich.
Um dies zu erreichen, leiten wir ein Credential vom öffentlichen Signierungsschlüssel ab:

  ```text
A = öffentlicher Signierungsschlüssel des Ziels
  stA = Signaturtyp von A, 2 Bytes Big Endian (0x0007 oder 0x000b)
  stA' = Signaturtyp von A', 2 Bytes Big Endian (0x000b)
  keydata = A || stA || stA'
  credential = H("credential", keydata)
```

Der Personalisierungs-String stellt sicher, dass das Credential nicht mit einem Hash kollidiert, der als DHT-Lookup-Schlüssel verwendet wird, wie der einfache Ziel-Hash.

Für einen gegebenen verschleierten Schlüssel können wir dann ein Subcredential ableiten:

  ```text
subcredential = H("subcredential", credential || verschleierter öffentlicher Schlüssel)
```

Das Subcredential wird in die untenstehenden Schlüsselderivationsprozesse eingeführt, die diese Schlüssel an die Kenntnis des öffentlichen Signierungsschlüssels des Ziels binden.

#### Schicht-1-Verschlüsselung
Zuerst wird der Eingang für den Schlüsselderivationsprozess vorbereitet:

  ```text
outerInput = subcredential || veröffentlicht-Zeitstempel
```

Als nächstes wird ein zufälliges Salt generiert:

  ```text
outerSalt = CSRNG(32)
```

Dann wird der Schlüssel, der zur Verschlüsselung von Schicht 1 verwendet wird, abgeleitet:

  ```text
keys = HKDF(outerSalt, outerInput, "ELS2_L1K", 44)
  outerKey = keys[0:31]
  outerIV = keys[32:43]
```

Abschließend wird der Schicht-1-Klartext verschlüsselt und serialisiert:

  ```text
outerCiphertext = outerSalt || ENCRYPT(outerKey, outerIV, outerPlaintext)
```

#### Schicht-1-Entschlüsselung
Das Salt wird aus dem Schicht-1-Chiffretext analysiert:

  ```text
outerSalt = outerCiphertext[0:31]
```

Dann wird der Schlüssel, der zur Verschlüsselung von Schicht 1 verwendet wurde, abgeleitet:

  ```text
outerInput = subcredential || veröffentlicht-Zeitstempel
  keys = HKDF(outerSalt, outerInput, "ELS2_L1K", 44)
  outerKey = keys[0:31]
  outerIV = keys[32:43]
```

Abschließend wird der Schicht-1-Chiffretext entschlüsselt:

  ```text
outerPlaintext = DECRYPT(outerKey, outerIV, outerCiphertext[32:end])
```

#### Schicht-2-Verschlüsselung
Wenn die Client-Autorisierung aktiviert ist, wird ``authCookie`` wie unten beschrieben berechnet.
Wenn die Client-Autorisierung deaktiviert ist, ist ``authCookie`` das null-Längen-Byte-Array.

Die Verschlüsselung erfolgt auf ähnliche Weise wie bei Schicht 1:

  ```text
innerInput = authCookie || subcredential || veröffentlicht-Zeitstempel
  innerSalt = CSRNG(32)
  keys = HKDF(innerSalt, innerInput, "ELS2_L2K", 44)
  innerKey = keys[0:31]
  innerIV = keys[32:43]
  innerCiphertext = innerSalt || ENCRYPT(innerKey, innerIV, innerPlaintext)
```

#### Schicht-2-Entschlüsselung
Wenn die Client-Autorisierung aktiviert ist, wird ``authCookie`` wie unten beschrieben berechnet.
Wenn die Client-Autorisierung deaktiviert ist, ist ``authCookie`` das null-Längen-Byte-Array.

Die Entschlüsselung erfolgt auf ähnliche Weise wie bei Schicht 1:

  ```text
innerInput = authCookie || subcredential || veröffentlicht-Zeitstempel
  innerSalt = innerCiphertext[0:31]
  keys = HKDF(innerSalt, innerInput, "ELS2_L2K", 44)
  innerKey = keys[0:31]
  innerIV = keys[32:43]
  innerPlaintext = DECRYPT(innerKey, innerIV, innerCiphertext[32:end])
```


Client-spezifische Autorisierung
````````````````````````
Wenn die Client-Autorisierung für ein Ziel aktiviert ist, führt der Server eine Liste von
Clients, die autorisiert werden, die verschlüsselten LS2-Daten zu entschlüsseln. Die Daten, die pro Client gespeichert werden,
hängen vom Autorisierungsmechanismus ab und enthalten eine Form von Schlüsseldaten, die jeder
Client generiert und sicher an den Server überträgt.

Es gibt zwei Alternativen für die Implementierung der client-spezifischen Autorisierung:

#### DH-Client-Autorisierung
Jeder Client generiert ein DH-Schlüsselpaar ``[csk_i, cpk_i]`` und sendet den öffentlichen Schlüssel ``cpk_i``
an den Server.

Serververarbeitung
^^^^^^^^^^^^^^^^^
Der Server generiert ein neues ``authCookie`` und ein ephemeres DH-Schlüsselpaar:

  ```text
authCookie = CSRNG(32)
  esk = GENERATE_PRIVATE()
  epk = DERIVE_PUBLIC(esk)
```

Dann verschlüsselt der Server für jeden autorisierten Client ``authCookie`` zu seinem öffentlichen Schlüssel:

  ```text
sharedSecret = DH(esk, cpk_i)
  authInput = sharedSecret || cpk_i || subcredential || veröffentlicht-Zeitstempel
  okm = HKDF(epk, authInput, "ELS2_XCA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
  clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
```

Der Server platziert jedes ``[clientID_i, clientCookie_i]`` Tuple in Schicht 1 des
verschlüsselten LS2, zusammen mit ``epk``.

Client-Verarbeitung
^^^^^^^^^^^^^^^^^
Der Client verwendet seinen privaten Schlüssel, um seine erwartete Client-ID ``clientID_i`` zu ermitteln,
Verschlüsselungsschlüssel ``clientKey_i`` und Verschlüsselungs-IV ``clientIV_i``:

  ```text
sharedSecret = DH(csk_i, epk)
  authInput = sharedSecret || cpk_i || subcredential || veröffentlicht-Zeitstempel
  okm = HKDF(epk, authInput, "ELS2_XCA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
```

Dann sucht der Client in den Schicht-1-Autorisierungsdaten nach einem Eintrag, der
``clientID_i`` enthält. Wenn ein passender Eintrag existiert, entschlüsselt der Client ihn, um
``authCookie`` zu erhalten:

  ```text
authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie_i)
```

#### Pre-shared key Client-Autorisierung
Jeder Client generiert einen geheimen 32-Byte-Schlüssel ``psk_i`` und sendet ihn an den Server.
Alternativ kann der Server den geheimen Schlüssel generieren und ihn mit einem oder mehreren Clients teilen.


Serververarbeitung
^^^^^^^^^^^^^^^^^
Der Server generiert ein neues ``authCookie`` und Salt:

  ```text
authCookie = CSRNG(32)
  authSalt = CSRNG(32)
```

Dann verschlüsselt der Server für jeden autorisierten Client ``authCookie`` zu seinem Pre-shared key:

  ```text
authInput = psk_i || subcredential || veröffentlicht-Zeitstempel
  okm = HKDF(authSalt, authInput, "ELS2PSKA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
  clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
```

Der Server platziert jedes ``[clientID_i, clientCookie_i]`` Tuple in Schicht 1 des
verschlüsselten LS2, zusammen mit ``authSalt``.

Client-Verarbeitung
^^^^^^^^^^^^^^^^^
Der Client nutzt seinen pre-shared key, um seine erwartete Client-ID ``clientID_i`` zu ermitteln,
Verschlüsselungsschlüssel ``clientKey_i`` und Verschlüsselungs-IV ``clientIV_i``:

  ```text
authInput = psk_i || subcredential || veröffentlicht-Zeitstempel
  okm = HKDF(authSalt, authInput, "ELS2PSKA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
```

Dann sucht der Client in den Schicht-1-Autorisierungsdaten nach einem Eintrag, der
``clientID_i`` enthält. Wenn ein passender Eintrag existiert, entschlüsselt der Client ihn, um
``authCookie`` zu erhalten:

  ```text
authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie_i)
```

#### Sicherheitsüberlegungen
Beide oben genannten Methoden für Client-Authentifizierungsmechanismen bieten Privatsphäre für die Mitgliedschaft der Clients.
Ein Entity, das nur das Ziel kennt, kann zwar sehen, wie viele Clients gleichzeitig eingetragen sind,
kann jedoch nicht ermitteln, welche Clients hinzugefügt oder widerrufen werden.

Server SOLLTEN die Reihenfolge der Clients jedes Mal, wenn sie ein verschlüsseltes LS2 generieren, randomisieren, um
zu verhindern, dass Clients ihre Position in der Liste kennen und daraus ableiten, wann andere Clients
hinzugefügt oder widerrufen werden.

Ein Server KANN sich dafür entscheiden, die Anzahl der eingetragenen Clients zu verschleiern, indem er zufällige
Einträge in die Liste der Authorisierungsdaten einfügt.

Vorteile der DH-Client-Authentifizierung
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- Die Sicherheit des Schemas hängt nicht allein von der außerhalb liegenden Übertragung des Client-Schlüsselmaterals ab.
  Der private Schlüssel des Clients muss niemals das Gerät verlassen, und daher kann ein
  Angreifer, der in der Lage ist, die außerbande Übertragung abzufangen, aber den DH-
  Algorithmus nicht brechen, weder das verschlüsselte LS2 entschlüsseln, noch ermitteln, wie lange der Client
  Zugriff erhält.

Nachteile der DH-Client-Authentifizierung
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- Erfordert N + 1 DH-Operationen auf der Serverseite für N Clients.
- Benötigt eine DH-Operation auf der Client-Seite.
- Erfordert, dass der Client den geheimen Schlüssel generiert.

Vorteile der PSK-Client-Authentifizierung
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- Erfordert keine DH-Operationen.
- Erlaubt es dem Server, den geheimen Schlüssel zu generieren.
- Erlaubt dem Server den gleichen Schlüssel an mehrere Clients zu verteilen, falls gewünscht.

Nachteile der PSK-Client-Authentifizierung
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- Die Sicherheit des Schemas hängt entscheidend von der außerhalb liegenden Übertragung des Client-Schlüsselmaterals ab. Ein Angreifer, der die Übertragung für einen bestimmten Client abfängt, kann
  jedes nachfolgende verschlüsselte LS2 entschlüsseln, für das dieser Client autorisiert ist, ebenso
  wie er bestimmen kann, wann der Zugriff des Clients widerrufen wird.


Verschlüsseltes LS mit Basis 32 Adressen
`````````````````````````````````````````

Siehe Vorschlag 149.

Sie können kein verschlüsseltes LS2 für Bittorrent verwenden, wegen der kompakten Antwortnachrichten, die 32 Bytes lang sind.
Die 32 Bytes enthalten nur den Hash. Es gibt keinen Raum, um anzugeben, dass das
Leaseset verschlüsselt ist, oder für die Signaturtypen.



Verschlüsseltes LS mit Offline-Schlüsseln
````````````````````````````````
Für verschlüsselte Leasesets mit Offline-Schlüsseln müssen die verschleierten privaten Schlüssel ebenfalls offline generiert werden,
einer für jeden Tag.

Da der optionale Offline-Signaturblock im klartextlischen Teil des verschlüsselten Leasesets ist,
könnte jeder, der Floodfills ausliest, dies verwenden, um das Leaseset (aber nicht entschlüsselt) über mehrere Tage zu verfolgen.
Um dies zu verhindern, sollte der Eigentümer der Schlüssel auch neue transiente Schlüssel
für jeden Tag generieren.
Sowohl die transienten als auch die verschleierten Schlüssel können im Voraus generiert und an den Router
in einem Paket geliefert werden.

Es gibt in diesem Vorschlag kein Dateiformat zum Verpacken mehrerer transiente und
verschleierter Schlüssel und deren Bereitstellung an den Client oder Router.
Es gibt in diesem Vorschlag keine I2CP-Protokollerweiterung zur Unterstützung
von verschlüsselten Leasesets mit Offline-Schlüsseln.



Anmerkungen
`````

- Ein Dienst, der verschlüsselte Leasesets verwendet, würde die verschlüsselte Version an die
  Floodfills senden. Für Effizienz allerdings, würde er unverschlüsselte Leasesets an
  Clients in der umhüllten Garlic-Nachricht senden, nachdem diese authentifiziert wurden (z.B. über eine Weißliste).

- Floodfills können die maximale Größe auf einen angemessenen Wert begrenzen, um Missbrauch zu verhindern.

- Nach der Entschlüsselung sollten mehrere Checks durchgeführt werden, unter anderem ob
  der innere Zeitstempel und das Ablaufen mit denen auf oberster Ebene übereinstimmen.

- ChaCha20 wurde anstelle von AES ausgewählt. Während die Geschwindigkeiten ähnlich sind, wenn AES-
  Hardware-Unterstützung verfügbar ist, ist ChaCha20 2,5-3x schneller, wenn
  AES-Hardware-Unterstützung nicht verfügbar ist, z.B. bei kostengünstigen ARM-Geräten.

- Wir sorgen uns nicht genug um die Geschwindigkeit, um BLAKE2b zu verwenden. Es hat eine Ausgabengröße, die
  groß genug ist, um die größten n, die wir erfordern, unterzubringen (oder wir können es einmal pro
  gewünschtem Schlüssel mit einem Zählerargument aufrufen). BLAKE2b ist viel schneller als SHA-256 und
  würde bei Verwendung von Keyed-Blake2b die Gesamtanzahl der Hash-Funktionsaufrufe verringern.
  Anzahl der Hash-Funktionsaufrufe reduzieren. Allerdings siehe Vorschlag 148, in dem vorgeschlagen wird, dass wir zu BLAKE2b aus anderen Gründen wechseln.
  See [Secure key derivation performance](https://www.lvh.io/posts/secure-key-derivation-performance.html).


### Meta LS2

Dies wird verwendet, um Multihoming zu ersetzen. Wie jedes Leaseset wird dies vom
Ersteller signiert. Dies ist eine authentifizierte Liste von Ziel-Hashes.

Das Meta LS2 ist die Oberseite von und möglicherweise Zwischenknoten eines Baumes.
Es enthält eine Anzahl von Einträgen, von denen jeder auf einen LS, LS2 oder einen anderen Meta LS2
verweist, um massives Multihoming zu unterstützen.
Ein Meta LS2 kann eine Mischung aus LS-, LS2- und Meta LS2-Einträgen enthalten.
Die Blätter des Baumes sind immer ein LS oder LS2.
Der Baum ist ein DAG; Schleifen sind verboten; Clients, die nachschauen, müssen Schleifen erkennen und
verweigern, ihnen zu folgen.

Ein Meta LS2 kann ein viel längeres Ablaufdatum haben als ein Standard-LS oder LS2.
Die oberste Ebene kann ein Ablaufdatum haben, das mehrere Stunden nach dem Veröffentlichungsdatum liegt.
Die maximale Ablaufzeit wird von Floodfills und Clients durchgesetzt und ist TBD.

Anwendungsfall für das Meta LS2 ist massives Multihoming, jedoch ohne mehr
Schutz für die Korrelation von Routern zu Leasesets (bei Router-Neustart) als
er jetzt mit LS oder LS2 bereitgestellt wird.
Dies entspricht dem "facebook"-Anwendungsfall, der wahrscheinlich keine
Korrelationserkennung benötigt. Dieser Anwendungsfall benötigt wahrscheinlich Offline-Schlüssel,
die im Standard-Header auf jeder Ebene des Baumes bereitgestellt werden.

Das Back-End-Protokoll für die Koordination zwischen den Blatt-Routern, den Zwischen- und Haupt-Meta LS-Unterzeichnern ist hier nicht spezifiziert. Die Anforderungen sind extrem einfach - nur überprüfen, ob der Peer aktiv ist, und alle paar Stunden ein neues LS veröffentlichen. Die einzige Komplexität besteht darin, neue Publisher für die oberste oder mittlere Ebene der Meta LS bei Fehlern auszuwählen.
Mix-and-match Leasesets, bei denen Leases von mehreren Routern kombiniert, signiert und in einem einzigen Leaseset veröffentlicht werden, sind in Vorschlag 140, "invisible multihoming", dokumentiert. Dieser Vorschlag ist unhaltbar, wie er geschrieben ist, weil Streaming-Verbindungen nicht
"sticky" zu einem einzigen Router wären, siehe http://zzz.i2p/topics/2335 .

Das Backend-Protokoll und die Interaktion mit den Interna von Routern und Clients wären
ziemlich komplex für invisibles Multihoming.

Um eine Überlastung des Floodfill für das oberste Meta LS zu vermeiden, sollte das Ablaufdatum
mehrere Stunden betragen. Clients müssen das oberste Meta LSN cachen und es
persistieren, wenn es nicht abgelaufen ist.

Wir müssen einen algorithmus definieren, damit Clients den Baum durchlaufen, einschließlich Fallbacks,
um sicherzustellen, dass die Nutzung sich verteilt. Einige Funktion aus Hash-Distanz, Kosten und Zufälligkeit.
Wenn ein Knoten sowohl LS als auch Meta LS hat, müssen wir wissen, wann es erlaubt ist
diese Leases zu verwenden, und wann wir dem Baum weiter folgen müssen.




Abfragemit
    Standard-LS-Flag (1)
Speichern mit
    Meta LS2 Typ (7)
Speichern bei
    Hash des Ziels
    Dieser Hash wird dann verwendet, um den täglichen "Routing-Schlüssel" zu generieren, wie bei LS1
Typische Laufzeit
    Stunden. Maximal 18,2 Stunden (65535 Sekunden)
Veröffentlicht von
    "Master"-Ziel oder Koordinator oder Zwischenkoordinatoren

Format
``````
::

  Standard-LS2-Header wie oben angegeben

  Meta LS2 Typspezifischer Teil
  - Eigenschaften (Mapping wie in der gemeinsamen Strukturspezifikation angegeben, 2 Null-Bytes bei Keine vorhanden)
  - Anzahl der Einträge (1 Byte) Maximum TBD
  - Einträge: Jeder Eintrag enthält: (40 Bytes)
    - Hash (32 Bytes)
    - Flags (2 Bytes)
      TBD. Für Kompatibilität mit zukünftigen Anwendungen alle auf null setzen.
    - Typ (1 Byte) Der Typ von LS, den er referenziert;
      1 für LS, 3 für LS2, 5 für verschlüsselt, 7 für Meta, 0 für unbekannt.
    - Kosten (Priorität) (1 Byte)
    - Läuft ab (4 Bytes) (4 Bytes, Big Endian, Sekunden seit Epoche, rollt über in 2106)
  - Anzahl der Widerrufe (1 Byte) Maximum TBD
  - Widerrufungen: Jede Widerrufung enthält: (32 Bytes)
    - Hash (32 Bytes)

  Standard LS2 Signatur:
  - Signatur (40+ Bytes)
    Die Signatur umfasst alles oben genannte.

Flags und Eigenschaften: für zukünftige Verwendung


Anmerkungen
`````
- Ein verteilter Dienst, der dies verwendet, hätte ein oder mehrere "Masters" mit dem
  privaten Schlüssel des Dienstziels. Sie würden (außerhalb der Band) die
  aktuelle Liste der aktiven Ziele bestimmen und das Meta LS2 veröffentlichen. Zum
  Redundanz könnten mehrere Masters das
  Meta LS2 multihomen (d.h. gleichzeitig veröffentlichen).

- Ein verteilter Dienst könnte mit einem einzigen Ziel beginnen oder das alte Multihoming verwenden,
  dann auf ein Meta LS2 umsteigen. Eine Standard-LS-Anfrage könnte
  ein beliebiges zur Rückgabe anbieten ein LS, LS2 oder Meta LS2.

- Wenn ein Dienst ein Meta LS2 verwendet, hat es keine Tunnel (leases).


### Service Record

Dies ist ein individueller Eintrag, der besagt, dass ein Ziel an einem
Dienst teilnimmt. Es wird vom Teilnehmer an das Floodfill gesendet. Es wird nie
individuell von einem Floodfill gesendet, sondern nur als Teil einer Service List. Der Service
Record wird auch verwendet, um die Teilnahme an einem Dienst zu widerrufen, indem die
Laufzeit auf null gesetzt wird.

Dies ist kein LS2, verwendet aber den Standard-LS2-Header und das Signaturformat.

Abfragemit
    n/a, siehe Service List
Speichern mit
    Service Record Typ (9)
Speichern bei
    Hash des Dienstnamens
    Dieser Hash wird dann verwendet, um den täglichen "Routing-Schlüssel" zu generieren, wie bei LS1
Typische Laufzeit
    Stunden. Maximal 18,2 Stunden (65535 Sekunden)
Veröffentlicht von
    Ziel

Format
``````
::

  Standard-LS2-Header wie oben angegeben

  Service Record Typspezifischer Teil
  - Port (2 Bytes, Big Endian) (0 wenn nicht spezifiziert)
  - Hash des Dienstnamens (32 Bytes)

  Standard LS2 Signatur:
  - Signatur (40+ Bytes)
    Die Signatur umfasst alles oben genannte.


Anmerkungen
`````
- Wenn der Ablauf alle Nullen ist, sollten die Floodfills den Datensatz widerrufen und nicht mehr
  in der Service List aufnehmen.

- Speicherung: Das Floodfill kann die Speicherung dieser Datensätze streng drosseln und
  die Anzahl der pro Hash gespeicherten Einträge und deren Laufzeit limitieren. Eine Weißliste
  der Hashes kann ebenfalls verwendet werden.

- Jeder andere NetDB-Typ am gleichen Hash hat Vorrang, so dass ein Servicerecord niemals
  ein LS/RI überschreiben kann, aber ein LS/RI wird alle Service Records an diesem Hash überschreiben.



### Service List

Dies ist nichts Ähnliches wie ein LS2 und verwendet ein anderes Format.

Die Dienstliste wird vom Floodfill erstellt und signiert. Es ist nicht authentifiziert
in dem Sinne, dass jeder einem Dienst beitreten kann, indem er einen Service Record an einen
Floodfill veröffentlicht.

Eine Service List enthält Short Service Records, keine vollständigen Service Records. Diese
enthalten Signaturen, aber nur Hashes, keine vollständigen Ziele, und alle Listen sind von unbekannter Qualität.

Die Sicherheit, falls vorhanden, und die Wünschbarkeit von Dienstlisten ist TBD.
Floodfills könnten die Veröffentlichung und Suchanfragen auf eine Whitelist von Diensten
begrenzen, aber diese Whitelist kann je nach Implementierung oder Betreiberpräferenz variieren.
Es könnte unmöglich sein, einen Konsens über eine gemeinsame Basiswhitelist
über alle Implementierungen hinweg zu erreichen.

Wenn der Dienstname im obenstehenden Service Record enthalten ist,
dann könnten Floodfill-Betreiber Einwände erheben; wenn nur der Hash enthalten ist,
gibt es keine Verifizierung, und ein Service-Record könnte "eindringen" vor
jedem anderen NetDB-Typ und im Floodfill gespeichert werden.


Abfrage mit
    Service List Suchtyp (11)
Speichern mit
    Service List Typ (11)
Speichern bei
    Hash des Dienstnamens
    Dieser Hash wird dann verwendet, um den täglichen "Routing-Schlüssel" zu generieren, wie bei LS1
Typische Laufzeit
    Stunden, nicht in der Liste selbst spezifiziert, bis zur lokalen Richtlinie
Veröffentlicht von
    Niemand, nie zum Floodfill gesendet, nie geflutet.

Format
``````
Verwendet NICHT den oben spezifizierten Standard-LS2-Header.

::

  - Typ (1 Byte)
    Tatsächlich nicht in der Überschrift, sondern Teil der durch die Signatur abgedeckten Daten.
    Nehmen Sie aus dem Datenbank-Speichermeldungsfeld.
  - Hash des Dienstnamens (implizit in der Datenbank-Speichermeldung)
  - Hash des Erstellers (Floodfill) (32 Bytes)
  - Veröffentlicht-Zeitstempel (8 Bytes, Big Endian)

  - Anzahl der Short Service Records (1 Byte)
  - Liste der Short Service Records:
    Jeder Short Service Record enthält (90+ Bytes)
    - Ziel-Hash (32 Bytes)
    - Veröffentlicht-Zeitstempel (8 Bytes, Big Endian)
    - Läuft ab (4 Bytes, Big Endian) (Offset ab veröffentlicht in ms)
    - Flags (2 Bytes)
    - Port (2 Bytes, Big Endian)
    - Sig-Länge (2 Bytes, Big Endian)
    - Signatur des Ziels (40+ Bytes)

  - Anzahl der Widerrufungsdatensätze (1 Byte)
  - Liste der Widerrufungsdatensätze:
    Jeder Widerrufungsdatensatz enthält (86+ Bytes)
    - Ziel-Hash (32 Bytes)
    - Veröffentlicht-Zeitstempel (8 Bytes, Big Endian)
    - Flags (2 Bytes)
    - Port (2 Bytes, Big Endian)
    - Sig-Länge (2 Bytes, Big Endian)
    - Signatur des Ziels (40+ Bytes)

  - Signatur des Floodfills (40+ Bytes)
    Die Signatur umfasst alles oben genannte.

Zur Überprüfung der Signatur der Service List:

- Hash des Dienstnamens voranstellen
- Hash des Erstellers entfernen
- Signatur der modifizierten Inhalte überprüfen

Zur Überprüfung der Signatur jedes Short Service Records:

- Ziel abrufen
- Signatur von (Veröffentlicht Zeitstempel + Läuft ab + Flags + Port + Hash des
  Dienstnamens) überprüfen

Zur Überprüfung der Signatur jedes Widerrufungsdatensatzes:

- Ziel abrufen
- Signatur von (Veröffentlicht Zeitstempel + 4 Null-Bytes + Flags + Port + Hash
  des Dienstnamens) überprüfen

Anmerkungen
`````
- Wir verwenden die Signaturlänge statt Signaturtyp, um unbekannte Signaturtypen zu unterstützen.

- Es gibt kein Ablaufdatum einer Service List, Empfänger können ihre eigene Entscheidung basierend auf der Richtlinie oder dem Ablauf der einzelnen Datensätze treffen.

- Service Lists werden nicht geflutet, nur einzelne Service Records. Jedes
  Floodfill erstellt, signiert und cached eine Service List. Das Floodfill verwendet seine
  eigene Richtlinie für Cache-Zeit und die maximale Anzahl an Service- und Widerrufungsdatensätze.



## Änderungen an der Common Structures Spezifikation erforderlich


### Key-Zertifikate

Außerhalb des Geltungsbereichs dieses Vorschlags.
Vergleichen Sie die ECIES-Vorschläge 144 und 145.


### Neue Zwischenstrukturen

Fügen Sie neue Strukturen für Lease2, MetaLease, LeaseSet2Header und OfflineSignature hinzu.
Wirksam seit Version 0.9.38.


### Neue NetDB-Typen

Fügen Sie für jeden neuen Leasesettyp Strukturen hinzu, die oben aufgenommen wurden.
Für LeaseSet2, verschlüsseltes LeaseSet und MetaLeaseSet,
ab Version 0.9.38 wirksam.
Für Service Record und Service List
vorläufig und nicht geplant.


### Neuer Signaturtyp

Fügen Sie RedDSA_SHA512_Ed25519 Typ 11 hinzu.
Öffentlicher Schlüssel ist 32 Bytes; privater Schlüssel ist 32 Bytes; Hash ist 64 Bytes; Signatur ist 64 Bytes.



## Änderungen an der Verschlüsselungsspezifikation erforderlich

Außerhalb des Geltungsbereichs dieses Vorschlags.
Siehe die Vorschläge 144 und 145.



## I2NP Änderungen erforderlich

Fügen Sie eine Notiz hinzu: LS2 kann nur an Floodfills mit einer Mindestversion veröffentlicht werden.


### Database Lookup Message

Fügen Sie den Service List-Suchtyp hinzu.

Änderungen
```````
::

  Flags-Byte: Lookup-Typ Feld, derzeit Bits 3-2, erweitert auf Bits 4-2.
  Lookup-Typ 0x04 wird als Service List Lookup definiert.

  Fügen Sie die Notiz hinzu: Service List Lookup darf nur an Floodfills mit einer Mindestversion gesendet werden.
  Mindestversion ist 0.9.38.

### Database Store Message

Fügen Sie alle neuen Speichertypen hinzu.

Änderungen
```````
::

  Typ Byte: Typfeld, derzeit Bit 0, erweitert auf Bits 3-0.
  Typ 3 wird als ein LS2 Store definiert.
  Typ 5 wird als ein verschlüsselter LS2 Store definiert.
  Typ 7 wird als ein Meta LS2 Store definiert.
  Typ 9 wird als ein Service Record Store definiert.
  Typ 11 wird als ein Service List Store definiert.
  Andere Typen sind undefiniert und ungültig.

  Fügen Sie eine Notiz hinzu: Alle neuen Typen dürfen nur an Floodfills einer Mindestversion veröffentlicht werden.
  Mindestversion ist 0.9.38.




## I2CP Änderungen erforderlich


### I2CP-Optionen

Neue von der Router-Seite interpretierte Optionen, die im SessionConfig Mapping gesendet werden:

::

  i2cp.leaseSetType=nnn       Der Typ des Leasesets, das in der Create Leaseset Nachricht gesendet werden soll
                              Der Wert ist derselbe wie der NetDB-Speichertyp in der obigen Tabelle.
                              Auf der Clientseite interpretiert, aber auch an den Router weitergegeben in der
                              SessionConfig, um die Absicht zu erklären und die Unterstützung zu überprüfen.

  i2cp.leaseSetEncType=nnn[,nnn]  Die zu verwendenden Verschlüsselungstypen.
                                  Auf der Clientseite interpretiert, aber auch an den Router weitergegeben
                                  in der SessionConfig, um die Absicht zu erklären und die Unterstützung zu überprüfen.
                                  Siehe die Vorschläge 144 und 145.

  i2cp.leaseSetOfflineExpiration=nnn  Das Ablaufdatum der Offline-Signatur, ASCII,
                                      Sekunden seit der Epoche.

  i2cp.leaseSetTransientPublicKey=[type:]b64  Die Base 64 des transienten privaten Schlüssels,
                                              vorangestellt von einer optionalen Signaturtypnummer
                                              oder einem Namen, standardmäßig DSA_SHA1.
                                              Länge wie aus dem Signaturtyp abgeleitet

  i2cp.leaseSetOfflineSignature=b64   Die Base 64 der Offline-Signatur.
                                      Länge wie durch den Signaturtyp des
                                      Ziel-Signaturschlüssels abgeleitet

  i2cp.leaseSetSecret=b64     Die Base 64 eines Geheimnisses, das zur Verschleierung der
                              Adresse des Leasesets verwendet wird, standardmäßig ""

  i2cp.leaseSetAuthType=nnn   Der Typ der Authentifizierung für verschlüsseltes LS2.
                              0 für keine client-spezifische Authentifizierung (Standard)
                              1 für client-spezifische DH-Authentifizierung
                              2 für client-spezifische PSK-Authentifizierung

  i2cp.leaseSetPrivKey=b64    Ein Base 64 privater Schlüssel, den der Router zur
                              Entschlüsselung des verschlüsselten LS2 verwenden soll,
                              nur wenn die client-spezifische Authentifizierung aktiviert ist


Neue auf der Client-Seite interpretierte Optionen:

::

  i2cp.leaseSetType=nnn     Der Typ des Leasesets, das in der Create Leaseset Nachricht gesendet werden soll
                            Der Wert ist derselbe wie der NetDB-Speichertyp in der obigen Tabelle.
                            Auf der Client-Seite
