---
title: "Poznámky ke stavu I2P k 2006-02-21"
date: 2006-02-21
author: "jr"
description: "Síťové problémy spojené s vydáním 0.6.1.10, rychlé následné vydání 0.6.1.11 a bezpečnostní obavy týkající se IE"
categories: ["status"]
---

Ahoj všichni, zase je tu úterý

* Index

1) Stav sítě 2) ???

* 1) Net status

Síť se s vydáním 0.6.1.10 potýkala s problémy, zčásti kvůli zpětné nekompatibilitě, ale také kvůli neočekávaným chybám. Ani spolehlivost, ani uptime (doba provozu bez výpadků) na 0.6.1.10 nebyly dostačující, takže během posledních 5 dní proběhla smršť záplat, která vyústila v nové vydání 0.6.1.11 - http://dev.i2p.net/pipermail/i2p/2006-February/001263.html

Většina chyb nalezených v 0.6.1.10 byla přítomna už od vydání 0.6 loni v září, ale nebyly snadno patrné, dokud bylo možné se uchýlit k alternativním transportům (TCP). Moje lokální testovací síť simuluje selhávání paketů, ale ve skutečnosti nepokrývala fluktuaci routerů a další přetrvávající selhání sítě. Testovací síť _PRE navíc zahrnovala samovýběrovou sadu poměrně spolehlivých peerů, takže existovaly podstatné situace, které nebyly před plným vydáním plně prozkoumány. To je samozřejmě problém a příště zajistíme, že zahrneme širší výběr scénářů.

* 2) ???

Momentálně se děje spousta věcí, ale nové vydání 0.6.1.11 se posunulo na první místo. Síť bude i nadále trochu nestabilní, dokud nebude mít velký počet lidí aktuální verzi, poté bude práce pokračovat dál. Za zmínku stojí, že cervantes pracuje na nějakém exploitu souvisejícím s bezpečnostní doménou v IE (Internet Exploreru), a i když si nejsem jistý, zda je připraven vysvětlit detaily, předběžné výsledky naznačují, že je to proveditelné, takže ti, kterým záleží na anonymitě, by se mezitím měli IE vyhýbat (ale to jste stejně věděli ;). Možná nám cervantes může na schůzce poskytnout shrnutí?

Každopádně, to je všechno, co teď můžu zmínit – za pár minut se stavte na schůzce a řekněte ahoj!

=jr
