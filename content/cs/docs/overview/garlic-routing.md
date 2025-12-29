---
title: "Garlic Routing"
description: "Porozumění terminologii garlic routing, architektuře a moderní implementaci v I2P"
slug: "garlic-routing"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

---

## 1. Přehled

**Garlic routing** (česneková směrování) zůstává jednou ze základních inovací I2P, kombinující vrstvené šifrování, sdružování zpráv a jednosměrné tunely. I když je koncepčně podobný **cibulové směrování** (onion routing), rozšiřuje tento model tak, že sdružuje více šifrovaných zpráv („cloves" – stroužky) do jediné obálky („garlic" – česnek), čímž zlepšuje efektivitu a anonymitu.

Termín *garlic routing* (česneková směrování) byl vytvořen [Michaelem J. Freedmanem](https://www.cs.princeton.edu/~mfreed/) v [diplomové práci Rogera Dingledina Free Haven](https://www.freehaven.net/papers.html) (červen 2000, §8.1.1). Vývojáři I2P přijali tento termín na začátku 2000. let, aby vyjádřili jeho vylepšení sdružování zpráv a jednosměrný transportní model, který ho odlišuje od architektury s přepínáním okruhů v síti Tor.

> **Shrnutí:** Garlic routing = vrstvené šifrování + sdružování zpráv + anonymní doručování prostřednictvím jednosměrných tunelů.

---

## 2. Terminologie „Garlic"

Historicky byl termín *garlic* používán ve třech různých kontextech v rámci I2P:

1. **Vrstvené šifrování** – ochrana ve stylu onion na úrovni tunelu  
2. **Sdružování více zpráv** – více "cloves" uvnitř "garlic message"  
3. **End‑to‑end šifrování** – dříve *ElGamal/AES+SessionTags*, nyní *ECIES‑X25519‑AEAD‑Ratchet*

Zatímco architektura zůstává nedotčena, šifrovací schéma bylo zcela modernizováno.

---

## 3. Vrstvené šifrování

Garlic routing sdílí svůj základní princip s onion routingem: každý router dešifruje pouze jednu vrstvu šifrování a dozví se pouze další hop, nikoli celou cestu.

Nicméně I2P implementuje **jednosměrné tunely**, nikoli obousměrné okruhy:

- **Odchozí tunel**: odesílá zprávy pryč od tvůrce  
- **Příchozí tunel**: přenáší zprávy zpět k tvůrci

Celá cesta tam i zpět (Alice ↔ Bob) využívá čtyři tunnely: odchozí Alice → příchozí Bob, poté odchozí Bob → příchozí Alice. Tento design **snižuje odhalení korelačních dat na polovinu** ve srovnání s obousměrnými okruhy.

Pro podrobnosti implementace tunelů viz [specifikace tunelů](/docs/specs/implementation) a specifikace [vytváření tunelů (ECIES)](/docs/specs/implementation).

---

## 4. Sdružování více zpráv („Cloves")

Freedmanova původní koncepce garlic routing předpokládala spojení více zašifrovaných "bulbů" do jedné zprávy. I2P to implementuje jako **cloves** (hřebíčky) uvnitř **garlic message** (česneková zpráva) — každý clove má své vlastní zašifrované instrukce pro doručení a cíl (router, destination nebo tunnel).

Garlic bundling umožňuje I2P:

- Kombinovat potvrzení a metadata s datovými zprávami
- Snížit pozorovatelné vzory provozu
- Podporovat komplexní struktury zpráv bez dodatečných spojení

![Garlic Message Cloves](/images/garliccloves.png)   *Obrázek 1: Garlic Message obsahující několik cloves, každý s vlastními pokyny pro doručení.*

Typické hřebíčky zahrnují:

1. **Zpráva o stavu doručení** — potvrzení úspěšného nebo neúspěšného doručení.  
   Tyto zprávy jsou zabaleny do vlastní garlic vrstvy pro zachování důvěrnosti.
2. **Zpráva Database Store** — automaticky přibalené LeaseSets, aby protějšky mohly odpovědět bez opětovného dotazování netDb.

Hřebíčky se sdružují, když:

- Musí být publikován nový LeaseSet  
- Jsou doručeny nové session tagy  
- V poslední době nedošlo k žádnému bundlování (~1 minuta ve výchozím nastavení)

Garlic zprávy dosahují efektivního end-to-end doručení více šifrovaných komponent v jediném paketu.

---

## 5. Vývoj šifrování

### 5.1 Historical Context

Raná dokumentace (≤ v0.9.12) popisovala šifrování *ElGamal/AES+SessionTags*:   - **ElGamal 2048‑bit** obalující AES session keys   - **AES‑256/CBC** pro šifrování datové části   - 32‑bajtové session tags použité jednou na zprávu

Tento kryptosystém je **zastaralý**.

### 5.2 ECIES‑X25519‑AEAD‑Ratchet (Current Standard)

Mezi lety 2019 a 2023 I2P kompletně přešel na ECIES‑X25519‑AEAD‑Ratchet. Moderní stack standardizuje následující komponenty:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Layer</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">ECIES Primitive or Concept</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Transport Layer (NTCP2, SSU2)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise_NX → X25519, ChaCha20/Poly1305, BLAKE2s</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2NP Delivery</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECIES‑X25519‑AEAD (ChaCha20/Poly1305)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Session Management</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ratchet with rekey records, per-clove key material</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline Authentication</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA (Ed25519) with LeaseSet2/MetaLeaseSet chains</td>
    </tr>
  </tbody>
</table>
Výhody migrace na ECIES:

- **Forward secrecy** prostřednictvím per-message ratcheting keys  
- **Zmenšená velikost datové části** ve srovnání s ElGamal  
- **Odolnost** proti pokrokům v kryptoanalýze  
- **Kompatibilita** s budoucími post-quantum hybridy (viz Proposal 169)

Další podrobnosti: viz [specifikace ECIES](/docs/specs/ecies) a [specifikace EncryptedLeaseSet](/docs/specs/encryptedleaseset).

---

## 6. LeaseSets and Garlic Bundling

Garlic obálky často zahrnují LeaseSets pro publikování nebo aktualizaci dosažitelnosti cílového místa.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Key Capabilities</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Distribution Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">LeaseSet (legacy)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Single encryption/signature pair</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Accepted for backward compatibility</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">LeaseSet2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Multiple crypto suites, offline signing keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default for modern routers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EncryptedLeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Access-controlled, destination hidden from floodfill</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Requires shared decryption key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MetaLeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Aggregates multiple destinations or multi-homed services</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Extends LeaseSet2 fields recursively</td>
    </tr>
  </tbody>
</table>
Všechny LeaseSety jsou distribuovány prostřednictvím *floodfill DHT* spravované specializovanými routery. Publikace jsou ověřovány, opatřovány časovými razítky a omezovány frekvencí, aby se snížila korelace metadat.

Viz [dokumentace Network Database](/docs/specs/common-structures) pro podrobnosti.

---

## 7. Modern “Garlic” Applications within I2P

Garlic encryption a seskupování zpráv jsou používány v celém protokolovém stacku I2P:

1. **Vytváření a využívání tunelů** — vrstvené šifrování na každém skoku  
2. **Doručování zpráv mezi koncovými body** — seskupené garlic zprávy s klonem potvrzení a LeaseSet cloves  
3. **Publikování v síťové databázi** — LeaseSety zabalené v garlic obálkách pro ochranu soukromí  
4. **Transporty SSU2 a NTCP2** — podkladové šifrování pomocí frameworku Noise a primitiv X25519/ChaCha20

Garlic routing je tedy jak *metoda vrstvení šifrování*, tak *model síťového zasílání zpráv*.

---

## 6. LeaseSets a sdružování Garlic

Centrum dokumentace I2P je [dostupné zde](/docs/), průběžně udržované. Relevantní živé specifikace zahrnují:

- [Specifikace ECIES](/docs/specs/ecies) — ECIES‑X25519‑AEAD‑Ratchet
- [Vytváření tunelů (ECIES)](/docs/specs/implementation) — moderní protokol pro vytváření tunelů
- [Specifikace I2NP](/docs/specs/i2np) — formáty zpráv I2NP
- [Specifikace SSU2](/docs/specs/ssu2) — transportní protokol SSU2 UDP
- [Společné struktury](/docs/specs/common-structures) — chování netDb a floodfill

Akademické ověření: Hoang et al. (IMC 2018, USENIX FOCI 2019) a Muntaka et al. (2025) potvrzují architektonickou stabilitu a provozní odolnost designu I2P.

---

## 7. Moderní aplikace "Garlic" v rámci I2P

Probíhající návrhy:

- **Návrh 169:** Hybridní post-kvantová (ML-KEM 512/768/1024 + X25519)  
- **Návrh 168:** Optimalizace šířky pásma pro transport  
- **Aktualizace datagramů a streamingu:** Vylepšená správa přetížení

Budoucí adaptace mohou zahrnovat dodatečné strategie zpoždění zpráv nebo redundanci více tunelů na úrovni garlic zpráv, navazující na nevyužité možnosti doručení původně popsané Freedmanem.

---

## 8. Aktuální dokumentace a odkazy

- Freedman, M. J. & Dingledine, R. (2000). *Free Haven Master's Thesis,* § 8.1.1. [Free Haven Papers](https://www.freehaven.net/papers.html)  
- [Onion Router Publications](https://www.onion-router.net/Publications.html)  
- [Garlic Routing (Wikipedia)](https://en.wikipedia.org/wiki/Garlic_routing)  
- [Tor Project](https://www.torproject.org/)  
- [Free Haven Anonbib](https://freehaven.net/anonbib/topic.html)  
- Goldschlag, D. M., Reed, M. G., Syverson, P. F. (1996). *Hiding Routing Information.* NRL Publication.

---
