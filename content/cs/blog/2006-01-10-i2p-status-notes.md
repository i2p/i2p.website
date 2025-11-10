---
title: "Poznámky ke stavu I2P ze dne 2006-01-10"
date: 2006-01-10
author: "jr"
description: "Týdenní aktualizace zahrnující algoritmy profilování propustnosti, vylepšení zobrazení blogu v Syndie, pokrok u trvalých HTTP spojení a vývoj gwebcache v I2Phexu"
categories: ["status"]
---

Ahoj všichni, zdá se, že je tu zase úterý

* Index

1) Stav sítě 2) Profilování propustnosti 3) Syndie blogy 4) Trvalá HTTP spojení 5) I2Phex gwebcache 6) ???

* 1) Net status

Uplynulý týden přinesl v CVS spoustu oprav chyb a vylepšení, přičemž aktuální sestavení je na verzi 0.6.1.8-11. Síť byla poměrně stabilní, i když některé výpadky u různých poskytovatelů služeb I2P vedly k občasným zádrhelům. Konečně jsme se v CVS zbavili zbytečně vysoké fluktuace identit routerů a v jádru je nová oprava chyby, se kterou včera přišel zzz; zní to docela slibně, ale musíme počkat, jaký to bude mít dopad. Dalšími dvěma velkými věcmi z minulého týdne bylo nové profilování rychlosti založené na propustnosti a výrazné práce na zobrazení blogu v Syndie. Co se týče toho, kdy uvidíme 0.6.1.9, mělo by to vyjít později tento týden, nejpozději o víkendu. Sledujte obvyklé kanály.

* 2) Throughput profiling

Otestovali jsme několik nových algoritmů profilování peerů (uzlů) pro sledování propustnosti, ale během posledního zhruba týdne jsme se zřejmě ustálili na jednom, který vypadá docela dobře. V zásadě sleduje potvrzenou propustnost jednotlivých tunnelů v jednominutových intervalech a podle toho upravuje odhady propustnosti pro peery. Nepokouší se určovat průměrnou rychlost pro daný peer, protože je to velmi složité, jednak proto, že tunnely zahrnují více peerů, a jednak proto, že měření potvrzené propustnosti často vyžaduje více tunnelů. Místo toho odhaduje průměrnou špičkovou rychlost - konkrétně měří tři nejvyšší rychlosti, jakými peerovy tunnely dokázaly přenášet, a ty zprůměruje.

Podstata je v tom, že tyto rychlosti, měřené po dobu celé minuty, jsou udržitelnými rychlostmi, kterých je peer schopen dlouhodobě dosahovat, a protože každý peer je přinejmenším tak rychlý jako end‑to‑end naměřená rychlost, je bezpečné označit každého z nich jako takto rychlého. Zkoušeli jsme na to i jiný postup – měřit celkovou propustnost peeru přes tunnels v různých obdobích, a to poskytovalo ještě jasnější informace o špičkové rychlosti, ale výrazně znevýhodňovalo ty peery, kteří ještě nebyli označeni jako „fast“, protože „fast“ peery jsou používány mnohem častěji (client tunnels používají pouze fast peery). Výsledkem tohoto měření celkové propustnosti bylo, že pro ty dostatečně zatížené shromáždilo výborná data, ale dostatečně zatíženy byly jen fast peery a probíhalo jen málo efektivního průzkumu.

Použití jednominutových intervalů a propustnosti pro jednotlivý tunnel však zřejmě poskytuje rozumnější hodnoty. Tento algoritmus bude nasazen v příštím vydání.

* 3) Syndie blogs

Na základě zpětné vazby proběhla v rámci zobrazení blogu v Syndie další vylepšení, která mu dodávají výrazně odlišný charakter než vláknové zobrazení připomínající diskusní skupiny/fóra. Kromě toho získalo zcela novou možnost definovat obecné informace o blogu prostřednictvím stávající architektury Syndie. Jako příklad se podívejte na výchozí příspěvek na blogu „about Syndie“:  http://syndiemedia.i2p.net/blog.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&entry=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=/1132012800001

Tohle je jen drobný náznak toho, co všechno můžeme udělat. Další vydání vám umožní definovat vlastní logo vašeho blogu, vlastní odkazy (na blogy, příspěvky, přílohy, libovolné externí URL), a doufejme i ještě více možností přizpůsobení. Jednou z takových úprav jsou ikony pro jednotlivé tagy (štítky) - rád bych přibalil sadu výchozích ikon pro standardní tagy, ale lidé si budou moci definovat ikony pro své vlastní tagy pro použití ve svém blogu a dokonce nahradit výchozí ikony pro standardní tagy (opět, pouze když si lidé prohlížejí jejich blog, samozřejmě). Možná dokonce i nějaké nastavení stylu, aby se příspěvky s různými tagy zobrazovaly odlišně (samozřejmě by bylo povoleno jen velmi specifické přizpůsobení stylu - žádné libovolné CSS exploity v Syndie, děkujeme pěkně :).

Ještě je spousta věcí, které bych rád udělal se zobrazením blogu a které se do příštího vydání nedostanou, ale mělo by to být dobrým impulsem, aby lidé začali experimentovat s některými jeho možnostmi, což by vám všem, doufejme, umožnilo ukázat mi, co *vy* potřebujete, spíš než co si myslím, že chcete. Možná jsem dobrý programátor, ale špatný jasnovidec.

* 4) HTTP persistent connections

zzz je maniak, říkám vám. Došlo k určitému pokroku u dlouho požadované funkce – podpory trvalých HTTP spojení, která umožňuje posílat více HTTP požadavků přes jediný stream a na oplátku přijímat více odpovědí. Myslím, že o to někdo poprvé požádal před dvěma lety nebo tak nějak a mohlo by to dost pomoci některým typům eepsite(I2P Site) i při outproxyingu (používání outproxy k přístupu na clearnet). Vím, že práce ještě není hotová, ale jde to dopředu. Snad nám zzz během schůzky poskytne aktualizaci stavu.

* 5) I2Phex gwebcache

Dostaly se ke mně zprávy o pokroku při znovuzavedení podpory gwebcache do I2Phex, ale nevím, jak to v tuto chvíli vypadá. Možná nám k tomu může dnes večer Complication poskytnout aktualizaci?

* 6) ???

Jak vidíte, děje se toho hodně, ale jestli máte ještě něco, co byste chtěli nastolit a probrat, zaskočte za pár minut na schůzku a dejte vědět. Mimochodem, jeden fajn web, který v poslední době sleduju, je http://freedomarchive.i2p/ (pro lenochy bez nainstalovaného I2P můžete použít Tinoovo inproxy (vstupní proxy) přes http://freedomarchive.i2p.tin0.de/). Každopádně, uvidíme se za pár minut.

=jr
