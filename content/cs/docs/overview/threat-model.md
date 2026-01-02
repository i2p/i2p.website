---
title: "Model hrozeb I2P"
description: "Katalog útoků zvažovaných v návrhu I2P a zavedená protiopatření"
slug: "threat-model"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "needs-review"
---

## 1. Co znamená „Anonymní"

I2P poskytuje *praktickou anonymitu*—nikoli neviditelnost. Anonymita je definována jako obtížnost pro protivníka zjistit informace, které si přejete udržet v soukromí: kdo jste, kde jste, nebo s kým komunikujete. Absolutní anonymita je nemožná; místo toho se I2P zaměřuje na **dostatečnou anonymitu** vůči globálním pasivním i aktivním protivníkům.

Vaše anonymita závisí na tom, jak nakonfigurujete I2P, jak si vyberete peery a odběry a jaké aplikace zpřístupníte.

---

## 2. Kryptografická a transportní evoluce (2003 → 2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Era</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Primary Algorithms</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.3 – 0.9</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ElGamal + AES-256 + DSA-SHA1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Legacy stack (2003–2015)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ed25519 signatures</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Replaced DSA</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.36 (2018)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NTCP2</strong> introduced</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise <em>XK_25519_ChaChaPoly_SHA256</em></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.56 (2022)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU2</strong> enabled by default</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise-based UDP transport</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.4.0 (2023)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NetDB Sub-DB isolation</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Prevents router↔client linkage</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.8.0+ (2025)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Congestion-aware routing / observability reductions</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DoS hardening</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0 (2025)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Post-quantum hybrid ML-KEM support (optional)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Experimental</td>
    </tr>
  </tbody>
</table>
**Současná kryptografická sada (Noise XK):** - **X25519** pro výměnu klíčů   - **ChaCha20/Poly1305 AEAD** pro šifrování   - **Ed25519 (EdDSA-SHA512)** pro podpisy   - **SHA-256** pro hashování a HKDF   - Volitelné **ML-KEM hybridy** pro testování post-kvantové kryptografie

Veškeré použití ElGamal a AES-CBC bylo vyřazeno. Transport je zcela založen na NTCP2 (TCP) a SSU2 (UDP); oba podporují IPv4/IPv6, forward secrecy a obfuskaci DPI.

---

## 3. Shrnutí síťové architektury

- **Mixnet s volnou trasou:** Odesílatelé a příjemci si každý definují vlastní tunnely.  
- **Žádná centrální autorita:** Směrování a pojmenování jsou decentralizované; každý router udržuje lokální důvěru.  
- **Jednosměrné tunnely:** Příchozí a odchozí jsou oddělené (životnost 10 minut).  
- **Explorační tunnely:** Standardně 2 přeskoky; klientské tunnely 2–3 přeskoky.  
- **Floodfill routery:** ~1 700 z ~55 000 uzlů (~6 %) udržuje distribuovanou NetDB.  
- **Rotace NetDB:** Klíčový prostor se rotuje denně o půlnoci UTC.  
- **Izolace sub-DB:** Od verze 2.4.0 používá každý klient a router samostatné databáze, aby se zabránilo propojení.

---

## 4. Kategorie útoků a současná obrana

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Category</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Current Status (2025)</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Primary Defenses</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Brute Force / Cryptanalysis</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Impractical with modern primitives (X25519, ChaCha20).</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Strong crypto, key rotation, Noise handshakes.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Timing Attacks</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Still unsolved for low-latency systems.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Unidirectional tunnels, 1024&nbsp;B cells, profile recalc (45&nbsp;s). Research continues for non-trivial delays (3.0+).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Intersection Attacks</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Inherent weakness of low latency mixnets.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel rotation (10&nbsp;min), leaseset expirations, multihoming.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Predecessor Attacks</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Partially mitigated.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tiered peer selection, strict XOR ordering, variable length tunnels.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Sybil Attacks</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No comprehensive defense.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">IP /16 limits, profiling, diversity rules; HashCash infra exists but not required.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Floodfill / NetDB Attacks</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Improved but still a concern.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">One /16 per lookup, limit 500 active, daily rotation, randomized verification delay, Sub-DB isolation.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>DoS / Flooding</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Frequent (esp. 2023 incidents).</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Congestion-aware routing (2.4+), aggressive leaseset removal (2.8+).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Traffic ID / Fingerprinting</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Greatly reduced.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise obfuscation, random padding, no plaintext headers.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Censorship / Partitioning</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Possible with state-level blocking.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Hidden mode, IPv6, multiple reseeds, mirrors.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Development / Supply Chain</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Mitigated.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Open source, signed SU3 releases (RSA-4096), multi-signer trust model.</td>
    </tr>
  </tbody>
</table>
---

## 5. Moderní síťová databáze (NetDB)

**Základní fakta (stále platná):** - Modifikované Kademlia DHT ukládá RouterInfo a LeaseSets.   - Hashování klíčů SHA-256; paralelní dotazy na 2 nejbližší floodfilly s timeoutem 10 s.   - Životnost LeaseSet ≈ 10 min (LeaseSet2) nebo 18 h (MetaLeaseSet).

**Nové typy (od verze 0.9.38):** - **LeaseSet2 (Typ 3)** – více typů šifrování, s časovým razítkem.   - **EncryptedLeaseSet2 (Typ 5)** – zastíněná destinace pro soukromé služby (autentizace DH nebo PSK).   - **MetaLeaseSet (Typ 7)** – multihoming a prodloužené doby platnosti.

**Významné bezpečnostní vylepšení – izolace Sub-DB (2.4.0):** - Zabraňuje asociaci router↔klient.   - Každý klient a router používá oddělené segmenty netDb.   - Ověřeno a auditováno (2.5.0).

