---
title: "ECIES-X25519-AEAD-Ratchet"
description: "Elliptic Curve Integrated Encryption Scheme pro end-to-end šifrování v I2P"
slug: "ecies"
aliases:
  - "/cs/docs/specs/ecies-x25519-aead-ratchet"
  - "/cs/docs/specs/ecies-x25519-aead-ratchet/"
category: "Protokoly"
lastUpdated: "2025-06"
accurateFor: "0.9.67"
---

## Poznámka

Nasazení sítě dokončeno. Podléhá drobným revizím. Viz [Prop144](/proposals/144-ecies-x25519/) pro původní návrh, včetně diskuze na pozadí a dalších informací.

Následující funkce nejsou implementovány k verzi 0.9.66:

- Bloky MessageNumbers, Options a Termination
- Odpovědi na úrovni protokolu
- Nulový statický klíč
- Multicast

Pro MLKEM PQ Hybrid verzi tohoto protokolu viz [ECIES-HYBRID](/docs/specs/ecies-hybrid/).

## Přehled

Toto je nový protokol end-to-end šifrování, který nahradí ElGamal/AES+SessionTags [ElG-AES](/docs/specs/elgamal-aes/).

Vychází z předchozí práce následovně:

- Specifikace běžných struktur [Common](/docs/specs/common-structures/)
- Specifikace [I2NP](/docs/specs/i2np/) včetně LS2
- ElGamal/AES+Session Tags [Elg-AES](/docs/specs/elgamal-aes/)
- <http://zzz.i2p/topics/1768> přehled nové asymetrické kryptografie
- Nízkoúrovňový přehled kryptografie [CRYPTO-ELG](/docs/specs/cryptography/#elgamal)
- ECIES <http://zzz.i2p/topics/2418>
- [NTCP2](/docs/specs/ntcp2/) [Prop111](/proposals/111-ntcp2/)
- 123 Nové záznamy netDB
- 142 Nová šablona kryptografie
- Protokol [Noise](https://noiseprotocol.org/noise.html)
- Algoritmus double ratchet [Signal](https://signal.org/docs/specifications/doubleratchet/)

Podporuje nové šifrování pro end-to-end komunikaci mezi destinacemi.

Design používá Noise handshake a datovou fázi zahrnující dvojitý ratchet ze Signalu.

Všechny odkazy na Signal a Noise v této specifikaci slouží pouze jako základní informace. Znalost protokolů Signal a Noise není vyžadována pro pochopení nebo implementaci této specifikace.

Tato specifikace je podporována od verze 0.9.46.

## Specifikace

Design využívá Noise handshake a datovou fázi zahrnující dvojitý ratchet protokolu Signal.

### Shrnutí kryptografického návrhu

Existuje pět částí protokolu, které je třeba přenavrhnout:

- 1\) Nové a stávající formáty kontejnerů Session jsou nahrazeny
  novými formáty.
- 2\) ElGamal (256 bajtové veřejné klíče, 128 bajtové privátní klíče) je
  nahrazen ECIES-X25519 (32 bajtové veřejné a privátní klíče)
- 3\) AES je nahrazen AEAD_ChaCha20_Poly1305 (zkráceně jako
  ChaChaPoly níže)
- 4\) SessionTags budou nahrazeny ratchets, což je v podstatě
  kryptografický, synchronizovaný PRNG.
- 5\) AES payload, jak je definován ve specifikaci ElGamal/AES+SessionTags,
  je nahrazen formátem bloku podobným tomu v NTCP2.

Každá z pěti změn má níže svou vlastní sekci.

### Typ šifrování

Typ šifrování (používaný v LS2) je 4. To označuje little-endian 32-bajtový X25519 veřejný klíč a end-to-end protokol specifikovaný zde.

Kryptografický typ 0 je ElGamal. Kryptografické typy 1-3 jsou rezervovány pro ECIES-ECDH-AES-SessionTag, viz návrh 145 [Prop145](/proposals/145-ecies-ecdh-aes/).

### Noise Protocol Framework

