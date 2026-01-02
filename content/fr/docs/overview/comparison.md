---
title: "I2P vs autres réseaux de confidentialité"
description: "Une comparaison technique et philosophique moderne mettant en avant les avantages uniques de conception d'I2P"
slug: "comparison"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Aperçu

Plusieurs grands réseaux de confidentialité et d'anonymat existent aujourd'hui, chacun avec des objectifs de conception et des modèles de menace différents. Bien que Tor, Lokinet, GNUnet et Freenet apportent tous des approches précieuses pour les communications préservant la vie privée, **I2P se distingue comme le seul réseau à commutation de paquets prêt pour la production, entièrement optimisé pour les services cachés dans le réseau et les applications pair-à-pair.**

Le tableau ci-dessous résume les principales distinctions architecturales et opérationnelles entre ces réseaux en 2025.

---

## Comparaison des Réseaux de Confidentialité (2025)

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

## Pourquoi I2P est leader en matière de conception axée sur la confidentialité

### 1. **Packet Switching > Circuit Switching**

Le modèle à commutation de circuits de Tor lie le trafic à des chemins fixes de trois sauts—efficace pour la navigation, mais fragile pour les services internes de longue durée. Les **tunnels à commutation de paquets** d'I2P envoient les messages à travers plusieurs chemins simultanés, contournant automatiquement la congestion ou les pannes pour une meilleure disponibilité et répartition de charge.

### 2. **Unidirectional Tunnels**

I2P sépare le trafic entrant et sortant. Cela signifie que chaque participant ne voit jamais que **la moitié** d'un flux de communication, rendant les attaques de corrélation temporelle considérablement plus difficiles. Tor, Lokinet et autres utilisent des circuits bidirectionnels où les requêtes et réponses partagent le même chemin—plus simple, mais plus traçable.

### 3. **Fully Distributed netDB**

Les neuf autorités de répertoire de Tor définissent sa topologie réseau. I2P utilise une **DHT Kademlia** auto-organisée maintenue par des routeurs floodfill rotatifs, éliminant tout point de contrôle central ou serveur de coordination.

### 1. **Commutation de paquets > Commutation de circuits**

I2P étend le routage en oignon avec le **garlic routing** (routage en ail), regroupant plusieurs messages chiffrés dans un seul conteneur. Cela réduit la fuite de métadonnées et la surcharge de bande passante tout en améliorant l'efficacité pour les messages d'accusé de réception, de données et de contrôle.

### 2. **Tunnels unidirectionnels**

Chaque routeur I2P achemine du trafic pour les autres. Il n'existe pas d'opérateurs de relais dédiés ni de nœuds privilégiés : la bande passante et la fiabilité déterminent automatiquement la quantité de routage qu'un nœud contribue. Cette approche démocratique renforce la résilience et s'adapte naturellement à mesure que le réseau se développe.

### 3. **netDB entièrement distribué**

L'aller-retour de 12 sauts d'I2P (6 entrants + 6 sortants) crée une déliaison plus forte que les circuits de service caché à 6 sauts de Tor. Parce que les deux parties sont internes, les connexions évitent complètement le goulot d'étranglement de sortie, offrant un hébergement interne plus rapide et une intégration native des applications (I2PSnark, I2PTunnel, I2PBote).

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

**L'architecture d'I2P est unique, privilégiant la confidentialité avant tout**—pas de serveurs d'annuaire, pas de dépendances blockchain, pas de confiance centralisée. Sa combinaison de **tunnels unidirectionnels, routage à commutation de paquets, regroupement de messages garlic et découverte distribuée de pairs** en fait le système techniquement le plus avancé pour l'hébergement anonyme et la communication pair-à-pair aujourd'hui.

> I2P n'est pas « une alternative à Tor ». C'est une classe de réseau différente — conçue pour ce qui se passe *à l'intérieur* du réseau de confidentialité, et non à l'extérieur.
