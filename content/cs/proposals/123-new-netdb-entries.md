---
title: "Nové záznamy netDB"
number: "123"
author: "zzz, str4d, orignal"
created: "2016-01-16"
lastupdated: "2020-07-18"
status: "Otevřít"
thread: "http://zzz.i2p/topics/2051"
supercedes: "110, 120, 121, 122"
---

## Stav

Části tohoto návrhu jsou dokončeny a implementovány ve verzích 0.9.38 a 0.9.39. Specifikace Common Structures, I2CP, I2NP a další jsou nyní aktualizovány tak, aby odrážely změny, které jsou aktuálně podporovány.

Dokončené části jsou stále předmětem drobných revizí. Ostatní části tohoto návrhu jsou stále ve vývoji a předmětem podstatných revizí.

Vyhledávání služeb (typy 9 a 11) má nízkou prioritu a není naplánované, a může být vyčleněno do samostatného návrhu.

## Přehled

Toto je aktualizace a agregace následujících 4 návrhů:

- 110 LS2
- 120 Meta LS2 pro masivní multihoming
- 121 Šifrovaný LS2
- 122 Neautentizované vyhledávání služby (anycasting)

Tyto návrhy jsou převážně nezávislé, ale pro rozumnost definujeme a používáme společný formát pro několik z nich.

Následující návrhy spolu částečně souvisí:

- 140 Invisible Multihoming (nekompatibilní s tímto návrhem)
- 142 New Crypto Template (pro novou symetrickou kryptografii)
- 144 ECIES-X25519-AEAD-Ratchet
- 145 ECIES-P256
- 146 Red25519
- 148 EdDSA-BLAKE2b-Ed25519
- 149 B32 for Encrypted LS2
- 150 Garlic Farm Protocol
- 151 ECDSA Blinding

## Návrh

Tento návrh definuje 5 nových typů DatabaseEntry a proces pro jejich ukládání do a získávání ze síťové databáze, stejně jako metodu pro jejich podepisování a ověřování těchto podpisů.

### Goals

- Zpětně kompatibilní
- LS2 použitelné se starým stylem multihomingu
- Pro podporu nejsou vyžadovány žádné nové krypto nebo primitivy
- Zachovat oddělení krypto a podepisování; podporovat všechny současné a budoucí verze
- Umožnit volitelné offline podepisovací klíče
- Snížit přesnost časových značek pro omezení fingerprintingu
- Umožnit nové krypto pro destinations
- Umožnit masivní multihoming
- Opravit více problémů s existujícími šifrovanými LS
- Volitelné blinding pro snížení viditelnosti floodfilly
- Šifrované podporuje jak single-key tak více odvolatelných klíčů
- Service lookup pro snadnější vyhledávání outproxies, aplikačního DHT bootstrap
  a dalších využití
- Nerozbít nic, co se spoléhá na 32-bytové binární destination hashe, např. bittorrent
- Přidat flexibilitu do leaseSets pomocí vlastností, jako máme v routerinfos
- Umístit publikované časové značky a variabilní expiraci do hlavičky, takže funguje i
  pokud je obsah šifrován (neodvozovat časovou značku z nejdřívějšího lease)
- Všechny nové typy žijí ve stejném DHT prostoru a na stejných místech jako existující leaseSets,
  takže uživatelé mohou migrovat ze starých LS na LS2,
  nebo měnit mezi LS2, Meta a Encrypted,
  bez změny Destination nebo hashe
- Existující Destination může být převedena na používání offline klíčů,
  nebo zpět na online klíče, bez změny Destination nebo hashe

### Non-Goals / Out-of-scope

- Nový algoritmus rotace DHT nebo generování sdíleného náhodného čísla
- Specifický nový typ šifrování a schéma end-to-end šifrování
  pro použití tohoto nového typu by bylo v samostatném návrhu.
  Žádná nová kryptografie zde není specifikována ani diskutována.
- Nové šifrování pro RI nebo budování tunelů.
  To by bylo v samostatném návrhu.
- Metody šifrování, přenosu a příjmu I2NP DLM / DSM / DSRM zpráv.
  Nemění se.
- Jak generovat a podporovat Meta, včetně backend komunikace mezi routery, správy, převzetí služeb při selhání a koordinace.
  Podpora může být přidána do I2CP, nebo i2pcontrol, nebo nového protokolu.
  Toto může nebo nemusí být standardizováno.
- Jak skutečně implementovat a spravovat tunely s delší dobou expirace, nebo zrušit existující tunely.
  To je extrémně obtížné, a bez toho nemůžete mít rozumné elegantní vypnutí.
- Změny modelu hrozeb
- Formát offline úložiště, nebo metody pro ukládání/načítání/sdílení dat.
- Implementační detaily zde nejsou diskutovány a jsou ponechány na každém projektu.

### Justification

LS2 přidává pole pro změnu typu šifrování a pro budoucí změny protokolu.

Šifrované LS2 opravuje několik bezpečnostních problémů se stávajícími šifrovanými LS pomocí asymetrického šifrování celé sady leasů.

Meta LS2 poskytuje flexibilní, efektivní, účinné a rozsáhlé multihoming.

Service Record a Service List poskytují anycast služby jako je vyhledávání názvů a DHT bootstrapping.

### Cíle

Čísla typů se používají ve zprávách I2NP Database Lookup/Store.

Sloupec end-to-end se vztahuje k tomu, zda jsou dotazy/odpovědi odesílány do Destination v Garlic Message.

Existující typy:

| NetDB Data | Lookup Type | Store Type |
|------------|-------------|------------|
| any        | 0           | any        |
| LS         | 1           | 1          |
| RI         | 2           | 0          |
| exploratory| 3           | DSRM       |
Nové typy:

| NetDB Data     | Lookup Type | Store Type | Std. LS2 Header? | Sent end-to-end? |
|----------------|-------------|------------|------------------|------------------|
| LS2            | 1           | 3          | yes              | yes              |
| Encrypted LS2  | 1           | 5          | no               | no               |
| Meta LS2       | 1           | 7          | yes              | no               |
| Service Record | n/a         | 9          | yes              | no               |
| Service List   | 4           | 11         | no               | no               |
### Necíle / Mimo rozsah

- Typy vyhledávání jsou aktuálně bity 3-2 ve zprávě Database Lookup Message.
  Jakékoli další typy by vyžadovaly použití bitu 4.

- Všechny typy úložišť jsou liché, protože starší routery ignorují vyšší bity v poli typu Database Store Message.
  Raději chceme, aby parsování selhalo jako LS než jako komprimované RI.

- Má být typ explicitní nebo implicitní, nebo ani jeden v datech pokrytých podpisem?

### Zdůvodnění

Typy 3, 5 a 7 mohou být vráceny jako odpověď na standardní vyhledávání leaseSetu (typ 1). Typ 9 není nikdy vrácen jako odpověď na vyhledávání. Typ 11 je vrácen jako odpověď na nový typ vyhledávání služby (typ 11).

Pouze typ 3 může být odeslán v garlic zprávě mezi klienty.

### Datové typy NetDB

Typy 3, 7 a 9 mají všechny společný formát::

Standardní LS2 hlavička   - jak je definována níže

Část specifická pro typ - jak je definována níže v každé části

