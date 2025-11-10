---
title: "Notes sur l'état d'I2P du 2005-02-22"
date: 2005-02-22
author: "jr"
description: "Notes hebdomadaires sur l’état du développement d’I2P couvrant le succès de la version 0.5, le correctif 0.5.0.1 à venir, les stratégies d’ordonnancement des pairs de tunnel et les mises à jour d’azneti2p"
categories: ["status"]
---

Salut tout le monde, c'est l'heure de la mise à jour hebdomadaire

* Index

1) 0.5 2) Étapes suivantes 3) azneti2p 4) ???

* 1) 0.5

Comme vous l’avez sans doute entendu, nous avons enfin sorti la version 0.5 et, dans l’ensemble, elle se comporte plutôt bien. J’apprécie vraiment la rapidité avec laquelle les utilisateurs ont mis à jour — au cours de la première journée, 50 à 75 % du réseau était déjà passé en 0.5 ! Grâce à cette adoption rapide, nous avons pu constater plus rapidement l’impact des différents changements et, ce faisant, nous avons découvert un certain nombre de bogues. Même s’il reste encore quelques problèmes en suspens, nous publierons une nouvelle version 0.5.0.1 plus tard dans la soirée pour corriger les plus importants.

Petit bonus des bogues : c’était sympa de voir que les routers peuvent gérer des milliers de tunnels ;)

* 2) Next steps

Après la publication de la version 0.5.0.1, il pourrait y avoir une autre build pour tester quelques modifications dans la construction des tunnels exploratoires (par exemple en n'utilisant qu'un ou deux pairs non défaillants, le reste étant de haute capacité, au lieu que tous les pairs soient non défaillants).  Après cela, nous passerons à la 0.5.1, qui améliorera le débit du tunnel (en groupant plusieurs petits messages en un seul message de tunnel) et permettra à l'utilisateur d'avoir davantage de contrôle sur sa vulnérabilité à l'attaque du prédécesseur.

Ces contrôles prendront la forme de stratégies d’ordonnancement et de sélection des pairs par client, l’une pour la passerelle entrante et l’extrémité sortante, et l’autre pour le reste du tunnel.  Ébauche actuelle des stratégies que j’envisage :  = aléatoire (ce que nous avons actuellement)  = équilibré (tenter explicitement de réduire la fréquence à laquelle nous utilisons chaque pair)  = strict (si nous utilisons un jour A-->B-->C, ils restent dans cet ordre            lors des tunnels ultérieurs [limité dans le temps])  = souple (générer une clé aléatoire pour le client, calculer le XOR           entre cette clé et chaque pair, et toujours ordonner les pairs           sélectionnés selon la distance à cette clé [limité dans le temps])  = fixe (toujours utiliser les mêmes pairs par MBTF)

Quoi qu’il en soit, c’est le plan, même si je ne sais pas quelles stratégies seront déployées en premier. Vos suggestions sont plus que bienvenues :)

* 3) azneti2p

Les gens chez azureus ont travaillé dur avec toute une série de mises à jour, et leur dernier instantané b34 [1] semble inclure des correctifs liés à I2P.  Bien que je n’aie pas eu le temps d’auditer le code source depuis le dernier problème d’anonymat que j’ai soulevé, ils ont corrigé ce bug en particulier, donc si vous vous sentez d’humeur aventureuse, récupérez leur mise à jour et essayez-la !

[1] http://azureus.sourceforge.net/index_CVS.php

* 4) ???

Il se passe énormément de choses, et je suis sûr d’être loin d’avoir tout couvert. Venez faire un tour à la réunion dans quelques minutes pour voir ce qui se passe !

=jr
