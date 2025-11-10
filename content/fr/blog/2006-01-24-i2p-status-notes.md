---
title: "Notes de statut d'I2P du 2006-01-24"
date: 2006-01-24
author: "jr"
description: "Mise à jour de l’état du réseau, nouveau processus de construction de tunnel pour 0.6.2, et améliorations de la fiabilité"
categories: ["status"]
---

Salut à tous, mardi n'arrête pas de revenir...

* Index

1) État du réseau 2) Nouveau processus de compilation 3) ???

* 1) Net status

La semaine passée n'a pas apporté beaucoup de changements au réseau, la plupart des utilisateurs (77 %) étant passés à la dernière version. Cela dit, des changements importants se profilent, liés au nouveau processus de construction de tunnels, et ces changements provoqueront quelques à-coups pour ceux qui aident à tester les builds non publiées. Dans l'ensemble, toutefois, ceux qui utilisent les versions publiées devraient continuer à bénéficier d'un niveau de service assez fiable.

* 2) New build process

Dans le cadre de la refonte des tunnels pour la 0.6.2, nous modifions la procédure utilisée au sein du router afin de mieux s’adapter à l’évolution des conditions et de gérer la charge plus proprement. Il s’agit d’un précurseur à l’intégration des nouvelles stratégies de sélection des pairs et de la nouvelle cryptographie de création de tunnel, et c’est entièrement rétrocompatible. Cependant, au passage, nous nettoyons certaines bizarreries du processus de construction de tunnel, et bien que certaines de ces bizarreries aient aidé à masquer certains problèmes de fiabilité, elles ont pu conduire à un compromis anonymat/fiabilité sous-optimal. Plus précisément, elles utilisaient des tunnels à 1 saut de repli en cas de pannes catastrophiques - le nouveau processus préférera plutôt l’injoignabilité à l’utilisation de tunnels de repli, ce qui signifie que les utilisateurs constateront davantage de problèmes de fiabilité. Au moins, ils seront visibles jusqu’à ce que la source du problème de fiabilité des tunnels soit traitée.

Quoi qu’il en soit, pour le moment, le processus de build n’assure pas une fiabilité acceptable, mais dès que ce sera le cas, nous le publierons pour vous tous dans une prochaine version.

* 3) ???

Je sais que quelques autres travaillent sur différentes activités connexes, mais je leur laisse le soin de nous donner des nouvelles quand ils jugeront le moment opportun. Quoi qu’il en soit, on se retrouve tous à la réunion dans quelques minutes !

=jr
