---
title: "Starší implementace Tunnelu (zastaralé)"
description: "Archivní popis návrhu pro tunnel, který se používal před I2P 0.6.1.10."
slug: "old-implementation"
lastUpdated: "2005-06"
accurateFor: "0.6.1"
reviewStatus: "needs-review"
---

> **Stav zastaralosti:** Tento obsah je zachován pouze pro historické referenční účely. Popisuje tunnel system, který byl distribuován před I2P&nbsp;0.6.1.10 a neměl by se používat pro moderní vývoj. Pro pokyny k produkčnímu nasazení viz [aktuální implementaci](/docs/specs/implementation/).

Původní tunnel subsystém také používal jednosměrné tunnels, ale lišil se uspořádáním zpráv, detekcí duplicit a strategií vytváření. Mnoho sekcí níže zrcadlí strukturu zastaralého dokumentu, aby usnadnilo srovnání.

## 1. Přehled Tunnel

- Tunnels byly vytvářeny jako uspořádané sekvence peerů vybraných tvůrcem.
- Tunnel lengths se pohybovaly v rozmezí 0–7 hopů, s několika možnostmi nastavení pro padding (doplnění dat), throttling (regulaci rychlosti) a chaff generation (generování šumu).
- Příchozí tunnels doručovaly zprávy z nedůvěryhodné brány k tvůrci (koncový bod); odchozí tunnels odesílaly data od tvůrce směrem ven.
- Životnost tunnels byla 10 minut, po uplynutí této doby se konstruovaly nové tunnels (často se stejnými peery, ale s odlišnými tunnel IDs).

## 2. Provoz v původním návrhu

### 2.1 Předzpracování zprávy

Brány shromáždily ≤32&nbsp;KB užitečných dat I2NP, zvolily výplň a vytvořily užitečná data obsahující:

- Dvoubytové pole délky výplně (padding length) a právě tolik náhodných bajtů
- Sekvence dvojic `{instructions, I2NP message}` popisujících cíle doručení, fragmentaci a volitelná zpoždění
- Celé zprávy I2NP zarovnané (výplní) na hranici 16 bajtů

Pokyny pro doručení zapouzdřovaly směrovací informace do bitových polí (typ doručení, příznaky zpoždění, příznaky fragmentace a volitelná rozšíření). Fragmentované zprávy obsahovaly 4bajtové ID zprávy a příznak indexu/posledního fragmentu.

### 2.2 Šifrování na bráně

Starší návrh stanovil délku tunnelu pro šifrovací fázi na osm skoků. Brány skládaly vrstvy AES-256/CBC spolu s bloky s kontrolním součtem, aby každý skok mohl ověřit integritu, aniž by se zmenšila užitečná data. Samotný kontrolní součet byl blok odvozený ze SHA-256, vložený do zprávy.

### 2.3 Chování účastníků

Účastníci sledovali ID příchozích tunnelů, včas ověřovali integritu a před přeposláním zahazovali duplikáty. Protože vycpávky a ověřovací bloky byly zabudovány, velikost zprávy zůstávala konstantní bez ohledu na počet skoků.

### 2.4 Zpracování koncového bodu

Koncové body postupně dešifrovaly vrstvené bloky, ověřily kontrolní součty a rozdělily užitečná data zpět na zakódované instrukce a zprávy I2NP pro další doručení.

## 3. Sestavování tunnelů (zastaralý proces)

1. **Výběr peerů:** Peerové byli vybíráni z lokálně spravovaných profilů (průzkumné (exploratory) vs. klientské (client)). Původní dokument už zdůrazňoval zmírnění [útoku předchůdce](https://en.wikipedia.org/wiki/Predecessor_attack) opětovným používáním seřazených seznamů peerů pro každý tunnel pool.
2. **Doručování požadavků:** Zprávy pro sestavení byly předávány postupně (hop-by-hop) se šifrovanými částmi pro každý peer. Alternativní nápady, jako teleskopické rozšiřování (telescopic extension), přesměrování uprostřed cesty (midstream rerouting) nebo odstranění bloků kontrolních součtů, byly diskutovány jako experimenty, ale nikdy nebyly přijaty.
3. **Poolování:** Každá místní destinace měla samostatné příchozí a odchozí pooly. Nastavení zahrnovala požadované množství, záložní tunnels, variabilitu délky, omezování rychlosti a zásady výplně (padding).

## 4. Koncepty škrcení a mixování

Starší dokument navrhl několik strategií, které ovlivnily pozdější vydání:

- Vážené náhodné předčasné zahazování (WRED) pro řízení zahlcení
- Limity pro každý tunnel založené na klouzavých průměrech nedávného využití
- Volitelné chaff (výplňová data) a řízení dávkování (není plně implementováno)

## 5. Archivované alternativy

Části původního dokumentu se zabývaly myšlenkami, které nikdy nebyly nasazeny:

- Odstranění bloků kontrolního součtu ke snížení zpracování na každém hopu
- Teleskopické rozšiřování tunnels za běhu za účelem změny složení uzlů
- Přechod na obousměrné tunnels (nakonec zamítnuto)
- Použití kratších hashů nebo odlišných schémat doplňování

Tyto myšlenky mají i nadále hodnotu jako historický kontext, ale neodrážejí moderní kódovou základnu.

## Reference

- Původní archiv zastaralých dokumentů (před verzí 0.6.1.10)
- [Přehled Tunnel](/docs/overview/tunnel-routing/) pro aktuální terminologii
- [Profilování a výběr protějšků](/docs/overview/tunnel-routing#peer-selection/) pro moderní heuristiky
