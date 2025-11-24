---
title: "UDP-Tracker"
number: "160"
author: "zzz"
created: "2022-01-03"
lastupdated: "2025-06-25"
status: "Closed"
thread: "http://zzz.i2p/topics/1634"
target: "0.9.67"
---

## Status

Genehmigt bei der Überprüfung am 2025-06-24.
Spezifikation ist unter [UDP specification](/en/docs/spec/udp-bittorrent-announces/) zu finden.
Im zzzot 0.20.0-beta2 implementiert.
In i2psnark ab API 0.9.67 implementiert.
Überprüfen Sie die Dokumentation anderer Implementierungen für den Status.


## Überblick

Dieser Vorschlag bezieht sich auf die Implementierung von UDP-Trackern in I2P.


### Änderungsverlauf

Ein vorläufiger Vorschlag für UDP-Tracker in I2P wurde im Mai 2014 auf unserer Bittorrent-Spezifikationsseite [/en/docs/applications/bittorrent/](/en/docs/applications/bittorrent/) gepostet; dies war vor unserem formalen Vorschlagsprozess und wurde nie implementiert.
Dieser Vorschlag wurde Anfang 2022 erstellt und vereinfacht die Version von 2014.

Da dieser Vorschlag auf replizierbaren Datagrammen basiert, wurde er auf Eis gelegt, sobald wir Anfang 2023 mit der Arbeit an dem Vorschlag Datagram2 [/en/proposals/163-datagram2/](/en/proposals/163-datagram2/) begannen.
Dieser Vorschlag wurde im April 2025 genehmigt.

Die Version von 2023 dieses Vorschlags spezifizierte zwei Modi, "Kompatibilität" und "Schnell".
Weitere Analysen ergaben, dass der Schnellmodus unsicher wäre und auch für Clients mit einer großen Anzahl von Torrents ineffizient wäre.
Außerdem zeigte BiglyBT eine Präferenz für den Kompatibilitätsmodus.
Dieser Modus wird einfacher für jeden Tracker oder Client zu implementieren sein, der den Standard [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) unterstützt.

Obwohl der Kompatibilitätsmodus komplexer ist, von Grund auf auf der Client-Seite zu implementieren, haben wir bereits 2023 mit der Vorabprogrammierung begonnen.

Daher ist die aktuelle Version hier weiter vereinfacht, um den Schnellmodus zu entfernen und den Begriff "Kompatibilität" zu streichen. Die aktuelle Version wechselt zum neuen Datagram2-Format und fügt Referenzen zum UDP-Announce-Erweiterungsprotokoll [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) hinzu.

Außerdem wird ein Verbindungs-ID-Lebensdauerfeld zur Verbindungsantwort hinzugefügt, um die Effizienzgewinne dieses Protokolls zu erweitern.


## Motivation

Da die Benutzerbasis im Allgemeinen und die Zahl der Bittorrent-Nutzer im Besonderen weiter wächst, müssen wir Tracker und Ankündigungen effizienter gestalten, damit Tracker nicht überlastet werden.

Bittorrent schlug UDP-Tracker in BEP 15 [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) im Jahr 2008 vor, und die überwiegende Mehrheit der Tracker auf Clearnet ist jetzt ausschließlich UDP.

Es ist schwierig, die Bandbreiteneinsparungen von Datagrammen im Vergleich zum Streaming-Protokoll zu berechnen.
Eine replizierbare Anfrage ist in etwa so groß wie ein Streaming-SYN, aber die Nutzlast ist etwa 500 Bytes kleiner, da der HTTP-GET über einen riesigen 600-Byte-URL-Parameterstring verfügt.
Die rohe Antwort ist viel kleiner als ein Streaming-SYN-ACK und ermöglicht eine signifikante Reduzierung des ausgehenden Datenverkehrs eines Trackers.

Zusätzlich sollte es implementationsspezifische Speichereinsparungen geben, da Datagramme viel weniger Speicherzustand als eine Streaming-Verbindung erfordern.

Post-Quantum-Verschlüsselung und -Signaturen, wie in [/en/proposals/169-pq-crypto/](/en/proposals/169-pq-crypto/) vorgestellt, werden den Overhead von verschlüsselten und signierten Strukturen, einschließlich Ziele, Leasesets, Streaming-SYN und -ACK, erheblich erhöhen. Es ist wichtig, diesen Overhead, wo immer möglich, vor der Einführung von PQ-Krypto in I2P zu minimieren.


