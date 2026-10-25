---
title: "Post-kvantové kryptografické protokoly"
number: "169"
author: "zzz, orignal, drzed, eyedeekay"
created: "2025-01-21"
lastupdated: "2026-04-09"
status: "Otevřít"
thread: "http://zzz.i2p/topics/3294"
target: "0.9.80"
toc: true
---

### Stav

| Protokol / Vlastnost | Stav |
|----------------------|------|
| Ratchet | Dokončeno v Java I2P a i2pd |
| NTCP2 | Beta Q1 2026 |
| SSU2 | Implementace začíná brzy, Beta Q23 2026 |
| MLDSA SigTypes | Nízká priorita, pravděpodobně 2027+ |
## Přehled

Zatímco výzkum a soutěž o vhodnou post-kvantovou (PQ) kryptografii probíhají již deset let, volby se staly jasnými teprve nedávno.

Začali jsme zkoumat důsledky PQ kryptografie v roce 2022 [zzz.i2p](http://zzz.i2p/topics/3294).

TLS standardy přidaly podporu pro hybridní šifrování v posledních dvou letech a nyní se používá pro významnou část šifrovaného provozu na internetu díky podpoře v Chrome a Firefox [Cloudflare](https://blog.cloudflare.com/pq-2024/).

NIST nedávno dokončil a publikoval doporučené algoritmy pro post-kvantovou kryptografii [NIST](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards). Několik běžných kryptografických knihoven nyní podporuje standardy NIST nebo v blízké budoucnosti uvolní jejich podporu.

Jak [Cloudflare](https://blog.cloudflare.com/pq-2024/), tak [NIST](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards) doporučují, aby migrace začala okamžitě. Viz také FAQ NSA o PQ z roku 2022 [NSA](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF). I2P by měl být lídrem v oblasti bezpečnosti a kryptografie. Nyní je čas implementovat doporučené algoritmy. Pomocí našeho flexibilního systému typů kryptografie a typů podpisů přidáme typy pro hybridní kryptografii a pro PQ a hybridní podpisy.

## Cíle

- Vybrat algoritmy odolné proti kvantovým počítačům
- Přidat pouze PQ a hybridní algoritmy do I2P protokolů tam, kde je to vhodné
- Definovat více variant
- Vybrat nejlepší varianty po implementaci, testování, analýze a výzkumu
- Přidat podporu postupně a se zpětnou kompatibilitou

## Nezamýšlené cíle

- Neměňte jednosměrné (Noise N) šifrovací protokoly
- Neodcházejte od SHA256, není v blízké budoucnosti ohroženo PQ
- Nevybírejte konečné preferované varianty v tuto chvíli

## Model hrozeb

- Routery na OBEP nebo IBGW, možná ve spolčení,
  ukládající garlic zprávy pro pozdější dešifrování (forward secrecy)
- Síťoví pozorovatelé
  ukládající transportní zprávy pro pozdější dešifrování (forward secrecy)
- Účastníci sítě falšující podpisy pro RI, LS, streaming, datagramy,
  nebo jiné struktury

## Postižené protokoly

Budeme upravovat následující protokoly, zhruba v pořadí jejich vývoje. Celkové zavedení bude pravděpodobně probíhat od konce roku 2025 do poloviny roku 2027. Podrobnosti najdete v sekci Priority a zavedení níže.

| Protokol / Funkce | Stav |
|--------------------|--------|
| Hybrid MLKEM Ratchet and LS | Schváleno 2025-06; beta 2025-08; vydání 2025-11 |
| Hybrid MLKEM NTCP2 | Testováno na živé síti, Schváleno 2026-02; beta cíl 2026-05; cíl vydání 2026-08 |
| Hybrid MLKEM SSU2 | Schváleno 2026-02; beta cíl 2026-08; cíl vydání 2026-11 |
| MLDSA SigTypes 12-14 | Návrh je stabilní, ale nemusí být dokončen až do 2027 |
| MLDSA Dests | Testováno na živé síti, vyžaduje upgrade sítě pro podporu floodfill |
| Hybrid SigTypes 15-17 | Předběžné |
| Hybrid Dests | |
## Návrh

Budeme podporovat standardy NIST FIPS 203 a 204 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf), které jsou založeny na algoritmech CRYSTALS-Kyber a CRYSTALS-Dilithium, ale NEJSOU s nimi kompatibilní (verze 3.1, 3 a starší).

### Výměna klíčů

Budeme podporovat hybridní výměnu klíčů v následujících protokolech:

| Proto   | Typ Noise | Podporuje pouze PQ? | Podporuje hybridní? |
|---------|-----------|---------------------|---------------------|
| NTCP2   | XK        | ne                  | ano                 |
| SSU2    | XK        | ne                  | ano                 |
| Ratchet | IK        | ne                  | ano                 |
| TBM     | N         | ne                  | ne                  |
| NetDB   | N         | ne                  | ne                  |
PQ KEM poskytuje pouze dočasné klíče a nepodporuje přímo handshaky se statickými klíči jako Noise XK a IK.

Noise N nepoužívá obousměrnou výměnu klíčů, a proto není vhodný pro hybridní šifrování.

Takže budeme podporovat pouze hybridní šifrování, pro NTCP2, SSU2 a Ratchet. Definujeme tři varianty ML-KEM podle [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf), celkem pro 3 nové typy šifrování. Hybridní typy budou definovány pouze v kombinaci s X25519.

Nové typy šifrování jsou:

| Typ | Kód |
|-----|-----|
| MLKEM512_X25519 | 5 |
| MLKEM768_X25519 | 6 |
| MLKEM1024_X25519 | 7 |
Režie bude značná. Typické velikosti zpráv 1 a 2 (pro XK a IK) jsou v současnosti kolem 100 bajtů (před jakýmkoliv dalším payloadem). To se zvýší 8x až 15x v závislosti na algoritmu.

### Podpisy

Budeme podporovat PQ a hybridní podpisy v následujících strukturách:

Takže budeme podporovat jak čistě PQ podpisy, tak hybridní podpisy. Definujeme tři varianty ML-DSA podle [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf), tři hybridní varianty s Ed25519 a tři čistě PQ varianty s prehash pouze pro SU3 soubory, celkem tedy 9 nových typů podpisů. Hybridní typy budou definovány pouze v kombinaci s Ed25519. Použijeme standardní ML-DSA, NE varianty pre-hash (HashML-DSA), s výjimkou SU3 souborů.

| Typ | Podporuje pouze PQ? | Podporuje hybridní? |
|------|---------------------|---------------------|
| RouterInfo | ano | ano |
| LeaseSet | ano | ano |
| Streaming SYN/SYNACK/Close | ano | ano |
| Repliable Datagrams | ano | ano |
| Datagram2 (prop. 163) | ano | ano |
| I2CP create session msg | ano | ano |
| SU3 files | ano | ano |
| X.509 certificates | ano | ano |
| Java keystores | ano | ano |
Budeme používat "hedged" nebo randomizovanou variantu podepisování, nikoli "deterministickou" variantu, jak je definováno v [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) sekci 3.4. To zajišťuje, že každý podpis je odlišný, i když se podepisují stejná data, a poskytuje dodatečnou ochranu proti útokům postranním kanálem. Další podrobnosti o volbách algoritmů včetně kódování a kontextu najdete v sekci poznámek k implementaci níže.

Nové typy podpisů jsou:

Certifikáty X.509 a další DER kódování budou používat kompozitní struktury a OID definované v [IETF návrhu](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/).

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
Overhead bude značný. Typické velikosti Ed25519 destinací a router identit jsou 391 bajtů. Ty se zvětší 3,5x až 6,8x v závislosti na algoritmu. Ed25519 podpisy mají 64 bajtů. Ty se zvětší 38x až 76x v závislosti na algoritmu. Typické podepsané RouterInfo, leaseSet, odpovědné datagramy a podepsané streaming zprávy mají kolem 1KB. Ty se zvětší 3x až 8x v závislosti na algoritmu.

Jelikož nové typy destinací a router identit nebudou obsahovat výplň, nebudou kompresibilní. Velikosti destinací a router identit, které jsou gzip komprimovány při přenosu, se zvětší 12x - 38x v závislosti na algoritmu.

Pro destinace jsou nové typy podpisů podporovány se všemi typy šifrování v leaseSet. Nastavte typ šifrování v certifikátu klíče na NONE (255).

### Legální kombinace

Pro RouterIdentities je typ šifrování ElGamal zastaralý. Nové typy podpisů jsou podporovány pouze se šifrováním X25519 (typ 4). Nové typy šifrování budou označeny v RouterAddresses. Typ šifrování v klíčovém certifikátu bude i nadále typ 4.

Testovací vektory pro SHA3-256, SHAKE128 a SHAKE256 jsou k dispozici na [NIST](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values).

### Je potřeba nová kryptografie

- ML-KEM (dříve CRYSTALS-Kyber) [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
- ML-DSA (dříve CRYSTALS-Dilithium) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)
- SHA3-128 (dříve Keccak-256) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf) Používá se pouze pro SHAKE128
- SHA3-256 (dříve Keccak-512) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
- SHAKE128 a SHAKE256 (XOF rozšíření pro SHA3-128 a SHA3-256) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)

