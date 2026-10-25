---
title: "SAM V1 Spezifikation"
description: "Legacy Simple Anonymous Messaging Protokoll Version 1 (veraltet)"
slug: "sam"
aliases:
  - "/de/docs/api/sam"
  - "/de/docs/api/sam/"
  - "/de/sam"
  - "/de/sam/"
lastUpdated: "2025-03"
accurateFor: "0.9.20"
---

## Warnung - Veraltet - Nicht unterstützt - Verwende [SAMv3](/docs/api/samv3)

Unten spezifiziert ist Version 1 eines einfachen Client-Protokolls für die Interaktion mit I2P. Neuere Alternativen: [SAM V2](/docs/api/samv2), [SAM V3](/docs/api/samv3), [BOB](/docs/api/bob).

## Sprachbibliotheken für die SAMv1 API

- C
- C#
- Perl
- Python

Die Bibliotheken befinden sich im I2P-Quell-Repository.

### I2P 0.9.14 Änderungen

Die gemeldete Version bleibt "1.0".

- DEST GENERATE unterstützt jetzt einen SIGNATURE_TYPE Parameter.
- Der MIN Parameter in HELLO VERSION ist jetzt optional.
- Die MIN und MAX Parameter in HELLO VERSION unterstützen jetzt einstellige Versionen wie "3".

## Version 1 Protokoll

Die Client-Anwendung kommuniziert mit der SAM-Bridge, die alle I2P-Funktionalitäten übernimmt (unter Verwendung der Streaming-Bibliothek für virtuelle Streams oder I2CP direkt für asynchrone Nachrichten).

Die gesamte Kommunikation zwischen Client und SAM bridge ist unverschlüsselt und nicht authentifiziert über einen einzelnen TCP-Socket. Der Zugang zur SAM bridge sollte durch Firewalls oder andere Mittel geschützt werden (möglicherweise kann die bridge ACLs haben, welche IPs sie für Verbindungen akzeptiert).

Alle diese SAM-Nachrichten werden in einer einzigen Zeile in reinem ASCII gesendet und mit dem Zeilenschaltzeichen (\\n) beendet. Die unten gezeigte Formatierung dient lediglich der Lesbarkeit, und während die ersten beiden Wörter in jeder Nachricht in ihrer spezifischen Reihenfolge bleiben müssen, kann sich die Reihenfolge der Schlüssel=Wert-Paare ändern (z.B. sind sowohl "ONE TWO A=B C=D" als auch "ONE TWO C=D A=B" vollkommen gültige Konstruktionen). Darüber hinaus ist das Protokoll case-sensitiv (Groß-/Kleinschreibung wird unterschieden).

SAM-Nachrichten werden in UTF-8 interpretiert. Schlüssel=Wert-Paare müssen durch ein einzelnes Leerzeichen getrennt werden. Werte können in Anführungszeichen eingeschlossen werden, wenn sie Leerzeichen enthalten, z.B. key="long value text". Es gibt keinen Escape-Mechanismus.

Die Kommunikation kann drei verschiedene Formen annehmen:

