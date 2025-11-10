---
title: "Poznámky ke stavu I2P k 2006-01-17"
date: 2006-01-17
author: "jr"
description: "Stav sítě ve verzi 0.6.1.9, vylepšení kryptografie při vytváření tunnel a aktualizace rozhraní blogu Syndie"
categories: ["status"]
---

Ahoj všichni, zase je úterý

* Index

1) Stav sítě a 0.6.1.9 2) Kryptografie pro vytváření Tunnel 3) Syndie blogy 4) ???

* 1) Net status and 0.6.1.9

Po vydání 0.6.1.9 a aktualizaci 70% sítě se zdá, že většina zahrnutých oprav chyb funguje podle očekávání; podle hlášení nové profilování rychlosti vybírá některé dobré peery. Slyšel jsem o trvalé propustnosti na rychlých peerech přesahující 300KBps při 50-70% využití cpu, zatímco jiné routery jsou v rozmezí 100-150KBps, s postupným poklesem až k těm, které dosahují jen 1-5KBps. Stále však dochází k výrazné obměně identit routerů, takže se zdá, že oprava chyby, u které jsem si myslel, že ji sníží, nezabrala (nebo je ta obměna legitimní).

* 2) Tunnel creation crypto

Na podzim proběhla rozsáhlá diskuse o tom, jak naše tunnel vytváříme, a také o kompromisech mezi teleskopickým vytvářením tunnel ve stylu Toru a průzkumným vytvářením tunnel ve stylu I2P [1]. V průběhu toho jsme přišli s kombinací [2], která odstraňuje problémy teleskopického vytváření ve stylu Toru [3], zachovává jednosměrné výhody I2P a omezuje zbytečná selhání. Vzhledem k tomu, že se tehdy dělo spousta dalších věcí, byla implementace nové kombinace odložena, ale jelikož se nyní blíží vydání 0.6.2, během něhož stejně potřebujeme přepracovat kód pro vytváření tunnel, je čas to definitivně dořešit.

Nastínil jsem návrh specifikace pro nové šifrování pro tunnel a před pár dny jsem ho zveřejnil na svém syndie blogu, a po několika drobných změnách, které vyplynuly při skutečné implementaci, máme specifikaci pohromadě v CVS [4]. V CVS [5] je také základní kód, který to implementuje, i když zatím není napojený na skutečné budování tunnel. Pokud se někdo nudí, uvítal bych nějakou zpětnou vazbu ke specifikaci. Mezitím budu pokračovat v práci na novém kódu pro budování tunnel.

[1] http://dev.i2p.net/pipermail/i2p/2005-October/thread.html a     viz vlákna týkající se bootstrap útoků [2] http://dev.i2p.net/pipermail/i2p/2005-October/001064.html [3] http://dev.i2p.net/pipermail/i2p/2005-October/001057.html [4] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/                                tunnel-alt-creation.html?rev=HEAD [5] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/java/src/net/                        i2p/router/tunnel/BuildMessageTest.java

* 3) Syndie blogs

Jak již bylo zmíněno, toto nové vydání 0.6.1.9 přináší několik zásadních úprav rozhraní blogu Syndie, včetně nového stylování od cervantes a možnosti, aby si každý uživatel zvolil odkazy a logo svého blogu (např. [6]). Tyto odkazy vlevo můžete spravovat kliknutím na odkaz "configure your blog" na své profilové stránce, který vás přesměruje na http://localhost:7657/syndie/configblog.jsp.  Jakmile tam provedete změny, při dalším odeslání příspěvku do archivu budou tyto informace zpřístupněny ostatním.

[6] http://syndiemedia.i2p.net/     blog.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=

* 4) ???

Vzhledem k tomu, že už mám na schůzku 20 minut zpoždění, měl bych to asi vzít stručně. Vím, že se děje ještě pár dalších věcí, ale místo abych je tady vytahoval, ať se vývojáři, kteří je chtějí probrat, staví na schůzce a nadhodí to. Každopádně, to je pro teď vše, uvidíme se na #i2p!

=jr
