---
title: "Discussion sur les tunnels"
description: "Exploration historique des stratégies de remplissage de tunnel, de fragmentation et de construction"
slug: "tunnel"
aliases:
  - "/fr/docs/discussions/tunnel"
  - "/fr/docs/discussions/tunnel/"
  - "/fr/tunnel_discussion"
  - "/fr/tunnel_discussion/"
lastUpdated: "2019-07"
accurateFor: "0.9.41"
---

Note : Ce document contient des informations plus anciennes sur les alternatives à l'implémentation actuelle des tunnels dans I2P, et des spéculations sur les possibilités futures. Pour les informations actuelles, voir [la page des tunnels](/docs/specs/tunnel-implementation).

Cette page documente l'implémentation actuelle de construction de tunnel depuis la version 0.6.1.10. L'ancienne méthode de construction de tunnel, utilisée avant la version 0.6.1.10, est documentée sur [la page tunnel historique](/docs/historical/tunnel-alt).

### Alternatives de configuration {#config}

Au-delà de leur longueur, il peut y avoir des paramètres configurables supplémentaires pour chaque tunnel qui peuvent être utilisés, tels qu'une limitation de la fréquence des messages délivrés, comment le remplissage doit être utilisé, combien de temps un tunnel doit être en fonctionnement, s'il faut injecter des messages de bourrage, et quelles stratégies de traitement par lots, le cas échéant, doivent être employées. Aucune de ces fonctionnalités n'est actuellement implémentée.

### Alternatives de remplissage {#tunnel.padding}

Plusieurs stratégies de remplissage de tunnel sont possibles, chacune avec ses propres avantages :

- Pas de remplissage
- Remplissage à une taille aléatoire
- Remplissage à une taille fixe
- Remplissage au KB le plus proche
- Remplissage à la taille exponentielle la plus proche (2^n octets)

