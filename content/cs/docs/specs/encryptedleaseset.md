---
title: "Šifrovaný LeaseSet"
description: "Formát LeaseSet s řízeným přístupem pro soukromé Destinations (cíle)"
slug: "encryptedleaseset"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Přehled

Tento dokument specifikuje zaslepení, šifrování a dešifrování šifrovaného LeaseSet2 (LS2). Šifrované LeaseSets umožňují publikování informací o skrytých službách v síťové databázi I2P s řízeným přístupem.

**Klíčové vlastnosti:** - Denní rotace klíčů pro dopředné utajení - Dvoustupňová autorizace klientů (na bázi DH a na bázi PSK) - Šifrování ChaCha20 pro vyšší výkon na zařízeních bez hardwarové podpory AES - Podpisy Red25519 se zaslepením klíče - Členství klientů s ochranou soukromí

**Související dokumentace:** - [Specifikace společných struktur](/docs/specs/common-structures/) - Struktura šifrovaného LeaseSet - [Návrh 123: Nové položky v netDB](/proposals/123-new-netdb-entries/) - Pozadí k šifrovaným LeaseSet - [Dokumentace k databázi sítě](/docs/specs/common-structures/) - Použití NetDB

---

## Historie verzí a stav implementace

### Časová osa vývoje protokolu

**Důležitá poznámka k číslování verzí:**   I2P používá dvě oddělená schémata číslování verzí: - **Verze API/Router:** řada 0.9.x (používaná v technických specifikacích) - **Verze produktového vydání:** řada 2.x.x (používaná pro veřejná vydání)

Technické specifikace odkazují na verze API (např. 0.9.41), zatímco koncoví uživatelé vidí produktové verze (např. 2.10.0).

### Milníky implementace

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Release Date</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Features</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.38</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">January 2019</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Floodfill support for standard LS2, offline keys</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.39</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">March 2019</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Full encrypted LS2 support, Red25519 (sig type&nbsp;11)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.40</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">May 2019</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Per-client authorization, encrypted LS2 with offline keys, B32 support</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.41</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">June 2019</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Protocol finalized as stable</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>2.10.0</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">September 2025</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Latest Java implementation (API version 0.9.61)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>i2pd 2.58.0</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">September 2025</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Full C++ implementation compatibility</td></tr>
  </tbody>
</table>
### Aktuální stav

- ✅ **Stav protokolu:** Stabilní a beze změny od června 2019
- ✅ **Java I2P:** Plně implementováno ve verzi 0.9.40+
- ✅ **i2pd (C++):** Plně implementováno ve verzi 2.58.0+
- ✅ **Interoperabilita:** Plná napříč implementacemi
- ✅ **Síťové nasazení:** Připraveno pro produkční nasazení s více než 6 lety provozních zkušeností

---

## Kryptografické definice

### Notace a konvence

- `||` označuje zřetězení
- `mod L` označuje modulární redukci podle řádu Ed25519
- Všechna pole bajtů jsou v síťovém pořadí bajtů (big-endian, nejvýznamnější bajt první), není-li uvedeno jinak
- Hodnoty v little-endian (nejméně významný bajt první) jsou výslovně označeny

### CSRNG(n)

**Kryptograficky bezpečný generátor náhodných čísel**

Vytvoří `n` bajtů kryptograficky bezpečných náhodných dat vhodných pro generování klíčového materiálu.

**Požadavky na zabezpečení:** - Musí být kryptograficky bezpečné (vhodné pro generování klíčů) - Musí být bezpečné i v případě, že jsou na síti vystaveny sousední bajtové sekvence - Implementace by měly hashovat výstup z potenciálně nedůvěryhodných zdrojů

