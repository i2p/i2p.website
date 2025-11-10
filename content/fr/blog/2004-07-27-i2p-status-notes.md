---
title: "Notes de statut I2P du 2004-07-27"
date: 2004-07-27
author: "jr"
description: "Mise à jour hebdomadaire de l’état d’I2P portant sur les problèmes de performances de la version 0.3.3 et les optimisations à venir"
categories: ["status"]
---

Salut tout le monde, c'est l'heure de la séance de coup de gueule hebdomadaire

## Index :

1. 0.3.3 & current updates
2. NativeBigInteger
3. ???

## 1) 0.3.3

Nous avons publié la version 0.3.3 vendredi dernier et, après un jour ou deux de turbulences, elle semble se comporter correctement. Pas aussi bien que la 0.3.2.3, mais j’ai généralement pu rester sur irc.duck.i2p par sessions de 2 à 7 h. Cependant, comme j’ai vu beaucoup de personnes rencontrer des problèmes, j’ai lancé le logger (outil de journalisation) et surveillé en détail ce qui se passait. En bref, nous utilisions simplement plus de bande passante que nécessaire, ce qui provoquait de la congestion et des défaillances de tunnel (à cause de l’expiration des messages de test, etc.).

Ces derniers jours, je suis retourné dans le simulateur et j’y ai fait circuler une série de heartbeats (signaux de vie) à travers un réseau pour voir ce que nous pouvons améliorer, et nous avons toute une série de mises à jour qui arrivent sur cette base :

### netDb update to operate more efficiently

Les messages de recherche netDb existants font jusqu’à 10+KB, et si les réponses réussies sont fréquentes, les réponses infructueuses peuvent atteindre 30+KB (car les deux contenaient des structures RouterInfo complètes). Le nouveau netDb remplace ces structures RouterInfo complètes par le hachage du router - transformant des messages de 10KB et 30KB en messages de ~100 octets.

### throw out the SourceRouteBlock and SourceRouteReplyMessage

Ces structures étaient le vestige d'une ancienne idée, mais n'apportent aucune valeur à l'anonymat ni à la sécurité du système. En les abandonnant au profit d'un ensemble plus simple de points de données de réponse, nous réduisons considérablement la taille des messages de gestion de tunnel et divisons par deux le temps de garlic encryption.

### Mise à jour de netDb pour fonctionner plus efficacement

Le code était un peu 'bavard' pendant la création du tunnel, donc les messages inutiles ont été supprimés.

### rejeter les SourceRouteBlock et SourceRouteReplyMessage

Une partie du code cryptographique pour le garlic routing (routage « garlic ») utilisait un bourrage fixe basé sur certaines techniques de garlic routing que nous n’utilisons pas (quand je l’ai écrit en septembre et octobre, je pensais que nous allions faire du garlic routing à plusieurs sauts au lieu de tunnels).

Je travaille également à déterminer si je peux mener à bien la mise à jour complète du routage de tunnel afin d’ajouter les identifiants de tunnel par saut.

Comme vous pouvez le voir dans la feuille de route, cela couvre une grande partie de la version 0.4.1, mais comme la modification de la netDb impliquait la perte de la rétrocompatibilité, autant en profiter pour effectuer d’un coup toute une série de changements non rétrocompatibles.

Je fais encore tourner des tests dans le simulateur et je dois voir si je peux terminer la fonctionnalité d’ID de tunnel par saut, mais j’espère publier une nouvelle version correctrice d’ici un jour ou deux. Elle ne sera pas rétrocompatible, donc la mise à niveau sera un peu cahoteuse, mais ça devrait en valoir la peine.

## 2) NativeBigInteger

Iakin a apporté quelques mises à jour au code NativeBigInteger pour l’équipe Freenet, en optimisant certains éléments que nous n’utilisons pas, mais aussi en mettant au point du code de détection du processeur (CPU) que nous pouvons utiliser pour sélectionner automatiquement la bonne bibliothèque native. Cela signifie que nous pourrons déployer jbigi sous la forme d’une seule bibliothèque avec l’installation par défaut, et jbigi choisira la bonne sans avoir à demander quoi que ce soit à l’utilisateur. Il a également accepté de publier ses modifications et le nouveau code de détection du processeur afin que nous puissions l’intégrer à notre code source (youpi, Iakin !). Je ne sais pas quand cela sera déployé, mais je le signalerai lorsqu’il le sera, car ceux qui disposent déjà de bibliothèques jbigi auront probablement besoin d’une nouvelle bibliothèque.

## 3) ???

Eh bien, la semaine dernière, on a eu le nez dans le code, donc pas trop de mises à jour. Quelqu’un a autre chose à aborder ? Si c’est le cas, passez à la réunion ce soir, à 21 h GMT sur #i2p.

=jr
