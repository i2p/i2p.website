---
title: "Stavové poznámky I2P k 2005-02-08"
date: 2005-02-08
author: "jr"
description: "Týdenní poznámky ke stavu vývoje I2P zahrnující aktualizace 0.4.2.6, pokrok ve verzi 0.5 v oblasti tunnel s Bloomovými filtry, i2p-bt 0.1.6 a Fortuna PRNG"
categories: ["status"]
---

Ahoj všichni, zase je čas na aktualizaci

* Index

1) 0.4.2.6-* 2) 0.5 3) i2p-bt 0.1.6 4) fortuna 5) ???

* 1) 0.4.2.6-*

Nezdá se to, ale od vydání 0.4.2.6 už uplynul více než měsíc a věci jsou pořád v docela dobrém stavu. Od té doby proběhla řada dost užitečných aktualizací [1], ale nic, co by bylo zásadním problémem vyžadujícím vydat novou verzi. Nicméně během posledního dne či dvou nám přišly opravdu dobré opravy chyb (díky, anon a Sugadude!), a kdybychom zrovna nebyli na prahu vydání 0.5, asi bych to zabalil a pustil ven. Aktualizace od anon opravuje okrajovou podmínku ve streaming lib (streamovací knihovna), která způsobovala mnoho timeoutů viděných v BT (BitTorrent) a dalších velkých přenosech, takže pokud jste dobrodružné povahy, stáhněte si CVS HEAD (nejnovější větev) a zkuste to. Nebo samozřejmě počkejte na příští vydání.

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/history.txt?rev=HEAD

* 2) 0.5

Spousta, opravdu spousta pokroku směrem k verzi 0.5 (jak může dosvědčit kdokoli z mailing listu i2p-cvs [2]). Všechny aktualizace pro tunnel a různé optimalizace výkonu byly otestovány, a přestože to zatím mnoho nepokrývá, pokud jde o různé [3] algoritmy vynucující pořadí, základy jsou pokryty. Také jsme integrovali sadu (s licencí BSD) Bloomových filtrů [4] od XLattice [5], což nám umožňuje detekovat útoky typu replay bez nutnosti jakékoli paměťové režie na zprávu a s téměř 0ms režijní zátěží. Abychom vyhověli našim potřebám, filtry byly triviálně rozšířeny tak, aby časem zapomínaly, takže poté, co tunnel vyprší, filtr už neobsahuje IV (inicializační vektory), které jsme v daném tunnel zaznamenali.

Zatímco se snažím do vydání 0.5 zařadit tolik, kolik jen mohu, také si uvědomuji, že musíme počítat s neočekávaným - což znamená, že nejlepší způsob, jak to vylepšit, je dostat to do vašich rukou a poučit se z toho, jak to pro vás funguje (a nefunguje). Abychom tomu pomohli, jak jsem už zmínil, budeme mít vydání 0.5 (doufejme během příštího týdne), které poruší zpětnou kompatibilitu, a pak na tom budeme dál pracovat a vylepšovat to, přičemž vytvoříme vydání 0.5.1, až bude připravené.

Když se ohlédnu za roadmapou [6], jedinou věcí, která se přesouvá na 0.5.1, je striktní pořadí. Postupem času se jistě zlepší omezování (throttling) i vyvažování zátěže, ale očekávám, že to budeme ladit prakticky donekonečna. Probíraly se i další věci, které jsem doufal zahrnout do 0.5, jako nástroj pro stahování a kód pro aktualizaci jedním kliknutím, ale vypadá to, že i ty budou odloženy.

[2] http://dev.i2p.net/pipermail/i2p-cvs/2005-February/thread.html [3] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/                     tunnel-alt.html?rev=HEAD#tunnel.selection.client [4] http://en.wikipedia.org/wiki/Bloom_filter [5] http://xlattice.sourceforge.net/index.html [6] http://www.i2p.net/roadmap

* 3) i2p-bt 0.1.6

duck vydal novou verzi i2p-bt s opravami (hurá!), dostupnou na obvyklých místech, tak si ji pořiďte, dokud je čerstvá [7]. Mezi touto aktualizací a patchem pro streamingovou knihovnu od anona jsem při seedování několika souborů prakticky vytížil svůj uplink na maximum, tak to zkuste.

[7] http://forum.i2p.net/viewtopic.php?t=300

* 4) fortuna

Jak bylo zmíněno na minulotýdenní schůzce, smeghead v poslední době usilovně pracuje na celé řadě různých aktualizací a při snaze zprovoznit I2P s gcj se v některých JVM objevily opravdu hrozivé problémy s PRNG (generátor pseudonáhodných čísel), což nás v podstatě nutí k tomu, abychom měli PRNG, na který se můžeme spolehnout. Po odezvě od lidí z GNU-Crypto se zdá, že jejich implementace fortuna, ač zatím není reálně nasazená, nejlépe vyhovuje našim potřebám. Možná se nám ji podaří dostat do vydání 0.5, ale je pravděpodobnější, že se odloží na 0.5.1, protože ji budeme chtít doladit tak, aby nám poskytovala potřebné množství náhodných dat.

* 5) ???

Děje se toho hodně a v poslední době byl nával aktivity i na fóru [8], takže mi nejspíš leccos uniklo. Každopádně zaskočte na schůzku za pár minut a řekněte, co máte na srdci (nebo jen tiše lurkujte a občas přihodíte nějakou jízlivou poznámku).

=jr [8] http://forum.i2p.net/
