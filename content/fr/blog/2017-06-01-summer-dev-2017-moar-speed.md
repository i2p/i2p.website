---
title: "I2P Summer Dev 2017 : Encore plus de vitesse !"
date: 2017-06-01
author: "str4d"
description: "Le Summer Dev de cette année sera axé sur la collecte de métriques et l’amélioration des performances du réseau."
categories: ["summer-dev"]
---

C’est à nouveau cette période de l’année ! Nous lançons notre programme de développement estival, au cours duquel nous nous concentrons sur un aspect particulier d’I2P pour le faire progresser. Pendant les trois prochains mois, nous encouragerons tant les nouveaux contributeurs que les membres actuels de la communauté à choisir une tâche et à prendre plaisir à la réaliser !

L’année dernière, nous nous sommes attachés à aider les utilisateurs et les développeurs à tirer parti d’I2P, en améliorant les outils pour les API et en apportant des améliorations aux applications qui fonctionnent via I2P. Cette année, nous voulons améliorer l’expérience utilisateur en travaillant sur un aspect qui concerne tout le monde : les performances.

Bien que les réseaux à routage en oignon soient souvent qualifiés de "réseaux à faible latence", faire transiter le trafic par des ordinateurs supplémentaires engendre une surcharge significative. La conception des tunnels unidirectionnels d'I2P fait que, par défaut, un aller-retour entre deux Destinations impliquera douze participants ! Améliorer les performances de ces participants contribuera à la fois à réduire la latence des connexions de bout en bout et à augmenter la qualité des tunnels à l'échelle de l'ensemble du réseau.

## Encore plus de vitesse !

Notre programme de développement cette année comportera quatre composantes :

### Measure

Nous ne pouvons pas savoir si nous améliorons les performances sans une ligne de base ! Nous allons créer un système de métriques pour collecter des données d’utilisation et de performance sur I2P d’une manière respectueuse de la vie privée, ainsi que porter divers outils de benchmarking pour qu’ils s’exécutent via I2P (p. ex. iperf3).

### Mesure

Il existe de nombreuses possibilités d’améliorer les performances de notre code existant, afin, par exemple, de réduire le surcoût de la participation aux tunnels. Nous étudierons des améliorations potentielles portant sur les primitives cryptographiques, les transports réseau (à la fois à la couche de liaison et de bout en bout), le profilage des pairs et la sélection du chemin de tunnel.

### Optimiser

Nous avons plusieurs propositions ouvertes pour améliorer l’évolutivité du réseau I2P (par exemple Prop115, Prop123, Prop124, Prop125, Prop138, Prop140). Nous travaillerons sur ces propositions et commencerons à mettre en œuvre celles finalisées dans les différents routers du réseau.

### Avancer

I2P est un réseau à commutation de paquets, comme l’Internet sur lequel il s’appuie. Cela nous offre une flexibilité importante quant à la manière dont nous acheminons les paquets, tant pour les performances que pour la confidentialité. La majeure partie de cette flexibilité reste inexplorée ! Nous souhaitons encourager la recherche sur la manière dont diverses techniques de la clearnet (internet public) visant à améliorer la bande passante peuvent être appliquées à I2P, et sur la façon dont elles pourraient affecter la confidentialité des participants au réseau.

## Take part in Summer Dev!

Nous avons bien d’autres idées de choses que nous aimerions réaliser dans ces domaines. Si vous souhaitez contribuer au développement de logiciels de confidentialité et d’anonymat, concevoir des protocoles (cryptographiques ou non), ou explorer des idées pour l’avenir, venez discuter avec nous sur IRC ou Twitter ! Nous sommes toujours heureux d’accueillir les nouveaux venus dans notre communauté. Nous enverrons également des autocollants I2P à tous les nouveaux contributeurs qui participeront !

Nous publierons ici au fur et à mesure, mais vous pouvez aussi suivre nos avancées et partager vos propres idées et contributions avec le hashtag #I2PSummer sur Twitter. Que l'été commence !
