---
title: "Specifikace šifrování ECIES-X25519-AEAD-Ratchet (ráčnování)"
description: "Integrované šifrovací schéma na eliptických křivkách pro I2P (X25519 + AEAD)"
slug: "ecies"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
toc: true
---

## Přehled

### Účel

ECIES-X25519-AEAD-Ratchet je moderní protokol pro end-to-end šifrování v I2P, který nahrazuje starší systém ElGamal/AES+SessionTags. Poskytuje dopředné utajení, autentizované šifrování a významná zlepšení výkonu i bezpečnosti.

### Hlavní vylepšení oproti ElGamal/AES+SessionTags

- **Menší klíče**: 32bajtové klíče vs 256bajtové veřejné klíče ElGamal (snížení o 87,5 %)
- **Dopředné utajení**: Dosahováno pomocí DH ratcheting (postupné obnovování klíčů) (není dostupné ve starším protokolu)
- **Moderní kryptografie**: X25519 DH, ChaCha20-Poly1305 AEAD (autentizované šifrování s přidruženými daty), SHA-256
- **Autentizované šifrování**: Vestavěná autentizace díky konstrukci AEAD
- **Obousměrný protokol**: Spárované příchozí/odchozí relace vs jednosměrný starší protokol
- **Efektivní značky**: 8bajtové značky relace vs 32bajtové značky (snížení o 75 %)
- **Zakrývání provozu**: Elligator2 kódování (technika maskování) činí handshaky (navazování spojení) nerozeznatelnými od náhodných dat

### Stav nasazení

- **První vydání**: Verze 0.9.46 (25. května 2020)
- **Nasazení v síti**: Dokončeno k roku 2020
- **Aktuální stav**: Vyzrálý, široce nasazený (v provozu 5+ let)
- **Podpora routeru**: Vyžadována verze 0.9.46 nebo vyšší
- **Požadavky na Floodfill**: Téměř 100% přijetí pro šifrované dotazy

### Stav implementace

**Plně implementováno:** - Zprávy typu New Session (NS) s vazbou - Zprávy typu New Session Reply (NSR) - Zprávy typu Existing Session (ES) - DH ratchet mechanism (ráčnový mechanismus DH) - Značka relace a ráčny symetrických klíčů - bloky DateTime, NextKey, ACK, ACK Request, Garlic Clove a Padding

**Není implementováno (k verzi 0.9.50):** - blok MessageNumbers (typ 6) - blok Options (typ 5) - blok Termination (typ 4) - automatické odpovědi na úrovni protokolu - režim Zero static key (režim bez statického klíče) - multicastové relace

**Poznámka**: Stav implementace pro verze 1.5.0 až 2.10.0 (2021–2025) vyžaduje ověření, protože některé funkce mohly být přidány.

---

## Základy protokolu

### Rámec protokolu Noise

