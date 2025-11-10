---
title: "GOST Sig Typ"
number: "134"
author: "orignal"
created: "2017-02-18"
lastupdated: "2017-03-31"
status: "Offen"
thread: "http://zzz.i2p/topics/2239"
---

## Überblick

Elliptische Kurven-Signatur GOST R 34.10 wird von Behörden und Unternehmen in Russland verwendet.
Die Unterstützung könnte die Integration bestehender Apps (normalerweise CryptoPro-basiert) vereinfachen.
Die Hash-Funktion ist GOST R 34.11 mit 32 oder 64 Bytes.
Funktioniert im Wesentlichen auf die gleiche Weise wie EcDSA, die Signatur- und öffentliche Schlüsselgröße beträgt 64 oder 128 Bytes.

## Motivation

Der elliptischen Kurven-Kryptographie wurde niemals vollständig vertraut, was viele Spekulationen über mögliche Hintertüren erzeugt hat.
Daher gibt es keinen ultimativen Signaturtyp, dem alle vertrauen.
Das Hinzufügen eines weiteren Signaturtyps gibt den Menschen mehr Wahlmöglichkeiten, wem sie mehr vertrauen.

## Design

GOST R 34.10 verwendet eine Standard-Elliptische-Kurve mit eigenen Parametersätzen.
Die Mathematik der vorhandenen Gruppen kann wiederverwendet werden.
Allerdings sind das Signieren und die Verifizierung unterschiedlich und müssen implementiert werden.
Siehe RFC: https://www.rfc-editor.org/rfc/rfc7091.txt
GOST R 34.10 soll zusammen mit dem GOST R 34.11-Hash arbeiten.
Wir werden GOST R 34.10-2012 (auch bekannt als steebog) entweder 256 oder 512 Bits verwenden.
Siehe RFC: https://tools.ietf.org/html/rfc6986

GOST R 34.10 spezifiziert keine Parameter, jedoch gibt es einige gute Parametersätze, die von allen genutzt werden.
GOST R 34.10-2012 mit 64-Byte-öffentlichen Schlüsseln erbt die Parametersätze von CryptoPro aus GOST R 34.10-2001.
Siehe RFC: https://tools.ietf.org/html/rfc4357

Jedoch wurden neuere Parametersätze für 128-Byte-Schlüssel von einem speziellen technischen Komitee tc26 (tc26.ru) erstellt.
Siehe RFC: https://www.rfc-editor.org/rfc/rfc7836.txt

Die auf Openssl basierende Implementierung in i2pd zeigt, dass es schneller als P256 und langsamer als 25519 ist.

## Spezifikation

Nur GOST R 34.10-2012 und GOST R 34.11-2012 werden unterstützt.
Zwei neue Signaturtypen:
9 - GOSTR3410_GOSTR3411_256_CRYPTO_PRO_A steht für einen öffentlichen Schlüssel und Signaturtyp von 64 Bytes, eine Hash-Größe von 32 Bytes und den Parametersatz CryptoProA (auch bekannt als CryptoProXchA).
10 - GOSTR3410_GOSTR3411_512_TC26_A steht für einen öffentlichen Schlüssel- und Signaturtyp von 128 Bytes, eine Hash-Größe von 64 Bytes und den Parametersatz A von TC26.

## Migration

Diese Signaturtypen sollen nur als optionaler Signaturtyp verwendet werden.
Keine Migration erforderlich. i2pd unterstützt es bereits.
