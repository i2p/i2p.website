---
title: "ElGamal/AES + SessionTag Verschlüsselung"
description: "Legacy End-to-End-Verschlüsselung, die ElGamal, AES, SHA-256 und einmalige Session-Tags kombiniert"
slug: "elgamal-aes"
aliases:
  - "/de/how_elgamalaes"
  - "/de/how_elgamalaes/"
lastUpdated: "2020-04"
accurateFor: "0.9.46"
---

## Übersicht

ElGamal/AES+SessionTags wird für die Ende-zu-Ende-Verschlüsselung verwendet.

Als unzuverlässiges, ungeordnetes, nachrichtenbasiertes System verwendet I2P eine einfache Kombination aus asymmetrischen und symmetrischen Verschlüsselungsalgorithmen, um Datenvertraulichkeit und -integrität für garlic messages zu gewährleisten. Als Ganzes wird die Kombination als ElGamal/AES+SessionTags bezeichnet, aber das ist eine übermäßig ausführliche Art, die Verwendung von 2048bit ElGamal, AES256, SHA256 und 32-Byte-Nonces zu beschreiben.

Wenn ein router zum ersten Mal eine garlic-Nachricht an einen anderen router verschlüsseln möchte, verschlüsselt er das Schlüsselmaterial für einen AES256-Sitzungsschlüssel mit ElGamal und fügt die AES256/CBC-verschlüsselte Nutzlast nach diesem verschlüsselten ElGamal-Block hinzu. Zusätzlich zur verschlüsselten Nutzlast enthält der AES-verschlüsselte Abschnitt die Nutzlastlänge, den SHA256-Hash der unverschlüsselten Nutzlast sowie eine Anzahl von "session tags" - zufällige 32-Byte-Nonces. Wenn der Absender das nächste Mal eine garlic-Nachricht an einen anderen router verschlüsseln möchte, verschlüsselt er nicht mit ElGamal einen neuen Sitzungsschlüssel, sondern wählt einfach einen der zuvor übermittelten session tags aus und verschlüsselt die Nutzlast wie zuvor mit AES, wobei er den Sitzungsschlüssel verwendet, der mit diesem session tag verwendet wurde, und stellt den session tag selbst voran. Wenn ein router eine garlic-verschlüsselte Nachricht empfängt, überprüft er die ersten 32 Bytes, um zu sehen, ob sie mit einem verfügbaren session tag übereinstimmen - falls ja, entschlüsselt er die Nachricht einfach mit AES, aber falls nicht, entschlüsselt er den ersten Block mit ElGamal.

Jeder Session-Tag kann nur einmal verwendet werden, um zu verhindern, dass interne Angreifer unnötigerweise verschiedene Nachrichten als zwischen denselben Routern stehend korrelieren. Der Absender einer ElGamal/AES+SessionTag-verschlüsselten Nachricht wählt, wann und wie viele Tags geliefert werden, und stattet den Empfänger mit genügend Tags aus, um eine Salve von Nachrichten abzudecken. Garlic-Nachrichten können die erfolgreiche Tag-Zustellung erkennen, indem sie eine kleine zusätzliche Nachricht als Clove bündeln (eine "Zustellungsstatusnachricht") - wenn die Garlic-Nachricht beim beabsichtigten Empfänger ankommt und erfolgreich entschlüsselt wird, ist diese kleine Zustellungsstatusnachricht eine der freigelegten Cloves und enthält Anweisungen für den Empfänger, die Clove an den ursprünglichen Absender zurückzusenden (natürlich durch einen inbound tunnel). Wenn der ursprüngliche Absender diese Zustellungsstatusnachricht erhält, weiß er, dass die in der Garlic-Nachricht gebündelten Session-Tags erfolgreich zugestellt wurden.

Session tags haben selbst eine kurze Lebensdauer, nach der sie verworfen werden, wenn sie nicht verwendet werden. Zusätzlich ist die für jeden Schlüssel gespeicherte Menge begrenzt, ebenso wie die Anzahl der Schlüssel selbst - wenn zu viele ankommen, können entweder neue oder alte Nachrichten verworfen werden. Der Sender verfolgt, ob Nachrichten, die session tags verwenden, durchkommen, und wenn nicht ausreichend Kommunikation stattfindet, kann er diejenigen verwerfen, die zuvor als ordnungsgemäß zugestellt angenommen wurden, und zur vollständigen teuren ElGamal-Verschlüsselung zurückkehren. Eine Session wird weiter existieren, bis alle ihre Tags verbraucht sind oder ablaufen.

Sessions sind unidirektional. Tags werden von Alice an Bob übermittelt, und Alice verwendet dann die Tags nacheinander in nachfolgenden Nachrichten an Bob.

Sessions können zwischen Destinations, zwischen Routern oder zwischen einem Router und einer Destination eingerichtet werden. Jeder Router und jede Destination unterhält ihren eigenen Session Key Manager, um Session Keys und Session Tags zu verwalten. Separate Session Key Manager verhindern, dass Angreifer mehrere Destinations miteinander oder mit einem Router korrelieren können.

## Nachrichtenempfang

