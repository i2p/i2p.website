---
title: "ECIES tunely"
aliases:
  - "/cs/proposals/152-ecies-config"
  - "/cs/proposals/152-ecies-config/"
  - "/cs/proposals/152"
  - "/cs/proposals/152/"
number: "152"
author: "chisana, zzz, orignal"
created: "2019-07-04"
lastupdated: "2025-03-05"
status: "Uzavřeno"
thread: "http://zzz.i2p/topics/2737"
target: "0.9.48"
implementedin: "0.9.48"
toc: true
---

## Poznámka

Nasazení sítě a testování probíhá. Podléhá drobným revizím. Viz [SPEC](/docs/specs/tunnel-implementation/) pro oficiální specifikaci.

## Přehled

Tento dokument navrhuje změny šifrování zpráv Tunnel Build pomocí kryptografických primitiv zavedených v [ECIES-X25519](/docs/specs/ecies/). Je součástí celkového návrhu [Proposal 156](/proposals/156-ecies-routers) pro převod routerů z ElGamal na ECIES-X25519 klíče.

Pro účely přechodu sítě z ElGamal + AES256 na ECIES + ChaCha20 jsou nezbytné tunnely se smíšenými ElGamal a ECIES routery. Jsou poskytnuty specifikace pro zpracování smíšených tunnel hopů. Nebudou provedeny žádné změny ve formátu, zpracování nebo šifrování ElGamal hopů.

ElGamal tvůrci tunelů budou muset vytvořit efemérní X25519 klíčové páry pro každý hop a následovat tuto specifikaci pro vytváření tunelů obsahujících ECIES hopy.

Tento návrh specifikuje změny potřebné pro ECIES-X25519 Tunnel Building. Pro přehled všech změn vyžadovaných pro ECIES routery viz návrh 156 [Proposal 156](/proposals/156-ecies-routers).

Tento návrh zachovává stejnou velikost pro záznamy budování tunelů, jak je vyžadováno pro kompatibilitu. Menší záznamy budování a zprávy budou implementovány později - viz [Proposal 157](/proposals/157-new-tbm).

### Cryptographic Primitives

Nejsou zavedeny žádné nové kryptografické primitiva. Primitiva potřebná k implementaci tohoto návrhu jsou:

