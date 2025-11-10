---
title: "Der I2P-Vorschlagsprozess"
number: "001"
author: "str4d"
created: "2016-04-10"
lastupdated: "2017-04-07"
status: "Meta"
thread: "http://zzz.i2p/topics/1980"
---

## Übersicht

Dieses Dokument beschreibt, wie die I2P-Spezifikationen geändert werden, wie I2P-Vorschläge funktionieren und die Beziehung zwischen I2P-Vorschlägen und den Spezifikationen.

Dieses Dokument ist vom Tor-Vorschlagsprozess adaptiert, und ein Großteil des untenstehenden Inhalts wurde ursprünglich von Nick Mathewson verfasst.

Dies ist ein informatives Dokument.

## Motivation

Bisher war unser Prozess zur Aktualisierung der I2P-Spezifikationen relativ informell: Wir machten einen Vorschlag im Entwicklungsforum und diskutierten die Änderungen, dann erreichten wir Konsens und änderten die Spezifikation mit Entwurfsänderungen (nicht unbedingt in dieser Reihenfolge), und schließlich implementierten wir die Änderungen.

Dies hatte einige Probleme.

Erstens war in der effizientesten Form des alten Prozesses die Spezifikation oft nicht synchron mit dem Code. Die schlimmsten Fälle waren solche, bei denen die Implementierung aufgeschoben wurde: Die Spezifikation und der Code konnten über Versionen hinweg asynchron bleiben.

Zweitens war es schwer, an Diskussionen teilzunehmen, da es nicht immer klar war, welche Teile des Diskussionsthreads Teil des Vorschlags waren oder welche Änderungen an der Spezifikation umgesetzt wurden. Die Entwicklungsforen sind auch nur innerhalb von I2P zugänglich, was bedeutet, dass Vorschläge nur von Personen eingesehen werden konnten, die I2P verwenden.

Drittens war es sehr einfach, einige Vorschläge zu vergessen, da sie mehrere Seiten zurück in der Foren-Thread-Liste vergraben wurden.

## Wie man jetzt die Spezifikationen ändert

Zuerst schreibt jemand ein Vorschlagsdokument. Es sollte die Änderung, die gemacht werden soll, im Detail beschreiben und eine Vorstellung davon geben, wie sie umgesetzt werden kann. Sobald es genügend ausgearbeitet ist, wird es zu einem Vorschlag.

Wie ein RFC bekommt jeder Vorschlag eine Nummer. Anders als bei RFCs können sich Vorschläge im Laufe der Zeit ändern und die gleiche Nummer behalten, bis sie schließlich akzeptiert oder abgelehnt werden. Die Historie für jeden Vorschlag wird im I2P-Website-Repository gespeichert.

Sobald ein Vorschlag im Repository ist, sollten wir ihn im entsprechenden Thread diskutieren und verbessern, bis wir Konsens darüber erreicht haben, dass es eine gute Idee ist und dass er detailliert genug ist, um umgesetzt zu werden. Wenn dies geschieht, implementieren wir den Vorschlag und integrieren ihn in die Spezifikationen. So bleiben die Spezifikationen die kanonische Dokumentation für das I2P-Protokoll: Kein Vorschlag ist jemals die kanonische Dokumentation für ein implementiertes Feature.

(Dieser Prozess ist ziemlich ähnlich zum Python-Enhancement-Prozess, mit der Hauptausnahme, dass I2P-Vorschläge nach der Implementierung wieder in die Spezifikationen integriert werden, während PEPs *zur* neuen Spezifikation werden.)

### Kleine Änderungen

Es ist immer noch in Ordnung, kleine Änderungen direkt an der Spezifikation vorzunehmen, wenn der Code mehr oder weniger sofort geschrieben werden kann, oder kosmetische Änderungen, wenn keine Code-Änderung erforderlich ist. Dieses Dokument spiegelt die aktuelle *Absicht* der Entwickler wider, nicht ein dauerhaftes Versprechen, diesen Prozess in Zukunft immer zu verwenden: Wir behalten uns das Recht vor, wirklich begeistert zu sein und etwas in einer von Koffein- oder M&M-getriebenen nächtlichen Hacking-Session zu implementieren.

## Wie neue Vorschläge hinzugefügt werden

Um einen Vorschlag einzureichen, veröffentlichen Sie ihn im Entwicklungsforum oder erstellen Sie ein Ticket mit dem angehängten Vorschlag.

