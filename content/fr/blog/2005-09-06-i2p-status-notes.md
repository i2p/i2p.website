---
title: "Notes d'état d'I2P du 2005-09-06"
date: 2005-09-06
author: "jr"
description: "Mise à jour hebdomadaire couvrant la réussite de la publication de la version 0.6.0.5, les performances du floodfill netDb, les progrès de Syndie avec RSS et les noms familiers (pet names), ainsi que la nouvelle application de gestion du carnet d’adresses susidns"
categories: ["status"]
---

Salut à tous,

* Index

1) Statut du réseau 2) Statut de Syndie 3) susidns 4) ???

* 1) Net status

Comme beaucoup l'ont vu, la version 0.6.0.5 est sortie la semaine dernière après une brève révision 0.6.0.4, et jusqu'à présent, la fiabilité s'est grandement améliorée, et le réseau s'est développé plus que jamais. Il reste encore une marge d'amélioration, mais il semble que le nouveau netDb fonctionne comme prévu. Nous avons même mis le mécanisme de repli à l'épreuve - lorsque les pairs floodfill sont injoignables, les routers se replient sur le netDb kademlia, et l'autre jour, lorsque ce scénario s'est produit, la fiabilité d'irc et des eepsite (site I2P) n'a pas été sensiblement diminuée.

J’ai bien reçu une question concernant le fonctionnement du nouveau netDb, et j’ai publié la réponse [1] sur mon blog [2]. Comme toujours, si quelqu’un a des questions de ce genre, n’hésitez pas à me les transmettre, soit sur la liste ou hors liste, sur le forum, ou même sur votre blog ;)

[1] http://syndiemedia.i2p.net/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&entry=1125792000000&expand=true [2] http://syndiemedia.i2p.net/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=

* 2) Syndie status

Comme vous pouvez le voir sur syndiemedia.i2p (et http://syndiemedia.i2p.net/), des progrès importants ont été réalisés récemment, notamment RSS, les pet names (petnames, étiquettes personnelles), des contrôles d’administration, et les prémices d’une utilisation raisonnable de CSS. La plupart des suggestions d’Isamoor ont également été déployées, tout comme celles d’Adam, donc si quelqu’un a quelque chose en tête qu’il aimerait y voir, n’hésitez pas à m’envoyer un message !

Syndie est désormais assez proche de la version bêta, moment auquel il sera livré comme l’une des applications I2P par défaut et également distribué en tant que paquet autonome, si bien que toute aide serait grandement appréciée. Avec les tout derniers ajouts d’aujourd’hui (dans cvs), le "skinning" (personnalisation de l’apparence) de Syndie est également un jeu d’enfant - il suffit de créer un nouveau fichier syndie_standard.css dans votre répertoire i2p/docs/, et les styles spécifiés remplaceront les valeurs par défaut de Syndie. Plus d’informations à ce sujet sont disponibles sur mon blog [2].

* 3) susidns

Susi a concocté une autre application web pour nous - susidns [3]. Celle-ci sert d’interface simple pour gérer l’application Addressbook (carnet d’adresses) - ses entrées, abonnements, etc. Cela semble plutôt réussi, donc avec un peu de chance nous pourrons bientôt l’inclure parmi les applications par défaut, mais pour l’instant, c’est un jeu d’enfant de le récupérer depuis son eepsite(I2P Site), de l’enregistrer dans votre répertoire webapps, de redémarrer votre router, et tout est prêt.

[3] http://susi.i2p/?page_id=13

* 4) ???

Même si nous nous sommes assurément concentrés ces derniers temps sur le côté application cliente (et que nous continuerons à le faire), une grande partie de mon temps reste consacrée au fonctionnement du cœur du réseau, et des nouveautés enthousiasmantes arrivent - contournement des pare-feu et du NAT via des introductions, autoconfiguration de SSU améliorée, ordonnancement et sélection avancés des pairs, et même une gestion simple des routes restreintes. Côté site web, HalfEmpty a apporté quelques améliorations à nos feuilles de style (youpi !).

Bref, il se passe plein de choses, mais c’est à peu près tout ce que j’ai le temps de mentionner pour le moment ; passez donc à la réunion à 20 h UTC et venez dire bonjour :)

=jr
