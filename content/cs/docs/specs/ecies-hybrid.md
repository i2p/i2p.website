---
title: "PQ Hybrid ECIES-X25519-AEAD-Ratchet"
description: "Post-kvantová hybridní varianta šifrovacího protokolu ECIES používající ML-KEM"
slug: "ecies-hybrid"
category: "Protokoly"
lastUpdated: "2026-04"
accurateFor: "0.9.69"
---

## Poznámka

Implementace, testování a nasazování probíhá v různých implementacích routeru. Zkontrolujte dokumentaci těchto implementací pro aktuální stav.

## Přehled

Toto je PQ Hybrid varianta protokolu ECIES-X25519-AEAD-Ratchet [ECIES](/docs/specs/ecies/). Je to první fáze celkového PQ návrhu [Prop169](/proposals/169-pq-crypto/), která byla schválena. Podívejte se na tento návrh pro celkové cíle, modely hrozeb, analýzu, alternativy a další informace.

Tato specifikace obsahuje pouze rozdíly oproti standardnímu [ECIES](/docs/specs/ecies/) a musí být čtena ve spojení s touto specifikací.

## Návrh

Podporujeme standard NIST FIPS 203 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf), který je založen na CRYSTALS-Kyber, ale NENÍ s ním kompatibilní.

Hybrid handshakes jsou specifikovány v [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf).

### Výměna klíčů

Definujeme hybridní výměnu klíčů pro Ratchet. PQ KEM poskytuje pouze dočasné klíče a přímo nepodporuje handshaky se statickými klíči, jako je Noise IK.

Definujeme tři varianty ML-KEM podle [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf), celkem pro 3 nové typy šifrování. Hybridní typy jsou definovány pouze v kombinaci s X25519.

Nové typy šifrování jsou:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Code</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
</tr>
</table>
Režie bude značná. Typické velikosti zpráv 1 a 2 (pro IK) jsou aktuálně kolem 100 bajtů (před jakýmkoliv dodatečným payloadem). To se zvýší 8x až 15x v závislosti na algoritmu.

### Nová kryptografie vyžadována

