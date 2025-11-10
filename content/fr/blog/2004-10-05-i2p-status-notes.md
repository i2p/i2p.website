---
title: "Notes d'état I2P du 2004-10-05"
date: 2004-10-05
author: "jr"
description: "Mise à jour hebdomadaire de l'état d'I2P couvrant la version 0.4.1.1, l'analyse des statistiques du réseau, les plans pour la bibliothèque de streaming 0.4.2 et l'eepserver intégré"
categories: ["status"]
---

Salut à tous, c'est l'heure de la mise à jour hebdomadaire

## Index :

1. 0.4.1.1 status
2. Pretty pictures
3. 0.4.1.2 and 0.4.2
4. Bundled eepserver
5. ???

## 1) 0.4.1.1 statut

Après une version 0.4.1 plutôt mouvementée (et la mise à jour 0.4.1.1 rapide qui a suivi), le réseau semble être revenu à la normale - une cinquantaine de pairs actifs en ce moment, et irc et eepsites(I2P Sites) sont accessibles. La plupart des problèmes étaient dus à des tests insuffisants du nouveau transport en dehors de conditions de laboratoire (par exemple, des sockets qui lâchent à des moments étranges, des délais excessifs, etc.). La prochaine fois que nous devrons apporter des modifications à cette couche, nous nous assurerons de les tester plus largement avant la publication.

## 2) Jolies images

Au cours des derniers jours, un grand nombre de mises à jour ont eu lieu dans CVS, et l'une des nouveautés ajoutées est un nouveau composant de journalisation des statistiques, qui nous permet d'extraire simplement les données de statistiques brutes au fur et à mesure qu'elles sont générées, plutôt que de se contenter des moyennes approximatives recueillies sur /stats.jsp. Grâce à cela, j'ai surveillé quelques statistiques clés sur plusieurs routers, et nous nous rapprochons de cerner les derniers problèmes de stabilité. Les statistiques brutes sont assez volumineuses (une exécution de 20 heures sur la machine de duck a généré presque 60MB de données), mais c'est pour cela que nous avons de jolis graphiques - `http://dev.i2p.net/~jrandom/stats/`

L’axe Y de la plupart d’entre eux est en millisecondes, tandis que l’axe X est en secondes. Il y a quelques points intéressants à noter. D’abord, client.sendAckTime.png est une assez bonne approximation du délai d’un aller-retour unique, car le message d’acquittement (ack) est envoyé avec la charge utile puis revient sur l’intégralité du chemin du tunnel ; ainsi, la grande majorité des près de 33 000 messages envoyés avec succès ont eu un temps aller-retour inférieur à 10 secondes. Si nous examinons ensuite client.sendsPerFailure.png à côté de client.sendAttemptAverage.png, nous constatons que les 563 envois échoués ont, pour la quasi-totalité, atteint le nombre maximal de réessais que nous autorisons (5 avec un délai d’expiration souple de 10 s par essai et un délai d’expiration strict de 60 s), tandis que la plupart des autres tentatives ont réussi du premier ou du deuxième coup.

Une autre image intéressante est client.timeout.png, qui remet fortement en question une hypothèse que j’avais - selon laquelle les échecs d’envoi de messages étaient corrélés à une forme de congestion locale. Les données représentées montrent que l’utilisation de la bande passante entrante variait fortement lors des échecs, qu’il n’y avait pas de pics réguliers dans le temps de traitement local des envois, et qu’il n’y avait apparemment aucun schéma quel qu’il soit avec la latence des tests de tunnel.

Les fichiers dbResponseTime.png et dbResponseTime2.png sont similaires à client.sendAckTime.png, sauf qu’ils correspondent à des messages netDb plutôt qu’à des messages client de bout en bout.

Le fichier transport.sendMessageFailedLifetime.png montre combien de temps nous conservons un message localement avant de le déclarer en échec pour une raison quelconque (par exemple, en raison de l’expiration atteinte ou parce que le pair qu’il cible est injoignable). Certains échecs sont inévitables, mais cette image montre qu’un nombre significatif échouent juste après le délai d’envoi local (10s). Il y a plusieurs choses que nous pouvons faire pour y remédier : - premièrement, nous pouvons rendre la shitlist (liste noire temporaire) plus adaptative - en augmentant exponentiellement la durée pendant laquelle un pair est sur la shitlist, plutôt qu’un palier fixe de 4 minutes chacun. (cela a déjà été intégré dans CVS) - deuxièmement, nous pouvons déclarer des messages en échec de manière proactive lorsqu’il semble qu’ils échoueront de toute façon. Pour ce faire, chaque connexion suit son débit d’envoi et, chaque fois qu’un nouveau message est ajouté à sa file d’attente, si le nombre d’octets déjà en file, divisé par le débit d’envoi, dépasse le temps restant avant l’expiration, le message est déclaré en échec immédiatement. Nous pourrions également utiliser cette métrique pour décider d’accepter ou non d’autres demandes de tunnel via un pair.

