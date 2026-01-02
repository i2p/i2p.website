---
title: "ECIES-X25519-AEAD-Ratchet"
number: "144"
author: "zzz, chisana, orignal"
created: "2018-11-22"
lastupdated: "2025-03-05"
status: "Zavřeno"
thread: "http://zzz.i2p/topics/2639"
target: "0.9.46"
implementedin: "0.9.46"
toc: true
---

## Poznámka

Nasazení sítě a testování probíhá. Může podléhat menším revizím. Viz [SPEC](/docs/specs/ecies/) pro oficiální specifikaci.

Následující funkce nejsou implementovány od verze 0.9.46:

- Bloky MessageNumbers, Options a Termination
- Odpovědi na protokolové vrstvě
- Nulový statický klíč
- Multicast

## Přehled

Toto je návrh prvního nového typu end-to-end šifrování od začátků I2P, který má nahradit ElGamal/AES+SessionTags [Elg-AES](/docs/legacy/elgamal-aes/).

Vychází z předchozí práce následovně:

- Specifikace společných struktur [Common Structures](/docs/specs/common-structures/)
- Specifikace [I2NP](/docs/specs/i2np/) včetně LS2
- ElGamal/AES+Session Tags [Elg-AES](/docs/legacy/elgamal-aes/)
- [http://zzz.i2p/topics/1768](http://zzz.i2p/topics/1768) přehled nové asymetrické kryptografie
- Nízkoúrovňový přehled kryptografie [CRYPTO-ELG](/docs/specs/cryptography/)
- ECIES [http://zzz.i2p/topics/2418](http://zzz.i2p/topics/2418)
- [NTCP2](/docs/specs/ntcp2/) [Proposal 111](/proposals/111-ntcp-2/)
- 123 Nové položky netDB
- 142 Nová kryptografická šablona
- Protokol [Noise](https://noiseprotocol.org/noise.html)
- Algoritmus [Signal](https://signal.org/docs/) double ratchet

Cílem je podpořit nové šifrování pro end-to-end komunikaci mezi destinacemi.

Design bude používat Noise handshake a datovou fázi zahrnující Signal double ratchet.

Všechny odkazy na Signal a Noise v tomto návrhu slouží pouze pro základní informace. Znalost protokolů Signal a Noise není vyžadována pro pochopení nebo implementaci tohoto návrhu.

### Current ElGamal Uses

Jako přehled, ElGamal 256-bajtové veřejné klíče mohou být nalezeny v následujících datových strukturách. Viz specifikace běžných struktur.

- V Router Identity
  Toto je šifrovací klíč routeru.

- V Destination
  Veřejný klíč destinace byl používán pro staré i2cp-to-i2cp šifrování,
  které bylo zakázáno ve verzi 0.6, aktuálně se nepoužívá kromě
  IV pro LeaseSet šifrování, které je zastaralé.
  Místo toho se používá veřejný klíč v LeaseSet.

- V LeaseSet
  Toto je šifrovací klíč cíle.

- V LS2
  Toto je šifrovací klíč cíle.

### EncTypes in Key Certs

Jako shrnutí, přidali jsme podporu pro typy šifrování, když jsme přidali podporu pro typy podpisů. Pole typu šifrování je vždy nula, jak v Destinations, tak v RouterIdentities. Zda to někdy změnit, je TBD. Viz specifikace běžných struktur [Common Structures](/docs/specs/common-structures/).

### Současné použití ElGamal

Jako shrnutí, používáme ElGamal pro:

1) Zprávy Tunnel Build (klíč je v RouterIdentity)    Náhrada není pokryta v tomto návrhu.    Viz návrh 152 [Proposal 152](/proposals/152-ecies-tunnels).

2) Router-to-router šifrování netDb a dalších I2NP zpráv (Klíč je v RouterIdentity)    Závisí na tomto návrhu.    Vyžaduje návrh také pro 1), nebo umístění klíče do RI možností.

3) Klientské End-to-end ElGamal+AES/SessionTag (klíč je v LeaseSet, klíč Destination se nepoužívá)    Náhrada JE pokryta v tomto návrhu.

4) Dočasný DH pro NTCP1 a SSU    Náhrada není pokryta v tomto návrhu.    Viz návrh 111 pro NTCP2.    Žádný současný návrh pro SSU2.

### EncTypes v Key Certs

- Zpětně kompatibilní
- Vyžaduje a staví na LS2 (návrh 123)
- Využívá novou kryptografii nebo primitiva přidaná pro NTCP2 (návrh 111)
- Žádná nová kryptografie nebo primitiva nejsou vyžadována pro podporu
- Zachovává oddělení kryptografie a podepisování; podporuje všechny současné i budoucí verze
- Umožňuje novou kryptografii pro destinace
- Umožňuje novou kryptografii pro routery, ale pouze pro garlic zprávy - budování tunelů
  by bylo samostatným návrhem
- Nerozbíjí nic, co spoléhá na 32-bajtové binární hashe destinací, např. bittorrent
- Zachovává 0-RTT doručování zpráv pomocí ephemeral-static DH
- Nevyžaduje ukládání do vyrovnávací paměti / řazení zpráv do fronty na této protokolové vrstvě;
  pokračuje v podpoře neomezeného doručování zpráv v obou směrech bez čekání na odpověď
- Upgraduje na ephemeral-ephemeral DH po 1 RTT
- Zachovává zpracování zpráv mimo pořadí
- Zachovává 256-bitové zabezpečení
- Přidává forward secrecy
- Přidává autentifikaci (AEAD)
- Mnohem více CPU-efektivní než ElGamal
- Nespoléhá na Java jbigi pro efektivní DH
- Minimalizuje DH operace
- Mnohem více šířka-pásmově efektivní než ElGamal (514 bajtový ElGamal blok)
- Podporuje novou i starou kryptografii na stejném tunelu podle potřeby
- Příjemce je schopen efektivně rozlišit novou od staré kryptografie přicházející
  stejným tunelem
- Ostatní nemohou rozlišit novou od staré nebo budoucí kryptografie
- Eliminuje klasifikaci délky Nové vs. Existující Session (podporuje padding)
- Žádné nové I2NP zprávy nejsou vyžadovány
- Nahrazuje SHA-256 kontrolní součet v AES payload pomocí AEAD
- Podporuje svázání transmitujících a přijímajících sessions tak, aby
  potvrzování mohlo probíhat v rámci protokolu, spíše než pouze out-of-band.
  To také umožní odpovědím mít forward secrecy okamžitě.
- Umožňuje end-to-end šifrování určitých zpráv (RouterInfo stores),
  které v současnosti neděláme kvůli CPU zátěži.
- Nemění I2NP Garlic Message
  nebo formát Garlic Message Delivery Instructions.
- Eliminuje nepoužívaná nebo redundantní pole ve formátech Garlic Clove Set a Clove.

Eliminuje několik problémů se session tagy, včetně:

- Nemožnost použít AES až do první odpovědi
- Nespolehlivost a zasekávání při předpokládané dodávce tagů
- Neefektivní využití šířky pásma, zejména při první dodávce
- Obrovská neefektivnost prostoru pro ukládání tagů
- Obrovská režie šířky pásma pro dodávání tagů
- Vysoce složité, obtížné implementovat
- Obtížné vyladit pro různé případy použití
  (streaming vs. datagramy, server vs. klient, vysoká vs. nízká šířka pásma)
- Zranitelnosti vyčerpání paměti kvůli dodávání tagů

### Použití asymetrické kryptografie

- Změny formátu LS2 (návrh 123 je dokončen)
- Nový algoritmus rotace DHT nebo generování sdíleného náhodného čísla
- Nové šifrování pro budování tunelů.
  Viz návrh 152 [Proposal 152](/proposals/152-ecies-tunnels).
- Nové šifrování pro šifrování vrstvy tunelu.
  Viz návrh 153 [Proposal 153](/proposals/153-chacha20-layer-encryption).
- Metody šifrování, přenosu a příjmu I2NP DLM / DSM / DSRM zpráv.
  Bez změn.
- Komunikace LS1-na-LS2 nebo ElGamal/AES-na-tento-návrh není podporována.
  Tento návrh je obousměrný protokol.
  Destinace mohou zvládat zpětnou kompatibilitu publikováním dvou leasesetů
  používajících stejné tunely, nebo vložením obou typů šifrování do LS2.
- Změny modelu hrozeb
- Detaily implementace zde nejsou diskutovány a jsou ponechány každému projektu.
- (Optimisticky) Přidat rozšíření nebo háčky pro podporu multicastu

### Cíle

ElGamal/AES+SessionTag byl naším jediným end-to-end protokolem přibližně 15 let, v podstatě bez úprav protokolu. Nyní existují kryptografické primitivy, které jsou rychlejší. Potřebujeme zvýšit bezpečnost protokolu. Také jsme vyvinuli heuristické strategie a náhradní řešení pro minimalizaci paměťové a šířkové režie protokolu, ale tyto strategie jsou křehké, obtížně nastavitelné a činí protokol ještě náchylnějším k poruchám, což způsobuje ukončení relace.

Po přibližně stejné časové období specifikace ElGamal/AES+SessionTag a související dokumentace popisovaly, jak nákladné z hlediska šířky pásma je doručování session tagů, a navrhly nahradit doručování session tagů "synchronizovaným PRNG". Synchronizovaný PRNG deterministicky generuje stejné tagy na obou koncích, odvozené ze společného seedu. Synchronizovaný PRNG lze také nazvat "ratchet". Tento návrh (konečně) specifikuje daný ratchet mechanismus a eliminuje doručování tagů.

Použitím ratchet mechanismu (synchronizovaný PRNG) pro generování session tagů eliminujeme režii odesílání session tagů ve zprávě New Session a následujících zprávách, když jsou potřeba. Pro typickou sadu tagů o 32 tazích to představuje 1KB. Toto také eliminuje ukládání session tagů na straně odesílatele, čímž se požadavky na úložiště snižují na polovinu.

K zabránění útokům typu Key Compromise Impersonation (KCI) je potřeba úplný obousměrný handshake, podobný vzoru Noise IK. Viz tabulka "Payload Security Properties" v [NOISE](https://noiseprotocol.org/noise.html). Pro více informací o KCI viz článek https://www.usenix.org/system/files/conference/woot15/woot15-paper-hlauschek.pdf

### Necíle / Mimo rozsah

Model hrozeb se poněkud liší od modelu pro NTCP2 (návrh 111). MitM uzly jsou OBEP a IBGW a předpokládá se, že mají úplný přehled o současné nebo historické globální NetDB prostřednictvím spolupráce s floodfill uzly.

Cílem je zabránit těmto MitM útočníkům v klasifikaci provozu jako zprávy nové a existující relace, nebo jako nové krypto vs. staré krypto.

## Detailed Proposal

Tento návrh definuje nový end-to-end protokol pro nahrazení ElGamal/AES+SessionTags. Design bude používat Noise handshake a datovou fázi zahrnující Signal's double ratchet.

### Odůvodnění

Existuje pět částí protokolu, které je třeba přepracovat:

- 1) Nové a stávající formáty kontejnerů Session
  jsou nahrazeny novými formáty.
- 2) ElGamal (256 bajtové veřejné klíče, 128 bajtové soukromé klíče) je nahrazen
  ECIES-X25519 (32 bajtové veřejné a soukromé klíče)
- 3) AES je nahrazen
  AEAD_ChaCha20_Poly1305 (zkráceně ChaChaPoly níže)
- 4) SessionTags budou nahrazeny ratchets,
  což je v podstatě kryptografický, synchronizovaný PRNG.
- 5) AES payload, jak je definován ve specifikaci ElGamal/AES+SessionTags,
  je nahrazen blokovým formátem podobným tomu v NTCP2.

Každá z pěti změn má níže svou vlastní sekci.

### Model hrozeb

Stávající implementace I2P routeru budou vyžadovat implementace následujících standardních kryptografických primitiv, které nejsou vyžadovány pro současné I2P protokoly:

- ECIES (ale toto je v podstatě X25519)
- Elligator2

Stávající implementace I2P routeru, které ještě neimplementovaly [NTCP2](/docs/specs/ntcp2/) ([Proposal 111](/proposals/111-ntcp-2/)), budou také vyžadovat implementace pro:

- Generování klíčů X25519 a DH
- AEAD_ChaCha20_Poly1305 (zkráceno jako ChaChaPoly níže)
- HKDF

### Crypto Type

Typ kryptografie (použitý v LS2) je 4. To označuje little-endian 32-bajtový X25519 veřejný klíč a end-to-end protokol specifikovaný zde.

Crypto type 0 je ElGamal. Crypto types 1-3 jsou vyhrazeny pro ECIES-ECDH-AES-SessionTag, viz návrh 145 [Proposal 145](/proposals/145-ecies).

### Shrnutí kryptografického návrhu

