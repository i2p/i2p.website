---
title: "SAM V2 Spezifikation"
description: "Legacy Simple Anonymous Messaging Protokoll Version 2 (veraltet)"
slug: "samv2"
aliases:
  - "/de/docs/api/samv2"
  - "/de/docs/api/samv2/"
  - "/de/samv2"
  - "/de/samv2/"
lastUpdated: "2025-03"
accurateFor: "0.9.20"
---

## Warnung - Veraltet - Nicht unterstützt - Verwenden Sie [SAMv3](/docs/api/samv3)

Nachfolgend ist Version 2 eines einfachen Client-Protokolls für die Interaktion mit I2P spezifiziert.

SAM V2 wurde in I2P-Version 0.6.1.31 eingeführt. Wesentliche Unterschiede zu SAM V1 sind mit "\*\*\*" markiert. Alternativen: [SAM V1](/docs/api/sam), [SAM V3](/docs/api/samv3), [BOB](/docs/api/bob).

## Änderungen in Version 2

SAM V2 wurde in I2P Release 0.6.1.31 eingeführt. Im Vergleich zu Version 1 bietet SAM v2 eine Möglichkeit, mehrere Sockets auf derselben I2P-Destination *parallel* zu verwalten, d.h. der Client muss nicht warten, bis Daten erfolgreich über einen Socket gesendet wurden, bevor er Daten über einen anderen Socket sendet. Alle Daten werden über denselben Client\<--\>SAM Socket übertragen. Für mehrere Sockets siehe [SAM V3](/docs/api/samv3).

### I2P 0.9.14 Änderungen

Die gemeldete Version bleibt "2.0".

- DEST GENERATE unterstützt jetzt einen SIGNATURE_TYPE Parameter.
- Der MIN Parameter in HELLO VERSION ist jetzt optional.
- Die MIN und MAX Parameter in HELLO VERSION unterstützen jetzt einstellige Versionsnummern wie "3".

## Version 2 Protokoll

Die Client-Anwendung kommuniziert mit der SAM-Bridge, die sich um die gesamte I2P-Funktionalität kümmert (unter Verwendung der Streaming-Bibliothek für virtuelle Streams oder I2CP direkt für asynchrone Nachrichten).

Die gesamte Client\<--\>SAM bridge Kommunikation erfolgt unverschlüsselt und nicht authentifiziert über einen einzigen TCP-Socket. Der Zugang zur SAM bridge sollte durch Firewalls oder andere Mittel geschützt werden (möglicherweise verfügt die bridge über ACLs, die festlegen, von welchen IPs sie Verbindungen akzeptiert).

Alle diese SAM-Nachrichten werden in einer einzigen Zeile in einfachem ASCII gesendet und mit dem Zeilenwechselzeichen (\\n) beendet. Die unten gezeigte Formatierung dient lediglich der Lesbarkeit, und während die ersten beiden Wörter in jeder Nachricht in ihrer spezifischen Reihenfolge bleiben müssen, kann die Reihenfolge der Schlüssel=Wert-Paare geändert werden (z.B. sind "ONE TWO A=B C=D" oder "ONE TWO C=D A=B" beide vollkommen gültige Konstruktionen). Außerdem ist das Protokoll case-sensitive (unterscheidet zwischen Groß- und Kleinschreibung).

SAM-Nachrichten werden in UTF-8 interpretiert. Schlüssel=Wert-Paare müssen durch ein einzelnes Leerzeichen getrennt werden. Werte können in Anführungszeichen gesetzt werden, wenn sie Leerzeichen enthalten, z.B. schlüssel="langer Wert Text". Es gibt keinen Escape-Mechanismus.

Kommunikation kann drei verschiedene Formen annehmen:

