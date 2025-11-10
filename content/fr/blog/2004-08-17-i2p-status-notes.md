---
title: "Notes de statut d'I2P du 2004-08-17"
date: 2004-08-17
author: "jr"
description: "Mise à jour hebdomadaire de l’état d’I2P portant sur les problèmes de performances du réseau, les attaques par déni de service (DoS) et le développement de la DHT Stasher (table de hachage distribuée)"
categories: ["status"]
---

Salut tout le monde, c'est l'heure de la mise à jour

## Index :

1. Network status and 0.3.4.3
2. Stasher
3. ???

## 1) État du réseau et 0.3.4.3

Bien que le réseau ait été fonctionnel au cours de la semaine écoulée, il y a eu par moments pas mal de problèmes, entraînant une baisse spectaculaire de la fiabilité. La version 0.3.4.2 a grandement contribué à atténuer un DoS causé par certaines incompatibilités et des problèmes de synchronisation de l'heure - voyez le graphique des requêtes à la base de données du réseau montrant le DoS (pics hors échelle) qui a été stoppé par l'introduction de la 0.3.4.2. Malheureusement, cela a à son tour introduit son propre lot de problèmes, provoquant la retransmission d'un nombre significatif de messages, comme on peut le voir sur le graphique de bande passante. L'augmentation de la charge était aussi due à une véritable hausse de l'activité des utilisateurs, donc ce n'est pas /si/ fou ;) Mais quand même, c'était un problème.

Ces derniers jours, j’ai été plutôt égoïste. Nous avons testé et déployé un paquet de correctifs de bugs sur quelques routers, mais je ne l’ai pas encore publié, puisque j’ai rarement l’occasion de tester l’interaction des incompatibilités dans le logiciel lorsque j’exécute mes simulations. Vous avez donc subi un fonctionnement du réseau extrêmement merdique pendant que je peaufinais des réglages pour trouver des moyens de permettre aux routers de bien fonctionner quand beaucoup de routers sont à la ramasse. Nous progressons sur ce front - faire du profilage et éviter les pairs qui exploitent la base de données du réseau, gérer plus efficacement les files de requêtes de la base de données du réseau, et imposer tunnel diversification (diversification des tunnels).

Nous n’y sommes pas encore, mais je reste optimiste. Des tests sont en cours actuellement sur le réseau en production, et, lorsqu’il sera prêt, une version 0.3.4.3 sera publiée pour diffuser les résultats.

## 2) Stasher

Aum a fait un excellent travail sur sa DHT (table de hachage distribuée), et bien qu’elle présente actuellement des limitations importantes, elle semble prometteuse. Elle n’est clairement pas encore prête pour un usage général, mais si vous êtes partant pour l’aider à tester (ou à coder :), consultez le site et démarrez un nœud.

## 3) ???

C’est à peu près tout pour l’instant. Puisque la réunion aurait dû commencer il y a une minute, je ferais mieux de conclure. On se retrouve sur #i2p !

=jr
