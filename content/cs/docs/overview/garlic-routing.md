---
title: "Garlic Routing"
description: "Porozumění terminologii, architektuře a implementaci garlic routing v I2P"
slug: "garlic-routing"
aliases:
  - "/cs/how_garlicrouting"
  - "/cs/how_garlicrouting/"
lastUpdated: "2025-10"
accurateFor: "0.9.12"
---

## Garlic Routing a terminologie "Garlic"

Termíny "garlic routing" a "garlic encryption" jsou často používány poměrně volně při odkazování na technologii I2P. Zde vysvětlujeme historii těchto termínů, jejich různé významy a použití "garlic" metod v I2P.

"Garlic routing" byl poprvé použit [Michaelem J. Freedmanem](https://www.cs.princeton.edu/~mfreed/) v [diplomové práci](https://www.freehaven.net/papers.html) Free Haven od Rogera Dingledinea, sekce 8.1.1 (červen 2000), jako odvozený od [Onion Routing](https://www.onion-router.net/).

"Garlic" mohl být původně použit vývojáři I2P, protože I2P implementuje formu balíčkování, jak popisuje Freedman, nebo jednoduše pro zdůraznění obecných rozdílů od Toru. Konkrétní zdůvodnění se mohlo ztratit v historii. Obecně se při odkazování na I2P může termín "garlic" vztahovat k jedné ze tří věcí:

1. Vrstvené šifrování
2. Sdružování více zpráv dohromady
3. ElGamal/AES šifrování

Bohužel používání terminologie "garlic" v I2P v minulých letech nebylo vždy přesné; čtenář je proto upozorněn na opatrnost při setkání s tímto termínem. Doufejme, že níže uvedené vysvětlení věci objasní.

### Vrstvené šifrování

Onion routing je technika pro budování cest neboli tunnelů přes řadu uzlů a následné využívání tohoto tunnelu. Zprávy jsou opakovaně šifrovány odesílatelem a poté dešifrovány každým uzlem na cestě. Během fáze budování jsou každému uzlu odhaleny pouze instrukce pro směrování k dalšímu uzlu. Během provozní fáze jsou zprávy předávány tunnelem a zpráva spolu s instrukcemi pro směrování jsou odhaleny pouze koncovému bodu tunnelu.

To je podobné způsobu, jakým Mixmaster (viz [porovnání sítí](/docs/overview/comparison/)) odesílá zprávy - vezme zprávu, zašifruje ji veřejným klíčem příjemce, vezme tuto zašifrovanou zprávu a znovu ji zašifruje (spolu s instrukcemi specifikujícími další skok), a pak vezme výslednou zašifrovanou zprávu a tak dále, dokud nemá jednu vrstvu šifrování na každý skok podél cesty.

V tomto smyslu je „garlic routing" jako obecný koncept identický s „onion routingem". Jak je implementován v I2P, existuje samozřejmě několik rozdílů oproti implementaci v Toru; viz níže. I přesto existují značné podobnosti, takže I2P těží z [velkého množství akademického výzkumu o onion routingu](https://www.onion-router.net/Publications.html), [Toru a podobných mixnets](https://freehaven.net/anonbib/topic.html).

### Sdružování více zpráv

Michael Freedman definoval "garlic routing" jako rozšíření onion routingu, ve kterém je spojeno více zpráv dohromady. Každou zprávu nazval "bulb" (cibulka). Všechny zprávy, každá se svými vlastními pokyny pro doručení, jsou odhaleny v koncovém bodě. To umožňuje efektivní spojení "reply block" (bloku odpovědi) onion routingu s původní zprávou.

Tento koncept je implementován v I2P, jak je popsáno níže. Náš termín pro garlic "cibule" je "stroužky". Může být obsaženo libovolné množství zpráv, místo jen jediné zprávy. To je významný rozdíl od onion routingu implementovaného v Toru. Nicméně, je to jen jeden z mnoha hlavních architektonických rozdílů mezi I2P a Torem; možná to samo o sobě nestačí k ospravedlnění změny v terminologii.

Další rozdíl od metody popsané Freedmanem je, že cesta je jednosměrná - neexistuje žádný "bod obratu" jako u onion routingu nebo mixmaster reply bloků, což výrazně zjednodušuje algoritmus a umožňuje flexibilnější a spolehlivější doručování.

### ElGamal/AES šifrování

V některých případech může "garlic encryption" jednoduše znamenat [ElGamal/AES+SessionTag](/docs/specs/elgamal-aes/) šifrování (bez více vrstev).

---

## "Garlic" metody v I2P

Nyní, když jsme definovali různé "garlic" termíny, můžeme říci, že I2P používá garlic routing, bundling a šifrování na třech místech:

1. Pro budování a směrování skrze tunnely (vrstvené šifrování)
2. Pro určování úspěchu nebo selhání doručení zpráv end-to-end (sdružování)
3. Pro publikování některých záznamů síťové databáze (snižování pravděpodobnosti úspěšného útoku analýzou provozu) (ElGamal/AES)

Existují také významné způsoby, jak lze tuto techniku využít ke zlepšení výkonu sítě, využívání kompromisů mezi latencí/propustností transportu a větvení dat prostřednictvím redundantních cest pro zvýšení spolehlivosti.

### Budování a směrování tunelů

V I2P jsou tunnely jednosměrné. Každá strana vytvoří dva tunnely, jeden pro odchozí a jeden pro příchozí provoz. Proto jsou pro jednu zprávu tam a zpět potřeba čtyři tunnely.

Tunnely jsou vybudovány a následně používány s vrstveným šifrováním. Toto je popsáno na [stránce implementace tunnelů](/docs/specs/tunnel-implementation/). Pro šifrování používáme [ElGamal/AES+SessionTag](/docs/specs/elgamal-aes/).

Tunnely jsou univerzálním mechanismem pro přenos všech [I2NP zpráv](/docs/specs/i2np/) a Garlic Messages se nepoužívají k budování tunelů. Nesdružujeme více I2NP zpráv do jediné Garlic Message pro rozbalení na koncovém bodu odchozího tunelu; šifrování tunelu je dostatečné.

### Sdružování zpráv od konce ke konci

Ve vrstvě nad tunely doručuje I2P end-to-end zprávy mezi [Destinations](/docs/specs/common-structures/). Stejně jako v rámci jednoho tunelu používáme pro šifrování [ElGamal/AES+SessionTag](/docs/specs/elgamal-aes/). Každá klientská zpráva doručená do routeru prostřednictvím [I2CP rozhraní](/docs/api/i2cp/) se stává jedním Garlic Clove se svými vlastními Delivery Instructions uvnitř Garlic Message. Delivery Instructions mohou specifikovat Destination, Router nebo Tunnel.

Obecně bude Garlic Message obsahovat pouze jeden clove. Router však periodicky zabalí dva další cloves do Garlic Message:

![Garlic Message Cloves](/images/garliccloves.svg)

1. **Zpráva o stavu doručení**, s instrukcemi pro doručení specifikujícími, že má být odeslána zpět do původního routeru jako potvrzení. To je podobné "reply bloku" nebo "reply onionu" popsanému v referencích. Používá se pro určení úspěchu nebo neúspěchu doručení zprávy end-to-end. Původní router může při neobdržení zprávy o stavu doručení v očekávaném časovém období upravit směrování k cílové destinaci nebo podniknout jiné kroky.

2. **Database Store Message**, obsahující LeaseSet pro původní cíl, s Delivery Instructions specifikující router vzdáleného konce. Periodickým přibalováním LeaseSet router zajišťuje, že vzdálený konec bude schopen udržovat komunikaci. Jinak by vzdálený konec musel dotazovat floodfill router na záznam v síťové databázi a všechny LeaseSets by musely být publikovány do síťové databáze, jak je vysvětleno na [stránce síťové databáze](/docs/specs/common-structures/).

Ve výchozím nastavení jsou zprávy Delivery Status a Database Store seskupeny, když se změní místní LeaseSet, když jsou doručeny dodatečné Session Tags, nebo pokud zprávy nebyly seskupeny během předchozí minuty.

Zjevně jsou dodatečné zprávy v současnosti seskupovány pro specifické účely a nejsou součástí obecného směrovacího schématu.

Od vydání 0.9.12 je Delivery Status Message zabalena do další Garlic Message odesílatelem, takže obsah je zašifrován a není viditelný pro routery na zpáteční cestě.

### Ukládání do Floodfill Network Database

Jak je vysvětleno na [stránce síťové databáze](/docs/specs/common-structures/), místní leaseSety jsou odesílány do floodfill routerů ve zprávě Database Store Message zabalenou do Garlic Message, takže nejsou viditelné pro odchozí bránu tunelu.

---

## Budoucí práce

Mechanismus Garlic Message je velmi flexibilní a poskytuje strukturu pro implementaci mnoha typů metod doručování mixnet. Společně s nepoužívanou možností zpoždění v Delivery Instructions tunelové zprávy je možné široké spektrum strategií dávkování, zpoždění, míchání a směrování.

Zejména existuje potenciál pro mnohem větší flexibilitu na koncovém bodu odchozího tunelu. Zprávy by odtud mohly být směrovány do jednoho z několika tunelů (čímž by se minimalizovaly point-to-point spojení), nebo multicast do několika tunelů pro redundanci, nebo pro streamování audia a videa.

Takové experimenty mohou být v rozporu s potřebou zajistit bezpečnost a anonymitu, například omezováním určitých směrovacích cest, omezováním typů I2NP zpráv, které mohou být předávány podél různých cest, a vynucováním určitých časů expirace zpráv.

Jako součást ElGamal/AES šifrování obsahuje garlic zpráva množství výplňových dat určené odesílatelem, což umožňuje odesílateli aktivně se bránit proti analýze provozu. Toto se v současnosti nepoužívá, kromě požadavku na doplnění na násobek 16 bajtů.

Šifrování dalších zpráv do a z [floodfill routerů](/docs/specs/common-structures/).

---

## Reference

- Termín garlic routing byl poprvé použit v [diplomové práci](https://www.freehaven.net/papers.html) Rogera Dingledina pro Free Haven (červen 2000), viz Sekce 8.1.1 napsaná [Michaelem J. Freedmanem](https://www.cs.princeton.edu/~mfreed/).
- [Publikace Onion Router](https://www.onion-router.net/Publications.html)
- [Onion Routing (Wikipedia)](https://en.wikipedia.org/wiki/Onion_routing)
- [Garlic Routing (Wikipedia)](https://en.wikipedia.org/wiki/Garlic_routing)
- [Tor Project](https://www.torproject.org/)
- [Free Haven Anonbib](https://freehaven.net/anonbib/topic.html)
- Onion routing bylo poprvé popsáno v [Hiding Routing Information](https://www.onion-router.net/Publications/IH-1996.pdf) od Davida M. Goldschlaga, Michaela G. Reeda a Paula F. Syversona v roce 1996.
