---
title: "Neviditelné Multihoming"
number: "140"
author: "str4d"
created: "2017-05-22"
lastupdated: "2017-07-04"
status: "Otevřený"
thread: "http://zzz.i2p/topics/2335"
---

## Přehled

Tento návrh načrtává design protokolu umožňujícího I2P klientovi, službě nebo externímu balancer procesu spravovat více routerů, které neviditelně hostují jediný [Destination](http://localhost:63465/en/docs/specs/common-structures/#destination).

Návrh momentálně nespecifikuje konkrétní implementaci. Mohl by být implementován jako rozšíření [I2CP](/en/docs/specs/i2cp/), nebo jako nový protokol.


## Motivace

Multihoming spočívá ve využití více routerů k hostování stejného destinace. Současný způsob, jak v I2P provádět multihoming, je provozovat stejnou destinaci na každém routeru nezávisle; router, který je právě používán klienty, je ten poslední, který publikoval [LeaseSet](http://localhost:63465/en/docs/specs/common-structures/#leaseset).

To je hack a pravděpodobně nebude fungovat pro rozsáhlé webové stránky. Řekněme, že máme 100 multihoming routerů, každý s 16 tunely. To je 1600 publikovaných LeaseSet každých 10 minut, což je téměř 3 za sekundu. Floodfill routery by byly zahlcené a aktivovaly by se omezovače. A to ještě předtím, než zmíníme lookup trafic.

[Proposal 123](/en/proposals/123-new-netdb-entries/) řeší tento problém pomocí meta-LeaseSet, který uvádí 100 skutečných hashů LeaseSet. Lookup se stává dvoufázovým procesem: nejdříve hledání meta-LeaseSet a poté jednoho z uvedených LeaseSets. To je dobré řešení problému s lookup trafficem, ale samo o sobě vytváří významný únik soukromí: Je možné určit, které multihoming routery jsou online sledováním publikovaného meta-LeaseSet, protože každý skutečný LeaseSet odpovídá jednomu routeru.

Potřebujeme způsob, jakým by I2P klient nebo služba mohla rozprostřít jedinou Destinaci mezi více routerů tak, aby to bylo nerozeznatelné od používání jednoho routeru (z pohledu LeaseSet samotného).


## Design

### Definice

    Uživatěl
        Osoba nebo organizace, která chce provádět multihoming svých Destinací. Zde se uvažuje s jedinou Destinací bez ztráty obecnosti (WLOG).

    Klient
        Aplikace nebo služba běžící za Destinací. Může to být aplikace na straně klienta, serveru nebo peer-to-peer aplikace; odkazujeme na ni jako na klienta ve smyslu, že se připojuje k I2P routerům.

        Klient se skládá ze tří částí, které mohou být všechny ve stejném procesu nebo mohou být rozděleny mezi procesy nebo stroje (v nastavení s více klienty):

        Balancer
            Část klienta, která spravuje výběr peerů a budování tunelů. V každém okamžiku je pouze jeden balancer a komunikuje se všemi I2P routery. Mohou existovat záložní balancery.

        Frontend
            Část klienta, která může běžet paralelně. Každý frontend komunikuje s jedním I2P routerem.

        Backend
            Část klienta, která je sdílena mezi všemi frontend. Nemá přímou komunikaci s jakýmkoliv I2P routerem.

    Router
        I2P router spravovaný uživatelem, který sídlí na hranici mezi I2P sítí a uživatelskou sítí (podobně jako hraniční zařízení v korporačních sítích). Buduje tunely pod velením balanceru a směruje pakety pro klienta nebo frontend.

### Přehled na vysoké úrovni

Představte si následující požadovanou konfiguraci:

- Aplikační klient s jednou Destinací.
- Čtyři routery, každý spravující tři příchodové tunely.
- Všechny dvanáct tunelů by měly být publikovány v jednom LeaseSet.

Jednokanálový klient

```
                -{ [Tunel 1]===\
                 |-{ [Tunel 2]====[Router 1]-----
                 |-{ [Tunel 3]===/               \
                 |                                 \
                 |-{ [Tunel 4]===\                 \
  [Destinace]    |-{ [Tunel 5]====[Router 2]-----   \
    \            |-{ [Tunel 6]===/               \   \
     [LeaseSet]--|                               [Klient]
                 |-{ [Tunel 7]===\               /   /
                 |-{ [Tunel 8]====[Router 3]-----   /
                 |-{ [Tunel 9]===/                 /
                 |                                 /
                 |-{ [Tunel 10]==\               /
                 |-{ [Tunel 11]===[Router 4]-----
                  -{ [Tunel 12]==/

Vícekanálový klient

```
                -{ [Tunel 1]===\
                 |-{ [Tunel 2]====[Router 1]---------[Frontend 1]
                 |-{ [Tunel 3]===/          \                    \
                 |                            \                    \
                 |-{ [Tunel 4]===\            \                    \
  [Destinace]    |-{ [Tunel 5]====[Router 2]---\-----[Frontend 2]   \
    \            |-{ [Tunel 6]===/          \   \                \   \
     [LeaseSet]--|                         [Balancer]            [Backend]
                 |-{ [Tunel 7]===\          /   /                /   /
                 |-{ [Tunel 8]====[Router 3]---/-----[Frontend 3]   /
                 |-{ [Tunel 9]===/            /                    /
                 |                            /                    /
                 |-{ [Tunel 10]==\          /                    /
                 |-{ [Tunel 11]===[Router 4]---------[Frontend 4]
                  -{ [Tunel 12]==/

### Obecný proces klienta
- Načíst nebo vygenerovat Destinaci.

- Otevřít sezení s každým routerem, svázané s Destinací.

- Pravidelně (asi každých deset minut, ale více či méně v závislosti na živosti tunelů):

  - Získat rychlou vrstvu od každého routeru.

  - Použít nadmnožinu peerů pro vytvoření tunelů k/od každého routeru.

    - Ve výchozím nastavení budou tunely k/od určitého routeru používat peery z rychlé vrstvy tohoto routeru, ale toto není protokolem vynuceno.

  - Shromáždit sadu aktivních příchozích tunelů od všech aktivních routerů a vytvořit LeaseSet.

  - Publikovat LeaseSet prostřednictvím jednoho nebo více routerů.

### Rozdíly oproti I2CP
Pro vytvoření a správu této konfigurace potřebuje klient následující novou funkcionalitu nad rámec toho, co je aktuálně poskytováno [I2CP](/en/docs/specs/i2cp/):

- Povědět routeru, aby vybudoval tunely, aniž by pro ně vytvořil LeaseSet.
- Získat seznam aktuálních tunelů v příchozí skupině.

Navíc by následující funkce umožnily významnou flexibilitu v tom, jak klient spravuje své tunely:

- Získat obsah rychlé vrstvy routeru.
- Povědět routeru, aby vybudoval příchodový nebo odchodový tunel pomocí daného seznamu peerů.

### Náčrt protokolu

```
         Klient                           Router

                    --------------------->  Vytvořit Sezení
   Stav Sezení     <---------------------
                    --------------------->  Získat Rychlou Vrstvu
       Seznam Peerů  <---------------------
                    --------------------->  Vytvořit Tunel
   Stav Tunelu  <---------------------
                    --------------------->  Získat Skupinu Tunelů
      Seznam Tunelek  <---------------------
                    --------------------->  Publikovat LeaseSet
                    --------------------->  Odeslat Paket
     Stav Odeslání <---------------------
     Obdržený Paket  <---------------------

### Zprávy
    Vytvořit Sezení
        Vytvořit sezení pro danou Destinaci.

    Stav Sezení
        Potvrzení, že sezení bylo nastaveno, a klient nyní může začít budovat tunely.

    Získat Rychlou Vrstvu
        Požádat o seznam peerů, které by router momentálně považoval za vhodné pro budování tunelů.

    Seznam Peerů
        Seznam peerů známých routeru.

    Vytvořit Tunel
        Požádat, aby router vytvořil nový tunel pomocí určených peerů.

    Stav Tunelu
        Výsledek určitého vytvoření tunelu, jakmile je dostupný.

    Získat Skupinu Tunelů
        Požádat o seznam aktuálních tunelů v příchozí nebo odchozí skupině pro Destinaci.

    Seznam Tunelek
        Seznam tunelů pro požadovanou skupinu.

    Publikovat LeaseSet
        Požádat, aby router publikoval poskytnutý LeaseSet prostřednictvím jednoho z odchozích tunelů pro Destinaci. Není potřeba zpětné potvrzení; router by měl pokračovat ve zkoušení, dokud nebude přesvědčen, že LeaseSet byl publikován.

    Odeslat Paket
        Odchozí paket od klienta. Př optionally specifikuje odchozí tunel, kterým musí (mělo by?) být zasláno.

    Stav Odeslání
        Informuje klienta o úspěchu nebo neúspěchu odeslání paketu.

    Obdržený Paket
        Příchozí paket pro klienta. Volitelně specifikuje příchozí tunel, kterým byl paket přijat(?)


## Bezpečnostní důsledky

Z pohledu routerů je tento design funkcionálně ekvivalentní současné situaci. Router stále buduje všechny tunely, udržuje své vlastní profily peerů a zajišťuje oddělení mezi routerem a klientskými operacemi. V základní konfiguraci je úplně identický, protože tunely pro daný router jsou budovány z jeho vlastní rychlé vrstvy.

Z pohledu netDB je jeden LeaseSet vytvořený prostřednictvím tohoto protokolu identický s současnou situací, protože využívá předexistující funkčnost. Nicméně, pro větší LeaseSety přibližující se 16 Lease, by mohlo být možné pro pozorovatele určit, že LeaseSet je multihoming:

- Současná maximální velikost rychlé vrstvy je 75 peerů. Inbound Gateway (IBGW, uzel publikovaný v Lease) je vybírán z části vrstvy (rozdělený náhodně na tunelové skupiny podle hashe, ne podle počtu):

      1 skok
          Celá rychlá vrstva

      2 skoky
          Polovina rychlé vrstvy
          (výchozí do poloviny roku 2014)

      3+ skoky
          Čtvrtina rychlé vrstvy
          (3 je aktuální výchozí hodnota)

  To znamená, že průměrně budou IBGWs z množiny 20-30 peerů.

- V nastavení s jednou doménou, plně 16-tunelový LeaseSet by měl 16 IBGWs náhodně vybraných ze sady až (řekněme) 20 peerů.

- V nastavení s 4 routery pro multihoming využívajícím výchozí konfiguraci, plně 16-tunelový LeaseSet by měl 16 IBGWs náhodně vybraných ze sady nejvíce 80 peerů, ačkoli je pravděpodobné, že mezi routery bude frakce společných peerů.

Takže s výchozí konfigurací by mohlo být možné pomocí statistické analýzy zjistit, že LeaseSet je generován tímto protokolem. Mohlo by být rovněž možné zjistit, kolik routerů existuje, ačkoli efekt rychlé vrstvy by snížil efektivitu této analýzy.

Protože klient má plnou kontrolu nad výběrem peerů, mohl by tento únik informací být snížen nebo eliminován výběrem IBGWs z omezené sady peerů.


## Kompatibilita

Tento design je plně zpětně kompatibilní se sítí, protože nejsou provedeny žádné změny formátu [LeaseSet](http://localhost:63465/en/docs/specs/common-structures/#leaseset). Všechny routery by musely být obeznámeny s novým protokolem, ale to není problém, jelikož by všechny byly řízeny stejnou entitou.


## Poznámky k výkonu a škálovatelnosti

Horní limit 16 [Lease](http://localhost:63465/en/docs/specs/common-structures/#lease) na LeaseSet není tímto návrhem změněn. Pro Destinace, které vyžadují více tunelů než tohle, existují dvě možné úpravy sítě:

- Zvýšit horní limit velikosti LeaseSetů. Toto by bylo nejjednodušší implementovat (i když by to stále vyžadovalo kompletní podporu napříč sítí, než by to mohlo být široce použito), ale mohlo by to vést k pomalejšímu vyhledávání kvůli větší velikosti paketů. Maximální proveditelná velikost LeaseSetu je definována MTU podkladových transportů a proto je kolem 16 kB.

- Implementovat [Proposal 123](/en/proposals/123-new-netdb-entries/) pro hierarchické LeaseSety. V kombinaci s tímto návrhem by Destinace pro podřízené LeaseSety mohly být rozloženy napříč více routery, efektivně fungující jako více IP adres pro službu na clearnetu.


## Poděkování

Díky psi za diskusi, která vedla k tomuto návrhu.
