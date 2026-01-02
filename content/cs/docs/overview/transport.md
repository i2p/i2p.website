---
title: "Transportní vrstva"
description: "Porozumění transportní vrstvě I2P - metody komunikace point-to-point mezi routers včetně NTCP2 a SSU2"
slug: "transport"
lastUpdated: "2025-03"
accurateFor: "2.10.0"
---

---

## 1. Přehled

V I2P je **transport** metodou přímé, bod‑na‑bod komunikace mezi routery. Tyto mechanismy zajišťují důvěrnost a integritu a zároveň ověřují identitu routerů.

Každý transport pracuje jako spojovaný protokol s podporou autentizace, řízení toku, potvrzování a opakovaného přenosu.

---

## 2. Aktuální transporty

I2P v současnosti podporuje dva hlavní přenosové protokoly:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Transport</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NTCP2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TCP</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise-based TCP transport with modern encryption (as of 0.9.36)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UDP</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Secure Semireliable UDP with modern encryption (as of 0.9.56)</td>
    </tr>
  </tbody>
</table>
### 2.1 Starší transportní protokoly (zastaralé)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Transport</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NTCP</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TCP</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Replaced by NTCP2; removed in 0.9.62</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UDP</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Replaced by SSU2; removed in 0.9.62</td>
    </tr>
  </tbody>
</table>
---

## 3. Transportní služby

Transportní podsystém poskytuje následující služby:

### 3.1 Doručování zpráv

- Spolehlivé doručování zpráv [I2NP](/docs/specs/i2np/) (transporty obsluhují výhradně I2NP komunikaci)
- Doručování ve správném pořadí **NENÍ univerzálně zaručeno**
- Řazení zpráv do front podle priority

### 3.2 Správa připojení

- Navazování a ukončování spojení
- Správa limitů spojení s vynucováním prahových hodnot
- Sledování stavu na úrovni jednotlivých peerů
- Automatické i manuální vynucování seznamu blokovaných peerů

### 3.3 Konfigurace sítě

- Více adres routeru pro každý transport (podpora IPv4 a IPv6 od verze v0.9.8)
- Otevírání portů firewallu přes UPnP
- Podpora průchodu přes NAT/firewall
- Detekce místní IP adresy více metodami

### 3.4 Zabezpečení

- Šifrování pro komunikaci bod–bod
- Ověření IP adresy podle místních pravidel
- Určování konsenzu času (záložní NTP)

### 3.5 Správa šířky pásma

- Limity příchozí a odchozí šířky pásma
- Optimální výběr transportního protokolu pro odchozí zprávy

---

## 4. Transportní adresy

Subsystém udržuje seznam kontaktních bodů pro router:

- Transportní metoda (NTCP2, SSU2)
- IP adresa
- Číslo portu
- Volitelné parametry

Pro každou přenosovou metodu může existovat více adres.

### 4.1 Běžné konfigurace adres

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Configuration</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Hidden</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Routers with no published addresses</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Firewalled</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Routers publishing SSU2 addresses with "introducer" peer lists for NAT traversal</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Unrestricted</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Routers advertising both NTCP2 and SSU2 addresses on IPv4 and/or IPv6</td>
    </tr>
  </tbody>
</table>
---

## 5. Výběr transportu

Systém vybírá transportní protokoly pro [I2NP messages](/docs/specs/i2np/) nezávisle na protokolech vyšších vrstev. Výběr používá **systém nabídek**, v němž každý transportní protokol podává nabídku a vyhrává nejnižší nabídka.

### 5.1 Faktory pro stanovení nabídky

- Nastavení preferencí transportu
- Stávající spojení s protějšky
- Aktuální vs. prahové počty spojení
- Historie nedávných pokusů o připojení
- Omezení velikosti zpráv
- Transportní schopnosti v RouterInfo protějšku
- Přímost spojení (přímé vs. závislé na introduceru (zprostředkovatel v SSU))
- Protějškem inzerované preference transportu

Obecně si dva routery udržují současně spojení s jedním transportem, ačkoli jsou možná i současná spojení s více transporty.

---

## 6. NTCP2

**NTCP2** (Nový transportní protokol 2) je moderní transport založený na TCP pro I2P, představený ve verzi 0.9.36.

### 6.1 Klíčové vlastnosti

- Na základě **Noise Protocol Framework** (rámec pro návrh šifrovaných handshake) (Noise_XK pattern)
- Používá **X25519** pro výměnu klíčů (elipticko-křivkový algoritmus)
- Používá **ChaCha20/Poly1305** pro autentizované šifrování (AEAD – autentizované šifrování s přidruženými daty)
- Používá **BLAKE2s** pro hashování (moderní kryptografická hashovací funkce)
- Obfuskace protokolu pro odolnost vůči DPI (Deep Packet Inspection – hloubková inspekce paketů)
- Volitelné padding (výplň) pro odolnost vůči analýze provozu

