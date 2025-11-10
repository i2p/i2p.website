---
title: "Poznámky ke stavu I2P k 2004-10-26"
date: 2004-10-26
author: "jr"
description: "Týdenní aktualizace stavu I2P zahrnující stabilitu sítě, vývoj knihovny pro streamování, pokrok u mail.i2p a pokroky v BitTorrentu"
categories: ["status"]
---

Ahoj všichni, je čas na týdenní aktualizaci

## Rejstřík

1. Net status
2. Streaming lib
3. mail.i2p progress
4. ???

## 1) Stav sítě

Nechci to zakřiknout, ale poslední týden je síť v podstatě jako dřív - poměrně stabilní pro irc, eepsites(I2P Sites) se načítají spolehlivě, i když velké soubory stále často vyžadují obnovování stahování. V zásadě nic nového k hlášení, kromě skutečnosti, že není nic nového k hlášení.

Mimochodem, zjistili jsme jednu věc: i když Jetty podporuje HTTP resume (obnovení přerušeného stahování), dělá to pouze pro HTTP 1.1. To je v pořádku u většiny prohlížečů a nástrojů pro stahování, *kromě* wget - wget posílá požadavek na obnovení jako HTTP 1.0. Takže pro stahování velkých souborů použijte curl nebo nějaký jiný nástroj s podporou HTTP 1.1 resume (díky duck a ardvark za to, že se do toho ponořili a našli řešení!).

## 2) Streamovací knihovna

Protože byla síť poměrně stabilní, věnoval jsem téměř veškerý svůj čas práci na nové streamovací knihovně. I když ještě není hotová, podařilo se udělat hodně pokroku – všechny základní scénáře fungují bez problémů, klouzavá okna dobře zajišťují self-clocking (samotaktování) a z pohledu klienta nová knihovna slouží jako náhrada použitelná bez úprav za tu starou (ty dvě streamovací knihovny spolu však nedokážou komunikovat).

Posledních pár dní pracuji na některých zajímavějších scénářích. Nejdůležitější je síť s vysokou latencí, kterou simulujeme vkládáním zpoždění do přijatých zpráv - buď jednoduché náhodné zpoždění 0-30s, nebo stupňované zpoždění (80% času je zpoždění 0-10s, 10% @ 10-20s zpoždění, 5% @ 20-30s, 3% @ 30-40s, 4% @ 40-50s). Dalším důležitým testem bylo náhodné zahazování zpráv - to by na I2P nemělo být běžné, ale měli bychom si s tím umět poradit.

Celkový výkon byl poměrně dobrý, ale stále zbývá spousta práce, než to budeme moci nasadit na živou síť. Tato aktualizace bude 'nebezpečná' v tom, že je mimořádně výkonná - pokud to příšerně zkazíme, můžeme si během okamžiku způsobit vlastní DDoS, ale pokud to uděláme správně, no, řeknu jen, že v tom je obrovský potenciál (raději méně slíbit a více dodat).

Takže, jak už bylo řečeno, a protože je síť v poměrně 'stabilním stavu', nepospíchám s vydáním něčeho nedostatečně otestovaného. Další novinky, až budou.

## 3) Pokrok mail.i2p

postman a jeho tým tvrdě pracují na e‑mailu přes i2p (viz www.postman.i2p) a chystají se nějaké vzrušující novinky - možná pro nás má postman nějakou aktualizaci?

Mimochodem, chápu a rozumím volání po webovém rozhraní pro e‑mail, ale postman je zavalen prací na zajímavých věcech v backendu poštovního systému. Alternativou však je nainstalovat si webmailové rozhraní *lokálně* na svůj vlastní webový server - existují webmailové JSP/servlet aplikace. To by vám umožnilo provozovat vlastní lokální webmailové rozhraní např. na `http://localhost:7657/mail/`

Vím, že existují nějaké open source skripty pro přístup k pop3 účtům, což je půlka práce - možná by se někdo mohl poohlédnout po takových, které podporují pop3 a SMTP s autentizací? No tak, víš, že to chceš!

## 4) ???

OK, to je zatím všechno, co mám momentálně - stav se za pár minut na schůzce a dej nám vědět, co se děje.

=jr
