---
title: "UDP-Tracker"
number: "160"
author: "zzz"
created: "2022-01-03"
lastupdated: "2025-06-25"
status: "Geschlossen"
thread: "http://zzz.i2p/topics/1634"
target: "0.9.67"
toc: true
---

## Status

Genehmigt bei der Überprüfung am 2025-06-24. Die Spezifikation befindet sich unter [UDP specification](/docs/specs/udp-bittorrent-announces/). Implementiert in zzzot 0.20.0-beta2. Implementiert in i2psnark ab API 0.9.67. Prüfen Sie die Dokumentation anderer Implementierungen für den Status.

## Überblick

Dieser Vorschlag ist für die Implementierung von UDP-Trackern in I2P.

### Change History

Ein vorläufiger Vorschlag für UDP-Tracker in I2P wurde im Mai 2014 auf unserer [bittorrent spec page](/docs/applications/bittorrent/) veröffentlicht; dies war vor unserem formalen Vorschlagsverfahren und wurde nie implementiert. Dieser Vorschlag wurde Anfang 2022 erstellt und vereinfacht die Version von 2014.

Da dieser Vorschlag auf antwortfähige Datagramme angewiesen ist, wurde er zurückgestellt, als wir Anfang 2023 mit der Arbeit am [Datagram2-Vorschlag](/proposals/163-datagram2/) begannen. Dieser Vorschlag wurde im April 2025 genehmigt.

Die 2023-Version dieses Vorschlags spezifizierte zwei Modi, "Kompatibilität" und "schnell". Weitere Analysen zeigten, dass der schnelle Modus unsicher wäre und auch ineffizient für Clients mit einer großen Anzahl von Torrents. Darüber hinaus gab BiglyBT eine Präferenz für den Kompatibilitätsmodus an. Dieser Modus wird einfacher zu implementieren sein für jeden tracker oder Client, der den Standard [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) unterstützt.

Obwohl der Kompatibilitätsmodus auf Client-Seite komplexer von Grund auf zu implementieren ist, haben wir vorläufigen Code dafür, der 2023 begonnen wurde.

Daher ist die aktuelle Version hier weiter vereinfacht, um den Fast Mode zu entfernen und den Begriff "Kompatibilität" zu streichen. Die aktuelle Version wechselt zum neuen Datagram2-Format und fügt Verweise auf das UDP-Announce-Erweiterungsprotokoll [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) hinzu.

Außerdem wird ein Verbindungs-ID-Lebensdauer-Feld zur Connect-Response hinzugefügt, um die Effizienzgewinne dieses Protokolls zu erweitern.

## Motivation

Da die Benutzerbasis im Allgemeinen und die Anzahl der BitTorrent-Nutzer im Besonderen weiter wächst, müssen wir Tracker und Announces effizienter gestalten, damit Tracker nicht überlastet werden.

Bittorrent schlug UDP-Tracker in BEP 15 [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) im Jahr 2008 vor, und die große Mehrheit der Tracker im Clearnet sind jetzt nur noch UDP-basiert.

Es ist schwierig, die Bandbreiteneinsparungen von Datagrammen gegenüber Streaming-Protokoll zu berechnen. Eine beantwortbare Anfrage hat etwa die gleiche Größe wie ein Streaming-SYN, aber die Nutzlast ist etwa 500 Bytes kleiner, da der HTTP-GET eine riesige 600-Byte-URL-Parameter-Zeichenkette hat. Die rohe Antwort ist viel kleiner als ein Streaming-SYN-ACK, was eine erhebliche Reduzierung für den ausgehenden Traffic eines Trackers bietet.

Zusätzlich sollte es implementierungsspezifische Speicherreduzierungen geben, da Datagramme deutlich weniger Arbeitsspeicher-Zustand erfordern als eine Streaming-Verbindung.

