---
title: "Notes d’état I2P pour le 2005-01-04"
date: 2005-01-04
author: "jr"
description: "Premières notes d'état hebdomadaires de 2005 couvrant la croissance du réseau jusqu'à 160 routers, les fonctionnalités de la 0.4.2.6 et le développement de la 0.5"
categories: ["status"]
---

Salut à tous, il est temps de publier nos premières notes de statut hebdomadaires de 2005

* Index

1) État du réseau 2) 0.4.2.6 3) 0.5 4) jabber @ chat.i2p 5) ???

* 1) Net status

Au cours de la semaine écoulée, les choses ont été plutôt intéressantes sur le réseau - la veille du Nouvel An, des commentaires ont été publiés sur un site web populaire à propos d’i2p-bt et nous avons eu un petit afflux de nouveaux utilisateurs. À l’heure actuelle, il y a entre 120 et 150 routers sur le réseau, bien que cela ait culminé à 160 il y a quelques jours. Le réseau a toutefois tenu le coup, des pairs à haute capacité absorbant la charge excédentaire sans trop de perturbations pour les autres pairs. Certains utilisateurs fonctionnant sans limites de bande passante sur des liaisons très rapides ont signalé des débits de 2-300KBps, tandis que ceux disposant de moins de capacité se contentent des faibles 1-5KBps habituels.

Je crois me souvenir que Connelly a mentionné qu’il voyait plus de 300 routers différents sur quelques jours après le Nouvel An, ce qui indique un fort renouvellement. D’un autre côté, nous avons désormais 120-150 utilisateurs en ligne de façon stable, contre 80-90 auparavant, ce qui constitue une augmentation raisonnable. Nous ne voulons *pas* encore que cela croisse trop cependant, car il reste des problèmes d’implémentation connus qui doivent encore être résolus. Plus précisément, jusqu’à la version 0.6 [1], nous allons vouloir rester en dessous de 2-300 pairs afin de maintenir le nombre de threads (fils d’exécution) à un niveau raisonnable. Cependant, si quelqu’un veut aider à implémenter le transport UDP, nous pourrons y arriver beaucoup plus vite.

Au cours de la dernière semaine, j’ai consulté les statistiques publiées par les trackers i2p-bt et des gigaoctets de gros fichiers ont été transférés, avec certains rapports faisant état de 80-120KBps. IRC a connu plus d’accrocs que d’habitude depuis que ces commentaires ont été publiés sur ce site web, mais l’intervalle entre deux déconnexions reste de l’ordre de quelques heures. (d’après ce que je peux voir, le router sur lequel se trouve irc.duck.i2p tourne assez près de sa limite de bande passante, ce qui expliquerait les choses)

[1] http://www.i2p.net/roadmap#0.6

* 2) 0.4.2.6

Depuis la publication de la version 0.4.2.5, plusieurs correctifs et nouvelles fonctionnalités ont été ajoutés à CVS, que nous souhaitons déployer prochainement, notamment des correctifs de fiabilité pour la bibliothèque de streaming, une meilleure résilience face aux changements d’adresse IP, et l’intégration de l’implémentation du carnet d’adresses de ragnarok.

Si vous n’avez jamais entendu parler de l’addressbook (carnet d’adresses) ou ne l’avez jamais utilisé, pour faire court, il mettra automatiquement à jour votre fichier hosts.txt en récupérant périodiquement et en fusionnant les modifications depuis certains emplacements hébergés anonymement (par défaut http://dev.i2p/i2p/hosts.txt et http://duck.i2p/hosts.txt).

Vous n’aurez besoin de changer aucun fichier, de modifier la moindre configuration, ni d’exécuter des applications supplémentaires - il sera déployé dans le router I2P sous la forme d’un fichier .war standard.

Bien sûr, si vous *voulez vraiment* mettre les mains dans le cambouis avec le carnet d’adresses, vous êtes tout à fait libre de le faire - voir le site de Ragnarok [2] pour les détails. Les personnes qui ont déjà le carnet d’adresses déployé dans leur router devront effectuer quelques petites manipulations lors de la mise à niveau 0.4.2.6, mais cela fonctionnera avec tous vos anciens paramètres de configuration.

[2] http://ragnarok.i2p/

* 3) 0.5

Des chiffres, des chiffres, des chiffres ! Eh bien, comme je l’ai déjà dit, la version 0.5 va remanier la façon dont fonctionne le routage de tunnel, et des progrès sont réalisés sur ce front. Ces derniers jours, j’ai implémenté le nouveau code de chiffrement (et les tests unitaires), et une fois que ce sera opérationnel je publierai un document décrivant mes réflexions actuelles sur le comment, le quoi et le pourquoi du nouveau routage de tunnel. Je mets en place le chiffrement dès maintenant plutôt que plus tard afin que les gens puissent examiner ce que cela signifie de manière concrète, ainsi qu’identifier les points problématiques et formuler des suggestions d’amélioration. J’espère avoir le code opérationnel d’ici la fin de la semaine, donc il y aura peut-être d’autres documents publiés ce week-end. Aucune promesse toutefois.

* 4) jabber @ chat.i2p

jdot a mis en place un nouveau serveur Jabber, et il semble plutôt bien fonctionner, aussi bien pour les conversations en tête-à-tête que pour les discussions de groupe. Consultez les informations sur le forum [3]. Le canal de discussion des développeurs i2p restera l'irc #i2p, mais c'est toujours appréciable d'avoir des alternatives.

[3] http://forum.i2p.net/viewtopic.php?t=229

* 5) ???

OK, c'est à peu près tout ce que j'ai à mentionner pour le moment — je suis sûr qu'il se passe bien d'autres choses que d'autres voudront aborder, alors passez à la réunion dans 15 min à l'endroit habituel [4] et dites-nous ce qui se passe !

=jr