Tento návrh poskytuje požadavky založené na Noise Protocol Framework [NOISE](https://noiseprotocol.org/noise.html) (Revize 34, 2018-07-11). Noise má podobné vlastnosti jako protokol Station-To-Station [STS](https://en.wikipedia.org/wiki/Station-to-Station_protocol), který je základem pro protokol [SSU](/docs/legacy/ssu/). V terminologii Noise je Alice iniciátor a Bob je respondent.

Tento návrh je založen na protokolu Noise Noise_IK_25519_ChaChaPoly_SHA256. (Skutečný identifikátor pro počáteční funkci odvození klíčů je "Noise_IKelg2_25519_ChaChaPoly_SHA256" pro označení rozšíření I2P - viz sekce KDF 1 níže) Tento protokol Noise používá následující primitiva:

- Interactive Handshake Pattern: IK
  Alice okamžitě přenáší svůj statický klíč Bobovi (I)
  Alice už zná Bobův statický klíč (K)

- One-Way Handshake Pattern: N
  Alice nepřenáší svůj statický klíč Bobovi (N)

- DH Function: X25519
  X25519 DH s délkou klíče 32 bajtů jak je specifikováno v [RFC-7748](https://tools.ietf.org/html/rfc7748).

- Cipher Function: ChaChaPoly
  AEAD_CHACHA20_POLY1305 jak je specifikováno v [RFC-7539](https://tools.ietf.org/html/rfc7539) sekce 2.8.
  12bytový nonce, s prvními 4 byty nastavenými na nulu.
  Identické s tím v [NTCP2](/docs/specs/ntcp2/).

- Hash Function: SHA256
  Standardní 32-bajtový hash, již extensively používaný v I2P.

### Nové kryptografické primitiva pro I2P

Tento návrh definuje následující vylepšení pro Noise_IK_25519_ChaChaPoly_SHA256. Obecně se řídí pokyny v [NOISE](https://noiseprotocol.org/noise.html) sekci 13.

1) Klíče cleartext ephemeral jsou kódovány pomocí [Elligator2](https://elligator.cr.yp.to/).

2) Odpověď je opatřena prefixem v podobě cleartext tagu.

3) Formát payload je definován pro zprávy 1, 2 a datovou fázi. To samozřejmě není definováno v Noise.

Všechny zprávy obsahují hlavičku [I2NP](/docs/specs/i2np/) Garlic Message. Datová fáze používá šifrování podobné, ale nekompatibilní s datovou fází Noise.

### Typ šifrování

Handshaky používají [Noise](https://noiseprotocol.org/noise.html) handshake vzory.

Používá se následující mapování písmen:

- e = jednorázový dočasný klíč
- s = statický klíč
- p = obsah zprávy

Jednorázové a Unbound relace jsou podobné Noise N vzoru.

```

<- s
  ...
  e es p ->

```
Bound sessions jsou podobné Noise IK patternu.

```

<- s
  ...
  e es s ss p ->
  <- tag e ee se
  <- p
  p ->

```
### Noise Protocol Framework

Současný protokol ElGamal/AES+SessionTag je jednosměrný. Na této vrstvě příjemce neví, odkud zpráva pochází. Odchozí a příchozí relace nejsou spojené. Potvrzení probíhají mimo hlavní pásmo pomocí DeliveryStatusMessage (zabaleného v GarlicMessage) v segmentu clove.

Jednosměrný protokol přináší značnou neefektivnost. Jakákoliv odpověď musí také použít nákladnou zprávu 'New Session'. To způsobuje vyšší spotřebu šířky pásma, CPU a paměti.

Existují také bezpečnostní slabiny v jednosměrném protokolu. Všechny relace jsou založeny na ephemeral-static DH. Bez návratové cesty neexistuje způsob, jak by Bob mohl "přepnout" svůj statický klíč na ephemeral klíč. Aniž by věděl, odkud zpráva pochází, neexistuje způsob, jak použít přijatý ephemeral klíč pro odchozí zprávy, takže i počáteční odpověď používá ephemeral-static DH.

Pro tento návrh definujeme dva mechanismy pro vytvoření obousměrného protokolu - "párování" a "vazbu". Tyto mechanismy poskytují zvýšenou efektivitu a bezpečnost.

### Doplňky k frameworku

Stejně jako u ElGamal/AES+SessionTags, všechny příchozí a odchozí relace musí být v daném kontextu, buď v kontextu routeru nebo v kontextu pro konkrétní místní cíl. V Java I2P se tento kontext nazývá Session Key Manager.

Relace nesmí být sdíleny mezi kontexty, protože by to umožnilo korelaci mezi různými místními cíli nebo mezi místním cílem a routerem.

Když daná destinace podporuje jak ElGamal/AES+SessionTags, tak i tento návrh, oba typy relací mohou sdílet kontext. Viz sekce 1c) níže.

### Vzory handshaku

Když je u původce (Alice) vytvořena odchozí relace, je vytvořena nová příchozí relace a spárována s odchozí relací, pokud se neočekává odpověď (např. surové datagramy).

Nová příchozí relace je vždy spárována s novou odchozí relací, pokud není požadována žádná odpověď (např. raw datagramy).

Pokud je požadována odpověď a je vázána na vzdálený cíl nebo router, tato nová odchozí relace je vázána na tento cíl nebo router a nahrazuje jakoukoli předchozí odchozí relaci k tomuto cíli nebo routeru.

Párování příchozích a odchozích relací poskytuje obousměrný protokol se schopností ratchetingu DH klíčů.

### Relace

K dané destinaci nebo routeru existuje pouze jedna odchozí relace. Může existovat několik aktuálních příchozích relací od dané destinace nebo routeru. Obecně platí, že když je vytvořena nová příchozí relace a na této relaci je přijat provoz (což slouží jako ACK), ostatní budou označeny k vypršení relativně rychle, během minuty nebo tak nějak. Je zkontrolována hodnota předchozích odeslaných zpráv (PN), a pokud v předchozí příchozí relaci nejsou žádné nepřijaté zprávy (v rámci velikosti okna), předchozí relace může být okamžitě smazána.

Když je u odesílatele (Alice) vytvořena odchozí relace, je svázána se vzdáleným Destination (Bob) a jakákoli spárovaná příchozí relace bude také svázána se vzdáleným Destination. Jak se relace přepínají, zůstávají nadále svázané se vzdáleným Destination.

Když je na příjemci (Bob) vytvořena inbound session, může být navázána na vzdálený Destination (Alice), dle volby Alice. Pokud Alice zahrne informace o navázání (svůj statický klíč) do zprávy New Session, session bude navázána na tento destination a bude vytvořena outbound session navázaná na stejný Destination. Jak se sessions ratchet, zůstávají navázány na vzdálený Destination.

### Kontext relace

Pro běžný případ streamování očekáváme, že Alice a Bob budou protokol používat následovně:

- Alice páruje svou novou odchozí relaci s novou příchozí relací, obě vázané k cílové destinaci na druhém konci (Bob).
- Alice zahrnuje informace o párování a podpis, a požadavek na odpověď, do
  zprávy New Session odeslané Bobovi.
- Bob páruje svou novou příchozí relaci s novou odchozí relací, obě vázané k cílové destinaci na druhém konci (Alice).
- Bob pošle odpověď (ack) Alici ve spárované relaci, s ratchet na nový DH klíč.
- Alice provede ratchet na novou odchozí relaci s Bobovým novým klíčem, spárovanou se stávající příchozí relací.

Vázáním příchozí relace na vzdálený Destination a spárováním příchozí relace s odchozí relací vázanou na stejný Destination dosahujeme dvou hlavních výhod:

1) Počáteční odpověď od Boba k Alici používá ephemeral-ephemeral DH

2) Poté, co Alice obdrží Bobovu odpověď a provede ratchet, všechny následující zprávy od Alice k Bobovi používají efemérní-efemérní DH.

### Párování příchozích a odchozích relací

V ElGamal/AES+SessionTags, když je LeaseSet zabalen jako garlic clove, nebo jsou doručeny tagy, odesílající router požaduje ACK. Toto je samostatná garlic clove obsahující DeliveryStatus Message. Pro dodatečnou bezpečnost je DeliveryStatus Message zabalena v Garlic Message. Tento mechanismus je z pohledu protokolu out-of-band.

V novém protokolu, jelikož jsou příchozí a odchozí relace spárovány, můžeme mít ACK přímo v pásmu. Není potřeba samostatný clove.

Explicitní ACK je jednoduše zpráva Existing Session bez I2NP bloku. Ve většině případů se však explicitnímu ACK lze vyhnout, protože existuje zpětný provoz. Pro implementace může být žádoucí chvíli počkat (možná sto ms) před odesláním explicitního ACK, aby měla streaming nebo aplikační vrstva čas odpovědět.

Implementace budou také muset odložit jakékoliv odesílání ACK až po zpracování I2NP bloku, protože Garlic Message může obsahovat Database Store Message s lease setem. Aktuální lease set bude nezbytný pro směrování ACK a cílová destinace na vzdáleném konci (obsažená v lease setu) bude nezbytná pro ověření vazebného statického klíče.

### Vazba relací a destinací

Odchozí relace by měly vždy vypršet před příchozími relacemi. Jakmile odchozí relace vyprší a vytvoří se nová, vytvoří se také nová spárovaná příchozí relace. Pokud existovala stará příchozí relace, bude jí umožněno vypršet.

### Výhody Bindingu a Párování

TBD

### Potvrzení zpráv

Definujeme následující funkce odpovídající použitým kryptografickým stavebním blokům.

ZEROLEN

    zero-length byte array

CSRNG(n)

    n-byte output from a cryptographically-secure random number generator.

