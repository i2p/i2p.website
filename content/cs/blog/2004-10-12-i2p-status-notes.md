---
title: "Poznámky ke stavu I2P k 2004-10-12"
date: 2004-10-12
author: "jr"
description: "Týdenní zpráva o stavu I2P zahrnující vydání verze 0.4.1.2, experimenty s dynamickým omezováním, vývoj streamovací knihovny pro verzi 0.4.2 a e-mailové diskuse"
categories: ["status"]
---

Ahoj všichni, je čas na naši týdenní aktualizaci.

## Rejstřík:

1. 0.4.1.2
2. 0.4.1.3
3. 0.4.2
4. mail discussions
5. ???

## 1) 0.4.1.2

Nová verze 0.4.1.2 je venku už pár dní a věci probíhají víceméně podle očekávání – i když se objevilo pár zádrhelů s novou komponentou watchdog, což způsobovalo, že při problémech místo restartu zabíjela váš router. Jak jsem dnes už zmiňoval, hledám lidi, kteří použijí nový nástroj pro logování statistik a pošlou mi nějaká data, takže vaši pomoc bych velmi ocenil.

## 2) 0.4.1.3

Než vyjde 0.4.2, bude ještě jedno vydání, protože chci, aby síť byla co nejrobustnější, než se posuneme dál. S čím teď experimentuji, je dynamické omezení tunnel participation - dávat routers pokyn, aby pravděpodobnostně odmítaly požadavky, pokud jsou přetížené nebo jejich tunnels jsou pomalejší než obvykle. Tyto pravděpodobnosti a prahové hodnoty se počítají dynamicky z průběžně sbíraných statistik - pokud je váš 10minutový čas testu tunnel větší než váš 60minutový čas testu tunnel, přijměte požadavek na tunnel s pravděpodobností 60minRate/10minRate (a pokud je váš aktuální počet tunnels větší než váš 60minutový průměrný počet tunnels, přijměte ho s p=60mRate/curTunnels).

Další možné omezení je vyhlazovat šířku pásma v tomto duchu - pravděpodobnostně odmítat tunnels, když naše využití šířky pásma prudce vyskočí. Každopádně záměrem toho všeho je pomoci rozprostřít využití sítě a rozložit tunnels mezi více lidí. Hlavním problémem, který jsme měli s vyvažováním zátěže, byl ohromný *nadbytek* kapacity, a tudíž se nespustil žádný z našich "sakra, jsme pomalí, tak pojďme odmítat" spouštěčů. Tyto nové pravděpodobnostní by snad měly udržet rychlé změny na uzdě.

Nemám žádný konkrétní plán, kdy vyjde vydání 0.4.1.3 – možná o víkendu. Data, která lidé posílají (viz výše), by měla pomoci rozhodnout, zda to bude stát za to, nebo zda existují jiné cesty, které se vyplatí víc.

## 3) 0.4.2

Jak jsme diskutovali na minulotýdenní schůzce, prohodili jsme vydání 0.4.2 a 0.4.3 - 0.4.2 bude nová streamovací knihovna a 0.4.3 bude aktualizace tunnel.

Znovu jsem procházel literaturu ohledně streamovací funkcionality TCP a narazil jsem na několik zajímavých témat, která jsou pro I2P důležitá. Konkrétně naše vysoká doba odezvy spíše nahrává něčemu jako XCP a pravděpodobně bychom měli být poměrně agresivní při používání různých forem explicitního oznamování přetížení, i když nemůžeme využít něco jako volbu časového razítka, protože naše hodiny mohou být posunuté až o jednu minutu.

Kromě toho se budeme chtít ujistit, že dokážeme optimalizovat streaming lib (knihovnu pro streamování) tak, aby zvládala krátkodobá spojení (v čem je standardní TCP poměrně špatné) - například chci mít možnost posílat malé (<32KB) HTTP GET požadavky a malé (<32KB) odpovědi doslova třemi zprávami:

```
Alice-->Bob: syn+data+close
Bob-->Alice: ack+data+close (the browser gets the response now)
Alice-->Bob: ack (so he doesn't resend the payload)
```
Každopádně na tom zatím nebylo napsáno mnoho kódu; po stránce protokolu to vypadá dost podobně jako TCP a pakety jsou do jisté míry jako sloučení návrhu uživatele „human“ a starého návrhu. Pokud má někdo nějaké návrhy nebo nápady, nebo chce pomoci s implementací, ozvěte se prosím.

## 4) e-mailová diskuse

Proběhly některé zajímavé diskuse o e‑mailu v (a mimo) I2P - postman zveřejnil sadu nápadů online a hledá návrhy. Také se vedly související diskuse na #mail.i2p. Možná bychom mohli postmana požádat o aktualizaci?

## 5) ???

To je pro tuto chvíli asi vše. Zastavte se na schůzku za pár minut a přineste své připomínky :)

=jr