- AES-256-CBC jak v [Cryptography](/docs/specs/cryptography/)
- STREAM ChaCha20/Poly1305 funkce:
  ENCRYPT(k, n, plaintext, ad) a DECRYPT(k, n, ciphertext, ad) - jak v [NTCP2](/docs/specs/ntcp2/) [ECIES-X25519](/docs/specs/ecies/) a [RFC-7539](https://tools.ietf.org/html/rfc7539)
- X25519 DH funkce - jak v [NTCP2](/docs/specs/ntcp2/) a [ECIES-X25519](/docs/specs/ecies/)
- HKDF(salt, ikm, info, n) - jak v [NTCP2](/docs/specs/ntcp2/) a [ECIES-X25519](/docs/specs/ecies/)

Další Noise funkce definované jinde:

- MixHash(d) - jako v [NTCP2](/docs/specs/ntcp2/) a [ECIES-X25519](/docs/specs/ecies/)
- MixKey(d) - jako v [NTCP2](/docs/specs/ntcp2/) a [ECIES-X25519](/docs/specs/ecies/)

### Goals

- Zvýšit rychlost kryptografických operací
- Nahradit ElGamal + AES256/CBC primitivy ECIES pro tunnel BuildRequestRecords a BuildReplyRecords
- Žádná změna velikosti šifrovaných BuildRequestRecords a BuildReplyRecords (528 bajtů) kvůli kompatibilitě
- Žádné nové I2NP zprávy
- Zachovat velikost šifrovaného build recordu kvůli kompatibilitě
- Přidat forward secrecy pro Tunnel Build Messages
- Přidat autentifikované šifrování
- Detekovat přeuspořádání BuildRequestRecords hopů
- Zvýšit rozlišení časového razítka, aby mohla být zmenšena velikost Bloom filtru
- Přidat pole pro vypršení tunnelu, aby byly možné proměnlivé životnosti tunnelů (pouze all-ECIES tunnely)
- Přidat rozšiřitelné pole možností pro budoucí funkce
- Znovu použít existující kryptografické primitivy
- Zlepšit bezpečnost tunnel build zpráv tam, kde je to možné při zachování kompatibility
- Podporovat tunnely se smíšenými ElGamal/ECIES partnery
- Zlepšit obranu proti "tagging" útokům na build zprávy
- Hopy nemusí znát typ šifrování dalšího hopu před zpracováním build zprávy,
  protože v té době nemusí mít RI dalšího hopu
- Maximalizovat kompatibilitu se současnou sítí
- Žádná změna AES šifrování tunnel build request/reply pro ElGamal routery
- Žádná změna AES "vrstvového" šifrování tunnelu, pro to viz [Proposal 153](/proposals/153-chacha20-layer-encryption)
- Pokračovat v podpoře jak 8-recordových TBM/TBRM, tak proměnlivě velkých VTBM/VTBRM
- Nevyžadovat upgrade celé sítě typu "flag day"

### Kryptografické primitiva

- Kompletní redesign zpráv pro stavbu tunnelů vyžadující "flag day".
- Zmenšování zpráv pro stavbu tunnelů (vyžaduje všechny ECIES hopy a nový návrh)
- Použití možností stavby tunnelů jak jsou definovány v [Proposal 143](/proposals/143-build-message-options), nutné pouze pro malé zprávy
- Obousměrné tunnely - pro to viz [Proposal 119](/proposals/119-bidirectional-tunnels)
- Menší zprávy pro stavbu tunnelů - pro to viz [Proposal 157](/proposals/157-new-tbm)

## Threat Model

### Cíle

- Žádný hop není schopen určit původce tunelu.

- Prostřední uzly nesmí být schopny určit směr tunelu
  nebo svou pozici v tunelu.

- Žádný hop nemůže číst jakýkoli obsah jiných záznamů požadavků nebo odpovědí, kromě
  zkráceného router hash a dočasného klíče pro další hop

- Žádný člen reply tunnel pro odchozí build nemůže číst žádné reply záznamy.

- Žádný člen odchozího tunelu pro příchozí sestavení nemůže číst žádné záznamy požadavků,
  kromě toho, že OBEP může vidět zkrácený hash routeru a dočasný klíč pro IBGW

### Necíle

Hlavním cílem návrhu budování tunelů je ztížit spolupracujícím routerům X a Y poznání, že se nacházejí v jednom tunelu. Pokud je router X na skoku m a router Y na skoku m+1, tak to samozřejmě poznají. Ale pokud je router X na skoku m a router Y na skoku m+n pro n>1, mělo by to být mnohem těžší.

Útoky označováním (tagging attacks) jsou situace, kdy router X ve střední části tunelu změní zprávu pro stavbu tunelu takovým způsobem, že router Y může detekovat tuto změnu, když se zpráva dostane k němu. Cílem je, aby jakákoliv změněná zpráva byla zahozena routerem mezi X a Y předtím, než se dostane k routeru Y. U modifikací, které nejsou zahozeny před routerem Y, by měl tvůrce tunelu detekovat poškození v odpovědi a tunel zahodit.

Možné útoky:

- Změnit záznam sestavení
- Nahradit záznam sestavení
- Přidat nebo odebrat záznam sestavení
- Změnit pořadí záznamů sestavení

TODO: Zabraňuje současný návrh všem těmto útokům?

## Design

### Noise Protocol Framework

Tento návrh poskytuje požadavky založené na Noise Protocol Framework [NOISE](https://noiseprotocol.org/noise.html) (Revize 34, 2018-07-11). V terminologii Noise je Alice iniciátor a Bob je respondent.

Tento návrh je založen na protokolu Noise Noise_N_25519_ChaChaPoly_SHA256. Tento protokol Noise používá následující primitiva:

- One-Way Handshake Pattern: N
  Alice nepřenáší svůj statický klíč Bobovi (N)

- DH Function: X25519
  X25519 DH s délkou klíče 32 bajtů podle specifikace v [RFC-7748](https://tools.ietf.org/html/rfc7748).

- Cipher Function: ChaChaPoly
  AEAD_CHACHA20_POLY1305 jak je specifikováno v [RFC-7539](https://tools.ietf.org/html/rfc7539) sekce 2.8.
  12 bajtový nonce, s prvními 4 bajty nastavenými na nulu.
  Identické s tím v [NTCP2](/docs/specs/ntcp2/).

- Hash Function: SHA256
  Standardní 32bajtový hash, již hojně používaný v I2P.

#### Additions to the Framework

Žádný.

### Cíle návrhu

Handshaky používají [Noise](https://noiseprotocol.org/noise.html) handshake vzory.

Použije se následující mapování písmen:

- e = jednorázový dočasný klíč
- s = statický klíč
- p = datová část zprávy

Build request je identický s Noise N vzorem. To je také identické s první zprávou (Session Request) ve vzoru XK používaném v [NTCP2](/docs/specs/ntcp2/).

```text
<- s
  ...
  e es p ->
```
### Útoky pomocí značkování

Záznamy požadavků na sestavení jsou vytvořeny tvůrcem tunnelu a asymetricky zašifrovány pro jednotlivé skoky. Toto asymetrické šifrování záznamů požadavků je v současnosti ElGamal jak je definováno v [Kryptografie](/docs/specs/cryptography/) a obsahuje kontrolní součet SHA-256. Tento návrh není forward-secret.

Nový design bude používat jednosměrný Noise pattern "N" s ECIES-X25519 ephemeral-static DH, s HKDF a ChaCha20/Poly1305 AEAD pro forward secrecy, integritu a autentifikaci. Alice je žadatel o vybudování tunelu. Každý hop v tunelu je Bob.

(Vlastnosti zabezpečení užitečného zatížení)

```text
N:                      Authentication   Confidentiality
    -> e, es                  0                2

    Authentication: None (0).
    This payload may have been sent by any party, including an active attacker.

    Confidentiality: 2.
    Encryption to a known recipient, forward secrecy for sender compromise
    only, vulnerable to replay.  This payload is encrypted based only on DHs
    involving the recipient's static key pair.  If the recipient's static
    private key is compromised, even at a later date, this payload can be
    decrypted.  This message can also be replayed, since there's no ephemeral
    contribution from the recipient.

    "e": Alice generates a new ephemeral key pair and stores it in the e
         variable, writes the ephemeral public key as cleartext into the
         message buffer, and hashes the public key along with the old h to
         derive a new h.

    "es": A DH is performed between the Alice's ephemeral key pair and the
          Bob's static key pair.  The result is hashed along with the old ck to
          derive a new ck and k, and n is set to zero.
```
### Reply encryption

Build reply záznamy jsou vytvářeny tvůrcem hopů a symetricky šifrovány k tvůrci. Toto symetrické šifrování reply záznamů je v současnosti AES s předřazeným SHA-256 kontrolním součtem. a obsahuje SHA-256 kontrolní součet. Tento návrh není forward-secret.

Nový design bude používat ChaCha20/Poly1305 AEAD pro integritu a autentifikaci.

### Noise Protocol Framework

Efemérní veřejný klíč v požadavku nemusí být zamaskován pomocí AES nebo Elligator2. Předchozí hop je jediný, který ho může vidět, a tento hop ví, že další hop je ECIES.

Záznamy odpovědí nepotřebují plné asymetrické šifrování s dalším DH.

## Specification

### Build Request Records

Šifrované BuildRequestRecords mají 528 bajtů jak pro ElGamal, tak pro ECIES, kvůli kompatibilitě.

#### Request Record Unencrypted (ElGamal)

Pro referenci, toto je současná specifikace tunnel BuildRequestRecord pro ElGamal routery, převzatá z [I2NP](/docs/specs/i2np/). Nešifrovaná data jsou prefixována nenulovým bytem a SHA-256 hashem dat před šifrováním, jak je definováno v [Cryptography](/docs/specs/cryptography/).

Všechna pole jsou ve formátu big-endian.

Nezašifrovaná velikost: 222 bajtů

```text
bytes     0-3: tunnel ID to receive messages as, nonzero
  bytes    4-35: local router identity hash
  bytes   36-39: next tunnel ID, nonzero
  bytes   40-71: next router identity hash
  bytes  72-103: AES-256 tunnel layer key
  bytes 104-135: AES-256 tunnel IV key
  bytes 136-167: AES-256 reply key
  bytes 168-183: AES-256 reply IV
  byte      184: flags
  bytes 185-188: request time (in hours since the epoch, rounded down)
  bytes 189-192: next message ID
  bytes 193-221: uninterpreted / random padding
```
#### Request Record Encrypted (ElGamal)

Pro referenci, toto je současná specifikace tunnel BuildRequestRecord pro ElGamal routery, převzatá z [I2NP](/docs/specs/i2np/).

Šifrovaná velikost: 528 bajtů

```text
bytes    0-15: Hop's truncated identity hash
  bytes  16-528: ElGamal encrypted BuildRequestRecord
```
#### Request Record Unencrypted (ECIES)

Toto je navrhovaná specifikace tunnel BuildRequestRecord pro ECIES-X25519 routery. Shrnutí změn:

- Odstranit nepoužívaný 32-bajtový router hash
- Změnit čas požadavku z hodin na minuty
- Přidat pole expiration pro budoucí proměnný čas tunelu
- Přidat více místa pro flags
- Přidat Mapping pro další možnosti buildu
- AES-256 reply klíč a IV nejsou používány pro hop's vlastní reply záznam
- Nezašifrovaný záznam je delší, protože je zde menší overhead šifrování

Záznam požadavku neobsahuje žádné ChaCha klíče pro odpověď. Tyto klíče jsou odvozeny z KDF. Viz níže.

Všechna pole jsou big-endian.

Nezašifrovaná velikost: 464 bajtů

```text
bytes     0-3: tunnel ID to receive messages as, nonzero
  bytes     4-7: next tunnel ID, nonzero
  bytes    8-39: next router identity hash
  bytes   40-71: AES-256 tunnel layer key
  bytes  72-103: AES-256 tunnel IV key
  bytes 104-135: AES-256 reply key
  bytes 136-151: AES-256 reply IV
  byte      152: flags
  bytes 153-155: more flags, unused, set to 0 for compatibility
  bytes 156-159: request time (in minutes since the epoch, rounded down)
  bytes 160-163: request expiration (in seconds since creation)
  bytes 164-167: next message ID
  bytes   168-x: tunnel build options (Mapping)
  bytes     x-x: other data as implied by flags or options
  bytes   x-463: random padding
```
Pole flags je stejné jako definované v [Tunnel Creation](/docs/specs/tunnel-implementation/) a obsahuje následující::

```text
Bit order: 76543210 (bit 7 is MSB)
bit 7: if set, allow messages from anyone
bit 6: if set, allow messages to anyone, and send the reply to the
       specified next hop in a Tunnel Build Reply Message
bits 5-0: Undefined, must set to 0 for compatibility with future options
```
Pořadí bitů: 76543210 (bit 7 je MSB)  bit 7: pokud je nastaven, povolit zprávy od kohokoliv  bit 6: pokud je nastaven, povolit zprávy komukoliv a odeslat odpověď na

bity 5-0: Nedefinované, musí být nastaveny na 0 pro kompatibilitu s budoucími možnostmi

Bit 7 označuje, že hop bude inbound gateway (IBGW). Bit 6 označuje, že hop bude outbound endpoint (OBEP). Pokud není nastaven žádný z bitů, hop bude intermediate participant. Oba nemohou být nastaveny současně.

#### Request Record Encrypted (ECIES)

Vypršení požadavku je pro budoucí proměnnou délku trvání tunnelu. Prozatím je jedinou podporovanou hodnotou 600 (10 minut).

Možnosti pro budování tunnelu jsou struktura Mapping jak je definována v [Common Structures](/docs/specs/common-structures/). Toto je pro budoucí použití. Žádné možnosti nejsou v současnosti definovány. Pokud je struktura Mapping prázdná, jedná se o dva bajty 0x00 0x00. Maximální velikost Mapping (včetně pole délky) je 296 bajtů a maximální hodnota pole délky Mapping je 294.

```text
bytes    0-15: Hop's truncated identity hash
  bytes   16-47: Sender's ephemeral X25519 public key
  bytes  48-511: ChaCha20 encrypted BuildRequestRecord
  bytes 512-527: Poly1305 MAC
```
### Vzory handshaku

Všechna pole jsou big-endian s výjimkou dočasného veřejného klíče, který je little-endian.

#### Reply Record Unencrypted (ElGamal)

Zašifrovaná velikost: 528 bajtů

Šifrované BuildReplyRecords mají 528 bajtů jak pro ElGamal, tak pro ECIES, kvůli kompatibilitě.

ElGamal odpovědi jsou šifrovány pomocí AES.

```text
bytes   0-31: SHA-256 Hash of bytes 32-527
  bytes 32-526: random data
  byte     527: reply

  total length: 528
```
#### Reply Record Unencrypted (ECIES)

Všechna pole jsou big-endian.

- Přidat mapování pro možnosti odpovědi sestavení
- Nešifrovaný záznam je delší, protože je menší režie šifrování

Nezašifrovaná velikost: 528 bytů

Toto je navrhovaná specifikace tunnel BuildReplyRecord pro ECIES-X25519 routery. Shrnutí změn:

ECIES odpovědi jsou šifrovány pomocí ChaCha20/Poly1305.

```text
bytes    0-x: Tunnel Build Reply Options (Mapping)
  bytes    x-x: other data as implied by options
  bytes  x-510: Random padding
  byte     511: Reply byte
```
Všechna pole jsou ve formátu big-endian.

Nezašifrovaná velikost: 512 bytů

- 0x00 (přijmout)
- 30 (TUNNEL_REJECT_BANDWIDTH)

#### Reply Record Encrypted (ECIES)

Možnosti odpovědi na tunnel build je struktura Mapping jak je definována v [Common Structures](/docs/specs/common-structures/). Toto je pro budoucí použití. Aktuálně nejsou definovány žádné možnosti. Pokud je struktura Mapping prázdná, jedná se o dva bajty 0x00 0x00. Maximální velikost Mapping (včetně pole délky) je 511 bajtů a maximální hodnota pole délky Mapping je 509.

```text
bytes   0-511: ChaCha20 encrypted BuildReplyRecord
  bytes 512-527: Poly1305 MAC
```
Odpověď byte je jedna z následujících hodnot definovaných v [Tunnel Creation](/docs/specs/tunnel-implementation/) k zamezení fingerprintingu:

### Šifrování požadavků

Šifrovaná velikost: 528 bajtů

Po úplném přechodu na ECIES záznamy jsou pravidla pro rozsahové padding stejná jako pro záznamy požadavků.

- "šifrování":

- šifra spuštěná v režimu dešifrování
- záznamy požadavků preventivně dešifrovány v preprocessing (skrývání šifrovaných záznamů požadavků)

- "dešifrování":

- šifra spuštěna v režimu šifrování
- záznamy požadavků zašifrovány (odhalující další plaintext záznam požadavku) účastnickými skoky

- ChaCha20 nemá "módy", takže se jednoduše spustí třikrát:

- jednou při předzpracování
- jednou hopem
- jednou při zpracování finální odpovědi

Smíšené tunely jsou povolené a nezbytné pro přechod z ElGamal na ECIES. Během přechodného období bude narůstající počet routerů používat ECIES klíče.

Preprocessing symetrické kryptografie bude probíhat stejným způsobem:

Při použití smíšených tunelů budou tvůrci tunelů potřebovat založit symetrické šifrování BuildRequestRecord na typu šifrování aktuálního a předchozího hopu.

Každý hop bude používat svůj vlastní typ šifrování pro šifrování BuildReplyRecords a dalších záznamů ve VariableTunnelBuildMessage (VTBM).

- Odesílatel (OBGW) -> ElGamal (H1) -> ECIES (H2) -> ElGamal (H3)

Na zpáteční cestě bude koncový bod (odesílatel) muset vrátit [Multiple Encryption](https://en.wikipedia.org/wiki/Multiple_encryption) zpět, pomocí klíče pro odpověď každého přeskoku.

Jako objasňující příklad se podívejme na odchozí tunnel s ECIES obklopeným ElGamal:

Všechny BuildRequestRecords jsou ve svém šifrovaném stavu (pomocí ElGamal nebo ECIES).

Šifra AES256/CBC, když je použita, je stále používána pro každý záznam, bez řetězení napříč více záznamy.

- Záznam H3 je "zašifrován" pomocí:

- Odpověďový klíč H2 (ChaCha20)
- Odpověďový klíč H1 (AES256/CBC)

- Záznam H2 je "šifrován" pomocí:

- Odpověďový klíč H1 (AES256/CBC)

- Záznam H1 odchází bez symetrického šifrování

Stejně tak bude ChaCha20 použito k šifrování každého záznamu, nikoli ke streamování přes celý VTBM.

Záznamy požadavků jsou předem zpracovány Odesílatelem (OBGW):

- Záznam H3 je "dešifrován" pomocí:

- H3 odpověďový klíč (AES256/CBC)

- H2 záznam je "dešifrován" pomocí:

- Klíč odpovědi H3 (AES256/CBC)
- Klíč odpovědi H2 (ChaCha20-Poly1305)

- Záznam H1 je "dešifrován" pomocí:

- Odpovědní klíč H3 (AES256/CBC)
- Odpovědní klíč H2 (ChaCha20)
- Odpovědní klíč H1 (AES256/CBC)

Pouze H2 kontroluje příznak šifrování odpovědi a vidí, že je následován AES256/CBC.

- Záznam H3 je "zašifrován" pomocí:

- Odpověďový klíč H3 (AES256/CBC)

- Záznam H2 je "šifrován" pomocí:

- Odpověďový klíč H3 (AES256/CBC)
- Odpověďový klíč H2 (ChaCha20-Poly1305)

- Záznam H1 je "šifrován" pomocí:

- Odpovědní klíč H3 (AES256/CBC)
- Odpovědní klíč H2 (ChaCha20)
- Odpovědní klíč H1 (AES256/CBC)

### Šifrování odpovědí

Po zpracování každým hopem jsou záznamy ve stavu "dešifrováno":

Tvůrce tunelu, také známý jako Inbound Endpoint (IBEP), zpracovává odpověď:

#### KDF for Initial ck and h

Tyto klíče jsou explicitně zahrnuty v ElGamal BuildRequestRecords. Pro ECIES BuildRequestRecords jsou zahrnuty tunnel klíče a AES reply klíče, ale ChaCha reply klíče jsou odvozeny z DH výměny. Podrobnosti o statických ECIES klíčích routeru najdete v [Proposal 156](/proposals/156-ecies-routers).

```text
This is the "e" message pattern:

  // Define protocol_name.
  Set protocol_name = "Noise_N_25519_ChaChaPoly_SHA256"
  (31 bytes, US-ASCII encoded, no NULL termination).

  // Define Hash h = 32 bytes
  // Pad to 32 bytes. Do NOT hash it, because it is not more than 32 bytes.
  h = protocol_name || 0

  Define ck = 32 byte chaining key. Copy the h data to ck.
  Set chainKey = h

  // MixHash(null prologue)
  h = SHA256(h);

  // up until here, can all be precalculated by all routers.
```
#### KDF for Request Record

Níže je popis toho, jak odvodit klíče dříve přenášené v záznamech požadavků.

Toto je standardní [NOISE](https://noiseprotocol.org/noise.html) pro vzor "N" se standardním názvem protokolu.

ElGamal tvůrci tunelů generují dočasný X25519 klíčový pár pro každý ECIES hop v tunelu a používají výše uvedené schéma pro šifrování svého BuildRequestRecord. ElGamal tvůrci tunelů budou používat schéma předcházející této specifikaci pro šifrování do ElGamal hopů.

ECIES tvůrci tunelů budou muset šifrovat k veřejnému klíči každého ElGamal hopu pomocí schématu definovaného v [Tunnel Creation](/docs/specs/tunnel-implementation/). ECIES tvůrci tunelů budou používat výše uvedené schéma pro šifrování k ECIES hopům.

To znamená, že hopové uzly tunelů uvidí pouze šifrované záznamy ze stejného typu šifrování.

```text
// Each hop's X25519 static keypair (hesk, hepk) from the Router Identity
  hesk = GENERATE_PRIVATE()
  hepk = DERIVE_PUBLIC(hesk)

  // MixHash(hepk)
  // || below means append
  h = SHA256(h || hepk);

  // up until here, can all be precalculated by each router
  // for all incoming build requests

  // Sender generates an X25519 ephemeral keypair per ECIES hop in the VTBM (sesk, sepk)
  sesk = GENERATE_PRIVATE()
  sepk = DERIVE_PUBLIC(sesk)

  // MixHash(sepk)
  h = SHA256(h || sepk);

  End of "e" message pattern.

  This is the "es" message pattern:

  // Noise es
  // Sender performs an X25519 DH with Hop's static public key.
  // Each Hop, finds the record w/ their truncated identity hash,
  // and extracts the Sender's ephemeral key preceding the encrypted record.
  sharedSecret = DH(sesk, hepk) = DH(hesk, sepk)

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // ChaChaPoly parameters to encrypt/decrypt
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  // Save for Reply Record KDF
  chainKey = keydata[0:31]

  // AEAD parameters
  k = keydata[32:63]
  n = 0
  plaintext = 464 byte build request record
  ad = h
  ciphertext = ENCRYPT(k, n, plaintext, ad)

  End of "es" message pattern.

  // MixHash(ciphertext)
  // Save for Reply Record KDF
  h = SHA256(h || ciphertext)
```
Pro tvůrce tunnelů ElGamal a ECIES budou generovat jedinečné dočasné X25519 páry klíčů pro každý hop při šifrování do ECIES hopů.

### Odůvodnění

**DŮLEŽITÉ**: Ephemeral klíče musí být jedinečné pro každý ECIES hop a pro každý build record. Nepoužívání jedinečných klíčů otevírá vektor útoku pro spolupracující hopy k potvrzení, že jsou ve stejném tunelu.

### Reply Record Encryption (ECIES)

``replyKey``, ``layerKey`` a ``layerIV`` musí být stále zahrnuty uvnitř ElGamal záznamů a mohou být generovány náhodně.

```text
// AEAD parameters
  k = chainkey from build request
  n = 0
  plaintext = 512 byte build reply record
  ad = h from build request

  ciphertext = ENCRYPT(k, n, plaintext, ad)
```
### Záznamy požadavků na sestavení

Jak je definováno v [Tunnel Creation](/docs/specs/tunnel-implementation/). Neexistují žádné změny v šifrování pro ElGamal hopy.

### Security Analysis

Odpověď record je šifrovaná pomocí ChaCha20/Poly1305.

Jak je definováno v [Tunnel Creation](/docs/specs/tunnel-implementation/). Nejsou žádné změny v šifrování pro ElGamal hopy.

ElGamal neposkytuje forward secrecy pro Tunnel Build Messages.

AES256/CBC je na tom o něco lépe, je zranitelný pouze teoretickým oslabením z útoku známým plaintextem `biclique`.

Jediný známý praktický útok proti AES256/CBC je padding oracle útok, když je IV známé útočníkovi.

Útočník by musel prolomit ElGamal šifrování dalšího skoku, aby získal informace o AES256/CBC klíči (reply key a IV).

ElGamal je výrazně náročnější na CPU než ECIES, což vede k potenciálnímu vyčerpání zdrojů.

## Model hrozeb

ECIES, používané s novými dočasnými klíči pro každý BuildRequestRecord nebo VariableTunnelBuildMessage, poskytuje forward-secrecy.

## Implementation Notes

* Starší routery nekontrolují typ šifrování směrování a budou odesílat ElGamal-šifrované
  záznamy. Některé nedávné routery jsou chybné a budou odesílat různé typy poškozených záznamů.
  Implementátoři by měli tyto záznamy detekovat a odmítnout před DH operací,
  pokud je to možné, aby snížili využití CPU.

## Issues

## Návrh

ChaCha20Poly1305 poskytuje AEAD šifrování, které umožňuje příjemci ověřit integritu zprávy před pokusem o dešifrování.

## Reference

* [Obecné](/docs/specs/common-structures/)
* [Kryptografie](/docs/specs/cryptography/)
* [ECIES-X25519](/docs/specs/ecies/)
* [I2NP](/docs/specs/i2np/)
* [NOISE](https://noiseprotocol.org/noise.html)
* [NTCP2](/docs/specs/ntcp2/)
* [Prop119](/proposals/119-bidirectional-tunnels/)
* [Prop143](/proposals/143-build-message-options/)
* [Prop153](/proposals/153-chacha20-layer-encryption/)
* [Prop156](/proposals/156-ecies-routers/)
* [Prop157](/proposals/157-new-tbm/)
* [SPEC](/docs/specs/tunnel-implementation/#tunnel-creation-ecies)
* [Vytváření tunelů](/docs/specs/tunnel-implementation/#tunnel-creation-ecies)
* [Násobené šifrování](https://en.wikipedia.org/wiki/Multiple_encryption)
* [RFC-7539](https://tools.ietf.org/html/rfc7539)
* [RFC-7748](https://tools.ietf.org/html/rfc7748)
