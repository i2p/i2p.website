---
title: "Verschlüsselter LeaseSet"
number: "121"
author: "zzz"
created: "2016-01-11"
lastupdated: "2016-01-12"
status: "Abgelehnt"
thread: "http://zzz.i2p/topics/2047"
supercededby: "123"
---

## Übersicht

Dieser Vorschlag bezieht sich auf die Neugestaltung des Mechanismus zur Verschlüsselung von LeaseSets.


## Motivation

Das derzeitige verschlüsselte LS ist schrecklich und unsicher. Ich kann das sagen, ich habe es entworfen und implementiert.

Gründe:

- AES CBC verschlüsselt
- Ein einzelner AES-Schlüssel für alle
- Lease-Ablaufdaten immer noch sichtbar
- Verschlüsselungs-Pubkey immer noch sichtbar


## Design

### Ziele

- Alles undurchsichtig machen
- Schlüssel für jeden Empfänger


### Strategie

Mach es wie GPG/OpenPGP. Asymmetrisch einen symmetrischen Schlüssel für jeden Empfänger verschlüsseln. Daten werden mit diesem asymmetrischen Schlüssel entschlüsselt. Siehe z.B. [RFC-4880-S5.1]_
WENN wir einen Algorithmus finden, der klein und schnell ist.

Der Trick besteht darin, eine asymmetrische Verschlüsselung zu finden, die klein und schnell ist. ElGamal mit 514 Bytes ist hier etwas schmerzhaft. Wir können es besser machen.

Siehe z.B. http://security.stackexchange.com/questions/824...

Dies funktioniert für kleine Anzahlen von Empfängern (oder eigentlich, Schlüssel; Sie können Schlüssel immer noch an mehrere Personen verteilen, wenn Sie möchten).


## Spezifikation

- Ziel
- Veröffentlichtes Zeitstempel
- Ablauf
- Flags
- Datenlänge
- Verschlüsselte Daten
- Signatur

Verschlüsselte Daten könnten mit einem Enctype-Spezifikator versehen werden, oder auch nicht.


## Referenzen

.. [RFC-4880-S5.1]
    https://tools.ietf.org/html/rfc4880#section-5.1