Post-Quantum-Verschlüsselung und -Signaturen, wie in [/proposals/169-pq-crypto/](/proposals/169-pq-crypto/) vorgesehen, werden den Overhead von verschlüsselten und signierten Strukturen erheblich erhöhen, einschließlich destinations, leasesets, streaming SYN und SYN ACK. Es ist wichtig, diesen Overhead wo möglich zu minimieren, bevor PQ-Kryptografie in I2P eingeführt wird.

## Motivation

Dieser Vorschlag verwendet repliable datagram2, repliable datagram3 und raw datagrams, wie in [/docs/api/datagrams/](/docs/api/datagrams/) definiert. Datagram2 und Datagram3 sind neue Varianten von repliable datagrams, die in Vorschlag 163 [/proposals/163-datagram2/](/proposals/163-datagram2/) definiert sind. Datagram2 fügt Replay-Resistenz und Offline-Signatur-Unterstützung hinzu. Datagram3 ist kleiner als das alte Datagram-Format, aber ohne Authentifizierung.

### BEP 15

Zur Referenz ist der in [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) definierte Nachrichtenfluss wie folgt:

```
Client                        Tracker
    Connect Req. ------------->
      <-------------- Connect Resp.
    Announce Req. ------------->
      <-------------- Announce Resp.
    Announce Req. ------------->
      <-------------- Announce Resp.
```
Die Connect-Phase ist erforderlich, um IP-Adressen-Spoofing zu verhindern. Der Tracker gibt eine Verbindungs-ID zurück, die der Client in nachfolgenden Ankündigungen verwendet. Diese Verbindungs-ID läuft standardmäßig nach einer Minute beim Client und nach zwei Minuten beim Tracker ab.

I2P wird den gleichen Nachrichtenfluss wie BEP 15 verwenden, um die Übernahme in bestehende UDP-fähige Client-Codebasen zu erleichtern: aus Effizienzgründen und aus den unten diskutierten Sicherheitsgründen:

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
Dies bietet potenziell erhebliche Bandbreiteneinsparungen gegenüber Streaming (TCP) Ankündigungen. Während das Datagram2 etwa die gleiche Größe wie ein Streaming SYN hat, ist die Raw-Antwort viel kleiner als das Streaming SYN ACK. Nachfolgende Anfragen verwenden Datagram3, und die nachfolgenden Antworten sind raw.

Die Announce-Anfragen sind Datagram3, sodass der Tracker keine große Zuordnungstabelle von Verbindungs-IDs zu Announce-Zielen oder Hashes verwalten muss. Stattdessen kann der Tracker Verbindungs-IDs kryptografisch aus dem Sender-Hash, dem aktuellen Zeitstempel (basierend auf einem bestimmten Intervall) und einem geheimen Wert generieren. Wenn eine Announce-Anfrage empfangen wird, validiert der Tracker die Verbindungs-ID und verwendet dann den Datagram3-Sender-Hash als Sendeziel.

### Änderungshistorie

Für eine integrierte Anwendung (Router und Client in einem Prozess, zum Beispiel i2psnark und das ZzzOT Java-Plugin) oder für eine I2CP-basierte Anwendung (zum Beispiel BiglyBT) sollte es unkompliziert sein, den Streaming- und Datagramm-Verkehr separat zu implementieren und zu routen. ZzzOT und i2psnark werden voraussichtlich der erste Tracker und Client sein, die diesen Vorschlag umsetzen.

Nicht-integrierte Tracker und Clients werden im Folgenden besprochen.

#### Trackers

Es gibt vier bekannte I2P-Tracker-Implementierungen:

- zzzot, ein integriertes Java router Plugin, läuft auf opentracker.dg2.i2p und mehreren anderen
- tracker2.postman.i2p, läuft vermutlich hinter einem Java router und HTTP Server tunnel
- Der alte C opentracker, portiert von zzz, mit auskommentierter UDP-Unterstützung
- Der neue C opentracker, portiert von r4sas, läuft auf opentracker.r4sas.i2p und möglicherweise anderen,
  läuft vermutlich hinter einem i2pd router und HTTP Server tunnel

