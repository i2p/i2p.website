---
title: "Stavové poznámky I2P k 2004-07-27"
date: 2004-07-27
author: "jr"
description: "Týdenní zpráva o stavu I2P věnovaná problémům s výkonem ve vydání 0.3.3 a nadcházejícím optimalizacím"
categories: ["status"]
---

Čau všichni, je čas na naši týdenní seanci nadávání

## Rejstřík:

1. 0.3.3 & current updates
2. NativeBigInteger
3. ???

## 1) 0.3.3

Minulý pátek jsme vydali verzi 0.3.3 a po dni či dvou dost hrbolaté jízdy se zdá, že si vede docela dobře. Ne tak dobře jako 0.3.2.3, ale obvykle se mi dařilo vydržet na irc.duck.i2p v blocích po 2-7h. Nicméně, protože jsem viděl, že spousta lidí má potíže, spustil jsem logger a podrobně sledoval, co se děje. Stručná odpověď je, že jsme jednoduše používali více šířky pásma, než je potřeba, což způsobovalo přetížení a selhání tunnelů (kvůli vypršení časového limitu testovacích zpráv apod.).

Posledních několik dní jsem byl zpět v simulátoru, spouštěl jsem sérii heartbeats (pravidelných testovacích signálů) napříč sítí, abych zjistil, co můžeme zlepšit, a na základě toho k nám míří celá řada aktualizací:

### netDb update to operate more efficiently

Stávající vyhledávací zprávy netDb mají až 10+KB a ačkoli úspěšné odpovědi jsou časté, neúspěšné odpovědi mohou mít až 30+KB (protože obě obsahovaly plné struktury RouterInfo). Nové netDb nahrazuje tyto plné struktury RouterInfo hashem routeru - čímž proměňuje 10KB a 30KB zprávy na zprávy o velikosti ~100 bajtů.

### throw out the SourceRouteBlock and SourceRouteReplyMessage

Tyto struktury byly pozůstatkem starého nápadu, ale nepřidávají žádnou hodnotu anonymitě ani bezpečnosti systému. Jejich vypuštěním ve prospěch jednodušší sady datových bodů odpovědi jsme dramaticky zmenšili velikost zpráv pro správu tunnel a zkrátili čas garlic encryption na polovinu.

### Aktualizace netDb pro efektivnější provoz

Kód byl během vytváření tunnelu trochu 'ukecaný', takže zbytečné zprávy byly odstraněny.

### Vyřaďte SourceRouteBlock a SourceRouteReplyMessage

Některé části kryptografického kódu pro garlic routing (způsob směrování používaný v I2P) používaly pevné vyplnění založené na některých technikách garlic routing, které nepoužíváme (když jsem to psal v září a říjnu, myslel jsem si, že budeme provádět víceskokový garlic routing místo tunnels).

Také pracuji na tom, abych zjistil, zda se mi podaří zavést plnohodnotnou aktualizaci směrování tunnelu, která přidá per-hop tunnel ids.

Jak můžete vidět z roadmapy, toto zahrnuje velkou část vydání 0.4.1, ale protože změna v netDb znamenala ztrátu zpětné kompatibility, můžeme rovnou udělat i řadu dalších zpětně nekompatibilních věcí naráz.

Pořád spouštím testy v simulátoru a musím zjistit, jestli stihnu dotáhnout tu věc s per-hop tunnel ID, ale doufám, že za den nebo dva vydám novou opravnou verzi. Nebude zpětně kompatibilní, takže přechod nebude úplně hladký, ale mělo by se to vyplatit.

## 2) NativeBigInteger

Iakin provádí nějaké aktualizace kódu NativeBigInteger pro tým Freenet, optimalizuje některé části, které nepoužíváme, ale také dává dohromady kód pro detekci CPU, který můžeme použít k automatickému výběru správné nativní knihovny. To znamená, že budeme moci nasadit jbigi jako jediný soubor knihovny ve výchozí instalaci a automaticky se vybere ta správná, aniž by bylo potřeba se uživatele na cokoli ptát. Také souhlasil s uvolněním svých úprav a nového kódu pro detekci CPU, abychom je mohli zahrnout do našeho zdrojového kódu (hurá, Iakin!). Nejsem si jistý, kdy to bude nasazeno, ale až to bude, dám lidem vědět, protože ti, kdo už mají existující knihovny jbigi, budou pravděpodobně potřebovat novou.

## 3) ???

No, poslední týden jsme byli hodně ponoření do hackování kódu, takže moc novinek není. Má někdo ještě něco, co by chtěl probrat? Pokud ano, zastavte se na dnešní schůzce ve 21:00 GMT na #i2p.

=jr