Standardní LS2 podpis:   - Délka podle typu podpisu podepisovacího klíče

Typ 5 (Šifrovaný) nezačíná Destination a má odlišný formát. Viz níže.

Typ 11 (Seznam služeb) je agregací několika Service Records a má odlišný formát. Viz níže.

### Poznámky

TBD

## Standard LS2 Header

Typy 3, 7 a 9 používají standardní LS2 hlavičku, specifikovanou níže:

### Proces vyhledávání/ukládání

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
### Formát

- Unpublished/published: Pro použití při odesílání database store end-to-end,
  odesílající router může chtít označit, že tento leaseSet by neměl být
  odeslán ostatním. V současnosti používáme heuristiky pro udržování tohoto stavu.

- Published: Nahrazuje komplexní logiku potřebnou k určení 'verze' leaseSetu. V současnosti je verzí vypršení posledního vypršujícího lease, a publikující router musí zvýšit toto vypršení alespoň o 1ms při publikování leaseSetu, který pouze odstraňuje starší lease.

- Expires: Umožňuje, aby vypršení platnosti záznamu netDb bylo dříve než u jeho naposledy vypršující leaseSet. Nemusí být užitečné pro LS2, kde se očekává, že leaseSet zůstanou s maximální dobou platnosti 11 minut, ale pro jiné nové typy je to nezbytné (viz Meta LS a Service Record níže).

- Offline klíče jsou volitelné, aby se snížila počáteční/požadovaná složitost implementace.

### Bezpečnostní a soukromí aspekty

- Mohlo by snížit přesnost časové značky ještě více (10 minut?), ale bylo by třeba přidat
  číslo verze. To by mohlo narušit multihoming, pokud nemáme šifrování zachovávající pořadí?
  Pravděpodobně se bez časových značek úplně obejít nemůžeme.

- Alternativa: 3bytový timestamp (epoch / 10 minut), 1bytová verze, 2bytový expires

- Je typ explicitní nebo implicitní v datech / podpisu? "Domain" konstanty pro podpis?

### Notes

- Routery by neměly publikovat LS více než jednou za sekundu.
  Pokud tak učiní, musí uměle navýšit publikované časové razítko o 1
  oproti předchozímu publikovanému LS.

- Implementace routerů mohou ukládat přechodné klíče a podpis do cache,
  aby se vyhnuly ověřování při každém použití. Zejména floodfilly a routery na
  obou koncích dlouhodobých spojení by z toho mohly těžit.

- Offline klíče a podpis jsou vhodné pouze pro dlouhodobě existující destinace,
  tj. servery, ne klienty.

## New DatabaseEntry types

### Formát

Změny oproti stávajícímu LeaseSet:

- Přidat publikované časové razítko, časové razítko vypršení, příznaky a vlastnosti
- Přidat typ šifrování
- Odstranit revokační klíč

Vyhledávání pomocí

    Standard LS flag (1)
Uložit pomocí

    Standard LS2 type (3)
Uložit v

    Hash of destination
    This hash is then used to generate the daily "routing key", as in LS1
Typická expirace

    10 minutes, as in a regular LS.
Publikoval

    Destination

### Zdůvodnění

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
### Problémy

- Properties: Budoucí rozšíření a flexibilita.
  Umístěno na první pozici pro případ, že by bylo nutné pro parsování zbývajících dat.

- Více párů typů šifrování/veřejných klíčů má
  usnadnit přechod na nové typy šifrování. Druhým způsobem, jak to udělat,
  je publikovat více leaseSetů, případně použít stejné tunely,
  jak to děláme nyní pro DSA a EdDSA destinace.
  Identifikace příchozího typu šifrování v tunelu
  může být provedena pomocí stávajícího mechanismu session tag,
  a/nebo zkuškového dešifrování pomocí každého klíče. Délky příchozích
  zpráv mohou také poskytnout nápovědu.

### Poznámky

Tento návrh nadále používá veřejný klíč v leaseSet pro koncové šifrovací klíče a ponechává pole veřejného klíče v Destination nepoužité, jak je tomu nyní. Typ šifrování není specifikován v certifikátu klíče Destination, zůstane 0.

Odmítnutou alternativou je specifikovat typ šifrování v certifikátu klíče Destination, použít veřejný klíč v Destination a nepoužívat veřejný klíč v leaseset. Neplánujeme toto dělat.

Výhody LS2:

- Umístění skutečného veřejného klíče se nemění.
- Typ šifrování nebo veřejný klíč se může změnit bez změny Destination.
- Odstraňuje nepoužívané pole pro odvolání
- Základní kompatibilita s ostatními typy DatabaseEntry v tomto návrhu
- Umožňuje více typů šifrování

Nevýhody LS2:

- Umístění veřejného klíče a typ šifrování se liší od RouterInfo
- Udržuje nepoužívaný veřejný klíč v leaseset
- Vyžaduje implementaci napříč sítí; alternativně mohou být použity experimentální
  typy šifrování, pokud to floodfills dovolují
  (viz související návrhy 136 a 137 o podpoře experimentálních typů podpisů).
  Alternativní návrh by mohl být jednodušší na implementaci a testování pro experimentální typy šifrování.

### New Encryption Issues

Některé z těchto bodů jsou mimo rozsah tohoto návrhu, ale prozatím zde uvádíme poznámky, protože ještě nemáme samostatný návrh pro šifrování. Viz také ECIES návrhy 144 a 145.

- Typ šifrování představuje kombinaci
  křivky, délky klíče a end-to-end schématu,
  včetně KDF a MAC, pokud existují.

- Zahrnuli jsme pole délky klíče, takže LS2 je
  parsovatelný a ověřitelný floodfill uzly i pro neznámé typy šifrování.

- První nový typ šifrování, který bude navržen, bude
  pravděpodobně ECIES/X25519. Jak bude použit end-to-end
  (buď mírně upravená verze ElGamal/AES+SessionTag
  nebo něco zcela nového, např. ChaCha/Poly) bude specifikováno
  v jednom nebo více samostatných návrzích.
  Viz také ECIES návrhy 144 a 145.

### LeaseSet 2

- 8-bajtová expirace v lease změněna na 4 bajty.

- Pokud někdy implementujeme revokaci, můžeme to udělat s expires polem nastaveným na nulu,
  nebo nulovými leases, nebo obojím. Není potřeba separátního revokačního klíče.

- Šifrovací klíče jsou seřazeny podle preferencí serveru, nejpreferovanější je první.
  Výchozí chování klienta je vybrat první klíč s
  podporovaným typem šifrování. Klienti mohou použít jiné algoritmy výběru
  založené na podpoře šifrování, relativním výkonu a dalších faktorech.

### Formát

Cíle:

- Přidat blinding
- Povolit více typů podpisů
- Nevyžadovat žádné nové kryptografické primitivy
- Volitelně šifrovat pro každého příjemce, odvolatelné
- Podporovat šifrování pouze Standard LS2 a Meta LS2

Šifrované LS2 se nikdy neodesílá v end-to-end garlic zprávě. Použijte standardní LS2 jako výše.

Změny oproti existujícímu šifrovanému LeaseSet:

- Zašifrovat celý obsah pro zabezpečení
- Bezpečně zašifrovat, ne pouze pomocí AES
- Zašifrovat pro každého příjemce

