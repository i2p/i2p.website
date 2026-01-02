---
title: "Datagramy"
description: "Autentizované, zodpověditelné a neupravené formáty zpráv nad I2CP"
slug: "datagrams"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
toc: true
---

## Přehled

Datagramy poskytují komunikaci orientovanou na zprávy nad [I2CP](/docs/specs/i2cp/) a paralelně s knihovnou pro streamování. Umožňují **odpovídatelné**, **autentizované** nebo **surové** pakety bez nutnosti spojově orientovaných streamů. Routery zapouzdřují datagramy do I2NP zpráv a tunnel zpráv bez ohledu na to, zda je přenos přenášen přes NTCP2 nebo SSU2.

Hlavní motivací je umožnit aplikacím (jako jsou trackery, DNS resolvery nebo hry) odesílat samostatné pakety, které identifikují svého odesílatele.

> **Nové v roce 2025:** Projekt I2P schválil **Datagram2 (protokol 19)** a **Datagram3 (protokol 20)**, které po deseti letech poprvé přidávají ochranu proti opakování zpráv a zasílání zpráv s nižší režijní zátěží, na které lze odpovědět.

---

## 1. Konstanty protokolu

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Value</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Introduced</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>PROTO_DATAGRAM</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">17</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Signed (repliable) datagram – “Datagram1”</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Original</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>PROTO_DATAGRAM_RAW</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unsigned (raw) datagram – no sender info</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Original</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>PROTO_DATAGRAM2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Signed + replay-protected datagram</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">API 0.9.66 (2025)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>PROTO_DATAGRAM3</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Repliable (no signature, hash only)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">API 0.9.66 (2025)</td>
    </tr>
  </tbody>
</table>
Protokoly 19 a 20 byly formalizovány v **Návrhu 163 (duben 2025)**. Koexistují s Datagram1 / RAW kvůli zpětné kompatibilitě.

---

## 2. Typy datagramů

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Repliable</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Authenticated</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Replay Protection</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Min Overhead</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Raw</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Minimal size; spoofable.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Datagram1</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">17</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">≈ 427</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Full Destination + signature.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Datagram2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">≈ 457</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Replay prevention + offline signatures; PQ-ready.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Datagram3</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">≈ 34</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Sender hash only; low overhead.</td>
    </tr>
  </tbody>
</table>
### Typické návrhové vzory

- **Požadavek → Odpověď:** Odešlete podepsaný Datagram2 (požadavek + nonce), obdržíte odpověď RAW nebo Datagram3 (echo nonce).  
- **Vysoká frekvence/nízká režie:** Preferujte Datagram3 nebo RAW.  
- **Autentizované kontrolní zprávy:** Datagram2.  
- **Kompatibilita se starším systémem:** Datagram1 stále plně podporován.

---

## 3. Podrobnosti o Datagram2 a Datagram3 (2025)

### Datagram2 (Protokol 19)

Vylepšená náhrada za Datagram1. Funkce: - **Ochrana proti opakování:** 4-bajtový token proti opakování. - **Podpora offline podpisů:** umožňuje použití offline podepsaných Destinací. - **Rozšířené pokrytí podpisem:** zahrnuje hash destinace, příznaky, možnosti, blok offline podpisu, payload. - **Připraveno pro post-kvantovou kryptografii:** kompatibilní s budoucími ML-KEM hybridy. - **Režie:** ≈ 457 bajtů (klíče X25519).

### Datagram3 (Protokol 20)

Překlenuje propast mezi čistými a podepsanými typy. Vlastnosti: - **Odpověditelné bez podpisu:** obsahuje 32-bajtový hash odesílatele + 2-bajtové příznaky. - **Minimální režie:** ≈ 34 bajtů. - **Žádná ochrana proti opakování** — musí implementovat aplikace.

Oba protokoly jsou funkcemi API 0.9.66 a jsou implementovány v Java routeru od vydání 2.9.0; zatím neexistují implementace v i2pd ani Go (říjen 2025).

