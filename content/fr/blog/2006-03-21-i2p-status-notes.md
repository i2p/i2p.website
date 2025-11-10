---
title: "Notes de statut d'I2P du 2006-03-21"
date: 2006-03-21
author: "jr"
description: "Intégration de JRobin pour les statistiques réseau, les bots IRC biff et toopie, et l'annonce d'une nouvelle clé GPG"
categories: ["status"]
---

Salut à tous, c’est encore mardi

* Index

1) État du réseau 2) jrobin 3) biff et toopie 4) nouvelle clé 5) ???

* 1) Net status

La semaine passée a été assez stable, sans nouvelle version pour l'instant. J'ai continué à travailler sur la régulation du débit des tunnels et le fonctionnement à faible bande passante, mais, pour faciliter ces tests, j'ai intégré JRobin à la console web et à notre système de gestion des statistiques.

* 2) JRobin

JRobin [1] est un portage Java pur de RRDtool [2], qui nous permet de générer de jolis graphiques comme ceux que zzz génère en continu, avec très peu de surcharge mémoire. Nous l’avons configuré pour fonctionner entièrement en mémoire, de sorte qu’il n’y a pas de contention sur les verrous de fichiers, et le temps nécessaire pour mettre à jour la base de données est imperceptible. Il y a beaucoup de fonctionnalités intéressantes que JRobin peut offrir et que nous n’exploitons pas, mais la prochaine version inclura les fonctionnalités de base, ainsi qu’un moyen d’exporter les données dans un format que RRDtool peut comprendre.

[1] http://www.jrobin.org/ [2] http://people.ee.ethz.ch/~oetiker/webtools/rrdtool/

* 3) biff and toopie

Postman a travaillé d'arrache-pied sur des bots utiles, et je suis ravi d’annoncer que l’adorable biff est de retour [3] et vous prévient dès que vous avez du courrier (anonyme) pendant que vous êtes sur irc2p. En outre, postman a développé un tout nouveau bot pour nous - toopie - pour servir de bot d’information pour I2P/irc2p. Nous sommes encore en train d’alimenter toopie avec des FAQ, mais il rejoindra bientôt les canaux habituels. Merci postman !

[3] http://hq.postman.i2p/?page_id=15

* 4) new key

Pour ceux qui suivent de près, vous aurez remarqué que ma clé GPG expire dans quelques jours.  Ma nouvelle clé à l’adresse http://dev.i2p.net/~jrandom a pour empreinte 0209 9706 442E C4A9 91FA  B765 CE08 BC25 33DC 8D49 et l’ID de clé 33DC8D49.  Ce billet est signé avec mon ancienne clé, mais mes billets suivants (et versions) pour l’année à venir seront signés avec la nouvelle clé.

* 5) ???

C’est à peu près tout pour le moment - faites un saut sur #i2p dans quelques minutes pour notre réunion hebdomadaire et venez dire bonjour !

=jr
