---
title: "Poznámky ke stavu I2P k 2005-11-01"
date: 2005-11-01
author: "jr"
description: "Týdenní aktualizace zahrnující úspěšné vydání verze 0.6.1.4, analýzu bootstrapového útoku, bezpečnostní opravy v I2Phex 0.1.1.34, vývoj hlasové aplikace voi2p a integraci RSS kanálu do Syndie"
categories: ["status"]
---

Ahoj všichni, opět nadešel ten čas v týdnu

* Index

1) 0.6.1.4 a stav sítě 2) boostraps, předchůdci, globální pasivní protivníci a CBR 3) i2phex 0.1.1.34 4) aplikace voi2p 5) syndie a sucker 6) ???

* 1) 0.6.1.4 and net status

Zdá se, že vydání 0.6.1.4 z minulé soboty proběhlo docela hladce – 75 % sítě už aktualizovalo (díky!) a většina ze zbytku je stejně na 0.6.1.3. Zdá se, že všechno funguje docela dobře, a i když jsem k tomu moc ohlasů – ani pozitivních, ani negativních – neslyšel, předpokládám, že kdyby to bylo špatné, hlasitě byste si stěžovali :)

Zejména by mě zajímala jakákoli zpětná vazba od lidí s vytáčeným modemovým připojením, protože testování, které jsem provedl, je pouze základní simulací tohoto typu připojení.

* 2) boostraps, predecessors, global passive adversaries, and CBR

Na mailing listu proběhla spousta dalších diskusí o několika nápadech a online je zveřejněn souhrn bootstrap attacks (útoků při bootstrapu) [1]. Udělal jsem určitý pokrok ve specifikaci kryptografie pro variantu 3 a i když zatím nic nebylo zveřejněno, je to poměrně přímočaré.

[1] http://dev.i2p.net/pipermail/i2p/2005-October/001146.html

Proběhly další diskuse o tom, jak zlepšit odolnost vůči silným protivníkům pomocí constant bitrate (CBR) tunnels, a přestože máme možnost se touto cestou vydat, je to v současnosti plánováno až na I2P 3.0, protože jeho správné použití vyžaduje značné prostředky a pravděpodobně by mělo měřitelný dopad na to, kdo by byl ochoten používat I2P s takovou režií, stejně jako na to, které skupiny by toho vůbec byly či nebyly schopny.

* 3) I2Phex 0.1.1.34

Minulou sobotu také vyšla nová verze I2Phexu [2], která opravuje únik souborových deskriptorů, který by nakonec způsobil selhání I2Phexu (díky, Complication!) a odstraňuje část kódu, která by lidem umožňovala na dálku přikázat vaší instanci I2Phex, aby stahovala některé konkrétní soubory (díky, GregorK!). Aktualizaci důrazně doporučujeme.

Kromě toho došlo k aktualizaci CVS verze (dosud nevydané), která řeší některé problémy se synchronizací – Phex předpokládá, že některé síťové operace jsou zpracovány okamžitě, zatímco v I2P může jejich provedení nějakou dobu trvat :). To se projevuje tím, že se na chvíli zasekne GUI, stahování nebo odesílání se zastaví, případně jsou odmítána spojení (a možná i dalšími způsoby). Ještě to nebylo moc testováno, ale pravděpodobně to bude tento týden zařazeno do verze 0.1.1.35. Jsem si jistý, že až bude více novinek, na fóru se objeví další informace.

[2] http://forum.i2p.net/viewtopic.php?t=1143

* 4) voi2p app

Aum pilně pracuje na své nové aplikaci pro hlasovou (a textovou) komunikaci přes I2P, a i když jsem ji ještě neviděl, zní to slibně. Možná nám Aum na schůzce poskytne aktualizaci, nebo prostě trpělivě počkáme na první alfa verzi :)

* 5) syndie and sucker

dust už nějakou dobu pracuje na syndie a sucker a nejnovější sestavení I2P z CVS nyní umožňuje automaticky stahovat obsah z kanálů RSS a Atom a zveřejňovat jej na vašem syndie blogu. Momentálně musíte výslovně přidat lib/rome-0.7.jar a lib/jdom.jar do svého wrapper.config (wrapper.java.classpath.20 a 21), ale později to zahrneme do balíčku, takže to už nebude nutné. Stále se na tom pracuje a rome 0.8 (zatím nevydané) zřejmě nabídne pár skvělých věcí, například možnost stáhnout enclosures (přílohy v RSS) z kanálu, které pak bude moci sucker importovat jako přílohu k příspěvku v syndie (už teď si to ale poradí i s obrázky a odkazy!).

Jako u všech RSS kanálů se zdá, že existují určité nesrovnalosti v tom, jak je obsah začleněn, takže některé kanály se zpracují hladčeji než jiné. Myslím, že kdyby lidé pomohli otestovat to s různými kanály a dali dust vědět o jakýchkoli problémech, na kterých se to rozsype, mohlo by to být užitečné. Každopádně tohle vypadá dost slibně, pěkná práce, dust!

* 6) ???

To je pro tuto chvíli asi vše, ale pokud má někdo nějaké dotazy nebo chce některé věci dále probrat, doražte na schůzku ve 20:00 GMT (nezapomeňte na letní čas!).

=jr
