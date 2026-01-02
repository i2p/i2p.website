---
title: "Post-kvantové kryptografické protokoly"
number: "169"
author: "zzz, orignal, drzed, eyedeekay"
created: "2025-01-21"
lastupdated: "2025-06-12"
status: "Otevřít"
thread: "http://zzz.i2p/topics/3294"
target: "0.9.80"
toc: true
---

## Přehled

Zatímco výzkum a soutěž o vhodnou post-kvantovou (PQ) kryptografii probíhají již celou dekádu, možnosti se staly jasné teprve nedávno.

Začali jsme zkoumat důsledky PQ kryptografie v roce 2022 [zzz.i2p](http://zzz.i2p/topics/3294).

Standardy TLS přidaly podporu hybridního šifrování v posledních dvou letech a nyní se používá pro významnou část šifrovaného provozu na internetu díky podpoře v Chrome a Firefox [Cloudflare](https://blog.cloudflare.com/pq-2024/).

NIST nedávno dokončil a publikoval doporučené algoritmy pro post-kvantovou kryptografii [NIST](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards). Několik běžných kryptografických knihoven nyní podporuje standardy NIST nebo v blízké budoucnosti vydá tuto podporu.

Jak [Cloudflare](https://blog.cloudflare.com/pq-2024/), tak [NIST](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards) doporučují, aby migrace začala okamžitě. Viz také NSA PQ FAQ z roku 2022 [NSA](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF). I2P by měl být lídrem v oblasti bezpečnosti a kryptografie. Nyní je čas implementovat doporučené algoritmy. Pomocí našeho flexibilního systému typů kryptografie a typů podpisů přidáme typy pro hybridní kryptografii a pro PQ a hybridní podpisy.

## Cíle

- Vybrat algoritmy odolné vůči PQ
- Přidat PQ-only a hybridní algoritmy do I2P protokolů tam, kde je to vhodné
- Definovat více variant
- Vybrat nejlepší varianty po implementaci, testování, analýze a výzkumu
- Přidat podporu postupně a se zpětnou kompatibilitou

## Necíle

- Neměňte jednosměrné (Noise N) šifrovací protokoly
- Neodcházejte od SHA256, není v blízké budoucnosti ohrožen PQ
- Nevybírejte konečné preferované varianty v tuto chvíli

## Model hrozeb

- Routery na OBEP nebo IBGW, možná spolupracující,
  ukládající garlic zprávy pro pozdější dešifrování (forward secrecy)
- Síťoví pozorovatelé
  ukládající transportní zprávy pro pozdější dešifrování (forward secrecy)
- Síťoví účastníci padělající podpisy pro RI, LS, streaming, datagramy,
  nebo jiné struktury

## Ovlivněné protokoly

Upravíme následující protokoly, zhruba v pořadí vývoje. Celkové nasazení proběhne pravděpodobně od konce roku 2025 do poloviny roku 2027. Podrobnosti najdete v sekci Priority a nasazení níže.

| Protocol / Feature | Status |
|--------------------|--------|
| Hybrid MLKEM Ratchet and LS | Approved 2026-06; beta target 2025-08; release target 2025-11 |
| Hybrid MLKEM NTCP2 | Some details to be finalized |
| Hybrid MLKEM SSU2 | Some details to be finalized |
| MLDSA SigTypes 12-14 | Proposal is stable but may not be finalized until 2026 |
| MLDSA Dests | Tested on live net, requires net upgrade for floodfill support |
| Hybrid SigTypes 15-17 | Preliminary |
| Hybrid Dests | |
## Návrh

Budeme podporovat standardy NIST FIPS 203 a 204 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf), které jsou založeny na, ale NEJSOU kompatibilní s, CRYSTALS-Kyber a CRYSTALS-Dilithium (verze 3.1, 3 a starší).

### Key Exchange

Budeme podporovat hybridní výměnu klíčů v následujících protokolech:

| Proto   | Noise Type | Support PQ only? | Support Hybrid? |
|---------|------------|------------------|-----------------|
| NTCP2   | XK         | no               | yes             |
| SSU2    | XK         | no               | yes             |
| Ratchet | IK         | no               | yes             |
| TBM     | N          | no               | no              |
| NetDB   | N          | no               | no              |
PQ KEM poskytuje pouze dočasné klíče a přímo nepodporuje handshaky se statickými klíči, jako jsou Noise XK a IK.

Noise N nepoužívá obousměrnou výměnu klíčů, a proto není vhodný pro hybridní šifrování.

Takže budeme podporovat pouze hybridní šifrování pro NTCP2, SSU2 a Ratchet. Definujeme tři varianty ML-KEM podle [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf), celkem pro 3 nové typy šifrování. Hybridní typy budou definovány pouze v kombinaci s X25519.

Nové typy šifrování jsou:

| Type | Code |
|------|------|
| MLKEM512_X25519 | 5 |
| MLKEM768_X25519 | 6 |
| MLKEM1024_X25519 | 7 |
Režie bude značná. Typické velikosti zpráv 1 a 2 (pro XK a IK) jsou v současnosti kolem 100 bajtů (před jakýmkoli dodatečným payloadem). To se zvýší 8× až 15× v závislosti na algoritmu.

### Signatures

Budeme podporovat PQ a hybridní podpisy v následujících strukturách:

| Type | Support PQ only? | Support Hybrid? |
|------|------------------|-----------------|
| RouterInfo | yes | yes |
| LeaseSet | yes | yes |
| Streaming SYN/SYNACK/Close | yes | yes |
| Repliable Datagrams | yes | yes |
| Datagram2 (prop. 163) | yes | yes |
| I2CP create session msg | yes | yes |
| SU3 files | yes | yes |
| X.509 certificates | yes | yes |
| Java keystores | yes | yes |
Takže budeme podporovat jak PQ-only, tak hybridní podpisy. Definujeme tři varianty ML-DSA podle [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf), tři hybridní varianty s Ed25519 a tři PQ-only varianty s prehash pouze pro SU3 soubory, celkem tedy 9 nových typů podpisů. Hybridní typy budou definovány pouze v kombinaci s Ed25519. Použijeme standardní ML-DSA, NIKOLI varianty pre-hash (HashML-DSA), kromě SU3 souborů.

Použijeme "hedged" neboli randomizovanou variantu podpisování, nikoliv "deterministickou" variantu, jak je definována v [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) sekce 3.4. Tím je zajištěno, že každý podpis je odlišný, i když se týká stejných dat, a poskytuje dodatečnou ochranu proti útokům postranním kanálem. Další podrobnosti o volbách algoritmů včetně kódování a kontextu naleznete v sekci poznámek k implementaci níže.

Nové typy podpisů jsou:

| Type | Code |
|------|------|
| MLDSA44 | 12 |
| MLDSA65 | 13 |
| MLDSA87 | 14 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 |
| MLDSA44ph | 18 |
| MLDSA65ph | 19 |
| MLDSA87ph | 20 |
X.509 certifikáty a další DER kódování budou používat kompozitní struktury a OID definované v [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/).

Režie bude značná. Typické velikosti Ed25519 destination a router identity jsou 391 bajtů. Tyto se zvýší 3,5x až 6,8x v závislosti na algoritmu. Ed25519 podpisy mají 64 bajtů. Tyto se zvýší 38x až 76x v závislosti na algoritmu. Typické podepsané RouterInfo, LeaseSet, odpovědní datagramy a podepsané streaming zprávy mají asi 1KB. Tyto se zvýší 3x až 8x v závislosti na algoritmu.

Protože nové typy identit destinací a routerů nebudou obsahovat výplň, nebudou kompresibilní. Velikosti destinací a identit routerů, které jsou gzipovány při přenosu, se zvýší 12x - 38x v závislosti na algoritmu.

### Legal Combinations

Pro Destinations jsou nové typy podpisů podporovány se všemi typy šifrování v leaseset. Nastavte typ šifrování v certifikátu klíče na NONE (255).

Pro RouterIdentities je typ šifrování ElGamal zastaralý. Nové typy podpisů jsou podporovány pouze se šifrováním X25519 (typ 4). Nové typy šifrování budou označeny v RouterAddresses. Typ šifrování v key certificate bude nadále typ 4.

### New Crypto Required

- ML-KEM (dříve CRYSTALS-Kyber) [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
- ML-DSA (dříve CRYSTALS-Dilithium) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)
- SHA3-128 (dříve Keccak-256) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf) Používá se pouze pro SHAKE128
- SHA3-256 (dříve Keccak-512) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
- SHAKE128 a SHAKE256 (XOF rozšíření pro SHA3-128 a SHA3-256) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)

