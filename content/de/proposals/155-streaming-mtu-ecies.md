---
title: "Streaming MTU für ECIES-Ziele"
number: "155"
author: "zzz"
created: "2020-05-06"
lastupdated: "2020-05-30"
status: "Geschlossen"
thread: "http://zzz.i2p/topics/2886"
target: "0.9.47"
implementedin: "0.9.47"
toc: true
---

## Hinweis
Netzwerkbereitstellung und -tests laufen.
Unterliegt geringfügigen Änderungen.


## Überblick


### Zusammenfassung

ECIES reduziert den Overhead bestehender Sitzung (ES) Nachrichten um etwa 90 Bytes.
Deshalb können wir das MTU für ECIES-Verbindungen um etwa 90 Bytes erhöhen.
Siehe the [ECIES specification](/docs/specs/ecies/#overhead), [Streaming specification](/docs/specs/streaming/#flags-and-option-data-fields), and [Streaming API documentation](/docs/api/streaming/).

Ohne die Erhöhung des MTU werden in vielen Fällen die Overhead-Einsparungen nicht wirklich „eingespart“, 
da die Nachrichten ohnehin auf die Nutzung von zwei vollständigen Tunnel-Nachrichten aufgefüllt werden.

Dieser Vorschlag erfordert keine Änderung der Spezifikationen.
Er wird ausschließlich als Vorschlag veröffentlicht, um Diskussionen und Konsensbildung 
über den empfohlenen Wert und die Implementierungsdetails zu erleichtern.


### Ziele

- Erhöhung des ausgehandelten MTU
- Maximierung der Nutzung von 1 KB Tunnel-Nachrichten
- Keine Änderung des Streaming-Protokolls


## Design

Verwendung der vorhandenen MAX_PACKET_SIZE_INCLUDED-Option und MTU-Aushandlung.
Streaming nutzt weiterhin das Minimum des gesendeten und empfangenen MTU.
Der Standardwert bleibt 1730 für alle Verbindungen, unabhängig von den verwendeten Schlüsseln.

Implementierungen werden ermutigt, die MAX_PACKET_SIZE_INCLUDED-Option in alle SYN-Pakete in beide Richtungen einzuschließen,
obwohl dies nicht erforderlich ist.

Wenn ein Ziel nur ECIES ist, verwenden Sie den höheren Wert (entweder als Alice oder Bob).
Wenn ein Ziel dual-key ist, kann das Verhalten variieren:

Wenn der Dual-Key-Client außerhalb des Routers (in einer externen Anwendung) ist,
kann er den verwendeten Schlüssel am fernen Ende nicht "kennen", und Alice kann 
einen höheren Wert im SYN anfordern, während die maximalen Daten im SYN bei 1730 bleiben.

Wenn der Dual-Key-Client innerhalb des Routers ist, kann die Information, welcher Schlüssel 
verwendet wird, dem Client bekannt oder unbekannt sein.
Die Leaseset wurde möglicherweise noch nicht abgerufen, oder die internen API-Schnittstellen 
können diese Information dem Client nicht leicht zugänglich machen.
Wenn die Information verfügbar ist, kann Alice den höheren Wert verwenden;
ansonsten muss Alice den Standardwert von 1730 verwenden, bis ausgehandelt wird.

Ein Dual-Key-Client als Bob kann den höheren Wert als Antwort senden,
selbst wenn kein Wert oder ein Wert von 1730 von Alice empfangen wurde;
es gibt jedoch keine Bestimmung zur nachträglichen Aushandlung im Streaming,
sodass das MTU bei 1730 bleiben sollte.


Wie in the [Streaming API documentation](/docs/api/streaming/) erwähnt,
können die Daten in den von Alice an Bob gesendeten SYN-Paketen Bobs MTU überschreiten.
Dies ist eine Schwäche im Streaming-Protokoll.
Daher müssen Dual-Key-Clients die Daten in den gesendeten SYN-Paketen
auf 1730 Bytes begrenzen, während sie eine höhere MTU-Option senden.
Sobald die höhere MTU von Bob empfangen wurde, kann Alice die tatsächliche maximale
Nutzlast erhöhen.


### Analyse

Wie in the [ECIES specification](/docs/specs/ecies/#overhead) beschrieben, beträgt der ElGamal-Overhead für bestehende Sitzung-Nachrichten
151 Bytes und der Ratchet-Overhead 69 Bytes.
Daher können wir das MTU für Ratchet-Verbindungen um (151 - 69) = 82 Bytes erhöhen,
von 1730 auf 1812.


## Spezifikation

Fügen Sie die folgenden Änderungen und Klarstellungen zum Abschnitt MTU-Auswahl und -Aushandlung von the [Streaming API documentation](/docs/api/streaming/) hinzu.
Keine Änderungen an the [Streaming specification](/docs/specs/streaming/).


Der Standardwert der Option i2p.streaming.maxMessageSize bleibt 1730 für alle Verbindungen, unabhängig von den verwendeten Schlüsseln.
Clients müssen wie üblich das Minimum aus gesendeten und empfangenen MTU verwenden.

Es gibt vier verwandte MTU-Konstanten und Variablen:

- DEFAULT_MTU: 1730, unverändert, für alle Verbindungen
- i2cp.streaming.maxMessageSize: Standard 1730 oder 1812, kann durch Konfiguration geändert werden
- ALICE_SYN_MAX_DATA: Die maximalen Daten, die Alice in ein SYN-Paket aufnehmen kann
- negotiated_mtu: Das Minimum aus Alice's und Bob's MTU, zu verwenden als Maximal-Datengröße
  im SYN ACK von Bob zu Alice und in allen nachfolgenden gesendeten Paketen in beide Richtungen


Es gibt fünf zu berücksichtigende Fälle:


### 1) Alice nur ElGamal
Keine Änderung, 1730 MTU in allen Paketen.

- ALICE_SYN_MAX_DATA = 1730
- i2cp.streaming.maxMessageSize Standard: 1730
- Alice kann MAX_PACKET_SIZE_INCLUDED im SYN senden, nicht erforderlich, es sei denn != 1730


### 2) Alice nur ECIES
1812 MTU in allen Paketen.

- ALICE_SYN_MAX_DATA = 1812
- i2cp.streaming.maxMessageSize Standard: 1812
- Alice muss MAX_PACKET_SIZE_INCLUDED im SYN senden


### 3) Alice Dual-Key und weiß, dass Bob ElGamal ist
1730 MTU in allen Paketen.

- ALICE_SYN_MAX_DATA = 1730
- i2cp.streaming.maxMessageSize Standard: 1812
- Alice kann MAX_PACKET_SIZE_INCLUDED im SYN senden, nicht erforderlich, es sei denn != 1730


### 4) Alice Dual-Key und weiß, dass Bob ECIES ist
1812 MTU in allen Paketen.

- ALICE_SYN_MAX_DATA = 1812
- i2cp.streaming.maxMessageSize Standard: 1812
- Alice muss MAX_PACKET_SIZE_INCLUDED im SYN senden


### 5) Alice Dual-Key und Bob-Schlüssel ist unbekannt
Senden Sie 1812 als MAX_PACKET_SIZE_INCLUDED im SYN-Paket, aber begrenzen Sie die SYN-Paketdaten auf 1730.

- ALICE_SYN_MAX_DATA = 1730
- i2cp.streaming.maxMessageSize Standard: 1812
- Alice muss MAX_PACKET_SIZE_INCLUDED im SYN senden


### Für alle Fälle

Alice und Bob berechnen
negotiated_mtu, das Minimum aus Alice's und Bob's MTU, zu verwenden als Maximal-Datengröße
im SYN ACK von Bob zu Alice und in allen nachfolgenden gesendeten Paketen in beide Richtungen.


## Rechtfertigung

Siehe the [Java I2P source code](https://github.com/i2p/i2p.i2p/blob/master/apps/streaming/java/src/net/i2p/client/streaming/impl/ConnectionOptions.java#L220) für den Grund, warum der aktuelle Wert 1730 ist.
Siehe the [ECIES specification](/docs/specs/ecies/#overhead) für den Grund, warum der ECIES-Overhead 82 Bytes weniger als ElGamal ist.


## Implementierungshinweise

Wenn Streaming Nachrichten optimaler Größe erstellt, ist es sehr wichtig, dass
die ECIES-Ratchet-Schicht nicht über diese Größe hinaus auffüllt.

Die optimale Größe einer Garlic-Nachricht zur Anpassung in zwei Tunnel-Nachrichten,
einschließlich der 16-Byte-Garlic-Nachricht I2NP-Header, 4-Byte-Garlic-Nachricht Länge,
8-Byte-ES-Tag und 16-Byte-MAC, beträgt 1956 Bytes.

Ein empfohlenes Auffüllungs-Algorithmus in ECIES ist wie folgt:

- Wenn die Gesamtlänge der Garlic-Nachricht 1954-1956 Bytes betragen würde,
  keinen Auffüllblock hinzufügen (kein Platz)
- Wenn die Gesamtlänge der Garlic-Nachricht 1938-1953 Bytes betragen würde,
  einen Auffüllblock hinzufügen, um genau auf 1956 Bytes zu kommen.
- Andernfalls wie gewohnt auffüllen, beispielsweise mit einer zufälligen Menge von 0-15 Bytes.

Ähnliche Strategien könnten bei der optimalen Ein-Tunnel-Nachricht-Größe (964)
und der Drei-Tunnel-Nachricht-Größe (2952) verwendet werden, obwohl diese Größen in der Praxis selten sein sollten.


## Probleme

Der Wert 1812 ist vorläufig. Er muss bestätigt und möglicherweise angepasst werden.


## Migration

Keine Rückwärtskompatibilitätsprobleme.
Dies ist eine bestehende Option und MTU-Aushandlung ist bereits Teil der Spezifikation.

Ältere ECIES-Ziele unterstützen 1730.
Jeder Client, der einen höheren Wert erhält, wird mit 1730 antworten, und das ferne Ende
wird abwärts verhandeln, wie üblich.


