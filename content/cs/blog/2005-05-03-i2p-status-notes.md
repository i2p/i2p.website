---
title: "Poznámky ke stavu I2P k 2005-05-03"
date: 2005-05-03
author: "jr"
description: "Týdenní aktualizace o stabilitě sítě, úspěchu živého testování SSU UDP transportu, pokroku ve sdílení souborů v i2phex a nadcházející 3–4týdenní nepřítomnosti"
categories: ["status"]
---

Ahoj všichni, tento týden je toho na pořadu dne hodně

* Index

1) Stav sítě 2) Stav SSU 3) i2phex 4) nezvěstný 5) ???

* 1) Net status

V celkovém zdraví sítě nedošlo k žádným velkým změnám – situace se zdá být poměrně stabilní a i když máme občasné zádrhele, služby fungují dobře. Od posledního vydání proběhlo v CVS mnoho aktualizací, ale žádné opravy blokujících (kritických) chyb. Možná stihneme ještě jedno vydání před mým stěhováním, jen abychom dostali nejnovější změny z CVS dál, ale zatím si nejsem jistý.

* 2) SSU status

Už vás unavuje, jak pořád říkám, že na UDP transportu je spousta pokroku? Tak to máte smůlu – na UDP transportu je opravdu spousta pokroku. Během víkendu jsme se přesunuli z testování na privátní síti na živou síť a zhruba tucet routerů upgradovalo a zveřejnilo svou SSU address – díky čemuž jsou pro většinu uživatelů dosažitelné přes TCP transport, zatímco routery s povoleným SSU mohou komunikovat přes UDP.

Testování je stále v rané fázi, ale probíhalo mnohem lépe, než jsem očekával. Řízení zahlcení se chovalo velmi dobře a jak propustnost, tak latence byly zcela dostačující - dokázalo správně identifikovat skutečná omezení šířky pásma a efektivně sdílet tuto linku s konkurujícími TCP toky.

Na základě statistik shromážděných od ochotných dobrovolníků se ukázalo, jak důležitý je kód selektivního potvrzování pro správný provoz ve vysoce přetížených sítích. Posledních pár dní jsem strávil implementací a testováním tohoto kódu a aktualizoval jsem specifikaci SSU [1] tak, aby zahrnovala novou efektivní techniku SACK (selektivního potvrzování). Nebude zpětně kompatibilní se starším kódem SSU, takže lidé, kteří pomáhali s testováním, by měli deaktivovat transport SSU, dokud nebude připraveno nové sestavení k testování (doufejme během příštího dne či dvou).

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/udp.html?rev=HEAD

* 3) i2phex

sirup pilně pracuje na portu phexu na i2p a i když je ještě potřeba udělat spoustu práce, než to bude připravené pro běžného uživatele, už dnes večer se mi to podařilo spustit, procházet sdílené soubory uživatele sirup, stáhnout nějaká data a použít jeho *cough* "okamžité" chatovací rozhraní.

Na sirupově eepsite(I2P web) [2] je spousta dalších informací a pomoc s testováním od lidí, kteří už jsou v komunitě I2P, by byla skvělá (ale prosím, dokud to sirup neprohlásí za veřejné vydání a I2P nebude alespoň 0.6, ne-li 1.0, držme to v rámci komunity I2P). Věřím, že sirup bude na schůzce tento týden, takže možná získáme další informace!

[2] http://sirup.i2p/

* 4) awol

Když už je o tom řeč, pravděpodobně nebudu na příští týdenní schůzce a budu offline následující 3-4 týdny. Ačkoli to nejspíš znamená, že nevyjdou žádná nová vydání, pořád je spousta opravdu zajímavých věcí, na kterých může komunita pracovat:
 = aplikace jako feedspace, i2p-bt/ducktorrent, i2phex, fire2pe,
     addressbook, susimail, q, nebo něco úplně nového.
 = eepproxy - bylo by skvělé přidat filtrování, podporu pro
     trvalá HTTP spojení, 'listen on' ACLs (seznamy řízení přístupu), a možná
     exponential backoff (exponenciální zpožďování mezi pokusy) pro řešení outproxy (výstupní proxy) timeoutů (namísto
     prostého round robin)
 = PRNG (generátor pseudonáhodných čísel; jak bylo probíráno na mailing listu)
 = knihovna pro PMTU (Path MTU – maximální přenosová jednotka na trase) (buď v Javě, nebo v C s JNI)
 = odměna za unit testy a odměna za GCJ
 = profilování a ladění paměti routeru
 = a spousta dalšího.

Takže pokud se nudíte a chcete pomoci, ale chybí vám inspirace, možná vás něco z výše uvedeného povzbudí k akci. Nejspíš se občas zastavím v internetové kavárně, takže budu k zastižení e‑mailem, ale doba odezvy bude v řádu dnů.

* 5) ???

OK, to je asi všechno, co pro tuto chvíli chci probrat. Pro ty, kdo chtějí pomoci s testováním SSU během příštího týdne, sledujte informace na mém blogu [3]. A vy ostatní, uvidíme se na schůzce!

=jr [3] http://jrandom.dev.i2p/