Sobald eine Idee vorgeschlagen wurde, ein ordnungsgemäß formatiertes (siehe unten) Entwurf existiert, und ein grober Konsens innerhalb der aktiven Entwickler-Community besteht, dass diese Idee einer Überlegung wert ist, werden die Vorschlags-Redakteure den Vorschlag offiziell hinzufügen.

Die aktuellen Vorschlags-Redakteure sind zzz und str4d.

## Was in einen Vorschlag gehört

Jeder Vorschlag sollte eine Kopfzeile mit diesen Feldern enthalten:

```
:author:
:created:
:thread:
:lastupdated:
:status:
```

- Das `author`-Feld sollte die Namen der Autoren dieses Vorschlags enthalten.
- Das `thread`-Feld sollte ein Link zu dem Entwicklungsforum-Thread sein, in dem dieser Vorschlag ursprünglich gepostet wurde, oder zu einem neuen Thread, der zur Diskussion dieses Vorschlags erstellt wurde.
- Das `lastupdated`-Feld sollte anfangs gleich dem `created`-Feld sein und aktualisiert werden, wann immer der Vorschlag geändert wird.

Diese Felder sollten bei Bedarf gesetzt werden:

```
:supercedes:
:supercededby:
:editor:
```

- Das `supercedes`-Feld ist eine kommagetrennte Liste aller Vorschläge, die dieser Vorschlag ersetzt. Diese Vorschläge sollten abgelehnt werden und ihr `supercededby`-Feld sollte auf die Nummer dieses Vorschlags gesetzt werden.
- Das `editor`-Feld sollte gesetzt werden, wenn bedeutende Änderungen an diesem Vorschlag vorgenommen werden, die den Inhalt nicht wesentlich ändern. Wenn der Inhalt wesentlich verändert wird, sollte entweder ein zusätzlicher `author` hinzugefügt oder ein neuer Vorschlag erstellt werden, der diesen ersetzt.

Diese Felder sind optional, aber empfohlen:

```
:target:
:implementedin:
```

- Das `target`-Feld sollte beschreiben, in welcher Version der Vorschlag voraussichtlich implementiert werden soll (wenn er Offen oder Akzeptiert ist).
- Das `implementedin`-Feld sollte beschreiben, in welcher Version der Vorschlag implementiert wurde (wenn er Fertig oder Geschlossen ist).

Der Hauptteil des Vorschlags sollte mit einem Übersicht-Abschnitt beginnen, der erklärt, worum es im Vorschlag geht, was er tut und in welchem Zustand er sich befindet.

Nach der Übersicht wird der Vorschlag freier strukturiert. Abhängig von seiner Länge und Komplexität kann der Vorschlag in passende Abschnitte unterteilt werden oder einem kurzen diskursiven Format folgen. Jeder Vorschlag sollte mindestens die folgende Information enthalten, bevor er Akzeptiert wird, obwohl die Information nicht in Abschnitten mit diesen Namen sein muss.

**Motivation**
: Welches Problem soll der Vorschlag lösen? Warum ist dieses Problem wichtig? Wenn mehrere Ansätze möglich sind, warum diesen wählen?

**Design**
: Eine Übersicht über die neuen oder modifizierten Features, wie die neuen oder modifizierten Features funktionieren, wie sie miteinander interagieren und wie sie mit dem Rest von I2P zusammenarbeiten. Dies ist der Hauptteil des Vorschlags. Einige Vorschläge beginnen nur mit einer Motivation und einem Design und warten mit einer Spezifikation, bis das Design ungefähr stimmt.

**Sicherheitsimplikationen**
: Welche Auswirkungen die vorgeschlagenen Änderungen auf die Anonymität haben könnten, wie gut diese Effekte verstanden sind usw.

**Spezifikation**
: Eine detaillierte Beschreibung dessen, was zu den I2P-Spezifikationen hinzugefügt werden muss, um den Vorschlag umzusetzen. Dies sollte in etwa so detailliert sein, wie die Spezifikationen letztendlich enthalten: Es sollte möglich sein, dass unabhängige Programmierer gegenseitig kompatible Implementierungen des Vorschlags auf der Basis seiner Spezifikationen schreiben.

