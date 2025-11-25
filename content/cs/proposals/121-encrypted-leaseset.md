---
title: "Šifrovaný LeaseSet"
number: "121"
author: "zzz"
created: "2016-01-11"
lastupdated: "2016-01-12"
status: "Zamítnuto"
thread: "http://zzz.i2p/topics/2047"
supercededby: "123"
---

## Přehled

Tento návrh se zabývá přepracováním mechanismu pro šifrování LeaseSets.


## Motivace

Současné šifrované LS je hrozné a nezabezpečené. Mohu to říct, navrhl a implementoval jsem to.

Důvody:

- Šifrování AES CBC
- Jediný klíč AES pro všechny
- Stále viditelné vypršení platnosti Lease
- Stále viditelný šifrovací veřejný klíč


## Návrh

### Cíle

- Udělat celou věc neprůhlednou
- Klíče pro každého příjemce


### Strategie

Postupovat jako GPG/OpenPGP. Asymetricky zašifrovat symetrický klíč pro každého příjemce. Data se dešifrují pomocí tohoto asymetrického klíče. Viz např. [RFC-4880-S5.1](https://tools.ietf.org/html/rfc4880#section-5.1)
POKUD najdeme algoritmus, který je malý a rychlý.

Trik je najít asymetrické šifrování, které je malé a rychlé. ElGamal o velikosti 514 bajtů je zde trochu bolestivé. Můžeme si vést lépe.

Viz např. http://security.stackexchange.com/questions/824...

Toto funguje pro malý počet příjemců (nebo spíše klíčů; stále můžete distribuovat klíče více lidem, pokud chcete).


## Specifikace

- Destinace
- Časové razítko publikace
- Vypršení platnosti
- Příznaky
- Délka dat
- Šifrovaná data
- Podpis

Šifrovaná data by mohla být předložena nějakým specifikátorem enctype, nebo ne.


## Reference

.. [RFC-4880-S5.1]
    https://tools.ietf.org/html/rfc4880#section-5.1
