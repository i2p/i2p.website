---
title: "RI a výplň cíle"
number: "161"
author: "zzz"
created: "2022-09-28"
lastupdated: "2023-01-02"
status: "Otevřeno"
thread: "http://zzz.i2p/topics/3279"
target: "0.9.57"
toc: true
---

## Stav

Implementováno ve verzi 0.9.57.
Necháváme tento návrh otevřený, abychom mohli zlepšit a diskutovat o myšlenkách v sekci "Budoucí plánování".


## Přehled


### Shrnutí

Veřejný klíč ElGamal v Destination od vydání 0.6 (2005) nebyl použit.
I když naše specifikace říkají, že není použit, NEŘÍKAJÍ, že implementace mohou
vynechat generování páru klíčů ElGamal a jednoduše vyplnit pole náhodnými daty.

Navrhujeme změnit specifikace, aby říkaly, že
pole je ignorováno a implementace MŮŽE vyplnit pole náhodnými daty.
Tato změna je zpětně kompatibilní. Není známa žádná implementace, která by ověřovala
veřejný klíč ElGamal.

Tento návrh navíc poskytuje implementátorům pokyny, jak generovat
náhodná data pro výplň Destination A Router Identity tak, aby byla komprimovatelná, ale
stále bezpečná, a přitom se zdálo, že představují Base 64 reprezentace neporušeně nebo nezávisle.
To poskytuje většinu výhod odstranění výplňových polí bez jakýchkoliv
narušujících protokolových změn.
Komprimovatelné Destinations snižují velikost streamovacího SYN a znovu odpovídatelného datagramu;
komprimovatelné Router Identities snižují Messages obchodu s databází, SSU2 zprávy potvrzované schůzky a
reseed su3 soubory.

Nakonec, návrh diskutuje o možnostech pro nové formáty Destination a Router Identity,
které by zcela odstranily výplň. Existuje také krátká diskuse o postkvantové
kryptografii a jak by to mohlo ovlivnit budoucí plánování.



### Cíle

- Odstranit požadavek na vytvoření cílů ElGamal klíčového páru
- Doporučit osvědčené postupy, aby Destinations a Router Identities byly vysoce komprimovatelné,
  a přitom nevykazovaly zřejmé vzory v Base 64 reprezentacích.
- Povzbudit adopci osvědčených postupů všemi implementacemi, aby
  pole nešla rozlišit
- Snížit velikost streamovacího SYN
- Snížit velikost znovu odpovídatelného datagramu
- Snížit velikost SSU2 bloku RI
- Snížit velikost a frekvenci fragmentace SSU2 potvrzené schůzky
- Snížit velikost Messages obchodu s databází (s RI)
- Snížit velikost reseed souboru
- Udržet kompatibilitu ve všech protokolech a API
- Aktualizovat specifikace
- Diskutovat o alternativách pro nové formáty Destination a Router Identity

Eliminací požadavku na generování klíčů ElGamal mohou implementace
zcela odstranit kód ElGamal, s ohledem na aspekty zpětné kompatibility
v jiných protokolech.



## Navrhovaný design

Přísně řečeno, 32-bytů veřejný podpisový klíč samotný (v rámci Destinations a Router Identities)
a 32-bytů šifrovací veřejný klíč (pouze v Router Identities) je náhodné číslo,
které poskytuje veškerou náhodnost potřebnou pro SHA-256 hashe těchto struktur,
které jsou kryptograficky silné a náhodně distribuované v síťové databázi DHT.

Nicméně, z důvodu opatrnosti, doporučujeme minimálně 32 bytů náhodných dat
použít v poli veřejného klíče ElG a ve výplni. Navíc, pokud by pole byla samé nuly,
Base 64 destinace by obsahovaly dlouhé sekvence znaků AAAA, což by mohlo uživatele
znepokojit nebo zmást.

