---
title: "Seznam blokovaných ve formátu SU3"
number: "130"
author: "psi, zzz"
created: "2016-11-23"
lastupdated: "2016-11-23"
status: "Otevřený"
thread: "http://zzz.i2p/topics/2192"
toc: true
---

## Přehled

Tento návrh je určen k distribuci aktualizací seznamu blokovaných v samostatném souboru su3.


## Motivace

Bez tohoto opatření je seznam blokovaných aktualizován pouze při vydání.
Tento formát by mohl být použit v různých implementacích routeru.


## Návrh

Definujte formát, který má být zabalen do souboru su3.
Umožňuje blokování podle IP adresy nebo hash routeru.
Routery se mohou přihlásit k odběru URL, nebo importovat soubor získaný jinými prostředky.
Soubor su3 obsahuje podpis, který musí být při importu ověřen.


## Specifikace

Bude přidáno na stránku specifikace aktualizace routeru.

Definujte nový obsahový typ BLOCKLIST (5).
Definujte nový typ souboru TXT_GZ (4) (formát .txt.gz).
Záznamy jsou po jedné na řádek, buď doslovná adresa IPv4 nebo IPv6,
nebo 44znakový router hash kódovaný v base64.
Podpora blokování s použitím netmasky, např. x.y.0.0/16, je volitelná.
Pro odblokování záznamu jej předejte s '!'.
Komentáře začínají znakem '#'.

## Migrace

n/a


