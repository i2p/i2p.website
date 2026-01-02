---
title: "OBEPs mit IBGWs abgleichen"
number: "138"
author: "str4d"
created: "2017-04-10"
lastupdated: "2017-04-10"
status: "Offen"
thread: "http://zzz.i2p/topics/2294"
toc: true
---

## Übersicht

Dieser Vorschlag fügt eine I2CP-Option für ausgehende Tunnel hinzu, die bewirkt, dass Tunnel ausgewählt oder aufgebaut werden, wenn eine Nachricht gesendet wird, sodass der OBEP mit einem der IBGWs aus dem LeaseSet für das Ziel-Destination übereinstimmt.


## Motivation

Die meisten I2P-Router verwenden eine Form der Paketabwurfsteuerung zur Überlastungsverwaltung. Die Referenzimplementierung nutzt eine WRED-Strategie, die sowohl die Nachrichtengröße als auch die Reisedistanz berücksichtigt (siehe [Tunnel Throttling Dokumentation](/docs/specs/implementation/#tunnelthrottling)). Aufgrund dieser Strategie ist die Hauptquelle für Paketverlust der OBEP.


## Design

Beim Senden einer Nachricht wählt oder baut der Sender einen Tunnel mit einem OBEP, der derselbe Router wie einer der IBGWs des Empfängers ist. Dadurch wird die Nachricht direkt aus einem Tunnel in den anderen gesendet, ohne dass sie zwischendurch über das Netzwerk verschickt werden muss.


## Sicherheitsimplikationen

Dieser Modus würde effektiv bedeuten, dass der Empfänger den OBEP des Senders auswählt. Um die aktuelle Privatsphäre zu wahren, würden durch diesen Modus ausgehende Tunnel um einen Hop länger gebaut als durch die Option outbound.length I2CP angegeben (wobei der letzte Hop möglicherweise außerhalb der schnellen Stufe des Senders liegt).


## Spezifikation

Eine neue I2CP-Option wird zur [I2CP-Spezifikation](/docs/specs/i2cp/) hinzugefügt:

    outbound.matchEndWithTarget
        Boolean

        Standardwert: fallspezifisch

        Wenn true, wählt der Router ausgehende Tunnel für während dieser Sitzung gesendete Nachrichten so aus, dass der OBEP des Tunnels einer der IBGWs für das Ziel-Destination ist. Wenn ein solcher Tunnel nicht existiert, wird der Router einen bauen.


## Kompatibilität

Die Abwärtskompatibilität ist sichergestellt, da Router immer Nachrichten an sich selbst senden können.


## Implementierung

### Java I2P

Tunnelaufbau und Nachrichtensendung sind derzeit separate Subsysteme:

- BuildExecutor kennt nur die outbound.*-Optionen des ausgehenden Tunnelpools und hat keine Kenntnis über deren Verwendung.

- OutboundClientMessageOneShotJob kann nur einen Tunnel aus dem bestehenden Pool auswählen; wenn eine Clientnachricht eingeht und es keine ausgehenden Tunnel gibt, verwirft der Router die Nachricht.

Die Implementierung dieses Vorschlags würde erfordern, dass diese beiden Subsysteme miteinander interagieren können.

### i2pd

Eine Testimplementierung wurde abgeschlossen.


## Leistung

Dieser Vorschlag hat verschiedene Auswirkungen auf Latenz, RTT und Paketverlust:

- Es ist wahrscheinlich, dass in den meisten Fällen dieser Modus erfordert, beim ersten Nachrichtensenden einen neuen Tunnel zu bauen, anstatt einen bestehenden Tunnel zu nutzen, was die Latenz erhöht.

- Bei Standardtunneln muss der OBEP möglicherweise den IBGW finden und sich mit ihm verbinden, was die Latenz erhöht, die den ersten RTT verlängert (da dies nach dem Senden des ersten Pakets erfolgt). Bei Verwendung dieses Modus muss der OBEP während des Tunnelbaus den IBGW finden und sich mit ihm verbinden, was dieselbe Latenz hinzufügt, aber den ersten RTT verkürzt (da dies vor dem Senden des ersten Pakets erfolgt).

- Die derzeitige Standardgröße von VariableTunnelBuild ist 2641 Bytes. Daher wird erwartet, dass dieser Modus zu einem geringeren Paketverlust bei durchschnittlichen Nachrichtengrößen führt, die größer als diese sind.

Weitere Forschung ist notwendig, um diese Effekte zu untersuchen, um zu entscheiden, bei welchen Standardtunneln dieser Modus standardmäßig aktiviert werden sollte.
