---
title: "Aktualizace k notarizaci Mac Easy Install"
date: 2023-01-31
author: "idk, sadie"
description: "Easy Install Bundle pro Mac se zasekl"
categories: ["release"]
API_Translate: pravda
---

I2P Easy-Install Bundle for Mac (balíček pro snadnou instalaci na Mac) se v posledních 2 vydáních potýká s pozastavenými aktualizacemi kvůli odchodu svého správce. Doporučuje se, aby uživatelé Easy-Install Bundle pro Mac přešli na klasický instalátor ve stylu Java, který byl nedávno obnoven na stránce ke stažení.  Verze 1.9.0 má známé bezpečnostní problémy a není vhodná pro hostování služeb ani pro jakékoli dlouhodobé použití. Uživatelům se doporučuje co nejdříve přejít na jiný způsob instalace. Pokročilí uživatelé Easy-Install Bundle to mohou obejít tak, že balíček zkompilují ze zdrojových kódů a software si sami podepíší.

## Proces notarizace pro MacOS

Proces distribuce aplikace uživatelům Apple zahrnuje mnoho kroků. Aby bylo možné aplikaci bezpečně distribuovat jako .dmg, musí projít procesem notarizace. Aby bylo možné aplikaci odeslat k notarizaci, musí ji vývojář podepsat sadou certifikátů, která zahrnuje jeden pro podepisování kódu a jeden pro podepsání samotné aplikace. Toto podepisování musí proběhnout v konkrétních fázích během procesu sestavení, ještě předtím, než lze vytvořit finální balíček .dmg, který je distribuován koncovým uživatelům.

I2P Java je komplexní aplikace, a proto je nutné metodou pokus–omyl ladit, jaké typy kódu v aplikaci odpovídají certifikátům od Apple a kde má proběhnout podepisování, aby vzniklo platné časové razítko. Právě kvůli této složitosti stávající dokumentace pro vývojáře nedostačuje a týmu nepomáhá porozumět správné kombinaci faktorů, jež povede k úspěšné notarizaci.

Tyto potíže způsobují, že časový plán dokončení tohoto procesu je těžko předvídatelný. Nebudeme vědět, že máme hotovo, dokud nebudeme schopni vyčistit kompilační prostředí a projít celý proces od začátku do konce. Dobrou zprávou je, že jsme snížili počet chyb během notarizačního procesu na pouhé 4 z více než 50 při prvním pokusu a můžeme rozumně předpokládat, že to bude dokončeno před nebo nejpozději včas pro další vydání v dubnu.

## Možnosti pro nové instalace a aktualizace I2P na macOS

Noví účastníci I2P si stále mohou stáhnout Easy Installer pro software pro macOS ve verzi 1.9.0. Doufám, že vydání bude připraveno ke konci dubna. Aktualizace na nejnovější verzi budou k dispozici, jakmile bude úspěšně dokončena notarizace.

Klasická možnost instalace je také k dispozici. To bude vyžadovat stažení Javy a softwaru I2P prostřednictvím instalátoru založeného na .jar.

[Pokyny k instalaci JAR jsou k dispozici zde](https://geti2p.net/en/download/macos)

Uživatelé Easy-Install mohou aktualizovat na tuto nejnovější verzi pomocí lokálně vytvořeného vývojového sestavení.

[Pokyny pro sestavení Easy-Install jsou k dispozici zde](https://i2pgit.org/i2p-hackers/i2p-jpackage-mac/-/blob/master/BUILD.md)

Je také možné odinstalovat software, odstranit konfigurační adresář I2P a znovu nainstalovat I2P pomocí instalátoru .jar.
