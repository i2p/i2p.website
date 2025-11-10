---
title: "Notes d'état I2P du 2005-02-15"
date: 2005-02-15
author: "jr"
description: "Notes hebdomadaires sur l'état du développement I2P couvrant la croissance du réseau atteignant 211 routers, les préparatifs de la version 0.5 et i2p-bt 0.1.7"
categories: ["status"]
---

Bonjour, c'est encore ce moment de la semaine,

* Index

1) Statut du réseau 2) Statut 0.5 3) i2p-bt 0.1.7 4) ???

* 1) Net status

Bien qu'aucun nouveau bug ne soit apparu sur le réseau, la semaine dernière nous avons gagné en visibilité sur un site web p2p français populaire, ce qui a entraîné une augmentation à la fois du nombre d'utilisateurs et de l'activité bittorrent.  Au pic, nous avons atteint 211 routers sur le réseau, même si cela oscille entre 150 et 180 ces derniers temps.  L'utilisation de bande passante rapportée est également en hausse, mais malheureusement la fiabilité de l'irc s'est dégradée, l'un des serveurs ayant réduit ses limites de bande passante en raison de la charge.  Un certain nombre d'améliorations ont été apportées à la bibliothèque de streaming pour aider à cela, mais elles se trouvent sur la branche 0.5-pre, donc pas encore disponibles sur le réseau en production.

Un autre problème temporaire a été la panne de l’un des outproxies HTTP (proxies de sortie) (www1.squid.i2p), entraînant l’échec de 50 % des requêtes via l’outproxy.  Vous pouvez retirer temporairement cet outproxy en ouvrant votre configuration I2PTunnel [1], en modifiant l’eepProxy, et en changeant la ligne "Outproxies:" pour qu’elle ne contienne que "squid.i2p".  Nous espérons remettre l’autre en ligne bientôt afin d’augmenter la redondance.

[1] http://localhost:7657/i2ptunnel/index.jsp

* 2) 0.5 status

Il y a eu beaucoup d’avancées cette semaine sur la 0.5 (je parie que vous en avez marre de l’entendre, hein ?). Grâce à l’aide de postman, cervantes, duck, spaetz et d’une personne restée anonyme, nous faisons tourner un réseau de test avec le nouveau code depuis près d’une semaine et avons résolu un bon nombre de bogues que je n’avais pas vus sur mon réseau de test local.

Depuis environ une journée, les changements ont été mineurs, et je ne prévois plus de code important restant avant la sortie de la version 0.5. Il reste un peu de nettoyage, de documentation et d’assemblage, et il n’est pas inutile de laisser le réseau de test 0.5 tourner au cas où des bogues supplémentaires seraient décelés au fil du temps. Étant donné qu’il s’agira d’une VERSION NON RÉTROCOMPATIBLE, pour vous laisser le temps de planifier la mise à jour, je fixe une simple date limite à CE VENDREDI, date à laquelle la 0.5 sera publiée.

Comme bla l'a mentionné sur irc, les administrateurs d'eepsite(I2P Site) pourraient vouloir mettre leur site hors ligne jeudi ou vendredi et le laisser ainsi jusqu'à samedi, lorsque de nombreux utilisateurs auront effectué la mise à jour. Cela aidera à réduire l'effet d'une attaque par intersection (par exemple, si 90 % du réseau a migré vers 0.5 et que vous utilisez encore la version 0.4, si quelqu'un accède à votre eepsite(I2P Site), il saura que vous faites partie des 10 % de routers restants sur le réseau).

Je pourrais commencer à détailler ce qui a été mis à jour en 0.5, mais je finirais par m’étendre pendant des pages et des pages, alors peut-être que je ferais mieux d’attendre et de mettre tout ça dans la documentation que je devrais rédiger :)

* 3) i2p-bt 0.1.7

duck a mis au point une version correctrice pour la mise à jour 0.1.6 de la semaine dernière, et les retours disent qu’elle dépote (peut-être même /trop/, vu l’augmentation de l’utilisation du réseau ;)  Plus d’infos sur le forum i2p-bt [2]

[2] http://forum.i2p.net/viewtopic.php?t=300

* 4) ???

Beaucoup d'autres choses se passent dans les discussions IRC et sur le forum [3], trop pour les résumer brièvement. Peut-être que les personnes intéressées peuvent passer à la réunion pour nous donner des nouvelles et partager leurs réflexions ? Quoi qu'il en soit, à tout à l'heure.

=jr
