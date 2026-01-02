---
title: "I2P vs jiné sítě pro ochranu soukromí"
description: "Moderní technické a filozofické srovnání zdůrazňující jedinečné designové výhody I2P"
slug: "comparison"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Přehled

Dnes existuje několik významných sítí pro ochranu soukromí a anonymity, z nichž každá má odlišné cíle návrhu a modely hrozeb. Zatímco Tor, Lokinet, GNUnet a Freenet přispívají cennými přístupy ke komunikaci chránící soukromí, **I2P vyniká jako jediná produkčně připravená síť s přepínáním paketů plně optimalizovaná pro skryté služby uvnitř sítě a peer-to-peer aplikace.**

Následující tabulka shrnuje klíčové architektonické a provozní rozdíly mezi těmito sítěmi k roku 2025.

---

## Srovnání síťí pro ochranu soukromí (2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature / Network</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);"><strong>I2P</strong></th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);"><strong>Tor</strong></th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);"><strong>Lokinet</strong></th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);"><strong>Freenet (Hyphanet)</strong></th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);"><strong>GNUnet</strong></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Primary Focus</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Hidden services, P2P applications</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Clearnet anonymity via exits</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Hybrid VPN + hidden services</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Distributed storage & publishing</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Research framework, F2F privacy</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Architecture</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fully distributed, packet-switched</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Centralized directory, circuit-switched</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Packet-switched LLARP with blockchain coordination</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DHT-based content routing</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DHT & F2F topology (R5N)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Routing Model</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Unidirectional tunnels (inbound/outbound)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Bidirectional circuits (3 hops)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Packet-switched over staked nodes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Key-based routing</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Random walk + DHT hybrid</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Directory / Peer Discovery</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Distributed Kademlia netDB with floodfills</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">9 hardcoded directory authorities</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Blockchain + Oxen staking</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Heuristic routing</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Distributed hash routing (R5N)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Encryption</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECIES-X25519-AEAD-Ratchet (ChaCha20/Poly1305)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES + RSA/ECDH</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Curve25519/ChaCha20</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Custom symmetric encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ed25519/Curve25519</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Participation Model</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">All routers route traffic (democratic)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Small relay subset, majority are clients</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Only staked nodes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">User-selectable trust mesh</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Optional F2F restriction</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Traffic Handling</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Packet-switched, multi-path, load-balanced</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Circuit-switched, fixed path per circuit</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Packet-switched, incentivized</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">File chunk propagation</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Message batching and proof-of-work</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Garlic Routing</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Yes (message bundling & tagging)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">❌ No</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Partial (message batches)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">❌ No</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">❌ No</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Exit to Clearnet</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Limited (discouraged)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Core design goal</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported (VPN-style exits)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Not applicable</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Not applicable</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Built-In Apps</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2PSnark, I2PTunnel, SusiMail, I2PBote</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tor Browser, OnionShare</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Lokinet GUI, SNApps</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Freenet UI</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">GNUnet CLI tools</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Performance</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Optimized for internal services, 1–3s RTT</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Optimized for exits, ~200–500ms RTT</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Low latency, staked node QoS</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">High latency (minutes)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Experimental, inconsistent</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Anonymity Set Size</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">~55,000 active routers</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Millions of daily users</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">&lt;1,000 service nodes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Thousands (small core)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Hundreds (research only)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Scalability</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Horizontal via floodfill rotation</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Centralized bottleneck (directory)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Dependent on token economics</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Limited by routing heuristics</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Research-scale only</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Funding Model</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Volunteer-driven nonprofit</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Major institutional grants</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Crypto-incentivized (OXEN)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Volunteer community</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Academic research</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>License / Codebase</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Open source (Java/C++/Go)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Open source (C)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Open source (C++)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Open source (Java)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Open source (C)</td>
    </tr>
  </tbody>
</table>
---

## Proč je I2P lídrem v designu zaměřeném na soukromí

