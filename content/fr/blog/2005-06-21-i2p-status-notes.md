---
title: "Notes d'état I2P du 2005-06-21"
date: 2005-06-21
author: "jr"
description: "Mise à jour hebdomadaire portant sur le retour de voyage du développeur, les progrès du transport SSU, l’achèvement de la prime pour les tests unitaires et une interruption de service"
categories: ["status"]
---

Salut à tous, il est temps de reprendre nos notes de suivi hebdomadaires

* Index

1) Statut du développeur 2) Statut du développement 3) Prime pour tests unitaires 4) Interruption de service 5) ???

* 1) Dev[eloper] status

Après 4 villes dans 4 pays, je m’installe enfin et je me replonge dans le code. La semaine dernière, j’ai enfin réuni les dernières pièces pour un ordinateur portable, je ne dors plus sur les canapés des uns et des autres, et même si je n’ai pas d’accès Internet à la maison, il y a de nombreux cybercafés autour, donc l’accès est fiable (seulement peu fréquent et cher).

Ce dernier point signifie que je ne traînerai pas sur irc autant qu’avant, au moins jusqu’à l’automne (j’ai une sous-location jusqu’en août environ et je chercherai un endroit où je peux avoir un accès au réseau 24 h/24 et 7 j/7). Cela ne veut toutefois pas dire que je vais en faire moins - je travaillerai surtout sur mon propre réseau de test, en publiant des builds pour des tests sur le réseau public (et, euh, ah oui, des releases). Cela signifie toutefois que nous voudrons peut-être déplacer certaines discussions qui se déroulaient de manière informelle sur #i2p vers la liste [1] et/ou le forum [2] (je lis toujours l’historique de #i2p, cela dit). Je n’ai pas encore trouvé d’endroit convenable où aller pour nos réunions de développement, donc je n’y serai pas cette semaine, mais peut-être que d’ici la semaine prochaine j’en aurai trouvé un.

Enfin bref, assez parlé de moi.

[1] http://dev.i2p.net/pipermail/i2p/ [2] http://forum.i2p.net/

* 2) Dev[elopment] status

Pendant mon déménagement, je me suis concentré sur deux axes principaux : la documentation et le transport SSU (ce dernier uniquement depuis que j’ai eu l’ordinateur portable). La documentation est toujours en cours, avec une grande présentation d’ensemble assez intimidante ainsi qu’une série de documents d’implémentation plus petits (couvrant des éléments tels que l’organisation du code source, l’interaction des composants, etc.).

Les avancées sur SSU se déroulent bien : les nouveaux champs de bits d’acquittement (ACK) sont en place, la communication gère efficacement les pertes (simulées), les débits sont adaptés aux différentes conditions et j’ai corrigé certains des bogues les plus pénibles rencontrés auparavant. Je continue toutefois à tester ces modifications et, lorsqu’il sera opportun, nous planifierons une série de tests réseau en conditions réelles pour lesquels nous aurons besoin de volontaires pour y participer. Plus d’informations à ce sujet dès que ce sera disponible.

* 3) Unit test bounty

Je suis heureux d’annoncer que Comwiz a proposé une série de correctifs pour réclamer la première phase de la prime pour tests unitaires [3] ! Nous sommes encore en train de régler quelques détails mineurs des correctifs, mais j’ai reçu les mises à jour et généré, au besoin, les rapports junit et clover. Je m’attends à ce que nous ayons les correctifs dans CVS sous peu, après quoi nous publierons la documentation de tests de Comwiz.

Comme clover est un produit commercial (gratuit pour les développeurs OSS [4]), seuls ceux qui ont installé clover et reçu leur licence clover pourront générer les rapports clover. Dans tous les cas, nous publierons périodiquement les rapports clover sur le web, afin que ceux qui n'ont pas installé clover puissent tout de même voir les performances de notre suite de tests.

[3] http://www.i2p.net/bounties_unittest [4] http://www.cenqua.com/clover/

* 4) Service outage

Comme beaucoup l'ont probablement remarqué, (au moins) un des outproxies (proxies de sortie) est hors ligne (squid.i2p), tout comme www.i2p, dev.i2p, cvs.i2p et mon blog. Ces événements ne sont pas indépendants - la machine qui les héberge est hors service.

=jr