Jede empfangene Nachricht hat eine von zwei möglichen Bedingungen:

1. Es ist Teil einer bestehenden Session und enthält ein Session Tag und einen AES-verschlüsselten Block
2. Es ist für eine neue Session und enthält sowohl ElGamal- als auch AES-verschlüsselte Blöcke

Wenn ein router eine Nachricht erhält, wird er zunächst annehmen, dass sie von einer bestehenden Sitzung stammt und versuchen, den Session Tag nachzuschlagen und die folgenden Daten mit AES zu entschlüsseln. Falls das fehlschlägt, wird er annehmen, dass es sich um eine neue Sitzung handelt und versuchen, sie mit ElGamal zu entschlüsseln.

## New Session Message Spezifikation {#new}

Eine New Session ElGamal Message enthält zwei Teile, einen verschlüsselten ElGamal-Block und einen verschlüsselten AES-Block.

Die verschlüsselte Nachricht enthält:

```
   +----+----+----+----+----+----+----+----+
   |                                       |
   +                                       +
   |       ElGamal Encrypted Block         |
   ~                                       ~
   |                                       |
   +         +----+----+----+----+----+----+
   |         |                             |
   +----+----+                             +
   |                                       |
   +                                       +
   |         AES Encrypted Block           |
   ~                                       ~
   |                                       |
   +         +----+----+----+----+----+----+
   |         +
   +----+----+
```
### ElGamal-Block

Der verschlüsselte ElGamal Block ist immer 514 Bytes lang.

Die unverschlüsselten ElGamal-Daten sind 222 Bytes lang und enthalten:

