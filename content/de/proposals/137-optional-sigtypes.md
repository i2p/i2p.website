---
title: "Floodfill-Unterstützung für optionale Signaturtypen"
number: "137"
author: "zzz"
created: "2017-03-31"
lastupdated: "2017-11-12"
status: "Open"
thread: "http://zzz.i2p/topics/2280"
toc: true
---

## Übersicht

Eine Möglichkeit hinzufügen, dass Floodfills die Unterstützung für optionale Signaturtypen anzeigen.
Dies bietet eine Möglichkeit, neue Signaturtypen langfristig zu unterstützen,
auch wenn nicht alle Implementierungen sie unterstützen.


## Motivation

Der GOST Vorschlag 134 hat mehrere Probleme mit dem bisher ungenutzten experimentellen Signaturtyp-Bereich aufgedeckt.

Erstens, da Signaturtypen im experimentellen Bereich nicht reserviert werden können, könnten sie für
mehrere Signaturtypen gleichzeitig verwendet werden.

Zweitens, sofern ein Routerinfo oder ein Lease-Set mit einem experimentellen Signaturtyp nicht bei einem Floodfill gespeichert werden kann,
ist es schwierig, den neuen Signaturtyp umfassend zu testen oder probeweise zu nutzen.

Drittens, wenn Vorschlag 136 umgesetzt wird, ist dies nicht sicher, da jeder einen Eintrag überschreiben kann.

Viertens kann die Implementierung eines neuen Signaturtyps einen großen Entwicklungsaufwand erfordern.
Es könnte schwierig sein, Entwickler aller Router-Implementationen davon zu überzeugen, Unterstützung für einen neuen
Signaturtyp rechtzeitig für eine bestimmte Veröffentlichung hinzuzufügen. Die Zeit und Motivation von Entwicklern kann variieren.

Fünftens, wenn GOST einen Signaturtyp im Standardbereich verwendet, gibt es immer noch keine Möglichkeit zu wissen, ob ein bestimmtes
Floodfill GOST unterstützt.


## Design

Alle Floodfills müssen die Signaturtypen DSA (0), ECDSA (1-3) und EdDSA (7) unterstützen.

Für alle anderen Signaturtypen im Standard- (nicht experimentellen) Bereich kann ein Floodfill
die Unterstützung in seinen Routerinfo-Eigenschaften anzeigen.


## Spezifikation


Ein Router, der einen optionalen Signaturtyp unterstützt, soll die Eigenschaft "sigTypes"
zu seinen veröffentlichten Routerinfos hinzufügen, mit kommagetrennten Signaturtyp-Nummern.
Die Signaturtypen werden in aufsteigender numerischer Reihenfolge dargestellt.
Verpflichtende Signaturtypen (0-4,7) sollen nicht enthalten sein.

Zum Beispiel: sigTypes=9,10

Router, die optionale Signaturtypen unterstützen, dürfen nur speichern, nachschlagen oder flooden,
zu Floodfills, die die Unterstützung für diesen Signaturtyp anzeigen.


## Migration

Nicht anwendbar.
Nur Router, die einen optionalen Signaturtyp unterstützen, müssen implementieren.


## Probleme

Wenn es nicht viele Floodfills gibt, die den Signaturtyp unterstützen, könnten sie schwer zu finden sein.

Es könnte nicht notwendig sein, ECDSA 384 und 521 (Signaturtypen 2 und 3) für alle Floodfills zu verlangen.
Diese Typen sind nicht weit verbreitet.

Ähnliche Probleme müssen mit Verschlüsselungstypen ungleich null behandelt werden,
was noch nicht formell vorgeschlagen wurde.


## Anmerkungen

NetDB-Speicherungen von unbekannten Signaturtypen, die nicht im experimentellen Bereich liegen, werden weiterhin
von Floodfills abgelehnt, da die Signatur nicht verifiziert werden kann.


