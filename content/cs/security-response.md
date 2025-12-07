---
title: "Proces reakce na zranitelnosti"
description: "Proces nahlášení a reakce na zranitelnosti bezpečnosti I2P"
layout: "security-response"
---

<div id="contact"></div>

## Nahlásit zranitelnost

Objevili jste bezpečnostní problém? Nahlaste jej na **security@i2p.net** (doporučujeme PGP)

<a href="/keys/i2p-security-public.asc" download class="pgp-key-btn">Stáhnout PGP klíč</a> | GPG otisk prstu: `40DF FE20 7D79 9BEC 3AE8 7DEA 5F98 BE91 176E 1941`

<div id="guidelines"></div>

## Pokyny pro výzkum

**Prosím, NE:**
- Zneužívejte živou síť I2P
- Provádějte sociální inženýrství nebo útočte na infrastrukturu I2P
- Narušujte služby pro ostatní uživatele

**Prosím, ANO:**
- Používejte izolované testovací sítě, kdykoli je to možné
- Dodržujte postupy koordinované zveřejnění
- Kontaktujte nás před testováním v živé síti

<div id="process"></div>

## Proces reakce

### 1. Přijetí hlášení
- Odpověď do **3 pracovních dnů**
- Přidělen manažer odpovědí
- Klasifikace závažnosti (VYSOKÁ/STŘEDNÍ/NÍZKÁ)

### 2. Vyšetřování a vývoj
- Vývoj soukromé opravy prostřednictvím šifrovaných kanálů
- Testování na izolované síti
- **VYSOKÁ závažnost:** Veřejné oznámení do 3 dnů (bez podrobností o zneužití)

### 3. Uvolnění a zveřejnění
- Nasazení aktualizace zabezpečení
- **Maximální doba 90 dní** k úplnému zveřejnění
- Možnost uznání výzkumníků v oznámeních

### Úrovně závažnosti

**VYSOKÁ** - Dopad na celou síť, vyžaduje okamžitou pozornost  
**STŘEDNÍ** - Individuální směrovače, cílené zneužití  
**NÍZKÁ** - Omezený dopad, teoretické scénáře

<div id="communication"></div>

## Bezpečná komunikace

Používejte šifrování PGP/GPG pro všechna bezpečnostní hlášení:

```
Otisk prstu: 40DF FE20 7D79 9BEC 3AE8 7DEA 5F98 BE91 176E 1941
```

Vložte do svého hlášení:
- Podrobný technický popis
- Kroky k reprodukci
- Proof-of-concept kód (pokud je to možné)

<div id="timeline"></div>

## Časový plán

| Fáze | Časový rámec |
|------|--------------|
| Počáteční odpověď | 0-3 dny |
| Vyšetřování | 1-2 týdny |
| Vývoj a testování | 2-6 týdnů |
| Uvolnění | 6-12 týdnů |
| Úplné zveřejnění | maximálně 90 dní |

<div id="faq"></div>

## Často kladené dotazy

**Dostanu se do problémů, pokud nahlásím?**
Ne. Odpovědné hlášení je oceňováno a chráněno.

**Mohu testovat na živé síti?**
Ne. Používejte pouze izolované testovací sítě.

**Mohu zůstat v anonymitě?**
Ano, ačkoli to může zkomplikovat komunikaci.

**Máte odměny za nalezené chyby?**
V současnosti ne. I2P je řízen dobrovolníky s omezenými zdroji.

<div id="examples"></div>

## Co hlásit

**V rozsahu:**
- Zranitelnosti směrovače I2P
- Nedostatky v protokolu nebo kryptografii
- Útoky na úrovni sítě
- Techniky de-anonymizace
- Problémy s odmítnutím služby

**Mimo rozsah:**
- Aplikace třetích stran (kontaktujte vývojáře)
- Sociální inženýrství nebo fyzické útoky
- Známé/oznámené zranitelnosti
- Čistě teoretické problémy

---

**Děkujeme, že pomáháte udržovat bezpečnost I2P!**