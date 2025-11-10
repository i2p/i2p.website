---
title: "Poznámky o stavu I2P k 2005-03-08"
date: 2005-03-08
author: "jr"
description: "Týdenní poznámky o stavu vývoje I2P zahrnující vylepšení ve vydání 0.5.0.2, zaměření na spolehlivost sítě a aktualizace e-mailových a BitTorrentových služeb"
categories: ["status"]
---

Ahoj všichni, je čas na týdenní aktualizaci

* Index

1) 0.5.0.2 2) aktualizace mail.i2p 3) aktualizace i2p-bt 4) ???

* 1) 0.5.0.2

Před pár dny jsme vydali verzi 0.5.0.2 a značná část sítě už aktualizovala (hurá!). Přicházejí hlášení, že nejhorší problémy z 0.5.0.1 byly odstraněny a celkově se zdá, že vše funguje v pořádku. Pořád jsou tu ale nějaké problémy se spolehlivostí, i když streaming lib (knihovna pro streamování) to zatím zvládá (irc připojení trvající 12-24+ hodin se zdají být normou). Snažím se dohledat některé zbývající problémy, ale bylo by opravdu, opravdu dobré, kdyby všichni co nejdřív přešli na nejnovější verzi.

Abychom se posunuli dál, je klíčová spolehlivost. Teprve až drtivá většina zpráv, které mají projít, skutečně projde, bude se pracovat na zlepšení propustnosti. Kromě dávkovacího tunnel preprocesoru bychom mohli prozkoumat i další rozměr: vkládat do profilů více údajů o latenci. V současnosti pro určování „rychlostního“ pořadí jednotlivých peerů používáme jen testovací zprávy a zprávy pro správu tunnel, ale zřejmě bychom měli zachytit jakékoli měřitelné hodnoty RTT (round-trip time) i u dalších akcí, například u netDb a dokonce i u end‑to‑end klientských zpráv. Na druhou stranu je budeme muset odpovídajícím způsobem vážit, protože u end‑to‑end zprávy nedokážeme oddělit čtyři složky měřitelného RTT (náš odchozí, jejich příchozí, jejich odchozí, náš příchozí). Možná můžeme použít nějaké garlic triky a svázat zprávu cílenou na jeden z našich příchozích tunnel společně s některými odchozími zprávami, čímž vyřadíme na druhé straně tunnel z měřicí smyčky.

* 2) mail.i2p updates

Ok, nevím, jaké aktualizace pro nás postman má připravené, ale během schůzky přijde aktualizace.  Podívejte se do logů, ať se to dozvíte!

* 3) i2p-bt update

Nevím, jaké novinky pro nás mají duck a parta, ale doslechl jsem se nějaké zvěsti o pokroku na kanále. Možná z něj vyloudíme nějakou aktualizaci.

* 4) ???

Strašně moc se toho děje, ale pokud je něco konkrétního, co byste chtěli otevřít a probrat, stavte se na schůzce za pár minut. A jen připomínka: pokud jste ještě neaktualizovali, prosím udělejte to co nejdřív (aktualizace je neuvěřitelně jednoduchá - stáhnete soubor, kliknete na tlačítko)

=jr
