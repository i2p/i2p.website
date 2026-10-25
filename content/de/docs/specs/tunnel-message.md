---
title: "Tunnel-Nachrichten-Spezifikation"
description: "Spezifikation für das Format von tunnel-Nachrichten in I2P"
slug: "tunnel-message"
aliases:
  - "/de/docs/legacy/tunnel-message"
  - "/de/docs/legacy/tunnel-message/"
  - "/de/tunnel_message_spec"
  - "/de/tunnel_message_spec/"
category: "Design"
lastUpdated: "2021-01"
accurateFor: "0.9.49"
---

## Überblick

Dieses Dokument spezifiziert das Format von tunnel-Nachrichten. Für allgemeine Informationen über tunnels siehe die [tunnel-Dokumentation](/docs/specs/tunnel-implementation).

## Nachrichtenvorverarbeitung

Ein *tunnel gateway* ist der Eingang oder erste Hop eines tunnels. Bei einem ausgehenden tunnel ist das gateway der Ersteller des tunnels. Bei einem eingehenden tunnel befindet sich das gateway am entgegengesetzten Ende zum Ersteller des tunnels.

Ein Gateway *verarbeitet* [I2NP](/docs/specs/i2np) Nachrichten vor, indem es sie fragmentiert und zu tunnel-Nachrichten zusammenfasst.

Während I2NP-Nachrichten eine variable Größe von 0 bis fast 64 KB haben, sind tunnel-Nachrichten von fester Größe, etwa 1 KB. Die feste Nachrichtengröße schränkt verschiedene Arten von Angriffen ein, die durch die Beobachtung der Nachrichtengröße möglich wären.

Nachdem die tunnel-Nachrichten erstellt wurden, werden sie wie in der [tunnel-Dokumentation](/docs/specs/tunnel-implementation) beschrieben verschlüsselt.

### Tunnel-Nachricht (Verschlüsselt)

Dies sind die Inhalte einer tunnel-Datennachricht nach der Verschlüsselung.