## Design

Dieser Vorschlag verwendet replizierbare Datagram2, replizierbare Datagram3 und rohe Datagramme, wie in [/en/docs/spec/datagrams/](/en/docs/spec/datagrams/) definiert.
Datagram2 und Datagram3 sind neue Varianten von replizierbaren Datagrammen, definiert in Vorschlag 163 [/en/proposals/163-datagram2/](/en/proposals/163-datagram2/).
Datagram2 fügt Wiederstand und Offline-Signaturunterstützung hinzu.
Datagram3 ist kleiner als das alte Datagram-Format, jedoch ohne Authentifizierung.


### BEP 15

Zur Referenz ist der Nachrichtenfluss, wie in [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) definiert, wie folgt:

```
Client                        Tracker
    Connect Req. ------------->
      <-------------- Connect Resp.
    Announce Req. ------------->
      <-------------- Announce Resp.
    Announce Req. ------------->
      <-------------- Announce Resp.
```

Die Verbindungsphase ist erforderlich, um IP-Adressen-Spoofing zu verhindern.
Der Tracker gibt eine Verbindungs-ID zurück, die der Client in späteren Ankündigungen verwendet.
Diese Verbindungs-ID läuft standardmäßig nach einer Minute beim Client und nach zwei Minuten beim Tracker ab.

I2P wird denselben Nachrichtenfluss wie BEP 15 verwenden, um die Einführung in bestehende UDP-fähige Client-Codebasen zu vereinfachen: für Effizienz und aus Sicherheitsgründen, die unten diskutiert werden:

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

Dies bietet potenziell große Bandbreiteneinsparungen im Vergleich zu Streaming (TCP)-Ankündigungen.
Während das Datagram2 etwa so groß wie ein Streaming-SYN ist, ist die rohe Antwort viel kleiner als das Streaming-SYN-ACK.
Nachfolgende Anfragen verwenden Datagram3, und die nachfolgenden Antworten sind roh.

Die Ankündigungsanfragen sind Datagram3, sodass der Tracker keine große Zuordnungstabelle der Verbindungs-IDs zur Ankündigungs-Zieladresse oder zum Hash führen muss.
Stattdessen kann der Tracker Verbindungs-IDs kryptografisch aus dem Sender-Hash, dem aktuellen Zeitstempel (basierend auf einem Intervall) und einem geheimen Wert generieren.
Wenn eine Ankündigungsanfrage empfangen wird, validiert der Tracker die Verbindungs-ID und verwendet den Datagram3-Sender-Hash als Sendziel.


### Tracker/Client-Unterstützung

Für eine integrierte Anwendung (Router und Client in einem Prozess, z. B. i2psnark und das ZzzOT-Java-Plugin) oder für eine auf I2CP basierende Anwendung (z. B. BiglyBT) sollte es einfach sein, den Streaming- und Datagram-Verkehr separat zu implementieren und zu routen.
Es wird erwartet, dass ZzzOT und i2psnark die ersten Tracker und Client sind, die diesen Vorschlag implementieren.

Nicht-integrierte Tracker und Clients werden unten diskutiert.


Tracker
````````

Es gibt vier bekannte I2P-Tracker-Implementierungen:

- zzzot, ein integriertes Java-Router-Plugin, läuft bei opentracker.dg2.i2p und mehreren anderen
- tracker2.postman.i2p, läuft vermutlich hinter einem Java-Router und HTTP-Server-Tunnel
- Der alte C-Opentracker, portiert von zzz, mit auskommentierter UDP-Unterstützung
- Der neue C-Opentracker, portiert von r4sas, läuft bei opentracker.r4sas.i2p und möglicherweise anderen, läuft vermutlich hinter einem i2pd-Router und HTTP-Server-Tunnel

Für eine externe Tracker-Anwendung, die momentan einen HTTP-Server-Tunnel verwendet, um Ankündigungsanfragen zu empfangen, könnte die Implementierung recht schwierig sein.
Ein spezialisierter Tunnel könnte entwickelt werden, um Datagramme in lokale HTTP-Anfragen/-Antworten zu übersetzen.
Oder, ein spezialisierter Tunnel, der sowohl HTTP-Anfragen als auch Datagramme behandelt, könnte entworfen werden, der die Datagramme an den externen Prozess weiterleiten würde.
Diese Designentscheidungen werden stark von den spezifischen Router- und Tracker-Implementierungen abhängen und liegen außerhalb des Anwendungsbereichs dieses Vorschlags.


