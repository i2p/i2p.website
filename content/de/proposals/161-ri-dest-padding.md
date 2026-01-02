---
title: "RI und Ziel Padding"
number: "161"
author: "zzz"
created: "2022-09-28"
lastupdated: "2023-01-02"
status: "Offen"
thread: "http://zzz.i2p/topics/3279"
target: "0.9.57"
toc: true
---

## Status

Implementiert in 0.9.57.
Dieser Vorschlag bleibt offen, damit wir die Ideen im Abschnitt "Zukünftige Planung" verbessern und diskutieren können.


## Übersicht


### Zusammenfassung

Der ElGamal-öffentliche Schlüssel in Zielen wurde seit der Veröffentlichung 0.6 (2005) nicht verwendet.
Obwohl unsere Spezifikationen sagen, dass er nicht verwendet wird, sagen sie NICHT, dass Implementierungen
die Erzeugung eines ElGamal-Schlüsselpaares vermeiden und das Feld einfach mit zufälligen Daten füllen können.

Wir schlagen vor, die Spezifikationen dahingehend zu ändern, dass das Feld ignoriert wird und dass Implementierungen
das Feld mit zufälligen Daten füllen KÖNNEN. Diese Änderung ist abwärtskompatibel.
Es ist keine Implementierung bekannt, die den ElGamal-öffentlichen Schlüssel validiert.

Zusätzlich bietet dieser Vorschlag den Implementierern Leitlinien,
wie sie die zufälligen Daten für Ziel- UND Router-Identitätspadding generieren können,
damit sie komprimierbar sind, aber dennoch sicher bleiben,
und ohne dass Base 64-Repräsentationen beschädigt oder unsicher erscheinen.
Dies bietet die meisten Vorteile der Entfernung der Padding-Felder,
ohne dass störende Protokolländerungen nötig sind.
Komprimierbare Ziele reduzieren die Streaming-SYN- und antwortbaren Datagrammgrößen;
komprimierbare Router-Identitäten reduzieren die Größe von Datenbank-Store-Nachrichten, SSU2-Session-Bestätigten-Nachrichten
und Reseed-su3-Dateien.

Abschließend erörtert der Vorschlag Möglichkeiten für neue Ziel- und Router-Identitätsformate,
die das Padding insgesamt beseitigen würden. Es gibt auch eine kurze Diskussion über Post-Quanten-Kryptographie und wie
diese die zukünftige Planung beeinflussen könnte.


### Ziele

- Anforderung zur Erzeugung eines ElGamal-Schlüsselpaares für Ziele eliminieren
- Best Practices empfehlen, damit Ziele und Router-Identitäten hochkomprimierbar sind,
  aber keine offensichtlichen Muster in Base 64-Repräsentationen zeigen.
- Annahme von Best Practices durch alle Implementierungen ermutigen,
  sodass die Felder nicht unterscheidbar sind
- Streaming-SYN-Größe reduzieren
- Größe antwortbarer Datagramme reduzieren
- SSU2-RI-Blockgröße reduzieren
- Größe und Fragmentierungshäufigkeit von SSU2-Session-Bestätigungen reduzieren
- Größe der Datenbank-Store-Nachricht (mit RI) reduzieren
- Reseed-Dateigröße reduzieren
- Kompatibilität in allen Protokollen und APIs aufrechterhalten
- Spezifikationen aktualisieren
- Alternativen für neue Ziel- und Router-Identitätsformate diskutieren

Durch die Eliminierung der Anforderung zur Erzeugung von ElGamal-Schlüsseln
können Implementierungen möglicherweise den ElGamal-Code vollständig entfernen,
vorbehaltlich von Überlegungen zur Abwärtskompatibilität in anderen Protokollen.


## Design

Streng genommen ist der 32-Byte-Signierschlüssel allein (sowohl in Zielen als auch in Router-Identitäten)
sowie der 32-Byte-Verschlüsselungsschlüssel (nur in Router-Identitäten) eine Zufallszahl,
die die gesamte für die SHA-256-Hashes dieser Strukturen notwendige Entropie bereitstellt,
damit sie kryptografisch stark und zufällig im Netzwerkdatenbank-DHT verteilt sind.

Aus übertriebener Vorsicht empfehlen wir jedoch,
mindestens 32 Byte zufällige Daten im ElG-öffentlichen Schlüsselfeld und Padding zu verwenden.
Darüber hinaus würde Base 64-Ziele, falls die Felder alle Nullen wären,
lange Folgen von AAAA-Zeichen enthalten,
was Benutzer alarmieren oder verwirren könnte.

