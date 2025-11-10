---
title: "Stavové poznámky I2P k 2006-08-01"
date: 2006-08-01
author: "jr"
description: "Silný výkon sítě s vysokými přenosovými rychlostmi I2PSnarku, stabilitou transportu NTCP a upřesněními dosažitelnosti eepsite"
categories: ["status"]
---

Ahoj všichni, je čas na stručné poznámky před dnešní večerní schůzkou. Uvědomuji si, že můžete mít celou řadu otázek nebo záležitostí, které chcete otevřít, takže zvolíme volnější formát než obvykle. Nejprve je jen pár věcí, které chci zmínit.

* Network status

Zdá se, že síť si vede docela dobře, dokončují se roje poměrně velkých přenosů v I2PSnarku a na jednotlivých routerech se dosahuje poměrně značných přenosových rychlostí - viděl jsem 650KBytes/sec a 17,000 zapojených tunnels bez jakýchkoli problémů. Routery na spodním konci spektra si také vedou dobře, procházení eepsites(I2P Sites) a irc se 2 hop tunnels vyžaduje v průměru méně než 1KByte/sec.

Není to ale pro každého jen růžové, pracujeme však na aktualizaci chování routeru, aby byl výkon konzistentnější a lépe použitelný.

* NTCP

Nový transport NTCP ("nový" tcp) si po překonání počátečních dětských nemocí vede docela dobře. Abychom odpověděli na častý dotaz, z dlouhodobého hlediska budou v provozu jak NTCP, tak SSU - nevracíme se k režimu pouze TCP.

* eepsite(I2P Site) reachability

Pamatujte, že eepsites(I2P Sites) jsou dostupné jen tehdy, když je ten, kdo je provozuje, má spuštěné - když jsou vypnuté, nedá se k nim nijak dostat ;) Bohužel posledních pár dní nebyl orion.i2p dostupný, ale síť rozhodně pořád funguje - zkuste se třeba zajít na inproxy.tino.i2p nebo eepsites(I2P Sites).i2p pro vaše potřeby průzkumu sítě.

Každopádně se toho děje spousta, ale bylo by trochu předčasné to tady zmiňovat. Samozřejmě, pokud máte nějaké otázky nebo obavy, za pár minut se připojte na #i2p k naší *cough* týdenní vývojářské schůzce.

Děkujeme za vaši pomoc, která nás posouvá vpřed! =jr
