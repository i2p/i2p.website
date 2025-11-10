---
title: "ECIES-P256"
number: "145"
author: "orignal"
created: "2019-01-23"
lastupdated: "2019-01-24"
status: "Open"
thread: "http://zzz.i2p/topics/2418"
---

## Motivace

ECIES-P256 je mnohem rychlejší než ElGamal. Existuje několik eepsites i2pd s typem šifrování ECIES-P256 a Java by s nimi měla být schopna komunikovat a naopak. i2pd jej podporuje od verze 2.16.0 (0.9.32 Java).

## Přehled

Tento návrh zavádí nový typ šifrování ECIES-P256, který se může objevit v části certifikátu identity, nebo jako samostatný typ šifrování v LeaseSet2.
Lze použít v RouterInfo, LeaseSet1 a LeaseSet2.

### Umístění klíčů ElGamal

Pro zopakování,
veřejné klíče ElGamal o délce 256 bajtů lze nalézt v následujících datových strukturách.
Odkaz na specifikaci společných struktur.

- V identitě směrovače
  Toto je šifrovací klíč směrovače.

- V Destination
  Veřejný klíč destinace byl použit pro staré šifrování i2cp-to-i2cp,
  které bylo ve verzi 0.6 zakázáno, aktuálně se nepoužívá kromě
  IV pro šifrování LeaseSet, které je zastaralé.
  Místo toho se používá veřejný klíč v LeaseSet.

- V LeaseSet
  Toto je šifrovací klíč destinace.

Ve 3 výše uvedeném ECIES veřejný klíč stále zabírá 256 bajtů, ačkoliv skutečná délka klíče je 64 bajtů.
Zbytek musí být vyplněn náhodnou výplní.

- V LS2
  Toto je šifrovací klíč destinace. Velikost klíče je 64 bajtů.

### Typy šifrování v certifikátech klíčů

ECIES-P256 používá typ šifrování 1.
Typy šifrování 2 a 3 by měly být rezervovány pro ECIES-P284 a ECIES-P521

### Použití asymetrického šifrování

Tento návrh popisuje nahrazení ElGamal pro:

1) Zprávy o vytváření tunelů (klíč je v RouterIdentity). Blok ElGamal má 512 bajtů

2) Šifrování typu klient-klient ElGamal+AES/SessionTag (klíč je v LeaseSet, klíč destinace není použit). Blok ElGamal má 514 bajtů

3) Šifrování mezi směrovači v netdb a dalších I2NP zprávách. Blok ElGamal má 514 bajtů

### Cíle

- Zpětná kompatibilita
- Žádné změny pro existující datové struktury
- Mnohem efektivnější z hlediska CPU než ElGamal

### Nepatří mezi cíle

- RouterInfo a LeaseSet1 nemohou publikovat ElGamal a ECIES-P256 společně

### Odůvodnění

ElGamal/AES+SessionTag engine se vždy zasekne na nedostatku tagů, což způsobuje dramatické snižování výkonu při I2P komunikacích.
Vytváření tunelu je nejtěžší operace, protože původce musí provést šifrování ElGamal třikrát pro každou žádost o vytvoření tunelu.

## Potřebné kryptografické primitivy

1) Generování klíčů křivky EC P256 a DH

2) AES-CBC-256

3) SHA256

## Podrobný návrh

Destinace s ECIES-P256 se publikuje s kryptotypem 1 v certifikátu.
Prvních 64 bajtů z 256 v identitě by mělo být interpretováno jako veřejný klíč ECIES a zbytek by měl být ignorován.
Samostatný šifrovací klíč LeaseSet je založen na typu klíče z identity.

### Blok ECIES pro ElGamal/AES+SessionTags
Blok ECIES nahrazuje blok ElGamal pro ElGamal/AES+SessionTags. Délka je 514 bajtů.
Skládá se ze dvou částí po 257 bajtech.
První část začíná nulou a poté následuje P256 efemérní veřejný klíč o délce 64 bajtů, zbytek 192 bajtů je náhodná výplň.
Druhá část začíná nulou a poté je AES-CBC-256 zašifrováno 256 bajtů se stejným obsahem jako v ElGamal.

### Blok ECIES pro záznam o vytváření tunelů
Záznam o vytváření tunelů je stejný, ale bez počátečních nul v blocích.
Tunel může probíhat přes libovolnou kombinaci typů šifrování směrovačů a je prováděn pro každý záznam.
Původce tunelu šifruje záznamy v závislosti na publikovaném typu kryptografie účastníka tunelu, účastník tunelu dešifruje na základě vlastního typu kryptografie.

### AES-CBC-256 klíč
Jedná se o výpočet sdílených klíčů ECDH, kde KDF je SHA256 nad x souřadnicí.
Nechť je Alice šifrovač a Bob dešifrovač.
Předpokládejme, že k je Alicin náhodně zvolený efemérní soukromý klíč P256 a P je Bobův veřejný klíč.
S je sdílené tajemství S(Sx, Sy)
Alice vypočítá S "dohodou" k s P, například S = k*P.

Předpokládejme, že K je Alicin efemérní veřejný klíč a p je Bobův soukromý klíč.
Bob vezme K z prvního bloku přijaté zprávy a vypočítá S = p*K

Klíč pro šifrování AES je SHA256(Sx) a iv je Sy.
