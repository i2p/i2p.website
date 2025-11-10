---
title: "Stavové poznámky I2P k 2006-02-07"
date: 2006-02-07
author: "jr"
description: "Pokrok v testování sítě PRE, optimalizace s krátkým exponentem pro ElGamalovo šifrování a I2Phex 0.1.1.37 s podporou gwebcache"
categories: ["status"]
---

Ahoj všichni, zase je tu úterý

* Index

1) Stav sítě 2) _PRE postup sítě 3) I2Phex 0.1.1.37 4) ???

* 1) Net status

Během uplynulého týdne nedošlo v živé síti k žádným podstatným změnám, takže se stav živé sítě příliš nezměnil.  Na druhou stranu...

* 2) _PRE net progress

Minulý týden jsem začal commitovat zpětně nekompatibilní kód pro vydání 0.6.1.10 do samostatné větve v CVS (i2p_0_6_1_10_PRE) a skupina dobrovolníků to pomohla otestovat. Tato nová _PRE síť nemůže komunikovat s živou sítí a neposkytuje žádnou smysluplnou anonymitu (protože je v ní méně než 10 uzlů). Díky záznamům pen register (záznamům metadat o připojeních) z těchto router se podařilo vysledovat a odstranit několik podstatných chyb jak v novém, tak i ve starém kódu, i když další testování a vylepšování pokračuje.

Jedním aspektem nové kryptografie pro vytváření tunnelu je, že tvůrce musí provést výpočetně náročné asymetrické šifrování pro každý skok předem, zatímco starší vytváření tunnelu provádělo šifrování jen tehdy, pokud předchozí skok souhlasil s účastí v tunnelu. Toto šifrování může trvat 400–1000 ms nebo více, v závislosti jak na místním výkonu CPU, tak na délce tunnelu (provádí plné šifrování ElGamalem pro každý skok). Jedna optimalizace aktuálně používaná na _PRE net je použití krátkého exponentu [1] - namísto použití 2048bit 'x' jako klíče šifry ElGamal používáme 228bit 'x', což je doporučená délka, aby odpovídala výpočetní náročnosti problému diskrétního logaritmu. To snížilo čas šifrování na jeden skok o řád, i když to neovlivňuje čas dešifrování.

Na používání krátkých exponentů panuje řada protichůdných názorů a v obecném případě to není bezpečné, ale podle toho, co se mi podařilo zjistit, jelikož používáme pevně dané bezpečné prvočíslo (Oakley group 14 [2]), řád q by měl být v pořádku. Pokud má však někdo v tomto duchu další postřehy, uvítám je.

Tou hlavní alternativou je přejít na 1024bitové šifrování (v jehož rámci bychom pak mohli případně použít 160bitový krátký exponent). To může být vhodné tak jako tak, a pokud bude 2048bitové šifrování na _PRE net příliš náročné, můžeme provést přechod už v rámci _PRE net. V opačném případě můžeme počkat až do vydání 0.6.1.10, kdy bude nová kryptografie nasazena ve větším měřítku, abychom zjistili, zda je to nutné. Pokud se takový přechod bude jevit jako pravděpodobný, bude následovat mnohem více informací.

[1] "O dohodě na klíči Diffie-Hellman s krátkými exponenty" -     van Oorschot, Weiner na EuroCrypt 96.  zrcadleno na     http://dev.i2p.net/~jrandom/Euro96-DH.ps [2] http://www.ietf.org/rfc/rfc3526.txt

Každopádně je na _PRE net spousta pokroku, přičemž většina související komunikace probíhá v kanálu #i2p_pre na irc2p.

* 3) I2Phex 0.1.1.37

Complication sloučil a upravil nejnovější kód I2Phexu tak, aby podporoval gwebcaches (GWebCache servery), kompatibilní s portem pycache od Rawna. To znamená, že uživatelé si mohou I2Phex stáhnout, nainstalovat, kliknout na "Connect to the network" a po minutě či dvou získá několik referencí na existující protějšky I2Phex a připojí se do sítě. Už žádné starosti s ruční správou souborů i2phex.hosts ani s ručním sdílením klíčů (w00t)! Ve výchozím stavu jsou k dispozici dva gwebcaches, ale lze je změnit nebo přidat třetí úpravou vlastností i2pGWebCache0, i2pGWebCache1 nebo i2pGWebCache2 v i2phex.cfg.

Dobrá práce, Complication a Rawn!

* 4) ???

To je prozatím asi vše, což je vlastně dobře, protože už jdu pozdě na schůzku :) Uvidíme se za chvilku na #i2p

=jr
