---
title: "Nové záznamy netDB"
number: "123"
author: "zzz, str4d, orignal"
created: "2016-01-16"
lastupdated: "2020-07-18"
status: "Otevřít"
thread: "http://zzz.i2p/topics/2051"
supercedes: "110, 120, 121, 122"
toc: true
---

## Stav

Části tohoto návrhu jsou dokončeny a implementovány ve verzích 0.9.38 a 0.9.39.   Společné struktury, I2CP, I2NP a další specifikace   jsou nyní aktualizovány, aby odrážely změny, které jsou nyní podporovány.

Dokončené části jsou stále předmětem drobných revizí.   Další části tohoto návrhu jsou stále ve vývoji   a podléhají významným revizím.

Vyhledávání služeb (typy 9 a 11) má nízkou prioritu,   není naplánováno a může být přesunuto do samostatného návrhu.

## Přehled

Toto je aktualizace a agregace následujících 4 návrhů:

- 110 LS2
- 120 Meta LS2 pro masivní multihoming
- 121 Šifrovaný LS2
- 122 Neověřené vyhledávání služeb (anycasting)

Tyto návrhy jsou většinou nezávislé, ale pro přehlednost definujeme a používáme   společný formát pro několik z nich.

Následující návrhy jsou nějakým způsobem související:

- 140 Neviditelný multihoming (nekompatibilní s tímto návrhem)
- 142 Nová šablona kryptografie (pro novou symetrickou kryptografii)
- 144 ECIES-X25519-AEAD-Ratchet
- 145 ECIES-P256
- 146 Red25519
- 148 EdDSA-BLAKE2b-Ed25519
- 149 B32 pro Šifrovaný LS2
- 150 Protokol Garlic Farm
- 151 ECDSA Blinding

## Návrh

Tento návrh definuje 5 nových typů DatabaseEntry a proces pro   jejich ukládání do a načítání z databáze sítě,   stejně jako metodu pro jejich podepisování a ověřování těchto podpisů.

### Cíle

- Zpětná kompatibilita
- LS2 použitelný se starším stylem multihomingu
- Pro podporu nejsou vyžadovány nové kryptografické algoritmy ani primitiva
- Zachování oddělení kryptografie a podepisování; podpora všech současných a budoucích verzí
- Povolení volitelných offline podepisovacích klíčů
- Snížení přesnosti časových razítek za účelem snížení možnosti fingerprintingu
- Povolení nové kryptografie pro cíle
- Povolení masivního multihomingu
- Oprava více problémů s existujícím šifrovaným LS
- Volitelné skrývání za účelem snížení viditelnosti pro floodfill uzly
- Šifrování podporuje jak jediný klíč, tak více odvolatelných klíčů
- Vyhledávání služeb pro snadnější vyhledávání outproxy, bootstrap aplikace DHT,  
  a další použití
- Neporušovat nic, co závisí na 32bitových binárních hashích cílů, např. bittorrent
- Přidání flexibility do leasesetů prostřednictvím vlastností, jako máme u routerinfos.
- Umístění časového razítka publikování a proměnné expirace do hlavičky, aby to fungovalo i  
  v případě, že obsah je šifrovaný (nepočítat časové razítko z nejstaršího lease)
- Všechny nové typy žijí ve stejném DHT prostoru a stejných umístěních jako stávající leasesety,  
  takže uživatelé mohou migrovat ze starého LS na LS2,  
  nebo přepínat mezi LS2, Meta a Šifrovaným,  
  aniž by měnili Cíl nebo hash.
- Stávající Cíl může být převeden na použití offline klíčů,  
  nebo zpět na online klíče, aniž by se měnil Cíl nebo hash.

### Není cílem / Mimo rozsah

- Nový algoritmus rotace DHT nebo generování sdíleného náhodného čísla
- Konkrétní nový typ šifrování a end-to-end šifrovací schéma  
  pro použití tohoto nového typu by bylo v samostatném návrhu.  
  Žádná nová kryptografie není zde specifikována ani diskutována.
- Nové šifrování pro RIs nebo stavbu tunelů.  
  To by bylo v samostatném návrhu.
- Metody šifrování, přenosu a příjmu zpráv I2NP DLM / DSM / DSRM.  
  Nebudou měněny.
- Jak generovat a podporovat Meta, včetně komunikace mezi backendovými směrovači, správy, převzetí a koordinace.  
  Podpora může být přidána do I2CP, nebo i2pcontrol, nebo nového protokolu.  
  To může být nebo nemusí být standardizováno.
- Jak skutečně implementovat a spravovat delší expirující tunely, nebo zrušit stávající tunely.  
  To je extrémně obtížné a bez toho nemůžete mít rozumné postupné vypnutí.
- Změny modelu hrozeb
- Formát offline úložiště, nebo metody pro ukládání/načítání/sdílení dat.
- Podrobnosti implementace nejsou zde diskutovány a jsou ponechány na každém projektu.

### Odůvodnění

LS2 přidává pole pro změnu typu šifrování a pro budoucí změny protokolu.

Šifrovaný LS2 opravuje několik bezpečnostních problémů stávajícího šifrovaného LS tím,   že používá asymetrické šifrování celé sady lease.

Meta LS2 poskytuje flexibilní, efektivní, účinné a škálovatelné řešení multihomingu.

Záznam služby a Seznam služeb poskytují anycast služby jako vyhledávání jmen   a bootstrapování DHT.

### Typy dat NetDB

Čísla typů jsou použita ve zprávách I2NP Database Lookup/Store.

Sloupec end-to-end označuje, zda jsou dotazy/odpovědi odesílány do Cíle ve zprávě Garlic.

Stávající typy:

| NetDB Data | Typ vyhledávání | Typ ukládání |
|------------|-------------|------------|
| jakýkoli        | 0           | jakýkoli        |
| LS         | 1           | 1          |
| RI         | 2           | 0          |
| exploratory| 3           | DSRM       |
Nové typy:

| NetDB Data     | Typ vyhledávání | Typ ukládání | Standardní hlavička LS2? | Odesíláno end-to-end? |
|----------------|-------------|------------|------------------|------------------|
| LS2            | 1           | 3          | ano              | ano              |
| Šifrovaný LS2  | 1           | 5          | ne               | ne               |
| Meta LS2       | 1           | 7          | ano              | ne               |
| Záznam služby | n/a         | 9          | ano              | ne               |
| Seznam služeb   | 4           | 11         | ne               | ne               |
### Poznámky

- Typy vyhledávání jsou aktuálně bity 3-2 ve zprávě Database Lookup.  
  Jakékoli další typy by vyžadovaly použití bitu 4.

- Všechny typy ukládání jsou liché, protože horní bity ve zprávě Database Store  
  jsou staršími směrovači ignorovány.  
  Raději bychom chtěli, aby se analýza nezdařila jako LS než jako komprimovaný RI.

- Měl by být typ explicitní, implicitní nebo ani jedno v datech pokrytých podpisem?

### Proces vyhledávání/ukládání

Typy 3, 5 a 7 mohou být vráceny jako odpověď na standardní vyhledávání leasesetu (typ 1).   Typ 9 nikdy není vrácen jako odpověď na vyhledávání.   Typ 11 je vrácen jako odpověď na nový typ vyhledávání služby (typ 11).

Pouze typ 3 může být odeslán ve zprávě Garlic mezi klienty.

### Formát

Typy 3, 7 a 9 mají společný formát::

```text
Standard LS2 Header
- as defined below

Type-Specific Part
- as defined below in each part

Standard LS2 Signature:
- Length as implied by sig type of signing key
```
Standardní hlavička LS2

Část specifická pro typ

### Úvahy o soukromí/bezpečnosti

Standardní podpis LS2:

## Standardní hlavička LS2

Typ 5 (Šifrovaný) nezačíná Cílem a má   jiný formát. Viz níže.

### Formát

```
Standard LS2 Header:
  - Type (1 byte)
    Not actually in header, but part of data covered by signature.
    Take from field in Database Store Message.
  - Destination (387+ bytes)
  - Published timestamp (4 bytes, big endian, seconds since epoch, rolls over in 2106)
  - Expires (2 bytes, big endian) (offset from published timestamp in seconds, 18.2 hours max)
  - Flags (2 bytes)
    Bit order: 15 14 ... 3 2 1 0
    Bit 0: If 0, no offline keys; if 1, offline keys
    Bit 1: If 0, a standard published leaseset.
           If 1, an unpublished leaseset. Should not be flooded, published, or
           sent in response to a query. If this leaseset expires, do not query the
           netdb for a new one, unless bit 2 is set.
    Bit 2: If 0, a standard published leaseset.
           If 1, this unencrypted leaseset will be blinded and encrypted when published.
           If this leaseset expires, query the blinded location in the netdb for a new one.
           If this bit is set to 1, set bit 1 to 1 also.
           As of release 0.9.42.
    Bits 3-15: set to 0 for compatibility with future uses
  - If flag indicates offline keys, the offline signature section:
    Expires timestamp (4 bytes, big endian, seconds since epoch, rolls over in 2106)
    Transient sig type (2 bytes, big endian)
    Transient signing public key (length as implied by sig type)
    Signature of expires timestamp, transient sig type, and public key,
    by the destination public key,
    length as implied by destination public key sig type.
    This section can, and should, be generated offline.
```
### Odůvodnění

  - jak je definováno níže

  - jak je definováno níže pro každou část

  - Délka podle typu podpisu podepisovacího klíče