Für den Ed25519-Signaturtyp und den X25519-Verschlüsselungstyp:
Ziele enthalten 11 Kopien (352 Bytes) der zufälligen Daten.
Router-Identitäten enthalten 10 Kopien (320 Bytes) der zufälligen Daten.


### Geschätzte Einsparungen

Ziele sind in jedem Streaming-SYN
und antwortbaren Datagramm enthalten.
Router-Infos (die Router-Identitäten enthalten) sind in Datenbank-Store-Nachrichten
und in den Session-bestätigten Nachrichten in NTCP2 und SSU2 enthalten.

NTCP2 komprimiert die Router-Info nicht.
RIs in Datenbank-Store-Nachrichten und SSU2-Session-bestätigten Nachrichten werden gezippt.
Router-Infos werden in reseed-SU3-Dateien gezippt.

Ziele in Datenbank-Store-Nachrichten werden nicht komprimiert.
Streaming-SYN-Nachrichten werden auf der I2CP-Ebene gezippt.

Für den Ed25519-Signaturtyp und den X25519-Verschlüsselungstyp,
geschätzte Einsparungen:

| Datentyp | Gesamtgröße | Schlüssel und Zertifikat | Unkomprimiertes Padding | Komprimiertes Padding | Größe | Einsparungen |
|----------|-------------|-------------------------|------------------------|-----------------------|-------|--------------|
| Ziel | 391 | 39 | 352 | 32 | 71 | 320 Bytes (82%) |
| Router-Identität | 391 | 71 | 320 | 32 | 103 | 288 Bytes (74%) |
| Router-Info | 1000 typ. | 71 | 320 | 32 | 722 typ. | 288 Bytes (29%) |

Hinweise: Annahme, dass 7-Byte-Zertifikat nicht komprimierbar ist, null zusätzlicher Gzip-Overhead.
Beides ist nicht zutreffend, aber die Effekte werden gering sein.
Ignoriert andere komprimierbare Teile der Router-Info.


## Spezifikation

Vorgeschlagene Änderungen an unseren aktuellen Spezifikationen sind im Folgenden dokumentiert.


### Gemeinsame Strukturen
Ändern Sie die Spezifikation der gemeinsamen Strukturen,
um anzugeben, dass das 256-Byte-Ziel öffentliches Schlüsselfeld ignoriert wird und zufällige Daten enthalten kann.

Fügen Sie einen Abschnitt zur Spezifikation der gemeinsamen Strukturen,
der eine bewährte Praxis für das Ziel öffentliches Schlüsselfeld und die
Padding-Felder im Ziel und in der Router-Identität, wie folgt, empfiehlt:

Generieren Sie 32 Byte zufällige Daten mit einem starken kryptographischen Pseudo-Zufallszahlengenerator (PRNG)
und wiederholen Sie diese 32 Byte so oft wie nötig, um das öffentliche Schlüsselfeld (für Ziele)
und das Padding-Feld (für Ziele und Router-Identitäten) zu füllen.

