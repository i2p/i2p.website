---
title: "NTCP2 Transport"
description: "TCP transport založený na Noise protokolu pro spojení router-router"
slug: "ntcp2"
category: "Transporty"
lastUpdated: "2026-07"
accurateFor: "0.9.70"
---

## Přehled

NTCP2 je autentizovaný protokol pro dohodu o klíčích, který zlepšuje odolnost [NTCP](/docs/transport/ntcp) proti různým formám automatické identifikace a útoků.

NTCP2 je navržen pro flexibilitu a koexistenci s NTCP. Může být podporován na stejném portu jako NTCP, nebo na jiném portu, nebo zcela bez současné podpory NTCP. Podrobnosti najdete v sekci Published Router Info níže.

Stejně jako u ostatních I2P transportů je NTCP2 definován výhradně pro point-to-point (router-to-router) přenos I2NP zpráv. Není to univerzální datový kanál.

NTCP2 je podporován od verze 0.9.36. Viz [Prop111](/proposals/111-ntcp-2) pro původní návrh, včetně diskuse na pozadí a dalších informací.

## Noise Protocol Framework

NTCP2 používá Noise Protocol Framework [NOISE](https://noiseprotocol.org/noise.html) (Revize 33, 2017-10-04). Noise má podobné vlastnosti jako protokol Station-To-Station [STS](#references), který je základem pro protokol [SSU](/docs/transport/ssu). V terminologii Noise je Alice iniciátor a Bob je respondent.

NTCP2 je založen na Noise protokolu Noise_XK_25519_ChaChaPoly_SHA256. (Skutečný identifikátor pro počáteční funkci odvození klíče je "Noise_XKaesobfse+hs2+hs3_25519_ChaChaPoly_SHA256" k označení I2P rozšíření - viz sekce KDF 1 níže) Tento Noise protokol používá následující primitiva:

- Handshake Pattern: XK Alice přenáší svůj klíč Bobovi (X) Alice již zná Bobův statický klíč (K)
- DH Function: X25519 X25519 DH s délkou klíče 32 bajtů podle specifikace v [RFC-7748](https://tools.ietf.org/html/rfc7748).
- Cipher Function: ChaChaPoly AEAD_CHACHA20_POLY1305 podle specifikace v [RFC-7539](https://tools.ietf.org/html/rfc7539) sekce 2.8. 12 bajtový nonce, s prvními 4 bajty nastavenými na nulu.
- Hash Function: SHA256 Standardní 32bajtový hash, již hojně používaný v I2P.

## Doplňky k frameworku

NTCP2 definuje následující vylepšení pro Noise_XK_25519_ChaChaPoly_SHA256. Tato obecně následují směrnice v sekci 13 [NOISE](https://noiseprotocol.org/noise.html).

1) Klíče v otevřeném textu (cleartext ephemeral keys) jsou zastírány pomocí AES šifrování s použitím známého klíče a IV. 2) K zprávám 1 a 2 je přidáno náhodné padding v otevřeném textu. Padding v otevřeném textu je zahrnut do výpočtu handshake hash (MixHash). Viz sekce KDF níže pro zprávu 2 a zprávu 3 část 1. Náhodné AEAD padding je přidáno ke zprávě 3 a zprávám datové fáze. 3) Je přidáno dvoubajtové pole délky rámce, jak je vyžadováno pro Noise over TCP a jako v obfs4. Toto je použito pouze ve zprávách datové fáze. AEAD rámce zpráv 1 a 2 mají pevnou délku. AEAD rámec zprávy 3 část 1 má pevnou délku. Délka AEAD rámce zprávy 3 část 2 je specifikována ve zprávě 1. 4) Dvoubajtové pole délky rámce je zastíráno pomocí SipHash-2-4, jako v obfs4. 5) Formát payload je definován pro zprávy 1,2,3 a datovou fázi. Samozřejmě, tyto nejsou definovány v rámci frameworku.

## Zprávy

Všechny NTCP2 zprávy mají délku maximálně 65537 bajtů. Formát zprávy je založen na Noise zprávách s úpravami pro rámování a nerozeznatelnost. Implementace používající standardní Noise knihovny možná budou muset předběžně zpracovat přijaté zprávy do/z formátu Noise zpráv. Všechna zašifrovaná pole jsou AEAD šifrotexty.

Sekvence vytváření je následující:

