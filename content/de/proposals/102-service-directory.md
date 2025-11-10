---
title: "Dienstverzeichnis"
number: "102"
author: "zzz"
created: "2009-01-01"
lastupdated: "2009-01-06"
status: "Abgelehnt"
thread: "http://zzz.i2p/topics/180"
supercededby: "122"
---

## Übersicht

Dieser Vorschlag ist für ein Protokoll, das Apps verwenden könnten, um Dienste
in einem Verzeichnis zu registrieren und nachzuschlagen.


## Motivation

Der einfachste Weg, onioncat zu unterstützen, ist ein Dienstverzeichnis.

Dies ist ähnlich einem Vorschlag, den Sponge vor einiger Zeit im IRC hatte. Ich denke nicht, dass er ihn ausgearbeitet hat, aber seine Idee war, es im netDb zu platzieren. Ich bin kein Befürworter davon, aber die Diskussion über die beste Methode, auf das Verzeichnis zuzugreifen (netDb-Nachschläge, DNS-over-i2p, HTTP, hosts.txt, etc.), werde ich auf einen anderen Tag verschieben.

Ich könnte dies wahrscheinlich ziemlich schnell mit HTTP und der Sammlung von
Perl-Skripten, die ich für das Hinzufügen von Schlüsselformularen verwende, umsetzen.


## Spezifikation

So würde eine App mit dem Verzeichnis interagieren:

REGISTRIEREN
  - DestKey
  - Liste von Protokoll/Dienst-Paaren:

    - Protokoll (optional, Standard: HTTP)
    - Dienst (optional, Standard: Website)
    - ID (optional, Standard: keine)

  - Hostname (optional)
  - Ablauf (Standard: 1 Tag? 0 für Löschen)
  - Sig (mit privatem Schlüssel für Ziel)

  Rückgabe: Erfolg oder Misserfolg

  Updates erlaubt

NACHSCHLAGEN
  - Hash oder Schlüssel (optional). EINS von:

    - 80-Bit-Teilmengen-Hash
    - 256-Bit-Vollhash
    - voller Destkey

  - Protokoll/Dienst-Paar (optional)

  Rückgabe: Erfolg, Misserfolg oder (für 80-Bit) Kollision.
  Bei Erfolg, Rückgabe des oben signierten Deskriptors.