Tento protokol poskytuje požadavky založené na Noise Protocol Framework [NOISE](https://noiseprotocol.org/noise.html) (Revize 34, 2018-07-11). Noise má podobné vlastnosti jako Station-To-Station protokol [STS](https://en.wikipedia.org/wiki/Station-to-Station_protocol), který je základem pro protokol [SSU](/docs/transport/ssu/). V terminologii Noise je Alice iniciátor a Bob je respondent.

Tato specifikace je založena na Noise protokolu Noise_IK_25519_ChaChaPoly_SHA256. (Skutečný identifikátor pro počáteční funkci odvození klíče je "Noise_IKelg2_25519_ChaChaPoly_SHA256" pro označení I2P rozšíření - viz sekce KDF 1 níže) Tento Noise protokol používá následující primitiva:

- Vzor interaktivního handshake: IK Alice okamžitě přenáší svůj
  statický klíč Bobovi (I) Alice už zná Bobův statický klíč (K)
- Vzor jednosměrného handshake: N Alice nepřenáší svůj statický klíč
  Bobovi (N)
- DH funkce: X25519 X25519 DH s délkou klíče 32 bajtů jak
  je specifikováno v [RFC-7748](https://tools.ietf.org/html/rfc7748).
- Šifrovací funkce: ChaChaPoly AEAD_CHACHA20_POLY1305 jak je specifikováno v
  [RFC-7539](https://tools.ietf.org/html/rfc7539) sekce 2.8. 12 bajtový nonce, s
  prvními 4 bajty nastavenými na nulu. Identické s tím v
  [NTCP2](/docs/specs/ntcp2/).
- Hash funkce: SHA256 Standardní 32-bajtový hash, již hojně používaný
  v I2P.

#### Doplňky k frameworku

Tato specifikace definuje následující vylepšení pro Noise_IK_25519_ChaChaPoly_SHA256. Ta obecně následují pokyny v [NOISE](https://noiseprotocol.org/noise.html) sekci 13.

1)  Cleartext ephemeral klíče jsou kódovány pomocí

    [Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf).
2) Odpověď má předponu s cleartext značkou. 3) Formát payload je definován pro zprávy 1, 2 a datovou fázi.

    Of course, this is not defined in Noise.

Všechny zprávy obsahují hlavičku [I2NP](/docs/specs/i2np/) Garlic Message. Datová fáze používá šifrování podobné datové fázi protokolu Noise, ale není s ní kompatibilní.

### Vzory handshake

Handshakes používají [Noise](https://noiseprotocol.org/noise.html) handshake vzory.

Použije se následující mapování písmen:

- e = jednosférový dočasný klíč
- s = statický klíč
- p = obsah zprávy

Jednorázové a nevázané relace jsou podobné vzoru Noise N.

```
<- s
...
e es p ->
```
Vázané relace jsou podobné vzoru Noise IK.

```
<- s
...
e es s ss p ->
<- tag e ee se
<- p
p ->
```
#### Bezpečnostní vlastnosti

Při použití terminologie Noise je sekvence ustanovení a dat následující: (Vlastnosti zabezpečení datové části z [Noise](https://noiseprotocol.org/noise.html) )

```
IK(s, rs):           Authentication   Confidentiality
  <- s
  ...
  -> e, es, s, ss           1                2
  <- e, ee, se              2                4
  ->                        2                5
  <-                        2                5
```
#### Rozdíly oproti XK

IK handshakes mají několik rozdílů oproti XK handshakes používaným v [NTCP2](/docs/specs/ntcp2/) a [SSU2](/docs/specs/ssu2/).

- Celkem čtyři DH operace ve srovnání se třemi pro XK
- Autentizace odesílatele v první zprávě: Užitečné zatížení je autentizováno
  jako patřící vlastníkovi veřejného klíče odesílatele, ačkoli
  klíč mohl být kompromitován (Authentication 1) XK vyžaduje další
  round trip před tím, než je Alice autentizována.
- Úplná forward secrecy (Confidentiality 5) po druhé zprávě. Bob
  může odeslat užitečné zatížení ihned po druhé zprávě s úplnou
  forward secrecy. XK vyžaduje další round trip pro úplnou forward
  secrecy.

Shrnutí: IK umožňuje 1-RTT doručení odpovědní zátěže od Boba k Alici s plnou forward secrecy, avšak požadavková zátěž není forward-secret.

### Relace

Protokol ElGamal/AES+SessionTag je jednosměrný. Na této vrstvě příjemce neví, odkud zpráva pochází. Odchozí a příchozí relace nejsou asociovány. Potvrzení jsou mimo pásmo pomocí DeliveryStatusMessage (zabalené v GarlicMessage) v segmentu.

Pro tuto specifikaci definujeme dva mechanismy pro vytvoření obousměrného protokolu - "párování" a "vázání". Tyto mechanismy poskytují zvýšenou efektivitu a bezpečnost.

#### Kontext relace

Stejně jako u ElGamal/AES+SessionTags, všechny příchozí a odchozí relace musí být v daném kontextu, buď v kontextu routeru nebo v kontextu pro konkrétní lokální cíl. V Java I2P se tento kontext nazývá Session Key Manager.

Relace nesmí být sdíleny mezi kontexty, protože by to umožnilo korelaci mezi různými lokálními destinacemi nebo mezi lokální destinací a routerem.

Když daná destinace podporuje jak ElGamal/AES+SessionTags, tak i tuto specifikaci, oba typy relací mohou sdílet kontext. Viz sekce 1c) níže.

#### Párování příchozích a odchozích relací

Když je vytvořena odchozí relace u původce (Alice), je vytvořena nová příchozí relace a spárována s odchozí relací, pokud se neočekává odpověď (např. surové datagramy).

Nová příchozí relace je vždy spárována s novou odchozí relací, pokud není požadována žádná odpověď (např. raw datagramy).

Pokud je požadována odpověď a je vázána na vzdálený cíl nebo router, tato nová odchozí relace je vázána na tento cíl nebo router a nahrazuje jakoukoliv předchozí odchozí relaci k tomuto cíli nebo routeru.

Párování příchozích a odchozích relací poskytuje obousměrný protokol s možností postupného obnovování DH klíčů.

#### Vazba relací a destinací

K danému cíli nebo routeru existuje pouze jedna odchozí relace. Z daného cíle nebo routeru může existovat několik aktuálních příchozích relací. Obecně, když je vytvořena nová příchozí relace a je na ní přijat provoz (který slouží jako ACK), všechny ostatní budou označeny k vypršení relativně rychle, během minuty nebo tak nějak. Je zkontrolována hodnota předchozích odeslaných zpráv (PN), a pokud v předchozí příchozí relaci nejsou žádné nepřijaté zprávy (v rámci velikosti okna), může být předchozí relace okamžitě smazána.

Když je u původce (Alice) vytvořena odchozí relace, je vázána na cílovou destinaci (Bob) a jakákoliv spárovaná příchozí relace bude také vázána na cílovou destinaci. Jak se relace posunují, zůstávají nadále vázány na cílovou destinaci.

Když je na straně příjemce (Bob) vytvořena příchozí relace, může být na volbu Alice svázána se vzdáleným Destination (Alice). Pokud Alice zahrne informace o vazbě (svůj statický klíč) do zprávy New Session, relace bude svázána s tímto destination a bude vytvořena odchozí relace svázaná se stejným Destination. Jak se relace vyvíjejí, zůstávají nadále svázané se vzdáleným Destination.

#### Výhody vazby a párování

Pro běžný případ streamování očekáváme, že Alice a Bob budou používat protokol následovně:

- Alice spáruje svou novou odchozí relaci s novou příchozí relací, obě
  vázané na vzdálený cíl (Bob).
- Alice zahrne informace o párování a podpis, a požadavek na odpověď,
  do zprávy New Session odeslané Bobovi.
- Bob spáruje svou novou příchozí relaci s novou odchozí relací, obě
  vázané na vzdálený cíl (Alice).
- Bob pošle odpověď (potvrzení) Alice v spárované relaci, s ratchet
  na nový DH klíč.
- Alice provede ratchet na novou odchozí relaci s Bobovým novým klíčem, spárovanou
  s existující příchozí relací.

Svázáním příchozí relace se vzdálenou destinací a spárováním příchozí relace s odchozí relací svázanou se stejnou destinací dosáhneme dvou hlavních výhod:

1)  Počáteční odpověď od Boba k Alice používá ephemeral-ephemeral DH

2\) Poté, co Alice obdrží Bobovu odpověď a provede ratchet, všechny následující zprávy od Alice k Bobovi používají ephemeral-ephemeral DH.

#### Potvrzení zpráv (ACK)

V ElGamal/AES+SessionTags, když je LeaseSet zabalen jako garlic clove, nebo jsou doručeny tagy, odesílající router požaduje ACK. Toto je samostatný garlic clove obsahující DeliveryStatus zprávu. Pro dodatečnou bezpečnost je DeliveryStatus zpráva zabalena do Garlic zprávy. Tento mechanismus je z pohledu protokolu out-of-band.

V novém protokolu, jelikož jsou vstupní a výstupní relace spárovány, můžeme mít ACK v rámci datového pásma. Není vyžadován žádný samostatný clove.

Explicitní ACK je jednoduše zpráva Existing Session bez I2NP bloku. Ve většině případů se však explicitnímu ACK lze vyhnout, protože existuje zpětný provoz. Pro implementace může být žádoucí počkat krátkou dobu (možná sto ms) před odesláním explicitního ACK, aby měla streamovací nebo aplikační vrstva čas na odpověď.

Implementace budou také muset odložit jakékoli odesílání ACK až po zpracování I2NP bloku, protože Garlic Message může obsahovat Database Store Message s lease set. Aktuální lease set bude nutný pro směrování ACK a vzdálený cíl (obsažený v lease set) bude nutný pro ověření binding static key.

#### Vypršení relace

Odchozí relace by měly vždy vypršet před příchozími relacemi. Když odchozí relace vyprší a je vytvořena nová, bude také vytvořena nová spárovaná příchozí relace. Pokud existovala stará příchozí relace, bude jí umožněno vypršet.

### Multicast

TBD

### Definice

Definujeme následující funkce odpovídající použitým kryptografickým stavebním blokům.

ZEROLEN

pole bajtů nulové délky

CSRNG(n)

n-bytový výstup z kryptograficky bezpečného generátoru náhodných čísel

    generator.

H(p, d)

SHA-256 hash funkce, která přijímá personalizační řetězec p a data

    d, and produces an output of length 32 bytes. As defined in
    [NOISE](https://noiseprotocol.org/noise.html). || below means append.

    Use SHA-256 as follows:

        H(p, d) := SHA-256(p || d)

MixHash(d)

SHA-256 hash funkce, která přijímá předchozí hash h a nová data d,

    and produces an output of length 32 bytes. || below means append.

    Use SHA-256 as follows:

        MixHash(d) := h = SHA-256(h || d)

STREAM

ChaCha20/Poly1305 AEAD jak je specifikován v

    [RFC-7539](https://tools.ietf.org/html/rfc7539). S_KEY_LEN = 32 and S_IV_LEN =
    12.

    ENCRYPT(k, n, plaintext, ad)

    :   Encrypts plaintext using the cipher key k, and nonce n which
        MUST be unique for the key k. Associated data ad is optional.
        Returns a ciphertext that is the size of the plaintext + 16
        bytes for the HMAC.

        The entire ciphertext must be indistinguishable from random if
        the key is secret.

    DECRYPT(k, n, ciphertext, ad)

    :   Decrypts ciphertext using the cipher key k, and nonce n.
        Associated data ad is optional. Returns the plaintext.

DH

Systém dohody na veřejných klíčích X25519. Soukromé klíče o délce 32 bajtů, veřejné

    keys of 32 bytes, produces outputs of 32 bytes. It has the following
    functions:

    GENERATE_PRIVATE()

    :   Generates a new private key.

    DERIVE_PUBLIC(privkey)

    :   Returns the public key corresponding to the given private key.

    GENERATE_PRIVATE_ELG2()

    :   Generates a new private key that maps to a public key suitable
        for Elligator2 encoding. Note that half of the
        randomly-generated private keys will not be suitable and must be
        discarded.

    ENCODE_ELG2(pubkey)

    :   Returns the Elligator2-encoded public key corresponding to the
        given public key (inverse mapping). Encoded keys are little
        endian. Encoded key must be 256 bits indistinguishable from
        random data. See Elligator2 section below for specification.

    DECODE_ELG2(pubkey)

    :   Returns the public key corresponding to the given
        Elligator2-encoded public key. See Elligator2 section below for
        specification.

    DH(privkey, pubkey)

    :   Generates a shared secret from the given private and public
        keys.

HKDF(salt, ikm, info, n)

Kryptografická funkce pro odvození klíče, která přijímá nějaký vstupní klíč

    material ikm (which should have good entropy but is not required to
    be a uniformly random string), a salt of length 32 bytes, and a
    context-specific 'info' value, and produces an output of n bytes
    suitable for use as key material.

    Use HKDF as specified in [RFC-5869](https://tools.ietf.org/html/rfc5869), using
    the HMAC hash function SHA-256 as specified in
    [RFC-2104](https://tools.ietf.org/html/rfc2104). This means that SALT_LEN is 32
    bytes max.

MixKey(d)

Použije HKDF() s předchozím chainKey a novými daty d, a nastaví nový

    chainKey and k. As defined in [NOISE](https://noiseprotocol.org/noise.html).

    Use HKDF as follows:

        MixKey(d) := output = HKDF(chainKey, d, "", 64)
                     chainKey = output[0:31]
                     k = output[32:63]

### 1) Formát zprávy

#### Přehled současného formátu zpráv

Garlic Message jak je specifikována v [I2NP](/docs/specs/i2np/) je následující. Jelikož návrhový cíl je, že prostřední uzly nemohou rozlišit nové od starého krypta, tento formát se nemůže změnit, i když je pole délky redundantní. Formát je zobrazen s úplnou 16-bajtovou hlavičkou, ačkoli skutečná hlavička může být v jiném formátu v závislosti na použitém transportu.

Po dešifrování data obsahují řadu Garlic Cloves a další data, také známá jako Clove Set.

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
#### Přehled formátu šifrovaných dat

V ElGamal/AES+SessionTags existují dva formáty zpráv:

1\) Nová relace: - 514 bajtový ElGamal blok - AES blok (minimálně 128 bajtů, násobek 16)

2\) Existující relace: - 32 bajtový Session Tag - AES blok (minimálně 128 bajtů, násobek 16)

Tyto zprávy jsou zapouzdřeny v I2NP garlic zprávě, která obsahuje pole délky, takže délka je známa.

Příjemce se nejprve pokusí vyhledat prvních 32 bajtů jako Session Tag. Pokud je nalezen, dešifruje AES blok. Pokud není nalezen a data mají délku alespoň (514+16), pokusí se dešifrovat ElGamal blok, a pokud je úspěšný, dešifruje AES blok.

#### Nové značky relace a srovnání se Signalem

V Signal Double Ratchet obsahuje hlavička:

- DH: Aktuální veřejný klíč ratchet
- PN: Délka zprávy předchozího řetězce
- N: Číslo zprávy

"Sending chains" protokolu Signal jsou zhruba ekvivalentní našim sadám tagů. Použitím session tagu můžeme většinu z toho eliminovat.

V New Session vkládáme pouze veřejný klíč do nešifrované hlavičky.

V Existující relaci používáme session tag pro hlavičku. Session tag je spojen s aktuálním ratchet veřejným klíčem a číslem zprávy.

V nové i existující relaci jsou PN a N v šifrovaném těle.

V Signalu se věci neustále rachetují. Nový DH veřejný klíč vyžaduje, aby příjemce provedl ratchet a poslal zpět nový veřejný klíč, což také slouží jako potvrzení pro přijatý veřejný klíč. To by pro nás bylo příliš mnoho DH operací. Proto oddělujeme potvrzení přijatého klíče a přenos nového veřejného klíče. Jakákoliv zpráva používající session tag vygenerovanou z nového DH veřejného klíče představuje potvrzení. Nový veřejný klíč přenášíme pouze tehdy, když chceme provést rekey.

Maximální počet zpráv před nutností ratchet DH je 65535.

Při doručování klíče relace z něj odvozujeme "Tag Set", místo aby bylo nutné doručovat také tagy relace. Tag Set může obsahovat až 65536 tagů. Příjemci by však měli implementovat strategii "dopředného hledání", místo aby generovali všechny možné tagy najednou. Generujte nanejvýš N tagů za posledním správně přijatým tagem. N může být nanejvýš 128, ale 32 nebo ještě méně může být lepší volbou.

### 1a) Nový formát relace

Nový jednorázový veřejný klíč relace (32 bajtů) Šifrovaná data a MAC (zbývající bajty)

Zpráva New Session může, ale nemusí obsahovat statický veřejný klíč odesílatele. Pokud je zahrnut, reverzní session je vázána na tento klíč. Statický klíč by měl být zahrnut, pokud se očekávají odpovědi, tj. pro streaming a odpovídatelné datagramy. Neměl by být zahrnut pro raw datagramy.

Zpráva New Session je podobná jednosměrnému Noise [NOISE](https://noiseprotocol.org/noise.html) vzoru "N" (pokud statický klíč není odeslán), nebo obousměrnému vzoru "IK" (pokud je statický klíč odeslán).

### 1b) Nový formát relace (s vazbou)

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
#### Nový dočasný klíč relace

Dočasný klíč má 32 bajtů a je kódován pomocí Elligator2. Tento klíč se nikdy znovu nepoužívá; nový klíč se generuje s každou zprávou, včetně opětovných přenosů.

#### Statický klíč

Po dešifrování, Alicin statický X25519 klíč, 32 bajtů.

#### Datová část

Délka šifrovaných dat je zbytek dat. Délka dešifrovaných dat je o 16 menší než délka šifrovaných dat. Payload musí obsahovat blok DateTime a obvykle bude obsahovat jeden nebo více bloků Garlic Clove. Viz sekce payload níže pro formát a další požadavky.

### 1c) Nový formát relace (bez vazby)

Pokud není vyžadována odpověď, žádný statický klíč se neposílá.

Délka je 96 + délka dat. Šifrovaný formát:

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
#### Nový dočasný klíč relace

Alicin dočasný klíč. Dočasný klíč má 32 bajtů, kódovaný pomocí Elligator2, little endian. Tento klíč se nikdy znovu nepoužívá; nový klíč se generuje pro každou zprávu, včetně opětovných přenosů.

#### Sekce příznaků Dešifrovaná data

Sekce Flags neobsahuje nic. Má vždy 32 bajtů, protože musí mít stejnou délku jako statický klíč pro zprávy New Session s vazbou. Bob určí, zda se jedná o statický klíč nebo sekci flags testováním, zda je všech 32 bajtů nulových.

TODO jsou zde potřeba nějaké příznaky?

#### Datová část

Šifrovaná délka je zbývající část dat. Dešifrovaná délka je o 16 menší než šifrovaná délka. Payload musí obsahovat DateTime blok a obvykle bude obsahovat jeden nebo více Garlic Clove bloků. Viz sekce payload níže pro formát a další požadavky.

### 1d) Jednorázový formát (bez vazby nebo relace)

Pokud se očekává odeslání pouze jedné zprávy, není nutné nastavení relace ani statický klíč.

Délka je 96 + délka datové části. Šifrovaný formát:

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
#### Nový jednorázový klíč relace

Jednorázový klíč má 32 bytů, kódovaný pomocí Elligator2, little endian. Tento klíč se nikdy znovu nepoužívá; nový klíč se generuje s každou zprávou, včetně opětovných přenosů.

#### Sekce příznaků Dešifrovaná data

Sekce Flags neobsahuje nic. Má vždy 32 bajtů, protože musí mít stejnou délku jako statický klíč pro zprávy New Session s vazbou. Bob určí, zda se jedná o statický klíč nebo sekci flags testováním, zda je všech 32 bajtů nulových.

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
#### Datová část

Šifrovaná délka je zbytek dat. Dešifrovaná délka je o 16 menší než šifrovaná délka. Payload musí obsahovat DateTime blok a obvykle bude obsahovat jeden nebo více Garlic Clove bloků. Viz sekce payload níže pro formát a další požadavky.

### 1f) KDF pro zprávy nové relace

#### KDF pro počáteční ChainKey

Toto je standardní [NOISE](https://noiseprotocol.org/noise.html) pro IK s upraveným názvem protokolu. Všimněte si, že používáme stejný inicializátor jak pro IK vzor (vázané relace), tak pro N vzor (nevázané relace).

Název protokolu je upraven ze dvou důvodů. Za prvé, aby označoval, že efemérní klíče jsou kódovány pomocí Elligator2, a za druhé, aby označoval, že MixHash() je volána před druhou zprávou pro zamíchání hodnoty tagu.

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
#### KDF pro šifrovaný obsah sekce Flags/Static Key

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
#### KDF pro sekci Payload (se statickým klíčem Alice)

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
#### KDF pro sekci užitečného zatížení (bez statického klíče Alice)

Poznamenejte, že se jedná o Noise "N" vzor, ale používáme stejný "IK" inicializátor jako pro vázané relace.

Zprávy New Session nelze identifikovat jako obsahující Alicein statický klíč, dokud není statický klíč dešifrován a prozkoumán, aby se určilo, zda obsahuje samé nuly. Proto musí příjemce použít stavový automat "IK" pro všechny zprávy New Session. Pokud je statický klíč tvořen samými nulami, musí být vzor zprávy "ss" přeskočen.

```
chainKey = from Flags/Static key section
k = from Flags/Static key section
n = 1
ad = h from Flags/Static key section
ciphertext = ENCRYPT(k, n, payload, ad)
```
### 1g) Formát odpovědi nové relace

Jedna nebo více New Session Replies může být odesláno v odpovědi na jedinou New Session zprávu. Každá odpověď je předpojena značkou, která je generována z TagSet pro danou relaci.

New Session Reply se skládá ze dvou částí. První část je dokončení Noise IK handshake s předřazeným tagem. Délka první části je 56 bajtů. Druhá část je payload datové fáze. Délka druhé části je 16 + délka payload.

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
#### Značka relace

Tag je generován v Session Tags KDF, jak je inicializován v DH Initialization KDF níže. Toto koreluje odpověď se session. Session Key z DH Initialization se nepoužívá.

#### Dočasný klíč odpovědi nové relace

Bobův dočasný klíč. Dočasný klíč má 32 bajtů, kódovaný pomocí Elligator2, little endian. Tento klíč se nikdy znovu nepoužívá; nový klíč se generuje s každou zprávou, včetně opakovaných přenosů.

#### Datová část

Délka šifrovaných dat je zbytek dat. Délka dešifrovaných dat je o 16 menší než délka šifrovaných dat. Payload obvykle obsahuje jeden nebo více bloků Garlic Clove. Viz sekce payload níže pro formát a další požadavky.

#### KDF pro Reply TagSet

Jeden nebo více tagů je vytvořeno z TagSet, který je inicializován pomocí níže uvedené KDF, za použití chainKey ze zprávy New Session.

```
// Generate tagset

tagsetKey = HKDF(chainKey, ZEROLEN, "SessionReplyTags", 32)
    tagset_nsr = DH_INITIALIZE(chainKey, tagsetKey)

```
#### KDF pro šifrovaný obsah sekce Reply Key

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
#### KDF pro šifrovaný obsah sekce Payload

Toto je jako první zpráva Existing Session po rozdělení, ale bez samostatného tagu. Navíc používáme hash z výše uvedeného pro spojení payload s NSR zprávou.

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
### Poznámky

Může být odesláno více NSR zpráv v odpovědi, každá s jedinečnými dočasnými klíči, v závislosti na velikosti odpovědi.

Alice a Bob jsou povinni používat nové dočasné klíče pro každou NS a NSR zprávu.

Alice musí obdržet jednu z Bobových NSR zpráv před odesláním zpráv Existing Session (ES), a Bob musí obdržet ES zprávu od Alice před odesláním ES zpráv.

`chainKey` a `k` z Bob's NSR Payload Section jsou použity jako vstupy pro počáteční ES DH Ratchets (oba směry, viz DH Ratchet KDF).

Bob musí zachovat pouze Existující Relace pro ES zprávy přijaté od Alice. Jakékoli jiné vytvořené příchozí a odchozí relace (pro více NSR) by měly být zničeny okamžitě po přijetí Alice's první ES zprávy pro danou relaci.

### 1h) Formát existující relace

Session tag (8 bytů) Šifrovaná data a MAC (viz sekce 3 níže)

#### Formát

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
#### Užitečná data

Šifrovaná délka je zbytek dat. Dešifrovaná délka je o 16 menší než šifrovaná délka. Viz sekce payload níže pro formát a požadavky.

#### KDF

```
See AEAD section below.

// AEAD parameters for Existing Session payload
k = The 32-byte session key associated with this session tag
n = The message number N in the current chain, as retrieved from the associated Session Tag.
ad = The session tag, 8 bytes
ciphertext = ENCRYPT(k, n, payload, ad)
```
### 2) ECIES-X25519

Formát: 32bajtové veřejné a soukromé klíče, little-endian.

### 2a) Elligator2

Ve standardních Noise handshake postupech začínají počáteční handshake zprávy v každém směru dočasnými klíči, které jsou přenášeny v otevřeném textu. Jelikož platné X25519 klíče jsou rozlišitelné od náhodných dat, může útočník typu man-in-the-middle rozlišit tyto zprávy od zpráv Existing Session, které začínají náhodnými session tagy. V [NTCP2](/docs/specs/ntcp2/) ([Prop111](/proposals/111-ntcp2/)) jsme použili nízkonákladovou XOR funkci využívající out-of-band statický klíč k zakrytí klíče. Nicméně model hrozeb je zde odlišný; nechceme umožnit žádnému MitM použít jakékoliv prostředky k potvrzení cíle provozu nebo k rozlišení počátečních handshake zpráv od zpráv Existing Session.

Proto se používá [Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf) k transformaci dočasných klíčů ve zprávách New Session a New Session Reply tak, aby byly nerozlišitelné od uniformně náhodných řetězců.

#### Formát

32bajtové veřejné a soukromé klíče. Kódované klíče jsou ve formátu little endian.

Jak je definováno v [Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf), kódované klíče jsou nerozeznatelné od 254 náhodných bitů. Vyžadujeme 256 náhodných bitů (32 bajtů). Kódování a dekódování jsou proto definovány následovně:

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
#### Poznámky

Elligator2 zdvojnásobuje průměrnou dobu generování klíčů, protože polovina privátních klíčů vede k veřejným klíčům, které nejsou vhodné pro kódování pomocí Elligator2. Doba generování klíčů je také neomezená s exponenciálním rozložením, protože generátor musí pokračovat v opakování, dokud nenajde vhodný pár klíčů.

Tato režie může být zvládnuta předběžným generováním klíčů v samostatném vlákně, aby byl udržován fond vhodných klíčů.

Generátor provádí funkci ENCODE_ELG2() k určení vhodnosti. Proto by měl generátor uložit výsledek ENCODE_ELG2(), aby nemusel být znovu vypočítán.

Navíc mohou být nevhodné klíče přidány do fondu klíčů používaných pro [NTCP2](/docs/specs/ntcp2/), kde se Elligator2 nepoužívá. Bezpečnostní problémy takového postupu jsou zatím neurčeny.

### 3) AEAD (ChaChaPoly)

AEAD používající ChaCha20 a Poly1305, stejně jako v [NTCP2](/docs/specs/ntcp2/). To odpovídá [RFC-7539](https://tools.ietf.org/html/rfc7539), který se také podobně používá v TLS [RFC-7905](https://tools.ietf.org/html/rfc7905).

#### Vstupy New Session a New Session Reply

Vstupy pro funkce šifrování/dešifrování pro AEAD blok ve zprávě New Session:

```
k :: 32 byte cipher key
     See New Session and New Session Reply KDFs above.

n :: Counter-based nonce, 12 bytes.
     n = 0

ad :: Associated data, 32 bytes.
      The SHA256 hash of the preceding data, as output from mixHash()

data :: Plaintext data, 0 or more bytes
```
#### Vstupy existující relace

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
#### Šifrovaný formát

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
#### Poznámky

- Protože ChaCha20 je proudová šifra, plaintexty nemusí být doplněny. Dodatečné bajty klíčového proudu jsou zahozeny.
- Klíč pro šifru (256 bitů) je dohodnut prostřednictvím SHA256 KDF. Podrobnosti KDF pro každou zprávu jsou v samostatných sekcích níže.
- ChaChaPoly rámce mají známou velikost, protože jsou zapouzdřeny v I2NP datové zprávě.
- Pro všechny zprávy je vyplnění uvnitř autentifikovaného datového rámce.

#### Zpracování chyb AEAD

Všechna přijatá data, která neprošla AEAD verifikací, musí být zahozena. Nevrací se žádná odpověď.

### 4) Ratchets

Stále používáme session tags jako dříve, ale k jejich generování používáme ratchets. Session tags také měly možnost rekeying, kterou jsme nikdy neimplementovali. Takže je to jako double ratchet, ale tu druhou jsme nikdy neudělali.

Zde definujeme něco podobného Signal Double Ratchet. Tagy relace jsou generovány deterministicky a identicky na straně příjemce i odesílatele.

Použitím symetrického klíč/tag ratchet mechanismu eliminujeme využití paměti pro ukládání session tagů na straně odesílatele. Také eliminujeme spotřebu šířky pásma při odesílání sad tagů. Využití na straně příjemce je stále významné, ale můžeme ho dále snížit, protože zmenšíme session tag z 32 bajtů na 8 bajtů.

Nepoužíváme šifrování hlaviček, jak je specifikováno (a volitelné) v Signal, místo toho používáme session tags.

Použitím DH ratchet dosahujeme dopředné tajnosti, která nebyla nikdy implementována v ElGamal/AES+SessionTags.

Poznámka: Jednorázový veřejný klíč New Session není součástí ratchet mechanismu, jeho jedinou funkcí je zašifrovat Alicin počáteční DH ratchet klíč.

#### Čísla zpráv

Double Ratchet zpracovává ztracené nebo neuspořádané zprávy tím, že do každého hlavičky zprávy zahrnuje tag. Příjemce vyhledá index tagu, což je číslo zprávy N. Pokud zpráva obsahuje blok Message Number s hodnotou PN, příjemce může smazat všechny tagy vyšší než tato hodnota v předchozí sadě tagů, zatímco si ponechá přeskočené tagy z předchozí sady tagů pro případ, že přeskočené zprávy dorazí později.

#### Ukázková implementace

Definujeme následující datové struktury a funkce pro implementaci těchto ratchetů.

TAGSET_ENTRY

Jednotlivý záznam v TAGSET.

    INDEX

    :   An integer index, starting with 0

    SESSION_TAG

    :   An identifier to go out on the wire, 8 bytes

    SESSION_KEY

    :   A symmetric key, never goes on the wire, 32 bytes

TAGSET

Kolekce TAGSET_ENTRIES.

    CREATE(key, n)

    :   Generate a new TAGSET using initial cryptographic key material
        of 32 bytes. The associated session identifier is provided. The
        initial number of of tags to create is specified; this is
        generally 0 or 1 for an outgoing session. LAST_INDEX = -1
        EXTEND(n) is called.

    EXTEND(n)

    :   Generate n more TAGSET_ENTRIES by calling EXTEND() n times.

    EXTEND()

    :   Generate one more TAGSET_ENTRY, unless the maximum number
        SESSION_TAGS have already been generated. If LAST_INDEX is
        greater than or equal to 65535, return. ++ LAST_INDEX Create a
        new TAGSET_ENTRY with the LAST_INDEX value and the calculated
        SESSION_TAG. Calls RATCHET_TAG() and (optionally) RATCHET_KEY().
        For inbound sessions, the calculation of the SESSION_KEY may be
        deferred and calculated in GET_SESSION_KEY(). Calls EXPIRE()

    EXPIRE()

    :   Remove tags and keys that are too old, or if the TAGSET size
        exceeds some limit.

    RATCHET_TAG()

    :   Calculates the next SESSION_TAG based on the last SESSION_TAG.

    RATCHET_KEY()

    :   Calculates the next SESSION_KEY based on the last SESSION_KEY.

    SESSION

    :   The associated session.

    CREATION_TIME

    :   When the TAGSET was created.

    LAST_INDEX

    :   The last TAGSET_ENTRY INDEX generated by EXTEND().

    GET_NEXT_ENTRY()

    :   Used for outgoing sessions only. EXTEND(1) is called if there
        are no remaining TAGSET_ENTRIES. If EXTEND(1) did nothing, the
        max of 65535 TAGSETS have been used, and return an error.
        Returns the next unused TAGSET_ENTRY.

    GET_SESSION_KEY(sessionTag)

    :   Used for incoming sessions only. Returns the TAGSET_ENTRY
        containing the sessionTag. If found, the TAGSET_ENTRY is
        removed. If the SESSION_KEY calculation was deferred, it is
        calculated now. If there are few TAGSET_ENTRIES remaining,
        EXTEND(n) is called.

#### 4a) DH Ratchet

Ratchets, ale zdaleka ne tak rychle jako Signal. Oddělujeme potvrzení přijatého klíče od generování nového klíče. Při typickém použití Alice a Bob každý provede ratchet (dvakrát) okamžitě v New Session, ale již nebudou provádět ratchet znovu.

Všimněte si, že ratchet je pro jeden směr a generuje řetěz ratchetu New Session tag / message key pro tento směr. Pro generování klíčů pro oba směry musíte provést ratchet dvakrát.

Posouváte se v ratchet algoritmu pokaždé, když vygenerujete a odešlete nový klíč. Posouváte se v ratchet algoritmu pokaždé, když obdržíte nový klíč.

Alice provede ratchet jednou při vytváření nevázané odchozí relace, nevytváří příchozí relaci (nevázaná relace neumožňuje odpověď).

Bob provede jeden ratchet při vytváření nevázané příchozí relace a nevytváří odpovídající odchozí relaci (nevázaná relace není zodpověditelná).

Alice pokračuje v odesílání zpráv New Session (NS) Bobovi, dokud neobdrží jednu z Bobových zpráv New Session Reply (NSR). Poté použije výsledky KDF z Payload Section zprávy NSR jako vstupy pro session ratchets (viz DH Ratchet KDF) a začne odesílat zprávy Existing Session (ES).

Pro každou přijatou NS zprávu vytvoří Bob novou příchozí relaci, přičemž použije výsledky KDF ze sekce Payload odpovědi jako vstupy pro nový příchozí a odchozí ES DH Ratchet.

Pro každou požadovanou odpověď pošle Bob Alici NSR zprávu s odpovědí v datové části. Je vyžadováno, aby Bob použil nové dočasné klíče pro každou NSR.

Bob musí obdržet ES zprávu od Alice na jedné z příchozích relací, před vytvořením a odesláním ES zpráv na odpovídající odchozí relaci.

Alice by měla použít časovač pro přijímání NSR zprávy od Boba. Pokud časovač vyprší, relace by měla být odstraněna.

Aby se předešlo útoku KCI a/nebo vyčerpání zdrojů, kdy útočník zahazuje Bobovy NSR odpovědi, aby Alice pokračovala v odesílání NS zpráv, měla by se Alice vyhnout zahajování nových relací s Bobem po určitém počtu opakovaných pokusů způsobených vypršením časovače.

Alice a Bob každý provádějí DH ratchet pro každý přijatý blok NextKey.

Alice a Bob vygenerují nové tag sady a dva symetrické klíče ratchets po každém DH ratchet. Pro každou novou ES zprávu v daném směru Alice a Bob posunou session tag a symetrické klíče ratchets.

Frekvence DH ratchets po počátečním handshake závisí na implementaci. Zatímco protokol stanovuje limit 65535 zpráv před požadovaným ratchet, častější ratcheting (založený na počtu zpráv, uplynulém čase nebo obojím) může poskytovat dodatečnou bezpečnost.

Po finálním handshake KDF na vázaných relacích musí Bob a Alice spustit funkci Noise Split() na výsledném CipherState pro vytvoření nezávislých symetrických a tag chain klíčů pro příchozí a odchozí relace.

##### ID SADY KLÍČŮ A TAGŮ

Čísla ID klíčů a sad tagů se používají k identifikaci klíčů a sad tagů. ID klíčů se používají v blocích NextKey k identifikaci odeslaného nebo použitého klíče. ID sad tagů se používají (společně s číslem zprávy) v blocích ACK k identifikaci potvrzované zprávy. ID klíčů i sad tagů se vztahují k sadám tagů pro jediný směr. Čísla ID klíčů a sad tagů musí být sekvenční.

V prvních sadách tagů použitých pro relaci v každém směru je ID sady tagů 0. Nebyly odeslány žádné bloky NextKey, takže neexistují žádné ID klíčů.

Pro zahájení DH ratchet pošle odesílatel nový blok NextKey s ID klíče 0. Příjemce odpoví novým blokem NextKey s ID klíče 0. Odesílatel pak začne používat novou sadu tagů s ID sady tagů 1.

Následující sady tagů jsou generovány podobně. Pro všechny sady tagů používané po NextKey výměnách je číslo sady tagů (1 + Alice's key ID + Bob's key ID).

ID klíčů a sad tagů začínají na 0 a postupně se zvyšují. Maximální ID sady tagů je 65535. Maximální ID klíče je 32767. Když je sada tagů téměř vyčerpána, odesílatel sady tagů musí zahájit výměnu NextKey. Když je sada tagů 65535 téměř vyčerpána, odesílatel sady tagů musí zahájit novou relaci odesláním zprávy New Session.

S maximální velikostí streamované zprávy 1730 a za předpokladu žádných retransmisí je teoretické maximum přenosu dat pomocí jedné sady tagů 1730 * 65536 ~= 108 MB. Skutečné maximum bude nižší kvůli retransmisím.

Teoretické maximum přenosu dat se všemi 65536 dostupnými sadami tagů, než by musela být relace zahozena a nahrazena, je 64K * 108 MB ~= 6,9 TB.

##### TOK ZPRÁV DH RATCHET

Další výměna klíčů pro sadu tagů musí být zahájena odesílatelem těchto tagů (vlastníkem odchozí sady tagů). Příjemce (vlastník příchozí sady tagů) odpoví. Pro typický HTTP GET provoz na aplikační vrstvě bude Bob posílat více zpráv a bude ratchet jako první zahájením výměny klíčů; diagram níže to ukazuje. Když Alice provede ratchet, děje se totéž v opačném směru.

První sada tagů použitá po handshake NS/NSR je sada tagů 0. Když je sada tagů 0 téměř vyčerpána, musí být vyměněny nové klíče v obou směrech pro vytvoření sady tagů 1. Poté je nový klíč zasílán pouze jedním směrem.

Pro vytvoření sady tagů 2 pošle odesílatel tagu nový klíč a příjemce tagu pošle ID svého starého klíče jako potvrzení. Obě strany provedou DH.

Pro vytvoření tag set 3 pošle odesílatel tagu ID svého starého klíče a požádá příjemce tagu o nový klíč. Obě strany provedou DH.

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
Po dokončení DH ratchet pro odchozí tagset a vytvoření nového odchozího tagsetu by měl být použit okamžitě a starý odchozí tagset může být smazán.

Po dokončení DH ratchet pro příchozí tagset a vytvoření nového příchozího tagset by měl příjemce naslouchat tagům v obou tagsetech a smazat starý tagset po krátké době, přibližně 3 minuty.

Souhrn postupu sady tagů a ID klíčů je v tabulce níže. * označuje, že je vygenerován nový klíč.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">New Tag Set ID</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Sender key ID</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Rcvr key ID</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">n/a</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">n/a</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 *</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 *</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 *</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 *</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2 *</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2 *</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">...</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">...</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">...</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">65534</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32767 *</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32766</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">65535</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32767</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32767 *</td>
</tr>
</table>
Čísla ID klíčů a sad tagů musí být postupná.

##### DH INITIALIZATION KDF

Toto je definice DH_INITIALIZE(rootKey, k) pro jeden směr. Vytváří tagset a "další root key" k použití pro následný DH ratchet v případě potřeby.

DH inicializaci používáme na třech místech. Zaprvé ji používáme k vygenerování sady tagů pro New Session Replies. Zadruhé ji používáme k vygenerování dvou sad tagů, jedné pro každý směr, pro použití ve zprávách Existing Session. Nakonec ji používáme po DH Ratchet k vygenerování nové sady tagů v jednom směru pro další zprávy Existing Session.

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
##### DH RATCHET KDF

Toto se používá poté, co jsou vyměněny nové DH klíče v NextKey blocích, před vyčerpáním tagset.

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
#### 4b) Session Tag Ratchet

Ratchety pro každou zprávu, jako v aplikaci Signal. Ratchet značky relace je synchronizován s ratchetem symetrického klíče, ale ratchet přijímacího klíče může "zaostávat" za účelem úspory paměti.

Transmitter se posouvá jednou pro každou odeslanou zprávu. Nemusí se ukládat žádné další značky. Transmitter musí také udržovat čítač pro 'N', což je číslo zprávy v aktuálním řetězci. Hodnota 'N' je zahrnuta v odeslané zprávě. Viz definice bloku Message Number.

Příjemce musí posunout ratchet dopředu o maximální velikost okna a uložit tagy do "sady tagů", která je přidružena k relaci. Jakmile je tag přijat, může být uložený tag zahozen, a pokud nejsou žádné předchozí nepřijaté tagy, okno může být posunuto dopředu. Příjemce by měl uchovávat hodnotu 'N' přidruženou ke každému tagu relace a zkontrolovat, že číslo v odeslané zprávě odpovídá této hodnotě. Viz definice bloku Message Number.

##### KDF

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
#### 4c) Ratchet symetrického klíče

Ratchets pro každou zprávu, stejně jako v Signal. Každý symetrický klíč má přiřazené číslo zprávy a session tag. Session key ratchet je synchronizován se symetrickým tag ratchet, ale receiver key ratchet může "zaostávat" kvůli úspoře paměti.

Transmitter ratchet se posune jednou pro každou odeslanou zprávu. Není nutné ukládat žádné další klíče.

Když příjemce obdrží session tag, pokud ještě neposunul symetrický key ratchet dopředu k přidruženému klíči, musí se k přidruženému klíči "dohnat". Příjemce pravděpodobně uloží do cache klíče pro všechny předchozí tagy, které ještě nebyly přijaty. Po přijetí může být uložený klíč zahozen, a pokud neexistují žádné předchozí nepřijaté tagy, může být okno posunuto vpřed.

Pro efektivitu jsou session tag a symmetric key ratchets oddělené, takže session tag ratchet může běžet před symmetric key ratchet. To také poskytuje dodatečné zabezpečení, protože session tagy odcházejí po drátě.

##### KDF

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
### 5) Payload

Toto nahrazuje formát sekce AES definovaný ve specifikaci ElGamal/AES+SessionTags.

Toto používá stejný formát bloku, jak je definován ve specifikaci [NTCP2](/docs/specs/ntcp2/). Jednotlivé typy bloků jsou definovány odlišně.

Existují obavy, že povzbuzování implementátorů ke sdílení kódu může vést k problémům s parsováním. Implementátoři by měli pečlivě zvážit přínosy a rizika sdílení kódu a zajistit, že pravidla pro řazení a platné bloky jsou pro tyto dva kontexty odlišná.

#### Payload Section Dešifrovaná data

Šifrovaná délka je zbytek dat. Dešifrovaná délka je o 16 kratší než šifrovaná délka. Všechny typy bloků jsou podporovány. Typický obsah zahrnuje následující bloky:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Payload Block Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type Number</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Block Length</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">DateTime</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Termination (TBD)</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">9 typ.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Options (TBD)</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">21+</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Message Number (TBD)</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">TBD</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Next Key</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3 or 35</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">ACK</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4 typ.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">ACK Request</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">9</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Garlic Clove</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">varies</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Padding</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">254</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">varies</td>
</tr>
</table>
#### Nešifrovaná data

V šifrovaném rámci je nula nebo více bloků. Každý blok obsahuje jednobytový identifikátor, dvoubajtovou délku a nula nebo více bajtů dat.

Pro rozšiřitelnost MUSÍ příjemci ignorovat bloky s neznámými čísly typů a zacházet s nimi jako s výplní.

Šifrovaná data mají maximálně 65535 bajtů, včetně 16bajtové autentizační hlavičky, takže maximální nešifrovaná data jsou 65519 bajtů.

(Poly1305 auth tag nezobrazena):

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
#### Pravidla řazení bloků

Ve zprávě New Session je blok DateTime povinný a musí být prvním blokem.

Další povolené bloky:

- Garlic Clove (typ 11)
- Možnosti (typ 5)
- Výplň (typ 254)

Ve zprávě New Session Reply nejsou vyžadovány žádné bloky.

Další povolené bloky:

- Garlic Clove (typ 11)
- Možnosti (typ 5)
- Výplň (typ 254)

Žádné další bloky nejsou povoleny. Padding, pokud je přítomen, musí být posledním blokem.

Ve zprávě Existing Session nejsou vyžadovány žádné bloky a pořadí není specifikováno, kromě následujících požadavků:

Ukončení, pokud je přítomno, musí být posledním blokem kromě odsazení. Odsazení, pokud je přítomno, musí být posledním blokem.

V jednom rámci může být více bloků Garlic Clove. V jednom rámci mohou být až dva bloky Next Key. Více bloků Padding není v jednom rámci povoleno. Ostatní typy bloků pravděpodobně nebudou mít více bloků v jednom rámci, ale není to zakázáno.

#### DateTime

Doba vypršení. Pomáhá předcházet replay útokům. Bob musí ověřit, že je zpráva aktuální, pomocí tohoto časového razítka. Bob musí implementovat Bloom filtr nebo jiný mechanismus pro předcházení replay útokům, pokud je čas platný. Bob může také použít dřívější kontrolu detekce replay pro duplicitní ephemeral klíč (buď před nebo po Elligator2 dekódování) k detekci a zahození nedávných duplicitních NS zpráv před dešifrováním. Obecně zahrnuto pouze ve zprávách New Session.

```
+----+----+----+----+----+----+----+
| 0  |    4    |     timestamp     |
+----+----+----+----+----+----+----+

blk :: 0
size :: 2 bytes, big endian, value = 4
timestamp :: Unix timestamp, unsigned seconds.
             Wraps around in 2106
```
#### Garlic Clove

Jeden dešifrovaný Garlic Clove jak je specifikován v [I2NP](/docs/specs/i2np/), s úpravami pro odstranění polí, která jsou nepoužívaná nebo redundantní. Upozornění: Tento formát se významně liší od formátu pro ElGamal/AES. Každý clove je samostatný payload blok. Garlic Cloves nesmí být fragmentovány napříč bloky nebo napříč ChaChaPoly rámci.

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
       the Garlic Clove section of [I2NP]_.
       Length varies but is typically 1, 33, or 37 bytes

type :: I2NP message type

Message_ID :: 4 byte `Integer` I2NP message ID

Expiration :: 4 bytes, seconds since the epoch
```
Poznámky:

- Implementátoři musí zajistit, že při čtení bloku nebudou poškozená nebo
  škodlivá data způsobovat čtení přesahující do dalšího bloku.
- Formát Clove Set specifikovaný v [I2NP](/docs/specs/i2np/) se
  nepoužívá. Každý clove je obsažen ve svém vlastním bloku.
- Hlavička I2NP zprávy má 9 bajtů s identickým formátem jako ten
  používaný v [NTCP2](/docs/specs/ntcp2/).
- Certificate, Message ID a Expiration z definice Garlic Message
  v [I2NP](/docs/specs/i2np/) nejsou zahrnuty.
- Certificate, Clove ID a Expiration z definice Garlic Clove
  v [I2NP](/docs/specs/i2np/) nejsou zahrnuty.

#### Ukončení

Implementace je volitelná. Ukončit relaci. Toto musí být poslední nepadovací blok v rámci. V této relaci nebudou odeslány žádné další zprávy.

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
#### Možnosti

NEIMPLEMENTOVÁNO, pro další studium. Předá aktualizované možnosti. Možnosti zahrnují různé parametry pro relaci. Více informací naleznete v sekci Analýza délky značky relace níže.

Blok možností může mít proměnnou délku, protože může být přítomen more_options.

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
SOTW je doporučení odesílatele pro příjemce ohledně okna příchozích značek příjemce (maximální předstih). RITW je prohlášení odesílatele o oknu příchozích značek (maximální předstih), které plánuje použít. Každá strana pak nastaví nebo upraví předstih na základě nějakého minima nebo maxima nebo jiného výpočtu.

Poznámky:

- Podpora pro nestandardní délku session tagu doufejme nikdy nebude
  vyžadována.
- Okno tagu je MAX_SKIP v dokumentaci Signal.

Problémy:

- Vyjednávání možností je TBD.
- Výchozí hodnoty TBD.
- Možnosti paddingu a zpoždění jsou zkopírovány z NTCP2, ale tyto možnosti
  tam nebyly plně implementovány nebo prostudovány.

#### Čísla zpráv

Implementace je volitelná. Délka (počet odeslaných zpráv) v předchozí sadě tagů (PN). Příjemce může okamžitě smazat tagy vyšší než PN z předchozí sady tagů. Příjemce může nechat vypršet tagy menší nebo rovny PN z předchozí sady tagů po krátké době (např. 2 minuty).

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
  Toto je podobné tomu, co dělá Signal, ale v Signal jsou PN a N v
  hlavičce. Zde jsou v šifrovaném těle zprávy.
- Neposílejte tento blok v sadě tagů 0, protože neexistovala žádná předchozí sada
  tagů.

#### Následující DH Ratchet veřejný klíč

Další DH ratchet klíč je v payload a je volitelný. Nerotujeme pokaždé. (Toto je odlišné od Signal, kde je v hlavičce a posílá se pokaždé)

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

- Key ID je inkrementální čítač pro lokální klíč používaný pro danou sadu tagů,
  začínající na 0.
- ID se nesmí změnit, pokud se nezmění klíč.
- Nemusí to být nezbytně nutné, ale je to užitečné pro ladění.
  Signal nepoužívá key ID.
- Maximální Key ID je 32767.
- Ve vzácném případě, kdy se sady tagů v obou směrech ratchetují
  současně, frame bude obsahovat dva Next Key bloky, jeden pro
  forward klíč a jeden pro reverse klíč.
- Čísla ID klíčů a sad tagů musí být sekvenční.
- Podrobnosti viz sekce DH Ratchet výše.

#### Potvrzení

Toto se odesílá pouze pokud byl přijat blok žádosti o potvrzení. Může být přítomno více potvrzení pro potvrzení více zpráv.

Není povoleno v NS nebo NSR. Zahrnuto pouze ve zprávách Existing Session.

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
- V prvních sadách tagů používaných pro relaci v každém směru je ID sady tagů 0.
- Nebyly odeslány žádné bloky NextKey, takže neexistují žádná ID klíčů.
- Pro všechny sady tagů používané po výměnách NextKey je číslo sady tagů (1 + ID klíče Alice + ID klíče Boba).

#### Žádost o potvrzení

Požádat o in-band potvrzení. Pro nahrazení out-of-band DeliveryStatus zprávy v Garlic Clove.

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
#### Výplň

Veškeré vyplňování je uvnitř AEAD rámců. TODO Vyplňování uvnitř AEAD by mělo přibližně odpovídat vyjednaným parametrům. TODO Alice poslala své požadované tx/rx min/max parametry ve zprávě NS. TODO Bob poslal své požadované tx/rx min/max parametry ve zprávě NSR. Aktualizované možnosti mohou být odeslány během datové fáze. Viz informace o bloku možností výše.

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

- Vyplňování samými nulami je v pořádku, protože bude zašifrováno.
- Strategie vyplňování budou určeny později.
- Rámce obsahující pouze vyplňování jsou povoleny.
- Výchozí vyplňování je 0-15 bajtů.
- Viz blok voleb pro vyjednávání parametrů vyplňování
- Viz blok voleb pro minimální/maximální parametry vyplňování
- Odpověď routeru na porušení vyjednaného vyplňování je
  závislá na implementaci.

#### Další typy bloků

Implementace by měly ignorovat neznámé typy bloků kvůli dopředné kompatibilitě.

#### Budoucí práce

- Délka padding má být buď rozhodována pro každou zprávu zvlášť na základě odhadů distribuce délky, nebo mají být přidány náhodné zpoždění. Tato protiopatření mají být zahrnuta pro odolnost vůči DPI, protože velikosti zpráv by jinak prozradily, že I2P provoz je přenášen transportním protokolem. Přesné schéma padding je oblastí budoucí práce, Příloha A poskytuje více informací k tomuto tématu.

## Typické vzorce použití

### HTTP GET

Toto je nejtypičtější případ použití a většina případů použití pro non-HTTP streaming bude identická s tímto případem použití. Je odeslána malá počáteční zpráva, následuje odpověď a další zprávy jsou odesílány v obou směrech.

HTTP GET se obecně vejde do jedné I2NP zprávy. Alice pošle malý požadavek s jedinou novou Session zprávou, která obsahuje odpověď leaseset. Alice zahrnuje okamžité přepnutí na nový klíč. Obsahuje podpis pro svázání s cílem. Není požadováno potvrzení.

Bob okamžitě provede ratchet.

Alice okamžitě provede ratchet.

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
### HTTP POST

Alice má tři možnosti:

1)  Odeslat pouze první zprávu (velikost okna = 1), jako u HTTP GET. Ne

    recommended.
2)  Odeslat až do streaming window, ale pomocí stejného Elligator2-kódovaného

    cleartext public key. All messages contain same next public key
    (ratchet). This will be visible to OBGW/IBEP because they all start
    with the same cleartext. Things proceed as in 1). Not recommended.
3)  Doporučená implementace. Odeslat až do streaming okna, ale pomocí

    different Elligator2-encoded cleartext public key (session) for
    each. All messages contain same next public key (ratchet). This will
    not be visible to OBGW/IBEP because they all start with different
    cleartext. Bob must recognize that they all contain the same next
    public key, and respond to all with the same ratchet. Alice uses
    that next public key and continues.

Tok zpráv možnosti 3:

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
### Repliable Datagram

Jediná zpráva s očekávanou jedinou odpovědí. Další zprávy nebo odpovědi mohou být odeslány.

Podobně jako HTTP GET, ale s menšími možnostmi pro velikost okna session tag a životnost. Možná nepožadovat ratchet.

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
### Více Raw Datagramů

Více anonymních zpráv, bez očekávaných odpovědí.

V tomto scénáři Alice požaduje relaci, ale bez vazby. Je odeslána zpráva nové relace. Žádný odpověď LS není přibalený. Odpověď DSM je přibalená (toto je jediný případ použití, který vyžaduje přibalené DSM). Žádný následující klíč není zahrnut. Žádná odpověď nebo ratchet není požadována. Žádný ratchet není odeslán. Možnosti nastaví okno session tags na nulu.

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
### Jediný Raw Datagram

Jedna anonymní zpráva, bez očekávané odpovědi.

Jednorázová zpráva je odeslána. Nejsou přiloženy žádné reply LS nebo DSM. Není zahrnut další klíč. Není požadována odpověď ani ratchet. Žádný ratchet není odeslán. Možnosti nastavují okno session tags na nulu.

```
Alice                           Bob

  One-Time Message (1d)   ------------------->
  with bundled message
  without bundled LS
  without bundled Delivery Status Message
```
### Dlouhodobé relace

Dlouhodobé relace mohou provést ratchet nebo požádat o ratchet kdykoli, aby udržely forward secrecy od daného okamžiku. Relace musí provést ratchet, když se blíží k limitu odeslaných zpráv na relaci (65535).

## Úvahy o implementaci

### Obrana

Stejně jako u stávajícího protokolu ElGamal/AES+SessionTag musí implementace omezit ukládání session tagů a chránit proti útokům vyčerpání paměti.

Některé doporučené strategie zahrnují:

- Pevný limit počtu uložených session tagů
- Agresivní vypršení nečinných příchozích relací při nedostatku 
  paměti
- Limit počtu příchozích relací vázaných na jednu vzdálenou
  destinaci
- Adaptivní snížení okna session tagů a mazání starých nepoužívaných
  tagů při nedostatku paměti
- Odmítnutí ratchetu na požádání, pokud je nedostatek paměti

### Parametry

Doporučené parametry a časové limity:

- Velikost NSR tagset: 12 tsmin a tsmax
- Velikost ES tagset 0: tsmin 24, tsmax 160
- Velikost ES tagset (1+): 160 tsmin a tsmax
- Timeout NSR tagset: 3 minuty pro příjemce
- Timeout ES tagset: 8 minut pro odesílatele, 10 minut pro příjemce
- Odstranit předchozí ES tagset po: 3 minutách
- Tagset look ahead tagu N: min(tsmax, tsmin + N/4)
- Tagset trim behind tagu N: min(tsmax, tsmin + N/4) / 2
- Poslat další klíč u tagu: 4096
- Poslat další klíč po životnosti tagset: TBD
- Nahradit session pokud NS přijat po: 3 minutách
- Maximální odchylka času: -5 minut až +2 minuty
- Doba trvání NS replay filtru: 5 minut
- Velikost paddingu: 0-15 bajtů (jiné strategie TBD)

### Klasifikace

Následují doporučení pro klasifikaci příchozích zpráv.

#### Pouze X25519

Na tunnel, který je použit výhradně s tímto protokolem, proveďte identifikaci tak, jak se aktuálně provádí s ElGamal/AES+SessionTags:

Nejprve považujte počáteční data za session tag a vyhledejte tento session tag. Pokud je nalezen, dešifrujte pomocí uložených dat přidružených k tomuto session tag.

Pokud není nalezeno, zacházejte s počátečními daty jako s DH veřejným klíčem a nonce. Proveďte DH operaci a zadanou KDF, a pokuste se dešifrovat zbývající data.

#### X25519 Sdílené s ElGamal/AES+SessionTags

Na tunelu, který podporuje jak tento protokol, tak ElGamal/AES+SessionTags, klasifikujte příchozí zprávy následovně:

Kvůli chybě ve specifikaci ElGamal/AES+SessionTags není AES blok doplněn na náhodnou délku, která není dělitelná 16. Proto je délka zpráv Existing Session mod 16 vždy 0 a délka zpráv New Session mod 16 je vždy 2 (protože ElGamal blok má délku 514 bajtů).

Pokud délka mod 16 není 0 nebo 2, považujte počáteční data za session tag a vyhledejte tento session tag. Pokud je nalezen, dešifrujte pomocí uložených dat asociovaných s tímto session tag.

Pokud není nalezen a délka mod 16 není 0 nebo 2, považujte počáteční data za DH veřejný klíč a nonce. Proveďte DH operaci a specifikovanou KDF a pokuste se dešifrovat zbývající data. (na základě relativního mixu provozu a relativních nákladů X25519 a ElGamal DH operací může být tento krok proveden jako poslední)

Jinak, pokud je délka mod 16 rovna 0, považujte počáteční data za ElGamal/AES session tag a vyhledejte session tag. Pokud je nalezen, dešifrujte pomocí uložených dat spojených s tímto session tag.

Pokud není nalezen a data jsou dlouhá alespoň 642 (514 + 128) bajtů a délka mod 16 je 2, považujte počáteční data za ElGamal blok. Pokuste se dešifrovat zbývající data.

Upozorňujeme, že pokud bude specifikace ElGamal/AES+SessionTag aktualizována tak, aby umožňovala padding, který není násobkem 16, bude potřeba postupovat jinak.

### Opětovné přenosy a přechody stavů

Vrstva ratchet neprovádí opětovné přenosy a až na dvě výjimky nepoužívá časovače pro přenosy. Časovače jsou také vyžadovány pro timeout tagset.

Časovače přenosu se používají pouze pro odesílání NSR a pro odpovídání pomocí ES, když přijatý ES obsahuje požadavek ACK. Doporučený timeout je jedna sekunda. Téměř ve všech případech vyšší vrstva (datagram nebo streaming) odpoví, což vynutí NSR nebo ES, a časovač může být zrušen. Pokud se časovač spustí, odešlete prázdný payload s NSR nebo ES.

#### Odpovědi vrstvy Ratchet

Počáteční implementace spoléhají na obousměrný provoz ve vyšších vrstvách. To znamená, že implementace předpokládají, že provoz v opačném směru bude brzy přenášen, což vynutí jakoukoliv požadovanou odpověď na vrstvě ECIES.

Určitý provoz však může být jednosměrný nebo s velmi malou šířkou pásma, takže neexistuje provoz vyšší vrstvy, který by generoval včasnou odpověď.

Přijetí zpráv NS a NSR vyžaduje odpověď; přijetí bloků ACK Request a Next Key také vyžaduje odpověď.

Implementace by měly spustit časovač při přijetí jedné z těchto zpráv, která vyžaduje odpověď, a vygenerovat "prázdnou" odpověď (bez bloku Garlic Clove) na vrstvě ECIES, pokud není v krátkém časovém období (např. 1 sekunda) odeslán žádný zpětný provoz.

Může být také vhodné použít ještě kratší timeout pro odpovědi na NS a NSR zprávy, aby se provoz co nejdříve přesunul na efektivní ES zprávy.

#### NS vazba pro NSR

Na ratchet vrstvě je Alice pro Boba známa pouze statickým klíčem. NS zpráva je autentifikována ([Noise](https://noiseprotocol.org/noise.html) IK sender authentication 1). To však není dostatečné pro to, aby ratchet vrstva mohla Alici cokoliv poslat, protože síťové směrování vyžaduje úplnou Destination.

Před odesláním NSR musí být úplná Alice's Destination objevena buď ratchet vrstvou nebo protokolem vyšší vrstvy umožňujícím odpověď, buď odpovídající [Datagrams](/docs/specs/datagrams/) nebo [Streaming](/docs/specs/streaming/). Po nalezení leaseSet pro tuto Destination bude tento leaseSet obsahovat stejný statický klíč jako je obsažen v NS.

Obvykle vyšší vrstva odpoví, což vynutí vyhledání Alice's Leaseset v síťové databázi podle Alice's Destination Hash. Tento Leaseset bude téměř vždy nalezen lokálně, protože NS obsahoval Garlic Clove blok, obsahující Database Store zprávu, obsahující Alice's Leaseset.

Aby byl Bob připraven odeslat ratchet-layer NSR a svázat čekající relaci s Destination Alice, měl by Bob "zachytit" Destination během zpracování NS payloadu. Pokud je nalezena zpráva Database Store obsahující Leaseset s klíčem odpovídajícím statickému klíči v NS, čekající relace je nyní svázána s tímto Destination a Bob ví, kam odeslat jakýkoli NSR, pokud vyprší časovač odpovědi. Toto je doporučená implementace.

Alternativní přístup spočívá v udržování cache nebo databáze, kde je statický klíč mapován na Destination. Bezpečnost a praktičnost tohoto přístupu je tématem pro další studium.

Ani tato specifikace ani jiné striktně nevyžadují, aby každé NS obsahovalo Alice's Leaseset. V praxi by však mělo. Doporučený timeout odesílatele ES tagset (8 minut) je kratší než maximální timeout Leaseset (10 minut), takže může existovat malé okno, kde předchozí relace vypršela, Alice si myslí, že Bob stále má její platný Leaseset, a neposílá nový Leaseset s novým NS. Toto je téma pro další studium.

#### Vícenásobné NS zprávy

Pokud není přijata žádná NSR odpověď před tím, než vyšší vrstva (datagram nebo streaming) odešle další data, případně jako retransmisi, Alice musí sestavit novou NS s použitím nového dočasného klíče. Nepoužívejte opakovaně dočasný klíč z jakékoli předchozí NS. Alice musí udržovat dodatečný stav handshaku a odvozený receive tagset, aby mohla přijímat NSR zprávy v odpověď na jakékoli NSR, které bylo odesláno.

Implementace mohou omezit celkový počet odeslaných NS zpráv nebo rychlost odesílání NS zpráv, a to buď pomocí zařazování do fronty nebo zahazování zpráv vyšších vrstev před jejich odesláním.

V určitých situacích, při vysokém zatížení nebo v určitých scénářích útoku, může být pro Boba vhodné zařadit do fronty, zahazovat nebo omezovat zdánlivé NS zprávy bez pokusu o dešifrování, aby se vyhnul útoku vyčerpání zdrojů.

Pro každý obdržený NS generuje Bob odchozí NSR tagset, odešle NSR, provede split() a generuje příchozí a odchozí ES tagsety. Bob však neodešle žádné ES zprávy, dokud neobdrží první ES zprávu na odpovídajícím příchozím tagsetu. Poté může Bob zahodit všechny handshake stavy a tagsety pro jakýkoli jiný obdržený NS nebo odeslaný NSR, nebo je nechat brzy vypršet. Nepoužívejte NSR tagsety pro ES zprávy.

Je to téma pro další studium, zda si Bob může zvolit spekulativně poslat ES zprávy ihned po NSR, ještě před obdržením první ES od Alice. V určitých scénářích a vzorcích provozu by to mohlo ušetřit značnou šířku pásma a výkon CPU. Tato strategie může být založena na heuristice jako jsou vzorce provozu, procento ES obdržených v první sadě tagů relace nebo jiná data.

#### Více NSR zpráv

Pro každou přijatou NS zprávu, dokud není přijata ES zpráva, musí Bob odpovědět novým NSR, buď kvůli odesílání provozu vyšší vrstvy, nebo kvůli vypršení časovače odesílání NSR.

Každý NSR používá handshake stav a tagset odpovídající příchozí NS. Bob musí udržovat handshake stav a tagset pro všechny přijaté NS zprávy, dokud není přijata ES zpráva.

Implementace mohou omezit celkový počet odeslaných NSR zpráv nebo rychlost odesílání NSR zpráv, a to buď zařazením do fronty nebo zahozením zpráv vyšší vrstvy před jejich odesláním. Tato omezení mohou být uplatněna buď v případě příchozích NS zpráv, nebo dodatečného odchozího provozu vyšší vrstvy.

V určitých situacích, při vysoké zátěži nebo v určitých scénářích útoků, může být vhodné, aby Alice zařadila do fronty, zahodila nebo omezila NSR zprávy bez pokusu o dešifrování, aby se vyhnula útoku vyčerpání zdrojů. Tato omezení mohou být buď celková napříč všemi relacemi, podle relace, nebo obojí.

Jakmile Alice obdrží NSR, Alice provede split() pro odvození ES session keys. Alice by měla nastavit časovač a poslat prázdnou ES zprávu, pokud vyšší vrstva nepošle žádný provoz, typicky do jedné sekundy.

Ostatní příchozí NSR tagsets mohou být brzy odstraněny nebo může být povoleno jejich vypršení, ale Alice by je měla ponechat na krátkou dobu, aby dešifrovala jakékoli další NSR zprávy, které budou přijaty.

### Prevence opakování

Bob musí implementovat Bloom filtr nebo jiný mechanismus pro prevenci replay útoků NS, pokud je zahrnutý DateTime nedávný, a odmítnout NS zprávy, kde je DateTime příliš starý. Bob může také použít dřívější kontrolu detekce opakování pro duplicitní dočasný klíč (buď před nebo po Elligator2 dekódování) k detekci a zahození nedávných duplicitních NS zpráv před dešifrováním.

Zprávy NSR a ES mají inherentní ochranu proti opakovanému přehrání, protože session tag je určen k jednorázovému použití.

Garlic zprávy mají také ochranu proti opakovanému přehrání, pokud router implementuje Bloomův filtr na úrovni celého routeru založený na ID I2NP zprávy.

## Související změny

Vyhledávání v databázi z ECIES destinací: Viz [Prop154](/proposals/154-ratchet/), nyní začleněno do [I2NP](/docs/specs/i2np/) pro verzi 0.9.46.

Tato specifikace vyžaduje podporu LS2 pro publikování veřejného klíče X25519 s leaseset. Nejsou nutné žádné změny ve specifikacích LS2 v [I2NP](/docs/specs/i2np/). Veškerá podpora byla navržena, specifikována a implementována v [Prop123](/proposals/123-new-netdb-entries/) implementovaném ve verzi 0.9.38.

Tato specifikace vyžaduje, aby byla v I2CP možnostech nastavena vlastnost pro povolení. Veškerá podpora byla navržena, specifikována a implementována v [Prop123](/proposals/123-new-netdb-entries/) implementované ve verzi 0.9.38.

Možnost potřebná k povolení ECIES je jediná I2CP vlastnost pro I2CP, BOB, SAM nebo i2ptunnel.

Typické hodnoty jsou i2cp.leaseSetEncType=4 pouze pro ECIES, nebo i2cp.leaseSetEncType=4,0 pro duální klíče ECIES a ElGamal.

## Kompatibilita

Jakýkoliv router podporující LS2 s duálními klíči (0.9.38 nebo vyšší) by měl podporovat připojení k cílům s duálními klíči.

Cíle pouze s ECIES vyžadují, aby byla většina floodfillů aktualizována na verzi 0.9.46, aby mohly získávat šifrované odpovědi na vyhledávání. Viz [Prop154](/proposals/154-ratchet/).

Destinace pouze s ECIES se mohou připojit pouze k jiným destinacím, které jsou buď také pouze s ECIES, nebo mají dvojitý klíč.

## Reference

- [Společné](/docs/specs/common-structures/)
- [CRYPTO-ELG](/docs/specs/cryptography/#elgamal)
- [Datagramy](/docs/specs/datagrams/)
- [ECIES-HYBRID](/docs/specs/ecies-hybrid/)
- [ElG-AES](/docs/specs/elgamal-aes/)
- [Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf) - Viz také [článek Elligator](https://www.imperialviolet.org/2013/12/25/elligator.html) a kód OBFS4
- [GARLICSPEC](/docs/overview/garlic-routing/)
- [I2CP](/docs/specs/i2cp/)
- [I2NP](/docs/specs/i2np/)
- [NOISE](https://noiseprotocol.org/noise.html)
- [NTCP2](/docs/specs/ntcp2/)
- [Prop111](/proposals/111-ntcp2/)
- [Prop123](/proposals/123-new-netdb-entries/)
- [Prop142](/proposals/142-ecies-template/)
- [Prop144](/proposals/144-ecies-x25519/)
- [Prop145](/proposals/145-ecies-ecdh-aes/)
- [Prop152](/proposals/152-ecies-config/)
- [Prop153](/proposals/153-chacha20-layer/)
- [Prop154](/proposals/154-ratchet/)
- [RFC-2104](https://tools.ietf.org/html/rfc2104)
- [RFC-4880-S5.1](https://tools.ietf.org/html/rfc4880#section-5.1)
- [RFC-5869](https://tools.ietf.org/html/rfc5869)
- [RFC-7539](https://tools.ietf.org/html/rfc7539)
- [RFC-7748](https://tools.ietf.org/html/rfc7748)
- [RFC-7905](https://tools.ietf.org/html/rfc7905)
- [Signal](https://signal.org/docs/specifications/doubleratchet/)
- [SSU](/docs/transport/ssu/)
- [SSU2](/docs/specs/ssu2/)
- [STS](https://en.wikipedia.org/wiki/Station-to-Station_protocol) - Diffie, W.; van Oorschot P. C.; Wiener M. J., Authentication and Authenticated Key Exchanges
- [Streaming](/docs/specs/streaming/)
