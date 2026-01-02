---
title: "Formát přístupového filtru"
description: "Syntaxe souborů filtrů řízení přístupu pro tunnel"
slug: "filter-format"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

Přístupové filtry umožňují správcům serveru I2PTunnel povolit, zakázat nebo omezit příchozí spojení na základě zdrojové Destination (identifikátor koncového bodu v I2P) a nedávné rychlosti navazování spojení. Filtr je prostý textový soubor s pravidly. Soubor se čte shora dolů a **první odpovídající pravidlo rozhoduje**.

> Změny v definici filtru se projeví **při restartu tunnelu**. Některá sestavení mohou za běhu znovu načítat seznamy uložené v souborech, ale počítejte s restartem, abyste měli jistotu, že se změny uplatní.

## Formát souboru

- Jedno pravidlo na řádek.  
- Prázdné řádky se ignorují.  
- `#` začíná komentář, který pokračuje až do konce řádku.  
- Pravidla se vyhodnocují v daném pořadí; použije se první shoda.

## Prahové hodnoty

**Práh** určuje, kolik pokusů o připojení od jedné Destinace je povoleno v klouzavém časovém okně.

- **Číselné:** `N/S` znamená povolit `N` připojení za `S` sekund. Příklad: `15/5` umožňuje až 15 připojení každých 5 sekund. Pokus `N+1` v rámci tohoto okna je zamítnut.  
- **Klíčová slova:** `allow` znamená bez omezení. `deny` znamená vždy zamítnout.

## Syntaxe pravidel

Pravidla mají tento tvar:

```
<threshold> <scope> <target>
```
Kde:

- `<threshold>` je `N/S`, `allow` nebo `deny`  
- `<scope>` je jedno z `default`, `explicit`, `file` nebo `record` (viz níže)  
- `<target>` závisí na rozsahu

### Výchozí pravidlo

Použije se, když žádné jiné pravidlo neodpovídá. Je povoleno pouze **jedno** výchozí pravidlo. Pokud není zadáno, jsou neznámé destinace povoleny bez omezení.

```
15/5 default
allow default
deny default
```
### Explicitní pravidlo

Cílí na konkrétní Destination (cílovou adresu v I2P) podle Base32 adresy (například `example1.b32.i2p`) nebo plného klíče.

```
15/5 explicit example1.b32.i2p
deny explicit example2.b32.i2p
allow explicit example3.b32.i2p
```
### Pravidlo založené na souboru

Cílí na **všechny** Destinations (cílová identita v I2P) uvedené v externím souboru. Každý řádek obsahuje jednu Destination; komentáře `#` a prázdné řádky jsou povoleny.

```
15/5 file /var/i2p/throttled.txt
deny file /var/i2p/blocked.txt
allow file /var/i2p/trusted.txt
```
> Provozní poznámka: Některé implementace pravidelně znovu načítají seznamy souborů. Pokud upravíte seznam, zatímco tunnel běží, počítejte s krátkým zpožděním, než jsou změny zaznamenány. Pro okamžité uplatnění změn restartujte.

### Nahrávač (plynulé ovládání)

**recorder** sleduje pokusy o připojení a zapisuje Destinations (identifikátory cíle v I2P), které překročí prahovou hodnotu, do souboru. Poté můžete na tento soubor odkázat v pravidle `file`, abyste na budoucí pokusy uplatnili omezení nebo blokování.

```
# Start permissive
allow default

# Record Destinations exceeding 30 connections in 5 seconds
30/5 record /var/i2p/aggressive.txt

# Apply throttling to recorded Destinations
15/5 file /var/i2p/aggressive.txt
```
> Než se na ni budete spoléhat, ověřte si podporu funkce záznamu ve svém sestavení. Pro zaručené chování použijte seznamy `file`.

## Pořadí vyhodnocování

Nejprve uveďte specifická pravidla, poté obecná. Běžný vzor:

1. Explicitní povolení pro důvěryhodné uzly  
2. Explicitní zákazy pro známé zneuživatele  
3. Seznamy povolení/zákazů v souborech  
4. Záznamníky pro postupné omezování rychlosti  
5. Výchozí pravidlo jako záchytné

## Kompletní příklad

```
# Moderate limits by default
30/10 default

# Always allow trusted peers
allow explicit friend1.b32.i2p
allow explicit friend2.b32.i2p

# Block known bad actors
deny file /var/i2p/blocklist.txt

# Throttle aggressive sources
15/5 file /var/i2p/throttle.txt

# Automatically populate the throttle list
60/5 record /var/i2p/throttle.txt
```
## Poznámky k implementaci

- Přístupový filtr pracuje na vrstvě tunnel, před aplikačním zpracováním, takže škodlivý provoz lze odmítnout včas.  
- Umístěte soubor filtru do konfiguračního adresáře I2PTunnel a restartujte tunnel, aby se změny projevily.  
- Sdílejte souborové seznamy napříč více tunnel, pokud chcete konzistentní zásady napříč službami.
