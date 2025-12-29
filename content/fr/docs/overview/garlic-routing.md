---
title: "Routage en bulbe d'ail (Garlic Routing)"
description: "Comprendre la terminologie, l'architecture et l'implémentation moderne du routage en ail (garlic routing) dans I2P"
slug: "garlic-routing"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

---

## 1. Aperçu général

Le **garlic routing** reste l'une des innovations fondamentales d'I2P, combinant le chiffrement en couches, le regroupement de messages et les tunnels unidirectionnels. Bien que conceptuellement similaire au **onion routing**, il étend le modèle en regroupant plusieurs messages chiffrés ("cloves") dans une seule enveloppe ("garlic"), améliorant l'efficacité et l'anonymat.

Le terme *garlic routing* a été inventé par [Michael J. Freedman](https://www.cs.princeton.edu/~mfreed/) dans [la thèse de Master de Roger Dingledine sur Free Haven](https://www.freehaven.net/papers.html) (juin 2000, §8.1.1). Les développeurs I2P ont adopté ce terme au début des années 2000 pour refléter ses améliorations en matière de regroupement et son modèle de transport unidirectionnel, le distinguant de la conception à commutation de circuits de Tor.

> **Résumé :** Garlic routing = chiffrement en couches + regroupement de messages + livraison anonyme via des tunnels unidirectionnels.

---

## 2. La terminologie "Garlic"

Historiquement, le terme *garlic* a été utilisé dans trois contextes différents au sein d'I2P :

1. **Chiffrement en couches** – protection de style onion au niveau du tunnel  
2. **Regroupement de plusieurs messages** – plusieurs « cloves » à l'intérieur d'un « garlic message »  
3. **Chiffrement de bout en bout** – anciennement *ElGamal/AES+SessionTags*, maintenant *ECIES‑X25519‑AEAD‑Ratchet*

Bien que l'architecture reste intacte, le schéma de chiffrement a été complètement modernisé.

---

## 3. Chiffrement en couches

Le routage garlic partage son principe fondamental avec le routage en oignon : chaque routeur ne déchiffre qu'une seule couche de chiffrement, ne connaissant que le prochain saut et non le chemin complet.

Cependant, I2P implémente des **tunnels unidirectionnels**, et non des circuits bidirectionnels :

- **Tunnel sortant** : envoie des messages à partir du créateur  
- **Tunnel entrant** : transporte les messages vers le créateur

Un aller-retour complet (Alice ↔ Bob) utilise quatre tunnels : outbound d'Alice → inbound de Bob, puis outbound de Bob → inbound d'Alice. Cette conception **réduit de moitié l'exposition des données de corrélation** par rapport aux circuits bidirectionnels.

Pour les détails d'implémentation des tunnels, voir la [Spécification des Tunnels](/docs/specs/implementation) et la spécification [Création de Tunnel (ECIES)](/docs/specs/implementation).

---

## 4. Regroupement de plusieurs messages (les "Cloves")

Le garlic routing original de Freedman envisageait de regrouper plusieurs « bulbes » chiffrés au sein d'un seul message. I2P implémente cela sous forme de **cloves** (gousses) à l'intérieur d'un **garlic message** — chaque clove possède ses propres instructions de livraison chiffrées et sa cible (router, destination ou tunnel).

Le regroupement en garlic permet à I2P de :

- Combiner les accusés de réception et les métadonnées avec les messages de données
- Réduire les modèles de trafic observables
- Prendre en charge des structures de messages complexes sans connexions supplémentaires

![Garlic Message Cloves](/images/garliccloves.png)   *Figure 1 : Un Garlic Message contenant plusieurs cloves, chacun avec ses propres instructions de livraison.*

Les clous de girofle typiques incluent :

1. **Message de statut de livraison** — accusés de réception confirmant le succès ou l'échec de la livraison.  
   Ceux-ci sont enveloppés dans leur propre couche garlic pour préserver la confidentialité.
2. **Message Database Store** — LeaseSets regroupés automatiquement afin que les pairs puissent répondre sans interroger à nouveau le netDb.

Les cloves sont regroupés lorsque :

- Un nouveau LeaseSet doit être publié
- De nouvelles balises de session sont livrées
- Aucun regroupement n'a eu lieu récemment (~1 minute par défaut)

Les messages garlic permettent une livraison de bout en bout efficace de plusieurs composants chiffrés dans un seul paquet.

---

## 5. Évolution du chiffrement

### 5.1 Historical Context

La documentation ancienne (≤ v0.9.12) décrivait le chiffrement *ElGamal/AES+SessionTags* :   - **ElGamal 2048 bits** encapsulant les clés de session AES   - **AES‑256/CBC** pour le chiffrement de la charge utile   - Balises de session de 32 octets utilisées une fois par message

Ce système cryptographique est **obsolète**.

### 5.2 ECIES‑X25519‑AEAD‑Ratchet (Current Standard)

Entre 2019 et 2023, I2P a migré entièrement vers ECIES‑X25519‑AEAD‑Ratchet. La pile moderne standardise les composants suivants :

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
Avantages de la migration ECIES :

- **Confidentialité persistante** via des clés de ratchet par message  
- **Taille de charge utile réduite** par rapport à ElGamal  
- **Résilience** contre les avancées cryptanalytiques  
- **Compatibilité** avec les futurs hybrides post-quantiques (voir Proposition 169)

Détails supplémentaires : voir la [spécification ECIES](/docs/specs/ecies) et la [spécification EncryptedLeaseSet](/docs/specs/encryptedleaseset).

---

## 6. LeaseSets and Garlic Bundling

Les enveloppes garlic incluent fréquemment des leaseSets pour publier ou mettre à jour l'accessibilité des destinations.

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
Tous les LeaseSets sont distribués via la *floodfill DHT* maintenue par des routeurs spécialisés. Les publications sont vérifiées, horodatées et limitées en débit pour réduire la corrélation des métadonnées.

Voir la [documentation de la base de données réseau](/docs/specs/common-structures) pour plus de détails.

---

## 7. Modern “Garlic” Applications within I2P

Le chiffrement basé sur garlic encryption et le regroupement de messages sont utilisés dans toute la pile de protocoles I2P :

1. **Création et utilisation de tunnels** — chiffrement en couches par saut  
2. **Livraison de messages de bout en bout** — messages garlic groupés avec accusés de réception clonés et cloves LeaseSet  
3. **Publication dans la Network Database** — LeaseSets encapsulés dans des enveloppes garlic pour la confidentialité  
4. **Transports SSU2 et NTCP2** — chiffrement de sous-couche utilisant le framework Noise et les primitives X25519/ChaCha20

Le garlic routing est donc à la fois une *méthode de chiffrement en couches* et un *modèle de messagerie réseau*.

---

## 6. LeaseSets et Garlic Bundling

Le centre de documentation d'I2P est [disponible ici](/docs/), maintenu en continu. Les spécifications pertinentes incluent :

- [Spécification ECIES](/docs/specs/ecies) — ECIES‑X25519‑AEAD‑Ratchet
- [Création de tunnel (ECIES)](/docs/specs/implementation) — protocole moderne de construction de tunnel
- [Spécification I2NP](/docs/specs/i2np) — formats de message I2NP
- [Spécification SSU2](/docs/specs/ssu2) — transport UDP SSU2
- [Structures communes](/docs/specs/common-structures) — comportement netDb et floodfill

Validation académique : Hoang et al. (IMC 2018, USENIX FOCI 2019) et Muntaka et al. (2025) confirment la stabilité architecturale et la résilience opérationnelle de la conception d'I2P.

---

## 7. Applications « Garlic » modernes au sein d'I2P

Propositions en cours :

- **Proposition 169 :** Hybride post-quantique (ML-KEM 512/768/1024 + X25519)  
- **Proposition 168 :** Optimisation de la bande passante du transport  
- **Mises à jour datagramme et streaming :** Gestion améliorée de la congestion

Les adaptations futures pourraient inclure des stratégies supplémentaires de délai de message ou une redondance multi-tunnel au niveau du garlic-message, en s'appuyant sur des options de livraison inutilisées décrites à l'origine par Freedman.

---

## 8. Documentation actuelle et références

- Freedman, M. J. & Dingledine, R. (2000). *Free Haven Master's Thesis,* § 8.1.1. [Free Haven Papers](https://www.freehaven.net/papers.html)  
- [Onion Router Publications](https://www.onion-router.net/Publications.html)  
- [Garlic Routing (Wikipedia)](https://en.wikipedia.org/wiki/Garlic_routing)  
- [Tor Project](https://www.torproject.org/)  
- [Free Haven Anonbib](https://freehaven.net/anonbib/topic.html)  
- Goldschlag, D. M., Reed, M. G., Syverson, P. F. (1996). *Hiding Routing Information.* NRL Publication.

---
