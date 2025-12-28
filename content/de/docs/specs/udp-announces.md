---
title: "UDP-BitTorrent-Announce-Anfragen"
description: "Protokollspezifikation für UDP-basierte BitTorrent-Tracker-Announces (Anfragen) in I2P"
slug: "udp-announces"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Überblick

Diese Spezifikation dokumentiert das Protokoll für UDP-BitTorrent-Announce-Anfragen (Tracker-Anfragen) in I2P. Für die allgemeine Spezifikation von BitTorrent in I2P siehe die [Dokumentation zu BitTorrent über I2P](/docs/applications/bittorrent/). Für Hintergrund und zusätzliche Informationen zur Entwicklung dieser Spezifikation siehe [Proposal 160](/proposals/160-udp-trackers/).

Dieses Protokoll wurde am 24. Juni 2025 formell genehmigt und in I2P Version 2.10.0 (API 0.9.67) implementiert, veröffentlicht am 8. September 2025. Die UDP-Tracker-Unterstützung ist derzeit im I2P-Netzwerk in Betrieb, mit mehreren produktiven Trackern und vollständiger Unterstützung im i2psnark-Client.

## Entwurf

Diese Spezifikation verwendet antwortfähige Datagram2, antwortfähige Datagram3 und Roh-Datagramme, wie in der [I2P Datagram Specification](/docs/api/datagrams/) definiert. Datagram2 und Datagram3 sind Varianten antwortfähiger Datagramme, definiert in [Proposal 163](/proposals/163-datagram2/). Datagram2 fügt Schutz vor Replay-Angriffen und Unterstützung für Offline-Signaturen hinzu. Datagram3 ist kleiner als das alte Datagrammformat, jedoch ohne Authentifizierung.

### BEP 15

Zur Orientierung ist der in [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) definierte Nachrichtenfluss wie folgt:

```
Client                        Tracker
  Connect Req. ------------->
    <-------------- Connect Resp.
  Announce Req. ------------->
    <-------------- Announce Resp.
  Announce Req. ------------->
    <-------------- Announce Resp.
```
Die Connect-Phase ist erforderlich, um IP-Adress-Spoofing zu verhindern. Der Tracker gibt eine Verbindungs-ID zurück, die der Client in nachfolgenden Announce-Anfragen verwendet. Diese Verbindungs-ID läuft standardmäßig beim Client nach einer Minute ab und beim Tracker nach zwei Minuten.

I2P verwendet denselben Nachrichtenfluss wie BEP 15, um die Übernahme in bestehenden UDP-fähigen Client-Codebasen zu erleichtern, aus Effizienzgründen und aus den nachfolgend erläuterten Sicherheitsgründen:

```
Client                        Tracker
  Connect Req. ------------->       (Repliable Datagram2)
    <-------------- Connect Resp.   (Raw)
  Announce Req. ------------->      (Repliable Datagram3)
    <-------------- Announce Resp.  (Raw)
  Announce Req. ------------->      (Repliable Datagram3)
    <-------------- Announce Resp.  (Raw)
           ...
```
Dies ermöglicht potenziell erhebliche Bandbreiteneinsparungen gegenüber Ankündigungen per Streaming (TCP). Während das Datagram2 (Datagramm-Typ 2) ungefähr die gleiche Größe wie ein Streaming-SYN hat, ist die rohe Antwort deutlich kleiner als das Streaming-SYN-ACK. Nachfolgende Anfragen verwenden Datagram3 (Datagramm-Typ 3), und die nachfolgenden Antworten sind roh.

Die Announce-Anfragen werden als Datagram3 (Datagramm-Version 3) gesendet, damit der Tracker keine große Zuordnungstabelle von Verbindungs-IDs zu Announce-Ziel oder Hash vorhalten muss. Stattdessen kann der Tracker die Verbindungs-IDs kryptografisch aus dem Sender-Hash, dem aktuellen Zeitstempel (basierend auf einem bestimmten Intervall) und einem geheimen Wert erzeugen. Wenn eine Announce-Anfrage eingeht, überprüft der Tracker die Verbindungs-ID und verwendet anschließend den Datagram3-Sender-Hash als Sendeziel.

### Lebensdauer der Verbindung