ECIES-X25519-AEAD-Ratchet je založen na [Noise Protocol Framework](https://noiseprotocol.org/) (rámec protokolu Noise; revize 34, 2018-07-11), konkrétně na vzoru handshaku **IK** (interaktivní, se známým vzdáleným statickým klíčem) s rozšířeními specifickými pro I2P.

### Identifikátor protokolu Noise

```
Noise_IKelg2+hs2_25519_ChaChaPoly_SHA256
```
**Komponenty identifikátoru:** - `Noise` - Základní rámec - `IK` - Interaktivní vzor handshake se známým statickým klíčem protistrany - `elg2` - Kódování Elligator2 pro efemérní klíče (rozšíření I2P) - `+hs2` - MixHash volaný před druhou zprávou pro smíchání tagu (rozšíření I2P) - `25519` - Diffie–Hellmanova funkce X25519 - `ChaChaPoly` - AEAD (ověřené šifrování s přidruženými daty) šifra ChaCha20-Poly1305 - `SHA256` - Hashovací funkce SHA-256

### Vzor handshaku Noise

**Notace vzoru IK:**

```
<- s                    (Bob's static key known to Alice)
...
-> e, es, s, ss         (Alice sends ephemeral, DH es, static key, DH ss)
<- e, ee, se            (Bob sends ephemeral, DH ee, DH se)
```
**Význam tokenů:** - `e` - Přenos efemérního klíče - `s` - Přenos statického klíče - `es` - DH (Diffie-Hellman) mezi efemérním klíčem Alice a statickým klíčem Boba - `ss` - DH mezi statickým klíčem Alice a statickým klíčem Boba - `ee` - DH mezi efemérním klíčem Alice a efemérním klíčem Boba - `se` - DH mezi statickým klíčem Boba a efemérním klíčem Alice

### Bezpečnostní vlastnosti protokolu Noise

V terminologii Noise poskytuje vzor IK:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Message</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Authentication Level</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Confidentiality Level</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Message&nbsp;1 (NS)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;1 (sender auth, KCI vulnerable)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;2 (weak forward secrecy)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Message&nbsp;2 (NSR)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;2 (mutual auth)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;4 (weak forward secrecy)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Transport (ES)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;2 (mutual auth)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;5 (strong forward secrecy)</td>
    </tr>
  </tbody>
</table>
**Úrovně autentizace:** - **Úroveň 1**: Uživatelská data jsou ověřena jako náležející vlastníkovi statického klíče odesílatele, ale jsou zranitelná vůči Key Compromise Impersonation (KCI, vydávání se za jinou stranu po kompromitaci klíče) - **Úroveň 2**: Odolné vůči útokům KCI po NSR

**Úrovně důvěrnosti:** - **Úroveň 2**: Dopředná bezpečnost pokud je později kompromitován statický klíč odesílatele - **Úroveň 4**: Dopředná bezpečnost pokud je později kompromitován efemérní klíč odesílatele - **Úroveň 5**: Plná dopředná bezpečnost po smazání obou efemérních klíčů

### Rozdíly mezi IK a XK

Vzor IK se liší od vzoru XK používaného v NTCP2 a SSU2:

1. **Čtyři DH operace**: IK používá 4 DH operace (es, ss, ee, se) oproti 3 u XK
2. **Okamžitá autentizace**: Alice je autentizována v první zprávě (úroveň autentizace 1)
3. **Rychlejší dopředné utajení**: Plné dopředné utajení (úroveň 5) dosaženo po druhé zprávě (1-RTT)
4. **Kompromis**: Užitečná data první zprávy nejsou chráněna dopředným utajením (oproti XK, kde jsou všechna užitečná data chráněna dopředným utajením)

**Shrnutí**: IK umožňuje doručení Bobovy odpovědi v 1-RTT s plným dopředným utajením, za cenu toho, že počáteční požadavek není chráněn dopředným utajením.

### Koncepty Signal Double Ratchet (dvojitý západkový mechanismus)

ECIES (schéma integrovaného šifrování na eliptických křivkách) přebírá koncepty z [Signal Double Ratchet Algorithm](https://signal.org/docs/specifications/doubleratchet/):

- **DH Ratchet** (ráčnový mechanismus založený na DH): Zajišťuje dopředné utajení pravidelnou výměnou nových DH klíčů
- **Symmetric Key Ratchet** (ráčnový mechanismus pro symetrické klíče): Odvozuje nové klíče relace pro každou zprávu
- **Session Tag Ratchet** (ráčnový mechanismus pro značky relace): Deterministicky generuje session tags pro jednorázové použití

**Klíčové rozdíly oproti Signal:** - **Méně časté ratcheting (postupné obnovování klíčů)**: I2P provádí ratcheting pouze když je to potřeba (při blížícím se vyčerpání tagů nebo podle zásad) - **Session tags (značky relace) místo šifrování hlavičky**: Používá deterministické session tags namísto šifrovaných hlaviček - **Explicitní ACK (potvrzení přijetí)**: Používá in-band ACK bloky místo toho, aby se spoléhal výhradně na reverzní provoz - **Oddělené ratchety tagů a klíčů**: Efektivnější pro příjemce (může odložit výpočet klíče)

### Rozšíření I2P pro Noise

1. **Kódování Elligator2**: Efemérní klíče kódované tak, aby byly nerozeznatelné od náhodných dat
2. **Tag předřazený před NSR**: Session tag (identifikátor relace) přidán před zprávu NSR (Noise Session Request) pro korelaci
3. **Definovaný formát užitečných dat**: Bloková struktura užitečných dat pro všechny typy zpráv
4. **Zapouzdření I2NP**: Všechny zprávy jsou zapouzdřeny do záhlaví I2NP Garlic Message
5. **Oddělená datová fáze**: Transportní zprávy (ES) se odchylují od standardní datové fáze protokolu Noise

---

## Kryptografické primitivy

### Diffie-Hellman na křivce X25519

**Specifikace**: [RFC 7748](https://tools.ietf.org/html/rfc7748)

**Vlastnosti klíče:** - **Velikost soukromého klíče**: 32 bajtů - **Velikost veřejného klíče**: 32 bajtů - **Velikost sdíleného tajemství**: 32 bajtů - **Pořadí bajtů**: Little-endian - **Křivka**: Curve25519

**Provoz:**

### X25519 GENERATE_PRIVATE()

Vygeneruje náhodný soukromý klíč o délce 32 bajtů:

```
privkey = CSRNG(32)
```
### X25519 DERIVE_PUBLIC(privkey)

Odvodí odpovídající veřejný klíč:

```
pubkey = curve25519_scalarmult_base(privkey)
```
Vrací 32bajtový veřejný klíč v little-endian (pořadí bajtů s nejméně významným bajtem jako prvním).

### X25519 DH(privkey, pubkey)

Provádí Diffie-Hellmanovu dohodu o klíči:

```
sharedSecret = curve25519_scalarmult(privkey, pubkey)
```
Vrací 32bajtové sdílené tajemství.

**Bezpečnostní poznámka**: Implementátoři musí ověřit, že sdílené tajemství není tvořeno samými nulami (slabý klíč). V takovém případě odmítněte a ukončete handshake (navázání spojení).

### ChaCha20-Poly1305 AEAD (autentizované šifrování s přidruženými daty)

**Specifikace**: [RFC 7539](https://tools.ietf.org/html/rfc7539) sekce 2.8

**Parametry:** - **Velikost klíče**: 32 bajtů (256 bitů) - **Velikost nonce (jednorázová hodnota)**: 12 bajtů (96 bitů) - **Velikost MAC (ověřovací kód zprávy)**: 16 bajtů (128 bitů) - **Velikost bloku**: 64 bajtů (interní)

**Formát nonce (jednorázové číslo):**

```
Byte 0-3:   0x00 0x00 0x00 0x00  (always zero)
Byte 4-11:  Little-endian counter (message number N)
```
**Konstrukce AEAD:**

AEAD kombinuje proudovou šifru ChaCha20 s MAC Poly1305:

1. Vygenerujte klíčový proud ChaCha20 z klíče a nonce (jednorázového čísla)
2. Zašifrujte otevřený text operací XOR s klíčovým proudem
3. Spočítejte Poly1305 MAC nad (asociovaná data || šifrotext)
4. Připojte 16bajtový MAC k šifrotextu

### ChaCha20-Poly1305 ENCRYPT(k, n, plaintext, ad)

Šifruje otevřený text s autentizací:

```python
# Inputs
k = 32-byte cipher key
n = 12-byte nonce (first 4 bytes zero, last 8 bytes = message number)
plaintext = data to encrypt (0 to 65519 bytes)
ad = associated data (optional, used in MAC calculation)

# Output
ciphertext = chacha20_encrypt(k, n, plaintext)
mac = poly1305(ad || ciphertext, poly1305_key_gen(k, n))
return ciphertext || mac  # Total length = len(plaintext) + 16
```
**Vlastnosti:** - Šifrovaný text má stejnou délku jako otevřený text (proudová šifra) - Výstup je plaintext_length + 16 bajtů (zahrnuje MAC) - Celý výstup je nerozeznatelný od náhodných dat, pokud je klíč tajný - MAC autentizuje jak přidružená data, tak šifrovaný text

### ChaCha20-Poly1305 DECRYPT(k, n, ciphertext, ad)

Dešifruje a ověřuje autentizaci:

```python
# Split ciphertext and MAC
ct_without_mac = ciphertext[0:-16]
received_mac = ciphertext[-16:]

# Verify MAC
expected_mac = poly1305(ad || ct_without_mac, poly1305_key_gen(k, n))
if not constant_time_compare(received_mac, expected_mac):
    raise AuthenticationError("MAC verification failed")

# Decrypt
plaintext = chacha20_decrypt(k, n, ct_without_mac)
return plaintext
```
**Kritické bezpečnostní požadavky:** - Nonces (jednorázové hodnoty) MUSÍ být jedinečné pro každou zprávu se stejným klíčem - Nonces NESMÍ být znovu použity (katastrofální selhání v případě opětovného použití) - Ověření MAC MUSÍ používat porovnání v konstantním čase k zamezení časových útoků - Neúspěšné ověření MAC MUSÍ vést k úplnému odmítnutí zprávy (žádné částečné dešifrování)

### Hashovací funkce SHA-256

**Specifikace**: NIST FIPS 180-4

**Vlastnosti:** - **Velikost výstupu**: 32 bajtů (256 bitů) - **Velikost bloku**: 64 bajtů (512 bitů) - **Úroveň zabezpečení**: 128 bitů (odolnost proti kolizím)

**Provoz:**

### SHA-256 H(p, d)

Hash SHA-256 s personalizačním řetězcem:

```
H(p, d) := SHA256(p || d)
```
Kde `||` značí zřetězení, `p` je personalizační řetězec, `d` jsou data.

### SHA-256 MixHash(d)

Aktualizuje průběžně počítaný hash novými daty:

```
h = SHA256(h || d)
```
Používá se během Noise handshake (navázání spojení v Noise) k udržování hashe transkriptu.

### Derivace klíče pomocí HKDF

**Specifikace**: [RFC 5869](https://tools.ietf.org/html/rfc5869)

**Popis**: Funkce odvozování klíče založená na HMAC s použitím SHA-256

**Parametry:** - **Hašovací funkce**: HMAC-SHA256 - **Délka soli**: až 32 bajtů (velikost výstupu SHA-256) - **Délka výstupu**: proměnlivá (až 255 * 32 bajtů)

**Funkce HKDF (funkce pro odvozování klíčů na bázi HMAC):**

```python
def HKDF(salt, ikm, info, length):
    """
    Args:
        salt: Salt value (32 bytes max for SHA-256)
        ikm: Input key material (any length)
        info: Context-specific info string
        length: Desired output length in bytes
    
    Returns:
        output: Derived key material (length bytes)
    """
    # Extract phase
    prk = HMAC-SHA256(salt, ikm)
    
    # Expand phase
    n = ceil(length / 32)
    t = b''
    okm = b''
    for i in range(1, n + 1):
        t = HMAC-SHA256(prk, t || info || byte(i))
        okm = okm || t
    
    return okm[0:length]
```
**Běžné vzorce používání:**

```python
# Generate two keys (64 bytes total)
keydata = HKDF(chainKey, sharedSecret, "KDFDHRatchetStep", 64)
nextRootKey = keydata[0:31]
chainKey = keydata[32:63]

# Generate session tag (8 bytes)
tagdata = HKDF(chainKey, CONSTANT, "SessionTagKeyGen", 64)
nextChainKey = tagdata[0:31]
sessionTag = tagdata[32:39]

# Generate symmetric key (32 bytes)
keydata = HKDF(chainKey, ZEROLEN, "SymmetricRatchet", 64)
nextChainKey = keydata[0:31]
sessionKey = keydata[32:63]
```
**Informační řetězce používané v ECIES:** - `"KDFDHRatchetStep"` - Odvozování klíče v DH ratchet (ráčnový mechanismus) - `"TagAndKeyGenKeys"` - Inicializace klíčů pro řetězce tagů a klíčů - `"STInitialization"` - Inicializace ratchetu relačního tagu - `"SessionTagKeyGen"` - Generování relačního tagu - `"SymmetricRatchet"` - Generování symetrického klíče - `"XDHRatchetTagSet"` - Klíč sady tagů pro DH ratchet - `"SessionReplyTags"` - Generování sady tagů pro NSR - `"AttachPayloadKDF"` - Odvozování klíče pro užitečná data NSR

### Kódování Elligator2 (algoritmus pro mapování bodů na eliptické křivce na náhodně vypadající data)

**Účel**: Zakódovat veřejné klíče X25519 tak, aby byly nerozeznatelné od rovnoměrně náhodných 32bajtových řetězců.

**Specifikace**: [Článek Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf)

**Problém**: Standardní veřejné klíče X25519 mají rozpoznatelnou strukturu. Pozorovatel může identifikovat zprávy handshake (navázání spojení) detekcí těchto klíčů, i když je obsah šifrován.

**Řešení**: Elligator2 poskytuje bijektivní zobrazení mezi ~50 % platných veřejných klíčů X25519 a náhodně vypadajícími 254bitovými řetězci.

**Generování klíčů pomocí Elligator2 (kryptografická technika pro maskování veřejných klíčů):**

### Elligator2 GENERATE_PRIVATE_ELG2()

Vygeneruje soukromý klíč, který se mapuje na veřejný klíč, jenž lze zakódovat pomocí Elligator2 (algoritmus pro zakódování do uniformní podoby):

```python
while True:
    privkey = CSRNG(32)
    pubkey = DERIVE_PUBLIC(privkey)
    
    # Test if public key is Elligator2-encodable
    try:
        encoded = ENCODE_ELG2(pubkey)
        # Success - this key pair is suitable
        return privkey
    except NotEncodableError:
        # Try again with new random key
        continue
```
**Důležité**: Přibližně 50 % náhodně generovaných soukromých klíčů vytvoří veřejné klíče, které nelze zakódovat. Tyto je třeba zahodit a pokusit se o novou generaci.

**Optimalizace výkonu**: Generujte klíče předem ve vlákně na pozadí, abyste udržovali zásobu vhodných párů klíčů a předešli prodlevám při navazování spojení.

### Elligator2 ENCODE_ELG2(pubkey)

Zakóduje veřejný klíč do 32 náhodně vypadajících bajtů:

```python
def ENCODE_ELG2(pubkey):
    """
    Encodes X25519 public key using Elligator2.
    
    Args:
        pubkey: 32-byte X25519 public key (little-endian)
    
    Returns:
        encoded: 32-byte encoded key indistinguishable from random
    
    Raises:
        NotEncodableError: If pubkey cannot be encoded
    """
    # Perform Elligator2 representative calculation
    # Returns 254-bit value (31.75 bytes)
    encodedKey = elligator2_encode(pubkey)
    
    # Add 2 random bits to MSB to make full 32 bytes
    randomByte = CSRNG(1)
    encodedKey[31] |= (randomByte & 0xc0)
    
    return encodedKey
```
**Podrobnosti kódování:** - Elligator2 (metoda pro uniformní kódování veřejných klíčů) vytváří 254 bitů (ne plných 256) - Nejvyšší 2 bity bajtu 31 jsou náhodná výplň - Výsledek je rovnoměrně rozložen v 32bajtovém prostoru - Úspěšně kóduje přibližně 50 % platných veřejných klíčů X25519

### Elligator2 DECODE_ELG2(encodedKey)

Dekóduje se zpět na původní veřejný klíč:

```python
def DECODE_ELG2(encodedKey):
    """
    Decodes Elligator2-encoded key back to X25519 public key.
    
    Args:
        encodedKey: 32-byte encoded key
    
    Returns:
        pubkey: 32-byte X25519 public key (little-endian)
    """
    # Mask out 2 random padding bits from MSB
    encodedKey[31] &= 0x3f
    
    # Perform Elligator2 representative inversion
    pubkey = elligator2_decode(encodedKey)
    
    return pubkey
```
**Bezpečnostní vlastnosti:** - Kódované klíče jsou výpočetně nerozlišitelné od náhodných bajtů - Žádné statistické testy nedokážou spolehlivě detekovat klíče kódované metodou Elligator2 - Dekódování je deterministické (stejný kódovaný klíč vždy vede ke stejnému veřejnému klíči) - Kódování je bijektivní pro ~50 % klíčů v kódovatelné podmnožině

**Poznámky k implementaci:** - Uložte zakódované klíče už ve fázi generování, abyste se vyhnuli opětovnému kódování během navazování spojení - Nevhodné klíče z generování Elligator2 lze použít pro NTCP2 (který Elligator2 nevyžaduje) - Generování klíčů na pozadí je zásadní pro výkon - Průměrná doba generování se kvůli 50% míře vyřazení zdvojnásobuje

---

## Formáty zpráv

### Přehled

ECIES definuje tři typy zpráv:

1. **New Session (NS)**: Počáteční zpráva handshake (navázání spojení) od Alice Bobovi
2. **New Session Reply (NSR)**: Bobova odpověď v rámci handshake Alici
3. **Existing Session (ES)**: Všechny následující zprávy v obou směrech

Všechny zprávy jsou zapouzdřeny ve formátu I2NP Garlic Message (specifický formát zprávy v rámci I2NP) s dalšími vrstvami šifrování.

### I2NP kontejner zpráv typu Garlic

Všechny zprávy ECIES (schéma šifrování s eliptickými křivkami) jsou zapouzdřeny do standardních hlaviček I2NP Garlic Message:

```
+----+----+----+----+----+----+----+----+
|type|      msg_id       |  expiration   |
+----+----+----+----+----+----+----+----+
                         |  size   |chks|
+----+----+----+----+----+----+----+----+
|      length       |                   |
+----+----+----+----+                   +
|          encrypted data               |
~                                       ~
```
**Pole:** - `type`: 0x26 (Garlic Message – zpráva Garlic) - `msg_id`: 4bajtové ID zprávy I2NP - `expiration`: 8bajtové unixové časové razítko (milisekundy) - `size`: 2bajtová velikost užitečných dat - `chks`: 1bajtový kontrolní součet - `length`: 4bajtová délka šifrovaných dat - `encrypted data`: užitečná data šifrovaná pomocí ECIES

**Účel**: Poskytuje identifikaci zpráv a směrování na vrstvě I2NP. Pole `length` umožňuje příjemcům zjistit celkovou velikost šifrovaných užitečných dat.

### Zpráva nové relace (NS)

Zpráva New Session zahajuje novou relaci od Alice k Bobovi. Má tři varianty:

1. **S vazbou** (1b): Zahrnuje Aličin statický klíč pro obousměrnou komunikaci
2. **Bez vazby** (1c): Vynechává statický klíč pro jednosměrnou komunikaci
3. **Jednorázové** (1d): Režim jediné zprávy bez navazování relace

### Zpráva NS s vazbou (typ 1b)

**Případ použití**: streamování, datagramy umožňující odpověď, jakýkoli protokol, který vyžaduje odpověď

**Celková délka**: 96 + payload_length bajtů

**Formát**:

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
+         Static Key Section            +
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
~          Variable length              ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
```
**Podrobnosti pole:**

**Efemérní veřejný klíč** (32 bajtů, v otevřeném textu): - Jednorázový veřejný klíč X25519 Alice - Kódován pomocí Elligator2 (nerozlišitelný od náhodných dat) - Pro každou NS zprávu generován nově (nikdy se nepoužije znovu) - Formát little-endian

**Sekce statického klíče** (32 bajtů šifrovaných, 48 bajtů včetně MAC): - Obsahuje statický veřejný klíč X25519 Alice (32 bajtů) - Šifrováno pomocí ChaCha20 - Autentizováno pomocí Poly1305 MAC (16 bajtů) - Použito Bobem ke svázání relace s destinací Alice

**Sekce datové části** (šifrovaná s proměnnou délkou, +16 bajtů MAC): - Obsahuje garlic cloves (části zprávy v rámci garlic encryption) a další bloky - Musí obsahovat blok DateTime jako první blok - Obvykle obsahuje bloky Garlic Clove s aplikačními daty - Může obsahovat blok NextKey pro okamžitý ratchet (krok posunu klíčů) - Šifrováno pomocí ChaCha20 - Autentizováno pomocí Poly1305 MAC (16 bajtů)

**Bezpečnostní vlastnosti:** - Efemérní klíč zajišťuje dopředné utajení - Statický klíč autentizuje Alici (svazuje s cílem) - Obě části mají samostatné MAC pro oddělení domén - Celé navázání spojení provádí 2 operace DH (es, ss)

### Zpráva NS bez vazby (typ 1c)

**Případ použití**: Surové datagramy, kde se odpověď neočekává ani není žádoucí

**Celková délka**: 96 + payload_length bajtů

**Formát**:

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
|           All zeros                   |
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
~          Variable length              ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
```
**Klíčový rozdíl**: sekce Flags obsahuje 32 nulových bajtů místo statického klíče.

**Detekce**: Bob určí typ zprávy dešifrováním 32bajtové sekce a ověřením, zda jsou všechny bajty nulové: - Všechny nuly → nevázaná relace (typ 1c) - Nenulové → vázaná relace se statickým klíčem (typ 1b)

**Vlastnosti:** - Žádný statický klíč znamená, že není vazba na Aličin cíl - Bob nemůže posílat odpovědi (není znám žádný cíl) - Provádí pouze 1 DH operaci - Řídí se vzorem Noise "N" spíše než "IK" - Efektivnější, když odpovědi nejsou nikdy potřeba

**Flags Section** (vyhrazeno pro budoucí použití): Aktuálně samé nuly. V budoucích verzích může sloužit k vyjednávání funkcí.

### NS Jednorázová zpráva (Typ 1d)

**Případ použití**: Jediná anonymní zpráva bez relace a bez očekávané odpovědi

**Celková délka**: 96 + payload_length bajtů

**Formát**: Shodný s NS bez vazby (typ 1c)

**Rozdíl**:  - Typ 1c může v rámci stejné relace odeslat více zpráv (následují ES messages) - Typ 1d odešle přesně jednu zprávu bez navázání relace - V praxi s nimi mohou implementace zpočátku zacházet totožně

**Vlastnosti:** - Maximální anonymita (žádný statický klíč, žádná relace) - Žádná ze stran neuchovává stav relace - Řídí se vzorcem Noise "N" - Jediná operace DH (es)

### Zpráva New Session Reply (NSR)

Bob odešle jednu nebo více zpráv NSR (typ protokolové zprávy) v reakci na zprávu NS (typ protokolové zprávy) od Alice. NSR dokončuje Noise IK handshake (navázání spojení pomocí schématu Noise IK) a zřizuje obousměrnou relaci.

**Celková délka**: 72 + payload_length bajtů

**Formát**:

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
+  (MAC) for Key Section (empty)        +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~          Variable length              ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
```
**Podrobnosti pole:**

**Značka relace** (8 bajtů, v otevřeném textu): - Generováno z NSR tagsetu (množina značek) (viz sekce KDF) - Propojuje tuto odpověď se zprávou NS od Alice - Umožňuje Alici identifikovat, na které NS tato NSR odpovídá - Jednorázové použití (nikdy se znovu nepoužije)

**Efemérní veřejný klíč** (32 bajtů, v otevřené podobě): - Bobův jednorázový veřejný klíč X25519 - Zakódovaný pomocí Elligator2 - Generován znovu pro každou zprávu NSR - Musí být odlišný pro každý odeslaný NSR

**MAC sekce klíče** (16 bajtů): - Autentizuje prázdná data (ZEROLEN) - Součást protokolu Noise IK (vzor se) - Používá hash přepisu jako přidružená data - Zásadní pro svázání NSR s NS

**Sekce užitečných dat** (proměnlivé délky): - Obsahuje garlic cloves (stroužky v rámci garlic encryption) a bloky - Obvykle zahrnuje odpovědi aplikační vrstvy - Může být prázdná (ACK-only NSR, tj. pouze potvrzení v NSR) - Maximální velikost: 65519 bajtů (65535 - 16bajtový MAC)

**Více zpráv NSR:**

Bob může v odpovědi na jeden NS odeslat více zpráv NSR: - Každá zpráva NSR má jedinečný efemérní klíč - Každá zpráva NSR má jedinečnou značku relace - Alice použije první přijatou zprávu NSR k dokončení navázání spojení (handshake) - Ostatní zprávy NSR slouží jako redundance (pro případ ztráty paketů)

**Kritické načasování:** - Alice musí obdržet jeden NSR před odesláním ES zpráv - Bob musí obdržet jednu ES zprávu před odesláním ES zpráv - NSR odvozuje obousměrné klíče relace pomocí operace split()

**Bezpečnostní vlastnosti:** - Dokončuje Noise IK handshake (schéma navázání spojení IK v rámci frameworku Noise) - Provádí 2 další operace DH (ee, se) - Celkem 4 operace DH napříč NS+NSR - Dosahuje vzájemného ověření (úroveň 2) - Poskytuje slabé dopředné utajení (úroveň 4) pro payload NSR

### Zpráva pro existující relaci (ES)

Všechny zprávy po handshake NS/NSR používají formát Existing Session (formát existující relace). Zprávy ES se používají obousměrně jak Alicí, tak Bobem.

**Celková délka**: 8 + payload_length + 16 bajtů (minimálně 24 bajtů)

**Formát**:

```
+----+----+----+----+----+----+----+----+
|       Session Tag   8 bytes           |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~          Variable length              ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+              (MAC)                    +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
```
**Podrobnosti pole:**

**Značka relace** (8 bajtů, v otevřené podobě): - Vygenerována z aktuální odchozí sady značek - Identifikuje relaci a číslo zprávy - Příjemce vyhledá značku, aby našel klíč relace a nonce (jednorázové číslo) - Jednorázové použití (každá značka je použita právě jednou) - Formát: Prvních 8 bajtů výstupu HKDF

**Sekce užitečných dat** (proměnlivé délky): - Obsahuje garlic cloves (části zprávy v rámci garlic encryption) a bloky - Nejsou žádné povinné bloky (může být prázdná) - Běžné bloky: Garlic Clove, NextKey, ACK, ACK Request, Padding - Maximální velikost: 65519 bajtů (65535 - 16 bajtů MAC)

**MAC** (16 bajtů): - Autentizační tag Poly1305 - Spočítán nad celou užitečnou zátěží - Asociovaná data: 8bajtový session tag (značka relace) - Musí být ověřen správně, jinak je zpráva odmítnuta

**Proces vyhledávání tagů:**

1. Příjemce extrahuje 8bajtový tag
2. Vyhledá tag ve všech aktuálních příchozích tagsetech (množinách tagů)
3. Načte přiřazený session key (relační klíč) a číslo zprávy N
4. Sestaví nonce: `[0x00, 0x00, 0x00, 0x00, N (8 bytes little-endian)]`
5. Dešifruje payload pomocí AEAD s tagem jako přidruženými daty
6. Odstraní tag z tagsetu (jednorázové použití)
7. Zpracuje dešifrované bloky

**Značka relace nenalezena:**

Pokud se tag (kryptografický identifikátor) nenajde v žádném tagsetu (množině tagů): - Může jít o zprávu NS → zkuste dešifrování NS - Může jít o zprávu NSR → zkuste dešifrování NSR - Může jít o ES doručené mimo pořadí → krátce vyčkejte na aktualizaci tagsetu - Může jít o útok opakovaným přehráním → odmítněte - Může jít o poškozená data → odmítněte

**Prázdná užitečná data:**

Zprávy ES mohou mít prázdná užitečná data (0 bajtů): - Slouží jako explicitní ACK, když byl přijat ACK Request - Poskytuje odpověď na úrovni protokolu bez aplikačních dat - Přesto spotřebuje session tag (značka relace) - Užitečné, když vyšší vrstva nemá okamžitě co odeslat

**Bezpečnostní vlastnosti:** - Plné dopředné utajení (úroveň 5) po přijetí NSR - Autentizované šifrování pomocí AEAD - Tag (značka) slouží jako dodatečná asociovaná data - Maximálně 65535 zpráv na jeden tagset (sadu značek) než je vyžadován ratchet (mechanismus postupné výměny klíčů)

---

## Funkce pro odvozování klíčů

Tato část dokumentuje všechny operace KDF (funkce odvození klíče) používané v ECIES (integrované šifrovací schéma na eliptických křivkách) a ukazuje úplná kryptografická odvození.

### Notace a konstanty

**Konstanty:** - `ZEROLEN` - Bajtové pole nulové délky (prázdný řetězec) - `||` - Operátor konkatenace

**Proměnné:** - `h` - Průběžný hash přepisu (32 bajtů) - `chainKey` - Řetězící klíč pro HKDF (32 bajtů) - `k` - Klíč symetrické šifry (32 bajtů) - `n` - Nonce (jednorázová hodnota) / číslo zprávy

**Klíče:** - `ask` / `apk` - statický soukromý/veřejný klíč Alice - `aesk` / `aepk` - efemérní soukromý/veřejný klíč Alice - `bsk` / `bpk` - statický soukromý/veřejný klíč Boba - `besk` / `bepk` - efemérní soukromý/veřejný klíč Boba

### Funkce odvození klíče (KDF) pro zprávy NS

### KDF 1: Počáteční řetězový klíč

Provedeno jednou při inicializaci protokolu (lze předpočítat):

```python
# Protocol name (40 bytes, ASCII, no null termination)
protocol_name = "Noise_IKelg2+hs2_25519_ChaChaPoly_SHA256"

# Initialize hash
h = SHA256(protocol_name)

# Initialize chaining key
chainKey = h

# MixHash with empty prologue
h = SHA256(h)

# State: chainKey and h initialized
# Can be precalculated for all outbound sessions
```
**Výsledek:** - `chainKey` = Počáteční řetězící klíč pro všechny následující KDF (funkce odvození klíče) - `h` = Počáteční hash transkriptu

### KDF 2: Směšování Bobova statického klíče

Bob to provede jednou (lze předpočítat pro všechny příchozí relace):

```python
# Bob's static keys (published in LeaseSet)
bsk = GENERATE_PRIVATE()
bpk = DERIVE_PUBLIC(bsk)

# Mix Bob's public key into hash
h = SHA256(h || bpk)

# State: h updated with Bob's identity
# Can be precalculated by Bob for all inbound sessions
```
### KDF 3: Generování Aličina efemérního klíče

Alice generuje nové klíče pro každou zprávu NS:

```python
# Generate ephemeral key pair suitable for Elligator2
aesk = GENERATE_PRIVATE_ELG2()
aepk = DERIVE_PUBLIC(aesk)

# Mix ephemeral public key into hash
h = SHA256(h || aepk)

# Elligator2 encode for transmission
elg2_aepk = ENCODE_ELG2(aepk)

# State: h updated with Alice's ephemeral key
# Send elg2_aepk as first 32 bytes of NS message
```
### KDF (funkce pro odvozování klíčů) 4: NS sekce statického klíče (es DH)

Odvozuje klíče pro šifrování Aličina statického klíče:

```python
# Perform first DH (ephemeral-static)
sharedSecret = DH(aesk, bpk)  # Alice computes
# Equivalent: sharedSecret = DH(bsk, aepk)  # Bob computes

# Derive cipher key from shared secret
keydata = HKDF(chainKey, sharedSecret, "", 64)
chainKey = keydata[0:31]
k = keydata[32:63]

# AEAD encryption parameters
nonce = 0
associated_data = h  # Current hash transcript

# Encrypt static key section
if binding_requested:
    plaintext = apk  # Alice's static public key (32 bytes)
else:
    plaintext = bytes(32)  # All zeros for unbound

ciphertext = ENCRYPT(k, nonce, plaintext, associated_data)
# ciphertext = 32 bytes encrypted + 16 bytes MAC = 48 bytes

# Mix ciphertext into hash
h = SHA256(h || ciphertext)

# State: Static key section encrypted, h updated
# Send ciphertext (48 bytes) as next part of NS message
```
### KDF 5: Sekce užitečných dat NS (ss DH, pouze vázané)

Pro vázané relace proveďte druhou výměnu DH (Diffie‑Hellmanova výměna klíčů) pro šifrování užitečných dat:

```python
if binding_requested:
    # Alice's static keys
    ask = GENERATE_PRIVATE()  # Alice's long-term key
    apk = DERIVE_PUBLIC(ask)
    
    # Perform second DH (static-static)
    sharedSecret = DH(ask, bpk)  # Alice computes
    # Equivalent: sharedSecret = DH(bsk, apk)  # Bob computes
    
    # Derive cipher key
    keydata = HKDF(chainKey, sharedSecret, "", 64)
    chainKey = keydata[0:31]
    k = keydata[32:63]
    
    nonce = 0
    associated_data = h
else:
    # Unbound: reuse keys from static key section
    # chainKey and k unchanged
    nonce = 1  # Increment nonce (reusing same key)
    associated_data = h

# Encrypt payload
payload = build_payload()  # DateTime + Garlic Cloves + etc.
ciphertext = ENCRYPT(k, nonce, payload, associated_data)

# Mix ciphertext into hash
h = SHA256(h || ciphertext)

# State: Payload encrypted, h contains complete NS transcript
# Save chainKey and h for NSR processing
# Send ciphertext as final part of NS message
```
**Důležité poznámky:**

1. **Vázané vs Nevázané**: 
   - Vázané provádí 2 operace DH (es + ss)
   - Nevázané provádí 1 operaci DH (jen es)
   - Nevázané inkrementuje nonce (jednorázová hodnota) místo odvození nového klíče

2. **Bezpečnost proti znovupoužití klíče**:
   - Různé nonces (jednorázové hodnoty) (0 vs 1) zabraňují znovupoužití klíče/nonce
   - Odlišná přidružená data (h se liší) zajišťují oddělení domén

3. **Hash transkript**:
   - `h` nyní obsahuje: protocol_name, prázdný prolog, bpk, aepk, static_key_ciphertext, payload_ciphertext
   - Tento transkript provazuje všechny části zprávy NS dohromady

### KDF sady odpovědních tagů NSR

Bob generuje tagy pro zprávy NSR:

```python
# Chain key from NS payload section
# chainKey = final chainKey from NS KDF

# Generate tagset key
tagsetKey = HKDF(chainKey, ZEROLEN, "SessionReplyTags", 32)

# Initialize NSR tagset (see DH_INITIALIZE below)
tagset_nsr = DH_INITIALIZE(chainKey, tagsetKey)

# Get tag for this NSR
tagsetEntry = tagset_nsr.GET_NEXT_ENTRY()
tag = tagsetEntry.SESSION_TAG  # 8 bytes

# State: tag available for NSR message
# Send tag as first 8 bytes of NSR
```
### Funkce odvození klíčů pro zprávy NSR

### KDF 6: Generování efemérního klíče NSR

Bob generuje nový efemérní klíč pro každý NSR:

```python
# Mix tag into hash (I2P extension to Noise)
h = SHA256(h || tag)

# Generate ephemeral key pair
besk = GENERATE_PRIVATE_ELG2()
bepk = DERIVE_PUBLIC(besk)

# Mix ephemeral public key into hash
h = SHA256(h || bepk)

# Elligator2 encode for transmission
elg2_bepk = ENCODE_ELG2(bepk)

# State: h updated with tag and Bob's ephemeral key
# Send elg2_bepk as bytes 9-40 of NSR message
```
### KDF 7: Sekce klíče NSR (ee a se DH)

Odvozuje klíče pro sekci klíčů NSR:

```python
# Perform third DH (ephemeral-ephemeral)
sharedSecret_ee = DH(aesk, bepk)  # Alice computes
# Equivalent: sharedSecret_ee = DH(besk, aepk)  # Bob computes

# Mix ee into chain
keydata = HKDF(chainKey, sharedSecret_ee, "", 32)
chainKey = keydata[0:31]

# Perform fourth DH (static-ephemeral)
sharedSecret_se = DH(ask, bepk)  # Alice computes
# Equivalent: sharedSecret_se = DH(besk, apk)  # Bob computes

# Derive cipher key from se
keydata = HKDF(chainKey, sharedSecret_se, "", 64)
chainKey = keydata[0:31]
k = keydata[32:63]

# AEAD encryption of empty data (key section has no payload)
nonce = 0
associated_data = h
ciphertext = ENCRYPT(k, nonce, ZEROLEN, associated_data)
# ciphertext = 16 bytes (MAC only, no plaintext)

# Mix ciphertext into hash
h = SHA256(h || ciphertext)

# State: Key section encrypted, chainKey contains all 4 DH results
# Send ciphertext (16 bytes MAC) as bytes 41-56 of NSR
```
**Kritické**: Tím je dokončen handshake protokolu Noise IK. `chainKey` nyní obsahuje příspěvky ze všech čtyř operací DH (Diffie–Hellman) (es, ss, ee, se).

### KDF (funkce odvození klíče) 8: Sekce užitečných dat NSR

Odvozuje klíče pro šifrování datové části NSR:

```python
# Split chainKey into bidirectional keys
keydata = HKDF(chainKey, ZEROLEN, "", 64)
k_ab = keydata[0:31]   # Alice → Bob key
k_ba = keydata[32:63]  # Bob → Alice key

# Initialize ES tagsets for both directions
tagset_ab = DH_INITIALIZE(chainKey, k_ab)  # Alice → Bob
tagset_ba = DH_INITIALIZE(chainKey, k_ba)  # Bob → Alice

# Derive NSR payload key (Bob → Alice)
k_nsr = HKDF(k_ba, ZEROLEN, "AttachPayloadKDF", 32)

# Encrypt NSR payload
nonce = 0
associated_data = h  # Binds payload to entire NSR
payload = build_payload()  # Usually application reply
ciphertext = ENCRYPT(k_nsr, nonce, payload, associated_data)

# State: Bidirectional ES sessions established
# tagset_ab and tagset_ba ready for ES messages
# Send ciphertext as bytes 57+ of NSR message
```
**Důležité poznámky:**

1. **Split Operation** (operace rozdělení):
   - Vytváří nezávislé klíče pro každý směr
   - Zabraňuje znovupoužití klíčů mezi Alice→Bob a Bob→Alice

2. **Vazba payloadu NSR**:
   - Používá `h` jako přidružená data k svázání payloadu s handshake
   - Samostatná KDF (funkce pro odvozování klíčů) ("AttachPayloadKDF") zajišťuje oddělení domén

3. **Připravenost ES**:
   - Po NSR mohou obě strany posílat zprávy ES
   - Alice musí před odesláním ES obdržet NSR
   - Bob musí před odesláním ES obdržet ES

### KDF (funkce odvození klíče) pro zprávy ES

Zprávy ES používají předem vygenerované relační klíče z tagsetů:

```python
# Sender gets next tag and key
tagsetEntry = outbound_tagset.GET_NEXT_ENTRY()
tag = tagsetEntry.SESSION_TAG     # 8 bytes
k = tagsetEntry.SESSION_KEY       # 32 bytes
N = tagsetEntry.INDEX             # Message number

# Construct nonce (12 bytes)
nonce = [0x00, 0x00, 0x00, 0x00] + little_endian_8_bytes(N)

# AEAD encryption
associated_data = tag  # Tag is associated data
payload = build_payload()
ciphertext = ENCRYPT(k, nonce, payload, associated_data)

# Send: tag || ciphertext (8 + len(ciphertext) bytes)
```
**Proces příjemce:**

```python
# Extract tag
tag = message[0:8]

# Look up tag in inbound tagsets
tagsetEntry = inbound_tagset.GET_SESSION_KEY(tag)
if tagsetEntry is None:
    # Not an ES message, try NS/NSR decryption
    return try_handshake_decryption(message)

k = tagsetEntry.SESSION_KEY
N = tagsetEntry.INDEX

# Construct nonce
nonce = [0x00, 0x00, 0x00, 0x00] + little_endian_8_bytes(N)

# AEAD decryption
associated_data = tag
ciphertext = message[8:]
try:
    payload = DECRYPT(k, nonce, ciphertext, associated_data)
except AuthenticationError:
    # MAC verification failed, reject message
    return reject_message()

# Process payload blocks
process_payload(payload)

# Remove tag from tagset (one-time use)
inbound_tagset.remove(tag)
```
### Funkce DH_INITIALIZE

Vytvoří sadu tagů pro jeden směr:

```python
def DH_INITIALIZE(rootKey, k):
    """
    Initializes a tagset with session tag and symmetric key ratchets.
    
    Args:
        rootKey: Chain key from previous DH ratchet (32 bytes)
        k: Key material from split() or DH ratchet (32 bytes)
    
    Returns:
        tagset: Initialized tagset object
    """
    # Derive next root key and chain key
    keydata = HKDF(rootKey, k, "KDFDHRatchetStep", 64)
    nextRootKey = keydata[0:31]
    chainKey_tagset = keydata[32:63]
    
    # Derive separate chain keys for tags and keys
    keydata = HKDF(chainKey_tagset, ZEROLEN, "TagAndKeyGenKeys", 64)
    sessTag_ck = keydata[0:31]   # Session tag chain key
    symmKey_ck = keydata[32:63]  # Symmetric key chain key
    
    # Create tagset object
    tagset = Tagset()
    tagset.nextRootKey = nextRootKey
    tagset.sessTag_chainKey = sessTag_ck
    tagset.symmKey_chainKey = symmKey_ck
    tagset.lastIndex = -1
    
    return tagset
```
**Kontexty použití:**

1. **NSR Tagset** (množina tagů): `DH_INITIALIZE(chainKey_from_NS, tagsetKey_NSR)`
2. **ES Tagsets**: `DH_INITIALIZE(chainKey_from_NSR, k_ab or k_ba)`
3. **Ratchetované Tagsets**: `DH_INITIALIZE(nextRootKey_from_previous, tagsetKey_from_DH)`

---

## Ráčnové mechanismy

ECIES používá tři synchronizované ratchet mechanisms (ráčnové mechanismy) k zajištění dopředného utajení a efektivní správy relací.

### Přehled ratchetu

**Tři typy ratchet (kryptografický ráčnový mechanismus):**

1. **DH Ratchet (ráčnový mechanismus)**: Provádí výměny klíčů Diffie–Hellman za účelem generování nových kořenových klíčů
2. **Session Tag Ratchet**: Deterministicky odvozuje jednorázové značky relace
3. **Symmetric Key Ratchet**: Odvozuje relační klíče pro šifrování zpráv

**Vztah:**

```
DH Ratchet (periodic)
    ↓
Creates new tagset
    ↓
Session Tag Ratchet (per message) ← synchronized → Symmetric Key Ratchet (per message)
    ↓                                                      ↓
Session Tags (8 bytes each)                      Session Keys (32 bytes each)
```
**Klíčové vlastnosti:**

- **Odesílatel**: Generuje tagy a klíče podle potřeby (není potřeba nic ukládat)
- **Příjemce**: Předgeneruje tagy pro look-ahead window (okno dopředu) (vyžaduje ukládání)
- **Synchronizace**: Index tagu určuje index klíče (N_tag = N_key)
- **Dopředné utajení**: Dosahuje se prostřednictvím periodického DH ratchet (postupné periodické překlápění klíčů Diffie-Hellman)
- **Efektivita**: Příjemce může odložit výpočet klíče, dokud neobdrží tag

### DH Ratchet (mechanismus průběžné obnovy klíčů pomocí Diffie–Hellman)

DH ratchet (mechanismus postupné obnovy klíčů Diffie‑Hellman) poskytuje dopředné utajení pravidelnou výměnou nových efemérních klíčů.

### Frekvence DH Ratchet (krokového mechanismu DH)

**Požadované podmínky pro ratchet (kryptografický krokovací mechanismus):** - Sada tagů se blíží vyčerpání (maximum je tag 65535) - Zásady specifické pro implementaci:   - Prahová hodnota počtu zpráv (např. každých 4096 zpráv)   - Časová prahová hodnota (např. každých 10 minut)   - Prahová hodnota objemu dat (např. každých 100 MB)

**Doporučený First Ratchet** (počáteční krok kryptografického mechanismu ratchet): Kolem čísla tagu 4096, aby se zabránilo dosažení limitu

**Maximální hodnoty:** - **Maximální ID sady tagů**: 65535 - **Maximální ID klíče**: 32767 - **Maximální počet zpráv na sadu tagů**: 65535 - **Teoretické maximální množství dat na relaci**: ~6,9 TB (64K sad tagů × 64K zpráv × 1730 bajtů průměrně)

### ID tagů a klíčů pro DH Ratchet (ráčnový mechanismus DH)

**Počáteční sada tagů** (po handshake (navázání spojení)): - ID sady tagů: 0 - Zatím nebyly odeslány žádné bloky NextKey - Nebyla přiřazena žádná ID klíčů

**Po prvním ratchetu (kryptografický mechanismus pro postupnou výměnu klíčů)**: - ID sady tagů: 1 = (1 + ID klíče Alice + ID klíče Boba) = (1 + 0 + 0) - Alice posílá zprávu NextKey s ID klíče 0 - Bob odpovídá zprávou NextKey s ID klíče 0

**Následující sady tagů**: - ID sady tagů = 1 + ID klíče odesílatele + ID klíče příjemce - Příklad: sada tagů 5 = (1 + sender_key_2 + receiver_key_2)

**Tabulka vývoje sady tagů:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Tag Set ID</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Sender Key ID</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Receiver Key ID</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">n/a</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">n/a</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Initial tag set (post-NSR)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">First ratchet (both generate new keys)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Sender generates new key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Receiver generates new key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Sender generates new key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Receiver generates new key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">...</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">...</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">...</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Pattern repeats</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">65534</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32767 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32766</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Second-to-last tag set</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">65535</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32767</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32767 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Final tag set</td>
    </tr>
  </tbody>
</table>
\* = Nový klíč vygenerovaný v tomto ratchetu (mechanismus postupné výměny klíčů)

**Pravidla pro ID klíče:** - ID jsou sekvenční a začínají od 0 - ID se zvyšují pouze při vytvoření nového klíče - Maximální ID klíče je 32767 (15 bitů) - Po ID klíče 32767 je vyžadována nová relace

### Tok zpráv DH Ratchet (mechanismus postupného odvozování klíčů)

**Role:** - **Odesílatel tagů**: Vlastní odchozí sadu tagů, odesílá zprávy - **Příjemce tagů**: Vlastní příchozí sadu tagů, přijímá zprávy

**Vzor:** Odesílatel tagů zahájí ratchet (mechanismus postupné obnovy klíčů), když je sada tagů téměř vyčerpána.

**Diagram toku zpráv:**

```
Tag Sender                         Tag Receiver

       ... using tag set #0 ...

(Tag set #0 approaching exhaustion)
(Generate new key #0)

NextKey forward, request reverse, with key #0  -------->
(Repeat until NextKey ACK received)
                                   (Generate new key #0)
                                   (Perform DH: sender_key_0 × receiver_key_0)
                                   (Create inbound tag set #1)

        <---------------           NextKey reverse, with key #0
                                   (Repeat until tag from tag set #1 received)

(Receive NextKey with key #0)
(Perform DH: sender_key_0 × receiver_key_0)
(Create outbound tag set #1)


       ... using tag set #1 ...


(Tag set #1 approaching exhaustion)
(Generate new key #1)

NextKey forward, with key #1        -------->
(Repeat until NextKey ACK received)
                                   (Reuse existing key #0)
                                   (Perform DH: sender_key_1 × receiver_key_0)
                                   (Create inbound tag set #2)

        <--------------            NextKey reverse, id 0 (ACK)
                                   (Repeat until tag from tag set #2 received)

(Receive NextKey with id 0)
(Perform DH: sender_key_1 × receiver_key_0)
(Create outbound tag set #2)


       ... using tag set #2 ...


(Tag set #2 approaching exhaustion)
(Reuse existing key #1)

NextKey forward, request reverse, id 1  -------->
(Repeat until NextKey received)
                                   (Generate new key #1)
                                   (Perform DH: sender_key_1 × receiver_key_1)
                                   (Create inbound tag set #3)

        <--------------            NextKey reverse, with key #1

(Receive NextKey with key #1)
(Perform DH: sender_key_1 × receiver_key_1)
(Create outbound tag set #3)


       ... using tag set #3 ...

       (Pattern repeats: even-numbered tag sets
        use forward key, odd-numbered use reverse key)
```
**Vzory pro Ratchet (ráčnový mechanismus):**

**Vytváření sudě číslovaných sad tagů** (2, 4, 6, ...): 1. Odesílatel vygeneruje nový klíč 2. Odesílatel pošle NextKey block s novým klíčem 3. Příjemce pošle NextKey block s ID starého klíče (ACK) 4. Oba provedou DH s (novým klíčem odesílatele × starým klíčem příjemce)

**Vytváření lichě číslovaných sad tagů** (3, 5, 7, ...): 1. Odesílatel požádá o reverzní klíč (pošle NextKey s příznakem žádosti) 2. Příjemce vygeneruje nový klíč 3. Příjemce pošle blok NextKey s novým klíčem 4. Oba provedou DH (Diffie–Hellman) s (starý klíč odesílatele × nový klíč příjemce)

### Formát bloku NextKey

Viz sekci Payload Format pro podrobnou specifikaci bloku NextKey.

**Klíčové prvky:** - **Bajt příznaků**:   - Bit 0: Klíč přítomen (1) nebo pouze ID (0)   - Bit 1: Reverzní klíč (1) nebo dopředný klíč (0)   - Bit 2: Požadavek na reverzní klíč (1) nebo bez požadavku (0) - **ID klíče**: 2 bajty, big-endian (0-32767) - **Veřejný klíč**: 32 bajtů X25519 (pokud bit 0 = 1)

**Ukázkové NextKey Blocks (bloky NextKey):**

```python
# Sender initiates ratchet with new key (key ID 0, tag set 1)
NextKey(flags=0x01, key_id=0, pubkey=sender_key_0)

# Receiver replies with new key (key ID 0, tag set 1)
NextKey(flags=0x03, key_id=0, pubkey=receiver_key_0)

# Sender ratchets again with new key (key ID 1, tag set 2)
NextKey(flags=0x01, key_id=1, pubkey=sender_key_1)

# Receiver ACKs with old key ID (tag set 2)
NextKey(flags=0x02, key_id=0)

# Sender requests reverse key (tag set 3)
NextKey(flags=0x04, key_id=1)

# Receiver sends new reverse key (key ID 1, tag set 3)
NextKey(flags=0x03, key_id=1, pubkey=receiver_key_1)
```
### KDF pro DH ratchet (funkce odvozování klíče pro ráčnový mechanizmus Diffie–Hellmana)

Když dojde k výměně nových klíčů:

```python
# Tag sender generates or reuses key
if generating_new:
    sender_sk = GENERATE_PRIVATE()
    sender_pk = DERIVE_PUBLIC(sender_sk)
else:
    # Reuse existing key pair
    sender_pk = existing_sender_pk

# Tag receiver generates or reuses key
if generating_new:
    receiver_sk = GENERATE_PRIVATE()
    receiver_pk = DERIVE_PUBLIC(receiver_sk)
else:
    # Reuse existing key pair
    receiver_pk = existing_receiver_pk

# Both parties perform DH
sharedSecret = DH(sender_sk, receiver_pk)

# Derive tagset key
tagsetKey = HKDF(sharedSecret, ZEROLEN, "XDHRatchetTagSet", 32)

# Get next root key from previous tagset
rootKey = previous_tagset.nextRootKey

# Initialize new tagset
new_tagset = DH_INITIALIZE(rootKey, tagsetKey)

# Tag sender: outbound tagset
# Tag receiver: inbound tagset
```
**Kritické načasování:**

**Odesílatel tagů:** - Okamžitě vytvoří novou odchozí sadu tagů - Okamžitě začne používat nové tagy - Odstraní starou odchozí sadu tagů

**Příjemce tagů:** - Vytváří novou příchozí sadu tagů - Ponechá starou příchozí sadu tagů po dobu přechodné lhůty (3 minuty) - Během přechodné lhůty přijímá tagy z obou sad, staré i nové - Po uplynutí přechodné lhůty smaže starou příchozí sadu tagů

### Správa stavu DH Ratchet (mechanismus postupné obnovy klíčů pomocí Diffie‑Hellman)

**Stav odesílatele:** - Aktuální odchozí sada tagů - ID sady tagů a ID klíčů - Další kořenový klíč (pro další ratchet, ráčnový mechanismus) - Počet zpráv v aktuální sadě tagů

**Stav příjemce:** - Aktuální množiny příchozích tagů (během ochranné lhůty mohou být dvě) - Čísla předchozích zpráv (PN) pro detekci mezer - Dopředné okno předem vygenerovaných tagů - Další kořenový klíč (pro další ratchet, mechanismus postupného odvozování klíčů)

**Pravidla přechodů stavů:**

1. **Před prvním Ratchet (mechanismus postupného obnovování klíčů)**:
   - Použití sady tagů 0 (z NSR)
   - Nejsou přiřazena žádná ID klíčů

2. **Zahájení Ratchet (kryptografického ráčnového mechanismu)**:
   - Vygenerujte nový klíč (pokud v tomto kole generuje odesílatel)
   - Odešlete blok NextKey v ES message
   - Před vytvořením novou sadu odchozích tagů vyčkejte na odpověď NextKey

3. **Přijetí požadavku Ratchet (mechanismus postupné obnovy klíčů)**:
   - Vygenerujte nový klíč (pokud v tomto kole generuje klíč příjemce)
   - Proveďte DH s přijatým klíčem
   - Vytvořte novou sadu příchozích značek
   - Odešlete odpověď NextKey
   - Ponechte starou sadu příchozích značek po dobu odkladu

4. **Dokončení ratchetu (ráčnového mechanismu)**:
   - Přijmout odpověď NextKey
   - Provést DH
   - Vytvořit novou sadu odchozích tagů
   - Začít používat nové tagy

### Rohatkový mechanismus značek relace

Mechanismus session tag ratchet (kryptografický mechanismus pro štítky relace) deterministicky generuje jednorázové 8bajtové session tags.

### Účel Session Tag Ratchet (mechanismus postupné změny tagů relace)

- Nahrazuje explicitní přenos tagů (ElGamal posílal 32bajtové tagy)
- Umožňuje příjemci předgenerovat tagy pro okno dopředného náhledu
- Odesílatel je generuje na vyžádání (není třeba je ukládat)
- Synchronizuje se se symmetric key ratchet (schéma postupného odvozování klíčů se symetrickým klíčem) prostřednictvím indexu

### Vzorec ráčnového mechanismu značky relace

**Inicializace:**

```python
# From DH_INITIALIZE
sessTag_ck = initial_chain_key  # 32 bytes

# Initialize session tag ratchet
keydata = HKDF(sessTag_ck, ZEROLEN, "STInitialization", 64)
sessTag_chainKey = keydata[0:31]    # First chain key
SESSTAG_CONSTANT = keydata[32:63]   # Constant for all tags in this tagset
```
**Generování značky (pro značku N):**

```python
# Generate tag N
keydata = HKDF(sessTag_chainKey_(N-1), SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
sessTag_chainKey_N = keydata[0:31]  # Chain key for next tag
tag_N = keydata[32:39]              # Session tag (8 bytes)

# Chain continues for each tag
# tag_0, tag_1, tag_2, ..., tag_65535
```
**Kompletní sekvence:**

```python
# Tag 0
keydata_0 = HKDF(sessTag_chainKey, SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
sessTag_chainKey_0 = keydata_0[0:31]
tag_0 = keydata_0[32:39]

# Tag 1
keydata_1 = HKDF(sessTag_chainKey_0, SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
sessTag_chainKey_1 = keydata_1[0:31]
tag_1 = keydata_1[32:39]

# Tag N
keydata_N = HKDF(sessTag_chainKey_(N-1), SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
sessTag_chainKey_N = keydata_N[0:31]
tag_N = keydata_N[32:39]
```
### Implementace odesílatele pro ráčnový mechanismus Session Tag

```python
class OutboundTagset:
    def __init__(self, sessTag_ck):
        # Initialize
        keydata = HKDF(sessTag_ck, ZEROLEN, "STInitialization", 64)
        self.chainKey = keydata[0:31]
        self.constant = keydata[32:63]
        self.index = -1
    
    def get_next_tag(self):
        # Increment index
        self.index += 1
        
        if self.index > 65535:
            raise TagsetExhausted("Ratchet required")
        
        # Generate tag
        keydata = HKDF(self.chainKey, self.constant, "SessionTagKeyGen", 64)
        self.chainKey = keydata[0:31]
        tag = keydata[32:39]
        
        return (tag, self.index)
```
**Proces odesílatele:** 1. Zavolejte `get_next_tag()` pro každou zprávu 2. Použijte vrácený tag (značka) v ES message (zpráva ES) 3. Uložte index N pro případné sledování ACK (potvrzení přijetí) 4. Není vyžadováno ukládání tagů (generují se podle potřeby)

### Implementace příjemce Session Tag Ratchet (ráčnový mechanismus pro značky relace)

```python
class InboundTagset:
    def __init__(self, sessTag_ck, look_ahead=32):
        # Initialize
        keydata = HKDF(sessTag_ck, ZEROLEN, "STInitialization", 64)
        self.chainKey = keydata[0:31]
        self.constant = keydata[32:63]
        self.index = -1
        self.look_ahead = look_ahead
        self.tags = {}  # Dictionary: tag -> index
        
        # Pre-generate initial tags
        self.extend(look_ahead)
    
    def extend(self, count):
        """Generate 'count' more tags"""
        for _ in range(count):
            self.index += 1
            
            if self.index > 65535:
                return  # Cannot exceed maximum
            
            # Generate tag
            keydata = HKDF(self.chainKey, self.constant, "SessionTagKeyGen", 64)
            self.chainKey = keydata[0:31]
            tag = keydata[32:39]
            
            # Store tag
            self.tags[tag] = self.index
    
    def lookup_tag(self, tag):
        """Look up tag and return index"""
        if tag in self.tags:
            index = self.tags[tag]
            # Remove tag (one-time use)
            del self.tags[tag]
            return index
        return None
    
    def check_and_extend(self):
        """Extend if tag count is low"""
        current_count = len(self.tags)
        if current_count < self.look_ahead // 2:
            # Extend to restore window
            self.extend(self.look_ahead - current_count)
```
**Proces příjemce:** 1. Předem vygenerujte tagy pro look-ahead window (dopředné okno) (např. 32 tagů) 2. Uložte tagy do hashovací tabulky nebo slovníku 3. Když dorazí zpráva, vyhledejte tag a získejte index N 4. Odstraňte tag z úložiště (jednorázové použití) 5. Rozšiřte okno, pokud počet tagů klesne pod prahovou hodnotu

### Strategie předzásobení Session Tag (značka relace)

**Účel**: Najít rovnováhu mezi využitím paměti a zpracováním zpráv mimo pořadí

**Doporučené velikosti Look-Ahead (dopředný náhled):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Tagset Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Initial Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Maximum Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR tagset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Short-lived</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ES tagset 0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">24</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">160</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Initial ES tagset</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ES tagset 1+</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">160</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">160</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Ratcheted tagsets</td>
    </tr>
  </tbody>
</table>
**Adaptivní Look-Ahead (dopředný náhled):**

```python
# Dynamic look-ahead based on highest tag received
look_ahead = min(tsmax, tsmin + N // 4)

# Example:
# tsmin = 24, tsmax = 160
# N = 0:   look_ahead = min(160, 24 + 0/4) = 24
# N = 100: look_ahead = min(160, 24 + 100/4) = 49
# N = 500: look_ahead = min(160, 24 + 500/4) = 149
# N = 544: look_ahead = min(160, 24 + 544/4) = 160
```
**Ořezat vzadu:**

```python
# Trim tags far behind highest received
trim_behind = look_ahead // 2

# If highest received tag is N=100, trim tags below N=50
```
**Výpočet paměti:**

```python
# Per tag: 8 bytes (tag) + 2 bytes (index) + overhead ≈ 16 bytes
# Look-ahead of 160 tags ≈ 2.5 KB per inbound tagset

# With multiple sessions:
# 100 inbound sessions × 2.5 KB = 250 KB total
```
### Zpracování Session Tag (značky relace) mimo pořadí

**Scénář**: Zprávy přicházejí mimo pořadí

```
Expected: tag_5, tag_6, tag_7, tag_8
Received: tag_5, tag_7, tag_6, tag_8
```
**Chování příjemce:**

1. Přijmout tag_5:
   - Vyhledat: nalezeno na indexu 5
   - Zpracovat zprávu
   - Odstranit tag_5
   - Nejvyšší přijaté: 5

2. Přijmout tag_7 (mimo pořadí):
   - Vyhledat: nalezeno na indexu 7
   - Zpracovat zprávu
   - Odstranit tag_7
   - Nejvyšší dosud přijaté: 7
   - Poznámka: tag_6 je stále v úložišti (dosud nepřijatý)

3. Přijmout tag_6 (zpožděno):
   - Vyhledat: nalezeno na indexu 6
   - Zpracovat zprávu
   - Odstranit tag_6
   - Nejvyšší přijaté: 7 (beze změny)

4. Přijmout tag_8:
   - Vyhledat: nalezen na indexu 8
   - Zpracovat zprávu
   - Odstranit tag_8
   - Nejvyšší přijaté: 8

**Správa okna:** - Sledovat nejvyšší přijatý index - Udržovat seznam chybějících indexů (mezery) - Rozšiřovat okno podle nejvyššího indexu - Volitelné: Po vypršení časového limitu odstranit staré mezery

### Symmetric Key Ratchet (symetrická ráčna)

Symmetric key ratchet (mechanismus postupné obnovy klíčů) generuje 32bajtové šifrovací klíče synchronizované s tagy relace.

### Účel Symmetric Key Ratchet (mechanismus postupné obměny symetrických klíčů)

- Poskytuje jedinečný šifrovací klíč pro každou zprávu
- Synchronizováno se session tag ratchet (krokovací mechanismus; stejný index)
- Odesílatel může generovat podle potřeby
- Příjemce může odložit generování, dokud neobdrží tag

### Vzorec pro Symmetric Key Ratchet (ráčnový mechanismus pro postupné odvozování symetrických klíčů)

**Inicializace:**

```python
# From DH_INITIALIZE
symmKey_ck = initial_chain_key  # 32 bytes

# No additional initialization needed
# Unlike session tag ratchet, no constant is derived
```
**Generování klíče (pro klíč N):**

```python
# Generate key N
SYMMKEY_CONSTANT = ZEROLEN  # Empty string
keydata = HKDF(symmKey_chainKey_(N-1), SYMMKEY_CONSTANT, "SymmetricRatchet", 64)
symmKey_chainKey_N = keydata[0:31]  # Chain key for next key
key_N = keydata[32:63]              # Session key (32 bytes)
```
**Kompletní sekvence:**

```python
# Key 0
keydata_0 = HKDF(symmKey_ck, ZEROLEN, "SymmetricRatchet", 64)
symmKey_chainKey_0 = keydata_0[0:31]
key_0 = keydata_0[32:63]

# Key 1
keydata_1 = HKDF(symmKey_chainKey_0, ZEROLEN, "SymmetricRatchet", 64)
symmKey_chainKey_1 = keydata_1[0:31]
key_1 = keydata_1[32:63]

# Key N
keydata_N = HKDF(symmKey_chainKey_(N-1), ZEROLEN, "SymmetricRatchet", 64)
symmKey_chainKey_N = keydata_N[0:31]
key_N = keydata_N[32:63]
```
### Implementace odesílatele pro Symmetric Key Ratchet (symetrický ráčnový mechanismus)

```python
class OutboundKeyRatchet:
    def __init__(self, symmKey_ck):
        self.chainKey = symmKey_ck
        self.index = -1
    
    def get_key(self, index):
        """Generate key for specific index"""
        # Fast-forward to desired index if needed
        while self.index < index:
            self.index += 1
            keydata = HKDF(self.chainKey, ZEROLEN, "SymmetricRatchet", 64)
            self.chainKey = keydata[0:31]
            if self.index == index:
                return keydata[32:63]
        
        # Should not reach here if called correctly
        raise ValueError("Key already generated")
```
**Proces odesílatele:** 1. Získat další značku a její index N 2. Vygenerovat klíč pro index N 3. Použít klíč k zašifrování zprávy 4. Není vyžadováno žádné ukládání klíče

### Implementace příjemce pro Symmetric Key Ratchet (ráčna se symetrickým klíčem)

**Strategie 1: Odložené generování (doporučeno)**

```python
class InboundKeyRatchet:
    def __init__(self, symmKey_ck):
        self.chainKey = symmKey_ck
        self.index = -1
        self.cache = {}  # Optional: cache recently used keys
    
    def get_key(self, index):
        """Generate key for specific index"""
        # Check cache first (optional optimization)
        if index in self.cache:
            key = self.cache[index]
            del self.cache[index]
            return key
        
        # Fast-forward to desired index
        while self.index < index:
            self.index += 1
            keydata = HKDF(self.chainKey, ZEROLEN, "SymmetricRatchet", 64)
            self.chainKey = keydata[0:31]
            
            if self.index == index:
                return keydata[32:63]
        
        raise ValueError("Index already passed")
```
**Proces odložené generace:** 1. Přijmout ES zprávu se značkou 2. Vyhledat značku a získat index N 3. Vygenerovat klíče 0 až N (pokud již nebyly vygenerovány) 4. Použít klíč N k dešifrování zprávy 5. Řetězový klíč je nyní umístěn na indexu N

**Výhody:** - Minimální využití paměti - Klíče se generují pouze když jsou potřeba - Jednoduchá implementace

**Nevýhody:** - Při prvním použití je nutné vygenerovat všechny klíče od 0 do N - Nemůže zpracovat zprávy mimo pořadí bez ukládání do mezipaměti

**Strategie 2: Předgenerování s Tag Window (okno značek) (Alternativa)**

```python
class InboundKeyRatchet:
    def __init__(self, symmKey_ck):
        self.chainKey = symmKey_ck
        self.index = -1
        self.keys = {}  # Dictionary: index -> key
    
    def extend(self, count):
        """Pre-generate 'count' more keys"""
        for _ in range(count):
            self.index += 1
            keydata = HKDF(self.chainKey, ZEROLEN, "SymmetricRatchet", 64)
            self.chainKey = keydata[0:31]
            key = keydata[32:63]
            self.keys[self.index] = key
    
    def get_key(self, index):
        """Retrieve pre-generated key"""
        if index in self.keys:
            key = self.keys[index]
            del self.keys[index]
            return key
        return None
```
**Proces předgenerování:** 1. Předgenerujte klíče odpovídající oknu značek (např. 32 klíčů) 2. Uložte klíče indexované podle čísla zprávy 3. Po přijetí značky vyhledejte odpovídající klíč 4. Rozšiřujte okno, jak se značky používají

**Výhody:** - Přirozeně zvládá zprávy doručené mimo pořadí - Rychlé získání klíče (bez zpoždění způsobeného generováním)

**Nevýhody:** - Vyšší spotřeba paměti (32 bajtů na klíč vs 8 bajtů na tag) - Je nutné udržovat klíče synchronizované s tagy

**Porovnání paměti:**

```python
# Look-ahead of 160:
# Tags only:  160 × 16 bytes = 2.5 KB
# Tags+Keys:  160 × (16 + 32) bytes = 7.5 KB
# 
# For 100 sessions:
# Tags only:  250 KB
# Tags+Keys:  750 KB
```
### Synchronizace Symmetric Ratchet (symetrické ráčnování) pomocí Session Tags (značky relace)

**Kritický požadavek**: Index značky relace MUSÍ být roven indexu symetrického klíče

```python
# Sender
tag, index = outbound_tagset.get_next_tag()
key = outbound_keyratchet.get_key(index)  # Same index
nonce = construct_nonce(index)
ciphertext = ENCRYPT(key, nonce, payload, tag)

# Receiver
index = inbound_tagset.lookup_tag(tag)
key = inbound_keyratchet.get_key(index)  # Same index
nonce = construct_nonce(index)
plaintext = DECRYPT(key, nonce, ciphertext, tag)
```
**Režimy selhání:**

Pokud se synchronizace přeruší: - Pro dešifrování použit nesprávný klíč - Ověření MAC selže - Zpráva odmítnuta

**Prevence:** - Vždy používejte stejný index pro značku a klíč - Nikdy nevynechávejte indexy v žádném ratchet (kryptografický mechanismus postupného posunu) - Zpracovávejte zprávy doručené mimo pořadí opatrně

### Konstrukce nonce pro symetrický ratchet (mechanismus postupného odvozování klíčů)

Nonce (jednorázová hodnota) je odvozena z pořadového čísla zprávy:

```python
def construct_nonce(index):
    """
    Construct 12-byte nonce for ChaCha20-Poly1305
    
    Args:
        index: Message number (0-65535)
    
    Returns:
        nonce: 12-byte nonce
    """
    # First 4 bytes are always zero
    nonce = bytearray(12)
    nonce[0:4] = b'\x00\x00\x00\x00'
    
    # Last 8 bytes are little-endian message number
    nonce[4:12] = index.to_bytes(8, byteorder='little')
    
    return bytes(nonce)
```
**Příklady:**

```python
index = 0:     nonce = 0x00000000 0000000000000000
index = 1:     nonce = 0x00000000 0100000000000000
index = 255:   nonce = 0x00000000 FF00000000000000
index = 256:   nonce = 0x00000000 0001000000000000
index = 65535: nonce = 0x00000000 FFFF000000000000
```
**Důležité vlastnosti:** - Nonce (jednorázová náhodná hodnota) jsou jedinečné pro každou zprávu v tagsetu (množina tagů) - Nonce se nikdy neopakují (one-time-use tagy to zajišťují) - 8bajtový čítač umožňuje 2^64 zpráv (my používáme jen 2^16) - Formát nonce odpovídá konstrukci založené na čítači podle RFC 7539

---

## Správa relací

### Kontext relace

Všechny příchozí a odchozí relace musí patřit do konkrétního kontextu:

1. **Kontext routeru**: Relace pro samotný router
2. **Kontext destinace**: Relace pro konkrétní místní destinaci (klientská aplikace)

**Kritické pravidlo**: Relace se NESMÍ sdílet napříč kontexty, aby se zabránilo korelačním útokům.

**Implementace:**

```python
class SessionKeyManager:
    """Context for managing sessions (router or destination)"""
    def __init__(self, context_id):
        self.context_id = context_id
        self.inbound_sessions = {}   # far_end_dest -> [sessions]
        self.outbound_sessions = {}  # far_end_dest -> session
        self.static_keypair = generate_keypair()  # Context's identity
    
    def get_outbound_session(self, destination):
        """Get or create outbound session to destination"""
        if destination not in self.outbound_sessions:
            self.outbound_sessions[destination] = create_outbound_session(destination)
        return self.outbound_sessions[destination]
    
    def add_inbound_session(self, session, destination=None):
        """Add inbound session, optionally bound to destination"""
        if destination:
            if destination not in self.inbound_sessions:
                self.inbound_sessions[destination] = []
            self.inbound_sessions[destination].append(session)
        else:
            # Unbound session
            self.inbound_sessions[None].append(session)
```
**Implementace I2P v Javě:**

V Java I2P třída `SessionKeyManager` poskytuje tuto funkcionalitu: - Jeden `SessionKeyManager` pro každý router - Jeden `SessionKeyManager` pro každou lokální destinaci - Oddělená správa relací ECIES a ElGamal v rámci každého kontextu

### Vazba relace

**Vazba** spojuje relaci s konkrétním cílem na vzdálené straně.

### Vázané relace

**Vlastnosti:** - Zahrnuje statický klíč odesílatele ve zprávě NS - Příjemce může identifikovat destinaci odesílatele - Umožňuje obousměrnou komunikaci - Jedna odchozí relace pro každou destinaci - Může mít více příchozích relací (během přechodů)

**Případy použití:** - Streamová spojení (podobná TCP) - Datagramy s možností odpovědi - Jakýkoli protokol vyžadující režim požadavek/odpověď

**Proces vázání:**

```python
# Alice creates bound outbound session
outbound_session = OutboundSession(
    destination=bob_destination,
    static_key=alice_static_key,
    bound=True
)

# Alice sends NS with static key
ns_message = build_ns_message(
    ephemeral_key=alice_ephemeral_key,
    static_key=alice_static_key,  # Included for binding
    payload=data
)

# Bob receives NS
bob_receives_ns(ns_message)
# Bob extracts Alice's static key
alice_static_key = decrypt_static_key_section(ns_message)

# Bob looks up Alice's destination (from bundled LeaseSet)
alice_destination = lookup_destination_by_static_key(alice_static_key)

# Bob creates bound inbound session
inbound_session = InboundSession(
    destination=alice_destination,
    bound=True
)

# Bob pairs with outbound session
outbound_session = OutboundSession(
    destination=alice_destination,
    bound=True
)
```
**Výhody:** 1. **Ephemeral-Ephemeral DH** (dočasný-dočasný Diffie-Hellman): Odpověď používá ee DH (plná dopředná důvěrnost) 2. **Kontinuita relace**: Ratchets (mechanismus postupného klíčování) udržují vazbu na stejnou destination (cílová identita v I2P) 3. **Zabezpečení**: Zabraňuje únosu relace (autentizace statickým klíčem) 4. **Efektivita**: Jedna relace na destination (bez duplikace)

### Nevázané relace

**Vlastnosti:** - V NS message (zpráva typu NS) není žádný statický klíč (sekce příznaků obsahuje samé nuly) - Příjemce nemůže identifikovat odesílatele - Pouze jednosměrná komunikace - Je povoleno více relací ke stejnému cíli

**Případy použití:** - Surové datagramy (odešli a zapomeň) - Anonymní publikování - Zasílání zpráv ve stylu broadcastu

**Vlastnosti:** - Anonymnější (bez identifikace odesílatele) - Efektivnější (1 DH vs 2 DH při navázání spojení) - Odpovědi nejsou možné (příjemce neví, kam odpovědět) - Žádné session ratcheting (postupné obměňování klíčů) (jednorázové nebo omezené použití)

### Párování relací

**Spárování** propojuje příchozí relaci s odchozí relací pro obousměrnou komunikaci.

### Vytváření spárovaných relací

**Pohled Alice (iniciátor):**

```python
# Create outbound session to Bob
outbound_session = create_outbound_session(bob_destination)

# Create paired inbound session
inbound_session = create_inbound_session(
    paired_with=outbound_session,
    bound_to=bob_destination
)

# Link them
outbound_session.paired_inbound = inbound_session
inbound_session.paired_outbound = outbound_session

# Send NS message
send_ns_message(outbound_session, payload)
```
**Bobova perspektiva (respondent):**

```python
# Receive NS message
ns_message = receive_ns_message()

# Create inbound session
inbound_session = create_inbound_session_from_ns(ns_message)

# If NS contains static key (bound):
if ns_message.has_static_key():
    alice_destination = extract_destination(ns_message)
    inbound_session.bind_to(alice_destination)
    
    # Create paired outbound session
    outbound_session = create_outbound_session(alice_destination)
    
    # Link them
    outbound_session.paired_inbound = inbound_session
    inbound_session.paired_outbound = outbound_session

# Send NSR
send_nsr_message(inbound_session, outbound_session, payload)
```
### Výhody párování relací

1. **In-band ACKs**: Mohou potvrzovat zprávy bez samostatného clove (části zprávy v garlic encryption)
2. **Efektivní ratcheting (kryptografický mechanismus postupného posunu klíčů)**: Oba směry se posouvají společně
3. **Řízení toku**: Lze implementovat zpětný tlak napříč párovanými relacemi
4. **Konzistence stavu**: Snazší udržovat synchronizovaný stav

### Pravidla spárování relací

- Odchozí relace může být nespárovaná (unbound NS)
- Příchozí relace pro bound NS by měla být spárovaná
- Párování probíhá při vytváření relace, ne až poté
- Spárované relace mají stejnou vazbu na destinaci
- Ratchets (kryptografický ráčnový mechanismus) probíhají nezávisle, ale jsou koordinované

### Životní cyklus relace

### Životní cyklus relace: fáze vytvoření

**Navázání odchozí relace (Alice):**

```python
def create_outbound_session(destination, bound=True):
    session = OutboundSession()
    session.destination = destination
    session.bound = bound
    session.state = SessionState.NEW
    session.created_time = now()
    
    # Generate keys for NS message
    session.ephemeral_keypair = generate_elg2_keypair()
    if bound:
        session.static_key = context.static_keypair.public_key
    
    # Will be populated after NSR received
    session.outbound_tagset = None
    session.inbound_tagset = None
    
    return session
```
**Vytváření příchozí relace (Bob):**

```python
def create_inbound_session_from_ns(ns_message):
    session = InboundSession()
    session.state = SessionState.ESTABLISHED
    session.created_time = now()
    
    # Extract from NS
    session.remote_ephemeral_key = ns_message.ephemeral_key
    session.remote_static_key = ns_message.static_key
    
    if session.remote_static_key:
        session.bound = True
        session.destination = lookup_destination(session.remote_static_key)
    else:
        session.bound = False
        session.destination = None
    
    # Generate keys for NSR
    session.ephemeral_keypair = generate_elg2_keypair()
    
    # Create tagsets from KDF
    session.inbound_tagset = create_tagset_from_nsr()
    session.outbound_tagset = create_tagset_from_nsr()
    
    return session
```
### Životní cyklus relace: Aktivní fáze

**Přechody stavů:**

```
NEW (outbound only)
  ↓
  NS sent
  ↓
PENDING_REPLY (outbound only)
  ↓
  NSR received
  ↓
ESTABLISHED
  ↓
  ES messages exchanged
  ↓
ESTABLISHED (ongoing)
  ↓
  (optional) RATCHETING
  ↓
ESTABLISHED
```
**Údržba aktivní relace:**

```python
def maintain_active_session(session):
    # Update last activity time
    session.last_activity = now()
    
    # Check for ratchet needed
    if session.outbound_tagset.needs_ratchet():
        initiate_ratchet(session)
    
    # Check for incoming ratchet
    if received_nextkey_block():
        process_ratchet(session)
    
    # Trim old tags from inbound tagset
    session.inbound_tagset.expire_old_tags()
    
    # Check session health
    if session.idle_time() > SESSION_TIMEOUT:
        mark_session_idle(session)
```
### Životní cyklus relace: fáze vypršení platnosti

**Hodnoty časového limitu relace:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Session Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Sender Timeout</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Receiver Timeout</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR tagset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">N/A</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Short-lived</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ES tagset 0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Initial</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ES tagset 1+</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Ratcheted</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Old tagset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">N/A</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">After ratchet</td>
    </tr>
  </tbody>
</table>
**Logika vypršení platnosti:**

```python
def check_session_expiration():
    for session in active_sessions:
        # Outbound session expiration (sender)
        if session.is_outbound():
            if session.idle_time() > 8 * 60:  # 8 minutes
                expire_outbound_session(session)
        
        # Inbound session expiration (receiver)
        else:
            if session.idle_time() > 10 * 60:  # 10 minutes
                expire_inbound_session(session)
    
    # Old tagsets (after ratchet)
    for tagset in old_tagsets:
        if tagset.age() > 3 * 60:  # 3 minutes
            delete_tagset(tagset)
```
**Kritické pravidlo**: Odchozí relace MUSÍ vypršet dříve než příchozí relace, aby se zabránilo desynchronizaci.

**Korektní ukončení:**

```python
def terminate_session(session, reason=0):
    # Send Termination block (if implemented)
    send_termination_block(session, reason)
    
    # Mark session for deletion
    session.state = SessionState.TERMINATED
    
    # Keep session briefly for final messages
    schedule_deletion(session, delay=30)  # 30 seconds
    
    # Notify paired session
    if session.paired_session:
        session.paired_session.mark_remote_terminated()
```
### Více NS zpráv

**Scénář**: Ztratí se zpráva NS od Alice nebo se ztratí odpověď NSR.

**Chování Alice:**

```python
class OutboundSession:
    def __init__(self):
        self.ns_messages_sent = []
        self.ns_timer = None
        self.max_ns_attempts = 5
    
    def send_ns_message(self, payload):
        # Generate new ephemeral key for each NS
        ephemeral_key = generate_elg2_keypair()
        
        ns_message = build_ns_message(
            ephemeral_key=ephemeral_key,
            static_key=self.static_key,
            payload=payload
        )
        
        # Store state for this NS
        ns_state = {
            'ephemeral_key': ephemeral_key,
            'chainkey': compute_chainkey(ns_message),
            'hash': compute_hash(ns_message),
            'tagset': derive_nsr_tagset(ns_message),
            'sent_time': now()
        }
        self.ns_messages_sent.append(ns_state)
        
        # Send message
        send_message(ns_message)
        
        # Set timer for retry
        if not self.ns_timer:
            self.ns_timer = set_timer(1.0, self.on_ns_timeout)
    
    def on_ns_timeout(self):
        if len(self.ns_messages_sent) >= self.max_ns_attempts:
            # Give up
            fail_session("No NSR received after {self.max_ns_attempts} attempts")
            return
        
        # Retry with new NS message
        send_ns_message(self.payload)
    
    def on_nsr_received(self, nsr_message):
        # Cancel timer
        cancel_timer(self.ns_timer)
        
        # Find which NS this NSR responds to
        tag = nsr_message.tag
        for ns_state in self.ns_messages_sent:
            if tag in ns_state['tagset']:
                # This NSR corresponds to this NS
                self.active_ns_state = ns_state
                break
        
        # Process NSR and complete handshake
        complete_handshake(nsr_message, self.active_ns_state)
        
        # Discard other NS states
        self.ns_messages_sent = []
```
**Důležité vlastnosti:**

1. **Jedinečné efemérní klíče**: Každý NS používá odlišný efemérní klíč
2. **Nezávislé handshake (navázání spojení)**: Každý NS vytváří samostatný stav handshake
3. **Korelace NSR**: Tag NSR identifikuje, na které NS odpovídá
4. **Vyčištění stavů**: Nepoužité stavy NS jsou po úspěšném NSR zahozeny

**Prevence útoků:**

Aby se předešlo vyčerpání prostředků:

```python
# Limit NS sending rate
max_ns_rate = 5 per 10 seconds per destination

# Limit total NS attempts
max_ns_attempts = 5

# Limit total pending NS states
max_pending_ns = 10 per context
```
### Více zpráv NSR

**Scénář**: Bob posílá více NSR (např. data odpovědi rozdělená do více zpráv).

**Bobovo chování:**

```python
class InboundSession:
    def send_nsr_replies(self, payload_chunks):
        # One NS received, multiple NSRs to send
        for chunk in payload_chunks:
            # Generate new ephemeral key for each NSR
            ephemeral_key = generate_elg2_keypair()
            
            # Get next tag from NSR tagset
            tag = self.nsr_tagset.get_next_tag()
            
            nsr_message = build_nsr_message(
                tag=tag,
                ephemeral_key=ephemeral_key,
                payload=chunk
            )
            
            send_message(nsr_message)
        
        # Wait for ES message from Alice
        self.state = SessionState.AWAITING_ES
```
**Chování Alice:**

```python
class OutboundSession:
    def on_nsr_received(self, nsr_message):
        if self.state == SessionState.PENDING_REPLY:
            # First NSR received
            complete_handshake(nsr_message)
            self.state = SessionState.ESTABLISHED
            
            # Create ES sessions
            self.es_outbound_tagset = derive_es_outbound_tagset()
            self.es_inbound_tagset = derive_es_inbound_tagset()
            
            # Send ES message (ACK)
            send_es_message(empty_payload)
        
        elif self.state == SessionState.ESTABLISHED:
            # Additional NSR received
            # Decrypt and process payload
            payload = decrypt_nsr_payload(nsr_message)
            process_payload(payload)
            
            # These NSRs are from other NS attempts, ignore handshake
```
**Bobovo vyčištění:**

```python
class InboundSession:
    def on_es_received(self, es_message):
        # First ES received from Alice
        # This confirms which NSR Alice used
        
        # Clean up other handshake states
        for other_ns_state in self.pending_ns_states:
            if other_ns_state != self.active_ns_state:
                delete_ns_state(other_ns_state)
        
        # Delete unused NSR tagsets
        for tagset in self.nsr_tagsets:
            if tagset != self.active_nsr_tagset:
                delete_tagset(tagset)
        
        self.state = SessionState.ESTABLISHED
```
**Důležité vlastnosti:**

1. **Více NSR je povoleno**: Bob může poslat více NSR pro jeden NS
2. **Odlišné efemérní klíče**: Každá NSR by měla použít jedinečný efemérní klíč
3. **Stejný tagset pro NSR**: Všechny NSR pro jeden NS používají stejný tagset (sada tagů)
4. **První ES rozhoduje**: První ES od Alice určuje, která NSR byla úspěšná
5. **Úklid po ES**: Bob po obdržení ES zahodí nepoužité stavy

### Stavový automat relace

**Úplný stavový diagram:**

```
                    Outbound Session                    Inbound Session

                         NEW
                          |
                     send NS
                          |
                   PENDING_REPLY -------------------- receive NS ---> ESTABLISHED
                          |                                                |
                   receive NSR                                        send NSR
                          |                                                |
                    ESTABLISHED <---------- receive ES ------------- AWAITING_ES
                          |                     |                          |
                    ┌─────┴─────┐               |                    receive ES
                    |           |               |                          |
              send ES      receive ES           |                    ESTABLISHED
                    |           |               |                          |
                    └─────┬─────┘               |                ┌─────────┴─────────┐
                          |                     |                |                   |
                          |                     |          send ES              receive ES
                          |                     |                |                   |
                          |                     |                └─────────┬─────────┘
                          |                     |                          |
                          └─────────────────────┴──────────────────────────┘
                                              ACTIVE
                                                |
                                         idle timeout
                                                |
                                             EXPIRED
```
**Popisy stavů:**

- **NEW**: Vytvořena odchozí relace, zatím nebyl odeslán žádný NS
- **PENDING_REPLY**: NS odeslán, čeká se na NSR
- **AWAITING_ES**: NSR odeslán, čeká se na první ES od Alice
- **ESTABLISHED**: Navázání spojení dokončeno, lze odesílat/přijímat ES
- **ACTIVE**: Aktivně probíhá výměna zpráv ES
- **RATCHETING**: Probíhá DH ratchet – postupné obnovování klíčů Diffie–Hellman (podmnožina stavu ACTIVE)
- **EXPIRED**: Relaci vypršel časový limit, čeká na smazání
- **TERMINATED**: Relace výslovně ukončena

---

## Formát užitečných dat

Sekce užitečných dat všech zpráv ECIES (NS, NSR, ES) používá blokový formát podobný NTCP2.

### Bloková struktura

**Obecný formát:**

```
+----+----+----+----+----+----+----+----+
|blk |  size   |       data             |
+----+----+----+                        +
|                                       |
~               ...                     ~
|                                       |
+----+----+----+----+----+----+----+----+
|blk |  size   |       data             |
+----+----+----+                        +
|                                       |
~               ...                     ~
|                                       |
+----+----+----+----+----+----+----+----+
```
**Pole:**

- `blk`: 1 bajt - Číslo typu bloku
- `size`: 2 bajty - Big-endianová velikost datového pole (0-65516)
- `data`: Proměnná délka - Data specifická pro blok

**Omezení:**

- Maximální rámec ChaChaPoly: 65535 bajtů
- Poly1305 MAC: 16 bajtů
- Maximální celková velikost bloků: 65519 bajtů (65535 - 16)
- Maximální velikost jednoho bloku: 65519 bajtů (včetně 3bajtové hlavičky)
- Maximální velikost dat v jednom bloku: 65516 bajtů

### Typy bloků

**Definované typy bloků:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DateTime</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">7 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Required in NS</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1-3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Future use</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Termination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">9+ bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unimplemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Session termination</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Options</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">21+ bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unimplemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Session options</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">MessageNumbers</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">5 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unimplemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">PN value</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NextKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">3 or 35 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DH ratchet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ACK</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">4+ bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Message acknowledgment</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">9</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ACK Request</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">3 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Request ACK</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Future use</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Garlic Clove</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Variable</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Application data</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12-223</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Future use</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">224-253</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Variable</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Testing features</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">254</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Padding</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Variable</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Traffic shaping</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">255</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Future extension</td>
    </tr>
  </tbody>
</table>
**Zpracování neznámých bloků:**

Implementace MUSÍ ignorovat bloky s neznámými typovými čísly a považovat je za výplň. To zajišťuje dopřednou kompatibilitu.

### Pravidla řazení bloků

### Pořadí zpráv NS

**Povinné:** - blok DateTime MUSÍ být první

**Povoleno:** - Garlic Clove (část zprávy Garlic; 'stroužek') (typ 11) - Možnosti (typ 5) - pokud je implementováno - Výplň (typ 254)

**Zakázáno:** - NextKey, ACK, ACK Request, Termination, MessageNumbers

**Příklad platného NS payloadu:**

```
DateTime (0) | Garlic Clove (11) | Garlic Clove (11) | Padding (254)
```
### Pořadí zpráv v NSR

**Povinné:** - Žádné (užitečná data mohou být prázdná)

**Povoleno:** - Garlic Clove (jedna zapouzdřená zpráva v garlic encryption) (type 11) - Možnosti (type 5) - pokud je implementováno - Výplň (type 254)

**Zakázáno:** - DateTime, NextKey, ACK, ACK Request, Termination, MessageNumbers

**Příklad platného NSR payloadu:**

```
Garlic Clove (11) | Garlic Clove (11) | Padding (254)
```
nebo

```
(empty - ACK only)
```
### Pořadí zpráv ES

**Povinné:** - Žádné (užitečná data mohou být prázdná)

**Povoleno (v libovolném pořadí):** - Garlic Clove (type 11) - NextKey (type 7) - ACK (type 8) - ACK Request (type 9) - Termination (type 4) - je-li implementováno - MessageNumbers (type 6) - je-li implementováno - Options (type 5) - je-li implementováno - Padding (type 254)

**Speciální pravidla:** - Termination (ukončovací blok) MUSÍ být poslední blok (kromě bloku Padding (vycpávka)) - Padding MUSÍ být poslední blok - Více Garlic Cloves (částí 'garlic' zprávy) je povoleno - Až 2 NextKey blocks (bloky s dalším klíčem) jsou povoleny (dopředný a zpětný) - Více bloků Padding NENÍ povoleno

**Příklady platných ES payloadů:**

```
Garlic Clove (11) | ACK (8) | Padding (254)
```
```
NextKey (7) | Garlic Clove (11) | Garlic Clove (11)
```
```
NextKey (7) forward | NextKey (7) reverse | Garlic Clove (11)
```
```
ACK Request (9) | Garlic Clove (11) | Termination (4) | Padding (254)
```
### Blok DateTime (Typ 0)

**Účel**: Časové razítko pro prevenci replay útoků (opakování zachycených zpráv) a ověření odchylky hodin

**Velikost**: 7 bajtů (3bajtová hlavička + 4 bajty dat)

**Formát:**

```
+----+----+----+----+----+----+----+
| 0  |    4    |     timestamp     |
+----+----+----+----+----+----+----+
```
**Pole:**

- `blk`: 0
- `size`: 4 (big-endian; nejvýznamnější bajt první)
- `timestamp`: 4 bajty - Unixové časové razítko v sekundách (bez znaménka, big-endian)

**Formát časového razítka:**

```python
timestamp = int(time.time())  # Seconds since 1970-01-01 00:00:00 UTC
# Wraps around in year 2106 (4-byte unsigned maximum)
```
**Pravidla validace:**

```python
MAX_CLOCK_SKEW_PAST = 5 * 60      # 5 minutes
MAX_CLOCK_SKEW_FUTURE = 2 * 60    # 2 minutes

def validate_datetime(timestamp):
    now = int(time.time())
    age = now - timestamp
    
    if age < -MAX_CLOCK_SKEW_FUTURE:
        return False  # Too far in future
    
    if age > MAX_CLOCK_SKEW_PAST:
        return False  # Too old
    
    return True
```
**Prevence replay útoků:**

```python
class ReplayFilter:
    def __init__(self, duration=5*60):
        self.duration = duration  # 5 minutes
        self.seen_messages = BloomFilter(size=100000, false_positive_rate=0.001)
        self.cleanup_timer = RepeatTimer(60, self.cleanup)
    
    def check_replay(self, ephemeral_key, timestamp):
        # Check timestamp validity
        if not validate_datetime(timestamp):
            return False
        
        # Check if ephemeral key seen recently
        if ephemeral_key in self.seen_messages:
            return False  # Replay attack
        
        # Add to seen messages
        self.seen_messages.add(ephemeral_key)
        return True
    
    def cleanup(self):
        # Expire old entries (Bloom filter automatically ages out)
        pass
```
**Poznámky k implementaci:**

1. **NS Messages**: DateTime MUSÍ být prvním blokem
2. **NSR/ES Messages**: DateTime se obvykle neuvádí
3. **Replay Window** (okno pro opakování útoku): minimálně doporučená hodnota je 5 minut
4. **Bloomův filtr**: doporučen pro efektivní detekci replay útoků
5. **Odchylka hodin**: povolte 5 minut do minulosti, 2 minuty do budoucnosti

### Garlic Clove Block (blok dílčí zprávy v rámci garlic zprávy) (Typ 11)

**Účel**: Zapouzdřuje zprávy I2NP pro doručení

**Formát:**

```
+----+----+----+----+----+----+----+----+
| 11 |  size   |                        |
+----+----+----+                        +
|      Delivery Instructions            |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|type|  Message_ID       | Expiration  |
+----+----+----+----+----+----+----+----+
     |      I2NP Message body           |
+----+                                  +
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
```
**Pole:**

- `blk`: 11
- `size`: Celková velikost clove (dílčí zpráva v rámci zprávy typu garlic; proměnlivá)
- `Delivery Instructions`: Jak je uvedeno ve specifikaci I2NP
- `type`: Typ zprávy I2NP (1 bajt)
- `Message_ID`: Identifikátor zprávy I2NP (4 bajty)
- `Expiration`: Unixové časové razítko v sekundách (4 bajty)
- `I2NP Message body`: Data zprávy s proměnlivou délkou

**Formáty pokynů pro doručení:**

**Lokální doručení** (1 bajt):

```
+----+
|0x00|
+----+
```
**Doručení pro Destination** (Destination = identita/koncová adresa v I2P) (33 bajtů):

```
+----+----+----+----+----+----+----+----+
|0x01|                                  |
+----+        Destination Hash         +
|              32 bytes                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
**Router Delivery** (33 bajtů):

```
+----+----+----+----+----+----+----+----+
|0x02|                                  |
+----+         Router Hash              +
|              32 bytes                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
**Tunnel Delivery** (37 bajtů):

```
+----+----+----+----+----+----+----+----+
|0x03|         Tunnel ID                |
+----+----+----+----+----+              +
|           Router Hash                 |
+              32 bytes                 +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
**Hlavička zprávy I2NP** (celkem 9 bajtů):

```
+----+----+----+----+----+----+----+----+
|type|      msg_id       |  expiration   |
+----+----+----+----+----+----+----+----+
     |                                   |
```
- `type`: typ zprávy I2NP (Database Store, Database Lookup, Data, atd.)
- `msg_id`: 4bajtový identifikátor zprávy
- `expiration`: 4bajtové Unixové časové razítko (sekundy)

**Důležité rozdíly oproti ElGamal Clove Format (formát 'clove' v rámci šifrovacího schématu ElGamal):**

1. **Žádný certifikát**: Pole certifikátu vynecháno (v ElGamalu se nepoužívá)
2. **Žádné Clove ID**: Clove ID vynecháno (bylo vždy 0; Clove = podzpráva v rámci I2P 'garlic' zprávy)
3. **Žádná expirace Clove**: Místo toho se používá expirace zprávy I2NP
4. **Kompaktní hlavička**: 9bajtová hlavička I2NP oproti většímu formátu ElGamalu
5. **Každý Clove je samostatný blok**: Žádná struktura CloveSet

**Více stroužků:**

```python
# Multiple Garlic Cloves in one message
payload = [
    build_datetime_block(),
    build_garlic_clove(i2np_message_1),
    build_garlic_clove(i2np_message_2),
    build_garlic_clove(i2np_message_3),
    build_padding_block()
]
```
**Běžné typy I2NP zpráv v Cloves (stroužcích, termín v rámci garlic encryption):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseStore</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Publishing LeaseSet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseLookup</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Requesting LeaseSet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DeliveryStatus</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ACK (legacy, avoid in ECIES)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Streaming data</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">21</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Garlic</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Nested garlic messages</td>
    </tr>
  </tbody>
</table>
**Zpracování clove (podzpráva v rámci garlic encryption):**

```python
def process_garlic_clove(clove_data):
    # Parse delivery instructions
    delivery_type = clove_data[0]
    
    if delivery_type == 0x00:
        # Local delivery
        offset = 1
    elif delivery_type == 0x01:
        # Destination delivery
        dest_hash = clove_data[1:33]
        offset = 33
    elif delivery_type == 0x02:
        # Router delivery
        router_hash = clove_data[1:33]
        offset = 33
    elif delivery_type == 0x03:
        # Tunnel delivery
        tunnel_id = struct.unpack('>I', clove_data[1:5])[0]
        router_hash = clove_data[5:37]
        offset = 37
    
    # Parse I2NP header
    i2np_type = clove_data[offset]
    msg_id = struct.unpack('>I', clove_data[offset+1:offset+5])[0]
    expiration = struct.unpack('>I', clove_data[offset+5:offset+9])[0]
    
    # Extract I2NP body
    i2np_body = clove_data[offset+9:]
    
    # Process message
    process_i2np_message(i2np_type, msg_id, expiration, i2np_body)
```
### Blok NextKey (Typ 7)

**Účel**: výměna klíčů pomocí DH ratchet (ráčnový mechanismus Diffie–Hellman)

**Formát (klíč přítomen - 38 bajtů):**

```
+----+----+----+----+----+----+----+----+
| 7  |   35    |flag|  key ID |         |
+----+----+----+----+----+----+         +
|                                       |
+     Next DH Ratchet Public Key        +
|              32 bytes                 |
+                                       +
|                                       |
+                             +----+----+
|                             |
+----+----+----+----+----+----+
```
**Formát (Pouze ID klíče - 6 bajtů):**

```
+----+----+----+----+----+----+
| 7  |    3    |flag|  key ID |
+----+----+----+----+----+----+
```
**Pole:**

- `blk`: 7
- `size`: 3 (pouze ID) nebo 35 (s klíčem)
- `flag`: 1 bajt - bity příznaku
- `key ID`: 2 bajty - Big-endian identifikátor klíče (0-32767)
- `Public Key`: 32 bajtů - veřejný klíč X25519 (little-endian), pokud je bit 0 příznaku = 1

**Příznakové bity:**

```
Bit 7 6 5 4 3 2 1 0
    | | | | | | | |
    | | | | | | | +-- Bit 0: Key present (1) or ID only (0)
    | | | | | | +---- Bit 1: Reverse key (1) or forward key (0)
    | | | | | +------ Bit 2: Request reverse key (1) or no request (0)
    | | | | |
    +-+-+-+-+-------- Bits 3-7: Reserved (set to 0)
```
**Příklady příznaků:**

```python
# Forward key present
flags = 0x01  # Binary: 00000001

# Reverse key present
flags = 0x03  # Binary: 00000011

# Forward key ID only (ACK)
flags = 0x00  # Binary: 00000000

# Reverse key ID only (ACK)
flags = 0x02  # Binary: 00000010

# Forward key ID with reverse request
flags = 0x04  # Binary: 00000100
```
**Pravidla pro ID klíčů:**

- ID jsou sekvenční: 0, 1, 2, ..., 32767
- ID se zvyšuje pouze při vygenerování nového klíče
- Stejné ID se používá pro více zpráv, dokud neproběhne další ratchet (kryptografický krok)
- Maximální ID je 32767 (poté je nutné zahájit novou relaci)

**Příklady použití:**

```python
# Initiating ratchet (sender generates new key)
nextkey = NextKeyBlock(
    flags=0x01,           # Key present, forward
    key_id=0,
    public_key=sender_new_pk
)

# Replying to ratchet (receiver generates new key)
nextkey = NextKeyBlock(
    flags=0x03,           # Key present, reverse
    key_id=0,
    public_key=receiver_new_pk
)

# Acknowledging ratchet (no new key from sender)
nextkey = NextKeyBlock(
    flags=0x02,           # ID only, reverse
    key_id=0
)

# Requesting reverse ratchet
nextkey = NextKeyBlock(
    flags=0x04,           # Request reverse, forward ID
    key_id=1
)
```
**Logika zpracování:**

```python
def process_nextkey_block(block):
    flags = block.flags
    key_id = block.key_id
    
    key_present = (flags & 0x01) != 0
    is_reverse = (flags & 0x02) != 0
    request_reverse = (flags & 0x04) != 0
    
    if key_present:
        public_key = block.public_key
        
        if is_reverse:
            # Reverse key received
            perform_dh_ratchet(receiver_key=public_key, key_id=key_id)
            # Sender should ACK with own key ID
        else:
            # Forward key received
            perform_dh_ratchet(sender_key=public_key, key_id=key_id)
            # Receiver should reply with reverse key
            send_reverse_key(generate_new_key())
    
    else:
        # Key ID only (ACK)
        if is_reverse:
            # Reverse key ACK
            confirm_reverse_ratchet(key_id)
        else:
            # Forward key ACK
            confirm_forward_ratchet(key_id)
    
    if request_reverse:
        # Sender requests receiver to generate new key
        send_reverse_key(generate_new_key())
```
**Více bloků NextKey:**

Jedna zpráva ES může obsahovat až 2 bloky NextKey, pokud v obou směrech současně probíhá ratcheting (průběžné obnovování klíčů):

```python
# Both directions ratcheting
payload = [
    NextKeyBlock(flags=0x01, key_id=2, public_key=forward_key),  # Forward
    NextKeyBlock(flags=0x03, key_id=1, public_key=reverse_key),  # Reverse
    build_garlic_clove(data)
]
```
### Blok ACK (Typ 8)

**Účel**: Potvrzovat přijaté zprávy v rámci stejného kanálu

**Formát (jediný ACK - 7 bajtů):**

```
+----+----+----+----+----+----+----+
| 8  |    4    |tagsetid |   N     |
+----+----+----+----+----+----+----+
```
**Formát (více ACKs (potvrzení)):**

```
+----+----+----+----+----+----+----+----+
| 8  |  size   |tagsetid |   N     |    |
+----+----+----+----+----+----+----+    +
|            more ACKs                  |
~               ...                     ~
|                                       |
+----+----+----+----+----+----+----+----+
```
**Pole:**

- `blk`: 8
- `size`: 4 * počet ACKů (minimálně 4)
- Pro každý ACK:
  - `tagsetid`: 2 bajty - Big-endian ID sady tagů (0-65535)
  - `N`: 2 bajty - Big-endian číslo zprávy (0-65535)

**Určení ID sady značek:**

```python
# Tag set 0 (initial, after NSR)
tagset_id = 0

# After first ratchet (tag set 1)
# Both Alice and Bob sent key ID 0
tagset_id = 1 + 0 + 0 = 1

# After second ratchet (tag set 2)
# Alice sent key ID 1, Bob still using key ID 0
tagset_id = 1 + 1 + 0 = 2

# After third ratchet (tag set 3)
# Alice still using key ID 1, Bob sent key ID 1
tagset_id = 1 + 1 + 1 = 3
```
**Příklad s jediným ACK:**

```python
# ACK message from tag set 5, message number 127
ack_block = ACKBlock(
    tagset_id=5,
    message_number=127
)

# Wire format (7 bytes):
# 08 00 04 00 05 00 7F
# |  |  |  |  |  |  |
# |  |  |  |  |  |  +-- N (127)
# |  |  |  |  +--------- N high byte
# |  |  |  +------------ tagset_id (5)
# |  |  +--------------- tagset_id high byte
# |  +------------------ size (4)
# +--------------------- type (8)
```
**Příklad více ACKů:**

```python
# ACK three messages
ack_block = ACKBlock([
    (tagset_id=3, N=42),
    (tagset_id=3, N=43),
    (tagset_id=4, N=0)
])

# Wire format (15 bytes):
# 08 00 0C 00 03 00 2A 00 03 00 2B 00 04 00 00
#                (ts=3, N=42) (ts=3, N=43) (ts=4, N=0)
```
**Zpracování:**

```python
def process_ack_block(block):
    num_acks = block.size // 4
    
    for i in range(num_acks):
        offset = i * 4
        tagset_id = struct.unpack('>H', block.data[offset:offset+2])[0]
        message_num = struct.unpack('>H', block.data[offset+2:offset+4])[0]
        
        # Mark message as acknowledged
        mark_acked(tagset_id, message_num)
        
        # May trigger retransmission timeout cancellation
        cancel_retransmit_timer(tagset_id, message_num)
```
**Kdy odesílat ACKs (potvrzení):**

1. **Explicitní ACK Request**: Vždy odpovězte na blok ACK Request
2. **Doručení LeaseSet**: Pokud odesílatel zahrne LeaseSet do zprávy
3. **Navázání relace**: Může potvrdit (ACK) NS/NSR (ačkoli protokol preferuje implicitní ACK prostřednictvím ES)
4. **Potvrzení ratchetu (ratchet = mechanismus průběžné rotace klíčů)**: Může potvrdit (ACK) přijetí NextKey
5. **Aplikační vrstva**: Podle požadavků protokolu vyšší vrstvy (např. Streaming)

**Načasování ACK:**

```python
class ACKManager:
    def __init__(self):
        self.pending_acks = []
        self.ack_timer = None
    
    def request_ack(self, tagset_id, message_num):
        self.pending_acks.append((tagset_id, message_num))
        
        if not self.ack_timer:
            # Delay ACK briefly to allow higher layer to respond
            self.ack_timer = set_timer(0.1, self.send_acks)  # 100ms
    
    def send_acks(self):
        if self.pending_acks and not has_outbound_data():
            # No higher layer data, send explicit ACK
            send_es_message(build_ack_block(self.pending_acks))
        
        # Otherwise, ACK will piggyback on next ES message
        self.pending_acks = []
        self.ack_timer = None
```
### Blok požadavku na ACK (Typ 9)

**Účel**: Vyžádat in-band (v rámci stejného kanálu) potvrzení přijetí aktuální zprávy

**Formát:**

```
+----+----+----+----+
| 9  |    1    |flg |
+----+----+----+----+
```
**Pole:**

- `blk`: 9
- `size`: 1
- `flg`: 1 bajt - Příznaky (všechny bity jsou aktuálně nepoužité, nastaveny na 0)

**Použití:**

```python
# Request ACK for this message
payload = [
    build_ack_request_block(),
    build_garlic_clove(important_data)
]
```
**Odpověď přijímače:**

Když je přijata ACK Request (požadavek na potvrzení):

1. **With Immediate Data**: Zahrňte blok ACK do okamžité odpovědi
2. **Without Immediate Data**: Spusťte časovač (např. 100ms) a pokud časovač vyprší, odešlete prázdný ES s ACK
3. **Tag Set ID**: Použijte aktuální ID příchozího tagsetu (sada tagů)
4. **Message Number**: Použijte číslo zprávy spojené s přijatým session tagem (značka relace)

**Zpracování:**

```python
def process_ack_request(message):
    # Extract message identification
    tagset_id = message.tagset_id
    message_num = message.message_num
    
    # Schedule ACK
    schedule_ack(tagset_id, message_num)
    
    # If no data to send immediately, start timer
    if not has_pending_data():
        set_timer(0.1, lambda: send_ack_only(tagset_id, message_num))
```
**Kdy použít ACK Request (požadavek na potvrzení):**

1. **Kritické zprávy**: Zprávy, které musí být potvrzeny
2. **Doručení LeaseSet**: Při přibalení LeaseSet
3. **Session Ratchet**: (mechanismus postupné obměny klíčů) Po odeslání NextKey block
4. **Konec přenosu**: Když odesílatel už nemá další data k odeslání, ale chce potvrzení

**Kdy NE používat:**

1. **Protokol pro streamování**: Vrstva streamování zpracovává ACK (potvrzení přijetí)
2. **Zprávy s vysokou četností**: Vyhněte se požadavku na ACK u každé zprávy (režie)
3. **Nedůležité datagramy**: Surové datagramy obvykle nepotřebují ACK

### Ukončovací blok (typ 4)

**Stav**: NEIMPLEMENTOVÁNO

**Účel**: Korektně ukončit relaci

**Formát:**

```
+----+----+----+----+----+----+----+----+
| 4  |  size   | rsn|     addl data     |
+----+----+----+----+                   +
~               ...                     ~
+----+----+----+----+----+----+----+----+
```
**Pole:**

- `blk`: 4
- `size`: 1 nebo více bajtů
- `rsn`: 1 bajt - kód důvodu
- `addl data`: Volitelná dodatečná data (formát závisí na důvodu)

**Důvodové kódy:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Meaning</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Additional Data</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Normal close / unspecified</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">None</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Termination received</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">None</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Idle timeout</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">None (implementation-specific)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Resource exhaustion</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">None (implementation-specific)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4+</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implementation-specific</td>
    </tr>
  </tbody>
</table>
**Použití (až bude implementováno):**

```python
# Normal session close
termination = TerminationBlock(
    reason=0,
    additional_data=b''
)

# Session termination due to received termination
termination = TerminationBlock(
    reason=1,
    additional_data=b''
)
```
**Pravidla:**

- MUSÍ být posledním blokem, s výjimkou Padding (výplň)
- Je-li přítomen Termination (ukončení), Padding jej MUSÍ následovat
- Není povoleno ve zprávách NS ani NSR
- Povoleno pouze ve zprávách ES

### Blok voleb (Typ 5)

**Stav**: NEIMPLEMENTOVÁNO

**Účel**: Vyjednat parametry relace

**Formát:**

```
+----+----+----+----+----+----+----+----+
| 5  |  size   |ver |flg |STL |STimeout |
+----+----+----+----+----+----+----+----+
|  SOTW   |  RITW   |tmin|tmax|rmin|rmax|
+----+----+----+----+----+----+----+----+
|  tdmy   |  rdmy   |  tdelay |  rdelay |
+----+----+----+----+----+----+----+----+
|              more_options             |
~               ...                     ~
|                                       |
+----+----+----+----+----+----+----+----+
```
**Pole:**

- `blk`: 5
- `size`: 21 nebo více bajtů
- `ver`: 1 bajt - Verze protokolu (musí být 0)
- `flg`: 1 bajt - Příznaky (všechny bity jsou aktuálně nevyužité)
- `STL`: 1 bajt - Délka session tagu (značky relace) (musí být 8)
- `STimeout`: 2 bajty - Časový limit nečinnosti relace v sekundách (big-endian)
- `SOTW`: 2 bajty - Okno odchozích značek odesílatele (big-endian)
- `RITW`: 2 bajty - Okno příchozích značek příjemce (big-endian)
- `tmin`, `tmax`, `rmin`, `rmax`: každý po 1 bajtu - Parametry vyplňování (4.4 s pevnou desetinnou čárkou)
- `tdmy`: 2 bajty - Max. falešný provoz (dummy traffic), který je ochoten posílat (bajtů/s, big-endian)
- `rdmy`: 2 bajty - Požadovaný falešný provoz (bajtů/s, big-endian)
- `tdelay`: 2 bajty - Max. vnitrozprávové zpoždění, které je ochoten vložit (msec, big-endian)
- `rdelay`: 2 bajty - Požadované vnitrozprávové zpoždění (msec, big-endian)
- `more_options`: Proměnná délka - budoucí rozšíření

**Parametry výplně (4.4 s pevnou řádovou čárkou):**

```python
def encode_padding_ratio(ratio):
    """
    Encode padding ratio as 4.4 fixed-point
    
    ratio: 0.0 to 15.9375
    returns: 0x00 to 0xFF
    """
    return int(ratio * 16)

def decode_padding_ratio(encoded):
    """
    Decode 4.4 fixed-point to ratio
    
    encoded: 0x00 to 0xFF
    returns: 0.0 to 15.9375
    """
    return encoded / 16.0

# Examples:
# 0x00 = 0.0 (no padding)
# 0x01 = 0.0625 (6.25% padding)
# 0x10 = 1.0 (100% padding - double traffic)
# 0x80 = 8.0 (800% padding - 9x traffic)
# 0xFF = 15.9375 (1593.75% padding)
```
**Vyjednávání okna tagů:**

```python
# SOTW: Sender's recommendation for receiver's inbound window
# RITW: Sender's declaration of own inbound window

# Receiver calculates actual inbound window:
inbound_window = calculate_window(
    sender_suggestion=SOTW,
    own_constraints=MAX_INBOUND_TAGS,
    own_resources=available_memory()
)

# Sender uses:
# - RITW to know how far ahead receiver will accept
# - Own SOTW to hint optimal window size
```
**Výchozí hodnoty (pokud nejsou vyjednány možnosti):**

```python
DEFAULT_OPTIONS = {
    'version': 0,
    'session_tag_length': 8,
    'session_timeout': 600,  # 10 minutes
    'sender_outbound_tag_window': 160,
    'receiver_inbound_tag_window': 160,
    'tmin': 0x00,  # No minimum padding
    'tmax': 0x10,  # Up to 100% padding
    'rmin': 0x00,  # No minimum requested
    'rmax': 0x10,  # Up to 100% requested
    'tdmy': 0,     # No dummy traffic
    'rdmy': 0,     # No dummy traffic requested
    'tdelay': 0,   # No delay
    'rdelay': 0    # No delay requested
}
```
### Blok čísel zpráv (Typ 6)

**Stav**: NEIMPLEMENTOVÁNO

**Účel**: Označuje poslední zprávu odeslanou v předchozí sadě tagů (umožňuje detekci mezer)

**Formát:**

```
+----+----+----+----+----+
| 6  |    2    |  PN    |
+----+----+----+----+----+
```
**Pole:**

- `blk`: 6
- `size`: 2
- `PN`: 2 bajty - číslo poslední zprávy předchozí sady značek (big-endian (pořadí bajtů od nejvýznamnějšího), 0-65535)

**Definice PN (předchozí číslo):**

PN je index poslední značky odeslané v předchozí sadě značek.

**Použití (až bude implementováno):**

```python
# After ratcheting to new tag set
# Old tag set: sent messages 0-4095
# New tag set: sending first message

payload = [
    MessageNumbersBlock(PN=4095),
    build_garlic_clove(data)
]
```
**Výhody pro příjemce:**

```python
def process_message_numbers(pn_value):
    # Receiver can now:
    
    # 1. Determine if any messages were skipped
    highest_received_in_old_tagset = 4090
    if pn_value > highest_received_in_old_tagset:
        missing_count = pn_value - highest_received_in_old_tagset
        # 5 messages were never received
    
    # 2. Delete tags higher than PN from old tagset
    for tag_index in range(pn_value + 1, MAX_TAG_INDEX):
        delete_tag(old_tagset, tag_index)
    
    # 3. Expire tags ≤ PN after grace period (e.g., 2 minutes)
    schedule_deletion(old_tagset, delay=120)
```
**Pravidla:**

- NESMÍ být odesláno v tag set 0 (žádný předchozí tag set; "tag set" = sada tagů)
- Odesílá se pouze v ES messages (ES zprávách)
- Odesílá se pouze v první zprávě (zprávách) nového tag set
- PN value (hodnota PN) je z pohledu odesílatele (poslední tag, který odesílatel poslal)

**Vztah k aplikaci Signal:**

V Signal Double Ratchet je PN v hlavičce zprávy. V ECIES je v šifrované části zprávy a je volitelný.

### Výplňový blok (typ 254)

**Účel**: Odolnost vůči analýze provozu a zamlžování velikosti zpráv

**Formát:**

```
+----+----+----+----+----+----+----+----+
|254 |  size   |      padding           |
+----+----+----+                        +
|                                       |
~               ...                     ~
|                                       |
+----+----+----+----+----+----+----+----+
```
**Pole:**

- `blk`: 254
- `size`: 0-65516 bajtů (big-endian, pořadí bajtů od nejvýznamnějšího)
- `padding`: Náhodná nebo nulová data

**Pravidla:**

- MUSÍ být posledním blokem ve zprávě
- Více bloků Padding (výplň) NENÍ povoleno
- Může mít nulovou délku (pouze 3bajtová hlavička)
- Data bloku Padding mohou být samé nuly nebo náhodné bajty

**Výchozí padding (výplň):**

```python
DEFAULT_PADDING_MIN = 0
DEFAULT_PADDING_MAX = 15

def generate_default_padding():
    size = random.randint(DEFAULT_PADDING_MIN, DEFAULT_PADDING_MAX)
    data = random.bytes(size)  # or zeros
    return PaddingBlock(size, data)
```
**Strategie odolnosti vůči analýze provozu:**

**Strategie 1: Náhodná velikost (výchozí)**

```python
# Add 0-15 bytes random padding to each message
padding_size = random.randint(0, 15)
padding_block = PaddingBlock(padding_size, random.bytes(padding_size))
```
**Strategie 2: Zaokrouhlení na násobek**

```python
# Round total message size to next multiple of 64
target_size = ((message_size + 63) // 64) * 64
padding_size = target_size - message_size - 3  # -3 for block header
padding_block = PaddingBlock(padding_size, random.bytes(padding_size))
```
**Strategie 3: Pevné velikosti zpráv**

```python
# Always send 1KB messages
TARGET_MESSAGE_SIZE = 1024
padding_size = TARGET_MESSAGE_SIZE - message_size - 3
padding_block = PaddingBlock(padding_size, random.bytes(padding_size))
```
**Strategie 4: Vyjednané vycpávání (blok Options)**

```python
# Calculate padding based on negotiated parameters
# tmin, tmax from Options block
min_padding = int(payload_size * tmin_ratio)
max_padding = int(payload_size * tmax_ratio)
padding_size = random.randint(min_padding, max_padding)
padding_block = PaddingBlock(padding_size, random.bytes(padding_size))
```
**Zprávy obsahující pouze výplň:**

Zprávy mohou sestávat výhradně z výplně (bez aplikačních dat):

```python
# Dummy traffic message
payload = [
    PaddingBlock(random.randint(100, 500), random.bytes(...))
]
```
**Poznámky k implementaci:**

1. **Výplň samými nulami**: Přijatelná (bude zašifrována algoritmem ChaCha20)
2. **Náhodná výplň**: Po šifrování neposkytuje žádné dodatečné zabezpečení, ale spotřebovává více entropie
3. **Výkon**: Generování náhodné výplně může být výpočetně náročné; zvažte použití samých nul
4. **Paměť**: Velké bloky výplně spotřebovávají šířku pásma; buďte opatrní s maximální velikostí

---

## Implementační příručka

### Předpoklady

**Kryptografické knihovny:**

- **X25519**: libsodium, NaCl nebo Bouncy Castle
- **ChaCha20-Poly1305**: libsodium, OpenSSL 1.1.0+ nebo Bouncy Castle
- **SHA-256**: OpenSSL, Bouncy Castle nebo vestavěná podpora v jazyce
- **Elligator2** (technika mapování veřejných klíčů na náhodně vypadající reprezentace): Omezená podpora v knihovnách; může vyžadovat vlastní implementaci

**Implementace Elligator2 (technika pro mapování bodů eliptické křivky na rovnoměrně rozdělená data):**

Elligator2 (kryptografická technika pro zakódování bodů eliptické křivky do náhodně vypadajících bajtů) není široce implementován. Možnosti:

1. **OBFS4**: Zásuvný transport obfs4 pro Tor obsahuje implementaci Elligator2 (kryptografická metoda pro mapování náhodných dat na body eliptické křivky)
2. **Vlastní implementace**: Založena na [článku Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf)
3. **kleshni/Elligator**: Referenční implementace na GitHubu

**Poznámka k Java I2P:** Java I2P používá knihovnu net.i2p.crypto.eddsa s vlastními rozšířeními Elligator2.

### Doporučené pořadí implementace

**Fáze 1: Základní kryptografie** 1. X25519 DH generování a výměna klíčů 2. ChaCha20-Poly1305 AEAD (autentizované šifrování s přidruženými daty) šifrování/dešifrování 3. SHA-256 hašování a MixHash 4. HKDF (odvozování klíčů na bázi HMAC) odvozování klíčů 5. Elligator2 (metoda maskování bodů eliptické křivky) kódování/dekódování (zpočátku lze použít testovací vektory)

**Fáze 2: Formáty zpráv** 1. Zpráva NS (nevázaná) - nejjednodušší formát 2. Zpráva NS (vázaná) - přidává statický klíč 3. Zpráva NSR 4. Zpráva ES 5. Parsování a generování bloků

**Fáze 3: Správa relací** 1. Vytváření a ukládání relací 2. Správa sady tagů (značek) (odesílatel a příjemce) 3. Ratchet (krokovací mechanismus) pro session tagy 4. Ratchet symetrického klíče 5. Vyhledávání tagů a správa okna

**Fáze 4: DH Ratcheting (ráčnový mechanismus Diffie–Hellman)** 1. Zpracování bloku NextKey 2. DH ratchet KDF (funkce odvození klíče) 3. Vytvoření sady tagů po provedení ratchet 4. Správa více sad tagů

**Fáze 5: Logika protokolu** 1. Stavový automat NS/NSR/ES 2. Prevence replay (útoku opakovaným přehráním) (DateTime, Bloomův filtr) 3. Logika retransmise (více NS/NSR) 4. Zpracování ACK (potvrzení přijetí)

**Fáze 6: Integrace** 1. zpracování I2NP Garlic Clove (jednotlivý segment zprávy) 2. sdružování LeaseSet 3. integrace streamingového protokolu 4. integrace datagramového protokolu

### Implementace odesílatele

**Životní cyklus odchozí relace:**

```python
class OutboundSession:
    def __init__(self, destination, bound=True):
        self.destination = destination
        self.bound = bound
        self.state = SessionState.NEW
        
        # Keys for NS message
        self.ephemeral_keypair = generate_elg2_keypair()
        if bound:
            self.static_key = context.static_keypair
        
        # Will be populated after NSR
        self.outbound_tagset = None
        self.outbound_keyratchet = None
        self.inbound_tagset = None
        self.inbound_keyratchet = None
        
        # Timing
        self.created_time = now()
        self.last_activity = now()
        
        # Retransmission
        self.ns_attempts = []
        self.ns_timer = None
    
    def send_initial_message(self, payload):
        """Send NS message"""
        # Build NS message
        ns_message = self.build_ns_message(payload)
        
        # Send
        send_to_network(self.destination, ns_message)
        
        # Track for retransmission
        self.ns_attempts.append({
            'message': ns_message,
            'time': now(),
            'ephemeral_key': self.ephemeral_keypair,
            'kdf_state': self.save_kdf_state()
        })
        
        # Start timer
        self.ns_timer = set_timer(1.0, self.on_ns_timeout)
        self.state = SessionState.PENDING_REPLY
    
    def build_ns_message(self, payload):
        """Construct NS message"""
        # KDF initialization
        chainKey, h = self.initialize_kdf()
        
        # Ephemeral key section
        elg2_ephemeral = ENCODE_ELG2(self.ephemeral_keypair.public_key)
        h = SHA256(h || self.destination.static_key)
        h = SHA256(h || self.ephemeral_keypair.public_key)
        
        # es DH
        es_shared = DH(self.ephemeral_keypair.private_key, 
                       self.destination.static_key)
        keydata = HKDF(chainKey, es_shared, "", 64)
        chainKey = keydata[0:31]
        k_static = keydata[32:63]
        
        # Encrypt static key section
        if self.bound:
            static_section = self.static_key.public_key
        else:
            static_section = bytes(32)
        
        static_ciphertext = ENCRYPT(k_static, 0, static_section, h)
        h = SHA256(h || static_ciphertext)
        
        # ss DH (if bound)
        if self.bound:
            ss_shared = DH(self.static_key.private_key, 
                          self.destination.static_key)
            keydata = HKDF(chainKey, ss_shared, "", 64)
            chainKey = keydata[0:31]
            k_payload = keydata[32:63]
            nonce = 0
        else:
            k_payload = k_static
            nonce = 1
        
        # Build payload blocks
        payload_data = self.build_ns_payload(payload)
        
        # Encrypt payload
        payload_ciphertext = ENCRYPT(k_payload, nonce, payload_data, h)
        h = SHA256(h || payload_ciphertext)
        
        # Save KDF state for NSR processing
        self.ns_chainkey = chainKey
        self.ns_hash = h
        
        # Assemble message
        return elg2_ephemeral + static_ciphertext + payload_ciphertext
    
    def build_ns_payload(self, application_data):
        """Build NS payload blocks"""
        blocks = []
        
        # DateTime block (required, first)
        blocks.append(build_datetime_block())
        
        # Garlic Clove(s) with application data
        blocks.append(build_garlic_clove(application_data))
        
        # Optionally bundle LeaseSet
        if should_send_leaseset():
            blocks.append(build_garlic_clove(build_leaseset_store()))
        
        # Padding
        blocks.append(build_padding_block(random.randint(0, 15)))
        
        return encode_blocks(blocks)
    
    def on_nsr_received(self, nsr_message):
        """Process NSR and establish ES session"""
        # Cancel retransmission timer
        cancel_timer(self.ns_timer)
        
        # Parse NSR
        tag = nsr_message[0:8]
        elg2_bob_ephemeral = nsr_message[8:40]
        key_section_mac = nsr_message[40:56]
        payload_ciphertext = nsr_message[56:]
        
        # Find corresponding NS attempt
        ns_state = self.find_ns_by_tag(tag)
        if not ns_state:
            raise ValueError("NSR tag doesn't match any NS")
        
        # Restore KDF state
        chainKey = ns_state['chainkey']
        h = ns_state['hash']
        
        # Decode Bob's ephemeral key
        bob_ephemeral = DECODE_ELG2(elg2_bob_ephemeral)
        
        # Mix tag and Bob's ephemeral into hash
        h = SHA256(h || tag)
        h = SHA256(h || bob_ephemeral)
        
        # ee DH
        ee_shared = DH(self.ephemeral_keypair.private_key, bob_ephemeral)
        keydata = HKDF(chainKey, ee_shared, "", 32)
        chainKey = keydata[0:31]
        
        # se DH
        se_shared = DH(self.static_key.private_key, bob_ephemeral)
        keydata = HKDF(chainKey, se_shared, "", 64)
        chainKey = keydata[0:31]
        k_key_section = keydata[32:63]
        
        # Verify key section MAC
        try:
            DECRYPT(k_key_section, 0, key_section_mac, h)
        except AuthenticationError:
            raise ValueError("NSR key section MAC verification failed")
        
        h = SHA256(h || key_section_mac)
        
        # Split for bidirectional ES
        keydata = HKDF(chainKey, ZEROLEN, "", 64)
        k_ab = keydata[0:31]  # Alice → Bob
        k_ba = keydata[32:63]  # Bob → Alice
        
        # Initialize ES tagsets
        self.outbound_tagset = DH_INITIALIZE(chainKey, k_ab)
        self.inbound_tagset = DH_INITIALIZE(chainKey, k_ba)
        
        # Decrypt NSR payload
        k_nsr = HKDF(k_ba, ZEROLEN, "AttachPayloadKDF", 32)
        try:
            payload = DECRYPT(k_nsr, 0, payload_ciphertext, h)
        except AuthenticationError:
            raise ValueError("NSR payload MAC verification failed")
        
        # Process NSR payload blocks
        self.process_payload_blocks(payload)
        
        # Session established
        self.state = SessionState.ESTABLISHED
        self.last_activity = now()
        
        # Send ES message (implicit ACK)
        self.send_es_ack()
    
    def send_es_message(self, payload):
        """Send ES message"""
        if self.state != SessionState.ESTABLISHED:
            raise ValueError("Session not established")
        
        # Get next tag and key
        tag, index = self.outbound_tagset.get_next_tag()
        key = self.outbound_keyratchet.get_key(index)
        
        # Construct nonce
        nonce = construct_nonce(index)
        
        # Build payload blocks
        payload_data = self.build_es_payload(payload)
        
        # AEAD encryption
        ciphertext = ENCRYPT(key, nonce, payload_data, tag)
        
        # Assemble message
        es_message = tag + ciphertext
        
        # Send
        send_to_network(self.destination, es_message)
        
        # Update activity
        self.last_activity = now()
        
        # Check if ratchet needed
        if self.outbound_tagset.should_ratchet():
            self.initiate_ratchet()
```
### Implementace přijímače

**Životní cyklus příchozí relace:**

```python
class InboundSession:
    def __init__(self):
        self.state = None
        self.bound = False
        self.destination = None
        
        # Keys
        self.remote_ephemeral_key = None
        self.remote_static_key = None
        self.ephemeral_keypair = None
        
        # Tagsets
        self.inbound_tagset = None
        self.outbound_tagset = None
        
        # Timing
        self.created_time = None
        self.last_activity = None
        
        # Paired session
        self.paired_outbound = None
    
    @staticmethod
    def try_decrypt_ns(message):
        """Attempt to decrypt as NS message"""
        # Parse NS structure
        elg2_ephemeral = message[0:32]
        static_ciphertext = message[32:80]  # 32 + 16
        payload_ciphertext = message[80:]
        
        # Decode ephemeral key
        try:
            alice_ephemeral = DECODE_ELG2(elg2_ephemeral)
        except:
            return None  # Not a valid Elligator2 encoding
        
        # Check replay
        if is_replay(alice_ephemeral):
            return None
        
        # KDF initialization
        chainKey, h = initialize_kdf()
        
        # Mix keys
        h = SHA256(h || context.static_keypair.public_key)
        h = SHA256(h || alice_ephemeral)
        
        # es DH
        es_shared = DH(context.static_keypair.private_key, alice_ephemeral)
        keydata = HKDF(chainKey, es_shared, "", 64)
        chainKey = keydata[0:31]
        k_static = keydata[32:63]
        
        # Decrypt static key section
        try:
            static_data = DECRYPT(k_static, 0, static_ciphertext, h)
        except AuthenticationError:
            return None  # Not a valid NS message
        
        h = SHA256(h || static_ciphertext)
        
        # Check if bound or unbound
        if static_data == bytes(32):
            # Unbound
            alice_static_key = None
            k_payload = k_static
            nonce = 1
        else:
            # Bound - perform ss DH
            alice_static_key = static_data
            ss_shared = DH(context.static_keypair.private_key, alice_static_key)
            keydata = HKDF(chainKey, ss_shared, "", 64)
            chainKey = keydata[0:31]
            k_payload = keydata[32:63]
            nonce = 0
        
        # Decrypt payload
        try:
            payload = DECRYPT(k_payload, nonce, payload_ciphertext, h)
        except AuthenticationError:
            return None
        
        h = SHA256(h || payload_ciphertext)
        
        # Create session
        session = InboundSession()
        session.state = SessionState.ESTABLISHED
        session.created_time = now()
        session.last_activity = now()
        session.remote_ephemeral_key = alice_ephemeral
        session.remote_static_key = alice_static_key
        session.bound = (alice_static_key is not None)
        session.ns_chainkey = chainKey
        session.ns_hash = h
        
        # Extract destination if bound
        if session.bound:
            session.destination = extract_destination_from_payload(payload)
        
        # Process payload
        session.process_payload_blocks(payload)
        
        return session
    
    def send_nsr_reply(self, reply_payload):
        """Send NSR message"""
        # Generate NSR tagset
        tagsetKey = HKDF(self.ns_chainkey, ZEROLEN, "SessionReplyTags", 32)
        nsr_tagset = DH_INITIALIZE(self.ns_chainkey, tagsetKey)
        
        # Get tag
        tag, _ = nsr_tagset.get_next_tag()
        
        # Mix tag into hash
        h = SHA256(self.ns_hash || tag)
        
        # Generate ephemeral key
        self.ephemeral_keypair = generate_elg2_keypair()
        bob_ephemeral = self.ephemeral_keypair.public_key
        elg2_bob_ephemeral = ENCODE_ELG2(bob_ephemeral)
        
        # Mix ephemeral key
        h = SHA256(h || bob_ephemeral)
        
        chainKey = self.ns_chainkey
        
        # ee DH
        ee_shared = DH(self.ephemeral_keypair.private_key, 
                      self.remote_ephemeral_key)
        keydata = HKDF(chainKey, ee_shared, "", 32)
        chainKey = keydata[0:31]
        
        # se DH
        se_shared = DH(context.static_keypair.private_key, 
                      self.remote_ephemeral_key)
        keydata = HKDF(chainKey, se_shared, "", 64)
        chainKey = keydata[0:31]
        k_key_section = keydata[32:63]
        
        # Encrypt key section (empty)
        key_section_ciphertext = ENCRYPT(k_key_section, 0, ZEROLEN, h)
        h = SHA256(h || key_section_ciphertext)
        
        # Split for bidirectional ES
        keydata = HKDF(chainKey, ZEROLEN, "", 64)
        k_ab = keydata[0:31]  # Alice → Bob
        k_ba = keydata[32:63]  # Bob → Alice
        
        # Initialize ES tagsets
        self.inbound_tagset = DH_INITIALIZE(chainKey, k_ab)
        self.outbound_tagset = DH_INITIALIZE(chainKey, k_ba)
        
        # Build reply payload
        payload_data = build_payload_blocks(reply_payload)
        
        # Encrypt payload
        k_nsr = HKDF(k_ba, ZEROLEN, "AttachPayloadKDF", 32)
        payload_ciphertext = ENCRYPT(k_nsr, 0, payload_data, h)
        
        # Assemble NSR
        nsr_message = tag + elg2_bob_ephemeral + key_section_ciphertext + payload_ciphertext
        
        # Send
        send_to_network(self.destination, nsr_message)
        
        # Wait for ES
        self.state = SessionState.AWAITING_ES
        self.last_activity = now()
    
    def on_es_received(self, es_message):
        """Process first ES message"""
        if self.state == SessionState.AWAITING_ES:
            # First ES received, confirms session
            self.state = SessionState.ESTABLISHED
        
        # Process ES message
        self.process_es_message(es_message)
    
    def process_es_message(self, es_message):
        """Decrypt and process ES message"""
        # Extract tag
        tag = es_message[0:8]
        ciphertext = es_message[8:]
        
        # Look up tag
        index = self.inbound_tagset.lookup_tag(tag)
        if index is None:
            raise ValueError("Tag not found")
        
        # Get key
        key = self.inbound_keyratchet.get_key(index)
        
        # Construct nonce
        nonce = construct_nonce(index)
        
        # Decrypt
        try:
            payload = DECRYPT(key, nonce, ciphertext, tag)
        except AuthenticationError:
            raise ValueError("ES MAC verification failed")
        
        # Process blocks
        self.process_payload_blocks(payload)
        
        # Update activity
        self.last_activity = now()
```
### Klasifikace zpráv

**Rozlišování typů zpráv:**

```python
def classify_message(message):
    """Determine message type"""
    
    # Minimum lengths
    if len(message) < 24:
        return None  # Too short
    
    # Check for session tag (8 bytes)
    tag = message[0:8]
    
    # Try ES decryption first (most common)
    session = lookup_session_by_tag(tag)
    if session:
        return ('ES', session)
    
    # Try NSR decryption (tag + Elligator2 key)
    if len(message) >= 72:
        # Check if bytes 8-40 are valid Elligator2
        try:
            nsr_ephemeral = DECODE_ELG2(message[8:40])
            nsr_session = find_pending_nsr_by_tag(tag)
            if nsr_session:
                return ('NSR', nsr_session)
        except:
            pass
    
    # Try NS decryption (starts with Elligator2 key)
    if len(message) >= 96:
        try:
            ns_ephemeral = DECODE_ELG2(message[0:32])
            ns_session = InboundSession.try_decrypt_ns(message)
            if ns_session:
                return ('NS', ns_session)
        except:
            pass
    
    # Check ElGamal/AES (for dual-key compatibility)
    if len(message) >= 514:
        if (len(message) - 2) % 16 == 0:
            # Might be ElGamal NS
            return ('ELGAMAL_NS', None)
        elif len(message) % 16 == 0:
            # Might be ElGamal ES
            return ('ELGAMAL_ES', None)
    
    return None  # Unknown message type
```
### Osvědčené postupy pro správu relací

**Úložiště relace:**

```python
class SessionKeyManager:
    def __init__(self):
        # Outbound sessions (one per destination)
        self.outbound_sessions = {}  # destination -> OutboundSession
        
        # Inbound sessions (multiple per destination during transition)
        self.inbound_sessions = []  # [InboundSession]
        
        # Session tag lookup (fast path for ES messages)
        self.tag_to_session = {}  # tag -> InboundSession
        
        # Limits
        self.max_inbound_sessions = 1000
        self.max_tags_per_session = 160
    
    def get_outbound_session(self, destination):
        """Get or create outbound session"""
        if destination not in self.outbound_sessions:
            session = OutboundSession(destination)
            self.outbound_sessions[destination] = session
        return self.outbound_sessions[destination]
    
    def add_inbound_session(self, session):
        """Add new inbound session"""
        # Check limits
        if len(self.inbound_sessions) >= self.max_inbound_sessions:
            self.expire_oldest_session()
        
        self.inbound_sessions.append(session)
        
        # Add tags to lookup table
        self.register_session_tags(session)
    
    def register_session_tags(self, session):
        """Register session's tags in lookup table"""
        for tag in session.inbound_tagset.get_all_tags():
            self.tag_to_session[tag] = session
    
    def lookup_tag(self, tag):
        """Fast tag lookup"""
        return self.tag_to_session.get(tag)
    
    def expire_sessions(self):
        """Periodic session expiration"""
        now_time = now()
        
        # Expire outbound sessions
        for dest, session in list(self.outbound_sessions.items()):
            if session.idle_time(now_time) > 8 * 60:
                del self.outbound_sessions[dest]
        
        # Expire inbound sessions
        expired = []
        for session in self.inbound_sessions:
            if session.idle_time(now_time) > 10 * 60:
                expired.append(session)
        
        for session in expired:
            self.remove_inbound_session(session)
    
    def remove_inbound_session(self, session):
        """Remove inbound session and clean up tags"""
        self.inbound_sessions.remove(session)
        
        # Remove tags from lookup
        for tag in session.inbound_tagset.get_all_tags():
            if tag in self.tag_to_session:
                del self.tag_to_session[tag]
```
**Správa paměti:**

```python
class TagMemoryManager:
    def __init__(self, max_memory_kb=10240):  # 10 MB default
        self.max_memory = max_memory_kb * 1024
        self.current_memory = 0
        self.max_tags_per_session = 160
        self.min_tags_per_session = 32
    
    def calculate_tag_memory(self, session):
        """Calculate memory used by session tags"""
        tag_count = len(session.inbound_tagset.tags)
        # Each tag: 8 bytes (tag) + 2 bytes (index) + 32 bytes (key, optional)
        # + overhead
        bytes_per_tag = 16 if session.defer_keys else 48
        return tag_count * bytes_per_tag
    
    def check_pressure(self):
        """Check if under memory pressure"""
        return self.current_memory > (self.max_memory * 0.9)
    
    def handle_pressure(self):
        """Reduce memory usage when under pressure"""
        if not self.check_pressure():
            return
        
        # Strategy 1: Reduce look-ahead windows
        for session in all_sessions:
            if session.look_ahead > self.min_tags_per_session:
                session.reduce_look_ahead(self.min_tags_per_session)
        
        # Strategy 2: Trim old tags aggressively
        for session in all_sessions:
            session.inbound_tagset.trim_behind(aggressive=True)
        
        # Strategy 3: Refuse new ratchets
        for session in all_sessions:
            if session.outbound_tagset.should_ratchet():
                session.defer_ratchet = True
        
        # Strategy 4: Expire idle sessions early
        expire_idle_sessions(threshold=5*60)  # 5 min instead of 10
```
### Testovací strategie

**Jednotkové testy:**

```python
def test_x25519_dh():
    """Test X25519 key exchange"""
    alice_sk = GENERATE_PRIVATE()
    alice_pk = DERIVE_PUBLIC(alice_sk)
    
    bob_sk = GENERATE_PRIVATE()
    bob_pk = DERIVE_PUBLIC(bob_sk)
    
    # Both sides compute same shared secret
    alice_shared = DH(alice_sk, bob_pk)
    bob_shared = DH(bob_sk, alice_pk)
    
    assert alice_shared == bob_shared

def test_elligator2_encode_decode():
    """Test Elligator2 roundtrip"""
    sk = GENERATE_PRIVATE_ELG2()
    pk = DERIVE_PUBLIC(sk)
    
    encoded = ENCODE_ELG2(pk)
    decoded = DECODE_ELG2(encoded)
    
    assert decoded == pk

def test_chacha_poly_encrypt_decrypt():
    """Test ChaCha20-Poly1305 AEAD"""
    key = CSRNG(32)
    nonce = construct_nonce(42)
    plaintext = b"Hello, I2P!"
    ad = b"associated_data"
    
    ciphertext = ENCRYPT(key, nonce, plaintext, ad)
    decrypted = DECRYPT(key, nonce, ciphertext, ad)
    
    assert decrypted == plaintext

def test_session_tag_ratchet():
    """Test session tag generation"""
    sessTag_ck = CSRNG(32)
    tagset = SessionTagRatchet(sessTag_ck)
    
    # Generate 100 tags
    tags = [tagset.get_next_tag() for _ in range(100)]
    
    # All tags should be unique
    assert len(set(tags)) == 100
    
    # Each tag should be 8 bytes
    for tag in tags:
        assert len(tag) == 8
```
**Integrační testy:**

```python
def test_ns_nsr_handshake():
    """Test NS/NSR handshake"""
    # Alice creates outbound session
    alice_session = OutboundSession(bob_destination, bound=True)
    
    # Alice sends NS
    ns_message = alice_session.build_ns_message(b"Hello Bob")
    
    # Bob receives NS
    bob_session = InboundSession.try_decrypt_ns(ns_message)
    assert bob_session is not None
    assert bob_session.bound == True
    
    # Bob sends NSR
    nsr_message = bob_session.build_nsr_message(b"Hello Alice")
    
    # Alice receives NSR
    alice_session.on_nsr_received(nsr_message)
    assert alice_session.state == SessionState.ESTABLISHED
    
    # Both should have matching ES tagsets
    # (Cannot directly compare, but can test by sending ES messages)

def test_es_bidirectional():
    """Test ES messages in both directions"""
    # (After NS/NSR handshake)
    
    # Alice sends ES to Bob
    es_alice_to_bob = alice_session.send_es_message(b"Data from Alice")
    
    # Bob receives ES
    bob_session.process_es_message(es_alice_to_bob)
    
    # Bob sends ES to Alice
    es_bob_to_alice = bob_session.send_es_message(b"Data from Bob")
    
    # Alice receives ES
    alice_session.process_es_message(es_bob_to_alice)

def test_dh_ratchet():
    """Test DH ratchet"""
    # (After established session)
    
    # Alice initiates ratchet
    alice_session.initiate_ratchet()
    nextkey_alice = build_nextkey_block(
        flags=0x01,
        key_id=0,
        public_key=alice_new_key
    )
    
    # Send to Bob
    bob_session.process_nextkey_block(nextkey_alice)
    
    # Bob replies
    nextkey_bob = build_nextkey_block(
        flags=0x03,
        key_id=0,
        public_key=bob_new_key
    )
    
    # Send to Alice
    alice_session.process_nextkey_block(nextkey_bob)
    
    # Both should now be using new tagsets
    assert alice_session.outbound_tagset.id == 1
    assert bob_session.inbound_tagset.id == 1
```
**Testovací vektory:**

Implementujte testovací vektory ze specifikace:

1. **Noise IK Handshake**: Použijte standardní testovací vektory pro Noise
2. **HKDF**: Použijte testovací vektory z RFC 5869
3. **ChaCha20-Poly1305**: Použijte testovací vektory z RFC 7539
4. **Elligator2**: Použijte testovací vektory z článku Elligator2 nebo z OBFS4

**Testování interoperability:**

1. **Java I2P**: Otestujte vůči referenční implementaci Java I2P
2. **i2pd**: Otestujte vůči C++ implementaci i2pd
3. **Zachycení paketů**: Použijte disektor Wiresharku (pokud je k dispozici) k ověření formátů zpráv
4. **Napříč implementacemi**: Vytvořte test harness (testovací rámec), který dokáže odesílat/přijímat mezi implementacemi

### Hlediska výkonu

**Generování klíčů:**

Generování klíčů Elligator2 (kryptografická technika pro maskování veřejných klíčů) je výpočetně náročné (50% míra odmítnutí):

```python
class KeyPool:
    """Pre-generate keys in background thread"""
    def __init__(self, pool_size=10):
        self.pool = Queue(maxsize=pool_size)
        self.generator_thread = Thread(target=self.generate_keys, daemon=True)
        self.generator_thread.start()
    
    def generate_keys(self):
        while True:
            if not self.pool.full():
                keypair = generate_elg2_keypair()
                # Also compute encoded form
                encoded = ENCODE_ELG2(keypair.public_key)
                self.pool.put((keypair, encoded))
            else:
                sleep(0.1)
    
    def get_keypair(self):
        try:
            return self.pool.get(timeout=1.0)
        except Empty:
            # Pool exhausted, generate inline
            return generate_elg2_keypair()
```
**Vyhledání tagu (štítku):**

Použijte hashovací tabulky pro O(1) vyhledávání tagů:

```python
class FastTagLookup:
    def __init__(self):
        self.tag_to_session = {}  # Python dict is hash table
    
    def add_tag(self, tag, session, index):
        # 8-byte tag as bytes is hashable
        self.tag_to_session[tag] = (session, index)
    
    def lookup_tag(self, tag):
        return self.tag_to_session.get(tag)
```
**Optimalizace paměti:**

Odložit generování symetrického klíče:

```python
class DeferredKeyRatchet:
    """Only generate keys when needed"""
    def __init__(self, symmKey_ck):
        self.chainKey = symmKey_ck
        self.index = -1
        self.cache = LRUCache(maxsize=32)  # Cache recent keys
    
    def get_key(self, index):
        # Check cache first
        if index in self.cache:
            return self.cache[index]
        
        # Generate keys up to index
        while self.index < index:
            self.index += 1
            keydata = HKDF(self.chainKey, ZEROLEN, "SymmetricRatchet", 64)
            self.chainKey = keydata[0:31]
            
            if self.index == index:
                key = keydata[32:63]
                self.cache[index] = key
                return key
```
**Dávkové zpracování:**

Zpracujte více zpráv dávkově:

```python
def process_message_batch(messages):
    """Process multiple messages efficiently"""
    results = []
    
    # Group by type
    ns_messages = []
    nsr_messages = []
    es_messages = []
    
    for msg in messages:
        msg_type = classify_message(msg)
        if msg_type[0] == 'NS':
            ns_messages.append(msg)
        elif msg_type[0] == 'NSR':
            nsr_messages.append(msg)
        elif msg_type[0] == 'ES':
            es_messages.append(msg)
    
    # Process in batches
    # ES messages are most common, process first
    for msg in es_messages:
        results.append(process_es_message(msg))
    
    for msg in nsr_messages:
        results.append(process_nsr_message(msg))
    
    for msg in ns_messages:
        results.append(process_ns_message(msg))
    
    return results
```
---

## Bezpečnostní hlediska

### Model hrozeb

**Schopnosti útočníka:**

1. **Pasivní pozorovatel**: Může sledovat veškerý síťový provoz
2. **Aktivní útočník**: Může vkládat, upravovat, zahazovat a opakovat (replay) zprávy
3. **Kompromitovaný uzel**: Může kompromitovat router nebo destination (cílový identifikátor v I2P)
4. **Analýza provozu**: Může provádět statistickou analýzu vzorců provozu

**Bezpečnostní cíle:**

1. **Důvěrnost**: Obsah zpráv skrytý před pozorovatelem
2. **Autentizace**: Identita odesílatele ověřena (u vázaných relací)
3. **Dopředné utajení**: Minulé zprávy zůstávají tajné i při kompromitaci klíčů
4. **Prevence replay útoků**: Nelze zopakovat staré zprávy
5. **Obfuskace provozu**: Navazování spojení nerozlišitelné od náhodných dat

### Kryptografické předpoklady

**Předpoklady o výpočetní obtížnosti:**

1. **X25519 CDH**: Výpočetní problém Diffie-Hellman je na křivce Curve25519 výpočetně těžký
2. **ChaCha20 PRF**: ChaCha20 je pseudonáhodná funkce
3. **Poly1305 MAC**: Poly1305 je nepodvrzitelný při útoku s volenou zprávou
4. **SHA-256 CR**: SHA-256 je odolná vůči kolizím
5. **HKDF Security**: HKDF extrahuje a rozšiřuje rovnoměrně rozdělené klíče

**Úrovně zabezpečení:**

- **X25519**: ~128bitová bezpečnost (řád křivky 2^252)
- **ChaCha20**: 256bitové klíče, 256bitová bezpečnost
- **Poly1305**: 128bitová bezpečnost (pravděpodobnost kolize)
- **SHA-256**: 128bitová odolnost vůči kolizím, 256bitová odolnost vůči předobrazu

### Správa klíčů

**Generování klíčů:**

```python
# CRITICAL: Use cryptographically secure RNG
def CSRNG(length):
    # GOOD: os.urandom, secrets.token_bytes (Python)
    # GOOD: /dev/urandom (Linux)
    # GOOD: BCryptGenRandom (Windows)
    # BAD: random.random(), Math.random() (NOT cryptographically secure)
    return os.urandom(length)

# CRITICAL: Validate keys
def validate_x25519_key(pubkey):
    # Check for weak keys (all zeros, small order points)
    if pubkey == bytes(32):
        raise WeakKeyError("All-zero public key")
    
    # Perform DH to check for weak shared secrets
    test_shared = DH(test_private_key, pubkey)
    if test_shared == bytes(32):
        raise WeakKeyError("Results in zero shared secret")
```
**Úložiště klíčů:**

```python
# CRITICAL: Protect private keys
class SecureKeyStorage:
    def __init__(self):
        # Store in memory with protection
        self.keys = {}
        
        # Option 1: Memory locking (prevent swapping to disk)
        # mlock(self.keys)
        
        # Option 2: Encrypted storage
        # self.encryption_key = derive_from_password()
    
    def store_key(self, key_id, private_key):
        # Option: Encrypt before storage
        # encrypted = encrypt(private_key, self.encryption_key)
        # self.keys[key_id] = encrypted
        self.keys[key_id] = private_key
    
    def delete_key(self, key_id):
        # Securely wipe memory
        if key_id in self.keys:
            key = self.keys[key_id]
            # Overwrite with zeros before deletion
            for i in range(len(key)):
                key[i] = 0
            del self.keys[key_id]
```
**Rotace klíčů:**

```python
# CRITICAL: Rotate keys regularly
class KeyRotationPolicy:
    def __init__(self):
        self.max_messages_per_tagset = 4096  # Ratchet before 65535
        self.max_tagset_age = 10 * 60       # 10 minutes
        self.max_session_age = 60 * 60      # 1 hour
    
    def should_ratchet(self, tagset):
        return (tagset.messages_sent >= self.max_messages_per_tagset or
                tagset.age() >= self.max_tagset_age)
    
    def should_replace_session(self, session):
        return session.age() >= self.max_session_age
```
### Opatření ke zmírnění útoků

### Opatření proti replay útokům

**Ověření data a času:**

```python
MAX_CLOCK_SKEW_PAST = 5 * 60
MAX_CLOCK_SKEW_FUTURE = 2 * 60

def validate_datetime(timestamp):
    now = int(time.time())
    age = now - timestamp
    
    if age < -MAX_CLOCK_SKEW_FUTURE:
        raise ReplayError("Timestamp too far in future")
    
    if age > MAX_CLOCK_SKEW_PAST:
        raise ReplayError("Timestamp too old")
    
    return True
```
**Bloomův filtr pro zprávy NS:**

```python
class ReplayFilter:
    def __init__(self, capacity=100000, error_rate=0.001, duration=5*60):
        self.bloom = BloomFilter(capacity=capacity, error_rate=error_rate)
        self.duration = duration
        self.entries = []  # (timestamp, ephemeral_key)
    
    def check_replay(self, ephemeral_key, timestamp):
        # Validate timestamp
        if not validate_datetime(timestamp):
            return False
        
        # Check Bloom filter
        if ephemeral_key in self.bloom:
            # Potential replay (or false positive)
            # Check exact match in entries
            for ts, key in self.entries:
                if key == ephemeral_key:
                    return False  # Definite replay
        
        # Add to filter
        self.bloom.add(ephemeral_key)
        self.entries.append((timestamp, ephemeral_key))
        
        # Expire old entries
        self.expire_old_entries()
        
        return True
    
    def expire_old_entries(self):
        now = int(time.time())
        self.entries = [(ts, key) for ts, key in self.entries
                       if now - ts < self.duration]
```
**Jednorázové použití Session Tag (značka relace):**

```python
def process_session_tag(tag):
    # Look up tag
    entry = tagset.lookup_tag(tag)
    if entry is None:
        raise ValueError("Invalid session tag")
    
    # CRITICAL: Remove tag immediately (one-time use)
    tagset.remove_tag(tag)
    
    # Use associated key
    return entry.key, entry.index
```
### Opatření proti Key Compromise Impersonation (KCI; vydávání se za protějšek po kompromitaci klíče)

**Problém**: Autentizace zpráv NS je zranitelná vůči KCI (napodobení po kompromitaci klíče) (Úroveň autentizace 1)

**Zmírnění**:

1. Přejděte na NSR (úroveň autentizace 2) co nejrychleji
2. Nevěřte NS payloadu při bezpečnostně kritických operacích
3. Před provedením nevratných akcí vyčkejte na potvrzení NSR

```python
def process_ns_message(ns_message):
    # NS authenticated at Level 1 (KCI vulnerable)
    # Do NOT perform security-critical operations yet
    
    # Extract sender's static key
    sender_key = ns_message.static_key
    
    # Mark session as pending Level 2 authentication
    session.auth_level = 1
    session.sender_key = sender_key
    
    # Send NSR
    send_nsr_reply(session)

def process_first_es_message(es_message):
    # Now we have Level 2 authentication (KCI resistant)
    session.auth_level = 2
    
    # Safe to perform security-critical operations
    process_security_critical_operation(es_message)
```
### Opatření proti útokům typu odmítnutí služby (DoS)

**Ochrana proti zahlcení NS (systém názvů):**

```python
class NSFloodProtection:
    def __init__(self):
        self.ns_count = defaultdict(int)  # source -> count
        self.ns_timestamps = defaultdict(list)  # source -> [timestamps]
        
        self.max_ns_per_source = 5
        self.rate_window = 10  # seconds
        self.max_concurrent_ns = 100
    
    def check_ns_allowed(self, source):
        # Global limit
        total_pending = sum(self.ns_count.values())
        if total_pending >= self.max_concurrent_ns:
            return False
        
        # Per-source rate limit
        now = time.time()
        timestamps = self.ns_timestamps[source]
        
        # Remove old timestamps
        timestamps = [ts for ts in timestamps if now - ts < self.rate_window]
        self.ns_timestamps[source] = timestamps
        
        # Check rate
        if len(timestamps) >= self.max_ns_per_source:
            return False
        
        # Allow NS
        timestamps.append(now)
        self.ns_count[source] += 1
        return True
    
    def on_session_established(self, source):
        # Decrease pending count
        if self.ns_count[source] > 0:
            self.ns_count[source] -= 1
```
**Limity ukládání značek:**

```python
class TagStorageLimit:
    def __init__(self, max_tags=1000000):
        self.max_tags = max_tags
        self.current_tags = 0
    
    def can_create_session(self, look_ahead):
        if self.current_tags + look_ahead > self.max_tags:
            return False
        return True
    
    def add_tags(self, count):
        self.current_tags += count
    
    def remove_tags(self, count):
        self.current_tags -= count
```
**Adaptivní správa zdrojů:**

```python
class AdaptiveResourceManager:
    def __init__(self):
        self.load_level = 0  # 0 = low, 1 = medium, 2 = high, 3 = critical
    
    def adjust_parameters(self):
        if self.load_level == 0:
            # Normal operation
            return {
                'max_look_ahead': 160,
                'max_sessions': 1000,
                'session_timeout': 10 * 60
            }
        
        elif self.load_level == 1:
            # Moderate load
            return {
                'max_look_ahead': 80,
                'max_sessions': 800,
                'session_timeout': 8 * 60
            }
        
        elif self.load_level == 2:
            # High load
            return {
                'max_look_ahead': 32,
                'max_sessions': 500,
                'session_timeout': 5 * 60
            }
        
        else:  # load_level == 3
            # Critical load
            return {
                'max_look_ahead': 16,
                'max_sessions': 200,
                'session_timeout': 3 * 60
            }
```
### Odolnost vůči analýze provozu

**Kódování Elligator2:**

Zajišťuje, že zprávy handshake (navázání spojení) jsou nerozlišitelné od náhodných dat:

```python
# NS and NSR start with Elligator2-encoded ephemeral keys
# Observer cannot distinguish from random 32-byte string
```
**Strategie výplně:**

```python
# Resist message size fingerprinting
def add_padding(payload, strategy='random'):
    if strategy == 'random':
        # Random padding 0-15 bytes
        size = random.randint(0, 15)
    
    elif strategy == 'round':
        # Round to next 64-byte boundary
        target = ((len(payload) + 63) // 64) * 64
        size = target - len(payload) - 3  # -3 for block header
    
    elif strategy == 'fixed':
        # Always 1KB messages
        size = 1024 - len(payload) - 3
    
    return build_padding_block(size)
```
**Časové útoky:**

```python
# CRITICAL: Use constant-time operations
def constant_time_compare(a, b):
    """Constant-time byte string comparison"""
    if len(a) != len(b):
        return False
    
    result = 0
    for x, y in zip(a, b):
        result |= x ^ y
    
    return result == 0

# CRITICAL: Constant-time MAC verification
def verify_mac(computed_mac, received_mac):
    if not constant_time_compare(computed_mac, received_mac):
        # Always take same time regardless of where comparison fails
        raise AuthenticationError("MAC verification failed")
```
### Úskalí implementace

**Časté chyby:**

1. **Znovupoužití nonce (jednorázové hodnoty)**: NIKDY znovu nepoužívejte dvojice (key, nonce)
   ```python
   # BAD: Reusing nonce with same key
   ciphertext1 = ENCRYPT(key, nonce, plaintext1, ad1)
   ciphertext2 = ENCRYPT(key, nonce, plaintext2, ad2)  # CATASTROPHIC

# DOBRÉ: Jedinečná nonce (jednorázová hodnota) pro každou zprávu    ciphertext1 = ENCRYPT(key, nonce1, plaintext1, ad1)    ciphertext2 = ENCRYPT(key, nonce2, plaintext2, ad2)

   ```

2. **Ephemeral Key Reuse**: Generate fresh ephemeral key for each NS/NSR
   ```python
# ŠPATNĚ: Opětovné použití efemérního klíče    ephemeral_key = generate_elg2_keypair()    send_ns_message(ephemeral_key)    send_ns_message(ephemeral_key)  # ŠPATNĚ

# SPRÁVNĚ: Nový klíč pro každou zprávu    send_ns_message(generate_elg2_keypair())    send_ns_message(generate_elg2_keypair())

   ```

3. **Weak RNG**: Use cryptographically secure random number generator
   ```python
# ŠPATNĚ: Nekryptografický generátor náhodných čísel (RNG)    import random    key = bytes([random.randint(0, 255) for _ in range(32)])  # NEZABEZPEČENÉ

# SPRÁVNĚ: Kryptograficky bezpečný generátor náhodných čísel    import os    key = os.urandom(32)

   ```

4. **Timing Attacks**: Use constant-time comparisons
   ```python
# ŠPATNĚ: Porovnání s předčasným ukončením    if computed_mac == received_mac:  # Časovací únik

       pass
   
# SPRÁVNĚ: Porovnání v konstantním čase    if constant_time_compare(computed_mac, received_mac):

       pass
   ```

5. **Incomplete MAC Verification**: Always verify before using data
   ```python
# ŠPATNĚ: Dešifrování před ověřením    plaintext = chacha20_decrypt(key, nonce, ciphertext)    mac_ok = verify_mac(mac, plaintext)  # PŘÍLIŠ POZDĚ    if not mac_ok:

       return error
   
# SPRÁVNĚ: AEAD ověřuje před dešifrováním    try:

       plaintext = DECRYPT(key, nonce, ciphertext, ad)  # Verifies MAC first
except AuthenticationError:

       return error
   ```

6. **Key Deletion**: Securely wipe keys from memory
   ```python
# ŠPATNĚ: Jednoduché smazání    del private_key  # Stále v paměti

# SPRÁVNĚ: Přepsat před smazáním    for i in range(len(private_key)):

       private_key[i] = 0
del private_key

   ```

### Security Audits

**Recommended Audits:**

1. **Cryptographic Review**: Expert review of KDF chains and DH operations
2. **Implementation Audit**: Code review for timing attacks, key management, RNG usage
3. **Protocol Analysis**: Formal verification of handshake security properties
4. **Side-Channel Analysis**: Timing, power, and cache attacks
5. **Fuzzing**: Random input testing for parser robustness

**Test Cases:**

```python
# Bezpečnostně kritické testovací případy

def test_nonce_uniqueness():

    """Ensure nonces are never reused"""
    nonces = set()
    for i in range(10000):
        nonce = construct_nonce(i)
        assert nonce not in nonces
        nonces.add(nonce)

def test_key_isolation():

    """Ensure sessions don't share keys"""
    session1 = create_session(destination1)
    session2 = create_session(destination2)
    
    assert session1.key != session2.key

def test_replay_prevention():

    """Ensure replay attacks are detected"""
    ns_message = create_ns_message()
    
    # First delivery succeeds
    assert process_ns_message(ns_message) == True
    
    # Replay fails
    assert process_ns_message(ns_message) == False

def test_mac_verification():

    """Ensure MAC verification is enforced"""
    key = CSRNG(32)
    nonce = construct_nonce(0)
    plaintext = b"test"
    ad = b"test_ad"
    
    ciphertext = ENCRYPT(key, nonce, plaintext, ad)
    
    # Correct MAC verifies
    assert DECRYPT(key, nonce, ciphertext, ad) == plaintext
    
    # Corrupted MAC fails
    corrupted = ciphertext[:-1] + bytes([ciphertext[-1] ^ 0xFF])
    with pytest.raises(AuthenticationError):
        DECRYPT(key, nonce, corrupted, ad)
```

---

## Configuration and Deployment

### I2CP Configuration

**Enable ECIES Encryption:**

```properties
# Pouze ECIES (Elliptic Curve Integrated Encryption Scheme – integrované šifrovací schéma na eliptických křivkách; doporučeno pro nová nasazení)

i2cp.leaseSetEncType=4

# Dvouklíčový (ECIES + ElGamal pro kompatibilitu)

i2cp.leaseSetEncType=4,0

# Pouze ElGamal (zastaralé, nedoporučuje se)

i2cp.leaseSetEncType=0

```

**LeaseSet Type:**

```properties
# Standardní LS2 (nejběžnější)

i2cp.leaseSetType=3

# Šifrované LS2 (zaslepené destinace)

i2cp.leaseSetType=5

# Meta LS2 (více destinací)

i2cp.leaseSetType=7

```

**Additional Options:**

```properties
# Statický klíč pro ECIES (schéma integrovaného šifrování na eliptických křivkách) (volitelný, automaticky se vygeneruje, pokud není uveden)

# 32bajtový veřejný klíč X25519, zakódovaný v Base64

i2cp.leaseSetPrivateKey=<base64-encoded-key>

# Typ podpisu (pro LeaseSet)

i2cp.leaseSetSigningPrivateKey=<base64-encoded-key> i2cp.leaseSetSigningType=7  # Ed25519

```

### Java I2P Configuration

**router.config:**

```properties
# ECIES mezi routery

i2p.router.useECIES=true

```

**Build Properties:**

```java
// Pro klienty I2CP (Java) Properties props = new Properties(); props.setProperty("i2cp.leaseSetEncType", "4"); props.setProperty("i2cp.leaseSetType", "3");

I2PSession session = i2pClient.createSession(props);

```

### i2pd Configuration

**i2pd.conf:**

```ini
[limity]

# Paměťový limit pro relace ECIES (Elliptic Curve Integrated Encryption Scheme – šifrovací schéma využívající eliptické křivky)

ecies.memory = 128M

[ecies]

# Povolit ECIES (integrované šifrování eliptických křivek)

enabled = true

# Pouze ECIES (Elliptic Curve Integrated Encryption Scheme) nebo dvouklíčové

compatibility = true  # true = dual-key (režim se dvěma klíči), false = pouze ECIES

```

**Tunnels Configuration:**

```ini
[my-service] type = http host = 127.0.0.1 port = 8080 keys = my-service-keys.dat

# Pouze ECIES (schéma integrovaného šifrování s eliptickými křivkami)

ecies = true

```

### Compatibility Matrix

**Router Version Support:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">ECIES Support</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">LS2 Support</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Dual-Key</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">&lt; 0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">❌ No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">❌ No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">N/A</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy only</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.38-0.9.45</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">❌ No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">N/A</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LS2 only</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.46-0.9.50</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Initial ECIES</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.5.0+</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.0.0+</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
  </tbody>
</table>

**Destination Compatibility:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Destination Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Can Connect To</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-only</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-only, Dual-key</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Requires 0.9.46+ routers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Dual-key</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Maximum compatibility</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal-only</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal-only, Dual-key</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy</td>
    </tr>
  </tbody>
</table>

**FloodFill Requirements:**

- **ECIES-only destinations**: Require majority of floodfills on 0.9.46+ for encrypted lookups
- **Dual-key destinations**: Work with any floodfill version
- **Current status**: Near 100% floodfill adoption as of 2025

### Migration Guide

**Migrating from ElGamal to ECIES:**

**Step 1: Enable Dual-Key Mode**

```properties
# Přidat ECIES při zachování ElGamalu

i2cp.leaseSetEncType=4,0

```

**Step 2: Monitor Connections**

```bash
# Zkontrolujte typy připojení

i2prouter.exe status

# nebo

http://127.0.0.1:7657/peers

```

**Step 3: Switch to ECIES-Only (after testing)**

```properties
# Odstranit ElGamal

i2cp.leaseSetEncType=4

```

**Step 4: Restart Application**

```bash
# Restartujte I2P router nebo aplikaci

systemctl restart i2p

# nebo

i2prouter.exe restart

```

**Rollback Plan:**

```properties
# V případě problémů se vraťte k režimu pouze ElGamal

i2cp.leaseSetEncType=0

```

### Performance Tuning

**Session Limits:**

```properties
# Maximální počet příchozích relací

i2p.router.maxInboundSessions=1000

# Maximální počet odchozích relací

i2p.router.maxOutboundSessions=1000

# Časový limit relace (sekundy)

i2p.router.sessionTimeout=600

```

**Memory Limits:**

```properties
# Limit pro ukládání značek (KB)

i2p.ecies.maxTagMemory=10240  # 10 MB

# Okno dopředného náhledu

i2p.ecies.tagLookAhead=160 i2p.ecies.tagLookAheadMin=32

```

**Ratchet Policy:**

```properties
# Zprávy před ratchet (kryptografický mechanismus průběžné obměny klíčů)

i2p.ecies.ratchetThreshold=4096

# Čas do ratchet (mechanismus postupné obměny klíčů) (sekundy)

i2p.ecies.ratchetTimeout=600  # 10 minut

```

### Monitoring and Debugging

**Logging:**

```properties
# Povolit ladicí protokolování pro ECIES (integrované šifrovací schéma založené na eliptických křivkách)

logger.i2p.router.transport.ecies=DEBUG

```

**Metrics:**

Monitor these metrics:

1. **NS Success Rate**: Percentage of NS messages receiving NSR
2. **Session Establishment Time**: Time from NS to first ES
3. **Tag Storage Usage**: Current memory usage for tags
4. **Ratchet Frequency**: How often sessions ratchet
5. **Session Lifetime**: Average session duration

**Common Issues:**

1. **NS Timeout**: No NSR received
   - Check destination is online
   - Check floodfill availability
   - Verify LeaseSet published correctly

2. **High Memory Usage**: Too many tags stored
   - Reduce look-ahead window
   - Decrease session timeout
   - Implement aggressive expiration

3. **Frequent Ratchets**: Sessions ratcheting too often
   - Increase ratchet threshold
   - Check for retransmissions

4. **Session Failures**: ES messages failing to decrypt
   - Verify tag synchronization
   - Check for replay attacks
   - Validate nonce construction

---

## References

### Specifications

1. **ECIES Proposal**: [Proposal 144](/proposals/144-ecies-x25519-aead-ratchet/)
2. **I2NP**: [I2NP Specification](/docs/specs/i2np/)
3. **Common Structures**: [Common Structures Specification](/docs/specs/common-structures/)
4. **NTCP2**: [NTCP2 Specification](/docs/specs/ntcp2/)
5. **SSU2**: [SSU2 Specification](/docs/specs/ssu2/)
6. **I2CP**: [I2CP Specification](/docs/specs/i2cp/)
7. **ElGamal/AES+SessionTags**: [ElGamal/AES Specification](/docs/legacy/elgamal-aes/)

### Cryptographic Standards

1. **Noise Protocol Framework**: [Noise Specification](https://noiseprotocol.org/noise.html) (Revision 34, 2018-07-11)
2. **Signal Double Ratchet**: [Signal Specification](https://signal.org/docs/specifications/doubleratchet/)
3. **RFC 7748**: [Elliptic Curves for Security (X25519)](https://tools.ietf.org/html/rfc7748)
4. **RFC 7539**: [ChaCha20 and Poly1305 for IETF Protocols](https://tools.ietf.org/html/rfc7539)
5. **RFC 5869**: [HKDF (HMAC-based Key Derivation Function)](https://tools.ietf.org/html/rfc5869)
6. **RFC 2104**: [HMAC: Keyed-Hashing for Message Authentication](https://tools.ietf.org/html/rfc2104)
7. **Elligator2**: [Elligator Paper](https://elligator.cr.yp.to/elligator-20130828.pdf)

### Implementation Resources

1. **Java I2P**: [i2p.i2p Repository](https://github.com/i2p/i2p.i2p)
2. **i2pd (C++)**: [i2pd Repository](https://github.com/PurpleI2P/i2pd)
3. **OBFS4 (Elligator2)**: [obfs4proxy Repository](https://gitlab.com/yawning/obfs4)

### Additional Information

1. **I2P Website**: [/](/)
2. **I2P Forum**: [https://i2pforum.net](https://i2pforum.net)
3. **I2P Wiki**: [https://wiki.i2p-projekt.de](https://wiki.i2p-projekt.de)

---

## Appendix A: KDF Summary

**All KDF Operations in ECIES:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Input</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Info String</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Output</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NS Initial ChainKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">protocol_name</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">(none - SHA256)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">h, chainKey</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NS Static Key Section</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, es_shared</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">""</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, k</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NS Payload Section (bound)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, ss_shared</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">""</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, k</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR Tagset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"SessionReplyTags"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">tagsetKey</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR ee DH</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, ee_shared</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">""</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR se DH</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, se_shared</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">""</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, k</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR Split</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">""</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">k_ab, k_ba</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR Payload</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">k_ba</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"AttachPayloadKDF"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">k_nsr</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DH Initialize</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">rootKey, k</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"KDFDHRatchetStep"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">nextRootKey, chainKey</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Tag and Key Chain Keys</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"TagAndKeyGenKeys"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">sessTag_ck, symmKey_ck</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Session Tag Init</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">sessTag_ck</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"STInitialization"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, CONSTANT</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Session Tag Gen</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, CONSTANT</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"SessionTagKeyGen"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, tag</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Symmetric Key Gen</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"SymmetricRatchet"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DH Ratchet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">sharedSecret</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"XDHRatchetTagSet"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">tagsetKey</td>
    </tr>
  </tbody>
</table>

---

## Appendix B: Message Size Calculator

**Calculate message sizes for capacity planning:**

```python
def calculate_ns_size(payload_size, bound=True):

    """Calculate New Session message size"""
    ephemeral_key = 32
    static_section = 32 + 16  # encrypted + MAC
    payload_encrypted = payload_size + 16  # + MAC
    
    return ephemeral_key + static_section + payload_encrypted

def calculate_nsr_size(payload_size):

    """Calculate New Session Reply message size"""
    tag = 8
    ephemeral_key = 32
    key_section_mac = 16
    payload_encrypted = payload_size + 16  # + MAC
    
    return tag + ephemeral_key + key_section_mac + payload_encrypted

def calculate_es_size(payload_size):

    """Calculate Existing Session message size"""
    tag = 8
    payload_encrypted = payload_size + 16  # + MAC
    
    return tag + payload_encrypted

# Příklady

print("NS (bound, 1KB payload):", calculate_ns_size(1024, bound=True), "bytes")

# Výstup: 1120 bajtů

print("NSR (1KB užitečných dat):", calculate_nsr_size(1024), "bajtů")

# Výstup: 1096 bajtů

print("ES (1 kB užitečných dat):", calculate_es_size(1024), "bajtů")

# Výstup: 1048 bajtů

```

---

## Appendix C: Glossary

**AEAD**: Authenticated Encryption with Associated Data - encryption mode that provides both confidentiality and authenticity

**Authentication Level**: Noise protocol security property indicating strength of sender identity verification

**Binding**: Association of a session with a specific far-end destination

**ChaCha20**: Stream cipher designed by Daniel J. Bernstein

**ChainKey**: Cryptographic key used in HKDF chains to derive subsequent keys

**Confidentiality Level**: Noise protocol security property indicating strength of forward secrecy

**DH**: Diffie-Hellman key agreement protocol

**Elligator2**: Encoding technique to make elliptic curve points indistinguishable from random

**Ephemeral Key**: Short-lived key used only for a single handshake

**ES**: Existing Session message (used after handshake completion)

**Forward Secrecy**: Property ensuring past communications remain secure if keys are compromised

**Garlic Clove**: I2NP message container for end-to-end delivery

**HKDF**: HMAC-based Key Derivation Function

**IK Pattern**: Noise handshake pattern where initiator sends static key immediately

**KCI**: Key Compromise Impersonation attack

**KDF**: Key Derivation Function - cryptographic function for generating keys from other keys

**LeaseSet**: I2P structure containing a destination's public keys and tunnel information

**LS2**: LeaseSet version 2 with encryption type support

**MAC**: Message Authentication Code - cryptographic checksum proving authenticity

**MixHash**: Noise protocol function for maintaining running hash transcript

**NS**: New Session message (initiates new session)

**NSR**: New Session Reply message (response to NS)

**Nonce**: Number used once - ensures unique encryption even with same key

**Pairing**: Linking an inbound session with an outbound session for bidirectional communication

**Poly1305**: Message authentication code designed by Daniel J. Bernstein

**Ratchet**: Cryptographic mechanism for deriving sequential keys

**Session Tag**: 8-byte one-time identifier for existing session messages

**Static Key**: Long-term key associated with a destination's identity

**Tag Set**: Collection of session tags derived from a common root

**X25519**: Elliptic curve Diffie-Hellman key agreement using Curve25519

---