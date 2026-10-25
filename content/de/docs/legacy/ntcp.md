---
title: "NTCP (NIO-basiertes TCP)"
description: "Legacy Java NIO-basierter TCP-Transport für I2P, ersetzt durch NTCP2"
slug: "ntcp"
aliases:
  - "/de/docs/transport/ntcp"
  - "/de/docs/transport/ntcp/"
  - "/de/docs/ntcp"
  - "/de/docs/ntcp/"
  - "/de/ntcp"
  - "/de/ntcp/"
lastUpdated: "2021-10"
accurateFor: "0.9.52"
---

VERALTET, NICHT MEHR UNTERSTÜTZT. Standardmäßig deaktiviert seit 0.9.40 2019-05. Unterstützung entfernt seit 0.9.50 2021-05. Ersetzt durch [NTCP2](/docs/specs/ntcp2). NTCP ist ein Java NIO-basiertes Transport-Protokoll, das in I2P Version 0.6.1.22 eingeführt wurde. Java NIO (new I/O) leidet nicht unter den "1 Thread pro Verbindung"-Problemen des alten TCP-Transports. NTCP-über-IPv6 wird seit Version 0.9.8 unterstützt.

Standardmäßig verwendet NTCP die IP/Port, die automatisch von SSU erkannt wird. Wenn auf config.jsp aktiviert, benachrichtigt/startet SSU NTCP neu, wenn sich die externe Adresse ändert oder wenn sich der Firewall-Status ändert. Jetzt können Sie eingehende TCP-Verbindungen ohne statische IP oder dyndns-Service aktivieren.

Der NTCP-Code innerhalb von I2P ist relativ schlank (1/4 der Größe des SSU-Codes), da er den zugrundeliegenden Java TCP-Transport für zuverlässige Übertragung verwendet.

## Router Address Spezifikation {#ra}

Die folgenden Eigenschaften werden in der netDb gespeichert.

- **Transport-Name:** NTCP
- **host:** IP (IPv4 oder IPv6).
  Verkürzte IPv6-Adressen (mit "::") sind erlaubt.
  Hostnamen waren früher erlaubt, sind aber seit Version 0.9.32 veraltet. Siehe Vorschlag 141.
- **port:** 1024 - 65535

## NTCP-Protokoll-Spezifikation

### Standard-Nachrichtenformat

Nach der Einrichtung sendet der NTCP transport einzelne I2NP-Nachrichten mit einer einfachen Prüfsumme. Die unverschlüsselte Nachricht wird wie folgt kodiert:

```
+-------+-------+-------+-------+-------+-------+-------+-------+
| sizeof(data)  |                                               |
+-------+-------+                                               +
|                            data                               |
~                                                               ~
|                                                               |
+                                       +-------+-------+-------+
|                                       |        padding
+-------+-------+-------+-------+-------+-------+-------+-------+
                                | Adler checksum of sz+data+pad |
+-------+-------+-------+-------+-------+-------+-------+-------+
```
Die Daten werden dann mit AES/256/CBC verschlüsselt. Der Sitzungsschlüssel für die Verschlüsselung wird während der Verbindungsherstellung ausgehandelt (mit Diffie-Hellman 2048 Bit). Die Verbindungsherstellung zwischen zwei Routern ist in der EstablishState-Klasse implementiert und wird unten detailliert beschrieben. Der IV für die AES/256/CBC-Verschlüsselung sind die letzten 16 Bytes der vorherigen verschlüsselten Nachricht.

0-15 Bytes Padding sind erforderlich, um die Gesamtnachrichtenlänge (einschließlich der sechs Größen- und Prüfsummen-Bytes) auf ein Vielfaches von 16 zu bringen. Die maximale Nachrichtengröße beträgt derzeit 16 KB. Daher beträgt die maximale Datengröße derzeit 16 KB - 6, oder 16378 Bytes. Die minimale Datengröße beträgt 1.

### Zeit-Synchronisations-Nachrichtenformat

Ein Sonderfall ist eine Metadaten-Nachricht, bei der sizeof(data) gleich 0 ist. In diesem Fall wird die unverschlüsselte Nachricht folgendermaßen kodiert:

