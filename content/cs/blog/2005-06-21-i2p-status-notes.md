---
title: "Stavové poznámky I2P k 2005-06-21"
date: 2005-06-21
author: "jr"
description: "Týdenní aktualizace zahrnující návrat vývojáře z cest, pokrok v transportu SSU, dokončení bounty za jednotkové testy a výpadek služby"
categories: ["status"]
---

Ahoj všichni, je čas znovu spustit naše týdenní poznámky o stavu

* Index

1) Stav vývojáře 2) Stav vývoje 3) Odměna za jednotkové testy 4) Výpadek služby 5) ???

* 1) Dev[eloper] status

Po čtyřech městech ve čtyřech zemích se konečně usazuji a znovu se pouštím do kódu. Minulý týden jsem dal dohromady poslední díly k notebooku, už nespím po gaučích, a i když doma nemám přístup k internetu, v okolí je spousta internetových kaváren, takže přístup je spolehlivý (jen občasný a drahý).

To poslední znamená, že nebudu tak často viset na irc jako dřív, alespoň do podzimu (mám podnájem zhruba do srpna a budu hledat místo, kde budu mít 24/7 přístup k internetu). To ale neznamená, že toho nebudu dělat tolik - jen budu převážně pracovat na své vlastní testovací síti, vydávat sestavení pro testování na živé síti (a, ehm, no jo, i vydání). Znamená to však, že bychom možná měli přesunout některé diskuse, které dříve volně probíhaly na #i2p, na mailing list [1] a/nebo fórum [2] (pořád ale čtu backlog (historii zpráv) na #i2p). Zatím jsem nenašel rozumné místo, kam bych mohl chodit na naše vývojové schůzky, takže tento týden tam nebudu, ale možná do příštího týdne nějaké najdu.

Ale dost o mně.

[1] http://dev.i2p.net/pipermail/i2p/ [2] http://forum.i2p.net/

* 2) Dev[elopment] status

Zatímco jsem se stěhoval, pracoval jsem na dvou hlavních oblastech - na dokumentaci a na SSU transport (ten druhý teprve od chvíle, kdy jsem si pořídil notebook). Dokumentace je stále rozpracovaná: jeden pořádně velký, trochu děsivý přehled a k tomu řada menších dokumentů k implementaci (které pokrývají věci jako uspořádání zdrojového kódu, interakce mezi komponentami apod.).

Práce na SSU pokračují dobře – nová ACK bitová pole jsou nasazena, komunikace si účinně poradí se (simulovanými) ztrátami, přenosové rychlosti odpovídají různým podmínkám a podařilo se mi odstranit některé z ošklivějších chyb, na které jsem dříve narazil. Tyto změny dál testuji a až to bude vhodné, naplánujeme sérii živých testů v síti, pro které budeme potřebovat několik dobrovolníků. Více novinek v tomto směru přineseme, jakmile budou k dispozici.

* 3) Unit test bounty

Jsem rád, že mohu oznámit, že Comwiz přišel s řadou patchů, aby získal první fázi odměny za jednotkové testy [3]! Stále dolaďujeme některé drobné detaily patchů, ale obdržel jsem aktualizace a podle potřeby vygeneroval jak junit, tak i clover reporty. Očekávám, že patche budeme mít brzy v CVS, a v tu chvíli zveřejníme Comwizovu testovací dokumentaci.

Protože clover je komerční produkt (zdarma pro vývojáře OSS [4]), pouze ti, kdo mají nainstalovaný clover a obdrželi svou licenci pro clover, budou moci generovat clover reporty. V každém případě budeme clover reporty pravidelně zveřejňovat na webu, takže i ti, kdo nemají clover nainstalovaný, si stále mohou prohlédnout, jak si vede naše sada testů.

[3] http://www.i2p.net/bounties_unittest [4] http://www.cenqua.com/clover/

* 4) Service outage

Jak si mnozí pravděpodobně všimli, (alespoň) jeden z outproxy (výstupních proxy) je offline (squid.i2p), stejně jako www.i2p, dev.i2p, cvs.i2p a můj blog. Nejde o nesouvisející události - server, který je hostuje, je nefunkční.

=jr
