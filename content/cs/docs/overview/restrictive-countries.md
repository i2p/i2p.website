---
title: "Striktní/restriktivní země"
description: "Jak se I2P chová v jurisdikcích s omezeními na směrování nebo nástroje pro anonymitu (Hidden Mode a striktní seznam)"
slug: "restrictive-countries"
lastUpdated: "2024-07"
accurateFor: "2.10.0"
type: docs
reviewStatus: "needs-review"
---

Tato implementace I2P (Java implementace distribuovaná na tomto webu) obsahuje „Seznam přísných zemí", který slouží k úpravě chování routeru v regionech, kde může být účast na směrování pro ostatní omezena zákonem. Přestože nejsme si vědomi jurisdikcí, které by zakazovaly používání I2P, několik z nich má široké zákazy přeposílání provozu. Routery, které se zdají být v „přísných" zemích, jsou automaticky přepnuty do skrytého režimu.

Projekt odkazuje na výzkum organizací pro občanská a digitální práva při těchto rozhodnutích. Zejména průběžný výzkum Freedom House ovlivňuje naše volby. Obecné vodítko je zahrnout země s hodnocením občanských svobod (CL) 16 nebo méně, nebo s hodnocením svobody internetu 39 nebo méně (není svobodný).

## Shrnutí skrytého režimu

Když je router přepnut do režimu Hidden, změní se tři klíčové věci v jeho chování:

- Nepublikuje RouterInfo do netDb.
- Nepřijímá participující tunely.
- Odmítá přímá připojení k routerům ve stejné zemi.

Tyto obranné mechanismy ztěžují spolehlivé mapování routerů a snižují riziko porušení místních zákazů týkajících se přeposílání provozu pro ostatní.

## Seznam zemí s přísnými omezeními (k roku 2024)

```
/* Afghanistan */ "AF",
/* Azerbaijan */ "AZ",
/* Bahrain */ "BH",
/* Belarus */ "BY",
/* Brunei */ "BN",
/* Burundi */ "BI",
/* Cameroon */ "CM",
/* Central African Republic */ "CF",
/* Chad */ "TD",
/* China */ "CN",
/* Cuba */ "CU",
/* Democratic Republic of the Congo */ "CD",
/* Egypt */ "EG",
/* Equatorial Guinea */ "GQ",
/* Eritrea */ "ER",
/* Ethiopia */ "ET",
/* Iran */ "IR",
/* Iraq */ "IQ",
/* Kazakhstan */ "KZ",
/* Laos */ "LA",
/* Libya */ "LY",
/* Myanmar */ "MM",
/* North Korea */ "KP",
/* Palestinian Territories */ "PS",
/* Pakistan */ "PK",
/* Rwanda */ "RW",
/* Saudi Arabia */ "SA",
/* Somalia */ "SO",
/* South Sudan */ "SS",
/* Sudan */ "SD",
/* Eswatini (Swaziland) */ "SZ",
/* Syria */ "SY",
/* Tajikistan */ "TJ",
/* Thailand */ "TH",
/* Turkey */ "TR",
/* Turkmenistan */ "TM",
/* Venezuela */ "VE",
/* United Arab Emirates */ "AE",
/* Uzbekistan */ "UZ",
/* Vietnam */ "VN",
/* Western Sahara */ "EH",
/* Yemen */ "YE"
```
Pokud si myslíte, že by měla být země přidána nebo odebrána ze striktního seznamu, otevřete prosím issue: https://i2pgit.org/i2p/i2p.i2p/

Reference: Freedom House – https://freedomhouse.org/