```
+-------+-------+-------+-------+-------+-------+-------+-------+
|       0       |      timestamp in seconds     | uninterpreted
+-------+-------+-------+-------+-------+-------+-------+-------+
        uninterpreted           | Adler checksum of bytes 0-11  |
+-------+-------+-------+-------+-------+-------+-------+-------+
```
Gesamtlänge: 16 Bytes. Die Zeitsynchronisationsnachricht wird in ungefähr 15-Minuten-Intervallen gesendet. Die Nachricht wird genauso verschlüsselt wie Standardnachrichten.

### Prüfsummen

Die Standard- und Zeitsynchronisationsnachrichten verwenden die Adler-32-Prüfsumme wie in der [ZLIB-Spezifikation](http://tools.ietf.org/html/rfc1950) definiert.

### Leerlauf-Timeout

Die Leerlauf-Zeitüberschreitung und das Schließen der Verbindung liegt im Ermessen jedes Endpunkts und kann variieren. Die aktuelle Implementierung reduziert die Zeitüberschreitung, wenn sich die Anzahl der Verbindungen dem konfigurierten Maximum nähert, und erhöht die Zeitüberschreitung, wenn die Verbindungsanzahl niedrig ist. Die empfohlene minimale Zeitüberschreitung beträgt zwei Minuten oder mehr, und die empfohlene maximale Zeitüberschreitung beträgt zehn Minuten oder mehr.

### RouterInfo-Austausch

Nach der Einrichtung und danach alle 30-60 Minuten sollten die beiden router im Allgemeinen RouterInfos über eine DatabaseStoreMessage austauschen. Alice sollte jedoch prüfen, ob die erste Nachricht in der Warteschlange eine DatabaseStoreMessage ist, um keine doppelte Nachricht zu senden; dies ist oft der Fall beim Verbinden mit einem floodfill router.

### Aufbausequenz

Im Establish-Status gibt es eine 4-phasige Nachrichtensequenz zum Austausch von DH-Schlüsseln und Signaturen. In den ersten beiden Nachrichten findet ein 2048-Bit Diffie-Hellman-Austausch statt. Anschließend werden Signaturen der kritischen Daten ausgetauscht, um die Verbindung zu bestätigen.

```
Alice                   contacts                      Bob
=========================================================
 X+(H(X) xor Bob.identHash)----------------------------->
 <----------------------------------------Y+E(H(X+Y)+tsB+padding, sk, Y[239:255])
 E(sz+Alice.identity+tsA+padding+S(X+Y+Bob.identHash+tsA+tsB), sk, hX_xor_Bob.identHash[16:31])--->
 <----------------------E(S(X+Y+Alice.identHash+tsA+tsB)+padding, sk, prev)
```
```
  Legend:
    X, Y: 256 byte DH public keys
    H(): 32 byte SHA256 Hash
    E(data, session key, IV): AES256 Encrypt
    S(): Signature
    tsA, tsB: timestamps (4 bytes, seconds since epoch)
    sk: 32 byte Session key
    sz: 2 byte size of Alice identity to follow
```
#### DH-Schlüsselaustausch {#DH}

Der initiale 2048-Bit DH-Schlüsselaustausch verwendet dieselbe geteilte Primzahl (p) und denselben Generator (g) wie die [ElGamal-Verschlüsselung](/docs/specs/cryptography#elgamal) von I2P.

Der DH-Schlüsselaustausch besteht aus mehreren Schritten, die unten dargestellt sind. Die Zuordnung zwischen diesen Schritten und den zwischen I2P-Routern gesendeten Nachrichten ist fett markiert.

1. Alice generiert eine geheime ganze Zahl x. Sie berechnet dann `X = g^x mod p`.
2. Alice sendet X an Bob **(Nachricht 1)**.
3. Bob generiert eine geheime ganze Zahl y. Er berechnet dann `Y = g^y mod p`.
4. Bob sendet Y an Alice. **(Nachricht 2)**
5. Alice kann nun `sessionKey = Y^x mod p` berechnen.
6. Bob kann nun `sessionKey = X^y mod p` berechnen.
7. Sowohl Alice als auch Bob haben nun einen gemeinsamen Schlüssel `sessionKey = g^(x*y) mod p`.

Der sessionKey wird dann verwendet, um Identitäten in **Nachricht 3** und **Nachricht 4** auszutauschen. Die Exponentenlänge (x und y) für den DH-Austausch ist auf der [Kryptografie-Seite](/docs/specs/cryptography#exponent) dokumentiert.

#### Session Key Details

Der 32-Byte-Sitzungsschlüssel wird wie folgt erstellt:

1. Nimm den ausgetauschten DH-Schlüssel, dargestellt als positives Byte-Array minimaler Länge eines BigInteger (Zweierkomplement Big-Endian)
2. Wenn das höchstwertige Bit 1 ist (d.h. array[0] & 0x80 != 0), stelle ein 0x00-Byte voran, wie in Javas BigInteger.toByteArray()-Darstellung
3. Wenn dieses Byte-Array größer oder gleich 32 Bytes ist, verwende die ersten (höchstwertigen) 32 Bytes
4. Wenn dieses Byte-Array weniger als 32 Bytes hat, hänge 0x00-Bytes an, um auf 32 Bytes zu erweitern. *(verschwindend unwahrscheinlich)*

#### Nachricht 1 (Sitzungsanfrage)

Dies ist die DH-Anfrage. Alice hat bereits Bobs [Router Identity](/docs/specs/common-structures#struct_RouterIdentity), IP-Adresse und Port, die in seiner [Router Info](/docs/specs/common-structures#struct_RouterInfo) enthalten sind, welche in der [network database](/docs/overview/network-database) veröffentlicht wurde. Alice sendet Bob:

```
 X+(H(X) xor Bob.identHash)----------------------------->

    Size: 288 bytes
```
Inhalt:

```
 +----+----+----+----+----+----+----+----+
 |         X, as calculated from DH      |
 +                                       +
 |                                       |
 ~               .   .   .               ~
 |                                       |
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |              HXxorHI                  |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +----+----+----+----+----+----+----+----+

  X :: 256 byte X from Diffie Hellman

  HXxorHI :: SHA256 Hash(X) xored with SHA256 Hash(Bob's RouterIdentity)
             (32 bytes)
```
**Hinweise:**

- Bob überprüft HXxorHI mit seinem eigenen router hash. Wenn die Überprüfung fehlschlägt, hat Alice den falschen router kontaktiert, und Bob bricht die Verbindung ab.

#### Nachricht 2 (Sitzung erstellt)

Das ist die DH-Antwort. Bob sendet Alice:

```
 <----------------------------------------Y+E(H(X+Y)+tsB+padding, sk, Y[239:255])

    Size: 304 bytes
```
Unverschlüsselte Inhalte:

```
 +----+----+----+----+----+----+----+----+
 |         Y as calculated from DH       |
 +                                       +
 |                                       |
 ~               .   .   .               ~
 |                                       |
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |              HXY                      |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +----+----+----+----+----+----+----+----+
 |        tsB        |     padding       |
 +----+----+----+----+                   +
 |                                       |
 +----+----+----+----+----+----+----+----+

  Y :: 256 byte Y from Diffie Hellman

  HXY :: SHA256 Hash(X concatenated with Y)
         (32 bytes)

  tsB :: 4 byte timestamp (seconds since the epoch)

  padding :: 12 bytes random data
```
Verschlüsselte Inhalte:

```
 +----+----+----+----+----+----+----+----+
 |         Y as calculated from DH       |
 +                                       +
 |                                       |
 ~               .   .   .               ~
 |                                       |
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |             encrypted data            |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +----+----+----+----+----+----+----+----+

  Y: 256 byte Y from Diffie Hellman

  encrypted data: 48 bytes AES encrypted using the DH session key and
                  the last 16 bytes of Y as the IV
```
**Hinweise:**

- Alice kann die Verbindung trennen, wenn die Zeitabweichung mit Bob zu hoch ist, wie mit tsB berechnet.

#### Nachricht 3 (Session Confirm A)

Dies enthält Alices router-Identität und eine Signatur der kritischen Daten. Alice sendet Bob:

```
 E(sz+Alice.identity+tsA+padding+S(X+Y+Bob.identHash+tsA+tsB), sk, hX_xor_Bob.identHash[16:31])--->

    Size: 448 bytes (typ. for 387 byte identity and DSA signature), see notes below
```
Unverschlüsselte Inhalte:

```
 +----+----+----+----+----+----+----+----+
 |   sz    | Alice's Router Identity     |
 +----+----+                             +
 |                                       |
 ~               .   .   .               ~
 |                                       |
 +                        +----+----+----+
 |                        |     tsA
 +----+----+----+----+----+----+----+----+
      |             padding              |
 +----+                                  +
 |                                       |
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |              signature                |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +----+----+----+----+----+----+----+----+

  sz :: 2 byte size of Alice's router identity to follow (387+)

  ident :: Alice's 387+ byte RouterIdentity

  tsA :: 4 byte timestamp (seconds since the epoch)

  padding :: 0-15 bytes random data

  signature :: the Signature of the following concatenated data:
               X, Y, Bob's RouterIdentity, tsA, tsB.
               Alice signs it with the SigningPrivateKey associated with
               the SigningPublicKey in her RouterIdentity
```
Verschlüsselte Inhalte:

```
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |             encrypted data            |
 ~               .   .   .               ~
 |                                       |
 +----+----+----+----+----+----+----+----+

  encrypted data: 448 bytes AES encrypted using the DH session key and
                  the last 16 bytes of HXxorHI (i.e., the last 16 bytes
                  of message #1) as the IV
                  448 is the typical length, but it could be longer, see below.
```
**Hinweise:**

- Bob verifiziert die Signatur und verwirft bei einem Fehler die Verbindung.
- Bob kann die Verbindung verwerfen, wenn die Uhrenabweichung mit Alice zu hoch ist, wie mit tsA berechnet.
- Alice wird die letzten 16 Bytes des verschlüsselten Inhalts dieser Nachricht als IV für die nächste Nachricht verwenden.
- Bis zur Version 0.9.15 war die router identity immer 387 Bytes, die Signatur war immer eine 40 Byte DSA-Signatur, und das Padding war immer 15 Bytes. Ab Version 0.9.16 kann die router identity länger als 387 Bytes sein, und der Signaturtyp und die Länge werden durch den Typ des [Signing Public Key](/docs/specs/common-structures#type_SigningPublicKey) in Alices [Router Identity](/docs/specs/common-structures#struct_RouterIdentity) impliziert. Das Padding erfolgt nach Bedarf auf ein Vielfaches von 16 Bytes für den gesamten unverschlüsselten Inhalt.
- Die Gesamtlänge der Nachricht kann nicht bestimmt werden, ohne sie teilweise zu entschlüsseln, um die Router Identity zu lesen. Da die minimale Länge der Router Identity 387 Bytes beträgt und die minimale Signaturlänge 40 (für DSA) ist, beträgt die minimale Gesamtnachrichtengröße 2 + 387 + 4 + (Signaturlänge) + (Padding auf 16 Bytes), oder 2 + 387 + 4 + 40 + 15 = 448 für DSA. Der Empfänger könnte diese minimale Menge lesen, bevor er entschlüsselt, um die tatsächliche Router Identity-Länge zu bestimmen. Bei kleinen Zertifikaten in der Router Identity wird das wahrscheinlich die gesamte Nachricht sein, und es werden keine weiteren Bytes in der Nachricht vorhanden sein, die eine zusätzliche Entschlüsselungsoperation erfordern.

#### Nachricht 4 (Session Confirm B)

Dies ist eine Signatur der kritischen Daten. Bob sendet an Alice:

```
 <----------------------E(S(X+Y+Alice.identHash+tsA+tsB)+padding, sk, prev)

    Size: 48 bytes (typ. for DSA signature), see notes below
```
Unverschlüsselte Inhalte:

```
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |              signature                |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +----+----+----+----+----+----+----+----+
 |               padding                 |
 +----+----+----+----+----+----+----+----+

  signature :: the Signature of the following concatenated data:
               X, Y, Alice's RouterIdentity, tsA, tsB.
               Bob signs it with the SigningPrivateKey associated with
               the SigningPublicKey in his RouterIdentity

  padding :: 0-15 bytes random data
```
Verschlüsselte Inhalte:

```
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |             encrypted data            |
 ~               .   .   .               ~
 |                                       |
 +----+----+----+----+----+----+----+----+

  encrypted data: Data AES encrypted using the DH session key and
                  the last 16 bytes of the encrypted contents of message #2 as the IV
                  48 bytes for a DSA signature, may vary for other signature types
```
**Hinweise:**

- Alice verifiziert die Signatur und bricht bei einem Fehler die Verbindung ab.
- Bob wird die letzten 16 Bytes des verschlüsselten Inhalts dieser Nachricht als IV für die nächste Nachricht verwenden.
- Bis einschließlich Release 0.9.15 war die Signatur immer eine 40 Byte DSA-Signatur und das Padding war immer 8 Bytes. Ab Release 0.9.16 werden der Signaturtyp und die Länge durch den Typ des [Signing Public Key](/docs/specs/common-structures#type_SigningPublicKey) in Bobs [Router Identity](/docs/specs/common-structures#struct_RouterIdentity) impliziert. Das Padding erfolgt nach Bedarf auf ein Vielfaches von 16 Bytes für den gesamten unverschlüsselten Inhalt.

#### Nach der Einrichtung

Die Verbindung ist hergestellt und Standard- oder Zeitsynchronisationsnachrichten können ausgetauscht werden. Alle nachfolgenden Nachrichten werden mit AES verschlüsselt unter Verwendung des ausgehandelten DH-Sitzungsschlüssels. Alice wird die letzten 16 Bytes des verschlüsselten Inhalts von Nachricht #3 als nächsten IV verwenden. Bob wird die letzten 16 Bytes des verschlüsselten Inhalts von Nachricht #4 als nächsten IV verwenden.

### Verbindung prüfen Nachricht

Alternativ könnte es sich, wenn Bob eine Verbindung erhält, um eine Prüfverbindung handeln (möglicherweise ausgelöst dadurch, dass Bob jemanden bittet, seinen Listener zu verifizieren). Check Connection wird derzeit nicht verwendet. Der Vollständigkeit halber sind Prüfverbindungen jedoch wie folgt formatiert. Eine Check-Info-Verbindung wird 256 Bytes erhalten, die Folgendes enthalten:

- 32 Bytes uninterpretierte, ignorierte Daten
- 1 Byte Größe
- so viele Bytes, die die IP-Adresse des lokalen routers ausmachen (wie von der entfernten Seite erreicht)
- 2 Byte Portnummer, über die der lokale router erreicht wurde
- 4 Byte i2p Netzwerkzeit, wie sie von der entfernten Seite bekannt ist (Sekunden seit der Epoche)
- uninterpretierte Füllbytes, bis zu Byte 223
- XOR des lokalen router-Identity-Hash und des SHA256 von Byte 32 bis Byte 223

Die Verbindungsüberprüfung ist ab Version 0.9.12 vollständig deaktiviert.

## Diskussion

Jetzt auf der [NTCP Diskussionsseite](/docs/discussions/ntcp).

## Zukünftige Arbeiten {#future}

- Die maximale Nachrichtengröße sollte auf etwa 32 KB erhöht werden.

- Ein Satz fester Paketgrößen könnte angemessen sein, um die Datenfragmentierung vor externen Angreifern weiter zu verbergen, aber das tunnel-, garlic- und Ende-zu-Ende-Padding sollte für die meisten Bedürfnisse bis dahin ausreichend sein.
  Es gibt jedoch derzeit keine Vorkehrung für Padding über die nächste 16-Byte-Grenze hinaus, um eine begrenzte Anzahl von Nachrichtengrößen zu schaffen.

- Die Speichernutzung (einschließlich der des Kernels) für NTCP sollte mit der für SSU verglichen werden.

- Können die Establishment-Nachrichten auf irgendeine Weise zufällig aufgefüllt werden, um die Identifizierung von I2P-Traffic basierend auf anfänglichen Paketgrößen zu erschweren?