Pro typ podpisu Ed25519 a typ šifrování X25519:
Destinations bude obsahovat 11 kopií (352 bytů) náhodných dat.
Router Identities bude obsahovat 10 kopií (320 bytů) náhodných dat.



### Odhadované úspory

Destinations jsou zahrnuty v každém přenosu SYN
a znovu odpovídatelném datagramu.
Router Infos (obsahující Router Identities) jsou zahrnuty v Messages obchodu s databází
a v zprávách potvrzovaných schůzkou v NTCP2 a SSU2.

NTCP2 nekomprimuje Router Info.
RIs v Messages obchodu s databází a SSU2 potvrzené schůzky jsou gzipovány.
Router Infos jsou zipovány v reseed SU3 souborech.

Destinations v Messages obchodu s databází nejsou komprimované.
Streamovací SYN zprávy jsou gzipovány na úrovni I2CP.

Pro typ podpisu Ed25519 a typ šifrování X25519,
odhadované úspory:

| Typ dat | Celková velikost | Klíče a cert | Nezkomprimovaná výplň | Zkomprimovaná výplň | Velikost | Úspory |
|---------|-----------------|--------------|----------------------|---------------------|----------|--------|
| Destination | 391 | 39 | 352 | 32 | 71 | 320 bytů (82 %) |
| Router Identity | 391 | 71 | 320 | 32 | 103 | 288 bytů (74 %) |
| Router Info | 1000 typ. | 71 | 320 | 32 | 722 typ. | 288 bytů (29 %) |

Poznámky: Předpokládá 7-bytový certifikát není komprimovatelný, žádné dodatečné gzip overhead.
Ani to není pravda, ale efekty budou malé.
Ignoruje další komprimovatelné části Router Info.



## Specifikace

Navrhované změny našich aktuálních specifikací jsou dokumentovány níže.


### Běžné struktury
Změnit specifikaci běžných struktur
tak, aby se uvedlo, že 256-bytové pole veřejného klíče Destination je ignorováno a může
obsahovat náhodná data.

Přidat sekci do specifikace běžných struktur
doporučující osvědčené postupy pro pole veřejného klíče Destination a
výplňová pole v Destination a Router Identity, jako následující:

Generovat 32 bytů náhodných dat pomocí silného kryptografického generátoru pseudonáhodných čísel (PRNG)
a opakovat těchto 32 bytů podle potřeby pro vyplnění pole veřejného klíče (pro Destinations)
a pole výplně (pro Destinations a Router Identities).