### 1. **Packet Switching > Circuit Switching**

Model spínaných okruhů v síti Tor váže provoz na pevné tříhopové cesty—efektivní pro prohlížení webu, ale křehký pro dlouhodobě běžící interní služby. **Paketově spínané tunely** I2P odesílají zprávy přes více současných cest a automaticky směrují obchází přetížení či výpadky pro lepší dostupnost a distribuci zátěže.

### 2. **Unidirectional Tunnels**

I2P odděluje příchozí a odchozí provoz. To znamená, že každý účastník vidí vždy pouze **polovinu** komunikačního toku, což výrazně ztěžuje korelační útoky založené na časování. Tor, Lokinet a další používají obousměrné okruhy, kde požadavky a odpovědi sdílejí stejnou cestu—je to jednodušší, ale lépe sledovatelné.

### 3. **Fully Distributed netDB**

Devět adresářových autorit Toru definuje topologii jeho sítě. I2P používá samořídící se **Kademlia DHT** (distribuovanou hash tabulku) spravovanou rotujícími floodfill routery, čímž eliminuje jakékoli centrální kontrolní body nebo koordinační servery.

### 1. **Přepínání paketů > Přepínání okruhů**

I2P rozšiřuje onion routing o **garlic routing**, který sdružuje více šifrovaných zpráv do jednoho kontejneru. To snižuje únik metadat a režii šířky pásma a zároveň zvyšuje efektivitu pro potvrzovací, datové a řídicí zprávy.

### 2. **Jednosměrné tunely**

Každý I2P router směruje provoz pro ostatní. Neexistují žádní vyhrazení operátoři přeposílacích uzlů ani privilegované uzly—šířka pásma a spolehlivost automaticky určují, kolik směrování uzel přispívá. Tento demokratický přístup buduje odolnost a přirozeně škáluje s růstem sítě.

### 3. **Plně distribuovaná netDB**

12-skokový okruh I2P tam a zpět (6 příchozích + 6 odchozích) vytváří silnější nepropojitelnost než 6-skokové obvody skrytých služeb Tor. Protože obě strany jsou interní, spojení se zcela vyhýbají úzkému hrdlu výstupních uzlů, což poskytuje rychlejší interní hosting a nativní integraci aplikací (I2PSnark, I2PTunnel, I2PBote).

---

## Architectural Takeaways

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Design Principle</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">I2P Advantage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Decentralization</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No trusted authorities; netDB managed by floodfill peers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Traffic Separation</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Unidirectional tunnels prevent request/response correlation</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Adaptability</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Packet-switching allows per-message load balancing</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Efficiency</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Garlic routing reduces metadata and increases throughput</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Inclusiveness</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">All peers route traffic, strengthening anonymity set</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Focus</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Built specifically for hidden services and in-network communication</td>
    </tr>
  </tbody>
</table>
---

## When to Use Each Network

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Use Case</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended Network</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Anonymous web browsing (clearnet access)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2P</strong></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Anonymous hosting, P2P, or DApps</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2P</strong></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Anonymous file publishing and storage</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Freenet (Hyphanet)</strong></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">VPN-style private routing with staking</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Lokinet</strong></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Academic experimentation and research</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>GNUnet</strong></td>
    </tr>
  </tbody>
</table>
---

## Summary

**Architektura I2P je unikátně zaměřena na soukromí**—žádné adresářové servery, žádné závislosti na blockchainu, žádná centralizovaná důvěra. Jeho kombinace **unidirectional tunnels (jednosměrných tunelů), packet-switched routingu (přepojování paketů), garlic message bundlingu (seskupování zpráv) a distribuovaného peer discovery (objevování uzlů)** z něj dělá technicky nejpokročilejší systém pro anonymní hosting a peer-to-peer komunikaci dnes.

> I2P není „alternativa k Toru." Jedná se o jinou třídu sítě – postavenou pro to, co se děje *uvnitř* privátní sítě, ne mimo ni.
