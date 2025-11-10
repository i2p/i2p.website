---
title: "Stavové poznámky I2P k 2005-02-22"
date: 2005-02-22
author: "jr"
description: "Týdenní poznámky ke stavu vývoje I2P zahrnující úspěch vydání 0.5, chystané opravné vydání 0.5.0.1, strategie řazení peerů pro tunnel a aktualizace azneti2p"
categories: ["status"]
---

Ahoj všichni, je čas na týdenní aktualizaci.

* Index

1) 0.5 2) Další kroky 3) azneti2p 4) ???

* 1) 0.5

Jak už jste všichni slyšeli, konečně jsme vydali verzi 0.5 a celkově si vede docela dobře. Opravdu si vážím toho, jak rychle lidé aktualizovali – během prvního dne bylo 50–75 % sítě na 0.5! Díky rychlému přijetí jsme mohli rychleji vidět dopad jednotlivých změn a zároveň jsme našli spoustu chyb. Přestože je stále několik otevřených problémů, ještě dnes večer vydáme novou verzi 0.5.0.1, abychom vyřešili ty nejdůležitější.

Jako vedlejší přínos těch chyb bylo fajn vidět, že routers zvládnou tisíce tunnels ;)

* 2) Next steps

Po vydání verze 0.5.0.1 může následovat další sestavení, abychom vyzkoušeli některé změny při budování průzkumných tunnel (například použití pouze jednoho nebo dvou neselhávajících peerů, přičemž zbytek bude vysokokapacitní, namísto toho, aby všichni peerové byli neselhávající). Poté se přesuneme k verzi 0.5.1, která zlepší propustnost tunnel (seskupováním více malých zpráv do jedné zprávy v rámci jednoho tunnel) a dá uživateli větší kontrolu nad svou náchylností k útoku předchůdce.

Tato nastavení budou mít podobu strategií řazení a výběru peerů (protějšků) na úrovni jednotlivého klienta, jedné pro vstupní bránu a výstupní koncový bod a jedné pro zbytek tunnel.  Aktuální stručný náčrt strategií, které předpokládám:
  = náhodné (co máme nyní)
  = vyvážené (výslovně se snažit snížit frekvenci používání jednotlivých peerů)
  = striktní (pokud někdy použijeme A-->B-->C, zůstanou v tomto pořadí
            během následných tunnels [omezeno časem])
  = volné (vygenerovat pro klienta náhodný klíč, spočítat XOR
           mezi tímto klíčem a každým peerem a vždy řadit peery
           podle vzdálenosti od tohoto klíče [omezeno časem])
  = pevné (vždy používat stejné peery podle MBTF)

Každopádně, to je plán, i když si nejsem jistý, které strategie budou nasazeny jako první.  Návrhy jsou více než vítány :)

* 3) azneti2p

Lidé z azureus tvrdě pracují a vydávají jednu aktualizaci za druhou a jejich nejnovější b34 snapshot (vývojové sestavení) [1] zřejmě obsahuje některé opravy chyb související s I2P. Ačkoli jsem od té poslední záležitosti ohledně anonymity, na kterou jsem upozornil, neměl čas auditovat zdrojový kód, tu konkrétní chybu opravili, takže pokud máte chuť experimentovat, stáhněte si jejich aktualizaci a zkuste ji!

[1] http://azureus.sourceforge.net/index_CVS.php

* 4) ???

Děje se toho strašně moc a jsem si jistý, že jsem zdaleka nepokryl všechno. Zaskoč na setkání za pár minut a podívej se, co se děje!

=jr
