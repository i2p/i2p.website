---
title: "Discussion sur le tunnel"
description: "Exploration historique du bourrage des tunnels, de la fragmentation et des stratégies de construction des tunnels"
slug: "tunnel"
layout: "single"
lastUpdated: "2019-07"
accurateFor: "0.9.41"
reviewStatus: "needs-review"
---

> **Remarque :** Cette archive rassemble des travaux de conception spéculatifs antérieurs à I2P 0.9.41. Pour l’implémentation en production, consultez la [documentation des tunnels](/docs/specs/implementation/).

## Alternatives de configuration

Les idées envisagées pour de futurs paramètres de tunnel comprenaient :

- Mécanismes de limitation de fréquence pour la livraison des messages
- Politiques de bourrage (y compris l'injection de chaff (trafic factice))
- Contrôles de durée de vie des tunnels
- Stratégies de traitement par lots et de gestion des files d'attente pour l'acheminement des charges utiles

Aucune de ces options n’était incluse dans l’ancienne implémentation.

## Stratégies de bourrage

Approches potentielles de remplissage discutées :

- Sans aucun remplissage
- Remplissage de longueur aléatoire
- Remplissage de longueur fixe
- Remplissage jusqu’au kilooctet le plus proche
- Remplissage jusqu’à une puissance de deux (`2^n` octets)

Les premières mesures (version 0.4) ont conduit à la taille fixe actuelle de 1024 octets des messages tunnel. Les garlic messages (format de messages agrégés spécifique à I2P) de niveau supérieur peuvent ajouter leur propre bourrage.

## Fragmentation

Pour éviter les attaques par marquage fondées sur la longueur des messages, les messages de tunnel ont une taille fixe de 1024 octets. Les charges utiles I2NP plus volumineuses sont fragmentées par la passerelle ; le point de terminaison réassemble les fragments dans un court délai d’expiration. Les routers peuvent réorganiser les fragments afin de maximiser l’efficacité du remplissage avant l’envoi.

## Alternatives supplémentaires

### Ajuster le traitement des tunnels en cours de route

Trois possibilités ont été examinées :

1. Autoriser un saut intermédiaire à mettre fin temporairement à un tunnel en accordant l’accès aux charges utiles déchiffrées.
2. Autoriser les routers participants à « remixer » les messages en les envoyant par l’un de leurs propres tunnels sortants avant de passer au prochain saut.
3. Permettre au créateur du tunnel de redéfinir dynamiquement le prochain saut d’un pair.

### Tunnels bidirectionnels

L’utilisation de tunnels entrants et sortants distincts limite les informations qu’un même ensemble de pairs peut observer (par exemple, une requête GET par opposition à une réponse volumineuse). Les tunnels bidirectionnels simplifient la gestion des pairs, mais exposent intégralement les schémas de trafic dans les deux directions simultanément. Les tunnels unidirectionnels sont donc restés l’approche privilégiée.

### Canaux de retour et tailles variables

Autoriser des tailles de messages de tunnel variables permettrait des canaux cachés entre des pairs agissant de concert (p. ex., en codant des données via des tailles ou des fréquences choisies). Des messages de taille fixe atténuent ce risque au prix d’un surcoût de bourrage supplémentaire.

## Alternatives pour la construction de tunnels

Référence : [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf)

### Ancienne méthode de compilation “parallèle”

Avant la version 0.6.1.10, les requêtes de construction de tunnel étaient envoyées en parallèle à chaque participant. Cette méthode est documentée sur la [ancienne page du tunnel](/docs/legacy/old-implementation/).

### Construction télescopique en une seule fois (méthode actuelle)

L’approche moderne envoie les messages de construction de saut en saut à travers le tunnel partiellement construit. Bien que similaire au "telescoping" de Tor (construction de circuits en ajoutant les relais un par un), l’acheminement des messages de construction via des tunnels exploratoires réduit les fuites d’information.

### Télescopage « interactif »

Construire un saut à la fois avec des allers-retours explicites permet aux pairs de compter les messages et d’inférer leur position dans le tunnel, donc cette approche a été rejetée.

### Tunnels de gestion non exploratoires

Une proposition était de maintenir un groupe distinct de tunnels de gestion dédiés au build traffic (trafic de construction de tunnels). Bien que cela puisse aider les routers partitionnés, cela a été jugé inutile avec une intégration réseau suffisante.

### Acheminement exploratoire (hérité)

Avant la version 0.6.1.10, les requêtes de tunnel individuelles étaient chiffrées avec garlic encryption et acheminées via des tunnels exploratoires, les réponses revenant séparément. Cette stratégie a été remplacée par la one-shot telescoping method (méthode télescopique en une seule étape) actuelle.

## Points à retenir

- Des messages de tunnel de taille fixe protègent contre le marquage basé sur la taille et les canaux clandestins, malgré le coût supplémentaire du bourrage.
- Des alternatives en matière de bourrage, de fragmentation et de stratégies de construction (build) ont été explorées, mais n'ont pas été adoptées au regard des compromis d’anonymat.
- La conception des tunnels continue d’équilibrer l’efficacité, l’observabilité et la résistance aux attaques de prédécesseur et de congestion.
