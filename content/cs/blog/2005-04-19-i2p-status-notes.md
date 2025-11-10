---
title: "Poznámky ke stavu I2P k 2005-04-19"
date: 2005-04-19
author: "jr"
description: "Týdenní aktualizace zahrnující nadcházející opravy ve verzi 0.5.0.7, pokrok v UDP transportu SSU, změny v plánu vývoje přesouvající 0.6 na červen a vývoj Q"
categories: ["status"]
---

Ahoj všichni, opět nastal ten čas týdne,

* Index

1) Stav sítě 2) Stav SSU 3) Aktualizace plánu vývoje 4) Stav Q 5) ???

* 1) Net status

Během téměř dvou týdnů od vydání 0.5.0.6 se věci vyvíjely většinou pozitivně, i když poskytovatelé služeb (eepsites(I2P Sites), ircd, atd.) se v poslední době potýkají s některými chybami. Zatímco klienti jsou na tom dobře, server se časem může dostat do situace, kdy selhávající tunnels mohou spustit příliš agresivní omezovací kód, který brání správnému znovuvytvoření a publikaci leaseSet.

V CVS mimo jiné proběhlo několik oprav a očekávám, že během příštího dne či dvou vydáme novou verzi 0.5.0.7.

* 2) SSU status

For those not following my (oh so exciting) blog, there's been a lot of progress with the UDP transport, and right now its fairly safe to say that the UDP transport will not be our throughput bottleneck :) While debugging that code, I've taken the opportunity to work through the queueing at higher levels as well, finding points where we can remove unnecessary choke points. As I said last week, though, there's still a lot of work to do. More info will be available when there's more info available.

* 3) Roadmap update

Je teď duben, takže roadmapa [1] byla příslušně aktualizována - vypuštěním 0.5.1 a posunem některých termínů. Hlavní změnou je přesun 0.6 z dubna na červen, i když to ve skutečnosti není tak velká změna, jak to vypadá. Jak jsem zmínil minulý týden, můj vlastní harmonogram se trochu posunul a místo stěhování do $somewhere v červnu se budu stěhovat do $somewhere v květnu. Přestože bychom mohli mít vše potřebné pro 0.6 hotové už tento měsíc, v žádném případě nehodlám vypustit takovou velkou aktualizaci a pak na měsíc zmizet, protože realita softwaru je taková, že se vždy najdou chyby, které testování neodhalí.

[1] http://www.i2p.net/roadmap

* 4) Q status

Aum se na Q pořádně rozjel a přidává pro nás další vylepšení, přičemž na svých stránkách [2] už jsou nejnovější snímky obrazovky. Kód už také provedl commit do CVS (hurá), takže bychom snad brzy mohli začít s alfa testováním. Jsem si jistý, že se od auma dozvíme více podrobností o tom, jak pomoci, anebo se můžete rovnou ponořit do materiálu v CVS na i2p/apps/q/

[2] http://aum.i2p/q/

* 5) ???

Také se toho dělo mnohem víc, se živými diskusemi na mailing listu, fóru a IRC. Nebudu se to tady snažit shrnout, protože do začátku schůzky zbývá jen pár minut, ale klidně se stavte, pokud je něco, o čem se nemluvilo a co chcete nastolit!

=jr
