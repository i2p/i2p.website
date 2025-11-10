---
title: "Poznámky ke stavu I2P k 2006-01-03"
date: 2006-01-03
author: "jr"
description: "Novoroční aktualizace zahrnující stabilitu verze 0.6.1.8, výsledky zátěžového testování a profilování peerů pro optimalizaci propustnosti a komplexní zhodnocení roku 2005 s náhledem na roadmapu (plán vývoje) pro rok 2006"
categories: ["status"]
---

Ahoj všichni, šťastný nový rok! Pojďme se po týdnu bez nich vrátit k našim týdenním poznámkám o stavu -

* Index

1) Stav sítě a 0.6.1.8 2) Výsledky zátěžového testování a profilování peerů 3) Zhodnocení roku 2005 / Výhled na rok 2006 / ???

* 1) Net status and 0.6.1.8

Nedávno jsme vydali 0.6.1.8 a zprávy z provozu říkají, že úpravy od zzz výrazně pomohly a že je situace v síti poměrně stabilní, a to i přes v poslední době výrazně zvýšený síťový provoz (podle stats.i2p se průměr za poslední měsíc zřejmě zdvojnásobil). I2PSnark se také zdá fungovat docela dobře - narazili jsme sice na několik zádrhelů, ale většinu z nich jsme dohledali a opravili v následujících sestaveních. K novému blogovému rozhraní Syndie nepřišlo mnoho ohlasů, ale zaznamenali jsme mírný nárůst provozu Syndie (částečně díky tomu, že protocol objevil dustův RSS/Atom importér :)

* 2) Load testing results and peer profiling

Posledních několik týdnů se snažím přesně identifikovat naše úzké hrdlo propustnosti. Různé softwarové komponenty jsou všechny schopné posílat data mnohem vyššími rychlostmi, než jaké obvykle vidíme u end-to-end komunikace přes I2P, takže je benchmarkuji v živé síti pomocí vlastního kódu pro zátěžové testování. První sada testů, budování jednohopových příchozích tunnels přes všechny routery v síti a co nejrychlejší přenos dat tímto tunnelem, přinesla velmi slibné výsledky, přičemž routery zvládaly rychlosti zhruba v rozsahu toho, co by se od nich dalo očekávat (např. většina zvládala jen dlouhodobý průměr 4-16KBps, ale jiné protlačily 20-120KBps skrz jediný tunnel). Tento test byl dobrým výchozím bodem pro další zkoumání a ukázal, že samotné zpracování tunnelu je schopné protlačit mnohem víc, než obvykle vídáme.

Pokusy replikovat tyto výsledky přes živé tunnels nebyly tak úspěšné. Nebo by se možná dalo říct, že byly úspěšnější, protože vykázaly propustnost podobnou té, kterou aktuálně vidíme, což znamenalo, že jsme byli na správné stopě. Když se vrátím k výsledkům 1hop testu, upravil jsem kód tak, aby vybíral peers (uzly), které jsem ručně identifikoval jako rychlé, a znovu jsem spustil zátěžové testy přes živé tunnels s tímto "podvodným" výběrem peers, a přestože to nedosáhlo hranice 120KBps, ukázalo to rozumné zlepšení.

Bohužel požadovat po lidech, aby si ručně vybírali své peery, přináší vážné problémy jak pro anonymitu, tak i, no, použitelnost, ale vyzbrojeni daty ze zátěžových testů se zdá, že existuje cesta ven. Posledních pár dní testuji novou metodu profilování peerů podle jejich rychlosti – v zásadě sleduje jejich špičkovou udržitelnou propustnost místo jejich nedávné latence. Naivní implementace byly poměrně úspěšné a přestože to nevybralo přesně ty peery, které bych zvolil ručně, odvedlo to docela dobrou práci. Stále je ale potřeba doladit několik věcí, například zajistit, že dokážeme povyšovat průzkumné tunnels (tunely) do rychlé úrovně, ale momentálně v této oblasti zkouším několik experimentů.

Celkově si myslím, že se blížíme ke konci této etapy zaměřené na propustnost, protože narážíme na nejužší hrdlo a rozšiřujeme ho. Jsem si jistý, že brzy narazíme na další, a to nám rozhodně nepřinese běžné rychlosti internetu, ale mělo by to pomoci.

* 3) 2005 review / 2006 preview / ???

Říci, že rok 2005 byl průlomový, je trochu slabé – během 25 vydání v uplynulém roce jsme I2P v mnoha ohledech vylepšili, síť jsme zvětšili pětinásobně, nasadili několik nových klientských aplikací (Syndie, I2Phex, I2PSnark, I2PRufus), migrovali na novou irc2p IRC síť postmana a cervantes a byli svědky rozkvětu několika užitečných eepsites(I2P Sites) (například zzz's stats.i2p, orion's orion.i2p a tino's proxy a monitorovací služby, abychom jmenovali alespoň některé). Komunita také opět o něco dospěla, a to z nemalé části díky podpoře, kterou na fóru a v kanálech poskytují Complication a další, a kvalita i pestrost hlášení chyb ze všech oblastí se výrazně zlepšily. Pokračující finanční podpora těch v rámci komunity je působivá, a přestože ještě nedosahuje úrovně potřebné pro zcela udržitelný vývoj, máme rezervu, která mě uživí přes zimu.

Všem, kteří se v uplynulém roce zapojili, ať už technicky, společensky nebo finančně, děkujeme za vaši pomoc!

Rok 2006 pro nás bude velký: 0.6.2 vyjde tuto zimu, vydání 1.0 plánujeme na jaro či léto a 2.0 na podzim, ne-li dříve. Tohle bude rok, kdy se ukáže, co dokážeme, a práce na aplikační vrstvě bude ještě důležitější než dřív. Takže pokud máte nějaké nápady, teď je ten pravý čas se do toho pustit :)

Každopádně, naše týdenní statusová schůzka začíná za pár minut, takže pokud je něco, co byste chtěli dál probrat, zastavte se na #i2p na obvyklých místech [1] a pozdravte!

=jr [1] http://forum.i2p.net/viewtopic.php?t=952