- Nepublikovaný/publikovaný: Pro použití při odesílání databáze uložit end-to-end,
  odesílající směrovač může chtít označit, že tento leaseset by neměl být
  odesílán ostatním. Aktuálně používáme heuristiku k udržování tohoto stavu.

### Problémy

- Publikovaný: Nahrazuje složitou logiku potřebnou k určení 'verze' leasesetu.
  Aktuálně je verzí expirace posledního expirujícího lease,
  a směrovač publikující leaseset, který pouze odstraňuje starší lease, musí tuto expiraci zvýšit alespoň o 1ms.

- Expire: Umožňuje, aby expirace záznamu v netdb byla dřívější než expirace
  jeho posledního leasesetu. Možná nebude užitečný pro LS2, kde se očekává, že leasesety
  budou mít maximální expiraci 11 minut, ale
  pro jiné nové typy je to nezbytné (viz Meta LS a Záznam služby níže).

- Offline klíče jsou volitelné, aby se snížila počáteční/požadovaná složitost implementace.

### Poznámky

- Můžeme snížit přesnost časového razítka ještě více (10 minut?), ale museli bychom přidat
  číslo verze. To by mohlo porušit multihoming, pokud nemáme šifrování zachovávající pořadí?
  Pravděpodobně nemůžeme bez časových razítek vůbec.

- Alternativa: 3 bajtové časové razítko (epocha / 10 minut), 1-bajtová verze, 2-bajtové expirace

- Je typ explicitní nebo implicitní v datech / podpisu? "Doménové" konstanty pro podpis?

## Nové typy DatabaseEntry

### LeaseSet 2

Typ 11 (Seznam služeb) je agregací několika Záznamů služeb a má   jiný formát. Viz níže.

- Směrovače by neměly publikovat LS více než jednou za sekundu.
  Pokud ano, musí uměle zvýšit časové razítko publikování o 1
  oproti dříve publikovanému LS.

TBD

    Standard LS flag (1)
Typy 3, 7 a 9 používají standardní hlavičku LS2, specifikovanou níže:

    Standard LS2 type (3)
Změny oproti stávajícímu LeaseSet:

    Hash of destination
    This hash is then used to generate the daily "routing key", as in LS1
Vyhledávání s

    10 minutes, as in a regular LS.
Ukládání s

    Destination

### Formát

```
Standard LS2 Header as specified above

  Standard LS2 Type-Specific Part
  - Properties (Mapping as specified in common structures spec, 2 zero bytes if none)
  - Number of key sections to follow (1 byte, max TBD)
  - Key sections:
    - Encryption type (2 bytes, big endian)
    - Encryption key length (2 bytes, big endian)
      This is explicit, so floodfills can parse LS2 with unknown encryption types.
    - Encryption key (number of bytes specified)
  - Number of lease2s (1 byte)
  - Lease2s (40 bytes each)
    These are leases, but with a 4-byte instead of an 8-byte expiration,
    seconds since the epoch (rolls over in 2106)

  Standard LS2 Signature:
  - Signature
    If flag indicates offline keys, this is signed by the transient pubkey,
    otherwise, by the destination pubkey
    Length as implied by sig type of signing key
    The signature is of everything above.
```
### Odůvodnění

- Implementace směrovačů by mohly ukládat přechodné klíče a podpis do mezipaměti, aby
  se vyhnuly ověřování pokaždé. Zejména floodfill uzly a směrovače na
  obou koncích dlouhodobých spojení by mohly z toho těžit.

- Offline klíče a podpis jsou vhodné pouze pro dlouhodobé cíle,
  tj. servery, ne klienty.

### Diskuze

Ukládání na

Typická expirace

Publikováno

- Přidání časového razítka publikování, časového razítka expirace, příznaků a vlastností
- Přidání typu šifrování
- Odstranění klíče pro odvolání

Tento návrh nadále používá veřejný klíč v leasesetu pro end-to-end šifrovací klíč a ponechává pole veřejného klíče v Cíli nevyužité, jak je to nyní. Typ šifrování není specifikován v certifikátu klíče Cíle, zůstane 0.

- Vlastnosti: Budoucí rozšiřitelnost a flexibilita.
  Umístěny na začátek pro případ, že jsou potřeba pro analýzu zbývajících dat.

### Nové problémy šifrování

Zamítnutá alternativa je specifikovat typ šifrování v certifikátu klíče Cíle, použít veřejný klíč v Cíli a nepoužívat veřejný klíč v leasesetu. Toto neplánujeme dělat.

- Více párů typ šifrování/veřejný klíč jsou
  pro usnadnění přechodu na nové typy šifrování. Jiná možnost je
  publikovat více leasesetů, možná pomocí stejných tunelů,
  jak to děláme nyní pro DSA a EdDSA cíle.
  Identifikace příchozího typu šifrování na tunelu
  může být provedena pomocí stávajícího mechanismu značky relace,
  a/nebo zkoušením dešifrování pomocí každého klíče. Délky příchozích
  zpráv mohou také poskytnout nápovědu.

- Umístění skutečného veřejného klíče se nemění.
- Typ šifrování nebo veřejný klíč se může změnit bez změny Cíle.
- Odstraňuje nepoužívané pole pro odvolání
- Základní kompatibilita s jinými typy DatabaseEntry v tomto návrhu
- Umožňuje více typů šifrování

- Umístění veřejného klíče a typu šifrování se liší od RouterInfo
- Zachovává nepoužívaný veřejný klíč v leasesetu
- Vyžaduje implementaci napříč sítí; v alternativě mohou být použity experimentální
  typy šifrování, pokud jsou povoleny floodfill uzly
  (ale viz související návrhy 136 a 137 o podpoře experimentálních typů podpisů).
  Alternativní návrh by mohl být jednodušší na implementaci a testování pro experimentální typy šifrování.

### Poznámky

- Typ šifrování představuje kombinaci
  křivky, délky klíče a end-to-end schématu,
  včetně KDF a MAC, pokud existují.

- Zahrnuli jsme pole délky klíče, aby LS2 byl
  analyzovatelný a ověřitelný floodfillem i pro neznámé typy šifrování.

- První nový typ šifrování, který bude navržen,
  bude pravděpodobně ECIES/X25519. Jak se používá end-to-end
  (buď mírně upravená verze ElGamal/AES+SessionTag
  nebo něco úplně nového, např. ChaCha/Poly) bude specifikováno
  v jednom nebo více samostatných návrzích.
  Viz také návrhy ECIES 144 a 145.

### Šifrovaný LS2

Výhody LS2:

- 8-bajtová expirace v lease byla změněna na 4 bajty.

Nevýhody LS2:

Některé z toho je mimo rozsah tohoto návrhu, ale zatím zde zanecháváme poznámky, protože nemáme zatím samostatný návrh na šifrování. Viz také návrhy ECIES 144 a 145.

- Pokud bychom kdy implementovali odvolání, mohli bychom to udělat s polem expirace na nule,
  nebo nulovými lease, nebo obojím. Není potřeba samostatný klíč pro odvolání.

Cíle:

    Standard LS flag (1)
Šifrovaný LS2 nikdy není odesílán ve zprávě Garlic end-to-end. Použijte standardní LS2 výše.

    Encrypted LS2 type (5)
Změny oproti stávajícímu šifrovanému LeaseSet:

    Hash of blinded sig type and blinded public key
    Two byte sig type (big endian, e.g. 0x000b) || blinded public key
    This hash is then used to generate the daily "routing key", as in LS1
Vyhledávání s

    10 minutes, as in a regular LS, or hours, as in a meta LS.
Ukládání s

    Destination


### Definice

Ukládání na

