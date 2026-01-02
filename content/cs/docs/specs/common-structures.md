---
title: "Společné struktury"
description: "Sdílené datové typy a serializační formáty používané napříč specifikacemi I2P"
slug: "common-structures"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Přehled

Tento dokument specifikuje základní datové struktury používané napříč všemi protokoly I2P, včetně [I2NP](/docs/specs/i2np/), [I2CP](/docs/specs/i2cp/), [SSU2](/docs/specs/ssu2/), [NTCP2](/docs/specs/ntcp2/) a dalších. Tyto společné struktury zajišťují interoperabilitu mezi různými implementacemi I2P a vrstvami protokolu.

### Hlavní změny od verze 0.9.58

- ElGamal a DSA-SHA1 jsou pro Router Identities zastaralé (použijte X25519 + EdDSA)
- Podpora postkvantového ML-KEM je v beta testování (opt-in (volitelné zapnutí) od verze 2.10.0)
- Možnosti záznamu služby byly standardizovány ([Proposal 167](/proposals/167-service-records/), implementováno ve verzi 0.9.66)
- Specifikace komprimovatelné výplně byly finalizovány ([Proposal 161](/cs/proposals/161-ri-dest-padding/), implementováno ve verzi 0.9.57)

---

## Obecné specifikace typů

### Celé číslo

**Popis:** Představuje nezáporné celé číslo v síťovém pořadí bajtů (big-endian).

**Obsah:** 1 až 8 bajtů představujících neznaménkové celé číslo.

**Použití:** Délky polí, počty, identifikátory typů a číselné hodnoty napříč protokoly I2P.

---

### Datum

**Popis:** Časové razítko udávající počet milisekund od unixové epochy (1. ledna 1970 00:00:00 GMT).

**Obsah:** 8bajtové celé číslo (neznaménkový long)

**Speciální hodnoty:** - `0` = nedefinované nebo nulové datum - Maximální hodnota: `0xFFFFFFFFFFFFFFFF` (rok 584,942,417,355)

**Poznámky k implementaci:** - Vždy časové pásmo UTC/GMT - Je vyžadována milisekundová přesnost - Používá se pro vypršení platnosti lease (I2P: záznam s dobou platnosti), publikaci RouterInfo (metadata o routeru) a ověření časových razítek

---

### Řetězec

**Popis:** Řetězec kódovaný v UTF‑8 s délkovým prefixem.

**Formát:**

```
+----+----+----+----+----+----+
|len | UTF-8 encoded data...   |
+----+----+----+----+----+----+

len :: Integer (1 byte)
       Value: 0-255 (string length in bytes, NOT characters)

data :: UTF-8 encoded bytes
        Length: 0-255 bytes
```
**Omezení:** - Maximální délka: 255 bajtů (nikoli znaky - vícebajtové sekvence UTF-8 se počítají jako více bajtů) - Délka může být nula (prázdný řetězec) - Nulový terminátor NENÍ zahrnut - Řetězec NENÍ ukončen nulou

**Důležité:** Sekvence UTF-8 mohou používat více bajtů na jeden znak. Řetězec se 100 znaky může překročit limit 255 bajtů, pokud používá vícebajtové znaky.

---

## Struktury kryptografických klíčů

### Veřejný klíč

**Popis:** Veřejný klíč pro asymetrické šifrování. Typ a délka klíče jsou závislé na kontextu nebo jsou uvedeny v Key Certificate (certifikátu klíče).

**Výchozí typ:** ElGamal (zastaralé pro Router Identities (identit routeru) od verze 0.9.58)

**Podporované typy:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destinations only (unused field)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated for RIs</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">132</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Recommended</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">800</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1184</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1568</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512_CT</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">768</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768_CT</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1088</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024_CT</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1568</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
  </tbody>
</table>
**Požadavky na implementaci:**

