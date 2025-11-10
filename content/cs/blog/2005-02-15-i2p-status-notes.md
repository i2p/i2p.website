---
title: "Poznámky ke stavu I2P ze dne 2005-02-15"
date: 2005-02-15
author: "jr"
description: "Týdenní poznámky o stavu vývoje I2P zahrnující růst sítě na 211 routerů, přípravy vydání 0.5 a i2p-bt 0.1.7"
categories: ["status"]
---

Dobrý den, je tu zase ta část týdne,

* Index

1) Stav sítě 2) Stav verze 0.5 3) i2p-bt 0.1.7 4) ???

* 1) Net status

Zatímco se v síti neobjevily žádné nové chyby, minulý týden jsme získali určitou pozornost na populárním francouzském p2p webu, což vedlo k nárůstu jak počtu uživatelů, tak i aktivity na BitTorrentu. V maximu jsme dosáhli 211 routers v síti, i když se to v poslední době pohybuje mezi 150 a 180. Nahlášené využití šířky pásma také vzrostlo, bohužel však spolehlivost irc klesla, protože jeden ze serverů snížil své limity šířky pásma kvůli zátěži. Proběhla řada vylepšení streamovací knihovny (streaming lib), která by s tím měla pomoci, ale jsou na větvi 0.5-pre, takže zatím nejsou dostupná na živé síti.

Dalším přechodným problémem byl výpadek jednoho z HTTP outproxy (výstupních proxy) (www1.squid.i2p), což způsobovalo, že 50 % požadavků přes outproxy selhalo. Tuto outproxy můžete dočasně odebrat tak, že otevřete svou konfiguraci I2PTunnel [1], upravíte eepProxy a změníte řádek "Outproxies:" tak, aby obsahoval pouze "squid.i2p". Doufejme, že tu druhou brzy zprovozníme, abychom zvýšili redundanci.

[1] http://localhost:7657/i2ptunnel/index.jsp

* 2) 0.5 status

Za uplynulý týden jsme na 0.5 udělali spoustu pokroku (vsadím se, že už vás to unavuje, co?). Díky pomoci postmana, cervantese, ducka, spaetze a nějaké nejmenované osoby už téměř týden provozujeme testovací síť s novým kódem a podařilo se nám vyřešit slušný počet chyb, které jsem na své lokální testovací síti neviděl.

Za poslední den či tak byly změny drobné a nečekám, že před vydáním verze 0.5 zbude ještě nějaká podstatná práce na kódu. Zbývá ještě trochu úklidu, dokumentace a sestavení a neuškodí nechat testovací síť 0.5 běžet, aby se případně časem odhalily další chyby. Protože to bude ZPĚTNĚ NEKOMPATIBILNÍ VYDÁNÍ, abyste měli čas naplánovat aktualizaci, stanovím jako termín vydání verze 0.5 TENTO PÁTEK.

Jak bla zmínil na IRC, provozovatelé eepsite(I2P Site) mohou zvážit odstavení svého webu ve čtvrtek nebo v pátek a nechat ho vypnutý až do soboty, kdy už mnoho uživatelů bude mít aktualizováno. To pomůže snížit účinek intersekčního útoku (např. pokud 90 % sítě přešlo na 0.5 a vy jste stále na 0.4, pak když se někdo dostane na vaše eepsite(I2P Site), bude vědět, že patříte mezi 10 % routers, které v síti zůstaly).

Mohl bych začít rozebírat, co bylo aktualizováno v 0.5, ale nakonec bych se rozepsal na stránky a stránky, takže to možná raději odložím a dám to do dokumentace, kterou bych měl sepsat :)

* 3) i2p-bt 0.1.7

duck dal dohromady vydání opravující chyby k aktualizaci 0.1.6, vydané minulý týden, a podle všeho je to pecka (možná až /moc/ velká pecka, vzhledem ke zvýšenému využití sítě ;)  Více informací na fóru i2p-bt [2]

[2] http://forum.i2p.net/viewtopic.php?t=300

* 4) ???

V diskusích na IRC a na fóru [3] se děje spousta dalších věcí, je toho příliš, než aby se to dalo stručně shrnout. Možná by zájemci mohli na schůzku zaskočit a dát nám aktuality a své postřehy? Každopádně, brzy na viděnou

=jr
