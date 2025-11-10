---
title: "Notes sur l’état d’I2P du 2005-09-13"
date: 2005-09-13
author: "jr"
description: "Mise à jour hebdomadaire couvrant les introductions SSU pour la perforation de NAT, l’avancement de la prime pour les tests unitaires, la discussion de la feuille de route des applications clientes, et la suppression du mode de livraison garanti déprécié"
categories: ["status"]
---

Salut tout le monde, c’est l’heure des notes de statut hebdomadaires

* Index

1) État du réseau 2) SSU introductions / percement de NAT 3) Primes 4) Instructions pour l'application cliente 5) ???

* 1) Net status

Nous poursuivons notre progression avec la version 0.6.0.5 déployée sur le réseau, et presque tout le monde a effectué la mise à jour, beaucoup exécutant l’une des builds publiées depuis (CVS HEAD est 0.6.0.5-9 en ce moment). Dans l’ensemble, tout fonctionne encore bien, même si j’ai observé une augmentation substantielle du trafic réseau, probablement due à une utilisation accrue de i2p-bt ou i2phex. L’un des serveurs IRC a eu un petit couac hier soir, mais l’autre a tenu bon et tout semble s’être bien remis. Cependant, les builds CVS ont apporté des améliorations substantielles dans la gestion des erreurs et d’autres fonctionnalités, donc je m’attends à ce que nous ayons une nouvelle version plus tard cette semaine.

* 2) SSU introductions / NAT hole punching

Les dernières versions dans CVS incluent la prise en charge des introductions SSU longuement discutées [1], nous permettant d’effectuer une perforation de NAT décentralisée pour les utilisateurs derrière un NAT ou un pare-feu qu’ils ne contrôlent pas. Bien qu’il ne prenne pas en charge le NAT symétrique, cela couvre la majorité des cas. Les retours du terrain sont bons, mais seuls les utilisateurs avec les dernières versions peuvent contacter les utilisateurs derrière un NAT — les anciennes versions doivent attendre que ces utilisateurs les contactent en premier. Pour cette raison, nous publierons le code dans une version plus tôt que d’habitude afin de réduire la durée pendant laquelle ces routes restreintes restent en place.

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/udp.html?rev=HEAD#introduction

* 3) Bounties

J’ai consulté plus tôt la liste de diffusion i2p-cvs et j’ai remarqué un paquet de commits de la part de Comwiz concernant ce qui semble être la phase 3 de la prime pour les tests unitaires [2]. Peut-être que Comwiz pourra nous faire un point d’avancement à ce sujet pendant la réunion de ce soir.

[2] http://www.i2p.net/bounty_unittests

Au passage, grâce à la suggestion d'une personne anonyme, j'ai légèrement mis à jour le Hall of Fame [3], en y ajoutant les dates de contribution, en regroupant plusieurs dons d'une même personne et en convertissant le tout dans une devise unique. Merci encore à toutes les personnes qui ont contribué, et s'il y a des informations incorrectes publiées ou si quelque chose manque, veuillez me contacter et cela sera mis à jour.

[3] http://www.i2p.net/halloffame

* 4) Client app directions

L’un des ajustements les plus récents dans les builds CVS actuels est la suppression de l’ancien mode de livraison mode=guaranteed. Je n’avais pas réalisé que quelqu’un l’utilisait encore (et c’est entièrement inutile, puisque nous disposons de la bibliothèque de streaming complète depuis un an maintenant), mais en fouillant dans i2phex, j’ai remarqué que ce flag était activé. Avec la version actuelle (et toutes les versions suivantes), i2phex utilisera simplement mode=best_effort, ce qui devrait améliorer ses performances.

Si j'en parle (au-delà de l'évoquer pour les utilisateurs d'i2phex), c'est pour vous demander ce dont vous avez besoin côté client d'I2P, et si je devrais consacrer une partie de mon temps à aider à en réaliser certains. De mémoire, je vois beaucoup de travail possible sur différents aspects :  = Syndie : publication simplifiée, synchronisation automatisée, données
    import, intégration applicative (avec i2p-bt, susimail, i2phex, etc.),
    prise en charge des fils de discussion pour permettre un comportement de type forum, et plus encore.
  = eepproxy : meilleur débit, prise en charge du pipelining
  = i2phex : maintenance générale (je ne l'ai pas assez utilisé pour connaître ses
    points de friction)
  = irc : meilleure résilience, détecter les indisponibilités récurrentes des serveurs irc et
    éviter les serveurs en panne, filtrer les actions CTCP localement plutôt que sur le
    serveur, proxy DCC
  = Amélioration de la prise en charge x64 avec jbigi, jcpuid et le service wrapper
  = intégration au systray (zone de notification), et suppression de cette fenêtre DOS
  = Amélioration des contrôles de bande passante pour le bursting (rafales)
  = Amélioration du contrôle de congestion pour les surcharges réseau et CPU, ainsi
    que des mécanismes de reprise.
  = Exposer davantage de fonctionnalités et documenter les capacités disponibles de
    la console du router pour les applications tierces
  = Documentation pour développeurs de clients
  = Documentation d'introduction à I2P

En plus, au-delà de tout ça, il y a le reste des trucs sur la feuille de route [4] et la liste de tâches [5]. Je sais ce dont nous avons besoin sur le plan technique, mais je ne sais pas ce dont *vous* avez besoin du point de vue utilisateur. Parlez-moi, vous voulez quoi ?

[4] http://www.i2p.net/roadmap [5] http://www.i2p.net/todo

* 5) ???

Il y a d’autres choses en cours dans le cœur du router et du côté du développement d’applications, au-delà de ce qui est mentionné ci-dessus, mais tout n’est pas prêt à être utilisé pour le moment. Si quelqu’un a quelque chose à aborder, passez à la réunion ce soir à 20 h UTC sur #i2p !

=jr
