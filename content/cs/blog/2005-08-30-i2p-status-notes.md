---
title: "I2P Status Notes for 2005-08-30"
date: 2005-08-30
author: "jr"
description: "Týdenní aktualizace o stavu sítě ve verzi 0.6.0.3, včetně problémů s NAT, nasazení floodfill netDb a pokroku v mezinárodnění Syndie"
categories: ["status"]
---

Ahoj všichni, zase nastal ten čas týdne

* Index

1) Stav sítě 2) floodfill netDb 3) Syndie 4) ???

* 1) Net status

Verze 0.6.0.3 je venku už týden a zprávy jsou celkem dobré, i když pro některé bylo logování a zobrazení poněkud matoucí. Podle stavu před pár minutami I2P hlásí, že značný počet lidí má špatně nakonfigurované NATy nebo firewally - z 241 peerů se u 41 stav změnil na ERR-Reject, zatímco 200 bylo rovnou OK (když lze získat explicitní stav). To není dobré, ale pomohlo to lépe vymezit, co je potřeba udělat dál.

Od vydání došlo k několika opravám chyb pro dlouho přetrvávající chybové stavy, což posunulo aktuální CVS HEAD (hlavní větev CVS) na 0.6.0.3-4, která bude pravděpodobně vydána jako 0.6.0.4 později tento týden.

* 2) floodfill netDb

Jak bylo probíráno [1] na mém blogu [2], testujeme novou zpětně kompatibilní netDb, která řeší jak situaci s omezenými trasami, kterou pozorujeme (20 % routerů), tak i věci trochu zjednodušuje. floodfill netDb je nasazena jako součást 0.6.0.3-4 bez jakékoli další konfigurace a v zásadě funguje tak, že nejprve dotazuje floodfill db, než přejde zpět na existující kademlia db. Pokud to pár lidí chce pomoci vyzkoušet, přejděte na 0.6.0.3-4 a vyzkoušejte to!

[1] http://syndiemedia.i2p.net/index.jsp?selector=entry://ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=/1125100800001 [2] http://syndiemedia.i2p.net/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=

* 3) Syndie

Vývoj Syndie postupuje velmi dobře, přičemž plná vzdálená syndikace je v provozu a je optimalizována pro potřeby I2P (minimalizuje počet HTTP požadavků, místo toho sdružuje výsledky a nahrávaná data do multipart HTTP POST požadavků). Nová vzdálená syndikace znamená, že si můžete spustit vlastní lokální instanci Syndie, číst a publikovat offline, a pak později synchronizovat svou Syndie s instancí někoho jiného - stáhnout všechny nové příspěvky a nahrát všechny lokálně vytvořené příspěvky (buď hromadně, podle blogu, nebo podle příspěvku).

Jedním veřejným serverem Syndie je syndiemedia.i2p (na webu dostupný také na http://syndiemedia.i2p.net/) s veřejnými archivy na adrese http://syndiemedia.i2p/archive/archive.txt (nasměrujte na ni svůj uzel Syndie, aby se synchronizoval). Na 'front page' tohoto syndiemedia je ve výchozím nastavení filtrován pouze můj blog, ale ostatní blogy můžete stále otevřít přes rozbalovací nabídku a podle toho upravit své výchozí nastavení. (v průběhu času se výchozí nastavení syndiemedia.i2p změní na sadu úvodních příspěvků a blogů, což poskytne dobrý vstupní bod do syndie).

Jednou z probíhajících prací je internacionalizace kódové základny Syndie. Upravil jsem svou lokální kopii tak, aby správně fungovala s jakýmkoli obsahem (libovolná znaková sada / místní nastavení / atd.) na jakémkoli stroji (s potenciálně odlišnými znakovými sadami / místním nastavením / atd.), přičemž data poskytuje v čisté podobě tak, aby je prohlížeč uživatele dokázal správně interpretovat. Narazil jsem však na problémy s jednou komponentou Jetty, kterou Syndie používá, protože jejich třída pro práci s internacionalizovanými multipart požadavky není citlivá na znakové sady. Zatím ;)

Každopádně to znamená, že jakmile bude část kolem internacionalizace vyřešená, bude možné obsah a blogy zobrazovat i upravovat ve všech jazycích (ale samozřejmě zatím ne přeložené). Do té doby se ale může vytvořený obsah po dokončení internacionalizace rozbít (protože uvnitř podepsaných částí obsahu jsou řetězce v UTF-8). Ale klidně si zatím hrajte a experimentujte a snad to dodělám dnes večer nebo někdy zítra.

Také některé nápady, které jsou pro SML [3] stále na obzoru, zahrnují značku [torrent attachment="1"]můj soubor[/torrent], která by nabízela způsob na jedno kliknutí, jak lidem umožnit spustit přiložený torrent v jejich oblíbeném BT klientu (susibt, i2p-bt, azneti2p, nebo dokonce v ne-i2p bt klientu). Je poptávka po jiných druzích hooků (body pro napojení) (např. po značce [ed2k]?), nebo mají lidé úplně jiné bláznivé nápady, jak v Syndii šířit obsah?

[3] http://syndiemedia.i2p.net/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&entry=1124496000000

* 4) ???

Každopádně, děje se toho opravdu hodně, tak se za 10 minut připojte na setkání na irc://irc.{postman,arcturus,freshcoffee}.i2p/#i2p nebo na freenode.net!

=jr
