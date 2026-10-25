---
title: "Datagramme"
description: "Authentifizierte, antwortfähige und rohe Nachrichtenformate über I2CP"
slug: "datagrams"
aliases:
  - "/de/datagrams"
  - "/de/datagrams/"
lastUpdated: "2025-04"
accurateFor: "0.9.66"
---

## Datagram-Übersicht {#overview}

Datagrams bauen auf dem grundlegenden [I2CP](/docs/specs/i2cp) auf, um authentifizierte und beantwortbare Nachrichten in einem Standardformat bereitzustellen. Dies ermöglicht es Anwendungen, die "Absender"-Adresse zuverlässig aus einem Datagram zu lesen und zu wissen, dass die Adresse die Nachricht wirklich gesendet hat. Dies ist für einige Anwendungen notwendig, da die grundlegende I2P-Nachricht völlig roh ist - sie hat keine "Absender"-Adresse (im Gegensatz zu IP-Paketen). Zusätzlich werden die Nachricht und der Absender durch Signierung der Payload authentifiziert.

Datagrams sind, wie [streaming library packets](/docs/api/streaming), ein Konstrukt auf Anwendungsebene. Diese Protokolle sind unabhängig von den Low-Level-[Transports](/docs/overview/transport); die Protokolle werden vom router in I2NP-Nachrichten umgewandelt, und beide Protokolle können von beiden Transports übertragen werden.

## Anwendungsleitfaden {#application}

In Java geschriebene Anwendungen können die Datagram-API verwenden, während Anwendungen in anderen Sprachen die Datagram-Unterstützung von [SAM](/docs/api/samv3) nutzen können. Es gibt auch begrenzte Unterstützung in i2ptunnel im [SOCKS proxy](/docs/api/socks), den 'streamr' tunnel-Typen und udpTunnel-Klassen.

### Datagram-Länge {#length}

Der Anwendungsdesigner sollte sorgfältig den Kompromiss zwischen beantwortbaren und nicht-beantwortbaren Datagrammen abwägen. Außerdem beeinflusst die Datagramm-Größe die Zuverlässigkeit, da es zur tunnel-Fragmentierung in 1KB tunnel-Nachrichten kommt. Je mehr Nachrichtenfragmente vorhanden sind, desto wahrscheinlicher ist es, dass eines davon von einem Zwischenknoten verworfen wird. Nachrichten größer als einige KB werden nicht empfohlen. Bei etwa 10 KB sinkt die Zustellwahrscheinlichkeit dramatisch.

[Siehe die Datagrams-Spezifikationsseite.](/docs/specs/datagrams)

Beachten Sie auch, dass die verschiedenen Overheads, die von unteren Schichten hinzugefügt werden, insbesondere garlic messages, eine große Belastung für intermittierende Nachrichten darstellen, wie sie von einer Kademlia-over-UDP-Anwendung verwendet werden. Die Implementierungen sind derzeit für häufigen Datenverkehr unter Verwendung der Streaming-Bibliothek optimiert.

### I2CP-Protokollnummer und Ports {#protocol}

Die Standard-I2CP-Protokollnummer für signierte (beantwortbare) Datagramme ist PROTO_DATAGRAM (17). Anwendungen können wählen, ob sie das Protokoll im I2CP-Header setzen oder nicht. Der Standard ist implementierungsabhängig. Es muss gesetzt werden, um Datagramm- und Streaming-Verkehr zu demultiplexen, der an derselben Destination empfangen wird.

Da Datagramme nicht verbindungsorientiert sind, kann die Anwendung Portnummern benötigen, um Datagramme mit bestimmten Peers oder Kommunikationssitzungen zu korrelieren, wie es bei UDP über IP üblich ist. Anwendungen können 'from'- und 'to'-Ports zum I2CP (gzip) Header hinzufügen, wie auf der [I2CP-Seite](/docs/specs/i2cp#format) beschrieben.

Es gibt keine Methode innerhalb der Datagram-API, um anzugeben, ob es nicht beantwortbar (raw) oder beantwortbar ist. Die Anwendung sollte so entworfen werden, dass sie den entsprechenden Typ erwartet. Die I2CP-Protokollnummer oder der Port sollte von der Anwendung verwendet werden, um den Datagram-Typ anzuzeigen. Die I2CP-Protokollnummern PROTO_DATAGRAM (signiert, auch bekannt als Datagram1), PROTO_DATAGRAM_RAW, PROTO_DATAGRAM2 und PROTO_DATAGRAM3 sind in der I2PSession-API für diesen Zweck definiert. Ein gängiges Designmuster in Client/Server-Datagram-Anwendungen ist die Verwendung signierter Datagrams für eine Anfrage, die eine Nonce enthält, und die Verwendung eines Raw-Datagrams für die Antwort, wobei die Nonce aus der Anfrage zurückgegeben wird.

**Standardwerte:**

- PROTO_DATAGRAM = 17
- PROTO_DATAGRAM_RAW = 18
- PROTO_DATAGRAM2 = 19
- PROTO_DATAGRAM3 = 20

### Datenintegrität {#integrity}

Die Datenintegrität wird durch die gzip CRC-32-Prüfsumme gewährleistet, die in [der I2CP-Schicht](/docs/specs/i2cp#format) implementiert ist. Authentifizierte Datagramme (Datagram1 und Datagram2) gewährleisten ebenfalls die Integrität. Es gibt kein Prüfsummenfeld im Datagramm-Protokoll.

### Paket-Kapselung {#encapsulation}

Jedes Datagramm wird durch I2P als einzelne Nachricht gesendet (oder als individuelle Nelke in einer [Garlic Message](/docs/overview/garlic-routing)). Die Nachrichtenkapselung wird in den zugrundeliegenden [I2CP](/docs/specs/i2cp)-, [I2NP](/docs/specs/i2np)- und [tunnel message](/docs/specs/tunnel-message)-Schichten implementiert. Es gibt keinen Pakettrennmechanismus oder Längenfeld im Datagramm-Protokoll.

## Spezifikation {#spec}

[Siehe die Datagrams-Spezifikationsseite.](/docs/specs/datagrams)
