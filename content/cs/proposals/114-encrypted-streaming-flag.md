---
title: "'Šifrovaná' Streamovací Vlajka"
number: "114"
author: "orignal"
created: "2015-01-21"
lastupdated: "2015-01-21"
status: "Vyžaduje-výzkum"
thread: "http://zzz.i2p/topics/1795"
---

## Přehled

Tento návrh je o přidání vlajky ke streamování, která specifikuje typ
end-to-end šifrování, které je používané.


## Motivace

Aplikace s vysokou zátěží mohou narazit na nedostatek tagů ElGamal/AES+SessionTags.


## Návrh

Přidat novou vlajku někam do streamovacího protokolu. Pokud paket přijde s
touto vlajkou, znamená to, že užitečné zatížení je zašifrováno pomocí AES klíče z privátního klíče a veřejného klíče vrstevníka. To by umožnilo eliminovat česnekové (ElGamal/AES) šifrování a problém s nedostatkem tagů.

Může být nastaveno na paket nebo stream prostřednictvím SYN.