**Odkazy:** - [Bezpečnostní úvahy ohledně PRNG](http://projectbullrun.org/dual-ec/ext-rand.html) - [Diskuse vývojářů projektu Tor](https://lists.torproject.org/pipermail/tor-dev/2015-November/009954.html)

### H(p, d)

**SHA-256 hash s personalizací**

Doménově oddělená hashovací funkce, která přijímá: - `p`: Personalizační řetězec (zajišťuje oddělení domén) - `d`: Data k hashování

**Implementace:**

```
H(p, d) := SHA-256(p || d)
```
**Použití:** Poskytuje kryptografické oddělení domén, aby se zabránilo kolizním útokům mezi různými protokolovými použitími SHA-256.

### PROUDOVÁ ŠIFRA: ChaCha20

**Proudová šifra: ChaCha20 podle RFC 7539, sekce 2.4**

**Parametry:** - `S_KEY_LEN = 32` (256bitový klíč) - `S_IV_LEN = 12` (96bitová nonce — jednorázová hodnota) - Počáteční čítač: `1` (RFC 7539 povoluje 0 nebo 1; 1 se doporučuje v kontextech AEAD)

**ENCRYPT(k, iv, plaintext)**

Šifruje otevřený text pomocí: - `k`: 32bajtový šifrovací klíč - `iv`: 12bajtová nonce (jednorázová hodnota; MUSÍ být jedinečná pro každý klíč) - Vrací šifrotext stejné délky jako otevřený text

**Bezpečnostní vlastnost:** Celý šifrotext musí být nerozlišitelný od náhodných dat, pokud je klíč tajný.

**DECRYPT(k, iv, ciphertext)**

Dešifruje šifrotext pomocí: - `k`: 32bajtový šifrovací klíč - `iv`: 12bajtový nonce (jednorázová hodnota) - Vrací prostý text

**Odůvodnění návrhu:** ChaCha20 byl upřednostněn před AES, protože: - 2,5–3× rychlejší než AES na zařízeních bez hardwarové akcelerace - Implementaci s konstantním časem je snazší dosáhnout - Srovnatelná bezpečnost a rychlost, když je k dispozici AES-NI

**Odkazy:** - [RFC 7539](https://datatracker.ietf.org/doc/html/rfc7539) - ChaCha20 a Poly1305 pro protokoly IETF

### Podpis: Red25519

**Schéma podpisu: Red25519 (SigType 11) se zaslepením klíče**

Red25519 je založena na podpisech Ed25519 nad křivkou Ed25519, při hašování používá SHA-512 a podporuje key blinding (zaslepení klíče), jak je specifikováno v ZCash RedDSA.

**Funkce:**

#### DERIVE_PUBLIC(privkey)

Vrátí veřejný klíč odpovídající zadanému soukromému klíči. - Používá standardní skalární násobení Ed25519 podle základního bodu (generátoru)

#### SIGN(privkey, m)

Vrátí podpis zprávy `m` soukromým klíčem `privkey`.

**Rozdíly Red25519 při podepisování oproti Ed25519:** 1. **Náhodná Nonce (jednorázová hodnota):** Používá 80 bajtů dodatečných náhodných dat

   ```
   T = CSRNG(80)  // 80 random bytes
   r = H*(T || publickey || message)
   ```
Díky tomu je každý podpis Red25519 jedinečný, i pro stejnou zprávu a stejný klíč.

2. **Generování soukromého klíče:** Soukromé klíče Red25519 se generují z náhodných čísel a redukují se `mod L`, nikoli pomocí přístupu Ed25519 zvaného bit-clamping (ořezání bitů).

#### VERIFY(pubkey, m, sig)

Ověří podpis `sig` vůči veřejnému klíči `pubkey` a zprávě `m`. - Vrátí `true`, pokud je podpis platný, jinak `false` - Ověření je totožné s Ed25519

**Operace zaslepení klíče:**

#### GENERATE_ALPHA(data, secret)

Generuje hodnotu alfa pro zaslepení klíče. - `data`: Obvykle obsahuje veřejný klíč pro podepisování a typy podpisů - `secret`: Volitelný dodatečný tajný údaj (pokud se nepoužije, má nulovou délku) - Výsledek má totožné rozdělení jako soukromé klíče Ed25519 (po redukci mod L)

#### BLIND_PRIVKEY(privkey, alpha)

Zaslepuje soukromý klíč pomocí tajné hodnoty `alpha`. - Implementace: `blinded_privkey = (privkey + alpha) mod L` - Používá skalární aritmetiku v tělese

#### BLIND_PUBKEY(pubkey, alpha)

Zaslepí veřejný klíč pomocí tajné hodnoty `alpha`. - Implementace: `blinded_pubkey = pubkey + DERIVE_PUBLIC(alpha)` - Používá sčítání prvků skupiny (bodů) na křivce

**Kritická vlastnost:**

```
BLIND_PUBKEY(pubkey, alpha) == DERIVE_PUBLIC(BLIND_PRIVKEY(privkey, alpha))
```
**Bezpečnostní hlediska:**

Ze specifikace protokolu ZCash, oddíl 5.4.6.1: Z hlediska bezpečnosti musí mít alpha stejnou distribuci jako unblinded (odzaslepené) soukromé klíče. To zajišťuje, že "kombinace re-randomized (znovunáhodněného) veřejného klíče a podpisu/podpisů pod tímto klíčem neodhaluje klíč, z něhož byl re-randomizován."

**Podporované typy podpisů:** - **Typ 7 (Ed25519):** Podporován pro existující destinace (zpětná kompatibilita) - **Typ 11 (Red25519):** Doporučen pro nové destinace využívající šifrování - **Zaslepené klíče:** Vždy používejte typ 11 (Red25519)

**Reference:** - [Specifikace protokolu Zcash](https://zips.z.cash/protocol/protocol.pdf) - Sekce 5.4.6 RedDSA - [Specifikace I2P Red25519](/docs/specs/red25519-signature-scheme/)

### DH: X25519

**Diffie–Hellman nad eliptickými křivkami: X25519**

Veřejnoklíčový systém pro dohodu klíče založený na Curve25519 (eliptická křivka 25519).

**Parametry:** - Soukromé klíče: 32 bajtů - Veřejné klíče: 32 bajtů - Výstup sdíleného tajemství: 32 bajtů

**Funkce:**

#### GENERATE_PRIVATE()

Vygeneruje nový 32bajtový soukromý klíč pomocí CSRNG (kryptograficky bezpečného generátoru náhodných čísel).

#### DERIVE_PUBLIC(privkey)

Odvodí 32bajtový veřejný klíč ze zadaného soukromého klíče. - Používá skalární násobení na eliptické křivce Curve25519

#### DH(privkey, pubkey)

Provádí Diffie-Hellmanovu dohodu o klíči. - `privkey`: Místní soukromý klíč o délce 32 bajtů - `pubkey`: Vzdálený veřejný klíč o délce 32 bajtů - Vrací: sdílené tajemství o délce 32 bajtů

**Bezpečnostní vlastnosti:** - Výpočetní předpoklad Diffie–Hellman na křivce Curve25519 - Dopředné utajení při použití efemérních klíčů - Implementace s konstantním časem je nezbytná k zabránění časovým útokům

**Reference:** - [RFC 7748](https://datatracker.ietf.org/doc/html/rfc7748) - Eliptické křivky pro zabezpečení

### HKDF (funkce pro odvozování klíčů založená na HMAC)

**Funkce pro odvozování klíčů založená na HMAC**

Extrahuje a rozšiřuje klíčový materiál ze vstupního klíčového materiálu.

**Parametry:** - `salt`: maximálně 32 bajtů (typicky 32 bajtů pro SHA-256) - `ikm`: vstupní klíčový materiál (libovolná délka, měl by mít vysokou entropii) - `info`: kontextově specifické informace (separace domén) - `n`: délka výstupu v bajtech

**Implementace:**

Používá HKDF (funkce derivace klíčů založená na HMAC) podle RFC 5869 s: - **Hašovací funkce:** SHA-256 - **HMAC:** Jak je uvedeno v RFC 2104 - **Délka saltu:** Maximálně 32 bajtů (HashLen pro SHA-256)

**Vzor použití:**

```
keys = HKDF(salt, ikm, info, n)
```
**Oddělení domén:** Parametr `info` zajišťuje kryptografické oddělení domén mezi různými použitími HKDF v protokolu.

**Ověřené hodnoty Info:** - `"ELS2_L1K"` - Šifrování 1. vrstvy (vnější) - `"ELS2_L2K"` - Šifrování 2. vrstvy (vnitřní) - `"ELS2_XCA"` - Autorizace klienta DH - `"ELS2PSKA"` - Autorizace klienta PSK - `"i2pblinding1"` - Generování alfy

**Odkazy:** - [RFC 5869](https://datatracker.ietf.org/doc/html/rfc5869) - Specifikace HKDF - [RFC 2104](https://datatracker.ietf.org/doc/html/rfc2104) - Specifikace HMAC

---

## Specifikace formátu

Šifrovaný LS2 (druhá generace leaseSet) se skládá ze tří vnořených vrstev:

1. **Vrstva 0 (vnější):** Informace v prostém textu pro ukládání a načítání
2. **Vrstva 1 (střední):** Data pro ověření klienta (šifrovaná)
3. **Vrstva 2 (vnitřní):** Vlastní data LeaseSet2 (I2P struktura s informacemi o dosažitelnosti služby) (šifrovaná)

**Celková struktura:**

```
Layer 0 data + Enc(layer 1 data + Enc(layer 2 data)) + Signature
```
**Důležité:** Šifrovaný LS2 (LeaseSet verze 2) používá zaslepené klíče. Destination (cílová identita v I2P) není v hlavičce. Místo uložení v DHT je `SHA-256(sig type || blinded public key)`, mění se každý den.

### Vrstva 0 (vnější) - prostý text

Vrstva 0 NEPOUŽÍVÁ standardní hlavičku LS2. Má vlastní formát optimalizovaný pro blinded keys (zaslepené klíče).

**Struktura:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Type</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Not in header, from DatabaseStore message field</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded Public Key Sig Type</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, always <code>0x000b</code> (Red25519 type 11)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded Public Key</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Red25519 blinded public key</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Published Timestamp</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, seconds since epoch (rolls over in 2106)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Expires</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, offset from published in seconds (max 65,535 &asymp; 18.2 hours)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Flags</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Bit flags (see below)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">[Optional] Transient Key Data</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Present if flag bit&nbsp;0 is set</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">lenOuterCiphertext</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, length of outer ciphertext</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">outerCiphertext</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">lenOuterCiphertext</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted Layer&nbsp;1 data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Red25519 signature over all preceding data</td></tr>
  </tbody>
</table>
**Pole příznaků (2 bajty, bity 15-0):** - **Bit 0:** Indikátor offline klíčů   - `0` = Žádné offline klíče   - `1` = Offline klíče jsou přítomny (následují dočasná data klíče) - **Bity 1-15:** Rezervováno, musí být 0 pro budoucí kompatibilitu

**Dočasná klíčová data (přítomná, pokud je bit příznaku 0 = 1):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Expires Timestamp</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, seconds since epoch</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Transient Sig Type</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, signature type</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Transient Signing Public Key</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Length implied by signature type</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signed by blinded public key; covers expires timestamp, transient sig type, and transient public key</td></tr>
  </tbody>
</table>
**Ověření podpisu:** - **Bez offline klíčů:** Ověřte pomocí zaslepeného veřejného klíče - **S offline klíči:** Ověřte pomocí dočasného veřejného klíče

Podpis se vztahuje na veškerá data od Type až po outerCiphertext (včetně).

### Vrstva 1 (střední) - Autorizace klienta

**Dešifrování:** Viz sekci [Layer 1 Encryption](#layer-1-encryption).

**Struktura:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Flags</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Authorization flags (see below)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">[Optional] Auth Data</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Present based on flags</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">innerCiphertext</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted Layer&nbsp;2 data (remainder)</td></tr>
  </tbody>
</table>
**Pole příznaků (1 bajt, bity 7-0):** - **Bit 0:** Režim autorizace   - `0` = Žádná autorizace pro jednotlivé klienty (kdokoli)   - `1` = Autorizace pro jednotlivé klienty (následuje sekce autorizace) - **Bity 3-1:** Schéma autentizace (pouze pokud bit 0 = 1)   - `000` = Autentizace klienta DH   - `001` = Autentizace klienta PSK   - Ostatní hodnoty jsou vyhrazeny - **Bity 7-4:** Nepoužito, musí být 0

**DH autorizační data klienta (příznaky = 0x01, bity 3-1 = 000):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ephemeralPublicKey</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Server's ephemeral X25519 public key</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">clients</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, number of client entries</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">authClient[]</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">40 bytes each</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Array of client authorization entries</td></tr>
  </tbody>
</table>
**Záznam authClient (40 bajtů):** - `clientID_i`: 8 bajtů - `clientCookie_i`: 32 bajtů (šifrovaný authCookie)

**Autorizační údaje klienta PSK (příznaky = 0x03, bity 3-1 = 001):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">authSalt</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Salt for PSK key derivation</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">clients</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, number of client entries</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">authClient[]</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">40 bytes each</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Array of client authorization entries</td></tr>
  </tbody>
</table>
**Záznam authClient (40 bajtů):** - `clientID_i`: 8 bajtů - `clientCookie_i`: 32 bajtů (šifrovaný authCookie)

### Vrstva 2 (vnitřní) - LeaseSet Data

**Dešifrování:** Viz část [Šifrování vrstvy 2](#layer-2-encryption).

**Struktura:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Type</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>3</code> (LS2) or <code>7</code> (Meta LS2)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Complete LeaseSet2 or MetaLeaseSet2</td></tr>
  </tbody>
</table>
Vnitřní vrstva obsahuje úplnou strukturu LeaseSet2 včetně: - záhlaví LS2 - informace o Lease (záznam o příchozím tunnelu s dobou platnosti) - podpis LS2

**Požadavky na ověření:** Po dešifrování musí implementace ověřit: 1. Vnitřní časové razítko se shoduje s vnějším publikovaným časovým razítkem 2. Vnitřní doba platnosti se shoduje s vnější dobou platnosti 3. Podpis LS2 (LeaseSet2, novější formát leaseSet) je platný 4. Data lease jsou syntakticky správná

**Odkazy:** - [Specifikace obecných struktur](/docs/specs/common-structures/) - Podrobnosti formátu LeaseSet2

---

## Odvození zaslepujícího klíče

### Přehled

I2P používá aditivní schéma zaslepování klíčů založené na Ed25519 a ZCash RedDSA. Zaslepené klíče se kvůli dopřednému utajení denně obměňují (o půlnoci UTC).

**Odůvodnění návrhu:**

I2P se výslovně rozhodl nepoužít přístup popsaný v dokumentu projektu Tor rend-spec-v3.txt, příloha A.2. Podle specifikace:

> "Nepoužíváme přílohu A.2 dokumentu projektu Tor rend-spec-v3.txt, která má podobné cíle návrhu, protože její zaslepené veřejné klíče mohou být mimo podskupinu s prvočíselným řádem, což má neznámé bezpečnostní důsledky."

Aditivní zaslepení v I2P zaručuje, že zaslepené klíče zůstávají v podskupině o prvočíselném řádu křivky Ed25519.

### Matematické definice

**Parametry Ed25519:** - `B`: základní bod Ed25519 (generátor) = `2^255 - 19` - `L`: řád Ed25519 = `2^252 + 27742317777372353535851937790883648493`

**Klíčové proměnné:** - `A`: Nezaslepený 32bajtový veřejný podpisový klíč (v Destination — identifikátoru cíle v I2P) - `a`: Nezaslepený 32bajtový soukromý podpisový klíč - `A'`: Zaslepený 32bajtový veřejný podpisový klíč (použit v šifrovaném LeaseSet) - `a'`: Zaslepený 32bajtový soukromý podpisový klíč - `alpha`: 32bajtový faktor zaslepení (tajný)

**Pomocné funkce:**

#### LEOS2IP(x)

"Převod řetězce oktetů v Little-Endian (pořadí bajtů, kde nejméně významný bajt je první) na celé číslo"

Převede pole bajtů v pořadí little-endian na celočíselnou reprezentaci.

#### H*(x)

"Hašování a redukce"

```
H*(x) = (LEOS2IP(SHA512(x))) mod L
```
Stejná operace jako při generování klíče Ed25519 (algoritmus eliptické křivky).

### Generace Alfa

**Denní rotace:** Každý den o půlnoci UTC (00:00:00 UTC) MUSÍ být vygenerovány nové alpha (parametr „alpha“) a blinded keys (zaslepené klíče).

**GENERATE_ALPHA(destination, date, secret) Algoritmus:**

```python
# Input parameters
A = destination's signing public key (32 bytes)
stA = signature type of A (2 bytes, big endian)
     # 0x0007 for Ed25519 or 0x000b for Red25519
stA' = signature type of blinded key A' (2 bytes, big endian) 
     # Always 0x000b (Red25519)
datestring = "YYYYMMDD" (8 bytes ASCII from current UTC date)
secret = optional UTF-8 encoded string (zero-length if not used)

# Computation
keydata = A || stA || stA'  # 36 bytes total
seed = HKDF(
    salt=H("I2PGenerateAlpha", keydata),
    ikm=datestring || secret,
    info="i2pblinding1",
    n=64
)

# Treat seed as 64-byte little-endian integer and reduce
alpha = seed mod L
```
**Ověřené parametry:** - Personalizace soli: `"I2PGenerateAlpha"` - HKDF info: `"i2pblinding1"` - Výstup: 64 bajtů před redukcí - Rozdělení Alpha: má stejné rozdělení jako soukromé klíče Ed25519 po `mod L`

### Zaslepení soukromého klíče

**Algoritmus BLIND_PRIVKEY(a, alpha):**

Pro vlastníka Destination (cílová adresa), který publikuje šifrovaný LeaseSet:

```python
# For Ed25519 private key (type 7)
if sigtype == 7:
    seed = destination's signing private key (32 bytes)
    a = left_half(SHA512(seed))  # 32 bytes
    a = clamp(a)  # Ed25519 clamping
    
# For Red25519 private key (type 11)
elif sigtype == 11:
    a = destination's signing private key (32 bytes)
    # No clamping for Red25519

# Additive blinding using scalar arithmetic
blinded_privkey = a' = (a + alpha) mod L

# Derive blinded public key
blinded_pubkey = A' = DERIVE_PUBLIC(a')
```
**Kritické:** Redukce `mod L` je nezbytná pro zachování správného algebraického vztahu mezi soukromými a veřejnými klíči.

### Zaslepení veřejného klíče

**Algoritmus BLIND_PUBKEY(A, alpha):**

Pro klienty, kteří načítají a ověřují šifrovaný LeaseSet:

```python
alpha = GENERATE_ALPHA(destination, date, secret)
A = destination's signing public key (32 bytes)

# Additive blinding using group elements (curve points)
blinded_pubkey = A' = A + DERIVE_PUBLIC(alpha)
```
**Matematická ekvivalence:**

Obě metody vedou ke shodným výsledkům:

```
BLIND_PUBKEY(A, alpha) == DERIVE_PUBLIC(BLIND_PRIVKEY(a, alpha))
```
Je to proto, že:

```
A' = A + [alpha]B
   = [a]B + [alpha]B
   = [a + alpha]B  (group operation)
   = DERIVE_PUBLIC(a + alpha mod L)
```
### Podepisování pomocí zaslepených klíčů

**Podepisování nezaslepeného LeaseSet:**

Nezaslepený LeaseSet (odesílán přímo ověřeným klientům) je podepsán pomocí: - standardního podpisu Ed25519 (type 7) nebo Red25519 (type 11) - nezaslepeného soukromého klíče pro podepisování - ověřován nezaslepeným veřejným klíčem

**S offline klíči:** - Podepsáno nezaslepeným dočasným soukromým klíčem - Ověřeno pomocí nezaslepeného dočasného veřejného klíče - Oba musí být typu 7 nebo 11

**Podepisování šifrovaného LeaseSetu:**

Vnější část šifrovaného LeaseSetu používá podpisy Red25519 se zaslepenými klíči.

**Podpisový algoritmus Red25519:**

```python
# Generate per-signature random nonce
T = CSRNG(80)  # 80 random bytes

# Calculate r (differs from Ed25519)
r = H*(T || blinded_pubkey || message)

# Rest is same as Ed25519
R = [r]B
S = (r + H(R || A' || message) * a') mod L
signature = R || S  # 64 bytes total
```
**Klíčové rozdíly oproti Ed25519:** 1. Používá 80 bajtů náhodných dat `T` (nikoli hash soukromého klíče) 2. Používá přímo hodnotu veřejného klíče (nikoli hash soukromého klíče) 3. Každý podpis je jedinečný i pro stejnou zprávu a klíč

**Ověření:**

Stejné jako u Ed25519 (schéma digitálního podpisu):

```python
# Parse signature
R = signature[0:32]
S = signature[32:64]

# Verify equation: [S]B = R + [H(R || A' || message)]A'
return [S]B == R + [H(R || A' || message)]A'
```
### Bezpečnostní hlediska

**Alfa distribuce:**

Z bezpečnostních důvodů musí mít alpha shodné rozdělení jako nezaslepené soukromé klíče. Při zaslepení Ed25519 (typ 7) (schéma digitálního podpisu) na Red25519 (typ 11) (varianta schématu založená na Ed25519) se rozdělení mírně liší.

**Doporučení:** Použijte Red25519 (type 11) pro nezaslepené i zaslepené klíče pro splnění požadavků ZCash: "kombinace re-randomized (znovu náhodně změněného) veřejného klíče a podpisů vytvořených tímto klíčem neodhaluje klíč, ze kterého byl re-randomized."

**Podpora typu 7:** Ed25519 je podporován pro zachování zpětné kompatibility se stávajícími destinacemi, ale pro nové šifrované destinace je doporučen typ 11.

**Výhody denní rotace:** - Dopředná bezpečnost: Kompromitace dnešního zaslepeného klíče neodhalí včerejšího - Nepropojitelnost: Denní rotace zabraňuje dlouhodobému sledování přes DHT - Oddělení klíčů: Různé klíče pro různá časová období

**Reference:** - [Specifikace protokolu Zcash](https://zips.z.cash/protocol/protocol.pdf) - Sekce 5.4.6.1 - [Diskuse o zaslepení klíče v Toru](https://lists.torproject.org/pipermail/tor-dev/2013-December/005943.html) - [Tor ticket č. 8106](https://trac.torproject.org/projects/tor/ticket/8106)

---

## Šifrování a zpracování

### Odvození Subcredential (podpověření)

Před šifrováním odvodíme pověření a podpověření, aby byly šifrované vrstvy vázány na znalost veřejného podpisového klíče Destination (adresa/identita služby v I2P).

**Cíl:** Zajistit, aby pouze ti, kteří znají veřejný podpisový klíč Destination (identita cíle v I2P), mohli dešifrovat šifrovaný LeaseSet. Není nutné znát celou Destination.

#### Výpočet pověření

```python
A = destination's signing public key (32 bytes)
stA = signature type of A (2 bytes big endian)
     # 0x0007 for Ed25519 or 0x000b for Red25519
stA' = signature type of blinded key A' (2 bytes big endian)
     # Always 0x000b (Red25519)

keydata = A || stA || stA'  # 36 bytes

credential = H("credential", keydata)  # 32 bytes
```
**Oddělení domén:** Personalizační řetězec `"credential"` zajišťuje, že tento hash nekoliduje s žádnými klíči pro vyhledávání v distribuované hašovací tabulce (DHT) ani s jinými způsoby použití protokolu.

#### Výpočet Subcredentialu (odvozeného pověření)

```python
blindedPublicKey = A' (32 bytes, from blinding process)

subcredential = H("subcredential", credential || blindedPublicKey)  # 32 bytes
```
**Účel:** Subcredential (podpověření) váže šifrovaný LeaseSet na: 1. konkrétní Destination (identifikátor cíle v I2P) (prostřednictvím credential) 2. konkrétní zaslepený klíč (prostřednictvím blindedPublicKey) 3. konkrétní den (prostřednictvím denní rotace blindedPublicKey)

Tím se zabraňuje replay attacks (útokům opakováním) a propojování napříč dny.

### Šifrování vrstvy 1

**Kontext:** Vrstva 1 obsahuje autorizační data klienta a je šifrována klíčem odvozeným od subcredential (dílčí pověřovací údaj).

#### Šifrovací algoritmus

```python
# Prepare input
outerInput = subcredential || publishedTimestamp
# publishedTimestamp: 4 bytes from Layer 0

# Generate random salt
outerSalt = CSRNG(32)  # 32 bytes

# Derive encryption key and IV
keys = HKDF(
    salt=outerSalt,
    ikm=outerInput,
    info="ELS2_L1K",  # Domain separation
    n=44  # 32 bytes key + 12 bytes IV
)

outerKey = keys[0:31]    # 32 bytes (indices 0-31 inclusive)
outerIV = keys[32:43]    # 12 bytes (indices 32-43 inclusive)

# Encrypt and prepend salt
outerPlaintext = [Layer 1 data]
outerCiphertext = outerSalt || ENCRYPT(outerKey, outerIV, outerPlaintext)
```
**Výstup:** `outerCiphertext` má `32 + len(outerPlaintext)` bajtů.

**Bezpečnostní vlastnosti:** - Salt zajišťuje jedinečné dvojice klíč/IV i při stejném subcredential (podpověření) - Kontextový řetězec `"ELS2_L1K"` zajišťuje oddělení domén - ChaCha20 poskytuje sémantické zabezpečení (šifrotext nerozlišitelný od náhodných dat)

#### Dešifrovací algoritmus

```python
# Parse salt from ciphertext
outerSalt = outerCiphertext[0:31]  # First 32 bytes

# Derive decryption key and IV (same process as encryption)
outerInput = subcredential || publishedTimestamp
keys = HKDF(
    salt=outerSalt,
    ikm=outerInput,
    info="ELS2_L1K",
    n=44
)

outerKey = keys[0:31]    # 32 bytes
outerIV = keys[32:43]    # 12 bytes

# Decrypt (skip salt bytes)
outerPlaintext = DECRYPT(outerKey, outerIV, outerCiphertext[32:end])
```
**Ověření:** Po dešifrování ověřte, že struktura vrstvy 1 je správně formovaná, než přejdete na vrstvu 2.

### Šifrování na 2. vrstvě

**Kontext:** Vrstva 2 obsahuje samotná data LeaseSet2 a je šifrována klíčem odvozeným z authCookie (pokud je povolena autentizace pro jednotlivé klienty) nebo klíčem odvozeným z prázdného řetězce (pokud není).

#### Šifrovací algoritmus

```python
# Determine authCookie based on authorization mode
if per_client_auth_enabled:
    authCookie = [32-byte cookie from client authorization process]
else:
    authCookie = b''  # Zero-length byte array

# Prepare input
innerInput = authCookie || subcredential || publishedTimestamp

# Generate random salt
innerSalt = CSRNG(32)  # 32 bytes

# Derive encryption key and IV
keys = HKDF(
    salt=innerSalt,
    ikm=innerInput,
    info="ELS2_L2K",  # Domain separation
    n=44  # 32 bytes key + 12 bytes IV
)

innerKey = keys[0:31]    # 32 bytes
innerIV = keys[32:43]    # 12 bytes

# Encrypt and prepend salt
innerPlaintext = [Layer 2 data: LS2 type byte + LeaseSet2 data]
innerCiphertext = innerSalt || ENCRYPT(innerKey, innerIV, innerPlaintext)
```
**Výstup:** `innerCiphertext` má velikost `32 + len(innerPlaintext)` bajtů.

**Vazba klíče:** - Pokud není použita autentizace klienta: Vázáno pouze na subcredential (podřazené pověření) a časové razítko - Pokud je zapnuta autentizace klienta: Navíc vázáno na authCookie (různé pro každého autorizovaného klienta)

#### Dešifrovací algoritmus

```python
# Determine authCookie (same as encryption)
if per_client_auth_enabled:
    authCookie = [32-byte cookie from client authorization process]
else:
    authCookie = b''  # Zero-length byte array

# Parse salt from ciphertext
innerSalt = innerCiphertext[0:31]  # First 32 bytes

# Derive decryption key and IV
innerInput = authCookie || subcredential || publishedTimestamp
keys = HKDF(
    salt=innerSalt,
    ikm=innerInput,
    info="ELS2_L2K",
    n=44
)

innerKey = keys[0:31]    # 32 bytes
innerIV = keys[32:43]    # 12 bytes

# Decrypt (skip salt bytes)
innerPlaintext = DECRYPT(innerKey, innerIV, innerCiphertext[32:end])
```
**Ověření:** Po dešifrování: 1. Ověřte, že bajt typu LS2 je platný (3 nebo 7) 2. Rozparsujte strukturu LeaseSet2 3. Ověřte, že vnitřní časové razítko odpovídá vnějšímu publikovanému časovému razítku 4. Ověřte, že vnitřní expirace odpovídá vnější expiraci 5. Ověřte podpis LeaseSet2

### Souhrn šifrovací vrstvy

```
┌─────────────────────────────────────────────────┐
│ Layer 0 (Plaintext)                             │
│ - Blinded public key                            │
│ - Timestamps                                    │
│ - Signature                                     │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │ Layer 1 (Encrypted with subcredential)  │   │
│  │ - Authorization flags                   │   │
│  │ - Client auth data (if enabled)         │   │
│  │                                          │   │
│  │  ┌────────────────────────────────┐     │   │
│  │  │ Layer 2 (Encrypted with        │     │   │
│  │  │          authCookie + subcred) │     │   │
│  │  │ - LeaseSet2 type               │     │   │
│  │  │ - LeaseSet2 data               │     │   │
│  │  │ - Leases                       │     │   │
│  │  │ - LS2 signature                │     │   │
│  │  └────────────────────────────────┘     │   │
│  └─────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```
**Postup dešifrování:** 1. Ověřte podpis Vrstvy 0 pomocí zaslepeného veřejného klíče 2. Dešifrujte Vrstvu 1 pomocí subcredential (podpověření) 3. Zpracujte autorizační data (pokud jsou k dispozici) pro získání authCookie 4. Dešifrujte Vrstvu 2 pomocí authCookie a subcredential 5. Ověřte a rozparsujte LeaseSet2

---

## Autorizace pro jednotlivé klienty

### Přehled

Je-li povolena autorizace pro jednotlivé klienty, server udržuje seznam autorizovaných klientů. Každý klient má klíčový materiál, který je nutné bezpečně předat mimo hlavní komunikační kanál.

**Dva mechanismy autorizace:** 1. **Autorizace klienta DH (Diffie-Hellman):** Bezpečnější, používá dohodu klíče X25519 2. **Autorizace PSK (Pre-Shared Key):** Jednodušší, používá symetrické klíče

**Obecné bezpečnostní vlastnosti:** - Soukromí členství klientů: Pozorovatelé vidí počet klientů, ale nemohou identifikovat konkrétní klienty - Anonymní přidávání/odebírání klientů: Nelze sledovat, kdy jsou konkrétní klienti přidáni nebo odebráni - Pravděpodobnost kolize 8bajtového identifikátoru klienta: ~1 z 18 kvintilionů (zanedbatelné)

### Autorizace klienta DH (Diffie–Hellmanova výměna klíčů)

**Přehled:** Každý klient generuje klíčový pár X25519 a prostřednictvím zabezpečeného mimopásmového kanálu odešle svůj veřejný klíč serveru. Server používá efemérní DH k zašifrování jedinečného authCookie pro každého klienta.

#### Generování klientských klíčů

```python
# Client generates keypair
csk_i = GENERATE_PRIVATE()  # 32-byte X25519 private key
cpk_i = DERIVE_PUBLIC(csk_i)  # 32-byte X25519 public key

# Client sends cpk_i to server via secure out-of-band channel
# Client KEEPS csk_i secret (never transmitted)
```
**Bezpečnostní výhoda:** Soukromý klíč klienta nikdy neopustí zařízení klienta. Útočník, který zachytí out-of-band (mimo hlavní kanál) přenos, nedokáže dešifrovat budoucí šifrované LeaseSets, aniž by prolomil X25519 DH.

#### Zpracování na serveru

```python
# Server generates new auth cookie and ephemeral keypair
authCookie = CSRNG(32)  # 32-byte cookie

esk = GENERATE_PRIVATE()  # 32-byte ephemeral private key
epk = DERIVE_PUBLIC(esk)  # 32-byte ephemeral public key

# For each authorized client i
for cpk_i in authorized_clients:
    # Perform DH key agreement
    sharedSecret = DH(esk, cpk_i)  # 32 bytes
    
    # Derive client-specific encryption key
    authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
    okm = HKDF(
        salt=epk,  # Ephemeral public key as salt
        ikm=authInput,
        info="ELS2_XCA",  # Domain separation
        n=52  # 32 key + 12 IV + 8 ID
    )
    
    # Extract components
    clientKey_i = okm[0:31]    # 32 bytes
    clientIV_i = okm[32:43]    # 12 bytes
    clientID_i = okm[44:51]    # 8 bytes
    
    # Encrypt authCookie for this client
    clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
    
    # Store [clientID_i, clientCookie_i] entry in Layer 1
```
**Datová struktura vrstvy 1:**

```
ephemeralPublicKey (32 bytes)
clients (2 bytes) = N
[clientID_1 (8 bytes) || clientCookie_1 (32 bytes)]
[clientID_2 (8 bytes) || clientCookie_2 (32 bytes)]
...
[clientID_N (8 bytes) || clientCookie_N (32 bytes)]
```
**Doporučení pro server:** - Vygenerujte nový efemérní pár klíčů pro každý zveřejněný šifrovaný LeaseSet - Náhodně měňte pořadí klientů, abyste zabránili sledování podle pozice - Zvažte přidání zástupných záznamů, abyste skryli skutečný počet klientů

#### Zpracování na straně klienta

```python
# Client has: csk_i (their private key), destination, date, secret
# Client receives: encrypted LeaseSet with epk in Layer 1

# Perform DH key agreement with server's ephemeral public key
sharedSecret = DH(csk_i, epk)  # 32 bytes

# Derive expected client identifier and decryption key
cpk_i = DERIVE_PUBLIC(csk_i)  # Client's own public key
authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp

okm = HKDF(
    salt=epk,
    ikm=authInput,
    info="ELS2_XCA",
    n=52
)

clientKey_i = okm[0:31]    # 32 bytes
clientIV_i = okm[32:43]    # 12 bytes
clientID_i = okm[44:51]    # 8 bytes

# Search Layer 1 authorization data for clientID_i
for (clientID, clientCookie) in layer1_auth_entries:
    if clientID == clientID_i:
        # Found matching entry, decrypt authCookie
        authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie)
        # Use authCookie to decrypt Layer 2
        break
else:
    # No matching entry - client not authorized or revoked
    raise AuthorizationError("Client not authorized")
```
**Zpracování chyb na straně klienta:** - Pokud `clientID_i` nenalezen: Klientovi byl přístup odebrán nebo nikdy nebyl autorizován - Pokud dešifrování selže: Poškozená data nebo nesprávné klíče (velmi vzácné) - Klienti by měli pravidelně znovu načítat, aby detekovali odebrání oprávnění

### Autorizace klienta pomocí předem sdíleného klíče (PSK)

**Přehled:** Každý klient má předem sdílený symetrický klíč o velikosti 32 bajtů. Server šifruje stejný authCookie pomocí PSK (předem sdílený klíč) každého klienta.

#### Generování klíčů

```python
# Option 1: Client generates key
psk_i = CSRNG(32)  # 32-byte pre-shared key
# Client sends psk_i to server via secure out-of-band channel

# Option 2: Server generates key
psk_i = CSRNG(32)  # 32-byte pre-shared key
# Server sends psk_i to one or more clients via secure out-of-band channel
```
**Bezpečnostní poznámka:** Stejný PSK (předem sdílený klíč) lze podle potřeby sdílet mezi více klienty (vytváří "skupinovou" autorizaci).

#### Zpracování na straně serveru

```python
# Server generates new auth cookie and salt
authCookie = CSRNG(32)  # 32-byte cookie
authSalt = CSRNG(32)     # 32-byte salt

# For each authorized client i
for psk_i in authorized_clients:
    # Derive client-specific encryption key
    authInput = psk_i || subcredential || publishedTimestamp
    
    okm = HKDF(
        salt=authSalt,
        ikm=authInput,
        info="ELS2PSKA",  # Domain separation
        n=52  # 32 key + 12 IV + 8 ID
    )
    
    # Extract components
    clientKey_i = okm[0:31]    # 32 bytes
    clientIV_i = okm[32:43]    # 12 bytes
    clientID_i = okm[44:51]    # 8 bytes
    
    # Encrypt authCookie for this client
    clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
    
    # Store [clientID_i, clientCookie_i] entry in Layer 1
```
**Datová struktura vrstvy 1:**

```
authSalt (32 bytes)
clients (2 bytes) = N
[clientID_1 (8 bytes) || clientCookie_1 (32 bytes)]
[clientID_2 (8 bytes) || clientCookie_2 (32 bytes)]
...
[clientID_N (8 bytes) || clientCookie_N (32 bytes)]
```
#### Zpracování klienta

```python
# Client has: psk_i (their pre-shared key), destination, date, secret
# Client receives: encrypted LeaseSet with authSalt in Layer 1

# Derive expected client identifier and decryption key
authInput = psk_i || subcredential || publishedTimestamp

okm = HKDF(
    salt=authSalt,
    ikm=authInput,
    info="ELS2PSKA",
    n=52
)

clientKey_i = okm[0:31]    # 32 bytes
clientIV_i = okm[32:43]    # 12 bytes
clientID_i = okm[44:51]    # 8 bytes

# Search Layer 1 authorization data for clientID_i
for (clientID, clientCookie) in layer1_auth_entries:
    if clientID == clientID_i:
        # Found matching entry, decrypt authCookie
        authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie)
        # Use authCookie to decrypt Layer 2
        break
else:
    # No matching entry - client not authorized or revoked
    raise AuthorizationError("Client not authorized")
```
### Srovnání a doporučení

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">DH Authorization</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">PSK Authorization</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Key Exchange</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Asymmetric (X25519)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Symmetric (shared secret)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Security</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Higher (forward secrecy)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Lower (depends on PSK secrecy)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Client Privacy</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Private key never transmitted</td><td style="border:1px solid var(--color-border); padding:0.5rem;">PSK must be transmitted securely</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Performance</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">N+1 DH operations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">No DH operations</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Key Sharing</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">One key per client</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Can share key among multiple clients</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Revocation Detection</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Adversary cannot tell when revoked</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Adversary can track revocation if PSK intercepted</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Use Case</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">High security requirements</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Performance-critical or group access</td></tr>
  </tbody>
</table>
**Doporučení:** - **Používejte autorizaci DH** pro vysoce zabezpečené aplikace, kde je důležité dopředné utajení - **Používejte autorizaci pomocí PSK (předem sdíleného klíče)** pokud je výkon kritický nebo při správě skupin klientů - **Nikdy znovu nepoužívejte PSK** napříč různými službami ani v různých časových obdobích - **Vždy používejte zabezpečené kanály** pro distribuci klíčů (např. Signal, OTR, PGP)

### Bezpečnostní hlediska

**Ochrana soukromí členství klienta:**

Oba mechanismy poskytují soukromí ohledně členství klientů prostřednictvím:
1. **Šifrované identifikátory klientů:** 8bajtové hodnoty clientID odvozené z výstupu HKDF (funkce pro odvozování klíčů na bázi HMAC)
2. **Nerozlišitelné soubory cookie:** Všechny hodnoty clientCookie o délce 32 bajtů se jeví jako náhodné
3. **Žádná metadata specifická pro klienta:** Neexistuje způsob, jak zjistit, která položka patří kterému klientovi

Pozorovatel může vidět: - Počet autorizovaných klientů (z pole `clients`) - Změny počtu klientů v čase

Pozorovatel NEMŮŽE vidět: - Kteří konkrétní klienti jsou autorizováni - Kdy jsou konkrétní klienti přidáni nebo odebráni (pokud počet zůstává stejný) - Jakékoli informace umožňující identifikaci klienta

**Doporučení pro randomizaci:**

Servery BY MĚLY pokaždé, když generují šifrovaný LeaseSet, náhodně změnit pořadí klientů:

```python
import random

# Before serializing
auth_entries = [(clientID_i, clientCookie_i) for each client]
random.shuffle(auth_entries)
# Now serialize in randomized order
```
**Výhody:** - Zabraňuje klientům zjistit svou pozici v seznamu - Zabraňuje inferenčním útokům založeným na změnách pozice v seznamu - Učiní přidání/odebrání klienta nerozlišitelným

**Skrytí počtu klientů:**

Servery MOHOU vkládat náhodné výplňové záznamy:

```python
# Add dummy entries
num_dummies = random.randint(0, max_dummies)
for _ in range(num_dummies):
    dummy_id = CSRNG(8)
    dummy_cookie = CSRNG(32)
    auth_entries.append((dummy_id, dummy_cookie))

# Randomize all entries (real + dummy)
random.shuffle(auth_entries)
```
**Náklady:** Zástupné položky zvětšují velikost šifrovaného LeaseSetu (každá o 40 bajtů).

**Rotace AuthCookie:**

Servery by měly vygenerovat nový authCookie: - Pokaždé, když je publikován šifrovaný LeaseSet (obvykle každých několik hodin) - Ihned po odebrání přístupu klientovi - V pravidelných intervalech (např. denně), i když nedojde k žádným změnám u klientů

**Výhody:** - Omezuje dopad, pokud dojde ke kompromitaci authCookie - Zajišťuje, že klientům s odvolaným oprávněním je přístup rychle zablokován - Poskytuje dopředné utajení pro vrstvu 2

---

## Adresování Base32 pro šifrované LeaseSets

### Přehled

Tradiční base32 adresy I2P obsahují pouze hash Destination (32 bajtů → 52 znaků). To je nedostatečné pro šifrované LeaseSets, protože:

1. Klienti potřebují **neoslepený veřejný klíč** k derivaci oslepeného veřejného klíče
2. Klienti potřebují **typy podpisů** (neoslepené a oslepené) pro správnou derivaci klíče
3. Samotný hash tyto informace neposkytuje

**Řešení:** Nový formát base32 (kódování Base32), který obsahuje veřejný klíč a typy podpisů.

### Specifikace formátu adresy

**Dekódovaná struktura (35 bajtů):**

```
┌─────────────────────────────────────────────────────┐
│ Byte 0   │ Byte 1  │ Byte 2  │ Bytes 3-34          │
│ Flags    │ Unblind │ Blinded │ Public Key          │
│ (XOR)    │ SigType │ SigType │ (32 bytes)          │
│          │ (XOR)   │ (XOR)   │                     │
└─────────────────────────────────────────────────────┘
```
**První 3 bajty (XOR s kontrolním součtem):**

První 3 bajty obsahují metadata XORovaná s částmi kontrolního součtu CRC-32:

```python
# Data structure before XOR
flags = 0x00           # 1 byte (reserved for future use)
unblinded_sigtype = 0x07 or 0x0b  # 1 byte (7 or 11)
blinded_sigtype = 0x0b  # 1 byte (always 11)

# Compute CRC-32 checksum of public key
checksum = crc32(pubkey)  # 4-byte CRC-32 of bytes 3-34

# XOR first 3 bytes with parts of checksum
data[0] = flags XOR (checksum >> 24) & 0xFF
data[1] = unblinded_sigtype XOR (checksum >> 16) & 0xFF  
data[2] = blinded_sigtype XOR (checksum >> 8) & 0xFF

# Bytes 3-34 contain the unmodified 32-byte public key
data[3:34] = pubkey
```
**Vlastnosti kontrolního součtu:** - Používá standardní polynom CRC-32 - Míra falešně negativních výsledků: ~1 z 16 milionů - Detekuje překlepy v adrese - Nelze použít k autentizaci (není kryptograficky bezpečný)

**Kódovaný formát:**

```
Base32Encode(35 bytes) || ".b32.i2p"
```
**Vlastnosti:** - Celkový počet znaků: 56 (35 bajtů × 8 bitů ÷ 5 bitů na znak) - Koncovka: ".b32.i2p" (stejná jako tradiční base32) - Celková délka: 56 + 8 = 64 znaků (bez nulového terminátoru)

**Kódování Base32:** - Abeceda: `abcdefghijklmnopqrstuvwxyz234567` (standardu RFC 4648) - 5 nevyužitých bitů na konci MUSÍ být 0 - Nerozlišuje velikost písmen (dle konvence malá písmena)

### Generování adres

```python
import struct
from zlib import crc32
import base64

def generate_encrypted_b32_address(pubkey, unblinded_sigtype, blinded_sigtype):
    """
    Generate base32 address for encrypted LeaseSet.
    
    Args:
        pubkey: 32-byte public key (bytes)
        unblinded_sigtype: Unblinded signature type (7 or 11)
        blinded_sigtype: Blinded signature type (always 11)
    
    Returns:
        String address ending in .b32.i2p
    """
    # Verify inputs
    assert len(pubkey) == 32, "Public key must be 32 bytes"
    assert unblinded_sigtype in [7, 11], "Unblinded sigtype must be 7 or 11"
    assert blinded_sigtype == 11, "Blinded sigtype must be 11"
    
    # Compute CRC-32 of public key
    checksum = crc32(pubkey) & 0xFFFFFFFF  # Ensure 32-bit unsigned
    
    # Prepare metadata bytes
    flags = 0x00
    
    # XOR metadata with checksum parts
    byte0 = flags ^ ((checksum >> 24) & 0xFF)
    byte1 = unblinded_sigtype ^ ((checksum >> 16) & 0xFF)
    byte2 = blinded_sigtype ^ ((checksum >> 8) & 0xFF)
    
    # Construct 35-byte data
    data = bytes([byte0, byte1, byte2]) + pubkey
    
    # Base32 encode (standard alphabet)
    # Python's base64 module uses uppercase by default
    b32 = base64.b32encode(data).decode('ascii').lower().rstrip('=')
    
    # Construct full address
    address = b32 + ".b32.i2p"
    
    return address
```
### Parsování adres

```python
import struct
from zlib import crc32
import base64

def parse_encrypted_b32_address(address):
    """
    Parse base32 address for encrypted LeaseSet.
    
    Args:
        address: String address ending in .b32.i2p
    
    Returns:
        Tuple of (pubkey, unblinded_sigtype, blinded_sigtype)
    
    Raises:
        ValueError: If address is invalid or checksum fails
    """
    # Remove suffix
    if not address.endswith('.b32.i2p'):
        raise ValueError("Invalid address suffix")
    
    b32 = address[:-8]  # Remove ".b32.i2p"
    
    # Verify length (56 characters for 35 bytes)
    if len(b32) != 56:
        raise ValueError(f"Invalid length: {len(b32)} (expected 56)")
    
    # Base32 decode
    # Add padding if needed
    padding_needed = (8 - (len(b32) % 8)) % 8
    b32_padded = b32.upper() + '=' * padding_needed
    
    try:
        data = base64.b32decode(b32_padded)
    except Exception as e:
        raise ValueError(f"Invalid base32 encoding: {e}")
    
    # Verify decoded length
    if len(data) != 35:
        raise ValueError(f"Invalid decoded length: {len(data)} (expected 35)")
    
    # Extract public key
    pubkey = data[3:35]
    
    # Compute CRC-32 for verification
    checksum = crc32(pubkey) & 0xFFFFFFFF
    
    # Un-XOR metadata bytes
    flags = data[0] ^ ((checksum >> 24) & 0xFF)
    unblinded_sigtype = data[1] ^ ((checksum >> 16) & 0xFF)
    blinded_sigtype = data[2] ^ ((checksum >> 8) & 0xFF)
    
    # Verify expected values
    if flags != 0x00:
        raise ValueError(f"Invalid flags: {flags:#x} (expected 0x00)")
    
    if unblinded_sigtype not in [7, 11]:
        raise ValueError(f"Invalid unblinded sigtype: {unblinded_sigtype} (expected 7 or 11)")
    
    if blinded_sigtype != 11:
        raise ValueError(f"Invalid blinded sigtype: {blinded_sigtype} (expected 11)")
    
    return pubkey, unblinded_sigtype, blinded_sigtype
```
### Srovnání s tradičním Base32

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Traditional B32</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Encrypted LS2 B32</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Content</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-256 hash of Destination</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Public key + signature types</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Decoded Size</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">35 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Encoded Length</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">52 characters</td><td style="border:1px solid var(--color-border); padding:0.5rem;">56 characters</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Suffix</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">.b32.i2p</td><td style="border:1px solid var(--color-border); padding:0.5rem;">.b32.i2p</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Total Length</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">60 chars</td><td style="border:1px solid var(--color-border); padding:0.5rem;">64 chars</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Checksum</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">None</td><td style="border:1px solid var(--color-border); padding:0.5rem;">CRC-32 (XOR'd into first 3 bytes)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Use Case</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Regular destinations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted LeaseSet destinations</td></tr>
  </tbody>
</table>
### Omezení použití

**Nekompatibilita BitTorrentu:**

Šifrované adresy LS2 NELZE používat s compact announce replies (kompaktními odpověďmi announce) BitTorrentu:

```
Compact announce reply format:
┌────────────────────────────┐
│ 32-byte destination hash   │  ← Only hash, no signature types
│ 2-byte port                │
└────────────────────────────┘
```
**Problém:** Kompaktní formát obsahuje pouze hash (32 bajtů), bez prostoru pro typy podpisů nebo informace o veřejném klíči.

**Řešení:** Použijte plné odpovědi announce (oznámení) nebo trackery založené na HTTP, které podporují plné adresy.

### Integrace adresáře

Pokud má klient v adresáři plnou Destination (cílová identita v I2P):

1. Uložit plnou Destination (cílový identifikátor; obsahuje veřejný klíč)
2. Podporovat reverzní vyhledávání podle hashe
3. Při nalezení šifrované LS2 získat veřejný klíč z adresáře
4. Není třeba nového formátu base32, pokud je plná Destination již známa

**Formáty adresáře, které podporují šifrované LS2:** - hosts.txt s úplnými řetězci destinací - databáze SQLite se sloupcem destination - formáty JSON/XML s úplnými daty destinace

### Příklady implementace

**Příklad 1: Vygenerování adresy**

```python
# Ed25519 destination example
pubkey = bytes.fromhex('a' * 64)  # 32-byte public key
unblinded_type = 7   # Ed25519
blinded_type = 11    # Red25519 (always)

address = generate_encrypted_b32_address(pubkey, unblinded_type, blinded_type)
print(f"Address: {address}")
# Output: 56 base32 characters + .b32.i2p
```
**Příklad 2: Parsování a validace**

```python
address = "abc...xyz.b32.i2p"  # 56 chars + suffix

try:
    pubkey, unblinded, blinded = parse_encrypted_b32_address(address)
    print(f"Public Key: {pubkey.hex()}")
    print(f"Unblinded SigType: {unblinded}")
    print(f"Blinded SigType: {blinded}")
except ValueError as e:
    print(f"Invalid address: {e}")
```
**Příklad 3: Převod z Destination (cíl v I2P)**

```python
def destination_to_encrypted_b32(destination):
    """
    Convert full Destination to encrypted LS2 base32 address.
    
    Args:
        destination: I2P Destination object
    
    Returns:
        Base32 address string
    """
    # Extract public key and signature type from destination
    pubkey = destination.signing_public_key  # 32 bytes
    sigtype = destination.sig_type  # 7 or 11
    
    # Blinded type is always 11 (Red25519)
    blinded_type = 11
    
    # Generate address
    return generate_encrypted_b32_address(pubkey, sigtype, blinded_type)
```
### Bezpečnostní aspekty

**Soukromí:** - Adresa Base32 odhaluje veřejný klíč - Je to záměrné a vyžadované protokolem - Neprozrazuje soukromý klíč ani neohrožuje bezpečnost - Veřejné klíče jsou záměrně veřejnou informací

**Odolnost vůči kolizím:** - CRC-32 poskytuje pouze 32 bitů odolnosti vůči kolizím - Není kryptograficky bezpečný (používejte pouze pro detekci chyb) - V žádném případě nespoléhejte na kontrolní součet pro autentizaci - Úplné ověření cíle je stále vyžadováno

**Ověření adresy:** - Před použitím vždy ověřte kontrolní součet - Odmítejte adresy s neplatnými typy podpisů - Ověřte, že veřejný klíč leží na křivce (v závislosti na implementaci)

**Odkazy:** - [Návrh 149: B32 pro šifrovaný LS2](/proposals/149-b32-encrypted-ls2/) - [Specifikace adresování B32](/docs/specs/b32-for-encrypted-leasesets/) - [Specifikace pojmenování I2P](/docs/overview/naming/)

---

## Podpora offline klíčů

### Přehled

Offline klíče umožňují, aby hlavní podepisovací klíč zůstal offline (v režimu studeného úložiště), zatímco dočasný podepisovací klíč se používá pro každodenní provoz. To je zásadní pro služby s vysokými nároky na bezpečnost.

**Specifické požadavky pro šifrované LS2:** - Dočasné klíče musí být generovány offline - Zaslepené soukromé klíče musí být předgenerovány (jeden denně) - Oba typy klíčů, dočasné i zaslepené, se dodávají v dávkách - Standardizovaný formát souboru zatím není definován (TODO ve specifikaci)

### Struktura offline klíče

**Data dočasného klíče vrstvy 0 (když je příznakový bit 0 = 1):**

```
┌───────────────────────────────────────────────────┐
│ Expires Timestamp       │ 4 bytes (seconds)       │
│ Transient Sig Type      │ 2 bytes (big endian)    │
│ Transient Signing Pubkey│ Variable (sigtype len)  │
│ Signature (by blinded)  │ 64 bytes (Red25519)     │
└───────────────────────────────────────────────────┘
```
**Rozsah podpisu:** Podpis v offline bloku klíče zahrnuje: - Časové razítko vypršení platnosti (4 bajty) - Dočasný typ podpisu (2 bajty)   - Dočasný veřejný klíč pro podepisování (proměnné délky)

Tento podpis je ověřen pomocí **zaslepeného veřejného klíče**, což dokazuje, že entita se zaslepeným soukromým klíčem autorizovala tento dočasný klíč.

### Proces generování klíčů

**Pro šifrovaný LeaseSet s offline klíči:**

1. **Vygenerujte dočasné klíčové páry** (offline, ve studeném úložišti):
   ```python
   # For each day in future
   for date in future_dates:
       # Generate daily transient keypair
       transient_privkey = generate_red25519_privkey()  # Type 11
       transient_pubkey = derive_public(transient_privkey)

       # Store for later delivery
       keys[date] = (transient_privkey, transient_pubkey)
   ```

2. **Generate daily blinded keypairs** (offline, in cold storage):
   ```python
# Pro každý den    for date in future_dates:

       # Derive alpha for this date
       datestring = date.strftime("%Y%m%d")  # "YYYYMMDD"
       alpha = GENERATE_ALPHA(destination, datestring, secret)
       
       # Blind the signing private key
       a = destination_signing_privkey  # Type 7 or 11
       blinded_privkey = BLIND_PRIVKEY(a, alpha)  # Result is type 11
       blinded_pubkey = DERIVE_PUBLIC(blinded_privkey)
       
       # Store for later delivery
       blinded_keys[date] = (blinded_privkey, blinded_pubkey)
   ```

3. **Sign transient keys with blinded keys** (offline):
   ```python
for date in future_dates:

       transient_pubkey = keys[date][1]
       blinded_privkey = blinded_keys[date][0]
       
       # Create signature data
       expires = int((date + timedelta(days=1)).timestamp())
       sig_data = struct.pack('>I', expires)  # 4 bytes
       sig_data += struct.pack('>H', 11)     # Transient type (Red25519)
       sig_data += transient_pubkey          # 32 bytes
       
       # Sign with blinded private key
       signature = RED25519_SIGN(blinded_privkey, sig_data)
       
       # Package for delivery
       offline_sig_blocks[date] = {
           'expires': expires,
           'transient_type': 11,
           'transient_pubkey': transient_pubkey,
           'signature': signature
       }
   ```

4. **Package for delivery to router:**
   ```python
# Pro každé datum    delivery_package[date] = {

       'transient_privkey': keys[date][0],
       'transient_pubkey': keys[date][1],
       'blinded_privkey': blinded_keys[date][0],
       'blinded_pubkey': blinded_keys[date][1],
       'offline_sig_block': offline_sig_blocks[date]
}

   ```

### Router Usage

**Daily Key Loading:**

```python
# O půlnoci UTC (nebo před zveřejněním)

date = datetime.utcnow().date()

# Načíst dnešní klíče

today_keys = load_delivery_package(date)

transient_privkey = today_keys['transient_privkey'] transient_pubkey = today_keys['transient_pubkey'] blinded_privkey = today_keys['blinded_privkey'] blinded_pubkey = today_keys['blinded_pubkey'] offline_sig_block = today_keys['offline_sig_block']

# Použijte tyto klíče pro dnešní šifrovaný LeaseSet

```

**Publishing Process:**

```python
# 1. Vytvořte vnitřní LeaseSet2

inner_ls2 = create_leaseset2(

    destinations, leases, expires, 
    signing_key=transient_privkey  # Use transient key
)

# 2. Zašifrujte vrstvu 2

layer2_ciphertext = encrypt_layer2(inner_ls2, authCookie, subcredential, timestamp)

# 3. Vytvořte vrstvu 1 s autorizačními údaji

layer1_plaintext = create_layer1(authorization_data, layer2_ciphertext)

# 4. Zašifrujte vrstvu 1

layer1_ciphertext = encrypt_layer1(layer1_plaintext, subcredential, timestamp)

# 5. Vytvořte vrstvu 0 s blokem offline podpisu

layer0 = create_layer0(

    blinded_pubkey,
    timestamp,
    expires,
    flags=0x0001,  # Bit 0 set (offline keys present)
    offline_sig_block=offline_sig_block,
    layer1_ciphertext=layer1_ciphertext
)

# 6. Podepište vrstvu 0 dočasným soukromým klíčem

signature = RED25519_SIGN(transient_privkey, layer0)

# 7. Připojte podpis a zveřejněte

encrypted_leaseset = layer0 + signature publish_to_netdb(encrypted_leaseset)

```

### Security Considerations

**Tracking via Offline Signature Block:**

The offline signature block is in plaintext (Layer 0). An adversary scraping floodfills could:
- Track the same encrypted LeaseSet across multiple days
- Correlate encrypted LeaseSets even though blinded keys change daily

**Mitigation:** Generate new transient keys daily (in addition to blinded keys):

```python
# Každý den generovat jak nové dočasné, tak i nové oslepené klíče

for date in future_dates:

    # New transient keypair for this day
    transient_privkey = generate_red25519_privkey()
    transient_pubkey = derive_public(transient_privkey)
    
    # New blinded keypair for this day
    alpha = GENERATE_ALPHA(destination, datestring, secret)
    blinded_privkey = BLIND_PRIVKEY(signing_privkey, alpha)
    blinded_pubkey = DERIVE_PUBLIC(blinded_privkey)
    
    # Sign new transient key with new blinded key
    sig = RED25519_SIGN(blinded_privkey, transient_pubkey || metadata)
    
    # Now offline sig block changes daily
```

**Benefits:**
- Prevents tracking across days via offline signature block
- Provides same security as encrypted LS2 without offline keys
- Each day appears completely independent

**Cost:**
- More keys to generate and store
- More complex key management

### File Format (TODO)

**Current Status:** No standardized file format defined for batch key delivery.

**Requirements for Future Format:**

1. **Must support multiple dates:**
   - Batch delivery of 30+ days worth of keys
   - Clear date association for each key set

2. **Must include all necessary data:**
   - Transient private key
   - Transient public key
   - Blinded private key
   - Blinded public key
   - Pre-computed offline signature block
   - Expiration timestamps

3. **Should be tamper-evident:**
   - Checksums or signatures over entire file
   - Integrity verification before loading

4. **Should be encrypted:**
   - Keys are sensitive material
   - Encrypt file with router's key or passphrase

**Proposed Format Example (JSON, encrypted):**

```json
{   "version": 1,   "destination_hash": "base64...",   "keys": [

    {
      "date": "2025-10-15",
      "transient": {
        "type": 11,
        "privkey": "base64...",
        "pubkey": "base64..."
      },
      "blinded": {
        "privkey": "base64...",
        "pubkey": "base64..."
      },
      "offline_sig_block": {
        "expires": 1729123200,
        "signature": "base64..."
      }
    }
],   "signature": "base64..."  // Signature over entire structure }

```

### I2CP Protocol Enhancement (TODO)

**Current Status:** No I2CP protocol enhancement defined for offline keys with encrypted LeaseSet.

**Requirements:**

1. **Key delivery mechanism:**
   - Upload batch of keys from client to router
   - Acknowledgment of successful key loading

2. **Key expiration notification:**
   - Router notifies client when keys running low
   - Client can generate and upload new batch

3. **Key revocation:**
   - Emergency revocation of future keys if compromise suspected

**Proposed I2CP Messages:**

```
UPLOAD_OFFLINE_KEYS   - Dávka šifrovaného klíčového materiálu   - Pokryté časové období

OFFLINE_KEY_STATUS   - Počet zbývajících dnů   - Datum příštího vypršení platnosti klíče

REVOKE_OFFLINE_KEYS     - Časové rozmezí k odvolání   - Nové klíče k nahrazení (volitelné)

```

### Implementation Status

**Java I2P:**
- ✅ Offline keys for standard LS2: Fully supported (since 0.9.38)
- ⚠️ Offline keys for encrypted LS2: Implemented (since 0.9.40)
- ❌ File format: Not standardized
- ❌ I2CP protocol: Not enhanced

**i2pd (C++):**
- ✅ Offline keys for standard LS2: Fully supported
- ✅ Offline keys for encrypted LS2: Fully supported (since 2.58.0)
- ❌ File format: Not standardized
- ❌ I2CP protocol: Not enhanced

**References:**
- [Offline Signatures Proposal](/proposals/123-new-netdb-entries/)
- [I2CP Specification](/docs/specs/i2cp/)

---

## Security Considerations

### Cryptographic Security

**Algorithm Selection:**

All cryptographic primitives are based on well-studied algorithms:
- **ChaCha20:** Modern stream cipher, constant-time, no timing attacks
- **SHA-256:** NIST-approved hash, 128-bit security level
- **HKDF:** RFC 5869 standard, proven security bounds
- **Ed25519/Red25519:** Curve25519-based, ~128-bit security level
- **X25519:** Diffie-Hellman over Curve25519, ~128-bit security level

**Key Sizes:**
- All symmetric keys: 256 bits (32 bytes)
- All public/private keys: 256 bits (32 bytes)
- All nonces/IVs: 96 bits (12 bytes)
- All signatures: 512 bits (64 bytes)

These sizes provide adequate security margins against current and near-future attacks.

### Forward Secrecy

**Daily Key Rotation:**

Encrypted LeaseSets rotate keys daily (UTC midnight):
- New blinded public/private key pair
- New storage location in DHT
- New encryption keys for both layers

**Benefits:**
- Compromising today's blinded key doesn't reveal yesterday's
- Limits exposure window to 24 hours
- Prevents long-term tracking via DHT

**Enhanced with Ephemeral Keys:**

DH client authorization uses ephemeral keys:
- Server generates new ephemeral DH keypair for each publication
- Compromising ephemeral key only affects that publication
- True forward secrecy even if long-term keys compromised

### Privacy Properties

**Destination Blinding:**

The blinded public key:
- Is unlinkable to the original destination (without knowing the secret)
- Changes daily, preventing long-term correlation
- Cannot be reversed to find the original public key

**Client Membership Privacy:**

Per-client authorization provides:
- **Anonymity:** No way to identify which clients are authorized
- **Untraceability:** Cannot track when specific clients added/revoked
- **Size obfuscation:** Can add dummy entries to hide true count

**DHT Privacy:**

Storage location rotates daily:
```
location = SHA-256(sig_type || blinded_public_key)

```

This prevents:
- Correlation across days via DHT lookups
- Long-term monitoring of service availability
- Traffic analysis of DHT queries

### Threat Model

**Adversary Capabilities:**

1. **Network Adversary:**
   - Can monitor all DHT traffic
   - Can observe encrypted LeaseSet publications
   - Cannot decrypt without proper keys

2. **Floodfill Adversary:**
   - Can store and analyze all encrypted LeaseSets
   - Can track publication patterns over time
   - Cannot decrypt Layer 1 or Layer 2
   - Can see client count (but not identities)

3. **Authorized Client Adversary:**
   - Can decrypt specific encrypted LeaseSets
   - Can access inner LeaseSet2 data
   - Cannot determine other clients' identities
   - Cannot decrypt past LeaseSets (with ephemeral keys)

**Out of Scope:**

- Malicious router implementations
- Compromised router host systems
- Side-channel attacks (timing, power analysis)
- Physical access to keys
- Social engineering attacks

### Attack Scenarios

**1. Offline Keys Tracking Attack:**

**Attack:** Adversary tracks encrypted LeaseSets via unchanging offline signature block.

**Mitigation:** Generate new transient keys daily (in addition to blinded keys).

**Status:** Documented recommendation, implementation-specific.

**2. Client Position Inference Attack:**

**Attack:** If client order is static, clients can infer their position and detect when other clients added/removed.

**Mitigation:** Randomize client order in authorization list for each publication.

**Status:** Documented recommendation in specification.

**3. Client Count Analysis Attack:**

**Attack:** Adversary monitors client count changes over time to infer service popularity or client churn.

**Mitigation:** Add random dummy entries to authorization list.

**Status:** Optional feature, deployment-specific trade-off (size vs. privacy).

**4. PSK Interception Attack:**

**Attack:** Adversary intercepts PSK during out-of-band exchange and can decrypt all future encrypted LeaseSets.

**Mitigation:** Use DH client authorization instead, or ensure secure key exchange (Signal, OTR, PGP).

**Status:** Known limitation of PSK approach, documented in specification.

**5. Timing Correlation Attack:**

**Attack:** Adversary correlates publication times across days to link encrypted LeaseSets.

**Mitigation:** Randomize publication times, use delayed publishing.

**Status:** Implementation-specific, not addressed in core specification.

**6. Long-term Secret Compromise:**

**Attack:** Adversary compromises the blinding secret and can compute all past and future blinded keys.

**Mitigation:** 
- Use optional secret parameter (not empty)
- Rotate secret periodically
- Use different secrets for different services

**Status:** Secret parameter is optional; using it is highly recommended.

### Operational Security

**Key Management:**

1. **Signing Private Key:**
   - Store offline in cold storage
   - Use only for generating blinded keys (batch process)
   - Never expose to online router

2. **Blinded Private Keys:**
   - Generate offline, deliver in batches
   - Rotate daily automatically
   - Delete after use (forward secrecy)

3. **Transient Private Keys (with offline keys):**
   - Generate offline, deliver in batches
   - Can be longer-lived (days/weeks)
   - Rotate regularly for enhanced privacy

4. **Client Authorization Keys:**
   - DH: Client private keys never leave client device
   - PSK: Use unique keys per client, secure exchange
   - Revoke immediately upon client removal

**Secret Management:**

The optional secret parameter in `GENERATE_ALPHA`:
- SHOULD be used for high-security services
- MUST be transmitted securely to authorized clients
- SHOULD be rotated periodically (e.g., monthly)
- CAN be different for different client groups

**Monitoring and Auditing:**

1. **Publication Monitoring:**
   - Verify encrypted LeaseSets published successfully
   - Monitor floodfill acceptance rates
   - Alert on publication failures

2. **Client Access Monitoring:**
   - Log client authorization attempts (without identifying clients)
   - Monitor for unusual patterns
   - Detect potential attacks early

3. **Key Rotation Auditing:**
   - Verify daily key rotation occurs
   - Check blinded key changes daily
   - Ensure old keys are deleted

### Implementation Security

**Constant-Time Operations:**

Implementations MUST use constant-time operations for:
- All scalar arithmetic (mod L operations)
- Private key comparisons
- Signature verification
- DH key agreement

**Memory Security:**

- Zero sensitive key material after use
- Use secure memory allocation for keys
- Prevent keys from being paged to disk
- Clear stack variables containing key material

**Random Number Generation:**

- Use cryptographically secure RNG (CSRNG)
- Properly seed RNG from OS entropy source
- Do not use predictable RNGs for key material
- Verify RNG output quality periodically

**Input Validation:**

- Validate all public keys are on the curve
- Check all signature types are supported
- Verify all lengths before parsing
- Reject malformed encrypted LeaseSets early

**Error Handling:**

- Do not leak information via error messages
- Use constant-time comparison for authentication
- Do not expose timing differences in decryption
- Log security-relevant events properly

### Recommendations

**For Service Operators:**

1. ✅ **Use Red25519 (type 11)** for new destinations
2. ✅ **Use DH client authorization** for high-security services
3. ✅ **Generate new transient keys daily** when using offline keys
4. ✅ **Use the optional secret parameter** in GENERATE_ALPHA
5. ✅ **Randomize client order** in authorization lists
6. ✅ **Monitor publication success** and investigate failures
7. ⚠️ **Consider dummy entries** to hide client count (size trade-off)

**For Client Implementers:**

1. ✅ **Validate blinded public keys** are on prime-order subgroup
2. ✅ **Verify all signatures** before trusting data
3. ✅ **Use constant-time operations** for cryptographic primitives
4. ✅ **Zero key material** immediately after use
5. ✅ **Implement proper error handling** without information leaks
6. ✅ **Support both Ed25519 and Red25519** destination types

**For Network Operators:**

1. ✅ **Accept encrypted LeaseSets** in floodfill routers
2. ✅ **Enforce reasonable size limits** to prevent abuse
3. ✅ **Monitor for anomalous patterns** (extremely large, frequent updates)
4. ⚠️ **Consider rate limiting** encrypted LeaseSet publications

---

## Implementation Notes

### Java I2P Implementation

**Repository:** https://github.com/i2p/i2p.i2p

**Key Classes:**
- `net.i2p.data.LeaseSet2` - LeaseSet2 structure
- `net.i2p.data.EncryptedLeaseSet` - Encrypted LS2 implementation
- `net.i2p.crypto.eddsa.EdDSAEngine` - Ed25519/Red25519 signatures
- `net.i2p.crypto.HKDF` - HKDF implementation
- `net.i2p.crypto.ChaCha20` - ChaCha20 cipher

**Configuration:**

Enable encrypted LeaseSet in `clients.config`:
```properties
# Povolit šifrovaný LeaseSet

i2cp.encryptLeaseSet=true

# Volitelné: Povolit autorizaci klienta

i2cp.enableAccessList=true

# Volitelné: Použít autorizaci DH (výchozí je PSK)

i2cp.accessListType=0

# Volitelné: Blinding secret (tajný údaj pro zaslepení) (důrazně doporučeno)

i2cp.blindingSecret=your-secret-here

```

**API Usage Example:**

```java
// Vytvořte šifrovaný LeaseSet EncryptedLeaseSet els = new EncryptedLeaseSet();

// Nastavit cílovou adresu els.setDestination(destination);

// Povolte autorizaci pro jednotlivé klienty els.setAuthorizationEnabled(true); els.setAuthType(EncryptedLeaseSet.AUTH_DH);

// Přidejte autorizované klienty (veřejné klíče DH) for (byte[] clientPubKey : authorizedClients) {

    els.addClient(clientPubKey);
}

// Nastavte parametry blinding (zaslepení) els.setBlindingSecret("your-secret");

// Podepište a publikujte els.sign(signingPrivateKey); netDb.publish(els);

```

### i2pd (C++) Implementation

**Repository:** https://github.com/PurpleI2P/i2pd

**Key Files:**
- `libi2pd/LeaseSet.h/cpp` - LeaseSet implementations
- `libi2pd/Crypto.h/cpp` - Cryptographic primitives
- `libi2pd/Ed25519.h/cpp` - Ed25519/Red25519 signatures
- `libi2pd/ChaCha20.h/cpp` - ChaCha20 cipher

**Configuration:**

Enable in tunnel configuration (`tunnels.conf`):
```ini
[my-hidden-service] type = http host = 127.0.0.1 port = 8080 keys = my-service-keys.dat

# Povolit šifrovaný LeaseSet

encryptleaseset = true

# Volitelné: Typ autorizace klienta (0=DH, 1=PSK)

authtype = 0

# Volitelné: Tajemství zaslepení

secret = váš-tajný-klíč-zde

# Volitelné: Autorizovaní klienti (po jednom na řádek, veřejné klíče zakódované v Base64)

client.1 = base64-encoded-client-pubkey-1 client.2 = base64-encoded-client-pubkey-2

```

**API Usage Example:**

```cpp
// Vytvořte šifrovaný LeaseSet (sada údajů o příchozích tunnel destinace v I2P) auto encryptedLS = std::make_shared<i2p::data::EncryptedLeaseSet>(

    destination,
    blindingSecret
);

// Povolit autorizaci pro jednotlivé klienty encryptedLS->SetAuthType(i2p::data::AUTH_TYPE_DH);

// Přidejte autorizované klienty for (const auto& clientPubKey : authorizedClients) {

    encryptedLS->AddClient(clientPubKey);
}

// Podepište a publikujte encryptedLS->Sign(signingPrivKey); netdb.Publish(encryptedLS);

```

### Testing and Debugging

**Test Vectors:**

Generate test vectors for implementation verification:

```python
# Testovací vektor 1: zaslepení klíče

destination_pubkey = bytes.fromhex('a' * 64) sigtype = 7 blinded_sigtype = 11 date = "20251015" secret = ""

alpha = generate_alpha(destination_pubkey, sigtype, blinded_sigtype, date, secret) print(f"Alpha: {alpha.hex()}")

# Očekávané: (ověřte podle referenční implementace)

```

**Unit Tests:**

Key areas to test:
1. HKDF derivation with various inputs
2. ChaCha20 encryption/decryption
3. Red25519 signature generation and verification
4. Key blinding (private and public)
5. Layer 1/2 encryption/decryption
6. Client authorization (DH and PSK)
7. Base32 address generation and parsing

**Integration Tests:**

1. Publish encrypted LeaseSet to test network
2. Retrieve and decrypt from client
3. Verify daily key rotation
4. Test client authorization (add/remove clients)
5. Test offline keys (if supported)

**Common Implementation Errors:**

1. **Incorrect mod L reduction:** Must use proper modular arithmetic
2. **Endianness errors:** Most fields are big-endian, but some crypto uses little-endian
3. **Off-by-one in array slicing:** Verify indices are inclusive/exclusive as needed
4. **Missing constant-time comparisons:** Use constant-time for all sensitive comparisons
5. **Not zeroing key material:** Always zero keys after use

### Performance Considerations

**Computational Costs:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Cost</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Key blinding (server)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 scalar mult</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per publication</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Key blinding (client)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 point add + 1 scalar mult</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per retrieval</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Layer 1 encryption</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 HKDF + 1 ChaCha20</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Fast</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Layer 2 encryption</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 HKDF + 1 ChaCha20</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Fast</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DH client auth (server)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">N+1 X25519 ops</td><td style="border:1px solid var(--color-border); padding:0.5rem;">N = number of clients</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DH client auth (client)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 X25519 op</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per retrieval</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">PSK client auth</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0 DH ops</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Only HKDF + ChaCha20</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature (Red25519)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 signature op</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Similar cost to Ed25519</td></tr>
  </tbody>
</table>

**Size Overhead:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Component</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Frequency</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded public key</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Layer 1 encryption overhead</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes (salt)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Layer 2 encryption overhead</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes (salt)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DH auth per client</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per client per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DH ephemeral pubkey</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet (if DH auth)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">PSK auth per client</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per client per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">PSK salt</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet (if PSK auth)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature</td><td style="border:1px solid var(--color-border); padding:0.5rem;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline sig block</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈100 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet (if offline keys)</td></tr>
  </tbody>
</table>

**Typical Sizes:**

- **No client auth:** ~200 bytes overhead
- **With 10 DH clients:** ~600 bytes overhead
- **With 100 DH clients:** ~4200 bytes overhead

**Optimization Tips:**

1. **Batch key generation:** Generate blinded keys for multiple days in advance
2. **Cache subcredentials:** Compute once per day, reuse for all publications
3. **Reuse ephemeral keys:** Can reuse ephemeral DH key for short period (minutes)
4. **Parallel client encryption:** Encrypt client cookies in parallel
5. **Fast path for no auth:** Skip authorization layer entirely when disabled

### Compatibility

**Backward Compatibility:**

- Ed25519 (type 7) destinations supported for unblinded keys
- Red25519 (type 11) required for blinded keys
- Traditional LeaseSets still fully supported
- Encrypted LeaseSets do not break existing network

**Forward Compatibility:**

- Reserved flag bits for future features
- Extensible authorization scheme (3 bits allow 8 types)
- Version field in various structures

**Interoperability:**

- Java I2P and i2pd fully interoperable since:
  - Java I2P 0.9.40 (May 2019)
  - i2pd 2.58.0 (September 2025)
- Encrypted LeaseSets work across implementations
- Client authorization works across implementations

---

## References

### IETF RFCs

- **[RFC 2104](https://datatracker.ietf.org/doc/html/rfc2104)** - HMAC: Keyed-Hashing for Message Authentication (February 1997)
- **[RFC 5869](https://datatracker.ietf.org/doc/html/rfc5869)** - HMAC-based Extract-and-Expand Key Derivation Function (HKDF) (May 2010)
- **[RFC 7539](https://datatracker.ietf.org/doc/html/rfc7539)** - ChaCha20 and Poly1305 for IETF Protocols (May 2015)
- **[RFC 7748](https://datatracker.ietf.org/doc/html/rfc7748)** - Elliptic Curves for Security (January 2016)

### I2P Specifications

- **[Common Structures Specification](/docs/specs/common-structures/)** - LeaseSet2 and EncryptedLeaseSet structures
- **[Proposal 123: New netDB Entries](/proposals/123-new-netdb-entries/)** - Background and design of LeaseSet2
- **[Proposal 146: Red25519](/proposals/146-red25519/)** - Red25519 signature scheme specification
- **[Proposal 149: B32 for Encrypted LS2](/proposals/149-b32-encrypted-ls2/)** - Base32 addressing for encrypted LeaseSets
- **[Red25519 Specification](/docs/specs/red25519-signature-scheme/)** - Detailed Red25519 implementation
- **[B32 Addressing Specification](/docs/specs/b32-for-encrypted-leasesets/)** - Base32 address format
- **[Network Database Documentation](/docs/specs/common-structures/)** - NetDB usage and operations
- **[I2CP Specification](/docs/specs/i2cp/)** - I2P Client Protocol

### Cryptographic References

- **[Ed25519 Paper](http://cr.yp.to/papers.html#ed25519)** - "High-speed high-security signatures" by Bernstein et al.
- **[ZCash Protocol Specification](https://zips.z.cash/protocol/protocol.pdf)** - Section 5.4.6: RedDSA signature scheme
- **[Tor Rendezvous Specification v3](https://spec.torproject.org/rend-spec)** - Tor's onion service specification (for comparison)

### Security References

- **[Key Blinding Security Discussion](https://lists.torproject.org/pipermail/tor-dev/2013-December/005943.html)** - Tor Project mailing list discussion
- **[Tor Ticket #8106](https://trac.torproject.org/projects/tor/ticket/8106)** - Key blinding implementation discussion
- **[PRNG Security](http://projectbullrun.org/dual-ec/ext-rand.html)** - Random number generator security considerations
- **[Tor PRNG Discussion](https://lists.torproject.org/pipermail/tor-dev/2015-November/009954.html)** - Discussion of PRNG usage in Tor

### Implementation References

- **[Java I2P Repository](https://github.com/i2p/i2p.i2p)** - Official Java implementation
- **[i2pd Repository](https://github.com/PurpleI2P/i2pd)** - C++ implementation
- **[I2P Website](/)** - Official I2P project website
- **[I2P Specifications](/docs/specs/)** - Complete specification index

### Version History

- **[I2P Release Notes](/en/blog)** - Official release announcements
- **[Java I2P Releases](https://github.com/i2p/i2p.i2p/releases)** - GitHub release history
- **[i2pd Releases](https://github.com/PurpleI2P/i2pd/releases)** - GitHub release history

---

## Appendix A: Cryptographic Constants

### Ed25519 / Red25519 Constants

```python
# Ed25519 základní bod (generátor)

B = 2**255 - 19

# Řád Ed25519 (velikost skalárního pole)

L = 2**252 + 27742317777372353535851937790883648493

# Hodnoty typu podpisu

SIGTYPE_ED25519 = 7    # 0x0007 SIGTYPE_RED25519 = 11  # 0x000b

# Délky klíčů

PRIVKEY_SIZE = 32  # bajtů PUBKEY_SIZE = 32   # bajtů SIGNATURE_SIZE = 64  # bajtů

```

### ChaCha20 Constants

```python
# Parametry ChaCha20

CHACHA20_KEY_SIZE = 32   # bajtů (256 bitů) CHACHA20_NONCE_SIZE = 12  # bajtů (96 bitů) CHACHA20_INITIAL_COUNTER = 1  # RFC 7539 povoluje 0 nebo 1

```

### HKDF Constants

```python
# Parametry HKDF (funkce odvozování klíčů založená na HMAC)

HKDF_HASH = "SHA-256" HKDF_SALT_MAX = 32  # bytes (HashLen)

# Řetězce info pro HKDF (funkce odvozování klíčů založená na HMAC) (oddělení domén)

HKDF_INFO_ALPHA = b"i2pblinding1" HKDF_INFO_LAYER1 = b"ELS2_L1K" HKDF_INFO_LAYER2 = b"ELS2_L2K" HKDF_INFO_DH_AUTH = b"ELS2_XCA" HKDF_INFO_PSK_AUTH = b"ELS2PSKA"

```

### Hash Personalization Strings

```python
# Personalizační řetězce pro SHA-256

HASH_PERS_ALPHA = b"I2PGenerateAlpha" HASH_PERS_RED25519 = b"I2P_Red25519H(x)" HASH_PERS_CREDENTIAL = b"credential" HASH_PERS_SUBCREDENTIAL = b"subcredential"

```

### Structure Sizes

```python
# Velikosti vrstvy 0 (vnější)

BLINDED_SIGTYPE_SIZE = 2   # bajty BLINDED_PUBKEY_SIZE = 32   # bajtů (pro Red25519) PUBLISHED_TS_SIZE = 4      # bajty EXPIRES_SIZE = 2           # bajty FLAGS_SIZE = 2             # bajty LEN_OUTER_CIPHER_SIZE = 2  # bajty SIGNATURE_SIZE = 64        # bajtů (Red25519)

# Velikosti bloků offline klíče

OFFLINE_EXPIRES_SIZE = 4   # bajty OFFLINE_SIGTYPE_SIZE = 2   # bajty OFFLINE_SIGNATURE_SIZE = 64  # bajtů

# Velikosti vrstvy 1 (střední)

AUTH_FLAGS_SIZE = 1        # bajt EPHEMERAL_PUBKEY_SIZE = 32  # bajtů (DH autentizace) AUTH_SALT_SIZE = 32        # bajtů (PSK autentizace) NUM_CLIENTS_SIZE = 2       # bajtů CLIENT_ID_SIZE = 8         # bajtů CLIENT_COOKIE_SIZE = 32    # bajtů AUTH_CLIENT_ENTRY_SIZE = 40  # bajtů (CLIENT_ID + CLIENT_COOKIE)

# Režie šifrování

SALT_SIZE = 32  # bajtů (přidáno před každou šifrovanou vrstvu)

# Adresa Base32

B32_ENCRYPTED_DECODED_SIZE = 35  # bajtů B32_ENCRYPTED_ENCODED_LEN = 56   # znaků B32_SUFFIX = ".b32.i2p"

```

---

## Appendix B: Test Vectors

### Test Vector 1: Alpha Generation

**Input:**
```python
# Veřejný klíč cíle (Ed25519)

A = bytes.fromhex('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa') stA = 0x0007  # Ed25519 stA_prime = 0x000b  # Red25519 date = "20251015" secret = ""  # Prázdné tajemství

```

**Computation:**
```python
keydata = A || bytes([0x00, 0x07]) || bytes([0x00, 0x0b])

# keydata = 36 bajtů

salt = SHA256(b"I2PGenerateAlpha" + keydata) ikm = b"20251015" info = b"i2pblinding1"

seed = HKDF(salt, ikm, info, 64) alpha = LEOS2IP(seed) mod L

```

**Expected Output:**
```
(Ověřte podle referenční implementace) alpha = [64bajtová hexadecimální hodnota]

```

### Test Vector 2: ChaCha20 Encryption

**Input:**
```python
key = bytes([i for i in range(32)])  # 0x00..0x1f nonce = bytes([i for i in range(12)])  # 0x00..0x0b plaintext = b"Hello, I2P!"

```

**Computation:**
```python
ciphertext = ChaCha20_Encrypt(key, nonce, plaintext, counter=1)

```

**Expected Output:**
```
ciphertext = [ověřte podle testovacích vektorů RFC 7539]

```

### Test Vector 3: HKDF

**Input:**
```python
salt = bytes(32)  # Samé nuly ikm = b"test input keying material" info = b"ELS2_L1K" n = 44

```

**Computation:**
```python
keys = HKDF(salt, ikm, info, n)

```

**Expected Output:**
```
keys = [44bajtová hexadecimální hodnota]

```

### Test Vector 4: Base32 Address

**Input:**
```python
pubkey = bytes.fromhex('bbbb' + 'bb' * 30)  # 32 bytes unblinded_sigtype = 11  # Red25519 blinded_sigtype = 11    # Red25519

```

**Computation:**
```python
address = generate_encrypted_b32_address(pubkey, unblinded_sigtype, blinded_sigtype)

```

**Expected Output:**
```
address = [56 znaků v base32].b32.i2p

# Ověřte, že se kontrolní součet ověřuje správně

```

---

## Appendix C: Glossary

**Alpha (α):** The secret blinding factor used to blind public and private keys. Generated from the destination, date, and optional secret.

**AuthCookie:** A 32-byte random value encrypted for each authorized client, used as input to Layer 2 encryption.

**B (Base Point):** The generator point for the Ed25519 elliptic curve.

**Blinded Key:** A public or private key that has been transformed using the alpha blinding factor. Blinded keys cannot be linked to the original keys without knowing alpha.

**ChaCha20:** A stream cipher providing fast, secure encryption without requiring AES hardware support.

**ClientID:** An 8-byte identifier derived from HKDF output, used to identify authorization entries for clients.

**ClientCookie:** A 32-byte encrypted value containing the authCookie for a specific client.

**Credential:** A 32-byte value derived from the destination's public key and signature types, binding encryption to knowledge of the destination.

**CSRNG:** Cryptographically Secure Random Number Generator. Must provide unpredictable output suitable for key generation.

**DH (Diffie-Hellman):** A cryptographic protocol for securely establishing shared secrets. I2P uses X25519.

**Ed25519:** An elliptic curve signature scheme providing fast signatures with 128-bit security level.

**Ephemeral Key:** A short-lived cryptographic key, typically used once and then discarded.

**Floodfill:** I2P routers that store and serve network database entries, including encrypted LeaseSets.

**HKDF:** HMAC-based Key Derivation Function, used to derive multiple cryptographic keys from a single source.

**L (Order):** The order of the Ed25519 scalar field (approximately 2^252).

**Layer 0 (Outer):** The plaintext portion of an encrypted LeaseSet, containing blinded key and metadata.

**Layer 1 (Middle):** The first encrypted layer, containing client authorization data.

**Layer 2 (Inner):** The innermost encrypted layer, containing the actual LeaseSet2 data.

**LeaseSet2 (LS2):** Second version of I2P's network database entry format, introducing encrypted variants.

**NetDB:** The I2P network database, a distributed hash table storing router and destination information.

**Offline Keys:** A feature allowing the main signing key to remain in cold storage while a transient key handles daily operations.

**PSK (Pre-Shared Key):** A symmetric key shared in advance between two parties, used for PSK client authorization.

**Red25519:** An Ed25519-based signature scheme with key blinding support, based on ZCash RedDSA.

**Salt:** Random data used as input to key derivation functions to ensure unique outputs.

**SigType:** A numeric identifier for signature algorithms (e.g., 7 = Ed25519, 11 = Red25519).

**Subcredential:** A 32-byte value derived from the credential and blinded public key, binding encryption to a specific encrypted LeaseSet.

**Transient Key:** A temporary signing key used with offline keys, with a limited validity period.

**X25519:** An elliptic curve Diffie-Hellman protocol over Curve25519, providing key agreement.

---

## Document Information

**Status:** This document represents the current stable encrypted LeaseSet specification as implemented in I2P since June 2019. The protocol is mature and widely deployed.

**Contributing:** For corrections or improvements to this documentation, please submit issues or pull requests to the I2P specifications repository.

**Support:** For questions about implementing encrypted LeaseSets:
- I2P Forum: https://i2pforum.net/
- IRC: #i2p-dev on OFTC
- Matrix: #i2p-dev:matrix.org

**Acknowledgments:** This specification builds on work by the I2P development team, ZCash cryptography research, and Tor Project's key blinding research.