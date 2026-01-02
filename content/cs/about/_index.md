---
title: "O I2P"
description: "Zjistěte více o projektu The Invisible Internet Project - plně šifrované peer-to-peer překryvné síti navržené pro anonymní komunikaci."
tagline: "The Invisible Internet Project"
type: "about"
layout: "about"
established: "2002"
---

Projekt The Invisible Internet Project začal v roce 2002. Vize projektu byla, aby síť I2P "poskytovala plnou anonymitu, soukromí a bezpečnost na nejvyšší možné úrovni. Decentralizovaný a peer-to-peer internet znamená, že se už nemusíte obávat o váš ISP, který kontroluje váš provoz. To umožní lidem provádět bezproblémové činnosti a změní způsob, jakým nahlížíme na bezpečnost a dokonce i internet, využívaje veřejné klíčové kryptografie, IP steganografie a autentizace zpráv. Internet, který měl být, bude brzy."

Od té doby se I2P vyvinulo tak, aby specifikovalo a implementovalo kompletní sadu síťových protokolů schopných poskytovat vysokou úroveň soukromí, bezpečnosti a autentizace pro různé aplikace.

## Síť I2P

Síť I2P je plně šifrovaná peer-to-peer překryvná síť. Pozorovatel nemůže vidět obsah, zdroj ani cíl zprávy. Nikdo nemůže vidět, odkud pochází provoz, kam směřuje nebo co obsahuje. Navíc přenosy I2P nabízejí odolnost proti rozpoznání a blokování cenzory. Protože síť spoléhá na peers k směrování provozu, blokování na základě polohy je výzvou, která roste se sítí. Každý router v síti se podílí na činění sítě anonymní. Kromě případů, kdy by to bylo nebezpečné, se všichni podílejí na odesílání a přijímání síťového provozu.

## Jak se připojit k síti I2P

Základní software (Java) obsahuje router, který zprostředkovává a udržuje spojení se sítí. Také poskytuje aplikace a možnosti konfigurace pro přizpůsobení vašeho zážitku a pracovního postupu. Další informace naleznete v naší [dokumentaci](/docs/).

## Co mohu dělat v síti I2P?

Síť poskytuje aplikační vrstvu pro služby, aplikace a správu sítě. Síť má také svůj vlastní unikátní DNS, který umožňuje vlastní hosting a zrcadlení obsahu z internetu (Clearnet). Síť I2P funguje stejným způsobem jako internet. Softwarový balík Java obsahuje BitTorrent klienta a e-mail, stejně jako šablonu pro statické webové stránky. Další aplikace lze snadno přidat do konzole vašeho routeru.

## Přehled sítě

I2P používá kryptografii k dosažení řady vlastností pro tunely, které vytváří, a komunikace, které přenáší. Tunely I2P používají přenosy, [NTCP2](/docs/specs/ntcp2/) a [SSU2](/docs/specs/ssu2/), k zakrytí přenášeného provozu. Spojení jsou šifrována od routeru k routeru a od klienta ke klientovi (end-to-end). Dopředná sekretnost je poskytována pro všechna spojení. Protože I2P je kryptograficky adresována, adresy I2P sítě se samy autentizují a patří pouze uživateli, který je vytvořil.

Síť se skládá z peers ("routerů") a jednosměrných příchozích a odchozích virtuálních tunelů. Routery komunikují mezi sebou pomocí protokolů postavených na existujících přenosových mechanismech (TCP, UDP), přenášejí zprávy. Klientské aplikace mají své vlastní kryptografické identifikátory („Cíl“), které umožňují odesílat a přijímat zprávy. Tito klienti se mohou připojit k jakémukoli routeru a autorizovat dočasnou alokaci ("půjčku") některých tunelů, které budou použity k odesílání a přijímání zpráv skrze síť. I2P má svou vlastní interní síťovou databázi (používající modifikaci Kademlia DHT) k bezpečnému distribuci směrovacích a kontaktních informací.

## O decentralizaci a síti I2P

Síť I2P je téměř úplně decentralizovaná, s výjimkou toho, co se nazývá Reseed servery. Toto řeší bootstrappingový problém DHT (Distributed Hash Table). V podstatě neexistuje dobrý a spolehlivý způsob, jak se vyhnout provozu alespoň jednoho permanentního bootstrappingového uzlu, který mohou nečlenové sítě najít, aby mohli začít. Jakmile je router připojen k síti, objevuje peers pouze vytvářením "průzkumných" tunelů, ale ke zřízení počátečního připojení je vyžadován Reseed hostitel, který vytvoří spojení a připojí nový router k síti. Reseed servery mohou pozorovat, kdy nový router stáhl Reseed z nich, ale nic jiného o provozu na síti I2P.

## Porovnání

Existuje mnoho jiných aplikací a projektů pracujících na anonymní komunikaci a I2P bylo inspirováno mnoha z jejich úsilí. Toto není vyčerpávající seznam zdrojů anonymity - jak [Anonymní bibliografie freehavenu](http://freehaven.net/anonbib/topic.html), tak i [související projekty GNUnet](https://www.gnunet.org/links/) tuto funkci dobře splňují. K tomu je třeba říci, že několik systémů vyčnívá pro další porovnání. Další informace o tom, jak se I2P porovnává s ostatními anonymními sítěmi, naleznete v naší [podrobné dokumentaci k porovnání](/docs/overview/comparison/).
