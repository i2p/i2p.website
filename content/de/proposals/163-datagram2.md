---
title: "Datagram2-Protokoll"
number: "163"
author: "zzz, orignal, drzed, eyedeekay"
created: "2023-01-24"
lastupdated: "2025-04-16"
status: "Closed"
thread: "http://zzz.i2p/topics/3540"
target: "0.9.66"
toc: true
---

## Status

Genehmigt bei der Überprüfung am 2025-04-15.
Änderungen in die Spezifikationen aufgenommen.
In Java I2P ab API 0.9.66 implementiert.
Überprüfen Sie die Implementierungsdokumentation für den Status.



## Übersicht

Aus [Prop123](/proposals/123-new-netdb-entries/) als separater Vorschlag herausgezogen.

Offline-Signaturen können bei der Verarbeitung von beantwortbaren Datagrammen nicht verifiziert werden.
Es wird eine Flagge benötigt, um offline signiert anzuzeigen, aber es gibt keinen Platz, um eine Flagge zu setzen.

Wird eine komplett neue I2CP-Protokollnummer und ein neues Format erfordern,
um der [DATAGRAMS](/docs/api/datagrams/) Spezifikation hinzugefügt zu werden.
Lassen Sie uns es "Datagram2" nennen.


## Ziele

- Unterstützung von Offline-Signaturen hinzufügen
- Wiederholungswiderstand hinzufügen
- Geschmack ohne Signaturen hinzufügen
- Flags und Optionsfelder für Erweiterbarkeit hinzufügen


## Nicht-Ziele

Vollständige Ende-zu-Ende-Protokollunterstützung für Staukontrolle usw.
Das würde auf Datagram2 aufgebaut oder als Alternative dazu dienen, welches ein Low-Level-Protokoll ist.
Es wäre nicht sinnvoll, ein Hochleistungsprotokoll ausschließlich auf
Datagram2 zu entwerfen, aufgrund des From-Feldes und des Signaturen-Overheads.
Ein solches Protokoll sollte einen Initialen Handshake mit Datagram2 durchführen und dann
auf RAW-Datagramme umschalten.


## Motivation

Übrig geblieben von der LS2-Arbeit, die ansonsten 2019 abgeschlossen wurde.

Die erste Anwendung, die Datagram2 verwenden wird,
erwartet man für BitTorrent UDP-Ankündigungen, wie in i2psnark und zzzot implementiert,
siehe [Prop160](/proposals/160-udp-trackers/).


## Spezifikation für beantwortenbare Datagramme

Zur Referenz,
folgt eine Überprüfung der Spezifikation für beantwortenbare Datagramme,
kopiert von [Datagrams](/docs/api/datagrams/).
Die Standard-I2CP-Protokollnummer für beantwortenbare Datagramme ist PROTO_DATAGRAM (17).

```text
+----+----+----+----+----+----+----+----+
  | from                                  |
  +                                       +
  |                                       |
  ~                                       ~
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  |                                       |
  +----+----+----+----+----+----+----+----+
  | signature                             |
  +                                       +
  |                                       |
  +                                       +
  |                                       |
  +                                       +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  | payload...
  +----+----+----+----//


  from :: ein `Destination`
          Länge: 387+ Bytes
          Der Urheber und Unterzeichner des Datagramms

  signature :: eine `Signature`
               Signaturtyp muss zum öffentlichen Schlüsseltyp des Unterzeichners from passen
               Länge: 40+ Bytes, wie durch den Signaturtyp impliziert.
               Für den Standard-DSA_SHA1-Schlüsseltyp:
                  Die DSA `Signature` des SHA-256-Hashes der Nutzlast.
               Für andere Schlüsseltypen:
                  Die `Signature` der Nutzlast.
               Die Signatur kann durch den öffentlichen Schlüssel des Unterzeichners from verifiziert werden

  payload ::  Die Daten
              Länge: 0 bis etwa 31,5 KB (Siehe Anmerkungen)

  Gesamtlänge: Nutzlastlänge + 423+
```



## Design

- Definiere neues Protokoll 19 - Beantwortbares Datagramm mit Optionen.
- Definiere neues Protokoll 20 - Beantwortbares Datagramm ohne Signatur.
- Flags-Feld für Offline-Signaturen und zukünftige Erweiterungen hinzufügen
- Signatur nach der Nutzlast verschieben für einfachere Verarbeitung
- Neue Signaturspezifikation, anders als beantwortenbare Datagramme oder Streaming, sodass
  die Signaturüberprüfung fehlschlägt, wenn sie als beantwortenbare Datagramm- oder Streaming-Nachricht interpretiert wird.
  Dies wird erreicht, indem die Signatur nach der Nutzlast verschoben wird
  und indem der Ziel-Hash in die Signaturfunktion einbezogen wird.
