---
title: "Modèle de menace I2P"
description: "Catalogue des attaques prises en compte dans la conception d'I2P et les mesures d'atténuation mises en place"
slug: "threat-model"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "needs-review"
---

## 1. Ce que signifie « Anonyme »

I2P fournit une *anonymat pratique*—pas l'invisibilité. L'anonymat est défini comme la difficulté pour un adversaire d'apprendre des informations que vous souhaitez garder privées : qui vous êtes, où vous êtes, ou à qui vous parlez. L'anonymat absolu est impossible ; à la place, I2P vise un **anonymat suffisant** face à des adversaires passifs et actifs globaux.

Votre anonymat dépend de la façon dont vous configurez I2P, de la manière dont vous choisissez vos pairs et vos abonnements, et des applications que vous exposez.

---

## 2. Évolution cryptographique et du transport (2003 → 2025)

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
**Suite cryptographique actuelle (Noise XK) :** - **X25519** pour l'échange de clés   - **ChaCha20/Poly1305 AEAD** pour le chiffrement   - **Ed25519 (EdDSA-SHA512)** pour les signatures   - **SHA-256** pour le hachage et HKDF   - **Hybrides ML-KEM** optionnels pour les tests post-quantiques

Toutes les utilisations d'ElGamal et d'AES-CBC ont été retirées. Le transport est entièrement NTCP2 (TCP) et SSU2 (UDP) ; les deux prennent en charge IPv4/IPv6, le secret de transmission (forward secrecy) et l'obscurcissement DPI.

---

## 3. Résumé de l'architecture réseau

- **Mixnet à routage libre :** Les émetteurs et les destinataires définissent chacun leurs propres tunnels.  
- **Aucune autorité centrale :** Le routage et le nommage sont décentralisés ; chaque router maintient une confiance locale.  
- **Tunnels unidirectionnels :** Les tunnels entrants et sortants sont séparés (durée de vie de 10 min).  
- **Tunnels exploratoires :** 2 sauts par défaut ; tunnels clients 2–3 sauts.  
- **Routeurs floodfill :** ~1 700 sur ~55 000 nœuds (~6 %) maintiennent la NetDB distribuée.  
- **Rotation NetDB :** L'espace de clés effectue une rotation quotidienne à minuit UTC.  
- **Isolation des sous-DB :** Depuis la version 2.4.0, chaque client et router utilisent des bases de données séparées pour éviter le lien.

---

## 4. Catégories d'attaques et défenses actuelles

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

## 5. Base de données réseau moderne (NetDB)

**Faits essentiels (toujours exacts) :** - DHT Kademlia modifiée stocke les RouterInfo et LeaseSets.   - Hachage de clé SHA-256 ; requêtes parallèles vers les 2 floodfills les plus proches avec délai d'attente de 10 s.   - Durée de vie des LeaseSet ≈ 10 min (LeaseSet2) ou 18 h (MetaLeaseSet).

**Nouveaux types (depuis 0.9.38) :** - **LeaseSet2 (Type 3)** – types de chiffrement multiples, horodaté.   - **EncryptedLeaseSet2 (Type 5)** – destination masquée pour services privés (authentification DH ou PSK).   - **MetaLeaseSet (Type 7)** – multihébergement et expirations étendues.

**Mise à niveau de sécurité majeure – Isolation Sub-DB (2.4.0) :** - Empêche l'association router↔client.   - Chaque client et router utilisent des segments netDb séparés.   - Vérifié et audité (2.5.0).

---

## 6. Mode caché et routes restreintes

- **Mode Caché :** Implémenté (automatique dans les pays strictes selon les scores Freedom House).  
    Les routeurs ne publient pas de RouterInfo et n'acheminent pas le trafic.  
- **Routes Restreintes :** Partiellement implémenté (tunnels de confiance basiques uniquement).  
    Le routage complet par pairs de confiance reste planifié (3.0+).

Compromis : Meilleure confidentialité ↔ contribution réduite à la capacité du réseau.

---

## 7. Attaques DoS et Floodfill

