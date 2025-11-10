---
title: "Poznámky ke stavu I2P k 2004-11-16"
date: 2004-11-16
author: "jr"
description: "Týdenní aktualizace stavu I2P pokrývající problémy s přetížením sítě, pokroky ve streamovací knihovně, pokrok v BitTorrentu a plány nadcházejícího vydání"
categories: ["status"]
---

Ahoj všichni, je zase úterý.

## Rejstřík

1. Congestion
2. Streaming
3. BT
4. ???

## 1) Přetížení

Vím, že tím porušuji zvyk nazývat bod 1 "Stav sítě", ale tento týden se jako výstižnější jeví "congestion" (zahlcení). Samotná síť si vedla docela dobře, ale s rostoucím používáním BitTorrentu se věci začaly čím dál víc ucpávat, což v podstatě vedlo ke kolapsu způsobenému zahlcením.

To se dalo očekávat a jen to posiluje náš plán - vydat novou streamingovou knihovnu a přepracovat správu tunnel tak, abychom měli dostatek dat o uzlech k použití ve chvíli, kdy naše rychlé uzly selžou. V nedávných problémech sítě sehrály roli i další faktory, ale většinu lze připsat zvýšenému zahlcení a následným selháním tunnel (která zase vedla k nejrůznějším chaotickým volbám uzlů).

## 2) Streamování

Došlo k výraznému pokroku ve streamovací knihovně a mám na ni přes živou síť napojený proxy Squid, takže jsem ho často používal pro své běžné prohlížení webu. S pomocí mule jsme ty proudy dost tvrdě zatěžovali tím, že jsme přes síť pouštěli frost a FUQID (bože, než jsem tohle začal dělat, vůbec jsem si neuvědomoval, jak moc je frost agresivní!). Tímto způsobem se podařilo vypátrat několik významných dlouhodobých chyb a byly přidány i některé úpravy, které pomáhají zvládat obrovské množství spojení.

Objemové datové proudy fungují také skvěle, a to jak s pomalým startem, tak s vyhýbáním se zahlcení, a rychlá spojení typu odeslání/odpověď (např. jako HTTP get+response) dělají přesně to, co mají.

Očekávám, že přizveme pár dobrovolníků, aby to v příštích několika dnech zkusili nasadit ve větším rozsahu, a snad se tak brzy dostaneme na verzi 0.4.2. Nechci tvrdit, že to bude tak dobré, že vám ještě umyje nádobí, a jsem si jistý, že nějaké chyby přece jen proklouznou, ale vypadá to slibně.

## 3) BT

Když pomineme nedávné potíže v síti, port i2p-bt postupuje mílovými kroky. Vím o několika lidech, kteří přes něj stáhli více než 1 GB dat, a výkon je takový, jak se očekávalo (kvůli staré streamingové knihovně, ~4KBps na peer v roji). Snažím se sledovat práci probíranou na kanálu #i2p-bt - možná by nám duck mohl na schůzce podat shrnutí?

## 4) ???

To je ode mě prozatím všechno. Uvidíme se na schůzce za pár minut.

=jr
