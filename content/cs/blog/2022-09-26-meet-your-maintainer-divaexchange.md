---
title: "Seznamte se se svým správcem: DivaExchange"
date: 2022-09-26
author: "sadie"
description: "Rozhovor s DivaExchange"
categories: ["general"]
API_Translate: pravda
---

*V tomto druhém pokračování série Meet Your Maintainer jsem oslovil Konrada z DIVA.EXCHANGE, abychom si promluvili o výzkumu a službách DIVA. DIVA.EXCHANGE vyvíjí software s cílem poskytovat bezplatnou bankovní technologii pro každého. Je bezpečný bez centrální infrastruktury a je založen na technologiích blockchain a I2P.*

**Co vás přimělo zajímat se o I2P?**

Před asi deseti lety jsem měl prezentaci pro "Technologieforum Zug" - velmi lokální technologickou síť pro lidi z byznysu. Představoval jsem jim I2P a Tor jako překryvné sítě - abych jim ukázal, že existují i další zajímavé věci.

Vždy mě velmi zajímaly technologie související s kryptografií. Obecně mohu říci, že mé klíčové zájmy byly a stále jsou: sítě, svoboda a soukromí na technické i společenské úrovni, zajímavé algoritmy, jako byl v letech 2000–2010 HashCash, což byl velmi dobře fungující Proof-of-Work (důkaz o práci) algoritmus vytvořený na univerzitách ve Spojeném království koncem 90. let.

I2P mě fascinovalo, protože je opravdu pečlivě udělané - od architektury až po implementaci v Javě a C++. Osobně dávám přednost odděleným a malým programům, které dělají jednu věc. Proto mě docela fascinovala verze v C++, I2Pd, která je úsporná, rychlá a bez závislostí. Funguje mi velmi dobře.

**Jaké rysy jeho technických možností byly v souladu s vaší vlastní prací nebo zájmy?**

Zbožňuji řemeslnost. To je umění. A I2P je moderní řemeslné umění. I2P vytváří pro koncové uživatele hodnoty, které nelze koupit: autonomii, svobodu a duševní klid.

I2P mě fascinuje, protože je agnostické. Kdokoli může na I2P provozovat cokoli, pokud to komunikuje přes TCP nebo UDP - a zvládá určitou latenci. Opravdu: "síť je počítač" a komunikace je podle současného stavu poznání skutečně soukromá.

**Pro koho je DIVA určena?**

DIVA se aktivně vyvíjí, a proto je projekt určen pro výzkumníky, softwarové vývojáře, odborníky na komunikaci (autory, ilustrátory…) a pro lidi, kteří se chtějí naučit opravdu nové věci v oblasti distribuovaných technologií.

Jakmile DIVA dospěje - prosím, neptejte se mě kdy - DIVA bude plně distribuovanou, samohostovanou bankou pro všechny.

**Můžete mi říct, co DIVA dělá?**

Jak už bylo řečeno, DIVA bude plně distribuovaná, samohostovaná banka pro každého. "Banking" znamená: spoření, platby, investice, půjčky – tedy vše, co lidé dělají každý den. V této souvislosti prosím vezměte na vědomí: DIVA funguje bez jakékoli centrální infrastruktury a DIVA nikdy - dokud k tomu budu mít co říct - nebude coin ani token. Nemůže v tom být zapojen žádný centrální obchodní model. Pokud transakce vytváří poplatky proto, že uzel distribuované infrastruktury odvedl nějakou práci, pak tyto poplatky zůstávají u uzlu, který tu práci vykonal.

Proč „banka“? Protože finanční svoboda a autonomie jsou klíčem k tomu, aby člověk žil dobrý a pokojný život a mohl svobodně činit všechna ta menší i větší každodenní rozhodnutí. Proto by lidé měli vlastnit své malé a bezpečné technologické součásti, aby mohli dělat cokoli, co chtějí, aniž by byli popostrkováni.

Tak tedy, seznamte se s DIVA, postavenou na I2P.

**Jaké jsou vaše nadcházející cíle? Jaké jsou vaše ambiciózní cíle?**

Bezprostředním cílem je porozumět dopadu protokolu SSU2, který byl nedávno implementován v I2P. Jde o technický cíl na několik příštích týdnů.

