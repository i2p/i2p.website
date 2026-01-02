---
title: "v3dgsend"
description: "CLI nástroj pro odesílání I2P datagramů přes SAM v3"
slug: "v3dgsend"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

> Stav: Toto je stručná reference pro nástroj `v3dgsend`. Doplňuje dokumentaci k [Datagram API](/docs/api/datagrams/) a [SAM v3](/docs/api/samv3/).

## Přehled

`v3dgsend` je nástroj příkazového řádku pro odesílání I2P datagramů pomocí rozhraní SAMv3. Je užitečný pro testování doručování datagramů, prototypování služeb a ověřování chování mezi koncovými body bez nutnosti psát plnohodnotného klienta.

Typická použití zahrnují:

- Kouřový test dostupnosti datagramu k Destinaci
- Ověření konfigurace firewallu a adresáře
- Experimentování se surovými vs. podepsanými (odpověditelnými) datagramy

## Použití

Základní spuštění se liší podle platformy a balíčku. Mezi běžné možnosti patří:

- Destination: base64 Destination nebo `.i2p` název
- Protocol: raw (PROTOCOL 18) nebo signed (PROTOCOL 17)
- Payload: inline řetězec nebo vstup ze souboru

Přesné příznaky naleznete v dokumentaci vaší distribuce nebo ve výstupu `--help`.

## Viz také

- [Datagram API](/docs/api/datagrams/)
- [SAM v3](/docs/api/samv3/)
- [Streaming Library](/docs/api/streaming/) (alternativa k datagramům)
