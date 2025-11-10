---
title: "Zvýšení IPv6 MTU"
number: "127"
author: "zzz"
created: "2016-08-23"
lastupdated: "2016-12-02"
status: "Uzavřeno"
thread: "http://zzz.i2p/topics/2181"
target: "0.9.28"
implementedin: "0.9.28"
---

## Přehled

Tento návrh je na zvýšení max SSU IPv6 MTU z 1472 na 1488.
Implementováno v 0.9.28.

## Motivace

IPv4 MTU musí být násobkem 16, + 12. IPv6 MTU musí být násobkem 16.

Když byla podpora IPv6 poprvé přidána před lety, nastavili jsme max IPv6 MTU na 1472, méně než
IPv4 MTU 1484. Toto bylo, aby věci zůstaly jednoduché a aby bylo zajištěno, že IPv6 MTU bylo menší
než stávající IPv4 MTU. Nyní, když je podpora IPv6 stabilní, bychom měli být schopni
nastavit IPv6 MTU vyšší než IPv4 MTU.

Typické rozhraní MTU je 1500, takže můžeme rozumně zvýšit IPv6 MTU o 16 na 1488.

## Návrh

Změnit maximum z 1472 na 1488.

## Specifikace

V sekcích "Router Address" a "MTU" přehledu SSU,
změnit max IPv6 MTU z 1472 na 1488.

## Migrace

Očekáváme, že routery nastaví připojení MTU jako minimum místního a vzdáleného
MTU, jako obvykle. Žádná kontrola verze by neměla být vyžadována.

Pokud zjistíme, že je kontrola verze vyžadována, nastavíme minimální úroveň verze
na 0.9.28 pro tuto změnu.