Pak, pravděpodobně ještě letos: nějaké kryptoměnové transakce s využitím DIVA na testnetech. Nezapomeňte prosím: DIVA je výzkumný projekt a lidé by měli být motivováni dělat si s DIVA vlastní věci - tak, jak to potřebují. Neprovozujeme žádnou infrastrukturu ani nic podobného pro ostatní, kromě několika transparentních testovacích sítí, abychom zvýšili znalosti a zkušenosti všech. Doporučujeme zůstat v kontaktu s DIVA prostřednictvím sociálních sítí ([@DigitalValueX](http://twitter.com/@DigitalValueX)) nebo chatů, abyste získali inspiraci, co s DIVA dělat.

Rád bych se také dotkl důležitého tématu pro komunitu I2P: DIVA je založena na divachain - a ta je pak založena na I2P. Divachain je velmi obecná, plně distribuovaná úložná vrstva. Takže, jen jako příklad: pokud si nějaký vývojář I2P myslí, že by plně distribuované DNS bez potřeby důvěry (trustless) bylo skvělým nápadem - pak je to další případ použití pro divachain. Plně distribuované - není potřeba důvěry - vše anonymní.

**Jaké další služby a příspěvky máte na starosti?**

DIVA.EXCHANGE - což je otevřené sdružení vyvíjející DIVA - provozuje už několik let reseed server pro I2P. Takže se s námi v minulosti pravděpodobně nějakým způsobem setkal téměř každý uživatel I2P. Jen poznámka: reseed server DIVA.EXCHANGE je k dispozici také jako .onion service - takže inicializaci I2P lze provést přes síť Tor - což je, alespoň z mého pohledu, při vstupu do sítě další vrstva ochrany.

DIVA také vytvořila knihovnu I2P SAM. Vývojáři tak mohou vytvářet libovolné moderní aplikace založené na I2P. Je na GitHubu a získává si stále větší popularitu: [github.com/diva-exchange/i2p-sam/](http://github.com/diva-exchange/i2p-sam/). Je kompletní, dobře zdokumentovaná a nabízí spoustu příkladů.

**Jaké priority by podle vás měl zvážit každý, kdo chce přispět do sítě I2P?**

Spusťte svůj I2P uzel. Podívejte se na různé varianty, například Docker verze I2Pd, případně jiné instalace dostupné pro různé operační systémy. K dispozici je několik variant a je důležité dobře zvládnout lokální instalaci a konfiguraci.

Pak se zamyslete nad svými dovednostmi – síťovými, programátorskými, komunikačními? I2P nabízí spoustu zajímavých výzev: lidé se síťovými dovednostmi mohou chtít provozovat reseed server – reseed servery jsou pro síť velmi důležité. Programátoři mohou pomoci s verzí I2P v Go, C++ nebo Javě. A komunikátoři jsou vždy potřeba: mluvit o I2P z objektivního a realistického pohledu velmi pomáhá. Každá drobnost se počítá.

V neposlední řadě: pokud jste výzkumník nebo student - prosím, obraťte se na nás prostřednictvím DIVA.EXCHANGE nebo na tým I2P - výzkumná práce je pro I2P důležitá.

**Jak nyní vnímáte diskusi a vyhlídky ohledně nástrojů, jako je I2P?**

Asi bych měl říct něco o vyhlídkách: I2P je důležité pro každého. Doufám, že komunita I2P - vývojáři, komunikátoři, atd. - zůstane motivovaná díky těm několika, kteří hluboce oceňují jejich tvrdou práci na skutečně náročné technologii.

Doufám, že stále více vývojářů uvidí přínos v tom vyvíjet software založený na I2P. To by vytvořilo více způsobů využití pro koncové uživatele.

**Můžete mi trochu popsat svůj pracovní postup v I2P? Jaké jsou vaše vlastní případy užití?**

Jsem vývojář, tester a výzkumník. Proto potřebuji mít všechno v kontejnerech, abych zůstal flexibilní. I2Pd běží v 1..n kontejnerech na více systémech a slouží například k obsluze požadavků na reseed, k provozu testovacího webu diva.i2p, k provozu částí testovací sítě DIVA I2P - viz testnet.diva.exchange, a také mám kontejnery, které slouží mým lokálním prohlížečům jako kombinovaný proxy server pro I2P a Tor.

**Jak může komunita I2P podpořit vaši práci?**

Jsme na sociálních sítích, například [@DigitalValueX](http://twitter.com/@DigitalValueX) - sledujte nás tam. Kromě toho bychom rádi viděli ještě větší zapojení na [github.com/diva-exchange](http://github.com/diva-exchange) - v posledních měsících to už získávalo čím dál větší pozornost. Za to moc děkujeme!
