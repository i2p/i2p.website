---
title: "Podpora Floodfill pro Volitelné Typy Podpisů"
number: "137"
author: "zzz"
created: "2017-03-31"
lastupdated: "2017-11-12"
status: "Otevřeno"
thread: "http://zzz.i2p/topics/2280"
toc: true
---

## Přehled

Přidat možnost, aby floodfilly inzerovaly podporu pro volitelné typy podpisů.
To poskytne způsob, jak podporovat nové typy podpisů z dlouhodobého hlediska,
i když je nebudou podporovat všechny implementace.


## Motivace

Návrh GOST 134 odhalil několik problémů s dříve nepoužívaným experimentálním rozsahem typů podpisů.

Za prvé, protože typy podpisů v experimentálním rozsahu nelze rezervovat, mohou být použity pro
více typů podpisů současně.

Za druhé, pokud router info nebo lease set s experimentálním typem podpisu nemůže být uložen na floodfill,
nový typ podpisu je obtížné plně otestovat nebo použít jako zkušební verzi.

Za třetí, pokud bude realizován návrh 136, není to bezpečné, protože kdokoli může přepsat záznam.

Za čtvrté, implementace nového typu podpisu může být velkým vývojovým úsilím.
Může být obtížné přesvědčit vývojáře pro všechny implementace routerů, aby přidali podporu pro nový
typ podpisu včas pro jakékoli konkrétní vydání. Čas a motivace vývojářů se mohou lišit.

Za páté, pokud GOST používá typ podpisu v standardním rozsahu, stále neexistuje způsob, jak zjistit, zda konkrétní
floodfill podporuje GOST.


## Návrh

Všechny floodfill musí podporovat typy podpisů DSA (0), ECDSA (1-3) a EdDSA (7).

Pro jakýkoli jiný typ podpisu ve standardním (ne-experimentálním) rozsahu může floodfill
inzerovat podporu ve svých vlastnostech router info.


## Specifikace


Router, který podporuje volitelný typ podpisu, by měl přidat vlastnost "sigTypes"
do svého zveřejněného router info s čísly typů podpisů oddělenými čárkami.
Typy podpisů budou v tříděném číselném pořadí.
Povinné typy podpisů (0-4,7) by neměly být zahrnuty.

Například: sigTypes=9,10

Routery, které podporují volitelné typy podpisů, musí ukládat, vyhledávat nebo šířit
pouze do floodfillů, které inzerují podporu pro tento typ podpisu.


## Migrace

Nepoužitelné.
Pouze routery, které podporují volitelný typ podpisu, to musí implementovat.


## Problémy

Pokud není mnoho floodfillů podporujících daný typ podpisu, mohou být těžko k nalezení.

Nemusí být nutné požadovat ECDSA 384 a 521 (typy podpisů 2 a 3) pro všechny floodfill.
Tyto typy nejsou široce používány.

Podobné problémy bude třeba řešit s nenulovými typy šifrování,
což ještě nebylo formálně navrženo.


## Poznámky

Úložiště NetDB neznámých typů podpisů, které nejsou v experimentálním rozsahu, budou nadále
odmítány floodfilly, protože podpis nemůže být ověřen.


