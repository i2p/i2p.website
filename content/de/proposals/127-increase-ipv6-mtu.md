---
title: "Erhöhung der IPv6 MTU"
number: "127"
author: "zzz"
created: "2016-08-23"
lastupdated: "2016-12-02"
status: "Geschlossen"
thread: "http://zzz.i2p/topics/2181"
target: "0.9.28"
implementedin: "0.9.28"
---

## Übersicht

Dieser Vorschlag zielt darauf ab, die maximale SSU IPv6 MTU von 1472 auf 1488 zu erhöhen. Implementiert in 0.9.28.

## Motivation

Die IPv4-MTU muss ein Vielfaches von 16 + 12 sein. Die IPv6-MTU muss ein Vielfaches von 16 sein.

Als die IPv6-Unterstützung vor einigen Jahren erstmals hinzugefügt wurde, setzten wir die maximale IPv6-MTU auf 1472, weniger als die IPv4-MTU von 1484. Dies wurde getan, um die Dinge einfach zu halten und sicherzustellen, dass die IPv6-MTU weniger als die bestehende IPv4-MTU ist. Da die IPv6-Unterstützung nun stabil ist, sollten wir in der Lage sein, die IPv6-MTU höher als die IPv4-MTU einzustellen.

Die typische Schnittstellen-MTU beträgt 1500, daher können wir die IPv6-MTU sinnvoll um 16 auf 1488 erhöhen.

## Design

Ändern Sie das Maximum von 1472 auf 1488.

## Spezifikation

Ändern Sie in den Abschnitten "Router Address" und "MTU" der SSU-Übersicht die maximale IPv6 MTU von 1472 auf 1488.

## Migration

Wir erwarten, dass Router die Verbindungs-MTU wie gewohnt als Minimum der lokalen und der entfernten MTU festlegen. Es sollte keine Versionsprüfung erforderlich sein.

Wenn wir feststellen, dass eine Versionsprüfung erforderlich ist, werden wir ein Mindestversionslevel von 0.9.28 für diese Änderung festlegen.
