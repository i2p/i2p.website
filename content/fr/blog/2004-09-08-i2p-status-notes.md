---
title: "Notes de statut d'I2P du 2004-09-08"
date: 2004-09-08
author: "jr"
description: "Mise à jour hebdomadaire de l’état d’I2P couvrant la version 0.4, les problèmes de capacité du réseau, les mises à jour du site web et les améliorations de l’interface I2PTunnel"
categories: ["status"]
---

Salut à tous, désolé pour le retard...

## Index :

1. 0.4
2. Capacity and overload
3. Website updates
4. I2PTunnel web interface
5. Roadmap and todo
6. ???

## 1) 0.4

Comme vous l’avez sans doute tous vu, la version 0.4 est sortie l’autre jour et, dans l’ensemble, ça se passe plutôt bien. Difficile de croire que cela fait six mois que la 0.3 est sortie (et un an que le SDK 1.0 a été publié), mais nous avons parcouru beaucoup de chemin, et votre travail acharné, votre enthousiasme et votre patience à tous ont fait des merveilles. Félicitations, et merci !

Comme pour toute bonne version, dès sa sortie nous avons trouvé quelques problèmes, et ces derniers jours nous avons accumulé des rapports de bogues et corrigé à tour de bras (vous pouvez suivre les modifications au fur et à mesure qu’elles sont corrigées). Il nous reste encore quelques bogues à écraser avant de publier la prochaine version, mais cela devrait être réglé d’ici un jour ou deux.

## 2) Capacité et surcharge

Nous avons observé des allocations de tunnels assez biaisées au cours des dernières versions, et même si certaines sont liées à des bogues (dont deux ont été corrigés depuis la sortie de la 0.4), il reste une question générale d’algorithme - quand un router doit-il cesser d’accepter davantage de tunnels ?

Il y a quelques révisions, nous avons ajouté du code de limitation de débit pour rejeter les demandes de participation à un tunnel si le router était surchargé (le temps de traitement local des messages dépasse 1s), et cela a considérablement aidé. Cependant, deux aspects de cet algorithme simple ne sont pas pris en compte : - lorsque notre bande passante est saturée, notre temps de traitement local peut rester rapide, nous continuerions donc à accepter davantage de demandes de participation à un tunnel - lorsqu’un seul pair participe à "trop" de tunnels, lorsqu’ils échouent, cela nuit davantage au réseau.

La première question se règle assez facilement en activant simplement le limiteur de bande passante (puisque la limitation de bande passante ralentit le temps de traitement des messages en fonction du délai de bande passante). La seconde est plus compliquée et nécessite à la fois davantage de recherche et davantage de simulations. Je pense à quelque chose comme le rejet probabiliste des demandes de tunnel, basé sur le rapport entre les tunnels auxquels nous participons et les tunnels demandés au réseau, avec un « facteur de bienveillance » de base, en fixant P(reject) = 0 si notre participation est inférieure à ce niveau.

Mais comme je l'ai dit, davantage de travail et de simulation sont nécessaires.

## 3) Mises à jour du site Web

Maintenant que nous disposons de la nouvelle interface web d'I2P, pratiquement toute notre ancienne documentation destinée aux utilisateurs finaux est obsolète. Nous avons besoin d'aide pour parcourir ces pages et les mettre à jour afin de décrire la situation actuelle. Comme l'ont suggéré duck et d'autres, nous avons besoin d'un nouveau 'guide de mise en route' au-delà du fichier README de `http://localhost:7657/` - quelque chose qui permette aux gens de démarrer et d'utiliser le système.

In addition, our new web interface has plenty of room for integrating context sensitive help. As you can see on the bundled help.jsp, "hmm. we should probably have some help text here."

Ce serait probablement une bonne idée si nous pouvions ajouter des liens 'À propos' et/ou 'Dépannage' sur les différentes pages, expliquant ce que signifient les éléments et comment les utiliser.

## 4) Interface web d'I2PTunnel

Qualifier la nouvelle interface `http://localhost:7657/i2ptunnel/` de « spartiate » serait un euphémisme. Il reste beaucoup de travail pour la rapprocher d’un état utilisable — pour l’instant, la fonctionnalité est techniquement là, mais il faut vraiment savoir ce qui se passe en coulisses pour y comprendre quelque chose. Je pense que duck a peut-être d’autres idées à ce sujet à évoquer pendant la réunion.

## 5) Feuille de route et tâches à faire

Je me suis relâché sur la mise à jour de la feuille de route, mais la réalité, c’est que nous avons encore des révisions devant nous. Pour aider à expliquer ce que je considère comme les « principaux problèmes », j’ai préparé une nouvelle liste de tâches, qui apporte quelques précisions sur chacun. Je pense qu’à ce stade, nous devrions être assez ouverts à réexaminer nos options et peut-être à retravailler la feuille de route.

Une chose que j’ai oublié de mentionner dans cette liste de tâches est que, lors de l’ajout du protocole de connexion léger, nous pouvons inclure une détection automatique (optionnelle) de l’adresse IP. Cela peut être « dangereux » (c’est pourquoi ce sera optionnel), mais cela réduira considérablement le nombre de demandes d’assistance que nous recevons :)

Quoi qu’il en soit, les problèmes inscrits sur la liste des tâches sont ceux que nous avons prévus pour diverses versions, et ils ne seront très certainement pas tous dans la 1.0 ni même la 2.0. J’ai esquissé quelques pistes différentes de priorisation et de versions, mais ce n’est pas encore gravé dans le marbre. Toutefois, si des personnes peuvent identifier d’autres gros sujets à venir, ce serait très apprécié, car un problème non planifié est toujours un vrai casse-pieds.

## 6) ???

Ok, c’est tout ce que j’ai pour l’instant (et tant mieux, puisque la réunion commence dans quelques minutes). Passez faire un tour sur #i2p sur irc.freenode.net, www.invisiblechat.com, ou irc.duck.i2p à 21 h GMT pour continuer la discussion.
