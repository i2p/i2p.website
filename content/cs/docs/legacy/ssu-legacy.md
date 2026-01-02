---
title: "SSU transport (zastaralý)"
description: "Původní transport přes UDP používaný před SSU2"
slug: "ssu"
lastUpdated: "2024-01"
accurateFor: "0.9.61"
type: docs
reviewStatus: "needs-review"
---

> **Zastaralé:** SSU (Secure Semi-Reliable UDP, zabezpečený částečně spolehlivý UDP) byl nahrazen [SSU2](/docs/specs/ssu2/). Java I2P odstranil SSU ve verzi 2.4.0 (API 0.9.61) a i2pd jej odstranil ve verzi 2.44.0 (API 0.9.56). Tento dokument je ponechán pouze pro historické účely.

## Hlavní body

- UDP transport poskytující šifrované, autentizované doručování zpráv I2NP v režimu bod‑bod.
- Spoléhal na 2048bitový Diffie–Hellmanův handshake (stejné prvočíslo jako u ElGamalu).
- Každý datagram nesl 16bajtový HMAC-MD5 (nestandardní zkrácená varianta) + 16bajtový IV, po nichž následovala užitečná data šifrovaná pomocí AES-256-CBC.
- Ochrana proti opakování (replay) a stav relace byly sledovány v rámci šifrovaných užitečných dat.

## Hlavička zprávy

```
[16-byte MAC][16-byte IV][encrypted payload]
```
Použitý výpočet MAC: `HMAC-MD5(ciphertext || IV || (len ^ version ^ ((netid-2)<<8)))` s 32bajtovým MAC klíčem. Délka užitečných dat byla 16bitová v pořadí bajtů big-endian a byla připojena do vstupu pro výpočet MAC. Verze protokolu měla výchozí hodnotu `0`; netId mělo výchozí hodnotu `2` (hlavní síť).

## Relační klíče a klíče MAC (kód autentizace zprávy)

Odvozeno ze sdíleného tajemství DH (Diffie-Hellman):

1. Převeďte sdílenou hodnotu na bajtové pole ve formátu big-endian (přidejte `0x00` na začátek, pokud je nastaven nejvyšší bit).
2. Klíč relace: prvních 32 bajtů (doplňte nulami, je-li kratší).
3. Klíč MAC: bajty 33–64; pokud jich není dost, použijte místo toho hash SHA-256 sdílené hodnoty.

## Stav

Routers již neoznamují SSU adresy. Klienti by měli přejít na transporty SSU2 nebo NTCP2. Historické implementace lze najít ve starších vydáních:

- Zdrojové kódy v jazyce Java starší než 2.4.0 v adresáři `router/transport/udp`
- Zdrojové kódy i2pd starší než 2.44.0

Aktuální chování UDP transportu naleznete v [specifikaci SSU2](/docs/specs/ssu2/).
