---
title: "SSU (Secure Semireliable UDP)"
description: "Ursprüngliche UDP-Transportprotokoll-Spezifikation (veraltet, ersetzt durch SSU2)"
slug: "ssu"
aliases:
  - "/de/docs/transport/ssu"
  - "/de/docs/transport/ssu/"
  - "/de/docs/transports/ssu"
  - "/de/docs/transports/ssu/"
  - "/de/docs/specs/ssu-spec"
  - "/de/docs/specs/ssu-spec/"
  - "/de/udp_spec"
  - "/de/udp_spec/"
category: "Transporte"
lastUpdated: "2024-01"
accurateFor: "0.9.61"
---

## Übersicht

VERALTET - SSU wurde durch SSU2 ersetzt. SSU-Unterstützung wurde aus i2pd in Version 2.44.0 (API 0.9.56) 2022-11 entfernt. SSU-Unterstützung wurde aus Java I2P in Version 2.4.0 (API 0.9.61) 2023-12 entfernt.

Siehe die [SSU-Übersicht](/docs/transport/ssu/) für weitere Informationen.

## DH Schlüsselaustausch {#dh}

Der anfängliche 2048-Bit DH-Schlüsselaustausch wird auf der [SSU Keys-Seite](/docs/transport/ssu/#keys) beschrieben. Dieser Austausch verwendet dieselbe geteilte Primzahl wie die für I2Ps [ElGamal-Verschlüsselung](/docs/specs/cryptography/#elgamal).

## Message Header {#header}

Alle UDP-Datagramme beginnen mit einem 16 Byte MAC (Message Authentication Code) und einem 16 Byte IV (Initialization Vector), gefolgt von einer variabel großen Nutzlast, die mit dem entsprechenden Schlüssel verschlüsselt ist. Der verwendete MAC ist HMAC-MD5, auf 16 Bytes gekürzt, während der Schlüssel ein vollständiger 32 Byte AES256-Schlüssel ist. Die spezifische Konstruktion des MAC besteht aus den ersten 16 Bytes von:

```
HMAC-MD5(encryptedPayload + IV + (payloadLength ^ protocolVersion ^ ((netid - 2) << 8)), macKey)
```
wobei '+' anhängen bedeutet und '^' exklusives Oder bedeutet.

Der IV wird für jedes Paket zufällig generiert. Die encryptedPayload ist die verschlüsselte Version der Nachricht, die mit dem Flag-Byte beginnt (encrypt-then-MAC). Die payloadLength, die im MAC verwendet wird, ist eine 2-Byte-Ganzzahl ohne Vorzeichen, Big Endian. Beachten Sie, dass protocolVersion 0 ist, sodass die Exklusiv-Oder-Verknüpfung ein No-Op ist. Der macKey ist entweder der introduction key oder wird aus dem ausgetauschten DH-Schlüssel konstruiert (siehe Details unten), wie für jede Nachricht unten spezifiziert.

**WARNUNG** - das hier verwendete HMAC-MD5-128 ist nicht standardkonform, siehe [HMAC-Details](/docs/specs/cryptography/#udp) für weitere Informationen.

Die Nutzlast selbst (das heißt, die Nachricht, die mit dem Flag-Byte beginnt) ist AES256/CBC-verschlüsselt mit der IV und dem sessionKey, wobei die Replay-Verhinderung in ihrem Körper behandelt wird, wie unten erklärt.

Die protocolVersion ist eine 2-Byte-Ganzzahl ohne Vorzeichen, Big Endian, und ist derzeit auf 0 gesetzt. Peers, die eine andere Protokollversion verwenden, können nicht mit diesem Peer kommunizieren, obwohl frühere Versionen, die dieses Flag nicht verwenden, es können.

Das exklusive ODER von ((netid - 2) << 8) wird verwendet, um netzwerkübergreifende Verbindungen schnell zu identifizieren. Die netid ist eine 2-Byte-Ganzzahl ohne Vorzeichen, Big-Endian, und ist derzeit auf 2 gesetzt. Ab 0.9.42. Siehe Vorschlag 147 für weitere Informationen. Da die aktuelle Netzwerk-ID 2 ist, ist dies ein No-Op für das aktuelle Netzwerk und ist rückwärtskompatibel. Alle Verbindungen von Testnetzwerken sollten eine andere ID haben und werden beim HMAC fehlschlagen.

### HMAC-Spezifikation

- Inner padding: 0x36...
- Outer padding: 0x5C...
- Key: 32 Bytes
- Hash digest function: MD5, 16 Bytes
- Block size: 64 Bytes
- MAC size: 16 Bytes
- Beispiel C-Implementierungen:
  - hmac.h in [i2pd](https://github.com/PurpleI2P/i2pd)
  - I2PHMAC.cpp in [i2pcpp](http://git.repo.i2p/w/i2pcpp.git)
- Beispiel Java-Implementierung:
  - I2PHMac.java in [I2P](https://github.com/i2p/i2p.i2p)

### Session-Schlüssel-Details

Der 32-Byte-Sitzungsschlüssel wird wie folgt erstellt:

1. Nehmen Sie den ausgetauschten DH-Schlüssel, dargestellt als positives Byte-Array mit minimaler Länge in BigInteger-Format (Zweierkomplement Big-Endian)
2. Wenn das höchstwertige Bit 1 ist (d.h. array[0] & 0x80 != 0), stellen Sie ein 0x00-Byte voran, wie in Javas BigInteger.toByteArray()-Darstellung
3. Wenn das Byte-Array größer oder gleich 32 Bytes ist, verwenden Sie die ersten (höchstwertigen) 32 Bytes
4. Wenn das Byte-Array kleiner als 32 Bytes ist, hängen Sie 0x00-Bytes an, um auf 32 Bytes zu erweitern. *Sehr unwahrscheinlich - Siehe Hinweis unten.*

### MAC-Schlüssel-Details

Der 32-Byte MAC-Schlüssel wird wie folgt erstellt:

1. Nehmen Sie das ausgetauschte DH-Schlüssel-Byte-Array, falls nötig mit einem vorangestellten 0x00-Byte, aus Schritt 2 in den Session Key Details oben.
2. Wenn dieses Byte-Array größer oder gleich 64 Bytes ist, ist der MAC-Schlüssel die Bytes 33-64 aus diesem Byte-Array.
3. Wenn dieses Byte-Array kleiner als 64 Bytes ist, ist der MAC-Schlüssel der SHA-256-Hash dieses Byte-Arrays. *Ab Release 0.9.8. Siehe Hinweis unten.*

#### Wichtiger Hinweis

Der Code vor Release 0.9.8 war fehlerhaft und behandelte DH-Schlüssel-Byte-Arrays zwischen 32 und 63 Bytes (Schritte 3 und 4 oben) nicht korrekt, wodurch die Verbindung fehlschlug. Da diese Fälle nie funktionierten, wurden sie wie oben beschrieben für Release 0.9.8 neu definiert, und der 0-32-Byte-Fall wurde ebenfalls neu definiert. Da der nominell ausgetauschte DH-Schlüssel 256 Bytes beträgt, ist die Wahrscheinlichkeit, dass die minimale Darstellung weniger als 64 Bytes beträgt, verschwindend gering.

### Header-Format

Innerhalb der AES-verschlüsselten Payload gibt es eine minimale gemeinsame Struktur für die verschiedenen Nachrichten - ein Ein-Byte-Flag und einen Vier-Byte-Sendetimestamp (Sekunden seit der Unix-Epoche).

Das Header-Format ist:

```
Header: 37+ bytes
  Encryption starts with the flag byte.
  +----+----+----+----+----+----+----+----+
  |                  MAC                  |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                   IV                  |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |flag|        time       |              |
  +----+----+----+----+----+              +
  | keying material (optional)            |
  +                                       +
  |                                       |
  ~                                       ~
  |                                       |
  +                        +----+----+----+
  |                        |#opt|         |
  +----+----+----+----+----+----+         +
  | #opt extended option bytes (optional) |
  ~                                       ~
  ~                                       ~
  +----+----+----+----+----+----+----+----+
```
Das Flag-Byte enthält die folgenden Bitfelder:

```
Bit order: 76543210 (bit 7 is MSB)

  bits 7-4: payload type
     bit 3: If 1, rekey data is included. Always 0, unimplemented
     bit 2: If 1, extended options are included. Always 0 before release
            0.9.24.
  bits 1-0: reserved, set to 0 for compatibility with future uses
```
Ohne Rekeying und erweiterte Optionen beträgt die Header-Größe 37 Bytes.

### Schlüsselerneuerung {#rekey}

Wenn das Rekey-Flag gesetzt ist, folgen 64 Bytes Schlüsselmaterial nach dem Zeitstempel.

Beim Rekeying werden die ersten 32 Bytes des Schlüsselmaterials in einen SHA256 eingespeist, um den neuen MAC-Schlüssel zu erzeugen, und die nächsten 32 Bytes werden in einen SHA256 eingespeist, um den neuen Session-Schlüssel zu erzeugen, obwohl die Schlüssel nicht sofort verwendet werden. Die andere Seite sollte ebenfalls mit gesetztem Rekey-Flag und demselben Schlüsselmaterial antworten. Sobald beide Seiten diese Werte gesendet und empfangen haben, sollten die neuen Schlüssel verwendet und die vorherigen Schlüssel verworfen werden. Es kann nützlich sein, die alten Schlüssel kurzzeitig aufzubewahren, um Paketverlust und Neuordnung zu bewältigen.

HINWEIS: Rekeying ist derzeit nicht implementiert.

### Erweiterte Optionen {#extend}

Wenn das Extended Options Flag gesetzt ist, wird ein Ein-Byte-Wert für die Optionsgröße angehängt, gefolgt von entsprechend vielen Extended Option Bytes. Extended Options waren schon immer Teil der Spezifikation, wurden aber erst ab Release 0.9.24 implementiert. Falls vorhanden, ist das Optionsformat spezifisch für den Nachrichtentyp. Siehe die Nachrichtendokumentation unten, ob Extended Options für die jeweilige Nachricht erwartet werden und welches Format spezifiziert ist. Während Java-Router das Flag und die Optionslänge schon immer erkannt haben, haben andere Implementierungen das nicht getan. Daher sollten Extended Options nicht an Router gesendet werden, die älter als Release 0.9.24 sind.

## Padding

Alle Nachrichten enthalten 0 oder mehr Bytes an Padding. Jede Nachricht muss auf eine 16-Byte-Grenze aufgefüllt werden, wie es von der [AES256-Verschlüsselungsschicht](/docs/specs/cryptography/#AES) gefordert wird.

Bis Release 0.9.7 wurden Nachrichten nur auf die nächste 16-Byte-Grenze aufgefüllt, und Nachrichten, die kein Vielfaches von 16 Bytes waren, konnten möglicherweise ungültig sein.

Ab Release 0.9.7 können Nachrichten auf jede beliebige Länge aufgefüllt werden, solange die aktuelle MTU eingehalten wird. Alle zusätzlichen 1-15 Padding-Bytes über den letzten 16-Byte-Block hinaus können weder verschlüsselt noch entschlüsselt werden und werden ignoriert. Die vollständige Länge und alle Padding-Bytes werden jedoch in die MAC-Berechnung einbezogen.

Ab Version 0.9.8 sind übertragene Nachrichten nicht zwangsläufig ein Vielfaches von 16 Bytes. Die SessionConfirmed-Nachricht ist eine Ausnahme, siehe unten.

## Schlüssel

Signaturen in den SessionCreated- und SessionConfirmed-Nachrichten werden unter Verwendung des [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) aus der [RouterIdentity](/docs/specs/common-structures/#routeridentity) generiert, welche außerhalb des Bands durch Veröffentlichung in der Netzwerkdatenbank verteilt wird, sowie dem zugehörigen [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey).

Bis einschließlich Release 0.9.15 war der Signaturalgorithmus immer DSA mit einer 40-Byte-Signatur.

Ab Release 0.9.16 kann der Signaturalgorithmus durch ein [KeyCertificate](/docs/specs/common-structures/#key-certificates) in Bobs [RouterIdentity](/docs/specs/common-structures/#routeridentity) spezifiziert werden.

Sowohl Einführungsschlüssel als auch Sitzungsschlüssel sind 32 Bytes lang und werden durch die Common structures-Spezifikation [SessionKey](/docs/specs/common-structures/#sessionkey) definiert. Der für MAC und Verschlüsselung verwendete Schlüssel wird für jede Nachricht unten spezifiziert.

Introduction Keys werden über einen externen Kanal (die Netzwerkdatenbank) übermittelt, wo sie traditionell bis Release 0.9.47 identisch mit dem router Hash waren, aber ab Release 0.9.48 zufällig sein können.

## Notizen

### IPv6

Die Protokollspezifikation erlaubt sowohl 4-Byte-IPv4- als auch 16-Byte-IPv6-Adressen. SSU-über-IPv6 wird ab Version 0.9.8 unterstützt. Siehe die Dokumentation der einzelnen Nachrichten unten für Details zur IPv6-Unterstützung.

### Zeitstempel {#time}

Während die meisten Teile von I2P 8-Byte [Date](/docs/specs/common-structures/#date) Zeitstempel mit Millisekundenauflösung verwenden, nutzt SSU 4-Byte unsigned Integer Zeitstempel mit einer Sekundenauflösung. Da diese Werte unsigned sind, werden sie erst im Februar 2106 überlaufen.

## Nachrichten

Es sind 10 Nachrichten (Payload-Typen) definiert:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Message</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Notes</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#sessionrequest">SessionRequest</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#sessioncreated">SessionCreated</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#sessionconfirmed">SessionConfirmed</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#relayrequest">RelayRequest</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#relayresponse">RelayResponse</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#relayintro">RelayIntro</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#data">Data</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#peertest">PeerTest</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#sessiondestroyed">SessionDestroyed</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Implemented as of 0.8.9</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">n/a</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#holepunch">HolePunch</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
</table>
### SessionRequest (Typ 0) {#sessionrequest}

Dies ist die erste Nachricht, die gesendet wird, um eine Sitzung zu etablieren.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice to Bob</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">256 byte X, to begin the DH agreement; 1 byte IP address size; that many bytes representation of Bob's IP address; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, as retrieved from the network database</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, as retrieved from the network database</td>
</tr>
</table>
Nachrichtenformat:

```
+----+----+----+----+----+----+----+----+
|         X, as calculated from DH      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|size| that many byte IP address (4-16) |
+----+----+----+----+----+----+----+----+
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
Typische Größe einschließlich Header in der aktuellen Implementierung: 304 (IPv4) oder 320 (IPv6) Bytes (vor non-mod-16 Padding)

#### Erweiterte Optionen

Hinweis: Implementiert in 0.9.24.

- Mindestlänge: 3 (Optionslängen-Byte + 2 Bytes)
- Optionslänge: mindestens 2
- 2 Bytes Flags:

```
Bit order: 15...76543210 (bit 15 is MSB)

      bit 0: 1 for Alice to request a relay tag from Bob in the
             SessionCreated response, 0 if Alice does not need a relay tag.
             Note that "1" is the default if no extended options are present
  bits 15-1: unused, set to 0 for compatibility with future uses
```
#### Notizen

- IPv4- und IPv6-Adressen werden unterstützt.
- Die nicht interpretierten Daten könnten möglicherweise in der Zukunft für Herausforderungen verwendet werden.

### SessionCreated (Typ 1) {#sessioncreated}

Dies ist die Antwort auf eine [SessionRequest](#sessionrequest).

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob to Alice</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">256 byte Y, to complete the DH agreement; 1 byte IP address size; that many bytes representation of Alice's IP address; 2 byte Alice's port number; 4 byte relay (introduction) tag which Alice can publish (else 0x00000000); 4 byte timestamp (seconds from the epoch) for use in the DSA signature; Bob's <a href="/docs/specs/common-structures/#signature">Signature</a> of the critical exchanged data (X + Y + Alice's IP + Alice's port + Bob's IP + Bob's port + Alice's new relay tag + Bob's signed on time), encrypted with another layer of encryption using the negotiated sessionKey. The IV is reused here. See notes for length information.; 0-15 bytes of padding of the signature, using random data, to a multiple of 16 bytes, so that the signature + padding may be encrypted with an additional layer of encryption using the negotiated session key as part of the DSA block.; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, with an additional layer of encryption over the 40 byte signature and the following 8 bytes padding.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey</td>
</tr>
</table>
Nachrichtenformat:

```
+----+----+----+----+----+----+----+----+
|         Y, as calculated from DH      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|size| that many byte IP address (4-16) |
+----+----+----+----+----+----+----+----+
| Port (A)| public relay tag  |  signed
+----+----+----+----+----+----+----+----+
  on time |                             |
+----+----+                             +
|                                       |
+                                       +
|             signature                 |
+                                       +
|                                       |
+                                       +
|                                       |
+         +----+----+----+----+----+----+
|         |   (0-15 bytes of padding) 
+----+----+----+----+----+----+----+----+
          |                             |
+----+----+                             +
|           arbitrary amount            |
~        of uninterpreted data          ~
~                .  .  .                ~
```
Typische Größe inklusive Header, in der aktuellen Implementierung: 368 Bytes (IPv4 oder IPv6) (vor nicht-mod-16-Padding)

#### Hinweise

- IPv4- und IPv6-Adressen werden unterstützt.
- Wenn das relay tag nicht null ist, bietet Bob an, als Introducer für
  Alice zu fungieren. Alice kann anschließend Bobs Adresse und das relay tag in der
  netDb veröffentlichen.
- Für die Signatur muss Bob seinen externen Port verwenden, da Alice diesen zur
  Verifikation nutzen wird. Wenn Bobs NAT/Firewall seinen internen Port auf einen
  anderen externen Port gemappt hat und Bob sich dessen nicht bewusst ist, wird die Verifikation durch Alice
  fehlschlagen.
- Siehe den Abschnitt [Keys](#keys) oben für Details zu Signaturen. Alice hat bereits
  Bobs öffentlichen Signaturschlüssel aus der netDb.
- Bis Release 0.9.15 war die Signatur immer eine 40 Byte DSA-Signatur und
  das Padding war immer 8 Bytes. Ab Release 0.9.16 werden Signaturtyp und
  -länge durch den Typ des [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) in Bobs
  [RouterIdentity](/docs/specs/common-structures/#routeridentity) impliziert. Das Padding erfolgt nach Bedarf auf ein Vielfaches von 16 Bytes.
- Dies ist die einzige Nachricht, die den intro key des Senders verwendet. Alle anderen nutzen den
  intro key des Empfängers oder den etablierten session key.
- Die signed-on time scheint in der aktuellen
  Implementierung ungenutzt oder unverifiziert zu sein.
- Die uninterpretierten Daten könnten möglicherweise in Zukunft für Challenges verwendet werden.
- Extended options im Header: Nicht erwartet, undefiniert.

### SessionConfirmed (Typ 2) {#sessionconfirmed}

Dies ist die Antwort auf eine [SessionCreated](#sessioncreated)-Nachricht und der letzte Schritt beim Aufbau einer Sitzung. Es können mehrere SessionConfirmed-Nachrichten erforderlich sein, wenn die Router Identity fragmentiert werden muss.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice to Bob</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 byte identity fragment info (bits 7-4: current identity fragment # 0-14; bits 3-0: total identity fragments (F) 1-15); 2 byte size of the current identity fragment; that many byte fragment of Alice's <a href="/docs/specs/common-structures/#routeridentity">RouterIdentity</a>; After the last identity fragment only: 4 byte signed-on time; N bytes padding, currently uninterpreted; After the last identity fragment only: The remaining bytes contain Alice's <a href="/docs/specs/common-structures/#signature">Signature</a> of the critical exchanged data (X + Y + Alice's IP + Alice's port + Bob's IP + Bob's port + Alice's new relay tag + Alice's signed on time). See notes for length information.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob sessionKey, as generated from the DH exchange</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob MAC Key, as generated from the DH exchange</td>
</tr>
</table>
**Fragment 0 bis F-2** (nur wenn F > 1; derzeit ungenutzt, siehe Hinweise unten):

```
+----+----+----+----+----+----+----+----+
|info| cursize |                        |
+----+----+----+                        +
|      fragment of Alice's full         |
~            Router Identity            ~
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
**Fragment F-1 (letztes oder einziges Fragment):**

```
+----+----+----+----+----+----+----+----+
|info| cursize |                        |
+----+----+----+                        +
|     last fragment of Alice's full     |
~            Router Identity            ~
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|  signed on time   |                   |
+----+----+----+----+                   +
|  arbitrary amount of uninterpreted    |
~      data, until the signature at     ~
~       end of the current packet       ~
|  Packet length must be mult. of 16    |
+----+----+----+----+----+----+----+----+
+                                       +
|                                       |
+                                       +
|             signature                 |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
Typische Größe einschließlich Header in der aktuellen Implementierung: 512 Bytes (mit Ed25519-Signatur) oder 480 Bytes (mit DSA-SHA1-Signatur) (vor non-mod-16-Padding)

#### Hinweise

- In der aktuellen Implementierung beträgt die maximale Fragmentgröße 512 Bytes. Dies
  sollte erweitert werden, damit längere Signaturen ohne Fragmentierung funktionieren.
  Die aktuelle Implementierung verarbeitet Signaturen, die über
  zwei Fragmente aufgeteilt sind, nicht korrekt.
- Die typische [RouterIdentity](/docs/specs/common-structures/#routeridentity) umfasst 387 Bytes, sodass niemals eine Fragmentierung
  notwendig ist. Falls neue Kryptographie die Größe der RouterIdentity erweitert, muss
  das Fragmentierungsschema sorgfältig getestet werden.
- Es gibt keinen Mechanismus zum Anfordern oder erneuten Zustellen fehlender Fragmente.
- Das Gesamtfragmente-Feld F muss in allen Fragmenten identisch gesetzt werden.
- Siehe den Abschnitt [Keys](#keys) oben für Details zu DSA-Signaturen.
- Die Signierungszeit scheint in der aktuellen
  Implementierung ungenutzt oder unverifiziert zu sein.
- Da sich die Signatur am Ende befindet, muss das Padding im letzten oder einzigen Paket
  das Gesamtpaket auf ein Vielfaches von 16 Bytes auffüllen, oder die Signatur wird
  nicht korrekt entschlüsselt. Dies unterscheidet sich von allen anderen Nachrichtentypen,
  wo sich das Padding am Ende befindet.
- Bis Release 0.9.15 war die Signatur immer eine 40 Byte DSA-Signatur. Ab
  Release 0.9.16 werden Signaturtyp und -länge durch den Typ des
  [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) in Alices [RouterIdentity](/docs/specs/common-structures/#routeridentity) impliziert. Das Padding erfolgt wie
  erforderlich auf ein Vielfaches von 16 Bytes.
- Erweiterte Optionen im Header: Nicht erwartet, undefiniert.

### SessionDestroyed (Typ 8) {#sessiondestroyed}

Die SessionDestroyed-Nachricht wurde (nur Empfang) in Version 0.8.1 implementiert und wird seit Version 0.8.9 gesendet.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice to Bob or Bob to Alice</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">none</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob sessionKey</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob MAC Key</td>
</tr>
</table>
Diese Nachricht enthält keine Daten. Typische Größe einschließlich Header in der aktuellen Implementierung: 48 Bytes (vor non-mod-16 padding)

#### Notizen

- Destroy-Nachrichten, die mit dem Intro-Schlüssel des Senders oder Empfängers empfangen werden, werden ignoriert.
- Erweiterte Optionen im Header: Nicht erwartet, undefiniert.

### RelayRequest (Typ 3) {#relayrequest}

Dies ist die erste Nachricht, die von Alice an Bob gesendet wird, um eine Einführung zu Charlie zu erbitten.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice to Bob</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4 byte relay (introduction) tag, nonzero, as received by Alice in the SessionCreated message from Bob; 1 byte IP address size; that many byte representation of Alice's IP address; 2 byte port number (of Alice); 1 byte challenge size; that many bytes to be relayed to Charlie in the intro; Alice's 32-byte introduction key (so Bob can reply with Charlie's info); 4 byte nonce of Alice's relay request; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, as retrieved from the network database (or Alice/Bob sessionKey, if established)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, as retrieved from the network database (or Alice/Bob MAC Key, if established)</td>
</tr>
</table>
Nachrichtenformat:

```
+----+----+----+----+----+----+----+----+
|      relay tag    |size| Alice IP addr
+----+----+----+----+----+----+----+----+
     | Port (A)|size| challenge bytes   |
+----+----+----+----+                   +
|      to be delivered to Charlie       |
+----+----+----+----+----+----+----+----+
| Alice's intro key                     |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|       nonce       |                   |
+----+----+----+----+                   +
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
Typische Größe einschließlich Header in der aktuellen Implementierung: 96 Bytes (ohne Alice-IP) oder 112 Bytes (mit 4-Byte-Alice-IP) (vor non-mod-16-Padding)

#### Notizen

- Die IP-Adresse wird nur eingefügt, wenn sie sich von der Quelladresse und dem Port des Pakets unterscheidet.
- Diese Nachricht kann über IPv4 oder IPv6 gesendet werden.
  Wenn die Nachricht über IPv6 für eine IPv4-Einführung gesendet wird,
  oder (ab Version 0.9.50) über IPv4 für eine IPv6-Einführung,
  muss Alice ihre Einführungsadresse und ihren Port angeben.
  Dies wird ab Version 0.9.50 unterstützt.
- Wenn Alice ihre Adresse/ihren Port angibt, kann Bob zusätzliche Validierung
  durchführen, bevor er fortfährt.
  - Vor Version 0.9.24 lehnte Java I2P jede Adresse oder jeden Port ab, die/der
    sich von der Verbindung unterschied.
- Challenge ist nicht implementiert, die Challenge-Größe ist immer null
- Weiterleitung für IPv6 wird ab Version 0.9.50 unterstützt.
- Vor Version 0.9.12 wurde immer Bobs Intro-Schlüssel verwendet. Ab Version
  0.9.12 wird der Sitzungsschlüssel verwendet, wenn eine etablierte Sitzung zwischen
  Alice und Bob besteht. In der Praxis muss eine etablierte Sitzung vorhanden sein, da Alice
  die Nonce (Introduction Tag) nur aus der Sitzungserstellungsnachricht erhält,
  und Bob das Introduction Tag als ungültig markiert, sobald die Sitzung zerstört wird.
- Erweiterte Optionen im Header: Nicht erwartet, undefiniert.

### RelayResponse (Typ 4) {#relayresponse}

Dies ist die Antwort auf eine [RelayRequest](#relayrequest) und wird von Bob an Alice gesendet.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob to Alice</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 byte IP address size; that many byte representation of Charlie's IP address; 2 byte Charlie's port number; 1 byte IP address size; that many byte representation of Alice's IP address; 2 byte Alice's port number; 4 byte nonce sent by Alice; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice's introKey, as received in the Relay Request (or Alice/Bob sessionKey, if established)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice's introKey, as received in the Relay Request (or Alice/Bob MAC Key, if established)</td>
</tr>
</table>
Nachrichtenformat:

```
+----+----+----+----+----+----+----+----+
|size|    Charlie IP     | Port (C)|size|
+----+----+----+----+----+----+----+----+
|    Alice IP       | Port (A)|  nonce
+----+----+----+----+----+----+----+----+
          |   arbitrary amount of       |
+----+----+                             +
|          uninterpreted data           |
~                .  .  .                ~
```
Typische Größe einschließlich Header in der aktuellen Implementierung: 64 (Alice IPv4) oder 80 (Alice IPv6) Bytes (vor non-mod-16 Padding)

#### Notizen

- Diese Nachricht kann über IPv4 oder IPv6 gesendet werden.
- Alices IP-Adresse/Port sind die scheinbare IP/Port, die Bob beim
  RelayRequest erhalten hat (nicht unbedingt die IP, die Alice im RelayRequest enthalten hat),
  und können IPv4 oder IPv6 sein. Alice ignoriert diese beim Empfang derzeit.
- Charlies IP-Adresse kann IPv4 oder, ab Release 0.9.50, IPv6 sein,
  da dies die Adresse ist, an die Alice
  die SessionRequest nach dem Hole Punch senden wird.
- Relaying für IPv6 wird ab Release 0.9.50 unterstützt.
- Vor Release 0.9.12 wurde immer Alices Intro-Schlüssel verwendet. Ab Release
  0.9.12 wird der Session-Schlüssel verwendet, wenn eine etablierte Session zwischen
  Alice und Bob besteht.
- Erweiterte Optionen im Header: Nicht erwartet, undefiniert.

### RelayIntro (Typ 5) {#relayintro}

Dies ist die Einführung für Alice, die von Bob an Charlie gesendet wird.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob to Charlie</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 byte IP address size; that many byte representation of Alice's IP address; 2 byte port number (of Alice); 1 byte challenge size; that many bytes relayed from Alice; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob/Charlie sessionKey</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob/Charlie MAC Key</td>
</tr>
</table>
Nachrichtenformat:

```
+----+----+----+----+----+----+----+----+
|size|     Alice IP      | Port (A)|size|
+----+----+----+----+----+----+----+----+
|      that many bytes of challenge     |
+                                       +
|        data relayed from Alice        |
+----+----+----+----+----+----+----+----+
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
Typische Größe einschließlich Header in der aktuellen Implementierung: 48 Bytes (vor non-mod-16 Padding)

#### Notizen

- Bei IPv4 ist Alices IP-Adresse immer 4 Bytes lang, da Alice versucht, sich über IPv4 mit Charlie zu verbinden.
  Ab Release 0.9.50 wird IPv6 unterstützt, und Alices IP-Adresse kann 16 Bytes lang sein.
- Bei IPv4 muss diese Nachricht über eine bestehende IPv4-Verbindung gesendet werden,
  da dies die einzige Möglichkeit für Bob ist, Charlies IPv4-Adresse zu kennen, um sie in der RelayResponse an Alice zurückzugeben.
  Ab Release 0.9.50 wird IPv6 unterstützt, und diese Nachricht kann über eine bestehende IPv6-Verbindung gesendet werden.
- Ab Release 0.9.50 muss jede SSU-Adresse, die mit introducers veröffentlicht wird, "4" oder "6" in der "caps"-Option enthalten.
- Challenge ist nicht implementiert, die Challenge-Größe ist immer null
- Erweiterte Optionen im Header: Nicht erwartet, undefiniert.

### Daten (Typ 6) {#data}

Diese Nachricht wird für Datentransport und Bestätigung verwendet.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Any</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob sessionKey</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob MAC Key</td>
</tr>
</table>
**Daten:** 1 Byte Flags (siehe unten); wenn explizite ACKs enthalten sind: 1 Byte Anzahl der ACKs, entsprechend viele 4 Byte MessageIds die vollständig bestätigt werden; wenn ACK-Bitfelder enthalten sind: 1 Byte Anzahl der ACK-Bitfelder, entsprechend viele 4 Byte MessageIds + ein 1 oder mehr Byte ACK-Bitfeld (siehe Hinweise); Wenn erweiterte Daten enthalten sind: 1 Byte Datengröße, entsprechend viele Bytes erweiterte Daten (derzeit nicht interpretiert); 1 Byte Anzahl der Fragmente (kann null sein); Falls nicht null, entsprechend viele Nachrichtenfragmente.

```
Flags byte:
  Bit order: 76543210 (bit 7 is MSB)
  bit 7: explicit ACKs included
  bit 6: ACK bitfields included
  bit 5: reserved
  bit 4: explicit congestion notification (ECN)
  bit 3: request previous ACKs
  bit 2: want reply
  bit 1: extended data included (unused, never set)
  bit 0: reserved
```
Jedes Fragment enthält: - 4 Byte messageId - 3 Byte Fragment-Info:   - Bits 23-17: Fragment # 0 - 127   - Bit 16: isLast (1 = true)   - Bits 15-14: unbenutzt, auf 0 gesetzt für Kompatibilität mit zukünftigen Verwendungen   - Bits 13-0: Fragmentgröße 0 - 16383 - so viele Bytes Fragmentdaten

Nachrichtenformat:

```
+----+----+----+----+----+----+----+----+
|flag| (additional headers, determined  |
+----+                                  +
~ by the flags, such as ACKs or         ~
| bitfields                             |
+----+----+----+----+----+----+----+----+
|#frg|     messageId     |   frag info  |
+----+----+----+----+----+----+----+----+
| that many bytes of fragment data      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|     messageId     |   frag info  |    |
+----+----+----+----+----+----+----+    +
| that many bytes of fragment data      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|     messageId     |   frag info  |    |
+----+----+----+----+----+----+----+    +
| that many bytes of fragment data      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
#### ACK Bitfeld Hinweise

Das Bitfeld verwendet die 7 niedrigen Bits jedes Bytes, wobei das höchste Bit angibt, ob ein weiteres Bitfeld-Byte folgt (1 = wahr, 0 = das aktuelle Bitfeld-Byte ist das letzte). Diese Sequenz von 7-Bit-Arrays repräsentiert, ob ein Fragment empfangen wurde - wenn ein Bit 1 ist, wurde das Fragment empfangen. Zur Verdeutlichung, angenommen die Fragmente 0, 2, 5 und 9 wurden empfangen, wären die Bitfeld-Bytes wie folgt:

```
byte 0:
   Bit order: 76543210 (bit 7 is MSB)
   bit 7: 1 (further bitfield bytes follow)
   bit 6: 0 (fragment 6 not received)
   bit 5: 1 (fragment 5 received)
   bit 4: 0 (fragment 4 not received)
   bit 3: 0 (fragment 3 not received)
   bit 2: 1 (fragment 2 received)
   bit 1: 0 (fragment 1 not received)
   bit 0: 1 (fragment 0 received)
byte 1:
   Bit order: 76543210 (bit 7 is MSB)
   bit 7: 0 (no further bitfield bytes)
   bit 6: 0 (fragment 13 not received)
   bit 5: 0 (fragment 12 not received)
   bit 4: 0 (fragment 11 not received)
   bit 3: 0 (fragment 10 not received)
   bit 2: 1 (fragment 9 received)
   bit 1: 0 (fragment 8 not received)
   bit 0: 0 (fragment 7 not received)
```
#### Hinweise

- Die aktuelle Implementierung fügt eine begrenzte Anzahl doppelter Bestätigungen für zuvor bestätigte Nachrichten hinzu, wenn Platz verfügbar ist.
- Wenn die Anzahl der Fragmente null ist, handelt es sich um eine reine Bestätigungs- oder Keepalive-Nachricht.
- Die ECN-Funktion ist nicht implementiert und das Bit wird nie gesetzt.
- In der aktuellen Implementierung wird das Want-Reply-Bit gesetzt, wenn die Anzahl der Fragmente größer als null ist, und nicht gesetzt, wenn keine Fragmente vorhanden sind.
- Extended Data ist nicht implementiert und niemals vorhanden.
- Der Empfang mehrerer Fragmente wird in allen Versionen unterstützt. Die Übertragung mehrerer Fragmente ist in Version 0.9.16 implementiert.
- Wie derzeit implementiert, beträgt die maximale Fragmentanzahl 64 (maximale Fragmentnummer = 63).
- Wie derzeit implementiert, ist die maximale Fragmentgröße selbstverständlich kleiner als die MTU.
- Achten Sie darauf, die maximale MTU nicht zu überschreiten, auch wenn eine große Anzahl von ACKs zu senden ist.
- Das Protokoll erlaubt Fragmente mit null Länge, aber es gibt keinen Grund, sie zu senden.
- In SSU verwenden die Daten einen kurzen 5-Byte I2NP-Header gefolgt von der Nutzlast der I2NP-Nachricht anstelle des standardmäßigen 16-Byte I2NP-Headers. Der kurze I2NP-Header besteht nur aus dem Ein-Byte I2NP-Typ und der 4-Byte-Ablaufzeit in Sekunden. Die I2NP-Nachrichten-ID wird als Nachrichten-ID für das Fragment verwendet. Die I2NP-Größe wird aus den Fragmentgrößen zusammengestellt. Die I2NP-Prüfsumme ist nicht erforderlich, da die UDP-Nachrichtenintegrität durch Entschlüsselung gewährleistet wird.
- Nachrichten-IDs sind keine Sequenznummern und sind nicht aufeinanderfolgend. SSU garantiert keine Zustellung in der richtigen Reihenfolge. Obwohl wir die I2NP-Nachrichten-ID als SSU-Nachrichten-ID verwenden, sind sie aus Sicht des SSU-Protokolls Zufallszahlen. Da der router einen einzigen Bloom-Filter für alle Peers verwendet, muss die Nachrichten-ID eine echte Zufallszahl sein.
- Da es keine Sequenznummern gibt, kann man nicht sicher sein, dass ein ACK empfangen wurde. Die aktuelle Implementierung sendet routinemäßig eine große Menge doppelter ACKs. Doppelte ACKs sollten nicht als Anzeichen für Überlastung interpretiert werden.
- ACK-Bitfeld-Hinweise: Der Empfänger eines Datenpakets weiß nicht, wie viele Fragmente in der Nachricht enthalten sind, es sei denn, er hat das letzte Fragment erhalten. Daher kann die Anzahl der als Antwort gesendeten Bitfeld-Bytes kleiner oder größer sein als die Anzahl der Fragmente geteilt durch 7. Wenn beispielsweise das höchste Fragment, das der Empfänger gesehen hat, die Nummer 4 ist, muss nur ein Byte gesendet werden, auch wenn es insgesamt 13 Fragmente geben könnte. Bis zu 10 Bytes (d.h. (64 / 7) + 1) können für jede bestätigte Nachrichten-ID eingefügt werden.
- Extended Options im Header: Nicht erwartet, undefiniert.

### PeerTest (Typ 7) {#peertest}

Siehe [SSU Peer Testing](/docs/transport/ssu/#peerTesting) für Details. Hinweis: IPv6 peer testing wird ab Version 0.9.27 unterstützt.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Any</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4 byte nonce; 1 byte IP address size (may be zero); that many byte representation of Alice's IP address, if size > 0; 2 byte Alice's port number; Alice's or Charlie's 32-byte introduction key; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">See notes below</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">See notes below</td>
</tr>
</table>
Verwendeter Crypto Key (aufgelistet in der Reihenfolge des Auftretens): 1. Bei Übertragung von Alice zu Bob: Alice/Bob sessionKey 2. Bei Übertragung von Bob zu Charlie: Bob/Charlie sessionKey 3. Bei Übertragung von Charlie zu Bob: Bob/Charlie sessionKey 4. Bei Übertragung von Bob zu Alice: Alice/Bob sessionKey (oder für Bob vor 0.9.52, Alice's introKey) 5. Bei Übertragung von Charlie zu Alice: Alice's introKey, wie in der PeerTest-Nachricht von Bob erhalten 6. Bei Übertragung von Alice zu Charlie: Charlie's introKey, wie in der PeerTest-Nachricht von Charlie erhalten

Verwendeter MAC Key (in der Reihenfolge des Auftretens aufgelistet): 1. Wenn von Alice an Bob gesendet: Alice/Bob MAC Key 2. Wenn von Bob an Charlie gesendet: Bob/Charlie MAC Key 3. Wenn von Charlie an Bob gesendet: Bob/Charlie MAC Key 4. Wenn von Bob an Alice gesendet: Alices introKey, wie in der PeerTest-Nachricht von Alice empfangen 5. Wenn von Charlie an Alice gesendet: Alices introKey, wie in der PeerTest-Nachricht von Bob empfangen 6. Wenn von Alice an Charlie gesendet: Charlies introKey, wie in der PeerTest-Nachricht von Charlie empfangen

Nachrichtenformat:

```
+----+----+----+----+----+----+----+----+
|    test nonce     |size| Alice IP addr
+----+----+----+----+----+----+----+----+
     | Port (A)|                        |
+----+----+----+                        +
| Alice or Charlie's                    |
+ introduction key (Alice's is sent to  +
| Bob and Charlie, while Charlie's is   |
+ sent to Alice)                        +
|                                       |
+              +----+----+----+----+----+
|              | arbitrary amount of    |
+----+----+----+                        |
| uninterpreted data                    |
~                .  .  .                ~
```
Typische Größe einschließlich Header in der aktuellen Implementierung: 80 Bytes (vor non-mod-16 Padding)

#### Notizen

- Wenn von Alice gesendet, ist die IP-Adressgröße 0, die IP-Adresse ist nicht vorhanden und der Port ist 0, da Bob und Charlie die Daten nicht verwenden; das Ziel ist es, Alices wahre IP-Adresse/Port zu bestimmen und Alice mitzuteilen; Bob und Charlie kümmert es nicht, was Alice denkt, dass ihre Adresse ist.
- Wenn von Bob oder Charlie gesendet, sind IP und Port vorhanden, und die IP-Adresse ist 4 oder 16 Bytes. IPv6-Tests werden ab Version 0.9.27 unterstützt.
- Wenn von Charlie an Alice gesendet, sind IP und Port wie folgt:
  Erstes Mal (Nachricht 5): Alices angeforderte IP und Port, wie in Nachricht 2 empfangen.
  Zweites Mal (Nachricht 7): Alices tatsächliche IP und Port, von der Nachricht 6 empfangen wurde.
- IPv6-Hinweise: Bis einschließlich Version 0.9.26 wird nur das Testen von IPv4-Adressen unterstützt. Daher muss die gesamte Alice-Bob- und Alice-Charlie-Kommunikation über IPv4 erfolgen. Bob-Charlie-Kommunikation kann jedoch über IPv4 oder IPv6 erfolgen. Alices Adresse, wenn in der PeerTest-Nachricht angegeben, muss 4 Bytes betragen.
  Ab Version 0.9.27 wird das Testen von IPv6-Adressen unterstützt, und Alice-Bob- sowie Alice-Charlie-Kommunikation kann über IPv6 erfolgen, wenn Bob und Charlie Unterstützung mit einer 'B'-Fähigkeit in ihrer veröffentlichten IPv6-Adresse anzeigen.
  Siehe Proposal 126 für Details.
- Alice sendet die Anfrage an Bob über eine bestehende Session über den Transport (IPv4 oder IPv6), den sie testen möchte.
  Wenn Bob eine Anfrage von Alice über IPv4 erhält, muss Bob einen Charlie auswählen, der eine IPv4-Adresse bewirbt.
  Wenn Bob eine Anfrage von Alice über IPv6 erhält, muss Bob einen Charlie auswählen, der eine IPv6-Adresse bewirbt.
  Die tatsächliche Bob-Charlie-Kommunikation kann über IPv4 oder IPv6 erfolgen (d.h. unabhängig von Alices Adresstyp).
- Ein Peer muss eine Tabelle aktiver Testzustände (nonces) führen. Beim Empfang einer PeerTest-Nachricht die nonce in der Tabelle nachschlagen. Wenn gefunden, ist es ein bestehender Test und du kennst deine Rolle (Alice, Bob oder Charlie). Andernfalls, wenn die IP nicht vorhanden ist und der Port 0 ist, ist dies ein neuer Test und du bist Bob.
  Andernfalls ist dies ein neuer Test und du bist Charlie.
- Ab Version 0.9.15 muss Alice eine etablierte Session mit Bob haben und den Session-Schlüssel verwenden.
- Vor API-Version 0.9.52 antwortete Bob in einigen Implementierungen Alice mit Alices Intro-Schlüssel anstatt dem Alice/Bob-Session-Schlüssel, obwohl Alice und Bob eine etablierte Session haben (seit 0.9.15).
  Ab API-Version 0.9.52 wird Bob in allen Implementierungen korrekt den Session-Schlüssel verwenden, und Alice sollte eine von Bob empfangene Nachricht mit Alices Intro-Schlüssel ablehnen, wenn Bob API-Version 0.9.52 oder höher ist.
- Erweiterte Optionen im Header: Nicht erwartet, undefiniert.

### HolePunch {#holepunch}

Ein HolePunch ist einfach ein UDP-Paket ohne Daten. Es ist weder authentifiziert noch verschlüsselt. Es enthält keinen SSU-Header, daher hat es keine Nachrichtentypnummer. Es wird von Charlie an Alice als Teil der Introduction-Sequenz gesendet.

## Beispiel-Datagramme {#sampledatagrams}

### Minimale Datennachricht

- keine Fragmente, keine ACKs, keine NACKs, etc.
- Größe: 39 Bytes

```
+----+----+----+----+----+----+----+----+
|                  MAC                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                   IV                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag|        time       |flag|#frg|    |
+----+----+----+----+----+----+----+    +
|  padding to fit a full AES256 block   |
+----+----+----+----+----+----+----+----+
```
### Minimale Datennachricht mit Nutzlast

- Größe: 46+fragmentSize Bytes

```
+----+----+----+----+----+----+----+----+
|                  MAC                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                   IV                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag|        time       |flag|#frg|
+----+----+----+----+----+----+----+----+
  messageId    |   frag info  |         |
----+----+----+----+----+----+         +
| that many bytes of fragment data      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
```
## Referenzen

- [AES-Verschlüsselung](/docs/specs/cryptography/#AES)
- [Spezifikation gemeinsamer Strukturen](/docs/specs/common-structures/)
- [Datum](/docs/specs/common-structures/#date)
- [ElGamal-Verschlüsselung](/docs/specs/cryptography/#elgamal)
- [HMAC-Details](/docs/specs/cryptography/#udp)
- [I2P-Quellcode](https://github.com/i2p/i2p.i2p)
- [i2pd-Quellcode](https://github.com/PurpleI2P/i2pd)
- [KeyCertificate](/docs/specs/common-structures/#key-certificates)
- [RouterIdentity](/docs/specs/common-structures/#routeridentity)
- [SessionKey](/docs/specs/common-structures/#sessionkey)
- [Signatur](/docs/specs/common-structures/#signature)
- [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey)
- [SigningPublicKey](/docs/specs/common-structures/#signingpublickey)
- [SSU-Übersicht](/docs/transport/ssu/)
- [SSU-Schlüssel](/docs/transport/ssu/#keys)
- [SSU-Peer-Tests](/docs/transport/ssu/#peerTesting)
