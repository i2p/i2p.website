---
title: "Průvodce provozem tunnel"
description: "Jednotná specifikace pro vytváření, šifrování a přenášení provozu pomocí I2P tunnels."
slug: "implementation"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
reviewStatus: "needs-review"
---

> **Rozsah:** Tato příručka sjednocuje implementaci tunnelu, formát zpráv a obě specifikace pro vytváření tunnelů (ECIES a starší ElGamal). Stávající hluboké odkazy nadále fungují prostřednictvím výše uvedených aliasů.

## Model Tunnel {#tunnel-model}

I2P přeposílá užitečná data prostřednictvím *jednosměrných tunnels*: uspořádaných sad routers, které přenášejí provoz jedním směrem. Plná cesta tam a zpět mezi dvěma cíli vyžaduje čtyři tunnels (dva odchozí, dva příchozí).

Začněte s [Tunnel Overview](/docs/overview/tunnel-routing/) pro seznámení s terminologií, poté použijte tuto příručku pro provozní podrobnosti.

### Životní cyklus zprávy {#message-lifecycle}

1. tunnel **brána** seskupí jednu nebo více zpráv I2NP, rozdělí je na fragmenty a zapíše pokyny pro doručení.
2. **Brána** zapouzdří užitečná data do zprávy tunnel pevné velikosti (1024&nbsp;B), v případě potřeby doplní výplň.
3. Každý **účastník** ověří předchozí skok, aplikuje svou šifrovací vrstvu a předá {nextTunnelId, nextIV, encryptedPayload} dalšímu skoku.
4. tunnel **koncový bod** odstraní poslední vrstvu, zpracuje pokyny pro doručení, znovu sestaví fragmenty a odešle rekonstruované zprávy I2NP.

Detekce duplikátů používá stárnoucí Bloomův filtr, klíčovaný bitovým XORem IV (inicializačního vektoru) a prvního bloku šifrotextu, aby zabránila značkovacím útokům založeným na záměně IV.

### Rychlý přehled rolí {#roles}

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Role</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Pre-processing</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Crypto Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Post-processing</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outbound gateway (creator)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fragment, batch, pad</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Iteratively <em>decrypt</em> using every hop’s keys (so downstream peers encrypt)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to first hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Participant</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt IV and payload with hop keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outbound endpoint</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt once more to reveal plaintext payload</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deliver to target tunnel/destination</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Inbound gateway</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fragment, batch, pad</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt with local keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Inbound endpoint (creator)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Iteratively decrypt using stored hop keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reassemble and deliver locally</td>
    </tr>
  </tbody>
</table>
### Postup šifrování {#encryption-workflow}

- **Inbound tunnels:** brána jednou zašifruje svým klíčem vrstvy; následující účastníci pokračují v šifrování, dokud tvůrce tunnelu nedešifruje finální užitečná data.
- **Outbound tunnels:** brána předem aplikuje inverzi šifrování každého skoku, takže každý účastník šifruje. Když koncový bod zašifruje, odhalí se původní otevřený text brány.

Oba směry předávají `{tunnelId, IV, encryptedPayload}` dalšímu uzlu.

---

## Formát zprávy pro tunnel {#tunnel-message-format}

Vstupní brány tunelu fragmentují zprávy I2NP do obálek pevné velikosti, aby skryly délku užitečných dat a zjednodušily zpracování na každém skoku.

### Šifrované uspořádání {#encrypted-layout}

```
+----------------+----------------+-------------------+
| Tunnel ID (4B) | IV (16B)       | Encrypted payload |
+----------------+----------------+-------------------+
```
- **Tunnel ID** – 32bitový identifikátor pro další uzel (nenulový, obměňuje se v každém cyklu sestavení).
- **IV** – 16bajtový AES IV (inicializační vektor) zvolený pro každou zprávu.
- **Šifrovaná užitečná data** – 1008 bajtů šifrotextu AES-256-CBC.

