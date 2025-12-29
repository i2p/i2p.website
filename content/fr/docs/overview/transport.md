---
title: "Couche de transport"
description: "Comprendre la couche de transport d'I2P - méthodes de communication point à point entre routers, y compris NTCP2 et SSU2"
slug: "transport"
lastUpdated: "2025-03"
accurateFor: "2.10.0"
---

---

## 1. Vue d'ensemble

Un **transport** dans I2P est une méthode de communication directe, point à point, entre routers. Ces mécanismes assurent la confidentialité et l'intégrité tout en vérifiant l'authentification des routers.

Chaque transport fonctionne selon des modèles de connexion intégrant l’authentification, le contrôle de flux, des accusés de réception et des fonctionnalités de retransmission.

---

## 2. Transports actuels

I2P prend actuellement en charge deux transports principaux :

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Transport</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NTCP2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TCP</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise-based TCP transport with modern encryption (as of 0.9.36)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UDP</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Secure Semireliable UDP with modern encryption (as of 0.9.56)</td>
    </tr>
  </tbody>
</table>
### 2.1 Transports hérités (dépréciés)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Transport</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NTCP</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TCP</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Replaced by NTCP2; removed in 0.9.62</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UDP</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Replaced by SSU2; removed in 0.9.62</td>
    </tr>
  </tbody>
</table>
---

## 3. Services de transport

Le sous-système de transport fournit les services suivants :

### 3.1 Acheminement des messages

- Acheminement fiable des messages [I2NP](/docs/specs/i2np/) (les transports gèrent exclusivement la messagerie I2NP)
- La livraison dans l'ordre n'est **PAS** garantie universellement
- Mise en file d'attente des messages basée sur les priorités

### 3.2 Gestion des connexions

- Établissement et fermeture des connexions
- Gestion des limites de connexion avec application des seuils
- Suivi de l’état pour chaque pair
- Application automatique et manuelle de la liste de bannissement des pairs

### 3.3 Configuration du réseau

- Plusieurs adresses de router par transport (prise en charge IPv4 et IPv6 depuis la v0.9.8)
- Ouverture des ports du pare-feu via UPnP
- Prise en charge de la traversée NAT/pare-feu
- Détection de l’adresse IP locale via plusieurs méthodes

### 3.4 Sécurité

- Chiffrement des échanges point à point
- Validation des adresses IP selon les règles locales
- Détermination du consensus horaire (repli NTP)

### 3.5 Gestion de la bande passante

- Limites de bande passante entrante et sortante
- Sélection optimale du transport pour les messages sortants

---

## 4. Adresses de transport

Le sous-système tient à jour la liste des points de contact du router:

- Méthode de transport (NTCP2, SSU2)
- Adresse IP
- Numéro de port
- Paramètres optionnels

Plusieurs adresses par méthode de transport sont possibles.

### 4.1 Configurations d'adresses courantes

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Configuration</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Hidden</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Routers with no published addresses</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Firewalled</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Routers publishing SSU2 addresses with "introducer" peer lists for NAT traversal</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Unrestricted</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Routers advertising both NTCP2 and SSU2 addresses on IPv4 and/or IPv6</td>
    </tr>
  </tbody>
</table>
---

## 5. Sélection du transport

Le système sélectionne les transports pour les [messages I2NP](/docs/specs/i2np/) indépendamment des protocoles de couche supérieure. La sélection utilise un **système d’enchères** dans lequel chaque transport soumet des offres, la valeur la plus basse l’emportant.

### 5.1 Facteurs de détermination des offres

- Paramètres des préférences de transport
- Connexions aux pairs existantes
- Nombres de connexions actuels par rapport aux seuils
- Historique récent des tentatives de connexion
- Contraintes de taille des messages
- Capacités de transport du RouterInfo du pair
- Directivité de la connexion (directe versus dépendante d’un introducer (nœud d’introduction))
- Préférences de transport annoncées par le pair

En général, deux routers maintiennent simultanément des connexions à transport unique, bien que des connexions multi-transport simultanées soient possibles.

---

## 6. NTCP2

**NTCP2** (New Transport Protocol 2) est le protocole de transport moderne basé sur TCP pour I2P, introduit dans la version 0.9.36.

### 6.1 Fonctionnalités clés

- Basé sur le **Noise Protocol Framework** (modèle Noise_XK)
- Utilise **X25519** pour l’échange de clés
- Utilise **ChaCha20/Poly1305** pour le chiffrement authentifié
- Utilise **BLAKE2s** pour le hachage
- Obfuscation du protocole pour résister à l’inspection approfondie des paquets (DPI)
- Remplissage optionnel pour résister à l’analyse du trafic

