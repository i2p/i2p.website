---
title: "'Verschlüsseltes' Streaming-Flag"
number: "114"
author: "orignal"
created: "2015-01-21"
lastupdated: "2015-01-21"
status: "Forschung-erforderlich"
thread: "http://zzz.i2p/topics/1795"
---

## Übersicht

Dieser Vorschlag betrifft das Hinzufügen eines Flags zum Streaming, das den Typ der
Ende-zu-Ende-Verschlüsselung spezifiziert.


## Motivation

Stark ausgelastete Apps können auf einen Mangel an ElGamal/AES+SessionTags stoßen.


## Design

Fügen Sie irgendwo im Streaming-Protokoll ein neues Flag hinzu. Wenn ein Paket mit
diesem Flag kommt, bedeutet das, dass die Nutzlast durch einen Schlüssel aus dem privaten Schlüssel und dem öffentlichen Schlüssel des Partners AES-verschlüsselt ist. Das würde es ermöglichen, die Garlic- (ElGamal/AES) Verschlüsselung zu eliminieren und das Problem des Tag-Mangels zu lösen.

Kann pro Paket oder pro Stream durch SYN gesetzt werden.
