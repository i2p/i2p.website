---
title: "Tour d'horizon du développement estival : les API"
date: 2016-07-02
author: "str4d"
description: "Au cours du premier mois de Summer Dev, nous avons amélioré la facilité d'utilisation de nos API pour les développeurs Java, Android et Python."
categories: ["summer-dev"]
---

Summer Dev bat son plein : nous avons été occupés à huiler les rouages, à arrondir les angles et à mettre de l’ordre. C’est l’heure de notre premier tour d’horizon, pour vous mettre au courant des progrès que nous accomplissons !

## Mois des API

Notre objectif pour ce mois-ci était de "s'intégrer" - faire en sorte que nos API et bibliothèques fonctionnent au sein de l'infrastructure existante de diverses communautés, afin que les développeurs d'applications puissent travailler avec I2P plus efficacement et que les utilisateurs n'aient pas à se soucier des détails.

### Java / Android

Les bibliothèques clientes d'I2P sont désormais disponibles sur Maven Central ! Cela devrait rendre l'utilisation d'I2P dans leurs applications beaucoup plus simple pour les développeurs Java. Au lieu de devoir récupérer les bibliothèques depuis une installation existante, ils peuvent simplement ajouter I2P à leurs dépendances. La mise à niveau vers de nouvelles versions sera également bien plus facile.

La bibliothèque cliente Android d'I2P a également été mise à jour pour utiliser les nouvelles bibliothèques I2P. Cela signifie que les applications multiplateformes peuvent fonctionner nativement soit avec I2P Android, soit avec la version de bureau d'I2P.

### Java / Android

#### txi2p

Le plugin Twisted `txi2p` prend désormais en charge les ports internes à I2P et fonctionne de manière transparente via des API SAM locales, distantes et avec redirection de port. Consultez sa documentation pour les instructions d’utilisation et signalez tout problème sur GitHub.

#### i2psocket

La première version (bêta) de `i2psocket` a été publiée ! Il s’agit d’un remplacement direct de la bibliothèque Python standard `socket` qui ajoute la prise en charge d’I2P via la SAM API. Consultez sa page GitHub pour des instructions d’utilisation et pour signaler tout problème.

### Python

- zzz has been hard at work on Syndie, getting a headstart on Plugins month
- psi has been creating an I2P test network using i2pd, and in the process has found and fixed several i2pd bugs that will improve its compatibility with Java I2P

## Coming up: Apps month!

Nous sommes ravis de collaborer avec Tahoe-LAFS en juillet ! I2P héberge depuis longtemps l’une des plus grandes grilles publiques, utilisant une version patchée de Tahoe-LAFS. Pendant le mois des applications, nous les aiderons dans leurs travaux en cours visant à ajouter une prise en charge native d’I2P et de Tor, afin que les utilisateurs d’I2P puissent bénéficier de toutes les améliorations en amont.

Nous discuterons également avec plusieurs autres projets de leurs plans d’intégration à I2P et les aiderons pour la conception. Restez à l’écoute !

## Take part in Summer Dev!

Nous avons bien d’autres idées de projets à mener dans ces domaines. Si vous souhaitez contribuer au développement de logiciels de protection de la vie privée et de l’anonymat, concevoir des sites Web ou des interfaces faciles à utiliser, ou rédiger des guides pour les utilisateurs : venez discuter avec nous sur IRC ou Twitter ! Nous sommes toujours heureux d’accueillir les nouveaux venus au sein de notre communauté.

Nous publierons ici au fur et à mesure, mais vous pouvez aussi suivre nos avancées et partager vos propres idées et travaux avec le hashtag #I2PSummer sur Twitter. Place à l'été !