- ML-KEM (dříve CRYSTALS-Kyber) [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
- SHA3-128 (dříve Keccak-256) [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf) Používá se pouze pro SHAKE128
- SHA3-256 (dříve Keccak-512) [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
- SHAKE128 a SHAKE256 (XOF rozšíření pro SHA3-128 a SHA3-256)
  [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)

Testovací vektory pro SHA3-256, SHAKE128 a SHAKE256 jsou dostupné na [NIST-VECTORS](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values).

Všimněte si, že Java knihovna bouncycastle podporuje vše výše uvedené. Podpora C++ knihovny je v OpenSSL 3.5 [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

## Specifikace

### Běžné struktury

Viz specifikaci běžných struktur [COMMON](/docs/specs/common-structures/) pro délky klíčů a identifikátory.

### Vzory handshake

Handshaky používají [Noise](https://noiseprotocol.org/noise.html) handshake vzory.

Používá se následující mapování písmen:

- e = jednorázový dočasný klíč
- s = statický klíč
- p = datová část zprávy
- e1 = jednorázový dočasný PQ klíč, odeslaný od Alice k Bobovi
- ekem1 = šifrovaný text KEM, odeslaný od Boba k Alice

Následující úpravy XK a IK pro hybridní dopřednou bezpečnost (hfs) jsou specifikovány v [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) sekci 5:

```
IK:                         IKhfs:
<- s                        <- s
...                         ...
-> e, es, s, ss, p          -> e, es, e1, s, ss, p
<- tag, e, ee, se, p        <- tag, e, ee, ekem1, se, p
<- p                        <- p
p ->                        p ->

e1 and ekem1 are encrypted. See pattern definitions below.
NOTE: e1 and ekem1 are different sizes (unlike X25519)
```
Vzor e1 je definován následovně, jak je specifikováno v [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) sekci 4:

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
Vzor ekem1 je definován následovně, jak je specifikováno v [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) sekci 4:

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
### Definované operace ML-KEM

Definujeme následující funkce odpovídající kryptografickým stavebním blokům použitým podle definice v [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

**(encap_key, decap_key) = PQ_KEYGEN()**

Alice vytvoří klíče pro enkapsulaci a dekapsulaci. Klíč pro enkapsulaci je odeslán ve zprávě NS. Velikosti encap_key a decap_key se liší podle varianty ML-KEM.

**(ciphertext, kem_shared_key) = ENCAPS(encap_key)**

Bob vypočítá šifrový text a sdílený klíč pomocí šifrového textu přijatého v NS zprávě. Šifrový text je odeslán v NSR zprávě. Velikost šifrového textu se liší podle varianty ML-KEM. kem_shared_key má vždy 32 bytů.

**kem_shared_key = DECAPS(ciphertext, decap_key)**

Alice vypočítá sdílený klíč pomocí šifrovaného textu přijatého v NSR zprávě. Kem_shared_key je vždy 32 bajtů.

Všimněte si, že jak encap_key, tak ciphertext jsou šifrovány uvnitř ChaCha/Poly bloků v Noise handshake zprávách 1 a 2. Budou dešifrovány jako součást procesu handshake.

Hodnota kem_shared_key je smíchána do chaining key pomocí MixHash(). Podrobnosti viz níže.

### Noise Handshake KDF

#### Přehled

Hybridní handshake je definován v [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf). První zpráva, od Alice k Bobovi, obsahuje e1, enkapsulační klíč, před užitečným obsahem zprávy. Tento je zpracován jako dodatečný statický klíč; zavolejte na něj EncryptAndHash() (jako Alice) nebo DecryptAndHash() (jako Bob). Poté zpracujte užitečný obsah zprávy jako obvykle.

Druhá zpráva, od Boba k Alici, obsahuje ekem1, šifrovaný text, před payload zprávy. To je považováno za dodatečný statický klíč; zavolejte na něj EncryptAndHash() (jako Bob) nebo DecryptAndHash() (jako Alice). Poté vypočítejte kem_shared_key a zavolejte MixKey(kem_shared_key). Poté zpracujte payload zprávy obvyklým způsobem.

#### Identifikátory Noise

Toto jsou Noise inicializační řetězce:

- "Noise_IKhfselg2_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM1024_ChaChaPoly_SHA256"

#### Alice KDF pro NS zprávu

Po vzoru zprávy 'es' a před vzorem zprávy 's' přidejte:

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

NOTE: For the next section (static key for IK),
the keydata and chain key remain the same, and n now equals 1
(instead of 0 for non-hybrid).
```
#### Bob KDF pro NS zprávu

Po vzoru zprávy 'es' a před vzorem zprávy 's' přidejte:

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

NOTE: For the next section (static key for IK),
the keydata and chain key remain the same, and n now equals 1
(instead of 0 for non-hybrid).
```
#### Bob KDF pro NSR zprávu

Po vzoru zprávy 'ee' a před vzorem zprávy 'se' přidejte:

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
```
#### Alice KDF pro NSR zprávu

Po vzoru zprávy 'ee' a před vzorem zprávy 'ss' přidejte:

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
```
#### KDF pro split()

nezměněno

### Formát zprávy

#### Formát NS

Změny: Současný ratchet obsahoval statický klíč v první ChaCha sekci a payload ve druhé sekci. S ML-KEM jsou nyní tři sekce. První sekce obsahuje šifrovaný PQ veřejný klíč. Druhá sekce obsahuje statický klíč. Třetí sekce obsahuje payload.

Šifrovaný formát:

```
+----+----+----+----+----+----+----+----+
|                                       |
+         New Session Ephemeral         +
|            Public Key                 |
+            32 bytes                   +
|      Encoded with Elligator2          |
+----+----+----+----+----+----+----+----+
|                                       |
+         ML-KEM encap_key              +
|       ChaCha20 encrypted data         |
+   (see table below for length)        +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+      (MAC) for encap_key Section      +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
|                                       |
+         X25519 Static Key             +
|       ChaCha20 encrypted data         |
+            32 bytes                   +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+     (MAC) for Static Key Section      +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
|                                       |
+          Payload Section              +
|       ChaCha20 encrypted data         |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+      (MAC) for Payload Section        +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
```
Dešifrovaný formát:

```
Payload Part 1:

+----+----+----+----+----+----+----+----+
|                                       |
+         ML-KEM encap_key              +
|                                       |
+   (see table below for length)        +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

Payload Part 2:

+----+----+----+----+----+----+----+----+
|                                       |
+         X25519 Static Key             +
|            (32 bytes)                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

Payload Part 3:

+----+----+----+----+----+----+----+----+
|                                       |
+          Payload Section              +
|                                       |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
Velikosti:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">X len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NS len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NS Enc len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NS Dec len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">PQ key len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">pl len</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">96+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">64+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">--</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">912+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">880+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">800+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">800</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1296+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1360+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1184+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1184</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1680+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1648+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1568+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1568</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
</table>
Upozorňujeme, že payload musí obsahovat DateTime blok, takže minimální velikost payload je 7. Minimální velikosti NS lze vypočítat odpovídajícím způsobem.

#### Formát NSR

Změny: Současný ratchet má prázdný payload pro první ChaCha sekci a payload ve druhé sekci. S ML-KEM jsou nyní tři sekce. První sekce obsahuje šifrovaný PQ ciphertext. Druhá sekce má prázdný payload. Třetí sekce obsahuje payload.

Šifrovaný formát:

```
+----+----+----+----+----+----+----+----+
|       Session Tag 8 bytes             |
+----+----+----+----+----+----+----+----+
|                                       |
+       Ephemeral Public Key            +
|            32 bytes                   |
+      Encoded with Elligator2          +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+         ML-KEM ciphertext             +
|       ChaCha20 encrypted data         |
+   (see table below for length)        +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+     (MAC) for ciphertext Section      +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+   (MAC) for key Section (no data)     +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
|                                       |
+          Payload Section              +
|       ChaCha20 encrypted data         |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+      (MAC) for Payload Section        +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
```
Dešifrovaný formát:

```
Payload Part 1:

+----+----+----+----+----+----+----+----+
|                                       |
+         ML-KEM ciphertext             +
|                                       |
+   (see table below for length)        +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

Payload Part 2:

empty

Payload Part 3:

+----+----+----+----+----+----+----+----+
|                                       |
+          Payload Section              +
|                                       |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
Velikosti:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Y len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NSR len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NSR Enc len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NSR Dec len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">PQ CT len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">opt len</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">72+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">--</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">856+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">816+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">768+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">768</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1176+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1136+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1088+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1088</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1656+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1616+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1568+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1568</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
</table>
Všimněte si, že zatímco NSR bude normálně mít nenulový payload, specifikace ratchet [ECIES](/docs/specs/ecies/) to nevyžaduje, takže minimální velikost payload je 0. Minimální velikosti NSR lze vypočítat odpovídajícím způsobem.

## Analýza režie

### Výměna klíčů

Nárůst velikosti (bajty):

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Pubkey (NS)</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Ciphertext (NSR)</th>
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
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+1584</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+1584</td>
</tr>
</table>
Rychlost:

Rychlosti podle [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/):

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Relative speed</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">X25519 DH/keygen</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">baseline</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2.25x faster</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1.5x faster</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1x (same)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">XK</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4x DH (keygen + 3 DH)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4x DH + 2x PQ (keygen + enc/dec) = 4.9x DH = 22% slower</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4x DH + 2x PQ (keygen + enc/dec) = 5.3x DH = 32% slower</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4x DH + 2x PQ (keygen + enc/dec) = 6x DH = 50% slower</td>
</tr>
</table>
## Analýza bezpečnosti

Bezpečnostní kategorie NIST jsou shrnuty v [NIST-PQ-END](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf) snímek 10. Předběžná kritéria: Naša minimální bezpečnostní kategorie NIST by měla být 2 pro hybridní protokoly a 3 pro pouze PQ.

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

Všechny tyto protokoly jsou hybridní. Pravděpodobně bude třeba upřednostnit MLKEM768; MLKEM512 není dostatečně bezpečný.

Bezpečnostní kategorie NIST [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf):

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
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
</tr>
</table>
## Předvolby typu

Doporučený typ pro počáteční podporu, založený na kategorii zabezpečení a délce klíče, je:

MLKEM768_X25519 (typ 6)

## Poznámky k implementaci

### Podpora knihoven

Knihovny Bouncycastle, BoringSSL a WolfSSL nyní podporují MLKEM. Podpora OpenSSL je v jejich vydání 3.5 z 8. dubna 2025 [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

### Sdílené tunnely

Automatická klasifikace/detekce více protokolů na stejných tunelech by měla být možná na základě kontroly délky zprávy 1 (New Session Message). Použijeme-li jako příklad MLKEM512_X25519, délka zprávy 1 je o 816 bajtů větší než současný ratchet protokol a minimální velikost zprávy 1 (pouze s DateTime payload) je 919 bajtů. Většina velikostí zpráv 1 se současným ratchet má payload menší než 816 bajtů, takže mohou být klasifikovány jako non-hybrid ratchet. Velké zprávy jsou pravděpodobně POST požadavky, které jsou vzácné.

Doporučená strategie je tedy:

- Pokud je zpráva 1 menší než 919 bajtů, jedná se o aktuální ratchet
  protokol.
- Pokud je zpráva 1 větší nebo rovna 919 bajtům, pravděpodobně se jedná o
  MLKEM512_X25519. Zkuste nejprve MLKEM512_X25519, a pokud selže, zkuste
  aktuální ratchet protokol.

To nám umožní efektivně podporovat standardní ratchet a hybridní ratchet na stejné destinaci, stejně jako jsme dříve podporovali ElGamal a ratchet na stejné destinaci. Proto můžeme migrovat na hybridní protokol MLKEM mnohem rychleji, než kdybychom nemohli podporovat duální protokoly pro stejnou destinaci, protože můžeme přidat podporu MLKEM do existujících destinací.

Požadované podporované kombinace jsou:

- X25519 + MLKEM512
- X25519 + MLKEM768
- X25519 + MLKEM1024

Následující kombinace mohou být složité a NENÍ vyžadováno, aby byly podporovány, ale mohou být, v závislosti na implementaci:

- Více než jeden MLKEM
- ElG + jeden nebo více MLKEM
- X25519 + jeden nebo více MLKEM
- ElG + X25519 + jeden nebo více MLKEM

Není požadována podpora více MLKEM algoritmů (například MLKEM512_X25519 a MLKEM_768_X25519) na stejné destinaci. Vyberte jen jeden. Závisí na implementaci.

Není nutné podporovat tři algoritmy (například X25519, MLKEM512_X25519 a MLKEM769_X25519) na stejné destinaci. Klasifikace a strategie opakování může být příliš složitá. Konfigurace a konfigurační rozhraní může být příliš složité. Závisí na implementaci.

Není vyžadováno podporovat ElGamal a hybridní algoritmy na stejné destinaci. ElGamal je zastaralý a ElGamal + hybridní pouze (bez X25519) nedává příliš smysl. Také ElGamal a Hybrid New Session Messages jsou obě velké, takže klasifikační strategie by často musely vyzkoušet obě dešifrování, což by bylo neefektivní. Závisí na implementaci.

Klienti mohou používat stejné nebo různé statické klíče X25519 pro protokoly X25519 a hybridní protokoly na stejných tunnelech, závisí na implementaci.

### Forward Secrecy

Specifikace ECIES umožňuje Garlic Messages v payloadu New Session Message, což umožňuje 0-RTT doručení počátečního streamovacího paketu, obvykle HTTP GET, společně s leaseset klienta. Nicméně payload New Session Message nemá forward secrecy. Jelikož tento návrh zdůrazňuje vylepšené forward secrecy pro ratchet, implementace mohou nebo by měly odložit zahrnutí streamovacího payloadu, nebo celé streamovací zprávy, až do první Existing Session Message. To by bylo na úkor 0-RTT doručení. Strategie mohou také záviset na typu provozu nebo typu tunelu, nebo například na GET vs. POST. Závisí na implementaci.

### Velikost nové relace

MLKEM dramaticky zvětší velikost New Session Message, jak je popsáno výše. To může výrazně snížit spolehlivost doručování New Session Message skrze tunnely, kde musí být fragmentovány do několika 1024bajtových tunnel zpráv. Úspěšnost doručení je úměrná exponenciálnímu počtu fragmentů. Implementace mohou použít různé strategie pro omezení velikosti zprávy na úkor 0-RTT doručení. Závisí na implementaci.

## Reference

- [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/)
- [COMMON](/docs/specs/common-structures/)
- [ECIES](/docs/specs/ecies/)
- [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
- [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
- [FORUM](http://zzz.i2p/topics/3294)
- [NIST-PQ-END](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf)
- [NIST-VECTORS](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values)
- [Noise](https://noiseprotocol.org/noise.html)
- [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf)
- [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)
- [PQ-WIREGUARD](https://eprint.iacr.org/2020/379.pdf)
- [Prop169](/proposals/169-pq-crypto/)
