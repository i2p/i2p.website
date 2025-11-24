---
title: "Post-kvantové kryptografické protokoly"
number: "169"
author: "zzz, orignal, drzed, eyedeekay"
created: "2025-01-21"
lastupdated: "2025-06-12"
status: "Otevřený"
thread: "http://zzz.i2p/topics/3294"
target: "0.9.80"
---

## Přehled

Zatímco výzkum a soutěž pro vhodnou post-kvantovou (PQ)
kryptografii pokračují desítku let, možnosti
nebyly jasné až donedávna.

Začali jsme zkoumat důsledky PQ kryptografie
v roce 2022 [FORUM](http://zzz.i2p/topics/3294).

Standardy TLS přidaly podporu pro hybridní šifrování v posledních dvou letech a nyní jsou používány pro značnou část šifrovaného provozu na internetu díky podpoře v Chrome a Firefox [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/).

NIST nedávno finalizoval a zveřejnil doporučené algoritmy
pro post-kvantovou kryptografii [NIST-PQ](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards).
Několik běžných kryptografických knihoven nyní podporuje standardy NIST
nebo bude podporu brzy vydávat.

Oba [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/) a [NIST-PQ](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards) doporučují, aby migrace začala okamžitě.
Viz také NSA PQ FAQ z roku 2022 [NSA-PQ](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF).
I2P by mělo být lídrem v oblasti bezpečnosti a kryptografie.
Nyní je čas implementovat doporučené algoritmy.
Pomocí našeho flexibilního systému typů kryptografií a typů podpisů,
přidáme typy pro hybridní kryptografii a pro PQ a hybridní podpisy.

## Cíle

- Vybrat algoritmy odolné proti PQ
- Přidat pouze PQ a hybridní algoritmy do I2P protokolů tam, kde je to vhodné
- Definovat více variant
- Vybrat nejlepší varianty po implementaci, testování, analýze a výzkumu
- Přidávat podporu postupně a s kompatibilitou směrem zpět

## Necíle

- Neměnit jednosměrné (hluk N) šifrovací protokoly
- Neměnit SHA256, krátkodobě neohrožené PQ
- Nevybírat v této době konečné preferované varianty

## Model hrozeb

- Směrovače na OBEP nebo IBGW, případně spolupracující,
  uchovávající česnekové zprávy pro pozdější dešifrování (budoucí tajemství)
- Pozorovatelé sítě
  uchovávající zprávy o přepravě pro pozdější dešifrování (budoucí tajemství)
- Účastníci sítě falšující podpisy pro RI, LS, streamování, datagramy
  nebo jiné struktury

## Dotčené protokoly

Změníme následující protokoly, zhruba v pořadí
vývoje. Celkové zpřístupnění pravděpodobně proběhne od konce roku 2025 do poloviny roku 2027.
Podrobnosti naleznete v sekci Priorities and Rollout níže.


| Protokol / Funkce | tav |
| ----------------- | --- |
| Hybridní MLKEM Ratchet a LS | Schvál |
| Hybridní MLKEM NTCP2 | Někter |
| Hybridní MLKEM SSU2 | Někter |
| MLDSA SigTypes 12-14 | Návrh |
| MLDSA Dests | Testov |
| Hybridní SigTypes 15-17 | Předbě |
| Hybridní Dests |  |




## Design

Budeme podporovat standardy NIST FIPS 203 a 204 [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf),
které jsou založeny na, ale nejsou kompatibilní s,
CRYSTALS-Kyber a CRYSTALS-Dilithium (verze 3.1, 3 a starší).

### Výměna klíčů

Budeme podporovat hybridní výměnu klíčů v následujících protokolech:

| Proto | Typ Noise | Podporuje pouze | ?  Podporuje Hy |
| ----- | --------- | --------------- | --------------- |
| NTCP2 | XK | ne | ano |
| SSU2 | XK | ne | ano |
| Ratchet | IK | ne | ano |
| TBM | N | ne | ne |
| NetDB | N | ne | ne |


PQ KEM poskytuje pouze efemérní klíče, a nepodporuje přímo
handshake pomocí statických klíčů jako je Noise XK a IK.

Noise N nepoužívá obousměrnou výměnu klíčů a tak není vhodná
pro hybridní šifrování.

Takže budeme podporovat pouze hybridní šifrování, pro NTCP2, SSU2 a Ratchet.
Definujeme tři varianty ML-KEM jak je uvedeno v [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf),
pro celkem 3 nové typy šifrování.
Hybridní typy budou definovány pouze v kombinaci s X25519.

Nové typy šifrování jsou:

| Typ | Kód |
| --- | --- |
| MLKEM512_X25519 | 5 |
| MLKEM768_X25519 | 6 |
| MLKEM1024_X25519 | 7 |


Režie bude značná. Typické velikosti zpráv 1 a 2 (pro XK a IK)
jsou v současnosti kolem 100 bajtů (před jakýmikoli dalšími údaji o zátěži).
To se zvýší o 8x až 15x v závislosti na algoritmu.


### Podpisy

Budeme podporovat PQ a hybridní podpisy v následujících strukturách:

| Typ | Podporuje pouze | ?  Podporuje Hy |
| --- | --------------- | --------------- |
| RouterInfo | ano | ano |
| LeaseSet | ano | ano |
| Streamová SYN/SYNACK/Close | ano | ano |
| Datagramy opakovaného odes | ní    ano | ano |
| Datagram2 (návrh 163) | ano | ano |
| I2CP vytváří zprávu o rela | ano | ano |
| SU3 soubory | ano | ano |
| X.509 certifikáty | ano | ano |
| Java keystore | ano | ano |



Takže budeme podporovat jak pouze PQ, tak hybridní podpisy.
Definujeme tři varianty ML-DSA jak je uvedeno v [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf),
tři hybridní varianty s Ed25519,
a tři pouze PQ varianty s prehash pro SU3 soubory pouze,
pro celkem 9 nových typů podpisů.
Hybridní typy budou definovány pouze v kombinaci s Ed25519.
Budeme používat standardní ML-DSA, NE předem hašované varianty (HashML-DSA),
kromě SU3 souborů.

Použijeme variantu "hedged" nebo náhodného podepisování,
nikoliv variantu "deterministické", jak je definováno v [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) sekce 3.4.
Toto zajišťuje, že každý podpis je jiný, i když pro stejná data,
a poskytuje dodatečnou ochranu proti útokům modelu side-channel.
Viz sekci implementačních poznámek níže pro další podrobnosti
o výběru algoritmu včetně kódování a kontextu.

Nové typy podpisů jsou:

| Typ | ód |
| --- | --- |
| MLDSA44 | 12 |
| MLDSA65 | 13 |
| MLDSA87 | 14 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 |
| MLDSA44ph | 18 |
| MLDSA65ph | 19 |
| MLDSA87ph | 20 |


X.509 certifikáty a další DER kódování budou používat
kompozitní struktury a OID definované v [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ounsworth-pq-composite-sigs/).

Režie bude značná. Typické velikosti cílů a směrovacích identit Ed25519
jsou 391 bajtů.
Tyto se zvýší o 3,5x až 6,8x v závislosti na algoritmu.
Ed25519 podpisy mají 64 bajtů.
Tyto se zvýší o 38x až 76x v závislosti na algoritmu.
Typicky podepsaná RouterInfo, LeaseSet, datagramy opakovaného odeslání a podepsané zprávy streamování mají kolem 1 KB.
Tyto se zvýší o 3x až 8x v závislosti na algoritmu.

Jelikož nové typy cílů a směrovací identity nebudou obsahovat vycpávky,
nebudou komprimovatelné. Velikosti cílů a identit routeru,
které jsou během přepravy gzipovány, se zvýší o 12x - 38x v závislosti na algoritmu.

### Legální kombinace

Pro Cíle jsou nové typy podpisů podporovány se všemi typy šifrování v leasesetu. Nastavte typ šifrování v klíčovém certifikátu na NONE (255).

Pro RouterIdentities, je typ šifrování ElGamal zastaralý.
Nové typy podpisů jsou podporovány pouze se šifrováním X25519 (typ 4).
Nové typy šifrování budou označeny v RouterAddresses.
Typ šifrování v klíčovém certifikátu zůstane typ 4.

### Vyžadována nová kryptografie

- ML-KEM (dříve CRYSTALS-Kyber) [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
- ML-DSA (dříve CRYSTALS-Dilithium) [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)
- SHA3-128 (dříve Keccak-256) [FIPS202]_ Použito pouze pro SHAKE128
- SHA3-256 (dříve Keccak-512) [FIPS202]_
- SHAKE128 a SHAKE256 (XOF rozšíření na SHA3-128 a SHA3-256) [FIPS202]_

Testovací vektory pro SHA3-256, SHAKE128 a SHAKE256 jsou k dispozici na [NIST-VECTORS]_.

Poznámka: Java bouncycastle knihovna podporuje vše výše uvedené.
Podpora C++ knihoven je v OpenSSL 3.5 [OPENSSL]_.

### Alternativy

Nepodporujeme [FIPS205]_ (Sphincs+), je mnohem pomalejší a větší než ML-DSA.
Nepodporujeme připravovaný FIPS206 (Falcon), ještě není standardizován.
Nepodporujeme NTRU nebo jiné kandidáty PQ, kteří nebyli standardizováni NIST.

Rosenpass
`````````

Existuje nějaký výzkum [PQ-WIREGUARD]_ na přizpůsobení Wireguarda (IK)
pro čistě PQ kryptografii, ale v tomto dokumentu je několik otevřených otázek.
Později byl tento přístup implementován jako Rosenpass [Rosenpass]_ [Rosenpass-Whitepaper]_
pro PQ Wireguard.

Rosenpass používá handshake podobný Noise KK s předpoužitím statických klíčů Classic McEliece 460896 (každý 500 KB) a efemerními klíči Kyber-512 (prakticky MLKEM-512).
Jelikož šifrované texty Classic McEliece mají pouze 188 bajtů, a veřejné klíče a šifrové texty Kyber-512 jsou rozumné, obě handshake zprávy se vejdou do standardní UDP MTU.
Výstupní sdílený klíč (osk) z PQ KK handshaku se použije jako vstupní předpoužitý klíč (psk)
pro standardní Wireguard IK handshake.
Takže výsledkem je, že se provádějí dva kompletní handshake, jeden čistě PQ a jeden čistě X25519.

Nemůžeme udělat nic z toho, abychom nahradili naše XK a IK handshaky, protože:

- Nemůžeme udělat KK, Bob nemá statický klíč Alice
- 500 KB statické klíče jsou příliš velké
- Nechceme další okruh

V dokumentu bílé knihy je mnoho dobrých informací,
a budeme je přezkoumávat pro nápady a inspiraci. TODO.

## Specifikace

### Běžné struktury

Aktualizujte sekce a tabulky v dokumentu obecných struktur [COMMON](https://geti2p.net/spec/common-structures) takto:

PublicKey
````````````````

Nové typy veřejného klíče jsou:

| Typ | élka veřejného kl | če Od | Použi |
| --- | ----------------- | ----- | ----- |
| MLKEM512_X25519 | 32 | 0.9.xx | Viz n |
| MLKEM768_X25519 | 32 | 0.9.xx | Viz n |
| MLKEM1024_X25519 | 32 | 0.9.xx | Viz n |
| MLKEM512 | 800 | 0.9.xx | Viz n |
| MLKEM768 | 1184 | 0.9.xx | Viz n |
| MLKEM1024 | 1568 | 0.9.xx | Viz n |
| MLKEM512_CT | 768 | 0.9.xx | Viz n |
| MLKEM768_CT | 1088 | 0.9.xx | Viz n |
| MLKEM1024_CT | 1568 | 0.9.xx | Viz n |
| NONE | 0 | 0.9.xx | Viz n |


Hybridní veřejné klíče jsou klíče X25519.
Veřejné klíče KEM jsou efemérní PQ klíče odeslané od Alice k Bobovi.
Kódování a pořadí bajtů jsou definovány v [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

Klíče MLKEM*_CT nejsou pravými veřejnými klíči, jsou "šifrovanými texty" odeslanými od Boba k Alice v Noise handshaku.
Jsou zde uvedeny pro úplnost.

PrivateKey
````````````````

Nové typy privátních klíčů jsou:

| Typ | élka privátního kl | če Od | Použi |
| --- | ------------------ | ----- | ----- |
| MLKEM512_X25519 | 32 | 0.9.xx | Viz n |
| MLKEM768_X25519 | 32 | 0.9.xx | Viz n |
| MLKEM1024_X25519 | 32 | 0.9.xx | Viz n |
| MLKEM512 | 1632 | 0.9.xx | Viz n |
| MLKEM768 | 2400 | 0.9.xx | Viz n |
| MLKEM1024 | 3168 | 0.9.xx | Viz n |


Hybridní privátní klíče jsou klíče X25519.
Privátní klíče KEM jsou pouze pro Alici.
Kódování KEM a pořadí bajtů jsou definovány v [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

SigningPublicKey
````````````````

Nové typy veřejného klíče pro podepisování jsou:

| Typ | élka (bajty) | d | oužit |
| --- | ------------ | --- | ----- |
| MLDSA44 | 1312 | 0.9.xx | Viz n |
| MLDSA65 | 1952 | 0.9.xx | Viz n |
| MLDSA87 | 2592 | 0.9.xx | Viz n |
| MLDSA44_EdDSA_SHA512_Ed25519 | 1344 | 0.9.xx | Viz n |
| MLDSA65_EdDSA_SHA512_Ed25519 | 1984 | 0.9.xx | Viz n |
| MLDSA87_EdDSA_SHA512_Ed25519 | 2624 | 0.9.xx | Viz n |
| MLDSA44ph | 1344 | 0.9.xx | Pouze |
| MLDSA65ph | 1984 | 0.9.xx | Pouze |
| MLDSA87ph | 2624 | 0.9.xx | Pouze |


Hybridní veřejné klíče pro podepisování jsou klíč Ed25519 následovaný PQ klíčem, jak je uvedeno v [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ounsworth-pq-composite-sigs/).
Kódování a pořadí bajtů jsou definovány v [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

SigningPrivateKey
`````````````````

Nové typy privátních klíčů pro podepisování jsou:

| Typ | élka (bajty) | d | oužit |
| --- | ------------ | --- | ----- |
| MLDSA44 | 2560 | 0.9.xx | Viz n |
| MLDSA65 | 4032 | 0.9.xx | Viz n |
| MLDSA87 | 4896 | 0.9.xx | Viz n |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2592 | 0.9.xx | Viz n |
| MLDSA65_EdDSA_SHA512_Ed25519 | 4064 | 0.9.xx | Viz n |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4928 | 0.9.xx | Viz n |
| MLDSA44ph | 2592 | 0.9.xx | Pouze |
| MLDSA65ph | 4064 | 0.9.xx | Pouze |
| MLDSA87ph | 4928 | 0.9.xx | Pouze |


Hybridní privátní klíče pro podepisování jsou klíč Ed25519 následovaný PQ klíčem, jak je uvedeno v [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ounsworth-pq-composite-sigs/).
Kódování a pořadí bajtů jsou definovány v [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

Signature
``````````

Nové typy podpisů jsou:

| Typ | élka (bajty) | d | oužit |
| --- | ------------ | --- | ----- |
| MLDSA44 | 2420 | 0.9.xx | Viz n |
| MLDSA65 | 3309 | 0.9.xx | Viz n |
| MLDSA87 | 4627 | 0.9.xx | Viz n |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2484 | 0.9.xx | Viz n |
| MLDSA65_EdDSA_SHA512_Ed25519 | 3373 | 0.9.xx | Viz n |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4691 | 0.9.xx | Viz n |
| MLDSA44ph | 2484 | 0.9.xx | Pouze |
| MLDSA65ph | 3373 | 0.9.xx | Pouze |
| MLDSA87ph | 4691 | 0.9.xx | Pouze |


Hybridní podpisy jsou podpis Ed25519 následovaný PQ podpisem, jak je uvedeno v [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ounsworth-pq-composite-sigs/).
Hybridní podpisy se ověřují ověřením obou podpisů, a selžou
pokud jeden z nich selže.
Kódování a pořadí bajtů jsou definovány v [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

Key Certificates
````````````````

Nové typy veřejného klíče pro podepisování jsou:

| Typ | ypový kód | elková délka veřejného | íče  O |  |
| --- | --------- | ---------------------- | ------ | --- |
| MLDSA44 | 12 | 1312 | 0.9.xx | Viz n |
| MLDSA65 | 13 | 1952 | 0.9.xx | Viz n |
| MLDSA87 | 14 | 2592 | 0.9.xx | Viz n |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 0.9.xx | Viz n |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 0.9.xx | Viz n |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 0.9.xx | Viz n |
| MLDSA44ph | 18 | n/a | 0.9.xx | Pouze |
| MLDSA65ph | 19 | n/a | 0.9.xx | Pouze |
| MLDSA87ph | 20 | n/a | 0.9.xx | Pouze |




Nové typy veřejného kryptografického klíče jsou:

| Typ | ypový kód | Celková délka veřejného | klíče |  |
| --- | --------- | ----------------------- | ----- | --- |
| MLKEM512_X25519 | 5 | 32 | 0.9.xx | Viz n |
| MLKEM768_X25519 | 6 | 32 | 0.9.xx | Viz n |
| MLKEM1024_X25519 | 7 | 32 | 0.9.xx | Viz n |
| NONE | 255 | 0 | 0.9.xx | Viz n |



Hybridní typy klíčů NIKDY nejsou zahrnuty v klíčových certifikátech; pouze v leasesetech.

Pro cíle s hybridními nebo PQ typy podpisů,
používejte NONE (typ 255) pro typ šifrování,
ale neexistuje žádný kryptografický klíč, a celá hlavní část o délce 384 bajtů je vyhrazena pro klíč podpisu.

Velikosti cílů
````````````````

Zde jsou délky pro nové typy cílů.
Typ šifrování pro všechny je NONE (typ 255) a délka šifrovacího klíče je považována za 0.
Celá část o délce 384 bajtů je použita pro první část veřejného klíče pro podepisování.
Poznámka: To je odlišné od specifikace pro typy ECDSA_SHA512_P521 a RSA podpis, kde jsme zachovali 256-bajtový ElGamal
alebo i když nebyl použit.

Žádné vycpávky.
Celková délka je 7 + celková délka klíče.
Délka klíčového certifikátu je 4 + nadbytečná délka klíče.

Příklad byte streamu destinace o délce 1319 bajtů pro MLDSA44:

skey[0:383] 5 (932 >> 8) (932 & 0xff) 00 12 00 255 skey[384:1311]



| Typ | ypový kód | Celková délka veřejného | líče | avní | adbyt |
| --- | --------- | ----------------------- | ---- | ---- | ----- |
| MLDSA44 | 12 | 1312 | 384 | 928 | 1319 |
| MLDSA65 | 13 | 1952 | 384 | 1568 | 1959 |
| MLDSA87 | 14 | 2592 | 384 | 2208 | 2599 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 384 | 960 | 1351 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 384 | 1600 | 1991 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 384 | 2240 | 2631 |




Velikosti RouterIdent
`````````````````````

Zde jsou délky pro nové typy destinací.
Typ šifrování pro všechny je X25519 (typ 4).
Celá část o délce 352 bajtů za veřejným klíčem X28819 je použita pro první část veřejného klíče pro podepisování.
Žádné vycpávky.
Celková délka je 39 + celková délka klíče.
Délka klíčového certifikátu je 4 + nadbytečná délka klíče.

Příklad byte streamu router identity o délce 1351 bajtů pro MLDSA44:

enckey[0:31] skey[0:351] 5 (960 >> 8) (960 & 0xff) 00 12 00 4 skey[352:1311]



| Typ | ypový kód | Celková délka veřejného | líče | avní | adbyt |
| --- | --------- | ----------------------- | ---- | ---- | ----- |
| MLDSA44 | 12 | 1312 | 352 | 960 | 1351 |
| MLDSA65 | 13 | 1952 | 352 | 1600 | 1991 |
| MLDSA87 | 14 | 2592 | 352 | 2240 | 2631 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 352 | 992 | 1383 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 352 | 1632 | 2023 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 352 | 2272 | 2663 |


### Ruční vzory

Ručně použití vzory používají [Noise]_ ruční vzory.

Použité označení písmen:

- e = jednorázový efemérní klíč
- s = statický klíč
- p = užitečná zátěž zprávy
- e1 = jednorázový efemérní PQ klíč, poslaný od Alice k Bobovi
- ekem1 = šifrovaný text KEM, poslaný od Boba k Alice

Následující úpravy pro XK a IK pro hybridní dopřednou tajnost (hfs) jsou
definovány v [Noise-Hybrid]_ sekce 5:

```dataspec

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

  e1 a ekem1 jsou šifrované. Viz definice vzorů níže.
  POZNÁMKA: e1 a ekem1 mají různé velikosti (na rozdíl od X25519)

```

Vzorec e1 je definován následovně, jak je specifikováno v [Noise-Hybrid]_ sekci 4:

```dataspec

Pro Alici:
  (encap_key, decap_key) = PQ_KEYGEN()

  // EncryptAndHash(encap_key)
  ciphertext = ENCRYPT(k, n, encap_key, ad)
  n++
  MixHash(ciphertext)

  Pro Boba:

  // DecryptAndHash(ciphertext)
  encap_key = DECRYPT(k, n, ciphertext, ad)
  n++
  MixHash(ciphertext)


```

Vzorec ekem1 je definován následovně, jak je specifikováno v [Noise-Hybrid]_ sekci 4:

```dataspec

Pro Boba:

  (kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

  // EncryptAndHash(kem_ciphertext)
  ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)
  MixHash(ciphertext)

  // MixKey
  MixKey(kem_shared_key)


  Pro Alici:

  // DecryptAndHash(ciphertext)
  kem_ciphertext = DECRYPT(k, n, ciphertext, ad)
  MixHash(ciphertext)

  // MixKey
  kem_shared_key = DECAPS(kem_ciphertext, decap_key)
  MixKey(kem_shared_key)


```

### Noise Handshake KDF

Problémy
``````

- Měli bychom změnit hašovací funkci handshaku? Viz [Choosing-Hash]_.
  SHA256 není ohrožena PQ, ale pokud bychom chtěli vylepšit
  naši hašovací funkci, teď je čas, zatímco měníme i jiné věci.
  Aktuální návrh IETF SSH [SSH-HYBRID]_ je používat MLKEM768
  s SHA256, a MLKEM1024 s SHA384. Tento návrh zahrnuje
  diskusi o bezpečnostních úvahách.
- Měli bychom přestat odesílat 0-RTT data ratchetu (kromě LS)?
- Měli bychom přepnout ratchet z IK na XK, pokud neodesíláme 0-RTT data?

Přehled
``````

Tato sekce se vztahuje na protokoly IK a XK.

Hybridní handshake je definován v [Noise-Hybrid]_.
První zpráva, od Alice k Bobovi, obsahuje e1, klíč pro encapsulaci, před užitečnou zátěží zprávy.
To je považováno za další statický klíč; zavolejte EncryptAndHash() na něj (jako Alice)
nebo DecryptAndHash() (jako Bob).
Poté zpracujte užitečnou zátěž zprávy klasicky.

Druhá zpráva, od Boba k Alice, obsahuje ekem1, šifovaný text, před užitečnou zátěží zprávy.
To je považováno za další statický klíč; zavolejte EncryptAndHash() na něj (jako Bob)
nebo DecryptAndHash() (jako Alice).
Poté vypočítejte kem_shared_key a zavolejte MixKey(kem_shared_key).
Poté zpracujte užitečnou zátěž zprávy klasicky.

Definované operace ML-KEM
`````````````````````````

Definujeme následující funkce odpovídající kryptografickým stavebním blokům používaným
jak je definováno v [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

(encap_key, dekap_key) = PQ_KEYGEN()
    Alice vytváří klíče pro encapulaci a dekapulaci
    Klíč pro encapulaci je poslán ve zprávě 1.
    Velikosti klíčů encap_key a dekap_key se liší na základě varianty ML-KEM.

(ciphertext, kem_shared_key) = ENCAPS(encap_key)
    Bob vypočítá šifrový text a sdílený klíč,
    pomocí šifrovaného textu přijatého ve zprávě 1.
    Šifrový text je poslán ve zprávě 2.
    Velikost šifrovaného textu se liší na základě varianty ML-KEM.
    kem_shared_key je vždy 32 bajtů.

kem_shared_key = DECAPS(ciphertext, dekap_key)
    Alice vypočítá sdílený klíč,
    pomocí šifrovaného textu přijatého ve zprávě 2.
    kem_shared_key je vždy 32 bajtů.

Poznámka: jak encap_key, tak šifrovaný text jsou šifrovány uvnitř ChaCha/Poly
bloků v Noise handshake zprávách 1 a 2.
Budou dešifrovány během handshake procesu.

kem_shared_key je smíchána do řetězecového klíče pomocí MixHash().
Viz níže pro podrobnosti.

Alice KDF pro Zprávu 1
```````````````````````

Pro XK: Po vzoru zprávy 'es' a před užitečnými daty, přidejte:

NEBO

Pro IK: Po vzoru zprávy 'es' a před vzoru zprávy 's', přidejte:

```text
To je vzorek zprávy "e1":
  (encap_key, dekap_key) = PQ_KEYGEN()

  // EncryptAndHash(encap_key)
  // AEAD parametry
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, encap_key, ad)
  n++

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)

  Konec vzoru zprávy "e1".

  POZNÁMKA: Pro další sekci (užitečnou zátěž pro XK nebo statický klíč pro IK),
  keydata a chain key zůstávají stejné,
  a n nyní rovná 1 (místo 0 pro nehybridní).

```

Bob KDF pro Zprávu 1
`````````````````````

Pro XK: Po vzoru zprávy 'es' a před užitečnými daty, přidejte:

NEBO

Pro IK: Po vzoru zprávy 'es' a před vzoru zprávy 's', přidejte:

```text
To je vzorek zprávy "e1":

  // DecryptAndHash(encap_key_section)
  // AEAD parametry
  k = keydata[32:63]
  n = 0
  ad = h
  encap_key = DECRYPT(k, n, encap_key_section, ad)
  n++

  // MixHash(encap_key_section)
  h = SHA256(h || encap_key_section)

  Konec vzoru zprávy "e1".

  POZNÁMKA: Pro další sekci (užitečná zátěž pro XK nebo statický klíč pro IK),
  keydata a chain key zůstávají stejné,
  a n nyní rovná 1 (místo 0 pro nehybridní).

```

Bob KDF pro Zprávu 2
`````````````````````

Pro XK: Po vzoru zprávy 'ee' a před užitečnými daty, přidejte:

NEBO

Pro IK: Po vzoru zprávy 'ee' a před vzorem zprávy 'se', přidejte:

```text
To je vzorek zprávy "ekem1":

  (kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

  // EncryptAndHash(kem_ciphertext)
  // AEAD parametry
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)

  // MixKey(kem_shared_key)
  keydata = HKDF(chainKey, kem_shared_key, "", 64)
  chainKey = keydata[0:31]

  Konec vzoru zprávy "ekem1".

```

Alice KDF pro Zprávu 2
`````````````````````

Po vzoru zprávy 'ee' (a před vzorem zprávy 'ss' pro IK), přidejte:

```text
To je vzorek zprávy "ekem1":

  // DecryptAndHash(kem_ciphertext_section)
  // AEAD parametry
  k = keydata[32:63]
  n = 0
  ad = h
  kem_ciphertext = DECRYPT(k, n, kem_ciphertext_section, ad)

  // MixHash(kem_ciphertext_section)
  h = SHA256(h || kem_ciphertext_section)

  // MixKey(kem_shared_key)
  kem_shared_key = DECAPS(kem_ciphertext, dekap_key)
  keydata = HKDF(chainKey, kem_shared_key, "", 64)
  chainKey = keydata[0:31]

  Konec vzoru zprávy "ekem1".

```

KDF pro Zprávu 3 (pouze XK)
``````````````
nezměněno

KDF pro split()
```````````````
nezměněno

### Ratchet

Aktualizujte specifikaci ECIES-Ratchet [ECIES](https://geti2p.net/spec/ecies) takto:

Identifikátory Noise
`````````````````````

- "Noise_IKhfselg2_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM1024_ChaChaPoly_SHA256"

1b) Nový formát relace (s vazbou)
```````````````````````````````````

Změny: Aktuální ratchet obsahoval statický klíč v první ChaCha sekci,
a užitečná zátěž ve druhé sekci.
S ML-KEM, jsou nyní tři sekce.
První sekce obsahuje šifrovaný PQ veřejný klíč.
Druhá sekce obsahuje statický klíč.
Třetí sekce obsahuje užitečnou zátěž.

Šifrovaný formát:

```dataspec
+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   Nový Efemérní Veřejný Klíč relace   |
  +             32 bajty                  +
  |     Kódováno s Elligator2             |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +           Šifrovaný text ML-KEM       +
  |       ChaCha20 šifrované data         |
  +      (viz tabulka níže pro délku)     +
  |                                       |
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Ověřovací Kód Zprávy        |
  +    (MAC) pro sekci encap_key           +
  |             16 bajtů                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +           Statický Klíč X25519        +
  |       ChaCha20 šifrované data         |
  +             32 bajty                  +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Ověřovací Kód Zprávy        |
  +    (MAC) pro sekci statického klíče   +
  |             16 bajtů                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Sekce Užitečné Zátěže      +
  |       ChaCha20 šifrované data         |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Ověřovací Kód Zprávy        |
  +         (MAC) pro sekci užitečné zátěže+
  |             16 bajtů                  |
  +----+----+----+----+----+----+----+----+

```

Dešifrovaný formát:

```dataspec
Část užitečné zátěže 1:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +       Šifrovaný text ML-KEM           +
  |                                       |
  +      (viz tabulka níže pro délku)     +
  |                                       |
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Část užitečné zátěže 2:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +       Statický Klíč X25519            +
  |                                       |
  +      (32 bajty)                       +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+

  Část užitečné zátěže 3:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Sekce Užitečné Zátěže      +
  |                                       |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+

```

Velikosti:

| Typ | ód Typu | len | sg 1 len | sg 1 Enc len | sg 1 Dec len | Q key len | l len |
| --- | ------- | --- | -------- | ------------ | ------------ | --------- | ----- |
| X25519 | 4 | 32 | 96+pl | 64+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 912+pl | 880+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1296+pl | 1360+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1680+pl | 1648+pl | 1568+pl | 1568 | pl |


Poznámka: Užitečná zátěž musí obsahovat blok DateTime, takže minimální velikost užitečné zátěže je 7.
Minimální velikosti zprávy 1 lze vypočítat odpovídajícím způsobem.

Podopvěď na Novou relaci
``````````````````````````

Změny: Aktuální ratchet má prázdnou užitečnou zátěž pro první ChaCha sekci,
a užitečná zátěž ve druhé sekci.
S ML-KEM, jsou nyní tři sekce.
První sekce obsahuje šifrovaný PQ šifrovaný text.
Druhá sekce má prázdnou užitečnou zátěž.
Třetí sekce obsahuje užitečnou zátěž.

Šifrovaný formát:

```dataspec
+----+----+----+----+----+----+----+----+
  |       Tag relace   8 bajtů             |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Efemérní Veřejný Klíč          +
  |                                       |
  +            32 bajty                   +
  |     Kódováno s Elligator2             |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  | ChaCha20 šifrovaný ML-KEM šifrovaný text  |
  +      (viz tabulka níže pro délku)     +
  ~                                       ~
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Ověřovací Kód Zprávy        |
  +  (MAC) pro sekci šifrovaného textu     +
  |             16 bajtů                  |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Ověřovací Kód Zprávy        |
  +  (MAC) pro sekci klíče (bez dat)      +
  |             16 bajtů                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Sekce Užitečné Zátěže      +
  |       ChaCha20 šifrované data         |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Ověřovací Kód Zprávy        |
  +         (MAC) pro sekci užitečné zátěže+
  |             16 bajtů                  |
  +----+----+----+----+----+----+----+----+

```

Dešifrovaný formát:

```dataspec
Část užitečné zátěže 1:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +       Šifrovaný text ML-KEM           +
  |                                       |
  +      (viz tabulka níže pro délku)     +
  |                                       |
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Část užitečné zátěže 2:

  prázdná

  Část užitečné zátěže 3:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Sekce Užitečné Zátěže      +
  |                                       |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+

```

Velikosti:

| Typ | ód Typu | len | sg 2 len | sg 2 Enc len | sg 2 Dec len | Q CT len | pt len |
| --- | ------- | --- | -------- | ------------ | ------------ | -------- | ------ |
| X25519 | 4 | 32 | 72+pl | 32+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 856+pl | 816+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1176+pl | 1136+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1656+pl | 1616+pl | 1568+pl | 1568 | pl |


Poznámka: Zpráva 2 bude mít obvykle nenulovou užitečnou zátěž,
specifikace ratchetu [ECIES](https://geti2p.net/spec/ecies) to nevyžaduje, takže minimální velikost užitečné zátěže je 0.
Minimální velikosti zprávy 2 lze vypočítat odpovídajícím způsobem.


### NTCP2

Aktualizujte specifikaci NTCP2 [NTCP2](https://geti2p.net/spec/ntcp2) takto:

Identifikátory Noise
```````````````````

- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM1024_ChaChaPoly_SHA256"


1) Relace žádosti
``````````````````

Změny: Aktuální NTCP2 obsahuje pouze možnosti v ChaCha sekci.
S ML-KEM, ChaCha sekce také obsahuje šifrovaný PQ veřejný klíč.

Surowý obsah:

```dataspec
+----+----+----+----+----+----+----+----+
  |                                       |
  +        zašifrováno s RH_B             +
  |       AES-CBC-256 šifrovaný X         |
  +             (32 bajtů)                +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaChaPoly rámec (MLKEM)            |
  +      (viz tabulka níže pro délku)     +
  |   k definováno v KDF pro zprávu 1     |
  +   n = 0                               +
  |   viz KDF pro související data        |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaChaPoly rámec (možnosti)         +
  +         32 bajtů                      +
  |   k definováno v KDF pro zprávu 1     |
  +   n = 0                               +
  |   viz KDF pro související data        |
  +----+----+----+----+----+----+----+----+
  |     nezašifrované ověřené             |
  ~         vycpávky (volitelné)          ~
  |     délka definována v bloku možností |
  +----+----+----+----+----+----+----+----+

  Stejné jako dříve kromě přidání druhého ChaChaPoly rámce

```

Nezašifrovaná data (ověřovací tag Poly1305 není zobrazen):

```dataspec
+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                   X                   |
  +              (32 bajtů)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           Šifrovaný text encap_key   |
  +      (viz tabulku níže pro délku)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |               možnosti                |
  +              (16 bajtů)               +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     nezašifrované ověřené             |
  +         vycpávky (volitelné)          +
  |     délka definována v bloku možností |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+



```

Velikosti:

| Typ | ód Typu | len | sg 1 len | sg 1 Enc len | sg 1 Dec len | Q key len | pt len |
| --- | ------- | --- | -------- | ------------ | ------------ | --------- | ------ |
| X25519 | 4 | 32 | 64+pad | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 880+pad | 848 | 816 | 800 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1264+pad | 1232 | 1200 | 1184 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1648+pad | 1616 | 1584 | 1568 | 16 |


Poznámka: Kódy typů jsou pro interní použití pouze. Směrovače zůstávají typu 4,
a podpora bude indikována v adresách směrovačů.


2) Relace vytvořena
``````````````````