### Soubor soukromého klíče
Formát souboru soukromého klíče (eepPriv.dat) není oficiální součástí našich specifikací,
ale je dokumentován v [Java I2P javadocs](http://idk.i2p/javadoc-i2p/net/i2p/data/PrivateKeyFile.html)
a další implementace jej podporují.
To umožňuje přenositelnost soukromých klíčů do různých implementací.
Přidat poznámku k tomu javadoc, že šifrovací veřejný klíč může být náhodná výplň
a šifrovací soukromý klíč může být samé nuly nebo náhodná data.

### SAM
Poznámka v specifikaci SAM že šifrovací soukromý klíč se nepoužívá a může být ignorován.
Jakákoli náhodná data mohou být navrácena klientem.
SAM Bridge může poslat náhodná data při vytváření (s DEST GENERATE nebo SESSION CREATE DESTINATION=TRANSIENT)
místo samých nul, aby Base 64 reprezentace neobsahovala sekvenci znaků AAAA
a nepůsobila jako poškozená.


### I2CP
Nejsou vyžadovány žádné změny pro I2CP. Soukromý klíč pro šifrovací veřejný klíč v Destination
není odesílán routeru.


## Budoucí plánování


### Změny protokolu

Za cenu změn protokolu a nedostatku zpětné kompatibility bychom mohli
změnit naše protokoly a specifikace, abychom odstranili výplňové pole v
Destination, Router Identity, nebo obojí.

Tento návrh se částečně podobá "b33" šifrovanému formátu leaseset,
obsahujícímu pouze klíč a typové pole.

Pro zachování nějaké kompatibility by určité úrovně protokolu mohly "rozšířit" výplňové pole
se všemi nulami, aby je představily jiným úrovním protokolu.

Pro Destinations bychom mohli také odstranit pole typu šifrování v certifikátu klíče,
s úsporou dvou bytů.
Alternativně by Destinations mohla získat nový typ šifrování v certifikátu klíče,
indikující nulový veřejný klíč (a výplň).

Pokud není zahrnut převod kompatibility mezi starými a novými formáty na nějaké úrovni protokolu,
následující specifikace, API, protokoly, a aplikace by byly ovlivněny:

- Specifikace běžných struktur
- I2NP
- I2CP
- NTCP2
- SSU2
- Ratchet
- Streaming
- SAM
- Bittorrent
- Reseeding
- Soubor soukromého klíče
- Java jádro a router API
- i2pd API
- Třetí strany SAM knihovny
- Balíky a třetí strany nástroje
- Několik Java pluginů
- Uživatelská rozhraní
- P2P aplikace např. MuWire, bitcoin, monero
- hosts.txt, adresář a předplatné

Pokud je v některé vrstvě specifikována konverze, seznam by byl zkrácen.

Náklady a výhody těchto změn nejsou jasné.

Konkrétní návrhy TBD:





### PQ klíče

Post-Quantum (PQ) veřejné klíče, pro jakýkoli předpokládaný algoritmus,
jsou větší než 256 bytů. To by eliminovalo jakoukoli výplň a jakékoli úspory z navrhovaných
změn výše, pro Router Identities.

V "hybridním" PQ přístupu, jako to dělá SSL, by PQ klíče byly pouze efemérní,
a neobjevovaly by se v Router Identity.

PQ podpisové klíče nejsou životaschopné,
a Destinations neobsahují šifrovací veřejné klíče.
Statické klíče pro ratchet jsou v Lease Set, ne v Destination,
takže můžeme vyloučit Destinations z následující diskuse.

Takže PQ ovlivňuje pouze Router Infos, a to pouze pro statické PQ (ne efemérní) klíče,
nikoli pro hybridní PQ.
To by bylo pro nový typ šifrování a ovlivnilo by NTCP2, SSU2, a
zašifrované dotazy na databázi a odpovědi.
Odhadovaný časový rámec pro návrh, vývoj a nasazení toho by byl ????????
Ale stalo by se to až po hybridním nebo ratchetu ????????????

Pro další diskusi viz [this topic](http://zzz.i2p/topics/3294).




## Problémy

Může být žádoucí znovu nastavit klíče sítě pomalým tempem, aby se poskytlo krytí pro nové routery.
"Znovu nastavit klíče" může znamenat jednoduše změnit výplň, ne skutečně měnit klíče.

Není možné znovu nastavit existující Destinations.

Měly by být Router Identities s výplní ve veřejném klíčovém polích identifikované odlišným typem šifrování v klíčovém certifikátu? To by způsobilo problémy s kompatibilitou.




## Migrace

Žádné problémy se zpětnou kompatibilitou pro nahrazení klíče ElGamal výplní.

Znovu nastavování klíčů, pokud by bylo implementováno, by bylo podobné tomu,
co bylo provedeno při třech předchozích přechodech router identity:
Od podpisů DSA-SHA1 ke ECDSA, poté k
podpisům EdDSA, a poté ke šifrování X25519.

S ohledem na problémy s zpětnou kompatibilitou, a po zakázání SSU,
implementace mohou zcela odstranit kód ElGamal.
Přibližně 14 % routerů v síti je typu šifrování ElGamal, včetně mnoha floodfillů.

Návrh na sloučení pro Java I2P je na [git.idk.i2p](http://git.idk.i2p/i2p-hackers/i2p.i2p/-/merge_requests/66).
