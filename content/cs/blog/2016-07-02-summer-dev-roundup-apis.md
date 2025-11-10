---
title: "Letní vývojářský souhrn: API"
date: 2016-07-02
author: "str4d"
description: "V prvním měsíci Summer Dev jsme zlepšili použitelnost našich rozhraní API pro vývojáře pracující s Javou, Androidem a Pythonem."
categories: ["summer-dev"]
---

Summer Dev je v plném proudu: pilně promazáváme soukolí, obrušujeme hrany a dáváme to tu do pucu. Teď je čas na náš první souhrn, ve kterém vás uvedeme do obrazu o tom, jakého děláme pokroku!

## Měsíc API

Naším cílem pro tento měsíc bylo "zapadnout" - zajistit, aby naše API a knihovny fungovaly v rámci stávající infrastruktury různých komunit, aby vývojáři aplikací mohli s I2P pracovat efektivněji a uživatelé nemuseli řešit detaily.

### Java / Android

Klientské knihovny I2P jsou nyní k dispozici na Maven Central! To by mělo vývojářům v Javě výrazně zjednodušit používání I2P v jejich aplikacích. Namísto nutnosti získávat knihovny z aktuální instalace mohou jednoduše přidat I2P mezi své závislosti. Aktualizace na nové verze bude podobně mnohem snazší.

Klientská knihovna I2P pro Android byla také aktualizována, aby používala nové knihovny I2P. To znamená, že multiplatformní aplikace mohou fungovat nativně buď s I2P Android, nebo s desktopovým I2P.

### Java / Android

#### txi2p

Zásuvný modul Twisted `txi2p` nyní podporuje porty uvnitř I2P a bezproblémově funguje přes místní rozhraní API SAM, vzdálená rozhraní API SAM a rozhraní API SAM s přesměrováním portů. Pokyny k použití najdete v jeho dokumentaci a případné problémy hlaste na GitHubu.

#### i2psocket

První (beta) verze `i2psocket` byla vydána! Jde o přímou náhradu za standardní knihovnu jazyka Python `socket`, která ji rozšiřuje o podporu I2P přes SAM API. Pokyny k použití a pro nahlášení případných problémů najdete na její stránce na GitHubu.

### Python

- zzz has been hard at work on Syndie, getting a headstart on Plugins month
- psi has been creating an I2P test network using i2pd, and in the process has found and fixed several i2pd bugs that will improve its compatibility with Java I2P

## Coming up: Apps month!

Jsme nadšení, že v červenci budeme spolupracovat s Tahoe-LAFS! I2P už dlouho hostí jeden z největších veřejných gridů, který používá upravenou verzi Tahoe-LAFS. Během měsíce aplikací jim pomůžeme s jejich probíhající prací na přidání nativní podpory pro I2P a Tor, aby uživatelé I2P mohli těžit ze všech vylepšení v upstreamu.

Existuje několik dalších projektů, se kterými budeme hovořit o jejich plánech na integraci s I2P a budeme také pomáhat s návrhem. Sledujte tento prostor!

## Take part in Summer Dev!

Máme mnoho dalších nápadů na to, co bychom v těchto oblastech chtěli udělat. Pokud máte zájem podílet se na vývoji softwaru pro ochranu soukromí a anonymitu, navrhovat uživatelsky přívětivé weby či rozhraní, nebo psát návody pro uživatele: přijďte si s námi popovídat na IRC nebo Twitteru! Vždy rádi vítáme nováčky v naší komunitě.

Budeme zde průběžně zveřejňovat, jak postupujeme, ale náš postup můžete také sledovat a své vlastní nápady a práci sdílet pod hashtagem #I2PSummer na Twitteru. Vzhůru do léta!
