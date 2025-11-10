---
title: "Stavové poznámky I2P k 2004-08-03"
date: 2004-08-03
author: "jr"
description: "Týdenní aktualizace stavu I2P věnovaná výkonu verze 0.3.4, vývoji nové webové konzole a různým aplikačním projektům"
categories: ["status"]
---

Ahoj všichni, ať máme tuhle aktualizaci stavu z krku.

## Rejstřík:

1. 0.3.4 status
2. On deck for 0.3.4.1
3. New web console / I2PTunnel controller
4. 0.4 stuff
5. Other development activities
6. ???

## 1) 0.3.4 stav

S minulým vydáním 0.3.4 si nová síť vede docela dobře – připojení k IRC vydrží v kuse několik hodin a načítání eepsite(I2P Site) se zdá být poměrně spolehlivé. Propustnost je stále obecně nízká, i když mírně vylepšená (dříve jsem stabilně vídal 4-5KBps, nyní stabilně vídám 5-8KBps). oOo zveřejnil dvojici skriptů shrnujících aktivitu na IRC, včetně doby cesty zprávy tam a zpět a délky trvání spojení (vycházejících z hypercubusova bogobota, který byl nedávno commitnut do CVS)

## 2) Plánováno pro 0.3.4.1

Jak si všichni na 0.3.4 všimli, byl jsem *cough* trochu příliš upovídaný ve svém logování, což bylo v cvs napraveno. Kromě toho, poté co jsem napsal pár nástrojů ke stresovému testování ministreaming lib, jsem přidal 'choke', aby to nespotřebovalo ohromné množství paměti (zablokuje se při pokusu přidat do bufferu streamu více než 128KB dat, takže při odesílání velkého souboru váš router nemá celý ten soubor nahraný v paměti). Myslím, že to pomůže s problémy OutOfMemory, které lidé zaznamenávají, ale přidám ještě nějaký dodatečný monitorovací / ladicí kód, abych to ověřil.

## 3) Nová webová konzole / správce I2PTunnel

Kromě výše uvedených úprav pro 0.3.4.1 máme připravenou první verzi nové konzole routeru k prvním testům. Z několika důvodů ji zatím nebudeme dodávat jako součást výchozí instalace, takže až za pár dní vyjde revize 0.3.4.1, budou k dispozici pokyny, jak ji zprovoznit. Jak jste viděli, s webovým designem jsem na tom opravdu bídně a jak mnozí z vás říkají, měl bych přestat se patlat v aplikační vrstvě a udělat jádro i router naprosto stabilní. Takže i když nová konzole už má mnoho dobrých funkcí, které chceme (konfigurovat router kompletně prostřednictvím několika jednoduchých webových stránek, nabídnout rychlé a přehledné shrnutí stavu routeru, zpřístupnit možnost vytvářet / upravovat / zastavovat / spouštět různé instance I2PTunnel), opravdu potřebuji pomoc od lidí, kteří se vyznají ve webových technologiích.

Technologie použité v nové webové konzoli jsou standardní JSP, CSS a jednoduché JavaBeans, které dotazují router / I2PTunnels na data a zpracovávají požadavky. Vše je zabaleno do dvojice souborů .war a nasazeno do integrovaného webserveru Jetty (který je třeba spouštět prostřednictvím řádků clientApp.* v routeru). Hlavní JSP a beany konzole routeru jsou po technické stránce poměrně solidní, i když nové JSP a beany, které jsem vytvořil pro správu instancí I2PTunnel, jsou tak trochu zbastlené.

## 4) věci k 0.4

Kromě nového webového rozhraní bude vydání 0.4 obsahovat nový instalátor od hypercubuse, který jsme zatím vlastně pořádně neintegrovali. Také musíme provést ještě několik simulací ve velkém měřítku (zejména pokud jde o obsluhu asymetrických aplikací, jako je IRC a outproxy (výstupní proxy)). Kromě toho jsou tu některé aktualizace, které musím prosadit do kaffe/classpath, abychom rozběhli novou webovou infrastrukturu na JVM s otevřeným zdrojovým kódem. Navíc musím dát dohromady ještě nějaké dokumenty (jeden o škálovatelnosti a další analyzující bezpečnost/anonymitu v několika běžných scénářích). Také chceme, aby všechna vylepšení, s nimiž přijdete, byla integrována do nové webové konzole.

A mimochodem, opravte jakékoli chyby, které pomůžete najít :)

## 5) Další vývojové aktivity

Ačkoli se na základním systému I2P dělá spousta pokroku, to je jen polovina příběhu - mnoho z vás odvádí skvělou práci na aplikacích a knihovnách, díky nimž je I2P užitečné. V historii chatu jsem viděl několik dotazů ohledně toho, kdo na čem pracuje, takže aby se ty informace dostaly ven, tady je vše, co o tom vím (pokud pracujete na něčem, co tu není uvedeno a chcete se podělit, pokud se mýlím, nebo pokud chcete probrat svůj pokrok, ozvěte se!)

### Active development:

- python SAM/I2P lib (devs: sunshine, aum)
- C SAM lib (devs: nightblade)
- python kademlia/I2P DHT (devs: aum)
- v2v - Voice over I2P (devs: aum)
- outproxy load balancing (devs: mule)

### Development I've heard about but don't know the status of:

- swarming file transfer / BT (devs: nickster)

### Paused development:

- Enclave DHT (devs: nightblade)
- perl SAM lib (devs: BrianR)
- I2PSnark / BT (devs: eco)
- i2pIM (devs: thecrypto)
- httptunnel (devs: mihi)
- MyI2P address book (devs: jrandom)
- MyI2P blogging (devs: jrandom)

## 6) ???

To je zatím všechno, co mě napadá - stavte se později dnes večer na schůzce a můžeme pokecat o věcech. Jako vždy ve 21:00 GMT na #i2p na obvyklých serverech.

=jr
