---
title: "Ministreaming-Bibliothek"
description: "Historische Notizen zu I2P's erster TCP-ähnlicher Transportschicht"
slug: "ministreaming"
aliases:
  - "/de/ministreaming"
  - "/de/ministreaming/"
lastUpdated: "2025-02"
accurateFor: "historical"
---

## Hinweis

Die Ministreaming-Bibliothek wurde durch die "vollständige" [Streaming-Bibliothek](/docs/api/streaming) erweitert und verbessert. Ministreaming ist veraltet und nicht kompatibel mit heutigen Anwendungen. Die folgende Dokumentation ist veraltet. Beachten Sie auch, dass Streaming das Ministreaming im gleichen Java-Paket (net.i2p.client.streaming) erweitert, sodass die aktuelle API-Dokumentation beide enthält. Veraltete Ministreaming-Klassen und -Methoden sind in den Javadocs klar als deprecated markiert.

## Ministreaming-Bibliothek

Die ministreaming-Bibliothek ist eine Schicht über dem Kern-[I2CP](/docs/protocol/i2cp), die zuverlässige, geordnete und authentifizierte Nachrichtenströme über eine unzuverlässige, ungeordnete und nicht authentifizierte Nachrichtenschicht ermöglicht. Genau wie bei der TCP-zu-IP-Beziehung bietet diese Streaming-Funktionalität eine ganze Reihe von Kompromissen und Optimierungen, aber anstatt diese Funktionalität in den I2P-Grundcode zu integrieren, wurde sie in eine eigene Bibliothek ausgelagert, um sowohl die TCP-ähnlichen Komplexitäten getrennt zu halten als auch alternative optimierte Implementierungen zu ermöglichen.

Die ministreaming-Bibliothek wurde von mihi als Teil seiner [I2PTunnel](/docs/api/i2ptunnel)-Anwendung geschrieben und dann ausgegliedert und unter der BSD-Lizenz veröffentlicht. Sie wird "mini"streaming-Bibliothek genannt, weil sie einige Vereinfachungen in der Implementierung vornimmt, während eine robustere streaming-Bibliothek für den Betrieb über I2P weiter optimiert werden könnte. Die beiden Hauptprobleme der ministreaming-Bibliothek sind die Verwendung des traditionellen TCP-Zweiphasen-Aufbauprotokolls und die derzeit feste Fenstergröße von 1. Das Aufbauproblem ist bei langlebigen Streams geringfügig, aber bei kurzen, wie schnellen HTTP-Anfragen, kann die Auswirkung erheblich sein. Was die Fenstergröße angeht, so führt die ministreaming-Bibliothek keine ID oder Reihenfolge innerhalb der gesendeten Nachrichten (oder enthält keine ACK oder SACK auf Anwendungsebene), daher muss sie im Durchschnitt doppelt so lange warten, wie es dauert, eine Nachricht zu senden, bevor sie eine weitere sendet.

Trotz dieser Probleme funktioniert die ministreaming-Bibliothek in vielen Situationen recht gut, und ihre API ist sowohl sehr einfach als auch in der Lage, unverändert zu bleiben, wenn verschiedene Streaming-Implementierungen eingeführt werden. Die Bibliothek wird in ihrer eigenen ministreaming.jar bereitgestellt. Java-Entwickler, die sie verwenden möchten, können direkt auf die API zugreifen, während Entwickler in anderen Sprachen sie über die Streaming-Unterstützung von [SAM](/docs/api/samv3) nutzen können.
