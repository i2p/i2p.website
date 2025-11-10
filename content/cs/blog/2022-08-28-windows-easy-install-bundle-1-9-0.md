---
title: "Balíček pro snadnou instalaci pro Windows, vydání 1.9.0"
date: 2022-08-28
author: "idk"
description: "Windows Easy-Install Bundle 1.9.0 - Zásadní vylepšení stability/kompatibility"
categories: ["release"]
API_Translate: pravda
---

## Tato aktualizace zahrnuje nový router 1.9.0 a zásadní vylepšení uživatelského komfortu pro uživatele balíčku

Toto vydání obsahuje nový router I2P 1.9.0 a je založeno na Javě 18.02.1.

Staré dávkové skripty byly vyřazeny ve prospěch flexibilnějšího a stabilnějšího řešení přímo v nástroji jpackage. To by mělo opravit všechny chyby související s vyhodnocováním cest a jejich uvozováním, které se v dávkových skriptech vyskytovaly. Po aktualizaci lze dávkové skripty bezpečně odstranit. Při příští aktualizaci je instalátor odstraní.

Byl zahájen subprojekt pro správu nástrojů pro prohlížení: i2p.plugins.firefox, který nabízí rozsáhlé možnosti automatické a stabilní konfigurace I2P prohlížečů na mnoha platformách. Tento nástroj byl použit k nahrazení dávkových skriptů, ale zároveň funguje jako multiplatformní nástroj pro správu I2P Browser. Příspěvky jsou vítány zde: http://git.idk.i2p/idk/i2p.plugins.firefox ve zdrojovém repozitáři.

Toto vydání zlepšuje kompatibilitu s instancemi I2P router běžícími externě, například s těmi, které poskytuje instalátor IzPack, a s implementacemi třetích stran, jako je i2pd. Zlepšením zjišťování externího router vyžaduje méně systémových prostředků, zkracuje dobu spouštění a brání vzniku konfliktů o prostředky.

Kromě toho byl profil aktualizován na nejnovější verzi profilu Arkenfox. I2P in Private Browsing a NoScript byly aktualizovány. Profil byl restrukturován, aby bylo možné vyhodnocovat různé konfigurace pro různé modely hrozeb.
