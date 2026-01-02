---
title: "20 let soukromí: Stručná historie I2P"
date: 2021-08-28
slug: "20-years-of-privacy-a-brief-history-of-i2p"
author: "sadie"
description: "Historie I2P, jak ji známe"
categories: ["general"]
API_Translate: pravda
---

## Invisibility is the best defense: building an internet within an internet

> "Věřím, že většina lidí chce tuto technologii proto, aby se mohli svobodně vyjadřovat. Je to příjemný pocit, když víte, že to můžete dělat. Zároveň můžeme překonat některé problémy, které na internetu vidíme, tím, že změníme způsob, jakým jsou vnímány bezpečnost a soukromí, a také míru, do jaké si jich ceníme."

V říjnu 2001 měl 0x90 (Lance James) sen. Začalo to jako "touha po okamžité komunikaci s dalšími uživateli Freenetu, aby bylo možné mluvit o otázkách týkajících se Freenetu a vyměňovat si klíče Freenetu, a přitom zachovat anonymitu, soukromí a bezpečnost." Říkalo se tomu IIP — the Invisible IRC Project.

The Invisible IRC Project vycházel z ideálu a rámce, které stály za The InvisibleNet. V rozhovoru z roku 2002 popsal 0x90 projekt jako zaměřený na "inovaci inteligentních síťových technologií" s cílem "poskytovat nejvyšší standardy v oblasti bezpečnosti a soukromí na široce používaném, avšak notoricky nezabezpečeném Internetu."

Do roku 2003 už vzniklo několik dalších podobných projektů, z nichž největšími byly Freenet, GNUNet a Tor. Všechny tyto projekty měly široké cíle: šifrovat a anonymizovat různé typy provozu. Pro IIP se ukázalo, že samotné IRC není dostatečně velkým cílem. Byla potřeba anonymizační vrstva pro všechny protokoly.

Na začátku roku 2003 se k projektu připojil nový anonymní vývojář, "jrandom". Jeho výslovným cílem bylo rozšířit rámec IIP. jrandom si přál přepsat kódovou základnu IIP v Javě a přepracovat protokoly na základě nedávných publikací a raných návrhových rozhodnutí, která tehdy přijímaly projekty Tor a Freenet. Některé koncepty, jako "cibulové směrování", byly upraveny a vzniklo z nich "česnekové směrování".

Ke konci léta 2003 převzal jrandom kontrolu nad projektem a přejmenoval jej na Invisible Internet Project neboli "I2P". Vydal dokument, který nastínil filozofii projektu, a zasadil jeho technické cíle a návrh do kontextu mixnetů a anonymizačních vrstev. Zveřejnil také specifikaci dvou protokolů (I2CP a I2NP), které se staly základem sítě, kterou I2P používá dodnes.

Do podzimu 2003 se I2P, Freenet a Tor rychle rozvíjely. jrandom vydal 1. listopadu 2003 verzi I2P 0.2 a následující tři roky pokračoval v rychlém vydávání.

V únoru 2005 zzz poprvé nainstaloval I2P. Do léta 2005 zzz zprovoznil zzz.i2p a stats.i2p, které se staly klíčovými zdroji pro vývoj I2P. V červenci 2005 jrandom vydal verzi 0.6, včetně inovativního transportního protokolu SSU (Secure Semi-reliable UDP) pro zjišťování IP adres a překonávání firewallů.

Od konce roku 2006 a v průběhu roku 2007 se vývoj jádra I2P dramaticky zpomalil, protože jrandom přesunul svou pozornost na Syndie. V listopadu 2007 udeřila pohroma, když jrandom poslal záhadnou zprávu, že si bude muset vzít volno na rok nebo déle. Bohužel už se jrandom nikdy neozval.

Druhá fáze katastrofy nastala 13. ledna 2008, kdy hostingovou společnost pro téměř všechny servery i2p.net postihl výpadek proudu a nepodařilo se jí plně obnovit provoz. Complication, welterde a zzz rychle přijali rozhodnutí, jak projekt znovu zprovoznit: přesunout se na i2p2.de a přejít z CVS na monotone pro správu zdrojového kódu.

Projekt si uvědomil, že byl příliš závislý na centralizovaných prostředcích. Práce v průběhu roku 2008 projekt decentralizovala a rozdělila role mezi více lidí. Počínaje vydáním 0.7.6 dne 31. července 2009 zzz podepsal následujících 49 vydání.

Do poloviny roku 2009 zzz mnohem lépe porozuměl kódové základně a identifikoval mnoho problémů se škálovatelností. Síť zaznamenala růst díky schopnostem anonymizace i obcházení cenzury. V rámci sítě se staly dostupnými automatické aktualizace.

Na podzim 2010 zzz vyhlásil moratorium na vývoj I2P, dokud nebude webová dokumentace kompletní a přesná. Trvalo to 3 měsíce.

Od roku 2010 se zzz, ech, hottuna a další přispěvatelé každoročně účastnili CCC (Chaos Communications Congress) až do zavedení omezení kvůli covidu. Projekt budoval komunitu a společně oslavoval vydání.

V roce 2013 vznikla Anoncoin jako první kryptoměna s vestavěnou podporou I2P, přičemž vývojáři jako meeh zajišťovali pro síť I2P infrastrukturu.

V roce 2014 začal str4d přispívat do I2PBote a na Real World Crypto se začalo diskutovat o aktualizaci kryptografie I2P. Ke konci roku 2014 byla většina nové podpisové kryptografie dokončena, včetně ECDSA a EdDSA.

V roce 2015 se v Torontu konala I2PCon s přednáškami, podporou komunity a účastníky z Ameriky a Evropy. V roce 2016 na Real World Crypto Stanford přednesl str4d přednášku o pokroku v migraci kryptografie.

NTCP2 bylo implementováno v roce 2018 (vydání 0.9.36), což poskytuje odolnost vůči cenzuře založené na DPI (hluboká inspekce paketů) a snižuje zatížení procesoru díky rychlejší, moderní kryptografii.

V roce 2019 se tým zúčastnil více konferencí, včetně DefConu a Monero Village, a oslovoval vývojáře a výzkumníky. Výzkum týkající se cenzury I2P od Hoàng Nguyêna Phonga byl přijat na FOCI v rámci USENIXu, což vedlo ke vzniku I2P Metrics.

Na CCC 2019 bylo rozhodnuto migrovat z Monotone na GitLab. Dne 10. prosince 2020 projekt oficiálně přešel z Monotone na Git a připojil se k řadám vývojářů používajících Git.

0.9.49 (2021) zahájila migraci na nové, rychlejší šifrování ECIES-X25519 pro routery, čímž završila roky práce na specifikaci. Migrace měla trvat několik vydání.

## 1.5.0 — Předčasné výroční vydání

Po 9 letech vydávání řady 0.9.x přešel projekt přímo z 0.9.50 na 1.5.0 jako uznání téměř 20 let práce na zajištění anonymity a bezpečnosti. Toto vydání dokončilo implementaci menších zpráv pro sestavování tunnel ke snížení spotřeby šířky pásma a pokračovalo v přechodu na šifrování X25519.

**Gratuluji, týme. Pojďme udělat dalších 20.**
