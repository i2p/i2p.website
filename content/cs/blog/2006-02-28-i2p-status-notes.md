---
title: "Poznámky ke stavu I2P k 2006-02-28"
date: 2006-02-28
author: "jr"
description: "Vylepšení sítě v 0.6.1.12, roadmapa k 0.6.2 s novými strategiemi výběru peerů a příležitosti pro miniprojekty"
categories: ["status"]
---

Ahoj všichni, je zase čas na naše úterní nadávání

* Index

1) Stav sítě a 0.6.1.12 2) Cesta k 0.6.2 3) Miniprojekty 4) ???

* 1) Net status and 0.6.1.12

Uplynulý týden přinesl v síti výrazná zlepšení, nejprve díky rozsáhlému nasazení 0.6.1.11 minulé úterý, následovanému pondělním vydáním 0.6.1.12 (které bylo dosud nasazeno na 70 % sítě - díky!)  Celkově je vše výrazně lepší než u 0.6.1.10 i starších vydání - míra úspěšnosti sestavení tunnel je o celý řád vyšší i bez jakýchkoli záložních tunnel, latence klesla, využití CPU kleslo a propustnost vzrostla.  Kromě toho se se zcela vypnutým TCP míra retransmisí paketů drží pod kontrolou.

* 2) Road to 0.6.2

V kódu pro výběr peerů je stále prostor pro zlepšení, protože stále vidíme 10-20% míru odmítnutí u klientských tunnels a tunnels s vysokou propustností (10+KBps) nejsou tak běžné, jak by měly být. Na druhou stranu, nyní, když je zatížení CPU mnohem nižší, mohu spustit další router na dev.i2p.net, aniž bych způsobil problémy pro svůj primární router (který obsluhuje squid.i2p, www.i2p, cvs.i2p, syndiemedia.i2p a další, s přenosem 2-300+KBps).

Navíc zkouším některá vylepšení pro lidi na silně přetížených sítích (cože, chcete říct, že jsou i lidé, kteří na nich nejsou?). Vypadá to, že v tomto směru je určitý pokrok, ale bude třeba více testování. To by, doufám, mělo pomoci těm 4 nebo 5 lidem na irc2p, kteří zjevně mají potíže udržet spolehlivá spojení (a samozřejmě i těm, kteří tiše trpí stejnými potížemi).

Až to bude dobře fungovat, pořád nás čeká nějaká práce, než tomu budeme moci říkat 0.6.2 - potřebujeme nové strategie řazení uzlů, navíc k těmto vylepšeným strategiím výběru uzlů.  Jako základ bych rád získal tři nové strategie - = přísné řazení (omezující předchůdce a následníka každého uzlu,   s rotací podle MTBF) = pevně dané krajní body (použití pevně určeného uzlu jako vstupní brány a   výstupního koncového bodu) = omezený soused (použití omezené sady uzlů jako prvního vzdáleného   skoku)

Existují i další zajímavé strategie, které je třeba ještě dořešit, ale ty tři jsou nejdůležitější.  Jakmile budou implementovány, budeme funkčně kompletní pro 0.6.2.  Neurčitá ETA: březen/duben.

* 3) Miniprojects

Je tu víc užitečných věcí k udělání, než bych dokázal spočítat, ale jen vás chci upozornit na příspěvek na svém blogu, který popisuje pět malých projektů, které by programátor mohl rychle dát dohromady, aniž by do toho investoval příliš času [1]. Pokud by se do nich někdo chtěl pustit, jsem si jistý, že bychom jako poděkování vyčlenili nějaké prostředky [2] z obecného fondu, i když chápu, že většinu z vás žene spíš hack (samotné hackování) než peníze ;)

[1] http://syndiemedia.i2p.net:8000/blog.jsp?     blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&     entry=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=/1140652800002 [2] http://www.i2p.net/halloffame

* 4) ???

Každopádně, to je rychlé shrnutí toho, co se děje, pokud vím. Gratulace také cervantesovi k pětistému uživateli fóra, mimochodem :) Jako vždy se za pár minut stavte na #i2p na setkání!

=jr