---

## 6. Skrytý režim a omezené trasy

- **Skrytý režim:** Implementováno (automaticky v přísných zemích podle skóre Freedom House).  
    Routery nepublikují RouterInfo ani nesměrují provoz.  
- **Omezené trasy:** Částečně implementováno (pouze základní tunnely založené na důvěře).  
    Komplexní směrování důvěryhodných uzlů zůstává plánováno (3.0+).

Kompromis: Lepší soukromí ↔ snížený příspěvek k kapacitě sítě.

---

## 7. Útoky DoS a útoky na Floodfill

**Historické:** Výzkum UCSB z roku 2013 ukázal možnost Eclipse a Floodfill převzetí.   **Moderní obrana zahrnuje:** - Denní rotaci klíčového prostoru.   - Floodfill limit ≈ 500, jeden na /16.   - Randomizované zpoždění ověřování úložiště.   - Preference novějších routerů (2.6.0).   - Oprava automatického zařazení (2.9.0).   - Směrování vnímaní přetížení a omezování lease (2.4.0+).

Útoky na floodfill uzly zůstávají teoreticky možné, ale prakticky obtížnější.

---

## 8. Analýza provozu a cenzura

Provoz I2P je obtížné identifikovat: žádný pevný port, žádný handshake v čitelném textu a náhodné vyplnění. Pakety NTCP2 a SSU2 napodobují běžné protokoly a používají obfuskaci hlaviček ChaCha20. Strategie vyplňování jsou základní (náhodné velikosti), fiktivní provoz není implementován (nákladné). Připojení z výstupních uzlů Tor jsou od verze 2.6.0 blokována (na ochranu zdrojů).

---

## 9. Trvalá omezení (uznávaná)

- Korelace časování u aplikací s nízkou latencí zůstává základním rizikem.
- Průnikové útoky jsou stále účinné proti známým veřejným cílům.
- Sybil útoky postrádají úplnou ochranu (HashCash není vynucován).
- Konstantní tok dat a netriviální zpoždění zůstávají neimplementované (plánováno pro verzi 3.0).

Transparentnost ohledně těchto omezení je záměrná — brání uživatelům v přeceňování anonymity.

---

## 10. Statistiky sítě (2025)

- ~55 000 aktivních routerů po celém světě (↑ ze 7 000 v roce 2013)  
- ~1 700 floodfill routerů (~6 %)  
- 95 % se standardně účastní směrování tunelů  
- Úrovně šířky pásma: K (<12 KB/s) → X (>2 MB/s)  
- Minimální rychlost pro floodfill: 128 KB/s  
- Konzole routeru Java 8+ (vyžadováno), Java 17+ plánováno pro další cyklus

---

## 11. Vývoj a centrální zdroje

- Oficiální stránky: [geti2p.net](/)
- Dokumentace: [Documentation](/docs/)  
- Debian repositář: <https://deb.i2pgit.org> ( nahradil deb.i2p2.de v říjnu 2023 )  
- Zdrojový kód: <https://i2pgit.org/I2P_Developers/i2p.i2p> (Gitea) + GitHub mirror  
- Všechny vydání jsou podepsané SU3 kontejnery (RSA-4096, zzz/str4d klíče)  
- Žádné aktivní mailing listy; komunita přes <https://i2pforum.net> a IRC2P.  
- Cyklus aktualizací: 6–8 týdnů stabilní vydání.

---

## 12. Shrnutí vylepšení zabezpečení od verze 0.8.x

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Year</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Effect</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2015</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ed25519 signatures</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Removed SHA1/DSA weakness</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2018</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NTCP2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise-based TCP transport</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2019</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">LeaseSet2 / EncryptedLeaseSet2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Hidden services privacy</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2022</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SSU2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise-based UDP transport</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2023</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Sub-DB Isolation + Congestion-Aware Routing</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stopped NetDB linkage / improved resilience</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2024</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Floodfill selection improvements</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reduced long-term node influence</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2025</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Observability reductions + PQ hybrid crypto</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Harder timing analysis / future-proofing</td>
    </tr>
  </tbody>
</table>
---

## 13. Známé nevyřešené nebo plánované práce

- Komplexní omezené trasy (trusted-peer routing) → plánováno pro 3.0.  
- Netriviální zpoždění/dávkování pro odolnost proti časové analýze → plánováno pro 3.0.  
- Pokročilé vyplňování a fiktivní provoz → neimplementováno.  
- Ověření identity pomocí HashCash → infrastruktura existuje, ale je neaktivní.  
- Náhrada R5N DHT → pouze návrh.

---

## 14. Klíčové reference

- *Practical Attacks Against the I2P Network* (Egger et al., RAID 2013)  
- *Privacy Implications of Performance-Based Peer Selection* (Herrmann & Grothoff, PETS 2011)  
- *Resilience of the Invisible Internet Project* (Muntaka et al., Wiley 2025)  
- [Oficiální dokumentace I2P](/docs/)

---

## 15. Závěr

Základní model anonymity I2P obstál po dvě desetiletí: obětovat globální jedinečnost ve prospěch lokální důvěry a bezpečnosti. Od ElGamal po X25519, od NTCP po NTCP2 a od manuálních reseedů po izolaci Sub-DB se projekt vyvíjel při zachování své filozofie důkladné obrany a transparentnosti.

Mnoho útoků zůstává teoreticky možných proti jakékoli mixnet síti s nízkou latencí, ale průběžné zpevňování I2P je činí stále nepraktičtějšími. Síť je větší, rychlejší a bezpečnější než kdy dříve — a přesto stále upřímná ohledně svých limitů.