- [Virtuelle Streams](/docs/api/streaming)
- [Antwortbare Datagramme](/docs/specs/datagrams#repliable) (Nachrichten mit einem FROM-Feld)
- [Anonyme Datagramme](/docs/specs/datagrams#raw) (reine anonyme Nachrichten)

## SAM Connection Handshake

Es kann keine SAM-Kommunikation stattfinden, bis sich Client und Bridge auf eine Protokollversion geeinigt haben. Dies geschieht, indem der Client ein HELLO sendet und die Bridge mit einem HELLO REPLY antwortet:

```
HELLO VERSION MIN=$min MAX=$max
```
und

```
*** HELLO REPLY RESULT=$result VERSION=2.0
```
Seit I2P 0.9.14 ist der MIN-Parameter optional. Der MAX-Parameter muss angegeben werden und größer oder gleich "2" und kleiner als "3" sein, um Version 2 zu verwenden.

Der RESULT-Wert kann einer der folgenden sein:

- `OK`
- `NOVERSION`

## SAM Sessions

Eine SAM-Session wird erstellt, indem ein Client eine Socket-Verbindung zur SAM-Bridge öffnet, einen Handshake durchführt und eine SESSION CREATE-Nachricht sendet. Die Session wird beendet, wenn die Socket-Verbindung getrennt wird.

Jede I2P Destination kann nur für eine SAM-Sitzung gleichzeitig verwendet werden und kann nur eine dieser Formen nutzen (Nachrichten, die über andere Formen empfangen werden, werden verworfen).

Die SESSION CREATE-Nachricht, die vom Client an die Bridge gesendet wird, lautet wie folgt:

```
SESSION CREATE
        STYLE={STREAM,DATAGRAM,RAW}
        DESTINATION={$name,TRANSIENT}
        [DIRECTION={BOTH,RECEIVE,CREATE}]
        [option=value]*
```
DESTINATION gibt an, welches Ziel für das Senden und Empfangen von Nachrichten/Streams verwendet werden soll. Wenn ein $name angegeben wird, durchsucht die SAM-Brücke ihren eigenen lokalen Speicher (die sam.keys-Datei) nach einem zugehörigen Ziel (und privatem Schlüssel). Wenn keine Zuordnung mit diesem Namen existiert, wird eine neue erstellt. Wenn das Ziel als TRANSIENT angegeben wird, wird immer ein neues erstellt.

Beachten Sie, dass DESTINATION ein Bezeichner ist, *nicht* Base 64-kodierte Daten. Um die Destination anzugeben, müssen Sie [SAM V3](/docs/api/samv3) verwenden.

Die DIRECTION kann nur für STREAM-Sessions angegeben werden und teilt der Bridge mit, dass der Client entweder Streams erstellen oder empfangen wird, oder beides. Wenn dies nicht angegeben wird, wird BOTH angenommen. Der Versuch, einen ausgehenden Stream zu erstellen, wenn DIRECTION=RECEIVE gesetzt ist, sollte zu einem Fehler führen, und eingehende Streams werden ignoriert, wenn DIRECTION=CREATE gesetzt ist.

Zusätzliche Optionen sollten in die I2P-Session-Konfiguration eingespeist werden, falls sie nicht von der SAM-Bridge interpretiert werden (z.B. "tunnels.depthInbound=0"). Diese Optionen sind unten dokumentiert.

Die SAM-Brücke selbst sollte bereits damit konfiguriert sein, über welchen router sie über I2P kommunizieren soll (obwohl es bei Bedarf möglicherweise eine Möglichkeit gibt, dies zu überschreiben, z.B. i2cp.tcp.host=localhost und i2cp.tcp.port=7654).

Nach Erhalt der Session-Create-Nachricht antwortet die SAM bridge mit einer Session-Status-Nachricht wie folgt:

```
SESSION STATUS
        RESULT=$result
        DESTINATION={$name,TRANSIENT}
        [MESSAGE=...]
```
Der RESULT-Wert kann einer der folgenden sein:

- `OK`
- `DUPLICATED_DEST`
- `I2P_ERROR`
- `INVALID_KEY`

Wenn es nicht OK ist, sollte die MESSAGE menschenlesbare Informationen darüber enthalten, warum die Sitzung nicht erstellt werden konnte.

Beachten Sie, dass keine Warnung ausgegeben wird, wenn der $name nicht gefunden wird und stattdessen ein temporäres Ziel erstellt wird. Beachten Sie, dass das tatsächliche temporäre Base64-Ziel nicht in der Antwort ausgegeben wird; es ist der $name oder TRANSIENT, wie in SESSION CREATE angegeben. Wenn Sie diese Funktionen benötigen, müssen Sie [SAM V3](/docs/api/samv3) verwenden.

## SAM Virtual Streams

Virtuelle Streams werden garantiert zuverlässig und in der richtigen Reihenfolge gesendet, mit Fehler- und Erfolgsbenachrichtigung, sobald diese verfügbar ist.

Nach dem Aufbau der Sitzung mit STYLE=STREAM können sowohl der Client als auch die SAM-Bridge asynchron verschiedene Nachrichten hin und her senden, um die Streams zu verwalten, wie unten aufgelistet:

```
STREAM CONNECT
       ID=$id
       DESTINATION=$destination
```
Dies stellt eine neue virtuelle Verbindung vom lokalen Ziel zum angegebenen Peer her und markiert sie mit der sitzungsbasierten eindeutigen ID. Die eindeutige ID ist eine ASCII-Base-10-Ganzzahl von 1 bis (2^31-1).

Das $destination ist die Base64-Kodierung der [Destination](/docs/specs/common-structures#type_Destination), die 516 oder mehr Base64-Zeichen (387 oder mehr Bytes in binärer Form) umfasst, abhängig vom Signaturtyp.

Die SAM bridge antwortet darauf mit einer Stream-Status-Nachricht:

```
STREAM STATUS
       RESULT=$result
       ID=$id
       [MESSAGE=...]
```
Der RESULT-Wert kann einer der folgenden sein:

- `OK`
- `CANT_REACH_PEER`
- `I2P_ERROR`
- `INVALID_KEY`
- `TIMEOUT`

Wenn das RESULT OK ist, ist das angegebene Ziel erreichbar und hat die Verbindung autorisiert; wenn die Verbindung nicht möglich war (Timeout, etc.), enthält RESULT den entsprechenden Fehlerwert (begleitet von einer optionalen menschenlesbaren MESSAGE).

Auf der Empfängerseite benachrichtigt die SAM bridge den Client einfach wie folgt:

```
STREAM CONNECTED
       DESTINATION=$destination
       ID=$id
```
Dies teilt dem Client mit, dass das angegebene Ziel eine virtuelle Verbindung mit ihm erstellt hat. Der folgende Datenstrom wird mit der angegebenen eindeutigen ID markiert, die eine ASCII-Base-10-Ganzzahl von -1 bis -(2^31-1) ist.

Das $destination ist die Base64-Kodierung der [Destination](/docs/specs/common-structures#type_Destination), welche 516 oder mehr Base64-Zeichen (387 oder mehr Bytes in binärer Form) umfasst, abhängig vom Signaturtyp.

Wenn der Client Daten über die virtuelle Verbindung senden möchte, geht er wie folgt vor:

```
STREAM SEND
       ID=$id
       SIZE=$numBytes\n[$numBytes of data]
```
Dies fordert die SAM bridge auf, die angegebenen Daten zum Puffer hinzuzufügen, der über die virtuelle Verbindung an den Peer gesendet wird. Die Sendegröße $numBytes gibt an, wie viele 8-Bit-Bytes nach dem Zeilenwechsel enthalten sind, was zwischen 1 und 32768 (32KB) liegen kann.

**\*\*\* Die SAM-Brücke antwortet sofort mit:**

```
*** STREAM SEND
***        ID=$id
***        RESULT=$result
***        STATE=$bufferState
```
**\*\*\*** wobei $bufferState sein kann:

- `BUFFER_FULL` - SAMs Puffer hat 32 oder mehr KB Daten zu senden, und nachfolgende SEND-Anfragen werden fehlschlagen
- `READY` - SAMs Puffer ist nicht voll, und die nächste SEND-Anfrage wird garantiert erfolgreich sein

**\*\*\*** und $result ist eines von:

- `OK` - die Daten wurden erfolgreich gepuffert
- `FAILED` - der Puffer war voll, keine Daten wurden gepuffert

**\*\*\*** Wenn die SAM bridge mit BUFFER_FULL geantwortet hat, wird sie eine weitere Nachricht senden, sobald ihr Puffer wieder verfügbar ist:

```
*** STREAM READY_TO_SEND ID=$id
```
**\*\*\*** Wenn das Ergebnis OK ist, wird die SAM-Brücke ihr Bestes geben, um die Nachricht so schnell und effizient wie möglich zu übermitteln, wobei möglicherweise mehrere SEND-Nachrichten zusammen gepuffert werden. Falls ein Fehler beim Übermitteln der Daten auftritt oder die Gegenseite die Verbindung schließt, wird die SAM-Brücke dem Client mitteilen:

```
STREAM CLOSED
       RESULT=$result
       ID=$id
       [MESSAGE=...]
```
Der RESULT-Wert kann einer der folgenden sein:

- `OK`
- `CANT_REACH_PEER`
- `I2P_ERROR`
- `PEER_NOT_FOUND`
- `TIMEOUT`

Wenn die Verbindung ordnungsgemäß vom anderen Peer geschlossen wurde, wird $result auf OK gesetzt. Wenn $result nicht OK ist, kann MESSAGE eine beschreibende Nachricht übermitteln, wie z.B. "peer unreachable", etc. Wann immer ein Client die Verbindung schließen möchte, sendet er der SAM bridge die close-Nachricht:

```
STREAM CLOSE
       ID=$id
```
Die Bridge räumt dann auf, was sie muss, und verwirft diese ID - es können keine weiteren Nachrichten darüber gesendet oder empfangen werden.

Für die andere Seite der Kommunikation wird die SAM-Bridge die Daten umgehend weiterleiten, sobald der Peer Daten gesendet hat und diese für den Client verfügbar sind:

```
STREAM RECEIVED
       ID=$id
       SIZE=$numBytes\n[$numBytes of data]
```
**\*\*\*** Mit SAM Version 2.0 muss der Client jedoch zuerst der SAM-Brücke mitteilen, wie viele eingehende Daten für die gesamte Sitzung erlaubt sind, indem er eine Nachricht sendet:

```
*** STREAM RECEIVE
***        ID=$id
***        LIMIT=$limit\n
```
**\*\*\*** wobei $limit sein kann:

- `NONE` - die SAM bridge wird weiter lauschen und eingehende Daten weiterleiten (gleiches Verhalten wie in Version 1.0)
- eine Ganzzahl (kleiner als 2^64) - die Anzahl der empfangenen Bytes, nach der die SAM bridge das Lauschen auf dem eingehenden Stream einstellt. Sobald der Client bereit ist, weitere Bytes vom Stream zu akzeptieren, muss er eine solche Nachricht erneut senden, mit einem größeren $limit.

**\*\*\*** Der Client muss solche STREAM RECEIVE-Nachrichten senden, nachdem die Verbindung zum Peer hergestellt wurde, d.h. nachdem der Client eine "STREAM CONNECTED"- oder eine "STREAM STATUS RESULT=OK"-Nachricht von der SAM-Bridge erhalten hat.

Alle Streams werden implizit geschlossen, wenn die Verbindung zwischen der SAM bridge und dem Client getrennt wird.

## SAM Repliable Datagrams

Obwohl I2P von sich aus keine FROM-Adresse enthält, wird zur Erleichterung der Nutzung eine zusätzliche Schicht als beantwortbare Datagramme bereitgestellt - ungeordnete und unzuverlässige Nachrichten von bis zu 31744 Bytes, die eine FROM-Adresse enthalten (wodurch bis zu 1KB für Header-Material verbleibt). Diese FROM-Adresse wird intern von SAM authentifiziert (unter Verwendung des Signaturschlüssels des Ziels zur Überprüfung der Quelle) und beinhaltet Schutz vor Replay-Angriffen.

Die Mindestgröße ist 1. Für beste Übertragungszuverlässigkeit wird eine maximale Größe von etwa 11 KB empfohlen.

Nach dem Aufbau einer SAM-Sitzung mit STYLE=DATAGRAM kann der Client an die SAM-Brücke senden:

```
DATAGRAM SEND
         DESTINATION=$destination
         SIZE=$numBytes\n[$numBytes of data]
```
Wenn ein Datagramm ankommt, leitet die Brücke es an den Client weiter über:

```
DATAGRAM RECEIVED
         DESTINATION=$destination
         SIZE=$numBytes\n[$numBytes of data]
```
Das $destination ist die Base64-Kodierung der [Destination](/docs/specs/common-structures#type_Destination), welche 516 oder mehr Base64-Zeichen (387 oder mehr Bytes in binärer Form) umfasst, abhängig vom Signaturtyp.

Die SAM-Brücke gibt niemals die Authentifizierungs-Header oder andere Felder an den Client weiter, sondern nur die Daten, die der Sender bereitgestellt hat. Dies geht so weiter, bis die Sitzung geschlossen wird (indem der Client die Verbindung trennt).

## SAM Anonyme Datagramme

Um das Beste aus I2Ps Bandbreite herauszuholen, ermöglicht SAM Clients das Senden und Empfangen anonymer Datagramme, wobei Authentifizierung und Antwortinformationen den Clients selbst überlassen bleiben. Diese Datagramme sind unzuverlässig und ungeordnet und können bis zu 32768 Bytes groß sein.

Die Mindestgröße beträgt 1. Für beste Zustellungszuverlässigkeit wird eine maximale Größe von etwa 11 KB empfohlen.

Nachdem eine SAM-Sitzung mit STYLE=RAW etabliert wurde, kann der Client an die SAM-Bridge senden:

```
RAW SEND
    DESTINATION=$destination
    SIZE=$numBytes\n[$numBytes of data]
```
Die $destination ist die Base64-Kodierung der [Destination](/docs/specs/common-structures#type_Destination), welche 516 oder mehr Base64-Zeichen (387 oder mehr Bytes in binärer Form) umfasst, abhängig vom Signaturtyp.

Wenn ein rohes Datagramm ankommt, liefert die Brücke es an den Client über:

```
RAW RECEIVED
    SIZE=$numBytes\n[$numBytes of data]
```
## SAM-Dienstprogramm-Funktionalität

Die folgende Nachricht kann vom Client verwendet werden, um die SAM-Bridge nach Namensauflösung abzufragen:

```
NAMING LOOKUP
       NAME=$name
```
was beantwortet wird durch

```
NAMING REPLY
       RESULT=$result
       NAME=$name
       [VALUE=$destination]
       [MESSAGE=$message]
```
Der RESULT-Wert kann einer der folgenden sein:

- `OK`
- `INVALID_KEY`
- `KEY_NOT_FOUND`

Wenn NAME=ME, dann enthält die Antwort das Ziel, das von der aktuellen Sitzung verwendet wird (nützlich, wenn Sie ein TRANSIENT verwenden). Wenn $result nicht OK ist, kann MESSAGE eine beschreibende Nachricht übermitteln, wie "bad format", etc.

Das $destination ist die Base64-Kodierung der [Destination](/docs/specs/common-structures#type_Destination), die 516 oder mehr Base64-Zeichen (387 oder mehr Bytes in binärer Form) umfasst, abhängig vom Signaturtyp.

Öffentliche und private base64-Schlüssel können mit der folgenden Nachricht generiert werden:

```
DEST GENERATE
```
was beantwortet wird durch

```
DEST REPLY
     PUB=$destination
     PRIV=$privkey
```
Seit I2P 0.9.14 wird ein optionaler Parameter SIGNATURE_TYPE unterstützt. Der SIGNATURE_TYPE-Wert kann ein beliebiger Name (z.B. ECDSA_SHA256_P256, Groß-/Kleinschreibung unbeachtet) oder eine Nummer (z.B. 1) sein, die von [Key Certificates](/docs/specs/common-structures#type_Certificate) unterstützt wird. Der Standard ist DSA_SHA1.

Das $destination ist die Base64-Darstellung der [Destination](/docs/specs/common-structures#type_Destination), die 516 oder mehr Base64-Zeichen (387 oder mehr Bytes in binärer Form) umfasst, je nach Signaturtyp.

Der $privkey ist die base 64-Codierung der Verkettung des [Destination](/docs/specs/common-structures#type_Destination), gefolgt vom [Private Key](/docs/specs/common-structures#type_PrivateKey), gefolgt vom [Signing Private Key](/docs/specs/common-structures#type_SigningPrivateKey), was 884 oder mehr base 64-Zeichen (663 oder mehr Bytes in binärer Form) entspricht, abhängig vom Signaturtyp.

## RESULT-Werte

Das sind die Werte, die das RESULT-Feld enthalten kann, mit ihrer Bedeutung:

| Wert | Bedeutung |
|------|-----------|
| `OK` | Operation erfolgreich abgeschlossen |
| `CANT_REACH_PEER` | Der Peer existiert, kann aber nicht erreicht werden |
| `DUPLICATED_DEST` | Das angegebene Destination wird bereits verwendet |
| `I2P_ERROR` | Ein allgemeiner I2P-Fehler (z.B. I2CP-Verbindungsabbruch, etc.) |
| `INVALID_KEY` | Der angegebene Schlüssel ist nicht gültig (falsches Format, etc.) |
| `KEY_NOT_FOUND` | Das Namensystem kann den angegebenen Namen nicht auflösen |
| `PEER_NOT_FOUND` | Der Peer kann im Netzwerk nicht gefunden werden |
| `TIMEOUT` | Zeitüberschreitung beim Warten auf ein Ereignis (z.B. Peer-Antwort) |
## Tunnel-, I2CP- und Streaming-Optionen

Diese Optionen können als name=wert-Paare am Ende einer SAM SESSION CREATE-Zeile übergeben werden.

Alle Sitzungen können [I2CP-Optionen wie tunnel-Längen](/docs/protocol/i2cp#options) enthalten. STREAM-Sitzungen können [Streaming-lib-Optionen](/docs/api/streaming#options) enthalten. Siehe diese Referenzen für Optionsnamen und Standardwerte.

## Base 64 Hinweise

Base 64-Kodierung muss das I2P-Standard Base 64-Alphabet "A-Z, a-z, 0-9, -, ~" verwenden.

## Client-Bibliothek-Implementierungen

Client-Bibliotheken sind verfügbar für C, C++, C#, Perl und Python. Diese befinden sich im Verzeichnis apps/sam/ im I2P Source Package. Einige könnten veraltet sein und wurden möglicherweise noch nicht für SAMv2-Unterstützung aktualisiert.

## Standard-SAM-Einrichtung

Der Standard-SAM-Port ist 7656. SAM ist standardmäßig im I2P Router nicht aktiviert; es muss manuell gestartet oder so konfiguriert werden, dass es automatisch startet, und zwar auf der Seite "Clients konfigurieren" in der Router-Konsole oder in der Datei clients.config.
