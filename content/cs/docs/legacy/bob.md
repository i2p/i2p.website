---
title: "BOB - Basic Open Bridge"
description: "Zastaralé API pro správu destinací"
slug: "bob"
aliases:
  - "/cs/docs/api/bob"
  - "/cs/docs/api/bob/"
  - "/cs/bob"
  - "/cs/bob/"
lastUpdated: "2025-05"
accurateFor: "0.9.8"
---

## Varování - Zastaralé

Není určen pro použití v nových aplikacích. BOB, jak je zde specifikován, podporuje pouze typ podpisu DSA-SHA1. BOB nebude rozšířen o podporu nových typů podpisů nebo dalších pokročilých funkcí. Nové aplikace by měly používat [SAM V3](/docs/api/samv3).

Podpora BOB byla odstraněna z nových instalací Java I2P od verze 1.7.0 (2022-02). Stále bude fungovat v Java I2P původně nainstalovaném jako verze 1.6.1 nebo starší, i po aktualizacích, ale není podporována a může se kdykoli pokazit. BOB je stále podporována i2pd od května 2025, ale aplikace by se měly přesto migrovat na SAMv3 z výše uvedených důvodů. Viz [dokumentace i2pd](https://i2pd.readthedocs.io/en/latest/devs/i2pd-specifics/) pro jakékoli rozšíření API zde zdokumentovaného, které jsou podporována i2pd.

V tomto bodě již většina dobrých nápadů z BOB byla začleněna do SAMv3, které má více funkcí a je více využíváno v praxi. BOB může stále fungovat na některých instalacích (viz výše), ale nezískává pokročilé funkce dostupné pro SAMv3 a v podstatě není podporován, kromě i2pd.

## Jazykové knihovny pro BOB API

- Go - [ccondom](https://bitbucket.org/kallevedin/ccondom)
- Python - i2py-bob (git.repo.i2p)
- Twisted - [txi2p](https://pypi.python.org/pypi/txi2p)
- C++ - [bobcpp](https://gitlab.com/rszibele/bobcpp)

## Přehled

`KEYS` = pár klíčů veřejný+soukromý, tyto jsou BASE64

`KEY` = veřejný klíč, také BASE64

`ERROR` jak název napovídá vrací zprávu `"ERROR "+DESCRIPTION+"\n"`, kde `DESCRIPTION` je popis toho, co se pokazilo.

`OK` vrací `"OK"` a pokud mají být vrácena data, jsou na stejném řádku. `OK` znamená, že příkaz je dokončen.

Řádky `DATA` obsahují informace, které jste požadovali. Na jeden požadavek může připadnout více řádků `DATA`.

**POZNÁMKA:** Příkaz help je JEDINÝ příkaz, který má výjimku z pravidel... může skutečně nevrátit nic! Toto je záměrné, protože help je příkaz pro ČLOVĚKA a ne pro APLIKACI.

## Připojení a verze

Veškerý stavový výstup BOB je po řádcích. Řádky mohou být ukončeny \\n nebo \\r\\n, v závislosti na systému. Po připojení BOB vypíše dva řádky:

```
BOB version
OK
```
Aktuální verze je: 00.00.10

Upozorňujeme, že předchozí verze používaly hexadecimální číslice velkými písmeny a neodpovídaly standardům verzování I2P. Doporučuje se, aby následující verze používaly pouze číslice 0-9.

### Historie verzí

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">I2P Router Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Changes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">00.00.10</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.8</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">current version</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">00.00.00 - 00.00.0F</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">&nbsp;</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">development versions</td>
    </tr>
  </tbody>
</table>
## Příkazy

**UPOZORNĚNÍ:** Pro AKTUÁLNÍ podrobnosti o příkazech POUŽIJTE vestavěný příkaz nápovědy. Jednoduše se připojte telnetem na localhost 2827 a zadejte help, abyste získali úplnou dokumentaci ke každému příkazu.

Příkazy nikdy nezastarávají ani se nemění, nicméně nové příkazy se čas od času přidávají.

```
COMMAND     OPERAND                             RETURNS
help        (optional command to get help on)   NOTHING or OK and description of the command
clear                                           ERROR or OK
getdest                                         ERROR or OK and KEY
getkeys                                         ERROR or OK and KEYS
getnick     tunnelname                          ERROR or OK
inhost      hostname or IP address              ERROR or OK
inport      port number                         ERROR or OK
list                                            ERROR or DATA lines and final OK
lookup      hostname                            ERROR or OK and KEY
newkeys                                         ERROR or OK and KEY
option      key1=value1 key2=value2...          ERROR or OK
outhost     hostname or IP address              ERROR or OK
outport     port number                         ERROR or OK
quiet                                           ERROR or OK
quit                                            OK and terminates the command connection
setkeys     KEYS                                ERROR or OK and KEY
setnick     tunnel nickname                     ERROR or OK
show                                            ERROR or OK and information
showprops                                       ERROR or OK and information
start                                           ERROR or OK
status      tunnel nickname                     ERROR or OK and information
stop                                            ERROR or OK
verify      KEY                                 ERROR or OK
visit                                           OK, and dumps BOB's threads to the wrapper.log
zap                                             nothing, quits BOB
```
Jakmile je vše nastaveno, všechny TCP sockety mohou a budou se blokovat podle potřeby, a není třeba žádných dalších zpráv do/z příkazového kanálu. To umožňuje routeru řídit rychlost toku dat bez výbuchů OOM chyb jako SAM, který se zadusí při pokusu protlačit mnoho streamů dovnitř nebo ven jedním socketem -- to se nemůže škálovat, když máte hodně připojení!

Co je také pěkné na tomto konkrétním rozhraní je, že psaní čehokoli pro rozhraní s ním je mnohem mnohem jednodušší než SAM. Po nastavení není třeba žádné další zpracování. Jeho konfigurace je tak jednoduchá, že lze použít velmi jednoduché nástroje, jako je nc (netcat), aby ukázaly na nějakou aplikaci. Hodnota spočívá v tom, že lze naplánovat časy spuštění a vypnutí pro aplikaci, aniž by bylo třeba aplikaci změnit nebo ji dokonce zastavit. Místo toho můžete doslova "odpojit" cíl a znovu ho "zapojit". Dokud se při spouštění mostu používají stejné IP/port adresy a klíče cíle, normální TCP aplikace si to nebude všímat a nezpozoruje to. Bude jednoduše oklamána -- cíle nejsou dostupné a nic nepřichází dovnitř.

## Příklady

Pro následující příklad nastavíme velmi jednoduché místní loopback připojení se dvěma destinacemi. Destinace "mouth" bude služba CHARGEN z INET superserver daemonu. Destinace "ear" bude místní port, do kterého se můžete připojit pomocí telnetu a sledovat, jak se vysypává pěkný ASCII test.

### Příklad dialogu relace

Jednoduchý telnet 127.0.0.1 2827 funguje.

- A = Aplikace
- C = Odpověď příkazu BOB.

```
FROM    TO      DIALOGUE
C       A       BOB 00.00.10
C       A       OK
A       C       setnick mouth
C       A       OK Nickname set to mouth
A       C       newkeys
C       A       OK ZMPz1zinTdy3~zGD~f3g9aikZTipujEvvXOEyYfq4Su-mNKerqG710hFbkR6P-xkouVyNQsqWLI8c6ngnkSwGdUfM7hGccqBYDjIubTrlr~0g2-l0vM7Y8nSqtFrSdMw~pyufXZ0Ys3NqUSb8NuZXpiH2lCCkFG21QPRVfKBGwvvyDVU~hPVfBHuR8vkd5x0teMXGGmiTzdB96DuNRWayM0y8vkP-1KJiPFxKjOXULjuXhLmINIOYn39bQprq~dAtNALoBgd-waZedYgFLvwHDCc9Gui8Cpp41EihlYGNW0cu0vhNFUN79N4DEpO7AtJyrSu5ZjFTAGjLw~lOvhyO2NwQ4RiC4UCKSuM70Fz0BFKTJquIjUNkQ8pBPBYvJRRlRG9HjAcSqAMckC3pvKKlcTJJBAE8GqexV7rdCCIsnasJXle-6DoWrDkY1s1KNbEVH6i1iUEtmFr2IHTpPeFCyWfZ581CAFNRbbUs-MmnZu1tXAYF7I2-oXTH2hXoxCGAAAA
```
**POZNAMENEJTE SI VÝŠE UVEDENÝ DESTINATION KEY, VÁŠ BUDE JINÝ!**

```
FROM    TO      DIALOGUE
A       C       outhost 127.0.0.1
C       A       OK outhost set
A       C       outport 19
C       A       OK outbound port set
A       C       start
C       A       OK tunnel starting
```
V tomto okamžiku nedošlo k žádné chybě, destination s přezdívkou "mouth" je nastavena. Když kontaktujete poskytnutou destination, ve skutečnosti se připojíte ke službě `CHARGEN` na `19/TCP`.

Nyní pro druhou polovinu, abychom mohli skutečně kontaktovat tuto destinaci.

```
FROM    TO      DIALOGUE
C       A       BOB 00.00.10
C       A       OK
A       C       setnick ear
C       A       OK Nickname set to ear
A       C       newkeys
C       A       OK 8SlWuZ6QNKHPZ8KLUlExLwtglhizZ7TG19T7VwN25AbLPsoxW0fgLY8drcH0r8Klg~3eXtL-7S-qU-wdP-6VF~ulWCWtDMn5UaPDCZytdGPni9pK9l1Oudqd2lGhLA4DeQ0QRKU9Z1ESqejAIFZ9rjKdij8UQ4amuLEyoI0GYs2J~flAvF4wrbF-LfVpMdg~tjtns6fA~EAAM1C4AFGId9RTGot6wwmbVmKKFUbbSmqdHgE6x8-xtqjeU80osyzeN7Jr7S7XO1bivxEDnhIjvMvR9sVNC81f1CsVGzW8AVNX5msEudLEggpbcjynoi-968tDLdvb-CtablzwkWBOhSwhHIXbbDEm0Zlw17qKZw4rzpsJzQg5zbGmGoPgrSD80FyMdTCG0-f~dzoRCapAGDDTTnvjXuLrZ-vN-orT~HIVYoHV7An6t6whgiSXNqeEFq9j52G95MhYIfXQ79pO9mcJtV3sfea6aGkMzqmCP3aikwf4G3y0RVbcPcNMQetDAAAA
A       C       inhost 127.0.0.1
C       A       OK inhost set
A       C       inport 37337
C       A       OK inbound port set
A       C       start
C       A       OK tunnel starting
A       C       quit
C       A       OK Bye!
```
Teď už jen stačí připojit se pomocí telnet na 127.0.0.1, port 37337, a poslat cílový klíč nebo adresu hostitele z adresáře, se kterým se chceme spojit. V tomto případě se chceme spojit s "mouth", takže jen vložíme klíč a odešleme ho.

**POZNÁMKA:** Příkaz "quit" v příkazovém kanálu NEODPOJUJE tunely jako u SAM.

```
$ telnet 127.0.0.1 37337
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
ZMPz1zinTdy3~zGD~f3g9aikZTipujEvvXOEyYfq4Su-mNKerqG710hFbkR6P-xkouVyNQsqWLI8c6ngnkSwGdUfM7hGccqBYDjIubTrlr~0g2-l0vM7Y8nSqtFrSdMw~pyufXZ0Ys3NqUSb8NuZXpiH2lCCkFG21QPRVfKBGwvvyDVU~hPVfBHuR8vkd5x0teMXGGmiTzdB96DuNRWayM0y8vkP-1KJiPFxKjOXULjuXhLmINIOYn39bQprq~dAtNALoBgd-waZedYgFLvwHDCc9Gui8Cpp41EihlYGNW0cu0vhNFUN79N4DEpO7AtJyrSu5ZjFTAGjLw~lOvhyO2NwQ4RiC4UCKSuM70Fz0BFKTJquIjUNkQ8pBPBYvJRRlRG9HjAcSqAMckC3pvKKlcTJJBAE8GqexV7rdCCIsnasJXle-6DoWrDkY1s1KNbEVH6i1iUEtmFr2IHTpPeFCyWfZ581CAFNRbbUs-MmnZu1tXAYF7I2-oXTH2hXoxCGAAAA
 !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefg
!"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefgh
"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghi
#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghij
$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijk
...
```
Po několika virtuálních mílích tohoto výpisu stiskněte `Control-]`

```
...
cdefghijklmnopqrstuvwxyz{|}~ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJK
defghijklmnopqrstuvwxyz{|}~ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKL
efghijklmnopqrstuvwxyz{|}~ !"#$%&'()*+,-./0123456789:;<=
telnet> c
Connection closed.
```
Toto se stalo...

```
telnet -> ear -> i2p -> mouth -> chargen -.
telnet <- ear <- i2p <- mouth <-----------'
```
Můžete se také připojit k I2P stránkám!

```
$ telnet 127.0.0.1 37337
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
i2host.i2p
GET / HTTP/1.1

HTTP/1.1 200 OK
Date: Fri, 05 Dec 2008 14:20:28 GMT
Connection: close
Content-Type: text/html
Content-Length: 3946
Last-Modified: Fri, 05 Dec 2008 10:33:36 GMT
Accept-Ranges: bytes

<html>
<head>
  <title>I2HOST</title>
  <link rel="shortcut icon" href="favicon.ico">
</head>
...
<a href="http://sponge.i2p/">--Sponge.</a></pre>
<img src="/counter.gif" alt="!@^7A76Z!#(*&%"> visitors. </body>
</html>
Connection closed by foreign host.
$
```
Docela cool, ne? Zkuste si některé další známé I2P SITES, pokud chcete, neexistující adresy atd., abyste získali představu o tom, jaký výstup očekávat v různých situacích. Většinou se doporučuje ignorovat jakékoli chybové zprávy. Byly by pro aplikaci bezvýznamné a jsou prezentovány pouze pro lidské ladění.

### Úklid

Nyní, když jsme s nimi hotovi, ukončeme naše destinace.

Nejprve se podívejme, jaké přezdívky destinací máme.

```
FROM    TO      DIALOGUE
A       C       list
C       A       DATA NICKNAME: mouth STARTING: false RUNNING: true STOPPING: false KEYS: true QUIET: false INPORT: not_set INHOST: localhost OUTPORT: 19 OUTHOST: 127.0.0.1
C       A       DATA NICKNAME: ear STARTING: false RUNNING: true STOPPING: false KEYS: true QUIET: false INPORT: 37337 INHOST: 127.0.0.1 OUTPORT: not_set OUTHOST: localhost
C       A       OK Listing done
```
Dobře, tady jsou. Nejprve odstraníme "mouth".

```
FROM    TO      DIALOGUE
A       C       getnick mouth
C       A       OK Nickname set to mouth
A       C       stop
C       A       OK tunnel stopping
A       C       clear
C       A       OK cleared
```
Nyní odstraňte "ear", všimněte si, že se to stává, když píšete příliš rychle, a ukazuje vám, jak vypadají typické chybové zprávy ERROR.

```
FROM    TO      DIALOGUE
A       C       getnick ear
C       A       OK Nickname set to ear
A       C       stop
C       A       OK tunnel stopping
A       C       clear
C       A       ERROR tunnel is active
A       C       clear
C       A       OK cleared
A       C       quit
C       A       OK Bye!
```
## Tichý režim

Nebudu se obtěžovat ukázat příklad přijímací strany mostu, protože je velmi jednoduchý. Existují dvě možná nastavení a přepíná se příkazem "quiet".

Výchozí nastavení NENÍ tiché a první data, která přijdou do vašeho naslouchajícího socketu, jsou destination, která navazuje kontakt. Jedná se o jeden řádek obsahující BASE64 adresu následovanou novým řádkem. Vše po tom je určeno pro skutečné zpracování aplikací.

V tichém režimu si to představte jako běžné internetové připojení. Žádná extra data vůbec nepřicházejí. Je to stejné, jako kdybyste byli normálně připojeni k běžnému internetu. Tento režim umožňuje formu transparentnosti podobnou té, která je dostupná na stránkách nastavení tunnel v konzoli routeru, takže můžete použít BOB k nasměrování destinace na webový server například, a nemuseli byste webový server vůbec upravovat.

## Výhody BOB

Výhoda používání BOB pro tento účel je, jak jsme již diskutovali dříve. Mohli byste naplánovat náhodné doby provozu aplikace, přesměrovat na jiný stroj atd. Jedním z možných použití může být například snaha zmást odhady dostupnosti router-to-destination. Mohli byste zastavit a spustit destination úplně jiným procesem, abyste vytvořili náhodné doby dostupnosti a nedostupnosti služeb. Tímto způsobem byste pouze zastavili možnost kontaktovat takovou službu, aniž byste ji museli vypínat a restartovat. Mohli byste přesměrovat a nasměrovat na jiný stroj ve vaší LAN během aktualizací, nebo nasměrovat na sadu záložních strojů v závislosti na tom, co běží, atd., atd. Pouze vaše představivost omezuje to, co byste s BOB mohli dělat.
