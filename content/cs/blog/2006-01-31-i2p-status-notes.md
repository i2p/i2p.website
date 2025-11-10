---
title: "Stavové poznámky I2P k 2006-01-31"
date: 2006-01-31
author: "jr"
description: "Problémy se spolehlivostí sítě, nadcházející vydání 0.6.1.10 s novou kryptografií pro vytváření tunnelů, a zpětně nekompatibilní změny"
categories: ["status"]
---

Ahoj všichni, opět je tu úterý,

* Index

1) Stav sítě 2) Stav 0.6.1.10 3) ???

* 1) Net status

Během posledního týdne jsem zkoušel několik různých úprav, abych zvýšil spolehlivost vytváření tunnel na živé síti, ale zatím to nepřineslo průlom. V CVS sice došlo k poměrně zásadním změnám, ale nenazval bych je... stabilní. Obecně tedy doporučuji buď používat nejnovější vydání (0.6.1.9, v CVS označené jako i2p_0_6_1_9), nebo u nejnovějších sestavení používat nejvýše 1 hop (skok) tunnels. Na druhou stranu...

* 2) 0.6.1.10 status

Namísto toho, abych se donekonečna pral s drobnými úpravami, pracuji na své lokální testovací síti na migraci na novou kryptografii a nový proces vytváření tunnel [1]. To by mělo odstranit velkou část příčin selhání při vytváření tunnel, po čemž to můžeme v případě potřeby dále doladit.

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/                                tunnel-alt-creation.html?rev=HEAD

Jedním nešťastným vedlejším efektem je, že 0.6.1.10 nebude zpětně kompatibilní. Už dlouho jsme nevydali verzi, která by nebyla zpětně kompatibilní, ale v začátcích jsme to dělali docela často, takže by to neměl být příliš velký problém. V zásadě, až to bude skvěle fungovat na mé místní testovací síti, nasadíme to paralelně několika odvážlivcům pro rané testování, pak, až to bude připravené k vydání, prostě přepneme seed references na seeds (reseed servery) pro novou síť a pošleme to ven.

Nemám odhad termínu vydání 0.6.1.10, ale momentálně to vypadá docela dobře (většina délek tunnelů funguje, ale je tu pár větví, které jsem ještě neotestoval pod zátěží). Další informace samozřejmě až budou.

* 3) ???

To je asi všechno, co teď chci zmínit, i když vím, že ostatní na něčem pracují a mám ještě pár triků v rukávu na později; víc se dozvíme, až přijde čas. Každopádně, uvidíme se za pár minut!

=jr
