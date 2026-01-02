---
title: "Unidirektionale Tunnels"
description: "Historische Zusammenfassung des unidirektionalen tunnel-Designs von I2P."
slug: "unidirectional"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

> **Historischer Hinweis:** Diese Seite bewahrt die ältere Diskussion über „Unidirectional Tunnels“ als Referenz. Für das aktuelle Verhalten siehe die aktive [tunnel-Implementierungsdokumentation](/docs/specs/implementation/).

## Überblick

I2P baut **unidirektionale tunnel**: Ein tunnel transportiert ausgehenden Verkehr und ein separater tunnel transportiert eingehende Antworten. Diese Struktur geht auf die frühesten Netzwerkentwürfe zurück und ist weiterhin ein zentrales Unterscheidungsmerkmal gegenüber bidirektionalen Circuit-Systemen wie Tor. Begriffe und Implementierungsdetails finden sich in der [tunnel-Übersicht](/docs/overview/tunnel-routing/) und der [tunnel-Spezifikation](/docs/specs/implementation/).

## Überprüfung

- Unidirektionale tunnel halten Anfrage- und Antwortverkehr getrennt, sodass jede einzelne Gruppe absprechender Peers nur die Hälfte einer gesamten Hin- und Rückkommunikation beobachtet.
- Timing-Angriffe müssen sich über zwei tunnel-Pools (ausgehend und eingehend) erstrecken, statt eine einzelne Verbindung zu analysieren, was Korrelationen erschwert.
- Unabhängige eingehende und ausgehende Pools ermöglichen es routers, Latenz, Kapazität und Eigenschaften der Fehlerbehandlung je Richtung anzupassen.
- Zu den Nachteilen zählen eine erhöhte Komplexität beim Peer-Management und die Notwendigkeit, mehrere tunnel-Sets zu pflegen, um eine zuverlässige Dienstbereitstellung zu gewährleisten.

## Anonymität

Hermann und Grothoffs Aufsatz, [*I2P is Slow… and What to Do About It*](http://grothoff.org/christian/i2p.pdf), analysiert Vorgängerangriffe gegen unidirektionale tunnels und legt nahe, dass entschlossene Angreifer langfristige Peers schließlich bestätigen können. Rückmeldungen aus der Community weisen darauf hin, dass die Studie auf spezifischen Annahmen über die Geduld und die rechtlichen Befugnisse von Angreifern beruht und den Ansatz nicht gegen Timing-Angriffe abwägt, die bidirektionale Designs betreffen. Fortgesetzte Forschung und praktische Erfahrungen bestärken weiterhin, dass unidirektionale tunnels eine bewusste Anonymitätsentscheidung und kein Versehen sind.
