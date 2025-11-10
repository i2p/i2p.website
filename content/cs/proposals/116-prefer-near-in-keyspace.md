---
title: "Preferovat blízké směrovače v keyspace"
number: "116"
author: "chisquare"
created: "2015-04-25"
lastupdated: "2015-04-25"
status: "Potřebuje-výzkum"
thread: "http://zzz.i2p/topics/1874"
---

## Přehled

Toto je návrh na organizaci peerů tak, aby upřednostňovali připojení k jiným peerům, kteří jsou k nim blízko v keyspace.


## Motivace

Myšlenkou je zlepšit úspěšnost vytváření tunelů tím, že se zvýší pravděpodobnost, že směrovač je již připojen k jinému.


## Návrh

### Požadované změny

Tato změna by vyžadovala:

1. Aby každý směrovač upřednostňoval připojení, která jsou blízko v keyspace.
2. Aby si každý směrovač byl vědom toho, že každý preferuje připojení blízko v
   keyspace.


### Výhody pro vytváření tunelů

Pokud vytvoříte tunel::

    A -dlouhý-> B -krátký-> C -krátký-> D

(dlouhý/náhodný vs krátký skok v keyspace), můžete odhadnout, kde se pravděpodobně tunel nezdařil, a vyzkoušet jiného peera v daném místě. Navíc by to umožnilo detekovat hustější části v keyspace a směrovače by je prostě nepoužívaly, protože by to mohl být někdo spolupracující.

Pokud vytvoříte tunel::

    A -dlouhý-> B -dlouhý-> C -krátký-> D

a nezdaří se, můžete odvodit, že pravděpodobně selhal u C -> D a můžete vybrat jiný skok D.

Můžete také vytvářet tunely tak, že OBEP je blíže k IBGW a použít tyto tunely s OBEP, které jsou blíže k danému IBGW v LeaseSet.


## Důsledky pro bezpečnost

Pokud náhodně umístíte krátké vs dlouhé skoky v keyspace, útočník pravděpodobně nezíská mnoho výhod.

Největší nevýhodou však může být, že by to mohlo usnadnit enumeraci uživatelů.