**Historique :** Une recherche de l'UCSB en 2013 a montré que les attaques Eclipse et la prise de contrôle des floodfills étaient possibles. **Les défenses modernes incluent :** - Rotation quotidienne de l'espace de clés. - Limite de floodfills ≈ 500, un par /16. - Délais de vérification de stockage aléatoires. - Préférence pour les routeurs plus récents (2.6.0). - Correction de l'inscription automatique (2.9.0). - Routage sensible à la congestion et limitation des baux (2.4.0+).

Les attaques floodfill restent théoriquement possibles mais pratiquement plus difficiles.

---

## 8. Analyse du trafic et censure

Le trafic I2P est difficile à identifier : pas de port fixe, pas de handshake en clair, et padding aléatoire. Les paquets NTCP2 et SSU2 imitent les protocoles courants et utilisent l'obfuscation d'en-tête ChaCha20. Les stratégies de padding sont basiques (tailles aléatoires), le trafic factice n'est pas implémenté (coûteux). Les connexions depuis les nœuds de sortie Tor sont bloquées depuis la version 2.6.0 (pour protéger les ressources).

---

## 9. Limitations persistantes (reconnues)

- La corrélation temporelle pour les applications à faible latence reste un risque fondamental.
- Les attaques par intersection restent puissantes contre les destinations publiques connues.
- Les attaques Sybil manquent de défense complète (HashCash non appliqué).
- Le trafic à débit constant et les délais non triviaux restent non implémentés (prévus pour la version 3.0).

La transparence concernant ces limites est intentionnelle — elle empêche les utilisateurs de surestimer l'anonymat.

---

## 10. Statistiques du réseau (2025)

- ~55 000 routeurs actifs dans le monde (↑ depuis 7 000 en 2013)  
- ~1 700 routeurs floodfill (~6 %)  
- 95 % participent au routage des tunnels par défaut  
- Niveaux de bande passante : K (<12 Ko/s) → X (>2 Mo/s)  
- Débit minimum floodfill : 128 Ko/s  
- Console du routeur Java 8+ (requis), Java 17+ prévu pour le prochain cycle

---

## 11. Développement et ressources centrales

- Site officiel : [geti2p.net](/)
- Docs : [Documentation](/docs/)  
- Dépôt Debian : <https://deb.i2pgit.org> ( a remplacé deb.i2p2.de en octobre 2023 )  
- Code source : <https://i2pgit.org/I2P_Developers/i2p.i2p> (Gitea) + miroir GitHub  
- Toutes les versions sont des conteneurs SU3 signés (RSA-4096, clés zzz/str4d)  
- Pas de listes de diffusion actives ; communauté via <https://i2pforum.net> et IRC2P.  
- Cycle de mise à jour : versions stables toutes les 6 à 8 semaines.

---

## 12. Résumé des améliorations de sécurité depuis la version 0.8.x

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

## 13. Travaux non résolus connus ou planifiés

- Routes restreintes complètes (routage par pairs de confiance) → prévu pour la version 3.0.  
- Délai/regroupement non trivial pour résistance au chronométrage → prévu pour la version 3.0.  
- Remplissage avancé et trafic factice → non implémenté.  
- Vérification d'identité HashCash → infrastructure existante mais inactive.  
- Remplacement DHT R5N → proposition uniquement.

---

## 14. Références clés

- *Practical Attacks Against the I2P Network* (Egger et al., RAID 2013)  
- *Privacy Implications of Performance-Based Peer Selection* (Herrmann & Grothoff, PETS 2011)  
- *Resilience of the Invisible Internet Project* (Muntaka et al., Wiley 2025)  
- [Documentation officielle I2P](/docs/)

---

## 15. Conclusion

Le modèle d'anonymat fondamental d'I2P perdure depuis deux décennies : sacrifier l'unicité globale au profit de la confiance locale et de la sécurité. D'ElGamal à X25519, de NTCP à NTCP2, et des réamorçages manuels à l'isolation Sub-DB, le projet a évolué tout en maintenant sa philosophie de défense en profondeur et de transparence.

De nombreuses attaques restent théoriquement possibles contre tout mixnet à faible latence, mais le renforcement continu d'I2P les rend de plus en plus impraticables. Le réseau est plus grand, plus rapide et plus sécurisé que jamais — tout en restant honnête sur ses limites.
