---
title: "Nová šablona návrhu šifrování"
number: "142"
author: "zzz"
created: "2018-01-11"
lastupdated: "2018-01-20"
status: "Meta"
thread: "http://zzz.i2p/topics/2499"
toc: true
---

## Přehled

Tento dokument popisuje důležité otázky, které je třeba zvážit při navrhování náhrady nebo doplnění našeho ElGamal asymetrického šifrování.

Toto je informační dokument.


## Motivace

ElGamal je starý a pomalý a existují lepší alternativy.
Avšak existuje několik problémů, které musíme vyřešit, než můžeme přidat nebo změnit jakýkoli nový algoritmus.
Tento dokument zdůrazňuje tyto nevyřešené problémy.


## Výzkumné pozadí

Každý, kdo navrhuje nové šifrování, musí nejprve znát následující dokumenty:

- [Návrh 111 NTCP2](/cs/proposals/111-ntcp-2/)
- [Návrh 123 LS2](/cs/proposals/123-new-netdb-entries/)
- [Návrh 136 experimentální typy podpisů](/cs/proposals/136-experimental-sigtypes/)
- [Návrh 137 volitelné typy podpisů](/cs/proposals/137-optional-sigtypes/)
- Diskusní vlákna zde pro každý z výše uvedených návrhů, odkazy uvnitř
- [priority návrhů pro rok 2018](http://zzz.i2p/topics/2494)
- [návrh ECIES](http://zzz.i2p/topics/2418)
- [přehled nového asymetrického šifrování](http://zzz.i2p/topics/1768)
- [Přehled nízkoúrovňového šifrování](/cs/docs/specs/common-structures/)


## Použití asymetrického šifrování

Jako přehled, používáme ElGamal pro:

1) Zprávy pro sestavení tunelu (klíč je v RouterIdentity)

2) Šifrování Router-to-router pro netdb a další I2NP zprávy (klíč je v RouterIdentity)

3) Klient Bezkoncečné ElGamal+AES/SessionTag (klíč je v LeaseSet, klíč Destination není použitý)

4) Efemérní DH pro NTCP a SSU


## Návrh

Jakýkoli návrh na nahrazení ElGamal něčím jiným musí poskytnout následující detaily.


## Specifikace

Jakýkoli návrh nového asymetrického šifrování musí plně specifikovat následující věci.


### 1. Obecné

Odpovězte na následující otázky ve vašem návrhu. Všimněte si, že to může potřebovat být samostatný návrh od konkrétních bodů v 2) níže, protože to může být v konfliktu s existujícími návrhy 111, 123, 136, 137, nebo jinými.

- Pro které případy 1-4 nahoře navrhujete použít nové šifrování?
- Pokud pro 1) nebo 2) (router), kam jde veřejný klíč, do RouterIdentity nebo do RouterInfo vlastností? Máte v úmyslu použít typ šifrování v certifikátu klíče? Plně specifikujte. Zdůvodněte své rozhodnutí v obou případech.
- Pokud pro 3) (klient), míníte uložit veřejný klíč v destination a použít typ šifrování v certifikátu klíče (jako v návrhu ECIES), nebo jej uložit v LS2 (jako v návrhu 123), nebo něco jiného? Plně specifikujte a zdůvodněte své rozhodnutí.
- Pro všechna použití, jak bude podpora inzerována? Pokud pro 3), jde to do LS2, nebo někam jinam? Pokud pro 1) a 2), je to podobné návrhům 136 a/nebo 137? Plně specifikujte a zdůvodněte svá rozhodnutí. Pravděpodobně bude potřeba samostatný návrh pro toto.
- Plně specifikujte jak a proč je toto zpětně kompatibilní, a plně specifikujte plán migrace.
- Které neimplementované návrhy jsou předpoklady pro váš návrh?


### 2. Specifický typ šifrování

Odpovězte na následující otázky ve vašem návrhu:

- Obecné informace o šifrování, specifické křivky/parametry, plně odůvodněte vaši volbu. Poskytněte odkazy na specifikace a další informace.
- Výsledky testů rychlosti ve srovnání s ElG a dalšími alternativami, pokud je to relevantní. Zahrňte šifrování, dešifrování a keygen.
- Dostupnost knihovny v C++ a Java (jak OpenJDK, tak BouncyCastle, a třetích stran)
  Pro třetí strany nebo ne-Java poskytněte odkazy a licence
- Navrhované číslo/čísla typu šifrování (experimentální rozsah nebo ne)


## Poznámky


