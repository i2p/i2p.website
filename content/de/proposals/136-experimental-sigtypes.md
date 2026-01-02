---
title: "Floodfill-Unterstützung für experimentelle Sig-Typen"
number: "136"
author: "zzz"
created: "2017-03-31"
lastupdated: "2017-11-12"
status: "Open"
thread: "http://zzz.i2p/topics/2279"
toc: true
---

## Übersicht

Für Sig-Typen im experimentellen Bereich (65280-65534) sollten Floodfills NetDB-Stores ohne Prüfung der Signatur akzeptieren.

Dies unterstützt das Testen neuer Sig-Typen.


## Motivation

Der GOST-Vorschlag 134 hat zwei Probleme mit dem bisher unbenutzten experimentellen Sig-Typ-Bereich aufgezeigt.

Erstens, da Sig-Typen im experimentellen Bereich nicht reserviert werden können, könnten sie gleichzeitig für mehrere Sig-Typen verwendet werden.

Zweitens, sofern ein Router-Info oder Lease-Set mit einem experimentellen Sig-Typ nicht in einem Floodfill gespeichert werden kann, ist der neue Sig-Typ schwer vollständig zu testen oder auf Probe zu verwenden.


## Design

Floodfills sollten LS-Stores mit Sig-Typen im experimentellen Bereich akzeptieren und verteilen, ohne die Signatur zu prüfen. Die Unterstützung für RI-Stores ist noch festzulegen und könnte mehr Sicherheitsimplikationen haben.


## Spezifikation


Für Sig-Typen im experimentellen Bereich sollte ein Floodfill NetDB-Stores akzeptieren und verteilen, ohne die Signatur zu prüfen.

Um das Spoofing von nicht-experimentellen Routern und Zielen zu verhindern, sollte ein Floodfill niemals einen Store eines experimentellen Sig-Typs akzeptieren, der eine Hash-Kollision mit einem bestehenden NetDB-Eintrag eines anderen Sig-Typs hat.
Dies verhindert das Kapern eines vorherigen NetDB-Eintrags.

Zusätzlich sollte ein Floodfill einen experimentellen NetDB-Eintrag mit einem Store eines nicht-experimentellen Sig-Typs überschreiben, der eine Hash-Kollision ist, um das Kapern eines zuvor nicht vorhandenen Hashs zu verhindern.

Floodfills sollten davon ausgehen, dass die Länge des signierenden öffentlichen Schlüssels 128 beträgt oder sie aus der Schlüsselfeldzertifikatslänge ableiten, falls diese länger ist. Einige Implementierungen unterstützen möglicherweise keine längeren Längen, es sei denn, der Sig-Typ ist informell reserviert.


## Migration

Sobald diese Funktion unterstützt wird, in einer bekannten Router-Version,
können experimentelle Sig-Typ-NetDB-Einträge zu Floodfills dieser Version oder höher gespeichert werden.

Falls einige Router-Implementierungen diese Funktion nicht unterstützen, wird der NetDB-Store fehlschlagen, aber das ist dasselbe wie jetzt.


## Probleme

Es könnten zusätzliche Sicherheitsimplikationen bestehen, die noch erforscht werden müssen (siehe Vorschlag 137).

Einige Implementierungen unterstützen möglicherweise keine Schlüssellängen über 128,
wie oben beschrieben. Zusätzlich könnte es notwendig sein, ein Maximum von 128 zu erzwingen
(mit anderen Worten, es gibt keine überschüssigen Schlüssel-Daten im Schlüsselzertifikat),
um die Fähigkeit der Angreifer, Hash-Kollisionen zu erzeugen, zu reduzieren.

Ähnliche Probleme müssen bei nicht-null Verschlüsselungstypen angesprochen werden,
die bisher noch nicht formell vorgeschlagen wurden.


## Anmerkungen

NetDB-Stores unbekannter Sig-Typen, die nicht im experimentellen Bereich liegen, werden weiterhin von Floodfills abgelehnt, da die Signatur nicht verifiziert werden kann.


