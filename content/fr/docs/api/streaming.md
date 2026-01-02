---
title: "Protocole de streaming"
description: "Transport de type TCP utilisé par la plupart des applications I2P"
slug: "streaming"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Aperçu

La **I2P Streaming Library** fournit un transport fiable, ordonné et authentifié sur la couche de messages I2P, similaire à **TCP sur IP**. Elle se situe au-dessus du [protocole I2CP](/docs/specs/i2cp/) et est utilisée par presque toutes les applications I2P interactives, notamment les proxies HTTP, IRC, BitTorrent et le courrier électronique.

### Caractéristiques principales

- Établissement de connexion en une phase utilisant les drapeaux **SYN**, **ACK** et **FIN** qui peuvent être regroupés avec les données de charge utile pour réduire les allers-retours.
- **Contrôle de congestion à fenêtre glissante**, avec démarrage lent et évitement de congestion ajustés pour l'environnement à haute latence d'I2P.
- Compression de paquets (segments compressés de 4 Ko par défaut) équilibrant le coût de retransmission et la latence de fragmentation.
- Abstraction de canal entièrement **authentifié, chiffré** et **fiable** entre les destinations I2P.

Cette conception permet aux petites requêtes et réponses HTTP de se terminer en un seul aller-retour. Un paquet SYN peut transporter la charge utile de la requête, tandis que le SYN/ACK/FIN du répondeur peut contenir le corps complet de la réponse.

---

## Notions de base de l'API

L'API de streaming Java reflète la programmation socket standard de Java :

```java
I2PSocketManager mgr = I2PSocketManagerFactory.createManager(host, port, options);
I2PSocket socket       = mgr.connect(destination);
I2PServerSocket server = mgr.getServerSocket();
```
- `I2PSocketManagerFactory` négocie ou réutilise une session router via I2CP.
- Si aucune clé n'est fournie, une nouvelle destination est automatiquement générée.
- Les développeurs peuvent transmettre des options I2CP (par exemple, longueurs de tunnel, types de chiffrement ou paramètres de connexion) via la map `options`.
- `I2PSocket` et `I2PServerSocket` reflètent les interfaces Java `Socket` standard, rendant la migration simple.

La documentation Javadocs complète est disponible depuis la console du routeur I2P ou [ici](/docs/specs/streaming/).

---

## Configuration et Réglage

Vous pouvez passer des propriétés de configuration lors de la création d'un gestionnaire de socket via :

```java
I2PSocketManagerFactory.createManager(host, port, properties);
```
### Options de clés

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
### Comportement par charge de travail

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
Les nouvelles fonctionnalités depuis la version 0.9.4 incluent la suppression des journaux de rejet, la prise en charge des listes DSA (0.9.21) et l'application obligatoire du protocole (0.9.36). Les routeurs depuis la version 2.10.0 incluent le chiffrement hybride post-quantique (ML-KEM + X25519) au niveau de la couche transport.

---

## Détails du protocole

Chaque flux est identifié par un **Stream ID**. Les paquets transportent des drapeaux de contrôle similaires à TCP : `SYNCHRONIZE`, `ACK`, `FIN`, et `RESET`. Les paquets peuvent contenir à la fois des données et des drapeaux de contrôle simultanément, améliorant l'efficacité pour les connexions de courte durée.

### Cycle de vie de la connexion

1. **SYN envoyé** — l'initiateur inclut des données optionnelles.  
2. **Réponse SYN/ACK** — le répondeur inclut des données optionnelles.  
3. **Finalisation ACK** — établit la fiabilité et l'état de session.  
4. **FIN/RESET** — utilisé pour une fermeture ordonnée ou une terminaison abrupte.

### Fragmentation et réordonnancement

Étant donné que les tunnels I2P introduisent de la latence et un réordonnancement des messages, la bibliothèque met en mémoire tampon les paquets provenant de flux inconnus ou arrivant prématurément. Les messages mis en mémoire tampon sont stockés jusqu'à ce que la synchronisation soit terminée, garantissant ainsi une livraison complète et ordonnée.

### Application du protocole

L'option `i2p.streaming.enforceProtocol=true` (par défaut depuis la version 0.9.36) garantit que les connexions utilisent le numéro de protocole I2CP correct, évitant ainsi les conflits entre plusieurs sous-systèmes partageant une même destination.

---

## Interopérabilité et bonnes pratiques

Le protocole de streaming coexiste avec l'**API Datagram**, donnant aux développeurs le choix entre des transports orientés connexion et sans connexion.

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
### Clients Partagés

Les applications peuvent réutiliser des tunnels existants en fonctionnant comme **clients partagés**, permettant à plusieurs services de partager la même destination. Bien que cela réduise la charge système, cela augmente le risque de corrélation entre services—à utiliser avec précaution.

### Contrôle de congestion

- La couche de streaming s'adapte en continu à la latence réseau et au débit via un retour d'information basé sur le RTT.
- Les applications fonctionnent mieux lorsque les routeurs sont des pairs contributeurs (tunnels participants activés).
- Les mécanismes de contrôle de congestion de type TCP empêchent la surcharge des pairs lents et aident à équilibrer l'utilisation de la bande passante entre les tunnels.

### Considérations de latence

Comme I2P ajoute plusieurs centaines de millisecondes de latence de base, les applications devraient minimiser les allers-retours. Regrouper les données avec l'établissement de connexion lorsque c'est possible (par exemple, requêtes HTTP dans SYN). Éviter les conceptions reposant sur de nombreux petits échanges séquentiels.

---

## Tests et Compatibilité

- Testez toujours avec **Java I2P** et **i2pd** pour garantir une compatibilité totale.  
- Bien que le protocole soit normalisé, des différences mineures d'implémentation peuvent exister.  
- Gérez les anciens routers avec souplesse—de nombreux pairs exécutent encore des versions antérieures à la 2.0.  
- Surveillez les statistiques de connexion en utilisant `I2PSocket.getOptions()` et `getSession()` pour lire les métriques de RTT et de retransmission.

Les performances dépendent fortement de la configuration des tunnels : - **Tunnels courts (1–2 sauts)** → latence plus faible, anonymat réduit. - **Tunnels longs (3+ sauts)** → anonymat accru, RTT augmenté.

---

## Améliorations clés (2.0.0–2.10.0)

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

## Résumé

La **bibliothèque I2P Streaming** est l'épine dorsale de toutes les communications fiables au sein d'I2P. Elle garantit la livraison de messages ordonnés, authentifiés et chiffrés, et fournit un remplacement quasi transparent pour TCP dans les environnements anonymes.

Pour obtenir des performances optimales : - Minimisez les allers-retours en regroupant SYN+payload.   - Ajustez les paramètres de fenêtre et de délai d'expiration selon votre charge de travail.   - Privilégiez des tunnels plus courts pour les applications sensibles à la latence.   - Utilisez des conceptions respectueuses de la congestion pour éviter de surcharger les pairs.
