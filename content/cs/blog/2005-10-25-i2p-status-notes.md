---
title: "Poznámky ke stavu I2P k 2005-10-25"
date: 2005-10-25
author: "jr"
description: "Týdenní aktualizace zahrnující růst sítě na 400-500 peerů, integraci Fortuna PRNG, podporu nativní kompilace pomocí GCJ, odlehčený torrentový klient i2psnark a analýzu útoku typu tunnel bootstrap"
categories: ["status"]
---

Ahoj všichni, další novinky z první linie

* Index

1) Stav sítě 2) Integrace Fortuny 3) Stav GCJ 4) i2psnark se vrací 5) Více o bootstrappingu 6) Vyšetřování virů 7) ???

* 1) Net status

Uplynulý týden byl na síti docela dobrý – zdá se, že je vše poměrně stabilní, propustnost je normální a síť pokračuje v růstu do rozmezí 4–500 uzlů. Od vydání 0.6.1.3 došlo také k několika významným vylepšením a protože ovlivňují výkon a spolehlivost, očekávám, že později tento týden vydáme verzi 0.6.1.4.

* 2) Fortuna integration

Díky rychlé opravě Caseyho Marshalla [1] se nám podařilo integrovat pseudonáhodný generátor čísel Fortuna [2] z GNU-Crypto. To odstraňuje příčinu mnoha frustrací s blackdown JVM a umožňuje nám plynule pracovat s GCJ. Integrace Fortuny do I2P byla jedním z hlavních důvodů, proč smeghead vyvinul "pants" (což je 'portage' založený na 'ant'), takže jsme nyní zaznamenali další úspěšné použití pants :)

[1] http://lists.gnu.org/archive/html/gnu-crypto-discuss/2005-10/msg00007.html [2] http://en.wikipedia.org/wiki/Fortuna

* 3) GCJ status

Jak bylo zmíněno na listu [3], nyní můžeme spouštět router a většinu klientů bezproblémově pomocí GCJ [4]. Sama webová konzole zatím stále ještě nefunguje plně, takže si musíte provést konfiguraci routeru v router.config (i když by to mělo prostě fungovat a po zhruba minutě spustit vaše tunnels). Nejsem si úplně jistý, jak GCJ zapadne do našich plánů vydávání, ale momentálně se přikláním k tomu distribuovat čistou Javu, přičemž bychom podporovali jak variantu v Javě, tak i nativně kompilované verze. Je poněkud nepříjemné muset sestavovat a distribuovat spoustu různých sestavení pro různé operační systémy a verze knihoven apod. Má k tomu někdo silný názor?

Další pozitivní vlastností podpory GCJ je možnost používat streamingovou knihovnu z C/C++/Pythonu atd. Nevím, zda na takové integraci někdo pracuje, ale pravděpodobně by to stálo za to, takže pokud máte o práci v této oblasti zájem, dejte mi, prosím, vědět!

[3] http://dev.i2p.net/pipermail/i2p/2005-October/001021.html [4] http://gcc.gnu.org/java/

* 4) i2psnark returns

Zatímco i2p-bt byl prvním klientem BitTorrentu portovaným do I2P, který se hodně používal, eco byl ve skutečnosti první, kdo přišel s portem snarku [5] už před delší dobou. Ten bohužel neudržel aktuálnost ani kompatibilitu s ostatními anonymními BitTorrent klienty, takže na nějakou dobu tak trochu zmizel. Minulý týden jsem však měl potíže s výkonností někde v řetězci i2p-bt<->sam<->streaming lib<->i2cp, takže jsem sáhl po původním kódu snarku od mjw a udělal jednoduchý port [6], přičemž jsem nahradil všechna volání java.net.*Socket voláními I2PSocket*, InetAddresses za Destinations a URLs za volání EepGet. Výsledkem je drobný klient BitTorrentu pro příkazový řádek (po zkompilování asi 60 KB), který nyní budeme dodávat s vydáním I2P.

Ragnarok už se do toho pustil a začal do něj hackovat, aby vylepšil jeho algoritmus výběru bloků, a doufejme, že na to stihneme přidat jak webové rozhraní, tak i podporu více torrentů (multitorrent) ještě před vydáním verze 0.6.2. Pokud máte zájem pomoci, ozvěte se! :)

[5] http://klomp.org/snark/ [6] http://dev.i2p.net/~jrandom/snark_diff.txt

* 5) More on bootstrapping

V poslední době byla e‑mailová konference poměrně aktivní, a to díky Michaelovým novým simulacím a analýze budování tunnelů. Diskuse stále pokračuje a zaznělo v ní několik dobrých nápadů od Toad, Tom a polecat, tak se na ni podívejte, pokud chcete přispět k rozhodování o kompromisech u návrhových otázek souvisejících s anonymitou, které budeme pro vydání 0.6.2 přepracovávat [7].

Pro ty, kdo mají rádi pastvu pro oči, má Michael pro vás také řešení, a to simulaci toho, s jakou pravděpodobností vás útok dokáže identifikovat - jako funkci procenta sítě, které mají pod kontrolou [8], a jako funkci toho, jak aktivní je váš tunnel [9]

(Dobrá práce, Michaeli, díky!)

[7] http://dev.i2p.net/pipermail/i2p/2005-October/thread.html     (sledujte vlákno "i2p tunnel bootstrap attack") [8] http://dev.i2p.net/~jrandom/fraction-of-attackers.png [9] http://dev.i2p.net/~jrandom/messages-per-tunnel.png

* 6) Virus investigations

Proběhla určitá diskuse o potenciálních problémech se škodlivým softwarem, který je šířen spolu s určitou aplikací s podporou I2P, a Complication odvedl skvělou práci při jejich důkladném prozkoumání. Data jsou k dispozici, takže si můžete utvořit vlastní názor. [10]

Díky, Complication, za veškerý tvůj výzkum v této věci!

[10] http://forum.i2p.net/viewtopic.php?t=1122

* 7) ???

Jak vidíš, děje se toho opravdu hodně, ale protože už jdu pozdě na schůzku, asi bych to měl uložit a odeslat, co? Uvidíme se na #i2p :)

=jr
