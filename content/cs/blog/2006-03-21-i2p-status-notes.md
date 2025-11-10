---
title: "Poznámky ke stavu I2P ze dne 2006-03-21"
date: 2006-03-21
author: "jr"
description: "Integrace JRobin pro síťové statistiky, IRC boti biff a toopie a oznámení nového GPG klíče"
categories: ["status"]
---

Ahoj všichni, zase je úterý

* Index

1) Stav sítě 2) jrobin 3) biff a toopie 4) nový klíč 5) ???

* 1) Net status

The past week has been pretty stable, with no new release yet.  I've been churning away on tunnel throttling and low bandwidth operation, but to help out with that testing, I've integrated JRobin with the web console and our stats management system.

* 2) JRobin

JRobin [1] je čistý port RRDtoolu [2] v Javě, který nám umožňuje generovat pěkné grafy, jako jsou ty, které zzz už nějakou dobu produkuje, a to s velmi malou paměťovou režií. Nastavili jsme jej tak, aby pracoval výhradně v paměti, takže nedochází k soupeření o zámky souborů, a čas potřebný k aktualizaci databáze je nepostřehnutelný. Existuje spousta šikovných věcí, které JRobin umí a které nevyužíváme, ale příští vydání bude mít základní funkcionalitu a navíc možnost exportovat data ve formátu, kterému RRDtool rozumí.

[1] http://www.jrobin.org/ [2] http://people.ee.ethz.ch/~oetiker/webtools/rrdtool/

* 3) biff and toopie

Postman už nějakou dobu intenzivně pracuje na několika užitečných botech a s potěšením oznamuji, že roztomilý biff je zpátky [3] a dá vám vědět, kdykoli budete mít (anonymní) poštu, když jste na irc2p.  Kromě toho postman pro nás vytvořil úplně nový bot - toopie - který bude sloužit jako informační bot pro I2P/irc2p.  Stále toopie krmíme často kladenými dotazy (FAQ), ale brzy se objeví v obvyklých kanálech.  Díky, postman!

[3] http://hq.postman.i2p/?page_id=15

* 4) new key

Pro ty, kteří dávají pozor: pravděpodobně jste si všimli, že můj GPG klíč vyprší za pár dní. Můj nový klíč na http://dev.i2p.net/~jrandom má otisk 0209 9706 442E C4A9 91FA  B765 CE08 BC25 33DC 8D49 a ID klíče 33DC8D49. Tento příspěvek je podepsán mým starým klíčem, ale mé následující příspěvky (a vydání) v průběhu příštího roku budou podepsány novým klíčem.

* 5) ???

To je pro tuto chvíli asi všechno - za pár minut se zastav na #i2p na naše týdenní setkání a pozdrav!

=jr