Für eine externe Tracker-Anwendung, die derzeit einen HTTP-Server-Tunnel verwendet, um Announce-Anfragen zu empfangen, könnte die Implementierung recht schwierig sein. Ein spezialisierter Tunnel könnte entwickelt werden, um Datagramme in lokale HTTP-Anfragen/Antworten zu übersetzen. Oder es könnte ein spezialisierter Tunnel entworfen werden, der sowohl HTTP-Anfragen als auch Datagramme verarbeitet und die Datagramme an den externen Prozess weiterleitet. Diese Designentscheidungen werden stark von den spezifischen Router- und Tracker-Implementierungen abhängen und liegen außerhalb des Umfangs dieses Vorschlags.

#### Clients

Externe SAM-basierte Torrent-Clients wie qbittorrent und andere libtorrent-basierte Clients würden [SAM v3.3](/docs/api/samv3/) benötigen, was von i2pd nicht unterstützt wird. Dies ist auch für DHT-Unterstützung erforderlich und komplex genug, dass kein bekannter SAM-Torrent-Client es implementiert hat. Keine SAM-basierten Implementierungen dieses Vorschlags werden in naher Zukunft erwartet.

### Connection Lifetime

[BEP 15](http://www.bittorrent.org/beps/bep_0015.html) legt fest, dass die Verbindungs-ID beim Client nach einer Minute und beim Tracker nach zwei Minuten abläuft. Dies ist nicht konfigurierbar. Das begrenzt die potenziellen Effizienzgewinne, es sei denn, Clients würden Announces stapelweise verarbeiten, um alle innerhalb eines einminütigen Zeitfensters durchzuführen. i2psnark stapelt derzeit keine Announces; es verteilt sie, um Verkehrsspitzen zu vermeiden. Power-User betreiben Berichten zufolge tausende von Torrents gleichzeitig, und so viele Announces in eine Minute zu bündeln ist nicht realistisch.

Hier schlagen wir vor, die Connect-Antwort zu erweitern, um ein optionales Feld für die Verbindungslebensdauer hinzuzufügen. Der Standardwert, falls nicht vorhanden, beträgt eine Minute. Andernfalls soll die in Sekunden angegebene Lebensdauer vom Client verwendet werden, und der Tracker wird die Verbindungs-ID für eine weitere Minute aufrechterhalten.

### Compatibility with BEP 15

Dieses Design behält die Kompatibilität mit [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) so weit wie möglich bei, um die erforderlichen Änderungen in bestehenden Clients und Trackern zu begrenzen.

Die einzige erforderliche Änderung ist das Format der Peer-Informationen in der Announce-Antwort. Die Hinzufügung des Lifetime-Feldes in der Connect-Antwort ist nicht erforderlich, wird aber aus Effizienzgründen dringend empfohlen, wie oben erklärt.

### BEP 15

Ein wichtiges Ziel eines UDP-Announce-Protokolls ist es, Address-Spoofing zu verhindern. Der Client muss tatsächlich existieren und ein echtes leaseset bündeln. Er muss über eingehende Tunnel verfügen, um die Connect Response zu empfangen. Diese Tunnel könnten Zero-Hop-Tunnel sein und sofort erstellt werden, aber das würde den Ersteller preisgeben. Dieses Protokoll erreicht dieses Ziel.

### Tracker/Client-Unterstützung

- Dieser Vorschlag unterstützt keine blinded destinations,
  kann aber entsprechend erweitert werden. Siehe unten.

## Design

### Protocols and Ports

Repliable Datagram2 verwendet I2CP-Protokoll 19; repliable Datagram3 verwendet I2CP-Protokoll 20; rohe Datagramme verwenden I2CP-Protokoll 18. Anfragen können Datagram2 oder Datagram3 sein. Antworten sind immer roh. Das ältere repliable datagram ("Datagram1") Format mit I2CP-Protokoll 17 darf NICHT für Anfragen oder Antworten verwendet werden; diese müssen verworfen werden, falls sie auf den Anfrage-/Antwort-Ports empfangen werden. Beachten Sie, dass Datagram1-Protokoll 17 weiterhin für das DHT-Protokoll verwendet wird.

Anfragen verwenden den I2CP "to port" aus der Announce-URL; siehe unten. Der "from port" der Anfrage wird vom Client gewählt, sollte aber ungleich null sein und sich von den Ports unterscheiden, die von DHT verwendet werden, damit Antworten leicht klassifiziert werden können. Tracker sollten Anfragen ablehnen, die auf dem falschen Port empfangen werden.

Antworten verwenden den I2CP "to port" aus der Anfrage. Der "from port" der Anfrage ist der "to port" aus der Anfrage.

### Announce URL

Das Format der Announce-URL ist in [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) nicht spezifiziert, aber wie im Clearnet haben UDP-Announce-URLs die Form "udp://host:port/path". Der Pfad wird ignoriert und kann leer sein, ist aber typischerweise "/announce" im Clearnet. Der :port-Teil sollte immer vorhanden sein, falls jedoch der ":port"-Teil weggelassen wird, verwende einen Standard-I2CP-Port von 6969, da dies der übliche Port im Clearnet ist. Es können auch CGI-Parameter &a=b&c=d angehängt werden, diese können verarbeitet und in der Announce-Anfrage bereitgestellt werden, siehe [BEP 41](http://www.bittorrent.org/beps/bep_0041.html). Falls keine Parameter oder Pfad vorhanden sind, kann der abschließende / ebenfalls weggelassen werden, wie in [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) impliziert.

### Verbindungslebensdauer

Alle Werte werden in Network-Byte-Reihenfolge (Big Endian) gesendet. Erwarten Sie nicht, dass Pakete genau eine bestimmte Größe haben. Zukünftige Erweiterungen könnten die Größe der Pakete erhöhen.

#### Connect Request

Client zum Tracker. 16 Bytes. Muss ein beantwortbares Datagram2 sein. Gleich wie in [BEP 15](http://www.bittorrent.org/beps/bep_0015.html). Keine Änderungen.

```
Offset  Size            Name            Value
  0       64-bit integer  protocol_id     0x41727101980 // magic constant
  8       32-bit integer  action          0 // connect
  12      32-bit integer  transaction_id
```
#### Connect Response

Tracker zu Client. 16 oder 18 Bytes. Muss raw sein. Gleich wie in [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) außer wie unten angemerkt.

```
Offset  Size            Name            Value
  0       32-bit integer  action          0 // connect
  4       32-bit integer  transaction_id
  8       64-bit integer  connection_id
  16      16-bit integer  lifetime        optional  // Change from BEP 15
```
Die Antwort MUSS an den I2CP "to port" gesendet werden, der als "from port" der Anfrage empfangen wurde.

Das lifetime-Feld ist optional und gibt die connection_id Client-Lebensdauer in Sekunden an. Der Standardwert ist 60, und das Minimum, wenn angegeben, ist 60. Das Maximum ist 65535 oder etwa 18 Stunden. Der Tracker sollte die connection_id 60 Sekunden länger als die Client-Lebensdauer aufrechterhalten.

#### Announce Request

Client zu Tracker. Mindestens 98 Bytes. Muss ein beantwortbares Datagram3 sein. Gleich wie in [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) außer wie unten vermerkt.

Die connection_id ist wie in der connect-Antwort empfangen.

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
  84      32-bit integer  IP address      0     // default
  88      32-bit integer  key
  92      32-bit integer  num_want        -1    // default
  96      16-bit integer  port
  98      varies          options     optional  // As specified in BEP 41
```
Änderungen von [BEP 15](http://www.bittorrent.org/beps/bep_0015.html):

- key wird ignoriert
- port wird wahrscheinlich ignoriert
- Der options-Abschnitt, falls vorhanden, ist wie in [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) definiert

Die Antwort MUSS an den I2CP "to port" gesendet werden, der als "from port" der Anfrage empfangen wurde. Verwenden Sie nicht den Port aus der Announce-Anfrage.

#### Announce Response

Tracker zu Client. Mindestens 20 Bytes. Muss raw sein. Gleich wie in [BEP 15](http://www.bittorrent.org/beps/bep_0015.html), außer wie unten angegeben.

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
Änderungen von [BEP 15](http://www.bittorrent.org/beps/bep_0015.html):

- Anstatt 6-Byte IPv4+Port oder 18-Byte IPv6+Port geben wir
  ein Vielfaches von 32-Byte "compact responses" mit den SHA-256 binären Peer-Hashes zurück.
  Wie bei TCP compact responses schließen wir keinen Port ein.

Die Antwort MUSS an den I2CP "to port" gesendet werden, der als "from port" der Anfrage empfangen wurde. Verwenden Sie nicht den Port aus der Announce-Anfrage.

I2P-Datagramme haben eine sehr große maximale Größe von etwa 64 KB; für eine zuverlässige Übertragung sollten jedoch Datagramme größer als 4 KB vermieden werden. Für Bandbreiteneffizienz sollten Tracker die maximalen Peers wahrscheinlich auf etwa 50 begrenzen, was etwa einem 1600-Byte-Paket vor Overhead auf verschiedenen Schichten entspricht und innerhalb eines Zwei-Tunnel-Nachrichten-Payload-Limits nach Fragmentierung liegen sollte.

Wie in BEP 15 ist keine Anzahl der folgenden Peer-Adressen (IP/Port für BEP 15, Hashes hier) enthalten. Obwohl in BEP 15 nicht vorgesehen, könnte eine End-of-Peers-Markierung aus lauter Nullen definiert werden, um anzuzeigen, dass die Peer-Informationen vollständig sind und einige Erweiterungsdaten folgen.

Damit eine Erweiterung in der Zukunft möglich ist, sollten Clients einen 32-Byte-Hash aus lauter Nullen und alle darauf folgenden Daten ignorieren. Tracker sollten Ankündigungen von einem Hash aus lauter Nullen ablehnen, obwohl dieser Hash bereits von Java-routern gesperrt wird.

#### Scrape

Scrape-Anfrage/Antwort aus [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) ist nicht von diesem Vorschlag gefordert, kann aber bei Bedarf implementiert werden, keine Änderungen erforderlich. Der Client muss zuerst eine Verbindungs-ID erwerben. Die Scrape-Anfrage ist immer beantwortbares Datagram3. Die Scrape-Antwort ist immer raw.

#### Tracker

Tracker zu Client. 8 Bytes mindestens (wenn die Nachricht leer ist). Muss raw sein. Gleich wie in [BEP 15](http://www.bittorrent.org/beps/bep_0015.html). Keine Änderungen.

```
Offset  Size            Name            Value
  0       32-bit integer  action          3 // error
  4       32-bit integer  transaction_id
  8       string          message
```
## Extensions

Extension-Bits oder ein Versionsfeld sind nicht enthalten. Clients und Tracker sollten nicht davon ausgehen, dass Pakete eine bestimmte Größe haben. Auf diese Weise können zusätzliche Felder hinzugefügt werden, ohne die Kompatibilität zu beeinträchtigen. Das in [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) definierte Extensions-Format wird empfohlen, falls erforderlich.

Die Connect-Antwort wird modifiziert, um eine optionale Lebensdauer der Verbindungs-ID hinzuzufügen.

Wenn Unterstützung für blinded destinations erforderlich ist, können wir entweder die blinded 35-Byte-Adresse am Ende der Announce-Anfrage hinzufügen oder blinded Hashes in den Antworten anfordern, unter Verwendung des [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) Formats (Parameter noch zu bestimmen). Der Satz von blinded 35-Byte-Peer-Adressen könnte am Ende der Announce-Antwort hinzugefügt werden, nach einem aus Nullen bestehenden 32-Byte-Hash.

## Implementation guidelines

Siehe den Design-Abschnitt oben für eine Diskussion der Herausforderungen für nicht-integrierte, nicht-I2CP Clients und Tracker.

### Kompatibilität mit BEP 15

Für einen gegebenen Tracker-Hostnamen sollte ein Client UDP gegenüber HTTP-URLs bevorzugen und sollte nicht an beide ankündigen.

Clients mit vorhandener BEP 15-Unterstützung sollten nur kleine Modifikationen benötigen.

Wenn ein Client DHT oder andere Datagramm-Protokolle unterstützt, sollte er wahrscheinlich einen anderen Port als "From-Port" für die Anfrage wählen, damit die Antworten an diesen Port zurückgesendet werden und nicht mit DHT-Nachrichten vermischt werden. Der Client empfängt nur rohe Datagramme als Antworten. Tracker senden niemals ein beantwortbares datagram2 an den Client.

Clients mit einer Standard-Liste von Opentrackers sollten die Liste aktualisieren, um UDP-URLs hinzuzufügen, nachdem bekannt ist, dass die bekannten Opentracker UDP unterstützen.

Clients können Retransmissionen von Anfragen implementieren oder auch nicht. Retransmissionen sollten, falls implementiert, ein anfängliches Timeout von mindestens 15 Sekunden verwenden und das Timeout für jede Retransmission verdoppeln (exponential backoff).

Clients müssen nach Erhalt einer Fehlerantwort zurückweichen.

### Sicherheitsanalyse

Tracker mit vorhandener BEP 15 Unterstützung sollten nur kleine Änderungen benötigen. Dieser Vorschlag unterscheidet sich von dem Vorschlag aus 2014 dahingehend, dass der Tracker den Empfang von repliable datagram2 und datagram3 auf demselben Port unterstützen muss.

Um die Ressourcenanforderungen des Trackers zu minimieren, ist dieses Protokoll darauf ausgelegt, jegliche Anforderung zu eliminieren, dass der Tracker Zuordnungen von Client-Hashes zu Verbindungs-IDs für spätere Validierung speichert. Dies ist möglich, weil das Announce-Request-Paket ein antwortbares Datagram3-Paket ist, daher enthält es den Hash des Senders.

Eine empfohlene Implementierung ist:

- Definiere die aktuelle Epoche als die aktuelle Zeit mit einer Auflösung der Verbindungslebensdauer,
  ``epoch = now / lifetime``.
- Definiere eine kryptographische Hash-Funktion ``H(secret, clienthash, epoch)``, die
  eine 8-Byte-Ausgabe erzeugt.
- Generiere die zufällige Konstante secret, die für alle Verbindungen verwendet wird.
- Für Connect-Antworten, generiere ``connection_id = H(secret,  clienthash, epoch)``
- Für Announce-Anfragen, validiere die empfangene Verbindungs-ID in der aktuellen Epoche durch Überprüfung von
  ``connection_id == H(secret, clienthash, epoch) || connection_id == H(secret, clienthash, epoch - 1)``

## Migration

Vorhandene Clients unterstützen keine UDP-Announce-URLs und ignorieren sie.

Bestehende Tracker unterstützen nicht den Empfang von beantwortbaren oder rohen Datagrammen, diese werden verworfen.

Dieser Vorschlag ist vollständig optional. Weder Clients noch Tracker sind verpflichtet, ihn zu irgendeinem Zeitpunkt zu implementieren.

## Rollout

Die ersten Implementierungen werden voraussichtlich in ZzzOT und i2psnark erfolgen. Sie werden zum Testen und Verifizieren dieses Vorschlags verwendet.

Andere Implementierungen werden nach Wunsch folgen, sobald die Tests und Überprüfungen abgeschlossen sind.
