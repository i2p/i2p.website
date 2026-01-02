---
title: "ECIES-X25519-AEAD-Ratchet hybridní šifrování"
description: "Postkvantová hybridní varianta šifrovacího protokolu ECIES využívající ML‑KEM (mechanismus zapouzdření klíče založený na modulech mříží)"
slug: "ecies-hybrid"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Stav implementace

**Aktuální nasazení:** - **i2pd (implementace v C++)**: Plně implementováno ve verzi 2.58.0 (září 2025) s podporou ML-KEM-512, ML-KEM-768 a ML-KEM-1024. Postkvantové end-to-end šifrování je ve výchozím nastavení povoleno, pokud je k dispozici OpenSSL 3.5.0 nebo novější. - **Java I2P**: Zatím neimplementováno k verzi 0.9.67 / 2.10.0 (září 2025). Specifikace schválena a implementace plánována do budoucích vydání.

Tato specifikace popisuje schválenou funkcionalitu, která je v současnosti nasazena v i2pd a je plánována pro implementace Java I2P.

## Přehled

Jedná se o postkvantovou hybridní variantu protokolu ECIES-X25519-AEAD-Ratchet [ECIES](/docs/specs/ecies/). Představuje první fázi Návrhu 169 [Prop169](/proposals/169-pq-crypto/), která má být schválena. Podrobnosti o celkových cílech, modelech hrozeb, analýze, alternativách a dalších informacích viz tento návrh.

Stav návrhu 169: **Otevřeno** (první fáze byla schválena pro hybridní implementaci ECIES (šifrovací schéma na eliptických křivkách)).

Tato specifikace obsahuje pouze rozdíly oproti standardu [ECIES](/docs/specs/ecies/) a je třeba ji číst ve spojení s danou specifikací.

## Návrh