[BEP 15](http://www.bittorrent.org/beps/bep_0015.html) legt fest, dass die Verbindungs-ID beim Client nach einer Minute und beim Tracker nach zwei Minuten abläuft. Das ist nicht konfigurierbar. Das begrenzt die möglichen Effizienzgewinne, es sei denn, Clients würden announces (Tracker-Ankündigungsanfragen) bündeln, um sie alle innerhalb eines Ein-Minuten-Zeitfensters abzusetzen. i2psnark bündelt announces derzeit nicht; es verteilt sie, um Verkehrsspitzen zu vermeiden. Berichten zufolge betreiben Power-User gleichzeitig Tausende von Torrents, und so viele announces in eine Minute zu pressen, ist unrealistisch.

Hier schlagen wir vor, die Verbindungsantwort um ein optionales Feld für die Lebensdauer der Verbindung zu erweitern. Fehlt es, beträgt der Standardwert eine Minute. Andernfalls soll die in Sekunden angegebene Lebensdauer vom Client verwendet werden, und der Tracker hält die Verbindungs-ID eine weitere Minute vor.

### Kompatibilität mit BEP 15

Dieses Design bewahrt die Kompatibilität mit [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) so weit wie möglich, um die in bestehenden Clients und Trackern erforderlichen Änderungen zu begrenzen.

Die einzige erforderliche Änderung betrifft das Format der Peer-Informationen in der Announce-Antwort. Die Ergänzung des Feldes lifetime in der Connect-Antwort ist nicht erforderlich, wird jedoch aus Effizienzgründen, wie oben erläutert, nachdrücklich empfohlen.

### Sicherheitsanalyse

Ein wichtiges Ziel eines UDP-Announce-Protokolls ist es, Adressfälschung zu verhindern. Der Client muss tatsächlich existieren und ein echtes leaseSet beifügen. Er muss über eingehende tunnels verfügen, um die Connect Response empfangen zu können. Diese tunnels könnten zero-hop (ohne Zwischenknoten) sein und sofort aufgebaut werden, aber das würde den Ersteller offenlegen. Dieses Protokoll erreicht dieses Ziel.

### Probleme

Dieses Protokoll unterstützt keine blinded destinations (verblindete Ziele), kann aber entsprechend erweitert werden, um dies zu ermöglichen. Siehe unten.

## Spezifikation

### Protokolle und Ports

Repliable Datagram2 (beantwortbares Datagramm) verwendet das I2CP-Protokoll 19; Repliable Datagram3 verwendet das I2CP-Protokoll 20; rohe Datagramme verwenden das I2CP-Protokoll 18. Anfragen dürfen Datagram2 oder Datagram3 sein. Antworten sind immer rohe Datagramme. Das ältere repliable datagram ("Datagram1")-Format mit I2CP-Protokoll 17 darf NICHT für Anfragen oder Antworten verwendet werden; diese müssen verworfen werden, wenn sie auf den Anfrage-/Antwort-Ports empfangen werden. Beachten Sie, dass Datagram1 Protokoll 17 weiterhin für das DHT (verteilte Hashtabelle)-Protokoll verwendet wird.

Anfragen verwenden den I2CP "to port" (Ziel-Port) aus der announce-URL; siehe unten. Der "from port" (Quell-Port) der Anfrage wird vom Client gewählt, sollte jedoch ungleich Null sein und sich von den von DHT verwendeten Ports unterscheiden, damit Antworten leicht zugeordnet werden können. Tracker sollten Anfragen ablehnen, die am falschen Port eingehen.

Antworten verwenden den I2CP "to port" (Zielport) aus der Anfrage. Der "from port" (Quellport) der Antwort ist der "to port" der Anfrage.

### Ankündigungs-URL

Das Format der Announce-URL ist in [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) nicht spezifiziert, aber wie im Clearnet haben UDP-Announce-URLs die Form "udp://host:port/path". Der Pfad wird ignoriert und darf leer sein, ist im Clearnet jedoch typischerweise "/announce". Der :port-Teil sollte immer vorhanden sein; falls der ":port"-Teil jedoch weggelassen wird, verwende den Standard-I2CP-Port 6969, da dies der übliche Port im Clearnet ist. Es können außerdem CGI-Parameter &a=b&c=d angehängt sein; diese können verarbeitet und in der Announce-Anfrage bereitgestellt werden, siehe [BEP 41](http://www.bittorrent.org/beps/bep_0041.html). Wenn es keine Parameter oder keinen Pfad gibt, kann der abschließende / ebenfalls weggelassen werden, wie in [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) impliziert.

### Datagrammformate

Alle Werte werden in Netzwerk-Byte-Reihenfolge (Big-Endian) gesendet. Erwarten Sie nicht, dass Pakete exakt eine bestimmte Größe haben. Zukünftige Erweiterungen könnten die Größe der Pakete erhöhen.

#### Verbindungsanfrage

Client an den Tracker. 16 Bytes. Muss ein repliable Datagram2 (antwortfähiges Datagram2) sein. Wie in [BEP 15](http://www.bittorrent.org/beps/bep_0015.html). Keine Änderungen.

```
Offset  Size            Name            Value
0       64-bit integer  protocol_id     0x41727101980 // magic constant
8       32-bit integer  action          0 // connect
12      32-bit integer  transaction_id
```
#### Verbindungsantwort

Tracker an den Client. 16 oder 18 Bytes. Muss roh sein. Entspricht [BEP 15](http://www.bittorrent.org/beps/bep_0015.html), außer wie unten angegeben.

```
Offset  Size            Name            Value
0       32-bit integer  action          0 // connect
4       32-bit integer  transaction_id
8       64-bit integer  connection_id
16      16-bit integer  lifetime        optional  // Change from BEP 15
```
Die Antwort MUSS an den I2CP "to port" gesendet werden, der als "from port" der Anfrage empfangen wurde.

Das Feld lifetime ist optional und gibt die clientseitige Lebensdauer der connection_id in Sekunden an. Der Standardwert beträgt 60, und der Mindestwert, sofern angegeben, ist 60. Der Höchstwert ist 65535 bzw. etwa 18 Stunden. Der Tracker sollte die connection_id 60 Sekunden länger als die clientseitige Lebensdauer vorhalten.

#### Ankündigungsanfrage

Client an den Tracker. Mindestens 98 Bytes. Muss ein beantwortbares Datagram3 (Datagramm-Typ 3) sein. Wie in [BEP 15](http://www.bittorrent.org/beps/bep_0015.html), außer wie unten angegeben.

Die connection_id ist die, die in der connect response empfangen wurde.

```
Offset  Size            Name            Value
0       64-bit integer  connection_id
8       32-bit integer  action          1     // announce
12      32-bit integer  transaction_id
16      20-byte string  info_hash
36      20-byte string  peer_id
56      64-bit integer  downloaded
64      64-bit integer  left
72      64-bit integer  uploaded
80      32-bit integer  event           0     // 0: none; 1: completed; 2: started; 3: stopped
84      32-bit integer  IP address      0     // default, unused in I2P
88      32-bit integer  key
92      32-bit integer  num_want        -1    // default
96      16-bit integer  port                  // must be same as I2CP from port
98      varies          options     optional  // As specified in BEP 41
```
Änderungen gegenüber [BEP 15](http://www.bittorrent.org/beps/bep_0015.html):

- Schlüssel wird ignoriert
- IP-Adresse wird nicht verwendet
- Port wird wahrscheinlich ignoriert, muss aber mit dem I2CP from port übereinstimmen
- Der Abschnitt options, falls vorhanden, ist wie in [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) definiert

Die Antwort MUSS an den I2CP "to port" gesendet werden, der als "from port" der Anfrage empfangen wurde. Verwenden Sie nicht den Port aus dem announce request (Ankündigungsanfrage).

#### Announce-Antwort

Vom Tracker zum Client. Mindestens 20 Byte. Muss im Rohformat vorliegen. Entspricht [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) mit den unten genannten Ausnahmen.

```
Offset  Size            Name            Value
0           32-bit integer  action          1 // announce
4           32-bit integer  transaction_id
8           32-bit integer  interval
12          32-bit integer  leechers
16          32-bit integer  seeders
20   32 * n 32-byte hash    binary hashes     // Change from BEP 15
...                                           // Change from BEP 15
```
Änderungen gegenüber [BEP 15](http://www.bittorrent.org/beps/bep_0015.html):

- Statt 6-Byte IPv4+Port oder 18-Byte IPv6+Port geben wir ein Vielfaches von 32 Byte in Form von "compact responses" (kompakte Antworten) mit den binären SHA-256-Peer-Hashes zurück. Wie bei TCP compact responses geben wir keinen Port an.

Die Antwort MUSS an den I2CP "to port" gesendet werden, der in der Anfrage als "from port" empfangen wurde. Verwenden Sie nicht den Port aus der announce request (Ankündigungsanfrage).

I2P-Datagramme haben eine sehr große maximale Größe von etwa 64 KB; für eine zuverlässige Zustellung sollten jedoch Datagramme größer als 4 KB vermieden werden. Um die Bandbreite effizient zu nutzen, sollten Tracker die maximale Anzahl von Peers vermutlich auf etwa 50 begrenzen; das entspricht ungefähr einem 1600‑Byte‑Paket vor dem Overhead in den verschiedenen Schichten und sollte nach der Fragmentierung innerhalb der Nutzlastgrenze einer über zwei tunnel gesendeten Nachricht liegen.

Wie in BEP 15 ist keine Anzahl der folgenden Peer-Adressen (bei BEP 15 IP/Port, hier Hashes) enthalten. Auch wenn BEP 15 dies nicht vorsieht, könnte eine aus lauter Nullen bestehende Endemarkierung der Peers definiert werden, um anzuzeigen, dass die Peer-Informationen vollständig sind und anschließend Erweiterungsdaten folgen.

Damit zukünftige Erweiterungen möglich sind, sollten Clients einen 32-Byte-Hash aus lauter Nullen und alle darauf folgenden Daten ignorieren. Tracker sollten Announce-Anfragen mit einem Hash aus lauter Nullen ablehnen, obwohl dieser Hash bereits von Java routers gesperrt ist.

#### Scrape (automatisches Extrahieren von Daten)

Scrape-Request/-Response gemäß [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) sind von dieser Spezifikation nicht vorgeschrieben, können jedoch bei Bedarf implementiert werden; es sind keine Änderungen erforderlich. Der Client muss zunächst eine Verbindungs-ID abrufen. Der Scrape-Request ist immer ein repliable (antwortfähig) Datagram3. Die Scrape-Response ist immer raw (roh).

#### Fehlerantwort

Tracker an den Client. Mindestens 8 Bytes (wenn die Nachricht leer ist). Muss im Rohformat vorliegen. Wie in [BEP 15](http://www.bittorrent.org/beps/bep_0015.html). Keine Änderungen.

```
Offset  Size            Name            Value
0       32-bit integer  action          3 // error
4       32-bit integer  transaction_id
8       string          message
```
## Erweiterungen

Erweiterungsbits oder ein Versionsfeld sind nicht enthalten. Clients und Tracker sollten nicht davon ausgehen, dass Pakete eine bestimmte Größe haben. Auf diese Weise können zusätzliche Felder hinzugefügt werden, ohne die Kompatibilität zu beeinträchtigen. Das in [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) definierte Erweiterungsformat wird bei Bedarf empfohlen.

Die Verbindungsantwort wird geändert, um eine optionale Lebensdauer der Verbindungs-ID hinzuzufügen.

Wenn Unterstützung für verblindete Ziele erforderlich ist, können wir entweder die verblindete 35-Byte-Adresse an das Ende der announce-Anfrage anhängen oder in den Antworten verblindete Hashes anfordern, unter Verwendung des [BEP 41](http://www.bittorrent.org/beps/bep_0041.html)-Formats (Parameter noch festzulegen). Die Menge der verblindeten 35-Byte-Peer-Adressen könnte an das Ende der announce-Antwort angehängt werden, nach einem 32-Byte-Hash aus lauter Nullen.

## Implementierungsrichtlinien

Siehe den oben stehenden Design-Abschnitt für eine Diskussion der Herausforderungen für nicht integrierte, nicht-I2CP-Clients und -Tracker.

### Client-Anwendungen

Für einen bestimmten Tracker-Hostnamen sollte ein Client UDP gegenüber HTTP-URLs bevorzugen und nicht an beide melden.

Clients mit vorhandener Unterstützung für BEP 15 sollten nur kleine Anpassungen erfordern.

Wenn ein Client DHT oder andere Datagramm-Protokolle unterstützt, sollte er wahrscheinlich einen anderen Port als den „from port“ der Anfrage wählen, damit die Antworten an diesen Port zurückkommen und nicht mit DHT-Nachrichten vermischt werden. Der Client empfängt als Antworten nur rohe Datagramme. Tracker werden dem Client niemals ein repliable datagram2 (antwortfähiges Datagramm) senden.

Clients mit einer Standardliste von Open-Trackern sollten die Liste aktualisieren und UDP-URLs hinzufügen, sobald bestätigt ist, dass die bekannten Open-Tracker UDP unterstützen.

Clients können die Neuübertragung von Anfragen implementieren, müssen dies jedoch nicht. Neuübertragungen sollten, falls implementiert, ein anfängliches Timeout von mindestens 15 Sekunden verwenden und das Timeout bei jeder weiteren Neuübertragung verdoppeln (exponentielles Backoff).

Clients müssen nach dem Erhalt einer Fehlerantwort ein Backoff (abgestufte Wartezeit) durchführen.

### Tracker

Tracker mit bestehender Unterstützung für BEP 15 sollten nur kleine Änderungen erfordern. Diese Spezifikation unterscheidet sich vom Vorschlag von 2014 dadurch, dass der Tracker den Empfang von antwortfähigen datagram2 und datagram3 auf demselben Port unterstützen muss.

Um die Ressourcenanforderungen des Trackers zu minimieren, ist dieses Protokoll so konzipiert, dass der Tracker keine Zuordnungen von Client-Hashes zu Verbindungs-IDs für eine spätere Validierung speichern muss. Dies ist möglich, weil das Announce-Anfragepaket ein beantwortbares Datagram3-Paket ist, sodass es den Hash des Absenders enthält.

Eine empfohlene Implementierung ist:

- Definiere die aktuelle Epoche als die aktuelle Zeit mit einer Auflösung entsprechend der Verbindungslebensdauer, `epoch = now / lifetime`.
- Definiere eine kryptografische Hashfunktion `H(secret, clienthash, epoch)`, die eine 8-Byte-Ausgabe erzeugt.
- Erzeuge den zufälligen, konstanten Geheimwert, der für alle Verbindungen verwendet wird.
- Für Verbindungsantworten generiere `connection_id = H(secret, clienthash, epoch)`
- Für Announce-Anfragen validiere die empfangene Verbindungs-ID in der aktuellen Epoche, indem du überprüfst `connection_id == H(secret, clienthash, epoch) || connection_id == H(secret, clienthash, epoch - 1)`

## Bereitstellungsstatus

Dieses Protokoll wurde am 24. Juni 2025 verabschiedet und ist seit September 2025 im I2P-Netzwerk vollständig in Betrieb.

### Aktuelle Implementierungen

**i2psnark**: Umfassende UDP-Tracker-Unterstützung ist in I2P Version 2.10.0 (API 0.9.67), veröffentlicht am 8. September 2025, enthalten. Alle I2P-Installationen ab dieser Version enthalten standardmäßig die UDP-Tracker-Funktionalität.

**zzzot tracker**: Version 0.20.0-beta2 und neuer unterstützen UDP-Announce-Anfragen. Stand Oktober 2025 sind die folgenden Tracker im Produktivbetrieb aktiv: - opentracker.dg2.i2p - opentracker.simp.i2p - opentracker.skank.i2p

### Hinweise zur Client-Kompatibilität

**SAM v3.3-Einschränkungen**: Externe BitTorrent-Clients, die SAM (Simple Anonymous Messaging, einfache anonyme Nachrichtenübermittlung) verwenden, benötigen SAM v3.3-Unterstützung für Datagram2/3. Dies ist in Java I2P verfügbar, wird jedoch von i2pd (der C++-I2P-Implementierung) derzeit nicht unterstützt, was den Einsatz in libtorrent-basierten Clients wie qBittorrent einschränken könnte.

**I2CP-Clients**: Clients, die I2CP direkt verwenden (z. B. BiglyBT), können UDP-Tracker-Unterstützung ohne SAM-Einschränkungen implementieren.

## Referenzen

- **[BEP15]**: [BitTorrent-UDP-Tracker-Protokoll](http://www.bittorrent.org/beps/bep_0015.html)
- **[BEP41]**: [Erweiterungen des UDP-Tracker-Protokolls](http://www.bittorrent.org/beps/bep_0041.html)
- **[DATAGRAMS]**: [Spezifikation zu I2P-Datagrammen](/docs/api/datagrams/)
- **[Prop160]**: [Vorschlag für UDP-Tracker](/proposals/160-udp-trackers/)
- **[Prop163]**: [Vorschlag für Datagram2](/proposals/163-datagram2/)
- **[SPEC]**: [BitTorrent über I2P](/docs/applications/bittorrent/)
