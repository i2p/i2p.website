---
title: "SSU-Transport (veraltet)"
description: "Ursprünglicher UDP-Transport, der vor SSU2 verwendet wurde"
slug: "ssu"
lastUpdated: "2024-01"
accurateFor: "0.9.61"
type: docs
reviewStatus: "needs-review"
---

> **Veraltet:** SSU (Secure Semi-Reliable UDP) wurde durch [SSU2](/docs/specs/ssu2/) ersetzt. Java I2P hat SSU in Version 2.4.0 (API 0.9.61) entfernt und i2pd hat es in 2.44.0 (API 0.9.56) entfernt. Dieses Dokument dient ausschließlich der historischen Referenz.

## Höhepunkte

- UDP-Transport, der eine verschlüsselte, authentifizierte Punkt-zu-Punkt-Übermittlung von I2NP-Nachrichten bereitstellt.
- Basierte auf einem 2048-Bit-Diffie–Hellman-Handshake (gleiche Primzahl wie ElGamal).
- Jedes Datagramm enthielt einen 16-Byte-HMAC-MD5 (nicht standardisierte, gekürzte Variante) + einen 16-Byte-IV, gefolgt von einer AES-256-CBC-verschlüsselten Nutzlast.
- Replay-Schutz und Sitzungszustand wurden innerhalb der verschlüsselten Nutzlast verwaltet.

## Nachrichtenkopf

```
[16-byte MAC][16-byte IV][encrypted payload]
```
Verwendete MAC-Berechnung: `HMAC-MD5(ciphertext || IV || (len ^ version ^ ((netid-2)<<8)))` mit einem 32-Byte-MAC-Schlüssel. Die Nutzlastlänge wurde als 16-Bit-Wert in Big-Endian-Reihenfolge angehängt und in die MAC-Berechnung einbezogen. Die Protokollversion war standardmäßig `0`; netId war standardmäßig `2` (Hauptnetz).

## Sitzungs- und MAC-Schlüssel

Abgeleitet aus dem gemeinsamen DH-Geheimnis:

1. Konvertieren Sie den gemeinsamen Wert in ein Big-Endian-Byte-Array (fügen Sie `0x00` voran, falls das höchstwertige Bit gesetzt ist).
2. Sitzungsschlüssel: erste 32 Bytes (falls kürzer, mit Nullen auffüllen).
3. MAC-Schlüssel: Bytes 33–64; falls nicht ausreichend, auf den SHA-256-Hash des gemeinsamen Werts zurückgreifen.

## Status

Router veröffentlichen keine SSU-Adressen mehr. Clients sollten auf SSU2 oder NTCP2 umsteigen. Historische Implementierungen finden sich in älteren Releases:

- Java-Quellcode vor 2.4.0 unter `router/transport/udp`
- i2pd-Quellcode vor 2.44.0

Informationen zum aktuellen Verhalten des UDP-Transports finden Sie in der [SSU2-Spezifikation](/docs/specs/ssu2/).