Vyhledání pomocí

    Standard LS flag (1)
Uložit pomocí

    Encrypted LS2 type (5)
Uložit v

    Hash of blinded sig type and blinded public key
    Two byte sig type (big endian, e.g. 0x000b) || blinded public key
    This hash is then used to generate the daily "routing key", as in LS1
Typická expirace

    10 minutes, as in a regular LS, or hours, as in a meta LS.
Publikoval

    Destination


### Odůvodnění

Definujeme následující funkce odpovídající kryptografickým stavebním blokům používaným pro šifrované LS2:

CSRNG(n)

    n-byte output from a cryptographically-secure random number generator.

    In addition to the requirement of CSRNG being cryptographically-secure (and thus
    suitable for generating key material), it MUST be safe
    for some n-byte output to be used for key material when the byte sequences immediately
    preceding and following it are exposed on the network (such as in a salt, or encrypted
    padding). Implementations that rely on a potentially-untrustworthy source should hash
    any output that is to be exposed on the network. See [PRNG references](http://projectbullrun.org/dual-ec/ext-rand.html) and [Tor dev discussion](https://lists.torproject.org/pipermail/tor-dev/2015-November/009954.html).

H(p, d)

    SHA-256 hash function that takes a personalization string p and data d, and
    produces an output of length 32 bytes.

    Use SHA-256 as follows::

        H(p, d) := SHA-256(p || d)

STREAM

    The ChaCha20 stream cipher as specified in [RFC 7539 Section 2.4](https://tools.ietf.org/html/rfc7539#section-2.4), with the initial counter
    set to 1. S_KEY_LEN = 32 and S_IV_LEN = 12.

    ENCRYPT(k, iv, plaintext)
        Encrypts plaintext using the cipher key k, and nonce iv which MUST be unique for
        the key k. Returns a ciphertext that is the same size as the plaintext.

        The entire ciphertext must be indistinguishable from random if the key is secret.

    DECRYPT(k, iv, ciphertext)
        Decrypts ciphertext using the cipher key k, and nonce iv. Returns the plaintext.


SIG

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

DH

    X25519 public key agreement system. Private keys of 32 bytes, public keys of 32
    bytes, produces outputs of 32 bytes. It has the following
    functions:

    GENERATE_PRIVATE()
        Generates a new private key.

    DERIVE_PUBLIC(privkey)
        Returns the public key corresponding to the given private key.

    DH(privkey, pubkey)
        Generates a shared secret from the given private and public keys.

HKDF(salt, ikm, info, n)

    A cryptographic key derivation function which takes some input key material ikm (which
    should have good entropy but is not required to be a uniformly random string), a salt
    of length 32 bytes, and a context-specific 'info' value, and produces an output
    of n bytes suitable for use as key material.

    Use HKDF as specified in [RFC 5869](https://tools.ietf.org/html/rfc5869), using the HMAC hash function SHA-256
    as specified in [RFC 2104](https://tools.ietf.org/html/rfc2104). This means that SALT_LEN is 32 bytes max.


### Diskuse

Šifrovaný formát LS2 se skládá ze tří vnořených vrstev:

- Vnější vrstva obsahující nezbytné informace v prostém textu pro ukládání a získávání.
- Střední vrstva, která zajišťuje autentifikaci klienta.
- Vnitřní vrstva obsahující skutečná data LS2.

Celkový formát vypadá takto::

    Layer 0 data + Enc(layer 1 data + Enc(layer 2 data)) + Signature

Poznamenejte, že šifrovaný LS2 je zaslepený. Destination není v hlavičce. Umístění DHT úložiště je SHA-256(sig type || blinded public key) a je denně rotováno.

Nepoužívá standardní LS2 hlavičku specifikovanou výše.

#### Layer 0 (outer)

Typ

    1 byte

    Not actually in header, but part of data covered by signature.
    Take from field in Database Store Message.

Typ podpisu zaslepeného veřejného klíče

    2 bytes, big endian
    This will always be type 11, identifying a Red25519 blinded key.

Zaslepený veřejný klíč

    Length as implied by sig type

Časové razítko publikování

    4 bytes, big endian

    Seconds since epoch, rolls over in 2106

Platnost vyprší

    2 bytes, big endian

    Offset from published timestamp in seconds, 18.2 hours max

Příznaky

    2 bytes

    Bit order: 15 14 ... 3 2 1 0

    Bit 0: If 0, no offline keys; if 1, offline keys

    Other bits: set to 0 for compatibility with future uses

Přechodná klíčová data

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

lenOuterCiphertext

    2 bytes, big endian

outerCiphertext

    lenOuterCiphertext bytes

    Encrypted layer 1 data. See below for key derivation and encryption algorithms.

Podpis

    Length as implied by sig type of the signing key used

    The signature is of everything above.

    If the flag indicates offline keys, the signature is verified with the transient
    public key. Otherwise, the signature is verified with the blinded public key.


#### Layer 1 (middle)

Příznaky

    1 byte
    
    Bit order: 76543210

    Bit 0: 0 for everybody, 1 for per-client, auth section to follow

    Bits 3-1: Authentication scheme, only if bit 0 is set to 1 for per-client, otherwise 000
              000: DH client authentication (or no per-client authentication)
              001: PSK client authentication

    Bits 7-4: Unused, set to 0 for future compatibility

DH autentizační data klienta

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

PSK data pro ověření klienta

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


innerCiphertext

    Length implied by lenOuterCiphertext (whatever data remains)

    Encrypted layer 2 data. See below for key derivation and encryption algorithms.


#### Layer 2 (inner)

Typ

    1 byte

    Either 3 (LS2) or 7 (Meta LS2)

Data

    LeaseSet2 data for the given type.

    Includes the header and signature.


### Nové problémy s šifrováním

Používáme následující schéma pro key blinding, založené na Ed25519 a [ZCash RedDSA](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf). Re25519 podpisy jsou nad Ed25519 křivkou, s použitím SHA-512 pro hash.

Nepoužíváme [Tor's rend-spec-v3.txt appendix A.2](https://spec.torproject.org/rend-spec-v3), který má podobné návrhové cíle, protože jeho zaslepené veřejné klíče mohou být mimo podskupinu prvočíselného řádu, s neznámými bezpečnostními důsledky.

#### Goals

- Podpisový veřejný klíč v neoslepeném cíli musí být
  Ed25519 (typ podpisu 7) nebo Red25519 (typ podpisu 11);
  žádné jiné typy podpisů nejsou podporovány
- Pokud je podpisový veřejný klíč offline, přechodný podpisový veřejný klíč musí být také Ed25519
- Blinding je výpočetně jednoduché
- Používá stávající kryptografické primitiva
- Oslepené veřejné klíče nelze rozoslepit
- Oslepené veřejné klíče musí být na křivce Ed25519 a v podgrupě s prvočíselným řádem
- Pro odvození oslepeného veřejného klíče je nutné znát podpisový veřejný klíč cíle
  (kompletní cíl není vyžadován)
- Volitelně poskytuje dodatečné tajemství požadované pro odvození oslepeného veřejného klíče

#### Security

Bezpečnost blinding schématu vyžaduje, aby distribuce alpha byla stejná jako u neoslepených soukromých klíčů. Když však oslepíme Ed25519 soukromý klíč (sig type 7) na Red25519 soukromý klíč (sig type 11), distribuce je odlišná. Pro splnění požadavků [zcash section 4.1.6.1](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf) by měl být Red25519 (sig type 11) použit i pro neoslepené klíče, takže "kombinace re-randomizovaného veřejného klíče a podpisu/ů pod tímto klíčem neodhalí klíč, ze kterého byl re-randomizován." Umožňujeme type 7 pro existující destinace, ale doporučujeme type 11 pro nové destinace, které budou šifrovány.

#### Definitions

B

    The Ed25519 base point (generator) 2^255 - 19 as in [Ed25519](http://cr.yp.to/papers.html#ed25519)

L

    The Ed25519 order 2^252 + 27742317777372353535851937790883648493
    as in [Ed25519](http://cr.yp.to/papers.html#ed25519)

DERIVE_PUBLIC(a)

    Convert a private key to public, as in Ed25519 (mulitply by G)

alfa

    A 32-byte random number known to those who know the destination.

GENERATE_ALPHA(destination, date, secret)

    Generate alpha for the current date, for those who know the destination and the secret.
    The result must be identically distributed as Ed25519 private keys.

a

    The unblinded 32-byte EdDSA or RedDSA signing private key used to sign the destination

A

    The unblinded 32-byte EdDSA or RedDSA signing public key in the destination,
    = DERIVE_PUBLIC(a), as in Ed25519

a'

    The blinded 32-byte EdDSA signing private key used to sign the encrypted leaseset
    This is a valid EdDSA private key.

A'

    The blinded 32-byte EdDSA signing public key in the Destination,
    may be generated with DERIVE_PUBLIC(a'), or from A and alpha.
    This is a valid EdDSA public key, on the curve and on the prime-order subgroup.

LEOS2IP(x)

    Flip the order of the input bytes to little-endian

H*(x)

    32 bytes = (LEOS2IP(SHA512(x))) mod B, same as in Ed25519 hash-and-reduce


#### Blinding Calculations

Nové tajné alpha a blinded klíče musí být vygenerovány každý den (UTC). Tajné alpha a blinded klíče se vypočítávají následovně.

GENERATE_ALPHA(destination, date, secret), pro všechny strany:

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
BLIND_PRIVKEY(), pro vlastníka publikujícího leaseSet:

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
BLIND_PUBKEY(), pro klienty získávající leaseset:

```text
// BLIND_PUBKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  A = destination's signing public key
  // Addition using group elements (points on the curve)
  blinded public key = A' = BLIND_PUBKEY(A, alpha) = A + DERIVE_PUBLIC(alpha)
```
Obě metody výpočtu A' poskytují stejný výsledek, jak je požadováno.

#### Signing

Neoslepený leaseset je podepsán neoslepeným Ed25519 nebo Red25519 podepisovacím privátním klíčem a ověřen neoslepeným Ed25519 nebo Red25519 podepisovacím veřejným klíčem (typy podpisů 7 nebo 11) jako obvykle.

Pokud je veřejný klíč pro podepisování offline, neoslepený leaseset je podepsán neoslepeným přechodným soukromým klíčem Ed25519 nebo Red25519 pro podepisování a ověřen neoslepeným přechodným veřejným klíčem Ed25519 nebo Red25519 pro podepisování (typy podpisů 7 nebo 11) obvyklým způsobem. Další poznámky k offline klíčům pro šifrované leasesety viz níže.

Pro podepisování šifrovaného leaseSet používáme Red25519, založené na [RedDSA](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf) pro podepisování a ověřování se zaslepenými klíči. Podpisy Red25519 jsou nad křivkou Ed25519, používající SHA-512 pro hash.

Red25519 je identický se standardním Ed25519 kromě níže uvedených specifikací.

#### Sign/Verify Calculations

Vnější část šifrovaného leaseSetu používá Red25519 klíče a podpisy.

Red25519 je téměř identické s Ed25519. Existují dva rozdíly:

Red25519 soukromé klíče jsou generovány z náhodných čísel a poté musí být redukovány mod L, kde L je definováno výše. Ed25519 soukromé klíče jsou generovány z náhodných čísel a poté "svorkovány" pomocí bitového maskování na byty 0 a 31. Toto se pro Red25519 nedělá. Funkce GENERATE_ALPHA() a BLIND_PRIVKEY() definované výše generují správné Red25519 soukromé klíče pomocí mod L.

V Red25519 používá výpočet r pro podepisování dodatečná náhodná data a využívá hodnotu veřejného klíče namísto hashe soukromého klíče. Díky náhodným datům je každý Red25519 podpis odlišný, i když se podepisují stejná data se stejným klíčem.

Podepisování:

```text
T = 80 random bytes
  r = H*(T || publickey || message)
  // rest is the same as in Ed25519
```
Ověření:

```text
// same as in Ed25519
```
### Poznámky

#### Derivation of subcredentials

V rámci procesu blinding musíme zajistit, že šifrovaný LS2 může být dešifrován pouze někým, kdo zná odpovídající veřejný podpisový klíč Destination. Úplná Destination není vyžadována. K dosažení tohoto cíle odvodíme credential z veřejného podpisového klíče:

```text
A = destination's signing public key
  stA = signature type of A, 2 bytes big endian (0x0007 or 0x000b)
  stA' = signature type of A', 2 bytes big endian (0x000b)
  keydata = A || stA || stA'
  credential = H("credential", keydata)
```
Personalizační řetězec zajišťuje, že credential nekoliduje s jakýmkoli hashem použitým jako klíč pro DHT vyhledávání, například s prostým hashem Destination.

Pro daný blinded key můžeme poté odvodit subcredential:

```text
subcredential = H("subcredential", credential || blindedPublicKey)
```
Subcredential je zahrnuta do procesů odvození klíčů níže, které tyto klíče váží na znalost podpisového veřejného klíče Destination.

#### Layer 1 encryption

Nejprve je připraven vstup pro proces derivace klíče:

```text
outerInput = subcredential || publishedTimestamp
```
Dále je vygenerována náhodná sůl:

```text
outerSalt = CSRNG(32)
```
Poté je odvozený klíč použitý k šifrování vrstvy 1:

```text
keys = HKDF(outerSalt, outerInput, "ELS2_L1K", 44)
  outerKey = keys[0:31]
  outerIV = keys[32:43]
```
Nakonec je vrstva 1 prostý text zašifrována a serializována:

```text
outerCiphertext = outerSalt || ENCRYPT(outerKey, outerIV, outerPlaintext)
```
#### Layer 1 decryption

Sůl je analyzována z šifrovaného textu vrstvy 1:

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
Nakonec je dešifrován ciphertext vrstvy 1:

```text
outerPlaintext = DECRYPT(outerKey, outerIV, outerCiphertext[32:end])
```
#### Layer 2 encryption

Když je povolena autorizace klienta, ``authCookie`` se vypočítá jak je popsáno níže. Když je autorizace klienta zakázána, ``authCookie`` je pole bajtů s nulovou délkou.

Šifrování probíhá podobným způsobem jako u vrstvy 1:

```text
innerInput = authCookie || subcredential || publishedTimestamp
  innerSalt = CSRNG(32)
  keys = HKDF(innerSalt, innerInput, "ELS2_L2K", 44)
  innerKey = keys[0:31]
  innerIV = keys[32:43]
  innerCiphertext = innerSalt || ENCRYPT(innerKey, innerIV, innerPlaintext)
```
#### Layer 2 decryption

Když je povolena autorizace klienta, ``authCookie`` se vypočítá podle popisu níže. Když je autorizace klienta zakázána, ``authCookie`` je pole bajtů nulové délky.

Dešifrování probíhá podobným způsobem jako u vrstvy 1:

```text
innerInput = authCookie || subcredential || publishedTimestamp
  innerSalt = innerCiphertext[0:31]
  keys = HKDF(innerSalt, innerInput, "ELS2_L2K", 44)
  innerKey = keys[0:31]
  innerIV = keys[32:43]
  innerPlaintext = DECRYPT(innerKey, innerIV, innerCiphertext[32:end])
```
### Šifrovaný LS2

Když je pro Destination povolena autorizace klientů, server udržuje seznam klientů, které autorizuje k dešifrování zašifrovaných dat LS2. Data uložená pro každého klienta závisí na autorizačním mechanismu a zahrnují určitou formu klíčového materiálu, který každý klient generuje a odesílá serveru prostřednictvím zabezpečeného out-of-band mechanismu.

Existují dvě alternativy pro implementaci autorizace podle klientů:

#### DH client authorization

Každý klient vygeneruje DH pár klíčů ``[csk_i, cpk_i]`` a odešle veřejný klíč ``cpk_i`` na server.

Zpracování serveru
^^^^^^^^^^^^^^^^^

Server vygeneruje nový ``authCookie`` a dočasný DH pár klíčů:

```text
authCookie = CSRNG(32)
  esk = GENERATE_PRIVATE()
  epk = DERIVE_PUBLIC(esk)
```
Poté server pro každého autorizovaného klienta zašifruje ``authCookie`` jeho veřejným klíčem:

```text
sharedSecret = DH(esk, cpk_i)
  authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
  okm = HKDF(epk, authInput, "ELS2_XCA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
  clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
```
Server umístí každou dvojici ``[clientID_i, clientCookie_i]`` do vrstvy 1 šifrovaného LS2, spolu s ``epk``.

Zpracování klienta
^^^^^^^^^^^^^^^^^

Klient používá svůj privátní klíč k odvození svého očekávaného identifikátoru klienta ``clientID_i``, šifrovacího klíče ``clientKey_i`` a šifrovacího IV ``clientIV_i``:

```text
sharedSecret = DH(csk_i, epk)
  authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
  okm = HKDF(epk, authInput, "ELS2_XCA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
```
Poté klient prohledává autorizační data vrstvy 1 pro záznam, který obsahuje ``clientID_i``. Pokud odpovídající záznam existuje, klient ho dešifruje, aby získal ``authCookie``:

```text
authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie_i)
```
#### Pre-shared key client authorization

Každý klient vygeneruje tajný 32-bajtový klíč ``psk_i`` a odešle ho serveru. Alternativně může server vygenerovat tajný klíč a odeslat ho jednomu nebo více klientům.

Zpracování na serveru
^^^^^^^^^^^^^^^^^^^

Server vygeneruje nový ``authCookie`` a salt:

```text
authCookie = CSRNG(32)
  authSalt = CSRNG(32)
```
Poté pro každého autorizovaného klienta server zašifruje ``authCookie`` jeho předsdíleným klíčem:

```text
authInput = psk_i || subcredential || publishedTimestamp
  okm = HKDF(authSalt, authInput, "ELS2PSKA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
  clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
```
Server umístí každou dvojici ``[clientID_i, clientCookie_i]`` do vrstvy 1 šifrovaného LS2 spolu s ``authSalt``.

Zpracování klienta
^^^^^^^^^^^^^^^^^

Klient používá svůj předem sdílený klíč k odvození svého očekávaného identifikátoru klienta ``clientID_i``, šifrovacího klíče ``clientKey_i`` a šifrovacího IV ``clientIV_i``:

```text
authInput = psk_i || subcredential || publishedTimestamp
  okm = HKDF(authSalt, authInput, "ELS2PSKA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
```
Poté klient prohledává autorizační data vrstvy 1 pro záznam, který obsahuje ``clientID_i``. Pokud odpovídající záznam existuje, klient ho dešifruje a získá ``authCookie``:

```text
authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie_i)
```
#### Security considerations

Oba výše uvedené mechanismy autorizace klientů poskytují soukromí pro členství klientů. Entita, která zná pouze Destination, může vidět, kolik klientů je v danou chvíli přihlášeno, ale nemůže sledovat, kteří klienti jsou přidáváni nebo odvoláváni.

Servery BY MĚLY randomizovat pořadí klientů pokaždé, když generují šifrovaný LS2, aby zabránily klientům zjistit jejich pozici v seznamu a odvodit, kdy byli jiní klienti přidáni nebo odvoláni.

Server MŮŽE zvolit skrytí počtu klientů, kteří jsou přihlášeni k odběru, vložením náhodných záznamů do seznamu autorizačních dat.

Výhody DH autorizace klienta
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Bezpečnost schématu není závislá pouze na out-of-band výměně klíčového materiálu klienta. Soukromý klíč klienta nikdy nepotřebuje opustit jejich zařízení, takže protivník, který je schopen zachytit out-of-band výměnu, ale nemůže prolomit DH algoritmus, nemůže dešifrovat šifrovaný LS2 ani určit, jak dlouho je klientovi udělen přístup.

Nevýhody DH klientské autorizace
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Vyžaduje N + 1 DH operací na straně serveru pro N klientů.
- Vyžaduje jednu DH operaci na straně klienta.
- Vyžaduje, aby klient vygeneroval tajný klíč.

Výhody PSK autorizace klienta
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Nevyžaduje žádné DH operace.
- Umožňuje serveru generovat tajný klíč.
- Umožňuje serveru sdílet stejný klíč s více klienty, pokud je to požadováno.

Nevýhody PSK autorizace klienta
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Bezpečnost schématu je kriticky závislá na out-of-band výměně klíčového materiálu klienta. Protivník, který zachytí výměnu pro konkrétního klienta, může dešifrovat jakýkoli následující zašifrovaný LS2, pro který je tento klient autorizován, a také určit, kdy je přístup klienta odvolán.

### Definice

Viz návrh 149.

Nemůžete použít šifrovaný LS2 pro bittorrent kvůli kompaktním announce odpovědím, které mají 32 bajtů. Těchto 32 bajtů obsahuje pouze hash. Není tam místo pro označení, že leaseset je šifrovaný, nebo pro typy podpisů.

### Formát

Pro šifrované leaseSety s offline klíči musí být také offline generovány zaslepené soukromé klíče, jeden pro každý den.

Jelikož volitelný offline podpisový blok je v nešifrované části šifrovaného leaseSetu, kdokoli procházející floodfilly by mohl tuto informaci použít ke sledování leaseSetu (ale nemohl by ho dešifrovat) po dobu několika dnů. Aby se tomu zabránilo, vlastník klíčů by měl také generovat nové přechodné klíče pro každý den. Jak přechodné, tak oslепené klíče lze generovat dopředu a doručit do routeru dávkově.

V tomto návrhu není definován žádný formát souboru pro zabalení více přechodných a zaslepených klíčů a jejich poskytování klientovi nebo routeru. V tomto návrhu není definováno žádné rozšíření protokolu I2CP pro podporu šifrovaných leaseSetu s offline klíči.

### Notes

- Služba používající šifrované leaseSet by publikovala šifrovanou verzi do floodfill. Pro efektivitu by však odesílala nešifrované leaseSet klientům ve zabaleném garlic message, jakmile by byly ověřeny (například přes whitelist).

- Floodfilly mohou omezit maximální velikost na rozumnou hodnotu, aby zabránily zneužití.

- Po dešifrování by mělo být provedeno několik kontrol, včetně ověření, že
  vnitřní časové razítko a doba vypršení odpovídají těm na nejvyšší úrovni.

- ChaCha20 byl vybrán místo AES. Zatímco rychlosti jsou podobné pokud je k dispozici hardwarová podpora AES, ChaCha20 je 2,5-3x rychlejší když hardwarová podpora AES není dostupná, například na méně výkonných ARM zařízeních.

- Nestaráme se dostatečně o rychlost, abychom používali keyed BLAKE2b. Má dostatečně velkou výstupní velikost pro největší n, které vyžadujeme (nebo jej můžeme zavolat jednou pro každý požadovaný klíč s argumentem čítače). BLAKE2b je mnohem rychlejší než SHA-256 a keyed-BLAKE2b by snížil celkový počet volání hash funkcí.
  Nicméně viz návrh 148, kde se navrhuje, abychom přešli na BLAKE2b z jiných důvodů.
  Viz [Secure key derivation performance](https://www.lvh.io/posts/secure-key-derivation-performance.html).

### Meta LS2

Toto se používá k nahrazení multihomingu. Stejně jako jakýkoli leaseset, je podepsáno tvůrcem. Jedná se o ověřený seznam hashů destinací.

Meta LS2 je vrchol a případně i mezilehlé uzly stromové struktury. Obsahuje řadu záznamů, z nichž každý odkazuje na LS, LS2 nebo jiný Meta LS2 pro podporu masivního multihomingu. Meta LS2 může obsahovat mix záznamů LS, LS2 a Meta LS2. Listy stromu jsou vždy LS nebo LS2. Strom je DAG; smyčky jsou zakázány; klienti provádějící vyhledávání musí detekovat a odmítnout následování smyček.

Meta LS2 může mít mnohem delší dobu vypršení než standardní LS nebo LS2. Nejvyšší úroveň může mít vypršení několik hodin po datu publikace. Maximální doba vypršení bude vynucována floodfilly a klienty a je TBD.

Případem použití pro Meta LS2 je masivní multihoming, ale bez větší ochrany proti korelaci routerů s leaseSety (v době restartu routeru), než jaká je poskytována nyní s LS nebo LS2. To je ekvivalentní případu použití "facebook", který pravděpodobně nepotřebuje ochranu proti korelaci. Tento případ použití pravděpodobně potřebuje offline klíče, které jsou poskytovány ve standardní hlavičce v každém uzlu stromu.

Back-end protokol pro koordinaci mezi leaf routery, zprostředkujícími a hlavními podepisovateli Meta LS zde není specifikován. Požadavky jsou velmi jednoduché - pouze ověřit, že peer je aktivní, a publikovat nový LS každých několik hodin. Jediná složitost spočívá ve výběru nových vydavatelů pro Meta LS na nejvyšší úrovni nebo zprostředkující úrovni při selhání.

Mix-and-match leasesets, kde jsou leasy z více routerů kombinovány, podepsány a publikovány v jednom leasesetu, jsou dokumentovány v návrhu 140, "invisible multihoming". Tento návrh je v současné podobě neudržitelný, protože streaming spojení by nebyla "lepkavá" k jednomu routeru, viz http://zzz.i2p/topics/2335 .

Back-end protokol a interakce s interními součástmi routeru a klienta by byly pro neviditelný multihoming poměrně složité.

Aby se zabránilo přetížení floodfill pro Meta LS nejvyšší úrovně, měla by být doba vypršení alespoň několik hodin. Klienti musí ukládat Meta LS nejvyšší úrovně do cache a zachovat jej při restartech, pokud nevypršel.

Potřebujeme definovat nějaký algoritmus pro klienty k procházení stromu, včetně záložních řešení, aby bylo použití rozptýlené. Nějakou funkci vzdálenosti hash, nákladů a náhodnosti. Pokud má uzel jak LS nebo LS2, tak i Meta LS, musíme vědět, kdy je dovoleno tyto leaseSety použít a kdy pokračovat v procházení stromu.

Vyhledání pomocí

    Standard LS flag (1)
Uložit pomocí

    Meta LS2 type (7)
Uložit v

    Hash of destination
    This hash is then used to generate the daily "routing key", as in LS1
Typické vypršení

    Hours. Max 18.2 hours (65535 seconds)
Publikováno

    "master" Destination or coordinator, or intermediate coordinators

### Format

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
Flags a vlastnosti: pro budoucí použití

### Odvození zaslepovacího klíče

- Distribuovaná služba používající toto by měla jednoho nebo více "masterů" s privátním klíčem cílové destinace služby. Ti by (mimo pásmo) určovali aktuální seznam aktivních destinací a publikovali by Meta LS2. Pro redundanci by mohlo více masterů současně hostovat (tj. souběžně publikovat) Meta LS2.

- Distribuovaná služba by mohla začít s jedinou destinací nebo použít multihoming starého stylu, poté přejít na Meta LS2. Standardní LS lookup by mohl vrátit kterýkoliv z LS, LS2, nebo Meta LS2.

- Když služba používá Meta LS2, nemá žádné tunely (leases).

### Service Record

Toto je individuální záznam, který říká, že destinace se účastní služby. Je odeslán od účastníka k floodfill. Nikdy není posílán jednotlivě floodfill routerem, ale pouze jako součást Service List. Service Record se také používá ke zrušení účasti ve službě nastavením vypršení na nulu.

Toto není LS2, ale používá standardní formát hlavičky a podpisu LS2.

Vyhledat pomocí

    n/a, see Service List
Uložit s

    Service Record type (9)
Uložit v

    Hash of service name
    This hash is then used to generate the daily "routing key", as in LS1
Typické vypršení

    Hours. Max 18.2 hours (65535 seconds)
Publikoval

    Destination

### Format

```
Standard LS2 Header as specified above

  Service Record Type-Specific Part
  - Port (2 bytes, big endian) (0 if unspecified)
  - Hash of service name (32 bytes)

  Standard LS2 Signature:
  - Signature (40+ bytes)
    The signature is of everything above.
```
### Notes

- Pokud je expires samé nuly, floodfill by měl záznam odvolat a již jej nezahrnovat do seznamu služeb.

- Úložiště: Floodfill může přísně omezovat ukládání těchto záznamů a
  limitovat počet záznamů uložených na hash a jejich expiraci. Může být také
  použit whitelist hashů.

- Jakýkoli jiný typ netdb se stejným hashem má prioritu, takže service record nikdy nemůže přepsat LS/RI, ale LS/RI přepíše všechny service records na tomto hashi.

### Service List

Toto není nic jako LS2 a používá jiný formát.

Seznam služeb je vytvořen a podepsán floodfill routerem. Je neautentizovaný v tom smyslu, že kdokoli se může připojit ke službě publikováním Service Record do floodfill routeru.

Seznam služeb obsahuje krátké záznamy služeb, nikoli úplné záznamy služeb. Tyto obsahují podpisy, ale pouze hashe, nikoli úplné destinace, takže nemohou být ověřeny bez úplné destinace.

Bezpečnost, pokud vůbec nějaká existuje, a žádoucnost seznamů služeb je TBD. Floodfilly by mohly omezit publikování a vyhledávání na whitelist služeb, ale tento whitelist se může lišit na základě implementace nebo preference operátora. Nemusí být možné dosáhnout konsenzu na společném, základním whitelistu napříč implementacemi.

Pokud je název služby zahrnut ve výše uvedeném záznamu služby, pak mohou operátoři floodfill namítat; pokud je zahrnut pouze hash, neexistuje žádné ověření a záznam služby by se mohl "dostat dovnitř" před jakýmkoli jiným typem netDb a být uložen ve floodfill.

Vyhledat pomocí

    Service List lookup type (11)
Ukládat s

    Service List type (11)
Uložit v

    Hash of service name
    This hash is then used to generate the daily "routing key", as in LS1
Typické vypršení

    Hours, not specified in the list itself, up to local policy
Publikoval

    Nobody, never sent to floodfill, never flooded.

### Format

Nepoužívá standardní LS2 hlavičku specifikovanou výše.

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
- zkontrolovat podpis upravených obsahů

Pro ověření podpisu každého Short Service Record:

- Načíst cíl
- Zkontrolovat podpis (publikované časové razítko + vypršení + příznaky + port + Hash názvu služby)

Pro ověření podpisu každého Revocation Record:

- Načíst cíl
- Zkontrolovat podpis (publikované časové razítko + 4 nulové bajty + příznaky + port + Hash
  názvu služby)

### Notes

- Používáme délku podpisu místo typu podpisu, abychom mohli podporovat neznámé typy podpisů.

- Neexistuje vypršení platnosti seznamu služeb, příjemci si mohou učinit vlastní rozhodnutí na základě zásad nebo vypršení platnosti jednotlivých záznamů.

- Seznamy služeb nejsou zaplavovány, pouze jednotlivé záznamy služeb. Každý floodfill vytváří, podepisuje a ukládá do cache Seznam služeb. Floodfill používá svou vlastní politiku pro dobu cache a maximální počet záznamů služeb a revokací.

## Common Structures Spec Changes Required

### Šifrování a zpracování

Mimo rozsah tohoto návrhu. Přidat do ECIES návrhů 144 a 145.

### New Intermediate Structures

Přidejte nové struktury pro Lease2, MetaLease, LeaseSet2Header a OfflineSignature. Platné od vydání 0.9.38.

### New NetDB Types

Přidejte struktury pro každý nový typ leaseSet, začleněné z výše uvedeného. Pro LeaseSet2, EncryptedLeaseSet a MetaLeaseSet platné od vydání 0.9.38. Pro Service Record a Service List předběžné a neplánované.

### New Signature Type

Přidat RedDSA_SHA512_Ed25519 Type 11. Veřejný klíč má 32 bajtů; soukromý klíč má 32 bajtů; hash má 64 bajtů; podpis má 64 bajtů.

## Encryption Spec Changes Required

Mimo rozsah tohoto návrhu. Viz návrhy 144 a 145.

## I2NP Changes Required

Přidat poznámku: LS2 lze publikovat pouze do floodfills s minimální verzí.

### Database Lookup Message

Přidat typ vyhledávání seznamu služeb.

### Changes

```
Flags byte: Lookup type field, currently bits 3-2, expands to bits 4-2.
  Lookup type 0x04 is defined as the service list lookup.

  Add note: Service list loookup may only be sent to floodfills with a minimum version.
  Minimum version is 0.9.38.
```
### Autorizace podle klienta

Přidejte všechny nové typy úložišť.

### Changes

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
## I2CP Changes Required

### I2CP Options

Nové možnosti interpretované na straně routeru, odeslané v mapování SessionConfig:

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
### Session Config

Poznamenejte, že pro offline podpisy jsou vyžadovány volby i2cp.leaseSetOfflineExpiration, i2cp.leaseSetTransientPublicKey a i2cp.leaseSetOfflineSignature a podpis je proveden pomocí dočasného soukromého klíče pro podepisování.

### Šifrované LS s Base 32 adresami

Router ke klientovi. Žádné změny. Leasy jsou odesílány s 8-bytovými časovými razítky, i když vrácený leaseSet bude LS2 se 4-bytovými časovými razítky. Poznamenejte, že odpověď může být zpráva Create Leaseset nebo Create Leaseset2 Message.

### Šifrované LS s offline klíči

Router ke klientovi. Žádné změny. Leases jsou odesílány s 8-bytovými časovými razítky, i když vrácený leaseSet bude LS2 se 4-bytovými časovými razítky. Vezměte na vědomí, že odpověď může být zpráva Create Leaseset nebo Create Leaseset2 Message.

### Poznámky

Klient na router. Nová zpráva, která se používá místo zprávy Create Leaseset Message.

### Meta LS2

- Aby router mohl analyzovat typ úložiště, typ musí být ve zprávě,
  pokud není předán routeru předem v konfiguraci relace.
  Pro společný kód pro analýzu je jednodušší mít jej přímo ve zprávě.

- Pro to, aby router znal typ a délku privátního klíče,
  musí být za lease setem, pokud parser nezná typ předem
  v konfiguraci relace.
  Pro společný parsing kód je jednodušší to poznat ze samotné zprávy.

- Soukromý klíč pro podepisování, dříve definovaný pro zrušení a nepoužívaný,
  není přítomen v LS2.

### Formát

Typ zprávy pro Create Leaseset2 Message je 41.

### Poznámky

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
### Záznam služby

- Minimální verze routeru je 0.9.39.
- Předběžná verze s typem zprávy 40 byla v 0.9.38, ale formát byl změněn.
  Typ 40 je opuštěn a není podporován.

### Formát

- Jsou potřebné další změny pro podporu šifrovaných a meta leaseSet.

### Poznámky

Klient ke směrovači. Nová zpráva.

### Seznam služeb

- Router potřebuje vědět, zda je cíl blinded.
  Pokud je blinded a používá tajnou nebo per-client autentifikaci,
  potřebuje mít také tyto informace.

- Vyhledání hostitele (Host Lookup) nového formátu b32 adresy ("b33")
  říká routeru, že adresa je zaslepená, ale neexistuje mechanismus pro
  předání tajného nebo soukromého klíče routeru ve zprávě Host Lookup.
  Ačkoli bychom mohli rozšířit zprávu Host Lookup o tyto informace,
  je čistší definovat novou zprávu.

- Potřebujeme programový způsob, jak může klient informovat router.
  Jinak by uživatel musel ručně konfigurovat každou destinaci.

### Formát

Před tím, než klient odešle zprávu na oslepené cílové místo, musí buď vyhledat "b33" ve zprávě Host Lookup, nebo odeslat zprávu Blinding Info. Pokud oslepené cílové místo vyžaduje tajemství nebo autentifikaci podle klienta, musí klient odeslat zprávu Blinding Info.

Router neodešle odpověď na tuto zprávu.

### Poznámky

Typ zprávy pro Blinding Info Message je 42.

### Format

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
### Certifikáty klíčů

- Minimální verze routeru je 0.9.43

### Nové mezilehlé struktury

### Nové typy NetDB

Pro podporu vyhledávání „b33" názvů hostitelů a vrácení indikace, pokud router nemá požadované informace, definujeme dodatečné kódy výsledků pro Host Reply Message, následovně:

```
2: Lookup password required
   3: Private key required
   4: Lookup password and private key required
   5: Leaseset decryption failure
```
Hodnoty 1-255 jsou již definovány jako chyby, takže nedochází k problému se zpětnou kompatibilitou.

### Nový typ podpisu

Router ke klientovi. Nová zpráva.

### Justification

Klient předem neví, že daný Hash se vyřeší na Meta LS.

Pokud vyhledání leaseset pro Destination vrátí Meta LS, router provede rekurzivní rozlišení. Pro datagramy nemusí klientská strana vědět; pro streaming však, kde protokol kontroluje cíl v SYN ACK, musí vědět, jaký je „skutečný" cíl. Proto potřebujeme novou zprávu.

### Usage

Router udržuje cache pro skutečnou destinaci, která je použita z meta LS. Když klient pošle zprávu na destinaci, která se překládá na meta LS, router zkontroluje cache pro skutečnou destinaci naposledy použitou. Pokud je cache prázdná, router vybere destinaci z meta LS a vyhledá leaseSet. Pokud je vyhledání leaseSet úspěšné, router přidá tuto destinaci do cache a pošle klientovi Meta Redirect Message. Toto se provádí pouze jednou, pokud destinace nevyprší a nemusí být změněna. Klient musí také v případě potřeby informace cachovat. Meta Redirect Message NENÍ posílána jako odpověď na každou SendMessage.

Router odesílá tuto zprávu pouze klientům s verzí 0.9.47 nebo vyšší.

Klient neposílá odpověď na tuto zprávu.

### Zpráva vyhledávání v databázi

Typ zprávy pro Meta Redirect Message je 43.

### Změny

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
### Zpráva uložení databáze

Jak generovat a podporovat Meta, včetně komunikace a koordinace mezi routery, je mimo rozsah tohoto návrhu. Viz související návrh 150.

### Změny

Offline podpisy nelze ověřit ve streaming nebo odpověditelných datagramech. Viz sekce níže.

## Private Key File Changes Required

Formát souboru s privátním klíčem (eepPriv.dat) není oficiální součástí našich specifikací, ale je zdokumentován v [Java I2P javadocs](http://idk.i2p/javadoc-i2p/net/i2p/data/PrivateKeyFile.html) a jiné implementace jej podporují. To umožňuje přenositelnost privátních klíčů mezi různými implementacemi.

Změny jsou nezbytné pro uložení dočasného veřejného klíče a informací o offline podepisování.

### Changes

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
### Možnosti I2CP

Přidejte podporu pro následující možnosti:

```
-d days              (specify expiration in days of offline sig, default 365)
      -o offlinedestfile   (generate the online key file,
                            using the offline key file specified)
      -r sigtype           (specify sig type of transient key, default Ed25519)
```
## Streaming Changes Required

Offline podpisy momentálně nelze ověřit ve streaming. Níže uvedená změna přidává blok offline podepisování do možností. Tím se zabrání nutnosti získávat tyto informace přes I2CP.

### Konfigurace relace

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
### Zpráva Request Leaseset

- Alternativou je pouze přidat příznak a získat přechodný veřejný klíč přes I2CP
  (Viz sekce Host Lookup / Host Reply Message výše)

## Standardní LS2 hlavička

Offline podpisy nelze ověřit při zpracování odpověditelných datagramů. Je potřeba příznak pro označení offline podepsaného, ale není místo, kam příznak umístit. Bude vyžadovat úplně nové číslo protokolu a formát.

### Zpráva požadavku na proměnný leaseSet

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
### Vytvořit zprávu Leaseset2

- Alternativou je pouze přidat příznak a získat přechodný veřejný klíč přes I2CP
  (Viz sekce Host Lookup / Host Reply Message výše)
- Měli bychom nyní přidat nějaké další možnosti, když máme flag byty?

## SAM V3 Changes Required

SAM musí být rozšířen o podporu offline podpisů v DESTINATION base 64.

### Odůvodnění

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
Poznámka: offline podpisy jsou podporovány pouze pro STREAM a RAW, nikoli pro DATAGRAM (dokud nedefinujeme nový DATAGRAM protokol).

Všimněte si, že SESSION STATUS vrátí Signing Private Key obsahující samé nuly a data Offline Signature přesně tak, jak byla zadána v SESSION CREATE.

Poznámka: DEST GENERATE a SESSION CREATE DESTINATION=TRANSIENT nelze použít k vytvoření offline podepsané destinace.

### Typ zprávy

Zvýšit verzi na 3.4, nebo ji nechat na 3.1/3.2/3.3, aby mohla být přidána bez nutnosti všech těch věcí z 3.2/3.3?

Další změny budou upřesněny. Viz sekce I2CP Host Reply Message výše.

## BOB Changes Required

BOB by musel být rozšířen o podporu offline podpisů a/nebo Meta LS. Toto má nízkou prioritu a pravděpodobně nikdy nebude specifikováno nebo implementováno. SAM V3 je preferované rozhraní.

## Publishing, Migration, Compatibility

LS2 (kromě šifrovaných LS2) je publikován na stejném DHT místě jako LS1. Neexistuje způsob, jak publikovat současně LS1 i LS2, pokud by LS2 nebylo na jiném místě.

Šifrovaný LS2 je publikován na hash blinded key typu a klíčových dat. Tento hash je pak použit k vygenerování denního "routing key", stejně jako u LS1.

LS2 by se používalo pouze když jsou požadovány nové funkce (nové krypto, šifrované LS, meta, atd.). LS2 lze publikovat pouze na floodfill uzly určené verze nebo vyšší.

Servery publikující LS2 by věděly, že všichni připojující se klienti podporují LS2. Mohly by poslat LS2 v garlic encryption.

Klienti by posílali LS2 v garlics pouze při použití nové kryptografie. Sdílení klienti by používali LS1 neomezeně? TODO: Jak mít sdílené klienty, které podporují starou i novou kryptografii?

## Rollout

0.9.38 obsahuje floodfill podporu pro standardní LS2, včetně offline klíčů.

0.9.39 obsahuje I2CP podporu pro LS2 a Encrypted LS2, podepisování/ověřování sig typu 11, floodfill podporu pro Encrypted LS2 (sig typy 7 a 11, bez offline klíčů) a šifrování/dešifrování LS2 (bez autorizace podle klienta).

0.9.40 má podle plánu obsahovat podporu pro šifrování/dešifrování LS2 s autorizací podle klienta, floodfill a I2CP podporu pro Meta LS2, podporu pro šifrované LS2 s offline klíči a b32 podporu pro šifrované LS2.

## Nové typy DatabaseEntry

Návrh šifrovaného LS2 je silně ovlivněn [deskriptory skrytých služeb v3 sítě Tor](https://spec.torproject.org/rend-spec-v3), které měly podobné návrhové cíle.
