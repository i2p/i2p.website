---
title: "Transport NTCP2"
description: "TCP transport založený na Noise (kryptografickém protokolu Noise) pro spojení router-to-router"
slug: "ntcp2"
lastUpdated: "2025-10"
accurateFor: "0.9.66"
type: docs
---

## Přehled

NTCP2 nahrazuje původní transport NTCP handshakem založeným na Noise (kryptografickém rámci pro handshake), který odolává rozpoznávání provozu podle otisků, šifruje délková pole a podporuje moderní sady šifer. Routery mohou provozovat NTCP2 vedle SSU2 jako dva povinné transportní protokoly v síti I2P. NTCP (verze 1) byl v 0.9.40 (květen 2019) označen jako zastaralý a v 0.9.50 (květen 2021) zcela odstraněn.

## Rámec protokolu Noise

NTCP2 používá Noise Protocol Framework (rámec protokolu Noise) [Revize 33, 2017-10-04](https://noiseprotocol.org/noise.html) s rozšířeními specifickými pro I2P:

- **Vzor**: `Noise_XK_25519_ChaChaPoly_SHA256`
- **Rozšířený identifikátor**: `Noise_XKaesobfse+hs2+hs3_25519_ChaChaPoly_SHA256` (pro inicializaci KDF)
- **Funkce DH**: X25519 (RFC 7748) - 32bajtové klíče, kódování little-endian
- **Šifra**: AEAD_CHACHA20_POLY1305 (RFC 7539/RFC 8439)
  - 12bajtový nonce (jednorázová hodnota): první 4 bajty jsou nula, posledních 8 bajtů je čítač (little-endian)
  - Maximální hodnota nonce: 2^64 - 2 (spojení se musí ukončit před dosažením 2^64 - 1)
- **Hašovací funkce**: SHA-256 (32bajtový výstup)
- **MAC**: Poly1305 (16bajtový autentizační tag)

### Rozšíření specifická pro I2P

1. **Obfuskace AES**: Efemerní klíče šifrované pomocí AES-256-CBC s využitím hashe routeru Boba a publikovaného IV (inicializačního vektoru)
2. **Náhodný padding**: Padding v otevřeném textu ve zprávách 1-2 (autentizovaný), padding AEAD (ověřené šifrování s připojenými daty) ve zprávách 3+ (šifrovaný)
3. **Zakrytí délky pomocí SipHash-2-4**: Dvoubajtové délky rámců jsou XORovány s výstupem SipHash
4. **Struktura rámců**: Rámce s délkovým prefixem pro datovou fázi (kompatibilita se streamováním přes TCP)
5. **Blokově strukturovaná uživatelská data**: Strukturovaný datový formát s typovanými bloky

## Postup navázání spojení

```
Alice (Initiator)             Bob (Responder)
SessionRequest  ──────────────────────►
                ◄────────────────────── SessionCreated
SessionConfirmed ──────────────────────►
```
### Třízprávový handshake

1. **SessionRequest** - Aličin zamaskovaný efemérní klíč, volby, nápovědy k paddingu (vycpávce)
2. **SessionCreated** - Bobův zamaskovaný efemérní klíč, šifrované volby, padding
3. **SessionConfirmed** - Aličin šifrovaný statický klíč a RouterInfo (dva AEAD rámce; ověřené šifrování s přidruženými daty)

### Vzory zpráv Noise (kryptografický rámec)

```
XK(s, rs):           Authentication   Confidentiality
  <- s               (Bob's static key known in advance)
  -> e, es                  0                2
  <- e, ee                  2                1
  -> s, se                  2                5
  <-                        2                5
```
**Úrovně autentizace:** - 0: Bez autentizace (mohl to poslat kdokoli) - 2: Autentizace odesílatele odolná vůči útoku typu key-compromise impersonation (KCI, podvržení po kompromitaci klíče)

**Úrovně důvěrnosti:** - 1: Efemérní příjemce (dopředné utajení, bez autentizace příjemce) - 2: Známý příjemce, dopředné utajení pouze při kompromitaci odesílatele - 5: Silné dopředné utajení (efemérní-efemérní + efemérní-statický DH)

## Specifikace zpráv

### Notace klíčů

- `RH_A` = Router Hash pro Alici (32 bajtů, SHA-256)
- `RH_B` = Router Hash pro Boba (32 bajtů, SHA-256)
- `||` = operátor zřetězení
- `byte(n)` = jeden bajt s hodnotou n
- Všechny vícebajtové celočíselné hodnoty jsou **big-endian** (pořadí bajtů od nejvýznamnějšího), není-li uvedeno jinak
- Klíče X25519 jsou **little-endian** (pořadí bajtů od nejméně významného) (32 bajtů)

### Autentizované šifrování (ChaCha20-Poly1305)

**Šifrovací funkce:**

```
AEAD_ChaCha20_Poly1305(key, nonce, associatedData, plaintext)
  → (ciphertext || MAC)
```
**Parametry:** - `key`: 32bajtový šifrovací klíč z KDF - `nonce`: 12 bajtů (4 nulové bajty + 8bajtový čítač, little-endian (nejméně významný bajt první)) - `associatedData`: 32bajtový hash ve fázi handshake; ve fázi dat nulové délky - `plaintext`: Data k zašifrování (0+ bajtů)

**Výstup:** - Šifrotext: Stejná délka jako otevřený text - MAC: 16 bajtů (autentizační tag Poly1305)

**Správa nonce:** - Čítač začíná na 0 u každé instance šifry - Zvyšuje se pro každou operaci AEAD v daném směru - Samostatné čítače pro Alice→Bob a Bob→Alice v datové fázi - Spojení se musí ukončit dříve, než čítač dosáhne 2^64 - 1

## Zpráva 1: SessionRequest (žádost o relaci)

Alice navazuje spojení s Bobem.

**Operace Noise**: `e, es` (generování a výměna efemérních klíčů)

### Surový formát

```
+----+----+----+----+----+----+----+----+
|                                       |
+    AES-256-CBC Encrypted X (32B)      +
|    Key: RH_B, IV: Bob's published IV  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+    ChaChaPoly Frame (48 bytes)        +
|    Plaintext: 32B (X + options)       |
+    k from KDF-1, n=0, ad=h            +
|                                       |
+----+----+----+----+----+----+----+----+
|    Cleartext Padding (optional)       |
+    Length specified in options         +
|    0 to 65535 - 80 bytes              |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
**Omezení velikosti:** - Minimum: 80 bajtů (32 AES + 48 AEAD) - Maximum: celkem 65535 bajtů - **Zvláštní případ**: Max 287 bajtů při připojení k adresám "NTCP" (detekce verze)

### Dešifrovaný obsah

```
+----+----+----+----+----+----+----+----+
|                                       |
+    X (Alice ephemeral public key)     +
|    32 bytes, X25519, little-endian    |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|           Options Block               |
+             (16 bytes)                +
|                                       |
+----+----+----+----+----+----+----+----+
|    Cleartext Padding (optional)       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
### Blok voleb (16 bajtů, big-endian (uspořádání s nejvýznamnějším bajtem jako prvním))

```
+----+----+----+----+----+----+----+----+
| id | ver|  padLen | m3p2len | Rsvd(0) |
+----+----+----+----+----+----+----+----+
|        tsA        |   Reserved (0)    |
+----+----+----+----+----+----+----+----+

id      : 1 byte  - Network ID (2 for mainnet, 16-254 for testnets)
ver     : 1 byte  - Protocol version (currently 2)
padLen  : 2 bytes - Padding length in this message (0-65455)
m3p2len : 2 bytes - Length of SessionConfirmed part 2 frame
Rsvd    : 2 bytes - Reserved, set to 0
tsA     : 4 bytes - Unix timestamp (seconds since epoch)
Reserved: 4 bytes - Reserved, set to 0
```
**Kritická pole:** - **Network ID** (od verze 0.9.42): Rychlé odmítnutí spojení napříč sítěmi - **m3p2len**: Přesná velikost části 2 zprávy 3 (musí odpovídat při odeslání)

### Funkce pro odvozování klíčů (KDF-1)

**Inicializace protokolu:**

```
protocol_name = "Noise_XKaesobfse+hs2+hs3_25519_ChaChaPoly_SHA256"
h = SHA256(protocol_name)
ck = h  // Chaining key initialized to hash
```
**Operace MixHash:**

```
h = SHA256(h)                    // Null prologue
h = SHA256(h || rs)              // Bob's static key (known)
h = SHA256(h || e.pubkey)        // Alice's ephemeral key X
// h is now the associated data for message 1 AEAD
```
**Operace MixKey (es pattern – vzor ephemeral-static):**

```
dh_result = X25519(Alice.ephemeral_private, Bob.static_public)
temp_key = HMAC-SHA256(ck, dh_result)
ck = HMAC-SHA256(temp_key, byte(0x01))
k = HMAC-SHA256(temp_key, ck || byte(0x02))
// k is the cipher key for message 1
// ck is retained for message 2 KDF
```
### Poznámky k implementaci

1. **AES obfuskace**: Používá se pouze pro odolnost vůči DPI (hloubková inspekce paketů); kdokoli s Bobovým hash routeru a IV může dešifrovat X
2. **Prevence replay útoků**: Bob musí ukládat do cache hodnoty X (nebo jejich šifrované ekvivalenty) po dobu alespoň 2*D sekund (D = maximální odchylka hodin)
3. **Validace časového razítka**: Bob musí odmítnout spojení s |tsA - current_time| > D (typicky D = 60 sekund)
4. **Validace křivky**: Bob musí ověřit, že X je platný bod X25519
5. **Rychlé odmítnutí**: Bob může zkontrolovat X[31] & 0x80 == 0 před dešifrováním (platné klíče X25519 mají nejvyšší bit (MSB) nulový)
6. **Zpracování chyb**: Při jakémkoli selhání Bob ukončí spojení s TCP RST po náhodném timeoutu a náhodném přečtení bajtů
7. **Bufferování**: Alice musí odeslat celou zprávu (včetně vycpávky) najednou kvůli efektivitě

## Zpráva 2: SessionCreated

Bob odpovídá Alici.

**Operace Noise**: `e, ee` (efemérní-efemérní DH)

### Surový formát

```
+----+----+----+----+----+----+----+----+
|                                       |
+    AES-256-CBC Encrypted Y (32B)      +
|    Key: RH_B, IV: AES state from msg1 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+    ChaChaPoly Frame (48 bytes)        +
|    Plaintext: 32B (Y + options)       |
+    k from KDF-2, n=0, ad=h            +
|                                       |
+----+----+----+----+----+----+----+----+
|    Cleartext Padding (optional)       |
+    Length specified in options         +
|    0 to 65535 - 80 bytes              |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
### Dešifrovaný obsah

```
+----+----+----+----+----+----+----+----+
|                                       |
+    Y (Bob ephemeral public key)       +
|    32 bytes, X25519, little-endian    |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|           Options Block               |
+             (16 bytes)                +
|                                       |
+----+----+----+----+----+----+----+----+
|    Cleartext Padding (optional)       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
### Blok možností (16 bajtů, big-endian (nejvýznamnější bajt první))

```
+----+----+----+----+----+----+----+----+
| Rsvd(0) | padLen  |   Reserved (0)    |
+----+----+----+----+----+----+----+----+
|        tsB        |   Reserved (0)    |
+----+----+----+----+----+----+----+----+

Rsvd    : 2 bytes - Reserved, set to 0
padLen  : 2 bytes - Padding length in this message
Reserved: 10 bytes - Reserved, set to 0
tsB     : 4 bytes - Unix timestamp (seconds since epoch)
```
### Funkce pro odvození klíče (KDF-2)

**Operace MixHash (mixovací hash):**

```
h = SHA256(h || encrypted_payload_msg1)  // 32-byte ciphertext
if (msg1_padding_length > 0):
    h = SHA256(h || padding_from_msg1)
h = SHA256(h || e.pubkey)                // Bob's ephemeral key Y
// h is now the associated data for message 2 AEAD
```
**Operace MixKey (vzor ee):**

```
dh_result = X25519(Bob.ephemeral_private, Alice.ephemeral_public)
temp_key = HMAC-SHA256(ck, dh_result)
ck = HMAC-SHA256(temp_key, byte(0x01))
k = HMAC-SHA256(temp_key, ck || byte(0x02))
// k is the cipher key for message 2
// ck is retained for message 3 KDF
```
**Vyčištění paměti:**

```
// Overwrite ephemeral keys after ee DH
Alice.ephemeral_public = zeros(32)
Alice.ephemeral_private = zeros(32)  // Bob side
Bob.received_ephemeral = zeros(32)    // Bob side
```
### Poznámky k implementaci

1. **Řetězení AES**: Šifrování Y používá stav AES-CBC ze zprávy 1 (neresetuje se)
2. **Prevence replay (opakovaného přehrání)**: Alice musí uchovávat hodnoty Y v mezipaměti alespoň po dobu 2*D sekund
3. **Ověření časového razítka**: Alice musí odmítnout, pokud |tsB - current_time| > D
4. **Ověření křivky**: Alice musí ověřit, že Y je platný bod X25519
5. **Zpracování chyb**: Při jakémkoli selhání Alice ukončí spojení pomocí TCP RST
6. **Bufferování**: Bob musí vyprázdnit celou zprávu najednou

## Zpráva 3: SessionConfirmed

Alice potvrdí relaci a odešle RouterInfo (metadata o routeru).

**Operace Noise**: `s, se` (zveřejnění statického klíče a staticko-efemérní DH)

### Dvoudílná struktura

Zpráva 3 se skládá ze **dvou samostatných rámců AEAD (ověřené šifrování s přidruženými daty)**:

1. **Část 1**: Pevný 48bajtový rámec s Aliciným zašifrovaným statickým klíčem
2. **Část 2**: Rámec proměnné délky obsahující RouterInfo, volby a vycpávku

### Surový formát

```
+----+----+----+----+----+----+----+----+
|    ChaChaPoly Frame 1 (48 bytes)      |
+    Plaintext: Alice static key (32B)  +
|    k from KDF-2, n=1, ad=h            |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+    ChaChaPoly Frame 2 (variable)      +
|    Length specified in msg1.m3p2len   |
+    k from KDF-3, n=0, ad=h            +
|    Plaintext: RouterInfo + padding    |
+                                       +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
**Omezení velikosti:** - Část 1: Přesně 48 bajtů (32 prostého textu + 16 MAC (Message Authentication Code, autentizační kód zprávy)) - Část 2: Délka uvedená ve zprávě 1 (pole m3p2len) - Celkové maximum: 65535 bajtů (část 1 max 48, takže část 2 max 65487)

### Dešifrovaný obsah

**Část 1:**

```
+----+----+----+----+----+----+----+----+
|                                       |
+    S (Alice static public key)        +
|    32 bytes, X25519, little-endian    |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
**Část 2:**

```
+----+----+----+----+----+----+----+----+
|    Block: RouterInfo (required)       |
+    Type=2, contains Alice's RI         +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
|    Block: Options (optional)          |
+    Type=1, padding parameters          +
|                                       |
+----+----+----+----+----+----+----+----+
|    Block: Padding (optional)          |
+    Type=254, random data               +
|    MUST be last block if present      |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
### Funkce pro odvozování klíčů (KDF-3)

**Část 1 (vzorec s):**

```
h = SHA256(h || encrypted_payload_msg2)  // 32-byte ciphertext
if (msg2_padding_length > 0):
    h = SHA256(h || padding_from_msg2)

// Encrypt static key with message 2 cipher key
ciphertext = AEAD_ChaCha20_Poly1305(k_msg2, n=1, h, Alice.static_public)
h = SHA256(h || ciphertext)  // 48 bytes (32 + 16)
// h is now the associated data for message 3 part 2
```
**Část 2 (se pattern):**

```
dh_result = X25519(Alice.static_private, Bob.ephemeral_public)
temp_key = HMAC-SHA256(ck, dh_result)
ck = HMAC-SHA256(temp_key, byte(0x01))
k = HMAC-SHA256(temp_key, ck || byte(0x02))
// k is the cipher key for message 3 part 2
// ck is retained for data phase KDF

ciphertext = AEAD_ChaCha20_Poly1305(k, n=0, h, payload)
h = SHA256(h || ciphertext)
// h is retained for SipHash KDF
```
**Vyčištění paměti:**

```
// Overwrite Bob's ephemeral key after se DH
Alice.received_ephemeral = zeros(32)  // Alice side
Bob.ephemeral_public = zeros(32)       // Bob side
Bob.ephemeral_private = zeros(32)      // Bob side
```
### Poznámky k implementaci

1. **Ověření RouterInfo**: Bob musí ověřit podpis, časové razítko a konzistenci klíče
2. **Shoda klíčů**: Bob musí ověřit, že statický klíč Alice v části 1 se shoduje s klíčem v RouterInfo
3. **Umístění statického klíče**: Hledejte odpovídající parametr "s" v NTCP nebo NTCP2 RouterAddress
4. **Pořadí bloků**: RouterInfo musí být první, Options jako druhý (pokud je přítomen), Padding jako poslední (pokud je přítomen)
5. **Plánování délky**: Alice musí zajistit, aby m3p2len ve zprávě 1 přesně odpovídal délce části 2
6. **Bufferování**: Alice musí odeslat obě části společně jako jedno odeslání TCP
7. **Volitelné řetězení**: Alice může pro vyšší efektivitu okamžitě připojit rámec datové fáze

## Datová fáze

Po dokončení handshake všechny zprávy používají rámce AEAD (ověřené šifrování s přidruženými daty) s proměnnou délkou a s obfuskovanými poli délky.

### Funkce odvození klíče (datová fáze)

**Funkce Split (Noise):**

```
// Generate transmit and receive keys
zerolen = ""  // Zero-length byte array
temp_key = HMAC-SHA256(ck, zerolen)

// Alice transmits to Bob
k_ab = HMAC-SHA256(temp_key, byte(0x01))

// Bob transmits to Alice  
k_ba = HMAC-SHA256(temp_key, k_ab || byte(0x02))

// Cleanup
ck = zeros(32)
temp_key = zeros(32)
```
**Odvození klíče SipHash:**

```
// Generate additional symmetric key for SipHash
ask_master = HMAC-SHA256(temp_key, "ask" || byte(0x01))

// "siphash" is 7 bytes US-ASCII
temp_key2 = HMAC-SHA256(ask_master, h || "siphash")
sip_master = HMAC-SHA256(temp_key2, byte(0x01))

// Alice to Bob SipHash keys
temp_key3 = HMAC-SHA256(sip_master, zerolen)
sipkeys_ab = HMAC-SHA256(temp_key3, byte(0x01))
sipk1_ab = sipkeys_ab[0:7]   // 8 bytes, little-endian
sipk2_ab = sipkeys_ab[8:15]  // 8 bytes, little-endian
sipiv_ab = sipkeys_ab[16:23] // 8 bytes, IV

// Bob to Alice SipHash keys
sipkeys_ba = HMAC-SHA256(temp_key3, sipkeys_ab || byte(0x02))
sipk1_ba = sipkeys_ba[0:7]   // 8 bytes, little-endian
sipk2_ba = sipkeys_ba[8:15]  // 8 bytes, little-endian
sipiv_ba = sipkeys_ba[16:23] // 8 bytes, IV
```
### Struktura rámce

```
+----+----+----+----+----+----+----+----+
|Obfs Len |                             |
+----+----+    ChaChaPoly Frame         +
|    Encrypted Block Data               |
+    k_ab (Alice→Bob) or k_ba (Bob→Alice)|
|    Nonce starts at 0, increments      |
+    No associated data (empty string)  +
|                                       |
~           .   .   .                   ~
|                                       |
+----+----+----+----+----+----+----+----+
|    Poly1305 MAC (16 bytes)            |
+----+----+----+----+----+----+----+----+
```
**Omezení rámce:** - Minimum: 18 bajtů (2 bajty zamaskované délky + 0 bajtů prostého textu + 16 bajtů MAC) - Maximum: 65537 bajtů (2 bajty zamaskované délky + rámec 65535 bajtů) - Doporučeno: pár KB na rámec (minimalizovat latenci přijímače)

### Maskování délky pomocí SipHash

**Účel**: Zabránit identifikaci hranic rámců pomocí DPI

**Algoritmus:**

```
// Initialization (per direction)
IV[0] = sipiv  // From KDF

// For each frame:
IV[n] = SipHash-2-4(sipk1, sipk2, IV[n-1])
Mask[n] = IV[n][0:1]  // First 2 bytes of IV
ObfuscatedLength = ActualLength XOR Mask[n]

// Send 2-byte ObfuscatedLength, then ActualLength bytes
```
**Dekódování:**

```
// Receiver maintains identical IV chain
IV[n] = SipHash-2-4(sipk1, sipk2, IV[n-1])
Mask[n] = IV[n][0:1]
ActualLength = ObfuscatedLength XOR Mask[n]
// Read ActualLength bytes (includes 16-byte MAC)
```
**Poznámky:** - Oddělené řetězce IV (inicializační vektor) pro každý směr (Alice→Bob a Bob→Alice) - Pokud SipHash vrací uint64, použijte nejméně významné 2 bajty jako masku - Převeďte uint64 na další IV jako bajty v pořadí little-endian

### Formát bloku

Každý rámec obsahuje nula nebo více bloků:

```
+----+----+----+----+----+----+----+----+
|Type| Length  |       Data              |
+----+----+----+                        +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type  : 1 byte  - Block type identifier
Length: 2 bytes - Big-endian, data size (0-65516)
Data  : Variable length payload
```
**Limity velikosti:** - Maximální rámec: 65535 bajtů (včetně MAC) - Maximální prostor pro blok: 65519 bajtů (rámec - 16bajtové MAC) - Maximální jednotlivý blok: 65519 bajtů (3bajtová hlavička + 65516 dat)

### Typy bloků

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DateTime</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Time synchronization (4-byte timestamp)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Options</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Padding parameters, dummy traffic</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo delivery/flooding</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2NP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2NP message with shortened header</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Termination</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Explicit connection close</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">224-253</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental features</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">254</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Padding</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Random padding (must be last)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">255</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Future extensions</td></tr>
  </tbody>
</table>
**Pravidla řazení bloků:** - **Zpráva 3, část 2**: RouterInfo, Možnosti (volitelné), Padding (vycpávka; volitelný) - ŽÁDNÉ jiné typy - **Datová fáze**: Libovolné pořadí s výjimkou:   - Padding MUSÍ být poslední blok, pokud je přítomen   - Ukončení MUSÍ být poslední blok (kromě Padding), pokud je přítomen - Více bloků I2NP je povoleno v jednom rámci - Více bloků Padding NENÍ povoleno v jednom rámci

### Typ bloku 0: Datum a čas

Synchronizace času pro detekci odchylky hodin.

```
+----+----+----+----+----+----+----+
| 0  |    4    |     timestamp     |
+----+----+----+----+----+----+----+

Type     : 0
Length   : 4 (big-endian)
Timestamp: 4 bytes, Unix seconds (big-endian)
```
**Implementace**: Zaokrouhlit na nejbližší sekundu, aby se zabránilo hromadění časové odchylky hodin.

### Typ bloku 1: Možnosti

Parametry paddingu (vycpávání/výplň dat) a tvarování provozu.

```
+----+----+----+----+----+----+----+----+
| 1  |  size   |tmin|tmax|rmin|rmax|tdmy|
+----+----+----+----+----+----+----+----+
|tdmy|  rdmy   |  tdelay |  rdelay |    |
+----+----+----+----+----+----+----+    +
|         more_options (TBD)            |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type  : 1
Length: 12+ bytes (big-endian)
```
**Poměry výplně** (4.4 číslo s pevnou řádovou čárkou, hodnota/16.0): - `tmin`: Minimální poměr výplně pro odesílání (0.0 - 15.9375) - `tmax`: Maximální poměr výplně pro odesílání (0.0 - 15.9375) - `rmin`: Minimální poměr výplně pro příjem (0.0 - 15.9375) - `rmax`: Maximální poměr výplně pro příjem (0.0 - 15.9375)

**Příklady:** - 0x00 = 0% výplně - 0x01 = 6.25% výplně - 0x10 = 100% výplně (poměr 1:1) - 0x80 = 800% výplně (poměr 8:1)

**Falešný provoz:** - `tdmy`: Maximální objem, který je ochoten odesílat (2 bajty, průměr v bajtech/s) - `rdmy`: Požadovaný příjem (2 bajty, průměr v bajtech/s)

**Vkládání zpoždění:** - `tdelay`: Max. zpoždění ochotné k vložení (2 bajty, průměr v milisekundách) - `rdelay`: Požadované zpoždění (2 bajty, průměr v milisekundách)

**Pokyny:** - Minimální hodnoty označují požadovanou odolnost vůči analýze provozu - Maximální hodnoty označují omezení šířky pásma - Odesílatel by měl respektovat maximální hodnotu příjemce - Odesílatel může respektovat minimální hodnotu příjemce v rámci omezení - Žádný mechanismus vynucování; implementace se mohou lišit

### Typ bloku 2: RouterInfo

Doručování RouterInfo pro naplnění a zaplavování netdb.

```
+----+----+----+----+----+----+----+----+
| 2  |  size   |flg |    RouterInfo     |
+----+----+----+----+                   +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type : 2
Length: Flag (1 byte) + RouterInfo size
Flag : Bit 0 = flood request (1) or local store (0)
       Bits 1-7 = Reserved, set to 0
```
**Použití:**

**V Message 3 Part 2** (handshake): - Alice pošle svůj RouterInfo Bobovi - Flood bit obvykle 0 (lokální uložení) - RouterInfo NENÍ komprimován pomocí gzipu

**Ve fázi dat:** - Každá ze stran může odeslat svůj aktualizovaný RouterInfo - Bit Flood = 1: Vyžádat distribuci přes floodfill (pokud je příjemce floodfill) - Bit Flood = 0: Pouze místní uložení do netdb

**Požadavky na ověřování:** 1. Ověřte, že typ podpisu je podporován 2. Ověřte podpis RouterInfo 3. Ověřte, že časové razítko je v přijatelných mezích 4. Pro handshake: Ověřte, že statický klíč odpovídá parametru "s" v adrese NTCP2 5. Pro datovou fázi: Ověřte, že router hash odpovídá protějšku relace 6. Floodujte (zaplavujte) pouze RouterInfos s publikovanými adresami

**Poznámky:** - Žádný mechanismus ACK (v případě potřeby použijte I2NP DatabaseStore s reply tokenem) - Může obsahovat RouterInfos třetích stran (při použití floodfill) - NENÍ komprimováno pomocí gzip (na rozdíl od I2NP DatabaseStore)

### Typ bloku 3: zpráva I2NP

Zpráva I2NP se zkrácenou hlavičkou o délce 9 bajtů.

```
+----+----+----+----+----+----+----+----+
| 3  |  size   |type|    msg_id         |
+----+----+----+----+----+----+----+----+
|   expiration  |     I2NP payload      |
+----+----+----+                        +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type      : 3
Length    : 9 + payload_size (big-endian)
Type      : 1 byte, I2NP message type
Msg_ID    : 4 bytes, big-endian, I2NP message ID
Expiration: 4 bytes, big-endian, Unix timestamp (seconds)
Payload   : I2NP message body (length = size - 9)
```
**Rozdíly oproti NTCP1:** - Expirace: 4 bajty (sekundy) vs 8 bajtů (milisekundy) - Délka: vynecháno (odvoditelné z délky bloku) - Kontrolní součet: vynecháno (AEAD zajišťuje integritu) - Hlavička: 9 bajtů vs 16 bajtů (snížení o 44 %)

**Fragmentace:** - Zprávy I2NP NESMÍ být fragmentovány napříč bloky - Zprávy I2NP NESMÍ být fragmentovány napříč rámci - Více bloků I2NP je povoleno v jednom rámci

### Typ bloku 4: Ukončení

Explicitní ukončení spojení s kódem důvodu.

```
+----+----+----+----+----+----+----+----+
| 4  |  size   |  valid_frames_recv    |
+----+----+----+----+----+----+----+----+
| (continued) |rsn |   additional_data   |
+----+----+----+----+                   +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type            : 4
Length          : 9+ bytes (big-endian)
Valid_Frames_Recv: 8 bytes, big-endian (receive nonce value)
                  0 if error in handshake phase
Reason          : 1 byte (see table below)
Additional_Data : Optional (format unspecified, for debugging)
```
**Kódy důvodů:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Reason</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Phase</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Normal close / unspecified</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Termination received</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Idle timeout</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Router shutdown</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data phase AEAD failure</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Incompatible options</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Incompatible signature type</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Clock skew</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Padding violation</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">9</td><td style="border:1px solid var(--color-border); padding:0.5rem;">AEAD framing error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Payload format error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Message 1 error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Message 2 error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">13</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Message 3 error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">14</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Intra-frame read timeout</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo signature verification fail</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">16</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Static key parameter mismatch</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">17</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Banned</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td></tr>
  </tbody>
</table>
**Pravidla:** - Ukončení MUSÍ být v rámci posledním nevyplňovacím blokem - Maximálně jeden ukončovací blok na rámec - Odesílatel by měl po odeslání uzavřít spojení - Příjemce by měl po přijetí uzavřít spojení

**Zpracování chyb:** - Chyby handshake: Typicky uzavřít pomocí TCP RST (bez ukončovacího bloku) - Chyby AEAD (autentizované šifrování s připojenými daty) ve fázi dat: Náhodný timeout + náhodné čtení, poté odeslat ukončení - Viz sekci "AEAD Error Handling" pro bezpečnostní postupy

### Typ bloku 254: Vycpávka

Náhodná výplň pro odolnost vůči analýze síťového provozu.

```
+----+----+----+----+----+----+----+----+
|254 |  size   |     random_data       |
+----+----+----+                        +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type: 254
Length: 0-65516 bytes (big-endian)
Data: Cryptographically random bytes
```
**Pravidla:** - Výplň MUSÍ být posledním blokem v rámci, pokud je přítomna - Výplň nulové délky je povolena - Pouze jeden blok výplně na rámec - Rámce pouze s výplní jsou povoleny - Měly by být dodrženy vyjednané parametry z Options block (blok s volbami)

**Výplň ve zprávách 1-2:** - Mimo rámec AEAD (v otevřeném textu) - Zahrnuto do hashového řetězce následující zprávy (autentizováno) - Manipulace je zjištěna, když AEAD následující zprávy selže

**Výplň ve zprávě 3+ a v datové fázi:** - Uvnitř rámce AEAD (šifrovaného a autentizovaného) - Používá se pro tvarování provozu a zastírání velikosti

## Ošetření chyb AEAD

**Kritické bezpečnostní požadavky:**

### Fáze navázání spojení (zprávy 1–3)

**Známá velikost zprávy:** - Velikosti zpráv jsou předem stanovené nebo určené - Selhání autentizace AEAD je jednoznačné

**Bobova reakce na selhání zprávy 1:** 1. Nastavit náhodný timeout (rozsah závislý na implementaci, doporučeno 100-500ms) 2. Přečíst náhodný počet bajtů (rozsah závislý na implementaci, doporučeno 1KB-64KB) 3. Ukončit spojení pomocí TCP RST (bez odpovědi) 4. Dočasně zablokovat zdrojovou IP 5. Sledovat opakovaná selhání pro dlouhodobé blokace

**Reakce Alice na selhání Message 2:** 1. Okamžitě ukončit spojení pomocí TCP RST 2. Neodpovídat Bobovi

**Bobova reakce na selhání zprávy 3:** 1. Okamžitě ukončit spojení pomocí TCP RST 2. Neodpovídat Alici

### Datová fáze

**Zamaskovaná velikost zprávy:** - Pole délky je zamaskované pomocí SipHash - Neplatná délka nebo selhání AEAD (autentizované šifrování s přidruženými daty) může naznačovat:   - Sondování útočníkem   - Poškození sítě   - Desynchronizovaný SipHash IV (inicializační vektor)   - Škodlivý uzel

**Reakce na chybu AEAD nebo délky:** 1. Nastavte náhodný časový limit (doporučeno 100-500ms) 2. Přečtěte náhodný počet bajtů (doporučeno 1KB-64KB) 3. Odešlete ukončovací blok s kódem důvodu 4 (selhání AEAD) nebo 9 (chyba rámce) 4. Ukončete spojení

**Prevence dešifrovacího orákula:** - Nikdy neprozrazujte protistraně typ chyby před uplynutím náhodného časového limitu - Nikdy nevynechávejte ověření délky před kontrolou AEAD - S neplatnou délkou zacházejte stejně jako se selháním AEAD - Pro obě chyby používejte stejný postup obsluhy chyb

**Úvahy k implementaci:** - Některé implementace mohou po chybách AEAD (autentizované šifrování s přidruženými daty) pokračovat v provozu, pokud se vyskytují jen zřídka - Ukončit po opakovaných chybách (doporučený práh: 3-5 chyb za hodinu) - Vyvážit obnovu po chybách a bezpečnost

## Publikované RouterInfo

### Formát adresy pro Router

Podpora NTCP2 je oznamována prostřednictvím publikovaných záznamů RouterAddress (typ záznamu adresy routeru) se specifickými volbami.

**Styl přenosu:** - `"NTCP2"` - NTCP2 pouze na tomto portu - `"NTCP"` - NTCP i NTCP2 na tomto portu (automatická detekce)   - **Poznámka**: podpora NTCP (v1) byla odstraněna ve verzi 0.9.50 (květen 2021)   - styl "NTCP" je nyní zastaralý; použijte "NTCP2"

### Povinné volby

**Všechny zveřejněné adresy NTCP2:**

1. **`host`** - IP adresa (IPv4 nebo IPv6) nebo název hostitele
   - Formát: Standardní IP zápis nebo doménové jméno
   - Může být vynecháno u routerů pouze pro odchozí provoz nebo u skrytých routerů

2. **`port`** - číslo TCP portu
   - Formát: celé číslo, 1-65535
   - Může být vynechán u pouze odchozích nebo skrytých routerů

3. **`s`** - Statický veřejný klíč (X25519)
   - Formát: kódováno v Base64, 44 znaků
   - Kódování: abeceda I2P Base64
   - Zdroj: veřejný klíč X25519 o délce 32 bajtů, little-endian

4. **`i`** - Inicializační vektor pro AES
   - Formát: zakódováno v Base64, 24 znaků
   - Kódování: abeceda I2P Base64
   - Zdroj: IV o délce 16 bajtů, big-endian

5. **`v`** - Verze protokolu
   - Formát: celé číslo nebo čárkou oddělená celá čísla
   - Aktuální: `"2"`
   - Budoucí: `"2,3"` (musí být v číselném pořadí)

**Volitelné možnosti:**

6. **`caps`** - Schopnosti (od 0.9.50)
   - Formát: řetězec znaků schopností
   - Hodnoty:
     - `"4"` - schopnost odchozího IPv4
     - `"6"` - schopnost odchozího IPv6
     - `"46"` - obojí, IPv4 i IPv6 (doporučené pořadí)
   - Není potřeba, pokud je `host` publikován
   - Užitečné pro skryté/za firewallem routers

7. **`cost`** - Priorita adresy
   - Formát: celé číslo, 0-255
   - Nižší hodnoty = vyšší priorita
   - Doporučeno: 5-10 pro běžné adresy
   - Doporučeno: 14 pro nepublikované adresy

### Příklady záznamů RouterAddress

**Zveřejněná IPv4 adresa:**

```
<Address cost="5">
  <transport_style>NTCP2</transport_style>
  <options>
    <host>192.0.2.1</host>
    <port>8887</port>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <i>MDEyMzQ1Njc4OUFCQ0RFRg==</i>
    <v>2</v>
  </options>
</Address>
```
**Skrytý Router (pouze odchozí):**

```
<Address cost="14">
  <transport_style>NTCP2</transport_style>
  <options>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <v>2</v>
    <caps>4</caps>
  </options>
</Address>
```
**Router s duálním stackem:**

```
<!-- IPv4 Address -->
<Address cost="5">
  <transport_style>NTCP2</transport_style>
  <options>
    <host>192.0.2.1</host>
    <port>8887</port>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <i>MDEyMzQ1Njc4OUFCQ0RFRg==</i>
    <v>2</v>
  </options>
</Address>

<!-- IPv6 Address (same keys, same port) -->
<Address cost="5">
  <transport_style>NTCP2</transport_style>
  <options>
    <host>2001:db8::1</host>
    <port>8887</port>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <i>MDEyMzQ1Njc4OUFCQ0RFRg==</i>
    <v>2</v>
  </options>
</Address>
```
**Důležitá pravidla:** - Více adres NTCP2 se **stejným portem** MUSÍ používat **shodné** hodnoty `s`, `i` a `v` - Různé porty mohou používat různé klíče - Dual-stack (současná podpora IPv4 i IPv6) routers by měly zveřejňovat oddělené adresy IPv4 a IPv6

### Nezveřejněná adresa NTCP2

**Pro pouze odchozí Routers:**

Pokud router nepřijímá příchozí spojení NTCP2, ale zahajuje odchozí spojení, MUSÍ i tak zveřejnit RouterAddress (záznam adresy routeru) s:

```xml
<Address cost="14">
  <transport_style>NTCP2</transport_style>
  <options>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <v>2</v>
  </options>
</Address>
```
**Účel:** - Umožňuje Bobovi ověřit Aličin statický klíč během handshake (navázání spojení) - Vyžadováno pro ověření RouterInfo ve 2. části zprávy 3 - Není potřeba `i`, `host` ani `port` (pouze odchozí)

**Alternativa:** - Přidejte `s` a `v` k již zveřejněné adrese "NTCP" nebo SSU

### Rotace veřejného klíče a IV (inicializačního vektoru)

**Kritická bezpečnostní politika:**

**Obecná pravidla:** 1. **Nikdy neprovádějte rotaci, když je router spuštěný** 2. **Trvale ukládejte klíč a IV** i mezi restarty 3. **Sledujte předchozí dobu výpadku** pro určení, zda je rotace vhodná

**Minimální doba nedostupnosti před rotací:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Router Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Min Downtime</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Reason</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Published NTCP2 address</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>1 month</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Many routers cache RouterInfo</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Published SSU only (no NTCP2)</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>1 day</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Moderate caching</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">No published addresses (hidden)</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>2 hours</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimal impact</td></tr>
  </tbody>
</table>
**Další spouštěče:** - Změna lokální IP adresy: Může dojít k rotaci bez ohledu na výpadek - Router "rekey" (změna klíčů) (nový Router Hash): Vygeneruje nové klíče

**Odůvodnění:** - Zabraňuje odhalení časů restartu prostřednictvím změn klíčů - Umožňuje, aby RouterInfos uložené v mezipaměti přirozeně vypršely - Udržuje stabilitu sítě - Snižuje počet neúspěšných pokusů o připojení

**Implementace:** 1. Uložit klíč, IV a časové razítko posledního vypnutí trvale 2. Při startu vypočítat downtime = current_time - last_shutdown 3. Pokud downtime > minimum pro typ routeru, lze provést rotaci 4. Pokud se IP změnila nebo probíhá výměna klíče, lze provést rotaci 5. Jinak znovu použít předchozí klíč a IV

**Rotace IV (inicializačního vektoru):** - Řídí se totožnými pravidly jako rotace klíče - Vyskytuje se pouze u zveřejněných adres (nikoli u skrytých routerů) - Doporučuje se měnit IV vždy, když se změní klíč

## Detekce verze

**Kontext:** Když je `transportStyle="NTCP"` (zastaralé), Bob podporuje NTCP v1 i v2 na stejném portu a musí automaticky detekovat verzi protokolu.

**Algoritmus detekce:**

```
1. Wait for at least 64 bytes (minimum NTCP2 message 1 size)

2. If received ≥ 288 bytes:
   → Connection is NTCP version 1 (NTCP1 message 1 is 288 bytes)

3. If received < 288 bytes:
   
   Option A (conservative, pre-NTCP2 majority):
   a. Wait additional short time (e.g., 100-500ms)
   b. If total received ≥ 288 bytes → NTCP1
   c. Otherwise → Attempt NTCP2 decode
   
   Option B (aggressive, post-NTCP2 majority):
   a. Attempt NTCP2 decode immediately:
      - Decrypt first 32 bytes (X key) with AES-256-CBC
      - Verify valid X25519 point (X[31] & 0x80 == 0)
      - Verify AEAD frame
   b. If decode succeeds → NTCP2
   c. If decode fails → Wait for more data or NTCP1
```
**Rychlá kontrola nejvýznamnějšího bitu (MSB):** - Před dešifrováním AES ověřte: `encrypted_X[31] & 0x80 == 0` - Platné klíče X25519 mají nejvyšší bit vynulovaný - Selhání pravděpodobně naznačuje NTCP1 (nebo útok) - Při selhání implementujte odolnost proti sondování (náhodný časový limit + čtení)

**Požadavky na implementaci:**

1. **Odpovědnost Alice:**
   - Při připojení k adrese "NTCP" omezte zprávu 1 na maximálně 287 bajtů
   - Uložte do bufferu a vyprázdněte celou zprávu 1 najednou
   - Zvyšuje pravděpodobnost doručení v jediném TCP paketu

2. **Bobova odpovědnost:**
   - Před určením verze bufferovat přijatá data
   - Implementovat správnou obsluhu časových limitů
   - Použít TCP_NODELAY pro rychlou detekci verze
   - Po detekci verze nabufferovat celou zprávu 2 a odeslat ji najednou

**Bezpečnostní aspekty:** - Útoky segmentací: Bob by měl být odolný vůči segmentaci TCP - Sondovací útoky: Při selháních implementovat náhodná zpoždění a čtení bajtů - Prevence DoS: Omezit počet souběžně čekajících spojení - Časové limity pro čtení: Jak pro každé čtení, tak celkové (ochrana proti útoku "slowloris")

## Pokyny pro časovou odchylku

**Pole časových razítek:** - Zpráva 1: `tsA` (časové razítko Alice) - Zpráva 2: `tsB` (časové razítko Boba) - Zpráva 3+: volitelné bloky DateTime (datum a čas)

**Maximální odchylka (D):** - Typicky: **±60 sekund** - Konfigurovatelné podle implementace - Odchylka > D je obecně fatální

### Zpracování na straně Boba (Zpráva 1)

```
1. Receive tsA from Alice
2. skew = tsA - current_time
3. If |skew| > D:
   a. Still send message 2 (allows Alice to calculate skew)
   b. Include tsB in message 2
   c. Do NOT initiate handshake completion
   d. Optionally: Temporary ban Alice's IP
   e. After message 2 sent, close connection

4. If |skew| ≤ D:
   a. Continue handshake normally
```
**Odůvodnění:** Odeslání zprávy 2 i při časové odchylce umožní Alici diagnostikovat problémy s časem.

### Zpracování u Alice (Zpráva 2)

```
1. Receive tsB from Bob
2. RTT = (current_time_now - tsA_sent)
3. adjusted_skew = (tsB - current_time_now) - (RTT / 2)
4. If |adjusted_skew| > D:
   a. Close connection immediately
   b. If local clock suspect: Adjust clock or use external time source
   c. If Bob's clock suspect: Temporary ban Bob
   d. Log for operator review
5. If |adjusted_skew| ≤ D:
   a. Continue handshake normally
   b. Optionally: Track skew for time synchronization
```
**Úprava RTT:** - Odečtěte polovinu RTT od vypočtené odchylky - Zohledňuje zpoždění šíření v síti - Přesnější odhad odchylky

### Bobovo zpracování (Zpráva 3)

```
1. If message 3 received (unlikely if skew exceeded in message 1)
2. Recalculate skew = tsA_received - current_time
3. If |adjusted_skew| > D:
   a. Send termination block (reason code 7: clock skew)
   b. Close connection
   c. Ban Alice for period (e.g., 1-24 hours)
```
### Synchronizace času

**Bloky DateTime (datová fáze):** - Pravidelně odesílat blok DateTime (typ 0) - Příjemce jej může použít k seřízení hodin - Zaokrouhlit časové razítko na nejbližší sekundu (předejít zkreslení)

**Externí zdroje času:** - NTP (síťový časový protokol) - Synchronizace systémových hodin - Konsenzuální čas sítě I2P

**Strategie úpravy hodin:** - Pokud jsou místní hodiny nesprávné: Upravte systémový čas nebo použijte posun - Pokud jsou hodiny peerů trvale nesprávné: Označte problém u peera - Sledujte statistiky časové odchylky (skew) pro monitorování zdraví sítě

## Bezpečnostní vlastnosti

### Dopředné utajení

**Dosaženo pomocí:** - Efemérní výměna klíčů Diffie-Hellman (X25519) - Tři operace DH: es, ee, se (vzor Noise XK) - Efemérní klíče jsou po dokončení handshake (navázání spojení) zničeny

**Progrese důvěrnosti:** - Zpráva 1: Úroveň 2 (dopředné utajení v případě kompromitace odesílatele) - Zpráva 2: Úroveň 1 (ephemeral recipient; dočasný příjemce) - Zpráva 3+: Úroveň 5 (silné dopředné utajení)

**Perfect Forward Secrecy (dopředné utajení):** - Kompromitace dlouhodobých statických klíčů NEodhalí minulé klíče sezení - Každé sezení používá jedinečné efemérní klíče - Efemérní soukromé klíče se nikdy znovu nepoužijí - Vyčištění paměti po dohodě o klíči

**Omezení:** - Zpráva 1 je zranitelná, pokud je kompromitován Bobův statický klíč (ale zachová se forward secrecy (dopředné utajení) i při kompromitaci Alice) - Opakované útoky (replay) jsou možné pro zprávu 1 (zmírněno pomocí časového razítka a replay cache (mezipaměť proti opakování))

### Autentizace

**Vzájemná autentizace:** - Alice ověřena pomocí statického klíče ve zprávě 3 - Bob ověřen na základě vlastnictví statického soukromého klíče (implicitně z úspěšného navázání spojení)

**Odolnost vůči Key Compromise Impersonation (KCI; zneužití identity po kompromitaci klíče):** - Úroveň autentizace 2 (odolné vůči KCI) - Útočník se nemůže vydávat za Alici ani se statickým soukromým klíčem Alice (bez efemérního klíče Alice) - Útočník se nemůže vydávat za Boba ani se statickým soukromým klíčem Boba (bez efemérního klíče Boba)

**Ověření statického klíče:** - Alice zná Bobův statický klíč předem (z RouterInfo) - Bob ověří, že Aličin statický klíč odpovídá RouterInfo ve zprávě 3 - Zabraňuje útokům typu man-in-the-middle

### Odolnost vůči analýze provozu

**Opatření proti DPI:** 1. **Obfuskace AES:** Dočasné klíče jsou šifrovány, jeví se náhodně 2. **Obfuskace délky pomocí SipHash:** Délky rámců nejsou v prostém textu 3. **Náhodná výplň (padding):** Proměnlivé velikosti zpráv, žádné pevné vzory 4. **Šifrované rámce:** Veškerá užitečná data jsou šifrována pomocí ChaCha20

**Prevence replay útoků (útoků přehráním):** - Ověření časového razítka (±60 sekund) - Replay cache efemérních klíčů (životnost 2*D) - Inkrementace nonce (jednorázové hodnoty) brání přehrání paketů v rámci relace

**Odolnost proti sondování:** - Náhodné vypršení časového limitu při selháních AEAD (ověřené šifrování s přidruženými daty) - Náhodné čtení bajtů před uzavřením spojení - Žádné odpovědi při selhání navázání spojení - Zařazení IP adres na černou listinu při opakovaných selháních

**Pokyny pro padding (vycpávání):** - Zprávy 1-2: nešifrovaný padding (ověřený) - Zpráva 3+: šifrovaný padding uvnitř rámců AEAD - Dohodnuté parametry paddingu (blok Options) - Rámce obsahující pouze padding jsou povoleny

### Zmírnění útoků typu DoS

**Limity připojení:** - Maximální počet aktivních spojení (v závislosti na implementaci) - Maximální počet čekajících handshaků (např. 100-1000) - Limity připojení na IP adresu (např. 3-10 současných)

**Ochrana prostředků:** - Operace DH s omezením rychlosti (výpočetně náročné) - Časové limity pro čtení pro každý socket i celkové - Ochrana proti "Slowloris" (celkové časové limity) - Zařazování IP adres na černou listinu při zneužívání

**Rychlé odmítnutí:** - Neshoda ID sítě → okamžité uzavření - Neplatný bod X25519 → rychlá kontrola nejvýznamnějšího bitu (MSB) před dešifrováním - Časové razítko mimo povolený rozsah → uzavření bez výpočtu - Selhání AEAD (autentizované šifrování s přidruženými daty) → bez odezvy, náhodné zpoždění

**Odolnost vůči sondování:** - Náhodný časový limit: 100-500ms (závislé na implementaci) - Náhodné čtení: 1KB-64KB (závislé na implementaci) - Žádné informace o chybě pro útočníka - Ukončit pomocí TCP RST (bez FIN handshake)

### Kryptografické zabezpečení

**Algoritmy:** - **X25519**: 128bitová bezpečnost, Diffie–Hellman nad eliptickou křivkou (Curve25519) - **ChaCha20**: proudová šifra s 256bitovým klíčem - **Poly1305**: informačně-teoreticky bezpečný MAC - **SHA-256**: 128bitová odolnost proti kolizím, 256bitová odolnost vůči předobrazu - **HMAC-SHA256**: PRF (pseudonáhodná funkce) pro odvozování klíčů

**Velikosti klíčů:** - Statické klíče: 32 bajtů (256 bitů) - Efemérní klíče: 32 bajtů (256 bitů) - Šifrovací klíče: 32 bajtů (256 bitů) - MAC: 16 bajtů (128 bitů)

**Známé problémy:** - Znovupoužití nonce (jednorázové číslo) u ChaCha20 je katastrofální (zabráněno inkrementací čítače) - X25519 má problémy s malými podgrupami (zmírněno ověřením bodu na křivce) - SHA-256 je teoreticky zranitelná vůči útoku rozšíření délky (v HMAC ji nelze zneužít)

**Žádné známé zranitelnosti (k říjnu 2025):** - Noise Protocol Framework rozsáhle analyzován - ChaCha20-Poly1305 nasazen v TLS 1.3 - X25519 standard v moderních protokolech - Žádné praktické útoky na konstrukci

## Reference

### Hlavní specifikace

- **[Specifikace NTCP2](/docs/specs/ntcp2/)** - Oficiální specifikace I2P
- **[Návrh 111](/proposals/111-ntcp-2/)** - Původní návrhový dokument se zdůvodněním
- **[Rámec protokolu Noise](https://noiseprotocol.org/noise.html)** - Revize 33 (2017-10-04)

### Kryptografické standardy

- **[RFC 7748](https://www.rfc-editor.org/rfc/rfc7748)** - Eliptické křivky pro bezpečnost (X25519)
- **[RFC 7539](https://www.rfc-editor.org/rfc/rfc7539)** - ChaCha20 a Poly1305 pro protokoly IETF
- **[RFC 8439](https://www.rfc-editor.org/rfc/rfc8439)** - ChaCha20-Poly1305 (nahrazuje RFC 7539)
- **[RFC 2104](https://www.rfc-editor.org/rfc/rfc2104)** - HMAC: klíčované hašování pro autentizaci zpráv
- **[SipHash](https://www.131002.net/siphash/)** - SipHash-2-4 pro použití jako hašovací funkce

### Související specifikace I2P

- **[Specifikace I2NP](/docs/specs/i2np/)** - formát zpráv I2NP
- **[Společné struktury](/docs/specs/common-structures/)** - formáty RouterInfo a RouterAddress
- **[Transport SSU](/docs/legacy/ssu/)** - transport přes UDP (původní, nyní SSU2)
- **[Návrh 147](/proposals/147-transport-network-id-check/)** - kontrola ID transportní sítě (0.9.42)

### Implementační odkazy

- **[I2P Java](https://github.com/i2p/i2p.i2p)** - Referenční implementace (Java)
- **[i2pd](https://github.com/PurpleI2P/i2pd)** - Implementace v C++
- **[Poznámky k vydání I2P](/blog/)** - Historie verzí a aktualizace

### Historické souvislosti

- **[Station-To-Station Protocol (STS)](https://en.wikipedia.org/wiki/Station-to-Station_protocol)** - Inspirace pro Noise framework (kryptografický rámec Noise)
- **[obfs4](https://gitlab.com/yawning/obfs4)** - Zásuvný transport (precedens zastírání délky pomocí SipHash)

## Pokyny k implementaci

### Povinné požadavky

**Pro dodržování předpisů:**

1. **Implementujte kompletní handshake (navázání kryptografické relace):**
   - Podporujte všechny tři zprávy se správnými řetězci KDF (funkce odvození klíče)
   - Ověřujte všechny AEAD tagy (ověřovací značky AEAD)
   - Ověřte, že body X25519 (body eliptické křivky X25519) jsou platné

2. **Implementovat datovou fázi:**
   - Obfuskace délky pomocí SipHash (v obou směrech)
   - Všechny typy bloků: 0 (DateTime), 1 (Options), 2 (RouterInfo), 3 (I2NP), 4 (Termination), 254 (Padding)
   - Správná správa nonce (jednorázová hodnota; oddělené čítače)

3. **Bezpečnostní funkce:**
   - Prevence replay útoků (ukládání efemérních klíčů do mezipaměti po dobu 2*D)
   - Ověření časového razítka (výchozí ±60 sekund)
   - Náhodná výplň ve zprávách 1-2
   - Zpracování chyb AEAD s náhodnými časovými limity

4. **Publikování RouterInfo:**
   - Publikovat statický klíč ("s"), IV ("i") a verzi ("v")
   - Rotovat klíče podle zásad
   - Podporovat pole schopností ("caps") pro skryté routery

5. **Kompatibilita sítě:**
   - Podporovat pole ID sítě (aktuálně 2 pro hlavní síť)
   - Interoperovat se stávajícími implementacemi v jazyce Java a i2pd
   - Podporovat IPv4 i IPv6

### Doporučené postupy

**Optimalizace výkonu:**

1. **Strategie bufferování:**
   - Odeslat celé zprávy najednou (zprávy 1, 2, 3)
   - Použít TCP_NODELAY pro zprávy během navázání spojení
   - Slučovat více datových bloků do jednoho rámce
   - Omezit velikost rámce na několik KB (minimalizovat latenci na straně příjemce)

2. **Správa připojení:**
   - Opakovaně používat připojení, pokud je to možné
   - Implementovat sdružování připojení
   - Sledovat stav připojení (DateTime blocks)

3. **Správa paměti:**
   - Po použití vynulujte citlivá data (efemérní klíče, výsledky DH)
   - Omezte souběžně probíhající handshake (úvodní fáze navázání spojení; prevence DoS)
   - Pro časté alokace používejte paměťové pooly

**Zpřísnění zabezpečení:**

1. **Odolnost vůči sondování:**
   - Náhodné časové limity: 100-500ms
   - Náhodné čtení bajtů: 1KB-64KB
   - IP blacklisting (zařazení IP adres na černou listinu) při opakovaných selháních
   - Žádné podrobnosti o chybách pro protějšky

2. **Limity prostředků:**
   - Maximální počet připojení na jednu IP adresu: 3-10
   - Maximální počet čekajících handshake (navázání spojení): 100-1000
   - Časové limity pro čtení: 30-60 sekund na operaci
   - Celkový časový limit spojení: 5 minut pro handshake

3. **Správa klíčů:**
   - Trvalé uložení statického klíče a IV (inicializačního vektoru)
   - Bezpečné generování náhodných hodnot (kryptografický generátor náhodných čísel, RNG)
   - Striktně dodržujte zásady rotace klíčů
   - Nikdy znovu nepoužívejte efemérní klíče

**Monitoring a diagnostika:**

1. **Metriky:**
   - Míry úspěchu/selhání handshaku
   - Míry chyb AEAD
   - Distribuce časové odchylky (clock skew)
   - Statistiky délky trvání spojení

2. **Logování:**
   - Zaznamenávejte selhání handshake (úvodní navázání spojení) s kódy důvodů
   - Zaznamenávejte události odchylky systémových hodin
   - Zaznamenávejte zakázané IP adresy
   - Nikdy nezaznamenávejte citlivý klíčový materiál

3. **Testování:**
   - Jednotkové testy pro řetězce KDF
   - Integrační testy s jinými implementacemi
   - Fuzzing pro zpracování paketů
   - Zátěžové testování odolnosti vůči DoS útokům

### Častá úskalí

**Kritické chyby, kterým je třeba se vyhnout:**

1. **Znovupoužití nonce (jednorázové hodnoty):**
   - Nikdy během relace neresetujte čítač nonce
   - Používejte samostatné čítače pro každý směr
   - Ukončete dříve, než dosáhnete 2^64 - 1

2. **Rotace klíčů:**
   - Nikdy nerotujte klíče, když je router spuštěn
   - Nikdy znovu nepoužívejte efemérní klíče napříč relacemi
   - Dodržujte pravidla pro minimální odstávku

3. **Zpracování časových razítek:**
   - Nikdy nepřijímejte expirovaná časová razítka
   - Vždy při výpočtu odchylky zohledněte RTT (doba obousměrné cesty)
   - Zaokrouhlujte časová razítka DateTime na sekundy

4. **Chyby AEAD:**
   - Nikdy neprozrazujte útočníkovi typ chyby
   - Vždy použijte náhodný časový limit před uzavřením
   - Zacházejte s neplatnou délkou stejně jako se selháním AEAD

5. **Výplň:**
   - Nikdy neodesílejte výplň mimo dohodnuté meze
   - Vždy umístěte blok výplně na konec
   - Nikdy nepoužívejte více než jeden blok výplně v rámci jednoho rámce

6. **RouterInfo (záznam s informacemi o I2P router):**
   - Vždy ověřujte, že se statický klíč shoduje s RouterInfo
   - Nikdy nešiřte RouterInfos bez zveřejněných adres
   - Vždy ověřujte podpisy

### Metodika testování

**Jednotkové testy:**

1. **Kryptografická primitiva:**
   - Testovací vektory pro X25519, ChaCha20, Poly1305, SHA-256
   - Testovací vektory pro HMAC-SHA256
   - Testovací vektory pro SipHash-2-4

2. **Řetězce KDF:**
   - Testy s předem známým výsledkem pro všechny tři zprávy
   - Ověřit propagaci řetězového klíče
   - Otestovat generování IV pro SipHash

3. **Parsování zpráv:**
   - Dekódování platných zpráv
   - Odmítnutí neplatných zpráv
   - Hraniční podmínky (prázdná zpráva, maximální velikost)

**Integrační testy:**

1. **Handshake (navázání spojení):**
   - Úspěšná výměna tří zpráv
   - Odmítnutí kvůli časové odchylce
   - Detekce replay útoku
   - Odmítnutí neplatného klíče

2. **Datová fáze:**
   - přenos zpráv I2NP
   - výměna RouterInfo
   - zpracování výplně
   - ukončovací zprávy

3. **Interoperabilita:**
   - Testovat s Java I2P
   - Testovat s i2pd
   - Testovat IPv4 a IPv6
   - Testovat zveřejněné a skryté routers

**Bezpečnostní testy:**

1. **Negativní testy:**
   - Neplatné značky AEAD
   - Zopakované zprávy (replay)
   - Útoky využívající odchylku systémových hodin
   - Chybně formátované rámce

2. **Testy DoS:**
   - Zaplavování spojení
   - Útoky typu Slowloris
   - Vyčerpání CPU (nadměrné DH)
   - Vyčerpání paměti

3. **Fuzzing (testování náhodnými vstupy):**
   - Náhodné zprávy pro handshake
   - Náhodné rámce datové fáze
   - Náhodné typy a velikosti bloků
   - Neplatné kryptografické hodnoty

### Přechod z NTCP

**Pro podporu zastaralého NTCP (nyní odstraněno):**

Podpora NTCP (verze 1) byla odstraněna v I2P 0.9.50 (květen 2021). Všechny současné implementace musí podporovat NTCP2. Historické poznámky:

1. **Přechodné období (2018-2021):**
   - 0.9.36: NTCP2 zaveden (ve výchozím nastavení zakázán)
   - 0.9.37: NTCP2 ve výchozím nastavení povolen
   - 0.9.40: NTCP označen jako zastaralý
   - 0.9.50: NTCP odstraněn

2. **Detekce verze:**
   - "NTCP" transportStyle (typ přenosu) znamenal, že jsou podporovány obě verze
   - "NTCP2" transportStyle znamenal pouze NTCP2
   - Automatická detekce na základě velikosti zprávy (287 vs 288 bajtů)

3. **Aktuální stav:**
   - Všechny routers musí podporovat NTCP2
   - "NTCP" transportStyle (styl přenosu) je zastaralý
   - Používejte výhradně transportStyle "NTCP2"

## Příloha A: Noise XK Pattern (vzor XK protokolu Noise)

**Standardní vzor Noise XK:**

```
XK(s, rs):
  <- s
  ...
  -> e, es
  <- e, ee
  -> s, se
```
**Interpretace:**

- `<-` : Zpráva od odpovídající strany (Bob) k iniciátorovi (Alice)
- `->` : Zpráva od iniciátora (Alice) k odpovídající straně (Bob)
- `s` : Statický klíč (dlouhodobý identitní klíč)
- `rs` : Vzdálený statický klíč (statický klíč protějšku, známý předem)
- `e` : Efemérní klíč (specifický pro relaci, generovaný podle potřeby)
- `es` : Efemérní-statický DH (Alice efemérní × Bob statický)
- `ee` : Efemérní-efemérní DH (Alice efemérní × Bob efemérní)
- `se` : Statický-efemérní DH (Alice statický × Bob efemérní)

**Postup dohodnutí klíče:**

1. **Předběžná zpráva:** Alice zná Bobův statický veřejný klíč (z RouterInfo)
2. **Zpráva 1:** Alice posílá efemérní klíč, provede es DH
3. **Zpráva 2:** Bob posílá efemérní klíč, provede ee DH
4. **Zpráva 3:** Alice odhalí statický klíč, provede se DH

**Bezpečnostní vlastnosti:**

- Alice ověřena: Ano (pomocí zprávy 3)
- Bob ověřen: Ano (držením statického soukromého klíče)
- Dopředné utajení: Ano (efemerní klíče zničeny)
- Odolnost vůči KCI (útoku s kompromitací klíče): Ano (úroveň ověření 2)

## Příloha B: Kódování Base64

**Abeceda I2P Base64:**

```
ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-~
```
**Rozdíly oproti standardnímu Base64:** - Znaky 62–63: `-~` místo `+/` - Výplň: Stejná (`=`) nebo vynechána v závislosti na kontextu

**Použití v NTCP2:** - Statický klíč ("s"): 32 bajtů → 44 znaků (bez paddingu) - IV (inicializační vektor) ("i"): 16 bajtů → 24 znaků (bez paddingu)

**Příklad kódování:**

```python
# 32-byte static key (hex): 
# f4489e1bb0597b39ca6cbf5ad9f5f1f09043e02d96cb9aa6a63742b3462429aa

# I2P Base64 encoded:
# 9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=
```
## Příloha C: Analýza zachycených paketů

**Identifikace provozu NTCP2:**

1. **Navázání TCP spojení:**
   - Standardní TCP SYN, SYN-ACK, ACK
   - Cílový port typicky 8887 nebo podobný

2. **Zpráva 1 (SessionRequest – žádost o relaci):**
   - První aplikační data od Alice
   - 80-65535 bajtů (obvykle několik stovek)
   - Vypadá náhodně (dočasný klíč šifrovaný AES)
   - 287 bajtů max, pokud se připojuje k adrese "NTCP"

3. **Zpráva 2 (SessionCreated – vytvoření relace):**
   - Odpověď od Boba
   - 80-65535 bajtů (typicky několik stovek)
   - Také působí náhodně

4. **Zpráva 3 (SessionConfirmed – potvrzení relace):**
   - Od Alice
   - 48 bajtů + proměnná část (velikost RouterInfo + výplň)
   - Obvykle 1-4 KB

5. **Datová fáze:**
   - Rámce s proměnnou délkou
   - Pole délky je zatemněné (vypadá náhodně)
   - Šifrovaná užitečná data
   - Výplň způsobuje, že velikost je nepředvídatelná

**Obcházení DPI:** - Žádné hlavičky v prostém textu - Žádné pevné vzory - Pole délky jsou obfuskovaná - Náhodná výplň narušuje heuristiky založené na velikosti

**Srovnání s NTCP:** - NTCP zpráva 1 má vždy 288 bajtů (identifikovatelná) - Zpráva 1 v NTCP2 má proměnlivou velikost (neidentifikovatelná) - NTCP měl rozpoznatelné vzorce - NTCP2 je navržen tak, aby odolal DPI (hluboké inspekci paketů)

## Příloha D: Historie verzí

**Hlavní milníky:**

- **0.9.36** (23. srpna 2018): NTCP2 zavedeno, ve výchozím nastavení zakázáno
- **0.9.37** (4. října 2018): NTCP2 ve výchozím nastavení povoleno
- **0.9.40** (20. května 2019): NTCP označen jako zastaralý
- **0.9.42** (27. srpna 2019): Přidáno pole Network ID (Návrh 147)
- **0.9.50** (17. května 2021): NTCP odstraněn, přidána podpora capabilities (schopností)
- **2.10.0** (9. září 2025): Nejnovější stabilní vydání

**Stabilita protokolu:** - Žádné zpětně nekompatibilní změny od 0.9.50 - Průběžná vylepšení odolnosti vůči sondování - Důraz na výkon a spolehlivost - Postkvantová kryptografie ve vývoji (není ve výchozím nastavení povolena)

**Aktuální stav transportních protokolů:** - NTCP2: Povinný TCP transport - SSU2: Povinný UDP transport - NTCP (v1): Odstraněno - SSU (v1): Odstraněno