1. **X25519 (Type 4) - aktuální standard:**
   - Používá se pro šifrování ECIES-X25519-AEAD-Ratchet
   - Povinné pro identity routeru od verze 0.9.48
   - Kódování little-endian (na rozdíl od ostatních typů)
   - Viz [ECIES](/docs/specs/ecies/) a [ECIES-ROUTERS](/docs/specs/ecies/#routers)

2. **ElGamal (Type 0) - zastaralé:**
   - Označeno jako zastaralé pro Router Identities od verze 0.9.58
   - Stále platné pro destinace (pole se nepoužívá od 0.6/2005)
   - Používá konstantní prvočísla definovaná ve [specifikaci ElGamal](/docs/specs/cryptography/)
   - Podpora je udržována kvůli zpětné kompatibilitě

3. **MLKEM (postkvantové) - Beta:**
   - Hybridní přístup kombinuje ML-KEM s X25519
   - NENÍ ve výchozím nastavení povoleno ve verzi 2.10.0
   - Vyžaduje ruční aktivaci prostřednictvím Hidden Service Manager (správce skrytých služeb)
   - Viz [ECIES-HYBRID](/docs/specs/ecies/#hybrid) a [Návrh 169](/proposals/169-pq-crypto/)
   - Kódy typů a specifikace podléhají změnám

**JavaDoc:** [PublicKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/PublicKey.html)

---

### Soukromý klíč

**Popis:** Soukromý klíč pro asymetrické dešifrování, odpovídající typům PublicKey.

**Úložiště:** Typ a délka jsou odvozeny z kontextu nebo uloženy odděleně v datových strukturách/souborech s klíči.

**Podporované typy:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destinations only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated for RIs</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">48</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">66</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Recommended</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1632</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2400</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3168</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
  </tbody>
</table>
**Bezpečnostní poznámky:** - Soukromé klíče MUSÍ být generovány pomocí kryptograficky bezpečných generátorů náhodných čísel - Soukromé klíče X25519 používají scalar clamping (úprava bitů skaláru) podle definice v RFC 7748 - Klíčový materiál MUSÍ být bezpečně vymazán z paměti, když již není potřeba

**JavaDoc:** [PrivateKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/PrivateKey.html)

---

### SessionKey (klíč relace)

**Popis:** Symetrický klíč pro šifrování a dešifrování AES-256 v I2P v rámci tunnel a garlic encryption.

**Obsah:** 32 bajtů (256 bitů)

**Použití:** - Šifrování vrstvy tunnel (AES-256/CBC s IV) - Garlic message encryption (šifrování zpráv metodou garlic) - End-to-end šifrování relace

**Generování:** MUSÍ použít kryptograficky bezpečný generátor náhodných čísel.

**JavaDoc:** [SessionKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SessionKey.html)

---

### SigningPublicKey

**Popis:** Veřejný klíč pro ověření podpisu. Typ a délka jsou specifikovány v Key Certificate of Destination (certifikátu klíče objektu Destination) nebo odvozeny z kontextu.

**Výchozí typ:** DSA_SHA1 (zastaralé od verze 0.9.58)

**Podporované typy:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA_SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">128</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA256_P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Older Destinations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA384_P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA512_P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">132</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA256_2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA384_3072</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA512_4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Recommended for SU3</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Recommended</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519ph</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.25</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RedDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted leasesets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specialized</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved (GOST)</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">9</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Proposal 134</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved (GOST)</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">128</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Proposal 134</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved (MLDSA)</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12-20</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Proposal 169</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">65280-65534</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Testing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Never production</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">65535</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Future expansion</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td></tr>
  </tbody>
</table>
**Požadavky na implementaci:**

1. **EdDSA_SHA512_Ed25519 (Typ 7) - Aktuální standard:**
   - Výchozí pro všechny nové identity routeru a destinace od konce roku 2015
   - Používá křivku Ed25519 s hashovací funkcí SHA-512
   - 32bajtové veřejné klíče, 64bajtové podpisy
   - Kódování little-endian (na rozdíl od většiny ostatních typů)
   - Vysoký výkon a bezpečnost

2. **RedDSA_SHA512_Ed25519 (Type 11) - Specializované:**
   - Používáno POUZE pro šifrované leasesets a zaslepení (blinding)
   - Nikdy se nepoužívá pro identity routeru ani pro standardní destinace
   - Hlavní rozdíly oproti EdDSA:
     - Odvozování soukromých klíčů prováděno modulární redukcí (nikoli clamping [bitové upnutí])
     - Podpisy zahrnují 80 bajtů náhodných dat
     - Používá veřejné klíče přímo (nikoli hashů soukromých klíčů)
   - Viz [Specifikace Red25519](//docs/specs/red25519-signature-scheme/

3. **DSA_SHA1 (Typ 0) - Historické:**
   - Zastaralé pro identity routeru od verze 0.9.58
   - Nedoporučeno pro nové Destinace
   - 1024bitové DSA se SHA-1 (známé slabiny)
   - Podpora je zachována pouze kvůli kompatibilitě

4. **Víceprvkové klíče:**
   - Pokud se skládají ze dvou prvků (např. souřadnice bodu ECDSA X,Y)
   - Každý prvek je doplněn na délku/2 počátečními nulami
   - Příklad: 64bajtový klíč ECDSA = 32 bajtů X + 32 bajtů Y

**JavaDoc:** [SigningPublicKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SigningPublicKey.html)

---

### SigningPrivateKey

**Popis:** Soukromý klíč pro vytváření podpisů, odpovídající typům SigningPublicKey.

**Úložiště:** Typ a délka jsou určeny při vytvoření.

**Podporované typy:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA_SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA256_P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Older Destinations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA384_P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">48</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA512_P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">66</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA256_2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA384_3072</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">768</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA512_4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1024</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Recommended for SU3</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Recommended</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519ph</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.25</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RedDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted leasesets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specialized</td></tr>
  </tbody>
</table>
**Požadavky na zabezpečení:** - Generovat s použitím kryptograficky bezpečného zdroje náhodnosti - Chránit pomocí vhodného řízení přístupu - Po dokončení bezpečně vymazat z paměti - Pro EdDSA: 32bajtový seed zahashovaný pomocí SHA-512, prvních 32 bajtů tvoří skalár (clamped – bitově upraveno dle specifikace) - Pro RedDSA: Odlišný způsob generování klíče (modulární redukce místo clamping)

**JavaDoc:** [SigningPrivateKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SigningPrivateKey.html)

---

### Podpis

**Popis:** Kryptografický podpis nad daty, s využitím podpisového algoritmu, který odpovídá typu SigningPrivateKey.

**Typ a délka:** Určeno podle typu klíče použitého pro podepisování.

**Podporované typy:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA_SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">40</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA256_P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Older Destinations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA384_P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA512_P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">132</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA256_2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA384_3072</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA512_4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current for SU3</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Recommended</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519ph</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.25</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RedDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted leasesets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specialized</td></tr>
  </tbody>
</table>
**Poznámky k formátu:** - Víceprvkové podpisy (např. hodnoty R,S u ECDSA) se pro každý prvek doplňují úvodními nulami na délku length/2 - EdDSA a RedDSA používají kódování little-endian (pořadí bajtů s nejméně významným bajtem první) - Všechny ostatní typy používají kódování big-endian (pořadí bajtů s nejvíce významným bajtem první)

**Ověření:** - Použijte odpovídající SigningPublicKey - Postupujte podle specifikací algoritmu podpisu pro daný typ klíče - Zkontrolujte, že délka podpisu odpovídá očekávané délce pro daný typ klíče

**JavaDoc:** [Signature](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Signature.html)

---

### Otisk

**Description:** SHA-256 hash dat, používaný v celém I2P k ověřování integrity a identifikaci.

**Obsah:** 32 bajtů (256 bitů)


**Algoritmus:** SHA-256 podle FIPS 180-4

**JavaDoc:** [Hash](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Hash.html)

---

### Session Tag (značka relace)

**Popis:** Náhodné číslo používané pro identifikaci relace a šifrování založené na značkách.

**Důležité:** Velikost Session Tagu (značka relace) se liší podle typu šifrování: - **ElGamal/AES+SessionTag:** 32 bajtů (starší) - **ECIES-X25519:** 8 bajtů (současný standard)

**Aktuální standard (ECIES – integrované šifrovací schéma eliptických křivek):**

```
Contents: 8 bytes
Usage: Ratchet-based encryption for Destinations and Routers
```
Viz [ECIES](/docs/specs/ecies/) a [ECIES-ROUTERS](/docs/specs/ecies/#routers) pro podrobné specifikace.

**Zastaralé (ElGamal/AES):**

```
Contents: 32 bytes
Usage: Deprecated encryption scheme
```
**Generování:** MUSÍ používat kryptograficky bezpečný generátor náhodných čísel.

**JavaDoc:** [SessionTag](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SessionTag.html)

---

### TunnelId

**Popis:** Jedinečný identifikátor pozice routeru v tunnelu. Každý hop v tunnelu má svůj vlastní TunnelId (identifikátor hopu v tunnelu).

**Formát:**

```
Contents: 4-byte Integer (unsigned 32-bit)
Range: Generally > 0 (zero reserved for special cases)
```
**Použití:** - Identifikuje příchozí/odchozí spojení v rámci tunnel pro každý router - Odlišné TunnelId na každém skoku v řetězci tunnel - Používá se ve strukturách Lease (I2P záznam o přístupu do tunnel) k identifikaci vstupních tunnel

**Speciální hodnoty:** - `0` = Vyhrazeno pro speciální účely protokolu (nepoužívat při běžném provozu) - TunnelIds mají lokální platnost pro každý router

**JavaDoc:** [TunnelId](http://docs.i2p-projekt.de/javadoc/net/i2p/data/TunnelId.html)

---

## Specifikace certifikátů

### Certifikát

**Popis:** Kontejner pro potvrzení, proof-of-work (důkaz práce) nebo kryptografická metadata používaný v celém I2P.

**Formát:**

```
+----+----+----+----+----+----+-//
|type| length  | payload
+----+----+----+----+----+----+-//

type :: Integer (1 byte)
        Values: 0-5 (see types below)

length :: Integer (2 bytes, big-endian)
          Size of payload in bytes

payload :: data
           length -> $length bytes
```
**Celková velikost:** minimálně 3 bajty (NULL certificate – certifikát typu NULL), maximálně 65538 bajtů

### Typy certifikátů

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Payload Length</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Total Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">NULL</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Default/empty certificate</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">HASHCASH</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused (was for proof-of-work)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">HIDDEN</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused (hidden routers don't advertise)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SIGNED</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 or 72</td><td style="border:1px solid var(--color-border); padding:0.5rem;">43 or 75</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused (DSA signature ± destination hash)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MULTIPLE</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused (multiple certificates)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">KEY</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4+</td><td style="border:1px solid var(--color-border); padding:0.5rem;">7+</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Current</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specifies key types (see below)</td></tr>
  </tbody>
</table>
### Certifikát klíče (typ 5)

**Úvod:** Verze 0.9.12 (prosinec 2013)

**Účel:** Určuje nevýchozí typy klíčů a ukládá dodatečná data klíče nad rámec standardní 384bajtové struktury KeysAndCert.

**Struktura užitečných dat:**

```
+----+----+----+----+----+----+----+----+-//
|SPKtype|CPKtype| Excess SPK data     |
+----+----+----+----+----+----+----+----+-//
              | Excess CPK data...    |
+----+----+----+----+----+----+----+----+

SPKtype :: Signing Public Key Type (2 bytes)
           See SigningPublicKey table above

CPKtype :: Crypto Public Key Type (2 bytes)
           See PublicKey table above

Excess SPK data :: Signing key bytes beyond 128 bytes
                   Length: 0 to 65531 bytes

Excess CPK data :: Crypto key bytes beyond 256 bytes
                   Length: 0 to remaining space
```
**Zásadní implementační poznámky:**

1. **Pořadí typů klíčů:**
   - **UPOZORNĚNÍ:** Typ podpisového klíče je PŘED typem kryptografického klíče
   - Je to neintuitivní, ale je to zachováno kvůli kompatibilitě
   - Pořadí: SPKtype, CPKtype (ne CPKtype, SPKtype)

2. **Uspořádání dat klíčů v KeysAndCert:**
   ```
   [Crypto Public Key (partial/complete)]
   [Padding (if total key lengths < 384)]
   [Signing Public Key (partial/complete)]
   [Certificate Header (3 bytes)]
   [Key Certificate (4+ bytes)]
   [Excess Signing Key Data]
   [Excess Crypto Key Data]
   ```

3. **Výpočet přebytečných dat klíče:**
   - Pokud Crypto Key > 256 bajtů: Excess = (Crypto Length - 256)
   - Pokud Signing Key > 128 bajtů: Excess = (Signing Length - 128)
   - Padding = max(0, 384 - Crypto Length - Signing Length)

**Příklady (kryptografický klíč ElGamal):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Signing Key Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Total SPK Length</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Padding</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Excess in Cert</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Total Structure Size</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA_SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">128</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 7 = 394</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 7 = 394</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 7 = 394</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">132</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 11 = 398</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">128</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 135 = 522</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">384</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 391 = 778</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 7 = 394</td></tr>
  </tbody>
</table>
**Požadavky na identitu pro router:** - NULL certificate (prázdný certifikát) používán do verze 0.9.15 - Key Certificate (certifikát klíče) vyžadován pro nevýchozí typy klíčů od verze 0.9.16 - Šifrovací klíče X25519 podporovány od verze 0.9.48

**Požadavky na Destination (identifikátor cíle v I2P):** - NULL certifikát NEBO Key Certificate (dle potřeby) - Key Certificate (certifikát s klíčem) vyžadován pro nevýchozí typy podpisových klíčů od verze 0.9.12 - Pole veřejného kryptografického klíče se od verze 0.6 (2005) nepoužívá, ale stále musí být přítomno

**Důležitá varování:**

1. **NULL vs. KEY certifikát:**
   - Certifikát KEY s typy (0,0) určujícími ElGamal+DSA_SHA1 je povolen, ale nedoporučuje se
   - Pro ElGamal+DSA_SHA1 vždy používejte certifikát NULL (kanonická reprezentace)
   - Certifikát KEY s (0,0) je o 4 bajty delší a může způsobit problémy s kompatibilitou
   - Některé implementace nemusí certifikáty KEY s (0,0) zpracovávat správně

2. **Validace nadbytečných dat:**
   - Implementace MUSÍ ověřovat, že délka certifikátu odpovídá očekávané délce pro dané typy klíčů
   - Odmítat certifikáty s nadbytečnými daty, která neodpovídají typům klíčů
   - Zakázat koncová odpadní data po platné struktuře certifikátu

**JavaDoc:** [Certificate](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Certificate.html)

---

### Mapování

**Popis:** Soubor dvojic klíč–hodnota používaný pro konfiguraci a metadata.

**Formát:**

```
+----+----+----+----+----+----+----+----+
|  size   | key_string (len + data)| =  |
+----+----+----+----+----+----+----+----+
| val_string (len + data)     | ;  | ...
+----+----+----+----+----+----+----+

size :: Integer (2 bytes, big-endian)
        Total number of bytes that follow (not including size field)
        Range: 0 to 65535

key_string :: String
              Format: 1-byte length + UTF-8 data
              Length: 0-255 bytes

= :: Single byte (0x3D, '=' character)

val_string :: String
              Format: 1-byte length + UTF-8 data
              Length: 0-255 bytes

; :: Single byte (0x3B, ';' character)

[Repeat key_string = val_string ; for additional entries]
```
**Limity velikosti:** - Délka klíče: 0-255 bajtů (+ 1 bajt pro délku) - Délka hodnoty: 0-255 bajtů (+ 1 bajt pro délku) - Celková velikost mapování: 0-65535 bajtů (+ 2 bajty pole velikosti) - Maximální velikost struktury: 65537 bajtů

**Zásadní požadavek na řazení:**

Když se mapování vyskytují v **podepsaných strukturách** (RouterInfo, RouterAddress, Destination properties, I2CP SessionConfig), položky MUSÍ být seřazeny podle klíče, aby byla zajištěna invariance podpisu:

1. **Metoda řazení:** Lexikografické pořadí podle hodnot kódových bodů Unicode (ekvivalentní k Java String.compareTo())
2. **Rozlišování velikosti písmen:** Klíče a hodnoty obecně rozlišují velikost písmen (závisí na aplikaci)
3. **Duplicitní klíče:** NEJSOU povoleny v podepsaných strukturách (způsobí selhání ověření podpisu)
4. **Kódování znaků:** Porovnávání na úrovni bajtů v UTF-8

**Proč na řazení záleží:** - Podpisy se počítají na základě bajtové reprezentace - Různá pořadí klíčů vedou k různým podpisům - Nepodepsaná mapování nevyžadují řazení, ale měla by se řídit stejnou konvencí

**Poznámky k implementaci:**

1. **Redundance v kódování:**
   - Jsou přítomny jak oddělovače `=` a `;`, tak i bajty délky řetězce
   - Je to neefektivní, ale kvůli kompatibilitě je to zachováno
   - Bajty délky jsou směrodatné; oddělovače jsou vyžadovány, ale jsou nadbytečné

2. **Podpora znaků:**
   - Navzdory dokumentaci jsou `=` a `;` UVNITŘ ŘETĚZCŮ PODPOROVÁNY (o to se starají délkové bajty)
   - Kódování UTF-8 podporuje celý Unicode
   - **Upozornění:** I2CP používá UTF-8, ale I2NP historicky nezpracovával UTF-8 správně
   - Pro maximální kompatibilitu používejte pro I2NP mapování pokud možno ASCII

3. **Zvláštní kontexty:**
   - **RouterInfo/RouterAddress:** (informace a adresa routeru) MUSÍ být seřazeny, bez duplicit
   - **I2CP SessionConfig:** (konfigurace relace I2CP) MUSÍ být seřazeno, bez duplicit  
   - **Mapování aplikací:** Řazení je doporučeno, ale ne vždy vyžadováno

**Příklad (možnosti RouterInfo):**

```
Mapping size: 45 bytes
Sorted entries:
  caps=L       (capabilities)
  netId=2      (network ID)
  router.version=0.9.67
```
**JavaDoc:** [DataHelper](http://docs.i2p-projekt.de/javadoc/net/i2p/data/DataHelper.html)

---

## Specifikace společné struktury

### Klíče a certifikát

**Popis:** Základní struktura kombinující šifrovací klíč, podpisový klíč a certifikát. Používá se jako RouterIdentity i jako Destination.

**Struktura:**

```
+----+----+----+----+----+----+----+----+
| public_key                            |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| padding (optional)                    |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signing_key                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| certificate                           |
+----+----+----+-//

public_key :: PublicKey (partial or full)
              Default: 256 bytes (ElGamal)
              Other sizes: As specified in Key Certificate

padding :: Random data
           Length: 0 bytes or as needed
           CONSTRAINT: public_key + padding + signing_key = 384 bytes

signing_key :: SigningPublicKey (partial or full)
               Default: 128 bytes (DSA_SHA1)
               Other sizes: As specified in Key Certificate

certificate :: Certificate
               Minimum: 3 bytes (NULL certificate)
               Common: 7 bytes (Key Certificate with default keys)

TOTAL LENGTH: 387+ bytes (never assume exactly 387!)
```
**Zarovnání klíčů:** - **Veřejný kryptografický klíč:** Zarovnaný na začátku (bajt 0) - **Vycpávka:** Uprostřed (pokud je potřeba) - **Veřejný klíč pro podpis:** Zarovnaný na konci (bajt 256 až bajt 383) - **Certifikát:** Začíná na bajtu 384

**Výpočet velikosti:**

```
Total size = 384 + 3 + key_certificate_length

For NULL certificate (ElGamal + DSA_SHA1):
  Total = 384 + 3 = 387 bytes

For Key Certificate (EdDSA + X25519):
  Total = 384 + 3 + 4 = 391 bytes

For larger keys (e.g., RSA_4096):
  Total = 384 + 3 + 4 + excess_key_data_length
```
### Pokyny pro generování vycpávky ([Návrh 161](/cs/proposals/161-ri-dest-padding/))

**Verze implementace:** 0.9.57 (leden 2023, vydání 2.1.0)

**Pozadí:** - U klíčů jiných než ElGamal+DSA je výplň přítomna v pevné struktuře o velikosti 384 bajtů - U Destinations (cílové identifikátory v I2P) je pole veřejného klíče o velikosti 256 bajtů nevyužité od verze 0.6 (2005) - Výplň by měla být generována tak, aby byla komprimovatelná a přitom zůstala bezpečná

**Požadavky:**

1. **Minimální množství náhodných dat:**
   - Použijte alespoň 32 bajtů kryptograficky bezpečných náhodných dat
   - To poskytuje dostatečnou entropii pro zajištění bezpečnosti

2. **Strategie komprese:**
   - Opakujte těch 32 bajtů napříč polem výplně/veřejného klíče
   - Protokoly jako I2NP Database Store, Streaming SYN, SSU2 handshake používají kompresi
   - Výrazná úspora šířky pásma bez ohrožení bezpečnosti

3. **Příklady:**

**Router identita (X25519 + EdDSA):**

```
Structure:
- 32 bytes X25519 public key
- 320 bytes padding (10 copies of 32-byte random data)
- 32 bytes EdDSA public key
- 7 bytes Key Certificate

Compression savings: ~288 bytes when compressed
```
**Cíl (ElGamal-unused + EdDSA):**

```
Structure:
- 256 bytes unused ElGamal field (11 copies of 32-byte random data, truncated to 256)
- 96 bytes padding (3 copies of 32-byte random data)
- 32 bytes EdDSA public key  
- 7 bytes Key Certificate

Compression savings: ~320 bytes when compressed
```
4. **Proč to funguje:**
   - Hash SHA-256 celé struktury stále zahrnuje veškerou entropii
   - Distribuce DHT síťové databáze závisí pouze na hashi
   - Podepisovací klíč (32 bajtů EdDSA/X25519) poskytuje 256 bitů entropie
   - Dalších 32 bajtů opakovaných náhodných dat = celkem 512 bitů entropie
   - Více než dostačující pro kryptografickou odolnost

5. **Poznámky k implementaci:**
   - MUSÍ ukládat a přenášet celou strukturu o velikosti 387+ bajtů
   - Hash SHA-256 se počítá nad kompletní nekomprimovanou strukturou
   - Komprese se aplikuje na úrovni protokolu (I2NP, Streaming, SSU2)
   - Zpětně kompatibilní se všemi verzemi od 0.6 (2005)

**JavaDoc:** [KeysAndCert](http://docs.i2p-projekt.de/javadoc/net/i2p/data/KeysAndCert.html)

---

### RouterIdentity (identita routeru)

**Popis:** Jednoznačně identifikuje router (směrovač) v síti I2P. Stejná struktura jako KeysAndCert.

**Formát:** Viz strukturu KeysAndCert výše

**Aktuální požadavky (k verzi 0.9.58):**

1. **Povinné typy klíčů:**
   - **Šifrování:** X25519 (typ 4, 32 bajtů)
   - **Podepisování:** EdDSA_SHA512_Ed25519 (typ 7, 32 bajtů)
   - **Certifikát:** Certifikát klíče (typ 5)

2. **Zastaralé typy klíčů:**
   - ElGamal (typ 0) označen jako zastaralý pro identity routerů od verze 0.9.58
   - DSA_SHA1 (typ 0) označen jako zastaralý pro identity routerů od verze 0.9.58
   - Tyto by NEMĚLY být používány pro nové routery

3. **Typická velikost:**
   - X25519 + EdDSA s certifikátem klíče = 391 bajtů
   - 32 bajtů veřejného klíče X25519
   - 320 bajtů výplně (komprimovatelná podle [Proposal 161](/cs/proposals/161-ri-dest-padding/))
   - 32 bajtů veřejného klíče EdDSA
   - 7 bajtů certifikátu (3bajtová hlavička + 4 bajty typů klíčů)

**Historický vývoj:** - Před 0.9.16: Vždy nulový certifikát (ElGamal + DSA_SHA1) - 0.9.16-0.9.47: Přidána podpora pro Key Certificate (typ certifikátu určující typ klíče) - 0.9.48+: Podpora šifrovacích klíčů X25519 - 0.9.58+: ElGamal a DSA_SHA1 zastaralé

**Klíč síťové databáze:** - RouterInfo (záznam s informacemi o routeru v I2P) je indexován pomocí SHA-256 hashe úplného RouterIdentity - Hash je vypočten nad celou strukturou o 391+ bajtech (včetně výplně)

**Viz také:** - Pokyny pro generování paddingu (vycpávky) ([Proposal 161](/cs/proposals/161-ri-dest-padding/)) - Specifikace Key Certificate výše

**JavaDoc:** [RouterIdentity](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterIdentity.html)

---

### Cíl

**Popis:** Identifikátor koncového bodu pro bezpečné doručování zpráv. Strukturálně totožný s KeysAndCert, ale s odlišnou sémantikou použití.

**Formát:** Viz strukturu KeysAndCert výše

**Zásadní rozdíl oproti RouterIdentity:** - **Pole veřejného klíče se NEPOUŽÍVÁ a může obsahovat náhodná data** - Toto pole se nepoužívá od verze 0.6 (2005) - Původně bylo určeno pro staré šifrování I2CP-to-I2CP (zakázáno) - Aktuálně slouží pouze jako IV (inicializační vektor) pro zastaralé šifrování LeaseSet

**Aktuální doporučení:**

1. **Podpisový klíč:**
   - **Doporučeno:** EdDSA_SHA512_Ed25519 (typ 7, 32 bajtů)
   - Alternativy: typy ECDSA pro zachování kompatibility se staršími verzemi
   - Vyhněte se: DSA_SHA1 (zastaralé, nedoporučuje se)

2. **Šifrovací klíč:**
   - Pole se nepoužívá, ale musí být přítomné
   - **Doporučeno:** Vyplňte náhodnými daty dle [Proposal 161](/cs/proposals/161-ri-dest-padding/) (komprimovatelná)
   - Velikost: vždy 256 bajtů (slot pro ElGamal, i když se ElGamal nepoužívá)

3. **Certifikát:**
   - NULL certificate pro ElGamal + DSA_SHA1 (jen pro starší verze)
   - Key Certificate pro všechny ostatní typy podpisových klíčů

**Typický moderní cíl:**

```
Structure:
- 256 bytes unused field (random data, compressible)
- 96 bytes padding (random data, compressible)
- 32 bytes EdDSA signing public key
- 7 bytes Key Certificate

Total: 391 bytes
Compression savings: ~320 bytes
```
**Skutečný šifrovací klíč:** - Šifrovací klíč pro Destination (cílový identifikátor) je v **LeaseSet**, nikoli v Destination - LeaseSet obsahuje aktuální veřejné šifrovací klíče - Viz specifikaci LeaseSet2 pro nakládání se šifrovacími klíči

**Klíč síťové databáze:** - LeaseSet je indexován podle hashe SHA-256 celého Destination (cílového identifikátoru) - Hash je vypočítán nad celou strukturou o velikosti 387+ bajtů

**JavaDoc:** [Destination](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Destination.html)

---

## Struktury síťové databáze

### Pronájem

**Popis:** Oprávňuje konkrétní tunnel přijímat zprávy pro Destination (cílový identifikátor). Součást původního formátu LeaseSet (typ 1).

**Formát:**

```
+----+----+----+----+----+----+----+----+
| tunnel_gw                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|     tunnel_id     |      end_date
+----+----+----+----+----+----+----+----+
                    |
+----+----+----+----+

tunnel_gw :: Hash (32 bytes)
             SHA-256 hash of the gateway RouterIdentity

tunnel_id :: TunnelId (4 bytes)
             Tunnel identifier at the gateway router

end_date :: Date (8 bytes)
            Expiration timestamp in milliseconds since epoch
```
**Celková velikost:** 44 bajtů

**Použití:** - Používá se pouze v původním LeaseSet (typ 1, zastaralý) - Pro LeaseSet2 a pozdější varianty použijte místo toho Lease2

**JavaDoc:** [Lease](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Lease.html)

---

### LeaseSet (Typ 1)

**Popis:** Původní formát LeaseSet. Obsahuje autorizované tunnels a klíče pro Destination (identifikátor cíle v I2P). Uloženo v síťové databázi. **Stav: Zastaralé** (místo toho použijte LeaseSet2).

**Struktura:**

```
+----+----+----+----+----+----+----+----+
| destination                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| encryption_key                        |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signing_key                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| num| Lease 0                          |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Lease 1                               |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Lease ($num-1)                        |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

destination :: Destination
               Length: 387+ bytes

encryption_key :: PublicKey (256 bytes, ElGamal)
                  Used for end-to-end ElGamal/AES+SessionTag encryption
                  Generated anew at each router startup (not persistent)

signing_key :: SigningPublicKey (128+ bytes)
               Same type as Destination signing key
               Used for LeaseSet revocation (unimplemented)
               Generated anew at each router startup (not persistent)

num :: Integer (1 byte)
       Number of Leases to follow
       Range: 0-16

leases :: Array of Lease structures
          Length: $num × 44 bytes
          Each Lease is 44 bytes

signature :: Signature (40+ bytes)
             Length determined by Destination signing key type
             Signed by Destination's SigningPrivateKey
```
**Uložení v databázi:** - **Typ databáze:** 1 - **Klíč:** SHA-256 hash destinace - **Hodnota:** Úplná struktura LeaseSet

**Důležité poznámky:**

1. **Veřejný klíč Destination (cílový identifikátor v I2P) se nepoužívá:**
   - Pole veřejného klíče pro šifrování v Destination se nepoužívá
   - Šifrovací klíč v LeaseSet je skutečný šifrovací klíč

2. **Dočasné klíče:**
   - `encryption_key` je dočasný (znovu vygenerován při startu routeru)
   - `signing_key` je dočasný (znovu vygenerován při startu routeru)
   - Ani jeden z klíčů se neuchovává napříč restarty

3. **Revokace (neimplementováno):**
   - `signing_key` byl zamýšlen pro revokaci LeaseSetu
   - Mechanismus revokace nebyl nikdy implementován
   - LeaseSet s nulovým počtem lease (časově omezených záznamů) byl zamýšlen pro revokaci, ale není používán

4. **Verzování/časové razítko:**
   - LeaseSet nemá žádné explicitní pole časového razítka `published`
   - Verze je nejbližší okamžik vypršení platnosti ze všech leases (technické záznamy o tunelech v I2P)
   - Nový LeaseSet musí mít dřívější dobu vypršení platnosti lease, aby byl přijat

5. **Zveřejňování expirace lease (dočasného záznamu pro tunnel):**
   - Před 0.9.7: Všechny lease byly zveřejněny se stejnou expirací (nejdřívější)
   - 0.9.7+: Zveřejňují se skutečné expirace jednotlivých lease
   - Toto je detail implementace, nikoli součást specifikace

6. **Nulový počet leases:**
   - LeaseSet s nulovým počtem leases (Lease – časově omezený záznam) je technicky povoleno
   - Určeno pro revokaci (neimplementováno)
   - V praxi se nepoužívá
   - Varianty LeaseSet2 vyžadují alespoň jeden Lease

**Zastarání:** LeaseSet typu 1 je zastaralý. Nové implementace by měly používat **LeaseSet2 (typ 3)** který poskytuje: - Pole s časovým razítkem publikace (lepší verzování) - Podpora více šifrovacích klíčů - Možnost offline podpisu - 4bajtové expirace lease (oproti 8bajtovým) - Flexibilnější možnosti

**JavaDoc:** [LeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/LeaseSet.html)

---

## Varianty LeaseSet

### Lease2 (druhá generace záznamu Lease v I2P)

**Popis:** Vylepšený formát lease (záznamu o tunelu) se 4bajtovou expirací. Používá se v LeaseSet2 (typ 3) a MetaLeaseSet (typ 7).

**Úvod:** Verze 0.9.38 (viz [Návrh 123](/proposals/123-new-netdb-entries/))

**Formát:**

```
+----+----+----+----+----+----+----+----+
| tunnel_gw                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|     tunnel_id     |      end_date     |
+----+----+----+----+----+----+----+----+

tunnel_gw :: Hash (32 bytes)
             SHA-256 hash of gateway RouterIdentity

tunnel_id :: TunnelId (4 bytes)
             Tunnel identifier at gateway

end_date :: 4-byte timestamp (seconds since epoch)
            Rolls over in year 2106
```
**Celková velikost:** 40 bajtů (o 4 bajty menší než původní Lease (záznam o pronájmu tunelu))

**Srovnání s původním Lease (záznamem v leaseSet):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1pxsolid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Lease (Type&nbsp;1)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Lease2 (Type&nbsp;3+)</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Size</td><td style="border:1px solid var(--color-border); padding:0.5rem;">44 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Expiration Size</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes (ms)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes (seconds)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Precision</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Millisecond</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Second</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Rollover</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Year&nbsp;292,277,026,596</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Year&nbsp;2106</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Used In</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet (deprecated)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2, MetaLeaseSet</td></tr>
  </tbody>
</table>
**JavaDoc:** [Lease2](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Lease2.html)

---

### Offline podpis

**Popis:** Volitelná struktura pro předem podepsané dočasné klíče, umožňující publikaci LeaseSetu bez online přístupu k soukromému podpisovému klíči Destination (identita cílové služby v I2P).

**Úvod:** Verze 0.9.38 (viz [Návrh 123](/proposals/123-new-netdb-entries/))

**Formát:**

```
+----+----+----+----+----+----+----+----+
|     expires       | sigtype |         |
+----+----+----+----+----+----+         +
|       transient_public_key            |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|           signature                   |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

expires :: 4-byte timestamp (seconds since epoch)
           Expiration of transient key validity
           Rolls over in year 2106

sigtype :: 2-byte signature type
           Type of transient_public_key (see SigningPublicKey types)

transient_public_key :: SigningPublicKey
                        Length determined by sigtype
                        Temporary signing key for LeaseSet

signature :: Signature
             Length determined by Destination's signing key type
             Signature of (expires || sigtype || transient_public_key)
             Signed by Destination's permanent SigningPrivateKey
```
**Účel:** - Umožňuje offline generování LeaseSet - Chrání hlavní klíč Destination (identifikátor cíle v I2P) před online odhalením - Dočasný klíč lze zneplatnit zveřejněním nového LeaseSet bez offline podpisu

**Scénáře použití:**

1. **Vysoce zabezpečené destinace:**
   - Hlavní podpisový klíč uložen offline (HSM, studené úložiště)
   - Dočasné klíče generované offline pro omezená časová období
   - Kompromitovaný dočasný klíč neprozradí hlavní klíč

2. **Šifrované publikování LeaseSet:**
   - EncryptedLeaseSet může obsahovat offline podpis
   - Zaslepený veřejný klíč + offline podpis poskytují dodatečné zabezpečení

**Bezpečnostní hlediska:**

1. **Správa doby platnosti:**
   - Nastavte rozumnou dobu platnosti (dny až týdny, ne roky)
   - Před vypršením generujte nové dočasné klíče
   - Kratší doba platnosti = lepší zabezpečení, více údržby

2. **Generování klíčů:**
   - Generujte dočasné klíče offline v zabezpečeném prostředí
   - Podepište hlavním klíčem offline
   - Přeneste pouze podepsaný dočasný klíč + podpis do online routeru

3. **Odvolání:**
   - Zveřejněte nový LeaseSet bez offline podpisu k implicitnímu odvolání
   - Nebo zveřejněte nový LeaseSet s jiným dočasným klíčem

**Ověření podpisu:**

```
Data to sign: expires (4 bytes) || sigtype (2 bytes) || transient_public_key

Verification:
1. Extract Destination from LeaseSet
2. Get Destination's SigningPublicKey
3. Verify signature over (expires || sigtype || transient_public_key)
4. Check that current time < expires
5. If valid, use transient_public_key to verify LeaseSet signature
```
**Poznámky k implementaci:** - Celková velikost se liší podle sigtype (typ podpisu) a typu podpisového klíče Destination - Minimální velikost: 4 + 2 + 32 (klíč EdDSA) + 64 (podpis EdDSA) = 102 bajtů - Maximální praktická velikost: ~600 bajtů (dočasný klíč RSA-4096 + podpis RSA-4096)

**Kompatibilní s:** - LeaseSet2 (typ 3) - EncryptedLeaseSet (typ 5) - MetaLeaseSet (typ 7)

**Viz také:** [Proposal 123](/proposals/123-new-netdb-entries/) pro podrobný offline podpisový protokol.

---

### LeaseSet2Header

**Popis:** Společná struktura hlavičky pro LeaseSet2 (typ 3) a MetaLeaseSet (typ 7).

**Úvod:** Verze 0.9.38 (viz [Návrh 123](/proposals/123-new-netdb-entries/))

**Formát:**

```
+----+----+----+----+----+----+----+----+
| destination                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|     published     | expires |  flags  |
+----+----+----+----+----+----+----+----+
| offline_signature (optional)          |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

destination :: Destination
               Length: 387+ bytes

published :: 4-byte timestamp (seconds since epoch)
             Publication time of this LeaseSet
             Rolls over in year 2106

expires :: 2-byte offset (seconds)
           Offset from published timestamp
           Maximum: 65535 seconds (18.2 hours)

flags :: 2 bytes (bit flags)
         See flag definitions below

offline_signature :: OfflineSignature (optional)
                     Present only if flags bit 0 is set
                     Variable length
```
**Minimální celková velikost:** 395 bajtů (bez offline podpisu)

**Definice příznaků (pořadí bitů: 15 14 ... 3 2 1 0):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Bit</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline Keys</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0 = No offline keys, 1 = Offline signature present</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unpublished</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0 = Standard published, 1 = Unpublished (client-side only)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0 = Standard, 1 = Will be blinded when published</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3-15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Must be 0 for compatibility</td></tr>
  </tbody>
</table>
**Podrobnosti příznaku:**

**Bit 0 - Offline klíče:** - `0`: Žádný offline podpis, použijte podpisový klíč Destination (kryptografický identifikátor cíle v I2P) k ověření podpisu LeaseSet - `1`: Struktura OfflineSignature následuje za polem flags

**Bit 1 - Nezveřejněno:** - `0`: Standardně publikovaný LeaseSet, měl by být rozšířen k floodfills - `1`: Nezveřejněný LeaseSet (pouze na straně klienta)   - Nesmí být rozšiřován, publikován ani posílán v odpovědi na dotazy   - Pokud vyprší, NEdotazovat se netdb na náhradu (pokud není nastaven i bit 2)   - Používá se pro lokální tunnels nebo testování

**Bit 2 - Blinded (zaslepené) (od verze 0.9.42):** - `0`: Standardní LeaseSet - `1`: Tento nešifrovaný LeaseSet bude při publikování blinded a zašifrován   - Publikovaná verze bude EncryptedLeaseSet (typ 5)   - Pokud vyprší, vyhledejte v netdb náhradu na **blinded location**   - Je také nutné nastavit bit 1 na 1 (unpublished + blinded)   - Používá se pro šifrované skryté služby

**Limity vypršení platnosti:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">LeaseSet Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Maximum Expires Value</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Maximum Actual Time</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2 (type 3)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈660 seconds</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈11 minutes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MetaLeaseSet (type 7)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">65,535 seconds</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈18.2 hours</td></tr>
  </tbody>
</table>
**Požadavky na časové razítko zveřejnění:**

LeaseSet (typ 1) neměl pole published, což vyžadovalo hledání nejdřívějšího vypršení platnosti lease (záznamu o pronájmu trasy v I2P) pro účely verzování. LeaseSet2 přidává explicitní časové razítko `published` s rozlišením na 1 sekundu.

**Kritická poznámka k implementaci:** - Routers MUSÍ omezovat rychlost publikování LeaseSet na **výrazně pomalejší než jednou za sekundu** pro každou Destination (identifikátor cíle) - Pokud publikujete rychleji, zajistěte, aby každý nový LeaseSet měl čas `published` alespoň o 1 sekundu později - Floodfills odmítnou LeaseSet, pokud čas `published` není novější než aktuální verze - Doporučený minimální interval: 10-60 sekund mezi publikacemi

**Příklady výpočtů:**

**LeaseSet2 (maximálně 11 minut):**

```
published = 1704067200 (2024-01-01 00:00:00 UTC)
expires = 660 (seconds)
Actual expiration = 1704067200 + 660 = 1704067860 (2024-01-01 00:11:00 UTC)
```
**MetaLeaseSet (max. 18,2 hodiny):**

```
published = 1704067200 (2024-01-01 00:00:00 UTC)
expires = 65535 (seconds)
Actual expiration = 1704067200 + 65535 = 1704132735 (2024-01-01 18:12:15 UTC)
```
**Verzování:** - LeaseSet je považován za „novější“, pokud je časové razítko `published` vyšší - Floodfills ukládají a rozesílají pouze nejnovější verzi - Dávejte pozor, když se nejstarší Lease (záznam o tunelu v I2P) shoduje s nejstarším Lease předchozího LeaseSetu

---

### LeaseSet2 (Typ 3)

**Popis:** Moderní formát LeaseSet s více šifrovacími klíči, offline podpisy a záznamy o službách. Aktuální standard pro skryté služby I2P.

**Úvod:** Verze 0.9.38 (viz [Návrh 123](/proposals/123-new-netdb-entries/))

**Struktura:**

```
+----+----+----+----+----+----+----+----+
|         ls2_header                    |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|          options                      |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|numk| keytype0| keylen0 |              |
+----+----+----+----+----+              +
|          encryption_key_0             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| keytypen| keylenn |                   |
+----+----+----+----+                   +
|          encryption_key_n             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| num| Lease2 0                         |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Lease2($num-1)                        |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

ls2header :: LeaseSet2Header
             Length: 395+ bytes (varies with offline signature)

options :: Mapping
           Key-value pairs for service records and metadata
           Length: 2+ bytes (size field + data)

numk :: Integer (1 byte)
        Number of encryption keys
        Range: 1 to (implementation-defined maximum, typically 8)

keytype :: 2-byte encryption type
           See PublicKey type table

keylen :: 2-byte key length
          Must match keytype specification

encryption_key :: PublicKey
                  Length: keylen bytes
                  Type: keytype

[Repeat keytype/keylen/encryption_key for each key]

num :: Integer (1 byte)
       Number of Lease2s
       Range: 1-16 (at least one required)

leases :: Array of Lease2 structures
          Length: $num × 40 bytes

signature :: Signature
             Length determined by signing key type
             Signed over entire structure including database type prefix
```
**Úložiště databáze:** - **Typ databáze:** 3 - **Klíč:** SHA-256 hash Destination (I2P cílová adresa) - **Hodnota:** Úplná struktura LeaseSet2

**Výpočet podpisu:**

```
Data to sign: database_type (1 byte, value=3) || complete LeaseSet2 data

Verification:
1. Prepend database type byte (0x03) to LeaseSet2 data
2. If offline signature present:
   - Verify offline signature against Destination key
   - Verify LeaseSet2 signature against transient key
3. Else:
   - Verify LeaseSet2 signature against Destination key
```
### Preferenční pořadí šifrovacích klíčů

**Pro publikovaný (serverový) LeaseSet:** - Klíče jsou uvedeny v pořadí preferencí serveru (nejpreferovanější první) - Klienti podporující více typů BY MĚLI respektovat preference serveru - Vyberte ze seznamu první podporovaný typ - Obecně jsou typy klíčů s vyšším číslem (novější) bezpečnější/efektivnější - Doporučené pořadí: Uvádějte klíče v obráceném pořadí podle kódu typu (nejnovější první)

**Příklad předvolby serveru:**

```
numk = 2
Key 0: X25519 (type 4, 32 bytes)         [Most preferred]
Key 1: ElGamal (type 0, 256 bytes)       [Legacy compatibility]
```
**Pro nepublikovaný (klientský) LeaseSet:** - Pořadí klíčů prakticky nehraje roli (pokusy o připojení ke klientům jsou vzácné) - Pro zachování konzistence dodržujte stejnou konvenci

**Výběr klíče klienta:** - Respektovat preferenci serveru (vybrat první podporovaný typ) - Nebo použít preferenci definovanou implementací - Nebo určit kombinovanou preferenci na základě schopností obou stran

### Mapování možností

**Požadavky:** - Možnosti MUSÍ být seřazeny podle klíče (lexikograficky, v pořadí bajtů UTF-8) - Řazení zajišťuje neměnnost podpisu - Duplicitní klíče NEJSOU povoleny

**Standardní formát ([Návrh 167](/proposals/167-service-records/)):**

Od API 0.9.66 (červen 2025, vydání 2.9.0) mají možnosti záznamu služby standardizovaný formát. Úplnou specifikaci viz [Proposal 167](/proposals/167-service-records/).

**Formát volby záznamu služby:**

```
Key: _service._proto
Value: record_type ttl [priority weight] port target [appoptions]

service :: Symbolic name of service (lowercase, [a-z0-9-])
           Examples: smtp, http, irc, mumble
           Use standard identifiers from IANA Service Name Registry
           or Linux /etc/services when available

proto :: Transport protocol (lowercase, [a-z0-9-])
         "tcp" = streaming protocol
         "udp" = repliable datagrams
         Protocol indicators for raw datagrams may be defined later

record_type :: "0" (self-reference) or "1" (SRV record)

ttl :: Time to live in seconds (positive integer)
       Recommended minimum: 86400 (one day)
       Prevents frequent re-queries

For record_type = 0 (self-reference):
  port :: I2CP port number (non-negative integer)
  appoptions :: Optional application-specific data (no spaces or commas)

For record_type = 1 (SRV record):
  priority :: Lower value = more preferred (non-negative integer)
  weight :: Relative weight for same priority, higher = more likely (non-negative)
  port :: I2CP port number (non-negative integer)
  target :: Hostname or b32 of destination (lowercase)
            Format: "example.i2p" or "aaaaa...aaaa.b32.i2p"
            Recommend b32 unless hostname is "well known"
  appoptions :: Optional application-specific data (no spaces or commas)
```
**Ukázkové záznamy služby:**

**1. Samoodkazující SMTP server:**

```
Destination: aaaa...aaaa.b32.i2p (this LeaseSet)
Option: "_smtp._tcp" = "0 999999 25"

Meaning: This destination provides SMTP service on I2CP port 25
```
**2. Jeden externí SMTP server:**

```
Destination: aaaa...aaaa.b32.i2p (this LeaseSet)
Option: "_smtp._tcp" = "1 86400 0 0 25 bbbb...bbbb.b32.i2p"

Meaning: SMTP service provided by bbbb...bbbb on port 25
         TTL = 1 day, single server (priority=0, weight=0)
```
**3. Více SMTP serverů (vyvažování zátěže):**

```
Destination: aaaa...aaaa.b32.i2p (this LeaseSet)
Option: "_smtp._tcp" = "1 86400 0 0 25 bbbb...bbbb.b32.i2p,1 86400 1 0 25 cccc...cccc.b32.i2p"

Meaning: Two SMTP servers
         bbbb...bbbb (priority=0, preferred)
         cccc...cccc (priority=1, backup)
```
**4. HTTP služba s možnostmi aplikace:**

```
Option: "_http._tcp" = "0 86400 80 tls=1.3;cert=ed25519"

Meaning: HTTP on port 80 with TLS 1.3 and EdDSA certificates
```
**Doporučení pro TTL (čas života):** - Minimum: 86400 sekund (1 den) - Delší TTL snižuje zátěž dotazů na netdb - Vyvážení mezi snížením počtu dotazů a propagací aktualizací služby - Pro stabilní služby: 604800 (7 dní) nebo déle

**Poznámky k implementaci:**

1. **Šifrovací klíče (stav k verzi 0.9.44):**
   - ElGamal (typ 0, 256 bajtů): Zpětná kompatibilita
   - X25519 (typ 4, 32 bajtů): Současný standard
   - Varianty MLKEM: Postkvantové (beta, dosud nefinalizované)

2. **Ověření délky klíče:**
   - Floodfills a klienti MUSÍ být schopni parsovat neznámé typy klíčů
   - Použijte pole keylen k přeskočení neznámých klíčů
   - Neukončujte parsování s chybou, pokud je typ klíče neznámý

3. **Časová značka zveřejnění:**
   - Viz poznámky k LeaseSet2Header ohledně omezování četnosti
   - Minimální rozestup mezi zveřejněními: 1 sekunda
   - Doporučeno: 10–60 sekund mezi zveřejněními

4. **Migrace typu šifrování:**
   - Použití více klíčů umožňuje postupnou migraci
   - Během přechodného období uveďte jak staré, tak nové klíče
   - Starý klíč odstraňte po uplynutí dostatečné doby pro aktualizaci klientů

**JavaDoc:** [LeaseSet2](http://docs.i2p-projekt.de/javadoc/net/i2p/data/LeaseSet2.html)

---

### MetaLease (speciální typ Lease s metadaty v I2P)

**Popis:** Struktura Lease (záznam v LeaseSet) pro MetaLeaseSet (metasada LeaseSet), která může odkazovat na jiné LeaseSets místo na tunnels. Používá se pro vyvažování zátěže a redundanci.

**Úvod:** Verze 0.9.38, naplánováno na 0.9.40 (viz [Návrh 123](/proposals/123-new-netdb-entries/))

**Formát:**

```
+----+----+----+----+----+----+----+----+
| tunnel_gw                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|    flags     |cost|      end_date     |
+----+----+----+----+----+----+----+----+

tunnel_gw :: Hash (32 bytes)
             SHA-256 hash of:
             - Gateway RouterIdentity (for type 1), OR
             - Another MetaLeaseSet destination (for type 3/5/7)

flags :: 3 bytes
         Bit order: 23 22 ... 3 2 1 0
         Bits 3-0: Entry type (see table below)
         Bits 23-4: Reserved (must be 0)

cost :: 1 byte (0-255)
        Lower value = higher priority
        Used for load balancing

end_date :: 4-byte timestamp (seconds since epoch)
            Expiration time
            Rolls over in year 2106
```
**Celková velikost:** 40 bajtů

**Typ položky (bity příznaků 3–0):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Unknown</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unknown/invalid entry</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Points to LeaseSet (type 1, deprecated)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Points to LeaseSet2 (type 3)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Points to EncryptedLeaseSet (type 5)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MetaLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align-center?">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Points to another MetaLeaseSet (type 7)</td></tr>
  </tbody>
</table>
**Scénáře použití:**

1. **Vyvažování zátěže:**
   - MetaLeaseSet (metasada pro agregaci více LeaseSet) s více záznamy MetaLease (metazáznamy)
   - Každý záznam odkazuje na jiný LeaseSet2 (novější formát LeaseSet)
   - Klienti vybírají na základě pole cost

2. **Redundance:**
   - Více záznamů odkazujících na záložní LeaseSets
   - Záložní řešení, pokud je primární LeaseSet nedostupný

3. **Migrace služby:**
   - MetaLeaseSet (meta-sada LeaseSet) odkazuje na nový LeaseSet
   - Umožňuje plynulý přechod mezi Destinations (cílovými adresami v I2P)

**Použití pole Cost:** - Nižší hodnota Cost = vyšší priorita - Cost 0 = nejvyšší priorita - Cost 255 = nejnižší priorita - Klienti BY MĚLI preferovat záznamy s nižší hodnotou Cost - Záznamy se stejnou hodnotou Cost mohou být náhodně vyvažovány

**Srovnání s Lease2:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Lease2</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">MetaLease</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Size</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Tunnel ID</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Replaced by flags (3 bytes) + cost (1 byte)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Points To</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specific tunnel</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet or MetaLeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Usage</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Direct tunnel reference</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Indirection/load balancing</td></tr>
  </tbody>
</table>
**JavaDoc:** [MetaLease](http://docs.i2p-projekt.de/javadoc/net/i2p/data/MetaLease.html)

---

### MetaLeaseSet (Typ 7; speciální varianta leaseSet)

**Popis:** Varianta LeaseSetu, která obsahuje položky MetaLease a poskytuje zprostředkované odkazování na jiné LeaseSety. Používá se pro vyvažování zátěže, redundanci a migraci služeb.

**Úvod:** Definováno ve verzi 0.9.38, naplánováno jako funkční v 0.9.40 (viz [Návrh 123](/proposals/123-new-netdb-entries/))

**Stav:** Specifikace je dokončena. Stav produkčního nasazení by měl být ověřen podle aktuálních vydání I2P.

**Struktura:**

```
+----+----+----+----+----+----+----+----+
|         ls2_header                    |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|          options                      |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| num| MetaLease 0                      |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| MetaLease($num-1)                     |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|numr|                                  |
+----+                                  +
|          revocation_0                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|          revocation_n                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

ls2header :: LeaseSet2Header
             Length: 395+ bytes

options :: Mapping
           Length: 2+ bytes (size + data)
           MUST be sorted by key

num :: Integer (1 byte)
       Number of MetaLease entries
       Range: 1 to (implementation-defined, recommend 1-16)

metaleases :: Array of MetaLease structures
              Length: $num × 40 bytes

numr :: Integer (1 byte)
        Number of revocation hashes
        Range: 0 to (implementation-defined, recommend 0-16)

revocations :: Array of Hash structures
               Length: $numr × 32 bytes
               SHA-256 hashes of revoked LeaseSet Destinations
```
**Úložiště databáze:** - **Typ databáze:** 7 - **Klíč:** SHA-256 hash z Destination (cíl v I2P) - **Hodnota:** Kompletní struktura MetaLeaseSet (typ rozšířeného leaseSetu)

**Výpočet podpisu:**

```
Data to sign: database_type (1 byte, value=7) || complete MetaLeaseSet data

Verification:
1. Prepend database type byte (0x07) to MetaLeaseSet data
2. If offline signature present in header:
   - Verify offline signature against Destination key
   - Verify MetaLeaseSet signature against transient key
3. Else:
   - Verify MetaLeaseSet signature against Destination key
```
**Scénáře použití:**

**1. Vyvažování zátěže:**

```
MetaLeaseSet for primary.i2p:
  MetaLease 0: cost=0, points to server1.i2p LeaseSet2
  MetaLease 1: cost=0, points to server2.i2p LeaseSet2
  MetaLease 2: cost=0, points to server3.i2p LeaseSet2

Clients randomly select among equal-cost entries
```
**2. Převzetí služeb při selhání:**

```
MetaLeaseSet for service.i2p:
  MetaLease 0: cost=0, points to primary.i2p LeaseSet2
  MetaLease 1: cost=100, points to backup.i2p LeaseSet2

Clients prefer cost=0 (primary), fall back to cost=100 (backup)
```
**3. Migrace služby:**

```
MetaLeaseSet for old-domain.i2p:
  MetaLease 0: cost=0, points to new-domain.i2p LeaseSet2

Transparently redirects clients from old to new destination
```
**4. Vícevrstvá architektura:**

```
MetaLeaseSet for service.i2p:
  MetaLease 0: cost=0, points to region1-meta.i2p (another MetaLeaseSet)
  MetaLease 1: cost=0, points to region2-meta.i2p (another MetaLeaseSet)

Each region MetaLeaseSet points to regional servers
Allows hierarchical load balancing
```
**Seznam zneplatnění:**

Revokační seznam umožňuje, aby MetaLeaseSet (rozšířená forma typu LeaseSet v I2P) výslovně odvolal dříve zveřejněné LeaseSets:

- **Účel:** Označit konkrétní Destinations (identifikátory cílů v I2P) jako již neplatné
- **Obsah:** Hashů SHA-256 odvolaných struktur Destination
- **Použití:** Klienti NESMÍ používat LeaseSets, jejichž hash Destination se nachází v revokačním seznamu
- **Typická hodnota:** Prázdné (numr=0) ve většině nasazení

**Příklad revokace:**

```
Service migrates from dest-v1.i2p to dest-v2.i2p:
  MetaLease 0: points to dest-v2.i2p
  Revocations: [hash(dest-v1.i2p)]

Clients will use v2 and ignore v1 even if cached
```
**Zpracování expirace:**

MetaLeaseSet (anglický termín pro speciální typ LeaseSet) používá LeaseSet2Header (anglický název hlavičky struktury LeaseSet2) s maximální hodnotou expires=65535 sekund (~18,2 hodin):

- Mnohem delší než LeaseSet2 (max ~11 minut)
- Vhodné pro relativně statickou indirekci
- Odkazované LeaseSets mohou mít kratší dobu platnosti
- Klienti musí kontrolovat platnost jak MetaLeaseSet, tak i odkazovaných LeaseSets

**Mapování možností:**

- Použijte stejný formát jako volby LeaseSet2
- Může obsahovat záznamy služby ([Proposal 167](/proposals/167-service-records/))
- MUSÍ být seřazeny podle klíče
- Záznamy služby zpravidla popisují koncovou službu, nikoli zprostředkovací strukturu

**Poznámky k implementaci klienta:**

1. **Postup resoluce:**
   ```
   1. Query netdb for MetaLeaseSet using SHA-256(Destination)
   2. Parse MetaLeaseSet, extract MetaLease entries
   3. Sort entries by cost (lower = better)
   4. For each entry in cost order:
      a. Extract LeaseSet hash from tunnel_gw field
      b. Determine entry type from flags
      c. Query netdb for referenced LeaseSet (may be another MetaLeaseSet)
      d. Check revocation list
      e. Check expiration
      f. If valid, use the LeaseSet; else try next entry
   ```

2. **Kešování:**
   - Kešujte jak MetaLeaseSet, tak odkazované LeaseSets
   - Kontrolujte vypršení platnosti na obou úrovních
   - Sledujte publikaci aktualizovaného MetaLeaseSet

3. **Failover (přepnutí při selhání):**
   - Pokud preferovaná položka selže, zkuste položku s dalším nejnižším nákladem
   - Zvažte označení selhaných položek jako dočasně nedostupných
   - Pravidelně znovu kontrolujte, zda se neobnovily

**Stav implementace:**

[Návrh 123](/proposals/123-new-netdb-entries/) uvádí, že některé části jsou stále „ve vývoji“. Implementátoři by měli: - Ověřit připravenost pro produkční nasazení v cílové verzi I2P - Otestovat podporu MetaLeaseSet (rozšířený typ leaseSet) před nasazením - Zkontrolovat aktualizované specifikace v novějších vydáních I2P

**JavaDoc:** [MetaLeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/MetaLeaseSet.html)

---

### EncryptedLeaseSet (šifrovaný LeaseSet; typ 5)

**Popis:** Šifrovaný a zaslepený LeaseSet pro zvýšenou ochranu soukromí. Pouze zaslepený veřejný klíč a metadata jsou viditelné; samotné leases (záznamy) a šifrovací klíče jsou šifrované.

**Úvod:** Definováno v 0.9.38, funkční od 0.9.39 (viz [Proposal 123](/proposals/123-new-netdb-entries/))

**Struktura:**

```
+----+----+----+----+----+----+----+----+
| sigtype |                             |
+----+----+                             +
|        blinded_public_key             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|     published     | expires |  flags  |
+----+----+----+----+----+----+----+----+
| offline_signature (optional)          |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|  len    |                             |
+----+----+                             +
|         encrypted_data                |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

sigtype :: 2-byte signature type
           Type of blinded_public_key
           MUST be RedDSA_SHA512_Ed25519 (type 11)

blinded_public_key :: SigningPublicKey (32 bytes for RedDSA)
                      Blinded version of Destination signing key
                      Used to verify signature on EncryptedLeaseSet

published :: 4-byte timestamp (seconds since epoch)
             Publication time
             Rolls over in year 2106

expires :: 2-byte offset (seconds)
           Offset from published
           Maximum: 65535 seconds (18.2 hours)
           Practical maximum for LeaseSet data: ~660 seconds (~11 min)

flags :: 2 bytes
         Bit 0: Offline signature present (0=no, 1=yes)
         Bit 1: Unpublished (0=published, 1=client-side only)
         Bits 15-2: Reserved (must be 0)

offline_signature :: OfflineSignature (optional)
                     Present only if flags bit 0 = 1
                     Variable length

len :: 2-byte integer
       Length of encrypted_data
       Range: 1 to 65535

encrypted_data :: Encrypted payload
                  Length: len bytes
                  Contains encrypted LeaseSet2 or MetaLeaseSet

signature :: Signature (64 bytes for RedDSA)
             Length determined by sigtype
             Signed by blinded_public_key or transient key
```
**Uložení v databázi:** - **Typ databáze:** 5 - **Klíč:** SHA-256 hash z **blinded Destination** (Destination: cílový identifikátor v I2P; nikoli původní Destination) - **Hodnota:** Úplná struktura EncryptedLeaseSet

**Zásadní rozdíly oproti LeaseSet2:**

1. **NEpoužívá strukturu LeaseSet2Header (hlavička LeaseSet verze 2)** (má podobná pole, ale jiné uspořádání)
2. **Zaslepený veřejný klíč** namísto plného Destination (I2P identifikátor cíle)
3. **Šifrovaná užitečná data** namísto leases a klíčů v otevřeném textu
4. **Databázový klíč je hash zaslepeného Destination**, ne původního Destination

**Výpočet podpisu:**

```
Data to sign: database_type (1 byte, value=5) || complete EncryptedLeaseSet data

Verification:
1. Prepend database type byte (0x05) to EncryptedLeaseSet data
2. If offline signature present (flags bit 0 = 1):
   - Verify offline signature against blinded public key
   - Verify EncryptedLeaseSet signature against transient key
3. Else:
   - Verify EncryptedLeaseSet signature against blinded public key
```
**Požadavek na typ podpisu:**

**MUSÍ se použít RedDSA_SHA512_Ed25519 (typ 11):** - 32bajtové zaslepené veřejné klíče - 64bajtové podpisy - Vyžadováno kvůli bezpečnostním vlastnostem zaslepení - Viz [specifikace Red25519](//docs/specs/red25519-signature-scheme/

**Klíčové rozdíly oproti EdDSA:** - Soukromé klíče odvozované pomocí modulární redukce (nikoli clamping, tj. ořezání bitů) - Podpisy obsahují 80 bajtů náhodných dat - Veřejné klíče používá přímo (nikoli hashe) - Umožňuje bezpečnou operaci zaslepení

**Zaslepení a šifrování:**

Pro veškeré podrobnosti viz [specifikaci EncryptedLeaseSet](/docs/specs/encryptedleaseset/):

**1. Oslepování klíče:**

```
Blinding process (daily rotation):
  secret = HKDF(original_signing_private_key, date_string, "i2pblinding1")
  alpha = SHA-256(secret) mod L (where L is Ed25519 group order)
  blinded_private_key = alpha * original_private_key
  blinded_public_key = alpha * original_public_key
```
**2. Umístění databáze:**

```
Client publishes to:
  Key = SHA-256(blinded_destination)
  
Where blinded_destination uses:
  - Blinded public key (signing key)
  - Same unused public key field (random)
  - Same certificate structure
```
**3. Šifrovací vrstvy (třívrstvé):**

**Vrstva 1 - Autentizační vrstva (přístup klienta):** - Šifrování: proudová šifra ChaCha20 - Odvozování klíčů: HKDF s tajemstvími pro jednotlivé klienty - Autentizovaní klienti mohou dešifrovat vnější vrstvu

**Vrstva 2 - šifrovací vrstva:** - Šifrování: ChaCha20 - Klíč: odvozen z Diffie–Hellmanovy výměny klíčů mezi klientem a serverem - Obsahuje skutečný LeaseSet2 nebo MetaLeaseSet

**Vrstva 3 - Vnitřní LeaseSet:** - Kompletní LeaseSet2 nebo MetaLeaseSet - Obsahuje všechny tunnels, šifrovací klíče, volby - Přístupné pouze po úspěšném dešifrování

**Odvozování šifrovacího klíče:**

```
Client has: ephemeral_client_private_key
Server has: ephemeral_server_public_key (in encrypted_data)

Shared secret = X25519(client_private, server_public)
Encryption key = HKDF(shared_secret, context_info, "i2pblinding2")
```
**Proces zjišťování:**

**Pro autorizované klienty:**

```
1. Client knows original Destination
2. Client computes current blinded Destination (based on current date)
3. Client computes database key: SHA-256(blinded_destination)
4. Client queries netdb for EncryptedLeaseSet using blinded key
5. Client decrypts layer 1 using authorization credentials
6. Client decrypts layer 2 using DH shared secret
7. Client extracts inner LeaseSet2/MetaLeaseSet
8. Client uses tunnels from inner LeaseSet for communication
```
**Pro neoprávněné klienty:** - Nelze dešifrovat ani v případě, že najdou EncryptedLeaseSet - Nelze určit původní Destination (cílový identifikátor v I2P) z oslepené verze - Nelze propojit EncryptedLeaseSets napříč různými obdobími oslepování (denní rotace)

**Časy vypršení platnosti:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Content Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Maximum Expires</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet (outer)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">65,535 sec (≈18.2 hr)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Full 2-byte expires field</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Inner LeaseSet2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈660 sec (≈11 min)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Actual lease data practical maximum</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Inner MetaLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">65,535 sec (≈18.2 hr)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Indirection can be longer-lived</td></tr>
  </tbody>
</table>
**Časové razítko zveřejnění:**

Stejné požadavky jako u LeaseSet2Header (hlavička datové struktury LeaseSet2):
- Musí se mezi publikacemi zvýšit alespoň o 1 sekundu
- Floodfills (speciální uzly I2P pro netDb) odmítnou, pokud není novější než aktuální verze
- Doporučeno: 10-60 sekund mezi publikacemi

**Offline podpisy se šifrovanými LeaseSets:**

Zvláštní aspekty při používání offline podpisů: - Blinded public key (zaslepený veřejný klíč) se mění denně - Offline podpis je nutné denně znovu vytvořit s novým blinded key - NEBO použijte offline podpis na vnitřním LeaseSet, nikoli na vnějším EncryptedLeaseSet - Viz poznámky k [Proposal 123](/proposals/123-new-netdb-entries/)

**Poznámky k implementaci:**

1. **Autorizace klientů:**
   - Více klientů lze autorizovat pomocí různých klíčů
   - Každý autorizovaný klient má jedinečné údaje pro dešifrování
   - Klientovi lze odebrat přístup změnou autorizačních klíčů

2. **Denní rotace klíčů:**
   - Oslepené klíče se mění o půlnoci UTC
   - Klienti musí denně znovu vypočítat oslepenou Destination (cílová identita)
   - Staré EncryptedLeaseSets se po rotaci stanou nedohledatelnými

3. **Vlastnosti ochrany soukromí:**
   - Floodfills nemohou určit původní Destination (identifikátor cíle v I2P)
   - Neoprávnění klienti nemohou přistupovat ke službě
   - Různá období zaslepení nelze vzájemně propojit
   - Žádná nešifrovaná metadata kromě časů expirace

4. **Výkon:**
   - Klienti musí provádět denní výpočet zaslepení
   - Třívrstvé šifrování přidává výpočetní režii
   - Zvažte ukládání do mezipaměti dešifrovaného vnitřního LeaseSet

**Bezpečnostní hlediska:**

1. **Správa autorizačních klíčů:**
   - Zabezpečeně distribuujte autorizační pověření klientů
   - Používejte jedinečná pověření pro každého klienta pro možnost cíleného odvolání
   - Pravidelně obměňujte autorizační klíče

2. **Synchronizace hodin:**
   - Denní blinding (kryptografické zaslepení) závisí na synchronizovaných datech UTC
   - Odchylka hodin může způsobovat selhání vyhledávání
   - Zvažte podporu blindingu pro předchozí/následující den pro zvýšení tolerance

3. **Únik metadat:**
   - Pole Published a expires jsou v nešifrovaném textu
   - Analýza vzorců může odhalit charakteristiky služby
   - Znáhodněte intervaly publikace, pokud máte obavy

**JavaDoc:** [EncryptedLeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/EncryptedLeaseSet.html)

---

## Struktury routeru

### RouterAddress (adresa routeru)

**Popis:** Definuje informace o připojení k routeru prostřednictvím konkrétního transportního protokolu.

**Formát:**

```
+----+----+----+----+----+----+----+----+
|cost|           expiration
+----+----+----+----+----+----+----+----+
     |        transport_style           |
+----+----+----+----+-//-+----+----+----+
|                                       |
+                                       +
|               options                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

cost :: Integer (1 byte)
        Relative cost, 0=free, 255=expensive
        Typical values:
          5-6: SSU2
          10-11: NTCP2

expiration :: Date (8 bytes)
              MUST BE ALL ZEROS (see critical note below)

transport_style :: String (1-256 bytes)
                   Transport protocol name
                   Current values: "SSU2", "NTCP2"
                   Legacy: "SSU", "NTCP" (removed)

options :: Mapping
           Transport-specific configuration
           Common options: "host", "port"
           Transport-specific options vary
```
**KRITICKÉ - Pole expirace:**

⚠️ **Pole expiration MUSÍ být nastaveno na samé nuly (8 nulových bajtů).**

- **Důvod:** Od verze 0.9.3 způsobuje nenulová expirace selhání ověření podpisu
- **Historie:** Expirace se původně nepoužívala, vždy byla null
- **Aktuální stav:** Pole bylo od verze 0.9.12 opět rozpoznáno, ale je nutné počkat na upgrade sítě
- **Implementace:** Vždy nastaveno na 0x0000000000000000

Jakákoli nenulová expirace způsobí, že podpis RouterInfo neprojde ověřením.

### Transportní protokoly

**Aktuální protokoly (stav k verzi 2.10.0):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Introduced</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Removed</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>SSU2</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.54 (May 2022)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Default since 0.9.56</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>NTCP2</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.36 (Aug 2018)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.50 (May 2021)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Use NTCP2</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2.4.0 (Dec 2023)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Use SSU2</td></tr>
  </tbody>
</table>
**Hodnoty stylu transportu:** - `"SSU2"`: Aktuální transport založený na UDP - `"NTCP2"`: Aktuální transport založený na TCP - `"NTCP"`: Zastaralý, odstraněn (nepoužívat) - `"SSU"`: Zastaralý, odstraněn (nepoužívat)

### Obecné volby

Všechny transporty obvykle zahrnují:

```
"host" = IPv4 or IPv6 address or hostname
"port" = Port number (1-65535)
```
### Možnosti specifické pro SSU2

Viz [specifikaci SSU2](/docs/specs/ssu2/) pro úplné podrobnosti.

**Povinné volby:**

```
"host" = IP address (IPv4 or IPv6)
"port" = UDP port number
"s" = Static X25519 public key (Base64, 44 characters = 32 bytes)
"i" = Introduction key X25519 (Base64, 44 characters = 32 bytes)
"v" = "2" (protocol version)
```
**Volitelné možnosti:**

```
"caps" = Capability string (e.g., "B" for bandwidth tier)
"ihost0", "ihost1", ... = Introducer IP addresses
"iport0", "iport1", ... = Introducer ports  
"ikey0", "ikey1", ... = Introducer static keys (Base64, 44 chars)
"itag0", "itag1", ... = Introducer relay tags
"iexp0", "iexp1", ... = Introducer expiration timestamps
"mtu" = Maximum transmission unit (default 1500, min 1280)
"mtu6" = IPv6 MTU (if different from IPv4)
```
**Příklad SSU2 RouterAddress:**

```
cost: 5
expiration: 0x0000000000000000
transport_style: "SSU2"
options:
  host=198.51.100.42
  port=12345
  s=SGVsbG8gV29ybGQhIFRoaXMgaXMgYSBzYW1wbGUga2V5IQ==
  i=QW5vdGhlciBTYW1wbGUgS2V5IGZvciBJbnRyb2R1Y3Rpb24=
  v=2
  caps=BC
  mtu=1472
```
### Specifické volby pro NTCP2

Pro úplné podrobnosti viz [specifikaci NTCP2](/docs/specs/ntcp2/).

**Povinné volby:**

```
"host" = IP address (IPv4 or IPv6)
"port" = TCP port number
"s" = Static X25519 public key (Base64, 44 characters = 32 bytes)
"i" = Initialization vector (Base64, 24 characters = 16 bytes)
"v" = "2" (protocol version)
```
**Volitelné možnosti (od 0.9.50):**

```
"caps" = Capability string
```
**Příklad NTCP2 RouterAddress:**

```
cost: 10
expiration: 0x0000000000000000
transport_style: "NTCP2"
options:
  host=198.51.100.42
  port=23456
  s=SGVsbG8gV29ybGQhIFRoaXMgaXMgYSBzYW1wbGUga2V5IQ==
  i=U2FtcGxlIElWIGhlcmU=
  v=2
```
### Poznámky k implementaci

1. **Hodnoty nákladů:**
   - UDP (SSU2) má obvykle nižší náklady (5-6) díky efektivitě
   - TCP (NTCP2) má obvykle vyšší náklady (10-11) kvůli režii
   - Nižší náklady = preferovaný transport

2. **Více adres:**
   - Routers mohou zveřejňovat více záznamů RouterAddress
   - Různé transporty (SSU2 a NTCP2)
   - Různé verze IP (IPv4 a IPv6)
   - Klienti vybírají na základě cost (metrika nákladů) a schopností

3. **Název hostitele vs. IP:**
   - Pro výkon jsou preferovány IP adresy
   - Názvy hostitelů jsou podporovány, ale přidávají režii vyhledávání v DNS
   - Zvažte použití IP pro publikované RouterInfos

4. **Kódování Base64:**
   - Všechny klíče a binární data jsou kódovány v Base64
   - Standardní Base64 (RFC 4648)
   - Bez paddingu (vyplňování) ani nestandardních znaků

**JavaDoc:** [RouterAddress](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterAddress.html)

---

### RouterInfo (informace o routeru)

**Popis:** Kompletní zveřejněné informace o routeru, uložené v síťové databázi. Obsahuje identitu, adresy a schopnosti.

**Formát:**

```
+----+----+----+----+----+----+----+----+
| router_ident                          |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| published                             |
+----+----+----+----+----+----+----+----+
|size| RouterAddress 0                  |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| RouterAddress 1                       |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| RouterAddress ($size-1)               |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+-//-+----+----+----+
|psiz| options                          |
+----+----+----+----+-//-+----+----+----+
| signature                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

router_ident :: RouterIdentity
                Length: 387+ bytes (typically 391 for X25519+EdDSA)

published :: Date (8 bytes)
             Publication timestamp (milliseconds since epoch)

size :: Integer (1 byte)
        Number of RouterAddress entries
        Range: 0-255

addresses :: Array of RouterAddress
             Variable length
             Each RouterAddress has variable size

peer_size :: Integer (1 byte)
             Number of peer hashes (ALWAYS 0)
             Historical, unused feature

options :: Mapping
           Router capabilities and metadata
           MUST be sorted by key

signature :: Signature
             Length determined by router_ident signing key type
             Typically 64 bytes (EdDSA)
             Signed by router_ident's SigningPrivateKey
```
**Databázové úložiště:** - **Typ databáze:** 0 - **Klíč:** hash SHA-256 z RouterIdentity (identita routeru) - **Hodnota:** kompletní struktura RouterInfo (informace o routeru)

**Publikované časové razítko:** - 8bajtové datum (milisekundy od epochy) - Používá se pro verzování RouterInfo - Routery periodicky publikují nové RouterInfo - Floodfills uchovávají nejnovější verzi na základě publikovaného časového razítka

**Řazení adres:** - **Historické:** Velmi staré routers vyžadovaly, aby adresy byly seřazeny podle SHA-256 jejich dat - **Současné:** Řazení NENÍ vyžadováno, nestojí za implementaci kvůli kompatibilitě - Adresy mohou být v libovolném pořadí

**Pole velikosti peerů (historické):** - **Vždy 0** v moderním I2P - Bylo zamýšleno pro omezené trasy (neimplementováno) - Pokud by bylo implementováno, následovalo by ho právě tolik hashů routerů - Některé staré implementace mohly vyžadovat seřazený seznam peerů

**Mapování možností:**

Volby MUSÍ být seřazeny podle klíče. Mezi standardní volby patří:

**Nastavení schopností:**

```
"caps" = Capability string
         Common values:
           f = Floodfill (network database)
           L or M or N or O = Bandwidth tier (L=lowest, O=highest)
           R = Reachable
           U = Unreachable/firewalled
           Example: "fLRU" = Floodfill, Low bandwidth, Reachable, Unreachable
```
**Možnosti sítě:**

```
"netId" = Network ID (default "2" for main I2P network)
          Different values for test networks

"router.version" = I2P version string
                   Example: "0.9.67" or "2.10.0"
```
**Statistické možnosti:**

```
"stat_uptime" = Uptime in milliseconds
"coreVersion" = Core I2P version
"router.version" = Full router version string
```
Viz [dokumentaci k RouterInfo v síťové databázi](/docs/specs/common-structures/#routerInfo) pro úplný seznam standardních možností.

**Výpočet podpisu:**

```
Data to sign: Complete RouterInfo structure from router_ident through options

Verification:
1. Extract RouterIdentity from RouterInfo
2. Get SigningPublicKey from RouterIdentity (type determines algorithm)
3. Verify signature over all data preceding signature field
4. Signature must match signing key type and length
```
**Typický moderní RouterInfo:**

```
RouterIdentity: 391 bytes (X25519+EdDSA with Key Certificate)
Published: 8 bytes
Size: 1 byte (typically 1-4 addresses)
RouterAddress × N: Variable (typically 200-500 bytes each)
Peer Size: 1 byte (value=0)
Options: Variable (typically 50-200 bytes)
Signature: 64 bytes (EdDSA)

Total: ~1000-2500 bytes typical
```
**Poznámky k implementaci:**

1. **Více adres:**
   - Routers obvykle zveřejňují 1-4 adresy
   - Varianty IPv4 a IPv6
   - Transporty SSU2 a/nebo NTCP2
   - Každá adresa je nezávislá

2. **Verzování:**
   - Novější RouterInfo (záznam s informacemi o routeru v I2P) má pozdější časové razítko `published`
   - Každý router znovu publikuje každé ~2 hodiny nebo když se změní adresy
   - Floodfill uzly ukládají a šíří pouze nejnovější verzi

3. **Validace:**
   - Ověřte podpis před přijetím RouterInfo
   - Zkontrolujte, že pole expiration má samé nuly v každém RouterAddress
   - Ověřte, že mapování options je seřazeno podle klíče
   - Zkontrolujte, že typy certifikátu a klíče jsou známé a podporované

4. **Síťová databáze:**
   - Floodfills (speciální router v I2P pro netDb) ukládají RouterInfo indexované podle Hash(RouterIdentity)
   - Uloženo po dobu ~2 dnů od poslední publikace
   - Routers posílají dotazy na floodfills, aby našly další routers

**JavaDoc:** [RouterInfo](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterInfo.html)

---

## Poznámky k implementaci

### Pořadí bajtů (Endianness)

**Výchozí: Big-Endian (síťové pořadí bajtů)**

Většina struktur I2P používá pořadí bajtů big-endian: - Všechny celočíselné typy (1-8 bajtů) - Časová razítka Date - TunnelId - Prefix délky řetězce - Typy a délky certifikátů - Kódy typů klíčů - Pole velikosti mapování

**Výjimka: Little-Endian**

Následující typy klíčů používají kódování **little-endian** (nejméně významný bajt je první): - **X25519** šifrovací klíče (typ 4) - **EdDSA_SHA512_Ed25519** podpisové klíče (typ 7) - **EdDSA_SHA512_Ed25519ph** podpisové klíče (typ 8) - **RedDSA_SHA512_Ed25519** podpisové klíče (typ 11)

**Implementace:**

```java
// Big-endian (most structures)
int value = ((bytes[0] & 0xFF) << 24) | 
            ((bytes[1] & 0xFF) << 16) |
            ((bytes[2] & 0xFF) << 8) | 
            (bytes[3] & 0xFF);

// Little-endian (X25519, EdDSA, RedDSA)
int value = (bytes[0] & 0xFF) | 
            ((bytes[1] & 0xFF) << 8) |
            ((bytes[2] & 0xFF) << 16) | 
            ((bytes[3] & 0xFF) << 24);
```
### Verzování datových struktur

**Nikdy nepředpokládejte pevné velikosti:**

Řada struktur má proměnnou délku: - RouterIdentity (identita uzlu): 387+ bajtů (ne vždy 387) - Destination (cílová identita): 387+ bajtů (ne vždy 387) - LeaseSet2 (struktura LeaseSet verze 2): Výrazně se liší - Certifikát: 3+ bajtů

**Vždy čtěte velikostní pole:** - Délka certifikátu na bajtech 1-2 - Velikost mapování na začátku - KeysAndCert se vždy počítá jako 384 + 3 + certificate_length

**Zkontrolujte nadbytečná data:** - Zakázat nadbytečná koncová data za platnými strukturami - Ověřit, že délky certifikátů odpovídají typům klíčů - Vynutit přesně očekávané délky u typů s pevnou velikostí

### Aktuální doporučení (říjen 2025)

**Pro nové identity routeru:**

```
Encryption: X25519 (type 4, 32 bytes)
Signing: EdDSA_SHA512_Ed25519 (type 7, 32 bytes)
Certificate: Key Certificate (type 5)
Total Size: 391 bytes
Padding: Compressible per [Proposal 161](/cs/proposals/161-ri-dest-padding/)
```
**Pro nové destinace:**

```
Unused Public Key Field: 256 bytes random (compressible)
Signing: EdDSA_SHA512_Ed25519 (type 7, 32 bytes)
Certificate: Key Certificate (type 5)
Total Size: 391 bytes
Padding: Compressible per [Proposal 161](/cs/proposals/161-ri-dest-padding/)
```
**Pro nové LeaseSets:**

```
Type: LeaseSet2 (type 3)
Encryption Keys: X25519 (type 4, 32 bytes)
Leases: At least 1, typically 3-5
Options: Include service records per [Proposal 167](/proposals/167-service-records/)
Signature: EdDSA (64 bytes)
```
**Pro šifrované služby:**

```
Type: EncryptedLeaseSet (type 5)
Blinding: RedDSA_SHA512_Ed25519 (type 11)
Inner LeaseSet: LeaseSet2 (type 3)
Rotation: Daily blinding key rotation
Authorization: Per-client encryption keys
```
### Zastaralé funkce - nepoužívat

**Zastaralé šifrování:** - ElGamal (typ 0) pro identity Routeru (zastaralé od 0.9.58) - Šifrování ElGamal/AES+SessionTag (použijte ECIES-X25519)

**Zastaralé podepisování:** - DSA_SHA1 (typ 0) pro identity routeru (zastaralé od verze 0.9.58) - varianty ECDSA (typy 1-3) pro nové implementace - varianty RSA (typy 4-6) kromě souborů SU3

**Zastaralé síťové formáty:** - LeaseSet typ 1 (použijte LeaseSet2) - Lease (44 bytů, použijte Lease2) - Původní formát vypršení platnosti Lease

**Zastaralé transporty:** - NTCP (odstraněno ve verzi 0.9.50) - SSU (odstraněno ve verzi 2.4.0)

**Zastaralé certifikáty:** - HASHCASH (typ 1) - HIDDEN (typ 2) - SIGNED (typ 3) - MULTIPLE (typ 4)

### Bezpečnostní aspekty

**Generování klíčů:** - Vždy používejte kryptograficky bezpečné generátory náhodných čísel - Nikdy znovu nepoužívejte klíče napříč různými kontexty - Chraňte soukromé klíče pomocí vhodných mechanismů řízení přístupu - Po dokončení bezpečně vymažte klíčový materiál z paměti

**Ověření podpisu:** - Vždy ověřujte podpisy, než budete datům důvěřovat - Zkontrolujte, že délka podpisu odpovídá typu klíče - Ověřte, že podepsaná data obsahují očekávaná pole - U seřazených map ověřte řazení před podepsáním/ověřením

**Ověření časových razítek:** - Zkontrolujte, že publikované časy jsou rozumné (ne v příliš vzdálené budoucnosti) - Ověřte, že platnost lease (záznam v leaseSet) nevypršela - Zohledněte toleranci odchylky hodin (typicky ±30 sekund)

**Síťová databáze (netDb):** - Ověřte všechny struktury před uložením - Prosazujte limity velikosti, abyste zabránili DoS - Omezujte rychlost dotazů a publikací - Ověřte, že klíče databáze odpovídají hashům struktur

### Poznámky ke kompatibilitě

**Zpětná kompatibilita:** - ElGamal a DSA_SHA1 jsou stále podporovány pro starší routers - Zastaralé typy klíčů zůstávají funkční, ale jejich používání se nedoporučuje - Komprimovatelný padding (komprimovatelná vycpávka) ([Proposal 161](/cs/proposals/161-ri-dest-padding/)) zpětně kompatibilní až k verzi 0.6

**Dopředná kompatibilita:** - Neznámé typy klíčů lze parsovat pomocí délkových polí - Neznámé typy certifikátů lze přeskočit pomocí délky - Neznámé typy podpisů by měly být zpracovány korektně - Implementace by neměly selhávat kvůli neznámým volitelným funkcím

**Migrační strategie:** - Během přechodu podporovat jak staré, tak nové typy klíčů - LeaseSet2 (nová verze formátu LeaseSet) může uvádět více šifrovacích klíčů - Offline podpisy umožňují bezpečnou rotaci klíčů - MetaLeaseSet (metazáznam LeaseSet pro migraci služeb) umožňuje transparentní migraci služby

### Testování a validace

**Validace struktury:** - Ověřte, že všechna délková pole jsou v očekávaných rozsazích - Zkontrolujte, že struktury s proměnnou délkou se správně parsují - Ověřte, že ověření podpisů proběhne úspěšně - Testujte se strukturami minimální i maximální velikosti

**Okrajové případy:** - Řetězce nulové délky - Prázdná mapování - Minimální a maximální počty lease (záznamů v leaseSetu) - Certifikát s nulovou délkou užitečných dat - Velmi velké struktury (blízko maximální velikosti)

**Interoperabilita:** - Testovat proti oficiální implementaci I2P v Javě - Ověřit kompatibilitu s i2pd - Testovat s různým obsahem síťové databáze - Validovat vůči ověřeným referenčním testovacím vektorům

---

## Reference

### Specifikace

- [Protokol I2NP](/docs/specs/i2np/)
- [Protokol I2CP](/docs/specs/i2cp/)
- [Transport SSU2](/docs/specs/ssu2/)
- [Transport NTCP2](/docs/specs/ntcp2/)
- [Protokol Tunnel](/docs/specs/implementation/)
- [Datagramový protokol](/docs/api/datagrams/)

### Kryptografie

- [Přehled kryptografie](/docs/specs/cryptography/)
- [Šifrování ElGamal/AES](/docs/legacy/elgamal-aes/)
- [Šifrování ECIES-X25519](/docs/specs/ecies/)
- [ECIES pro Routers](/docs/specs/ecies/#routers)
- [Hybridní ECIES (postkvantový)](/docs/specs/ecies/#hybrid)
- [Podpisy Red25519](/docs/specs/red25519-signature-scheme/)
- [Šifrovaný LeaseSet](/docs/specs/encryptedleaseset/)

### Návrhy

- [Návrh 123: Nové záznamy v netDB](/proposals/123-new-netdb-entries/)
- [Návrh 134: Typy podpisů GOST](/proposals/134-gost/)
- [Návrh 136: Experimentální typy podpisů](/proposals/136-experimental-sigtypes/)
- [Návrh 145: ECIES-P256](/proposals/145-ecies/)
- [Návrh 156: ECIES routery](/proposals/156-ecies-routers/)
- [Návrh 161: Generování vycpávky](/cs/proposals/161-ri-dest-padding/)
- [Návrh 167: Záznamy služeb](/proposals/167-service-records/)
- [Návrh 169: Postkvantová kryptografie](/proposals/169-pq-crypto/)
- [Rejstřík všech návrhů](/proposals/)

### Síťová databáze

- [Přehled síťové databáze](/docs/specs/common-structures/)
- [Standardní možnosti RouterInfo](/docs/specs/common-structures/#routerInfo)

### Referenční dokumentace API JavaDoc

- [Balíček základních dat](http://docs.i2p-projekt.de/javadoc/net/i2p/data/)
- [PublicKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/PublicKey.html)
- [PrivateKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/PrivateKey.html)
- [SessionKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SessionKey.html)
- [SigningPublicKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SigningPublicKey.html)
- [SigningPrivateKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SigningPrivateKey.html)
- [Signature](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Signature.html)
- [Hash](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Hash.html)
- [SessionTag](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SessionTag.html)
- [TunnelId](http://docs.i2p-projekt.de/javadoc/net/i2p/data/TunnelId.html)
- [Certificate](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Certificate.html)
- [DataHelper](http://docs.i2p-projekt.de/javadoc/net/i2p/data/DataHelper.html)
- [KeysAndCert](http://docs.i2p-projekt.de/javadoc/net/i2p/data/KeysAndCert.html)
- [RouterIdentity](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterIdentity.html)
- [Destination](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Destination.html)
- [Lease](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Lease.html)
- [LeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/LeaseSet.html)
- [Lease2](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Lease2.html)
- [LeaseSet2](http://docs.i2p-projekt.de/javadoc/net/i2p/data/LeaseSet2.html)
- [MetaLease](http://docs.i2p-projekt.de/javadoc/net/i2p/data/MetaLease.html)
- [MetaLeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/MetaLeaseSet.html)
- [EncryptedLeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/EncryptedLeaseSet.html)
- [RouterAddress](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterAddress.html)
- [RouterInfo](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterInfo.html)

### Externí standardy

- **RFC 7748 (X25519):** Eliptické křivky pro zabezpečení
- **RFC 7539 (ChaCha20):** ChaCha20 a Poly1305 pro protokoly IETF
- **RFC 4648 (Base64):** Kódování dat Base16, Base32 a Base64
- **FIPS 180-4 (SHA-256):** Bezpečnostní hašovací standard
- **FIPS 204 (ML-DSA):** Module-Lattice-Based Digital Signature Standard (standard digitálních podpisů založený na mřížkové kryptografii s moduly)
- [Registr služeb IANA](http://www.dns-sd.org/ServiceTypes.html)

### Zdroje komunity

- [Webové stránky I2P](/)
- [Fórum I2P](https://i2pforum.net)
- [I2P GitLab](https://i2pgit.org/I2P_Developers/i2p.i2p)
- [Zrcadlo I2P na GitHubu](https://github.com/i2p/i2p.i2p)
- [Index technické dokumentace](/docs/)

### Informace o vydání

- [Vydání I2P 2.10.0](/cs/blog/2025/09/08/i2p-2.10.0-release/)
- [Historie vydání](https://github.com/i2p/i2p.i2p/blob/master/history.txt)
- [Seznam změn](https://github.com/i2p/i2p.i2p/blob/master/debian/changelog)

---

## Příloha: Stručné referenční tabulky

### Rychlý přehled typů klíčů

**Aktuální standard (doporučený pro všechny nové implementace):** - **Šifrování:** X25519 (typ 4, 32 bajtů, little-endian) - **Podepisování:** EdDSA_SHA512_Ed25519 (typ 7, 32 bajtů, little-endian)

**Starší (podporováno, ale zastaralé):** - **Šifrování:** ElGamal (typ 0, 256 bajtů, big-endian (nejvýznamnější bajt první)) - **Podepisování:** DSA_SHA1 (typ 0, 20bajtový soukromý / 128bajtový veřejný, big-endian)

**Specializované:** - **Podpis (šifrovaný LeaseSet):** RedDSA_SHA512_Ed25519 (typ 11, 32 bajtů, little-endian)

**Postkvantové (beta, zatím nefinalizované):** - **Hybridní šifrování:** varianty MLKEM_X25519 (typy 5-7) - **Čistě postkvantové šifrování:** varianty MLKEM (zatím nemají přiřazené kódy typů)

### Rychlý přehled velikostí struktur

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Structure</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Minimum Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Typical Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Maximum Size</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Integer</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Date</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">String</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">256 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SessionKey</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Hash</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelId</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Certificate</td><td style="border:1px solid var(--color-border); padding:0.5rem;">3 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">7 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">65,538 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">KeysAndCert</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">391 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterIdentity</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">391 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Destination</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">391 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Lease</td><td style="border:1px solid var(--color-border); padding:0.5rem;">44 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">44 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">44 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Lease2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1200 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈2000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈500 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈800 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈2000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈600 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈3000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterAddress</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈150 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈300 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈600 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1500 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈3000+ bytes</td></tr>
  </tbody>
</table>
### Rychlý přehled typů databází

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Structure</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Stored under Hash(RouterIdentity)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Use LeaseSet2 instead</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Stored under Hash(Destination)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Stored under Hash(Blinded Destination)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">MetaLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Defined</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Verify production status</td></tr>
  </tbody>
</table>
### Rychlá referenční příručka k transportním protokolům

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Port Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">UDP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.54</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Default since 0.9.56</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TCP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.36</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">UDP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1pxsolid var(--color-border); padding:0.5rem;">Removed in 2.4.0</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TCP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed in 0.9.50</td></tr>
  </tbody>
</table>
### Rychlý přehled verzí a milníků

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">API</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Date</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Changes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.6.x</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2005</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destination encryption disabled</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Dec 2013</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Key Certificates introduced</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Sep 2015</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA support added</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.16</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.16</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Nov 2015</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Router Key Certificates</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.36</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.36</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Aug 2018</td><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP2 introduced</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Nov 2018</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2, X25519 for Destinations</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Dec 2018</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet working</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.48</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.48</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Jul 2020</td><td style="border:1px solid var(--color-border); padding:0.5rem;">X25519 for Router Identities</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.50</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.50</td><td style="border:1px solid var(--color-border); padding:0.5rem;">May 2021</td><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP removed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.54</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.54</td><td style="border:1px solid var(--color-border); padding:0.5rem;">May 2022</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 testing</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.57</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.57</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Jan 2023</td><td style="border:1px solid var(--color-border); padding:0.5rem;">[Proposal 161](/cs/proposals/161-ri-dest-padding/) padding (release 2.1.0)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.58</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.58</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mar 2023</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal/DSA deprecated for RIs (2.2.0)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.66</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.66</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Jun 2025</td><td style="border:1px solid var(--color-border); padding:0.5rem;">[Proposal 167](/proposals/167-service-records/) service records (2.9.0)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Sep 2025</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ML-KEM beta support (2.10.0)</td></tr>
  </tbody>
</table>
---
