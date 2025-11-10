---
title: "Stavové poznámky k 2005-03-01"
date: 2005-03-01
author: "jr"
description: "Týdenní poznámky ke stavu vývoje I2P zahrnující chyby ve verzi 0.5.0.1 a nadcházející verzi 0.5.0.2, aktualizace plánu vývoje, editor adresáře a aktualizace i2p-bt"
categories: ["status"]
---

Ahoj všichni, je čas na naši aktualizaci stavu

* Index

1) 0.5.0.1 2) plán vývoje 3) editor adresáře a konfigurace 4) i2p-bt 5) ???

* 1) 0.5.0.1

Jak jsme probírali minulý týden, několik hodin po schůzce jsme vydali nové vydání 0.5.0.1, které opravovalo chyby v 0.5, jež způsobily, že se vytvářelo obrovské množství tunnels (mimo jiné). Obecně tato revize situaci zlepšila, ale při širším testování jsme narazili na další chyby, které postihly několik uživatelů. Zejména revize 0.5.0.1 může spotřebovávat značné množství CPU, pokud máte pomalý stroj nebo pokud tunnels vašeho routeru hromadně selžou, a některé dlouho běžící servery I2PTunnel mohou postupně spotřebovat RAM, až dojde k OOM (nedostatku paměti). Také se vyskytuje dlouhodobá chyba ve streamingové knihovně, kvůli níž se nám nemusí podařit navázat spojení, pokud nastane právě ta správná kombinace selhání.

Většina z nich (mimo jiné) byla opravena v cvs, ale některé stále zůstávají nevyřešené. Jakmile budou všechny opraveny, zabalíme to a vydáme jako verzi 0.5.0.2. Nejsem si úplně jistý, kdy to bude, doufejme, že tento týden, ale uvidíme.

* 2) roadmap

Po hlavních vydáních má roadmapa [1] tendenci se... upravovat.  Vydání 0.5 nebylo výjimkou.  Tato stránka odráží to, co považuji za rozumné a vhodné pro další postup, ale samozřejmě, pokud se připojí více lidí, aby s tím pomohli, lze ji jistě upravit.  Všimnete si výrazné pauzy mezi 0.6 a 0.6.1, a i když to sice odráží spoustu práce, odráží to také skutečnost, že se budu stěhovat (je to zase ten čas v roce).

[1] http://www.i2p.net/roadmap

* 3) addressbook editor and config

Detonate zahájil práce na webovém rozhraní pro správu položek knihy adres (hosts.txt) a vypadá to docela slibně. Možná bychom během setkání mohli získat aktualizaci od detonate?

Kromě toho smeghead v poslední době pracuje na webovém rozhraní pro správu konfigurace adresáře (soubory subscriptions.txt, config.txt). Možná bychom během schůzky mohli získat aktualizaci od smegheada?

* 4) i2p-bt

V oblasti i2p-bt došlo k pokroku: nová verze 0.1.8 řeší problémy s kompatibilitou azneti2p, jak bylo diskutováno na minulotýdenní schůzce. Možná bychom během schůzky mohli dostat aktualizaci od duck nebo smeghead?

Legion také vytvořil fork (odštěpenou větev) z i2p-bt rev, sloučil do něj další kód, některé věci opravil a na svém eepsite(I2P Site) má k dispozici binárku pro Windows. Oznámení [2] naznačuje, že by mohl být zpřístupněn zdrojový kód, i když v tuto chvíli není na eepsite(I2P Site) k dispozici. Vývojáři I2P kód tohoto klienta neauditovali (ani jej neviděli), takže ti, kdo potřebují anonymitu, si možná budou chtít nejdřív opatřit a prověřit kopii kódu.

[2] http://forum.i2p.net/viewtopic.php?t=382

There's also work on a version 2 of Legion's BT client, though I don't know the status of that.  Perhaps we can get an update from Legion during the meeting?

* 5) ???

To je asi vše, co teď mohu říct; děje se toho opravdu hodně. Pracuje někdo další na něčem, o čem bychom mohli během schůzky dostat aktualizaci?

=jr
