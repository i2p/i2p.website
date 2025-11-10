---
title: "Multicast"
number: "101"
author: "zzz"
created: "2008-12-08"
lastupdated: "2009-03-25"
status: "Dead"
thread: "http://zzz.i2p/topics/172"
---

## Übersicht

Grundidee: Eine Kopie durch Ihren ausgehenden Tunnel senden, der ausgehende Endpunkt verteilt an alle eingehenden Gateways. Ende-zu-Ende-Verschlüsselung ausgeschlossen.


## Design

- Neuer Multicast-Typ für Tunnel-Nachrichten (Zustelltyp = 0x03)
- Ausgehender Endpunkt Multicast-Verteilung
- Neuer I2NP Multicast-Nachrichtentyp?
- Neuer I2CP Multicast SendMessageMessage Nachrichtentyp
- Keine Verschlüsselung von Router zu Router in OutNetMessageOneShotJob (Knoblauch?)

App:

- RTSP-Proxy?

Streamr:

- MTU anpassen? Oder einfach in der App erledigen?
- Empfang und Übertragung auf Abruf