Typická expirace

    n-byte output from a cryptographically-secure random number generator.

    In addition to the requirement of CSRNG being cryptographically-secure (and thus
    suitable for generating key material), it MUST be safe
    for some n-byte output to be used for key material when the byte sequences immediately
    preceding and following it are exposed on the network (such as in a salt, or encrypted
    padding). Implementations that rely on a potentially-untrustworthy source should hash
    any output that is to be exposed on the network. See [PRNG references](http://projectbullrun.org/dual-ec/ext-rand.html) and [Tor dev discussion](https://lists.torproject.org/pipermail/tor-dev/2015-November/009954.html).

Publikováno

    SHA-256 hash function that takes a personalization string p and data d, and
    produces an output of length 32 bytes.

    Use SHA-256 as follows::

        H(p, d) := SHA-256(p || d)

Definujeme následující funkce odpovídající kryptografickým stavebním blokům použitým pro šifrovaný LS2:

    The ChaCha20 stream cipher as specified in [RFC 7539 Section 2.4](https://tools.ietf.org/html/rfc7539#section-2.4), with the initial counter
    set to 1. S_KEY_LEN = 32 and S_IV_LEN = 12.

    ENCRYPT(k, iv, plaintext)
        Encrypts plaintext using the cipher key k, and nonce iv which MUST be unique for
        the key k. Returns a ciphertext that is the same size as the plaintext.

        The entire ciphertext must be indistinguishable from random if the key is secret.

    DECRYPT(k, iv, ciphertext)
        Decrypts ciphertext using the cipher key k, and nonce iv. Returns the plaintext.


CSRNG(n)

    The RedDSA signature scheme (corresponding to SigType 11) with key blinding.
    It has the following functions:

    DERIVE_PUBLIC(privkey)
        Returns the public key corresponding to the given private key.

    SIGN(privkey, m)
        Returns a signature by the private key privkey over the given message m.

    VERIFY(pubkey, m, sig)
        Verifies the signature sig against the public key pubkey and message m. Returns
        true if the signature is valid, false otherwise.

    It must also support the following key blinding operations:

    GENERATE_ALPHA(data, secret)
        Generate alpha for those who know the data and an optional secret.
        The result must be identically distributed as the private keys.

    BLIND_PRIVKEY(privkey, alpha)
        Blinds a private key, using a secret alpha.

    BLIND_PUBKEY(pubkey, alpha)
        Blinds a public key, using a secret alpha.
        For a given keypair (privkey, pubkey) the following relationship holds::

            BLIND_PUBKEY(pubkey, alpha) ==
            DERIVE_PUBLIC(BLIND_PRIVKEY(privkey, alpha))

H(p, d)

    X25519 public key agreement system. Private keys of 32 bytes, public keys of 32
    bytes, produces outputs of 32 bytes. It has the following
    functions:

    GENERATE_PRIVATE()
        Generates a new private key.

    DERIVE_PUBLIC(privkey)
        Returns the public key corresponding to the given private key.

    DH(privkey, pubkey)
        Generates a shared secret from the given private and public keys.

STREAM

    A cryptographic key derivation function which takes some input key material ikm (which
    should have good entropy but is not required to be a uniformly random string), a salt
    of length 32 bytes, and a context-specific 'info' value, and produces an output
    of n bytes suitable for use as key material.

    Use HKDF as specified in [RFC 5869](https://tools.ietf.org/html/rfc5869), using the HMAC hash function SHA-256
    as specified in [RFC 2104](https://tools.ietf.org/html/rfc2104). This means that SALT_LEN is 32 bytes max.


### Formát

SIG

- Šifrovací klíče jsou v pořadí podle preference serveru, nejpreferovanější první.
  Výchozí chování klienta je vybrat první klíč s
  podporovaným typem šifrování. Klienti mohou používat jiné algoritmy výběru
  na základě podpory šifrování, relativního výkonu a dalších faktorů.

DH

    Layer 0 data + Enc(layer 1 data + Enc(layer 2 data)) + Signature

HKDF(salt, ikm, info, n)

Formát šifrovaného LS2 se skládá ze tří vnořených vrstev:

#### Vrstva 0 (vnější)

Celkový formát vypadá takto::

    1 byte

    Not actually in header, but part of data covered by signature.
    Take from field in Database Store Message.

Všimněte si, že šifrovaný LS2 je zaslepený. Cíl není v hlavičce. Umístění úložiště DHT je SHA-256(typ podpisu || zaslepený veřejný klíč) a rotuje se denně.

    2 bytes, big endian
    This will always be type 11, identifying a Red25519 blinded key.

Nepoužívá standardní hlavičku LS2 specifikovanou výše.

    Length as implied by sig type

Typ

    4 bytes, big endian

    Seconds since epoch, rolls over in 2106

Typ zaslepeného veřejného klíče

    2 bytes, big endian

    Offset from published timestamp in seconds, 18.2 hours max

Zaslepený veřejný klíč

    2 bytes

    Bit order: 15 14 ... 3 2 1 0

    Bit 0: If 0, no offline keys; if 1, offline keys

    Other bits: set to 0 for compatibility with future uses

Časové razítko publikování

    Present if flag indicates offline keys

    Expires timestamp
        4 bytes, big endian

        Seconds since epoch, rolls over in 2106

    Transient sig type
        2 bytes, big endian

    Transient signing public key
        Length as implied by sig type

    Signature
        Length as implied by blinded public key sig type

        Over expires timestamp, transient sig type, and transient public key.

        Verified with the blinded public key.

Expire

    2 bytes, big endian

Příznaky

    lenOuterCiphertext bytes

    Encrypted layer 1 data. See below for key derivation and encryption algorithms.

Data přechodného klíče

    Length as implied by sig type of the signing key used

    The signature is of everything above.

    If the flag indicates offline keys, the signature is verified with the transient
    public key. Otherwise, the signature is verified with the blinded public key.


#### Vrstva 1 (střední)

lenOuterCiphertext

    1 byte
    
    Bit order: 76543210

    Bit 0: 0 for everybody, 1 for per-client, auth section to follow

    Bits 3-1: Authentication scheme, only if bit 0 is set to 1 for per-client, otherwise 000
              000: DH client authentication (or no per-client authentication)
              001: PSK client authentication

    Bits 7-4: Unused, set to 0 for future compatibility

outerCiphertext

    Present if flag bit 0 is set to 1 and flag bits 3-1 are set to 000.

    ephemeralPublicKey
        32 bytes

    clients
        2 bytes, big endian

        Number of authClient entries to follow, 40 bytes each

    authClient
        Authorization data for a single client.
        See below for the per-client authorization algorithm.

        clientID_i
            8 bytes

        clientCookie_i
            32 bytes

Podpis

    Present if flag bit 0 is set to 1 and flag bits 3-1 are set to 001.

    authSalt
        32 bytes

    clients
        2 bytes, big endian

        Number of authClient entries to follow, 40 bytes each

    authClient
        Authorization data for a single client.
        See below for the per-client authorization algorithm.

        clientID_i
            8 bytes

        clientCookie_i
            32 bytes


Příznaky

    Length implied by lenOuterCiphertext (whatever data remains)

    Encrypted layer 2 data. See below for key derivation and encryption algorithms.


#### Vrstva 2 (vnitřní)

Data ověření klienta DH

    1 byte

    Either 3 (LS2) or 7 (Meta LS2)

Data ověření klienta PSK

    LeaseSet2 data for the given type.

    Includes the header and signature.


### Odvození klíče zaslepení

innerCiphertext

Typ

#### Cíle

- Přidání zaslepení
- Povolení více typů podpisů
- Nevyžadovat žádné nové kryptografické primitivy
- Volitelně šifrovat každému příjemci, odvolatelné
- Podpora šifrování Standardního LS2 a Meta LS2 pouze

#### Bezpečnost

Data

#### Definice

Používáme následující schéma pro zaslepení klíče, založené na Ed25519 a [ZCash RedDSA](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf). Podpisy Re25519 jsou nad křivkou Ed25519, pomocí SHA-512 pro hash.

    The Ed25519 base point (generator) 2^255 - 19 as in [Ed25519](http://cr.yp.to/papers.html#ed25519)

Nepoužíváme [Tor's rend-spec-v3.txt appendix A.2](https://spec.torproject.org/rend-spec-v3), který má podobné cíle návrhu, protože jeho zaslepené veřejné klíče mohou být mimo prvočíselnou podskupinu, s neznámými bezpečnostními důsledky.

    The Ed25519 order 2^252 + 27742317777372353535851937790883648493
    as in [Ed25519](http://cr.yp.to/papers.html#ed25519)

Bezpečnost schématu zaslepení vyžaduje, aby distribuce alfa byla stejná jako u nezaslepených soukromých klíčů. Avšak když zaslepíme soukromý klíč Ed25519 (typ podpisu 7) na soukromý klíč Red25519 (typ podpisu 11), distribuce je jiná. Pro splnění požadavků [zcash section 4.1.6.1](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf), měl by být pro nezaslepené klíče použit také Red25519 (typ podpisu 11), aby "kombinace znovu náhodně generovaného veřejného klíče a podpisů pod tímto klíčem neodhalila klíč, ze kterého byl znovu náhodně generován." Umožňujeme typ 7 pro stávající cíle, ale doporučujeme typ 11 pro nové cíle, které budou šifrované.

    Convert a private key to public, as in Ed25519 (mulitply by G)

B

    A 32-byte random number known to those who know the destination.

L

    Generate alpha for the current date, for those who know the destination and the secret.
    The result must be identically distributed as Ed25519 private keys.

DERIVE_PUBLIC(a)

    The unblinded 32-byte EdDSA or RedDSA signing private key used to sign the destination

alpha

    The unblinded 32-byte EdDSA or RedDSA signing public key in the destination,
    = DERIVE_PUBLIC(a), as in Ed25519

GENERATE_ALPHA(destination, date, secret)

    The blinded 32-byte EdDSA signing private key used to sign the encrypted leaseset
    This is a valid EdDSA private key.

a

    The blinded 32-byte EdDSA signing public key in the Destination,
    may be generated with DERIVE_PUBLIC(a'), or from A and alpha.
    This is a valid EdDSA public key, on the curve and on the prime-order subgroup.

A

    Flip the order of the input bytes to little-endian

a'

    32 bytes = (LEOS2IP(SHA512(x))) mod B, same as in Ed25519 hash-and-reduce


#### Výpočty zaslepení

A'

LEOS2IP(x)

```text
// GENERATE_ALPHA(destination, date, secret)

  // secret is optional, else zero-length
  A = destination's signing public key
  stA = signature type of A, 2 bytes big endian (0x0007 or 0x000b)
  stA' = signature type of blinded public key A', 2 bytes big endian (0x000b)
  keydata = A || stA || stA'
  datestring = 8 bytes ASCII YYYYMMDD from the current date UTC
  secret = UTF-8 encoded string
  seed = HKDF(H("I2PGenerateAlpha", keydata), datestring || secret, "i2pblinding1", 64)
  // treat seed as a 64 byte little-endian value
  alpha = seed mod L
```
H*(x)

```text
// BLIND_PRIVKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  // If for a Ed25519 private key (type 7)
  seed = destination's signing private key
  a = left half of SHA512(seed) and clamped as usual for Ed25519
  // else, for a Red25519 private key (type 11)
  a = destination's signing private key
  // Addition using scalar arithmentic
  blinded signing private key = a' = BLIND_PRIVKEY(a, alpha) = (a + alpha) mod L
  blinded signing public key = A' = DERIVE_PUBLIC(a')
```
Nové tajemství alfa a zaslepené klíče musí být generovány každý den (UTC). Tajemství alfa a zaslepené klíče jsou vypočítány následovně.

```text
// BLIND_PUBKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  A = destination's signing public key
  // Addition using group elements (points on the curve)
  blinded public key = A' = BLIND_PUBKEY(A, alpha) = A + DERIVE_PUBLIC(alpha)
```
GENERATE_ALPHA(destination, date, secret), pro všechny strany:

#### Podepisování

BLIND_PRIVKEY(), pro vlastníka publikujícího leaseset:

BLIND_PUBKEY(), pro klienty načítající leaseset:

Obě metody výpočtu A' dávají stejný výsledek, jak je vyžadováno.

Nezaslepený leaseset je podepsán nezaslepeným soukromým klíčem pro podepisování Ed25519 nebo Red25519 a ověřen pomocí nezaslepeného veřejného klíče pro podepisování Ed25519 nebo Red25519 (typy podpisu 7 nebo 11) jako obvykle.

#### Výpočty podepisování/ověřování

Pokud je veřejný klíč pro podepisování offline, je nezaslepený leaseset podepsán nezaslepeným přechodným soukromým klíčem pro podepisování Ed25519 nebo Red25519 a ověřen pomocí nezaslepeného veřejného klíče pro podepisování Ed25519 nebo Red25519 (typy podpisu 7 nebo 11) jako obvykle. Viz níže pro další poznámky k offline klíčům pro šifrované leasesety.

Pro podepisování šifrovaného leasesetu používáme Red25519, založené na [RedDSA](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf) k podepisování a ověřování pomocí zaslepených klíčů. Podpisy Red25519 jsou nad křivkou Ed25519, pomocí SHA-512 pro hash.

Red25519 je identické se standardním Ed25519 s výjimkou níže uvedeného.

Vnější část šifrovaného leasesetu používá klíče a podpisy Red25519.

Red25519 je téměř identické s Ed25519. Jsou dvě rozdíly:

```text
T = 80 random bytes
  r = H*(T || publickey || message)
  // rest is the same as in Ed25519
```
Soukromé klíče Red25519 jsou generovány z náhodných čísel a pak musí být redukovány mod L, kde L je definováno výše. Soukromé klíče Ed25519 jsou generovány z náhodných čísel a pak "upraveny" pomocí bitové masky na bajty 0 a 31. To se u Red25519 nedělá. Funkce GENERATE_ALPHA() a BLIND_PRIVKEY() definované výše generují správné soukromé klíče Red25519 pomocí mod L.

```text
// same as in Ed25519
```
### Šifrování a zpracování

#### Odvození podpověření

V Red25519 se výpočet r pro podepisování používá další náhodná data, a používá hodnotu veřejného klíče místo hashu soukromého klíče. Kvůli náhodným datům je každý podpis Red25519 jiný, i když podepisuje stejná data stejným klíčem.

```text
A = destination's signing public key
  stA = signature type of A, 2 bytes big endian (0x0007 or 0x000b)
  stA' = signature type of A', 2 bytes big endian (0x000b)
  keydata = A || stA || stA'
  credential = H("credential", keydata)
```
Podepisování:

Ověřování:

```text
subcredential = H("subcredential", credential || blindedPublicKey)
```
Jako součást procesu zaslepení musíme zajistit, že šifrovaný LS2 může být dešifrován pouze někým, kdo zná odpovídající veřejný klíč pro podepisování Cíle. Plný Cíl není vyžadován. Pro dosažení tohoto cíle odvozujeme pověření z veřejného klíče pro podepisování:

#### Šifrování vrstvy 1

Osobní řetězec zajišťuje, že pověření se nesrazí s žádným hashem použitým jako klíč vyhledávání DHT, jako je prostý hash Cíle.

```text
outerInput = subcredential || publishedTimestamp
```
Pro daný zaslepený klíč pak můžeme odvodit podpověření:

```text
outerSalt = CSRNG(32)
```
Podpověření je zahrnuto do procesů odvození klíčů níže, což váže tyto klíče ke znalosti veřejného klíče pro podepisování Cíle.

```text
keys = HKDF(outerSalt, outerInput, "ELS2_L1K", 44)
  outerKey = keys[0:31]
  outerIV = keys[32:43]
```
Nejprve je připraven vstup do procesu odvození klíče:

```text
outerCiphertext = outerSalt || ENCRYPT(outerKey, outerIV, outerPlaintext)
```
#### Dešifrování vrstvy 1

Dále je generována náhodná sůl:

```text
outerSalt = outerCiphertext[0:31]
```
Poté je odvozen klíč použitý k zašifrování vrstvy 1:

```text
outerInput = subcredential || publishedTimestamp
  keys = HKDF(outerSalt, outerInput, "ELS2_L1K", 44)
  outerKey = keys[0:31]
  outerIV = keys[32:43]
```
Nakonec je prostý text vrstvy 1 zašifrován a serializován:

```text
outerPlaintext = DECRYPT(outerKey, outerIV, outerCiphertext[32:end])
```
#### Šifrování vrstvy 2

Sůl je analyzována z šifrového textu vrstvy 1:

Poté je odvozen klíč použitý k zašifrování vrstvy 1:

```text
innerInput = authCookie || subcredential || publishedTimestamp
  innerSalt = CSRNG(32)
  keys = HKDF(innerSalt, innerInput, "ELS2_L2K", 44)
  innerKey = keys[0:31]
  innerIV = keys[32:43]
  innerCiphertext = innerSalt || ENCRYPT(innerKey, innerIV, innerPlaintext)
```
#### Dešifrování vrstvy 2

Nakonec je šifrový text vrstvy 1 dešifrován:

Když je povoleno ověřování klienta, ``authCookie`` je vypočítáno jak je popsáno níže. Když je ověřování klienta zakázáno, ``authCookie`` je prázdné pole bajtů.

```text
innerInput = authCookie || subcredential || publishedTimestamp
  innerSalt = innerCiphertext[0:31]
  keys = HKDF(innerSalt, innerInput, "ELS2_L2K", 44)
  innerKey = keys[0:31]
  innerIV = keys[32:43]
  innerPlaintext = DECRYPT(innerKey, innerIV, innerCiphertext[32:end])
```
### Autorizace pro konkrétního klienta

Šifrování pokračuje podobně jako u vrstvy 1:

Když je povoleno ověřování klienta, ``authCookie`` je vypočítáno jak je popsáno níže. Když je ověřování klienta zakázáno, ``authCookie`` je prázdné pole bajtů.

#### Autorizace klienta DH

Dešifrování pokračuje podobně jako u vrstvy 1:

Když je pro Cíl povolena autorizace klienta, server udržuje seznam klientů, které opravňuje k dešifrování dat šifrovaného LS2. Data uložená pro každého klienta závisí na mechanismu autorizace a zahrnují nějaký druh materiálu klíče, který každý klient generuje a posílá serveru prostřednictvím bezpečného out-of-band mechanismu.

```text
authCookie = CSRNG(32)
  esk = GENERATE_PRIVATE()
  epk = DERIVE_PUBLIC(esk)
```
Existují dvě alternativy pro implementaci autorizace pro konkrétního klienta:

```text
sharedSecret = DH(esk, cpk_i)
  authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
  okm = HKDF(epk, authInput, "ELS2_XCA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
  clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
```
Každý klient generuje pár klíčů DH ``[csk_i, cpk_i]`` a pošle veřejný klíč ``cpk_i`` serveru.

Zpracování serveru ^^^^^^^^^^^^^^^^^ Server generuje nové ``authCookie`` a dočasný pár klíčů DH:

```text
sharedSecret = DH(csk_i, epk)
  authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
  okm = HKDF(epk, authInput, "ELS2_XCA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
```
Pak pro každého oprávněného klienta server zašifruje ``authCookie`` na jeho veřejný klíč:

```text
authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie_i)
```
#### Autorizace klienta s předem sdíleným klíčem

Server umístí každou dvojici ``[clientID_i, clientCookie_i]`` do vrstvy 1 šifrovaného LS2, spolu s ``epk``.

Zpracování klienta ^^^^^^^^^^^^^^^^^ Klient použije svůj soukromý klíč k odvození očekávaného identifikátoru klienta ``clientID_i``, šifrovacího klíče ``clientKey_i`` a IV šifrování ``clientIV_i``:

```text
authCookie = CSRNG(32)
  authSalt = CSRNG(32)
```
Pak klient vyhledá v datech autorizace vrstvy 1 položku obsahující ``clientID_i``. Pokud existuje shodná položka, klient ji dešifruje a získá ``authCookie``:

```text
authInput = psk_i || subcredential || publishedTimestamp
  okm = HKDF(authSalt, authInput, "ELS2PSKA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
  clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
```
Každý klient generuje tajný 32bajtový klíč ``psk_i`` a pošle ho serveru. Alternativně může server vygenerovat tajný klíč a poslat ho jednomu nebo více klientům.

Zpracování serveru ^^^^^^^^^^^^^^^^^ Server generuje nové ``authCookie`` a sůl:

```text
authInput = psk_i || subcredential || publishedTimestamp
  okm = HKDF(authSalt, authInput, "ELS2PSKA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
```
Pak pro každého oprávněného klienta server zašifruje ``authCookie`` na jeho předem sdílený klíč:

```text
authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie_i)
```
#### Bezpečnostní úvahy

Server umístí každou dvojici ``[clientID_i, clientCookie_i]`` do vrstvy 1 šifrovaného LS2, spolu s ``authSalt``.

Zpracování klienta ^^^^^^^^^^^^^^^^^ Klient použije svůj předem sdílený klíč k odvození očekávaného identifikátoru klienta ``clientID_i``, šifrovacího klíče ``clientKey_i`` a IV šifrování ``clientIV_i``:

Pak klient vyhledá v datech autorizace vrstvy 1 položku obsahující ``clientID_i``. Pokud existuje shodná položka, klient ji dešifruje a získá ``authCookie``:

Oba výše uvedené mechanismy autorizace klienta poskytují soukromí pro členství klientů. Entita, která zná pouze Cíl, může vidět, kolik klientů je přihlášeno v daném okamžiku, ale nemůže sledovat, kteří klienti jsou přidáváni nebo odvoláváni.

- Šifrovat celou věc pro zabezpečení
- Bezpečně šifrovat, ne jen pomocí AES.
- Šifrovat každému příjemci

Servery by měly každým generováním šifrovaného LS2 náhodně změnit pořadí klientů, aby zabránily klientům zjistit jejich pozici v seznamu a odvodit, kdy byli přidáni nebo odvoláni jiní klienti.

- Vnější vrstva obsahující nezbytné prosté informace pro ukládání a načítání.
- Střední vrstva, která zpracovává ověřování klienta.
- Vnitřní vrstva, která obsahuje skutečná data LS2.

Server může zvolit skrytí počtu přihlášených klientů vložením náhodných položek do seznamu autorizačních dat.

- Veřejný klíč pro podepisování v nezaslepeném cíli musí být
  Ed25519 (typ podpisu 7) nebo Red25519 (typ podpisu 11);
  žádné jiné typy podpisů nejsou podporovány
- Pokud je veřejný klíč pro podepisování offline, musí být přechodný veřejný klíč pro podepisování také Ed25519
- Zaslepení je výpočetně jednoduché
- Použití stávajících kryptografických primitiv
- Zaslepené veřejné klíče nelze odzaslepit
- Zaslepené veřejné klíče musí být na křivce Ed25519 a v prvočíselné podskupině
- Musí být znám veřejný klíč pro podepisování cíle
  (plný cíl není vyžadován) pro odvození zaslepeného veřejného klíče
- Volitelně poskytnout další tajemství vyžadované pro odvození zaslepeného veřejného klíče

Výhody autorizace klienta DH ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Bezpečnost schématu nezávisí výhradně na out-of-band výměně materiálu klíče klienta. Soukromý klíč klienta nikdy nemusí opustit jejich zařízení, a tak protivník, který může zachytit out-of-band výměnu, ale nemůže prolomit algoritmus DH, nemůže dešifrovat šifrovaný LS2, ani určit, jak dlouho má klient přístup.

### Šifrovaný LS s adresami Base 32

Nevýhody autorizace klienta DH ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Výhody autorizace klienta PSK ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

### Šifrovaný LS s offline klíči

Nevýhody autorizace klienta PSK ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Viz ná

Tento návrh nedefinuje žádný formát souboru pro zabalení více transientních a blinded klíčů a jejich poskytnutí klientovi nebo routeru. Tento návrh nedefinuje žádné rozšíření protokolu I2CP pro podporu šifrovaných leaseSetů s offline klíči.

### Poznámky

- Vyžaduje N + 1 operací DH na straně serveru pro N klientů.
- Vyžaduje jednu operaci DH na straně klienta.
- Vyžaduje, aby klient vygeneroval tajný klíč.

- Nevyžaduje žádné operace DH.
- Umožňuje serveru generovat tajný klíč.
- Umožňuje serveru sdílet stejný klíč s více klienty, pokud je to žádoucí.

- Bezpečnost schématu je kriticky závislá na out-of-band výměně materiálu klíče klienta. Protivník, který zachytí výměnu pro konkrétního klienta, může dešifrovat jakýkoli následný šifrovaný LS2, pro který je klient oprávněn, stejně jako určit, kdy je přístup klienta odvolán.

- ChaCha20 byl zvolen místo AES. Zatímco jsou rychlosti podobné, pokud je dostupná hardwarová podpora AES, ChaCha20 je 2,5–3× rychlejší, když hardwarová podpora AES není dostupná, například na méně výkonných zařízeních ARM.

- Na rychlosti nám nezáleží natolik, abychom použili BLAKE2b s klíčem. Velikost jeho výstupu je dostatečně velká, aby se do ní vešlo největší n, které potřebujeme (nebo jej můžeme zavolat jednou pro každý požadovaný klíč s čítačem jako argumentem). BLAKE2b je mnohem rychlejší než SHA-256 a BLAKE2b s klíčem by snížil celkový počet volání hashovací funkce.
  Viz však proposal 148, kde se navrhuje, abychom na BLAKE2b přešli z jiných důvodů.
  Viz [Secure key derivation performance](https://www.lvh.io/posts/secure-key-derivation-performance.html).

### Meta LS2

Používá se k nahrazení multihomingu. Stejně jako každý leaseSet je i tento podepsán tvůrcem. Jedná se o autentizovaný seznam hashů destinací.

Meta LS2 představuje vrchol, a možná také mezifázové uzly stromy. Obsahuje několik záznamů, z nichž každý ukazuje na LS, LS2 nebo jiný Meta LS2, aby podpořil masivní multihoming. Meta LS2 může obsahovat směs záznamů LS, LS2 a Meta LS2. Listvy stromu jsou vždy LS nebo LS2. Stromy jsou DAG; smyčky jsou zakázány; klienti provádějící hledání musí detekovat a odmítat následovat smyčky.

Meta LS2 může mít mnohem delší expiraci než standardní LS nebo LS2. Nejvyšší úroveň může mít expiraci několik hodin po datu zveřejnění. Maximální expirační doba bude vynucována floodfill routery a klienty a bude určena později.

Případ použití pro Meta LS2 je masivní multihoming, ale bez větší ochrany proti korelaci routerů s leaseSet (při restartu routeru), než jakou nyní poskytuje LS nebo LS2. To je ekvivalentní případu použití „facebook“, který pravděpodobně ochranu proti korelaci nepotřebuje. Tento případ použití pravděpodobně potřebuje offline klíče, které jsou poskytovány ve standardní hlavičce v každém uzlu stromu.

Back-end protokol pro koordinaci mezi leaf routery, intermediárními a master Meta LS signery zde není specifikován. Požadavky jsou extrémně jednoduché – pouze ověřit, že peer je dostupný, a každých několik hodin publikovat nový LS. Jediná složitost spočívá ve výběru nových publisherů pro Meta LS na nejvyšší nebo intermediární úrovni v případě selhání.

Mix-and-match leasesetů, kdy se lease z více routerů kombinují, podepisují a publikují v jediném leasesetu, je dokumentováno v návrhu 140 „invisible multihoming“. Tento návrh je v uvedené podobě neudržitelný, protože streamovací spojení by nebyla „sticky“ na jediném routeru, viz http://zzz.i2p/topics/2335 .

Back-end protokol a interakce s interními mechanismy routeru a klienta by pro neviditelný multihoming byly poměrně složité.

Aby nedošlo k přetížení floodfill pro top-level Meta LS, měla by být doba expirace alespoň několik hodin. Klienti musí top-level Meta LS ukládat do cache a uchovávat jej napříč restarty, pokud ještě nevypršel.

Je třeba definovat nějaký algoritmus pro klienty k procházení stromu, včetně záložních postupů, aby bylo využití rozptýleno. Nějakou funkci vzdálenosti hashů, ceny a náhodnosti. Pokud má uzel LS nebo LS2 a také Meta LS, musíme vědět, kdy smí tyto leaseSety použít a kdy pokračovat v procházení stromu.

TBD

    Standard LS flag (1)
Typy 3, 7 a 9 používají standardní hlavičku LS2, specifikovanou níže:

    Meta LS2 type (7)
Změny oproti stávajícímu LeaseSet:

    Hash of destination
    This hash is then used to generate the daily "routing key", as in LS1
Vyhledávání s

    Hours. Max 18.2 hours (65535 seconds)
Ukládání s

    "master" Destination or coordinator, or intermediate coordinators

### Formát

```
Standard LS2 Header as specified above

  Meta LS2 Type-Specific Part
  - Properties (Mapping as specified in common structures spec, 2 zero bytes if none)
  - Number of entries (1 byte) Maximum TBD
  - Entries. Each entry contains: (40 bytes)
    - Hash (32 bytes)
    - Flags (2 bytes)
      TBD. Set all to zero for compatibility with future uses.
    - Type (1 byte) The type of LS it is referencing;
      1 for LS, 3 for LS2, 5 for encrypted, 7 for meta, 0 for unknown.
    - Cost (priority) (1 byte)
    - Expires (4 bytes) (4 bytes, big endian, seconds since epoch, rolls over in 2106)
  - Number of revocations (1 byte) Maximum TBD
  - Revocations: Each revocation contains: (32 bytes)
    - Hash (32 bytes)

  Standard LS2 Signature:
  - Signature (40+ bytes)
    The signature is of everything above.
```
Příznaky a vlastnosti: pro budoucí použití

### Poznámky

- Distribuovaná služba, která by toto používala, by měla jednoho nebo více „masterů“ s privátním klíčem destinace služby. Ti by (out of band) určovali aktuální seznam aktivních destinací a publikovali Meta LS2. Pro redundanci by více masterů mohlo multihome (tj. souběžně publikovat) Meta LS2.

- Distribuovaná služba by mohla začít s jediným destination nebo použít multihoming starého stylu a poté přejít na Meta LS2. Standardní LS lookup by mohl vrátit kterýkoli z LS, LS2 nebo Meta LS2.

- Když služba používá Meta LS2, nemá žádné tunnely (leases).

### Záznam služby

Toto je individuální záznam říkající, že se destination účastní služby. Odesílá jej účastník floodfillu. Floodfill jej nikdy neodesílá samostatně, ale pouze jako součást Service Listu. Service Record se také používá k odvolání účasti ve službě, a to nastavením expirace na nulu.

Toto není LS2, ale používá standardní hlavičku a formát podpisu LS2.

TBD

    n/a, see Service List
Typy 3, 7 a 9 používají standardní hlavičku LS2, specifikovanou níže:

    Service Record type (9)
Změny oproti stávajícímu LeaseSet:

    Hash of service name
    This hash is then used to generate the daily "routing key", as in LS1
Vyhledávání s

    Hours. Max 18.2 hours (65535 seconds)
Ukládání s

    Destination

### Formát

```
Standard LS2 Header as specified above

  Service Record Type-Specific Part
  - Port (2 bytes, big endian) (0 if unspecified)
  - Hash of service name (32 bytes)

  Standard LS2 Signature:
  - Signature (40+ bytes)
    The signature is of everything above.
```
### Poznámky

- Pokud jsou hodnoty expires samé nuly, floodfill by měl záznam odvolat a již jej nezahrnovat do seznamu služeb.

- Ukládání: Floodfill může přísně omezovat ukládání těchto záznamů a omezit počet záznamů uložených na jeden hash a jejich expiraci. Může být také použit whitelist hashů.

- Jakýkoli jiný typ netdb se stejným hashem má prioritu, takže záznam služby nikdy nemůže
  přepsat LS/RI, ale LS/RI přepíše všechny záznamy služeb na daném hashi.

### Seznam služeb

To nemá s LS2 nic společného a používá jiný formát.

Seznam služeb je vytvářen a podepisován floodfillem. Je neautentizovaný v tom smyslu, že k jakékoli službě se může kdokoli připojit publikováním Service Record na floodfill.

Seznam služeb obsahuje krátké záznamy služeb, nikoli úplné záznamy služeb. Ty obsahují podpisy, ale pouze hashe, nikoli úplné destinace, takže je nelze ověřit bez úplné destinace.

Bezpečnost, pokud nějaká existuje, a vhodnost seznamů služeb jsou TBD. Floodfilly by mohly omezit publikování a vyhledávání na whitelist služeb, ale tento whitelist se může lišit v závislosti na implementaci nebo preferencích operátora. Nemusí být možné dosáhnout konsensu na společném základním whitelistu napříč implementacemi.

Pokud je v záznamu služby výše uveden název služby, mohou operátoři floodfill mít námitky; pokud je uveden pouze hash, neprobíhá žádná verifikace a záznam služby by se mohl „dostat dovnitř“ před jakýmkoli jiným typem netdb a být uložen ve floodfill.

TBD

    Service List lookup type (11)
Typy 3, 7 a 9 používají standardní hlavičku LS2, specifikovanou níže:

    Service List type (11)
Změny oproti stávajícímu LeaseSet:

    Hash of service name
    This hash is then used to generate the daily "routing key", as in LS1
Vyhledávání s

    Hours, not specified in the list itself, up to local policy
Ukládání s

    Nobody, never sent to floodfill, never flooded.

### Formát

Formát šifrovaného LS2 se skládá ze tří vnořených vrstev:

```
- Type (1 byte)
    Not actually in header, but part of data covered by signature.
    Take from field in Database Store Message.
  - Hash of the service name (implicit, in the Database Store message)
  - Hash of the Creator (floodfill) (32 bytes)
  - Published timestamp (8 bytes, big endian)

  - Number of Short Service Records (1 byte)
  - List of Short Service Records:
    Each Short Service Record contains (90+ bytes)
    - Dest hash (32 bytes)
    - Published timestamp (8 bytes, big endian)
    - Expires (4 bytes, big endian) (offset from published in ms)
    - Flags (2 bytes)
    - Port (2 bytes, big endian)
    - Sig length (2 bytes, big endian)
    - Signature of dest (40+ bytes)

  - Number of Revocation Records (1 byte)
  - List of Revocation Records:
    Each Revocation Record contains (86+ bytes)
    - Dest hash (32 bytes)
    - Published timestamp (8 bytes, big endian)
    - Flags (2 bytes)
    - Port (2 bytes, big endian)
    - Sig length (2 bytes, big endian)
    - Signature of dest (40+ bytes)

  - Signature of floodfill (40+ bytes)
    The signature is of everything above.
```
Pro ověření podpisu seznamu služeb:

- připojit hash názvu služby na začátek
- odstranit hash tvůrce
- zkontrolovat podpis upraveného obsahu

Pro ověření podpisu každého Short Service Record:

- Načíst destination
- Ověřit podpis (published timestamp + expires + flags + port + Hash názvu služby)

Pro ověření podpisu každého Revocation Record:

- Získat destinaci
- Ověřit podepsání (published timestamp + 4 zero bytes + flags + port + Hash of service name)

### Poznámky

- Používáme délku podpisu namísto typu sig, abychom mohli podporovat neznámé typy podpisů.

- Seznam služeb nemá dobu expirace; příjemci se mohou rozhodnout sami na základě zásad nebo expirace jednotlivých záznamů.

- Service Lists se nefloodují, floodují se pouze jednotlivé Service Records. Každý
  floodfill vytváří, podepisuje a ukládá do cache Service List. Floodfill používá
  vlastní politiku pro dobu cache a maximální počet záznamů služeb a revokací.

## Požadované změny specifikace společných struktur

### Certifikáty klíčů

Mimo rozsah tohoto návrhu. Přidat k návrhům ECIES 144 a 145.

### Nové zprostředkující struktury

Přidat nové struktury pro Lease2, MetaLease, LeaseSet2Header a OfflineSignature. Platné od verze 0.9.38.

### Nové typy NetDB

Přidat struktury pro každý nový typ leaseset, převzaté z výše uvedeného. Pro LeaseSet2, EncryptedLeaseSet a MetaLeaseSet platné od verze 0.9.38. Pro Service Record a Service List předběžné a bez stanoveného termínu.

### Nový typ podpisu

Přidat RedDSA_SHA512_Ed25519 Typ 11. Veřejný klíč má 32 bajtů; soukromý klíč má 32 bajtů; hash má 64 bajtů; podpis má 64 bajtů.

## Vyžadované změny specifikace šifrování

Mimo rozsah tohoto návrhu. Viz návrhy 144 a 145.

## Požadované změny I2NP

Poznámka: LS2 lze publikovat pouze do floodfills s minimální verzí.

### Zpráva o vyhledávání v databázi

Přidat typ vyhledávání seznamu služeb.

### Změny

```
Flags byte: Lookup type field, currently bits 3-2, expands to bits 4-2.
  Lookup type 0x04 is defined as the service list lookup.

  Add note: Service list loookup may only be sent to floodfills with a minimum version.
  Minimum version is 0.9.38.
```
### Zpráva o uložení do databáze

Přidat všechny nové typy úložišť.

### Změny

```
Type byte: Type field, currently bit 0, expands to bits 3-0.
  Type 3 is defined as a LS2 store.
  Type 5 is defined as a encrypted LS2 store.
  Type 7 is defined as a meta LS2 store.
  Type 9 is defined as a service record store.
  Type 11 is defined as a service list store.
  Other types are undefined and invalid.

  Add note: All new types may only be published to floodfills with a minimum version.
  Minimum version is 0.9.38.
```
## Požadované změny I2CP

### Možnosti I2CP

Nové volby interpretované na straně routeru, odesílané v SessionConfig Mapping:

```

  i2cp.leaseSetType=nnn       The type of leaseset to be sent in the Create Leaseset Message
                              Value is the same as the netdb store type in the table above.
                              Interpreted client-side, but also passed to the router in the
                              SessionConfig, to declare intent and check support.

  i2cp.leaseSetEncType=nnn[,nnn]  The encryption types to be used.
                                  Interpreted client-side, but also passed to the router in
                                  the SessionConfig, to declare intent and check support.
                                  See proposals 144 and 145.

  i2cp.leaseSetOfflineExpiration=nnn  The expiration of the offline signature, ASCII,
                                      seconds since the epoch.

  i2cp.leaseSetTransientPublicKey=[type:]b64  The base 64 of the transient private key,
                                              prefixed by an optional sig type number
                                              or name, default DSA_SHA1.
                                              Length as inferred from the sig type

  i2cp.leaseSetOfflineSignature=b64   The base 64 of the offline signature.
                                      Length as inferred from the destination
                                      signing public key type

  i2cp.leaseSetSecret=b64     The base 64 of a secret used to blind the
                              address of the leaseset, default ""

  i2cp.leaseSetAuthType=nnn   The type of authentication for encrypted LS2.
                              0 for no per-client authentication (the default)
                              1 for DH per-client authentication
                              2 for PSK per-client authentication

  i2cp.leaseSetPrivKey=b64    A base 64 private key for the router to use to
                              decrypt the encrypted LS2,
                              only if per-client authentication is enabled
```
Nové možnosti interpretované na straně klienta:

```

  i2cp.leaseSetType=nnn     The type of leaseset to be sent in the Create Leaseset Message
                            Value is the same as the netdb store type in the table above.
                            Interpreted client-side, but also passed to the router in the
                            SessionConfig, to declare intent and check support.

  i2cp.leaseSetEncType=nnn[,nnn]  The encryption types to be used.
                                  Interpreted client-side, but also passed to the router in
                                  the SessionConfig, to declare intent and check support.
                                  See proposals 144 and 145.

  i2cp.leaseSetSecret=b64     The base 64 of a secret used to blind the
                              address of the leaseset, default ""

  i2cp.leaseSetAuthType=nnn       The type of authentication for encrypted LS2.
                                  0 for no per-client authentication (the default)
                                  1 for DH per-client authentication
                                  2 for PSK per-client authentication

  i2cp.leaseSetBlindedType=nnn   The sig type of the blinded key for encrypted LS2.
                                 Default depends on the destination sig type.

  i2cp.leaseSetClient.dh.nnn=b64name:b64pubkey   The base 64 of the client name (ignored, UI use only),
                                                 followed by a ':', followed by the base 64 of the public
                                                 key to use for DH per-client auth. nnn starts with 0

  i2cp.leaseSetClient.psk.nnn=b64name:b64privkey   The base 64 of the client name (ignored, UI use only),
                                                   followed by a ':', followed by the base 64 of the private
                                                   key to use for PSK per-client auth. nnn starts with 0
```
### Konfigurace relace

Je třeba poznamenat, že pro offline podpisy jsou vyžadovány volby i2cp.leaseSetOfflineExpiration, i2cp.leaseSetTransientPublicKey a i2cp.leaseSetOfflineSignature a podpis je vytvořen přechodným podepisovacím soukromým klíčem.

### Zpráva žádosti o leaseSet

Router ke clientovi. Bez změn. Leases se posílají s 8bajtovými časovými stempeli, i když vrácený leaseset bude LS2 s 4bajtovými časovými stempeli. Je nutné si uvědomit, že odpověď může být Create Leaseset nebo Create Leaseset2 Message.

### Zpráva požadavku na variabilní leaseSet

Router ke clientovi. Bez změn. Leases se posílají s 8bajtovými časovými stempeli, i když vrácený leaseset bude LS2 s 4bajtovými časovými stempeli. Je nutné si uvědomit, že odpověď může být Create Leaseset nebo Create Leaseset2 Message.

### Vytvořit zprávu Leaseset2

Od klienta k routeru. Nová zpráva k použití místo Create Leaseset Message.

### Odůvodnění

- Aby router mohl zpracovat typ úložiště, musí být tento typ ve zprávě,
  pokud mu není předán předem v konfiguraci session.
  Pro společný parsovací kód je jednodušší mít jej v samotné zprávě.

- Aby router znal typ a délku soukromého klíče,
  musí být za lease set, pokud parser nezná typ předem
  v konfiguraci session.
  Pro obecný kód pro parsování je snazší znát ho ze samotné zprávy.

- Soukromý podpisový klíč, dříve definovaný pro revokaci a nepoužitý, se v LS2 nenachází.

### Typ zprávy

Typ zprávy Create Leaseset2 Message je 41.

### Formát

```
Session ID
  Type byte: Type of lease set to follow
             Type 1 is a LS
             Type 3 is a LS2
             Type 5 is a encrypted LS2
             Type 7 is a meta LS2
  LeaseSet: type specified above
  Number of private keys to follow (1 byte)
  Encryption Private Keys: For each public key in the lease set,
                           in the same order
                           (Not present for Meta LS2)
                           - Encryption type (2 bytes, big endian)
                           - Encryption key length (2 bytes, big endian)
                           - Encryption key (number of bytes specified)
```
### Poznámky

- Minimální verze routeru je 0.9.39.
- Předběžná verze s typem zprávy 40 byla v 0.9.38, ale formát byl změněn.
  Typ 40 je opuštěn a není podporován.

### Problémy

- K podpoře šifrovaných a meta LS je zapotřebí dalších změn.

### Informační zpráva o zaslepení

Od klienta k routeru. Nová zpráva.

### Odůvodnění

- Router potřebuje vědět, zda je destination blinded.
  Pokud je blinded a používá secret nebo per-client autentizaci,
  potřebuje mít tyto informace také.

- Host Lookup adresy b32 v novém formátu ("b33")
  sdělí routeru, že adresa je blinded, ale neexistuje žádný mechanismus,
  jak předat tajný nebo privátní klíč routeru ve zprávě Host Lookup.
  Ačkoli bychom mohli zprávu Host Lookup rozšířit o tuto informaci,
  čistší je definovat novou zprávu.

- Potřebujeme programový způsob, jak může klient sdělit routeru.
  Jinak by uživatel musel ručně nakonfigurovat každý destination.

### Použití

Než klient odešle zprávu na blinded destination, musí buď vyhledat "b33" ve zprávě Host Lookup, nebo odeslat zprávu Blinding Info. Pokud blinded destination vyžaduje tajný údaj nebo autentizaci jednotlivých klientů, musí klient odeslat zprávu Blinding Info.

Router na tuto zprávu neposílá odpověď.

### Typ zprávy

Typ zprávy pro Blinding Info Message je 42.

### Formát

```
Session ID
  Flags:       1 byte
               Bit order: 76543210
               Bit 0: 0 for everybody, 1 for per-client
               Bits 3-1: Authentication scheme, if bit 0 is set to 1 for per-client, otherwise 000
                         000: DH client authentication (or no per-client authentication)
                         001: PSK client authentication
               Bit 4: 1 if secret required, 0 if no secret required
               Bits 7-5: Unused, set to 0 for future compatibility
  Type byte:   Endpoint type to follow
               Type 0 is a Hash
               Type 1 is a host name String
               Type 2 is a Destination
               Type 3 is a Sig Type and Signing Public Key
  Blind Type:  2 byte blinded sig type (big endian)
  Expiration:  4 bytes, big endian, seconds since epoch
  Endpoint:    Data as specified above
               For type 0: 32 byte binary hash
               For type 1: host name String
               For type 2: binary Destination
               For type 3: 2 byte sig type (big endian)
                           Signing Public Key (length as implied by sig type)
  Private Key: Only if flag bit 0 is set to 1
               A 32-byte ECIES_X25519 private key
  Secret:      Only if flag bit 4 is set to 1
               A secret String
```
### Poznámky

- Minimální verze routeru je 0.9.43

### Problémy

### Zpráva odpovědi hostitele (enc)

Abychom podpořili vyhledávání hostname "b33" a vraceli informaci o tom, že router nemá požadované informace, definujeme pro Host Reply Message další kódy výsledku následovně:

```
2: Lookup password required
   3: Private key required
   4: Lookup password and private key required
   5: Leaseset decryption failure
```
Hodnoty 1–255 jsou již definovány jako chyby, takže neexistuje problém se zpětnou kompatibilitou.

### Zpráva o přesměrování meta

Router ke klientovi. Nová zpráva.

### Odůvodnění

Klient a priori neví, že daný Hash bude resolvovat na Meta LS.

Pokud vyhledání leaseset pro Destination vrátí Meta LS, router provede rekurzivní rozlišení. U datagramů to klientská strana vědět nemusí; u streamingu však, kde protokol kontroluje destination v SYN ACK, musí vědět, jaký je „skutečný" destination. Proto potřebujeme novou zprávu.

### Použití

Router udržuje cache pro skutečný cíl, který se používá z meta LS. Když klient odešle zprávu cíli, který se překládá na meta LS, router zkontroluje cache, zda obsahuje naposledy použitý skutečný cíl. Pokud je cache prázdná, router vybere cíl z meta LS a vyhledá leaseset. Pokud je vyhledání leaseset úspěšné, router přidá daný cíl do cache a odešle klientovi Meta Redirect Message. To se provádí pouze jednou, dokud cíl nevyprší a není nutné jej změnit. Klient musí tyto informace také uložit do cache, pokud je to potřeba. Meta Redirect Message se NEODESÍLÁ jako odpověď na každou SendMessage.

Router odesílá tuto zprávu pouze klientům s verzí 0.9.47 nebo vyšší.

Klient na tuto zprávu neposílá odpověď.

### Typ zprávy

Typ zprávy pro Meta Redirect Message je 43.

### Formát

```
Session ID (2 bytes) The value from the Send Message.
  Message ID generated by the router (4 bytes)
  4 byte nonce previously generated by the client
               (the value from the Send Message, may be zero)
  Flags:       2 bytes, bit order 15...0
               Unused, set to 0 for future compatibility
               Bit 0: 0 - the destination is no longer meta
                      1 - the destination is now meta
               Bits 15-1: Unused, set to 0 for future compatibility
  Original Destination (387+ bytes)
  (following fields only present if flags bit 0 is 1)
  MFlags:      2 bytes
               Unused, set to 0 for future compatibility
               From the Meta Lease for the actual Destination
  Expiration:  4 bytes, big endian, seconds since epoch
               From the Meta Lease for the actual Destination
  Cost (priority) 1 byte
               From the Meta Lease for the actual Destination
  Actual (real) Destination (387+ bytes)
```
### Změny pro podporu Meta

Jak generovat a podporovat Meta, včetně komunikace a koordinace mezi routery, je mimo rozsah tohoto návrhu. Viz související návrh 150.

### Změny pro podporu offline klíčů

Offline podpisy nelze ověřit ve streamovém přenosu ani v datagramech s možností odpovědi. Viz níže uvedené sekce.

## Je nutné provést změny v souboru soukromého klíče

Formát souboru soukromého klíče (eepPriv.dat) není oficiální součástí našich specifikací, ale je zdokumentován v [Java I2P javadocs](http://idk.i2p/javadoc-i2p/net/i2p/data/PrivateKeyFile.html) a další implementace jej podporují. To umožňuje přenositelnost soukromých klíčů mezi různými implementacemi.

Pro uložení dočasného veřejného klíče a informací o offline podepisování jsou nutné změny.

### Změny

```
If the signing private key is all zeros, the offline information section follows:

  - Expires timestamp
    (4 bytes, big endian, seconds since epoch, rolls over in 2106)
  - Sig type of transient Signing Public Key (2 bytes, big endian)
  - Transient Signing Public key
    (length as specified by transient sig type)
  - Signature of above three fields by offline key
    (length as specified by destination sig type)
  - Transient Signing Private key
    (length as specified by transient sig type)
```
### Požadované změny CLI pro soubor privátního klíče

Přidat podporu pro následující možnosti:

```
-d days              (specify expiration in days of offline sig, default 365)
      -o offlinedestfile   (generate the online key file,
                            using the offline key file specified)
      -r sigtype           (specify sig type of transient key, default Ed25519)
```
## Požadované změny streamování

Offline podpisy nelze v současnosti ověřovat ve streamingu. Níže uvedená změna přidává do možností blok pro offline podepisování. Tím se vyhneme nutnosti získávat tyto informace přes I2CP.

### Změny

```
Add new option:
  Bit:          11
  Flag:         OFFLINE_SIGNATURE
  Option order: 4
  Option data:  Variable bytes
  Function:     Contains the offline signature section from LS2.
                FROM_INCLUDED must also be set.
                Expires timestamp
                (4 bytes, big endian, seconds since epoch, rolls over in 2106)
                Transient sig type (2 bytes, big endian)
                Transient signing public key (length as implied by sig type)
                Signature of expires timestamp, transient sig type,
                and public key, by the destination public key,
                length as implied by destination public key sig type.

  Change option:
  Bit:          3
  Flag:         SIGNATURE_INCLUDED
  Option order: Change from 4 to 5

  Add information about transient keys to the
  Variable Length Signature Notes section:
  The offline signature option does not needed to be added for a CLOSE packet if
  a SYN packet containing the option was previously acked.
  More info TODO
```
### Poznámky

- Alternativou je pouze přidat příznak a získat přechodný veřejný klíč přes I2CP
  (Viz sekce Host Lookup / Host Reply Message výše)

## Požadované změny u Repliable Datagram

Offline podpisy nelze ověřit při zpracování repliable datagramů. Je potřeba příznak označující offline podepsání, ale není kam příznak umístit. Bude to vyžadovat zcela nové číslo protokolu a formát.

### Změny

```
Define new protocol 19 - Repliable datagram with options?
  - Destination (387+ bytes)
  - Flags (2 bytes)
    Bit order: 15 14 ... 3 2 1 0
    Bit 0: If 0, no offline keys; if 1, offline keys
    Bits 1-15: set to 0 for compatibility with future uses
  - If flag indicates offline keys, the offline signature section:
    Expires timestamp
    (4 bytes, big endian, seconds since epoch, rolls over in 2106)
    Transient sig type (2 bytes, big endian)
    Transient signing public key (length as implied by sig type)
    Signature of expires timestamp, transient sig type,
    and public key, by the destination public key,
    length as implied by destination public key sig type.
    This section can, and should, be generated offline.
  - Data
```
### Poznámky

- Alternativou je pouze přidat příznak a získat přechodný veřejný klíč prostřednictvím I2CP
  (Viz sekce Host Lookup / Host Reply Message výše)
- Jaké další možnosti bychom měli nyní přidat, když už máme bajty příznaků?

## Požadované změny SAM V3

SAM musí být rozšířen o podporu offline podpisů v DESTINATION base 64.

### Změny

```
Note that in the SESSION CREATE DESTINATION=$privkey,
  the $privkey raw data (before base64 conversion)
  may be optionally followed by the Offline Signature as specified in the
  Common Structures Specification.

  If the signing private key is all zeros, the offline information section follows:

  - Expires timestamp
    (4 bytes, big endian, seconds since epoch, rolls over in 2106)
  - Sig type of transient Signing Public Key (2 bytes, big endian)
  - Transient Signing Public key
    (length as specified by transient sig type)
  - Signature of above three fields by offline key
    (length as specified by destination sig type)
  - Transient Signing Private key (length as specified by transient sig type)
```
Poznamenejme, že offline podpisy jsou podporovány pouze pro STREAM a RAW, nikoli pro DATAGRAM (dokud nedefinujeme nový protokol DATAGRAM).

Je třeba poznamenat, že SESSION STATUS vrátí Signing Private Key složený ze samých nul a data Offline Signature přesně tak, jak byla dodána v SESSION CREATE.

Je důležité si uvědomit, že DEST GENERATE a SESSION CREATE DESTINATION=TRANSIENT nelze použít k vytvoření offline podepsané destinace.

### Problémy

Zvýšit verzi na 3.4, nebo ji ponechat na 3.1/3.2/3.3, aby mohla být přidána, aniž by vyžadovala všechny věci z 3.2/3.3?

Ostatní změny TBD. Viz výše uvedená sekce I2CP Host Reply Message.

## BOB: požadované změny

BOB by musel být rozšířen, aby podporoval offline podpisy a/nebo Meta LS. To má nízkou prioritu a pravděpodobně nebude nikdy specifikováno ani implementováno. Preferovaným rozhraním je SAM V3.

## Publikování, migrace, kompatibilita

LS2 (kromě šifrovaného LS2) se publikuje na stejném umístění v DHT jako LS1. Neexistuje způsob, jak publikovat LS1 i LS2, ledaže by LS2 byl na jiném místě.

Šifrovaný LS2 je publikován pod hashem typu blinded klíče a dat klíče. Tento hash se pak používá k vygenerování denního „routing key“, stejně jako v LS1.

LS2 je používán pouze tehdy, gdy jsou vyžadovány nové funkce (nový crypto, šifrované LS, meta atd.). LS2 lze publikovat pouze do floodfillů s uvedenou nebo vyšší verzí.

Servery publikující LS2 by věděly, že všichni připojující se klienti podporují LS2. Mohly by posílat LS2 v garlic.

Klienti by posílali LS2 v garlic zprávách pouze v případě, že používají novou kryptografii. Sdílení klienti by používali LS1 neomezeně? TODO: Jak mít sdíleného klienta, který podporuje starou i novou kryptografii?

## Nasazení

Verze 0.9.38 obsahuje podporu floodfill pro standardní LS2, včetně offline klíčů.

0.9.39 obsahuje podporu I2CP pro LS2 a Encrypted LS2, podepisování a ověřování typu sig 11, podporu floodfill pro Encrypted LS2 (typy sig 7 a 11, bez offline klíčů) a šifrování a dešifrování LS2 (bez autorizace pro jednotlivé klienty).

Verze 0.9.40 má podle plánu obsahovat podporu šifrování/dešifrování LS2 s autorizací pro jednotlivé klienty, podporu floodfill a I2CP pro Meta LS2, podporu šifrovaných LS2 s offline klíči a podporu b32 pro šifrované LS2.

## Poděkování

Návrh šifrovaného LS2 je výrazně ovlivněn [deskriptory skrytých služeb v3 v Toru](https://spec.torproject.org/rend-spec-v3), které měly podobné cíle návrhu.

## Odkazy

* ["High-speed high-security signatures" od Daniel J. Bernstein, Niels Duif, Tanja Lange, Peter Schwabe a Bo-Yin Yang](https://ed25519.cr.yp.to/)
* [KEYBLIND-PROOF](https://lists.torproject.org/pipermail/tor-dev/2013-December/005943.html)
* [KEYBLIND-REFS](https://gitlab.torproject.org/tpo/core/tor/-/issues/8106)
* [PRNG-REFS](http://projectbullrun.org/dual-ec/ext-rand.html)
* [RFC-2104](https://tools.ietf.org/html/rfc2104)
* [RFC-4880-S5.1](https://tools.ietf.org/html/rfc4880#section-5.1)
* [RFC-5869](https://tools.ietf.org/html/rfc5869)
* [RFC-7539-S2.4](https://tools.ietf.org/html/rfc7539#section-2.4)
* [TOR-REND-SPEC-V3](https://spec.torproject.org/rend-spec-v3)
* [UNSCIENTIFIC-KDF-SPEEDS](https://www.lvh.io/posts/secure-key-derivation-performance.html)
* [ZCASH](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf)
