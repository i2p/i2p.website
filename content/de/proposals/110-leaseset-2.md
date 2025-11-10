---
title: "LeaseSet 2"
number: "110"
author: "zzz"
created: "2014-01-22"
lastupdated: "2016-04-04"
status: "Abgelehnt"
thread: "http://zzz.i2p/topics/1560"
supercededby: "123"
---

## Übersicht

Dieser Vorschlag betrifft ein neues LeaseSet-Format mit Unterstützung für neuere Verschlüsselungsarten.

## Motivation

Die End-to-End-Kryptografie, die durch I2P-Tunnel verwendet wird, verfügt über separate Verschlüsselungs- und Signaturschlüssel. Die Signaturschlüssel befinden sich in der Tunnel-Destination, die bereits mit KeyCertificates erweitert wurde, um neuere Signaturtypen zu unterstützen. Allerdings sind die Verschlüsselungsschlüssel Teil des LeaseSets, das keine Zertifikate enthält. Daher ist es notwendig, ein neues LeaseSet-Format zu implementieren und die Unterstützung für dessen Speicherung im netDb hinzuzufügen.

Ein positiver Aspekt ist, dass sobald LS2 implementiert ist, alle bestehenden Destinationen von moderneren Verschlüsselungsarten Gebrauch machen können; Router, die ein LS2 abrufen und lesen können, werden garantiert Unterstützung für alle Verschlüsselungstypen haben, die damit eingeführt werden.

## Spezifikation

Das grundlegende LS2-Format würde folgendermaßen aussehen:

- dest
- Veröffentlichungszeitstempel (8 Byte)
- läuft ab (8 Byte)
- Subtyp (1 Byte) (normal, verschlüsselt, meta oder service)
- Flags (2 Byte)

- Subtypspezifischer Teil:
  - Verschlüsselungsart, Verschlüsselungsschlüssel und Leases für regulär
  - Blob für verschlüsselt
  - Eigenschaften, Hashes, Ports, Widerrufe, etc. für service

- Signatur
