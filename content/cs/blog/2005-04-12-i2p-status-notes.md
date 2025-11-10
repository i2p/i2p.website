---
title: "Poznámky ke stavu I2P k 2005-04-12"
date: 2005-04-12
author: "jr"
description: "Týdenní aktualizace zahrnující opravy netDb ve verzi 0.5.0.6, pokrok v transportu SSU přes UDP, výsledky bayesovského profilování peerů a vývoj Q"
categories: ["status"]
---

Ahoj všichni, zase je čas na aktualizaci

* Index

1) Stav sítě 2) Stav SSU 3) Bayesovské profilování peerů (protějšků v síti) 4) Stav Q 5) ???

* 1) Net status

Zdá se, že vydání 0.5.0.6 z minulého týdne opravilo problémy s netDb, které jsme zaznamenávali (hurá). Weby a služby jsou mnohem spolehlivější než byly ve verzi 0.5.0.5, i když se objevily některé zprávy o potížích, kdy se web nebo služba po několika dnech provozu staly nedostupnými.

* 2) SSU status

Na kódu UDP pro verzi 0.6 došlo k velkému pokroku a první várka commitů už byla zanesena do CVS. Zatím to není nic, co byste skutečně mohli používat, ale základy jsou na svém místě. Vyjednávání relace funguje dobře a polospolehlivé doručování zpráv se chová podle očekávání. Pořád je však před námi spousta práce, je potřeba napsat testovací případy a odladit neobvyklé situace, ale je to pokrok.

Pokud půjde vše dobře, mohli bychom příští týden spustit alfa testování, určené jen pro lidi, kteří dokážou explicitně nakonfigurovat své firewally/NATy. Nejprve bych chtěl odladit obecné fungování, než přidám obsluhu relé, doladím netDb pro rychlejší expiraci routerInfo a vyberu relé k publikování. Také využiji této příležitosti k provedení celé řady testů, protože se řeší několik kritických faktorů řazení do front.

* 3) Bayesian peer profiling

bla intenzivně pracuje na některých revizích toho, jak rozhodujeme, přes které protějšky prochází tunnel, a přestože se bla nemohl zúčastnit schůzky, je tu několik zajímavých údajů k předložení:

<+bla> Provedl jsem přímá měření rychlosti uzlů: profiloval jsem        asi 150 uzlů pomocí OB tunnels o délce 0, IB tunnels o        délce 1, batching-interval = 0ms
<+bla> K tomu jsem právě udělal _velmi_ základní a        _předběžné_ odhadování rychlosti pomocí naivní Bayesovské        klasifikace
<+bla> To druhé bylo provedeno s výchozími délkami expl. tunnels
<+bla> Průnik množiny uzlů, u nichž mám "skutečná data", a množiny        uzlů v aktuálních měřeních, je 117 uzlů
<+bla> Výsledky nejsou _tak_ špatné, ale ani nijak zvlášť působivé
<+bla> Viz http://theland.i2p/estspeed.png
<+bla> Základní oddělení velmi pomalých/rychlých uzlů je tak nějak OK, ale jemné        rozlišení mezi rychlejšími uzly by mohlo být mnohem lepší
<+jrandom2p> hmm, jak se vlastně vypočítaly skutečné hodnoty – je to              plné RTT (round-trip time, doba zpáteční cesty) nebo je to RTT/délka ?
<+bla> Při použití normálních expl. tunnels je téměř nemožné        zabránit dávkovacím prodlevám.
<+bla> Skutečné hodnoty jsou „skutečná data“: ty získané        s OB=0 a IB=1
<+bla> (a variance=0 a bez dávkovací prodlevy)
<+jrandom2p> ty výsledky ale odsud vypadají docela dobře
<+bla> Odhadované časy jsou ty získané pomocí Bayesovské        inference z _reálných_ expl. tunnels o délce 2 +/- 1
<+bla> Je to získáno z 3000 RTT, zaznamenaných během        zhruba 3 hodin (to je dlouhé)
<+bla> Prozatím to předpokládá, že rychlost peera je statická.        Ještě musím implementovat váhování
<+jrandom2p> zní to božsky.  pěkná práce, bla
<+jrandom2p> hmm, takže odhad by se měl rovnat 1/4 skutečného
<+bla> jrandom: Ne: Všechny naměřené RTT (používající normální expl.        tunnels) jsou korigovány o počet hopů na        cestě tam a zpět
<+jrandom2p> aha, ok
<+bla> Teprve potom se natrénuje Bayesovský klasifikátor
<+bla> Zatím řadím naměřené časy na hop do 10 tříd:        50, 100, ..., 450 ms, a další třídu >500 ms
<+bla> Např. malé zpoždění na hop by mohlo být váženo větším        faktorem, stejně jako úplná selhání (>60000 ms).
<+bla> I tak... 65% odhadovaných časů spadá do 0.5        směrodatné odchylky od skutečného času uzlu
<+bla> Nicméně to je potřeba přepočítat, protože směrodatnou odchylku        silně ovlivňují selhání >60000 ms

Po další diskusi bla předložil srovnání se stávajícím kalkulátorem rychlosti, zveřejněné na http://theland.i2p/oldspeed.png Zrcadla těch PNG jsou k dispozici na http://dev.i2p.net/~jrandom/estspeed.png a http://dev.i2p.net/~jrandom/oldspeed.png

(pro terminologii, IB=počet hopů ve vstupním tunnelu, OB=počet hopů ve výstupním tunnelu, a po upřesnění byla "ground truth" (referenční) měření získána s 1 hopem na výstupu a 0 hopem na vstupu, nikoli naopak)

* 4) Q status

Aum také výrazně pokročil s Q; nejnověji pracoval na webovém klientském rozhraní. Příští sestavení Q nebude zpětně kompatibilní, protože obsahuje celou řadu nových funkcí, ale jsem si jistý, že od Auma uslyšíme víc, jakmile bude co sdělit :)

* 5) ???

To je pro tuto chvíli asi všechno (musím to rychle uzavřít, než začne schůzka). Jo, a jen tak na okraj, vypadá to, že se budu stěhovat dřív, než bylo plánováno, takže se možná některé termíny v roadmapě posunou, zatímco budu na cestě někam, kde nakonec zakotvím. Každopádně se za pár minut zastavte na kanálu a bombardujte nás novými nápady!

=jr
