---
title: "ECIES-P256"
number: "145"
author: "orignal"
created: "2019-01-23"
lastupdated: "2019-01-24"
status: "Open"
thread: "http://zzz.i2p/topics/2418"
---

## Motivation

ECIES-P256 ist viel schneller als ElGamal. Es gibt bereits wenige i2pd Eepsites mit dem Kryptotyp ECIES-P256, und Java sollte in der Lage sein, mit ihnen zu kommunizieren und umgekehrt. i2pd unterstützt es seit der Version 2.16.0 (0.9.32 Java).

## Überblick

Dieser Vorschlag führt den neuen Kryptotyp ECIES-P256 ein, der im Zertifikateteil der Identität oder als separater Verschlüsselungsschlüsseltyp in LeaseSet2 erscheinen kann. Kann in RouterInfo, LeaseSet1 und LeaseSet2 verwendet werden.


### ElGamal-Schlüssellokationen

Zur Überprüfung:
ElGamal 256-Byte öffentliche Schlüssel können in den folgenden Datenstrukturen gefunden werden.
Verweisen Sie auf die Spezifikation der allgemeinen Strukturen.

- In einer Router-Identität
  Dies ist der Verschlüsselungsschlüssel des Routers.

- In einem Ziel
  Der öffentliche Schlüssel des Ziels wurde für die alte i2cp-to-i2cp-Verschlüsselung verwendet,
  die in Version 0.6 deaktiviert wurde und derzeit außer für
  den IV für die LeaseSet-Verschlüsselung, die veraltet ist, nicht verwendet wird.
  Der öffentliche Schlüssel im LeaseSet wird stattdessen verwendet.

- In einem LeaseSet
  Dies ist der Verschlüsselungsschlüssel des Ziels.

In 3 oben nimmt der ECIES öffentliche Schlüssel immer noch 256 Bytes ein, obwohl die tatsächliche Schlüssellänge 64 Bytes beträgt.
Der Rest muss mit zufälligem Padding gefüllt werden.

- In einem LS2
  Dies ist der Verschlüsselungsschlüssel des Ziels. Die Schlüssellänge beträgt 64 Bytes.


### EncTypes in Schlüsselzertifikaten

ECIES-P256 verwendet den Verschlüsselungstyp 1.
Die Verschlüsselungstypen 2 und 3 sollten für ECIES-P284 und ECIES-P521 reserviert werden.


### Verwendung asymmetrischer Kryptografie

Dieser Vorschlag beschreibt den Ersatz von ElGamal für:

1) Nachrichten zum Tunnelaufbau (Schlüssel ist in RouterIdentity). Der ElGamal-Block ist 512 Bytes groß.
  
2) Client-Ende-zu-Ende ElGamal+AES/SessionTag (Schlüssel ist in LeaseSet, der Zielspeicherschlüssel wird nicht verwendet). Der ElGamal-Block ist 514 Bytes groß.

3) Router-zu-Router-Verschlüsselung von netdb und anderen I2NP Nachrichten. Der ElGamal-Block ist 514 Bytes groß.


### Ziele

- Rückwärtskompatibel
- Keine Änderungen an bestehenden Datenstrukturen
- Viel CPU-effizienter als ElGamal

### Nicht-Ziele

- RouterInfo und LeaseSet1 können nicht ElGamal und ECIES-P256 zusammen veröffentlichen

### Rechtfertigung

Der ElGamal/AES+SessionTag-Motor bleibt immer bei fehlenden Tags hängen, was zu einer dramatischen Leistungsverschlechterung in I2P-Kommunikationen führt.
Der Tunnelaufbau ist die schwerwiegendste Operation, da der Urheber ElGamal-Verschlüsselungen dreimal pro Tunnelaufbauanfrage ausführen muss.


## Erforderliche kryptografische Primitive

1) EC P256 Kurvengenerierung und DH

2) AES-CBC-256

3) SHA256


## Detaillierter Vorschlag

Ein Ziel mit ECIES-P256 veröffentlicht sich mit dem Kryptotyp 1 im Zertifikat.
Die ersten 64 Bytes von 256 in der Identität sollten als ECIES-öffentlicher Schlüssel interpretiert werden und der Rest muss ignoriert werden.
Der separate Verschlüsselungsschlüssel des LeaseSets basiert auf dem Schlüsseltyp der Identität.

### ECIES-Block für ElGamal/AES+SessionTags
Der ECIES-Block ersetzt den ElGamal-Block für ElGamal/AES+SessionTags. Die Länge beträgt 514 Bytes.
Besteht aus zwei Teilen mit jeweils 257 Bytes. 
Der erste Teil beginnt mit Null und dann dem 64 Byte langen ephemeren öffentlichen P256-Schlüssel, der Rest von 192 Bytes ist zufälliges Padding.
Der zweite Teil beginnt mit Null und dann mit AES-CBC-256 verschlüsselten 256 Bytes mit demselben Inhalt wie beim ElGamal.

### ECIES-Block für Tunnelaufzeichnungsaufzeichnungen
Die Tunnelaufzeichnungsaufzeichnung ist dieselbe, jedoch ohne führende Nullen in den Blöcken.
Ein Tunnel kann durch jede Kombination von Kryptotypen der Router gehen und wird pro Aufzeichnung durchgeführt.
Der Urheber des Tunnels verschlüsselt die Aufzeichnungen je nach veröffentlichtem Kryptotyp des Tunnelteilnehmers, der Tunnelteilnehmer entschlüsselt basierend auf seinem eigenen Kryptotyp.


### AES-CBC-256 Schlüssel
Dies ist die Berechnung der gemeinsam genutzten ECDH-Schlüssel, wobei KDF über die x-Koordinate SHA256 ist.
Betrachten wir Alice als Verschlüsselerin und Bob als Entschlüsseler.
Angenommen, k ist Alices zufällig gewählter ephemerer P256-Privatschlüssel und P ist Bobs öffentlicher Schlüssel.
S ist das gemeinsame Geheimnis S(Sx, Sy)
Alice berechnet S durch "Vereinbarung" von k mit P, z.B. S = k*P.

Angenommen, K ist Alices ephemerer öffentlicher Schlüssel und p ist Bobs privater Schlüssel.
Bob nimmt K aus dem ersten Block der empfangenen Nachricht und berechnet S = p*K

Der AES-Verschlüsselungsschlüssel ist SHA256(Sx) und der IV ist Sy.
