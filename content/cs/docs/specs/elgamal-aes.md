---
title: "ElGamal/AES + SessionTag šifrování"
description: "Starší end-to-end šifrování kombinující ElGamal, AES, SHA-256 a jednorázové session tagy"
slug: "elgamal-aes"
aliases:
  - "/cs/how_elgamalaes"
  - "/cs/how_elgamalaes/"
lastUpdated: "2020-04"
accurateFor: "0.9.46"
---

## Přehled

ElGamal/AES+SessionTags se používá pro koncové šifrování.

Jako nespolehlivý, neuspořádaný systém založený na zprávách používá I2P jednoduchou kombinaci asymetrických a symetrických šifrovacích algoritmů k zajištění důvernosti a integrity dat pro garlic zprávy. Jako celek se tato kombinace označuje jako ElGamal/AES+SessionTags, ale to je příliš podrobný způsob, jak popsat použití 2048bit ElGamal, AES256, SHA256 a 32bytových nonce.

Když chce router poprvé zašifrovat garlic zprávu pro jiný router, zašifruje klíčový materiál pro AES256 session key pomocí ElGamal a připojí AES256/CBC šifrovaný payload za tento šifrovaný ElGamal blok. Kromě šifrovaného payload obsahuje AES šifrovaná sekce délku payload, SHA256 hash nešifrovaného payload, stejně jako řadu "session tags" - náhodných 32 bajtových nonce. Až příště chce odesílatel zašifrovat garlic zprávu pro jiný router, místo ElGamal šifrování nového session key jednoduše vybere jeden z dříve doručených session tags a AES zašifruje payload jako předtím, pomocí session key použitého s tímto session tag, s předponou samotného session tag. Když router obdrží garlic šifrovanou zprávu, zkontroluje prvních 32 bajtů, zda odpovídají dostupnému session tag - pokud ano, jednoduše AES dešifrují zprávu, ale pokud ne, ElGamal dešifrují první blok.

Každý session tag lze použít pouze jednou, aby se zabránilo interním protivníkům v zbytečném korelování různých zpráv jako pocházejících mezi stejnými routery. Odesílatel ElGamal/AES+SessionTag šifrované zprávy si volí, kdy a kolik tagů doručit, předzásobuje příjemce dostatečným množstvím tagů pro pokrytí salvy zpráv. Garlic zprávy mohou detekovat úspěšné doručení tagů pomocí připojení malé dodatečné zprávy jako clove ("delivery status message") - když garlic zpráva dorazí k zamýšlenému příjemci a je úspěšně dešifrována, tato malá delivery status zpráva je jedním z odhalených cloves a obsahuje instrukce pro příjemce, aby clove poslal zpět původnímu odesílateli (samozřejmě skrze inbound tunnel). Když původní odesílatel obdrží tuto delivery status zprávu, ví, že session tagy připojené v garlic zprávě byly úspěšně doručeny.

Session tagy samy o sobě mají krátkou životnost, po které jsou zahozeny, pokud nejsou použity. Navíc je omezeno množství uložené pro každý klíč, stejně jako počet samotných klíčů - pokud jich přijde příliš mnoho, mohou být zahozeny buď nové nebo staré zprávy. Odesílatel sleduje, zda zprávy používající session tagy procházejí, a pokud není dostatečná komunikace, může zahodit ty, které byly dříve považovány za správně doručené, a vrátit se zpět k plnému nákladnému ElGamal šifrování. Relace bude pokračovat, dokud nebudou vyčerpány nebo nevyprší všechny její tagy.

Relace jsou jednosměrné. Tagy jsou doručovány od Alice k Bobovi a Alice pak používá tagy, jeden po druhém, v následných zprávách pro Boba.

Relace mohou být navázány mezi Destinations, mezi routery nebo mezi routerem a Destination. Každý router a Destination udržuje svůj vlastní Session Key Manager pro sledování Session Keys a Session Tags. Oddělené Session Key Managery zabraňují protivníkům korelaci více Destinations mezi sebou nebo s routerem.

## Příjem zpráv

Každá přijatá zpráva má jednu ze dvou možných podmínek:

1. Je součástí existující relace a obsahuje Session Tag a AES šifrovaný blok
2. Je určeno pro novou relaci a obsahuje jak ElGamal, tak AES šifrované bloky

