---
title: "Notes de statut d'I2P du 2006-04-18"
date: 2006-04-18
author: "jr"
description: "Améliorations du réseau de la version 0.6.1.16, analyse de l’effondrement de congestion lors de la création de tunnel, et mises à jour du développement de Feedspace"
categories: ["status"]
---

Salut tout le monde, c’est à nouveau mardi : place à nos notes de statut hebdomadaires.

* Index

1) Statut du réseau et 0.6.1.16 2) Création de tunnel et congestion 3) Feedspace 4) ???

* 1) Net status and 0.6.1.16

Avec 70 % du réseau mis à niveau vers 0.6.1.16, il semble que nous observions une amélioration par rapport aux versions précédentes, et, les problèmes corrigés dans cette version étant derrière nous, nous avons une vision plus claire de notre prochain goulot d’étranglement. Pour ceux qui ne sont pas encore sous 0.6.1.16, veuillez mettre à niveau dès que possible, car les versions précédentes rejettent arbitrairement les demandes de création de tunnel (même si le router dispose de ressources suffisantes pour participer à davantage de tunnels).

* 2) Tunnel creation and congestion

En ce moment, il semble que nous subissions ce qu'il est probablement le plus exact de décrire comme un effondrement par congestion - les demandes de création de tunnel sont rejetées parce que les routers sont à court de bande passante, donc davantage de demandes de création de tunnel sont envoyées dans l'espoir de trouver d'autres routers disposant de ressources libres, ce qui ne fait qu'augmenter la bande passante utilisée. Ce problème existe depuis notre passage au nouveau mécanisme de chiffrement pour la création de tunnel dans la version 0.6.1.10 et il est largement lié au fait que nous ne recevons pas de retour par saut concernant l'admission/le refus tant que (ou plus précisément, *sauf si*) la demande et la réponse n'ont pas parcouru la longueur de deux tunnels. Si l'un de ces pairs n'arrive pas à relayer le message, nous ne savons pas quel pair a échoué, quels pairs ont accepté et quels pairs l'ont explicitement rejeté.

Nous limitons déjà le nombre de requêtes concurrentes de création de tunnel en cours (et les tests montrent qu’augmenter le délai d’expiration n’aide pas), donc la solution traditionnelle de Nagle n’est pas suffisante. J’essaie actuellement quelques ajustements de notre code de traitement des requêtes afin de réduire la fréquence des pertes silencieuses de requêtes (par opposition aux rejets explicites), ainsi que de notre code de génération de requêtes pour réduire le niveau de concurrence sous charge. J’essaie aussi d’autres améliorations qui augmentent sensiblement les taux de réussite de la construction des tunnels, bien que celles-ci ne soient pas encore prêtes pour une utilisation sûre.

On voit la lumière au bout du tunnel, et je vous remercie de votre patience et de rester à nos côtés pendant que nous avançons. Je m’attends à ce que nous publiions une nouvelle version plus tard cette semaine pour déployer certaines des améliorations, après quoi nous réévaluerons l’état du réseau afin de voir si l’effondrement par congestion est résolu.

* 3) Feedspace

Frosk travaille d’arrache-pied sur Feedspace et a mis à jour quelques pages sur le site Trac, dont un nouveau document de présentation, une série de tâches en suspens, quelques détails de base de données, et plus encore. Passez faire un tour sur http://feedspace.i2p/ pour vous mettre au courant des dernières modifications, et peut-être bombarder Frosk de questions dès que vous en aurez l’occasion :)

* 4) ???

C’est à peu près tout ce que je suis prêt à discuter pour le moment, mais passez sur #i2p pour notre réunion plus tard dans la soirée (20 h UTC) afin d’en discuter davantage !

=jr
