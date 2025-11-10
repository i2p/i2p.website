---
title: "Adresář služeb"
number: "102"
author: "zzz"
created: "2009-01-01"
lastupdated: "2009-01-06"
status: "Odmítnuto"
thread: "http://zzz.i2p/topics/180"
supercededby: "122"
---

## Přehled

Tento návrh je pro protokol, který by aplikace mohly používat k registraci a vyhledávání služeb v adresáři.


## Motivace

Nejjednodušší způsob, jak podporovat onioncat, je pomocí adresáře služeb.

Toto je podobné návrhu, který měl Sponge před časem na IRC. Nemyslím, že by ho napsal, ale jeho myšlenka byla umístit to do netDb. Nejsem zastánce toho, ale diskusi o nejlepším způsobu přístupu k adresáři (vyhledávání v netDb, DNS přes i2p, HTTP, hosts.txt atd.) nechám na jiný den.

Pravděpodobně bych to mohl rychle upravit pomocí HTTP a sbírky perl skriptů, které používám pro formulář přidání klíče.


## Specifikace

Zde je způsob, jakým by aplikace interagovala s adresářem:

REGISTRACE
  - DestKey
  - Seznam dvojic Protokol/Služba:

    - Protokol (volitelné, výchozí: HTTP)
    - Služba (volitelné, výchozí: webová stránka)
    - ID (volitelné, výchozí: žádné)

  - Hostname (volitelné)
  - Expirace (výchozí: 1 den? 0 pro smazání)
  - Sig (použitím privkey pro dest)

  Vrátí: úspěch nebo selhání

  Povolené aktualizace

VYHLEDÁVÁNÍ
  - Hash nebo klíč (volitelné). JEDEN z:

    - 80-bitový částečný hash
    - 256-bitový plný hash
    - plný destkey

  - Dvojice protokol/služba (volitelné)

  Vrátí: úspěch, selhání nebo (pro 80-bit) kolize.
  Pokud úspěch, vrátí podepsaný popis výše.
