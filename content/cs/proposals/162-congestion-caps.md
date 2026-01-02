---
title: "Limity Zácpy"
number: "162"
author: "dr|z3d, idk, orignal, zzz"
created: "2023-01-24"
lastupdated: "2023-02-01"
status: "Open"
thread: "http://zzz.i2p/topics/3516"
target: "0.9.59"
toc: true
---

## Přehled

Přidejte indikátory zácpy do publikovaných informací o směrovači (RI).


## Motivace

Šířkové "limity" (schopnosti) indikují sdílené limity šířky pásma a dosažitelnost, ale ne stav zácpy.
Indikátor zácpy pomůže směrovačům vyhnout se pokusům o budování přes ucpaný směrovač,
což přispívá k větší zácpě a snížené úspěšnosti budování tunelu.


## Návrh

Definujte nové limity pro indikaci různých úrovní zácpy nebo problémů s kapacitou.
Tyto limity budou umístěny v nejvyšší úrovni RI, ne v adresových limitech.


### Definice Zácpy

Zácpa obecně znamená, že peer pravděpodobně
neobdrží a nepřijme žádost o vytvoření tunelu.
Jak definovat nebo klasifikovat úrovně zácpy je specifičtí pro implementaci.

Implementace mohou zvážit jednu nebo více z následujících možností:

- Na nebo blízko limitů šířky pásma
- Na nebo blízko maximu účastnických tunelů
- Na nebo blízko maximu připojení na jednom nebo více protokolech
- Nad prahovou hodnotou pro hloubku fronty, latenci nebo využití CPU; přetečení interní fronty
- Základní možnosti platformy / OS CPU a paměti
- Vnímaná zácpa sítě
- Stav sítě jako je firewall, symetrický NAT nebo skrytý či proxy použití
- Nastaveno neakceptovat tunely

Stav zácpy by měl být založen na průměru podmínek
po několik minut, ne na okamžitém měření.


## Specifikace

Aktualizujte [NETDB](/docs/overview/network-database/) následujícím způsobem:


```text
D: Střední zácpa, nebo směrovač s nízkým výkonem (např. Android, Raspberry Pi)
     Jiné směrovače by měly degradovat nebo omezit zdánlivou kapacitu
     tohoto směrovače v profilu.

  E: Vysoká zácpa, tento směrovač je blízko nebo na nějakém limitu,
     a odmítá nebo zahazuje většinu požadavků na tunely.
     Pokud byl tento RI publikován v posledních 15 minutách, jiné směrovače
     by měly výrazně degradovat nebo omezit kapacitu tohoto směrovače.
     Pokud je tento RI starší než 15 minut, zacházejte s ním jako s 'D'.

  G: Tento směrovač dočasně nebo trvale odmítá všechny tunely.
     Nepokoušejte se postavit tunel přes tento směrovač,
     dokud není přijata nová RI bez 'G'.
```

Pro konzistenci by implementace měly přidat jakýkoli indikátor zácpy
na konec (po R nebo U).


## Analýza Bezpečnosti

Žádné publikované informace o peerovi nelze důvěřovat.
Limity, jako cokoli jiného v informacích o směrovači, mohou být falšovány.
Nikdy nepoužíváme nic v informacích o směrovači k navýšení vnímané kapacity směrovače.

Publikování indikátorů zácpy, informování peerů, aby se tomuto směrovači vyhnuli, je inherentně
mnohem bezpečnější než dovolující nebo kapacitní indikátory vybízející k více tunelům.

Současné indikátory kapacity šířky pásma (L-P, X) jsou důvěryhodné pouze k vyhýbání se
velmi nízko-šířkovým směrovačům. Limit "U" (nedosažitelný) má podobný účinek.

Jakýkoli publikovaný indikátor zácpy by měl mít stejný účinek jako
odmítnutí nebo shození žádosti o vytvoření tunelu, s podobnými bezpečnostními vlastnostmi.


## Poznámky

Peerové by neměli zcela vyhýbat směrovačům 'D', pouze je degradovat.

Je třeba dbát na to, aby se úplně nevyhýbali směrovačům 'E',
takže když je celá síť v zácpě a publikuje 'E',
věci se úplně nerozpadnou.

Směrovače mohou používat různé strategie pro to, jaké typy tunelů budovat přes směrovače 'D' a 'E',
například průzkumné vs. klientské nebo tunely pro vysokou vs. nízkou šířku pásma.

Směrovače by pravděpodobně neměly výchozí publikovat indikátor zácpy při startu nebo vypínání,
i když je stav jejich sítě neznámý, aby se zabránilo detekci restartu peerů.


## Kompatibilita

Žádné problémy, všechny implementace ignorují neznámé limity.


## Migrace

Implementace mohou přidat podporu kdykoli, není potřeba koordinace.

Předběžný plán:
Publikujeme limity ve verzi 0.9.58 (duben 2023);
využíváme publikované limity ve verzi 0.9.59 (červenec 2023).


## Reference

* [NETDB](/docs/overview/network-database/)
