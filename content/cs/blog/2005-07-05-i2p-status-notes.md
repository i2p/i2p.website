---
title: "Poznámky ke stavu I2P ze dne 2005-07-05"
date: 2005-07-05
author: "jr"
description: "Týdenní aktualizace zahrnující pokrok v transportu SSU, mitigaci útoku IV na tunnel a optimalizaci SSU MAC pomocí HMAC-MD5"
categories: ["status"]
---

Ahoj všichni, zase nastal ten týdenní čas,

* Index

1) Stav vývoje 2) Tunnel IVs (inicializační vektory) 3) SSU MACs (autentizační kódy zpráv) 4) ???

* 1) Dev status

Další týden, další zpráva říkající "Na SSU transportu jsme udělali hodně pokroku" ;) Moje lokální úpravy jsou stabilní a byly odeslány do CVS (HEAD je na verzi 0.5.0.7-9), ale zatím žádné vydání. Brzy další novinky v této oblasti. Podrobnosti o změnách nesouvisejících se SSU jsou v historii [1], i když změny týkající se SSU z toho seznamu zatím vynechávám, protože SSU zatím nepoužívá nikdo mimo vývojáře (a vývojáři čtou i2p-cvs@ :)

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/history.txt?rev=HEAD

* 2) Tunnel IVs

Posledních pár dní dvorak zveřejňuje občasné úvahy o různých způsobech, jak napadnout kryptografii tunnel, a přestože většina z nich už byla adresována, podařilo se nám vymyslet jeden scénář, který by účastníkům umožnil označit dvojici zpráv, aby zjistili, že jsou ve stejném tunnel. Fungovalo by to tak, že dřívější peer nechá zprávu projít dál a později vezme IV a první datový blok z té první tunnel zprávy a vloží je do nové. Tato nová by samozřejmě byla poškozená, ale nevypadala by jako replay (opakované přehrání), protože IV by byly jiné. Dále na trase by pak druhý peer mohl tuto zprávu jednoduše zahodit, aby koncový bod tunnel nemohl útok detekovat.

Jedním z hlavních problémů je, že neexistuje způsob, jak ověřit zprávu pro tunnel, když prochází skrz tunnel, aniž by to otevřelo celou řadu útoků (viz dřívější návrh kryptografie pro tunnel [2] s jednou metodou, která se tomu blíží, ale má dost pochybné pravděpodobnosti a zavádí některá umělá omezení pro tunnels).

[2] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/tunnel.html?rev=HEAD

Existuje však triviální způsob, jak uvedený útok obejít - stačí považovat xor(IV, first data block) za jedinečný identifikátor posílaný přes Bloomův filtr místo samotného IV. Tímto způsobem mezilehlé uzly uvidí duplicitní zprávu a zahodí ji dříve, než dorazí k druhému spolupracujícímu uzlu. CVS bylo aktualizováno tak, aby tuto obranu zahrnovalo, ačkoli velmi, opravdu velmi pochybuji, že jde vzhledem k současné velikosti sítě o praktickou hrozbu, takže to nevydávám jako samostatné vydání.

To sice neovlivňuje proveditelnost jiných útoků založených na časování nebo shaping (tvarování provozu), ale je nejlepší odstranit ty snadno řešitelné útoky, jakmile na ně narazíme.

* 3) SSU MACs

Jak je popsáno ve specifikaci [3], transport SSU používá pro každý odeslaný datagram MAC (autentizační kód zprávy). To je navíc k ověřovacímu hashi posílanému s každou zprávou I2NP (stejně jako k end to end ověřovacím hashům u klientských zpráv). V tuto chvíli specifikace i kód používají zkrácený HMAC-SHA256 - přenáší a ověřují pouze prvních 16 bajtů MAC. To je *cough* poněkud plýtvavé, protože HMAC ve svém běhu používá hash SHA256 dvakrát, pokaždé pracuje s 32bajtovým hashem, a nedávné profilování transportu SSU naznačuje, že je to blízko kritické cesty zátěže CPU. Proto jsem trochu zkoumal náhradu HMAC-SHA256-128 za prostý HMAC-MD5(-128) - i když MD5 není zjevně tak silný jako SHA256, SHA256 stejně zkracujeme na stejnou velikost jako MD5, takže množství hrubé síly potřebné k nalezení kolize je stejné (2^64 pokusů). Momentálně si s tím hraji a zrychlení je výrazné (na 2KB paketech dosahuji více než 3x větší propustnosti HMAC než se SHA256), takže je možné, že s tím půjdeme do provozu. A pokud někdo přijde s dobrým důvodem, proč to nedělat (nebo s lepší alternativou), je dost jednoduché to vyměnit (jen jeden řádek kódu).

[3] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/udp.html?rev=HEAD

* 4) ???

To je pro tuto chvíli asi vše a jako vždy se neváhejte kdykoli podělit o své názory a připomínky. CVS HEAD je nyní znovu sestavitelný i pro ty, kteří nemají nainstalovaný junit (prozatím jsem testy vyňal z i2p.jar, ale stále je lze spouštět pomocí test ant target), a očekávám, že poměrně brzy budou další novinky ohledně testování 0.6 (momentálně se pořád potýkám s podivnostmi na colo boxu (server v colocation) – připojení přes telnet na vlastní rozhraní lokálně selhává (bez jakéhokoli použitelného errno), na dálku to funguje, a to vše bez jakýchkoli iptables či jiných filtrů. radost). Pořád nemám doma přístup k internetu, takže dnes večer nebudu na schůzce, ale snad příští týden.

=jr