### 6.2 Établissement de la connexion

1. **Requête de session** (Alice → Bob): Clé X25519 éphémère + charge utile chiffrée
2. **Session créée** (Bob → Alice): Clé éphémère + confirmation chiffrée
3. **Session confirmée** (Alice → Bob): Poignée de main finale avec RouterInfo (informations du router)

Toutes les données suivantes sont chiffrées avec des clés de session dérivées du handshake (phase d'initialisation).

Voir la [spécification NTCP2](/docs/specs/ntcp2/) pour tous les détails.

---

## 7. SSU2

**SSU2** (Secure Semireliable UDP 2, protocole UDP semi-fiable sécurisé) est le transport moderne basé sur UDP pour I2P, introduit dans la version 0.9.56.

### 7.1 Fonctionnalités clés

- Basé sur le **Noise Protocol Framework** (modèle Noise_XK)
- Utilise **X25519** pour l'échange de clés
- Utilise **ChaCha20/Poly1305** pour le chiffrement authentifié
- Remise semi-fiable avec accusés de réception sélectifs
- Traversée de NAT via hole punching (perforation de NAT) et relais/introduction
- Prise en charge de la migration de connexion
- Découverte du MTU de chemin

### 7.2 Avantages par rapport à SSU (ancien)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">SSU (Legacy)</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">SSU2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ElGamal + AES</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519 + ChaCha20/Poly1305</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Header encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Partial</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Full (ChaCha20)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connection ID</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fixed</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypted, rotatable</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NAT traversal</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Basic introduction</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Enhanced hole punching + relay</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Obfuscation</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Minimal</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Improved (variable padding)</td>
    </tr>
  </tbody>
</table>
Consultez la [spécification SSU2](/docs/specs/ssu2/) (protocole de transport UDP de seconde génération d'I2P) pour tous les détails.

---

## 8. Traversée de NAT

Les deux transports prennent en charge la traversée du NAT afin de permettre aux routers derrière un pare-feu de participer au réseau.

### 8.1 Introduction à SSU2

Lorsqu’un router ne peut pas accepter des connexions entrantes directement :

1. Le router publie les adresses d'**introducer** (nœud introducteur) dans son RouterInfo
2. Le pair qui se connecte envoie une requête d'introduction à l'introducer
3. L'introducer relaie les informations de connexion au router derrière un pare-feu
4. Le router derrière un pare-feu initie une connexion sortante (hole punch, traversée de NAT)
5. Communication directe établie

### 8.2 NTCP2 et pare-feu

NTCP2 nécessite une connectivité TCP entrante. Les routers derrière un NAT peuvent :

- Utiliser l'UPnP pour ouvrir automatiquement les ports
- Configurer manuellement la redirection de ports
- S'appuyer sur SSU2 pour les connexions entrantes tout en utilisant NTCP2 pour les connexions sortantes

---

## 9. Obfuscation du protocole

Les deux transports modernes intègrent des fonctionnalités d’obfuscation :

- **Bourrage aléatoire** dans les messages d'initialisation
- **En-têtes chiffrés** qui ne révèlent pas les signatures du protocole
- **Messages de longueur variable** pour résister à l'analyse du trafic
- **Aucun schéma fixe** lors de l'établissement de la connexion

> **Remarque**: L'obfuscation de la couche de transport complète mais ne remplace pas l'anonymat fourni par l'architecture de tunnel d'I2P.

---

## 10. Développements futurs

Les recherches et améliorations prévues comprennent:

- **Transports enfichables** – plugins d'obfuscation compatibles avec Tor
- **Transport basé sur QUIC** – étude des avantages du protocole QUIC
- **Optimisation des limites de connexion** – recherche sur les limites optimales des connexions aux pairs
- **Stratégies de padding améliorées** – résistance accrue à l'analyse de trafic

---

## 11. Références

- [Spécification NTCP2](/docs/specs/ntcp2/) – Transport TCP basé sur Noise
- [Spécification SSU2](/docs/specs/ssu2/) – UDP semi-fiable sécurisé 2
- [Spécification I2NP](/docs/specs/i2np/) – Messages du protocole réseau I2P
- [Structures communes](/docs/specs/common-structures/) – RouterInfo et structures d’adresses
- [Discussion historique sur NTCP](/docs/ntcp/) – Historique du développement du transport hérité
- [Documentation SSU héritée](/docs/legacy/ssu/) – Spécification SSU originale (obsolète)
