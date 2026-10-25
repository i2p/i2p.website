---
title: "Ministreaming Library"
description: "Historické poznámky k první TCP-like transportní vrstvě I2P"
slug: "ministreaming"
aliases:
  - "/cs/ministreaming"
  - "/cs/ministreaming/"
lastUpdated: "2025-02"
accurateFor: "historical"
---

## Poznámka

Knihovna ministreaming byla vylepšena a rozšířena "úplnou" [streaming knihovnou](/docs/api/streaming). Ministreaming je zastaralé a není kompatibilní s dnešními aplikacemi. Následující dokumentace je stará. Také si všimněte, že streaming rozšiřuje ministreaming ve stejném Java balíčku (net.i2p.client.streaming), takže aktuální API dokumentace obsahuje obojí. Zastaralé ministreaming třídy a metody jsou v Javadocs jasně označeny jako deprecated.

## Knihovna Ministreaming

Knihovna ministreaming je vrstva nad jádrem [I2CP](/docs/protocol/i2cp), která umožňuje spolehlivé, seřazené a autentizované proudy zpráv fungovat přes nespolehlivou, neseřazenou a neautentizovanou vrstvu zpráv. Stejně jako vztah TCP k IP má tato streaming funkcionalnost celou řadu kompromisů a optimalizací k dispozici, ale místo vkládání této funkcionality do základního I2P kódu byla vyčleněna do vlastní knihovny jak pro udržení TCP-podobných složitostí odděleně, tak pro umožnění alternativních optimalizovaných implementací.

Knihovna ministreaming byla napsána uživatelem mihi jako součást jeho aplikace [I2PTunnel](/docs/api/i2ptunnel) a poté byla vydělena a uvolněna pod licencí BSD. Nazývá se knihovna "mini"streaming, protože provádí určitá zjednodušení v implementaci, zatímco robustnější streaming knihovna by mohla být dále optimalizována pro provoz nad I2P. Dva hlavní problémy s knihovnou ministreaming jsou její použití tradičního TCP dvoufázového protokolu pro navázání spojení a současná pevná velikost okna 1. Problém s navazováním spojení je menší u dlouho žijících streamů, ale u krátkých, jako jsou rychlé HTTP požadavky, může být dopad významný. Pokud jde o velikost okna, knihovna ministreaming neudržuje žádné ID nebo pořadí v rámci odesílaných zpráv (ani nezahrnuje žádné ACK nebo SACK na aplikační úrovni), takže musí čekat v průměru dvojnásobek času potřebného k odeslání zprávy, než odešle další.

I přes tyto problémy ministreaming knihovna funguje docela dobře v mnoha situacích a její API je jednoduché a schopné zůstat nezměněné při zavádění různých streaming implementací. Knihovna je nasazena ve svém vlastním ministreaming.jar. Vývojáři v Javě, kteří ji chtějí používat, mohou přistupovat k API přímo, zatímco vývojáři v jiných jazycích ji mohou používat prostřednictvím streaming podpory [SAM](/docs/api/samv3).
