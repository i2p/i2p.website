---
title: "Podpora Floodfill pro Experimentální Typy Podpisů"
number: "136"
author: "zzz"
created: "2017-03-31"
lastupdated: "2017-11-12"
status: "Open"
thread: "http://zzz.i2p/topics/2279"
toc: true
---

## Přehled

Pro typy podpisů v experimentálním rozmezí (65280-65534),
by měly floodfills akceptovat úložiště netdb bez kontroly podpisu.

Tím se podpoří testování nových typů podpisů.


## Motivace

Návrh GOST 134 odhalil dva problémy s dříve nepoužívaným experimentálním rozsahem typů podpisů.

Za prvé, protože typy podpisů v experimentálním rozmezí nemohou být rezervovány, mohou být
použity pro více typů podpisů najednou.

Za druhé, pokud nemůže být router info nebo lease set s experimentálním typem podpisu uložen v floodfill,
je nový typ podpisu obtížné plně otestovat nebo použít na zkušební bázi.


## Návrh

Floodfills by měly přijímat a šířit úložiště LS s typy podpisů v experimentálním rozmezí,
bez kontroly podpisu. Podpora pro úložiště RI je zatím nejasná a může mít více bezpečnostních implikací.


## Specifikace


Pro typy podpisů v experimentálním rozmezí by floodfill měl přijímat a šířit netdb
úložiště bez kontroly podpisu.

Aby se zabránilo podvodům s neexperimentálními routery a cíli, floodfill
by nikdy neměl přijímat úložiště experimentálního typu podpisu, které má kolizi hash
s existujícím záznamem netdb jiného typu podpisu.
To brání únosu předchozího záznamu netdb.

Kromě toho by floodfill měl přepsat experimentální záznam netdb
úložištěm neexperimentálního typu podpisu, který je kolizí hash,
aby se zabránilo únosu dříve neexistujícího hashe.

Floodfills by měly předpokládat délku veřejného klíče pro podpis 128, nebo ji odvodit z
délky certifikátu klíče, pokud je delší. Některé implementace nemusí
podporovat delší délky, pokud typ podpisu není neformálně rezervován.


## Migrace

Jakmile je tato funkce podporována v známé verzi routeru,
mohou být experimentální záznamy netdb typu podpisu uložené do floodfills této verze nebo vyšší.

Pokud některé implementace routeru tuto funkci nepodporují, ukládání do netdb
selže, ale to je stejné jako nyní.


## Problémy

Mohou existovat další bezpečnostní implikace, které je třeba prozkoumat (viz návrh 137)

Některé implementace nemusí podporovat délky klíčů větší než 128,
jak je popsáno výše. Dále může být nutné vynutit maximum 128
(tedy žádná nadbytečná data klíče v certifikátu klíče),
aby se snížila schopnost útočníků generovat kolize hash.

Podobné problémy bude třeba řešit s ne-nulovými typy šifrování,
což ještě nebylo formálně navrženo.


## Poznámky

Úložiště NetDB neznámých typů podpisů, které nejsou v experimentálním rozmezí, budou nadále
odmítána floodfills, protože podpis nelze ověřit.


