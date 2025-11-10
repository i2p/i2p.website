---
title: "Poznámky ke stavu I2P ze dne 2005-01-25"
date: 2005-01-25
author: "jr"
description: "Týdenní poznámky o stavu vývoje I2P zahrnující pokrok v tunnel směrování ve verzi 0.5, portaci SAM na .NET, kompilaci pomocí GCJ a diskuse o UDP transportu"
categories: ["status"]
---

Ahoj všichni, krátká týdenní aktualizace stavu

* Index

1) stav verze 0.5 2) sam.net 3) pokrok v gcj 4) udp 5) ???

* 1) 0.5 status

Za uplynulý týden došlo ohledně 0.5 k velkému pokroku. Dříve probírané problémy se podařilo vyřešit, což výrazně zjednodušilo kryptografii a odstranilo problém se smyčkováním tunnelů.  Nová technika [1] byla implementována a jednotkové testy jsou připraveny.  Dále dávám dohromady další část kódu pro integraci těchto tunnels do hlavního routeru, poté vybuduji infrastrukturu pro správu a pooling tunnelů.  Jakmile to bude hotové, proženeme to simulátorem a následně i na paralelní síť, abychom to důkladně prověřili, než tomu dáme finální podobu a označíme to jako 0.5.

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/tunnel-alt.html?rev=HEAD

* 2) sam.net

smeghead dal dohromady nový port protokolu SAM pro .net - kompatibilní s c#, mono/gnu.NET (hurá, smeghead!). Je to v cvs v adresáři i2p/apps/sam/csharp/ s nant a dalšími nástroji - teď vy všichni .net vývojáři můžete začít hackovat s i2p :)

* 3) gcj progress

smeghead je rozhodně ve velkém tempu - podle posledního stavu se s několika úpravami router se kompiluje pod nejnovějším sestavením gcj [2] (w00t!). Pořád to ještě nefunguje, ale úpravy, které obcházejí zmatky gcj kolem některých konstrukcí vnitřních tříd, jsou rozhodně pokrok. Možná by nám smeghead mohl poskytnout aktualizaci?

[2] http://gcc.gnu.org/java/

* 4) udp

Tady toho není moc co říct, ale Nightblade na fóru vznesl zajímavou sadu obav [3] a ptal se, proč volíme UDP. Pokud máte podobné obavy nebo jiné návrhy, jak můžeme řešit problémy, které jsem zmínil ve své odpovědi, prosím, zapojte se!

[3] http://forum.i2p.net/viewtopic.php?t=280

* 5) ???

Jo, dobře, zase mám zpoždění s poznámkami, strhněte mi z platu ;)  Každopádně se toho děje hodně, tak se buď stavte na kanálu na schůzku, potom si přečtěte zveřejněné logy, nebo napište na list, pokud máte co říct.  Jo, a mimochodem, kapituloval jsem a spustil blog v rámci i2p [4].

=jr [4] http://jrandom.dev.i2p/ (klíč v http://dev.i2p.net/i2p/hosts.txt)
