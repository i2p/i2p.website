---
title: "Poznámky ke stavu I2P k 2004-10-19"
date: 2004-10-19
author: "jr"
description: "Týdenní aktualizace stavu I2P zahrnující vydání verze 0.4.1.3, vylepšení výkonu tunnel, pokrok ve streamovací knihovně a vyhledávač files.i2p"
categories: ["status"]
---

Ahoj všichni, je zase úterý

## Rejstřík

1. 0.4.1.3
2. Tunnel test time, and send processing time
3. Streaming lib
4. files.i2p
5. ???

## 1) 0.4.1.3

Vydání 0.4.1.3 vyšlo před dnem či dvěma a vypadá to, že většina lidí aktualizovala (díky!). Síť funguje poměrně dobře, ale stále žádné revoluční zvýšení spolehlivosti. Chyby watchdogu z 0.4.1.2 zmizely (nebo je alespoň nikdo nezmínil). Mým cílem je, aby toto vydání 0.4.1.3 bylo poslední záplatou před 0.4.2, i když samozřejmě pokud se objeví něco velkého, co bude potřeba opravit, vydáme další.

## 2) Doba testu Tunnel a doba zpracování odesílání

Nejvýznamnější změny ve vydání 0.4.1.3 se týkaly testování tunnel - namísto pevně daného (30sekundového!) testovacího období máme mnohem agresivnější časové limity odvozené z naměřené výkonnosti. To je dobře, protože nyní označujeme tunnels jako selhávající, když jsou příliš pomalé na to, aby se daly k čemukoli užitečnému použít. Zároveň je to ale i špatně, protože se někdy tunnels dočasně zahltí, a pokud je testujeme během toho období, označíme tunnel, který by jinak fungoval, jako selhávající.

Nedávný graf ukazující, jak dlouho trvá test tunnelu na jednom routeru:

To jsou obecně v pořádku časy testů pro tunnel - procházejí přes 4 vzdálené peery (s 2 hop tunnels), takže většina z nich má ~1-200ms na skok. Nicméně to tak není vždy, jak vidíte - někdy to trvá řádově sekundy na skok.

Tady přichází na řadu následující graf - doba čekání ve frontě od okamžiku, kdy jeden konkrétní router chtěl odeslat zprávu, do okamžiku, kdy byla tato zpráva odeslána přes socket:

Asi 95 % hodnot je pod 50ms, ale výkyvy jsou zabijácké.

Potřebujeme se zbavit těch špiček a také obejít situace, kdy selhává více peerů. V současném stavu, když se 'dozvíme', že nějaký peer způsobuje selhání našich tunnels, ve skutečnosti se nedozvídáme nic specifického o jejich router - tyto špičky mohou způsobit, že i peery s vysokou kapacitou působí pomalu, když se trefíme zrovna do takové špičky.

## 3) Streamingová knihovna

Druhá část obcházení selhávajících tunnels bude zčásti zajištěna streamingovou knihovnou - ta nám poskytne mnohem robustnější end to end streamovací komunikaci. Tohle není nic nového - ta knihovna udělá všechny ty pokročilé věci, o kterých už nějakou dobu mluvíme (a samozřejmě si ponese i svůj díl chyb). V tomto směru jsme udělali velký pokrok a implementace je pravděpodobně zhruba ze 60 % hotová.

Více novinek, až budou.

## 4) files.i2p

Ok, v poslední době se objevilo hodně nových eepsites(I2P Sites), což je paráda. Jen bych chtěl zvlášť upozornit na jeden z nich, protože má docela šikovnou funkci pro nás ostatní. Pokud jste ještě nebyli na files.i2p, je to v zásadě vyhledávač podobný Googlu, s cache stránek, které prochází (takže můžete vyhledávat i procházet, i když je eepsite(I2P Site) offline). Fakt super.

## 5) ???

Tento týden jsou stavové poznámky docela stručné, ale děje se toho spousta - - jen nemám čas napsat víc před schůzkou. Takže se za pár minut zastavte na #i2p a můžeme probrat cokoli, co jsem hloupě přehlédl.

=jr
