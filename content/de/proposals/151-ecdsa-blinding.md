---
title: "ECDSA Schlüssel Blinden"
number: "151"
author: "orignal"
created: "2019-05-21"
lastupdated: "2019-05-29"
status: "Offen"
thread: "http://zzz.i2p/topics/2717"
toc: true
---

## Motivation

Einige Leute mögen EdDSA oder RedDSA nicht. Wir sollten einige Alternativen anbieten und ihnen ermöglichen, ECDSA-Signaturen zu blenden.

## Überblick

Dieser Vorschlag beschreibt das Schlüsselblinden für ECDSA-Signaturtypen 1, 2, 3.

## Vorschlag

Funktioniert genauso wie RedDSA, aber alles ist in Big Endian.
Es sind nur gleiche Signaturtypen erlaubt, z.B. 1->1, 2->2, 3->3.

### Definitionen

B
    Basispunkt der Kurve 

L
   Gruppengröße der elliptischen Kurve. Eigenschaft der Kurve.

DERIVE_PUBLIC(a)
    Konvertiere einen privaten Schlüssel zu einem öffentlichen, indem B über eine elliptische Kurve multipliziert wird

alpha
    Eine 32-Byte lange Zufallszahl, die denjenigen bekannt ist, die das Ziel kennen.

GENERATE_ALPHA(destination, date, secret)
    Erzeuge alpha für das aktuelle Datum, für diejenigen, die das Ziel und das Geheimnis kennen.

a
    Der unverblindete 32-Byte lange Signatur-Privatschlüssel, der verwendet wird, um das Ziel zu signieren

A
    Der unverblindete 32-Byte lange Signatur-Öffentlichschlüssel im Ziel,
    = DERIVE_PUBLIC(a), wie in der entsprechenden Kurve

a'
    Der verblindete 32-Byte lange Signatur-Privatschlüssel, der verwendet wird, um das verschlüsselte Leaseset zu signieren
    Dies ist ein gültiger ECDSA-Privatschlüssel.

A'
    Der verblindete 32-Byte lange ECDSA-Signatur-Öffentlichschlüssel im Ziel,
    kann mit DERIVE_PUBLIC(a') erzeugt werden, oder von A und alpha.
    Dies ist ein gültiger ECDSA-Öffentlichschlüssel auf der Kurve

H(p, d)
    SHA-256 Hashfunktion, die einen Personalisierungsstring p und Daten d nimmt und
    eine Ausgabe von 32 Byte Länge erzeugt.

    Verwende SHA-256 wie folgt::

        H(p, d) := SHA-256(p || d)

HKDF(salt, ikm, info, n)
    Eine kryptographische Schlüsselableitungsfunktion, die ein Inputschlüsselmaterial ikm nimmt (das
    gute Entropie haben sollte, aber nicht erforderlich ist, um eine gleichmäßig zufällige Zeichenfolge zu sein), ein Salt
    von 32 Bytes Länge und einen kontextspezifischen 'info'-Wert und erzeugt eine Ausgabe
    von n Bytes, die als Schlüsselmateriel geeignet ist.

    Verwende HKDF wie in [RFC-5869](https://tools.ietf.org/html/rfc5869) angegeben, unter Verwendung der HMAC-Hashfunktion SHA-256
    wie in [RFC-2104](https://tools.ietf.org/html/rfc2104). Dies bedeutet, dass SALT_LEN maximal 32 Bytes beträgt.


### Verblindungsberechnungen

Ein neues geheimes Alpha und verblindete Schlüssel müssen jeden Tag (UTC) generiert werden.
Das geheime Alpha und die verblindeten Schlüssel werden wie folgt berechnet.

GENERATE_ALPHA(destination, date, secret), für alle Parteien:

```text
// GENERATE_ALPHA(destination, date, secret)

  // secret ist optional, sonst null-Länge
  A = Signing-Öffentlichschlüssel des Ziels
  stA = Signaturtyp von A, 2 Byte Big Endian (0x0001, 0x0002 oder 0x0003)
  stA' = Signaturtyp des verblindeten Öffentlichschlüssels A', 2 Byte Big Endian, immer gleich wie stA
  keydata = A || stA || stA'
  datestring = 8 Bytes ASCII YYYYMMDD vom aktuellen Datum UTC
  secret = UTF-8 kodierter String
  seed = HKDF(H("I2PGenerateAlpha", keydata), datestring || secret, "i2pblinding1", 64)
  // behandle seed als einen 64 Byte Big-Endian Wert
  alpha = seed mod L
```


BLIND_PRIVKEY(), für den Besitzer, der das Leaseset veröffentlicht:

```text
// BLIND_PRIVKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  a = Signing-Privatschlüssel des Ziels
  // Addition unter Verwendung von Skalararithmetik
  verblindeter Signing-Privatschlüssel = a' = BLIND_PRIVKEY(a, alpha) = (a + alpha) mod L
  verblindeter Signing-Öffentlichschlüssel = A' = DERIVE_PUBLIC(a')
```


BLIND_PUBKEY(), für die Klienten, die das Leaseset abrufen:

```text
// BLIND_PUBKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  A = Signing-Öffentlichschlüssel des Ziels
  // Addition unter Verwendung von Gruppenelementen (Punkte auf der Kurve)
  verblindeter Öffentlichkeitsschlüssel = A' = BLIND_PUBKEY(A, alpha) = A + DERIVE_PUBLIC(alpha)
```


Beide Berechnungsmethoden für A' liefern das gleiche Ergebnis, wie erforderlich.

## b33 Adresse

Der ECDSA-Öffentlichschlüssel ist ein (X,Y)-Paar, also beispielsweise bei P256 sind es 64 Bytes, anstatt wie bei RedDSA 32 Bytes.
Entweder wird die b33-Adresse länger, oder der Öffentlichkeitsschlüssel kann in komprimiertem Format wie in Bitcoin-Wallets gespeichert werden.


## Referenzen

* [RFC-2104](https://tools.ietf.org/html/rfc2104)
* [RFC-5869](https://tools.ietf.org/html/rfc5869)