---

## 4. Limity velikosti a fragmentace

- **Velikost tunnel zprávy:** 1 028 bajtů (4 B Tunnel ID + 16 B IV + 1 008 B datová část).  
- **Počáteční fragment:** 956 B (typické TUNNEL doručení).  
- **Následující fragment:** 996 B.  
- **Maximální počet fragmentů:** 63–64.  
- **Praktický limit:** ≈ 62 708 B (~61 KB).  
- **Doporučený limit:** ≤ 10 KB pro spolehlivé doručení (ztráty se za touto hranicí exponenciálně zvyšují).

**Shrnutí režie:** - Datagram1 ≈ 427 B (minimum).   - Datagram2 ≈ 457 B.   - Datagram3 ≈ 34 B.   - Další vrstvy (I2CP gzip hlavička, I2NP, Garlic, Tunnel): + ~5,5 KB v nejhorším případě.

---

## 5. Integrace I2CP / I2NP

Cesta zprávy: 1. Aplikace vytvoří datagram (přes I2P API nebo SAM).   2. I2CP zabalí s gzip hlavičkou (`0x1F 0x8B 0x08`, RFC 1952) a CRC-32 kontrolním součtem.   3. Čísla protokolu + portu jsou uložena v polích gzip hlavičky.   4. Router zapouzdří jako I2NP zprávu → Garlic clove → 1 KB tunnel fragmenty.   5. Fragmenty procházejí odchozím → sítí → příchozím tunelem.   6. Znovu sestavený datagram je doručen handleru aplikace na základě čísla protokolu.

**Integrita:** CRC-32 (z I2CP) + volitelný kryptografický podpis (Datagram1/2). V samotném datagramu není samostatné pole kontrolního součtu.

---

## 6. Programovací rozhraní

### Java API

Balíček `net.i2p.client.datagram` obsahuje: - `I2PDatagramMaker` – vytváří podepsané datagramy.   - `I2PDatagramDissector` – ověřuje a extrahuje informace o odesílateli.   - `I2PInvalidDatagramException` – vyvolána při selhání ověření.

`I2PSessionMuxedImpl` (`net.i2p.client.impl.I2PSessionMuxedImpl`) spravuje multiplexování protokolu a portů pro aplikace sdílející Destination.