Změny: Aktuální NTCP2 obsahuje pouze možnosti v ChaCha sekci.
S ML-KEM, ChaCha sekce také obsahuje šifrovaný PQ veřejný klíč.

Surowý obsah:

```dataspec
+----+----+----+----+----+----+----+----+
  |                                       |
  +        zašifrováno s RH_B             +
  |       AES-CBC-256 šifrovaný Y         +
  +              (32 bajtů)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaChaPoly rámec (MLKEM)            +
  +   Encrypted and authenticated data    +
  -      (viz tabulka níže pro délku)     -
  +   k definováno v KDF pro zprávu 2     +
  |   n = 0; viz KDF pro související data  |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaChaPoly rámec (možnosti)         +
  +   Encrypted and authenticated data    +
  -           32 bajtů                    -
  +   k definováno v KDF pro zprávu 2     +
  |   n = 0; viz KDF pro související data  |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     nezašifrované ověřené             +
  +         vycpávky (volitelné)          +
  |     délka definována v bloku možností |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Stejné jako dříve kromě přidání druhého ChaChaPoly rámce

```

Nezašifrovaná data (ověřovací tag Poly1305 není zobrazen):

```dataspec
+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                  Y                    |
  +              (32 bajtů)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           Šifrovaný text ML-KEM       |
  +      (viz tabulku níže pro délku)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |               možnosti                |
  +              (16 bajtů)               +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     nezašifrované ověřené             +
  +         vycpávky (volitelné)          +
  |     délka definována v bloku možností |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+

```

