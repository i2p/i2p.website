---
title: "Streamovací protokol"
description: "Spolehlivý transport podobný TCP, používaný většinou I2P aplikací"
slug: "streaming"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## Přehled

I2P Streaming Library (knihovna pro streamování v I2P) poskytuje spolehlivé, se zachováním pořadí a autentizované doručování dat nad nespolehlivou vrstvou zpráv I2P — analogicky k TCP nad IP. Používají ji téměř všechny interaktivní aplikace I2P, jako je prohlížení webu, IRC, e‑mail a sdílení souborů.

Zajišťuje spolehlivý přenos, řízení zahlcení, retransmise a řízení toku napříč anonymními I2P tunnels s vysokou latencí. Každý datový proud je mezi destinacemi plně šifrován end-to-end.

---

## Základní principy návrhu

Streamovací knihovna implementuje **jednofázové navázání spojení**, kde příznaky SYN, ACK a FIN mohou nést užitečná data ve stejné zprávě. To minimalizuje počet kol cesty v prostředích s vysokou latencí — malá HTTP transakce se může dokončit během jediného kola cesty.

Řízení zahlcení a opětovné odesílání jsou inspirovány TCP, ale přizpůsobeny prostředí I2P. Velikost okna je založená na zprávách, nikoli na bajtech, a je vyladěna s ohledem na latenci tunnelu a režii. Protokol podporuje pomalý start, vyhýbání se zahlcení a exponenciální backoff (exponenciální zpožďování), podobně jako AIMD algoritmus TCP.

---

## Architektura

Streamovací knihovna funguje mezi aplikacemi a rozhraním I2CP.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Layer</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Responsibility</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Application</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Standard I2PSocket and I2PServerSocket usage</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Streaming Library</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connection setup, sequencing, retransmission, and flow control</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2CP</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel creation, routing, and message handling</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2NP / Router Layer</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Transport through tunnels</td>
    </tr>
  </tbody>
</table>
Většina uživatelů k němu přistupuje přes I2PSocketManager, I2PTunnel nebo SAMv3. Knihovna transparentně zajišťuje správu destinací, práci s tunnel a retransmise.

---

## Formát paketu

```
+-----------------------------------------------+
| Send Stream ID (4B) | Receive Stream ID (4B) |
+-----------------------------------------------+
| Sequence Number (4B) | Ack Through (4B)      |
+-----------------------------------------------+
| NACK Count (1B) | optional NACK list (4B each)
+-----------------------------------------------+
| Flags (1B) | Option Size (1B) | Options ...   |
+-----------------------------------------------+
| Payload ...                                  |
```
### Podrobnosti hlavičky

- **Identifikátory streamů**: 32bitové hodnoty, které jednoznačně identifikují lokální a vzdálené streamy.
- **Sekvenční číslo**: Začíná na 0 pro SYN, inkrementuje se pro každou zprávu.
- **Potvrzení až do**: Potvrzuje všechny zprávy až do N, s výjimkou těch v seznamu NACK.
- **Příznaky**: Bitová maska řídicí stav a chování.
- **Volby**: Seznam proměnné délky pro RTT, MTU a vyjednávání protokolu.

### Příznaky klíče

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Flag</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SYN</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connection initiation</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ACK</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Acknowledge received packets</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">FIN</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Graceful close</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RST</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reset connection</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">FROM_INCLUDED</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Sender’s destination included</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SIGNATURE_INCLUDED</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Message signed by sender</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECHO / ECHO_REPLY</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ping/Pong keepalive</td>
    </tr>
  </tbody>
</table>
---

## Řízení toku a spolehlivost

Streaming používá **okenní řízení založené na zprávách**, na rozdíl od bajtově orientovaného přístupu TCP. Počet nepotvrzených paketů povolených v letu se rovná aktuální velikosti okna (výchozí 128).

### Mechanismy

- **Řízení zahlcení:** Pomalý start a vyhýbání založené na AIMD (aditivní zvýšení/multiplikativní snížení).  
- **Choke/Unchoke (škrcení/uvolnění):** Signalizace řízení toku založená na zaplnění vyrovnávací paměti.  
- **Retransmise:** Výpočet RTO podle RFC 6298 s exponenciálním backoffem (exponenciální prodlužování čekací doby).  
- **Filtrování duplicit:** Zajišťuje spolehlivost nad potenciálně přeuspořádanými zprávami.

