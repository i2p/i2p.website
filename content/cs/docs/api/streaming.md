---
title: "Streamovací protokol"
description: "Transportní protokol podobný TCP, používaný většinou I2P aplikací"
slug: "streaming"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Přehled

**I2P Streaming Library** poskytuje spolehlivý, uspořádaný a autentizovaný přenos přes zprávy I2P, podobně jako **TCP over IP**. Nachází se nad [protokolem I2CP](/docs/specs/i2cp/) a používají jej téměř všechny interaktivní aplikace I2P, včetně HTTP proxy, IRC, BitTorrentu a emailu.

### Základní charakteristiky

- Jednofázové navázání spojení pomocí příznaků **SYN**, **ACK** a **FIN**, které mohou být sdruženy s užitečnými daty pro snížení počtu přenosových cyklů.
- **Řízení zahltění pomocí posuvného okna** s pomalým startem a vyhýbáním se zahlcení optimalizovaným pro prostředí I2P s vysokou latencí.
- Komprese paketů (výchozí 4KB komprimované segmenty) vyvažující náklady na opětovný přenos a latenci fragmentace.
- Plně **autentizovaná, šifrovaná** a **spolehlivá** abstrakce kanálu mezi I2P destinacemi.

Tento design umožňuje dokončit malé HTTP požadavky a odpovědi v jediném cyklu. SYN paket může nést payload požadavku, zatímco SYN/ACK/FIN respondenta může obsahovat celé tělo odpovědi.

---

## Základy API

Java streaming API kopíruje standardní programování soketů v Javě:

```java
I2PSocketManager mgr = I2PSocketManagerFactory.createManager(host, port, options);
I2PSocket socket       = mgr.connect(destination);
I2PServerSocket server = mgr.getServerSocket();
```
- `I2PSocketManagerFactory` vyjednává nebo znovu používá session routeru přes I2CP.  
- Pokud není poskytnut klíč, je automaticky vygenerována nová destinace.  
- Vývojáři mohou předat I2CP volby (např. délky tunelů, typy šifrování nebo nastavení připojení) pomocí mapy `options`.  
- `I2PSocket` a `I2PServerSocket` zrcadlí standardní Java rozhraní `Socket`, což usnadňuje migraci.

Kompletní Javadocs jsou dostupné z I2P router console nebo [zde](/docs/specs/streaming/).

---

## Konfigurace a ladění

Konfigurační vlastnosti můžete předat při vytváření správce socketů pomocí:

```java
I2PSocketManagerFactory.createManager(host, port, properties);
```
### Klíčové možnosti

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Default</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.maxWindowSize</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Maximum send window (bytes)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128 KB</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.initialRTO</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Initial retransmission timeout</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">9s</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.inactivityTimeout</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Timeout before connection close</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">90s</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.enforceProtocol</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Enforce protocol ID (prevents confusion)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">true</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.congestionAlgorithm</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Congestion control method</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default (AIMD TCP-like)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.disableRejectLogging</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Disable logging rejected packets</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">false</td>
    </tr>
  </tbody>
</table>
### Chování podle zátěže

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Workload</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended Settings</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>HTTP-like</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default parameters are ideal.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Bulk Transfer</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Increase window size to 256 KB or 512 KB; lengthen timeouts.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Real-time Streaming</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Lower tunnel length to 1-2 hops; adjust RTO downwards.</td>
    </tr>
  </tbody>
</table>
Novější funkce od verze 0.9.4 zahrnují potlačení záznamů o odmítnutí, podporu DSA seznamů (0.9.21) a vynucené dodržování protokolu (0.9.36). Routery od verze 2.10.0 zahrnují post-kvantové hybridní šifrování (ML-KEM + X25519) na transportní vrstvě.

---

## Detaily protokolu

Každý stream je identifikován pomocí **Stream ID**. Pakety nesou kontrolní příznaky podobné TCP: `SYNCHRONIZE`, `ACK`, `FIN` a `RESET`. Pakety mohou současně obsahovat jak data, tak kontrolní příznaky, což zlepšuje efektivitu krátkodobých spojení.

### Životní cyklus spojení

1. **SYN odeslán** — iniciátor zahrnuje volitelná data.  
2. **SYN/ACK odpověď** — respondent zahrnuje volitelná data.  
3. **ACK finalizace** — navazuje spolehlivost a stav relace.  
4. **FIN/RESET** — používá se pro řádné uzavření nebo náhlé ukončení.

