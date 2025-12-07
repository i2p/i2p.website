---
title: "Akademický výzkum"
description: "Informace a pokyny pro akademický výzkum v síti I2P"
layout: "research"
---

<div id="intro"></div>

## Akademický výzkum I2P

Existuje velká výzkumná komunita zkoumající širokou škálu aspektů anonymity. Aby mohly sítě pro anonymitu pokračovat ve zlepšování, věříme, že je nutné pochopit problémy, kterým čelíme. Výzkum sítě I2P je stále v počátcích, přičemž většina dosavadního výzkumu se zaměřila na jiné sítě pro anonymitu. To představuje jedinečnou příležitost pro původní vědecké přínosy.

<div id="notes"></div>

## Poznámky pro výzkumníky

### Priority obranného výzkumu

Vítáme výzkum, který nám pomáhá posílit síť a zlepšit její bezpečnost. Testování, které posiluje infrastrukturu I2P, je podporováno a oceňováno.

### Pokyny pro komunikaci výzkumu

Silně povzbuzujeme výzkumníky, aby své výzkumné nápady co nejdříve komunikovali s vývojovým týmem. To pomáhá:

- Vyhnout se možnému překrývání se stávajícími projekty
- Minimalizovat potenciální poškození sítě
- Koordinovat úsilí o testování a sběr dat
- Zajistit, že výzkum bude v souladu s cíli sítě

<div id="ethics"></div>

## Etika výzkumu a pokyny pro testování

### Obecné principy

Při provádění výzkumu v I2P zvažte následující:

1. **Posouzení přínosů vs. rizik výzkumu** - Zvažte, zda potenciální přínosy vašeho výzkumu převýší jakákoli rizika pro síť nebo její uživatele
2. **Preferujte testovací síť před ostrou sítí** - Kdykoli je to možné, použijte konfiguraci testovací sítě I2P
3. **Shromažďujte pouze nezbytná data** - Sbírejte pouze minimum dat potřebné pro váš výzkum
4. **Zajistěte, že publikovaná data respektují soukromí uživatelů** - Jakákoli publikovaná data by měla být anonymizována a respektovat soukromí uživatelů

### Metody testování sítě

Pro výzkumníky, kteří potřebují provádět testy na I2P:

- **Používejte konfiguraci testovací sítě** - I2P lze nakonfigurovat pro provoz na izolované testovací síti
- **Využívejte režim MultiRouter** - Pro testování provozujte více instancí routeru na jednom stroji
- **Konfigurujte rodinu routeru** - Umožněte, aby vaše výzkumné routery byly identifikovatelné jejich konfigurací jako rodina routerů

### Doporučené praktiky

- **Kontaktujte tým I2P před testováním na ostré síti** - Obraťte se na nás na research@i2p.net před prováděním jakýchkoli testů na ostré síti
- **Používejte konfiguraci rodiny routerů** - To činí vaše výzkumné routery průhlednými pro síť
- **Zabraňte potenciálnímu rušení sítě** - Navrhněte své testy tak, aby minimalizovaly jakýkoli negativní dopad na běžné uživatele

<div id="questions"></div>

## Otevřené výzkumné otázky

Komunita I2P identifikovala několik oblastí, kde by byl výzkum obzvláště cenný:

### Databáze sítě

**Floodfill:**
- Existují jiné způsoby, jak zmírnit „brute-force“ útoky v síti prostřednictvím významné kontroly floodfillu?
- Existuje způsob, jak detekovat, označit a případně odstranit „špatné floodfille“ bez nutnosti spoléhat na formu ústřední autority?

### Transportní protokoly

- Jak by bylo možné vylepšit strategie pro opakovaný přenos paketů a časové limity?
- Existuje způsob, jak by I2P mohlo efektivněji maskovat pakety a snižovat analýzu provozu?

### Tunely a destinace

**Výběr vrstevníků:**
- Existuje způsob, jak by I2P mohlo provádět výběr vrstevníků efektivněji nebo bezpečněji?
- Mělo by použití geoip pro upřednostňování blízkých vrstevníků negativní dopad na anonymitu?

**Jednosměrné tunely:**
- Jaké jsou přínosy jednosměrných tunelů oproti obousměrným tunelům?
- Jaké jsou kompromisy mezi jednosměrnými a obousměrnými tunely?

**Multihoming:**
- Jak efektivní je multihoming při vyvažování zátěže?
- Jak se škáluje?
- Co se stane, když více routerů hostí stejnou destinaci?
- Jaké jsou kompromisy v oblasti anonymity?

### Směrování zpráv

- Nakolik je snížena efektivita útoků na časování fragmentací a mícháním zpráv?
- Jaké strategie míchání by mohlo I2P přijmout?
- Jak lze účinně uplatnit techniky s vysokou latencí uvnitř nebo vedle naší sítě s nízkou latencí?

### Anonymita

- Jak významně ovlivňuje otisk prohlížeče anonymitu uživatelů I2P?
- Přínosilo by průměrným uživatelům vyvinout balíček prohlížeče?

### Příbuzné k síti

- Jaký má celkový dopad na síť chování „nenasytných uživatelů“?
- Byly by další kroky pro podporu účasti na šířce pásma hodnotné?

<div id="contact"></div>

## Kontakt

Pro dotazy týkající se výzkumu, příležitostí ke spolupráci nebo k diskusi o vašich výzkumných plánech nás prosím kontaktujte na:

**Email:** research@i2p.net

Těšíme se na spolupráci s výzkumnou komunitou na zlepšení sítě I2P!
