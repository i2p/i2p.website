---
title: "Vylepšení přenosu IPv6"
number: "158"
author: "zzz, původní"
created: "2021-03-19"
lastupdated: "2021-04-26"
status: "Uzavřeno"
thread: "http://zzz.i2p/topics/3060"
target: "0.9.50"
---

## Poznámka
Nasazení a testování v síti probíhá.
Podléhá drobným úpravám.


## Přehled

Tento návrh se zaměřuje na implementaci vylepšení přenosů SSU a NTCP2 pro IPv6.


## Motivace

Jak se IPv6 stává stále rozšířenějším po celém světě a nastavení jen s IPv6 (zejména na mobilních zařízeních) se stává běžnějším,
potřebujeme zlepšit podporu IPv6 a odstranit předpoklady,
že všechny směrovače podporují IPv4.



### Kontrola připojení

Při výběru peerů pro tunely nebo při výběru cest OBEP/IBGW pro směrování zpráv,
je užitečné vypočítat, zda se router A může připojit k routeru B.
Obecně to znamená zjistit, zda má A schopnost odchozího spojení pro typ přenosu a adresu (IPv4/v6),
která odpovídá jedné z B inzerovaných příchozích adres.

Nicméně v mnoha případech neznáme schopnosti A a musíme dělat předpoklady.
Pokud je A skrytý nebo za firewallem, adresy nejsou publikovány a nemáme přímé znalosti -
takže předpokládáme, že je schopný IPv4, ale ne schopný IPv6.
Řešením je přidání dvou nových "caps" nebo schopností do informací o routeru, které indikují schopnost odchozího spojení pro IPv4 a IPv6.


### IPv6 Introductors

Naše specifikace [SSU](/en/docs/transport/ssu/) a [SSU-SPEC](/en/docs/spec/ssu/) obsahují chyby a nesrovnalosti ohledně toho,
zda jsou podpůrci IPv6 podporovány pro úvody IPv4.
V každém případě to nikdy nebylo implementováno v Java I2P ani i2pd.
To je třeba napravit.


### IPv6 Introductory

Naše specifikace [SSU](/en/docs/transport/ssu/) a [SSU-SPEC](/en/docs/spec/ssu/) jasně uvádějí, že
Úvody IPv6 nejsou podporovány.
To bylo pod předpokladem, že IPv6 není nikdy za firewallem.
Což zjevně není pravda, a potřebujeme zlepšit podporu pro směrovače IPv6, které jsou za firewallem.


### Schémata úvodů

Legenda: ----- je IPv4, ====== je IPv6

Aktuální pouze IPv4:

```
      Alice                         Bob                  Charlie
  RelayRequest ---------------------->
       <-------------- RelayResponse    RelayIntro ----------->
       <-------------------------------------------- HolePunch
  SessionRequest -------------------------------------------->
       <-------------------------------------------- SessionCreated
  SessionConfirmed ------------------------------------------>
  Data <--------------------------------------------------> Data
```


Úvod IPv4, zavaděč IPv6

```
Alice                         Bob                  Charlie
  RelayRequest ======================>
       <============== RelayResponse    RelayIntro ----------->
       <-------------------------------------------- HolePunch
  SessionRequest -------------------------------------------->
       <-------------------------------------------- SessionCreated
  SessionConfirmed ------------------------------------------>
  Data <--------------------------------------------------> Data
```

Úvod IPv6, zavaděč IPv6


```
Alice                         Bob                  Charlie
  RelayRequest ======================>
       <============== RelayResponse    RelayIntro ===========>
       <============================================ HolePunch
  SessionRequest ============================================>
       <============================================ SessionCreated
  SessionConfirmed ==========================================>
  Data <==================================================> Data
```

Úvod IPv6, zavaděč IPv4

```
Alice                         Bob                  Charlie
  RelayRequest ---------------------->
       <-------------- RelayResponse    RelayIntro ===========>
       <============================================ HolePunch
  SessionRequest ============================================>
       <============================================ SessionCreated
  SessionConfirmed ==========================================>
  Data <==================================================> Data
```


## Design

Budou implementovány tři změny.

