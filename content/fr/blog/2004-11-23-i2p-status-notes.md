---
title: "Notes d'état I2P du 2004-11-23"
date: 2004-11-23
author: "jr"
description: "Mise à jour hebdomadaire de l’état d’I2P portant sur la reprise du réseau, l’avancement des tests de la bibliothèque de streaming, les plans de la prochaine version 0.4.2 et les améliorations du carnet d’adresses"
categories: ["status"]
---

Salut tout le monde, il est temps de faire un point de situation

## Index :


1. Net status
2. Streaming lib
3. 0.4.2
4. Addressbook.py 0.3.1
5. ???

## 1) État du réseau

Après l’épisode de 2 à 3 jours de forte congestion de la semaine dernière, le réseau est revenu à la normale (probablement parce que nous avons arrêté les tests de charge sur le port BitTorrent ;). Le réseau est plutôt fiable depuis lors - nous avons quelques routers qui tournent sans interruption depuis 30 à plus de 40 jours, mais les connexions IRC ont encore connu quelques accrocs. D’un autre côté...

## 2) Bibliothèque de streaming

Depuis environ une semaine, nous effectuons beaucoup plus de tests en conditions réelles de la bibliothèque de streaming sur le réseau, et les résultats sont plutôt encourageants. Duck a mis en place un tunnel que les gens pouvaient utiliser pour accéder à son serveur IRC et, au cours de quelques jours, je n’ai eu que deux déconnexions intempestives (ce qui nous a aidés à traquer quelques bogues). Nous avons également une instance i2ptunnel pointant vers un outproxy (proxy sortant) squid que des personnes ont essayé, et le débit, la latence et la fiabilité sont nettement améliorés par rapport à l’ancienne bibliothèque, les deux ayant été testées côte à côte.

Dans l'ensemble, la bibliothèque de streaming semble suffisamment mature pour une première version. Il reste quelques éléments qui ne sont pas encore finalisés, mais c'est une amélioration significative par rapport à l'ancienne bibliothèque, et il faut bien vous donner une raison de mettre à niveau plus tard, non ? ;)

En fait, juste pour vous taquiner (ou peut-être vous inspirer à trouver quelques solutions), les principales choses que je vois arriver pour la streaming lib (bibliothèque de streaming) sont :
 - quelques algorithmes pour partager les informations de congestion et de RTT entre les flux (par destination cible ? par destination source ? pour toutes les destinations locales ?)
 - des optimisations supplémentaires pour les flux interactifs (dans l’implémentation actuelle, l’accent est surtout mis sur les flux de masse)
 - un usage plus explicite des fonctionnalités de la nouvelle streaming lib dans I2PTunnel, afin de réduire la surcharge par tunnel.
 - limitation de bande passante au niveau client (dans un sens ou les deux sur un flux, ou éventuellement partagée entre plusieurs flux). Cela viendrait s’ajouter à la limitation globale de bande passante du router, bien sûr.
 - divers contrôles permettant aux destinations de réguler le nombre de flux qu’elles acceptent ou créent (nous avons du code de base, mais il est largement désactivé)
 - des listes de contrôle d’accès (n’autorisant des flux que vers ou depuis certaines autres destinations connues)
 - des contrôles web et la surveillance de l’état de santé des différents flux, ainsi que la capacité de les fermer explicitement ou de les limiter

Vous pouvez probablement proposer d’autres idées aussi, mais ce n’est qu’une brève liste de choses que j’aimerais voir dans la bibliothèque de streaming, sans pour autant retarder la sortie de la version 0.4.2. Si quelqu’un est intéressé par l’une d’elles, s’il vous plaît, faites-le-moi savoir !

## 3) 0.4.2

Alors, si la streaming lib (bibliothèque de streaming) est au point, quand allons-nous sortir la version ? Le plan actuel est de la sortir d’ici la fin de la semaine, peut-être même dès demain. Il y a encore quelques autres choses en cours que je veux régler d’abord, et bien sûr il faut les tester, bla bla bla.

Le grand changement de la version 0.4.2 sera bien sûr la nouvelle bibliothèque de streaming. Du point de vue de l'API, elle est identique à l'ancienne bibliothèque - I2PTunnel et les flux SAM l'utilisent automatiquement, mais du point de vue des paquets, elle n'est *pas* rétrocompatible. Cela nous laisse face à un dilemme intéressant - rien dans I2P ne nous oblige à faire de la 0.4.2 une mise à niveau obligatoire, toutefois ceux qui ne mettront pas à jour ne pourront pas utiliser I2PTunnel - pas d'eepsites (Sites I2P), pas d'IRC, pas d'outproxy, pas d'email. Je ne veux pas aliéner nos utilisateurs de longue date en les forçant à mettre à niveau, mais je ne veux pas non plus les aliéner en laissant tout ce qui est utile cesser de fonctionner ;)

Je suis ouvert à me laisser convaincre dans un sens comme dans l'autre - il serait assez facile de modifier une seule ligne de code pour que la version 0.4.2 ne communique pas avec les versions plus anciennes, ou bien on peut simplement laisser les choses en l'état et laisser les gens mettre à jour lorsqu'ils iront sur le site web ou le forum pour se plaindre que tout est cassé. Qu'en pensez-vous ?

## 4) AddressBook.py 0.3.1

Ragnarok a publié une nouvelle version corrective pour son application de carnet d'adresses - voir `http://ragnarok.i2p/` pour plus d'informations (ou peut-être pourra-t-il nous faire un point lors de la réunion ?)

## 5) ???

Je sais qu’il y a beaucoup plus d’activité en ce moment — avec le port BitTorrent, susimail, le nouveau service d’hébergement de slacker, entre autres. Quelqu’un a autre chose à ajouter ? Si oui, passez à la réunion dans ~30 min sur #i2p, sur les serveurs IRC habituels !

=jr
