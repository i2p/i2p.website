---
title: "Poznámky ke stavu I2P k 2005-09-13"
date: 2005-09-13
author: "jr"
description: "Týdenní aktualizace zahrnující zprostředkování v SSU pro NAT hole punching (prorážení NAT), pokrok v programu odměn za jednotkové testy, diskusi o plánu vývoje klientské aplikace a odstranění režimu zaručeného doručení označeného jako zastaralý"
categories: ["status"]
---

Ahoj všichni, je čas na týdenní poznámky o stavu.

* Index

1) Stav sítě 2) SSU introductions / NAT hole punching (prorážení NATu) 3) Odměny 4) Pokyny pro klientskou aplikaci 5) ???

* 1) Net status

Stále jedeme s vydáním 0.6.0.5 v síti a téměř všichni už upgradovali; mnozí běží na některém z buildů od té doby (CVS HEAD je teď 0.6.0.5-9). Celkově vše stále funguje dobře, i když podle toho, co pozoruji, došlo k výraznému nárůstu síťového provozu, pravděpodobně kvůli vyššímu využívání i2p-bt nebo i2phex. Jeden z irc serverů měl včera v noci menší zádrhel, ale druhý to udržel v pohodě a zdá se, že se vše dobře zotavilo. Nicméně v CVS buildech došlo k podstatným vylepšením ve zpracování chyb i dalších funkcí, takže očekávám, že později v tomto týdnu bude nové vydání.

* 2) SSU introductions / NAT hole punching

Nejnovější sestavení v CVS zahrnují podporu pro dlouho diskutované SSU introductions [1], což nám umožňuje provádět decentralizované NAT hole punching (tj. techniku navázání spojení skrz NAT) pro uživatele za NATem nebo firewallem, který nemají pod kontrolou. Ačkoli si neporadí se symetrickým NATem, pokrývá většinu reálných případů. Zprávy z praxe jsou dobré, i když pouze uživatelé s nejnovějšími sestaveními mohou kontaktovat uživatele za NATem - starší sestavení musí čekat, až je daný uživatel kontaktuje jako první. Z tohoto důvodu vypustíme kód do vydání dříve než obvykle, abychom zkrátili dobu, po kterou budeme mít tyto omezené trasy v provozu.

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/udp.html?rev=HEAD#introduction

* 3) Bounties

Kontroloval jsem dnes dříve mailing list i2p-cvs a všiml jsem si spousty commitů od Comwize týkajících se zřejmě 3. fáze odměny za jednotkové testy [2]. Možná nám k tomu může Comwiz během dnešní večerní schůzky podat aktualizaci stavu.

[2] http://www.i2p.net/bounty_unittests

Mimochodem, díky podnětu anonymní osoby jsem trochu aktualizoval síň slávy [3], včetně dat o příspěvcích, sloučení více darů od jedné osoby dohromady a převodu na jednu měnu. Ještě jednou děkuji všem, kteří přispěli, a pokud je uvedena nesprávná informace nebo něco chybí, dejte prosím vědět a bude to aktualizováno.

[3] http://www.i2p.net/halloffame

* 4) Client app directions

Jednou z novějších úprav v aktuálních sestaveních CVS je odstranění staré formy doručování mode=guaranteed. Neuvědomil jsem si, že to ještě někdo používá (a je to zcela zbytečné, protože už rok máme plnohodnotnou streamingovou knihovnu), ale když jsem se vrtal v i2phex, všiml jsem si, že je ten příznak nastaven. S aktuálním sestavením (a všemi následujícími vydáními) bude i2phex používat pouze mode=best_effort, což by mělo zlepšit jeho výkon.

Můj záměr, proč to zmiňuji (kromě toho, že to uvádím kvůli uživatelům i2phex), je zeptat se, co byste všichni potřebovali na klientské straně I2P, a zda bych měl část svého času vyčlenit na pomoc s jejich naplněním. Jen tak z hlavy vidím spoustu práce v různých oblastech:  = Syndie: zjednodušené publikování, automatizovaná synchronizace, data    import, integrace aplikací (s i2p-bt, susimail, i2phex, atd.),    podpora vláken pro chování podobné fóru a další.  = eepproxy: zvýšená propustnost, podpora pipeliningu  = i2phex: obecná údržba (nepoužíval jsem ho dost na to, abych znal jeho    slabá místa)  = irc: lepší odolnost, detekce opakovaných výpadků irc serverů a    vyhýbání se nedostupným serverům, filtrování akcí CTCP lokálně místo na    serveru, DCC proxy  = Vylepšená podpora x64 s jbigi, jcpuid a service wrapperem  = integrace se systray (oznamovací oblast), a odstranění toho DOS okna  = Vylepšené řízení šířky pásma pro bursting (krátkodobé špičky)  = Vylepšené řízení zahlcení při přetížení sítě a CPU, stejně tak    i při obnově.  = Zpřístupnit více funkcí a zdokumentovat dostupné možnosti    router console pro aplikace třetích stran  = Dokumentace pro vývojáře klientů  = Úvodní dokumentace k I2P

A navíc, kromě toho všeho, je tu ještě zbytek věcí na roadmapě [4] a v seznamu úkolů [5]. Vím, co technicky potřebujeme, ale nevím, co potřebujete *vy* z uživatelského pohledu. Řekněte mi, co byste chtěli?

[4] http://www.i2p.net/roadmap [5] http://www.i2p.net/todo

* 5) ???

V jádru routeru a na straně vývoje aplikací se děje i pár dalších věcí nad rámec toho, co je uvedeno výše, ale ne všechno je v tuto chvíli připraveno k použití. Pokud má někdo něco, co by chtěl(a) probrat, zastavte se na setkání dnes večer ve 20:00 UTC na kanálu #i2p!

=jr
