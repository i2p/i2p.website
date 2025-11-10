---
title: "Notes d'état I2P du 2006-02-28"
date: 2006-02-28
author: "jr"
description: "Améliorations du réseau avec la 0.6.1.12, feuille de route vers la 0.6.2 avec de nouvelles stratégies de sélection des pairs, et possibilités de mini-projets"
categories: ["status"]
---

Salut à tous, c'est reparti pour notre coup de gueule du mardi

* Index

1) Statut du réseau et 0.6.1.12 2) En route vers 0.6.2 3) Mini-projets 4) ???

* 1) Net status and 0.6.1.12

La semaine dernière a apporté des améliorations importantes sur le réseau, d’abord avec le déploiement à grande échelle de la 0.6.1.11 mardi dernier, suivi par la sortie de la 0.6.1.12 ce lundi (qui a été déployée sur 70 % du réseau jusqu’à présent - merci !) Dans l’ensemble, la situation s’est nettement améliorée par rapport à la 0.6.1.10 et aux versions précédentes - les taux de réussite de construction de tunnel sont supérieurs d’un ordre de grandeur sans aucun de ces tunnels de repli, la latence est en baisse, l’utilisation du processeur est en baisse, et le débit est en hausse. En outre, avec TCP entièrement désactivé, le taux de retransmission des paquets reste maîtrisé.

* 2) Road to 0.6.2

Il reste encore des améliorations à apporter au code de sélection des pairs, car nous observons toujours des taux de rejet de tunnels clients de 10-20 %, et les tunnels à haut débit (10+KBps) ne sont pas aussi courants qu'ils devraient l'être. D'un autre côté, maintenant que la charge CPU a tellement diminué, je peux exécuter un router supplémentaire sur dev.i2p.net sans causer de problèmes à mon router principal (qui héberge squid.i2p, www.i2p, cvs.i2p, syndiemedia.i2p, et d'autres, atteignant 2-300+KBps).

De plus, je teste quelques améliorations destinées aux personnes sur des réseaux très congestionnés (comment ça, il y en a qui ne le sont pas ?). Il semble y avoir des progrès de ce côté-là, mais des tests supplémentaires seront nécessaires. Cela devrait, je l’espère, aider les 4 ou 5 personnes sur irc2p qui semblent avoir du mal à maintenir des connexions fiables (et, bien sûr, aider aussi celles qui souffrent en silence des mêmes symptômes).

Une fois que cela fonctionnera bien, il nous restera encore du travail avant de pouvoir l’appeler 0.6.2 - nous avons besoin des nouvelles stratégies d’ordonnancement des pairs, en plus de ces stratégies améliorées de sélection des pairs.  Au minimum, j’aimerais obtenir trois nouvelles stratégies -
= ordonnancement strict (limitant le prédécesseur et le successeur de chaque pair,
   avec une rotation basée sur le MTBF)
= extrêmes fixes (en utilisant un pair fixe comme passerelle entrante et
   point de terminaison sortant)
= voisinage limité (en utilisant un ensemble limité de pairs comme premier saut
   distant)

Il existe d’autres stratégies intéressantes à approfondir, mais ces trois-là sont les plus pertinentes. Une fois qu’elles seront en place, nous serons fonctionnellement complets pour la version 0.6.2. Estimation approximative : mars/avril.

* 3) Miniprojects

Il y a plus de choses utiles à faire que je ne saurais en compter, mais je veux simplement attirer votre attention sur un billet publié sur mon blog décrivant cinq petits projets qu’un développeur pourrait monter rapidement sans y consacrer trop de temps [1]. Si quelqu’un souhaite s’y lancer, je suis sûr que nous allouerions quelques ressources [2] provenant du fonds général en guise de remerciement, même si je me doute que la plupart d’entre vous sont motivés par le hack et non par le cash ;)

[1] http://syndiemedia.i2p.net:8000/blog.jsp?     blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&     entry=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=/1140652800002 [2] http://www.i2p.net/halloffame

* 4) ???

Bref, voilà un petit récapitulatif de ce qui se passe, autant que je sache. Félicitations à cervantes également pour le 500e utilisateur du forum, au fait :) Comme toujours, passez sur #i2p pour la réunion dans quelques minutes !

=jr
