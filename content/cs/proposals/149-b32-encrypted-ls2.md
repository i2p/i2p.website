---
title: "B32 pro šifrované LS2"
number: "149"
author: "zzz"
created: "2019-03-13"
lastupdated: "2020-08-05"
status: "Closed"
thread: "http://zzz.i2p/topics/2682"
target: "0.9.40"
implementedin: "0.9.40"
---

## Poznámka
Probíhá nasazení a testování v síti.
Předmět drobných revizí.
Viz [SPEC](/docs/specs/b32-for-encrypted-leasesets/) pro oficiální specifikaci.


## Přehled

Standardní adresa Base 32 ("b32") obsahuje hash cíle.
To nebude fungovat pro šifrované ls2 (návrh 123).

Nemůžete použít tradiční adresu base 32 pro šifrované LS2 (návrh 123), 
protože obsahuje pouze hash cíle. Neposkytuje nezastřený veřejný klíč.
Klienti musí znát veřejný klíč cíle, typ podpisu,  
typ zakrytého podpisu a volitelný tajný nebo privátní klíč
pro načtení a dešifrování leasesetu.
Proto je samotná adresa base 32 nedostatečná.
Klient potřebuje buď celý cíl (který obsahuje veřejný klíč),
nebo veřejný klíč sám o sobě.
Pokud má klient plný cíl v adresáři a adresář
podporuje zpětné vyhledávání podle hashe, pak může být veřejný klíč získán.

Takže potřebujeme nový formát, který nahradí hash veřejným klíčem
v adrese base32. Tento formát musí také obsahovat typ podpisu
veřejného klíče a typ zakrývacího schématu podpisu.

Tento návrh dokumentuje nový b32 formát pro tyto adresy.
Zatímco jsme o tomto novém formátu během diskuzí 
mluvili jako o adrese "b33", skutečný nový formát si zachovává obvyklou příponu ".b32.i2p".

## Cíle

- Zahrnout jak nezastřený, tak zastřený typ podpisu pro podporu budoucích zastíracích schémat
- Podpora veřejných klíčů větších než 32 bajtů
- Zajistit, aby byly b32 znaky všechny nebo většinou náhodné, zejména na začátku
  (nechceme, aby všechny adresy začínaly stejnými znaky)
- Parazitovatelnost
- Uvést, že je vyžadováno odhalené tajemství a/nebo klíč pro každého klienta
- Přidat kontrolní součet pro detekci přešlapů
- Minimalizovat délku, udržet délku štítku DNS pod 63 znaků pro běžné použití
- Pokračovat v používání base 32 kvůli necitlivosti na velikost písmen
- Zachovat obvyklou příponu ".b32.i2p".

## Necíle

- Nepodporujeme "soukromé" odkazy, které by zahrnovaly odhalené tajemství a/nebo klíč pro každého klienta;
  to by bylo nebezpečné.


## Návrh

- Nový formát bude obsahovat nezastřený veřejný klíč, nezastřený typ podpisu,
  a zastřený typ podpisu.
- Volitelně obsahovat tajný a/nebo privátní klíč, pouze pro soukromé odkazy
- Použít stávající příponu ".b32.i2p", ale s delší délkou.
- Přidat kontrolní součet.
- Adresy pro šifrované leasesety jsou identifikovatelné 56 nebo více zakódovanými znaky
  (35 nebo více dešifrovanými bajty), ve srovnání s 52 znaky (32 bajty) pro tradiční base 32 adresy.


## Specifikace

### Vytváření a kódování

Sestavení hostname o {56+ znakech}.b32.i2p (35+ znaků v binární podobě) následujícím způsobem:

```text
flag (1 bajt)
    bit 0: 0 pro jedno-bytové typy podpisu, 1 pro dvou-bytové typy podpisu
    bit 1: 0 pokud není tajemství, 1 pokud je tajemství vyžadováno
    bit 2: 0 pokud není autentizace pro klienta,
           1 pokud je vyžadován privátní klíč klienta
    bitů 7-3: Nepoužité, nastavte na 0

  typ podpisu veřejného klíče (1 nebo 2 bajty podle uvedení ve vlajkách)
    Pokud 1 byte, horní byte se předpokládá jako nula

  typ podpisu zakrytého klíče (1 nebo 2 bajty podle uvedení ve vlajkách)
    Pokud 1 byte, horní byte se předpokládá jako nula

  veřejný klíč
    Počet bajtů, jak je určeno typem podpisu

```

