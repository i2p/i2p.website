---
title: "Neviditelný Multihoming"
number: "140"
author: "str4d"
created: "2017-05-22"
lastupdated: "2017-07-04"
status: "Otevřít"
thread: "http://zzz.i2p/topics/2335"
toc: true
---

## Přehled

Tento návrh popisuje design protokolu umožňujícího I2P klientovi, službě nebo externímu balancovacímu procesu transparentně spravovat více routerů hostujících jedinou [Destination](http://localhost:63465/docs/specs/common-structures/#destination).

Návrh momentálně nespecifikuje konkrétní implementaci. Mohl by být implementován jako rozšíření [I2CP](/docs/specs/i2cp/), nebo jako nový protokol.

## Motivace

Multihoming je situace, kdy je pro hostování stejné Destination použito více routerů. Současný způsob multihomingu v I2P spočívá v nezávislém spuštění stejné Destination na každém routeru; router, který je klienty v daném okamžiku používán, je ten, který naposledy publikoval LeaseSet.

Tohle je hack a pravděpodobně nebude fungovat pro velké weby v měřítku. Řekněme, že máme 100 multihoming routerů, každý se 16 tunely. To je 1600 publikací LeaseSet každých 10 minut, nebo téměř 3 za sekundu. Floodfilly by se přetížily a začaly by fungovat omezení. A to ještě ani nezmiňujeme vyhledávací provoz.

Návrh 123 řeší tento problém pomocí meta-LeaseSet, který uvádí 100 skutečných hashů LeaseSet. Vyhledávání se stává dvoustupňovým procesem: nejprve se vyhledá meta-LeaseSet a poté jeden z pojmenovaných LeaseSets. Toto je dobré řešení problému s vyhledávacím provozem, ale samo o sobě vytváří významný únik soukromí: Je možné určit, které multihoming routery jsou online, sledováním publikovaného meta-LeaseSet, protože každý skutečný LeaseSet odpovídá jedinému routeru.

Potřebujeme způsob, jak může I2P klient nebo služba rozdělit jednu Destination napříč více routery, způsobem, který je nerozlišitelný od používání jediného routeru (z pohledu samotného LeaseSet).

## Návrh

### Definitions

    User
        The person or organisation wanting to multihome their Destination(s). A
        single Destination is considered here without loss of generality (WLOG).

    Client
        The application or service running behind the Destination. It may be a
        client-side, server-side, or peer-to-peer application; we refer to it as
        a client in the sense that it connects to the I2P routers.

        The client consists of three parts, which may all be in the same process
        or may be split across processes or machines (in a multi-client setup):

        Balancer
            The part of the client that manages peer selection and tunnel
            building. There is a single balancer at any one time, and it
            communicates with all I2P routers. There may be failover balancers.

        Frontend
            The part of the client that can be operated in parallel. Each
            frontend communicates with a single I2P router.

        Backend
            The part of the client that is shared between all frontends. It has
            no direct communication with any I2P router.

    Router
        An I2P router run by the user that sits at the boundary between the I2P
        network and the user's network (akin to an edge device in corporate
        networks). It builds tunnels under the command of a balancer, and routes
        packets for a client or frontend.

### High-level overview

Představte si následující požadovanou konfiguraci:

- Klientská aplikace s jednou Destination.
- Čtyři routery, každý spravující tři příchozí tunely.
- Všech dvanáct tunelů by mělo být publikováno v jednom LeaseSet.

### Single-client

```
                -{ [Tunnel 1]===\
                 |-{ [Tunnel 2]====[Router 1]-----
                 |-{ [Tunnel 3]===/               \
                 |                                 \
                 |-{ [Tunnel 4]===\                 \
  [Destination]  |-{ [Tunnel 5]====[Router 2]-----   \
    \            |-{ [Tunnel 6]===/               \   \
     [LeaseSet]--|                               [Client]
                 |-{ [Tunnel 7]===\               /   /
                 |-{ [Tunnel 8]====[Router 3]-----   /
                 |-{ [Tunnel 9]===/                 /
                 |                                 /
                 |-{ [Tunnel 10]==\               /
                 |-{ [Tunnel 11]===[Router 4]-----
                  -{ [Tunnel 12]==/
```
### Definice

