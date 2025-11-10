---
title: "Notes d'état d'I2P du 2005-03-08"
date: 2005-03-08
author: "jr"
description: "Notes hebdomadaires sur l'état du développement d'I2P couvrant les améliorations de la version 0.5.0.2, l'accent mis sur la fiabilité du réseau et les mises à jour des services de messagerie et de BitTorrent"
categories: ["status"]
---

Salut tout le monde, c'est l'heure de la mise à jour hebdomadaire

* Index

1) 0.5.0.2 2) mises à jour de mail.i2p 3) mises à jour d'i2p-bt 4) ???

* 1) 0.5.0.2

L’autre jour, nous avons publié la version 0.5.0.2 et une bonne partie du réseau a effectué la mise à niveau (youpi !) Des rapports nous parviennent indiquant que les pires problèmes de la 0.5.0.1 ont été éliminés, et dans l’ensemble tout semble bien fonctionner. Il reste encore quelques problèmes de fiabilité, mais la bibliothèque de streaming gère la situation (les connexions irc durant 12-24+ heures semblent être la norme). J’essaie de traquer certains des problèmes restants, mais ce serait vraiment, vraiment bien que tout le monde se mette à jour au plus vite.

Dans l’état actuel des choses, pour aller de l’avant, la fiabilité est reine.  Ce n’est que lorsque l’écrasante majorité des messages qui devraient réussir réussissent que des travaux seront engagés pour améliorer le débit.  Au-delà du préprocesseur de regroupement de tunnel, une autre dimension que nous pourrions vouloir explorer consiste à alimenter les profils avec davantage de données de latence.  Actuellement, nous n’utilisons que des messages de test et de gestion de tunnel pour déterminer le classement en "vitesse" de chaque pair, mais nous devrions probablement récupérer toutes les RTT (temps aller-retour) mesurables pour d’autres actions, comme netDb et même les messages client de bout en bout.  En revanche, il faudra les pondérer en conséquence, puisque pour un message de bout en bout, nous ne pouvons pas séparer les quatre composantes de la RTT mesurable (notre sortant, leur entrant, leur sortant, notre entrant).  Peut-être pouvons-nous recourir à un peu d’astuce garlic pour regrouper un message ciblant l’un de nos tunnels entrants en même temps que quelques messages sortants, en excluant ainsi les tunnels de l’autre côté de la boucle de mesure.

* 2) mail.i2p updates

OK, je ne sais pas quelles mises à jour postman nous réserve, mais il y aura une mise à jour pendant la réunion. Consultez les logs pour le savoir !

* 3) i2p-bt update

Je ne sais pas quelles mises à jour duck & gang ont pour nous, mais j’ai entendu quelques échos de progrès sur le canal. Peut-être qu’on pourra lui soutirer une mise à jour.

* 4) ???

Il se passe énormément de choses, mais si vous avez un point particulier à soulever et à discuter, passez à la réunion dans quelques minutes.  Ah, et petit rappel : si vous n'avez pas encore effectué la mise à jour, faites-le au plus vite (la mise à jour est d'une simplicité folle - téléchargez un fichier, cliquez sur un bouton)

=jr
