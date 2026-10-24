---
title: "PQ Hybrid SSU2"
description: "Post-kvantová hybridní varianta transportního protokolu SSU2 využívající ML-KEM"
slug: "ssu2-hybrid"
lastupdated: "2026-10"
category: "Transporty"
accurateFor: "0.9.71"
---

### Stav

Beta Q2 2026, vydání Q3 2026

## Přehled

Toto je hybridní post-kvantová varianta transportního protokolu SSU2, navržená v Proposal 169. Další kontext naleznete v daném návrhu.

PQ Hybrid SSU2 je definováno pouze na stejné adrese a portu jako standardní SSU2. Provoz na jiném portu nebo bez podpory standardního SSU2 není povolen a nebude povolen po dobu několika let, dokud nebude standardní SSU2 označeno jako zastaralé.

Tato specifikace dokumentuje pouze změny potřebné pro standardní SSU2 k podpoře PQ Hybrid. Podrobnosti o základní implementaci naleznete ve specifikaci SSU2.

## Návrh

Podporujeme standardy NIST FIPS 203 a 204 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf), které vycházejí z CRYSTALS-Kyber a CRYSTALS-Dilithium (verze 3.1, 3 a starší), ale NEJSOU s nimi kompatibilní.

### Výměna klíčů

PQ KEM poskytuje pouze dočasné (ephemeral) klíče a přímo nepodporuje handshake se statickými klíči, jako jsou Noise XK a IK. Typy šifrování jsou stejné jako ty používané v PQ Hybrid Ratchet a jsou definovány v dokumentu o společných strukturách [/docs/specs/common-structures/](/docs/specs/common-structures/), přičemž jako v [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) jsou hybridní typy definovány pouze v kombinaci s X25519.

Typy šifrování jsou:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">SSU2 Version</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
</tr>
</table>
### Povolené kombinace

Nové typy šifrování jsou uvedeny v RouterAddresses. Typ šifrování v certifikátu klíče bude nadále typu 4.

## Specifikace

### Vzory handshake

