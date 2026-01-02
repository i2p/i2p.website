---
title: "Seznamte se se svým správcem: StormyCloud"
date: 2022-09-07
author: "sadie"
description: "Rozhovor se správci StormyCloud Outproxy (výstupní proxy)"
categories: ["general"]
API_Translate: pravda
---

## Rozhovor se společností StormyCloud Inc.

S nejnovějším [vydáním I2P Java](https://geti2p.net/en/blog/2022/08/22/1.9.0-Release), byl stávající outproxy false.i2p nahrazen novým outproxy StormyCloud pro nové instalace I2P. Pro uživatele, kteří aktualizují svůj router, lze přechod na službu Stormycloud provést rychle.

Ve Správci skrytých služeb změňte obě položky Outproxies i SSL Outproxies na exit.stormycloud.i2p a klikněte na tlačítko Uložit ve spodní části stránky.

## Kdo je StormyCloud Inc?

**Poslání společnosti StormyCloud Inc.**

Obhajovat přístup k internetu jako univerzální lidské právo. Tím skupina chrání elektronické soukromí uživatelů a buduje komunitu podporou neomezeného přístupu k informacím, a tím i svobodné výměny myšlenek napříč hranicemi. Je to zásadní, protože internet je nejsilnějším dostupným nástrojem k dosažení pozitivní změny ve světě.

**Prohlášení o vizi**

Stát se průkopníkem v poskytování svobodného a otevřeného internetu všem ve vesmíru, protože přístup k internetu je základní lidské právo ([https://stormycloud.org/about-us/](https://stormycloud.org/about-us/))

Setkal jsem se s Dustinem, abychom se pozdravili a více si promluvili o soukromí, o potřebě služeb, jako je StormyCloud, a o tom, co společnost přivedlo k I2P.

**Co bylo inspirací k založení StormyCloud?**

Na konci roku 2021 jsem byl na subredditu /r/tor. V jednom vlákně o tom, jak používat Tor, odpověděl člověk, který uvedl, že se spoléhá na Tor, aby zůstal v kontaktu se svou rodinou. Rodina toho člověka žila ve Spojených státech, ale tato osoba tehdy žila v zemi, kde byl přístup k internetu velmi omezený. Musela být velmi opatrná ohledně toho, s kým komunikuje a co říká. Z těchto důvodů se spoléhala na Tor. Zamyslel jsem se nad tím, že mohu komunikovat s lidmi bez strachu ani omezení a že tak by to mělo být pro všechny.

Cílem StormyCloud je pomoci co nejvíce lidem, aby to mohli udělat.

**Jaké byly některé z výzev při rozjezdu StormyCloud?**

Ty náklady — je to neskutečně drahé. Zvolili jsme řešení v datovém centru, protože rozsah toho, co děláme, není něco, co by šlo zvládnout na domácí síti. Jsou tu výdaje na vybavení a opakující se náklady na hosting.

Při zakládání neziskové organizace jsme se vydali ve stopách Emerald Onion a využili některé jejich dokumenty a získané poznatky. Komunita Tor má k dispozici mnoho velmi užitečných zdrojů.

**Jaké byly ohlasy na vaše služby?**

V červenci jsme napříč všemi našimi službami obsloužili 1,5 miliardy DNS dotazů. Lidé oceňují, že neprobíhá žádné logování. Ta data prostě nejsou k dispozici a lidem se to líbí.

**Co je to outproxy?**

Outproxy (výstupní proxy) je podobný výstupním uzlům Toru a umožňuje, aby byl clearnet (běžný internetový provoz) přeposílán přes síť I2P. Jinými slovy umožňuje uživatelům I2P přistupovat k internetu v bezpečí sítě I2P.

**Co je zvláštního na StormyCloud I2P Outproxy?**

Pro začátek jsme multi-homed, což znamená, že máme několik serverů, které obsluhují outproxy provoz. To zajišťuje, že je služba pro komunitu vždy dostupná. Veškeré logy na našich serverech se každých 15 minut mažou. To zajišťuje, že k žádným datům nemají přístup ani orgány činné v trestním řízení, ani my sami. Podporujeme návštěvu odkazů .onion přes outproxy a naše outproxy je poměrně rychlé.

**Jak definujete soukromí? Jaké problémy spojené s nepřiměřenými zásahy a nakládáním s daty vnímáte?**

Soukromí je ochrana před neoprávněným přístupem. Transparentnost je důležitá, například opt-in (aktivní souhlas) — příkladem jsou požadavky GDPR.

Existují velké společnosti, které hromadí data, jež jsou využívána k [přístupu k údajům o poloze bez soudního příkazu](https://www.eff.org/deeplinks/2022/08/fog-revealed-guided-tour-how-cops-can-browse-your-location-data). Dochází k neoprávněnému zasahování technologických společností do toho, co lidé považují za soukromé — a co by soukromé být mělo — například do věcí, jako jsou fotografie nebo zprávy.

Je důležité nadále dělat osvětu o tom, jak udržet komunikaci v bezpečí, a jaké nástroje či aplikace v tom lidem pomohou. Důležitý je také způsob, jakým zacházíme se všemi dostupnými informacemi. Musíme důvěřovat, ale prověřovat.

**Jak I2P zapadá do prohlášení o poslání a vizi společnosti StormyCloud?**

I2P je projekt s otevřeným zdrojovým kódem a to, co nabízí, je v souladu s posláním společnosti StormyCloud Inc. I2P poskytuje vrstvu soukromí a ochrany pro síťový provoz a komunikaci a projekt věří, že každý má právo na soukromí.

O I2P jsme se dozvěděli na začátku roku 2022, když jsme mluvili s lidmi z komunity Tor, a líbilo se nám, co projekt dělá. Zdálo se, že je podobné Toru.

Během našeho seznamování s I2P a jeho možnostmi jsme zjistili, že je potřeba spolehlivého outproxy (výstupní proxy). Od lidí z komunity I2P jsme získali opravdu skvělou podporu k vytvoření a zahájení poskytování služby outproxy.

**Závěr**

Potřeba povědomí o sledování toho, co by v našich online životech mělo zůstat soukromé, je stále aktuální. Shromažďování jakýchkoli dat by mělo probíhat se souhlasem a soukromí by mělo být samozřejmostí.

Tam, kde nemůžeme důvěřovat, že náš provoz ani komunikace nebudou bez našeho souhlasu monitorovány, naštěstí máme přístup k sítím, které již ze svého návrhu anonymizují provoz a skrývají naši polohu.

Děkuji StormyCloud a všem, kdo poskytují výstupní proxy nebo uzly pro Tor a I2P, aby lidé mohli v případě potřeby bezpečněji přistupovat k internetu. Těším se na to, že více lidí bude propojovat možnosti těchto vzájemně se doplňujících sítí, aby vznikl robustnější ekosystém ochrany soukromí pro všechny.

Zjistěte více o službách společnosti StormyCloud Inc. na [https://stormycloud.org/](https://stormycloud.org/) a podpořte jejich práci poskytnutím daru na [https://stormycloud.org/donate/](https://stormycloud.org/donate/).
