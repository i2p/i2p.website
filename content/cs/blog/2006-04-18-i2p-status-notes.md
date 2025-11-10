---
title: "Stavové poznámky I2P k 2006-04-18"
date: 2006-04-18
author: "jr"
description: "Vylepšení sítě ve verzi 0.6.1.16, analýza kolapsu způsobeného zahlcením při vytváření tunnelů a novinky ve vývoji Feedspace"
categories: ["status"]
---

Ahoj všichni, opět je tu úterý a s ním naše týdenní poznámky o stavu

* Index

1) Stav sítě a 0.6.1.16 2) Vytváření Tunnel a přetížení 3) Feedspace 4) ???

* 1) Net status and 0.6.1.16

Protože 70 % sítě už přešlo na 0.6.1.16, zdá se, že oproti dřívějším verzím dochází ke zlepšení, a s vyřešenými problémy v této verzi máme jasnější představu o našem dalším úzkém hrdle. Ti, kteří ještě nejsou na 0.6.1.16, prosíme, aktualizujte co nejdříve, protože dřívější verze budou nahodile odmítat požadavky na vytvoření tunnelů (i když má router dostatek prostředků k účasti ve více tunnelů).

* 2) Tunnel creation and congestion

Zdá se, že právě teď zažíváme něco, co lze nejlépe popsat jako kolaps z přetížení – požadavky na vytváření tunnelů jsou odmítány, protože routery mají málo šířky pásma, takže se rozesílá více požadavků na vytváření tunnelů v naději, že se najdou jiné routery s volnými prostředky, což však jen dále zvyšuje využitou šířku pásma. Tento problém tu je od doby, kdy jsme v 0.6.1.10 přešli na novou kryptografii pro vytváření tunnelů, a lze jej z velké části připsat tomu, že nedostáváme zpětnou vazbu o přijetí/odmítnutí na každém hopu (skoku) dříve, než (přesněji řečeno, *ledaže*) požadavek a odpověď projdou dvěma tunnely. Pokud kterýkoli z těchto peers (protějšků) zprávu dál nepředá, nevíme, který peer selhal, kteří peerové souhlasili a kteří ji explicitně odmítli.

Už omezujeme počet současně probíhajících požadavků na vytvoření tunnel (a testy ukazují, že zvýšení časového limitu (timeoutu) nepomáhá), takže Nagleovo tradiční řešení nestačí.  Zkouším několik úprav v našem kódu pro zpracování požadavků, abych snížil četnost tichého zahazování požadavků (na rozdíl od explicitních odmítnutí), a také v našem kódu pro generování požadavků, abych snížil souběžnost při zátěži.  Také zkouším další vylepšení, která přinášejí výrazně vyšší úspěšnost sestavení tunnel, i když ještě nejsou připravena k bezpečnému použití.

Už se blýská na lepší časy a vážím si vaší trpělivosti, že s námi zůstáváte, jak postupujeme dál. Očekávám, že později tento týden vydáme další verzi, abychom uvolnili některá vylepšení; poté znovu vyhodnotíme stav sítě, abychom zjistili, zda byl kolaps způsobený zahlcením vyřešen.

* 3) Feedspace

Frosk usilovně pracuje na Feedspace a na webu Trac aktualizoval několik stránek, včetně nového přehledového dokumentu, sady otevřených úkolů, některých podrobností o databázi a dalšího. Zastavte se na http://feedspace.i2p/, abyste se seznámili s nejnovějšími změnami a třeba zasypte Froska otázkami, jakmile budete mít chvilku :)

* 4) ???

To je asi všechno, co mohu v tuto chvíli probrat, ale prosím, zastavte se na #i2p na naše setkání později dnes večer (20:00 UTC), abychom si mohli ještě popovídat!

=jr