Celková velikost: 1028 bajtů.

### Dešifrované uspořádání {#decrypted-layout}

Poté, co uzel odstraní svou vrstvu šifrování:

```
[Checksum (4B)][Padding ... 0x00 terminator]
[Delivery Instructions 1][I2NP fragment 1]
[Delivery Instructions 2][I2NP fragment 2]
...
```
- **Kontrolní součet** ověřuje dešifrovaný blok.
- **Výplň** jsou náhodné nenulové bajty ukončené nulovým bajtem.
- **Pokyny pro doručení** sdělují koncovému bodu, jak nakládat s každým fragmentem (doručit lokálně, předat do jiného tunnelu apod.).
- **Fragmenty** nesou podkladové zprávy I2NP; koncový bod je znovu sestaví předtím, než je předá vyšším vrstvám.

### Kroky zpracování {#processing-steps}

1. Brány fragmentují a řadí do fronty zprávy I2NP, přičemž dočasně uchovávají částečné fragmenty pro opětovné sestavení.
2. Brána šifruje užitečná data příslušnými klíči vrstvy a nastaví tunnel ID a IV (inicializační vektor).
3. Každý účastník zašifruje IV (AES-256/ECB) a poté užitečná data (AES-256/CBC), následně znovu zašifruje IV a zprávu předá dál.
4. Koncový uzel dešifruje v opačném pořadí, ověří kontrolní součet, zpracuje pokyny pro doručení a znovu sestaví fragmenty.

---

## Vytváření tunnelu (ECIES-X25519) {#tunnel-creation-ecies}

Moderní routers vytvářejí tunnels s klíči ECIES-X25519, čímž zmenšují velikost sestavovacích zpráv a umožňují dopředné utajení.

- **Sestavovací zpráva:** jediná zpráva I2NP `TunnelBuild` (nebo `VariableTunnelBuild`) nese 1–8 šifrovaných sestavovacích záznamů, jeden na hop.
- **Klíče vrstvy:** tvůrce odvozuje pro každý hop klíče vrstvy, IV a odpovědi pomocí HKDF s využitím statické identity X25519 daného hopu a svého efemérního klíče.
- **Zpracování:** každý hop dešifruje svůj záznam, ověří příznaky požadavku, zapíše odpovědní blok (úspěch nebo podrobný kód selhání), znovu zašifruje zbývající záznamy a předá zprávu dál.
- **Odpovědi:** tvůrce obdrží odpovědní zprávu zabalenou pomocí garlic encryption. Záznamy označené jako neúspěšné obsahují kód závažnosti, aby mohl router profilovat protějšek.
- **Kompatibilita:** routery mohou kvůli zpětné kompatibilitě nadále přijímat starší sestavení na bázi ElGamalu, ale nové tunnely ve výchozím nastavení používají ECIES.

> Pro konstanty pro jednotlivá pole a poznámky k derivaci klíčů viz historii návrhu ECIES a zdrojový kód routeru; tato příručka popisuje provozní tok.

---

## Zastaralé vytváření Tunnel (ElGamal-2048) {#tunnel-creation-elgamal}

Původní formát pro vytváření tunnel používal ElGamalovy veřejné klíče. Moderní routers zachovávají omezenou podporu kvůli zpětné kompatibilitě.

> **Stav:** Zastaralé. Ponecháno zde pro historickou referenci a pro každého, kdo udržuje nástroje kompatibilní se staršími verzemi.

- **Neinteraktivní teleskopování:** jediná sestavovací zpráva prochází celou trasu. Každý hop dešifruje svůj 528bajtový záznam, aktualizuje zprávu a předá ji dál.
- **Proměnná délka:** Variable Tunnel Build Message (VTBM; proměnná zpráva pro sestavení Tunnelu) umožňovala 1–8 záznamů. Dřívější pevná zpráva vždy obsahovala osm záznamů, aby zamaskovala délku tunnelu.
- **Struktura záznamu požadavku:**

