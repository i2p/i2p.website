---
title: "PT Transport"
number: "109"
author: "zzz"
created: "2014-01-09"
lastupdated: "2014-09-28"
status: "Offen"
thread: "http://zzz.i2p/topics/1551"
---

## Überblick

Dieser Vorschlag zielt darauf ab, einen I2P-Transport zu erstellen, der sich über Pluggable Transports mit anderen Routern verbindet.


## Motivation

Pluggable Transports (PTs) wurden von Tor als eine Möglichkeit entwickelt, um Verschleierungstransporte auf Tor-Bridges modular hinzuzufügen.

I2P verfügt bereits über ein modulares Transportsystem, das die Hürde zur Hinzufügung alternativer Transporte senkt. Die Unterstützung von PTs würde I2P eine einfache Möglichkeit bieten, mit alternativen Protokollen zu experimentieren und sich für Blockierungsresistenz bereit zu machen.


## Design

Es gibt einige potenzielle Umsetzungsebenen:

1. Ein generisches PT, das SOCKS und ExtORPort implementiert sowie die Ein- und Ausprozesse konfiguriert und forkt und sich beim Kommunikationssystem registriert. Diese Ebene kennt nichts über NTCP und könnte NTCP verwenden oder auch nicht. Geeignet für Tests.

2. Aufbauend auf 1), ein generisches NTCP PT, das auf den NTCP-Code aufbaut und NTCP an 1) weiterleitet.

3. Aufbauend auf 2), ein spezifisches NTCP-xxxx PT, das so konfiguriert ist, dass ein gegebener externer Ein- und Ausprozess ausgeführt wird.
