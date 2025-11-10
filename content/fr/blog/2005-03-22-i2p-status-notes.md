---
title: "Notes de statut I2P du 2005-03-22"
date: 2005-03-22
author: "jr"
description: "Notes hebdomadaires sur l'état du développement d'I2P couvrant la version 0.5.0.3, la mise en œuvre du traitement par lots des messages de tunnel, et les outils de mise à jour automatique"
categories: ["status"]
---

Salut tout le monde, petite mise à jour rapide

* Index

1) 0.5.0.3 2) regroupement par lots 3) mise à jour 4) ???

* 0.5.0.3

La nouvelle version est sortie et la plupart d'entre vous ont mis à jour assez rapidement - merci !  Il y a eu quelques correctifs de bogues pour divers problèmes, mais rien de révolutionnaire - la mesure principale a consisté à écarter du réseau les utilisateurs des versions 0.5 et 0.5.0.1.  Depuis, je surveille le comportement du réseau, en analysant ce qui se passe, et même s'il y a eu quelques améliorations, il reste encore des points à régler.

Une nouvelle version sera publiée d’ici un jour ou deux, avec un correctif pour un problème que personne n’a encore rencontré, mais qui met en échec le nouveau code de traitement par lots. Il y aura également quelques outils pour automatiser le processus de mise à jour selon les préférences de l’utilisateur, ainsi que d’autres modifications mineures.

* batching

Comme je l’ai mentionné sur mon blog, il est possible de réduire de façon spectaculaire la bande passante et le nombre de messages requis sur le réseau en effectuant un batching (regroupement par lots) très simple des messages de tunnel - plutôt que de placer chaque message I2NP, quelle que soit sa taille, dans son propre message de tunnel, en ajoutant un bref délai nous pouvons regrouper jusqu’à 15, voire davantage, dans un seul message de tunnel.  Les gains les plus importants apparaîtront pour les services qui utilisent de petits messages (comme IRC), tandis que les transferts de gros fichiers seront peu affectés.  Le code pour effectuer le batching a été implémenté et testé, mais malheureusement il y a un bug sur le réseau en production qui ferait que tous les messages I2NP sauf le premier à l’intérieur d’un message de tunnel seraient perdus.  C’est pourquoi nous allons publier une version intermédiaire avec ce correctif, suivie de la version de batching une semaine environ plus tard.

* updating

Dans cette version intermédiaire, nous allons livrer une partie du code 'autoupdate' souvent évoqué. Nous disposons des outils pour rechercher périodiquement des annonces de mise à jour authentiques, télécharger la mise à jour de manière anonyme ou non, puis soit l’installer, soit simplement afficher un avis sur la console du router vous indiquant qu’elle est prête et en attente d’installation. La mise à jour elle-même utilisera désormais le nouveau format de mise à jour signée de smeghead, qui consiste essentiellement en la mise à jour accompagnée d’une signature DSA. Les clés utilisées pour vérifier cette signature seront fournies avec I2P et seront également configurables sur la console du router.

Le comportement par défaut consistera simplement à vérifier périodiquement l’existence d’annonces de mise à jour, sans y donner suite - il se contentera d’afficher sur la console du router une fonctionnalité "Mettre à jour maintenant" en un clic.  Il y aura de nombreux autres scénarios pour différents besoins des utilisateurs, mais ils devraient tous être pris en compte au moyen d’une nouvelle page de configuration.

* ???

Je me sens un peu patraque, donc ce qui précède n’entre pas vraiment dans tous les détails sur ce qui se passe.  Passez faire un tour à la réunion et comblez les lacunes :)

Oh, au passage, je publierai également une nouvelle clé PGP pour moi d’ici un jour ou deux (puisque celle-ci expire bientôt...), donc restez à l’affût.

=jr