```
Bytes 0–3    : Tunnel ID (receiving ID)
Bytes 4–35   : Current hop router hash
Bytes 36–39  : Next tunnel ID
Bytes 40–71  : Next hop router hash
Bytes 72–103 : AES-256 layer key
Bytes 104–135: AES-256 IV key
Bytes 136–167: AES-256 reply key
Bytes 168–183: AES-256 reply IV
Byte 184     : Flags (bit7=IBGW, bit6=OBEP)
Bytes 185–188: Request time (hours since epoch)
Bytes 189–192: Next message ID
Bytes 193–221: Padding
```
- **Příznaky:** bit 7 označuje vstupní bránu (inbound gateway, IBGW); bit 6 označuje výstupní koncový bod (outbound endpoint, OBEP). Navzájem se vylučují.
- **Šifrování:** každý záznam je šifrován algoritmem ElGamal-2048 veřejným klíčem příslušného uzlu. Symetrické vrstvení AES-256-CBC zajišťuje, že záznam si přečte pouze zamýšlený uzel.
- **Klíčová fakta:** identifikátory tunnelu jsou nenulové 32bitové hodnoty; tvůrci mohou vkládat falešné záznamy, aby skryli skutečnou délku tunnelu; spolehlivost závisí na opakování neúspěšných pokusů o sestavení.

---

## Pooly tunnelů a životní cyklus {#tunnel-pools}

Routers udržují nezávislé příchozí a odchozí tunnel pooly pro průzkumný provoz a pro každou relaci I2CP.

- **Výběr peerů:** průzkumné tunnels čerpají ze skupiny peerů „active, not failing“ pro podporu diverzity; klientské tunnels preferují rychlé peery s vysokou kapacitou.
- **Deterministické řazení:** peery jsou seřazeny podle XOR vzdálenosti mezi `SHA256(peerHash || poolKey)` a náhodným klíčem daného poolu. Klíč se při restartu rotuje, což zajišťuje stabilitu v rámci jednoho běhu a zároveň ztěžuje predecessor attacks (útoky předchůdce) napříč běhy.
- **Životní cyklus:** routers sledují historické časy sestavování pro n-tici `{mode, direction, length, variance}`. Jak se tunnels blíží expiraci, náhrady začínají dříve; router zvyšuje počet paralelních sestavení při výskytu selhání, zároveň omezuje počet otevřených pokusů.
- **Konfigurační parametry:** počty aktivních/záložních tunnels, délka a odchylka počtu hopů, povolení zero-hop (nulový počet hopů) a limity rychlosti sestavování jsou nastavitelné pro každý pool.

---

## Přetížení a spolehlivost {#congestion}

Ačkoli tunnels připomínají okruhy, routers s nimi zacházejí jako s frontami zpráv. K udržení latence v mezích se používá Weighted Random Early Discard (WRED; vážené náhodné předčasné zahazování):

- Pravděpodobnost zahazování roste, jak se zatížení blíží nakonfigurovaným limitům.
- Účastníci uvažují fragmenty pevné velikosti; brány/koncové body zahazují podle souhrnné velikosti fragmentů a přednostně zahazují velká užitečná data.
- Výstupní koncové body zahazují dříve než jiné role, aby se co nejméně plýtvalo síťovými prostředky.

Zaručené doručování je ponecháno vyšším vrstvám, jako je [Streaming library (knihovna pro streamování)](/docs/specs/streaming/). Aplikace, které vyžadují spolehlivost, si musí samy zajišťovat retransmise a potvrzování.

---

## Další čtení {#further-reading}

- [Jednosměrné tunnels (historické)](/docs/legacy/unidirectional-tunnels/)
- [Výběr peerů](/docs/overview/tunnel-routing#peer-selection/)
- [Přehled Tunnel](/docs/overview/tunnel-routing/)
- [Stará implementace Tunnel](/docs/legacy/old-implementation/)
