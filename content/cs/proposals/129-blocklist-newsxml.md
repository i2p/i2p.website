---
title: "Seznam blokací ve Zpravodajském kanálu"
number: "129"
author: "zzz"
created: "2016-11-23"
lastupdated: "2016-12-02"
status: "Uzavřeno"
thread: "http://zzz.i2p/topics/2191"
target: "0.9.28"
implementedin: "0.9.28"
toc: true
---

## Přehled

Tento návrh je určen k distribuci aktualizací seznamu blokací v souboru zpráv,
který je distribuován ve formátu podepsaného su3.
Implementováno ve verzi 0.9.28.


## Motivace

Bez toho je seznam blokací aktualizován pouze v rámci vydání.
Využívá stávající odběr zpráv.
Tento formát by mohl být použit v různých implementacích routerů, ale pouze Java router
nyní používá odběr zpráv.


## Návrh

Přidat novou sekci do souboru news.xml.
Umožnit blokování podle IP nebo hashe routeru.
Sekce bude mít své vlastní časové razítko.
Umožnit odblokování dříve blokovaných položek.

Obsahovat podpis sekce, který bude specifikován.
Podpis bude pokrývat časové razítko.
Podpis musí být ověřen při importu.
Podepisovatel bude specifikován a může se lišit od toho, kdo podepsal su3.
Routery mohou používat jiný důvěryhodný seznam pro seznam blokací.


## Specifikace

Nyní na stránce specifikace aktualizace routeru.

Položky jsou buď doslovná IPv4 nebo IPv6 adresa,
nebo 44znakový base64 zakódovaný hash routeru.
IPv6 adresy mohou být ve zkráceném formátu (obsahující "::").
Podpora blokování s maskou sítě, např. x.y.0.0/16, je volitelná.
Podpora pro názvy hostitelů je volitelná.


## Migrace

Routery, které toto nepodporují, novou sekci XML ignorují.


