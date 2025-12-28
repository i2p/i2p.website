---
title: "Diskuse o tunnel"
description: "Historický přehled výplně pro tunnel, fragmentace a strategií sestavení"
slug: "tunnel"
layout: "single"
lastUpdated: "2019-07"
accurateFor: "0.9.41"
reviewStatus: "needs-review"
---

> **Poznámka:** Tento archiv zachycuje spekulativní návrhové práce vzniklé před verzí I2P 0.9.41. Pro produkční implementaci konzultujte [dokumentaci k tunnelu](/docs/specs/implementation/).

## Alternativy konfigurace

Zvažované nápady na budoucí parametry pro tunnel zahrnovaly:

- Omezování frekvence pro doručování zpráv
- Zásady vyplňování (včetně chaff injection (vkládání balastních dat))
- Řízení životnosti pro tunnel
- Strategie dávkování a frontování pro odesílání užitečných dat

Žádná z těchto možností nebyla součástí starší implementace.

## Strategie výplně

Projednávané možné přístupy k paddingu:

- Žádný padding (doplnění dat)
- Padding náhodné délky
- Padding pevné délky
- Padding na nejbližší kilobajt
- Padding na mocniny dvou (`2^n` bajtů)

Raná měření (verze 0.4) vedla k současné pevně stanovené velikosti zprávy pro tunnel 1024 bajtů. Na vyšší úrovni mohou garlic messages (garlic zprávy) přidat vlastní výplň.

## Fragmentace

Aby se zabránilo tagging attacks (útokům na základě označování) využívajícím délku zprávy, mají tunnelové zprávy pevnou velikost 1024 bajtů. Větší I2NP užitečná data fragmentuje vstupní brána tunnelu; koncový bod tunnelu fragmenty znovu sestaví v rámci krátkého časového limitu. Routery mohou fragmenty před odesláním přeuspořádat, aby maximalizovaly využití kapacity.

## Další alternativy

### Upravit zpracování Tunnel za běhu

Byly prozkoumány tři možnosti:

1. Umožnit, aby prostřední skok mohl dočasně přerušit tunnel udělením přístupu k dešifrovaným užitečným datům.
2. Povolit účastnícím se routerům “remixovat” zprávy tím, že je pošlou přes jeden ze svých vlastních odchozích tunnelů, než budou pokračovat k dalšímu skoku.
3. Umožnit tvůrci tunnelu dynamicky předefinovat další skok protějšku.

### Obousměrné Tunnels

Používání oddělených příchozích a odchozích tunnels omezuje množství informací, které může pozorovat jediná skupina uzlů (např. požadavek GET vs. velká odpověď). Obousměrné tunnels zjednodušují správu uzlů, ale zároveň odhalují úplné vzorce provozu v obou směrech. Jednosměrné tunnels proto zůstaly preferovaným návrhem.

### Zpětné kanály a proměnlivé velikosti

Povolení proměnlivých velikostí zpráv v rámci tunnel by umožnilo skryté kanály mezi spřaženými uzly (např. kódování dat prostřednictvím zvolených velikostí nebo frekvencí). Zprávy s pevnou velikostí toto riziko zmírňují za cenu dodatečné režie na vyplňovací data.

## Alternativy pro budování Tunnel

Odkaz: [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf)

### Starší „paralelní“ metoda sestavení

Před vydáním verze 0.6.1.10 byly požadavky na sestavení tunnelu odesílány paralelně každému účastníkovi. Tato metoda je zdokumentována na [staré stránce o tunnelu](/docs/legacy/old-implementation/).

### Jednorázové teleskopické budování (současná metoda)

Moderní přístup odesílá sestavovací zprávy po jednotlivých uzlech (hop-by-hop) skrz částečně sestavený tunnel. Ačkoli je podobný mechanismu Toru zvanému „telescoping“ (teleskopické vytváření okruhu), směrování sestavovacích zpráv přes explorační tunnely snižuje únik informací.

### “Interaktivní” Teleskopování

Budování po jednom skoku s explicitními round-trips (komunikací tam a zpět) umožňuje uzlům počítat zprávy a odvodit svou pozici v tunnel, proto byl tento přístup odmítnut.

### Neprůzkumné správní Tunnels

Jedním z návrhů bylo udržovat samostatný pool řídicích tunnels pro sestavovací provoz. Ačkoli by to mohlo pomoci odděleným routers, při dostatečné integraci sítě bylo vyhodnoceno jako zbytečné.

### Průzkumné doručování (zastaralé)

Před verzí 0.6.1.10 byly samostatné požadavky na tunnel zašifrovány pomocí garlic encryption a doručovány prostřednictvím průzkumných tunnels, přičemž odpovědi se vracely odděleně. Tato strategie byla nahrazena současnou metodou one-shot telescoping (jednorázového teleskopického navazování).

## Hlavní poznatky

- Zprávy v rámci tunnelu s pevnou velikostí chrání před označováním podle velikosti a skrytými kanály, a to navzdory dodatečným nákladům na výplň.
- Alternativní strategie vyplňování, fragmentace a sestavování byly prozkoumány, ale při zohlednění kompromisů v oblasti anonymity nebyly přijaty.
- Návrh tunnelu nadále vyvažuje efektivitu, pozorovatelnost a odolnost vůči útokům predecessor (útoky zaměřené na identifikaci předchůdce) a útokům využívajícím zahlcení.