- [Virtuelle Streams](/docs/api/streaming)
- [Beantwortbare Datagramme](/docs/specs/datagrams#repliable) (Nachrichten mit einem FROM-Feld)
- [Anonyme Datagramme](/docs/specs/datagrams#raw) (reine anonyme Nachrichten)

## SAM-Verbindungs-Handshake

Keine SAM-Kommunikation kann stattfinden, bis sich Client und Bridge auf eine Protokollversion geeinigt haben. Dies geschieht durch das Senden eines HELLO vom Client und einer HELLO REPLY von der Bridge:

```
HELLO VERSION MIN=$min MAX=$max
```
und

```
HELLO REPLY RESULT=$result VERSION=1.0
```
Ab I2P 0.9.14 ist der MIN-Parameter optional. Der MAX-Parameter muss angegeben werden und größer oder gleich "1" und kleiner als "2" sein, um Version 1 zu verwenden.

Der RESULT-Wert kann einer der folgenden sein:

- `OK`
- `NOVERSION`

## SAM Sessions

Eine SAM-Sitzung wird erstellt, indem ein Client einen Socket zur SAM-Brücke öffnet, einen Handshake durchführt und eine SESSION CREATE-Nachricht sendet. Die Sitzung endet, wenn der Socket getrennt wird.

Jede I2P Destination kann nur für eine SAM-Sitzung gleichzeitig verwendet werden und kann nur eine dieser Formen nutzen (Nachrichten, die über andere Formen empfangen werden, werden verworfen).

Die SESSION CREATE Nachricht, die vom Client an die Bridge gesendet wird, ist wie folgt:

```
SESSION CREATE
        STYLE={STREAM,DATAGRAM,RAW}
        DESTINATION={$name,TRANSIENT}
        [DIRECTION={BOTH,RECEIVE,CREATE}]
        [option=value]*
```
DESTINATION gibt an, welche Destination für das Senden und Empfangen von Nachrichten/Streams verwendet werden soll. Wenn ein $name angegeben wird, durchsucht die SAM-Bridge ihren eigenen lokalen Speicher (die sam.keys-Datei) nach einer zugehörigen Destination (und privatem Schlüssel). Wenn keine Zuordnung mit diesem Namen existiert, wird eine neue erstellt. Wenn die Destination als TRANSIENT angegeben wird, wird immer eine neue erstellt.

Beachten Sie, dass DESTINATION ein Bezeichner ist, *nicht* Base64-kodierte Daten. Um die Destination anzugeben, müssen Sie [SAM V3](/docs/api/samv3) verwenden.

Die DIRECTION kann nur für STREAM-Sitzungen angegeben werden und weist die Brücke an, dass der Client entweder Streams erstellen oder empfangen wird, oder beides. Wenn dies nicht angegeben wird, wird BOTH angenommen. Der Versuch, einen ausgehenden Stream zu erstellen, wenn DIRECTION=RECEIVE gesetzt ist, sollte zu einem Fehler führen, und eingehende Streams werden ignoriert, wenn DIRECTION=CREATE gesetzt ist.

Zusätzliche Optionen sollten in die I2P-Sitzungskonfiguration eingegeben werden, wenn sie nicht von der SAM-Brücke interpretiert werden (z.B. "tunnels.depthInbound=0"). Diese Optionen sind unten dokumentiert.

Die SAM bridge selbst sollte bereits konfiguriert sein, mit welchem router sie über I2P kommunizieren soll (obwohl es bei Bedarf möglicherweise eine Möglichkeit gibt, dies zu überschreiben, z.B. i2cp.tcp.host=localhost und i2cp.tcp.port=7654).

Nach dem Empfang der Session-Erstellungsnachricht antwortet die SAM-Bridge mit einer Session-Statusnachricht wie folgt:

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

Wenn es nicht in Ordnung ist, sollte die MESSAGE menschenlesbare Informationen darüber enthalten, warum die Sitzung nicht erstellt werden konnte.

Beachten Sie, dass keine Warnung ausgegeben wird, wenn der $name nicht gefunden wird und stattdessen ein temporäres Ziel erstellt wird. Beachten Sie, dass das tatsächliche temporäre Base64-Ziel nicht in der Antwort ausgegeben wird; es ist der $name oder TRANSIENT, wie in SESSION CREATE angegeben. Wenn Sie diese Funktionen benötigen, müssen Sie [SAM V3](/docs/api/samv3) verwenden.

## SAM Virtuelle Streams

Virtuelle Streams werden garantiert zuverlässig und in der richtigen Reihenfolge gesendet, mit Fehler- und Erfolgsbenachrichtigung sobald diese verfügbar ist.

Nach dem Aufbau der Session mit STYLE=STREAM können sowohl der Client als auch die SAM-Bridge asynchron verschiedene Nachrichten hin und her senden, um die Streams zu verwalten, wie unten aufgelistet:

```
STREAM CONNECT
       ID=$id
       DESTINATION=$destination
```
Dies stellt eine neue virtuelle Verbindung vom lokalen Ziel zum angegebenen Peer her und markiert sie mit der sitzungsbereichsspezifischen eindeutigen ID. Die eindeutige ID ist eine ASCII-Dezimalzahl von 1 bis (2^31-1).

Die $destination ist die Base-64-Darstellung der [Destination](/docs/specs/common-structures#type_Destination), welche 516 oder mehr Base-64-Zeichen (387 oder mehr Bytes in binärer Form) umfasst, abhängig vom Signaturtyp.

Die SAM-Brücke muss darauf mit einer Stream-Status-Nachricht antworten:

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

Auf der empfangenden Seite benachrichtigt die SAM bridge den Client einfach wie folgt:

```
STREAM CONNECTED
       DESTINATION=$destination
       ID=$id
```
Dies teilt dem Client mit, dass das angegebene Ziel eine virtuelle Verbindung mit ihm erstellt hat. Der folgende Datenstrom wird mit der angegebenen eindeutigen ID markiert, die eine ASCII-Basis-10-Ganzzahl von -1 bis -(2^31-1) ist.

Die $destination ist die Base64-Kodierung der [Destination](/docs/specs/common-structures#type_Destination), welche 516 oder mehr Base64-Zeichen (387 oder mehr Bytes in binärer Form) umfasst, abhängig vom Signaturtyp.

Wenn der Client Daten über die virtuelle Verbindung senden möchte, geht er wie folgt vor:

```
STREAM SEND
       ID=$id
       SIZE=$numBytes\n[$numBytes of data]
```
Dies fügt die angegebenen Daten zum Puffer hinzu, der über die virtuelle Verbindung an den Peer gesendet wird. Die Sendegröße $numBytes gibt an, wie viele 8-Bit-Bytes nach der Zeilenschaltung enthalten sind, was zwischen 1 und 32768 (32KB) liegen kann.

Die SAM-Brücke wird dann ihr Bestes tun, um die Nachricht so schnell und effizient wie möglich zu übermitteln, wobei sie möglicherweise mehrere SEND-Nachrichten zusammen puffert. Falls ein Fehler bei der Datenübermittlung auftritt oder die Gegenseite die Verbindung schließt, wird die SAM-Brücke dem Client mitteilen:

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

Wenn die Verbindung ordnungsgemäß vom anderen Peer geschlossen wurde, wird $result auf OK gesetzt. Wenn $result nicht OK ist, kann MESSAGE eine beschreibende Nachricht übermitteln, wie z.B. "peer unreachable", etc. Immer wenn ein Client die Verbindung schließen möchte, sendet er der SAM bridge die close-Nachricht:

```
STREAM CLOSE
       ID=$id
```
Die Bridge räumt dann auf, was sie benötigt, und verwirft diese ID - es können keine weiteren Nachrichten darüber gesendet oder empfangen werden.

Für die andere Seite der Kommunikation wird die SAM-Bridge die Daten umgehend weiterleiten, sobald der Peer Daten gesendet hat und diese für den Client verfügbar sind:

```
STREAM RECEIVED
       ID=$id
       SIZE=$numBytes\n[$numBytes of data]
```
Alle Streams werden implizit geschlossen, wenn die Verbindung zwischen der SAM bridge und dem Client getrennt wird.

## SAM Repliable Datagrams

Obwohl I2P nicht grundsätzlich eine FROM-Adresse enthält, wird zur einfacheren Verwendung eine zusätzliche Schicht als antwortfähige Datagramme bereitgestellt - ungeordnete und unzuverlässige Nachrichten von bis zu 31744 Bytes, die eine FROM-Adresse enthalten (wobei bis zu 1KB für Header-Material verbleibt). Diese FROM-Adresse wird intern von SAM authentifiziert (unter Verwendung des Signaturschlüssels der Destination zur Verifizierung der Quelle) und beinhaltet Schutz vor Replay-Angriffen.

Die Mindestgröße ist 1. Für beste Zustellungszuverlässigkeit wird eine maximale Größe von ungefähr 11 KB empfohlen.

Nach dem Aufbau einer SAM-Sitzung mit STYLE=DATAGRAM kann der Client an die SAM-Bridge senden:

```
DATAGRAM SEND
         DESTINATION=$destination
         SIZE=$numBytes\n[$numBytes of data]
```
Wenn ein Datagramm ankommt, liefert die Bridge es an den Client über:

```
DATAGRAM RECEIVED
         DESTINATION=$destination
         SIZE=$numBytes\n[$numBytes of data]
```
Das $destination ist die Base64-Kodierung der [Destination](/docs/specs/common-structures#type_Destination), die 516 oder mehr Base64-Zeichen (387 oder mehr Bytes in binärer Form) umfasst, abhängig vom Signaturtyp.

Die SAM-Bridge stellt dem Client niemals die Authentifizierungsheader oder andere Felder zur Verfügung, sondern lediglich die Daten, die der Absender bereitgestellt hat. Dies setzt sich fort, bis die Sitzung geschlossen wird (indem der Client die Verbindung trennt).

## SAM Anonyme Datagramme

Um das Maximum aus I2P's Bandbreite herauszuholen, ermöglicht SAM es Clients, anonyme Datagramme zu senden und zu empfangen, wobei Authentifizierung und Antwortinformationen dem Client selbst überlassen werden. Diese Datagramme sind unzuverlässig und ungeordnet und können bis zu 32768 Bytes groß sein.

Die Mindestgröße ist 1. Für beste Zustellzuverlässigkeit wird eine maximale Größe von ungefähr 11 KB empfohlen.

Nach dem Aufbau einer SAM-Sitzung mit STYLE=RAW kann der Client an die SAM-Bridge senden:

```
RAW SEND
    DESTINATION=$destination
    SIZE=$numBytes\n[$numBytes of data]
```
Die $destination ist die Base64-Darstellung der [Destination](/docs/specs/common-structures#type_Destination), die 516 oder mehr Base64-Zeichen (387 oder mehr Bytes in Binärform) umfasst, abhängig vom Signaturtyp.

Wenn ein rohes Datagramm ankommt, liefert die Brücke es an den Client über:

```
RAW RECEIVED
    SIZE=$numBytes\n[$numBytes of data]
```
## SAM Utility-Funktionalität

Die folgende Nachricht kann vom Client verwendet werden, um die SAM-Bridge nach Namensauflösung zu fragen:

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

Wenn NAME=ME, dann wird die Antwort das Ziel enthalten, das von der aktuellen Sitzung verwendet wird (nützlich, wenn Sie ein TRANSIENT-Ziel verwenden). Wenn $result nicht OK ist, kann MESSAGE eine beschreibende Nachricht übermitteln, wie z.B. "bad format", etc.

Die $destination ist die Base64-Kodierung der [Destination](/docs/specs/common-structures#type_Destination), welche 516 oder mehr Base64-Zeichen (387 oder mehr Bytes in binärer Form) umfasst, abhängig vom Signaturtyp.

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
Ab I2P 0.9.14 wird ein optionaler Parameter SIGNATURE_TYPE unterstützt. Der SIGNATURE_TYPE-Wert kann jeder Name (z.B. ECDSA_SHA256_P256, Groß-/Kleinschreibung unerheblich) oder jede Nummer (z.B. 1) sein, die von [Key Certificates](/docs/specs/common-structures#type_Certificate) unterstützt wird. Der Standard ist DSA_SHA1.

Die $destination ist die Base64-Darstellung der [Destination](/docs/specs/common-structures#type_Destination), welche 516 oder mehr Base64-Zeichen (387 oder mehr Bytes in binärer Form) umfasst, abhängig vom Signaturtyp.

Der $privkey ist die Base64-Kodierung der Verkettung aus dem [Destination](/docs/specs/common-structures#type_Destination) gefolgt vom [Private Key](/docs/specs/common-structures#type_PrivateKey) gefolgt vom [Signing Private Key](/docs/specs/common-structures#type_SigningPrivateKey), was 884 oder mehr Base64-Zeichen (663 oder mehr Bytes in binärer Form) entspricht, abhängig vom Signaturtyp.

## RESULT-Werte

Dies sind die Werte, die das RESULT-Feld enthalten kann, mit ihrer Bedeutung:

| Wert | Bedeutung |
|------|-----------|
| `OK` | Operation erfolgreich abgeschlossen |
| `CANT_REACH_PEER` | Der Peer existiert, kann aber nicht erreicht werden |
| `DUPLICATED_DEST` | Die angegebene Destination wird bereits verwendet |
| `I2P_ERROR` | Ein allgemeiner I2P-Fehler (z.B. I2CP-Verbindungsabbruch, etc.) |
| `INVALID_KEY` | Der angegebene Schlüssel ist nicht gültig (falsches Format, etc.) |
| `KEY_NOT_FOUND` | Das Namensystem kann den angegebenen Namen nicht auflösen |
| `PEER_NOT_FOUND` | Der Peer kann im Netzwerk nicht gefunden werden |
| `TIMEOUT` | Zeitüberschreitung beim Warten auf ein Ereignis (z.B. Peer-Antwort) |
## Tunnel-, I2CP- und Streaming-Optionen

Diese Optionen können als Name=Wert-Paare am Ende einer SAM SESSION CREATE-Zeile übergeben werden.

Alle Sitzungen können [I2CP-Optionen wie tunnel-Längen](/docs/protocol/i2cp#options) enthalten. STREAM-Sitzungen können [Streaming-lib-Optionen](/docs/api/streaming#options) enthalten. Siehe diese Referenzen für Optionsnamen und Standardwerte.

## Base 64 Hinweise

Base 64-Kodierung muss das I2P-Standard-Base 64-Alphabet "A-Z, a-z, 0-9, -, ~" verwenden.

## Client-Bibliothek-Implementierungen

Client-Bibliotheken sind für C, C++, C#, Perl und Python verfügbar. Diese befinden sich im Verzeichnis apps/sam/ im I2P Source Package.

## Standard-SAM-Konfiguration

Der Standard-SAM-Port ist 7656. SAM ist standardmäßig nicht im I2P Router aktiviert; es muss manuell gestartet oder so konfiguriert werden, dass es automatisch startet, auf der Konfigurationsseite für Clients in der Router-Konsole oder in der clients.config-Datei.
