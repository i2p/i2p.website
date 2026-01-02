---
title: "I2P : Un cadre évolutif pour la communication anonyme"
description: "Introduction technique à l'architecture et au fonctionnement d'I2P"
slug: "tech-intro"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Introduction

I2P est une couche réseau anonyme à commutation de paquets, évolutive, auto-organisée et résiliente, sur laquelle peut fonctionner un nombre quelconque d'applications différentes soucieuses de l'anonymat ou de la sécurité. Chacune de ces applications peut faire ses propres compromis en matière d'anonymat, de latence et de débit sans se soucier de la mise en œuvre appropriée d'un mixnet à route libre, leur permettant de fusionner leur activité avec l'ensemble d'anonymat plus large des utilisateurs qui utilisent déjà I2P.

Les applications déjà disponibles offrent une gamme complète d'activités Internet typiques — navigation web **anonyme**, hébergement web, messagerie instantanée, partage de fichiers, courrier électronique, blogs et syndication de contenu, ainsi que plusieurs autres applications en cours de développement.

- **Navigation web :** en utilisant n'importe quel navigateur existant qui prend en charge un proxy  
- **Chat :** IRC et autres protocoles  
- **Partage de fichiers :** [I2PSnark](#i2psnark) et autres applications  
- **E-mail :** [Susimail](#i2pmail) et autres applications  
- **Blog :** en utilisant n'importe quel serveur web local, ou des plugins disponibles

Contrairement aux sites web hébergés au sein de réseaux de distribution de contenu comme [Freenet](/docs/overview/comparison#freenet) ou [GNUnet](https://www.gnunet.org/), les services hébergés sur I2P sont entièrement interactifs — il existe des moteurs de recherche de style web traditionnel, des forums de discussion, des blogs sur lesquels vous pouvez commenter, des sites pilotés par base de données, et des passerelles pour interroger des systèmes statiques comme Freenet sans avoir besoin de les installer localement.

Avec toutes ces applications permettant l'anonymat, I2P agit comme un **intergiciel orienté messages** — les applications spécifient les données à envoyer vers un identifiant cryptographique (une "destination"), et I2P s'assure qu'elles arrivent de manière sécurisée et anonyme. I2P inclut également une simple [bibliothèque de streaming](#streaming) pour permettre aux messages anonymes en best-effort d'I2P d'être transférés sous forme de flux fiables et ordonnés, offrant un contrôle de congestion basé sur TCP adapté au produit bande passante-délai élevé du réseau.

Bien que de simples proxies SOCKS aient été développés pour connecter des applications existantes, leur valeur est limitée car la plupart des applications divulguent des informations sensibles dans un contexte anonyme. L'approche la plus sûre consiste à **auditer et adapter** l'application pour utiliser directement les API d'I2P.

I2P n'est pas un projet de recherche — académique, commercial ou gouvernemental — mais un effort d'ingénierie visant à fournir un anonymat utilisable. Il est en développement continu depuis début 2003 par un groupe distribué de contributeurs dans le monde entier. Tout le travail sur I2P est **open source** sur le [site officiel](https://geti2p.net/), principalement publié dans le domaine public, avec certains composants sous licences permissives de style BSD. Plusieurs applications clientes sous licence GPL sont disponibles, telles que [I2PTunnel](#i2ptunnel), [Susimail](#i2pmail) et [I2PSnark](#i2psnark). Le financement provient uniquement de dons d'utilisateurs.

---

## Fonctionnement

### Overview

I2P fait une distinction claire entre les routers (nœuds participant au réseau) et les destinations (points de terminaison anonymes pour les applications). L'exécution d'I2P elle-même n'est pas secrète ; ce qui est caché est **ce que** l'utilisateur fait et quel router ses destinations utilisent. Les utilisateurs finaux exécutent généralement plusieurs destinations (par exemple, une pour la navigation web, une autre pour l'hébergement, une autre pour IRC).

Un concept clé dans I2P est le **tunnel** — un chemin unidirectionnel chiffré à travers une série de routeurs. Chaque routeur ne déchiffre qu'une seule couche et ne connaît que le saut suivant. Les tunnels expirent toutes les 10 minutes et doivent être reconstruits.

![Schéma des tunnels entrants et sortants](/images/tunnels.png)   *Figure 1 : Il existe deux types de tunnels — entrants (inbound) et sortants (outbound).*

- **Les tunnels sortants** envoient des messages depuis le créateur.  
- **Les tunnels entrants** ramènent des messages vers le créateur.

La combinaison de ces éléments permet une communication bidirectionnelle. Par exemple, "Alice" utilise un tunnel sortant pour envoyer vers le tunnel entrant de "Bob". Alice chiffre son message avec les instructions de routage vers la passerelle d'entrée de Bob.

Un autre concept clé est la **base de données réseau** ou **netDb**, qui distribue les métadonnées sur les routeurs et les destinations :

- **RouterInfo:** Contient les informations de contact du routeur et le matériel cryptographique.  
- **LeaseSet:** Contient les informations nécessaires pour contacter une destination (passerelles de tunnel, dates d'expiration, clés de chiffrement).

Les routeurs publient leur RouterInfo directement dans la netDb ; les LeaseSets sont envoyés via des tunnels sortants pour l'anonymat.

Pour construire des tunnels, Alice interroge la netDb à la recherche d'entrées RouterInfo afin de choisir des pairs, puis envoie des messages de construction de tunnel chiffrés de pair en pair jusqu'à ce que le tunnel soit complet.

![Les informations de router sont utilisées pour construire des tunnels](/images/netdb_get_routerinfo_2.png)   *Figure 2 : Les informations de router sont utilisées pour construire des tunnels.*

Pour envoyer des données à Bob, Alice recherche le LeaseSet de Bob et utilise l'un de ses tunnels sortants pour acheminer les données via la passerelle du tunnel entrant de Bob.

![Les LeaseSets connectent les tunnels entrants et sortants](/images/netdb_get_leaseset.png)   *Figure 3 : Les LeaseSets connectent les tunnels sortants et entrants.*

Parce qu'I2P est basé sur les messages, il ajoute un **chiffrement garlic de bout en bout** pour protéger les messages même du point de sortie sortant ou de la passerelle d'entrée. Un message garlic enveloppe plusieurs "cloves" (messages) chiffrés pour masquer les métadonnées et améliorer l'anonymat.

Les applications peuvent soit utiliser l'interface de message directement, soit s'appuyer sur la [bibliothèque de streaming](#streaming) pour des connexions fiables.

---

### Tunnels

Les tunnels entrants et sortants utilisent tous deux le chiffrement en couches, mais diffèrent dans leur construction :

- Dans les **tunnels entrants**, le créateur (le point de terminaison) déchiffre toutes les couches.
- Dans les **tunnels sortants**, le créateur (la passerelle) pré-déchiffre les couches pour assurer la clarté au point de terminaison.

I2P profile les pairs via des métriques indirectes telles que la latence et la fiabilité sans sondage direct. Sur la base de ces profils, les pairs sont regroupés dynamiquement en quatre niveaux :

1. Rapide et haute capacité
2. Haute capacité
3. Non défaillant
4. Défaillant

La sélection des pairs de tunnel privilégie généralement les pairs à haute capacité, choisis aléatoirement pour équilibrer anonymat et performance, avec des stratégies d'ordonnancement supplémentaires basées sur XOR pour atténuer les attaques par prédécesseur et la collecte du netDb.

Pour plus de détails, consultez la [Spécification des Tunnels](/docs/specs/implementation).

---

### Aperçu

Les routeurs participant à la table de hachage distribuée (DHT) **floodfill** stockent et répondent aux recherches de LeaseSet. La DHT utilise une variante de [Kademlia](https://en.wikipedia.org/wiki/Kademlia). Les routeurs floodfill sont sélectionnés automatiquement s'ils disposent de suffisamment de capacité et de stabilité, ou peuvent être configurés manuellement.

- **RouterInfo:** Décrit les capacités et les transports d'un router.  
- **LeaseSet:** Décrit les tunnels et les clés de chiffrement d'une destination.

Toutes les données dans le netDb sont signées par l'éditeur et horodatées pour prévenir les attaques par rejeu ou par entrées périmées. La synchronisation temporelle est maintenue via SNTP et la détection de décalage au niveau de la couche transport.

#### Additional concepts

- **LeaseSets non publiés et chiffrés :**  
  Une destination peut rester privée en ne publiant pas son LeaseSet, en le partageant uniquement avec des pairs de confiance. L'accès nécessite la clé de déchiffrement appropriée.

- **Bootstrapping (reseeding) :**  
  Pour rejoindre le réseau, un nouveau router télécharge des fichiers RouterInfo signés depuis des serveurs de reseed HTTPS de confiance.

- **Évolutivité des recherches :**  
  I2P utilise des recherches **itératives**, et non récursives, pour améliorer l'évolutivité et la sécurité de la DHT.

---

### Tunnels

La communication I2P moderne utilise deux transports entièrement chiffrés :

- **[NTCP2](/docs/specs/ntcp2):** Protocole basé sur TCP chiffré  
- **[SSU2](/docs/specs/ssu2):** Protocole basé sur UDP chiffré

Tous deux sont construits sur le moderne [Noise Protocol Framework](https://noiseprotocol.org/), offrant une authentification forte et une résistance à l'empreinte digitale du trafic. Ils ont remplacé les protocoles hérités NTCP et SSU (complètement retirés depuis 2023).

**NTCP2** offre un streaming chiffré et efficace sur TCP.

**SSU2** fournit une fiabilité basée sur UDP, la traversée NAT et un perçage de trou optionnel. SSU2 est conceptuellement similaire à WireGuard ou QUIC, équilibrant fiabilité et anonymat.

Les routeurs peuvent prendre en charge à la fois IPv4 et IPv6, en publiant leurs adresses de transport et leurs coûts dans la netDb. Le transport d'une connexion est sélectionné dynamiquement par un **système d'enchères** qui optimise en fonction des conditions et des liens existants.

---

### Base de données réseau (netDb)

I2P utilise une cryptographie en couches pour tous les composants : transports, tunnels, messages garlic et la base de données réseau (netDb).

Les primitives actuelles incluent :

- X25519 pour l'échange de clés
- EdDSA (Ed25519) pour les signatures
- ChaCha20-Poly1305 pour le chiffrement authentifié
- SHA-256 pour le hachage
- AES256 pour le chiffrement de la couche tunnel

Les algorithmes historiques (ElGamal, DSA-SHA1, ECDSA) sont conservés pour des raisons de rétrocompatibilité.

I2P introduit actuellement des schémas cryptographiques hybrides post-quantiques (PQ) combinant **X25519** avec **ML-KEM** pour résister aux attaques de type « récolter maintenant, déchiffrer plus tard ».

#### Garlic Messages

Les messages garlic étendent le routage en oignon en regroupant plusieurs « cloves » (segments) chiffrés avec des instructions de livraison indépendantes. Ceux-ci permettent une flexibilité de routage au niveau des messages et un remplissage uniforme du trafic.

#### Session Tags

Deux systèmes cryptographiques sont pris en charge pour le chiffrement de bout en bout :

- **ElGamal/AES+SessionTags (hérité) :**  
  Utilise des tags de session pré-livrés comme nonces de 32 octets. Désormais obsolète en raison de son inefficacité.

- **ECIES-X25519-AEAD-Ratchet (actuel) :**  
  Utilise ChaCha20-Poly1305 et des PRNG synchronisés basés sur HKDF pour générer dynamiquement des clés de session éphémères et des balises de 8 octets, réduisant la charge processeur, mémoire et bande passante tout en maintenant la confidentialité persistante (forward secrecy).

---

## Future of the Protocol

Les domaines de recherche clés se concentrent sur le maintien de la sécurité contre les adversaires étatiques et l'introduction de protections post-quantiques. Deux concepts de conception précoces — les **routes restreintes** et la **latence variable** — ont été remplacés par des développements modernes.

### Restricted Route Operation

Les concepts originaux de routage restreint visaient à masquer les adresses IP. Ce besoin a été largement atténué par :

- UPnP pour la redirection automatique de ports  
- Traversée NAT robuste en SSU2  
- Support IPv6  
- Introducers coopératifs et perforation NAT  
- Connectivité overlay optionnelle (par exemple, Yggdrasil)

Ainsi, l'I2P moderne atteint les mêmes objectifs de manière plus pratique sans routage restreint complexe.

---

## Similar Systems

I2P intègre des concepts issus des middleware orientés messages, des DHT et des mixnets. Son innovation réside dans la combinaison de ces éléments en une plateforme d'anonymat utilisable et auto-organisée.

### Protocoles de transport

*[Site web](https://www.torproject.org/)*

**Tor** et **I2P** partagent des objectifs mais diffèrent architecturalement :

- **Tor:** Commutation de circuits ; repose sur des autorités d'annuaire de confiance. (~10k relais)  
- **I2P:** Commutation de paquets ; réseau entièrement distribué piloté par DHT. (~50k routers)

Les tunnels unidirectionnels d'I2P exposent moins de métadonnées et permettent des chemins de routage flexibles, tandis que Tor se concentre sur l'accès anonyme à **Internet (outproxying)**.   I2P prend plutôt en charge l'**hébergement anonyme dans le réseau**.

### Cryptographie

*[Site web](https://freenetproject.org/)*

**Freenet** se concentre sur la publication et la récupération anonymes et persistantes de fichiers. **I2P**, en revanche, fournit une **couche de communications en temps réel** pour une utilisation interactive (web, chat, torrents). Ensemble, les deux systèmes se complètent — Freenet fournit un stockage résistant à la censure ; I2P fournit l'anonymat du transport.

### Other Networks

- **Lokinet:** Réseau superposé basé sur IP utilisant des nœuds de service incités.  
- **Nym:** Mixnet de nouvelle génération mettant l'accent sur la protection des métadonnées avec trafic de couverture à latence plus élevée.

---

## Appendix A: Application Layer

I2P lui-même ne gère que le transport des messages. Les fonctionnalités de la couche application sont implémentées en externe via des API et des bibliothèques.

### Streaming Library {#streaming}

La **bibliothèque de streaming** fonctionne comme l'analogue TCP d'I2P, avec un protocole de fenêtre glissante et un contrôle de congestion optimisés pour le transport anonyme à haute latence.

Les schémas typiques de requête/réponse HTTP peuvent souvent se terminer en un seul aller-retour grâce aux optimisations de regroupement de messages.

### Naming Library and Address Book

*Développé par : mihi, Ragnarok*   Voir la page [Nommage et Carnet d'adresses](/docs/overview/naming).

Le système de nommage d'I2P est **local et décentralisé**, évitant les noms globaux de type DNS. Chaque router maintient une correspondance locale entre des noms lisibles par l'homme et des destinations. Des carnets d'adresses optionnels basés sur un réseau de confiance peuvent être partagés ou importés depuis des pairs de confiance.

Cette approche évite les autorités centralisées et contourne les vulnérabilités Sybil inhérentes aux systèmes de nommage globaux ou basés sur le vote.

### Fonctionnement en mode de routage restreint

*Développé par : mihi*

**I2PTunnel** est l'interface principale de la couche client permettant le proxy TCP anonyme. Il prend en charge :

- **Tunnels client** (sortants vers les destinations I2P)  
- **Client HTTP (eepproxy)** pour les domaines ".i2p"  
- **Tunnels serveur** (entrants depuis I2P vers un service local)  
- **Tunnels serveur HTTP** (proxy sécurisé pour les services web)

L'outproxy (vers l'Internet classique) est facultatif, mis en œuvre par des tunnels « serveur » gérés par des volontaires.

### I2PSnark {#i2psnark}

*Développé par : jrandom, et al — porté depuis [Snark](http://www.klomp.org/snark/)*

Fourni avec I2P, **I2PSnark** est un client BitTorrent anonyme multi-torrent avec support DHT et UDP, accessible via une interface web.

### Tor

*Développé par : postman, susi23, mastiejaner*

**I2Pmail** fournit un courrier électronique anonyme via des connexions I2PTunnel. **Susimail** est un client web conçu spécifiquement pour empêcher les fuites d'informations courantes dans les clients de messagerie traditionnels. Le service [mail.i2p](https://mail.i2p/) propose un filtrage antivirus, des quotas [hashcash](https://en.wikipedia.org/wiki/Hashcash) et une séparation des proxies de sortie pour une protection supplémentaire.

---
