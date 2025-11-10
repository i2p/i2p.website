---
title: "LeaseSet 2"
number: "110"
author: "zzz"
created: "2014-01-22"
lastupdated: "2016-04-04"
status: "Zamítnuto"
thread: "http://zzz.i2p/topics/1560"
supercededby: "123"
---

## Přehled

Tento návrh se zabývá novým formátem LeaseSet s podporou novějších typů šifrování.


## Motivace

Kryptografie typu end-to-end, která je používána v tunelech I2P, má oddělené šifrovací a podepisovací klíče. Podepisovací klíče jsou součástí destinace tunelu, která již byla rozšířena certifikáty klíčů na podporu novějších typů podpisů. Šifrovací klíče jsou však součástí LeaseSet, která neobsahuje žádné certifikáty. Z tohoto důvodu je nutné implementovat nový formát LeaseSet a přidat podporu pro jeho ukládání v netDb.

Pozitivním vedlejším efektem je, že jakmile bude LS2 implementován, všechny stávající destinace mohou využívat modernější typy šifrování; směrovače, které dokážou LS2 načíst a přečíst, budou mít zaručenou podporu jakýchkoli typů šifrování, které budou zavedeny společně s ním.


## Specifikace

Základní formát LS2 by byl následující:

- dest
- časové razítko publikace (8 bajtů)
- vyprší (8 bajtů)
- podtyp (1 bajt) (běžný, šifrovaný, meta nebo služba)
- příznaky (2 bajty)

- část specifická pro podtyp:
  - typ šifrování, šifrovací klíč a pronájmy pro běžné
  - blob pro šifrované
  - vlastnosti, hashe, porty, odvolání atd. pro službu

- podpis