Handshaky (navazování spojení) využívají vzory handshake z [Noise Protocol](https://noiseprotocol.org/noise.html).

Používá se následující mapování písmen:

- e = jednorázový efemerní klíč
- s = statický klíč
- p = obsah zprávy
- e1 = jednorázový efemerní PQ klíč, odeslaný od Alice k Bobovi
- ekem1 = šifrový text KEM, odeslaný od Boba k Alici

Následující úpravy XK a IK pro hybridní dopřednou tajnost (hfs) jsou specifikovány v [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) sekci 5:

```
XK:                       XKhfs:
  <- s                      <- s
  ...                       ...
  -> e, es, p               -> e, es, e1, p
  <- e, ee, p               <- e, ee, ekem1, p
  -> s, se                  -> s, se
  <- p                      <- p
  p ->                      p ->


  e1 and ekem1 are encrypted. See pattern definitions below.
  NOTE: e1 and ekem1 are different sizes (unlike X25519)
```
Vzor e1 je definován následovně, jak je uvedeno v [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) sekci 4:

```
For Alice:
  (encap_key, decap_key) = PQ_KEYGEN()

  // EncryptAndHash(encap_key)
  ciphertext = ENCRYPT(k, n, encap_key, ad)
  n++
  MixHash(ciphertext)

  For Bob:

  // DecryptAndHash(ciphertext)
  encap_key = DECRYPT(k, n, ciphertext, ad)
  n++
  MixHash(ciphertext)
```
Vzor ekem1 je definován následovně, jak je uvedeno v [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) sekci 4:

```
For Bob:

  (kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

  // EncryptAndHash(kem_ciphertext)
  ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)
  MixHash(ciphertext)

  // MixKey
  MixKey(kem_shared_key)


  For Alice:

  // DecryptAndHash(ciphertext)
  kem_ciphertext = DECRYPT(k, n, ciphertext, ad)
  MixHash(ciphertext)

  // MixKey
  kem_shared_key = DECAPS(kem_ciphertext, decap_key)
  MixKey(kem_shared_key)
```
### KDF pro Noise handshake

#### Přehled

Hybridní handshake (výměna klíčů) je definován ve [specifikaci Noise HFS](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf). První zpráva, od Alice k Bobovi, obsahuje e1, encapsulační klíč (klíč pro zapouzdření), před samotným obsahem zprávy. Ten je zpracován jako dodatečný statický klíč; zavolejte na něj EncryptAndHash() (jako Alice) nebo DecryptAndHash() (jako Bob). Poté zpracujte obsah zprávy obvyklým způsobem.

Druhá zpráva, od Boba k Alici, obsahuje ekem1, šifrovaný text, před samotným obsahem zprávy. Tento text je zpracován jako dodatečný statický klíč; zavolejte na něj EncryptAndHash() (jako Bob) nebo DecryptAndHash() (jako Alice). Poté vypočítejte kem_shared_key a zavolejte MixKey(kem_shared_key). Následně zpracujte obsah zprávy obvyklým způsobem.

#### Definované operace ML-KEM

Definujeme následující funkce odpovídající kryptografickým stavebním blokům používaným podle definice v [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

(encap_key, decap_key) = PQ_KEYGEN()

    Alice creates the encapsulation and decapsulation keys
    The encapsulation key is sent in message 1.
    encap_key and decap_key sizes vary based on ML-KEM variant.

(ciphertext, kem_shared_key) = ENCAPS(encap_key)

    Bob calculates the ciphertext and shared key,
    using the ciphertext received in message 1.
    The ciphertext is sent in message 2.
    ciphertext size varies based on ML-KEM variant.
    The kem_shared_key is always 32 bytes.

kem_shared_key = DECAPS(ciphertext, decap_key)

    Alice calculates the shared key,
    using the ciphertext received in message 2.
    The kem_shared_key is always 32 bytes.

Upozorňujeme, že jak encap_key, tak šifrový text jsou zašifrovány uvnitř bloků ChaCha/Poly v Noise handshake zprávách 1 a 2. Budou dešifrovány jako součást procesu handshake.

Klíč kem_shared_key je zakomponován do řetězového klíče pomocí MixHash(). Podrobnosti viz níže.

#### KDF Alice pro zprávu 1

Po vzoru zprávy 'es' a před samotným obsahem přidejte:

```
This is the "e1" message pattern:
  (encap_key, decap_key) = PQ_KEYGEN()

  // EncryptAndHash(encap_key)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, encap_key, ad)
  n++

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)


  End of "e1" message pattern.

  NOTE: For the next section (payload for XK or static key for IK),
  the keydata and chain key remain the same,
  and n now equals 1 (instead of 0 for non-hybrid).
```
#### Bob KDF pro zprávu 1

Po vzoru zprávy 'es' a před samotným obsahem přidejte:

```
This is the "e1" message pattern:

  // DecryptAndHash(encap_key_section)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  encap_key = DECRYPT(k, n, encap_key_section, ad)
  n++

  // MixHash(encap_key_section)
  h = SHA256(h || encap_key_section)

  End of "e1" message pattern.

  NOTE: For the next section (payload for XK or static key for IK),
  the keydata and chain key remain the same,
  and n now equals 1 (instead of 0 for non-hybrid).
```
#### Bob KDF pro zprávu 2

Pro XK: Po vzoru zprávy 'ee' a před datovou částí (payload) přidejte:

```
This is the "ekem1" message pattern:

  (kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

  // EncryptAndHash(kem_ciphertext)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)

  // MixKey(kem_shared_key)
  keydata = HKDF(chainKey, kem_shared_key, "", 64)
  chainKey = keydata[0:31]

  End of "ekem1" message pattern.

  // AEAD parameters for payload section
  ... as in standard SSU2 ...
  k = keydata[32:63]
  ...

```
#### KDF Alice pro zprávu 2

Po vzoru zprávy 'ee' přidejte:

```
This is the "ekem1" message pattern:

  // DecryptAndHash(kem_ciphertext_section)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  kem_ciphertext = DECRYPT(k, n, kem_ciphertext_section, ad)

  // MixHash(kem_ciphertext_section)
  h = SHA256(h || kem_ciphertext_section)

  // MixKey(kem_shared_key)
  kem_shared_key = DECAPS(kem_ciphertext, decap_key)
  keydata = HKDF(chainKey, kem_shared_key, "", 64)
  chainKey = keydata[0:31]

  End of "ekem1" message pattern.

  // AEAD parameters for payload section
  ... as in standard SSU2 ...
  k = keydata[32:63]
  ...

```
#### KDF pro zprávu 3

unchanged

#### KDF pro split()

unchanged

### Podrobnosti o handshake

#### Identifikátory Noise

- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"

Upozorňujeme, že MLKEM-1024 NENÍ podporován pro SSU2, protože klíče jsou příliš velké a nevejdou se do standardního datagramu o velikosti 1500 bajtů.

#### Dlouhá hlavička

Dlouhá hlavička má 32 bajtů. Používá se před vytvořením relace, pro Token Request, SessionRequest, SessionCreated a Retry. Používá se také pro zprávy Peer Test a Hole Punch mimo relaci.

V následujících zprávách nastavte pole ver (verze) v dlouhém záhlaví na hodnotu 3 nebo 4, což označuje MLKEM-512 nebo MLKEM-768.

- (0) Žádost o relaci
- (1) Relace vytvořena
- (9) Opakování
- (10) Žádost o token
- (11) Hole Punch

V následujících zprávách nastavte pole ver (verze) v dlouhém záhlaví na hodnotu 2, jako obvykle, i když je podporováno MLKEM-512 nebo MLKEM-768. Implementace mohou také nastavit hodnotu na 3 nebo 4, pokud to druhá strana podporuje, není to však nutné. Implementace by měly přijímat jakoukoli hodnotu v rozsahu 2–4.

- (7) Peer Test (zprávy mimo relaci 5-7)

Diskuze: Nastavení pole verze na 3 nebo 4 nemusí být striktně nutné pro všechny typy zpráv, ale napomáhá dřívější detekci selhání u nepodporovaných post-kvantových spojení. Zprávy Token Request a Retry (typy 9 a 10) by měly mít verze 3/4 pro konzistenci. Zprávy Hole Punch (typ 11) toto ošetření nemusí vyžadovat, ale budeme se řídit stejným vzorem pro jednotnost. Zprávy Peer Test (typ 7) jsou mimo relaci a nenaznačují záměr zahájit relaci.

- Relay Request
- Relay Response
- Relay Intro
- Peer Test

Před šifrováním záhlaví:

Před šifrováním hlavičky:

```

  +----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+

  Destination Connection ID :: 8 bytes, unsigned big endian integer

  Packet Number :: 4 bytes, unsigned big endian integer

  type :: The message type = 0, 1, 7, 9, 10, or 11

  ver :: The protocol version = 2, 3, or 4 for non-PQ, MLKEM512, MLKEM768

  id :: 1 byte, the network ID (currently 2, except for test networks)

  flag :: 1 byte, unused, set to 0 for future compatibility

  Source Connection ID :: 8 bytes, unsigned big endian integer

  Token :: 8 bytes, unsigned big endian integer

```
#### Krátká hlavička

unchanged

#### SessionRequest (Typ 0)

Změny: Aktuální SSU2 obsahuje v sekci ChaCha pouze data bloků. S ML-KEM bude sekce ChaCha obsahovat také zašifrovaný PQ veřejný klíč.

Změna KDF pro ochranu před spoofingem: Pro řešení problémů nastolených v Návrhu 165 [Prop165]_, avšak s odlišným řešením, upravujeme KDF pro Session Request. Tato změna se týká pouze PQ relací. KDF pro non-PQ relace zůstává nezměněn.

```

// End of KDF for initial chain key (unchanged)
  // Bob static key
  // MixHash(bpk)
  h = SHA256(h || bpk);

  // Start of KDF for session request
  // NEW for PQ only
  // bhash = Bob router hash (32 bytes)
  // MixHash(bhash)
  h = SHA256(h || bhash);

  // Rest of KDF for session request, unchanged, as in SSU2 spec
  // MixHash(header)
  h = SHA256(h || header)

  ...

```
Nezpracovaný obsah:

```
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 0-15, ChaCha20     |
  +  encrypted with Bob intro key         +
  |    See Header Encryption KDF          |
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 16-31, ChaCha20    |
  +  encrypted with Bob intro key n=0     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +       X, ChaCha20 encrypted           +
  |       with Bob intro key n=0          |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (MLKEM)     |
  +          (length varies)              +
  |  k defined in KDF for Session Request |
  +  n = 0                                +
  |  see KDF for associated data          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (payload)   |
  +          (length varies)              +
  |  k defined in KDF for Session Request |
  +  n = 1                                +
  |  see KDF for associated data          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
Nešifrovaná data (ověřovací značka Poly1305 není zobrazena):

```
  +----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                   X                   |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM encap_key            |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     Noise payload (block data)        |
  +          (length varies)              +
  |     see below for allowed blocks      |
  +----+----+----+----+----+----+----+----+
```
Velikosti, bez zahrnutí IP režie:

| Typ | Kód typu | Délka X | Délka Zpr. 1 | Délka Zpr. 1 šifr. | Délka Zpr. 1 dešifr. | Délka PQ klíče | Délka pl |
|------|-----------|-------|-----------|---------------|---------------|------------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 896+pl | 832+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1280+pl | 1216+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | n/a | příliš velké | | | | |
Poznámka: Kódy typů jsou určeny pouze pro interní použití. Routery zůstanou typu 4 a podpora bude uvedena v adresách routeru.

Minimální MTU pro MLKEM768_X25519: 1318 pro IPv4 a 1338 pro IPv6. Viz níže.

Změny: Současný SSU2 obsahuje užitečná data pouze v jedné sekci ChaCha. U ML-KEM bude před užitečnými daty nová sekce ChaCha obsahující zašifrovaný PQ šifrový text.

#### SessionCreated (Typ 1)

Změny: Aktuální SSU2 obsahuje uživatelská data pouze v jedné ChaCha sekci. U ML-KEM bude před uživatelskými daty přidána nová ChaCha sekce obsahující zašifrovaný PQ šifrový text.

Nezpracovaný obsah:

```
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 0-15, ChaCha20     |
  +  encrypted with Bob intro key and     +
  | derived key, see Header Encryption KDF|
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 16-31, ChaCha20    |
  +  encrypted with derived key n=0       +
  |  See Header Encryption KDF            |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +       Y, ChaCha20 encrypted           +
  |       with derived key n=0            |
  +              (32 bytes)               +
  |       See Header Encryption KDF       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 data (MLKEM)               |
  +   Encrypted and authenticated data    +
  |  length varies                        |
  +  k defined in KDF for Session Created +
  |  (before mixKey)                      |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 data (payload)             |
  +   Encrypted and authenticated data    +
  |  length varies                        |
  +  k defined in KDF for Session Created +
  |  (after mixKey)                       |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
Nezašifrovaná data (autentizační tag Poly1305 není zobrazen):

```
  +----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                  Y                    |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM Ciphertext           |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     Noise payload (block data)        |
  +          (length varies)              +
  |      see below for allowed blocks     |
  +----+----+----+----+----+----+----+----+
```
Velikosti, bez zahrnutí IP režie:

| Typ | Kód typu | Délka Y | Délka Msg 2 | Délka Msg 2 Enc | Délka Msg 2 Dec | Délka PQ CT | Délka pl |
|------|-----------|-------|-----------|---------------|---------------|-----------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 864+pl | 800+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1184+pl | 1120+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | n/a | příliš velké | | | | |
Poznámka: Kódy typů jsou určeny pouze pro interní použití. Routery zůstanou typu 4 a podpora bude uvedena v adresách routeru.

Minimální MTU pro MLKEM768_X25519: 1318 pro IPv4 a 1338 pro IPv6. Viz níže.

Maximální velikost: Alice zatím nemá Bobův RouterInfo a nezná jeho zveřejněnou MTU. Pro tuto zprávu použijte dočasnou MTU následovně. Pro MLKEM512_X25519 použijte maximum z hodnot 1280 nebo velikosti přijaté SessionRequest jako MTU. Pro MLKEM768_X25519 použijte maximum z hodnot (1318 pro IPv4 nebo 1338 pro IPv6) nebo velikosti přijaté SessionRequest jako MTU. Režie SessionCreated je menší než režie SessionRequest, protože MLKEM šifrovaný text je menší než MLKEM veřejný klíč. To umožňuje širší rozsah velikostí doplňování v SessionCreated, i když bylo v SessionRequest minimální nebo žádné doplňování.

#### SessionConfirmed (Typ 2)

unchanged

#### KDF pro datovou fázi

unchanged

#### Relay a Peer Test

Následující bloky obsahují pole verze. Zůstanou ve verzi 2 (kvůli kompatibilitě s non-PQ Bobem) a nebudou změněny na verzi 3/4 pro PQ.

* [CABFORUM](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/)
* [Choosing-Hash](https://kerkour.com/fast-secure-hash-function-sha256-sha512-sha3-blake3)
* [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/)
* [COMMON](/docs/specs/common-structures/)
* [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/)
* [ECIES](/docs/specs/ecies/)
* [FORUM](http://zzz.i2p/topics/3294)
* [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
* [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
* [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)
* [FIPS205](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.205.pdf)
* [MLDSA-OIDS](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/)
* [NIST-PQ](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards)
* [NIST-PQ-UPDATE](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf)
* [NIST-PQ-END](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf)
* [NIST-VECTORS](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values)
* [Noise](https://noiseprotocol.org/noise.html)
* [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf)
* [NSA-PQ](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF)
* [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)
* [Prop165](/docs/proposals/165/)
* [PQ-WIREGUARD](https://eprint.iacr.org/2020/379.pdf)
* [RFC-2104](https://tools.ietf.org/html/rfc2104)
* [Rosenpass](https://rosenpass.eu/)
* [Rosenpass-Whitepaper](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf)
* [SSH-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-sshm-mlkem-hybrid-kex/)
* [SSU2](/docs/specs/ssu2/)
* [TLS-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-tls-hybrid-design/)

#### Zveřejněné adresy

Ve všech případech používejte název transportu SSU2 jako obvykle. MLKEM-1024 není podporováno.

Použijte stejnou adresu/port jako pro non-PQ, nefirewallovanou variantu. Jedna nebo obě PQ varianty jsou podporovány. V adrese routeru publikujte v=2 (jako obvykle) a nový parametr pq=[3|4|3,4|4,3] označující MLKEM 512/768/obě. Routery s MTU menším než níže uvedené minimum nesmí publikovat parametr „pq" obsahující „4". Publikujte 4,3 pro vyjádření preference pro MLKEM-768 nebo 3,4 pro preferenci MLKEM-512. Skutečná verze závisí na iniciátorovi a preference nemusí být zohledněna. Routery s MTU menším než níže uvedené minimum nesmí navazovat spojení pomocí MLKEM768. Starší routery parametr pq ignorují a připojují se non-PQ způsobem jako obvykle.

Různá adresa/port oproti non-PQ, nebo pouze PQ, bez firewallu NENÍ podporováno. Toto nebude implementováno, dokud nebude non-PQ SSU2 zakázáno, což nastane za několik let. Jakmile bude non-PQ zakázáno, budou podporovány jedna nebo obě PQ varianty. V adrese routeru publikujte v=[3|4|3,4|4,3] pro označení MLKEM 512/768/obou. Starší routery zkontrolují parametr v a tuto adresu přeskočí jako nepodporovanou.

Adresy za firewallem (bez zveřejněné IP adresy): V adrese routeru zveřejněte v=2 (jako obvykle). Parametr pq MUSÍ být zveřejněn v adresách za firewallem, aby byla podporována funkce relay.

Alice se může připojit k PQ Bobovi pomocí PQ varianty, kterou Bob zveřejňuje, bez ohledu na to, zda Alice ve svém router info inzeruje podporu PQ, nebo zda inzeruje stejnou variantu.

#### MTU

Dbejte na to, abyste nepřekročili MTU při použití MLKEM768. Minimální MTU pro MLKEM768_X25519 je 1318 pro IPv4 a 1338 pro IPv6 (za předpokladu minimálního payloadu 10 bajtů s blokem DateTime a Padding nebo RelayTagRequest). Minimální MTU pro SSU2 obecně je 1280, takže ne všechny peers mohou používat MLKEM768. Nepublikujte ani nepoužívejte MLKEM768, pokud je skutečné MTU menší než minimum, ať už lokálně nebo jak je inzerováno peerem. Dbejte na to, aby velikost paddingu nezpůsobila, že zpráva 1 nebo 2 překročí lokální nebo vzdálené MTU.

## Analýza režijních nákladů

### Výměna klíčů

Nárůst velikosti (bajty):

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Pubkey (Msg 1)</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Ciphertext (Msg 2)</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+816</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+784</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+1200</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+1104</td>
</tr>
</table>
## Bezpečnostní analýza

Bezpečnostní kategorie NIST jsou shrnuty na snímku 10 v [prezentaci NIST](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf). Předběžná kritéria: Minimální bezpečnostní kategorie NIST by měla být 2 pro hybridní protokoly a 3 pro protokoly pouze s post-kvantovou kryptografií (PQ-only).

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Category</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">As Secure As</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES128</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">SHA256</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES192</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">SHA384</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES256</td>
</tr>
</table>
### Handshakes

Jedná se o hybridní protokoly. Implementace by měly upřednostňovat MLKEM768; MLKEM512 není dostatečně bezpečný.

Bezpečnostní kategorie NIST [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf):

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Algorithm</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Security Category</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
</tr>
</table>
## Poznámky k implementaci

### Podpora knihoven

Knihovny Bouncycastle, BoringSSL a WolfSSL nyní podporují MLKEM a MLDSA. Podpora OpenSSL bude zahrnuta v jejich vydání 3.5 dne 8. dubna 2025 [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

### Identifikace příchozího provozu

Pole verze v dlouhé hlavičce zprávy Session Request má hodnotu 2 pro nepost-kvantové, 3 pro MLKEM-512 a 4 pro MLKEM-768. To nám umožňuje spouštět standardní SSU2 i hybridní SSU2 na stejném portu a zároveň podporovat oba varianty MLKEM.

## Kompatibilita routeru

### Názvy transportů

Ve všech případech použijte název přenosu SSU2 jako obvykle. Starší směrovače budou parametr pq ignorovat a připojí se pomocí standardního SSU2 jako dosud.

## Reference

* [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/)
* [COMMON](/docs/specs/common-structures/)
* [ECIES](/docs/specs/ecies/)
* [FORUM](http://zzz.i2p/topics/3294)
* [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
* [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
* [NIST-PQ](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards)
* [NIST-PQ-UPDATE](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf)
* [NIST-PQ-END](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf)
* [NIST-VECTORS](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values)
* [Noise](https://noiseprotocol.org/noise.html)
* [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf)
* [NSA-PQ](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF)
* [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)
* [Prop165](/docs/proposals/165/)
* [PQ-WIREGUARD](https://eprint.iacr.org/2020/379.pdf)
* [RFC-2104](https://tools.ietf.org/html/rfc2104)
* [Rosenpass](https://rosenpass.eu/)
* [Rosenpass-Whitepaper](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf)
* [SSH-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-sshm-mlkem-hybrid-kex/)
* [SSU2](/docs/specs/ssu2/)
* [TLS-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-tls-hybrid-design/)