Bref, passons à la prochaine jolie image - transport.sendProcessingTime.png. Dans celle-ci, vous voyez que cette machine en particulier est rarement responsable d’une forte latence - typiquement 10-100ms, même si quelques pics atteignent 1s ou plus.

Chaque point tracé dans tunnel.participatingMessagesProcessed.png représente le nombre de messages qui ont été acheminés via un tunnel auquel le router a participé. En combinant cela avec la taille moyenne d’un message, on obtient une estimation de la charge réseau que le pair prend en charge pour les autres.

La dernière image est le tunnel.testSuccessTime.png, qui montre combien de temps il faut pour envoyer un message en sortant d’un tunnel et revenir chez nous via un autre tunnel entrant, nous donnant une estimation de la qualité de nos tunnels.

D’accord, assez de jolies images pour l’instant. Vous pouvez générer les données vous-même avec n’importe quelle version postérieure à 0.4.1.1-6 en définissant la propriété de configuration du router "stat.logFilters" à une liste de noms de statistiques, séparée par des virgules (récupérez les noms depuis la page /stats.jsp). Ceci est consigné dans stats.log, que vous pouvez traiter avec

```
java -cp lib/i2p.jar net.i2p.stat.StatLogFilter stat.log
```
qui le scinde en fichiers séparés pour chaque statistique, adaptés au chargement dans votre outil préféré (par exemple gnuplot).

## 3) 0.4.1.2 et 0.4.2

De nombreuses mises à jour ont été réalisées depuis la version 0.4.1.1 (voir l’historique pour la liste complète), mais aucun correctif critique pour l’instant. Nous les déploierons dans la prochaine version correctrice 0.4.1.2 plus tard cette semaine, une fois que certains bogues en suspens liés à l’autodétection de l’adresse IP auront été résolus.

La prochaine tâche majeure à ce stade sera d’atteindre la version 0.4.2, qui est actuellement envisagée comme une refonte majeure du traitement des tunnels. Cela va demander beaucoup de travail, ce qui impliquera de revoir le chiffrement et le traitement des messages ainsi que la gestion des pools de tunnels, mais c’est assez critique, car un attaquant pourrait assez facilement mener des attaques statistiques contre les tunnels à l’heure actuelle (par exemple, une attaque du prédécesseur avec un ordonnancement aléatoire des tunnels ou une collecte dans la netDb).

dm a toutefois soulevé la question de savoir s’il serait judicieux de faire la bibliothèque de streaming d’abord (actuellement prévue pour la version 0.4.3). L’avantage serait que le réseau deviendrait à la fois plus fiable et offrirait un meilleur débit, ce qui encouragerait d’autres développeurs à se lancer dans le développement d’applications clientes. Une fois cela en place, je pourrais alors revenir à la refonte du tunnel et traiter les problèmes de sécurité (non visibles par l’utilisateur).

Techniquement, les deux tâches prévues pour 0.4.2 et 0.4.3 sont orthogonales, et elles seront de toute façon réalisées, donc il ne semble pas y avoir beaucoup d’inconvénients à les intervertir. Je suis enclin à être d’accord avec dm et, à moins que quelqu’un ne puisse avancer des raisons de conserver 0.4.2 comme mise à jour du tunnel et 0.4.3 comme bibliothèque de streaming, nous les inverserons.

## 4) eepserver intégré

Comme mentionné dans les notes de version 0.4.1, nous avons intégré le logiciel et la configuration nécessaires pour exécuter un eepsite(site I2P) prêt à l'emploi - vous pouvez simplement déposer un fichier dans le répertoire ./eepsite/docroot/ et partager la destination I2P affichée sur la console du router.

Quelques personnes m'ont reproché mon zèle pour les fichiers .war - malheureusement, la plupart des applications nécessitent un peu plus de travail que de simplement déposer un fichier dans le répertoire ./eepsite/webapps/. J'ai rédigé un court tutoriel sur l'exécution du moteur de blog blojsom, et vous pouvez voir à quoi cela ressemble sur le site de detonate.

## 5) ???

C'est à peu près tout ce que j'ai pour le moment - passez à la réunion dans 90 minutes si vous voulez en discuter.

=jr