Používáme standard NIST FIPS 203 [FIPS203](https://csrc.nist.gov/pubs/fips/203/final), který je založen na CRYSTALS-Kyberu (verze 3.1, 3 a starší), ale není s ním kompatibilní.

Hybridní handshaky kombinují klasickou výměnu klíčů X25519 Diffie-Hellman s postkvantovými mechanismy zapouzdření klíče ML-KEM (NIST standard pro postkvantové zapouzdření klíče). Tento přístup vychází z konceptů hybridního dopředného utajení popsaných ve výzkumu PQNoise (výzkum postkvantové varianty protokolu Noise) a z podobných implementací v TLS 1.3, IKEv2 a WireGuard.

### Výměna klíčů

Definujeme hybridní výměnu klíčů pro Ratchet (mechanismus postupné obnovy klíčů). Postkvantové KEM poskytuje pouze efemérní klíče a přímo nepodporuje navázání spojení se statickými klíči, jako je Noise IK.

Definujeme tři varianty ML-KEM podle specifikace v [FIPS203](https://csrc.nist.gov/pubs/fips/203/final), celkem tedy tři nové typy šifrování. Hybridní typy jsou definovány pouze v kombinaci s X25519.

Nové typy šifrování jsou:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Security Level</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">ML-KEM Variant</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NIST Category 1 (AES-128 equivalent)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ML-KEM-512</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NIST Category 3 (AES-192 equivalent)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ML-KEM-768 (Recommended)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NIST Category 5 (AES-256 equivalent)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ML-KEM-1024</td>
    </tr>
  </tbody>
</table>
**Poznámka:** MLKEM768_X25519 (Type 6) je doporučená výchozí varianta, která zajišťuje silné postkvantové zabezpečení při rozumné režii.

Režie je značná ve srovnání se šifrováním pouze pomocí X25519. Typické velikosti zpráv 1 a 2 (pro IK pattern (schéma IK)) jsou aktuálně okolo 96–103 bajtů (před přidáním dodatečných užitečných dat). To se zvýší přibližně 9–12× u MLKEM512, 13–16× u MLKEM768 a 17–23× u MLKEM1024, v závislosti na typu zprávy.

### Vyžadováno nové šifrování

- **ML-KEM** (dříve CRYSTALS-Kyber) [FIPS203](https://csrc.nist.gov/pubs/fips/203/final) - Standard mechanismu zapouzdření klíčů založený na modulových mřížích
- **SHA3-256** (dříve Keccak-512) [FIPS202](https://csrc.nist.gov/pubs/fips/202/final) - Součást standardu SHA-3
- **SHAKE128 a SHAKE256** (XOF (funkce s rozšiřitelným výstupem) rozšíření pro SHA3) [FIPS202](https://csrc.nist.gov/pubs/fips/202/final) - Funkce s rozšiřitelným výstupem

Testovací vektory pro SHA3-256, SHAKE128 a SHAKE256 jsou k dispozici v rámci [NIST Cryptographic Algorithm Validation Program](https://csrc.nist.gov/Projects/cryptographic-algorithm-validation-program).

**Podpora knihoven:** - Java: knihovna Bouncycastle ve verzi 1.79 a novější podporuje všechny varianty ML-KEM (mechanismus zapouzdření klíče na bázi mřížek) a funkce SHA3/SHAKE - C++: OpenSSL 3.5 a novější zahrnuje plnou podporu ML-KEM (vydáno v dubnu 2025) - Go: Pro implementaci ML-KEM a SHA3 je k dispozici více knihoven

## Specifikace

### Společné struktury

Viz [Common Structures Specification](/docs/specs/common-structures/) pro informace o délkách klíčů a identifikátorech.

### Vzory navázání spojení

Navazování spojení používá vzory handshake z [Noise Protocol Framework](https://noiseprotocol.org/noise.html) s úpravami specifickými pro I2P pro hybridní postkvantové zabezpečení.

Používá se následující mapování písmen:

- **e** = jednorázový efemérní klíč (X25519)
- **s** = statický klíč
- **p** = datová část zprávy
- **e1** = jednorázový efemérní PQ (postkvantový) klíč, odeslaný od Alice Bobovi (token specifický pro I2P)
- **ekem1** = šifrotext KEM, odeslaný od Boba Alici (token specifický pro I2P)

**Důležité upozornění:** Názvy vzorců "IKhfs" a "IKhfselg2" a tokeny "e1" a "ekem1" jsou úpravy specifické pro I2P, které nejsou zdokumentovány v oficiální specifikaci Noise Protocol Framework. Představují vlastní definice pro integraci ML-KEM (postkvantový mechanismus zapouzdření klíče) do vzorce Noise IK. Ačkoli je hybridní přístup X25519 + ML-KEM široce uznáván ve výzkumu postkvantové kryptografie a v dalších protokolech, konkrétní názvosloví použité zde je specifické pro I2P.

Následující úpravy IK pro hybridní dopředné utajení se uplatňují:

```
Standard IK:              I2P IKhfs (Hybrid):
<- s                      <- s
...                       ...
-> e, es, s, ss, p        -> e, es, e1, s, ss, p
<- e, ee, se, p           <- e, ee, ekem1, se, p
<- p                      <- p
p ->                      p ->

Note: e1 and ekem1 are encrypted within ChaCha20-Poly1305 AEAD blocks.
Note: e1 (ML-KEM public key) and ekem1 (ML-KEM ciphertext) have different sizes.
```
Vzor **e1** je definován následovně:

```
For Alice (sender):
(encap_key, decap_key) = PQ_KEYGEN()

// EncryptAndHash(encap_key)
ciphertext = ENCRYPT(k, n, encap_key, ad)
n++
MixHash(ciphertext)

For Bob (receiver):
// DecryptAndHash(ciphertext)
encap_key = DECRYPT(k, n, ciphertext, ad)
n++
MixHash(ciphertext)
```
Vzor **ekem1** je definován následovně:

```
For Bob (receiver of encap_key):
(kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

// EncryptAndHash(kem_ciphertext)
ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)
MixHash(ciphertext)

// MixKey
MixKey(kem_shared_key)

For Alice (sender of encap_key):
// DecryptAndHash(ciphertext)
kem_ciphertext = DECRYPT(k, n, ciphertext, ad)
MixHash(ciphertext)

// MixKey
kem_shared_key = DECAPS(kem_ciphertext, decap_key)
MixKey(kem_shared_key)
```
### Definované operace ML-KEM

Definujeme následující funkce odpovídající kryptografickým stavebním prvkům v souladu s [FIPS203](https://csrc.nist.gov/pubs/fips/203/final).

**(encap_key, decap_key) = PQ_KEYGEN()** : Alice vytvoří klíče pro enkapsulaci a dekapsulaci. Klíč pro enkapsulaci je odeslán ve zprávě NS. Velikosti klíčů:   - ML-KEM-512: encap_key = 800 bajtů, decap_key = 1632 bajtů   - ML-KEM-768: encap_key = 1184 bajtů, decap_key = 2400 bajtů   - ML-KEM-1024: encap_key = 1568 bajtů, decap_key = 3168 bajtů

**(ciphertext, kem_shared_key) = ENCAPS(encap_key)** : Bob vypočítá šifrotext a sdílený klíč pomocí zapouzdřovacího klíče přijatého ve zprávě NS. Šifrotext je odeslán ve zprávě NSR. Velikosti šifrotextu:   - ML-KEM-512: 768 bajtů   - ML-KEM-768: 1088 bajtů   - ML-KEM-1024: 1568 bajtů

kem_shared_key má vždy délku **32 bajtů** u všech tří variant.

**kem_shared_key = DECAPS(ciphertext, decap_key)** : Alice vypočítá sdílený klíč pomocí šifrotextu obdrženého ve zprávě NSR. kem_shared_key má vždy délku **32 bajtů**.

**Důležité:** Jak encap_key, tak ciphertext jsou zašifrovány uvnitř bloků ChaCha20-Poly1305 v handshake zprávách 1 a 2 protokolu Noise (kryptografický protokol pro handshake). Budou dešifrovány v rámci procesu handshaku.

kem_shared_key je smíchán do řetězicího klíče pomocí MixKey(). Podrobnosti viz níže.

### KDF (funkce pro odvozování klíčů) pro handshake protokolu Noise

#### Přehled

Hybridní handshake (navázání spojení) kombinuje klasické X25519 ECDH s postkvantovým ML-KEM. První zpráva, od Alice Bobovi, obsahuje e1 (zapouzdřovací klíč ML-KEM) před datovou částí zprávy. S tímto se zachází jako s dodatečným klíčovým materiálem; zavolejte na něj EncryptAndHash() (jako Alice) nebo DecryptAndHash() (jako Bob). Poté zpracujte datovou část zprávy jako obvykle.

Druhá zpráva, od Boba k Alici, obsahuje ekem1 (ML-KEM šifrotext) před datovou částí zprávy. S tímto se zachází jako s dodatečným klíčovým materiálem; použijte na něj EncryptAndHash() (jako Bob) nebo DecryptAndHash() (jako Alice). Poté vypočítejte kem_shared_key a zavolejte MixKey(kem_shared_key). Následně zpracujte datovou část zprávy jako obvykle.

#### Identifikátory protokolu Noise

Toto jsou inicializační řetězce pro Noise (kryptografický protokol) (specifické pro I2P):

- `Noise_IKhfselg2_25519+MLKEM512_ChaChaPoly_SHA256`
- `Noise_IKhfselg2_25519+MLKEM768_ChaChaPoly_SHA256`
- `Noise_IKhfselg2_25519+MLKEM1024_ChaChaPoly_SHA256`

#### Alice KDF (funkce odvození klíče) pro zprávu NS

Za vzorem zprávy 'es' a před vzorem zprávy 's' přidejte:

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
#### Bobův KDF (funkce pro odvozování klíčů) pro zprávu NS

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

NOTE: For the next section (payload for XK or static key for IK),
the keydata and chain key remain the same,
and n now equals 1 (instead of 0 for non-hybrid).
```
#### Bobův KDF (funkce pro odvozování klíčů) pro zprávu NSR

Za vzorem zprávy 'ee' a před vzorem zprávy 'se' přidejte:

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
#### Alice KDF (funkce pro odvozování klíčů) pro zprávu NSR

Po schématu zprávy 'ee' a před schématem zprávy 'ss' přidejte:

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
#### KDF (funkce derivace klíče) pro split()

Funkce split() zůstává nezměněna oproti standardní specifikaci ECIES. Po dokončení handshake (úvodního navázání spojení):

```
keydata = HKDF(chainKey, ZEROLEN, "", 64)
k_ab = keydata[0:31]
k_ba = keydata[32:63]
```
Toto jsou obousměrné klíče používané pro probíhající komunikaci v rámci relace.

### Formát zprávy

#### Formát NS (New Session)

**Změny:** Aktuální ratchet (kryptografický mechanismus pro postupné odvozování klíčů) obsahuje statický klíč v první sekci ChaCha20-Poly1305 a užitečná data ve druhé sekci. S ML-KEM jsou nyní tři sekce. První sekce obsahuje šifrovaný veřejný klíč ML-KEM (encap_key). Druhá sekce obsahuje statický klíč. Třetí sekce obsahuje užitečná data.

**Velikosti zpráv:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">X25519 len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NS len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NS Enc len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NS Dec len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">PQ key len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">pl len</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">96+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">--</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">912+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">880+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">800+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">800</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1296+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1264+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1184+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1184</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1680+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1648+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1568+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1568</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
  </tbody>
</table>
**Poznámka:** Užitečná data musí obsahovat blok DateTime (minimálně 7 bajtů: 1 bajt na typ, 2 bajty na velikost, 4 bajty na časové razítko). Minimální velikosti NS lze podle toho vypočítat. Minimální praktická velikost NS je tedy 103 bajtů pro X25519 a u hybridních variant se pohybuje od 919 do 1687 bajtů.

Nárůsty velikosti o 816, 1200 a 1584 bajtů u všech tří variant ML-KEM jsou způsobeny veřejným klíčem ML-KEM a 16bajtovým Poly1305 MAC pro autentizované šifrování.

#### Formát NSR (New Session Reply – odpověď na novou relaci)

**Změny:** Současný ratchet (kryptografický ráčnový mechanismus) má prázdná užitečná data pro první sekci ChaCha20-Poly1305 a užitečná data ve druhé sekci. S ML-KEM jsou nyní tři sekce. První sekce obsahuje zašifrovaný ML-KEM šifrotext. Druhá sekce má prázdná užitečná data. Třetí sekce obsahuje užitečná data.

**Velikosti zpráv:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">X25519 len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NSR len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NSR Enc len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NSR Dec len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">PQ ct len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">pl len</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">72+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">40+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">--</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">856+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">824+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">784+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">768</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1176+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1144+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1104+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1088</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1656+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1624+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1584+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1568</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
  </tbody>
</table>
Navýšení velikosti o 784, 1104 a 1584 bajtů u tří variant ML-KEM odpovídají součtu šifrotextu ML-KEM a 16bajtového Poly1305 MAC (ověřovací kód zprávy) pro autentizované šifrování.

## Analýza režie

### Výměna klíčů

Režie u hybridního šifrování je značná ve srovnání se samotným X25519:

- **MLKEM512_X25519**: Přibližně 9-12x nárůst velikosti zprávy pro handshake (navázání spojení) (NS: 9.5x, NSR: 11.9x)
- **MLKEM768_X25519**: Přibližně 13-16x nárůst velikosti zprávy pro handshake (NS: 13.5x, NSR: 16.3x)
- **MLKEM1024_X25519**: Přibližně 17-23x nárůst velikosti zprávy pro handshake (NS: 17.5x, NSR: 23x)

Tato režie je přijatelná vzhledem k dodatečným přínosům postkvantového zabezpečení. Násobicí faktory se liší podle typu zprávy, protože základní velikosti zpráv se liší (NS minimálně 96 bajtů, NSR minimálně 72 bajtů).

### Úvahy o šířce pásma

Pro typické zřízení relace s minimálními užitečnými daty: - X25519 pouze: ~200 bajtů celkem (NS + NSR) - MLKEM512_X25519: ~1,800 bajtů celkem (zvýšení 9×) - MLKEM768_X25519: ~2,500 bajtů celkem (zvýšení 12,5×) - MLKEM1024_X25519: ~3,400 bajtů celkem (zvýšení 17×)

Po navázání relace používá průběžné šifrování zpráv stejný formát přenosu dat jako relace pouze s X25519, takže pro následné zprávy nevzniká žádná dodatečná režie.

## Bezpečnostní analýza

### Navazování spojení

Hybridní handshake poskytuje jak klasickou (X25519), tak postkvantovou (ML-KEM) bezpečnost. Útočník musí prolomit **obojí**, tedy jak klasické ECDH, tak postkvantové KEM (mechanismus zapouzdření klíče), aby kompromitoval klíče relace.

To poskytuje: - **Současná bezpečnost**: X25519 ECDH poskytuje bezpečnost proti klasickým útočníkům (úroveň bezpečnosti 128 bitů) - **Budoucí bezpečnost**: ML-KEM (postkvantový mechanismus zapouzdření klíče) poskytuje bezpečnost proti kvantovým útočníkům (liší se podle sady parametrů) - **Hybridní bezpečnost**: Obě musí být prolomeny, aby došlo ke kompromitaci relace (úroveň bezpečnosti = maximum z obou komponent)

### Úrovně zabezpečení

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Variant</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NIST Category</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Classical Security</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">PQ Security</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Hybrid Security</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Category 1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit (X25519)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-128 equivalent</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Category 3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit (X25519)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-192 equivalent</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Category 5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit (X25519)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 equivalent</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit</td>
    </tr>
  </tbody>
</table>
**Poznámka:** Hybridní úroveň bezpečnosti je dána slabší ze dvou komponent. Ve všech případech poskytuje X25519 (eliptická křivka pro výměnu klíčů) 128bitovou klasickou úroveň bezpečnosti. Pokud bude k dispozici kryptograficky relevantní kvantový počítač, úroveň bezpečnosti by závisela na zvolené sadě parametrů ML-KEM (postkvantový mechanismus zapouzdření klíče).

### Dopředné utajení

Hybridní přístup zachovává vlastnosti dopředné bezpečnosti. Relační klíče jsou odvozeny jak z efemérní výměny klíčů X25519, tak z efemérní výměny klíčů ML-KEM (postkvantní mechanismus zapouzdření klíče). Pokud jsou po navázání spojení zničeny efemérní soukromé klíče X25519 nebo ML-KEM, minulé relace nelze dešifrovat, i kdyby byly kompromitovány dlouhodobé statické klíče.

Vzor IK (vzor handshake „IK“ v Noise) poskytuje dokonalé dopředné utajení (úroveň důvěrnosti Noise 5) po odeslání druhé zprávy (NSR).

## Předvolby typu

Implementace by měly podporovat více hybridních typů a vyjednat nejsilnější vzájemně podporovanou variantu. Pořadí preferencí by mělo být:

1. **MLKEM768_X25519** (Type 6) - Doporučená výchozí volba, nejlepší rovnováha mezi zabezpečením a výkonem
2. **MLKEM1024_X25519** (Type 7) - Nejvyšší úroveň zabezpečení pro citlivé aplikace
3. **MLKEM512_X25519** (Type 5) - Základní postkvantové zabezpečení pro scénáře s omezenými prostředky
4. **X25519** (Type 4) - Pouze klasická kryptografie, záložní varianta pro kompatibilitu

**Odůvodnění:** MLKEM768_X25519 se doporučuje jako výchozí, protože poskytuje zabezpečení NIST Category 3 (ekvivalent AES-192), které je považováno za dostatečnou ochranu proti kvantovým počítačům při zachování přiměřené velikosti zpráv. MLKEM1024_X25519 poskytuje vyšší úroveň zabezpečení, ale za cenu podstatně vyšší režie.

## Poznámky k implementaci

### Podpora knihoven

- **Java**: Knihovna Bouncycastle od verze 1.79 (srpen 2024) podporuje všechny požadované varianty ML-KEM a funkce SHA3/SHAKE. Pro zajištění shody s FIPS 203 použijte `org.bouncycastle.pqc.crypto.mlkem.MLKEMEngine`.
- **C++**: OpenSSL 3.5 (duben 2025) a novější zahrnuje podporu ML-KEM prostřednictvím rozhraní EVP_KEM. Jedná se o vydání s dlouhodobou podporou, udržované do dubna 2030.
- **Go**: K dispozici je několik knihoven třetích stran pro ML-KEM a SHA3, včetně knihovny CIRCL od Cloudflare.

### Migrační strategie

Implementace by měly: 1. Podporovat během přechodného období jak variantu pouze X25519, tak hybridní varianty ML-KEM 2. Preferovat hybridní varianty, pokud je podporují obě strany 3. Zachovat fallback (záložní varianta) na variantu pouze X25519 kvůli zpětné kompatibilitě 4. Zohlednit omezení šířky pásma sítě při volbě výchozí varianty

### Sdílené Tunnels

Zvýšené velikosti zpráv mohou ovlivnit využití sdíleného tunnelu. Implementace by měly zvážit: - Sdružovat handshake (úvodní navázání spojení), kde je to možné, aby se rozložila režie - Používat kratší doby platnosti u hybridních relací ke snížení udržovaného stavu - Sledovat využití šířky pásma a podle toho upravovat parametry - Zavést řízení přetížení pro provoz při navazování relace

### Úvahy o velikosti nové relace

Vzhledem k větším zprávám handshake (navázání spojení) mohou implementace potřebovat: - Zvýšit velikosti vyrovnávacích pamětí pro vyjednávání relace (doporučené minimum 4KB) - Upravit hodnoty časových limitů pro pomalejší připojení (počítat s ~3-17x většími zprávami) - Zvážit kompresi užitečných dat v NS/NSR zprávách - Implementovat zpracování fragmentace, pokud to vyžaduje transportní vrstva

### Testování a ověřování

Implementace by měly ověřit: - Správné generování klíčů ML-KEM, zapouzdření a decapsulaci - Správnou integraci kem_shared_key do Noise KDF - Shodu výpočtů velikosti zpráv se specifikací - Interoperabilitu s jinými implementacemi I2P routeru - Záložní chování při nedostupnosti ML-KEM

Testovací vektory pro operace ML-KEM jsou k dispozici v programu NIST [Cryptographic Algorithm Validation Program](https://csrc.nist.gov/Projects/cryptographic-algorithm-validation-program) (program ověřování kryptografických algoritmů).

## Kompatibilita verzí

**Číslování verzí I2P:** I2P udržuje dvě paralelní číselné řady verzí: - **Verze vydání routeru**: formát 2.x.x (např. 2.10.0 vydáno v září 2025) - **Verze API/protokolu**: formát 0.9.x (např. 0.9.67 odpovídá routeru 2.10.0)

Tato specifikace odkazuje na verzi protokolu 0.9.67, která odpovídá vydání routeru 2.10.0 a novějším.

**Matice kompatibility:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Implementation</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">ML-KEM Support</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2pd</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.58.0+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Full (512/768/1024)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deployed September 2025</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Java I2P</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67 / 2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Not yet</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Planned for future release</td>
    </tr>
  </tbody>
</table>
## Reference

- **[ECIES]**: [Specifikace ECIES-X25519-AEAD-Ratchet](/docs/specs/ecies/)
- **[Prop169]**: [Návrh 169: postkvantová kryptografie](/proposals/169-pq-crypto/)
- **[FIPS203]**: [NIST FIPS 203 - standard ML-KEM](https://csrc.nist.gov/pubs/fips/203/final)
- **[FIPS202]**: [NIST FIPS 202 - standard SHA-3](https://csrc.nist.gov/pubs/fips/202/final)
- **[Noise]**: [Rámec protokolu Noise](https://noiseprotocol.org/noise.html)
- **[COMMON]**: [Specifikace společných struktur](/docs/specs/common-structures/)
- **[RFC7539]**: [RFC 7539 - ChaCha20 a Poly1305](https://www.rfc-editor.org/rfc/rfc7539)
- **[RFC5869]**: [RFC 5869 - HKDF](https://www.rfc-editor.org/rfc/rfc5869)
- **[OpenSSL]**: [Dokumentace OpenSSL 3.5 ML-KEM](https://docs.openssl.org/3.5/man7/EVP_KEM-ML-KEM/)
- **[Bouncycastle]**: [Java kryptografická knihovna Bouncycastle](https://www.bouncycastle.org/)

---
