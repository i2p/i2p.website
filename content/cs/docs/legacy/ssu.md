---
title: "SSU (starší)"
description: "Původní zabezpečený polospolehlivý transport přes UDP"
slug: "ssu"
lastUpdated: "2025-01"
accurateFor: "0.9.64"
reviewStatus: "needs-review"
---

> **Zastaralé:** SSU bylo nahrazeno SSU2. Podpora byla odstraněna ve verzi i2pd 2.44.0 (API 0.9.56, listopad 2022) a ve verzi Java I2P 2.4.0 (API 0.9.61, prosinec 2023).

SSU poskytoval na UDP založené, částečně spolehlivé doručování s řízením přetížení, průchodem NATem a podporou introducerů (prostředníků pro navázání spojení). Doplňoval NTCP tím, že obsluhoval routers za NATem/firewally a koordinoval zjišťování IP adres.

## Prvky adresy

- `transport`: `SSU`
- `caps`: příznaky schopností (`B`, `C`, `4`, `6`, atd.)
- `host` / `port`: naslouchající pro IPv4 nebo IPv6 (volitelné, pokud je za firewallem)
- `key`: úvodní klíč v Base64
- `mtu`: Volitelné; výchozí 1484 (IPv4) / 1488 (IPv6)
- `ihost/ikey/iport/itag/iexp`: záznamy introduceru (prostředník pro navázání spojení), když je router za firewallem

## Funkce

- Kooperativní traverzování NAT pomocí introducers (zprostředkovatelů)
- Zjišťování lokální IP pomocí testů peerů a inspekce příchozích paketů
- Automatické předávání stavu firewallu ostatním transportům a konzoli routeru
- Polospolehlivé doručování: zprávy jsou znovu odesílány až do určitého limitu, poté jsou zahazovány
- Řízení zahlcení s aditivním zvyšováním / multiplikativním snižováním a bitovými poli ACK fragmentů

SSU také zajišťoval metadatové úlohy, jako jsou časovací majáky a vyjednávání MTU. Veškerá funkcionalita je nyní poskytována (s moderní kryptografií) protokolem [SSU2](/docs/specs/ssu2/).
