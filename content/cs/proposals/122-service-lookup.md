---
title: "Zjišťování služby"
number: "122"
author: "zzz"
created: "2016-01-13"
lastupdated: "2016-01-13"
status: "Zamítnuto"
thread: "http://zzz.i2p/topics/2048"
supercedes: "102"
supercededby: "123"
---

## Přehled

Toto je bombastická absolutní návrh v rámci netDB. AKA anycast. Toto by byl 4. navržený podtyp LS2.


## Motivace

Řekněme, že byste chtěli inzerovat svůj cíl jako outproxy, nebo GNS node, nebo
Tor gateway, nebo Bittorrent DHT nebo imule nebo i2phex nebo Seedless bootstrap, atd.
Můžete uložit tyto informace v netDB namísto použití samostatné
bootstrapping vrstvy nebo informační vrstvy.

Nikdo není za to zodpovědný, takže na rozdíl od masivního multihomingu nemůžete mít
podepsaný autoritativní seznam. Takže byste jen publikovali svůj záznam do floodfill.
Floodfill by tyto záznamy shromažďoval a odesílal je jako odpověď na dotazy.


## Příklad

Představte si, že vaše služba byla "GNS". Odeslali byste ukládání databáze do floodfill:

- Hash "GNS"
- cíl
- časová značka publikace
- expirace (0 pro zrušení)
- port
- podpis

Když by někdo provedl dotaz, dostal by seznam těchto záznamů zpět:

- Hash "GNS"
- Hash floodfill
- Časová značka
- počet záznamů
- Seznam záznamů
- podpis floodfill

Expirace by byly relativně dlouhé, minimálně hodiny.


## Implications of Security

Nevýhodou je, že by se to mohlo proměnit v Bittorrent DHT nebo horší. Minimálně by floodfill musel mít přísný limit pro rychlost a kapacitu ukládání a dotazování. Mohli bychom schválit vyšší limity pro schválené názvy služeb. Mohli bychom také zakázat nepovolené služby úplně.

Samozřejmě, i dnešní netDB je otevřený zneužití. Můžete uložit libovolná data v netDB, pokud se tváří jako RI nebo LS a podpis je ověřen. Ale toto by to hodně zjednodušilo.
