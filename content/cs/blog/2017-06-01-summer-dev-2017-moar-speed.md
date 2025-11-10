---
title: "I2P Letní vývoj 2017: Ještě víc rychlosti!"
date: 2017-06-01
author: "str4d"
description: "Letošní Summer Dev se zaměří na sběr metrik a zlepšení výkonu sítě."
categories: ["summer-dev"]
---

Je tu zase to období roku! Pouštíme se do našeho letního vývojového programu, v němž se zaměřujeme na konkrétní aspekt I2P, abychom jej posunuli dál. Během následujících tří měsíců budeme povzbuzovat jak nové přispěvatele, tak stávající členy komunity, aby si vybrali úkol a bavili se u toho!

Loni jsme se zaměřili na pomoc uživatelům a vývojářům s lepším využitím I2P, a to vylepšováním nástrojů pro API a věnováním větší pozornosti aplikacím, které běží přes I2P. Letos chceme zlepšit uživatelskou zkušenost tím, že se zaměříme na aspekt, který se týká všech: výkon.

Přestože se sítě s onion routingem často označují jako "nízkolatenční" sítě, směrování provozu přes další počítače vytváří významnou režii. Jednosměrný design tunnel v I2P znamená, že ve výchozím nastavení se na cestě tam a zpět mezi dvěma Destinations (koncovými identitami v I2P) podílí dvanáct účastníků! Zlepšení výkonu těchto účastníků pomůže jak snížit latenci end-to-end spojení, tak zvýšit kvalitu tunnels napříč sítí.

## Ještě víc rychlosti!

Náš vývojový program bude mít letos čtyři součásti:

### Measure

Bez referenčního základu nemůžeme říct, zda zlepšujeme výkon! Vytvoříme systém metrik pro sběr údajů o používání a výkonu I2P způsobem, který zachovává soukromí, a také budeme portovat různé nástroje pro měření výkonu tak, aby běžely přes I2P (např. iperf3).

### Měření

Je zde velký prostor pro zlepšení výkonu našeho stávajícího kódu, například pro snížení režie spojené s účastí v tunnels. Zaměříme se na potenciální vylepšení kryptografických primitiv, síťových transportů (jak na úrovni spojové vrstvy, tak end-to-end), profilování peerů a výběru tras pro tunnels.

### Optimalizovat

Máme několik otevřených návrhů na zlepšení škálovatelnosti sítě I2P (např. Prop115, Prop123, Prop124, Prop125, Prop138, Prop140). Budeme na těchto návrzích pracovat a začneme ty dokončené implementovat v různých síťových routerech.

### Postup

I2P je paketově komutovaná síť, podobně jako internet, nad kterým běží. To nám dává značnou flexibilitu v tom, jak směrujeme pakety, a to jak z hlediska výkonu, tak soukromí. Většina této flexibility zůstává neprozkoumaná! Chceme podpořit výzkum toho, jak lze různé techniky z clearnetu (veřejný internet) pro zlepšení propustnosti aplikovat na I2P a jak by mohly ovlivnit soukromí účastníků sítě.

## Take part in Summer Dev!

Máme spoustu dalších nápadů na věci, které bychom v těchto oblastech rádi dokončili. Pokud máte zájem vyvíjet software pro ochranu soukromí a anonymitu, navrhovat protokoly (kryptografické či jiné) nebo zkoumat nové nápady do budoucna – přijďte si s námi popovídat na IRC nebo na Twitteru! Vždy rádi vítáme nováčky v naší komunitě. Navíc pošleme I2P samolepky všem novým přispěvatelům, kteří se zapojí!

Budeme zde průběžně zveřejňovat, ale náš postup můžete také sledovat a sdílet své vlastní nápady a práci pod hashtagem #I2PSummer na Twitteru. Vzhůru do léta!
