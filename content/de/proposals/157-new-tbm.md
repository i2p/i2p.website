---
title: "Kleinere Tunnel-Nachrichten"
number: "157"
author: "zzz, original"
created: "2020-10-09"
lastupdated: "2021-07-31"
status: "Geschlossen"
thread: "http://zzz.i2p/topics/2957"
target: "0.9.51"
toc: true
---

## Hinweis
Implementiert ab API-Version 0.9.51.
Netzwerkbereitstellung und -test im Gange.
Unterliegt geringfügigen Überarbeitungen.
Siehe [I2NP](/docs/specs/i2np/) und [Tunnel-Creation-ECIES](/docs/specs/implementation/#tunnel-creation-ecies) für die endgültige Spezifikation.


## Übersicht


### Zusammenfassung

Die aktuelle Größe der verschlüsselten Tunnel-Bauanfrage- und Antwortdatensätze beträgt 528.
Für typische Variable Tunnel-Bau- und Variable Tunnel-Bau-Antwortnachrichten
beträgt die Gesamtgröße 2113 Byte. Diese Nachricht wird in drei 1KB-Tunnel-Nachrichten für den Rückweg fragmentiert.

Änderungen des 528-Byte-Datensatzformats für ECIES-X25519-Router sind in [Prop152](/proposals/152-ecies-tunnels/) und [Tunnel-Creation-ECIES](/docs/specs/implementation/#tunnel-creation-ecies) angegeben.
Für einen Mix aus ElGamal- und ECIES-X25519-Routern in einem Tunnel muss die Datensatzgröße
bei 528 Byte bleiben. Wenn jedoch alle Router in einem Tunnel ECIES-X25519 sind, ist ein neuer, kleinerer
Baudatensatz möglich, da die ECIES-X25519-Verschlüsselung erheblich weniger Overhead hat als ElGamal.

Kleinere Nachrichten würden Bandbreite sparen. Auch wenn die Nachrichten in eine
einzelne Tunnel-Nachricht passen könnten, wäre der Rückweg dreimal effizienter.

Dieser Vorschlag definiert neue Anforderungs- und Antwortdatensätze sowie neue Bauanforderungs- und Bauantwortnachrichten.

Der Tunnel-Ersteller und alle Hops im erstellten Tunnel müssen ECIES-X25519 und mindestens Version 0.9.51 sein.
Dieser Vorschlag wird nicht nützlich sein, bis die Mehrheit der Router im Netzwerk ECIES-X25519 ist.
Dies soll bis Ende 2021 geschehen.


### Ziele

Siehe [Prop152](/proposals/152-ecies-tunnels/) und [Prop156](/proposals/156-ecies-routers/) für zusätzliche Ziele.

- Kleinere Datensätze und Nachrichten
- Genügend Platz für zukünftige Optionen bereitstellen, wie in [Prop152](/proposals/152-ecies-tunnels/) und [Tunnel-Creation-ECIES](/docs/specs/implementation/#tunnel-creation-ecies)
- In eine Tunnel-Nachricht für den Rückweg passen
- Nur ECIES-Hops unterstützen
- Verbesserungen beibehalten, die in [Prop152](/proposals/152-ecies-tunnels/) und [Tunnel-Creation-ECIES](/docs/specs/implementation/#tunnel-creation-ecies) implementiert wurden
- Maximale Kompatibilität mit aktuellem Netzwerk
- Eingehende Bau-Nachrichten vom OBEP verbergen
- Ausgehende Bau-Antwortnachrichten vom IBGW verbergen
- Kein Upgrade des gesamten Netzwerks auf einen "Stichtag" benötigen
- Schrittweise Einführung zur Minimierung von Risiken
- Bestehende kryptografische Primitiven wiederverwenden


### Nicht-Ziele

Siehe [Prop156](/proposals/156-ecies-routers/) für zusätzliche Nicht-Ziele.

- Keine Anforderung für gemischte ElGamal/ECIES-Tunnel
- Schichtverschlüsselungsänderungen, siehe [Prop153](/proposals/153-chacha20-layer-encryption/)
- Keine Beschleunigungen von Krypto-Operationen. Es wird angenommen, dass ChaCha20 und AES ähnlich sind,
  selbst mit AESNI, zumindest für die in Frage kommenden kleinen Datenmengen.


## Design


### Datensätze

Siehe Anhang für Berechnungen.

Verschlüsselte Anforderungs- und Antwortdatensätze werden 218 Byte groß sein, verglichen mit 528 Byte jetzt.

Die unverschlüsselten Anforderungssätze werden 154 Byte sein,
verglichen mit 222 Byte für ElGamal-Datensätze,
und 464 Byte für ECIES-Datensätze, wie in [Prop152](/proposals/152-ecies-tunnels/) und [Tunnel-Creation-ECIES](/docs/specs/implementation/#tunnel-creation-ecies) definiert.

Die unverschlüsselten Antwortsätze werden 202 Byte sein,
verglichen mit 496 Byte für ElGamal-Datensätze,
und 512 Byte für ECIES-Datensätze, wie in [Prop152](/proposals/152-ecies-tunnels/) und [Tunnel-Creation-ECIES](/docs/specs/implementation/#tunnel-creation-ecies) definiert.

Die Antwortverschlüsselung wird ChaCha20 (NICHT ChaCha20/Poly1305) sein,
sodass die Klartextdatensätze nicht ein Vielfaches von 16 Byte sein müssen.

Anforderungsdatensätze werden durch die Verwendung von HKDF zur Erstellung der
Schicht- und Antwortschlüssel kleiner gemacht, damit sie nicht ausdrücklich in die Anfrage aufgenommen werden müssen.


### Tunnel-Baunachrichten

Beide werden "variabel" mit einem einbyte-großen Datensatzzahlen-Feld sein,
wie bei den bestehenden Variablen-Nachrichten.

#### ShortTunnelBuild: Typ 25

Typische Länge (mit 4 Datensätzen): 873 Byte

Wenn für eingehende Tunnelbauten verwendet,
wird empfohlen (aber nicht erforderlich), dass diese Nachricht vom Urheber knoblauchverschlüsselt wird,
zielt auf das eingehende Gateway (Lieferanweisungen ROUTER ab),
um eingehende Bau-Nachrichten vom OBEP zu verbergen.
Der IBGW entschlüsselt die Nachricht,
setzt die Antwort in den richtigen Slot und sendet die ShortTunnelBuildMessage
zum nächsten Hop.

Die Datensatzlänge wird so gewählt, dass ein knoblauchverschlüsseltes STBM
in eine einzelne Tunnel-Nachricht passt. Siehe den Anhang unten.


#### OutboundTunnelBuildReply: Typ 26

Wir definieren eine neue OutboundTunnelBuildReply-Nachricht.
Diese wird nur für ausgehende Tunnelbauten verwendet.
Der Zweck ist, ausgehende Bau-Antwortnachrichten vom IBGW zu verbergen.
Sie muss vom OBEP knoblauchverschlüsselt werden, zielt auf den Urheber
(Lieferanweisungen TUNNEL ab).
Der OBEP entschlüsselt die Tunnel-Baunachricht,
konstruiert eine OutboundTunnelBuildReply-Nachricht
und setzt die Antwort in das Klartextfeld.
Die anderen Datensätze gehen in die anderen Slots.
Dann knoblauchverschlüsselt es die Nachricht an den Urheber mit den abgeleiteten symmetrischen Schlüsseln.


#### Hinweise

Durch das Knoblauchverschlüsseln der OTBRM und STBM vermeiden wir auch potenzielle
Kompatibilitätsprobleme beim IBGW und OBEP der gepaarten Tunnel.


### Nachrichtenfluss


```
STBM: Kurze Tunnel-Baunachricht (Typ 25)
OTBRM: Ausgehende Tunnel-Bau-Antwortnachricht (Typ 26)

Ausgehender Bau A-B-C
Antwort über bestehenden eingehenden D-E-F


                Neuer Tunnel
         STBM      STBM      STBM
Ersteller ------> A ------> B ------> C ---\
                                   OBEP   \
                                          | Knoblauch eingewickelt
                                          | OTBRM
                                          | (TUNNEL-Lieferung)
                                          | von OBEP zu
                                          | Ersteller
              Bestehender Tunnel             /
Ersteller <-------F---------E-------- D <--/
                                   IBGW


Eingehender Aufbau D-E-F
Gesendet durch bestehenden ausgehenden A-B-C


              Bestehender Tunnel
Ersteller ------> A ------> B ------> C ---\
                                  OBEP    \
                                          | Knoblauch eingewickelt (optional)
                                          | STBM
                                          | (ROUTER-Lieferung)
                                          | vom Ersteller
                Neuer Tunnel                | zu IBGW
          STBM      STBM      STBM        /
Ersteller <------ F <------ E <------ D <--/
                                   IBGW


```


### Datensatzverschlüsselung

Anforderungs- und Antwortdatensatzverschlüsselung: wie in [Prop152](/proposals/152-ecies-tunnels/) und [Tunnel-Creation-ECIES](/docs/specs/implementation/#tunnel-creation-ecies) definiert.

Antwortdatensatzverschlüsselung für andere Slots: ChaCha20.


### Schichtverschlüsselung

Derzeit gibt es keinen Plan, die Schichtverschlüsselung für Tunnel, die mit
dieser Spezifikation gebaut wurden, zu ändern; sie würde AES bleiben, wie derzeit für alle Tunnel verwendet.

Eine Änderung der Schichtverschlüsselung zu ChaCha20 ist ein Thema für weitere Forschung.


### Neue Tunnel-Daten-Nachricht

Derzeit gibt es keinen Plan, die 1KB-Tunnel-Daten-Nachricht, die für Tunnel gebaut mit
dieser Spezifikation verwendet wird, zu ändern.

Es könnte nützlich sein, eine neue I2NP-Nachricht einzuführen, die größer oder variabel groß ist, parallel zu diesem Vorschlag,
für die Nutzung über diese Tunnel.
Dies würde den Overhead für große Nachrichten reduzieren.
Dies ist ein Thema für weitere Forschung.


## Spezifikation


### Kurzer Anforderungsdatensatz


#### Kurzer Anforderungsdatensatz Unverschlüsselt

Dies ist die vorgeschlagene Spezifikation des Tunnel-Bauanforderungsdatensatzes für ECIES-X25519-Router.
Zusammenfassung der Änderungen von [Tunnel-Creation-ECIES](/docs/specs/implementation/#tunnel-creation-ecies):

- Unverschlüsselte Länge von 464 auf 154 Bytes ändern
- Verschlüsselte Länge von 528 auf 218 Bytes ändern
- Schicht- und Antwortschlüssel und IVs entfernen, sie werden aus split() und einem KDF generiert


Der Anforderungsdatensatz enthält keine ChaCha-Antwortschlüssel.
Diese Schlüssel werden aus einem KDF abgeleitet. Siehe unten.

Alle Felder sind Big-Endian.

Unverschlüsselte Größe: 154 Byte.


```
bytes     0-3: Tunnel-ID zum Empfangen von Nachrichten als, ungleich null
bytes     4-7: nächste Tunnel-ID, ungleich null
bytes    8-39: nächster Router-Identitätshash
byte       40: Flags
bytes   41-42: mehr Flags, ungenutzt, aus Kompatibilitätsgründen auf 0 setzen
byte       43: Schichtverschlüsselungstyp
bytes   44-47: Anforderungszeit (in Minuten seit der Epoche, abgerundet)
bytes   48-51: Ablauf der Anforderung (in Sekunden seit der Erstellung)
bytes   52-55: nächste Nachrichten-ID
bytes    56-x: Tunnel-Bauoptionen (Mapping)
bytes     x-x: andere Daten wie durch Flags oder Optionen impliziert
bytes   x-153: zufällige Auffüllung (siehe unten)
```


Das Flags-Feld ist dasselbe wie in [Tunnel-Creation](/docs/specs/implementation/#tunnel-creation-ecies) definiert und enthält die folgenden::

 Bit-Reihenfolge: 76543210 (Bit 7 ist MSB)
 bit 7: wenn gesetzt, Nachrichten von allen zulassen
 bit 6: wenn gesetzt, Nachrichten an alle zulassen und die Antwort
        zum angegebenen nächsten Hop in einer Tunnel-Bau-Antwortnachricht senden
 bits 5-0: Undefiniert, muss aus Kompatibilitätsgründen mit zukünftigen Optionen auf 0 gesetzt werden

Bit 7 zeigt an, dass der Hop ein eingehendes Gateway (IBGW) sein wird. Bit 6
zeigt an, dass der Hop ein ausgehender Endpunkt (OBEP) sein wird. Wenn weder das eine noch das andere Bit
gesetzt ist, wird der Hop ein Zwischen-Teilnehmer sein. Beide können nicht gleichzeitig gesetzt werden.

Schichtverschlüsselungstyp: 0 für AES (wie in aktuellen Tunneln);
1 für die Zukunft (ChaCha?)

Das Ablaufdatum der Anfrage ist für zukünftige variable Tunneldauer.
Für jetzt ist der einzige unterstützte Wert 600 (10 Minuten).

Der ephemere öffentliche Schlüssel des Erstellers ist ein ECIES-Schlüssel, Big-Endian.
Er wird für das KDF für die IBGW-Schicht und Antwortschlüssel und IVs verwendet.
Dies ist nur im unverschlüsselten Datensatz in einer eingehenden Tunnel-Baunachricht enthalten.
Es ist erforderlich, da es in dieser Schicht für den Baudatensatz keine DH gibt.

Die Tunnel-Bauoptionen sind eine Mapping-Struktur, wie in [Common](/docs/specs/common-structures/) definiert.
Dies ist für zukünftige Nutzung. Derzeit sind keine Optionen definiert.
Wenn die Mapping-Struktur leer ist, ist dies zwei Bytes 0x00 0x00.
Die maximale Größe des Mappings (einschließlich des Längenfeldes) beträgt 98 Bytes,
und der maximale Wert des Längenfeldes des Mappings beträgt 96.


#### Kurzer Anforderungsdatensatz Verschlüsselt

Alle Felder sind Big-Endian außer dem ephemeren öffentlichen Schlüssel, der Little-Endian ist.

Verschlüsselte Größe: 218 Byte


```
bytes    0-15: Trunkierter Identitätshash des Hops
bytes   16-47: Ephemerer X25519-Öffentlichschlüssel des Absenders
bytes  48-201: ChaCha20-verschlüsselter ShortBuildRequestRecord
bytes 202-217: Poly1305-MAC
```


### Kurzer Antwortdatensatz


#### Kurzer Antwortdatensatz Unverschlüsselt

Dies ist die vorgeschlagene Spezifikation des Tunnel-ShortBuildReplyRecord für ECIES-X25519-Router.
Zusammenfassung der Änderungen von [Tunnel-Creation-ECIES](/docs/specs/implementation/#tunnel-creation-ecies):

- Unverschlüsselte Länge von 512 auf 202 Bytes ändern
- Verschlüsselte Länge von 528 auf 218 Bytes ändern


ECIES-Antworten werden mit ChaCha20/Poly1305 verschlüsselt.

Alle Felder sind Big-Endian.

Unverschlüsselte Größe: 202 Byte.


```
bytes    0-x: Tunnel-Bauoptionen (Mapping)
bytes    x-x: andere Daten wie durch Optionen impliziert
bytes  x-200: Zufällige Auffüllung (siehe unten)
byte     201: Antwort-Byte
```

Die Tunnel-Bauoptionen sind eine Mapping-Struktur, wie in [Common](/docs/specs/common-structures/) definiert.
Dies ist für zukünftige Nutzung. Derzeit sind keine Optionen definiert.
Wenn die Mapping-Struktur leer ist, ist dies zwei Bytes 0x00 0x00.
Die maximale Größe des Mappings (einschließlich des Längenfeldes) beträgt 201 Bytes,
und der maximale Wert des Längenfeldes des Mappings beträgt 199.

Das Antwort-Byte ist einer der folgenden Werte
wie in [Tunnel-Creation](/docs/specs/implementation/#tunnel-creation-ecies) definiert, um Fingerprinting zu vermeiden:

- 0x00 (akzeptieren)
- 30 (TUNNEL_REJECT_BANDWIDTH)


#### Kurzer Antwortdatensatz Verschlüsselt

Verschlüsselte Größe: 218 Byte


```
bytes   0-201: ChaCha20-verschlüsselter ShortBuildReplyRecord
bytes 202-217: Poly1305-MAC
```


### KDF

Siehe KDF-Abschnitt unten.


### ShortTunnelBuild
I2NP Typ 25

Diese Nachricht wird an mittlere Hops, OBEP und IBEP (Ersteller) gesendet.
Sie darf nicht an den IBGW gesendet werden (verwenden Sie stattdessen Knoblauch eingewickeltes InboundTunnelBuild).
Wenn sie vom OBEP empfangen wird, wird sie in eine OutboundTunnelBuildReply umgewandelt,
Knoblauch eingewickelt, und an den Urheber gesendet.


```
+----+----+----+----+----+----+----+----+
| num| ShortBuildRequestRecords...
+----+----+----+----+----+----+----+----+

num ::
       1 Byte `Integer`
       Gültige Werte: 1-8

Datensatzgröße: 218 Byte
Gesamtgröße: 1+$num*218
```

#### Hinweise

* Typische Anzahl der Datensätze ist 4, für eine Gesamtgröße von 873.


### OutboundTunnelBuildReply
I2NP Typ 26

Diese Nachricht wird nur vom OBEP an den IBEP (Ersteller) über einen bestehenden eingehenden Tunnel gesendet.
Sie darf nicht an einen anderen Hop gesendet werden.
Sie ist immer Knoblauch verschlüsselt.


```
+----+----+----+----+----+----+----+----+
| num|                                  |
+----+                                  +
|      ShortBuildReplyRecords...        |
+----+----+----+----+----+----+----+----+

num ::
       Gesamtanzahl der Datensätze,
       1 Byte `Integer`
       Gültige Werte: 1-8

ShortBuildReplyRecords ::
       Verschlüsselte Datensätze
       Länge: num * 218

Verschlüsselte Datensatzgröße: 218 Byte
Gesamtgröße: 1+$num*218
```

#### Hinweise

* Typische Anzahl der Datensätze ist 4, für eine Gesamtgröße von 873.
* Diese Nachricht sollte Knoblauch verschlüsselt werden.


### KDF

Wir verwenden ck aus dem Noise-Zustand nach der Tunnel-Baudatensatzverschlüsselung/-entschlüsselung, um folgende Schlüssel abzuleiten: Antwortschlüssel, AES-Schlüssel, AES-IV-Schlüssel und Knoblauch-Antwortschlüssel/Tag für OBEP.

Antwortschlüssel:
Im Gegensatz zu langen Datensätzen können wir nicht den linken Teil von ck für den Antwortschlüssel verwenden, da er nicht der letzte ist und später verwendet wird.
Der Antwortschlüssel wird verwendet, um den Antwortdatensatz mit AEAD/Chaha20/Poly1305 und Chacha20 zu antworten, um andere Datensätze zu antworten.
Beide verwenden denselben Schlüssel, Nonce ist die Position des Datensatzes in der Nachricht, beginnend bei 0.


```
keydata = HKDF(ck, ZEROLEN, "SMTunnelReplyKey", 64)
replyKey = keydata[32:63]
ck = keydata[0:31]

Schichtschlüssel:
Der Schichtschlüssel ist derzeit immer AES, aber derselbe KDF kann für Chacha20 verwendet werden

keydata = HKDF(ck, ZEROLEN, "SMTunnelLayerKey", 64)
layerKey = keydata[32:63]

IV-Schlüssel für nicht-OBEP-Datensatz:
ivKey = keydata[0:31]
weil es das letzte ist

IV-Schlüssel für OBEP-Datensatz:
ck = keydata[0:31]
keydata = HKDF(ck, ZEROLEN, "TunnelLayerIVKey", 64)
ivKey = keydata[32:63]
ck = keydata[0:31]

OBEP-Knoblauch-Antwortschlüssel/Tag:
keydata = HKDF(ck, ZEROLEN, "RGarlicKeyAndTag", 64)
replyKey = keydata[32:63]
replyTag = keydata[0:7]
```


## Begründung

Dieses Design maximiert die Wiederverwendung bestehender kryptografischer Primitiven, Protokolle und Codes.

Dieses Design minimiert das Risiko.

ChaCha20 ist in Java-Tests für kleine Datensätze etwas schneller als AES.
ChaCha20 vermeidet eine Anforderung an die Datengröße, Vielfache von 16 zu sein.


## Implementierungs-Hinweise

- Wie bei der bestehenden variablen Tunnel-Baunachricht,
  werden Nachrichten mit weniger als 4 Datensätzen nicht empfohlen.
  Die typische Standardeinstellung sind 3 Hops.
  Eingehende Tunnel müssen mit einem zusätzlichen Datensatz für
  den Urheber gebaut werden, sodass der letzte Hop nicht weiß, dass er der letzte ist.
  Damit mittlere Hops nicht wissen, ob ein Tunnel eingehend oder ausgehend ist,
  sollten ausgehende Tunnel auch mit 4 Datensätzen gebaut werden.


## Probleme


## Migration

Die Implementierung, das Testen und die Einführung werden mehrere Releases
und etwa ein Jahr dauern. Die Phasen sind wie folgt. Zuordnung jeder Phase zu einer bestimmten Version ist TBD und hängt vom
Entwicklungstempo ab.

Einzelheiten der Implementierung und Migration können
für jede I2P-Implementierung variieren.

Der Tunnel-Ersteller muss sicherstellen, dass alle Hops im erstellten Tunnel ECIES-X25519 sind UND mindestens Version TBD.
Der Tunnel-Ersteller muss NICHT ECIES-X25519 sein; er kann ElGamal sein.
Wenn der Ersteller jedoch ElGamal ist, offenbart er dem nächsten Hop, dass er der Ersteller ist.
In der Praxis sollten diese Tunnel daher nur von ECIES-Routern erstellt werden.

Es sollte NICHT erforderlich sein, dass der gepaarte Tunnel OBEP oder IBGW ECIES ist oder
einer bestimmten Version entspricht.
Die neuen Nachrichten sind Knoblauch-verschlüsselt und nicht sichtbar beim OBEP oder IBGW
des gepaarten Tunnels.

Phase 1: Implementierung, nicht standardmäßig aktiviert

Phase 2 (nächste Veröffentlichung): Standardmäßig aktivieren

Es gibt keine Rückwärtskompatibilitätsprobleme. Die neuen Nachrichten dürfen nur an Router gesendet werden, die sie unterstützen.


## Anhang


Ohne Knoblauch-Overhead für unverschlüsseltes eingehendes STBM,
wenn wir kein ITBM verwenden:


```
Aktuelle Größe mit 4 Slots: 4 * 528 + Overhead = 3 Tunnel Nachrichten

Bau Nachricht mit 4 Slots, die in eine Tunnel Nachricht passt, nur ECIES:

1024
- 21 Fragment-Header
----
1003
- 35 unfragmentierte ROUTER-Lieferanweisungen
----
968
- 16 I2NP-Header
----
952
- 1 Anzahl der Slots
----
951
/ 4 Slots
----
237 Neue verschlüsselte Bau-Datensatzgröße (vs. 528 jetzt)
- 16 verkürzter Hash
- 32 ephem. Schlüssel
- 16 MAC
----
173 maximaler Klartext-Baudatensatz (vs. 222 jetzt)


```


Mit Knoblauch-Overhead für 'N'-Noise-Pattern zur Verschlüsselung von eingehendem STBM,
wenn wir kein ITBM verwenden:


```
Aktuelle Größe mit 4 Slots: 4 * 528 + Overhead = 3 Tunnel Nachrichten

Bau-Nachricht mit 4 Slots, die Knoblauch-verschlüsselt in eine Tunnel-Nachricht passt, nur ECIES:

1024
- 21 Fragment-Header
----
1003
- 35 unfragmentierte ROUTER-Lieferanweisungen
----
968
- 16 I2NP-Header
-  4 Länge
----
948
- 32 Byte ephem. Schlüssel
----
916
- 7 Byte DateTime-Block
----
909
- 3 Byte Knoblauch-Block-Overhead
----
906
- 9 Byte I2NP-Header
----
897
- 1 Byte Knoblauch-LOKAL-Lieferanweisungen
----
896
- 16 Byte Poly1305-MAC
----
880
- 1 Anzahl der Slots
----
879
/ 4 Slots
----
219 Neue verschlüsselte Bau-Datensatzgröße (vs. 528 jetzt)
- 16 verkürzter Hash
- 32 ephem. Schlüssel
- 16 MAC
----
155 maximaler Klartext-Baudatensatz (vs. 222 jetzt)

```

Hinweise:

Aktuelle Größe des Bau-Datensatzes vor ungenutztem Padding: 193

Das Entfernen des vollständigen Router-Hashes und die HKDF-Erzeugung von Schlüsseln/IVs würde viel Platz für zukünftige Optionen frei machen.
Wenn alles HKDF ist, beträgt der erforderliche Klartext-Raum etwa 58 Byte (ohne Optionen).

Der Knoblauch-verpackte OTBRM wird etwas kleiner sein als der Knoblauch-verpackte STBM,
weil die Lieferanweisungen LOKAL statt ROUTER sind,
kein DATETIME-Block enthalten ist und
es einen 8-Byte-Tag anstelle des 32-Byte-ephemeren Schlüssels für eine volle 'N'-Nachricht verwendet.


