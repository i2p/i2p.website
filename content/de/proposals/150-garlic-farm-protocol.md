---
title: "Garlic Farm-Protokoll"
number: "150"
author: "zzz"
created: "2019-05-02"
lastupdated: "2019-05-20"
status: "Offen"
thread: "http://zzz.i2p/topics/2234"
toc: true
---

## Überblick

Dies ist die Spezifikation für das Garlic Farm-Wire-Protokoll, basierend auf JRaft, seinem "exts"-Code zur Implementierung über TCP und seiner "dmprinter"-Beispielanwendung [JRAFT](https://github.com/datatechnology/jraft). JRaft ist eine Implementierung des Raft-Protokolls [RAFT](https://ramcloud.stanford.edu/wiki/download/attachments/11370504/raft.pdf).

Wir konnten keine Implementierung mit einem dokumentierten Wire-Protokoll finden. Allerdings ist die JRaft-Implementierung einfach genug, dass wir den Code überprüfen und dann sein Protokoll dokumentieren konnten. Dieser Vorschlag ist das Ergebnis dieser Bemühung.

Dies wird das Backend für die Koordination von Routern sein, die Einträge in einem Meta-LeaseSet veröffentlichen. Siehe Vorschlag 123.


## Ziele

- Kleine Codegröße
- Basierend auf bestehender Implementierung
- Keine serialisierten Java-Objekte oder Java-spezifische Funktionen oder Codierungen
- Jegliches Bootstraping ist außerhalb des Umfangs. Es wird angenommen, dass mindestens ein anderer Server fest codiert oder außerhalb dieses Protokolls konfiguriert ist.
- Unterstützung sowohl für Out-of-Band- als auch für In-I2P-Anwendungsfälle.


## Design

Das Raft-Protokoll ist kein konkretes Protokoll; es definiert nur eine Zustandsmaschine. Daher dokumentieren wir das konkrete Protokoll von JRaft und basieren unser Protokoll darauf. Es gibt keine Änderungen am JRaft-Protokoll außer der Hinzufügung eines Authentifizierungs-Handshakes.

Raft wählt einen Leader, dessen Aufgabe es ist, ein Log zu veröffentlichen. Das Log enthält Raft-Konfigurationsdaten und Anwendungsdaten. Die Anwendungsdaten enthalten den Status jedes Serverrouters und das Ziel für den Meta-LS2-Cluster. Die Server verwenden einen gemeinsamen Algorithmus, um den Herausgeber und den Inhalt des Meta LS2 zu bestimmen. Der Herausgeber des Meta LS2 ist NICHT notwendigerweise der Raft-Leader.


## Spezifikation

Das Wire-Protokoll erfolgt über SSL-Sockets oder nicht-SSL-I2P-Sockets. I2P-Sockets werden durch das HTTP-Proxy weitergeleitet. Es gibt keine Unterstützung für Clearnet-nicht-SSL-Sockets.

### Handshake und Authentifizierung

Nicht definiert von JRaft.

Ziele:

- Benutzer-/Passwort-Authentifizierungsmethode
- Versionskennung
- Cluster-Kennung
- Erweiterbar
- Einfachheit des Proxying bei Verwendung für I2P-Sockets
- Server als Garlic Farm-Server nicht unnötig exponieren
- Einfaches Protokoll, damit keine vollständige Webserver-Implementierung erforderlich ist
- Kompatibel mit gängigen Standards, sodass Implementierungen, falls gewünscht, Standardbibliotheken verwenden können

Wir werden einen websocket-ähnlichen Handshake [WEBSOCKET](https://en.wikipedia.org/wiki/WebSocket) und HTTP-Digest-Authentifizierung [RFC-2617](https://tools.ietf.org/html/rfc2617) verwenden. Die RFC 2617-Basic-Authentifizierung wird NICHT unterstützt. Beim Proxying durch den HTTP-Proxy kommunizieren Sie mit dem Proxy wie in [RFC-2616](https://tools.ietf.org/html/rfc2616) spezifiziert.

#### Credentials

Ob Benutzernamen und Passwörter pro Cluster oder pro Server erfolgen, ist implementierungsabhängig.


#### HTTP-Anfrage 1

Der Absender sendet folgendes.

Alle Zeilen werden mit CRLF abgeschlossen, wie von HTTP gefordert.

```text
GET /GarlicFarm/CLUSTER/VERSION/websocket HTTP/1.1
  Host: (ip):(port)
  Cache-Control: no-cache
  Connection: close
  (any other headers ignored)
  (blank line)

  CLUSTER ist der Name des Clusters (Standard "farm")
  VERSION ist die Garlic Farm-Version (derzeit "1")
```


#### HTTP-Antwort 1

Wenn der Pfad nicht korrekt ist, sendet der Empfänger eine standardmäßige "HTTP/1.1 404 Not Found"-Antwort, wie in [RFC-2616](https://tools.ietf.org/html/rfc2616).

Wenn der Pfad korrekt ist, sendet der Empfänger eine standardmäßige "HTTP/1.1 401 Unauthorized"-Antwort, einschließlich des WWW-Authenticate-HTTP-Digest-Authentifizierungs-Headers, wie in [RFC-2617](https://tools.ietf.org/html/rfc2617).

Beide Parteien schließen dann den Socket.


#### HTTP-Anfrage 2

Der Absender sendet folgendes, wie in [RFC-2617](https://tools.ietf.org/html/rfc2617) und [WEBSOCKET](https://en.wikipedia.org/wiki/WebSocket).

Alle Zeilen werden mit CRLF abgeschlossen, wie von HTTP gefordert.

```text
GET /GarlicFarm/CLUSTER/VERSION/websocket HTTP/1.1
  Host: (ip):(port)
  Cache-Control: no-cache
  Connection: keep-alive, Upgrade
  Upgrade: websocket
  (Sec-Websocket-* headers if proxied)
  Authorization: (HTTP-Digest-Authorization-Header gemäß RFC 2617)
  (any other headers ignored)
  (blank line)

  CLUSTER ist der Name des Clusters (Standard "farm")
  VERSION ist die Garlic Farm-Version (derzeit "1")
```


#### HTTP-Antwort 2

Wenn die Authentifizierung nicht korrekt ist, sendet der Empfänger eine weitere standardmäßige "HTTP/1.1 401 Unauthorized"-Antwort, wie in [RFC-2617](https://tools.ietf.org/html/rfc2617).

Wenn die Authentifizierung korrekt ist, sendet der Empfänger die folgende Antwort, wie in [WEBSOCKET](https://en.wikipedia.org/wiki/WebSocket).

Alle Zeilen werden mit CRLF abgeschlossen, wie von HTTP gefordert.

```text
HTTP/1.1 101 Switching Protocols
  Connection: Upgrade
  Upgrade: websocket
  (Sec-Websocket-* headers)
  (any other headers ignored)
  (blank line)
```

Nach dieser Empfang bleibt der Socket offen. Das nachstehend definierte Raft-Protokoll wird über denselben Socket gestartet.


#### Caching

Anmeldeinformationen sollen mindestens eine Stunde im Cache gespeichert werden, sodass nachfolgende Verbindungen direkt zur "HTTP-Anfrage 2" oben springen können.


### Nachrichtentypen

Es gibt zwei Arten von Nachrichten, Anfragen und Antworten. Anfragen können Log-Einträge enthalten und sind variabel groß; Antworten enthalten keine Log-Einträge und sind fest groß.

Nachrichtentypen 1-4 sind die Standard-RPC-Nachrichten, die von Raft definiert sind. Dies ist das Kern-Raft-Protokoll.

Nachrichtentypen 5-15 sind die erweiterten RPC-Nachrichten, die von JRaft definiert sind, um Clients, dynamische Serveränderungen und effiziente Logsynchronisation zu unterstützen.

Nachrichtentypen 16-17 sind die Log-Kompressions-RPC-Nachrichten, die in Raft Abschnitt 7 definiert sind.


| Nachricht | Nummer | gesendet von | gesendet an | Hinweise |
| :--- | :--- | :--- | :--- | :--- |
| RequestVoteRequest | 1 | Kandidat | Follower | Standard Raft RPC; darf keine Log-Einträge enthalten |
| RequestVoteResponse | 2 | Follower | Kandidat | Standard Raft RPC |
| AppendEntriesRequest | 3 | Leader | Follower | Standard Raft RPC |
| AppendEntriesResponse | 4 | Follower | Leader / Client | Standard Raft RPC |
| ClientRequest | 5 | Client | Leader / Follower | Antwort ist AppendEntriesResponse; darf nur Anwendungs-Log-Einträge enthalten |
| AddServerRequest | 6 | Client | Leader | Muss nur einen ClusterServer-Log-Eintrag enthalten |
| AddServerResponse | 7 | Leader | Client | Leader wird auch eine JoinClusterRequest senden |
| RemoveServerRequest | 8 | Follower | Leader | Muss nur einen ClusterServer-Log-Eintrag enthalten |
| RemoveServerResponse | 9 | Leader | Follower | |
| SyncLogRequest | 10 | Leader | Follower | Muss nur einen LogPack-Log-Eintrag enthalten |
| SyncLogResponse | 11 | Follower | Leader | |
| JoinClusterRequest | 12 | Leader | Neuer Server | Einladung zum Beitritt; muss nur einen Konfigurations-Log-Eintrag enthalten |
| JoinClusterResponse | 13 | Neuer Server | Leader | |
| LeaveClusterRequest | 14 | Leader | Follower | Befehl zum Verlassen |
| LeaveClusterResponse | 15 | Follower | Leader | |
| InstallSnapshotRequest | 16 | Leader | Follower | Raft Abschnitt 7; muss nur einen SnapshotSyncRequest-Log-Eintrag enthalten |
| InstallSnapshotResponse | 17 | Follower | Leader | Raft Abschnitt 7 |


### Etablierung

Nach dem HTTP-Handshake ist die Einrichtungssequenz wie folgt:

```text
Neue Serverin Alice            Zufälliger Follower Bob

  ClientRequest   ------->
          <---------   AppendEntriesResponse

  Wenn Bob sagt, er sei der Leader, weiter wie unten. Andernfalls muss Alice die Verbindung zu Bob trennen und sich mit dem Leader verbinden.


  Neue Serverin Alice            Leader Charlie

  ClientRequest   ------->
          <---------   AppendEntriesResponse
  AddServerRequest   ------->
          <---------   AddServerResponse
          <---------   JoinClusterRequest
  JoinClusterResponse  ------->
          <---------   SyncLogRequest
                       ODER InstallSnapshotRequest
  SyncLogResponse  ------->
  ODER InstallSnapshotResponse
```

Trennsequenz:

```text
Followerin Alice            Leader Charlie

  RemoveServerRequest   ------->
          <---------   RemoveServerResponse
          <---------   LeaveClusterRequest
  LeaveClusterResponse  ------->
```

Wahlsequenz:

```text
Kandidatin Alice               Follower Bob

  RequestVoteRequest   ------->
          <---------   RequestVoteResponse

  Wenn Alice die Wahl gewinnt:

  Leiterin Alice                Follower Bob

  AppendEntriesRequest   ------->
  (Herzschlag)
          <---------   AppendEntriesResponse
```


### Definitionen

- Quelle: Identifiziert den Ursprungsort der Nachricht
- Ziel: Identifiziert den Empfänger der Nachricht
- Begriffe: Siehe Raft. Initialisiert auf 0, steigt monoton
- Indizes: Siehe Raft. Initialisiert auf 0, steigt monoton


### Anfragen

Anfragen enthalten einen Header und null oder mehr Log-Einträge. Anfragen haben einen Header mit fester Größe und optionale Logs-Einträge variabler Größe.


#### Anfrageheader

Der Anfrageheader ist 45 Bytes groß, wie folgt. Alle Werte sind unsigned Big-Endian.

```dataspec
Nachrichtentyp:         1 Byte
  Quelle:                 ID, 4-Byte-Integer
  Ziel:                   ID, 4-Byte-Integer
  Begriff:                Aktueller Begriff (siehe Anmerkungen), 8-Byte-Integer
  Letzter Log-Begriff:    8-Byte-Integer
  Letzter Log-Index:      8-Byte-Integer
  Bestätigungsindex:      8-Byte-Integer
  Log-Eintragsgröße:      Gesamte Größe in Bytes, 4-Byte-Integer
  Log-Einträge:           siehe unten, Gesamtlänge wie angegeben
```


#### Anmerkungen

Im RequestVoteRequest ist Begriff der Begriff des Kandidaten. Andernfalls ist es der aktuelle Begriff des Leaders.

Im AppendEntriesRequest, wenn die Log-Eintragsgröße null ist, ist diese Nachricht eine Herzschlag (Keepalive)-Nachricht.


#### Logs-Einträge

Das Log enthält null oder mehr Log-Einträge. Jeder Log-Eintrag ist wie folgt. Alle Werte sind unsigned Big-Endian.

```dataspec
Begriff:        8-Byte-Integer
  Werttyp:        1 Byte
  Eintragsgröße:  In Bytes, 4-Byte-Integer
  Eintrag:        Länge wie angegeben
```


#### Log-Inhalt

Alle Werte sind unsigned Big-Endian.

| Log-Werttyp | Nummer |
| :--- | :--- |
| Anwendung | 1 |
| Konfiguration | 2 |
| ClusterServer | 3 |
| LogPack | 4 |
| SnapshotSyncRequest | 5 |


#### Anwendung

Anwendungsinhalte sind UTF-8-codiert [JSON](https://www.json.org/). Siehe den Abschnitt Anwendungsebene unten.


#### Konfiguration

Dies wird verwendet, damit der Leader eine neue Clusterkonfiguration serialisiert und an Peers repliziert. Es enthält null oder mehr ClusterServer-Konfigurationen.


```dataspec
Log-Index:   8-Byte-Integer
  Letzter Log-Index:   8-Byte-Integer
  ClusterServer-Daten für jeden Server:
    ID:                4-Byte-Integer
    Endpunkt-Datenlänge: In Bytes, 4-Byte-Integer
    Endpunkt-Daten:     ASCII-String der Form "tcp://localhost:9001", Länge wie angegeben
```


#### ClusterServer

Die Konfigurationsinformationen für einen Server in einem Cluster. Dies ist nur in einer AddServerRequest- oder RemoveServerRequest-Nachricht enthalten.

Verwendet in einer AddServerRequest-Nachricht:

```dataspec
ID:                4-Byte-Integer
  Endpunkt-Datenlänge: In Bytes, 4-Byte-Integer
  Endpunkt-Daten:      ASCII-String der Form "tcp://localhost:9001", Länge wie angegeben
```


Verwendet in einer RemoveServerRequest-Nachricht:

```dataspec
ID:                4-Byte-Integer
```


#### LogPack

Dies ist nur in einer SyncLogRequest-Nachricht enthalten.

Folgendes wird vor der Übertragung komprimiert:

```dataspec
Index-Datenlänge: In Bytes, 4-Byte-Integer
  Log-Datenlänge:   In Bytes, 4-Byte-Integer
  Index-Daten:      8 Bytes für jeden Index, Länge wie angegeben
  Log-Daten:        Länge wie angegeben
```


#### SnapshotSyncRequest

Dies ist nur in einer InstallSnapshotRequest-Nachricht enthalten.

```dataspec
Letzter Log-Index:   8-Byte-Integer
  Letzter Log-Begriff:  8-Byte-Integer
  Konfigurationsdatenlänge: In Bytes, 4-Byte-Integer
  Konfigurationsdaten:     Länge wie angegeben
  Versatz:          Der Versatz der Daten in der Datenbank, in Bytes, 8-Byte-Integer
  Datenlänge:       In Bytes, 4-Byte-Integer
  Daten:            Länge wie angegeben
  Ist abgeschlossen: 1 falls abgeschlossen, 0 falls nicht (1 Byte)
```


### Antworten

Alle Antworten sind 26 Bytes groß, wie folgt. Alle Werte sind unsigned Big-Endian.

```dataspec
Nachrichtentyp:  1 Byte
  Quelle:          ID, 4-Byte-Integer
  Ziel:            Normalerweise die tatsächliche Ziel-ID (siehe Anmerkungen), 4-Byte-Integer
  Begriff:         Aktueller Begriff, 8-Byte-Integer
  Nächster Index:  Initialisiert auf den letzten Log-Index des Leaders + 1, 8-Byte-Integer
  Ist angenommen:  1 falls angenommen, 0 falls nicht (siehe Anmerkungen), 1 Byte
```


#### Anmerkungen

Die Ziel-ID ist normalerweise das tatsächliche Ziel für diese Nachricht. Für AppendEntriesResponse, AddServerResponse und RemoveServerResponse ist es jedoch die ID des aktuellen Leaders.

Im RequestVoteResponse ist "Ist angenommen" 1 für eine Stimme für den Kandidaten (Anforderer) und 0 für keine Stimme.


## Anwendungsebene

Jeder Server veröffentlicht regelmäßig Anwendungsdaten im Log in einer ClientRequest. Anwendungsdaten enthalten den Status jedes Serverrouters und das Ziel für den Meta-LS2-Cluster. Die Server verwenden einen gemeinsamen Algorithmus, um den Herausgeber und den Inhalt des Meta LS2 zu bestimmen. Der Server mit dem "besten" aktuellen Status im Log ist der Herausgeber des Meta-LS2. Der Herausgeber des Meta LS2 ist NICHT notwendigerweise der Raft-Leader.


### Inhalte der Anwendungsdaten

Anwendungsinhalte sind UTF-8-codiert [JSON](https://www.json.org/), der Einfachheit und Erweiterbarkeit halber. Die vollständige Spezifikation ist TBD. Das Ziel ist es, genügend Daten zur Verfügung zu stellen, um einen Algorithmus zu schreiben, der den "besten" Router zur Veröffentlichung des Meta LS2 bestimmt, und für den Herausgeber, genügend Informationen zu haben, um die Ziele im Meta LS2 zu gewichten. Die Daten enthalten sowohl Router- als auch Zielstatistiken.

Die Daten können optional Fernerkundungsdaten über die Gesundheit der anderen Server und die Möglichkeit, das Meta LS abzurufen, enthalten. Diese Daten würden in der ersten Veröffentlichung nicht unterstützt werden.

Die Daten können optional Konfigurationsinformationen enthalten, die von einem Administrator-Client veröffentlicht werden. Diese Daten würden in der ersten Veröffentlichung nicht unterstützt werden.

Wenn "name: value" aufgeführt ist, spezifiziert dies den JSON-Map-Schlüssel und -Wert. Andernfalls ist die Spezifikation TBD.


Cluster-Daten (oberste Ebene):

- cluster: Cluster-Name
- date: Datum dieser Daten (long, ms seit der Epoche)
- id: Raft ID (Integer)

Konfigurationsdaten (config):

- Jegliche Konfigurationsparameter

MetaLS-Veröffentlichungsstatus (meta):

- destination: die Metalls-Destination, Base64
- lastPublishedLS: falls vorhanden, Base64-Codierung des zuletzt veröffentlichten Metalls
- lastPublishedTime: in ms oder 0, falls niemals
- publishConfig: Publisher-Konfigurationsstatus aus/an/auto
- publishing: Metalls-Publisher-Status Boolescher Wert wahr/falsch

Router-Daten (router):

- lastPublishedRI: falls vorhanden, Base64-Codierung der zuletzt veröffentlichten Router-Info
- uptime: Betriebszeit in ms
- Jobverzögerung
- Erkundungstunnel
- Beteiligte Tunnel
- Konfigurierte Bandbreite
- Aktuelle Bandbreite

Ziele (destinations):
Liste

Zieldaten:

- destination: das Ziel, Base64
- uptime: Betriebszeit in ms
- Konfigurierte Tunnel
- Aktuelle Tunnel
- Konfigurierte Bandbreite
- Aktuelle Bandbreite
- Konfigurierte Verbindungen
- Aktuelle Verbindungen
- Blacklist-Daten

Remote-Router-Sensorikdaten:

- Letzte gesehene RI-Version
- LS Abrufzeit
- Verbindungstestdaten
- Profil-Daten der nächsten Floodfills für die Zeiträume gestern, heute und morgen

Remote-Ziel-Sensorikdaten:

- Letzte gesehene LS-Version
- LS Abrufzeit
- Verbindungstestdaten
- Profil-Daten der nächsten Floodfills für die Zeiträume gestern, heute und morgen

Meta LS-Sensorikdaten:

- Letzte gesehene Version
- Abrufzeit
- Profil-Daten der nächsten Floodfills für die Zeiträume gestern, heute und morgen


## Verwaltungsinterface

TBD, möglicherweise ein separater Vorschlag. Nicht erforderlich für die erste Veröffentlichung.

Anforderungen eines Admin-Interfaces:

- Unterstützung für mehrere Master-Ziele, d.h. mehrere virtuelle Cluster (Farmen)
- Umfassende Übersicht über den gemeinsam genutzten Cluster-Zustand bieten - alle von den Mitgliedern veröffentlichten Statistiken, wer ist der aktuelle Leader usw.
- Möglichkeit, einen Teilnehmer oder Leader aus dem Cluster zu entfernen
- Möglichkeit, die Veröffentlichung von MetaLS zu erzwingen (wenn aktueller Knoten Herausgeber ist)
- Möglichkeit, Hashes aus MetaLS auszuschließen (wenn aktueller Knoten Herausgeber ist)
- Import-/Export-Funktionalität für Konfigurationen für Massenbereitstellungen


## Router-Interface

TBD, möglicherweise ein separater Vorschlag. i2pcontrol ist in der ersten Veröffentlichung nicht erforderlich und detaillierte Änderungen werden in einem separaten Vorschlag enthalten sein.

Anforderungen für Garlic Farm an Router-API (in-JVM Java oder i2pcontrol)

- getLocalRouterStatus()
- getLocalLeafHash(Hash masterHash)
- getLocalLeafStatus(Hash leaf)
- getRemoteMeasuredStatus(Hash masterOrLeaf) // wahrscheinlich nicht im MVP
- publishMetaLS(Hash masterHash, List<MetaLease> contents) // oder signiertes MetaLeaseSet? Wer unterschreibt?
- stopPublishingMetaLS(Hash masterHash)
- Authentifizierung TBD?


## Begründung

Atomix ist zu groß und erlaubt keine Anpassung, um das Protokoll über I2P zu leiten. Außerdem ist sein Wire-Format undokumentiert und hängt von der Java-Serialisierung ab.


## Anmerkungen


## Probleme

- Es gibt keine Möglichkeit für einen Client, von einem unbekannten Leader zu erfahren und sich mit ihm zu verbinden. Es wäre eine kleine Änderung, wenn ein Follower die Konfiguration als Log-Eintrag in der AppendEntriesResponse senden würde.


## Migration

Keine Abwärtskompatibilitätsprobleme.


## Referenzen

* [JRAFT](https://github.com/datatechnology/jraft)
* [JSON](https://json.org/)
* [RAFT](https://ramcloud.stanford.edu/wiki/download/attachments/11370504/raft.pdf)
* [RFC-2616](https://tools.ietf.org/html/rfc2616)
* [RFC-2617](https://tools.ietf.org/html/rfc2617)
* [WEBSOCKET](https://en.wikipedia.org/wiki/WebSocket)