- Hinzufügen von Wiederholungsprävention für Datagramme, wie in [Prop164](/proposals/164-streaming/) für Streaming geschehen.
- Abschnitt für beliebige Optionen hinzufügen
- Offline-Signaturformat aus [Common](/docs/specs/common-structures/) und [Streaming](/docs/specs/streaming/) wiederverwenden.
- Abschnitt zur Offline-Signatur muss vor den variabellen Nutzlast- und Signaturabschnitten liegen, da er die Länge
  der Signatur spezifiziert.


## Spezifikation

### Protokoll

Die neue I2CP-Protokollnummer für Datagram2 ist 19.
Fügen Sie es als PROTO_DATAGRAM2 zu [I2CP](/docs/protocol/i2cp/) hinzu.

Die neue I2CP-Protokollnummer für Datagram3 ist 20.
Fügen Sie es als PROTO_DATAGRAM2 zu [I2CP](/docs/protocol/i2cp/) hinzu.


### Datagram2-Format

Füge Datagram2 zu [DATAGRAMS](/docs/api/datagrams/) wie folgt hinzu:

```text
+----+----+----+----+----+----+----+----+
  |                                       |
  ~            from                       ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  flags  |     options (optional)      |
  +----+----+                             +
  ~                                       ~
  ~                                       ~
  +----+----+----+----+----+----+----+----+
  |                                       |
  ~     offline_signature (optional)      ~
  ~   expires, sigtype, pubkey, offsig    ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  ~            payload                    ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  ~            signature                  ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  from :: ein `Destination`
          Länge: 387+ Bytes
          Der Urheber und (sofern nicht offline signiert) der Unterzeichner des Datagramms

  flags :: (2 Bytes)
           Bit-Reihenfolge: 15 14 ... 3 2 1 0
           Bits 3-0: Version: 0x02 (0 0 1 0)
           Bit 4: Wenn 0, keine Optionen; wenn 1, Options-Mapping enthalten
           Bit 5: Wenn 0, keine Offline-Signatur; wenn 1, offline signiert
           Bits 15-6: ungenutzt, auf 0 setzen für Kompatibilität mit zukünftigen Verwendungen

  options :: (2+ Bytes, wenn vorhanden)
           Wenn Indikator für Optionen gesetzt ist, ein `Mapping`
           mit beliebigen Textoptionen

  offline_signature ::
               Wenn Indikator für Offline-Schlüssel gesetzt ist, der Abschnitt für offline Signatur,
               wie in der Spezifikation für Common Structures spezifiziert,
               mit den folgenden 4 Feldern. Länge: variiert nach online- und offline
               Signaturtypen, in der Regel 102 Bytes für Ed25519
               Dieser Abschnitt kann und sollte offline generiert werden.

    expires :: Ablaufzeitstempel
               (4 Bytes, Big Endian, Sekunden seit dem Epoch, läuft 2106 ab)

    sigtype :: Transienter Signaturtyp (2 Bytes, Big Endian)

    pubkey :: Transienter öffentlicher Signaturschlüssel (Länge wie durch Signaturtyp impliziert),
              typischerweise 32 Bytes für den Ed25519-Signaturtyp.

    offsig :: eine `Signature`
              Signatur des Ablaufzeitstempels, des transienten Signaturtyps
              und des öffentlichen Schlüssels, durch den öffentlichen Schlüssel der Destination,
              Länge: 40+ Bytes, wie durch den Signaturtyp impliziert, typischerweise
              64 Bytes für Ed25519-Signaturtyp.

  payload ::  Die Daten
              Länge: 0 bis etwa 61 KB (siehe Anmerkungen)

  signature :: eine `Signature`
               Signaturtyp muss mit dem öffentlichen Schlüsseltyp des Unterzeichners from übereinstimmen
               (wenn keine Offline-Signatur) oder dem transienten sigtype
               (wenn offline signiert)
               Länge: 40+ Bytes, wie durch den Signaturtyp impliziert, typischerweise
               64 Bytes für Ed25519-Signaturtyp.
               Die `Signature` der Nutzlast und anderer Felder wie unten spezifiziert.
               Die Signatur wird durch den öffentlichen Signaturschlüssel des Unterzeichners from verifiziert
               (wenn keine Offline-Signatur) oder den transienten pubkey
               (wenn offline signiert)

```

Gesamtlänge: mindestens 433 + Nutzlastlänge;
typische Länge für X25519-Absender und ohne Offline-Signaturen:
457 + Nutzlastlänge.
Beachten Sie, dass die Nachricht in der Regel mit gzip auf der I2CP-Schicht komprimiert wird,
was zu erheblichen Einsparungen führen wird, wenn das From-Ziel komprimierbar ist.

Hinweis: Das Offline-Signaturformat ist dasselbe wie in der Common Structures-Spezifikation [Common](/docs/specs/common-structures/) und [Streaming](/docs/specs/streaming/).

### Signaturen

Die Signatur umfasst die folgenden Felder.

- Prelude: Der 32-Byte-Hash des Zielorts (nicht im Datagramm enthalten)
- flags
- options (falls vorhanden)
- offline_signature (falls vorhanden)
- payload