```
Alice                           Bob

SessionRequest ------------------->
<------------------- SessionCreated
SessionConfirmed ----------------->
```
Používając terminologii Noise, sekvence navázání spojení a dat je následující: (Vlastnosti zabezpečení užitečného zatížení z [Noise](https://noiseprotocol.org/noise.html) )

```
XK(s, rs):           Authentication   Confidentiality
  <- s
  ...
  -> e, es                  0                2
  <- e, ee                  2                1
  -> s, se                  2                5
  <-                        2                5
```
Jakmile je relace navázána, Alice a Bob si mohou vyměňovat datové zprávy.

Všechny typy zpráv (SessionRequest, SessionCreated, SessionConfirmed, Data a TimeSync) jsou specifikovány v této sekci.

Některé značení:

    - RH_A = Router Hash for Alice (32 bytes)
    - RH_B = Router Hash for Bob (32 bytes)

### Autentizované šifrování

Existují tři samostatné instance autentifikovaného šifrování (CipherStates). Jedna během fáze handshake a dvě (odesílání a příjem) pro datovou fázi. Každá má svůj vlastní klíč z KDF.

Šifrovaná/autentizovaná data budou reprezentována jako

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|   Encrypted and authenticated data    |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
```
#### ChaCha20/Poly1305

Šifrovaný a ověřený formát dat.

Vstupy do funkcí pro šifrování/dešifrování:

```
k :: 32 byte cipher key, as generated from KDF

nonce :: Counter-based nonce, 12 bytes.
         Starts at 0 and incremented for each message.
         First four bytes are always zero.
         Last eight bytes are the counter, little-endian encoded.
         Maximum value is 2**64 - 2.
         Connection must be dropped and restarted after
         it reaches that value.
         The value 2**64 - 1 must never be sent.

ad :: In handshake phase:
      Associated data, 32 bytes.
      The SHA256 hash of all preceding data.
      In data phase:
      Zero bytes

data :: Plaintext data, 0 or more bytes
```
Výstup šifrovací funkce, vstup dešifrovací funkce:

```
+----+----+----+----+----+----+----+----+
|Obfs Len |                             |
+----+----+                             +
|       ChaCha20 encrypted data         |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+              (MAC)                    +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Obfs Len :: Length of (encrypted data + MAC) to follow, 16 - 65535
            Obfuscation using SipHash (see below)
            Not used in message 1 or 2, or message 3 part 1, where the length is fixed
            Not used in message 3 part 1, as the length is specified in message 1

encrypted data :: Same size as plaintext data, 0 - 65519 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
Pro ChaCha20 to, co je zde popsáno, odpovídá [RFC-7539](https://tools.ietf.org/html/rfc7539), který se také podobně používá v TLS [RFC-7905](https://tools.ietf.org/html/rfc7905).

#### Poznámky

- Protože ChaCha20 je proudová šifra, plaintexty nemusí být doplňovány. Další bajty keystream jsou zahozeny.
- Klíč pro šifru (256 bitů) je dohodnut prostřednictvím SHA256 KDF. Podrobnosti KDF pro každou zprávu jsou uvedeny v samostatných sekcích níže.
- ChaChaPoly rámce pro zprávy 1, 2 a první část zprávy 3 mají známou velikost. Počínaje druhou částí zprávy 3 mají rámce proměnlivou velikost. Velikost části 1 zprávy 3 je specifikována ve zprávě 1. Počínaje datovou fází jsou rámce předsazeny dvoubajtovou délkou obfuskovanou pomocí SipHash jako v obfs4.
- Padding je mimo autentizovaný datový rámec pro zprávy 1 a 2. Padding je použit v KDF pro další zprávu, takže manipulace bude detekována. Počínaje zprávou 3 je padding uvnitř autentizovaného datového rámce.

#### Zpracování chyb AEAD

- V zprávách 1, 2 a ve zprávě 3 částech 1 a 2 je velikost AEAD zprávy známa předem. Při selhání AEAD autentizace musí příjemce zastavit další zpracování zpráv a uzavřít spojení bez odpovědi. Toto by mělo být abnormální uzavření (TCP RST).
- Pro odolnost proti sondování by Bob ve zprávě 1 po selhání AEAD měl nastavit náhodný timeout (rozsah TBD) a poté přečíst náhodný počet bajtů (rozsah TBD) před uzavřením socketu. Bob by měl udržovat černou listinu IP adres s opakovanými selháními.
- Ve fázi dat je velikost AEAD zprávy "zašifrována" (obfuskována) pomocí SipHash. Je třeba dbát na to, aby se nevytvořil dešifrovací oracle. Při selhání AEAD autentizace ve fázi dat by příjemce měl nastavit náhodný timeout (rozsah TBD) a poté přečíst náhodný počet bajtů (rozsah TBD). Po přečtení nebo při vypršení timeoutu pro čtení by příjemce měl odeslat payload s ukončovacím blokem obsahujícím kód důvodu "selhání AEAD" a uzavřít spojení.
- Proveďte stejnou chybovou akci pro neplatnou hodnotu pole délky ve fázi dat.

### Funkce pro odvození klíče (KDF) (pro handshake zprávu 1)

KDF generuje klíč k pro šifrování fáze handshake z výsledku DH, pomocí HMAC-SHA256(key, data) jak je definováno v [RFC-2104](https://tools.ietf.org/html/rfc2104). Jedná se o funkce InitializeSymmetric(), MixHash() a MixKey(), přesně jak jsou definovány ve specifikaci Noise.

```
This is the "e" message pattern:

// Define protocol_name.
Set protocol_name = "Noise_XKaesobfse+hs2+hs3_25519_ChaChaPoly_SHA256"
 (48 bytes, US-ASCII encoded, no NULL termination).

// Define Hash h = 32 bytes
h = SHA256(protocol_name);

Define ck = 32 byte chaining key. Copy the h data to ck.
Set ck = h

Define rs = Bob's 32-byte static key as published in the RouterInfo

// MixHash(null prologue)
h = SHA256(h);

// up until here, can all be precalculated by Alice for all outgoing connections

// Alice must validate that Bob's static key is a valid point on the curve here.

// Bob static key
// MixHash(rs)
// || below means append
h = SHA256(h || rs);

// up until here, can all be precalculated by Bob for all incoming connections

This is the "e" message pattern:

Alice generates her ephemeral DH key pair e.

// Alice ephemeral key X
// MixHash(e.pubkey)
// || below means append
h = SHA256(h || e.pubkey);

// h is used as the associated data for the AEAD in message 1
// Retain the Hash h for the message 2 KDF


End of "e" message pattern.

This is the "es" message pattern:

// DH(e, rs) == DH(s, re)
Define input_key_material = 32 byte DH result of Alice's ephemeral key and Bob's static key
Set input_key_material = X25519 DH result

// MixKey(DH())

Define temp_key = 32 bytes
Define HMAC-SHA256(key, data) as in [RFC-2104]_
// Generate a temp key from the chaining key and DH result
// ck is the chaining key, defined above
temp_key = HMAC-SHA256(ck, input_key_material)
// overwrite the DH result in memory, no longer needed
input_key_material = (all zeros)

// Output 1
// Set a new chaining key from the temp key
// byte() below means a single byte
ck =       HMAC-SHA256(temp_key, byte(0x01)).

// Output 2
// Generate the cipher key k
Define k = 32 bytes
// || below means append
// byte() below means a single byte
k =        HMAC-SHA256(temp_key, ck || byte(0x02)).
// overwrite the temp_key in memory, no longer needed
temp_key = (all zeros)

// retain the chaining key ck for message 2 KDF


End of "es" message pattern.
```
### 1) SessionRequest

Alice posílá Bobovi.

Noise obsah: Alice ephemeral klíč X Noise payload: 16 bajtový option blok Non-noise payload: Náhodné vyplnění

(Vlastnosti zabezpečení payload z [Noise](https://noiseprotocol.org/noise.html) )

```
XK(s, rs):           Authentication   Confidentiality
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
Hodnota X je zašifrována, aby byla zajištěna nerozlišitelnost a jedinečnost payload, což jsou nezbytná protiopatření proti DPI. K dosažení tohoto cíle používáme AES šifrování místo složitějších a pomalejších alternativ, jako je elligator2. Asymetrické šifrování veřejným klíčem Bobova routeru by bylo příliš pomalé. AES šifrování používá hash Bobova routeru jako klíč a Bobovo IV, jak je publikováno v síťové databázi.

AES šifrování slouží pouze k odolnosti proti DPI. Jakákoli strana znající Bobův router hash a IV, které jsou publikovány v síťové databázi, může dešifrovat hodnotu X v této zprávě.

Výplň není šifrována Alicí. Může být nutné, aby Bob dešifroval výplň, aby zabránil časovým útokům.

Surový obsah:

```
+----+----+----+----+----+----+----+----+
|                                       |
+        obfuscated with RH_B           +
|       AES-CBC-256 encrypted X         |
+             (32 bytes)                +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|   ChaChaPoly encrypted data           |
+             (16 bytes)                +
|   k defined in KDF for message 1      |
+   n = 0                               +
|   see KDF for associated data         |
+----+----+----+----+----+----+----+----+
|                                       |
+        Poly1305 MAC (16 bytes)        +
|                                       |
+----+----+----+----+----+----+----+----+
|     unencrypted authenticated         |
~         padding (optional)            ~
|     length defined in options block   |
+----+----+----+----+----+----+----+----+

X :: 32 bytes, AES-256-CBC encrypted X25519 ephemeral key, little endian
        key: RH_B
        iv: As published in Bobs network database entry

padding :: Random data, 0 or more bytes.
           Total message length must be 65535 bytes or less.
           Total message length must be 287 bytes or less if
           Bob is publishing his address as NTCP
           (see Version Detection section below).
           Alice and Bob will use the padding data in the KDF for message 2.
           It is authenticated so that any tampering will cause the
           next message to fail.
```
Nešifrovaná data (autentifikační tag Poly1305 není zobrazen):

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|                   X                   |
+              (32 bytes)               +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|               options                 |
+              (16 bytes)               +
|                                       |
+----+----+----+----+----+----+----+----+
|     unencrypted authenticated         |
+         padding (optional)            +
|     length defined in options block   |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

X :: 32 bytes, X25519 ephemeral key, little endian

options :: options block, 16 bytes, see below

padding :: Random data, 0 or more bytes.
           Total message length must be 65535 bytes or less.
           Total message length must be 287 bytes or less if
           Bob is publishing his address as "NTCP"
           (see Version Detection section below)
           Alice and Bob will use the padding data in the KDF for message 2.
           It is authenticated so that any tampering will cause the
           next message to fail.
```
Blok možností: Poznámka: Všechna pole jsou ve formátu big-endian.

```
+----+----+----+----+----+----+----+----+
| id | ver|  padLen | m3p2len | Rsvd(0) |
+----+----+----+----+----+----+----+----+
|        tsA        |   Reserved (0)    |
+----+----+----+----+----+----+----+----+

id :: 1 byte, the network ID (currently 2, except for test networks)
      As of 0.9.42. See proposal 147.

ver :: 1 byte, protocol version (currently 2)

padLen :: 2 bytes, length of the padding, 0 or more
          See below for max guidelines. Random size from 0 to 64 bytes minimum is recommended.
          (Distribution is implementation-dependent)

m3p2Len :: 2 bytes, length of the the second AEAD frame in SessionConfirmed
           (message 3 part 2) See notes below

Rsvd :: 2 bytes, set to 0 for compatibility with future options

tsA :: 4 bytes, Unix timestamp, unsigned seconds.
       Wraps around in 2106

Reserved :: 4 bytes, set to 0 for compatibility with future options
```
#### Poznámky

- Když je publikovaná adresa "NTCP", Bob podporuje jak NTCP tak NTCP2 na stejném portu. Z důvodu kompatibility, když Alice navazuje spojení na adresu publikovanou jako "NTCP", musí omezit maximální velikost této zprávy včetně výplně na 287 bajtů nebo méně. To usnadňuje automatickou identifikaci protokolu ze strany Boba. Když je publikována jako "NTCP2", neexistuje žádné omezení velikosti. Viz sekce Publikované adresy a Detekce verzí níže.

- Jedinečná hodnota X v počátečním AES bloku zajišťuje, že šifrovaný text je odlišný pro každou relaci.

- Bob musí odmítnout spojení, kde je hodnota časového razítka příliš vzdálená od aktuálního času. Nazvěme maximální časový rozdíl "D". Bob musí udržovat lokální mezipaměť dříve použitých hodnot handshake a odmítat duplikáty, aby zabránil replay útokům. Hodnoty v mezipaměti musí mít životnost alespoň 2*D. Hodnoty mezipaměti jsou závislé na implementaci, nicméně lze použít 32-bytovou hodnotu X (nebo její šifrovaný ekvivalent).

- Diffie-Hellman dočasné klíče nesmí být nikdy znovu použity, aby se zabránilo kryptografickým útokům, a opětovné použití bude odmítnuto jako replay útok.

- Možnosti "KE" a "auth" musí být kompatibilní, tj. sdílené tajemství K musí mít odpovídající velikost. Pokud budou přidány další možnosti "auth", mohlo by to implicitně změnit význam příznaku "KE" tak, aby používal jiný KDF nebo jinou velikost zkrácení.

- Bob musí ověřit, že Aliceův dočasný klíč je platný bod na křivce zde.

- Padding by měl být omezen na rozumné množství. Bob může odmítnout spojení s nadměrným padding. Bob specifikuje své možnosti padding ve zprávě 2. Minimální/maximální pokyny budou určeny později. Náhodná velikost od 0 do minimálně 31 bajtů? (Distribuce závisí na implementaci) Java implementace aktuálně omezují padding na maximálně 256 bajtů.

- Při jakékoli chybě, včetně AEAD, DH, časového razítka, zjevného opakování nebo selhání validace klíče, musí Bob zastavit další zpracování zpráv a uzavřít spojení bez odpovědi. Toto by mělo být abnormální uzavření (TCP RST). Pro odolnost proti sondování by měl Bob po selhání AEAD nastavit náhodný timeout (rozsah TBD) a poté přečíst náhodný počet bytů (rozsah TBD), před uzavřením socketu.

- Bob může provést rychlou MSB kontrolu platného klíče (X[31] & 0x80 == 0) před pokusem o dešifrování. Pokud je nejvyšší bit nastaven, implementujte odolnost proti sondování stejně jako u selhání AEAD.

- Zmírnění DoS: DH je relativně nákladná operace. Stejně jako u předchozího protokolu NTCP by měly routery přijmout všechna nezbytná opatření k zabránění vyčerpání CPU nebo připojení. Nastavte limity na maximální počet aktivních připojení a maximální počet probíhajících nastavování připojení. Vynucujte časové limity pro čtení (jak pro jednotlivé čtení, tak celkové pro "slowloris"). Omezte opakovaná nebo současná připojení ze stejného zdroje. Udržujte černé listiny zdrojů, které opakovaně selhávají. Neodpovídejte na selhání AEAD.

- Pro usnadnění rychlé detekce verze a handshakingu musí implementace zajistit, že Alice nejprve uloží do bufferu a poté vyprázdní celý obsah první zprávy najednou, včetně paddingu. To zvyšuje pravděpodobnost, že data budou obsažena v jediném TCP paketu (pokud nebudou segmentována OS nebo middleboxes) a Bob je přijme všechna najednou. Navíc musí implementace zajistit, že Bob uloží do bufferu a poté vyprázdní celý obsah druhé zprávy najednou, včetně paddingu, a že Bob uloží do bufferu a poté vyprázdní celý obsah třetí zprávy najednou. To je také kvůli efektivitě a k zajištění účinnosti náhodného paddingu.

- pole "ver": Celkový Noise protokol, rozšíření a NTCP protokol včetně specifikací payload, indikující NTCP2. Toto pole může být použito k indikaci podpory budoucích změn.

- Délka části 2 zprávy 3: Toto je velikost druhého AEAD rámce (včetně 16-bajtového MAC) obsahujícího Router Info Alice a volitelné doplnění, které bude odesláno ve zprávě SessionConfirmed. Protože routery pravidelně regenerují a znovu publikují své Router Info, velikost aktuálního Router Info se může změnit před odesláním zprávy 3. Implementace musí zvolit jednu ze dvou strategií:

a\) uložit aktuální Router Info pro odeslání ve zprávě 3, aby byla známa velikost, a volitelně přidat místo pro padding;

b\) zvětšit specifikovanou velikost dostatečně, aby umožnila možné zvětšení velikosti Router Info, a vždy přidat padding když je zpráva 3 skutečně odeslána. V obou případech musí být délka "m3p2len" zahrnutá ve zprávě 1 přesně velikostí tohoto rámce při odeslání ve zprávě 3.

- Bob musí ukončit spojení, pokud po validaci zprávy 1 a načtení paddingu zůstanou jakákoliv příchozí data. Neměla by existovat žádná další data od Alice, protože Bob ještě neodpověděl zprávou 2.

- Pole network ID se používá k rychlé identifikaci připojení mezi sítěmi. Pokud je toto pole nenulové a neodpovídá network ID Boba, Bob by se měl odpojit a blokovat budoucí připojení. Všechna připojení z testovacích sítí by měla mít jiné ID a test neprojedou. Od verze 0.9.42. Více informací najdete v návrhu 147.

- Přes API 0.9.68 (vydání 2.11.0) implementovalo Java I2P maximum 256 bajtů paddingu pro non-PQ připojení, nicméně toto
  nebylo dříve dokumentováno.
  Od API 0.9.69 (vydání 2.12.0) implementuje Java I2P stejný maximální padding pro non-PQ připojení
  jako pro MLKEM-512. Maximální padding je 880 bajtů.

### Funkce pro odvození klíče (KDF) (pro handshake zprávu 2 a zprávu 3 část 1)

```
// take h saved from message 1 KDF
// MixHash(ciphertext)
h = SHA256(h || 32 byte encrypted payload from message 1)

// MixHash(padding)
// Only if padding length is nonzero
h = SHA256(h || random padding from message 1)

This is the "e" message pattern:

Bob generates his ephemeral DH key pair e.

// h is from KDF for handshake message 1
// Bob ephemeral key Y
// MixHash(e.pubkey)
// || below means append
h = SHA256(h || e.pubkey);

// h is used as the associated data for the AEAD in message 2
// Retain the Hash h for the message 3 KDF

End of "e" message pattern.

This is the "ee" message pattern:

// DH(e, re)
Define input_key_material = 32 byte DH result of Alice's ephemeral key and Bob's ephemeral key
Set input_key_material = X25519 DH result
// overwrite Alice's ephemeral key in memory, no longer needed
// Alice:
e(public and private) = (all zeros)
// Bob:
re = (all zeros)

// MixKey(DH())

Define temp_key = 32 bytes
Define HMAC-SHA256(key, data) as in [RFC-2104]_
// Generate a temp key from the chaining key and DH result
// ck is the chaining key, from the KDF for handshake message 1
temp_key = HMAC-SHA256(ck, input_key_material)
// overwrite the DH result in memory, no longer needed
input_key_material = (all zeros)

// Output 1
// Set a new chaining key from the temp key
// byte() below means a single byte
ck =       HMAC-SHA256(temp_key, byte(0x01)).

// Output 2
// Generate the cipher key k
Define k = 32 bytes
// || below means append
// byte() below means a single byte
k =        HMAC-SHA256(temp_key, ck || byte(0x02)).
// overwrite the temp_key in memory, no longer needed
temp_key = (all zeros)

// retain the chaining key ck for message 3 KDF

End of "ee" message pattern.
```
### 2) SessionCreated

Bob posílá Alici.

Noise obsah: Bobův dočasný klíč Y Noise payload: 16 bajtový blok možností Non-noise payload: Náhodné výplň

(Vlastnosti zabezpečení užitečného zatížení z [Noise](https://noiseprotocol.org/noise.html) )

```
XK(s, rs):           Authentication   Confidentiality
  <- e, ee                  2                1

  Authentication: 2.
  Sender authentication resistant to key-compromise impersonation (KCI).
  The sender authentication is based on an ephemeral-static DH ("es" or "se")
  between the sender's static key pair and the recipient's ephemeral key pair.
  Assuming the corresponding private keys are secure, this authentication cannot be forged.

  Confidentiality: 1.
  Encryption to an ephemeral recipient.
  This payload has forward secrecy, since encryption involves an ephemeral-ephemeral DH ("ee").
  However, the sender has not authenticated the recipient,
  so this payload might be sent to any party, including an active attacker.


  "e": Bob generates a new ephemeral key pair and stores it in the e variable,
  writes the ephemeral public key as cleartext into the message buffer,
  and hashes the public key along with the old h to derive a new h.

  "ee": A DH is performed between the Bob's ephemeral key pair and the Alice's ephemeral key pair.
  The result is hashed along with the old ck to derive a new ck and k, and n is set to zero.
```
Hodnota Y je šifrována za účelem zajištění nerozlišitelnosti a jedinečnosti payload, které jsou nezbytná opatření proti DPI. K dosažení tohoto cíle používáme šifrování AES místo složitějších a pomalejších alternativ jako je elligator2. Asymetrické šifrování veřejným klíčem Alice routeru by bylo příliš pomalé. Šifrování AES používá hash Bob routeru jako klíč a AES stav ze zprávy 1 (který byl inicializován s Bob IV, jak je publikován v síťové databázi).

AES šifrování slouží pouze k odolnosti vůči DPI. Jakákoliv strana znající hash routeru Boba a IV, které jsou publikovány v síťové databázi, a která zachytila prvních 32 bajtů zprávy 1, může dešifrovat hodnotu Y v této zprávě.

Surový obsah:

```
+----+----+----+----+----+----+----+----+
|                                       |
+        obfuscated with RH_B           +
|       AES-CBC-256 encrypted Y         |
+              (32 bytes)               +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|   ChaChaPoly encrypted data (options) |
+   16 bytes                            +
|   k defined in KDF for message 2      |
+   n = 0; see KDF for associated data  +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+        Poly1305 MAC (16 bytes)        +
|                                       |
+----+----+----+----+----+----+----+----+
|     unencrypted authenticated         |
+         padding (optional)            +
|     length defined in options block   |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

Y :: 32 bytes, AES-256-CBC encrypted X25519 ephemeral key, little endian
        key: RH_B
        iv: Using AES state from message 1
```
Nešifrovaná data (Poly1305 autentizační tag není zobrazen):

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|                  Y                    |
+              (32 bytes)               +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|               options                 |
+              (16 bytes)               +
|                                       |
+----+----+----+----+----+----+----+----+
|     unencrypted authenticated         |
+         padding (optional)            +
|     length defined in options block   |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

Y :: 32 bytes, X25519 ephemeral key, little endian

options :: options block, 16 bytes, see below

padding :: Random data, 0 or more bytes.
           Total message length must be 65535 bytes or less.
           Alice and Bob will use the padding data in the KDF for message 3 part 1.
           It is authenticated so that any tampering will cause the
           next message to fail.
```
#### Poznámky

- Alice musí ověřit, že Bobův dočasný klíč je platný bod na křivce.
- Padding by měl být omezen na rozumné množství. Alice může odmítnout připojení s nadměrným paddingem. Alice specifikuje své možnosti paddingu ve zprávě 3. Min/max směrnice ještě nejsou určeny. Náhodná velikost od 0 do minimálně 31 bajtů? (Distribuce závisí na implementaci)
- Při jakékoli chybě, včetně AEAD, DH, časového razítka, zdánlivého replay útoku nebo selhání ověření klíče, musí Alice zastavit další zpracování zpráv a zavřít připojení bez odpovědi. Toto by mělo být abnormální uzavření (TCP RST).
- Pro usnadnění rychlého handshakingu musí implementace zajistit, že Bob uloží do bufferu a poté vyprázdní celý obsah první zprávy najednou, včetně paddingu. Toto zvyšuje pravděpodobnost, že data budou obsažena v jediném TCP paketu (pokud nebudou segmentována OS nebo middleboxy) a Alice je obdrží všechna najednou. Toto je také pro efektivitu a zajištění účinnosti náhodného paddingu.
- Alice musí ukončit připojení, pokud po ověření zprávy 2 a načtení paddingu zůstanou jakákoli příchozí data. Od Boba by neměla být žádná další data, protože Alice ještě neodpověděla zprávou 3.

Blok možností: Poznámka: Všechna pole jsou v big-endian formátu.

```
+----+----+----+----+----+----+----+----+
| Rsvd(0) | padLen  |   Reserved (0)    |
+----+----+----+----+----+----+----+----+
|        tsB        |   Reserved (0)    |
+----+----+----+----+----+----+----+----+

Reserved :: 10 bytes total, set to 0 for compatibility with future options

padLen :: 2 bytes, big endian, length of the padding, 0 or more
          See below for max guidelines. Random size from 0 to 64 bytes minimum is recommended.
          (Distribution is implementation-dependent)

tsB :: 4 bytes, big endian, Unix timestamp, unsigned seconds.
       Wraps around in 2106
```
#### Poznámky

- Alice musí odmítnout připojení, kde je hodnota časového razítka příliš vzdálená od aktuálního času. Nazvěme maximální rozdíl času "D". Alice musí udržovat lokální cache dříve použitých hodnot handshake a odmítat duplikáty, aby zabránila replay útokům. Hodnoty v cache musí mít životnost alespoň 2*D. Hodnoty cache jsou závislé na implementaci, nicméně může být použita 32-bajtová hodnota Y (nebo její šifrovaný ekvivalent).

- Prostřednictvím API 0.9.68 (vydání 2.11.0), Java I2P implementovala maximum 256 bajtů paddingu pro non-PQ spojení, toto však nebylo dříve zdokumentováno.
  Od API 0.9.69 (vydání 2.12.0), Java I2P implementuje stejný maximální padding pro non-PQ spojení
  jako pro MLKEM-512. Maximální padding je 848 bajtů.

#### Problémy

- Zahrnout zde možnosti min/max odsazení?

### Šifrování pro handshake zprávu 3 část 1, pomocí zprávy 2 KDF)

```
// take h saved from message 2 KDF
// MixHash(ciphertext)
h = SHA256(h || 24 byte encrypted payload from message 2)

// MixHash(padding)
// Only if padding length is nonzero
h = SHA256(h || random padding from message 2)
// h is used as the associated data for the AEAD in message 3 part 1, below

This is the "s" message pattern:

Define s = Alice's static public key, 32 bytes

// EncryptAndHash(s.publickey)
// EncryptWithAd(h, s.publickey)
// AEAD_ChaCha20_Poly1305(key, nonce, associatedData, data)
// k is from handshake message 1
// n is 1
ciphertext = AEAD_ChaCha20_Poly1305(k, n++, h, s.publickey)
// MixHash(ciphertext)
// || below means append
h = SHA256(h || ciphertext);

// h is used as the associated data for the AEAD in message 3 part 2

End of "s" message pattern.
```
### Funkce pro odvození klíčů (KDF) (pro handshake zprávu 3 část 2)

```
This is the "se" message pattern:

// DH(s, re) == DH(e, rs)
Define input_key_material = 32 byte DH result of Alice's static key and Bob's ephemeral key
Set input_key_material = X25519 DH result
// overwrite Bob's ephemeral key in memory, no longer needed
// Alice:
re = (all zeros)
// Bob:
e(public and private) = (all zeros)

// MixKey(DH())

Define temp_key = 32 bytes
Define HMAC-SHA256(key, data) as in [RFC-2104]_
// Generate a temp key from the chaining key and DH result
// ck is the chaining key, from the KDF for handshake message 1
temp_key = HMAC-SHA256(ck, input_key_material)
// overwrite the DH result in memory, no longer needed
input_key_material = (all zeros)

// Output 1
// Set a new chaining key from the temp key
// byte() below means a single byte
ck =       HMAC-SHA256(temp_key, byte(0x01)).

// Output 2
// Generate the cipher key k
Define k = 32 bytes
// || below means append
// byte() below means a single byte
k =        HMAC-SHA256(temp_key, ck || byte(0x02)).

// h from message 3 part 1 is used as the associated data for the AEAD in message 3 part 2

// EncryptAndHash(payload)
// EncryptWithAd(h, payload)
// AEAD_ChaCha20_Poly1305(key, nonce, associatedData, data)
// n is 0
ciphertext = AEAD_ChaCha20_Poly1305(k, n++, h, payload)
// MixHash(ciphertext)
// || below means append
h = SHA256(h || ciphertext);

// retain the chaining key ck for the data phase KDF
// retain the hash h for the data phase Additional Symmetric Key (SipHash) KDF

End of "se" message pattern.

// overwrite the temp_key in memory, no longer needed
temp_key = (all zeros)
```
### 3) SessionConfirmed

Alice posílá Bobovi.

Noise obsah: Alicin statický klíč Noise payload: Alicina RouterInfo a náhodné vyplnění Non-noise payload: žádný

(Vlastnosti zabezpečení datové části z [Noise](https://noiseprotocol.org/noise.html) )

```
XK(s, rs):           Authentication   Confidentiality
  -> s, se                  2                5

  Authentication: 2.
  Sender authentication resistant to key-compromise impersonation (KCI).  The
  sender authentication is based on an ephemeral-static DH ("es" or "se")
  between the sender's static key pair and the recipient's ephemeral key
  pair.  Assuming the corresponding private keys are secure, this
  authentication cannot be forged.

  Confidentiality: 5.
  Encryption to a known recipient, strong forward secrecy.  This payload is
  encrypted based on an ephemeral-ephemeral DH as well as an ephemeral-static
  DH with the recipient's static key pair.  Assuming the ephemeral private
  keys are secure, and the recipient is not being actively impersonated by an
  attacker that has stolen its static private key, this payload cannot be
  decrypted.

  "s": Alice writes her static public key from the s variable into the
  message buffer, encrypting it, and hashes the output along with the old h
  to derive a new h.

  "se": A DH is performed between the Alice's static key pair and the Bob's
  ephemeral key pair.  The result is hashed along with the old ck to derive a
  new ck and k, and n is set to zero.
```
Toto obsahuje dva ChaChaPoly rámce. První je Alicin šifrovaný statický veřejný klíč. Druhý je Noise payload: Alicina šifrovaná RouterInfo, volitelné možnosti a volitelné vyplnění. Používají různé klíče, protože mezi nimi je volána funkce MixKey().

Nezpracovaný obsah:

```
+----+----+----+----+----+----+----+----+
|                                       |
+   ChaCha20 encrypted data (32 bytes)  +
|   Alice static key S                  |
+     k defined in KDF for message 2    +
|   n = 1 see KDF for associated data   |
+----+----+----+----+----+----+----+----+
|                                       |
+        Poly1305 MAC (16 bytes)        +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+   ChaCha20 encrypted data             +
|     Length specified in message 1     |
+     (including 16 byte MAC to follow) +
|                                       |
+       Alice RouterInfo                +
|       using block format 2            |
+       Alice Options (optional)        +
|       using block format 1            |
+       Arbitrary padding               +
|       using block format 254          |
+                                       +
| k defined in KDF for message 3 part 2 |
+     n = 0                             +
|     see KDF for associated data       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+        Poly1305 MAC (16 bytes)        +
|                                       |
+----+----+----+----+----+----+----+----+

S :: 32 bytes, ChaChaPoly encrypted Alice's X25519 static key, little endian
     inside 48 byte ChaChaPoly frame
```
Nešifrovaná data (Poly1305 autentizační tagy nejsou zobrazeny):

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|              S                        |
+       Alice static key                +
|          (32 bytes)                   |
+                                       +
|                                       |
+                                       +
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|                                       |
+                                       +
|       Alice RouterInfo block          |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+       Optional Options block          +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+       Optional Padding block          +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

S :: 32 bytes, Alice's X25519 static key, little endian
```
#### Poznámky

- Bob musí provést běžnou validaci Router Info. Ujistit se, že typ podpisu je podporován, ověřit podpis, ověřit, že časové razítko je v mezích, a jakékoli další potřebné kontroly.

- Bob musí ověřit, že Alicin statický klíč přijatý v prvním rámci odpovídá statickému klíči v Router Info. Bob musí nejprve prohledat Router Info pro NTCP nebo NTCP2 Router Address s odpovídající verzí (v) možností. Viz sekce Published Router Info a Unpublished Router Info níže.

- Pokud má Bob starší verzi Alice RouterInfo ve své netdb, ověř, že statický klíč v router info je ve obou stejný, pokud je přítomen, a pokud je starší verze méně než XXX stará (viz doba rotace klíčů níže)

- Bob musí zde ověřit, že statický klíč Alice je platný bod na křivce.

- Možnosti by měly být zahrnuty pro specifikaci parametrů odsazení.

- Při jakékoli chybě, včetně selhání AEAD, RI, DH, časového razítka nebo validace klíče, musí Bob zastavit další zpracování zpráv a uzavřít spojení bez odpovědi. Mělo by se jednat o abnormální uzavření (TCP RST).

- Pro usnadnění rychlého handshaku musí implementace zajistit, že Alice vyrovná do bufferu a poté najednou vyprázdní celý obsah třetí zprávy, včetně obou AEAD rámců. To zvyšuje pravděpodobnost, že data budou obsažena v jediném TCP paketu (pokud nebudou segmentována OS nebo middleboxy) a Bob je přijme najednou. Slouží to také pro efektivitu a zajištění účinnosti náhodného paddingu.

- Délka rámce části 2 zprávy 3: Délku tohoto rámce (včetně MAC) posílá Alice ve zprávě 1. Viz tuto zprávu pro důležité poznámky o ponechání dostatečného prostoru pro padding.

- Obsah rámce části 2 zprávy 3: Formát tohoto rámce je stejný jako formát rámců datové fáze, s výjimkou toho, že délku rámce poslala Alice ve zprávě 1. Viz níže formát rámce datové fáze. Rámec musí obsahovat 1 až 3 bloky v následujícím pořadí:

1)  Blok Router Info Alice (povinný)   2)  Blok možností (volitelný)

3\) Padding blok (volitelný) Tento rámec nesmí nikdy obsahovat žádný jiný typ bloku.

- Výplň druhé části zprávy 3 není vyžadována, pokud Alice připojí rámec datové fáze (volitelně obsahující výplň) na konec zprávy 3 a pošle obě najednou, protože se pozorovateli budou jevit jako jeden velký proud bajtů. Jelikož Alice bude obecně, ale ne vždy, mít I2NP zprávu k odeslání Bobovi (proto se k němu připojila), je toto doporučená implementace kvůli efektivitě a zajištění účinnosti náhodné výplně.

- Teoretická maximální celková délka obou AEAD rámců zprávy 3 (části 1 a 2) je 65535 bajtů; část 1 má 48 bajtů, takže maximální délka rámce části 2 je 65487 bajtů; maximální délka otevřeného textu části 2 bez MAC je 65471 bajtů.
  VAROVÁNÍ: Některé implementace vynucují mnohem menší délky. Java I2P aktuálně omezuje celkovou délku na 4096 bajtů. Nepoužívejte nadměrné doplňování.

### Funkce pro odvození klíčů (KDF) (pro datovou fázi)

Fáze dat používá vstup přidružených dat s nulovou délkou.

KDF generuje dva šifrovací klíče k_ab a k_ba z chaining key ck, používá HMAC-SHA256(key, data) jak je definováno v [RFC-2104](https://tools.ietf.org/html/rfc2104). Toto je funkce Split(), přesně jak je definována ve specifikaci Noise.

```
ck = from handshake phase

// k_ab, k_ba = HKDF(ck, zerolen)
// ask_master = HKDF(ck, zerolen, info="ask")

// zerolen is a zero-length byte array
temp_key = HMAC-SHA256(ck, zerolen)
// overwrite the chaining key in memory, no longer needed
ck = (all zeros)

// Output 1
// cipher key, for Alice transmits to Bob (Noise doesn't make clear which is which, but Java code does)
k_ab =   HMAC-SHA256(temp_key, byte(0x01)).

// Output 2
// cipher key, for Bob transmits to Alice (Noise doesn't make clear which is which, but Java code does)
k_ba =   HMAC-SHA256(temp_key, k_ab || byte(0x02)).


KDF for SipHash for length field:
Generate an Additional Symmetric Key (ask) for SipHash
SipHash uses two 8-byte keys (big endian) and 8 byte IV for first data.

// "ask" is 3 bytes, US-ASCII, no null termination
ask_master = HMAC-SHA256(temp_key, "ask" || byte(0x01))
// sip_master = HKDF(ask_master, h || "siphash")
// "siphash" is 7 bytes, US-ASCII, no null termination
// overwrite previous temp_key in memory
// h is from KDF for message 3 part 2
temp_key = HMAC-SHA256(ask_master, h || "siphash")
// overwrite ask_master in memory, no longer needed
ask_master = (all zeros)
sip_master = HMAC-SHA256(temp_key, byte(0x01))

Alice to Bob SipHash k1, k2, IV:
// sipkeys_ab, sipkeys_ba = HKDF(sip_master, zerolen)
// overwrite previous temp_key in memory
temp_key = HMAC-SHA256(sip_master, zerolen)
// overwrite sip_master in memory, no longer needed
sip_master = (all zeros)

sipkeys_ab = HMAC-SHA256(temp_key, byte(0x01)).
sipk1_ab = sipkeys_ab[0:7], little endian
sipk2_ab = sipkeys_ab[8:15], little endian
sipiv_ab = sipkeys_ab[16:23]

Bob to Alice SipHash k1, k2, IV:

sipkeys_ba = HMAC-SHA256(temp_key, sipkeys_ab || byte(0x02)).
sipk1_ba = sipkeys_ba[0:7], little endian
sipk2_ba = sipkeys_ba[8:15], little endian
sipiv_ba = sipkeys_ba[16:23]

// overwrite the temp_key in memory, no longer needed
temp_key = (all zeros)
```
### 4) Fáze dat

Noise payload: Jak je definováno níže, včetně náhodného odsazení Non-noise payload: žádný

Počínaje 2. částí zprávy 3 jsou všechny zprávy uvnitř autentifikovaného a šifrovaného ChaChaPoly "rámce" s předřazenou dvoubajtovou obfuskovanou délkou. Veškeré vyplnění je uvnitř rámce. Uvnitř rámce je standardní formát s nulovými nebo více "bloky". Každý blok má jednobajtový typ a dvoubajtovou délku. Typy zahrnují datum/čas, I2NP zprávu, možnosti, ukončení a vyplnění.

Poznámka: Bob může, ale není povinen, poslat své RouterInfo Alici jako svou první zprávu Alici ve fázi dat.

(Vlastnosti zabezpečení payloadu z [Noise](https://noiseprotocol.org/noise.html) )

```
XK(s, rs):           Authentication   Confidentiality
  <-                        2                5
  ->                        2                5

  Authentication: 2.
  Sender authentication resistant to key-compromise impersonation (KCI).
  The sender authentication is based on an ephemeral-static DH ("es" or "se")
  between the sender's static key pair and the recipient's ephemeral key pair.
  Assuming the corresponding private keys are secure, this authentication cannot be forged.

  Confidentiality: 5.
  Encryption to a known recipient, strong forward secrecy.
  This payload is encrypted based on an ephemeral-ephemeral DH as well as
  an ephemeral-static DH with the recipient's static key pair.
  Assuming the ephemeral private keys are secure, and the recipient is not being actively impersonated
  by an attacker that has stolen its static private key, this payload cannot be decrypted.
```
#### Poznámky

- Pro efektivitu a minimalizaci identifikace pole délky musí implementace zajistit, že odesílatel ukládá do vyrovnávací paměti a poté vyprázdní celý obsah datových zpráv najednou, včetně pole délky a AEAD rámce. To zvyšuje pravděpodobnost, že data budou obsažena v jednom TCP paketu (pokud nebudou segmentována operačním systémem nebo middleboxy) a přijata najednou druhou stranou. Toto je také pro efektivitu a zajištění účinnosti náhodného paddingu.
- Router může zvolit ukončení relace při AEAD chybě, nebo může pokračovat v pokusech o komunikaci. Pokud pokračuje, router by měl ukončit relaci po opakovaných chybách.

#### SipHash zastřená délka

Reference: [SipHash](https://www.131002.net/siphash/)

Jakmile obě strany dokončí handshake, přenášejí payloady, které jsou poté šifrovány a autentifikovány v ChaChaPoly "rámcích".

Každý rámec je předcházen dvoubajtovou délkou ve formátu big endian. Tato délka specifikuje počet šifrovaných bajtů rámce, které následují, včetně MAC. Aby se zabránilo přenosu identifikovatelných polí délky v datovém proudu, je délka rámce obfuskována pomocí XOR s maskou odvozenou ze SipHash, jak byla inicializována z KDF datové fáze. Poznámka: oba směry mají jedinečné SipHash klíče a IV z KDF.

```
    sipk1, sipk2 = The SipHash keys from the KDF.  (two 8-byte long integers)
    IV[0] = sipiv = The SipHash IV from the KDF. (8 bytes)
    length is big endian.
    For each frame:
      IV[n] = SipHash-2-4(sipk1, sipk2, IV[n-1])
      Mask[n] = First 2 bytes of IV[n]
      obfuscatedLength = length ^ Mask[n]

    The first length output will be XORed with with IV[1].
```
Příjemce má identické SipHash klíče a IV. Dekódování délky se provádí odvozením masky použité k zamaskování délky a XOR operací zkráceného digestu pro získání délky rámce. Délka rámce je celková délka šifrovaného rámce včetně MAC.

#### Poznámky

- Pokud používáte funkci knihovny SipHash, která vrací unsigned long integer, použijte nejméně významné dva bajty jako Mask. Převeďte long integer na další IV jako little endian.

#### Surový obsah

```
+----+----+----+----+----+----+----+----+
|obf size |                             |
+----+----+                             +
|                                       |
+   ChaChaPoly frame                    +
|   Encrypted and authenticated         |
+   key is k_ab for Alice to Bob        +
|   key is k_ba for Bob to Alice        |
+   as defined in KDF for data phase    +
|   n starts at 0 and increments        |
+   for each frame in that direction    +
|   no associated data                  |
+   16 bytes minimum                    +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

obf size :: 2 bytes length obfuscated with SipHash
            when de-obfuscated: 16 - 65535

Minimum size including length field is 18 bytes.
Maximum size including length field is 65537 bytes.
Obfuscated length is 2 bytes.
Maximum ChaChaPoly frame is 65535 bytes.
```
#### Poznámky

- Jelikož příjemce musí získat celý rámec pro kontrolu MAC, doporučuje se, aby odesílatel omezil velikost rámců na několik KB namísto maximalizace velikosti rámce. Tím se minimalizuje latence u příjemce.

#### Nešifrovaná data

V šifrovaném rámci je nula nebo více bloků. Každý blok obsahuje jednobytový identifikátor, dvoubajtovou délku a nula nebo více bajtů dat.

Pro rozšiřitelnost musí příjemci ignorovat bloky s neznámými identifikátory a zacházet s nimi jako s výplní.

Šifrovaná data mají maximálně 65535 bytů, včetně 16bytové autentizační hlavičky, takže maximální nešifrovaná data jsou 65519 bytů.

(Poly1305 auth tag není zobrazen):

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
       0 for datetime
       1 for options
       2 for RouterInfo
       3 for I2NP message
       4 for termination
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

Ve zprávě handshake 3 část 2 musí být pořadí: RouterInfo, následované Options pokud jsou přítomny, následované Padding pokud je přítomno. Žádné jiné bloky nejsou povoleny.

Ve fázi dat není pořadí specifikováno, kromě následujících požadavků: Padding, pokud je přítomen, musí být posledním blokem. Termination, pokud je přítomen, musí být posledním blokem kromě Padding.

V jednom rámci může být více I2NP bloků. Více Padding bloků není v jednom rámci povoleno. Ostatní typy bloků pravděpodobně nebudou mít více bloků v jednom rámci, ale není to zakázáno.

#### DateTime

Speciální případ pro synchronizaci času:

```
+----+----+----+----+----+----+----+
| 0  |    4    |     timestamp     |
+----+----+----+----+----+----+----+

blk :: 0
size :: 2 bytes, big endian, value = 4
timestamp :: Unix timestamp, unsigned seconds.
             Wraps around in 2106
```
POZNÁMKA: Implementace musí zaokrouhlovat na nejbližší sekundu, aby se zabránilo časovému zkreslení v síti.

#### Možnosti

Předejte aktualizované možnosti. Možnosti zahrnují: Minimální a maximální padding.

Blok možností bude mít proměnnou délku.

```
+----+----+----+----+----+----+----+----+
| 1  |  size   |tmin|tmax|rmin|rmax|tdmy|
+----+----+----+----+----+----+----+----+
|tdmy|  rdmy   |  tdelay |  rdelay |    |
~----+----+----+----+----+----+----+    ~
|              more_options             |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 1
size :: 2 bytes, big endian, size of options to follow, 12 bytes minimum

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

Padding distribution specified as additional parameters?
Random delay specified as additional parameters?

more_options :: Format TBD
```
#### Problémy s možnostmi

- Formát možností je zatím neurčen.
- Vyjednávání možností je zatím neurčeno.

#### RouterInfo

Předej RouterInfo Alice Bobovi. Používá se ve zprávě handshake 3 část 2. Předej RouterInfo Alice Bobovi, nebo Bobovu Alici. Používá se volitelně ve fázi dat.

```
+----+----+----+----+----+----+----+----+
| 2  |  size   |flg |    RouterInfo     |
+----+----+----+----+                   +
| (Alice RI in handshake msg 3 part 2)  |
~ (Alice, Bob, or third-party           ~
|  RI in data phase)                    |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 2
size :: 2 bytes, big endian, size of flag + router info to follow
flg :: 1 byte flags
       bit order: 76543210
       bit 0: 0 for local store, 1 for flood request
       bits 7-1: Unused, set to 0 for future compatibility
routerinfo :: Alice's or Bob's RouterInfo
```
#### Poznámky

- Při použití ve fázi dat musí příjemce (Alice nebo Bob) ověřit, že se jedná o stejný Router Hash, jaký byl původně odeslán (pro Alice) nebo na který byl odeslán (pro Bob). Poté s ním nakládat jako s místní I2NP DatabaseStore Message. Ověřit podpis, ověřit novější časové razítko a uložit do místní netDb. Pokud je flag bit 0 nastaven na 1 a přijímající strana je floodfill, nakládat s ním jako s DatabaseStore Message s nenulovým reply tokenem a zaplavit jej k nejbližším floodfillům.
- Router Info NENÍ komprimován gzip (na rozdíl od DatabaseStore Message, kde komprimován je)
- Flooding nesmí být vyžádán, pokud RouterInfo neobsahuje publikované RouterAddresses. Přijímající router nesmí RouterInfo zaplavit, pokud v něm nejsou publikované RouterAddresses.
- Implementátoři musí zajistit, že při čtení bloku nebudou poškozená nebo škodlivá data způsobovat přečtení do dalšího bloku.
- Tento protokol neposkytuje potvrzení, že RouterInfo byl přijat, uložen nebo zaplavěn (ani ve fázi handshake ani ve fázi dat). Pokud je potvrzení žádoucí a příjemce je floodfill, měl by odesílatel místo toho poslat standardní I2NP DatabaseStoreMessage s reply tokenem.

#### Problémy

- Mohlo by být také použito ve fázi dat, místo I2NP DatabaseStoreMessage. Například Bob by to mohl použít k zahájení fáze dat.
- Je dovoleno, aby toto obsahovalo RI pro routery jiné než původce, jako obecná náhrada za DatabaseStoreMessages, např. pro flooding floodfilly?

#### I2NP Message

Jedna I2NP zpráva s upravenou hlavičkou. I2NP zprávy nesmí být fragmentovány napříč bloky nebo napříč ChaChaPoly rámci.

Toto používá prvních 9 bajtů ze standardní NTCP I2NP hlavičky a odstraňuje posledních 7 bajtů hlavičky následovně: zkrátí expiraci z 8 na 4 bajty (sekundy místo milisekund, stejně jako pro SSU), odstraní 2-bajtovou délku (použije velikost bloku - 9) a odstraní jednobajtový SHA256 kontrolní součet.

```
+----+----+----+----+----+----+----+----+
| 3  |  size   |type|    msg id         |
+----+----+----+----+----+----+----+----+
|   short exp       |     message       |
+----+----+----+----+                   +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 3
size :: 2 bytes, big endian, size of type + msg id + exp + message to follow
        I2NP message body size is (size - 9).
type :: 1 byte, I2NP msg type, see I2NP spec
msg id :: 4 bytes, big endian, I2NP message ID
short exp :: 4 bytes, big endian, I2NP message expiration, Unix timestamp, unsigned seconds.
             Wraps around in 2106
message :: I2NP message body
```
#### Poznámky

- Implementátoři musí zajistit, že při čtení bloku nebudou poškozená nebo škodlivá data způsobovat přečtení do následujícího bloku.

#### Ukončení

Noise doporučuje explicitní zprávu o ukončení. Původní NTCP ji nemá. Ukončit spojení. Toto musí být poslední blok bez výplně v rámci.

```
+----+----+----+----+----+----+----+----+
| 4  |  size   |    valid data frames   |
+----+----+----+----+----+----+----+----+
    received   | rsn|     addl data     |
+----+----+----+----+                   +
~               .   .   .               ~
+----+----+----+----+----+----+----+----+

blk :: 4
size :: 2 bytes, big endian, value = 9 or more
valid data frames received :: The number of valid AEAD data phase frames received
                              (current receive nonce value)
                              0 if error occurs in handshake phase
                              8 bytes, big endian
rsn :: reason, 1 byte:
       0: normal close or unspecified
       1: termination received
       2: idle timeout
       3: router shutdown
       4: data phase AEAD failure
       5: incompatible options
       6: incompatible signature type
       7: clock skew
       8: padding violation
       9: AEAD framing error
       10: payload format error
       11: message 1 error
       12: message 2 error
       13: message 3 error
       14: intra-frame read timeout
       15: RI signature verification fail
       16: s parameter missing, invalid, or mismatched in RouterInfo
       17: banned
addl data :: optional, 0 or more bytes, for future expansion, debugging,
             or reason text.
             Format unspecified and may vary based on reason code.
```
#### Poznámky

Ne všechny důvody mohou být skutečně použity, závisí na implementaci. Selhání handshaku obecně povede k uzavření s TCP RST místo toho. Viz poznámky v sekcích zpráv handshaku výše. Dodatečné uvedené důvody jsou pro konzistenci, logování, ladění nebo v případě změn zásad.

#### Padding

Toto je pro padding uvnitř AEAD rámců. Padding pro zprávy 1 a 2 jsou mimo AEAD rámce. Veškerý padding pro zprávu 3 a datovou fázi jsou uvnitř AEAD rámců.

Padding uvnitř AEAD by mělo přibližně odpovídat vyjednaným parametrům. Bob poslal své požadované tx/rx min/max parametry ve zprávě 2. Alice poslala své požadované tx/rx min/max parametry ve zprávě 3. Aktualizované možnosti mohou být poslány během datové fáze. Viz informace o bloku možností výše.

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
size :: 2 bytes, big endian, size of padding to follow
padding :: random data
```
#### Poznámky

- Velikost = 0 je povolena.
- Strategie paddingu TBD.
- Minimální padding TBD.
- Pouze paddingové rámce jsou povoleny.
- Výchozí padding TBD.
- Viz blok options pro vyjednávání parametrů paddingu
- Viz blok options pro parametry min/max paddingu
- Noise omezuje zprávy na 64KB. Pokud je potřeba více paddingu, pošlete více rámců.
- Odpověď routeru na porušení vyjednaného paddingu je závislá na implementaci.

#### Další typy bloků

Implementace by měly ignorovat neznámé typy bloků kvůli zpětné kompatibilitě, s výjimkou zprávy 3 části 2, kde neznámé bloky nejsou povoleny.

#### Budoucí práce

- Délka paddingu má být buď rozhodnuta na základě jednotlivých zpráv a odhadů distribuce délek, nebo by měly být přidány náhodné prodlevy. Tato protiopatření mají být zahrnuta pro odolnost vůči DPI, protože velikosti zpráv by jinak odhalily, že I2P provoz je přenášen transportním protokolem. Přesné schéma paddingu je oblastí budoucí práce.

### 5) Ukončení

Připojení mohou být ukončena normálním nebo abnormálním uzavřením TCP socketu, nebo, jak Noise doporučuje, explicitní ukončovací zprávou. Explicitní ukončovací zpráva je definována ve fázi dat výše.

Při jakémkoli normálním nebo abnormálním ukončení by routery měly vynulovat veškerá dočasná data v paměti, včetně dočasných klíčů handshaku, symetrických kryptografických klíčů a souvisejících informací.

## Publikované informace o router

### Možnosti

Od verze 0.9.50 je možnost "caps" podporována v NTCP2 adresách, podobně jako u SSU. V možnosti "caps" může být publikována jedna nebo více schopností. Schopnosti mohou být v libovolném pořadí, ale "46" je doporučené pořadí pro konzistenci napříč implementacemi. Jsou definovány dvě schopnosti:

4: Označuje odchozí IPv4 schopnost. Pokud je IP adresa publikována v poli host, tato schopnost není nutná. Pokud je router skrytý nebo je NTCP2 pouze odchozí, '4' a '6' mohou být zkombinované v jedné adrese.

6: Označuje schopnost odchozího IPv6. Pokud je IP publikována v poli hostitele, tato schopnost není nutná. Pokud je router skrytý, nebo je NTCP2 pouze odchozí, '4' a '6' mohou být zkombinována v jedné adrese.

### Publikované adresy

Publikovaná RouterAddress (část RouterInfo) bude mít identifikátor protokolu buď "NTCP" nebo "NTCP2".

RouterAddress musí obsahovat možnosti "host" a "port", jako v současném NTCP protokolu.

RouterAddress musí obsahovat tři možnosti pro indikaci podpory NTCP2:

- s=(Base64 klíč) Aktuální Noise statický veřejný klíč (s) pro tuto RouterAddress. Kódován Base 64 pomocí standardní I2P Base 64 abecedy. 32 bytů v binární podobě, 44 bytů jako Base 64 kódovaný, little-endian X25519 veřejný klíč.
- i=(Base64 IV) Aktuální IV pro šifrování hodnoty X ve zprávě 1 pro tuto RouterAddress. Kódován Base 64 pomocí standardní I2P Base 64 abecedy. 16 bytů v binární podobě, 24 bytů jako Base 64 kódovaný, big-endian.
- v=2 Aktuální verze (2). Když je publikováno jako "NTCP", je implikována dodatečná podpora pro verzi 1. Podpora budoucích verzí bude s hodnotami oddělenými čárkami, např. v=2,3 Implementace by měla ověřit kompatibilitu, včetně více verzí pokud je přítomna čárka. Verze oddělené čárkami musí být v číselném pořadí.

Alice musí ověřit, že všechny tři možnosti jsou přítomné a platné před připojením pomocí protokolu NTCP2.

Když je publikována jako "NTCP" s možnostmi "s", "i" a "v", router musí přijímat příchozí spojení na daném hostiteli a portu pro protokoly NTCP i NTCP2 a automaticky detekovat verzi protokolu.

Když je publikováno jako "NTCP2" s možnostmi "s", "i" a "v", router přijímá příchozí připojení na tomto hostiteli a portu pouze pro protokol NTCP2.

Pokud router podporuje jak NTCP1, tak NTCP2 připojení, ale neimplementuje automatickou detekci verze pro příchozí připojení, musí inzerovat jak "NTCP", tak "NTCP2" adresy a zahrnout NTCP2 možnosti pouze v "NTCP2" adrese. Router by měl nastavit nižší hodnotu nákladů (vyšší prioritu) v "NTCP2" adrese než v "NTCP" adrese, takže NTCP2 je preferováno.

Pokud je ve stejném RouterInfo publikováno více NTCP2 RouterAddresses (buď jako "NTCP" nebo "NTCP2") (pro dodatečné IP adresy nebo porty), všechny adresy specifikující stejný port musí obsahovat identické NTCP2 možnosti a hodnoty. Konkrétně všechny musí obsahovat stejný statický klíč a iv.

### Nepublikovaná NTCP2 adresa

Pokud Alice nepublikuje svou NTCP2 adresu (jako "NTCP" nebo "NTCP2") pro příchozí spojení, musí publikovat "NTCP2" router adresu obsahující pouze svůj statický klíč a NTCP2 verzi, aby Bob mohl ověřit klíč poté, co obdrží Alice RouterInfo ve zprávě 3 část 2.

- s=(Base64 klíč) Jak je definováno výše pro publikované adresy.
- v=2 Jak je definováno výše pro publikované adresy.

Tato adresa routeru nebude obsahovat možnosti "i", "host" nebo "port", protože tyto nejsou vyžadovány pro odchozí NTCP2 spojení. Publikované náklady pro tuto adresu nejsou striktně důležité, protože je pouze příchozí; nicméně může být užitečné pro ostatní routery, pokud jsou náklady nastaveny výše (nižší priorita) než u jiných adres. Doporučená hodnota je 14.

Alice může také jednoduše přidat možnosti "s" a "v" k existující publikované NTCP adrese.

### Rotace veřejného klíče a IV

Kvůli ukládání RouterInfo do mezipaměti nesmí routery rotovat statický veřejný klíč nebo IV, když je router v provozu, ať už v publikované adrese nebo ne. Routery musí tento klíč a IV trvale uložit pro opětovné použití po okamžitém restartu, aby příchozí spojení nadále fungovala a časy restartů nebyly odhaleny. Routery musí trvale uložit, nebo jinak určit, čas posledního vypnutí, aby mohl být při startu vypočítán čas předchozího výpadku.

S ohledem na obavy z odhalení časů restartů mohou routery rotovat tento klíč nebo IV při spuštění, pokud byl router předtím vypnutý po určitou dobu (alespoň několik hodin).

Pokud má router nějaké publikované NTCP2 RouterAddresses (jako NTCP nebo NTCP2), minimální doba odstavení před rotací by měla být mnohem delší, například jeden měsíc, pokud se nezměnila lokální IP adresa nebo router neprovede "rekeys".

Pokud má router jakékoliv publikované SSU RouterAddresses, ale ne NTCP2 (jako NTCP nebo NTCP2), minimální doba nečinnosti před rotací by měla být delší, například jeden den, pokud se nezměnila místní IP adresa nebo router neprovede "rekeys". To platí i když publikovaná SSU adresa má introducery.

Pokud router nemá žádné publikované RouterAddresses (NTCP, NTCP2, nebo SSU), minimální doba nečinnosti před rotací může být pouhé dvě hodiny, i když se změní IP adresa, pokud router neprovede "rekeys".

Pokud router provede "rekey" na jiný Router Hash, měl by také vygenerovat nový noise klíč a IV.

Implementace si musí být vědomy toho, že změna statického veřejného klíče nebo IV zabrání příchozím NTCP2 spojením od routerů, které mají uložený starší RouterInfo. Publikování RouterInfo, výběr tunnel peerů (včetně OBGW i IB nejbližších hopů), výběr zero-hop tunelů, výběr transportu a další implementační strategie to musí brát v úvahu.

Rotace IV podléhá stejným pravidlům jako rotace klíčů, s výjimkou toho, že IV nejsou přítomny kromě publikovaných RouterAddresses, takže pro skryté nebo za firewallem chráněné routery neexistuje žádné IV. Pokud se něco změní (verze, klíč, možnosti?), doporučuje se, aby se změnilo také IV.

Poznámka: Minimální doba nečinnosti před přegenerováním klíčů může být upravena za účelem zajištění zdraví sítě a zamezení opětovnému seedování u routeru, který byl nedostupný po mírně delší dobu.

## Detekce verze

Když je publikován jako "NTCP", router musí automaticky detekovat verzi protokolu pro příchozí spojení.

Tato detekce závisí na implementaci, ale zde je několik obecných pokynů.

Pro detekci verze příchozího NTCP spojení Bob postupuje následovně:

- Čekejte alespoň na 64 bajtů (minimální velikost NTCP2 zprávy 1)

- Pokud jsou prvotní přijatá data 288 nebo více bajtů, příchozí spojení je verze 1.

- Pokud méně než 288 bajtů, pak buď

> - Počkat krátkou dobu na více dat (dobrá strategie před rozšířeným přijetím NTCP2), pokud je celkem přijato alespoň 288, je to NTCP 1.   >   > - Zkusit první fáze dekódování jako verze 2, pokud selže, počkat krátkou dobu na více dat (dobrá strategie po rozšířeném přijetí NTCP2)   >   >   > - Dešifrovat prvních 32 bajtů (X klíč) SessionRequest paketu pomocí AES-256 s klíčem RH_B.   >   > - Ověřit platný bod na křivce. Pokud selže, počkat krátkou dobu na více dat pro NTCP 1   >   > - Ověřit AEAD rámec. Pokud selže, počkat krátkou dobu na více dat pro NTCP 1

Upozorňujeme, že změny nebo dodatečné strategie mohou být doporučeny, pokud detekujeme aktivní útoky TCP segmentace na NTCP 1.

Pro usnadnění rychlé detekce verze a handshake musí implementace zajistit, aby Alice ukládala do bufferu a poté vyprázdnila celý obsah první zprávy najednou, včetně paddingu. Tím se zvyšuje pravděpodobnost, že data budou obsažena v jediném TCP paketu (pokud nebudou segmentována OS nebo middleboxy) a Bob je přijme všechna najednou. Toto je také pro efektivitu a pro zajištění účinnosti náhodného paddingu. Toto se vztahuje na handshake jak u NTCP, tak u NTCP2.

## Varianty, záložní řešení a obecné problémy

- Pokud Alice i Bob podporují NTCP2, Alice by se měla připojit pomocí NTCP2.
- Pokud se Alice nepodaří připojit k Bobovi pomocí NTCP2 z jakéhokoli důvodu, připojení selže. Alice se nesmí pokusit o opětovné připojení pomocí NTCP 1.

## Pokyny pro odchylku hodin

Časové značky peerů jsou zahrnuty v prvních dvou handshake zprávách, Session Request a Session Created. Časový posun mezi dvěma peery větší než +/- 60 sekund je obecně fatální. Pokud si Bob myslí, že jeho místní hodiny jsou špatné, může upravit své hodiny pomocí vypočítaného posunu nebo nějakého externího zdroje. Jinak by Bob měl odpovědět Session Created, i když je maximální posun překročen, spíše než jednoduše zavřít spojení. To umožňuje Alici získat Bobovu časovou značku a vypočítat posun a v případě potřeby podniknout kroky. Bob v tomto okamžiku nemá identitu Alice routeru, ale pro úsporu zdrojů může být žádoucí, aby Bob zakázal příchozí spojení z Alice IP na určité časové období, nebo po opakovaných pokusech o připojení s nadměrným posunem.

Alice by měla upravit vypočítaný posun hodin odečtením poloviny RTT. Pokud si Alice myslí, že její místní hodiny jsou špatné, může upravit své hodiny pomocí vypočítaného posunu nebo některého externího zdroje. Pokud si Alice myslí, že Bobovy hodiny jsou špatné, může Boba zakázat na určité období. V každém případě by Alice měla ukončit spojení.

Pokud Alice skutečně odpoví pomocí Session Confirmed (pravděpodobně proto, že skew je velmi blízko k limitu 60s a výpočty Alice a Boba nejsou úplně stejné kvůli RTT), Bob by měl upravit vypočítané zpoždění hodin odečtením poloviny RTT. Pokud upravené zpoždění hodin překročí maximum, Bob by pak měl odpovědět zprávou Disconnect obsahující kód důvodu zpoždění hodin a uzavřít spojení. V tomto okamžiku má Bob identitu router Alice a může Alice zakázat na určité časové období.

## Reference

- [Společné struktury](/docs/specs/common-structures)
- [I2NP](/docs/specs/i2np)
- [Network Database](/docs/overview/network-database)
- [NOISE - Noise Protocol Framework](https://noiseprotocol.org/noise.html)
- [NTCP](/docs/transport/ntcp)
- [Prop104](/proposals/104-tls-transport)
- [Prop109](/proposals/109-pt-transport)
- [Prop111](/proposals/111-ntcp-2)
- [RFC-2104 - HMAC](https://tools.ietf.org/html/rfc2104)
- [RFC-3526 - DH Groups](https://tools.ietf.org/html/rfc3526)
- [RFC-6151](https://tools.ietf.org/html/rfc6151)
- [RFC-7539 - ChaCha20-Poly1305](https://tools.ietf.org/html/rfc7539)
- [RFC-7748 - X25519](https://tools.ietf.org/html/rfc7748)
- [RFC-7905](https://tools.ietf.org/html/rfc7905)
- [SipHash](https://www.131002.net/siphash/)
- [SSU](/docs/transport/ssu)
- **[STS]** Diffie, W.; van Oorschot P. C.; Wiener M. J., Authentication and Authenticated Key Exchanges