H(p, d)

    SHA-256 hash function that takes a personalization string p and data d, and
    produces an output of length 32 bytes.
    As defined in [NOISE](https://noiseprotocol.org/noise.html).
    || below means append.

    Use SHA-256 as follows::

        H(p, d) := SHA-256(p || d)

MixHash(d)

    SHA-256 hash function that takes a previous hash h and new data d,
    and produces an output of length 32 bytes.
    || below means append.

    Use SHA-256 as follows::

        MixHash(d) := h = SHA-256(h || d)

STREAM

    The ChaCha20/Poly1305 AEAD as specified in [RFC-7539](https://tools.ietf.org/html/rfc7539).
    S_KEY_LEN = 32 and S_IV_LEN = 12.

    ENCRYPT(k, n, plaintext, ad)
        Encrypts plaintext using the cipher key k, and nonce n which MUST be unique for
        the key k.
        Associated data ad is optional.
        Returns a ciphertext that is the size of the plaintext + 16 bytes for the HMAC.

        The entire ciphertext must be indistinguishable from random if the key is secret.

    DECRYPT(k, n, ciphertext, ad)
        Decrypts ciphertext using the cipher key k, and nonce n.
        Associated data ad is optional.
        Returns the plaintext.

DH

    X25519 public key agreement system. Private keys of 32 bytes, public keys of 32
    bytes, produces outputs of 32 bytes. It has the following
    functions:

    GENERATE_PRIVATE()
        Generates a new private key.

    DERIVE_PUBLIC(privkey)
        Returns the public key corresponding to the given private key.

    GENERATE_PRIVATE_ELG2()
        Generates a new private key that maps to a public key suitable for Elligator2 encoding.
        Note that half of the randomly-generated private keys will not be suitable and must be discarded.

    ENCODE_ELG2(pubkey)
        Returns the Elligator2-encoded public key corresponding to the given public key (inverse mapping).
        Encoded keys are little endian.
        Encoded key must be 256 bits indistinguishable from random data.
        See Elligator2 section below for specification.

    DECODE_ELG2(pubkey)
        Returns the public key corresponding to the given Elligator2-encoded public key.
        See Elligator2 section below for specification.

    DH(privkey, pubkey)
        Generates a shared secret from the given private and public keys.

HKDF(salt, ikm, info, n)

    A cryptographic key derivation function which takes some input key material ikm (which
    should have good entropy but is not required to be a uniformly random string), a salt
    of length 32 bytes, and a context-specific 'info' value, and produces an output
    of n bytes suitable for use as key material.

    Use HKDF as specified in [RFC-5869](https://tools.ietf.org/html/rfc5869), using the HMAC hash function SHA-256
    as specified in [RFC-2104](https://tools.ietf.org/html/rfc2104). This means that SALT_LEN is 32 bytes max.

MixKey(d)

    Use HKDF() with a previous chainKey and new data d, and
    sets the new chainKey and k.
    As defined in [NOISE](https://noiseprotocol.org/noise.html).

    Use HKDF as follows::

        MixKey(d) := output = HKDF(chainKey, d, "", 64)
                     chainKey = output[0:31]
                     k = output[32:63]


### Časové limity relace

### Multicast

Garlic Message jak je specifikována v [I2NP](/docs/specs/i2np/) je následující. Jelikož cílem designu je, že zprostředkující uzly nemohou rozlišit novou od staré kryptografie, tento formát se nemůže změnit, i když pole délky je nadbytečné. Formát je zobrazen s úplnou 16-bytovou hlavičkou, ačkoli skutečná hlavička může být v jiném formátu v závislosti na použitém transportu.

Když jsou data dešifrována, obsahují sérii Garlic Cloves a dodatečná data, také známá jako Clove Set.

Podrobnosti a úplnou specifikaci najdete v [I2NP](/docs/specs/i2np/).

```

+----+----+----+----+----+----+----+----+
  |type|      msg_id       |  expiration
  +----+----+----+----+----+----+----+----+
                           |  size   |chks|
  +----+----+----+----+----+----+----+----+
  |      length       |                   |
  +----+----+----+----+                   +
  |          encrypted data               |
  ~                                       ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

```
### Definice

Současný formát zpráv, používaný více než 15 let, je ElGamal/AES+SessionTags. V ElGamal/AES+SessionTags existují dva formáty zpráv:

1) Nová relace: - 514 bajtový ElGamal blok - AES blok (minimálně 128 bajtů, násobek 16)

2) Existující relace: - 32 bajtový Session Tag - AES blok (minimálně 128 bajtů, násobek 16)

Minimální padding na 128 je implementován v Java I2P, ale není vynucován při příjmu.

Tyto zprávy jsou zapouzdřeny v I2NP garlic zprávě, která obsahuje pole délky, takže délka je známa.

Poznamenejte, že není definováno žádné vyplnění na délku, která není násobkem 16, takže New Session je vždy (mod 16 == 2) a Existing Session je vždy (mod 16 == 0). Toto je třeba opravit.

Příjemce se nejprve pokusí vyhledat prvních 32 bajtů jako Session Tag. Pokud je nalezen, dešifruje AES blok. Pokud není nalezen a data jsou dlouhá alespoň (514+16), pokusí se dešifrovat ElGamal blok, a pokud je úspěšný, dešifruje AES blok.

### 1) Formát zprávy

V Signal Double Ratchet hlavička obsahuje:

- DH: Aktuální veřejný klíč ratchetu
- PN: Délka zprávy předchozího řetězce
- N: Číslo zprávy

Signal-ovy "sending chains" jsou zhruba ekvivalentní našim tag setům. Použitím session tagu můžeme většinu z toho eliminovat.

V New Session vkládáme pouze veřejný klíč do nešifrované hlavičky.

V Existing Session používáme session tag pro záhlaví. Session tag je asociován s aktuálním ratchet veřejným klíčem a číslem zprávy.

V obou případech nové i existující relace jsou PN a N v zašifrovaném těle.

V Signalu se věci neustále ratchetují. Nový DH veřejný klíč vyžaduje, aby příjemce provedl ratchet a poslal zpět nový veřejný klíč, což také slouží jako potvrzení pro přijatý veřejný klíč. To by pro nás bylo příliš mnoho DH operací. Proto oddělujeme potvrzení přijatého klíče a přenos nového veřejného klíče. Jakákoli zpráva používající session tag vygenerovaný z nového DH veřejného klíče představuje ACK. Nový veřejný klíč přenášíme pouze tehdy, když si přejeme provést rekey.

Maximální počet zpráv před tím, než se musí DH přepnout, je 65535.

Při doručování session key z něj odvozujeme „Tag Set", místo abychom museli doručovat také session tags. Tag Set může obsahovat až 65536 tagů. Příjemci by však měli implementovat strategii „look-ahead", místo generování všech možných tagů najednou. Generujte maximálně N tagů za posledním správně přijatým tagem. N může být nejvýše 128, ale 32 nebo dokonce méně může být lepší volbou.

### Přehled současného formátu zpráv

Nová relace jednorázový veřejný klíč (32 bytů) Šifrovaná data a MAC (zbývající byty)

Zpráva New Session může nebo nemusí obsahovat statický veřejný klíč odesílatele. Pokud je zahrnut, reverzní relace je vázána na tento klíč. Statický klíč by měl být zahrnut, pokud se očekávají odpovědi, tj. pro streaming a odpovídatelné datagramy. Neměl by být zahrnut pro surové datagramy.

Zpráva New Session je podobná jednosměrnému Noise [NOISE](https://noiseprotocol.org/noise.html) vzoru "N" (pokud se statický klíč neposílá), nebo obousměrnému vzoru "IK" (pokud se statický klíč posílá).

### Přehled formátu šifrovaných dat

Délka je 96 + délka payload. Šifrovaný formát:

```

+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   New Session Ephemeral Public Key    |
  +             32 bytes                  +
  |     Encoded with Elligator2           |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +         Static Key                    +
  |       ChaCha20 encrypted data         |
  +            32 bytes                   +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +    (MAC) for Static Key Section       +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |       ChaCha20 encrypted data         |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) for Payload Section     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  Public Key :: 32 bytes, little endian, Elligator2, cleartext

  Static Key encrypted data :: 32 bytes

  Payload Section encrypted data :: remaining data minus 16 bytes

  MAC :: Poly1305 message authentication code, 16 bytes

```
### Nové Session Tags a porovnání se Signal

Efemérní klíč má 32 bajtů a je kódován pomocí Elligator2. Tento klíč se nikdy znovu nepoužívá; nový klíč se generuje pro každou zprávu, včetně opakovaných přenosů.

### 1a) Nový formát relace

Po dešifrování, statický X25519 klíč Alice, 32 bajtů.

### 1b) Nový formát relace (s vazbou)

Délka šifrovaných dat je zbytek dat. Délka dešifrovaných dat je o 16 menší než délka šifrovaných dat. Payload musí obsahovat blok DateTime a obvykle bude obsahovat jeden nebo více bloků Garlic Clove. Formát a další požadavky najdete v sekci payload níže.

### Nový dočasný klíč relace

Pokud není vyžadována odpověď, žádný statický klíč se neposílá.

Délka je 96 + délka payload. Šifrovaný formát:

```

+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   New Session Ephemeral Public Key    |
  +             32 bytes                  +
  |     Encoded with Elligator2           |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +           Flags Section               +
  |       ChaCha20 encrypted data         |
  +            32 bytes                   +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) for above section       +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |       ChaCha20 encrypted data         |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) for Payload Section     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  Public Key :: 32 bytes, little endian, Elligator2, cleartext

  Flags Section encrypted data :: 32 bytes

  Payload Section encrypted data :: remaining data minus 16 bytes

  MAC :: Poly1305 message authentication code, 16 bytes

```
### Statický klíč

Alicin dočasný klíč. Dočasný klíč má 32 bajtů, kódovaný pomocí Elligator2, little endian. Tento klíč se nikdy znovu nepoužije; nový klíč se generuje s každou zprávou, včetně opakovaných přenosů.

### Datová část

Sekce Flags neobsahuje nic. Má vždy 32 bajtů, protože musí mít stejnou délku jako statický klíč pro zprávy New Session s vazbou. Bob určuje, zda se jedná o statický klíč nebo sekci flags tím, že testuje, zda jsou všechny 32 bajty nulové.

TODO nějaké flagy potřebné zde?

### 1c) Nový formát relace (bez vazby)

Délka šifrovaných dat je zbytek dat. Délka dešifrovaných dat je o 16 menší než délka šifrovaných dat. Payload musí obsahovat blok DateTime a obvykle bude obsahovat jeden nebo více bloků Garlic Clove. Formát a další požadavky najdete v sekci payload níže.

### Nový dočasný klíč relace

Pokud se očekává odeslání pouze jedné zprávy, není nutné nastavení relace ani statický klíč.

Délka je 96 + délka payload. Šifrovaný formát:

```

+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |       Ephemeral Public Key            |
  +             32 bytes                  +
  |     Encoded with Elligator2           |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +           Flags Section               +
  |       ChaCha20 encrypted data         |
  +            32 bytes                   +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) for above section       +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |       ChaCha20 encrypted data         |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) for Payload Section     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  Public Key :: 32 bytes, little endian, Elligator2, cleartext

  Flags Section encrypted data :: 32 bytes

  Payload Section encrypted data :: remaining data minus 16 bytes

  MAC :: Poly1305 message authentication code, 16 bytes

```
### Sekce příznaků Dešifrovaná data

Jednorázový klíč má 32 bytů, kódovaný pomocí Elligator2, little endian. Tento klíč se nikdy znovu nepoužívá; nový klíč se generuje s každou zprávou, včetně opětovných přenosů.

### Datová část

Sekce Flags neobsahuje nic. Má vždy 32 bajtů, protože musí mít stejnou délku jako statický klíč pro zprávy New Session s vazbou. Bob určí, zda se jedná o statický klíč nebo sekci flags testováním, zda jsou všechny 32 bajty nulové.

TODO jsou zde potřeba nějaké příznaky?

```

+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                                       |
  +             All zeros                 +
  |              32 bytes                 |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+

  zeros:: All zeros, 32 bytes.

```
### 1d) Jednorázový formát (bez vazby nebo relace)

Šifrovaná délka je zbytek dat. Dešifrovaná délka je o 16 menší než šifrovaná délka. Payload musí obsahovat blok DateTime a obvykle bude obsahovat jeden nebo více bloků Garlic Clove. Viz sekci payload níže pro formát a další požadavky.

### Nový jednorázový klíč relace

### Sekce příznaků Dešifrovaná data

Toto je standardní [NOISE](https://noiseprotocol.org/noise.html) pro IK s upraveným názvem protokolu. Všimněte si, že používáme stejný inicializátor jak pro vzor IK (vázané relace), tak pro vzor N (nevázané relace).

Název protokolu je modifikován ze dvou důvodů. Za prvé, k označení, že efemerní klíče jsou kódovány pomocí Elligator2, a za druhé, k označení, že MixHash() je volána před druhou zprávou pro zamíchání hodnoty tag.

```

This is the "e" message pattern:

  // Define protocol_name.
  Set protocol_name = "Noise_IKelg2+hs2_25519_ChaChaPoly_SHA256"
   (40 bytes, US-ASCII encoded, no NULL termination).

  // Define Hash h = 32 bytes
  h = SHA256(protocol_name);

  Define ck = 32 byte chaining key. Copy the h data to ck.
  Set chainKey = h

  // MixHash(null prologue)
  h = SHA256(h);

  // up until here, can all be precalculated by Alice for all outgoing connections

```
### Datová část

```

This is the "e" message pattern:

  // Bob's X25519 static keys
  // bpk is published in leaseset
  bsk = GENERATE_PRIVATE()
  bpk = DERIVE_PUBLIC(bsk)

  // Bob static public key
  // MixHash(bpk)
  // || below means append
  h = SHA256(h || bpk);

  // up until here, can all be precalculated by Bob for all incoming connections

  // Alice's X25519 ephemeral keys
  aesk = GENERATE_PRIVATE_ELG2()
  aepk = DERIVE_PUBLIC(aesk)

  // Alice ephemeral public key
  // MixHash(aepk)
  // || below means append
  h = SHA256(h || aepk);

  // h is used as the associated data for the AEAD in the New Session Message
  // Retain the Hash h for the New Session Reply KDF
  // eapk is sent in cleartext in the
  // beginning of the New Session message
  elg2_aepk = ENCODE_ELG2(aepk)
  // As decoded by Bob
  aepk = DECODE_ELG2(elg2_aepk)

  End of "e" message pattern.

  This is the "es" message pattern:

  // Noise es
  sharedSecret = DH(aesk, bpk) = DH(bsk, aepk)

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // ChaChaPoly parameters to encrypt/decrypt
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  chainKey = keydata[0:31]

  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, flags/static key section, ad)

  End of "es" message pattern.

  This is the "s" message pattern:

  // MixHash(ciphertext)
  // Save for Payload section KDF
  h = SHA256(h || ciphertext)

  // Alice's X25519 static keys
  ask = GENERATE_PRIVATE()
  apk = DERIVE_PUBLIC(ask)

  End of "s" message pattern.


```
### 1f) KDF pro New Session Message

```

This is the "ss" message pattern:

  // Noise ss
  sharedSecret = DH(ask, bpk) = DH(bsk, apk)

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // ChaChaPoly parameters to encrypt/decrypt
  // chainKey from Static Key Section
  Set sharedSecret = X25519 DH result
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  chainKey = keydata[0:31]

  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, payload, ad)

  End of "ss" message pattern.

  // MixHash(ciphertext)
  // Save for New Session Reply KDF
  h = SHA256(h || ciphertext)

```
### KDF pro počáteční ChainKey

Všimněte si, že se jedná o Noise "N" vzor, ale používáme stejný "IK" inicializátor jako u vázaných relací.

Zprávy New Session nelze identifikovat jako obsahující nebo neobsahující Alicin statický klíč, dokud není statický klíč dešifrován a zkontrolován, zda neobsahuje samé nuly. Proto musí příjemce použít stavový automat "IK" pro všechny zprávy New Session. Pokud statický klíč obsahuje samé nuly, vzor zprávy "ss" musí být přeskočen.

```

chainKey = from Flags/Static key section
  k = from Flags/Static key section
  n = 1
  ad = h from Flags/Static key section
  ciphertext = ENCRYPT(k, n, payload, ad)

```
### KDF pro šifrovaný obsah sekce Flags/Static Key

Jedna nebo více New Session Replies může být odesláno v odpovědi na jedinou New Session zprávu. Každá odpověď je doplněna tagem, který je generován z TagSet pro danou relaci.

Odpověď New Session je ve dvou částech. První část je dokončení Noise IK handshake s předřazeným tagem. Délka první části je 56 bajtů. Druhá část je payload datové fáze. Délka druhé části je 16 + délka payload.

Celková délka je 72 + délka payload. Šifrovaný formát:

```

+----+----+----+----+----+----+----+----+
  |       Session Tag   8 bytes           |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Ephemeral Public Key           +
  |                                       |
  +            32 bytes                   +
  |     Encoded with Elligator2           |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +  (MAC) for Key Section (no data)      +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |       ChaCha20 encrypted data         |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) for Payload Section     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  Tag :: 8 bytes, cleartext

  Public Key :: 32 bytes, little endian, Elligator2, cleartext

  MAC :: Poly1305 message authentication code, 16 bytes
         Note: The ChaCha20 plaintext data is empty (ZEROLEN)

  Payload Section encrypted data :: remaining data minus 16 bytes

  MAC :: Poly1305 message authentication code, 16 bytes

```
### KDF pro sekci Payload (se statickým klíčem Alice)

Značka je generována v Session Tags KDF, jak je inicializováno v DH Initialization KDF níže. Toto koreluje odpověď se session. Session Key z DH Initialization se nepoužívá.

### KDF pro sekci Payload (bez statického klíče Alice)

Bobův dočasný klíč. Dočasný klíč má 32 bajtů, kódovaný pomocí Elligator2, little endian. Tento klíč se nikdy nepoužívá opakovaně; nový klíč se generuje s každou zprávou, včetně opětovných přenosů.

### 1g) Formát New Session Reply

Šifrovaná délka je zbývající část dat. Dešifrovaná délka je o 16 menší než šifrovaná délka. Payload obvykle obsahuje jeden nebo více bloků Garlic Clove. Formát a další požadavky viz sekce payload níže.

### Session Tag

Jeden nebo více tagů je vytvořeno z TagSet, který je inicializován pomocí níže uvedeného KDF, s použitím chainKey ze zprávy New Session.

```

// Generate tagset
  tagsetKey = HKDF(chainKey, ZEROLEN, "SessionReplyTags", 32)
  tagset_nsr = DH_INITIALIZE(chainKey, tagsetKey)

```
### Odpověď na novou relaci - efemérní klíč

```

// Keys from the New Session message
  // Alice's X25519 keys
  // apk and aepk are sent in original New Session message
  // ask = Alice private static key
  // apk = Alice public static key
  // aesk = Alice ephemeral private key
  // aepk = Alice ephemeral public key
  // Bob's X25519 static keys
  // bsk = Bob private static key
  // bpk = Bob public static key

  // Generate the tag
  tagsetEntry = tagset_nsr.GET_NEXT_ENTRY()
  tag = tagsetEntry.SESSION_TAG

  // MixHash(tag)
  h = SHA256(h || tag)

  This is the "e" message pattern:

  // Bob's X25519 ephemeral keys
  besk = GENERATE_PRIVATE_ELG2()
  bepk = DERIVE_PUBLIC(besk)

  // Bob's ephemeral public key
  // MixHash(bepk)
  // || below means append
  h = SHA256(h || bepk);

  // elg2_bepk is sent in cleartext in the
  // beginning of the New Session message
  elg2_bepk = ENCODE_ELG2(bepk)
  // As decoded by Bob
  bepk = DECODE_ELG2(elg2_bepk)

  End of "e" message pattern.

  This is the "ee" message pattern:

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // ChaChaPoly parameters to encrypt/decrypt
  // chainKey from original New Session Payload Section
  sharedSecret = DH(aesk, bepk) = DH(besk, aepk)
  keydata = HKDF(chainKey, sharedSecret, "", 32)
  chainKey = keydata[0:31]

  End of "ee" message pattern.

  This is the "se" message pattern:

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  sharedSecret = DH(ask, bepk) = DH(besk, apk)
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  chainKey = keydata[0:31]

  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, ZEROLEN, ad)

  End of "se" message pattern.

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)

  chainKey is used in the ratchet below.

```
### Datová část

Toto je podobné první zprávě Existing Session po rozdělení, ale bez samostatného tagu. Navíc používáme hash z výše uvedeného k navázání payloadu na zprávu NSR.

```

// split()
  keydata = HKDF(chainKey, ZEROLEN, "", 64)
  k_ab = keydata[0:31]
  k_ba = keydata[32:63]
  tagset_ab = DH_INITIALIZE(chainKey, k_ab)
  tagset_ba = DH_INITIALIZE(chainKey, k_ba)

  // AEAD parameters for New Session Reply payload
  k = HKDF(k_ba, ZEROLEN, "AttachPayloadKDF", 32)
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, payload, ad)
```
### KDF pro Reply TagSet

V odpovědi může být odesláno více NSR zpráv, každá s jedinečnými dočasnými klíči, v závislosti na velikosti odpovědi.

Alice a Bob jsou povinni používat nové dočasné klíče pro každou NS a NSR zprávu.

Alice musí obdržet jednu z Bobových NSR zpráv před odesláním zpráv Existing Session (ES), a Bob musí obdržet ES zprávu od Alice před odesláním ES zpráv.

``chainKey`` a ``k`` z Bob's NSR Payload Section se používají jako vstupy pro počáteční ES DH Ratchets (oba směry, viz DH Ratchet KDF).

Bob musí zachovat pouze Existující relace pro ES zprávy přijaté od Alice. Všechny ostatní vytvořené příchozí a odchozí relace (pro více NSR) by měly být zničeny okamžitě po přijetí první ES zprávy od Alice pro danou relaci.

### KDF pro šifrovaný obsah sekce Reply Key

Session tag (8 bajtů) Šifrovaná data a MAC (viz sekce 3 níže)

### KDF pro šifrovaný obsah sekce Payload

Šifrované:

```

+----+----+----+----+----+----+----+----+
  |       Session Tag                     |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |       ChaCha20 encrypted data         |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +              (MAC)                    +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  Session Tag :: 8 bytes, cleartext

  Payload Section encrypted data :: remaining data minus 16 bytes

  MAC :: Poly1305 message authentication code, 16 bytes

```
### Poznámky

Šifrovaná délka je zbývající část dat. Dešifrovaná délka je o 16 menší než šifrovaná délka. Viz sekce payload níže pro formát a požadavky.

KDF

```
See AEAD section below.

  // AEAD parameters for Existing Session payload
  k = The 32-byte session key associated with this session tag
  n = The message number N in the current chain, as retrieved from the associated Session Tag.
  ad = The session tag, 8 bytes
  ciphertext = ENCRYPT(k, n, payload, ad)
```
### 1h) Formát existující relace

Formát: 32-bajtové veřejné a soukromé klíče, little-endian.

Zdůvodnění: Používá se v [NTCP2](/docs/specs/ntcp2/).

### Formát

Ve standardních Noise handshake postupech začínají počáteční handshake zprávy v každém směru s efemérními klíči, které jsou přenášeny v otevřeném textu. Jelikož platné X25519 klíče jsou rozlišitelné od náhodných dat, může útočník typu man-in-the-middle rozlišit tyto zprávy od zpráv Existing Session, které začínají náhodnými session tagy. V [NTCP2](/docs/specs/ntcp2/) ([Proposal 111](/proposals/111-ntcp-2/)) jsme použili nízkonákladovou XOR funkci využívající out-of-band statický klíč k zamaskování klíče. Avšak model hrozeb je zde odlišný; nechceme umožnit žádnému MitM používat jakékoli prostředky k potvrzení cíle provozu nebo k rozlišení počátečních handshake zpráv od zpráv Existing Session.

Proto se používá [Elligator2](https://elligator.cr.yp.to/) k transformaci dočasných klíčů ve zprávách New Session a New Session Reply tak, aby byly nerozeznatelné od uniformních náhodných řetězců.

### Datová část

32bajtové veřejné a soukromé klíče. Kódované klíče jsou ve formátu little endian.

Jak je definováno v [Elligator2](https://elligator.cr.yp.to/), zakódované klíče jsou nerozeznatelné od 254 náhodných bitů. Potřebujeme 256 náhodných bitů (32 bajtů). Kódování a dekódování jsou proto definovány následovně:

Kódování:

```

ENCODE_ELG2() Definition

  // Encode as defined in Elligator2 specification
  encodedKey = encode(pubkey)
  // OR in 2 random bits to MSB
  randomByte = CSRNG(1)
  encodedKey[31] |= (randomByte & 0xc0)
```
Dekódování:

```

DECODE_ELG2() Definition

  // Mask out 2 random bits from MSB
  encodedKey[31] &= 0x3f
  // Decode as defined in Elligator2 specification
  pubkey = decode(encodedKey)
```
### 2) ECIES-X25519

Vyžadováno k zabránění klasifikaci provozu ze strany OBEP a IBGW.

### 2a) Elligator2

Elligator2 zdvojnásobuje průměrný čas generování klíčů, protože polovina soukromých klíčů má za následek veřejné klíče, které nejsou vhodné pro kódování pomocí Elligator2. Také čas generování klíčů je neomezený s exponenciálním rozdělením, protože generátor musí pokračovat v opakování, dokud není nalezen vhodný pár klíčů.

Tato režie může být řízena předem prováděným generováním klíčů v samostatném vláknu, aby se udržel fond vhodných klíčů.

Generátor provádí funkci ENCODE_ELG2() k určení vhodnosti. Proto by měl generátor uložit výsledek ENCODE_ELG2(), aby nemusel být znovu vypočítáván.

Navíc mohou být nevhodné klíče přidány do fondu klíčů používaných pro [NTCP2](/docs/specs/ntcp2/), kde se Elligator2 nepoužívá. Bezpečnostní problémy tohoto postupu jsou zatím neurčené.

### Formát

AEAD používající ChaCha20 a Poly1305, stejně jako v [NTCP2](/docs/specs/ntcp2/). To odpovídá [RFC-7539](https://tools.ietf.org/html/rfc7539), které se také podobně používá v TLS [RFC-7905](https://tools.ietf.org/html/rfc7905).

### Odůvodnění

Vstupy do funkcí šifrování/dešifrování pro AEAD blok ve zprávě New Session:

```

k :: 32 byte cipher key
       See New Session and New Session Reply KDFs above.

  n :: Counter-based nonce, 12 bytes.
       n = 0

  ad :: Associated data, 32 bytes.
        The SHA256 hash of the preceding data, as output from mixHash()

  data :: Plaintext data, 0 or more bytes

```
### Poznámky

Vstupy do funkcí šifrování/dešifrování pro AEAD blok ve zprávě Existing Session:

```

k :: 32 byte session key
       As looked up from the accompanying session tag.

  n :: Counter-based nonce, 12 bytes.
       Starts at 0 and incremented for each message when transmitting.
       For the receiver, the value
       as looked up from the accompanying session tag.
       First four bytes are always zero.
       Last eight bytes are the message number (n), little-endian encoded.
       Maximum value is 65535.
       Session must be ratcheted when N reaches that value.
       Higher values must never be used.

  ad :: Associated data
        The session tag

  data :: Plaintext data, 0 or more bytes

```
### 3) AEAD (ChaChaPoly)

Výstup šifrovací funkce, vstup dešifrovací funkce:

```

+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |       ChaCha20 encrypted data         |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +              (MAC)                    +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  encrypted data :: Same size as plaintext data, 0 - 65519 bytes

  MAC :: Poly1305 message authentication code, 16 bytes

```
### Vstupy New Session a New Session Reply

- Jelikož ChaCha20 je proudová šifra, plaintexty nemusí být doplňovány.
  Dodatečné bajty keystreamu jsou zahozeny.

- Klíč pro šifru (256 bitů) je dohodnut prostřednictvím SHA256 KDF.
  Podrobnosti KDF pro každou zprávu jsou v oddílech níže.

- ChaChaPoly rámce mají známou velikost, protože jsou zapouzdřeny v I2NP datové zprávě.

- Pro všechny zprávy
  se padding nachází uvnitř autentifikovaného
  datového rámce.

### Vstupy existující relace

Všechna přijatá data, která neprošla AEAD ověřením, musí být zahozena. Žádná odpověď není vrácena.

### Šifrovaný formát

Používá se v [NTCP2](/docs/specs/ntcp2/).

### Poznámky

Stále používáme session tags, jako předtím, ale používáme ratchets k jejich generování. Session tags také měly možnost rekey, kterou jsme nikdy neimplementovali. Takže je to jako double ratchet, ale ten druhý jsme nikdy neudělali.

Zde definujeme něco podobného jako Signal's Double Ratchet. Značky relace jsou generovány deterministicky a identicky na straně příjemce i odesílatele.

Použitím symetrického klíče/tag ratchet eliminujeme využití paměti pro ukládání session tagů na straně odesílatele. Také eliminujeme spotřebu šířky pásma při odesílání sad tagů. Využití na straně příjemce je stále významné, ale můžeme ho dále snížit, protože zmenšíme session tag z 32 bajtů na 8 bajtů.

Nepoužíváme šifrování hlaviček jak je specifikováno (a volitelné) v Signal, místo toho používáme session tags.

Použitím DH ratchet dosahujeme forward secrecy, která nikdy nebyla implementována v ElGamal/AES+SessionTags.

Poznámka: Jednorázový veřejný klíč nové relace není součástí ratchetu, jeho jedinou funkcí je zašifrovat Alicein počáteční DH ratchet klíč.

### Zpracování chyb AEAD

Double Ratchet zpracovává ztracené nebo neuspořádané zprávy tak, že do hlavičky každé zprávy zahrnuje značku. Příjemce vyhledá index značky, což je číslo zprávy N. Pokud zpráva obsahuje blok Message Number s hodnotou PN, příjemce může smazat všechny značky vyšší než tato hodnota v předchozí sadě značek, přičemž si ponechá přeskočené značky z předchozí sady značek pro případ, že přeskočené zprávy dorazí později.

### Odůvodnění

Definujeme následující datové struktury a funkce pro implementaci těchto ratchetů.

TAGSET_ENTRY

    A single entry in a TAGSET.

    INDEX
        An integer index, starting with 0

    SESSION_TAG
        An identifier to go out on the wire, 8 bytes

    SESSION_KEY
        A symmetric key, never goes on the wire, 32 bytes

TAGSET

    A collection of TAGSET_ENTRIES.

    CREATE(key, n)
        Generate a new TAGSET using initial cryptographic key material of 32 bytes.
        The associated session identifier is provided.
        The initial number of of tags to create is specified; this is generally 0 or 1
        for an outgoing session.
        LAST_INDEX = -1
        EXTEND(n) is called.

    EXTEND(n)
        Generate n more TAGSET_ENTRIES by calling EXTEND() n times.

    EXTEND()
        Generate one more TAGSET_ENTRY, unless the maximum number SESSION_TAGS have
        already been generated.
        If LAST_INDEX is greater than or equal to 65535, return.
        ++ LAST_INDEX
        Create a new TAGSET_ENTRY with the LAST_INDEX value and the calculated SESSION_TAG.
        Calls RATCHET_TAG() and (optionally) RATCHET_KEY().
        For inbound sessions, the calculation of the SESSION_KEY may
        be deferred and calculated in GET_SESSION_KEY().
        Calls EXPIRE()

    EXPIRE()
        Remove tags and keys that are too old, or if the TAGSET size exceeds some limit.

    RATCHET_TAG()
        Calculates the next SESSION_TAG based on the last SESSION_TAG.

    RATCHET_KEY()
        Calculates the next SESSION_KEY based on the last SESSION_KEY.

    SESSION
        The associated session.

    CREATION_TIME
        When the TAGSET was created.

    LAST_INDEX
        The last TAGSET_ENTRY INDEX generated by EXTEND().

    GET_NEXT_ENTRY()
        Used for outgoing sessions only.
        EXTEND(1) is called if there are no remaining TAGSET_ENTRIES.
        If EXTEND(1) did nothing, the max of 65535 TAGSETS have been used,
        and return an error.
        Returns the next unused TAGSET_ENTRY.

    GET_SESSION_KEY(sessionTag)
        Used for incoming sessions only.
        Returns the TAGSET_ENTRY containing the sessionTag.
        If found, the TAGSET_ENTRY is removed.
        If the SESSION_KEY calculation was deferred, it is calculated now.
        If there are few TAGSET_ENTRIES remaining, EXTEND(n) is called.


### 4) Západky

Ratchets, ale ne zdaleka tak rychle jako Signal. Oddělujeme potvrzení přijatého klíče od generování nového klíče. V typickém použití Alice a Bob každý provede ratchet (dvakrát) okamžitě v nové relaci, ale poté již ratchet neprovedou znovu.

Poznámka: ratchet je pro jeden směr a generuje řetězec ratchet pro New Session tag / klíč zprávy pro daný směr. Pro generování klíčů pro oba směry musíte provést ratchet dvakrát.

Ratchet se provádí pokaždé, když vygenerujete a odešlete nový klíč. Ratchet se provádí pokaždé, když obdržíte nový klíč.

Alice provede jeden ratchet při vytváření nevázané odchozí relace, nevytváří příchozí relaci (nevázaná je bez možnosti odpovědi).

Bob provede jednu rotaci ratchet při vytváření nevázané příchozí relace a nevytváří odpovídající odchozí relaci (nevázaná je neoddpověditelná).

Alice pokračuje v odesílání zpráv New Session (NS) Bobovi, dokud neobdrží jednu z Bobových zpráv New Session Reply (NSR). Poté použije výsledky KDF z Payload Section NSR jako vstupy pro session ratchets (viz DH Ratchet KDF) a začne odesílat zprávy Existing Session (ES).

Pro každou přijatou NS zprávu vytvoří Bob novou příchozí relaci, přičemž použije výsledky KDF z části Payload odpovědi jako vstupy pro nový příchozí a odchozí ES DH Ratchet.

Pro každou vyžadovanou odpověď pošle Bob Alici NSR zprávu s odpovědí v datové části. Je vyžadováno, aby Bob použil nové efemérní klíče pro každou NSR.

Bob musí obdržet ES zprávu od Alice na jedné z příchozích relací, před vytvořením a odesláním ES zpráv na odpovídající odchozí relaci.

Alice by měla použít časovač pro příjem NSR zprávy od Boba. Pokud časovač vyprší, relace by měla být odstraněna.

Aby se předešlo KCI a/nebo útoku vyčerpáním zdrojů, kde útočník zahazuje Bobovy NSR odpovědi, aby Alice nadále posílala NS zprávy, Alice by se měla vyhnout zahajování nových relací s Bobem po určitém počtu opakování kvůli vypršení časovače.

Alice a Bob každý provádí DH ratchet pro každý přijatý blok NextKey.

Alice a Bob vygenerují nové tag sety a dva symetrické klíče po každém DH ratchet. Pro každou novou ES zprávu v daném směru Alice a Bob posunou session tag a symetrické klíčové ratchety.

Frekvence DH ratchetů po počátečním handshaku závisí na implementaci. Zatímco protokol stanovuje limit 65535 zpráv před tím, než je vyžadován ratchet, častější ratcheting (založený na počtu zpráv, uběhlém čase nebo obojím) může poskytovat dodatečnou bezpečnost.

Po finálním handshake KDF na vázaných relacích musí Bob a Alice spustit funkci Noise Split() na výsledném CipherState, aby vytvořili nezávislé symetrické klíče a klíče řetězce tagů pro příchozí a odchozí relace.

#### KEY AND TAG SET IDS

Čísla ID klíčů a tag setů se používají k identifikaci klíčů a tag setů. ID klíčů se používají v blocích NextKey k identifikaci odeslaného nebo použitého klíče. ID tag setů se používají (společně s číslem zprávy) v blocích ACK k identifikaci potvrzované zprávy. ID klíčů i tag setů se vztahují k tag setům pro jeden směr. Čísla ID klíčů a tag setů musí být sekvenční.

V prvních sadách tagů použitých pro relaci v každém směru je ID sady tagů 0. Nebyly odeslány žádné bloky NextKey, takže neexistují žádné ID klíčů.

Pro začátek DH ratchet odešle odesílatel nový NextKey blok s key ID 0. Příjemce odpoví novým NextKey blokem s key ID 0. Odesílatel pak začne používat novou sadu tagů s tag set ID 1.

Následující sady tagů jsou generovány podobně. Pro všechny sady tagů použité po výměnách NextKey je číslo sady tagů (1 + Alice's key ID + Bob's key ID).

ID klíčů a tag setů začínají na 0 a postupně se zvyšují. Maximální ID tag setu je 65535. Maximální ID klíče je 32767. Když je tag set téměř vyčerpán, odesílatel tag setu musí iniciovat výměnu NextKey. Když je tag set 65535 téměř vyčerpán, odesílatel tag setu musí iniciovat novou relaci odesláním zprávy New Session.

S maximální velikostí zprávy pro streaming 1730 a za předpokladu žádných opětovných přenosů je teoretické maximum přenosu dat pomocí jediné sady tagů 1730 * 65536 ~= 108 MB. Skutečné maximum bude nižší kvůli opětovným přenosům.

Teoretické maximum přenosu dat se všemi 65536 dostupnými sadami tagů, předtím než by musela být relace zahozena a nahrazena, je 64K * 108 MB ~= 6,9 TB.

#### DH RATCHET MESSAGE FLOW

Další výměna klíčů pro sadu tagů musí být iniciována odesílatelem těchto tagů (vlastníkem odchozí sady tagů). Příjemce (vlastník příchozí sady tagů) odpoví. Pro typický HTTP GET provoz na aplikační vrstvě bude Bob posílat více zpráv a bude ratchet jako první tím, že iniciuje výměnu klíčů; diagram níže to ukazuje. Když Alice provede ratchet, stejná věc se stane obráceně.

První sada tagů použitá po NS/NSR handshake je sada tagů 0. Když je sada tagů 0 téměř vyčerpána, musí být v obou směrech vyměněny nové klíče pro vytvoření sady tagů 1. Poté je nový klíč odesílán pouze v jednom směru.

Pro vytvoření sady tagů 2 odesílá odesílatel tagů nový klíč a příjemce tagů odesílá ID svého starého klíče jako potvrzení. Obě strany provedou DH.

Pro vytvoření sady tagů 3 odešle odesílatel tagu ID svého starého klíče a požádá příjemce tagu o nový klíč. Obě strany provádějí DH.

Následující sady tagů jsou generovány stejně jako sady tagů 2 a 3. Číslo sady tagů je (1 + ID klíče odesílatele + ID klíče příjemce).

```

Tag Sender                    Tag Receiver

                   ... use tag set #0 ...


  (Tagset #0 almost empty)
  (generate new key #0)

  Next Key, forward, request reverse, with key #0  -------->
  (repeat until next key received)

                              (generate new key #0, do DH, create IB Tagset #1)

          <-------------      Next Key, reverse, with key #0
                              (repeat until tag received on new tagset)

  (do DH, create OB Tagset #1)


                   ... use tag set #1 ...


  (Tagset #1 almost empty)
  (generate new key #1)

  Next Key, forward, with key #1        -------->
  (repeat until next key received)

                              (reuse key #0, do DH, create IB Tagset #2)

          <--------------     Next Key, reverse, id 0
                              (repeat until tag received on new tagset)

  (do DH, create OB Tagset #2)


                   ... use tag set #2 ...


  (Tagset #2 almost empty)
  (reuse key #1)

  Next Key, forward, request reverse, id 1  -------->
  (repeat until next key received)

                              (generate new key #1, do DH, create IB Tagset #3)

          <--------------     Next Key, reverse, with key #1

  (do DH, create OB Tagset #3)
  (reuse key #1, do DH, create IB Tagset #3)


                   ... use tag set #3 ...


       After tag set 3, repeat the above
       patterns as shown for tag sets 2 and 3.

       To create a new even-numbered tag set, the sender sends a new key
       to the receiver. The receiver sends his old key ID
       back as an acknowledgement.

       To create a new odd-numbered tag set, the sender sends a reverse request
       to the receiver. The receiver sends a new reverse key to the sender.

```
Po dokončení DH ratchet pro odchozí tagset a vytvoření nového odchozího tagsetu by měl být okamžitě použit a starý odchozí tagset může být smazán.

Po dokončení DH ratchet pro příchozí tagset a vytvoření nového příchozího tagset by měl příjemce naslouchat tagům v obou tagsetech a smazat starý tagset po krátké době, přibližně 3 minuty.

Přehled postupu sady tagů a ID klíčů je v tabulce níže. * označuje, že je vygenerován nový klíč.

| New Tag Set ID | Sender key ID | Rcvr key ID |
|----------------|---------------|-------------|
| 0              | n/a           | n/a         |
| 1              | 0 *           | 0 *         |
| 2              | 1 *           | 0           |
| 3              | 1             | 1 *         |
| 4              | 2 *           | 1           |
| 5              | 2             | 2 *         |
| ...            | ...           | ...         |
| 65534          | 32767 *       | 32766       |
| 65535          | 32767         | 32767 *     |
Čísla ID klíčů a sad tagů musí být sekvenční.

#### DH INITIALIZATION KDF

Toto je definice DH_INITIALIZE(rootKey, k) pro jeden směr. Vytváří tagset a "další root key", který se použije pro následný DH ratchet v případě potřeby.

Používáme DH inicializaci na třech místech. Zaprvé ji používáme k vygenerování sady tagů pro New Session Replies. Zadruhé ji používáme k vygenerování dvou sad tagů, jedné pro každý směr, pro použití ve zprávách Existing Session. Nakonec ji používáme po DH Ratchet k vygenerování nové sady tagů v jednom směru pro další zprávy Existing Session.

```

Inputs:
  1) rootKey = chainKey from Payload Section
  2) k from the New Session KDF or split()

  // KDF_RK(rk, dh_out)
  keydata = HKDF(rootKey, k, "KDFDHRatchetStep", 64)

  // Output 1: The next Root Key (KDF input for the next DH ratchet)
  nextRootKey = keydata[0:31]
  // Output 2: The chain key to initialize the new
  // session tag and symmetric key ratchets
  // for the tag set
  ck = keydata[32:63]

  // session tag and symmetric key chain keys
  keydata = HKDF(ck, ZEROLEN, "TagAndKeyGenKeys", 64)
  sessTag_ck = keydata[0:31]
  symmKey_ck = keydata[32:63]

```
#### DH RATCHET KDF

Toto se používá po výměně nových DH klíčů v NextKey blocích, před vyčerpáním tagset.

```


// Tag sender generates new X25519 ephemeral keys
  // and sends rapk to tag receiver in a NextKey block
  rask = GENERATE_PRIVATE()
  rapk = DERIVE_PUBLIC(rask)
  
  // Tag receiver generates new X25519 ephemeral keys
  // and sends rbpk to Tag sender in a NextKey block
  rbsk = GENERATE_PRIVATE()
  rbpk = DERIVE_PUBLIC(rbsk)

  sharedSecret = DH(rask, rbpk) = DH(rbsk, rapk)
  tagsetKey = HKDF(sharedSecret, ZEROLEN, "XDHRatchetTagSet", 32)
  rootKey = nextRootKey // from previous tagset in this direction
  newTagSet = DH_INITIALIZE(rootKey, tagsetKey)

```
### Čísla zpráv

Ratchets pro každou zprávu, stejně jako v Signal. Ratchet session tagu je synchronizován s ratchetem symetrického klíče, ale ratchet klíče příjemce může „zaostávat" kvůli úspoře paměti.

Transmitter provede ratchet jednou pro každou odeslanou zprávu. Nemusí být uloženy žádné další tagy. Transmitter musí také udržovat čítač pro 'N', číslo zprávy ve stávajícím řetězci. Hodnota 'N' je zahrnuta v odeslané zprávě. Viz definice bloku Message Number.

Příjemce musí posunout ratchet dopředu o maximální velikost okna a uložit tagy do "sady tagů", která je asociována se session. Jakmile je přijat, uložený tag může být zahozen, a pokud nejsou žádné předchozí nepřijaté tagy, okno může být posunuto. Příjemce by měl udržovat hodnotu 'N' asociovanou s každým session tagem a kontrolovat, že číslo v odeslané zprávě odpovídá této hodnotě. Viz definice bloku Message Number.

#### KDF

Toto je definice RATCHET_TAG().

```

Inputs:
  1) Session Tag Chain key sessTag_ck
     First time: output from DH ratchet
     Subsequent times: output from previous session tag ratchet

  Generated:
  2) input_key_material = SESSTAG_CONSTANT
     Must be unique for this tag set (generated from chain key),
     so that the sequence isn't predictable, since session tags
     go out on the wire in plaintext.

  Outputs:
  1) N (the current session tag number)
  2) the session tag (and symmetric key, probably)
  3) the next Session Tag Chain Key (KDF input for the next session tag ratchet)

  Initialization:
  keydata = HKDF(sessTag_ck, ZEROLEN, "STInitialization", 64)
  // Output 1: Next chain key
  sessTag_chainKey = keydata[0:31]
  // Output 2: The constant
  SESSTAG_CONSTANT = keydata[32:63]

  // KDF_ST(ck, constant)
  keydata_0 = HKDF(sessTag_chainkey, SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
  // Output 1: Next chain key
  sessTag_chainKey_0 = keydata_0[0:31]
  // Output 2: The session tag
  // or more if tag is longer than 8 bytes
  tag_0 = keydata_0[32:39]

  // repeat as necessary to get to tag_n
  keydata_n = HKDF(sessTag_chainKey_(n-1), SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
  // Output 1: Next chain key
  sessTag_chainKey_n = keydata_n[0:31]
  // Output 2: The session tag
  // or more if tag is longer than 8 bytes
  tag_n = keydata_n[32:39]

```
### Ukázková implementace

Ratchets pro každou zprávu, jako v aplikaci Signal. Každý symetrický klíč má přiřazené číslo zprávy a session tag. Ratchet session klíče je synchronizován s ratchetem symetrického tagu, ale ratchet klíče příjemce může "zaostávat" kvůli úspoře paměti.

Transmitter se posune jednou pro každou odeslanou zprávu. Není nutné ukládat žádné další klíče.

Když příjemce obdrží session tag, pokud ještě neposunul symetrický key ratchet dopředu k přidruženému klíči, musí se "dohnat" k přidruženému klíči. Příjemce pravděpodobně uloží do cache klíče pro všechny předchozí tagy, které ještě nebyly přijaty. Po přijetí může být uložený klíč zahozen, a pokud neexistují žádné předchozí nepřijaté tagy, může být okno posunuto dopředu.

Pro efektivitu jsou session tag a symetrické klíčové ratchety oddělené, takže session tag ratchet může běžet před symetrickým klíčovým ratchetem. To také poskytuje dodatečnou bezpečnost, protože session tagy jdou ven po drátě.

#### KDF

Toto je definice RATCHET_KEY().

```

Inputs:
  1) Symmetric Key Chain key symmKey_ck
     First time: output from DH ratchet
     Subsequent times: output from previous symmetric key ratchet

  Generated:
  2) input_key_material = SYMMKEY_CONSTANT = ZEROLEN
     No need for uniqueness. Symmetric keys never go out on the wire.
     TODO: Set a constant anyway?

  Outputs:
  1) N (the current session key number)
  2) the session key
  3) the next Symmetric Key Chain Key (KDF input for the next symmetric key ratchet)

  // KDF_CK(ck, constant)
  SYMMKEY_CONSTANT = ZEROLEN
  // Output 1: Next chain key
  keydata_0 = HKDF(symmKey_ck, SYMMKEY_CONSTANT, "SymmetricRatchet", 64)
  symmKey_chainKey_0 = keydata_0[0:31]
  // Output 2: The symmetric key
  k_0 = keydata_0[32:63]

  // repeat as necessary to get to k[n]
  keydata_n = HKDF(symmKey_chainKey_(n-1), SYMMKEY_CONSTANT, "SymmetricRatchet", 64)
  // Output 1: Next chain key
  symmKey_chainKey_n = keydata_n[0:31]
  // Output 2: The symmetric key
  k_n = keydata_n[32:63]


```
### 4a) DH Ratchet

Toto nahrazuje formát sekce AES definovaný ve specifikaci ElGamal/AES+SessionTags.

Toto používá stejný formát bloků jako je definován ve specifikaci [NTCP2](/docs/specs/ntcp2/). Jednotlivé typy bloků jsou definovány odlišně.

Existují obavy, že povzbuzování implementátorů ke sdílení kódu může vést k problémům s parsováním. Implementátoři by měli pečlivě zvážit výhody a rizika sdílení kódu a zajistit, aby se pravidla pro pořadí a platné bloky lišila pro oba kontexty.

### Payload Section Decrypted data

Délka šifrovaných dat je zbývající část dat. Délka dešifrovaných dat je o 16 menší než délka šifrovaných dat. Všechny typy bloků jsou podporovány. Typický obsah zahrnuje následující bloky:

| Payload Block Type | Type Number | Block Length |
|--------------------|-------------|--------------|
| DateTime           | 0           | 7            |
| Termination (TBD)  | 4           | 9 typ.       |
| Options (TBD)      | 5           | 21+          |
| Message Number (TBD) | 6           | TBD          |
| Next Key           | 7           | 3 or 35      |
| ACK                | 8           | 4 typ.       |
| ACK Request        | 9           | 3            |
| Garlic Clove       | 11          | varies       |
| Padding            | 254         | varies       |
### Unencrypted data

V šifrovaném rámci se nachází nula nebo více bloků. Každý blok obsahuje jednobytový identifikátor, dvoubytovou délku a nula nebo více bajtů dat.

Z důvodu rozšiřitelnosti MUSÍ příjemci ignorovat bloky s neznámými čísly typů a zacházet s nimi jako s výplní.

Šifrovaná data mají maximálně 65535 bajtů, včetně 16bajtové autentizační hlavičky, takže maximální nešifrovaná data jsou 65519 bajtů.

(Poly1305 autentizační tag není zobrazen):

```

+----+----+----+----+----+----+----+----+
  |blk |  size   |       data             |
  +----+----+----+                        +
  |                                       |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |blk |  size   |       data             |
  +----+----+----+                        +
  |                                       |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  ~               .   .   .               ~

  blk :: 1 byte
         0 datetime
         1-3 reserved
         4 termination
         5 options
         6 previous message number
         7 next session key
         8 ack
         9 ack request
         10 reserved
         11 Garlic Clove
         224-253 reserved for experimental features
         254 for padding
         255 reserved for future extension
  size :: 2 bytes, big endian, size of data to follow, 0 - 65516
  data :: the data

  Maximum ChaChaPoly frame is 65535 bytes.
  Poly1305 tag is 16 bytes
  Maximum total block size is 65519 bytes
  Maximum single block size is 65519 bytes
  Block type is 1 byte
  Block length is 2 bytes
  Maximum single block data size is 65516 bytes.

```
### Block Ordering Rules

Ve zprávě New Session je blok DateTime povinný a musí být prvním blokem.

Další povolené bloky:

- Garlic Clove (typ 11)
- Možnosti (typ 5)
- Výplň (typ 254)

V odpovědi zprávy New Session Reply nejsou vyžadovány žádné bloky.

Další povolené bloky:

- Garlic Clove (typ 11)
- Možnosti (typ 5)
- Výplň (typ 254)

Žádné další bloky nejsou povoleny. Padding, pokud je přítomen, musí být posledním blokem.

V existující relaci nejsou vyžadovány žádné bloky a pořadí není specifikováno, kromě následujících požadavků:

Ukončení, pokud je přítomno, musí být posledním blokem kromě Padding. Padding, pokud je přítomen, musí být posledním blokem.

V jednom snímku může být více bloků Garlic Clove. V jednom snímku mohou být až dva bloky Next Key. Více bloků Padding v jednom snímku není povoleno. Ostatní typy bloků pravděpodobně nebudou mít více bloků v jednom snímku, ale není to zakázáno.

### DateTime

Vypršení platnosti. Pomáhá při prevenci opakovaných odpovědí. Bob musí ověřit, že zpráva je aktuální, pomocí tohoto časového razítka. Bob musí implementovat Bloomův filtr nebo jiný mechanismus pro prevenci replay útoků, pokud je čas platný. Obecně zahrnuto pouze ve zprávách New Session.

```

+----+----+----+----+----+----+----+
  | 0  |    4    |     timestamp     |
  +----+----+----+----+----+----+----+

  blk :: 0
  size :: 2 bytes, big endian, value = 4
  timestamp :: Unix timestamp, unsigned seconds.
               Wraps around in 2106

```
### 4b) Session Tag Ratchet

Jeden dešifrovaný Garlic Clove jak je specifikován v [I2NP](/docs/specs/i2np/), s modifikacemi pro odstranění polí, která jsou nepoužívaná nebo redundantní. Upozornění: Tento formát se významně liší od toho pro ElGamal/AES. Každý clove je samostatný payload blok. Garlic Cloves nesmí být fragmentovány napříč bloky nebo napříč ChaChaPoly rámci.

```

+----+----+----+----+----+----+----+----+
  | 11 |  size   |                        |
  +----+----+----+                        +
  |      Delivery Instructions            |
  ~                                       ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |type|  Message_ID       | Expiration   
  +----+----+----+----+----+----+----+----+
       |      I2NP Message body           |
  +----+                                  +
  ~                                       ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  size :: size of all data to follow

  Delivery Instructions :: As specified in
         the Garlic Clove section of [I2NP](/docs/specs/i2np/).
         Length varies but is typically 1, 33, or 37 bytes

  type :: I2NP message type

  Message_ID :: 4 byte `Integer` I2NP message ID

  Expiration :: 4 bytes, seconds since the epoch

```
Poznámky:

- Implementátoři musí zajistit, že při čtení bloku
  nebudou chybně formátovaná nebo škodlivá data způsobovat
  přečtení dat přesahující do dalšího bloku.

- Formát Clove Set specifikovaný v [I2NP](/docs/specs/i2np/) se nepoužívá.
  Každý clove je obsažen ve svém vlastním bloku.

- Hlavička I2NP zprávy má 9 bajtů, s identickým formátem
  jako ten používaný v [NTCP2](/docs/specs/ntcp2/).

- Certifikát, ID zprávy a vypršení z
  definice Garlic Message v [I2NP](/docs/specs/i2np/) nejsou zahrnuty.

- Certificate, Clove ID a Expiration z definice
  Garlic Clove v [I2NP](/docs/specs/i2np/) nejsou zahrnuty.

Zdůvodnění:

- Certifikáty nebyly nikdy použity.
- Samostatné ID zprávy a ID clove nebyly nikdy použity.
- Samostatné expirační doby nebyly nikdy použity.
- Celkové úspory ve srovnání se starými formáty Clove Set a Clove
  jsou přibližně 35 bajtů pro 1 clove, 54 bajtů pro 2 cloves
  a 73 bajtů pro 3 cloves.
- Formát bloku je rozšiřitelný a jakákoli nová pole mohou být přidána
  jako nové typy bloků.

### Termination

Implementace je volitelná. Ukončit relaci. Toto musí být poslední nepadovací blok v rámci. V této relaci již nebudou odesílány žádné další zprávy.

Není povoleno v NS nebo NSR. Zahrnuto pouze ve zprávách Existing Session.

```

+----+----+----+----+----+----+----+----+
  | 4  |  size   | rsn|     addl data     |
  +----+----+----+----+                   +
  ~               .   .   .               ~
  +----+----+----+----+----+----+----+----+

  blk :: 4
  size :: 2 bytes, big endian, value = 1 or more
  rsn :: reason, 1 byte:
         0: normal close or unspecified
         1: termination received
         others: optional, impementation-specific
  addl data :: optional, 0 or more bytes, for future expansion, debugging,
               or reason text.
               Format unspecified and may vary based on reason code.

```
### 4c) Symmetric Key Ratchet

NEIMPLEMENTOVÁNO, pro další studium. Předat aktualizované volby. Volby zahrnují různé parametry pro relaci. Viz sekce Analýza délky značky relace níže pro více informací.

Blok možností může mít variabilní délku, protože může být přítomen more_options.

```

+----+----+----+----+----+----+----+----+
  | 5  |  size   |ver |flg |STL |STimeout |
  +----+----+----+----+----+----+----+----+
  |  SOTW   |  RITW   |tmin|tmax|rmin|rmax|
  +----+----+----+----+----+----+----+----+
  |  tdmy   |  rdmy   |  tdelay |  rdelay |
  +----+----+----+----+----+----+----+----+
  |              more_options             |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  blk :: 5
  size :: 2 bytes, big endian, size of options to follow, 21 bytes minimum
  ver :: Protocol version, must be 0
  flg :: 1 byte flags
         bits 7-0: Unused, set to 0 for future compatibility
  STL :: Session tag length (must be 8), other values unimplemented
  STimeout :: Session idle timeout (seconds), big endian
  SOTW :: Sender Outbound Tag Window, 2 bytes big endian
  RITW :: Receiver Inbound Tag Window 2 bytes big endian

  tmin, tmax, rmin, rmax :: requested padding limits
      tmin and rmin are for desired resistance to traffic analysis.
      tmax and rmax are for bandwidth limits.
      tmin and tmax are the transmit limits for the router sending this options block.
      rmin and rmax are the receive limits for the router sending this options block.
      Each is a 4.4 fixed-point float representing 0 to 15.9375
      (or think of it as an unsigned 8-bit integer divided by 16.0).
      This is the ratio of padding to data. Examples:
      Value of 0x00 means no padding
      Value of 0x01 means add 6 percent padding
      Value of 0x10 means add 100 percent padding
      Value of 0x80 means add 800 percent (8x) padding
      Alice and Bob will negotiate the minimum and maximum in each direction.
      These are guidelines, there is no enforcement.
      Sender should honor receiver's maximum.
      Sender may or may not honor receiver's minimum, within bandwidth constraints.

  tdmy: Max dummy traffic willing to send, 2 bytes big endian, bytes/sec average
  rdmy: Requested dummy traffic, 2 bytes big endian, bytes/sec average
  tdelay: Max intra-message delay willing to insert, 2 bytes big endian, msec average
  rdelay: Requested intra-message delay, 2 bytes big endian, msec average

  more_options :: Format undefined, for future use

```
SOTW je doporučení odesílatele pro příjemce ohledně okna příchozích tagů příjemce (maximální předstih). RITW je prohlášení odesílatele o okně příchozích tagů (maximální předstih), které plánuje použít. Každá strana pak nastaví nebo upraví předstih na základě nějakého minima nebo maxima nebo jiného výpočtu.

Poznámky:

- Podpora pro nestandardní délku session tagu doufejme
  nikdy nebude vyžadována.
- Okno tagů je MAX_SKIP v dokumentaci Signal.

Problémy:

- Vyjednávání opcí bude teprve určeno.
- Výchozí hodnoty budou teprve určeny.
- Možnosti paddingu a zpoždění jsou zkopírovány z NTCP2,
  ale tyto možnosti tam nebyly plně implementovány ani prostudovány.

### Message Numbers

Implementace je volitelná. Délka (počet odeslaných zpráv) v předchozí sadě tagů (PN). Příjemce může okamžitě smazat tagy vyšší než PN z předchozí sady tagů. Příjemce může nechat vypršet tagy menší nebo rovné PN z předchozí sady tagů po krátké době (např. 2 minuty).

```

+----+----+----+----+----+
  | 6  |  size   |  PN    |
 +----+----+----+----+----+

  blk :: 6
  size :: 2
  PN :: 2 bytes big endian. The index of the last tag sent in the previous tag set.

```
Poznámky:

- Maximální PN je 65535.
- Definice PN se rovná definici Signal, minus jedna.
  To je podobné tomu, co dělá Signal, ale v Signal jsou PN a N v hlavičce.
  Zde jsou v zašifrovaném těle zprávy.
- Neposílejte tento blok v tag set 0, protože neexistoval žádný předchozí tag set.

### 5) Datová část

Další DH ratchet klíč je v datové části a je volitelný. Nerotujeme pokaždé. (To se liší od Signal, kde je v hlavičce a posílá se pokaždé)

Pro první ratchet, Key ID = 0.

Není povoleno v NS nebo NSR. Zahrnuto pouze ve zprávách Existing Session.

```

+----+----+----+----+----+----+----+----+
  | 7  |  size   |flag|  key ID |         |
  +----+----+----+----+----+----+         +
  |                                       |
  +                                       +
  |     Next DH Ratchet Public Key        |
  +                                       +
  |                                       |
  +                             +----+----+
  |                             |
  +----+----+----+----+----+----+

  blk :: 7
  size :: 3 or 35
  flag :: 1 byte flags
          bit order: 76543210
          bit 0: 1 for key present, 0 for no key present
          bit 1: 1 for reverse key, 0 for forward key
          bit 2: 1 to request reverse key, 0 for no request
                 only set if bit 1 is 0
          bits 7-2: Unused, set to 0 for future compatibility
  key ID :: The key ID of this key. 2 bytes, big endian
            0 - 32767
  Public Key :: The next X25519 public key, 32 bytes, little endian
                Only if bit 0 is 1


```
Poznámky:

- Key ID je rostoucí čítač pro lokální klíč používaný pro danou sadu tagů, začínající na 0.
- ID se nesmí změnit, dokud se nezmění klíč.
- Možná to není striktně nutné, ale je to užitečné pro ladění.
  Signal nepoužívá key ID.
- Maximální Key ID je 32767.
- Ve vzácném případě, že se sady tagů v obou směrech ratchetují současně,
  bude frame obsahovat dva bloky Next Key, jeden pro forward klíč a jeden pro reverse klíč.
- Čísla ID klíčů a sad tagů musí být sekvenční.
- Podrobnosti viz sekce DH Ratchet výše.

### Sekce Payload Dešifrovaná data

Toto je odesláno pouze v případě, že byl přijat blok s požadavkem na potvrzení. Může být přítomno více potvrzení pro potvrzení více zpráv.

Nepovoleno v NS nebo NSR. Zahrnuto pouze ve zprávách Existing Session.

```
+----+----+----+----+----+----+----+----+
  | 8  |  size   |tagsetid |   N     |    |
  +----+----+----+----+----+----+----+    +
  |             more acks                 |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  blk :: 8
  size :: 4 * number of acks to follow, minimum 1 ack
  for each ack:
  tagsetid :: 2 bytes, big endian, from the message being acked
  N :: 2 bytes, big endian, from the message being acked


```
Poznámky:

- ID sady tagů a N jednoznačně identifikují zprávu, která je potvrzována.
- V prvních sadách tagů použitých pro relaci v každém směru je ID sady tagů 0.
- Nebyly odeslány žádné bloky NextKey, takže neexistují žádné ID klíčů.
- Pro všechny sady tagů použité po výměnách NextKey je číslo sady tagů (1 + Alice's key ID + Bob's key ID).

### Nešifrovaná data

Požádat o in-band ack. Pro nahrazení out-of-band DeliveryStatus Message v Garlic Clove.

Pokud je vyžádáno explicitní potvrzení, aktuální ID tagset a číslo zprávy (N) jsou vráceny v bloku potvrzení.

Není povoleno v NS nebo NSR. Zahrnuto pouze ve zprávách Existing Session.

```

+----+----+----+----+
  |  9 |  size   |flg |
  +----+----+----+----+

  blk :: 9
  size :: 1
  flg :: 1 byte flags
         bits 7-0: Unused, set to 0 for future compatibility

```
### Pravidla řazení bloků

Veškeré vyplnění je uvnitř AEAD rámců. TODO Vyplnění uvnitř AEAD by mělo zhruba dodržovat vyjednaná parametry. TODO Alice poslala své požadované tx/rx min/max parametry ve zprávě NS. TODO Bob poslal své požadované tx/rx min/max parametry ve zprávě NSR. Aktualizované možnosti mohou být odeslány během datové fáze. Viz informace o bloku možností výše.

Pokud je přítomen, musí to být poslední blok v rámci.

```

+----+----+----+----+----+----+----+----+
  |254 |  size   |      padding           |
  +----+----+----+                        +
  |                                       |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  blk :: 254
  size :: 2 bytes, big endian, 0-65516
  padding :: zeros or random data

```
Poznámky:

- Výplň samými nulami je v pořádku, protože bude zašifrována.
- Strategie výplně budou teprve určeny.
- Rámce obsahující pouze výplň jsou povoleny.
- Výchozí výplň je 0-15 bajtů.
- Viz blok options pro vyjednávání parametrů výplně
- Viz blok options pro parametry min/max výplně
- Reakce routeru na porušení vyjednaných parametrů výplně závisí na implementaci.

### DateTime

Implementace by měly ignorovat neznámé typy bloků kvůli dopředné kompatibilitě.

### Garlic Clove

- Délka paddingu má být buď rozhodována na bázi jednotlivých zpráv a
  odhadů distribuce délek, nebo mají být přidána náhodná zpoždění.
  Tato protiopatření mají být zahrnuta pro odolnost vůči DPI, jelikož velikosti
  zpráv by jinak prozradily, že I2P provoz je přenášen transportním
  protokolem. Přesné schéma paddingu je oblastí budoucí práce, Příloha A
  poskytuje více informací k tomuto tématu.

## Typical Usage Patterns

### Ukončení

Toto je nejběžnější případ použití a většina non-HTTP streaming případů použití bude totožná s tímto případem použití také. Pošle se krátká počáteční zpráva, následuje odpověď a další zprávy se odesílají v obou směrech.

HTTP GET obecně zapadá do jedné I2NP zprávy. Alice pošle malý požadavek s jednou novou Session zprávou, přibalí reply leaseset. Alice zahrnuje okamžité ratchet na nový klíč. Zahrnuje sig pro svázání s destinací. Není požadováno žádné potvrzení.

Bob se okamžitě přepne na další klíč.

Alice okamžitě provádí ratcheting.

Pokračuje s těmito relacemi.

```

Alice                           Bob

  New Session (1b)     ------------------->
  with ephemeral key 1
  with static key for binding
  with next key
  with bundled HTTP GET
  with bundled LS
  without bundled Delivery Status Message

  any retransmissions, same as above

  following messages may arrive in any order:

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 1
                      with bundled HTTP reply part 1

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 2
                      with bundled HTTP reply part 2

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 3
                      with bundled HTTP reply part 3

  After reception of any of these messages,
  Alice switches to use Existing Session messages,
  creates a new inbound + outbound session pair,
  and ratchets.


  Existing Session     ------------------->
  with bundled streaming ack


  Existing Session     ------------------->
  with bundled streaming ack


  After reception of any of these messages,
  Bob switches to use Existing Session messages.


  <--------------     Existing Session
                      with bundled HTTP reply part 4


  Existing Session     ------------------->
  with bundled streaming ack

  <--------------     Existing Session
                      with bundled HTTP reply part 5

```
### Možnosti

Alice má tři možnosti:

1) Odeslat pouze první zprávu (velikost okna = 1), jako u HTTP GET. Nedoporučuje se.

2) Odeslat až do streaming okna, ale používat stejný Elligator2-kódovaný cleartext veřejný klíč. Všechny zprávy obsahují stejný další veřejný klíč (ratchet). Toto bude viditelné pro OBGW/IBEP, protože všechny začínají se stejným cleartextem. Věci pokračují jako v 1). Nedoporučuje se.

3) Doporučená implementace.    Posílat až do streaming window, ale použitím jiného Elligator2-kódovaného cleartext veřejného klíče (session) pro každou zprávu.    Všechny zprávy obsahují stejný další veřejný klíč (ratchet).    Toto nebude viditelné pro OBGW/IBEP, protože všechny začínają jiným cleartext.    Bob musí rozpoznat, že všechny obsahují stejný další veřejný klíč,    a odpovědět na všechny se stejným ratchet.    Alice použije tento další veřejný klíč a pokračuje.

Možnost 3 průběh zpráv:

```

Alice                           Bob

  New Session (1b)     ------------------->
  with ephemeral key 1
  with static key for binding
  with bundled HTTP POST part 1
  with bundled LS
  without bundled Delivery Status Message


  New Session (1b)     ------------------->
  with ephemeral key 2
  with static key for binding
  with bundled HTTP POST part 2
  with bundled LS
  without bundled Delivery Status Message


  New Session (1b)     ------------------->
  with ephemeral key 3
  with static key for binding
  with bundled HTTP POST part 3
  with bundled LS
  without bundled Delivery Status Message


  following messages can arrive in any order:

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 1
                      with bundled streaming ack

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 2
                      with bundled streaming ack

  After reception of any of these messages,
  Alice switches to use Existing Session messages,
  creates a new inbound + outbound session pair,
  and ratchets.


  following messages can arrive in any order:


  Existing Session     ------------------->
  with bundled HTTP POST part 4

  Existing Session     ------------------->
  with next key
  with bundled HTTP POST part 5


  After reception of any of these messages,
  Bob switches to use Existing Session messages.


  <--------------     Existing Session
                      with bundled streaming ack

  After reception of any of this message,
  Alice switches to use Existing Session messages,
  and Alice ratchets.


  Existing Session     ------------------->
  with next key
  with bundled HTTP POST part 4

  after reception of this message, Bob ratchets

  Existing Session     ------------------->
  with next key
  with bundled HTTP POST part 5

  <--------------     Existing Session
                      with bundled streaming ack

```
### Čísla zpráv

Jedna zpráva s očekávanou jednou odpovědí. Další zprávy nebo odpovědi mohou být odeslány.

Podobné HTTP GET, ale s menšími možnostmi pro velikost okna session tag a životnost. Možná nepožadovat ratchet.

```

Alice                           Bob

  New Session (1b)     ------------------->
  with static key for binding
  with next key
  with bundled repliable datagram
  with bundled LS
  without bundled Delivery Status Message


  <--------------     New Session Reply (1g)
                      with Bob ephemeral key
                      with bundled reply part 1

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key
                      with bundled reply part 2

  After reception of either message,
  Alice switches to use Existing Session messages,
  and ratchets.

  If the Existing Session message arrives first,
  Alice ratchets on the existing inbound and outbound
  sessions.

  When the New Session Reply arrives, Alice
  sets the existing inbound session to expire,
  creates a new inbound and outbound session,
  and sends Existing Session messages on
  the new outbound session.

  Alice keeps the expiring inbound session
  around for a while to process the Existing Session
  message sent to Alice.
  If all expected original Existing Session message replies
  have been processed, Alice can expire the original
  inbound session immediately.

  if there are any other messages:

  Existing Session     ------------------->
  with bundled message

  Existing Session     ------------------->
  with bundled streaming ack

  <--------------     Existing Session
                      with bundled message

```
### Další veřejný klíč DH Ratchet

Více anonymních zpráv, bez očekávání odpovědí.

V tomto scénáři Alice požaduje session, ale bez bindingu. Je odeslána zpráva New session. Žádný reply LS není připojen. Reply DSM je připojen (toto je jediný případ použití, který vyžaduje připojené DSM). Žádný next key není zahrnut. Žádný reply nebo ratchet není požadován. Žádný ratchet není odeslán. Volby nastavují okno session tags na nulu.

```

Alice                           Bob

  New Session (1c)     ------------------->
  with bundled message
  without bundled LS
  with bundled Delivery Status Message 1

  New Session (1c)     ------------------->
  with bundled message
  without bundled LS
  with bundled Delivery Status Message 2

  New Session (1c)     ------------------->
  with bundled message
  without bundled LS
  with bundled Delivery Status Message 3
 
  following messages can arrive in any order:

  <--------------     Delivery Status Message 1

  <--------------     Delivery Status Message 2

  <--------------     Delivery Status Message 3

  After reception of any of these messages,
  Alice switches to use Existing Session messages.

  Existing Session     ------------------->

  Existing Session     ------------------->

  Existing Session     ------------------->

```
### Potvrzení

Jediná anonymní zpráva, bez očekávané odpovědi.

Jednorázová zpráva je odeslána. Žádné odpovědní LS nebo DSM nejsou připojeny. Žádný další klíč není zahrnut. Žádná odpověď nebo ratchet není vyžádán. Žádný ratchet není odeslán. Možnosti nastavují okno session tags na nulu.

```

Alice                           Bob

  One-Time Message (1d)   ------------------->
  with bundled message
  without bundled LS
  without bundled Delivery Status Message

```
### Žádost o potvrzení

Dlouhodobé relace mohou provést ratchet, nebo požádat o ratchet, kdykoli, aby udržely forward secrecy od daného okamžiku. Relace musí provést ratchet, když se blíží limitu odeslaných zpráv na relaci (65535).

## Implementation Considerations

### Výplň

Stejně jako u stávajícího protokolu ElGamal/AES+SessionTag musí implementace omezit ukládání session tagů a chránit se proti útokům vyčerpáním paměti.

Některé doporučené strategie zahrnují:

- Pevný limit na počet uložených session tagů
- Agresivní vypršení nečinných příchozích sessions při tlaku na paměť
- Limit na počet příchozích sessions navázaných na jednu vzdálenou destinaci
- Adaptivní snížení okna session tagů a mazání starých nepoužívaných tagů
  při tlaku na paměť
- Odmítnutí ratchet operace na požádání, pokud je tlak na paměť

### Ostatní typy bloků

Doporučené parametry a časové limity:

- Velikost NSR tagset: 12 tsmin a tsmax
- Velikost ES tagset 0: tsmin 24, tsmax 160
- Velikost ES tagset (1+): 160 tsmin a tsmax
- Timeout NSR tagset: 3 minuty pro příjemce
- Timeout ES tagset: 8 minut pro odesílatele, 10 minut pro příjemce
- Odstranit předchozí ES tagset po: 3 minutách
- Tagset look ahead tagu N: min(tsmax, tsmin + N/4)
- Tagset trim behind tagu N: min(tsmax, tsmin + N/4) / 2
- Poslat další klíč u tagu: TBD
- Poslat další klíč po životnosti tagset: TBD
- Nahradit relaci pokud NS přijato po: 3 minutách
- Maximální odchylka hodin: -5 minut až +2 minuty
- Doba trvání NS replay filtru: 5 minut
- Velikost paddingu: 0-15 bajtů (další strategie TBD)

### Budoucí práce

Následují doporučení pro klasifikaci příchozích zpráv.

### X25519 Only

Na tunnelu, který je používán výhradně s tímto protokolem, proveďte identifikaci tak, jak se aktuálně provádí s ElGamal/AES+SessionTags:

Nejprve zpracujte počáteční data jako session tag a vyhledejte session tag. Pokud je nalezen, dešifrujte pomocí uložených dat spojených s tímto session tagem.

Pokud nebyl nalezen, zpracuj počáteční data jako DH veřejný klíč a nonce. Proveď DH operaci a specifikovaný KDF, a pokus se dešifrovat zbývající data.

### HTTP GET

Na tunelu, který podporuje jak tento protokol, tak ElGamal/AES+SessionTags, klasifikujte příchozí zprávy následovně:

Kvůli chybě ve specifikaci ElGamal/AES+SessionTags není AES blok doplněn na náhodnou délku, která by nebyla dělitelná 16. Proto je délka zpráv Existing Session modulo 16 vždy 0 a délka zpráv New Session modulo 16 je vždy 2 (jelikož ElGamal blok je dlouhý 514 bajtů).

Pokud délka modulo 16 není 0 nebo 2, považujte počáteční data za session tag a vyhledejte tento session tag. Pokud je nalezen, dešifrujte pomocí uložených dat přidružených k tomuto session tagu.

Pokud není nalezen a délka mod 16 není 0 nebo 2, považujte počáteční data za DH veřejný klíč a nonce. Proveďte DH operaci a specifikovanou KDF a pokuste se dešifrovat zbývající data. (na základě relativního mixu provozu a relativních nákladů X25519 a ElGamal DH operací může být tento krok proveden jako poslední)

Jinak, pokud je délka mod 16 rovna 0, považujte počáteční data za ElGamal/AES session tag a vyhledejte tento session tag. Pokud je nalezen, dešifrujte pomocí uložených dat spojených s tímto session tagem.

Pokud není nalezeno a data jsou dlouhá alespoň 642 (514 + 128) bajtů a délka mod 16 je 2, považujte počáteční data za ElGamal blok. Pokuste se dešifrovat zbývající data.

Vezměte na vědomí, že pokud bude specifikace ElGamal/AES+SessionTag aktualizována tak, aby umožňovala padding jiný než mod-16, bude třeba postupovat odlišně.

### HTTP POST

Počáteční implementace spoléhají na obousměrný provoz ve vyšších vrstvách. To znamená, že implementace předpokládají, že provoz v opačném směru bude brzy přenášen, což vynutí jakoukoli požadovanou odpověď na vrstvě ECIES.

Nicméně určitý provoz může být jednosměrný nebo s velmi nízkou šířkou pásma, takže neexistuje provoz vyšší vrstvy, který by vygeneroval včasnou odpověď.

Příjem NS a NSR zpráv vyžaduje odpověď; příjem ACK Request a Next Key bloků také vyžaduje odpověď.

Sofistikovaná implementace může spustit časovač při přijetí jedné z těchto zpráv, která vyžaduje odpověď, a vygenerovat "prázdnou" (bez bloku Garlic Clove) odpověď na vrstvě ECIES, pokud není odeslán žádný zpětný provoz v krátkém časovém období (např. 1 sekunda).

Může být také vhodné nastavit ještě kratší timeout pro odpovědi na NS a NSR zprávy, aby se provoz co nejdříve přesunul k efektivním ES zprávám.

## Analysis

### Odpověditelný datagram

Režijní náklad zpráv pro první dvě zprávy v každém směru je následující. To předpokládá pouze jednu zprávu v každém směru před ACK, nebo že jakékoliv další zprávy jsou odesílány spekulativně jako zprávy Existing Session. Pokud neexistují spekulativní potvrzení doručených session tagů, režijní náklad starého protokolu je mnohem vyšší.

Pro analýzu nového protokolu se nepředpokládá žádné vyplňování. Nepředpokládá se žádný přibalený leaseSet.

### Vícenásobné Raw datagramy

Zpráva nové relace, stejná v každém směru:

```

ElGamal block:
  514 bytes

  AES block:
  - 2 byte tag count
  - 1024 bytes of tags (32 typical)
  - 4 byte payload size
  - 32 byte hash of payload
  - 1 byte flags
  - 1 byte clove count
  - 33 byte Garlic deliv. inst.
  - 16 byte I2NP header
  - 15 byte clove cert, id, exp.
  - 15 byte msg cert, id, exp.
  - 0 byte padding assuming 1936 byte message
  1143 total

  Total:
  1657 bytes
```
Zprávy existující relace, stejné v každém směru:

```

AES block:
  - 32 byte session tag
  - 2 byte tag count
  - 4 byte payload size
  - 32 byte hash of payload
  - 1 byte flags
  - 1 byte clove count
  - 33 byte Garlic deliv. inst.
  - 16 byte I2NP header
  - 15 byte msg cert, id, exp.
  - 15 byte clove cert, id, exp.
  - 0 byte padding assuming 1936 byte message
  151 total
```
```
Four message total (two each direction)
  3616 bytes overhead
```
### Jednotný Raw Datagram

Zpráva Alice-to-Bob New Session:

```

- 32 byte ephemeral public key
  - 32 byte static public key
  - 16 byte Poly1305 MAC
  - 7 byte DateTime block
  - 3 byte Garlic block overhead
  - 9 byte I2NP header
  - 33 byte Garlic deliv. inst.
  - 16 byte Poly1305 MAC

  Total:
  148 bytes overhead
```
Zpráva Bob-to-Alice New Session Reply:

```

- 8 byte session tag
  - 32 byte ephemeral public key
  - 16 byte Poly1305 MAC
  - 3 byte Garlic block overhead
  - 9 byte I2NP header
  - 33 byte Garlic deliv. inst.
  - 16 byte Poly1305 MAC

  Total:
  117 bytes overhead
```
Stávající zprávy relace, stejné v každém směru:

```

- 8 byte session tag
  - 3 byte Garlic block overhead
  - 9 byte I2NP header
  - 33 byte Garlic deliv. inst.
  - 16 byte Poly1305 MAC

  Total:
  69 bytes
```
### Dlouhodobé relace

Celkem čtyři zprávy (dvě v každém směru):

```

372 bytes
  90% (approx. 10x) reduction compared to ElGamal/AES+SessionTags
```
Pouze handshake:

```

ElGamal: 1657 + 1657 = 3314 bytes
  Ratchet: 148 _ 117 = 265 bytes
  92% (approx. 12x) reduction compared to ElGamal/AES+SessionTags
```
Dlouhodobý celkový součet (ignorování handshakes):

```
ElGamal: 151 + 32 byte tag sent previously = 183 bytes
  Ratchet: 69 bytes
  64% (approx. 3x) reduction compared to ElGamal/AES+SessionTags
```
### CPU

TODO aktualizovat tuto sekci poté, co bude návrh stabilní.

Následující kryptografické operace jsou vyžadovány každou stranou pro výměnu zpráv New Session a New Session Reply:

- HMAC-SHA256: 3 na HKDF, celkem TBD
- ChaChaPoly: 2 každý
- Generování klíče X25519: 2 Alice, 1 Bob
- X25519 DH: 3 každý
- Ověření podpisu: 1 (Bob)

Alice vypočítá 5 ECDH na vázanou relaci (minimum), 2 pro každou NS zprávu Bobovi a 3 pro každou Bobovu NSR zprávu.

Bob také vypočítá 6 ECDH per-bound-session, 3 pro každou z Alice NS zpráv a 3 pro každou ze svých NSR zpráv.

Následující kryptografické operace jsou vyžadovány každou stranou pro každou zprávu Existing Session:

- HKDF: 2
- ChaChaPoly: 1

### Obrana

Současná délka session tagu je 32 bajtů. Zatím jsme nenašli žádné odůvodnění pro tuto délku, ale pokračujeme ve výzkumu archivů. Výše uvedený návrh definuje novou délku tagu jako 8 bajtů. Analýza odůvodňující 8bajtový tag je následující:

Předpokládá se, že session tag ratchet generuje náhodné, rovnoměrně distribuované tagy. Neexistuje žádný kryptografický důvod pro konkrétní délku session tagu. Session tag ratchet je synchronizován se symetrickým klíčovým ratchetem, ale generuje nezávislý výstup. Výstupy obou ratchetů mohou mít různé délky.

Jediným problémem je tedy kolize session tagů. Předpokládá se, že implementace se nebudou pokoušet řešit kolize pokusem o dešifrování v obou sessions; implementace jednoduše přiřadí tag buď k předchozí nebo nové session, a jakákoli zpráva přijatá s tímto tagem v druhé session bude zahozena po neúspěšném dešifrování.

Cílem je vybrat délku session tag, která je dostatečně velká pro minimalizaci rizika kolizí, a zároveň dostatečně malá pro minimalizaci využití paměti.

Toto předpokládá, že implementace omezují ukládání session tagů, aby zabránily útokům vyčerpáním paměti. To také výrazně sníží šance, že útočník dokáže vytvořit kolize. Viz sekce Implementační úvahy níže.

V nejhorším případě předpokládejme zaneprázdněný server s 64 novými inbound relacemi za sekundu. Předpokládejme 15minutovou životnost inbound session tagů (stejně jako nyní, pravděpodobně by měla být snížena). Předpokládejme inbound session tag okno o velikosti 32. 64 * 15 * 60 * 32 = 1,843,200 tagů. Současné maximum inbound tagů v Java I2P je 750,000 a pokud víme, nikdy nebylo dosaženo.

Cíl 1 kolize session tagů na milion (1e-6) je pravděpodobně dostatečný. Pravděpodobnost zahození zprávy na cestě kvůli přetížení je daleko vyšší.

Ref: https://en.wikipedia.org/wiki/Birthday_paradox sekce tabulka pravděpodobností.

S 32bytovými session tagy (256 bitů) je prostor session tagů 1,2e77. Pravděpodobnost kolize s pravděpodobností 1e-18 vyžaduje 4,8e29 záznamů. Pravděpodobnost kolize s pravděpodobností 1e-6 vyžaduje 4,8e35 záznamů. 1,8 milionu tagů po 32 bytech je celkem asi 59 MB.

S 16bytovými session tagy (128 bitů) je prostor session tagů 3,4e38. Pravděpodobnost kolize s pravděpodobností 1e-18 vyžaduje 2,6e10 záznamů. Pravděpodobnost kolize s pravděpodobností 1e-6 vyžaduje 2,6e16 záznamů. 1,8 milionu tagů po 16 bajtech každý představuje celkem asi 30 MB.

S 8bytovými session tagy (64 bitů) je prostor session tagů 1,8e19. Pravděpodobnost kolize s pravděpodobností 1e-18 vyžaduje 6,1 záznamů. Pravděpodobnost kolize s pravděpodobností 1e-6 vyžaduje 6,1e6 (6 100 000) záznamů. 1,8 milionu tagů po 8 bytech každý činí celkem asi 15 MB.

6,1 milionu aktivních tagů je více než 3x více než náš nejhorší odhad 1,8 milionu tagů. Pravděpodobnost kolize by tedy byla menší než jedna ku milionu. Docházíme tedy k závěru, že 8bajtové session tagy jsou dostatečné. To vede ke 4x snížení úložného prostoru, kromě 2x snížení kvůli tomu, že transmit tagy nejsou uložené. Takže budeme mít 8x snížení využití paměti pro session tagy ve srovnání s ElGamal/AES+SessionTags.

Pro zachování flexibility v případě, že by tyto předpoklady byly chybné, zahrneme do možností pole délky session tagu, takže výchozí délka může být přepsána na základě jednotlivých relací. Neočekáváme, že budeme implementovat dynamické vyjednávání délky tagů, pokud to nebude naprosto nezbytné.

Implementace by měly minimálně rozpoznat kolize session tagů, zvládnout je elegantně a zalogovat nebo spočítat počet kolizí. Ačkoli jsou stále extrémně nepravděpodobné, budou mnohem pravděpodobnější než byly u ElGamal/AES+SessionTags a skutečně se mohou stát.

### Parametry

Při použití dvakrát více relací za sekundu (128) a dvakrát většího okna tagů (64) máme 4krát více tagů (7,4 milionu). Maximum pro šanci kolize jedna ku milionu je 6,1 milionu tagů. 12bajtové (nebo dokonce 10bajtové) tagy by přidaly obrovskou rezervu.

Je však šance jeden k milionu pro kolizi dobrým cílem? Mnohem větší než šance být zahozena cestou není příliš užitečná. Cíl pro falešně pozitivní výsledky pro Java DecayingBloomFilter je zhruba 1 ku 10 000, ale dokonce ani 1 ku 1 000 není vážným problémem. Snížením cíle na 1 ku 10 000 je dostatečná rezerva s 8bajtovými tagy.

### Klasifikace

Odesílatel generuje tagy a klíče za běhu, takže není potřeba žádné úložiště. To snižuje celkové požadavky na úložiště na polovinu ve srovnání s ElGamal/AES. ECIES tagy mají 8 bajtů namísto 32 u ElGamal/AES. To snižuje celkové požadavky na úložiště o další faktor 4. Klíče relací pro jednotlivé tagy nejsou na straně příjemce ukládány kromě "mezer", které jsou při rozumných mírách ztrát minimální.

33% snížení času vypršení tagu vytváří další 33% úspory, za předpokladu krátkých časů relací.

Proto je celková úspora místa oproti ElGamal/AES faktorem 10,7, neboli 92%.

## Related Changes

### Pouze X25519

Databázové vyhledávání z ECIES destinací: Viz [Proposal 154](/proposals/154-ecies-lookups), nyní začleněno v [I2NP](/docs/specs/i2np/) pro vydání 0.9.46.

Tento návrh vyžaduje podporu LS2 pro publikování veřejného klíče X25519 s leaseset. Nejsou vyžadovány žádné změny ve specifikacích LS2 v [I2NP](/docs/specs/i2np/). Veškerá podpora byla navržena, specifikována a implementována v [Návrhu 123](/proposals/123-new-netdb-entries) implementovaném ve verzi 0.9.38.

### X25519 sdílené s ElGamal/AES+SessionTags

Žádné. Tento návrh vyžaduje podporu LS2 a nastavení vlastnosti v I2CP možnostech pro aktivaci. Nejsou vyžadovány žádné změny ve specifikacích [I2CP](/docs/specs/i2cp/). Veškerá podpora byla navržena, specifikována a implementována v [Návrhu 123](/proposals/123-new-netdb-entries) implementovaném ve verzi 0.9.38.

Možnost potřebná k povolení ECIES je jedna I2CP vlastnost pro I2CP, BOB, SAM nebo i2ptunnel.

Typické hodnoty jsou i2cp.leaseSetEncType=4 pouze pro ECIES, nebo i2cp.leaseSetEncType=4,0 pro ECIES a ElGamal duální klíče.

### Odpovědi na protokolové vrstvě

Tato sekce je zkopírována z [Návrhu 123](/proposals/123-new-netdb-entries).

Možnost v mapování SessionConfig:

```
  i2cp.leaseSetEncType=nnn[,nnn]  The encryption types to be used.
                                  0: ElGamal
                                  1-3: See proposal 145
                                  4: This proposal.
```
### Create Leaseset2 Message

Tento návrh vyžaduje LS2, který je podporován od verze 0.9.38. Nejsou potřeba žádné změny specifikací [I2CP](/docs/specs/i2cp/). Veškerá podpora byla navržena, specifikována a implementována v [Proposal 123](/proposals/123-new-netdb-entries) implementovaném ve verzi 0.9.38.

### Režie

Jakýkoliv router podporující LS2 s duálními klíči (0.9.38 nebo vyšší) by měl podporovat připojení k destinacím s duálními klíči.

Pouze ECIES destinace budou vyžadovat, aby většina floodfillů byla aktualizována na verzi 0.9.46 pro získání šifrovaných odpovědí na vyhledávání. Viz [Proposal 154](/proposals/154-ecies-lookups).

ECIES-only destinace se mohou připojit pouze k jiným destinacím, které jsou buď také ECIES-only, nebo dual-key.