```
+----+----+----+----+----+----+----+----+
|    Tunnel ID      |       IV          |
+----+----+----+----+                   +
|                                       |
+                   +----+----+----+----+
|                   |                   |
+----+----+----+----+                   +
|                                       |
+           Encrypted Data              +
~                                       ~
|                                       |
+                   +-------------------+
|                   |
+----+----+----+----+
```
**Tunnel ID** :: [TunnelId](/docs/specs/common-structures#tunnelid) : 4 Bytes. Die ID des nächsten Hops, ungleich null.

**IV** :: : 16 Bytes. Der Initialisierungsvektor.

**Verschlüsselte Daten** :: : 1008 Bytes. Die verschlüsselte Tunnel-Nachricht.

**Gesamtgröße: 1028 Bytes**

### Tunnel-Nachricht (Entschlüsselt)

Dies sind die Inhalte einer tunnel data message, wenn sie entschlüsselt ist.

```
+----+----+----+----+----+----+----+----+
|    Tunnel ID      |       IV          |
+----+----+----+----+                   +
|                                       |
+                   +----+----+----+----+
|                   |     Checksum      |
+----+----+----+----+----+----+----+----+
|          nonzero padding...           |
~                                       ~
|                                       |
+                                  +----+
|                                  |zero|
+----+----+----+----+----+----+----+----+
|                                       |
|       Delivery Instructions  1        |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+       I2NP Message Fragment 1         +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
|       Delivery Instructions 2...      |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+       I2NP Message Fragment 2...      +
|                                       |
~                                       ~
|                                       |
+                   +-------------------+
|                   |
+----+----+----+----+
```
**Tunnel ID** :: [TunnelId](/docs/specs/common-structures#tunnelid) : 4 Bytes. Die ID des nächsten Hops, ungleich null.

**IV** :: : 16 Bytes. Der Initialisierungsvektor.

**Checksum** :: : 4 Bytes. Die ersten 4 Bytes des SHA256-Hashes von (dem Inhalt der Nachricht (nach dem Null-Byte) + IV).

**Nonzero padding** :: : 0 oder mehr Bytes. Zufällige Nonzero-Daten zur Auffüllung.

**Zero** :: : 1 Byte. Der Wert 0x00.

**Lieferungsanweisungen** :: TunnelMessageDeliveryInstructions : Länge variiert, aber ist typischerweise 7, 39, 43 oder 47 Bytes. Gibt das Fragment und das Routing für das Fragment an.

**Message Fragment** :: : 1 bis 996 Bytes, das tatsächliche Maximum hängt von der Größe der Zustellungsanweisung ab. Eine teilweise oder vollständige I2NP Message.

**Gesamtgröße: 1028 Bytes**

#### Hinweise

- Das Padding, falls vorhanden, muss vor den Anweisungs-/Nachrichtenpaaren stehen. Es ist keine Vorkehrung für Padding am Ende vorgesehen.
- Die Prüfsumme deckt NICHT das Padding oder das Null-Byte ab. Nehmen Sie die Nachricht beginnend bei den ersten Zustellungsanweisungen, verketten Sie den IV und erstellen Sie den Hash davon.

## Tunnel-Nachrichten-Zustellungsanweisungen

Die Anweisungen werden mit einem einzigen Kontrollbyte codiert, gefolgt von allen notwendigen zusätzlichen Informationen. Das erste Bit (MSB) in diesem Kontrollbyte bestimmt, wie der Rest des Headers interpretiert wird - wenn es nicht gesetzt ist, ist die Nachricht entweder nicht fragmentiert oder dies ist das erste Fragment in der Nachricht. Wenn es gesetzt ist, handelt es sich um ein nachfolgendes Fragment.

Diese Spezifikation gilt nur für Delivery Instructions innerhalb von Tunnel Messages. Beachten Sie, dass "Delivery Instructions" auch innerhalb von Garlic Cloves verwendet werden, wo das Format erheblich anders ist. Siehe die [I2NP-Dokumentation](/docs/specs/i2np#garlicclovedeliveryinstructions) für Details. Verwenden Sie die folgende Spezifikation NICHT für Garlic Clove Delivery Instructions!

### Anweisungen zur Übertragung des ersten Fragments

Wenn das MSB des ersten Bytes 0 ist, handelt es sich um ein erstes I2NP-Nachrichtenfragment oder eine vollständige (unfragmentierte) I2NP-Nachricht, und die Anweisungen sind:

```
+----+----+----+----+----+----+----+----+
|flag|  Tunnel ID (opt)  |              |
+----+----+----+----+----+              +
|                                       |
+                                       +
|         To Hash (optional)            |
+                                       +
|                                       |
+                        +--------------+
|                        |dly | Message
+----+----+----+----+----+----+----+----+
 ID (opt) |extended opts (opt)|  size   |
+----+----+----+----+----+----+----+----+
```
**flag** :: : 1 Byte. Bit-Reihenfolge: 76543210   - Bit 7: 0 um ein erstes Fragment oder eine nicht fragmentierte Nachricht anzugeben   - Bits 6-5: Zustellungstyp

    - 0x0 = LOCAL
    - 0x01 = TUNNEL
    - 0x02 = ROUTER
    - 0x03 = unused, invalid
    - Note: LOCAL is used for inbound tunnels only, unimplemented for outbound tunnels
- bit 4: Verzögerung enthalten? Nicht implementiert, immer 0. Falls 1, ist ein Verzögerungsbyte enthalten.
  - bit 3: fragmentiert? Falls 0, ist die Nachricht nicht fragmentiert, es folgt die gesamte Nachricht. Falls 1, ist die Nachricht fragmentiert, und die Anweisungen enthalten eine Message ID.
  - bit 2: erweiterte Optionen? Nicht implementiert, immer 0. Falls 1, sind erweiterte Optionen enthalten.
  - bits 1-0: reserviert, auf 0 gesetzt für Kompatibilität mit zukünftigen Verwendungen

**Tunnel ID** :: [TunnelId](/docs/specs/common-structures#tunnelid) : 4 Bytes. Optional, vorhanden wenn der Übermittlungstyp TUNNEL ist. Die Ziel-Tunnel-ID, ungleich null.

**To Hash** :: : 32 Bytes. Optional, vorhanden wenn der Delivery-Typ ROUTER oder TUNNEL ist. Bei ROUTER der SHA256-Hash des routers. Bei TUNNEL der SHA256-Hash des Gateway-routers.

**Delay** :: : 1 Byte. Optional, vorhanden wenn das Delay-Flag gesetzt ist. In tunnel-Nachrichten: Nicht implementiert, nie vorhanden; ursprüngliche Spezifikation: Bit 7: Typ (0 = strikt, 1 = randomisiert), Bits 6-0: Delay-Exponent (2^Wert Minuten).

**Message ID** :: : 4 Bytes. Optional, vorhanden wenn diese Nachricht das erste von 2 oder mehr Fragmenten ist (d.h. wenn das Fragmentierungs-Bit 1 ist). Eine ID, die alle Fragmente eindeutig als zu einer einzigen Nachricht gehörend identifiziert (die aktuelle Implementierung verwendet I2NPMessageHeader.msg_id).

**Erweiterte Optionen** :: : 2 oder mehr Bytes. Optional, vorhanden wenn das Flag für erweiterte Optionen gesetzt ist. Nicht implementiert, nie vorhanden; ursprüngliche Spezifikation: Ein Byte Länge und dann entsprechend viele Bytes.

**size** :: : 2 Bytes. Die Länge des folgenden Fragments. Gültige Werte: 1 bis ca. 960 in einer tunnel message.

**Gesamtlänge:** Typische Länge ist: - 3 Bytes für LOCAL-Zustellung (tunnel message) - 35 Bytes für ROUTER-Zustellung oder 39 Bytes für TUNNEL-Zustellung (unfragmentierte tunnel message) - 39 Bytes für ROUTER-Zustellung oder 43 Bytes für TUNNEL-Zustellung (erstes Fragment)

### Anweisungen zur Zustellung von Folgefragmenten

Wenn das MSB des ersten Bytes 1 ist, handelt es sich um ein Folgefragment, und die Anweisungen lauten:

```
+----+----+----+----+----+----+----+
|frag|     Message ID    |  size   |
+----+----+----+----+----+----+----+
```
**frag** :: : 1 Byte. Bit-Reihenfolge: 76543210. Binär 1nnnnnnd:   - Bit 7: 1 um anzuzeigen, dass dies ein Folgefragment ist   - Bits 6-1: nnnnnn ist die 6-Bit-Fragmentnummer von 1 bis 63   - Bit 0: d ist 1 um das letzte Fragment anzuzeigen, ansonsten 0

**Message ID** :: : 4 Bytes. Identifiziert die Fragment-Sequenz, zu der dieses Fragment gehört. Diese stimmt mit der Message ID eines initialen Fragments überein (ein Fragment mit Flag-Bit 7 auf 0 und Flag-Bit 3 auf 1 gesetzt).

**size** :: : 2 Bytes. Die Länge des nachfolgenden Fragments. Gültige Werte: 1 bis 996.

**Gesamtlänge: 7 Bytes**

## Notizen

### I2NP Nachricht Maximalgröße

Während die maximale I2NP-Nachrichtengröße nominell 64 KB beträgt, wird die Größe durch die Methode der Fragmentierung von I2NP-Nachrichten in mehrere 1 KB tunnel-Nachrichten weiter eingeschränkt. Die maximale Anzahl von Fragmenten beträgt 64, und das erste Fragment ist möglicherweise nicht perfekt am Anfang einer tunnel-Nachricht ausgerichtet. Daher muss die Nachricht nominell in 63 Fragmente passen.

Die maximale Größe eines anfänglichen Fragments beträgt 956 Bytes (bei TUNNEL-Übertragungsmodus); die maximale Größe eines nachfolgenden Fragments beträgt 996 Bytes. Daher beträgt die maximale Größe ungefähr 956 + (62 * 996) = 62708 Bytes oder 61,2 KB.

### Reihenfolge, Stapelverarbeitung, Verpackung

Tunnel-Nachrichten können verworfen oder neu angeordnet werden. Das tunnel gateway, das tunnel-Nachrichten erstellt, kann frei jede Stapelverarbeitung-, Vermischungs- oder Neuanordnungsstrategie implementieren, um I2NP-Nachrichten zu fragmentieren und Fragmente effizient in tunnel-Nachrichten zu packen. Im Allgemeinen ist eine optimale Packung nicht möglich (das "Packungsproblem"). Die gateways können verschiedene Verzögerungs- und Neuanordnungsstrategien implementieren.

### Cover Traffic

Tunnel-Nachrichten können nur Padding enthalten (d.h. gar keine Zustellungsanweisungen oder Nachrichtenfragmente) für Tarndatenverkehr. Dies ist nicht implementiert.

## Referenzen

- **[I2NP]** [I2NP Protocol](/docs/specs/i2np)
- **[I2NP-GC]** [GarlicClove](/docs/specs/i2np#garlicclove)
- **[I2NP-GCDI]** [GarlicCloveDeliveryInstructions](/docs/specs/i2np#garlicclovedeliveryinstructions)
- **[TUNNEL-IMPL]** [Tunnel-Implementierung](/docs/specs/tunnel-implementation)
