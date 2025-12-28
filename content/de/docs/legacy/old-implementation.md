---
title: "Alte Tunnel-Implementierung (Legacy)"
description: "Archivierte Beschreibung des vor I2P 0.6.1.10 verwendeten tunnel-Designs."
slug: "old-implementation"
lastUpdated: "2005-06"
accurateFor: "0.6.1"
reviewStatus: "needs-review"
---

> **Legacy-Status:** Dieser Inhalt wird ausschließlich als historische Referenz vorgehalten. Er dokumentiert das tunnel system, das vor I2P&nbsp;0.6.1.10 ausgeliefert wurde, und sollte nicht für moderne Entwicklung verwendet werden. Hinweise für den produktiven Einsatz finden Sie in der [aktuellen Implementierung](/docs/specs/implementation/).

Das ursprüngliche tunnel-Subsystem verwendete ebenfalls unidirektionale tunnel, unterschied sich jedoch beim Nachrichtenlayout, bei der Duplikaterkennung und bei der Aufbaustrategie. Viele der nachfolgenden Abschnitte orientieren sich an der Struktur des als veraltet markierten Dokuments, um den Vergleich zu erleichtern.

## 1. Tunnel-Übersicht

- Tunnels wurden als geordnete Sequenzen von vom Ersteller ausgewählten Peers aufgebaut.
- Die Tunnel-Längen reichten von 0–7 Hops, mit mehreren Einstellmöglichkeiten für Padding, Drosselung und die Erzeugung von chaff (Täuschdaten).
- Eingehende Tunnels lieferten Nachrichten von einem nicht vertrauenswürdigen Gateway an den Ersteller (Endpunkt); ausgehende Tunnels leiteten Daten vom Ersteller weg.
- Die Lebensdauer der Tunnels betrug 10 Minuten; danach wurden neue Tunnels aufgebaut (oft mit denselben Peers, aber unterschiedlichen Tunnel-IDs).

## 2. Betrieb im Legacy-Design

### 2.1 Nachrichtenvorverarbeitung

Gateways sammelten ≤32&nbsp;KB an I2NP-Nutzlast, wählten Padding aus und erzeugten eine Nutzlast, die Folgendes enthielt:

- Ein 2-Byte-Feld für die Padding-Länge und entsprechend viele Zufallsbytes
- Eine Folge von `{instructions, I2NP message}`-Paaren, die Zustellziele, Fragmentierung und optionale Verzögerungen beschreiben
- Vollständige I2NP-Nachrichten, aufgefüllt bis zur 16-Byte-Grenze

Zustellanweisungen packten Routing-Informationen in Bitfelder (Zustelltyp, Verzögerungs-Flags, Fragmentierungs-Flags und optionale Erweiterungen). Fragmentierte Nachrichten enthielten eine 4-Byte-Nachrichten-ID sowie ein Index-/Letztes-Fragment-Flag.

### 2.2 Gateway-Verschlüsselung

Das Legacy-Design fixierte die tunnel-Länge für die Verschlüsselungsphase auf acht Hops. Gateways schichteten AES-256/CBC- sowie Prüfsummenblöcke aufeinander, sodass jeder Hop die Integrität prüfen konnte, ohne die Nutzlast zu verkleinern. Die Prüfsumme selbst war ein aus SHA-256 abgeleiteter Block, der in die Nachricht eingebettet war.

### 2.3 Teilnehmerverhalten

Die Teilnehmer verfolgten eingehende tunnel-IDs, überprüften die Integrität frühzeitig und verwarfen Duplikate vor dem Weiterleiten. Da Padding- und Verifizierungsblöcke eingebettet waren, blieb die Nachrichtengröße unabhängig von der Anzahl der Hops konstant.

### 2.4 Verarbeitung am Endpunkt

Die Endpunkte entschlüsselten die mehrschichtigen Blöcke sequenziell, validierten die Prüfsummen und spalteten die Nutzlast wieder in die kodierten Anweisungen sowie I2NP-Nachrichten zur Weiterleitung.

## 3. Tunnelaufbau (veralteter Prozess)

1. **Peer-Auswahl:** Peers wurden aus lokal gepflegten Profilen (exploratory vs. client) ausgewählt. Das ursprüngliche Dokument betonte bereits die Abmilderung des [Predecessor-Angriffs](https://en.wikipedia.org/wiki/Predecessor_attack) durch die Wiederverwendung geordneter Peer-Listen pro tunnel pool.
2. **Zustellung von Anfragen:** Build-Nachrichten wurden Hop-by-Hop weitergeleitet, mit verschlüsselten Abschnitten für jeden Peer. Alternative Ideen wie telescopic extension (teleskopische Erweiterung), midstream rerouting (Umleitung in der Mitte der Kette) oder das Entfernen von Prüfsummenblöcken wurden als Experimente diskutiert, aber nie übernommen.
3. **Pooling:** Jede lokale Destination hielt separate eingehende und ausgehende Pools. Einstellungen umfassten gewünschte Anzahl, Backup tunnels, Längenvarianz, Drosselung und Padding-Richtlinien.

## 4. Drosselungs- und Mischkonzepte

Die ältere Ausarbeitung schlug mehrere Strategien vor, die spätere Releases prägten:

- Weighted Random Early Discard (WRED, gewichtete zufällige Frühverwerfung) zur Staukontrolle
- Pro-Tunnel-Drosselungen auf Basis gleitender Mittelwerte der jüngsten Nutzung
- Optionale Steuerungen für chaff (Füllverkehr) und batching (Stapelbildung) (noch nicht vollständig implementiert)

## 5. Archivierte Alternativen

Abschnitte des ursprünglichen Dokuments behandelten Ideen, die nie eingesetzt wurden:

- Entfernen von Prüfsummenblöcken, um die pro Hop anfallende Verarbeitung zu reduzieren
- Teleskopieren von tunnels im laufenden Betrieb, um die Peer-Zusammensetzung zu ändern
- Wechsel zu bidirektionalen tunnels (letztlich verworfen)
- Verwendung kürzerer Hashes oder anderer Padding-Verfahren (Auffüllungsverfahren)

Diese Ideen stellen weiterhin einen wertvollen historischen Kontext dar, spiegeln jedoch die moderne Codebasis nicht wider.

## Referenzen

- Ursprüngliches Legacy-Dokumentarchiv (vor 0.6.1.10)
- [Tunnel-Übersicht](/docs/overview/tunnel-routing/) für die aktuelle Terminologie
- [Peer-Profiling und -Auswahl](/docs/overview/tunnel-routing#peer-selection/) für moderne Heuristiken
