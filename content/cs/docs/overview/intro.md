---
title: "Úvod do I2P"
description: "Méně technický úvod do anonymní sítě I2P"
slug: "intro"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "needs-review"
---

## Co je I2P?

Invisible Internet Project (I2P) je anonymní síťová vrstva, která umožňuje komunikaci peer-to-peer odolnou vůči cenzuře. Anonymní spojení je dosaženo šifrováním provozu uživatele a jeho odesíláním prostřednictvím distribuované sítě provozované dobrovolníky po celém světě.

## Klíčové vlastnosti

### Anonymity

I2P skrývá jak odesílatele, tak příjemce zpráv. Na rozdíl od tradičních internetových připojení, kde je vaše IP adresa viditelná pro webové stránky a služby, I2P používá několik vrstev šifrování a směrování k ochraně vašeho soukromí.

### Decentralization

V I2P neexistuje žádná centrální autorita. Síť je udržována dobrovolníky, kteří darují šířku pásma a výpočetní zdroje. Díky tomu je odolná vůči cenzuře a jednotlivým bodům selhání.

### Anonymita

Veškerý provoz v rámci I2P je šifrován end-to-end. Zprávy jsou šifrovány vícekrát při průchodu sítí, podobně jako funguje Tor, ale s důležitými rozdíly v implementaci.

## How It Works

### Decentralizace

I2P používá „tunnely" k směrování provozu. Když odesíláte nebo přijímáte data:

1. Váš router vytvoří odchozí tunnel (pro odesílání)
2. Váš router vytvoří příchozí tunnel (pro příjem)
3. Zprávy jsou šifrovány a odesílány přes více routerů
4. Každý router zná pouze předchozí a následující hop, ne celou cestu

### Šifrování typu End-to-End

I2P vylepšuje tradiční onion routing pomocí „garlic routing":

- Více zpráv může být sdruženo dohromady (jako stroužky v hlavičce česneku)
- To poskytuje lepší výkon a dodatečnou anonymitu
- Ztěžuje analýzu síťového provozu

### Network Database

I2P udržuje distribuovanou síťovou databázi obsahující:

- Informace o routeru
- Cílové adresy (podobné webovým stránkám .i2p)
- Šifrovaná směrovací data

## Common Use Cases

### Tunnely

Hostujte nebo navštivte webové stránky s koncovkou `.i2p` - ty jsou dostupné pouze v rámci sítě I2P a poskytují silné záruky anonymity jak pro hostitele, tak pro návštěvníky.

### Garlic Routing

Sdílejte soubory anonymně pomocí BitTorrentu přes I2P. Mnoho torrentových aplikací má vestavěnou podporu I2P.

### Síťová databáze

Posílejte a přijímejte anonymní e-maily pomocí I2P-Bote nebo jiných e-mailových aplikací navržených pro I2P.

### Messaging

Používejte IRC, instant messaging nebo další komunikační nástroje soukromě přes síť I2P.

## Getting Started

Jste připraveni vyzkoušet I2P? Podívejte se na naši [stránku se soubory ke stažení](/downloads) a nainstalujte si I2P do svého systému.

Pro více technických podrobností se podívejte na [Technický úvod](/docs/overview/tech-intro) nebo prozkoumejte kompletní [dokumentaci](/docs).

## Jak to funguje

- [Technický úvod](/docs/overview/tech-intro) - Hlubší technické koncepty
- [Model hrozeb](/docs/overview/threat-model) - Pochopení bezpečnostního modelu I2P
- [Srovnání s Tor](/docs/overview/comparison) - Jak se I2P liší od Tor
- [Kryptografie](/docs/specs/cryptography) - Podrobnosti o kryptografických algoritmech I2P