```
                -{ [Tunnel 1]===\
                 |-{ [Tunnel 2]====[Router 1]---------[Frontend 1]
                 |-{ [Tunnel 3]===/          \                    \
                 |                            \                    \
                 |-{ [Tunnel 4]===\            \                    \
  [Destination]  |-{ [Tunnel 5]====[Router 2]---\-----[Frontend 2]   \
    \            |-{ [Tunnel 6]===/          \   \                \   \
     [LeaseSet]--|                         [Balancer]            [Backend]
                 |-{ [Tunnel 7]===\          /   /                /   /
                 |-{ [Tunnel 8]====[Router 3]---/-----[Frontend 3]   /
                 |-{ [Tunnel 9]===/            /                    /
                 |                            /                    /
                 |-{ [Tunnel 10]==\          /                    /
                 |-{ [Tunnel 11]===[Router 4]---------[Frontend 4]
                  -{ [Tunnel 12]==/
```
### Přehled na vysoké úrovni

- Načíst nebo vygenerovat Destination.

- Otevřít relaci s každým routerem, vázanou na Destination.

- Pravidelně (přibližně každých deset minut, ale více či méně na základě
  životnosti tunelu):

- Získejte rychlou úroveň z každého routeru.

- Použijte nadmnožinu peerů k budování tunnelů do/z každého routeru.

    - By default, tunnels to/from a particular router will use peers from
      that router's fast tier, but this is not enforced by the protocol.

- Shromáždit sadu aktivních příchozích tunelů ze všech aktivních routerů a vytvořit LeaseSet.

- Publikovat LeaseSet prostřednictvím jednoho nebo více routerů.

### Jeden klient

Pro vytvoření a správu této konfigurace potřebuje klient následující novou funkcionalitu nad rámec toho, co v současnosti poskytuje [I2CP](/docs/specs/i2cp/):

- Říct routeru, aby vybudoval tunely, aniž by pro ně vytvořil LeaseSet.
- Získat seznam aktuálních tunelů v inbound poolu.

Navíc by následující funkcionalita umožnila významnou flexibilitu v tom, jak klient spravuje své tunnely:

- Získat obsah rychlé úrovně routeru.
- Říct routeru, aby vybudoval příchozí nebo odchozí tunel pomocí daného seznamu
  peerů.

### Více klientů

```
         Client                           Router

                    --------------------->  Create Session
   Session Status  <---------------------
                    --------------------->  Get Fast Tier
        Peer List  <---------------------
                    --------------------->  Create Tunnel
    Tunnel Status  <---------------------
                    --------------------->  Get Tunnel Pool
      Tunnel List  <---------------------
                    --------------------->  Publish LeaseSet
                    --------------------->  Send Packet
      Send Status  <---------------------
  Packet Received  <---------------------
```
### Obecný klientský proces

**Vytvořit relaci** - Vytvoří relaci pro danou Destination.

**Stav relace** - Potvrzení, že relace byla nastavena a klient nyní může začít budovat tunnely.

**Get Fast Tier** - Vyžádání seznamu peerů, přes které by router aktuálně zvážil budování tunelů.

**Seznam peerů** - Seznam peerů známých routeru.

**Vytvořit Tunnel** - Požádat router, aby vybudoval nový tunnel přes zadané uzly.

**Stav tunelu** - Výsledek konkrétního vytvoření tunelu, jakmile je dostupný.

**Získat pool tunelů** - Požadavek na seznam aktuálních tunelů v příchozím nebo odchozím poolu pro Destination.

**Seznam tunelů** - Seznam tunelů pro požadovaný pool.

