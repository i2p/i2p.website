---
title: "Bevorzugung von nahen Routern im Keyspace"
number: "116"
author: "chisquare"
created: "2015-04-25"
lastupdated: "2015-04-25"
status: "Forschungsbedarf"
thread: "http://zzz.i2p/topics/1874"
---

## Übersicht

Dies ist ein Vorschlag, Peers so zu organisieren, dass sie bevorzugt eine Verbindung zu anderen Peers herstellen, die ihnen im Keyspace nahe sind.


## Motivation

Die Idee ist, den Erfolg beim Erstellen von Tunneln zu verbessern, indem die Wahrscheinlichkeit erhöht wird, dass ein Router bereits mit einem anderen verbunden ist.


## Design

### Erforderliche Änderungen

Diese Änderung würde erfordern:

1. Jeder Router bevorzugt Verbindungen, die ihnen im Keyspace nahe sind.
2. Jeder Router weiß, dass jeder Router Verbindungen bevorzugt, die ihnen im
   Keyspace nahe sind.


### Vorteile für den Tunnelaufbau

Wenn Sie einen Tunnel bauen::

    A -lang-> B -kurz-> C -kurz-> D

(lang/zufällig vs. kurzer Sprung im Keyspace), können Sie erraten, wo der Tunnelbau wahrscheinlich fehlgeschlagen ist, und an diesem Punkt einen anderen Peer versuchen. Darüber hinaus würde es Ihnen ermöglichen, dichtere Teile im Keyspace zu erkennen und Router dazu zu bringen, diese nicht zu nutzen, da es sich um jemanden handeln könnte, der kolludiert.

Wenn Sie einen Tunnel bauen::

    A -lang-> B -lang-> C -kurz-> D

und er fehlschlägt, können Sie daraus schließen, dass es eher bei C -> D fehlschlug, und Sie können einen anderen D-Sprung wählen.

Sie können auch Tunnel so bauen, dass der OBEP näher am IBGW ist, und diese Tunnel mit OBEP verwenden, die näher am gegebenen IBGW in einem LeaseSet sind.


## Sicherheitsimplikationen

Wenn Sie die Platzierung von kurzen vs. langen Sprüngen im Keyspace randomisieren, wird ein Angreifer wahrscheinlich keinen großen Vorteil daraus ziehen.

Der größte Nachteil ist jedoch, dass dies die Benutzerauszählung etwas erleichtern könnte.