Clients
```````
Externe SAM-basierte Torrent-Clients wie qbittorrent und andere libtorrent-basierte Clients würden SAM v3.3 benötigen [/en/docs/api/samv3/](/en/docs/api/samv3/), welches von i2pd nicht unterstützt wird.
Dies ist auch für die DHT-Unterstützung erforderlich und komplex genug, dass kein bekannter SAM-Torrent-Client es implementiert hat.
Keine SAM-basierten Implementierungen dieses Vorschlags werden in naher Zukunft erwartet.


### Verbindungs-Lebensdauer

[BEP 15](http://www.bittorrent.org/beps/bep_0015.html) spezifiziert, dass die Verbindungs-ID beim Client nach einer Minute und beim Tracker nach zwei Minuten abläuft.
Es ist nicht konfigurierbar.
Dies begrenzt die potenziellen Effizienzgewinne, außer die Clients würden Ankündigungen bündeln, um alle innerhalb eines Ein-Minuten-Fensters zu erfolgen.
i2psnark bündelt derzeit keine Ankündigungen; es streut sie, um Verkehrsspitzen zu vermeiden.
Power-User sollen Berichten zufolge Tausende von Torrents gleichzeitig betreiben, und so viele Ankündigungen in einer Minute zu bündeln, ist nicht realistisch.

Wir schlagen hier vor, die Verbindungsantwort zu erweitern, um ein optionales Verbindungs-Lebensdauer-Feld hinzuzufügen.
Der Standard, falls nicht vorhanden, ist eine Minute. Andernfalls soll die in Sekunden angegebene Lebensdauer vom Client verwendet werden, und der Tracker wird die Verbindungs-ID eine Minute länger halten.


### Kompatibilität mit BEP 15

Dieses Design bewahrt soweit wie möglich die Kompatibilität mit [BEP 15](http://www.bittorrent.org/beps/bep_0015.html), um die erforderlichen Änderungen in bestehenden Clients und Trackern zu begrenzen.

Die einzige erforderliche Änderung ist das Format der Peer-Information in der Ankündigungsantwort.
Das Hinzufügen des Lebensdauer-Feldes in der Verbindungsantwort ist nicht erforderlich, wird jedoch dringend zur Effizienzsteigerung empfohlen, wie oben erklärt.



### Sicherheitsanalyse

Ein wichtiges Ziel eines UDP-Announce-Protokolls ist es, Adressen-Spoofing zu verhindern.
Der Client muss tatsächlich existieren und ein echtes Leaseset bündeln.
Er muss eingehende Tunnel haben, um die Verbindungsantwort zu erhalten.
Diese Tunnel könnten Zero-Hop und sofort aufgebaut sein, aber das würde den Ersteller exponieren.
Dieses Protokoll erreicht dieses Ziel.



### Probleme

- Dieser Vorschlag unterstützt keine geblindeten Ziele,
  könnte jedoch erweitert werden, um dies zu tun. Siehe unten.




## Spezifikation

### Protokolle und Ports

Replizierbare Datagram2 verwendet I2CP-Protokoll 19;
replizierbare Datagram3 verwendet I2CP-Protokoll 20;
rohe Datagramme verwenden I2CP-Protokoll 18.
Anfragen können Datagram2 oder Datagram3 sein. Antworten sind immer roh.
Das ältere replizierbare Datagram ("Datagram1")-Format, das I2CP-Protokoll 17 verwendet, darf NICHT für Anfragen oder Antworten verwendet werden; diese müssen verworfen werden, wenn sie auf den Anfragen-/Antwort-Ports empfangen werden. Beachten Sie, dass Datagram1-Protokoll 17 noch für das DHT-Protokoll verwendet wird.

Anfragen verwenden den I2CP-"zu-Port" aus der Announce-URL; siehe unten.
Der Anfragen-"Von-Port" wird vom Client gewählt, sollte aber nicht Null sein und sich von denen unterscheiden, die von DHT verwendet werden, damit Antworten leicht klassifiziert werden können.
Tracker sollten Anfragen ablehnen, die auf dem falschen Port empfangen werden.

Antworten verwenden den I2CP-"zu-Port" aus der Anfrage.
Der Anfragen-"Von-Port" ist der "zu-Port" aus der Anfrage.


### Ankündigungs-URL

Das Format der Ankündigungs-URL ist in [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) nicht spezifiziert, aber wie im Clearnet sind UDP-Ankündigungs-URLs in der Form "udp://host:port/path".
Der Pfad wird ignoriert und kann leer sein, ist jedoch auf Clearnet typischerweise "/announce".
Der :port-Teil sollte immer vorhanden sein, jedoch gilt, wenn der ":port"-Teil weggelassen wird, verwenden Sie einen Standard I2CP-Port von 6969, da dies der übliche Port auf Clearnet ist.
Es können auch CGI-Parameter &a=b&c=d angehängt werden, diese können verarbeitet und in der Announce-Anfrage bereitgestellt werden, siehe [BEP 41](http://www.bittorrent.org/beps/bep_0041.html).
Wenn keine Parameter oder kein Pfad vorhanden sind, kann auch der abschließende / weggelassen werden, wie in [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) impliziert.


### Datagram-Formate

Alle Werte werden in Netzwerk-Byte-Reihenfolge (Big Endian) gesendet.
Erwarten Sie nicht, dass Pakete eine bestimmte Größe haben.
Zukünftige Erweiterungen könnten die Größe von Paketen erhöhen.



Connect-Anfrage
```````````````