In beantwortenbarem Datagramm, für den DSA_SHA1-Schlüsseltyp, war die Signatur über den
SHA-256-Hash der Nutzlast, nicht die Nutzlast selbst; hier ist die Signatur
immer über die obigen Felder (NICHT den Hash), unabhängig vom Schlüsseltyp.


### ToHash-Überprüfung

Empfänger müssen die Signatur verifizieren (mithilfe ihres Ziel-Hashes)
und das Datagramm bei einem Fehler verwerfen, zur Wiederholungsprävention.


### Datagram3-Format

Fügen Sie Datagram3 zu [DATAGRAMS](/docs/api/datagrams/) wie folgt hinzu:

```text
+----+----+----+----+----+----+----+----+
  |                                       |
  ~            fromhash                   ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  flags  |     options (optional)      |
  +----+----+                             +
  ~                                       ~
  ~                                       ~
  +----+----+----+----+----+----+----+----+
  |                                       |
  ~            payload                    ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  fromhash :: ein `Hash`
              Länge: 32 Bytes
              Der Urheber des Datagramms

  flags :: (2 Bytes)
           Bit-Reihenfolge: 15 14 ... 3 2 1 0
           Bits 3-0: Version: 0x03 (0 0 1 1)
           Bit 4: Wenn 0, keine Optionen; wenn 1, Options-Mapping enthalten
           Bits 15-5: ungenutzt, auf 0 setzen für Kompatibilität mit zukünftigen Verwendungen

  options :: (2+ Bytes, wenn vorhanden)
           Wenn Indikator für Optionen gesetzt ist, ein `Mapping`
           mit beliebigen Textoptionen

  payload ::  Die Daten
              Länge: 0 bis etwa 61 KB (siehe Anmerkungen)

```

Gesamtlänge: mindestens 34 + Nutzlastlänge.



### SAM

Fügen Sie STYLE=DATAGRAM2 und STYLE=DATAGRAM3 zur SAMv3-Spezifikation hinzu.
Aktualisieren Sie die Informationen zu Offline-Signaturen.


### Overhead

Dieses Design fügt beantwortbaren Datagrammen 2 Bytes Overhead für Flags hinzu.
Dies ist akzeptabel.



## Sicherheitsanalyse

Die Einbeziehung des Ziel-Hashes in die Signatur sollte wirksam sein, um Wiederholungsangriffe zu verhindern.

Das Datagram3-Format enthält keine Signaturen, sodass der Absender nicht verifiziert werden kann,
und Wiederholungsangriffe sind möglich. Jegliche erforderliche Validierung muss auf der Anwendungsebene stattfinden,
oder durch den Router auf der Ratchet-Ebene.



## Anmerkungen

- Die praktische Länge ist durch niedrigere Protokollschichten begrenzt - die Tunnel-
  Nachrichtenspezifikation [TUNMSG](/docs/specs/tunnel-message/#notes) begrenzt Nachrichten auf etwa 61,2 KB und die Transporte
  [TRANSPORT](/docs/transport/) beschränken Nachrichten derzeit auf etwa 64 KB, sodass die Datenlänge hier
  auf etwa 61 KB begrenzt ist.
- Siehe wichtige Anmerkungen zur Zuverlässigkeit großer Datagramme [API](/docs/api/datagrams/). Für
  beste Ergebnisse begrenzen Sie die Nutzlast auf etwa 10 KB oder weniger.




## Kompatibilität

Keine. Anwendungen müssen umgeschrieben werden, um Datagram2-I2CP-Nachrichten
basierend auf Protokoll und/oder Port zu leiten.
Datagram2-Nachrichten, die fehlgeleitet und als
beantwortbare Datagramm- oder Streaming-Nachrichten interpretiert werden, werden fehlschlagen basierend auf Signatur, Format oder beidem.



## Migration

Jede UDP-Anwendung muss die Unterstützung separat erkennen und migrieren.
Die prominenteste UDP-Anwendung ist BitTorrent.

### BitTorrent

BitTorrent DHT: Braucht wahrscheinlich Erweiterungsflagge,
z.B. i2p_dg2, koordinieren mit BiglyBT

BitTorrent UDP-Ankündigungen [Prop160](/proposals/160-udp-trackers/): Design von Anfang an.
Koordinieren mit BiglyBT, i2psnark, zzzot

### Andere

Bote: Unwahrscheinlich zu migrieren, wird nicht aktiv gewartet

Streamr: Niemand nutzt es, keine Migration geplant

SAM-UDP-Anwendungen: Keine bekannt


## Referenzen

* [API](/docs/api/datagrams/)
* [BT-SPEC](/docs/applications/bittorrent/)
* [Common](/docs/specs/common-structures/)
* [DATAGRAMS](/docs/specs/datagrams/)
* [I2CP](/docs/protocol/i2cp/)
* [Prop123](/proposals/123-new-netdb-entries/)
* [Prop160](/proposals/160-udp-trackers/)
* [Prop164](/proposals/164-streaming/)
* [Streaming](/docs/specs/streaming/)
* [TRANSPORT](/docs/transport/)
* [TUNMSG](/docs/specs/tunnel-message/#notes)
