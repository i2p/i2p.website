---
title: "Trvalost klíčů LeaseSet"
number: "113"
author: "zzz"
created: "2014-12-13"
lastupdated: "2016-12-02"
status: "Uzavřeno"
thread: "http://zzz.i2p/topics/1770"
target: "0.9.18"
implementedin: "0.9.18"
---

## Přehled

Tento návrh se týká uchovávání dodatečných dat v LeaseSet, která jsou
aktuálně nestálá. Implementováno ve verzi 0.9.18.

## Motivace

V 0.9.17 byla přidána trvalost pro netDb slicing klíč, uložený v
i2ptunnel.config. To pomáhá předcházet některým útokům tím, že se při restartu
routeru udržuje stejný slice, a také to zabraňuje možné korelaci s restartem routeru.

Existují další dvě věci, které se dají ještě snadněji korelovat s restartem routeru:
klíče pro šifrování a podepisování leasesetu. Tyto aktuálně nejsou uchovávány.

## Navrhované změny

Soukromé klíče jsou uloženy v i2ptunnel.config, jako i2cp.leaseSetPrivateKey a i2cp.leaseSetSigningPrivateKey.
