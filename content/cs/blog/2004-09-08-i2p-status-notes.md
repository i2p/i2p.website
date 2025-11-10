---
title: "Poznámky ke stavu I2P k 2004-09-08"
date: 2004-09-08
author: "jr"
description: "Týdenní aktualizace stavu I2P zahrnující vydání verze 0.4, problémy s kapacitou sítě, aktualizace webu a vylepšení rozhraní I2PTunnel"
categories: ["status"]
---

Ahoj všichni, omlouvám se za zpoždění...

## Rejstřík:

1. 0.4
2. Capacity and overload
3. Website updates
4. I2PTunnel web interface
5. Roadmap and todo
6. ???

## 1) 0.4

Jak jste si jistě všichni všimli, verze 0.4 vyšla před pár dny a celkově to jde docela dobře. Je těžké uvěřit, že už je to 6 měsíců od vydání 0.3 (a rok od vydání 1.0 SDK), ale ušli jsme dlouhou cestu a vaše tvrdá práce, nadšení a trpělivost udělaly divy. Gratulujeme a děkujeme!

Jako u každého dobrého vydání jsme hned po vypuštění narazili na pár problémů a za posledních pár dní se nám nahromadila hlášení o chybách a opravujeme jako šílení (můžete sledovat změny, jak jsou opravovány). Pořád nám ještě zbývá pár chyb k odstranění předtím, než vypustíme další revizi, ale to bychom měli stihnout během příštího dne nebo dvou.

## 2) Kapacita a přetížení

V posledních několika vydáních jsme zaznamenali poměrně nevyvážené alokace tunnels, a i když některé z nich souvisejí s chybami (dva z nich byly opraveny od vydání 0.4), stále tu zůstává obecná otázka ohledně algoritmu - kdy by měl router přestat přijímat další tunnels?

Před několika revizemi jsme přidali kód pro throttling (omezení průtoku), který odmítá požadavky na účast v tunnelu, pokud byl router přetížen (lokální doba zpracování zpráv přesahuje 1 s), a to výrazně pomohlo. Nicméně existují dva aspekty toho jednoduchého algoritmu, které nejsou řešeny: - když je naše šířka pásma saturovaná, naše lokální doba zpracování může být stále rychlá, takže bychom dál přijímali další požadavky na tunnel - když se jeden peer účastní "příliš mnoha" tunnels, jejich selhání více poškodí síť.

První problém se řeší poměrně snadno prostým zapnutím omezení šířky pásma (protože omezení šířky pásma zpomaluje dobu zpracování zpráv úměrně prodlevě dané šířkou pásma). Druhý je složitější a je potřeba jak více výzkumu, tak i více simulací. Uvažuji o přístupu, kdy by se pravděpodobnostně odmítaly požadavky na tunnel podle poměru mezi účastí v tunnel a požadavky na tunnel ze sítě, s nějakým základním "kindness factor" (faktorem vstřícnosti), přičemž P(reject) = 0, pokud se účastníme méně než to.

Ale jak jsem řekl, je potřeba více práce a simulace.

## 3) Aktualizace webu

Teď, když máme nové webové rozhraní I2P, je prakticky veškerá naše stará dokumentace pro koncové uživatele zastaralá. Potřebujeme pomoc s procházením těchto stránek a jejich aktualizací tak, aby popisovaly, jak věci fungují nyní. Jak navrhli duck a další, potřebujeme nového průvodce 'rychlým startem' nad rámec `http://localhost:7657/` readme - něco, co lidem pomůže rychle začít a dostat se do systému.

Kromě toho má naše nové webové rozhraní dostatek prostoru pro integraci kontextově citlivé nápovědy. Jak můžete vidět v přiloženém help.jsp, "hmm. asi bychom sem měli dát nějaký text nápovědy."

Bylo by asi dobré, kdybychom na různé stránky mohli přidat odkazy 'O aplikaci' a/nebo 'Řešení problémů', které by vysvětlovaly, co jednotlivé položky znamenají a jak je používat.

## 4) Webové rozhraní I2PTunnel

Nazvat nové `http://localhost:7657/i2ptunnel/` rozhraní „spartánským“ by bylo slabé slovo. Musíme na tom ještě hodně zapracovat, aby se to přiblížilo použitelné podobě - momentálně tam ta funkčnost sice technicky je, ale abyste se v tom vyznali, opravdu musíte vědět, co se děje na pozadí. Myslím, že duck k tomu možná bude mít další nápady, které zmíní na schůzce.

## 5) Plán vývoje a úkoly

Zanedbával jsem udržování roadmapy v aktuálním stavu, ale pravda je, že nás čekají další revize. Abych pomohl vysvětlit, co považuji za „velké problémy“, dal jsem dohromady nový seznam úkolů, který u každého z nich jde trochu do detailu. Myslím, že bychom nyní měli být poměrně otevření zvážení našich možností a případnému přepracování roadmapy.

Jedna věc, kterou jsem na tom seznamu úkolů zapomněl zmínit, je, že při přidávání odlehčeného protokolu připojení můžeme zahrnout (volitelnou) automatickou detekci IP adresy. To může být 'nebezpečné' (proto to bude volitelné), ale dramaticky to sníží počet požadavků na podporu, které dostáváme :)

Každopádně problémy uvedené na seznamu úkolů jsou ty, které jsme plánovali pro různá vydání, a rozhodně nebudou všechny v 1.0 ani v 2.0. Načrtl jsem několik různých možných variant prioritizace/vydání, ale zatím to nemám pevně dané. Nicméně pokud budou lidé schopni identifikovat další velké věci do budoucna, bylo by to velmi vítané, protože neplánovaný problém vždycky přináší komplikace.

## 6) ???

Dobře, to je prozatím všechno (což je vlastně dobře, protože schůzka začíná za pár minut). Zastavte se na #i2p na irc.freenode.net, www.invisiblechat.com, nebo irc.duck.i2p v 21:00 GMT, abychom mohli dál chatovat.