Velikosti:

| Typ | ód Typu | len | sg 2 len | sg 2 Enc len | sg 2 Dec len | Q CT len | pt len |
| --- | ------- | --- | -------- | ------------ | ------------ | -------- | ------ |
| X25519 | 4 | 32 | 64+pad | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 848+pad | 816 | 784 | 768 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1136+pad | 1104 | 1104 | 1088 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1616+pad | 1584 | 1584 | 1568 | 16 |


Poznámka: Kódy typů jsou pro interní použití pouze. Směrovače zůstávají typu 4,
a podpora bude indikována v adresách směrovačů.



3) Relace potvrzena
```````````````````

Neoáda se

Funkce pro derivaci klíčů (KDF) (pro datovou fázi)
```````````````````````````````````````````````
Neoáda se




### SSU2

Aktualizujte specifikaci SSU2 [SSU2](https://geti2p.net/spec/ssu2) takto:

Identifikátory Noise
```````````````````

- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM1024_ChaChaPoly_SHA256"

Dlouhá Hlavička
```````````````
Dlouhá hlavička je 32 bajtů dlouhá. Používá se před vytvořením relace, pro Požadavek na Pierre, Vytvoření relace, Vytvoření opakovaný pokus, Požadavek Testování a Hole Punch zprávy.

TODO: Můžeme interně použít pole verze a použít 3 pro MLKEM512 a 4 pro MLKEM768.
Děláme to jenom pro typy 0 a 1 nebo pro všechny 6 typů?

Před šifrováním hlavičky:

```dataspec

+----+----+----+----+----+----+----+----+
  |      Identifikátor připojení Cíle    |
  +----+----+----+----+----+----+----+----+
  |   Číslo paketu   |typ| ver| id |tag |
  +----+----+----+----+----+----+----+----+
  |       Identifikátor připojení Zdroje |
  +----+----+----+----+----+----+----+----+
  |               Token                  |
  +----+----+----+----+----+----+----+----+

  Identifikátor připojení Cíle :: 8 bajtů, bezznaménkový velký-endian integer

  Číslo paketu :: 4 bajtů, bezznaménkový velký-endian integer

  typ :: Typ zprávy = 0, 1, 7, 9, 10 nebo 11

  ver :: Verze protokolu, rovna 2
         TODO Můžeme interně použít pole verze a použít 3 pro MLKEM512 a 4 pro MLKEM768

  id :: 1 bajt, identifikátor sítě (aktuálně 2, kromě testovacích sítí)

  tag :: 1 bajt, nepoužitý, nastaven na 0 pro budoucí kompatibilitu

  Identifikátor připojení Zdroje :: 8 bajtů, bezznaménkový velký-endian integer

  Token :: 8 bajtů, bezznaménkový velký-endian integer

```

Krátká hlavička
`````````````
nezměněno

Relace žádosti (Typ 0)
`````````````````````

Změny: Aktuální SSU2 obsahuje pouze bloková data v ChaCha sekci.
S ML-KEM, ChaCha sekce také obsahuje šifrovaný PQ veřejný klíč.

Surowý obsah:

```dataspec
+----+----+----+----+----+----+----+----+
  |  Dlouhá hlavička bajty 0-15, ChaCha20|
  +  šifrováno s úvodním klíčem Boba    +
  |  Viz KDF pro šifrování hlavičky      |
  +----+----+----+----+----+----+----+----+
  |  Dlouhá hlavička bajty 16-31, ChaCha20|
  +  šifrováno s úvodním klíčem Boba n=0 +
  |                                      |
  +----+----+----+----+----+----+----+----+
  |                                      |
  +       X, ChaCha20 šifrované          +
  |      s úvodním klíčem Boba n=0       |
  +             (32 bajtů)              +
  |                                      |
  +                                      +
  |                                      |
  +----+----+----+----+----+----+----+----+
  |                                      |
  +                                       +
  |  ChaCha20 šifrovaná data (MLKEM)      |
  +         (délka liší)                  +
  |  k definováno v KDF pro Požadavek Relace |
  +  n = 0                               +
  |  viz KDF pro související data        |
  +----+----+----+----+----+----+----+----+
  |                                      |
  +                                       +
  |  ChaCha20 šifrovaná data (užitečná zátěž)|
  +         (délka liší)                  +
  |  k definováno v KDF pro Požadavek Relace |
  +  n = 0                               +
  |  viz KDF pro související data        |
  +----+----+----+----+----+----+----+----+
  |                                      |
  +      Ověřovací kód Poly1305 (16 bajtů) |
  |                                      |
  +----+----+----+----+----+----+----+----+

```

Nezašifrovaná data (ověřovací tag Poly1305 není zobrazen):

```dataspec
+----+----+----+----+----+----+----+----+
  |      Identifikátor připojení Cíle    |
  +----+----+----+----+----+----+----+----+
  |   Číslo paketu   |typ| ver| id |tag |
  +----+----+----+----+----+----+----+----+
  |       Identifikátor připojení Zdroje |
  +----+----+----+----+----+----+----+----+
  |               Token                  |
  +----+----+----+----+----+----+----+----+
  |                                      |
  +                                       +
  |                   X                  +
  +              (32 bajtů)              +
  |                                      |
  +                                        +
  |                                      |
  +----+----+----+----+----+----+----+----+
  |           Šifrovaný text encap_key  |
  +      (viz tabulku níže pro délku)   +
  |                                      |
  +----+----+----+----+----+----+----+----+
  |     Noise užitečná zátěž (bloková data)|
  +         (délka liší)                 +
  |     viz níže pro povolené bloky       |
  +----+----+----+----+----+----+----+----+

```

Velikosti, bez IP režie:

| Typ | ód Typu | len | sg 1 len | sg 1 Enc len | sg 1 Dec len | Q key len | l len |
| --- | ------- | --- | -------- | ------------ | ------------ | --------- | ----- |
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 896+pl | 832+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1280+pl | 1216+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | n/a | příliš ve | é |  |  |  |


Poznámka: Kódy typů jsou pro interní použití pouze. Směrovače zůstávají typu 4,
a podpora bude indik