Testovací vektory pro SHA3-256, SHAKE128 a SHAKE256 jsou dostupné na [NIST](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values).

Poznámka: Java bouncycastle knihovna podporuje všechny výše uvedené. Podpora C++ knihovny je v OpenSSL 3.5 [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

### Alternatives

Nebudeme podporovat [FIPS 205](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.205.pdf) (Sphincs+), je mnohem mnohem pomalejší a větší než ML-DSA. Nebudeme podporovat nadcházející FIPS206 (Falcon), ještě není standardizován. Nebudeme podporovat NTRU nebo jiné PQ kandidáty, které nebyly standardizovány NIST.

### Rosenpass

Existuje nějaký výzkum [paper](https://eprint.iacr.org/2020/379.pdf) o adaptaci Wireguard (IK) pro čistou PQ kryptografii, ale v tomto článku je několik otevřených otázek. Později byl tento přístup implementován jako Rosenpass [Rosenpass](https://rosenpass.eu/) [whitepaper](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf) pro PQ Wireguard.

Rosenpass používá handshake podobný Noise KK s předsdílenými statickými klíči Classic McEliece 460896 (každý 500 KB) a efemérními klíči Kyber-512 (v podstatě MLKEM-512). Jelikož šifrotexty Classic McEliece mají pouze 188 bajtů a veřejné klíče a šifrotexty Kyber-512 mají rozumnou velikost, obě handshake zprávy se vejdou do standardního UDP MTU. Výstupní sdílený klíč (osk) z PQ KK handshake se používá jako vstupní předsdílený klíč (psk) pro standardní Wireguard IK handshake. Celkem tak probíhají dva kompletní handshaky, jeden čistě PQ a jeden čistě X25519.

Nemůžeme nic z toho udělat pro nahrazení našich XK a IK handshake, protože:

- Nemůžeme dělat KK, Bob nemá Alicin statický klíč
- Statické klíče o velikosti 500KB jsou příliš velké
- Nechceme další round-trip

V whitepaperu je mnoho dobrých informací a my si je projdeme pro nápady a inspiraci. TODO.

## Specification

### Výměna klíčů

Aktualizujte sekce a tabulky v dokumentu běžných struktur [/docs/specs/common-structures/](/docs/specs/common-structures/) následovně:

### Podpisy

Nové typy veřejných klíčů jsou:

| Type | Public Key Length | Since | Usage |
|------|-------------------|-------|-------|
| MLKEM512_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM768_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM1024_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM512 | 800 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM768 | 1184 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM1024 | 1568 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM512_CT | 768 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM768_CT | 1088 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM1024_CT | 1568 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| NONE | 0 | 0.9.xx | See proposal 169, for destinations with PQ sig types only, not for RIs or Leasesets |
Hybridní veřejné klíče jsou klíče X25519. Veřejné klíče KEM jsou dočasné PQ klíče odeslané od Alice k Bobovi. Kódování a pořadí bytů jsou definovány v [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

MLKEM*_CT klíče nejsou ve skutečnosti veřejné klíče, jsou to "šifrovaný text" odeslaný od Boba k Alici v Noise handshake. Jsou zde uvedeny pro úplnost.

### Legální kombinace

Nové typy Private Key jsou:

| Type | Private Key Length | Since | Usage |
|------|---------------------|-------|-------|
| MLKEM512_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM768_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM1024_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM512 | 1632 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM768 | 2400 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM1024 | 3168 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
Hybridní privátní klíče jsou X25519 klíče. KEM privátní klíče jsou pouze pro Alice. KEM kódování a pořadí bajtů jsou definovány v [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

### Vyžadována nová kryptografie

Nové typy podpisových veřejných klíčů jsou:

| Type | Length (bytes) | Since | Usage |
|------|----------------|-------|-------|
| MLDSA44 | 1312 | 0.9.xx | See proposal 169 |
| MLDSA65 | 1952 | 0.9.xx | See proposal 169 |
| MLDSA87 | 2592 | 0.9.xx | See proposal 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 1344 | 0.9.xx | See proposal 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 1984 | 0.9.xx | See proposal 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 2624 | 0.9.xx | See proposal 169 |
| MLDSA44ph | 1344 | 0.9.xx | Only for SU3 files, not for netdb structures |
| MLDSA65ph | 1984 | 0.9.xx | Only for SU3 files, not for netdb structures |
| MLDSA87ph | 2624 | 0.9.xx | Only for SU3 files, not for netdb structures |
Hybridní veřejné klíče pro podepisování jsou klíč Ed25519 následovaný PQ klíčem, jak je uvedeno v [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/). Kódování a pořadí bajtů jsou definovány v [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

### Alternativy

Nové typy Signing Private Key jsou:

| Type | Length (bytes) | Since | Usage |
|------|----------------|-------|-------|
| MLDSA44 | 2560 | 0.9.xx | See proposal 169 |
| MLDSA65 | 4032 | 0.9.xx | See proposal 169 |
| MLDSA87 | 4896 | 0.9.xx | See proposal 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2592 | 0.9.xx | See proposal 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 4064 | 0.9.xx | See proposal 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4928 | 0.9.xx | See proposal 169 |
| MLDSA44ph | 2592 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
| MLDSA65ph | 4064 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
| MLDSA87ph | 4928 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
Hybridní podpisové privátní klíče jsou Ed25519 klíč následovaný PQ klíčem, jak je uvedeno v [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/). Kódování a pořadí bajtů jsou definovány v [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

### Rosenpass

Nové typy Signature jsou:

| Type | Length (bytes) | Since | Usage |
|------|----------------|-------|-------|
| MLDSA44 | 2420 | 0.9.xx | See proposal 169 |
| MLDSA65 | 3309 | 0.9.xx | See proposal 169 |
| MLDSA87 | 4627 | 0.9.xx | See proposal 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2484 | 0.9.xx | See proposal 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 3373 | 0.9.xx | See proposal 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4691 | 0.9.xx | See proposal 169 |
| MLDSA44ph | 2484 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
| MLDSA65ph | 3373 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
| MLDSA87ph | 4691 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
Hybridní podpisy jsou podpis Ed25519 následovaný PQ podpisem, jak je uvedeno v [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/). Hybridní podpisy jsou ověřovány ověřením obou podpisů a selhávají, pokud selže kterýkoliv z nich. Kódování a pořadí bajtů jsou definovány v [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

### Key Certificates

Nové typy Signing Public Key jsou:

| Type | Type Code | Total Public Key Length | Since | Usage |
|------|-----------|-------------------------|-------|-------|
| MLDSA44 | 12 | 1312 | 0.9.xx | See proposal 169 |
| MLDSA65 | 13 | 1952 | 0.9.xx | See proposal 169 |
| MLDSA87 | 14 | 2592 | 0.9.xx | See proposal 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 0.9.xx | See proposal 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 0.9.xx | See proposal 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 0.9.xx | See proposal 169 |
| MLDSA44ph | 18 | n/a | 0.9.xx | Only for SU3 files |
| MLDSA65ph | 19 | n/a | 0.9.xx | Only for SU3 files |
| MLDSA87ph | 20 | n/a | 0.9.xx | Only for SU3 files |
Nové typy Crypto Public Key jsou:

| Type | Type Code | Total Public Key Length | Since | Usage |
|------|-----------|-------------------------|-------|-------|
| MLKEM512_X25519 | 5 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM768_X25519 | 6 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM1024_X25519 | 7 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| NONE | 255 | 0 | 0.9.xx | See proposal 169 |
Hybridní typy klíčů NIKDY nejsou zahrnuty v certifikátech klíčů; pouze v leaseSetech.

Pro destinace s hybridními nebo PQ typy podpisů použijte NONE (typ 255) pro typ šifrování, ale není zde žádný kryptografický klíč a celá 384-bajtová hlavní sekce je pro podpisový klíč.

### Běžné struktury

Zde jsou délky pro nové typy Destination. Typ šifrování pro všechny je NONE (typ 255) a délka šifrovacího klíče je považována za 0. Celá 384-bajtová sekce se používá pro první část veřejného podpisového klíče. POZNÁMKA: To se liší od specifikace pro typy podpisů ECDSA_SHA512_P521 a RSA, kde jsme zachovali 256-bajtový ElGamal klíč v destination, i když byl nepoužívaný.

Žádné padding. Celková délka je 7 + celková délka klíče. Délka key certificate je 4 + nadměrná délka klíče.

Příklad 1319-bajtového proudu bajtů destinace pro MLDSA44:

skey[0:383] 5 (932 >> 8) (932 & 0xff) 00 12 00 255 skey[384:1311]

| Type | Type Code | Total Public Key Length | Main | Excess | Total Dest Length |
|------|-----------|-------------------------|------|--------|-------------------|
| MLDSA44 | 12 | 1312 | 384 | 928 | 1319 |
| MLDSA65 | 13 | 1952 | 384 | 1568 | 1959 |
| MLDSA87 | 14 | 2592 | 384 | 2208 | 2599 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 384 | 960 | 1351 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 384 | 1600 | 1991 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 384 | 2240 | 2631 |
### PublicKey

Zde jsou délky pro nové typy Destination. Enc typ pro všechny je X25519 (typ 4). Celá 352-bytová sekce po X25519 veřejném klíči se používá pro první část veřejného klíče pro podpisování. Bez paddingu. Celková délka je 39 + celková délka klíče. Délka key certificate je 4 + přebývající délka klíče.

Příklad 1351-bajtového proudu bajtů router identity pro MLDSA44:

enckey[0:31] skey[0:351] 5 (960 >> 8) (960 & 0xff) 00 12 00 4 skey[352:1311]

| Type | Type Code | Total Public Key Length | Main | Excess | Total RouterIdent Length |
|------|-----------|-------------------------|------|--------|--------------------------|
| MLDSA44 | 12 | 1312 | 352 | 960 | 1351 |
| MLDSA65 | 13 | 1952 | 352 | 1600 | 1991 |
| MLDSA87 | 14 | 2592 | 352 | 2240 | 2631 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 352 | 992 | 1383 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 352 | 1632 | 2023 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 352 | 2272 | 2663 |
### PrivateKey

Handshaky používají [Noise Protocol](https://noiseprotocol.org/noise.html) handshake vzory.

Používá se následující mapování písmen:

- e = jednorázový dočasný klíč
- s = statický klíč
- p = užitečné zatížení zprávy
- e1 = jednorázový dočasný PQ klíč, poslaný od Alice k Bobovi
- ekem1 = KEM šifrový text, poslaný od Boba k Alici

Následující modifikace XK a IK pro hybridní forward secrecy (hfs) jsou specifikovány v [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) sekce 5:

```
XK:                       XKhfs:
  <- s                      <- s
  ...                       ...
  -> e, es, p               -> e, es, e1, p
  <- e, ee, p               <- e, ee, ekem1, p
  -> s, se                  -> s, se
  <- p                      <- p
  p ->                      p ->


  IK:                       IKhfs:
  <- s                      <- s
  ...                       ...
  -> e, es, s, ss, p       -> e, es, e1, s, ss, p
  <- tag, e, ee, se, p     <- tag, e, ee, ekem1, se, p
  <- p                     <- p
  p ->                     p ->

  e1 and ekem1 are encrypted. See pattern definitions below.
  NOTE: e1 and ekem1 are different sizes (unlike X25519)
```
Vzor e1 je definován následovně, jak je specifikováno v [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) sekci 4:

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
Vzor ekem1 je definován následovně, jak je specifikováno v [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) sekci 4:

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
### SigningPublicKey

#### Issues

- Měli bychom změnit hash funkci pro handshake? Viz [comparison](https://kerkour.com/fast-secure-hash-function-sha256-sha512-sha3-blake3).
  SHA256 není zranitelná vůči PQ, ale pokud chceme upgradovat
  naši hash funkci, nyní je ten správný čas, zatímco měníme další věci.
  Aktuální IETF SSH návrh [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-sshm-mlkem-hybrid-kex/) je používat MLKEM768
  s SHA256 a MLKEM1024 s SHA384. Tento návrh zahrnuje
  diskusi bezpečnostních hledisek.
- Měli bychom přestat odesílat 0-RTT ratchet data (kromě LS)?
- Měli bychom přepnout ratchet z IK na XK, pokud neodesíláme 0-RTT data?

#### Overview

Tato sekce se vztahuje na protokoly IK i XK.

Hybridní handshake je definován v [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf). První zpráva, od Alice k Bobovi, obsahuje e1, enkapsulační klíč, před datovou částí zprávy. Tento je považován za dodatečný statický klíč; zavolejte na něj EncryptAndHash() (jako Alice) nebo DecryptAndHash() (jako Bob). Poté zpracujte datovou část zprávy jako obvykle.

Druhá zpráva, od Boba k Alici, obsahuje ekem1, šifrovaný text, před užitečným obsahem zprávy. To je považováno za dodatečný statický klíč; zavolejte na něj EncryptAndHash() (jako Bob) nebo DecryptAndHash() (jako Alice). Poté vypočítejte kem_shared_key a zavolejte MixKey(kem_shared_key). Následně zpracujte užitečný obsah zprávy jako obvykle.

#### Defined ML-KEM Operations

Definujeme následující funkce odpovídající kryptografickým stavebním blokům použitým podle definice v [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

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

Všimněte si, že jak encap_key, tak ciphertext jsou šifrovány uvnitř ChaCha/Poly bloků ve zprávách 1 a 2 Noise handshake. Budou dešifrovány jako součást procesu handshake.

kem_shared_key se smíchá do řetězícího klíče pomocí MixHash(). Podrobnosti viz níže.

#### Alice KDF for Message 1

Pro XK: Po vzoru zprávy 'es' a před payload, přidejte:

NEBO

Pro IK: Po vzoru zprávy 'es' a před vzorem zprávy 's' přidejte:

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
#### Bob KDF for Message 1

Pro XK: Po message patternu 'es' a před payload, přidat:

NEBO

Pro IK: Po message patternu 'es' a před message patternem 's' přidejte:

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
#### Bob KDF for Message 2

Pro XK: Po vzoru zprávy 'ee' a před payload, přidej:

NEBO

Pro IK: Po vzoru zprávy 'ee' a před vzorem zprávy 'se' přidejte:

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
#### Alice KDF for Message 2

Po vzoru zprávy 'ee' (a před vzorem zprávy 'ss' pro IK), přidejte:

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
#### KDF for Message 3 (XK only)

nezměněno

#### KDF for split()

nezměněno

### SigningPrivateKey

Aktualizujte specifikaci ECIES-Ratchet [/docs/specs/ecies/](/docs/specs/ecies/) následovně:

#### Noise identifiers

- "Noise_IKhfselg2_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM1024_ChaChaPoly_SHA256"

#### 1b) New session format (with binding)

Změny: Současný ratchet obsahoval statický klíč v první ChaCha sekci a payload ve druhé sekci. S ML-KEM jsou nyní tři sekce. První sekce obsahuje šifrovaný PQ veřejný klíč. Druhá sekce obsahuje statický klíč. Třetí sekce obsahuje payload.

Šifrovaný formát:

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
  +           ML-KEM encap_key            +
  |       ChaCha20 encrypted data         |
  +      (see table below for length)     +
  |                                       |
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +    (MAC) for encap_key Section        +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +           X25519 Static Key           +
  |       ChaCha20 encrypted data         |
  +             32 bytes                  +
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
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) for Payload Section     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
```
Dešifrovaný formát:

```
Payload Part 1:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +       ML-KEM encap_key                +
  |                                       |
  +      (see table below for length)     +
  |                                       |
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Payload Part 2:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +       X25519 Static Key               +
  |                                       |
  +      (32 bytes)                       +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+

  Payload Part 3:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |                                       |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
```
Velikosti:

| Type | Type Code | X len | Msg 1 len | Msg 1 Enc len | Msg 1 Dec len | PQ key len | pl len |
|------|-----------|-------|-----------|---------------|---------------|------------|--------|
| X25519 | 4 | 32 | 96+pl | 64+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 912+pl | 880+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1296+pl | 1360+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1680+pl | 1648+pl | 1568+pl | 1568 | pl |
Všimněte si, že payload musí obsahovat DateTime blok, takže minimální velikost payload je 7. Minimální velikosti zpráv typu 1 mohou být vypočítány odpovídajícím způsobem.

#### 1g) New Session Reply format

Změny: Současný ratchet má prázdný payload pro první ChaCha sekci a payload ve druhé sekci. S ML-KEM jsou nyní tři sekce. První sekce obsahuje zašifrovaný PQ ciphertext. Druhá sekce má prázdný payload. Třetí sekce obsahuje payload.

Šifrovaný formát:

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
  |                                       |
  +                                       +
  | ChaCha20 encrypted ML-KEM ciphertext  |
  +      (see table below for length)     +
  ~                                       ~
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +  (MAC) for ciphertext Section         +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +  (MAC) for key Section (no data)      +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |       ChaCha20 encrypted data         |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) for Payload Section     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
```
Dešifrovaný formát:

```
Payload Part 1:


  +----+----+----+----+----+----+----+----+
  |                                       |
  +       ML-KEM ciphertext               +
  |                                       |
  +      (see table below for length)     +
  |                                       |
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Payload Part 2:

  empty

  Payload Part 3:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |                                       |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
```
Velikosti:

| Type | Type Code | Y len | Msg 2 len | Msg 2 Enc len | Msg 2 Dec len | PQ CT len | opt len |
|------|-----------|-------|-----------|---------------|---------------|-----------|---------|
| X25519 | 4 | 32 | 72+pl | 32+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 856+pl | 816+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1176+pl | 1136+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1656+pl | 1616+pl | 1568+pl | 1568 | pl |
Upozorňujeme, že zatímco zpráva 2 bude normálně mít nenulový payload, specifikace ratchet [/docs/specs/ecies/](/docs/specs/ecies/) to nevyžaduje, takže minimální velikost payload je 0. Minimální velikosti zprávy 2 mohou být vypočítány odpovídajícím způsobem.

### Podpis

Aktualizujte specifikaci NTCP2 [/docs/specs/ntcp2/](/docs/specs/ntcp2/) následovně:

#### Noise identifiers

- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM1024_ChaChaPoly_SHA256"

#### 1) SessionRequest

Změny: Současný NTCP2 obsahuje pouze možnosti v sekci ChaCha. S ML-KEM bude sekce ChaCha také obsahovat zašifrovaný PQ veřejný klíč.

Nezpracovaný obsah:

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
  |   ChaChaPoly frame (MLKEM)            |
  +      (see table below for length)     +
  |   k defined in KDF for message 1      |
  +   n = 0                               +
  |   see KDF for associated data         |
  ~   n = 0                               ~
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaChaPoly frame (options)          |
  +         32 bytes                      +
  |   k defined in KDF for message 1      |
  +   n = 0                               +
  |   see KDF for associated data         |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  ~         padding (optional)            ~
  |     length defined in options block   |
  +----+----+----+----+----+----+----+----+

  Same as before except add a second ChaChaPoly frame
```
Nešifrovaná data (Poly1305 autentizační tag není zobrazen):

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
  |           ML-KEM encap_key            |
  +      (see table below for length)     +
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
```
Velikosti:

| Type | Type Code | X len | Msg 1 len | Msg 1 Enc len | Msg 1 Dec len | PQ key len | opt len |
|------|-----------|-------|-----------|---------------|---------------|------------|---------|
| X25519 | 4 | 32 | 64+pad | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 880+pad | 848 | 816 | 800 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1264+pad | 1232 | 1200 | 1184 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1648+pad | 1616 | 1584 | 1568 | 16 |
Poznámka: Kódy typů jsou určeny pouze pro interní použití. Routery zůstanou typ 4 a podpora bude uvedena v adresách routerů.

#### 2) SessionCreated

Změny: Současný NTCP2 obsahuje pouze možnosti v sekci ChaCha. S ML-KEM bude sekce ChaCha také obsahovat šifrovaný PQ veřejný klíč.

Nezpracovaný obsah:

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
  |   ChaChaPoly frame (MLKEM)            |
  +   Encrypted and authenticated data    +
  -      (see table below for length)     -
  +   k defined in KDF for message 2      +
  |   n = 0; see KDF for associated data  |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaChaPoly frame (options)          |
  +   Encrypted and authenticated data    +
  -           32 bytes                    -
  +   k defined in KDF for message 2      +
  |   n = 0; see KDF for associated data  |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  +         padding (optional)            +
  |     length defined in options block   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Same as before except add a second ChaChaPoly frame
```
Nešifrovaná data (Poly1305 auth tag nezobrazeno):

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
  |           ML-KEM Ciphertext           |
  +      (see table below for length)     +
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
```
Velikosti:

| Type | Type Code | Y len | Msg 2 len | Msg 2 Enc len | Msg 2 Dec len | PQ CT len | opt len |
|------|-----------|-------|-----------|---------------|---------------|-----------|---------|
| X25519 | 4 | 32 | 64+pad | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 848+pad | 816 | 784 | 768 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1136+pad | 1104 | 1104 | 1088 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1616+pad | 1584 | 1584 | 1568 | 16 |
Poznámka: Kódy typů jsou pouze pro interní použití. Routery zůstanou typ 4 a podpora bude označena v adresách routerů.

#### 3) SessionConfirmed

Nezměněno

#### Key Derivation Function (KDF) (for data phase)

Nezměněno

### Certifikáty klíčů

Aktualizujte specifikaci SSU2 [/docs/specs/ssu2/](/docs/specs/ssu2/) následovně:

#### Noise identifiers

- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM1024_ChaChaPoly_SHA256"

#### Long Header

Dlouhá hlavička má 32 bajtů. Používá se před vytvořením relace, pro Token Request, SessionRequest, SessionCreated a Retry. Používá se také pro zprávy Peer Test a Hole Punch mimo relaci.

TODO: Interně bychom mohli použít pole verze a použít 3 pro MLKEM512 a 4 pro MLKEM768. Děláme to pouze pro typy 0 a 1 nebo pro všech 6 typů?

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

  ver :: The protocol version, equal to 2
         TODO We could internally use the version field and use 3 for MLKEM512 and 4 for MLKEM768.

  id :: 1 byte, the network ID (currently 2, except for test networks)

  flag :: 1 byte, unused, set to 0 for future compatibility

  Source Connection ID :: 8 bytes, unsigned big endian integer

  Token :: 8 bytes, unsigned big endian integer

```
#### Short Header

nezměněno

#### SessionRequest (Type 0)

Změny: Současné SSU2 obsahuje v sekci ChaCha pouze data bloků. S ML-KEM bude sekce ChaCha také obsahovat zašifrovaný PQ veřejný klíč.

Surový obsah:

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
  +                                       +
  |   ChaCha20 encrypted data (payload)   |
  +          (length varies)              +
  |  k defined in KDF for Session Request |
  +  n = 0                                +
  |  see KDF for associated data          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
Nešifrovaná data (Poly1305 autentizační tag není zobrazen):

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
Velikosti, nezahrnují IP overhead:

| Type | Type Code | X len | Msg 1 len | Msg 1 Enc len | Msg 1 Dec len | PQ key len | pl len |
|------|-----------|-------|-----------|---------------|---------------|------------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 896+pl | 832+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1280+pl | 1216+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | n/a | too big | | | | |
Poznámka: Kódy typů jsou pouze pro interní použití. Routery zůstanou typu 4 a podpora bude uvedena v adresách routerů.

Minimální MTU pro MLKEM768_X25519: Přibližně 1316 pro IPv4 a 1336 pro IPv6.

#### SessionCreated (Type 1)

Změny: Současné SSU2 obsahuje pouze data bloku v sekci ChaCha. S ML-KEM bude sekce ChaCha obsahovat také šifrovaný PQ veřejný klíč.

Surový obsah:

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
  |  n = 0; see KDF for associated data   |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 data (payload)             |
  +   Encrypted and authenticated data    +
  |  length varies                        |
  +  k defined in KDF for Session Created +
  |  n = 0; see KDF for associated data   |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
Nešifrovaná data (Poly1305 autentizační tag není zobrazen):

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
Velikosti, bez započítání IP overhead:

| Type | Type Code | Y len | Msg 2 len | Msg 2 Enc len | Msg 2 Dec len | PQ CT len | pl len |
|------|-----------|-------|-----------|---------------|---------------|-----------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 864+pl | 800+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1184+pl | 1118+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | n/a | too big | | | | |
Poznámka: Kódy typů jsou určeny pouze pro interní použití. Routery zůstanou typu 4 a podpora bude uvedena v adresách routerů.

Minimální MTU pro MLKEM768_X25519: Přibližně 1316 pro IPv4 a 1336 pro IPv6.

#### SessionConfirmed (Type 2)

nezměněno

#### KDF for data phase

nezměněno

#### Problémy

Relay bloky, Peer Test bloky a Peer Test zprávy všechny obsahují podpisy. Bohužel PQ podpisy jsou větší než MTU. V současnosti neexistuje žádný mechanismus pro fragmentaci Relay nebo Peer Test bloků či zpráv napříč více UDP pakety. Protokol musí být rozšířen o podporu fragmentace. To bude provedeno v samostatném návrhu TBD. Dokud nebude dokončeno, Relay a Peer Test nebudou podporovány.

#### Přehled

Interně bychom mohli použít pole version a použít 3 pro MLKEM512 a 4 pro MLKEM768.

Pro zprávy 1 a 2 by MLKEM768 zvýšil velikosti paketů nad minimální MTU 1280. Pravděpodobně by se pro takové spojení jednoduše nepodporovalo, pokud by bylo MTU příliš nízké.

Pro zprávy 1 a 2 by MLKEM1024 zvýšilo velikost paketů nad maximální MTU 1500. To by vyžadovalo fragmentaci zpráv 1 a 2 a byla by to velká komplikace. Pravděpodobně se to nebude dělat.

Relay a Peer Test: Viz výše

### Velikosti destinací

TODO: Existuje efektivnější způsob, jak definovat podepisování/ověřování, aby se předešlo kopírování podpisu?

### Velikosti RouterIdent

TODO

[IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/) sekce 8.1 zakazuje HashML-DSA v X.509 certifikátech a nepřiřazuje OID pro HashML-DSA kvůli implementačním složitostem a snížené bezpečnosti.

Pro PQ-only podpisy SU3 souborů používejte OID definované v [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/) pro non-prehash varianty certifikátů. Nedefinujeme hybridní podpisy SU3 souborů, protože bychom mohli muset hashovat soubory dvakrát (ačkoliv HashML-DSA a X2559 používají stejnou hash funkci SHA512). Také by zřetězení dvou klíčů a podpisů v X.509 certifikátu bylo zcela nestandardní.

Upozorňujeme, že zakazujeme Ed25519 podepisování SU3 souborů, a ačkoli jsme definovali Ed25519ph podepisování, nikdy jsme se nedohodli na OID pro něj ani ho nepoužívali.

Normální typy sig jsou pro soubory SU3 zakázané; použijte varianty ph (prehash).

### Vzory handshaku

Nová maximální velikost Destination bude 2599 (3468 v base 64).

Aktualizovat další dokumenty, které poskytují pokyny k velikostem Destination, včetně:

- SAMv3
- Bittorrent
- Pokyny pro vývojáře
- Pojmenování / adresář / jump servery
- Další dokumentace

## Overhead Analysis

### Noise Handshake KDF

Zvětšení velikosti (bajty):

| Type | Pubkey (Msg 1) | Cipertext (Msg 2) |
|------|----------------|-------------------|
| MLKEM512_X25519 | +816 | +784 |
| MLKEM768_X25519 | +1200 | +1104 |
| MLKEM1024_X25519 | +1584 | +1584 |
Rychlost:

Rychlosti podle zprávy [Cloudflare](https://blog.cloudflare.com/pq-2024/):

| Type | Relative speed |
|------|----------------|
| X25519 DH/keygen | baseline |
| MLKEM512 | 2.25x faster |
| MLKEM768 | 1.5x faster |
| MLKEM1024 | 1x (same) |
| XK | 4x DH (keygen + 3 DH) |
| MLKEM512_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 4.9x DH = 22% slower |
| MLKEM768_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 5.3x DH = 32% slower |
| MLKEM1024_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 6x DH = 50% slower |
Předběžné výsledky testů v Javě:

| Type | Relative DH/encaps | DH/decaps | keygen |
|------|-------------------|-----------|--------|
| X25519 | baseline | baseline | baseline |
| MLKEM512 | 29x faster | 22x faster | 17x faster |
| MLKEM768 | 17x faster | 14x faster | 9x faster |
| MLKEM1024 | 12x faster | 10x faster | 6x faster |
### Signatures

Velikost:

Typické velikosti klíčů, podpisů, RIdent, Dest nebo zvýšení velikosti (Ed25519 uveden pro referenci) za předpokladu typu šifrování X25519 pro RI. Přidaná velikost pro Router Info, LeaseSet, odpověditelné datagramy a každý ze dvou streaming (SYN a SYN ACK) paketů uvedených. Současné Destinations a Leasesets obsahují opakované vyplnění a jsou kompresovatelné během přenosu. Nové typy neobsahují vyplnění a nebudou kompresovatelné, což má za následek mnohem vyšší zvýšení velikosti během přenosu. Viz sekce návrhu výše.

| Type | Pubkey | Sig | Key+Sig | RIdent | Dest | RInfo | LS/Streaming/Datagram (each msg) |
|------|--------|-----|---------|--------|------|-------|----------------------------------|
| EdDSA_SHA512_Ed25519 | 32 | 64 | 96 | 391 | 391 | baseline | baseline |
| MLDSA44 | 1312 | 2420 | 3732 | 1351 | 1319 | +3316 | +3284 |
| MLDSA65 | 1952 | 3309 | 5261 | 1991 | 1959 | +5668 | +5636 |
| MLDSA87 | 2592 | 4627 | 7219 | 2631 | 2599 | +7072 | +7040 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 1344 | 2484 | 3828 | 1383 | 1351 | +3412 | +3380 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 1984 | 3373 | 5357 | 2023 | 1991 | +5668 | +5636 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 2624 | 4691 | 7315 | 2663 | 2631 | +7488 | +7456 |
Rychlost:

Rychlosti dle zprávy na [Cloudflare](https://blog.cloudflare.com/pq-2024/):

| Type | Relative speed sign | verify |
|------|---------------------|--------|
| EdDSA_SHA512_Ed25519 | baseline | baseline |
| MLDSA44 | 5x slower | 2x faster |
| MLDSA65 | ??? | ??? |
| MLDSA87 | ??? | ??? |
Předběžné výsledky testů v Javě:

| Type | Relative speed sign | verify | keygen |
|------|---------------------|--------|--------|
| EdDSA_SHA512_Ed25519 | baseline | baseline | baseline |
| MLDSA44 | 4.6x slower | 1.7x faster | 2.6x faster |
| MLDSA65 | 8.1x slower | same | 1.5x faster |
| MLDSA87 | 11.1x slower | 1.5x slower | same |
## Security Analysis

Bezpečnostní kategorie NIST jsou shrnuty v [NIST presentation](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf) slide 10. Předběžná kritéria: Naše minimální bezpečnostní kategorie NIST by měla být 2 pro hybridní protokoly a 3 pro PQ-only.

| Category | As Secure As |
|----------|--------------|
| 1 | AES128 |
| 2 | SHA256 |
| 3 | AES192 |
| 4 | SHA384 |
| 5 | AES256 |
### Handshakes

Všechny tyto protokoly jsou hybridní. Pravděpodobně je třeba upřednostnit MLKEM768; MLKEM512 není dostatečně bezpečný.

Bezpečnostní kategorie NIST [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf):

| Algorithm | Security Category |
|-----------|-------------------|
| MLKEM512 | 1 |
| MLKEM768 | 3 |
| MLKEM1024 | 5 |
### Signatures

Tento návrh definuje jak hybridní, tak čistě PQ typy podpisů. MLDSA44 hybridní je vhodnější než MLDSA65 čistě PQ. Velikosti klíčů a podpisů pro MLDSA65 a MLDSA87 jsou pro nás pravděpodobně příliš velké, alespoň zpočátku.

Bezpečnostní kategorie NIST [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf):

| Algorithm | Security Category |
|-----------|-------------------|
| MLDSA44 | 2 |
| MLKEM67 | 3 |
| MLKEM87 | 5 |
## Type Preferences

Zatímco budeme definovat a implementovat 3 krypto a 9 typů podpisů, plánujeme měřit výkon během vývoje a dále analyzovat účinky zvětšených velikostí struktur. Budeme také pokračovat ve výzkumu a sledování vývoje v jiných projektech a protokolech.

Po roce nebo více vývoje se pokusíme usadit na preferovaném typu nebo výchozím nastavení pro každý případ použití. Výběr bude vyžadovat kompromisy mezi šířkou pásma, CPU a odhadovanou úrovní zabezpečení. Ne všechny typy nemusí být vhodné nebo povolené pro všechny případy použití.

Předběžné preference jsou následující, mohou se změnit:

Šifrování: MLKEM768_X25519

Podpisy: MLDSA44_EdDSA_SHA512_Ed25519

Předběžná omezení jsou následující a mohou se změnit:

Šifrování: MLKEM1024_X25519 není povoleno pro SSU2

Podpisy: MLDSA87 a hybridní varianta pravděpodobně příliš velké; MLDSA65 a hybridní varianta mohou být příliš velké

## Implementation Notes

### Library Support

Knihovny Bouncycastle, BoringSSL a WolfSSL nyní podporují MLKEM a MLDSA. Podpora OpenSSL bude v jejich vydání 3.5 dne 8. dubna 2025 [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

Noise knihovna ze southernstorm.com adaptovaná pro Java I2P obsahovala předběžnou podporu pro hybridní handshaky, ale odstranili jsme ji jako nepoužívanou; budeme ji muset přidat zpět a aktualizovat tak, aby odpovídala [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf).

### Signing Variants

Použijeme variantu "hedged" nebo randomizovaného podepisování, nikoliv "deterministickou" variantu, jak je definováno v [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) sekce 3.4. Tím je zajištěno, že každý podpis je odlišný, i když je nad stejnými daty, a poskytuje dodatečnou ochranu proti útokům pomocí postranních kanálů. Zatímco [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) specifikuje, že varianta "hedged" je výchozí, to nemusí být pravda v různých knihovnách. Implementátoři musí zajistit, aby byla pro podepisování použita varianta "hedged".

Používáme normální proces podepisování (nazývaný Pure ML-DSA Signature Generation), který kóduje zprávu interně jako 0x00 || len(ctx) || ctx || message, kde ctx je nějaká volitelná hodnota o velikosti 0x00..0xFF. Nepoužíváme žádný volitelný kontext. len(ctx) == 0. Tento proces je definován v [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) Algoritmus 2 krok 10 a Algoritmus 3 krok 5. Upozorňujeme, že některé publikované testovací vektory mohou vyžadovat nastavení režimu, kde zpráva není kódována.

### Reliability

Zvětšení velikosti bude mít za následek mnohem více fragmentace tunelů pro NetDB úložiště, streaming handshake a další zprávy. Zkontrolujte změny výkonu a spolehlivosti.

### Structure Sizes

Najděte a zkontrolujte jakýkoli kód, který omezuje velikost v bajtech router infos a leasesetů.

### NetDB

Zkontrolovat a případně snížit maximum LS/RI uložených v RAM nebo na disku, aby se omezil nárůst úložiště. Zvýšit minimální požadavky na šířku pásma pro floodfilly?

### Ratchet

#### Definované operace ML-KEM

Automatická klasifikace/detekce více protokolů na stejných tunelech by měla být možná na základě kontroly délky zprávy 1 (New Session Message). Při použití MLKEM512_X25519 jako příkladu je délka zprávy 1 o 816 bytů větší než u současného ratchet protokolu a minimální velikost zprávy 1 (pouze s DateTime payloadem) je 919 bytů. Většina velikostí zpráv 1 u současného ratchet má payload menší než 816 bytů, takže mohou být klasifikovány jako nehybridní ratchet. Velké zprávy jsou pravděpodobně POST požadavky, které jsou vzácné.

Doporučená strategie je tedy:

- Pokud je zpráva 1 menší než 919 bajtů, jedná se o současný ratchet protokol.
- Pokud je zpráva 1 větší nebo rovna 919 bajtům, pravděpodobně se jedná o MLKEM512_X25519.
  Zkuste nejprve MLKEM512_X25519, a pokud selže, zkuste současný ratchet protokol.

Toto by nám mělo umožnit efektivně podporovat standardní ratchet a hybridní ratchet na stejné destinaci, stejně jako jsme dříve podporovali ElGamal a ratchet na stejné destinaci. Proto můžeme migrovat na MLKEM hybridní protokol mnohem rychleji, než kdybychom nemohli podporovat duální protokoly pro stejnou destinaci, protože můžeme přidat podporu MLKEM do existujících destinací.

Požadované podporované kombinace jsou:

- X25519 + MLKEM512
- X25519 + MLKEM768
- X25519 + MLKEM1024

Následující kombinace mohou být složité a NENÍ vyžadováno, aby byly podporovány, ale mohou být, v závislosti na implementaci:

- Více než jeden MLKEM
- ElG + jeden nebo více MLKEM
- X25519 + jeden nebo více MLKEM
- ElG + X25519 + jeden nebo více MLKEM

Nemusíme se pokoušet podporovat více MLKEM algoritmů (například MLKEM512_X25519 a MLKEM_768_X25519) na stejné destinaci. Vyberte pouze jeden; to však závisí na tom, že vybereme preferovanou MLKEM variantu, aby ji mohly používat HTTP klientské tunnely. Závislé na implementaci.

MŮŽEME se pokusit podporovat tři algoritmy (například X25519, MLKEM512_X25519 a MLKEM769_X25519) na stejné destinaci. Klasifikace a strategie opakování mohou být příliš složité. Konfigurace a konfigurační UI mohou být příliš složité. Závislé na implementaci.

Pravděpodobně se NEBUDEME pokoušet podporovat ElGamal a hybridní algoritmy na stejné destinaci. ElGamal je zastaralý a ElGamal + hybridní pouze (bez X25519) nedává velký smysl. Také ElGamal a Hybrid New Session Messages jsou oba velké, takže klasifikační strategie by často musely zkusit oba typy dešifrování, což by bylo neefektivní. Závislé na implementaci.

Klienti mohou používat stejné nebo odlišné X25519 statické klíče pro X25519 a hybridní protokoly na stejných tunnelech, závisí na implementaci.

#### Alice KDF pro Zprávu 1

Specifikace ECIES umožňuje Garlic Messages v datové části New Session Message, což umožňuje 0-RTT doručení počátečního streamovacího paketu, obvykle HTTP GET, společně s leaseset klienta. Avšak datová část New Session Message nemá dopřednou bezpečnost (forward secrecy). Protože tento návrh zdůrazňuje vylepšenou dopřednou bezpečnost pro ratchet, implementace mohou nebo by měly odložit zahrnutí streamovací datové části nebo úplné streamovací zprávy až do první Existing Session Message. To by bylo na úkor 0-RTT doručení. Strategie mohou také záviset na typu provozu nebo typu tunelu, nebo například na GET vs. POST. Závislé na implementaci.

#### Bob KDF pro Zprávu 1

MLKEM, MLDSA, nebo obojí na stejné destinaci dramaticky zvýší velikost New Session Message, jak je popsáno výše. To může významně snížit spolehlivost doručování New Session Message prostřednictvím tunelů, kde musí být fragmentovány do více 1024 bajtových tunelových zpráv. Úspěšnost doručení je úměrná exponenciálnímu počtu fragmentů. Implementace mohou používat různé strategie k omezení velikosti zprávy na úkor 0-RTT doručení. Závislé na implementaci.

### Ratchet

Můžeme nastavit MSB efemérního klíče (key[31] & 0x80) v session request, abychom označili, že se jedná o hybridní spojení. To by nám umožnilo provozovat jak standardní NTCP, tak hybridní NTCP na stejném portu. Podporována by byla pouze jedna hybridní varianta a inzerována v router address. Například v=2,3 nebo v=2,4 nebo v=2,5.

Pokud to neuděláme, potřebujeme jinou transportní adresu/port a nový název protokolu jako "NTCP1PQ1".

Poznámka: Kódy typů jsou pouze pro interní použití. Routery zůstanou typu 4 a podpora bude označena v adresách routerů.

TODO

### SSU2

MOŽNÁ Potřebuje jinou transportní adresu/port, ale doufejme, že ne, máme hlavičku s příznaky pro zprávu 1. Mohli bychom interně použít pole verze a použít 3 pro MLKEM512 a 4 pro MLKEM768. Možná by stačilo jen v=2,3,4 v adrese. Ale potřebujeme identifikátory pro oba nové algoritmy: 3a, 3b?

Zkontrolujte a ověřte, že SSU2 dokáže zpracovat RI fragmentované napříč více pakety (6-8?). i2pd aktuálně podporuje pouze maximum 2 fragmenty?

Poznámka: Kódy typů jsou pouze pro interní použití. Routery zůstanou typu 4 a podpora bude označena v adresách routeru.

TODO

## Router Compatibility

### Transport Names

Pravděpodobně nebudeme potřebovat nové názvy transportů, pokud budeme moci provozovat jak standardní, tak hybridní na stejném portu s version flags.

Pokud budeme potřebovat nové názvy transportů, budou to:

| Transport | Type |
|-----------|------|
| NTCP2PQ1 | MLKEM512_X25519 |
| NTCP2PQ2 | MLKEM768_X25519 |
| NTCP2PQ3 | MLKEM1024_X25519 |
| SSU2PQ1 | MLKEM512_X25519 |
| SSU2PQ2 | MLKEM768_X25519 |
Všimněte si, že SSU2 nemůže podporovat MLKEM1024, je příliš velký.

### Router Enc. Types

Máme několik alternativ k zvážení:

#### Bob KDF pro zprávu 2

Nedoporučuje se. Používejte pouze nové transporty uvedené výše, které odpovídají typu routeru. Starší routery se nemohou připojit, stavět tunely skrz ně nebo jim posílat netDb zprávy. Trvalo by několik vývojových cyklů ladění a zajištění podpory před povolením jako výchozí. Mohlo by to prodloužit zavádění o rok nebo více oproti alternativám uvedeným níže.

#### Alice KDF pro Message 2

Doporučeno. Protože PQ neovlivňuje statický klíč X25519 ani handshake protokoly N, mohli bychom ponechat routery jako typ 4 a pouze inzerovat nové transporty. Starší routery by se stále mohly připojovat, budovat tunely skrz ně nebo jim posílat netDb zprávy.

#### KDF pro Zprávu 3 (pouze XK)

Routery typu 4 mohou inzerovat jak NTCP2, tak NTCP2PQ* adresy. Ty mohou používat stejný statický klíč a další parametry, nebo ne. Tyto budou pravděpodobně muset být na různých portech; bylo by velmi obtížné podporovat jak NTCP2, tak NTCP2PQ* protokoly na stejném portu, protože neexistuje žádná hlavička nebo rámování, které by Bobovi umožnilo klasifikovat a zarámovat příchozí zprávu Session Request.

Oddělené porty a adresy budou obtížné pro Java, ale jednoduché pro i2pd.

#### KDF pro split()

Type 4 routery by mohly inzerovat jak SSU2, tak SSU2PQ* adresy. S přidanými hlavičkovými příznaky by Bob mohl identifikovat příchozí typ transportu v první zprávě. Proto bychom mohli podporovat jak SSU2, tak SSUPQ* na stejném portu.

Tyto by mohly být publikovány jako samostatné adresy (jak to i2pd dělalo při předchozích přechodech) nebo ve stejné adrese s parametrem indikujícím PQ podporu (jak to Java i2p dělalo při předchozích přechodech).

Pokud se nachází na stejné adrese nebo na stejném portu v různých adresách, použily by stejný statický klíč a další parametry. Pokud se nachází na různých adresách s různými porty, mohly by používat stejný statický klíč a další parametry, nebo nemusí.

Oddělené porty a adresy budou obtížné pro Javu, ale jednoduché pro i2pd.

#### Recommendations

TODO

### NTCP2

#### Identifikátory Noise

Starší routery ověřují RI a proto se nemohou připojit, stavět tunely přes ně, nebo jim posílat netDb zprávy. Vyžadovalo by několik vývojových cyklů na ladění a zajištění podpory před povolením ve výchozím nastavení. Byly by to stejné problémy jako při zavádění enc. typu 5/6/7; mohlo by prodloužit zavádění o rok nebo více oproti alternativě zavádění enc. typu 4 uvedené výše.

Žádné alternativy.

### LS Enc. Types

#### 1b) Nový formát relace (s vazbou)

Tyto mohou být přítomny v LS se staršími klíči typu 4 X25519. Starší routery neznámé klíče ignorují.

Destinations mohou podporovat více typů klíčů, ale pouze prostřednictvím zkušebního dešifrování zprávy 1 s každým klíčem. Režie může být zmírněna udržováním počtu úspěšných dešifrování pro každý klíč a nejprve zkušením nejpoužívanějšího klíče. Java I2P používá tuto strategii pro ElGamal+X25519 na stejné destination.

### Dest. Sig. Types

#### 1g) Formát New Session Reply

Routery ověřují podpisy leaseset a proto se nemohou připojit nebo přijímat leaseset pro destinace typu 12-17. Trvalo by několik cyklů vydání na ladění a zajištění podpory před výchozím povolením.

Žádné alternativy.

## Specifikace

Nejcennější data jsou end-to-end provoz, zašifrovaný pomocí ratchet. Jako externí pozorovatel mezi skoky tunelu je to zašifrováno ještě dvakrát více, pomocí šifrování tunelu a transportního šifrování. Jako externí pozorovatel mezi OBEP a IBGW je to zašifrováno pouze jednou více, pomocí transportního šifrování. Jako účastník OBEP nebo IBGW je ratchet jediné šifrování. Nicméně, protože tunely jsou jednosměrné, zachycení obou zpráv v ratchet handshake by vyžadovalo spolupracující routery, pokud by tunely nebyly postaveny s OBEP a IBGW na stejném routeru.

Nejzávažnějším PQ modelem hrozby je v současnosti ukládání provozu dnes, pro dešifrování za mnoho let (forward secrecy). Hybridní přístup by to chránil.

Model hrozby PQ spočívající v prolomení autentizačních klíčů v rozumném časovém období (řekněme několik měsíců) a následném vydávání se za autentizaci nebo dešifrování v téměř reálném čase, je mnohem vzdálenější? A to je okamžik, kdy bychom chtěli migrovat na PQC statické klíče.

Takže nejčasnější PQ model hrozby je OBEP/IBGW ukládající provoz pro pozdější dešifrování. Měli bychom nejprve implementovat hybridní ratchet.

Ratchet má nejvyšší prioritu. Transporty jsou další. Podpisy mají nejnižší prioritu.

Zavedení podpisů bude také o rok nebo více později než zavedení šifrování, protože zpětná kompatibilita není možná. Také přijetí MLDSA v průmyslu bude standardizováno CA/Browser Forum a certifikačními autoritami. CA nejprve potřebují podporu hardwarového bezpečnostního modulu (HSM), která v současnosti není dostupná [CA/Browser Forum](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/). Očekáváme, že CA/Browser Forum bude řídit rozhodnutí o konkrétních parametrických volbách, včetně toho, zda podporovat nebo vyžadovat kompozitní podpisy [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/).

| Milestone | Target |
|-----------|--------|
| Ratchet beta | Late 2025 |
| Select best enc type | Early 2026 |
| NTCP2 beta | Early 2026 |
| SSU2 beta | Mid 2026 |
| Ratchet production | Mid 2026 |
| Ratchet default | Late 2026 |
| Signature beta | Late 2026 |
| NTCP2 production | Late 2026 |
| SSU2 production | Early 2027 |
| Select best sig type | Early 2027 |
| NTCP2 default | Early 2027 |
| SSU2 default | Mid 2027 |
| Signature production | Mid 2027 |
## Migration

Pokud nebudeme schopni podporovat staré i nové ratchet protokoly na stejných tunelech, migrace bude mnohem obtížnější.

Měli bychom být schopni zkusit jen jeden-pak-druhý, jak jsme to udělali s X25519, což je třeba dokázat.

## Issues

- Výběr Noise Hash - zůstat u SHA256 nebo upgradovat?
  SHA256 by měl být dobrý dalších 20-30 let, není ohrožen PQ,
  Viz [NIST presentation](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf) a [NIST presentation](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf).
  Pokud bude SHA256 prolomeno, budeme mít horší problémy (netdb).
- NTCP2 separátní port, separátní router adresa
- SSU2 relay / peer test
- SSU2 pole verze
- SSU2 router adresa verze
