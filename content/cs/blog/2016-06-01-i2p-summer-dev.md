---
title: "I2P letní vývoj"
date: 2016-06-01
author: "str4d"
description: "S potěšením oznamujeme, že toto léto I2P zahájí vývojový program zaměřený na zlepšení ekosystému softwaru pro ochranu soukromí jak pro vývojáře, tak pro uživatele."
categories: ["summer-dev"]
---

V uplynulých několika letech se stále zřetelněji ukazuje, že je nezbytné, aby uživatelé měli kontrolu nad svými vlastními daty. V tomto ohledu bylo dosaženo vynikajícího pokroku s nástupem komunikačních aplikací jako Signal a systémů pro ukládání souborů jako Tahoe-LAFS. Probíhající práce projektu Let's Encrypt na tom, aby se HTTPS rozšířilo po celém světě, stabilně nabírá na síle.

Avšak zabudovat ochranu soukromí a anonymitu do aplikací není triviální. Velká část softwaru, který lidé denně používají, nebyla navržena tak, aby chránila soukromí, a nástroje, které mají vývojáři k dispozici, se obecně nepracuje snadno. Nedávno zveřejněný průzkum OnionScan poskytuje představu o tom, jak snadné je i pro technicky zdatné uživatele své služby nesprávně nakonfigurovat, čímž zcela podkopají své záměry.

## Pomáháme vývojářům pomáhat svým uživatelům

S potěšením oznamujeme, že toto léto se I2P pustí do vývojového programu zaměřeného na zlepšení ekosystému softwaru pro ochranu soukromí. Naším cílem je usnadnit život jak vývojářům, kteří chtějí využít I2P ve svých aplikacích, tak uživatelům, kteří se snaží své aplikace přes I2P konfigurovat a provozovat.

We will be focusing our time this summer into three complementary areas:

### June: APIs

V červnu aktualizujeme různé knihovny určené pro práci s I2P. Letos jsme dosáhli významného pokroku v rozšíření našeho SAM API o další funkce, například podporu datagramů a portů. Plánujeme, aby byly tyto funkce snadno dostupné v našich knihovnách pro C++ a Python.

Brzy také výrazně usnadníme vývojářům pro Javu a Android přidání podpory I2P do jejich aplikací. Sledujte novinky!

### Červen: rozhraní API

V červenci budeme spolupracovat s aplikacemi, které projevily zájem přidat podporu pro I2P. V oblasti ochrany soukromí se právě teď rozvíjí několik opravdu zajímavých nápadů a chceme jejich komunitám pomoci využít více než desetiletí výzkumu a vývoje v oblasti peer‑to‑peer anonymity. Rozšíření těchto aplikací tak, aby nativně fungovaly přes I2P, je dobrým krokem vpřed z hlediska použitelnosti a zároveň zlepší způsob, jakým tyto aplikace uvažují o informacích o uživatelích a jak s nimi nakládají.

### Červenec: Aplikace

Finally, in August we will turn out attention to the apps we bundle inside I2P, and the wider array of plugins. Some of these are due for some love, to make them more user-friendly - as well as fix any outstanding bugs! We hope that longtime I2P supporters will enjoy the outcome of this work.

## Take part in Summer Dev!

Máme ještě spoustu dalších nápadů na věci, které bychom v těchto oblastech chtěli realizovat. Pokud vás láká podílet se na vývoji softwaru pro ochranu soukromí a anonymity, navrhování uživatelsky přívětivých webů a rozhraní nebo psaní návodů pro uživatele: přijďte si s námi popovídat na IRC nebo na Twitteru! Vždy rádi přivítáme nováčky v naší komunitě. Všem novým přispěvatelům, kteří se zapojí, pošleme I2P samolepky!

Stejně tak, pokud jste vývojář aplikací, který chce pomoc s integrací I2P, nebo si chcete jen popovídat o konceptech či detailech: ozvěte se! Pokud se chcete zapojit do našeho červencového měsíce aplikací, kontaktujte @GetI2P, @i2p nebo @str4d na Twitteru. Najdete nás také v #i2p-dev na OFTC nebo FreeNode.

Budeme zde průběžně zveřejňovat novinky, ale můžete také sledovat náš postup a sdílet své vlastní nápady a práci na Twitteru s hashtagem #I2PSummer. Sem s létem!