### 6.2 Navázání spojení

1. **Požadavek na relaci** (Alice → Bob): efemérní klíč X25519 + šifrovaná užitečná data
2. **Relace vytvořena** (Bob → Alice): efemérní klíč + šifrované potvrzení
3. **Relace potvrzena** (Alice → Bob): závěrečný handshake (navázání spojení) s RouterInfo

Veškerá následná data jsou šifrována pomocí klíčů sezení odvozených z handshake (navázání spojení).

Podrobné informace najdete v [specifikaci NTCP2](/docs/specs/ntcp2/).

---

## 7. SSU2

**SSU2** (Zabezpečený částečně spolehlivý UDP 2) je moderní transportní protokol založený na UDP pro I2P, představený ve verzi 0.9.56.

### 7.1 Klíčové vlastnosti

- Založeno na **Noise Protocol Framework** (rámec protokolu Noise) (Noise_XK pattern)
- Používá **X25519** pro výměnu klíčů
- Používá **ChaCha20/Poly1305** pro autentizované šifrování
- Částečně spolehlivé doručování se selektivními potvrzeními
- Průchod NATem pomocí hole punchingu (technika navazování přímého spojení přes NAT) a relay/introduction
- Podpora migrace spojení
- Zjišťování MTU na trase

### 7.2 Výhody oproti SSU (starší)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">SSU (Legacy)</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">SSU2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ElGamal + AES</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519 + ChaCha20/Poly1305</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Header encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Partial</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Full (ChaCha20)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connection ID</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fixed</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypted, rotatable</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NAT traversal</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Basic introduction</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Enhanced hole punching + relay</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Obfuscation</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Minimal</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Improved (variable padding)</td>
    </tr>
  </tbody>
</table>
Pro úplné podrobnosti viz [Specifikace SSU2](/docs/specs/ssu2/).

---

## 8. Průchod NAT

Oba transportní protokoly podporují průchod přes NAT, aby se routers za firewallem mohly zapojit do sítě.

### 8.1 Úvod do SSU2

Pokud router nemůže přímo přijímat příchozí spojení:

1. Router zveřejňuje adresy **introducer** (zprostředkovatel spojení) ve svém RouterInfo (informace o routeru)
2. Připojující se uzel odešle požadavek na zprostředkování introduceru
3. Introducer předá routeru za firewallem informace o připojení
4. Router za firewallem iniciuje odchozí spojení (hole punch, prorážení NATu)
5. Je navázána přímá komunikace

### 8.2 NTCP2 a firewally

NTCP2 vyžaduje příchozí TCP konektivitu. Routers za NATem mohou:

- Použít UPnP k automatickému otevření portů
- Ručně nakonfigurovat přesměrování portů
- Spoléhat se na SSU2 pro příchozí připojení, zatímco pro odchozí používat NTCP2

---

## 9. Obfuskace protokolu

Oba moderní přenosové protokoly obsahují prvky pro zastírání:

- **Náhodná výplň** ve zprávách handshake (navazovací procedury)
- **Šifrované hlavičky**, které neprozrazují signatury protokolu
- **Zprávy proměnlivé délky**, aby odolaly analýze provozu
- **Žádné pevné vzorce** při navazování spojení

> **Poznámka**: Obfuskace na transportní vrstvě doplňuje, ale nenahrazuje anonymitu poskytovanou tunnel architekturou I2P.

---

## 10. Budoucí vývoj

Plánovaný výzkum a vylepšení zahrnují:

- **Zásuvné transporty** – zásuvné moduly pro zastírání kompatibilní s Tor
- **Transport založený na QUIC** – zkoumání přínosů protokolu QUIC
- **Optimalizace limitů připojení** – výzkum optimálních limitů připojení k peerům
- **Vylepšené strategie paddingu** – zlepšená odolnost vůči analýze provozu

---

## 11. Odkazy

- [Specifikace NTCP2](/docs/specs/ntcp2/) – Transport přes TCP založený na Noise (kryptografický rámec)
- [Specifikace SSU2](/docs/specs/ssu2/) – Bezpečné částečně spolehlivé UDP 2
- [Specifikace I2NP](/docs/specs/i2np/) – Zprávy síťového protokolu I2P
- [Společné struktury](/docs/specs/common-structures/) – RouterInfo a struktury adres
- [Historická diskuse o NTCP](/docs/ntcp/) – Historie vývoje staršího transportu
- [Dokumentace ke staršímu SSU](/docs/legacy/ssu/) – Původní specifikace SSU (zastaralá)