Post-processing a kontrolní součet:

```text
Sestavte binární data, jak je uvedeno výše.
  Zacházejte s kontrolním součtem jako s little-endian.
  Vypočítejte kontrolní součet = CRC-32(data[3:end])
  data[0] ^= (byte) kontrolní součet
  data[1] ^= (byte) (kontrolní součet >> 8)
  data[2] ^= (byte) (kontrolní součet >> 16)

  hostname = Base32.encode(data) || ".b32.i2p"
```

Jakékoli nepoužité bity na konci b32 musí být 0.
Neexistují žádné nepoužité bity pro standardní 56 znakovou (35 bajtovou) adresu.


### Dekódování a Ověřování

```text
odstraňte ".b32.i2p" z hostname
  data = Base32.decode(hostname)
  Vypočítejte kontrolní součet = CRC-32(data[3:end])
  Zacházejte s kontrolním součtem jako s little-endian.
  vlajky = data[0] ^ (byte) kontrolní součet
  pokud 1 byte typů podpisu:
    typ podpisu veřejného klíče = data[1] ^ (byte) (kontrolní součet >> 8)
    typ zastřeného podpisu = data[2] ^ (byte) (kontrolní součet >> 16)
  jinak (2 byte typy podpisu):
    typ podpisu veřejného klíče = data[1] ^ ((byte) (kontrolní součet >> 8)) || data[2] ^ ((byte) (kontrolní součet >> 16))
    typ zastřeného podpisu = data[3] || data[4]
  analyzujte zbytek na základě vlajek pro získání veřejného klíče
```


### Tajné a Privátní Klíčové Bity

Tajné a privátní klíčové bity se používají k tomu, aby indikovaly klientům, proxy nebo jiné
klientské kódy, že tajemství a/nebo privátní klíč budou potřeba k dešifrování
leasesetu. Konkrétní implementace mohou uživatele požádat o dodání
požadovaných dat, nebo odmítnout pokusy o připojení, pokud požadovaná data chybí.


## Odůvodnění

- XORování prvních 3 bajtů s hashem poskytuje omezenou schopnost kontrolního součtu,
  a zajišťuje, že všechny base32 znaky na začátku jsou náhodné.
  Jen několik kombinací vlajek a typů podpisu je platných, takže jakákoliv typografická chyba pravděpodobně vytvoří neplatnou kombinaci a bude odmítnuta.
- Obvykle (1 byte typy podpisu, žádné tajemství, žádná autentizace pro klienta),
  hostname bude mít {56 znaků}.b32.i2p, dekódování na 35 bajtů, stejně jako Tor.
- Tor dvou-bytový kontrolní součet má 1/64K negativní míru falešnosti. S 3 bajty, minus několik ignorovaných bajtů,
  naše se blíží 1 ku milionu, protože většina kombinací vlajek/typů podpisu je neplatná.
- Adler-32 je špatná volba pro malý vstup, a pro detekci malých změn .
  Použijte místo toho CRC-32. CRC-32 je rychlé a široce dostupné.

## Uchovávání do mezipaměti

I když je to mimo rozsah tohoto návrhu, směrovače a/nebo klienti si musí pamatovat a ukládat do mezipaměti
(pravděpodobně trvale) mapování veřejného klíče na cíl a naopak.



## Poznámky

- Odlište staré a nové formáty podle délky. Staré b32 adresy mají vždy {52 znaků}.b32.i2p. Nové mají {56+ znaků}.b32.i2p
- Diskusní vlákno Tor: https://lists.torproject.org/pipermail/tor-dev/2017-January/011816.html
- Neočekávejte, že dvou-bytové typy podpisu se někdy stanou, jsme jen na 13. Není třeba nyní implementovat.
- Nový formát může být použit v odkazovacích serverech (a podáván odkazovacími servery), pokud je to žádoucí, stejně jako b32.


## Problémy

- Jakýkoliv tajný, privátní klíč, nebo veřejný klíč delší než 32 bajtů by
  překročil maximální délku štítku DNS 63 znaků. Prohlížečům to pravděpodobně nebude vadit.


## Migrace

Žádné problémy s kompatibilitou zpětně. Delší b32 adresy se nepovedou převést
na 32-bytové hashe v starém softwaru.
