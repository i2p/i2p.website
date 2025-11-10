---
title: "Poznámky ke stavu I2P k 2005-10-18"
date: 2005-10-18
author: "jr"
description: "Týdenní aktualizace zahrnující úspěšné vydání 0.6.1.3, diskusi o spolupráci s Freenetem, analýzu útoků na bootstrap pro tunnel, pokrok v řešení chyby nahrávání v I2Phex a odměnu za řešení symetrického NATu"
categories: ["status"]
---

Ahoj všichni, zase je úterý

* Index

1) 0.6.1.3 2) Freenet, I2P a darknety (pane jo) 3) Útoky při bootstrapu (inicializaci) Tunnel 4) I2Phex 5) Syndie/Sucker 6) ??? [odměna 500+ za symetrický NAT]

* 1) 0.6.1.3

Minulý pátek jsme vydali novou verzi 0.6.1.3 a protože už je aktualizováno 70 % sítě, jsou ohlasy velmi pozitivní. Zdá se, že nová vylepšení SSU omezila zbytečné retransmise, což umožňuje efektivnější propustnost při vyšších rychlostech, a pokud je mi známo, nevyskytly se žádné větší problémy s IRC proxy ani s vylepšeními Syndie.

Za zmínku stojí, že Eol vypsal na rentacoder[1] odměnu za implementaci podpory symetrického NATu, takže doufejme, že se v této oblasti dočkáme nějakého pokroku!

[1] http://rentacoder.com/RentACoder/misc/BidRequests/ShowBidRequest.asp?lngBidRequestId=349320

* 2) Freenet, I2P, and darknets (oh my)

Konečně jsme uzavřeli to vlákno s více než stovkou zpráv — máme teď jasnější představu o obou sítích, o tom, kam zapadají, a jaký máme prostor pro další spolupráci. Nebudu se zde pouštět do toho, pro jaké topologie nebo modely hrozeb se nejlépe hodí, ale pokud chcete vědět víc, můžete se ponořit do mailing listů. Co se týče spolupráce, poslal jsem toadovi nějaký ukázkový kód pro opětovné využití našeho SSU transportu, který by mohl být krátkodobě užitečný pro lidi z Freenetu, a časem bychom mohli společně nabídnout premix routing (předmíchávací směrování) pro uživatele Freenetu v prostředích, kde je I2P použitelné. Jak se bude Freenet vyvíjet, možná se nám podaří zprovoznit Freenet i nad I2P jako klientskou aplikaci, což by umožnilo automatickou distribuci obsahu mezi uživateli, kteří ho provozují (např. rozesílání archivů a příspěvků Syndie), ale nejdřív uvidíme, jak budou fungovat ve Freenetu plánované systémy řízení zátěže a distribuce obsahu.

* 3) Tunnel bootstrap attacks

Michael Rogers se ozval ohledně několika zajímavých nových útoků na vytváření tunnels v I2P [2][3][4]. Primární útok (úspěšné provedení predecessor attack (útoku předchůdce) během celého bootstrap procesu) je zajímavý, ale není příliš praktický – pravděpodobnost úspěchu je (c/n)^t, kde c je počet útočníků, n počet peerů v síti a t počet tunnels vybudovaných cílem (za dobu životnosti) – je menší než pravděpodobnost, že útočník ovládne tunnel na všech h skocích (P(success) = (c/n)^h) poté, co router vybuduje h tunnels.

Michael na mailing listu zveřejnil další útok, kterým se právě zabýváme, takže ho tam budete moci také sledovat.

[2] http://dev.i2p.net/pipermail/i2p/2005-October/001005.html [3] http://dev.i2p.net/pipermail/i2p/2005-October/001008.html [4] http://dev.i2p.net/pipermail/i2p/2005-October/001006.html

* 4) I2Phex

Striker dělá další pokrok ohledně chyby při nahrávání a podle zpráv ji už přesně identifikoval. Doufejme, že se to dnes v noci dostane do CVS a krátce poté bude vydáno jako 0.1.1.33. Sledujte fórum [5] pro více informací.

[5] http://forum.i2p.net/viewforum.i2p?f=25

Říká se, že redzara dělá docela dobré pokroky na opětovné integraci do hlavní větve Phexu, takže doufejme, že s Gregorovou pomocí to brzy dáme do aktuálního stavu!

* 5) Syndie/Sucker

dust také usilovně pracuje na Suckeru a kód do Syndie přináší více dat z RSS/Atom. Možná se nám podaří Sucker a post CLI dále integrovat do Syndie, možná dokonce přidat webové rozhraní pro plánování importů různých RSS/Atom kanálů do různých blogů. Uvidíme...

* 6) ???

Nad rámec výše uvedeného se toho děje spousta, ale to je hlavní podstata toho, o čem vím. Pokud má někdo nějaké otázky nebo obavy, nebo chce probrat další věci, přijďte dnes večer ve 20:00 UTC na setkání v #i2p!

=jr
