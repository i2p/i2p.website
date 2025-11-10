---
title: "Meta-LeaseSet pro multihoming"
number: "120"
author: "zzz"
created: "2016-01-09"
lastupdated: "2016-01-11"
status: "Zamítnuto"
thread: "http://zzz.i2p/topics/2045"
supercededby: "123"
---

## Přehled

Tento návrh se týká implementace správné podpory multihomingu v I2P, která může
škálovat až na velké weby.


## Motivace

Multihoming je hack a pravděpodobně nebude fungovat pro např. facebook.i2p v měřítku.
Řekněme, že bychom měli 100 multihomů, každý se 16 tunely, to by bylo 1600 publikací LS každých
10 minut, nebo téměř 3 za sekundu. Floodfill servery by byly přetíženy a spuštěny omezení.
A to jsme ještě nezmínili vyhledávací provoz.

Potřebujeme nějaký typ meta-LS, kde LS uvádí 100 reálných hashů LS. To by bylo
dlouhodobě, mnohem déle než 10 minut. Takže je to dvoustupňové vyhledávání pro LS, ale první
stupeň by mohl být kešován po celé hodiny.


## Specifikace

Meta-LeaseSet by měl mít následující formát::

  - Destinace
  - Časová známka publikace
  - Vypršení
  - Praporky
  - Vlastnosti
  - Počet položek
  - Počet zrušení

  - Položky. Každá položka obsahuje:
    - Hash
    - Praporky
    - Vypršení
    - Náklad (priorita)
    - Vlastnosti

  - Zrušení. Každé zrušení obsahuje:
    - Hash
    - Praporky
    - Vypršení

  - Podpis

Praporky a vlastnosti jsou zahrnuty pro maximální flexibilitu.


## Komentáře

To by pak mohlo být zobecněno jako služba pro vyhledávání jakéhokoli typu. Identifikátor služby je SHA256 hash.

Pro ještě masivnější škálovatelnost bychom mohli mít několik úrovní, tj. meta-LS
může ukazovat na další meta-LS.
