---
title: "Poznámky ke stavu I2P k 2005-04-26"
date: 2005-04-26
author: "jr"
description: "Stručná týdenní aktualizace zahrnující stabilitu sítě 0.5.0.7, pokrok v UDP transportu SSU s podporou více sítí a financování odměny za jednotkové testy"
categories: ["status"]
---

Ahoj všichni, dnes jen stručné týdenní poznámky ke stavu

* Index

1) Stav sítě 2) Stav SSU 3) Odměna za jednotkové testy 4) ???

* 1) Net status

Většina lidí poměrně rychle aktualizovala na verzi 0.5.0.7 vydanou minulý týden (díky!) a celkový výsledek se zdá pozitivní. Síť se jeví poměrně spolehlivá a dřívější omezování rychlosti u tunnel bylo vyřešeno. Stále se však objevují některé občasné problémy hlášené některými uživateli a ty nyní dohledáváme.

* 2) SSU status

Většinu času se soustředím na kód UDP pro verzi 0.6, a ne, není připraven k vydání, a ano, je tu pokrok ;) V tuto chvíli zvládá více sítí, přičemž některé uzly drží na UDP a jiné na TCP s docela rozumným výkonem. Nejtěžší je vypořádat se se všemi případy přetížení a konkurence o prostředky, protože živá síť bude pod stálou zátěží, ale za poslední den nebo tak se v tom udělal velký pokrok. Další novinky, až budou další novinky.

* 3) Unit test bounty

Jak duck zmínil na mailing listu [1], zab založil a počátečně financoval bounty (odměnu), aby pomohl I2P se sérií testovacích aktualizací - nějaké prostředky pro kohokoli, kdo dokáže splnit úkoly uvedené na stránce bounty [2]. Obdrželi jsme další příspěvky na tuto bounty [3] - aktuálně je na $1000USD. Ačkoli tyto bounties jistě nenabízejí "tržní sazbu", jsou malým povzbuzením pro vývojáře, kteří chtějí pomoci.

[1] http://dev.i2p.net/pipermail/i2p/2005-April/000721.html [2] http://www.i2p.net/bounty_unittests [3] http://www.i2p.net/halloffame

* 4) ???

Ok, zase jdu pozdě na schůzku... Měl bych to asi podepsat a rozeslat, co? Zaskoč na schůzku a můžeme probrat i další záležitosti.

=jr
