---
title: "Přehled transportu"
description: "Přehled transportní vrstvy I2P pro komunikaci mezi routery typu point-to-point"
slug: "transport"
aliases:
  - "/cs/transport"
  - "/cs/transport/"
lastUpdated: "2026-03"
accurateFor: "0.9.69"
---

## Transporty v I2P

"Transport" v I2P je metoda pro přímou komunikaci typu bod-bod mezi dvěma routery. Transports musí poskytovat důvěrnost a integritu proti externím protivníkům a současně ověřovat, že kontaktovaný router je ten, který by měl danou zprávu obdržet.

I2P podporuje více transportů současně. V současnosti jsou implementovány tři transporty:

1. [NTCP](/docs/legacy/ntcp/), Java New I/O (NIO) TCP transport
2. [SSU](/docs/legacy/ssu/), neboli Secure Semireliable UDP
3. [NTCP2](/docs/specs/ntcp2/), nová verze NTCP

Každý poskytuje paradigma "připojení" s autentizací, řízením toku, potvrzeními a retransmisí.

- Spolehlivé doručování [I2NP](/docs/specs/i2np/) zpráv. Transporty podporují doručování I2NP zpráv POUZE. Nejsou to univerzální datové roury.
- Doručování zpráv v pořadí NENÍ garantováno všemi transporty.
- Udržování sady router adres, jedné nebo více pro každý transport, které router publikuje jako své globální kontaktní informace (RouterInfo). Každý transport se může připojit pomocí jedné z těchto adres, která může být IPv4 nebo (od verze 0.9.8) IPv6.
- Výběr nejlepšího transportu pro každou odchozí zprávu
- Řazení odchozích zpráv podle priority do fronty
- Omezení šířky pásma, jak odchozího tak příchozího, podle konfigurace routeru
- Nastavení a ukončování transportních připojení
- Šifrování point-to-point komunikace
- Udržování limitů připojení pro každý transport, implementace různých prahových hodnot pro tyto limity a komunikace stavu prahových hodnot routeru, aby mohl provádět operační změny na základě stavu
- Otevírání portů firewallu pomocí UPnP (Universal Plug and Play)
- Kooperativní procházení NAT/Firewallu
- Detekce lokální IP různými metodami, včetně UPnP, kontroly příchozích připojení a výčtu síťových zařízení
- Koordinace stavu firewallu a lokální IP a změn kteréhokoli z nich mezi transporty
- Komunikace stavu firewallu a lokální IP a změn kteréhokoli z nich routeru a uživatelskému rozhraní
- Určení konsenzu času, který se používá k periodické aktualizaci času routeru jako záloha pro NTP
- Udržování stavu pro každý peer, včetně toho, zda je připojen, zda byl nedávno připojen a zda byl dostupný při posledním pokusu
- Kvalifikace platných IP adres podle místní sady pravidel
- Respektování automatizovaných a manuálních seznamů zakázaných peerů udržovaných routerem a odmítání odchozích a příchozích připojení k těmto peerům

---

Transportní subsystém v I2P poskytuje následující služby:

## Transportní služby

---

- Router nemá publikované adresy, takže je považován za "skrytý" a nemůže přijímat příchozí připojení
- Router je za firewallem, a proto publikuje SSU adresu, která obsahuje seznam spolupracujících uzlů nebo "introducers", kteří pomohou s NAT traversal (viz [SSU specifikace](/docs/legacy/ssu/) pro podrobnosti)
- Router není za firewallem nebo má otevřené NAT porty; publikuje jak NTCP, tak SSU adresy obsahující přímo přístupné IP a porty.

Transportní subsystém udržuje sadu router adres, z nichž každá obsahuje transportní metodu, IP a port. Tyto adresy tvoří inzerované kontaktní body a jsou publikovány routerem do síťové databáze. Adresy mohou také obsahovat libovolnou sadu dalších možností.

## Transportní adresy

Každá transportní metoda může publikovat více router adres.

Typické scénáře jsou:

---

- Konfigurace transportních preferencí
- Zda je transport již připojen k peer
- Počet aktuálních připojení ve srovnání s různými prahovými hodnotami limitů připojení
- Zda nedávné pokusy o připojení k peer selhaly
- Velikost zprávy, protože různé transporty mají různé limity velikosti
- Zda peer může přijímat příchozí připojení pro daný transport, jak je inzerováno v jeho RouterInfo
- Zda by připojení bylo nepřímé (vyžadující introducery) nebo přímé
- Transportní preference peer, jak je inzerována v jeho RouterInfo

Transportní systém doručuje pouze [I2NP zprávy](/docs/specs/i2np/). Transport vybraný pro jakoukoli zprávu je nezávislý na protokolech a obsahu vyšší vrstvy (zprávy routeru nebo klienta, zda externí aplikace používala TCP nebo UDP pro připojení k I2P, zda vyšší vrstva používala [streaming knihovnu](/docs/api/streaming/) nebo [datagramy](/docs/api/datagrams/), atd.).

## Výběr transportu

Pro každou odchozí zprávu transportní systém vyžádá "nabídky" od každého transportu. Transport s nejnižší (nejlepší) nabídkou vyhraje a obdrží zprávu k doručení. Transport může odmítnout podat nabídku.

Zda transport nabídne a s jakou hodnotou, závisí na mnoha faktorech:

Obecně jsou hodnoty nabídek vybírány tak, aby dva routery byly v daný okamžik propojeny pouze jedním transportem. Nicméně to není požadavek.

- Transport podobný TLS/SSH
- "Nepřímý" transport pro routery, které nejsou dostupné pro všechny ostatní routery (jedna forma "omezených tras")
- Tor-kompatibilní pluggable transports

---

Další transporty mohou být vyvíjeny, včetně:

## Nové transporty a budoucí práce

Pokračuje práce na úpravě výchozích limitů připojení pro každý transport. I2P je navrženo jako "mesh síť", kde se předpokládá, že jakýkoli router se může připojit k jakémukoli jinému routeru. Tento předpoklad může být narušen routery, které překročily své limity připojení, a routery, které jsou za restriktivními stavovými firewally (omezené trasy).

- Přenos podobný TLS/SSH
- „Nepřímý“ přenos pro směrovače, které nejsou dosažitelné všemi ostatními směrovači (jedna forma „omezených tras“)
- Tor-kompatibilní připojitelné přenosy

Současné limity připojení jsou vyšší pro SSU než pro NTCP, založené na předpokladu, že paměťové požadavky pro NTCP připojení jsou vyšší než pro SSU. Nicméně, jelikož NTCP buffery jsou částečně v kernelu a SSU buffery jsou na Java heap, tento předpoklad je obtížné ověřit.

Analyzujte [Breaking and Improving Protocol Obfuscation](http://www.iis.se/docs/hjelmvik_breaking.pdf) a podívejte se, jak může padding transportní vrstvy věci zlepšit.

Analyzujte [Breaking and Improving Protocol Obfuscation](http://www.iis.se/docs/hjelmvik_breaking.pdf) a zjistěte, jak by mohlo vylepšit věci přidávání náhodných dat (padding) na transportní vrstvě.
