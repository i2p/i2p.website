---
title: "Aktualizace Streamování"
number: "164"
author: "zzz"
created: "2023-01-24"
lastupdated: "2023-10-23"
status: "Closed"
thread: "http://zzz.i2p/topics/3541"
target: "0.9.58"
implementedin: "0.9.58"
toc: true
---

## Přehled

Java I2P a i2pd routery starší než API 0.9.58 (uvolněné v březnu 2023)
jsou zranitelné útokem opakovaného přehrání SYN paketů.
Toto je problém návrhu protokolu, nikoli chyba implementace.

SYN pakety jsou podepsány, ale podpis počátečního SYN paketu odeslaného od Alice k Bobovi
není vázán na Bobovu identitu, takže Bob může tento paket uložit a přehrát,
posílající jej oběti Charliemu. Charlie si bude myslet, že paket přišel od
Alice a odpoví jí. Ve většině případů je to neškodné, ale
SYN paket může obsahovat počáteční data (například GET nebo POST), která
Charlie okamžitě zpracuje.


## Návrh

Řešení je, aby Alice zahrnula Bobův hash destinace do podepsaných dat SYN.
Bob při přijetí ověří, zda tento hash odpovídá jeho hashi.

Jakákoli potenciální oběť útoku Charlie
tato data zkontroluje a odmítne SYN, pokud neodpovídá jeho hashi.

Použitím volitelného pole NACKs ve SYN pro uložení hashe
je změna zpětně kompatibilní, protože NACKs se neočekávají v SYN paketu a aktuálně jsou ignorovány.

Všechna volitelná pole jsou kryta podpisem, jako obvykle, takže Bob nemůže
přepsat hash.

Pokud jsou Alice a Charlie na verzi API 0.9.58 nebo novější, jakýkoli pokus o opakování od Boba bude odmítnut.


## Specifikace

Aktualizujte [specifikaci Streaming](/docs/specs/streaming/) a přidejte následující sekci:

### Prevence opakování

Aby se zabránilo Bobovi používat útok opakovaného přehrání ukládáním platného podepsaného SYNCHRONIZE paketu
obdrženého od Alice a jeho pozdějším odesíláním oběti Charliemu,
Alice musí zahrnout Bobův hash destinace do SYNCHRONIZE paketu následovně:

.. raw:: html

  {% highlight lang='dataspec' %}
Nastavte pole pro počet NACK na 8
  Nastavte pole NACKs na Bobův 32-bytový hash destinace

{% endhighlight %}

Při přijetí SYNCHRONIZE, pokud je pole pro počet NACK 8,
Bob musí interpretovat pole NACKs jako 32-bytový hash destinace,
a musí ověřit, zda odpovídá jeho hashi destinace.
Musí také obvyklým způsobem ověřit podpis paketu,
protože zahrnuje celý paket včetně počtu NACK a pole NACKs.
Pokud je počet NACK 8 a pole NACKs neodpovídá,
Bob musí paket zahodit.

Toto je vyžadováno pro verze 0.9.58 a vyšší.
Toto je zpětně kompatibilní se staršími verzemi,
protože NACKs se neočekávají v SYNCHRONIZE paketu.
Destinace neznají a nemohou vědět, jakou verzi druhý konec používá.

Žádná změna není nutná pro SYNCHRONIZE ACK paketu odesílaného od Boba k Alice;
nezařazujte NACKs v tomto paketu.


## Analýza Bezpečnosti

Tento problém byl přítomen v streamovacím protokolu od jeho vzniku v roce 2004.
Byl objeven interně vývojáři I2P.
Nemáme žádné důkazy, že by problém byl někdy zneužit.
Skutečná možnost úspěchu zneužití se může velmi lišit v závislosti
na protokolu aplikační vrstvy a službě.
Aplikace peer-to-peer budou pravděpodobně více ovlivněny
než aplikace klient/server.


## Kompatibilita

Žádné problémy. Všechny známé implementace aktuálně ignorují pole NACKs v SYN paketu.
A i kdyby je neignorovaly a pokusily se je interpretovat
jako NACKs pro 8 různých zpráv, tyto zprávy by nebyly nevyřešené
během SYNCHRONIZE handshake a NACKs by nedávaly smysl.


## Migrace

Implementace mohou přidat podporu kdykoli, není třeba koordinace.
Java I2P a i2pd routery to implementovaly v API 0.9.58 (uvolněné v březnu 2023).


