---
title: "NTCP-Verschleierung"
number: "106"
author: "zzz"
created: "2010-11-23"
lastupdated: "2014-01-03"
status: "Abgelehnt"
thread: "http://zzz.i2p/topics/774"
supercededby: "111"
---

## Überblick

Dieser Vorschlag bezieht sich auf die Überarbeitung des NTCP-Transports, um seine Widerstandsfähigkeit gegen automatisierte Identifikation zu verbessern.

## Motivation

NTCP-Daten sind nach der ersten Nachricht verschlüsselt (und die erste Nachricht erscheint als Zufallsdaten), was die Protokollidentifikation durch "Payload-Analyse" verhindert. Es ist jedoch immer noch anfällig für die Protokollidentifikation durch "Flow-Analyse". Das liegt daran, dass die ersten 4 Nachrichten (d. h. der Handshake) eine feste Länge haben (288, 304, 448 und 48 Bytes).

Durch das Hinzufügen zufälliger Mengen an Zufallsdaten zu jeder der Nachrichten können wir es erheblich schwerer machen.

## Änderungen am NTCP

Dies ist ziemlich aufwändig, verhindert jedoch jede Erkennung durch DPI-Geräte.

Die folgenden Daten werden am Ende der 288-Byte-Nachricht 1 hinzugefügt:

- Ein 514-Byte-ElGamal-verschlüsselter Block
- Zufälliges Padding

Der ElG-Block ist zu Bobs öffentlichem Schlüssel verschlüsselt. Wenn er zu 222 Bytes entschlüsselt wird, enthält er:
- 214 Bytes zufälliges Padding
- 4 Bytes 0 reserviert
- 2 Bytes Padding-Länge die folgt
- 2 Bytes Protokollversion und Flags

In den Nachrichten 2-4 geben die letzten beiden Bytes des Paddings nun die Länge von weiterem Padding an, das folgen soll.

Beachten Sie, dass der ElG-Block keine perfekte Vorwärts-Sicherheit hat, aber es gibt dort nichts Interessantes.

Wir könnten unsere ElG-Bibliothek modifizieren, sodass sie kleinere Datenmengen verschlüsselt, falls wir denken, dass 514 Bytes viel zu viel sind? Ist ElG-Verschlüsselung für jedes NTCP-Setup zu viel?

Die Unterstützung hierfür würde in der netdb RouterAddress mit der Option "version=2" angezeigt. Wenn nur 288 Bytes in Nachricht 1 empfangen werden, wird angenommen, dass Alice Version 1 ist und in den folgenden Nachrichten wird kein Padding gesendet. Beachten Sie, dass die Kommunikation blockiert werden könnte, wenn ein MITM IP auf 288 Bytes fragmentiert (laut Brandon sehr unwahrscheinlich).
