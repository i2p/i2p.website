---
title: "Dávkování Více Datových Stroužků v Česneku"
number: "115"
author: "orignal"
created: "2015-01-22"
lastupdated: "2015-01-22"
status: "Potřeba-Výzkumu"
thread: "http://zzz.i2p/topics/1797"
---

## Přehled

Tento návrh se týká odesílání více datových stroužků uvnitř koncového
česnekového zprávy, místo pouze jednoho.


## Motivace

Není jasné.


## Potřebné Změny

Změny by byly v OCMOSJ a příslušných pomocných třídách, a v
ClientMessagePool. Jelikož nyní neexistuje žádná fronta, byla by nutná nová
fronta a nějaké zpoždění. Jakékoliv dávkování by muselo respektovat maximální
velikost česneku, aby se minimalizovalo riziko ztráty. Možná 3KB? Nejdříve by
bylo vhodné věci instrumentovat, aby se změřilo, jak často by se to využívalo.


## Úvahy

Není jasné, zda to bude mít nějaký užitečný efekt, protože streamování už nyní
provádí dávkování a vybírá optimální MTU. Dávkování by zvětšilo velikost zprávy
a exponenciální pravděpodobnost ztráty.

Výjimkou je nekomprimovaný obsah, gzipovaný na úrovni I2CP. Ale HTTP provoz je
už komprimován na vyšší úrovni a data Bittorrentu jsou obvykle nekomprimovatelná.
Co zbývá? I2pd aktuálně neprovádí komprimaci x-i2p-gzip, takže by to zde mohlo
hodně pomoci. Ale uváděný cíl, aby nedošlo k vyčerpání značek, je lepší řešit
správnou implementací okének v jeho streamingové knihovně.


## Kompatibilita

Je to zpětně kompatibilní, protože přijímač česneku již zpracuje všechny
stroužky, které obdrží.
