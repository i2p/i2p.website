---
title: "Možnosti Zprávy o Výstavbě Tunelu"
number: "143"
author: "zzz"
created: "2018-01-14"
lastupdated: "2022-01-28"
status: "Zamítnuto"
thread: "http://zzz.i2p/topics/2500"
toc: true
---

## Poznámka
Tento návrh nebyl implementován tak, jak bylo specifikováno,
nicméně dlouhé a krátké zprávy o výstavbě ECIES (návrhy 152 a 157)
byly navrženy s rozšiřitelnými poli možností.
Viz [specifikace Tunnel Creation ECIES](/docs/specs/implementation/#tunnel-creation-ecies) pro oficiální specifikaci.


## Přehled

Přidat flexibilní a rozšiřitelný mechanismus pro volby v I2NP Záznamech o Výstavbě Tunelu,
které jsou obsaženy ve Zprávách o Výstavbě Tunelu a Odpovědích na Výstavbu Tunelu.


## Motivace

Existuje několik předběžných, nezveřejněných návrhů na nastavení možností nebo konfigurace ve Zprávě o Výstavbě Tunelu,
takže tvůrce tunelu může předat některé parametry každému skoku tunelu.

V TBM je 29 volných bajtů. Chceme zachovat flexibilitu pro budoucí vylepšení, ale také využít prostor moudře.
Použití konstrukce 'mapování' by použilo alespoň 6 bajtů na možnost ("1a=1b;").
Pevné definování více polí možností by mohlo později způsobit problémy.

Tento dokument navrhuje nový, flexibilní systém mapování možností.


## Návrh

Potřebujeme reprezentaci možností, která je kompaktní a přesto flexibilní, abychom mohli umístit více
možností různé délky do 29 bajtů.
Tyto možnosti zatím nejsou definovány a není nutné je nyní definovat.
Nepoužívejte strukturu "mapování" (která kóduje Java Properties objekt), je příliš plýtvavá.
Použijte číslo k označení každé možnosti a délky, což má za následek kompaktní, ale flexibilní kódování.
Možnosti musí být registrovány podle čísla v našich specifikacích, ale také rezervujeme rozsah pro experimentální možnosti.


## Specifikace

Předběžné - několik alternativ je popsáno níže.

To by bylo přítomné pouze v případě, že bit 5 ve vlajkách (bajt 184) je nastaven na 1.

Každá možnost je dvoubajtové číslo možnosti a délka, následována bajty délky hodnoty možnosti.

Možnosti začínají na bajtu 193 a pokračují nejvýše po poslední bajt 221.

Číslo/délka možnosti:

Dva bajty. Bity 15-4 jsou 12bitové číslo možnosti, 1 - 4095.
Bity 3-0 jsou počet bajtů hodnoty možnosti, které budou následovat, 0 - 15.
Boolovská možnost by mohla mít nula bajtů hodnoty.
Budeme udržovat registr čísel možností v našich specifikacích a také definujeme rozsah pro experimentální možnosti.

Hodnota možnosti má 0 až 15 bajtů, které mají být interpretovány čímkoliv, co tu možnost potřebuje. Neznámá čísla možností by měla být ignorována.

Možnosti jsou uzavřeny číslem/délkou možnosti 0/0, což znamená dva 0 bajty.
Zbytek z 29 bajtů, pokud vůbec, by měl být vyplněn náhodným polstrováním, jako obvykle.

Toto kódování nám poskytuje prostor pro 14 0bajtových možností, nebo 9 1bajtových možností, nebo 7 2bajtových možností.
Alternativou by bylo použít pouze jeden bajt pro číslo/délku možnosti,
možná s 5 bity pro číslo možnosti (max 32) a 3 bity pro délku (max 7).
To by zvýšilo kapacitu na 28 0bajtových možností, 14 1bajtových možností, nebo 9 dvoubajtových možností.
Můžeme také udělat to variabilním, kde 5bitové číslo možnosti 31 znamená přečíst dalších 8 bitů pro číslo možnosti.

Pokud tunelová zastávka potřebuje vrátit možnosti tvůrci, můžeme použít stejný formát v zprávě o odpovědi na výstavbu tunelu,
předponěný nějakým magickým číslem několika bajtů (protože nemáme definovaný vlajkový bajt k indikaci, že možnosti jsou přítomny).
V TBRM je 495 volných bajtů.


## Poznámky

Tyto změny se týkají Záznamů o Výstavbě Tunelu, a tak mohou být použity ve všech typech Zpráv o Výstavbě -
Žádost o Výstavbu Tunelu, Žádost o Variabilní Výstavbu Tunelu, Odpověď na Výstavbu Tunelu a Odpověď na Variabilní Výstavbu Tunelu.


## Migrace

Nepoužitý prostor v Záznamech o Výstavbě Tunelu je vyplněn náhodnými daty a aktuálně ignorován.
Prostor může být převeden na obsah možností bez problémů s migrací.
Ve zprávě o výstavbě je přítomnost možností indikována ve vlajkovém bajtu.
V odpovědi na výstavbu je přítomnost možností indikována vícebajtovým magickým číslem.
