---
title: "Specifikace vytváření tunelů (ECIES-X25519)"
description: "Šifrování zpráv Tunnel Build pomocí kryptografických primitiv ECIES-X25519 pro forward secrecy (dopřednou bezpečnost)."
slug: "tunnel-creation-ecies"
aliases:
  - "/cs/docs/specs/tunnel-creation-ecies-spec"
  - "/cs/docs/specs/tunnel-creation-ecies-spec/"
category: "Protokoly"
lastUpdated: "2025-06"
accurateFor: "0.9.66"
---

## Přehled

Tento dokument specifikuje šifrování zpráv Tunnel Build pomocí kryptografických primitiv zavedených v [ECIES-X25519](/docs/specs/ecies/). Je to část celkového návrhu [Prop156](/proposals/156/) pro převod routerů z ElGamal na ECIES-X25519 klíče.

Jsou specifikovány dvě verze. První používá stávající build zprávy a velikost build záznamu pro kompatibilitu s ElGamal routery. Tato specifikace byla implementována od vydání 0.9.48 a nyní je zastaralá. Druhá používá dvě nové build zprávy a menší velikost build záznamu a může být použita pouze s ECIES routery. Tato specifikace je implementována od vydání 0.9.51.

Pro účely přechodu sítě z ElGamal + AES256 na ECIES + ChaCha20 jsou nutné tunnely se smíšenými ElGamal a ECIES routery. Jsou poskytnuty specifikace pro zpracování smíšených tunnel hopů. Nebudou provedeny žádné změny formátu, zpracování nebo šifrování ElGamal hopů. Tento formát zachovává stejnou velikost pro tunnel build záznamy, jak je vyžadováno pro kompatibilitu.

ElGamal tvůrci tunelů budou generovat dočasné X25519 klíčové páry pro každý hop a budou následovat tuto specifikaci pro vytváření tunelů obsahujících ECIES hopy.

Tento dokument specifikuje ECIES-X25519 Tunnel Building. Pro přehled všech změn potřebných pro ECIES routery viz návrh 156 [Prop156](/proposals/156/). Pro další informace o vývoji specifikace dlouhého záznamu viz návrh 152 [Prop152](/proposals/152/). Pro další informace o vývoji specifikace krátkého záznamu viz návrh 157 [Prop157](/proposals/157/).

### Kryptografické primitiva

Primitiva potřebná k implementaci této specifikace jsou:

- AES-256-CBC jak v [Cryptography](/docs/specs/cryptography/)
- STREAM ChaCha20 funkce: ENCRYPT(k, iv, plaintext) a DECRYPT(k, iv, ciphertext) - jak v [EncryptedLeaseSet](/docs/specs/encryptedleaseset/) a [RFC-7539](https://tools.ietf.org/html/rfc7539)
- STREAM ChaCha20/Poly1305 funkce: ENCRYPT(k, n, plaintext, ad) a DECRYPT(k, n, ciphertext, ad) - jak v [NTCP2](/docs/specs/ntcp2/), [ECIES-X25519](/docs/specs/ecies/) a [RFC-7539](https://tools.ietf.org/html/rfc7539)
- X25519 DH funkce - jak v [NTCP2](/docs/specs/ntcp2/) a [ECIES-X25519](/docs/specs/ecies/)
- HKDF(salt, ikm, info, n) - jak v [NTCP2](/docs/specs/ntcp2/) a [ECIES-X25519](/docs/specs/ecies/)

Další Noise funkce definované jinde:

- MixHash(d) - jako v [NTCP2](/docs/specs/ntcp2/) a [ECIES-X25519](/docs/specs/ecies/)
- MixKey(d) - jako v [NTCP2](/docs/specs/ntcp2/) a [ECIES-X25519](/docs/specs/ecies/)

## Design

### Noise Protocol Framework

Tato specifikace poskytuje požadavky založené na Noise Protocol Framework [NOISE](https://noiseprotocol.org/noise.html) (Revize 34, 2018-07-11). V terminologii Noise je Alice iniciátor a Bob respondent.

Je založen na Noise protokolu Noise_N_25519_ChaChaPoly_SHA256. Tento Noise protokol používá následující primitiva:

- One-Way Handshake Pattern: N - Alice nepřenáší svůj statický klíč Bobovi (N)
- DH Function: X25519 - X25519 DH s délkou klíče 32 bajtů podle specifikace v [RFC-7748](https://tools.ietf.org/html/rfc7748)
- Cipher Function: ChaChaPoly - AEAD_CHACHA20_POLY1305 podle specifikace v [RFC-7539](https://tools.ietf.org/html/rfc7539) sekce 2.8. 12bajtový nonce, s prvními 4 bajty nastavenými na nulu. Identické s tím v [NTCP2](/docs/specs/ntcp2/)
- Hash Function: SHA256 - Standardní 32bajtový hash, již rozsáhle používaný v I2P

### Vzory handshake

Handshaky používají [Noise](https://noiseprotocol.org/noise.html) handshake vzory.

Používá se následující mapování písmen:

- e = jednorázový dočasný klíč
- s = statický klíč
- p = obsah zprávy

Požadavek na sestavení je identický s Noise N patternem. Toto je také identické s první zprávou (Session Request) v XK patternu používaném v [NTCP2](/docs/specs/ntcp2/).

```
<- s
  ...
  e es p ->
```
### Šifrování požadavků

Záznamy požadavku na výstavbu jsou vytvořeny tvůrcem tunelu a asymetricky šifrovány pro jednotlivé skoky. Toto asymetrické šifrování záznamů požadavku je v současnosti ElGamal jak je definováno v [Cryptography](/docs/specs/cryptography/) a obsahuje SHA-256 kontrolní součet. Tento návrh není forward-secret (neposkytuje dopřednou tajnost).

Design ECIES používá jednosměrný Noise pattern "N" s ECIES-X25519 ephemeral-static DH, s HKDF a ChaCha20/Poly1305 AEAD pro forward secrecy, integritu a autentifikaci. Alice je žadatel o vytvoření tunnelu. Každý skok v tunnelu je Bob.

### Šifrování odpovědí

Build reply záznamy jsou vytvořeny tvůrcem hopů a symetricky zašifrovány pro tvůrce. Toto symetrické šifrování ElGamal reply záznamů používá AES s předřazeným SHA-256 kontrolním součtem. Tento návrh není forward-secret.

ECIES odpovědi používají ChaCha20/Poly1305 AEAD pro integritu a autentizaci.

## Specifikace dlouhých záznamů

POZNÁMKA: Zastaralé, nepoužívané. Použijte formát Short Record uvedený níže.

### Záznamy požadavků na sestavení

Šifrované BuildRequestRecords mají 528 bajtů jak pro ElGamal, tak pro ECIES, kvůli kompatibilitě.

#### Záznam požadavku nešifrovaný

Toto je specifikace tunnel BuildRequestRecord pro ECIES-X25519 routery. Shrnutí změn:

- Odstranit nepoužívaný 32-bytový hash routeru
- Změnit čas požadavku z hodin na minuty
- Přidat pole vypršení pro budoucí variabilní čas tunnelu
- Přidat více místa pro příznaky
- Přidat mapování pro další možnosti sestavení
- AES-256 klíč odpovědi a IV se nepoužívají pro vlastní záznam odpovědi hopu
- Nešifrovaný záznam je delší, protože je menší režie šifrování

Záznam požadavku neobsahuje žádné ChaCha reply klíče. Tyto klíče jsou odvozeny z KDF. Viz níže.

Všechna pole jsou ve formátu big-endian.

Nešifrovaná velikost: 464 bajtů

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-3</td><td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel ID to receive messages as, nonzero</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">4-7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next tunnel ID, nonzero</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">8-39</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next router identity hash</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">40-71</td><td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 tunnel layer key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">72-103</td><td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 tunnel IV key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">104-135</td><td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 reply key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">136-151</td><td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 reply IV</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">152</td><td style="border:1px solid var(--color-border); padding:0.6rem;">flags</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">153-155</td><td style="border:1px solid var(--color-border); padding:0.6rem;">more flags, unused, set to 0 for compatibility</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">156-159</td><td style="border:1px solid var(--color-border); padding:0.6rem;">request time (in minutes since the epoch, rounded down)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">160-163</td><td style="border:1px solid var(--color-border); padding:0.6rem;">request expiration (in seconds since creation)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">164-167</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next message ID</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">168-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel build options (Mapping)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">other data as implied by flags or options</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-463</td><td style="border:1px solid var(--color-border); padding:0.6rem;">random padding</td></tr>
</tbody>
</table>
Pole flags je stejné jako je definováno v [Tunnel-Creation](/docs/specs/tunnel-creation/) a obsahuje následující:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bit</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;" colspan="2"><em>Bit order: 76543210 (bit 7 is MSB)</em></td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">if set, allow messages from anyone</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">6</td><td style="border:1px solid var(--color-border); padding:0.6rem;">if set, allow messages to anyone, and send the reply to the specified next hop in a Tunnel Build Reply Message</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">5-0</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Undefined, must set to 0 for compatibility with future options</td></tr>
</tbody>
</table>
Bit 7 označuje, že hop bude inbound gateway (IBGW). Bit 6 označuje, že hop bude outbound endpoint (OBEP). Pokud není nastaven žádný bit, hop bude intermediate participant. Oba bity nemohou být nastaveny současně.

Vypršení požadavku je pro budoucí proměnnou dobu trvání tunnelu. Prozatím je jedinou podporovanou hodnotou 600 (10 minut).

Možnosti sestavení tunelu jsou struktura Mapping, jak je definována v [Common](/docs/specs/common-structures/). Jediné aktuálně definované možnosti jsou pro parametry šířky pásma, od API 0.9.65, viz níže pro podrobnosti. Pokud je struktura Mapping prázdná, jedná se o dva bajty 0x00 0x00. Maximální velikost Mapping (včetně pole délky) je 296 bajtů a maximální hodnota pole délky Mapping je 294.

#### Záznam požadavku zašifrován

Všechna pole jsou big-endian kromě dočasného veřejného klíče, který je little-endian.

Šifrovaná velikost: 528 bajtů

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-15</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Hop's truncated identity hash</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">16-47</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Sender's ephemeral X25519 public key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">48-511</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20 encrypted BuildRequestRecord</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">512-527</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Poly1305 MAC</td></tr>
</tbody>
</table>
### Sestavit záznamy odpovědí

Šifrované BuildReplyRecords mají 528 bajtů jak pro ElGamal, tak pro ECIES, z důvodu kompatibility.

#### Reply Record nezašifrovaný

Toto je specifikace tunnel BuildReplyRecord pro ECIES-X25519 routery. Shrnutí změn:

- Přidat mapování pro možnosti odpovědi na sestavení
- Nezašifrovaný záznam je delší, protože má menší režijní náklady šifrování

ECIES odpovědi jsou šifrovány pomocí ChaCha20/Poly1305.

Všechna pole jsou ve formátu big-endian.

Nezašifrovaná velikost: 512 bajtů

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel Build Reply Options (Mapping)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">other data as implied by options</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-510</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Random padding</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">511</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Reply byte</td></tr>
</tbody>
</table>
Možnosti odpovědi na sestavení tunelu je struktura Mapping definovaná v [Common](/docs/specs/common-structures/). Jediné možnosti aktuálně definované jsou pro parametry šířky pásma, od API 0.9.65, viz níže pro podrobnosti. Pokud je struktura Mapping prázdná, jsou to dva bajty 0x00 0x00. Maximální velikost Mapping (včetně pole délky) je 511 bajtů a maximální hodnota pole délky Mapping je 509.

Odpověďový byte je jedna z následujících hodnot definovaných v [Tunnel-Creation](/docs/specs/tunnel-creation/) pro zamezení fingerprintingu:

- 0x00 (přijmout)
- 30 (TUNNEL_REJECT_BANDWIDTH)

#### Šifrovaný záznam odpovědi

Šifrovaná velikost: 528 bajtů

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-511</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20 encrypted BuildReplyRecord</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">512-527</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Poly1305 MAC</td></tr>
</tbody>
</table>
Po úplném přechodu na ECIES záznamy platí stejná pravidla pro rozsahové vyplňování jako pro záznamy požadavků.

### Symetrické šifrování záznamů

Smíšené tunnely jsou povolené a nezbytné pro přechod z ElGamal na ECIES. Během přechodného období bude stále více routerů používat ECIES klíče.

Předběžné zpracování symetrické kryptografie bude probíhat stejným způsobem:

- "encryption":
  - šifra běží v režimu dešifrování
  - záznamy požadavků preventivně dešifrovány v předběžném zpracování (skrývání šifrovaných záznamů požadavků)
- "decryption":
  - šifra běží v režimu šifrování
  - záznamy požadavků šifrovány (odhalování dalšího plaintext záznamu požadavku) pomocí účastnických hopů
- ChaCha20 nemá "režimy", takže se jednoduše spouští třikrát:
  - jednou v předběžném zpracování
  - jednou hopem
  - jednou při finálním zpracování odpovědi

Když jsou použity smíšené tunnely, tvůrci tunnelů budou muset založit symetrické šifrování BuildRequestRecord na typu šifrování současného a předchozího hopu.

Každý hop použije svůj vlastní typ šifrování pro šifrování BuildReplyRecords a dalších záznamů ve VariableTunnelBuildMessage (VTBM).

Na zpáteční cestě bude koncový bod (odesílatel) muset zrušit [Multiple-Encryption](https://en.wikipedia.org/wiki/Multiple_encryption) pomocí reply klíče každého uzlu.

Pro objasnění se podívejme na příklad odchozího tunnelu s ECIES obklopeným ElGamalem:

- Odesílatel (OBGW) -> ElGamal (H1) -> ECIES (H2) -> ElGamal (H3)

Všechny BuildRequestRecords jsou ve svém šifrovaném stavu (pomocí ElGamal nebo ECIES).

AES256/CBC šifra, když je použita, je stále používána pro každý záznam, bez propojení napříč více záznamy.

Podobně bude ChaCha20 použit k šifrování každého záznamu, nikoli k streamování přes celý VTBM.

Záznamy požadavků jsou předpracovány odesílatelem (OBGW):

- H3 záznam je "šifrován" pomocí:
  - H2 reply key (ChaCha20)
  - H1 reply key (AES256/CBC)
- H2 záznam je "šifrován" pomocí:
  - H1 reply key (AES256/CBC)
- H1 záznam odchází bez symetrického šifrování

Pouze H2 kontroluje příznak šifrování odpovědi a vidí, že následuje AES256/CBC.

Po zpracování každým hopem jsou záznamy v "dešifrovaném" stavu:

- Záznam H3 je "dešifrován" pomocí:
  - Reply key H3 (AES256/CBC)
- Záznam H2 je "dešifrován" pomocí:
  - Reply key H3 (AES256/CBC)
  - Reply key H2 (ChaCha20-Poly1305)
- Záznam H1 je "dešifrován" pomocí:
  - Reply key H3 (AES256/CBC)
  - Reply key H2 (ChaCha20)
  - Reply key H1 (AES256/CBC)

Tvůrce tunnelu, tzv. Inbound Endpoint (IBEP), zpracovává odpověď:

- Záznam H3 je "zašifrován" pomocí:
  - Odpověďového klíče H3 (AES256/CBC)
- Záznam H2 je "zašifrován" pomocí:
  - Odpověďového klíče H3 (AES256/CBC)
  - Odpověďového klíče H2 (ChaCha20-Poly1305)
- Záznam H1 je "zašifrován" pomocí:
  - Odpověďového klíče H3 (AES256/CBC)
  - Odpověďového klíče H2 (ChaCha20)
  - Odpověďového klíče H1 (AES256/CBC)

### Klíče záznamů požadavků

Tyto klíče jsou explicitně zahrnuty v ElGamal BuildRequestRecords. Pro ECIES BuildRequestRecords jsou zahrnuty tunnel klíče a AES reply klíče, ale ChaCha reply klíče jsou odvozeny z DH výměny. Podrobnosti o statických ECIES klíčích routeru najdete v [Prop156](/proposals/156/).

Níže je popis toho, jak odvodit klíče dříve přenesené v záznamech požadavků.

#### KDF pro počáteční ck a h

Toto je standardní [NOISE](https://noiseprotocol.org/noise.html) pro vzor "N" se standardním názvem protokolu.

```
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
#### KDF pro Request Record

ElGamal tvůrci tunelů generují dočasný X25519 pár klíčů pro každý ECIES hop v tunelu a používají výše uvedené schéma pro šifrování svého BuildRequestRecord. ElGamal tvůrci tunelů budou používat schéma předcházející této specifikaci pro šifrování do ElGamal hopů.

Tvůrci ECIES tunnelů budou muset šifrovat k veřejnému klíči každého ElGamal hopu pomocí schématu definovaného v [Tunnel-Creation](/docs/specs/tunnel-creation/). Tvůrci ECIES tunnelů budou používat výše uvedené schéma pro šifrování k ECIES hopům.

To znamená, že tunnel skoky uvidí pouze šifrované záznamy ze stejného typu šifrování.

Pro tvůrce tunelů ElGamal a ECIES budou generovat jedinečné dočasné X25519 páry klíčů na jeden hop pro šifrování do ECIES hopů.

**DŮLEŽITÉ**: Ephemeral keys (dočasné klíče) musí být jedinečné pro každý ECIES hop a pro každý build record. Nepoužívání jedinečných klíčů otevírá útočný vektor pro spolupracující hopy k potvrzení, že se nacházejí ve stejném tunnel.

```
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
`replyKey`, `layerKey` a `layerIV` musí být stále zahrnuty uvnitř ElGamal záznamů a mohou být generovány náhodně.

### Šifrování záznamu odpovědi

Záznam odpovědi je šifrován pomocí ChaCha20/Poly1305.

```
// AEAD parameters
k = chainkey from build request
n = 0
plaintext = 512 byte build reply record
ad = h from build request

ciphertext = ENCRYPT(k, n, plaintext, ad)
```
## Specifikace krátkých záznamů

Tato specifikace používá dvě nové I2NP zprávy pro stavbu tunelů, Short Tunnel Build Message (typ 25) a Outbound Tunnel Build Reply Message (typ 26).

Tvůrce tunelu a všechny přeskoky v vytvořeném tunelu musí podporovat ECIES-X25519 a nejméně verzi 0.9.51. Přeskoky v odpovědním tunelu (pro odchozí sestavení) nebo v odchozím tunelu (pro příchozí sestavení) nemají žádné požadavky.

Šifrované záznamy požadavků a odpovědí budou mít 218 bajtů, ve sravnání s 528 bajty pro všechny ostatní build zprávy.

Záznamy požadavků v prostém textu budou mít 154 bajtů, ve srovnání s 222 bajty pro ElGamal záznamy a 464 bajty pro ECIES záznamy jak jsou definovány výše.

Záznamy odpovědi v otevřeném textu budou mít 202 bajtů, ve srovnání s 496 bajty pro ElGamal záznamy a 512 bajty pro ECIES záznamy jak jsou definovány výše.

Šifrování odpovědi bude ChaCha20/Poly1305 pro vlastní záznam hop-u a ChaCha20 (NE ChaCha20/Poly1305) pro ostatní záznamy ve zprávě build.

Záznamy požadavků budou menší díky použití HKDF pro vytvoření klíčů vrstvy a odpovědi, takže nebudou explicitně zahrnuty v požadavku.

### Tok zpráv

```
STBM: Short tunnel build message (type 25)
OTBRM: Outbound tunnel build reply message (type 26)

Outbound Build A-B-C
Reply through existing inbound D-E-F


                New Tunnel
         STBM      STBM      STBM
Creator ------> A ------> B ------> C ---\
                                   OBEP   \
                                          | Garlic wrapped (optional)
                                          | OTBRM
                                          | (TUNNEL delivery)
                                          | from OBEP to
                                          | creator
              Existing Tunnel             /
Creator <-------F---------E-------- D <--/
                                   IBGW



Inbound Build D-E-F
Sent through existing outbound A-B-C


              Existing Tunnel
Creator ------> A ------> B ------> C ---\
                                  OBEP    \
                                          | Garlic wrapped (optional)
                                          | STBM
                                          | (ROUTER delivery)
                                          | from creator
                New Tunnel                | to IBGW
          STBM      STBM      STBM        /
Creator <------ F <------ E <------ D <--/
                                   IBGW
```
#### Poznámky

Garlic encryption zpráv je skryje před OBEP (pro příchozí build) nebo IBGW (pro odchozí build). Toto je doporučené, ale není vyžadované. Pokud jsou OBEP a IBGW stejný router, není to nutné.

### Záznamy krátkých žádostí o sestavení

Krátké šifrované BuildRequestRecords mají 218 bajtů.

#### Záznam krátkého požadavku nešifrovaný

Shrnutí změn z dlouhých záznamů:

- Změnit nezašifrovanou délku z 464 na 154 bajtů
- Změnit zašifrovanou délku z 528 na 218 bajtů
- Odstranit vrstvové a odpovědní klíče a IV, budou generovány z KDF

Záznam požadavku neobsahuje žádné ChaCha odpovědi klíče. Tyto klíče jsou odvozeny z KDF. Viz níže.

Všechna pole jsou ve formátu big-endian.

Nezašifrovaná velikost: 154 bajtů.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-3</td><td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel ID to receive messages as, nonzero</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">4-7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next tunnel ID, nonzero</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">8-39</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next router identity hash</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">40</td><td style="border:1px solid var(--color-border); padding:0.6rem;">flags</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">41-42</td><td style="border:1px solid var(--color-border); padding:0.6rem;">more flags, unused, set to 0 for compatibility</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">43</td><td style="border:1px solid var(--color-border); padding:0.6rem;">layer encryption type</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">44-47</td><td style="border:1px solid var(--color-border); padding:0.6rem;">request time (in minutes since the epoch, rounded down)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">48-51</td><td style="border:1px solid var(--color-border); padding:0.6rem;">request expiration (in seconds since creation)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">52-55</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next message ID</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">56-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel build options (Mapping)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">other data as implied by flags or options</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-153</td><td style="border:1px solid var(--color-border); padding:0.6rem;">random padding (see below)</td></tr>
</tbody>
</table>
Pole flags je stejné jako definované v [Tunnel-Creation](/docs/specs/tunnel-creation/) a obsahuje následující:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bit</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;" colspan="2"><em>Bit order: 76543210 (bit 7 is MSB)</em></td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">if set, allow messages from anyone</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">6</td><td style="border:1px solid var(--color-border); padding:0.6rem;">if set, allow messages to anyone, and send the reply to the specified next hop in a Tunnel Build Reply Message</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">5-0</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Undefined, must set to 0 for compatibility with future options</td></tr>
</tbody>
</table>
Bit 7 označuje, že hop bude příchozí bránou (IBGW). Bit 6 označuje, že hop bude odchozím koncovým bodem (OBEP). Pokud není nastaven ani jeden bit, hop bude zprostředkujícím účastníkem. Oba nemohou být nastaveny současně.

Typ šifrování vrstvy: 0 pro AES (jako v současných tunnelech); 1 pro budoucí (ChaCha?)

Vypršení požadavku je určeno pro budoucí variabilní délku trvání tunelu. Prozatím je jedinou podporovanou hodnotou 600 (10 minut).

Ephemeral veřejný klíč tvůrce je ECIES klíč, big-endian. Používá se pro KDF pro IBGW vrstvu a klíče a IV pro odpovědi. Je zahrnut pouze v plaintext záznamu ve zprávě Inbound Tunnel Build. Je vyžadován, protože na této vrstvě neexistuje žádný DH pro build záznam.

Možnosti stavby tunelu jsou strukturou Mapping, jak je definováno v [Common](/docs/specs/common-structures/). Jediné možnosti, které jsou v současnosti definovány, jsou pro parametry šířky pásma, od API 0.9.65, viz níže pro podrobnosti. Pokud je struktura Mapping prázdná, jsou to dva bajty 0x00 0x00. Maximální velikost struktury Mapping (včetně pole délky) je 98 bajtů a maximální hodnota pole délky Mapping je 96.

#### Krátký zašifrovaný záznam požadavku

Všechna pole jsou ve formátu big-endian kromě dočasného veřejného klíče, který je ve formátu little-endian.

Velikost zašifrovaných dat: 218 bajtů

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-15</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Hop's truncated identity hash</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">16-47</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Sender's ephemeral X25519 public key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">48-201</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20 encrypted ShortBuildRequestRecord</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">202-217</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Poly1305 MAC</td></tr>
</tbody>
</table>
### Krátké záznamy odpovědi sestavení

Krátké šifrované BuildReplyRecords mají 218 bajtů.

#### Záznam krátké odpovědi nezašifrovaný

Shrnutí změn z dlouhých záznamů:

- Změnit nešifrovanou délku z 512 na 202 bajtů
- Změnit šifrovanou délku z 528 na 218 bajtů

ECIES odpovědi jsou šifrovány pomocí ChaCha20/Poly1305.

Všechna pole jsou v pořadí big-endian.

Nezašifrovaná velikost: 202 bajtů.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel Build Reply Options (Mapping)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">other data as implied by options</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-200</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Random padding (see below)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">201</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Reply byte</td></tr>
</tbody>
</table>
Možnosti odpovědi na sestavení tunelu jsou struktura Mapping, jak je definováno v [Common](/docs/specs/common-structures/). Jediné aktuálně definované možnosti jsou pro parametry šířky pásma, od API 0.9.65, viz níže pro podrobnosti. Pokud je struktura Mapping prázdná, jedná se o dva bajty 0x00 0x00. Maximální velikost Mapping (včetně pole délky) je 201 bajtů a maximální hodnota pole délky Mapping je 199.

Bajt odpovědi je jedna z následujících hodnot definovaných v [Tunnel-Creation](/docs/specs/tunnel-creation/) pro zamezení fingerprintingu:

- 0x00 (přijmout)
- 30 (TUNNEL_REJECT_BANDWIDTH)

V budoucnu může být definována další hodnota odpovědi pro reprezentaci odmítnutí nepodporovaných možností.

#### Zašifrovaný záznam krátké odpovědi

Velikost šifrovaných dat: 218 bajtů

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-201</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20 encrypted ShortBuildReplyRecord</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">202-217</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Poly1305 MAC</td></tr>
</tbody>
</table>
### KDF

Používáme chaining key (ck) ze stavu Noise po šifrování/dešifrování záznamu výstavby tunelu k odvození následujících klíčů: reply key, AES layer key, AES IV key a garlic reply key/tag pro OBEP.

Reply keys: Poznamenejte, že KDF se mírně liší pro OBEP a non-OBEP hopy. Na rozdíl od dlouhých záznamů nemůžeme použít levou část ck pro reply key, protože to není poslední a bude použito později. Reply key se používá k šifrování odpovědi tohoto záznamu pomocí AEAD/ChaCha20/Poly1305 a ChaCha20 pro odpověď na ostatní záznamy. Oba používají stejný klíč. Nonce je pozice záznamu ve zprávě počínaje od 0. Podrobnosti viz níže.

```
keydata = HKDF(ck, ZEROLEN, "SMTunnelReplyKey", 64)
replyKey = keydata[32:63]
ck = keydata[0:31]

AES Layer key:
keydata = HKDF(ck, ZEROLEN, "SMTunnelLayerKey", 64)
layerKey = keydata[32:63]

IV key for non-OBEP record:
ivKey = keydata[0:31]
because it's last

IV key for OBEP record:
ck = keydata[0:31]
keydata = HKDF(ck, ZEROLEN, "TunnelLayerIVKey", 64)
ivKey = keydata[32:63]
ck = keydata[0:31]

OBEP garlic reply key/tag:
keydata = HKDF(ck, ZEROLEN, "RGarlicKeyAndTag", 64)
garlicReplyKey = keydata[32:63]
garlicReplyTag = keydata[0:7]
```
Poznámka: KDF pro IV klíč na OBEP se liší od těch pro ostatní směrování, i když odpověď není šifrována garlic encryption.

#### Šifrování záznamů

Reply záznam samotného hopu je šifrován pomocí ChaCha20/Poly1305. Toto je stejné jako pro specifikaci dlouhého záznamu výše, S VÝJIMKOU toho, že 'n' je číslo záznamu 0-7, místo aby to bylo vždy 0. Viz [RFC-7539](https://tools.ietf.org/html/rfc7539).

```
// AEAD parameters
k = replyKey from KDF above
n = record number 0-7
plaintext = 202 byte build reply record
ad = h from build request

ciphertext = ENCRYPT(k, n, plaintext, ad)
```
Ostatní záznamy jsou iterativně a symetricky šifrovány na každém skoku pomocí ChaCha20 (NIKOLIV ChaCha20/Poly1305). To se liší od specifikace dlouhého záznamu výše, která používá AES a nepoužívá číslo záznamu.

Číslo záznamu se vkládá do IV na byte 4, protože ChaCha20 používá 12-bytový IV s little-endian nonce na bytech 4-11. Viz [RFC-7539](https://tools.ietf.org/html/rfc7539).

```
// Parameters
k = replyKey from KDF above
n = record number 0-7
iv = 12 bytes, all zeros except iv[4] = n
plaintext = 218 byte encrypted record

ciphertext = ENCRYPT(k, iv, plaintext)
```
#### Garlic Encryption

Garlic wrapping zpráv je skryje před OBEP (pro příchozí build) nebo IBGW (pro odchozí build). Toto je doporučeno, ale není vyžadováno. Pokud jsou OBEP a IBGW stejný router, není to nutné.

Garlic encryption příchozí Short Tunnel Build Message, vytvořené tvůrcem, šifrované pro ECIES IBGW, používá Noise 'N' šifrování, jak je definováno v [ECIES-ROUTERS](/docs/specs/ecies-routers/).

Garlic encryption odchozí zprávy Tunnel Build Reply Message od OBEP, šifrované pro tvůrce, používá zprávy Existing Session s 32-bytovým garlic reply klíčem a 8-bytovým garlic reply tagem z KDF výše. Formát je specifikován pro odpovědi na Database Lookups v [I2NP](/docs/specs/i2np/), [ECIES-ROUTERS](/docs/specs/ecies-routers/) a [ECIES-X25519](/docs/specs/ecies/).

#### Šifrování vrstev

Tato specifikace zahrnuje pole typu šifrování vrstvy v záznamu požadavku na sestavení. Jediný typ šifrování vrstvy aktuálně podporovaný je typ 0, což je AES. To je nezměněno oproti předchozím specifikacím, až na to, že klíč vrstvy a IV klíč jsou odvozeny z výše uvedené KDF místo toho, aby byly zahrnuty v záznamu požadavku na sestavení.

Přidání nových typů vrstvového šifrování, například ChaCha20, je tématem pro další výzkum a v současné době není součástí této specifikace.

## Poznámky k implementaci

- Starší routery nekontrolují typ šifrování skoku a budou odesílat ElGamal-šifrované záznamy. Některé nedávné routery jsou chybové a budou odesílat různé typy poškozených záznamů. Implementátoři by měli tyto záznamy detekovat a odmítnout před DH operací, pokud je to možné, aby se snížilo využití CPU.

### Záznamy sestavení

Pořadí build záznamů musí být randomizováno, aby prostřední uzly neznaly svou pozici v rámci tunelu.

Doporučený minimální počet build records je 4. Pokud je build records více než hopů, musí být přidány "falešné" záznamy obsahující náhodná nebo implementačně specifická data. Pro inbound tunnel builds musí vždy existovat jeden "falešný" záznam pro původní router s korektním 16-bytovým hash prefixem a skutečným X25519 efemérním klíčem, jinak nejbližší hop pozná, že další hop je původce.

Zbytek "falešného" záznamu může být náhodná data, nebo může být zašifrován v jakémkoliv formátu, aby původce mohl poslat data sám sobě o sestavení, možná za účelem snížení nároků na úložiště pro probíhající sestavení.

Původci příchozích tunnelů musí použít nějakou metodu k ověření, že jejich "falešný" záznam nebyl upraven předchozím hopem, protože to může být také použito pro deanonymizaci. Původce může uložit a ověřit kontrolní součet záznamu, nebo zahrnout kontrolní součet do záznamu, nebo použít AEAD funkci pro šifrování/dešifrování, závisí na implementaci. Pokud byl upraven 16-bajtový prefix hashe nebo jiný obsah záznamu sestavení, router musí tunnel zahodit.

Falešné záznamy pro odchozí tunely a dodatečné falešné záznamy pro příchozí tunely nemají tyto požadavky a mohou být zcela náhodná data, protože nebudou nikdy viditelné pro žádný hop. Může být stále žádoucí, aby původce ověřil, že nebyly upraveny.

## Parametry šířky pásma tunnel

### Přehled

Jak jsme v posledních několika letech zvýšili výkon sítě novými protokoly, typy šifrování a vylepšeními řízení přetížení, stávají se možnými rychlejší aplikace jako je streamování videa. Tyto aplikace vyžadují vysokou šířku pásma v každém skoku svých klientských tunnelů.

Účastnické routery však nemají žádné informace o tom, kolik šířky pásma bude tunnel používat, když obdrží zprávu o vybudování tunnelu. Mohou tunnel pouze přijmout nebo odmítnout na základě aktuální celkové šířky pásma používané všemi účastnickými tunnely a celkového limitu šířky pásma pro účastnické tunnely.

Požadující routery také nemají žádné informace o tom, kolik šířky pásma je k dispozici na každém skoku.

Také routery v současnosti nemají způsob, jak omezit příchozí provoz v tunelu. To by bylo velmi užitečné během přetížení nebo DDoS útoku na službu.

Parametry šířky pásma tunnel v žádostech o sestavení tunnel a odpovědích přidávají podporu pro tyto funkce. Další informace najdete v [Prop168](/proposals/168/). Tyto parametry jsou definovány od API 0.9.65, ale podpora se může lišit podle implementace. Jsou podporovány jak pro dlouhé, tak pro krátké ECIES build záznamy.

### Možnosti požadavku na sestavení

Následující tři možnosti mohou být nastaveny v mapovacím poli možností sestavení tunelu záznamu: Žádající router může zahrnout jakékoli, všechny, nebo žádné.

- m := minimální požadovaná šířka pásma pro tento tunnel (KBps kladné celé číslo jako řetězec)
- r := požadovaná šířka pásma pro tento tunnel (KBps kladné celé číslo jako řetězec)
- l := omezení šířky pásma pro tento tunnel; odesílá se pouze do IBGW (KBps kladné celé číslo jako řetězec)

Omezení: m <= r <= l

Zúčastněný router by měl tunnel odmítnout, pokud je specifikováno "m" a nemůže poskytnout alespoň takovou šířku pásma.

Možnosti požadavku jsou odeslány každému účastníkovi v odpovídajícím šifrovaném záznamu žádosti o sestavení a nejsou viditelné ostatním účastníkům.

### Možnost odpovědi sestavení

Následující možnost může být nastavena v mapovacím poli možností odpovědi na tunnel build ve záznamu, když je odpověď ACCEPTED:

- b := šířka pásma dostupná pro tento tunel (KBps kladné celé číslo jako řetězec)

Omezení: b >= m

Zúčastněný router by měl tento údaj zahrnout, pokud bylo v žádosti o sestavení uvedeno buď "m" nebo "r". Hodnota by měla být alespoň stejná jako hodnota "m", pokud byla specifikována, ale může být menší nebo větší než hodnota "r", pokud byla specifikována.

Účastnící se router by se měl pokusit rezervovat a poskytnout alespoň tolik šířky pásma pro tunnel, avšak toto není zaručeno. Routery nemohou předpovídat podmínky 10 minut do budoucna a účastnický provoz má nižší prioritu než vlastní provoz a tunnely routeru.

Router také mohou v případě potřeby překročit dostupnou šířku pásma, což je pravděpodobně žádoucí, protože ji mohou odmítnout jiné přeskoky v tunnelu.

Z těchto důvodů by měla být odpověď účastnícího se router považována za závazek na bázi nejlepšího úsilí, nikoli za záruku.

Možnosti odpovědi jsou odeslány do požadujícího routeru v odpovídajícím šifrovaném záznamu odpovědi na sestavení a nejsou viditelné ostatním účastníkům.

### Poznámky k implementaci

Parametry šířky pásma jsou zobrazeny tak, jak je vidí účastnící se routery na vrstvě tunelu, tj. počet zpráv tunelu o pevné velikosti 1 KB za sekundu. Režie transportu (NTCP2 nebo SSU2) není zahrnuta.

Tato šířka pásma může být mnohem větší nebo menší než šířka pásma pozorovaná na klientovi. Zprávy tunelu obsahují značnou režii, včetně režie z vyšších vrstev včetně ratchet a streaming. Přerušované malé zprávy jako streaming ack budou rozšířeny na 1 KB každá. Nicméně gzip komprese na vrstvě I2CP může výrazně snížit šířku pásma.

Nejjednodušší implementace na žádajícím routeru je použít průměrnou, minimální a/nebo maximální šířku pásma současných tunnelů v poolu k výpočtu hodnot, které se vloží do požadavku. Složitější algoritmy jsou možné a závisí na implementátorovi.

V současnosti neexistují žádné I2CP nebo SAM možnosti definované pro klienta, aby informoval router o požadované šířce pásma, a zde nejsou navrženy žádné nové možnosti. Možnosti mohou být definovány později, pokud to bude nutné.

Implementace mohou použít dostupnou šířku pásma nebo jakákoliv jiná data, algoritmus, místní zásady nebo místní konfiguraci k výpočtu hodnoty šířky pásma vrácené v odpovědi build.

## Reference

- [Společné](/docs/specs/common-structures/)
- [Kryptografie](/docs/specs/cryptography/)
- [ECIES-ROUTERS](/docs/specs/ecies-routers/)
- [ECIES-X25519](/docs/specs/ecies/)
- [EncryptedLeaseSet](/docs/specs/encryptedleaseset/)
- [I2NP](/docs/specs/i2np/)
- [Vícenásobné šifrování](https://en.wikipedia.org/wiki/Multiple_encryption)
- [NOISE](https://noiseprotocol.org/noise.html)
- [NTCP2](/docs/specs/ntcp2/)
- [Prop119](/proposals/119/)
- [Prop143](/proposals/143/)
- [Prop152](/proposals/152/)
- [Prop153](/proposals/153/)
- [Prop156](/proposals/156/)
- [Prop157](/proposals/157/)
- [Prop168](/proposals/168/)
- [RFC-7539](https://tools.ietf.org/html/rfc7539)
- [RFC-7748](https://tools.ietf.org/html/rfc7748)
- [Vytváření tunelů](/docs/specs/tunnel-creation/)