**Přístup k Javadoc:** - [idk.i2p Javadoc](http://idk.i2p/javadoc-i2p/) (pouze síť I2P) - [Javadoc Mirror](https://eyedeekay.github.io/javadoc-i2p/) (clearnet zrcadlo) - [Oficiální Javadocs](http://docs.i2p-projekt.de/javadoc/) (oficiální dokumentace)

### Podpora SAM v3

- SAM 3.2 (2016): přidány parametry PORT a PROTOCOL.  
- SAM 3.3 (2016): zaveden model PRIMARY/subsession; umožňuje streamy + datagramy na jednom Destination.  
- Podpora pro styly relací Datagram2 / 3 přidána do specifikace 2025 (implementace probíhá).  
- Oficiální specifikace: [SAM v3 Specification](/docs/api/samv3/)

### i2ptunnel moduly

- **udpTunnel:** Plně funkční základ pro I2P UDP aplikace (`net.i2p.i2ptunnel.udpTunnel`).  
- **streamr:** Funkční pro A/V streaming (`net.i2p.i2ptunnel.streamr`).  
- **SOCKS UDP:** **Nefunkční** od verze 2.10.0 (pouze UDP stub).

> Pro obecné UDP použijte Datagram API nebo přímo udpTunnel—nespoléhejte na SOCKS UDP.

---

## 7. Ekosystém a jazyková podpora (2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Language</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Library / Package</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">SAM Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Java</td><td style="border:1px solid var(--color-border); padding:0.5rem;">core API (net.i2p.client.datagram)</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✓ full support</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">C++</td><td style="border:1px solid var(--color-border); padding:0.5rem;">i2pd / libsam3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2 partial</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Limited</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Go</td><td style="border:1px solid var(--color-border); padding:0.5rem;">go-i2p / sam3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1–3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td><td style="border:1px solid var(--color-border); padding:0.5rem;">i2plib, i2p.socket, txi2p</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Rust</td><td style="border:1px solid var(--color-border); padding:0.5rem;">i2p-rs, i2p_client</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">C#</td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2PSharp</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">JS/TS</td><td style="border:1px solid var(--color-border); padding:0.5rem;">node-i2p, i2p-sam</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Haskell</td><td style="border:1px solid var(--color-border); padding:0.5rem;">network-anonymous-i2p</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Lua</td><td style="border:1px solid var(--color-border); padding:0.5rem;">mooni2p</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental</td></tr>
  </tbody>
</table>
Java I2P je v současné době jediný router podporující plné SAM 3.3 subsessions a Datagram2 API.

---

## 8. Příklad použití – UDP Tracker (I2PSnark 2.10.0)

První aplikace Datagram2/3 v reálném světě:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Datagram Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Announce Request</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Datagram3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Repliable but low-overhead update</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Response</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Raw Datagram</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimal payload return</td></tr>
  </tbody>
</table>
Vzor demonstruje smíšené použití autentizovaných a lehkých datagramů pro vyvážení bezpečnosti a výkonu.

---

## 9. Bezpečnost a osvědčené postupy

- Použijte Datagram2 pro jakoukoliv autentizovanou výměnu nebo když záleží na replay útocích.
- Upřednostněte Datagram3 pro rychlé odpovědi s možností odpovědět při střední důvěryhodnosti.
- Použijte RAW pro veřejné vysílání nebo anonymní data.
- Udržujte velikost payloadů ≤ 10 KB pro spolehlivé doručení.
- Mějte na paměti, že SOCKS UDP zůstává nefunkční.
- Vždy ověřujte gzip CRC a digitální podpisy při příjmu.

---

## 10. Technická specifikace

Tato sekce pokrývá nízkoúrovňové formáty datagramů, zapouzdření a detaily protokolů.

### 10.1 Identifikace protokolu

Formáty datagramů **nemají** společnou hlavičku. Routery nemohou odvodit typ pouze z bajtů datové části.

Při kombinaci více typů datagramů—nebo při kombinaci datagramů se streamováním—explicitně nastavte: - **Číslo protokolu** (přes I2CP nebo SAM) - Volitelně **číslo portu**, pokud vaše aplikace multiplexuje služby

Ponechání protokolu nenastavené hodnoty (`0` nebo `PROTO_ANY`) se nedoporučuje a může vést k chybám směrování nebo doručení.

### 10.2 Hrubé datagramy

Non-repliable datagramy nenesou žádná data odesílatele ani autentizační data. Jedná se o neprůhledné datové náklady, zpracovávané mimo vyšší úroveň datagram API, ale podporované prostřednictvím SAM a I2PTunnel.

**Protokol:** `18` (`PROTO_DATAGRAM_RAW`)

**Formát:**

```
+----+----+----+----+----//
|     payload...
+----+----+----+----+----//
```
Délka payload je omezena limity transportu (≈32 KB praktické maximum, často mnohem méně).

### 10.3 Datagram1 (Odpověditelné datagramy)

Obsahuje **Destination** odesílatele a **Signature** pro autentizaci a zpětnou adresaci.

**Protokol:** `17` (`PROTO_DATAGRAM`)

**Režie:** ≥427 bajtů **Datová část:** až ~31,5 KB (omezeno transportem)

**Formát:**

```
+----+----+----+----+----+----+----+----+
|               from                    |
+                                       +
|                                       |
~             Destination bytes         ~
|                                       |
+----+----+----+----+----+----+----+----+
|             signature                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|     payload...
+----+----+----+----//
```
- `from`: Destination (387+ bajtů)
- `signature`: podpis odpovídající typu klíče
  - Pro DSA_SHA1: Podpis SHA-256 hashe užitečného zatížení
  - Pro ostatní typy klíčů: Podpis přímo nad užitečným zatížením

**Poznámky:** - Podpisy pro typy jiné než DSA byly standardizovány v I2P 0.9.14. - LS2 (Návrh 123) offline podpisy nejsou v současnosti podporovány v Datagram1.

### 10.4 Formát Datagram2

Vylepšený replikovatelný datagram, který přidává **odolnost proti replay útokům** jak je definováno v [Proposal 163](/proposals/163-datagram2/).

**Protokol:** `19` (`PROTO_DATAGRAM2`)

Implementace probíhá. Aplikace by měly zahrnovat kontroly nonce nebo časového razítka pro zajištění redundance.

### 10.5 Formát Datagram3

Poskytuje **odpověditelné, ale neautentizované** datagramy. Spoléhá na autentizaci relace udržovanou routerem místo vestavěné destinace a podpisu.

**Protokol:** `20` (`PROTO_DATAGRAM3`) **Stav:** Ve vývoji od verze 0.9.66

Užitečné když: - Destinace jsou velké (např. post-kvantové klíče) - Autentizace probíhá na jiné vrstvě - Efektivita šířky pásma je kritická

### 10.6 Integrita dat

Integrita datagramu je chráněna **gzip CRC-32 kontrolním součtem** ve vrstvě I2CP. V samotném formátu datagramové zátěže neexistuje žádné explicitní pole kontrolního součtu.

### 10.7 Zapouzdření paketů

Každý datagram je zapouzdřen jako jediná I2NP zpráva nebo jako jednotlivý clove (segment) v **Garlic Message**. I2CP, I2NP a vrstvy tunelů zpracovávají délku a rámování — v datagramovém protokolu není žádný interní oddělovač ani pole délky.

### 10.8 Úvahy o post-kvantové kryptografii (PQ)

Pokud bude implementován **Proposal 169** (ML-DSA podpisy), velikost podpisů a destinací se dramaticky zvýší — z ~455 bajtů na **≥3739 bajtů**. Tato změna podstatně zvýší režii datagramu a sníží efektivní kapacitu datové části.

**Datagram3**, který se spoléhá na autentizaci na úrovni relace (nikoli na vestavěné podpisy), se pravděpodobně stane preferovaným návrhem v postkvantových prostředích I2P.

---

## 11. Reference

- [Návrh 163 – Datagram2 a Datagram3](/proposals/163-datagram2/)
- [Návrh 160 – Integrace UDP Trackeru](/proposals/160-udp-trackers/)
- [Návrh 144 – Výpočty MTU pro Streaming](/proposals/144-ecies-x25519-aead-ratchet/)
- [Návrh 169 – Post-kvantové podpisy](/proposals/169-pq-crypto/)
- [Specifikace I2CP](/docs/specs/i2cp/)
- [Specifikace I2NP](/docs/specs/i2np/)
- [Specifikace Tunnel zpráv](/docs/specs/implementation/)
- [Specifikace SAM v3](/docs/api/samv3/)
- [Dokumentace i2ptunnel](/docs/api/i2ptunnel/)

## 12. Hlavní body změnového protokolu (2019 – 2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Year</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Release</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Change</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2019</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.43</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Datagram API stabilization</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2021</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.50</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Protocol port handling reworked</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2022</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2.0.0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 adoption completed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2024</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2.6.0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy transport removal simplified UDP code</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2025</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2.9.0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Datagram2/3 support added (Java API)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2025</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2.10.0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">UDP Tracker implementation released</td></tr>
  </tbody>
</table>
---

## 13. Shrnutí

Subsystém datagramů nyní podporuje čtyři varianty protokolu nabízející spektrum od plně autentizovaného až po lehký přenos surových dat. Vývojáři by měli přejít na **Datagram2** pro bezpečnostně citlivé použití a **Datagram3** pro efektivní provoz s možností odpovědi. Všechny starší typy zůstávají kompatibilní pro zajištění dlouhodobé interoperability.
