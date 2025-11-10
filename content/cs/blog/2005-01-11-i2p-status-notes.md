---
title: "Stavové poznámky I2P k 2005-01-11"
date: 2005-01-11
author: "jr"
description: "Týdenní poznámky o stavu vývoje I2P zahrnující stav sítě, pokrok ve verzi 0.5, stav verze 0.6, azneti2p, port pro FreeBSD a hosts.txt jako síť důvěry"
categories: ["status"]
---

Ahoj všichni, je čas na týdenní aktualizaci

* Index

1) Stav sítě 2) 0.5 pokrok 3) 0.6 stav 4) azneti2p 5) fbsd 6) hosts.txt jako WoT 7) ???

* 1) Net status

Celkově se síť chová dobře, i když jsme měli problémy s tím, že jeden z IRC serverů byl offline a můj outproxy (výstupní proxy) zlobil. Nicméně druhý IRC server byl (a stále je) k dispozici (i když momentálně nemá vypnuté CTCP - viz [1]), takže jsme si mohli ukojit chuť na IRC :)

[1] http://ugha.i2p/HowTo/IrcAnonymityGuide

* 2) 0.5 progress

Je tu pokrok, stále kupředu! Dobře, asi bych to měl trochu víc rozvést. Už mám konečně implementovanou a otestovanou novou kryptografii pro směrování v tunnelu (hurá!), ale během několika diskusí jsme našli místo, kde by mohlo docházet k úniku anonymity na jedné úrovni, takže se to upravuje (první hop by věděl, že je první hop, což je špatně. ale je to opravdu, opravdu snadné opravit). Každopádně doufám, že brzy aktualizuji a zveřejním dokumentaci a kód k tomu a dokumentaci k ostatnímu ohledně provozu tunnelu ve verzi 0.5 / poolování / atd. zveřejním později. Další novinky, až budou.

* 3) 0.6 status

(cože!?)

Mule zahájil zkoumání UDP transportu a čerpáme od zab jeho zkušenosti s UDP kódem LimeWire. Vypadá to velmi slibně, ale je před námi ještě hodně práce (a na roadmapě [2] je to stále ještě otázka několika měsíců).  Máte nějakou inspiraci nebo návrhy?  Zapojte se a pomozte to nasměrovat k tomu, co je třeba udělat!

[2] http://www.i2p.net/roadmap#0.6

* 4) azneti2p

Málem jsem se z toho počůral, když jsem tu informaci dostal, ale vypadá to, že lidi z Azureusu napsali I2P plugin (zásuvný modul), který umožňuje jak anonymní používání trackeru, tak anonymní přenos dat! Více torrentů funguje i v rámci jediné I2P destination (identifikátor cíle) a přímo používá I2PSocket, což umožňuje těsnou integraci se streamingovou knihovnou. Plugin azneti2p je s tímto vydáním 0.1 pořád v rané fázi a spousta optimalizací a zlepšení použitelnosti je na cestě, ale pokud vám nevadí si trochu ušpinit ruce, zastavte se na i2p-bt na I2P IRC sítích a přidejte se k té zábavě :)

Pro dobrodružné typy si stáhněte nejnovější azureus [3], podívejte se na jejich i2p návod [4] a stáhněte si zásuvný modul [5].

[3] http://azureus.sourceforge.net/index_CVS.php [4] http://azureus.sourceforge.net/doc/AnonBT/i2p/I2P_howto.htm [5] http://azureus.sourceforge.net/plugin_details.php?plugin=azneti2p

duck vyvíjí heroické úsilí, aby zachoval kompatibilitu s i2p-bt, a zatímco tohle píšu, v #i2p-bt probíhá horečnaté hackování, takže očekávejte nové vydání i2p-bt už opravdu brzy.

* 5) fbsd

Díky práci lioux je nyní ve FreeBSD Ports k dispozici port pro i2p [6].  Ačkoli neusilujeme o to, aby existovalo mnoho instalací specifických pro jednotlivé distribuce, slibuje, že jej bude udržovat aktuální, pokud o novém vydání dáme vědět s dostatečným předstihem.  To by mělo být užitečné pro uživatele FreeBSD-CURRENT - díky, lioux!

[6] http://www.freshports.org/net/i2p/

* 6) hosts.txt as WoT

Nyní, když vydání 0.4.2.6 obsahuje Ragnarokův adresář, je proces udržování vašeho hosts.txt naplněného novými záznamy v rukou každého uživatele.  A nejen to, na odběry adresáře můžete pohlížet jako na jednoduchou obdobu sítě důvěry - importujete nové záznamy z webu, kterému důvěřujete, aby vás seznamoval s novými destinacemi (výchozí jsou dev.i2p a duck.i2p).

S touto možností přichází zcela nový rozměr - možnost, aby si lidé zvolili, které weby si zahrnou do svého hosts.txt a které ne. Ačkoliv má své místo i veřejný, zcela neregulovaný přístup, k němuž v minulosti docházelo, nyní, když je systém pojmenování nejen teoreticky, ale i prakticky plně distribuovaný, si budou lidé muset stanovit vlastní zásady pro zveřejňování cizích Destinations (cílových adres v I2P).

To podstatné v pozadí je, že jde o příležitost k poučení pro komunitu I2P. Dříve jsme se s gottem snažili posunout vpřed otázku pojmenování tím, že jsme zveřejnili gottovu stránku jako jrandom.i2p (o tuto adresu požádal jako první on - já ne, a nad obsahem této URL nemám vůbec žádnou kontrolu). Nyní můžeme začít zkoumat, jak budeme zacházet se stránkami, které nejsou uvedeny v http://dev.i2p.net/i2p/hosts.txt ani na forum.i2p. To, že nejsou uvedeny na těchto místech, nijak nebrání provozu dané stránky - váš hosts.txt je jen váš místní seznam adres.

Každopádně, dost bylo řečí, chtěl jsem jen lidi upozornit, abychom všichni viděli, co je třeba udělat.

* 7) ???

Ty jo, to je spousta věcí. Rušný týden a nečekám, že to v dohledné době poleví. Tak se za pár minut zastav na schůzce a můžeme to probrat.

=jr
