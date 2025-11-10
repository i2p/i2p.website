---
title: "Poznámky ke stavu I2P k 17. 8. 2004"
date: 2004-08-17
author: "jr"
description: "Týdenní aktualizace stavu I2P věnovaná problémům s výkonem sítě, útokům DoS a vývoji Stasher DHT"
categories: ["status"]
---

Ahoj všichni, je čas na aktualizaci

## Rejstřík:

1. Network status and 0.3.4.3
2. Stasher
3. ???

## 1) Stav sítě a 0.3.4.3

Ačkoli byla síť během posledního týdne funkční, místy se vyskytlo mnoho potíží, což vedlo k dramatickému poklesu spolehlivosti. Vydání 0.3.4.2 významně pomohlo při řešení DoS způsobeného jistou nekompatibilitou a problémy se synchronizací času – viz graf požadavků na síťovou databázi ukazující DoS (špičky mimo graf), který byl zastaven nasazením 0.3.4.2. To však bohužel zase přineslo vlastní sadu problémů, což vedlo k významnému počtu retransmisí zpráv, jak je vidět na grafu šířky pásma. Zvýšené zatížení tam bylo také způsobeno skutečným nárůstem uživatelské aktivity, takže to zas /tak/ šílené není ;) Ale stejně to byl problém.

Posledních pár dní jsem byl docela sobecký. Měli jsme spoustu oprav chyb otestovaných a nasazených na několika routers, ale ještě jsem je nevydal, protože se mi při spouštění mých simulací jen zřídka podaří otestovat vzájemnou interakci nekompatibilit v softwaru. Takže jste byli vystaveni příšerně mizernému provozu sítě, zatímco ladím věci, abych našel způsoby, jak nechat routers fungovat dobře i tehdy, když spousta routers stojí za nic. V tomhle ohledu děláme pokroky - profilování a vyhýbání se peerům, kteří zneužívají network database, efektivnější správa front požadavků network database a vynucování diverzifikace tunnelů.

Ještě tam nejsme, ale mám naději. Testy nyní běží na živé síti a až to bude připraveno, vyjde verze 0.3.4.3, která přinese výsledky.

## 2) Stasher

Aum odvádí na svém DHT (distribuovaná hašovací tabulka) skvělou práci a přestože v současnosti má několik zásadních omezení, vypadá slibně. Rozhodně ještě není připraveno pro běžné použití, ale pokud se chcete zapojit a pomoci mu s testováním (nebo programováním :), podívejte se na web a spusťte uzel.

## 3) ???

To je zatím asi všechno. Protože schůzka měla před minutou začít, měl bych to asi ukončit. Uvidíme se na #i2p!

=jr
