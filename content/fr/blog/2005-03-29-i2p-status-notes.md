---
title: "I2P Status Notes for 2005-03-29"
date: 2005-03-29
author: "jr"
description: "Notes hebdomadaires sur l’état du développement d’I2P couvrant la version 0.5.0.5 avec le regroupement par lots, le protocole de transport UDP (SSU) et le stockage distribué Q"
categories: ["status"]
---

Salut à tous, c'est l'heure des notes de statut hebdomadaires

* Index

1) 0.5.0.5 2) UDP (SSU) 3) Q 4) ???

* 1) 0.5.0.5

Puisque vous avez tous fait un excellent travail en mettant à jour si rapidement vers la 0.5.0.4, nous publierons la nouvelle version 0.5.0.5 après la réunion. Comme évoqué la semaine dernière, le grand changement est l’intégration du code de regroupement (batching), qui regroupe plusieurs petits messages ensemble, plutôt que de leur attribuer à chacun leur propre message de tunnel complet de 1KB. Même si cela ne sera pas révolutionnaire en soi, cela devrait réduire substantiellement le nombre de messages transmis, ainsi que la bande passante utilisée, en particulier pour des services comme IRC.

Il y aura plus d’informations dans l’annonce de version, mais deux autres points importants accompagnent la 0.5.0.5 rev.  Premièrement, nous cessons la prise en charge des versions antérieures à 0.5.0.4 - il y a bien plus de 100 utilisateurs sur 0.5.0.4, et les versions précédentes présentent des problèmes conséquents.  Deuxièmement, la nouvelle version inclut une correction importante en matière d’anonymat; l’attaque visée, bien qu’elle nécessiterait un certain effort de développement pour être montée, n’est pas invraisemblable.  L’essentiel du changement concerne la manière dont nous gérons le netDb - plutôt que d’agir à la légère et de mettre en cache des entrées un peu partout, nous ne répondrons qu’aux requêtes netDb pour des éléments qui nous ont été explicitement fournis, que nous disposions ou non des données en question.

Comme toujours, il y a des corrections de bogues et quelques nouvelles fonctionnalités, mais davantage d'informations seront communiquées dans l'annonce de la version.

* 2) UDP (SSU)

Comme nous en avons discuté de façon intermittente au cours des 6 à 12 derniers mois, nous allons migrer vers l'UDP pour nos communications entre routers une fois la version 0.6 publiée. Pour nous faire avancer sur cette voie, nous avons mis une première ébauche du protocole de transport dans CVS @ http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/udp.html?rev=HEAD

C’est un protocole assez simple, dont les objectifs sont exposés dans le document, et qui exploite les capacités d’I2P pour à la fois authentifier et sécuriser les données, tout en divulguant le moins d’informations externes possible. Même la première partie de la poignée de main de connexion n’est pas identifiable pour quelqu’un qui n’exécute pas I2P. Le comportement du protocole n’est pas encore entièrement défini dans la spécification, par exemple comment se déclenchent les temporisateurs ou comment sont utilisés les trois différents indicateurs d’état semi-fiables, mais elle couvre les bases du chiffrement, de la paquetisation et de la perforation de NAT. Rien de tout cela n’a encore été implémenté, mais cela le sera bientôt, donc tout retour serait grandement apprécié !

* 3) Q

Aum travaille d'arrache-pied sur Q(uartermaster), un magasin de données distribué, et une première version de la documentation est en ligne [1]. Une des idées intéressantes qui s’y trouvent semble être de s’éloigner d’une DHT (table de hachage distribuée) « pure » au profit d’un système de type memcached [2], où chaque utilisateur effectue toutes les recherches entièrement *localement*, et demande les données proprement dites au serveur Q « directement » (enfin, via I2P). Quoi qu’il en soit, des choses intéressantes ; peut-être que si Aum est réveillé [3], on pourra lui arracher une mise à jour ?

[1] http://aum.i2p/q/ [2] http://www.danga.com/memcached/ [3] maudits fuseaux horaires !

* 4) ???

Il se passe bien plus de choses, et s'il restait plus de quelques minutes avant la réunion, je pourrais continuer, mais c'est la vie.  Passez faire un tour

# i2p dans un moment pour discuter.

=jr
