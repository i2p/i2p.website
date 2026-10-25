---
title: "Jednosměrné tunnely"
description: "Historické shrnutí návrhu jednosměrných tunelů I2P"
slug: "unidirectional"
aliases:
  - "/cs/unidirectional-tunnels"
  - "/cs/unidirectional-tunnels/"
lastUpdated: "2016-11"
accurateFor: "0.9.27"
---

## Přehled

Tato stránka popisuje původ a návrh jednosměrných tunnelů I2P. Pro další informace viz:

- [Přehledová stránka tunelů](/docs/overview/tunnel-routing)
- [Specifikace tunelů](/docs/specs/tunnel-implementation)
- [Specifikace vytváření tunelů](/docs/specs/tunnel-creation)
- [Diskuze o designu tunelů](/docs/discussions/tunnel)
- [Výběr peerů](/docs/overview/peer-selection)

## Recenze

Ačkoli si nejsme vědomi žádného publikovaného výzkumu o výhodách jednosměrných tunelů, zdá se, že ztěžují detekci vzoru požadavek/odpověď, který je u obousměrného tunelu docela možné detekovat. Několik aplikací a protokolů, zejména HTTP, přenáší data tímto způsobem. Pokud by provoz sledoval stejnou trasu k cíli a zpět, mohlo by to útočníkovi, který má pouze data o časování a objemu provozu, usnadnit odvození cesty, kterou tunnel používá. Když se odpověď vrátí jinou cestou, je to pravděpodobně obtížnější.

Při jednání s vnitřním protivníkem nebo většinou vnějších protivníků odhalují jednosměrné tunnely I2P polovinu tolik provozních dat, než by bylo odhaleno s obousměrnými okruhy pouhým pozorováním samotných toků - HTTP požadavek a odpověď by následovaly stejnou cestu v Tor, zatímco v I2P by pakety tvořící požadavek procházely jedním nebo více odchozími tunnely a pakety tvořící odpověď by se vracely jedním nebo více různými příchozími tunnely.

Strategie používání dvou oddělených tunnelů pro příchozí a odchozí komunikaci není jedinou dostupnou technikou a má důsledky pro anonymitu. Na pozitivní straně, používáním oddělených tunnelů se snižuje množství komunikačních dat vystavených analýze účastníků tunnelu - například uzly v odchozím tunnelu z webového prohlížeče by viděly pouze provoz HTTP GET požadavku, zatímco uzly v příchozím tunnelu by viděly datovou část doručenou prostřednictvím tunnelu. U obousměrných tunnelů by všichni účastníci měli přístup k informaci, že například 1KB bylo odesláno jedním směrem a pak 100KB druhým. Na negativní straně, používání jednosměrných tunnelů znamená, že existují dvě sady uzlů, které je třeba profilovat a brát v úvahu, a je nutné věnovat dodatečnou pozornost řešení zvýšené rychlosti útoků předchůdců. Proces sdružování a budování tunnelů (strategie výběru a uspořádání uzlů) by měl minimalizovat obavy z útoků předchůdců.

## Anonymita

[Článek od Hermanna a Grothoffa](http://grothoff.org/christian/i2p.pdf) prohlásil, že jednosměrné tunnely I2P "se zdají být špatným designovým rozhodnutím".

Hlavní bod práce je, že deanonymizace na jednosměrných tunnelech trvá déle, což je výhoda, ale útočník si může být v jednosměrném případě jistější. Proto práce tvrdí, že to vůbec není výhoda, ale nevýhoda, alespoň u dlouhodobě existujících I2P Sites.

Tento závěr není plně podpořen článkem. Jednosměrné tunnely jednoznačně zmírňují jiné útoky a není jasné, jak vyvážit riziko útoku popsaného v článku s útoky na architekturu obousměrných tunnelů.

Tento závěr je založen na libovolném vážení (kompromisu) mezi jistotou a časem, které nemusí být použitelné ve všech případech. Například někdo by mohl vytvořit seznam možných IP adres a poté vydat předvolání k soudu na každou z nich. Nebo by útočník mohl postupně provést DDoS útoky na každou a pomocí jednoduchého průsečíkového útoku zjistit, zda I2P Site přestane fungovat nebo se zpomalí. Takže přibližný výsledek může být dostatečný, nebo čas může být důležitější.

Závěr je založen na specifickém vážení důležitosti jistoty versus času, a toto vážení může být chybné a je rozhodně diskutabilní, zejména v reálném světě s obsíláními, zatykačemi a dalšími metodami dostupnými pro konečné potvrzení.

Úplná analýza kompromisů mezi jednosměrnými a obousměrnými tunnely je zjevně mimo rozsah tohoto článku a nebyla provedena ani jinde. Například, jak se tento útok srovnává s mnoha možnými časovými útoky publikovanými o sítích s onion routingem? Je jasné, že autoři tuto analýzu neprovedli, pokud je vůbec možné ji efektivně provést.

Tor používá obousměrné tunnely a prošel rozsáhlým akademickým přezkoumáním. I2P používá jednosměrné tunnely a prošel velmi malým přezkoumáním. Znamená absence výzkumné práce obhajující jednosměrné tunnely, že je to špatná volba designu, nebo jen to, že potřebuje více studia? Timing útoky a distribuované útoky je obtížné bránit jak v I2P, tak v Tor. Záměr designu (viz odkazy výše) byl takový, že jednosměrné tunnely jsou odolnější vůči timing útokům. Článek však představuje poněkud jiný typ timing útoku. Je tento útok, jakkoli inovativní, dostatečný k označení tunnel architektury I2P (a tedy I2P jako celku) za "špatný design" a implicitně jasně horší než Tor, nebo je to jen alternativa designu, která jasně potřebuje další zkoumání a analýzu? Existuje několik dalších důvodů k považování I2P za momentálně horší než Tor a jiné projekty (malá velikost sítě, nedostatek financování, nedostatek přezkoumání), ale jsou jednosměrné tunnely skutečně důvodem?

Shrnutí: "špatné návrhové rozhodnutí" je zjevně (protože článek neoznačuje obousměrné tunnely jako "špatné") zkratkou pro "jednosměrné tunnely jsou jednoznačně horší než obousměrné tunnely", přesto tento závěr není článkem podpořen.
