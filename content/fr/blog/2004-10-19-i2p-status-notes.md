---
title: "Notes de statut I2P du 2004-10-19"
date: 2004-10-19
author: "jr"
description: "Mise à jour hebdomadaire de l’état d’I2P portant sur la sortie de la version 0.4.1.3, des améliorations des performances du tunnel, les progrès de la bibliothèque de streaming et le moteur de recherche files.i2p"
categories: ["status"]
---

Salut à tous, c'est encore mardi

## Index

1. 0.4.1.3
2. Tunnel test time, and send processing time
3. Streaming lib
4. files.i2p
5. ???

## 1) 0.4.1.3

La version 0.4.1.3 est sortie il y a un jour ou deux et il semble que la plupart des utilisateurs ont effectué la mise à jour (merci !). Le réseau fonctionne plutôt bien, mais il n’y a toujours pas d’amélioration radicale de la fiabilité. Cependant, les bogues du watchdog de la 0.4.1.2 ont disparu (ou du moins, personne ne les a signalés). Mon objectif est que cette version 0.4.1.3 soit le dernier correctif avant la 0.4.2, bien sûr, si quelque chose d’important apparaît et nécessite une correction, nous en publierons un autre.

## 2) Temps de test du tunnel, et temps de traitement de l'envoi

Les changements les plus significatifs de la version 0.4.1.3 concernaient les tests de tunnel - au lieu d’avoir une période de test fixe (30 secondes!), nous avons des délais d’expiration beaucoup plus agressifs dérivés des performances mesurées. C’est une bonne chose, car nous marquons désormais les tunnels comme défaillants lorsqu’ils sont trop lents pour faire quoi que ce soit d’utile. Cependant, c’est mauvais, car parfois les tunnels s’engorgent temporairement, et si nous les testons pendant cette période nous considérons comme défaillant un tunnel qui fonctionnerait autrement.

Un graphique récent montrant la durée d’un test de tunnel sur un router :

Ce sont généralement des temps de test de tunnel corrects - ils traversent 4 pairs distants (avec des tunnels à 2 sauts), ce qui donne à la plupart d’entre eux ~1-200ms par saut. Cependant, ce n’est pas toujours le cas, comme vous pouvez le voir - parfois cela prend de l’ordre de plusieurs secondes par saut.

C’est là qu’intervient le graphique suivant - le temps de file d’attente entre le moment où un router particulier a voulu envoyer un message et le moment où ce message a été vidé vers un socket:

Environ 95 % des valeurs sont inférieures à 50ms, mais les pics sont catastrophiques.

Nous devons éliminer ces pics, ainsi que contourner les situations où davantage de pairs sont défaillants. En l'état actuel, lorsque nous 'apprenons' qu'un pair fait échouer nos tunnels, nous n'apprenons en réalité rien de particulier à leur router - ces pics peuvent faire paraître lents même des pairs à haute capacité si cela coïncide avec un pic.

## 3) Bibliothèque de streaming

La deuxième composante pour contourner les tunnels défaillants sera assurée en partie par la bibliothèque de streaming - nous offrant une communication en streaming de bout en bout bien plus robuste. Cette discussion n'a rien de nouveau - la bibliothèque prendra en charge toutes les fonctionnalités impressionnantes dont nous parlons depuis un moment (et elle aura bien sûr sa part de bogues). Des progrès importants ont été réalisés sur ce front, et l'implémentation est probablement achevée à 60 %.

D’autres nouvelles quand il y en aura.

## 4) files.i2p

Ok, on a eu pas mal de nouveaux eepsites(I2P Sites) dernièrement, et c'est franchement génial. Je veux simplement signaler celui-ci en particulier, car il propose une fonctionnalité très pratique pour nous tous. Si vous n'avez pas visité files.i2p, c'est en gros un moteur de recherche de type Google, avec un cache des sites qu'il explore (de sorte que vous pouvez à la fois rechercher et parcourir lorsque l'eepsite(I2P Site) est hors ligne). Vraiment cool.

## 5) ???

Les notes de statut de cette semaine sont assez brèves, mais il se passe beaucoup de choses - - je n'ai tout simplement pas le temps d'en écrire davantage avant la réunion. Alors, passez sur #i2p dans quelques minutes et nous pourrons discuter de tout ce que j'ai bêtement oublié.

=jr
