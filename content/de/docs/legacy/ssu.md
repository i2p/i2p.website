---
title: "SSU (veraltet)"
description: "Ursprünglicher Secure Semireliable UDP-Transport"
slug: "ssu"
lastUpdated: "2025-01"
accurateFor: "0.9.64"
reviewStatus: "needs-review"
---

> **Veraltet:** SSU wurde durch SSU2 ersetzt. Die Unterstützung für SSU wurde aus i2pd 2.44.0 (API 0.9.56, Nov 2022) und aus Java I2P 2.4.0 (API 0.9.61, Dez 2023) entfernt.

SSU bot eine UDP-basierte, halbzuverlässige Übertragung mit Staukontrolle, NAT-Traversal und Unterstützung für Introducer. Es ergänzte NTCP, indem es router hinter NAT/Firewalls handhabte und die IP-Ermittlung koordinierte.

## Adress-Elemente

- `transport`: `SSU`
- `caps`: Fähigkeits-Flags (`B`, `C`, `4`, `6`, usw.)
- `host` / `port`: IPv4- oder IPv6-Listener (optional, wenn der router hinter einer Firewall ist)
- `key`: Base64-Einführungsschlüssel
- `mtu`: Optional; Standardwert 1484 (IPv4) / 1488 (IPv6)
- `ihost/ikey/iport/itag/iexp`: Introducer-Einträge (Vermittler-Einträge), wenn der router hinter einer Firewall ist

## Funktionen

- Kooperative NAT-Traversierung unter Verwendung von introducers (Vermittler)
- Erkennung der lokalen IP über Peer-Tests und die Inspektion eingehender Pakete
- Automatisches Weiterleiten des Firewall-Status an andere Transportprotokolle und die router-Konsole
- Teilweise zuverlässige Zustellung: Nachrichten werden bis zu einer Grenze erneut übertragen und danach verworfen
- Staukontrolle mit additiver Erhöhung / multiplikativer Verringerung und Fragment-ACK-Bitfeldern

SSU übernahm auch Metadatenaufgaben wie Timing-Beacons (Zeitsignale) und die MTU-Aushandlung. Die gesamte Funktionalität wird inzwischen (mit moderner Kryptografie) von [SSU2](/docs/specs/ssu2/) bereitgestellt.
