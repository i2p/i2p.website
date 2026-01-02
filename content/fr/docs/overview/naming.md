---
title: "Nommage et carnet d'adresses"
description: "Comment I2P associe les noms d'hôtes lisibles aux destinations"
slug: "naming"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

Les adresses I2P sont de longues clés cryptographiques. Le système de nommage fournit une couche plus conviviale au-dessus de ces clés **sans introduire d'autorité centrale**. Tous les noms sont **locaux**—chaque router décide indépendamment à quelle destination un nom d'hôte fait référence.

> **Besoin de contexte ?** La [discussion sur le nommage](/docs/legacy/naming/) documente les débats de conception initiaux, les propositions alternatives et les fondements philosophiques derrière le système de nommage décentralisé d'I2P.

---

## 1. Composants

La couche de nommage d'I2P est composée de plusieurs sous-systèmes indépendants mais coopératifs :

1. **Service de nommage** – résout les noms d'hôtes en destinations et gère les [noms d'hôtes Base32](#base32-hostnames).
2. **Proxy HTTP** – transmet les recherches `.i2p` au router et suggère des services jump lorsqu'un nom est inconnu.
3. **Services d'ajout d'hôtes** – formulaires de type CGI qui ajoutent de nouvelles entrées dans le carnet d'adresses local.
4. **Services jump** – assistants distants qui renvoient la destination pour un nom d'hôte fourni.
5. **Carnet d'adresses** – récupère et fusionne périodiquement des listes d'hôtes distantes en utilisant un « réseau de confiance » localement approuvé.
6. **SusiDNS** – une interface web pour gérer les carnets d'adresses, les abonnements et les remplacements locaux.

Cette conception modulaire permet aux utilisateurs de définir leurs propres limites de confiance et d'automatiser autant ou aussi peu que souhaité le processus de nommage.

---

## 2. Services de Nommage

L'API de nommage du router (`net.i2p.client.naming`) prend en charge plusieurs backends via la propriété configurable `i2p.naming.impl=<class>`. Chaque implémentation peut offrir différentes stratégies de recherche, mais toutes partagent le même modèle de confiance et de résolution.

### 2.1 Hosts.txt (legacy format)

Le modèle historique utilisait trois fichiers en texte brut vérifiés dans l'ordre :

1. `privatehosts.txt`
2. `userhosts.txt`
3. `hosts.txt`

Chaque ligne stocke une correspondance `hostname=base64-destination`. Ce format texte simple reste entièrement pris en charge pour l'import/export, mais ce n'est plus le format par défaut en raison de performances médiocres une fois que la liste d'hôtes dépasse quelques milliers d'entrées.

---

### 2.2 Blockfile Naming Service (default backend)

Introduit dans la **version 0.8.8**, le Blockfile Naming Service est désormais le backend par défaut. Il remplace les fichiers plats par un magasin clé/valeur haute performance sur disque basé sur des skiplists (`hostsdb.blockfile`) qui offre des recherches environ **10× plus rapides**.

**Caractéristiques principales :** - Stocke plusieurs carnets d'adresses logiques (privé, utilisateur et hôtes) dans une seule base de données binaire. - Maintient la compatibilité avec l'import/export des fichiers hosts.txt hérités. - Prend en charge les recherches inversées, les métadonnées (date d'ajout, source, commentaires) et la mise en cache efficace. - Utilise le même ordre de recherche à trois niveaux : privé → utilisateur → hôtes.

Cette approche préserve la rétrocompatibilité tout en améliorant considérablement la vitesse de résolution et l'évolutivité.

---

### 2.1 Hosts.txt (format obsolète)

Les développeurs peuvent implémenter des backends personnalisés tels que : - **Meta** – agrège plusieurs systèmes de nommage. - **PetName** – prend en charge les petnames stockés dans un fichier `petnames.txt`. - **AddressDB**, **Exec**, **Eepget**, et **Dummy** – pour la résolution externe ou de secours.

L'implémentation blockfile reste le backend **recommandé** pour un usage général en raison de ses performances et de sa fiabilité.

---

## 3. Base32 Hostnames

Les noms d'hôte Base32 (`*.b32.i2p`) fonctionnent de manière similaire aux adresses `.onion` de Tor. Lorsque vous accédez à une adresse `.b32.i2p` :

1. Le routeur décode la charge utile Base32.
2. Il reconstruit la destination directement à partir de la clé—**aucune recherche dans le carnet d'adresses n'est requise**.

Cela garantit l'accessibilité même si aucun nom d'hôte lisible par l'homme n'existe. Les noms Base32 étendus introduits dans la **version 0.9.40** prennent en charge **LeaseSet2** et les destinations chiffrées.

---

## 4. Address Book & Subscriptions

L'application de carnet d'adresses récupère les listes d'hôtes distants via HTTP et les fusionne localement selon les règles de confiance configurées par l'utilisateur.

### 2.2 Service de nommage Blockfile (backend par défaut)

- Les abonnements sont des URL `.i2p` standard pointant vers des fichiers `hosts.txt` ou des flux de mise à jour incrémentale.
- Les mises à jour sont récupérées périodiquement (toutes les heures par défaut) et validées avant fusion.
- Les conflits sont résolus selon le principe **premier arrivé, premier servi**, suivant l'ordre de priorité :  
  `privatehosts.txt` → `userhosts.txt` → `hosts.txt`.

#### Default Providers

Depuis **I2P 2.3.0 (juin 2023)**, deux fournisseurs d'abonnement par défaut sont inclus : - `http://i2p-projekt.i2p/hosts.txt` - `http://notbob.i2p/hosts.txt`

Cette redondance améliore la fiabilité tout en préservant le modèle de confiance local. Les utilisateurs peuvent ajouter ou supprimer des abonnements via SusiDNS.

#### Incremental Updates

Les mises à jour incrémentales sont récupérées via `newhosts.txt` (remplaçant l'ancien concept `recenthosts.cgi`). Ce point de terminaison fournit des mises à jour delta efficaces **basées sur ETag**—renvoyant uniquement les nouvelles entrées depuis la dernière requête ou `304 Not Modified` lorsqu'il n'y a aucun changement.

---

### 2.3 Backends alternatifs et plug-ins

- **Les services Host-add** (`add*.cgi`) permettent la soumission manuelle de mappages nom-vers-destination. Vérifiez toujours la destination avant d'accepter.  
- **Les services Jump** répondent avec la clé appropriée et peuvent rediriger via le proxy HTTP avec un paramètre `?i2paddresshelper=`.  
  Exemples courants : `stats.i2p`, `identiguy.i2p`, et `notbob.i2p`.  
  Ces services ne sont **pas des autorités de confiance**—les utilisateurs doivent décider lesquels utiliser.

---

## 5. Managing Entries Locally (SusiDNS)

SusiDNS est disponible à : `http://127.0.0.1:7657/susidns/`

Vous pouvez : - Afficher et modifier les carnets d'adresses locaux. - Gérer et prioriser les abonnements. - Importer/exporter des listes d'hôtes. - Configurer les planifications de récupération.

**Nouveautés d'I2P 2.8.1 (mars 2025) :** - Ajout d'une fonctionnalité « trier par date ». - Amélioration de la gestion des abonnements (correction des incohérences ETag).

Tous les changements restent **locaux**—le carnet d'adresses de chaque routeur est unique.

---

## 3. Noms d'hôte Base32

Conformément à la RFC 9476, I2P a enregistré **`.i2p.alt`** auprès de la GNUnet Assigned Numbers Authority (GANA) depuis **mars 2025 (I2P 2.8.1)**.

**Objectif :** Empêcher les fuites DNS accidentelles provenant de logiciels mal configurés.

- Les résolveurs DNS conformes à la RFC 9476 **ne transmettront pas** les domaines `.alt` au DNS public.
- Le logiciel I2P traite `.i2p.alt` comme équivalent à `.i2p`, en supprimant le suffixe `.alt` lors de la résolution.
- `.i2p.alt` n'est **pas** destiné à remplacer `.i2p` ; c'est une mesure de sécurité technique, pas un changement de marque.

---

## 4. Carnet d'adresses et abonnements

- **Clés de destination :** 516–616 octets (Base64)  
- **Noms d'hôte :** Maximum 67 caractères (incluant `.i2p`)  
- **Caractères autorisés :** a–z, 0–9, `-`, `.` (pas de points doubles, pas de majuscules)  
- **Réservé :** `*.b32.i2p`  
- **ETag et Last-Modified :** activement utilisés pour minimiser la bande passante  
- **Taille moyenne de hosts.txt :** ~400 Ko pour ~800 hôtes (chiffre d'exemple)  
- **Utilisation de la bande passante :** ~10 octets/sec si récupéré toutes les 12 heures

---

## 8. Security Model and Philosophy

I2P sacrifie intentionnellement l'unicité globale en échange de la décentralisation et de la sécurité—une application directe du **triangle de Zooko**.

**Principes clés :** - **Aucune autorité centrale :** toutes les recherches sont locales.   - **Résistance au détournement DNS :** les requêtes sont chiffrées vers les clés publiques de destination.   - **Prévention des attaques Sybil :** aucun système de vote ou de nommage basé sur le consensus.   - **Associations immuables :** une fois qu'une association locale existe, elle ne peut pas être écrasée à distance.

Les systèmes de nommage basés sur la blockchain (par exemple, Namecoin, ENS) ont exploré la résolution des trois côtés du triangle de Zooko, mais I2P les évite intentionnellement en raison de la latence, de la complexité et de l'incompatibilité philosophique avec son modèle de confiance local.

---

## 9. Compatibility and Stability

- Aucune fonctionnalité de nommage n'a été dépréciée entre 2023 et 2025.
- Le format hosts.txt, les services de redirection (jump services), les abonnements et toutes les implémentations d'API de nommage restent fonctionnels.
- Le projet I2P maintient une stricte **rétrocompatibilité** tout en introduisant des améliorations de performance et de sécurité (isolation NetDB, séparation Sub-DB, etc.).

---

## 10. Best Practices

- Conservez uniquement les abonnements de confiance ; évitez les listes d'hôtes volumineuses et inconnues.
- Sauvegardez `hostsdb.blockfile` et `privatehosts.txt` avant toute mise à niveau ou réinstallation.
- Examinez régulièrement les services de saut (jump services) et désactivez ceux en qui vous n'avez plus confiance.
- N'oubliez pas : votre carnet d'adresses définit votre version du monde I2P—**chaque nom d'hôte est local**.

---

### Further Reading

- [Discussion sur le nommage](/docs/legacy/naming/)  
- [Spécification Blockfile](/docs/specs/blockfile/)  
- [Format du fichier de configuration](/docs/specs/configuration/)  
- [Javadoc du service de nommage](http://idk.i2p/javadoc-i2p/net/i2p/client/naming/package-summary.html)

---