Ces stratégies de remplissage peuvent être utilisées à différents niveaux, permettant de traiter l'exposition des informations sur la taille des messages à différents adversaires. Après avoir rassemblé et examiné quelques statistiques du réseau 0.4, ainsi qu'exploré les compromis d'anonymat, nous commençons avec une taille fixe de message tunnel de 1024 octets. Cependant, à l'intérieur de cela, les messages fragmentés eux-mêmes ne sont pas du tout rembourrés par le tunnel (bien que pour les messages de bout en bout, ils puissent être rembourrés dans le cadre de l'encapsulation garlic).

### Alternatives de fragmentation {#tunnel.fragmentation}

Pour empêcher les adversaires de marquer les messages le long du chemin en ajustant la taille des messages, tous les messages de tunnel ont une taille fixe de 1024 octets. Pour accommoder les messages I2NP plus volumineux ainsi que pour supporter les plus petits de manière plus efficace, la passerelle divise les messages I2NP plus volumineux en fragments contenus dans chaque message de tunnel. Le point de terminaison tentera de reconstruire le message I2NP à partir des fragments pendant une courte période de temps, mais les rejettera si nécessaire.

Les routers ont beaucoup de latitude quant à la façon dont les fragments sont organisés, qu'ils soient empaquetés de manière inefficace comme unités discrètes, regroupés pendant une brève période pour faire tenir plus de charge utile dans les messages tunnel de 1024 octets, ou complétés de manière opportuniste avec d'autres messages que la passerelle voulait envoyer.

### Plus d'alternatives {#tunnel.alternatives}

#### Ajuster le traitement des tunnels en cours de route {#tunnel.reroute}

Bien que l'algorithme de routage de tunnel simple devrait être suffisant dans la plupart des cas, il existe trois alternatives qui peuvent être explorées :

- Faire en sorte qu'un pair autre que le point de terminaison agisse temporairement comme point de terminaison d'un tunnel en ajustant le chiffrement utilisé à la passerelle pour lui donner le texte en clair des messages I2NP prétraités. Chaque pair pourrait vérifier s'il avait le texte en clair, traitant le message à la réception comme s'il l'avait.
- Permettre aux routeurs participant à un tunnel de remixer le message avant de le transmettre - en le faisant rebondir à travers l'un des tunnels sortants de ce pair, portant des instructions pour la livraison au saut suivant.
- Implémenter du code pour que le créateur du tunnel redéfinisse le "saut suivant" d'un pair dans le tunnel, permettant une redirection dynamique supplémentaire.

#### Utiliser des Tunnels Bidirectionnels {#tunnel.bidirectional}

La stratégie actuelle consistant à utiliser deux tunnels séparés pour la communication entrante et sortante n'est pas la seule technique disponible, et elle a des implications en matière d'anonymat. Du côté positif, en utilisant des tunnels séparés, cela réduit les données de trafic exposées à l'analyse aux participants d'un tunnel - par exemple, les pairs dans un tunnel sortant depuis un navigateur web ne verraient que le trafic d'une requête HTTP GET, tandis que les pairs dans un tunnel entrant verraient la charge utile livrée le long du tunnel. Avec des tunnels bidirectionnels, tous les participants auraient accès au fait que par exemple 1 Ko a été envoyé dans une direction, puis 100 Ko dans l'autre. Du côté négatif, utiliser des tunnels unidirectionnels signifie qu'il y a deux ensembles de pairs qui doivent être profilés et pris en compte, et des précautions supplémentaires doivent être prises pour traiter la vitesse accrue des attaques de prédécesseur. Le processus de mise en commun et de construction de tunnels décrit ci-dessous devrait minimiser les inquiétudes concernant l'attaque de prédécesseur, bien que si cela était souhaité, il ne serait pas très difficile de construire à la fois les tunnels entrants et sortants le long des mêmes pairs.

#### Communication de canal de retour {#tunnel.backchannel}

Pour le moment, les valeurs IV utilisées sont des valeurs aléatoires. Cependant, il est possible que cette valeur de 16 octets soit utilisée pour envoyer des messages de contrôle depuis la passerelle vers le point de terminaison, ou sur les tunnels sortants, depuis la passerelle vers n'importe lequel des pairs. La passerelle entrante pourrait encoder certaines valeurs dans l'IV une seule fois, que le point de terminaison serait capable de récupérer (puisqu'il sait que le point de terminaison est aussi le créateur). Pour les tunnels sortants, le créateur pourrait fournir certaines valeurs aux participants durant la création du tunnel (par exemple "si vous voyez 0x0 comme IV, cela signifie X", "0x1 signifie Y", etc). Puisque la passerelle du tunnel sortant est aussi le créateur, elle peut construire un IV de sorte que n'importe lequel des pairs recevra la valeur correcte. Le créateur du tunnel pourrait même donner à la passerelle du tunnel entrant une série de valeurs IV que cette passerelle pourrait utiliser pour communiquer avec des participants individuels exactement une fois (bien que cela aurait des problèmes concernant la détection de collusion).

Cette technique pourrait être utilisée ultérieurement pour livrer des messages en cours de flux, ou pour permettre à la passerelle entrante d'informer le point de terminaison qu'il subit une attaque DoS ou qu'il est sur le point de défaillir. Pour le moment, il n'y a aucun plan pour exploiter ce canal de retour.

#### Messages tunnel de taille variable {#tunnel.variablesize}

Bien que la couche transport puisse avoir sa propre taille de message fixe ou variable, utilisant sa propre fragmentation, la couche tunnel peut à la place utiliser des messages tunnel de taille variable. La différence est une question de modèles de menace - une taille fixe au niveau de la couche transport aide à réduire les informations exposées aux adversaires externes (bien que l'analyse de flux globale fonctionne toujours), mais pour les adversaires internes (c'est-à-dire les participants tunnel) la taille du message est exposée. Les messages tunnel de taille fixe aident à réduire les informations exposées aux participants tunnel, mais ne cachent pas les informations exposées aux points de terminaison et passerelles tunnel. Les messages de bout en bout de taille fixe cachent les informations exposées à tous les pairs du réseau.

Comme toujours, c'est une question de savoir contre qui I2P essaie de se protéger. Les messages de tunnel de taille variable sont dangereux, car ils permettent aux participants d'utiliser la taille du message elle-même comme canal auxiliaire vers d'autres participants - par exemple, si vous voyez un message de 1337 octets, vous êtes sur le même tunnel qu'un autre pair complice. Même avec un ensemble fixe de tailles autorisées (1024, 2048, 4096, etc.), ce canal auxiliaire existe toujours car les pairs pourraient utiliser la fréquence de chaque taille comme porteuse (par exemple, deux messages de 1024 octets suivis d'un 8192). Les messages plus petits entraînent bien la surcharge des en-têtes (IV, ID de tunnel, portion de hachage, etc.), mais les messages de taille fixe plus importants augmentent soit la latence (due au regroupement) soit dramatiquement la surcharge (due au rembourrage). La fragmentation aide à amortir la surcharge, au prix d'une perte potentielle de messages due aux fragments perdus.

Les attaques par analyse temporelle sont également pertinentes lors de l'évaluation de l'efficacité des messages de taille fixe, bien qu'elles nécessitent une vue substantielle des modèles d'activité du réseau pour être efficaces. Les délais artificiels excessifs dans le tunnel seront détectés par le créateur du tunnel, en raison de tests périodiques, causant l'abandon de l'ensemble du tunnel et l'ajustement des profils des pairs qui s'y trouvent.

### Alternatives de Construction {#tunnel.building.alternatives}

Référence : [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf)

#### Ancienne méthode de construction de tunnel {#tunnel.building.old}

L'ancienne méthode de construction de tunnel, utilisée avant la version 0.6.1.10, est documentée sur [l'ancienne page des tunnels](/docs/historical/tunnel-alt). Il s'agissait d'une méthode "tout à la fois" ou "parallèle", où les messages étaient envoyés en parallèle à chacun des participants.

#### Construction télescopique à usage unique {#tunnel.building.oneshot}

NOTE : C'est la méthode actuelle.

Une question qui s'est posée concernant l'utilisation des tunnels exploratoires pour envoyer et recevoir des messages de création de tunnels est de savoir comment cela affecte la vulnérabilité du tunnel aux attaques de prédécesseur. Bien que les points terminaux et les passerelles de ces tunnels soient distribués de manière aléatoire à travers le réseau (incluant peut-être même le créateur du tunnel dans cet ensemble), une autre alternative est d'utiliser les chemins des tunnels eux-mêmes pour transmettre la requête et la réponse, comme c'est fait dans [Tor](https://www.torproject.org/). Ceci, cependant, peut conduire à des fuites durant la création du tunnel, permettant aux pairs de découvrir combien de sauts il y a plus loin dans le tunnel en surveillant le timing ou le nombre de paquets pendant que le tunnel est construit.

#### Construction télescopique "interactive" {#tunnel.building.telescoping}

Construire les sauts un par un avec un message à travers la partie existante du tunnel pour chacun. A des problèmes majeurs car les pairs peuvent compter les messages pour déterminer leur position dans le tunnel.

#### Tunnels non exploratoires pour la gestion {#tunnel.building.nonexploratory}

Une deuxième alternative au processus de construction de tunnel consiste à donner au router un ensemble supplémentaire de pools entrants et sortants non exploratoires, en les utilisant pour la demande et la réponse de tunnel. En supposant que le router ait une vue bien intégrée du réseau, cela ne devrait pas être nécessaire, mais si le router était partitionné d'une manière ou d'une autre, l'utilisation de pools non exploratoires pour la gestion des tunnels réduirait la fuite d'informations sur les pairs qui se trouvent dans la partition du router.

#### Livraison de Requête Exploratoire {#tunnel.building.exploratory}

Une troisième alternative, utilisée jusqu'à I2P 0.6.1.10, chiffrait par garlic encryption les messages de requête de tunnel individuels et les livrait aux relais individuellement, les transmettant à travers des tunnels exploratoires avec leur réponse revenant dans un tunnel exploratoire séparé. Cette stratégie a été abandonnée au profit de celle décrite ci-dessus.

#### Plus d'historique et de discussion {#history}

Avant l'introduction du Variable Tunnel Build Message, il y avait au moins deux problèmes :

1. La taille des messages (causée par un maximum de 8 sauts, alors que la longueur typique d'un tunnel est de 2 ou 3 sauts...
   et les recherches actuelles indiquent que plus de 3 sauts n'améliore pas l'anonymat) ;
2. Le taux élevé d'échecs de construction, en particulier pour les tunnels longs (et exploratoires), car tous les sauts doivent être d'accord ou le tunnel est rejeté.

Le VTBM a corrigé le #1 et amélioré le #2.

Welterde a proposé des modifications à la méthode parallèle pour permettre la reconfiguration. Sponge a proposé d'utiliser des 'tokens' d'une certaine sorte.

Tout étudiant de la construction de tunnels doit étudier les archives historiques menant à la méthode actuelle, en particulier les diverses vulnérabilités d'anonymat qui peuvent exister dans différentes méthodes. Les archives de courrier d'octobre 2005 sont particulièrement utiles. Comme indiqué dans [la spécification de création de tunnels](/docs/specs/tunnel-creation), la stratégie actuelle est née lors d'une discussion sur la liste de diffusion I2P entre Michael Rogers, Matthew Toseland (toad), et jrandom concernant l'attaque du prédécesseur.

#### Alternatives d'Ordonnancement des Pairs {#ordering}

Un ordonnancement moins strict est également possible, garantissant que bien que le saut après A puisse être B, B ne peut jamais être avant A. D'autres options de configuration incluent la possibilité que seuls les passerelles de tunnel entrant et les points de terminaison de tunnel sortant soient fixes, ou alternés selon un taux MTBF.

## Mélange/Traitement par lots {#tunnel.mixing}

Quelles stratégies devraient être utilisées au niveau de la passerelle et à chaque saut pour retarder, réorganiser, rediriger ou compléter les messages ? Dans quelle mesure ceci devrait-il être fait automatiquement, quelle part devrait être configurée comme paramètre par tunnel ou par saut, et comment le créateur du tunnel (et par extension, l'utilisateur) devrait-il contrôler cette opération ? Tout cela reste inconnu, à élaborer pour une version future.
