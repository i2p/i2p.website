---
title: "Ministreaming-Bibliothek"
description: "Historische Anmerkungen zur ersten TCP-ähnlichen Transportschicht von I2P"
slug: "ministreaming"
lastUpdated: "2025-02"
accurateFor: "historical"
---

> **Veraltet:** Die Ministreaming-Bibliothek entstand vor der heutigen [Streaming-Bibliothek](/docs/specs/streaming/). Moderne Anwendungen müssen die vollständige Streaming-API oder SAM v3 verwenden. Die folgenden Informationen werden für Entwickler beibehalten, die den in `ministreaming.jar` ausgelieferten Legacy-Quellcode prüfen.

## Überblick

Ministreaming (leichtgewichtiges Streaming-Protokoll) baut auf [I2CP](/docs/specs/i2cp/) auf, um eine zuverlässige, geordnete Zustellung über die Nachrichtenebene von I2P bereitzustellen—ähnlich wie TCP über IP. Es wurde ursprünglich aus der frühen **I2PTunnel**-Anwendung (BSD-lizenziert) herausgelöst, damit sich alternative Transportprotokolle unabhängig entwickeln konnten.

Wesentliche Entwurfsbeschränkungen:

- Klassischer zweiphasiger Verbindungsaufbau (SYN/ACK/FIN), aus TCP übernommen
- Feste Fenstergröße von **1** Paket
- Keine IDs pro Paket oder selektive Bestätigungen

Diese Entscheidungen haben die Implementierung klein gehalten, begrenzen jedoch den Durchsatz—jedes Paket wartet normalerweise fast zwei RTTs (Round-Trip-Zeiten), bevor das nächste gesendet wird. Für lang andauernde Streams ist die Verzögerung akzeptabel, aber kurze HTTP-artige Austauschvorgänge leiden spürbar.

## Beziehung zur Streaming-Bibliothek

Die aktuelle Streaming-Bibliothek verwendet weiterhin dasselbe Java-Paket (`net.i2p.client.streaming`). Veraltete Klassen und Methoden bleiben in den Javadocs erhalten und sind klar gekennzeichnet, damit Entwickler APIs aus der ministreaming-Ära (ältere Streaming-Bibliothek) erkennen können. Als die Streaming-Bibliothek ministreaming ablöste, fügte sie Folgendes hinzu:

- Intelligenter Verbindungsaufbau mit weniger Round-Trips
- Adaptive Staukontrollfenster und Wiederübertragungslogik
- Bessere Leistung über verlustbehaftete tunnels

## Wann war Ministreaming nützlich?

Trotz seiner Grenzen bot ministreaming (eine minimalistische Streaming-Implementierung) in den frühesten Bereitstellungen zuverlässigen Transport. Die API war absichtlich klein und zukunftssicher gehalten, sodass alternative Streaming-Engines ausgetauscht werden konnten, ohne Änderungen an den aufrufenden Anwendungen zu erfordern. Java-Anwendungen banden sie direkt ein; Nicht-Java-Clients griffen über die [SAM](/docs/legacy/sam/)-Unterstützung für Streaming-Sitzungen auf dieselbe Funktionalität zu.

Aktuell ist `ministreaming.jar` nur als Kompatibilitätsschicht zu betrachten. Neuentwicklungen sollten:

1. Verwenden Sie die vollständige Streaming-Bibliothek (Java) oder SAM v3 (`STREAM`-Stil)  
2. Entfernen Sie beim Modernisieren des Codes alle verbleibenden Fixed-Window-Annahmen  
3. Bevorzugen Sie größere Fenstergrößen und optimierte Verbindungs-Handshakes, um die Leistung latenzkritischer Arbeitslasten zu verbessern

## Referenz

- [Dokumentation zur Streaming-Bibliothek](/docs/specs/streaming/)
- [Streaming-Javadoc](http://idk.i2p/javadoc-i2p/net/i2p/client/streaming/package-summary.html) – enthält veraltete Ministreaming-Klassen
- [SAM v3-Spezifikation](/docs/api/samv3/) – Streaming-Unterstützung für Nicht-Java-Anwendungen

Wenn Sie auf Code stoßen, der noch von ministreaming (veraltetes minimalistisches Streaming-Subsystem) abhängt, planen Sie, ihn auf die moderne Streaming-API zu portieren — das Netzwerk und sein Tooling erwarten das neuere Verhalten.
