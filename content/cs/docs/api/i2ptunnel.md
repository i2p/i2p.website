---
title: "I2PTunnel"
description: "Nástroj pro propojení s I2P a poskytování služeb na I2P"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Přehled

I2PTunnel je základní komponenta I2P pro rozhraní a poskytování služeb v síti I2P. Umožňuje aplikacím založeným na TCP a streamování médií pracovat anonymně prostřednictvím abstrakce tunelů. Cíl tunelu lze definovat pomocí [názvu hostitele](/docs/overview/naming), [Base32](/docs/overview/naming#base32) nebo úplného klíče cíle.

Každý vytvořený tunnel naslouchá lokálně (např. `localhost:port`) a připojuje se interně k I2P destinacím. Pro hostování služby vytvořte tunnel směřující na požadovanou IP adresu a port. Vygeneruje se odpovídající I2P destination key, který umožní službě být globálně dostupnou v rámci I2P sítě. Webové rozhraní I2PTunnel je k dispozici na adrese [I2P Router Tunnel Manager](http://localhost:7657/i2ptunnel/).

---

## Výchozí služby

### Serverový tunel

- **I2P Webserver** – Tunnel k Jetty webserveru na [localhost:7658](http://localhost:7658) pro snadný hosting na I2P.  
  - **Unix:** `$HOME/.i2p/eepsite/docroot`  
  - **Windows:** `%LOCALAPPDATA%\I2P\I2P Site\docroot` → `C:\Users\<username>\AppData\Local\I2P\I2P Site\docroot`

### Klientské tunely

- **I2P HTTP Proxy** – `localhost:4444` – Používá se pro prohlížení I2P a internetu prostřednictvím outproxies.  
- **I2P HTTPS Proxy** – `localhost:4445` – Zabezpečená varianta HTTP proxy.  
- **Irc2P** – `localhost:6668` – Výchozí tunel anonymní IRC sítě.  
- **Git SSH (gitssh.idk.i2p)** – `localhost:7670` – Klientský tunel pro SSH přístup k repozitářům.  
- **Postman SMTP** – `localhost:7659` – Klientský tunel pro odchozí poštu.  
- **Postman POP3** – `localhost:7660` – Klientský tunel pro příchozí poštu.

> Poznámka: Pouze I2P Webserver je výchozí **server tunnel**; všechny ostatní jsou klientské tunnely připojující se k externím I2P službám.

---

## Konfigurace

Specifikace konfigurace I2PTunnel je dokumentována na [/spec/configuration](/docs/specs/configuration/).

---

## Klientské režimy

### Standardní

Otevře lokální TCP port, který se připojí ke službě na I2P destinaci. Podporuje více záznamů destinací oddělených čárkami pro redundanci.

### HTTP

Proxy tunel pro HTTP/HTTPS požadavky. Podporuje lokální a vzdálené outproxy, odstranění hlaviček, ukládání do mezipaměti, autentizaci a transparentní kompresi.

**Ochrana soukromí:**   - Odstraňuje hlavičky: `Accept-*`, `Referer`, `Via`, `From`   - Nahrazuje hlavičky hostitele Base32 destinacemi   - Vynucuje odstranění hop-by-hop podle RFC   - Přidává podporu pro transparentní dekompresi   - Poskytuje interní chybové stránky a lokalizované odpovědi

**Chování komprese:**   - Požadavky mohou používat vlastní hlavičku `X-Accept-Encoding: x-i2p-gzip`   - Odpovědi s `Content-Encoding: x-i2p-gzip` jsou transparentně dekomprimovány   - Komprese je vyhodnocována podle MIME typu a délky odpovědi pro efektivitu

**Persistence (nové od verze 2.5.0):**   HTTP Keepalive a trvalá spojení jsou nyní podporována pro služby hostované v I2P prostřednictvím správce skrytých služeb (Hidden Services Manager). To snižuje latenci a režii spojení, ale zatím neumožňuje plně RFC 2616-kompatibilní trvalé sokety přes všechny skoky (hops).

**Pipelining:**   Zůstává nepodporován a nepotřebný; moderní prohlížeče ho opustily.

**Chování User-Agent:**   - **Outproxy:** Používá aktuální User-Agent z Firefox ESR.   - **Interní:** `MYOB/6.66 (AN/ON)` pro konzistenci anonymity.

### IRC klient

Připojuje se k IRC serverům v síti I2P. Umožňuje bezpečnou podmnožinu příkazů a filtruje identifikátory pro zachování soukromí.

### SOCKS 4/4a/5

Poskytuje funkcionalitu SOCKS proxy pro TCP připojení. UDP zůstává neimplementováno v Java I2P (pouze v i2pd).

### PŘIPOJIT

Implementuje HTTP `CONNECT` tunelování pro SSL/TLS připojení.

### Streamr

Umožňuje streamování ve stylu UDP prostřednictvím zapouzdření založeného na TCP. Podporuje streamování médií při použití s odpovídajícím serverovým tunelem Streamr.

![Diagram I2PTunnel Streamr](/images/I2PTunnel-streamr.png)

---

## Režimy serveru

### Standardní server

Vytvoří TCP destinaci mapovanou na lokální IP:port.

### HTTP Server

Vytváří destinaci, která komunikuje s lokálním webovým serverem. Podporuje kompresi (`x-i2p-gzip`), odstraňování hlaviček a ochranu proti DDoS útokům. Nyní těží z **podpory trvalých spojení** (v2.5.0+) a **optimalizace sdružování vláken** (v2.7.0–2.9.0).

### HTTP Obousměrné

**Zastaralé** – Stále funkční, ale nedoporučuje se. Funguje jako HTTP server i klient bez outproxingu. Používá se především pro diagnostické loopback testy.

### IRC Server

Vytvoří filtrovanou destinaci pro IRC služby, předávající klíče klientských destinací jako názvy hostitelů.

### Streamr Server

Páruje se s tunelem Streamr klienta pro zpracování UDP-stylových datových streamů přes I2P.

---

## Nové funkce (2.4.0–2.10.0)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Introduced</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Summary</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Keepalive/Persistent Connections</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.5.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HTTP tunnels now support persistent sockets for I2P-hosted services, improving performance.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Thread Pooling Optimization</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.7.0-2.9.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reduced CPU overhead and latency by improving thread management.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Post-Quantum Encryption (ML-KEM)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Optional hybrid X25519+ML-KEM encryption to resist future quantum attacks.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NetDB Segmentation</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.4.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Isolates I2PTunnel contexts for improved security and privacy.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU1 Removal / SSU2 Adoption</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.4.0-2.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Upgraded transport layer; transparent to users.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2P-over-Tor Blocking</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Prevents inefficient and unstable I2P-over-Tor routing.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Browser Proxy (Proposal 166)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.7.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Introduced identity-aware proxy mode; details pending confirmation.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Java 17 Requirement (upcoming)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.11.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Future release will require Java 17+.</td>
    </tr>
  </tbody>
</table>
---

## Bezpečnostní funkce

- **Odstranění hlaviček** pro anonymitu (Accept, Referer, From, Via)
- **Randomizace User-Agent** v závislosti na in/outproxy
- **Omezení rychlosti POST** a **ochrana proti Slowloris**
- **Omezování připojení** v streamovacích subsystémech
- **Zvládání přetížení sítě** na vrstvě tunelů
- **Izolace NetDB** zabraňující únikům mezi aplikacemi

---

## Technické podrobnosti

- Výchozí velikost klíče destinace: 516 bajtů (může být větší u rozšířených LS2 certifikátů)
- Base32 adresy: `{52–56+ znaků}.b32.i2p`
- Server tunnely zůstávají kompatibilní s Java I2P i i2pd
- Zastaralá funkce: pouze `httpbidirserver`; žádné odstranění od verze 0.9.59
- Ověřeny správné výchozí porty a kořenové adresáře dokumentů pro všechny platformy

---

## Shrnutí

I2PTunnel zůstává základem integrace aplikací s I2P. Mezi verzemi 0.9.59 a 2.10.0 získal podporu perzistentních spojení, postkvantovou šifru a významná vylepšení vláknování. Většina konfigurací zůstává kompatibilní, ale vývojáři by měli ověřit svá nastavení, aby zajistili soulad s moderními výchozími hodnotami pro transport a zabezpečení.