**Publikovat LeaseSet** - Požadavek, aby router publikoval poskytnutý LeaseSet prostřednictvím jednoho z odchozích tunelů pro Cíl. Není potřeba žádný stav odpovědi; router by měl pokračovat v opakovaných pokusech, dokud nebude spokojen s tím, že LeaseSet byl publikován.

**Odeslat Packet** - Odchozí packet od klienta. Volitelně specifikuje odchozí tunnel, kterým musí (měl by?) být packet odeslán.

**Send Status** - Informuje klienta o úspěchu nebo neúspěchu odeslání paketu.

**Packet Received** - Příchozí paket pro klienta. Volitelně specifikuje příchozí tunnel, kterým byl paket přijat(?)

## Security implications

Z pohledu routerů je tento návrh funkčně ekvivalentní současnému stavu. Router stále buduje všechny tunely, udržuje své vlastní profily peerů a vynucuje oddělení mezi router a klientskými operacemi. Ve výchozí konfiguraci je zcela identický, protože tunely pro daný router jsou budovány z jeho vlastní rychlé vrstvy.

Z pohledu netDB je jednotlivý LeaseSet vytvořený prostřednictvím tohoto protokolu identický se současným stavem, protože využívá již existující funkcionalitu. Nicméně u větších LeaseSets blížících se 16 Leases může být pro pozorovatele možné určit, že LeaseSet je multihomed:

- Aktuální maximální velikost rychlé úrovně je 75 peerů. Inbound Gateway
  (IBGW, uzel publikovaný v Lease) je vybrán z části této úrovně
  (náhodně rozdělené podle hash pro každý tunnel pool, nikoli podle počtu):

      1 hop
          The whole fast tier

      2 hops
          Half of the fast tier
          (the default until mid-2014)

      3+ hops
          A quarter of the fast tier
          (3 being the current default)

To znamená, že v průměru budou IBGW pocházet ze skupiny 20-30 peerů.

- V jednodomé konfiguraci by úplný 16-tunelový LeaseSet měl 16 IBGW náhodně vybraných ze sady až (řekněme) 20 peerů.

- V 4-routerovém multihomed nastavení používajícím výchozí konfiguraci by měl úplný 16-tunnel LeaseSet 16 IBGW náhodně vybraných ze sady maximálně 80 peerů, ačkoli mezi routery bude pravděpodobně zlomek společných peerů.

Takže s výchozí konfigurací může být možné prostřednictvím statistické analýzy zjistit, že LeaseSet je generován tímto protokolem. Mohlo by být také možné zjistit, kolik je routerů, ačkoli efekt změn v rychlých vrstvách by snížil účinnost této analýzy.

Jelikož má klient plnou kontrolu nad tím, které peer vybere, toto unikání informací by mohlo být sníženo nebo eliminováno výběrem IBGW z redukované sady peer.

## Compatibility

Tento návrh je zcela zpětně kompatibilní se sítí, protože nedochází k žádným změnám formátu LeaseSet. Všechny routery by musely být informovány o novém protokolu, ale to není problém, jelikož by všechny byly ovládány stejnou entitou.

## Performance and scalability notes

Horní limit 16 Lease na LeaseSet zůstává tímto návrhem nezměněn. Pro Destinations, které vyžadují více tunelů než je tento limit, existují dvě možné síťové modifikace:

- Zvýšit horní limit velikosti LeaseSets. Toto by bylo nejjednodušší k implementaci (ačkoli by to stále vyžadovalo rozsáhlou podporu v síti, než by to mohlo být široce používáno), ale mohlo by to vést k pomalejším vyhledáváním kvůli větším velikostem paketů. Maximální proveditelná velikost LeaseSet je definována MTU podkladových transportů, a proto je kolem 16kB.

- Implementovat Návrh 123 pro vrstvené LeaseSets. V kombinaci s tímto návrhem by mohly být Destinations pro pod-LeaseSets rozloženy napříč více routery, což by efektivně fungovalo jako více IP adres pro službu na clearnetu.

## Acknowledgements

Díky psi za diskuzi, která vedla k tomuto návrhu.