Client zum Tracker.
16 Bytes. Muss replizierbar Datagram2 sein. Gleich wie in [BEP 15](http://www.bittorrent.org/beps/bep_0015.html). Keine Änderungen.


```
Offset  Größe            Name            Wert
  0       64-Bit Ganzzahl  protocol_id     0x41727101980 // magische Konstante
  8       32-Bit Ganzzahl  action          0 // verbinden
  12      32-Bit Ganzzahl  transaction_id
```



Connect-Antwort
````````````````

Tracker zum Client.
16 oder 18 Bytes. Muss roh sein. Gleich wie in [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) außer wie unten angegeben.


```
Offset  Größe            Name            Wert
  0       32-Bit Ganzzahl  action          0 // verbinden
  4       32-Bit Ganzzahl  transaction_id
  8       64-Bit Ganzzahl  connection_id
  16      16-Bit Ganzzahl  lifetime        optional  // Änderung von BEP 15
```

Die Antwort MUSS an den I2CP-"zu-Port" gesendet werden, der als Anfragen-"Von-Port" empfangen wurde.

Das Lebensdauer-Feld ist optional und gibt die Verbindungs-ID-Client-Lebensdauer in Sekunden an.
Standardmäßig ist diese 60 und das Minimum, falls angegeben, ist 60.
Das Maximum beträgt 65535 oder etwa 18 Stunden.
Der Tracker sollte die Verbindungs-ID 60 Sekunden länger als die Client-Lebensdauer speichern.



Ankündigungsanfrage
````````````````

Client zum Tracker.
Mindestens 98 Bytes. Muss replizierbarer Datagram3 sein. Gleich wie in [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) außer wie unten angegeben.

Die Verbindungs-ID ist wie in der Verbindungsantwort erhalten.



```
Offset  Größe            Name            Wert
  0       64-Bit Ganzzahl  connection_id
  8       32-Bit Ganzzahl  action          1     // ankündigen
  12      32-Bit Ganzzahl  transaction_id
  16      20-Byte Zeichenkette  info_hash
  36      20-Byte Zeichenkette  peer_id
  56      64-Bit Ganzzahl  downloaded
  64      64-Bit Ganzzahl  left
  72      64-Bit Ganzzahl  uploaded
  80      32-Bit Ganzzahl  event           0     // 0: keine; 1: abgeschlossen; 2: gestartet; 3: gestoppt
  84      32-Bit Ganzzahl  IP-Adresse      0     // Standard
  88      32-Bit Ganzzahl  key
  92      32-Bit Ganzzahl  num_want        -1    // Standard
  96      16-Bit Ganzzahl  port
  98      variiert         Optionen     optional  // Wie in BEP 41 angegeben
```

Änderungen von [BEP 15](http://www.bittorrent.org/beps/bep_0015.html):

- key wird ignoriert
- port wird wahrscheinlich ignoriert
- Der Optionsbereich, falls vorhanden, ist wie in [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) definiert

Die Antwort MUSS an den I2CP-"zu-Port" gesendet werden, der als Anfragen-"Von-Port" empfangen wurde.
Verwenden Sie nicht den Port aus der Ankündigungsanfrage.



Ankündigungsantwort
`````````````````

Tracker zum Client.
Mindestens 20 Bytes. Muss roh sein. Gleich wie in [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) außer wie unten angegeben.



```
Offset  Größe            Name            Wert
  0           32-Bit Ganzzahl  action          1 // ankündigen
  4           32-Bit Ganzzahl  transaction_id
  8           32-Bit Ganzzahl  interval
  12          32-Bit Ganzzahl  leechers
  16          32-Bit Ganzzahl  seeders
  20   32 * n 32-Byte hash    Binäre Hashes     // Änderung von BEP 15
  ...                                           // Änderung von BEP 15
```

Änderungen von [BEP 15](http://www.bittorrent.org/beps/bep_0015.html):

- Anstatt 6-Byte IPv4+port oder 18-Byte IPv6+port, geben wir
  multiple 32-Byte "kompakte Antworten" mit den SHA-256-binären Peer-Hashes zurück.
  Wie bei TCP-kompakten Antworten, enthalten wir keinen Port.

Die Antwort MUSS an den I2CP-"zu-Port" gesendet werden, der als Anfragen-"Von-Port" empfangen wurde.
Verwenden Sie nicht den Port aus der Ankündigungsanfrage.

I2P-Datagramme haben eine sehr große maximale Größe von etwa 64 KB;
jedoch sollten für zuverlässige Übertragung Datagramme, die größer als 4 KB sind, vermieden werden.
Für Bandbreiteneffizienz sollten Tracker die maximalen Peers wahrscheinlich auf etwa 50 begrenzen, was etwa einem 1600-byte-Paket vor Overhead auf verschiedenen Schichten entspricht und innerhalb eines Zwei-Tunnel-Nachrichten-Payload-Limits nach Fragmentierung liegen sollte.

Wie in BEP 15 ist keine Zählung der Zahl der Peer-Adressen
(IP/port für BEP 15, hier Hashes) enthalten, die folgen.
Obwohl in BEP 15 nicht erwogen, könnte ein End-of-Peers-Marker
aus allen Nullen definiert werden, um anzuzeigen, dass die Peer-Info vollständig ist
und einige Erweiterungsdaten folgen.

Damit Erweiterung in der Zukunft möglich ist, sollten Clients
einen 32-byte all-Zeros-Hash ignorieren, und alle Daten, die folgen.
Tracker sollten Ankündigungen von einem All-Zeros-Hash ablehnen,
obwohl dieser Hash bereits von Java-Routern verboten ist.


Scrape
``````

Scrape-Anfrage/antwort von [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) ist in diesem Vorschlag nicht erforderlich,
kann jedoch implementiert werden, wenn gewünscht, keine Änderungen erforderlich.
Der Client muss zuerst eine Verbindungs-ID erwerben.
Die Scrape-Anfrage ist immer replizierbarer Datagram3.
Die Scrape-Antwort ist immer roh.



Fehlerantwort
``````````````

Tracker zum Client.
Mindestens 8 Bytes (wenn die Nachricht leer ist).
Muss roh sein. Gleich wie in [BEP 15](http://www.bittorrent.org/beps/bep_0015.html). Keine Änderungen.

```

Offset  Größe            Name            Wert
  0       32-Bit Ganzzahl  action          3 // Fehler
  4       32-Bit Ganzzahl  transaction_id
  8       Zeichenkette     Nachricht

```



## Erweiterungen

Erweiterungsflags oder ein Versionsfeld sind nicht enthalten.
Clients und Tracker sollten nicht erwarten, dass Pakete eine bestimmte Größe haben.
Auf diese Weise können zusätzliche Felder hinzugefügt werden, ohne die Kompatibilität zu brechen.
Das in [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) definierte Erweiterungsformat wird empfohlen, falls erforderlich.

Die Verbindungsantwort wird modifiziert, um ein optionales Verbindungs-ID-Lebensdauerfeld hinzuzufügen.

Wenn eine Unterstützung für geblendete Ziele erforderlich ist, können wir entweder die
geblendete 35-Byte-Adresse am Ende der Ankündigungsanfrage hinzufügen,
oder geblendete Hashes in den Antworten anfordern,
mit dem [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) Format (Parameter TBD).
Die Menge der geblendeten 35-Byte-Peer-Adressen könnte am Ende der Ankündigungsantwort hinzugefügt werden,
nach einem kompletten All-Zeros-32-Byte-Hash.



## Implementierungsrichtlinien

Siehe den Design-Abschnitt oben für eine Diskussion der Herausforderungen für
nicht-integrierte, nicht-I2CP-Clients und -Tracker.


### Clients

Für einen bestimmten Tracker-Hostnamen sollte ein Client UDP-URLs gegenüber HTTP-URLs bevorzugen,
und nicht an beide ankündigen.

Clients mit vorhandener BEP 15-Unterstützung sollten nur kleine Änderungen erfordern.

Wenn ein Client DHT- oder andere Datagram-Protokolle unterstützt,
sollte er wahrscheinlich einen anderen Port als den Anfrage-"Von-Port" wählen,
damit die Antworten an diesen Port zurückkommen und nicht mit DHT-Nachrichten vermischt werden.
Der Client empfängt nur rohe Datagramme als Antworten.
Tracker werden niemals ein replizierbares Datagram2 an den Client senden.

Clients mit einer Standardliste von Opentrackern sollten diese aktualisieren, um UDP-URLs hinzuzufügen,
nachdem die bekannten Opentracker bekannt sind, UDP zu unterstützen.

Clients können oder müssen keine erneute Übertragung von Anfragen implementieren.
Erneute Übertragungen, wenn implementiert, sollten eine Anfangszeitüberschreitung
von mindestens 15 Sekunden verwenden und die Zeitüberschreitung für jede erneute Übertragung verdoppeln
(exponentielles Backoff).

Clients müssen zurückweichen, nachdem sie eine Fehlerantwort erhalten haben.


### Tracker

Tracker mit bestehender BEP 15-Unterstützung sollten nur kleine Änderungen erfordern.
Dieser Vorschlag unterscheidet sich vom Vorschlag von 2014 darin, dass der Tracker
den Empfang von replizierbarem Datagram2 und Datagram3 auf demselben Port unterstützen muss.

Um die Anforderungen an die Tracker-Ressourcen zu minimieren,
ist dieses Protokoll darauf ausgelegt, jegliche Anforderung zu eliminieren, dass der Tracker
Zuordnungen von Client-Hashes zu Verbindungs-IDs zur späteren Validierung speichern muss.
Dies ist möglich, weil das Ankündigungspaket ein replizierbares
Datagram3-Paket ist und somit den Sender-Hash enthält.

Eine empfohlene Implementierung ist:

- Definieren Sie den aktuellen Epoch-Wert als die aktuelle Zeit mit einer Auflösung der Verbindungs-Lebensdauer,
  ``epoch = jetzt / lebensdauer``.
- Definieren Sie eine kryptografische Hash-Funktion ``H(secret, clienthash, epoch)``, die eine 8-Byte-Ausgabe erzeugt.
- Generieren Sie die zufällige konstante Secret, die für alle Verbindungen verwendet wird.
- Für Verbindungsantworten generieren Sie ``connection_id = H(secret, clienthash, epoch)``
- Für Ankündigungsanfragen validieren Sie die empfangene Verbindungs-ID in der aktuellen Epoche, indem Sie überprüfen
  ``connection_id == H(secret, clienthash, epoch) || connection_id == H(secret, clienthash, epoch - 1)``


## Migration

Bestehende Clients unterstützen keine UDP-Announce-URLs und ignorieren sie.

Bestehende Tracker unterstützen keinen Empfang von replizierbaren oder rohen Datagrammen, sie werden verworfen.

Dieser Vorschlag ist völlig optional. Weder Clients noch Tracker sind zu einem beliebigen Zeitpunkt verpflichtet, ihn zu implementieren.



## Rollout

Es wird erwartet, dass die ersten Implementierungen in ZzzOT und i2psnark sein werden.
Sie werden für das Testen und die Überprüfung dieses Vorschlags verwendet.

Andere Implementierungen werden je nach Bedarf folgen, nachdem die Tests und Überprüfungen abgeschlossen sind.




