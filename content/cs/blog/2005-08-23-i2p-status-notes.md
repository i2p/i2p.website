---
title: "Stavové poznámky I2P k datu 2005-08-23"
date: 2005-08-23
author: "jr"
description: "Týdenní aktualizace zahrnující vylepšení ve verzi 0.6.0.3, stav sítě Irc2P, webové rozhraní susibt pro i2p-bt a zabezpečené blogování v Syndie"
categories: ["status"]
---

Ahoj všichni, zase nastal čas na týdenní statusové poznámky.

* Index

1) 0.6.0.3 stav 2) IRC stav 3) susibt 4) Syndie 5) ???

* 1) 0.6.0.3 status

Jak bylo nedávno zmíněno [1], je venku nové vydání 0.6.0.3, připravené pro vaše potěšení. Je to výrazné zlepšení oproti vydání 0.6.0.2 (není neobvyklé vydržet na irc několik dní bez odpojení - mně upgrade přerušil pětidenní dobu běhu), ale je tu pár věcí, které stojí za zmínku. Přesto to není vždy tak - lidé s pomalým připojením k síti narážejí na potíže, ale je to pokrok.

Jedna (velmi) častá otázka se objevila ohledně kódu peer testu-"Proč to ukazuje Status: Unknown?" Unknown je *naprosto v pořádku* - NENÍ to známkou problému. Také, pokud někdy vidíte, že to přeskakuje mezi "OK" a "ERR-Reject", neznamená to, že je to v pořádku - pokud se vám kdykoli objeví ERR-Reject, velmi pravděpodobně máte problém s NATem nebo firewallem. Vím, že je to matoucí a později vyjde verze s přehlednějším zobrazením stavu (a automatickým řešením, kdykoli to bude možné), ale prozatím se nedivte, když vás budu ignorovat, když řeknete "omg je to rozbité!!!11 status je Unknown!" ;)

(Příčina nadbytku hodnot stavu Unknown je v tom, že ignorujeme peer testy, v nichž je "Charlie" [2] někým, s kým už máme relaci SSU, protože to znamená, že by se dokázal dostat skrz náš NAT, i kdyby byl náš NAT nefunkční)

[1] http://dev.i2p.net/pipermail/i2p/2005-August/000844.html [2] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/udp.html?rev=HEAD#peerTesting

* 2) IRC status

Jak bylo uvedeno výše, operátoři Irc2P odvedli skvělou práci se svou sítí, protože latence je výrazně nižší a spolehlivost výrazně vyšší - už několik dní jsem neviděl netsplit (rozpojení sítě). Je tam také nový irc server, takže jich máme 3 - irc.postman.i2p, irc.arcturus.i2p a irc.freshcoffee.i2p. Možná by nám někdo z Irc2P mohl během schůzky poskytnout aktualizaci o pokroku?

* 3) susibt

susi23 (známá díky susimailu) je zpět s dvojicí nástrojů souvisejících s BT - susibt [3] a nový tracker bot [4]. susibt je webová aplikace (triviálně nasaditelná ve vaší i2p instanci Jetty) pro správu provozu i2p-bt. Jak se píše na jejím webu:

SusiBT je webové rozhraní pro i2p-bt. Integruje se do vašeho i2p   routeru a umožňuje automatické nahrávání i stahování, obnovování po   restartu a některé funkce správy, jako je nahrávání a stahování   souborů. Pozdější verze aplikace budou podporovat automatické   vytváření a nahrávání torrentových souborů.

[3] http://susi.i2p/?page_id=31 [4] http://susi.i2p/?p=33

Můžu slyšet "w00t"?

* 4) Syndie

Jak bylo zmíněno na mailing listu a na kanálu, máme novou klientskou aplikaci pro bezpečné a autentizované blogování / distribuci obsahu. Se Syndie otázka "is your eepsite(I2P Site) up" odpadá, protože si můžete obsah přečíst i tehdy, když je web nedostupný, a zároveň se Syndie vyhýbá všem nepříjemným problémům vlastní povaze sítí pro distribuci obsahu tím, že se soustředí na frontend. Každopádně je to pořád hodně ve vývoji, ale pokud se lidé chtějí zapojit a vyzkoušet si to, je k dispozici veřejný Syndie uzel na http://syndiemedia.i2p/ (dostupný také na webu na http://66.111.51.110:8000/). Klidně tam běžte a založte si blog, nebo pokud máte dobrodružnou náladu, napište na blog nějaké komentáře/návrhy/připomínky! Samozřejmě jsou vítány patche, stejně tak i návrhy na funkce, takže do toho.

* 5) ???

Říct, že se teď děje spousta věcí, je trochu slabé vyjádření... Kromě výše uvedeného pracuju na několika vylepšeních řízení zahlcení v SSU (-1 už je v cvs), na našem omezovači šířky pásma a na netDb (kvůli občasné nedostupnosti některých stránek), a také ladím problém s CPU nahlášený na fóru. Jsem si jistý, že i ostatní pracují na nějakých parádních věcech, o kterých bude co říct, takže snad se dnes večer zastaví na schůzku a pořádně se rozmluví :)

Každopádně, uvidíme se dnes večer ve 20:00 GMT na kanálu #i2p na obvyklých serverech!

=jr
