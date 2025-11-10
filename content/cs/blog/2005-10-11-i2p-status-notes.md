---
title: "Poznámky o stavu I2P k 2005-10-11"
date: 2005-10-11
author: "jr"
description: "Týdenní aktualizace o úspěšném vydání 0.6.1.2, novém proxy I2PTunnelIRCClient pro filtrování nebezpečných IRC zpráv, Syndie CLI a převodu RSS na SML a plánech integrace I2Phex"
categories: ["status"]
---

Ahoj všichni, zase je úterý

* Index

1) 0.6.1.2 2) I2PTunnelIRCClient 3) Syndie 4) I2Phex 5) Steganografie a darknety (ohledně flamewaru) 6) ???

* 1) 0.6.1.2

Uvedení verze 0.6.1.2 z minulého týdne zatím proběhlo docela dobře - 75 % sítě se aktualizovalo, HTTP POST funguje bez problémů a streaming lib (streamovací knihovna) posílá data poměrně efektivně (úplná odpověď na požadavek HTTP je často přijata během jediné end-to-end zpáteční cesty). Síť také trochu narostla - stabilně je to kolem 400 uzlů, i když to během špičky zmínky na digg/gotroot [1] o víkendu vystřelilo ještě výš na 6-700 s obměnou uzlů.

[1] http://gotroot.com/tiki-read_article.php?articleId=195     (jo, fakt starý článek, já vím, ale někdo ho zase našel)

Od vydání verze 0.6.1.2 přibylo ještě několik dalších vylepšení – byla nalezena (a opravena) příčina nedávných netsplitů na irc2p, a také poměrně výrazná vylepšení v přenosu paketů v SSU (úspora více než 5 % paketů). Nejsem si jistý, kdy přesně vyjde 0.6.1.3, ale možná později tento týden. Uvidíme.

* 2) I2PTunnelIRCClient

Nedávno, po určité diskusi, dust rychle vytvořil nové rozšíření pro I2PTunnel - proxy "ircclient". Funguje tak, že filtruje obsah odesílaný a přijímaný mezi klientem a serverem přes I2P, odstraňuje nebezpečné zprávy IRC a přepisuje ty, které je vhodné upravit. Po několika testech to vypadá velmi dobře a dust jej přidal do I2PTunnel a nyní je nabízen uživatelům prostřednictvím webového rozhraní. Bylo skvělé, že lidé z irc2p upravili své IRC servery tak, aby zahazovaly nebezpečné zprávy, ale teď už na to nemusíme spoléhat - lokální uživatel má kontrolu nad vlastním filtrováním.

Použití je poměrně snadné - místo vytváření "Client proxy" pro IRC jako dříve jednoduše vytvořte "IRC proxy". Pokud chcete převést svůj stávající "Client proxy" na "IRC proxy", můžete (au) upravit soubor i2ptunnel.config, změnou "tunnel.1.type=client" na "tunnel.1.ircclient" (nebo jakékoli číslo, které je vhodné pro váš proxy server).

Pokud půjde vše dobře, bude v příštím vydání nastaven jako výchozí typ proxy I2PTunnel pro IRC připojení.

Dobrá práce, dust, díky!

* 3) Syndie

Zdá se, že Ragnarokova funkce plánované syndikace funguje dobře, a co vyšla verze 0.6.1.2, přibyly dvě nové funkce - přidal jsem nové zjednodušené CLI (rozhraní příkazového řádku) pro publikování v Syndie [2], a dust (hurá, dust!) dal dohromady kód, který vytáhne obsah z kanálu RSS/Atom, stáhne jakékoli přílohy či obrázky, na které se v něm odkazuje, a převede obsah RSS do SML (!!!) [3][4].

Důsledky kombinace těchto dvou by měly být jasné. Další novinky, až budou.

[2] http://syndiemedia.i2p/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&entry=1128816000000&expand=true [3] http://syndiemedia.i2p/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&entry=1128816000001&expand=true [4] http://dust.i2p/Sucker.java     (brzy to začleníme do CVS)

* 4) I2Phex

Podle všeho I2Phex funguje docela dobře, ale problémy v čase stále přetrvávají. Na fóru [5] proběhla určitá diskuse o tom, jak dál postupovat, a dokonce se ozval i GregorK, hlavní vývojář Phexu, který vyjádřil podporu integraci funkcionality I2Phex zpět do Phexu (nebo alespoň tomu, aby hlavní větev Phexu nabízela jednoduché pluginové rozhraní pro transportní vrstvu).

To by bylo vážně parádní, protože by to znamenalo mnohem méně kódu k údržbě, a navíc bychom využili práci týmu Phex na zlepšování kódové základny. Aby to ale fungovalo, potřebujeme, aby se ozvali nějací hackeři a ujali se vedení migrace. Kód I2Phex celkem jasně ukazuje, kde sirup věci měnil, takže by to nemělo být příliš těžké, ale nejspíš to nebude úplně triviální ;)

Teď se do toho opravdu nemůžu pustit, ale pokud chceš pomoct, zastav se na fóru.

[5] http://forum.i2p.net/viewforum.php?f=25

* 5) Stego and darknets (re: flamewar)

Mailing list [6] byla v poslední době poměrně aktivní, a to díky diskusi o steganografii a darknetech. Téma se z velké části přesunulo na Freenet tech list [7] s předmětem "I2P conspiracy theories flamewar", ale stále pokračuje.

Nejsem si jistý, že mám co dodat, co už není součástí samotných příspěvků, ale někteří lidé zmínili, že jim diskuse pomohla s pochopením I2P a Freenetu, takže by možná stálo za to si ji projít. Nebo taky ne ;)

[6] http://dev.i2p.net/pipermail/i2p/2005-October/thread.html [7] nttp://news.gmane.org/gmane.network.freenet.technical

* 6) ???

Jak vidíte, děje se spousta zajímavých věcí a určitě jsem něco vynechal. Zaskočte za pár minut na #i2p na naše týdenní setkání a pozdravte!

=jr
