---
title: "Kontrola ID dopravní sítě"
number: "147"
author: "zzz"
created: "2019-02-28"
lastupdated: "2019-08-13"
status: "Closed"
thread: "http://zzz.i2p/topics/2687"
target: "0.9.42"
implementedin: "0.9.42"
toc: true
---

## Přehled

NTCP2 (návrh 111) neodmítá spojení s různými ID sítí
ve fázi žádosti o spojení.
Spojení musí být v současné době odmítnuto ve fázi potvrzení spojení,
když Bob zkontroluje Alicein RI.

Podobně SSU neodmítá spojení s různými ID sítí
ve fázi žádosti o spojení.
Spojení musí být v současné době odmítnuto po fázi potvrzení spojení,
když Bob zkontroluje Alicein RI.

Tento návrh mění fázi žádosti o spojení obou protokolů tak,
aby zahrnoval ID sítě, způsobem kompatibilním s předchozími verzemi.


## Motivace

Spojení z nesprávné sítě by měla být odmítnuta a
kolega by měl být co nejdříve zařazen na černou listinu.


## Cíle

- Zabránit křížové kontaminaci testovacích sítí a klonovaných sítí

- Přidat ID sítě do handshake NTCP2 a SSU

- Pro NTCP2,
  přijímač (příchozí spojení) by měl být schopen rozpoznat, že ID sítě je jiné,
  aby mohl zařadit IP adresu kolegy na černou listinu.

- U SSU,
  přijímač (příchozí spojení) nemůže zařadit na černou listinu ve fázi žádosti o spojení, protože
  příchozí IP by mohla být podvržena. Stačí změnit kryptografii handshake.

- Zabránit opětovnému dosazování z nesprávné sítě

- Musí být kompatibilní s předchozími verzemi


## Ne-cíle

- NTCP 1 už se nepoužívá, takže nebude změněn.


## Návrh

Pro NTCP2,
XORování něčeho by pouze způsobilo selhání šifrování a
přijímač by neměl dostatek informací k zařazení původce na černou listinu,
takže tento přístup není preferován.

Pro SSU,
provedeme XOR s ID sítě někde v žádosti o spojení.
Jelikož toto musí být kompatibilní s předchozími verzemi, provedeme XOR s (id - 2),
takže to nebude mít žádný vliv na stávající hodnotu ID sítě, což je 2.



## Specifikace

### Dokumentace

Přidejte následující specifikaci pro platné hodnoty ID sítě:


| Použití | Číslo NetID |
|-------|--------------|
| Rezervováno | 0 |
| Rezervováno | 1 |
| Aktuální síť (výchozí) | 2 |
| Rezervované budoucí sítě | 3 - 15 |
| Klonované a testovací sítě | 16 - 254 |
| Rezervováno | 255 |


Konfigurace Java I2P ke změně výchozí hodnoty je "router.networkID=nnn".
Lepší dokumentace tohoto a povzbuzení klonů a testovacích sítí k přidání tohoto nastavení do jejich konfigurace.
Povzbudit jiné implementace k implementaci a dokumentaci této možnosti.


### NTCP2

Použijte první rezervovaný byte možností (byte 0) ve zprávě žádosti o spojení, aby obsahoval ID sítě, aktuálně 2.
Obsahuje ID sítě.
Pokud není nula, přijímač by měl zkontrolovat proti nejméně významnému bytu místního ID sítě.
Pokud se neshodují, přijímač by měl okamžitě odpojit a zařadit na černou listinu IP původce.


### SSU

Pro SSU, přidejte XOR s ((netid - 2) << 8) v HMAC-MD5 výpočtu.

Existující:

```text
HMAC-MD5(encryptedPayload + IV + (payloadLength ^ protocolVersion), macKey)

  '+' znamená přidat a '^' znamená exkluzivní neboli.
  payloadLength je 2-bajtní neznačkové celé číslo
  protocolVersion je jeden byte 0x00
```

Nové:

```text
HMAC-MD5(encryptedPayload + IV + (payloadLength ^ protocolVersion ^ ((netid - 2) << 8)), macKey)

  '+' znamená přidání, '^' znamená exkluzivní neboli, '<<' znamená posun vlevo.
  payloadLength je dvoubajtní neznačkové celé číslo, big endian
  protocolVersion je dva bajty 0x0000, big endian
  netid je dvoubajtní neznačkové celé číslo, big endian, legální hodnoty jsou 2-254
```


### Opětovné dosazování

Přidejte parametr ?netid=nnn k načítání souboru reseed su3.
Aktualizujte software pro obnovu k ověření netid. Pokud je přítomen a není roven "2",
načtení by mělo být odmítnuto s chybovým kódem, možná 403.
Přidejte konfigurační možnost do software pro obnovu, aby bylo možné konfigurovat alternativní netid pro testovací nebo klonované sítě.


## Poznámky

Nemůžeme přinutit testovací sítě a klony změnit ID sítě.
Nejlepší, co můžeme udělat, je dokumentace a komunikace.
Pokud zjistíme křížovou kontaminaci s jinými sítěmi, měli bychom se pokusit
kontaktovat vývojáře nebo operátory a vysvětlit důležitost změny ID sítě.


## Problémy



## Migrace

Toto je zpětně kompatibilní s aktuální hodnotou ID sítě 2.
Pokud někdo provozuje sítě (testovací nebo jiné) s jinou hodnotou ID sítě,
tato změna je zpětně nekompatibilní.
Nicméně, o nikom takovém nevíme.
Pokud je to jen testovací síť, není to problém, jen aktualizujte všechny routery najednou.