### Fragmentace a přeuspořádání

Protože I2P tunnely zavádějí latenci a změnu pořadí zpráv, knihovna ukládá pakety z neznámých nebo předčasně přicházejících streamů do vyrovnávací paměti. Uložené zprávy jsou uchovávány až do dokončení synchronizace, což zajišťuje úplné doručení ve správném pořadí.

### Vynucení protokolu

Volba `i2p.streaming.enforceProtocol=true` (výchozí od verze 0.9.36) zajišťuje, že připojení používají správné číslo I2CP protokolu, čímž zabraňuje konfliktům mezi více subsystémy sdílejícími jednu destinaci.

---

## Interoperabilita a osvědčené postupy

Protokol streaming koexistuje s **Datagram API**, což vývojářům poskytuje možnost volby mezi spojově orientovanou a nespojovou přenosovou vrstvou.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Use Case</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended Transport</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reliable, ordered data (HTTP, IRC, FTP)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Streaming</strong></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connectionless or lossy data (DNS, telemetry)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Datagram</strong></td>
    </tr>
  </tbody>
</table>
### Sdílení klienti

Aplikace mohou opětovně využívat existující tunnely tím, že běží jako **sdílení klienti**, což umožňuje více službám sdílet stejnou destinaci. I když to snižuje režii, zvyšuje to riziko korelace mezi službami—používejte opatrně.

### Řízení zahlcení

- Vrstva streamování se průběžně přizpůsobuje latenci a propustnosti sítě prostřednictvím zpětné vazby založené na RTT.
- Aplikace fungují nejlépe, když routery jsou přispívajícími uzly (zapnuté účastnické tunnely).
- Mechanismy kontroly zahlcení podobné TCP zabraňují přetížení pomalých uzlů a pomáhají vyvážit využití šířky pásma napříč tunnely.

### Úvahy o latenci

Protože I2P přidává několik stovek milisekund základní latence, aplikace by měly minimalizovat počet přenosů tam a zpět. Pokud je to možné, seskupte data s navázáním spojení (např. HTTP požadavky v SYN). Vyhněte se návrhům spoléhajícím na mnoho malých sekvenčních výměn dat.

---

## Testování a Kompatibilita

- Vždy testujte proti **Java I2P** i **i2pd**, abyste zajistili plnou kompatibilitu.
- Ačkoli je protokol standardizovaný, mohou existovat drobné rozdíly v implementaci.
- Zacházejte s staršími routery ohleduplně—mnoho protějšků stále používá verze před 2.0.
- Sledujte statistiky připojení pomocí `I2PSocket.getOptions()` a `getSession()` pro čtení RTT a metrik retransmise.

Výkon značně závisí na konfiguraci tunnelu:   - **Krátké tunnely (1–2 hopy)** → nižší latence, snížená anonymita.   - **Dlouhé tunnely (3+ hopy)** → vyšší anonymita, zvýšené RTT.

---

## Klíčová vylepšení (2.0.0–2.10.0)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Introduced</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Persistent ACK Bundling</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.0.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Optimized round-trip reduction for HTTP workloads.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Adaptive Window Scaling</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.3.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Improved large file transfer stability.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Thread Pooling and Socket Reuse</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.5.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reduced per-connection overhead.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Protocol Enforcement Default</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.36</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ensures correct stream usage.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Hybrid ML-KEM Ratchet</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Adds post-quantum hybrid encryption layer.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>i2pd Streaming API Compatibility Fixes</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.9.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Full parity with Java I2P library behavior.</td>
    </tr>
  </tbody>
</table>
---

## Shrnutí

**I2P Streaming Library** je páteří veškeré spolehlivé komunikace v rámci I2P. Zajišťuje doručování zpráv ve správném pořadí, autentizované a šifrované, a poskytuje téměř přímou náhradu za TCP v anonymních prostředích.

Pro dosažení optimálního výkonu: - Minimalizujte počet přenosů pomocí sdružování SYN+payload.   - Upravte parametry okna a timeoutu podle vašeho zatížení.   - U aplikací citlivých na latenci upřednostněte kratší tunnely.   - Používejte návrhy šetrné ke kongesti, abyste nepřetěžovali ostatní uzly.