Typické hodnoty konfigurace:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Parameter</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Default</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>maxWindowSize</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Max unacknowledged messages</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>maxMessageSize</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1730</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Maximum payload bytes per message</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>initialRTO</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">9000 ms</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Initial retransmission timeout</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>inactivityTimeout</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">90000 ms</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Idle connection timeout</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>connectTimeout</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">300000 ms</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connection establishment timeout</td>
    </tr>
  </tbody>
</table>
---

## Navázání spojení

1. **Iniciátor** odešle SYN (volitelně s užitečnými daty a FROM_INCLUDED).  
2. **Odpovídající strana** odpoví SYN+ACK (může obsahovat užitečná data).  
3. **Iniciátor** odešle závěrečný ACK potvrzující navázání spojení.

Volitelná počáteční užitečná data umožňují přenos dat ještě před úplným dokončením handshake.

---

## Podrobnosti implementace

### Retransmise a časový limit

Algoritmus retransmise se řídí **RFC 6298**.   - **Počáteční RTO:** 9s   - **Minimální RTO:** 100ms   - **Maximální RTO:** 45s   - **Alfa:** 0.125   - **Beta:** 0.25

### Sdílení řídicího bloku

Nedávná spojení se stejným peerem znovu využívají předchozí data RTT a okna pro rychlejší náběh, čímž se vyhnou latenci „studeného startu“. Řídicí bloky vyprší po několika minutách.

### MTU a fragmentace

- Výchozí MTU: **1730 bajtů** (pojme dvě I2NP zprávy).  
- ECIES destinace: **1812 bajtů** (snížená režie).  
- Minimální podporované MTU: 512 bajtů.

Velikost užitečných dat nezahrnuje minimální streamingovou hlavičku o velikosti 22 bajtů.

---

## Historie verzí

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Router Version</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.7.1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Protocol numbers defined in I2CP</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.11</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Variable-length signatures</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA signature support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ed25519 signature support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.18</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ping/Pong payloads</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.20</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">FROM_INCLUDED not required in RESET</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.36</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Protocol enforcement enabled by default</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.39</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">OFFLINE_SIGNATURE support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.58</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Bob’s hash added to NACK field in SYN</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Post-Quantum hybrid encryption (experimental)</td>
    </tr>
  </tbody>
</table>
---

## Použití na aplikační úrovni

### Příklad v Javě

```java
Properties props = new Properties();
props.setProperty("i2p.streaming.maxWindowSize", "512");
I2PSocketManager mgr = I2PSocketManagerFactory.createManager(props);

I2PSocket socket = mgr.connect(destination);
InputStream in = socket.getInputStream();
OutputStream out = socket.getOutputStream();
```
### Podpora SAMv3 a i2pd

- **SAMv3**: Poskytuje režimy STREAM a DATAGRAM pro klienty nepsané v jazyce Java.  
- **i2pd**: Zpřístupňuje totožné parametry streamování prostřednictvím voleb v konfiguračním souboru (např. `i2p.streaming.maxWindowSize`, `profile`, atd.).

---

## Volba mezi streamováním a datagramy

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Use Case</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended Transport</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Reason</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HTTP, IRC, Email</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Streaming</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Requires reliability</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DNS</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Repliable Datagram</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Single request/response</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Telemetry, Logging</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Raw Datagram</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Best-effort acceptable</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P2P DHT</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Datagram</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">High connection churn</td>
    </tr>
  </tbody>
</table>
---

## Bezpečnost a postkvantová budoucnost

Streamingové relace jsou na vrstvě I2CP šifrovány end-to-end.   Postkvantové hybridní šifrování (ML-KEM + X25519) je v 2.10.0 experimentálně podporováno, ale ve výchozím nastavení je vypnuto.

---

## Reference

- [Přehled API pro streamování](/docs/specs/streaming/)  
- [Specifikace protokolu pro streamování](/docs/specs/streaming/)  
- [Specifikace I2CP](/docs/specs/i2cp/)  
- [Návrh 144: Výpočty MTU pro streamování](/proposals/144-ecies-x25519-aead-ratchet/)  
- [Poznámky k vydání I2P 2.10.0](/cs/blog/2025/09/08/i2p-2.10.0-release/)
