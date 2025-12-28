---
title: "B32 pro šifrované leaseSets"
description: "Formát adresy Base 32 pro šifrované LS2 leasesets"
slug: "b32encrypted"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
status: "Implementováno"
---

## Přehled

Standardní adresy Base 32 ("b32") obsahují hash destinace. To nebude fungovat pro šifrované LS2 (návrh 123).

Tradiční adresu Base32 nemůžeme použít pro šifrovaný LS2 (LeaseSet2; návrh 123), protože obsahuje pouze hash destinace. Neposkytuje nezaslepený veřejný klíč. Klienti musí znát veřejný klíč destinace, typ podpisu, typ zaslepeného podpisu a volitelné tajemství nebo soukromý klíč, aby bylo možné leaseset získat a dešifrovat. Samotná adresa Base32 tedy nestačí. Klient potřebuje buď úplnou destinaci (která obsahuje veřejný klíč), nebo samotný veřejný klíč. Pokud má klient úplnou destinaci v adresáři a adresář podporuje reverzní vyhledávání podle hashe, pak lze veřejný klíč získat.

Tento formát ukládá do adresy ve formátu base32 namísto hashe veřejný klíč. Tento formát musí také obsahovat typ podpisu veřejného klíče a typ podpisu schématu zaslepení.

Tento dokument specifikuje formát b32 pro tyto adresy. Ačkoli jsme se během diskusí na tento nový formát odkazovali jako na adresu "b33", skutečný nový formát si ponechává obvyklou příponu ".b32.i2p".

## Stav implementace

Návrh 123 (New netDB Entries) byl plně implementován ve verzi 0.9.43 (říjen 2019). Sada funkcí šifrovaného LS2 (nová verze leaseSet v I2P) zůstala stabilní až do verze 2.10.0 (září 2025) bez zpětně nekompatibilních změn ve formátu adresace ani v kryptografických specifikacích.

Klíčové milníky implementace: - 0.9.38: Podpora Floodfill pro standardní LS2 s offline klíči - 0.9.39: RedDSA typ podpisu 11 a základní šifrování/dešifrování - 0.9.40: Kompletní podpora adresování B32 (Návrh 149) - 0.9.41: Ověřování na bázi X25519 pro jednotlivé klienty - 0.9.42: Všechny funkce zaslepení jsou v provozu - 0.9.43: Dokončená implementace oznámena (říjen 2019)

## Návrh

- Nový formát obsahuje odslepený veřejný klíč, typ odslepeného podpisu a typ zaslepeného podpisu.
- Volitelně uvádí požadavky na secret (tajemství) a/nebo soukromý klíč pro soukromé odkazy.
- Používá stávající příponu ".b32.i2p", ale s delší délkou.
- Obsahuje kontrolní součet pro detekci chyb.
- Adresy šifrovaných leaseSet se poznají podle 56 a více zakódovaných znaků (35 a více dekódovaných bajtů), oproti 52 znakům (32 bajtům) u tradičních adres base 32.

## Specifikace

### Vytváření a kódování

Sestavte název hostitele ve tvaru {56+ chars}.b32.i2p (35+ znaků v binární podobě) následovně:

```
flag (1 byte)
  bit 0: 0 for one-byte sigtypes, 1 for two-byte sigtypes
  bit 1: 0 for no secret, 1 if secret is required
  bit 2: 0 for no per-client auth,
         1 if client private key is required
  bits 7-3: Unused, set to 0

public key sigtype (1 or 2 bytes as indicated in flags)
  If 1 byte, the upper byte is assumed zero

blinded key sigtype (1 or 2 bytes as indicated in flags)
  If 1 byte, the upper byte is assumed zero

public key
  Number of bytes as implied by sigtype
```
Následné zpracování a kontrolní součet:

```
Construct the binary data as above.
Treat checksum as little-endian.
Calculate checksum = CRC-32(data[3:end])
data[0] ^= (byte) checksum
data[1] ^= (byte) (checksum >> 8)
data[2] ^= (byte) (checksum >> 16)

hostname = Base32.encode(data) || ".b32.i2p"
```
Jakékoli nevyužité bity na konci b32 (kódování base32) musí být 0. U standardní 56znakové (35bajtové) adresy žádné nevyužité bity nejsou.

### Dekódování a ověření

```
strip the ".b32.i2p" from the hostname
data = Base32.decode(hostname)
Calculate checksum = CRC-32(data[3:end])
Treat checksum as little-endian.
flags = data[0] ^ (byte) checksum
if 1 byte sigtypes:
  pubkey sigtype = data[1] ^ (byte) (checksum >> 8)
  blinded sigtype = data[2] ^ (byte) (checksum >> 16)
else (2 byte sigtypes):
  pubkey sigtype = data[1] ^ ((byte) (checksum >> 8)) || data[2] ^ ((byte) (checksum >> 16))
  blinded sigtype = data[3] || data[4]
parse the remainder based on the flags to get the public key
```
### Bity tajného a soukromého klíče

Příznakové bity „secret“ a „private key“ se používají k indikaci klientům, proxy serverům nebo jinému klientskému kódu, že k dešifrování leaseSet bude vyžadováno tajemství a/nebo soukromý klíč. Konkrétní implementace mohou uživatele vyzvat k poskytnutí požadovaných údajů, nebo pokusy o připojení odmítnout, pokud požadované údaje chybí.

