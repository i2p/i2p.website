---
title: "Stavové poznámky I2P k 2005-03-29"
date: 2005-03-29
author: "jr"
description: "Týdenní poznámky ke stavu vývoje I2P k vydání 0.5.0.5 s dávkováním, transportním protokolem UDP (SSU) a distribuovaným úložištěm Q"
categories: ["status"]
---

Ahoj všichni, je čas na týdenní statusové poznámky

* Index

1) 0.5.0.5 2) UDP (SSU) 3) Q 4) ???

* 1) 0.5.0.5

Protože jste všichni tak skvěle a rychle přešli na 0.5.0.4, nová verze 0.5.0.5 vyjde po schůzce. Jak jsme probírali minulý týden, velkou změnou je zahrnutí batching code (kód pro dávkové zpracování), který sdružuje více malých zpráv dohromady místo toho, aby každá měla vlastní plnohodnotnou 1KB zprávu v rámci tunnelu. Ačkoliv to samo o sobě nebude revoluční, mělo by to výrazně snížit počet předávaných zpráv i využitou šířku pásma, zejména u služeb jako IRC.

V oznámení o vydání bude více informací, ale s rev. 0.5.0.5 přicházejí ještě dvě důležité věci. Zaprvé ukončujeme podporu pro uživatele s verzemi staršími než 0.5.0.4 – na 0.5.0.4 je více než 100 uživatelů a u dřívějších vydání jsou značné problémy. Zadruhé je v novém sestavení důležitá oprava týkající se anonymity; i když by provedení souvisejícího útoku vyžadovalo určité vývojové úsilí, není nereálné. Většina změn se týká způsobu, jak spravujeme netDb – místo dosavadního ledabylého přístupu s kešováním záznamů všude možně budeme odpovídat na netDb požadavky pouze pro položky, které nám byly výslovně předány, bez ohledu na to, zda daná data máme či nikoli.

Jako vždy jsou součástí opravy chyb i některé nové funkce, ale další informace budou zveřejněny v oznámení o vydání.

* 2) UDP (SSU)

Jak jsme v posledních 6-12 měsících průběžně probírali, přejdeme na UDP pro naši komunikaci mezi routery, jakmile vyjde verze 0.6.  Abychom se na této cestě posunuli dál, máme v CVS k dispozici první návrh transportního protokolu na http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/udp.html?rev=HEAD

Je to poměrně jednoduchý protokol s cíli popsanými v dokumentu a využívá schopností I2P jak k autentizaci, tak k zabezpečení dat, přičemž zároveň odhaluje co nejméně externích informací. Ani první část handshaku při navazování spojení není identifikovatelná pro někoho, komu neběží I2P. Chování protokolu ještě není ve specifikaci plně definováno, například jak se spouštějí časovače nebo jak se používají tři různé polospolehlivé indikátory stavu, ale pokrývá základy šifrování, paketizace a NAT hole punching (prorážení NATu). Nic z toho zatím není implementováno, ale brzy bude, takže jakákoli zpětná vazba bude velmi vítána!

* 3) Q

Aum usilovně pracuje na Q(uartermaster), distribuovaném úložišti, a první verze dokumentace je k dispozici [1]. Jedním ze zajímavých nápadů se tam zdá být odklon od čisté DHT k systému ve stylu memcached [2], kde každý uživatel provádí veškeré vyhledávání zcela *lokálně* a skutečná data si vyžádá od serveru Q "přímo" (tedy přes I2P). Každopádně, pár pěkných věcí; možná, pokud je Aum vzhůru [3], z něj dokážeme vymámit nějakou aktualizaci?

[1] http://aum.i2p/q/ [2] http://www.danga.com/memcached/ [3] zatracená ta časová pásma!

* 4) ???

Děje se toho mnohem víc, a kdyby do schůzky zbývalo víc než jen pár minut, mohl bych pokračovat, ale takový je život.  Stavte se

# i2p in a few to chat.

=jr