Když router obdrží zprávu, nejprve předpokládá, že pochází z existující relace a pokusí se vyhledat Session Tag a dešifrovat následující data pomocí AES. Pokud to selže, předpokládá, že je určena pro novou relaci a pokusí se ji dešifrovat pomocí ElGamal.

## Specifikace zprávy nové relace {#new}

Zpráva New Session ElGamal obsahuje dvě části, šifrovaný ElGamal blok a šifrovaný AES blok.

Šifrovaná zpráva obsahuje:

```
   +----+----+----+----+----+----+----+----+
   |                                       |
   +                                       +
   |       ElGamal Encrypted Block         |
   ~                                       ~
   |                                       |
   +         +----+----+----+----+----+----+
   |         |                             |
   +----+----+                             +
   |                                       |
   +                                       +
   |         AES Encrypted Block           |
   ~                                       ~
   |                                       |
   +         +----+----+----+----+----+----+
   |         +
   +----+----+
```
### ElGamal blok

Šifrovaný ElGamal blok má vždy délku 514 bajtů.

Nešifrovaná ElGamal data jsou dlouhá 222 bajtů a obsahují:

```
   +----+----+----+----+----+----+----+----+
   |                                       |
   +                                       +
   |           Session Key                 |
   +                                       +
   |                                       |
   +                                       +
   |                                       |
   +----+----+----+----+----+----+----+----+
   |                                       |
   +                                       +
   |              Pre-IV                   |
   +                                       +
   |                                       |
   +                                       +
   |                                       |
   +----+----+----+----+----+----+----+----+
   +                                       +
   |                                       |
   +                                       +
   |       158 bytes random padding        |
   ~                                       ~
   |                                       |
   +                             +----+----+
   |                             |
   +----+----+----+----+----+----+
```
32bytový [Session Key](/docs/specs/common-structures#type_SessionKey) je identifikátor pro relaci. 32bytový Pre-IV bude použit pro generování IV pro následující AES blok; IV je prvních 16 bajtů SHA-256 hashe Pre-IV.

222bajtový payload je šifrován [pomocí ElGamal](/docs/specs/cryptography#elgamal) a šifrovaný blok je dlouhý 514 bajtů.

### AES Block {#aes}

Nešifrovaná data v AES bloku obsahují následující:

```
   +----+----+----+----+----+----+----+----+
   |tag count|                             |
   +----+----+                             +
   |                                       |
   +                                       +
   |          Session Tags                 |
   ~                                       ~
   |                                       |
   +                                       +
   |                                       |
   +         +----+----+----+----+----+----+
   |         |    payload size   |         |
   +----+----+----+----+----+----+         +
   |                                       |
   +                                       +
   |          Payload Hash                 |
   +                                       +
   |                                       |
   +                             +----+----+
   |                             |flag|    |
   +----+----+----+----+----+----+----+    +
   |                                       |
   +                                       +
   |          New Session Key (opt.)       |
   +                                       +
   |                                       |
   +                                  +----+
   |                                  |    |
   +----+----+----+----+----+----+----+    +
   |                                       |
   +                                       +
   |           Payload                     |
   ~                                       ~
   |                                       |
   +                        +----//---+----+
   |                        |              |
   +----+----+----//---+----+              +
   |          Padding to 16 bytes          |
   +----+----+----+----+----+----+----+----+
```
#### Definice

```
tag count:
    2-byte Integer, 0-200

Session Tags:
    That many 32-byte SessionTags

payload size:
    4-byte Integer

Payload Hash:
    The 32-byte SHA256 Hash of the payload

flag:
    A one-byte value. Normally == 0. If == 0x01, a Session Key follows

New Session Key:
    A 32-byte SessionKey,
    to replace the old key, and is only present if preceding flag is 0x01

Payload:
    the data

Padding:
    Random data to a multiple of 16 bytes for the total length.
    May contain more than the minimum required padding.
```
Minimální délka: 48 bajtů

Data jsou poté [AES šifrována](/docs/specs/cryptography) pomocí session key a IV (vypočítaného z pre-IV) z ElGamal sekce. Délka šifrovaného AES bloku je proměnná, ale vždy je násobkem 16 bytů.

#### Poznámky

- Skutečná maximální délka užitečného zatížení a maximální délka bloku je menší než 64 KB; viz [Přehled I2NP](/docs/protocol/i2np).
- New Session Key se v současnosti nepoužívá a nikdy není přítomen.

## Specifikace zprávy existující relace {#existing}

Úspěšně doručené session tags jsou zapamatovány na krátkou dobu (aktuálně 15 minut), dokud nejsou použity nebo zahozeny. Tag je použit zabalením do Existing Session Message, která obsahuje pouze AES šifrovaný blok a není předcházena ElGamal blokem.

Stávající zpráva relace je následující:

```
   +----+----+----+----+----+----+----+----+
   |                                       |
   +                                       +
   |            Session Tag                |
   +                                       +
   |                                       |
   +                                       +
   |                                       |
   +----+----+----+----+----+----+----+----+
   |                                       |
   +                                       +
   |         AES Encrypted Block           |
   ~                                       ~
   |                                       |
   +                                       +
   |                                       |
   +----+----+----+----+----+----+----+----+
```
#### Definice

```
Session Tag:
    A 32-byte SessionTag
    previously delivered in an AES block

AES Encrypted Block:
    As specified above.
```
Session tag také slouží jako pre-IV. IV je prvních 16 bajtů SHA-256 hashe sessionTag.

Pro dekódování zprávy z existující relace router vyhledá Session Tag a najde přidružený Session Key. Pokud je Session Tag nalezen, AES blok je dešifrován pomocí přidruženého Session Key. Pokud tag není nalezen, předpokládá se, že zpráva je [New Session Message](#new).

## Možnosti konfigurace Session Tag {#config}

Od verze 0.9.2 může klient nakonfigurovat výchozí počet Session Tags k odeslání a nízký práh tagů pro aktuální relaci. Pro krátká streamovaná spojení nebo datagramy mohou být tyto možnosti použity k významnému snížení šířky pásma. Pro podrobnosti viz [specifikace možností I2CP](/docs/protocol/i2cp#options). Nastavení relace může být také přepsáno na základě jednotlivých zpráv. Pro podrobnosti viz [specifikace I2CP Send Message Expires](/docs/specs/i2cp#msg_SendMessageExpires).

## Budoucí práce {#future}

**Poznámka:** ElGamal/AES+SessionTags je nahrazován protokolem ECIES-X25519-AEAD-Ratchet (Návrh 144). Problémy a nápady uvedené níže byly začleněny do návrhu nového protokolu. Následující položky nebudou řešeny v ElGamal/AES+SessionTags.

Existuje mnoho možných oblastí pro optimalizaci algoritmů Session Key Manager; některé mohou ovlivňovat chování streaming knihovny nebo mít významný dopad na celkový výkon.

- Počet doručených tagů může záviset na velikosti zprávy, s ohledem na
  případné doplnění na 1KB ve vrstvě tunnel zpráv.

- Klienti by mohli poslat routeru odhad délky trvání relace jako doporučení
  pro počet požadovaných tagů.

- Dodání příliš málo tagů způsobí, že router přejde na nákladné ElGamal šifrování.

- Router může předpokládat doručení Session Tags, nebo čekat na potvrzení před jejich použitím;
  každá strategie má své kompromisy.

- Pro velmi krátké zprávy by téměř celých 222 bajtů polí pre-IV a padding v ElGamal bloku
  mohlo být použito pro celou zprávu, namísto navazování relace.

- Vyhodnotit strategii paddingu; aktuálně paddujeme na minimálně 128 bajtů.
  Bylo by lepší přidat několik tagů k malým zprávám než paddovat.

- Možná by věci mohly být efektivnější, kdyby byl systém Session Tag obousměrný,
  takže tagy doručené v 'dopředné' cestě by mohly být použity v 'zpětné' cestě,
  čímž by se zabránilo ElGamal v počáteční odpovědi.
  Router v současnosti používá podobné triky, když posílá
  testovací zprávy tunelu sám sobě.

- Změna ze Session Tags na
  [synchronizovaný PRNG](/docs/overview/performance#future#prng).

- Několik z těchto nápadů může vyžadovat nový typ I2NP zprávy, nebo
  nastavit příznak v
  [Delivery Instructions](/docs/specs/tunnel-message#struct_TunnelMessageDeliveryInstructions),
  nebo nastavit magické číslo v prvních několika bajtech pole Session Key
  a přijmout malé riziko, že náhodný Session Key se bude shodovat s magickým číslem.
