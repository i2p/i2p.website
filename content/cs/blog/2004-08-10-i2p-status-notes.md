---
title: "Poznámky ke stavu I2P k 2004-08-10"
date: 2004-08-10
author: "jr"
description: "Týdenní aktualizace stavu I2P zaměřená na výkon verze 0.3.4.1, vyvažování zátěže outproxy (výstupní proxy) a aktualizace dokumentace"
categories: ["status"]
---

Ahoj všichni, je čas na týdenní aktualizaci

## Rejstřík:

1. 0.3.4.1 status
2. Updated docs
3. 0.4 progress
4. ???

## 1) 0.3.4.1 stav

Tak, před pár dny jsme vypustili verzi 0.3.4.1 a vede si docela dobře. Časy připojení na irc jsou stabilně v řádu několika hodin a přenosové rychlosti jsou také dost dobré (před pár dny jsem z jednoho eepsite(I2P Site) při použití 3 paralelních streamů stáhl 25KBps).

Jedna opravdu skvělá funkce přidaná ve vydání 0.3.4.1 (kterou jsem zapomněl uvést v oznámení o vydání) byl patch od mule, který umožňuje eepproxy střídavě (round-robin) směrovat požadavky mimo I2P přes řadu outproxy (výstupních proxy). Výchozí chování je stále jen použít outproxy squid.i2p, ale pokud otevřete svůj soubor router.config a upravíte řádek clientApp tak, aby obsahoval:

```
-e 'httpclient 4444 squid.i2p,www1.squid.i2p'
```
bude náhodně směrovat každý HTTP požadavek přes jednu ze dvou uvedených outproxies (výstupní proxy) (squid.i2p a www1.squid.i2p). Díky tomu, pokud bude pár dalších lidí provozovat outproxies, nebudete tolik závislí na squid.i2p. Samozřejmě jste všichni slyšeli o mých obavách týkajících se outproxies, ale tato funkce lidem dává více možností.

V uplynulých několika hodinách jsme zaznamenali určitou nestabilitu, ale s pomocí duck a cervantes jsem identifikoval dvě závažné chyby a momentálně testuji opravy. Tyto opravy jsou zásadní, takže očekávám, že během jednoho až dvou dnů vydám verzi 0.3.4.2, jakmile ověřím výsledky.

## 2) Aktualizovaná dokumentace

Trochu jsme polevili, pokud jde o udržování dokumentace na webu aktuální, a přestože tam pořád zůstává několik velkých mezer (např. dokumentace k netDb a i2ptunnel), nedávno jsme některé z nich aktualizovali (srovnání sítí a FAQ). Jak se blížíme k vydáním 0.4 a 1.0, ocenil bych, kdyby lidé prošli web a podívali se, co lze zlepšit.

Za zvláštní zmínku stojí aktualizovaná Síň slávy - konečně jsme ji synchronizovali tak, aby odrážela štědré dary, které jste nám všichni poskytli (díky!). Do budoucna budeme tyto prostředky používat k odměňování vývojářů a dalších přispěvatelů, stejně jako k pokrytí vzniklých nákladů (např. poskytovatelé hostingu apod.).

## 3) 0.4 průběh

Když se ohlédneme za poznámkami z minulého týdne, ještě nám pro 0.4 zbývá pár věcí, ale simulace probíhají docela dobře a většina problémů s kaffe byla odhalena. Bylo by ale skvělé, kdybyste mohli důkladně otestovat různé aspekty routeru nebo klientských aplikací a nahlásit jakékoli chyby, na které narazíte.

## 4) ???

To je ode mě pro tuto chvíli vše – vážím si času, který tomu všichni věnujete, abychom se posunuli dál, a myslím, že děláme skvělý pokrok. Samozřejmě, pokud má někdo ještě něco, o čem chce mluvit, zaskočte na schůzku v #i2p... ehm... právě teď :)

=jr
