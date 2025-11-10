---
title: "Poznámky ke stavu I2P k 2005-03-15"
date: 2005-03-15
author: "jr"
description: "Týdenní poznámky o stavu vývoje I2P, které se zabývají analýzou výkonu sítě, vylepšeními ve výpočtu rychlosti a vývojem Feedspace"
categories: ["status"]
---

Ahoj všichni, je čas na týdenní aktualizaci

* Index

1) Stav sítě 2) Feedspace 3) ???

* 1) Net status

Za poslední týden jsem většinu času věnoval analýze chování sítě, sledování statistik a pokusům reprodukovat různé události v simulátoru. Zatímco některé z podivného chování sítě lze přičíst zhruba dvěma tuctům routers, které jsou stále na starších verzích, klíčovým faktorem je, že naše výpočty rychlosti nám neposkytují dobrá data – nejsme schopni správně identifikovat protějšky, které dokážou rychle přenášet data. V minulosti to nebyl velký problém, protože chyba způsobovala, že jsme jako 'fast' pool používali 8 protějšků s nejvyšší kapacitou, namísto vytváření legitimních úrovní odvozených z kapacity. Náš současný výpočet rychlosti vychází z periodického testu latence (konkrétně z RTT z tunnel testu), ale ten poskytuje nedostatečné množství dat, takže nemůžeme mít v tuto hodnotu důvěru. Potřebujeme tedy lepší způsob, jak získat více datových bodů, a přitom stále umožnit protějškům s 'high capacity', aby mohli být podle potřeby povyšeni do 'fast' úrovně.

Abych ověřil, že tohle je klíčový problém, kterému čelíme, trochu jsem to obešel a přidal funkci umožňující ručně vybrat, které peery se mají použít při výběru pro konkrétní pool tunnelů.  S těmi explicitně zvolenými peery jsem byl na IRC více než dva dny bez odpojení a u jiné služby, kterou spravuji, to mělo docela rozumný výkon.  Poslední asi dva dny zkouším nový kalkulátor rychlosti využívající některé nové statistiky a i když zlepšil výběr, pořád má některé problémy.  Dnes odpoledne jsem prošel několik alternativ, ale ještě je potřeba je vyzkoušet na síti.

* 2) Feedspace

Frosk zveřejnil další revizi dokumentace i2pcontent/fusenet, ale tentokrát na novém místě s novým názvem: http://feedspace.i2p/ – adresu najdete buď u orion [1], nebo na mém blogu [2]. Tohle vypadá opravdu slibně, jak z pohledu „hele, skvělá funkcionalita“, tak „hele, to pomůže anonymitě I2P“. Frosk a parta na tom makají, ale rozhodně hledají zpětnou vazbu (a pomoc). Možná bychom mohli Froska přemluvit, aby nám na schůzce dal aktualizaci?

[1] http://orion.i2p/#feedspace.i2p [2] http://jrandom.dev.i2p/

* 3) ???

OK, možná to nevypadá na nic moc, ale opravdu se toho hodně děje :) Určitě jsem taky některé věci vynechal, tak se stavte na schůzce a podívejte se, co se děje.

=jr
