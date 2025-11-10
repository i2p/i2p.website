---
title: "Překlad Jména pro GarliCat"
number: "105"
author: "Bernhard R. Fischer"
created: "2009-12-04"
lastupdated: "2009-12-04"
status: "Neaktivní"
thread: "http://zzz.i2p/topics/453"
---

## Přehled

Tento návrh se týká přidání podpory pro reverzní DNS dotazy do I2P.

## Současný Mechanismus Překladu

GarliCat (GC) provádí překlad jmen pro navazování spojení s ostatními uzly GC. Tento překlad jmen je pouze překódování binární reprezentace adresy do Base32 kódovaného tvaru. Překlad tedy funguje obousměrně.

Tyto adresy jsou zvoleny jako 80bitové. Důvodem je, že Tor používá 80bitové hodnoty pro adresování svých skrytých služeb. Takže OnionCat (což je GC pro Tor) funguje s Tor bez dalšího zásahu.

Bohužel (pokud jde o tento adresní model), I2P používá 256bitové hodnoty pro adresování svých služeb. Jak již bylo zmíněno, GC překóduje mezi binárním a Base32 kódovaným tvarem. Vzhledem k tomu, že GC je vrstva 3 VPN, v binární reprezentaci jsou adresy definovány jako IPv6 adresy, které mají celkovou délku 128 bitů. Očividně, 256bitové I2P adresy se do tohoto nevejdou.

Proto je nutný druhý krok překladu jmen:
IPv6 adresa (binární) -1a-> Base32 adresa (80 bitů) -2a-> I2P adresa (256 bitů)
-1a- ... GC překlad
-2a- ... I2P hosts.txt hledání

Současné řešení je nechat I2P router vykonat práci. To je dosaženo vložením 80bitové Base32 adresy a jejího cíle (I2P adresa) jako dvojice jméno/hodnota do souboru hosts.txt nebo privatehosts.txt ve směrovači I2P.

Toto v podstatě funguje, ale závisí to na službě pojmenování, která (podle mého názoru) je ve stavu vývoje a není dostatečně zralá (zejména pokud jde o distribuci jmen).

## Škálovatelné Řešení

Navrhuji změnit úrovně adresování ve vztahu k I2P (a možná také pro Tor) tak, aby GC prováděl reverzní dotazy na IPv6 adresy pomocí běžného DNS protokolu. Reverzní zóna by měla přímo obsahovat 256bitovou I2P adresu ve své Base32 kódované podobě. To mění mechanismus hledání na jediný krok, čímž se přidávají další výhody.
IPv6 adresa (binární) -1b-> I2P adresa (256 bitů)
-1b- ... DNS reverzní dotaz

DNS dotazy v rámci Internetu jsou známé jako úniky informací v souvislosti s anonymitou. Tudíž, tyto dotazy musí být prováděny v rámci I2P. To znamená, že by se v rámci I2P mělo nacházet několik DNS služeb. Jelikož DNS dotazy se obvykle provádějí pomocí UDP protokolu, je GC samotný potřebný pro přenos dat, protože on přenáší UDP pakety, které I2P nativně nedělá.

Další výhody spojené s DNS jsou:
1) Je to dobře známý standardní protokol, a proto je neustále zdokonalován a existuje mnoho nástrojů (klientů, serverů, knihoven,...).
2) Je to distribuovaný systém. Podporuje to, aby byl jmenný prostor hostován na několika serverech paralelně ve výchozím nastavení.
3) Podporuje kryptografii (DNSSEC), která umožňuje autentizaci záznamů zdrojů. To by mohlo být přímo spojeno s klíči destinace.

## Budoucí Příležitosti

Je možné, že by tato služba pojmenování mohla být použita i pro vyhledávání směru vpřed. To znamená převádění hostnames na I2P adresy a/nebo IPv6 adresy. Ale tento druh vyhledávání potřebuje další prozkoumání, protože tyto dotazy jsou obvykle prováděny místně nainstalovanou knihovnou resolveru, která používá běžné internetové jmenné servery (např. jak specifikováno v /etc/resolv.conf na systémech podobných Unixu). To je odlišné od reverzních dotazů GC, které jsem uvedl výše.
Další příležitost by mohla být, že se I2P adresa (destinace) zaregistruje automaticky při vytváření GC příchozího tunelu. To by výrazně zlepšilo použitelnost.
