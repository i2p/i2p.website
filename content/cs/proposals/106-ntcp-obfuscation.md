---
title: "NTCP Zatemnění"
number: "106"
author: "zzz"
created: "2010-11-23"
lastupdated: "2014-01-03"
status: "Odmítnuto"
thread: "http://zzz.i2p/topics/774"
supercededby: "111"
---

## Přehled

Tento návrh se týká přepracování transportu NTCP za účelem zlepšení jeho odolnosti vůči automatizované identifikaci.


## Motivace

NTCP data jsou šifrována po prvním zprávě (a první zpráva se jeví jako náhodná data), což zabraňuje identifikaci protokolu přes "analýzu obsahu". Stále je však náchylný k identifikaci protokolu prostřednictvím "analýzy toku". To proto, že první 4 zprávy (tj. handshake) mají pevnou délku (288, 304, 448 a 48 bajtů).

Přidáním náhodného množství náhodných dat ke každé ze zpráv můžeme situaci značně ztížit.


## Úpravy NTCP

To je poměrně těžkopádné, ale zabraňuje jakékoli detekci DPI zařízeními.

Do konce 288-bytové zprávy 1 budou přidána následující data:

- 514-bytový blok šifrovaný pomocí ElGamal
- Náhodné vycpávky

ElG blok je šifrován veřejným klíčem Boba. Po dešifrování na 222 bajtů obsahuje:
- 214 bajtů náhodných vycpávek
- 4 bajty 0 rezervováno
- 2 bajty vycpávkové délky, která následuje
- 2 bajty verze protokolu a příznaků

Ve zprávách 2-4 budou poslední dva bajty vycpávek nyní označovat délku dalších vycpávek, které následují.

Poznámka, že ElG blok nemá dokonalou dopřednou utajitelnost, ale není tam nic zajímavého.

Mohli bychom upravit naši ElG knihovnu tak, aby šifrovala menší datové velikosti, pokud si myslíme, že 514 bajtů je příliš mnoho? Je šifrování ElG pro každé nastavení NTCP příliš?

Podpora tohoto bude oznámena v netdb RouterAddress s volbou "version=2". Pokud je přijato pouze 288 bajtů v Zprávě 1, Alice se předpokládá jako verze 1 a v následujících zprávách se neodesílají žádné vycpávky. Upozorňujeme, že komunikace by mohla být zablokována, pokud by MITM fragmentoval IP na 288 bajtů (podle Brandona velmi nepravděpodobné).