```
   +----+----+----+----+----+----+----+----+
   |                                       |
   +                                       +
   |           Session Key                 |
   +                                       +
   |                                       |
   +                                       +
   |                                       |
   +----+----+----+----+----+----+----+----+
   |                                       |
   +                                       +
   |              Pre-IV                   |
   +                                       +
   |                                       |
   +                                       +
   |                                       |
   +----+----+----+----+----+----+----+----+
   +                                       +
   |                                       |
   +                                       +
   |       158 bytes random padding        |
   ~                                       ~
   |                                       |
   +                             +----+----+
   |                             |
   +----+----+----+----+----+----+
```
Der 32-Byte [Session Key](/docs/specs/common-structures#type_SessionKey) ist der Bezeichner für die Sitzung. Der 32-Byte Pre-IV wird verwendet, um den IV für den folgenden AES-Block zu generieren; der IV sind die ersten 16 Bytes des SHA-256-Hash des Pre-IV.

Die 222 Byte große Nutzlast wird [mit ElGamal](/docs/specs/cryptography#elgamal) verschlüsselt und der verschlüsselte Block ist 514 Bytes lang.

### AES Block {#aes}

Die unverschlüsselten Daten im AES-Block enthalten Folgendes:

```
   +----+----+----+----+----+----+----+----+
   |tag count|                             |
   +----+----+                             +
   |                                       |
   +                                       +
   |          Session Tags                 |
   ~                                       ~
   |                                       |
   +                                       +
   |                                       |
   +         +----+----+----+----+----+----+
   |         |    payload size   |         |
   +----+----+----+----+----+----+         +
   |                                       |
   +                                       +
   |          Payload Hash                 |
   +                                       +
   |                                       |
   +                             +----+----+
   |                             |flag|    |
   +----+----+----+----+----+----+----+    +
   |                                       |
   +                                       +
   |          New Session Key (opt.)       |
   +                                       +
   |                                       |
   +                                  +----+
   |                                  |    |
   +----+----+----+----+----+----+----+    +
   |                                       |
   +                                       +
   |           Payload                     |
   ~                                       ~
   |                                       |
   +                        +----//---+----+
   |                        |              |
   +----+----+----//---+----+              +
   |          Padding to 16 bytes          |
   +----+----+----+----+----+----+----+----+
```
#### Definition

```
tag count:
    2-byte Integer, 0-200

Session Tags:
    That many 32-byte SessionTags

payload size:
    4-byte Integer

Payload Hash:
    The 32-byte SHA256 Hash of the payload

flag:
    A one-byte value. Normally == 0. If == 0x01, a Session Key follows

New Session Key:
    A 32-byte SessionKey,
    to replace the old key, and is only present if preceding flag is 0x01

Payload:
    the data

Padding:
    Random data to a multiple of 16 bytes for the total length.
    May contain more than the minimum required padding.
```
Mindestlänge: 48 Bytes

Die Daten werden dann [AES-verschlüsselt](/docs/specs/cryptography), unter Verwendung des Sitzungsschlüssels und IV (berechnet aus dem Pre-IV) aus dem ElGamal-Abschnitt. Die Länge des verschlüsselten AES-Blocks ist variabel, aber immer ein Vielfaches von 16 Bytes.

#### Notizen

- Die tatsächliche maximale Payload-Länge und maximale Block-Länge ist kleiner als 64 KB; siehe die [I2NP Übersicht](/docs/protocol/i2np).
- New Session Key wird derzeit nicht verwendet und ist nie vorhanden.

## Spezifikation für bestehende Session-Nachrichten {#existing}

Die erfolgreich übermittelten Session-Tags werden für eine kurze Zeit (derzeit 15 Minuten) gespeichert, bis sie verwendet oder verworfen werden. Ein Tag wird verwendet, indem es in eine Existing Session Message verpackt wird, die nur einen AES-verschlüsselten Block enthält und nicht von einem ElGamal-Block vorangestellt wird.

Die bestehende Session-Nachricht lautet wie folgt:

```
   +----+----+----+----+----+----+----+----+
   |                                       |
   +                                       +
   |            Session Tag                |
   +                                       +
   |                                       |
   +                                       +
   |                                       |
   +----+----+----+----+----+----+----+----+
   |                                       |
   +                                       +
   |         AES Encrypted Block           |
   ~                                       ~
   |                                       |
   +                                       +
   |                                       |
   +----+----+----+----+----+----+----+----+
```
#### Definition

```
Session Tag:
    A 32-byte SessionTag
    previously delivered in an AES block

AES Encrypted Block:
    As specified above.
```
Der Session-Tag dient auch als Pre-IV. Der IV sind die ersten 16 Bytes des SHA-256-Hashes des sessionTag.

Um eine Nachricht aus einer bestehenden Sitzung zu entschlüsseln, sucht ein router nach dem Session Tag, um einen zugehörigen Session Key zu finden. Wenn der Session Tag gefunden wird, wird der AES-Block mit dem zugehörigen Session Key entschlüsselt. Wenn der Tag nicht gefunden wird, wird angenommen, dass es sich bei der Nachricht um eine [New Session Message](#new) handelt.

## Konfigurationsoptionen für Session Tags {#config}

Ab Version 0.9.2 kann der Client die Standard-Anzahl der zu sendenden Session Tags und die niedrige Tag-Schwelle für die aktuelle Sitzung konfigurieren. Für kurze Streaming-Verbindungen oder Datagramme können diese Optionen verwendet werden, um die Bandbreite erheblich zu reduzieren. Siehe die [I2CP-Optionsspezifikation](/docs/protocol/i2cp#options) für Details. Die Sitzungseinstellungen können auch pro Nachricht überschrieben werden. Siehe die [I2CP Send Message Expires-Spezifikation](/docs/specs/i2cp#msg_SendMessageExpires) für Details.

## Zukünftige Arbeiten {#future}

**Hinweis:** ElGamal/AES+SessionTags wird durch ECIES-X25519-AEAD-Ratchet (Vorschlag 144) ersetzt. Die unten referenzierten Probleme und Ideen wurden in das Design des neuen Protokolls eingearbeitet. Die folgenden Punkte werden in ElGamal/AES+SessionTags nicht behandelt.

Es gibt viele mögliche Bereiche, um die Algorithmen des Session Key Managers zu optimieren; einige können mit dem Verhalten der Streaming-Bibliothek interagieren oder erhebliche Auswirkungen auf die Gesamtleistung haben.

- Die Anzahl der übermittelten Tags könnte von der Nachrichtengröße abhängen, wobei das eventuelle Padding auf 1KB auf der tunnel message Ebene zu berücksichtigen ist.

- Clients könnten eine Schätzung der Sitzungsdauer an den router senden, als Empfehlung für die Anzahl der benötigten Tags.

- Die Lieferung von zu wenigen Tags führt dazu, dass der router auf eine teure ElGamal-Verschlüsselung zurückgreift.

- Der router kann die Zustellung von Session Tags annehmen oder auf eine Bestätigung warten, bevor er sie verwendet;
  es gibt Kompromisse für jede Strategie.

- Für sehr kurze Nachrichten könnten fast die vollen 222 Bytes der pre-IV- und Padding-Felder im ElGamal-Block für die gesamte Nachricht verwendet werden, anstatt eine Sitzung zu etablieren.

- Padding-Strategie bewerten; derzeit padden wir auf mindestens 128 Bytes.
  Es wäre besser, kleinen Nachrichten ein paar Tags hinzuzufügen, anstatt zu padden.

- Vielleicht könnten die Dinge effizienter sein, wenn das Session Tag System bidirektional wäre,
  so dass Tags, die im 'Vorwärts'-Pfad übertragen werden, im 'Rückwärts'-Pfad verwendet werden könnten,
  wodurch ElGamal in der ersten Antwort vermieden würde.
  Der Router wendet derzeit einige solcher Tricks an, wenn er
  tunnel Test-Nachrichten an sich selbst sendet.

- Wechsel von Session Tags zu
  [einem synchronisierten PRNG](/docs/overview/performance#future#prng).

- Mehrere dieser Ideen könnten einen neuen I2NP-Nachrichtentyp erfordern, oder
  ein Flag in den
  [Delivery Instructions](/docs/specs/tunnel-message#struct_TunnelMessageDeliveryInstructions) setzen,
  oder eine magische Zahl in den ersten Bytes des Session Key-Felds setzen
  und ein geringes Risiko akzeptieren, dass der zufällige Session Key mit der magischen Zahl übereinstimmt.