### Private Key Datei
Das Format der Private Key Datei (eepPriv.dat) ist kein offizieller Bestandteil unserer Spezifikationen,
aber es ist in den [Java I2P javadocs](http://idk.i2p/javadoc-i2p/net/i2p/data/PrivateKeyFile.html) dokumentiert
und wird auch von anderen Implementierungen unterstützt.
Dies ermöglicht die Portabilität von privaten Schlüsseln zu verschiedenen Implementierungen.
Fügen Sie eine Anmerkung zu diesem Javadoc hinzu, dass der öffentliche Verschlüsselungsschlüssel zufälliges Padding sein kann
und der private Verschlüsselungsschlüssel null oder zufällige Daten sein kann.

### SAM
Weisen Sie in der SAM-Spezifikation darauf hin, dass der private Verschlüsselungsschlüssel nicht verwendet wird und ignoriert werden kann.
Der Client kann beliebige zufällige Daten zurückgeben.
Die SAM Bridge kann bei der Erstellung (mit DEST GENERATE oder SESSION CREATE DESTINATION=TRANSIENT)
zufällige Daten senden, anstatt alles auf Null zu setzen, damit die Base 64-Repräsentation keine Zeichenfolge von AAAA hat
und gebrochen aussieht.


### I2CP
Keine Änderungen erforderlich für I2CP. Der private Schlüssel für den Verschlüsselungsschlüssel im Ziel wird nicht an den Router gesendet.


## Zukünftige Planung


### Protokolländerungen

Auf Kosten von Protokolländerungen und eines Mangels an Abwärtskompatibilität könnten wir
unsere Protokolle und Spezifikationen ändern, um das Padding-Feld im
Ziel, in der Router-Identität, oder beidem zu eliminieren.

Dieser Vorschlag hat einige Ähnlichkeiten mit dem "b33"-verschlüsselten Leaseset-Format,
das nur einen Schlüssel und ein Typ-Feld enthält.

Um eine gewisse Kompatibilität beizubehalten, könnten bestimmte Protokollschichten das Padding-Feld
mit Nullen "erweitern" und anderen Protokollschichten präsentieren.

Für Ziele könnten wir auch das Verschlüsselungstyp-Feld im Schlüsselzertifikat entfernen,
um zwei Bytes einzusparen.
Alternativ könnten Ziele einen neuen Verschlüsselungstyp im Schlüsselzertifikat erhalten,
der einen Null-Schlüssel (und Padding) anzeigt.

Wird die Kompatibilitätskonvertierung zwischen alten und neuen Formaten nicht auf irgendeiner Protokollschicht einbezogen,
würden die folgenden Spezifikationen, APIs, Protokolle und Anwendungen betroffen sein:

- Gemeinsame Strukturen Spez
- I2NP
- I2CP
- NTCP2
- SSU2
- Ratchet
- Streaming
- SAM
- Bittorrent
- Reseeding
- Private Key Datei
- Java Core und Router API
- i2pd API
- Drittanbieter-SAM-Bibliotheken
- Bündel- und Drittanbieter-Tools
- Mehrere Java-Plugins
- Benutzeroberflächen
- P2P-Anwendungen, z.B. MuWire, Bitcoin, Monero
- hosts.txt, Adressbuch und Abonnements

Wenn die Konvertierung auf irgendeiner Schicht spezifiziert ist, würde die Liste verkleinert werden.

Die Kosten und Vorteile dieser Änderungen sind unklar.

Spezifische Vorschläge TBD:


### PQ-Schlüssel

Post-Quanten (PQ) -Verschlüsselungsschlüssel, für jeden erwarteten Algorithmus,
sind größer als 256 Byte. Dies würde jedes Padding und jede Einsparung aus den oben vorgeschlagenen
Änderungen für Router-Identitäten beseitigen.

In einem "hybriden" PQ-Ansatz, wie es SSL tut, wären die PQ-Schlüssel nur flüchtig,
und würden nicht in der Router-Identität erscheinen.

PQ-Signaturschlüssel sind nicht machbar,
und Ziele enthalten keine Verschlüsselungsschlüssel.
Statische Schlüssel für Ratchet sind im Lease-Set, nicht im Ziel.
also können wir Ziele aus der folgenden Diskussion eliminieren.

PQ betrifft also nur Router-Infos, und nur für PQ-statische (nicht flüchtige) Schlüssel, nicht für PQ-hybrid.
Dies wäre für einen neuen Verschlüsselungstyp und würde NTCP2, SSU2 und
verschlüsselte Datenbankabfragen und -antworten betreffen.
Geschätzter Zeitrahmen für Design, Entwicklung und Einführung dessen wäre ???????????
Aber wäre nach hybriden oder Ratsch ?????????

Für weitere Diskussion siehe [this topic](http://zzz.i2p/topics/3294).


## Probleme

Es könnte wünschenswert sein, das Netzwerk langsam neu zu verschlüsseln, um neuen Routern Deckung zu bieten.
"Neuverteilung" könnte einfach nur bedeuten, das Padding zu ändern und nicht wirklich die Schlüssel zu ändern.

Es ist nicht möglich, vorhandene Ziele neu zu verschlüsseln.

Sollten Router-Identitäten mit Padding im öffentlichen Schlüsselfeld mit einem anderen
Verschlüsselungstyp im Schlüsselzertifikat identifiziert werden? Dies würde Kompatibilitätsprobleme verursachen.


## Migration

Keine Kompatibilitätsprobleme beim Ersetzen des ElGamal-Schlüssels durch Padding.

Neuverteilung, falls implementiert, wäre ähnlich wie bei drei vorherigen Router-Identitätsübergängen:
Von DSA-SHA1 zu ECDSA-Signaturen, dann zu
EdDSA-Signaturen, dann zu X25519-Verschlüsselung.

Vorbehaltlich von Kompatibilitätsproblemen und nach der Deaktivierung von SSU,
können Implementierungen den ElGamal-Code vollständig entfernen.
Etwa 14% der Router im Netzwerk sind ElGamal-Verschlüsselungstyp, einschließlich vieler Floodfills.

Ein Entwurf für eine Merge-Anfrage für Java I2P befindet sich unter [git.idk.i2p](http://git.idk.i2p/i2p-hackers/i2p.i2p/-/merge_requests/66).