**Kompatibilität**
: Werden Versionen von I2P, die dem Vorschlag folgen, mit Versionen kompatibel sein, die es nicht tun? Wenn ja, wie wird die Kompatibilität erreicht? Generell versuchen wir, die Kompatibilität nicht aufzugeben, wenn es irgendwie möglich ist; wir haben seit März 2008 keine "Flag-Tag"-Änderung mehr durchgeführt und wollen dies auch nicht wieder tun.

**Implementierung**
: Wenn es schwierig sein wird, den Vorschlag in I2Ps aktueller Architektur umzusetzen, kann das Dokument einige Diskussionen darüber enthalten, wie man es schaffen kann, dass es funktioniert. Tatsächliche Patches sollten auf öffentlichen Monotone-Branches gepostet oder auf Trac hochgeladen werden.

**Leistungs- und Skalierbarkeitshinweise**
: Wenn das Feature Auswirkungen auf die Leistung (in RAM, CPU, Bandbreite) oder Skalierbarkeit hat, sollte eine Analyse darüber erfolgen, wie signifikant dieser Effekt sein wird, damit wir wirklich teure Leistungsrückschritte vermeiden und keine Zeit auf unbedeutende Gewinne verschwenden.

**Referenzen**
: Wenn der Vorschlag auf externe Dokumente verweist, sollten diese aufgelistet werden.

## Vorschlagsstatus

**Offen**
: Ein Vorschlag in Diskussion.

**Akzeptiert**
: Der Vorschlag ist abgeschlossen, und wir beabsichtigen, ihn umzusetzen. Ab diesem Punkt sollten wesentliche Änderungen am Vorschlag vermieden und als Zeichen dafür gesehen werden, dass der Prozess irgendwo fehlgeschlagen ist.

**Fertig**
: Der Vorschlag wurde akzeptiert und umgesetzt. Ab diesem Punkt sollte der Vorschlag nicht mehr geändert werden.

**Geschlossen**
: Der Vorschlag wurde akzeptiert, umgesetzt und in die Hauptspezifikationsdokumente integriert. Der Vorschlag sollte ab diesem Punkt nicht mehr geändert werden.

**Abgelehnt**
: Wir werden das Feature nicht wie hier beschrieben umsetzen, obwohl wir vielleicht eine andere Version machen. Siehe Kommentare im Dokument für Details. Der Vorschlag sollte ab diesem Punkt nicht mehr geändert werden; um eine andere Version der Idee vorzubringen, schreiben Sie einen neuen Vorschlag.

**Entwurf**
: Dies ist noch kein vollständiger Vorschlag; es gibt deutliche fehlende Teile. Bitte fügen Sie keine neuen Vorschläge mit diesem Status hinzu; legen Sie sie stattdessen im "ideas"-Unterverzeichnis ab.

**Überarbeitungsbedürftig**
: Die Idee für den Vorschlag ist gut, aber der Vorschlag hat schwerwiegende Probleme, die ihn daran hindern, akzeptiert zu werden. Siehe Kommentare im Dokument für Details.

**Verstorben**
: Der Vorschlag wurde lange nicht mehr angerührt, und es sieht nicht so aus, als würde jemand ihn bald fertigstellen. Er kann wieder "Offen" werden, wenn er einen neuen Befürworter bekommt.

**Forschungsbedarf**
: Es gibt Forschungsprobleme, die gelöst werden müssen, bevor klar ist, ob der Vorschlag eine gute Idee ist.

**Meta**
: Dies ist kein Vorschlag, sondern ein Dokument über Vorschläge.

**Reserviert**
: Dieser Vorschlag ist etwas, das wir derzeit nicht umsetzen planen, aber wir könnten ihn eines Tages wiederbeleben wollen, wenn wir uns entscheiden, etwas Ähnliches wie das darin Vorgeschlagene zu tun.

**Informativ**
: Dieser Vorschlag ist das letzte Wort dazu, was er tut. Er wird nicht in eine Spezifikation umgewandelt, es sei denn, jemand kopiert und fügt ihn in eine neue Spezifikation für ein neues Subsystem ein.

Die Redakteure pflegen den korrekten Status der Vorschläge, basierend auf grobem Konsens und ihrem eigenen Ermessen.

## Vorschlagsnummerierung

Nummern 000-099 sind für spezielle und Meta-Vorschläge reserviert. Ab 100 werden tatsächliche Vorschläge verwendet. Nummern werden nicht recycelt.

## Referenzen

- [Tor Proposal Process](https://gitweb.torproject.org/torspec.git/tree/proposals/001-process.txt)