- Přidejte schopnosti "4" a "6" do schopností Router Address k indikaci odchozí podpory IPv4 a IPv6
- Přidejte podporu pro úvody IPv4 prostřednictvím zavaděčů IPv6
- Přidejte podporu pro úvody IPv6 prostřednictvím zavaděčů IPv4 a IPv6



## Specifikace

### 4/6 schopnosti

To bylo původně implementováno bez formálního návrhu, ale je to vyžadováno pro
úvody IPv6, takže to zde zahrnujeme.
Viz také [CAPS](http://zzz.i2p/topics/3050).


Jsou definovány dvě nové schopnosti "4" a "6".
Tyto nové schopnosti budou přidány do vlastnosti "caps" v Router Address, nikoliv v kapsách informací o routeru.
V současné době nemáme definovánu vlastnost "caps" pro NTCP2.
Adresa SSU s zavaděči je nyní, ze své definice, IPv4. Úvod IPv6 vůbec nepodporujeme.
Nicméně tento návrh je kompatibilní s úvody IPv6. Viz níže.

Kromě toho může router podporovat připojení přes překryvnou síť, jako je I2P-over-Yggdrasil,
ale nemusí chtít zveřejnit adresu, nebo tato adresa nemá standardní formát IPv4 nebo IPv6.
Tento nový systém schopností by měl být dostatečně flexibilní, aby podporoval i tyto sítě.

Definujeme následující změny:

NTCP2: Přidejte vlastnost "caps"

SSU: Přidat podporu pro adresu routeru bez hostitele nebo zavaděčů, k indikaci odchozí podpory
pro IPv4, IPv6 nebo obojí.

Oba přenosy: definujte následující hodnoty caps:

- "4": Podpora IPv4
- "6": Podpora IPv6

Více hodnot může být podporováno v jedné adrese. Viz níže.
Nejméně jedna z těchto schopností je povinná, pokud není ve vlastní adrese routeru zahrnuta hodnota "host".
Nejvýše jedna z těchto schopností je volitelná, pokud je ve vlastní adrese routeru zahrnuta hodnota "host".
Další přenosové schopnosti mohou být definovány v budoucnosti, aby indikovaly podporu pro překryvné sítě nebo jiné konektivity.


#### Případové studie a příklady

SSU:

SSU s hostitelem: 4/6 volitelný, nikdy více než jeden.
Příklad: SSU caps="4" host="1.2.3.4" key=... port="1234"

Skrytý SSU pouze pro jeden, druhý je publikován: Pouze caps, 4/6.
Příklad: SSU caps="6"

SSU s zavaděči: nikdy nekombinováno. 4 nebo 6 je požadováno.
Příklad: SSU caps="4" iexp0=... ihost0=... iport0=... itag0=... key=...

Skrytý SSU: Pouze caps, 4, 6 nebo 46. Vícenásobné je povoleno.
Není potřeba dvě adresy, jedna s 4 a jedna s 6.
Příklad: SSU caps="46"

NTCP2:

NTCP2 s hostitelem: 4/6 volitelný, nikdy více než jeden.
Příklad: NTCP2 caps="4" host="1.2.3.4" i=... port="1234" s=... v="2"

Skrytý NTCP2 pouze pro jeden, druhý je publikován: Caps, s, v only, 4/6/y, vícenásobné je povoleno.
Příklad: NTCP2 caps="6" i=... s=... v="2"

Skrytý NTCP2: Caps, s, v pouze 4/6, vícenásobné je povoleno Není potřeba dvě adresy, jedna s 4 a jedna s 6.
Příklad: NTCP2 caps="46" i=... s=... v="2"



### Zavaděči IPv6 pro IPv4

K nápravě chyb a nesrovnalostí ve specifikacích jsou nutné následující změny.
Toto jsme také popsali jako "část 1" návrhu.

#### Změny specifikace

[SSU](/en/docs/transport/ssu/) momentálně říká (poznámky k IPv6):

IPv6 je podporováno od verze 0.9.8. Publikované adresy relé mohou být IPv4 nebo IPv6, a komunikace Alice-Bob může probíhat přes IPv4 nebo IPv6.

Přidejte následující:

Specifikace se změnila od verze 0.9.8, ale komunikace Alice-Bob přes IPv6 nebyla ve skutečnosti podporována do verze 0.9.50.
Dřívější verze Java routerů chybně zveřejňovaly schopnost 'C' pro adresy IPv6,
i když ve skutečnosti nefungovaly jako zavaděči přes IPv6.
Proto by routery měly důvěřovat schopnosti 'C' na IPv6 adresách pouze, pokud je verze routeru 0.9.50 nebo vyšší.



[SSU-SPEC](/en/docs/spec/ssu/) momentálně říká (Relay Request):

IP adresa je zahrnuta pouze pokud je odlišná od zdrojové adresy a portu paketu.
V aktuální implementaci je délka IP vždy 0 a port je vždy 0,
a příjemce by měl použít zdrojovou adresu a port paketu.
Tato zpráva může být odeslána přes IPv4 nebo IPv6. Pokud je to IPv6, musí Alice zahrnout svou IPv4 adresu a port.

Přidejte následující:

IP a port musí být zahrnuty pro úvod IPv4 při odesílání této zprávy přes IPv6.
Toto je podporováno od verze 0.9.50.



### Úvody IPv6

Všechny tři relé zprávy SSU (RelayRequest, RelayResponse a RelayIntro) obsahují pole délky IP
k určení délky následující IP adresy (Alice, Bob nebo Charlie).

Proto není nutná žádná změna formátu zpráv.
Pouze textové změny specifikací, které indikují, že 16-bytové IP adresy jsou povoleny.

K nápravě specifikací jsou nutné následující změny.
Toto jsme také popsali jako "část 2" návrhu.


#### Změny specifikace

[SSU](/en/docs/transport/ssu/) momentálně říká (poznámky k IPv6):

Komunikace Bob-Charlie a Alice-Charlie probíhá pouze přes IPv4.

[SSU-SPEC](/en/docs/spec/ssu/) momentálně říká (Relay Request):

Neexistují žádné plány na implementaci přenosu pro IPv6.

Změňte na:

Přenos pro IPv6 je podporován od verze 0.9.xx

[SSU-SPEC](/en/docs/spec/ssu/) momentálně říká (Relay Response):

Adresa Charlieho musí být IPv4, protože to je adresa, na kterou Alice pošle SessionRequest po Hole Punch.
Neexistují žádné plány na implementaci přenosu pro IPv6.

Změňte na:

Adresa Charlieho může být IPv4 nebo, od verze 0.9.xx, IPv6.
To je adresa, na kterou Alice pošle SessionRequest po Hole Punch.
Přenos pro IPv6 je podporován od verze 0.9.xx

[SSU-SPEC](/en/docs/spec/ssu/) momentálně říká (Relay Intro):

Adresa Alice má v aktuální implementaci vždy 4 byty, protože Alice se snaží připojit k Charliemu přes IPv4.
Tato zpráva musí být odeslána přes etablované připojení IPv4,
protože to je jediný způsob, jak Bob zná Charlieho IPv4 adresu, kterou poslat zpět Alice v odpovědi RelayResponse.

Změňte na:

Pro IPv4 má adresa Alice vždy 4 byty, protože Alice se snaží připojit k Charliemu přes IPv4.
Od verze 0.9.xx je podporováno IPv6 a adresa Alice může mít 16 bytů.

Pro IPv4 musí být tato zpráva odeslána přes etablované připojení IPv4,
protože to je jediný způsob, jak Bob zná Charlieho IPv4 adresu, kterou poslat zpět Alice v odpovědi RelayResponse.
Od verze 0.9.xx je podporováno IPv6 a tato zpráva může být odeslána přes etablované připojení IPv6.

Také přidejte:

Od verze 0.9.xx musí každá SSU adresa publikovaná se zavaděči obsahovat "4" nebo "6" v možnosti "caps".


## Migrace

Všechny staré routery by měly ignorovat vlastnost caps u NTCP2 a neznámé znaky schopností v vlastnosti SSU caps.

Jakákoli adresa SSU se zavaděči, která neobsahuje cap "4" nebo "6", se považuje za určenou pro úvod IPv4.
