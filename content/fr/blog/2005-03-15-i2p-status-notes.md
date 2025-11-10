---
title: "Notes sur l'état d'I2P du 2005-03-15"
date: 2005-03-15
author: "jr"
description: "Notes hebdomadaires sur l'état du développement d'I2P couvrant l'analyse des performances du réseau, les améliorations du calcul de la vitesse et le développement de Feedspace"
categories: ["status"]
---

Salut à tous, c’est l’heure de la mise à jour hebdomadaire

* Index

1) Statut du réseau
2) Feedspace (espace des flux)
3) ???

* 1) Net status

Au cours de la semaine écoulée, j’ai passé une grande partie de mon temps à analyser le comportement du réseau, à suivre des statistiques et à essayer de reproduire divers événements dans le simulateur.  Si certains des comportements étranges du réseau peuvent être attribués aux deux douzaines environ de routers encore sur d’anciennes versions, le facteur clé est que nos calculs de vitesse ne nous donnent pas de bonnes données — nous ne sommes pas en mesure d’identifier correctement les pairs capables d’acheminer des données rapidement.  Par le passé, ce n’était pas vraiment un problème, puisqu’un bug nous amenait à utiliser les 8 pairs à la plus forte capacité comme pool 'fast', plutôt que de construire de véritables niveaux dérivés de la capacité.  Notre calcul de vitesse actuel est dérivé d’un test périodique de latence (le RTT d’un test de tunnel, en particulier), mais cela ne fournit pas suffisamment de données pour avoir confiance dans la valeur. Ce dont nous avons besoin, c’est d’une meilleure façon de collecter davantage de points de données tout en permettant aux pairs 'high capacity' d’être promus au niveau 'fast', si nécessaire.

Pour vérifier que c’est bien le problème principal auquel nous sommes confrontés, j’ai un peu triché et ajouté une fonctionnalité permettant de sélectionner manuellement quels pairs doivent être utilisés dans la sélection d’un pool de tunnels particulier. Avec ces pairs explicitement choisis, j’ai passé plus de deux jours sur irc sans déconnexion et avec des performances assez raisonnables avec un autre service que je contrôle. Depuis environ deux jours, je teste un nouveau calculateur de vitesse s’appuyant sur de nouvelles statistiques et, bien qu’il ait amélioré la sélection, il présente encore des problèmes. J’ai étudié quelques alternatives cet après-midi, mais il reste du travail pour les tester sur le réseau.

* 2) Feedspace

Frosk a mis en ligne une autre révision de la doc i2pcontent/fusenet, sauf que maintenant c’est à une nouvelle adresse et sous un nouveau nom : http://feedspace.i2p/ - voir soit orion [1] soit mon blog [2] pour la destination. Tout cela semble vraiment prometteur, à la fois du point de vue "hé, des fonctionnalités qui déchirent" et "hé, ça va aider l’anonymat d’I2P". Frosk et son équipe travaillent dur, mais ils sont assurément à la recherche de retours (et d’aide). Peut-être pourrions-nous demander à Frosk de nous faire un point lors de la réunion ?

[1] http://orion.i2p/#feedspace.i2p [2] http://jrandom.dev.i2p/

* 3) ???

D’accord, ça n’a peut-être pas l’air de grand-chose, mais il se passe vraiment beaucoup de choses :) Je suis certain d’avoir aussi raté certaines choses, alors passez faire un tour à la réunion pour voir ce qu’il en est.

=jr