Tyto bity slouží pouze jako indikátory. Tajný ani soukromý klíč nesmí být nikdy součástí samotné B32 adresy, protože by to ohrozilo bezpečnost.

## Kryptografické podrobnosti

### Schéma zaslepení

Zaslepovací schéma používá RedDSA (varianta digitálního podpisu založená na EdDSA) vycházející z Ed25519 a návrhu ZCash, přičemž vytváří podpisy Red25519 nad křivkou Ed25519 s využitím SHA-512. Tento postup zajišťuje, že zaslepené veřejné klíče zůstávají v podgrupě s prvočíselným řádem, čímž se vyhýbá bezpečnostním rizikům, která se vyskytují v některých alternativních návrzích.

Blinded keys (zaslepené klíče) se rotují denně na základě data UTC podle vzorce:

```
blinded_key = BLIND(unblinded_key, date, optional_secret)
```
Umístění úložiště v DHT se vypočítá takto:

```
SHA256(type_byte || blinded_public_key)
```
### Šifrování

Šifrovaný leaseset používá pro šifrování proudovou šifru ChaCha20, zvolenou kvůli vyššímu výkonu na zařízeních bez hardwarové akcelerace AES. Specifikace používá HKDF pro odvozování klíčů a X25519 pro operace Diffie‑Hellman.

Šifrované leasesets mají třívrstvou strukturu: - Vnější vrstva: metadata v prostém textu - Střední vrstva: autentizace klienta (metody DH nebo PSK) - Vnitřní vrstva: vlastní data LS2 s informacemi o leasech (záznam o použitelnosti tunelu v I2P)

### Metody autentizace

Ověřování pro jednotlivé klienty podporuje dvě metody:

**Ověřování DH**: Využívá dohodu o klíči X25519. Každý autorizovaný klient poskytne serveru svůj veřejný klíč a server zašifruje prostřední vrstvu pomocí sdíleného tajemství odvozeného z ECDH.

**Ověřování pomocí PSK**: Používá předem sdílené klíče přímo k šifrování.

Příznakový bit 2 v adrese B32 určuje, zda je vyžadováno ověřování jednotlivých klientů.

## Ukládání do mezipaměti

Byť je to mimo rozsah této specifikace, routers a klienti si musí pamatovat a ukládat do mezipaměti (doporučeno trvalé uložení) mapování veřejného klíče na destinaci a naopak.

blockfile naming service (pojmenovávací služba využívající formát blockfile), výchozí systém adresářů I2P od verze 0.9.8, spravuje více adresářů s vyhrazenou mapou pro zpětné vyhledávání, která umožňuje rychlé vyhledávání podle hashe. Tato funkce je zásadní pro získání šifrovaného leaseSet, když je zpočátku znám pouze hash.

## Typy podpisů

Od verze I2P 2.10.0 jsou definovány typy podpisů 0 až 11. Jednobajtové kódování zůstává standardem, přičemž dvojbajtové kódování je k dispozici, ale v praxi se nepoužívá.

**Běžně používané typy:** - Typ 0 (DSA_SHA1): Zastaralý pro routers, podporovaný pro destinace - Typ 7 (EdDSA_SHA512_Ed25519): Současný standard pro identity routers i destinace - Typ 11 (RedDSA_SHA512_Ed25519): Výhradně pro šifrované LS2 leasesets s podporou zaslepení

**Důležité upozornění**: Pouze Ed25519 (typ 7) a Red25519 (typ 11) podporují zaslepení nezbytné pro šifrované leasesets. Jiné typy podpisů nelze s touto funkcí použít.

Typy 9-10 (algoritmy GOST) zůstávají vyhrazené, ale neimplementované. Typy 4-6 a 8 jsou označeny jako "pouze offline" pro offline podpisové klíče.

## Poznámky


## Kompatibilita verzí

Tato specifikace je přesná pro I2P verzi 0.9.47 (srpen 2020) až po verzi 2.10.0 (září 2025). Během tohoto období nedošlo k žádným nekompatibilním změnám v adresním formátu B32, šifrované struktuře LS2 ani v kryptografických implementacích. Všechny adresy vytvořené ve verzi 0.9.47 zůstávají plně kompatibilní s aktuálními verzemi.

## Reference

**CRC-32** - [CRC-32 (Wikipedie)](https://en.wikipedia.org/wiki/CRC-32) - [RFC 3309: Kontrolní součet SCTP (Stream Control Transmission Protocol)](https://tools.ietf.org/html/rfc3309)

**Specifikace I2P** - [Specifikace šifrovaného LeaseSetu](/docs/specs/encryptedleaseset/) - [Návrh 123: Nové záznamy netDB](/proposals/123-new-netdb-entries/) - [Návrh 149: B32 pro šifrovaný LS2](/proposals/149-b32-encrypted-ls2/) - [Specifikace společných struktur](/docs/specs/common-structures/) - [Pojmenovávání a adresář](/docs/overview/naming/)

**Srovnání s Torem** - [Diskusní vlákno o Toru (kontext návrhu)](https://lists.torproject.org/pipermail/tor-dev/2017-January/011816.html)

**Další zdroje** - [Projekt I2P](/) - [Fórum I2P](https://i2pforum.net) - [Dokumentace Java API](http://docs.i2p-projekt.de/javadoc/)
