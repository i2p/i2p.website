---
title: "Discussion sur la base de données du réseau"
description: "Notes historiques sur floodfill, les expérimentations Kademlia et les ajustements futurs pour la netDb"
slug: "netdb"
reviewStatus: "needs-review"
---

> **Remarque :** Cette discussion archivée présente des approches historiques de la base de données réseau (netDb). Consultez la [documentation principale de netDb](/docs/specs/common-structures/) pour le comportement actuel et les recommandations.

## Historique

Le netDb d'I2P est distribué au moyen d'un algorithme floodfill simple. Les premières versions conservaient également une implémentation de la DHT Kademlia comme solution de repli, mais elle s'est révélée peu fiable et a été entièrement désactivée dans la version 0.6.1.20. La conception floodfill transmet une entrée publiée à un router participant, attend une confirmation, puis réessaie avec d'autres pairs floodfill si nécessaire. Les pairs floodfill propagent vers tous les autres participants floodfill les enregistrements provenant des routers non-floodfill.

Fin 2009, les recherches Kademlia (protocole DHT) ont été partiellement réintroduites afin de réduire la charge de stockage pesant sur les floodfill routers individuels.

### Introduction à Floodfill

Floodfill est apparu pour la première fois dans la version 0.6.0.4, tandis que Kademlia est resté disponible en solution de repli. À l'époque, d'importantes pertes de paquets et des routes restreintes rendaient difficile l'obtention d'accusés de réception de la part des quatre pairs les plus proches, nécessitant souvent des dizaines de tentatives de stockage redondantes. Le passage à un sous-ensemble floodfill de routers joignables depuis l'extérieur a apporté une solution pragmatique à court terme.

### Repenser Kademlia (protocole de table de hachage distribuée, DHT)

Parmi les alternatives envisagées figuraient :

- Exécuter la netDb en tant que DHT Kademlia, limitée aux routers joignables qui choisissent d’y participer
- Conserver le modèle floodfill tout en limitant la participation aux routers capables et en vérifiant la distribution au moyen de contrôles aléatoires

L’approche floodfill l’a emporté parce qu’elle était plus facile à déployer et que la netDb ne contient que des métadonnées, pas de données utilisateur. La plupart des destinations ne publient jamais de LeaseSet, car l’expéditeur inclut généralement son LeaseSet dans des garlic messages (un mécanisme de regroupement de messages).

## Statut actuel (perspective historique)

Les algorithmes du netDb sont adaptés aux besoins du réseau et ont historiquement géré aisément quelques centaines de routers. Les premières estimations suggéraient que 3–5 floodfill routers pouvaient prendre en charge environ 10 000 nœuds.

### Calculs mis à jour (mars 2008)

```
recvKBps = N * (L + 1) * (1 + F) * (1 + R) * S / T
```
Où :

- `N`: routers dans le réseau
- `L`: Nombre moyen de destinations client par router (plus un pour le `RouterInfo`)
- `F`: Pourcentage d’échec de tunnel
- `R`: Période de reconstruction de tunnel en fraction de la durée de vie du tunnel
- `S`: Taille moyenne d’une entrée netDb
- `T`: Durée de vie du tunnel

En utilisant des valeurs datant de 2008 (`N = 700`, `L = 0.5`, `F = 0.33`, `R = 0.5`, `S = 4 KB`, `T = 10 minutes`) on obtient :

```
recvKBps ≈ 700 * (0.5 + 1) * (1 + 0.33) * (1 + 0.5) * 4 KB / 10m ≈ 28 KBps
```
### Kademlia (protocole DHT) fera-t-il son retour ?

Les développeurs ont discuté de la réintroduction de Kademlia (algorithme de table de hachage distribuée, DHT) vers début 2007. Le consensus était que la capacité floodfill (mode de diffusion de la netDb) pouvait être augmentée progressivement selon les besoins, tandis que Kademlia ajoutait une complexité et des besoins en ressources importants pour la population de routers standard. Le mécanisme de repli reste dormant à moins que la capacité floodfill ne devienne insuffisante.

### Planification de la capacité Floodfill

L’admission automatique des routers de classe de bande passante `O` dans le floodfill, bien que tentante, comporte le risque de scénarios de déni de service si des nœuds hostiles choisissent d’y participer. Des analyses historiques ont suggéré que limiter le pool de floodfill (par exemple, 3–5 pairs gérant ~10K routers) était plus sécurisé. Des opérateurs de confiance ou des heuristiques automatiques ont été utilisés pour maintenir un ensemble de floodfill adéquat mais contrôlé.

## Floodfill À faire (Historique)

> Cette section est conservée pour la postérité. La page principale de netDb (base de données du réseau I2P) suit la feuille de route actuelle et les considérations de conception.

Des incidents opérationnels, comme une période, le 13 mars 2008, au cours de laquelle un seul floodfill router était disponible, ont entraîné plusieurs améliorations introduites dans les versions 0.6.1.33 à 0.7.x, notamment :

- Randomisation de la sélection des floodfill pour les recherches et préférence donnée aux pairs réactifs
- Affichage de métriques floodfill supplémentaires sur la page "Profiles" de la console du router
- Réductions progressives de la taille des entrées netDb pour réduire l'utilisation de bande passante des floodfill
- Participation automatique pour un sous-ensemble de routers de classe `O`, en fonction des performances collectées via les données de profil
- Amélioration des listes de blocage, de la sélection des pairs floodfill et des heuristiques d'exploration

Les idées restantes de cette période comprenaient :

- Utiliser les statistiques de `dbHistory` pour mieux évaluer et sélectionner des pairs floodfill
- Améliorer le comportement de réessai afin d’éviter de contacter à répétition des pairs défaillants
- Exploiter les métriques de latence et les scores d’intégration lors de la sélection
- Détecter et réagir plus rapidement aux routers floodfill défaillants
- Continuer à réduire la charge en ressources sur les nœuds à haut débit et les nœuds floodfill

Même à la date de ces notes, le réseau était considéré comme résilient, avec une infrastructure en place pour réagir rapidement aux floodfills hostiles ou aux attaques par déni de service ciblant les floodfills.

## Notes supplémentaires

- La console du router expose depuis longtemps des données de profil enrichies pour faciliter l'analyse de la fiabilité du floodfill.
- Alors que des commentaires historiques ont spéculé sur Kademlia ou des schémas DHT alternatifs, le floodfill est resté l'algorithme principal pour les réseaux de production.
- La recherche prospective s'est concentrée sur le fait de rendre l'admission au floodfill adaptative tout en limitant les possibilités d'abus.
