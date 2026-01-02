---
title: "Diskuse o síťové databázi"
description: "Historické poznámky k floodfill, experimentům s Kademlií a budoucímu ladění netDb"
slug: "netdb"
reviewStatus: "needs-review"
---

> **Poznámka:** Tato archivní diskuse nastiňuje historické přístupy k síťové databázi (netDb). Podrobnosti o aktuálním chování a pokynech najdete v [hlavní dokumentaci netDb](/docs/specs/common-structures/).

## Historie

netDb projektu I2P je distribuována pomocí jednoduchého algoritmu floodfill. Ranější vydání také ponechávala implementaci Kademlia DHT jako záložní možnost, ale ta se ukázala jako nespolehlivá a byla ve verzi 0.6.1.20 zcela deaktivována. Návrh floodfill předá publikovaný záznam účastnickému routeru, počká na potvrzení a v případě potřeby to zkusí znovu s dalšími floodfill uzly. Floodfill uzly rozposílají 'store' (zprávy pro uložení) z non-floodfill routerů všem ostatním účastníkům floodfill.

Koncem roku 2009 byly dotazy Kademlia (distribuovaná hašovací tabulka) částečně znovu zavedeny, aby se snížily požadavky na úložiště jednotlivých floodfill routers.

### Úvod do Floodfill

Floodfill se poprvé objevil ve vydání 0.6.0.4, zatímco Kademlia zůstala k dispozici jako záloha. Tehdy velká ztráta paketů a omezené směrovací cesty ztěžovaly získání potvrzení od čtyř nejbližších protějšků, což často vyžadovalo desítky redundantních pokusů o uložení. Přechod na podmnožinu floodfill tvořenou zvenčí dosažitelnými routers poskytl pragmatické krátkodobé řešení.

### Přehodnocení Kademlia (distribuovaná hašovací tabulka, DHT)

Mezi zvažované alternativy patřily:

- Provoz netDb jako Kademlia DHT, omezený na dosažitelné routers, které se k účasti přihlásí
- Zachování modelu floodfill, ale omezení účasti na schopné routers a ověřování distribuce náhodnými kontrolami

Přístup floodfill zvítězil, protože byl snazší nasadit a netDb uchovává pouze metadata, nikoli uživatelská data. Většina destinací nikdy nepublikuje LeaseSet, protože odesílatel typicky zahrne svůj LeaseSet do garlic messages (garlic zprávy).

## Současný stav (z historického hlediska)

Algoritmy netDb jsou vyladěny pro potřeby sítě a historicky bez potíží zvládaly několik stovek routerů. Rané odhady naznačovaly, že 3–5 floodfill routerů by dokázalo obsloužit zhruba 10 000 uzlů.

### Aktualizované výpočty (březen 2008)

```
recvKBps = N * (L + 1) * (1 + F) * (1 + R) * S / T
```
Kde:

- `N`: Routery v síti
- `L`: Průměrný počet klientských destinací na router (plus jedna pro `RouterInfo`)
- `F`: Procento selhání tunnelů
- `R`: Období přestavby tunnelu jako zlomek životnosti tunnelu
- `S`: Průměrná velikost záznamu netDb
- `T`: Životnost tunnelu

Při použití hodnot platných v roce 2008 (`N = 700`, `L = 0.5`, `F = 0.33`, `R = 0.5`, `S = 4 KB`, `T = 10 minutes`) vychází:

```
recvKBps ≈ 700 * (0.5 + 1) * (1 + 0.33) * (1 + 0.5) * 4 KB / 10m ≈ 28 KBps
```
### Vrátí se Kademlia?

Vývojáři zhruba na začátku roku 2007 diskutovali o opětovném zavedení Kademlia. Panoval konsenzus, že kapacitu floodfill lze podle potřeby postupně rozšiřovat, zatímco Kademlia přidávala značnou složitost a nároky na zdroje pro základní populaci routerů. Záložní varianta zůstává nečinná, dokud je kapacita floodfill dostačující.

### Plánování kapacity floodfillu (uzel v I2P, který spravuje netDb)

Automatické zařazování routerů třídy šířky pásma `O` do floodfill, byť lákavé, představuje riziko scénářů odepření služby (denial-of-service), pokud se do něj zapojí nepřátelské uzly. Historická analýza naznačila, že omezení skupiny floodfill (například 3–5 uzlů obsluhujících ~10K routers) bylo bezpečnější. K udržení dostatečné, avšak kontrolované sady floodfill byli nasazováni důvěryhodní provozovatelé nebo se uplatňovaly automatické heuristiky.

## Floodfill TODO (Historické)

> Tato sekce je zachována pro historické účely. Hlavní stránka netDb sleduje aktuální plán rozvoje a návrhové úvahy.

Provozní incidenty, jako například období 13. března 2008, kdy byl k dispozici pouze jeden floodfill router, vedly k několika vylepšením zahrnutým ve verzích 0.6.1.33 až 0.7.x, včetně:

- Náhodný výběr floodfill pro vyhledávání a upřednostnění rychle reagujících peerů
- Zobrazení dalších metrik floodfill na stránce "Profiles" konzole routeru
- Postupné zmenšování velikosti záznamů v netDb za účelem snížení využití šířky pásma u floodfill
- Automatické zapojení (opt-in) podmnožiny routerů třídy `O` na základě výkonu zjištěného z profilových dat
- Vylepšené blokování pomocí blokovacích seznamů, výběr floodfill peerů a heuristiky průzkumu

Zbývající nápady z daného období zahrnovaly:

- Využití statistik `dbHistory` pro lepší hodnocení a výběr floodfill protějšků
- Zlepšení chování při opakování pokusů, aby se předešlo opakovanému kontaktování selhávajících protějšků
- Využití metrik latence a skóre integrace při výběru
- Rychlejší detekce a reakce na selhávající floodfill routery
- Pokračování ve snižování nároků na zdroje u uzlů s vysokou šířkou pásma a u floodfill uzlů

I v době sepsání těchto poznámek byla síť považována za odolnou, s připravenou infrastrukturou pro rychlou reakci na nepřátelské floodfills nebo na útoky typu odmítnutí služby cílené na floodfill.

## Další poznámky

- Konzole routeru dlouhodobě zpřístupňuje rozšířená profilová data, která pomáhají při analýze spolehlivosti floodfill.
- Ačkoli se v historických komentářích spekulovalo o Kademlia a alternativních schématech DHT, floodfill zůstal hlavním algoritmem pro produkční sítě.
- Na budoucnost zaměřený výzkum se soustředil na to, aby byl mechanismus přijímání do floodfill adaptivní, zároveň aby se omezily příležitosti ke zneužití.
