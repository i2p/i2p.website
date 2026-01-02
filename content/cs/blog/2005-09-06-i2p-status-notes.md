---
title: "Poznámky ke stavu I2P ze dne 2005-09-06"
date: 2005-09-06
author: "jr"
description: "Týdenní aktualizace zahrnující úspěšné vydání 0.6.0.5, výkon floodfill netDb, pokrok Syndie v oblasti RSS a pet names (uživatelské názvy), a novou aplikaci pro správu adresáře susidns"
categories: ["status"]
---

Ahoj všichni,


* Index

1) Stav sítě 2) Stav Syndie 3) susidns 4) ???

* 1) Net status

Jak si mnozí všimli, vydání 0.6.0.5 vyšlo minulý týden po krátké revizi 0.6.0.4 a zatím se spolehlivost výrazně zlepšila a síť je větší než kdy dřív. Stále je prostor ke zlepšení, ale zdá se, že nový netDb funguje tak, jak byl navržen. Dokonce jsme otestovali i fallback (záložní mechanismus) - když jsou floodfill peery nedostupné, routers přejdou na kademlia netDb, a před pár dny, když k takové situaci došlo, spolehlivost irc a eepsite(I2P Site) nebyla výrazně snížena.

Dostal jsem dotaz ohledně toho, jak funguje nový netDb, a odpověď [1] jsem zveřejnil na svém blogu [2]. Jako vždy, pokud má někdo ohledně takových věcí nějaké otázky, klidně mi je pošlete, ať už na mailing listu nebo mimo něj, na fóru, nebo třeba i na svém blogu ;)

[1] http://syndiemedia.i2p.net/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&entry=1125792000000&expand=true [2] http://syndiemedia.i2p.net/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=

* 2) Syndie status

Jak můžete vidět na syndiemedia.i2p (a http://syndiemedia.i2p.net/), v poslední době došlo k velkému pokroku, včetně RSS, přezdívek, administrátorských ovládacích prvků a počátků rozumného používání css. Také byla nasazena většina Isamoorových návrhů, stejně jako Adamových, takže pokud má někdo něco, co by tam rád viděl, napište mi prosím zprávu!

Syndie je nyní poměrně blízko beta verze, a v této fázi bude distribuována jako jedna z výchozích aplikací I2P i jako samostatný balíček, takže jakákoli pomoc bude velmi vítána. S dnešními nejnovějšími přírůstky (in cvs) je i úprava vzhledu Syndie hračka - stačí vytvořit nový soubor syndie_standard.css ve svém adresáři i2p/docs/ a zadané styly přepíší výchozí nastavení Syndie. Více informací o tom najdete na mém blogu [2].

* 3) susidns

Susi pro nás dala dohromady další webovou aplikaci - susidns [3]. Slouží jako jednoduché rozhraní pro správu aplikace addressbook - jejích záznamů, odběrů atd. Vypadá to docela dobře, takže doufejme, že ji brzy budeme moci dodávat jako jednu z výchozích aplikací, ale prozatím je hračka ji stáhnout z jejího eepsite(I2P Site), uložit ji do svého adresáře webapps, restartovat svůj router a jste připraveni.

[3] http://susi.i2p/?page_id=13

* 4) ???

Ačkoli jsme se v poslední době určitě soustředili na oblast klientských aplikací (a budeme v tom pokračovat), velkou část svého času stále věnuji základnímu fungování sítě a na obzoru jsou některé zajímavé novinky – obcházení firewallů a NATu pomocí introductions (zprostředkování spojení), vylepšená automatická konfigurace SSU, pokročilé řazení a výběr peerů a dokonce i jednoduchá obsluha omezených tras. Co se týče webu, HalfEmpty provedl několik vylepšení v našich kaskádových stylech (hurá!).

Každopádně se toho děje spousta, ale to je tak všechno, na co mám teď čas se zmínit, tak se zastavte na setkání ve 20:00 UTC a pozdravte :)

=jr
