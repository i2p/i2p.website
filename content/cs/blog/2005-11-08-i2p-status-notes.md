---
title: "Stavové poznámky k I2P ze dne 2005-11-08"
date: 2005-11-08
author: "jr"
description: "Týdenní aktualizace zahrnující stabilitu verze 0.6.1.4, plán optimalizace výkonu, vydání I2Phex 0.1.1.35, vývoj BT klienta I2P-Rufus, pokrok u I2PSnarkGUI a přepracování uživatelského rozhraní Syndie"
categories: ["status"]
---

Ahoj všichni, zase úterý.

* Index

1) Stav sítě / krátkodobý plán 2) I2Phex 3) I2P-Rufus 4) I2PSnarkGUI 5) Syndie 6) ???

* 1) Net status / short term roadmap

0.6.1.4 se stále zdá být docela stabilní, i když od té doby v CVS přibylo několik oprav chyb. Také jsem přidal několik optimalizací pro SSU, aby přenášel data efektivněji, které by, doufám, po širokém nasazení měly mít znatelný dopad na síť. Momentálně však 0.6.1.5 odkládám, protože je tu ještě několik dalších věcí, které chci dostat do příštího vydání. Aktuální plán je vydat ho tento víkend, takže sledujte nejnovější zprávy.

Vydání 0.6.2 přinese spoustu skvělých novinek, abychom mohli čelit ještě silnějším protivníkům, ale jednu věc neovlivní: výkon. Hlavním smyslem I2P je sice anonymita, ale pokud jsou propustnost a latence špatné, nebudeme mít žádné uživatele. Proto je mým plánem nejprve dostat výkon tam, kde má být, a teprve poté přistoupit k implementaci strategií řazení peerů pro 0.6.2 a nových technik pro vytváření tunnel.

* 2) I2Phex

V poslední době se toho hodně děje i kolem I2Phexu, včetně nové verze 0.1.1.35 [1]. V CVS navíc proběhly další změny (díky, Legion!), takže by mě nepřekvapilo, kdyby se později tento týden objevila verze 0.1.1.36.

Také v oblasti gwebcache došlo k dobrému pokroku (viz http://awup.i2p/), ale pokud vím, nikdo zatím nezačal pracovat na úpravě I2Phexu, aby používal gwebcache s podporou I2P (máte zájem? Dejte mi vědět!).

[1] http://forum.i2p.net/viewtopic.php?t=1157

* 3) I2P-Rufus

Říká se, že defnax a Rawn provádějí úpravy BT klienta Rufus a slučují do něj kód související s I2P z I2P-BT. Nevím, jaký je aktuální stav toho portu (portace), ale vypadá to, že bude mít pár pěkných funkcí. Jsem si jistý, že se dozvíme víc, až bude co dalšího sdělit.

* 4) I2PSnarkGUI

Další kolující zvěst je, že Markus pracuje na novém GUI v C#... Snímky obrazovky na PlanetPeer vypadají dost dobře [2]. Stále existují plány na webové rozhraní nezávislé na platformě, ale tohle vypadá velmi pěkně. Jsem si jist, že jak bude vývoj GUI postupovat, uslyšíme od Markuse víc.

[2] http://board.planetpeer.de/index.php?topic=1338

* 5) Syndie

Probíhá také diskuse o přepracování uživatelského rozhraní Syndie [3] a očekávám, že v tomto ohledu poměrně brzy uvidíme pokrok. dust také usilovně pracuje na projektu Sucker, přidává lepší podporu pro načítání více RSS/Atom kanálů do Syndie a také některá vylepšení samotného SML.

[3] http://syndiemedia.i2p.net:8000/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&entry=1131235200000&expand=true

* 6) ???

Děje se toho spousta, jako vždy. Zaskočte za pár minut na #i2p na naši týdenní vývojářskou schůzku.

=jr