Poznamenejte, že Java bouncycastle knihovna podporuje všechny výše uvedené. Podpora C++ knihovny je v OpenSSL 3.5 [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

Nebudeme podporovat [FIPS 205](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.205.pdf) (Sphincs+), je mnohem mnohem pomalejší a větší než ML-DSA. Nebudeme podporovat nadcházející FIPS206 (Falcon), ještě není standardizován. Nebudeme podporovat NTRU nebo jiné PQ kandidáty, které nebyly standardizovány NIST.

### Alternativy

Existuje určitý výzkumný [článek](https://eprint.iacr.org/2020/379.pdf) o přizpůsobení Wireguard (IK) pro čistou PQ kryptografii, ale v tomto článku zůstává několik otevřených otázek. Později byl tento přístup implementován jako Rosenpass [Rosenpass](https://rosenpass.eu/) [whitepaper](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf) pro PQ Wireguard.

### Rosenpass

Rosenpass používá handshake podobný Noise KK s předsdílenými statickými klíči Classic McEliece 460896 (každý 500 KB) a efemérními klíči Kyber-512 (v podstatě MLKEM-512). Jelikož šifrotexty Classic McEliece mají pouze 188 bajtů a veřejné klíče a šifrotexty Kyber-512 mají rozumnou velikost, obě handshake zprávy se vejdou do standardního UDP MTU. Výstupní sdílený klíč (osk) z PQ KK handshake se používá jako vstupní předsdílený klíč (psk) pro standardní Wireguard IK handshake. Celkově se tedy provádějí dva kompletní handshaky, jeden čistě PQ a jeden čistě X25519.

Nemůžeme udělat nic z toho pro nahrazení našich XK a IK handshake, protože:

V whitepaperu je spousta dobrých informací a projdeme si ho kvůli nápadům a inspiraci. TODO.

- Nemůžeme provést KK, Bob nemá statický klíč Alice
- 500KB statické klíče jsou příliš velké
- Nechceme další round-trip

Aktualizujte sekce a tabulky v dokumentu běžných struktur [/docs/specs/common-structures/](/docs/specs/common-structures/) následovně:

## Specifikace

### Běžné struktury

Nové typy veřejných klíčů jsou:

#### PublicKey

Hybridní veřejné klíče jsou klíče X25519. KEM veřejné klíče jsou dočasné PQ klíče poslané od Alice k Bobovi. Kódování a pořadí bajtů jsou definovány v [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

| Typ | Délka veřejného klíče | Od verze | Použití |
|------|-------------------|-------|-------|
| MLKEM512_X25519 | 32 | 0.9.xx | Viz návrh 169, pouze pro Leasesets, ne pro RI nebo Destinations |
| MLKEM768_X25519 | 32 | 0.9.xx | Viz návrh 169, pouze pro Leasesets, ne pro RI nebo Destinations |
| MLKEM1024_X25519 | 32 | 0.9.xx | Viz návrh 169, pouze pro Leasesets, ne pro RI nebo Destinations |
| MLKEM512 | 800 | 0.9.xx | Viz návrh 169, pouze pro handshakes, ne pro Leasesets, RI nebo Destinations |
| MLKEM768 | 1184 | 0.9.xx | Viz návrh 169, pouze pro handshakes, ne pro Leasesets, RI nebo Destinations |
| MLKEM1024 | 1568 | 0.9.xx | Viz návrh 169, pouze pro handshakes, ne pro Leasesets, RI nebo Destinations |
| MLKEM512_CT | 768 | 0.9.xx | Viz návrh 169, pouze pro handshakes, ne pro Leasesets, RI nebo Destinations |
| MLKEM768_CT | 1088 | 0.9.xx | Viz návrh 169, pouze pro handshakes, ne pro Leasesets, RI nebo Destinations |
| MLKEM1024_CT | 1568 | 0.9.xx | Viz návrh 169, pouze pro handshakes, ne pro Leasesets, RI nebo Destinations |
| NONE | 0 | 0.9.xx | Viz návrh 169, pro destinations s PQ sig typy pouze, ne pro RI nebo Leasesets |
MLKEM*_CT klíče nejsou skutečně veřejné klíče, jsou to "šifrovaný text" poslaný od Boba k Alici v Noise handshaku. Jsou zde uvedeny pro úplnost.

Nové typy Privátních klíčů jsou:

#### PrivateKey

Hybridní privátní klíče jsou X25519 klíče. KEM privátní klíče jsou pouze pro Alici. KEM kódování a pořadí bajtů jsou definovány v [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

| Typ | Délka privátního klíče | Od verze | Použití |
|-----|------------------------|----------|---------|
| MLKEM512_X25519 | 32 | 0.9.xx | Viz návrh 169, pouze pro Leasesets, ne pro RI nebo Destinations |
| MLKEM768_X25519 | 32 | 0.9.xx | Viz návrh 169, pouze pro Leasesets, ne pro RI nebo Destinations |
| MLKEM1024_X25519 | 32 | 0.9.xx | Viz návrh 169, pouze pro Leasesets, ne pro RI nebo Destinations |
| MLKEM512 | 1632 | 0.9.xx | Viz návrh 169, pouze pro handshaky, ne pro Leasesets, RI nebo Destinations |
| MLKEM768 | 2400 | 0.9.xx | Viz návrh 169, pouze pro handshaky, ne pro Leasesets, RI nebo Destinations |
| MLKEM1024 | 3168 | 0.9.xx | Viz návrh 169, pouze pro handshaky, ne pro Leasesets, RI nebo Destinations |
Nové typy podpisových veřejných klíčů jsou:

#### SigningPublicKey

Hybridní veřejné klíče pro podepisování jsou klíč Ed25519 následovaný PQ klíčem, jak je uvedeno v [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/). Kódování a pořadí bajtů jsou definovány v [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

| Typ | Délka (bajty) | Od verze | Použití |
|------|----------------|-------|-------|
| MLDSA44 | 1312 | 0.9.xx | Viz návrh 169 |
| MLDSA65 | 1952 | 0.9.xx | Viz návrh 169 |
| MLDSA87 | 2592 | 0.9.xx | Viz návrh 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 1344 | 0.9.xx | Viz návrh 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 1984 | 0.9.xx | Viz návrh 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 2624 | 0.9.xx | Viz návrh 169 |
| MLDSA44ph | 1344 | 0.9.xx | Pouze pro SU3 soubory, ne pro netDb struktury |
| MLDSA65ph | 1984 | 0.9.xx | Pouze pro SU3 soubory, ne pro netDb struktury |
| MLDSA87ph | 2624 | 0.9.xx | Pouze pro SU3 soubory, ne pro netDb struktury |
Nové typy Signing Private Key jsou:

#### SigningPrivateKey

Hybridní podepisovací soukromé klíče jsou klíč Ed25519 následovaný PQ klíčem, jak je uvedeno v [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/). Kódování a pořadí bajtů jsou definovány v [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

| Typ | Délka (bajty) | Od verze | Použití |
|-----|---------------|----------|---------|
| MLDSA44 | 2560 | 0.9.xx | Viz návrh 169 |
| MLDSA65 | 4032 | 0.9.xx | Viz návrh 169 |
| MLDSA87 | 4896 | 0.9.xx | Viz návrh 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2592 | 0.9.xx | Viz návrh 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 4064 | 0.9.xx | Viz návrh 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4928 | 0.9.xx | Viz návrh 169 |
| MLDSA44ph | 2592 | 0.9.xx | Pouze pro SU3 soubory, ne pro netDb struktury. Viz návrh 169 |
| MLDSA65ph | 4064 | 0.9.xx | Pouze pro SU3 soubory, ne pro netDb struktury. Viz návrh 169 |
| MLDSA87ph | 4928 | 0.9.xx | Pouze pro SU3 soubory, ne pro netDb struktury. Viz návrh 169 |
Nové typy podpisů jsou:

Hybridní podpisy jsou podpis Ed25519 následovaný PQ podpisem, jak je uvedeno v [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/). Hybridní podpisy se ověřují ověřením obou podpisů a selhávají, pokud jeden z nich selže. Kódování a pořadí bytů jsou definovány v [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

#### Podpis

Nové typy veřejných klíčů pro podepisování jsou:

| Typ | Délka (bajty) | Od verze | Použití |
|------|----------------|-------|-------|
| MLDSA44 | 2420 | 0.9.xx | Viz návrh 169 |
| MLDSA65 | 3309 | 0.9.xx | Viz návrh 169 |
| MLDSA87 | 4627 | 0.9.xx | Viz návrh 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2484 | 0.9.xx | Viz návrh 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 3373 | 0.9.xx | Viz návrh 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4691 | 0.9.xx | Viz návrh 169 |
| MLDSA44ph | 2484 | 0.9.xx | Pouze pro soubory SU3, ne pro struktury netDb. Viz návrh 169 |
| MLDSA65ph | 3373 | 0.9.xx | Pouze pro soubory SU3, ne pro struktury netDb. Viz návrh 169 |
| MLDSA87ph | 4691 | 0.9.xx | Pouze pro soubory SU3, ne pro struktury netDb. Viz návrh 169 |
Nové typy kryptografických veřejných klíčů jsou:

#### Klíčové certifikáty

Hybridní veřejné klíče pro podepisování jsou klíč Ed25519 následovaný PQ klíčem, jak je uvedeno v [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/). Kódování a pořadí bajtů jsou definovány v [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

| Typ | Kód typu | Celková délka veřejného klíče | Od verze | Použití |
|------|-----------|-------------------------|-------|-------|
| MLDSA44 | 12 | 1312 | 0.9.xx | Viz návrh 169 |
| MLDSA65 | 13 | 1952 | 0.9.xx | Viz návrh 169 |
| MLDSA87 | 14 | 2592 | 0.9.xx | Viz návrh 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 0.9.xx | Viz návrh 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 0.9.xx | Viz návrh 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 0.9.xx | Viz návrh 169 |
| MLDSA44ph | 18 | n/a | 0.9.xx | Pouze pro SU3 soubory |
| MLDSA65ph | 19 | n/a | 0.9.xx | Pouze pro SU3 soubory |
| MLDSA87ph | 20 | n/a | 0.9.xx | Pouze pro SU3 soubory |
Pro destinace s Hybrid nebo PQ typy podpisů použijte NONE (typ 255) pro typ šifrování, ale není zde žádný kryptografický klíč a celá 384-bajtová hlavní sekce je určena pro podpisový klíč.

| Typ | Kód typu | Celková délka veřejného klíče | Od verze | Použití |
|------|-----------|-------------------------|-------|-------|
| MLKEM512_X25519 | 5 | 32 | 0.9.xx | Viz návrh 169, pouze pro LeaseSet, ne pro RI nebo Destinations |
| MLKEM768_X25519 | 6 | 32 | 0.9.xx | Viz návrh 169, pouze pro LeaseSet, ne pro RI nebo Destinations |
| MLKEM1024_X25519 | 7 | 32 | 0.9.xx | Viz návrh 169, pouze pro LeaseSet, ne pro RI nebo Destinations |
| NONE | 255 | 0 | 0.9.xx | Viz návrh 169 |
Hybridní typy klíčů nejsou NIKDY zahrnuty v certifikátech klíčů; pouze v leaseSets.

Bez výplně. Celková délka je 7 + celková délka klíče. Délka certifikátu klíče je 4 + přebytečná délka klíče.

#### Velikosti destinací

Zde jsou délky pro nové typy Destination. Typ šifrování pro všechny je NONE (typ 255) a délka šifrovacího klíče je považována za 0. Celá 384-bajtová sekce se používá pro první část veřejného podpisového klíče. POZNÁMKA: To se liší od specifikace pro typy podpisů ECDSA_SHA512_P521 a RSA, kde jsme zachovali 256-bajtový ElGamal klíč v destination, i když nebyl používán.

skey[0:383] 5 (932 >> 8) (932 & 0xff) 00 12 00 255 skey[384:1311]

Příklad 1319-bajtového proudu bajtů cíle pro MLDSA44:

Příklad 1351-bajtového proudu bajtů identity routeru pro MLDSA44:

| Typ | Kód typu | Celková délka veřejného klíče | Hlavní | Přebytek | Celková délka Dest |
|------|-----------|-------------------------|------|--------|-------------------|
| MLDSA44 | 12 | 1312 | 384 | 928 | 1319 |
| MLDSA65 | 13 | 1952 | 384 | 1568 | 1959 |
| MLDSA87 | 14 | 2592 | 384 | 2208 | 2599 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 384 | 960 | 1351 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 384 | 1600 | 1991 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 384 | 2240 | 2631 |
#### Velikosti RouterIdent

Zde jsou délky pro nové typy Destination. Typ šifrování pro všechny je X25519 (typ 4). Celá 352-bajtová sekce po veřejném klíči X25519 se používá pro první část veřejného podpisového klíče. Žádné vyplňování. Celková délka je 39 + celková délka klíče. Délka certifikátu klíče je 4 + přebytečná délka klíče.

Handshakes používají vzory handshake [Noise Protocol](https://noiseprotocol.org/noise.html).

enckey[0:31] skey[0:351] 5 (960 >> 8) (960 & 0xff) 00 12 00 4 skey[352:1311]

| Typ | Kód typu | Celková délka veřejného klíče | Hlavní | Přebytek | Celková délka RouterIdent |
|------|-----------|-------------------------|------|--------|--------------------------|
| MLDSA44 | 12 | 1312 | 352 | 960 | 1351 |
| MLDSA65 | 13 | 1952 | 352 | 1600 | 1991 |
| MLDSA87 | 14 | 2592 | 352 | 2240 | 2631 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 352 | 992 | 1383 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 352 | 1632 | 2023 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 352 | 2272 | 2663 |
### PublicKey

Následující úpravy XK a IK pro hybridní dopřednou sekretnost (hfs) jsou specifikovány v [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) sekce 5:

Vzor e1 je definován následovně, jak je specifikováno v [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) sekci 4:

#### KDF pro split()

```

  M = message
  Prefix = "CompositeAlgorithmSignatures2025" (32 bytes, not null terminated)
  Label = (30 bytes, not null terminated), one of:
          "COMPSIG-MLDSA44-Ed25519-SHA512"
          "COMPSIG-MLDSA65-Ed25519-SHA512"
          "COMPSIG-MLDSA87-Ed25519-SHA512"  // not in [COMPOSITE-SIGS]
  ctx = "" (0 bytes)
  len(ctx) = 0  (1 byte)
  PH(M) = SHA512(M) (64 bytes)


  Compute a hash of the message prepended as follows:

  M' = Prefix || Label || len(ctx) || ctx || PH( M )

  M' length is 127 bytes.

  Sign the prehashed message M':

  signature = MLDSA_SIGN(M') || Ed25519_SIGN(M')

```
#### Identifikátory Noise

Vzor ekem1 je definován následovně, jak je specifikováno v [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) sekci 4:

```

  M' = as above

  signature = MLDSA_VERIFY(M') && Ed25519_VERIFY(M')


```
#### Problémy

Tato sekce se vztahuje na protokoly IK i XK.

### Vzory handshake

Hybridní handshake je definován v [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf). První zpráva, od Alice k Bobovi, obsahuje e1, enkapsulační klíč, před datovou částí zprávy. Toto je považováno za dodatečný statický klíč; zavolejte na něj EncryptAndHash() (jako Alice) nebo DecryptAndHash() (jako Bob). Poté zpracujte datovou část zprávy obvyklým způsobem.

Používá se následující mapování písmen:

- e = jednorázový dočasný klíč
- s = statický klíč
- p = datová část zprávy
- e1 = jednorázový dočasný PQ klíč, odeslaný od Alice k Bobovi
- ekem1 = šifrový text KEM, odeslaný od Boba k Alici

Definujeme následující funkce odpovídající kryptografickým stavebním blokům použitým podle definice v [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

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
(encap_key, decap_key) = PQ_KEYGEN()

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
(ciphertext, kem_shared_key) = ENCAPS(encap_key)

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
### Noise Handshake KDF

#### Problémy

- Měli bychom změnit hash funkci pro handshake? Viz [porovnání](https://kerkour.com/fast-secure-hash-function-sha256-sha512-sha3-blake3).
  SHA256 není zranitelná vůči PQ, ale pokud chceme upgradovat
  naši hash funkci, teď je ten správný čas, zatímco měníme další věci.
  Aktuální IETF SSH návrh [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-sshm-mlkem-hybrid-kex/) je použít MLKEM768
  se SHA256, a MLKEM1024 se SHA384. Tento návrh zahrnuje
  diskusi o bezpečnostních úvahách.
- Měli bychom přestat posílat 0-RTT ratchet data (kromě leaseSet)?
- Měli bychom přepnout ratchet z IK na XK, pokud neposíláme 0-RTT data?

#### Přehled

kem_shared_key = DECAPS(ciphertext, decap_key)

Všimněte si, že jak encap_key, tak ciphertext jsou šifrovány uvnitř ChaCha/Poly bloků ve zprávách 1 a 2 Noise handshake. Budou dešifrovány jako součást procesu handshake.

Druhá zpráva, od Boba k Alici, obsahuje ekem1, šifrovaný text, před datovou částí zprávy. Toto se zachází jako s dodatečným statickým klíčem; zavolej EncryptAndHash() na něj (jako Bob) nebo DecryptAndHash() (jako Alice). Poté vypočítej kem_shared_key a zavolej MixKey(kem_shared_key). Pak zpracuj datovou část zprávy jako obvykle.

#### Definované operace ML-KEM

Pro XK: Po vzoru zprávy 'es' a před nákladem přidejte:

NEBO

    Alice creates the encapsulation and decapsulation keys
    The encapsulation key is sent in message 1.
    encap_key and decap_key sizes vary based on ML-KEM variant.

Pro IK: Po vzoru zprávy 'es' a před vzorem zprávy 's' přidejte:

    Bob calculates the ciphertext and shared key,
    using the ciphertext received in message 1.
    The ciphertext is sent in message 2.
    ciphertext size varies based on ML-KEM variant.
    The kem_shared_key is always 32 bytes.

Pro XK: Po vzoru zprávy 'es' a před payloadem přidejte:

    Alice calculates the shared key,
    using the ciphertext received in message 2.
    The kem_shared_key is always 32 bytes.

NEBO

kem_shared_key se vmíchá do chaining key pomocí MixHash(). Podrobnosti viz níže.

#### Alice KDF pro Zprávu 1

Pro XK: Po vzoru zprávy 'ee' a před nákladem přidat:

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
#### Bob KDF pro zprávu 1

Pro XK: Po vzoru zprávy 'ee' a před nákladem přidat:

NEBO

Pro IK: Po vzoru zprávy 'es' a před vzorem zprávy 's' přidejte:

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
#### Bob KDF pro Zprávu 2

Aktualizujte specifikaci ECIES-Ratchet [/docs/specs/ecies/](/docs/specs/ecies/) následovně:

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

  // AEAD parameters for payload section
  ... as in standard SSU2 ...
  k = keydata[32:63]
  ...

```
#### Alice KDF pro zprávu 2

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

  // AEAD parameters for payload section
  ... as in standard SSU2 ...
  k = keydata[32:63]
  ...

```
#### KDF pro Zprávu 3 (pouze XK)

nezměněno

#### Identifikátory Noise

nezměněno

### Ratchet

Změny: Současný ratchet má prázdný payload pro první ChaCha sekci a payload ve druhé sekci. S ML-KEM jsou nyní tři sekce. První sekce obsahuje šifrovaný PQ ciphertext. Druhá sekce má prázdný payload. Třetí sekce obsahuje payload.

#### Identifikátory Noise

- "Noise_IKhfselg2_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM1024_ChaChaPoly_SHA256"

#### 1b) Nový formát relace (s vazbou)

Změny: Současný ratchet obsahoval statický klíč v první sekci ChaCha a payload ve druhé sekci. S ML-KEM nyní existují tři sekce. První sekce obsahuje zašifrovaný PQ veřejný klíč. Druhá sekce obsahuje statický klíč. Třetí sekce obsahuje payload.

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

| Typ | Kód typu | X délka | Délka Msg 1 | Délka Msg 1 Enc | Délka Msg 1 Dec | Délka PQ klíče | délka pl |
|-----|----------|---------|-------------|-----------------|-----------------|----------------|----------|
| X25519 | 4 | 32 | 96+pl | 64+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 912+pl | 880+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1296+pl | 1360+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1680+pl | 1648+pl | 1568+pl | 1568 | pl |
Všimněte si, že payload musí obsahovat blok DateTime, takže minimální velikost payload je 7. Minimální velikosti zprávy 1 mohou být vypočítány odpovídajícím způsobem.

#### 1g) Formát odpovědi na novou relaci

Změny: Současný NTCP2 obsahuje pouze možnosti v sekci ChaCha. S ML-KEM bude sekce ChaCha také obsahovat zašifrovaný PQ veřejný klíč.

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

| Typ | Kód typu | Y délka | Msg 2 délka | Msg 2 Enc délka | Msg 2 Dec délka | PQ CT délka | opt délka |
|-----|----------|---------|-------------|-----------------|-----------------|-------------|-----------|
| X25519 | 4 | 32 | 72+pl | 32+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 856+pl | 816+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1176+pl | 1136+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1656+pl | 1616+pl | 1568+pl | 1568 | pl |
Všimněte si, že zatímco zpráva 2 bude normálně mít nenulový payload, specifikace ratchet [/docs/specs/ecies/](/docs/specs/ecies/) to nevyžaduje, takže minimální velikost payload je 0. Minimální velikosti zprávy 2 mohou být vypočítány odpovídajícím způsobem.

### NTCP2

Aktualizujte specifikaci NTCP2 [/docs/specs/ntcp2/](/docs/specs/ntcp2/) následovně:

#### Identifikátory Noise

- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM1024_ChaChaPoly_SHA256"

#### 1) SessionRequest

Nezpracovaný obsah:

Aby bylo možné podporovat PQ i non-PQ NTCP2 na stejné adrese a portu routeru, používáme nejvýznamnější bit hodnoty X (X25519 ephemeral public key) k označení, že se jedná o PQ připojení. Tento bit je vždy nenastaven pro non-PQ připojení.

U Alice, po zašifrování zprávy pomocí Noise, ale před AES zamaskováním X, nastavte X[31] |= 0x80.

Pro Boba, po AES de-obfuskaci X, otestujte X[31] & 0x80. Pokud je bit nastaven, vymažte jej pomocí X[31] &= 0x7f a dešifrujte přes Noise jako PQ spojení. Pokud je bit vymazán, dešifrujte přes Noise jako non-PQ spojení obvyklým způsobem.

Pro PQ NTCP2 inzerované na jiné router adrese a portu to není vyžadováno.

Pro další informace viz sekci Publikované adresy níže.

Nešifrovaná data (Poly1305 auth tag nezobrazena):

```
  +----+----+----+----+----+----+----+----+
  |        MS bit set to 1 and then       |
  +        obfuscated with RH_B           +
  |       AES-CBC-256 encrypted X         |
  +             (32 bytes)                +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaChaPoly encrypted data (MLKEM)   |
  +      (see table below for length)     +
  |   k defined in KDF for message 1      |
  +   n = 0                               +
  |   see KDF for associated data         |
  ~                                       ~
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (options)   |
  +         16 bytes                      +
  |   k defined in KDF for message 1      |
  +   n = 1                               +
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

  Same as current specification except add a second ChaChaPoly frame
```
Nešifrovaná data (Poly1305 autentifikační tag není zobrazen):

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
Poznámka: pole verze v bloku možností zprávy 1 musí být nastaveno na hodnotu 2, i pro PQ připojení.

Velikosti:

| Typ | Kód typu | X délka | Délka zprávy 1 | Délka zprávy 1 šifrované | Délka zprávy 1 dešifrované | Délka PQ klíče | délka opt |
|------|-----------|-------|-----------|---------------|---------------|------------|---------|
| X25519 | 4 | 32 | 64+pad | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 880+pad | 848 | 816 | 800 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1264+pad | 1232 | 1200 | 1184 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1648+pad | 1616 | 1584 | 1568 | 16 |
Poznámka: Kódy typů jsou pouze pro interní použití. Routery zůstanou typu 4 a podpora bude uvedena v adresách routerů.

#### 2) SessionCreated

Nezpracovaný obsah:

Nešifrovaná data (Poly1305 auth tag nezobrazena):

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
  |   ChaCha20 encrypted data (MLKEM)     |
  -      (see table below for length)     -
  +   k defined in KDF for message 2      +
  |  (before mixKey)                      |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 encrypted data (options)   |
  +         16 bytes                      +
  +   k defined in KDF for message 2      +
  |  (after mixKey)                       |
  +  n = 0; see KDF for associated data   +
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

  Same as current specification except add a second ChaChaPoly frame
```
Velikosti:

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

| Typ | Kód typu | Y délka | Msg 2 délka | Msg 2 Enc délka | Msg 2 Dec délka | PQ CT délka | opt délka |
|-----|----------|---------|-------------|-----------------|-----------------|-------------|-----------|
| X25519 | 4 | 32 | 64+pad | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 848+pad | 816 | 784 | 768 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1136+pad | 1104 | 1104 | 1088 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1616+pad | 1584 | 1584 | 1568 | 16 |
Poznámka: Kódy typů jsou pouze pro interní použití. Routery zůstanou typu 4 a podpora bude uvedena v adresách routerů.

#### 3) SessionConfirmed

Nezměněno

#### Funkce pro odvození klíče (KDF) (pro datovou fázi)

Nezměněno

#### Zveřejněné adresy

Ve všech případech použijte název transportu NTCP2 jako obvykle.

Jiná adresa/port než non-PQ, nebo pouze PQ, bez firewallu NENÍ podporováno. Toto nebude implementováno dokud nebude zakázáno non-PQ NTCP2, což bude za několik let. Když bude non-PQ zakázáno, může být podporováno více PQ variant, ale pouze jedna na adresu. V adrese routeru publikujte v=[3|4|5] pro označení MLKEM 512/768/1024. Alice nenastavuje MSB dočasného klíče. Starší routery zkontrolují parametr v a přeskočí tuto adresu jako nepodporovanou.

Adresy za firewallem (žádná IP není publikována): V adrese routeru publikujte v=2 (jako obvykle). Není potřeba publikovat parametr pq.

Alice se může připojit k PQ Bobovi pomocí PQ varianty, kterou Bob publikuje, bez ohledu na to, zda Alice inzeruje pq podporu ve svých router informacích, nebo zda inzeruje stejnou variantu.

V současné specifikaci jsou zprávy 1 a 2 definovány tak, aby měly "rozumné" množství výplně, s doporučeným rozsahem 0-31 bajtů a bez specifikovaného maxima.

#### Maximální vyplnění

Až do API 0.9.68 (vydání 2.11.0) implementovala Java I2P maximum 256 bajtů padding pro non-PQ připojení, avšak toto nebylo dříve dokumentováno. Od API 0.9.69 (vydání 2.12.0) implementuje Java I2P stejné maximální padding pro non-PQ připojení jako pro MLKEM-512. Viz tabulka níže.

Použijte definovanou velikost zprávy jako maximální padding, to znamená, že maximální padding zdvojnásobí velikost zprávy pro PQ připojení následovně:

Aktualizujte specifikaci SSU2 [/docs/specs/ssu2/](/docs/specs/ssu2/) následovně:

| Maximální padding zprávy | non-PQ (do 0.9.68) | non-PQ (od 0.9.69) | MLKEM-512 | MLKEM-768 | MLKEM-1024 |
|--------------------------|--------------------|--------------------|-----------|-----------|------------|
| Session Request          |   256              |   880              |    880    |     1264  |    1648    |
| Session Created          |   256              |   848              |    848    |     1136  |    1616    |
### SSU2

Poznamenejte, že MLKEM-1024 NENÍ podporován pro SSU2, protože klíče jsou příliš velké na to, aby se vešly do standardního 1500bajtového datagramu.

#### Identifikátory Noise

- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"

Dlouhá hlavička má 32 bajtů. Používá se před vytvořením relace pro Token Request, SessionRequest, SessionCreated a Retry. Používá se také pro zprávy Peer Test a Hole Punch mimo relaci.

#### Dlouhá hlavička

V následujících zprávách nastavte pole ver (verze) v dlouhé hlavičce na 3 nebo 4, což označuje MLKEM-512 nebo MLKEM-768.

V následujících zprávách nastavte pole ver (verze) v dlouhé hlavičce na 2, jako obvykle, i když je podporováno MLKEM-512 nebo MLKEM-768. Implementace mohou také nastavit hodnotu na 3 nebo 4, pokud ji druhá strana podporuje, ale není to nutné. Implementace by měly přijímat jakoukoliv hodnotu 2-4.

- (0) Požadavek na relaci
- (1) Relace vytvořena
- (9) Opakování (poznámka: Opakování s ukončením může obsahovat jakoukoli verzi 2–4)
- (10) Požadavek na token

Ve zprávě níže nastavte pole ver (verze) v dlouhém záhlaví na libovolnou verzi 2–4, protože volbu verze provádí Alice, nikoli Charlie. Přijatelné je ji vždy nastavit na 2. Implementace by měly přijímat jakoukoli hodnotu v rozsahu 2–4.

- (11) Průraz otvoru

V následující zprávě nastavte pole ver (verze) v dlouhém záhlaví na hodnotu 2, jak je obvyklé, i když je podporován MLKEM-512 nebo MLKEM-768. Implementace mohou hodnotu nastavit na 3 nebo 4, pokud to druhá strana podporuje, ale není to nutné. Implementace by měly přijímat jakoukoli hodnotu v rozsahu 2–4.

- (7) Testování protějšku (mimo relační zprávy 5–7)

Diskuze: Nastavení pole verze na 3 nebo 4 nemusí být striktně nutné pro všechny typy zpráv, ale pomáhá dřívější detekci selhání u nepodporovaných post-kvantových připojení. Zprávy Token Request a Retry (typy 9 a 10) by měly mít verze 3/4 z důvodu konzistence. Zprávy Peer Test (typ 7) jsou mimo relaci a nesvědčí o záměru iniciovat relaci.

nezměněno

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

nezměněno

#### SessionRequest (Typ 0)

Změna KDF pro ochranu proti spoofingu: K řešení problémů uvedených v Návrhu 165 [Prop165]_, ale s jiným řešením, upravujeme KDF pro Session Request. Toto platí pouze pro PQ sessions. KDF pro non-PQ sessions zůstává nezměněno.

Surový obsah:

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
Nešifrovaná data (Poly1305 auth tag nezobrazena):

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
Nešifrovaná data (Poly1305 autentifikační tag není zobrazen):

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
Velikosti, bez započtení režie IP:

| Typ | Kód typu | X délka | Délka Msg 1 | Délka Msg 1 Enc | Délka Msg 1 Dec | Délka PQ klíče | délka pl |
|------|-----------|-------|-----------|---------------|---------------|------------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 896+pl | 832+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1280+pl | 1216+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | n/a | příliš velké | | | | |
Poznámka: Kódy typů jsou pouze pro interní použití. Routery zůstanou typu 4 a podpora bude uvedena v adresách routerů.

Minimální MTU pro MLKEM768_X25519: Přibližně 1316 pro IPv4 a 1336 pro IPv6.

Nešifrovaná data (Poly1305 auth tag nezobrazena):

#### SessionCreated (Typ 1)

Surový obsah:

Nešifrovaná data (Poly1305 auth tag nezobrazena):

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
  |   ChaCha20 encrypted data (MLKEM)     |
  ~  length varies                        ~
  +  k defined in KDF for Session Created +
  |  (before mixKey)                      |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 encrypted data (payload)   |
  ~  length varies                        ~
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
Velikosti:

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
Velikosti, bez započtení režie IP:

| Typ | Kód typu | Y délka | Msg 2 délka | Msg 2 Enc délka | Msg 2 Dec délka | PQ CT délka | pl délka |
|-----|-----------|---------|-------------|-----------------|-----------------|-------------|----------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 864+pl | 800+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1184+pl | 1118+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | n/a | příliš velký | | | | |
Poznámka: Kódy typů jsou pouze pro interní použití. Routery zůstanou typu 4 a podpora bude uvedena v adresách routerů.

Minimální MTU pro MLKEM768_X25519: Přibližně 1316 pro IPv4 a 1336 pro IPv6.

PQ podpisy: Relay bloky, Peer Test bloky a Peer Test zprávy obsahují podpisy. Bohužel jsou PQ podpisy větší než MTU. Neexistuje žádný současný mechanismus pro fragmentaci Relay nebo Peer Test bloků či zpráv napříč více UDP pakety. Protokol musí být rozšířen o podporu fragmentace. To bude provedeno v samostatném návrhu, který bude určen později. Dokud nebude dokončeno, Relay a Peer Test nebudou podporovány.

#### SessionConfirmed (Typ 2)

nezměněno

#### KDF pro datovou fázi

nezměněno

#### Relay a Peer Test

Následující bloky obsahují pole verzí. Zůstanou verzí 2 (kvůli kompatibilitě s non-PQ Bobem) a nezmění se na verzi 3/4 pro PQ.

- Žádost o přepojení (Relay Request)
- Odpověď na přepojení (Relay Response)
- Úvodní zpráva přepojení (Relay Intro)
- Test protějšku (Peer Test)

Ve všech případech použijte název transportu SSU2 jako obvykle. MLKEM-1024 není podporován.

#### Zveřejněné adresy

Použijte stejnou adresu/port jako u non-PQ, non-firewalled. Je podporována jedna nebo obě PQ varianty. V adrese routeru publikujte v=2 (jako obvykle) a nový parametr pq=[3|4|3,4] pro označení MLKEM 512/768/obojí. Starší routery budou ignorovat parametr pq a připojí se non-pq jako obvykle.

Buďte opatrní, abyste nepřekročili MTU s MLKEM768. Minimální MTU pro SSU2 je 1280, což je velikost zprávy 1 bez výplně. Nezahrnujte výplň do zprávy 1, pokud je MTU Alice nebo Boba 1280.

Adresy za firewallem (žádná IP publikována): V adrese routeru publikujte v=2 (jako obvykle). Parametr pq MUSÍ být publikován v adresách za firewallem pro podporu relay.

Alice se může připojit k PQ Bobovi pomocí PQ varianty, kterou Bob publikuje, bez ohledu na to, zda Alice inzeruje podporu pq ve svých informacích o routeru, nebo zda inzeruje stejnou variantu.

V současné specifikaci jsou zprávy 1 a 2 definovány tak, aby měly "rozumné" množství výplně, s doporučeným rozsahem 0-31 bajtů a bez specifikovaného maxima.

#### MTU

Mohli bychom interně použít pole verze a použít 3 pro MLKEM512 a 4 pro MLKEM768.

### Streamování

Pro zprávy 1 a 2 by MLKEM768 zvýšilo velikosti paketů nad minimální MTU 1280. Pravděpodobně by se pro dané připojení nepodporovalo, pokud by bylo MTU příliš nízké.

### SU3 soubory

Pro zprávy 1 a 2 by MLKEM1024 zvýšil velikost paketů nad maximální MTU 1500. To by vyžadovalo fragmentaci zpráv 1 a 2 a byla by to velká komplikace. Pravděpodobně to nebudeme dělat.

Relay a Peer Test: Viz výše

TODO: Existuje efektivnější způsob definování podepisování/ověřování, aby se předešlo kopírování podpisu?

TODO

[IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/) sekce 8.1 zakazuje HashML-DSA v X.509 certifikátech a nepřiřazuje OID pro HashML-DSA kvůli implementační složitosti a snížené bezpečnosti.

### Ostatní specifikace

Pro PQ-only podpisy souborů SU3 použijte OID definované v [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/) pro varianty bez prehash pro certifikáty. Nedefinujeme hybridní podpisy souborů SU3, protože bychom možná museli soubory hashovat dvakrát (ačkoli HashML-DSA a X2559 používají stejnou hash funkci SHA512). Také by zřetězení dvou klíčů a podpisů v X.509 certifikátu bylo zcela nestandardní.

Všimněte si, že nepovolujeme Ed25519 podepisování SU3 souborů, a ačkoli jsme definovali Ed25519ph podepisování, nikdy jsme se nedohodli na OID pro něj, ani jsme ho nepoužili.

- SAMv3
- Bittorrent
- Pokyny pro vývojáře
- Pojmenování / adresář / skokové servery
- Ostatní dokumenty

## Analýza režie

### Výměna klíčů

Běžné typy sig jsou pro SU3 soubory zakázané; používejte varianty ph (prehash).

| Typ | Pubkey (Zpráva 1) | Cipertext (Zpráva 2) |
|------|----------------|-------------------|
| MLKEM512_X25519 | +816 | +784 |
| MLKEM768_X25519 | +1200 | +1104 |
| MLKEM1024_X25519 | +1584 | +1584 |
Nová maximální velikost Destination bude 2599 (3468 v base 64).

Aktualizujte další dokumenty, které poskytují pokyny ohledně velikostí Destination, včetně:

| Typ | Relativní rychlost |
|------|----------------|
| X25519 DH/keygen | základní |
| MLKEM512 | 2,25x rychlejší |
| MLKEM768 | 1,5x rychlejší |
| MLKEM1024 | 1x (stejná) |
| XK | 4x DH (keygen + 3 DH) |
| MLKEM512_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 4,9x DH = 22% pomalejší |
| MLKEM768_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 5,3x DH = 32% pomalejší |
| MLKEM1024_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 6x DH = 50% pomalejší |
Zvýšení velikosti (bajty):

| Typ | Relativní DH/encaps | DH/decaps | keygen |
|------|-------------------|-----------|--------|
| X25519 | základ | základ | základ |
| MLKEM512 | 29x rychlejší | 22x rychlejší | 17x rychlejší |
| MLKEM768 | 17x rychlejší | 14x rychlejší | 9x rychlejší |
| MLKEM1024 | 12x rychlejší | 10x rychlejší | 6x rychlejší |
### Podpisy

#### Velikosti

Rychlosti podle zprávy od [Cloudflare](https://blog.cloudflare.com/pq-2024/):

| Typ | Pubkey | Sig | Key+Sig | RIdent | Dest | RInfo | LS/Streaming/Datagram (každá zpráva) |
|------|--------|-----|---------|--------|------|-------|----------------------------------|
| EdDSA_SHA512_Ed25519 | 32 | 64 | 96 | 391 | 391 | baseline | baseline |
| MLDSA44 | 1312 | 2420 | 3732 | 1351 | 1319 | +3316 | +3284 |
| MLDSA65 | 1952 | 3309 | 5261 | 1991 | 1959 | +5668 | +5636 |
| MLDSA87 | 2592 | 4627 | 7219 | 2631 | 2599 | +7072 | +7040 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 1344 | 2484 | 3828 | 1383 | 1351 | +3412 | +3380 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 1984 | 3373 | 5357 | 2023 | 1991 | +5668 | +5636 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 2624 | 4691 | 7315 | 2663 | 2631 | +7488 | +7456 |
#### Rychlosti

Aktualizujte další dokumenty, které poskytují pokyny ohledně velikostí Destination, včetně:

| Typ | Relativní rychlost podpisu | ověření |
|------|---------------------|--------|
| EdDSA_SHA512_Ed25519 | základní | základní |
| MLDSA44 | 5x pomalejší | 2x rychlejší |
| MLDSA65 | ??? | ??? |
| MLDSA87 | ??? | ??? |
Zvýšení velikosti (bajty):

| Typ | Relativní rychlost podpisu | ověření | generování klíčů |
|------|---------------------------|---------|------------------|
| EdDSA_SHA512_Ed25519 | výchozí | výchozí | výchozí |
| MLDSA44 | 4,6x pomalejší | 1,7x rychlejší | 2,6x rychlejší |
| MLDSA65 | 8,1x pomalejší | stejné | 1,5x rychlejší |
| MLDSA87 | 11,1x pomalejší | 1,5x pomalejší | stejné |
## Analýza zabezpečení

Typické velikosti klíčů, podpisů, RIdent, Dest nebo nárůsty velikostí (Ed25519 uvedeno pro referenci) za předpokladu typu šifrování X25519 pro RI. Přidaná velikost pro Router Info, LeaseSet, odpověditelné datagramy a každý ze dvou streaming paketů (SYN a SYN ACK) uvedených v seznamu. Současné Destinations a Leasesets obsahují opakované padding a jsou kompresovatelné při přenosu. Nové typy neobsahují padding a nebudou kompresovatelné, což povede k mnohem většímu nárůstu velikosti při přenosu. Viz sekce návrhu výše.

| Kategorie | Stejně bezpečná jako |
|-----------|---------------------|
| 1 | AES128 |
| 2 | SHA256 |
| 3 | AES192 |
| 4 | SHA384 |
| 5 | AES256 |
### Handshakes

Rychlosti jak uvádí [Cloudflare](https://blog.cloudflare.com/pq-2024/):

Předběžné výsledky testů v Javě:

| Algoritmus | Kategorie zabezpečení |
|------------|----------------------|
| MLKEM512 | 1 |
| MLKEM768 | 3 |
| MLKEM1024 | 5 |
### Podpisy

Bezpečnostní kategorie NIST jsou shrnuty v [NIST prezentaci](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf) na slidě 10. Předběžná kritéria: Naše minimální bezpečnostní kategorie NIST by měla být 2 pro hybridní protokoly a 3 pro PQ-only.

Všechny tyto protokoly jsou hybridní. Implementace by měly upřednostňovat MLKEM768; MLKEM512 není dostatečně bezpečný.

| Algoritmus | Kategorie zabezpečení |
|-----------|---------------------|
| MLDSA44 | 2 |
| MLKEM67 | 3 |
| MLKEM87 | 5 |
## Předvolby typů

Bezpečnostní kategorie NIST [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf):

Tento návrh definuje jak hybridní, tak pouze PQ typy podpisů. MLDSA44 hybridní je preferována před MLDSA65 pouze PQ. Velikosti klíčů a podpisů pro MLDSA65 a MLDSA87 jsou pro nás pravděpodobně příliš velké, alespoň zpočátku.

Bezpečnostní kategorie NIST [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf):

Zatímco definujeme a implementujeme 3 kryptografické a 9 typů podpisů, plánujeme měřit výkon během vývoje a dále analyzovat účinky zvětšených velikostí struktur. Budeme také pokračovat ve výzkumu a sledování vývoje v ostatních projektech a protokolech.

Po roce nebo více vývoje se pokusíme dohodnout na preferovaném typu nebo výchozím nastavení pro každý případ použití. Výběr bude vyžadovat kompromisy mezi šířkou pásma, CPU a odhadovanou úrovní zabezpečení. Všechny typy nemusí být vhodné nebo povolené pro všechny případy použití.

Předběžné preference jsou následující, mohou se změnit:

Encryption: MLKEM768_X25519

## Poznámky k implementaci

### Podpora knihoven

Signatures: MLDSA44_EdDSA_SHA512_Ed25519

Předběžná omezení jsou následující a mohou se změnit:

### Varianty podepisování

Šifrování: MLKEM1024_X25519 není povoleno pro SSU2

Podpisy: MLDSA87 a hybridní varianta pravděpodobně příliš velké; MLDSA65 a hybridní varianta mohou být příliš velké

### Spolehlivost

Knihovny Bouncycastle, BoringSSL a WolfSSL nyní podporují MLKEM a MLDSA. Podpora OpenSSL bude v jejich vydání 3.5 dne 8. dubna 2025 [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

### Velikosti struktur

Noise knihovna z southernstorm.com adaptovaná pro Java I2P obsahovala předběžnou podporu pro hybridní handshaky, ale odstranili jsme ji jako nepoužívanou; budeme ji muset přidat zpět a aktualizovat tak, aby odpovídala [specifikaci Noise HFS](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf).

### NetDB

Budeme používat "hedged" nebo randomizovanou variantu podpisování, nikoli "deterministickou" variantu, jak je definována v [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) sekci 3.4. To zajišťuje, že každý podpis je odlišný, i když se podepisují stejná data, a poskytuje dodatečnou ochranu proti útokům postranními kanály. Zatímco [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) specifikuje, že "hedged" varianta je výchozí, nemusí to být pravda v různých knihovnách. Implementátoři musí zajistit, že se pro podpisování používá "hedged" varianta.

### Ratchet

#### Problémy

Používáme běžný proces podepisování (nazývaný Pure ML-DSA Signature Generation), který interně kóduje zprávu jako 0x00 || len(ctx) || ctx || message, kde ctx je nějaká volitelná hodnota o velikosti 0x00..0xFF. Nepoužíváme žádný volitelný kontext. len(ctx) == 0. Tento proces je definován v [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) Algorithm 2 krok 10 a Algorithm 3 krok 5. Všimněte si, že některé publikované testovací vektory mohou vyžadovat nastavení režimu, kde zpráva není kódována.

Zvýšení velikosti povede k mnohem větší fragmentaci tunelů pro NetDB úložiště, streaming handshakes a další zprávy. Zkontrolujte změny výkonu a spolehlivosti.

- Pokud je zpráva 1 menší než 919 bajtů, jedná se o aktuální protokol ratchet.
- Pokud je zpráva 1 větší nebo rovna 919 bajtům, pravděpodobně se jedná o MLKEM512_X25519.
  Nejprve zkuste MLKEM512_X25519 a pokud selže, zkuste aktuální protokol ratchet.

Najděte a zkontrolujte jakýkoli kód, který omezuje velikost v bajtech u router infos a leasesets.

Zkontrolovat a případně snížit maximální počet LS/RI uložených v RAM nebo na disku, aby se omezil nárůst úložiště. Zvýšit minimální požadavky na šířku pásma pro floodfilly?

- X25519 + MLKEM512
- X25519 + MLKEM768
- X25519 + MLKEM1024

Automatická klasifikace/detekce více protokolů na stejných tunnelech by měla být možná na základě kontroly délky zprávy 1 (New Session Message). Použitím MLKEM512_X25519 jako příkladu je zpráva 1 o 816 bajtů delší než současný ratchet protokol a minimální velikost zprávy 1 (pouze s DateTime payload) je 919 bajtů. Většina velikostí zprávy 1 se současným ratchet má payload menší než 816 bajtů, takže mohou být klasifikovány jako non-hybrid ratchet. Velké zprávy jsou pravděpodobně POST požadavky, které jsou vzácné.

- Více než jeden MLKEM
- ElG + jeden nebo více MLKEM
- X25519 + jeden nebo více MLKEM
- ElG + X25519 + jeden nebo více MLKEM

Doporučená strategie je tedy:

To nám umožní efektivně podporovat standardní ratchet a hybridní ratchet na stejné destinaci, stejně jako jsme předtím podporovali ElGamal a ratchet na stejné destinaci. Proto můžeme migrovat na hybridní protokol MLKEM mnohem rychleji, než kdybychom nemohli podporovat duální protokoly pro stejnou destinaci, protože můžeme přidat podporu MLKEM do existujících destinací.

Požadované podporované kombinace jsou:

Následující kombinace mohou být složité a NENÍ vyžadováno, aby byly podporovány, ale mohou být, v závislosti na implementaci:

#### Sdílené tunnely

Možná se nebudeme pokoušet podporovat více MLKEM algoritmů (například MLKEM512_X25519 a MLKEM_768_X25519) na stejné destinaci. Vyberte pouze jeden; to však závisí na tom, že vybereme preferovanou MLKEM variantu, aby ji mohly používat HTTP klientské tunnely. Závisí na implementaci.

#### Forward Secrecy

MŮŽEME se pokusit podporovat tři algoritmy (například X25519, MLKEM512_X25519 a MLKEM769_X25519) na stejné destinaci. Klasifikace a strategie opakování může být příliš složitá. Konfigurace a konfigurační UI může být příliš složité. Závisí na implementaci.

### NTCP2

Pravděpodobně se NEBUDEME pokoušet podporovat algoritmy ElGamal a hybrid na stejné destinaci. ElGamal je zastaralý a ElGamal + hybrid pouze (bez X25519) nedává příliš smysl. Také ElGamal i Hybrid New Session Messages jsou obě velké, takže strategie klasifikace by často musely zkoušet obě dešifrování, což by bylo neefektivní. Závisí na implementaci.

#### Velikost nové relace

Klienti mohou používat stejné nebo různé X25519 statické klíče pro X25519 a hybridní protokoly na stejných tunelech, závisí na implementaci.

Specifikace ECIES umožňuje Garlic Messages v datové části New Session Message, což umožňuje 0-RTT doručení počátečního streamovacího paketu, obvykle HTTP GET, společně s leaseset klienta. Datová část New Session Message však nemá forward secrecy. Jelikož tento návrh klade důraz na rozšířenou forward secrecy pro ratchet, implementace mohou nebo by měly odložit zahrnutí streamovací datové části, nebo celé streamovací zprávy, až do první Existing Session Message. To by bylo na úkor 0-RTT doručení. Strategie mohou také záviset na typu provozu nebo typu tunelu, nebo například na GET vs. POST. Závislé na implementaci.

MLKEM, MLDSA, nebo obojí na stejném cíli dramaticky zvýší velikost New Session Message, jak je popsáno výše. To může výrazně snížit spolehlivost doručování New Session Message přes tunely, kde musí být fragmentovány do více tunnel zpráv o velikosti 1024 bajtů. Úspěšnost doručení je úměrná exponenciálnímu počtu fragmentů. Implementace mohou používat různé strategie pro omezení velikosti zprávy na úkor 0-RTT doručování. Závislé na implementaci.

Poznámka: Kódy typů jsou pouze pro interní použití. Routery zůstanou typu 4 a podpora bude uvedena v adresách routerů.

### SSU2

Nastavujeme MSB dočasného klíče (key[31] & 0x80) v požadavku na relaci pro označení, že se jedná o hybridní připojení. To nám umožňuje provozovat standardní NTCP i hybridní NTCP na stejném portu. Byla by podporována pouze jedna hybridní varianta a inzerována v adrese routeru. Například v=2,3 nebo v=2,4 nebo v=2,5.

Jako Bob, otestujte, zda (X[31] & 0x80) != 0 po de-obfuskaci. Pokud ano, jedná se o PQ spojení.

Poznámka: Kódy typů jsou pouze pro interní použití. Routery zůstanou typu 4 a podpora bude uvedena v adresách routerů.

## Kompatibilita routerů

### Názvy transportů

Minimální verze routeru vyžadovaná pro NTCP2-PQ bude určena později.

### Typy šifrování routeru

Používáme pole verze v dlouhé hlavičce a nastavujeme ji na 3 pro MLKEM512 a 4 pro MLKEM768. v=2,3,4 v adrese by bylo dostačující.

#### Obfuskace

Zkontrolujte a ověřte, že SSU2 dokáže zpracovat MLDSA-podepsaný RI fragmentovaný napříč několika pakety (6-8?).

#### Routery typu 5/6/7

Poznámka: Kódy typů jsou určeny pouze pro interní použití. Routery zůstanou typu 4 a podpora bude označena v adresách routeru.

#### Type 4 Routers

Ve všech případech používejte názvy transportů NTCP2 a SSU2 jako obvykle.

### Typy podpisů routeru

#### Doporučení

Máme několik alternativ k zvážení:

Nedoporučuje se. Používejte pouze nové transporty uvedené výše, které odpovídají typu routeru. Starší routery se nemohou připojit, budovat tunnely přes ně nebo posílat netDb zprávy. Trvalo by několik cyklů vydání, než by se vyladily chyby a zajistila podpora před výchozím povolením. Mohlo by to prodloužit zavedení o rok nebo více oproti níže uvedeným alternativám.

### Typy šifrování LS

#### Routery typu 12-17

Doporučeno. Jelikož PQ neovlivňuje statický klíč X25519 ani protokoly N handshake, mohli bychom ponechat routery jako typ 4 a pouze inzerovat nové transporty. Starší routery by se stále mohly připojit, budovat tunely skrze ně nebo jim posílat netDb zprávy.

MLKEM-768 je doporučeno pro Ratchet, NTCP2 a SSU2 jako nejlepší rovnováha mezi bezpečností a délkou klíče.

### Typy podpisů cíle

#### Klíče LS typu 5-7

Starší routery ověřují RI a proto se nemohou připojit, budovat tunely skrz ně, nebo jim posílat netDb zprávy. Trvalo by několik cyklů vydání na ladění a zajištění podpory před výchozím povolením. Byly by to stejné problémy jako při zavedení enc. type 5/6/7; mohlo by prodloužit zavedení o rok nebo více oproti výše uvedené alternativě zavedení enc. type 4.

Nedoporučuje se. Používejte pouze nové transporty uvedené výše, které odpovídají typu routeru. Starší routery se nemohou připojit, budovat tunnely přes ně nebo posílat netDb zprávy. Trvalo by několik cyklů vydání, než by se vyladily chyby a zajistila podpora před výchozím povolením. Mohlo by to prodloužit zavedení o rok nebo více oproti níže uvedeným alternativám.

## Priority a zavedení

Žádné alternativy.

Destinations mohou podporovat více typů klíčů, ale pouze tak, že provádějí zkušební dešifrování zprávy 1 s každým klíčem. Režii lze zmírnit udržováním počtu úspěšných dešifrování pro každý klíč a nejprve zkusit nejpoužívanější klíč. Java I2P používá tuto strategii pro ElGamal+X25519 na stejné destination.

Routery ověřují podpisy leaseset a nemohou se proto připojit nebo přijímat leasesety pro destinace typu 12-17. Vyžadovalo by to několik vydání pro ladění a zajištění podpory před aktivací jako výchozí nastavení.

Žádné alternativy.

Nejcennější data jsou end-to-end provoz, šifrovaný pomocí ratchet. Jako externí pozorovatel mezi skoky tunelu je to šifrováno dvakrát navíc - tunelovou a transportní šifrou. Jako externí pozorovatel mezi OBEP a IBGW je to šifrováno pouze jednou navíc transportní šifrou. Jako účastník OBEP nebo IBGW je ratchet jedinou šifrou. Protože jsou však tunely jednosměrné, zachycení obou zpráv v ratchet handshake by vyžadovalo spolupracující routery, pokud by nebyly tunely vybudovány s OBEP a IBGW na stejném routeru.

Hrozba PQ spočívající v prolomení autentizačních klíčů v rozumném časovém období (řekněme několik měsíců) a následném vydávání se za autentizaci nebo dešifrování téměř v reálném čase, je mnohem vzdálenější? A to je doba, kdy bychom chtěli přejít na PQC statické klíče.

Práce na podpoře podpisů MLDSA v I2P jsou pozastaveny do konce roku 2027 nebo roku 2028, a to v závislosti na výsledcích standardizačních organizací, které mají vybrat algoritmy, případně snížit velikost klíčů a/nebo podpisů a podpořit jejich přijetí v průmyslu. Viz [CABFORUM](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/), [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/) a [PLANTS](https://datatracker.ietf.org/wg/plants/about/). Navíc bude přijetí MLDSA v průmyslu standardizováno IETF, CA/Browser Forum a certifikačními autoritami. Certifikační autority nejprve potřebují podporu modulů hardwarové bezpečnosti (HSM), která v současnosti není k dispozici [CA/Browser Forum](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/). Očekáváme, že IETF a CA/Browser Forum budou rozhodovat o konkrétních volbách parametrů, včetně toho, zda budou podporovat nebo vyžadovat kompozitní podpisy [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/).

| Milník | Cíl |
|--------|-----|
| Ratchet beta | Konec 2025 |
| Výběr nejlepšího typu šifrování | Začátek 2026 |
| NTCP2 beta | Začátek 2026 |
| SSU2 beta | Polovina 2026 |
| Ratchet produkce | Polovina 2026 |
| Ratchet výchozí | Konec 2026 |
| Signature beta | Konec 2026 |
| NTCP2 produkce | Konec 2026 |
| SSU2 produkce | Začátek 2027 |
| Výběr nejlepšího typu podpisu | Začátek 2027 |
| NTCP2 výchozí | Začátek 2027 |
| SSU2 výchozí | Polovina 2027 |
| Signature produkce | Polovina 2027 |
## Migrace

Ratchet má nejvyšší prioritu. Transporty jsou další. Podpisy mají nejnižší prioritu.

Zavedení podpisů bude také o rok nebo více později než zavedení šifrování, protože není možná zpětná kompatibilita. Také přijetí MLDSA v průmyslu bude standardizováno CA/Browser Forum a certifikačními autoritami. CA nejprve potřebují podporu hardwarových bezpečnostních modulů (HSM), která momentálně není dostupná [CA/Browser Forum](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/). Očekáváme, že CA/Browser Forum bude řídit rozhodnutí o konkrétních volbách parametrů, včetně toho, zda podporovat nebo vyžadovat kompozitní podpisy [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/).

## Problémy

SHA256 by mělo být bezpečné dalších 20–30 let a není ohroženo kvantovými počítači. Viz [prezentace NIST](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf) a [prezentace NCCOE](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf). Pokud by SHA256 bylo prolomeno, budeme mít vážnější problémy (např. s netDb).

## Reference

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
* [NTCP2](/docs/specs/ntcp2/)
* [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)
* [Prop165](/docs/proposals/165/)
* [PQ-WIREGUARD](https://eprint.iacr.org/2020/379.pdf)
* [RFC-2104](https://tools.ietf.org/html/rfc2104)
* [Rosenpass](https://rosenpass.eu/)
* [Rosenpass-Whitepaper](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf)
* [SSH-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-sshm-mlkem-hybrid-kex/)
* [SSU2](/docs/specs/ssu2/)
* [TLS-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-tls-hybrid-design/)
